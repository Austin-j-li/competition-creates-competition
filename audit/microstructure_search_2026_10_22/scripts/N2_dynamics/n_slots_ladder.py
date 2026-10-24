"""N2, extension A: n order slots with fresh informed arrivals, decision after the last slot.

Each slot: with probability lam a fresh informed investor (sees the class) fills it; else a liquidity
trader sells, waits, buys with probabilities (beta, 1 - 2 beta, beta). Under full informed orders
(class H buys, class L sells) the posterior odds after n slots are (1 + u)^D, with D the net imbalance.

Print-only. Exact quantities use fractions.Fraction; mpmath (40 digits) is used only for irrational
strip endpoints, the u-sweep, the binomial tail bounds, and Poisson sums. Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N2_dynamics/n_slots_ladder.py
"""
import sys
import os
from fractions import Fraction as F
from math import comb, factorial

import mpmath

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n2_common import (RHO, K, R0, R1, R2, MID, objects, direct_objects, B, CH, dec, head)  # noqa: E402

mpmath.mp.dps = 40

O3, O36, O12 = objects(R1), objects(R2), objects(R0)
T1 = O3["tau"] / (1 - O3["tau"])      # odds threshold at r = 3
T2 = O36["tau"] / (1 - O36["tau"])    # odds threshold at r = 3.6
L1 = mpmath.log(mpmath.mpf(T1.numerator) / T1.denominator)
L2 = mpmath.log(mpmath.mpf(T2.numerator) / T2.denominator)


def slot_law(u, beta):
    """Per-slot order law (plus, zero, minus) under H and under L at full informed orders."""
    lam = u * beta / (1 + u * beta)
    b = (1 - lam) * beta
    c0 = (1 - lam) * (1 - 2 * beta)
    return lam, b, c0, (lam + b, c0, b), (b, c0, lam + b)


def tail_D(law, n, d):
    """P(N_plus - N_minus >= d) after n i.i.d. slots with law (p+, p0, p-). Exact if the law is exact."""
    pp, p0, pm = law
    tot = 0 * pp
    for npl in range(n + 1):
        for nmi in range(n - npl + 1):
            if npl - nmi >= d:
                n0 = n - npl - nmi
                tot += comb(n, npl) * comb(n - npl, nmi) * pp ** npl * pm ** nmi * p0 ** n0
    return tot


def dstar(u):
    """Smallest net imbalance whose posterior odds (1+u)^D reach T1 (C1 tie rule)."""
    d, z = 0, 1
    while z < T1:
        d += 1
        z *= (1 + u)
    return d


def dstar_mp(u):
    return int(mpmath.ceil(L1 / mpmath.log(1 + u)))


def rC(M):
    """Entry ceiling for a top posterior M: the root of B_r(M) = c_H (T2 memo equation (24))."""
    M = mpmath.mpf(M.numerator) / M.denominator if isinstance(M, F) else mpmath.mpf(M)
    return ((10 * M - 6) + mpmath.sqrt((10 * M - 6) ** 2 + M * (mpmath.mpf(3) / 4 - M))) / M


