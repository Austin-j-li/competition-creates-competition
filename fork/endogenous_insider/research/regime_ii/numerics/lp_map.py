"""Order-lattice map of the pure-order equilibrium set under ARBITRARY pools (uses pool_lp.py).

For one economy: for every order pair on a lattice, solve the pool LP for the lowest total entry E and the
lowest high-type entry e_H (hence O_H). A pair is feasible when some pool makes the orders a global best
response with a consistent pool belief. Each minimiser is polished by best-response iteration under its
own pool and checked by the exact engine; verify.py then checks it independently.

  python3 lp_map.py r3 [rho]     c_L sweep at r1 = 3 (default rho = 0.25)
  python3 lp_map.py region       (r1, rho, c_L) lattice, coarser order lattice
"""
from __future__ import annotations

import csv
import json
import math
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import Econ, build_schedule, entry_at_belief, make_econ, outcome, pure_pool, regret
from island import iterate_pool
from pool_lp import build_cells, pool_to_intervals, solve
from run_sweep import CH, R0, cL_grid, fmt
from scan import regime_of

HERE = Path(__file__).resolve().parent
EPS = 2e-4


def jenc(pool: tuple[tuple[float, float], ...]) -> str:
    return json.dumps([[("-inf" if a == -math.inf else a), ("inf" if b == math.inf else b)] for a, b in pool])


def jdec(s: str) -> tuple[tuple[float, float], ...]:
    out = []
    for a, b in json.loads(s):
        out.append((-math.inf if a == "-inf" else float(a), math.inf if b == "inf" else float(b)))
    return tuple(out)


def polish(ec: Econ, qH: float, qL: float, pool: tuple[tuple[float, float], ...]) -> dict | None:
    """Best-response iteration under the LP pool. Returns an exact fixed point or None."""
    fp = iterate_pool(ec, (qH, qL), pool)
    if fp is None:
        return None
    sch = build_schedule(ec, pure_pool(fp[0], fp[1], pool))
    rH, rL = regret(sch, fp[0], fp[1])
    o = outcome(sch)
    ok = sch.consistent and rH <= 1e-9 and rL <= 1e-9
    return {"qH": fp[0], "qL": fp[1], "consistent": sch.consistent, "regret_H": rH, "regret_L": rL, "E": o.E,
            "O_H": o.O_H, "eH": o.eH, "eL": o.eL, "pool_prob": o.pool_prob, "pool_belief": o.pool_belief,
            "var_mu": o.var_mu, "exact": ok}


def envelope(ec: Econ, qHs: list[float], qLs: list[float]) -> tuple[list[dict], list[dict]]:
    """Feasibility and minima over the order lattice. Returns (lattice rows, polished minimisers)."""
    rows: list[dict] = []
    best: dict[str, tuple[float, dict]] = {}
    for qH in qHs:
        for qL in qLs:
            if qH == 0.0 and qL == 0.0:
                continue
            cells = build_cells(ec, qH, qL)
            sE = solve(ec, qH, qL, "E", cells=cells, eps=EPS)
            if sE is None:
                rows.append({"qH": qH, "qL": qL, "feasible": False})
                continue
            sH = solve(ec, qH, qL, "eH", cells=cells, eps=EPS)
            rows.append({"qH": qH, "qL": qL, "feasible": True, "E_min": sE["E"], "OH_min": sH["O_H"] if sH else math.nan,
                         "E_at_OHmin": sH["E"] if sH else math.nan, "belief_E": sE["belief"]})
            for key, sol in (("E", sE), ("OH", sH)):
                if sol is None:
                    continue
                val = sol["E"] if key == "E" else sol["O_H"]
                if key not in best or val < best[key][0]:
                    best[key] = (val, {"qH": qH, "qL": qL, "sol": sol})
    mins: list[dict] = []
    for key, (val, d) in best.items():
        pool = pool_to_intervals(d["sol"])
        pol = polish(ec, d["qH"], d["qL"], pool)
        mins.append({"which": key, "lp_value": val, "qH0": d["qH"], "qL0": d["qL"], "pool": pool, "polished": pol})
    return rows, mins


def lattice(ec: Econ, coarse: bool = False) -> tuple[list[float], list[float]]:
    if coarse:
        return [1.0, 0.7, 0.4], [round(-0.1 * i, 2) for i in range(0, 11)]
    return [1.0, 0.8, 0.6, 0.4, 0.2, 0.0], [round(-0.05 * i, 2) for i in range(0, 21)]


