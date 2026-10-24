from pathlib import Path
from fractions import Fraction as Q
from math import factorial
import csv, re, itertools
from mpmath import mp, iv
mp.dps=90
iv.dps=80
ROOT = Path(__file__).resolve().parents[5]
OUT=Path('scripts/ext_2')
reg={x['key']:x for x in csv.DictReader((ROOT/'audit/slot_manuscript_2026_10_23/registry/registry.csv').open())}
files=[ROOT/'slot/manuscript'/folder/(name+'.tex') for folder,names in [('sections',['05_research','06_robustness','07_welfare','08_empirical']),('appendix',['A5_research','A6_robustness','A7_welfare','A8_empirical'])] for name in names]
keys=set().union(*(set(re.findall(r'\\reg\{([^}]+)\}',f.read_text())) for f in files))
val={}
def I(x):
 if hasattr(x,'_mpi_'): return x
 f=Q(x); return iv.mpf(f.numerator)/f.denominator
def put(key,x): val[key]=I(x); return val[key]
def endpoints(x):
 x=I(x); return mp.mpf(x.a),mp.mpf(x.b)
def mid(x):
 l,h=endpoints(x); return (l+h)/2
def imin(xs):
 ends=[endpoints(x) for x in xs]; return iv.mpf([min(x[0] for x in ends),min(x[1] for x in ends)])
def imax(xs): return -imin([-I(x) for x in xs])
def positive(x): return endpoints(x)[0]>0
def negative(x): return endpoints(x)[1]<0
def indicator(x):
 if positive(x): return I(1)
 if negative(x): return I(0)
 return iv.mpf([0,1])
def clamp(x):
 lo,hi=endpoints(x); return iv.mpf([max(mp.mpf(0),min(mp.mpf(1),lo)),max(mp.mpf(0),min(mp.mpf(1),hi))])
def root(fn,lo,hi):
 lo,hi=Q(lo),Q(hi)
 # The caller supplies an increasing function and a bracket.
 for _ in range(210):
  c=(lo+hi)/2; v=fn(I(c))
  if positive(v): hi=c
  elif negative(v): lo=c
  else: break
 return iv.mpf([endpoints(I(lo))[0],endpoints(I(hi))[1]])
E=iv.exp(I(1)); u=E-1; beta=I('0.294655'); lam=u*beta/(1+u*beta); b=(1-lam)*beta; b0=(1-lam)*(1-2*beta)
m=1/(1+E); M=1-m; rho=I('1/4'); k=I('1/50'); a=I('1/40'); half=I('1/2')
# Direct closed forms, including arbitrary reserves and class supports.
def point(v,p,r):
 v,p,r=map(Q,(v,p,r)); fp=min(p/r,Q(1)); t0=p*(1-fp); alloc0=max(Q(0),(r*r-p*p)/(2*r))
 if v<p: return (t0,Q(0),Q(0),Q(0),alloc0)
 if r<=p: return (p,v-p,Q(1),Q(1),v)
 if v<=r: t=v-(v*v-p*p)/(2*r); g=(v*v-p*p)/(2*r); win=v/r
 else: t=r/2+p*p/(2*r); g=v-t; win=Q(1)
 return (t,g,win,Q(1),alloc0+g+p*fp)
def average(law,p,r):
 lo,hi=map(Q,law); p,r=map(Q,(p,r))
 if lo==hi: return point(lo,p,r)
 # Open three-point Newton-Cotes exactly integrates each polynomial piece.
 cuts=sorted({lo,hi}|{c for c in [p,r] if lo<c<hi}); out=[Q(0)]*5
 for left,right in zip(cuts,cuts[1:]):
  width=right-left
  for z,w in [(Q(1,4),Q(2,3)),(Q(1,2),Q(-1,3)),(Q(3,4),Q(2,3))]:
   for j,f in enumerate(point(left+z*width,p,r)): out[j]+=width*w*f/(hi-lo)
 return tuple(out)
def auction(r):
 r=I(r); t0=half*(1-half/r); th=r/2+1/(8*r); tl=1-3/(8*r)
 return dict(t0=t0,th=th,tl=tl,gh=10-th,gl=1-tl,D=th-tl,wh=th-t0,wl=tl-t0)
