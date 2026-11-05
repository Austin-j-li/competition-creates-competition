# generic point-mass classes h>l>p, incumbent law given by numeric CDF; compute Delta, gL, gH, tau, J
import numpy as np
def objs(F,h,l,p,cH,n=40001):
    y=np.linspace(p,h,n); dy=y[1]-y[0]
    Fy=F(y)
    Dm=(y>=l)  # D=1 on [l,h)
    Delta=np.sum((1-Fy)*Dm)*dy
    gL=np.sum(Fy*(y<l))*dy
    gam=np.sum(Fy*Dm)*dy
    tau=(cH-gL)/gam
    return Delta,gL,gam,tau,Delta*(1-tau)
# Astra example
h,l,p,cH=10,1,0.5,2
for z in [6.0,6.5,7.0,7.3,7.5,7.8]:
    F=lambda y,z=z: np.clip((y-(z-0.1))/0.2,0,1)
    Dl,gL,gam,tau,J=objs(F,h,l,p,cH)
    print("Astra z",z,"Delta/K",round(Dl/9,3),"tau",round(tau,3),"Delta/K+tau",round(Dl/9+tau,3),"J",round(J,3))
# genuine non-interval: mixture (1-q)U[0,u]+q U[A,A+0.1]; stage1 u:0.5->1, stage2 A: 1.5->2.5
h,l,p,cH=10,1,0.5,None
q=0.5
def mix(u,A):
    return lambda y: (1-q)*np.clip(y/u,0,1)+q*np.clip((y-A)/0.1,0,1)
path=[(0.5+0.5*t,1.5) for t in np.linspace(0,1,11)]+[(1.0,1.5+0.1*j) for j in range(1,11)]
# choose cH so tau ~0.6 at start
D0,gL0,gam0,_,_=objs(mix(0.5,1.5),h,l,p,0)
cH=gL0+0.6*gam0
print("cH",cH)
rows=[]
for (u,A) in path:
    Dl,gL,gam,tau,J=objs(mix(u,A),h,l,p,cH)
    rows.append((u,A,Dl,gL,tau,J))
    print("u %.2f A %.2f Delta %.4f gL %.4f tau %.4f J %.5f"%(u,A,Dl,gL,tau,J))
