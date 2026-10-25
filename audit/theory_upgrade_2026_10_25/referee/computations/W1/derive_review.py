from math import exp, sqrt, log
from fractions import Fraction as Q

p, h, ell, cost, rho, k, pi = .5, 10., 1., 6., .25, .02, .5
beta = .294655
u = exp(1) - 1
lam = u * beta / (1 + u * beta)
b = (1-lam)*beta
M = (1+u)/(2+u)
d = h-ell

def show(label, **values):
    print(label + ': ' + ', '.join(f'{key}={value:.12f}' if isinstance(value, (int,float)) else f'{key}={value}' for key,value in values.items()))

def bisect(f, left, right):
    fl = f(left)
    for unused in range(90):
        mid = (left+right)/2
        fm = f(mid)
        if fl*fm <= 0:
            right = mid
        else:
            left, fl = mid, fm
    return (left+right)/2

def inv_delta(x):
    return ell+x+sqrt(x*x+2*ell*x)

def bench(r, c=cost, low_mean=ell, low_second=ell**2, high_mean=h):
    D = r/2-low_mean+low_second/(2*r)
    gh = high_mean-r/2-p*p/(2*r)
    gl = (low_second-p*p)/(2*r)
    gam = gh-gl
    tau = (c-gl)/gam
    X = gh-c
    Dp = .5-low_second/(2*r*r)
    gp = -.5+p*p/(2*r*r)
    J = D*X/gam
    Jp = ((high_mean-low_mean)*Dp*X+D*gam*gp)/(gam*gam)
    eta = -gp/Dp
    Zp = Dp*(1-tau)/gam*((high_mean-low_mean)*(1-tau)-D*(1+tau)-2*D*(eta-1))
    return dict(Delta=D,gH=gh,gL=gl,gamma=gam,tau=tau,X=X,J=J,Dp=Dp,gp=gp,Jp=Jp,eta=eta,Zp=Zp)

def uniform_payoffs(lo, hi, value, reserve=p):
    cuts = sorted(set([lo,hi]+[x for x in [reserve,value] if lo<x<hi]))
    target, profit = 0., 0.
    for x,y in zip(cuts,cuts[1:]):
        mid=(x+y)/2
        target += (y-x)*max(reserve,min(mid,value))/(hi-lo)
        profit += (y-x)*max(value-max(reserve,mid),0)/(hi-lo)
    return target,profit

def mix_payoffs(components, c=cost):
    th,tl,gh,gl=0.,0.,0.,0.
    for weight,lo,hi in components:
        th1,gh1=uniform_payoffs(lo,hi,h)
        tl1,gl1=uniform_payoffs(lo,hi,ell)
        th+=weight*th1; gh+=weight*gh1
        tl+=weight*tl1; gl+=weight*gl1
    D=th-tl; gam=gh-gl; tau=(c-gl)/gam; J=D*(1-tau)
    return dict(Delta=D,gH=gh,gL=gl,gamma=gam,tau=tau,J=J,Nreturn=rho*D/2)

def informative(v, c=cost, slotM=M, trading=k):
    D=v['Delta']; tau=v['tau']
    s=min(lam,b/pi*((1-pi)*D/trading-1))
    post=pi*(b+s)/(b+pi*s)
    return dict(rate=s,posterior=post,threshold=tau,purchase_return=D*(1-post),sale_return=rho*D*pi,entry=rho+(1-rho)*(b+pi*s))

print('BENCHMARK: exact declared inputs, direct auction formulas')
show('slot',beta=beta,lambda_=lam,b=b,M=M,Delta_full=k/(1-M),Delta_no_trade=2*k/rho,universal_prior_cap=1/(1+rho))
rA=bisect(lambda r:bench(r)['J']-k,1.2,3.6)
rF=inv_delta(k/(1-M)); rN=inv_delta(2*k/rho)
rC=bisect(lambda r:bench(r)['tau']-M,1.2,3.6)
rJ=bisect(lambda r:rho*bench(r)['J']-k,1.2,3.6)
rstar=bisect(lambda r:rho*bench(r)['Delta']*bench(r)['tau']-k,1.2,3.6)
show('thresholds',rA=rA,rF=rF,rN=rN,rC=rC,rJ=rJ,rstar=rstar,pi_max=bench(rstar)['tau'])
for r in [1.2,rA,rF,rN,3.6]:
    v=bench(r)
    show('benchmark '+str(r),**v)
    direct=mix_payoffs([(1,0,r)])
    show('direct auction integral '+str(r),**direct)
    show('analytic margins '+str(r), product_margin=v['X']-v['eta']*v['Delta'], product2_margin=v['X']-2*v['eta']*v['Delta'], erosion_ratio=v['X']/(v['eta']*v['Delta']), J_ratio=d*(1-v['tau'])/(v['eta']*v['Delta']), Z_sign_margin=d*(1-v['tau'])-v['Delta']*(1+v['tau'])-2*v['Delta']*(v['eta']-1))
    if r in [rA,rF,rN]:
        show('informative branch '+str(r),**informative(v))
