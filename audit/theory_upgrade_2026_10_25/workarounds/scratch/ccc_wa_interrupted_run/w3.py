import math

def brentq(f,lo,hi,xtol=1e-14):
    flo=f(lo)
    for _ in range(200):
        mid=.5*(lo+hi); fm=f(mid)
        if (fm>0)==(flo>0): lo,flo=mid,fm
        else: hi=mid
    return .5*(lo+hi)


def auction(r,cH,h=10.,l=1.,p=.5):
    # point masses h,l; R~U[0,r], l<r<h
    D=(r-l)**2/(2*r)
    gL=(l*l-p*p)/(2*r)
    gam=(r*r-l*l)/(2*r)+h-r
    tau=(cH-gL)/gam
    return D,tau

def m_(lam,beta): return beta*(1-lam)/(2*beta+lam*(1-2*beta))
def M_(lam,beta): return 1-m_(lam,beta)
def lamE(tau,beta): return beta*(2*tau-1)/(beta+(1-2*beta)*(1-tau))

def V(lam,D,rho,k,beta):
    m=m_(lam,beta)
    return .5*max(D*m-k,0)+.5*max(rho*D*m-k,0)

def Lam(D,rho,k,beta,a,cap):
    g=lambda x: a*x-V(x,D,rho,k,beta)
    if g(0)>=0: return 0.0
    if g(cap)<=0: return cap
    return brentq(g,0,cap,xtol=1e-14)

def regime(D,lam,rho,k,beta):
    m=m_(lam,beta)
    if rho*D<=2*k: return 'abstain'
    if rho*D*m<k: return 'mix'
    return 'sell'

def verify(D,tau,lam,rho,k,beta,a,cap):
    # build tuple: H buys, L sale prob s from regime, e(1)=1 iff M>=tau (C1)
    b=(1-lam)*beta; b0=(1-lam)*(1-2*beta)
    reg=regime(D,lam,rho,k,beta)
    if reg=='abstain': s=0.
    elif reg=='sell': s=1.
    else: s=b*(rho*D/k-2)/lam
    fH={1:b+lam,0:b0,-1:b}; fL={1:b,0:b0+lam*(1-s),-1:b+lam*s}
    mu={x:fH[x]/(fH[x]+fL[x]) for x in fH}
    e={x:(1. if mu[x]>=tau else rho) for x in mu}
    UH1=e[1]*D*(1-mu[1])-k; UL1=-e[-1]*D*mu[-1]*(-1)-k  # sale payoff: e D mu - k
    UL1=e[-1]*D*mu[-1]-k
    Vv=.5*max(UH1,0)+.5*max(UL1,0)
    ok_res=abs(min(cap,Vv/a)-lam)<1e-9
    ok_L = (s==0 and UL1<=1e-12) or (s==1 and UL1>=-1e-12) or (0<s<1 and abs(UL1)<1e-9)
    ent=sum(.5*(fH[x]+fL[x])*e[x] for x in fH)
    return dict(s=s,mu=mu,e1=e[1],UH1=UH1,UL1=UL1,ok_res=ok_res,ok_L=ok_L,entry=ent,recruit=mu[1]>=tau)

def scan(name,cH,rho,k,beta,a,cap,rs):
    print('==',name)
    for r in rs:
        D,tau=auction(r,cH)
        L=Lam(D,rho,k,beta,a,cap)
        out=verify(D,tau,L,rho,k,beta,a,cap)
        print(f"r={r:6.3f} D={D:.4f} tau={tau:.4f} Lam={L:.5f} lamE={lamE(tau,beta) if tau<1 else float('nan'):.5f} M={M_(L,beta):.4f} reg={regime(D,L,rho,k,beta):7s} s={out['s']:.3f} recruit={out['recruit']} okres={out['ok_res']} okL={out['ok_L']} entry={out['entry']:.5f}")


# Counterexample
scan('astra cx',4.5,.5,.5,.2,.01,.4,[4+0.25*i for i in range(24)])
