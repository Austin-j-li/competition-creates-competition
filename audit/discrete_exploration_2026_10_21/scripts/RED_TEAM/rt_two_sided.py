"""Red team: C1 two-sided constants against the paper's Laplace values (print only).

Checks the exact matches (M, r_C at c_H = 6, r_N, rfrak(k)) and the non-matches
(r_U, entry, Proposition 3 values), and reproduces the paper's entry 0.522757 from eq. (12).
Run from the repository root with .venv/bin/python. No assertions.
"""
from mpmath import mp, mpf, exp, sqrt, log

mp.dps = 40
h, l, p, rho, k, b = mpf(10), mpf(1), mpf(1) / 2, mpf(1) / 4, mpf(1) / 50, mpf(2)
a = exp(-1 / b)


def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p ** 2 / (2 * r)
    tL = l - (l ** 2 - p ** 2) / (2 * r)
    return t0, tH, tL, h - tH, (l ** 2 - p ** 2) / (2 * r), (r - l) ** 2 / (2 * r)


def B(r, mu):
    _, _, _, gH, gL, _ = auction(r)
    return gL + mu * (gH - gL)


def rfrak(d):
    return l + d + sqrt(d ** 2 + 2 * l * d)


def r_ceiling(mu, cH):
    return (mu * h - cH + sqrt((mu * h - cH) ** 2 + mu * ((1 - mu) * l ** 2 - p ** 2))) / mu


M2 = 1 / (1 + a ** 2)   # paper's M = 1/(1+e^{-2/b})
m2 = a ** 2 / (1 + a ** 2)
M1, m1 = 1 / (1 + a), a / (1 + a)
print("=== posterior bounds ===")
print("paper M = 1/(1+e^{-2/b}) =", M2, " m =", m2)
print("buy-only M1 =", M1, " m1 =", m1)

print("\n=== exact matches ===")
print("r_C at c_H = 6 with M:", r_ceiling(M2, mpf(6)), " (paper 3.592658519)")
print("r_C at c_H = 5 with M:", r_ceiling(M2, mpf(5)), " buy-only r_C at c_H = 5 with M1:", r_ceiling(M1, mpf(5)))
print("r_N = rfrak(2k/rho) =", rfrak(2 * k / rho), " (paper 1.747877538)")
print("rfrak(k) =", rfrak(k), " (paper 1.220997512)")
print("c_H window two-sided at (1.2, 3): (", B(mpf('1.2'), mpf(1) / 2), ",", B(mpf(3), M2), "]")
print("c_H window buy-only at (1.2, 3): (", B(mpf('1.2'), mpf(1) / 2), ",", B(mpf(3), M1), "]")

print("\n=== non-matches ===")
print("two-sided sufficient full-order bound rfrak(k/(rho m)) =", rfrak(k / (rho * m2)))
print("paper r_U = rfrak(k/((1-1/b) rho m)) =", rfrak(k / ((1 - 1 / b) * rho * m2)), " (paper 2.837416964)")
print("upper bound on k in (A3): paper (1-1/b) rho m Delta_T(3) =", (1 - 1 / b) * rho * m2 * auction(mpf(3))[5], " discrete rho m Delta_T(3) =", rho * m2 * auction(mpf(3))[5])
E2 = rho + (1 - rho) * (1 + a ** 2) / (2 * (1 + a))
O2 = (rho + (1 - rho) / (1 + a)) / 2
print("two-sided full-trade entry =", E2, " ownership =", O2)
J = a ** 2 / ((1 + a) * (1 + a ** 2))
phi = a * (1 - a) / (1 + a)
cT = J * (1 + rho) + phi * rho / 2
print("c_T =", cT, " full-trade existence r = rfrak(k/c_T) =", rfrak(k / cT), " no-feedback coefficient rho[beta m + phi/2 + delta M] =", rho * (M1 * m2 + phi / 2 + (a ** 2 / (1 + a)) * M2))
gT3 = auction(mpf(3))[5] * cT
print("two-sided net gain at r=3 with recruitment:", gT3 - k, " without:", auction(mpf(3))[5] * rho * (M1 * m2 + phi / 2 + (a ** 2 / (1 + a)) * M2) - k)

print("\n=== the paper's own entry at r_1 = 3, c_H = 6 from eq. (12) ===")
r = mpf(3)
_, _, _, gH, gL, DT = auction(r)
tau = (mpf(6) - gL) / (gH - gL)
xs = (b / 2) * log(tau / (1 - tau))
aH = 1 - exp((xs - 1) / b) / 2
aL = exp(-(xs + 1) / b) / 2
print("tau =", tau, " x* =", xs, " alpha_H =", aH, " alpha_L =", aL)
print("E = rho + (1-rho)(alpha_H+alpha_L)/2 =", rho + (1 - rho) * (aH + aL) / 2, " (paper 0.522757)")
print("O_H = [rho + (1-rho) alpha_H]/2 =", (rho + (1 - rho) * aH) / 2, " (paper 0.324192)")
print("A.14 limit of entry as r -> r_C: rho + (1-rho)(1+e^{-2/b})/4 =", rho + (1 - rho) * (1 + a ** 2) / 4)