def solve_point(args: tuple) -> tuple[list[dict], dict, list[dict]]:
    r, rho, cL, tau, coarse = args
    ec = make_econ(r, rho, cL, CH, tauL=tau)
    ecw = make_econ(R0, rho, ec.cL, CH)
    qHs, qLs = lattice(ec, coarse)
    rows, mins = envelope(ec, qHs, qLs)
    e_w = entry_at_belief(ecw, 0.5)
    feas = [x for x in rows if x["feasible"]]
    summ = {"r": r, "rho": rho, "cL": ec.cL, "tauL": ec.tauL, "regime": regime_of(ec), "E_weak": e_w,
            "OH_weak": 0.5 * e_w, "n_lattice": len(rows), "n_feasible": len(feas),
            "E_min_LP": min([x["E_min"] for x in feas], default=math.nan),
            "OH_min_LP": min([x["OH_min"] for x in feas if not math.isnan(x["OH_min"])], default=math.nan)}
    summ["reversal_all_LP"] = bool(feas) and summ["E_min_LP"] > e_w + 1e-9 and summ["OH_min_LP"] > 0.5 * e_w + 1e-9
    for m in mins:
        tag = m["which"]
        p = m["polished"]
        summ[f"qH_at_{tag}min"] = m["qH0"]
        summ[f"qL_at_{tag}min"] = m["qL0"]
        summ[f"pool_{tag}"] = jenc(m["pool"])
        summ[f"polished_{tag}"] = bool(p and p["exact"])
        summ[f"E_polished_{tag}"] = p["E"] if p else math.nan
        summ[f"OH_polished_{tag}"] = p["O_H"] if p else math.nan
        summ[f"qH_polished_{tag}"] = p["qH"] if p else math.nan
        summ[f"qL_polished_{tag}"] = p["qL"] if p else math.nan
    lat_rows = [{"r": r, "rho": rho, "cL": ec.cL, **x} for x in rows]
    return lat_rows, summ, mins


SUM_COLS = ["r", "rho", "cL", "tauL", "regime", "E_weak", "OH_weak", "n_lattice", "n_feasible", "E_min_LP", "OH_min_LP",
            "reversal_all_LP", "qH_at_Emin", "qL_at_Emin", "E_polished_E", "OH_polished_E", "qH_polished_E",
            "qL_polished_E", "polished_E", "pool_E", "qH_at_OHmin", "qL_at_OHmin", "OH_polished_OH", "E_polished_OH",
            "qH_polished_OH", "qL_polished_OH", "polished_OH", "pool_OH"]


def write(path: Path, cols: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: fmt(r.get(c, "")) for c in cols})


def run_r3(rho: float) -> None:
    jobs = [(3.0, rho, c if t is None else None, t, False) for c, t in cL_grid()]
    t0 = time.time()
    with Pool(4) as pool:
        out = pool.map(solve_point, jobs, chunksize=1)
    write(HERE / f"lp_summary_r3_rho{rho:g}.csv", SUM_COLS, [s for _, s, _ in out])
    lat_cols = ["r", "rho", "cL", "qH", "qL", "feasible", "E_min", "OH_min", "E_at_OHmin", "belief_E"]
    write(HERE / f"lp_lattice_r3_rho{rho:g}.csv", lat_cols, [x for rows, _, _ in out for x in rows])
    print(f"lp r3 rho={rho}: {len(out)} points in {time.time() - t0:.0f}s")


def region_jobs() -> list[tuple]:
    jobs = []
    for rho in (0.1, 0.25, 0.5):
        for r1 in np.round(np.arange(1.5, 3.6001, 0.1), 4):
            ec = make_econ(float(r1), rho, 1.0, CH)
            lo = ec.gL + ec.m * (ec.gH - ec.gL)
            hi = ec.gL + 0.5 * (ec.gH - ec.gL)
            cl = [lo + (i + 0.5) / 12.0 * (hi - lo) for i in range(12)]
            for c in cl:
                jobs.append((float(r1), rho, float(c), None, True))
    return jobs


def run_region() -> None:
    jobs = region_jobs()
    t0 = time.time()
    with Pool(4) as pool:
        out = pool.map(solve_point, jobs, chunksize=1)
    write(HERE / "lp_summary_region.csv", SUM_COLS, [s for _, s, _ in out])
    print(f"lp region: {len(out)} points in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "r3"
    if what == "r3":
        run_r3(float(sys.argv[2]) if len(sys.argv) > 2 else 0.25)
    elif what == "region":
        run_region()
