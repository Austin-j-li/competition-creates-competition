#!/usr/bin/env python3
"""The sale and the zero order with one posterior, in recruiting research at the cap.

The example at the prior 1/2: the incumbent's value is uniform on [0, r]; the class values are h = 10 and
ell = 1; the reserve is p = 1/2; the preparation cost is zero with probability rho = 1/4 and c_H = 6
otherwise; the trading cost is k = 1/50; the liquidity share is beta = 294655/10^6, and the slot has
1 + u = e. Research costs (a/2) lambda^2 with a = 1/40, up to the cap lambda_bar = u beta/(1 + u beta).

In recruiting research at the cap, research is lambda_bar, class H buys after a success, and class L sells
with probability z = s/lambda_bar and abstains otherwise, where s = min{lambda_bar, b_bar [rho Delta_T/k - 2]^+}
and b_bar = (1 - lambda_bar) beta. The posteriors after a sale, no order and a purchase are
b_bar/(2 b_bar + lambda_bar z), b_bar_0/(2 b_bar_0 + lambda_bar (1 - z)) and M at the cap, with
b_bar_0 = (1 - lambda_bar)(1 - 2 beta). The first two coincide exactly when z = beta/(1 - beta). The program
finds the strength at which that happens and prints the posteriors, entry and prices there and at two
other strengths.

Quantities that involve e are closed intervals (mpmath.iv, 60 digits); the others are exact rationals.
The program prints; it checks nothing by assertion.

Usage: python3 o7_pool.py
"""

from fractions import Fraction as Fr

from mpmath import iv, mp

iv.dps = 60
mp.dps = 60

h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, c_H, k = Fr(1, 4), Fr(6), Fr(1, 50)
beta = Fr(294655, 10**6)
a = Fr(1, 40)


def I(x):
    x = Fr(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)


def show(x, digits=15):
    lo, hi = mp.mpf(x.a.a), mp.mpf(x.b.b)
    return "[{}, {}]  width {}".format(mp.nstr(lo, digits), mp.nstr(hi, digits), mp.nstr(hi - lo, 3))


e = iv.e
u = e - 1
cap = u * I(beta) / (1 + u * I(beta))
bb = (1 - cap) * I(beta)
bb0 = (1 - cap) * I(1 - 2 * beta)
M_cap = (bb + cap) / (2 * bb + cap)
m_cap = 1 - M_cap


def auction(r):
    """Closed forms for the uniform incumbent on [0, r], ell <= r <= h."""
    t0 = I(p) * (1 - I(p) / r)
    tL = I(ell) - I(ell * ell - p * p) / (2 * r)
    tH = r / 2 + I(p * p) / (2 * r)
    Delta = (r - I(ell)) ** 2 / (2 * r)
    tau = (2 * r * I(c_H) - I(ell * ell - p * p)) / (2 * r * I(h) - r * r - I(ell * ell))
    return t0, tL, tH, Delta, tau


def tuple_at(r):
    t0, tL, tH, Delta, tau = auction(r)
    s = bb * (I(rho) * Delta / I(k) - 2)
    z = s / cap
    mu_m = bb / (2 * bb + cap * z)
    mu_0 = bb0 / (2 * bb0 + cap * (1 - z))
    mu_p = M_cap
    wL = tL - t0
    P = {x: t0 + ent * (wL + Delta * mu) for x, ent, mu in ((-1, I(rho), mu_m), (0, I(rho), mu_0), (1, I(1), mu_p))}
    return dict(t0=t0, tL=tL, tH=tH, Delta=Delta, tau=tau, s=s, z=z, mu=(mu_m, mu_0, mu_p), P=P)


print("Slot and research at the cap")
print("  lambda_bar     ", show(cap))
print("  b_bar          ", show(bb))
print("  b_bar_0        ", show(bb0))
print("  M at the cap   ", show(M_cap))
print("  m at the cap   ", show(m_cap))
print("  beta/(1 - beta) = {} = {}".format(beta / (1 - beta), float(beta / (1 - beta))))
print()

