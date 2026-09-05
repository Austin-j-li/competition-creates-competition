"""C.2: exact thresholds, interval certificates, and the equilibrium correspondence on the declared grid.

Peer-circulation revision (S3): canonical Decimal node keys; every candidate carries its complete continuation
identity (numerics.continuations) and is deduplicated by that identity, with the raw attempts kept in
`numerics/correspondence_attempts.csv`; every validated row carries a separate error budget checked against the
declared quadrature targets and their refinement; the mixed search runs documented starts with a stated budget
and writes an attempt ledger (`numerics/mixed_search_attempts.csv`) and explicit open rows; the status vocabulary
distinguishes rejected (candidate with witness), no candidate (search path formed no candidate) and open.

Usage:
    python numerics/exercises/c2_correspondence.py [--workers=N] [--quick] [--nodes=1.2,1.6] [--out=DIR] [--mixed-iter=120]
"""
from __future__ import annotations

import sys
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal
from pathlib import Path

import numpy as np
from scipy import optimize

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import payoffs_closed_form  # noqa: E402
from numerics.certificates import certify, lo, hi, endpoint_str as es  # noqa: E402
from numerics.continuations import (INFO_FEEDBACK_STATE, NA, _norm_dec, continuation_from_schedule, deduplicate,  # noqa: E402
                                    parameter_set_id)
from numerics.deviations import dU  # noqa: E402
from numerics.error_budget import BUDGET_COLUMNS, error_budget, na_budget_row  # noqa: E402
from numerics.exercises.common import node_margins  # noqa: E402
from numerics.information import OrderProfile, make_schedule  # noqa: E402
from numerics.io import MANIFEST_DIR, ROOT, write_csv, write_manifest  # noqa: E402
from numerics.mixed_search import ATTEMPT_COLUMNS as MIXED_ATTEMPT_COLUMNS, attempt_row, mixed_search_node  # noqa: E402
from numerics.params import (BENCHMARK, BENCHMARK_STRENGTHS, CERTIFICATE_BRACKETS, CONTROLS, CORRESPONDENCE_MESH,  # noqa: E402
                             CORRESPONDENCE_OFFSETS, decimal_range)
from numerics.search import (Candidate, Psi, asymmetric_candidate, asymmetric_roots, full_order_candidate,  # noqa: E402
                             pooling_candidate, pure_fixed_points, derivative_cover)
from numerics.status_rules import (ANALYTICAL, COMPUTER_ASSISTED, NO_CANDIDATE, NUMERICAL_DIAGNOSTIC, OPEN, REJECTED,  # noqa: E402
                                   classify_tangency, pooling_existence_label)
from numerics.thresholds import compute_thresholds  # noqa: E402
from numerics.validation import validate  # noqa: E402

PRIM = BENCHMARK
LEGACY_COLUMNS = ["r", "branch", "q_H", "q_L", "v", "e_H", "e_L", "E", "O_H", "R_T", "tau", "x_star", "pooling_exists",
                  "pooling_unique_bound", "full_unique_bound", "existence_status", "uniqueness_status", "accepted",
                  "multiplicity_found", "epsilon_P", "epsilon_e", "epsilon_q", "tail_bound", "unresolved_reason"]
IDENTITY_COLUMNS = ["candidate_id", "continuation_id", "parameter_set_id", "search_path", "duplicate_of", "n_distinct_accepted",
                    "result_status"]
COLUMNS = LEGACY_COLUMNS + IDENTITY_COLUMNS + BUDGET_COLUMNS
MIXED_COLUMNS = ["r", "branch", "state", "support_index", "q", "weight", "U(q)", "support_gap", "off_support_gain_bound", "accepted", "status",
                 "init_id", "mesh_spacing", "iterations", "stop_reason", "final_gap", "gap_to_best_tested", "simplex_residual",
                 "residual_monotone", "quadrature_error", "search_domain", "outcome"]
PURE_INITS = [(u, v) for u in (0.2, 0.6, 0.95) for v in (0.2, 0.6, 0.95)]
TANGENCY_SUBMESH = 41
MIXED_MESHES = (0.05, 0.025)
RUN_ID = "c2"

OUTPUT_NAMES = {"correspondence": "correspondence.csv", "attempts": "correspondence_attempts.csv", "mixed": "mixed_supports.csv",
                "mixed_attempts": "mixed_search_attempts.csv", "thresholds": "thresholds.csv", "certificates": "certificates.csv"}


def canonical_r(s: str) -> str:
    """Canonical exact decimal label of a strength node (no `1.6` / `1.60` duplicates)."""
    return _norm_dec(s)


