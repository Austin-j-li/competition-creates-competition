"""C.2: exact thresholds, interval certificates, and the equilibrium correspondence on the declared grid."""
from __future__ import annotations

import sys
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import payoffs_closed_form  # noqa: E402
from numerics.certificates import certify, lo, hi, endpoint_str as es  # noqa: E402
from numerics.exercises.common import node_margins  # noqa: E402
from numerics.information import OrderProfile, make_schedule  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.params import (BENCHMARK, BENCHMARK_STRENGTHS, CERTIFICATE_BRACKETS, CONTROLS, CORRESPONDENCE_MESH,  # noqa: E402
                             CORRESPONDENCE_OFFSETS, decimal_range)
from numerics.search import (asymmetric_candidate, asymmetric_roots, full_order_candidate, mixed_support_search,  # noqa: E402
                             pooling_candidate, pure_fixed_points, derivative_cover)
from numerics.thresholds import compute_thresholds  # noqa: E402
from numerics.validation import validate  # noqa: E402

PRIM = BENCHMARK
COLUMNS = ["r", "branch", "q_H", "q_L", "v", "e_H", "e_L", "E", "O_H", "R_T", "tau", "x_star", "pooling_exists",
           "pooling_unique_bound", "full_unique_bound", "existence_status", "uniqueness_status", "accepted",
           "multiplicity_found", "epsilon_P", "epsilon_e", "epsilon_q", "tail_bound", "unresolved_reason"]
MIXED_COLUMNS = ["r", "branch", "state", "support_index", "q", "weight", "U(q)", "support_gap", "off_support_gain_bound", "accepted", "status"]


def strength_grid() -> list[str]:
    start, stop, step = CORRESPONDENCE_MESH
    pts = set(decimal_range(start, stop, step))
    pts |= set(BENCHMARK_STRENGTHS.values())
    pts |= {r for r, _, _ in CERTIFICATE_BRACKETS}
    for row in compute_thresholds(PRIM):
        if row["boundary"] in ("pooling_unique_sufficient", "pooling_existence", "full_orders_unique_sufficient", "high_cost_ceiling"):
            val = Decimal(repr(float(row["value"])))
            pts.add(str(val))
            for off in CORRESPONDENCE_OFFSETS:
                pts.add(str(val - Decimal(off)))
                pts.add(str(val + Decimal(off)))
    return sorted(pts, key=Decimal)


def _row(rs: str, branch: str, cand, val, mg, existence: str, uniqueness: str, reason: str = "") -> dict:
    o = val.outcome
    return {"r": rs, "branch": branch, "q_H": cand.profile.q_H[0] if cand.profile.is_pure else "mixed",
            "q_L": cand.profile.q_L[0] if cand.profile.is_pure else "mixed", "v": -cand.profile.q_L[0],
            "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "tau": o.tau, "x_star": o.x_star,
            "pooling_exists": mg.pooling_exists, "pooling_unique_bound": mg.pooling_unique_bound,
            "full_unique_bound": mg.full_unique_bound, "existence_status": existence, "uniqueness_status": uniqueness,
            "accepted": val.accepted, "multiplicity_found": False, "epsilon_P": val.epsilon_P, "epsilon_e": val.epsilon_e,
            "epsilon_q": max(val.epsilon_q, val.epsilon_q_refined), "tail_bound": val.tail_bound,
            "unresolved_reason": reason if reason else ("" if val.accepted else "; ".join(val.breaches))}


