"""Red team: three-point checks and the A.10 attribution (print only, exact fractions).

Confirms K = (2/3) rho (1-pi) Delta_T at r = 3, the cutoffs rfrak(6/25) and rfrak(4/25),
the benchmark outcomes, and the floor argument behind the A.10 verdict:
with c_L = 0, B_r(mu) >= g_L > 0 at every posterior under every noise law, so no
zero-entry price pool exists; with c_L = 1, pools need an attained posterior with
B_r(mu) < 1, which the three-point model attains (posterior 0) and the Laplace model
does not within its own condition (A1).
Run from the repository root with .venv/bin/python. No assertions.
"""
from fractions import Fraction as Fr
from mpmath import mp, mpf, sqrt, exp

mp.dps = 30
h, l, p, rho, k, pi = Fr(10), Fr(1), Fr(1, 2), Fr(1, 4), Fr(1, 50), Fr(1, 2)


def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p ** 2 / (2 * r)
    tL = l - (l ** 2 - p ** 2) / (2 * r)
    return t0, tH, tL, h - tH, (l ** 2 - p ** 2) / (2 * r), (r - l) ** 2 / (2 * r)


r = Fr(3)
t0, tH, tL, gH, gL, DT = auction(r)
K = Fr(2, 3) * rho * (1 - pi) * DT
print("r = 3: Delta_T =", DT, " K = (2/3) rho (1-pi) Delta_T =", K, float(K), " K_dev under passive belief (3/2)K =", Fr(3, 2) * K)
print("g_H(3) =", gH, float(gH), " g_L(3) =", gL, " B_3(1/2) =", gL + (gH - gL) / 2, float(gL + (gH - gL) / 2))
E = rho + (1 - rho) * pi / 3
OH = pi * rho + (1 - rho) * pi / 3
RT = t0 + OH * (tH - t0) + (E - OH) * (tL - t0)
print("benchmark full buying at r = 3 (c_H = 6): E =", E, " O_H =", OH, " R_T =", RT, float(RT))
rf = lambda d: 1 + d + sqrt(d * d + 2 * d)
print("IC cutoff rfrak(3k/rho) = rfrak(6/25) =", rf(mpf(6) / 25), " passive cutoff rfrak(2k/rho) = rfrak(4/25) =", rf(mpf(4) / 25))
rC1 = h - 6 + sqrt(mpf(16) - mpf(1) / 4)
print("three-point ceiling r_C(1) at c_H = 6: h - c_H + sqrt((h-c_H)^2 - p^2) =", rC1)

print("\n=== A.10 attribution ===")
for rr in (Fr(6, 5), Fr(3), Fr(18, 5)):
    _, _, _, gH, gL, _ = auction(rr)
    print(f"r={rr}: min over mu of B_r(mu) = g_L = {gL} = {float(gL):.6f} > 0 = c_L; with c_L = 1, B_r(mu) < 1 iff mu < {(1 - gL) / (gH - gL)} = {float((1 - gL) / (gH - gL)):.6f}")
a = exp(-mpf(1) / 2)
m_lap, m1 = a ** 2 / (1 + a ** 2), a / (1 + a)
print("Laplace lowest posterior m =", m_lap, " buy-only dLaplace m1 =", m1, " three-point lowest posterior under full buying = 0")
print("So at c_L = 1 and r = 3: the three-point model has zero entry at posterior 0 (pool possible);")
print("the Laplace and discrete-Laplace models keep the floor since m, m1 > 0.105; at c_L = 0 no model has a pool.")
