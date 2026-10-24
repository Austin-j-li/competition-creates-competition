"""Print exact auction values and high-precision acquisition equilibria."""

from fractions import Fraction
from typing import NamedTuple

import mpmath as mp

mp.mp.dps = 90


class Auction(NamedTuple):
    r: Fraction
    t0: Fraction
    th: Fraction
    tl: Fraction
    gh: Fraction
    gl: Fraction
    spread: Fraction


def auction(r: Fraction) -> Auction:
    p, ell, h = Fraction(1, 2), Fraction(1), Fraction(10)
    t0 = p * (1 - p / r)
    th = r / 2 + p * p / (2 * r)
    tl = ell - (ell * ell - p * p) / (2 * r)
    return Auction(r, t0, th, tl, h - th, ell - tl, th - tl)


def high(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def display(name: str, value: object) -> None:
    if isinstance(value, mp.mpf):
        print(name, mp.nstr(value, 48))
    else:
        print(name, value)


rho, prior, k = mp.mpf('0.25'), mp.mpf('0.5'), mp.mpf('0.02')
a = mp.exp(-mp.mpf('0.5'))
d = 1 - a


def posterior(s: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    y = prior * d * s
    low = prior * (1 - d * s) / (1 - y)
    upper = prior * (a + d * s) / (a + y)
    return low, upper


def benefit(values: Auction, belief: mp.mpf) -> mp.mpf:
    return high(values.gl) + belief * high(values.gh - values.gl)


def gross(values: Auction, s: mp.mpf, cost: mp.mpf) -> mp.mpf:
    lower, upper = posterior(s)
    e0 = mp.mpf(1) if benefit(values, lower) >= cost else rho
    e1 = mp.mpf(1) if benefit(values, upper) >= cost else rho
    return high(values.spread) * (
        a * e0 * (1 - lower) + e1 * (1 - upper)
    ) / (1 + a)


def branch_value(values: Auction, s: mp.mpf, e1: mp.mpf) -> mp.mpf:
    y = prior * d * s
    scale = high(values.spread) * (1 - prior) * a / (1 + a)
    return prior * (scale * (rho / (1 - y) + e1 / (a + y)) - k)


def root(values: Auction, cost: mp.mpf, left: mp.mpf,
         right: mp.mpf, e1: mp.mpf) -> mp.mpf:
    for _ in range(320):
        midpoint = (left + right) / 2
        if branch_value(values, midpoint, e1) > cost:
            left = midpoint
        else:
            right = midpoint
    return (left + right) / 2


def equilibrium(values: Auction, cost: mp.mpf,
                research_cost: mp.mpf) -> tuple[mp.mpf, ...]:
    v0 = prior * max(gross(values, mp.mpf(0), cost) - k, mp.mpf(0))
    v1 = prior * (gross(values, mp.mpf(1), cost) - k)
    points = []
    if research_cost >= v0:
        points.append(mp.mpf(0))
    if research_cost <= v1:
        points.append(mp.mpf(1))
    tau = (cost - high(values.gl)) / high(values.gh - values.gl)
    if prior < tau <= posterior(mp.mpf(1))[1]:
        threshold = a * (tau - prior) / (prior * d * (1 - tau))
        before = branch_value(values, threshold, rho)
        after = branch_value(values, threshold, mp.mpf(1))
        if before < research_cost < v0:
            points.append(root(values, research_cost, mp.mpf(0), threshold, rho))
        if v1 < research_cost <= after:
            points.append(root(values, research_cost, threshold, mp.mpf(1), mp.mpf(1)))
    elif tau > posterior(mp.mpf(1))[1] and v1 < research_cost < v0:
        points.append(root(values, research_cost, mp.mpf(0), mp.mpf(1), rho))
    return tuple(sorted(points))


def outcomes(values: Auction, cost: mp.mpf, research_cost: mp.mpf,
             s: mp.mpf) -> tuple[mp.mpf, ...]:
    upper = posterior(s)[1]
    probability = (a + prior * d * s) / (1 + a)
    recruited = benefit(values, upper) >= cost
    addition = (1 - rho) * probability if recruited else mp.mpf(0)
    entry = rho + addition
    ownership = prior * rho
    entry_gain = mp.mpf(0)
    if recruited:
        ownership += (1 - rho) * prior * (a + d * s) / (1 + a)
        entry_gain = addition * (benefit(values, upper) - cost + high(Fraction(1, 4) / values.r))
    welfare = entry_gain - s * research_cost - prior * s * k
    return entry, ownership, entry_gain, welfare


print('Precision: 90 decimal places. Costs are per share. No tail truncation enters the formulas.')
print('Equal noise: exact rational auction values and research returns')
for r in (Fraction(6, 5), Fraction(3), Fraction(18, 5), Fraction(17, 2)):
    values = auction(r)
    net = Fraction(1, 4) * values.spread / 3 - Fraction(1, 50)
    value = max(net, Fraction(0)) / 2
    display('auction', values)
    display('research_value_equal_noise', value)
    display('research_value_equal_noise_decimal', high(value))

print('Discrete Laplace: analytic tail classes')
display('a', a)
display('m', a / (1 + a))
display('M', 1 / (1 + a))
values = auction(Fraction(3))
cost = mp.mpf(5)
tau = (cost - high(values.gl)) / high(values.gh - values.gl)
threshold = a * (tau - prior) / (prior * d * (1 - tau))
display('tau_at_r3_cH5', tau)
display('entry_threshold_s', threshold)
display('V0', branch_value(values, mp.mpf(0), rho))
display('VE_before', branch_value(values, threshold, rho))
display('VE_after', branch_value(values, threshold, mp.mpf(1)))
display('V1', branch_value(values, mp.mpf(1), mp.mpf(1)))
display('V1_without_high_cost_entry', branch_value(values, mp.mpf(1), rho))
display('conditional_H_profit_with_entry', gross(values, mp.mpf(1), cost) - k)
display('conditional_H_profit_without_entry', branch_value(values, mp.mpf(1), rho) / prior)

for research_cost in map(mp.mpf, ('0.02', '0.03', '0.05', '0.09', '0.094', '0.095')):
    display('kappa', research_cost)
    points = equilibrium(values, cost, research_cost)
    print('equilibria', ', '.join(mp.nstr(s, 36) for s in points))
    for s in points:
        display('psi', s)
        display('acquisition_value', prior * max(gross(values, s, cost) - k, mp.mpf(0)))
        if 0 < s < 1:
            e1 = mp.mpf(1) if s >= threshold else rho
            scale = high(values.spread) * (1 - prior) * a / (1 + a)
            level = k + research_cost / prior
            coefficient_b = scale * (rho - e1) - level * d
            coefficient_c = scale * (rho * a + e1) - level * a
            discriminant = coefficient_b ** 2 - 4 * level * coefficient_c
            algebraic_s = (-coefficient_b - mp.sqrt(discriminant)) / (2 * level * prior * d)
            display('quadratic_root', algebraic_s)
            display('quadratic_minus_interval_root', algebraic_s - s)
        for name, value in zip(('entry', 'ownership_H', 'entry_allocation_gain', 'net_welfare_with_real_trade_cost'),
                               outcomes(values, cost, research_cost, s)):
            display(name, value)

print('Proposition 2 comparison: cH=5, kappa=0.02')
for r in (Fraction(6, 5), Fraction(3), Fraction(21, 5)):
    values = auction(r)
    display('r', r)
    display('B_prior', benefit(values, prior))
    display('B_M', benefit(values, posterior(mp.mpf(1))[1]))
    display('uniform_research_lower_bound', prior * (rho * a / (1 + a) * high(values.spread) - k))
    points = equilibrium(values, cost, mp.mpf('0.02'))
    print('equilibria', ', '.join(mp.nstr(s, 36) for s in points))
    for s in points:
        print('outcomes', ', '.join(mp.nstr(v, 36) for v in outcomes(values, cost, mp.mpf('0.02'), s)))

print('Original high cost: cH=6, r=3, kappa=0.03')
values = auction(Fraction(3))
points = equilibrium(values, mp.mpf(6), mp.mpf('0.03'))
print('equilibria', ', '.join(mp.nstr(s, 36) for s in points))
for s in points:
    print('outcomes', ', '.join(mp.nstr(v, 36) for v in outcomes(values, mp.mpf(6), mp.mpf('0.03'), s)))

print('Research need not rise with strength: cH=5, kappa=0.06')
for r in (Fraction(199, 50), Fraction(399, 100), Fraction(4), Fraction(21, 5)):
    values = auction(r)
    display('r', r)
    display('B_M', benefit(values, posterior(mp.mpf(1))[1]))
    display('V0', branch_value(values, mp.mpf(0), rho))
    points = equilibrium(values, cost, mp.mpf('0.06'))
    print('equilibria', ', '.join(mp.nstr(s, 36) for s in points))

print('Equal noise: research threshold and welfare, cH=6, kappa=0.01')
research_cost_exact = Fraction(1, 100)
spread_cutoff = 6 * (research_cost_exact + Fraction(1, 100)) / Fraction(1, 4)
display('spread_cutoff', spread_cutoff)
display('strength_cutoff', 1 + high(spread_cutoff) + mp.sqrt(high(spread_cutoff) ** 2 + 2 * high(spread_cutoff)))
values = auction(Fraction(3))
entry_gain_exact = Fraction(1, 8) * (values.gh - 6 + Fraction(1, 4) / values.r)
display('entry_gain', entry_gain_exact)
display('net_welfare_with_real_trade_cost', entry_gain_exact - research_cost_exact - Fraction(1, 100))

print('Independent finite-flow sums: fixed schedules, both post-acquisition actions')
for s in (mp.mpf('0'), mp.mpf('0.5'), mp.mpf('0.8'), mp.mpf('1')):
    values = auction(Fraction(3))
    profit_h = mp.mpf(0)
    profit_l = mp.mpf(0)
    for z in range(-400, 401):
        probability = (1 - a) / (1 + a) * a ** abs(z)
        x = z + 1
        n0 = (1 - a) / (1 + a) * a ** abs(x)
        n1 = (1 - a) / (1 + a) * a ** abs(x - 1)
        fh = (1 - s) * n0 + s * n1
        belief = prior * fh / (prior * fh + (1 - prior) * n0)
        rate = mp.mpf(1) if benefit(values, belief) >= cost else rho
        price = high(values.t0) + rate * (high(values.tl - values.t0) + high(values.spread) * belief)
        payoff_h = high(values.t0) + rate * high(values.th - values.t0)
        payoff_l = high(values.t0) + rate * high(values.tl - values.t0)
        profit_h += probability * (payoff_h - price)
        profit_l += probability * (payoff_l - price)
    display('s', s)
    display('H_buy_net_finite_sum', profit_h - k)
    display('H_buy_net_closed_form', gross(values, s, cost) - k)
    display('difference', profit_h - gross(values, s, cost))
    display('L_buy_net_finite_sum', profit_l - k)
    display('both_zero_orders', mp.mpf(0))
display('absolute_tail_error_bound_gross_H', 2 * high(values.spread) * a ** 401 / (1 + a))

print('Information ceiling: solve B_r(M)=5')
upper = posterior(mp.mpf(1))[1]
numerator = upper * 10 - 5
ceiling = (numerator + mp.sqrt(numerator ** 2 + upper * ((1 - upper) - mp.mpf('0.25')))) / upper
display('r_ceiling_dlaplace_cH5', ceiling)
display('r_ceiling_equal_noise_cH6', 4 + mp.sqrt(mp.mpf('15.75')))
