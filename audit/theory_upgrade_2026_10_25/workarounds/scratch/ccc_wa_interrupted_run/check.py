exec(open('branch.py').read().split("run('counterexample'")[0])
import math
def tuple_check(D,tau,k,rho,beta,a,cap,lam,sH,sL):
    # sH, sL: dicts q->prob
    b=(1-lam)*beta; b0=(1-lam)*(1-2*beta)
    eta={-1:b,0:b0,1:b}
    fH={q:eta[q]+lam*sH[q] for q in eta}; fL={q:eta[q]+lam*sL[q] for q in eta}
    mu={q:fH[q]/(fH[q]+fL[q]) for q in eta}
    e={q:(1.0 if mu[q]>tau+1e-12 else rho) for q in eta}
    UH={q:q*e[q]*D*(1-mu[q])-k*abs(q) for q in eta}
    UL={q:-q*e[q]*D*mu[q]-k*abs(q) for q in eta}
    V=0.5*max(UH.values())+0.5*max(UL.values())
    return mu,e,UH,UL,V,min(cap,V/a)
def show(label,r,h,l,p,cH,k,rho,beta,a,cap):
    D,gam,gL=auction(r,h,l,p); tau=(cH-gL)/gam
    lam=min(research_star(D,k,rho,beta,a),cap)
    reg,s=regime(D,lam,k,rho,beta)
    sH={-1:0,0:0,1:1}; sL={-1:s,0:1-s,1:0}
    mu,e,UH,UL,V,lamopt=tuple_check(D,tau,k,rho,beta,a,cap,lam,sH,sL)
    print(label,'r=%.3f'%r,reg,'lam=%.5f best=%.5f'%(lam,lamopt),'s=%.4f'%s,
      'mu=',{q:round(mu[q],4) for q in mu},'tau=%.4f'%tau,'e=',e,
      'UH=',{q:round(UH[q],5) for q in UH},'UL=',{q:round(UL[q],5) for q in UL})
for r in [6.0,7.0,7.25]:
    show('CE',r,10,1,.5,4.5,.5,.5,.2,.01,.4)
beta=0.294655; u=math.e-1; cap=u*beta/(1+u*beta)
for rho in [0.30,0.40]:
    # endpoints
    def solve(f,lo,hi):
        for _ in range(200):
            mid=(lo+hi)/2
            if f(mid)>0: hi=mid
            else: lo=mid
        return mid
    k=1/50;a=1/40
    rN=solve(lambda r: rho*auction(r,10,1,.5)[0]-2*k,1.01,5)
    rcap=solve(lambda r: research_star(auction(r,10,1,.5)[0],k,rho,beta,a)-cap,1.2,5)
    print('benchmark rho=%.2f: r_N=%.4f r_cap(unified)=%.4f r_cap(orig formula)=%.4f'%(rho,rN,rcap,solve(lambda r: auction(r,10,1,.5)[0]-(2*a*cap+k)/m(cap,beta),1.2,5)))
    for r in [1.6,rN+0.01,(rN+rcap)/2,rcap-0.002]:
        show(' B rho=%.2f'%rho,r,10,1,.5,6,k,rho,beta,a,cap)
