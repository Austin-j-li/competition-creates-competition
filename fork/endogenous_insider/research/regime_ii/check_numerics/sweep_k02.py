"""Sweep at r1=3, rho=.25, k=.02: full-order family members and the knapsack worst pools, checked by quadrature."""
import csv, sys, time
from model import *
from bathtub import *
rows=[]
cLs=[2.40,2.60,2.80,2.95,2.98,3.00,3.20,3.50,4.00]
for cL in cLs:
    P=Prm(cL=cL,r=3.0)
    a=auction(P); oH,oL=full_orders()
    z=z0(P); xb=xbar(P)
    members={'min_pool':((-math.inf,z),),
             'halfline_xbar':((-math.inf,xb-1e-7),),}
    kn=knap(P,1e-3,scale=0.999)
    members['bathtub_E']=((-math.inf,z),)+kn.poolE
    members['bathtub_eH']=((-math.inf,z),)+kn.poolH
    for name,pool in members.items():
        t=time.time()
        r=check(P,oH,oL,pool,ngrid=101)
        rows.append(dict(cL=cL,member=name,**{k:r[k] for k in ('accepted','pool_belief','tauL','pool_prob','regret_H','regret_L','br_H','br_L','E','eH','eL','OH')}))
        print(cL,name,r['accepted'],"E=%.5f OH=%.5f eH=%.5f pb=%.5f/%.5f regH=%.1e regL=%.1e (%.1fs)"%(r['E'],r['OH'],r['eH'],r['pool_belief'],r['tauL'],r['regret_H'],r['regret_L'],time.time()-t),flush=True)
with open('sweep_k02.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
