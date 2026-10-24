"""Exact arithmetic for the strategic-trader review. Run from the repository root."""
from fractions import Fraction as F
from pathlib import Path
import sys

L = F(6, 17)
B = F(11, 51)
C = B
RHO = F(1, 4)
K = F(1, 50)
P = F(1, 2)
ORDERS = (-1, 0, 1)


def show(label, value):
    if isinstance(value, F):
        print(f"{label}: {value} ; decimal={float(value):.12f}")
    else:
        print(f"{label}: {value}")


def integral_linear(a, b, intercept, slope):
    return intercept * (b-a) + slope * (b*b-a*a) / 2


def auction(r):
    # Integrate target payments, challenger profits, and total allocation values.
    t0 = P * (r-P) / r
    th = (P*P + (r*r-P*P)/2) / r
    tl = (P*P + (1-P*P)/2 + (r-1)) / r
    gh = (integral_linear(F(0), P, 10-P, 0)
          + integral_linear(P, r, 10, -1)) / r
    gl = (integral_linear(F(0), P, 1-P, 0)
          + integral_linear(P, F(1), 1, -1)) / r
    return dict(r=r, t0=t0, th=th, tl=tl, wh=th-t0, wl=tl-t0,
                d=th-tl, gh=gh, gl=gl, tau=(6-gl)/(gh-gl),
                w=(th+tl)/2-t0, s0=(r*r-P*P)/(2*r),
                sh=F(10), sl=(r*r+1)/(2*r))


def bisect_fraction(fn, lo, hi, iterations=100):
    left = fn(lo)
    for _ in range(iterations):
        mid = (lo+hi)/2
        value = fn(mid)
        if value == 0:
            return mid, mid
        if (left < 0) == (value < 0):
            lo, left = mid, value
        else:
            hi = mid
    return lo, hi


def bracket_print(label, fn, lo, hi, iterations=80):
    low, high = bisect_fraction(fn, lo, hi, iterations)
    show(label + " lower", low)
    show(label + " upper", high)
    show(label + " signs", (str(fn(low)), str(fn(high))))
    return low, high


def holder_profile(r, stake, s, t, m, ep):
    a = auction(r)
    masses = {
        1: (L*s+B+C*m, B+C*m),
        -1: (B, B+L*t),
        0: (L*(1-s)+C*(1-m), L*(1-t)+C*(1-m)),
    }
    mu, entry, price = {}, {}, {}
    for q in ORDERS:
        ah, al = masses[q]
        mu[q] = ah/(ah+al) if ah+al else F(1, 2)
        entry[q] = ep if q == 1 else RHO
        price[q] = a['t0']+entry[q]*(a['wl']+a['d']*mu[q])
    gains = {
        0: F(0),
        1: stake*(entry[1]-entry[0])*a['w']
           +a['t0']+entry[1]*a['w']-price[1]-K,
        -1: stake*(entry[-1]-entry[0])*a['w']
            +price[-1]-a['t0']-entry[-1]*a['w']-K,
    }
    hi = {q: q*(a['t0']+entry[q]*a['wh']-price[q])-K*abs(q) for q in ORDERS}
    low = {q: q*(a['t0']+entry[q]*a['wl']-price[q])-K*abs(q) for q in ORDERS}
    mean_entry = sum((sum(masses[q])/2)*entry[q] for q in ORDERS)
    print(f"profile r={r} stake={stake} s={s} t={t} m={m} ep={ep}")
    for label, item in [('mu', mu), ('holder_gain', gains), ('H_payoff', hi), ('L_payoff', low)]:
        print(label, {key: str(value) for key, value in item.items()})
    show('entry', mean_entry)
    show('price_gaps', (str(price[0]-price[-1]), str(price[1]-price[0])))
    return mean_entry


def holder_thresholds(r):
    a = auction(r)
    top = (L+B)/(L+2*B)
    o1 = (a['d']*(top-F(1, 2))+K)/((1-RHO)*a['w'])
    o2 = (a['d']*(a['tau']-F(1, 2))+K)/((1-RHO)*a['w'])
    cap = (L*(1-a['tau'])-B*(2*a['tau']-1))/(C*(2*a['tau']-1))
    bar = K*a['d']/(2*a['w']*(K-RHO*a['d']*(1-a['tau'])))
    return o1, o2, cap, bar


