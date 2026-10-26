# Random search: pairs of incumbent laws (piecewise-uniform mixtures) with general ranked classes.
# Report how often a mixture of two coexistence laws fails coexistence (convexity check), and
# how often a random FOSD path has a disconnected coexistence set.
import numpy as np
rng=np.random.default_rng(1)
p=0.5; X=np.linspace(p,12,6001)
GH=lambda x: np.clip((x-4)/6,0,1)        # class H ~ U[4,10]
GL=lambda x: np.clip((x-0.5)/2.5,0,1)    # class L ~ U[0.5,3]
D=GL(X)-GH(X)
def stats(Fx,cH):
    Dl=np.trapezoid((1-Fx)*D,X); gL=np.trapezoid(Fx*(1-GL(X)),X); gH=np.trapezoid(Fx*(1-GH(X)),X)
    gam=gH-gL; return Dl,gam,(cH-gL)/gam
def co(Fx,cH,pi,M,rho,k):
    Dl,gam,t=stats(Fx,cH)
    return (Dl>0 and gam>0 and Dl*(1-t)>=k and pi<t<=M and rho*Dl*max(pi,1-pi)<=k)
def randlaw():
    n=3; w=rng.dirichlet(np.ones(n)); lo=rng.uniform(0,6,n); wid=rng.uniform(0.05,2,n)
    return sum(wi*np.clip((X-a)/c,0,1) for wi,a,c in zip(w,lo,wid))
rho,k,pi=0.25,0.02,0.5; M=0.8
pairs=0; fails=0
for trial in range(20000):
    cH=rng.uniform(1,6)
    F0,F1=randlaw(),randlaw()
    if co(F0,cH,pi,M,rho,k) and co(F1,cH,pi,M,rho,k):
        pairs+=1
        for a in np.linspace(0,1,21):
            if not co((1-a)*F0+a*F1,cH,pi,M,rho,k): fails+=1; break
print("coexistence pairs found:",pairs," mixtures failing:",fails)