def strength_grid() -> list[str]:
    start, stop, step = CORRESPONDENCE_MESH
    pts = {canonical_r(x) for x in decimal_range(start, stop, step)}
    pts |= {canonical_r(x) for x in BENCHMARK_STRENGTHS.values()}
    pts |= {canonical_r(r) for r, _, _ in CERTIFICATE_BRACKETS}
    for row in compute_thresholds(PRIM):
        if row["boundary"] in ("pooling_unique_sufficient", "pooling_existence", "full_orders_unique_sufficient", "high_cost_ceiling"):
            val = Decimal(repr(float(row["value"])))
            pts.add(canonical_r(str(val)))
            for off in CORRESPONDENCE_OFFSETS:
                pts.add(canonical_r(str(val - Decimal(off))))
                pts.add(canonical_r(str(val + Decimal(off))))
    return sorted(pts, key=Decimal)


def pure_label(u: float, v: float) -> str:
    """Data label for a pure fixed point found by the best-response search (a label, not a selection)."""
    if abs(u - 1.0) < 1e-6:
        return "asymmetric"
    if abs(u - v) < 1e-6:
        return "symmetric_interior"
    return "pure"


def _status_word(existence: str) -> str:
    for w in (COMPUTER_ASSISTED, NUMERICAL_DIAGNOSTIC, NO_CANDIDATE, ANALYTICAL, REJECTED, OPEN):
        if existence.startswith(w):
            return w
    return existence


def _row(rs: str, branch: str, cand: Candidate, val, mg, existence: str, uniqueness: str, *, seq: int, search_path: str,
         reason: str = "", analytical_cover: bool = False) -> dict:
    """Legacy row plus continuation identity and the error budget. The budget can turn an accepted candidate into a rejection."""
    o = val.outcome
    eb = error_budget(val, cand.sched, CONTROLS, analytical_cover=analytical_cover)
    accepted = bool(val.accepted) and eb.within_targets
    if val.accepted and not eb.within_targets:
        existence = REJECTED
        reason = "error budget: " + "; ".join(eb.breaches)
    ps_id = parameter_set_id(PRIM, rs, PRIM.p, "binary", "0")
    cont = continuation_from_schedule(cand.sched, val, candidate_id=f"{RUN_ID}:r={rs}:{branch}#{seq}", parameter_set=ps_id,
                                      information=INFO_FEEDBACK_STATE, controls=CONTROLS, branch=branch, result_status=_status_word(existence),
                                      existence_scope="this node only; found by the declared search" if accepted else "none",
                                      uniqueness_scope=uniqueness,
                                      search_coverage_scope="pooling, full orders, asymmetric roots and tangencies, pure fixed points, mixed supports (C.2)",
                                      run_id=RUN_ID, unresolved_reason=reason if existence.startswith(OPEN) else "")
    row = {"r": rs, "branch": branch, "q_H": cand.profile.q_H[0] if cand.profile.is_pure else "mixed",
           "q_L": cand.profile.q_L[0] if cand.profile.is_pure else "mixed", "v": -cand.profile.q_L[0],
           "e_H": o.e_H, "e_L": o.e_L, "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "tau": o.tau, "x_star": o.x_star,
           "pooling_exists": mg.pooling_exists, "pooling_unique_bound": mg.pooling_unique_bound,
           "full_unique_bound": mg.full_unique_bound, "existence_status": existence, "uniqueness_status": uniqueness,
           "accepted": accepted, "multiplicity_found": False, "epsilon_P": val.epsilon_P, "epsilon_e": val.epsilon_e,
           "epsilon_q": max(val.epsilon_q, val.epsilon_q_refined), "tail_bound": val.tail_bound,
           "unresolved_reason": reason if reason else ("" if accepted else "; ".join(val.breaches)),
           "candidate_id": cont.candidate_id, "continuation_id": cont.continuation_id, "parameter_set_id": ps_id,
           "search_path": search_path, "duplicate_of": "", "n_distinct_accepted": 0, "result_status": _status_word(existence)}
    row.update(eb.row())
    row["_cont"] = cont
    return row


