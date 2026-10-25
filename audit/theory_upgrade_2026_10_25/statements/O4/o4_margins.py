#!/usr/bin/env python3
"""Margins of the recruiting equilibrium along the example path, and the rows that the area-C statements print.

The example: the incumbent's value is uniform on [0, r]; the class values are h = 10 and ell = 1; the reserve is
p = 1/2; the preparation cost is zero with probability rho = 1/4 and c_H = 6 otherwise; the trading cost is
k = 1/50; the prior is 1/2; the liquidity share is beta = 294655/10^6, and the slot has 1 + u = e. Research costs
(a/2) lambda^2 with a = 1/40, up to the cap lambda_bar = u beta/(1 + u beta). The strengths run over
[r_0, r_2] = [6/5, 18/5]. Section 6 also takes the cost a = 1/5 with every other primitive unchanged.

Every quantity is an exact rational, or a closed interval with rational endpoints that contains the exact value:
Euler's number enters through the partial sums of its series and the bound 2/(N+1)! on the tail, and each square
root through integer square roots. Interval endpoints are rounded outward to multiples of 10^-60. The program
prints; it checks nothing by assertion.

Usage: python3 o4_margins.py
"""

import csv
from fractions import Fraction as Fr
from math import factorial, isqrt
from pathlib import Path

# ------------------------------------------------------------------------------------------------
# Intervals with rational endpoints (the same arithmetic as the program of statements/O1)

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


def pos(x):
    """The positive part of a rational or of an interval."""
    if isinstance(x, Iv):
        return Iv(max(Fr(0), x.lo), max(Fr(0), x.hi), round_out=False)
    return max(Fr(0), Fr(x))


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
    x = Fr(x)
    q = (x.numerator * 10 ** n) // x.denominator
    neg = q < 0
    s = str(abs(q)).rjust(n + 1, "0")
    return ("-" if neg else "") + s[:-n] + "." + s[-n:]