vA=bench(rA); v2=bench(3.6)
piLo=vA['tau']/(vA['tau']+(1-vA['tau'])*(1+u))
show('prior margins',feasibility=1-rho/2-vA['tau'],tauA_below_1_minus_rho=1-rho-vA['tau'],piLo=piLo,start_lo=1-vA['tau']-rho*max(piLo,1-piLo),start_hi=1-vA['tau']-rho*vA['tau'],tauN_ceiling=M-bench(rN)['tau'])
show('uniform sufficient and exact cost bounds',coverage=h-3.6-cost,weaker_bound=h-3.6+ell/2-p*p/(2*3.6),weaker_slack=h-3.6+ell/2-p*p/(2*3.6)-cost,exact_bound=v2['gH']-v2['Delta']*v2['gamma']*v2['eta']/d)
for r in [1.2,3.6]:
    show('higher cost 6.6 '+str(r),Jp=bench(r,c=6.6)['Jp'])
    lv,uv=.75,1.1
    vm=(lv+uv)/2; m2=(lv*lv+lv*uv+uv*uv)/3
    show('dispersed classes '+str(r),**bench(r,low_mean=vm,low_second=m2,high_mean=10))
    tl,gl=tuple(sum(weight*uniform_payoffs(0,r,val)[j] for weight,val in [(1/6,lv),(4/6,vm),(1/6,uv)]) for j in [0,1])
    th,gh=tuple(sum(weight*uniform_payoffs(0,r,val)[j] for weight,val in [(1/6,9),(4/6,10),(1/6,11)]) for j in [0,1])
    show('dispersed direct integrals '+str(r),Delta=th-tl,gH=gh,gL=gl,J=(th-tl)*(gh-cost)/(gh-gl))
L=119/44
show('solver_A finite difference bound',L=L,ceiling=d*rho*rho/(4*L),exact_ceiling=str(Q(99,1904)),cost_slack=d*rho*rho/(4*L)-k,factor=d*rho*rho/(4*L*k),margin=d*rho*rho/4-k*L)
Lsmall=bench(1.01)['eta']
show('extended weak endpoint',L=Lsmall,ceiling=d*rho*rho/(4*Lsmall))
show('boundary comparison',AkDp=d*k*vA['Dp'],minus_D2gp=-vA['Delta']**2*vA['gp'],B=d*k*vA['Dp']+vA['Delta']**2*vA['gp'],eta=vA['eta'],squared=d*(1-vA['tau'])**2,k_eta=k*vA['eta'],factor=d*(1-vA['tau'])**2/(k*vA['eta']))
rlo=inv_delta(k/(1-pi)); rlo_all=inv_delta(k)
show('Solver B K bounds',half_prior_lower=rlo,half_prior_upper=rF,eta_band=bench(rlo)['eta'],rhs=d*(1-M)**2,lhs=k*bench(rlo)['eta'],factor=d*(1-M)**2/(k*bench(rlo)['eta']),conservative_factor=d*(1-M)**2/(k*L),all_prior_lower=rlo_all,all_prior_upper=rN,eta_all_band=bench(rlo_all)['eta'],all_rhs=d*rho*rho/4,all_lhs=k*L,all_factor=d*rho*rho/(4*k*L))
v13=bench(1.3);v29=bench(2.9)
show('finite difference identity',left=v13['gamma']*v29['gamma']*(v29['J']-v13['J']),right=d*v29['X']*(v29['Delta']-v13['Delta'])-v29['gamma']*v13['Delta']*(v13['gH']-v29['gH']))
r_eta_max=1+sqrt(2)
show('CM auxiliary',Gamma_1mtau=d*(1-v2['tau']),D_1ptau=v2['Delta']*(1+v2['tau']),twiceEtaDelta=2*v2['Delta']*v2['eta'],other_max=.75*(r_eta_max-1)/(r_eta_max*(r_eta_max+1)),global_rhs_bound=v2['Delta']*(1+v2['tau'])+.75*(r_eta_max-1)/(r_eta_max*(r_eta_max+1)))

