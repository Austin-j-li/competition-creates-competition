"""Print independent cash-flow calculations for the W5 referee. No assertions."""
import csv
import sys
from pathlib import Path
import mpmath as mp

mp.mp.dps = 65
D = mp.mpf
ROOT = Path.cwd()
beta = D('0.294655')
u = mp.exp(1) - 1
lam = u * beta / (1 + u * beta)
b = (1 - lam) * beta
b0 = 1 - 2*b - lam
rho = D('0.25')
k = D('0.02')

def fmt(x):
    if isinstance(x, (list, tuple)):
        return '[' + ', '.join(fmt(a) for a in x) + ']'
    if isinstance(x, str):
        return x
    return mp.nstr(x, 19)

def row(name, **values):
    print(name + ' | ' + ' | '.join(key + '=' + fmt(value) for key, value in values.items()))

def auction(components, p='0.5', ell='1', h='10', cost='6'):
    p, ell, h, cost = map(D, (p, ell, h, cost))
    components = [tuple(map(D, c)) for c in components]
    fp = sum(w * max(D(0), min(hi,p)-lo)/(hi-lo) for w,lo,hi in components)
    t0 = p*(1-fp)
    def integral(fn, points, lo, hi):
        xs = sorted(set([lo,hi]+[q for q in points if lo<q<hi]))
        return sum((right-left)*(fn(left)+fn(right))/2 for left,right in zip(xs,xs[1:]))
    def val(theta):
        t = sum(w*integral(lambda R: max(p,min(R,theta)),[p,theta],lo,hi)/(hi-lo) for w,lo,hi in components)
        g = sum(w*integral(lambda R: max(theta-max(p,R),D(0)),[p,theta],lo,hi)/(hi-lo) for w,lo,hi in components)
        win = sum(w*max(D(0),min(hi,theta)-lo)/(hi-lo) for w,lo,hi in components)
        return t,g,win
    tl,gl,wl = val(ell)
    th,gh,wh = val(h)
    delta = th-tl
    gamma = gh-gl
    return dict(t0=t0,tl=tl,th=th,gl=gl,gh=gh,delta=delta,gamma=gamma,tau=(cost-gl)/gamma,wL=tl-t0,fp=fp,p=p,WL=wl,WH=wh,cost=cost)

def uniform(r, **kwargs):
    return auction([(1,0,D(r))],**kwargs)

def post(pi, ratio=u):
    pi=D(pi)
    return pi/(1+(1-pi)*ratio), pi*(1+ratio)/(1+pi*ratio)

def outcome(a, pi, s=None, t=None, lm=lam, bb=b, rr=rho, kk=k, entries=None):
    pi,lm,bb,rr,kk=map(D,(pi,lm,bb,rr,kk))
    s=lm if s is None else D(s)
    t=lm if t is None else D(t)
    fH=[bb,1-2*bb-s,bb+s]
    fL=[bb+t,1-2*bb-t,bb]
    f=[pi*x+(1-pi)*y for x,y in zip(fH,fL)]
    mu=[pi*x/y for x,y in zip(fH,f)]
    e=[rr if x<a['tau'] else D(1) for x in mu] if entries is None else list(map(D,entries))
    A=[a['wL']+a['delta']*x for x in mu]
    prices=[a['t0']+ex*ax for ex,ax in zip(e,A)]
    avg=sum(fx*px for fx,px in zip(f,prices))
    total=sum(fx*ex for fx,ex in zip(f,e))
    ann=sum(fx*ex*(1-ex)*ax for fx,ex,ax in zip(f,e,A))/total
    im=prices[1]-prices[0]
    ip=prices[2]-prices[1]
    T=f[2]*ip-f[0]*im
    UH=e[2]*a['delta']*(1-mu[2])-kk
    UL=e[0]*a['delta']*mu[0]-kk
    covE=sum(fx*xx*ex for fx,xx,ex in zip(f,[-1,0,1],e))-(f[2]-f[0])*total
    win=[a['WL']+(a['WH']-a['WL'])*x for x in mu]
    covW=sum(fx*xx*ex*wx for fx,xx,ex,wx in zip(f,[-1,0,1],e,win))-(f[2]-f[0])*sum(fx*ex*wx for fx,ex,wx in zip(f,e,win))
    return dict(mu=mu,e=e,f=f,P=prices,A=A,avg=avg,entry=total,ann=ann,im=im,ip=ip,T=T,raw=ip-im,spread=ip+im,UH=UH,UL=UL,covE=covE,covW=covW,s=s,t=t)

