"""Print exact flow, payoff, and outcome calculations for the liquidity slot."""
from fractions import Fraction as F
from pathlib import Path
import argparse

RHO, K = F(1, 4), F(1, 50)
LAM, BETA = F(6, 17), F(1, 3)
ZERO, ONE = F(0), F(1)


def auction(r):
    p, ell, h = F(1, 2), F(1), F(10)
    t0 = p * (1 - p / r)
    th = r / 2 + p * p / (2 * r)
    tl = ell - (ell * ell - p * p) / (2 * r)
    gh, gl = h - th, ell - tl
    delta = th - tl
    tau = (6 - gl) / (gh - gl)
    return t0, th, tl, gh, gl, delta, tau


def fmt(x):
    return f"{x} ({float(x):.12f})"


def distribution(menu, zlaw, lam, beta, sh, sl, sell_beta=None):
    sell_beta = beta if sell_beta is None else sell_beta
    eta = {0: 1 - beta, 1: beta} if menu == 'buy' else {-1: sell_beta, 0: 1 - beta - sell_beta, 1: beta}
    ph = {q: (1 - lam) * eta[q] for q in eta}
    pl = dict(ph)
    ph[1] += sh
    ph[0] += lam - sh
    if menu == 'buy':
        pl[0] += lam
    else:
        pl[-1] += sl
        pl[0] += lam - sl
    flows = sorted({q + z for q in eta for z in zlaw})
    ah = {x: sum((v * zlaw.get(x - q, ZERO) for q, v in ph.items()), ZERO) for x in flows}
    al = {x: sum((v * zlaw.get(x - q, ZERO) for q, v in pl.items()), ZERO) for x in flows}
    mu = {x: ah[x] / (ah[x] + al[x]) for x in flows if ah[x] + al[x] > 0}
    return ah, al, mu


def candidate(name, menu, zlaw, lam, beta, r, sh, sl, hidden=False, sell_beta=None):
    t0, th, tl, gh, gl, delta, tau = auction(r)
    ah, al, mu = distribution(menu, zlaw, lam, beta, sh, sl, sell_beta)
    entry = {x: RHO + (1 - RHO) * ((F(1, 2) if hidden else m) >= tau) for x, m in mu.items()}
    prices = {x: t0 + entry[x] * (tl - t0 + delta * mu[x]) for x in mu}
    kh = delta * sum((w * entry[1 + z] * (1 - mu[1 + z]) for z, w in zlaw.items()), ZERO)
    kl = None if menu == 'buy' else delta * sum((w * entry[-1 + z] * mu[-1 + z] for z, w in zlaw.items()), ZERO)
    eh = sum((ah[x] * entry[x] for x in mu), ZERO)
    el = sum((al[x] * entry[x] for x in mu), ZERO)
    total, ownership = (eh + el) / 2, eh / 2
    proceeds = t0 + (eh * (th - t0) + el * (tl - t0)) / 2
    welfare = (eh * (gh + F(1, 4) / r) + el * (gl + F(1, 4) / r)) / 2 - 6 * (total - RHO)
    print(name, 'r', r, 'hidden', hidden, 's_H', sh, 's_L', sl)
    print('  delta', fmt(delta), 'tau', fmt(tau))
    print('  posteriors', ' '.join(f'{x}:{mu[x]}' for x in mu))
    print('  prices', ' '.join(f'{x}:{prices[x]}' for x in prices))
    print('  entry', fmt(total), 'ownership_H', fmt(ownership))
    print('  gross_H', fmt(kh), 'net_H', fmt(kh - K))
    if kl is not None:
        print('  gross_L', fmt(kl), 'net_L', fmt(kl - K))
    print('  proceeds', fmt(proceeds), 'surplus_increment_from_no_entry', fmt(welfare))
    direct_h = sum((w * (t0 + entry[1 + z] * (th - t0) - prices[1 + z]) for z, w in zlaw.items()), ZERO)
    print('  direct_high_value_minus_price', fmt(direct_h))
    for q in ([1] if menu == 'buy' else [-1, 1]):
        uninformed = q * sum((w * (t0 + entry[q + z] * ((th + tl) / 2 - t0) - prices[q + z])
                             for z, w in zlaw.items()), ZERO) - K
        print('  uninformed_order', q, 'net_payoff', fmt(uninformed))
    return total, ownership, proceeds, welfare