def B(r,mu):
 z=auction(r); return z['gl']+mu*(z['gh']-z['gl'])
def D(r): return auction(r)['D']
def tau(r):
 z=auction(r); return (6-z['gl'])/(z['gh']-z['gl'])
def invD(d): return 1+d+iv.sqrt(d*d+2*d)
def mlam(l,beta=beta): return (1-l)*beta/(2*beta+l*(1-2*beta))
def lamE(r,beta=beta):
 t=tau(r); return beta*(2*t-1)/(beta+(1-2*beta)*(1-t))
def lamR(r):
 d=D(r); aa=2*a*(1-2*beta); bb=4*a*beta+k*(1-2*beta)+beta*d; cc=beta*(2*k-d)
 return -2*cc/(bb+iv.sqrt(bb*bb-4*aa*cc))
def phi(r): return D(r)*(1-tau(r))-k-2*a*lamE(r)
def entryR(l): return rho+(1-rho)*(beta+(half-beta)*l)
def ownR(l): return half*(rho+(1-rho)*(beta+(1-beta)*l))
rA=root(lambda r:D(r)*(1-tau(r))-k,'1.2','1.75'); rR=root(phi,'1.2','1.75')
rN=invD(2*k/rho); rcap=invD((2*a*lam+k)/m); rU=invD((k+a*lam)/(rho*m)); rC=root(lambda r:6-B(r,M),3,'3.6'); rS=invD(k/(rho*m))
inputs={'beta_B':'0.294655','prim_p':'1/2','prim_rho':'1/4','entry_r0':'1/4','res_a':'1/40','str_r155':'1.55','str_r160':'1.60','str_r165':'1.65','atom_L':'1/5','atom_eps':'1/10','atom_eps_small':'1/1000','access_out_cH':'12/5','rsv_points_excl':'101/100','rsv_bands_excl':'11/10','rsv_deter':'31/20','four_prior':'1/4','four_v1':'1','four_v2':'1001/1000','four_v3':'9999/1000','four_v4':'10','sig_aT':'.70','sig_d':'.75','sig_comp_aT':'.94','sig_comp_d':'.505','sig_cH':'7.14','sig_rho':'.85','sig_k':'.015','sig_r0':'1.1','sig_r1':'2.3','u_lo_frac':'82/59','u_hi_frac':'2686/1559','rS_cert_hi_B':'2.124149','rS_counter_r_B':'2.1241481'}
for key,x in inputs.items(): put(key,x)
for key,x in {'res_cap':lam,'res_rA':rA,'res_rR':rR,'res_rN':rN,'res_rcap':rcap,'res_rUR':rU,'res_rC':rC,'rC_B':rC,'rS_B':rS,'res_lambda_rR':lamE(rR),'res_entry_rR':entryR(lamE(rR)),'res_entry_cap':entryR(lam),'res_entry_r1':entryR(lam),'res_entry_r2':rho,'margin_res_rN_B':rN-rcap,'res_Delta_r0':D('1.2'),'margin_res_weak_B':k-D('1.2'),'margin_res_half_B':6-B('1.2',half)}.items(): put(key,x)
for tag,r in [('155','1.55'),('160','1.60'),('165','1.65')]:
 l=lamR(r); le=lamE(r); star=(2*a*le+k)/(D(r)*(1-tau(r)))
 for label,x in {'Delta':D(r),'tau':tau(r),'lamE':le,'lambda':l,'muplus':1-mlam(l),'entry':entryR(l),'own':ownR(l),'ULgap':k-rho*D(r)/2,'lamgap':l-le,'capgap':lam-l,'th_estar':star,'th_entry':rho+(star-rho)*(beta+(half-beta)*le)}.items(): put('res_'+label+'_r'+tag,x)
