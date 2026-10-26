#!/usr/bin/env python3
"""Numbers of the example that the upgraded statements print; writes registry/TU.csv.

The example: the incumbent's value is uniform on [0, r]; the class values are h = 10 and ell = 1; the reserve is
p = 1/2; the preparation cost is zero with probability rho = 1/4 and c_H = 6 otherwise; the trading cost is
k = 1/50; the prior is 1/2; the liquidity share is beta = 294655/10^6; the slot has 1 + u = e; research costs
(a/2) lambda^2 with a = 1/40 up to the cap lambda_bar = u beta/(1 + u beta); the strengths are
r_0 = 6/5, r_1 = 3, r_2 = 18/5.

Every rational quantity is computed with fractions.Fraction. Every quantity that involves e or a square root is a
closed interval (mpmath.iv, 80 digits) whose display is checked to be the same at both ends. Every root is
bracketed by a decided sign change of an exact rational function, and halved with exact signs; the monotonicity
that makes the root unique is stated in the note column of its row. The program prints; it checks nothing by
assertion, and it stops with a nonzero exit status only if a display is undecided or an output file cannot be
written.

Usage: python3 tu_numbers.py > run.log
"""

import csv
import hashlib
import platform
import sys
from fractions import Fraction as Fr
from pathlib import Path

import mpmath
from mpmath import iv, mp

iv.dps = 80
mp.dps = 80

ROOT = Path(__file__).resolve().parents[4]
TEAM = ROOT / "audit/slot_manuscript_2026_10_23"
OUT = TEAM / "registry/TU.csv"
REG_PATH = TEAM / "registry/registry.csv"
SRC = "scripts/TU/tu_numbers.py"
LOG = "scripts/TU/run.log"
COLS = ["key", "value", "display", "status", "source_script", "run_log", "note"]

# ------------------------------------------------------------------------------------------------
# Intervals and rounding


def I(q):
    q = Fr(q)
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


def fr_of(t):
    s, man, exp, _bc = t
    v = Fr(int(man)) * (Fr(2) ** exp if exp >= 0 else Fr(1, 2 ** (-exp)))
    return -v if s else v


def lohi(x):
    if hasattr(x, "_mpi_"):
        return fr_of(x._mpi_[0]), fr_of(x._mpi_[1])
    return Fr(x), Fr(x)


def hull(a, b):
    return iv.mpf([a.a, b.b])


def span(q1, q2):
    """The interval between the two rationals q1 <= q2."""
    return iv.mpf([I(min(q1, q2)).a, I(max(q1, q2)).b])


def rnd(x, n):
    """The rational x rounded half up (half away from zero) to n decimals, as a string."""
    x = Fr(x)
    neg = x < 0
    y = abs(x) * 10 ** n
    q = (y.numerator * 2 + y.denominator) // (2 * y.denominator)
    s = str(q).rjust(n + 1, "0")
    out = s[:-n] + "." + s[-n:] if n else s
    return ("-" if neg and q else "") + out


def rnd_down(x, n):
    x = Fr(x)
    q = (x.numerator * 10 ** n) // x.denominator
    s = str(abs(q)).rjust(n + 1, "0")
    return ("-" if q < 0 else "") + s[:-n] + "." + s[-n:]


