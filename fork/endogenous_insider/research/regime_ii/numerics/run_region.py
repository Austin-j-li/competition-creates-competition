"""Region sweep: cutoff scan (best-response iteration from many starts) at c_L values placed around each threshold.

Reads thresholds.csv (written by thresholds.py). For every (r1, rho) it scans c_L at: a regime I control just
below B(m); three points between B(m) and the threshold c*; points just below and just above c*; and two points
above c*. Writes eq_region.csv (every equilibrium found) and summary_region.csv (one row per point).
The scan is independent of the threshold solvers, so agreement is a cross-check.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

from run_sweep import EQ_COLS, SUM_COLS, solve_point, write_csv

HERE = Path(__file__).resolve().parent


def jobs() -> list[tuple]:
    out = []
    with (HERE / "thresholds.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r1, rho = float(r["r1"]), float(r["rho"])
        bm, bh = float(r["B_m"]), float(r["B_half"])
        cs = float(r["cL_star"]) if r["cL_star"] not in ("", "nan") else math.nan
        pts = [bm - 0.05]
        if math.isnan(cs):
            pts += [bm + f * (bh - bm) for f in (0.15, 0.4, 0.7, 0.95)]
        else:
            w = max(cs - bm, 1e-3)
            pts += [bm + f * w for f in (0.3, 0.7, 0.95)]
            pts += [cs - 0.01, cs + 0.01, cs + 0.15 * (bh - cs), cs + 0.6 * (bh - cs)]
        for c in pts:
            if bm - 0.06 <= c <= bh - 1e-6:
                out.append((r1, rho, float(c), 0.05, None))
    return out


if __name__ == "__main__":
    js = jobs()
    with Pool(4) as pool:
        res = pool.map(solve_point, js, chunksize=1)
    write_csv(HERE / "eq_region.csv", EQ_COLS, [x for rs, _ in res for x in rs])
    write_csv(HERE / "summary_region.csv", SUM_COLS, [s for _, s in res])
    print("region", len(js), "points", sum(len(rs) for rs, _ in res), "equilibria")
