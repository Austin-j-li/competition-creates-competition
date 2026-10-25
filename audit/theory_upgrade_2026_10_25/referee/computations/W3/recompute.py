"""Direct numerical evaluation of the supplied W3 research economies.

Prints the equilibrium construction, its payoffs and candidate claims.
No assertions, test cases, or pass/fail checks.
"""
from dataclasses import dataclass, replace
from math import exp, sqrt, inf
import json


@dataclass(frozen=True)
class Economy:
    c: float = 6.0
    k: float = .02
    rho: float = .25
    beta: float = .294655
    a: float = .025
    cap: float = (exp(1)-1)*.294655/(1+(exp(1)-1)*.294655)
    h: float = 10.0
    ell: float = 1.0
    p: float = .5


def root(fun, lo, hi):
    flo = fun(lo)
    for _ in range(100):
        mid = (lo+hi)/2
        fm = fun(mid)
        if flo*fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo+hi)/2


def zeros(fun, lo, hi, n=4000):
    out = []
    x, y = lo, fun(lo)
    for i in range(1,n+1):
        nx = lo+(hi-lo)*i/n
        ny = fun(nx)
        if y*ny < 0:
            out.append(root(fun,x,nx))
        x, y = nx, ny
    return out


def m(e, lam):
    return e.beta*(1-lam)/(2*e.beta+(1-2*e.beta)*lam)


def mp(e, lam):
    return -e.beta/(2*e.beta+(1-2*e.beta)*lam)**2


def le(e, tau):
    return e.beta*(2*tau-1)/(e.beta+(1-2*e.beta)*(1-tau)) if tau<1 else inf


def lep(e, tau):
    return e.beta/(e.beta+(1-2*e.beta)*(1-tau))**2


def auction(e, r):
    def g(v):
        if r <= e.p:
            return v-e.p
        if v <= r:
            return (v*v-e.p*e.p)/(2*r)
        return v-r/2-e.p*e.p/(2*r)
    gh, gl = g(e.h), g(e.ell)
    th, tl = e.h-gh, e.ell-gl
    return dict(gh=gh,gl=gl,th=th,tl=tl,t0=e.p*max(0,1-e.p/r),D=th-tl,
                gamma=gh-gl,tau=(e.c-gl)/(gh-gl))


def intensity(e, D, kind="recruit"):
    if kind == "floor":
        if e.rho*D <= 2*e.k:
            return 0.0
        return root(lambda x:e.rho*D*m(e,x)-e.k-e.a*x,0,1)
    if D <= 2*e.k:
        return 0.0
    if kind == "old":
        return root(lambda x:D*m(e,x)-e.k-2*e.a*x,0,1)
    return root(lambda x:D*m(e,x)-e.k+max(e.rho*D*m(e,x)-e.k,0)-2*e.a*x,0,1)


def phi(e, r, extended=False):
    v=auction(e,r)
    J=v['D']*(1-v['tau'])
    return J-e.k-2*e.a*le(e,v['tau'])+(max(e.rho*J-e.k,0) if extended else 0)


def derivatives(e,r):
    v=auction(e,r)
    dp=(1-1/r**2)/2
    tp=(.375/r**2+v['tau']*dp)/v['gamma']
    jp=dp*(1-v['tau'])-v['D']*tp
    return dict(dp=dp,tp=tp,jp=jp,pp=jp-2*e.a*lep(e,v['tau'])*tp,
                ratio=jp/(2*lep(e,v['tau'])*tp))


