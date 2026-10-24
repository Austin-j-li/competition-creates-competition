"""Read-only arithmetic worksheet. Compute values and print differences; no assertions."""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial
import csv, io, re
from mpmath import iv
iv.dps=85
ROOT=Path('/Users/austinli/Projects/competition-creates-competition')
OUT=Path('scripts/core_2')
def I(x):
    if hasattr(x,'_mpi_'): return x
    x=Q(x)
    return iv.mpf(x.numerator)/iv.mpf(x.denominator)
def ends(v):
    out=[]
    for sign,man,exp,bc in I(v)._mpi_:
        out.append((-1 if sign else 1)*Q(man)*Q(2)**exp)
    return out
def fixed(q,n=18,mode='nearest'):
    q=Q(q); s=10**n
    if mode=='down': z=(q*s).__floor__()
    elif mode=='up': z=-(-q*s).__floor__()
    else: z=(abs(q)*s+Q(1,2)).__floor__() * (-1 if q<0 else 1)
    sign='-' if z<0 else ''; z=str(abs(z)).rjust(n+1,'0')
    return sign+(z if not n else z[:-n]+'.'+z[-n:])
def enc(v,n=18):
    lo,hi=ends(v);return '['+fixed(lo,n,'down')+', '+fixed(hi,n,'up')+']'
def bisect(f,lo=Q(6,5),hi=Q(18,5)):
    while hi-lo>Q(1,10**70):
        mid=(lo+hi)/2
        if f(mid)>0:hi=mid
        elif f(mid)<0:lo=mid
        else:lo=hi=mid
    return lo,hi

def interval(br):return iv.mpf([I(br[0]).a,I(br[1]).b])
h,l,p,rho,c,k,pi=map(Q,['10','1','1/2','1/4','6','1/50','1/2'])
r0,r1,r2=map(Q,['6/5','3','18/5'])
beta=Q('0.294655')
e_lo=sum((Q(1,factorial(n)) for n in range(111)),Q(0))
e_hi=e_lo+Q(112,111*factorial(111))
E=interval((e_lo,e_hi));u=E-1
lam=u*I(beta)/(1+u*I(beta));b=I(beta)/(1+u*I(beta));b0=(1-lam)*(1-2*I(beta))
M=E/(1+E);m=1/(1+E)
def A(r):
    return {'t0':p*(1-p/r),'th':r/2+p*p/(2*r),'tl':l-(l*l-p*p)/(2*r),'gh':h-r/2-p*p/(2*r),'gl':(l*l-p*p)/(2*r)}
def D(r):return (r-l)**2/(2*r)
def tau(r):return (2*r*c-l*l+p*p)/(2*r*h-r*r-l*l)
def J(r):return D(r)*(1-tau(r))
def B(r,mu):
    a=A(r)
    if hasattr(mu,'_mpi_'):return I(a['gl'])+mu*I(a['gh']-a['gl'])
    return a['gl']+mu*(a['gh']-a['gl'])
def rootD(d):d=I(d);return 1+d+iv.sqrt(d*d+2*d)
def ti(r):return (2*r*I(c)-I(l*l-p*p))/(2*r*I(h)-r*r-I(l*l))
rAb=bisect(lambda r:J(r)-k);rJb=bisect(lambda r:rho*J(r)-k);rstarb=bisect(lambda r:rho*D(r)*tau(r)-k)
rA=interval(rAb);rJ=interval(rJb);rstar=interval(rstarb)
tA=interval((tau(rAb[0]),tau(rAb[1])));pimax=interval((tau(rstarb[0]),tau(rstarb[1])))
Ds=interval((D(rstarb[0]),D(rstarb[1])))
rF=rootD(I(k)/m);rS=rootD(I(k/rho)/m);rN=rootD(2*k/rho)
z=M*I(h)-I(c);rC=(z+iv.sqrt(z*z+M*((1-M)*I(l*l)-I(p*p))))/M
entry=I(rho)+I(1-rho)*(b+lam/2);eH=I(rho)+I(1-rho)*(b+lam);eL=I(rho)+I(1-rho)*b
v={}
def put(key,value):v[key]=value
for nm,x in dict(h=h,ell=l,p=p,rho=rho,cH=c,k=k,pi=pi,r0=r0,r1=r1,r2=r2).items():put('prim_'+nm,x)
for nm,x in dict(u_B=u,beta_B=beta,lambda_B=lam,b_B=b,b0_B=b0,M_half_B=M,m_half_B=m,b_plus_lambda_B=b+lam,rA=rA,rJ=rJ,rstar=rstar,rN=rN,rF_B=rF,rS_B=rS,rC_B=rC,piA_hi=tA,pimax=pimax).items():put(nm,x)
for name,r in [('r0',r0),('r1',r1),('r2',r2)]:
    for key,val in A(r).items():put('p2_base_'+name+'_'+key,val)
    for suffix in ('','_frac'):put('tau_'+name+suffix,tau(r))
    put('Delta_'+name,D(r));put('Bprior_'+name+('_B' if name=='r1' else ''),B(r,pi))
    post=[I(pi)]*3 if name=='r0' else [m,I(pi),M]
    for suffix,val in zip(['minus','zero','plus'],post):put('p2_base_'+name+'_mu_'+suffix,val)
    a=A(r); prices=[I(a['t0'])+ee*(I(a['tl']-a['t0'])+I(D(r))*mu) for mu,ee in zip(post,[I(rho),I(rho),I(1) if name=='r1' else I(rho)])]
    if name=='r0':put('price_r0',prices[0])
    else:
        for suffix,val in zip(['m1','0','p1'],prices):put('price_'+name+'_'+suffix+'_B',val)
    put('p4_base_'+name+'_proceeds',I(a['t0'])+(eH*I(a['th']-a['t0'])+eL*I(a['tl']-a['t0']))/2 if name=='r1' else prices[1])
