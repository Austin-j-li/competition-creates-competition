"""C.6b: identical orders, distinct rational price pools (peer-circulation spec section 8; tests T18, T19, T20).

Family: benchmark primitives with reserve p = 7 at strength r = 1.2 (t_0 = t_L = g_L = 0, t_H = 7, g_H = 3),
full orders (1, -1), lower-tail zero-entry pool {x < c} with cutoffs c_j = -log 2 (1 - j/16), j = 0..16.
At price zero nobody prepares; at every positive price the low-cost type prepares and the high-cost type
does not. Each member is a complete continuation and is validated as such: pooled posterior from the full
preimage (OA.70), buyer optimality at the pooled posterior, pointwise conditional pricing on both regions,
no price collision, every unilateral investor deviation on [-1, 1], and the exact-rational global bound
J_c >= rho p m / 2 > 7/32, U'_theta(s) >= (1 - 1/b) J_c - k > 143/1600 (the proof; the mesh scan checks it).

Negative controls are stored as expected failures, never as accepted rows.
"""
from __future__ import annotations

import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import payoffs_closed_form, payoffs_integrated  # noqa: E402
from numerics.continuations import (INFO_FEEDBACK_STATE, INSTITUTION_RESERVE_AUCTION, NA, TIE_RULE, Continuation,  # noqa: E402
                                    PooledSchedule, PriceInformation, PricingRule, PreparationRule, ValidationEvidence,
                                    continuation_identity, deduplicate, economically_equivalent, laplace_cdf_mp,
                                    laplace_survival_mp, make_pooled_schedule, orders_only_key, parameter_set_id,
                                    payoffs_exact, validate_pooled_schedule)
from numerics.information import OrderProfile  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.params import BENCHMARK, CONTROLS  # noqa: E402

PRIM = BENCHMARK.with_(p="7", parameter_set="price_pool_regression")
R_STR = "1.2"
DPS = 50
LANDMARKS = {  # spec 8.6, 10 decimals
    "c=-log2": {"pool_posterior": "0.2729788130", "preparation": "0.1518051214", "sale": "0.0981948786", "revenue": "0.6873641502"},
    "c=0": {"pool_posterior": "0.3032653299", "preparation": "0.1250000000", "sale": "0.0870918338", "revenue": "0.6096428364"},
}
LANDMARK_TOL = 1e-10
RUN_ID = "c6b"

COLUMNS = ["h", "ell", "p", "rho", "c_L", "c_H", "b", "k", "r", "noise", "cost", "prior_H", "q_H", "q_L", "t_0", "t_H", "t_L", "g_H", "g_L",
           "cutoff_exact", "cutoff_decimal", "pool_probability", "state_H_pool_mass", "state_L_pool_mass", "pool_posterior",
           "buyer_slack_zero_price_c_L", "buyer_slack_zero_price_c_H", "buyer_slack_positive_price_c_L_min", "buyer_slack_positive_price_c_H_min",
           "global_bound_J_lower_rational", "global_bound_Uprime_lower_rational", "J_numeric", "min_dU_mesh",
           "preparation_probability", "sale_probability", "admissible_challenger_probability", "two_admissible_bidders_probability",
           "high_value_ownership_probability", "seller_revenue", "mean_financial_price", "closed_form_vs_integration_error",
           "pricing_error", "entry_deviation_gain", "investor_deviation_gain_estimate", "investor_deviation_gain_upper_bound",
           "validation_status", "accepted", "expected_failure_reason", "candidate_id", "continuation_id", "run_id"]


class RegressionError(Exception):
    """A required regression assertion failed (fail-fast; spec 3.3)."""


def cutoff_family() -> list[tuple[str, object]]:
    with mp.workdps(DPS):
        return [(f"-log2*(1-{j}/16)", -mp.log(2) * (1 - mp.mpf(j) / 16)) for j in range(17)]


def closed_forms(cutoff_mp) -> dict:
    """Spec 8.6 closed forms in 50-digit arithmetic (CDF F_Z and survival S_Z = 1 - F_Z kept distinct)."""
    with mp.workdps(DPS):
        b, rho, p = mp.mpf(PRIM.b), mp.mpf(PRIM.rho), mp.mpf(PRIM.p)
        Fm, Fp = laplace_cdf_mp(cutoff_mp - 1, b), laplace_cdf_mp(cutoff_mp + 1, b)
        Sm, Sp = laplace_survival_mp(cutoff_mp - 1, b), laplace_survival_mp(cutoff_mp + 1, b)
        return {"Pr_P0": (Fm + Fp) / 2, "pool_posterior": Fm / (Fm + Fp), "E": rho / 2 * (Sm + Sp), "sale": rho / 2 * Sm,
                "revenue": rho * p / 2 * Sm, "two_admissible": mp.mpf(0), "mass_H": Fm, "mass_L": Fp}


