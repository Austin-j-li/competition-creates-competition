"""Chapter 09 (research): recompute research, entry and ownership on the research
branch, the branch end points, the strong-incumbent bound, the admissible cap and
cost, the range of beta and the threshold equilibria of the tie remark.

Exact fractions for rational quantities; mpmath at 50 digits for quantities that
depend on Euler's number. The script prints; it checks nothing by assertion.
"""
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50

h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, cH, k = Fr(1, 4), Fr(6), Fr(1, 50)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)
a = Fr(1, 40)
beta = mp.mpf("0.294655")
u = mp.e - 1
cap = u * beta / (1 + u * beta)       # the research cap = the benchmark presence
rq, kq, aq = mp.mpf(1) / 4, mp.mpf(1) / 50, mp.mpf(1) / 40


def q(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else mp.mpf(x)


def Delta(r):
    return (r - ell) ** 2 / (2 * r)


def tau(r):
    return (2 * r * cH - ell ** 2 + p ** 2) / (2 * r * h - r ** 2 - ell ** 2)


def B(r, mu):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    return gL + mu * (gH - gL)


def m_lam(lam, bt=beta):
    return (1 - lam) * bt / (2 * bt + lam * (1 - 2 * bt))


def lam_E(t, bt=beta):
    t = q(t)
    return bt * (2 * t - 1) / (bt + (1 - 2 * bt) * (1 - t))


def F_r(lam, D, aa=aq, bt=beta):
    return 2 * aa * (1 - 2 * bt) * lam ** 2 + (4 * aa * bt + kq * (1 - 2 * bt) + bt * D) * lam + bt * (2 * kq - D)


def lam_R(D, aa=aq, bt=beta):
    A2 = 2 * aa * (1 - 2 * bt)
    A1 = 4 * aa * bt + kq * (1 - 2 * bt) + bt * D
    A0 = bt * (2 * kq - D)
    return (-A1 + mp.sqrt(A1 ** 2 - 4 * A2 * A0)) / (2 * A2)


def frak(d):
    d = q(d)
    return 1 + d + mp.sqrt(d * d + 2 * d)


def bisect(g, lo, hi, it=200):
    lo, hi = q(lo), q(hi)
    for _ in range(it):
        mid = (lo + hi) / 2
        if g(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def Dq(r):
    r = q(r)
    return (r - 1) ** 2 / (2 * r)


def tauq(r):
    r = q(r)
    return (48 * r - 3) / (4 * (20 * r - r ** 2 - 1))


print("=" * 72)
print("1. Slot functions of research")
print("=" * 72)
print(f"  beta = {beta}, u = e - 1 = {mp.nstr(u, 12)}, cap = u beta/(1 + u beta) = {mp.nstr(cap, 12)}")
print(f"  u_cap = cap/((1-cap) beta) = {mp.nstr(cap / ((1 - cap) * beta), 12)} (equals u)")
print(f"  M_cap = {mp.nstr(1 - m_lam(cap), 12)} = e/(1+e) = {mp.nstr(mp.e / (1 + mp.e), 12)}; m_cap = {mp.nstr(m_lam(cap), 12)}")
print(f"  F_r(1) = 2a + k = {2 * a + k}; check at r = 1.6: {mp.nstr(F_r(1, Dq('1.6')), 12)}")
for lam in ("0", "0.1", "0.2", "0.3"):
    print(f"  lambda = {lam}: m_lambda = {mp.nstr(m_lam(mp.mpf(lam)), 8)}, M_lambda = {mp.nstr(1 - m_lam(mp.mpf(lam)), 8)}, "
          f"purchase probability beta + (1/2 - beta) lambda = {mp.nstr(beta + (mp.mpf(1)/2 - beta) * mp.mpf(lam), 8)}")

print("=" * 72)
print("2. Proposition 4(b): the six strengths")
print("=" * 72)
print(f"  (i) r0: Delta(r0) = {Delta(r0)}; k - Delta(r0) = {k - Delta(r0)} = {float(k - Delta(r0)):.6f}; "
      f"c_H - B(1/2) = {cH - B(r0, Fr(1, 2))} = {float(cH - B(r0, Fr(1, 2))):.6f}")
print("  (ii) intermediate strengths:")
for rs in ("1.55", "1.60", "1.65"):
    r = Fr(rs)
    D, t = Delta(r), tau(r)
    Dm, tm = q(D), q(t)
    lE = lam_E(t)
    lR = lam_R(Dm)
    MR = 1 - m_lam(lR)
    ent = rq + (1 - rq) * (beta + (mp.mpf(1) / 2 - beta) * lR)
    own = (rq + (1 - rq) * (beta + (1 - beta) * lR)) / 2
    UH = Dm * m_lam(lR) - kq
    phi = Dm * (1 - tm) - kq - 2 * aq * lE
    estar = (2 * aq * lE + kq) / (Dm * (1 - tm))
    entT = rq + (estar - rq) * (beta + (mp.mpf(1) / 2 - beta) * lE)
    print(f"    r = {rs}: Delta = {D} = {mp.nstr(Dm, 8)}, tau = {t} = {mp.nstr(tm, 8)}")
    print(f"      k - rho Delta/2 = {mp.nstr(kq - rq * Dm / 2, 8)};  Delta > 2k: {Dm > 2 * kq} ({mp.nstr(Dm - 2 * kq, 6)})")
    print(f"      lambda_E = {mp.nstr(lE, 8)}, lambda_R = {mp.nstr(lR, 8)}, F_r(lambda_R) = {mp.nstr(F_r(lR, Dm), 3)}")
    print(f"      lambda_R - lambda_E = {mp.nstr(lR - lE, 8)};  cap - lambda_R = {mp.nstr(cap - lR, 8)};  phi_a = {mp.nstr(phi, 8)}")
    print(f"      M_lambdaR = {mp.nstr(MR, 8)};  purchase payoff Delta m - k = {mp.nstr(UH, 8)} = 2a lambda_R = {mp.nstr(2 * aq * lR, 8)}")
    print(f"      entry = {mp.nstr(ent, 8)};  high-class ownership = {mp.nstr(own, 8)}")
    print(f"      rule CM threshold equilibrium: e* = {mp.nstr(estar, 8)}, entry = {mp.nstr(entT, 8)}")
print("  (iii) strong incumbents:")
Mcap = 1 - m_lam(cap)
bbar = (1 - cap) * beta
for r in (r1, r2):
    Dm = q(Delta(r))
    U = rq * Dm * m_lam(cap) - kq - aq * cap
    rec = Mcap > q(tau(r))
    ent = rq + (1 - rq) * (bbar + cap / 2) if rec else rq
    print(f"    r = {r}: tau = {mp.nstr(q(tau(r)), 8)}, M_cap - tau = {mp.nstr(Mcap - q(tau(r)), 6)}; "
          f"(U) margin rho Delta m_cap - k - a cap = {mp.nstr(U, 8)}; entry = {mp.nstr(ent, 8)}")
rU = frak((kq + aq * cap) * (1 + mp.e) / rq)
print(f"    r_U = frak((k + a cap)(1+e)/rho) = frak({mp.nstr((kq + aq * cap) * (1 + mp.e) / rq, 10)}) = {mp.nstr(rU, 10)}")

print("=" * 72)
print("3. Proposition 4(a): the implicit-function derivative at r = 1.6")
print("=" * 72)
r = mp.mpf("1.6")
D = Dq(r)
lR = lam_R(D)
dD = (1 - 1 / r ** 2) / 2
dFl = 4 * aq * (1 - 2 * beta) * lR + 4 * aq * beta + kq * (1 - 2 * beta) + beta * D
dFr = -beta * (1 - lR) * dD
slope = -dFr / dFl
eps = mp.mpf("1e-12")
fd = (lam_R(Dq(r + eps)) - lam_R(Dq(r - eps))) / (2 * eps)
print(f"  Delta'(1.6) = {mp.nstr(dD, 10)};  dF/dlambda = {mp.nstr(dFl, 10)};  dF/dr = -beta(1-lambda)Delta' = {mp.nstr(dFr, 10)}")
print(f"  lambda_R'(1.6) = {mp.nstr(slope, 10)};  central difference = {mp.nstr(fd, 10)}")
print(f"  entry slope (1-rho)(1/2-beta) lambda_R' = {mp.nstr((1 - rq) * (mp.mpf(1) / 2 - beta) * slope, 10)}")
print(f"  ownership slope (1/2)(1-rho)(1-beta) lambda_R' = {mp.nstr((1 - rq) * (1 - beta) * slope / 2, 10)}")

print("=" * 72)
print("4. The research branch at the benchmark")
print("=" * 72)


def phi_a(r, aa=aq):
    return Dq(r) * (1 - tauq(r)) - kq - 2 * aa * lam_E(tauq(r))


print(f"  phi_a(r0) = {mp.nstr(phi_a(q(r0)), 8)};  phi_a(7/4) = {mp.nstr(phi_a(mp.mpf(7) / 4), 8)}")
rR = bisect(phi_a, r0, Fr(7, 4))
rbarR = frak((2 * aq * cap + kq) * (1 + mp.e))
rN = frak(2 * kq / rq)
print(f"  r_R (phi_a = 0) = {mp.nstr(rR, 10)};  lambda_E(r_R) = {mp.nstr(lam_E(tauq(rR)), 8)}; "
      f"entry at r_R = {mp.nstr(rq + (1 - rq) * (beta + (mp.mpf(1)/2 - beta) * lam_E(tauq(rR))), 8)}")
print(f"  bar r_R = frak((2 a cap + k)(1+e)) = {mp.nstr(rbarR, 10)};  lambda_R(bar r_R) = {mp.nstr(lam_R(Dq(rbarR)), 10)} (= cap)")
print(f"  entry at the cap = {mp.nstr(rq + (1 - rq) * (beta + (mp.mpf(1)/2 - beta) * cap), 10)}")
print(f"  r_N = {mp.nstr(rN, 10)};  r_N - bar r_R = {mp.nstr(rN - rbarR, 8)};  r_A = see chapter 08 script")
print(f"  lambda_E(7/4) = {mp.nstr(lam_E(tauq(mp.mpf(7) / 4)), 8)} < cap = {mp.nstr(cap, 8)}")
# derivative bound for phi_a on [r0, 7/4]
dD_lo = Fr(1, 2) * (1 - 1 / r0 ** 2)
one_minus_tau = 1 - tau(Fr(7, 4))
D_hi = Delta(Fr(7, 4))
rr = Fr(7, 4)
taup_hi = 3 * (8 * rr ** 2 - rr + 2) / (2 * (20 * r0 - r0 ** 2 - 1) ** 2)
lead = dD_lo * one_minus_tau - D_hi * taup_hi
den = (beta + (1 - 2 * beta) * q(one_minus_tau)) ** 2
phip_lb = q(lead) - 2 * aq * beta * q(taup_hi) / den
amono = q(lead) * den / (2 * beta * q(taup_hi))
print(f"  bounds on [r0, 7/4]: Delta' >= {dD_lo}, 1 - tau >= {one_minus_tau}, Delta <= {D_hi}, tau' <= {taup_hi} = {float(taup_hi):.6f}")
print(f"  (Delta(1-tau))' >= {lead} = {float(lead):.6f};  phi_a' >= {mp.nstr(phip_lb, 8)};  a_mono = {mp.nstr(amono, 8)}")

print("=" * 72)
print("5. The admissible cap and cost (Proposition A.2)")
print("=" * 72)
lE1, lE2 = lam_E(tau(r1)), lam_E(tau(r2))
print(f"  cap strip (lambda_E(r1), lambda_E(r2)) = ({mp.nstr(lE1, 8)}, {mp.nstr(lE2, 8)})")
print(f"  margins of the benchmark cap: {mp.nstr(cap - lE1, 8)}, {mp.nstr(lE2 - cap, 8)}")
D155, D165 = q(Delta(Fr('1.55'))), q(Delta(Fr('1.65')))
a_up = (D155 * (1 - q(tau(Fr('1.55')))) - kq) / (2 * lam_E(tau(Fr('1.55'))))


def a_lo(c, bt=beta):
    return (D165 * m_lam(c, bt) - kq) / (2 * c)


print(f"  a_lo(cap) = {mp.nstr(a_lo(cap), 8)};  a_up = {mp.nstr(a_up, 8)};  window width = {mp.nstr(a_up - a_lo(cap), 6)}")
print(f"  margins of a = 1/40: {mp.nstr(aq - a_lo(cap), 8)}, {mp.nstr(a_up - aq, 8)}")
cap_lo_a = bisect(lambda c: aq - a_lo(c), mp.mpf("0.2"), mp.mpf("0.4"))
print(f"  at a = 1/40 the cap range is ({mp.nstr(cap_lo_a, 8)}, {mp.nstr(lE2, 8)});  lambda_R(1.65) = {mp.nstr(lam_R(D165), 8)}")
print(f"  a_lo(lambda_E(r1)) = {mp.nstr(a_lo(lE1), 8)} < a_up")
for c in (lE1, mp.mpf("0.30"), mp.mpf("0.31"), mp.mpf("0.32"), mp.mpf("0.33"), cap, lE2):
    aU1 = (rq * q(Delta(r1)) * m_lam(c) - kq) / c
    aU2 = (rq * q(Delta(r2)) * m_lam(c) - kq) / c
    print(f"    cap {mp.nstr(c, 6)}: a_lo = {mp.nstr(a_lo(c), 6)}, a_up = {mp.nstr(a_up, 6)}, "
          f"a_U(r1) = {mp.nstr(aU1, 6)}, a_U(r2) = {mp.nstr(aU2, 6)}")

print("=" * 72)
print("6. The range of beta (cap = u beta/(1 + u beta), a = 1/40)")
print("=" * 72)
L = (D165 / (1 + mp.e) - kq) / (2 * aq)
beta_lo = L / (u * (1 - L))
print(f"  a_lo(beta) = a  <=>  lambda_B(beta) = [Delta(1.65)/(1+e) - k]/(2a) = {mp.nstr(L, 10)}  <=>  beta = {mp.nstr(beta_lo, 10)}")


def a_up_beta(bt):
    t = q(tau(Fr('1.55')))
    return (D155 * (1 - t) - kq) / (2 * lam_E(t, bt))


beta_hi = bisect(lambda bt: aq - a_up_beta(bt), mp.mpf("0.3"), mp.mpf("0.49999"))
print(f"  a_up(beta) = a at beta = {mp.nstr(beta_hi, 8)}")
third = mp.mpf(1) / 3
capB = u * third / (1 + u * third)
print(f"  (U) at r1 with beta = 1/3: rho Delta(r1)/(1+e) - k - a lambda_B(1/3) = {mp.nstr(rq * q(Delta(r1)) / (1 + mp.e) - kq - aq * capB, 8)}")
den3 = (third + (1 - 2 * third) * q(one_minus_tau)) ** 2
print(f"  a_mono(1/3) = {mp.nstr(q(lead) * den3 / (2 * third * q(taup_hi)), 8)}")
print(f"  benchmark beta - beta_lo = {mp.nstr(beta - beta_lo, 8)}")

print("=" * 72)
print("7. Tie remark: entry range at r_C under rule CM")
print("=" * 72)
Mh_c = Mcap * 10 - 6
rC = (Mh_c + mp.sqrt(Mh_c ** 2 + Mcap * ((1 - Mcap) - mp.mpf(1) / 4))) / Mcap
print(f"  r_C = {mp.nstr(rC, 10)};  entry under CM fills [rho, {mp.nstr(rq + (1 - rq) * (bbar + cap / 2), 8)}]")
