"""Exact sign certificates for Proposition 3 at the benchmark auction (print only).

1. The closed-form auction objects equal direct integration over R ~ U[0, r].
2. tau is strictly increasing on [6/5, 18/5].
3. J(r) = Delta(r)(1 - tau(r)) is strictly increasing on [6/5, 18/5] (Sturm count).
4. Delta(r)(1 - tau(r))^2 is strictly increasing on [6/5, 2] (Sturm count).
5. Delta(r) tau(r) is strictly increasing on [6/5, 18/5].
6. Rational brackets for r_A (J = k), r_J (rho J = k), r_star (rho Delta tau = k), printed outward.
7. The ordering r_0 < r_A < r_N < r_J < r_1 and the slot-dependent orderings as bounds on M.
Run from the repository root:
  .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_certificates.py
"""
from fractions import Fraction as Fr

from p1_common import (HERE, Log, auction, auction_by_integration, tau, Delta, J, B,
                       h, ell, p, rho, cH, k, r0, r1, r2,
                       pmul, psub, pder, peval, roots_in, pstr, ptrim,
                       TAU_NUM, TAU_DEN, ONE_MINUS_TAU_NUM, DELTA_NUM, DELTA_DEN,
                       bisect_root, qbrstr, round_dec)


def dd(x, places=12):
    """Nearest decimal of an exact rational (a display, not an enclosure)."""
    return round_dec(x, places)


def sg(x):
    return "+" if x > 0 else "-" if x < 0 else "0"

log = Log(HERE / "p1_certificates.log")
log("P1_core certificates: exact rational arithmetic (fractions.Fraction) only.")
log("Benchmark: h, ell, p, rho, c_H, k =", h, ell, p, rho, cH, k, "; path [r0, r2] =", r0, r2)

# 1. closed forms against direct integration
log("\n1. Auction objects: closed form minus direct integration (must print 0 everywhere)")
for r in [r0, Fr(7, 5), Fr(31, 20), Fr(8, 5), Fr(33, 20), Fr(2), r1, r2]:
    a, d = auction(r), auction_by_integration(r)
    diffs = {key: a[key] - d[key] for key in ("t0", "tH", "tL", "gH", "gL", "D")}
    log(f"   r = {r}: " + ", ".join(f"{key} {v}" for key, v in diffs.items()),
        f"| t_H + g_H - h = {a['tH'] + a['gH'] - h}, t_L + g_L - ell = {a['tL'] + a['gL'] - ell}")

def quotient_derivative_numerator(num, den):
    """Sign of (num/den)' equals the sign of num' den - num den' where den != 0."""
    return psub(pmul(pder(num), den), pmul(num, pder(den)))

def integer_form(poly):
    """Scale by the least common denominator so that the coefficients are integers."""
    from math import lcm
    d = 1
    for c in poly:
        d = lcm(d, Fr(c).denominator)
    return [c * d for c in poly], d


def certify_positive(poly, lo, hi, name):
    n = roots_in(poly, lo, hi)
    v = peval(poly, lo)
    ipoly, d = integer_form(poly)
    log(f"   {name}: polynomial {pstr(poly)}")
    log(f"   integer form ({d} x polynomial), highest degree first: "
        + " ".join(f"{int(c):+d}r^{i}" for i, c in reversed(list(enumerate(ipoly)))))
    log(f"   integer form at {lo} = {peval(ipoly, lo)}")
    log(f"   value at {lo} = {v} (sign {'+' if v > 0 else '-' if v < 0 else '0'});"
        f" Sturm count of real roots in ({lo}, {hi}] = {n}")
    log(f"   => {'POSITIVE on [' + str(lo) + ', ' + str(hi) + ']' if (n == 0 and v > 0) else 'NOT CERTIFIED'}")
    return n == 0 and v > 0

# denominators stay positive on the path
log("\n   Denominators: tau denominator 2rh - r^2 - ell^2 and 2r on the path")
certify_positive(TAU_DEN, r0, r2, "2rh - r^2 - ell^2")
certify_positive(ONE_MINUS_TAU_NUM, r0, r2, "2r(h - c_H) - r^2 - p^2 (numerator of 1 - tau)")