def show(name,a,pi,**kwargs):
    z=outcome(a,pi,**kwargs)
    row(name,tau=a['tau'],delta=a['delta'],wL=a['wL'],mu=z['mu'],e=z['e'],f=z['f'],P=z['P'],Iplus=z['ip'],Iminus=z['im'],raw=z['raw'],T=z['T'],Pbar=z['avg'],ann=z['ann'],UH=z['UH'],UL=z['UL'])
    return z

def rootstrength(delta):
    return 1+delta+mp.sqrt(delta*delta+2*delta)

def ceiling(pi):
    m,M=post(pi)
    return mp.findroot(lambda r: uniform(r)['tau']-M,(D('1.1'),D('4')))

def dA(r, M=post('.5')[1], p=D('.5')):
    return (1-3*p*p+M*(r*r-1))/(2*r*r)

def registry():
    a1,a2=uniform('3'),uniform('3.6')
    z1,z2=outcome(a1,'.5'),outcome(a2,'.5')
    mm,MM=post('.5')
    rS=rootstrength(k/(rho*mm))
    rC=ceiling('.5')
    ac=uniform(rC)
    entryC=(1-rho)*(ac['wL']+ac['delta']*MM)
    classC=rho*ac['delta']*(MM-mm)
    v=2*b+lam
    priorlo=a1['tau']/(a1['tau']+(1-a1['tau'])*mp.exp(1))
    priorhi=a2['tau']/(a2['tau']+(1-a2['tau'])*mp.exp(1))
    values=dict(lambda_B=lam,b_B=b,b0_B=b0,M_half_B=MM,m_half_B=mm,u_B=u,beta_B=beta,vol_full_B=v,theta_B=lam/v,rS_B=rS,rC_B=rC,delta_rS_B=k/(rho*mm),ba_class_r1_B=rho*a1['delta']*(MM-mm),ba_entry_r1_B=(1-rho)*z1['A'][2],ba_r1_B=z1['spread'],ba_r2_B=z2['spread'],ba_rC_left_B=classC+entryC,ba_rC_right_B=classC,ba_jump_rC_B=entryC,p_neutral_r1_B=z1['P'][1],pbar_r1_B=z1['avg'],pdrop_neutral_r1_B=-z1['T'],pdrop_neutral_r2_B=-z2['T'],cov_entry_r1_B=z1['covE'],evprep_mean_r1_B=z1['ann'],evprep_mean_r2_B=z2['ann'],theta_min_counts_B=3-2/v,theta_max_full_eq_r1_B=1-2*k/(rho*a1['delta']),theta_max_full_eq_r2_B=1-2*k/(rho*a2['delta']),prior_lo_B=priorlo,prior_hi_B=priorhi,theta_lo=2*a1['tau']-1,theta_hi=2*a2['tau']-1)
    rows={r['key']:r for r in csv.DictReader((ROOT/'audit/slot_manuscript_2026_10_23/registry/registry.csv').open())}
    print('REGISTRY: direct auction cash flows; registry is read only for the comparison column')
    for key,value in values.items():
        source=rows[key]
        sv=source['value']
        if '/' in sv:
            n,d=sv.split('/')
            stored=D(n)/D(d)
        else:
            stored=D(sv)
        row(key,recomputed=value,display=source['display'],recomputed_minus_stored=value-stored)
    row('benchmark extra',fplus=v/2,A_M=z1['A'][2],Iminus=z1['im'],Iplus=z1['ip'],threshold_r1=a1['tau'],threshold_r2=a2['tau'],forcing_margin_r1=rho*a1['delta']*mm-k,forcing_margin_r2=rho*a2['delta']*mm-k,min_cost_margin=D(6)-(uniform('1.2')['gl']+D('.5')*uniform('1.2')['gamma']),cost_margin_r1=6-(a1['gl']+D('.5')*a1['gamma']),dA_path_min=dA(D('1.2')),dA_full_inf=dA(rS),Freserve_rS=D('.5')/rS,Freserve_rC=D('.5')/rC,band_fraction_below_half=(D('.5')-priorlo)/(priorhi-priorlo),lowvalue_margin=1-mp.sqrt(3)/2,reserve_margin=1/mp.sqrt(3)-D('.5'))

