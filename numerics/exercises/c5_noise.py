"""C.5: noise laws, threshold distance, and posterior upper tails under full orders."""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
from scipy import integrate

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import payoffs_closed_form  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.noise import pdf, posterior_bounds, variance  # noqa: E402
from numerics.params import BENCHMARK, BENCHMARK_STRENGTHS, CONTROLS, Noise  # noqa: E402

TOL = CONTROLS.independent_formula_acceptance


def tails(noise: Noise, b: float, tau: float, m: float, M: float) -> tuple:
    """(x_star, alpha_H, alpha_L, label) under full orders for threshold tau; endpoint conventions per C.5."""
    if tau <= 0.5 + 0.0 and tau <= m:
        return -np.inf, 1.0, 1.0, "always"
    if tau > M:
        return np.inf, 0.0, 0.0, "unattainable"
    if noise == Noise.LAPLACE:
        if tau == M:
            return 1.0, 0.5, 0.5 * np.exp(-2 / b), "plateau_tie_rule"
        x = b / 2 * np.log(tau / (1 - tau))
        return x, 1 - 0.5 * np.exp((x - 1) / b), 0.5 * np.exp(-(x + 1) / b), "interior"
    if tau == M:
        return np.inf, 0.0, 0.0, "unattainable_endpoint"
    A = np.exp(1 / b)
    w = np.sqrt(tau / (1 - tau))
    x = b * np.log((A * w - 1) / (A - w))
    return x, 1 / (1 + np.exp((x - 1) / b)), 1 / (1 + np.exp((x + 1) / b)), "interior"


def run() -> bool:
    checks = {}
    prim = BENCHMARK
    r = float(BENCHMARK_STRENGTHS["r_strong"])
    pay = payoffs_closed_form(prim, r)
    b, rho, k = prim.fb, prim.frho, prim.fk
    m, M = posterior_bounds(b)
    tau_bench = pay.tau(prim.fc_H)
    rows = []
    d_grid = [Decimal(i) / Decimal(400) for i in range(401)]
    taus = [(float(M - float(d) * (M - 0.5)), "grid") for d in d_grid]
    taus += [(tau_bench, "benchmark"), (M - 1e-4, "M_minus_1e-4"), (M - 1e-6, "M_minus_1e-6"), (M + 1e-6, "M_plus_1e-6")]
    full_margin = (1 - 1 / b) * rho * m * pay.Delta_T - k
    max_int_err = 0.0
    for noise in (Noise.LAPLACE, Noise.LOGISTIC):
        nvar = variance(noise, b)
        for tau, label in taus:
            x, aH, aL, kind = tails(noise, b, tau, m, M)
            # direct integration of the conditional flow densities above the cutoff
            if np.isfinite(x):
                def tail_int(shift: float) -> float:
                    a0, a1 = x, x + 60 * b
                    v1 = integrate.quad(lambda z: pdf(noise, z - shift, b), a0, a1, epsabs=1e-14, epsrel=1e-14, limit=400,
                                        points=[shift] if a0 < shift < a1 else None)[0]
                    v2 = integrate.quad(lambda z: pdf(noise, z - shift, b), a1, np.inf, epsabs=1e-14, epsrel=1e-14)[0]
                    return v1 + v2
                iH, iL = tail_int(1.0), tail_int(-1.0)
                if kind == "plateau_tie_rule":
                    pass  # x = 1 exactly: entire upper plateau
                err = max(abs(iH - aH), abs(iL - aL))
            else:
                err = 0.0
            max_int_err = max(max_int_err, err)
            mass = (aH + aL) / 2
            E = rho + (1 - rho) * mass
            cH_tau = pay.g_L + tau * (pay.g_H - pay.g_L)
            valid = (prim.fc_L < pay.B(m)) and (prim.fc_L < cH_tau) and (full_margin > 0)
            rows.append({"noise": noise.value, "b": prim.b, "tau": tau, "tau_label": label, "M_minus_tau": M - tau,
                         "normalized_distance": (M - tau) / (M - 0.5), "x_star": ("unattainable" if not np.isfinite(x) and x > 0 else x),
                         "alpha_H": aH, "alpha_L": aL, "posterior_upper_tail_mass": mass, "E": E, "implied_c_H": cH_tau,
                         "noise_variance": nvar, "flow_variance": 1.0 + nvar, "threshold_noise_sd": (x / np.sqrt(nvar) if np.isfinite(x) else "unattainable"),
                         "full_order_margin": full_margin, "equilibrium_interpretation_valid": valid, "integration_error": err,
                         "status": ("analytical (full-order equilibrium with c_H = implied_c_H)" if valid else "numerical diagnostic (information experiment only)")
                         + f"; endpoint={kind}"})
    checks["tail_integration"] = {"max_error": max_int_err, "pass": max_int_err <= TOL}
    bench = [row for row in rows if row["tau_label"] == "benchmark"]
    checks["benchmark_rows"] = {"count": len(bench), "pass": len(bench) == 2,
                                "logistic_threshold_noise_sd": [row["threshold_noise_sd"] for row in bench if row["noise"] == "logistic"]}
    passed = all(c["pass"] for c in checks.values())
    write_csv("figures_data/posterior_tails.csv", ["noise", "b", "tau", "tau_label", "M_minus_tau", "normalized_distance", "x_star", "alpha_H", "alpha_L",
                                                   "posterior_upper_tail_mass", "E", "implied_c_H", "noise_variance", "flow_variance",
                                                   "threshold_noise_sd", "full_order_margin", "equilibrium_interpretation_valid",
                                                   "integration_error", "status"], rows)
    write_manifest("c5_noise", {"benchmark": prim.__dict__, "r": BENCHMARK_STRENGTHS["r_strong"], "grid": "401 points of normalized distance on [0,1]",
                                "specials": ["benchmark tau", "M-1e-4", "M-1e-6", "M+1e-6"]},
                   "Closed-form cutoffs and tails (eq. 14, eq. 20) verified by direct quadrature of the conditional flow densities; "
                   "endpoint conventions: Laplace plateau tie rule at tau = M, logistic zero mass at the unattained endpoint, zero above M.",
                   CONTROLS.as_dict(), ["figures_data/posterior_tails.csv"], checks, passed)
    print("C.5 passed" if passed else "C.5 FAILED", checks)
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
