"""C.6c: exact reserve events and admissible-bid outcomes (peer-circulation spec section 9; tests T21, T22, T23).

Runs the C.6 node solver (repaired continuation identity, tie rules applied to declared identities) on the
event grid only: 0, ell, r, h, ell +- eps_V, h +- eps_V, the declared reserve alternatives, the exact events
p_L = h - c_L/m and p_H = sqrt(2r(h - c_H/M) - r^2), each with one-sided offsets 1e-4, 1e-6, 1e-8, and the
published sampled weak reserve 6.280. Writes numerics/reserve_events.csv (the C.6 continuation schema plus
event classification) and numerics/reserve_event_ranges.csv, and a manifest. The full C.6 sweep is untouched.
"""
from __future__ import annotations

import sys
import json
from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor, as_completed
from decimal import Decimal
from pathlib import Path

import mpmath as mp

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.exercises.c6_reserve import (BENCHMARK_EXTRA, CONT_COLS, DECLARED, PRIM, RANGE_COLS, STRENGTHS, TOL,  # noqa: E402
                                           finalize_node, node_from_args, solve_reserve)
from numerics.io import _json_default, write_csv, write_manifest  # noqa: E402
from numerics.params import CONTROLS  # noqa: E402
from numerics.reserve_events import EventNode, classify_node, event_grid, full_order_objects_mp  # noqa: E402

RUN_ID = "c6c"
SAMPLED_WEAK_RESERVE = "6.280"
EVENT_CLASSIFICATION = {
    "floor_equality_p_L": "analytically supported event candidate: B_r(m) = c_L holds exactly and entry is admitted by the tie rule; "
                          "supported by the inversion/global-bound argument with e >= rho under equality; NOT an interior point of the strict "
                          "low-cost inequality region",
    "ceiling_equality_p_H": "analytically supported event candidate: M g_H = c_H holds exactly, tau = M and x* = 1; the upper plateau "
                            "(positive probability) enters by the tie rule; low-cost floor strictly positive and full-order bound checked separately",
}
LANDMARKS = {"p_L": {"value": "6.2817181715", "E": "0.25", "sale": "0.125", "R_T": "0.7852147714"},
             "p_H": {"value": "1.3252698283", "E": "0.5064773952", "R_T": "1.0688544444", "alpha_H": "0.5", "x_star": "1"},
             "sampled_6.280": {"E": "0.25", "sale": "0.125", "two_admissible": "0", "R_T": "0.785"}}


class RegressionError(Exception):
    pass


def _solve(node: EventNode):
    return solve_reserve(node, run_id=RUN_ID)


def event_nodes() -> list[EventNode]:
    nodes: list[EventNode] = []
    for law in ("binary", "uniform_classes"):
        eps_V = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
        for rs in STRENGTHS.values():
            nodes += event_grid(PRIM, law, rs, eps_V, DECLARED[law])
    n = node_from_args(("binary", "1.2", SAMPLED_WEAK_RESERVE))
    nodes.append(EventNode(n.law, n.r, n.p_exact, n.p_decimal, "published_sampled_weak_reserve_6.280", "published sampled weak reserve (Table 4 discussion)", True))
    return nodes


def _close(a: float, target: str, tol: float) -> bool:
    return abs(a - float(target)) <= tol