def cases():
    print('GENERAL PRIOR FULL-ORDER CASES')
    for pi,r in [('.3','3'),('.4','3'),('.4','3.6'),('.5','3'),('.6','3'),('.6','3.6'),('.7','2'),('.7','2.5'),('.75','3'),('.9','3'),('.7','2.88'),('.7','2.89')]:
        show('full pi='+pi+' r='+r,uniform(r),pi)
    for pi in ['.3','.4','.45','.4679','.5','.55','.6','.7']:
        mm,MM=post(pi)
        row('threshold pi='+pi,M=MM,m=mm,rS=rootstrength(k/(rho*min(mm,1-MM))),relative_naive_bias=u*(1-2*D(pi))/(1+u*D(pi)),posteriorgap=MM-mm)
    for pi in ['.4','.45','.5']:
        row('ceiling pi='+pi,rC=ceiling(pi))
    show('PURCHASES ONLY pi=.3 r=2',uniform('2'),'.3',t=0)
    show('not-equilibrium purchases-only pi=.5 r=6',uniform('6'),'.5',t=0)
    a=uniform('2.3')
    show('VISIBLE full pi=.6 r=2.3',a,'.6')
    sh=b/D('.6')*((1-D('.6'))*rho*a['delta']/k-1)
    show('HIDDEN mixed pi=.6 r=2.3',a,'.6',s=sh,entries=[rho]*3)
    row('hidden full-order H margin',margin=rho*a['delta']*(1-post('.6')[1])-k,s=sh)
    a=uniform('3',cost=uniform('3')['gl']+D('.5')*uniform('3')['gamma'])
    # Entry at the prior is free at the CM tie. H and L strictly choose full orders.
    for e0 in ['.25','.625','.9','1']:
        show('CM prior tie e0='+e0,a,'.5',entries=[rho,D(e0),1])
    a=uniform('3',cost=uniform('3')['gl']+post('.6')[1]*uniform('3')['gamma'])
    for ep in ['.251','1']:
        show('CM top tie pi=.6 eplus='+ep,a,'.6',entries=[rho,rho,D(ep)])
    show('always-entry no-trade pi=.7 r=1.2',uniform('1.2'),'.7',s=0,t=0)
    show('false negative high rho',uniform('9',cost='5.214'),'.9',lm=D('20')*beta/(1+20*beta),bb=beta/(1+20*beta),rr='.8',kk='.01')

def identification():
    print('IDENTIFICATION AND SAME-COUNT FAMILIES')
    v=2*b+lam
    d=lam*D('.2')
    for pi in ['.56','.6','.65']:
        pp=D(pi)
        ll=d/(2*pp-1)
        bb=(v-ll)/2
        mm,MM=post(pi,ll/bb)
        row('same-counts pi='+pi,lam=ll,beta=bb/(1-ll),force_r3=rho*uniform(3)['delta']*min(mm,1-MM)-k,force_r36=rho*uniform('3.6')['delta']*min(mm,1-MM)-k,M=MM)
        for r in ['3','3.6']:
            show('samecounts '+pi+' r='+r,uniform(r),pi,lm=ll,bb=bb)
    for pi in ['.6','.7']:
        dd=lam*(2*D(pi)-1)
        row('slot-only prior interval true='+pi,lower=(1+dd/v)/2,upper=(1+dd/(3*v-2))/2,lambda_lower=3*v-2,theta_lower=3-2/v)
    for pi in ['.3','.4','.45','.5','.55','.6','.62','.7']:
        for r in ['2.5','3','3.6','5']:
            a=uniform(r)
            z=outcome(a,pi)
            ff=z['f']; dd=ff[2]-ff[0]
            Q=ff[0]*z['im']/(rho*a['delta'])
            lr=2*Q+mp.sqrt(4*Q*Q+dd*dd)
            pp=(1+dd/lr)/2
            row('inverse pi='+pi+' r='+r,low_entry=z['e'][0],zero_entry=z['e'][1],UH=z['UH'],UL=z['UL'],lambda_recovered=lr,pi_recovered=pp,beta_recovered=(v-lr)/(2*(1-lr)))
    for pi,r,change in [('.6','1.4','.05'),('.5','1.45','.01'),('.55','1.45','.01')]:
        pp=D(pi); a=uniform(r)
        sr=b/pp*((1-pp)*a['delta']/k-1)
        for ll in [lam,lam-D(change)]:
            z=show('R pi='+pi+' r='+r+' lambda='+fmt(ll),a,pi,s=sr,t=0,lm=ll,bb=b)
            row('R extras',s=sr,beta=b/(1-ll),sigmaH=sr/ll,d=z['f'][2]-z['f'][0],v=z['f'][2]+z['f'][0],quiet_sale=z['avg']-z['P'][0])
    aa=uniform(rootstrength(D('.24')))
    row('incentive boundary singleton',r=rootstrength(D('.24')),v=D('.8'),d=D('.08'),slot_lower_lambda=D('.4'))
    for ll in ['.4','.41','.5']:
        ll=D(ll); bb=(D('.8')-ll)/2; pp=(1+D('.08')/ll)/2
        show('same count boundary lambda='+fmt(ll),aa,pp,lm=ll,bb=bb)

