"""Exact finite-history calculations, with print-only output."""
from fractions import Fraction as F
from itertools import product
from math import log, exp

K, RHO = F(1, 50), F(1, 4)

def auction(r):
    p = F(1, 2)
    t0 = p * (r-p)/r
    def integrate(v):
        top = min(v, r)
        t = (p*p + (top*top-p*p)/2 + v*max(r-v, 0))/r
        g = ((v-p)*p + v*(top-p)-(top*top-p*p)/2)/r
        return t, g
    th, gh = integrate(F(10))
    tl, gl = integrate(F(1))
    return t0, th, tl, gh, gl

def show(label, x):
    print(label, x, float(x))

def bisect(fun, lo=F(0), hi=F(1), steps=48):
    flo = fun(lo)
    for _ in range(steps):
        mid = (lo+hi)/2
        fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return lo, hi

def timing(beta, lam, xh, xl, r=F(3), hidden=False, ties=None):
    """One unit; first-date rates x; all surviving units trade at date two."""
    eta = {0:1-beta, 1:beta} if xl is None else {-1: beta, 0: 1-2*beta, 1: beta}
    t0, th, tl, gh, gl = auction(r)
    w = {1: th-t0, -1: tl-t0}
    xs = {1: xh, -1: xl}
    masses, mu, entry, prices = {}, {}, {}, {}
    for a, b in product(eta, repeat=2):
        pair = (a,b)
        masses[pair] = {}
        for j in (1,-1):
            if j == -1 and xl is None:
                f = eta[a]*eta[b]
            else:
                x = xs[j]
                f = ((1-lam)*eta[a]*eta[b]
                     +lam*x*(a == j)*eta[b]
                     +lam*(1-x)*eta[a]*(b == j))
            masses[pair][j] = f
        fh, fl = masses[pair][1], masses[pair][-1]
        mu[pair] = fh/(fh+fl)
        gain = gl+mu[pair]*(gh-gl)-6
        z = F(gain > 0) if gain else (ties or {}).get(pair, F(1))
        entry[pair] = RHO if hidden else RHO+(1-RHO)*z
        prices[pair] = t0+entry[pair]*(w[-1]+mu[pair]*(th-tl))
    p1 = {}
    for a in eta:
        denom = sum(sum(masses[a,b].values()) for b in eta)
        p1[a] = sum(sum(masses[a,b].values())*prices[a,b] for b in eta)/denom
    now, later, last, wrong = {}, {}, {}, {}
    for j in ((1,) if xl is None else (1,-1)):
        now[j] = j*(t0+w[j]*sum(eta[b]*entry[j,b] for b in eta)-p1[j])-K
        last[j] = {a: j*(t0+w[j]*entry[a,j]-prices[a,j])-K for a in eta}
        later[j] = sum(eta[a]*max(F(0),last[j][a]) for a in eta)
        if xl is not None:
            wrong[j] = j*-1*(t0+w[j]*sum(eta[b]*entry[-j,b] for b in eta)-p1[-j])-K
    en = sum(sum(masses[h].values())*entry[h]/2 for h in masses)
    return now, later, last, wrong, en, mu, entry, p1, prices

def fresh(n, beta, lam, r):
    t0, th, tl, gh, gl = auction(r)
    eta = {-1: beta, 0:1-2*beta, 1:beta}
    laws = {j:{q:(1-lam)*eta[q]+lam*(q==j) for q in eta} for j in (1,-1)}
    rows = {}
    for h in product(eta, repeat=n):
        f = {j:F(1) for j in laws}
        for q in h:
            for j in f:
                f[j] *= laws[j][q]
        mu=f[1]/sum(f.values())
        e=RHO+(1-RHO)*(gl+mu*(gh-gl)>=6)
        price=t0+e*(tl-t0+mu*(th-tl))
        rows[h]=(f,mu,e,price)
    prices={}
    for t in range(n+1):
        for h in product(eta,repeat=t):
            below=[row for path,row in rows.items() if path[:t]==h]
            denom=sum(sum(row[0].values()) for row in below)
            prices[h]=sum(sum(row[0].values())*row[3] for row in below)/denom
    en=sum(sum(row[0].values())*row[2]/2 for row in rows.values())
    return rows,prices,en,laws

