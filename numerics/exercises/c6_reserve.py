"""C.6: reserve comparisons and the exploratory seller continuation sweep."""
from __future__ import annotations

import sys
import json
import os
from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor, as_completed
from decimal import Decimal
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import (payoffs_class_closed_form, payoffs_class_formula_OA52, payoffs_class_integrated,  # noqa: E402
                              payoffs_closed_form, payoffs_integrated)
from numerics.continuations import (INFO_FEEDBACK_CLASS, INFO_FEEDBACK_STATE, NA, SCHEMA_COLUMNS, ContinuationOutcome,  # noqa: E402
                                    continuation_from_schedule, continuation_row, deduplicate, parameter_set_id)
from numerics.information import OrderProfile, entry_at_posterior, make_schedule  # noqa: E402
from numerics.error_budget import BUDGET_COLUMNS, error_budget
from numerics.io import ROOT, _json_default, write_csv, write_manifest  # noqa: E402
from numerics.noise import posterior_bounds  # noqa: E402
from numerics.params import BENCHMARK, BENCHMARK_EXTRA, BENCHMARK_STRENGTHS, CONTROLS, decimal_range  # noqa: E402
from numerics.search import (Candidate, asymmetric_candidate, asymmetric_roots, full_order_candidate, mixed_support_search,  # noqa: E402
                             pooling_candidate, pure_fixed_points)
from numerics.reserve_events import EventNode, classify_node, event_grid, outcome_measures  # noqa: E402
from numerics.validation import validate  # noqa: E402

PRIM = BENCHMARK
EPS_V = float(BENCHMARK_EXTRA["value_band_halfwidth"])
TOL = CONTROLS.independent_formula_acceptance
STRENGTHS = {k: v for k, v in BENCHMARK_STRENGTHS.items() if k != "r_collapse"}
DECLARED = {"binary": ["0.5", BENCHMARK_EXTRA["binary_alternative_reserve"]],
            "uniform_classes": ["0.5", BENCHMARK_EXTRA["atomless_alternative_reserve"]]}
LEGACY_COLS = ["value_law", "r", "p", "branch", "q_H", "q_L", "E", "O_H", "R_T", "no_entry_price_mass", "posterior_in_no_entry_pool",
               "epsilon_P", "epsilon_e", "epsilon_q", "status", "accepted", "unresolved_reason"]
# legacy columns first (unchanged names), then the complete continuation schema (spec 16.1); p_exact carries the
# exact declaration or event tag when p is irrational, and the node classification columns record how each
# inequality was decided (strict sign at 50 digits, declared equality event, or unresolved).
CONT_COLS = LEGACY_COLS + ["p_exact", "regime", "band_status", "low_cost_floor_relation", "ceiling_relation", "duplicate_of", "identity_note"] + \
    [c for c in SCHEMA_COLUMNS + BUDGET_COLUMNS if c not in LEGACY_COLS]
RANGE_COLS = ["value_law", "r", "p", "accepted_continuations_found", "E_min_found", "E_max_found", "R_T_min_found", "R_T_max_found",
              "search_unresolved", "global_envelope_certified", "p_exact", "event_id", "candidates_evaluated", "candidates_accepted_raw",
              "candidates_rejected", "candidates_unresolved", "duplicates_merged", "search_outcome"]


