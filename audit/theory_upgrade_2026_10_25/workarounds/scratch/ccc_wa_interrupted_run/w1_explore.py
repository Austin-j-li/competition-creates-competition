# Explore coexistence along FOSD paths. h=10, l=1 point masses; p=1/2.
import numpy as np
h,l,p=10.0,1.0,0.5
def integ(F,a,b,n=200001):
    x=np.linspace(a,b,n); y=F(x); return np.trapezoid(y,x)
def red(F,cH):
    D=integ(lambda x:1-F(x),l,h)          # Delta = int_l^h (1-F)
    gL=integ(F,p,l)                        # g_L = int_p^l F
    gH=integ(F,p,h)
    gam=gH-gL
    tau=(cH-gL)/gam
    return D,gL,gam,tau
def mixunif(parts):
    # parts: list of (weight, lo, hi)
    def F(x):
        out=np.zeros_like(x)
        for w,a,b in parts: out+=w*np.clip((x-a)/(b-a),0,1)
        return out
    return F
def coexist(D,tau,pi,M,rho,k):
    J=D*(1-tau)
    return (J>=k) and (pi<tau<=M) and (rho*D*max(pi,1-pi)<=k), J
rho,k,pi=0.25,0.02,0.5
lam,beta=0.5,1/3; b=(1-lam)*beta; u=lam/b; M=(1+u)/(2+u)
print("M(1/2)=",M)
cH=6.825; q=0.5; dl=0.002
print("--- two-phase FOSD path: phase1 moves low mass x1 0.55->0.91, phase2 moves high mass x2 1.16->1.30")
path=[]
for x1 in np.linspace(0.55,0.91,10): path.append((x1,1.16))
for x2 in np.linspace(1.16,1.30,10)[1:]: path.append((0.91,x2))
for s,(x1,x2) in enumerate(path):
    F=mixunif([(q,x1-dl,x1+dl),(1-q,x2-dl,x2+dl)])
    D,gL,gam,tau=red(F,cH)
    c,J=coexist(D,tau,pi,M,rho,k)
    E=rho+(1-rho)*min((1-pi)*b*D/k,b+pi*lam) if c else None
    print(f"s={s:2d} x1={x1:.3f} x2={x2:.3f} Delta={D:.4f} gL={gL:.4f} tau={tau:.4f} J={J:.5f} coexist={c} entry={E}")