# 2. tau increasing
log("\n2. tau(r) = (2 r c_H - ell^2 + p^2) / (2 r h - r^2 - ell^2) is strictly increasing")
tau_prime = quotient_derivative_numerator(TAU_NUM, TAU_DEN)
certify_positive(tau_prime, r0, r2, "numerator of tau'")
log("   tau(6/5) =", tau(r0), "=", dd(tau(r0)), "; tau(3) =", tau(r1), "; tau(18/5) =", tau(r2),
    "=", dd(tau(r2)))
log("   tau(6/5) - 1/2 =", tau(r0) - Fr(1, 2), "> 0, so the prior 1/2 never recruits on the path.")

# 3. J increasing
log("\n3. J(r) = Delta(r)(1 - tau(r)) is strictly increasing on [6/5, 18/5]")
J_num = pmul(DELTA_NUM, ONE_MINUS_TAU_NUM)
J_den = pmul(DELTA_DEN, TAU_DEN)
log("   J = [", pstr(J_num), "] / [", pstr(J_den), "]")
for r in [r0, Fr(2), r1, r2]:
    log(f"   check J({r}): polynomial form {peval(J_num, r) / peval(J_den, r)} vs direct {J(r)}")
certify_positive(quotient_derivative_numerator(J_num, J_den), r0, r2, "numerator of J'")
log("   J(6/5) =", J(r0), "=", dd(J(r0)), "< k;  J(18/5) =", J(r2), "=", dd(J(r2)))
log("   rho J(6/5) =", rho * J(r0), "< k;  rho J(18/5) =", rho * J(r2), "=", dd(rho * J(r2)), "> k")
log("   k - J(6/5) =", k - J(r0), "; rho J(18/5) - k =", rho * J(r2) - k, "; rho J(2) - k =", rho * J(Fr(2)) - k,
    "(so r_J < 2); rho J(3) - k =", rho * J(r1) - k)

# 4. Delta (1 - tau)^2 increasing on [6/5, 2]
log("\n4. Delta(r)(1 - tau(r))^2 is strictly increasing on [6/5, 2]")
S_num = pmul(DELTA_NUM, pmul(ONE_MINUS_TAU_NUM, ONE_MINUS_TAU_NUM))
S_den = pmul(DELTA_DEN, pmul(TAU_DEN, TAU_DEN))
certify_positive(quotient_derivative_numerator(S_num, S_den), r0, Fr(2), "numerator of (Delta (1-tau)^2)'")

# 5. Delta tau increasing
log("\n5. Delta(r) tau(r) is strictly increasing on [6/5, 18/5] (both factors positive and increasing)")
T_num = pmul(DELTA_NUM, TAU_NUM)
T_den = pmul(DELTA_DEN, TAU_DEN)
certify_positive(quotient_derivative_numerator(T_num, T_den), r0, r2, "numerator of (Delta tau)'")
certify_positive(TAU_NUM, r0, r2, "numerator of tau")

# 6. root brackets
log("\n6. Root brackets by exact bisection (width <= 1e-40); the two end values have opposite signs.")
log("   Brackets print outward: the lower end rounds down, the upper end rounds up.")
rA = bisect_root(lambda r: J(r) - k, r0, r2)
rJ = bisect_root(lambda r: rho * J(r) - k, r0, r2)
rS = bisect_root(lambda r: rho * Delta(r) * tau(r) - k, r0, r2)
for name, br, fn in (("r_A: J(r) - k", rA, "J - k"), ("r_J: rho J(r) - k", rJ, "rho J - k"),
                     ("r_star: rho Delta(r) tau(r) - k", rS, "rho Delta tau - k")):
    lo, hi, flo, fhi = br
    log(f"   {name}: {qbrstr(lo, hi, 45)}; signs of {fn} at the ends: {sg(flo)}, {sg(fhi)}")