def point(e,r,kind="recruit",eplus=None,lam=None,z=None):
    v=auction(e,r)
    D,tau=v['D'],v['tau']
    raw=intensity(e,D,kind)
    lam=min(e.cap,raw) if lam is None else lam
    if lam == 0:
        return dict(r=r,D=D,tau=tau,lam=0,entry=e.rho,V=max(e.rho*D/2-e.k,0))
    b=(1-lam)*e.beta
    b0=(1-lam)*(1-2*e.beta)
    z=max(0,min(1,b/lam*(e.rho*D/e.k-2))) if z is None else z
    fh=[b,b0,b+lam]
    fl=[b+lam*z,b0+lam*(1-z),b]
    mu=[fh[i]/(fh[i]+fl[i]) for i in range(3)]
    ep=e.rho if kind=="floor" else 1
    ep=ep if eplus is None else eplus
    ent=[e.rho,e.rho,ep]
    prices=[v['t0']+ent[i]*(mu[i]*(v['th']-v['t0'])+(1-mu[i])*(v['tl']-v['t0'])) for i in range(3)]
    uh=[q*(v['t0']+ent[i]*(v['th']-v['t0'])-prices[i])-e.k*abs(q) for i,q in enumerate([-1,0,1])]
    ul=[q*(v['t0']+ent[i]*(v['tl']-v['t0'])-prices[i])-e.k*abs(q) for i,q in enumerate([-1,0,1])]
    V=(max(uh)+max(ul))/2
    return dict(r=r,D=D,tau=tau,raw=raw,lam=lam,lambda_E=le(e,tau),z=z,mu=mu,
                entry=sum((fh[i]+fl[i])/2*ent[i] for i in range(3)),P=prices,
                UH=uh,UL=ul,V=V,V_over_a=V/e.a,BR=min(e.cap,V/e.a),
                research_gap=min(e.cap,V/e.a)-lam,prep_gaps=[v['gl']+u*v['gamma']-e.c for u in mu],
                posterior_margin=mu[2]-tau,phi=phi(e,r),phi_star=phi(e,r,True))


def r_of_D(e,D):
    return root(lambda r:auction(e,r)['D']-D,1,10000)


def cutoffs(e):
    ls=(1-e.rho)*e.k/(2*e.a*e.rho)
    dc=(2*e.a*e.cap+e.k)/m(e,e.cap) if e.cap<=ls else (2*e.a*e.cap+2*e.k)/((1+e.rho)*m(e,e.cap))
    nc=2*e.k/e.rho
    ss=e.k/(e.rho*m(e,min(e.cap,ls)))
    rc=root(lambda r:auction(e,r)['tau']-(1-m(e,e.cap)),1,100)
    return dict(lambda_S=ls,D_N=nc,D_cap=dc,D_sale=ss,
                r_N=r_of_D(e,nc),r_cap=r_of_D(e,dc),r_sale=r_of_D(e,ss),r_C=rc,
                r_R=zeros(lambda r:phi(e,r,True),1.01,rc),
                r_X=zeros(lambda r:e.rho*auction(e,r)['D']*(1-auction(e,r)['tau'])-e.k-e.a*le(e,auction(e,r)['tau']),1.01,rc),
                r_U=r_of_D(e,(e.k+e.a*e.cap)/(e.rho*m(e,e.cap))))


def emit(label,data):
    print(label, json.dumps(data,sort_keys=True))


def compact(e,r,kind="recruit"):
    v=point(e,r,kind)
    return {k:v[k] for k in ['r','D','tau','lam','entry']+(['z','posterior_margin','V','research_gap'] if v['lam'] else [])}


