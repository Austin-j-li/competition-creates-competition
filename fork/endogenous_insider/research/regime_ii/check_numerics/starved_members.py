import csv, math
from model import *
from starved import *
rows=[]
for cL in (3.0,3.5,4.0):
    P=Prm(cL=cL,r=3.0,k=0.02,rho=0.25); a=auction(P)
    vH=P.b*logit(a.tauH)-1
    vs=[0.05,0.2,0.4,0.55,0.65,0.70,0.7344,0.738,0.742,vH-1e-4]
    for v in vs:
        m=member(P,v)
        if m is None: continue
        cons=m['pool_belief']<a.tauL and m['mu_at_xp']>=a.tauL
        if not cons:
            continue
        pool=((-math.inf,m['xp']),)
        r=check(P,((1.0,1.0),),((-v,1.0),),pool,ngrid=401)
        rows.append(dict(cL=cL,v=v,xp=m['xp'],**{k:r[k] for k in ('accepted','pool_belief','tauL','regret_H','regret_L','br_H','br_L','E','eH','OH')}))
        print(cL,"v=%.4f x'=%.4f"%(v,m['xp']),r['accepted'],"E=%.5f OH=%.5f pb=%.5f regH=%.1e regL=%.1e brH=%.4f brL=%.4f"%(r['E'],r['OH'],r['pool_belief'],r['regret_H'],r['regret_L'],r['br_H'],r['br_L']),flush=True)
with open('starved_members.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
