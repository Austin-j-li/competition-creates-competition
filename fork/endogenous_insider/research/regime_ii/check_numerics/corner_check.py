"""Decisive check of the small-rho corner: at cL=4.20 build the worst pool and verify by quadrature that
(a) its pool belief is below tauL (consistency) and (b) E < rho. Also tabulate the limit of the entry threshold."""
import math
from model import *
from bathtub import knap, threshold
P=Prm(r=3.0)
Bm=B(P,auction(P).m)
for cL,rho in ((4.20,0.0007),(4.20,0.0001),(4.20,0.02),(4.15,0.0007),(4.14,0.0007)):
    Q=with_(P,cL=cL,rho=rho); a=auction(Q)
    kn=knap(Q,2.5e-4,scale=0.999)
    pool=((-math.inf,z0(Q)),)+kn.poolE
    r=check(Q,*full_orders(),pool,ngrid=61)
    print("cL=%.2f rho=%.4f  E0=%.6g infE(knap)=%.6g  rho=%.6g | quad: E=%.6g pool belief=%.6g tauL=%.6g consistent=%s acc=%s"
          %(cL,rho,kn.E0,kn.infE,rho,r['E'],r['pool_belief'],a.tauL,r['pool_belief']<a.tauL,r['accepted']),flush=True)
print()
for rho in (1e-5,1e-4,1e-3,1e-2):
    print("rho=%g  entry threshold cL=%.5f  (B(1/2)=%.5f)"%(rho,threshold(with_(P,rho=rho),'E',Bm+1e-9,4.2916,2.5e-4),B(P,0.5)))
