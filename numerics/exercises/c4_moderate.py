"""C.4: moderate acquisition values and the constructive nonemptiness sequence."""
from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import payoffs_closed_form, payoffs_integrated  # noqa: E402
from numerics.exercises.common import classify_feedback, classify_hidden, node_margins, theorem_margins, validate_control  # noqa: E402
from numerics.information import laplace_full_order_objects  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.params import CONTROLS, MODERATE, MODERATE_STRENGTHS  # noqa: E402
from numerics.search import full_order_candidate, pooling_candidate  # noqa: E402
from numerics.validation import validate  # noqa: E402

TOL = CONTROLS.independent_formula_acceptance


def nonemptiness_rows(checks: dict) -> list[dict]:
    """A.6 construction with (OA.69) choices, evaluated in 50-digit arithmetic."""
    mp.mp.dps = 50
    ell, p, rho, b = mp.mpf(1), mp.mpf("0.5"), mp.mpf("0.25"), mp.mpf(2)
    m = 1 / (1 + mp.e ** (2 / b))
    M = 1 - m
    rows = []
    for ratio in ("1.05", "1.10", "1.25", "1.50", "2.00"):
        h = ell * mp.mpf(ratio)
        D = h - ell
        first_feasible = None
        for j in range(1, 21):
            delta = D / mp.mpf(2) ** j
            r1 = ell + delta
            r0 = ell + delta * delta / D

            def prim(r):
                t0 = p * (1 - p / r)
                tH = r / 2 + p * p / (2 * r)
                tL = ell - (ell * ell - p * p) / (2 * r)
                gH, gL = h - tH, (ell * ell - p * p) / (2 * r)
                return gH, gL, tH - tL

            gH0, gL0, D0 = prim(r0)
            gH1, gL1, D1 = prim(r1)
            B = lambda gH, gL, mu: gL + mu * (gH - gL)
            k = (D0 + (1 - 1 / b) * rho * m * D1) / 2
            cH = (B(gH0, gL0, mp.mpf("0.5")) + B(gH1, gL1, M)) / 2
            cL = B(gH1, gL1, m) / 2
            margins = {
                "zeta_L": B(gH1, gL1, m) - cL,
                "zeta_H0": cH - B(gH0, gL0, mp.mpf("0.5")),
                "zeta_H1": B(gH1, gL1, M) - cH,
                "zeta_0": k - D0,
                "zeta_1": (1 - 1 / b) * rho * m * D1 - k,
                "cost_order": cH - cL,
                "support_r0": r0 - ell,
                "support_r1_below_h": h - r1,
                "order_r0_r1": r1 - r0,
                "cL_positive": cL,
            }
            mn = min(margins.values())
            feasible = mn > 0
            reason = "all theorem inequalities strict" if feasible else \
                "; ".join(f"{k_}<=0" for k_, v in margins.items() if v <= 0)
            if feasible and first_feasible is None:
                first_feasible = j
            rows.append({"h_over_ell": ratio, "j": j, "delta": mp.nstr(delta, 30), "r_weak": mp.nstr(r0, 30), "r_strong": mp.nstr(r1, 30),
                         "k": mp.nstr(k, 30), "c_L": mp.nstr(cL, 30), "c_H": mp.nstr(cH, 30), "all_margins_min": mp.nstr(mn, 20),
                         "feasible": feasible, "arithmetic_precision": f"mpmath dps={mp.mp.dps}", "reason": reason})
        checks[f"nonemptiness_first_feasible_j_ratio_{ratio}"] = {"first_feasible_j": first_feasible, "pass": first_feasible is not None}
    return rows


