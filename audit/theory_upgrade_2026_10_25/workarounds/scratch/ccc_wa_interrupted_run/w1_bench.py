from math import sqrt
h,l,p,rho,cH,k=10,1,0.5,0.25,6,1/50
K=h-l
def D(r): return (r-l)**2/(2*r)
def gL(r): return (l*l-p*p)/(2*r)
def gam(r): return K-D(r)
def tau(r): return (cH-gL(r))/gam(r)
def J(r): return D(r)*(1-tau(r))
def kap(r): return (r*r-l*l)/(r*r-p*p)
def bis(f,a,b):
    for _ in range(200):
        m=(a+b)/2
        if (f(a)>0)==(f(m)>0): a=m
        else: b=m
    return (a+b)/2
r0,r2=1.2,3.6
rA=bis(lambda r:J(r)-k,r0,r2)
rN=bis(lambda r:rho*D(r)/2-k,r0,r2)
print("rA",rA,"rN",rN,"tau(r0)",tau(r0),"tau(r2)",tau(r2))
print("Delta(rA)",D(rA),"kappa(rA)",kap(rA),"tauA",tau(rA))
print("(i) crossing margin kappa*k*K/Delta^2 at rA:",kap(rA)*k*K/D(rA)**2)
for lab,r in [("r1? M band low tau(r1)",None)]: pass
# global monotone margin
import numpy as np
rs=np.linspace(r0,r2,20001)
g=[kap(r)*(1-tau(r))*K/D(r) for r in rs]
i=int(np.argmin(g)); print("(iv) min over path kappa(1-tau)K/Delta:",g[i],"at r",rs[i])
# also direct J' sign numeric
dJ=np.diff([J(r) for r in rs]); print("min dJ",dJ.min())
print("kappa(r0)",kap(r0),"kappa(rN)",kap(rN))
print("(iii) all-prior uniform: kappa(r0)*rho^2*K/(4k) =",kap(r0)*rho**2*K/(4*k))
print("   with kappa over [r0,rN] min (same):",kap(r0))
# band M in (tau(r1),tau(r2)); r1? find from registry: try r1=2? 
for M in [tau(2.0),tau(r2), 0.7]:
    print("M",M,"(ii) kappa(r0)K max(rho/2,1-M)^2/k=",kap(r0)*K*max(rho/2,1-M)**2/k)
# where is the relevant crossing region: s in I with J=k only rA. Delta bound in I at pi=1/2:
print("Delta bound 2k/rho",2*k/rho,"Delta(rN)",D(rN))
# condition with kappa at rA but uniform Delta bound
print("kappa(rA)K(rho/2)^2/k",kap(rA)*K*(rho/2)**2/k)
