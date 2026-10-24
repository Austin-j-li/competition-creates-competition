"""Print independent exact and interval calculations for the pinned manuscript.

The program uses closed-form auction payoffs and split convolution integrals.
It imports no numerical module from the project. Decimal endpoints round outward.
"""
from __future__ import annotations

import csv
import hashlib
import platform
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path

import mpmath as mp

HERE = Path(__file__).resolve().parent
iv = mp.iv
iv.dps = 65
ROWS = []


def I(x):
    if isinstance(x, Q):
        return iv.mpf(x.numerator) / x.denominator
    return iv.mpf(x)


def rational_endpoint(t):
    sign, mantissa, exponent, _ = t
    return (-1 if sign else 1) * Q(mantissa) * Q(2) ** exponent


def endpoints(x):
    return tuple(rational_endpoint(t) for t in I(x)._mpi_)


def decimal_grid(n, digits=42):
    sign = '-' if n < 0 else ''
    s = str(abs(n)).zfill(digits + 1)
    return sign + s[:-digits] + '.' + s[-digits:]


def outward(x):
    low, high = endpoints(x)
    scale = 10**42
    lower = (low * scale).__floor__()
    upper = (high * scale).__ceil__()
    return decimal_grid(lower), decimal_grid(upper)


def record(key, value):
    lower, upper = (str(value), str(value)) if isinstance(value, Q) else outward(value)
    lo, hi = (value, value) if isinstance(value, Q) else endpoints(value)
    sign = 'positive' if lo > 0 else 'negative' if hi < 0 else 'contains_zero'
    ROWS.append((key, lower, upper, sign))
    print(f'{key}: [{lower}, {upper}] {sign}', flush=True)


def auction(r, h=Q(10), ell=Q(1), p=Q(1, 2)):
    t0 = p * (1 - p / r)
    # Integrals of the cash payment, split at the reserve and the low value.
    tH = (p*p + (r*r-p*p)/2) / r
    tL = (p*p + (ell*ell-p*p)/2 + ell*(r-ell)) / r
    return dict(t0=t0, tH=tH, tL=tL, D=tH-tL,
                gH=h-tH, gL=ell-tL)


def B(obj, mu):
    return I(obj['gL']) + mu * I(obj['gH']-obj['gL'])


def threshold(obj, cost=Q(6)):
    return (cost-obj['gL'])/(obj['gH']-obj['gL'])


def inverse_spread(d):
    d = I(d)
    return 1+d+iv.sqrt(d*d+2*d)


def posterior_prior_inverse(t):
    return I(t)/(I(t)+(1-I(t))*iv.exp(1))


def full_order_entry(obj):
    t = I(threshold(obj))
    xs = iv.log(t/(1-t))
    ah = 1-iv.exp((xs-1)/2)/2
    al = iv.exp(-(xs+1)/2)/2
    return xs, ah, al, I('0.25')+I('0.375')*(ah+al)


def candidate(r, v):
    a = auction(r)
    D = I(a['D'])
    tau = I(threshold(a))
    xs = iv.log(tau/(1-tau))+(1-v)/2
    mv = 1/(1+iv.exp((1+v)/2))
    return a, D, xs, mv


def angle(x, c):
    return iv.atan2(iv.exp((x-c)/2), I(1))


def low_root(r, v):
    _, D, xs, mv = candidate(r, v)
    c = (1-v)/2
    # The deviation center equals -v. The entire central interval is to its right.
    left = I('0.25')*D*mv/2
    factor = iv.exp((-v-c)/2)/2
    central = factor * (I('0.25')*(angle(xs, c)-angle(-v, c))
                        + angle(I(1), c)-angle(xs, c))
    right = D * (central + (1-mv)*iv.exp((-v-1)/2)/2)
    return (1+v/2)*left+(1-v/2)*right-I('0.02')


def high_marginal(r, v, s):
    _, D, xs, mv = candidate(r, v)
    c = (1-v)/2
    # Separate masses to the left and right of the deviation center.
    left = I('0.25')*(1-mv)*iv.exp((-v-s)/2)/2
    right = mv*iv.exp((s-1)/2)/2

    def integral(a, z, side):
        if side == 'left':
            return iv.exp((c-s)/2)*(angle(z, c)-angle(a, c))/2
        ta, tz = iv.exp((a-c)/2), iv.exp((z-c)/2)
        return iv.exp((s-c)/2)*(-1/tz-angle(z, c)+1/ta+angle(a, c))/2

    for a, z, entry in ((-v, xs, I('0.25')), (xs, I(1), I(1))):
        if endpoints(s)[1] <= endpoints(a)[0]:
            right += entry*integral(a, z, 'right')
        elif endpoints(s)[0] >= endpoints(z)[1]:
            left += entry*integral(a, z, 'left')
        elif endpoints(s)[0] > endpoints(a)[1] and endpoints(s)[1] < endpoints(z)[0]:
            left += entry*integral(a, s, 'left')
            right += entry*integral(s, z, 'right')
        else:
            raise ValueError('Unresolved interval order at a cut')
    return D*((1-s/2)*left+(1+s/2)*right)-I('0.02')


