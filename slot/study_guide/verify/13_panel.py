"""Chapter 13 (panel preparation): recompute the numbers that the chapter adds.

Every other number in chapter 13 is a registry value or a number that chapters 01-12
derive. Exact fractions for rational quantities; mpmath at 50 digits for quantities
that depend on Euler's number (the benchmark slot has 1 + u = e). The script prints;
it checks nothing by assertion.
"""
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50


def show(x, places=6):
    """Format a Fraction or an mpmath value to a fixed number of places."""
    return f"{float(x):.{places}f}"


# Benchmark primitives.
h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, cH, k, pi = Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)
beta = mp.mpf("0.294655")
u = mp.e - 1
lam = u * beta / (1 + u * beta)
b = (1 - lam) * beta
M = (1 + u) / (2 + u)          # top posterior at the prior 1/2
m = 1 - M                      # bottom posterior at the prior 1/2


def payoffs(r):
    """Equation (6) of the paper: t0, tH, tL, gH, gL, Delta for R ~ U[0, r]."""
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    return t0, tH, tL, gH, gL, tH - tL


def B(r, mu):
    t0, tH, tL, gH, gL, D = payoffs(r)
    return gL + mu * (gH - gL)


print("=" * 78)
print("1. The trading-cost window (H2) at the benchmark")
print("=" * 78)
D0 = payoffs(r0)[5]
D1 = payoffs(r1)[5]
upper = rho * m * mp.mpf(D1.numerator) / D1.denominator   # rho kappa Delta1, kappa = m at pi = 1/2
print(f"  lower end Delta(r0) = {D0} = {show(D0)}")
print(f"  upper end rho kappa Delta(r1) = 1/(6(1+e)) = {show(upper)}")
print(f"  ratio of the ends = 10/(1+e) = {show(upper / (mp.mpf(1) / 60))} (about {float(upper * 60):.2f})")

print()
print("=" * 78)
print("2. The slot band for parts (i) and (ii) alone, (H1) and (H2): 82/59 < u < 19/3")
print("=" * 78)
u_lo, u_ii = Fr(82, 59), Fr(19, 3)
print(f"  u range: ({show(u_lo)}, {show(u_ii)})")
print(f"  top posterior range: ({Fr(141, 200)}, {(1 + u_ii) / (2 + u_ii)}) = "
      f"({show(Fr(141, 200))}, {show((1 + u_ii) / (2 + u_ii))})")
lam_ii_hi = mp.mpf(19) * beta / (3 + 19 * beta)
lam_lo = mp.mpf(82) * beta / (59 + 82 * beta)
print(f"  presence range at beta = 0.294655: ({show(lam_lo)}, {show(lam_ii_hi)})")
u_hi = Fr(2686, 1559)
pos = (u - mp.mpf(82) / 59) / (mp.mpf(2686) / 1559 - mp.mpf(82) / 59)
print(f"  full band (H1)-(H3): ({show(u_lo)}, {show(u_hi)}); benchmark u = {show(u)}")
print(f"  share of the full band below the benchmark u = {show(pos)} (about {float(pos) * 100:.1f} percent)")

print()
print("=" * 78)
print("3. Sizes of the main comparison (r0 against r1)")
print("=" * 78)
B0 = B(r0, pi)
B1 = B(r1, pi)
fall = (B0 - B1) / B0
print(f"  gross profit at the prior: {B0} -> {B1}; fall {B0 - B1} = {fall} of B(r0) "
      f"= {show(fall)} (about {float(fall) * 100:.1f} percent)")
print(f"  spread: {D0} -> {D1}; ratio {D1 / D0}")
E0 = rho
E1 = rho + (1 - rho) * (b + pi * lam)
print(f"  entry: {show(E0)} -> {show(E1)}; ratio {show(E1 / E0)} (about {float(E1 / E0):.2f}); "
      f"rise {show(E1 - E0)}")
eH = rho + (1 - rho) * (b + lam)
O0 = pi * rho
O1 = pi * eH
print(f"  high-class ownership: {show(O0)} -> {show(O1)}; rise {show(O1 - O0)} "
      f"(about {float(O1 - O0) * 100:.0f} percentage points)")

print()
print("=" * 78)
print("4. Where r2 sits relative to the entry ceiling")
print("=" * 78)
# r_C solves M r^2 - 2(M h - cH) r - [(1-M) ell^2 - p^2] = 0 (chapter 06).
A = M * h - cH
C = (1 - M) * ell * ell - p * p
rC = (A + mp.sqrt(A * A + M * C)) / M
print(f"  r_C = {show(rC)}; r2 - r_C = {show(mp.mpf(18) / 5 - rC)}")
print(f"  c_H - B_r2(M) = {show(cH - (B(r2, 0) + M * (B(r2, 1) - B(r2, 0))))}")
for r in (Fr(37, 10), Fr(4), Fr(5)):
    margin = cH - (B(r, 0) + M * (B(r, 1) - B(r, 0)))
    print(f"  at r = {r} = {float(r):.1f}: c_H - B_r(M) = {show(margin)}")
