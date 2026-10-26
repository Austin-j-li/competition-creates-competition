import numpy as np
import math
erf=np.vectorize(math.erf)
def lncdf(x,s,scale):
    x=np.asarray(x,float); out=np.zeros_like(x); m=x>0; out[m]=0.5*(1+erf(np.log(x[m]/scale)/(s*np.sqrt(2)))); return out
def brentq(f,a,b):
    fa=f(a)
    if fa*f(b)>0: raise ValueError
    for _ in range(80):
        c=(a+b)/2; fc=f(c)
        if fa*fc<=0: b=c
        else: a,fa=c,fc
    return (a+b)/2
p=0.5; cH=6.0; M=0.731059
def make(kind,s):
    if kind=='lognormal':
        GH=lambda y: lncdf(y-p,s,10-p)
        GL=lambda y: lncdf(y-p,s,1-p)
    if kind=='uniform':  # half-width s*value
        GH=lambda y: np.clip((y-10*(1-s))/(20*s),0,1)
        GL=lambda y: np.clip((y-(1-s*0.5))/(1.0*s),0,1)  # half-width s*0.5 keeps >= p
    if kind=='exp':  # p + exponential with means h-p, l-p
        GH=lambda y: np.where(y>p,1-np.exp(-(y-p)/(10-p)),0)
        GL=lambda y: np.where(y>p,1-np.exp(-(y-p)/(1-p)),0)
    return GH,GL
ys=np.linspace(0,60,240001)
for kind,ss in [('lognormal',[0.1,0.3,0.5,1.0]),('uniform',[0.2,0.5,0.9]),('exp',[None])]:
    for s in ss:
        GH,GL=make(kind,s); D=GL(ys)-GH(ys)
        dD=np.diff(D); ystar=ys[np.argmax(dD< -1e-12)]  # first point where D decreases
        cum=np.concatenate([[0],np.cumsum((D[1:]+D[:-1])/2*np.diff(ys))])
        def gap(r): return np.interp(r,ys,cum)/r
        def W(G,r): # E_G[F(theta)], F=U[0,r]
            th=ys; dens=np.gradient(G(th),th); return np.trapezoid(np.minimum(th/r,1)*dens,th)
        def gam(r): return gap_int(r,'g')
        def gap_int(r,w):
            m=(ys>=p); y=ys[m]; F=np.minimum(y/r,1); d=D[m]
            return np.trapezoid((F if w=='g' else 1-F)*d,y)
        def gL(r):
            m=(ys>=p); y=ys[m]; return np.trapezoid((1-GL(y))*np.minimum(y/r,1),y)
        tau=lambda r:(cH-gL(r))/gap_int(r,'g')
        rs=np.linspace(1.2,30,2000); gs=np.array([gap(r) for r in rs])
        rstar=rs[np.argmax(gs)]
        try: rC=brentq(lambda r:tau(r)-M,1.2,60)
        except Exception as e: rC=float('nan')
        print(f"{kind:9s} s={s}: D increasing up to y*={ystar:.3f}; gap peak r**={rstar:.3f}; rC={rC:.3f}; "
              f"gap(1.2)={gap(1.2):.4f} gap(3)={gap(3):.4f} gap(3.6)={gap(3.6):.4f}; WH(3.6)={W(GH,3.6):.4f} WL(3.6)={W(GL,3.6):.4f}; tau(3)={tau(3):.3f} tau(3.6)={tau(3.6):.3f}")
print("---- pivotal shares at the gap peak r** (uniform family)")
for kind,ss in [('lognormal',[0.3,0.5,1.0]),('uniform',[0.5,0.9]),('exp',[None])]:
    for s in ss:
        GH,GL=make(kind,s); D=GL(ys)-GH(ys)
        cum=np.concatenate([[0],np.cumsum((D[1:]+D[:-1])/2*np.diff(ys))])
        rs=np.linspace(1.2,30,4000); gs=np.interp(rs,ys,cum)/rs; rstar=rs[np.argmax(gs)]
        dens=np.gradient(GH(ys),ys); WH=np.trapezoid(np.minimum(ys/rstar,1)*dens,ys)
        Dr=np.interp(rstar,ys,D)
        print(f"{kind} s={s}: r**={rstar:.3f}, D(r**)={Dr:.4f} vs avg={gs.max():.4f}; Pr(incumbent beats H) at r** = {1-WH:.3f}; Pr_H(theta<r**)={np.interp(rstar,ys,GH(ys)):.3f}")
# benchmark scaling of Sol counterexample
h,l=10,1
for r in [3,3.6,9,10,12,20]:
    WH=min(h/r,1); WL=l/r; print(f"benchmark r={r}: WH-WL={WH-WL:.4f}")
