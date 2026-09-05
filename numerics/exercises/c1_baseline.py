"""C.1: baseline, controls, extensions, and scalar reproduction."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import (Delta_T_formula, dB_dr, dDelta_T_dr, payoffs_benchmark_formula,  # noqa: E402
                              payoffs_closed_form, payoffs_integrated)
from numerics.exercises.common import (classify_feedback, classify_hidden, deviation_rows, node_margins,  # noqa: E402
                                      theorem_margins, validate_control)
from numerics.information import (laplace_full_order_objects, logistic_full_order_objects, make_schedule,  # noqa: E402
                                  OrderProfile)
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.noise import posterior_bounds  # noqa: E402
from numerics.params import (BENCHMARK, BENCHMARK_EXTRA, BENCHMARK_STRENGTHS, CONTROLS, MODERATE, MODERATE_STRENGTHS,  # noqa: E402
                             SIGNAL, SIGNAL_STRENGTHS, CostLaw, Noise, Primitives, decimal_range)
from numerics.search import full_order_candidate, pooling_candidate  # noqa: E402
from numerics.validation import _integrate_flow, validate  # noqa: E402

TOL = CONTROLS.independent_formula_acceptance


def auction_rows(checks: dict) -> list[dict]:
    rows = []
    m, M = posterior_bounds(BENCHMARK.fb)
    for prim, strengths in ((BENCHMARK, BENCHMARK_STRENGTHS), (MODERATE, MODERATE_STRENGTHS), (SIGNAL, SIGNAL_STRENGTHS)):
        for name, rs in strengths.items():
            r = float(rs)
            pay = payoffs_closed_form(prim, r)
            pay_f = payoffs_benchmark_formula(prim, r)
            pay_i, err = payoffs_integrated(prim, r)
            diff = max(abs(getattr(pay, a) - getattr(pay_i, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L"))
            diff2 = max(abs(getattr(pay, a) - getattr(pay_f, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L"))
            dd = abs(pay.Delta_T - Delta_T_formula(prim, r))
            checks[f"auction_integration_{prim.parameter_set}_{name}"] = {"max_abs_diff": diff, "formula_diff": diff2,
                                                                          "Delta_T_diff": dd, "quad_err": err,
                                                                          "pass": max(diff, diff2, dd) <= TOL}
            rows.append({"parameter_set": prim.parameter_set, "r": rs, "p": prim.p, "t_0": pay.t_0, "t_H": pay.t_H,
                         "t_L": pay.t_L, "g_H": pay.g_H, "g_L": pay.g_L, "Delta_T": pay.Delta_T,
                         "B_m": pay.B(m), "B_prior": pay.B(0.5), "B_M": pay.B(M)})
    return rows


def welfare_direct(sched_fb, sched_hidden) -> float:
    """OA.47 / OA.48 evaluated on the feedback marginal flow density."""
    prim, pay = sched_fb.prim, sched_fb.pay
    rho, p, r = prim.frho, pay.p, pay.r
    g = lambda x: 0.5 * (sched_fb.profile.a(prim.noise, prim.fb, x, "H") + sched_fb.profile.a(prim.noise, prim.fb, x, "L"))
    if prim.cost_law == CostLaw.ATOMS:
        cH = prim.fc_H
        integrand = lambda x: g(x) * (pay.B(sched_fb.mu(x)) - cH + p * p / r) * (pay.B(sched_fb.mu(x)) >= cH)
    else:
        e = prim.feps_C
        lo, hi = prim.fc_H - e, prim.fc_H + e

        def inner(B):  # int_{lo}^{min(B,hi)} (B - c + p^2/r) dc / (2e), zero if B < lo
            top = np.clip(B, lo, hi)
            return ((B + p * p / r) * (top - lo) - (top ** 2 - lo ** 2) / 2) / (hi - lo)

        integrand = lambda x: g(x) * inner(pay.B(sched_fb.mu(x)))
    return (1 - rho) * _integrate_flow(sched_fb, integrand)


def run() -> bool:
    checks: dict = {}
    notes: list[str] = []
    auction = auction_rows(checks)
    write_csv("tables/auction_primitives.csv",
              ["parameter_set", "r", "p", "t_0", "t_H", "t_L", "g_H", "g_L", "Delta_T", "B_m", "B_prior", "B_M"], auction)

    eq_rows, dev_rows, ext_rows, fb_rows = [], [], [], []
    eps_C = BENCHMARK_EXTRA["cost_halfwidth"]
    economies = []
    for noise in (Noise.LAPLACE, Noise.LOGISTIC):
        for cost in (CostLaw.ATOMS, CostLaw.UNIFORM_MIXTURE):
            economies.append(BENCHMARK.with_(noise=noise, cost_law=cost, cost_halfwidth=eps_C if cost == CostLaw.UNIFORM_MIXTURE else "0"))

    for prim in economies:
        tag = f"{prim.noise.value}_{prim.cost_law.value}"
        results = {}
        for sname, rs in BENCHMARK_STRENGTHS.items():
            r = float(rs)
            pay = payoffs_closed_form(prim, r)
            mg = node_margins(prim, pay)
            base_row = {"parameter_set": prim.parameter_set, "noise": prim.noise.value, "cost_law": prim.cost_law.value, "r": rs}
            prefix = {**base_row, "noise": prim.noise.value}
            node = {"pay": pay, "mg": mg}

            # --- feedback equilibrium candidates: pooling and full orders ---------------------
            accepted_fb = []
            for cand in (pooling_candidate(prim, pay), full_order_candidate(prim, pay)):
                val = validate(cand.sched, CONTROLS)
                status = classify_feedback(cand.branch, mg, val)
                o = val.outcome
                # cross-check full-order closed forms
                if cand.branch == "full_orders" and prim.cost_law == CostLaw.ATOMS:
                    cf = laplace_full_order_objects(prim, pay) if prim.noise == Noise.LAPLACE else logistic_full_order_objects(prim, pay)
                    d = max(abs(cf["E"] - o.E), abs(cf["e_H"] - o.e_H), abs(cf["e_L"] - o.e_L), abs(cf["O_H"] - o.O_H))
                    checks[f"full_order_closed_form_{tag}_{sname}"] = {"max_abs_diff": d, "pass": d <= TOL, "x_star_formula": cf["x_star"], "x_star_root": o.x_star}
                    if d > TOL:
                        val.breaches.append(f"closed_form_mismatch={d:.3e}")
                        status = "rejected: closed-form mismatch"
                eq_rows.append({**base_row, "experiment": "feedback", "q_H": cand.profile.q_H[0], "q_L": cand.profile.q_L[0],
                                "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "W": o.W,
                                "expected_preparation_cost": o.expected_preparation_cost, "tau": o.tau, "x_star": o.x_star,
                                "matched_dividend": 0.0, "status": status, "accepted": val.accepted})
                dev_rows += deviation_rows({**prefix, "experiment": "feedback"}, val)
                checks[f"feedback_{cand.branch}_{tag}_{sname}"] = {"accepted": val.accepted, "breaches": val.breaches,
                                                                  "epsilon_P": val.epsilon_P, "epsilon_e": val.epsilon_e,
                                                                  "epsilon_q_initial": val.epsilon_q, "epsilon_q_refined": val.epsilon_q_refined,
                                                                  "J": cand.diagnostics}
                if val.accepted:
                    accepted_fb.append((cand, val, status))
            node["feedback"] = accepted_fb
            if len(accepted_fb) != 1:
                notes.append(f"{tag} r={rs}: {len(accepted_fb)} accepted feedback candidates among pooling/full orders")

            # --- frozen-profile control: full orders imposed, buyer reoptimizes ------------
            cand = full_order_candidate(prim, pay)
            val = validate_control(cand.sched, CONTROLS)
            o = val.outcome
            gain = max(val.epsilon_q, val.epsilon_q_refined)
            status = ("numerical diagnostic (fixed full-order profile; investor deviation gain "
                      f"{gain:.3e}; not an equilibrium assertion)") if val.accepted else "rejected: " + "; ".join(val.breaches)
            eq_rows.append({**base_row, "experiment": "frozen", "q_H": 1.0, "q_L": -1.0, "e_H": o.e_H, "e_L": o.e_L, "E": o.E,
                            "O_H": o.O_H, "R_T": o.R_T, "W": o.W, "expected_preparation_cost": o.expected_preparation_cost,
                            "tau": o.tau, "x_star": o.x_star, "matched_dividend": 0.0, "status": status, "accepted": val.accepted})
            dev_rows += deviation_rows({**prefix, "experiment": "frozen"}, val)
            checks[f"frozen_{tag}_{sname}"] = {"accepted": val.accepted, "investor_deviation_gain": gain, "breaches": val.breaches}

            # --- price-hidden equilibrium: reoptimize investor with buyer at the prior -------
            accepted_hidden = []
            for cand in (pooling_candidate(prim, pay, "price_hidden"), full_order_candidate(prim, pay, "price_hidden")):
                val = validate(cand.sched, CONTROLS)
                status = classify_hidden(cand.branch, mg, val)
                o = val.outcome
                eq_rows.append({**base_row, "experiment": "price_hidden", "q_H": cand.profile.q_H[0], "q_L": cand.profile.q_L[0],
                                "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "W": o.W,
                                "expected_preparation_cost": o.expected_preparation_cost, "tau": o.tau, "x_star": float("nan"),
                                "matched_dividend": 0.0, "status": status, "accepted": val.accepted})
                dev_rows += deviation_rows({**prefix, "experiment": "price_hidden"}, val)
                checks[f"hidden_{cand.branch}_{tag}_{sname}"] = {"accepted": val.accepted, "breaches": val.breaches}
                if val.accepted:
                    accepted_hidden.append((cand, val, status))
            node["hidden"] = accepted_hidden
            if len(accepted_hidden) != 1:
                notes.append(f"{tag} r={rs}: {len(accepted_hidden)} accepted price-hidden candidates")

            # --- matched-dividend control ---------------------------------------------------
            if len(accepted_fb) == 1 and len(accepted_hidden) == 1:
                cfb, vfb, _ = accepted_fb[0]
                chd, vhd, _ = accepted_hidden[0]
                D0 = vfb.outcome.R_T - vhd.outcome.R_T
                cand = full_order_candidate(prim, pay, "price_hidden", D0) if chd.branch == "full_orders" else \
                    pooling_candidate(prim, pay, "price_hidden", D0)
                val = validate(cand.sched, CONTROLS)
                o = val.outcome
                xs = np.linspace(-6, 6, 2401)
                inv = max(float(np.max(np.abs(cand.sched.A(xs, s) - chd.sched.A(xs, s)))) for s in "HL")
                inv = max(inv, abs(o.e_H - vhd.outcome.e_H), abs(o.e_L - vhd.outcome.e_L))
                price_shift = float(np.max(np.abs(cand.sched.price(xs) - chd.sched.price(xs) - D0)))
                ok = val.accepted and inv <= TOL and price_shift <= TOL and abs(o.mean_price - vfb.outcome.R_T) <= TOL
                status = ("numerical diagnostic (level-matching dividend; residuals, orders and entry unchanged)" if ok
                          else "rejected: " + "; ".join(val.breaches + ([f"residual_invariance={inv:.3e}"] if inv > TOL else [])))
                eq_rows.append({**base_row, "experiment": "matched_dividend", "q_H": cand.profile.q_H[0], "q_L": cand.profile.q_L[0],
                                "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "W": o.W,
                                "expected_preparation_cost": o.expected_preparation_cost, "tau": o.tau, "x_star": float("nan"),
                                "matched_dividend": D0, "status": status, "accepted": ok})
                dev_rows += deviation_rows({**prefix, "experiment": "matched_dividend"}, val)
                checks[f"matched_dividend_{tag}_{sname}"] = {"accepted": ok, "residual_invariance_error": inv, "price_shift_error": price_shift,
                                                            "mean_price_matches_feedback_revenue": abs(o.mean_price - vfb.outcome.R_T)}
                # --- feedback comparisons (welfare and revenue) ---------------------------------
                dW_direct = welfare_direct(cfb.sched, chd.sched) if cfb.branch == "full_orders" else 0.0
                W_gain = vfb.outcome.W - vhd.outcome.W
                dR_cond = 0.5 * ((vfb.outcome.e_H - vhd.outcome.e_H) * pay.w_H + (vfb.outcome.e_L - vhd.outcome.e_L) * pay.w_L)
                dR_price = vfb.outcome.mean_price - vhd.outcome.mean_price
                w_err, r_err = abs(dW_direct - W_gain), abs(dR_cond - dR_price)
                same_profile = cfb.profile == chd.profile
                fb_ok = w_err <= TOL and r_err <= TOL and (same_profile or (abs(W_gain) <= TOL))
                fb_status = ("analytical (Proposition 2 region: matched full orders)" if same_profile and cfb.branch == "full_orders"
                             and mg.low_cost_floor > 0 and mg.full_unique_bound > 0 and mg.high_prior_exclusion > 0 else
                             "numerical diagnostic (profiles differ or theorem margins not all positive)")
                fb_rows.append({**base_row, "W_feedback": vfb.outcome.W, "W_hidden": vhd.outcome.W, "W_gain": W_gain,
                                "R_T_feedback": vfb.outcome.R_T, "R_T_hidden": vhd.outcome.R_T, "R_T_gain": dR_cond,
                                "matched_dividend": D0, "welfare_identity_error": w_err, "revenue_identity_error": r_err,
                                "residual_invariance_error": inv, "status": fb_status, "accepted": fb_ok})
                checks[f"feedback_comparison_{tag}_{sname}"] = {"accepted": fb_ok, "welfare_identity_error": w_err, "revenue_identity_error": r_err}
            results[sname] = node

        # --- extensions row: theorem margins at (r_weak, r_strong) ---------------------------
        pay0, pay1 = results["r_weak"]["pay"], results["r_strong"]["pay"]
        zeta = theorem_margins(prim, pay0, pay1)
        fw, fs = results["r_weak"]["feedback"], results["r_strong"]["feedback"]
        ok = len(fw) == 1 and len(fs) == 1
        all_pos = all(z > 0 for z in zeta.values())
        status = ("analytical (all five Theorem 1 margins strictly positive)" if all_pos and ok else
                  "numerical diagnostic (a theorem margin is not strictly positive or a node has multiple accepted candidates)")
        ext_rows.append({"parameter_set": prim.parameter_set, "noise": prim.noise.value, "cost_law": prim.cost_law.value,
                         "r_weak": BENCHMARK_STRENGTHS["r_weak"], "r_strong": BENCHMARK_STRENGTHS["r_strong"],
                         "E_weak": fw[0][1].outcome.E if ok else float("nan"), "E_strong": fs[0][1].outcome.E if ok else float("nan"),
                         "O_H_weak": fw[0][1].outcome.O_H if ok else float("nan"), "O_H_strong": fs[0][1].outcome.O_H if ok else float("nan"),
                         **zeta, "status": status, "accepted": ok})
        checks[f"extensions_{tag}"] = {"margins": zeta, "all_positive": all_pos, "accepted": ok}

    write_csv("tables/equilibrium_controls.csv",
              ["parameter_set", "noise", "cost_law", "r", "experiment", "q_H", "q_L", "e_H", "e_L", "E", "O_H", "R_T", "W",
               "expected_preparation_cost", "tau", "x_star", "matched_dividend", "status", "accepted"], eq_rows)
    write_csv("tables/extensions.csv",
              ["parameter_set", "noise", "cost_law", "r_weak", "r_strong", "E_weak", "E_strong", "O_H_weak", "O_H_strong",
               "zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1", "status", "accepted"], ext_rows)
    write_csv("numerics/baseline_deviations.csv",
              ["parameter_set", "experiment", "noise", "cost_law", "r", "state", "q", "U(q)", "U(candidate)", "deviation_gain",
               "quadrature_error", "tail_bound"], dev_rows)
    write_csv("numerics/feedback_comparisons.csv",
              ["parameter_set", "noise", "cost_law", "r", "W_feedback", "W_hidden", "W_gain", "R_T_feedback", "R_T_hidden", "R_T_gain",
               "matched_dividend", "welfare_identity_error", "revenue_identity_error", "residual_invariance_error", "status", "accepted"], fb_rows)

    # --- two returns figure data -----------------------------------------------------------------
    m, M = posterior_bounds(BENCHMARK.fb)
    tr_rows = []
    for rs in decimal_range("1.005", "3.800", "0.005"):
        r = float(rs)
        pay = payoffs_closed_form(BENCHMARK, r)
        for mu_name, mu in (("m", m), ("1/2", 0.5), ("M", M)):
            tr_rows.append({"r": rs, "mu": mu, "Delta_T": pay.Delta_T, "B_r(mu)": pay.B(mu),
                            "d_Delta_T_dr": dDelta_T_dr(BENCHMARK, r), "d_B_r_mu_dr": dB_dr(BENCHMARK, r, mu)})
    write_csv("figures_data/two_returns.csv", ["r", "mu", "Delta_T", "B_r(mu)", "d_Delta_T_dr", "d_B_r_mu_dr"], tr_rows)

    # --- refinement pass on the declared Laplace/atoms nodes (tightened controls) ----------------
    tight = CONTROLS.tightened()
    for sname, rs in BENCHMARK_STRENGTHS.items():
        pay = payoffs_closed_form(BENCHMARK, float(rs))
        cand = pooling_candidate(BENCHMARK, pay) if sname == "r_weak" else full_order_candidate(BENCHMARK, pay)
        v = validate(cand.sched, tight)
        checks[f"refinement_pass_{sname}"] = {"controls": tight.as_dict(), "accepted": v.accepted, "epsilon_q": v.epsilon_q_refined,
                                              "E": v.outcome.E, "breaches": v.breaches}

    passed = all(c.get("pass", c.get("accepted", True)) for k, c in checks.items()
                 if not k.startswith(("feedback_pooling", "feedback_full", "hidden_")))  # candidate rejections are legitimate
    # required declared rows must be accepted
    required = [("feedback", "Laplace", "atoms", "1.2"), ("feedback", "Laplace", "atoms", "3"), ("feedback", "Laplace", "atoms", "3.6"),
                ("frozen", "Laplace", "atoms", "1.2"), ("frozen", "Laplace", "atoms", "3"), ("price_hidden", "Laplace", "atoms", "1.2"),
                ("price_hidden", "Laplace", "atoms", "3"), ("matched_dividend", "Laplace", "atoms", "3"),
                ("feedback", "logistic", "atoms", "3"), ("feedback", "Laplace", "uniform_mixture", "3"), ("feedback", "logistic", "uniform_mixture", "3")]
    for exp, nz, cl, r in required:
        hits = [row for row in eq_rows if row["experiment"] == exp and row["noise"] == nz and row["cost_law"] == cl and row["r"] == r and row["accepted"]]
        checks[f"required_row_{exp}_{nz}_{cl}_{r}"] = {"accepted_rows": len(hits), "pass": len(hits) == 1}
        passed = passed and len(hits) == 1
    outputs = ["tables/auction_primitives.csv", "tables/equilibrium_controls.csv", "tables/extensions.csv",
               "numerics/baseline_deviations.csv", "numerics/feedback_comparisons.csv", "figures_data/two_returns.csv"]
    write_manifest("c1_baseline", {"benchmark": BENCHMARK.__dict__, "strengths": BENCHMARK_STRENGTHS, "extra": BENCHMARK_EXTRA,
                                   "economies": [f"{p.noise.value}/{p.cost_law.value}" for p in economies]},
                   "Closed-form auction payoffs checked against direct integration of OA.50; candidate schedules (pooling, full "
                   "orders) validated by flow- and cost-based entry integration, pointwise price identity, entry optimality, "
                   "posterior inversion, and global order-deviation scans on the initial and refined grids with segment-wise "
                   "Gauss-Legendre quadrature and analytic Laplace tails (numeric logistic tails with recorded bound).",
                   CONTROLS.as_dict(), outputs, checks, passed, notes)
    print("C.1 passed" if passed else "C.1 FAILED", "| notes:", notes)
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
