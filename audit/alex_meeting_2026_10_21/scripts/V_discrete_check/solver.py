"""Independent finite auction/trade computation. No assertions or test runner.

Use compute.py for the consumer CLI. All quantities use the price information set.
The search uses the full strategy simplex before the strict-dominance reduction.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product, permutations
import math
import numpy as np
from scipy.optimize import root, brentq

TOL = 2e-9
MENUS = {"M1": (0, 1), "M2": (-1, 0), "M3": (-1, 0, 1)}


@dataclass(frozen=True)
class Params:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    rho: float = 0.25
    c_L: float = 1.0
    c_H: float = 6.0
    r: float = 3.0
    lam: float = 1.0
    noise: tuple[float, float, float] = (1/3, 1/3, 1/3)


def auction(p: Params) -> tuple[float, float, float, float, float]:
    # Integrate the piecewise auction receipts, independently of trading code.
    t0 = p.p * (p.r - p.p) / p.r
    th = (p.p**2 + (p.r**2-p.p**2)/2) / p.r
    tl = (p.p**2 + (p.ell**2-p.p**2)/2 + p.ell*(p.r-p.ell)) / p.r
    gh = p.h - th
    gl = (p.ell-p.p)*p.p/p.r + (p.ell-p.p)**2/(2*p.r)
    return t0, th, tl, gh, gl


def entry(p: Params, mu: np.ndarray | float) -> np.ndarray:
    _, _, _, gh, gl = auction(p)
    b = gl + np.asarray(mu)*(gh-gl)
    # Entry at equality. This is an absolute rounding convention, not a cost band.
    return p.rho*(b >= p.c_L-2e-13) + (1-p.rho)*(b >= p.c_H-2e-13)


@lru_cache(None)
def partitions(n: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    if n == 0:
        return ((),)
    answer = []
    for old in partitions(n-1):
        answer.append(old+((n-1,),))
        for i in range(len(old)):
            answer.append(old[:i]+(old[i]+(n-1,),)+old[i+1:])
    return tuple(answer)


class Game:
    def __init__(self, p: Params, menu: str):
        self.p, self.menu = p, menu
        self.actions = np.array(MENUS[menu])
        self.flows = np.arange(min(self.actions)-1, max(self.actions)+2)
        self.qnoise = np.array([[p.noise[int(x-q+1)] if -1 <= x-q <= 1 else 0.
                                for x in self.flows] for q in self.actions])
        self.zero = self.qnoise[list(self.actions).index(0)]
        self.buy = self.qnoise[list(self.actions).index(1)] if 1 in self.actions else self.zero
        self.sell = self.qnoise[list(self.actions).index(-1)] if -1 in self.actions else self.zero
        # f_H(x)=H[x] dot (1,a,b); f_L(x)=L[x] dot (1,a,b).
        self.H = np.column_stack((self.zero, p.lam*(self.buy-self.zero), np.zeros(len(self.flows))))
        self.L = np.column_stack((self.zero, np.zeros(len(self.flows)), p.lam*(self.sell-self.zero)))
        self.t0, self.th, self.tl, self.gh, self.gl = auction(p)
        self.delta = self.th-self.tl
        self.cache = {}

    def profile(self, a: float, b: float) -> np.ndarray:
        out = np.zeros((2, len(self.actions)))
        iz = list(self.actions).index(0)
        out[:, iz] = 1
        if 1 in self.actions:
            out[0, list(self.actions).index(1)] = a
            out[0, iz] = 1-a
        if -1 in self.actions:
            out[1, list(self.actions).index(-1)] = b
            out[1, iz] = 1-b
        return out

    def likelihood(self, strategy: np.ndarray) -> np.ndarray:
        return (1-self.p.lam)*self.zero + self.p.lam*(strategy@self.qnoise)

    def point(self, a: float, b: float, belief: str = "directional"):
        v = np.array([1., a, b])
        f = np.array([self.H@v, self.L@v])
        d = f.sum(axis=0)
        mu = np.divide(f[0], d, out=np.zeros_like(d), where=d > 1e-12)
        off = d <= 1e-12
        if belief == "all_L":
            mu[off] = 0.
        elif belief == "all_H":
            mu[off] = 1.
        elif belief == "max_deviation":
            # The optimistic/pessimistic state beliefs do not bound incentives.
            candidates = [0., 1.]
            for cost in (self.p.c_L, self.p.c_H):
                candidates.append(float(np.clip((cost-self.gl)/(self.gh-self.gl), 0, 1)))
            best = max(candidates, key=lambda u: float(entry(self.p, u))*(1-u))
            mu[off] = [best if x > 0 else 1. for x in self.flows[off]]
        elif belief == "prior":
            mu[off] = .5
        else:
            mu[off] = (self.flows[off] > 0).astype(float)
        return f, mu, off

    def full_partitions(self, a: float, b: float, belief: str = "directional") -> list[dict]:
        """Enumerate all Bell partitions, including unused flows and price aliases."""
        cache_key=(round(a,12),round(b,12),belief)
        if cache_key in self.cache:
            return self.cache[cache_key]
        f, mu, off = self.point(a, b, belief)
        d = f.sum(axis=0)
        answer = []
        for part in partitions(len(self.flows)):
            rates = np.zeros(len(mu))
            prices = np.zeros(len(mu))
            beliefs, block_prices = [], []
            possible = True
            for block in part:
                ix = np.array(block)
                mass = d[ix].sum()
                if mass > 1e-12:
                    nu = f[0, ix].sum()/mass
                    e = float(entry(self.p, nu))
                elif np.ptp(mu[ix]) < 1e-11:
                    nu = float(mu[ix[0]])
                    e = float(entry(self.p, nu))
                else:
                    # An unused price has a free posterior over its unused flows.
                    # Positive entry cannot pool distinct flow beliefs. Zero entry can.
                    low, high = float(mu[ix].min()), float(mu[ix].max())
                    ceiling = (self.p.c_L-self.gl)/(self.gh-self.gl)
                    if ceiling <= low + 1e-13:
                        possible = False
                        break
                    nu = (low + min(high, ceiling))/2
                    e = 0.
                px = self.t0 + e*(self.tl-self.t0+self.delta*mu[ix])
                if np.ptp(px) > 2e-10:
                    possible = False
                    break
                rates[ix], prices[ix] = e, px
                beliefs.append(float(nu))
                block_prices.append(float(px[0]))
            if not possible:
                continue
            if any(abs(x-y) < 2e-10 for i,x in enumerate(block_prices) for y in block_prices[i+1:]):
                continue  # These are one price and must be in the same block.
            # Compute deviations from terminal receipts minus actual prices.
            terminal = self.t0 + rates[None, :]*(np.array([self.th,self.tl])[:,None]-self.t0)
            gross = (terminal-prices[None,:])@self.qnoise.T * self.actions[None,:]
            e0 = entry(self.p, mu)
            self_pool = bool(np.any((~off)&(rates==0)&(e0>0)))
            answer.append({"partition": [[int(self.flows[i]) for i in z] for z in part],
                           "price_beliefs": beliefs, "mu": mu.tolist(), "price": prices.tolist(),
                           "entry_rates": rates.tolist(), "gross": gross.tolist(),
                           "E": float(.5*np.dot(d,rates)), "O_H": float(.5*np.dot(f[0],rates)),
                           "self_pool": self_pool, "off": self.flows[off].tolist()})
        self.cache[cache_key]=answer
        return answer

    def rates_feasible(self, a: float, b: float, rates: np.ndarray) -> bool:
        f,mu,off=self.point(a,b)
        zero=rates==0
        if np.any(abs(rates[~zero]-entry(self.p,mu[~zero]))>1e-12):
            return False
        if zero.any():
            mass=f[:,zero].sum()
            nu=f[0,zero].sum()/mass if mass>1e-12 else mu[zero].min()
            if float(entry(self.p,nu))>0:
                return False
        return True

    def optimal(self, a: float, b: float, k: float, schedule: dict) -> tuple[bool, bool, float]:
        strat = self.profile(a,b)
        u = np.asarray(schedule["gross"])-k*np.abs(self.actions)[None,:]
        best = u.max(axis=1)
        regret = float(np.max(np.where(strat>1e-8,best[:,None]-u,0)))
        conventional = regret <= TOL and np.all((strat>=-TOL)&(strat<=1+TOL))
        iz = list(self.actions).index(0)
        strict = conventional and all(not(np.any(strat[j,np.abs(self.actions)>0]>1e-8)
                                           and abs(best[j]-u[j,iz])<=TOL) for j in (0,1))
        return bool(conventional), bool(strict), regret

    def gross_at(self, a, b, rates: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        a,b = np.broadcast_arrays(a,b)
        v = np.stack((np.ones_like(a),a,b),axis=-1)
        fh,fl = v@self.H.T, v@self.L.T
        den = fh+fl
        mu = np.divide(fh,den,out=np.zeros_like(fh),where=den>1e-14)
        off = den <= 1e-14
        mu = np.where(off, (self.flows>0).astype(float), mu)
        return (self.delta*np.sum(self.buy*rates*(1-mu),axis=-1),
                self.delta*np.sum(self.sell*rates*mu,axis=-1))


def clip_polygon(poly: np.ndarray, line: np.ndarray) -> np.ndarray:
    if len(poly)==0:
        return poly
    out = []
    for i,p in enumerate(poly):
        q = poly[(i+1)%len(poly)]
        fp,fq = line[0]+line[1:]@p, line[0]+line[1:]@q
        if fp >= -1e-12:
            out.append(p)
        if (fp>1e-12 and fq < -1e-12) or (fp < -1e-12 and fq > 1e-12):
            out.append(p+(q-p)*fp/(fp-fq))
    return np.asarray(out).reshape(-1,2)


def regions(game: Game) -> list[tuple[np.ndarray, np.ndarray]]:
    """Enumerate all entry vectors and all feasible zero-price pools.

    Region borders are affine inequalities after Bayes denominators cancel.
    Each returned polygon closes strict borders; full_partitions enforces ties.
    """
    g,p = game,game.p
    n = len(g.flows)
    result=[]
    for code in product((0.,p.rho,1.),repeat=n):
        e=np.array(code)
        zero=e==0
        constraints=[]
        if zero.any():
            # No entry at the price iff the pooled gross profit is below c_L.
            constraints.append(-((g.gh-p.c_L)*g.H[zero]+(g.gl-p.c_L)*g.L[zero]).sum(axis=0))
        for i in np.flatnonzero(~zero):
            c=p.c_L if e[i]==p.rho else p.c_H
            constraints.append((g.gh-c)*g.H[i]+(g.gl-c)*g.L[i])
            if e[i]==p.rho:
                constraints.append(-((g.gh-p.c_H)*g.H[i]+(g.gl-p.c_H)*g.L[i]))
        poly=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
        for line in constraints:
            poly=clip_polygon(poly,line)
            if len(poly)==0:
                break
        if len(poly)==0:
            continue
        if g.menu=="M1":
            poly=clip_polygon(poly,np.array([0.,0.,-1.]))
        elif g.menu=="M2":
            poly=clip_polygon(poly,np.array([0.,-1.,0.]))
        if len(poly)==0:
            continue
        # Discard impossible entry vectors on every relative-interior point.
        center=np.mean(poly,axis=0)
        valid=g.rates_feasible(float(center[0]),float(center[1]),e)
        if valid:
            result.append((e,poly))
    return result


def quadratic_roots(fn) -> tuple[list[float], bool]:
    # Fit a quadratic exactly from three evaluations of a cleared equation.
    y0,yh,y1=fn(0.),fn(.5),fn(1.)
    c2=2*(y1+y0-2*yh)
    c1=y1-y0-c2
    c=np.array([c2,c1,y0])
    scale=max(1.,float(np.max(np.abs(c))))
    nz=np.flatnonzero(np.abs(c)>2e-12*scale)
    if len(nz)==0:
        return [],True
    roots=np.roots(c[nz[0]:])
    return [float(x.real) for x in roots if abs(x.imag)<1e-8 and -1e-8<=x.real<=1+1e-8],False


def cleared_equations(g: Game, rates: np.ndarray, k: float, a: float, b: float) -> np.ndarray:
    v=np.array([1.,a,b]); h=g.H@v; l=g.L@v; d=h+l
    # Only the two overlapping flows affect each correctly directed trade.
    hs=[i for i,x in enumerate(g.flows) if x in (0,1)]
    ls=[i for i,x in enumerate(g.flows) if x in (-1,0)]
    def equation(ix,weights,num):
        i,j=ix
        return k*d[i]*d[j]-g.delta*(weights[i]*rates[i]*num[i]*d[j]+weights[j]*rates[j]*num[j]*d[i])
    return np.array([equation(hs,g.buy,l),equation(ls,g.sell,h)])


def equilibrium_candidates(g: Game, ks: np.ndarray, mesh: int = 40) -> tuple[dict[float,list],list[dict],dict]:
    """Fine simplex face grid, exact quadratic edge roots, local interior roots.

    Every entry regime comes from an exhaustive finite enumeration. All roots
    receive a fresh exhaustive price-partition and every-menu-action calculation.
    """
    candidates={float(k): [(0.,0.)] for k in ks}
    pure=[(0.,0.)]
    if g.menu!="M2": pure.append((1.,0.))
    if g.menu!="M1": pure.append((0.,1.))
    if g.menu=="M3": pure.append((1.,1.))
    for k in ks: candidates[float(k)]=pure.copy()
    continuum=[]
    regs=regions(g)
    points=np.linspace(0,1,mesh+1)
    aa,bb=np.meshgrid(points,points,indexing="ij")
    root_calls=0
    def retain(k,a,b,e):
        if not g.rates_feasible(a,b,e):
            return
        uh,ul=g.gross_at(a,b,e)
        if g.menu!="M2" and ((a<1-1e-8 and float(uh)>k+TOL) or (a>1e-8 and float(uh)<k-TOL)):
            return
        if g.menu!="M1" and ((b<1-1e-8 and float(ul)>k+TOL) or (b>1e-8 and float(ul)<k-TOL)):
            return
        candidates[k].append((a,b))
    for e,poly in regs:
        center=poly.mean(axis=0)
        gh,gl=g.gross_at(aa,bb,e)
        if g.menu=="M3":
            hmin=np.minimum.reduce([gh[:-1,:-1],gh[1:,:-1],gh[:-1,1:],gh[1:,1:]])
            hmax=np.maximum.reduce([gh[:-1,:-1],gh[1:,:-1],gh[:-1,1:],gh[1:,1:]])
            lmin=np.minimum.reduce([gl[:-1,:-1],gl[1:,:-1],gl[:-1,1:],gl[1:,1:]])
            lmax=np.maximum.reduce([gl[:-1,:-1],gl[1:,:-1],gl[:-1,1:],gl[1:,1:]])
        for kv in ks:
            k=float(kv)
            # Search every edge support, plus every pure support above.
            for variable in (0,1):
                if (g.menu=="M1" and variable==1) or (g.menu=="M2" and variable==0):
                    continue
                for other in ((0.,1.) if g.menu=="M3" else (0.,)):
                    def eq(t):
                        a,b=(t,other) if variable==0 else (other,t)
                        return cleared_equations(g,e,k,a,b)[variable]
                    roots,flat=quadratic_roots(eq)
                    for t in roots:
                        a,b=(float(np.clip(t,0,1)),other) if variable==0 else (other,float(np.clip(t,0,1)))
                        retain(k,a,b,e)
                    if flat:
                        samples=[]
                        for t in np.linspace(0,1,201):
                            a,b=(t,other) if variable==0 else (other,t)
                            for s in g.full_partitions(float(a),float(b)):
                                if np.allclose(s["entry_rates"],e,atol=1e-12,rtol=0) and g.optimal(a,b,k,s)[0]:
                                    samples.append([float(a),float(b),s["E"],s["O_H"]])
                                    break
                        if samples:
                            continuum.append({"k":k,"variable":variable,"other":other,
                                              "entry_rates":e.tolist(),"samples":samples,
                                              "interpretation":"feasible subset of an indifference edge; samples are not a continuum certificate"})
                            candidates[k].extend((x[0],x[1]) for x in samples)
            if g.menu!="M3":
                continue
            cells=np.argwhere((hmin<=k+1e-11)&(hmax>=k-1e-11)&(lmin<=k+1e-11)&(lmax>=k-1e-11))
            seeds=[((float(i)+.5)/mesh,(float(j)+.5)/mesh) for i,j in cells]
            # Add polygon seeds when a region is narrower than the mesh.
            ph,pl=g.gross_at(poly[:,0],poly[:,1],e)
            if ph.min()-TOL<=k<=ph.max()+TOL and pl.min()-TOL<=k<=pl.max()+TOL:
                seeds.extend([tuple(center)]+[tuple(.9*x+.1*center) for x in poly])
            # Avoid many redundant seeds along an exact indifference curve.
            if len(seeds)>50:
                seeds=seeds[::max(1,len(seeds)//40)]
            found=[]
            for seed in seeds:
                if any(np.linalg.norm(np.asarray(seed)-x)<.02 for x in found):
                    continue
                sol=root(lambda v: cleared_equations(g,e,k,float(v[0]),float(v[1])),seed,tol=1e-11)
                root_calls+=1
                a,b=sol.x
                if not(-1e-8<=a<=1+1e-8 and -1e-8<=b<=1+1e-8):
                    continue
                a,b=float(np.clip(a,0,1)),float(np.clip(b,0,1))
                uh,ul=g.gross_at(a,b,e)
                if max(abs(float(uh)-k),abs(float(ul)-k))>TOL:
                    continue
                if any(np.linalg.norm(np.array([a,b])-x)<1e-7 for x in found):
                    continue
                found.append(np.array([a,b]))
                retain(k,a,b,e)
    # Roots from a fixed entry regime must satisfy the actual price fixed point.
    accepted={}
    for k,pairs in candidates.items():
        seen=set(); rows=[]
        for a,b in pairs:
            key=(round(a,8),round(b,8))
            if key in seen: continue
            seen.add(key)
            for s in g.full_partitions(a,b):
                ok,strict,regret=g.optimal(a,b,k,s)
                if ok:
                    rows.append({"a":a,"b":b,"strict":strict,"regret":regret,**s})
        accepted[k]=rows
    return accepted,continuum,{"regions":len(regs),"local_root_calls":root_calls,"mesh":mesh}


def full_simplex_audit(p: Params, menu: str, n: int=40) -> dict:
    """Enumerate both full simplices; compute posteriors before dominance pruning."""
    g=Game(p,menu)
    if len(g.actions)==2:
        simplex=np.array([[i/n,1-i/n] for i in range(n+1)])
    else:
        simplex=np.array([[i/n,j/n,(n-i-j)/n] for i in range(n+1) for j in range(n-i+1)])
    fh=(1-p.lam)*g.zero+p.lam*simplex@g.qnoise
    surviving=0; partial=0; count=0
    for i in range(len(simplex)):
        h=np.broadcast_to(fh[i],fh.shape); l=fh
        d=h+l; mu=np.divide(h,d,out=np.zeros_like(d),where=d>0)
        partial+=int(np.count_nonzero(np.any((mu>1e-12)&(mu<1-1e-12)&(abs(mu-.5)>1e-12),axis=1)))
        keep=np.ones(len(simplex),dtype=bool)
        if -1 in g.actions:
            keep &= simplex[i,list(g.actions).index(-1)]==0
        if 1 in g.actions:
            keep &= simplex[:,list(g.actions).index(1)]==0
        surviving+=int(keep.sum()); count+=len(simplex)
    return {"menu":menu,"lambda":p.lam,"noise":p.noise,"mesh_denominator":n,
            "strategies_per_type":len(simplex),"profile_pairs":count,
            "survive_strict_dominance":surviving,"profiles_with_partial_belief":partial,
            "partitions_per_full_support_profile":len(partitions(len(g.flows))),
            "dominance":"wrong-direction payoff <= -k under every rational price and every belief; analytical pruning"}