def _open_row(rs: str, branch: str, mg, reason: str, tau: float, search_path: str) -> dict:
    row = {"r": rs, "branch": branch, "q_H": NA, "q_L": NA, "v": NA, "e_H": NA, "e_L": NA, "E": NA, "O_H": NA, "R_T": NA, "tau": tau,
           "x_star": NA, "pooling_exists": mg.pooling_exists, "pooling_unique_bound": mg.pooling_unique_bound,
           "full_unique_bound": mg.full_unique_bound, "existence_status": OPEN, "uniqueness_status": "not established", "accepted": False,
           "multiplicity_found": False, "epsilon_P": NA, "epsilon_e": NA, "epsilon_q": NA, "tail_bound": NA, "unresolved_reason": reason,
           "candidate_id": NA, "continuation_id": NA, "parameter_set_id": parameter_set_id(PRIM, rs, PRIM.p, "binary", "0"),
           "search_path": search_path, "duplicate_of": "", "n_distinct_accepted": 0, "result_status": OPEN}
    row.update(na_budget_row())
    row["_cont"] = None
    return row


def _in_bracket(v: float, br: tuple[str, str] | None) -> bool:
    return br is not None and float(br[0]) <= v <= float(br[1])


def _tangency_refine(pay, v0: float, mesh: float = 0.01, v_lo: float = 0.005, v_hi: float = 0.9999) -> dict:
    """Sub-mesh the bracket around a |Psi| minimum: bracketed roots if Psi changes sign there, else the refined minimum."""
    a, b_ = max(v_lo, v0 - mesh), min(v_hi, v0 + mesh)
    vs = np.linspace(a, b_, TANGENCY_SUBMESH)
    psi = np.array([Psi(PRIM, pay, v) for v in vs])
    roots = []
    for i in range(len(vs) - 1):
        if psi[i] == 0.0:
            roots.append(float(vs[i]))
        elif psi[i] * psi[i + 1] < 0:
            roots.append(float(optimize.brentq(lambda v: Psi(PRIM, pay, v), vs[i], vs[i + 1], xtol=1e-13, rtol=1e-13)))
    i = int(np.abs(psi).argmin())
    res = optimize.minimize_scalar(lambda v: abs(Psi(PRIM, pay, v)), bounds=(vs[max(i - 1, 0)], vs[min(i + 1, len(vs) - 1)]),
                                   method="bounded", options={"xatol": 1e-10})
    v_min, f_min = (float(res.x), float(res.fun)) if res.fun <= abs(psi[i]) else (float(vs[i]), float(abs(psi[i])))
    return {"roots": roots, "v_min": v_min, "resid": f_min, "bracket": (a, b_)}


