"""Theory track solver: writes the CSV files that the note cites. Run from this folder: python3 thresholds.py

Outputs
- constants_r1.csv     profit levels and belief thresholds at r1 = 3 (benchmark primitives)
- knapsack_r1.csv      per (rho, c_L): forcing bound K, pool cap, minimal-pool and worst-pool entry and e_H
- thresholds_r1.csv    per rho: c_L thresholds of the knapsack, the half-line family, and the simple bound
- starved_r1.csv       per k: lowest c_L at which the starved family exists, and the limiting member
- starved_checks.csv   high-type best-response checks on starved members (grid, numerical diagnostic)
- example_r1.csv       one parameter point inside Proposition 2' (r0 = 1.1, k = 0.008)
"""
from __future__ import annotations

import csv
import math
from dataclasses import replace

import numpy as np
from scipy import optimize

import formulas as fm

BASE = fm.Params()


def write(path: str, rows: list[dict]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in row.items()})


def constants() -> list[dict]:
    lv = fm.levels(BASE)
    lv0 = fm.levels(BASE, r=1.2)
    return [{"r": 3.0, "t0": lv.t0, "wL": lv.wL, "Delta_T": lv.DeltaT, "m": lv.m, "M": lv.M, "B_m": lv.B_m,
             "B_half": lv.B_half, "B_M": lv.B_M, "tau_H": lv.tau_H, "x_star": lv.x_star,
             "v_H": fm.v_H(BASE, lv), "A3_bound": fm.a3_bound(BASE, lv), "two_k_over_DeltaT": 2 * BASE.k / lv.DeltaT,
             "Delta_T_r0": lv0.DeltaT, "B_r0_half": lv0.B_half, "B_r0_m": lv0.B_m}]


def knapsack_rows() -> list[dict]:
    rows = []
    for rho in (0.1, 0.2, 0.25, 0.3, 0.35, 0.5):
        for cL in np.round(np.arange(2.37, 4.29, 0.01), 4):
            prm = replace(BASE, rho=rho, c_L=float(cL))
            lv = fm.levels(prm)
            if not fm.regime_ii(prm, lv):
                continue
            E0, eH0 = fm.full_minimal_pool(prm, lv)
            kE = fm.knapsack(prm, lv, "E")
            kH = fm.knapsack(prm, lv, "eH")
            uH, uL, pib = fm.pool_cap(prm, lv)
            rows.append({"rho": rho, "c_L": float(cL), "tau_L": lv.tau_L, "z0": lv.z0, "x_bar": lv.x_bar,
                         "pool_cap": pib, "pool_cap_H": uH, "K_force": fm.forcing_bound(prm, lv),
                         "E0": E0, "infE": kE.inf_value, "eH0": eH0, "infeH": kH.inf_value,
                         "budget": kE.budget, "E_island_end": kE.y2, "E_mid_end": kE.y1,
                         "E_plateau_frac": kE.plateau_frac, "simple_lowerE": fm.simple_sufficient(prm, lv)})
    return rows


def crossing(rows: list[dict], rho: float, col: str, level: float) -> float:
    """Smallest c_L on the grid at which col drops to level or below, refined by bisection on the closed form."""
    sel = [r for r in rows if r["rho"] == rho]
    prev = None
    for r in sel:
        if r[col] <= level:
            if prev is None:
                return r["c_L"]
            f = lambda c: _eval(rho, c, col) - level
            return optimize.brentq(f, prev["c_L"], r["c_L"], xtol=1e-10)
        prev = r
    return float("nan")


def _eval(rho: float, cL: float, col: str) -> float:
    prm = replace(BASE, rho=rho, c_L=cL)
    lv = fm.levels(prm)
    if col == "infE":
        return fm.knapsack(prm, lv, "E").inf_value
    if col == "infeH":
        return fm.knapsack(prm, lv, "eH").inf_value
    if col == "simple_lowerE":
        return fm.simple_sufficient(prm, lv)
    raise ValueError(col)