print('\nSHIFTED UNIFORM')
def shifted(z,c=2):
    return mix_payoffs([(1,z-.1,z+.1)],c=c)
for z in [1.1,2,6,7,7.5]:
    v=shifted(z)
    show('shift '+str(z),**v,Jp=1-18/(10-z)**2)
show('shift peak and Solver C roots',peak=10-sqrt(18),x_low=4-sqrt(7),x_high=4+sqrt(7),z_low=5-sqrt(7),z_high=5+sqrt(7),B=8*sqrt(7)-14)
for trading,ceiling in [(2,M),(1.5,.8)]:
    end=bisect(lambda z:shifted(z)['J']-trading,6.5,7.9)
    show('shift coexistence cost '+str(trading),left_open=6,right_closed=end,zC=10-2/ceiling,zN=1+2*trading/rho,zF=1+trading/(1-ceiling))
show('eta1 truncated-path necessity counterexample',c_minus_gL=2,Msquared_gap=M*M*d,Jp_at_low=1-18/(10-1.1)**2,Jp_at_high=1-18/8**2,tau_low=2/8.9,tau_high=2/8)

print('\nSOL DISCONNECTED EXAMPLE')
def solver_A_path(t,strict=False):
    if t<=1:
        ml=.6+.38*t; mh=1.57+(.001*t if strict else 0)
    else:
        ml=.98; mh=(1.571+.229*(t-1)) if strict else (1.57+.23*(t-1))
    return mix_payoffs([(.9,ml-.01,ml+.01),(.1,mh-.01,mh+.01)])
for t in [0,1,2]:
    v=solver_A_path(t)
    show('solver_A t='+str(t),**v)
    show('recruiting tuple at solver_A t='+str(t),**informative(v))
tleave=bisect(lambda t:solver_A_path(t)['J']-k,0,1)
treturn=bisect(lambda t:solver_A_path(t)['J']-k,1,2)
tfull=1+(k/(1-M)-.057)/.023
show('solver_A exact endpoints',leave=tleave,return_=treturn,return_Delta=solver_A_path(treturn)['Delta'],leave_gL=solver_A_path(tleave)['gL'],full_purchase=tfull,coverage=10-1.81-6)
show('solver_A strict spread middle',**solver_A_path(1,True))

print('\nsolver_B DISCONNECTED EXAMPLE, AS WRITTEN')
def solver_B_components(s):
    if s<=1: a=.55; z=1.10+.28*s
    elif s<=2: a=.55+.40*(s-1); z=1.38
    else: a=.95; z=1.38+.20*(s-2)
    return [(.85,a-.02,a+.02),(.15,z-.02,z+.02)]
def solver_B_path(s,epsilon=0):
    parts=[(weight*(1-epsilon),lo,hi) for weight,lo,hi in solver_B_components(s)]
    if epsilon: parts.append((epsilon,0,10))
    return mix_payoffs(parts)
for s in [0,1,2,3]:
    v=solver_B_path(s)
    show('Solver B s='+str(s),**v)
    if s:
        show('Solver B full support s='+str(s),**solver_B_path(s,1e-4))
starts=[bisect(lambda s:solver_B_path(s)['J']-k,0,1),bisect(lambda s:solver_B_path(s)['J']-k,1,2),bisect(lambda s:solver_B_path(s)['J']-k,2,3)]
show('Solver B component endpoints',first_start=starts[0],first_end=starts[1],second_start=starts[2],second_end=3,full_start=2+(k/(1-M)-.057)/.03)
show('Solver B numbers at upper center 1.46',**mix_payoffs([(.85,.93,.97),(.15,1.44,1.48)]))

print('\nsolver_B LONGER UNIFORM PATH')
rpeak=bisect(lambda r:bench(r)['Jp'],4,6)
kbig=bench(5.7)['J']
show('longer uniform',rpeak=rpeak,taupeak=bench(rpeak)['tau'],kbig=kbig,start=bisect(lambda r:bench(r)['J']-kbig,3.6,rpeak),end=5.7,rC=bisect(lambda r:bench(r)['tau']-.87,5,7),rN=inv_delta(2*kbig/rho),gH_equal_cost=bisect(lambda r:bench(r)['gH']-cost,7,9),tau_r2=bench(3.6)['tau'])