def rational_landmarks() -> dict:
    """Exact-rational statement of the spec 8.5 bound at these primitives (independent of any float)."""
    rho, p, b, k = Fraction(1, 4), Fraction(7), Fraction(2), Fraction(1, 50)
    return {"J_lower": rho * p * Fraction(1, 4) / 2, "Uprime_lower": (1 - 1 / b) * (rho * p * Fraction(1, 4) / 2) - k,
            "J_target": Fraction(7, 32), "Uprime_target": Fraction(143, 1600)}


def build(cutoff: float, cutoff_exact: str, prep_zero=(False, False), prep_positive=(True, False), raw_posterior_in_pool=False,
          candidate_tag: str = "closed_form_construction"):
    pay = payoffs_closed_form(PRIM, float(R_STR), PRIM.fp)
    prof = OrderProfile.pure(1.0, -1.0)
    sched = make_pooled_schedule(PRIM, pay, prof, cutoff, prep_zero, prep_positive, raw_posterior_in_pool=raw_posterior_in_pool)
    return sched, pay


def to_continuation(sched: PooledSchedule, pv, cutoff_exact: str, cutoff_mp, candidate_tag: str, status: str, expected_failure: str = "") -> Continuation:
    ps_id = parameter_set_id(PRIM, R_STR, PRIM.p, "binary", "0")
    pricing = PricingRule("lower_cutoff_pool", (("-inf", cutoff_exact),), cutoff_exact, mp.nstr(cutoff_mp, 32),
                          "P(x) = t_0 + rho [w_L + Delta_T mu_X(x)] = (7/4) mu_X(x) on x >= c", ())
    prep = PreparationRule("prescribed_by_observed_price_region",
                           (("zero_price", "c_L", sched.prep_zero[0]), ("zero_price", "c_H", sched.prep_zero[1]),
                            ("positive_price", "c_L", sched.prep_positive[0]), ("positive_price", "c_H", sched.prep_positive[1])))
    if sched.raw_posterior_in_pool:
        prep = PreparationRule("INVALID_raw_posterior_inside_pool", prep.actions)
    info = PriceInformation(pv.atoms, "mu_X recovered from P = (7/4) mu_X on the positive-entry region; pooled posterior on the zero atom", 0.0)
    ident = continuation_identity(ps_id, INSTITUTION_RESERVE_AUCTION, INFO_FEEDBACK_STATE, TIE_RULE, sched.profile, pricing, prep, info, CONTROLS)
    return Continuation(f"{RUN_ID}:{candidate_tag}:c={cutoff_exact}", ident, ps_id, INSTITUTION_RESERVE_AUCTION, INFO_FEEDBACK_STATE, TIE_RULE,
                        sched.profile, pricing, info, prep, pv.outcome, pv.evidence, status,
                        "analytical existence for every member of the declared cutoff family (global rational bound); this node only" if pv.evidence.accepted else "none (rejected)",
                        "not established within the reserve game (the family itself shows non-uniqueness of the price rule at fixed orders)",
                        "declared 17-cutoff family at fixed full orders", "lower-interval cutoff scan at fixed orders (1,-1); not a search over all measurable pools",
                        False, NA, NA, "" if pv.evidence.accepted else "; ".join(pv.evidence.breaches), "", RUN_ID, "full_orders_lower_pool")