def run(workers: int | None = None, replay: str | None = None) -> bool:
    import os
    workers = workers or min(8, os.cpu_count() or 1)
    nodes = event_nodes()
    cont, ranges, diags = [], [], []
    run_id = datetime.now(timezone.utc).strftime("c6c_%Y%m%dT%H%M%S%fZ")
    ledger_path = Path("audit/peer_polish") / f"{run_id}.jsonl"
    def completed_results():
        if replay:
            records = [json.loads(line) for line in Path(replay).read_text().splitlines()]
            expected = {(n.law, n.r, n.p_exact) for n in nodes}
            actual = {(r[1]["value_law"], r[1]["r"], r[1]["p_exact"]) for r in records}
            if len(records) != len(nodes) or actual != expected:
                raise ValueError("Event replay ledger does not match requested nodes")
            yield from map(finalize_node, records)
        else:
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futures = {ex.submit(solve_reserve, node, run_id): node for node in nodes}
                for future in as_completed(futures):
                    yield future.result()
    with ledger_path.open("w") as ledger:
        for completed, (rows, rng, dg) in enumerate(completed_results(), 1):
            ledger.write(json.dumps((rows, rng, dg), default=_json_default) + "\n")
            ledger.flush()
            cont += rows
            ranges.append(rng)
            diags.append(dg)
            if completed % 20 == 0 or completed == len(nodes):
                print(f"C.6c: {completed}/{len(nodes)} nodes completed", flush=True)
    for x in cont:
        x["event_classification"] = EVENT_CLASSIFICATION.get(x["event_id"], "")
    cont.sort(key=lambda x: (x["value_law"], Decimal(x["r"]), Decimal(x["p"][:24]), x["branch"]))
    ranges.sort(key=lambda x: (x["value_law"], Decimal(x["r"]), Decimal(x["p"][:24])))
    checks: dict = {}

    def acc_rows(law, rs, event_id, branch=None):
        return [x for x in cont if x["value_law"] == law and x["r"] == rs and x["event_id"] == event_id and x["accepted"] is True
                and (branch is None or x["branch"] == branch)]

    # --- T21: exact floor event -------------------------------------------------------------------
    t21 = {}
    for law in ("binary", "uniform_classes"):
        for rs in STRENGTHS.values():
            eps_V = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
            node = next(n for n in nodes if n.law == law and n.r == rs and n.event_id == "floor_equality_p_L")
            cls = classify_node(PRIM, node, eps_V)
            fo = full_order_objects_mp(PRIM, cls, False, True)
            rows = acc_rows(law, rs, "floor_equality_p_L", "full_orders")
            ok = (cls["low_cost_floor_relation"] == "equality_event" and len(rows) == 1
                  and _close(rows[0]["E"], LANDMARKS["p_L"]["E"], 1e-10) and _close(rows[0]["sale_probability"], LANDMARKS["p_L"]["sale"], 1e-10)
                  and _close(rows[0]["R_T"], LANDMARKS["p_L"]["R_T"], 1e-10) and _close(float(fo["R_T"]), LANDMARKS["p_L"]["R_T"], 1e-10)
                  and _close(node.p_float, LANDMARKS["p_L"]["value"], 1e-10) and rows[0]["two_admissible_bidders_probability"] == 0.0
                  and "equality" in rows[0]["status"] and "strict" not in rows[0]["status"].split("equality")[0])
            # both sides classify strictly (no rounded tie): below the event the floor is strictly positive, above strictly negative
            below = [d for d in diags if d["law"] == law and d["r"] == rs and d["event_id"].startswith("offset:floor_equality_p_L-")]
            above = [d for d in diags if d["law"] == law and d["r"] == rs and d["event_id"].startswith("offset:floor_equality_p_L+")]
            sides_ok = all(d["low_cost_floor_relation"] == "strict_positive" for d in below) and all(d["low_cost_floor_relation"] == "strict_negative" for d in above) \
                and len(below) == 3 and len(above) == 3
            t21[f"{law}_r{rs}"] = {"p_L": node.p_decimal, "floor_relation": cls["low_cost_floor_relation"], "accepted_full_order_rows": len(rows),
                                  "E": rows[0]["E"] if rows else None, "sale": rows[0]["sale_probability"] if rows else None, "R_T": rows[0]["R_T"] if rows else None,
                                  "R_T_mp": mp.nstr(fo["R_T"], 16), "status": rows[0]["status"] if rows else None, "sides_strict": sides_ok,
                                  "classification": EVENT_CLASSIFICATION["floor_equality_p_L"], "pass": bool(ok and sides_ok)}
    checks["T21_floor_event"] = {**t21, "pass": all(v["pass"] for v in t21.values())}
    # --- T22: exact ceiling event (defined only at r = 3) -------------------------------------------
    t22 = {}
    for law in ("binary", "uniform_classes"):
        for rs in STRENGTHS.values():
            eps_V = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
            node = next(n for n in nodes if n.law == law and n.r == rs and n.event_id == "ceiling_equality_p_H")
            cls = classify_node(PRIM, node, eps_V)
            if not node.applicable:
                t22[f"{law}_r{rs}"] = {"applicable": False, "p_H_value": node.p_decimal, "regime": cls["regime"],
                                      "note": "event outside its defining regime (p_H > r); treated as an ordinary reserve node", "pass": cls["ceiling_relation"] != "equality_event"}
                continue
            fo = full_order_objects_mp(PRIM, cls, True, False)
            rows = acc_rows(law, rs, "ceiling_equality_p_H", "full_orders")
            ok = (cls["ceiling_relation"] == "equality_event" and cls["low_cost_floor_relation"] == "strict_positive" and len(rows) == 1
                  and _close(rows[0]["E"], LANDMARKS["p_H"]["E"], 1e-10) and _close(rows[0]["R_T"], LANDMARKS["p_H"]["R_T"], 1e-10)
                  and _close(float(fo["E"]), LANDMARKS["p_H"]["E"], 1e-10) and float(fo["alpha_H"]) == 0.5 and float(fo["x_star"]) == 1.0
                  and _close(float(fo["alpha_L"]), str(0.5 * mp.e ** -1), 1e-12) and _close(node.p_float, LANDMARKS["p_H"]["value"], 1e-10)
                  and cls["full_unique_relation"] == "strict_positive")
            t22[f"{law}_r{rs}"] = {"applicable": True, "p_H": node.p_decimal, "ceiling_relation": cls["ceiling_relation"], "floor_relation": cls["low_cost_floor_relation"],
                                  "alpha_H": mp.nstr(fo["alpha_H"], 16), "alpha_L": mp.nstr(fo["alpha_L"], 16), "x_star": mp.nstr(fo["x_star"], 5),
                                  "E": rows[0]["E"] if rows else None, "R_T": rows[0]["R_T"] if rows else None, "E_mp": mp.nstr(fo["E"], 16), "R_T_mp": mp.nstr(fo["R_T"], 16),
                                  "full_unique_relation": cls["full_unique_relation"], "pass": bool(ok)}
    checks["T22_ceiling_event"] = {**t22, "pass": all(v["pass"] for v in t22.values())}
    # --- T23: outcome measures --------------------------------------------------------------------
    samp = acc_rows("binary", "1.2", "published_sampled_weak_reserve_6.280")
    samp_ok = (len(samp) == 1 and _close(samp[0]["E"], "0.25", 1e-10) and _close(samp[0]["sale_probability"], "0.125", 1e-10)
               and samp[0]["two_admissible_bidders_probability"] == 0.0 and _close(samp[0]["R_T"], "0.785", 5e-4)
               and _close(samp[0]["R_T"], str(0.25 * 6.280 / 2), 1e-10))
    ident_ok = all(("outcome identity" not in (x["unresolved_reason"] or "")) for x in cont)
    bounds_ok = all(0 <= x["two_admissible_bidders_probability"] <= x["admissible_challenger_probability"] + 1e-15 <= x["preparation_probability"] + 2e-15 <= 1 + 3e-15
                    and 0 <= x["sale_probability"] <= 1 + 1e-15 for x in cont)
    checks["T23_outcome_measures"] = {"sampled_6.280": {k_: samp[0][k_] for k_ in ("E", "admissible_challenger_probability", "sale_probability",
                                                                                   "two_admissible_bidders_probability", "high_value_ownership_probability", "R_T")} if samp else None,
                                      "union_identity_all_rows": ident_ok, "bounds_all_rows": bounds_ok, "rows": len(cont), "pass": bool(samp_ok and ident_ok and bounds_ok)}
    # --- ledger --------------------------------------------------------------------------------------
    checks["ledger"] = {"nodes_attempted": len(ranges), "candidates_evaluated": sum(r_["candidates_evaluated"] for r_ in ranges),
                        "candidates_rejected": sum(r_["candidates_rejected"] for r_ in ranges), "candidates_unresolved": sum(r_["candidates_unresolved"] for r_ in ranges),
                        "duplicates_merged": sum(r_["duplicates_merged"] for r_ in ranges), "unresolved_nodes": sum(1 for r_ in ranges if r_["search_unresolved"]),
                        "nodes_without_accepted_continuation": [f'{r_["value_law"]} r={r_["r"]} p={r_["p"][:14]}' for r_ in ranges if r_["accepted_continuations_found"] == 0],
                        "nodes_with_multiple_distinct_continuations": [f'{r_["value_law"]} r={r_["r"]} p={r_["p"][:14]} ({r_["accepted_continuations_found"]})'
                                                                       for r_ in ranges if r_["accepted_continuations_found"] > 1]}
    max_oracle = max(d["payoff_oracle_error"] for d in diags)
    checks["payoff_oracle"] = {"max_error": max_oracle, "pass": max_oracle <= TOL}
    write_csv("numerics/reserve_events.csv", CONT_COLS + ["event_classification"], cont)
    write_csv("numerics/reserve_event_ranges.csv", RANGE_COLS, ranges)
    passed = all(c.get("pass", True) for c in checks.values())
    write_manifest("c6c_reserve_events", {"benchmark": PRIM.__dict__, "epsilon_V": BENCHMARK_EXTRA["value_band_halfwidth"], "declared": DECLARED, "strengths": STRENGTHS,
                                          "events": "0, ell, r, h, ell+-eps_V, h+-eps_V (classes), declared reserves, p_L = h - c_L/m, p_H = sqrt(2r(h - c_H/M) - r^2)",
                                          "offsets": ["1e-4", "1e-6", "1e-8"], "sampled_weak_reserve": SAMPLED_WEAK_RESERVE, "landmarks": LANDMARKS, "workers": workers, "replay_source": replay, "run_id": run_id, "attempt_ledger": str(ledger_path)},
                   "Event nodes solved with the C.6 node solver: exact events classified algebraically at 50 digits with the tie rule applied to the "
                   "declared identity; offsets classified by high-precision sign; payoff oracle by direct OA.50 integration; continuation candidates "
                   "validated with price pools (OA.70); outcome measures E, A, S, C2, O_H from the actual allocation event with the union identity "
                   "S = Pr(R >= p) + A - C2 checked by direct integration; accepted candidates merged only by the continuation identity.",
                   CONTROLS.as_dict(), ["numerics/reserve_events.csv", "numerics/reserve_event_ranges.csv", str(ledger_path)], checks, passed,
                   ["Event candidates improve sampled maxima; they prove neither global optimality nor envelope completeness.",
                    "A node without an accepted candidate is 'no candidate found by the declared searches', not nonexistence."])
    print("C.6c passed" if passed else "C.6c FAILED", {k_: v_.get("pass") for k_, v_ in checks.items()}, checks["ledger"])
    return passed


if __name__ == "__main__":
    w = next((int(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--workers=")), None)
    replay = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--replay=")), None)
    sys.exit(0 if run(workers=w, replay=replay) else 1)
