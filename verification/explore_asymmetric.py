#!/usr/bin/env python3
"""Pure-profile exploration, not exhaustive equilibrium enumeration.
Numerical stationary candidates must pass continuous-order deviation diagnostics.
"""
import json, math, csv
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.optimize import brentq, minimize_scalar
from review_checks import BASE, prims, lap_pdf, lap_surv, integrate_real

OUT=Path(__file__).resolve().parent/'results'

def candidate(r,u,v):
    a=BASE; pp=prims(r);tau=(a.cH-pp['gL'])/(pp['gH']-pp['gL'])
    maxmu=float(expit((u+v)/a.b))
    xs=(a.b*math.log(tau/(1-tau))+u-v)/2 if tau<=maxmu else math.inf
    mu=lambda x:float(expit((abs(x+v)-abs(x-u))/a.b))
    ent=lambda x:a.rho+(1-a.rho)*(x>=xs)
    ah=lambda x:ent(x)*pp['Delta']*(1-mu(x))
    al=lambda x:ent(x)*pp['Delta']*mu(x)
    def vals(s,sgn):
        A=ah if sgn==1 else al
        center=sgn*s;breaks=[-v,u,center,xs]
        F=integrate_real(lambda x:lap_pdf(x-center,a.b)*A(x),breaks)
        Fp=integrate_real(lambda x:sgn*float(np.sign(x-center))*lap_pdf(x-center,a.b)*A(x)/a.b,breaks)
        return s*(F-a.k),F+s*Fp-a.k
    return vals,xs,pp,maxmu

records=[]
for r in [1.4,1.5,1.55,1.6,1.625,1.65,1.675,1.69,1.7]:
    # Search boundary q_H=1 and q_L=-v. This is not a search over all pairs.
    grid=np.linspace(.001,1.,121); ys=[]
    for v in grid:
        fun,xs,_,_=candidate(r,1.,float(v))
        ys.append(fun(float(v),-1)[1])
    roots=[]
    for j in range(len(grid)-1):
        if ys[j]*ys[j+1]>=0:continue
        rt=brentq(lambda v:candidate(r,1.,float(v))[0](v,-1)[1],float(grid[j]),float(grid[j+1]),xtol=1e-11)
        if any(abs(rt-x)<1e-7 for x in roots):continue
        roots.append(rt)
    for v in roots:
        fn,xs,pp,maxmu=candidate(r,1.,v)
        if not math.isfinite(xs):continue
        # Exclude false roots caused by the entry/no-entry discontinuity.
        foc=fn(v,-1)[1]
        if abs(foc)>1e-7:continue
        result=dict(r=r,qH=1.,qL=-v,entry=.25+.75*.5*(lap_surv(xs-1.,2.)+lap_surv(xs+v,2.)),
                    xs=xs,pooling_equilibrium=.25*pp['Delta']/2<=.02)
        for state,sgn,qmag in [('H',1,1.),('L',-1,v)]:
            mesh=np.linspace(0,1,401)
            us=np.array([fn(float(s),sgn)[0] for s in mesh]); best=int(np.argmax(us))
            low=mesh[max(0,best-1)];hi=mesh[min(400,best+1)]
            opt=minimize_scalar(lambda s:-fn(float(s),sgn)[0],bounds=(low,hi),method='bounded',options={'xatol':1e-12})
            bestvalue=max(float(us[best]),-float(opt.fun))
            result[state]=dict(candidate_payoff=fn(qmag,sgn)[0],local_foc=fn(qmag,sgn)[1],
               grid_and_local_deviation_gain=bestvalue-fn(qmag,sgn)[0],best_grid_order=float(mesh[best]),best_refined_order=float(opt.x))
        records.append(result)
        print(json.dumps(result))
(OUT/'asymmetric_candidates.json').write_text(json.dumps(records,indent=2))
