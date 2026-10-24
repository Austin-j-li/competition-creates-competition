"""Print independent auction, order, signal, and coexistence calculations."""

from fractions import Fraction as F
from itertools import product
import platform
import mpmath as mp

mp.mp.dps = 70


def dec(x):
    if isinstance(x, F):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x)


def show(x):
    if isinstance(x, F):
        return f"{x} ({mp.nstr(dec(x), 18)})"
    return mp.nstr(x, 55)


def auction(r):
    """Integrate payments and rents on each interval of incumbent values."""
    p = r * 0 + F(1, 2)
    result = [p * (r - p) / r]
    for theta in (r * 0 + 10, r * 0 + 1):
        breaks = sorted(set([r * 0, r, p] + ([theta] if theta < r else [])))
        payment, rent = r * 0, r * 0
        for lo, hi in zip(breaks, breaks[1:]):
            center = (lo + hi) / 2
            if center < p:
                payment += p * (hi - lo)
                rent += (theta - p) * (hi - lo)
            elif center < theta:
                payment += (hi**2 - lo**2) / 2
                rent += theta * (hi - lo) - (hi**2 - lo**2) / 2
            else:
                payment += theta * (hi - lo)
        result.extend([payment / r, rent / r])
    t0, th, gh, tl, gl = result
    return dict(t0=t0, th=th, gh=gh, tl=tl, gl=gl, D=th-tl, wh=th-t0, wl=tl-t0)


def gross(r, mu):
    z = auction(r)
    return mu*z['gh'] + (1-mu)*z['gl']


def threshold(r, cost=F(6)):
    z = auction(r)
    return (cost-z['gl'])/(z['gh']-z['gl'])


def uniform_cdf(value, low, high):
    return min(1, max(0, (value-low)/(high-low)))


def prepare(r, mu, rho, cost, continuous=False):
    value = gross(r, mu)
    if continuous:
        return rho*uniform_cdf(value, F(0), F(1, 5)) + (1-rho)*uniform_cdf(value, F(59,10), F(61,10))
    return rho + (1-rho)*int(value >= cost)


def slot_rows(r, b, lam, pi=F(1, 2), rho=F(1, 4), cost=F(6), continuous=False, s=None, t=None):
    """Construct class flow masses and compute preparation, prices, and payoffs."""
    c = 1-lam-2*b
    if s is None:
        s = lam
    if t is None:
        t = lam
    laws = {1:(b+s,b), -1:(b,b+t), 0:(c+lam-s,c+lam-t)}
    z = auction(r)
    rows = []
    for q, (ph,pl) in laws.items():
        prob = pi*ph+(1-pi)*pl
        mu = pi*ph/prob
        e = prepare(r,mu,rho,cost,continuous)
        price = z['t0']+e*(mu*z['wh']+(1-mu)*z['wl'])
        rows.append(dict(q=q,ph=ph,pl=pl,prob=prob,mu=mu,e=e,price=price))
    entry = sum(v['prob']*v['e'] for v in rows)
    ownership = pi*sum(v['ph']*v['e'] for v in rows)
    high_util = {v['q']:v['q']*(z['t0']+v['e']*z['wh']-v['price'])-abs(v['q'])*F(1,50) for v in rows}
    low_util = {v['q']:v['q']*(z['t0']+v['e']*z['wl']-v['price'])-abs(v['q'])*F(1,50) for v in rows}
    return rows,entry,ownership,high_util,low_util


def laplace_tail(y):
    return mp.exp(-y/2)/2 if y >= 0 else 1-mp.exp(y/2)/2


def laplace_entry_for_cost(r, cost):
    """Obtain the flow cutoff from likelihoods, then integrate each density."""
    tau = threshold(r, cost)
    lower, upper = 1/(1+mp.e), mp.e/(1+mp.e)
    if tau <= lower:
        return mp.mpf(1),mp.mpf(1)
    if tau > upper:
        return mp.mpf(0),mp.mpf(0)
    cutoff = mp.log(tau/(1-tau))
    return laplace_tail(cutoff-1),laplace_tail(cutoff+1)


def laplace_cost_mixture(r):
    lower,upper = 1/(1+mp.e),mp.e/(1+mp.e)
    floor,ceiling = gross(r,lower),gross(r,upper)
    means=[]
    for lo,hi in ((mp.mpf(0),mp.mpf('0.2')),(mp.mpf('5.9'),mp.mpf('6.1'))):
        pieces=sorted(set([lo,hi]+[v for v in (floor,ceiling) if lo<v<hi]))
        means.append([sum(mp.quad(lambda cost:laplace_entry_for_cost(r,cost)[j],[l,h]) for l,h in zip(pieces,pieces[1:]))/(hi-lo) for j in (0,1)])
    eh=means[0][0]/4+3*means[1][0]/4
    el=means[0][1]/4+3*means[1][1]/4
    return (eh+el)/2,eh/2


