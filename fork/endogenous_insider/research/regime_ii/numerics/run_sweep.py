"""Drivers that write CSV. Solvers write CSV only; render.py reads CSV and never solves.

  python3 run_sweep.py r3 [rho]        c_L sweep at r1 = 3 (default rho = 0.25, 0.1, 0.5 in turn)
  python3 run_sweep.py region          (r1, rho, c_L) region map

Files written next to this script:
  eq_r3_rho<rho>.csv        every distinct equilibrium found, one row each
  summary_r3_rho<rho>.csv   one row per c_L: counts, extremes, reversal flag
  eq_region.csv, summary_region.csv   the region sweep
"""
from __future__ import annotations

import csv
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import make_econ, no_trade_exists
from scan import regime_of, row_of, scan_point

HERE = Path(__file__).resolve().parent
CH = 6.0
R0 = 1.2

EQ_COLS = ["r", "rho", "cL", "cH", "tauL", "tauH", "regime", "family", "cutoff", "pool_end", "qH", "qL", "eH", "eL",
           "E", "O_H", "pool_prob", "pool_belief", "var_mu", "informative", "E_weak", "OH_weak", "E_gt_weak",
           "OH_gt_weak", "reversal", "regret_H", "regret_L", "entry_gap_E", "entry_gap_OH"]
SUM_COLS = ["r", "rho", "cL", "tauL", "regime", "no_trade_r1", "n_eq", "n_profiles", "unique_full", "n_unresolved",
            "E_min", "E_max", "OH_min", "OH_max", "fam_at_Emin", "q_at_Emin", "cutoff_at_Emin", "reversal_all",
            "reversal_any", "E_weak", "OH_weak", "weak_notrade_unique", "all_informative", "status"]


def fmt(v):
    if isinstance(v, (bool, np.bool_)):
        return "true" if v else "false"
    if isinstance(v, float):
        if math.isinf(v):
            return "inf" if v > 0 else "-inf"
        return f"{v:.10g}"
    return v


def write_csv(path: Path, cols: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: fmt(row.get(c, "")) for c in cols})


def solve_point(args: tuple) -> tuple[list[dict], dict]:
    """All equilibria found at one (r, rho, c_L) and the summary row."""
    r, rho, cL, step, tau_override = args
    ec = make_econ(r, rho, cL, CH, tauL=tau_override)
    ecw = make_econ(R0, rho, ec.cL, CH)
    res = scan_point(ec, step=step)
    rows = [row_of(ec, c, ecw) for c in res.members]
    nt = no_trade_exists(ec)
    summ = summarize(ec, ecw, rows, nt, res.unresolved)
    return rows, summ


def summarize(ec, ecw, rows: list[dict], nt: bool, unresolved: int) -> dict:
    from engine import entry_at_belief
    e_w = entry_at_belief(ecw, 0.5)
    base = {"r": ec.r, "rho": ec.rho, "cL": ec.cL, "tauL": ec.tauL, "regime": regime_of(ec), "no_trade_r1": nt,
            "n_unresolved": unresolved, "E_weak": e_w, "OH_weak": 0.5 * e_w,
            "weak_notrade_unique": ecw.DeltaT < ec.k}
    if not rows:
        return {**base, "n_eq": 0, "status": "open: no equilibrium found"}
    imin = int(np.argmin([r["E"] for r in rows]))
    profs = {(round(r["qH"], 4), round(r["qL"], 4)) for r in rows}
    return {**base, "n_eq": len(rows), "n_profiles": len(profs),
            "unique_full": profs == {(1.0, -1.0)},
            "E_min": min(r["E"] for r in rows), "E_max": max(r["E"] for r in rows),
            "OH_min": min(r["O_H"] for r in rows), "OH_max": max(r["O_H"] for r in rows),
            "fam_at_Emin": rows[imin]["family"], "q_at_Emin": f"({rows[imin]['qH']:.4f};{rows[imin]['qL']:.4f})",
            "cutoff_at_Emin": rows[imin]["cutoff"],
            "reversal_all": all(r["reversal"] for r in rows), "reversal_any": any(r["reversal"] for r in rows),
            "all_informative": all(r["informative"] for r in rows),
            "status": "numerical diagnostic"}


def cL_grid() -> list[tuple[float, float | None]]:
    """c_L grid for the r1 = 3 sweep: step 0.025 on [2.30, 4.35] plus exact ties (given as tau)."""
    base = [(round(float(x), 6), None) for x in np.arange(2.30, 4.35 + 1e-9, 0.025)]
    extra = [(2.36, None), (2.37, None), (4.28, None), (4.29, None), (4.2917, None), (4.30, None)]
    ties = [(0.0, 0.2689414213699951), (0.0, 0.5)]   # c_L = B(m) and c_L = B(1/2) via tau
    seen = {}
    for c, t in base + extra + ties:
        seen[(c, t)] = (c, t)
    return sorted(seen.values(), key=lambda v: (v[0], v[1] or 0.0))


def run_r3(rho: float, step: float = 0.05) -> None:
    jobs = []
    for cL, tau in cL_grid():
        jobs.append((3.0, rho, cL if tau is None else None, step, tau))
    t0 = time.time()
    with Pool(4) as pool:
        out = pool.map(solve_point, jobs, chunksize=1)
    rows = [r for rs, _ in out for r in rs]
    summ = [s for _, s in out]
    tag = f"{rho:g}"
    write_csv(HERE / f"eq_r3_rho{tag}.csv", EQ_COLS, rows)
    write_csv(HERE / f"summary_r3_rho{tag}.csv", SUM_COLS, summ)
    print(f"rho={rho}: {len(rows)} equilibria at {len(summ)} points in {time.time() - t0:.0f}s")


def region_jobs(step: float):
    """(r1, rho, c_L) lattice. c_L runs over regime I control and regime II at each r1."""
    from engine import make_econ as mk
    jobs = []
    for rho in (0.1, 0.25, 0.5):
        for r1 in np.round(np.arange(1.5, 3.6001, 0.1), 4):
            ec = mk(float(r1), rho, 1.0, CH)
            lo = ec.gL + ec.m * (ec.gH - ec.gL)         # B(m)
            hi = ec.gL + 0.5 * (ec.gH - ec.gL)          # B(1/2)
            # regime I control, then fractions of the regime II interval
            cl = [lo - 0.05] + [lo + f * (hi - lo) for f in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95)]
            for c in cl:
                jobs.append((float(r1), rho, float(c), step, None))
    return jobs


def run_region(step: float = 0.1) -> None:
    jobs = region_jobs(step)
    t0 = time.time()
    with Pool(4) as pool:
        out = pool.map(solve_point, jobs, chunksize=1)
    rows = [r for rs, _ in out for r in rs]
    summ = [s for _, s in out]
    write_csv(HERE / "eq_region.csv", EQ_COLS, rows)
    write_csv(HERE / "summary_region.csv", SUM_COLS, summ)
    print(f"region: {len(rows)} equilibria at {len(summ)} points in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "r3"
    if what == "r3":
        rhos = [float(sys.argv[2])] if len(sys.argv) > 2 else [0.25, 0.1, 0.5]
        for rho in rhos:
            run_r3(rho)
    elif what == "region":
        run_region()
