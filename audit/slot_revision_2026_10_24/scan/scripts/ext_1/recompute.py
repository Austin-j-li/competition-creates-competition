"""Read-only numerical use of manuscript formulas; print values, without assertions."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import csv
import re
from itertools import product
from mpmath import mp, iv

ROOT = Path('/Users/austinli/Projects/competition-creates-competition')
OUT = Path('scripts/ext_1')
mp.dps = 85
iv.dps = 85

def I(x):
    if hasattr(x, '_mpi_'):
        return x
    f = F(str(x))
    return iv.mpf(f.numerator) / f.denominator

def lower(x):
    return mp.mpf(I(x)._mpi_[0])

def upper(x):
    return mp.mpf(I(x)._mpi_[1])

def least(xs):
    xs = [I(x) for x in xs]
    return iv.mpf([min(lower(x) for x in xs), min(upper(x) for x in xs)])

def greatest(xs):
    return -least([-I(x) for x in xs])

def sign(x):
    if lower(x) > 0:
        return 1
    if upper(x) < 0:
        return -1
    return 0

values = {}
def put(k, v):
    values[k] = I(v)
    return I(v)

# Rational Taylor bounds, followed by outward interval operations.
partial = sum((F(1, factorial(i)) for i in range(101)), F(0))
E = iv.mpf([lower(I(partial)), upper(I(partial + F(1, 100*factorial(100))))])
beta, rho, fee, capcost = map(I, ('0.294655', '1/4', '1/50', '1/40'))
u = E-1
lam = u*beta/(1+u*beta)
b, b0 = (1-lam)*beta, (1-lam)*(1-2*beta)
m, M = 1/(1+E), E/(1+E)
volume, theta = 2*b+lam, lam/(2*b+lam)
for k,v in dict(beta_B=beta, entry_r0=rho, prim_h=10, prim_ell=1, prim_p='1/2',
                prim_rho=rho, prim_pi='1/2', res_a=capcost, res_cap=lam,
                atom_L='1/5', atom_eps='1/10', atom_eps_small='1/1000',
                four_prior='1/4',four_v1=1,four_v2='1001/1000',four_v3='9999/1000',four_v4=10,
                access_out_cH='12/5',rsv_points_excl='101/100',rsv_bands_excl='11/10',rsv_deter='31/20',
                sig_aT='7/10',sig_d='3/4',sig_rho='17/20',sig_cH='357/50',sig_k='3/200',
                sig_r0='11/10',sig_r1='23/10',sig_comp_aT='47/50',sig_comp_d='101/200',
                str_r155='31/20',str_r160='8/5',str_r165='33/20').items(): put(k,v)

def point(v,p,r):
    v,p,r = map(F,(v,p,r))
    s0 = (r*r-p*p)/(2*r) if r>p else F(0)
    t0 = p*(1-p/r) if r>p else F(0)
    if v<p: return (t0,F(0),F(0),s0,F(0))
    if r<=p: return (p,v-p,F(1),v,F(1))
    if v<=r: return (v-(v*v-p*p)/(2*r),(v*v-p*p)/(2*r),v/r,(r*r+v*v)/(2*r),F(1))
    return ((r*r+p*p)/(2*r),v-(r*r+p*p)/(2*r),F(1),v,F(1))

def average(law,p,r):
    low,high = map(F,law)
    p,r = F(p),F(r)
    if low==high: return point(low,p,r)
    cuts=sorted({low,high}|{x for x in (p,r) if low<x<high})
    result=[F(0)]*5
    # The kernels are quadratic on each piece. Exact polynomial integration
    # uses the midpoint rule plus its exact quadratic correction.
    for a,z in zip(cuts,cuts[1:]):
        mid=(a+z)/2
        quarter=(3*a+z)/4
        threequarter=(a+3*z)/4
        # Interior samples avoid the jump at the reserve.
        aa,bb,cc=point(quarter,p,r),point(mid,p,r),point(threequarter,p,r)
        for j in range(5):
            curvature=4*(aa[j]+cc[j]-2*bb[j])/((z-a)/2)**2
            result[j]+=(z-a)*bb[j]+curvature*(z-a)**3/24
    return tuple(x/(high-low) for x in result)

def auction(r,p=F(1,2),high=(10,10),low=(1,1)):
    r,p=F(r),F(p)
    h,l=average(high,p,r),average(low,p,r)
    fp=min(p/r,F(1))
    return dict(h=h,l=l,fp=fp,t0=p*(1-fp),s0=(r*r-p*p)/(2*r) if r>p else F(0),D=h[0]-l[0])

def B(r,z,p=F(1,2),high=(10,10),low=(1,1)):
    a=auction(r,p,high,low)
    return I(a['l'][1])+z*I(a['h'][1]-a['l'][1])

def tau(r):
    a=auction(r)
    return (F(6)-a['l'][1])/(a['h'][1]-a['l'][1])

def D(r): return auction(r)['D']
def fr(d):
    d=I(d)
    return 1+d+iv.sqrt(d*d+2*d)
def le(r,bb=beta):
    t=I(tau(r))
    return bb*(2*t-1)/(bb+(1-2*bb)*(1-t))
def residual(z,bb=beta): return (1-z)*bb/(2*bb+z*(1-2*bb))
def research(r,bb=beta):
    aa=2*capcost*(1-2*bb)
    cc=bb*(2*fee-I(D(r)))
    dd=4*capcost*bb+fee*(1-2*bb)+bb*I(D(r))
    return -2*cc/(dd+iv.sqrt(dd*dd-4*aa*cc))
def bisect_rational(fn,lo,hi):
    lo,hi=F(lo),F(hi)
    for j in range(210):
        mid=(lo+hi)/2
        if fn(mid)<0: lo=mid
        else: hi=mid
    return lo,hi

for tag,r in [('r155',F(31,20)),('r160',F(8,5)),('r165',F(33,20))]:
    z=research(r)
    es=(2*capcost*le(r)+fee)/(I(D(r))*(1-I(tau(r))))
    data=dict(Delta=D(r),tau=tau(r),lamE=le(r),**{'lambda':z},muplus=1-residual(z),
              entry=rho+(1-rho)*(beta+(I('1/2')-beta)*z),
              own=(rho+(1-rho)*(beta+(1-beta)*z))/2,
              ULgap=fee-rho*I(D(r))/2,lamgap=z-le(r),capgap=lam-z,
              th_estar=es,th_entry=rho+(es-rho)*(beta+(I('1/2')-beta)*le(r)))
    for k,v in data.items(): put('res_'+k+'_'+tag,v)

bb=F(294655,1000000)
phi=lambda r: D(r)*(1-tau(r))-F(1,50)-F(1,20)*(bb*(2*tau(r)-1)/(bb+(1-2*bb)*(1-tau(r))))
rlo,rhi=bisect_rational(phi,'6/5','7/4')
rR=iv.mpf([lower(I(rlo)),upper(I(rhi))])
lR=iv.mpf([lower(le(rlo)),upper(le(rhi))])
rN=fr(2*fee/rho)
rCap=fr((2*capcost*lam+fee)*(1+E))
rU=fr((fee+capcost*lam)*(1+E)/rho)
rS=fr(fee/(rho*m))
# B_r(M)=6 after multiplication by r is a quadratic.
tcoef=10*M-6
rC=(tcoef+iv.sqrt(tcoef*tcoef+M*((1-M)-I('1/4'))))/M
aRlo,aRhi=bisect_rational(lambda r: D(r)*(1-tau(r))-F(1,50),'6/5','7/4')
for k,v in dict(res_Delta_r0=D('6/5'),res_rR=rR,res_lambda_rR=lR,
                res_entry_rR=rho+(1-rho)*(beta+(I('1/2')-beta)*lR),
                res_rcap=rCap,res_rUR=rU,res_rN=rN,res_rC=rC,
                res_rA=iv.mpf([lower(I(aRlo)),upper(I(aRhi))]),
                res_entry_cap=rho+(1-rho)*volume/2,res_entry_r1=rho+(1-rho)*volume/2,
                res_entry_r2=rho,res_lamE_r175=le(F(7,4)),
                margin_res_rN_B=rN-rCap,margin_res_weak_B=fee-I(D('6/5')),
                margin_res_half_B=6-B('6/5',I('1/2'))).items(): put(k,v)
end=F(7,4)
tp=F(3)*(8*end**2-end+2)/(2*(20*F(6,5)-F(6,5)**2-1)**2)
dD=F(11,72)
q=1-tau(end)
lead=dD*q-D(end)*tp
den=bb+(1-2*bb)*q
amono=I(lead)/(2*I(bb*tp/den**2))
amono3=I(lead)/(2*I(F(1,3)*tp/(F(1,3)+F(1,3)*q)**2))
alo=(I(D('33/20'))*m-fee)/(2*lam)
aup=(I(D('31/20'))*(1-I(tau('31/20')))-fee)/(2*le(F(31,20)))
caplo,caphi=le(F(3)),le(F(18,5))
target=(I(D('33/20'))*m-fee)/(2*capcost)
targetup=(I(D('31/20'))*(1-I(tau('31/20')))-fee)/(2*capcost)
for k,v in dict(res_bound_dDelta=dD,res_bound_tau74=q,res_bound_Delta74=D(end),res_bound_taup=tp,
                res_dphi_lead=lead,res_phip_lb=I(lead)-2*capcost*I(bb*tp/den**2),
                res_amono=amono,res_amono_third=amono3,res_a_lo=alo,res_a_up=aup,
                res_cap_lo=caplo,res_cap_hi=caphi,res_cap_lo_a=research(F(33,20)),
                res_region_aU3_6=(rho*I(D(3))*residual(caphi)-fee)/caphi,
                res_region_a36_6=(rho*I(D('18/5'))*residual(caphi)-fee)/caphi,
                res_region_alo_0=(I(D('33/20'))*residual(caplo)-fee)/(2*caplo),
                res_beta_lo=target/(1-target)/u,
                res_beta_hi=targetup*(1-I(tau('31/20')))/((2*I(tau('31/20'))-1)*(1-targetup)),
                margin_res_alo_B=capcost-alo,margin_res_aup_B=aup-capcost,
                margin_res_caplo_B=lam-caplo,margin_res_caphi_B=caphi-lam,
                margin_res_tau_r1_B=M-I(tau(3)),margin_res_tau_r2_B=I(tau('18/5'))-M,
                margin_res_bound_r1_B=rho*I(D(3))*m-fee-capcost*lam,
                margin_res_bound_r2_B=rho*I(D('18/5'))*m-fee-capcost*lam).items(): put(k,v)

def economy_node(stem,r,high=(10,10),low=(1,1),pi=F(1,2),p=F(1,2),cost=F(6),k=F(1,50),
                 orders=(1,-1),pattern=(0,0,1),hidden=False):
    a=auction(r,p,high,low)
    pi=I(pi)
    hh=[b+(lam if orders[0]==-1 else 0),b0+(lam if orders[0]==0 else 0),b+(lam if orders[0]==1 else 0)]
    ll=[b+(lam if orders[1]==-1 else 0),b0+(lam if orders[1]==0 else 0),b+(lam if orders[1]==1 else 0)]
    mass=[pi*h+(1-pi)*l for h,l in zip(hh,ll)]
    post=[pi*h/f for h,f in zip(hh,mass)]
    ee=[rho+(1-rho)*v for v in pattern]
    eh=sum(x*y for x,y in zip(hh,ee)); el=sum(x*y for x,y in zip(ll,ee))
    adm=pi*eh*I(a['h'][4])+(1-pi)*el*I(a['l'][4])
    out=dict(entry=pi*eh+(1-pi)*el,ownership=pi*eh*I(a['h'][2]),
             proceeds=I(a['t0'])+pi*eh*I(a['h'][0]-a['t0'])+(1-pi)*el*I(a['l'][0]-a['t0']),
             surplus=I(a['s0'])+pi*eh*I(a['h'][3]-a['s0'])+(1-pi)*el*I(a['l'][3]-a['s0'])
             -(1-rho)*I(cost)*sum(x*y for x,y in zip(mass,pattern)),
             sale=1-I(a['fp'])+I(a['fp'])*adm,two=(1-I(a['fp']))*adm,
             prior_cost_margin=I(cost)-(I(a['l'][1])+pi*I(a['h'][1]-a['l'][1])))
    for suffix,z in zip(('minus','zero','plus'),post):
        zz=pi if hidden else z
        out['cost_sign_'+suffix]=I(a['l'][1])+zz*I(a['h'][1]-a['l'][1])-I(cost)
    for k2,v in out.items(): put(stem+'_'+k2,v)
    return out

specs=[('base',(10,10),(1,1),'1/2',6,'1/50',['6/5',3,'18/5']),
       ('moderate',(2,2),(1,1),'1/2','89/100','1/500',['21/20','3/2']),
       ('bands',('199/20','201/20'),('19/20','21/20'),'1/2',6,'1/50',['6/5',3,'18/5']),
       ('ex_a',(10,10),(1,1),'3/10','9/2','1/100',['11/10',3,'18/5']),
       ('ex_b',(10,10),(1,1),'7/10','36/5','1/100',['11/10',3,'18/5']),
       ('ex_c',(1,19),('3/5','7/5'),'7/10','67/10','1/50',[1,'9/2','11/2']),
       ('ex_d',(10,10),(1,1),'7/10','67/10','1/50',[1,'9/2','11/2'])]
nodes={}
for name,h,l,pi,c,k,rr in specs:
    h,l=tuple(map(F,h)),tuple(map(F,l))
    pi,c,k=map(F,(pi,c,k))
    for n,v in dict(high_lo=h[0],high_hi=h[1],low_lo=l[0],low_hi=l[1],pi=pi,cost=c,k=k).items():put('p2_input_'+name+'_'+n,v)
    for j,r in enumerate(rr):
        put('p2_input_'+name+'_r'+str(j),r)
        nodes[name,j]=economy_node('p2_'+name+'_r'+str(j),r,h,l,pi,cost=c,k=k,
                                  orders=(0,0) if j==0 else (1,-1),
                                  pattern=(0,0,1) if j==1 and name!='ex_d' else (0,0,0))
put('margin_p2_ex_d_strong_top_B',nodes['ex_d',1]['cost_sign_plus'])
for pi,n in [('3/10','three_tenths'),('7/10','seven_tenths')]:
    for j,r in enumerate(['6/5',3]):
        economy_node('p2_fixed_prior_'+n+'_r'+str(j),r,pi=F(pi),orders=(0,0) if j==0 else (1,-1),
                     pattern=(0,0,0) if pi=='3/10' else ((1,1,1) if j==0 else (0,0,1)))
hidden=economy_node('p2_base_hidden',3,pattern=(0,0,0),hidden=True)
dr=nodes['base',1]['proceeds']-hidden['proceeds']
dw=nodes['base',1]['surplus']-hidden['surplus']
gross=lam*I(D(3))*(1+rho)*m/2
for k,v in dict(p2_access_proceeds_gain=dr,p2_access_surplus_gain=dw,p2_access_gross_transfer=gross,
                p2_access_break_even=dr/gross,res_dR_r1=dr,res_dW_r1=dw,pay_gap_coef=F(13,20)).items():put(k,v)
seen=economy_node('p2_outside_seen',3,cost=F(12,5),pattern=(0,1,1))
hid=economy_node('p2_outside_hidden',3,cost=F(12,5),pattern=(1,1,1),hidden=True)
for k in ('proceeds','surplus'):put('p2_outside_'+k+'_gain',seen[k]-hid[k])

reserve_nodes={}
for name,h,l,excl in [('points',(10,10),(1,1),'101/100'),('bands',('199/20','201/20'),('19/20','21/20'),'11/10')]:
    h,l=tuple(map(F,h)),tuple(map(F,l))
    for tag,p in [('base','1/2'),('exclude',excl),('deter','31/20')]:
        for j,r in enumerate(['6/5',3]):
            stem='p2_reserve_'+name+'_'+tag+'_r'+str(j)
            full=not(tag=='base' and j==0)
            nn=economy_node(stem,r,h,l,p=F(p),orders=(1,-1) if full else (0,0),
                            pattern=(0,0,1) if full and not(tag=='deter' and j==1) else (0,0,0))
            reserve_nodes[name,tag,j]=nn
            put(stem+'_global',rho*m*I(auction(r,F(p),h,l)['D'])-fee if full else fee-I(auction(r,F(p),h,l)['D']))
    for j in (0,1):
        for tag,typ in [('exclude','exclude_gain'),('deter','rev')]:
            put('margin_p2_reserve_'+name+'_'+typ+str(j)+'_B',reserve_nodes[name,tag,j]['proceeds']-reserve_nodes[name,'base',j]['proceeds'])
ph=iv.sqrt(6*(10-6/M)-9)
for k,v in dict(p2_reserve_ph=ph,p2_reserve_weak_top=10-6/M,margin_p2_ph_weak_B=ph-I('6/5'),
                margin_p2_deter_lower_B=I('31/20')-ph,margin_p2_deter_upper_B=10-6/M-I('31/20'),
                margin_p2_reserve_admissible_top_B=M*I('413/50')-6,
                margin_p2_reserve_uniform_weak_B=rho*m*I('17/20')-fee,
                margin_p2_reserve_uniform_strong_B=rho*m-fee,
                margin_p2_ph_trade_B=rho*m*(I('3/2')-ph+ph*ph/2)-fee).items():put(k,v)
economy_node('p2_endpoint_r1',3,p=F(10),pattern=(0,0,0))

# Class vector calculations use each joint order probability directly.
weight=(1+2*b0+lam)/2
means=[]
ts=[I(1),1+I('49/16')*weight,I('65/16')]
for qi,q in enumerate([-1,0,1]):
    joint=[I(pr)*( (b0 if q==0 else b)+(lam if j==qi else 0)) for j,pr in enumerate(['1/4','1/2','1/4'])]
    post=[x/sum(joint) for x in joint]
    mean=sum(x*t for x,t in zip(post,ts));means.append(mean)
    for j,x in enumerate(post):put('p2_many_q'+str(qi)+'_mu'+str(j),x)
    put('p2_many_q'+str(qi)+'_price',I('7/8')+rho*(mean-I('7/8')))
for j,t in enumerate(ts):
    pays=[q*rho*(t-mean)-I('1/8')*abs(q) for q,mean in zip([-1,0,1],means)]
    put('p2_many_choice'+str(j),least([pays[j]-pays[k] for k in range(3) if k!=j]))
put('p2_many_weight',weight)
vs=list(map(F,['1','1001/1000','9999/1000','10']))
aa0=[point(v,F(1,2),F(6,5)) for v in vs]
aa1=[point(v,F(1,2),F(3)) for v in vs]
weighted=[]
for bits in product([0,1],repeat=4):
    ww=[1+u*bit for bit in bits]
    weighted.append(sum(w*I(a[0]) for w,a in zip(ww,aa1))/sum(ww))
gamma=least([I(min(a[0] for a in aa1[2:]))-greatest(weighted),least(weighted)-I(max(a[0] for a in aa1[:2]))])
gl=sum(a[1] for a in aa1[:2])/2;gh=sum(a[1] for a in aa1[2:])/2
for k,v in dict(p2_groups_gamma=gamma,p2_groups_trade=rho*gamma-fee,
                p2_groups_weak_range=fee-I(max(a[0] for a in aa0)-min(a[0] for a in aa0)),
                p2_groups_weak_cost=6-I(sum(a[1] for a in aa0)/4),p2_groups_profit_gap=gh-gl,
                p2_groups_top=I(gl)+M*I(gh-gl)-6).items():put(k,v)

# Atomless costs: the low component always enters at the stated nodes.
put('margin_return_B',6-B('18/5',M))
put('margin_return_post_B',I(tau('18/5'))-M)
for k,v in dict(atomless_floor_B=B(3,m)-I('1/5'),atomless_weak_B=I('59/10')-B('6/5',I('1/2')),
                atomless_strong_B=B(3,M)-I('61/10'),atomless_return_B=I('59/10')-B('18/5',M),
                atomless_top_lower_r2_B=B('18/5',M)-I('59/10'),atomless_top_upper_r2_B=I('61/10')-B('18/5',M),
                atomless_small_width_return=6-B('18/5',M)-I('1/1000')).items():put('margin_p4_'+k,v)
for j,r in [(1,3),(2,'18/5')]:
    qprob=I(1) if j==1 else (B(r,M)-I('59/10'))/I('1/5')
    put('p4_atomless_r'+str(j)+'_entry',rho+(1-rho)*volume*qprob/2)
    put('p4_atomless_r'+str(j)+'_own',(rho+(1-rho)*(b+lam)*qprob)/2)
put('p4_atomless_max_width_floor_r2',6-B('18/5',M))
for k,v in dict(control_crossing_r0_r1=0,control_crossing_r1_r2=(1-rho)*volume/2,
                frozen_entry_below_ceiling=rho+(1-rho)*volume/2,frozen_entry_above_ceiling=rho,hidden_r0_entry=rho).items():put('p4_'+k,v)

def phis(z,d,positive=True):
    weight=d if positive else 1-d
    return weight*z/(weight*z+(1-weight)*(1-z))
def sigmarg(tag,r0,r1,rr,c,k,acc,d):
    rr,c,k,acc,d=map(I,(rr,c,k,acc,d))
    mu=1-acc+(2*acc-1)*M
    wH=I(auction(r0)['h'][0]-auction(r0)['t0'])
    data=dict(private=c-B(r0,d),joint=B(r1,phis(mu,d))-c,
              weak=k-(2*acc-1)*(I(D(r0))+(1-rr)*(2*d-1)*wH),
              strong=(2*acc-1)*rr*m*I(D(r1))-k,other_pair=c-B(r1,phis(mu,d,False)))
    for k2,v in data.items():put('margin_p4_'+tag+'_'+k2,v)
    return data
sigmarg('signal_s','11/10','23/10','17/20','357/50','3/200','7/10','3/4')
sigmarg('signal_comp_b','6/5',3,'1/4',6,'1/50','47/50','101/200')
sigmarg('grid_72_75','11/10','23/10','17/20','357/50','3/200','72/100','75/100')
def signal_profile(stem,r,rr,c,k,s,t,acc,d):
    rr,c,k,acc,d=map(I,(rr,c,k,acc,d))
    laws=[(b,b+t),(b0+lam-s,b0+lam-t),(b+s,b)]
    ehbar,elbar=I(0),I(0)
    mus=[]
    for plus,minus in laws:
        fh=acc*plus+(1-acc)*minus;fl=(1-acc)*plus+acc*minus
        mu=fh/(fh+fl);mus.append(mu)
        ip=1 if sign(B(r,phis(mu,d))-c)>0 else 0
        im=1 if sign(B(r,phis(mu,d,False))-c)>0 else 0
        eh=rr+(1-rr)*(d*ip+(1-d)*im)
        el=rr+(1-rr)*((1-d)*ip+d*im)
        ehbar+=fh*eh;elbar+=fl*el
    put(stem+'_entry',(ehbar+elbar)/2);put(stem+'_own',ehbar/2)
    put(stem+'_buy_rate',s/lam);put(stem+'_sell_rate',t/lam)
    return mus
for name,r0,r1,rr,c,k,acc,d in [('s_signal','11/10','23/10','17/20','357/50','3/200','7/10','3/4'),
                               ('comp_b','6/5',3,'1/4',6,'1/50','47/50','101/200'),
                               ('s_no_y','11/10','23/10','17/20','357/50','3/200','7/10','1/2'),
                               ('s_class','11/10','23/10','17/20','357/50','3/200',1,'1/2'),
                               ('comp_b_no_y','6/5',3,'1/4',6,'1/50','47/50','1/2')]:
    signal_profile('p4_'+name+'_r0',r0,rr,c,k,I(0),I(0),acc,d)
    signal_profile('p4_'+name+'_r1',r1,rr,c,k,lam,lam,acc,d)
signal_profile('p4_b_signal_r0','6/5','1/4',6,'1/50',I('119/96')*b,I('119/96')*b,'7/10','3/4')
mu_actual=signal_profile('p4_b_signal_r1',3,'1/4',6,'1/50',lam,I('4/3')*b,'7/10','3/4')
zmin=fee/(rho*m*I(D(3)))
a,d=I('7/10'),I('3/4')
mulo=1-a+(2*a-1)*m;muhi=1-a+(2*a-1)*M
for k,v in dict(b_weak_all_yplus=B('6/5',phis(mulo,d))-6,
                b_weak_no_yminus=6-B('6/5',phis(muhi,d,False)),
                b_weak_zero_return=I('2/5')*I('311/1920')/2-fee,
                b_weak_full_loss=fee-I('2/5')*m*I('311/1920'),b_weak_rate_room=u-I('119/96'),
                b_strong_buy=I('2/5')*m*I('137/192')-fee,b_strong_no_yminus=6-B(3,phis(muhi,d,False)),
                b_strong_prior_yplus=B(3,d)-6,b_strong_threshold_floor_return=I('19/795')-fee,
                b_strong_rate_room=u-I('4/3'),b_strong_sale_public_gap=I('47/106')-I('21/50'),
                b_strong_zero_yplus=B(3,phis(mu_actual[1],d))-6,
                b_d_ge_a_impossible=zmin*(I(D('6/5'))+(1-rho)*zmin*I(auction('6/5')['h'][0]-auction('6/5')['t0']))-fee).items():put('margin_p4_'+k,v)
put('p4_b_signal_z_min',zmin)
put('p4_b_no_y_r1_zero_gross',rho*I('2/5')*I(D(3))/2)
put('p4_b_no_y_r1_full_gross',rho*I('2/5')*m*I(D(3)))
for name,rr,cc,kk,acc,r0,r1 in [('s_no_y','17/20','357/50','3/200','7/10','11/10','23/10'),
                               ('s_class','17/20','357/50','3/200',1,'11/10','23/10'),
                               ('comp_b_no_y','1/4',6,'1/50','47/50','6/5',3)]:
    rr,cc,kk,acc=map(I,(rr,cc,kk,acc))
    for k,v in dict(weak=kk-(2*acc-1)*I(D(r0)),strong=(2*acc-1)*rr*m*I(D(r1))-kk,
                    top_r0=cc-B(r0,1-acc+(2*acc-1)*M),top_r1=cc-B(r1,1-acc+(2*acc-1)*M),
                    prior_r0=cc-B(r0,I('1/2'))).items():put('margin_p4_'+name+'_'+k,v)

def A(r,z):
    a=auction(r)
    return I(a['l'][0]-a['t0'])+I(a['D'])*z
for tag,r,chi in [('r1',F(3),1),('r2',F(18,5),0)]:
    cls=rho*I(D(r))*theta
    ent=(1-rho)*chi*A(r,M)
    bar=I(auction(r)['t0'])+rho*A(r,I('1/2'))+(1-rho)*chi*volume*A(r,M)/2
    entry=rho+(1-rho)*chi*volume/2
    pp=[volume/2,1-volume,volume/2]
    ee=[rho,rho,rho+(1-rho)*chi]
    mm=[m,I('1/2'),M]
    announcement=sum(f*e*(1-e)*A(r,z) for f,e,z in zip(pp,ee,mm))/entry
    for k,v in {'ba_'+tag+'_B':cls+ent,'wgap_'+tag+'_B':theta*(1-I(1)/I(r)),
                'evprep_mean_'+tag+'_B':announcement}.items():put(k,v)
    if tag=='r1':
        for k,v in dict(ba_class_r1_B=cls,ba_entry_r1_B=ent,ba_share_r1_B=ent/(cls+ent),
                        pbar_r1_B=bar,p_neutral_r1_B=I(auction(r)['t0'])+rho*A(r,I('1/2')),
                        pdrop_neutral_r1_B=-(1-rho)*volume*A(r,M)/2).items():put(k,v)
# Evaluate rational formulas at an interval strength for the ceiling.
DC=(rC-1)**2/(2*rC)
AC=I('1/2')-1/(8*rC)+DC*M
cc=rho*DC*theta
for k,v in dict(ba_rC_left_B=cc+(1-rho)*AC,ba_rC_right_B=cc,ba_jump_rC_B=(1-rho)*AC,
                entry_jump_B=(1-rho)*volume/2,cov_entry_r1_B=(1-rho)*volume/2,
                margin_obs_post_over_58_B=M-I('5/8'),margin_obs_rS_rC_B=rC-rS,
                delta_rS_B=fee/(rho*m),rS_B=rS,rC_B=rC,
                rS_counter_r_B='2.1241481',rS_cert_hi_B='2.124149',
                rS_counter_margin_B=rho*I(D('2.1241481'))*m-fee,
                theta_min_counts_B=3-2/volume,theta_max_full_eq_r1_B=1-2*fee/(rho*I(D(3))),
                theta_max_full_eq_r2_B=1-2*fee/(rho*I(D('18/5'))),
                theta09_beta_B=volume*I('1/10')/(2*(1-volume*I('9/10'))),
                theta09_lowsale_r1_B=rho*I(D(3))*I('1/20')-fee,
                margin_obs_band_incentive_B=rho*I(D(3))*(1-I(tau('18/5')))-fee,
                u_lo_frac=(2*I(tau(3))-1)/(1-I(tau(3))),u_hi_frac=(2*I(tau('18/5'))-1)/(1-I(tau('18/5'))),
                vol_full_B=volume,alt_theta_B=I('4/9'),
                alt_ba_r1_B=rho*I(D(3))*I('4/9')+(1-rho)*A(3,I('13/18')),
                imb_buy_B=lam/2).items():put(k,v)
r=F(8,5)
mu0=b0/(2*b0+lam)
sp=b*(2*I(tau(r))-1)/(1-I(tau(r)))
e=fee/(I(D(r))*(1-I(tau(r))))
for k,v in dict(U_gap_r160_B=rho*I(D(r))*(I('1/2')-mu0),mix_sigma_r160_B=sp/lam,
                mix_e1_r160_B=e,mix_mean_order_r160_B=sp/2,mix_lowsale_r160_B=rho*I(D(r))/2-fee,
                mix_entry_r160_B=rho+(e-rho)*(b+sp/2)).items():put(k,v)

keys=set((OUT/'used_keys.txt').read_text().splitlines())
registry={r['key']:r for r in csv.DictReader((ROOT/'audit/slot_manuscript_2026_10_23/registry/registry.csv').open())}
macros=dict(re.findall(r'\\csname reg@([^\\]+)\\endcsname\{(.*)\}',(ROOT/'slot/manuscript/numbers.tex').read_text()))
rows=[]
missing=[]
bad=[]
for key in sorted(keys):
    reg=registry[key]
    if key not in values:
        missing.append(key)
        continue
    x=values[key]
    s=reg['display'].replace(r'\%', '%')
    pct=s.endswith('%')
    if pct:s=s[:-1]
    match=re.fullmatch(r'\\ensuremath\{(-?[\d.]+)\\times10\^\{(-?\d+)\}\}',s)
    if match:
        mant,ex=match.groups();ex=int(ex)
        target=I(mant)*I(10)**ex
        tol=I(10)**(ex-len(mant.split('.')[-1]))/2
    else:
        try:
            target=I(s)
        except Exception:
            missing.append(key+' [display '+s+']')
            continue
        tol=I(0) if '/' in s or '.' not in s else I(10)**(-len(s.split('.')[1]))/2
    if pct:target/=100;tol/=100
    difference=x-target
    display_ok=lower(difference)>=-upper(tol)-mp.mpf('1e-75') and upper(difference)<=upper(tol)+mp.mpf('1e-75')
    macro_ok=macros.get(key)==reg['display']
    row=dict(key=key,display=reg['display'],lower=mp.nstr(lower(x),45),upper=mp.nstr(upper(x),45),
             display_result='within displayed precision' if display_ok else 'MISMATCH',
             macro_result='same' if macro_ok else 'MISMATCH',sign=sign(x))
    rows.append(row)
    if not display_ok or not macro_ok:bad.append(row)
with (OUT/'recomputed_values.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
print('Used keys:',len(keys),'Recomputed:',len(rows),'Missing:',len(missing),'Display/macro discrepancies:',len(bad))
for x in bad: print(x)
print('MISSING',missing)
print('Exact root bracket r_R:',rlo,rhi)
print('Intervals: r_R',rR,'r_cap',rCap,'r_U',rU,'r_S',rS,'r_C',rC)
print('Signal sale gross at t=4b/3:',I('1/15')*b/(2*b+I('4/3')*b))
print('Signal sale net at t=4b/3:',I('1/15')*b/(2*b+I('4/3')*b)-fee)

# Additional displayed claims outside the registry.
grid=[]
for ai in range(68,73):
    for di in range(73,78):
        acc,dd=I(F(ai,100)),I(F(di,100))
        rr,cc,kk=I('17/20'),I('357/50'),I('3/200')
        mu=1-acc+(2*acc-1)*M
        margins=[cc-B('11/10',dd),B('23/10',phis(mu,dd))-cc,
                 kk-(2*acc-1)*(I(D('11/10'))+(1-rr)*(2*dd-1)*I(auction('11/10')['h'][0]-auction('11/10')['t0'])),
                 (2*acc-1)*rr*m*I(D('23/10'))-kk,
                 cc-B('23/10',phis(mu,dd,False))]
        if all(sign(x)>0 for x in margins[:4]):
            grid.append((ai,di,least(margins)))
print('Signal grid admissible pairs:',[(a,d) for a,d,_ in grid])
print('Signal grid smallest margin:',least([g for _,_,g in grid]))
for step in [-I('1/1000'),I('1/1000')]:
    wt=weight+step
    tjs=[I(1),1+I('49/16')*wt,I('65/16')]
    av=[]
    for qi,q in enumerate([-1,0,1]):
        jj=[I(pr)*((b0 if q==0 else b)+(lam if j==qi else 0)) for j,pr in enumerate(['1/4','1/2','1/4'])]
        av.append(sum(x*t for x,t in zip(jj,tjs))/sum(jj))
    gaps=[]
    for j,t in enumerate(tjs):
        pays=[q*rho*(t-mean)-I('1/8')*abs(q) for q,mean in zip([-1,0,1],av)]
        gaps.append(least([pays[j]-pays[k] for k in range(3) if k!=j]))
    print('Collision perturbation',step,'price P(0)-P(1)',rho*(av[1]-av[2]),'choice margins',gaps)
print('Research region secondary margins: a_mono-a_up',amono-aup,
      'aU3(cap_hi)-a_up',values['res_region_aU3_6']-aup,
      'a36(cap_hi)-a_up',values['res_region_a36_6']-aup,
      'a_up-a_lo(cap_lo)',aup-values['res_region_alo_0'],
      'a_mono(1/3)-a',amono3-capcost)
