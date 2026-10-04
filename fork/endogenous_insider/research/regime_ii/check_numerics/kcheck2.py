import math
from scipy import optimize
from model import *
from starved import UL_prime
def member2(P,v,lo=-1.5,hi=8.0):
    g=lambda xp: UL_prime(P,v,xp)
    try: xp=optimize.brentq(g,lo,hi,xtol=1e-12)
    except ValueError: return None
    pb=F(xp-1,P.b)/(F(xp-1,P.b)+F(xp+v,P.b))
    return xp,pb
for cL,k in ((2.6,0.03),(2.9,0.035),(2.6,0.025),(2.9,0.03)):
    P=Prm(cL=cL,r=3.0,k=k,rho=0.25); a=auction(P); vH=P.b*logit(a.tauH)-1
    best=None; diag=[]
    for i in range(61):
        v=0.05+(vH-0.05-1e-6)*i/60
        m=member2(P,v)
        if m is None: diag.append((v,'no x\'')); continue
        xp,pb=m
        if pb>=a.tauL: diag.append((round(v,3),'belief %.4f>=tauL %.4f'%(pb,a.tauL))); continue
        r=check(P,((1.0,1.0),),((-v,1.0),),((-math.inf,xp),),ngrid=401)
        diag.append((round(v,3),'x\'=%.3f acc=%s E=%.4f regH=%.1e regL=%.1e brH=%.3f brL=%.3f'%(xp,r['accepted'],r['E'],r['regret_H'],r['regret_L'],r['br_H'],r['br_L'])))
        if r['accepted'] and (best is None or r['E']<best[1]): best=(v,r['E'],xp)
    print("== cL=%.1f k=%.3f tauL=%.4f  best=%s"%(cL,k,a.tauL,best))
    for d in diag[::10]: print("   ",d)
