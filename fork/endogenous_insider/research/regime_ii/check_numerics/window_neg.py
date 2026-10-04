"""Critical test: starved members with a pool cutoff BELOW zero at the paper's k=0.02, inside the open window."""
import math, csv
from scipy import optimize
from model import *
from starved import UL_prime
rows=[]
for cL in (2.5,2.6,2.7,2.8,2.9,2.95,2.98,3.0):
    P=Prm(cL=cL,r=3.0,k=0.02,rho=0.25); a=auction(P); vH=P.b*logit(a.tauH)-1
    acc=[]; consistent=0
    for i in range(121):
        v=0.02+(vH-0.02-1e-6)*i/120
        g=lambda xp: UL_prime(P,v,xp)
        xp=None
        for lo,hi in ((-2.0,0.0),(0.0,8.0)):
            try: xp=optimize.brentq(g,lo,hi,xtol=1e-12)
            except ValueError: xp=None
            if xp is None: continue
            pb=F(xp-1,P.b)/(F(xp-1,P.b)+F(xp+v,P.b))
            if pb>=a.tauL: continue
            consistent+=1
            r=check(P,((1.0,1.0),),((-v,1.0),),((-math.inf,xp),),ngrid=401)
            if r['accepted']: acc.append((v,xp,r['E'],r['OH']))
    msg = ("min E=%.5f at v=%.4f x'=%.4f" % (min(acc, key=lambda t: t[2])[2], min(acc, key=lambda t: t[2])[0], min(acc, key=lambda t: t[2])[1])) if acc else ""
    print("cL=%.2f  consistent starved candidates (x' any sign): %d ; accepted: %d %s" % (cL, consistent, len(acc), msg), flush=True)
    rows.append(dict(cL=cL,consistent=consistent,accepted=len(acc),minE=(min(a[2] for a in acc) if acc else '')))
with open('window_neg.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
