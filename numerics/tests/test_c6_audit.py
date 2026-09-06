"""C.6 acceptance, null semantics, and attempt-count regression checks."""
from numerics.exercises.c6_reserve import PRIM, CONTROLS, _row, node_from_args, payoffs, solve_reserve
from numerics.reserve_events import classify_node
from numerics.search import pooling_candidate
from numerics.validation import validate


def test_rejected_candidate_cannot_remain_accepted():
    node = node_from_args(("binary", "1.2", "0.5"))
    pay, _ = payoffs("binary", 1.2, 0.5)
    cand = pooling_candidate(PRIM, pay)
    val = validate(cand.sched, CONTROLS, price_pools=True)
    if not val.accepted:
        raise ValueError("Regression setup must be a valid pooling candidate")
    row = _row(node, "asymmetric_discontinuity", cand, val, "rejected", "sign change without root",
               cls=classify_node(PRIM, node, "0"), seq=1, run_id="test")
    if row["accepted"] or "sign change without root" not in row["rejection_reason"]:
        raise ValueError("Explicit root rejection was lost at the acceptance boundary")


def test_degenerate_node_ledger_and_missing_pool_posterior():
    rows, rng, diag = solve_reserve(("binary", "1.2", "10"), run_id="test")
    if rng["candidates_evaluated"] != rng["candidates_accepted_raw"] + rng["candidates_rejected"] + rng["candidates_unresolved"]:
        raise ValueError("Attempt ledger counts do not partition attempted candidates")
    if not rows or rng["accepted_continuations_found"] != 1:
        raise ValueError("No-entry endpoint must retain its validated pooling continuation")
    for row in rows:
        if row["accepted"] and row["error_budget_breaches"]:
            raise ValueError("Accepted candidate exceeds its numerical budget")


def test_endpoint_refinement_does_not_inflate_continuation_count():
    rows, rng, diag = solve_reserve(("binary", "1.2", "6.2817191715409547646397125286473"), run_id="test")
    if rng["accepted_continuations_found"] != 1 or rng["duplicates_merged"] != 10:
        raise ValueError("Approximate endpoints inflated economic multiplicity")
    if len(diag["pure_attempts"]["fixed_points"]) != 9:
        raise ValueError("Original pure solver attempts were lost")
    for row in rows:
        if row["accepted"] and (row["q_H"], row["q_L"]) != (1.0, -1.0):
            raise ValueError("Endpoint proposal was not revalidated as the exact full-order candidate")


def test_terminal_rejection_preserves_open_search_and_raw_attempt():
    from numerics.exercises.c6_reserve import finalize_node
    row = {"accepted": False, "result_status": "rejected", "rejection_reason": "epsilon_q=0.01",
           "status": "open"}
    rng = {"candidates_evaluated": 2, "candidates_rejected": 0, "candidates_unresolved": 2,
           "search_unresolved": True}
    diag = {"ledger": {"evaluated": 2, "rejected": 0, "open": 2}}
    rows, result, _ = finalize_node(([row], rng, diag))
    if rows[0]["status"] != "rejected" or not result["search_unresolved"]:
        raise ValueError("Rejected terminal candidate and open search were conflated")
    if result["candidates_rejected"] != 1 or result["candidates_unresolved"] != 1:
        raise ValueError("Reclassification changed or lost attempted candidates")
    if row["status"] != "open" or rng["candidates_rejected"] != 0:
        raise ValueError("Immutable raw attempt was modified")
