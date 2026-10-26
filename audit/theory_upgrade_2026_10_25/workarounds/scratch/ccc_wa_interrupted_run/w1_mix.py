import numpy as np
exec(open('/tmp/ccc_wa/w1_explore.py').read().split('rho,k,pi=')[0])
rho,k,pi=0.25,0.02,0.5
lam,beta=0.5,1/3; b=(1-lam)*beta; u=lam/b; M=(1+u)/(2+u)
q=0.5; dl=0.002; cH=6.825
F0=mixunif([(q,0.55-dl,0.55+dl),(1-q,1.16-dl,1.16+dl)])
F1=mixunif([(q,0.91-dl,0.91+dl),(1-q,1.30-dl,1.30+dl)])
print("--- mixture path between the endpoints of the two-phase path")
for a in np.linspace(0,1,11):
    F=lambda x,a=a:(1-a)*F0(x)+a*F1(x)
    D,gL,gam,tau=red(F,cH); c,J=coexist(D,tau,pi,M,rho,k)
    E=rho+(1-rho)*min((1-pi)*b*D/k,b+pi*lam) if c else None
    print(f"alpha={a:.1f} Delta={D:.4f} gL={gL:.4f} tau={tau:.4f} J={J:.5f} coexist={c} entry={E}")
print("--- benchmark: mixture of U[0,6/5] and U[0,18/5], cH=6, benchmark slot band example")
cH=6.0
lam,beta=0.5,0.25; b=(1-lam)*beta; u=lam/b; M=(1+u)/(2+u); print("M=",M)
G0=mixunif([(1,0,1.2)]); G1=mixunif([(1,0,3.6)])
prev=None
for a in np.linspace(0,1,41):
    F=lambda x,a=a:(1-a)*G0(x)+a*G1(x)
    D,gL,gam,tau=red(F,cH); c,J=coexist(D,tau,pi,M,rho,k)
    E=rho+(1-rho)*min((1-pi)*b*D/k,b+pi*lam) if c else None
    if c!=prev or c: print(f"alpha={a:.3f} Delta={D:.4f} tau={tau:.4f} J={J:.5f} rhoD/2={rho*D/2:.4f} coexist={c} entry={E}")
    prev=c