for nm,x in dict(entry_r0=rho,entry_r1_B=entry,entry_r2=rho,own_r0=pi*rho,own_r1_B=eH/2,own_r2_B=pi*rho).items():put(nm,x)
for name,r in [('r0',r0),('r1',r1)]:
    a=A(r)
    for scenario in ('frozen','hidden'):
        eh,el=(eH,eL) if scenario=='frozen' else (I(rho),I(rho))
        pref='p4_'+scenario+'_'+name+'_'
        put(pref+'entry',(eh+el)/2);put(pref+'own',eh/2)
        put(pref+'proceeds',I(a['t0'])+(eh*I(a['th']-a['t0'])+el*I(a['tl']-a['t0']))/2)
put('p4_control_crossing_r0_r1',Q(0));put('p4_control_crossing_r1_r2',entry-I(rho))
put('ba_share_r1_B',I(1-rho)*(I(A(r1)['tl']-A(r1)['t0'])+I(D(r1))*M)/(v['price_r1_p1_B']-v['price_r1_m1_B']))
u_lo=Q(82,59);u_hi=Q(2686,1559);uk=Q(19,3)
for name,val in [('u_lo',u_lo),('u_hi',u_hi),('M_lo',tau(r1)),('M_hi',tau(r2))]:
    put(name,val);put(name+'_frac',val)
put('u_kstrong_frac',uk)
for suffix,beta2 in [('B',beta),('third',Q(1,3))]:
    put('lambda_lo_'+suffix,u_lo*beta2/(1+u_lo*beta2));put('lambda_hi_'+suffix,u_hi*beta2/(1+u_hi*beta2))
plo=I(tau(r1))/(I(tau(r1))+(1-I(tau(r1)))*E);phi=I(tau(r2))/(I(tau(r2))+(1-I(tau(r2)))*E)
palo=tA/(tA+(1-tA)*E)
for nm,x in dict(prior_lo_B=plo,prior_hi_B=phi,prior_ii_hi=tau(r0),prior_kappa_lo_B=3*E/(22+3*E),prior_kappa_hi_B=22/(22+3*E),p2_prior_trade_lo=E/(9+E),p2_prior_trade_hi=9/(9+E),piA_lo_B=palo).items():put(nm,x)
mg=dict(weakcost_B=c-B(r0,pi),recruit_B=B(r1,M)-I(c),recruit_post_B=M-I(tau(r1)),kweak_B=k-D(r0),kstrong_B=I(rho*D(r1))*m-I(k),return_B=I(c)-B(r2,M),return_post_B=I(tau(r2))-M,implied_prior_r1=c-B(r1,pi),implied_prior_r2=c-B(r2,pi),kstrong2_B=I(rho*D(r2))*m-I(k),u_lo_B=u-I(u_lo),u_hi_B=I(u_hi)-u,u_kstrong_B=I(uk)-u,lambda_lo_B=lam-I(v['lambda_lo_B']),lambda_hi_B=I(v['lambda_hi_B'])-lam,prior_lo_B=I(pi)-plo,prior_hi_B=phi-I(pi),beta_B=Q(1,3)-beta,p4_ownership_rise_B=eH-I(rho),p2_bplus_B=b+lam-I(pi),Delta_pos_B_frac=D(r0),gHgL_B_frac=A(r2)['gh']-A(r2)['gl'],tau_r0_half=tau(r0)-pi,J_r0_B_frac=k-J(r0),rhoJ_r1_B_frac=rho*J(r1)-k,rhoJ_r2_B=rho*J(r2)-k,rhoJ_2_B_frac=rho*J(Q(2))-k,tau_r2_3q_B_frac=Q(3,4)-tau(r2),tau_rN_half_B=ti(rN)-I(pi),piA_lo_B=I(pi)-palo,piA_hi=tA-I(pi),tauA_3q_B=I(Q(3,4))-tA,pimax_tauA_B=pimax-tA)
for name,x in mg.items():put('margin_'+name,x)
for nm,x in [('rA_r0',rA-I(r0)),('rF_rA',rF-rA),('rN_rF',rN-rF),('rJ_rN',rJ-rN),('rS_rJ',rS-rJ),('r1_rS',I(r1)-rS),('rC_r1',rC-I(r1)),('r2_rC',I(r2)-rC)]:put('gap_'+nm+'_B',x)
Mpm=pimax*E/(pimax*E+1-pimax)
put('M_pimax_B',Mpm);put('mu0_pimax_B',pimax*b0/(pimax*b0+(1-pimax)*(b0+lam)))
put('margin_cmend_B',Ds*(1-Mpm)-I(k));put('entry_cmend_B',I(rho)+I(1-rho)*(b+pimax*lam))
put('entry_rA_B',I(rho)+I(1-rho)*b/(2*(1-tA)))
for suffix,r in [('r140',Q(7,5)),('r145',Q(29,20)),('r155',Q(31,20)),('r160',Q(8,5)),('r165',Q(33,20))]:
    put('str_'+suffix,r)
    put('entry_mb_'+suffix+'_B',I(rho)+I((1-rho)*D(r)/(2*k))*b)
    put('entry_th_'+suffix+'_B',I(rho)+b*I((k-rho*J(r))/(2*D(r)*(1-tau(r))**2)))