def run() -> bool:
    checks, notes = {}, []
    prim = MODERATE
    pays = {}
    for name, rs in MODERATE_STRENGTHS.items():
        pay = payoffs_closed_form(prim, float(rs))
        pay_i, err = payoffs_integrated(prim, float(rs))
        d = max(abs(getattr(pay, a) - getattr(pay_i, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L"))
        checks[f"auction_integration_{name}"] = {"max_abs_diff": d, "pass": d <= TOL}
        pays[name] = pay
    zeta = theorem_margins(prim, pays["r_weak"], pays["r_strong"])
    all_pos = all(z > 0 for z in zeta.values())
    checks["theorem_margins"] = {**zeta, "all_positive": all_pos, "pass": all_pos}

    ctrl_rows = []
    results = {}
    for name, rs in MODERATE_STRENGTHS.items():
        pay = pays[name]
        mg = node_margins(prim, pay)
        acc = []
        for cand in (pooling_candidate(prim, pay), full_order_candidate(prim, pay)):
            val = validate(cand.sched, CONTROLS)
            status = classify_feedback(cand.branch, mg, val)
            if cand.branch == "full_orders":
                cf = laplace_full_order_objects(prim, pay)
                d = abs(cf["E"] - val.outcome.E)
                checks[f"full_order_closed_form_{name}"] = {"diff": d, "pass": d <= TOL}
            o = val.outcome
            ctrl_rows.append({"parameter_set": "moderate", "noise": prim.noise.value, "cost_law": prim.cost_law.value, "r": rs, "experiment": "feedback",
                              "q_H": cand.profile.q_H[0], "q_L": cand.profile.q_L[0], "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H,
                              "R_T": o.R_T, "W": o.W, "expected_preparation_cost": o.expected_preparation_cost, "tau": o.tau, "x_star": o.x_star,
                              "status": status, "accepted": val.accepted})
            checks[f"feedback_{cand.branch}_{name}"] = {"accepted": val.accepted, "breaches": val.breaches, "eps_q": max(val.epsilon_q, val.epsilon_q_refined)}
            if val.accepted:
                acc.append((cand, val))
        results[name] = acc
        # controls
        cand = full_order_candidate(prim, pay)
        val = validate_control(cand.sched, CONTROLS)
        o = val.outcome
        ctrl_rows.append({"parameter_set": "moderate", "noise": prim.noise.value, "cost_law": prim.cost_law.value, "r": rs, "experiment": "frozen",
                          "q_H": 1.0, "q_L": -1.0, "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "W": o.W,
                          "expected_preparation_cost": o.expected_preparation_cost, "tau": o.tau, "x_star": o.x_star,
                          "status": f"numerical diagnostic (fixed full-order profile; investor deviation gain {max(val.epsilon_q, val.epsilon_q_refined):.3e})",
                          "accepted": val.accepted})
        for cand in (pooling_candidate(prim, pay, "price_hidden"), full_order_candidate(prim, pay, "price_hidden")):
            val = validate(cand.sched, CONTROLS)
            o = val.outcome
            ctrl_rows.append({"parameter_set": "moderate", "noise": prim.noise.value, "cost_law": prim.cost_law.value, "r": rs, "experiment": "price_hidden",
                              "q_H": cand.profile.q_H[0], "q_L": cand.profile.q_L[0], "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H,
                              "R_T": o.R_T, "W": o.W, "expected_preparation_cost": o.expected_preparation_cost, "tau": o.tau, "x_star": float("nan"),
                              "status": classify_hidden(cand.branch, mg, val), "accepted": val.accepted})
    ok = len(results["r_weak"]) == 1 and len(results["r_strong"]) == 1 and all_pos
    vw, vs = results["r_weak"][0][1].outcome, results["r_strong"][0][1].outcome
    status = "analytical (all five Theorem 1 margins strictly positive)" if ok else "numerical diagnostic"
    row = {**prim.columns(), "r_weak": MODERATE_STRENGTHS["r_weak"], "r_strong": MODERATE_STRENGTHS["r_strong"], **zeta,
           "E_weak": vw.E, "E_strong": vs.E, "O_H_weak": vw.O_H, "O_H_strong": vs.O_H, "status": status, "accepted": ok}
    write_csv("numerics/moderate_values.csv", ["h", "ell", "p", "rho", "c_L", "c_H", "b", "k", "r_weak", "r_strong", "zeta_L", "zeta_H0",
                                               "zeta_H1", "zeta_0", "zeta_1", "E_weak", "E_strong", "O_H_weak", "O_H_strong", "status", "accepted"], [row])
    write_csv("numerics/moderate_controls.csv", ["parameter_set", "noise", "cost_law", "r", "experiment", "q_H", "q_L", "e_H", "e_L", "E", "O_H",
                                                 "R_T", "W", "expected_preparation_cost", "tau", "x_star", "status", "accepted"], ctrl_rows)
    ne_rows = nonemptiness_rows(checks)
    write_csv("numerics/nonemptiness_construction.csv", ["h_over_ell", "j", "delta", "r_weak", "r_strong", "k", "c_L", "c_H", "all_margins_min",
                                                         "feasible", "arithmetic_precision", "reason"], ne_rows)
    passed = ok and all(c.get("pass", True) for c in checks.values())
    write_manifest("c4_moderate", {"moderate": prim.__dict__, "strengths": MODERATE_STRENGTHS, "ratios": ["1.05", "1.10", "1.25", "1.50", "2.00"], "j": "1..20"},
                   "Moderate declaration solved with the C.1 machinery (independent auction integration, analytical margins, validated "
                   "pooling/full-order candidates and controls); nonemptiness sequence per A.6 with OA.69 choices in 50-digit arithmetic.",
                   CONTROLS.as_dict(), ["numerics/moderate_values.csv", "numerics/moderate_controls.csv", "numerics/nonemptiness_construction.csv"],
                   checks, passed, notes)
    print("C.4 passed" if passed else "C.4 FAILED", {k: v for k, v in checks.items() if "first_feasible" in k}, "E:", vw.E, vs.E)
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
