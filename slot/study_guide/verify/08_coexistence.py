"""Chapter 08 (coexistence): recompute the thresholds, the Sturm counts, the entry
along the informative branch, the prior windows and the equilibrium set.

Exact fractions for rational quantities and rational polynomials; mpmath at 50
digits for quantities that depend on Euler's number. The script prints; it checks
nothing by assertion.
"""
from fractions import Fraction as Fr
import mpmath as mp

mp.mp.dps = 50

h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, cH, k = Fr(1, 4), Fr(6), Fr(1, 50)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)
beta = mp.mpf("0.294655")
u = mp.e - 1
lam = u * beta / (1 + u * beta)
b = (1 - lam) * beta
b0 = (1 - lam) * (1 - 2 * beta)
M = (1 + u) / (2 + u)
m = 1 - M


def q(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else mp.mpf(x)


def Delta(r):
    return (r - ell) ** 2 / (2 * r)


def tau(r):
    return (2 * r * cH - ell ** 2 + p ** 2) / (2 * r * h - r ** 2 - ell ** 2)


def J(r):
    return Delta(r) * (1 - tau(r))


def frak(d):
    """Root above ell of Delta(r) = d."""
    d = q(d)
    return q(ell) + d + mp.sqrt(d * d + 2 * q(ell) * d)


def bisect_exact(g, lo, hi, width=Fr(1, 10 ** 30)):
    """Root of an increasing rational function g on [lo, hi] by exact-sign bisection."""
    while hi - lo > width:
        mid = (lo + hi) / 2
        mid = Fr(round(mid * 10 ** 40), 10 ** 40) if mid.denominator > 10 ** 40 else mid
        if g(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi, (g(lo) < 0 < g(hi))


def bisect_mp(g, lo, hi, it=200):
    lo, hi = mp.mpf(lo), mp.mpf(hi)
    for _ in range(it):
        mid = (lo + hi) / 2
        if g(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- polynomials
def padd(a, c):
    n = max(len(a), len(c))
    return trim([(a[i] if i < len(a) else 0) + (c[i] if i < len(c) else 0) for i in range(n)])


def pneg(a):
    return [-x for x in a]


def pmul(a, c):
    out = [Fr(0)] * (len(a) + len(c) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(c):
            out[i + j] += x * y
    return trim(out)


def pder(a):
    return trim([i * a[i] for i in range(1, len(a))]) or [Fr(0)]


def trim(a):
    a = [Fr(x) for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def peval(a, x):
    out = Fr(0)
    for c in reversed(a):
        out = out * x + c
    return out


def pdivmod(a, d):
    a = trim(a)
    d = trim(d)
    quo = [Fr(0)] * max(1, len(a) - len(d) + 1)
    rem = a[:]
    while len(rem) >= len(d) and any(rem):
        coef = rem[-1] / d[-1]
        shift = len(rem) - len(d)
        quo[shift] = coef
        rem = padd(rem, pneg(pmul([Fr(0)] * shift + [coef], d)))
        if len(rem) >= len(a) and rem[-1] == 0:
            rem = trim(rem)
        if len(rem) == 1 and rem[0] == 0:
            break
        if len(rem) < len(d):
            break
    return trim(quo), trim(rem)


def sturm_count(poly, a, bnd):
    """Number of distinct real roots of poly in (a, bnd]."""
    seq = [trim(poly), pder(poly)]
    while len(seq[-1]) > 1 or seq[-1][0] != 0:
        _, rem = pdivmod(seq[-2], seq[-1])
        if len(rem) == 1 and rem[0] == 0:
            break
        seq.append(pneg(rem))
        if len(seq[-1]) == 1:
            break

    def changes(x):
        vals = [peval(s, x) for s in seq]
        vals = [v for v in vals if v != 0]
        return sum(1 for i in range(len(vals) - 1) if (vals[i] < 0) != (vals[i + 1] < 0))
    return changes(a) - changes(bnd), len(seq)


def integerize(a):
    from math import lcm, gcd
    L = 1
    for c in a:
        L = lcm(L, c.denominator)
    ints = [int(c * L) for c in a]
    G = 0
    for c in ints:
        G = gcd(G, abs(c))
    ints = [c // G for c in ints]
    if ints[-1] < 0:
        ints = [-c for c in ints]
    return ints


R = [Fr(0), Fr(1)]                     # the polynomial r
A = padd(R, [-ell])                    # r - ell
Ntau = [2 * cH * 0 - ell ** 2 + p ** 2, 2 * cH]          # 2 r cH - ell^2 + p^2
Dtau = [-ell ** 2, 2 * h, Fr(-1)]                          # 2 r h - r^2 - ell^2
Bpol = padd(Dtau, pneg(Ntau))                              # D_tau - N_tau = 2r(h-cH) - r^2 - p^2

print("=" * 72)
print("1. The path lemma (Lemma A.4)")
print("=" * 72)
dtau = padd(pmul(pder(Ntau), Dtau), pneg(pmul(Ntau, pder(Dtau))))
print("  (a) N_tau' D_tau - N_tau D_tau' =", [str(c) for c in dtau], "(constant, r, r^2)")
print("      discriminant =", dtau[1] ** 2 - 4 * dtau[2] * dtau[0])
print(f"      tau(r0) = {tau(r0)} = {float(tau(r0)):.6f};  tau(r2) = {tau(r2)} = {float(tau(r2)):.6f};  "
      f"3/4 - tau(r2) = {Fr(3, 4) - tau(r2)}")
print(f"      tau(r1) = {tau(r1)};  tau(r0) - 1/2 = {float(tau(r0) - Fr(1, 2)):.6f}")

NJ = pmul(pmul(A, A), Bpol)
DJ = pmul([Fr(0), Fr(2)], Dtau)
QJ = padd(pmul(pder(NJ), DJ), pneg(pmul(NJ, pder(DJ))))
QJi = integerize(QJ)
print("  (b) J = N/D with N = (r-1)^2 (8r - r^2 - 1/4), D = 2r(20r - r^2 - 1)")
print("      N'D - ND' (integer, lowest terms, constant first):", QJi)
paper_QJ = [-1, 40, -614, -12, 743, -160, 4]
print("      paper's Q_J (constant first):                     ", paper_QJ, " same:", QJi == paper_QJ)
QJp = [Fr(c) for c in paper_QJ]
print(f"      Q_J(r0) = {peval(QJp, r0)} (registry QJ_r0 = 4634399/15625)")
cnt, ln = sturm_count(QJp, r0, r2)
print(f"      Sturm count of real roots of Q_J in (r0, r2]: {cnt} (Sturm sequence of length {ln})")
print(f"      J(r0) = {J(r0)} = {float(J(r0)):.6e};  k - J(r0) = {float(k - J(r0)):.6e}")
print(f"      rho J(r1) = {rho * J(r1)};  rho J(r1) - k = {rho * J(r1) - k}")
print(f"      rho J(r2) = {rho * J(r2)};  rho J(r2) - k = {rho * J(r2) - k} = {float(rho * J(r2) - k):.6f}")

NG = pmul(pmul(A, A), pmul(Bpol, Bpol))
DG = pmul([Fr(0), Fr(2)], pmul(Dtau, Dtau))
QG = padd(pmul(pder(NG), DG), pneg(pmul(NG, pder(DG))))
QGi = integerize(QG)
paper_QG = [-1, 80, -2685, 48456, -374607, -32808, 562917, -229344, 29256, -1280, 16]
print("  (c) G = Delta (1-tau)^2: N'D - ND' (integer, lowest terms, constant first):")
print("      ", QGi)
print("      paper's degree-10 polynomial:", paper_QG, " same:", QGi == paper_QG)
QGp = [Fr(c) for c in paper_QG]
cnt, ln = sturm_count(QGp, r0, Fr(2))
print(f"      value at r0 = {peval(QGp, r0)} = {float(peval(QGp, r0)):.4f};  value at 2 = {float(peval(QGp, Fr(2))):.4f}")
print(f"      Sturm count of real roots in (r0, 2]: {cnt} (Sturm sequence of length {ln})")
print(f"      for comparison, Sturm count in (r0, r2]: {sturm_count(QGp, r0, r2)[0]}")
print(f"      rho J(2) - k = {rho * J(Fr(2)) - k} (so r_J < 2)")

print("=" * 72)
print("2. The six marked strengths at the benchmark slot")
print("=" * 72)
print(f"  lambda = {mp.nstr(lam, 12)}, b = {mp.nstr(b, 12)}, u = {mp.nstr(u, 12)}, M = {mp.nstr(M, 12)}, m = {mp.nstr(m, 12)}")
loA, hiA, ok = bisect_exact(lambda r: J(r) - k, r0, r2)
rA = q((loA + hiA) / 2)
print(f"  r_A (J = k): exact bracket [{loA}, {hiA}]")
print(f"      width = {hiA-loA}; final signs (-,+): {ok}; values {mp.nstr(q(J(loA)-k), 8)}, {mp.nstr(q(J(hiA)-k), 8)}")
rF = frak(k * (2 + u))
rN = frak(2 * k / rho)
loJ, hiJ, okJ = bisect_exact(lambda r: rho * J(r) - k, r0, r2)
rJ = q((loJ + hiJ) / 2)
rS = frak(k * (2 + u) / rho)
Mh_c = M * q(h) - q(cH)
rC = (Mh_c + mp.sqrt(Mh_c ** 2 + M * ((1 - M) * q(ell) ** 2 - q(p) ** 2))) / M
print(f"  r_F = frak(k(2+u))     = frak({mp.nstr(k * (2 + u), 10)}) = {mp.nstr(rF, 10)}")
print(f"  r_N = frak(2k/rho)     = frak({float(2 * k / rho)}) = {mp.nstr(rN, 10)}"
      f"   [= 1.16 + sqrt(0.0256 + 0.32) = 1.16 + {mp.nstr(mp.sqrt(mp.mpf('0.3456')), 10)}]")
print(f"  r_J (rho J = k): exact bracket [{loJ}, {hiJ}]")
print(f"      width = {hiJ-loJ}; final signs (-,+): {okJ}; values {mp.nstr(q(rho*J(loJ)-k), 8)}, {mp.nstr(q(rho*J(hiJ)-k), 8)}")
print(f"  r_S = frak(k/(rho m))  = frak({mp.nstr(k * (2 + u) / rho, 10)}) = {mp.nstr(rS, 10)}")
print(f"  r_C = closed form      = {mp.nstr(rC, 10)};  Mh - c_H = {mp.nstr(Mh_c, 8)}, "
      f"M[(1-M)l^2 - p^2] = {mp.nstr(M * ((1 - M) - mp.mpf(1) / 4), 8)}")
print("  order r0 < rA < rF < rN < rJ < rS < r1 < rC < r2:",
      [mp.nstr(x, 7) for x in (q(r0), rA, rF, rN, rJ, rS, q(r1), rC, q(r2))])
print("  Lemma A.5 margins:")
print(f"    tau(r_A) = {mp.nstr(q(tau(Fr(loA))), 10)};  M - tau(r_A) = {mp.nstr(M - q(tau(Fr(loA))), 8)}")
print(f"    1 - rho/2 - M = {mp.nstr(1 - q(rho) / 2 - M, 8)} (r_F < r_N)")
tau_rN = (48 * rN - 3) / (4 * (20 * rN - rN ** 2 - 1))
print(f"    tau(r_N) - 1/2 = {mp.nstr(tau_rN - mp.mpf(1) / 2, 8)} (r_N < r_J)")
print(f"    tau(r_J) = {mp.nstr(q(tau(Fr(loJ))), 8)};  M - tau(r_J) = {mp.nstr(M - q(tau(Fr(loJ))), 8)} (r_J < r_S)")
print(f"    22/25 - M = {mp.nstr(mp.mpf(22) / 25 - M, 8)} (r_S < r_1)")
print(f"    M - tau(r1) = {mp.nstr(M - q(tau(r1)), 8)}, tau(r2) - M = {mp.nstr(q(tau(r2)) - M, 8)} (r1 < rC < r2)")
print(f"  Delta(r_A) = {mp.nstr(q(Delta(Fr(loA))), 8)}")

print("=" * 72)
print("3. Entry along the informative branch (prior 1/2)")
print("=" * 72)
rhoq, kq = q(rho), q(k)


def Dq(r):
    r = mp.mpf(r)
    return (r - 1) ** 2 / (2 * r)


def tauq(r):
    r = mp.mpf(r)
    return (48 * r - 3) / (4 * (20 * r - r ** 2 - 1))


def Jq(r):
    return Dq(r) * (1 - tauq(r))


def E_R(r):
    return rhoq + (1 - rhoq) * b * Dq(r) / (2 * kq)


E_F = rhoq + (1 - rhoq) * (b + lam / 2)


def E_T(r):
    return rhoq + b / 2 * (kq - rhoq * Jq(r)) / (Dq(r) * (1 - tauq(r)) ** 2)


tauA = tauq(rA)
print(f"  at r_A: rho + (1-rho) b/(2(1-tau_A)) = {mp.nstr(rhoq + (1 - rhoq) * b / (2 * (1 - tauA)), 8)};"
      f"  E_R(r_A) = {mp.nstr(E_R(rA), 8)};  E_T(r_A) = {mp.nstr(E_T(rA), 8)}")
for r in ("1.40", "1.45"):
    print(f"  R at r = {r}: s_R = b(Delta/k - 2) = {mp.nstr(b * (Dq(r) / kq - 2), 8)};  entry = {mp.nstr(E_R(r), 8)}")
print(f"  at r_F: b Delta(r_F)/(2k) = {mp.nstr(b * Dq(rF) / (2 * kq), 10)}; b + lambda/2 = {mp.nstr(b + lam / 2, 10)}")
print(f"  F plateau entry rho + (1-rho)(b + lambda/2) = {mp.nstr(E_F, 10)}")
print("  threshold pair T (rule CM):")
for r in ("1.55", "1.60", "1.65"):
    estar = kq / Jq(r)
    sstar = b * (2 * tauq(r) - 1) / (1 - tauq(r))
    print(f"    r = {r}: s* = {mp.nstr(sstar, 8)}, e* = k/J = {mp.nstr(estar, 8)}, entry E_T = {mp.nstr(E_T(r), 8)}")
print(f"    E_T(r_J) = {mp.nstr(E_T(rJ), 8)} (should be rho)")
print("  minimum formula rho + (1-rho) min{b Delta/(2k), b + lambda/2} on a grid:")
for r in ("1.40", "1.42", "1.45", "1.4671", "1.50", "1.60", "1.70", "1.74"):
    val = rhoq + (1 - rhoq) * min(b * Dq(r) / (2 * kq), b + lam / 2)
    print(f"    r = {r}: {mp.nstr(val, 8)}")

print("=" * 72)
print("4. Direct check of each listed tuple at sample strengths (rules IM, C1)")
print("=" * 72)


def tuple_check(r, s, t, rule_cm_e1=None):
    """Build the tuple from rates s (purchase) and t (sale) at prior 1/2 and report
    each condition: posteriors, C1 entry, gross returns against k."""
    r = mp.mpf(r)
    D, ta = Dq(r), tauq(r)
    fH = {-1: b, 0: b0 + lam - s, 1: b + s}
    fL = {-1: b + t, 0: b0 + lam - t, 1: b}
    mu = {x: fH[x] / (fH[x] + fL[x]) for x in (-1, 0, 1)}
    e = {x: (1 if mu[x] >= ta else rhoq) for x in (-1, 0, 1)}
    if rule_cm_e1 is not None:
        e[1] = rule_cm_e1
    KH = e[1] * D * (1 - mu[1])
    KL = e[-1] * D * mu[-1]

    def ok_rate(rate, K):
        if rate == 0:
            return K <= kq
        if abs(rate - lam) < mp.mpf(10) ** -30:
            return K >= kq
        return abs(K - kq) < mp.mpf(10) ** -30
    return mu, e, KH, KL, ok_rate(s, KH), ok_rate(t, KL)


samples = ["1.30", "1.42", "1.60", "1.85", "2.05", "2.50", "3.59", "3.60"]
for rs in samples:
    r = mp.mpf(rs)
    D = Dq(r)
    sR = b * (D / kq - 2)
    sQ = b * (rhoq * D / kq - 2)
    tlow = 0 if rhoq * D / 2 <= kq else (lam if rhoq * D * m >= kq else b * (rhoq * D / kq - 2))
    forms = {"N": 0, "R": sR, "F": lam, "Q": sQ}
    line = []
    for name, s in forms.items():
        if not (0 <= s <= lam):
            continue
        mu, e, KH, KL, okH, okL = tuple_check(r, s, tlow)
        # Q needs the purchase posterior below tau; R needs it above tau
        extra = True
        if name == "Q":
            extra = mu[1] < tauq(r) and s > 0
        if name == "R":
            extra = mu[1] > tauq(r) and 0 < s < lam
        if name == "N":
            extra = (tlow == 0)
        if okH and okL and extra:
            PrX = {x: ((b if x == -1 else (b0 + lam - s if x == 0 else b + s)) +
                       (b + tlow if x == -1 else (b0 + lam - tlow if x == 0 else b))) / 2 for x in (-1, 0, 1)}
            Ent = sum(PrX[x] * e[x] for x in (-1, 0, 1))
            line.append(f"{name} (entry {mp.nstr(Ent, 6)})")
    print(f"  r = {rs}: low-class sale rate t = {mp.nstr(tlow, 6)};  equilibria found: {', '.join(line)}")

print("=" * 72)
print("5. Other priors (Corollary A.2)")
print("=" * 72)
piA_lo = tauA / (tauA + (1 - tauA) * (1 + u))
print(f"  tau_A = pi_A^hi = {mp.nstr(tauA, 10)};  pi_A^lo = tau_A/(tau_A + (1-tau_A)(1+u)) = {mp.nstr(piA_lo, 10)}")
lo_s, hi_s, ok_s = bisect_exact(lambda r: rho * Delta(r) * tau(r) - k, r0, r2)
rstar = q((lo_s + hi_s) / 2)
pimax = tauq(rstar)
print(f"  r_* (rho Delta tau = k) = {mp.nstr(rstar, 10)};  pi_max = tau(r_*) = {mp.nstr(pimax, 10)}")
Mpi = pimax * (1 + u) / (pimax * (1 + u) + 1 - pimax)
mu0 = 1 / (1 + (1 - pimax) / pimax * (b0 + lam) / b0)
print(f"  at pi_max: M(pi) = {mp.nstr(Mpi, 8)};  zero-order posterior (high class buys fully, low class abstains) = {mp.nstr(mu0, 8)}")
print(f"  full purchase return Delta(r_*)(1 - M(pi)) - k = {mp.nstr(Dq(rstar) * (1 - Mpi) - kq, 8)};  "
      f"entry rho + (1-rho)(b + pi lambda) = {mp.nstr(rhoq + (1 - rhoq) * (b + pimax * lam), 8)}")
print(f"  3/4 - tau_A = {mp.nstr(mp.mpf(3) / 4 - tauA, 8)}")
for pi in ("0.30", "0.396", "0.45", "0.50", "0.60", "0.645", "0.66"):
    pi = mp.mpf(pi)
    Mp = pi * (1 + u) / (pi * (1 + u) + 1 - pi)
    rNp = frak(k / (rho * max(pi, 1 - pi)))
    # r_C(pi): largest r on the path with tau(r) <= M(pi)
    if tauq(r0) > Mp:
        rCp = None
    elif tauq(r2) <= Mp:
        rCp = q(r2)
    else:
        rCp = bisect_mp(lambda r: tauq(r) - Mp, q(r0), q(r2))
    if pi < tauq(r0):
        start = rA
        kind = "[r_A,"
    elif pi <= tauq(r2):
        start = bisect_mp(lambda r: tauq(r) - pi, q(r0), q(r2))
        kind = "(r_pi,"
    else:
        start = None
    if rCp is None or start is None:
        print(f"  pi = {mp.nstr(pi, 4)}: C(pi) empty (no strength with tau <= M(pi) or no strength with pi < tau)")
        continue
    lo = max(start, rA)
    hi = min(rNp, rCp)
    if lo > hi or (lo == hi and kind == "(r_pi,"):
        print(f"  pi = {mp.nstr(pi, 4)}: C(pi) empty (start {mp.nstr(lo, 6)} > end {mp.nstr(hi, 6)})")
    else:
        print(f"  pi = {mp.nstr(pi, 4)}: C(pi) = {kind if lo == start else '[r_A,'} {mp.nstr(lo, 6)} ... {mp.nstr(hi, 6)}]"
              f"  (r_N(pi) = {mp.nstr(rNp, 6)}, r_C(pi) = {mp.nstr(rCp, 6)})")

print("=" * 72)
print("6. Tie rules: the low class on (r_N, r_S] under rule I0")
print("=" * 72)
for rs in ("1.80", "2.00", "2.12"):
    D = Dq(rs)
    print(f"  r = {rs}: rho Delta/2 = {mp.nstr(rhoq * D / 2, 6)} > k = 0.02;  rho Delta m = {mp.nstr(rhoq * D * m, 6)} <= k"
          f"  -> abstention fails, a full sale fails, a mixture needs rule IM")