def solve_node(rs: str, certified: dict[str, tuple[str, str]], do_pure: bool = True, do_mixed: bool = True) -> tuple[list[dict], list[dict], dict]:
    r = float(rs)
    pay = payoffs_closed_form(PRIM, r)
    mg = node_margins(PRIM, pay)
    rows, mixed_rows, diag = [], [], {"r": rs}
    accepted_profiles = []

    # pooling ------------------------------------------------------------------
    cand = pooling_candidate(PRIM, pay)
    val = validate(cand.sched, CONTROLS)
    ex = ("analytical" if val.accepted and mg.in_domain and mg.pooling_exists >= 0 else
          "analytical (outside maintained domain; prior entry rule evaluated)" if val.accepted else "rejected")
    un = "analytical (Delta_T < k)" if mg.in_domain and mg.pooling_unique_bound > 0 else "not established"
    rows.append(_row(rs, "pooling", cand, val, mg, ex, un))
    if val.accepted:
        accepted_profiles.append((0.0, 0.0))

    # full orders ---------------------------------------------------------------
    cand = full_order_candidate(PRIM, pay)
    val = validate(cand.sched, CONTROLS)
    cover = derivative_cover(cand.sched, "H", CONTROLS.certificate_derivative_intervals) if val.accepted else {}
    if val.accepted:
        if mg.low_cost_floor > 0 and mg.full_unique_bound > 0:
            ex = "analytical (uniform derivative bound)"
        elif mg.low_cost_floor > 0 and cand.diagnostics["J_margin"] > 0:
            ex = "analytical (candidate J test, OA.22)"
        else:
            ex = "numerical diagnostic"
    else:
        ex = "rejected"
    un = "analytical ((1-1/b) rho m Delta_T > k)" if mg.low_cost_floor > 0 and mg.full_unique_bound > 0 else "not established"
    rows.append(_row(rs, "full_orders", cand, val, mg, ex, un))
    diag["full_J"] = cand.diagnostics
    diag["full_cover"] = cover
    if val.accepted:
        accepted_profiles.append((1.0, 1.0))

    # asymmetric (1, -v) --------------------------------------------------------
    extra = [tuple(float(x) for x in certified[rs])] if rs in certified else None
    ar = asymmetric_roots(PRIM, pay, extra_brackets=extra)
    diag["asym_roots"] = ar["roots"]
    diag["asym_tangencies"] = ar["tangencies"]
    for v in ar["roots"]:
        cand = asymmetric_candidate(PRIM, pay, v)
        if abs(cand.diagnostics["Psi"]) > 1e-6:
            # sign change across a discontinuity of Psi (threshold reaches the plateau boundary), not a root
            val = validate(cand.sched, CONTROLS)
            rows.append(_row(rs, "asymmetric_discontinuity", cand, val, mg, "rejected", "not established",
                             f"Psi sign change without root: |Psi|={abs(cand.diagnostics['Psi']):.3e} at tau = M_v boundary"))
            continue
        val = validate(cand.sched, CONTROLS)
        ex = "computer-assisted" if (rs in certified and val.accepted and abs(v - 0.5 * sum(map(float, certified[rs]))) < 1e-6) \
            else ("numerical diagnostic" if val.accepted else "rejected")
        rows.append(_row(rs, "asymmetric", cand, val, mg, ex, "not established"))
        if val.accepted:
            accepted_profiles.append((1.0, v))
    for v, resid in ar["tangencies"]:
        cand = asymmetric_candidate(PRIM, pay, v)
        val = validate(cand.sched, CONTROLS)
        rows.append(_row(rs, "asymmetric_tangency", cand, val, mg, "open" if not val.accepted else "numerical diagnostic",
                         "not established", f"local |Psi| minimum {resid:.3e} without sign change; unresolved"))
        if val.accepted:
            accepted_profiles.append((1.0, v))

    # other pure profiles (u, -v) ------------------------------------------------
    if do_pure:
        fp = pure_fixed_points(PRIM, pay, inits=[(u, v) for u in (0.2, 0.6, 0.95) for v in (0.2, 0.6, 0.95)], max_iter=40)
        diag["pure_unconverged"] = len(fp["unconverged"])
        for u, v, init in fp["fixed_points"]:
            if any(abs(u - au) < 1e-5 and abs(v - av) < 1e-5 for au, av in accepted_profiles):
                continue
            cand_sched = make_schedule(PRIM, pay, OrderProfile.pure(u, -v))
            from numerics.search import Candidate
            cand = Candidate("pure", cand_sched.profile, cand_sched, {"init": init})
            val = validate(cand.sched, CONTROLS)
            rows.append(_row(rs, "pure", cand, val, mg, "numerical diagnostic" if val.accepted else "rejected", "not established"))
            if val.accepted:
                accepted_profiles.append((u, v))
        if fp["unconverged"]:
            rows.append({"r": rs, "branch": "pure_search", "q_H": "n/a", "q_L": "n/a", "v": "n/a", "e_H": "n/a", "e_L": "n/a", "E": "n/a",
                         "O_H": "n/a", "R_T": "n/a", "tau": pay.tau(PRIM.fc_H), "x_star": "n/a", "pooling_exists": mg.pooling_exists,
                         "pooling_unique_bound": mg.pooling_unique_bound, "full_unique_bound": mg.full_unique_bound,
                         "existence_status": "open", "uniqueness_status": "not established", "accepted": False, "multiplicity_found": False,
                         "epsilon_P": "n/a", "epsilon_e": "n/a", "epsilon_q": "n/a", "tail_bound": "n/a",
                         "unresolved_reason": f"{len(fp['unconverged'])} best-response iterations did not converge"})

    # finite-support mixed search -------------------------------------------------
    if do_mixed:
        for mesh in (0.05, 0.025):
            ms = mixed_support_search(PRIM, pay, mesh=mesh, iters=150)
            prof = ms["profile"]
            status = "converged" if ms["converged"] else "not converged"
            if len(prof.q_H) == 1 and ms["converged"]:
                status += f" to pure candidate ({prof.q_H[0]:.6g},{prof.q_L[0]:.6g})"
                acc = False
            elif ms["converged"]:
                val = validate(ms["sched"], CONTROLS)
                acc = val.accepted
                from numerics.search import Candidate
                cand = Candidate("mixed", prof, ms["sched"], {})
                rows.append(_row(rs, "mixed", cand, val, mg, "numerical diagnostic" if acc else "rejected", "not established"))
            else:
                acc = False
            for j, (q, w) in enumerate(zip(prof.q_H, prof.w_H)):
                mixed_rows.append({"r": rs, "branch": f"mixed_mesh_{mesh}", "state": "H", "support_index": j, "q": q, "weight": w,
                                   "U(q)": float(ms["payoffs"][np.argmin(np.abs(ms["mesh_q"] - q))]), "support_gap": ms["support_gap"],
                                   "off_support_gain_bound": ms["off_support_gain"], "accepted": acc, "status": status})
            mixed_rows.append({"r": rs, "branch": f"mixed_mesh_{mesh}", "state": "L", "support_index": 0, "q": prof.q_L[0], "weight": 1.0,
                               "U(q)": "n/a", "support_gap": 0.0, "off_support_gain_bound": "n/a", "accepted": acc, "status": status})

    n_acc = sum(1 for row in rows if row["accepted"] is True)
    for row in rows:
        row["multiplicity_found"] = n_acc >= 2
    return rows, mixed_rows, diag


