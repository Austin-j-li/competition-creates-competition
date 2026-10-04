import csv, sys
from model import *
from bathtub import *
rows=[]
base=dict(rho=0.25)
tab={0.1:(3.9201,4.0036),0.2:(3.6330,3.8350),0.25:(3.4607,3.7408),0.3:(3.2638,3.6388),0.35:(3.0366,3.5280),0.5:(2.3726,3.1300)}
for rho,(tE,tH) in tab.items():
    P=Prm(rho=rho,cL=3.0,r=3.0)
    lo=auction(P).gL+auction(P).m*(auction(P).gH-auction(P).gL)+1e-6
    for h1 in (2e-3,1e-3,5e-4):
        rE=threshold(P,'E',lo,4.29,h1); rH=threshold(P,'H',lo,4.29,h1)
        print(rho,h1,"E %.5f (theory %.4f)  H %.5f (theory %.4f)"%(rE,tE,rH,tH),flush=True)
    rows.append(dict(rho=rho,thrE=rE,thrH=rH,theoryE=tE,theoryH=tH))
with open('thr_bathtub.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