# z = beta/(1 - beta) means s = lambda_bar beta/(1 - beta), i.e. rho Delta/k = 2 + u beta/(1 - beta),
# because lambda_bar/(1 - lambda_bar) = u beta.
D = I(k / rho) * (2 + u * I(beta) / I(1 - beta))
r_pool = 1 + D + iv.sqrt(D * D + 2 * D)
print("The strength at which the sale and the zero order have one posterior")
print("  Delta_T there  ", show(D))
print("  r              ", show(r_pool))
T = tuple_at(r_pool)
print("  Delta_T(r) from the closed form", show(T["Delta"]))
print("  tau(r)         ", show(T["tau"]))
print("  M at the cap minus tau(r)", show(M_cap - T["tau"]))
print("  rho Delta_T - 2k (positive: class L sells with positive probability)", show(I(rho) * T["Delta"] - 2 * I(k)))
print("  k - rho Delta_T m_cap (positive: class L also abstains with positive probability)", show(I(k) - I(rho) * T["Delta"] * m_cap))
print("  sale rate s    ", show(T["s"]))
print("  z = s/lambda_bar", show(T["z"]))
print("  z - beta/(1 - beta)", show(T["z"] - I(beta / (1 - beta))))
mu_m, mu_0, mu_p = T["mu"]
print("  posterior after a sale     ", show(mu_m))
print("  posterior after no order   ", show(mu_0))
print("  their difference           ", show(mu_m - mu_0))
print("  k/(rho Delta_T), the sale posterior at which a sale pays k", show(I(k) / (I(rho) * T["Delta"])))
print("  posterior after a purchase ", show(mu_p))
print("  entry after a sale, no order, a purchase: rho, rho, 1 (posteriors below 1/2 < tau, and M at the cap above tau)")
print("  price after a sale         ", show(T["P"][-1]))
print("  price after no order       ", show(T["P"][0]))
print("  their difference           ", show(T["P"][-1] - T["P"][0]))
print("  price after a purchase     ", show(T["P"][1]))
gap = T["Delta"] * m_cap - I(k) - 2 * I(a) * cap
print("  research gap at the cap, Delta_T m_cap - k - 2 a lambda_bar (positive: research sits at the cap)", show(gap))
print()

print("Two other strengths on the recruiting stretch")
for r in (Fr(18, 10), Fr(2)):
    T = tuple_at(I(r))
    mu_m, mu_0, mu_p = T["mu"]
    print("  r = {}".format(float(r)))
    print("    z            ", show(T["z"]))
    print("    posteriors (sale, no order, purchase)", mp.nstr(mp.mpf(mu_m.a.a), 9), mp.nstr(mp.mpf(mu_0.a.a), 9), mp.nstr(mp.mpf(mu_p.a.a), 9))
    print("    sale posterior minus no-order posterior", show(mu_m - mu_0))
    print("    prices (sale, no order, purchase)", mp.nstr(mp.mpf(T["P"][-1].a.a), 9), mp.nstr(mp.mpf(T["P"][0].a.a), 9), mp.nstr(mp.mpf(T["P"][1].a.a), 9))
print()

print("Ends of recruiting research at the cap, for reference")
# r_C: tau(r) = M at the cap, the root in (ell, h) of M r^2 + 2(c_H - M h) r - (ell^2 - p^2) + M ell^2 = 0.
A_, B_, C_ = M_cap, 2 * (I(c_H) - M_cap * I(h)), M_cap * I(ell * ell) - I(ell * ell - p * p)
r_C = (-B_ + iv.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
print("  r_C (tau = M at the cap)", show(r_C))
# Research reaches the cap where Delta_T m_cap - k = 2 a lambda_bar (the sale pays less than k there).
Dc = (I(k) + 2 * I(a) * cap) / m_cap
r_lb = 1 + Dc + iv.sqrt(Dc * Dc + 2 * Dc)
print("  strength at which research reaches the cap", show(r_lb))
print("  rho Delta_T m_cap - k there (negative: the positive part of the research equation is zero)", show(I(rho) * Dc * m_cap - I(k)))