caplo,caphi=lamE(3),lamE('3.6'); alo=(D('1.65')*m-k)/(2*lam); aup=(D('1.55')*(1-tau('1.55'))-k)/(2*lamE('1.55'))
for key,x in {'res_cap_lo':caplo,'res_cap_hi':caphi,'res_a_lo':alo,'res_a_up':aup,'res_cap_lo_a':lamR('1.65'),'margin_res_alo_B':a-alo,'margin_res_aup_B':aup-a,'margin_res_caplo_B':lam-caplo,'margin_res_caphi_B':caphi-lam,'res_region_alo_0':(D('1.65')*mlam(caplo)-k)/(2*caplo),'res_region_aU3_6':(rho*D(3)*mlam(caphi)-k)/caphi,'res_region_a36_6':(rho*D('3.6')*mlam(caphi)-k)/caphi,'res_lamE_r175':lamE('1.75')}.items(): put(key,x)
for tag,r in [('r1',3),('r2','3.6')]: put('margin_res_bound_'+tag+'_B',rho*D(r)*m-k-a*lam)
put('margin_res_tau_r1_B',M-tau(3)); put('margin_res_tau_r2_B',tau('3.6')-M); put('margin_return_post_B',tau('3.6')-M); put('margin_return_B',6-B('3.6',M))
tmax=I(3)*(8*I('1.75')**2-I('1.75')+2)/(2*(20*I('1.2')-I('1.2')**2-1)**2)
dmin=(1-1/I('1.2')**2)/2; dtau=1-tau('1.75'); dmax=D('1.75'); lead=dmin*dtau-dmax*tmax
lmax=beta*tmax/(beta+(1-2*beta)*dtau)**2
for key,x in {'res_bound_dDelta':dmin,'res_bound_tau74':dtau,'res_bound_Delta74':dmax,'res_bound_taup':tmax,'res_dphi_lead':lead,'res_phip_lb':lead-2*a*lmax,'res_amono':lead/(2*lmax),'res_amono_third':lead/(2*(I('1/3')*tmax/(I('1/3')+I('1/3')*dtau)**2))}.items(): put(key,x)
x=(D('1.65')*m-k)/(2*a); put('res_beta_lo',x/(1-x)/u)
y=(D('1.55')*(1-tau('1.55'))-k)/(2*a); put('res_beta_hi',y*(1-tau('1.55'))/((2*tau('1.55')-1)*(1-y)))
# P5: prices and probabilities computed at the stated tuple.
f=b+lam/2; v=2*f; share=lam/v
put('vol_full_B',v); put('imb_buy_B',lam/2); put('entry_jump_B',(1-rho)*f)
def A(r,mu): z=auction(r); return z['wl']+z['D']*mu
def prices(r,chi):
 z=auction(r); return [z['t0']+rho*A(r,m),z['t0']+rho*A(r,half),z['t0']+(rho+(1-rho)*chi)*A(r,M)]
for tag,r,chi in [('r1',3,1),('r2','3.6',0)]:
 pm,pz,pp=prices(r,chi); probs=[f,1-2*f,f]; es=[rho,rho,rho+(1-rho)*chi]
 ent=sum(p*e for p,e in zip(probs,es)); avg=sum(p*x for p,x in zip(probs,[pm,pz,pp])); reportmean=sum(p*e*(1-e)*A(r,mu) for p,e,mu in zip(probs,es,[m,half,M]))/ent
 for key,x in {'ba_'+tag+'_B':pp-pm,'wgap_'+tag+'_B':share*(1-1/I(r)),'evprep_mean_'+tag+'_B':reportmean}.items():put(key,x)
 if tag=='r1':
  for key,x in {'ba_class_r1_B':rho*D(r)*share,'ba_entry_r1_B':(1-rho)*A(r,M),'ba_share_r1_B':(1-rho)*A(r,M)/(pp-pm),'cov_entry_r1_B':(1-rho)*f,'pbar_r1_B':avg,'p_neutral_r1_B':pz,'pdrop_neutral_r1_B':pz-avg}.items(): put(key,x)
