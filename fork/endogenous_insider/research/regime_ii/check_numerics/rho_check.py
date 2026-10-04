import csv, math
from model import *
from bathtub import *
from formulas_check import K_of
rows=[]
def run(rho,cL,k=0.02,label=""):
    P=Prm(rho=rho,cL=cL,r=3.0,k=k)
    oH,oL=full_orders()
    z=z0(P)
    r=check(P,oH,oL,((-math.inf,z),),ngrid=401)
    kn=knap(P,1e-3,scale=0.999)
    r2=check(P,oH,oL,((-math.inf,z),)+kn.poolE,ngrid=201)
    print(label,"rho=%.4f cL=%.4f K=%.4f minpool: acc=%s E=%.5f eH=%.5f eL=%.5f OH=%.5f | worst pool acc=%s E=%.5f (knap inf %.5f)"%(rho,cL,K_of(P),r['accepted'],r['E'],r['eH'],r['eL'],r['OH'],r2['accepted'],r2['E'],kn.infE))
    rows.append(dict(rho=rho,cL=cL,k=k,K=K_of(P),acc=r['accepted'],E=r['E'],eH=r['eH'],eL=r['eL'],OH=r['OH'],worst_acc=r2['accepted'],worst_E=r2['E']))
P=Prm(r=3.0)
Bm=B(P,auction(P).m)
run(0.6,2.4,label="ADV example")
for rho in (0.5,0.5154,0.55,0.6,0.75,0.8):
    run(rho,Bm+1e-4,label="floor")
run(0.5,2.4162,label="num#5"); run(0.5,2.6662,label="num#5")
run(0.45,2.4162,label="num#5"); run(0.45,2.6662,label="num#5")
with open('rho_check.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
