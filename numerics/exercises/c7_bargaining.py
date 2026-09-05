"""C.7: bargaining weights and the payment property (Lemma 3, OA.42 to OA.44)."""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
from scipy import integrate

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import bargaining_closed_form, bargaining_transfer  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.params import BENCHMARK, BENCHMARK_STRENGTHS, CONTROLS  # noqa: E402

TOL = CONTROLS.independent_formula_acceptance


def integrate_uniform(fun, r: float, splits: list[float]) -> float:
    pts = sorted({0.0, r, *[s for s in splits if 0 < s < r]})
    return sum(integrate.quad(fun, a, b_, epsabs=1e-13, epsrel=1e-13)[0] for a, b_ in zip(pts[:-1], pts[1:])) / r


def run() -> bool:
    checks = {}
    prim = BENCHMARK
    h, ell = prim.fh, prim.fell
    etas = [str(Decimal(i) / Decimal(100)) for i in range(0, 100)] + ["1"]
    rows = []
    max_err, max_feas, max_foc = 0.0, 0.0, 0.0
    strengths = {k: float(v) for k, v in BENCHMARK_STRENGTHS.items() if k in ("r_weak", "r_strong")}
    per_eta = {}
    for eta_s in etas:
        eta = float(eta_s)
        for name, r in strengths.items():
            cf = bargaining_closed_form(prim, r, eta)
            tH = integrate_uniform(lambda R: bargaining_transfer(R, h, eta), r, [h])
            tL = integrate_uniform(lambda R: bargaining_transfer(R, ell, eta), r, [ell])
            t0 = integrate_uniform(lambda R: eta * R, r, [])
            GH = integrate_uniform(lambda R: (1 - eta) * np.maximum(h - R, 0.0), r, [h])
            GL = integrate_uniform(lambda R: (1 - eta) * np.maximum(ell - R, 0.0), r, [ell])
            err = max(abs(tH - cf["t_H_eta"]), abs(tL - cf["t_L_eta"]), abs(t0 - cf["t_0_eta"]), abs(GH - cf["G_H_eta"]),
                      abs(GL - cf["G_L_eta"]), abs((tH - tL) - cf["Delta_eta"]))
            # feasibility z <= T <= V and Nash first-order condition on a grid of R
            Rg = np.linspace(0, r, 2001)
            feas = 0.0
            foc = 0.0
            for theta in (h, ell):
                z = np.minimum(Rg, theta)
                V = np.maximum(Rg, theta)
                T = bargaining_transfer(Rg, theta, eta)
                feas = max(feas, float(np.max(np.maximum(z - T, 0) + np.maximum(T - V, 0))))
                if 0 < eta < 1:
                    inter = V > z
                    foc = max(foc, float(np.max(np.abs(eta * (V[inter] - T[inter]) - (1 - eta) * (T[inter] - z[inter])))))
            max_err, max_feas, max_foc = max(max_err, err), max(max_feas, feas), max(max_foc, foc)
            per_eta[(eta_s, name)] = {"t_0_eta": t0, "t_H_eta": tH, "t_L_eta": tL, "Delta_eta": tH - tL, "G_H_eta": GH, "G_L_eta": GL,
                                      "feas": feas, "err": err}
        w, s = per_eta[(eta_s, "r_weak")], per_eta[(eta_s, "r_strong")]
        for name, r in strengths.items():
            d = per_eta[(eta_s, name)]
            status = ("payment-stage limit (eta = 1: buyer rents extinguished; not a positive-cost entry equilibrium)" if eta_s == "1"
                      else "analytical (Lemma 3; acquisition-stage comparison, no entry prediction)")
            rows.append({"eta": eta_s, "r": BENCHMARK_STRENGTHS[name], "t_0_eta": d["t_0_eta"], "t_H_eta": d["t_H_eta"], "t_L_eta": d["t_L_eta"],
                         "Delta_eta": d["Delta_eta"], "G_H_eta": d["G_H_eta"], "G_L_eta": d["G_L_eta"],
                         "spread_strength_difference": s["Delta_eta"] - w["Delta_eta"],
                         "profit_H_strength_difference": s["G_H_eta"] - w["G_H_eta"], "profit_L_strength_difference": s["G_L_eta"] - w["G_L_eta"],
                         "transfer_feasibility_error": d["feas"], "integration_error": d["err"], "status": status})
    # sign change of the spread difference at the midpoint
    diff = {e: per_eta[(e, "r_strong")]["Delta_eta"] - per_eta[(e, "r_weak")]["Delta_eta"] for e in etas}
    below = all(diff[e] > 0 for e in etas if Decimal(e) < Decimal("0.5"))
    above = all(diff[e] < 0 for e in etas if Decimal("0.5") < Decimal(e) < 1)
    checks["integration_vs_OA44"] = {"max_error": max_err, "pass": max_err <= TOL}
    checks["transfer_feasibility"] = {"max_error": max_feas, "pass": max_feas <= TOL}
    checks["nash_foc"] = {"max_error": max_foc, "pass": max_foc <= TOL}
    checks["spread_difference_sign"] = {"positive_below_half": below, "negative_above_half": above, "at_half": diff["0.5"],
                                        "pass": below and above and abs(diff["0.5"]) <= TOL}
    checks["profits_decrease_with_strength"] = {"pass": all(per_eta[(e, "r_strong")]["G_H_eta"] <= per_eta[(e, "r_weak")]["G_H_eta"] + TOL
                                                            and per_eta[(e, "r_strong")]["G_L_eta"] <= per_eta[(e, "r_weak")]["G_L_eta"] + TOL for e in etas)}
    passed = all(c["pass"] for c in checks.values())
    write_csv("figures_data/bargaining.csv", ["eta", "r", "t_0_eta", "t_H_eta", "t_L_eta", "Delta_eta", "G_H_eta", "G_L_eta", "spread_strength_difference",
                                              "profit_H_strength_difference", "profit_L_strength_difference", "transfer_feasibility_error",
                                              "integration_error", "status"], rows)
    write_manifest("c7_bargaining", {"h": prim.h, "ell": prim.ell, "strengths": strengths, "reserve": "0", "eta": "0..0.99 by 0.01, plus 1 as limit"},
                   "Pointwise Nash transfers integrated over the uniform incumbent and compared with OA.44; feasibility and FOC checked on a grid.",
                   CONTROLS.as_dict(), ["figures_data/bargaining.csv"], checks, passed)
    print("C.7 passed" if passed else "C.7 FAILED", checks)
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
