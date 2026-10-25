#!/usr/bin/env python3
"""Bounds for the lemma on research at the entry floor along the example path.

The example: the incumbent's value is uniform on [0, r]; the class values are h = 10 and ell = 1; the
reserve is p = 1/2; the preparation cost is zero with probability rho = 1/4 and c_H = 6 otherwise; the
trading cost is k = 1/50; the prior is 1/2; the liquidity share is beta = 294655/10^6, and the slot has
1 + u = e. Research costs (a/2) lambda^2 with a = 1/40, up to the cap lambda_bar = u beta/(1 + u beta).
The strengths run over [r_0, r_2] = [6/5, 18/5].

Every quantity is an exact rational, or a closed interval with rational endpoints that contains the
exact value: Euler's number enters through the partial sums of its series and the bound 2/(N+1)! on
the tail, and each square root through integer square roots. Interval endpoints are rounded outward to
multiples of 10^-60. The program prints; it checks nothing by assertion.

Usage: python3 o1_bounds.py
"""

import csv
from fractions import Fraction as Fr
from math import factorial, isqrt
from pathlib import Path

# ------------------------------------------------------------------------------------------------
# Intervals with rational endpoints

GRID = 10 ** 60


def _down(x):
    x = Fr(x)
    return Fr((x.numerator * GRID) // x.denominator, GRID)


def _up(x):
    x = Fr(x)
    return Fr(-((-x.numerator * GRID) // x.denominator), GRID)


class Iv:
    """The closed interval [lo, hi]; every operation rounds the result outward."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None, round_out=True):
        lo = Fr(lo)
        hi = lo if hi is None else Fr(hi)
        if round_out:
            lo, hi = _down(lo), _up(hi)
        self.lo, self.hi = lo, hi

    @staticmethod
    def of(x):
        return x if isinstance(x, Iv) else Iv(x, x, round_out=False)

    def __add__(self, o):
        o = Iv.of(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo, round_out=False)

    def __sub__(self, o):
        return self + (-Iv.of(o))

    def __rsub__(self, o):
        return Iv.of(o) + (-self)

    def __mul__(self, o):
        o = Iv.of(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(ps), max(ps))

    __rmul__ = __mul__

    def inv(self):
        # used only for intervals that exclude zero
        return Iv(1 / self.hi, 1 / self.lo)

    def __truediv__(self, o):
        return self * Iv.of(o).inv()

    def __rtruediv__(self, o):
        return Iv.of(o) * self.inv()

    def __pow__(self, n):
        out = Iv.of(1)
        for _ in range(n):
            out = out * self
        return out


def sqrt_iv(x):
    """An interval that contains the square root of every point of x (x >= 0)."""
    x = Iv.of(x)

    def fl(y):
        return isqrt((y.numerator * GRID * GRID) // y.denominator)

    return Iv(Fr(fl(x.lo), GRID), Fr(fl(x.hi) + 1, GRID), round_out=False)


def sign(x):
    """+1 or -1 when the sign is decided, 0 for an exact zero or an interval that contains zero."""
    if isinstance(x, Iv):
        if x.lo > 0:
            return 1
        if x.hi < 0:
            return -1
        return 0
    return (x > 0) - (x < 0)


def lo_of(x):
    return x.lo if isinstance(x, Iv) else Fr(x)


def hi_of(x):
    return x.hi if isinstance(x, Iv) else Fr(x)


def iv_min(x, y):
    return Iv(min(lo_of(x), lo_of(y)), min(hi_of(x), hi_of(y)), round_out=False)


def iv_max(x, y):
    return Iv(max(lo_of(x), lo_of(y)), max(hi_of(x), hi_of(y)), round_out=False)


def rnd(x, n=6):
    """The rational x rounded half up to n decimals, as a string."""
    x = Fr(x)
    neg = x < 0
    y = abs(x) * 10 ** n
    q = (y.numerator * 2 + y.denominator) // (2 * y.denominator)
    s = str(q).rjust(n + 1, "0")
    out = s[:-n] + "." + s[-n:] if n else s
    return ("-" if neg and q else "") + out


def rnd_down(x, n=6):
    """The largest n-decimal number at or below x, as a string."""
    x = Fr(x)
    q = (x.numerator * 10 ** n) // x.denominator
    neg = q < 0
    s = str(abs(q)).rjust(n + 1, "0")
    return ("-" if neg else "") + s[:-n] + "." + s[-n:]


def show(x, n=6):
    """A value rounded to n decimals; an interval whose endpoints round differently prints both."""
    if isinstance(x, Iv):
        a, b = rnd(x.lo, n), rnd(x.hi, n)
        return a if a == b else f"[{a}, {b}]"
    return rnd(x, n)


def digits(x, n=22):
    """Both endpoints of an interval to n decimals, rounded outward."""
    if isinstance(x, Iv):
        return f"[{rnd_down(x.lo, n)}, {rnd_up(x.hi, n)}]"
    return rnd(x, n)


def rnd_up(x, n):
    x = Fr(x)
    q = -((-x.numerator * 10 ** n) // x.denominator)
    neg = q < 0
    s = str(abs(q)).rjust(n + 1, "0")
    return ("-" if neg else "") + s[:-n] + "." + s[-n:]


def width(x):
    return hi_of(x) - lo_of(x)


# ------------------------------------------------------------------------------------------------
# Primitives of the example

H, ELL, P = Fr(10), Fr(1), Fr(1, 2)
RHO, CH, K, PRIOR = Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
BETA = Fr(294655, 10 ** 6)
A = Fr(1, 40)
R0, R1, R2 = Fr(6, 5), Fr(3), Fr(18, 5)
STEP = Fr(1, 10)          # width of the pieces in the derivative bound
LB_CLAIM = Fr(1, 100)     # lower bound on the derivative that the proof states

N_E = 40
_S = sum(Fr(1, factorial(n)) for n in range(N_E + 1))
EUL = Iv(_S, _S + Fr(2, factorial(N_E + 1)), round_out=False)
U_SLOT = EUL - 1
CAP = 1 - 1 / (1 + U_SLOT * BETA)          # u beta / (1 + u beta), with u entering once
M_CAP = 1 - 1 / (1 + EUL)                 # e / (1 + e)
m_CAP = 1 / (1 + EUL)                     # 1 / (1 + e)
ETA = {-1: BETA, 0: 1 - 2 * BETA, 1: BETA}

# ------------------------------------------------------------------------------------------------
# The auction: closed forms, and the same quantities by piecewise integration over R ~ U[0, r]


def Delta(r):
    return (r - ELL) ** 2 / (2 * r)


def dDelta(r):
    return (1 - ELL ** 2 / r ** 2) / 2


def gL_closed(r):
    return (ELL ** 2 - P ** 2) / (2 * r)


def gH_closed(r):
    return H - r / 2 - P ** 2 / (2 * r)


def tau(r):
    return (CH - gL_closed(r)) / (gH_closed(r) - gL_closed(r))


def tau_display(r):
    return (12 * r - Fr(3, 4)) / (20 * r - r * r - 1)


def dtau(r):
    return 3 * (8 * r * r - r + 2) / (2 * (20 * r - r * r - 1) ** 2)


def T_bound(l, u):
    """Upper bound on tau' over [l, u]: largest numerator over smallest denominator."""
    return 3 * (8 * u * u - u + 2) / (2 * (20 * l - l * l - 1) ** 2)


def expect_uniform(f, r, cuts):
    """E f(R) for R uniform on [0, r], with f linear between consecutive cut points (midpoint rule)."""
    pts = sorted({Fr(0), Fr(r)} | {Fr(c) for c in cuts if 0 < c < r})
    total = Fr(0)
    for x0, x1 in zip(pts, pts[1:]):
        total += (x1 - x0) * f((x0 + x1) / 2)
    return total / r


def auction_by_integration(r):
    """t_0, t_H, t_L, g_H, g_L from the auction rules: second price with reserve p, truthful bids."""
    def t_no_entry(R):
        return P if R >= P else Fr(0)

    def t_with(theta):
        return lambda R: max(P, min(R, theta))

    def g_with(theta):
        return lambda R: max(Fr(0), theta - max(P, R))

    cuts = [P, ELL, H]
    return {
        "t0": expect_uniform(t_no_entry, r, cuts),
        "tH": expect_uniform(t_with(H), r, cuts),
        "tL": expect_uniform(t_with(ELL), r, cuts),
        "gH": expect_uniform(g_with(H), r, cuts),
        "gL": expect_uniform(g_with(ELL), r, cuts),
    }


# ------------------------------------------------------------------------------------------------
# Research objects


def m_of(lam):
    return BETA * (1 - lam) / (2 * BETA + (1 - 2 * BETA) * lam)


def M_of(lam):
    return 1 - m_of(lam)


def lamE(t):
    return BETA * (2 * t - 1) / (BETA + (1 - 2 * BETA) * (1 - t))


def dlamE(t):
    return BETA / (BETA + (1 - 2 * BETA) * (1 - t)) ** 2


def phi_floor(r):
    """The floor margin rho Delta (1 - tau) - k - a lambda_E, an exact rational at rational r."""
    t = tau(r)
    return RHO * Delta(r) * (1 - t) - K - A * lamE(t)


def dphi_floor(r):
    t = tau(r)
    tp = dtau(r)
    return RHO * (dDelta(r) * (1 - t) - Delta(r) * tp) - A * dlamE(t) * tp


def b_piece(l, u):
    """Lower bound on the derivative of the floor margin over [l, u]."""
    tu = tau(u)
    T = T_bound(l, u)
    return RHO * (dDelta(l) * (1 - tu) - Delta(u) * T) - A * dlamE(tu) * T


def floor_root(D):
    """The root in (0, 1) of rho D m_lambda - k - a lambda, for rho D > 2k, by the quadratic formula.

    Clearing 2 beta + (1 - 2 beta) lambda > 0 gives
    a (1 - 2 beta) lambda^2 + [rho D beta + k (1 - 2 beta) + 2 a beta] lambda + beta (2k - rho D) = 0,
    whose positive root is -2C / (B + sqrt(B^2 - 4AC)).
    """
    qa = A * (1 - 2 * BETA)
    qb = RHO * D * BETA + K * (1 - 2 * BETA) + 2 * A * BETA
    qc = BETA * (2 * K - RHO * D)
    disc = qb * qb - 4 * qa * qc
    return Iv.of(-2 * qc) / (qb + sqrt_iv(disc))


def frak_r(d):
    """The strength above ell at which Delta(r) = d: r = ell + d + sqrt(d^2 + 2 ell d)."""
    return ELL + d + sqrt_iv(d * d + 2 * ELL * d)


def bracket(f, lo, hi, steps=100):
    """Halve [lo, hi] by the decided sign of the increasing function f; returns the final bracket."""
    for _ in range(steps):
        mid = (lo + hi) / 2
        s = sign(f(mid))
        if s < 0:
            lo = mid
        elif s > 0:
            hi = mid
        else:
            return lo, hi, mid
    return lo, hi, None


def at_bracket(fun, br):
    """The values of an increasing function at both ends of a bracket, as one interval."""
    lo, hi = br[0], br[1]
    return Iv(lo_of(fun(lo)), hi_of(fun(hi)))


# ------------------------------------------------------------------------------------------------
# The rows of the numbers table that the lemma and its proof rely on

REG_PATH = Path(__file__).resolve().parents[4] / "audit" / "slot_manuscript_2026_10_23" / "registry" / "registry.csv"


def load_registry():
    rows = {}
    try:
        with open(REG_PATH, newline="") as fh:
            for row in csv.DictReader(fh):
                rows[row["key"]] = (row["value"], row["display"])
    except OSError as exc:
        print(f"numbers table not readable at {REG_PATH}: {exc}")
    return rows


REG = load_registry()


def beside(key, value, n=6, note=""):
    disp = REG.get(key, ("(absent)", "(absent)"))[1]
    mine = show(value, n) if not isinstance(value, str) else value
    agree = "same" if mine == disp else "DIFFERENT"
    print(f"  {key:<24} here {mine:<24} table display {disp:<14} {agree}  {note}")


def hdr(title):
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


# ================================================================================================
hdr("1. Primitives, Euler's number and the cap")
print(f"  beta = {BETA} ; a = {A} ; rho = {RHO} ; k = {K} ; c_H = {CH} ; h = {H} ; ell = {ELL} ; p = {P}")
print(f"  r_0 = {R0} ; r_1 = {R1} ; r_2 = {R2} ; prior = {PRIOR}")
print(f"  e in {digits(EUL, 30)}  (partial sum to n = {N_E}, tail at most 2/{N_E + 1}!)")
print(f"  width of the interval for e: {float(width(EUL)):.3e}")
print(f"  cap lambda_bar = u beta/(1 + u beta) in {digits(CAP, 24)}  -> {show(CAP)}")
print(f"  M at the cap, e/(1+e) in {digits(M_CAP, 24)}  -> {show(M_CAP)}")
print(f"  m at the cap, 1/(1+e) in {digits(m_CAP, 24)}  -> {show(m_CAP)}")
mcap_formula = m_of(CAP)
print(f"  m_lambda at lambda = cap from beta(1-lambda)/[2 beta + (1-2 beta) lambda]: {digits(mcap_formula, 24)}")
print(f"  difference from 1/(1+e): {digits(mcap_formula - m_CAP, 30)}")

# ================================================================================================
hdr("2. The auction at sample strengths: closed forms against piecewise integration")
for r in (R0, Fr(7, 4), Fr(2), R1, R2):
    a_int = auction_by_integration(r)
    cf = {
        "t0": P * (1 - P / r),
        "tH": r / 2 + P ** 2 / (2 * r),
        "tL": ELL - (ELL ** 2 - P ** 2) / (2 * r),
        "gH": gH_closed(r),
        "gL": gL_closed(r),
    }
    diffs = {key: a_int[key] - cf[key] for key in cf}
    spread = a_int["tH"] - a_int["tL"]
    tau_int = (CH - a_int["gL"]) / (a_int["gH"] - a_int["gL"])
    print(f"  r = {str(r):<5} differences (integration minus closed form): "
          + ", ".join(f"{key} {diffs[key]}" for key in diffs)
          + f" ; Delta {spread - Delta(r)} ; tau {tau_int - tau(r)} ; tau display form {tau_display(r) - tau(r)}")
print(f"  tau(r_2) = {tau(R2)}  (below 1: {tau(R2) < 1})")
print("  B_r(1/2) = 5 - r/4 + 1/(8r) falls in r; at r_0 it is "
      f"{(gL_closed(R0) + gH_closed(R0)) / 2} = {float((gL_closed(R0) + gH_closed(R0)) / 2):.6f} < c_H = 6")

# ================================================================================================
hdr("3. Derivative identities (polynomial identities checked at more points than their degree)")
# tau' : 12(20r - r^2 - 1) - (12r - 3/4)(20 - 2r) = (3/2)(8r^2 - r + 2), a quadratic identity
print("  tau' numerator: 12(20r - r^2 - 1) - (12r - 3/4)(20 - 2r) - (3/2)(8r^2 - r + 2) at r = 0, 1, 2, 3, 7/4:",
      [str(12 * (20 * r - r * r - 1) - (12 * r - Fr(3, 4)) * (20 - 2 * r) - Fr(3, 2) * (8 * r * r - r + 2))
       for r in (Fr(0), Fr(1), Fr(2), Fr(3), Fr(7, 4))])
# Delta' : d/dr (r-1)^2/(2r) = (r^2 - 1)/(2 r^2): 2(r-1) 2r - 2 (r-1)^2 = 2 (r^2 - 1)
print("  Delta' numerator: 4r(r-1) - 2(r-1)^2 - 2(r^2 - 1) at r = 0, 1, 2, 3:",
      [str(4 * r * (r - 1) - 2 * (r - 1) ** 2 - 2 * (r * r - 1)) for r in (Fr(0), Fr(1), Fr(2), Fr(3))])
# lambda_E' : 2 beta D + beta (2t - 1)(1 - 2 beta) = beta, with D = beta + (1 - 2 beta)(1 - t)
print("  lambda_E' numerator: 2 beta D(t) + beta(2t-1)(1-2beta) - beta at t = 0, 1/2, 1:",
      [str(2 * BETA * (BETA + (1 - 2 * BETA) * (1 - t)) + BETA * (2 * t - 1) * (1 - 2 * BETA) - BETA)
       for t in (Fr(0), Fr(1, 2), Fr(1))])
# M_{lambda_E(tau)} = tau
print("  M at lambda_E(tau) minus tau at tau = 0.6, 0.7, 0.73:",
      [str(M_of(lamE(t)) - t) for t in (Fr(3, 5), Fr(7, 10), Fr(73, 100))])
print("  tau' from the formula against a symmetric difference quotient with step 10^-8 at r = 2, 3:")
for r in (Fr(2), Fr(3)):
    hstep = Fr(1, 10 ** 8)
    dq = (tau(r + hstep) - tau(r - hstep)) / (2 * hstep)
    print(f"    r = {r}: formula {float(dtau(r)):.12f}, quotient {float(dq):.12f}")

# ================================================================================================
hdr("4. The floor margin phi(r) = rho Delta (1 - tau) - k - a lambda_E (exact rationals)")
for r in (R0, Fr(3, 2), Fr(7, 4), Fr(2), Fr(43, 20), Fr(11, 5), Fr(5, 2), R1, R2):
    v = phi_floor(r)
    print(f"  r = {str(r):<6} phi = {rnd(v, 9):>13}   phi' = {rnd(dphi_floor(r), 9)}   "
          f"tau = {rnd(tau(r), 9)}   lambda_E = {rnd(lamE(tau(r)), 9)}")

# ================================================================================================
hdr("5. Lower bound on phi' over the pieces [r_0 + i/10, r_0 + (i+1)/10] of [r_0, r_2]")
print("  b(r',r'') = rho[Delta'(r')(1 - tau(r'')) - Delta(r'') T(r',r'')] - a beta T(r',r'')/[beta + (1-2beta)(1-tau(r''))]^2,")
print("  T(r',r'') = 3(8(r'')^2 - r'' + 2)/[2(20r' - (r')^2 - 1)^2] >= tau' on [r',r'']")
pieces = []
l = R0
while l < R2:
    u = l + STEP
    pieces.append((l, u))
    l = u
bmin, argmin = None, None
for (l, u) in pieces:
    b = b_piece(l, u)
    # the exact derivative at both ends, for comparison with the bound
    dl, du = dphi_floor(l), dphi_floor(u)
    print(f"  [{float(l):.1f}, {float(u):.1f}]  b = {rnd_down(b, 6)}   phi'(r') = {rnd(dl, 6)}   phi'(r'') = {rnd(du, 6)}"
          f"   b <= min(phi'(r'), phi'(r'')): {b <= min(dl, du)}")
    if bmin is None or b < bmin:
        bmin, argmin = b, (l, u)
print(f"  number of pieces: {len(pieces)} ; last right end equals r_2: {pieces[-1][1] == R2}")
print(f"  smallest b: {rnd_down(bmin, 9)} (rounded down), on [{argmin[0]}, {argmin[1]}]")
print(f"  smallest b at least {LB_CLAIM}: {bmin >= LB_CLAIM}")
print(f"  exact smallest b: {bmin.numerator}/{bmin.denominator}" if len(str(bmin.denominator)) < 400
      else "  exact smallest b: (long rational)")
print("  For comparison, single pieces: "
      f"b(6/5, 7/4) = {rnd(b_piece(R0, Fr(7, 4)), 6)}, b(17/10, 5/2) = {rnd(b_piece(Fr(17, 10), Fr(5, 2)), 6)}, "
      f"b(5/2, 18/5) = {rnd(b_piece(Fr(5, 2), R2), 6)}, b(17/10, 18/5) = {rnd(b_piece(Fr(17, 10), R2), 6)}")

# ================================================================================================
hdr("6. Boundary strengths (brackets from decided signs of increasing functions on [r_0, r_2])")
two_k_rho = 2 * K / RHO
br_N = bracket(lambda r: Delta(r) - two_k_rho, R0, R2)
rN_closed = (29 + 6 * sqrt_iv(Fr(6))) / 25
print(f"  r_N: rho Delta = 2k, Delta = {two_k_rho}; bracket [{rnd_down(br_N[0], 22)}, {rnd_up(br_N[1], 22)}]")
print(f"       closed form (29 + 6 sqrt 6)/25 in {digits(rN_closed, 22)}")
print(f"       25 r^2 - 58 r + 25 at the closed form, interval: {digits(25 * rN_closed ** 2 - 58 * rN_closed + 25, 20)}")
d_cap = (2 * A * CAP + K) * (1 + EUL)
d_S = K * (1 + EUL) / RHO
d_U = (K + A * CAP) * (1 + EUL) / RHO
br_cap = bracket(lambda r: Delta(r) - d_cap, R0, R2)
br_S = bracket(lambda r: Delta(r) - d_S, R0, R2)
br_U = bracket(lambda r: Delta(r) - d_U, R0, R2)
br_C = bracket(lambda r: tau(r) - M_CAP, R0, R2)
print(f"  r_cap: Delta = (2 a cap + k)(1 + e); bracket [{rnd_down(br_cap[0], 22)}, {rnd_up(br_cap[1], 22)}]; "
      f"closed form {digits(frak_r(d_cap), 22)}")
print(f"  r_S:   Delta = k(1 + e)/rho;          bracket [{rnd_down(br_S[0], 22)}, {rnd_up(br_S[1], 22)}]; "
      f"closed form {digits(frak_r(d_S), 22)}")
print(f"  r_U:   Delta = (k + a cap)(1 + e)/rho; bracket [{rnd_down(br_U[0], 22)}, {rnd_up(br_U[1], 22)}]; "
      f"closed form {digits(frak_r(d_U), 22)}")
print(f"  r_C:   tau = e/(1 + e);               bracket [{rnd_down(br_C[0], 22)}, {rnd_up(br_C[1], 22)}]")
for name, br in (("r_N", br_N), ("r_cap", br_cap), ("r_S", br_S), ("r_U", br_U), ("r_C", br_C)):
    print(f"    {name:<6} bracket width {float(br[1] - br[0]):.2e}; undecided midpoint: {br[2]}")

# ================================================================================================
hdr("7. The floor margin at the boundary strengths, and the order of the strengths")
br_Q = bracket(phi_floor, Fr(7, 4), Fr(5, 2), steps=100)
print(f"  phi(7/4) = {rnd(phi_floor(Fr(7, 4)), 9)} < 0 and phi(5/2) = {rnd(phi_floor(Fr(5, 2)), 9)} > 0")
phi_N = at_bracket(phi_floor, br_N)
print(f"  phi(r_N) in {digits(phi_N, 12)} (sign {sign(phi_N)})")
phi_N_struct2 = Iv(min(lo_of(K * (1 - 2 * tau(br_N[0])) - A * lamE(tau(br_N[0]))),
                       lo_of(K * (1 - 2 * tau(br_N[1])) - A * lamE(tau(br_N[1])))),
                   max(hi_of(K * (1 - 2 * tau(br_N[0])) - A * lamE(tau(br_N[0]))),
                       hi_of(K * (1 - 2 * tau(br_N[1])) - A * lamE(tau(br_N[1])))))
print(f"  k(1 - 2 tau(r_N)) - a lambda_E(r_N) in {digits(phi_N_struct2, 12)}  (sign {sign(phi_N_struct2)})")
phi_U = at_bracket(phi_floor, br_U)
U_margin_at_U = at_bracket(lambda r: RHO * Delta(r) * m_CAP - K - A * CAP, br_U)
print(f"  phi(r_U) in {digits(phi_U, 12)} (sign {sign(phi_U)}); (U) margin rho Delta m_cap - k - a cap at r_U "
      f"in {digits(U_margin_at_U, 12)}")
phi_C = at_bracket(phi_floor, br_C)
U_margin_at_C = at_bracket(lambda r: RHO * Delta(r) * m_CAP - K - A * CAP, br_C)
print(f"  phi(r_C) in {digits(phi_C, 12)} (sign {sign(phi_C)}); (U) margin at r_C in {digits(U_margin_at_C, 12)}")
lamE_C = at_bracket(lambda r: lamE(tau(r)), br_C)
print(f"  lambda_E(r_C) in {digits(lamE_C, 18)} ; cap in {digits(CAP, 18)}")
gap_identity = [(RHO * Delta(r) * (M_CAP - tau(r)) + A * (CAP - lamE(tau(r))), r) for r in (Fr(5, 2), R1)]
for v, r in gap_identity:
    print(f"  phi minus (U) margin = rho Delta (M_cap - tau) + a (cap - lambda_E) at r = {r}: {digits(v, 12)}; "
          f"direct difference {digits(phi_floor(r) - (RHO * Delta(r) * m_CAP - K - A * CAP), 12)}")
order = [("r_0", Iv.of(R0)), ("r_cap", Iv(br_cap[0], br_cap[1])), ("r_N", Iv(br_N[0], br_N[1])),
         ("r_S", Iv(br_S[0], br_S[1])), ("r_Q", Iv(br_Q[0], br_Q[1])), ("r_U", Iv(br_U[0], br_U[1])),
         ("r_1", Iv.of(R1)), ("r_C", Iv(br_C[0], br_C[1])), ("r_2", Iv.of(R2))]
print("  order of the strengths:")
for (n1, v1), (n2, v2) in zip(order, order[1:]):
    print(f"    {n1} < {n2}: {v1.hi < v2.lo}   ({show(v1)} < {show(v2)})")
print("  In the recruiting equilibrium at the cap the low class abstains up to r_N, mixes on (r_N, r_S) and sells")
print("  with probability one from r_S; r_S < r_Q, so the low class sells with probability one on [r_S, r_Q).")

# ================================================================================================
hdr("8. r_Q, the zero of the floor margin")
rQ = Iv(br_Q[0], br_Q[1])
print(f"  bracket [{rnd_down(br_Q[0], 24)}, {rnd_up(br_Q[1], 24)}], width {float(br_Q[1] - br_Q[0]):.2e}; "
      f"undecided midpoint: {br_Q[2]}")
print(f"  phi at the bracket ends: {float(phi_floor(br_Q[0])):.3e} and {float(phi_floor(br_Q[1])):.3e}")
print(f"  r_Q = {rnd(br_Q[0], 15)} (15 decimals) -> display {show(rQ)}")
tau_Q = at_bracket(tau, br_Q)
lamE_Q = at_bracket(lambda r: lamE(tau(r)), br_Q)
print(f"  tau(r_Q) in {digits(tau_Q, 18)} -> {show(tau_Q)}")
print(f"  lambda_E(r_Q) in {digits(lamE_Q, 18)} -> {show(lamE_Q)}")
LQ_lo, LQ_hi = floor_root(Delta(br_Q[0])), floor_root(Delta(br_Q[1]))
print(f"  floor root at the bracket ends: {digits(LQ_lo, 18)} and {digits(LQ_hi, 18)}")
print(f"  floor root minus lambda_E at the left end:  {digits(LQ_lo - lamE(tau(br_Q[0])), 12)} (sign {sign(LQ_lo - lamE(tau(br_Q[0])))})")
print(f"  floor root minus lambda_E at the right end: {digits(LQ_hi - lamE(tau(br_Q[1])), 12)} (sign {sign(LQ_hi - lamE(tau(br_Q[1])))})")
print(f"  floor root at r_Q below the cap: {LQ_hi.hi < CAP.lo}  (cap {show(CAP)})")
print(f"  phi'(r_Q) at the bracket ends: {rnd(dphi_floor(br_Q[0]), 9)}, {rnd(dphi_floor(br_Q[1]), 9)}")
print(f"  M at the floor root, at the bracket ends: {digits(M_of(LQ_lo), 14)}, {digits(M_of(LQ_hi), 14)}; "
      f"tau there: {rnd(tau(br_Q[0]), 14)}, {rnd(tau(br_Q[1]), 14)}")
print(f"  rho Delta(r_Q) - 2k in {digits(at_bracket(lambda r: RHO * Delta(r) - 2 * K, br_Q), 12)} (positive)")

# ================================================================================================
hdr("9. The comparison tau versus M at floor research, against the sign of the floor margin")
print("  r       floor root            cap?   floor research   M there      tau          tau-M  phi    root-lambda_E")
for r in (Fr(7, 4), Fr(9, 5), Fr(19, 10), Fr(2), Fr(21, 10), Fr(43, 20), Fr(217, 100), Fr(11, 5), Fr(23, 10),
          Fr(12, 5), Fr(5, 2), Fr(14, 5), R1, Fr(7, 2), Fr(359, 100), R2):
    D = Delta(r)
    if RHO * D <= 2 * K:
        print(f"  {float(r):<6.3f} rho Delta <= 2k: no positive floor research")
        continue
    root = floor_root(D)
    s_cap = sign(root - CAP)
    q = root if s_cap < 0 else CAP
    Mq = M_of(q)
    t = tau(r)
    print(f"  {float(r):<6.3f}  {show(root, 9):<20}  {'cap' if s_cap > 0 else '   '}    {show(q, 6):<15}  "
          f"{show(Mq, 6):<11}  {rnd(t, 6):<11}  {sign(t - Mq):+d}     {sign(phi_floor(r)):+d}     "
          f"{sign(root - lamE(t)):+d}")
print("  (For r <= r_C the columns tau-M and phi carry opposite signs; above r_C the floor research is at the cap.)")
print("  floor root at the r_U bracket ends minus the cap: "
      f"{digits(floor_root(Delta(br_U[0])) - CAP, 14)}, {digits(floor_root(Delta(br_U[1])) - CAP, 14)}")

# ================================================================================================
hdr("10. Equilibrium conditions of stated tuples, from the auction rules (payoffs from prices)")


def tuple_report(label, r, lam, sig, zeta):
    """Prints (E1)-(E7) for the tuple with research lam, order laws sig[j][q] and preparation zeta[q]."""
    auc = auction_by_integration(r)
    t0, tH, tL, gH, gL = auc["t0"], auc["tH"], auc["tL"], auc["gH"], auc["gL"]
    f = {j: {q: (1 - lam) * ETA[q] + lam * sig[j][q] for q in (-1, 0, 1)} for j in ("H", "L")}
    mu = {q: f["H"][q] / (f["H"][q] + f["L"][q]) for q in (-1, 0, 1)}
    e = {q: RHO + (1 - RHO) * zeta[q] for q in (-1, 0, 1)}
    price = {q: t0 + e[q] * ((1 - mu[q]) * (tL - t0) + mu[q] * (tH - t0)) for q in (-1, 0, 1)}
    t_of = {"H": tH, "L": tL}
    Upay = {j: {q: q * (t0 + e[q] * (t_of[j] - t0) - price[q]) - K * abs(q) for q in (-1, 0, 1)} for j in ("H", "L")}
    Bgross = {q: gL + mu[q] * (gH - gL) for q in (-1, 0, 1)}
    print(f"  {label} at r = {r} ({float(r):.3f}); research {show(lam, 9)}")
    print(f"    posteriors (sale, none, purchase): {show(mu[-1], 6)}, {show(mu[0], 6)}, {show(mu[1], 6)}; "
          f"tau = {rnd(tau(r), 6)}")
    ivp = {q: Iv.of(price[q]) for q in (-1, 0, 1)}
    disjoint = all(ivp[a].hi < ivp[b].lo or ivp[b].hi < ivp[a].lo for a, b in ((-1, 0), (-1, 1), (0, 1)))
    print(f"    (E2) the three price intervals are pairwise disjoint: {disjoint}, so the belief at each price is "
          "the posterior of its order")
    ok3 = True
    for q in (-1, 0, 1):
        s = sign(Bgross[q] - CH)
        good = (zeta[q] == 1 and s >= 0) or (zeta[q] == 0 and s < 0)
        ok3 = ok3 and good
    print(f"    (E3) B(belief) - c_H signs {[sign(Bgross[q] - CH) for q in (-1, 0, 1)]} with stated preparation "
          f"{[zeta[q] for q in (-1, 0, 1)]}: consistent with preparing at a tie: {ok3}")
    best = {}
    for j in ("H", "L"):
        vals = Upay[j]
        top = vals[-1]
        for q in (0, 1):
            top = iv_max(top, vals[q])
        best[j] = top
        support = [q for q in (-1, 0, 1) if sign(sig[j][q]) > 0]
        verdicts = []
        for q in support:
            others = [q2 for q2 in (-1, 0, 1) if q2 != q]
            strict = all(lo_of(vals[q]) > hi_of(vals[q2]) for q2 in others)
            weak = all(hi_of(vals[q]) >= lo_of(vals[q2]) for q2 in others)
            verdicts.append(f"{q:+d}: {'strict best' if strict else ('best with a tie' if weak else 'NOT best')}")
        print(f"    (E5) class {j}: U(-1), U(0), U(1) = {show(vals[-1], 6)}, {show(vals[0], 6)}, {show(vals[1], 6)}; "
              + "; ".join(verdicts))
    Psi = (best["H"] + best["L"]) / 2
    ratio = Iv.of(Psi) / A
    if hi_of(ratio) < CAP.lo:
        zstar, which = ratio, "Psi/a"
    elif lo_of(ratio) > CAP.hi:
        zstar, which = CAP, "cap"
    else:
        zstar, which = None, "undecided"
    if zstar is None:
        print(f"    (E7) Psi/a = {show(ratio, 9)}, cap {show(CAP, 9)}: undecided")
    else:
        diff = Iv.of(zstar) - lam
        print(f"    (E7) best research min(cap, Psi/a) = {which} = {show(zstar, 9)}; minus stated research in "
              f"[{float(diff.lo):.2e}, {float(diff.hi):.2e}]")
    entry = sum((f["H"][q] + f["L"][q]) / 2 * e[q] for q in (-1, 0, 1))
    print(f"    entry {show(entry, 6)}")
    return entry


ONE = Fr(1)
ZERO = Fr(0)
print("  Research at the entry floor: both classes trade, no order recruits.")
for r in (Fr(9, 5), Fr(2), Fr(21, 10), Fr(43, 20), Fr(11, 5), R2):
    root = floor_root(Delta(r))
    lam = root if sign(root - CAP) < 0 else CAP
    sig = {"H": {-1: ZERO, 0: ZERO, 1: ONE}, "L": {-1: ONE, 0: ZERO, 1: ZERO}}
    tuple_report("floor tuple", r, lam, sig, {-1: 0, 0: 0, 1: 0})
print()
print("  Recruiting research at the cap: class H buys; class L sells with probability")
print("  s = min{1, b(rho Delta - 2k)^+/(k cap)}, b = (1 - cap) beta; only a purchase recruits.")
entries_cap = []
for r in (Fr(17, 10), Fr(7, 4), Fr(9, 5), Fr(2), Fr(21, 10), Fr(11, 5), R1, Fr(7, 2), R2):
    bbar = (1 - CAP) * BETA
    raw = RHO * Delta(r) - 2 * K
    if raw <= 0:
        s = ZERO
    else:
        s_mix = bbar * raw / (K * CAP)
        s = s_mix if sign(s_mix - 1) < 0 else ONE
    sig = {"H": {-1: ZERO, 0: ZERO, 1: ONE}, "L": {-1: s, 0: 1 - s, 1: ZERO}}
    print(f"  sale probability of class L: {show(s, 9)}")
    entries_cap.append(tuple_report("recruiting tuple at the cap", r, CAP, sig, {-1: 0, 0: 0, 1: 1}))

# ================================================================================================
hdr("11. Values beside the table displays")
entry_cap = RHO + (1 - RHO) * (BETA + (Fr(1, 2) - BETA) * CAP)
beside("prim_h", str(H))
beside("prim_ell", str(ELL))
beside("prim_rho", str(RHO))
beside("prim_k", str(K))
beside("prim_cH", str(CH))
beside("prim_p", str(P))
beside("prim_pi", str(PRIOR))
beside("prim_r0", str(R0))
beside("prim_r1", str(R1))
beside("prim_r2", str(R2))
beside("res_a", str(A))
beside("beta_B", BETA, 6)
beside("u_B", U_SLOT, 6)
beside("res_cap", CAP, 6)
beside("lambda_B", CAP, 6)
beside("M_half_B", M_CAP, 6)
beside("m_half_B", m_CAP, 6)
beside("res_rN", Iv(br_N[0], br_N[1]), 6)
beside("rN", rN_closed, 6)
beside("res_rcap", Iv(br_cap[0], br_cap[1]), 6)
beside("margin_res_rN_B", Iv(br_N[0], br_N[1]) - Iv(br_cap[0], br_cap[1]), 6)
beside("rS_B", Iv(br_S[0], br_S[1]), 6)
beside("res_rUR", Iv(br_U[0], br_U[1]), 6)
beside("res_rC", Iv(br_C[0], br_C[1]), 6)
beside("rC_B", Iv(br_C[0], br_C[1]), 6)
beside("res_entry_cap", entry_cap, 6, "rho + (1-rho)[beta + (1/2 - beta) cap]")
print(f"  entry of the recruiting tuples at the cap above: {', '.join(show(x) for x in entries_cap)}")
beside("entry_r0", RHO, 6, "entry rho")
beside("tau_r2", tau(R2), 6, f"exact {tau(R2)}")
beside("margin_res_bound_r1_B", RHO * Delta(R1) * m_CAP - K - A * CAP, 6, "(U) margin at r_1")
beside("margin_res_bound_r2_B", RHO * Delta(R2) * m_CAP - K - A * CAP, 6, "(U) margin at r_2")
beside("margin_res_tau_r1_B", M_CAP - tau(R1), 6, "M_cap - tau(r_1)")
beside("margin_res_tau_r2_B", tau(R2) - M_CAP, 6, "tau(r_2) - M_cap")

# ================================================================================================
hdr("12. Proposed rows")
print(f"  res_rQ               value {rnd(br_Q[0], 15)}   display {show(rQ)}   "
      "zero of the floor margin rho Delta(1 - tau) - k - a lambda_E on [r_0, r_2]")
print(f"  res_lambda_floor_rQ  value {rnd(lamE_Q.lo, 15)}   display {show(lamE_Q)}   "
      "lambda_E(r_Q) = floor research at r_Q")
print(f"  res_floor_step       value 1/10   display 1/10   width of the pieces in the bound on the floor margin's slope")
print(f"  res_floor_dphi_lb    value 1/100  display 1/100  lower bound on that slope over [r_0, r_2] "
      f"(smallest piece bound {rnd_down(bmin, 6)})")
print(f"  for reference: tau(r_Q) = {show(tau_Q)}; r_Q to 20 decimals {rnd_down(br_Q[0], 20)} .. {rnd_up(br_Q[1], 20)}")