def row_from(sched, pay, pv, cutoff_exact: str, cutoff_mp, cont: Continuation, status: str, expected_failure: str, cf_err: float) -> dict:
    o = pv.outcome
    gb = pv.global_bound
    pool = pv.atoms[0] if pv.atoms and pv.atoms[0].kind.endswith("pool") else None
    return {**PRIM.columns(), "r": R_STR, "noise": PRIM.noise.value, "cost": PRIM.cost_law.value, "prior_H": PRIM.fundamental_prior_H,
            "q_H": 1.0, "q_L": -1.0, "t_0": pay.t_0, "t_H": pay.t_H, "t_L": pay.t_L, "g_H": pay.g_H, "g_L": pay.g_L,
            "cutoff_exact": cutoff_exact, "cutoff_decimal": mp.nstr(cutoff_mp, 32),
            "pool_probability": pool.probability if pool else 0.0, "state_H_pool_mass": pool.mass_H if pool else NA,
            "state_L_pool_mass": pool.mass_L if pool else NA, "pool_posterior": pool.posterior if pool else NA,
            "buyer_slack_zero_price_c_L": pv.buyer_slack.get("zero_price_c_L", NA), "buyer_slack_zero_price_c_H": pv.buyer_slack.get("zero_price_c_H", NA),
            "buyer_slack_positive_price_c_L_min": pv.buyer_slack.get("positive_price_c_L_min", NA),
            "buyer_slack_positive_price_c_H_min": pv.buyer_slack.get("positive_price_c_H_min", NA),
            "global_bound_J_lower_rational": str(gb["J_lower_bound"]) if gb.get("available") else NA,
            "global_bound_Uprime_lower_rational": str(gb["Uprime_lower_bound"]) if gb.get("available") else NA,
            "J_numeric": gb.get("J_H", NA), "min_dU_mesh": gb.get("min_dU_mesh", NA),
            "preparation_probability": o.E, "sale_probability": o.S, "admissible_challenger_probability": o.A,
            "two_admissible_bidders_probability": o.C2, "high_value_ownership_probability": o.O_H, "seller_revenue": o.R_T,
            "mean_financial_price": o.mean_price, "closed_form_vs_integration_error": cf_err,
            "pricing_error": pv.evidence.pricing_error, "entry_deviation_gain": pv.evidence.entry_deviation_gain,
            "investor_deviation_gain_estimate": pv.evidence.investor_deviation_gain_estimate,
            "investor_deviation_gain_upper_bound": NA if pv.evidence.investor_deviation_gain_upper_bound is None else pv.evidence.investor_deviation_gain_upper_bound,
            "validation_status": status, "accepted": cont.accepted and not expected_failure, "expected_failure_reason": expected_failure,
            "candidate_id": cont.candidate_id, "continuation_id": cont.continuation_id, "run_id": RUN_ID}


def evaluate_member(cutoff_exact: str, cutoff_mp, candidate_tag: str = "closed_form_construction", **kw) -> tuple[dict, Continuation, object]:
    sched, pay = build(float(cutoff_mp), cutoff_exact, **kw)
    pv = validate_pooled_schedule(sched, CONTROLS, cutoff_exact=cutoff_mp)
    cf = closed_forms(cutoff_mp)
    o = pv.outcome
    cf_err = max(abs(float(cf["E"]) - o.E), abs(float(cf["sale"]) - o.S), abs(float(cf["revenue"]) - o.R_T), abs(float(cf["two_admissible"]) - o.C2),
                 abs(float(cf["Pr_P0"]) - (pv.atoms[0].probability if pv.atoms else 0.0)))
    if pv.atoms and pv.atoms[0].kind.endswith("pool"):
        cf_err = max(cf_err, abs(float(cf["pool_posterior"]) - pv.atoms[0].posterior))
    breaches = list(pv.evidence.breaches)
    if cf_err > CONTROLS.independent_formula_acceptance and not kw.get("raw_posterior_in_pool"):
        breaches.append(f"closed_form_vs_integration={cf_err:.3e}")
        pv = type(pv)(pv.atoms, pv.outcome, ValidationEvidence(**{**pv.evidence.__dict__, "breaches": tuple(breaches)}), pv.buyer_slack, pv.global_bound, pv.closed_forms, pv.scans)
    status = "analytical (global rational bound; buyer, pricing, belief checks passed)" if pv.evidence.accepted else "rejected: " + "; ".join(pv.evidence.breaches)
    cont = to_continuation(sched, pv, cutoff_exact, cutoff_mp, candidate_tag, status)
    return row_from(sched, pay, pv, cutoff_exact, cutoff_mp, cont, status, "", cf_err), cont, pv