if __name__ == '__main__':
    B=Economy()
    A=Economy(c=4.5,k=.5,rho=.5,beta=.2,a=.01,cap=.4)
    S=Economy(c=4.7,k=.1,rho=.5,beta=.2,a=1,cap=.3)
    F=replace(B,c=5,rho=.5,a=.1)
    for name,e,rs in [
        ('benchmark',B,[1.2,1.55,1.6,1.65,1.745,1.75,1.76,1.8,1.9,2,2.1,2.12,2.13,2.3,3.59,3.595]),
        ('the referee',A,[4,5,5.5,5.9,6,6.2,6.5,6.8,7,7.2,7.28,8,9,9.9]),
        ('solver_A_full',S,[2,3,4,5]),
        ('solver_D_full',F,[1.45,1.49,1.53,1.55,1.8,2.04,2.05,2.1,3,4,6.3,6.4])]:
        cs=cutoffs(e)
        emit(name+'_params',e.__dict__)
        emit(name+'_cutoffs',cs)
        selected=rs+cs['r_R']+[cs['r_N'],cs['r_cap'],cs['r_sale'],cs['r_C']]
        for r in sorted(set(selected)):
            emit(name+'_recruit',compact(e,r))
        for r in sorted(set(rs+[cs['r_C']]+cs['r_X'])):
            if auction(e,r)['D']*e.rho > 2*e.k:
                emit(name+'_floor',compact(e,r,'floor'))
        for r in [cs['r_cap'],cs['r_C']]:
            emit(name+'_tuple',point(e,r))
    for e,r in [(B,1.9),(B,2),(A,6.5),(S,3)]:
        emit('detailed_tuple',dict(economy=e.__dict__,tuple=point(e,r)))
    for a in [.025,.035,.1,.16,.2,.3,.40833,.5,1]:
        e=replace(B,a=a)
        emit('benchmark_other_a',dict(a=a,cutoffs=cutoffs(e),phi_roots=zeros(lambda r:phi(e,r),1.2,3.6),at_N=point(e,cutoffs(B)['r_N'])['lam']))
    e=replace(B,a=.2)
    emit('a02_at225',point(e,2.25))
    emit('a02_at266',point(e,2.66))
    mb=m(B,B.cap)
    aN=B.k*(2*mb-B.rho)/(2*B.rho*B.cap)
    rc=cutoffs(B)['r_C']
    vc=auction(B,rc)
    jc=vc['D']*(1-vc['tau'])
    amax=(jc-B.k+max(B.rho*jc-B.k,0))/(2*B.cap)
    ratios=[(derivatives(B,1.2+i*2.4/24000)['ratio'],1.2+i*2.4/24000) for i in range(24001)]
    d,dm,T,t=11/72,9/56,1-19/55,16875/211288
    lead=d*(1-T)-dm*t
    amono=lead*(B.beta+(1-2*B.beta)*(1-T))**2/(2*B.beta*t)
    alo=(auction(B,1.65)['D']*mb-B.k)/(2*B.cap)
    aup=(auction(B,1.55)['D']*(1-auction(B,1.55)['tau'])-B.k)/(2*le(B,auction(B,1.55)['tau']))
    emit('benchmark_margins',dict(mcap=mb,cap_margin=2*B.k*mb-B.rho*(2*B.a*B.cap+B.k),
         aN=aN,rhoN=2*B.k*mb/(2*B.a*B.cap+B.k),kN=2*B.rho*B.a*B.cap/(2*mb-B.rho),
         capN=root(lambda l:2*B.k*m(B,l)-B.rho*(2*B.a*l+B.k),.001,.999),
         normalized=B.rho*(2*B.a*B.cap+B.k)/(2*B.k*mb),
         beta_family_cap_bound=B.k*(2*mb-B.rho)/(2*B.rho*B.a),
         beta_family_one_third=(exp(1)-1)/(3+exp(1)-1),
         aFull=(1-B.rho)*B.k/(2*B.rho*B.cap),
         amax=amax,amin_ratio=min(ratios),lead=lead,amono=amono,phi_prime_bound=lead*(1-B.a/amono),
         phi_initial=phi(B,1.2),phi_cap=phi(B,cutoffs(B)['r_cap']),alo=alo,aup=aup,
         affected_window_share=(aup-aN)/(aup-alo)))
    emit('amax_singleton',point(replace(B,a=amax),rc))
    for name,e in [('the referee',A),('benchmark',B)]:
        rc=cutoffs(e)['r_C']
        v=auction(e,rc)
        J=v['D']*(1-v['tau'])
        w=max(e.rho*J-e.k,0)
        emin=(2*e.a*e.cap+e.k-w)/J
        emit(name+'_CM_cap',dict(r=rc,J=J,emin=emin,admissible_lower=max(e.rho,emin),upper=1))
    rr=replace(B,rho=.3)
    emit('rho03',dict(cutoffs=cutoffs(rr),at_N=point(rr,cutoffs(rr)['r_N']),at_cap=point(rr,cutoffs(rr)['r_cap'])))
    # solver_A's translated-uniform example has direct auction integrals.
    def solver_A_phi(D):
        tau=4/(9-D)
        return D*(1-tau)-.55-3.4*(D-1)/(4*(6-D))
    emit('solver_A_J_example',dict(roots=zeros(solver_A_phi,1.1,2.99),values=[dict(D=D,J=D*(5-D)/(9-D),Jp=1-36/(9-D)**2,phi=solver_A_phi(D),lambda_E=(D-1)/(4*(6-D)),lambda_R=intensity(Economy(k=.55,rho=.1,beta=.2,a=1.7,cap=.8),D)) for D in [1.1,2,2.9,2.99]]))
    O=Economy(c=4.75,k=.02,rho=.25,beta=.3,a=2,cap=.9)
    emit('solver_B_J_example',dict(tauhalf=root(lambda r:auction(O,r)['tau']-.5,1.2,1.6),phi_roots=zeros(lambda r:phi(O,r),1.2,5),phi_star_roots=zeros(lambda r:phi(O,r,True),1.2,5),min_Jp=min((derivatives(O,1.2+i*3.8/3800)['jp'],1.2+i*3.8/3800) for i in range(3801))))
    for r in [1.4,1.45,1.55,1.7,1.85,1.896793,2.5,4,4.911424,4.95]:
        emit('solver_B_J_example_point',point(O,r))
    vv=auction(B,1.6)
    dd=derivatives(B,1.6)
    extra_tau=.25/vv['gamma']*.1
    emit('solver_D_local_example',dict(tau_coefficient=.25/vv['gamma'],dJ=dd['jp']*.004-vv['D']*extra_tau,dphi=dd['pp']*.004-(vv['D']+2*B.a*lep(B,vv['tau']))*extra_tau,base_phi=phi(B,1.6)))
    for name,e in [('solver_A_full',S),('solver_D_full',F)]:
        cs=cutoffs(e)
        ls=cs['lambda_S']; ds=cs['D_sale']
        emit(name+'_slopes',dict(left=m(e,ls)/(2*e.a-ds*mp(e,ls)),right=(1+e.rho)*m(e,ls)/(2*e.a-(1+e.rho)*ds*mp(e,ls))))
    cA=cutoffs(A); cS=cutoffs(S)
    tpA=223.5/63**2
    boundA=.46875*(1-auction(A,5)['tau'])-(1.6+2*A.a*lep(A,auction(A,5)['tau']))*tpA
    tpS=(9.4*cS['r_N']**2-3+5.6)/35**2
    boundS=.375*(1-auction(S,cS['r_N'])['tau'])-(.4+2*S.a*lep(S,auction(S,cS['r_N'])['tau']))*tpS
    pairs=[(cS['r_N'],cS['r_sale']),(cS['r_sale'],3),(3,4),(4,5),(5,cS['r_cap'])]
    emit('solver_A_interval_bounds',dict(referee_deriv=boundA,referee_56=1.6*(1-auction(A,6)['tau'])-.5-.02*.4,referee_6cap=(25/12)*(1-auction(A,cA['r_cap'])['tau'])-.5-.02*.4,full_deriv=boundS,full_posterior_margins=[1-m(S,min(S.cap,intensity(S,auction(S,l)['D'])))-auction(S,r)['tau'] for l,r in pairs]))
    emit('referee_J_peak_values',[dict(r=r,J=auction(A,r)['D']*(1-auction(A,r)['tau']),Jp=derivatives(A,r)['jp']) for r in [7.28,7.3]])
    emit('referee_J_peak',root(lambda r:derivatives(A,r)['jp'],6,8))
    # A threshold equilibrium with strict trades under I0 and mixed preparation under CM.
    r=2.0
    v=auction(B,r)
    lam=le(B,v['tau']); J=v['D']*(1-v['tau'])
    ep=(2*B.a*lam+B.k-max(B.rho*J-B.k,0))/J
    emit('I0_CM_at2',point(B,r,eplus=ep,lam=lam))
    # A coincident sale and abstention price, obtained without imposing a posterior.
    z0=B.beta/(1-B.beta)
    d0=B.k/B.rho*(2+B.cap*z0/((1-B.cap)*B.beta))
    rr=r_of_D(B,d0)
    emit('pooled_sale_zero',point(B,rr))
    # The equality in rho*Delta=2k allows any hypothetical best correct orders at zero research.
    for name,e in [('benchmark',B),('the referee',A)]:
        rr=cutoffs(e)['r_N']; v=auction(e,rr)
        emit(name+'_Z_tie',dict(r=rr,lam=0,mu=[.5,.5,.5],price=v['t0']+e.rho*(v['tl']-v['t0']+v['D']/2),
                  UH_buy=e.rho*v['D']/2-e.k,UL_sell=e.rho*v['D']/2-e.k,V=0,
                  example_sigma_H=[0,0,1],example_sigma_L=[1,0,0]))
