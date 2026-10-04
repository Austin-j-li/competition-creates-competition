"""Theory referee's claim: starved equilibria at (cL,k)=(2.6,.03),(2.9,.03),(2.9,.035), below numerics' k_U."""
import math, csv
from model import *
from starved import member, UL_prime
from starved_thr import thr
rows=[]
for k in (0.025,0.03,0.035,0.04,0.05):
    try: t=thr(k)
    except Exception as e: t=float('nan')
    print("k=%.3f starved threshold cL=%.5f"%(k,t),flush=True)
for cL,k in ((2.6,0.03),(2.9,0.03),(2.9,0.035),(2.6,0.02)):
    P=Prm(cL=cL,r=3.0,k=k,rho=0.25); a=auction(P); vH=P.b*logit(a.tauH)-1
    best=None
    for i in range(40):
        v=0.2+(vH-0.2-1e-6)*i/39
        m=member(P,v)
        if m is None: continue
        if m['pool_belief']>=a.tauL: continue
        r=check(P,((1.0,1.0),),((-v,1.0),),((-math.inf,m['xp']),),ngrid=401)
        if r['accepted'] and (best is None or r['E']<best[1]['E']): best=(v,r,m)
    if best is None:
        print("cL=%.1f k=%.3f : no accepted starved member"%(cL,k))
        rows.append(dict(cL=cL,k=k,found=False,v='',E='',OH=''))
    else:
        v,r,m=best
        print("cL=%.1f k=%.3f : accepted starved member v=%.4f x'=%.4f E=%.5f OH=%.5f belief %.5f<%.5f regH=%.1e regL=%.1e"%(cL,k,v,m['xp'],r['E'],r['OH'],r['pool_belief'],r['tauL'],r['regret_H'],r['regret_L']))
        rows.append(dict(cL=cL,k=k,found=True,v=v,E=r['E'],OH=r['OH']))
with open('kcheck.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
