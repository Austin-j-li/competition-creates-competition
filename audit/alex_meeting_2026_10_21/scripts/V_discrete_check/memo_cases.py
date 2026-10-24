"""Print the memo-specific parameter cases through the independent solver."""
from dataclasses import replace,asdict
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from compute import one_config,print_record
from solver import Params,Game,auction,entry

p=Params()
cases=[
 ('off_path_18',replace(p,r=1.8),[.02]),
 ('off_path_19',replace(p,r=1.9),[.02]),
 ('lambda_lower',replace(p,lam=82/141),[.04,.05]),
 ('lambda_upper',replace(p,lam=6/7),[.04,.05]),
 ('presence075',replace(p,lam=.75),[.02]),
 ('coexist_sell',replace(p,r=2,noise=(.4,.4,.2),c_H=7),[.02]),
 ('unimodal_sell',replace(p,r=1.7,noise=(.2,.6,.2)),[.02]),
 ('unimodal_sell_quarter',replace(p,r=1.7,noise=(.25,.5,.25)),[.02]),
 ('challenger_tie_gap',replace(p,r=3,c_L=2.5,c_H=7,noise=(.2,.6,.2)),[.03]),
 ('pool_missing_ceiling',replace(p,r=3,c_L=3,c_H=12),[.02]),
 ('high_rho',replace(p,r=3,rho=.6),[.02]),
 ('investor_tie_gap_sell',replace(p,r=2+np.sqrt(3),c_L=.02,c_H=12,noise=(.1,.2,.7)),[.08]),
 ('symmetric_constant_entry',replace(p,r=3,c_L=.02,c_H=12,noise=(.25,.5,.25)),[.06]),
]
for name,cp,ks in cases:
    v=one_config((cp,ks,80,True,['M1','M2','M3']));v['case']=name;print_record(v)

for cl in (1.,0.):
    cp=replace(p,c_L=cl); sell=Game(cp,'M2'); buy=Game(cp,'M1')
    ss=sell.full_partitions(0.,1.)[0]; sb=buy.full_partitions(1.,0.)[0]
    t0,th,tl,gh,gl=auction(cp)
    se=np.asarray(ss['entry_rates']); be=np.asarray(sb['entry_rates'])
    sale_gross=ss['gross'][1][0]
    sell_gain=(tl-t0)*(sell.sell-sell.zero)@se
    buy_gross=sb['gross'][1][1]
    buy_gain=(tl-t0)*(buy.buy-buy.zero)@be
    print_record({'case':'stake_local_thresholds','c_L':cl,
                  'omega_sale':(.02-sale_gross)/sell_gain,
                  'omega_fake_buy':(.02-buy_gross)/buy_gain,
                  'sale_net_at_omega1':sale_gross-.02+sell_gain})

for r in (1.2,3.,3.6,8.5):
    cp=replace(p,r=r)
    t0=quad(lambda v:cp.p*(v>=cp.p),0,r,points=[cp.p])[0]/r
    th=quad(lambda v:max(cp.p,v),0,r,points=[cp.p])[0]/r
    tl=quad(lambda v:max(cp.p,min(cp.ell,v)),0,r,points=[cp.p,cp.ell])[0]/r
    gh=quad(lambda v:max(cp.h-max(cp.p,v),0),0,r,points=[cp.p])[0]/r
    gl=quad(lambda v:max(cp.ell-max(cp.p,v),0),0,r,points=[cp.p,cp.ell])[0]/r
    print_record({'case':'auction_integrals','r':r,'quadrature':[t0,th,tl,gh,gl],'solver_objects':auction(cp)})

# Fixed experiment and the reference hidden-price trade profit.
for r in (1.2,3.):
    for cl in (1.,0.,.2):
        g=Game(replace(p,r=r,c_L=cl),'M2')
        s=g.full_partitions(0.,1.)[0]
        print_record({'case':'fixed_sell_experiment','r':r,'c_L':cl,'E':s['E'],'O_H':s['O_H']})

# Local derivative need not have the endpoint comparison's sign.
q=replace(p,c_L=.02,c_H=12,noise=(.1,.7,.2));g=Game(q,'M2')
for b in (.999,1.):
    s=g.full_partitions(0.,b)[0]
    print_record({'case':'local_complementarity','b':b,'gross_sell':s['gross'][1][0]})

# Strict no-trade can sit at equality in the lower inequality of S3.
rstar=1+.24+np.sqrt(.24**2+.48)
print_record({'case':'exact_cutoffs','r_trade':rstar,'r_expensive':4+np.sqrt(16-.25),
              'r_passive':1+.16+np.sqrt(.16**2+.32),
              'r_adverse_sell':1+.048+np.sqrt(.048**2+.096),
              'lambda_recruitment':82/141,'lambda_snb':6/7,'lambda_buy_floor':158/179})

for lam in (1.,.5,.7,.8,.9):
    mu=1/(2-lam)
    value=lambda r:auction(replace(p,r=r))[4]+mu*(auction(replace(p,r=r))[3]-auction(replace(p,r=r))[4])-6
    crossing=brentq(value,1.000001,9.999999) if value(1.000001)*value(9.999999)<0 else None
    print_record({'case':'sell_highcost_ceiling','lambda':lam,'mu':mu,'r':crossing})

# Changed tie rules, declared separately from the pinned game.
for name,cp,cost,flow in (
    ('high_cost_mix_variant',replace(p,r=1.7,noise=(.2,.6,.2)),.02,0),
    ('low_cost_mix_variant',replace(p,r=3,c_L=2.5,c_H=7,noise=(.2,.6,.2)),.03,-1)):
    g=Game(cp,'M2'); threshold=((cp.c_H if flow==0 else cp.c_L)-g.gl)/(g.gh-g.gl)
    ix=list(g.flows).index(flow)
    beta=brentq(lambda b:g.point(0,b)[1][ix]-threshold,1e-8,1-1e-8)
    f,mu,off=g.point(0,beta);rates=entry(cp,mu)
    rates[ix]=0.
    rest=float(g.gross_at(0,beta,rates)[1])
    rates[ix]=(cost-rest)/(g.delta*g.sell[ix]*mu[ix])
    probability=(rates[ix]-cp.rho)/(1-cp.rho) if flow==0 else rates[ix]/cp.rho
    print_record({'case':name,'s_L':beta,'entrant_mix':probability,
                  'E':float(.5*f.sum(axis=0)@rates),'O_H':float(.5*f[0]@rates),
                  'pinning':'requires both investor mixing at zero profit and challenger mixing at its cost threshold'})

for noise,ch in (((.25,.5,.25),6.),((.2,.6,.2),6.),((.4,.4,.2),7.)):
    coexist=[]
    for r in np.round(np.arange(1.01,4.1001,.005),6):
        g=Game(replace(p,r=float(r),noise=noise,c_H=ch),'M2')
        nt=any(g.optimal(0,0,.02,s)[1] for s in g.full_partitions(0,0))
        full=any(g.optimal(0,1,.02,s)[1] for s in g.full_partitions(0,1))
        if nt and full:coexist.append(float(r))
    print_record({'case':'sell_coexistence_r_grid','noise':noise,'c_H':ch,'r_first':min(coexist) if coexist else None,
                  'r_last':max(coexist) if coexist else None,'grid_step':.005})