def signal_profile(r,b,lam,a,d,orders):
    """Sum the joint law over class, signal, identity, order, and private signal."""
    rho,cost,k=F(17,20),F(357,50),F(3,200)
    z=auction(r)
    c=1-lam-2*b
    joint=[]
    for j,t,y in product((1,0),repeat=3):
        pt=a if t==j else 1-a
        py=d if y==j else 1-d
        for informed,prob in ((True,lam),(False,1-lam)):
            law={orders[t]:1} if informed else {-1:b/(1-lam),0:c/(1-lam),1:b/(1-lam)}
            for q,pq in law.items():
                joint.append((j,t,y,q,F(1,2)*pt*py*prob*pq))
    prices,policies,posterior={},{},{}
    for q in (-1,0,1):
        mass=sum(v[4] for v in joint if v[3]==q)
        mu=sum(v[4]*v[0] for v in joint if v[3]==q)/mass
        posterior[q]=mu
        for y in (0,1):
            sub=[v for v in joint if v[3]==q and v[2]==y]
            joint_mu=sum(v[4]*v[0] for v in sub)/sum(v[4] for v in sub)
            policies[q,y]=prepare(r,joint_mu,rho,cost)
        prices[q]=sum(v[4]*(z['t0']+policies[q,v[2]]*(z['wh'] if v[0] else z['wl'])) for v in joint if v[3]==q)/mass
    entry=sum(v[4]*policies[v[3],v[2]] for v in joint)
    ownership=sum(v[4]*v[0]*policies[v[3],v[2]] for v in joint)
    utility={}
    for t in (0,1):
        utility[t]={}
        for q in (-1,0,1):
            conditional=0
            for j,y in product((0,1),repeat=2):
                pj=a if j==t else 1-a
                py=d if y==j else 1-d
                conditional+=pj*py*(z['t0']+policies[q,y]*(z['wh'] if j else z['wl']))
            utility[t][q]=q*(conditional-prices[q])-abs(q)*k
    return entry,ownership,utility,posterior,policies


def signal_margins(b,lam,a,d):
    rho,cost,k=F(17,20),F(357,50),F(3,200)
    M=(b+lam)/(2*b+lam)
    mu=(1-a)+(2*a-1)*M
    combined=d*mu/(d*mu+(1-d)*(1-mu))
    weak,strong=auction(F(11,10)),auction(F(23,10))
    return (cost-gross(F(11,10),d),gross(F(23,10),combined)-cost,
            k-(2*a-1)*(weak['D']+(1-rho)*(2*d-1)*weak['wh']),
            (2*a-1)*rho*(1-M)*strong['D']-k)


def inverse_spread(D):
    D=dec(D)
    return 1+D+mp.sqrt(D*D+2*D)


def candidate_buys(r,b,lam,pi):
    """List all positive high-class buy rates while the low class waits."""
    rho,k=F(1,4),F(1,50)
    z=auction(r)
    candidates=[('full',lam)]
    for name,e in (('floor',rho),('recruited',F(1))):
        rate=((1-pi)*b*e*z['D']/k-b)/pi
        if 0<rate<lam:
            candidates.append((name,rate))
    answer=[]
    for name,s in candidates:
        rows,E,O,uh,ul=slot_rows(r,b,lam,pi=pi,s=s,t=F(0))
        if name=='full':
            allowed=uh[1]>=0
        else:
            expected=F(1,4) if name=='floor' else F(1)
            allowed=rows[0]['e']==expected
        if allowed:
            answer.append((name,s,E,rows[0]['mu'],uh[1],ul[-1]))
    return answer


