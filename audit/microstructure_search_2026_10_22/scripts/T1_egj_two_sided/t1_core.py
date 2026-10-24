"""Exact primitives for workstream T1.

Model: Reading N with point masses (h, ell), prior pi; two-sided unit orders
q in {-1, 0, 1}; noise Z in {-1, 0, 1} with weights (theta, 1 - 2 theta, theta);
the informed investor is present with probability lam; flow X = q + Z;
competitive price P = E[V_T | X]; the challenger sees the price and its cost;
c_L = 0; the paper's second-price auction with reserve p.

Every function uses fractions.Fraction. Nothing here prints or asserts.

Strategy notation after the dominance reduction:
  a = lam * Pr(H buys | present),  b = lam * Pr(L sells | present).
"""
from fractions import Fraction as F
from math import isqrt

FLOWS = (-2, -1, 0, 1, 2)


def bench(**over):
    """Benchmark parameter record (paper, Appendix A.8, with c_L = 0)."""
    P = dict(h=F(10), ell=F(1), p=F(1, 2), rho=F(1, 4), cH=F(6), k=F(1, 50),
             pi=F(1, 2), r=F(3), lam=F(1), theta=F(1, 3))
    for key, val in over.items():
        P[key] = F(val)
    return P


def auction(P):
    """Auction objects of TEAM_RULES section 3 (paper eq. (4)); needs p < ell < r < h."""
    h, ell, p, r = P['h'], P['ell'], P['p'], P['r']
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    D = (r - ell) ** 2 / (2 * r)
    tau = (P['cH'] - gL) / (gH - gL)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D, wH=tH - t0, wL=tL - t0,
                tau=tau, base=(r * r - p * p) / (2 * r), pF=p * p / r)


def auction_by_integration(P):
    """Same objects from the piecewise integrals over R ~ U[0, r] (independent check)."""
    h, ell, p, r = P['h'], P['ell'], P['p'], P['r']
    # no entry: incumbent buys at p when R >= p
    t0 = (r - p) * p / r
    # high challenger (value h > r) always wins and pays max(p, R)
    tH = (p * p + (r * r - p * p) / 2) / r
    gH = h - tH
    # low challenger: target gets max(p, min(R, ell)); challenger keeps (ell - max(p, R))_+
    tL = (p * p + (ell * ell - p * p) / 2 + (r - ell) * ell) / r
    gL = ((ell - p) * p + (ell - p) ** 2 / 2) / r
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL)


def noise(theta):
    return {-1: theta, 0: 1 - 2 * theta, 1: theta}


def flow_laws(P, a, b):
    """Class-conditional flow laws f_H(x), f_L(x) for effective rates (a, b)."""
    n = noise(P['theta'])
    fH, fL = {}, {}
    for x in FLOWS:
        fH[x] = (1 - a) * n.get(x, 0) + a * n.get(x - 1, 0)
        fL[x] = (1 - b) * n.get(x, 0) + b * n.get(x + 1, 0)
    return fH, fL


def flow_laws_general(P, sH, sL):
    """Flow laws for general mixed strategies sH, sL: dicts q -> prob (given presence)."""
    n = noise(P['theta'])
    lam = P['lam']
    out = []
    for s in (sH, sL):
        f = {}
        for x in FLOWS:
            val = (1 - lam) * n.get(x, 0)
            for q, pr in s.items():
                val += lam * pr * n.get(x - q, 0)
            f[x] = val
        out.append(f)
    return out[0], out[1]


def posteriors(P, fH, fL, v_off):
    """Posterior at each flow; v_off maps an unused flow to its off-path belief."""
    pi = P['pi']
    mu, used = {}, {}
    for x in FLOWS:
        den = pi * fH[x] + (1 - pi) * fL[x]
        used[x] = den > 0
        mu[x] = pi * fH[x] / den if den > 0 else v_off[x]
    return mu, used


def B(A, mu):
    return A['gL'] + mu * (A['gH'] - A['gL'])


def entry_options(P, A, mu):
    """Entry correspondence at posterior mu (c_L = 0): ('fix', e) or ('tie', (rho, 1))."""
    val = B(A, mu) - P['cH']
    if val > 0:
        return ('fix', F(1))
    if val < 0:
        return ('fix', P['rho'])
    return ('tie', (P['rho'], F(1)))


def entry_rule_E(P, A, mu):
    """Entry when an indifferent high-cost challenger prepares (the paper's rule)."""
    return F(1) if B(A, mu) >= P['cH'] else P['rho']