def rnd_up(x, n):
    x = Fr(x)
    q = -((-x.numerator * 10 ** n) // x.denominator)
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


def frac(x):
    x = Fr(x)
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def hdr(title):
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


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
    return Iv(lo_of(fun(br[0])), hi_of(fun(br[1])))


def hull(*xs):
    return Iv(min(lo_of(x) for x in xs), max(hi_of(x) for x in xs), round_out=False)


# ------------------------------------------------------------------------------------------------
# Primitives of the example

H, ELL, P = Fr(10), Fr(1), Fr(1, 2)
RHO, CH, K = Fr(1, 4), Fr(6), Fr(1, 50)
BETA = Fr(294655, 10 ** 6)
A0 = Fr(1, 40)          # the example's research cost
A1 = Fr(1, 5)           # the variant of section 6
R0, R1, R2 = Fr(6, 5), Fr(3), Fr(18, 5)

N_E = 40
_S = sum(Fr(1, factorial(n)) for n in range(N_E + 1))
EUL = Iv(_S, _S + Fr(2, factorial(N_E + 1)), round_out=False)
U_SLOT = EUL - 1
CAP = 1 - 1 / (1 + U_SLOT * BETA)          # u beta / (1 + u beta)
M_CAP = 1 - 1 / (1 + EUL)                 # e / (1 + e)
m_CAP = 1 / (1 + EUL)                     # 1 / (1 + e)
B_CAP = (1 - CAP) * BETA                  # liquidity mass b at the cap
PURCH_CAP = B_CAP + CAP / 2               # purchase probability b + lambda/2 at the cap

# ------------------------------------------------------------------------------------------------
# The auction of the example, 1 < r < 10


def Delta(r):
    return (r - ELL) ** 2 / (2 * r)


def dDelta(r):
    return (1 - ELL ** 2 / r ** 2) / 2


def gL(r):
    return (ELL ** 2 - P ** 2) / (2 * r)


def gH(r):
    return H - r / 2 - P ** 2 / (2 * r)


def t0(r):
    return P * (1 - P / r)


def tL(r):
    return ELL - (ELL ** 2 - P ** 2) / (2 * r)


def tau(r):
    return (CH - gL(r)) / (gH(r) - gL(r))


def dtau(r):
    return 3 * (8 * r * r - r + 2) / (2 * (20 * r - r * r - 1) ** 2)


def T_bound(l, u):
    """Upper bound on tau' over [l, u]: largest numerator over smallest denominator."""
    return 3 * (8 * u * u - u + 2) / (2 * (20 * l - l * l - 1) ** 2)


def J(r):
    return Delta(r) * (1 - tau(r))


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


def phi_a(r, a):
    """The recruitment margin J - k - 2 a lambda_E, an exact rational at rational r."""
    return J(r) - K - 2 * a * lamE(tau(r))


def phi_star(r, a):
    """The exact recruitment margin J - k + (rho J - k)^+ - 2 a lambda_E."""
    j = J(r)
    return j - K + pos(RHO * j - K) - 2 * a * lamE(tau(r))


def phi_rho(r, a):
    """The floor margin rho J - k - a lambda_E."""
    return RHO * J(r) - K - a * lamE(tau(r))


def dphi_a(r, a):
    t = tau(r)
    tp = dtau(r)
    return dDelta(r) * (1 - t) - Delta(r) * tp - 2 * a * dlamE(t) * tp


def b_piece(l, u, a):
    """Lower bound on phi_a' over [l, u]: Delta'(l)(1 - tau(u)) - [Delta(u) + 2a lambda_E'(tau(u))] T(l,u)."""
    tu = tau(u)
    T = T_bound(l, u)
    return dDelta(l) * (1 - tu) - (Delta(u) + 2 * a * dlamE(tu)) * T


def quad_root(qa, qb, qc):
    """The positive root of qa x^2 + qb x + qc with qa > 0 > qc, as -2 qc / (qb + sqrt(qb^2 - 4 qa qc))."""
    disc = qb * qb - 4 * qa * qc
    return Iv.of(-2 * qc) / (qb + sqrt_iv(disc))


def lamR(D, a):
    """The root in (0, 1) of 2 a lambda = D m - k + (rho D m - k)^+, for D > 2k; also returns the piece used."""
    r1 = quad_root(2 * a * (1 - 2 * BETA), 4 * a * BETA + K * (1 - 2 * BETA) + BETA * D, BETA * (2 * K - D))
    if sign(RHO * D * m_of(r1) - K) <= 0:
        # rho D m <= k at the root of the first piece (an undecided sign would print as 0 and use this piece)
        return r1, "abstain-or-mix piece"
    r2 = quad_root(2 * a * (1 - 2 * BETA), 4 * a * BETA + 2 * K * (1 - 2 * BETA) + (1 + RHO) * BETA * D,
                   BETA * (4 * K - (1 + RHO) * D))
    return r2, "full-sale piece"


def lamQ(D, a):
    """The root in (0, 1) of a lambda = rho D m - k, for rho D > 2k."""
    return quad_root(a * (1 - 2 * BETA), RHO * D * BETA + K * (1 - 2 * BETA) + 2 * a * BETA, BETA * (2 * K - RHO * D))


def frak_r(d):
    """The strength above ell at which Delta(r) = d: r = ell + d + sqrt(d^2 + 2 ell d)."""
    return ELL + d + sqrt_iv(d * d + 2 * ELL * d)


def kink_research(a):
    return (1 - RHO) * K / (2 * a * RHO)


def cap_spread(a):
    """The spread at which research reaches the cap: W3 eq. (9)."""
    if sign(CAP - kink_research(a)) <= 0:
        return (2 * a * CAP + K) / m_CAP, "cap at or below the kink research"
    return (2 * a * CAP + 2 * K) / ((1 + RHO) * m_CAP), "cap above the kink research"


def e_star(r, a):
    """Entry after a purchase in the threshold pair: [2 a lambda_E + k - (rho J - k)^+]/J."""
    j = J(r)
    return (2 * a * lamE(tau(r)) + K - pos(RHO * j - K)) / j


# ------------------------------------------------------------------------------------------------
# The rows of the numbers table

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
    agree = "same" if mine == disp else ("ABSENT" if disp == "(absent)" else "DIFFERENT")
    print(f"  {key:<26} here {mine:<26} table display {disp:<14} {agree}  {note}")


# ================================================================================================
hdr("1. Primitives, Euler's number and the cap")
print(f"  beta = {BETA} ; a = {A0} ; rho = {RHO} ; k = {K} ; c_H = {CH} ; h = {H} ; ell = {ELL} ; p = {P}")
print(f"  e in {digits(EUL, 30)}")
print(f"  cap in {digits(CAP, 24)} -> {show(CAP)} ; M at the cap in {digits(M_CAP, 24)} ; m at the cap {show(m_CAP)}")
print(f"  m_lambda at the cap from the formula minus 1/(1+e): {digits(m_of(CAP) - m_CAP, 30)}")
print(f"  purchase probability at the cap, b + lambda/2 = beta + (1/2 - beta) cap: {show(PURCH_CAP, 9)}")

# ================================================================================================
hdr("2. The example at a = 1/40: the recruitment margin and the exact margin on [r_0, r_cap]")
kr = kink_research(A0)
print(f"  kink research (1 - rho) k/(2 a rho) = {frac(kr)} (> 1: {kr > 1}), so the research root is the root of the")
print("  abstain-or-mix piece 2 a lambda = Delta m - k at every strength, and the cap spread is (2 a cap + k)(1 + e)")
phi0 = phi_a(R0, A0)
print(f"  phi_a(r_0) = {frac(phi0)} = {rnd(phi0, 12)}  (exact rational)")
print(f"     J(r_0) = {frac(J(R0))}, tau(r_0) = {frac(tau(R0))}, lambda_E(r_0) = {frac(lamE(tau(R0)))} = {rnd(lamE(tau(R0)), 12)}")
print(f"     rho J(r_0) - k = {frac(RHO * J(R0) - K)} < 0, so phi*_a(r_0) = phi_a(r_0)")
dcap0, why0 = cap_spread(A0)
rcap0 = frak_r(dcap0)
print(f"  cap spread ({why0}) in {digits(dcap0, 18)} ; r_cap = frak_r(spread) in {digits(rcap0, 18)} -> {show(rcap0)}")
br_cap0 = bracket(lambda r: Delta(r) - dcap0, R0, R2)
print(f"  r_cap by bisection of Delta(r) - spread: [{rnd_down(br_cap0[0], 18)}, {rnd_up(br_cap0[1], 18)}]")
phi_cap = at_bracket(lambda r: phi_a(r, A0), br_cap0)
print(f"  phi_a(r_cap) in {digits(phi_cap, 14)} -> {show(phi_cap)}  (phi_a rises on [r_0, 7/4], see below)")
rhoJcap = at_bracket(lambda r: RHO * J(r) - K, br_cap0)
print(f"  rho J(r_cap) - k in {digits(rhoJcap, 14)}  (negative: phi*_a(r_cap) = phi_a(r_cap))")
r74 = Fr(7, 4)
print(f"  J(7/4) = {frac(J(r74))} ; rho J(7/4) = {frac(RHO * J(r74))} = {rnd(RHO * J(r74), 9)} < k = {K}: {RHO * J(r74) < K}")
tail_margin = J(r74) - K - 2 * A0 * lamE(tau(R2))
print(f"  res_J74_frac = {frac(J(r74))}; J(7/4) - k - 2 a lambda_E(r_2) = {frac(tail_margin)} = {rnd(tail_margin, 12)}")
# the existing one-piece bound over [6/5, 7/4]
T0 = T_bound(R0, r74)
lead = dDelta(R0) * (1 - tau(r74)) - Delta(r74) * T0
phip = lead - 2 * A0 * dlamE(tau(r74)) * T0
print(f"  one piece [6/5, 7/4]: Delta'(6/5) = {frac(dDelta(R0))}, 1 - tau(7/4) = {frac(1 - tau(r74))}, "
      f"Delta(7/4) = {frac(Delta(r74))}, T = {frac(T0)}")
print(f"     lower bound on J' = {frac(lead)} = {rnd(lead, 9)} ; on phi_a' at a = 1/40: {frac(phip)} = {rnd(phip, 9)}")
amono = lead / (2 * dlamE(tau(r74)) * T0)
print(f"     the bound on phi_a' stays positive for every a below {frac(amono)} = {rnd(amono, 9)}")
print(f"  r_cap < 7/4: {hi_of(rcap0) < r74}")
br_R = bracket(lambda r: phi_a(r, A0), R0, r74)
print(f"  r_R, the zero of phi_a on [6/5, 7/4]: [{rnd_down(br_R[0], 18)}, {rnd_up(br_R[1], 18)}] -> {rnd(br_R[0], 6)}")
lamE_R = at_bracket(lambda r: lamE(tau(r)), br_R)
print(f"  lambda_E(r_R) in {digits(lamE_R, 14)} -> {show(lamE_R)}")
ent_R = RHO + (1 - RHO) * (BETA + (Fr(1, 2) - BETA) * lamE_R)
print(f"  entry at r_R in {digits(ent_R, 14)} -> {show(ent_R)}")
for r in (Fr(31, 20), Fr(8, 5), Fr(33, 20)):
    D = Delta(r)
    lr, piece = lamR(D, A0)
    t = tau(r)
    eH = RHO + (1 - RHO) * (BETA + (1 - BETA) * lr)
    eL = RHO + (1 - RHO) * BETA * (1 - lr)
    ent = RHO + (1 - RHO) * (BETA + (Fr(1, 2) - BETA) * lr)
    print(f"  r = {float(r):.2f}: lambda_E = {rnd(lamE(t), 6)} < lambda_R = {show(lr)} ({piece}) < cap: "
          f"{lamE(t) < lo_of(lr) and hi_of(lr) < lo_of(CAP)} ; entry {show(ent)} ; e_H {show(eH)} ; e_L {show(eL)} ; "
          f"ownership e_H/2 {show(eH / 2)} ; e_H/rho {show(eH / RHO)} ; phi_a = {rnd(phi_a(r, A0), 6)}")

# ================================================================================================
hdr("3. The threshold pair in the example (an indifferent high-cost challenger may prepare with any probability)")
print("  e* = [2 a lambda_E + k - (rho J - k)^+]/J ; the pair needs rho <= e* <= 1 and lambda_E < cap")
print("  identities: 1 - e* = phi*_a/J ; and where rho J > k, e* - rho = -2 phi_rho/J")
for r in (Fr(29, 20), Fr(3, 2), Fr(31, 20), Fr(8, 5), Fr(33, 20), Fr(7, 4), Fr(2), Fr(43, 20), Fr(11, 5), Fr(5, 2)):
    es = e_star(r, A0)
    t = tau(r)
    ent = RHO + (es - RHO) * (BETA + (Fr(1, 2) - BETA) * lamE(t))
    ok = RHO <= es <= 1
    print(f"  r = {float(r):.3f}: e* = {rnd(es, 9):>12}  rho <= e* <= 1: {str(ok):<5}  entry {rnd(ent, 6)}  "
          f"1 - e* - phi*/J = {frac(1 - es - phi_star(r, A0) / J(r))}")
br_Q = bracket(lambda r: phi_rho(r, A0), r74, Fr(5, 2))
print(f"  r_Q (zero of the floor margin) in [{rnd_down(br_Q[0], 18)}, {rnd_up(br_Q[1], 18)}] -> {rnd(br_Q[0], 6)}")
print(f"  e* at the ends of the r_R bracket: {rnd(e_star(br_R[0], A0), 15)}, {rnd(e_star(br_R[1], A0), 15)}  (tends to 1)")
print(f"  e* at the ends of the r_Q bracket: {rnd(e_star(br_Q[0], A0), 15)}, {rnd(e_star(br_Q[1], A0), 15)}  (tends to rho)")
for key_e, key_n, r in (("res_th_estar_r155", "res_th_entry_r155", Fr(31, 20)),
                        ("res_th_estar_r160", "res_th_entry_r160", Fr(8, 5)),
                        ("res_th_estar_r165", "res_th_entry_r165", Fr(33, 20))):
    es = e_star(r, A0)
    ent = RHO + (es - RHO) * (BETA + (Fr(1, 2) - BETA) * lamE(tau(r)))
    beside(key_e, es)
    beside(key_n, ent)
# the cap family at r_C
br_C = bracket(lambda r: tau(r) - M_CAP, R0, R2)
print(f"  r_C in [{rnd_down(br_C[0], 18)}, {rnd_up(br_C[1], 18)}]")
JC = hull(Delta(br_C[0]) * m_CAP, Delta(br_C[1]) * m_CAP)
WC = pos(RHO * JC - K)
lowC = (2 * A0 * CAP + K - WC) / JC
print(f"  J(r_C) = Delta(r_C) m_cap in {digits(JC, 12)} ; (rho J - k)^+ in {digits(WC, 12)}")
print(f"  lower endpoint (2 a cap + k - (rho J - k)^+)/J at r_C in {digits(lowC, 12)} ; below rho: {hi_of(lowC) < RHO}")
print(f"  so every e(1) in [rho, 1] is admitted at r_C, and entry rho + (e(1) - rho)(b + cap/2) fills "
      f"[{rnd(RHO, 6)}, {show(RHO + (1 - RHO) * PURCH_CAP)}]")

# ================================================================================================
hdr("4. At r = 2, when an indifferent investor abstains and an indifferent challenger may prepare with any probability")
r2 = Fr(2)
t = tau(r2)
le = lamE(t)
j = J(r2)
W = pos(RHO * j - K)
es = e_star(r2, A0)
UH = es * j - K
UL = RHO * Delta(r2) * m_of(le) - K
ent = RHO + (es - RHO) * (BETA + (Fr(1, 2) - BETA) * le)
Psi = (UH + max(UL, Fr(0))) / 2
print(f"  tau(2) = {frac(t)} ; Delta(2) = {frac(Delta(r2))} ; J(2) = {frac(j)} ; rho Delta(2) - 2k = {frac(RHO * Delta(r2) - 2 * K)} > 0")
print(f"  lambda_E(2) = {frac(le)} = {rnd(le, 12)}  (below the cap: {le < CAP.lo})")
print(f"  rho Delta m at lambda_E = rho J = {frac(RHO * j)} > k: {RHO * j > K}  (a sale with probability one strictly pays)")
print(f"  (rho J - k)^+ = {frac(W)} = {rnd(W, 12)}")
print(f"  e* = {frac(es)} = {rnd(es, 12)} ; preparation probability (e* - rho)/(1 - rho) = {rnd((es - RHO) / (1 - RHO), 12)}")
print(f"  U_H(1) = e* J - k = {rnd(UH, 12)} > 0 ; U_L(-1) = rho Delta m - k = {rnd(UL, 12)} > 0 ; both strict best orders")
print(f"  research value Psi = {rnd(Psi, 12)} ; Psi/a = {rnd(Psi / A0, 12)} ; equal to lambda_E: {Psi / A0 == le}")
print(f"  entry rho + (e* - rho)[beta + (1/2 - beta) lambda_E] = {frac(ent)} = {rnd(ent, 12)}")
lq2 = lamQ(Delta(r2), A0)
print(f"  for comparison: lambda_Q(Delta(2)) in {digits(lq2, 12)} < lambda_E(2) < cap")

# ================================================================================================
hdr("5. r_J, the root of rho J = k, and where the threshold pair survives an abstaining investor")
br_J = bracket(lambda r: RHO * J(r) - K, r74, Fr(9, 4))
print(f"  rho J(7/4) - k = {rnd(RHO * J(r74) - K, 9)} ; rho J(9/4) - k = {rnd(RHO * J(Fr(9, 4)) - K, 9)}")
print(f"  r_J in [{rnd_down(br_J[0], 18)}, {rnd_up(br_J[1], 18)}] -> {rnd(br_J[0], 6)}")
print("  rho J - k at sample strengths (sign):",
      [(float(r), sign(RHO * J(r) - K)) for r in (Fr(7, 4), Fr(9, 5), Fr(19, 10), Fr(39, 20), Fr(197, 100), Fr(2), Fr(21, 10), Fr(11, 5))])
br_N = bracket(lambda r: RHO * Delta(r) - 2 * K, R0, R2)
br_S = bracket(lambda r: RHO * Delta(r) * m_CAP - K, R0, R2)
print(f"  r_N in [{rnd_down(br_N[0], 15)}, {rnd_up(br_N[1], 15)}] ; r_S in [{rnd_down(br_S[0], 15)}, {rnd_up(br_S[1], 15)}]")
print(f"  order r_R < r_cap < r_N < r_J < r_S < r_Q: "
      f"{br_R[1] < br_cap0[0] and br_cap0[1] < br_N[0] and br_N[1] < br_J[0] and br_J[1] < br_S[0] and br_S[1] < br_Q[0]}")
print("  The threshold pair needs, when the investor abstains at a tie, rho Delta <= 2k (r <= r_N) or rho J > k (r > r_J);")
print("  on [r_R, r_Q] that leaves [r_R, r_N] and (r_J, r_Q].")

# ================================================================================================
hdr("6. The variant a = 1/5, every other primitive of the example unchanged")
kr1 = kink_research(A1)
print(f"  kink research (1 - rho) k/(2 a rho) = {frac(kr1)} = {rnd(kr1, 6)} < cap: {kr1 < CAP.lo}")
dcap1, why1 = cap_spread(A1)
rcap1 = frak_r(dcap1)
print(f"  cap spread ({why1}) in {digits(dcap1, 15)} ; r_cap = {digits(rcap1, 15)} -> {show(rcap1)}")
STEP = Fr(1, 50)
pieces = []
l = R0
while l < R2:
    pieces.append((l, l + STEP))
    l = l + STEP
bmin, argmin = None, None
for (l, u) in pieces:
    b = b_piece(l, u, A1)
    if bmin is None or b < bmin:
        bmin, argmin = b, (l, u)
print(f"  lower bound on phi_a' at a = 1/5 over {len(pieces)} pieces of width {STEP} covering [r_0, r_2] "
      f"(last end r_2: {pieces[-1][1] == R2}):")
print(f"     smallest piece bound {rnd_down(bmin, 9)} on [{argmin[0]}, {argmin[1]}] ; positive: {bmin > 0}")
print(f"     smallest piece bound at a = 1/40 on the same pieces: "
      f"{rnd_down(min(b_piece(l, u, A0) for (l, u) in pieces), 9)}")
print("  so phi_a rises strictly on [r_0, r_2] at a = 1/5, and with it J = phi_a + k + 2a lambda_E and phi*_a")
for r in (Fr(2), Fr(11, 5), Fr(9, 4), Fr(5, 2), Fr(8, 3)):
    print(f"     r = {float(r):.4f}: phi_a = {rnd(phi_a(r, A1), 9):>13}  phi*_a = {rnd(phi_star(r, A1), 9):>13}  "
          f"rho J - k = {rnd(RHO * J(r) - K, 9)}")
br_R1 = bracket(lambda r: phi_star(r, A1), Fr(2), Fr(5, 2))
br_Ra = bracket(lambda r: phi_a(r, A1), Fr(2), Fr(3))
print(f"  zero of phi*_a: [{rnd_down(br_R1[0], 15)}, {rnd_up(br_R1[1], 15)}] -> {rnd(br_R1[0], 6)}  (the start r_R)")
print(f"  zero of phi_a:  [{rnd_down(br_Ra[0], 15)}, {rnd_up(br_Ra[1], 15)}] -> {rnd(br_Ra[0], 6)}")
print(f"  at the start: rho J - k in {digits(at_bracket(lambda r: RHO * J(r) - K, br_R1), 12)} (> 0: a sure sale pays);"
      f" r_N < start: {br_N[1] < br_R1[0]} ; r_S < start: {br_S[1] < br_R1[0]}")
lE1 = at_bracket(lambda r: lamE(tau(r)), br_R1)
print(f"  research at the start, lambda_E, in {digits(lE1, 12)}")
for r in (Fr(9, 4), Fr(133, 50)):
    lr, piece = lamR(Delta(r), A1)
    print(f"  research root at r = {float(r):.2f}: {digits(lr, 12)} ({piece})")
print(f"  the recruiting equilibrium of the variant: one interval from {rnd(br_R1[0], 6)} to r_C = {rnd(br_C[0], 6)}, "
      f"with the cap from {show(rcap1)}")

# ================================================================================================
hdr("7. Access to prices with research at r_1: the general formulas against the table")
r = R1
wL = tL(r) - t0(r)
gam = gH(r) - gL(r)
dR = (1 - RHO) * PURCH_CAP * (wL + Delta(r) * M_CAP)
dW = (1 - RHO) * PURCH_CAP * (gam * (M_CAP - tau(r)) + P * (P / r))
print(f"  t_L - t_0 = {frac(wL)} ; Delta = {frac(Delta(r))} ; gamma = {frac(gam)} ; tau = {frac(tau(r))} ; p F(p) = {frac(P * P / r)}")
print(f"  M_cap - tau(r_1) in {digits(M_CAP - tau(r), 12)} (positive)")
beside("res_dR_r1", dR)
beside("res_dW_r1", dW)

# ================================================================================================
hdr("8. Values beside the table displays, and the proposed rows")
beside("res_phi_r0_frac", frac(phi0), note="exact rational display")
beside("res_bound_strength", "7/4", note="right endpoint of the derivative bound")
beside("res_beta_upper", "1/3", note="upper liquidity share in the six-strength statement")
beside("res_phi_rcap", phi_cap, note="proposed row")
beside("str_r200", Fr(2), n=0, note="proposed row; display 2")
beside("res_I0CM_lambda_r200", le, note="proposed row; exact rational above")
beside("res_I0CM_e1_r200", es, note="proposed row; exact rational above")
beside("res_I0CM_entry_r200", ent, note="proposed row; exact rational above")
beside("res_rR", Iv(br_R[0], br_R[1]))
beside("res_rcap", rcap0)
beside("res_rN", Iv(br_N[0], br_N[1]))
beside("rJ", Iv(br_J[0], br_J[1]))
beside("rS_B", Iv(br_S[0], br_S[1]))
beside("res_rC", Iv(br_C[0], br_C[1]))
beside("res_lambda_rR", lamE_R)
beside("res_entry_rR", ent_R)
beside("res_entry_cap", RHO + (1 - RHO) * PURCH_CAP)
beside("res_dphi_lead", lead)
beside("res_phip_lb", phip)
beside("res_amono", amono)
beside("res_phi_r155", phi_a(Fr(31, 20), A0))
for key_l, key_n, key_o, r in (("res_lambda_r155", "res_entry_r155", "res_own_r155", Fr(31, 20)),
                               ("res_lambda_r160", "res_entry_r160", "res_own_r160", Fr(8, 5)),
                               ("res_lambda_r165", "res_entry_r165", "res_own_r165", Fr(33, 20))):
    lr, _ = lamR(Delta(r), A0)
    beside(key_l, lr)
    beside(key_n, RHO + (1 - RHO) * (BETA + (Fr(1, 2) - BETA) * lr))
    beside(key_o, (RHO + (1 - RHO) * (BETA + (1 - BETA) * lr)) / 2)
print()
print(f"  exact values of the proposed rows:")
print(f"    res_phi_r0_frac      = {frac(phi0)}")
print(f"    res_phi_rcap         in {digits(phi_cap, 20)}")
print(f"    str_r200             = 2")
print(f"    res_I0CM_lambda_r200 = {frac(le)}")
print(f"    res_I0CM_e1_r200     = {frac(es)}")
print(f"    res_I0CM_entry_r200  = {frac(ent)}")
