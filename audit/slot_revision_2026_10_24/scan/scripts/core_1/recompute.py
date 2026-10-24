"""Independent printed computations for the core manuscript. No assertions or repository writes."""
from fractions import Fraction as Q
from math import factorial, isqrt, lcm, gcd
from pathlib import Path
from decimal import Decimal, localcontext
import csv, re, json

OUT=Path('scripts/core_1')
ROOT = Path(__file__).resolve().parents[5]
class I:
    def __init__(self, lo, hi=None):
        if isinstance(lo,I): self.lo,self.hi=lo.lo,lo.hi
        else: self.lo,self.hi=Q(lo),Q(lo if hi is None else hi)
    def __add__(self,o):
        o=I(o); return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,o): return self+-I(o)
    def __rsub__(self,o): return I(o)+-self
    def __mul__(self,o):
        o=I(o); z=[a*b for a in [self.lo,self.hi] for b in [o.lo,o.hi]]; return I(min(z),max(z))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I(o)
        if o.lo<=0<=o.hi: raise ValueError('Interval division across zero')
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o): return I(o)/self
    def __pow__(self,n):
        if n==0: return I(1)
        if n<0: return I(1)/(self**(-n))
        return self*(self**(n-1))

def dec(q,n=24):
    with localcontext() as ctx:
        ctx.prec=max(n+20,80)
        return format(Decimal(q.numerator)/Decimal(q.denominator),f'.{n}f')
