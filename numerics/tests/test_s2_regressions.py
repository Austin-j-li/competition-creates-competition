"""S2 regressions: T18 to T23 and the full-domain auction regime cases.

Plain test functions. Run with `.venv/bin/python -m pytest numerics/tests` when pytest is installed, or
`.venv/bin/python numerics/tests/test_s2_regressions.py` (the __main__ runner prints one line per test and
exits nonzero on any failure).
"""
from __future__ import annotations

import sys
import traceback
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import kernel_uniform, payoffs_closed_form, payoffs_integrated  # noqa: E402
from numerics.continuations import (economically_equivalent, deduplicate, make_pooled_schedule, orders_only_key, payoff_regime,  # noqa: E402
                                    payoffs_exact, rational_full_order_bound, validate_pooled_schedule)
from numerics.exercises import c6b_price_pools as c6b  # noqa: E402
from numerics.exercises.c6_reserve import node_from_args, reserve_nodes, solve_reserve  # noqa: E402
from numerics.information import OrderProfile, make_schedule  # noqa: E402
from numerics.params import BENCHMARK, CONTROLS  # noqa: E402
from numerics.reserve_events import classify_node, event_grid, full_order_objects_mp, outcome_measures  # noqa: E402
from numerics.validation import validate  # noqa: E402


class Check(Exception):
    pass


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise Check(msg)