for nm,x in dict(J_r0=J(r0),rhoJ_r1=rho*J(r1),rhoJ_r2=rho*J(r2),B_r0_half=B(r0,pi),Delta_r155_frac=D(Q(31,20)),nec_cH=Q(47,10),nec_r2=Q(8),nec_entry_r0=Q(1),nec_margin_kweak=k-D(r0),nec_margin_prior_r1=Q(47,10)-B(r1,pi),nec_margin_recruit_B=B(r1,M)-I(Q(47,10)),nec_margin_kstrong_B=mg['kstrong_B'],nec_margin_return_B=I(Q(47,10))-B(Q(8),M),nec_margin_weakcost=Q(47,10)-B(r0,pi)).items():put(nm,x)
qj=[-1,40,-614,-12,743,-160,4]
put('QJ_r0',sum(Q(c)*r0**i for i,c in enumerate(qj)))
# Independent formal polynomial operations for the derivatives and Sturm variations.
def trim(a):
    a=list(map(Q,a))
    while len(a)>1 and a[-1]==0:a.pop()
    return a
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def sub(a,b):return add(a,[-x for x in b])
def der(a):return trim([i*a[i] for i in range(1,len(a))] or [0])
def val(a,x):
    z=Q(0)
    for c in a[::-1]:z=z*x+c
    return z
def rem(a,b):
    a=trim(a);b=trim(b)
    while len(a)>=len(b) and a!=[0]:
        a=sub(a,[Q(0)]*(len(a)-len(b))+[z*a[-1]/b[-1] for z in b])
    return a
def sturm(a):
    chain=[trim(a),der(a)]
    while chain[-1]!=[0]:
        z=rem(chain[-2],chain[-1])
        if z==[0]:break
        chain.append([-x for x in z])
    return chain
def variations(chain,x):
    z=[val(a,x) for a in chain];z=[a>0 for a in z if a]
    return sum(a!=b for a,b in zip(z,z[1:]))
nt=[-Q(3,4),12];dt=[-1,20,-1];nd=[1,-2,1];dd=[0,2];nmt=sub(dt,nt)
polys={}
for nm,n,d in [('J',mul(nd,nmt),mul(dd,dt)),('D(1-tau)^2',mul(nd,mul(nmt,nmt)),mul(dd,mul(dt,dt)))]:
    polys[nm]=sub(mul(der(n),d),mul(n,der(d)))
print('Euler rational enclosure:',enc(E,70))
print('Series remainder upper bound:',Q(112,111*factorial(111)))
for nm,poly in polys.items():
    scale=Q(2) if nm=='J' else Q(8)
    print(nm,'integer coefficients ascending:',[str(z*scale) for z in poly])
    chain=sturm(poly);hi=r2 if nm=='J' else Q(2)
    print(nm,'endpoint variations:',variations(chain,r0),variations(chain,hi),'left value:',val(poly,r0),'interval:',r0,hi)
    if nm!='J': print(nm,'variations at full path end:',variations(chain,r2))