def trends():
    print('FOSD COUNTEREXAMPLES')
    M=post('.5')[1]
    paths={
      'solver_A':lambda s:[('.1',D('.3')+D('.3')*s,D('.4')+D('.3')*s),('.9',D('1.5')+D('.01')*s,D('1.7')+D('.01')*s)],
      'takeover_mild':lambda s:[('.5',D('.1')+D('.2')*s,D('.7')+D('.2')*s),('.5',D('1.5')+D('.02')*s,D('2.5')+D('.02')*s)],
      'solver_F_extreme':lambda s:[('.9',D('.5')*s,D('.5')+D('.5')*s),('.1',D('9'),D('10'))],
      'solver_F_strict':lambda s:[('.9',D('.5')*s,D('.5')+D('.5')*s),('.1',D('9')+D('.02')*s,D('10')+D('.02')*s)]
    }
    for name,fun in paths.items():
        for ss in ['0','.5','1']:
            s=D(ss); a=auction(fun(s)); z=outcome(a,'.5')
            row(name+' s='+ss,fp=a['fp'],delta=a['delta'],tau=a['tau'],wL=a['wL'],A_M=z['A'][2],Q_M=z['A'][2]-D('.5')*a['fp'],entry_component=(1-rho)*z['A'][2],class_component=rho*a['delta']*(2*M-1),Iplus=z['ip'],spread=z['spread'],forcing_margin=rho*a['delta']*post('.5')[0]-k,Bprior=a['gl']+a['gamma']/2,BM_minus_cost=a['gl']+M*a['gamma']-6)
    pp=D('.95'); kk=D('.004')
    row('highreserve turning points',rS=rootstrength(kk/(rho*post('.5')[0])),rA_turn=mp.sqrt(1+(3*pp*pp-1)/M),rI_turn=mp.sqrt(1+(1-rho)*(3*pp*pp-1)/((1-rho)*M+rho*(M-D('.5')))),rSprice_turn=mp.sqrt(1+(1-rho)*(3*pp*pp-1)/((1-rho)*M+rho*(2*M-1))))
    for rr in ['1.5','1.71','1.76','1.83']:
        show('p=.95 r='+rr,uniform(rr,p=pp),'.5',kk=kk)
    for ratio in [u,D(5),D(20)]:
        f=lambda pi:post(pi,ratio)[1]/(2*pi-post(pi,ratio)[0])
        pp=mp.findroot(lambda pi:mp.diff(f,pi),D('.8'))
        row('rho sufficient bound ratio='+fmt(ratio),pi_at_min=pp,min=f(pp))
    # Exact differentiable mild path: wL=13/30-s/20+s^2/60; delta=.5+.01s.
    for s in [D(0),D(1)]:
        derivative=-D(1)/20+s/30+M/100
        row('mild path derivative s='+fmt(s),dA=derivative,dSpread=rho*(2*M-1)/100+(1-rho)*derivative,dIplus=rho*(M-D('.5'))/100+(1-rho)*derivative)