def welfare(r, m, ep):
    a = auction(r)
    masses = {1: (L+B+C*m, B+C*m), -1: (B, B+L), 0: (C*(1-m), C*(1-m))}
    target = challenger = incumbent = allocation = F(0)
    investor = holder_trade = F(0)
    for q, (ah, al) in masses.items():
        e = ep if q == 1 else RHO
        mu = ah/(ah+al) if ah+al else F(1, 2)
        price = a['t0']+e*(a['wl']+a['d']*mu)
        for mass, tj, gj, sj, vj in [(ah, a['th'], a['gh'], a['sh'], F(10)),
                                    (al, a['tl'], a['gl'], a['sl'], F(1))]:
            target += mass*(a['t0']+e*(tj-a['t0']))/2
            challenger += mass*(e*gj-(e-RHO)*6)/2
            incumbent += mass*((1-e)*(r-P)**2/(2*r)+e*(sj-vj))/2
            allocation += mass*(a['s0']+e*(sj-a['s0'])-(e-RHO)*6)/2
        forced_mass = B if q else F(0)
        free_mass = C*m if q == 1 else F(0)
        holder_trade += (forced_mass+free_mass)*(q*(a['t0']+e*a['w']-price)-K*abs(q))
        if q == 1:
            investor += L*(a['t0']+e*a['wh']-price-K)/2
        elif q == -1:
            investor += L*(price-a['t0']-e*a['wl']-K)/2
    fees = K*(L+2*B+C*m)
    return dict(target=target, challenger=challenger, incumbent=incumbent,
                investor=investor, holder_trade=holder_trade, net_surplus=allocation-fees,
                auction_identity_gap=allocation-target-challenger-incumbent)


def holder_part():
    print('\nPART 1: HOLDER')
    for r in [F(6,5), F(3), F(18,5), F(31,20), F(8,5), F(33,20)]:
        a = auction(r)
        print('auction', {key: str(value) for key,value in a.items()})
    o1, o2, cap, _ = holder_thresholds(F(3))
    for label, value in [('Omega1(3)', o1), ('Omega2(3)', o2), ('mmax(3)', cap)]:
        show(label, value)
    for stake in [o2, F(392,1425), o1, F(1), F(10)]:
        a = auction(F(3))
        ep = (K+RHO*stake*a['w'])/(stake*a['w']-a['d']*(a['tau']-F(1,2)))
        holder_profile(F(3), stake, F(1), F(1), cap, ep)
    print('\nWELFARE: every row uses the same auction and actual trade fees')
    hidden = welfare(F(3), F(0), RHO)
    base = welfare(F(3), F(0), F(1))
    for label, row in [('hidden', hidden), ('V3', base)]:
        print(label)
        for key,value in row.items(): show(key,value)
    for stake in [F(27,100), o2, F(3,10), F(1), F(10)]:
        a = auction(F(3))
        if stake == F(27,100):
            ep = F(1)
            aa = stake*(1-RHO)*a['w']-K
            m = (L*a['d']/(2*aa)-L-2*B)/(2*C)
        else:
            m = cap
            ep = (K+RHO*stake*a['w'])/(stake*a['w']-a['d']*(a['tau']-F(1,2)))
        row = welfare(F(3), m, ep)
        print('manipulation stake', stake)
        for key,value in row.items(): show(key,value)
        show('proceeds minus V3',row['target']-base['target'])
        show('surplus gain relative to hidden',row['net_surplus']-hidden['net_surplus'])
        show('discovery gain retained',(row['net_surplus']-hidden['net_surplus'])/(base['net_surplus']-hidden['net_surplus']))
    print('\nRECOVERED ENTRY: full-purchase outcome and partial-purchase outcome')
    strengths = [F(31,20), F(8,5), F(33,20)]
    for r in strengths:
        o1r, o2r, mr, barr = holder_thresholds(r)
        for label,value in [('r',r),('Omega1',o1r),('Omega2',o2r),('mmax',mr),('bar_omega_H',barr)]: show(label,value)
        a = auction(r)
        sstar = B*(2*a['tau']-1)/(L*(1-a['tau']))
        ebase = K/(a['d']*(1-a['tau']))
        for stake in [F(7,50),F(3,20)]:
            ep = (K+RHO*stake*a['w'])/(stake*a['w']-a['d']*(a['tau']-F(1,2)))
            print('full-purchase threshold profile')
            holder_profile(r, stake, F(1), F(0), mr, ep)
            print('partial-purchase threshold profile')
            holder_profile(r, stake, sstar, F(0), F(0), ebase)
    left = holder_thresholds(strengths[-1])[0]
    right = holder_thresholds(strengths[0])[3]
    show('entry-window left',left)
    show('entry-window right',right)
    # Each entry difference has a linear numerator in the stake.
    coeffs=[]
    for r in strengths:
        a=auction(r)
        dmass=L/(2*(2*a['tau']-1))
        bb=a['d']*(a['tau']-F(1,2))
        coeffs.append((dmass*(K+RHO*bb),a['w'],bb))
    for first,second in zip(coeffs,coeffs[1:]):
        c1,a1,b1=first; c2,a2,b2=second
        slope=c2*a1-c1*a2; intercept=c1*b2-c2*b1
        show('entry-difference numerator slope',slope)
        show('entry-difference numerator intercept',intercept)
        show('entry-difference numerator at left',slope*left+intercept)
        show('entry-difference numerator at right',slope*right+intercept)
    # I0 can permit a strict pure purchase by the free holder near r_F.
    r=F(147,100); a=auction(r)
    show('I0 example mmax', holder_thresholds(r)[2])
    holder_profile(r,F(1,10),F(1),F(0),F(1),F(1))


