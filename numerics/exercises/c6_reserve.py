"""C.6: reserve comparisons and the exploratory seller continuation sweep."""
from __future__ import annotations

import sys
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import (payoffs_class_closed_form, payoffs_class_formula_OA52, payoffs_class_integrated,  # noqa: E402
                              payoffs_closed_form, payoffs_integrated)
from numerics.information import OrderProfile, entry_at_posterior, make_schedule  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.noise import posterior_bounds  # noqa: E402
from numerics.params import BENCHMARK, BENCHMARK_EXTRA, BENCHMARK_STRENGTHS, CONTROLS, decimal_range  # noqa: E402
from numerics.search import (Candidate, asymmetric_candidate, asymmetric_roots, full_order_candidate, mixed_support_search,  # noqa: E402
                             pooling_candidate, pure_fixed_points)
from numerics.validation import validate  # noqa: E402

PRIM = BENCHMARK
EPS_V = float(BENCHMARK_EXTRA["value_band_halfwidth"])
TOL = CONTROLS.independent_formula_acceptance
STRENGTHS = {k: v for k, v in BENCHMARK_STRENGTHS.items() if k != "r_collapse"}
DECLARED = {"binary": ["0.5", BENCHMARK_EXTRA["binary_alternative_reserve"]],
            "uniform_classes": ["0.5", BENCHMARK_EXTRA["atomless_alternative_reserve"]]}
CONT_COLS = ["value_law", "r", "p", "branch", "q_H", "q_L", "E", "O_H", "R_T", "no_entry_price_mass", "posterior_in_no_entry_pool",
             "epsilon_P", "epsilon_e", "epsilon_q", "status", "accepted", "unresolved_reason"]


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


def _row(law, rs, ps, branch, cand, val, existence, reason=""):
    o = val.outcome
    return {"value_law": law, "r": rs, "p": ps, "branch": branch,
            "q_H": cand.profile.q_H[0] if cand.profile.is_pure else "mixed", "q_L": cand.profile.q_L[0] if cand.profile.is_pure else "mixed",
            "E": o.E, "O_H": o.O_H, "R_T": o.R_T, "no_entry_price_mass": val.no_entry_price_mass,
            "posterior_in_no_entry_pool": val.posterior_in_no_entry_pool, "epsilon_P": val.epsilon_P, "epsilon_e": val.epsilon_e,
            "epsilon_q": max(val.epsilon_q, val.epsilon_q_refined), "status": existence, "accepted": val.accepted,
            "unresolved_reason": reason or ("" if val.accepted else "; ".join(val.breaches))}


