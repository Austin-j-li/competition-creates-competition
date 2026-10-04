import math, csv
from model import *
from forcing_map import *
P0=Prm(r=3.0,k=0.02,rho=0.25)
a0=auction(P0); vH=P0.b*logit(a0.tauH)-1
rows=[]
for cL in (2.55,2.58,2.5833,2.585,2.59,2.60,2.62):
    P=with_(P0,cL=cL); a=auction(P)
    best=(1e9,None); npool=0
    for i in range(0,61):
        v=0.65+ (vH-0.65-1e-6)*i/60
        for pool in consistent_cutoffs(P,a,1.0,-v,n=3):
            if pool!=(): npool+=1
            m,arg=schedule_min(P,1.0,-v,pool)
            if m<best[0]: best=(m,(v,pool))
    print("cL=%.4f  schedules with a pool: %d ; min over (1,-v), v in [.65,vH): m=%.5f at v=%.4f pool=%s"%(cL,npool,best[0],best[1][0],best[1][1]),flush=True)
    rows.append(dict(cL=cL,n_pool_sched=npool,kmin=best[0],v=best[1][0]))
with open('break_check.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