def payoffs(law: str, r: float, p: float):
    if law == "binary":
        pay = payoffs_closed_form(PRIM, r, p)
        pay_i, _ = payoffs_integrated(PRIM, r, p)
        err = max(abs(getattr(pay, a) - getattr(pay_i, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L"))
    else:
        pay = payoffs_class_closed_form(PRIM, r, p, EPS_V)
        pay_i, _ = payoffs_class_integrated(PRIM, r, p, EPS_V, epsabs=1e-12, epsrel=1e-12)
        err = max(abs(getattr(pay, a) - getattr(pay_i, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L"))
        if p < PRIM.fell - EPS_V and PRIM.fell + EPS_V < r < PRIM.fh - EPS_V:
            pay_f = payoffs_class_formula_OA52(PRIM, r, p, EPS_V)
            err = max(err, max(abs(getattr(pay, a) - getattr(pay_f, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L")))
    return pay, err


def analytic_bounds(pay) -> dict:
    """Strict bounds with the actual entry floor e(m) = H_C(B(m)) and the class payoff spread."""
    m, M = posterior_bounds(PRIM.fb)
    e_m = float(entry_at_posterior(PRIM, pay, np.array([m]))[0])
    e0 = float(entry_at_posterior(PRIM, pay, np.array([0.5]))[0])
    return {"low_cost_floor_margin": pay.B(m) - PRIM.fc_L, "e_m": e_m, "e0": e0,
            "no_trade_unique_margin": PRIM.fk - pay.Delta_T,
            "pooling_exists_margin": PRIM.fk - e0 * pay.Delta_T / 2,
            "full_unique_margin": (1 - 1 / PRIM.fb) * e_m * m * pay.Delta_T - PRIM.fk if e_m > 0 else float("-inf")}


def _row(node: EventNode, branch: str, cand, val, existence: str, reason: str = "", *, cls: dict, seq: int, run_id: str,
         uniqueness: str = "not established", coverage: str = "") -> dict:
    """Legacy row plus the complete continuation record (candidate identity separate from economic identity)."""
    law, rs, ps = node.law, node.r, legacy_p(node)
    budget = error_budget(val, cand.sched, CONTROLS, analytical_cover=existence.startswith("analytical"))
    val.breaches.extend(b for b in budget.breaches if b not in val.breaches)
    if existence == "rejected" and reason and reason not in val.breaches:
        val.breaches.append(reason)
    o = val.outcome
    eps_V = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
    ps_id = parameter_set_id(PRIM, rs, node.p_exact, law, eps_V)
    info = INFO_FEEDBACK_CLASS if law == "uniform_classes" else INFO_FEEDBACK_STATE
    om = outcome_measures(PRIM, law, eps_V, float(rs), node.p_float, o.e_H, o.e_L)
    if om["S_identity_error"] > TOL or not om["bounds_ok"]:
        val.breaches.append(f"outcome identity: S error {om['S_identity_error']:.3e}, bounds_ok={om['bounds_ok']}")
    extra = ContinuationOutcome(o.e_H, o.e_L, o.E, om["A"], om["S"], om["C2"], om["O_H"], o.R_T, o.mean_price)
    unresolved = reason if (existence == "open") else ""
    status = existence if val.accepted else ("rejected" if not existence.startswith("open") else existence)
    cont = continuation_from_schedule(cand.sched, val, candidate_id=f"{run_id}:{law}:r={rs}:p={node.p_decimal[:20]}:{branch}#{seq}",
                                      parameter_set=ps_id, information=info, controls=CONTROLS, branch=branch, result_status=status,
                                      existence_scope=("this node only; found by the declared search" if val.accepted else "none (rejected)"),
                                      uniqueness_scope=uniqueness, search_coverage_scope=coverage or "pooling, full orders, asymmetric roots, pure fixed points, mixed supports (C.6)",
                                      run_id=run_id, event_id=node.event_id, event_relation=node.event_defining_relation,
                                      outcome_extra=extra, unresolved_reason=unresolved)
    row = {"value_law": law, "r": rs, "p": ps, "branch": branch,
           "q_H": cand.profile.q_H[0] if cand.profile.is_pure else "mixed", "q_L": cand.profile.q_L[0] if cand.profile.is_pure else "mixed",
           "E": o.E, "O_H": om["O_H"], "R_T": o.R_T, "no_entry_price_mass": val.no_entry_price_mass,
           "posterior_in_no_entry_pool": val.posterior_in_no_entry_pool if np.isfinite(val.posterior_in_no_entry_pool) else NA, "epsilon_P": val.epsilon_P, "epsilon_e": val.epsilon_e,
           "epsilon_q": max(val.epsilon_q, val.epsilon_q_refined), "status": status, "accepted": cont.accepted,
           "unresolved_reason": reason or ("" if val.accepted else "; ".join(val.breaches)),
           "p_exact": node.p_exact, "regime": cls["regime"], "band_status": cls["band_status"],
           "low_cost_floor_relation": cls["low_cost_floor_relation"], "ceiling_relation": cls["ceiling_relation"], "duplicate_of": "",
           "identity_note": ""}
    row.update({k_: v_ for k_, v_ in continuation_row(cont).items() if k_ not in row})
    if not cont.accepted:
        row["status"] = "open" if existence == "open" else "rejected"
        row["unresolved_reason"] = reason or cont.rejection_reason
    row.update(budget.row())
    row["_cont"] = cont
    row["_profile"] = cand.profile
    return row


def legacy_p(node: EventNode) -> str:
    """The legacy `p` column: the exact decimal when the declaration is one, else the 32-digit decimal of the event value."""
    try:
        Decimal(node.p_exact)
        return node.p_exact
    except Exception:
        return node.p_decimal


def node_from_args(args) -> EventNode:
    """Legacy (law, r, p) grid triples become plain grid nodes; EventNodes pass through."""
    if isinstance(args, EventNode):
        return args
    law, rs, ps = args
    from numerics.reserve_events import _dec30
    return EventNode(law, rs, ps, _dec30(ps), "grid", "declared reserve grid point (C.6)", True)


def snap_endpoint(q: float) -> float:
    """Propose an exact order boundary within solver tolerance, then revalidate its schedule."""
    endpoint = min((-1.0, 0.0, 1.0), key=lambda e: abs(q - e))
    return endpoint if abs(q - endpoint) <= 1e-7 else q


def finalize_node(result: tuple[list[dict], dict, dict]) -> tuple[list[dict], dict, dict]:
    """Separate rejected terminal profiles from unresolved searches, using recorded validation evidence."""
    original_rows, original_range, original_diag = result
    rows = [dict(row) for row in original_rows]
    rng, diag = dict(original_range), dict(original_diag)
    for row in rows:
        if row["accepted"] is not True and row["result_status"] == "rejected" and row["rejection_reason"]:
            row["status"] = "rejected"
    open_solver_attempts = int(rng["candidates_evaluated"]) - len(rows)
    rng["candidates_rejected"] = sum(row["accepted"] is not True and not row["status"].startswith("open") for row in rows)
    rng["candidates_unresolved"] = open_solver_attempts + sum(row["status"].startswith("open") for row in rows)
    diag["ledger"] = {**diag["ledger"], "rejected": rng["candidates_rejected"], "open": rng["candidates_unresolved"]}
    # The separate search_unresolved flag and its diagnostic reasons are preserved.
    return rows, rng, diag


def solve_reserve(args, run_id: str = "c6", refine_identity: bool = False) -> tuple[list[dict], dict, dict]:
    node = node_from_args(args)
    law, rs = node.law, node.r
    ps = legacy_p(node)
    r, p = float(rs), node.p_float
    eps_V = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
    pay, oracle_err = payoffs(law, r, p)
    if not np.isfinite(oracle_err) or oracle_err > TOL:
        raise ValueError(f"Payoff oracle failed at {node}: error={oracle_err}")
    ab = analytic_bounds(pay)
    cls = classify_node(PRIM, node, eps_V)
    # exact classification overrides the float sign where the two disagree (equality event or unresolved sign)
    floor_rel, ceil_rel = cls["low_cost_floor_relation"], cls["ceiling_relation"]
    tie_floor = node.tie_at_floor and node.applicable and floor_rel == "equality_event"
    tie_ceiling = node.tie_at_ceiling and node.applicable and ceil_rel == "equality_event"
    floor_ok = floor_rel in ("strict_positive", "equality_event")
    rows, diag = [], {"law": law, "r": rs, "p": ps, "p_exact": node.p_exact, "event_id": node.event_id, "payoff_oracle_error": oracle_err, **ab,
                      "regime": cls["regime"], "low_cost_floor_relation": floor_rel, "ceiling_relation": ceil_rel,
                      "full_unique_relation": cls["full_unique_relation"]}
    unresolved = False
    seq = 0
    open_attempts = 0
    m, M = posterior_bounds(PRIM.fb)
    e_M = float(entry_at_posterior(PRIM, pay, np.array([M]))[0])
    if tie_ceiling:
        e_M = 1.0
    degenerate = pay.Delta_T <= 0 or pay.g_H <= 0 or e_M <= 0
    if floor_rel == "unresolved" or ceil_rel == "unresolved":
        unresolved = True
        diag["classification_unresolved"] = f"floor={floor_rel}, ceiling={ceil_rel}"
    full_unique = cls["full_unique_relation"] == "strict_positive" and floor_ok
    # pooling / constant-price candidate (always analysed directly)
    cand = pooling_candidate(PRIM, pay)
    val = validate(cand.sched, CONTROLS, price_pools=True)
    ex = ("analytical (unique no trade: Delta_T < k)" if val.accepted and ab["no_trade_unique_margin"] > 0 else
          "analytical (pooling exists: e0 Delta_T/2 <= k)" if val.accepted and ab["pooling_exists_margin"] >= 0 else
          "numerical diagnostic" if val.accepted else "rejected")
    seq += 1
    rows.append(_row(node, "pooling", cand, val, ex, cls=cls, seq=seq, run_id=run_id,
                     uniqueness="unique (Delta_T < k)" if ab["no_trade_unique_margin"] > 0 else "not established"))
    if degenerate:
        diag["skipped_searches"] = ("all entry impossible (H_C(B_r(M)) = 0): constant-price candidate only" if e_M <= 0 else
                                    "degenerate payoff (Delta_T <= 0 or g_H <= 0): constant-price candidate only")
    elif ab["no_trade_unique_margin"] > 0:
        diag["skipped_searches"] = "Delta_T < k excludes every nonzero order against any candidate schedule"
    else:
        sched = make_schedule(PRIM, pay, OrderProfile.pure(1.0, -1.0), tie_at_ceiling=tie_ceiling, tie_at_floor=tie_floor)
        from numerics.search import J_test
        from numerics.deviations import dU
        cand = Candidate("full_orders", sched.profile, sched, J_test(sched))
        cand.diagnostics["dU_L_at_1"] = dU(sched, "L", 1.0).value
        cand.diagnostics["dU_H_at_1"] = dU(sched, "H", 1.0).value
        val = validate(cand.sched, CONTROLS, price_pools=True)
        if val.accepted:
            if full_unique:
                ex = "analytical (unique full orders: uniform derivative bound with entry floor)"
                if floor_rel == "equality_event":
                    ex = "analytical (unique full orders: uniform derivative bound with the floor at equality, e >= rho by the tie rule)"
            elif floor_ok and cand.diagnostics["J_margin"] > 0:
                ex = "analytical (candidate J test)"
            else:
                ex = "numerical diagnostic"
        else:
            ex = "rejected"
        seq += 1
        rows.append(_row(node, "full_orders", cand, val, ex, cls=cls, seq=seq, run_id=run_id,
                         uniqueness="unique within all continuations (uniform derivative bound)" if full_unique else "not established"))
        if full_unique:
            diag["skipped_searches"] = "uniform full-order bound with positive (or equality-event) entry floor excludes every other candidate"
        else:
            # asymmetric roots
            ar = asymmetric_roots(PRIM, pay)
            diag["asymmetric_attempts"] = ar
            for v in ar["roots"]:
                cand = asymmetric_candidate(PRIM, pay, v)
                val = validate(cand.sched, CONTROLS, price_pools=True)
                seq += 1
                if abs(cand.diagnostics["Psi"]) > 1e-6:
                    rows.append(_row(node, "asymmetric_discontinuity", cand, val, "rejected", "Psi sign change without root at a region boundary",
                                     cls=cls, seq=seq, run_id=run_id))
                    continue
                rows.append(_row(node, "asymmetric", cand, val, "numerical diagnostic" if val.accepted else "rejected", cls=cls, seq=seq, run_id=run_id))
            for v, resid in ar["tangencies"]:
                cand = asymmetric_candidate(PRIM, pay, v)
                val = validate(cand.sched, CONTROLS, price_pools=True)
                seq += 1
                rows.append(_row(node, "asymmetric_tangency", cand, val, "open" if not val.accepted else "numerical diagnostic",
                                 f"local |Psi| minimum {resid:.3e} without sign change", cls=cls, seq=seq, run_id=run_id))
                unresolved = unresolved or not val.accepted
            # Preserve each start before the shared search's within-call deduplication.
            fp = {"fixed_points": [], "unconverged": []}
            for init in [(u, v) for u in (0.2, 0.6, 0.95) for v in (0.2, 0.6, 0.95)]:
                result = pure_fixed_points(PRIM, pay, inits=[init], max_iter=40)
                for key in fp:
                    fp[key].extend(result[key])
            diag["pure_attempts"] = fp
            for u, v, init in fp["fixed_points"]:
                u, v = snap_endpoint(u), snap_endpoint(v)
                if refine_identity and u == 1.0 and 0.0 < v < 1.0:
                    from numerics.continuations import ORDER_IDENTITY_TOL
                    nearby = [root for root in ar["roots"] if abs(root - v) <= ORDER_IDENTITY_TOL]
                    if nearby:
                        v = min(nearby, key=lambda root: abs(root - v))
                # every converged start is validated and recorded; economic duplicates are merged below by the
                # continuation identity (complete strategies plus price information), never by orders alone
                sched = make_schedule(PRIM, pay, OrderProfile.pure(u, -v))
                cand = Candidate("pure", sched.profile, sched, {"init": init})
                val = validate(sched, CONTROLS, price_pools=True)
                seq += 1
                rows.append(_row(node, "pure", cand, val, "numerical diagnostic" if val.accepted else "rejected", cls=cls, seq=seq, run_id=run_id))
            if fp["unconverged"]:
                unresolved = True
                diag["pure_unconverged"] = len(fp["unconverged"])
                open_attempts += len(fp["unconverged"])
            ms = mixed_support_search(PRIM, pay, mesh=0.05, iters=150)
            prof = ms["profile"]
            diag["mixed_attempt"] = {k: v for k, v in ms.items() if k not in ("sched", "profile")}
            diag["mixed_attempt"]["profile"] = prof.__dict__
            if ms["converged"]:
                prof = OrderProfile(tuple(snap_endpoint(q) for q in prof.q_H), prof.w_H,
                                    tuple(snap_endpoint(q) for q in prof.q_L), prof.w_L)
                ms["sched"] = make_schedule(PRIM, pay, prof)
                diag["mixed_attempt"]["endpoint_refined_profile"] = prof.__dict__
                val = validate(ms["sched"], CONTROLS, price_pools=True)
                for state, qs, weights in (("H", prof.q_H, prof.w_H), ("L", prof.q_L, prof.w_L)):
                    if abs(sum(weights) - 1) > CONTROLS.probability_acceptance or any(w < 0 for w in weights) or any(abs(q) > 1 for q in qs):
                        val.breaches.append(f"mixed support/simplex invalid for {state}")
                if ms["support_gap"] > CONTROLS.deviation_gain_acceptance:
                    val.breaches.append(f"mixed support payoff gap={ms['support_gap']:.3e}")
                cand = Candidate("mixed", prof, ms["sched"], {})
                seq += 1
                rows.append(_row(node, "mixed", cand, val, "numerical diagnostic" if val.accepted else "rejected", cls=cls, seq=seq, run_id=run_id))
            elif not ms["converged"]:
                unresolved = True
                open_attempts += 1
                diag["mixed_search"] = f"not converged (support gap {ms['support_gap']:.2e})"
    # --- attempt ledger and economic deduplication ------------------------------------------------
    acc_raw = [x for x in rows if x["accepted"] is True]
    reps, absorbed = deduplicate([x["_cont"] for x in acc_raw], CONTROLS)
    merged = 0
    for cid, cands in absorbed.items():
        for extra_cid in cands[1:]:
            for x in acc_raw:
                if x["_cont"].candidate_id == extra_cid:
                    x["duplicate_of"] = cands[0]
                    merged += 1
    acc = [x for x in acc_raw if not x["duplicate_of"]]
    # same orders within the identity tolerance but different price information: kept distinct, and said so
    from numerics.continuations import _same_profile
    conts = {x["candidate_id"]: x for x in acc}
    for x in acc:
        for y in acc:
            if x is not y and _same_profile(x["_profile"], y["_profile"]):
                x["identity_note"] = f"orders within identity tolerance of {y['candidate_id']} but distinct price atoms/pools: kept as a distinct continuation"
    for x in rows:
        x.pop("_cont", None)
        x.pop("_profile", None)
    n_rej = sum(1 for x in rows if x["accepted"] is not True and not x["status"].startswith("open"))
    n_open = open_attempts + sum(1 for x in rows if x["status"].startswith("open"))
    if unresolved:
        outcome = "unresolved search (open nodes or unconverged starts retained)"
    elif not acc:
        outcome = "no accepted candidate found by the declared searches (not a nonexistence proof)"
    elif full_unique or ab["no_trade_unique_margin"] > 0:
        outcome = "analytically unique continuation"
    else:
        outcome = "accepted continuation(s) found; uniqueness not established"
    rng = {"value_law": law, "r": rs, "p": ps, "accepted_continuations_found": len(acc),
           "E_min_found": min(x["E"] for x in acc) if acc else NA, "E_max_found": max(x["E"] for x in acc) if acc else NA,
           "R_T_min_found": min(x["R_T"] for x in acc) if acc else NA, "R_T_max_found": max(x["R_T"] for x in acc) if acc else NA,
           "search_unresolved": unresolved or not acc, "global_envelope_certified": False,
           "p_exact": node.p_exact, "event_id": node.event_id, "candidates_evaluated": len(rows) + open_attempts, "candidates_accepted_raw": len(acc_raw),
           "candidates_rejected": n_rej, "candidates_unresolved": n_open, "duplicates_merged": merged, "search_outcome": outcome}
    diag["unresolved"] = unresolved
    diag["ledger"] = {"evaluated": len(rows) + open_attempts, "accepted_raw": len(acc_raw), "accepted_distinct": len(acc), "rejected": n_rej, "open": n_open, "merged": merged}
    result = finalize_node((rows, rng, diag))
    if any(row["identity_note"] for row in rows) and not refine_identity:
        refined_rows, refined_range, refined_diag = solve_reserve(node, run_id + ":identity_refined", refine_identity=True)
        refined_diag["prior_identity_attempt"] = result
        refined_diag["identity_refinement_method"] = ("A pure high-type endpoint with a nearby independently solved asymmetric root proposes that root "
                                                      "within the existing order-identity tolerance, then rebuilds and fully validates the schedule. "
                                                      "Raw prior profiles and validations remain in prior_identity_attempt.")
        if any(row["identity_note"] for row in refined_rows):
            raise ValueError(f"Economic identity remained unresolved after bounded root refinement: {node}")
        return refined_rows, refined_range, refined_diag
    return result


def reserve_grid(law: str) -> list[str]:
    top = Decimal(PRIM.h) + (Decimal(BENCHMARK_EXTRA["value_band_halfwidth"]) if law == "uniform_classes" else 0)
    pts = set(decimal_range("0", str(top), "0.05"))
    specials = set(DECLARED[law]) | set(STRENGTHS.values())
    ell, h, eV = Decimal(PRIM.ell), Decimal(PRIM.h), Decimal(BENCHMARK_EXTRA["value_band_halfwidth"])
    edges = {ell, h} if law == "binary" else {ell - eV, ell + eV, h - eV, h + eV}
    specials |= {str(e) for e in edges}
    for e in list(edges) + [Decimal(v) for v in STRENGTHS.values()]:
        for off in (Decimal("0.0001"), Decimal("-0.0001")):
            x = e + off
            if 0 <= x <= top:
                specials.add(str(x))
    return sorted(pts | specials, key=Decimal)


def reserve_nodes(law: str, rs: str) -> list[EventNode]:
    """Declared grid plus every support/participation event with one-sided offsets (spec 9.1)."""
    eps_V = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
    events = event_grid(PRIM, law, rs, eps_V, DECLARED[law])
    seen = {n.p_decimal for n in events}
    nodes = list(events)
    for ps in reserve_grid(law):
        n = node_from_args((law, rs, ps))
        if n.p_decimal not in seen:
            seen.add(n.p_decimal)
            nodes.append(n)
    nodes.sort(key=lambda n: Decimal(n.p_decimal))
    return nodes


def run(workers: int | None = None, quick: bool = False, max_refine_nodes: int | None = None, out: str | None = None, declared_only: bool = False, replay: str | None = None) -> bool:
    workers = workers or min(8, os.cpu_count() or 1)
    output_root = Path(out).resolve() if out else ROOT
    exercise = "c6_fixed_reserves" if declared_only else "c6_reserve"
    cont_file = "numerics/reserve_fixed_continuations.csv" if declared_only else "numerics/reserve_continuations.csv"
    range_file = "numerics/reserve_fixed_ranges.csv" if declared_only else "numerics/reserve_ranges.csv"
    run_id = datetime.now(timezone.utc).strftime("c6_%Y%m%dT%H%M%S%fZ")
    checkpoint = output_root / "audit/peer_polish" / run_id
    checkpoint.mkdir(parents=True, exist_ok=False)
    def collect(nodes, phase):
        with (checkpoint / f"{phase}.jsonl").open("w") as ledger:
            if replay:
                source = Path(replay) / f"{phase}.jsonl"
                records = [json.loads(line) for line in source.read_text().splitlines()]
                declared_nodes = {(n.law, n.r, n.p_exact): n for n in map(node_from_args, nodes)}
                expected = set(declared_nodes)
                actual = {(r[1]["value_law"], r[1]["r"], r[1]["p_exact"]) for r in records}
                if len(records) != len(nodes) or actual != expected:
                    raise ValueError(f"Replay ledger does not match requested {phase} nodes")
                for raw in records:
                    if any(row["identity_note"] for row in raw[0]):
                        key = (raw[1]["value_law"], raw[1]["r"], raw[1]["p_exact"])
                        result = solve_reserve(declared_nodes[key], raw[0][0]["run_id"])
                    else:
                        result = finalize_node(raw)
                    ledger.write(json.dumps(result, default=_json_default) + "\n")
                    yield result
                return
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futures = {ex.submit(solve_reserve, node, run_id): node for node in nodes}
                for completed, future in enumerate(as_completed(futures), 1):
                    node = futures[future]
                    try:
                        result = future.result()
                    except Exception as exc:
                        ledger.write(json.dumps({"node": str(node), "exception": repr(exc)}) + "\n")
                        ledger.flush()
                        for pending in futures:
                            pending.cancel()
                        raise
                    ledger.write(json.dumps(result, default=_json_default) + "\n")
                    ledger.flush()
                    if completed % 20 == 0 or completed == len(nodes):
                        print(f"C.6 {phase}: {completed}/{len(nodes)} nodes completed", flush=True)
                    yield result
    checks, notes = {}, []
    tasks = []
    for law in ("binary", "uniform_classes"):
        for rs in STRENGTHS.values():
            nodes = [node_from_args((law, rs, p)) for p in DECLARED[law]] if declared_only else reserve_nodes(law, rs)
            if quick:
                nodes = [n for n in nodes if n.event_id != "grid" and not n.event_id.startswith("offset")
                         or (n.event_id == "grid" and Decimal(n.p_exact) % Decimal("0.5") == 0)]
            tasks += nodes
    cont, ranges, diags = [], [], []
    for rows, rng, dg in collect(tasks, "initial"):
        cont += rows
        ranges.append(rng)
        diags.append(dg)
    # refinement: branch changes, unresolved nodes, and the found revenue maximum, to spacing 0.002
    refine = set()
    by_key = {(d["law"], d["r"]): [] for d in diags}
    for rng in ranges:
        by_key[(rng["value_law"], rng["r"])].append(rng)
    def acc_set(law, rs, ps):
        return frozenset(x["branch"] for x in cont if x["value_law"] == law and x["r"] == rs and x["p"] == ps and x["accepted"] is True)
    intervals = []
    for (law, rs), lst in by_key.items():
        lst.sort(key=lambda x: Decimal(x["p"]))
        best = max((x for x in lst if x["R_T_max_found"] != "n/a"), key=lambda x: x["R_T_max_found"], default=None)
        for a, b_ in zip(lst[:-1], lst[1:]):
            gap = Decimal(b_["p"]) - Decimal(a["p"])
            if gap <= Decimal("0.002"):
                continue
            why = []
            if acc_set(law, rs, a["p"]) != acc_set(law, rs, b_["p"]):
                why.append("branch change")
            if a["search_unresolved"] or b_["search_unresolved"]:
                why.append("unresolved")
            if best is not None and (a is best or b_ is best):
                why.append("revenue maximum")
            if why:
                intervals.append((law, rs, a["p"], b_["p"], "; ".join(why)))
    if declared_only:
        intervals = []
    for law, rs, pa, pb, why in intervals:
        x = Decimal(pa[:24]) + Decimal("0.002")
        while x < Decimal(pb[:24]):
            refine.add((law, rs, str(x)))
            x += Decimal("0.002")
    refine = sorted(refine, key=lambda t: (t[0], Decimal(t[1]), Decimal(t[2])))
    skipped = 0
    if max_refine_nodes is not None and len(refine) > max_refine_nodes:
        skipped = len(refine) - max_refine_nodes
        # keep refinement for revenue maxima and branch changes first, in listed order
        refine = refine[:max_refine_nodes]
    if refine and not quick and not declared_only:
        for rows, rng, dg in collect(refine, "refinement"):
            cont += rows
            ranges.append(rng)
            diags.append(dg)
    cont.sort(key=lambda x: (x["value_law"], Decimal(x["r"]), Decimal(x["p"][:24]), x["branch"]))
    ranges.sort(key=lambda x: (x["value_law"], Decimal(x["r"]), Decimal(x["p"][:24])))
    write_csv(output_root / cont_file, CONT_COLS, cont)
    write_csv(output_root / range_file, RANGE_COLS, ranges)
    # --- declared comparisons table ------------------------------------------------------------
    comp_rows = []
    for law in ("binary", "uniform_classes"):
        for rs in STRENGTHS.values():
            for ps in DECLARED[law]:
                pay, oracle_err = payoffs(law, float(rs), float(ps))
                ab = analytic_bounds(pay)
                acc = [x for x in cont if x["value_law"] == law and x["r"] == rs and x["p"] == ps and x["accepted"] is True and not x["duplicate_of"]]
                for x in acc:
                    if x["branch"] == "pooling":
                        margin = ab["no_trade_unique_margin"]
                        status = "analytical (unique no trade: k - Delta_T > 0)" if margin > 0 else "numerical diagnostic (pooling validated; uniqueness not established)"
                    elif x["branch"] == "full_orders":
                        margin = ab["full_unique_margin"]
                        status = ("analytical (unique full orders: (1-1/b) e(m) m Delta_T - k > 0 with positive floor)"
                                  if margin > 0 and ab["low_cost_floor_margin"] > 0 else "numerical diagnostic (full orders validated; uniqueness not established)")
                    else:
                        margin, status = NA, "numerical diagnostic (additional continuation found)"
                    eH, eL = 2 * x["O_H"], 2 * x["E"] - 2 * x["O_H"]
                    comp_rows.append({"value_law": law, "signal_information": "class only" if law == "uniform_classes" else "exact value",
                                      "epsilon_V": BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0", "r": rs, "p": ps,
                                      "t_0": pay.t_0, "t_H": pay.t_H, "t_L": pay.t_L, "g_H": pay.g_H, "g_L": pay.g_L, "Delta_T": pay.Delta_T,
                                      "q_H": x["q_H"], "q_L": x["q_L"], "e_H": eH, "e_L": eL, "E": x["E"], "R_T": x["R_T"],
                                      "low_cost_floor_margin": ab["low_cost_floor_margin"], "trading_margin": margin, "payoff_oracle_error": oracle_err,
                                      "status": status, "accepted": oracle_err <= TOL and len(acc) == 1,
                                      **{key: x[key] for key in ("parameter_set_id", "continuation_id", "candidate_id", "information_structure_id", "institution_id", "event_id", "p_exact", "branch")}})
                checks[f"declared_{law}_r{rs}_p{ps}"] = {"accepted_continuations": len(acc), "payoff_oracle_error": oracle_err,
                                                         "pass": len(acc) == 1 and oracle_err <= TOL}
    write_csv(output_root / "tables/reserve_comparisons.csv", ["value_law", "signal_information", "epsilon_V", "r", "p", "t_0", "t_H", "t_L", "g_H", "g_L", "Delta_T",
                                                 "q_H", "q_L", "e_H", "e_L", "E", "R_T", "low_cost_floor_margin", "trading_margin", "payoff_oracle_error",
                                                 "status", "accepted", "parameter_set_id", "continuation_id", "candidate_id", "information_structure_id", "institution_id", "event_id", "p_exact", "branch"], comp_rows)
    # revenue comparison at the declared reserves (alternative vs original at the same strength)
    for law in ("binary", "uniform_classes"):
        for rs in STRENGTHS.values():
            a_ = [x for x in comp_rows if x["value_law"] == law and x["r"] == rs and x["p"] == DECLARED[law][0] and x["accepted"]]
            b_ = [x for x in comp_rows if x["value_law"] == law and x["r"] == rs and x["p"] == DECLARED[law][1] and x["accepted"]]
            if a_ and b_:
                checks[f"revenue_comparison_{law}_r{rs}"] = {"R_T_original": a_[0]["R_T"], "R_T_alternative": b_[0]["R_T"],
                                                             "alternative_higher": b_[0]["R_T"] > a_[0]["R_T"], "E_original": a_[0]["E"], "E_alternative": b_[0]["E"]}
    max_oracle = max(d["payoff_oracle_error"] for d in diags)
    checks["payoff_oracle"] = {"max_error": max_oracle, "pass": max_oracle <= TOL}
    # counts come from the attempt/validation ledger (one range record per solved node), not from the grid length
    checks["sweep"] = {"nodes_attempted": len(ranges), "initial_nodes": len(tasks), "refined_nodes": len(refine) if not (quick or declared_only) else 0, "refinement_planned_nodes": len(refine), "refinement_intervals": intervals,
                       "refinement_skipped_nodes": skipped,
                       "identity_refinement_nodes": sum("prior_identity_attempt" in d for d in diags),
                       "prior_identity_candidates_preserved": sum(d["prior_identity_attempt"][1]["candidates_evaluated"] for d in diags if "prior_identity_attempt" in d),
                       "event_nodes": sum(1 for r_ in ranges if r_["event_id"] not in ("grid",) and not r_["event_id"].startswith("offset")),
                       "candidates_evaluated": sum(r_["candidates_evaluated"] for r_ in ranges),
                       "candidates_rejected": sum(r_["candidates_rejected"] for r_ in ranges),
                       "candidates_unresolved": sum(r_["candidates_unresolved"] for r_ in ranges),
                       "duplicates_merged": sum(r_["duplicates_merged"] for r_ in ranges),
                       "unresolved_nodes": sum(1 for r_ in ranges if r_["search_unresolved"]),
                       "nodes_without_accepted_continuation": sum(1 for r_ in ranges if r_["accepted_continuations_found"] == 0),
                       "nodes_analytically_unique": sum(1 for r_ in ranges if r_["search_outcome"].startswith("analytically unique")),
                       "refinement_rule": "intervals with a change in the accepted branch set, an unresolved endpoint, or the found revenue maximum are refined to 0.002"}
    passed = all(c.get("pass", True) for c in checks.values())
    if out:
        from numerics import io
        original_manifest_dir = io.MANIFEST_DIR
        io.MANIFEST_DIR = output_root / "numerics/manifests"
    write_manifest(exercise, {"benchmark": PRIM.__dict__, "epsilon_V": BENCHMARK_EXTRA["value_band_halfwidth"], "declared": DECLARED,
                                  "strengths": STRENGTHS, "run_id": run_id, "replay_source": replay, "workers": workers, "endpoint_refinement": "orders within solver tolerance 1e-7 of -1,0,1 proposed at exact boundary and fully revalidated; raw solver profiles retained", "attempt_ledger": str(checkpoint.relative_to(output_root)), "grid": "0..h (+eps_V for classes) by 0.05 plus events {0, ell, r, h, ell+-eps_V, h+-eps_V, declared reserves, p_L = h - c_L/m, "
                                          "p_H = sqrt(2r(h - c_H/M) - r^2)} with one-sided offsets 1e-4, 1e-6, 1e-8", "quick": quick, "declared_only": declared_only},
                   "Payoff oracle: direct integration of OA.50 over R (and over class bands) versus OA.51/OA.52; continuation candidates "
                   "(pooling, full, asymmetric, pure, mixed) validated with price-pool handling (OA.70) at every reserve; analytical uniqueness "
                   "bounds (Delta_T < k; uniform derivative bound with positive floor) recorded and used to skip exploratory searches only where they hold. "
                   "Exact events are classified algebraically at 50 digits with the tie rule; accepted candidates are merged only by the "
                   "continuation identity (complete strategies plus price information); counts come from the attempt ledger.",
                   CONTROLS.as_dict(), [str(output_root / name) if out else name for name in ("tables/reserve_comparisons.csv", cont_file, range_file)], checks, passed, notes)
    if out:
        io.MANIFEST_DIR = original_manifest_dir
    print("C.6 passed" if passed else "C.6 FAILED", {k: v for k, v in checks.items() if k.startswith(("declared", "revenue", "payoff", "sweep"))})
    return passed


if __name__ == "__main__":
    w = next((int(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--workers=")), None)
    o = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--out=")), None)
    replay = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--replay=")), None)
    sys.exit(0 if run(workers=w, quick="--quick" in sys.argv, out=o, declared_only="--declared-only" in sys.argv, replay=replay) else 1)