def liquidity_part():
    print('\nPART 2: PRICE-SENSITIVE LIQUIDITY')
    bhat=(1-L)*F(2,5); vmax=F(51,50)
    def quadratic(r,e,b):
        a=auction(r)
        return (2*b*b+(L-2*bhat*(1-K/vmax))*b
                -bhat*(1-K/vmax)*L+bhat*e*a['d']*L/(2*vmax))
    def root(r,e):
        return bisect_fraction(lambda b:quadratic(r,e,b),F(0),bhat,90)
    def btau(r):
        tau=auction(r)['tau']
        return L*(1-tau)/(2*tau-1)
    for e,label in [(RHO,'lower coexistence endpoint'),(F(1),'upper coexistence endpoint')]:
        bracket_print(label,lambda r:quadratic(r,e,btau(r)),F(3),F(4),80)
    for r in [F(3),F(18,5)]:
        a=auction(r)
        sale_lo,sale_hi=root(r,RHO)
        for e in [F(1),RHO]:
            blo,bhi=root(r,e)
            b=(blo+bhi)/2; bs=(sale_lo+sale_hi)/2
            mu=(L+b)/(L+2*b); mum=bs/(L+2*bs)
            show('r',r);show('buy entry',e)
            show('buy mass lower',blo);show('buy mass upper',bhi)
            show('buy posterior',mu);show('posterior minus threshold',mu-a['tau'])
            show('buy participation',b/bhat)
            show('sell mass lower',sale_lo);show('sell mass upper',sale_hi)
            show('H buy net',e*a['d']*(1-mu)-K)
            show('L sell net',RHO*a['d']*mum-K)
            show('total entry',RHO+(e-RHO)*(b+L/2))
            show('mass residual',quadratic(r,e,b))
        b=btau(r)
        et=(vmax*(1-b/bhat)-K)/(a['d']*(a['tau']-F(1,2)))
        show('CM threshold buy mass',b);show('CM threshold entry',et)
        show('CM threshold H buy net',et*a['d']*(1-a['tau'])-K)
    show('no-informed-trade liquidity mass',bhat*(1-K/vmax))


def challenger_part():
    print('\nPART 3: CHALLENGER')
    a=auction(F(3))
    vh=a['t0']+RHO*a['wh']; vl=a['t0']+RHO*a['wl']
    vliq=a['t0']+RHO*a['w']; vch=a['t0']+a['w']
    threshold=B*(vh-K-vliq)/(RHO*(vch-vh+K))
    show('challenger presence threshold',threshold)
    for chi in [F(1,51),F(1,17),threshold,threshold+F(1,1000),F(2,17)]:
        t=min(F(1),2*(B*(vliq-vl-K)-chi*(1-RHO)*(vl+K-a['t0']))/(L*K))
        d0=1-L-chi-2*B
        mu0=(d0+L)/(2*d0+L*(2-t))
        pbuy=(B*vliq+chi*RHO*vch)/(B+chi*RHO)
        e0=F(1) if mu0>=a['tau'] else RHO
        show('chi',chi);show('toehold informed sale probability',t)
        show('outside zero posterior',mu0)
        show('H purchase net',vh-pbuy-K)
        show('toehold entry',RHO+(e0-RHO)*(d0+L*(1-t/2)))
    for r in [F(6,5),F(3),F(18,5)]:
        a=auction(r)
        mu=F(1,2) if r==F(6,5) else (L+B)/(L+2*B)
        mum=1-mu
        e=F(1) if r==F(3) else RHO
        show('r',r)
        show('rare low-cost buy',(1-e)*a['wl']+a['d']*(F(1,2)-e*mu)-K)
        show('rare high-cost sale',RHO*(a['wl']+a['d']*mum)-K)