def solve_node(rs: str, certified: dict[str, tuple[str, str]], do_pure: bool = True, do_mixed: bool = True,
               tie_at_ceiling: bool = False, mixed_iter: int = 120) -> tuple[list[dict], list[dict], list[dict], dict]:
    """Solve one strength node. Returns (attempt rows incl. duplicates, mixed support rows, mixed attempt rows, diagnostics).

    Every attempt row has `duplicate_of` set when its continuation identity coincides with an earlier row at the node;
    `n_distinct_accepted` and `multiplicity_found` are computed from distinct accepted continuations.
    """
    rs = canonical_r(rs)
    r = float(rs)
    pay = payoffs_closed_form(PRIM, r)
    mg = node_margins(PRIM, pay)
    rows: list[dict] = []
    mixed_rows: list[dict] = []
    mixed_attempts: list[dict] = []
    diag: dict = {"r": rs}
    seq = 0
    br = certified.get(rs)

    def nxt() -> int:
        nonlocal seq
        seq += 1
        return seq

    # pooling ------------------------------------------------------------------
    cand = pooling_candidate(PRIM, pay)
    val = validate(cand.sched, CONTROLS)
    ex, note = pooling_existence_label(mg.pooling_exists, mg.in_domain, val.accepted)
    un = "analytical (Delta_T < k)" if mg.in_domain and mg.pooling_unique_bound > 0 else "not established"
    rows.append(_row(rs, "pooling", cand, val, mg, ex, un, seq=nxt(), search_path="pooling: declared profile (0,0)",
                     reason=note if ex.startswith(OPEN) else "", analytical_cover=ex.startswith(ANALYTICAL)))
    diag["pooling_note"] = note

    # full orders ---------------------------------------------------------------
    cand = full_order_candidate(PRIM, pay)
    if tie_at_ceiling:
        sched_tie = make_schedule(PRIM, pay, OrderProfile.pure(1.0, -1.0), tie_at_ceiling=True)
        cand = Candidate("full_orders", sched_tie.profile, sched_tie, cand.diagnostics)
    val = validate(cand.sched, CONTROLS)
    cover = derivative_cover(cand.sched, "H", CONTROLS.certificate_derivative_intervals) if val.accepted else {}
    if val.accepted:
        if mg.low_cost_floor > 0 and mg.full_unique_bound > 0:
            ex = "analytical (uniform derivative bound)"
        elif mg.low_cost_floor > 0 and cand.diagnostics["J_margin"] > 0:
            ex = "analytical (candidate J test, OA.22)"
        else:
            ex = NUMERICAL_DIAGNOSTIC
    else:
        ex = REJECTED
    un = "analytical ((1-1/b) rho m Delta_T > k)" if mg.low_cost_floor > 0 and mg.full_unique_bound > 0 else "not established"
    rows.append(_row(rs, "full_orders", cand, val, mg, ex + (" (tau = M treated symbolically; tie rule admits the upper plateau)" if tie_at_ceiling else ""),
                     un, seq=nxt(), search_path="full_orders: declared profile (1,-1)", analytical_cover=ex.startswith(ANALYTICAL)))
    diag["full_J"] = cand.diagnostics
    diag["full_cover"] = cover

    # asymmetric (1, -v): sign-change roots, certified bracket, tangency sub-mesh ------------------
    extra = [tuple(float(x) for x in br)] if br else None
    ar = asymmetric_roots(PRIM, pay, extra_brackets=extra, v_hi=0.9999)
    diag["asym_roots"] = ar["roots"]
    diag["asym_tangencies"] = ar["tangencies"]
    root_paths = [(v, "asymmetric: Psi sign change on mesh 0.01, Brent" + (" (certified bracket)" if _in_bracket(v, br) else "")) for v in ar["roots"]]
    tangency_records = []
    for v0, resid0 in ar["tangencies"]:
        tr = _tangency_refine(pay, v0)
        for v in tr["roots"]:
            root_paths.append((v, f"asymmetric: Psi sign change on the {TANGENCY_SUBMESH}-point sub-mesh of the tangency bracket [{tr['bracket'][0]:.4g},{tr['bracket'][1]:.4g}], Brent"))
        if not tr["roots"]:
            tangency_records.append((tr["v_min"], tr["resid"], tr["bracket"]))
    for v, path in root_paths:
        cand = asymmetric_candidate(PRIM, pay, v)
        val = validate(cand.sched, CONTROLS)
        if abs(cand.diagnostics["Psi"]) > 1e-6:
            # sign change across a discontinuity of Psi (threshold reaches the plateau boundary): no root, no candidate formed
            rows.append(_row(rs, "asymmetric_discontinuity", cand, val, mg, NO_CANDIDATE, "not established", seq=nxt(), search_path=path,
                             reason=f"Psi sign change without root: |Psi|={abs(cand.diagnostics['Psi']):.3e} at the tau = M_v boundary; no candidate formed"))
            continue
        ex = COMPUTER_ASSISTED if (val.accepted and _in_bracket(v, br)) else (NUMERICAL_DIAGNOSTIC if val.accepted else REJECTED)
        rows.append(_row(rs, "asymmetric", cand, val, mg, ex, "not established", seq=nxt(), search_path=path))
    for v, resid, (a_, b_) in tangency_records:
        cand = asymmetric_candidate(PRIM, pay, v)
        val = validate(cand.sched, CONTROLS)
        path = f"asymmetric: |Psi| minimisation on [{a_:.4g},{b_:.4g}] without sign change ({TANGENCY_SUBMESH}-point sub-mesh)"
        if val.accepted:
            rows.append(_row(rs, "asymmetric", cand, val, mg, NUMERICAL_DIAGNOSTIC, "not established", seq=nxt(), search_path=path,
                             reason=f"root located by |Psi| minimization ({resid:.3e}) rather than a sign change"))
            continue
        verdict = classify_tangency(resid, dU(cand.sched, "L", v))
        rows.append(_row(rs, "asymmetric_tangency", cand, val, mg, verdict.status, "not established", seq=nxt(), search_path=path,
                         reason=verdict.reason))

    # other pure profiles (u, -v) ------------------------------------------------
    if do_pure:
        fp = pure_fixed_points(PRIM, pay, inits=PURE_INITS, max_iter=40)
        diag["pure_unconverged"] = len(fp["unconverged"])
        for u, v, init in fp["fixed_points"]:
            sched = make_schedule(PRIM, pay, OrderProfile.pure(u, -v))
            cand = Candidate("pure", sched.profile, sched, {"init": init})
            val = validate(cand.sched, CONTROLS)
            rows.append(_row(rs, pure_label(u, v), cand, val, mg, NUMERICAL_DIAGNOSTIC if val.accepted else REJECTED, "not established",
                             seq=nxt(), search_path=f"pure: damped best-response fixed point from init (u,v)=({init[0]},{init[1]})"))
        if fp["unconverged"]:
            inits = "; ".join(f"({u0},{v0})->({u:.4g},{v:.4g})" for u0, v0, u, v in fp["unconverged"])
            rows.append(_open_row(rs, "pure_search", mg, f"{len(fp['unconverged'])} of {len(PURE_INITS)} best-response iterations did not converge "
                                  f"(40 iterations, damping 0.5, tol 1e-7): {inits}", pay.tau(PRIM.fc_H),
                                  "pure: damped best-response fixed points from the 9 declared initialisations"))

    # finite-support mixed search: documented starts, budget, support system, attempt ledger --------------
    if do_mixed:
        attempts = mixed_search_node(PRIM, pay, CONTROLS, rs, meshes=MIXED_MESHES, max_iter=mixed_iter)
        unresolved = []
        for at in attempts:
            path = f"mixed: mesh {at.mesh}, start {at.start_id}"
            val_text, acc, qerr, status = "", False, NA, f"{at.outcome} ({at.stop_reason}; support solve {at.support_solve})"
            gaps = list(at.gap_to_best_tested)
            if at.outcome == "converged-candidate":
                val = validate(at.sched, CONTROLS)
                cand = Candidate("mixed", at.profile, at.sched, {})
                rw = _row(rs, "mixed", cand, val, mg, NUMERICAL_DIAGNOSTIC if val.accepted else REJECTED, "not established", seq=nxt(), search_path=path)
                rows.append(rw)
                acc, qerr = rw["accepted"], rw["quadrature_error"]
                sc = val.scans.get("H_refined", val.scans["H"])
                best = max(x[1] for x in sc["rows"])
                gaps = [best - p for p in at.support_payoffs]
                val_text = "accepted" if acc else "rejected: " + rw["unresolved_reason"]
            elif at.outcome == "converged-pure":
                u, v = at.support_q[0], at.v
                sched = make_schedule(PRIM, pay, OrderProfile.pure(u, -v))
                val = validate(sched, CONTROLS)
                cand = Candidate("pure", sched.profile, sched, {})
                label = "pooling" if (abs(u) < 1e-6 and abs(v) < 1e-6) else ("full_orders" if (abs(u - 1) < 1e-6 and abs(v - 1) < 1e-6) else pure_label(u, v))
                rw = _row(rs, label, cand, val, mg, NUMERICAL_DIAGNOSTIC if val.accepted else REJECTED, "not established", seq=nxt(), search_path=path)
                rows.append(rw)
                acc, qerr = rw["accepted"], rw["quadrature_error"]
                val_text = ("accepted" if acc else "rejected: " + rw["unresolved_reason"]) + f"; pure profile ({u:.6g},{-v:.6g})"
            else:
                unresolved.append(at)
                val_text = "not validated (unresolved attempt)"
            mixed_attempts.append(attempt_row(at, val_text))
            common = {"init_id": at.start_id, "mesh_spacing": at.mesh, "iterations": at.iterations, "stop_reason": at.stop_reason,
                      "final_gap": at.final_gap, "simplex_residual": at.simplex_residual, "residual_monotone": at.residual_monotone,
                      "quadrature_error": qerr, "search_domain": at.domain, "outcome": at.outcome}
            for j, (q, w, pq, g) in enumerate(zip(at.support_q, at.support_w, at.support_payoffs, gaps)):
                mixed_rows.append({"r": rs, "branch": f"mixed_mesh_{at.mesh}", "state": "H", "support_index": j, "q": q, "weight": w, "U(q)": pq,
                                   "support_gap": max(at.support_payoffs) - min(at.support_payoffs), "off_support_gain_bound": max(gaps),
                                   "gap_to_best_tested": g, "accepted": acc, "status": status, **common})
            mixed_rows.append({"r": rs, "branch": f"mixed_mesh_{at.mesh}", "state": "L", "support_index": 0, "q": -at.v, "weight": 1.0, "U(q)": NA,
                               "support_gap": 0.0, "off_support_gain_bound": NA, "gap_to_best_tested": at.final_v_residual, "accepted": acc,
                               "status": status, **common})
        if unresolved:
            detail = "; ".join(f"mesh {a.mesh} {a.start_id}: {a.witness}" for a in unresolved)
            rows.append(_open_row(rs, "mixed_search", mg, f"mixed search unresolved on {len(unresolved)} of {len(attempts)} attempts: {detail}",
                                  pay.tau(PRIM.fc_H), f"mixed: {len(attempts)} attempts ({len(MIXED_MESHES)} meshes x 3 starts), budget {mixed_iter} iterations each"))
        diag["mixed_outcomes"] = {a.start_id + f"@{a.mesh}": a.outcome for a in attempts}

    # deduplication by complete continuation identity (accepted and non-accepted separately) ---------------------
    _dedupe(rows)
    return rows, mixed_rows, mixed_attempts, diag