for key,x in {'ba_jump_rC_B':(1-rho)*A(rC,M),'ba_rC_left_B':rho*D(rC)*share+(1-rho)*A(rC,M),'ba_rC_right_B':rho*D(rC)*share,'delta_rS_B':k/(rho*m),'margin_obs_rS_rC_B':rC-rS,'margin_obs_post_over_58_B':M-I('5/8'),'rS_counter_margin_B':rho*D('2.1241481')*m-k,'margin_obs_band_incentive_B':rho*D(3)*(1-tau('3.6'))-k,'theta_min_counts_B':3-2/v,'theta_max_full_eq_r1_B':1-2*k/(rho*D(3)),'theta_max_full_eq_r2_B':1-2*k/(rho*D('3.6')),'theta09_beta_B':v*I('.1')/(2*(1-v*I('.9'))),'theta09_lowsale_r1_B':rho*D(3)*I('.05')-k,'alt_theta_B':I('4/9'),'alt_ba_r1_B':rho*D(3)*I('4/9')+(1-rho)*A(3,I('13/18'))}.items():put(key,x)
vu=2*b+lam/2; put('U_gap_r160_B',rho*D('1.6')*lam/(4*(1-vu)))
s=b*(2*tau('1.6')-1)/(1-tau('1.6')); ent1=k/(D('1.6')*(1-tau('1.6')))
for key,x in {'mix_sigma_r160_B':s/lam,'mix_e1_r160_B':ent1,'mix_mean_order_r160_B':s/2,'mix_lowsale_r160_B':rho*D('1.6')/2-k,'mix_entry_r160_B':rho+(ent1-rho)*(b+s/2)}.items(): put(key,x)
# P2: general classes, reserves, access and surplus.
cases={
'base':('10','10','1','1','1/2','6','1/50',['6/5','3','18/5']),
'moderate':('2','2','1','1','1/2','89/100','1/500',['21/20','3/2']),
'bands':('199/20','201/20','19/20','21/20','1/2','6','1/50',['6/5','3','18/5']),
'ex_a':('10','10','1','1','3/10','9/2','1/100',['11/10','3','18/5']),
'ex_b':('10','10','1','1','7/10','36/5','1/100',['11/10','3','18/5']),
'ex_c':('1','19','3/5','7/5','7/10','67/10','1/50',['1','9/2','11/2']),
'ex_d':('10','10','1','1','7/10','67/10','1/50',['1','9/2','11/2'])}
def node(stem,case,r,p='1/2',orders=(1,-1),pattern=(0,0,1),cost=None,prior=None):
 hl,hh,ll,lh,pi,c,fee,rs=case; pi=I(pi if prior is None else prior); c=I(c if cost is None else cost)
 H=list(map(I,average((hl,hh),p,r))); L=list(map(I,average((ll,lh),p,r))); rf,pf=Q(r),Q(p); fp=I(min(pf/rf,Q(1))); t0=I(pf)*(1-fp); alloc0=I(max(Q(0),(rf*rf-pf*pf)/(2*rf)))
 d=H[0]-L[0]; mus=[]; masses=[]; eh=I(0); el=I(0); prep=I(0); rev=I(0); costpaid=I(0)
 for q,base,n in zip([-1,0,1],[b,b0,b],pattern):
  fh=base+(lam if orders[0]==q else 0); fl=base+(lam if orders[1]==q else 0); mass=pi*fh+(1-pi)*fl; mu=pi*fh/mass; e=rho+(1-rho)*n
  mus.append(mu); masses.append(mass); eh+=fh*e; el+=fl*e; prep+=mass*e; rev+=mass*(t0+e*(L[0]-t0+d*mu)); costpaid+=mass*n*(1-rho)*c
  suffix={-1:'minus',0:'zero',1:'plus'}[q]; put(stem+'_cost_sign_'+suffix,L[1]+mu*(H[1]-L[1])-c)
 adm=pi*eh*H[3]+(1-pi)*el*L[3]; totalalloc=alloc0+pi*eh*(H[4]-alloc0)+(1-pi)*el*(L[4]-alloc0)
 out={'entry':prep,'ownership':pi*eh*H[2],'proceeds':rev,'surplus':totalalloc-costpaid,'sale':1-fp+fp*adm,'two':(1-fp)*adm,'prior_cost_margin':c-L[1]-pi*(H[1]-L[1]),'global':rho*d*imin([1-(pi*E)/(1-pi+pi*E),pi/(pi+(1-pi)*E)])-I(fee)}
 for key,x in out.items(): put(stem+'_'+key,x)
 return out,H,L,d
