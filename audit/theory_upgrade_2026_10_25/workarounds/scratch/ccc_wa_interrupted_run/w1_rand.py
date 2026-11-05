import numpy as np
rng=np.random.default_rng(1)
# point masses h>l>p, R~U[0,r], l<r<h closed forms
def f(r,h,l,p,cH):
    D=(r-l)**2/(2*r); gL=(l*l-p*p)/(2*r); K=h-l; gam=K-D; tau=(cH-gL)/gam; return D,tau,D*(1-tau)
hits=[];N=0
for it in range(200000):
    l=1.0; h=l+rng.uniform(0.05,20); p=rng.uniform(0,l)
    rs=np.linspace(l+1e-6,h-1e-6,1500)
    # cH: between g_L range and gH so tau in (0,1) somewhere
    cH=rng.uniform(0,h)
    rho=rng.uniform(0.01,0.99); M=rng.uniform(0.5,0.999)
    D,tau,J=f(rs,h,l,p,cH)
    Jmax=J[(tau>0.5)&(tau<=M)].max() if np.any((tau>0.5)&(tau<=M)) else None
    if Jmax is None or Jmax<=0: continue
    k=rng.uniform(0,Jmax)
    N+=1
    I=(tau>0.5)&(tau<=M)&(rho*D/2<=k)
    s=np.sign(J-k)
    down=np.where((s[:-1]>0)&(s[1:]<=0)&I[:-1]&I[1:])[0]
    if len(down):
        i=down[0]; r=rs[i]
        hits.append((h,p,cH,rho,M,k,r,D[i],tau[i],D[i]/(h-l),k/(h-l)))
print("draws",N,"downcrossings inside I:",len(hits))
hits.sort(key=lambda x:x[-1])
for x in hits[:8]: print("h %.2f p %.2f cH %.2f rho %.2f M %.3f k %.4f r %.3f Delta %.3f tau %.3f Delta/K %.3f k/K %.4f"%x)
if hits:
    a=np.array(hits); print("min k/K",a[:,-1].min(),"min Delta/K",a[:,-2].min(),"min r/h",(a[:,6]/a[:,0]).min(), "min tau", a[:,8].min())
print("--- hits sorted by tau")
hits.sort(key=lambda x:x[8])
for x in hits[:10]:
    h,p,cH,rho,M,k,r,D,tau,_,_=x
    kap=(r*r-1)/(r*r-p*p)
    print("h %.2f p %.2f cH %.2f rho %.2f M %.3f k %.4f r %.3f Delta %.3f tau %.3f Delta/K %.3f kappa %.3f k/(kappa K (1-tau)^2) %.3f gH-cH %.3f"%(h,p,cH,rho,M,k,r,D,tau,D/(h-1),kap,k/(kap*(h-1)*(1-tau)**2),(h-r/2-p*p/(2*r))-cH))
import collections
a=np.array(hits)
print("share of hits with tau<0.8:",np.mean(a[:,8]<0.8),"tau<0.9:",np.mean(a[:,8]<0.9))
print("share of hits with Delta/K>0.3:",np.mean(a[:,9]>0.3))
