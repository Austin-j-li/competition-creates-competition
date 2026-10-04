"""Slack-relaxed pool LP on a fine order lattice: a search for equilibria the coarse lattice could miss.

For each c_L, every order pair on a fine lattice (qH step 0.1, qL step 0.025) is tested with the pool LP in
which each type may gain up to `slack` from a deviation (an epsilon-equilibrium in orders). An exact equilibrium
whose orders lie within about one lattice step of a lattice point is epsilon-feasible, so this finds windows
that are too narrow for the exact lattice. Feasible pairs other than a neighbourhood of (1,-1) are then
examined: polish() runs best-response iteration under the LP pool and reports whether an exact equilibrium
sits nearby. Writes lp_relaxed.csv.  r1 = 3, rho = 0.25, k = 0.02.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import make_econ
from lp_map import EPS, jenc, polish
from pool_lp import build_cells, pool_to_intervals, solve
from run_sweep import CH, fmt

HERE = Path(__file__).resolve().parent
SLACK = 2e-5


def job(cL: float) -> list[dict]:
    ec = make_econ(3.0, 0.25, cL, CH)
    rows = []
    for qH in [round(0.1 * i, 1) for i in range(0, 11)]:
        for qL in [round(-0.025 * i, 3) for i in range(0, 41)]:
            if qH == 0.0 and qL == 0.0:
                continue
            cells = build_cells(ec, qH, qL)
            s = solve(ec, qH, qL, "E", cells=cells, eps=EPS, slack=SLACK)
            if s is None:
                continue
            near_full = qH >= 0.9 and qL <= -0.95
            row = {"cL": cL, "qH": qH, "qL": qL, "E_min": s["E"], "near_full": near_full, "polished": "", "E_pol": "",
                   "qH_pol": "", "qL_pol": ""}
            if not near_full:
                pol = polish(ec, qH, qL, pool_to_intervals(s))
                if pol is not None:
                    row.update({"polished": bool(pol["exact"]), "E_pol": pol["E"], "qH_pol": pol["qH"],
                                "qL_pol": pol["qL"]})
            rows.append(row)
    return rows


if __name__ == "__main__":
    cls = [2.40, 2.50, 2.55, 2.60, 2.70, 2.80, 2.90, 2.95, 2.97, 2.98]
    with Pool(4) as p:
        out = p.map(job, cls, chunksize=1)
    rows = [r for rs in out for r in rs]
    cols = ["cL", "qH", "qL", "E_min", "near_full", "polished", "E_pol", "qH_pol", "qL_pol"]
    with (HERE / "lp_relaxed.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: fmt(r.get(c, "")) for c in cols})
    print("lp_relaxed", len(rows))