for nm,br,fn in [('rA',rAb,lambda r:J(r)-k),('rJ',rJb,lambda r:rho*J(r)-k),('rstar',rstarb,lambda r:rho*D(r)*tau(r)-k)]:
    print(nm,'root bracket',enc(interval(br)), 'endpoint signs', '-' if fn(br[0])<0 else '0', '+' if fn(br[1])>0 else '0','rational width',br[1]-br[0])
raw=(ROOT/'audit/slot_manuscript_2026_10_23/registry/registry.csv').read_text().replace('\\r\\n','\n')
rows={r['key']:r for r in csv.DictReader(io.StringIO(raw))}
# Six introduction previews: recompute their numbers without auditing the research theorem.
research_a=Q(rows['res_a']['value'])
for suffix,r in [('r155',Q(31,20)),('r160',Q(8,5)),('r165',Q(33,20))]:
    # The arrival rate changes against the continuation prices. Its interior FOC is
    # D*b/(2*(2*b+lambda))-k/2 = a*lambda, with b=beta*(1-lambda).
    def research_eq(z):
        return (k+2*research_a*z)*(2*beta*(1-z)+z)-D(r)*beta*(1-z)
    br=bisect(research_eq,Q(0),Q(1))
    z=interval(br)
    put('res_lambda_'+suffix,z)
    put('res_entry_'+suffix,I(rho)+I(1-rho)*(I(beta)*(1-z)+z/2))
    print('Research preview',suffix,'rate bracket',enc(z),'equation signs',research_eq(br[0])<0,research_eq(br[1])>0)
files=[ROOT/'slot/manuscript/main.tex',*sorted((ROOT/'slot/manuscript/sections').glob('0[1-4]_*.tex')),*[next((ROOT/'slot/manuscript/appendix').glob(f'A{i}_*.tex')) for i in (1,2,3,4)]]
keys=set()
for f in files:keys.update(re.findall(r'\\reg\{([^}]+)\}',re.sub(r'%[^\n]*','',f.read_text())))
a9=(ROOT/'slot/manuscript/appendix/A9_parameters.tex').read_text().splitlines()
keys.update(re.findall(r'\\reg\{([^}]+)\}','\n'.join(a9[:28]+a9[90:132])))
macros=dict(re.findall(r'\\csname reg@([^\\]+)\\endcsname\{([^}]*)\}',(ROOT/'slot/manuscript/numbers.tex').read_text()))
print('Registry keys in scope:',len(keys),'computed:',len(keys&v.keys()),'uncomputed:',sorted(keys-v.keys()))
print('Macro/registry display differences:',[(key,macros.get(key),rows[key]['display']) for key in sorted(keys) if macros.get(key)!=rows[key]['display']])
records=[]
for key in sorted(keys&v.keys()):
    display=rows[key]['display'];x=I(v[key]);scaled=x*100 if display.endswith('\\%') else x
    d=display.replace('\\%','');lo,hi=ends(scaled)
    if '/' in d or '.' not in d:
        z=Q(d);delta=enc(scaled-I(z),12);render='exact='+str(z)
    else:
        n=len(d.split('.')[1]);render=fixed(lo,n)+' / '+fixed(hi,n);delta=enc(scaled-I(Q(d)),12)
    records.append({'key':key,'display':display,'computed_enclosure':enc(x,24),'rounded_endpoints':render,'difference_from_display':delta})
with (OUT/'recomputed_values.csv').open('w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print('Independent computations and signed display differences:')
for row in records: print(row['key'],row['display'],row['computed_enclosure'],row['rounded_endpoints'])
print('Research cost declaration:',rows['res_a'])
print('Fixed-tuple gross returns and net payoffs at the three benchmark strengths:')
for name,r in [('r0',r0),('r1',r1),('r2',r2)]:
    mm,pp=(I(pi),I(pi)) if name=='r0' else (m,M)
    ep=I(1) if name=='r1' else I(rho)
    kh=ep*I(D(r))*(1-pp);kl=I(rho*D(r))*mm
    uhminus=-I(rho*D(r))*(1-mm)-I(k)
    ulplus=-ep*I(D(r))*pp-I(k)
    print(name,'K_H-k',enc(kh-I(k)),'K_L-k',enc(kl-I(k)),'U_H(-1)',enc(uhminus),'U_L(1)',enc(ulplus),'abstention',0)
print('Boundary u=82/59: universal correct-order upper net return at r0=',D(r0)-k)
print('Boundary u=82/59: proposed full-order H purchase net return at r0=',D(r0)*(1-tau(r1))-k)
print('Notation collision at r1: target t_L=',A(r1)['tl'],'sale rate t_L=',enc(lam))