def rnd_up(x, n):
    x = Fr(x)
    q = -((-x.numerator * 10 ** n) // x.denominator)
    s = str(abs(q)).rjust(n + 1, "0")
    return ("-" if q < 0 else "") + s[:-n] + "." + s[-n:]


def frac(x):
    x = Fr(x)
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def dec_exact(x):
    """A terminating decimal of the rational x, without trailing zeros (x must have only 2 and 5 in its denominator)."""
    x = Fr(x)
    for n in range(0, 30):
        if (x * 10 ** n).denominator == 1:
            s = rnd(x, n)
            return s
    raise SystemExit(f"{x} is not a terminating decimal")


def hdr(title):
    print()
    print("=" * 110)
    print(title)
    print("=" * 110)


# ------------------------------------------------------------------------------------------------
# The registry rows

ROWS = []


def _add(key, value, display, status, note):
    ROWS.append(dict(key=key, value=value, display=display, status=status, source_script=SRC, run_log=LOG, note=note))


def add_exact(key, q, display, status, note):
    """A rational row; the display is a string chosen by the caller."""
    _add(key, frac(q), display, status, note)
    print(f"  row {key:<28} = {frac(q):<34} display {display}")


def add_iv(key, x, nd, status, note, display=None):
    """An interval row, displayed to nd decimals; refuses a display that differs between the two ends."""
    lo, hi = lohi(x)
    a, b = rnd(lo, nd), rnd(hi, nd)
    if a != b:
        raise SystemExit(f"display of {key} undecided: {a} versus {b}")
    mid = (lo + hi) / 2
    full = f"{note}; enclosure [{rnd_down(lo, 25)}, {rnd_up(hi, 25)}]"
    _add(key, rnd(mid, 30), display or a, status, full)
    print(f"  row {key:<28} in [{rnd_down(lo, 20)}, {rnd_up(hi, 20)}]  display {display or a}")


def add_root(key, lo, hi, nd, status, note, display=None):
    """A row for a root given by a rational bracket [lo, hi] of a sign change."""
    a, b = rnd(lo, nd), rnd(hi, nd)
    if a != b:
        raise SystemExit(f"display of {key} undecided: {a} versus {b}")
    mid = (lo + hi) / 2
    _add(key, rnd(mid, 30), display or a, status, f"{note}; bracket [{rnd_down(lo, 25)}, {rnd_up(hi, 25)}]")
    print(f"  row {key:<28} in [{rnd_down(lo, 20)}, {rnd_up(hi, 20)}]  display {display or a}")


def bisect(f, lo, hi, width=Fr(1, 10 ** 60)):
    """Halve [lo, hi] by the decided sign of f (exact rationals); f(lo) and f(hi) must have opposite signs."""
    slo, shi = (f(lo) > 0) - (f(lo) < 0), (f(hi) > 0) - (f(hi) < 0)
    if slo * shi >= 0:
        raise SystemExit("no sign change on the bracket")
    while hi - lo > width:
        mid = (lo + hi) / 2
        sm = (f(mid) > 0) - (f(mid) < 0)
        if sm == 0:
            return mid, mid
        if sm == slo:
            lo = mid
        else:
            hi = mid
    return lo, hi


def out_bracket(x, digits=40):
    """Rational endpoints, rounded outward to 10^-digits, around an interval."""
    lo, hi = lohi(x)
    g = 10 ** digits
    return Fr((lo.numerator * g) // lo.denominator, g), Fr(-((-hi.numerator * g) // hi.denominator), g)


# ------------------------------------------------------------------------------------------------
# Primitives and the auction of the example (exact rationals)

H, ELL, P = Fr(10), Fr(1), Fr(1, 2)
RHO, CH, K = Fr(1, 4), Fr(6), Fr(1, 50)
BETA = Fr(294655, 10 ** 6)
A0 = Fr(1, 40)
R0, R1, R2 = Fr(6, 5), Fr(3), Fr(18, 5)

EUL = iv.e
U_SLOT = EUL - 1
CAP = U_SLOT * I(BETA) / (1 + U_SLOT * I(BETA))
M_CAP = EUL / (1 + EUL)
m_CAP = 1 / (1 + EUL)
B_PURCH = (1 - CAP) * I(BETA) + CAP / 2            # purchase probability b + lambda/2 at the cap


def Delta(r):
    return (r - ELL) ** 2 / (2 * r)


def gL(r):
    return (ELL ** 2 - P ** 2) / (2 * r)


def gH(r):
    return H - r / 2 - P ** 2 / (2 * r)


def tau(r):
    return (CH - gL(r)) / (gH(r) - gL(r))


def J(r):
    return Delta(r) * (1 - tau(r))


def L(t):
    """lambda_E as a function of the threshold t."""
    return BETA * (2 * t - 1) / (BETA + (1 - 2 * BETA) * (1 - t))


def phi_a(r, a=A0):
    return J(r) - K - 2 * a * L(tau(r))


def phi_rho(r, a=A0):
    return RHO * J(r) - K - a * L(tau(r))


def dDelta(r):
    return (1 - ELL ** 2 / r ** 2) / 2


def dtau(r):
    return 3 * (8 * r * r - r + 2) / (2 * (20 * r - r * r - 1) ** 2)


def dL(t):
    return BETA / (BETA + (1 - 2 * BETA) * (1 - t)) ** 2


def T_bound(l, u):
    return 3 * (8 * u * u - u + 2) / (2 * (20 * l - l * l - 1) ** 2)


def b_piece(l, u):
    tu = tau(u)
    T = T_bound(l, u)
    return RHO * (dDelta(l) * (1 - tu) - Delta(u) * T) - A0 * dL(tu) * T


def fr_root(d):
    """The strength above ell at which Delta(r) = d, for the interval d: ell + d + sqrt(d^2 + 2 ell d)."""
    return I(ELL) + d + iv.sqrt(d * d + 2 * I(ELL) * d)


def quad_root(qa, qb, qc):
    """The positive root of qa x^2 + qb x + qc, qa > 0 > qc, as -2 qc/(qb + sqrt(qb^2 - 4 qa qc)); intervals in, interval out."""
    return -2 * qc / (qb + iv.sqrt(qb * qb - 4 * qa * qc))


def m_of(lam):
    return I(BETA) * (1 - lam) / (2 * I(BETA) + (1 - 2 * I(BETA)) * lam)


# ================================================================================================
hdr("0. Software")
print(f"  python {platform.python_version()} ; mpmath {mpmath.__version__} ; interval precision {iv.dps} digits")
print(f"  e in [{rnd_down(lohi(EUL)[0], 30)}, {rnd_up(lohi(EUL)[1], 30)}]")
print(f"  cap lambda_bar in [{rnd_down(lohi(CAP)[0], 25)}, {rnd_up(lohi(CAP)[1], 25)}]")

# ================================================================================================
hdr("1. Conditions on the class values and the cost (areas A and B)")
print("-- decisive advantage and affordability for the point classes")
fl = (H ** 2 - P ** 2) / (2 * H)
ceil = H - R2
print(f"  (h^2 - p^2)/(2h) = {frac(fl)} = {dec_exact(fl)} ; h - r_2 = {frac(ceil)} = {dec_exact(ceil)} ; c_H = {CH}")
add_exact("cH_DA_floor_B", fl, frac(fl), "analytical",
          "(h^2 - p^2)/(2h): the cost floor of decisive advantage for point classes and the uniform incumbent family")
add_exact("cH_afford_ceiling_B", ceil, frac(ceil), "analytical",
          "h - r_2: the cost ceiling of the affordability condition, equal to the margin by which class H outbids "
          "the strongest incumbent's top value")
add_exact("margin_decisive_B_frac", CH - fl, frac(CH - fl), "analytical", "c_H - (h^2 - p^2)/(2h) = 6 - 399/80")
add_exact("margin_unif_afford_B", ceil - CH, frac(ceil - CH), "analytical", "h - r_2 - c_H = 10 - 18/5 - 6")
# the strength above which no uniform incumbent recruits: the upper root of g_H(r) = c_H on [p, h]
f = lambda r: gH(r) - CH
br = bisect(f, Fr(4), Fr(10))
print(f"  g_H(r) = c_H on [4, 10]: g_H(4) = {rnd(gH(Fr(4)), 6)} > c_H > g_H(10) = {rnd(gH(Fr(10)), 6)} ; g_H falls on r > 1/2 "
      f"(derivative -1/2 + p^2/(2r^2) < 0), so the root is unique there: [{rnd_down(br[0], 20)}, {rnd_up(br[1], 20)}]")
rstar = 4 + iv.sqrt(I(63)) / 2
print(f"  closed form 4 + sqrt(63)/2 in [{rnd_down(lohi(rstar)[0], 20)}, {rnd_up(lohi(rstar)[1], 20)}] ; "
      f"bracket contains it: {br[0] <= lohi(rstar)[1] and lohi(rstar)[0] <= br[1]}")
add_iv("decisive_rmax_B", rstar, 6, "computer-assisted",
       "4 + sqrt(63)/2: the upper root of g_H(r) = c_H on p <= r <= h, where g_H(r) = h - r/2 - p^2/(2r) falls strictly; "
       "the strength above which no uniform incumbent of the example's class values and cost recruits")
add_iv("margin_decisive_rmax_B", I(H) - rstar, 6, "computer-assisted", "h - decisive_rmax_B: the distance of that strength below h")

print("-- the balance margins of Lemma A.10 (b) and (c): minima over the path of (g_H - c_H) - eta Delta and - 2 eta Delta")


def f1(r):
    return gH(r) - CH


def f2(r):
    """-g_H' Delta/Delta' in closed form."""
    return (r - 1) * (r * r - Fr(1, 4)) / (2 * r * (r + 1))


def f2_direct(r):
    gHp = -Fr(1, 2) + P ** 2 / (2 * r * r)
    return -gHp * Delta(r) / dDelta(r)


print("  identity check of the closed form -g_H' Delta/Delta' at four strengths:",
      [f2(r) - f2_direct(r) for r in (R0, Fr(2), R1, R2)])
b1 = f1(R2) - f2(R2)
b2 = f1(R2) - 2 * f2(R2)
print(f"  at r_2: g_H - c_H = {frac(f1(R2))} ; -g_H' Delta/Delta' = {frac(f2(R2))}")
print(f"  (b) margin = {frac(b1)} = {rnd(b1, 6)} ; (c) margin = {frac(b2)} = {rnd(b2, 6)}")
N = 2400
grid = [R0 + (R2 - R0) * i / N for i in range(N + 1)]
m1 = min(f1(r) - f2(r) for r in grid)
m2 = min(f1(r) - 2 * f2(r) for r in grid)
print(f"  smallest value on a grid of {N + 1} strengths: (b) {rnd(m1, 6)} ; (c) {rnd(m2, 6)} ; both attained at r_2: "
      f"{m1 == b1 and m2 == b2}")
print("  g_H - c_H falls for r > 1/2 and -g_H' Delta/Delta' rises for r > 1 (its derivative is positive there), so each "
      "difference falls on [r_0, r_2] and its minimum is at r_2")
add_exact("margin_balance_B_frac", b1, frac(b1), "analytical",
          "min over [r_0, r_2] of (g_H - c_H) + g_H' Delta/Delta', attained at r_2; g_H - c_H falls and -g_H' Delta/Delta' rises there")
add_exact("margin_balance_B", b1, rnd(b1, 6), "analytical", "decimal display of margin_balance_B_frac")
add_exact("margin_balance_sq_B_frac", b2, frac(b2), "analytical",
          "min over [r_0, r_2] of (g_H - c_H) + 2 g_H' Delta/Delta', attained at r_2")
add_exact("margin_balance_sq_B", b2, rnd(b2, 6), "analytical", "decimal display of margin_balance_sq_B_frac")

print("-- the translated-uniform economy of Lemma A.5: h = 10, ell = 1, p = 1/2, c_H = 2, half-width 1/10")
tw = dict(h=Fr(10), ell=Fr(1), p=Fr(1, 2), cH=Fr(2), hw=Fr(1, 10), rlo=Fr(7), rhi=Fr(15, 2))


def Jtw(r):
    return (r - tw["ell"]) * (1 - tw["cH"] / (tw["h"] - r))


Jlo, Jhi = Jtw(tw["rlo"]), Jtw(tw["rhi"])
print(f"  J(7) = {frac(Jlo)} ; J(15/2) = {frac(Jhi)}")
for key, val, disp, what in (("twonum_h", tw["h"], "10", "high-class value h of the translated-uniform economy"),
                             ("twonum_ell", tw["ell"], "1", "low-class value ell"),
                             ("twonum_p", tw["p"], "1/2", "reserve p"),
                             ("twonum_cH", tw["cH"], "2", "preparation cost c_H"),
                             ("twonum_halfwidth", tw["hw"], "1/10", "half-width of the incumbent's uniform law"),
                             ("twonum_rlo", tw["rlo"], "7", "lower centre of the incumbent law"),
                             ("twonum_rhi", tw["rhi"], "15/2", "upper centre of the incumbent law")):
    add_exact(key, val, disp, "input", "translated-uniform economy: " + what)
add_exact("twonum_Jlo", Jlo, frac(Jlo), "analytical", "(r - ell)(1 - c_H/(h - r)) at r = 7")
add_exact("twonum_Jhi", Jhi, frac(Jhi), "analytical", "(r - ell)(1 - c_H/(h - r)) at r = 15/2")

print("-- the two-interval path of Lemma A.10 (the incumbent is a mixture of two uniform laws)")
wl, hw = Fr(9, 10), Fr(1, 100)
cl0, cl1, cu0, cu1 = Fr(3, 5), Fr(49, 50), Fr(157, 100), Fr(9, 5)
for key, val, disp, what in (("twopath_weight_lower", wl, "0.9", "weight of the lower uniform law"),
                             ("twopath_halfwidth", hw, "0.01", "half-width of both uniform laws"),
                             ("twopath_lower_start", cl0, "0.6", "centre of the lower law at r = 0"),
                             ("twopath_lower_end", cl1, "0.98", "centre of the lower law on [1, 2]"),
                             ("twopath_upper_start", cu0, "1.57", "centre of the upper law on [0, 1]"),
                             ("twopath_upper_end", cu1, "1.8", "centre of the upper law at r = 2")):
    add_exact(key, val, disp, "input", "two-interval path: " + what)


def centres(r):
    cl = cl0 + (cl1 - cl0) * min(r, Fr(1))
    cu = cu0 + (cu1 - cu0) * max(r - 1, Fr(0))
    return cl, cu


def two_path(r):
    """Spread, profit gap, J and tau on the two-interval path (every lower value in (p, ell), every upper value in (ell, h))."""
    cl, cu = centres(r)
    EV = wl * cl + (1 - wl) * cu
    gl = wl * (ELL - cl)                    # class L wins only against the lower law, and earns ell - value
    gh = H - EV                             # class H wins against every value and pays it
    gam = gh - gl
    D = (H - ELL) - gam                     # spread = (h - ell) - profit gap
    t = (CH - gl) / gam
    return dict(D=D, gl=gl, gh=gh, gam=gam, tau=t, J=D * (1 - t), cl=cl, cu=cu)


print("  r = 0, 1, 2: spread, J, tau, g_L, g_H - g_L")
for r in (Fr(0), Fr(1), Fr(2)):
    T = two_path(r)
    print(f"   r = {r}: spread {frac(T['D'])} J {rnd(T['J'], 9)} tau {rnd(T['tau'], 9)} g_L {frac(T['gl'])} gamma {frac(T['gam'])}")
print(f"  J - k at r = 0 and r = 1 and r = 2: {[rnd(two_path(Fr(r))['J'] - K, 9) for r in (0, 1, 2)]}")
# first piece [0, 1]: J is linear in r; its zero k is solved exactly
f_a = lambda r: two_path(r)["J"] - K
br_a = bisect(f_a, Fr(0), Fr(1, 2))
x_lo = Fr(3137, 6498)
print(f"  first piece: J(r) - k at 3137/6498 = {frac(f_a(x_lo))} (zero exactly: {f_a(x_lo) == 0}); J falls on [0, 1] (g_L-part), "
      f"so J >= k exactly on [0, 3137/6498]; bracket of the zero [{rnd_down(br_a[0], 20)}, {rnd_up(br_a[1], 20)}]")
print(f"  spread on [0, 1] is constant: {two_path(Fr(0))['D']} = {two_path(Fr(1))['D']}")
add_exact("twopath_lo", x_lo, rnd(x_lo, 6), "analytical",
          "end of the first piece of sure purchase: on [0, 1] the spread is 57/1000 and J >= k exactly when the lower centre is "
          "at most 13397/17100, that is r <= 3137/6498; J(3137/6498) = k exactly")
# second piece [1, 2]: the spread is a linear function of r and J = D (3.018 - D)/(9 - D) there
f_b = lambda r: two_path(r)["J"] - K
Dq = lambda D: D * D - Fr(1519, 500) * D + Fr(9, 50)        # J >= k exactly when this is <= 0 (spread D > 0, gamma > 0)
print("  second piece [1, 2]: g_L = {} and J >= k exactly when D^2 - (1519/500) D + 9/50 <= 0".format(frac(two_path(Fr(3, 2))['gl'])))
chk = [two_path(r) for r in (Fr(1), Fr(3, 2), Fr(2))]
print("   J - k equals -(D^2 - (1519/500) D + 9/50)/(9 - D) at three strengths:")
for c in chk:
    print(f"    D = {frac(c['D'])}: J - k = {frac(c['J'] - K)} ; -(D^2 - (1519/500) D + 9/50)/(9 - D) = {frac(-Dq(c['D']) / (9 - c['D']))}")
root_small = (1519 - iv.sqrt(I(2127361))) / 1000
root_big = (1519 + iv.sqrt(I(2127361))) / 1000
r_hi_iv = 1 + (1000 * root_small - 57) / 23
print(f"  roots of D^2 - (1519/500) D + 9/50: {rnd(lohi(root_small)[0], 12)} and {rnd(lohi(root_big)[0], 12)} ; larger root above 2/25")
print(f"  smaller root as a spread is >= 57/1000 (the spread at r = 1): {lohi(root_small)[0] >= Fr(57, 1000)} ; "
      f"r = 1 + (1000 root - 57)/23 in [{rnd_down(lohi(r_hi_iv)[0], 20)}, {rnd_up(lohi(r_hi_iv)[1], 20)}]")
bq = bisect(f_b, Fr(1), Fr(3, 2))
print(f"  exact-sign bisection of J - k on [1, 3/2]: [{rnd_down(bq[0], 20)}, {rnd_up(bq[1], 20)}]")
print(f"  closed form (1485 - sqrt(2127361))/23 in [{rnd_down(lohi((1485 - iv.sqrt(I(2127361))) / 23)[0], 20)}, "
      f"{rnd_up(lohi((1485 - iv.sqrt(I(2127361))) / 23)[1], 20)}]")
add_root("twopath_hi", bq[0], bq[1], 6, "computer-assisted",
         "start of the second piece of sure purchase: the smaller root of J(r) = k on [1, 2], equal to (1485 - sqrt(2127361))/23; "
         "J - k changes sign from negative to positive on the bracket and the spread rises with r")
add_exact("twopath_lo_frac", x_lo, frac(x_lo), "analytical", "twopath_lo as a fraction: the strength on [0, 1] at which J = k")
add_exact("twopath_hi_c", Fr(1485), "1485", "analytical", "twopath_hi = (c - sqrt(d))/q: the constant c")
add_exact("twopath_hi_d", Fr(2127361), "2127361", "analytical", "twopath_hi = (c - sqrt(d))/q: the radicand d")
add_exact("twopath_hi_q", Fr(23), "23", "analytical", "twopath_hi = (c - sqrt(d))/q: the denominator q")
D_r0_ell = R0 / 2 - ELL + 3 * ELL ** 2 / (2 * R0)
print(f"  spread at r_0 with point values and the reserve at ell: r_0/2 - ell + 3 ell^2/(2 r_0) = {frac(D_r0_ell)}")
add_exact("rsv_Delta_r0_at_ell", D_r0_ell, frac(D_r0_ell), "analytical",
          "Delta(r_0) with point values at the reserve p = ell: r_0/2 - p + 3 p^2/(2 r_0) at p = 1")

# ================================================================================================
hdr("2. Takeover shares (area A)")
eH_cap = I(RHO) + I(1 - RHO) * (I(BETA) + (1 - I(BETA)) * CAP)
eL_cap = I(RHO) + I(1 - RHO) * I(BETA) * (1 - CAP)
pi_ = Fr(1, 2)
s0 = pi_ * RHO / (pi_ * RHO + (1 - pi_) * RHO * ELL / R0)
s1 = eH_cap / (eH_cap + eL_cap * I(ELL / R1))
s2 = RHO / (RHO + RHO * ELL / R2)
closed1 = (3 + (12 * EUL - 3) * I(BETA)) / (4 + (13 * EUL - 1) * I(BETA))
print(f"  share at r_0: {frac(s0)} ; at r_2: {frac(s2)} ; at r_1: e_H/(e_H + e_L/3) in [{rnd_down(lohi(s1)[0], 20)}, {rnd_up(lohi(s1)[1], 20)}]")
print(f"  closed form [3 + (12e - 3) beta]/[4 + (13e - 1) beta] minus the share at r_1: {rnd(lohi(closed1 - s1)[0], 40)} .. {rnd(lohi(closed1 - s1)[1], 40)}")
add_exact("share_H_r0", s0, rnd(s0, 6), "analytical",
          "class H's share of challenger acquisitions at r_0: pi rho/[pi rho + (1 - pi) rho ell/r_0] = 6/11 (no research, entry rho in both classes, W_H = 1, W_L = ell/r_0)")
add_iv("share_H_r1_B", s1, 6, "computer-assisted",
       "pi e_H/[pi e_H + (1 - pi) e_L ell/r_1] with e_H = rho + (1 - rho)(b + lambda), e_L = rho + (1 - rho) b at the slot; "
       "equals [3 + (12e - 3) beta]/[4 + (13e - 1) beta]")
add_exact("share_H_r2_B", s2, rnd(s2, 6), "analytical",
          "class H's share at r_2: entry rho in both classes, W_H = 1, W_L = ell/r_2; 1/(1 + 5/18) = 18/23")

# ================================================================================================
hdr("3. Winners, covariance, volume and reserve (area D)")
bet, e_ = I(BETA), EUL
den = 1 + (e_ - 1) * bet
wtest = bet * (11 + 27 * e_) / (64 * den)
cov_class = (e_ - 1) * bet / (12 * den)
cov_rec = bet * (1 + 3 * e_) / (8 * den)
wsec = (1 + 3 * e_) / (4 * (1 + e_))
print(f"  weighted impact difference: closed form in [{rnd_down(lohi(wtest)[0], 25)}, {rnd_up(lohi(wtest)[1], 25)}]")
add_iv("wtest_r1_B", wtest, 6, "computer-assisted",
       "frequency-weighted impact difference E[P(X)] - P(0) at r_1: (1 - rho)(b + lambda/2) w_3(M) = beta (11 + 27e)/(64 [1 + (e - 1) beta])")
add_iv("cov_win_class_r1_B", cov_class, 6, "computer-assisted",
       "class component of Cov(X, 1_W) at r_1: rho lambda Omega(F_{r_1})/2 = lambda/12 = (e - 1) beta/(12 [1 + (e - 1) beta])")
add_iv("cov_win_recruit_r1_B", cov_rec, 6, "computer-assisted",
       "entry component of Cov(X, 1_W) at r_1: (1 - rho)(b + lambda/2) W_{F_3}(M) = beta (1 + 3e)/(8 [1 + (e - 1) beta])")
add_iv("wsecond_r1_B", wsec, 6, "computer-assisted",
       "(1 - rho) W_{F_3}(M) = (1 + 3e)/(4 (1 + e)): the winning probability of the second purchaser at r_1")
add_exact("margin_reserve_unif_B", ELL ** 2 - 3 * P ** 2, frac(ELL ** 2 - 3 * P ** 2), "analytical", "ell^2 - 3 p^2 = 1 - 3/4")
add_exact("margin_winsep_r1_B", ELL / R1, frac(ELL / R1), "analytical", "D(r_1) - Omega(F_{r_1}) = ell/r_1, with D = 1 on [ell, h) and Omega = 1 - ell/r")
add_exact("margin_winsep_r2_B", ELL / R2, frac(ELL / R2), "analytical", "D(r_2) - Omega(F_{r_2}) = ell/r_2 = 5/18")
v = bet * (1 + e_) / den
vol_max = Fr(200, 259)
add_exact("vol_band_max_frac", vol_max, frac(vol_max), "analytical",
          "the largest volume at which every ratio u' above 82/59 meets 3 v <= 2 + u'(1 - v): 200/259")
add_iv("margin_vol_band_B", I(vol_max) - v, 6, "computer-assisted", "200/259 - v, with v = beta (1 + e)/(1 + (e - 1) beta) the volume at the slot")

# ================================================================================================
hdr("4. Recruiting research: the start, the cap, class entry, the exact margin at r_0 (area C)")
phi0 = phi_a(R0)
lam_E0 = L(tau(R0))
print(f"  J(6/5) = {frac(J(R0))} ; tau(6/5) = {frac(tau(R0))} ; lambda_E(6/5) = {frac(lam_E0)}")
print(f"  phi_a(r_0) = {frac(phi0)} = {rnd(phi0, 12)}")
add_exact("res_phi_r0_frac", phi0, frac(phi0), "analytical", "J(r_0) - k - 2 a lambda_E(r_0) at a = 1/40, an exact rational")
add_exact("res_phi_r0", phi0, rnd(phi0, 6), "analytical", "decimal display of res_phi_r0_frac")
add_exact("margin_res_phi_r0_B", -phi0, rnd(-phi0, 6), "analytical",
          "-phi_a(r_0): the margin of the cheap-research condition phi_a(r_0) < 0, an exact rational")
j74 = J(Fr(7, 4))
print(f"  J(7/4) = {frac(j74)} ; rho J(7/4) = {rnd(RHO * j74, 9)} < k : {RHO * j74 < K}")
add_exact("res_J74_frac", j74, frac(j74), "analytical", "J(7/4) = Delta(7/4) (1 - tau(7/4)) = (9/56)(19/55)")
add_exact("res_bound_strength", Fr(7, 4), "7/4", "input", "right endpoint of the rational derivative bound on the recruitment margin")
add_exact("margin_rho2Delta_r1_B_frac", RHO * RHO * Delta(R1) - K, frac(RHO * RHO * Delta(R1) - K), "analytical", "rho^2 Delta_T(r_1) - k = 1/24 - 1/50 (Lemma on the order of the marked strengths)")
add_exact("res_beta_upper", Fr(1, 3), "1/3", "input", "upper end of the stated sufficient interval for the liquidity share")
add_exact("str_r200", Fr(2), "2", "input", "strength 2 (the threshold pair under an abstaining investor)")

kink = (1 - RHO) * K / (2 * A0 * RHO)
print(f"  kink research (1 - rho) k/(2 a rho) = {frac(kink)} > 1 > cap: the research root is on the abstain-or-mix piece")
Dcap = (2 * I(A0) * CAP + I(K)) / m_CAP
rcap = fr_root(Dcap)
bcap = out_bracket(rcap)
print(f"  cap spread (2 a cap + k)(1 + e) in [{rnd_down(lohi(Dcap)[0], 20)}, {rnd_up(lohi(Dcap)[1], 20)}] ; "
      f"r_cap in [{rnd_down(lohi(rcap)[0], 20)}, {rnd_up(lohi(rcap)[1], 20)}] ; below 7/4: {bcap[1] < Fr(7, 4)}")
print(f"  phi_a rises on [6/5, 7/4] at a = 1/40 (derivative bound 0.033767 > 0, registry res_phip_lb), so the value at r_cap is the "
      f"interval between the values at the ends of its bracket")
phi_cap = span(phi_a(bcap[0]), phi_a(bcap[1]))
add_iv("res_phi_rcap", phi_cap, 6, "computer-assisted",
       "recruitment margin J - k - 2 a lambda_E at the strength where research reaches the cap, Delta(r) = (2 a cap + k)(1 + e); phi_a rises on [6/5, 7/4]")
# the start of the recruiting branch
brR = bisect(lambda r: phi_a(r), R0, Fr(7, 4))
print(f"  r_R, the zero of phi_a on [6/5, 7/4]: [{rnd_down(brR[0], 25)}, {rnd_up(brR[1], 25)}] "
      f"(phi_a(6/5) = {rnd(phi_a(R0), 6)} < 0 < phi_a(7/4) = {rnd(phi_a(Fr(7, 4)), 6)})")
lamR_start = span(L(tau(brR[0])), L(tau(brR[1])))


def class_entry(lam):
    eH = I(RHO) + I(1 - RHO) * (I(BETA) + (1 - I(BETA)) * lam)
    eL = I(RHO) + I(1 - RHO) * I(BETA) * (1 - lam)
    return eH, eL


def research_root(r):
    """The research of recruiting research at r below the cap: root of 2 a lambda = Delta m_lambda - k on the abstain-or-mix piece."""
    D = I(Delta(r))
    qa = 2 * I(A0) * (1 - 2 * I(BETA))
    qb = 4 * I(A0) * I(BETA) + I(K) * (1 - 2 * I(BETA)) + I(BETA) * D
    qc = I(BETA) * (2 * I(K) - D)
    lam = quad_root(qa, qb, qc)
    pos = I(RHO) * D * m_of(lam) - I(K)
    return lam, lohi(pos)[1] <= 0, lohi(lam)[1] < lohi(CAP)[0]


print("-- class entry in recruiting research below the cap, at the start and at the cap")
ent_rows = []
for tag, r in (("r155", Fr(31, 20)), ("r160", Fr(8, 5)), ("r165", Fr(33, 20))):
    lam, piece_ok, below_cap = research_root(r)
    ent_rows.append((tag, f"r = {r}", lam, piece_ok, below_cap))
ent_rows.append(("rR", "r_R", lamR_start, True, True))
ent_rows.append(("cap", "the cap (research lambda_bar, every strength from r_cap to r_C, in particular r_1 = 3)", CAP, True, True))
for tag, what, lam, piece_ok, below_cap in ent_rows:
    eH, eL = class_entry(lam)
    print(f"  {what}: lambda in [{rnd_down(lohi(lam)[0], 15)}, {rnd_up(lohi(lam)[1], 15)}] abstain-or-mix piece valid: {piece_ok} ; below cap: {below_cap if tag != 'cap' else 'it is the cap'}")
    base = "class-{} entry rho + (1 - rho)[{}] at {}"
    wh = "recruiting research at r = " + {"r155": "31/20", "r160": "8/5", "r165": "33/20"}.get(tag, "") if tag in ("r155", "r160", "r165") else (
        "the start r_R of the recruiting branch" if tag == "rR" else "the cap (r_cap <= r <= r_C, in particular r_1)")
    add_iv(f"res_eH_{tag}", eH, 6, "computer-assisted", f"class-H entry rho + (1 - rho)[beta + (1 - beta) lambda] in recruiting research at {wh}")
    add_iv(f"res_eL_{tag}", eL, 6, "computer-assisted", f"class-L entry rho + (1 - rho) beta (1 - lambda) in recruiting research at {wh}")
print("  entry at r_0 and at r_2 is rho in both classes (zero research; floor-entry research at the cap): rows entry_r0, entry_r2 exist")

# the research of recruiting research at the three strengths against the registry
REG = {}
try:
    with open(REG_PATH, newline="") as fh:
        for row in csv.DictReader(fh):
            REG[row["key"]] = row["display"]
except OSError as exc:
    print(f"registry not readable: {exc}")


def beside(key, x, nd=6):
    lo, hi = lohi(x)
    mine = rnd(lo, nd) if rnd(lo, nd) == rnd(hi, nd) else f"[{rnd(lo, nd)}, {rnd(hi, nd)}]"
    disp = REG.get(key, "(absent)")
    print(f"  {key:<24} here {mine:<22} table display {disp:<12} {'same' if mine == disp else 'DIFFERENT'}")


print("-- the same quantities beside the existing rows")
for tag, key_l in (("r155", "res_lambda_r155"), ("r160", "res_lambda_r160"), ("r165", "res_lambda_r165"), ("rR", "res_lambda_rR")):
    lam = [x for x in ent_rows if x[0] == tag][0][2]
    beside(key_l, lam)
    eH, eL = class_entry(lam)
    if tag != "rR":
        beside("res_entry_" + tag, (eH + eL) / 2)
        beside("res_own_" + tag, eH / 2)
    else:
        beside("res_entry_rR", (eH + eL) / 2)
beside("res_entry_cap", (class_entry(CAP)[0] + class_entry(CAP)[1]) / 2)
beside("res_rcap", rcap)
beside("res_rR", span(brR[0], brR[1]))
beside("res_dR_r1", wtest)
beside("p2_access_proceeds_gain", wtest)
beside("cov_win_r1_B", cov_class + cov_rec)

print("-- the cap-based identities the notes quote")
print(f"  class-H entry at the cap {rnd(lohi(class_entry(CAP)[0])[0], 6)}, class-L {rnd(lohi(class_entry(CAP)[1])[0], 6)}; sum/2 = entry")

# ------------------------------------------------------------------------------------------------
print("-- the threshold pair at r = 2 when an indifferent investor abstains (area C)")
t2 = tau(Fr(2))
lE2 = L(t2)
J2 = J(Fr(2))
es = (2 * A0 * lE2 + K - max(RHO * J2 - K, Fr(0))) / J2
ent2 = RHO + (es - RHO) * (BETA + (Fr(1, 2) - BETA) * lE2)
print(f"  tau(2) = {frac(t2)} ; lambda_E(2) = {frac(lE2)} ; e* = {frac(es)} ; entry {frac(ent2)}")
add_exact("res_I0CM_lambda_r200", lE2, rnd(lE2, 6), "analytical", "lambda_E(2) = L(tau(2)) with tau(2) = 93/140")
add_exact("res_I0CM_e1_r200", es, rnd(es, 6), "analytical",
          "entry after a purchase in the threshold pair at r = 2: [2 a lambda_E + k - (rho J - k)^+]/J, with J(2) = 47/560")
add_exact("res_I0CM_entry_r200", ent2, rnd(ent2, 6), "analytical", "rho + (e* - rho)[beta + (1/2 - beta) lambda_E] at r = 2")

# ================================================================================================
hdr("5. Floor-entry research: its end r_Q (area C, proof of the floor margin)")
print("-- the derivative bound of the floor margin on the 24 pieces of width 1/10 that partition [6/5, 18/5]")
pieces = []
l = R0
while l < R2:
    pieces.append((l, l + Fr(1, 10)))
    l += Fr(1, 10)
bs = [b_piece(a, b) for a, b in pieces]
bmin = min(bs)
print(f"  pieces: {len(pieces)} ; last right end is r_2: {pieces[-1][1] == R2} ; smallest bound {bmin.numerator}/{bmin.denominator} = {rnd(bmin, 9)} "
      f"on [{frac(pieces[bs.index(bmin)][0])}, {frac(pieces[bs.index(bmin)][1])}] ; at least 1/100: {bmin >= Fr(1, 100)}")
add_exact("res_floor_step", Fr(1, 10), "1/10", "input", "width of each rational piece in the lower bound on the floor margin's derivative")
add_exact("res_floor_dphi_lb", Fr(1, 100), "1/100", "analytical",
          "lower bound on the derivative of the floor margin rho J - k - a lambda_E over [r_0, r_2]: every piece bound is at least 1/100")
add_exact("margin_res_floor_slope_B", bmin, rnd(bmin, 6), "analytical", "smallest of the 24 piece bounds on the floor margin's derivative")
print("-- the zero r_Q")
fq = lambda r: phi_rho(r)
for r in (Fr(7, 4), Fr(2), Fr(11, 5), Fr(5, 2)):
    print(f"   phi_rho({r}) = {rnd(fq(r), 9)}")
brQ = bisect(fq, Fr(7, 4), Fr(5, 2))
print(f"  r_Q in [{rnd_down(brQ[0], 25)}, {rnd_up(brQ[1], 25)}]")
add_root("res_rQ", brQ[0], brQ[1], 6, "computer-assisted",
         "r_Q: the zero of the floor margin rho Delta (1 - tau) - k - a lambda_E on [r_0, r_2]; the margin is negative at 7/4 and positive at 5/2 and "
         "rises strictly (derivative at least 1/100 on every piece), so the zero is unique")
lamQ = span(L(tau(brQ[0])), L(tau(brQ[1])))
tauQ = span(tau(brQ[0]), tau(brQ[1]))
add_iv("res_lambda_floor_rQ", lamQ, 6, "computer-assisted",
       "lambda_E(r_Q): floor-entry research at r_Q, equal to lambda_Q(Delta(r_Q)) because the floor margin vanishes there; lambda_E rises with r")
add_iv("res_tau_rQ", tauQ, 6, "computer-assisted", "tau(r_Q): the threshold at the end of floor-entry research; tau rises with r")
# the floor research is the root of a lambda = rho Delta m_lambda - k at Delta(r_Q); check by the quadratic
D_Q = span(Delta(brQ[0]), Delta(brQ[1]))
qa = I(A0) * (1 - 2 * I(BETA))
qb = I(RHO) * D_Q * I(BETA) + I(K) * (1 - 2 * I(BETA)) + 2 * I(A0) * I(BETA)
qc = I(BETA) * (2 * I(K) - I(RHO) * D_Q)
lq = quad_root(qa, qb, qc)
print(f"  lambda_Q(Delta(r_Q)) from the quadratic formula in [{rnd_down(lohi(lq)[0], 20)}, {rnd_up(lohi(lq)[1], 20)}] ; "
      f"lambda_E(r_Q) in [{rnd_down(lohi(lamQ)[0], 20)}, {rnd_up(lohi(lamQ)[1], 20)}]")
print(f"  floor research at r_Q below the cap: {lohi(lamQ)[1] < lohi(CAP)[0]}")
print("-- the margins of the floor-margin conditions r_N < r_Q < r_U and lambda_E(r_Q) < lambda_bar")
rQ_iv = span(brQ[0], brQ[1])
rN_iv = fr_root(I(2 * K / RHO))
rU_iv = fr_root((I(K) + I(A0) * CAP) * (1 + EUL) / I(RHO))
print(f"  r_N in [{rnd_down(lohi(rN_iv)[0], 20)}, {rnd_up(lohi(rN_iv)[1], 20)}] ; r_U in [{rnd_down(lohi(rU_iv)[0], 20)}, {rnd_up(lohi(rU_iv)[1], 20)}]")
add_iv("margin_res_rQ_rN_B", rQ_iv - rN_iv, 6, "computer-assisted",
       "r_Q - r_N, with r_N = fr(2k/rho) the strength at which rho Delta = 2k")
add_iv("margin_res_rU_rQ_B", rU_iv - rQ_iv, 6, "computer-assisted",
       "r_U - r_Q, with r_U = fr((k + a lambda_bar)(1 + e)/rho) the strength at which floor-entry research reaches the cap")
add_iv("margin_res_cap_lamQ_B", CAP - lamQ, 6, "computer-assisted",
       "lambda_bar - lambda_E(r_Q): floor-entry research at r_Q lies below the cap")

# ================================================================================================
hdr("6. The pooling strength (area A, constructed tuples)")
Dp = I(K / RHO) * (2 + (e_ - 1) * I(BETA) / I(1 - BETA))
rp = I(ELL) + Dp + iv.sqrt(Dp * Dp + 2 * Dp)
print(f"  pooling spread in [{rnd_down(lohi(Dp)[0], 20)}, {rnd_up(lohi(Dp)[1], 20)}] ; r in [{rnd_down(lohi(rp)[0], 20)}, {rnd_up(lohi(rp)[1], 20)}]")
D_chk = (rp - 1) ** 2 / (2 * rp)
print(f"  Delta(r) from the closed form minus the spread: {rnd(lohi(D_chk - Dp)[0], 40)} .. {rnd(lohi(D_chk - Dp)[1], 40)}")
mu_p = I(K) / (I(RHO) * Dp)
t0p = I(P) * (1 - I(P) / rp)
tLp = I(ELL) - I(ELL ** 2 - P ** 2) / (2 * rp)
price_p = t0p + I(RHO) * (tLp - t0p) + I(K)
add_iv("r_pool_B", rp, 6, "computer-assisted",
       "the strength at which the sale and the zero order have one posterior in recruiting research at the cap: ell + D + sqrt(D^2 + 2 ell D) "
       "with D = (k/rho)[2 + (e - 1) beta/(1 - beta)]; the sale probability rises strictly from 0 to 1 between r_N and r_S, so the strength is unique")
add_iv("pool_mu_B", mu_p, 6, "computer-assisted", "k/[rho Delta(r_pool)]: the common posterior of the sale and the zero order, at which the sale just pays k")
add_iv("pool_price_B", price_p, 6, "computer-assisted", "t_0 + rho (t_L - t_0) + k at r_pool: the common price after a sale and after no order")

# ================================================================================================
hdr("6b. Numbers of Appendix A.3 (Corollary 1 proof) and A.6 (price collision, signal examples)")
print("-- Corollary 1: spreads at r_1 and r_2 and the floor of kappa at the prior 1/2")
D1, D2 = Delta(R1), Delta(R2)
kap = K / (RHO * D1)
print(f"  Delta(r_1) = {frac(D1)} ; Delta(r_2) = {frac(D2)} ; k/(rho Delta(r_1)) = {frac(kap)}")
add_exact("a236_Delta_r1_frac", D1, frac(D1), "analytical", "Delta(r_1) = (r_1 - ell)^2/(2 r_1)")
add_exact("a236_Delta_r2_frac", D2, frac(D2), "analytical", "Delta(r_2) = (r_2 - ell)^2/(2 r_2)")
add_exact("a236_kappa_floor_frac", kap, frac(kap), "analytical", "k/(rho Delta(r_1)): the lower bound on kappa(pi) = min{m, 1 - M} in the trading hypothesis at r_1")

print("-- price collision at three classes (declared primitives)")
pool = (("cH", Fr(10), "10", "preparation cost"), ("h", Fr(10), "10", "high class value"),
        ("k", Fr(1, 8), "1/8", "trading cost"), ("p", Fr(1), "1", "reserve, also the value of class 1"),
        ("perturb", Fr(1, 1000), frac(Fr(1, 1000)), "size of the perturbation of the class-2 weight that separates the two prices"),
        ("pi1", Fr(1, 4), "1/4", "prior of class 1"), ("pi2", Fr(1, 2), "1/2", "prior of class 2"),
        ("pi3", Fr(1, 4), "1/4", "prior of class 3"), ("r", Fr(8), "8", "upper end of the uniform incumbent law"),
        ("rho", Fr(1, 4), "1/4", "probability of the zero preparation cost"))
for nm, val, disp, what in pool:
    add_exact("a236_pool_" + nm, val, disp, "input", "three-class price collision: " + what)
g3 = Fr(10) - (Fr(8) / 2 + Fr(1) / (2 * 8))
print(f"  g_3 = h - t_3 = {frac(g3)} < c_H = 10: {g3 < 10} ; priors sum to {Fr(1, 4) + Fr(1, 2) + Fr(1, 4)}")

print("-- the complementary-signal example with a more accurate challenger signal (lambda = 1/3, beta = 3/10)")
aI, aC = Fr(7, 10), Fr(3, 4)
lam_s, bet_s = Fr(1, 3), Fr(3, 10)
b_s = bet_s * (1 - lam_s)
M_s = (b_s + lam_s) / (2 * b_s + lam_s)
m_s = b_s / (2 * b_s + lam_s)
MI = (1 - aI) + (2 * aI - 1) * M_s
mI = (1 - aI) + (2 * aI - 1) * m_s
print(f"  b = {frac(b_s)} ; M = {frac(M_s)} ; m = {frac(m_s)} ; M^I = {frac(MI)} ; m^I = {frac(mI)}")
rho_s, cH_s, k_s, r0_s, r1_s = Fr(17, 20), Fr(357, 50), Fr(3, 200), Fr(11, 10), Fr(23, 10)


def muC(mu, plus):
    num = aC * mu if plus else (1 - aC) * mu
    den = aC * mu + (1 - aC) * (1 - mu) if plus else (1 - aC) * mu + aC * (1 - mu)
    return num / den


def Bmu(r, mu):
    return gL(r) + mu * (gH(r) - gL(r))


def tH(r):
    return r / 2 + P ** 2 / (2 * r)


def t0(r):
    return P * (1 - P / r)


alt_private = cH_s - Bmu(r0_s, aC)
alt_joint = Bmu(r1_s, muC(MI, True)) - cH_s
DPbar0 = Delta(r0_s) + (1 - rho_s) * (2 * aC - 1) * (tH(r0_s) - t0(r0_s))
alt_weak = k_s - (2 * aI - 1) * DPbar0
alt_strong = (2 * aI - 1) * rho_s * m_s * Delta(r1_s) - k_s
alt_other = cH_s - Bmu(r1_s, muC(MI, False))
for key, val, what in (("a236_sig_alt_private", alt_private, "c_H - B_{r_0}(alpha_C): the challenger's private signal alone does not recruit at r_0"),
                       ("a236_sig_alt_joint", alt_joint, "B_{r_1}(mu^C_+(M^I)) - c_H: a purchase with the favourable challenger signal recruits at r_1"),
                       ("a236_sig_alt_weak", alt_weak, "k - (2 alpha_I - 1) Delta_P-bar(r_0): the weak-incumbent trading bound"),
                       ("a236_sig_alt_strong", alt_strong, "(2 alpha_I - 1) rho m Delta(r_1) - k: the strong-incumbent trading bound"),
                       ("a236_sig_alt_other", alt_other, "c_H - B_{r_1}(mu^C_-(M^I)): the unfavourable challenger signal does not recruit at r_1")):
    print(f"  {key} = {frac(val)} = {rnd(val, 9)}")
    add_exact(key, val, rnd(val, 6), "analytical", what + " (point classes, uniform incumbents, signal example with rho = 17/20, c_H = 357/50, k = 3/200, r_0 = 11/10, r_1 = 23/10)")
add_exact("a236_sig_lambda", lam_s, frac(lam_s), "input", "presence probability of the signal example with the more accurate challenger signal")
add_exact("a236_sig_beta", bet_s, frac(bet_s), "input", "liquidity share of that signal example")
add_exact("a236_sig_M", M_s, frac(M_s), "analytical", "M(1/2) = (b + lambda)/(2b + lambda), b = beta(1 - lambda)")
add_exact("a236_sig_m", m_s, frac(m_s), "analytical", "m(1/2) = b/(2b + lambda), b = beta(1 - lambda)")

print("-- the example with the signal example's accuracies (rho = 1/4, c_H = 6, k = 1/50, r_0 = 6/5, r_1 = 3)")
zp_r0 = 1                                          # zeta_+ = 1, zeta_- = 0 at r_0
eH = RHO + (1 - RHO) * aC
eL = RHO + (1 - RHO) * (1 - aC)
wH = lambda r: tH(r) - t0(r)
DP0 = eL * Delta(R0) + (eH - eL) * wH(R0)
DP1 = eL * Delta(R1) + (eH - eL) * wH(R1)
rate0 = (2 * aI - 1) * DP0 / K - 2
rate1 = (2 * aI - 1) * RHO * Delta(R1) / K - 2
nu_sale = K / ((2 * aI - 1) * RHO * Delta(R1))
mu_sale = (1 - aI) + (2 * aI - 1) * nu_sale
tau1 = tau(R1)
# S_C = + recruits after a sale exactly when mu^C_+(mu) >= tau(r_1), i.e. mu >= tau/(tau + (1 - tau) alpha_C/(1 - alpha_C)) ... solved directly
pub_cut = tau1 * (1 - aC) / (tau1 * (1 - aC) + (1 - tau1) * aC)
nu_cut = (pub_cut - (1 - aI)) / (2 * aI - 1)
sale_cut = (1 / nu_cut - 2)                         # nu = b/(2b + s) >= nu_cut  <=>  s/b <= 1/nu_cut - 2
sale_floor = (2 * aI - 1) * RHO * Delta(R1) * nu_cut
print(f"  e_H = {frac(eH)} ; e_L = {frac(eL)} ; Delta_P(r_0) = {frac(DP0)} ; Delta_P(r_1) = {frac(DP1)}")
print(f"  zero-profit rates: s/b = {frac(rate0)} at r_0 ; {frac(rate1)} at r_1 ; sale posterior nu = {frac(nu_sale)}, mu(-1) = {frac(mu_sale)}")
print(f"  tau(r_1) = {frac(tau1)} ; public cutoff {frac(pub_cut)} ; sale rate cutoff s/b <= {frac(sale_cut)} ; return at the cutoff {frac(sale_floor)} ; minus k {frac(sale_floor - K)}")
print(f"  mu^C_+(cutoff) = {frac(muC(pub_cut, True))} equals tau(r_1): {muC(pub_cut, True) == tau1}")
add_exact("a236_sig_eH", eH, frac(eH), "analytical", "class-H entry rho + (1 - rho) alpha_C when zeta_+ = 1 and zeta_- = 0, at rho = 1/4, alpha_C = 3/4")
add_exact("a236_sig_eL", eL, frac(eL), "analytical", "class-L entry rho + (1 - rho)(1 - alpha_C) when zeta_+ = 1 and zeta_- = 0")
add_exact("a236_sig_DP0", DP0, frac(DP0), "analytical", "Delta_P = e_L Delta(r_0) + (e_H - e_L)(t_H - t_0) at r_0 with e_H = 13/16, e_L = 7/16")
add_exact("a236_sig_DP1", DP1, frac(DP1), "analytical", "Delta_P at r_1 with e_H = 13/16, e_L = 7/16")
add_exact("a236_sig_rate0", rate0, frac(rate0), "analytical", "zero-profit rate s_+/b = s_-/b at r_0: (2 alpha_I - 1) Delta_P(r_0)/k - 2; each correct gross return falls strictly in its rate")
add_exact("a236_sig_rate1", rate1, frac(rate1), "analytical", "zero-profit sale rate s_-/b at r_1: (2 alpha_I - 1) rho Delta(r_1)/k - 2")
add_exact("a236_sig_sale_mu", mu_sale, frac(mu_sale), "analytical", "public belief after a sale at the zero-profit rate: (1 - alpha_I) + (2 alpha_I - 1) k/[(2 alpha_I - 1) rho Delta(r_1)]")
add_exact("a236_sig_public_cutoff", pub_cut, frac(pub_cut), "analytical", "the public belief at which a challenger with S_C = + is indifferent: mu^C_+(mu) = tau(r_1) = 141/200")
add_exact("a236_sig_sale_cutoff", sale_cut, frac(sale_cut), "analytical", "S_C = + recruits after a sale exactly when s_-/b is at most this value")
add_exact("a236_sig_sale_floor", sale_floor, frac(sale_floor), "analytical", "sale return (2 alpha_I - 1) rho Delta(r_1) nu at the cutoff posterior; it exceeds k")

print("-- beside the existing rows that name the same quantities (the rows that depend on the slot, margin_p4_signal_s_joint, _strong and _other_pair, "
      "belong to the slot of the example and differ from the lambda = 1/3, beta = 3/10 values)")
for key, val in (("margin_p4_signal_s_private", alt_private), ("margin_p4_signal_s_weak", alt_weak),
                 ("p4_b_signal_r0_buy_eh", eH), ("p4_b_signal_r0_buy_el", eL), ("p4_b_signal_r1_sell_mu", mu_sale),
                 ("margin_p4_b_strong_sale_public_gap", pub_cut - mu_sale), ("margin_p4_b_strong_threshold_floor_return", sale_floor - K)):
    print(f"  {key:<44} here {rnd(val, 9):<14} table display {REG.get(key, '(absent)')}")

# ================================================================================================
hdr("7. The rows beside the display of existing rows (readings)")
beside("margin_res_half_B", I(Fr(287, 240)))
beside("res_rcap", rcap)

# ------------------------------------------------------------------------------------------------
hdr("8. Output")
seen = set()
for r in ROWS:
    if r["key"] in seen:
        raise SystemExit("duplicate key " + r["key"])
    seen.add(r["key"])
with OUT.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    for r in ROWS:
        w.writerow(r)
digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
print(f"  wrote {OUT.relative_to(ROOT)} with {len(ROWS)} rows")
print(f"  sha256 {digest}")