def solve_reserve(args) -> tuple[list[dict], dict, dict]:
    law, rs, ps = args
    r, p = float(rs), float(ps)
    pay, oracle_err = payoffs(law, r, p)
    ab = analytic_bounds(pay)
    rows, diag = [], {"law": law, "r": rs, "p": ps, "payoff_oracle_error": oracle_err, **ab}
    unresolved = False
    m, M = posterior_bounds(PRIM.fb)
    e_M = float(entry_at_posterior(PRIM, pay, np.array([M]))[0])
    degenerate = pay.Delta_T <= 0 or pay.g_H <= 0 or e_M <= 0
    # pooling / constant-price candidate (always analysed directly)
    cand = pooling_candidate(PRIM, pay)
    val = validate(cand.sched, CONTROLS, price_pools=True)
    ex = ("analytical (unique no trade: Delta_T < k)" if val.accepted and ab["no_trade_unique_margin"] > 0 else
          "analytical (pooling exists: e0 Delta_T/2 <= k)" if val.accepted and ab["pooling_exists_margin"] >= 0 else
          "numerical diagnostic" if val.accepted else "rejected")
    rows.append(_row(law, rs, ps, "pooling", cand, val, ex))
    if degenerate:
        diag["skipped_searches"] = ("all entry impossible (H_C(B_r(M)) = 0): constant-price candidate only" if e_M <= 0 else
                                    "degenerate payoff (Delta_T <= 0 or g_H <= 0): constant-price candidate only")
    elif ab["no_trade_unique_margin"] > 0:
        diag["skipped_searches"] = "Delta_T < k excludes every nonzero order against any candidate schedule"
    else:
        cand = full_order_candidate(PRIM, pay)
        val = validate(cand.sched, CONTROLS, price_pools=True)
        if val.accepted:
            ex = ("analytical (unique full orders: uniform derivative bound with entry floor)" if ab["full_unique_margin"] > 0 and ab["low_cost_floor_margin"] > 0
                  else "analytical (candidate J test)" if ab["low_cost_floor_margin"] > 0 and cand.diagnostics["J_margin"] > 0 else "numerical diagnostic")
        else:
            ex = "rejected"
        rows.append(_row(law, rs, ps, "full_orders", cand, val, ex))
        if ab["full_unique_margin"] > 0 and ab["low_cost_floor_margin"] > 0:
            diag["skipped_searches"] = "uniform full-order bound with positive entry floor excludes every other candidate"
        else:
            # asymmetric roots
            ar = asymmetric_roots(PRIM, pay)
            for v in ar["roots"]:
                cand = asymmetric_candidate(PRIM, pay, v)
                val = validate(cand.sched, CONTROLS, price_pools=True)
                if abs(cand.diagnostics["Psi"]) > 1e-6:
                    rows.append(_row(law, rs, ps, "asymmetric_discontinuity", cand, val, "rejected", "Psi sign change without root at a region boundary"))
                    continue
                rows.append(_row(law, rs, ps, "asymmetric", cand, val, "numerical diagnostic" if val.accepted else "rejected"))
            for v, resid in ar["tangencies"]:
                cand = asymmetric_candidate(PRIM, pay, v)
                val = validate(cand.sched, CONTROLS, price_pools=True)
                rows.append(_row(law, rs, ps, "asymmetric_tangency", cand, val, "open" if not val.accepted else "numerical diagnostic",
                                 f"local |Psi| minimum {resid:.3e} without sign change"))
                unresolved = unresolved or not val.accepted
            accepted = [(float(x["q_H"]), -float(x["q_L"])) for x in rows if x["accepted"] is True and x["q_H"] != "mixed"]
            fp = pure_fixed_points(PRIM, pay, inits=[(u, v) for u in (0.2, 0.6, 0.95) for v in (0.2, 0.6, 0.95)], max_iter=40)
            for u, v, init in fp["fixed_points"]:
                if any(abs(u - au) < 1e-5 and abs(v - av) < 1e-5 for au, av in accepted):
                    continue
                sched = make_schedule(PRIM, pay, OrderProfile.pure(u, -v))
                cand = Candidate("pure", sched.profile, sched, {"init": init})
                val = validate(sched, CONTROLS, price_pools=True)
                rows.append(_row(law, rs, ps, "pure", cand, val, "numerical diagnostic" if val.accepted else "rejected"))
            if fp["unconverged"]:
                unresolved = True
                diag["pure_unconverged"] = len(fp["unconverged"])
            ms = mixed_support_search(PRIM, pay, mesh=0.05, iters=150)
            prof = ms["profile"]
            if ms["converged"] and len(prof.q_H) > 1:
                val = validate(ms["sched"], CONTROLS, price_pools=True)
                cand = Candidate("mixed", prof, ms["sched"], {})
                rows.append(_row(law, rs, ps, "mixed", cand, val, "numerical diagnostic" if val.accepted else "rejected"))
            elif not ms["converged"]:
                unresolved = True
                diag["mixed_search"] = f"not converged (support gap {ms['support_gap']:.2e})"
    acc = [x for x in rows if x["accepted"] is True]
    rng = {"value_law": law, "r": rs, "p": ps, "accepted_continuations_found": len(acc),
           "E_min_found": min(x["E"] for x in acc) if acc else "n/a", "E_max_found": max(x["E"] for x in acc) if acc else "n/a",
           "R_T_min_found": min(x["R_T"] for x in acc) if acc else "n/a", "R_T_max_found": max(x["R_T"] for x in acc) if acc else "n/a",
           "search_unresolved": unresolved or not acc, "global_envelope_certified": False}
    diag["unresolved"] = unresolved
    return rows, rng, diag


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


