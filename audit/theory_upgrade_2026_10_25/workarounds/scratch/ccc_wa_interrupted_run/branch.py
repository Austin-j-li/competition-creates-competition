import math

def brentq(f,lo,hi):
    flo=f(lo)
    for _ in range(200):
        mid=(lo+hi)/2; fm=f(mid)
        if (fm>0)==(flo>0): lo,flo=mid,fm
        else: hi=mid
    return (lo+hi)/2


def auction(r,h,l,p):
    # point masses h,l ; R~U[0,r], l<=r<=h
    D = (r-l)**2/(2*r)
    gam = (r*r-l*l)/(2*r) + h - r
    gL = (l*l-p*p)/(2*r)
    return D, gam, gL

def m(lam,beta): return beta*(1-lam)/(2*beta+(1-2*beta)*lam)
def lamE(tau,beta): return beta*(2*tau-1)/(beta+(1-2*beta)*(1-tau))

def research_star(D,k,rho,beta,a):
    # unified: 2 a lam = D m - k + (rho D m - k)^+
    f=lambda lam: D*m(lam,beta)-k+max(0.0,rho*D*m(lam,beta)-k)-2*a*lam
    if f(0)<=0: return 0.0
    return brentq(f,0,1-1e-12)

def regime(D,lam,k,rho,beta):
    b=(1-lam)*beta
    if rho*D/2<=k: return 'R (L abstains)', 0.0
    if rho*D*m(lam,beta)>=k: return 'R2 (L sells)',1.0
    s=b*(rho*D/k-2)/lam
    return 'Rmix (L mixes)', s

def run(name,h,l,p,cH,k,rho,beta,a,cap,rs):
    print('==',name, 'cap-before-sell cond: rho(2a cap+k)=%.5f  2k m_cap=%.5f'%(rho*(2*a*cap+k),2*k*m(cap,beta)))
    print('  2 m_cap=%.4f rho=%.3f  Delta_cap=%.4f Delta_N=%.4f'%(2*m(cap,beta),rho,(2*a*cap+k)/m(cap,beta),2*k/rho))
    for r in rs:
        D,gam,gL=auction(r,h,l,p); tau=(cH-gL)/gam
        lam=research_star(D,k,rho,beta,a); lamc=min(lam,cap)
        reg,s=regime(D,lamc,k,rho,beta)
        lE=lamE(tau,beta) if 0.5<tau<1 else float('nan')
        rec = lamc>=lE
        ent=rho+(1-rho)*(beta+(0.5-beta)*lamc) if rec else rho
        V=0.5*(D*m(lamc,beta)-k)+0.5*max(0,rho*D*m(lamc,beta)-k)
        print('  r=%.3f D=%.4f tau=%.4f lamE=%.4f lam*=%.4f%s %s s=%.3f recruit=%s entry=%.5f V/a=%.4f rhoD/2-k=%.4f'%(r,D,tau,lE,lamc,'(cap)' if lam>=cap else '',reg,s,rec,ent,V/a,rho*D/2-k))

run('counterexample',10,1,.5,4.5,.5,.5,.2,.01,.4,[4,4.5,5,5.5,5.83,6,6.5,7,7.28,7.5,8])

import math
beta=0.294655; u=math.e-1; cap=u*beta/(1+u*beta)
print('cap',cap)
run('benchmark',10,1,.5,6,1/50,.25,beta,1/40,cap,[1.45,1.50,1.5010,1.55,1.6,1.65,1.6776,1.70,1.7479,1.80,1.9,2.0,2.2,2.434,2.8,3.2,3.59,3.6])
# root finding for endpoints in benchmark
def phi(r,h=10,l=1,p=.5,cH=6,k=1/50,rho=.25,a=1/40):
    D,gam,gL=auction(r,h,l,p); tau=(cH-gL)/gam
    return D*(1-tau)-k-2*a*lamE(tau,beta)
for r in [1.3,1.4,1.5,1.6,1.75,2,2.5,3,3.3,3.5,3.59]:
    print('phi_a(%.2f)=%.5f'%(r,phi(r)))
k=1/50;rho=.25;a=1/40
mc=m(cap,beta)
print('paper cond: 2k m_cap - rho(2a cap+k) =',2*k*mc-rho*(2*a*cap+k), ' IM cond: k - rho(2a cap+k)=',k-rho*(2*a*cap+k))
print('rho thresholds: paper rho<=',2*k*mc/(2*a*cap+k),' IM rho<=',k/(2*a*cap+k))
print('Delta_cap',(2*a*cap+k)/mc,'Delta_N',2*k/rho,'Delta_S(cap) where rho D m_cap=k',k/(rho*mc))