def main():
    head("A. Auction objects: closed forms against direct integration")
    for r in (R0,) + MID + (R1, R2):
        o, d = objects(r), direct_objects(r)
        diff = max(abs(o[key] - d[key]) for key in ("t0", "tH", "tL", "gH", "gL"))
        print(f"  r = {str(r):6s}  Delta = {str(o['D']):10s} tau = {str(o['tau']):12s} (~{dec(o['tau'], 6)})"
              f"  wL = {str(o['wL']):8s}  max |closed - direct| = {diff}")
    print(f"  odds threshold at 3:   T1 = {T1}  (log = {mpmath.nstr(L1, 12)})")
    print(f"  odds threshold at 3.6: T2 = {T2}  (log = {mpmath.nstr(L2, 12)})")
    print(f"  ratio L1/L2 = {mpmath.nstr(L1 / L2, 12)}")
    g_bar = mpmath.findroot(lambda r: 10 - r / 2 - mpmath.mpf(1) / (8 * r) - 6, 7.9)
    print(f"  revelation ceiling (g_H(r) = c_H): r = {mpmath.nstr(g_bar, 12)}  (exact (32 + sqrt(1008))/8)")

    head("B. Uniform margins used in the proofs (exact)")
    print(f"  Delta(6/5) - k = {O12['D'] - K}  (< 0: no informed trade at r_0 under any schedule)")
    for r, o in ((R1, O3), (R2, O36)):
        m = RHO * o["D"] * (1 - O36["tau"]) - K
        print(f"  r = {r}: rho Delta (1 - tau(3.6)) - k = {m}  (~{dec(m, 6)})  > 0: full orders forced")
    for r in MID:
        o = objects(r)
        print(f"  r = {r}: rho Delta / 2 - k = {RHO * o['D'] / 2 - K}  (<= 0: no trade is an equilibrium)")

    head("C. The strip for n slots: L1 <= n log(1+u) < L2; knobs at beta = 1/3")
    print("   n   u_low          u_high         lam_low(b=1/3) lam_high(b=1/3) D* at top  D=n-1 recruits?")
    for n in range(1, 13):
        ul = mpmath.e ** (L1 / n) - 1
        uh = mpmath.e ** (L2 / n) - 1
        lam_l, lam_h = ul / (3 + ul), uh / (3 + uh)
        dtop = int(mpmath.ceil(n * L1 / L2))
        print(f"  {n:2d}  {mpmath.nstr(ul, 10):14s} {mpmath.nstr(uh, 10):14s} {mpmath.nstr(lam_l, 8):14s} "
              f"{mpmath.nstr(lam_h, 8):15s} {dtop:4d}       {'yes' if dtop <= n - 1 else 'no'}")
    print("  n * u_high -> L2 =", mpmath.nstr(L2, 10), "; n * u_low -> L1 =", mpmath.nstr(L1, 10))

    head("D. Entry at r = 3 under full orders on the strip (sup over u; beta = 1/3 and beta -> 1/2)")
    print("   n   sup E_n(3), beta=1/3    sup E_n(3), beta->1/2    extra entry ratio to n=1 (beta=1/3)")
    base = None
    sups = {}
    for n in range(1, 13):
        row = []
        for beta in (mpmath.mpf(1) / 3, mpmath.mpf(1) / 2):
            ul = mpmath.e ** (L1 / n) - 1
            uh = mpmath.e ** (L2 / n) - 1
            best = mpmath.mpf(0)
            steps = 400
            for i in range(steps + 1):
                u = ul + (uh - ul) * i / steps
                if i == steps:
                    u = uh * (1 - mpmath.mpf(10) ** -30)
                _, _, _, lh, ll = slot_law(u, beta)
                d = dstar_mp(u)
                e = mpmath.mpf(1) / 4 + mpmath.mpf(3) / 4 * (tail_D(lh, n, d) + tail_D(ll, n, d)) / 2
                best = max(best, e)
            row.append(best)
        sups[n] = row
        if base is None:
            base = row[0] - mpmath.mpf(1) / 4
        print(f"  {n:2d}  {mpmath.nstr(row[0], 10):22s} {mpmath.nstr(row[1], 10):24s} "
              f"{mpmath.nstr((row[0] - mpmath.mpf(1) / 4) / base, 8)}")

    head("E. Exact rational points on the strip (beta = 1/3), full orders, r = 3")
    pts = {1: F(18, 11), 2: F(3, 5), 3: F(3, 8), 4: F(27, 100), 5: F(21, 100), 6: F(17, 100), 8: F(13, 100),
           10: F(1, 10), 12: F(17, 200)}
    for n, u in pts.items():
        lam, b, c0, lh, ll = slot_law(u, F(1, 3))
        top = (1 + u) ** n
        inside = (T1 <= top < T2)
        d = dstar(u)
        ph, pl = tail_D(lh, n, d), tail_D(ll, n, d)
        e3 = RHO + (1 - RHO) * (ph + pl) / 2
        Mn = top / (1 + top)
        print(f"  n = {n:2d}, u = {str(u):7s} lam = {str(lam):9s} on strip: {inside};  M_n = {dec(Mn, 6)};"
              f"  D* = {d};  E_n(3) = {dec(e3, 8)}")
        if n <= 2:
            print(f"        exact E_n(3) = {e3};  P_H(D>=D*) = {ph};  P_L(D>=D*) = {pl}")

    head("F. Decay of extra entry: binomial tail and Chernoff bound (beta <= 1/2, any u on the strip)")
    print("  extra entry <= (1-rho) P(Bin(n, p_n) >= ceil(theta n)), p_n = (1+u_high)/(2+u_high),"
          " theta = L1/L2")
    theta = L1 / L2
    for n in (1, 2, 4, 6, 8, 10, 12, 16, 20, 30, 40):
        uh = mpmath.e ** (L2 / n) - 1
        p = (1 + uh) / (2 + uh)
        m = int(mpmath.ceil(theta * n))
        tail = mpmath.fsum(mpmath.binomial(n, j) * p ** j * (1 - p) ** (n - j) for j in range(m, n + 1))
        th = mpmath.mpf(m) / n
        kl = th * mpmath.log(th / p) + ((1 - th) * mpmath.log((1 - th) / (1 - p)) if th < 1 else 0)
        print(f"  n = {n:2d}: p_n = {mpmath.nstr(p, 8)}, ceil(theta n) = {m:2d}, (1-rho)*tail = "
              f"{mpmath.nstr(mpmath.mpf(3) / 4 * tail, 8):12s} Chernoff (1-rho)exp(-n KL) = "
              f"{mpmath.nstr(mpmath.mpf(3) / 4 * mpmath.e ** (-n * kl), 8)}")
    half = mpmath.mpf(1) / 2
    rate = theta * mpmath.log(theta / half) + (1 - theta) * mpmath.log((1 - theta) / half)
    print(f"  limiting exponent KL(theta || 1/2) = {mpmath.nstr(rate, 10)}")

    head("G. Calibration A (beta = 1/3, lam = 6/17, u = 18/11) with n slots: Prop. 2(iii) and the ceiling")
    u = F(18, 11)
    lam, b, c0, lh, ll = slot_law(u, F(1, 3))
    print(f"  lam = {lam}, b = {b}, c0 = {c0}")
    for n in range(1, 9):
        top = (1 + u) ** n
        Mn = top / (1 + top)
        print(f"  n = {n}: M_n = {Mn} (~{dec(Mn, 6)}), r_C(M_n) = {mpmath.nstr(rC(Mn), 10)},"
              f" M_n < tau(3.6): {Mn < O36['tau']}")
    for n in (1, 2, 3, 4):
        for r, o in ((R1, O3), (R2, O36)):
            thr = o["tau"] / (1 - o["tau"])
            d, z = 0, F(1)
            while z < thr:
                d += 1
                z *= (1 + u)
            if d > n:
                e = RHO
            else:
                e = RHO + (1 - RHO) * (tail_D(lh, n, d) + tail_D(ll, n, d)) / 2
            print(f"    n = {n}, r = {str(r):5s}: recruiting D >= {d}; entry = {e} (~{dec(e, 6)})")

    head("H. Random (Poisson) number of arrivals at calibration A: lower bound valid in every equilibrium")
    print("  Bound: entry(3.6) >= rho + (1-rho) P(N = 2) P((+,+) | N = 2); P((+,+)|N=2) = (p_H(+)^2 + p_L(+)^2)/2")
    pp2 = ((lh[0]) ** 2 + (ll[0]) ** 2) / 2
    print(f"  P((+,+) | N = 2) = {pp2} (~{dec(pp2, 6)})")
    for Lam in (mpmath.mpf(1) / 2, mpmath.mpf(1), mpmath.mpf(2)):
        pN2 = mpmath.e ** (-Lam) * Lam ** 2 / 2
        lb = mpmath.mpf(1) / 4 + mpmath.mpf(3) / 4 * pN2 * (mpmath.mpf(pp2.numerator) / pp2.denominator)
        print(f"  Lambda = {mpmath.nstr(Lam, 4)}: entry(3.6) >= {mpmath.nstr(lb, 10)}")
    # margins behind the bound at r = 3.6
    o = O36
    m1 = RHO * o["D"] * (1 - F(29, 40)) - K
    m2 = RHO * o["D"] * (1 - F(841, 962)) - K
    print(f"  slot-1 margin rho Delta (1 - 29/40) - k = {m1} (~{dec(m1, 6)})")
    print(f"  slot-2 margin after a buy rho Delta (1 - 841/962) - k = {m2} (~{dec(m2, 6)})")
    print(f"  posterior after (+,+) = 841/962 ~ {dec(F(841, 962), 6)} > tau(3.6) = {dec(o['tau'], 6)}")


if __name__ == "__main__":
    main()
