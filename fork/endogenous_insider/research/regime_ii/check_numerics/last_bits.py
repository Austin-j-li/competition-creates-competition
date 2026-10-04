import csv, math
from model import *
from bathtub import knap
rows=[]
# (a) c_L = 2.975 at k=.02: minimal pool, half-line end, worst pool (accepted?)
P=Prm(cL=2.975,r=3.0,k=0.02,rho=0.25)
oH,oL=full_orders(); z=z0(P); xb=xbar(P)
kn=knap(P,2.5e-4,scale=0.999)
for name,pool in (("min",((-math.inf,z),)),("halfline",((-math.inf,xb-1e-7),)),("worst",((-math.inf,z),)+kn.poolE),("worst_eH",((-math.inf,z),)+kn.poolH)):
    r=check(P,oH,oL,pool,ngrid=201)
    print("cL=2.975 %-9s acc=%s E=%.5f OH=%.5f pool prob=%.4f regL=%.1e"%(name,r['accepted'],r['E'],r['OH'],r['pool_prob'],r['regret_L']))
    rows.append(dict(case="cL2.975_"+name,**{k:r[k] for k in ('accepted','E','OH','pool_prob','regret_L')}))
print("knap at 2.975: infE=%.5f infeH=%.5f -> inf OH=%.5f"%(kn.infE,kn.infeH,kn.infeH/2))
# (b) adversary example variants at cL=2.4
for rho in (0.5,0.75,0.8):
    Q=Prm(cL=2.4,r=3.0,k=0.02,rho=rho)
    kn2=knap(Q,2.5e-4,scale=0.999)
    r=check(Q,oH,oL,((-math.inf,z0(Q)),),ngrid=201)
    print("rho=%.2f cL=2.4 minimal pool: E=%.5f (rho=%.2f) OH=%.5f (rho/2=%.3f) acc=%s | all-pools infE=%.5f infOH=%.5f"%(rho,r['E'],rho,r['OH'],rho/2,r['accepted'],kn2.infE,kn2.infeH/2))
    rows.append(dict(case="adv_rho%.2f_cL2.4"%rho,accepted=r['accepted'],E=r['E'],OH=r['OH'],pool_prob=r['pool_prob'],regret_L=r['regret_L']))
with open('last_bits.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
