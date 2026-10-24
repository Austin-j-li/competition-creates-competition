"""Exact stake thresholds of the three-point model (benchmark values; print only).

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/tp_thresholds.py
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tp_lib import BENCH, R0, R1, R2, auction, tau_of  # noqa: E402


def thr(r, par=BENCH):
    a = auction(r, par)
    rho, k = par["rho"], par["k"]
    tau = tau_of(a, par)
    D, wL, wH = a["D"], a["wL"], a["wH"]
    out = dict(a=a, tau=tau)
    out["omega_H"] = (3 * k - rho * D) / ((1 - rho) * wH)          # H buys against NT (belief 1) / S needs >=
    out["Omega1"] = ((1 + rho) * D + 3 * k) / ((1 - rho) * wL)      # L mimics H at S above this
    out["Omega2"] = ((rho + tau) * D + 3 * k) / ((1 - rho) * wL)    # L buys at the top-flow posterior tau
    out["beta_max"] = 1 / tau - 1
    out["zero_stake_H_gain"] = rho * D / 3 - k
    return out


def show(label, x):
    print(f"  {label:34s} {str(x):>24s}  = {float(x):.10f}")


if __name__ == "__main__":
    print("Benchmark:", {k_: str(v) for k_, v in BENCH.items()})
    for name, r in (("r0 = 6/5", R0), ("r1 = 3", R1), ("r2 = 18/5", R2)):
        t = thr(r)
        a = t["a"]
        print(f"\n== {name} ==")
        for key in ("t0", "tL", "tH", "gL", "gH", "D", "wL", "wH"):
            show(key, a[key])
        show("tau", t["tau"])
        show("B(1/2)", a["gL"] + (a["gH"] - a["gL"]) / 2)
        show("beta_max = 1/tau - 1", t["beta_max"])
        show("zero-stake H gain rho*D/3 - k", t["zero_stake_H_gain"])
        show("omega_H (S appears / NT breaks)", t["omega_H"])
        show("Omega2 (L buys at mu=tau)", t["Omega2"])
        show("Omega1 (L mimics at S)", t["Omega1"])
    # Closed form for the L-indifference mix at r1: 1 + beta = D / (omega wL (1-rho) - rho D - 3k)
    t1 = thr(R1)
    a1 = t1["a"]
    rho, k = BENCH["rho"], BENCH["k"]
    print("\nMixed L-buying probability beta*(omega) at r1 (H buys, e(2)=1):")
    for om in (F(2027, 1000), F(21, 10), F(22, 10), F(23, 10), F(24, 10), F(25, 10), t1["Omega1"]):
        den = om * a1["wL"] * (1 - rho) - rho * a1["D"] - 3 * k
        if den > 0:
            beta = a1["D"] / den - 1
        else:
            beta = None
        ok = (beta is not None) and (0 <= beta <= t1["beta_max"])
        print(f"  omega={float(om):.6f}  beta*={None if beta is None else float(beta):}  feasible={ok}")
    # Challenger-mixing branch at beta_max: e2 = (3k + rho D + rho omega wL)/(omega wL - D tau)
    print("\nChallenger-mixing branch at beta_max (r1): e(2), entry E, O_H")
    for om in (t1["Omega2"], F(25, 10), t1["Omega1"], F(3), F(5), F(10), F(100), F(1000)):
        num = 3 * k + rho * a1["D"] + rho * om * a1["wL"]
        den = om * a1["wL"] - a1["D"] * t1["tau"]
        e2 = num / den
        beta = t1["beta_max"]
        E = rho + (1 + beta) * (e2 - rho) / 6
        OH = F(1, 2) * (rho + (e2 - rho) / 3)
        print(f"  omega={float(om):10.4f} e2={float(e2):.6f} E={float(E):.6f} O_H={float(OH):.6f}")
    # Sell-only memo, claim 14 comparison numbers
    print("\nCompare Q2 sell-only Claim 14 (buy-only menu, c_L = 0): 2.5987878788 =",
          float(t1["Omega1"]))
    print("Compare Laplace memo Omega_F = 2.1584629814; pure branch end 2.4988548726")
