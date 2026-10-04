"""Half-line family at k=.02: verify the members where E or e_H reaches rho, and the end of the investor test."""
import csv, math
from scipy import optimize
from model import *
rows=[]
P0=Prm(r=3.0,k=0.02,rho=0.25)
b=P0.b
xE=optimize.brentq(lambda x:SX(x,b)-P0.rho,0,30,xtol=1e-13)
xO=optimize.brentq(lambda x:S(x-1,b)-P0.rho,0,30,xtol=1e-13)
xk=1+b*math.log((1-1/b)*auction(P0).m*auction(P0).DT/(2*P0.k))
print("xE=%.5f xO=%.5f xk=%.5f thrE=%.5f thrO=%.5f"%(xE,xO,xk,B(P0,mubar(xE,b)),B(P0,mubar(xO,b))))
for cL,xp in ((3.66,xE+0.002),(3.70,xE+0.05),(3.90,xO+0.002),(4.00,xO+0.05),(4.20,xk-0.01),(4.20,xk+0.05)):
    P=with_(P0,cL=cL); a=auction(P)
    oH,oL=full_orders()
    r=check(P,oH,oL,((-math.inf,xp),),ngrid=401)
    print("cL=%.2f x'=%.4f  belief %.5f < tauL %.5f ? %s  acc=%s E=%.5f OH=%.5f regL=%.2e brL=%.4f"%(cL,xp,mubar(xp,b),a.tauL,mubar(xp,b)<a.tauL,r['accepted'],r['E'],r['OH'],r['regret_L'],r['br_L']))
    rows.append(dict(cL=cL,xp=xp,belief=mubar(xp,b),tauL=a.tauL,accepted=r['accepted'],E=r['E'],OH=r['OH'],regL=r['regret_L']))
with open('halfline_check.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