nodes={}
for name,case in cases.items():
 hl,hh,ll,lh,pi,c,fee,rs=case
 for key,x in dict(high_lo=hl,high_hi=hh,low_lo=ll,low_hi=lh,pi=pi,cost=c,k=fee,**{'r'+str(i):r for i,r in enumerate(rs)}).items():put('p2_input_'+name+'_'+key,x)
 for i,r in enumerate(rs):
  n=node('p2_'+name+'_r'+str(i),case,r,orders=(0,0) if i==0 else (1,-1),pattern=(0,0,1) if i==1 and name!='ex_d' else (0,0,0)); nodes[name,i]=n
  if name=='ex_d' and i==1: put('margin_p2_ex_d_strong_top_B',val['p2_ex_d_r1_cost_sign_plus'])
for pi,tag in [('3/10','three_tenths'),('7/10','seven_tenths')]:
 for i,r in enumerate(['6/5','3','18/5']):
  pat=(0,0,0) if pi=='3/10' else (1,1,1) if i==0 else (0,0,1)
  node('p2_fixed_prior_'+tag+'_r'+str(i),cases['base'],r,orders=(0,0) if i==0 else (1,-1),pattern=pat,prior=pi)
seen=nodes['base',1][0]; hidden=node('p2_base_hidden',cases['base'],'3',pattern=(0,0,0))[0]
dR=seen['proceeds']-hidden['proceeds']; dW=seen['surplus']-hidden['surplus']; gross=lam*D(3)*(half*(1-M)+half*rho*m)
for key,x in {'p2_access_proceeds_gain':dR,'p2_access_surplus_gain':dW,'p2_access_gross_transfer':gross,'p2_access_break_even':dR/gross,'res_dR_r1':dR,'res_dW_r1':dW,'pay_gap_coef':D(3)-D('1.2')}.items():put(key,x)
outseen=node('p2_outside_seen',cases['base'],'3',pattern=(0,1,1),cost='12/5')[0]; outhidden=node('p2_outside_hidden',cases['base'],'3',pattern=(1,1,1),cost='12/5')[0]
for label in ['proceeds','surplus']: put('p2_outside_'+label+'_gain',outseen[label]-outhidden[label])
# The hidden economy uses the prior for entry; its reported node beliefs only serve prices.
rnodes={}
for name,case,pex in [('points',cases['base'],'101/100'),('bands',cases['bands'],'11/10')]:
 for tag,p in [('base','1/2'),('exclude',pex),('deter','31/20')]:
  for i,r in enumerate(['6/5','3']):
   pat=(0,0,0) if (tag=='base' and i==0) or (tag=='deter' and i==1) else (0,0,1)
   rnodes[name,tag,i]=node('p2_reserve_'+name+'_'+tag+'_r'+str(i),case,r,p,orders=(0,0) if tag=='base' and i==0 else (1,-1),pattern=pat)[0]
 for i in [0,1]:
  put('margin_p2_reserve_'+name+'_exclude_gain'+str(i)+'_B',rnodes[name,'exclude',i]['proceeds']-rnodes[name,'base',i]['proceeds'])
  put('margin_p2_reserve_'+name+'_rev'+str(i)+'_B',rnodes[name,'deter',i]['proceeds']-rnodes[name,'base',i]['proceeds'])