def incumbent_part():
    print('\nPART 4: INCUMBENT')
    a=auction(F(3));r=F(3)
    ih=L/2; mass=ih+B
    vh=a['t0']+RHO*a['wh'];vl=a['t0']+RHO*a['wl'];vu=a['t0']+RHO*a['w']
    base_value=ih*vh+B*vu
    def buy_eq(d,chi):
        value=F(1,2)+d/8
        numerator=base_value+chi*(3-d)*(F(1,2)+(3+d)/16)/3
        denominator=mass+chi*(3-d)/3
        return value-K-numerator/denominator
    def buy_root(chi):
        return bisect_fraction(lambda d:buy_eq(d,chi),F(1),F(2),90)
    def sale_value_integral(s):
        return RHO*P*P+integral_linear(P,s,F(3,8),RHO)
    def sell_eq(s,chi):
        price=(ih*vl+B*vu+chi*sale_value_integral(s)/3)/(mass+chi*s/3)
        return F(3,8)+s/4-price+K
    def sale_root(chi):
        return bisect_fraction(lambda s:sell_eq(s,chi),P,F(1),90)
    base_margin=ih*(a['gh']-6)+B*((a['gh']+a['gl'])/2-6)
    show('gross preparation margin without incumbent',base_margin)
    for chi in [F(1,51),F(1,17),F(13,170),F(2,17)]:
        dlo,dhi=buy_root(chi);d=(dlo+dhi)/2
        slo,shi=sale_root(chi)
        incmass=chi*(3-d)/3
        mu=(ih+B/2+incmass/2)/(mass+incmass)
        predicted=a['gl']+mu*(a['gh']-a['gl'])
        actual=(ih*a['gh']+B*(a['gh']+a['gl'])/2+chi*(3-d)*(17-d)/12)/(mass+incmass)
        show('chi',chi);show('buy cutoff lower',dlo);show('buy cutoff upper',dhi)
        show('sale cutoff lower',slo);show('sale cutoff upper',shi)
        show('class posterior at buy',mu)
        show('gross preparation value with unconditional R',predicted)
        show('gross preparation value conditional on order',actual)
    # Eliminate chi from the buy cutoff and the preparation condition.
    def critical_d_eq(d):
        return 3*(mass*(F(1,2)+d/8-K)-base_value)*(7+d)-12*base_margin*((3-d)/16+K)
    dl,dh=bracket_print('correct incumbent threshold cutoff',critical_d_eq,F(1),F(2),100)
    def chi_true(d):
        return 12*base_margin/((3-d)*(7+d))
    show('correct incumbent chi lower',chi_true(dl));show('correct incumbent chi upper',chi_true(dh))
    # The class-only criterion replaces the selected R law by the original uniform law.
    top=a['tau'];qmass=L*(1-top)/(2*top-1)-B
    def old_d_eq(d):
        return buy_eq(d,qmass*3/(3-d))
    ol,oh=bracket_print('class-only threshold cutoff',old_d_eq,F(1),F(2),90)
    show('class-only chi lower',qmass*3/(3-ol));show('class-only chi upper',qmass*3/(3-oh))
    show('recruiting incumbent purchase upper bound at zeta=1',F(1,2)+F(3,8)-F(163,120)-K)


def main():
    print('Independent exact derivation. No source module is imported.')
    holder_part()
    liquidity_part()
    challenger_part()
    incumbent_part()


if __name__ == '__main__':
    if len(sys.argv)>1:
        with Path(sys.argv[1]).open('w') as output:
            original=sys.stdout
            sys.stdout=output
            main()
            sys.stdout=original
        print('Wrote',sys.argv[1])
    else:
        main()
