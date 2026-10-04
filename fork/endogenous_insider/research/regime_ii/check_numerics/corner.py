"""v -> 0 corner of the starved family: L abstains, H buys 1; the cutoff solves C_L(0,x') = k."""
import math
from scipy import optimize
from model import *
P0=Prm(r=3.0,k=0.02,rho=0.25)
def CL(P,xp,h=1e-6):
    oH,oL=((1.0,1.0),),((0.0,1.0),)
    pcs=entry_pieces(P,oH,oL,((-math.inf,xp),))
    return (payoff(P,'L',-h,pcs,oH,oL)+P.k*h)/h
for cL in (3.9,3.95,4.0,4.2):
    P=with_(P0,cL=cL); a=auction(P)
    try:
        xp=optimize.brentq(lambda x: CL(P,x)-P.k, 0.0, 8.0, xtol=1e-11)
    except ValueError:
        print("cL=%.2f: no root of C_L=k in [0,8]; C_L(0)=%.5f C_L(8)=%.5f"%(cL,CL(P,0.0),CL(P,8.0))); continue
    pb=mubar_gen=F(xp-1,P.b)/(F(xp-1,P.b)+F(xp,P.b))
    oH,oL=((1.0,1.0),),((0.0,1.0),)
    r=check(P,oH,oL,((-math.inf,xp),),ngrid=401)
    print("cL=%.2f x'=%.4f pool belief=%.5f (tauL=%.5f) acc=%s E=%.5f OH=%.5f regH=%.1e regL=%.1e brH=%.3f brL=%.3f"%(cL,xp,pb,a.tauL,r['accepted'],r['E'],r['OH'],r['regret_H'],r['regret_L'],r['br_H'],r['br_L']))
