import math, csv
from model import *
rows=[]
for r2 in (3.6,3.8,4.0,5.0):
    for cL in (2.0,2.4,3.0):
        P=Prm(cL=cL,r=r2,k=0.02,rho=0.25); a=auction(P)
        regimeM=B(P,a.m); regimeH=B(P,0.5); ceil=B(P,a.M)
        oH,oL=full_orders()
        if not (a.tauL<1): continue
        z=z0(P) if 0<a.tauL<1 else None
        # full orders, minimal pool (regime II) or none (regime I)
        if cL>regimeM:
            pool=((-math.inf,z),)
        else:
            pool=()
        r=check(P,oH,oL,pool,ngrid=201)
        reg = "I" if cL<regimeM else ("II" if cL<=regimeH else "III")
        print("r2=%.1f cL=%.1f regime %s  B(m)=%.3f B(1/2)=%.3f B(M)=%.3f (<cH=6: %s)  acc=%s E=%.5f OH=%.5f  E<rho:%s OH<rho/2:%s"%(r2,cL,reg,regimeM,regimeH,ceil,ceil<6,r['accepted'],r['E'],r['OH'],r['E']<0.25-1e-12,r['OH']<0.125-1e-12),flush=True)
        rows.append(dict(r2=r2,cL=cL,regime=reg,ceilingBelowcH=ceil<6,accepted=r['accepted'],E=r['E'],OH=r['OH']))
with open('collapse.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
