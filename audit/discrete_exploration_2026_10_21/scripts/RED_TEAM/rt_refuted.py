"""Red team: the refuted claims, recomputed (print only).

(a) the brief's feedback number +0.060 against the exact +0.058335;
(b) C5's rent-transfer reading: the three-point ledger at r = 3, c_H = 6 (exact fractions);
(c) C7's silence pooling: a binding bid J = 2 at r = 3, mu = 3/5, c_H = 5;
(d) C8's unobservable-preparation equivalence: the sunk-preparation deviation at r = 3.6;
(e) C3's late ceiling at delta = 0.8: the root of 0.8 B_r(M_2) = 5 and the residual at r = 8.
Run from the repository root with .venv/bin/python. No assertions.
"""
from fractions import Fraction as Fr
from mpmath import mp, mpf, exp, sqrt, findroot

mp.dps = 30
h, l, p, rho, k, b = mpf(10), mpf(1), mpf(1) / 2, mpf(1) / 4, mpf(1) / 50, mpf(2)
a = exp(-1 / b)


def auction(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p ** 2 / (2 * r)
    tL = l - (l ** 2 - p ** 2) / (2 * r)
    return t0, tH, tL, h - tH, (l ** 2 - p ** 2) / (2 * r), (r - l) ** 2 / (2 * r)


print("=== (a) feedback at r = 3, c_H = 5 ===")
DT3 = auction(mpf(3))[5]
print("net, entry fixed at rho: 2*rho*a*Delta_T/(1+a)^2 - k =", 2 * rho * a * DT3 / (1 + a) ** 2 - k)
print("net, entry after good news: (1+rho)*a*Delta_T/(1+a)^2 - k =", (1 + rho) * a * DT3 / (1 + a) ** 2 - k)
print("nearby objects: rho*Delta_T/2 - k =", rho * DT3 / 2 - k, " rho*m1*Delta_T - k =", rho * (a / (1 + a)) * DT3 - k)

print("\n=== (b) C5 ledger, three-point model, r = 3, c_H = 6 (exact) ===")
hF, lF, pF, rhoF, cHF, rF = Fr(10), Fr(1), Fr(1, 2), Fr(1, 4), Fr(6), Fr(3)
t0 = pF * (1 - pF / rF)
tH = rF / 2 + pF ** 2 / (2 * rF)
tL = lF - (lF ** 2 - pF ** 2) / (2 * rF)
gH, gL, DT = hF - tH, (lF ** 2 - pF ** 2) / (2 * rF), tH - tL
wH, wL = tH - t0, tL - t0
a0 = (rF ** 2 - pF ** 2) / (2 * rF)
aH, aL = hF - a0, (lF ** 2 + pF ** 2) / (2 * rF)
tau = (cHF - gL) / (gH - gL)
beta_max = 1 / tau - 1
print("tau =", tau, " beta_max =", beta_max)


def ledger(eH, eL, E, kcost):
    T = t0 + (eH * wH + eL * wL) / 2
    C = (eH * gH + eL * gL) / 2 - cHF * (E - rhoF)
    W = a0 + (eH * aH + eL * aL) / 2 - cHF * (E - rhoF) - kcost
    return T, C, W


# hidden price: entry rho, orders full (one unit by H), trading cost k/2
kk = Fr(1, 50)
T_h, C_h, W_h = ledger(rhoF, rhoF, rhoF, kk / 2)
# S: (1,0), e(2)=1: eH = rho + (1-rho)/3, eL = rho
eH_S, eL_S = rhoF + (1 - rhoF) / 3, rhoF
E_S = (eH_S + eL_S) / 2
T_S, C_S, W_S = ledger(eH_S, eL_S, E_S, kk / 2)
# M at Omega_2: (1, beta_max), e(2)=1
beta = beta_max
eH_M, eL_M = rhoF + (1 - rhoF) / 3, rhoF + beta * (1 - rhoF) / 3
E_M = (eH_M + eL_M) / 2
T_M, C_M, W_M = ledger(eH_M, eL_M, E_M, kk * (1 + beta) / 2)
print("hidden: E", rhoF, " T", T_h, float(T_h), " C", C_h, float(C_h), " W", W_h, float(W_h))
print("S:      E", E_S, float(E_S), " T", T_S, float(T_S), " C", C_S, float(C_S), " W", W_S, float(W_S))
print("M(O2):  E", E_M, float(E_M), " T", T_M, float(T_M), " C", C_M, float(C_M), " W", W_M, float(W_M))
print("Delta T (M - S) =", T_M - T_S, float(T_M - T_S), " Delta C =", C_M - C_S, float(C_M - C_S), " ratio Delta T / (-Delta C) =", (T_M - T_S) / (C_S - C_M), float((T_M - T_S) / (C_S - C_M)))
print("share of information surplus lost (W_S - W_M)/(W_S - W_h) =", (W_S - W_M) / (W_S - W_h), float((W_S - W_M) / (W_S - W_h)))

print("\n=== (c) C7 silence pooling at r = 3, mu = 3/5, c_H = 5: binding bid J = 2 ===")
mu, J, R = Fr(3, 5), Fr(2), Fr(3)
print("upper bound on challenger gross profit after bid J (any belief): mu*(h-J) + (1-mu)*(l-J)_+ =", mu * (hF - J), float(mu * (hF - J)), "< 5")
gain = (R - J) * (1 - rhoF * mu) - (1 - mu) * (R - lF)
print("gain of type R = 3 from the bid over silence with full entry:", gain, float(gain))
muM = 1 / (1 + a)
gainM = (mpf(3) - 2) * (1 - rho * muM) - (1 - muM) * (mpf(3) - 1)
print("same at mu = M1:", gainM, " bound mu*(h-J) =", muM * (h - 2))
# the selected cutoff at (r=3, mu=M1): D_mu(c) = mu (h - (c+r)/2) + (1-mu) (l-c)^2/(2(r-c)) = c_H
r3 = mpf(3)
Dmu = lambda c: muM * (h - (c + r3) / 2) + (1 - muM) * (l - c) ** 2 / (2 * (r3 - c))
cstar = findroot(lambda c: Dmu(c) - 5, (mpf('0.9'), mpf('0.95')))
print("selected cutoff c* at (r=3, mu=M1):", cstar, " entry rho + (1-rho)/2 * c*/r =", rho + (1 - rho) / 2 * cstar / r3)

print("\n=== (d) C8: sunk preparation at r = 3.6, mu = M1, c_L = 0 ===")
r36 = mpf('3.6')
p1 = l                                         # the main-timing optimum at (3.6, M1) is the reserve p = l = 1
t0 = p1 * (1 - p1 / r36)
tH = r36 / 2 + p1 ** 2 / (2 * r36)
tL = l - (l ** 2 - p1 ** 2) / (2 * r36)
gH, gL, DT = h - tH, (l ** 2 - p1 ** 2) / (2 * r36), tH - tL
S_main = t0 + 1 * (tL - t0 + muM * DT)       # entry 1 at p = l (regime I boundary)
print("B(p=1, M1) at r=3.6 =", gL + muM * (gH - gL), " (>= 5 gives entry 1)")
print("main timing proceeds at p = 1 with entry 1:", S_main)
print("deviation to p = h with preparation sunk at 1: mu*h =", muM * h)
print("exclusion value at p = h with entry rho: rho*mu*h =", rho * muM * h)

print("\n=== (e) C3: late ceiling at delta = 0.8 ===")
M2 = 1 / (1 + a ** 2)
Bm = lambda r, m: m * h - m * r / 2 + ((1 - m) * l ** 2 - p ** 2) / (2 * r)
root = (M2 * h - mpf('6.25') + sqrt((M2 * h - mpf('6.25')) ** 2 + M2 * ((1 - M2) * l ** 2 - p ** 2))) / M2
print("root of 0.8*B_r(M2) = 5:", root, " check 0.8*B_root(M2) - 5 =", mpf('0.8') * Bm(root, M2) - 5)
print("residual at r = 8: 0.8*B_8(M2) - 5 =", mpf('0.8') * Bm(mpf(8), M2) - 5)
print("one-round ceiling B_r(M1) = 5 at r =", (muM * h - 5 + sqrt((muM * h - 5) ** 2 + muM * ((1 - muM) * l ** 2 - p ** 2))) / muM)
print("delta = 0.95 late ceiling root of 0.95*B_r(M2) = 5:", (M2 * h - 5 / mpf('0.95') + sqrt((M2 * h - 5 / mpf('0.95')) ** 2 + M2 * ((1 - M2) * l ** 2 - p ** 2))) / M2)
