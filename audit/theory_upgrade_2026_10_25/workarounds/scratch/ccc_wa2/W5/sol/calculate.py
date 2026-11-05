from decimal import Decimal, getcontext

getcontext().prec = 55
D = Decimal
beta = D('0.294655')
u = D(1).exp() - 1
lam = u * beta / (1 + u * beta)
b = (1 - lam) * beta
rho, cost, k, reserve = D('.25'), D(6), D('.02'), D('.5')


def show(label, values):
    print(label)
    for name, value in values.items():
        print(f'  {name}: {value:.12f}' if isinstance(value, D) else f'  {name}: {value}')


def auction(intervals):
    target = []
    profit = []
    t0 = sum(weight * reserve * max(D(0), hi - max(lo, reserve)) / (hi - lo)
             for weight, lo, hi in intervals)
    for theta in (D(10), D(1)):
        proceeds = D(0)
        rents = D(0)
        for weight, lo, hi in intervals:
            points = sorted({lo, hi, *[z for z in (reserve, theta) if lo < z < hi]})
            for left, right in zip(points, points[1:]):
                middle = (left + right) / 2
                mass = weight * (right - left) / (hi - lo)
                proceeds += mass * max(reserve, min(theta, middle))
                rents += mass * max(D(0), theta - max(reserve, middle))
        target.append(proceeds)
        profit.append(rents)
    th, tl = target
    gh, gl = profit
    return dict(t0=t0, wL=tl-t0, delta=th-tl, gh=gh, gl=gl,
                tau=(cost-gl)/(gh-gl))


def full(pi, aq):
    fp, fm = b + pi * lam, b + (1-pi) * lam
    f0 = 1-fp-fm
    M, m = pi * (b+lam) / fp, pi*b/fm
    mus = (m, pi, M)
    es = tuple(D(1) if aq['gl'] + mu*(aq['gh']-aq['gl']) >= cost else rho for mu in mus)
    gains = tuple(aq['wL']+aq['delta']*mu for mu in mus)
    prices = tuple(aq['t0']+e*gain for e,gain in zip(es,gains))
    ip, im = prices[2]-prices[1], prices[1]-prices[0]
    probs = (fm, f0, fp)
    E = sum(f*e for f,e in zip(probs,es))
    prep_mean = sum(f*e*(1-e)*gain for f,e,gain in zip(probs,es,gains)) / E
    c = fm * im / (rho * aq['delta'])
    recovered_lam = 2*c + (4*c*c+(fp-fm)**2).sqrt() if c >= 0 else D('NaN')
    results = dict(pi=pi, m=m, M=M, fp=fp, fm=fm, mean_order=fp-fm, volume=fp+fm,
                   e_minus=es[0], e_zero=es[1], e_plus=es[2],
                   I_plus=ip, I_minus=im, raw_asymmetry=ip-im,
                   weighted_asymmetry=fp*ip-fm*im,
                   purchase_entry_component=(es[2]-rho)*gains[2],
                   expected_entry=E, preparation_report_mean=prep_mean,
                   high_buy_net=es[2]*aq['delta']*(1-M)-k,
                   low_sell_net=es[0]*aq['delta']*m-k,
                   full_order_floor_margin=rho*aq['delta']*min(m,1-M)-k,
                   top_profit_minus_cost=aq['gl']+M*(aq['gh']-aq['gl'])-cost,
                   prior_profit_minus_cost=aq['gl']+pi*(aq['gh']-aq['gl'])-cost,
                   A_top=gains[2], spread=ip+im)
    if es[0] == rho and es[1] == rho:
        results.update(price_recovered_lambda=recovered_lam,
                       price_recovered_pi=(1+(fp-fm)/recovered_lam)/2,
                       price_recovered_beta=(fp+fm-recovered_lam)/(2*(1-recovered_lam)))
    return results


show('BENCHMARK SLOT', dict(u=u, beta=beta, lam=lam, b=b, v=2*b+lam, informed_share=lam/(2*b+lam)))
for rr, pp in [('3','.5'), ('3.6','.5'), ('3.6','.4'), ('3','.6'), ('3','.9')]:
    aq=auction([(D(1),D(0),D(rr))])
    show('UNIFORM AUCTION r='+rr,aq)
    show('FULL ORDERS r='+rr+' pi='+pp,full(D(pp),aq))

for name, intervals in [
    ('weak',[(D('.1'),D('.3'),D('.4')),(D('.9'),D('1.5'),D('1.7'))]),
    ('strong',[(D('.1'),D('.6'),D('.7')),(D('.9'),D('1.51'),D('1.71'))])]:
    aq=auction(intervals)
    show('RESERVE CROSSING '+name, aq)
    show('RESERVE CROSSING FULL '+name, full(D('.5'),aq))

rr=D('1.4')
pi=D('.6')
aq=auction([(D(1),D(0),rr)])
s=b/pi*((1-pi)*aq['delta']/k-1)
muplus=pi*(b+s)/(b+pi*s)
fzero=1-2*b-pi*s
muzero=pi*(1-2*b-s)/fzero
for presence in (lam,lam-D('.05')):
    show('MIXED PURCHASES ONLY',dict(pi=pi, r=rr, lam=presence, beta=b/(1-presence),
         effective_rate=s, conditional_H_buy=s/presence, purchase_probability=b+pi*s,
         sale_probability=b, mean_order=pi*s, volume=2*b+pi*s,
         muplus=muplus, muzero=muzero, tau=aq['tau'],
         top_profit_minus_cost=aq['gl']+muplus*(aq['gh']-aq['gl'])-cost,
         high_buy_net=aq['delta']*(1-muplus)-k,
         low_sell_net=rho*aq['delta']*pi-k))

M=(1+u)/(2+u)
print('BENCHMARK MARGINS')
for rr in (D('1.2'),D('2.124148'),D('3'),D('3.592659'),D('3.6'),D('10')):
    aq=auction([(D(1),D(0),rr)])
    aprime=D(1)/(8*rr*rr) + M*(D('.5')-D(1)/(2*rr*rr))
    show('r='+str(rr),dict(Aprime=aprime,prior_cost_margin=cost-(aq['gl']+(aq['gh']-aq['gl'])/2),
         uniform_reserve_margin=D(1)-3*reserve*reserve))