print('\nADDITIONAL QUALIFICATIONS')
neg0=mix_payoffs([(.9,.59,.61),(.1,1.56,1.58)],c=.1)
neg1=mix_payoffs([(.9,.59,.61),(.1,1.79,1.81)],c=.1)
show('negative threshold moves down, first',**neg0)
show('negative threshold moves down, stronger',**neg1)
show('dispersion decreases eta',point_L_eta=1/.1,uniform_L_eta=1/(.9*.3+.1),point_Dp=.1,uniform_Dp=.9*.3+.1)
for s in [-1,0,1]:
    r=rA+.1*s**3
    vr=bench(r)
    show('strictly increasing J with stationary boundary s='+str(s),r=r,J=vr['J'],J_derivative=vr['Jp']*.3*s*s,boundary_expression=(d*k*vr['Dp']+vr['Delta']**2*vr['gp'])*.3*s*s)

print('\nEXACT DECIMAL BENCHMARK ENDPOINTS')
r=Q(6,5); D=(r-Q(1))**2/(2*r); gh=Q(10)-r/2-Q(1,4)/(2*r); gl=Q(3,4)/(2*r)
print('J(r0) fraction =',D*(gh-Q(6))/(gh-gl))

print('\nEXACT ANALYTICAL MARGINS AND BOUNDARY QUALIFICATIONS')
r=Q(18,5)
D=(r-1)**2/(2*r); X=Q(4)-r/2-Q(1,4)/(2*r)
eta=(r*r-Q(1,4))/(r*r-1)
print('product monotonicity endpoint margin =', X-eta*D)
print('squared product monotonicity endpoint margin =', X-2*eta*D)
for z in [5,5.5]:
    v=shifted(z)
    show('recruitment-feasible eta=1 counterexample z='+str(z),Delta=v['Delta'],tau=v['tau'],J=v['J'],Jp=1-18/(10-z)**2,no_trade_return=.25*.7*v['Delta'],pi=.3,M=.7,k=2,lambda_=8/17,beta=.2)
ve=bench(rN)
ce=ve['gL']+.875*ve['gamma']
show('mixed crossing at no-trade equality',r=rN,cH=ce,Delta=ve['Delta'],tau=bench(rN,c=ce)['tau'],J=bench(rN,c=ce)['J'],M=.9,one_minus_tau=.125,rho_q=.125,one_minus_M=.1)

print('\nNONDIMENSIONAL CM CONDITION AND DISPERSION CALCULATION')
print('Benchmark share endpoint =', v2['Delta']/d)
print('Relative factor lost by E at endpoint =',1/(1-v2['Delta']/d)-1)
def average_uniform_cdf(lo,hi,al,au):
    cuts=sorted(set([lo,hi]+[x for x in [al,au] if lo<x<hi]))
    return sum((y-x)*max(0,min(1,((x+y)/2-al)/(au-al)))/(hi-lo) for x,y in zip(cuts,cuts[1:]))
point_dp=.9*0+.1*1
spread_dp=.9*average_uniform_cdf(.79,.81,.5,1.5)+.1*average_uniform_cdf(1.99,2.01,.5,1.5)
show('dispersion primitive integrals',point_gap_growth=point_dp,spread_gap_growth=spread_dp,high_profit_erosion=1,point_eta=1/point_dp,spread_eta=1/spread_dp)

print('\nsolver_B PATH EXACT COEXISTENCE ENDPOINT EQUATIONS')
for gl in [.3825,.0425]:
    coeff=3+gl+k
    lowroot=(coeff-sqrt(coeff*coeff-4*9*k))/2
    show('root gL='+str(gl),Delta=lowroot,quadratic_linear_coefficient=coeff)

print('\nDIRECT DIFFERENTIATION AND CLAIMED NUMERICAL MINIMUM')
for r in [1.2,rA,rF,rN,3.6]:
    num=(r-1)**2*(8*r-r*r-.25)
    den=2*r*(20*r-r*r-1)
    nump=2*(r-1)*(8*r-r*r-.25)+(r-1)**2*(8-2*r)
    denp=2*(20*r-r*r-1)+2*r*(20-2*r)
    direct=(nump*den-num*denp)/(den*den)
    show('direct rational differentiation '+str(r),direct=direct,identity=bench(r)['Jp'])
samples=[]
for index in range(24001):
    r=1.2+index/10000
    v=bench(r)
    margin=d*(1-v['tau'])-v['Delta']*(1+v['tau'])-2*v['Delta']*(v['eta']-1)
    samples.append((margin,r))
value,r=min(samples)
show('sampled minimum of Solver B CM margin',margin=value,r=r,points=len(samples))