pH=iv.sqrt(6*(10-6/M)-9); ptop=10-6/M; dph=I('3/2')-pH+pH*pH/2
for key,x in {'p2_reserve_ph':pH,'p2_reserve_weak_top':ptop,'margin_p2_ph_weak_B':pH-I('6/5'),'margin_p2_deter_lower_B':I('31/20')-pH,'margin_p2_deter_upper_B':ptop-I('31/20'),'margin_p2_ph_trade_B':rho*m*dph-k,'margin_p2_reserve_admissible_top_B':M*I('413/50')-6,'margin_p2_reserve_uniform_weak_B':rho*m*I('17/20')-k,'margin_p2_reserve_uniform_strong_B':rho*m-k}.items():put(key,x)
node('p2_endpoint_r1',cases['base'],'3','10',pattern=(0,0,0))
# More than two classes: posterior vectors and fixed-price payoffs.
weight=(1+2*b0+lam)/2; put('p2_many_weight',weight); priors=[I('1/4'),half,I('1/4')]; ts=[I(1),1+I('49/16')*weight,I('65/16')]; means=[]
for qi,(q,base) in enumerate(zip([-1,0,1],[b,b0,b])):
 joint=[p*(base+(lam if j==qi else 0)) for j,p in enumerate(priors)]; post=[v/sum(joint) for v in joint]; mean=sum(p*t for p,t in zip(post,ts)); means.append(mean)
 for j,mu in enumerate(post):put('p2_many_q'+str(qi)+'_mu'+str(j),mu)
 put('p2_many_q'+str(qi)+'_price',I('7/8')+rho*(mean-I('7/8')))
for j,t in enumerate(ts):
 pays=[q*rho*(t-mean)-I('1/8')*abs(q) for q,mean in zip([-1,0,1],means)]
 put('p2_many_choice'+str(j),imin([pays[j]-pay for i,pay in enumerate(pays) if i!=j]))
vals=['1','1001/1000','9999/1000','10']; objs0=[tuple(map(I,point(v,'1/2','6/5'))) for v in vals]; objs1=[tuple(map(I,point(v,'1/2','3'))) for v in vals]
possible=[]
for bits in itertools.product([0,1],repeat=4):
 weights=[E if z else I(1) for z in bits]; possible.append(sum(w*o[0] for w,o in zip(weights,objs1))/sum(weights))
gamma=imin([imin([o[0] for o in objs1[2:]])-imax(possible),imin(possible)-imax([o[0] for o in objs1[:2]])]); gl=sum(o[1] for o in objs1[:2])/2; gh=sum(o[1] for o in objs1[2:])/2
for key,x in {'p2_groups_gamma':gamma,'p2_groups_trade':rho*gamma-k,'p2_groups_weak_range':k-(imax([o[0] for o in objs0])-imin([o[0] for o in objs0])),'p2_groups_weak_cost':6-sum(o[1] for o in objs0)/4,'p2_groups_profit_gap':gh-gl,'p2_groups_top':gl+M*(gh-gl)-6}.items():put(key,x)
# P4: cost laws and private signals, from the joint law of class, signal and order.
for key,x in {'p4_control_crossing_r0_r1':0,'p4_control_crossing_r1_r2':(1-rho)*f,'p4_frozen_entry_below_ceiling':entryR(lam),'p4_frozen_entry_above_ceiling':rho,'p4_hidden_r0_entry':rho,'margin_p4_atomless_floor_B':B(3,m)-I('1/5'),'margin_p4_atomless_weak_B':I('59/10')-B('1.2',half),'margin_p4_atomless_strong_B':B(3,M)-I('61/10'),'margin_p4_atomless_return_B':I('59/10')-B('3.6',M),'margin_p4_atomless_top_lower_r2_B':B('3.6',M)-I('59/10'),'margin_p4_atomless_top_upper_r2_B':I('61/10')-B('3.6',M),'p4_atomless_max_width_floor_r2':6-B('3.6',M),'margin_p4_atomless_small_width_return':6-B('3.6',M)-I('1/1000')}.items():put(key,x)
for idx,r in [('1','3'),('2','3.6')]:
 upper=clamp((B(r,M)-I('59/10'))/I('1/5'))
 put('p4_atomless_r'+idx+'_entry',rho+(1-rho)*f*upper)
 put('p4_atomless_r'+idx+'_own',half*(rho+(1-rho)*(b+lam)*upper))
def phi_y(mu,d,positive_signal):
 w=d if positive_signal else 1-d
 return mu*w/(mu*w+(1-mu)*(1-w))