# --- auction oracle over the full reserve domain (T03 support for the S2 cases) ------------------------
def test_auction_full_domain_regimes():
    P = BENCHMARK
    r = 1.2
    cases = {  # p: (t_0, t_H, t_L, g_H, g_L)
        7.0: (0.0, 7.0, 0.0, 3.0, 0.0),           # r < p < h  (spec 8.1)
        1.2: (0.0, 1.2, 0.0, 8.8, 0.0),           # p = r
        1.0: (1 - 1 / 1.2, 0.6 + 1 / 2.4, 1.0, 10 - 0.6 - 1 / 2.4, 0.0),  # p = ell: low value bids at the reserve (admissible)
        10.0: (0.0, 10.0, 0.0, 0.0, 0.0),         # p = h: zero rent, sale at the reserve
        10.5: (0.0, 0.0, 0.0, 0.0, 0.0),          # p > h: no sale
    }
    for p, want in cases.items():
        cf = payoffs_closed_form(P, r, p)
        it, _ = payoffs_integrated(P, r, p)
        got = (cf.t_0, cf.t_H, cf.t_L, cf.g_H, cf.g_L)
        require(max(abs(a - b) for a, b in zip(got, want)) < 1e-12, f"closed form at p={p}: {got} vs {want}")
        require(max(abs(getattr(cf, a) - getattr(it, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L")) < 1e-9, f"integration oracle at p={p}")
    ex = payoffs_exact(P, Fraction(6, 5), Fraction(7))
    require((ex["t_0"], ex["t_L"], ex["g_L"], ex["t_H"], ex["g_H"]) == (0, 0, 0, 7, 3), f"exact rational payoffs {ex}")
    require(payoff_regime(1, 10, Fraction(6, 5), Fraction(7)).startswith("r<p<h"), "regime label")
    require(payoff_regime(1, 10, Fraction(3), Fraction(1)).startswith("p=ell"), "p = ell regime label")
    # ell < p < r regime (strong benchmark): t_L = t_0, g_L = 0, t_H = r/2 + p^2/(2r)
    cf = payoffs_closed_form(P, 3.0, 1.5)
    require(abs(cf.t_L - cf.t_0) < 1e-15 and cf.g_L == 0 and abs(cf.t_H - (1.5 + 2.25 / 6)) < 1e-15, "ell<p<r kernel")


# --- T18: valid fixed-order price-pool family ------------------------------------------------------------
def test_T18_price_pool_family_all_members_validate():
    fam = c6b.cutoff_family()
    got = []
    for tag, c in fam:
        row, cont, pv = c6b.evaluate_member(tag, c)
        require(row["accepted"], f"member {tag} rejected: {pv.evidence.breaches}")
        got.append((row["preparation_probability"], row["seller_revenue"], row["pool_posterior"]))
    require(all(a[0] > b[0] and a[1] > b[1] for a, b in zip(got[:-1], got[1:])), "prep/revenue not decreasing in the cutoff")
    lm = c6b.LANDMARKS
    for i, key in ((0, "c=-log2"), (16, "c=0")):
        require(abs(got[i][2] - float(lm[key]["pool_posterior"])) <= 1e-10, f"{key} pool posterior {got[i][2]}")
        require(abs(got[i][0] - float(lm[key]["preparation"])) <= 1e-10, f"{key} preparation {got[i][0]}")
        require(abs(got[i][1] - float(lm[key]["revenue"])) <= 1e-10, f"{key} revenue {got[i][1]}")
        cf = c6b.closed_forms(fam[i][1])
        require(abs(float(cf["sale"]) - float(lm[key]["sale"])) <= 1e-10 and float(cf["two_admissible"]) == 0.0, f"{key} closed-form sale")


def test_T18_global_bound_is_rational_and_exceeds_targets():
    P = c6b.PRIM
    gb = rational_full_order_bound(P, Fraction(7), Fraction(0))
    require(gb["available"] and isinstance(gb["J_lower_bound"], Fraction), "bound must be an exact Fraction")
    require(gb["J_lower_bound"] >= Fraction(7, 32), f"J lower bound {gb['J_lower_bound']} < 7/32")
    require(gb["Uprime_lower_bound"] >= Fraction(143, 1600), f"U' lower bound {gb['Uprime_lower_bound']} < 143/1600")
    # mesh derivative scan is only an implementation check: it must sit above the rational bound
    sched, pay = c6b.build(-float(mp.log(2)), "-log2")
    pv = validate_pooled_schedule(sched, CONTROLS, cutoff_exact=-mp.log(2))
    require(pv.global_bound["min_dU_mesh"] >= float(gb["Uprime_lower_bound"]), "mesh derivative below the rational bound")
    require(pv.global_bound["J_H"] >= float(gb["J_lower_bound"]) and pv.global_bound["J_gap"] < 1e-9, "numeric J inconsistent with the bound")
    require(pv.evidence.investor_deviation_gain_upper_bound == 0.0, "rigorous upper bound should be 0 when the bound holds")
    # and unavailable (None, not 0) when the hypotheses fail
    gb2 = rational_full_order_bound(P, Fraction(7), Fraction(3, 2))
    require(not gb2["available"], "bound must be unavailable when the cutoff exceeds 1")


# --- T19: invalid controls fail for the stated reasons -----------------------------------------------------
def test_T19_negative_controls():
    row, cont, pv = c6b.evaluate_member("-1", mp.mpf(-1), candidate_tag="ctrl")
    require(not cont.accepted and any("buyer_deviation_at_positive_price_c_L" in b for b in pv.evidence.breaches), f"c=-1 breaches {pv.evidence.breaches}")
    row, cont, pv = c6b.evaluate_member("1", mp.mpf(1), candidate_tag="ctrl")
    require(not cont.accepted and any("buyer_deviation_at_zero_price_c_L" in b for b in pv.evidence.breaches), f"c=1 breaches {pv.evidence.breaches}")
    row, cont, pv = c6b.evaluate_member("0", mp.mpf(0), candidate_tag="ctrl", raw_posterior_in_pool=True)
    require(not cont.accepted and any("preparation_not_price_measurable" in b for b in pv.evidence.breaches), f"raw-posterior control {pv.evidence.breaches}")
    require(any(b.startswith("epsilon_P") for b in pv.evidence.breaches), "raw-posterior policy must also break conditional pricing")


# --- T20: continuation identity ---------------------------------------------------------------------------
def test_T20_identity_same_orders_different_pools_distinct_and_duplicates_merge():
    fam = c6b.cutoff_family()
    _, c0, _ = c6b.evaluate_member(*fam[0])
    _, c16, _ = c6b.evaluate_member(*fam[16])
    _, c0b, _ = c6b.evaluate_member(*fam[0], candidate_tag="other_start")
    require(orders_only_key(c0) == orders_only_key(c16), "an orders-only key must (wrongly) merge the endpoints; the test exposes it")
    require(not economically_equivalent(c0, c16, CONTROLS), "endpoints with different pools must be distinct continuations")
    require(c0.continuation_id != c16.continuation_id, "continuation ids must differ across pools")
    require(economically_equivalent(c0, c0b, CONTROLS) and c0.candidate_id != c0b.candidate_id and c0.continuation_id == c0b.continuation_id,
            "repeated construction must share the continuation id but keep its own candidate id")
    reps, absorbed = deduplicate([c0, c16, c0b], CONTROLS)
    require(len(reps) == 2 and absorbed[c0.continuation_id] == (c0.candidate_id, c0b.candidate_id), f"dedupe {absorbed}")
    # identity never keys on revenue / entry alone: two rows with equal revenue but different atoms stay distinct
    require(abs(c0.outcome.R_T - c16.outcome.R_T) > 0.05, "sanity: endpoints have different revenue")


# --- T21: exact floor event -------------------------------------------------------------------------------
def test_T21_exact_floor_event_classified_algebraically():
    nodes = {n.event_id: n for n in reserve_nodes("binary", "1.2")}
    node = nodes["floor_equality_p_L"]
    cls = classify_node(BENCHMARK, node, "0")
    require(cls["low_cost_floor_relation"] == "equality_event", f"floor relation {cls['low_cost_floor_relation']}")
    require(abs(node.p_float - 6.2817181715) < 1e-10, f"p_L {node.p_decimal}")
    for off in ("0.0001", "0.000001", "0.00000001"):
        below = classify_node(BENCHMARK, nodes[f"offset:floor_equality_p_L-{off}"], "0")
        above = classify_node(BENCHMARK, nodes[f"offset:floor_equality_p_L+{off}"], "0")
        require(below["low_cost_floor_relation"] == "strict_positive" and above["low_cost_floor_relation"] == "strict_negative",
                f"offset {off}: {below['low_cost_floor_relation']}, {above['low_cost_floor_relation']}")
    rows, rng, diag = solve_reserve(node, run_id="test")
    full = [x for x in rows if x["branch"] == "full_orders"]
    require(len(full) == 1 and full[0]["accepted"] is True, f"full orders at p_L: {full}")
    require(abs(full[0]["E"] - 0.25) < 1e-10 and abs(full[0]["sale_probability"] - 0.125) < 1e-10, "E, sale at p_L")
    require(abs(full[0]["R_T"] - 0.7852147714) < 1e-10, f"R_T at p_L {full[0]['R_T']}")
    require("equality" in full[0]["status"] and "tie rule" in full[0]["status"], f"status must name the equality/tie support: {full[0]['status']}")
    require(full[0]["event_id"] == "floor_equality_p_L" and "B_r(m) = c_L" in full[0]["event_defining_relation"], "event columns")
    # the tie is symbolic: a schedule with tie_at_floor enters everywhere; a float comparison at the same p may not
    pay = payoffs_closed_form(BENCHMARK, 1.2, node.p_float)
    s_tie = make_schedule(BENCHMARK, pay, OrderProfile.pure(1.0, -1.0), tie_at_floor=True)
    require(float(s_tie.entry(np.array([-5.0]))[0]) == 0.25, "tie_at_floor must prescribe low-cost entry on the lower plateau")


# --- T22: exact ceiling event -----------------------------------------------------------------------------
def test_T22_exact_ceiling_event_plateau_enters():
    nodes = {n.event_id: n for n in reserve_nodes("binary", "3")}
    node = nodes["ceiling_equality_p_H"]
    require(node.applicable and abs(node.p_float - 1.3252698283) < 1e-10, f"p_H {node.p_decimal}")
    cls = classify_node(BENCHMARK, node, "0")
    require(cls["ceiling_relation"] == "equality_event" and cls["low_cost_floor_relation"] == "strict_positive", "relations at p_H")
    fo = full_order_objects_mp(BENCHMARK, cls, True, False)
    require(float(fo["alpha_H"]) == 0.5 and float(fo["x_star"]) == 1.0 and abs(float(fo["alpha_L"]) - 0.5 * float(mp.e ** -1)) < 1e-15, "plateau objects")
    require(abs(float(fo["E"]) - 0.5064773952) < 1e-10 and abs(float(fo["R_T"]) - 1.0688544444) < 1e-10, f"E, R_T at p_H: {fo['E']}, {fo['R_T']}")
    rows, rng, diag = solve_reserve(node, run_id="test")
    full = [x for x in rows if x["branch"] == "full_orders"]
    require(len(full) == 1 and full[0]["accepted"] is True and abs(full[0]["E"] - 0.5064773952) < 1e-10 and abs(full[0]["R_T"] - 1.0688544444) < 1e-10,
            f"validated full orders at p_H: {full}")
    # at r = 1.2 the same formula is outside its regime and must not be treated as an event
    n12 = {n.event_id: n for n in reserve_nodes("binary", "1.2")}["ceiling_equality_p_H"]
    require(not n12.applicable and classify_node(BENCHMARK, n12, "0")["ceiling_relation"] != "equality_event", "p_H at r=1.2 is not an event")


# --- T23: sale / admissible / competitive probabilities ----------------------------------------------------
def test_T23_outcome_measures():
    om = outcome_measures(BENCHMARK, "binary", "0", 1.2, 6.280, 0.25, 0.25)
    require(om["E"] == 0.25 and abs(om["S"] - 0.125) < 1e-15 and om["C2"] == 0.0 and om["S_identity_error"] < 1e-12 and om["bounds_ok"], f"6.280: {om}")
    rows, rng, diag = solve_reserve(node_from_args(("binary", "1.2", "6.280")), run_id="test")
    acc = [x for x in rows if x["accepted"] is True]
    require(len(acc) == 1 and abs(acc[0]["E"] - 0.25) < 1e-10 and abs(acc[0]["sale_probability"] - 0.125) < 1e-10
            and acc[0]["two_admissible_bidders_probability"] == 0.0 and abs(acc[0]["R_T"] - 0.785) < 1e-10, f"6.280 accepted rows {acc}")
    # low reserve with the incumbent in play: union identity and bounds with C2 > 0
    om = outcome_measures(BENCHMARK, "binary", "0", 3.0, 0.5, 0.9, 0.6)
    require(abs(om["S"] - (om["Pr_R_ge_p"] + om["A"] - om["C2"])) < 1e-15 and om["C2"] > 0 and om["S_identity_error"] < 1e-12 and om["bounds_ok"], f"low reserve {om}")
    # class economy with the reserve inside the low band: A uses the band tail, not the atom indicator
    om = outcome_measures(BENCHMARK, "uniform_classes", "0.05", 1.2, 1.0, 0.25, 0.25)
    require(abs(om["A"] - (0.5 * 0.25 + 0.5 * 0.25 * 0.5)) < 1e-15 and om["S_identity_error"] < 1e-12, f"band tail {om}")
    # high-value ownership from the allocation event: with h < p it is zero even if e_H > 0
    om = outcome_measures(BENCHMARK, "binary", "0", 1.2, 10.5, 0.25, 0.25)
    require(om["O_H"] == 0.0 and om["A"] == 0.0 and om["S"] == 0.0, f"p > h: {om}")


TESTS = [test_auction_full_domain_regimes, test_T18_price_pool_family_all_members_validate, test_T18_global_bound_is_rational_and_exceeds_targets,
         test_T19_negative_controls, test_T20_identity_same_orders_different_pools_distinct_and_duplicates_merge,
         test_T21_exact_floor_event_classified_algebraically, test_T22_exact_ceiling_event_plateau_enters, test_T23_outcome_measures]


if __name__ == "__main__":
    failures = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception:
            failures += 1
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    print(f"\n{len(TESTS) - failures}/{len(TESTS)} passed")
    sys.exit(1 if failures else 0)
