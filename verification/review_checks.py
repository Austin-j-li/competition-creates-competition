#!/usr/bin/env python3
"""Independent checks for the CCC critique response.

No optimization of sale rules or first-price auction equilibrium is claimed.
All integrals cover the real line, split at payoff and density breakpoints.
Finite-mesh deviations are diagnostics. Reported sufficient inequalities are
analytic global certificates only insofar as their primitive evaluations have
strict margins; scipy error estimates are not interval-arithmetic enclosures.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from dataclasses import dataclass, asdict, replace
from pathlib import Path
from typing import Callable
import warnings
import numpy as np
import scipy
from scipy.integrate import quad, IntegrationWarning
from scipy.optimize import brentq
from scipy.special import expit

warnings.filterwarnings('error', category=IntegrationWarning)

@dataclass(frozen=True)
class Params:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    rho: float = 0.25
    cL: float = 1.0
    cH: float = 6.0
    b: float = 2.0
    k: float = 0.02

BASE=Params()
QUAD_MAX_ERROR=0.0

def integrate_real(fun: Callable[[float],float], breaks: list[float]) -> float:
    global QUAD_MAX_ERROR
    cuts=[-np.inf]+sorted(set(float(x) for x in breaks if math.isfinite(x)))+[np.inf]
    total=0.0; error=0.0
    for lo,hi in zip(cuts[:-1],cuts[1:]):
        value,err=quad(fun,lo,hi,epsabs=2e-12,epsrel=2e-12,limit=180)
        total+=value; error+=err
    QUAD_MAX_ERROR=max(QUAD_MAX_ERROR,error)
    return total

def prims(r: float, a: Params=BASE, halfwidth: float=0.0) -> dict[str,float]:
    """Conditional value classes, each uniform +/-halfwidth around ell or h.
    For halfwidth=0 these are the original binary fundamental values.
    Only supported reserve regions are used, with an explicit error otherwise.
    """
    p,ell,h=a.p,a.ell,a.h
    if not (0<=p<r<h-halfwidth):
        raise ValueError('This routine only handles 0<=p<r<h-halfwidth.')
    t0=p*(1-p/r)
    tH=r/2+p*p/(2*r)
    if p<ell-halfwidth and ell+halfwidth<r:
        second=ell*ell+halfwidth*halfwidth/3
        tL=ell-(second-p*p)/(2*r)
        gL=(second-p*p)/(2*r)
    elif ell+halfwidth<p:
        tL=t0; gL=0.
    else:
        raise ValueError('Reserve crosses a value band; use direct integration.')
    return dict(t0=t0,tH=tH,tL=tL,gH=h-tH,gL=gL,Delta=tH-tL)

def B(v: dict[str,float],mu:float) -> float:
    return v['gL']+mu*(v['gH']-v['gL'])

def lap_pdf(z:float,b:float)->float:
    return math.exp(-abs(z)/b)/(2*b)

def lap_surv(z:float,b:float)->float:
    return 0.5*math.exp(-z/b) if z>=0 else 1-0.5*math.exp(z/b)

def post(x:float,b:float)->float:
    return float(expit((abs(x+1)-abs(x-1))/b))

def signal_threshold(tau:float,b:float)->float:
    m=float(expit(-2/b)); M=1-m
    if tau <= m: return -math.inf
    if tau > M: return math.inf
    if tau == M: return 1.0 # entry on ties; only for this diagnostic convention
    return b/2*math.log(tau/(1-tau))

def margins(r0:float,r1:float,a:Params,halfwidth:float=0.)->dict[str,float]:
    v0=prims(r0,a,halfwidth);v1=prims(r1,a,halfwidth)
    m=float(expit(-2/a.b))
    return dict(low_cost=B(v1,m)-a.cL,high_cost_prior=a.cH-B(v0,.5),
                high_cost_ceiling=B(v1,1-m)-a.cH,
                weak_no_trade=a.k-v0['Delta'],
                strong_full_trade=(1-1/a.b)*a.rho*m*v1['Delta']-a.k)

def full_candidate(r:float,a:Params=BASE,halfwidth:float=0.)->dict:
    v=prims(r,a,halfwidth);m=float(expit(-2/a.b))
    if a.cL>=B(v,m):
        raise ValueError('Low-cost participation floor is not satisfied.')
    tau=(a.cH-v['gL'])/(v['gH']-v['gL'])
    xs=signal_threshold(tau,a.b)
    alphaH=lap_surv(xs-1,a.b)
    alphaL=lap_surv(xs+1,a.b)
    entry=a.rho+(1-a.rho)*(alphaH+alphaL)/2
    eH=a.rho+(1-a.rho)*alphaH;eL=a.rho+(1-a.rho)*alphaL
    proceeds=v['t0']+.5*(eH*(v['tH']-v['t0'])+eL*(v['tL']-v['t0']))
    def ent(x): return a.rho+(1-a.rho)*(x>=xs)
    def ah(x): return ent(x)*v['Delta']*(1-post(x,a.b))
    def al(x): return ent(x)*v['Delta']*post(x,a.b)
    return dict(v=v,tau=tau,xs=xs,alphaH=alphaH,alphaL=alphaL,
                entry=entry,proceeds=proceeds,AH=ah,AL=al)

def deviation_objects(s:float,sign:int,A:Callable[[float],float],b:float,k:float,
                      extra_breaks:list[float])->tuple[float,float,float]:
    center=sign*s
    cuts=[-1.,1.,center]+extra_breaks
    F=integrate_real(lambda x:lap_pdf(x-center,b)*A(x),cuts)
    # d/ds f(x-sign*s) = sign*sign(x-sign*s)*f/b a.e.
    Fp=integrate_real(lambda x:sign*float(np.sign(x-center))*lap_pdf(x-center,b)*A(x)/b,cuts)
    return s*(F-k), F+s*Fp-k,F

def candidate_diagnostics(r:float,a:Params,n:int=101,halfwidth:float=0.)->tuple[dict,list[dict]]:
    c=full_candidate(r,a,halfwidth); rows=[];summ={}
    for label,A,sgn in [('H',c['AH'],1),('L',c['AL'],-1)]:
        for s in np.linspace(0,1,n):
            u,up,fval=deviation_objects(float(s),sgn,A,a.b,a.k,[c['xs']])
            rows.append(dict(state=label,s=float(s),U=u,Uprime=up,F=fval))
        rs=rows[-n:];maxU=max(t['U'] for t in rs);u1=rs[-1]['U'];J=rs[-1]['F']
        # This lower bound covers gaps in the derivative mesh analytically,
        # apart from quadrature numerical evaluation uncertainty.
        L2=2*c['v']['Delta']/a.b+c['v']['Delta']/a.b**2
        derivative_cover=min(t['Uprime'] for t in rs)-L2/(2*(n-1))
        summ[label]=dict(U1=u1,max_grid_deviation_gain=maxU-u1,
            min_grid_derivative=min(t['Uprime'] for t in rs),
            derivative_Lipschitz_cover_lower=derivative_cover,
            endpoint_convolution=J,
            endpoint_sufficient_margin=(1-1/a.b)*J-a.k,
            best_grid_s=max(rs,key=lambda t:t['U'])['s'])
    visible={k:(v if not isinstance(v,float) or math.isfinite(v) else ('+infinity' if v>0 else '-infinity')) for k,v in c.items() if not callable(v)}
    visible['diagnostics']=summ
    return visible,rows

def no_trade_revenue(r:float,a:Params,halfwidth:float=0.)->float:
    v=prims(r,a,halfwidth)
    prior_entry=a.rho*(B(v,.5)>=a.cL)+(1-a.rho)*(B(v,.5)>=a.cH)
    return v['t0']+.5*prior_entry*(v['tH']+v['tL']-2*v['t0'])

def two_signal(r0:float=1.1,r1:float=2.3,a:Params=replace(BASE,rho=.85,k=.015,cH=7.14),
               accuracy_trader:float=.70,accuracy_buyer:float=.75,n:int=201)->tuple[dict,list[dict]]:
    at,db=accuracy_trader,accuracy_buyer
    lam_lo=float(expit(-2/a.b));lam_hi=1-lam_lo
    mu_lo=1-at+(2*at-1)*lam_lo
    mu_hi=1-at+(2*at-1)*lam_hi
    def buyer_update(mu,y):
        if y==1: return db*mu/(db*mu+(1-db)*(1-mu))
        return (1-db)*mu/((1-db)*mu+db*(1-mu))
    v0=prims(r0,a);v1=prims(r1,a)
    upper0=(2*at-1)*(v0['Delta']+(1-a.rho)*(2*db-1)*(v0['tH']-v0['t0']))
    lower1=(1-1/a.b)*lam_lo*(2*at-1)*a.rho*v1['Delta']
    conds=dict(weak_global_no_trade=a.k-upper0,strong_global_full_trade=lower1-a.k,
        low_cost_floor=B(v1,buyer_update(mu_lo,-1))-a.cL,
        high_cost_excluded_without_price=a.cH-B(v0,db),
        high_cost_positive_good_price_good_private=B(v1,buyer_update(mu_hi,1))-a.cH)
    if min(conds.values())<=0: raise ValueError(f'Two-signal theorem conditions fail: {conds}')
    tau=(a.cH-v1['gL'])/(v1['gH']-v1['gL'])
    mu_req=tau*(1-db)/(db*(1-tau)+tau*(1-db))
    lam_req=(mu_req-(1-at))/(2*at-1)
    xs=signal_threshold(lam_req,a.b)
    if B(v1,buyer_update(mu_hi,-1))>=a.cH:
        raise ValueError('Code special case requires bad private signal never triggers high-cost entry.')
    def pub_mu(x):return 1-at+(2*at-1)*post(x,a.b)
    def decisions(x):
        mu=pub_mu(x)
        ip=float(B(v1,buyer_update(mu,1))>=a.cH)
        im=float(B(v1,buyer_update(mu,-1))>=a.cH)
        return ip,im
    def conditional_entry(x):
        ip,im=decisions(x)
        eh=a.rho+(1-a.rho)*(db*ip+(1-db)*im)
        el=a.rho+(1-a.rho)*((1-db)*ip+db*im)
        return eh,el
    def vals(x):
        eh,el=conditional_entry(x)
        vh=v1['t0']+eh*(v1['tH']-v1['t0'])
        vl=v1['t0']+el*(v1['tL']-v1['t0'])
        price=pub_mu(x)*vh+(1-pub_mu(x))*vl
        traderplus=at*vh+(1-at)*vl
        traderminus=(1-at)*vh+at*vl
        return vh,vl,price,traderplus,traderminus
    def Aplus(x):
        eh,el=conditional_entry(x)
        D=eh*(v1['tH']-v1['t0'])-el*(v1['tL']-v1['t0'])
        return (1-post(x,a.b))*(2*at-1)*D
    def Aminus(x):
        eh,el=conditional_entry(x)
        D=eh*(v1['tH']-v1['t0'])-el*(v1['tL']-v1['t0'])
        return post(x,a.b)*(2*at-1)*D
    alphap=lap_surv(xs-1,a.b);alpham=lap_surv(xs+1,a.b)
    probXH=at*alphap+(1-at)*alpham
    probXL=(1-at)*alphap+at*alpham
    eH=a.rho+(1-a.rho)*db*probXH
    eL=a.rho+(1-a.rho)*(1-db)*probXL
    entry=.5*(eH+eL)
    def fH(x):return at*lap_pdf(x-1,a.b)+(1-at)*lap_pdf(x+1,a.b)
    def fL(x):return (1-at)*lap_pdf(x-1,a.b)+at*lap_pdf(x+1,a.b)
    entry_int=integrate_real(lambda x:.5*(fH(x)*conditional_entry(x)[0]+fL(x)*conditional_entry(x)[1]),[-1,1,xs])
    meanP=integrate_real(lambda x:.5*(lap_pdf(x-1,a.b)+lap_pdf(x+1,a.b))*vals(x)[2],[-1,1,xs])
    meanV=v1['t0']+.5*(eH*(v1['tH']-v1['t0'])+eL*(v1['tL']-v1['t0']))
    errors=[]
    for x in list(np.linspace(-15,15,601))+[xs-1e-5,xs+1e-5]:
        vh,vl,pr,tplus,tminus=vals(float(x))
        errors += [abs(tplus-pr-Aplus(x)),abs(pr-tminus-Aminus(x))]
    rows=[]; diag={}
    for label,A,sgn in [('T+',Aplus,1),('T-',Aminus,-1)]:
        for s in np.linspace(0,1,n):
            u,up,F=deviation_objects(float(s),sgn,A,a.b,a.k,[xs])
            rows.append(dict(state=label,s=float(s),U=u,Uprime=up,F=F))
        rs=rows[-n:]
        diag[label]=dict(U1=rs[-1]['U'],max_grid_deviation_gain=max(t['U'] for t in rs)-rs[-1]['U'],min_grid_derivative=min(t['Uprime'] for t in rs))
    result=dict(parameters=asdict(a),r0=r0,r1=r1,trader_accuracy=at,buyer_accuracy=db,
        primitive_margins=conds,weak_residual_upper=upper0,strong_derivative_before_cost=lower1,
        public_posterior_range=[mu_lo,mu_hi],fundamental_threshold=tau,
        required_public_posterior=mu_req,required_trader_signal_posterior=lam_req,
        order_flow_threshold=xs,entry_weak=a.rho,entry_strong=entry,
        high_fundamental_acquisition_weak=a.rho/2,high_fundamental_acquisition_strong=eH/2,
        entry_integral_check=entry_int,mean_price=meanP,mean_terminal_payoff=meanV,
        max_residual_identity_error=max(errors),diagnostics=diag)
    assert abs(entry-entry_int)<1e-9 and abs(meanP-meanV)<1e-9 and max(errors)<1e-10
    return result,rows

def run(out:Path,mode:str)->None:
    out.mkdir(parents=True,exist_ok=True)
    m=float(expit(-2/BASE.b));M=1-m
    def r_of_d(d):return BASE.ell+d+math.sqrt(d*d+2*BASE.ell*d)
    if mode in ('core','all'):
        rN=r_of_d(2*BASE.k/BASE.rho)
        rU=r_of_d(BASE.k/((1-1/BASE.b)*BASE.rho*m))
        d0=M*BASE.h-BASE.cH
        rC=(d0+math.sqrt(d0*d0+M*((1-M)*BASE.ell**2-BASE.p**2)))/M
        result={'versions':dict(numpy=np.__version__,scipy=scipy.__version__),
                'base':asdict(BASE),'thresholds':dict(no_trade_uniform_sufficient=r_of_d(BASE.k),
                    no_trade_exact_existence=rN,full_trade_uniform_sufficient=rU,
                    high_cost_ceiling_cutoff=rC,
                    laplace_entry_left_limit_at_ceiling=BASE.rho+(1-BASE.rho)*(1+math.exp(-2/BASE.b))/4)}
        allrows=[];curve=[]
        for r in [1.2,1.60,1.65,1.675,1.69,1.70,1.72,1.747,1.75,2.,2.85,3.,3.55,3.60,6.]:
            c,rows=candidate_diagnostics(r,BASE,n=101)
            for rr in rows:rr.update(environment='base',r=r)
            allrows.extend(rows)
            v=c['v']; prior=B(v,.5)
            c['pooling_equilibrium']=BASE.cL<prior<BASE.cH and BASE.rho*v['Delta']/2<=BASE.k
            c['global_full_trade_sufficient_margin']=(1-1/BASE.b)*BASE.rho*m*v['Delta']-BASE.k
            curve.append(dict(r=r,**c))
        result['full_candidate_scan']=curve
        mild=replace(BASE,h=2.,cL=.3,cH=.89,k=.002)
        mc,mrows=candidate_diagnostics(1.5,mild,n=201)
        for rr in mrows:rr.update(environment='mild',r=1.5)
        allrows.extend(mrows)
        result['mild']=dict(parameters=asdict(mild),r0=1.05,r1=1.5,
            primitive_margins=margins(1.05,1.5,mild),strong_candidate=mc,
            weak_entry=mild.rho)
        assert min(result['mild']['primitive_margins'].values())>0
        tau=full_candidate(3.,BASE)['tau']
        aa=math.exp(1/BASE.b);w=math.sqrt(tau/(1-tau))
        xlog=BASE.b*math.log((aa*w-1)/(aa-w))
        alphaH=float(expit(-(xlog-1)/BASE.b));alphaL=float(expit(-(xlog+1)/BASE.b))
        result['logistic']=dict(threshold=xlog,noise_sd=BASE.b*math.pi/math.sqrt(3),
            threshold_in_noise_sd=xlog/(BASE.b*math.pi/math.sqrt(3)),
            threshold_in_aggregate_sd=xlog/math.sqrt((BASE.b*math.pi/math.sqrt(3))**2+1),
            entry=BASE.rho+(1-BASE.rho)*(alphaH+alphaL)/2,
            alphaH=alphaH,alphaL=alphaL)
        result['continuous_value_reserve_test']={}
        for r in [1.2,3.]:
            eps=.05
            for p in [.5,1.1]:
                ap=replace(BASE,p=p)
                v=prims(r,ap,halfwidth=eps)
                if v['Delta']<ap.k:
                    regime='unique_no_trade';entry=ap.rho
                    revenue=no_trade_revenue(r,ap,eps)
                    cert=ap.k-v['Delta']
                else:
                    cc=full_candidate(r,ap,eps)
                    cert=(1-1/ap.b)*ap.rho*m*v['Delta']-ap.k
                    assert cert>0 and B(v,m)>ap.cL
                    regime='unique_full_trade';entry=cc['entry'];revenue=cc['proceeds']
                result['continuous_value_reserve_test'][f'r={r},p={p}']=dict(r=r,p=p,halfwidth=eps,
                    primitives=v,regime=regime,entry=entry,revenue=revenue,strict_trading_margin=cert)
        result['quadrature_max_error_estimate']=QUAD_MAX_ERROR
        (out/'core_results.json').write_text(json.dumps(result,indent=2,allow_nan=False))
        with (out/'deviations.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['environment','r','state','s','U','Uprime','F'])
            writer.writeheader();writer.writerows(allrows)
        print(json.dumps({'thresholds':result['thresholds'],'mild_margins':result['mild']['primitive_margins'],
          'mild_entry':mc['entry'],'logistic':result['logistic'],'continuous_value':result['continuous_value_reserve_test'],
          'quadrature_max_error_estimate':QUAD_MAX_ERROR},indent=2))
    if mode in ('signals','all'):
        result,rows=two_signal()
        result['quadrature_max_error_estimate']=QUAD_MAX_ERROR
        (out/'two_signal_results.json').write_text(json.dumps(result,indent=2,allow_nan=False))
        with (out/'two_signal_deviations.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['state','s','U','Uprime','F']);writer.writeheader();writer.writerows(rows)
        print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=Path('results'))
    parser.add_argument('--mode',choices=['all','core','signals'],default='all')
    args=parser.parse_args();run(args.out,args.mode)