def _dedupe(rows: list[dict]) -> None:
    """Mark duplicates by continuation identity; count distinct accepted continuations; set multiplicity."""
    acc = [rw for rw in rows if rw["accepted"] is True and rw["_cont"] is not None]
    reps, absorbed = deduplicate([rw["_cont"] for rw in acc], CONTROLS)
    first = {}
    for cid, cands in absorbed.items():
        first[cands[0]] = cands[0]
        for extra in cands[1:]:
            first[extra] = cands[0]
    for rw in acc:
        dup = first.get(rw["_cont"].candidate_id, rw["_cont"].candidate_id)
        rw["duplicate_of"] = "" if dup == rw["_cont"].candidate_id else dup
    n_distinct = len(reps)
    rej = [rw for rw in rows if rw["accepted"] is not True and rw["_cont"] is not None]
    reps_r, absorbed_r = deduplicate([rw["_cont"] for rw in rej], CONTROLS)
    first_r = {}
    for cid, cands in absorbed_r.items():
        for extra in cands[1:]:
            first_r[extra] = cands[0]
    for rw in rej:
        # a rejected/no-candidate attempt that repeats an accepted or earlier non-accepted continuation is a duplicate attempt
        same_acc = next((a for a in acc if a["_cont"].continuation_id == rw["_cont"].continuation_id and a["branch"] == rw["branch"]), None)
        rw["duplicate_of"] = same_acc["candidate_id"] if same_acc else first_r.get(rw["_cont"].candidate_id, "")
    for rw in rows:
        rw["n_distinct_accepted"] = n_distinct
        rw["multiplicity_found"] = n_distinct >= 2
        rw.pop("_cont", None)


