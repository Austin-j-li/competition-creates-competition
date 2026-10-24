"""Exact primitives and an exhaustive equilibrium enumerator for workstream T6.

Model: Reading N with point masses (h, ell), prior pi; one order slot; with probability lam the
informed investor fills it (class H may buy, class L may sell; each may mix); otherwise a liquidity
trader fills it and sells, abstains, buys with probabilities (beta, 1 - 2 beta, beta); separate noise
Z in {-1, 0, 1} with weights (theta, 1 - 2 theta, theta); flow X = Q + Z; competitive price
P = E[V_T | X]; the challenger sees the price and its cost; c_L = 0; the paper's second-price
auction with reserve p.

Strategy notation after the dominance reduction (wrong-way orders lose strictly because every
posterior is interior):
  A = lam * Pr(H buys | informed),  S = lam * Pr(L sells | informed),  (A, S) in [0, lam]^2,
  c = (1 - lam) * beta  (the liquidity trader's rate on each side).

Every function uses fractions.Fraction or rational intervals. Nothing here prints or asserts.
The univariate tools (Sturm isolation) and the interval class are copied from workstream T1.
"""
from fractions import Fraction as F
from math import isqrt
import itertools

FLOWS = (-2, -1, 0, 1, 2)
BUY_FLOWS = (0, 1, 2)      # flows reached by a purchase (z = -1, 0, 1)
SELL_FLOWS = (-2, -1, 0)   # flows reached by a sale (z = -1, 0, 1)


def bench(**over):
    """Benchmark parameter record (paper, Appendix A.8, with c_L = 0)."""
    P = dict(h=F(10), ell=F(1), p=F(1, 2), rho=F(1, 4), cH=F(6), k=F(1, 50),
             pi=F(1, 2), r=F(3), lam=F(1, 2), beta=F(1, 4), theta=F(1, 3))
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
    t0 = (r - p) * p / r
    tH = (p * p + (r * r - p * p) / 2) / r
    gH = h - tH
    tL = (p * p + (ell * ell - p * p) / 2 + (r - ell) * ell) / r
    gL = ((ell - p) * p + (ell - p) ** 2 / 2) / r
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL)


# ---------------------------------------------------------------------------
# Exact interval arithmetic with rational endpoints (copied from T1).
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


def is_iv(x):
    return isinstance(x, Iv)


def sign_of(v):
    """+1, -1, 0 for exact values; +1, -1 or None for intervals."""
    if is_iv(v):
        return 1 if v.lo > 0 else (-1 if v.hi < 0 else None)
    return (v > 0) - (v < 0)


