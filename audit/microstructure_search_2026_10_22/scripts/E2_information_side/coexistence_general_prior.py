"""General-prior coexistence formulas of the ledger note (22 Oct, coordinator), checked against a complete
equilibrium classification of the slot (investor sees the class: a = 1; no buyer signal: d = 1/2). Print only.

Ledger claims:
  (N) no trade is an equilibrium iff rho * Delta_T * max{pi, 1 - pi} <= k;
  (A) r_A solves Delta_T (1 - tau) = k for every prior;
  (E) on the interior branch, E = rho + (1 - rho)(1 - pi) b Delta_T / k.
Tie rules: investor IM, challenger C1 (CM threshold mixtures are counted separately).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from mpmath import mp, mpf, sqrt
from common import EXACT, MP, show, auction, B, tau, bounds, calibration_A, calibration_B
from slot_solver import SlotModel, fmt

RHO, CH, K = Fr(1, 4), 6, Fr(1, 50)


def frak(D):
    D = mpf(D) if not isinstance(D, Fr) else mpf(D.numerator) / D.denominator
    return 1 + D + sqrt(D * D + 2 * D)


def r_A_bracket():
    """Exact rational bisection of J(r) = Delta_T(r)(1 - tau(r)) - k on [6/5, 7/4] (one root, T2 / X_check)."""
    J = lambda r: auction(EXACT, r)["D"] * (1 - tau(auction(EXACT, r), EXACT(CH))) - K
    lo, hi = Fr(6, 5), Fr(7, 4)
    for _ in range(45):
        mid = (lo + hi) / 2
        if J(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi, J(lo), J(hi)


def run(label, F, S, priors, grid):
    lo, hi, Jlo, Jhi = r_A_bracket()
    rA = (mpf(lo.numerator) / lo.denominator + mpf(hi.numerator) / hi.denominator) / 2
    tau_rA = tau(auction(MP, rA), MP(CH))
    print("=" * 100)
    print(f"Calibration {label}. r_A in [{mp.nstr(mpf(lo.numerator) / lo.denominator, 14)}, {mp.nstr(mpf(hi.numerator) / hi.denominator, 14)}] "
          f"(J signs {'-' if Jlo < 0 else '+'}/{'-' if Jhi < 0 else '+'}); tau(r_A) = {mp.nstr(tau_rA, 10)}; r_A does not depend on pi or on the slot")
    rho, k, cH = F(RHO), F(K), F(CH)
    u = S["u"] if not isinstance(S["u"], Fr) else mpf(S["u"].numerator) / S["u"].denominator
    print(f"   lowest prior with M(pi) >= tau(r_A): pi_lo = {mp.nstr(tau_rA / ((1 + u) * (1 - tau_rA) + tau_rA), 10)}; "
          f"rho * Delta_T(r_A) = {mp.nstr(auction(MP, rA)['D'] / 4, 6)} < k, so r_A < r_N(pi) at every prior")
    for pi in priors:
        pi = F(pi)
        m, M = bounds(S["u"], pi)
        piv = mpf(pi.numerator) / pi.denominator if isinstance(pi, Fr) else pi
        Mv = mpf(M.numerator) / M.denominator if isinstance(M, Fr) else M
        rN = frak(k / (rho * max(pi, 1 - pi)))
        rF = frak(k / (1 - M))
        cond = piv < tau_rA < Mv
        print(f"-- prior pi = {show(pi, 8)}: M(pi) = {show(M, 8)}; r_N(pi) = {mp.nstr(rN, 10)}; r_F(pi) = {mp.nstr(rF, 10)}; "
              f"pi < tau(r_A) < M(pi): {cond}")
        nt_set, coex_set, mism_N, mism_A, e_err, cm_count = [], [], 0, 0, F(0), 0
        first_inf_by_type = {}
        n_rec, rec_set = 0, []
        for r in grid:
            rr = F(r)
            A = auction(F, rr)
            mod = SlotModel(F, S, A, pi, 1, Fr(1, 2) if F is EXACT else "1/2", RHO, CH, K)
            eqs, cms, cmt = mod.equilibria()
            cm_count += len(cms) + len(cmt)
            has_nt = any(s == 0 and t == 0 for s, t, *_ in eqs)
            infs = [(s, t, ks, kt) for s, t, ks, kt in eqs if s > 0 or t > 0]
            tau_r = tau(A, cH)
            pred_nt = (rho if pi < tau_r else 1) * A["D"] * max(pi, 1 - pi) <= k
            if has_nt != pred_nt:
                mism_N += 1
            if has_nt:
                nt_set.append(r)
            if has_nt and infs:
                coex_set.append(r)
                # prediction (A): an informative equilibrium coexists iff Delta_T(1 - tau) >= k and pi < tau(r) <= M(pi)
            pred_coex = pred_nt and (A["D"] * (1 - tau_r) >= k) and (pi < tau_r <= M)
            if (has_nt and bool(infs)) != pred_coex:
                mism_A += 1
            for s, t, ks, kt in infs:
                out = mod.outcome(s, t)
                if ks == "interior, state (1, 1)" and t == 0:
                    formula = rho + (1 - rho) * (1 - pi) * S["b"] * A["D"] / k
                    e_err = max(e_err, abs(out["E"] - formula))
                    n_rec += 1
                    rec_set.append(r)
                first_inf_by_type.setdefault(f"buy {ks} / sell {kt}", r)
        rng = lambda L: f"[{L[0]}, {L[-1]}] ({len(L)} grid points)" if L else "empty"
        print(f"   no trade is an equilibrium on {rng(nt_set)}; mismatches with (N): {mism_N}")
        print(f"   no trade coexists with an informative equilibrium on {rng(coex_set)}; mismatches with the predicted set: {mism_A}")
        print(f"   first grid strength of each informative branch: {first_inf_by_type}")
        print(f"   interior recruiting branch (state (1, 1), no sale) found on {rng(rec_set)}; predicted open interval (r_A, r_F(pi))")
        print(f"   max |E - formula (E)| on that branch: {fmt(e_err, 3)} over {n_rec} grid points; CM-only threshold mixtures seen: {cm_count}")


def main():
    grid = [Fr(1200 + 5 * i, 1000) for i in range(141)]  # 1.200, 1.205, ..., 1.900
    SA = calibration_A()
    SB, _ = calibration_B()
    run("A (exact)", EXACT, SA, [Fr(1, 2), Fr(12, 25), Fr(51, 100), Fr(3, 5), Fr(2, 5)], grid)
    run("B (40 digits)", MP, SB, ["1/2", "12/25", "13/25"], grid)
    # Spot values that match X_check's table (pi = 1/2, calibration A)
    print("=" * 100)
    for r in (Fr(7, 5), Fr(29, 20)):
        A = auction(EXACT, r)
        val = RHO + (1 - RHO) * Fr(1, 2) * SA["b"] * A["D"] / K
        print(f"pi = 1/2, A, r = {r}: interior-branch entry = {show(val)} (X_check: 0.481092 at 1.40, 0.532391 at 1.45)")


if __name__ == "__main__":
    main()