def bracket_root(func, lo, hi, n=90):
    flo = func(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (func(mid) > 0) == (flo > 0):
            lo = mid
            flo = func(lo)
        else:
            hi = mid
    return lo, hi, func(lo), func(hi)


def root_line(title, func, lo=F(6, 5), hi=F(4)):
    left, right, fl, fr = bracket_root(func, lo, hi)
    print(title, 'decimal display', f'[{float(left):.12f}, {float(right):.12f}]')
    print('  rational bracket', left, right)
    print('  exact endpoint values', fl, fr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.output:
        import sys
        sys.stdout = Path(args.output).open('w')
    b = (1 - LAM) * BETA
    m = (b + LAM) / (2 * b + LAM)
    n = (1 - b) / (2 * (1 - b) - LAM)
    print('DECLARATION all comparisons use fractions; decimal values are displays only')
    print('lambda', fmt(LAM), 'beta', fmt(BETA), 'b', fmt(b), 'M', fmt(m), 'N', fmt(n))
    for r in [F(6, 5), F(3), F(18, 5), F(31, 20), F(8, 5), F(33, 20)]:
        print('auction', r, ' '.join(fmt(a) for a in auction(r)))
    tau1, tau2 = auction(F(3))[-1], auction(F(18, 5))[-1]
    a1, a2 = (2 * tau1 - 1) / (1 - tau1), (2 * tau2 - 1) / (1 - tau2)
    print('WORKING M interval', tau1, tau2, 'lambda/b interval', a1, a2)
    print('fixed beta lambda interval', a1 * BETA / (1 + a1 * BETA), a2 * BETA / (1 + a2 * BETA))
    laws = [('V1', 'buy', {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}),
            ('V2', 'two', {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}),
            ('V3_buy', 'buy', {0: ONE}), ('V3_two', 'two', {0: ONE})]
    for name, menu, zlaw in laws:
        for r in [F(6, 5), F(3), F(18, 5)]:
            active = r != F(6, 5)
            sh = LAM if active else ZERO
            sl = LAM if active and menu == 'two' else ZERO
            result = candidate(name, menu, zlaw, LAM, BETA, r, sh, sl)
            if r == 3:
                hidden = candidate(name, menu, zlaw, LAM, BETA, r, sh, sl, hidden=True)
                print('  access_differences', ' '.join(fmt(x - y) for x, y in zip(result, hidden)))
    root_line('r_N', lambda r: RHO * auction(r)[5] / 2 - K)
    root_line('r_C', lambda r: auction(r)[4] + m * (auction(r)[3] - auction(r)[4]) - 6)
    root_line('V1_V2 r_F', lambda r: auction(r)[5] * (RHO + 1 - m) / 3 - K)
    root_line('V1_V2 r_A', lambda r: auction(r)[5] * (RHO + 1 - auction(r)[6]) / 3 - K)
    root_line('V3 r_F', lambda r: auction(r)[5] * (1 - m) - K)
    root_line('V3 r_A', lambda r: auction(r)[5] * (1 - auction(r)[6]) - K)
    print('COEXISTENCE POINTS')
    v3_middle_entries = []
    for r in [F(31, 20), F(8, 5), F(33, 20)]:
        delta, tau = auction(r)[5:]
        ss = b * (2 * tau - 1) / (1 - tau)
        print('r', r, 'no_trade_margin', fmt(K - RHO * delta / 2), 'threshold_rate', fmt(ss))
        for label, g, common in [('V1_V2', F(1, 3), RHO), ('V3', ONE, ZERO)]:
            kfull = delta * g * (common + 1 - m)
            kjump = delta * g * (common + 1 - tau)
            e_star = (K / (delta * g) - common) / (1 - tau)
            full_total = RHO + (1 - RHO) * (2 * b + LAM) * g / 2
            mixed_total = RHO + (e_star - RHO) * (2 * b + ss) * g / 2
            recruited_rate = b * (1 / (K / (delta * g) - common) - 2)
            print(label, 'full_margin', fmt(kfull - K), 'jump_margin', fmt(kjump - K),
                  'threshold_entry', fmt(e_star), 'threshold_mixed_total', fmt(mixed_total),
                  'full_total', fmt(full_total), 'recruited_rate', fmt(recruited_rate))
            print('  full_admissible', kfull >= K,
                  'threshold_admissible', ZERO < ss < LAM and RHO <= e_star <= ONE,
                  'recruited_interior_admissible', ss < recruited_rate < LAM)
            if label == 'V3':
                v3_middle_entries.append(mixed_total)
            if ss < recruited_rate < LAM:
                total = RHO + (1 - RHO) * (2 * b + recruited_rate) * g / 2
                print('  recruited_interior_total', fmt(total), 'net_H', ZERO)
    print('V3 threshold entry drops',
          fmt(v3_middle_entries[0] - v3_middle_entries[1]),
          fmt(v3_middle_entries[1] - v3_middle_entries[2]))
    print('V2 MAXIMUM BUY-ONLY COEXISTENCE PAYOFF AT r=1.55')
    r = F(31, 20)
    print(fmt(auction(r)[5] * (RHO + 1 - auction(r)[6]) / 3 - K))
    print('FULL-ORDER FLOOR MARGINS AT r=3')
    print('V1', fmt(RHO * auction(F(3))[5] / 3 - K))
    print('V2', fmt(RHO * auction(F(3))[5] / 6 - K))
    print('V3 working-strip bound', fmt(RHO * auction(F(3))[5] * (1 - tau2) - K))
    print('LITERAL BUY SELL ABSTAIN ORDER')
    lam_extra, beta_extra = F(216, 491), F(12, 25)
    bm = (1 - lam_extra) * (1 - 2 * beta_extra)
    for r in [F(3), F(18, 5)]:
        low_rate = min(lam_extra, bm * (RHO * auction(r)[5] / K - 2))
        for name, zlaw, sl in [
            ('V2_literal', {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}, lam_extra),
            ('V3_two_literal', {0: ONE}, low_rate),
        ]:
            candidate(name, 'two', zlaw, lam_extra, beta_extra, r, lam_extra, sl, sell_beta=1 - 2 * beta_extra)
    candidate('V2_symmetric_extra', 'two', {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)},
              lam_extra, beta_extra, F(3), lam_extra, lam_extra)
    print('SHORT RATIONAL BRACKETS')
    brackets = [
        ('r_N', lambda r: RHO * auction(r)[5] / 2 - K, '1.747877538267', '1.747877538269'),
        ('r_C', lambda r: auction(r)[4] + m * (auction(r)[3] - auction(r)[4]) - 6, '3.458247029058', '3.458247029060'),
        ('V1_V2 r_A', lambda r: auction(r)[5] * (RHO + 1 - auction(r)[6]) / 3 - K, '1.556594422881', '1.556594422883'),
        ('V1_V2 r_F', lambda r: auction(r)[5] * (RHO + 1 - m) / 3 - K, '1.605847158116', '1.605847158118'),
        ('V3 r_A', lambda r: auction(r)[5] * (1 - auction(r)[6]) - K, '1.393957920278', '1.393957920280'),
        ('V3 r_F', lambda r: auction(r)[5] * (1 - m) - K, '1.460984663709', '1.460984663711'),
    ]
    for label, fun, lo, hi in brackets:
        print(label, lo, hi, 'endpoint values', fun(F(lo)), fun(F(hi)))
    print('GEOMETRIC BASE PAYOFFS AT MATCHED BINARY EXPERIMENT')
    dl_hidden = 2 * RHO * m * (1 - m) * auction(F(3))[5]
    dl_access = (1 + RHO) * m * (1 - m) * auction(F(3))[5]
    print('base hidden', fmt(dl_hidden), 'base access', fmt(dl_access))
    print('r_A derivative bounds', 1620 - 170 * F(3, 4) ** 4, 972 - 136 * F(3, 4) ** 4)
    print('r_A maximum trade cost at 1.55', auction(F(31, 20))[5] * (RHO + 1 - auction(F(31, 20))[6]) / 3)
    print('V3 uniform full-order margin at 1.55', auction(F(31, 20))[5] * (1 - tau2) - K)


if __name__ == '__main__':
    main()