def signal_node(stem,r,rh,c,fee,acc,d,s,t):
 rh,c,fee,acc,d=map(I,(rh,c,fee,acc,d)); z=auction(r); ehbar=I(0); elbar=I(0); public={}
 for q,base,fh,fl in [(-1,b,b,b+t),(0,b0,b0+lam-s,b0+lam-t),(1,b,b+s,b)]:
  nu=fh/(fh+fl); mu=1-acc+(2*acc-1)*nu; public[q]=mu
  Ip=indicator(B(r,phi_y(mu,d,True))-c); Im=indicator(B(r,phi_y(mu,d,False))-c)
  eh=rh+(1-rh)*(d*Ip+(1-d)*Im); el=rh+(1-rh)*((1-d)*Ip+d*Im)
  # T and Y are conditionally independent given the class.
  lh=acc*fh+(1-acc)*fl; ll=(1-acc)*fh+acc*fl
  ehbar+=lh*eh; elbar+=ll*el
 put(stem+'_entry',(ehbar+elbar)/2); put(stem+'_own',ehbar/2)
 put(stem+'_buy_rate',s/lam); put(stem+'_sell_rate',t/lam)
 return public

def signal_margin(stem,r0,r1,rh,c,fee,acc,d):
 rh,c,fee,acc,d=map(I,(rh,c,fee,acc,d)); zz=2*acc-1; top=1-acc+zz*M; z0=auction(r0)
 out={'private':c-B(r0,d),'joint':B(r1,phi_y(top,d,True))-c,'weak':fee-zz*(D(r0)+(1-rh)*(2*d-1)*z0['wh']),'strong':zz*rh*m*D(r1)-fee,'other_pair':c-B(r1,phi_y(top,d,False))}
 for key,x in out.items():put('margin_'+stem+'_'+key,x)
 return out
signal_margin('p4_signal_s','1.1','2.3','.85','7.14','.015','.70','.75')
signal_margin('p4_signal_comp_b','1.2','3','.25','6','.02','.94','.505')
signal_margin('p4_grid_72_75','1.1','2.3','.85','7.14','.015','.72','.75')
for regime,acc,d in [('signal','.70','.75'),('no_y','.70','.50'),('class','1','.50')]:
 for idx,r in [('0','1.1'),('1','2.3')]:signal_node('p4_s_'+regime+'_r'+idx,r,'.85','7.14','.015',acc,d,I(0) if idx=='0' else lam,I(0) if idx=='0' else lam)
for regime,acc,d in [('comp_b','.94','.505'),('comp_b_no_y','.94','.50')]:
 for idx,r in [('0','1.2'),('1','3')]:signal_node('p4_'+regime+'_r'+idx,r,'.25','6','.02',acc,d,I(0) if idx=='0' else lam,I(0) if idx=='0' else lam)
