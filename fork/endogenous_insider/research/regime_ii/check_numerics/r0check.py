import math, csv
from model import *
rows=[]
for rho in (0.1,0.25,0.5):
    for cL in (1.0,2.4,3.0,4.0,4.8):
        P=Prm(cL=cL,r=1.2,k=0.02,rho=rho)
        # zero orders is an equilibrium; test no profitable deviation and uniqueness margin
        r=check(P,((0.0,1.0),),((0.0,1.0),),(),ngrid=401)
        a=auction(P)
        # best deviation payoff of each type over q != 0 (should be negative: <= s(DT-k))
        oH=oL=((0.0,1.0),); pcs=entry_pieces(P,oH,oL,())
        devH=max(payoff(P,'H',q,pcs,oH,oL) for q in [0.01*i for i in range(1,101)])
        devL=max(payoff(P,'L',-q,pcs,oH,oL) for q in [0.01*i for i in range(1,101)])
        print("rho=%.2f cL=%.2f acc=%s E=%.12f OH=%.12f  best dev H %.5f L %.5f (bound s(DT-k) = %.5f per unit)"%(rho,cL,r['accepted'],r['E'],r['OH'],devH,devL,a.DT-P.k),flush=True)
        rows.append(dict(rho=rho,cL=cL,accepted=r['accepted'],E=r['E'],OH=r['OH'],devH=devH,devL=devL))
print("DT(r0)=",auction(Prm(r=1.2)).DT, " B_r0(1/2)=",B(Prm(r=1.2),0.5))
with open('r0check.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
