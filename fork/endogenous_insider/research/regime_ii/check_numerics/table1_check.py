"""Theory Table 1 at rho=.25: pibar, K, E0, inf E, eH0, inf eH; plus acceptance of the worst pool at k = 0.9*K."""
import csv, math
from model import *
from bathtub import knap
from formulas_check import K_of
rows=[]
theory={2.37:(0.359,0.01068,0.4371,0.4330,0.6023,0.6000),2.50:(0.447,0.00858,0.4339,0.4107,0.6005,0.5790),
        2.80:(0.542,0.00708,0.4268,0.3711,0.5962,0.5253),3.00:(0.591,0.00648,0.4225,0.3403,0.5934,0.4824),
        3.20:(0.637,0.00601,0.4183,0.3048,0.5904,0.4325),3.40:(0.683,0.00558,0.4143,0.2637,0.5873,0.3742),
        3.60:(0.736,0.00494,0.4105,0.2157,0.5842,0.3057),3.80:(0.797,0.00402,0.4067,0.1591,0.5810,0.2244),
        4.00:(0.868,0.00261,0.4030,0.0916,0.5777,0.1269),4.20:(0.955,0.00090,0.3994,0.0158,0.5742,0.0210)}
for cL,(pb,K,E0,iE,eH0,ieH) in theory.items():
    P=Prm(cL=cL,r=3.0,rho=0.25,k=0.02)
    kn=knap(P,2.5e-4); xb=xbar(P); pibar=0.5*(F(xb-1,P.b)+F(xb+1,P.b)); Kv=K_of(P)
    Q=with_(P,k=0.9*Kv)
    kn2=knap(Q,2.5e-4,scale=0.999)
    r=check(Q,*full_orders(),((-math.inf,z0(Q)),)+kn2.poolE,ngrid=61)
    print("cL=%.2f pibar %.4f/%.3f  K %.5f/%.5f  E0 %.4f/%.4f infE %.4f/%.4f eH0 %.4f/%.4f infeH %.4f/%.4f | worst pool at k=0.9K accepted=%s regL=%.1e"
          %(cL,pibar,pb,Kv,K,kn.E0,E0,kn.infE,iE,kn.eH0,eH0,kn.infeH,ieH,r['accepted'],r['regret_L']),flush=True)
    rows.append(dict(cL=cL,pibar=pibar,K=Kv,E0=kn.E0,infE=kn.infE,eH0=kn.eH0,infeH=kn.infeH,
                     th_pibar=pb,th_K=K,th_E0=E0,th_infE=iE,th_eH0=eH0,th_infeH=ieH,accepted_at_09K=r['accepted']))
with open('table1_check.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
