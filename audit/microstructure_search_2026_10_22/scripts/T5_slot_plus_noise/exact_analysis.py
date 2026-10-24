"""Print rational flow calculations and root enclosures for the combined slot."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import platform
from source_slot import auction, bracket_root
from source_bounded import b1

RHO, K = F(1, 4), F(1, 50)
LAM, BETA, THETA = F(5, 11), F(1, 2), F(71, 200)


def flow(lam, beta, theta, s):
    b = (1 - lam) * beta
    f = b1(theta)
    low = {x: (1 - b) * f.get(x, F(0)) + b * f.get(x - 1, F(0)) for x in (-1, 0, 1, 2)}
    high = {x: low[x] + s * (f.get(x - 1, F(0)) - f.get(x, F(0))) for x in low}
    mu = {x: high[x] / (low[x] + high[x]) for x in low}
    mass = {x: (low[x] + high[x]) / 2 for x in low}
    return low, high, mu, mass


def evaluate(r, s, hidden=False):
    t0, tH, tL, gH, gL, delta, tau = auction(r)
    low, high, mu, mass = flow(LAM, BETA, THETA, s)
    es = {x: RHO if hidden or mu[x] < tau else F(1) for x in mu}
    price = {x: t0 + es[x] * (tL - t0 + delta * mu[x]) for x in mu}
    f = b1(THETA)
    UH = sum((w * (t0 + es[z + 1] * (tH - t0) - price[z + 1]) for z, w in f.items()), F(0)) - K
    UL = sum((w * (t0 + es[z + 1] * (tL - t0) - price[z + 1]) for z, w in f.items()), F(0)) - K
    ent = sum((mass[x] * es[x] for x in mass), F(0))
    eh = sum((high[x] * es[x] for x in mass), F(0))
    el = sum((low[x] * es[x] for x in mass), F(0))
    rt = t0 + (eh * (tH - t0) + el * (tL - t0)) / 2
    welfare = (r * r - F(1, 4)) / (2 * r) + (eh * (gH + F(1, 4) / r) + el * (gL + F(1, 4) / r)) / 2 - 6 * (ent - RHO)
    return dict(low=low, high=high, mu=mu, mass=mass, es=es, price=price, UH=UH, UL=UL, entry=ent, ownership=eh / 2, proceeds=rt, welfare=welfare)


def coefficient(s, b, theta, e2):
    a, d = 1 - 2 * theta, 1 - 3 * theta
    a0, a1 = a - b * d, theta + b * d
    return theta * RHO * a0 / (2 * a0 - s * d) + a * RHO * a1 / (2 * a1 + s * d) + theta * e2 * b / (2 * b + s)


def derivative(s, b, theta, e2):
    a, d = 1 - 2 * theta, 1 - 3 * theta
    a0, a1 = a - b * d, theta + b * d
    return theta * RHO * a0 * d / (2 * a0 - s * d) ** 2 - a * RHO * a1 * d / (2 * a1 + s * d) ** 2 - theta * e2 * b / (2 * b + s) ** 2


def entry(s, b, theta, e2=F(1)):
    return RHO + (e2 - RHO) * theta * (b + s / 2)


def star(r, b):
    t = auction(r)[-1]
    return b * (2 * t - 1) / (1 - t)


def display(label, value):
    print(label, value, f'({float(value):.12f})')


def endpoint_line(label, fun, left, right):
    print(label, 'rational bracket', left, right)
    display('left payoff', fun(left))
    display('right payoff', fun(right))


class Interval:
    """Rational closed interval with natural outward arithmetic."""
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)

    def __add__(self, other):
        v = interval(other)
        return Interval(self.lo + v.lo, self.hi + v.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-interval(other))

    def __rsub__(self, other):
        return interval(other) + (-self)

    def __mul__(self, other):
        v = interval(other)
        vals = (self.lo * v.lo, self.lo * v.hi, self.hi * v.lo, self.hi * v.hi)
        return Interval(min(vals), max(vals))

    __rmul__ = __mul__

    def __truediv__(self, other):
        v = interval(other)
        if v.lo <= 0 <= v.hi:
            raise ValueError('The denominator interval contains zero.')
        return self * Interval(1 / v.hi, 1 / v.lo)

    def __rtruediv__(self, other):
        return interval(other) / self

    def __pow__(self, power):
        if power == 0:
            return Interval(1)
        out = self
        for _ in range(power - 1):
            out = out * self
        return out


def interval(value):
    return value if isinstance(value, Interval) else Interval(value)


def region_margins(lam, beta, theta):
    b = (1 - lam) * beta
    m = (b + lam) / (2 * b + lam)
    r1, r2, r3 = F(31, 20), F(8, 5), F(33, 20)
    a, d = 1 - 2 * theta, 1 - 3 * theta
    a0 = a - b * d
    mu0 = (a0 - lam * d) / (2 * a0 - lam * d)
    s1, s2, s3 = (star(r, b) for r in (r1, r2, r3))
    return {
        'M above tau(3)': m - auction(F(3))[-1],
        'M below tau(18/5)': auction(F(18, 5))[-1] - m,
        'middle posterior below tau(3/2)': auction(F(3, 2))[-1] - mu0,
        'top threshold below full at 33/20': lam - s3,
        'negative floor slope at full': -derivative(lam, b, theta, RHO),
        'negative recruited slope at full': -derivative(lam, b, theta, F(1)),
        'positive jump payoff at 31/20': auction(r1)[5] * coefficient(s1, b, theta, F(1)) - K,
        'negative full payoff at 8/5': K - auction(r2)[5] * coefficient(lam, b, theta, F(1)),
        'positive full payoff at 33/20': auction(r3)[5] * coefficient(lam, b, theta, F(1)) - K,
        'positive jump payoff derivative on strength interval': jump_derivative(lam, beta, theta),
    }


def region_certificate():
    radii = (F(1, 1000), F(1, 1000), F(1, 2000))
    centers = (LAM, BETA, THETA)
    print('\nOPEN BOX centers', centers, 'radii', radii)
    partitions = 8
    axes = []
    for center, radius in zip(centers, radii):
        lo, step = center - radius, 2 * radius / partitions
        axes.append([Interval(lo + j * step, lo + (j + 1) * step) for j in range(partitions)])
    ranges = {}
    count = 0
    for la in axes[0]:
        for be in axes[1]:
            for th in axes[2]:
                count += 1
                for key, value in region_margins(la, be, th).items():
                    if key not in ranges:
                        ranges[key] = value
                    else:
                        ranges[key] = Interval(min(ranges[key].lo, value.lo), max(ranges[key].hi, value.hi))
    print('closed rational cells', count)
    for key, value in ranges.items():
        print(key, 'enclosure', value.lo, value.hi, 'decimal', float(value.lo), float(value.hi))
    print('all displayed lower endpoints positive', all(value.lo > 0 for value in ranges.values()))
    return ranges


def jump_derivative(lam, beta, theta):
    r = Interval(F(3, 2), F(7, 4))
    b = (1 - lam) * beta
    den = 4 * (20 * r - r * r - 1)
    tau = (48 * r - 3) / den
    tauprime = (48 * den - (48 * r - 3) * (80 - 8 * r)) / den ** 2
    s = b * (2 * tau - 1) / (1 - tau)
    delta = (r - 1) ** 2 / (2 * r)
    delta_prime = F(1, 2) - F(1, 2) / r ** 2
    return delta_prime * coefficient(s, b, theta, F(1)) + delta * derivative(s, b, theta, F(1)) * b * tauprime / (1 - tau) ** 2


def main():
    b = (1 - LAM) * BETA
    m = (b + LAM) / (2 * b + LAM)
    print('STATUS: computer-assisted rational calculations. No statistical estimate.')
    print('lambda', LAM, 'beta', BETA, 'theta', THETA, 'b', b, 'M', m)
    print('noise', b1(THETA))
    for r in (F(6, 5), F(3), F(18, 5)):
        print('\nBENCHMARK strength', r)
        print('auction', auction(r))
        ev = evaluate(r, F(0) if r == F(6, 5) else LAM)
        for key in ('mu', 'mass', 'es', 'price'):
            print(key, ev[key])
        for key in ('UH', 'UL', 'entry', 'ownership', 'proceeds', 'welfare'):
            display(key, ev[key])
        if r == 3:
            hidden = evaluate(r, LAM, hidden=True)
            for key in ('UH', 'entry', 'proceeds', 'welfare'):
                display('hidden ' + key, hidden[key])
            display('access gain in proceeds', ev['proceeds'] - hidden['proceeds'])
            display('access gain in net surplus', ev['welfare'] - hidden['welfare'])
    print('\nCOMPLETE SCALAR CONDITIONS')
    display('floor coefficient derivative at full', derivative(LAM, b, THETA, RHO))
    display('recruited coefficient derivative at full', derivative(LAM, b, THETA, F(1)))
    for r in (F(31, 20), F(8, 5), F(33, 20)):
        delta, tau = auction(r)[5:]
        st = star(r, b)
        fun = lambda s: delta * coefficient(s, b, THETA, F(1)) - K
        print('\nINTERMEDIATE strength', r)
        display('no-trade deviation payoff', delta * RHO / 2 - K)
        display('top threshold s_T', st)
        display('below-jump payoff', delta * coefficient(st, b, THETA, RHO) - K)
        display('above-jump payoff', fun(st))
        display('full payoff', fun(LAM))
        if fun(st) > 0 > fun(LAM):
            lo, hi, _, _ = bracket_root(fun, st, LAM, n=55)
            scale = 10 ** 12
            lo = F((lo * scale).__floor__(), scale)
            hi = F((hi * scale).__ceil__(), scale)
            endpoint_line('mixed s_A', fun, lo, hi)
            display('alpha lower', lo / LAM)
            display('alpha upper', hi / LAM)
            display('entry lower', entry(lo, b, THETA))
            display('entry upper', entry(hi, b, THETA))
        elif fun(LAM) > 0:
            display('full branch entry', entry(LAM, b, THETA))
        base = coefficient(st, b, THETA, RHO)
        eT = RHO + (K / delta - base) / (THETA * b / (2 * b + st))
        display('threshold challenger preparation probability', (eT - RHO) / (1 - RHO))
        display('threshold total entry', entry(st, b, THETA, eT))
    for name, fun, lo, hi in [
        ('r_A', lambda r: auction(r)[5] * coefficient(star(r, b), b, THETA, F(1)) - K, F(3, 2), F(8, 5)),
        ('r_F', lambda r: auction(r)[5] * coefficient(LAM, b, THETA, F(1)) - K, F(8, 5), F(33, 20)),
        ('r_N', lambda r: RHO * auction(r)[5] / 2 - K, F(17, 10), F(9, 5)),
        ('r_C', lambda r: auction(r)[4] + m * (auction(r)[3] - auction(r)[4]) - 6, F(3), F(18, 5)),
    ]:
        left, right, _, _ = bracket_root(fun, lo, hi, n=55)
        scale = 10 ** 12
        left = F((left * scale).__floor__(), scale)
        right = F((right * scale).__ceil__(), scale)
        endpoint_line(name, fun, left, right)
    print('\nSTRICT REGION MARGINS AT THE POINT')
    for key, value in region_margins(LAM, BETA, THETA).items():
        if isinstance(value, Interval):
            print(key, 'enclosure', value.lo, value.hi, float(value.lo), float(value.hi))
        else:
            display(key, value)
    region_certificate()
    print('\nRUN RECEIPT')
    print('date 2026-10-22; pinned paper commit 01bd5d6; benchmark declared in this file')
    print('Python', platform.python_version())
    for name in ('source_slot.py', 'source_bounded.py', 'exact_analysis.py', 'search.py'):
        path = Path(__file__).with_name(name)
        print(name, 'bytes', path.stat().st_size, 'sha256', sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
