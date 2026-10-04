"""Largest rho at which inf E >= rho (all pools) and E_0 >= rho (minimal pool), per cL. Own knapsack."""
import csv
from scipy import optimize
from model import Prm, with_
from bathtub import knap

def root(cL, which, pool):
    def g(rho):
        kn = knap(with_(Prm(r=3.0, cL=cL), rho=rho), 1e-3)
        v = {('E','all'):kn.infE, ('E','min'):kn.E0, ('H','all'):kn.infeH, ('H','min'):kn.eH0}[(which,pool)]
        return v - rho
    return optimize.brentq(g, 1e-7, 0.9999, xtol=1e-9)

if __name__ == "__main__":
    adv = {4.20:(0.0,0.4244,0.0,0.6416), 2.3662:(0.5145,0.5151,0.7332,0.7426), 2.37:(0.5034,0.5151,0.7332,0.7426), 2.50:(0.4488,0.5056,0.6760,0.7350),
           2.80:(0.3950,0.4866,0.5979,0.7181), 3.00:(0.3574,0.4755,0.5410,0.7070), 3.46:(0.2502,0.4535,0.3787,0.6820),
           3.74:(0.1654,0.4418,0.2504,0.6668), 4.00:(0.0676,0.4317,0.1023,0.6526),}
    rows=[]
    for cL,(aE,mE,aO,mO) in adv.items():
        try:
            r=[root(cL,'E','all'),root(cL,'E','min'),root(cL,'H','all'),root(cL,'H','min')]
        except ValueError:
            # no positive rho keeps the reversal: the all-pools entries are 0
            r=[0.0,root(cL,'E','min'),0.0,root(cL,'H','min')]
        print("cL=%.4f  entry all %.4f (adv %.4f)  entry min %.4f (%.4f)  own all %.4f (%.4f)  own min %.4f (%.4f)"%(cL,r[0],aE,r[1],mE,r[2],aO,r[3],mO),flush=True)
        rows.append(dict(cL=cL,entry_all=r[0],adv_entry_all=aE,entry_min=r[1],adv_entry_min=mE,own_all=r[2],adv_own_all=aO,own_min=r[3],adv_own_min=mO))
    with open('rho_curve.csv','w',newline='') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