def threshold_rows(krows: list[dict]) -> list[dict]:
    out = []
    for rho in (0.1, 0.2, 0.25, 0.3, 0.35, 0.5):
        prm = replace(BASE, rho=rho)
        lv = fm.levels(prm)
        hl = fm.half_line_thresholds(prm, lv)
        out.append({"rho": rho, "cL_knapsack_E": crossing(krows, rho, "infE", rho),
                    "cL_knapsack_O": crossing(krows, rho, "infeH", rho),
                    "cL_simple_E": crossing(krows, rho, "simple_lowerE", rho),
                    "cL_halfline_E": hl["cL_E"], "cL_halfline_O": hl["cL_eH"],
                    "x_E": hl["x_E"], "x_eH": hl["x_eH"], "x_k": hl["x_k"]})
    return out


def starved_rows() -> tuple[list[dict], list[dict]]:
    rows, checks = [], []
    for k in (0.03, 0.025, 0.0224, 0.022, 0.021, 0.02, 0.019, 0.018, 0.017, 0.016, 0.015, 0.0125, 0.01, 0.0075, 0.005):
        prm = replace(BASE, k=k)
        lv = fm.levels(prm)
        vh = fm.v_H(prm, lv)
        best = None
        for v in np.linspace(0.01, vh * (1 - 1e-9), 600):
            mem = fm.starved_member(prm, lv, float(v))
            if mem is None:
                continue
            if best is None or mem[1] < best[1][1]:
                best = (float(v), mem)
        if best is None:
            rows.append({"k": k, "cL_starved": float("nan"), "v": float("nan"), "x_prime": float("nan"),
                         "pool_belief": float("nan"), "E": float("nan"), "eH": float("nan")})
            continue
        v, (xp, pb, E, eH) = best
        cL = lv.gL + pb * (lv.gH - lv.gL)
        rows.append({"k": k, "cL_starved": cL, "v": v, "x_prime": xp, "pool_belief": pb, "E": E, "eH": eH})
        # high type check on a fine grid at three members along the family
        for vv in (v, 0.6 * v, 0.3 * v):
            mem = fm.starved_member(prm, lv, vv)
            if mem is None:
                continue
            s_grid = np.linspace(0.0, 1.0, 401)
            U = np.array([fm.starved_UH(prm, lv, vv, mem[0], float(s)) for s in s_grid])
            checks.append({"k": k, "v": vv, "x_prime": mem[0], "pool_belief": mem[1], "U_H_full": U[-1],
                           "max_U_H_interior": float(U[:-1].max()), "argmax_s": float(s_grid[U.argmax()]),
                           "full_buy_best": bool(U.argmax() == len(U) - 1 and U[-1] > 0)})
    return rows, checks


def example_rows() -> list[dict]:
    """A point inside Proposition 2': r0 = 1.1, k = 0.008, c_L in regime II at r1 = 3."""
    out = []
    for cL in (2.40, 2.50, 2.60, 2.70):
        prm = replace(BASE, k=0.008, c_L=cL)
        lv = fm.levels(prm)
        lv0 = fm.levels(prm, r=1.1)
        kE = fm.knapsack(prm, lv, "E")
        kH = fm.knapsack(prm, lv, "eH")
        out.append({"c_L": cL, "k": prm.k, "Delta_T_r0": lv0.DeltaT, "B_r0_half": lv0.B_half,
                    "K_force": fm.forcing_bound(prm, lv), "A3_ok": lv0.DeltaT < prm.k < fm.forcing_bound(prm, lv),
                    "infE": kE.inf_value, "E0": kE.base, "infeH": kH.inf_value, "eH0": kH.base,
                    "PE_ok": kE.inf_value >= prm.rho, "PO_ok": kH.inf_value >= prm.rho})
    return out


def main() -> None:
    write("constants_r1.csv", constants())
    krows = knapsack_rows()
    write("knapsack_r1.csv", krows)
    write("thresholds_r1.csv", threshold_rows(krows))
    srows, checks = starved_rows()
    write("starved_r1.csv", srows)
    write("starved_checks.csv", checks)
    write("example_r1.csv", example_rows())


if __name__ == "__main__":
    main()