def order_payoffs(P, A, mu, e):
    """Gross payoff of each order for each class, holding the schedule fixed.

    Returns dict (class, q) -> gross payoff (before the cost k|q|).
    Residuals: E[V_T | H, x] - P(x) = e_x D (1 - mu_x); E[V_T | L, x] - P(x) = -e_x D mu_x.
    """
    n = noise(P['theta'])
    D = A['D']
    out = {}
    for j in ('H', 'L'):
        for q in (-1, 1):
            tot = F(0)
            for z, pz in n.items():
                x = q + z
                res = e[x] * D * (1 - mu[x]) if j == 'H' else -e[x] * D * mu[x]
                tot += pz * q * res
            out[(j, q)] = tot
    return out


def outcomes(P, A, fH, fL, mu, e):
    """Entry, high-class ownership, proceeds, net surplus, price informativeness."""
    pi, rho = P['pi'], P['rho']
    E = sum((pi * fH[x] + (1 - pi) * fL[x]) * e[x] for x in FLOWS)
    OH = pi * sum(fH[x] * e[x] for x in FLOWS)
    RT = A['t0'] + OH * A['wH'] + (E - OH) * A['wL']
    W = A['base'] + OH * (A['gH'] + A['pF']) + (E - OH) * (A['gL'] + A['pF']) - P['cH'] * (E - rho)
    m1 = sum((pi * fH[x] + (1 - pi) * fL[x]) * mu[x] for x in FLOWS
             if pi * fH[x] + (1 - pi) * fL[x] > 0)
    m2 = sum((pi * fH[x] + (1 - pi) * fL[x]) * mu[x] ** 2 for x in FLOWS
             if pi * fH[x] + (1 - pi) * fL[x] > 0)
    return dict(E=E, OH=OH, RT=RT, W=W, VarMu=m2 - m1 * m1)


def fmt(q, digits=6):
    """Exact fraction followed by a decimal."""
    q = F(q)
    if q.denominator == 1:
        return f"{q.numerator}"
    if q.denominator < 10 ** 7:
        return f"{q.numerator}/{q.denominator} = {float(q):.{digits}f}"
    return f"{float(q):.{digits}f}"


# ---------------------------------------------------------------------------
# Exact interval arithmetic with rational endpoints (used for certificates).
# ---------------------------------------------------------------------------
class Iv:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        lo = F(lo)
        hi = lo if hi is None else F(hi)
        self.lo, self.hi = (lo, hi) if lo <= hi else (hi, lo)

    @staticmethod
    def of(x):
        return x if isinstance(x, Iv) else Iv(x)

    def __add__(self, o):
        o = Iv.of(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-Iv.of(o))

    def __rsub__(self, o):
        return Iv.of(o) - self

    def __mul__(self, o):
        o = Iv.of(o)
        c = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Iv(min(c), max(c))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Iv.of(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError('interval divisor contains zero')
        return self * Iv(1 / o.hi, 1 / o.lo)

    def __rtruediv__(self, o):
        return Iv.of(o) / self

    def __pow__(self, n):
        out = Iv(1)
        for _ in range(n):
            out = out * self
        return out

    def pos(self):
        return self.lo > 0

    def neg(self):
        return self.hi < 0

    def width(self):
        return self.hi - self.lo

    def mid(self):
        return (self.lo + self.hi) / 2

    def __repr__(self):
        return f"[{float(self.lo):.12g}, {float(self.hi):.12g}]"


def sqrt_bounds(q, bits=200):
    """Rational lo <= sqrt(q) <= hi for rational q >= 0, width about 2^-bits."""
    q = F(q)
    if q < 0:
        raise ValueError('negative')
    scale = 1 << (2 * bits)
    num = q.numerator * scale
    den = q.denominator
    s = isqrt(num // den)
    lo = F(s, 1 << bits)
    hi = F(s + 1, 1 << bits)
    while lo * lo > q:
        lo -= F(1, 1 << bits)
    while hi * hi < q:
        hi += F(1, 1 << bits)
    return lo, hi


def iv_sqrt(x, bits=200):
    x = Iv.of(x)
    lo, _ = sqrt_bounds(max(x.lo, F(0)), bits)
    _, hi = sqrt_bounds(x.hi, bits)
    return Iv(lo, hi)


def r_of_spread(d, ell=F(1), bits=200):
    """Rational bracket for frak r(d) = ell + d + sqrt(d^2 + 2 ell d), the root of Delta_T(r) = d above ell."""
    s = iv_sqrt(Iv(d * d + 2 * ell * d), bits)
    return Iv(ell + d) + s


def r_ceiling(P, mu, bits=200):
    """Rational bracket for r_C(mu), the larger root of B_r(mu) = c_H (point masses)."""
    h, ell, p, cH = P['h'], P['ell'], P['p'], P['cH']
    mu = Iv.of(mu)
    A = mu * h - cH
    disc = A * A + mu * ((1 - mu) * ell * ell - p * p)
    return (A + iv_sqrt(disc, bits)) / mu
