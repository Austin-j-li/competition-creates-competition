"""Independent Reading N calculations. Print results only; no assertions.

Run from the repository root with .venv/bin/python and a command below.
All inputs are declared here. No project numerical module is imported.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import platform

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.special import expit, logit
from scipy.optimize import brentq


@dataclass(frozen=True)
class Parameters:
    name: str
    a_l: float
    z_l: float
    a_h: float
    z_h: float
    p: float = 0.5
    pi: float = 0.5
    rho: float = 0.25
    c_l: float = 1.0
    c_h: float = 6.0
    b: float = 2.0
    k: float = 0.02
    ell: float = 1.0
    h: float = 10.0


FAMILIES = (
    Parameters("narrow05", 0.95, 1.05, 9.95, 10.05),
    Parameters("narrow50", 0.5, 1.5, 9.5, 10.5),
    Parameters("narrow100", 0.0, 2.0, 9.0, 11.0),
    Parameters("wide20", 0.2, 4.0, 1.0, 19.0),
    Parameters("wide40", 0.4, 4.0, 1.0, 19.0),
    Parameters("wide50", 0.5, 4.0, 1.0, 19.0),
)
PRIORS = (0.2, 0.35, 0.5, 0.65, 0.8)


def grid(p: Parameters, n: int = 9001) -> np.ndarray:
    return np.linspace(max(p.p, p.ell) + 1e-6, p.h, n)


def class_objects(p: Parameters, r: np.ndarray | float, a: float, z: float) -> tuple:
    """Uniform class means: target cash, challenger gross profit, win chance."""
    r = np.asarray(r, dtype=float)
    width = z - a
    t0 = p.p * np.maximum(1 - p.p / r, 0)
    # On the middle segment E(theta^2)=midpoint^2+length^2/12.
    lo = max(a, p.p)
    hi = np.maximum(lo, np.minimum(z, r))
    length = hi - lo
    mean = (hi + lo) / 2
    second = mean * mean + length * length / 12
    t_mid = length * (mean - (second - p.p**2) / (2 * r))
    g_mid = length * (second - p.p**2) / (2 * r)
    w_mid = length * mean / r
    tail_lo = np.maximum(a, np.maximum(p.p, r))
    tail_len = np.maximum(z - tail_lo, 0)
    tail_mean = (z + tail_lo) / 2
    cap = r / 2 + p.p**2 / (2 * r)
    below = max(min(z, p.p) - a, 0)
    t = (below * t0 + t_mid + tail_len * cap) / width
    g = (g_mid + tail_len * (tail_mean - cap)) / width
    w = (w_mid + tail_len) / width
    # If the reserve exceeds all incumbent values, the challenger is alone.
    admissible = max(z - max(a, p.p), 0)
    t = np.where(r <= p.p, p.p * admissible / width, t)
    g = np.where(r <= p.p, admissible * ((z + max(a, p.p)) / 2 - p.p) / width, g)
    w = np.where(r <= p.p, admissible / width, w)
    return t, g, w


def auction(p: Parameters, r: np.ndarray | float) -> dict:
    tl, gl, wl = class_objects(p, r, p.a_l, p.z_l)
    th, gh, wh = class_objects(p, r, p.a_h, p.z_h)
    return dict(t0=p.p * np.maximum(1 - p.p / np.asarray(r), 0),
                tl=tl, th=th, gl=gl, gh=gh, wl=wl, wh=wh, delta=th-tl, gap=gh-gl)


def bounds(p: Parameters) -> tuple[float, float, float]:
    m = float(expit(logit(p.pi) - 2 / p.b))
    M = float(expit(logit(p.pi) + 2 / p.b))
    return m, M, min(m, 1-M)


def profit(o: dict, mu: np.ndarray | float) -> np.ndarray:
    return o['gl'] + mu * o['gap']


def entry(p: Parameters, o: dict, mu: np.ndarray | float) -> np.ndarray:
    B = profit(o, mu)
    return p.rho * (B >= p.c_l) + (1-p.rho) * (B >= p.c_h)


def posterior(p: Parameters, x: np.ndarray | float) -> np.ndarray:
    x = np.asarray(x)
    return expit(logit(p.pi) + (np.abs(x+1)-np.abs(x-1))/p.b)


def laplace_sf(p: Parameters, z: float) -> float:
    return 0.5 * np.exp(-z/p.b) if z >= 0 else 1 - 0.5 * np.exp(z/p.b)


def entry_tail(p: Parameters, o: dict, cost: float) -> tuple[float, float, float]:
    m, M, _ = bounds(p)
    if cost <= profit(o, m):
        return 1.0, 1.0, -np.inf
    if cost > profit(o, M):
        return 0.0, 0.0, np.inf
    tau = float((cost-o['gl'])/o['gap'])
    x = float(p.b/2*(logit(tau)-logit(p.pi)))
    return laplace_sf(p, x-1), laplace_sf(p, x+1), x


def outcomes(p: Parameters, r: float, full: bool) -> dict:
    o = auction(p, r)
    if full:
        low_h, low_l, _ = entry_tail(p, o, p.c_l)
        high_h, high_l, xstar = entry_tail(p, o, p.c_h)
        eh = p.rho*low_h+(1-p.rho)*high_h
        el = p.rho*low_l+(1-p.rho)*high_l
    else:
        eh = el = float(entry(p, o, p.pi))
        high_h = high_l = float(profit(o, p.pi) >= p.c_h)
        xstar = np.nan
    E = p.pi*eh+(1-p.pi)*el
    OH = p.pi*eh*o['wh']
    OL = (1-p.pi)*el*o['wl']
    adm_h = max(p.z_h-max(p.a_h, p.p), 0)/(p.z_h-p.a_h)
    adm_l = max(p.z_l-max(p.a_l, p.p), 0)/(p.z_l-p.a_l)
    admissible = p.pi*eh*adm_h+(1-p.pi)*el*adm_l
    return dict(E=float(E), OH=float(OH), OL=float(OL), eh=float(eh), el=float(el),
                high_cost=float(p.pi*high_h+(1-p.pi)*high_l),
                two_admissible=float(max(1-p.p/r, 0)*admissible),
                target=float(o['t0']+p.pi*eh*(o['th']-o['t0'])+(1-p.pi)*el*(o['tl']-o['t0'])),
                xstar=float(xstar))


def intervals(r: np.ndarray, mask: np.ndarray) -> str:
    ind = np.flatnonzero(mask)
    if not len(ind):
        return "none"
    pieces = np.split(ind, np.flatnonzero(np.diff(ind) > 1)+1)
    return ";".join(f"{r[v[0]]:.6f}:{r[v[-1]]:.6f}" for v in pieces)


def scan() -> None:
    print("GRID: 9001 points, r in [1.000001,10], spacing about .001; fixed costs cL=1,cH=6,k=.02")
    print("UNIQUE_N: Delta<k; UNIQUE_F: floor and global bound>0; no claim outside these sufficient regions")
    print("family,pi,Delta_min,Delta_max,min_step_Delta,gap_min,gap_max,max_step_B,floor,unique_N,no_trade_EQ,unique_F,high_cost_full,unique_F_and_high_cost")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p = replace(p0, pi=pi)
            r = grid(p)
            o = auction(p, r)
            m, M, d = bounds(p)
            bm, bp, bM = [profit(o, u) for u in (m, pi, M)]
            floor = bm > p.c_l
            full = floor & ((1-1/p.b)*p.rho*d*o['delta'] > p.k)
            nt = entry(p, o, pi)*o['delta']*max(pi, 1-pi) <= p.k
            hc = bM >= p.c_h
            print(f"{p.name},{pi:.2f},{o['delta'].min():.9f},{o['delta'].max():.9f},"
                  f"{np.diff(o['delta']).min():.3e},{o['gap'].min():.6f},{o['gap'].max():.6f},"
                  f"{max(np.diff(v).max() for v in (bm,bp,bM)):.3e},"
                  + ",".join(intervals(r, v) for v in (floor,o['delta']<p.k,nt,full,hc,full&hc)))
    print("ANCHORS: family,pi,r,Delta,B_m,B_prior,B_M,global_margin,price_m,price_prior,price_M,E_no,OH_no,E_full,OH_full,high_cost_full,floor")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p = replace(p0, pi=pi)
            m, M, d = bounds(p)
            for r in (1.2,3.0,3.6,10.0):
                o = auction(p, r)
                bb = [float(profit(o,u)) for u in (m,pi,M)]
                pp = [float(o['t0']+entry(p,o,u)*(o['tl']-o['t0']+o['delta']*u)) for u in (m,pi,M)]
                nt, ff = outcomes(p,r,False), outcomes(p,r,True)
                values = [r,o['delta'],*bb,(1-1/p.b)*p.rho*d*o['delta']-p.k,*pp,
                          nt['E'],nt['OH'],ff['E'],ff['OH'],ff['high_cost']]
                print(f"{p.name},{pi:.2f},"+",".join(f"{v:.9f}" for v in values)+f",{bb[0]>p.c_l}")


def find_pair(p: Parameters) -> dict | None:
    """Search strict sufficient windows. Main families have increasing Delta."""
    r = grid(p)
    o = auction(p, r)
    m, M, d = bounds(p)
    low = profit(o,p.pi)
    high = profit(o,M)
    floor = profit(o,m)>p.c_l
    upper = (1-1/p.b)*p.rho*d*o['delta']
    # Necessary r0 indices: cost comparison gives a lower index; trade gives an upper.
    left = np.searchsorted(-low, -high, side='right')
    right = np.minimum(np.searchsorted(o['delta'], upper, side='left')-1, np.arange(len(r))-1)
    best = None
    for j in np.flatnonzero(floor & (left<=right)):
        i = int((left[j]+right[j])//2)
        if i < 0 or i >= j:
            continue
        ch_lo = max(float(low[i]),p.c_l)
        ch_hi = float(high[j])
        k_lo = float(o['delta'][i])
        k_hi = float(upper[j])
        if ch_hi <= ch_lo or k_hi <= k_lo:
            continue
        pp = replace(p,c_h=(ch_lo+ch_hi)/2,k=(k_lo+k_hi)/2)
        no, full = outcomes(pp,float(r[i]),False),outcomes(pp,float(r[j]),True)
        score = ((ch_hi-ch_lo)/max(ch_hi,1))*((k_hi-k_lo)/max(k_hi,1e-10))
        result = dict(r0=float(r[i]),r1=float(r[j]),ch_lo=ch_lo,ch_hi=ch_hi,
                      k_lo=k_lo,k_hi=k_hi,c_h=pp.c_h,k=pp.k,
                      floor_margin=float(profit(auction(p,r[j]),m)-p.c_l),
                      E0=no['E'],E1=full['E'],OH0=no['OH'],OH1=full['OH'],score=score)
        if best is None or score>best['score']:
            best=result
    return best


def pairs() -> None:
    print("PAIR SEARCH: fixed p=.5,rho=.25,cL=1,b=2; choose cH,k strictly inside windows; 9001-point grid")
    print("family,pi,r0,r1,cH_lo,cH_hi,k_lo,k_hi,cH,k,floor_margin,E0,E1,OH0,OH1")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p=replace(p0,pi=pi)
            ans=find_pair(p)
            if ans is None:
                o=auction(p,grid(p))
                m,M,d=bounds(p)
                # Upper envelope with r0 at the smallest spread, irrespective of A2.
                print(f"{p.name},{pi:.2f},NONE;Dmin={min(o['delta']):.9f};global_max={(1-1/p.b)*p.rho*d*max(o['delta']):.9f}")
            else:
                keys=('r0','r1','ch_lo','ch_hi','k_lo','k_hi','c_h','k','floor_margin','E0','E1','OH0','OH1')
                print(f"{p.name},{pi:.2f},"+",".join(f"{ans[z]:.9f}" for z in keys))
    print("FAILED-WINDOW DIAGNOSTIC: best cost-window gap among A1/A3-feasible pairs")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p=replace(p0,pi=pi)
            if find_pair(p) is not None:
                continue
            r=grid(p); o=auction(p,r); m,M,d=bounds(p)
            up=(1-1/p.b)*p.rho*d*o['delta']
            right=np.minimum(np.searchsorted(o['delta'],up,side='left')-1,np.arange(len(r))-1)
            ok=(right>=0)&(profit(o,m)>p.c_l)
            if not np.any(ok):
                max_allowed=float(np.max(up[profit(o,m)>p.c_l])) if np.any(profit(o,m)>p.c_l) else np.nan
                print(f"{p.name},{pi:.2f},NO_A1_A3;max_k_upper_with_floor={max_allowed:.9f};min_k_lower={o['delta'][0]:.9f}")
            else:
                jj=np.flatnonzero(ok)
                gaps=profit(o,M)[jj]-profit(o,pi)[right[jj]]
                j=jj[int(np.argmax(gaps))]; i=right[j]
                print(f"{p.name},{pi:.2f},A2_gap_max={max(gaps):.9f};r0={r[i]:.6f};r1={r[j]:.6f}")


def realized(p: Parameters, R: float, theta: float) -> tuple[float,float,float]:
    if max(R,theta)<p.p:
        return 0.0,0.0,0.0
    if theta<R:
        return max(p.p,theta),0.0,0.0
    payment=max(p.p,R)
    return payment,theta-payment,1.0


def direct(p: Parameters, r: float, a: float, z: float) -> tuple[float,float,float]:
    """Nested quadrature over actual bids, split at reserve and bid ties."""
    points=sorted(set([a,z]+[v for v in (p.p,r) if a<v<z]))
    result=[]
    for component in range(3):
        def theta_integrand(theta: float) -> float:
            inner=sorted(set([0.0,r]+[v for v in (p.p,theta) if 0<v<r]))
            return sum(quad(lambda R:realized(p,R,theta)[component],u,v,
                            epsabs=2e-12,epsrel=2e-12)[0] for u,v in zip(inner[:-1],inner[1:]))/r
        result.append(sum(quad(theta_integrand,u,v,epsabs=2e-12,epsrel=2e-12)[0]
                          for u,v in zip(points[:-1],points[1:]))/(z-a))
    return tuple(result)


def quadrature() -> None:
    rng=np.random.default_rng(20261021)
    cases=[]
    for p in FAMILIES:
        for r in (0.3,0.5,0.8,1.000001,1.2,3,3.6,9.5,10,12,20):
            cases.append((p,r))
    for i in range(100):
        aa=rng.uniform(-0.5,3,2); ww=rng.uniform(.01,20,2)
        p=Parameters(f"random{i}",aa[0],aa[0]+ww[0],aa[1],aa[1]+ww[1],p=float(rng.uniform(.1,2)))
        cases.append((p,float(rng.uniform(.15,20))))
    errors={key:0.0 for key in ('t0','tL','tH','gL','gH','wL','wH','Delta','B')}
    worst={}
    for p,r in cases:
        o=auction(p,r)
        dl=direct(p,r,p.a_l,p.z_l); dh=direct(p,r,p.a_h,p.z_h)
        t0=quad(lambda R:p.p*float(R>=p.p),0,r,points=[p.p] if p.p<r else [],epsabs=2e-12)[0]/r
        comparisons=dict(t0=(float(o['t0']),t0),tL=(float(o['tl']),dl[0]),tH=(float(o['th']),dh[0]),
                         gL=(float(o['gl']),dl[1]),gH=(float(o['gh']),dh[1]),wL=(float(o['wl']),dl[2]),
                         wH=(float(o['wh']),dh[2]),Delta=(float(o['delta']),dh[0]-dl[0]))
        for key,(closed,value) in comparisons.items():
            error=abs(closed-value)
            if error>errors[key]:errors[key]=error;worst[key]=(p.name,r)
        for mu in (.01,.2,.5,.8,.99):
            error=abs(float(profit(o,mu))-((1-mu)*dl[1]+mu*dh[1]))
            if error>errors['B']:errors['B']=error;worst['B']=(p.name,r,mu)
    print(f"Direct nested auction integration: {len(cases)} economies, {2*len(cases)} class distributions; deterministic seed=20261021")
    for key in errors:print(f"{key}: maximum absolute discrepancy={errors[key]:.16e}; location={worst.get(key)}")
    print(f"overall_max={max(errors.values()):.16e}")


def cdf(a: float,z: float,u: np.ndarray|float) -> np.ndarray:
    return np.clip((np.asarray(u)-a)/(z-a),0,1)


def spread_derivative(p: Parameters,r:float) -> float:
    D=lambda u:float(cdf(p.a_l,p.z_l,u)-cdf(p.a_h,p.z_h,u))
    pts=sorted(set([p.p,r]+[v for v in (p.a_l,p.z_l,p.a_h,p.z_h) if p.p<v<r]))
    value=sum(quad(lambda u:u*D(u),a,z,epsabs=2e-12)[0] for a,z in zip(pts[:-1],pts[1:]))
    return (value-p.p**2*D(p.p))/r**2


def failures() -> None:
    variants=(replace(FAMILIES[3],name='wide20_reserve09',p=.9),
              Parameters('reserve_straddle',.2,.4,.3,.6),
              Parameters('crossing_cdf',1,3,0,3.8),
              Parameters('reverse_class',9,11,0,2))
    for p in variants:
        r=grid(p);o=auction(p,r)
        dd=np.diff(o['delta']);gg=o['gap']
        print(f"{p.name}: GL=U[{p.a_l},{p.z_l}],GH=U[{p.a_h},{p.z_h}],p={p.p};FOSD={p.a_h>=p.a_l and p.z_h>=p.z_l}")
        print(f"Delta_falls={intervals(r[:-1],dd<-1e-12)};gap_negative={intervals(r,gg<0)};Delta_negative={intervals(r,o['delta']<0)}")
        for rr in (1.000001,1.2,1.5,3,5,10):
            oo=auction(p,rr)
            print(f"r={rr:.6f},Delta={oo['delta']:.9f},derivative={spread_derivative(p,rr):.9f},gap={oo['gap']:.9f}")
        switches=np.flatnonzero(gg[:-1]*gg[1:]<0)
        for i in switches:
            root=brentq(lambda rr:float(auction(p,rr)['gap']),r[i],r[i+1])
            print(f"gap_zero={root:.12f}")
        switches=np.flatnonzero(dd[:-1]*dd[1:]<0)
        for i in switches:
            root=brentq(lambda rr:spread_derivative(p,rr),r[max(i-1,0)],r[min(i+3,len(r)-1)])
            print(f"Delta_turn={root:.12f}")
    print("RESERVE TERM: full Delta, omitted-term expression, missing amount at r=1.2")
    for p in FAMILIES:
        r=1.2;o=auction(p,r)
        missing=p.p**2/r*float(cdf(p.a_l,p.z_l,p.p)-cdf(p.a_h,p.z_h,p.p))
        print(f"{p.name},{o['delta']:.12f},{o['delta']-missing:.12f},{missing:.12f}")


NODES,WEIGHTS=np.polynomial.legendre.leggauss(48)


def deviation(p: Parameters,r:float,state:str,s:float) -> tuple[float,float]:
    o=auction(p,r);q=s if state=='H' else -s
    m,M,_=bounds(p)
    residual=lambda mu:entry(p,o,mu)*o['delta']*((1-mu) if state=='H' else mu)
    left=float(residual(m));right=float(residual(M))
    # All q lie in [-1,1], so each tail has a constant density score.
    left_mass=1-laplace_sf(p,-1-q);right_mass=laplace_sf(p,1-q)
    F=left*left_mass+right*right_mass
    derivative_q=(-left*left_mass+right*right_mass)/p.b
    thresholds=[entry_tail(p,o,c)[2] for c in (p.c_l,p.c_h)]
    points=sorted(set([-1.0,1.0,q]+[x for x in thresholds if -1<x<1]))
    for a,z in zip(points[:-1],points[1:]):
        x=(a+z)/2+(z-a)/2*NODES
        weight=(z-a)/2*WEIGHTS
        v=np.exp(-np.abs(x-q)/p.b)/(2*p.b)*residual(posterior(p,x))
        F+=float(weight@v)
        derivative_q+=float(weight@(v*np.sign(x-q)/p.b))
    Fs=derivative_q if state=='H' else -derivative_q
    return s*(F-p.k), F+s*Fs-p.k


def deviations() -> None:
    print("Full-order candidate: 401 correctly signed order magnitudes; 48-node quadrature per smooth segment; exact tails")
    for p0 in FAMILIES:
        p=replace(p0,pi=.5);ans=find_pair(p)
        if ans is None:
            continue
        p=replace(p,c_h=ans['c_h'],k=ans['k']);r=ans['r1']
        oo=auction(p,r);m,M,d=bounds(p)
        print(f"{p.name},r={r:.9f},global_bound={(1-1/p.b)*p.rho*d*oo['delta']-p.k:.12f}")
        for state in ('H','L'):
            ss=np.linspace(0,1,401);values=np.array([deviation(p,r,state,float(s)) for s in ss])
            print(f"{state}: best_s={ss[np.argmax(values[:,0])]:.6f},U_full={values[-1,0]:.12f},min_marginal={values[:,1].min():.12f},J={values[-1,0]+p.k:.12f}")
    print("General-prior J asymmetry at narrow05,r=3 with fixed benchmark costs")
    for pi in PRIORS:
        p=replace(FAMILIES[0],pi=pi)
        JH=deviation(p,3,'H',1)[0]+p.k
        JL=deviation(p,3,'L',1)[0]+p.k
        print(f"pi={pi},JH={JH:.12f},JL={JL:.12f},JH/JL={JH/JL:.12f},(1-pi)/pi={(1-pi)/pi:.12f}")


def examples() -> None:
    examples=((FAMILIES[0],1.2,3,6,.02),
              (FAMILIES[1],1.05,4,5.5,.032),
              (FAMILIES[3],1.01,5.7,5.45,.0356),
              (FAMILIES[4],1.05,4.8,5.6,.021),
              (FAMILIES[5],1.1,4,5.8,.0125))
    print("Selected simple parameter vectors, pi=.5,p=.5,rho=.25,cL=1,b=2")
    for p0,r0,r1,ch,k in examples:
        p=replace(p0,c_h=ch,k=k);m,M,d=bounds(p)
        o0,o1=auction(p,r0),auction(p,r1)
        oo0,oo1=outcomes(p,r0,False),outcomes(p,r1,True)
        print(f"{p.name},r0={r0},r1={r1},cH={ch},k={k}")
        print(f"A1 margin={profit(o1,m)-p.c_l:.12f},A2=({profit(o0,p.pi):.12f},{profit(o1,M):.12f}),A3=({o0['delta']:.12f},{(1-1/p.b)*p.rho*d*o1['delta']:.12f})")
        print(f"outcomes_no={oo0};outcomes_full={oo1}")
        print(f"wH0={o0['wh']:.12f},wH1={o1['wh']:.12f},Delta1={o1['delta']:.12f}")
        for state in ('H','L'):
            ss=np.linspace(0,1,401);v=np.array([deviation(p,r1,state,float(s)) for s in ss])
            print(f"{state}: best_s={ss[np.argmax(v[:,0])]:.6f},U_full={v[-1,0]:.12f},min_marginal={v[:,1].min():.12f}")
    print("Posterior bounds and global coefficient")
    for pi in PRIORS:
        p=replace(FAMILIES[0],pi=pi);m,M,d=bounds(p)
        print(f"pi={pi},m={m:.12f},M={M:.12f},min_residual_factor={d:.12f},global_coefficient={(1-1/p.b)*p.rho*d:.12f}")


def boundaries() -> None:
    def roots(p:Parameters,fun) -> str:
        lo=max(p.p,p.ell)+1e-6;hi=p.h
        if fun(lo)*fun(hi)>=0:
            return "none"
        return f"{brentq(fun,lo,hi):.9f}"
    print("Continuous boundary roots; strict sufficient inequalities determine endpoint inclusion")
    print("family,pi,floor_boundary,unique_N_boundary,unique_F_bound,high_cost_ceiling,prior_high_cost_boundary")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p=replace(p0,pi=pi);m,M,d=bounds(p)
            funs=(lambda r:float(profit(auction(p,r),m)-p.c_l),
                  lambda r:float(auction(p,r)['delta']-p.k),
                  lambda r:float((1-1/p.b)*p.rho*d*auction(p,r)['delta']-p.k),
                  lambda r:float(profit(auction(p,r),M)-p.c_h),
                  lambda r:float(profit(auction(p,r),pi)-p.c_h))
            print(f"{p.name},{pi},"+",".join(roots(p,f) for f in funs))


def memo_tables() -> None:
    print("R=3: family | pi | B_m / B_prior / B_M | E_full / OH_full | E_no / OH_no")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p=replace(p0,pi=pi);o=auction(p,3);m,M,d=bounds(p)
            ff=outcomes(p,3,True);nn=outcomes(p,3,False)
            bb=" / ".join(f"{profit(o,v):.4f}" for v in (m,pi,M))
            print(f"| {p.name} | {pi:.2f} | {bb} | {ff['E']:.4f} / {ff['OH']:.4f} | {nn['E']:.4f} / {nn['OH']:.4f} |")
    print("REGIONS: family | pi | sharp unique no trade | exact no-trade existence | unique full orders | high-cost ceiling under full orders")
    for p0 in FAMILIES:
        for pi in PRIORS:
            p=replace(p0,pi=pi);r=grid(p);o=auction(p,r);m,M,d=bounds(p)
            sharp=entry(p,o,M)*max(M,1-m)*o['delta'] < p.k
            nn=entry(p,o,pi)*max(pi,1-pi)*o['delta'] <= p.k
            ff=(profit(o,m)>p.c_l)&((1-1/p.b)*p.rho*d*o['delta']>p.k)
            hh=profit(o,M)>=p.c_h
            print(f"| {p.name} | {pi:.2f} | "+" | ".join(intervals(r,v) for v in (sharp,nn,ff,hh))+" |")


def features() -> None:
    p=replace(FAMILIES[0],pi=.65)
    prior_cross=brentq(lambda r:float(profit(auction(p,r),p.pi)-p.c_h),1.1,2)
    nt_high=brentq(lambda r:float(auction(p,r)['delta']*p.pi-p.k),1,2)
    nt_low=brentq(lambda r:float(p.rho*auction(p,r)['delta']*p.pi-p.k),1,2)
    print(f"narrow05,pi=.65:no-trade intervals=(1,{nt_high:.12f}] union ({prior_cross:.12f},{nt_low:.12f}]")
    p=FAMILIES[3]
    for r in (5,10):
        print(f"wide20 fixed benchmark costs at r={r}: {outcomes(p,r,True)}")
    print("Small-support spread at r down to 1")
    for p in FAMILIES:
        oo=auction(p,1)
        print(f"{p.name}:Delta_limit={oo['delta']:.12f},gL={oo['gl']:.12f},gH={oo['gh']:.12f}")


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('quadrature','scan','pairs','failures','deviations','examples','boundaries','memo_tables','features'))
    args=parser.parse_args()
    print(f"Python {platform.python_version()}; numpy {np.__version__}; scipy {scipy.__version__}")
    globals()[args.command]()


if __name__=='__main__':
    main()
