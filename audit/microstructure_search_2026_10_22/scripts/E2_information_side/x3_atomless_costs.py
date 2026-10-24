"""X3: atomless preparation costs (Prop. A.6) with the order slot. Print only.

Declared cost law (online appendix C.0, C.1): rho * U[0, 2 eps] + (1 - rho) * U[c_H - eps, c_H + eps],
eps = 0.1, c_H = 6, rho = 0.25. Benchmark strengths 1.2 (weak), 3 (strong), 3.6 (collapse).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from mpmath import mp, mpf, quad, exp, sqrt, inf
from common import EXACT, MP, show, auction, B, tau, bounds, calibration_A, calibration_B

RHO, CH, EPS, K = "1/4", 6, "1/10", "1/50"


def HC(F, x, rho=RHO, cH=CH, eps=EPS):
    rho, cH, eps = F(rho), F(cH), F(eps)
    low = min(max(x / (2 * eps), F(0)), F(1))
    high = min(max((x - (cH - eps)) / (2 * eps), F(0)), F(1))
    return rho * low + (1 - rho) * high, low, high


def flow_law(S, pi, orders):
    """Class-conditional laws of Q for the investor orders (qH, qL) in {-1,0,1}."""
    lam, b, c = S["lam"], S["b"], S["c"]
    base = {1: b, 0: c, -1: b}
    lawH = dict(base); lawH[orders[0]] += lam
    lawL = dict(base); lawL[orders[1]] += lam
    out = {}
    for x in (1, 0, -1):
        pr = pi * lawH[x] + (1 - pi) * lawL[x]
        out[x] = (lawH[x], lawL[x], pi * lawH[x] / pr)
    return out


def outcome(F, S, r, orders, pi="1/2"):
    pi = F(pi)
    A = auction(F, r)
    law = flow_law(S, pi, orders)
    eH = eL = F(0)
    detail = {}
    for x, (pH, pL, mu) in law.items():
        e, low, high = HC(F, B(A, mu))
        eH += pH * e
        eL += pL * e
        detail[x] = (mu, B(A, mu), low, high, e)
    E = pi * eH + (1 - pi) * eL
    return dict(E=E, eH=eH, eL=eL, OH=pi * eH, detail=detail, A=A)


def entry_by_cost_integration(F, S, r, orders, pi="1/2"):
    """Independent route: integrate Pr(prepare | C = c) over each uniform cost component (mpmath quad)."""
    pi = F(pi)
    A = auction(F, r)
    law = flow_law(S, pi, orders)
    pts = []
    for x, (pH, pL, mu) in law.items():
        prob = pi * pH + (1 - pi) * pL
        g = B(A, mu)
        pts.append((mpf(prob) if not isinstance(prob, Fr) else mpf(prob.numerator) / prob.denominator,
                    mpf(g) if not isinstance(g, Fr) else mpf(g.numerator) / g.denominator))

    def prep(cst):
        return sum(pr for pr, g in pts if cst <= g)

    eps, cH, rho = mpf(1) / 10, mpf(CH), mpf(1) / 4
    brk_low = sorted({mpf(0), 2 * eps, *[g for _, g in pts if 0 < g < 2 * eps]})
    brk_high = sorted({cH - eps, cH + eps, *[g for _, g in pts if cH - eps < g < cH + eps]})
    low = quad(prep, brk_low) / (2 * eps)
    high = quad(prep, brk_high) / (2 * eps)
    return rho * low + (1 - rho) * high


def laplace_mixture_entry(r, bscale=2):
    """Paper cross-check: Laplace noise, full orders, prior 1/2, declared cost mixture."""
    A = auction(MP, MP(r))
    bscale = mpf(bscale)
    f = lambda z: exp(-abs(z) / bscale) / (2 * bscale)
    mu = lambda x: 1 / (1 + exp(-(2 / bscale) * max(-1, min(x, 1))))
    hi = lambda x: HC(MP, B(A, mu(x)))[2]
    pts = [-inf, -1, 0, 1, inf]
    aH = quad(lambda x: hi(x) * f(x - 1), pts)
    aL = quad(lambda x: hi(x) * f(x + 1), pts)
    rho = mpf(1) / 4
    eH, eL = rho + (1 - rho) * aH, rho + (1 - rho) * aL
    return (eH + eL) / 2, eH / 2


def r_where_BM_equals(M, cval):
    """Root in r of B_r(M) = cval for the benchmark (unique, B_r(M) falls in r)."""
    M = mpf(M) if not isinstance(M, Fr) else mpf(M.numerator) / M.denominator
    cval = mpf(cval)
    return ((10 * M - cval) + sqrt((10 * M - cval) ** 2 + M * (3 - 4 * M) / 4)) / M


def main():
    SA = calibration_A()
    SB, _ = calibration_B()
    for label, F, S in (("A (exact)", EXACT, SA), ("B (40 digits)", MP, SB)):
        half = F(Fr(1, 2))
        m, M = bounds(S["u"], half)
        A0, A1, A2 = auction(F, F(Fr(6, 5))), auction(F, F(3)), auction(F, F(Fr(18, 5)))
        rho, k, eps, cH = F(RHO), F(K), F(EPS), F(CH)
        kappa = min(m, 1 - M)
        print("=" * 100)
        print(f"Calibration {label}: m = {show(m)}, M = {show(M)}")
        print("Slot margins of Prop. A.6 (all must be strictly positive):")
        marg = {
            "zeta_L  = B_3(m) - 2 eps": B(A1, m) - 2 * eps,
            "zeta_H0 = c_H - eps - B_1.2(1/2)": cH - eps - B(A0, half),
            "zeta_H1 = B_3(M) - c_H - eps": B(A1, M) - cH - eps,
            "zeta_0  = k - Delta_T(1.2)": k - A0["D"],
            "zeta_1  = rho kappa Delta_T(3) - k  (slot: no (1 - 1/b) factor)": rho * kappa * A1["D"] - k,
        }
        for name, v in marg.items():
            print(f"   {name}: {show(v)}")
        print(f"   (Laplace version of zeta_1 for comparison: (1/2) rho m Delta_T(3) - k = {show((rho * kappa * A1['D']) / 2 - k)})")
        print(f"   domain: beta <= 1/3, so c >= b and the zero-flow posterior stays in [m, M]: c - b = {show(S['c'] - S['b'])}")

        print("Weak economy r = 1.2, zero orders (unique by zeta_0):")
        w = outcome(F, S, F(Fr(6, 5)), (0, 0))
        print(f"   E = {show(w['E'])}, O_H = {show(w['OH'])}, entry at the prior = {show(w['detail'][0][4])}")
        print("Strong economy r = 3, full orders (unique by zeta_1):")
        s = outcome(F, S, F(3), (1, -1))
        for x, (mu, g, lo, hi, e) in s["detail"].items():
            print(f"   Q = {x:+d}: mu = {show(mu, 10)}, B = {show(g, 10)}, H_low = {show(lo, 6)}, H_high = {show(hi, 6)}, e = {show(e, 10)}")
        print(f"   E = {show(s['E'])}, e_H = {show(s['eH'])}, e_L = {show(s['eL'])}, O_H = {show(s['OH'])}")
        S_atomic = F(rho) + (1 - rho) * (S["b"] + S["lam"] / 2)
        print(f"   atomic-cost entry rho + (1 - rho)(b + lam/2) = {show(S_atomic)}; difference = {show(s['E'] - S_atomic)}")
        E_int = entry_by_cost_integration(F, S, F(3), (1, -1))
        Es = s["E"] if not isinstance(s["E"], Fr) else mpf(s["E"].numerator) / s["E"].denominator
        print(f"   independent cost integration: E = {mp.nstr(E_int, 20)}; difference = {mp.nstr(E_int - Es, 3)}")

        # Direct investor payoffs at the strong candidate (unit orders; conditional on an informed arrival)
        A = s["A"]
        P = {x: A["t0"] + e * (A["wL"] + A["D"] * mu) for x, (mu, g, lo, hi, e) in s["detail"].items()}
        VH = {x: A["t0"] + e * A["wH"] for x, (mu, g, lo, hi, e) in s["detail"].items()}
        VL = {x: A["t0"] + e * A["wL"] for x, (mu, g, lo, hi, e) in s["detail"].items()}
        print("   investor payoffs at r = 3 (q = +1, 0, -1): "
              f"H: {show(VH[1] - P[1] - k, 8)}, 0, {show(P[-1] - VH[-1] - k, 8)}; "
              f"L: {show(VL[1] - P[1] - k, 8)}, 0, {show(P[-1] - VL[-1] - k, 8)}")
        P0 = {x: w["A"]["t0"] + e * (w["A"]["wL"] + w["A"]["D"] * mu) for x, (mu, g, lo, hi, e) in w["detail"].items()}
        VH0 = {x: w["A"]["t0"] + e * w["A"]["wH"] for x, (mu, g, lo, hi, e) in w["detail"].items()}
        VL0 = {x: w["A"]["t0"] + e * w["A"]["wL"] for x, (mu, g, lo, hi, e) in w["detail"].items()}
        print("   investor payoffs at r = 1.2 (q = +1, 0, -1): "
              f"H: {show(VH0[1] - P0[1] - k, 8)}, 0, {show(P0[-1] - VH0[-1] - k, 8)}; "
              f"L: {show(VL0[1] - P0[1] - k, 8)}, 0, {show(P0[-1] - VL0[-1] - k, 8)}")

        print("The smoothed ceiling: full orders (unique for r >= 3), entry along r:")
        r_hi = r_where_BM_equals(M, cH + eps)
        r_lo = r_where_BM_equals(M, cH - eps)
        r_C = r_where_BM_equals(M, cH)
        print(f"   B_r(M) = 6.1 at r = {mp.nstr(r_hi, 12)}; = 6 at r = {mp.nstr(r_C, 12)}; = 5.9 at r = {mp.nstr(r_lo, 12)}")
        for r in ("3", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9"):
            o = outcome(F, S, F(r), (1, -1))
            print(f"   r = {r}: E = {show(o['E'], 10)}, O_H = {show(o['OH'], 10)}, H_high at Q=1 = {show(o['detail'][1][3], 8)}")
        o36 = outcome(F, S, F(Fr(18, 5)), (1, -1))
        print(f"   part (iii) with atomless costs needs c_H - eps > B_3.6(M): margin = {show(cH - eps - B(A2, M))}")
        print(f"   trading bound at 3.6: rho kappa Delta_T(3.6) - k = {show(rho * kappa * A2['D'] - k)}")

    print("=" * 100)
    print("Laplace cross-check (paper Table 3, Panel A, 'Laplace, cost mixture': 0.522715 and 0.324148)")
    for r in ("3", "3.6"):
        E_lap, OH_lap = laplace_mixture_entry(r)
        print(f"   r = {r}: E = {mp.nstr(E_lap, 12)}, O_H = {mp.nstr(OH_lap, 12)}")


if __name__ == "__main__":
    main()