def main():
    print('Independent calculation; Python',platform.python_version(),'mpmath',mp.__version__,'digits',mp.mp.dps)
    for r in (F(11,10),F(6,5),F(23,10),F(3),F(18,5)):
        print('AUCTION',r,{k:show(v) for k,v in auction(r).items()},'tau',show(threshold(r)))
    alpha_h,alpha_l=laplace_entry_for_cost(mp.mpf(3),mp.mpf(6))
    bB=(alpha_h+alpha_l)/(1+mp.e)
    lamB=(mp.e-1)*bB
    calibrations=(('A',F(11,51),F(6,17)),('B',bB,lamB))
    for tag,b,lam in calibrations:
        print('CALIBRATION',tag,'b',show(b),'lambda',show(lam),'beta',show(b/(1-lam)),'M',show((b+lam)/(2*b+lam)))
    print('\nX1 frozen orders and Laplace controls')
    for tag,b,lam in calibrations:
        for r in (F(6,5),F(3),F(18,5)):
            rows,E,O,uh,ul=slot_rows(r,b,lam)
            print(tag,r,'E',show(E),'O',show(O),'net_H_buy',show(uh[1]),'net_L_sell',show(ul[-1]))
            print('FLOW',[(v['q'],show(v['mu']),show(gross(r,v['mu'])),show(v['e'])) for v in rows])
    for r in (mp.mpf('1.2'),mp.mpf(3)):
        ah,al=laplace_entry_for_cost(r,mp.mpf(6))
        print('LAPLACE_ATOMIC',r,'E',show(mp.mpf(1)/4+3*(ah+al)/8),'O',show(mp.mpf(1)/8+3*ah/8))
    print('\nX3 declared continuous cost law')
    for tag,b,lam in calibrations:
        for r in (F(6,5),F(3),F(18,5)):
            s,t=(0,0) if r==F(6,5) else (lam,lam)
            rows,E,O,uh,ul=slot_rows(r,b,lam,continuous=True,s=s,t=t)
            print(tag,r,'E',show(E),'O',show(O),'entry_at_buy',show(rows[0]['e']),'H_buy_net',show(uh[1]),'L_sell_net',show(ul[-1]))
        M=(b+lam)/(2*b+lam)
        margins=[gross(F(3),1-M)-F(1,5),F(59,10)-gross(F(6,5),F(1,2)),gross(F(3),M)-F(61,10),F(1,50)-auction(F(6,5))['D'],F(1,4)*(1-M)*auction(F(3))['D']-F(1,50)]
        print('X3_MARGINS',tag,list(map(show,margins)),'collapse_top_profit',show(gross(F(18,5),M)))
    for r in (mp.mpf('1.2'),mp.mpf(3),mp.mpf('3.6')):
        E,O=laplace_cost_mixture(r)
        print('LAPLACE_FULL_ORDERS_CONTINUOUS',r,'E',show(E),'O',show(O))
    print('LAPLACE_CONTINUOUS_WEAK_EQUILIBRIUM E 1/4 O 1/8; the weak full-order row is a frozen control')
    print('\nX4 joint enumeration and accuracy grid')
    for tag,b,lam in calibrations:
        met=[]
        for ai,di in product(range(68,73),range(73,78)):
            a,d=F(ai,100),F(di,100)
            margins=signal_margins(b,lam,a,d)
            if min(margins)>0:
                met.append((ai,di))
            for r,orders in ((F(11,10),{0:0,1:0}),(F(23,10),{0:-1,1:1})):
                E,O,U,posterior,policies=signal_profile(r,b,lam,a,d,orders)
                gains=[max(U[t].values())-U[t][orders[t]] for t in (0,1)]
                print('SIGNALS',tag,ai,di,r,'E',show(E),'O',show(O),'deviation_gains',list(map(show,gains)))
                if (ai,di)==(70,75):
                    print('DECLARED_DETAIL',tag,r,'margins',list(map(show,margins)),'U', {t:{q:show(v) for q,v in u.items()} for t,u in U.items()},'posteriors',{q:show(v) for q,v in posterior.items()},'preparation',{str(key):show(v) for key,v in policies.items()})
        print('MET_PAIRS',tag,met)
    print('\nCOEXISTENCE')
    J=lambda r:auction(r)['D']*(1-threshold(r))
    root=mp.findroot(lambda r:J(r)-mp.mpf('0.02'),(mp.mpf('1.3'),mp.mpf('1.5')))
    tauA=threshold(root)
    print('rA',show(root),'tauA',show(tauA),'DeltaA',show(auction(root)['D']))
    for edge in ('1.3939579202792','1.3939579202793'):
        val=F(edge)
        print('ROOT_BRACKET',edge,'J-k',show(J(val)-F(1,50)))
    for tag,b,lam in calibrations:
        u=lam/b
        pi_low=tauA/((1+dec(u))*(1-tauA)+tauA)
        print('PRIOR_LOWER',tag,show(pi_low))
        for pi in (F(2,5),F(397,1000),F(12,25),F(1,2),F(3,5),F(16,25),F(321,500),F(13,20),F(4,5)):
            M=pi*(b+lam)/(b+pi*lam)
            rN=inverse_spread(F(1,50)/(F(1,4)*max(pi,1-pi)))
            rF=inverse_spread(F(1,50)/(1-M))
            print('PRIOR',tag,pi,'M',show(M),'rN',show(rN),'rF',show(rF))
            coex=[]
            branches=[]
            for ri in range(240,381):
                r=F(ri,200)
                eprior=prepare(r,pi,F(1,4),F(6))
                no_trade=eprior*auction(r)['D']*max(pi,1-pi)<=F(1,50)
                if no_trade:
                    positive=candidate_buys(r,b,lam,pi)
                    if positive:
                        coex.append(r)
                        for name,s,E,mu,uh,ul in positive:
                            if name=='recruited':
                                formula=F(1,4)+F(3,4)*(1-pi)*b*auction(r)['D']/F(1,50)
                                branches.append((r,E,E-formula,ul))
            print('COEX_GRID',tag,pi,'range',([str(coex[0]),str(coex[-1])] if coex else []),'points',len(coex),'interior_count',len(branches),'max_entry_difference',show(max([abs(v[2]) for v in branches],default=F(0))))
            if pi in (F(1,2),F(321,500),F(16,25)):
                for r in (F(7,5),F(29,20),F(3,2)):
                    eprior=prepare(r,pi,F(1,4),F(6))
                    print('COEX_DETAIL',tag,pi,r,'prior_entry',show(eprior),'no_trade_margin',show(F(1,50)-eprior*auction(r)['D']*max(pi,1-pi)),'positive_candidates',[[name,show(s),show(E),show(mu),show(uh),show(ul)] for name,s,E,mu,uh,ul in candidate_buys(r,b,lam,pi)])


if __name__ == '__main__':
    main()