def uniform_class(r, low, high, p=Q(1,2)):
    cut = min(high, max(low, r))
    rent = ((cut**3-low**3)/3-p*p*(cut-low))/(2*r)
    rent += (high*high-cut*cut)/2-(r/2+p*p/(2*r))*(high-cut)
    g = rent/(high-low)
    win = ((cut*cut-low*low)/(2*r)+high-cut)/(high-low)
    return (low+high)/2-g, g, win


def main():
    print('UTC', datetime.now(timezone.utc).isoformat())
    print('Python', platform.python_version(), 'mpmath', mp.__version__, 'interval digits', iv.dps)
    print('source SHA256', hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    m = 1/(1+iv.exp(1))
    M = 1-m
    record('m', m)
    record('M', M)
    a0, a1, a2 = (auction(Q(s)) for s in ('1.2', '3', '3.6'))
    for n, a in enumerate((a0, a1, a2)):
        for key, value in a.items():
            record(f'r{n}_{key}', value)
        record(f'r{n}_tau', threshold(a))
        record(f'r{n}_B_floor', B(a, m))
    record('A1_lower', Q(6)-(a0['gH']+a0['gL'])/2)
    record('A1_upper', B(a1, M)-6)
    record('A2_lower', Q(1, 50)-a0['D'])
    record('A2_upper', m*I(a1['D'])/8-I('0.02'))
    record('ownership_sufficient_margin', Q(3, 4))
    record('return_cost_margin', 6-B(a2, M))
    record('return_posterior_margin', I(threshold(a2))-M)
    record('return_trade_margin', m*I(a2['D'])/8-I('0.02'))
    record('spread_increase', a2['D']-a1['D'])
    A = 10*M-6
    C = 1-M-I('0.25')
    ceiling = (A+iv.sqrt(A*A+M*C))/M
    record('rC', ceiling)
    record('r2_minus_rC', I('3.6')-ceiling)
    record('rC_derivative_at_r2', -M/2-C/(2*I('3.6')**2))
    record('rN', inverse_spread(Q(4, 25)))
    record('rU', inverse_spread(I('0.16')/m))
    record('r_unique_zero', inverse_spread(Q(1, 50)))
    record('prior_lower', posterior_prior_inverse(threshold(a1)))
    record('prior_upper', posterior_prior_inverse(threshold(a2)))
    record('prior_ii_upper', 1-I('0.24')*iv.exp(1)/(I('0.76')+I('0.24')*iv.exp(1)))
    record('return_cH_lower', B(a2, M))
    record('return_cH_upper', B(a1, M))
    xs, ah, al, ent = full_order_entry(a1)
    record('strong_xstar', xs)
    record('strong_entry', ent)
    record('strong_ownership', (I('0.25')+I('0.75')*ah)/2)
    record('frozen_weak_entry', full_order_entry(a0)[3])
    gainR = I('0.375')*(ah*I(a1['tH']-a1['t0'])+al*I(a1['tL']-a1['t0']))
    gainW = I('0.375')*(ah*I(a1['gH']+Q(1,12)-6)+al*I(a1['gL']+Q(1,12)-6))
    hiddenW = Q(35,24)+Q(1,8)*(a1['gH']+a1['gL']+Q(1,6))
    record('proceeds_gain', gainR)
    record('surplus_gain', gainW)
    record('hidden_surplus', hiddenW)
    record('feedback_surplus', I(hiddenW)+gainW)
    record('stake_omegaU', 4*(m*I(a1['D'])/8-I('0.02'))/(I('0.75')*I(a1['tH']-a1['t0'])))
    record('stake_omega0', I(4*(Q(1,50)-a0['D']))/(I('0.75')*I(a0['tH']-a0['t0'])))
    # Atomless-cost support margins and the logistic threshold.
    record('A6_low_support', B(a1,m)-I('0.2'))
    record('A6_weak_exclusion', Q(59,10)-(a0['gH']+a0['gL'])/2)
    record('A6_strong_entry', B(a1,M)-I('6.1'))
    t=I(threshold(a1)); w=iv.sqrt(t/(1-t)); ee=iv.exp(I('0.5'))
    xl=2*iv.log((ee*w-1)/(ee-w))
    record('logistic_xstar', xl)
    record('logistic_entry', I('0.25')+I('0.375')*(1/(1+iv.exp((xl-1)/2))+1/(1+iv.exp((xl+1)/2))))
    # The uniform-class exhibit uses exact polynomial integrals.
    classes=[]
    for r in (Q(1), Q(9,2), Q(11,2)):
        tH,gH,wH=uniform_class(r,Q(1),Q(19))
        tL,gL,_=uniform_class(r,Q(3,5),Q(7,5))
        classes.append(dict(tH=tH,tL=tL,gH=gH,gL=gL,D=tH-tL,wH=wH))
    cm=I('0.7')/(I('0.7')+I('0.3')*iv.exp(1))
    cM=I('0.7')/(I('0.7')+I('0.3')/iv.exp(1))
    ck=1-cM
    record('caseC_A1_lower', Q(67,10)-(Q(7,10)*classes[0]['gH']+Q(3,10)*classes[0]['gL']))
    record('caseC_A1_upper', B(classes[1],cM)-I('6.7'))
    record('caseC_A2_lower', Q(1,50)-classes[0]['D'])
    record('caseC_A2_upper', ck*I(classes[1]['D'])/8-I('0.02'))
    record('caseC_return', I('6.7')-B(classes[2],cM))
    record('caseC_ownership_sufficient', Q(5,4)*classes[1]['wH']-Q(1,2)*classes[0]['wH'])
    for name, prior, cost, fee, strengths in (
            ('A',Q(3,10),Q(9,2),Q(1,100),('1.1','3','3.6')),
            ('B',Q(7,10),Q(36,5),Q(1,100),('1.1','3','3.6')),
            ('D',Q(7,10),Q(67,10),Q(1,50),('1','4.5','5.5'))):
        aa=[auction(Q(r)) for r in strengths]
        postmin=I(prior)/(I(prior)+I(1-prior)*iv.exp(1))
        postmax=I(prior)/(I(prior)+I(1-prior)/iv.exp(1))
        kap=postmin if prior<Q(1,2) else 1-postmax
        record(f'case{name}_A1_lower', cost-prior*aa[0]['gH']-(1-prior)*aa[0]['gL'])
        record(f'case{name}_A1_upper', B(aa[1],postmax)-I(cost))
        record(f'case{name}_A2_lower', fee-aa[0]['D'])
        record(f'case{name}_A2_upper', kap*I(aa[1]['D'])/8-I(fee))
        record(f'case{name}_return', I(cost)-B(aa[2],postmax))
        record(f'case{name}_ownership_sufficient', Q(3,4))
    am0,am1=auction(Q('1.05'),h=Q(2)),auction(Q('1.5'),h=Q(2))
    record('moderate_A1_lower',Q('0.89')-(am0['gH']+am0['gL'])/2)
    record('moderate_A1_upper',B(am1,M)-I('0.89'))
    record('moderate_A2_lower',Q('0.002')-am0['D'])
    record('moderate_A2_upper',m*I(am1['D'])/8-I('0.002'))
    as0,as1=auction(Q('1.1')),auction(Q('2.3'))
    mup=I('0.3')+I('0.4')*M
    joint=I('0.75')*mup/(I('0.75')*mup+I('0.25')*(1-mup))
    record('signal_A1_lower',Q('7.14')-Q('0.75')*as0['gH']-Q('0.25')*as0['gL'])
    record('signal_A1_upper',B(as1,joint)-I('7.14'))
    record('signal_A2_lower',Q('0.015')-Q('0.4')*(as0['D']+Q('0.15')*Q('0.5')*(as0['tH']-as0['t0'])))
    record('signal_A2_upper',I('0.5')*m*I('0.4')*I('0.85')*I(as1['D'])-I('0.015'))
    for rs, vl, vh in (('1.55','0.46031618','0.46031620'),
                       ('1.60','0.70747537','0.70747539'),
                       ('1.65','0.90333198','0.90333201')):
        r, v = Q(rs), iv.mpf([vl, vh])
        a, D, xs, mv = candidate(r, v)
        record(f'P3_{rs}_Psi_left', low_root(r, I(vl)))
        record(f'P3_{rs}_Psi_right', low_root(r, I(vh)))
        record(f'P3_{rs}_pooling_margin', Q(1,50)-a['D']/8)
        record(f'P3_{rs}_domain_margin', Q(6)-(a['gH']+a['gL'])/2)
        record(f'P3_{rs}_threshold_margin', 1-mv-I(threshold(a)))
        record(f'P3_{rs}_floor', B(a, m))
        grid = [high_marginal(r, v, I(Q(i, 200))) for i in range(201)]
        lower = min(endpoints(g)[0] for g in grid)
        record(f'P3_{rs}_Gamma_H', I(lower)-I(Q(5,4)*a['D']/400))
        record(f'P3_{rs}_entry', I('0.25')+I('0.375')*(1-iv.exp((xs-1)/2)/2+iv.exp(-(xs+v)/2)/2))
    # Read the audit CSV only after all independent computations.
    old = list(csv.DictReader((HERE.parent/'LA'/'margins.csv').open()))
    collapsed = [r['key'] for r in old if r['kind']=='interval' and r['lower']==r['upper']]
    print('LA interval rows with equal decimal endpoints:', len(collapsed), 'of', sum(r['kind']=='interval' for r in old))
    print('Equal endpoints include:', ', '.join(collapsed[:5]))
    with (HERE/'independent_intervals.csv').open('w', newline='') as f:
        w = csv.writer(f)
        w.writerow(('key','lower','upper','sign'))
        w.writerows(ROWS)
    print('Rows:', len(ROWS))


if __name__ == '__main__':
    main()