def run() -> bool:
    checks: dict = {}
    rows: list[dict] = []
    conts: list[Continuation] = []
    # --- auction objects on the expanded domain (spec 8.1) ------------------------------------------
    ex = payoffs_exact(PRIM, Fraction(Decimal(R_STR)), Fraction(Decimal(PRIM.p)))
    pay_i, _ = payoffs_integrated(PRIM, float(R_STR), PRIM.fp)
    exact_ok = ex["t_0"] == 0 and ex["t_L"] == 0 and ex["g_L"] == 0 and ex["t_H"] == 7 and ex["g_H"] == 3
    int_err = max(abs(float(ex[a]) - getattr(pay_i, a)) for a in ("t_0", "t_H", "t_L", "g_H", "g_L"))
    checks["auction_expanded_domain"] = {"exact": {k_: str(v_) for k_, v_ in ex.items()}, "integration_error": int_err,
                                         "pass": bool(exact_ok and int_err <= CONTROLS.independent_formula_acceptance)}
    if not checks["auction_expanded_domain"]["pass"]:
        raise RegressionError(f"expanded-domain auction objects wrong: {ex}, integration error {int_err:.3e}")
    # --- the family (T18) ---------------------------------------------------------------------------
    fam = cutoff_family()
    member_rows = []
    for tag, c in fam:
        row, cont, pv = evaluate_member(tag, c)
        rows.append(row)
        conts.append(cont)
        member_rows.append(row)
    all_accepted = all(r_["accepted"] for r_ in member_rows)
    checks["family_all_validated"] = {"members": len(member_rows), "rejected": [r_["cutoff_exact"] for r_ in member_rows if not r_["accepted"]], "pass": all_accepted}
    preps = [r_["preparation_probability"] for r_ in member_rows]
    revs = [r_["seller_revenue"] for r_ in member_rows]
    mono = all(a > b_ for a, b_ in zip(preps[:-1], preps[1:])) and all(a > b_ for a, b_ in zip(revs[:-1], revs[1:]))
    checks["monotone_decrease_in_cutoff"] = {"preparation": preps, "revenue": revs, "pass": mono}
    # rational bound (proof) at the spec landmarks
    rl = rational_landmarks()
    gb0 = validate_pooled_schedule(build(float(fam[0][1]), fam[0][0])[0], CONTROLS, cutoff_exact=fam[0][1]).global_bound
    bound_ok = gb0["available"] and gb0["J_lower_bound"] >= rl["J_target"] and gb0["Uprime_lower_bound"] >= rl["Uprime_target"] and gb0["positive"]
    checks["global_rational_bound"] = {"J_lower_bound": str(gb0.get("J_lower_bound")), "J_target": "7/32", "Uprime_lower_bound": str(gb0.get("Uprime_lower_bound")),
                                       "Uprime_target": "143/1600", "min_dU_mesh_over_family": min(r_["min_dU_mesh"] for r_ in member_rows),
                                       "role": "the rational bound is the proof; the mesh derivative scan is an implementation check", "pass": bool(bound_ok)}
    # landmarks at both endpoints (closed form and integration, 10 decimals)
    land = {}
    for key, tag in (("c=-log2", fam[0][0]), ("c=0", fam[16][0])):
        r_ = next(x for x in member_rows if x["cutoff_exact"] == tag)
        cfm = closed_forms(fam[0][1] if key == "c=-log2" else fam[16][1])
        got = {"pool_posterior": r_["pool_posterior"], "preparation": r_["preparation_probability"], "sale": r_["sale_probability"], "revenue": r_["seller_revenue"]}
        cfv = {"pool_posterior": float(cfm["pool_posterior"]), "preparation": float(cfm["E"]), "sale": float(cfm["sale"]), "revenue": float(cfm["revenue"])}
        errs = {k_: max(abs(got[k_] - float(LANDMARKS[key][k_])), abs(cfv[k_] - float(LANDMARKS[key][k_]))) for k_ in got}
        land[key] = {"integration": got, "closed_form": cfv, "landmark": LANDMARKS[key], "max_error": max(errs.values()), "pass": max(errs.values()) <= LANDMARK_TOL}
    checks["endpoint_landmarks"] = {**land, "pass": all(v["pass"] for v in land.values())}
    # --- identity (T20): endpoints distinct; repeated construction of one endpoint merges --------------
    c0, c16 = conts[0], conts[16]
    row_dup, cont_dup, _ = evaluate_member(fam[0][0], fam[0][1], candidate_tag="second_start_same_outcome")
    reps, absorbed = deduplicate([c0, c16, cont_dup], CONTROLS)
    dedupe_ok = (len(reps) == 2 and not economically_equivalent(c0, c16, CONTROLS) and economically_equivalent(c0, cont_dup, CONTROLS)
                 and c0.candidate_id != cont_dup.candidate_id and c0.continuation_id == cont_dup.continuation_id)
    orders_key_merges = orders_only_key(c0) == orders_only_key(c16)
    checks["continuation_identity"] = {"endpoints_distinct": not economically_equivalent(c0, c16, CONTROLS), "orders_only_key_would_merge_endpoints": orders_key_merges,
                                       "repeat_start_merged": economically_equivalent(c0, cont_dup, CONTROLS), "representatives": len(reps),
                                       "absorbed": absorbed, "pass": bool(dedupe_ok and orders_key_merges)}
    rows.append({**row_dup, "validation_status": row_dup["validation_status"] + " [duplicate start: merged into " + c0.candidate_id + "]", "accepted": False,
                 "expected_failure_reason": "not a failure: repeated construction of the same continuation; recorded in the ledger, merged by identity"})
    # --- negative controls (T19), stored as expected failures ----------------------------------------
    neg = []
    with mp.workdps(DPS):
        for tag, c, why, must_contain in (("-1", mp.mpf(-1), "positive prices with 3 mu_X < 1: prescribed low-cost preparation not optimal", "buyer_deviation_at_positive_price_c_L"),
                                          ("1", mp.mpf(1), "pooled zero-price posterior makes low-cost preparation profitable: prescribed nonpreparation fails", "buyer_deviation_at_zero_price_c_L")):
            row, cont, pv = evaluate_member(tag, c, candidate_tag="negative_control")
            failed_right = (not cont.accepted) and any(must_contain in b_ for b_ in pv.evidence.breaches)
            neg.append({"cutoff": tag, "expected": why, "breaches": list(pv.evidence.breaches), "pass": failed_right})
            rows.append({**row, "accepted": False, "expected_failure_reason": why if failed_right else "CONTROL DID NOT FAIL AS REQUIRED"})
    row, cont, pv = evaluate_member(fam[16][0], fam[16][1], candidate_tag="negative_control_raw_posterior_in_pool", raw_posterior_in_pool=True)
    failed_right = (not cont.accepted) and any("preparation_not_price_measurable" in b_ for b_ in pv.evidence.breaches)
    neg.append({"cutoff": "0 (raw posterior inside pool)", "expected": "policy inconsistent with the observed-price information structure", "breaches": list(pv.evidence.breaches), "pass": failed_right})
    rows.append({**row, "accepted": False, "expected_failure_reason": "buyer acts on raw mu_X inside the zero-price atom: inconsistent with observed-price information" if failed_right else "CONTROL DID NOT FAIL AS REQUIRED"})
    checks["negative_controls"] = {"controls": neg, "orders_only_dedupe_control": "see continuation_identity.orders_only_key_would_merge_endpoints", "pass": all(n["pass"] for n in neg)}
    if not checks["negative_controls"]["pass"]:
        raise RegressionError(f"a negative control did not fail as required: {neg}")

    write_csv("numerics/price_pool_regression.csv", COLUMNS, rows)
    passed = all(c.get("pass", True) for c in checks.values())
    write_manifest("c6b_price_pools", {"primitives": PRIM.__dict__, "r": R_STR, "orders": [1, -1], "cutoff_family": "c_j = -log2 (1 - j/16), j = 0..16",
                                       "preparation_rule": "zero price: none; positive price: low cost prepares, high cost does not",
                                       "negative_controls": ["c=-1", "c=1", "raw posterior inside c=0 pool", "orders-only deduplication key"],
                                       "landmarks": LANDMARKS, "landmark_tolerance": LANDMARK_TOL},
                   "Complete pooled continuations validated pointwise: OA.70 pooled posterior by 50-digit closed form and by segment-wise "
                   "Gauss-Legendre integration; buyer optimality at the pooled posterior and pointwise on positive prices; conditional pricing on "
                   "both regions; collision and monotonicity of the positive-entry price; investor deviations on the declared and refined order grids "
                   "over [-1, 1] for both signs and types; exact-rational global derivative bound as the proof with a 200-point mesh as implementation check.",
                   CONTROLS.as_dict(), ["numerics/price_pool_regression.csv"], checks, passed,
                   ["The 17-cutoff scan is not an exhaustive search over measurable pools (exhaustive_pricing_search = false).",
                    "Negative controls appear in the CSV with accepted = false and an expected_failure_reason; they are not accepted rows."])
    print("C.6b passed" if passed else "C.6b FAILED", {k_: v_.get("pass") for k_, v_ in checks.items()})
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