controls={'s_no_y_weak':I('.015')-I('.4')*D('1.1'),'s_no_y_strong':I('.4')*I('.85')*m*D('2.3')-I('.015'),'s_no_y_top_r0':I('7.14')-B('1.1',I('.3')+I('.4')*M),'s_no_y_top_r1':I('7.14')-B('2.3',I('.3')+I('.4')*M),'s_class_weak':I('.015')-D('1.1'),'s_class_strong':I('.85')*m*D('2.3')-I('.015'),'s_class_prior_r0':I('7.14')-B('1.1',half),'s_class_top_r1':I('7.14')-B('2.3',M),'comp_b_no_y_weak':k-I('.88')*D('1.2'),'comp_b_no_y_strong':I('.88')*rho*m*D('3')-k,'comp_b_no_y_top_r1':6-B('3',I('.06')+I('.88')*M)}
for key,x in controls.items():put('margin_p4_'+key,x)
zmin=k/(m*rho*D('3')); put('p4_b_signal_z_min',zmin); put('margin_p4_b_d_ge_a_impossible',zmin*(D('1.2')+(1-rho)*zmin*auction('1.2')['wh'])-k)
s0=I('119/96')*b; t1=I('4/3')*b
signal_node('p4_b_signal_r0','1.2','.25','6','.02','.70','.75',s0,s0)
public1=signal_node('p4_b_signal_r1','3','.25','6','.02','.70','.75',lam,t1)
put('p4_b_no_y_r1_zero_gross',rho*I('.4')*D(3)/2); put('p4_b_no_y_r1_full_gross',rho*I('.4')*D(3)*m)
mulo=I('.3')+I('.4')*m; muhi=I('.3')+I('.4')*M; dp0=I('13/16')*auction('1.2')['wh']-I('7/16')*auction('1.2')['wl']; dp1=I('13/16')*auction(3)['wh']-I('7/16')*auction(3)['wl']
extras={'b_weak_all_yplus':B('1.2',phi_y(mulo,I('.75'),True))-6,'b_weak_no_yminus':6-B('1.2',phi_y(muhi,I('.75'),False)),'b_weak_zero_return':I('.4')*dp0/2-k,'b_weak_full_loss':k-I('.4')*m*dp0,'b_weak_rate_room':u-I('119/96'),'b_strong_buy':I('.4')*m*dp1-k,'b_strong_prior_yplus':B(3,I('.75'))-6,'b_strong_no_yminus':6-B(3,phi_y(muhi,I('.75'),False)),'b_strong_threshold_floor_return':I('19/795')-k,'b_strong_rate_room':u-I('4/3'),'b_strong_sale_public_gap':I('47/106')-I('21/50'),'b_strong_zero_yplus':B(3,phi_y(public1[0],I('.75'),True))-6}
for key,x in extras.items():put('margin_p4_'+key,x)
# Each row reports a calculation and its distance from the printed number.
# This script has no assertions and does not select a pass/fail exit status.
def shown_number(s):
 if '\\%' in s: return mp.mpf(s.replace('\\%',''))/100, mp.mpf('0.0005')
 if 'ensuremath' in s:
  match=re.search(r'([+-]?[0-9.]+)\\times10\^\{([+-]?[0-9]+)\}',s); mant,exp=match.groups(); exp=int(exp); places=len(mant.split('.')[1]) if '.' in mant else 0
  return mp.mpf(mant)*10**mp.mpf(exp),mp.mpf('0.5')*10**mp.mpf(exp-places)
 q=Q(s); places=len(s.split('.')[1]) if '.' in s else None
 return mp.mpf(q.numerator)/q.denominator,(mp.mpf('0.5')*mp.power(10,-places) if places is not None else mp.mpf('1e-60'))
rows=[]; diffs=[]
for key in sorted(keys & val.keys()):
 lo,hi=endpoints(val[key]); target,unit=shown_number(reg[key]['display']); distance=max(mp.mpf(0),lo-target,target-hi)
 rows.append([key,mp.nstr(lo,45),mp.nstr(hi,45),reg[key]['display'],mp.nstr((lo+hi)/2-target,18),reg[key]['source_script']])
 if distance>unit+mp.mpf('1e-70'): diffs.append((key,mp.nstr((lo+hi)/2,35),reg[key]['display'],mp.nstr(distance,10),mp.nstr(unit,10)))
with (OUT/'recomputed_values.tsv').open('w') as f:
 writer=csv.writer(f,delimiter='\t'); writer.writerow(['key','lower','upper','display','computed_minus_display','source']);writer.writerows(rows)
numlines=(ROOT/'slot/manuscript/numbers.tex').read_text().splitlines(); tex={}
for line in numlines:
 match=re.match(r'\\expandafter\\def\\csname reg@([^\\]+)\\endcsname\{(.*)\}',line)
 if match: tex[match[1]]=match[2]
texdiff=[(key,tex.get(key),reg[key]['display']) for key in sorted(keys) if tex.get(key)!=reg[key]['display']]
print('Referenced keys',len(keys),'Computed keys',len(keys&val.keys()))
print('Not yet computed',sorted(keys-val.keys()))
print('Display distances beyond half a displayed unit',diffs)
print('Manuscript and registry display differences',texdiff)
print('Output',OUT/'recomputed_values.tsv')
print('Research signs', {k:mp.nstr(mid(val[k]),16) for k in ['res_phip_lb','margin_res_bound_r1_B','margin_res_bound_r2_B','margin_res_caphi_B']})
