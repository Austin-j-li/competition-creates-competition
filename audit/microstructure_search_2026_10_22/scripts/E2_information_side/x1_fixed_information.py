"""X1: the fixed-information control (Prop. A.3) with the order slot. Print only.

Frozen profile: full orders (q_H, q_L) = (1, -1) at every strength; the challenger and the market
maker re-optimize. The slot experiment is the order Q in {-1, 0, 1} with
  Pr(Q=1|H) = b + lam, Pr(Q=1|L) = b, Pr(Q=0|j) = c, Pr(Q=-1|H) = b, Pr(Q=-1|L) = b + lam.
Atomic costs {0, c_H} (C1: prepare at indifference) and, as a second case, the declared atomless law.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from mpmath import mp, mpf, sqrt
from common import EXACT, MP, show, auction, B, tau, bounds, calibration_A, calibration_B, laplace_full_order_entry


def frozen(F, S, r, pi="1/2", rho="1/4", cH=6, cost="atomic", eps="1/10"):
    pi, rho, cH, eps = F(pi), F(rho), F(cH), F(eps)
    A = auction(F, r)
    lam, b, c = S["lam"], S["b"], S["c"]
    law = {1: (b + lam, b), 0: (c, c), -1: (b, b + lam)}  # (Pr(Q|H), Pr(Q|L))
    eH = eL = F(0)
    rows = []
    for q, (pH, pL) in law.items():
        mu = pi * pH / (pi * pH + (1 - pi) * pL)
        gross = B(A, mu)
        if cost == "atomic":
            e = rho + (1 - rho) * (1 if gross >= cH else 0)
        else:  # rho * U[0, 2 eps] + (1 - rho) * U[cH - eps, cH + eps]
            low = min(max(gross / (2 * eps), F(0)), F(1))
            high = min(max((gross - (cH - eps)) / (2 * eps), F(0)), F(1))
            e = rho * low + (1 - rho) * high
        eH += pH * e
        eL += pL * e
        rows.append((q, mu, gross, e))
    E = pi * eH + (1 - pi) * eL
    OH = pi * eH  # W_H = 1 because h exceeds the incumbent support
    RT = A["t0"] + pi * eH * A["wH"] + (1 - pi) * eL * A["wL"]
    return dict(A=A, rows=rows, E=E, eH=eH, eL=eL, OH=OH, RT=RT)


def strict_set_probability(F, S, r0, r1, pi="1/2", rho="1/4", cH=6):
    """Pr{ B_{r1}(mu(Q)) < C <= B_{r0}(mu(Q)) } under frozen full orders and atomic costs (Prop. A.3)."""
    pi, rho, cH = F(pi), F(rho), F(cH)
    A0, A1 = auction(F, r0), auction(F, r1)
    lam, b, c = S["lam"], S["b"], S["c"]
    tot = F(0)
    for pH, pL in ((b + lam, b), (c, c), (b, b + lam)):
        prob = pi * pH + (1 - pi) * pL
        mu = pi * pH / prob
        lo, hi = B(A1, mu), B(A0, mu)
        pc = (rho if lo < 0 <= hi else 0) + ((1 - rho) if lo < cH <= hi else 0)
        tot += prob * pc
    return tot


def main():
    print("=" * 100)
    print("X1. Threshold beliefs tau(r) = (c_H - g_L)/(g_H - g_L) at the benchmark (c_H = 6)")
    for r in (1, Fr(6, 5), Fr(3), Fr(18, 5)):
        if r == 1:
            print("   r -> 1: tau = 45/72 = 5/8 (limit of (48r-3)/(4(20r-r^2-1)))")
            continue
        print(f"   r = {r}: tau = {show(tau(auction(EXACT, r), EXACT(6)))}")
    print("   d tau/dr has numerator 4(48 r^2 - 6 r + 12) > 0 (no real root), so tau rises in r; tau > 5/8 > 1/2.")

    SA = calibration_A()
    SB, _ = calibration_B()
    for label, F, S in (("A (exact)", EXACT, SA), ("B (40 digits)", MP, SB)):
        m, M = bounds(S["u"], F(Fr(1, 2)))
        print("=" * 100)
        print(f"Calibration {label}: m = {show(m)}, M = {show(M)}")
        for cost in ("atomic", "atomless"):
            print(f"-- frozen full orders, cost law: {cost}")
            for r in (Fr(6, 5), Fr(3), Fr(18, 5)):
                out = frozen(F, S, F(r), cost=cost)
                post = ", ".join(f"Q={q}: mu={show(mu, 8)}, B={show(g, 8)}, e={show(e, 8)}" for q, mu, g, e in out["rows"])
                print(f"   r = {r}: E = {show(out['E'])}, O_H = {show(out['OH'])}, R_T = {show(out['RT'], 10)}")
                print(f"      {post}")
        # The frozen profile is not an investor equilibrium at r = 1.2 (full orders lose there)
        A12 = auction(F, F(Fr(6, 5)))
        k = F(Fr(1, 50))
        out12 = frozen(F, S, F(Fr(6, 5)))
        eQ = {q: e for q, mu, g, e in out12["rows"]}
        print(f"   frozen profile at r = 6/5: class-H buy nets e(M) Delta_T (1 - M) - k = {show(eQ[1] * A12['D'] * (1 - M) - k)}; "
              f"class-L sale nets e(m) Delta_T m - k = {show(eQ[-1] * A12['D'] * m - k)}")
        p_strict = strict_set_probability(F, S, F(Fr(6, 5)), F(3))
        print(f"   Prop. A.3 strictness set, r0 = 6/5 -> r1 = 3, atomic costs: probability = {show(p_strict)}")
        p_strict2 = strict_set_probability(F, S, F(3), F(Fr(18, 5)))
        print(f"   Prop. A.3 strictness set, r1 = 3 -> r2 = 18/5, atomic costs: probability = {show(p_strict2)}")
        # The only step of frozen entry: tau(r) = M at r_C(M)
        Mm = mpf(M.numerator) / M.denominator if isinstance(M, Fr) else M
        rC = (10 * Mm - 6 + sqrt((10 * Mm - 6) ** 2 + Mm * (mpf(3) / 4 - Mm))) / Mm
        print(f"   frozen entry is constant on (1, r_C] and equals rho above; r_C(M) = {mp.nstr(rC, 15)}")

    print("=" * 100)
    print("Laplace cross-check (paper Table 2, Panel B): frozen full orders, prior 1/2, b = 2")
    for r in (Fr(6, 5), Fr(3)):
        E_lap, eH, eL, xs = laplace_full_order_entry(tau(auction(MP, MP(r)), MP(6)), MP("0.25"))
        print(f"   r = {r}: E = {mp.nstr(E_lap, 12)}, O_H = {mp.nstr(eH / 2, 12)}, x* = {mp.nstr(xs, 12)}")
    print("   (paper: 0.562178 and 0.350606 at r = 1.2; 0.522757 and 0.324192 at r = 3)")


if __name__ == "__main__":
    main()