def enclosure(x,n=24):
    x=I(x); scale=10**n
    low=(x.lo.numerator*scale)//x.lo.denominator
    high=-((-x.hi.numerator*scale)//x.hi.denominator)
    return '['+dec(Q(low,scale),n)+', '+dec(Q(high,scale),n)+']'
def sqrtI(x):
    x=I(x); scale=10**80
    a=isqrt(x.lo.numerator*scale**2//x.lo.denominator)
    b=isqrt(x.hi.numerator*scale**2//x.hi.denominator)+1
    return I(Q(a,scale),Q(b,scale))
def root(f,lo=Q(6,5),hi=Q(18,5)):
    lo,hi=Q(lo),Q(hi)
    for _ in range(185):
        mid=(lo+hi)/2; val=I(f(mid))
        if val.hi<0: lo=mid
        elif val.lo>0: hi=mid
        elif val.lo==val.hi==0: return I(mid)
        else: break
    print('root',enclosure(I(lo,hi)), 'f(lo) sign',('-' if I(f(lo)).hi<0 else '0?'),'f(hi) sign',('+' if I(f(hi)).lo>0 else '0?'),'width',dec(hi-lo,60))
    return I(lo,hi)

h,l,p,rho,c,k,pi=Q(10),Q(1),Q(1,2),Q(1,4),Q(6),Q(1,50),Q(1,2)
r0,r1,r2=Q(6,5),Q(3),Q(18,5)
beta=Q('0.294655')
e_lo=sum((Q(1,factorial(j)) for j in range(111)),Q(0))
e_hi=e_lo+Q(112,111*factorial(111))
e=I(e_lo,e_hi); u=e-1
b=beta/(1+u*beta); lam=u*b; b0=(1-lam)*(1-2*beta)
M=e/(1+e); m=1/(1+e)
def D(r): return (r-1)**2/(2*r)
def tau(r): return (12*r-Q(3,4))/(20*r-r*r-1)
def J(r): return D(r)*(1-tau(r))
def B(r,mu): return Q(3,4)/(2*r)+mu*(h-r/2-1/(2*r))
def auction(r): return dict(t0=p*(1-p/r),th=r/2+p*p/(2*r),tl=l-Q(3,4)/(2*r),gh=h-r/2-p*p/(2*r),gl=Q(3,4)/(2*r))
def fr(d): return 1+d+sqrtI(d*d+2*d)
rA=root(lambda r:J(r)-k); rJ=root(lambda r:rho*J(r)-k)
rstar=root(lambda r:rho*D(r)*tau(r)-k)
rF=fr(k/(1-M)); rN=fr(I(2*k/rho)); rS=fr(k/(rho*m))
rC=root(lambda r:tau(r)-M)
tA,tJ,pimax=tau(rA),tau(rJ),tau(rstar)
E1=rho+(1-rho)*(b+pi*lam); eH=rho+(1-rho)*(b+lam); eL=rho+(1-rho)*b
own=eH*pi
v={}
def put(key,x): v[key]=I(x)
for key,x in dict(prim_h=h,prim_ell=l,prim_p=p,prim_rho=rho,prim_cH=c,prim_k=k,prim_pi=pi,prim_r0=r0,prim_r1=r1,prim_r2=r2,u_B=u,beta_B=beta,lambda_B=lam,b_B=b,b0_B=b0,M_half_B=M,m_half_B=m,b_plus_lambda_B=b+lam).items():put(key,x)
for name,r in [('r0',r0),('r1',r1),('r2',r2)]:
    a=auction(r)
    for key,x in a.items():put(f'p2_base_{name}_{key}',x)
    for key,x in [('Delta',D(r)),('tau',tau(r))]:
        put(f'{key}_{name}',x);put(f'{key}_{name}_frac',x)
    put('Bprior_'+name+('_B' if name=='r1' else ''),B(r,pi))
    mus=[I(pi)]*3 if name=='r0' else [m,I(pi),M]
    ents=[I(rho)]*3 if name!='r1' else [I(rho),I(rho),I(1)]
    prices=[]
    for sgn,mu,ent in zip(['minus','zero','plus'],mus,ents):
        put(f'p2_base_{name}_mu_{sgn}',mu)
        prices.append(a['t0']+ent*(a['tl']-a['t0']+D(r)*mu))
    for suffix,P in zip(['m1','0','p1'],prices):put(f'price_{name}_{suffix}_B',P)
put('price_r0',v['price_r0_0_B'])
for key,x in dict(entry_r0=rho,entry_r1_B=E1,entry_r2=rho,eH_r1_B=eH,eL_r1_B=eL,own_r0=pi*rho,own_r1_B=own,own_r2_B=pi*rho,B_r0_half=B(r0,pi),B_r1_half=B(r1,pi)).items():put(key,x)
ulo,uhi,uk=Q(82,59),Q(2686,1559),Q(19,3)
for key,x in [('u_lo',ulo),('u_hi',uhi),('u_kstrong',uk),('M_lo',tau(r1)),('M_hi',tau(r2))]:
    put(key,x);put(key+'_frac',x)
llo=ulo*beta/(1+ulo*beta); lhi=uhi*beta/(1+uhi*beta)
plo=141/(141+59*e);phi=4245/(4245+1559*e)
for key,x in dict(lambda_lo_B=llo,lambda_hi_B=lhi,lambda_lo_third=Q(82,259),lambda_hi_third=Q(2686,7363),prior_lo_B=plo,prior_hi_B=phi,prior_ii_hi=tau(r0),prior_kappa_lo_B=3*e/(22+3*e),prior_kappa_hi_B=22/(22+3*e),p2_prior_trade_lo=e/(9+e),p2_prior_trade_hi=9/(9+e)).items():put(key,x)
mg=dict(weakcost_B=c-B(r0,pi),recruit_B=B(r1,M)-c,kweak_B=k-D(r0),kstrong_B=rho*m*D(r1)-k,return_B=c-B(r2,M),return_post_B=tau(r2)-M,recruit_post_B=M-tau(r1),implied_prior_r1=c-B(r1,pi),kstrong2_B=rho*m*D(r2)-k,implied_prior_r2=c-B(r2,pi),tau_r0_half=tau(r0)-pi,beta_B=Q(1,3)-beta,u_lo_B=u-ulo,u_hi_B=uhi-u,u_kstrong_B=uk-u,lambda_lo_B=lam-llo,lambda_hi_B=lhi-lam,prior_lo_B=pi-plo,prior_hi_B=phi-pi,Delta_pos_B=D(r0),gHgL_B=h-r2/2-1/(2*r2),J_r0_B=k-J(r0),rhoJ_r1_B=rho*J(r1)-k,rhoJ_r2_B=rho*J(r2)-k,rhoJ_2_B=rho*J(Q(2))-k,tau_r2_3q_B=Q(3,4)-tau(r2),tau_rN_half_B=tau(rN)-pi,tauA_3q_B=Q(3,4)-tA,pimax_tauA_B=pimax-tA,piA_hi=tA-pi,p2_bplus_B=b+lam-pi,p4_ownership_rise_B=eH-rho,p4_weak_top_B=B(r0,M)-c)
pialo=tA/(tA+(1-tA)*e);mg['piA_lo_B']=pi-pialo
for key,x in mg.items():put('margin_'+key,x);put('margin_'+key+'_frac',x)
for key,x in dict(rA=rA,rJ=rJ,rstar=rstar,rF_B=rF,rN=rN,rS_B=rS,rC_B=rC,piA_lo_B=pialo,piA_hi=tA,pimax=pimax,Delta_rA=D(rA),tau_rA=tA,tau_rJ=tJ,J_r0=J(r0),rhoJ_r1=rho*J(r1),rhoJ_r2=rho*J(r2)).items():put(key,x)
for nm,gap in [('rA_r0',rA-r0),('rF_rA',rF-rA),('rN_rF',rN-rF),('rJ_rN',rJ-rN),('rS_rJ',rS-rJ),('r1_rS',r1-rS),('rC_r1',rC-r1),('r2_rC',r2-rC)]:put('gap_'+nm+'_B',gap)
put('entry_rA_B',rho+(1-rho)*b/(2*(1-tA)))
for name,r in [('r140',Q(7,5)),('r145',Q(29,20))]:
    put('str_'+name,r);put('entry_mb_'+name+'_B',rho+(1-rho)*b*D(r)/(2*k))
for name,r in [('r155',Q(31,20)),('r160',Q(8,5)),('r165',Q(33,20))]:
    put('str_'+name,r);put('entry_th_'+name+'_B',rho+b*(k-rho*J(r))/(2*D(r)*(1-tau(r))**2))
put('Delta_r155_frac',D(Q(31,20)))
Mpm=pimax*e/(pimax*e+1-pimax)
for key,x in dict(M_pimax_B=Mpm,mu0_pimax_B=pimax*b0/(pimax*b0+(1-pimax)*(b0+lam)),margin_cmend_B=D(rstar)*(1-Mpm)-k,entry_cmend_B=rho+(1-rho)*(b+pimax*lam)).items():put(key,x)
cex=Q(47,10)
for key,x in dict(nec_cH=cex,nec_r2=Q(8),nec_margin_kweak=k-D(r0),nec_margin_prior_r1=cex-B(r1,pi),nec_margin_recruit_B=B(r1,M)-cex,nec_margin_kstrong_B=rho*m*D(r1)-k,nec_margin_return_B=cex-B(Q(8),M),nec_margin_weakcost=cex-B(r0,pi),nec_entry_r0=Q(1)).items():put(key,x)
for name,r in [('r0',r0),('r1',r1),('r2',r2)]:
    a=auction(r); baseline=a['t0']+rho*((a['th']+a['tl'])/2-a['t0'])
    extra=(1-rho)*(pi*(b+lam)*(a['th']-a['t0'])+(1-pi)*b*(a['tl']-a['t0']))
    put('p4_base_'+name+'_proceeds',baseline+extra if name=='r1' else baseline)
    for key,x in [('entry',E1),('own',own),('proceeds',baseline+extra)]:put(f'p4_frozen_{name}_{key}',x)
    for key,x in [('entry',rho),('own',rho*pi),('proceeds',baseline)]:put(f'p4_hidden_{name}_{key}',x)
put('p4_control_crossing_r0_r1',0);put('p4_control_crossing_r1_r2',E1-rho)
a=auction(r1); entry_component=(1-rho)*(a['tl']-a['t0']+D(r1)*M)
put('ba_share_r1_B',100*entry_component/(v['price_r1_p1_B']-v['price_r1_m1_B']))
for key,x in dict(weak_cost=c-B(r0,pi),strong_top=B(r1,M)-c,weak_trade=k-D(r0),high_floor=rho*(1-M)*D(r1)-k,low_floor=rho*m*D(r1)-k,collapse=c-B(r2,M),ownership=eH-rho).items():put('margin_p2_base_'+key+'_B',x)

# Polynomial arithmetic, independently derived from the rational expressions.
def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return [-x for x in a]
def mul(a,b):
    z=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return trim(z)
def deriv(a):return [i*a[i] for i in range(1,len(a))] or [Q(0)]
def val(a,x):
    z=Q(0)
    for c0 in reversed(a):z=z*x+c0
    return z
def rem(a,b):
    a=list(a)
    while len(a)>=len(b) and a!=[0]:
        s=len(a)-len(b);fac=a[-1]/b[-1]
        a=add(a,[Q(0)]*s+[-fac*z for z in b])
    return a

def prim(a):
    scale=lcm(*(x.denominator for x in a));z=[int(x*scale) for x in a]
    g=gcd(*z);return [Q(x,g) for x in z]

def changes(a,x):
    z=[val(p0,x) for p0 in a];s=[1 if y>0 else -1 for y in z if y!=0]
    return sum(a0!=b1 for a0,b1 in zip(s,s[1:]))
def sturm(a,lo,hi):
    seq=[prim(a),prim(deriv(a))]
    while seq[-1]!=[0]:
        rr=rem(seq[-2],seq[-1])
        if rr==[0]:break
        seq.append(prim(neg(rr)))
    return changes(seq,lo),changes(seq,hi)
def dn(n,d):return add(mul(deriv(n),d),neg(mul(n,deriv(d))))
tn=[-Q(3,4),Q(12)];td=[Q(-1),Q(20),Q(-1)]
on=add(td,neg(tn));dd=[Q(0),Q(2)];nn=[Q(1),Q(-2),Q(1)]
jnum,jden=mul(nn,on),mul(dd,td)
snum,sden=mul(nn,mul(on,on)),mul(dd,mul(td,td))
qj=prim(dn(jnum,jden));qs=prim(dn(snum,sden))
put('QJ_r0',val(qj,r0))
for name,poly,lo,hi in [('Jprime',qj,r0,r2),('Sprime',qs,r0,Q(2)),('Sprime_full_path',qs,r0,r2)]:
    vleft,vright=sturm(poly,lo,hi)
    print(name,'coefficients low to high',','.join(str(q) for q in poly))
    print(name,'Sturm variations',vleft,vright,'root count',vleft-vright,'left value',str(val(poly,lo)))

reg={x['key']:x for x in csv.DictReader((ROOT/'audit/slot_manuscript_2026_10_23/registry/registry.csv').open())}
files=[ROOT/'slot/manuscript/sections'/f for f in ['01_introduction.tex','02_model.tex','03_competition_information.tex','04_equilibrium_results.tex']]+[ROOT/'slot/manuscript/appendix'/f for f in ['A1_payoffs.tex','A2_beliefs_trading.tex','A3_proposition2.tex','A4_coexistence.tex']]
keys=set(k0 for f in files for k0 in re.findall(r'\\reg\{([^}]+)\}',f.read_text()))
for lineno,line in enumerate((ROOT/'slot/manuscript/appendix/A9_parameters.tex').read_text().splitlines(),1):
    if lineno<=28 or 91<=lineno<=132 or lineno in [167,228]:
        keys.update(re.findall(r'\\reg\{([^}]+)\}',line))
numbers=dict(re.findall(r'\\csname reg@([^\\]+)\\endcsname\{([^\n]*)\}',(ROOT/'slot/manuscript/numbers.tex').read_text()))
rows=[];differences=[]
for key in sorted(keys):
    meta=reg[key];x=v.get(key)
    if x is None:
        print('OUTSIDE_CORE',key);continue
    display=meta['display'];bare=display.replace(r'\%','')
    if '/' in bare:
        requested=Q(bare);compatible=x.lo<=requested<=x.hi
    else:
        requested=Q(bare);places=len(bare.partition('.')[2]);half=Q(1,2*10**places)
        compatible=requested-half<=x.lo and x.hi<=requested+half
    row=dict(key=key,display=display,computed_lo=dec(x.lo,30),computed_hi=dec(x.hi,30),display_compatible=compatible,numbers_tex=numbers.get(key),status=meta['status'])
    rows.append(row)
    if not compatible or numbers.get(key)!=display:differences.append(row)
with (OUT/'recomputed_values.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
with (OUT/'rational_endpoints.json').open('w') as f:
    json.dump({key:{'lo':str(x.lo),'hi':str(x.hi)} for key,x in v.items()},f,indent=2)
print('Euler series interval',enclosure(e,60),'width',dec(e.hi-e.lo,180))
for key in ['lambda_B','b_B','M_half_B','margin_weakcost_B','margin_recruit_B','margin_kweak_B','margin_kstrong_B','margin_return_B','margin_return_post_B','rA','rF_B','rN','rJ','rS_B','rC_B','gap_r2_rC_B','piA_lo_B','piA_hi','pimax','margin_cmend_B']:
    print(key,enclosure(v[key]))
print('Computed displays',len(rows),'differences',json.dumps(differences))
print('Core scope keys',len(keys),'outside computation',','.join(sorted(keys-set(v))))

print('Direct investor payoffs against fixed tuples, order -1,0,+1')
for name,r in [('r0',r0),('r1',r1),('r2',r2)]:
    a=auction(r)
    mus=[I(pi)]*3 if name=='r0' else [m,I(pi),M]
    ents=[I(rho)]*3 if name!='r1' else [I(rho),I(rho),I(1)]
    prices=[a['t0']+ent*(a['tl']-a['t0']+D(r)*mu) for mu,ent in zip(mus,ents)]
    for cl in ['H','L']:
        tj=a['th'] if cl=='H' else a['tl']
        gains=[q*(a['t0']+ent*(tj-a['t0'])-price)-k*abs(q) for q,ent,price in zip([-1,0,1],ents,prices)]
        print(name,cl,*[enclosure(g,15) for g in gains])
print('Path payoff table: r,t0,tH,tL,gH,gL,Delta,tau,B(prior)')
for r in [r0,r1,r2]:
    a=auction(r);print(str(r),*[str(a[n]) for n in ['t0','th','tl','gh','gl']],str(D(r)),str(tau(r)),str(B(r,pi)))
