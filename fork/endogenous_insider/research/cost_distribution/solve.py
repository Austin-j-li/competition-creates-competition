"""Solver for the cost-distribution track. Writes CSV only; the renderer never solves.

Outputs (all in this folder):
  laws.csv               declared cost laws
  regime_map.csv         regime of each law across incumbent strengths, with the mass thresholds
  laws_r3.csv            full-order outcomes at r = 3 for every declared law, plus grid checks
  eps_r3.csv             uniform cost noise of half-width eps around c = 6 at r = 3
  floor_rho.csv          the benchmark floor rho -> 0 at r = 3
  lowest_cost_r3.csv     which pools survive a vanishing two-point perturbation, by its lowest cost
  family_r3.csv          grid cutoff families at r = 3 for three laws
  branches.csv           grid live branches across strengths, with the analytical no-trade rows

Status: every grid row is a numerical diagnostic. Rows computed from the closed forms of the note by
quadrature are numerical diagnostics as well; certify.py encloses the r = 3 existence statistics.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from core import (CostLaw, Primitives, M_bound, belief_for_profit, ceiling_strength, cost_cdf, entry_at_belief,
                  flow_for_belief, forced_pool_end, frak_r, full_order_outcome, full_orders_unique_sufficient,
                  gross_profit, half_line_pool_belief, largest_consistent_cutoff, lowest_cost, m_bound,
                  mass_needed_no_trade_removed, mass_needed_unique_full, mu_full, no_trade_exists, payoffs, regime,
                  sufficient_cutoff_end)
from grid import Grid, iterate, make_grid

HERE = Path(__file__).resolve().parent
PRIM = Primitives()
R1 = 3.0
C = 6.0

LAWS: tuple[CostLaw, ...] = (
    CostLaw("fork_point_6", atoms=((6.0, 1.0),)),
    CostLaw("noise_eps_0.1", uniforms=((5.9, 6.1, 1.0),)),
    CostLaw("noise_eps_0.5", uniforms=((5.5, 6.5, 1.0),)),
    CostLaw("uniform_3_9", uniforms=((3.0, 9.0, 1.0),)),
    CostLaw("uniform_0_12", uniforms=((0.0, 12.0, 1.0),)),
    CostLaw("benchmark_two_point", atoms=((1.0, 0.25), (6.0, 0.75))),
)

STARTS = ((1.0, -1.0), (1.0, -0.5), (1.0, 0.0), (0.5, -0.5), (0.25, -0.25))


def fmt(v: object) -> object:
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (float, np.floating)):
        return f"{float(v):.10g}"
    return v


def write_csv(path: Path, rows: list[dict]) -> None:
    keys: list[str] = []
    for row in rows:
        for k in row:
            if k not in keys:
                keys.append(k)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: fmt(row.get(k, "")) for k in keys})


def law_mean(law: CostLaw) -> float:
    return sum(loc * m for loc, m in law.atoms) + sum(0.5 * (lo + hi) * m for lo, hi, m in law.uniforms)


def laws_table() -> list[dict]:
    rows = []
    for law in LAWS:
        c0, atom = lowest_cost(PRIM, law)
        rows.append({"law": law.label, "atoms": ";".join(f"{a}@{m}" for a, m in law.atoms),
                     "uniforms": ";".join(f"U[{lo},{hi}]@{m}" for lo, hi, m in law.uniforms),
                     "mean_cost": law_mean(law), "lowest_cost_c0": c0, "atom_at_c0": atom, "status": "input"})
    return rows


def regime_rows() -> list[dict]:
    rows = []
    m, M = m_bound(PRIM), M_bound(PRIM)
    for r in np.round(np.arange(1.02, 4.001, 0.01), 4):
        pay = payoffs(PRIM, float(r))
        base = {"r": float(r), "B_m": gross_profit(PRIM, pay, m), "B_half": gross_profit(PRIM, pay, 0.5),
                "B_M": gross_profit(PRIM, pay, M), "DeltaT": pay.DeltaT,
                "mass_kill_no_trade": mass_needed_no_trade_removed(PRIM, pay),
                "mass_unique_full": mass_needed_unique_full(PRIM, pay)}
        for law in LAWS:
            o = full_order_outcome(PRIM, pay, law)
            rows.append({**base, "law": law.label, "regime": regime(PRIM, pay, law),
                         "G_at_B_m": entry_at_belief(PRIM, pay, law, m),
                         "G_at_B_half": entry_at_belief(PRIM, pay, law, 0.5),
                         "G_at_B_M": entry_at_belief(PRIM, pay, law, M),
                         "dead_exists": entry_at_belief(PRIM, pay, law, 0.5) == 0.0,
                         "no_trade_exists": no_trade_exists(PRIM, pay, law),
                         "no_trade_entry": entry_at_belief(PRIM, pay, law, 0.5),
                         "unique_full_sufficient": full_orders_unique_sufficient(PRIM, pay, law),
                         "full_min_pool_J": o.J, "full_min_pool_test": o.sufficient_test,
                         "full_min_pool_E": o.E, "full_min_pool_pool_prob": o.pool_prob,
                         "status": "analytical classification; J and E by quadrature (numerical diagnostic)"})
    return rows


def grid_starts(grid: Grid, r: float, law: CostLaw) -> tuple[list, int, int]:
    found, n_live, n_dead = [], 0, 0
    for qH0, qL0 in STARTS:
        fp = iterate(PRIM, grid, r, law, qH0, qL0)
        if fp is None:
            continue
        if fp.E > 0.0 and (abs(fp.qH) > 0 or abs(fp.qL) > 0):
            n_live += 1
            if not any(abs(fp.qH - g.qH) < 0.015 and abs(fp.qL - g.qL) < 0.015 for g in found):
                found.append(fp)
        elif fp.qH == 0.0 and fp.qL == 0.0:
            n_dead += 1
    return found, n_live, n_dead


def laws_r3_rows(grid: Grid) -> list[dict]:
    pay = payoffs(PRIM, R1)
    m = m_bound(PRIM)
    rows = []
    for law in LAWS:
        o = full_order_outcome(PRIM, pay, law)
        found, n_live, n_zero = grid_starts(grid, R1, law)
        full = [fp for fp in found if abs(fp.qH - 1.0) < 1e-3 and abs(fp.qL + 1.0) < 1e-3]
        g_half = entry_at_belief(PRIM, pay, law, 0.5)
        rows.append({"law": law.label, "r": R1, "regime": regime(PRIM, pay, law),
                     "G_at_B_m": entry_at_belief(PRIM, pay, law, m), "G_at_B_half": g_half,
                     "G_at_B_M": entry_at_belief(PRIM, pay, law, M_bound(PRIM)),
                     "dead_exists": g_half == 0.0, "no_trade_exists": no_trade_exists(PRIM, pay, law),
                     "no_trade_materiality": pay.DeltaT * g_half,
                     "unique_full_sufficient": full_orders_unique_sufficient(PRIM, pay, law),
                     "z0": o.z0, "pool_prob": o.pool_prob, "pool_belief": o.pool_belief,
                     "pool_consistent": o.pool_consistent, "J": o.J, "sufficient_test": o.sufficient_test,
                     "E": o.E, "O_H": o.O_H, "U": o.U, "materiality_ex_ante": o.materiality_ex_ante,
                     "materiality_min_price": o.materiality_min_price,
                     "entry_gain_vs_uninformative": o.E - g_half,
                     "largest_consistent_cutoff": largest_consistent_cutoff(PRIM, pay, law),
                     "sufficient_cutoff_end": sufficient_cutoff_end(PRIM, pay, law),
                     "grid_full_E": full[0].E if full else float("nan"),
                     "grid_full_U_H": full[0].U_H if full else float("nan"),
                     "grid_starts_to_live": n_live, "grid_starts_to_zero": n_zero,
                     "grid_live_profiles": ";".join(f"({fp.qH:+.3f},{fp.qL:+.3f})" for fp in found),
                     "status": "closed form by quadrature and grid fixed points: numerical diagnostic"})
    return rows


def uniform_noise_law(eps: float) -> CostLaw:
    if eps == 0.0:
        return CostLaw("fork_point_6", atoms=((C, 1.0),))
    return CostLaw(f"noise_eps_{eps:g}", uniforms=((C - eps, C + eps, 1.0),))


def eps_rows(grid: Grid) -> list[dict]:
    pay = payoffs(PRIM, R1)
    rows = []
    for eps in (0.0, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 1.7):
        law = uniform_noise_law(eps)
        o = full_order_outcome(PRIM, pay, law)
        fp = iterate(PRIM, grid, R1, law, 1.0, -1.0)
        tau_lo = belief_for_profit(PRIM, pay, C - eps)
        tau_hi = belief_for_profit(PRIM, pay, C + eps)
        rows.append({"eps": eps, "r": R1, "regime": regime(PRIM, pay, law), "tau_minus": tau_lo, "tau_plus": tau_hi,
                     "x_minus": flow_for_belief(PRIM, tau_lo),
                     "x_plus": flow_for_belief(PRIM, min(tau_hi, M_bound(PRIM))),
                     "dead_exists": entry_at_belief(PRIM, pay, law, 0.5) == 0.0,
                     "z0": o.z0, "pool_prob": o.pool_prob, "pool_belief": o.pool_belief, "J": o.J,
                     "sufficient_test": o.sufficient_test, "E": o.E, "O_H": o.O_H, "U": o.U,
                     "largest_consistent_cutoff": largest_consistent_cutoff(PRIM, pay, law),
                     "sufficient_cutoff_end": sufficient_cutoff_end(PRIM, pay, law),
                     "ceiling_strength": ceiling_strength(PRIM, C - eps),
                     "grid_full_fixed_point": fp is not None and abs(fp.qH - 1) < 1e-3 and abs(fp.qL + 1) < 1e-3,
                     "grid_E": fp.E if fp else float("nan"),
                     "status": "numerical diagnostic"})
    return rows


def floor_rows() -> list[dict]:
    pay = payoffs(PRIM, R1)
    tau = belief_for_profit(PRIM, pay, C)
    fork = full_order_outcome(PRIM, pay, CostLaw("fork", atoms=((C, 1.0),)))
    rows = []
    for rho in (0.25, 0.1, 0.06, 0.05, 0.02, 0.01, 0.001, 0.0):
        law = (CostLaw(f"floor_rho_{rho:g}", atoms=((1.0, rho), (C, 1.0 - rho))) if rho > 0
               else CostLaw("fork", atoms=((C, 1.0),)))
        o = full_order_outcome(PRIM, pay, law)
        m = m_bound(PRIM)
        r_N = frak_r(PRIM, 2 * PRIM.k / rho) if rho > 0 else math.inf
        r_U = frak_r(PRIM, PRIM.k / ((1 - 1 / PRIM.b) * rho * m)) if rho > 0 else math.inf
        rows.append({"rho": rho, "r": R1, "regime": regime(PRIM, pay, law), "G_at_B_half": rho,
                     "no_trade_exists": no_trade_exists(PRIM, pay, law), "r_N": r_N, "r_U": r_U,
                     "unique_full_sufficient": full_orders_unique_sufficient(PRIM, pay, law),
                     "J": o.J, "E": o.E, "O_H": o.O_H, "U": o.U, "pool_prob": o.pool_prob,
                     "E_minus_fork_E": o.E - fork.E,
                     "sup_price_gap_to_fork": rho * (pay.wL + pay.DeltaT * tau),
                     "status": "analytical bounds; J and E by quadrature (numerical diagnostic)"})
    return rows


def lowest_cost_rows() -> list[dict]:
    pay = payoffs(PRIM, R1)
    m = m_bound(PRIM)
    fork = CostLaw("fork", atoms=((C, 1.0),))
    fork_out = full_order_outcome(PRIM, pay, fork)
    x_star = fork_out.z0
    fork_suff_end = sufficient_cutoff_end(PRIM, pay, fork)
    B_pool_min = gross_profit(PRIM, pay, fork_out.pool_belief)
    eta = 0.05
    specials = [gross_profit(PRIM, pay, m), B_pool_min, gross_profit(PRIM, pay, 0.5)]
    rows = []
    for c_low in sorted({1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.2, 4.5, 5.0, *specials}):
        law = CostLaw(f"two_point_{c_low:g}", atoms=((c_low, eta), (C, 1.0 - eta)))
        mu_low = belief_for_profit(PRIM, pay, c_low)
        xbar = largest_consistent_cutoff(PRIM, pay, law)
        if xbar == -math.inf:
            label, hi = "minimal pool only (no pool for eta > 0)", x_star
        elif xbar <= x_star:
            label, hi = "minimal pool only", x_star
        elif xbar == math.inf:
            label, hi = "whole family", fork_suff_end
        else:
            label, hi = "truncated family", min(xbar, fork_suff_end)
        rows.append({"c_low": c_low, "eta": eta, "r": R1, "mu_low": mu_low, "regime": regime(PRIM, pay, law),
                     "forced_pool_end": forced_pool_end(PRIM, pay, law), "largest_consistent_cutoff": xbar,
                     "fork_x_star": x_star, "fork_min_pool_belief": fork_out.pool_belief,
                     "fork_sufficient_cutoff_end": fork_suff_end, "limit_cutoffs_low": x_star,
                     "limit_cutoffs_high_sufficient": hi, "selection": label,
                     "no_trade_exists": no_trade_exists(PRIM, pay, law),
                     "status": "analytical classification; cutoffs by root finding (numerical diagnostic)"})
    return rows


def family_rows(grid: Grid) -> list[dict]:
    pay = payoffs(PRIM, R1)
    laws = (CostLaw("fork_point_6", atoms=((C, 1.0),)), uniform_noise_law(0.5),
            CostLaw("two_point_3.5", atoms=((3.5, 0.05), (C, 0.95))))
    rows = []
    for law in laws:
        z0 = forced_pool_end(PRIM, pay, law)
        start = max(z0, -1.0)
        for cutoff in np.round(np.arange(start, 4.0001, 0.05), 4):
            fp = iterate(PRIM, grid, R1, law, 1.0, -1.0, cutoff=float(cutoff))
            belief = half_line_pool_belief(PRIM, float(cutoff))
            consistent = float(entry_at_belief(PRIM, pay, law, belief)) == 0.0
            rows.append({"law": law.label, "r": R1, "cutoff": float(cutoff), "pool_belief_formula": belief,
                         "challenger_consistent": consistent,
                         "fixed_point": fp is not None,
                         "qH": fp.qH if fp else float("nan"), "qL": fp.qL if fp else float("nan"),
                         "E": fp.E if fp else float("nan"), "U_H": fp.U_H if fp else float("nan"),
                         "U_L": fp.U_L if fp else float("nan"),
                         "live": bool(fp is not None and fp.E > 0.0),
                         "status": "numerical diagnostic" if fp else
                         ("analytical: not an equilibrium, pool belief justifies entry" if not consistent else
                          "open: no fixed point from full-order start")})
    return rows


def branch_rows(grid: Grid) -> list[dict]:
    rs = sorted(set(np.round(np.arange(1.2, 3.5, 0.05), 4).tolist())
                | set(np.round(np.arange(3.5, 4.0, 0.01), 4).tolist())
                | set(np.round(np.arange(4.0, 5.001, 0.05), 4).tolist()) | {3.5926, 3.5927})
    laws = LAWS[:5]
    rows = []
    for law in laws:
        for r in rs:
            pay = payoffs(PRIM, r)
            g_half = entry_at_belief(PRIM, pay, law, 0.5)
            rows.append({"law": law.label, "r": r, "branch": "no_trade", "qH": 0.0, "qL": 0.0, "E": g_half,
                         "O_H": 0.5 * g_half, "U_H": 0.0, "U_L": 0.0, "pool_prob": 1.0 if g_half == 0.0 else 0.0,
                         "exists": no_trade_exists(PRIM, pay, law), "regime": regime(PRIM, pay, law),
                         "status": "analytical"})
            found, n_live, n_zero = grid_starts(grid, r, law)
            for fp in found:
                rows.append({"law": law.label, "r": r, "branch": "live", "qH": fp.qH, "qL": fp.qL, "E": fp.E,
                             "O_H": fp.O_H, "U_H": fp.U_H, "U_L": fp.U_L, "pool_prob": fp.pool_prob, "exists": True,
                             "regime": regime(PRIM, pay, law), "starts_to_live": n_live,
                             "starts_to_zero": n_zero, "status": "numerical diagnostic"})
            print(f"{law.label} r={r:.4f} live={[(round(f.qH, 2), round(f.qL, 2), round(f.E, 4)) for f in found]}",
                  flush=True)
    return rows


def full_order_boundary_rows() -> list[dict]:
    """Strength interval on which the full-order minimal-pool equilibrium exists, for regime III laws.

    When the entry set lies in [0, inf), the low type's full short is optimal iff k <= (1 - 1/b) J (Lemma C.8),
    and the high type's full buy is then optimal as well, so the test is exact. Endpoints by root finding on
    the quadrature value of J: numerical diagnostic.
    """
    from scipy import optimize
    rows = []
    for law in LAWS[:3]:
        c0, _ = lowest_cost(PRIM, law)
        r_top = ceiling_strength(PRIM, c0)

        def margin(r: float) -> float:
            pay = payoffs(PRIM, r)
            return (1.0 - 1.0 / PRIM.b) * full_order_outcome(PRIM, pay, law).J - PRIM.k

        grid_r = np.linspace(1.05, r_top - 1e-6, 400)
        vals = [margin(float(r)) for r in grid_r]
        lo = hi = float("nan")
        for a, b_, va, vb in zip(grid_r[:-1], grid_r[1:], vals[:-1], vals[1:]):
            if va < 0.0 <= vb and math.isnan(lo):
                lo = optimize.brentq(margin, a, b_, xtol=1e-10)
            if va >= 0.0 > vb:
                hi = optimize.brentq(margin, a, b_, xtol=1e-10)
        top_margin = vals[-1]
        rows.append({"law": law.label, "full_order_lower_r": lo,
                     "full_order_upper_r": hi if not math.isnan(hi) else r_top,
                     "upper_end_reason": "investor test fails" if not math.isnan(hi) else "preparation ceiling",
                     "ceiling_r_C_of_c0": r_top, "margin_just_below_ceiling": top_margin,
                     "x_pool_end_nonnegative": True, "status": "numerical diagnostic"})
    return rows


def main() -> None:
    grid = make_grid(PRIM)
    write_csv(HERE / "laws.csv", laws_table())
    write_csv(HERE / "regime_map.csv", regime_rows())
    write_csv(HERE / "laws_r3.csv", laws_r3_rows(grid))
    write_csv(HERE / "eps_r3.csv", eps_rows(grid))
    write_csv(HERE / "floor_rho.csv", floor_rows())
    write_csv(HERE / "lowest_cost_r3.csv", lowest_cost_rows())
    write_csv(HERE / "family_r3.csv", family_rows(grid))
    write_csv(HERE / "full_order_boundaries.csv", full_order_boundary_rows())
    write_csv(HERE / "branches.csv", branch_rows(grid))
    print("done")


if __name__ == "__main__":
    main()