def _worker(args):
    return solve_node(*args)


def quick_grid(grid: list[str], certified: dict, rC: str) -> list[str]:
    keep = {canonical_r(x) for x in BENCHMARK_STRENGTHS.values()} | set(certified) | {"1.51", "1.8", "2.5", rC}
    return [g for g in grid if g in keep]


def run(workers: int | None = None, quick: bool = False, out: str | None = None, nodes: list[str] | None = None,
        mixed_iter: int = 120) -> bool:
    import os
    import shutil
    workers = workers or max(1, (os.cpu_count() or 8) - 2)
    out_dir = Path(out).resolve() if out else (ROOT / "numerics")
    out_dir.mkdir(parents=True, exist_ok=True)
    # manifest output keys stay repository-relative for the default location (verify.py rehashes them by key)
    paths = {k: (str(out_dir / v) if out else f"numerics/{v}") for k, v in OUTPUT_NAMES.items()}
    checks, notes = {}, []
    # --- thresholds -------------------------------------------------------------------
    th = compute_thresholds(PRIM)
    write_csv(paths["thresholds"], ["boundary", "value", "lower", "upper", "defining_residual", "in_support_domain",
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
    write_csv(paths["certificates"], ["r", "v_lower", "v_upper", "Psi_left_lower", "Psi_left_upper", "Psi_right_lower",
                                      "Psi_right_upper", "Gamma_H_lower", "L_U_upper", "mesh_intervals", "interval_digits",
                                      "E_lower", "E_upper", "pooling_margin_lower", "threshold_margin_lower", "accepted"], cert_rows)
    ordered = all(float(a["E_upper"]) < float(b["E_lower"]) for a, b in zip(cert_rows[:-1], cert_rows[1:]) if a["accepted"] and b["accepted"])
    checks["certified_entry_intervals_strictly_ordered"] = {"pass": ordered}

    # --- correspondence -----------------------------------------------------------------
    certified = {canonical_r(r): (vl, vr) for r, vl, vr in CERTIFICATE_BRACKETS}
    grid = strength_grid()
    rC = canonical_r(str(Decimal(repr(float(next(row["value"] for row in th if row["boundary"] == "high_cost_ceiling"))))))
    if nodes:
        grid = sorted({canonical_r(n) for n in nodes}, key=Decimal)
    elif quick:
        grid = quick_grid(grid, certified, rC)
    assert len(grid) == len({Decimal(g) for g in grid}), "strength grid has Decimal duplicates"
    tasks = [(rs, certified, True, True, rs == rC, mixed_iter) for rs in grid]
    rows, mixed_rows, mixed_attempts, diags = [], [], [], []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for rws, mrows, matt, dg in ex.map(_worker, tasks, chunksize=1):
            rows += rws
            mixed_rows += mrows
            mixed_attempts += matt
            diags.append(dg)
    # --- refinement where accepted branch sets change between adjacent grid nodes -------------
    def accepted_set(rs: str) -> frozenset:
        return frozenset(row["branch"] for row in rows if row["r"] == rs and row["accepted"] is True)
    refine_pairs = []
    for a, b_ in zip(grid[:-1], grid[1:]):
        if accepted_set(a) != accepted_set(b_) and Decimal(b_) - Decimal(a) > Decimal("0.001"):
            refine_pairs.append((a, b_))
    refine_nodes = set()
    for a, b_ in refine_pairs:
        x = Decimal(a) + Decimal("0.001")
        while x < Decimal(b_):
            refine_nodes.add(canonical_r(str(x)))
            x += Decimal("0.001")
    refine_nodes -= set(grid)
    refine_nodes = sorted(refine_nodes, key=Decimal)
    if refine_nodes and not quick and not nodes:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for rws, mrows, matt, dg in ex.map(_worker, [(rs, certified, True, True, False, mixed_iter) for rs in refine_nodes], chunksize=1):
                rows += rws
                mixed_rows += mrows
                mixed_attempts += matt
                diags.append(dg)
    rows.sort(key=lambda row: (Decimal(row["r"]), row["branch"], row["candidate_id"]))
    mixed_rows.sort(key=lambda row: (Decimal(row["r"]), row["branch"], row["init_id"], row["state"], row["support_index"]))
    mixed_attempts.sort(key=lambda row: (Decimal(row["r"]), row["mesh"], row["start_id"]))
    distinct = [row for row in rows if not row["duplicate_of"]]
    write_csv(paths["attempts"], COLUMNS, rows)
    write_csv(paths["correspondence"], COLUMNS, distinct)
    write_csv(paths["mixed"], MIXED_COLUMNS, mixed_rows)
    write_csv(paths["mixed_attempts"], MIXED_ATTEMPT_COLUMNS, mixed_attempts)

    # --- summary checks -----------------------------------------------------------------------
    all_nodes = sorted({row["r"] for row in distinct}, key=Decimal)
    n_open = sum(1 for row in distinct if row["existence_status"].startswith(OPEN))
    n_multi = len({row["r"] for row in distinct if row["multiplicity_found"] is True})
    budget_fail = [row for row in rows if row["error_budget_breaches"] not in ("", NA)]
    checks["correspondence"] = {
        "nodes": len(all_nodes), "grid_nodes": len(grid), "refined_nodes": len(refine_nodes), "refinement_pairs": refine_pairs,
        "refinement_rule": "adjacent grid nodes whose accepted branch sets differ are refined to spacing 0.001",
        "node_keys_canonical": len(all_nodes) == len({Decimal(x) for x in all_nodes}),
        "attempt_rows": len(rows), "distinct_rows": len(distinct), "duplicate_attempts": len(rows) - len(distinct),
        "open_rows": n_open, "open_rows_by_branch": {b: sum(1 for row in distinct if row["branch"] == b and row["existence_status"].startswith(OPEN))
                                                    for b in sorted({row["branch"] for row in distinct})},
        "no_candidate_rows": sum(1 for row in distinct if row["existence_status"].startswith(NO_CANDIDATE)),
        "rejected_rows": sum(1 for row in distinct if row["existence_status"].startswith(REJECTED)),
        "nodes_with_multiplicity": n_multi,
        "asymmetric_accepted_nodes": sorted({row["r"] for row in distinct if row["branch"] == "asymmetric" and row["accepted"] is True}, key=Decimal),
        "accepted_branch_labels": sorted({row["branch"] for row in distinct if row["accepted"] is True}),
        "error_budget_breached_rows": len(budget_fail),
        "mixed_attempt_outcomes": {k: sum(1 for a in mixed_attempts if a["outcome"] == k) for k in ("converged-candidate", "converged-pure", "unresolved")},
        "mixed_nodes_unresolved": sorted({a["r"] for a in mixed_attempts if a["outcome"] == "unresolved"}, key=Decimal),
        "mixed_candidates_accepted": sum(1 for row in distinct if row["branch"] == "mixed" and row["accepted"] is True),
    }
    checks["error_budget"] = {"pass": all(row["error_budget_breaches"] in ("", NA) for row in rows if row["accepted"] is True),
                              "rule": "quadrature |GL48-GL24| <= 1e-11 on the declared scan; refined |GL64-GL32| <= 1e-12 on 800 intervals; "
                                      "tail truncation bound <= 1e-11; a breached target rejects the row (never loosened)",
                              "breached_candidates": [row["candidate_id"] for row in budget_fail]}
    for rs, want in (("1.2", "pooling"), ("3", "full_orders"), ("3.6", "full_orders")):
        if canonical_r(rs) in grid:
            acc = accepted_set(canonical_r(rs))
            checks[f"declared_node_{rs}"] = {"accepted_branches": sorted(acc), "pass": want in acc}
    for r_s, vl, vr in CERTIFICATE_BRACKETS:
        rc = canonical_r(r_s)
        if rc in grid:
            hits = [row for row in distinct if row["r"] == rc and row["branch"] == "asymmetric" and row["accepted"] is True
                    and float(vl) <= float(row["v"]) <= float(vr)]
            checks[f"certified_node_root_in_bracket_{r_s}"] = {"pass": len(hits) == 1 and hits[0]["existence_status"] == COMPUTER_ASSISTED,
                                                               "v": [row["v"] for row in hits], "status": [row["existence_status"] for row in hits]}
    if rC in grid:
        accs = accepted_set(rC)
        checks["r_C_node_tie_rule"] = {"accepted_branches": sorted(accs), "pass": "full_orders" in accs,
                                       "E_full_orders": [row["E"] for row in distinct if row["r"] == rC and row["branch"] == "full_orders"]}
    passed = all(c.get("pass", c.get("accepted", True)) for c in checks.values())
    notes.append("Node keys are canonical exact decimals (Decimal.normalize); the certificate label 1.60 and the mesh node 1.6 are one node.")
    notes.append("Candidates are deduplicated by complete continuation identity (orders, pricing family, price atoms, preparation rule); "
                 "raw attempts, including duplicates, are in correspondence_attempts.csv; multiplicity_found counts distinct accepted continuations.")
    notes.append("Refinement rule for the quadrature targets: the x10 tightening is implemented by raising the Gauss-Legendre order 48 -> 64 "
                 "and the order intervals 400 -> 800; the refined error estimate is compared with target/10 on every row.")
    notes.append("No retries beyond the documented starts: 9 pure initialisations (40 damped iterations each) and 3 mixed starts per mesh "
                 f"({mixed_iter} replicator iterations each, then the support indifference/simplex solve). Unconverged starts produce open rows.")
    notes.append("Tangency rule: a local |Psi| minimum without sign change on the 41-point sub-mesh is open when within the numerical resolution "
                 "(10 x quadrature error + tail bound, floor 1e-8) and 'no candidate' otherwise; the same rule is proposed for C.6.")
    notes.append("Mixed-search outcomes are search records only; they never assert that mixed equilibria do not exist.")
    exercise = "c2_correspondence" if out is None else "c2_correspondence_quick"
    man_path = write_manifest(exercise, {"benchmark": PRIM.__dict__, "mesh": CORRESPONDENCE_MESH, "offsets": CORRESPONDENCE_OFFSETS,
                                         "certificate_brackets": CERTIFICATE_BRACKETS, "grid_size": len(grid), "quick": quick, "nodes": nodes,
                                         "mixed_iterations": mixed_iter, "mixed_meshes": MIXED_MESHES, "pure_inits": PURE_INITS},
                              "Exact boundaries from Proposition 3 with residual checks; interval certificates per Appendix B (mpmath iv, "
                              "exact antiderivatives, uniform high-type cover over the root bracket, mesh 200 and 400); at each strength node "
                              "pooling, full-order, asymmetric (1,-v) roots by sign-change bracketing plus |Psi| minimisation with a 41-point "
                              "sub-mesh of each tangency bracket, pure (u,-v) best-response fixed points from 9 initialisations, and "
                              "finite-support mixed search (3 documented starts per mesh, meshes 0.05 and 0.025, replicator budget then the "
                              "support indifference/simplex system); every candidate validated independently with a per-row error budget; "
                              "deduplication by continuation identity; refinement to 0.001 where accepted branch sets change.",
                              CONTROLS.as_dict(), list(paths.values()), checks, passed, notes)
    if out is not None:
        shutil.move(str(man_path), str(out_dir / "c2_correspondence.json"))
    print("C.2 passed" if passed else "C.2 FAILED", checks["correspondence"])
    return passed


if __name__ == "__main__":
    w = next((int(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--workers=")), None)
    out = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
    nodes = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--nodes=")), None)
    mi = next((int(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--mixed-iter=")), 120)
    sys.exit(0 if run(workers=w, quick="--quick" in sys.argv, out=out, nodes=nodes, mixed_iter=mi) else 1)