def sqrt_bounds(q, bits=200):
    q = F(q)
    scale = 1 << (2 * bits)
    s = isqrt(q.numerator * scale // q.denominator)
    lo, hi = F(s, 1 << bits), F(s + 1, 1 << bits)
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
    """Rational bracket for the root of Delta_T(r) = d above ell."""
    return Iv(ell + d) + iv_sqrt(Iv(d * d + 2 * ell * d), bits)


def r_ceiling(P, mu, bits=200):
    """Rational bracket for r_C(mu), the larger root of B_r(mu) = c_H (point masses)."""
    h, ell, p, cH = P['h'], P['ell'], P['p'], P['cH']
    mu = Iv.of(mu)
    A = mu * h - cH
    disc = A * A + mu * ((1 - mu) * ell * ell - p * p)
    return (A + iv_sqrt(disc, bits)) / mu


# ---------------------------------------------------------------------------
# Univariate polynomials (lists, low to high) and Sturm isolation (copied from T1).
# ---------------------------------------------------------------------------
def utrim(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def uadd(p, q):
    n = max(len(p), len(q))
    return utrim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def uneg(p):
    return [-c for c in p]


def uscale(p, s):
    return utrim([c * s for c in p])


def umul(p, q):
    if not p or not q:
        return []
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, c1 in enumerate(p):
        for j, c2 in enumerate(q):
            out[i + j] += c1 * c2
    return utrim(out)


def ueval(p, x):
    tot = F(0) if not is_iv(x) else Iv(0)
    for c in reversed(p):
        tot = tot * x + c
    return tot


def uderiv(p):
    return utrim([i * p[i] for i in range(1, len(p))])


def udivmod(p, q):
    p, q = utrim(p), utrim(q)
    out = [F(0)] * max(len(p) - len(q) + 1, 1)
    r = list(p)
    while len(utrim(r)) >= len(q) and utrim(r):
        r = utrim(r)
        s = len(r) - len(q)
        c = r[-1] / q[-1]
        out[s] = c
        for i, qc in enumerate(q):
            r[s + i] -= c * qc
        r = utrim(r)
    return utrim(out), utrim(r)


def uprimitive(p):
    """Scale a rational polynomial to coprime integer coefficients (same roots)."""
    p = utrim(p)
    if not p:
        return p
    from math import gcd
    den = 1
    for c in p:
        den = den * c.denominator // gcd(den, c.denominator)
    ints = [int(c * den) for c in p]
    g = 0
    for v in ints:
        g = gcd(g, abs(v))
    return [F(v // g) for v in ints]


def sturm(p):
    seq = [uprimitive(p), uprimitive(uderiv(p))]
    while seq[-1] and len(seq[-1]) > 1:
        _, r = udivmod(seq[-2], seq[-1])
        if not r:
            break
        seq.append(uprimitive(uneg(r)) if any(r) else r)
    return [s for s in seq if s]


def sign_changes(seq, x):
    signs = []
    for s in seq:
        v = ueval(s, x)
        if v != 0:
            signs.append(v > 0)
    return sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])


def ugcd(p, q):
    p, q = utrim(p), utrim(q)
    while q:
        _, r = udivmod(p, q)
        p, q = q, r
    return uprimitive(p)


def squarefree(p):
    p = utrim(p)
    if len(p) <= 2:
        return p
    g = ugcd(p, uderiv(p))
    if len(g) <= 1:
        return p
    q, _ = udivmod(p, g)
    return uprimitive(q)


def deflate(p, x0):
    p = utrim(p)
    while p and ueval(p, x0) == 0:
        p, _ = udivmod(p, [-x0, F(1)])
    return p


def isolate(p, lo, hi, width=F(1, 2 ** 90)):
    """Brackets (l, u), lo < l < u < hi, each with exactly one distinct root of p and no root at
    l or u. A rational root met during bisection is returned as (x, x). Roots at lo or hi are dropped."""
    p = utrim(p)
    if len(p) <= 1:
        return []
    p = deflate(deflate(p, lo), hi)
    if len(p) <= 1:
        return []
    p = squarefree(p)
    if len(p) <= 1:
        return []
    seq = sturm(p)
    out = []
    stack = [(lo, hi)]
    while stack:
        l, u = stack.pop()
        n = sign_changes(seq, l) - sign_changes(seq, u)
        if n == 0:
            continue
        if n == 1 and u - l <= width:
            out.append((l, u))
            continue
        m = (l + u) / 2
        if ueval(p, m) == 0:
            out.append((m, m))
            q = deflate(p, m)
            if len(q) > 1:
                out.extend(s for s in isolate(q, l, u, width) if s != (m, m))
            continue
        stack.append((l, m))
        stack.append((m, u))
    return sorted(set(out))


# ---------------------------------------------------------------------------
# Bivariate polynomials in (A, S): dict {(i, j): coeff}, i = degree in A, j = degree in S.
# ---------------------------------------------------------------------------
def P_(c0=0, ca=0, cs=0):
    p = {}
    for key, c in (((0, 0), c0), ((1, 0), ca), ((0, 1), cs)):
        c = F(c)
        if c != 0:
            p[key] = c
    return p


def padd(*ps):
    out = {}
    for p in ps:
        for key, c in p.items():
            out[key] = out.get(key, F(0)) + c
    return {k_: c for k_, c in out.items() if c != 0}


def pscale(p, s):
    s = F(s)
    return {k_: c * s for k_, c in p.items() if c * s != 0}


def pmul(p, q):
    out = {}
    for (i1, j1), c1 in p.items():
        for (i2, j2), c2 in q.items():
            key = (i1 + i2, j1 + j2)
            out[key] = out.get(key, F(0)) + c1 * c2
    return {k_: c for k_, c in out.items() if c != 0}


def peval(p, a, s):
    if is_iv(a) or is_iv(s):
        a, s = Iv.of(a), Iv.of(s)
        tot = Iv(0)
        for (i, j), c in p.items():
            tot = tot + (a ** i) * (s ** j) * c
        return tot
    tot = F(0)
    for (i, j), c in p.items():
        tot += c * (a ** i) * (s ** j)
    return tot


def as_poly_in(p, var):
    """Coefficient list (low to high) in var ('A' or 'S'); each coefficient a univariate list in the other."""
    idx = 0 if var == 'A' else 1
    deg = max((key[idx] for key in p), default=0)
    out = []
    for d in range(deg + 1):
        other = {}
        for key, c in p.items():
            if key[idx] == d:
                other[key[1 - idx]] = other.get(key[1 - idx], F(0)) + c
        od = max(other, default=-1)
        out.append(utrim([other.get(t, F(0)) for t in range(od + 1)]))
    while out and not out[-1]:
        out.pop()
    return out


def restrict(p, var, val):
    """Univariate polynomial in the other variable after setting var = val (rational)."""
    idx = 0 if var == 'A' else 1
    out = {}
    for key, c in p.items():
        out[key[1 - idx]] = out.get(key[1 - idx], F(0)) + c * val ** key[idx]
    if not out:
        return []
    return utrim([out.get(t, F(0)) for t in range(max(out) + 1)])


def along_line(p, alpha, slope, param):
    """Substitute a line into p. param 'S': A = alpha + slope * t, S = t.
    param 'A': S = alpha + slope * t, A = t. Returns univariate in t."""
    lin = [alpha, slope]
    out = []
    for (i, j), c in p.items():
        if param == 'S':
            term = [c]
            for _ in range(i):
                term = umul(term, lin)
            term = umul(term, [F(0)] * j + [F(1)])
        else:
            term = [c]
            for _ in range(j):
                term = umul(term, lin)
            term = umul(term, [F(0)] * i + [F(1)])
        out = uadd(out, term)
    return utrim(out)


# polynomials whose coefficients are univariate lists (for elimination)
def cpoly_deg(f):
    return len(f) - 1


def cpoly_prem(f, g):
    """Pseudo-remainder of f by g in the main variable; coefficients are univariate lists."""
    r = [list(c) for c in f]
    dg = cpoly_deg(g)
    lg = g[-1]
    while r and cpoly_deg(r) >= dg:
        lr = r[-1]
        s = cpoly_deg(r) - dg
        new = [umul(c, lg) for c in r]
        for i, gc in enumerate(g):
            new[s + i] = uadd(new[s + i], uneg(umul(lr, gc)))
        while new and not new[-1]:
            new.pop()
        r = new
    return r


def eliminate(pA, pB, var):
    """Eliminate var from pA = pB = 0. Returns (R, u, v, lcs) with R univariate in the other
    variable, var = -v/u at a common root, and lcs the leading coefficients that must not vanish.
    Returns None when the remainder sequence does not end with a degree-one element."""
    f, g = as_poly_in(pA, var), as_poly_in(pB, var)
    if cpoly_deg(f) < cpoly_deg(g):
        f, g = g, f
    lcs = []
    seq = [f, g]
    while True:
        a, b = seq[-2], seq[-1]
        if cpoly_deg(b) <= 0:
            break
        lcs.append(b[-1])
        r = cpoly_prem(a, b)
        seq.append(r)
        if not r:
            return None
    # seq[-1] has degree <= 0 in var, seq[-2] should be degree 1
    last, lin = seq[-1], seq[-2]
    if cpoly_deg(lin) != 1:
        return None
    R = last[0] if last else []
    v, u = lin[0], lin[1]
    return utrim(R), u, v, lcs[:-1]


def exclude_strip(NH, NL, tI, var_t, lo, hi, depth=60):
    """Show that NH = NL = 0 has no solution with the variable var_t in the tiny bracket tI and the
    other variable in [lo, hi], by bisection with rational interval arithmetic.
    Returns True (no solution), or False (a sub-box could not be excluded)."""
    other = 'A' if var_t == 'S' else 'S'
    cH = [ueval(c, tI) if c else Iv(0) for c in as_poly_in(NH, other)]
    cL = [ueval(c, tI) if c else Iv(0) for c in as_poly_in(NL, other)]

    def horner(cs, x):
        tot = Iv(0)
        for c in reversed(cs):
            tot = tot * x + c
        return tot
    stack = [(F(lo), F(hi), 0)]
    while stack:
        l, u, d = stack.pop()
        box = Iv(l, u)
        if sign_of(horner(cH, box)) in (1, -1) or sign_of(horner(cL, box)) in (1, -1):
            continue
        if d >= depth:
            return False
        m = (l + u) / 2
        stack.append((l, m, d + 1))
        stack.append((m, u, d + 1))
    return True


# ---------------------------------------------------------------------------
# The model.
# ---------------------------------------------------------------------------
class Model:
    def __init__(self, P, hidden=False):
        self.P = P
        self.hidden = hidden
        self.A = auction(P)
        th = P['theta']
        self.th, self.ph = th, 1 - 2 * th
        self.n = {-1: th, 0: 1 - 2 * th, 1: th}
        self.lam, self.beta = P['lam'], P['beta']
        self.c = (1 - self.lam) * self.beta
        self.pi, self.rho = P['pi'], P['rho']
        self.kD = P['k'] / self.A['D']
        self.tau = self.A['tau']
        n, c, pi = self.n, self.c, self.pi
        # slot laws: (constant, coefficient on own rate)
        PH = {1: (c, F(1)), 0: (1 - 2 * c, F(-1)), -1: (c, F(0))}
        PL = {1: (c, F(0)), 0: (1 - 2 * c, F(-1)), -1: (c, F(1))}
        self.fH, self.fL, self.Dn, self.L = {}, {}, {}, {}
        for x in FLOWS:
            h0 = sum(PH[q][0] * n.get(x - q, 0) for q in PH)
            h1 = sum(PH[q][1] * n.get(x - q, 0) for q in PH)
            l0 = sum(PL[q][0] * n.get(x - q, 0) for q in PL)
            l1 = sum(PL[q][1] * n.get(x - q, 0) for q in PL)
            self.fH[x] = P_(h0, h1, 0)
            self.fL[x] = P_(l0, 0, l1)
            self.Dn[x] = padd(pscale(self.fH[x], pi), pscale(self.fL[x], 1 - pi))
            self.L[x] = padd(pscale(self.fH[x], pi * (1 - self.tau)), pscale(self.fL[x], -(1 - pi) * self.tau))
        if hidden:
            val = self.Bmu(pi) - P['cH']
            self.e_hidden = F(1) if val > 0 else (self.rho if val < 0 else None)

    def Bmu(self, mu):
        return self.A['gL'] + mu * (self.A['gH'] - self.A['gL'])

    def entry_at(self, mu, rule='E'):
        val = self.Bmu(mu) - self.P['cH']
        if val > 0:
            return F(1)
        if val < 0:
            return self.rho
        return F(1) if rule == 'E' else None

    # ---- weights: G_H / Delta = sum_x wH_x e_x ; G_L / Delta = sum_x wL_x e_x ----
    def weights(self, a, s):
        pi = self.pi
        wH, wL = {}, {}
        for x in BUY_FLOWS:
            wH[x] = self.n[x - 1] * (1 - pi) * peval(self.fL[x], a, s) / peval(self.Dn[x], a, s)
        for x in SELL_FLOWS:
            wL[x] = self.n[x + 1] * pi * peval(self.fH[x], a, s) / peval(self.Dn[x], a, s)
        return wH, wL

    def gains(self, a, s, e):
        wH, wL = self.weights(a, s)
        gH = sum((wH[x] * e[x] for x in BUY_FLOWS), F(0) if not (is_iv(a) or is_iv(s)) else Iv(0))
        gL = sum((wL[x] * e[x] for x in SELL_FLOWS), F(0) if not (is_iv(a) or is_iv(s)) else Iv(0))
        return gH, gL

    def wrong_way(self, a, s, e):
        """Gross gains per unit Delta of H selling and L buying (both negative)."""
        pi = self.pi
        hs = F(0)
        lb = F(0)
        for z, pz in self.n.items():
            x = -1 + z
            mu = pi * peval(self.fH[x], a, s) / peval(self.Dn[x], a, s)
            hs = hs - pz * e[x] * (1 - mu)
            x = 1 + z
            mu = pi * peval(self.fH[x], a, s) / peval(self.Dn[x], a, s)
            lb = lb - pz * e[x] * mu
        return hs, lb

    def posteriors(self, a, s):
        return {x: self.pi * peval(self.fH[x], a, s) / peval(self.Dn[x], a, s) for x in FLOWS}

    def NH(self, e):
        """Numerator of (G_H - k)/Delta times prod_{x in BUY} D_x."""
        pi = self.pi
        terms = []
        for x in BUY_FLOWS:
            t = pscale(self.fL[x], self.n[x - 1] * (1 - pi) * e[x])
            for y in BUY_FLOWS:
                if y != x:
                    t = pmul(t, self.Dn[y])
            terms.append(t)
        prod = {(0, 0): F(1)}
        for y in BUY_FLOWS:
            prod = pmul(prod, self.Dn[y])
        terms.append(pscale(prod, -self.kD))
        return padd(*terms)

    def NL(self, e):
        pi = self.pi
        terms = []
        for x in SELL_FLOWS:
            t = pscale(self.fH[x], self.n[x + 1] * pi * e[x])
            for y in SELL_FLOWS:
                if y != x:
                    t = pmul(t, self.Dn[y])
            terms.append(t)
        prod = {(0, 0): F(1)}
        for y in SELL_FLOWS:
            prod = pmul(prod, self.Dn[y])
        terms.append(pscale(prod, -self.kD))
        return padd(*terms)

    def sign_line(self, x, a, s):
        if self.hidden:
            return 1 if self.e_hidden == 1 else -1
        return sign_of(peval(self.L[x], a, s))

    def outcomes(self, a, s, e):
        pi, rho, A = self.pi, self.rho, self.A
        E = F(0) if not (is_iv(a) or is_iv(s) or any(is_iv(v) for v in e.values())) else Iv(0)
        OH = E
        for x in FLOWS:
            fh, fl = peval(self.fH[x], a, s), peval(self.fL[x], a, s)
            E = E + (fh * pi + fl * (1 - pi)) * e[x]
            OH = OH + fh * pi * e[x]
        RT = A['t0'] + OH * A['wH'] + (E - OH) * A['wL']
        W = A['base'] + OH * (A['gH'] + A['pF']) + (E - OH) * (A['gL'] + A['pF']) - self.P['cH'] * (E - rho)
        cost = self.P['k'] * (pi * a + (1 - pi) * s)
        return dict(E=E, OH=OH, RT=RT, W=W, cost=cost)

    def flow_probs(self, a, s):
        return {x: self.pi * peval(self.fH[x], a, s) + (1 - self.pi) * peval(self.fL[x], a, s) for x in FLOWS}


# ---------------------------------------------------------------------------
# Enumeration helpers.
# ---------------------------------------------------------------------------
def kind_of(rate, lam):
    if rate == 0:
        return 'zero'
    if rate == lam:
        return 'full'
    return 'mix'


def cond_ok(val, kind, strict_full=False):
    """val = G/Delta - k/Delta. Returns True, False or None (undecided)."""
    sg = sign_of(val)
    if kind == 'zero':
        if sg is None:
            return None
        return sg <= 0
    if kind == 'full':
        if sg is None:
            return None
        return sg > 0 if strict_full else sg >= 0
    if is_iv(val):
        return None
    return val == 0


def point_feasible(M, a, s, kH, kL, rule='X', strict_full=False):
    """Exact rational point (a, s). Tied flows (posterior = tau) carry free entry in [rho, 1]
    (rule X) or entry 1 (rule E). Returns (representative entry dict or None, tied flows).

    G_H/Delta and G_L/Delta are affine and increasing in each entry rate. The two classes share only
    e_0. For fixed e_0 the other free rates move each payoff over an interval, so feasibility reduces
    to a one-dimensional search over e_0 at its candidate breakpoints and the midpoints between them."""
    rho, kD = M.rho, M.kD
    e, free = {}, []
    for x in FLOWS:
        sg = M.sign_line(x, a, s)
        if sg > 0:
            e[x] = F(1)
        elif sg < 0:
            e[x] = rho
        elif rule == 'E':
            e[x] = F(1)
        else:
            free.append(x)
    wH, wL = M.weights(a, s)

    def rng(w, flows, e0):
        lo = sum(w[x] * (e0 if x == 0 else (rho if x in free else e[x])) for x in flows)
        hi = sum(w[x] * (e0 if x == 0 else (F(1) if x in free else e[x])) for x in flows)
        return lo, hi

    def ok(kind, lo, hi):
        if kind == 'zero':
            return lo <= kD
        if kind == 'full':
            return hi > kD if strict_full else hi >= kD
        return lo <= kD <= hi

    if 0 in free:
        cands = {rho, F(1)}
        for w, flows in ((wH, BUY_FLOWS), (wL, SELL_FLOWS)):
            for which in (0, 1):
                v0 = rng(w, flows, F(0))[which]
                v1 = rng(w, flows, F(1))[which]
                if v1 != v0:
                    t0 = (kD - v0) / (v1 - v0)
                    if rho < t0 < 1:
                        cands.add(t0)
        cands = sorted(cands)
        cands = cands + [(x1 + x2) / 2 for x1, x2 in zip(cands[:-1], cands[1:])]
    else:
        cands = [e[0]]
    for e0 in cands:
        loH, hiH = rng(wH, BUY_FLOWS, e0)
        loL, hiL = rng(wL, SELL_FLOWS, e0)
        if ok(kH, loH, hiH) and ok(kL, loL, hiL):
            rep = dict(e)
            rep[0] = e0
            for flows, w, kind, lo in ((BUY_FLOWS, wH, kH, loH), (SELL_FLOWS, wL, kL, loL)):
                fr = [x for x in flows if x in free and x != 0]
                if not fr:
                    continue
                if kind == 'zero':
                    for x in fr:
                        rep[x] = rho
                elif kind == 'full':
                    for x in fr:
                        rep[x] = F(1)
                else:
                    need = kD - lo
                    for x in fr:
                        add = min(need, w[x] * (1 - rho))
                        rep[x] = rho + (add / w[x] if w[x] != 0 else 0)
                        need -= add
            return rep, free
    return None, free


def polygon_clip(poly, a, s, c, strict_sign):
    """Clip a convex polygon (list of (A, S)) by the half-plane sign(a A + s S + c) = strict_sign."""
    out = []
    n = len(poly)
    for i in range(n):
        P1, P2 = poly[i], poly[(i + 1) % n]
        v1 = (a * P1[0] + s * P1[1] + c) * strict_sign
        v2 = (a * P2[0] + s * P2[1] + c) * strict_sign
        if v1 >= 0:
            out.append(P1)
        if (v1 > 0 > v2) or (v1 < 0 < v2):
            t = v1 / (v1 - v2)
            out.append((P1[0] + t * (P2[0] - P1[0]), P1[1] + t * (P2[1] - P1[1])))
    return out


def polygon_area2(poly):
    if len(poly) < 3:
        return F(0)
    s = F(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s)


def line_coeffs(Lx):
    return Lx.get((1, 0), F(0)), Lx.get((0, 1), F(0)), Lx.get((0, 0), F(0))


def label(a, s, lam):
    names = {('zero', 'zero'): 'NT', ('full', 'full'): 'T', ('full', 'zero'): 'BNS', ('zero', 'full'): 'SNB'}
    ka = 'mix' if is_iv(a) else kind_of(a, lam)
    ks = 'mix' if is_iv(s) else kind_of(s, lam)
    if (ka, ks) in names:
        return names[(ka, ks)]
    return {'zero': 'no buy', 'full': 'full buy', 'mix': 'partial buy'}[ka] + ', ' + \
        {'zero': 'no sell', 'full': 'full sell', 'mix': 'partial sell'}[ks]


def record(M, a, s, e, where, cert, note=''):
    out = M.outcomes(a, s, e)
    cm = []
    for x in FLOWS:
        v = e[x]
        if is_iv(v):
            if not (v.lo == v.hi and v.lo in (M.rho, F(1))):
                cm.append(x)
        elif M.rho < v < 1:
            cm.append(x)
    rec = dict(a=a, s=s, e=e, label=label(a, s, M.lam), where=where, cert=cert, chall_mix=cm,
               out=out, note=note)
    rec['recruit'] = tuple(x for x in FLOWS if (not is_iv(e[x]) and e[x] == 1))
    return rec


def enumerate_equilibria(P, investor='M', challenger='X', hidden=False):
    """All equilibria at P. investor in {'M', 'Z'}; challenger in {'X', 'E'}.
    hidden=True: the challenger cannot see the price (entry fixed at the prior's level).
    Returns (records, undecided notes, model)."""
    M = Model(P, hidden)
    lam, rho = M.lam, M.rho
    strict_full = investor == 'Z'
    eqs, undecided = [], []
    if hidden and M.e_hidden is None:
        undecided.append('hidden prices: prior belief is a tie')
        return eqs, undecided, M
    lines = {} if hidden else {x: line_coeffs(M.L[x]) for x in FLOWS}

    def pattern_ok(a, s, e, skip=()):
        """True / False / None: strict line signs at (a, s) agree with the fixed entry e."""
        res = True
        for x in FLOWS:
            if x in skip:
                continue
            sg = M.sign_line(x, a, s)
            want = 1 if e[x] == 1 else -1
            if sg is None:
                res = None
            elif sg != want:
                return False
        return res

    def fixed_e(sig):
        return {x: (F(1) if sg else rho) for x, sg in zip(FLOWS, sig)}

    # ---------------- corners ----------------
    for a in (F(0), lam):
        for s in (F(0), lam):
            rep, free = point_feasible(M, a, s, kind_of(a, lam), kind_of(s, lam),
                                       rule=('E' if (challenger == 'E' or hidden) else 'X'),
                                       strict_full=strict_full)
            if rep is not None:
                eqs.append(record(M, a, s, rep, 'corner', 'exact', f'ties at {free}' if free else ''))
    if investor == 'Z':
        return eqs, undecided, M

    # ---------------- edges ----------------
    for fixed, val in (('S', F(0)), ('S', lam), ('A', F(0)), ('A', lam)):
        mover = 'H' if fixed == 'S' else 'L'

        def ab(t, fixed=fixed, val=val):
            return (t, val) if fixed == 'S' else (val, t)
        bps = []
        for x, (ca, cs, c0) in lines.items():
            c1 = ca if fixed == 'S' else cs
            cc = c0 + (cs if fixed == 'S' else ca) * val
            if c1 != 0:
                t0 = -cc / c1
                if 0 < t0 < lam:
                    bps.append(t0)
        bps = sorted(set(bps))
        pts = [F(0)] + bps + [lam]
        for lo, hi in zip(pts[:-1], pts[1:]):
            mid = (lo + hi) / 2
            am, sm = ab(mid)
            if hidden:
                e = {x: M.e_hidden for x in FLOWS}
            else:
                e = {x: (F(1) if M.sign_line(x, am, sm) > 0 else rho) for x in FLOWS}
            N = M.NH(e) if mover == 'H' else M.NL(e)
            uni = restrict(N, fixed, val)
            if not uni:
                undecided.append(f'edge {fixed}={val}: indifference on all of ({float(lo)},{float(hi)})')
                continue
            for (l, u) in isolate(uni, lo, hi):
                tI = Iv(l, u) if l != u else l
                a_, s_ = ab(tI)
                ok_pat = True if hidden else pattern_ok(a_, s_, e)
                if ok_pat is False:
                    continue
                gH, gL = M.gains(a_, s_, e)
                other = (gL - M.kD) if mover == 'H' else (gH - M.kD)
                ok = cond_ok(other, kind_of(val, lam))
                if ok is False:
                    continue
                if ok is None or ok_pat is None:
                    undecided.append(f'edge {fixed}={val}, root near {float(l):.10g}: undecided sign')
                    continue
                eqs.append(record(M, a_, s_, e, 'edge', 'exact' if l == u else 'enclosure'))
        if hidden or challenger == 'E':
            # rule E: points on a line with entry 1 at the tied flow
            for t0 in bps:
                a_, s_ = ab(t0)
                rep, free = point_feasible(M, a_, s_, 'mix' if mover == 'H' else kind_of(a_, lam),
                                           'mix' if mover == 'L' else kind_of(s_, lam), rule='E')
                if rep is not None and not hidden:
                    eqs.append(record(M, a_, s_, rep, 'edge-line', 'exact', f'ties at {free}'))
            continue
        for t0 in bps:
            a_, s_ = ab(t0)
            rep, free = point_feasible(M, a_, s_, 'mix' if mover == 'H' else kind_of(a_, lam),
                                       'mix' if mover == 'L' else kind_of(s_, lam), rule='X')
            if rep is not None:
                eqs.append(record(M, a_, s_, rep, 'edge-line', 'exact', f'ties at {free}'))

    # ---------------- open cells ----------------
    square = [(F(0), F(0)), (lam, F(0)), (lam, lam), (F(0), lam)]
    sigs = [tuple(1 if M.e_hidden == 1 else 0 for _ in FLOWS)] if hidden else \
        list(itertools.product((0, 1), repeat=5))
    for sig in sigs:
        if not hidden:
            poly = square
            for x, sg in zip(FLOWS, sig):
                ca, cs, c0 = lines[x]
                poly = polygon_clip(poly, ca, cs, c0, 1 if sg else -1)
                if len(poly) < 3:
                    break
            if polygon_area2(poly) == 0:
                continue
        e = fixed_e(sig) if not hidden else {x: M.e_hidden for x in FLOWS}
        NH, NL = M.NH(e), M.NL(e)
        el = eliminate(NH, NL, 'A')
        var_out = 'S'
        if el is None:
            el = eliminate(NH, NL, 'S')
            var_out = 'A'
        if el is None:
            undecided.append(f'cell {sig}: elimination failed')
            continue
        R, u, v, lcs = el
        if not R:
            undecided.append(f'cell {sig}: resultant vanishes identically')
            continue
        for (l, uu) in isolate(R, F(0), lam):
            tI = Iv(l, uu) if l != uu else l
            uval = ueval(u, tI)
            if sign_of(uval) in (None, 0) or any(sign_of(ueval(c, tI)) in (None, 0) for c in lcs):
                # a leading coefficient may vanish here (a spurious root of the eliminant);
                # exclude the strip by interval bisection in the other variable
                if exclude_strip(NH, NL, Iv.of(tI), var_out, F(0), lam):
                    continue
                undecided.append(f'cell {sig}: degenerate elimination near {float(l):.8g}')
                continue
            other = -ueval(v, tI) / uval
            if var_out == 'S':
                a_, s_ = other, tI
            else:
                a_, s_ = tI, other
            inside = True
            for val_ in (a_, s_):
                if is_iv(val_):
                    if val_.hi <= 0 or val_.lo >= lam:
                        inside = False
                        break
                    if val_.lo <= 0 or val_.hi >= lam:
                        inside = None
                elif not (0 < val_ < lam):
                    inside = False
                    break
            if inside is False:
                continue
            if inside is None:
                undecided.append(f'cell {sig}: root at the boundary near ({float(Iv.of(a_).mid()):.6g},{float(Iv.of(s_).mid()):.6g})')
                continue
            ok_pat = True if hidden else pattern_ok(a_, s_, e)
            if ok_pat is False:
                continue
            if ok_pat is None:
                undecided.append(f'cell {sig}: root on a line near ({float(Iv.of(a_).mid()):.6g},{float(Iv.of(s_).mid()):.6g})')
                continue
            eqs.append(record(M, a_, s_, e, 'cell', 'enclosure' if (is_iv(a_) or is_iv(s_)) else 'exact'))

    if challenger == 'E' or hidden:
        return eqs, undecided, M

    # ---------------- lines: challenger mixing at one flow, both investors mixing ----------------
    for x in FLOWS:
        ca, cs, c0 = lines[x]
        if ca == 0 and cs == 0:
            continue
        if ca != 0:
            alpha, slope, param = -c0 / ca, -cs / ca, 'S'     # A = alpha + slope * S
        else:
            alpha, slope, param = -c0 / cs, F(0), 'A'         # S = alpha, t = A
        # t-range inside the open square
        if param == 'S':
            lo, hi = F(0), lam
            if slope == 0:
                if not (0 < alpha < lam):
                    continue
            else:
                t1, t2 = -alpha / slope, (lam - alpha) / slope
                lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
        else:
            if not (0 < alpha < lam):
                continue
            lo, hi = F(0), lam
        if lo >= hi:
            continue

        def pt(t, alpha=alpha, slope=slope, param=param):
            return (alpha + slope * t, t) if param == 'S' else (t, alpha)
        others = [y for y in FLOWS if y != x]
        for so in itertools.product((0, 1), repeat=4):
            base = {y: (F(1) if sg else rho) for y, sg in zip(others, so)}
            e_lo, e_hi = dict(base), dict(base)
            e_lo[x], e_hi[x] = rho, F(1)
            NH_lo, NH_hi = M.NH(e_lo), M.NH(e_hi)
            NL_lo, NL_hi = M.NL(e_lo), M.NL(e_hi)
            if x in (1, 2):
                eqp = along_line(NL_lo, alpha, slope, param)
            elif x in (-1, -2):
                eqp = along_line(NH_lo, alpha, slope, param)
            else:
                PH = along_line(NH_lo, alpha, slope, param)
                QH = uadd(along_line(NH_hi, alpha, slope, param), uneg(PH))
                PL = along_line(NL_lo, alpha, slope, param)
                QL = uadd(along_line(NL_hi, alpha, slope, param), uneg(PL))
                eqp = uadd(umul(PH, QL), uneg(umul(PL, QH)))
            eqp = utrim(eqp)
            if not eqp:
                undecided.append(f'line {x}, others {so}: identity (continuum)')
                continue
            for (l, u) in isolate(eqp, lo, hi):
                tI = Iv(l, u) if l != u else l
                a_, s_ = pt(tI)
                eb = dict(base)
                eb[x] = rho
                ok_pat = pattern_ok(a_, s_, eb, skip=(x,))
                if ok_pat is False:
                    continue
                if ok_pat is None:
                    undecided.append(f'line {x}: crossing near t={float(Iv.of(tI).mid()):.8g}')
                    continue
                gH_lo, gL_lo = M.gains(a_, s_, e_lo)
                gH_hi, gL_hi = M.gains(a_, s_, e_hi)
                if x in (1, 2, 0):
                    v0, v1 = gH_lo - M.kD, gH_hi - M.kD
                else:
                    v0, v1 = gL_lo - M.kD, gL_hi - M.kD
                dv = v1 - v0
                if sign_of(dv) in (None, 0):
                    undecided.append(f'line {x}: flat response near t={float(Iv.of(tI).mid()):.8g}')
                    continue
                frac = -v0 / dv
                fs_lo, fs_hi = sign_of(frac), sign_of(frac - 1)
                if fs_lo == -1 or fs_hi == 1:
                    continue
                if fs_lo is None or fs_hi is None:
                    undecided.append(f'line {x}: mixing probability near 0 or 1')
                    continue
                e = dict(base)
                e[x] = rho + frac * (1 - rho)
                eqs.append(record(M, a_, s_, e, 'line', 'enclosure' if is_iv(tI) else 'exact'))
    # ---------------- crossings of two lines inside the open square ----------------
    for x, y in itertools.combinations(FLOWS, 2):
        a1, s1, c1 = lines[x]
        a2, s2, c2 = lines[y]
        det = a1 * s2 - a2 * s1
        if det == 0:
            continue
        a_ = (-c1 * s2 + c2 * s1) / det
        s_ = (-a1 * c2 + a2 * c1) / det
        if 0 < a_ < lam and 0 < s_ < lam:
            rep, free = point_feasible(M, a_, s_, 'mix', 'mix', rule='X')
            if rep is not None:
                eqs.append(record(M, a_, s_, rep, 'crossing', 'exact', f'ties at {free}'))
    return eqs, undecided, M


def fmt(q, digits=6):
    if is_iv(q):
        return f"[{float(q.lo):.{digits + 3}f}, {float(q.hi):.{digits + 3}f}]"
    q = F(q)
    if q.denominator == 1:
        return f"{q.numerator}"
    if q.denominator < 10 ** 8:
        return f"{q.numerator}/{q.denominator} = {float(q):.{digits}f}"
    return f"{float(q):.{digits}f}"


def fl(q):
    return float(q.mid()) if is_iv(q) else float(q)