def magnitudes():
    M=post('.5')[1]
    for pp in ['.3','.4679']:
        pi=D(pp); mm,MM=post(pi)
        for rr in ['3','3.6']:
            aa=uniform(rr)
            bias=rho*aa['delta']*(MM+mm-2*pi)
            row('bias pi='+pp+' r='+rr,versus_sale=bias/(rho*aa['delta']*(pi-mm)),versus_class=bias/(rho*aa['delta']*(MM-mm)),versus_hypothetical_entry=bias/((1-rho)*(aa['wL']+aa['delta']*MM)))
    low=mp.findroot(lambda pi:rho*uniform('3.6')['delta']*post(pi)[0]-k,D('.2'))
    pi=low; a=uniform('3.6'); mm,MM=post(pi)
    row('max false gap within forced domain at endpoint',prior_boundary=low,ratio=rho*a['delta']*(MM+mm-2*pi)/((1-rho)*(a['wL']+a['delta']*MM)))
    row('auctionfree limit',ratio=(u/(1+u))**2/3)
    row('sale deters interval pi=.7',lower=rootstrength(k/(rho*post('.7')[0])),upper=mp.findroot(lambda r:uniform(r)['tau']-D('.7'),D('2.9')))

def edges():
    print('ADDITIONAL DOMAIN AND NUMERICAL QUALIFICATIONS')
    for pi in ['.203','.21']:
        a=uniform('3.6'); pp=D(pi); mm,MM=post(pp)
        row('false-gap size pi='+pi,forcing_margin=rho*a['delta']*min(mm,1-MM)-k,ratio=rho*a['delta']*(MM+mm-2*pp)/((1-rho)*(a['wL']+a['delta']*MM)))
    a=uniform('3'); z=outcome(a,'.5')
    es=(z['f'][2]*z['A'][2]+rho*z['f'][0]*z['A'][0])/(z['f'][2]*z['A'][2]+z['f'][0]*z['A'][0])
    row('CM ties',top_tie_cost=a['gl']+post('.6')[1]*a['gamma'],prior_tie_cost=a['gl']+a['gamma']/2,zero_statistic_e0=es)
    row('extended benchmark infima',cost_margin=6-(uniform(1)['gl']+uniform(1)['gamma']/2),prior_threshold_margin=uniform(1)['tau']-D('.5'))
    v=2*b+lam; d=lam/5
    ll=d/D('.1'); bb=(v-ll)/2
    show('slot-feasible but not equilibrium pi=.55',a,'.55',lm=ll,bb=bb)
    mmin=k/(rho*a['delta']); aa=(v-d)*(1-2*mmin)
    llmax=(aa+mp.sqrt(aa*aa+4*d*v))/2
    row('r=3 full-trade samecounts restriction',lambda_max=llmax,prior_min=(1+d/llmax)/2)
    a=uniform('2.3'); mm,MM=post('.6')
    row('unique full trade below forcing cutoff',low_all_candidate_margin=rho*a['delta']*mm-k,high_below_threshold_margin=rho*a['delta']*(1-a['tau'])-k,high_above_threshold_margin=a['delta']*(1-MM)-k)
    # The nonzero-order mean price is required to weight impacts consistently.
    row('wL-zero illustration',recruitment_term=D('.2')*post('.9',D(20))[1],bias_abs=D('.8')*(D('1.8')-sum(post('.9',D(20)))))
    for pi in ['.3','.4','.6','.7']:
        z=outcome(uniform('3.6'),pi); pp=D(pi)
        row('covariance pi='+pi,cov_entry=z['covE'],formula_entry=(z['e'][2]-rho)*z['f'][2]*(1-(z['f'][2]-z['f'][0])),cov_winner=z['covW'],floor_only_winner=2*rho*pp*(1-pp)*lam*(1-D(1)/D('3.6')))

if __name__ == '__main__':
    tasks={'registry':registry,'cases':cases,'identification':identification,'trends':trends,'magnitudes':magnitudes,'edges':edges}
    for name in sys.argv[1:] or tasks:
        tasks[name]()
