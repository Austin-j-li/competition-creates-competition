"""Print the values that the report's charts plot.

Print only. Every value comes from a closed form stated in a memo:
- auction objects: TEAM_RULES section 3 (paper eq. (4));
- three-point path: memos/A_three_point.md, Section 5 (cutoff r(3k/(2 rho (1-pi))), r_C(1) = 4 + 1.5 sqrt 7);
- buy-only discrete-Laplace: memos/B_dlaplace_theory.md, Results 2, 3, 6, 6A
  (K_1(s) = Delta_T kappa phi_1(pi delta s), entry rho + (1-rho) N_+(s));
- two-sided discrete-Laplace: memos/C1_two_sided.md, Prop. C1.1 and Result 3
  (P_+ = (1+a^2)/(2(1+a)), c_T = J(1+rho) + phi rho/2);
- unequal three-point noise: memos/C9_unequal_mixing.md, exact table of branch A.
"""
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 40

h, ell, p, rho, k, pi = mp.mpf(10), mp.mpf(1), mp.mpf("0.5"), mp.mpf("0.25"), mp.mpf("0.02"), mp.mpf("0.5")
b = mp.mpf(2)
a = mp.e ** (-1 / b)


def DT(r):
    return (r - ell) ** 2 / (2 * r)


def gH(r):
    return h - r / 2 - p ** 2 / (2 * r)


def gL(r):
    return (ell ** 2 - p ** 2) / (2 * r)


def B(r, mu):
    return gL(r) + mu * (gH(r) - gL(r))


def rinv(d):
    """Root above ell of Delta_T(r) = d (paper (A.10))."""
    return ell + d + mp.sqrt(d ** 2 + 2 * ell * d)


def f6(x):
    return mp.nstr(x, 7, strip_zeros=False)


print("== Constants (b = 2) ==")
gam = 1 / (1 + a)
m1, M1 = 1 - gam, gam
M = 1 / (1 + a ** 2)
m = 1 - M
print("a =", f6(a))
print("buy-only posteriors m1, M1 =", f6(m1), f6(M1))
print("two-sided posteriors m, 1/2, M =", f6(m), "0.5", f6(M))

print("\n== Three-point base, c_H = 6 (A1 Section 5) ==")
cut3 = rinv(3 * k / (2 * rho * (1 - pi)))
rC1 = 4 + mp.mpf(3) / 2 * mp.sqrt(7)
print("trade cutoff r(3k/(2 rho (1-pi))) =", f6(cut3))
print("ceiling r_C(1) (g_H(r) = 6) =", f6(rC1), " check g_H =", f6(gH(rC1)))
print("entry: 0.25 for r <=", f6(cut3), "; 3/8 =", 3 / 8, "up to", f6(rC1), "; 0.25 above")

print("\n== Buy-only discrete-Laplace base, c_H = 5 (B2) ==")
cH = mp.mpf(5)
delta = 2 * gam - 1
kap = (1 - pi) * gam * (1 - gam)


def phi1(y):
    return 1 / (1 - gam + y) + rho / (gam - y)


def K1(r, s):
    return DT(r) * kap * phi1(pi * delta * s)


def Nplus(s):
    return 1 - gam + pi * delta * s


def tau(r):
    return (cH - gL(r)) / (gH(r) - gL(r))


def sstar(r):
    t = tau(r)
    return (1 - gam) * (t - pi) / (pi * delta * (1 - t))


rF = rinv(k / ((1 + rho) * a / (1 + a) ** 2))
rN = rinv(2 * k / rho)
rC5 = mp.findroot(lambda r: B(r, M1) - cH, 4)
rI = mp.findroot(lambda r: K1(r, sstar(r)) - k, 1.405)
print("r_I =", f6(rI), " r_F =", f6(rF), " r_N =", f6(rN), " r_C =", f6(rC5))
print("full-purchase entry rho + (1-rho) N_+(1) =", f6(rho + (1 - rho) * Nplus(1)))
print("entry at r_I (s_hat = s*) =", f6(rho + (1 - rho) * Nplus(sstar(rI))))


def shat(r):
    return mp.findroot(lambda s: K1(r, s) - k, (sstar(r) + 1) / 2)


print("check against B2 (0.558559, 0.576414, 0.595797, 0.617257):")
for r in ("1.41", "1.42", "1.43", "1.44"):
    rr = mp.mpf(r)
    print("  r =", r, " entry =", f6(rho + (1 - rho) * Nplus(shat(rr))))
print("s_hat branch points for the chart (r, entry):")
pts = [rI + (rF - rI) * mp.mpf(i) / 12 for i in range(13)]
out = []
for r in pts:
    s = sstar(r) if r == rI else (mp.mpf(1) if r == rF else shat(r))
    out.append("[%s,%s]" % (mp.nstr(r, 7), mp.nstr(rho + (1 - rho) * Nplus(s), 6)))
print("  " + ",".join(out))

print("\n== Two-sided discrete-Laplace base, c_H = 6 (C1) ==")
cH6 = mp.mpf(6)
Pplus = (1 + a ** 2) / (2 * (1 + a))
beta, dlt = 1 / (1 + a), a ** 2 / (1 + a)
phi0 = 1 - beta - dlt
J = a ** 2 / ((1 + a) * (1 + a ** 2))
cT = J * (1 + rho) + phi0 * rho / 2
rC6 = mp.findroot(lambda r: B(r, M) - cH6, 3.6)
print("P_+ =", f6(Pplus), " entry under full orders =", f6(rho + (1 - rho) * Pplus))
print("c_T =", f6(cT), " full trade from r(k/c_T) =", f6(rinv(k / cT)))
print("no trade up to r_N =", f6(rN), " ceiling r_C =", f6(rC6))
print("sufficient bounds r(k) =", f6(rinv(k)), " r(k/(rho m)) =", f6(rinv(k / (rho * m))))

print("\n== Unequal three-point noise (C9, exact table of branch A) ==")
for r, e in (("63/40", "1567/2974"), ("79/50", "4137/7730"), ("317/200", "201299/370310")):
    print("  r =", r, "=", float(Fraction(r)), " entry =", round(float(Fraction(e)), 6))