def main():
    print('AUCTION BY PIECEWISE INTEGRATION')
    for r in (F(6,5),F(31,20),F(8,5),F(33,20),F(3),F(18,5)):
        t0,th,tl,gh,gl=auction(r)
        print(r,'objects',t0,th,tl,gh,gl,'delta',th-tl,'tau',(6-gl)/(gh-gl))
    print('C TWO-SIDED: EXACT DATE INDIFFERENCE')
    gap=lambda x: timing(F(1,3),F(6,17),F(1),x)[0][-1]-timing(F(1,3),F(6,17),F(1),x)[1][-1]
    lo,hi=bisect(gap, F(1,10),F(1,4))
    print('xL bracket',lo,hi, float(lo),float(hi),'endpoint gaps',gap(lo),gap(hi))
    z=timing(F(1,3),F(6,17),F(1),(lo+hi)/2)
    for j in (1,-1):
        show('now '+str(j),z[0][j]); show('later '+str(j),z[1][j]); show('wrong '+str(j),z[3][j])
        print('last-date payoffs',j,[(a,float(v)) for a,v in z[2][j].items()])
    show('entry',z[4]); print('recruit histories',[h for h,e in z[6].items() if e>RHO])
    show('mu(+,-)',z[5][1,-1])
    print('C ADDITIONAL EQUILIBRIUM: H AT SECOND DATE')
    gap=lambda x: timing(F(1,3),F(6,17),F(0),x)[0][-1]-timing(F(1,3),F(6,17),F(0),x)[1][-1]
    lo,hi=bisect(gap,F(4,5),F(9,10))
    print('xL second equilibrium bracket',lo,hi,float(lo),float(hi),'gaps',gap(lo),gap(hi))
    for x in (lo,hi):
        show('polynomial at bracket',198*x*x-3819*x+3060)
    z=timing(F(1,3),F(6,17),F(0),(lo+hi)/2)
    for j in (1,-1):
        show('additional now '+str(j),z[0][j]);show('additional later '+str(j),z[1][j]);show('additional wrong '+str(j),z[3][j])
        print('additional last-date payoffs',j,[(a,float(v)) for a,v in z[2][j].items()])
    show('additional entry',z[4]);print('additional recruit histories',[h for h,e in z[6].items() if e>RHO])
    now_at_lower=timing(F(1,3),F(6,17),F(0),F(4,5))[0][1]
    show('H date gap upper bound on xL in [4/5,9/10]',now_at_lower-(F(2,3)*F(49,300)+F(1,3)*F(31,1200)))
    print('C BUY-ONLY')
    for x in (F(0),F(1),F(467,531)):
        z=timing(F(1,5),F(9,22),x,None)
        print('x',x,'now',float(z[0][1]),'later',float(z[1][1]),'entry',z[4], 'ties',[(h,m) for h,m in z[5].items() if m==F(141,200)])
    x=F(467,531)
    z0=timing(F(1,5),F(9,22),x,None,ties={(1,0):F(0)})
    z1=timing(F(1,5),F(9,22),x,None,ties={(1,0):F(1)})
    g0=z0[0][1]-z0[1][1]; g1=z1[0][1]-z1[1][1]
    tie=-g0/(g1-g0)
    z=timing(F(1,5),F(9,22),x,None,ties={(1,0):tie})
    show('challenger mixture',tie);show('entry threshold date',z[4]);show('date gap',z[0][1]-z[1][1])
    print('C BUY-ONLY COMPLETE CELL SIGNS')
    def cellgap(x,e10,e01):
        beta,lam=F(1,5),F(9,22)
        t0,th,tl,gh,gl=auction(F(3));wh,wl=th-t0,tl-t0
        a,c=1-lam,lam/beta
        top=a+c
        v=wh*(beta+(1-beta)*e10)
        p=(beta*(wh*top+wl)+(1-beta)*e10*(wh*(a+c*x)+wl))/(2+c*(1-beta)*x)
        waiting=(th-tl)*(beta/(1+top)+(1-beta)*e01/(1+a+c*(1-x)))
        return v-p-waiting
    boundaries=(F(0),F(64,531),F(467,531),F(1))
    for i,(e10,e01) in enumerate(((RHO,F(1)),(RHO,RHO),(F(1),RHO))):
        def numerator(x):
            return cellgap(x,e10,e01)*(2+F(18,11)*x)*(1+F(13,22)+F(45,22)*(1-x))
        v0,vm,v1=numerator(F(0)),numerator(F(1,2)),numerator(F(1))
        a=2*(v1+v0-2*vm); b=v1-v0-a; c=v0
        left,right=boundaries[i:i+2]
        values=[numerator(left),numerator(right)]
        if a and left < -b/(2*a) < right:
            values.append(numerator(-b/(2*a)))
        print('cell',i,'bounds',left,right,'quadratic a,b,c',a,b,c,'range extrema',min(values),max(values))
    for cutoff in boundaries[1:3]:
        print('cutoff',cutoff,'gap e10,e01 extremes',[(e10,e01,cellgap(cutoff,e10,e01)) for e10,e01 in ((RHO,F(1)),(RHO,RHO),(F(1),RHO))])
    for two in (False,True):
        b,l=(F(1,3),F(6,17)) if two else (F(1,5),F(9,22))
        f=lambda x: timing(b,l,x,x if two else None,hidden=True)[0][1]-timing(b,l,x,x if two else None,hidden=True)[1][1]
        lo,hi=bisect(f)
        print('hidden date bracket',two,float(lo),float(hi), 'gap endpoints',f(lo),f(hi))
    print('A STRIP AND DECAY')
    l1,l2=log(F(141,59)),log(F(4245,1559)); theta=l1/l2
    print('L1,L2,theta,KL',l1,l2,theta,theta*log(2*theta)+(1-theta)*log(2*(1-theta)))
    for beta in (1/3,1/2):
        y=(theta*(1-2*beta)+(theta**2*(1-2*beta)**2+4*beta**2*(1-theta**2))**0.5)/(2*beta*(1-theta))
        rate=theta*log(y)-log(1-2*beta+beta*(y+1/y))
        print('true limiting imbalance rate at upper strip edge',beta,rate)
    for n in (12,24,48,96,192):
        weights={-1:100*n,0:100*n,1:100*n+93}
        denom=300*n+93
        law={0:1}
        for _ in range(n):
            nxt={}
            for d,mass in law.items():
                for q,v in weights.items():
                    nxt[d+q]=nxt.get(d+q,0)+mass*v
            law=nxt
        dstar=0
        while 59*(100*n+93)**dstar < 141*(100*n)**dstar:
            dstar+=1
        tail=sum(v for d,v in law.items() if d>=dstar)+sum(v for d,v in law.items() if d<=-dstar)
        extra=F(3*tail,8*denom**n)
        print('exact DP n,u,dstar,extra,negative log/n',n,F(93,100*n),dstar,float(extra),-log(extra)/n)
    for n in (1,2,3,4,6,12):
        print('n,u range',n, exp(l1/n)-1,exp(l2/n)-1)
    for n,u in ((2,F(3,5)),(3,F(3,8))):
        lam=u/(3+u)
        show('fresh entry n='+str(n),fresh(n,F(1,3),lam,F(3))[2])
    print('B FULL TWO-SLOT PRICE PATH AND PROFIT')
    rows,prices,en,laws=fresh(2,F(1,3),F(1,6),F(3))
    for h in ((),(1,),(0,),(-1,),(1,1),(-1,-1)):
        show('P '+str(h),prices[h])
    show('entry',en)
    t0,th,tl,gh,gl=auction(F(3)); wh,wl=th-t0,tl-t0
    eh=sum(laws[1][q]*rows[1,q][2] for q in laws[1])
    el=sum(laws[-1][q]*rows[1,q][2] for q in laws[-1])
    base=(th-tl)*eh; term=wl*(eh-el)
    show('D base',base);show('D early term',term);show('fraction',term/(base+term))
    profit1=(1-F(8,13))*(base+term)-K
    profit2=F(0)
    for a in laws[1]:
        mu,e=rows[a,1][1:3]
        profit2+=laws[1][a]*((1-mu)*e*(th-tl)-K)
    show('slot1 H net',profit1);show('slot2 H net',profit2);show('relative net increase',profit1/profit2-1)
    r=F(6,5)
    weakrows,weakprices,weaken,weaklaws=fresh(2,F(1,3),F(1,6),r)
    t0,th,tl,gh,gl=auction(r)
    eh=sum(weaklaws[1][q]*weakrows[1,q][2] for q in weaklaws[1])
    el=sum(weaklaws[-1][q]*weakrows[1,q][2] for q in weaklaws[-1])
    show('r0 first buy net under prescribed full future orders',F(5,13)*((th-t0)*eh-(tl-t0)*el)-K)
    print('B MIDDLE STRENGTH REDUCED SYSTEM')
    beta,lam,b=F(1,3),F(1,6),F(5,18)
    for r in (F(31,20),F(8,5),F(33,20)):
        t0,th,tl,gh,gl=auction(r); d=th-tl; wh,wl=th-t0,tl-t0
        tau=(6-gl)/(gh-gl); T=tau/(1-tau); es=K/(d*(1-tau))
        def threshold_gap(a):
            a2=b*(T*b/(b+a)-1)
            eh=RHO+(es-RHO)*(b+a2)
            el=RHO+(es-RHO)*b
            m=(b+a)/(2*b+a)
            return (1-m)*(wh*eh-wl*el)-K
        amin=max(F(0),b*(T/(1+lam/b)-1)); amax=min(lam,b*(T-1))
        lo,hi=bisect(threshold_gap,amin,amax)
        a=(lo+hi)/2; a2=b*(T*b/(b+a)-1)
        ent=RHO+(es-RHO)*b*b/(2*(1-tau))
        print('r',r,'tau',tau,'T',T,'a1/lambda',float(a/lam),'a2/lambda',float(a2/lam),'challenger mix',float((es-RHO)/(1-RHO)))
        show('TH entry',ent);show('sale bound margin',RHO*d*F(8,13)-K)
        eh=RHO+(1-RHO)*(b+lam);el=RHO+(1-RHO)*b
        show('full continuation first buy margin',F(5,13)*(wh*eh-wl*el)-K)
    print('D EXACT N=2 FACTOR')
    rows,prices,en,laws=fresh(2,F(1,3),F(6,17),F(18,5))
    mass=sum(rows[1,1][0].values())/2
    show('N2 ++ mass',mass);show('mu++',rows[1,1][1]);show('entry conditional N2',en)
    for mean in (0.5,1,2):
        print('Poisson lower bound',mean,0.25+0.75*exp(-mean)*mean**2/2*float(mass))

if __name__ == '__main__':
    main()
