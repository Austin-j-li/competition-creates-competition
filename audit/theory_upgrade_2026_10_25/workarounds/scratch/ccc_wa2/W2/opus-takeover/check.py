"""Remaining formula checks: the at-risk share elasticity of W_H for a uniform class and uniform incumbents,
the ceiling psi on the spread elasticity of class-H entry, the point-mass discrete sufficient condition,
and the frozen-information ownership in the research branch. Prints only."""
import random
from mpmath import mp, mpf, sqrt, e as E, quad

mp.dps = 30

print("=== (1) d log W_H / d log r = -(1 - Pr_H(theta >= r)/W_H(r)) for G_H = U[1,19], R ~ U[0,r] ===")
lo, hi = mpf(1), mpf(19)


def WH(r):
    return quad(lambda t: min(t / r, mpf(1)), [lo, min(max(r, lo), hi), hi]) / (hi - lo)


for r in (mpf("4.5"), mpf(9), mpf(15)):
    hstep = mpf(10) ** -8
    fd = (WH(r * (1 + hstep)) - WH(r * (1 - hstep))) / (2 * hstep) / WH(r)
    surv = (hi - r) / (hi - lo) if r < hi else mpf(0)
    formula = -(1 - surv / WH(r))
    print(f"  r={mp.nstr(r, 3)}: W_H={mp.nstr(WH(r), 7)} finite diff={mp.nstr(fd, 8)} formula={mp.nstr(formula, 8)} at-risk share={mp.nstr(-formula, 6)}")

print("\n=== (2) psi(lam) decreasing on [0,1) for beta in (0,1/3], and eps_e < psi(lam_R) on random branch points ===")
ok = True
for bi in range(1, 34):
    b = mpf(bi) / 100
    vals = [(1 - b) * (1 - l) * (2 * b + (1 - 2 * b) * l) / (b + (1 - b) * l) for l in [mpf(i) / 200 for i in range(0, 200)]]
    if any(vals[i + 1] > vals[i] for i in range(len(vals) - 1)):
        ok = False
print("  psi decreasing on the grid for every beta = 0.01..0.33:", ok)


def m_of(lam, beta):
    return (1 - lam) * beta / (2 * beta + lam * (1 - 2 * beta))


def lam_R(Delta, a, beta, k):
    A = 2 * a * (1 - 2 * beta)
    B = 4 * a * beta + k * (1 - 2 * beta) + beta * Delta
    C = beta * (2 * k - Delta)
    return (-B + sqrt(B * B - 4 * A * C)) / (2 * A)


random.seed(11)
worst = mpf(0)
for t in range(3000):
    beta = mpf(random.uniform(0.01, 1 / 3))
    rho = mpf(random.uniform(0.001, 0.9))
    a = mpf(10) ** random.uniform(-3, 2)
    k = mpf(10) ** random.uniform(-3, 0)
    Delta = 2 * k * (1 + mpf(10) ** random.uniform(-3, 2))
    lR = lam_R(Delta, a, beta, k)
    den = 2 * beta + lR * (1 - 2 * beta)
    Lp = m_of(lR, beta) / (2 * a + Delta * beta / den ** 2)
    eH = rho + (1 - rho) * (beta + (1 - beta) * lR)
    eps = Delta * (1 - rho) * (1 - beta) * Lp / eH
    psi = (1 - beta) * (1 - lR) * den / (beta + (1 - beta) * lR)
    worst = max(worst, eps / psi)
print("  max over 3000 random (beta, rho, a, k, Delta) of eps_e/psi(lam_R):", mp.nstr(worst, 6))

print("\n=== (3) point masses: O_H(F1) > O_H(F0) whenever e_H(F1)/e_H(F0) >= (h-ell)/(h-ell-Delta(F1)) ===")
h, ell, rho, k = mpf(10), mpf(1), mpf(1) / 4, mpf(1) / 50
Dmax = 2 * k / rho
print(f"  branch needs Delta < 2k/rho = {mp.nstr(Dmax, 5)}; worst required entry gain (h-ell)/(h-ell-2k/rho) - 1 = {mp.nstr((h - ell) / (h - ell - Dmax) - 1, 6)}")
beta = mpf("0.294655")
u = E - 1
cap = u * beta / (1 + u * beta)
eH_R = mpf(1) / 4 + mpf(3) / 4 * (beta + (1 - beta) * mpf("0.193853382"))
eH_cap = mpf(1) / 4 + mpf(3) / 4 * (beta + (1 - beta) * cap)
print(f"  benchmark path: e_H rises {mp.nstr(100 * (eH_cap / eH_R - 1), 5)}% from r_R to rbar_R")

print("\n=== (4) frozen information on the research branch (Proposition A.3 setting), counterexample family ===")
# freeze lamR(F0) and the orders (H buys, L abstains) at r0 = 11; evaluate at r1 = 12
beta, rho, kk, a, cH = mpf(1) / 5, mpf(1) / 20, mpf(1) / 5, mpf(5), mpf(5) / 2


def unif(r):
    Delta = 9 - mpf(99) / (2 * r)
    gam = mpf(99) / (2 * r)
    gL = mpf("0.375") / r
    return Delta, (cH - gL) / gam, mpf(10) / r


D0, t0, W0 = unif(mpf(11))
D1, t1, W1 = unif(mpf(12))
l0, l1 = lam_R(D0, a, beta, kk), lam_R(D1, a, beta, kk)
M0 = 1 - m_of(l0, beta)
recruits = M0 >= t1
eH0 = rho + (1 - rho) * (beta + (1 - beta) * l0)
eH1 = rho + (1 - rho) * (beta + (1 - beta) * l1)
ebar = eH0 if recruits else rho
O0, O1, Obar = eH0 * W0 / 2, eH1 * W1 / 2, ebar * W1 / 2
print(f"  M at frozen lam={mp.nstr(M0, 7)} tau(12)={mp.nstr(t1, 7)} frozen purchase recruits: {recruits}")
print(f"  O_H(11)={mp.nstr(O0, 7)} frozen O_H(12)={mp.nstr(Obar, 7)} O_H(12)={mp.nstr(O1, 7)}")
print(f"  information effect O_H(12)-frozen={mp.nstr(O1 - Obar, 7)}  fixed-information effect frozen-O_H(11)={mp.nstr(Obar - O0, 7)}")
