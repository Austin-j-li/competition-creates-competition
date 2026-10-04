"""Starved family and pooled schedules at rho=0.1 (numerics claims no break; 288 unconverged starts)."""
import math
from model import *
from starved import *
for rho in (0.1,):
    for cL in (3.0,3.5,4.0):
        P=Prm(rho=rho,cL=cL,r=3.0,k=0.02); a=auction(P)
        vH=P.b*logit(a.tauH)-1
        found=0
        for v in [0.02+0.05*i for i in range(15)]+[vH-1e-3]:
            m=member(P,v)
            if m is not None: found+=1
        print("rho=%.2f cL=%.1f starved members with x'>=0 on v grid: %d ; UL' at x'=0: v=.5 -> %.5f ; k=%.3f"%(rho,cL,found,UL_prime(P,0.5,0.0),P.k))
