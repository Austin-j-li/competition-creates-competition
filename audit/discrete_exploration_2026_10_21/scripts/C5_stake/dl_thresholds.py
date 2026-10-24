"""Stake thresholds of the discrete-Laplace model (mpmath, 60 digits; print only).

Checks first the reduction to a good-news / bad-news model by direct summation over flows.
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/dl_thresholds.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, exp, nstr  # noqa: E402
from dl_lib import BENCH, R0, R1, R2, R_END, auction, tau_of, posteriors, check_reduction_by_summation  # noqa: E402

mp.dps = 60


def consts(par=BENCH):
    aa = exp(-1 / par["b"])
    delta = (1 - aa) / (1 + aa)
    g0 = aa / (1 + aa)
    g1 = 1 / (1 + aa)
    return aa, delta, g0, g1


def thresholds(r, par=BENCH):
    a = auction(r, par)
    rho, k = par["rho"], par["k"]
    aa, delta, g0, g1 = consts(par)
    tau = tau_of(a, par)
    D, wL, wH = a["D"], a["wL"], a["wH"]
    out = dict(a=a, tau=tau, aa=aa, delta=delta, g0=g0, g1=g1)
    out["M1"], out["m1"] = g1, g0
    out["Bhalf"] = a["gL"] + (a["gH"] - a["gL"]) / 2
    out["B_M1"] = a["gL"] + g1 * (a["gH"] - a["gL"])
    out["NT_cost_ok"] = rho * D / 2 <= k                      # no trade exists for every omega iff True
    # S = (bH, bL) = (1, 0)
    out["DH_S_zero"] = D * g0 * g1 * (1 + rho) - k            # H gain at S with omega = 0
    out["omega_H"] = (k - D * g0 * g1 * (1 + rho)) / (wH * delta * (1 - rho))
    out["Omega1"] = (D * (g1 ** 2 + rho * g0 ** 2) + k) / (wL * delta * (1 - rho))
    # recruitment feasible at the best price?
    out["recruit_ok"] = tau <= g1
    if out["recruit_ok"] and tau > mpf(1) / 2:
        beta_max = (g1 / tau - 1) / delta
        m_at = g0 / (1 - delta * beta_max)
        out["beta_max"] = beta_max
        out["Omega2"] = (D * (g1 * tau + rho * g0 * m_at) + k) / (wL * delta * (1 - rho))
        # H-threshold mixing profile (beta_star, 0)
        ustar = g0 * (2 * tau - 1) / (1 - tau)
        out["beta_star"] = ustar / delta
        DH_I = D * g0 * g1 * rho * (1 / (2 * g0 + ustar) + 1 / (2 * g1 - ustar)) - k
        out["DH_I_at_star"] = DH_I
        const = D * g0 * g1 * (1 / (2 * g0 + ustar) + rho / (2 * g1 - ustar)) - k
        out["omega_star"] = -const / (wH * delta * (1 - rho))   # D_H^{II}(beta_star) = 0
        out["DH_II_star_zero_stake"] = const
    return out


def show(name, x):
    print(f"  {name:36s} {nstr(x, 12):>18s}")


if __name__ == "__main__":
    print("Benchmark (D-Laplace): h=10 l=1 p=1/2 rho=1/4 cL=0 cH=5 k=1/50 b=2")
    aa, delta, g0, g1 = consts()
    show("a = exp(-1/b)", aa)
    show("delta = (1-a)/(1+a)", delta)
    show("g0 = a/(1+a) = m1", g0)
    show("g1 = 1/(1+a) = M1", g1)
    print("\nReduction check (direct summation over flows -3..120 vs two-value posterior):")
    for (bH, bL) in ((mpf(1), mpf(0)), (mpf(1), mpf("0.3")), (mpf("0.4"), mpf(0)), (mpf("0.7"), mpf("0.2"))):
        M, m = posteriors(bH, bL)
        Mmin, Mmax, mmin, mmax = check_reduction_by_summation(bH, bL)
        print(f"  (bH,bL)=({nstr(bH,3)},{nstr(bL,3)}): M={nstr(M,12)} spread={nstr(Mmax-Mmin,3)}; "
              f"m={nstr(m,12)} spread={nstr(mmax-mmin,3)}; |dev|={nstr(abs(Mmax-M)+abs(mmax-m),3)}")
    for name, r in (("r0 = 6/5", R0), ("r1 = 3", R1), ("r_end = 4", R_END), ("r2 = 21/5", R2)):
        t = thresholds(r)
        print(f"\n== {name} ==")
        show("Delta_T", t["a"]["D"])
        show("tau", t["tau"])
        show("B(1/2)", t["Bhalf"])
        show("B(M1)", t["B_M1"])
        print(f"  recruit feasible (tau <= M1): {t['recruit_ok']};  NT exists for all omega (rho D/2 <= k): {t['NT_cost_ok']}")
        show("H gain at S, zero stake", t["DH_S_zero"])
        show("omega_H (S appears)", t["omega_H"])
        if "Omega2" in t:
            show("beta_max", t["beta_max"])
            show("beta_star (posterior = tau, bL=0)", t["beta_star"])
            show("D_H^I at beta_star (zero stake)", t["DH_I_at_star"])
            show("omega_star (H threshold-mix)", t["omega_star"])
            show("Omega2 (L buys at M=tau)", t["Omega2"])
        show("Omega1 (L mimics at S)", t["Omega1"])