tA_lo, tA_hi = tau(rA[0]), tau(rA[1])
tJ_lo, tJ_hi = tau(rJ[0]), tau(rJ[1])
tS_lo, tS_hi = tau(rS[0]), tau(rS[1])
log(f"   tau(r_A) in {qbrstr(tA_lo, tA_hi)} (tau increasing)")
log(f"   tau(r_J) in {qbrstr(tJ_lo, tJ_hi)}")
log(f"   pi_max = tau(r_star) in {qbrstr(tS_lo, tS_hi)}")
log(f"   Delta(r_A) in {qbrstr(Delta(rA[0]), Delta(rA[1]))} (Delta increasing)")

# 7. orderings
log("\n7. Orderings of the thresholds")
# r_N = (29 + 6 sqrt 6)/25; rational bracket from sqrt(6) bounds
s6_lo, s6_hi = Fr(2449489742783178, 10**15), Fr(2449489742783179, 10**15)
log("   sqrt(6) bracket check:", s6_lo**2 < 6 < s6_hi**2)
rN_lo, rN_hi = (29 + 6 * s6_lo) / 25, (29 + 6 * s6_hi) / 25
log(f"   r_N = (29 + 6 sqrt 6)/25 in {qbrstr(rN_lo, rN_hi, 15)};"
    f" signs of rho Delta(r_N)/2 - k at the ends: {sg(rho*Delta(rN_lo)/2-k)}, {sg(rho*Delta(rN_hi)/2-k)}")
log("   r_0 < r_A:  J(r_0) - k =", J(r0) - k, "< 0")
log("   r_A < r_N:  tau(r_A) < 1 - rho, since 3/4 - tau(r_A) >=", dd(Fr(3, 4) - tA_hi), "> 0; then rho Delta(r_A) =",
    "rho k/(1 - tau(r_A)) < k. Direct check J(r_N_lo) - k =", dd(J(rN_lo) - k), "> 0")
log("   r_N < r_J:  rho J(r_N_hi) - k =", dd(rho * J(rN_hi) - k), "< 0 (J increasing)")
log("   r_J < r_1:  rho J(3) - k =", rho * J(r1) - k, "> 0")
M_lo, M_hi = tau(r1), tau(r2)
log("   Band: M in (tau(3), tau(18/5)) = (", M_lo, ",", M_hi, ")")
log("   r_A < r_F  <=>  M > tau(r_A):  tau(r_A_hi) - M_lo =", dd(tA_hi - M_lo), "< 0, so it holds on the band")
log("   r_F < r_N  <=>  M < 1 - rho/2 = 7/8:  M_hi - 7/8 =", M_hi - Fr(7, 8), "< 0")
log("   r_J < r_S  <=>  M > tau(r_J):  tau(r_J_hi) - M_lo =", dd(tJ_hi - M_lo), "< 0")
log("   r_S < r_1  <=>  M < 1 - k/(rho Delta(3)) =", 1 - k / (rho * Delta(r1)), ": M_hi - 22/25 =", M_hi - Fr(22, 25), "< 0")
log("   r_1 < r_C < r_2  <=>  tau(3) < M < tau(18/5): the band itself.")
log("   pi_A_hi = tau(r_A) < pi_max = tau(r_star) <=> r_A < r_star: rho Delta(r_A) tau(r_A) - k <=",
    dd(rho * Delta(rA[1]) * tA_hi - k), "< 0")
log("   r_star < r_N: rho Delta(r_N_lo) tau(r_N_lo) - k =", dd(rho * Delta(rN_lo) * tau(rN_lo) - k), "> 0")
log("   3/4 - tau(18/5) =", Fr(3, 4) - tau(r2), "> 0, so M < 3/4 on the band")
gmin = h - r2 / 2 - ell * ell / (2 * r2)
log("   g_H - g_L = h - r/2 - ell^2/(2r) decreases for r > ell; its value at 18/5 is", gmin, "> 0")
log("   Delta increases for r > ell; Delta(6/5) =", Delta(r0), "> 0")
log.close()