def run(workers: int | None = None, quick: bool = False, max_refine_nodes: int | None = None) -> bool:
    import os
    workers = workers or max(1, (os.cpu_count() or 8) - 2)
    checks, notes = {}, []
    tasks = []
    for law in ("binary", "uniform_classes"):
        grid = reserve_grid(law)
        if quick:
            grid = [g for g in grid if Decimal(g) % Decimal("0.5") == 0 or g in DECLARED[law]]
        for rs in STRENGTHS.values():
            tasks += [(law, rs, ps) for ps in grid]
    cont, ranges, diags = [], [], []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for rows, rng, dg in ex.map(solve_reserve, tasks, chunksize=1):
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
    for law, rs, pa, pb, why in intervals:
        x = Decimal(pa) + Decimal("0.002")
        while x < Decimal(pb):
            refine.add((law, rs, str(x)))
            x += Decimal("0.002")
    refine = sorted(refine, key=lambda t: (t[0], Decimal(t[1]), Decimal(t[2])))
    skipped = 0
    if max_refine_nodes is not None and len(refine) > max_refine_nodes:
        skipped = len(refine) - max_refine_nodes
        # keep refinement for revenue maxima and branch changes first, in listed order
        refine = refine[:max_refine_nodes]
    if refine and not quick:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for rows, rng, dg in ex.map(solve_reserve, refine, chunksize=1):
                cont += rows
                ranges.append(rng)
                diags.append(dg)
    cont.sort(key=lambda x: (x["value_law"], Decimal(x["r"]), Decimal(x["p"]), x["branch"]))
    ranges.sort(key=lambda x: (x["value_law"], Decimal(x["r"]), Decimal(x["p"])))
    write_csv("numerics/reserve_continuations.csv", CONT_COLS, cont)
    write_csv("numerics/reserve_ranges.csv", ["value_law", "r", "p", "accepted_continuations_found", "E_min_found", "E_max_found",
                                              "R_T_min_found", "R_T_max_found", "search_unresolved", "global_envelope_certified"], ranges)
    # --- declared comparisons table ------------------------------------------------------------
    comp_rows = []
    for law in ("binary", "uniform_classes"):
        for rs in STRENGTHS.values():
            for ps in DECLARED[law]:
                pay, oracle_err = payoffs(law, float(rs), float(ps))
                ab = analytic_bounds(pay)
                acc = [x for x in cont if x["value_law"] == law and x["r"] == rs and x["p"] == ps and x["accepted"] is True]
                for x in acc:
                    if x["branch"] == "pooling":
                        margin = ab["no_trade_unique_margin"]
                        status = "analytical (unique no trade: k - Delta_T > 0)" if margin > 0 else "numerical diagnostic (pooling validated; uniqueness not established)"
                    elif x["branch"] == "full_orders":
                        margin = ab["full_unique_margin"]
                        status = ("analytical (unique full orders: (1-1/b) e(m) m Delta_T - k > 0 with positive floor)"
                                  if margin > 0 and ab["low_cost_floor_margin"] > 0 else "numerical diagnostic (full orders validated; uniqueness not established)")
                    else:
                        margin, status = float("nan"), "numerical diagnostic (additional continuation found)"
                    sched_rows = [y for y in cont if y is x]
                    eH, eL = 2 * x["O_H"], 2 * x["E"] - 2 * x["O_H"]
                    comp_rows.append({"value_law": law, "signal_information": "class only" if law == "uniform_classes" else "exact value",
                                      "epsilon_V": BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0", "r": rs, "p": ps,
                                      "t_0": pay.t_0, "t_H": pay.t_H, "t_L": pay.t_L, "g_H": pay.g_H, "g_L": pay.g_L, "Delta_T": pay.Delta_T,
                                      "q_H": x["q_H"], "q_L": x["q_L"], "e_H": eH, "e_L": eL, "E": x["E"], "R_T": x["R_T"],
                                      "low_cost_floor_margin": ab["low_cost_floor_margin"], "trading_margin": margin, "payoff_oracle_error": oracle_err,
                                      "status": status, "accepted": oracle_err <= TOL and len(acc) == 1})
                checks[f"declared_{law}_r{rs}_p{ps}"] = {"accepted_continuations": len(acc), "payoff_oracle_error": oracle_err,
                                                         "pass": len(acc) == 1 and oracle_err <= TOL}
    write_csv("tables/reserve_comparisons.csv", ["value_law", "signal_information", "epsilon_V", "r", "p", "t_0", "t_H", "t_L", "g_H", "g_L", "Delta_T",
                                                 "q_H", "q_L", "e_H", "e_L", "E", "R_T", "low_cost_floor_margin", "trading_margin", "payoff_oracle_error",
                                                 "status", "accepted"], comp_rows)
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
    checks["sweep"] = {"nodes": len(tasks), "refined_nodes": len(refine), "refinement_intervals": intervals, "refinement_skipped_nodes": skipped,
                       "unresolved_nodes": sum(1 for r_ in ranges if r_["search_unresolved"]),
                       "nodes_without_accepted_continuation": sum(1 for r_ in ranges if r_["accepted_continuations_found"] == 0),
                       "refinement_rule": "intervals with a change in the accepted branch set, an unresolved endpoint, or the found revenue maximum are refined to 0.002"}
    passed = all(c.get("pass", True) for c in checks.values())
    write_manifest("c6_reserve", {"benchmark": PRIM.__dict__, "epsilon_V": BENCHMARK_EXTRA["value_band_halfwidth"], "declared": DECLARED,
                                  "strengths": STRENGTHS, "grid": "0..h (+eps_V for classes) by 0.05 plus band edges, r, declared reserves, offsets 0.0001", "quick": quick},
                   "Payoff oracle: direct integration of OA.50 over R (and over class bands) versus OA.51/OA.52; continuation candidates "
                   "(pooling, full, asymmetric, pure, mixed) validated with price-pool handling (OA.70) at every reserve; analytical uniqueness "
                   "bounds (Delta_T < k; uniform derivative bound with positive floor) recorded and used to skip exploratory searches only where they hold.",
                   CONTROLS.as_dict(), ["tables/reserve_comparisons.csv", "numerics/reserve_continuations.csv", "numerics/reserve_ranges.csv"], checks, passed, notes)
    print("C.6 passed" if passed else "C.6 FAILED", {k: v for k, v in checks.items() if k.startswith(("declared", "revenue", "payoff", "sweep"))})
    return passed


if __name__ == "__main__":
    w = next((int(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--workers=")), None)
    sys.exit(0 if run(workers=w, quick="--quick" in sys.argv) else 1)
