#!/usr/bin/env python3
"""Class H's takeover share in the three economies of the example.

The example: the incumbent's value is uniform on [0, r]; the class values are h = 10 and ell = 1; the
reserve is p = 1/2; the preparation cost is zero with probability rho = 1/4 and c_H = 6 otherwise; the
trading cost is k = 1/50; the prior is pi = 1/2; the liquidity share is beta = 294655/10^6, and the slot
has 1 + u = e, so lambda = u beta/(1 + u beta) and b = (1 - lambda) beta. The strengths are
r_0 = 6/5, r_1 = 3 and r_2 = 18/5.

A prepared challenger with value v >= p beats the incumbent U[0, r] with probability min(v/r, 1). In the
unique outcomes of Proposition 2, entry by class is (rho, rho) at r_0 and at r_2, and
(rho + (1 - rho)(b + lambda), rho + (1 - rho) b) at r_1. Ownership by class j is pi_j e_j W_j, with
pi_H = pi and pi_L = 1 - pi, and class H's takeover share is O_H / (O_H + O_L).

Quantities that involve e are closed intervals (mpmath.iv, 60 digits); the others are exact rationals.
The program prints; it checks nothing by assertion.

Usage: python3 o6_shares.py
"""

from fractions import Fraction as Fr

from mpmath import iv, mp

iv.dps = 60
mp.dps = 60

h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, c_H, k, pi = Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
beta = Fr(294655, 10**6)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)


def I(x):
    """A rational as a point interval."""
    x = Fr(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)


def show(x, digits=15):
    """An interval as [lo, hi], each end printed to the given number of significant digits, and its width."""
    lo, hi = mp.mpf(x.a.a), mp.mpf(x.b.b)
    return "[{}, {}]  width {}".format(mp.nstr(lo, digits), mp.nstr(hi, digits), mp.nstr(hi - lo, 3))


def win(v, r):
    """Probability that a prepared challenger with value v >= p beats U[0, r]."""
    return min(Fr(v) / Fr(r), Fr(1))


def share(eH, eL, WH, WL):
    oH = I(pi) * eH * WH
    oL = I(1 - pi) * eL * WL
    return oH, oL, oH / (oH + oL)


e = iv.e
u = e - 1
lam = u * I(beta) / (1 + u * I(beta))
b = (1 - lam) * I(beta)
eH1 = I(rho) + I(1 - rho) * (b + lam)
eL1 = I(rho) + I(1 - rho) * b

print("Slot")
print("  e             ", show(e))
print("  lambda        ", show(lam))
print("  b             ", show(b))
print("  b + lambda    ", show(b + lam))
print()
print("Win probabilities against U[0, r] (exact)")
for name, r in (("r_0", r0), ("r_1", r1), ("r_2", r2)):
    print("  {} = {}:  W_H = {}   W_L = {}".format(name, r, win(h, r), win(ell, r)))
print()

rows = (
    ("r_0", r0, I(rho), I(rho)),
    ("r_1", r1, eH1, eL1),
    ("r_2", r2, I(rho), I(rho)),
)
print("Entry, ownership and class H's takeover share")
for name, r, eH, eL in rows:
    WH, WL = I(win(h, r)), I(win(ell, r))
    oH, oL, s = share(eH, eL, WH, WL)
    entry = I(pi) * eH + I(1 - pi) * eL
    print("  {}".format(name))
    print("    entry in class H   ", show(eH))
    print("    entry in class L   ", show(eL))
    print("    entry              ", show(entry))
    print("    ownership, class H ", show(oH))
    print("    ownership, class L ", show(oL))
    print("    takeovers by a challenger", show(oH + oL))
    print("    class H's share    ", show(s))
print()

print("Exact values at r_0 and r_2 (entry rho in both classes, W_H = 1, W_L = ell/r)")
for name, r in (("r_0", r0), ("r_2", r2)):
    s = pi / (pi + (1 - pi) * win(ell, r))
    print("  {}: share = {} = {}   ownership, class H = {}".format(name, s, float(s), pi * rho * win(h, r)))
print()

print("Closed form at r_1 and prior 1/2: share = [3 + (12e - 3) beta] / [4 + (13e - 1) beta]")
closed = (3 + (12 * e - 3) * I(beta)) / (4 + (13 * e - 1) * I(beta))
direct = share(eH1, eL1, I(1), I(win(ell, r1)))[2]
print("  closed form   ", show(closed))
print("  direct        ", show(direct))
print("  difference    ", show(closed - direct))
print()

print("The condition of the share part, e_H W_H(F_1) W_L(F_0) - e_L W_H(F_0) W_L(F_1), at F_0 = U[0, r_0], F_1 = U[0, r_1]")
cond = eH1 * I(win(h, r1)) * I(win(ell, r0)) - eL1 * I(win(h, r0)) * I(win(ell, r1))
print("  value         ", show(cond))
print("  e_H - e_L = (1 - rho) lambda", show(eH1 - eL1))
print()

print("Decisive advantage on the uniform family with point-mass classes (exact)")
gH_at_h = (h * h - p * p) / (2 * h)
print("  (h^2 - p^2)/(2h) = {} = {}".format(gH_at_h, float(gH_at_h)))
print("  c_H - (h^2 - p^2)/(2h) = {} = {}".format(c_H - gH_at_h, float(c_H - gH_at_h)))
print("  h - r_2 = {} = {}   h - r_2 - c_H = {}".format(h - r2, float(h - r2), h - r2 - c_H))
# g_H(r) = h - r/2 - p^2/(2r) on p <= r <= h; g_H(r) = c_H gives r^2 - 2(h - c_H) r + p^2 = 0.
q = (h - c_H) ** 2 - p * p
root = mp.mpf(int(h - c_H)) + mp.sqrt(mp.mpf(q.numerator) / q.denominator)
print("  (h - c_H)^2 - p^2 = {}".format(q))
print("  root of g_H(r) = c_H in (p, h): (h - c_H) + sqrt((h - c_H)^2 - p^2) = 4 + sqrt(63)/2 =", mp.nstr(root, 20))
print("  h minus that root =", mp.nstr(mp.mpf(10) - root, 20))
gH = lambda r: h - Fr(r) / 2 - p * p / (2 * Fr(r))
print("  g_H at r_2 = {} = {}, and c_H - g_H(r_2) = {}".format(gH(r2), float(gH(r2)), float(c_H - gH(r2))))