def _worker(args):
    return solve_node(*args)


def run(workers: int = 8, quick: bool = False) -> bool:
    checks, notes = {}, []
    # --- thresholds -------------------------------------------------------------------
    th = compute_thresholds(PRIM)
    write_csv("numerics/thresholds.csv", ["boundary", "value", "lower", "upper", "defining_residual", "in_support_domain",
                                          "low_cost_floor_valid", "interpretation"], th)
    for row in th:
        if isinstance(row["defining_residual"], float) and row["boundary"] not in ("m", "M", "laplace_entry_left_limit"):
            checks[f"threshold_{row['boundary']}"] = {"value": row["value"], "residual": row["defining_residual"],
                                                      "pass": abs(row["defining_residual"]) <= CONTROLS.independent_formula_acceptance}
    # --- certificates -----------------------------------------------------------------
    cert_rows = []
    for r_s, vl, vr in CERTIFICATE_BRACKETS:
        rec = certify(PRIM, r_s, vl, vr, CONTROLS)
        rec2 = certify(PRIM, r_s, vl, vr, CONTROLS, n=CONTROLS.certificate_refined_intervals)
        checks[f"certificate_{r_s}"] = {"accepted": rec.accepted, "predicates": rec.predicates, "failures": rec.failures,
                                        "refined_mesh_accepted": rec2.accepted,
                                        "Gamma_H_lower_refined": lo(rec2.values["Gamma_H"]) if "Gamma_H" in rec2.values else None}
        V = rec.values
        cert_rows.append({"r": r_s, "v_lower": vl, "v_upper": vr,
                          "Psi_left_lower": es(V["Psi_left"], "lower"), "Psi_left_upper": es(V["Psi_left"], "upper"),
                          "Psi_right_lower": es(V["Psi_right"], "lower"), "Psi_right_upper": es(V["Psi_right"], "upper"),
                          "Gamma_H_lower": es(V["Gamma_H"], "lower") if "Gamma_H" in V else "n/a",
                          "L_U_upper": es(V["L_U"], "upper") if "L_U" in V else "n/a",
                          "mesh_intervals": V.get("mesh_intervals", "n/a"), "interval_digits": CONTROLS.interval_decimal_precision,
                          "E_lower": es(V["E"], "lower") if "E" in V else "n/a", "E_upper": es(V["E"], "upper") if "E" in V else "n/a",
                          "pooling_margin_lower": es(V["pooling_margin"], "lower"),
                          "threshold_margin_lower": es(V["low_cost_margin"], "lower"),
                          "accepted": rec.accepted})
    write_csv("numerics/certificates.csv", ["r", "v_lower", "v_upper", "Psi_left_lower", "Psi_left_upper", "Psi_right_lower",
                                            "Psi_right_upper", "Gamma_H_lower", "L_U_upper", "mesh_intervals", "interval_digits",
                                            "E_lower", "E_upper", "pooling_margin_lower", "threshold_margin_lower", "accepted"], cert_rows)
    ordered = all(float(a["E_upper"]) < float(b["E_lower"]) for a, b in zip(cert_rows[:-1], cert_rows[1:]) if a["accepted"] and b["accepted"])
    checks["certified_entry_intervals_strictly_ordered"] = {"pass": ordered}

    # --- correspondence -----------------------------------------------------------------
    certified = {r: (vl, vr) for r, vl, vr in CERTIFICATE_BRACKETS}
    grid = strength_grid()
    if quick:
        grid = [g for g in grid if Decimal(g) % Decimal("0.1") == 0 or g in certified or g in BENCHMARK_STRENGTHS.values()]
    tasks = [(rs, certified) for rs in grid]
    rows, mixed_rows, diags = [], [], []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for rws, mrows, dg in ex.map(_worker, tasks, chunksize=2):
            rows += rws
            mixed_rows += mrows
            diags.append(dg)
    # --- refinement where accepted branch sets change between adjacent grid nodes -------------
    def accepted_set(rs: str) -> frozenset:
        return frozenset(row["branch"] for row in rows if row["r"] == rs and row["accepted"] is True)
    refine_pairs = []
    base_grid = [g for g in grid]
    for a, b_ in zip(base_grid[:-1], base_grid[1:]):
        if accepted_set(a) != accepted_set(b_) and Decimal(b_) - Decimal(a) > Decimal("0.001"):
            refine_pairs.append((a, b_))
    refine_nodes = set()
    for a, b_ in refine_pairs:
        x = Decimal(a) + Decimal("0.001")
        while x < Decimal(b_):
            refine_nodes.add(str(x))
            x += Decimal("0.001")
    refine_nodes -= set(grid)
    refine_nodes = sorted(refine_nodes, key=Decimal)
    if refine_nodes and not quick:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for rws, mrows, dg in ex.map(_worker, [(rs, certified) for rs in refine_nodes], chunksize=2):
                rows += rws
                mixed_rows += mrows
                diags.append(dg)
    rows.sort(key=lambda row: (Decimal(row["r"]), row["branch"]))
    mixed_rows.sort(key=lambda row: (Decimal(row["r"]), row["branch"], row["state"], row["support_index"]))
    write_csv("numerics/correspondence.csv", COLUMNS, rows)
    write_csv("numerics/mixed_supports.csv", MIXED_COLUMNS, mixed_rows)

    # --- summary checks -----------------------------------------------------------------------
    n_open = sum(1 for row in rows if row["existence_status"] == "open")
    n_multi = len({row["r"] for row in rows if row["multiplicity_found"] is True})
    checks["correspondence"] = {"nodes": len(grid) + len(refine_nodes), "refined_nodes": len(refine_nodes), "refinement_pairs": refine_pairs,
                                "refinement_rule": "adjacent grid nodes whose accepted branch sets differ are refined to spacing 0.001",
                                "open_rows": n_open, "nodes_with_multiplicity": n_multi,
                                "asymmetric_accepted_nodes": sorted({row["r"] for row in rows if row["branch"] == "asymmetric" and row["accepted"] is True}, key=Decimal)}
    # cross-checks against declared strengths
    for rs, want in (("1.2", "pooling"), ("3", "full_orders"), ("3.6", "full_orders")):
        acc = accepted_set(rs)
        checks[f"declared_node_{rs}"] = {"accepted_branches": sorted(acc), "pass": want in acc}
    for r_s, vl, vr in CERTIFICATE_BRACKETS:
        hits = [row for row in rows if row["r"] == r_s and row["branch"] == "asymmetric" and row["accepted"] is True
                and float(vl) <= float(row["v"]) <= float(vr)]
        checks[f"certified_node_root_in_bracket_{r_s}"] = {"pass": len(hits) == 1, "v": [row["v"] for row in hits]}
    passed = all(c.get("pass", c.get("accepted", True)) for c in checks.values())
    outputs = ["numerics/thresholds.csv", "numerics/certificates.csv", "numerics/correspondence.csv", "numerics/mixed_supports.csv"]
    write_manifest("c2_correspondence", {"benchmark": PRIM.__dict__, "mesh": CORRESPONDENCE_MESH, "offsets": CORRESPONDENCE_OFFSETS,
                                         "certificate_brackets": CERTIFICATE_BRACKETS, "grid_size": len(grid), "quick": quick},
                   "Exact boundaries from Proposition 3 with residual checks; interval certificates per Appendix B (mpmath iv, "
                   "exact antiderivatives, uniform high-type cover over the root bracket, mesh 200 and 400); at each strength node "
                   "pooling, full-order, asymmetric (1,-v) roots by sign-change bracketing plus |Psi| minimization, pure (u,-v) "
                   "best-response fixed points from 9 initializations, and finite-support mixed search on meshes 0.05 and 0.025; "
                   "every candidate validated independently; refinement to 0.001 where accepted branch sets change.",
                   CONTROLS.as_dict(), outputs, checks, passed, notes)
    print("C.2 passed" if passed else "C.2 FAILED", checks["correspondence"])
    return passed


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    sys.exit(0 if run(quick=quick) else 1)
