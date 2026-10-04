"""Export one confirmed breaking member per threshold, just inside the broken range, for independent verification.

For every (r1, rho) row of thresholds.csv this writes equilibria (as rows for verify_csv.py) at c_L a little above c_L*:
  * the oracle member (partial, starved window or low-trade) at c_L* + 0.003 and at the middle of the broken range;
  * the island pool of the knapsack LP (full orders) at the knapsack thresholds + 0.005, with a belief margin of 3e-4
    so that the rounded pool is consistent.
Writes threshold_members.csv. verify_csv.py then checks each row by adaptive quadrature with no engine code.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

from engine import make_econ
from knapsack import check_pool, min_entry, pool_intervals
from lp_map import jenc
from partial import combined_failure
from run_sweep import CH, fmt

HERE = Path(__file__).resolve().parent
COLS = ["r", "rho", "cL", "cH", "regime", "family", "cutoff", "pool", "qH", "qL", "E", "O_H", "which"]


def num(x: str) -> float:
    return math.nan if x in ("", "nan") else float(x)


def member_row(r1: float, rho: float, c: float, k: float, tag: str) -> dict | None:
    ec = make_econ(r1, rho, c, CH, k=k)
    m = combined_failure(ec)
    if m is None:
        return None
    qH = m.get("qH", 1.0)
    return {"r": r1, "rho": rho, "cL": c, "cH": CH, "regime": "II", "family": m["kind"], "cutoff": m["x"], "pool": "",
            "qH": qH, "qL": -m["v"], "E": m["E"], "O_H": m["O_H"], "which": tag}


def island_row(r1: float, rho: float, c: float, k: float, objective: str, tag: str) -> dict | None:
    ec = make_econ(r1, rho, c, CH, k=k)
    sol = min_entry(ec, k / (1.0 - 1.0 / ec.b), objective=objective, eps=3e-4)
    if sol is None:
        return None
    pool = pool_intervals(sol)
    chk = check_pool(ec, pool)
    if not (chk["consistent"] and chk["regret_H"] <= 1e-9 and chk["regret_L"] <= 1e-9):
        return None
    return {"r": r1, "rho": rho, "cL": c, "cH": CH, "regime": "II", "family": "island", "cutoff": "", "pool": jenc(pool),
            "qH": 1.0, "qL": -1.0, "E": float(chk["E"]), "O_H": float(chk["O_H"]), "which": tag}


def job(row: dict) -> list[dict]:
    r1, rho, k = float(row["r1"]), float(row["rho"]), float(row["k"])
    out: list[dict | None] = []
    bm, bh = float(row["B_m"]), float(row["B_half"])
    cp = num(row["cL_partial"])
    if row["no_trade"] != "true" and row["ceiling"] != "true" and not math.isnan(cp):
        out.append(member_row(r1, rho, cp + 0.003, k, "oracle:first break"))
        out.append(member_row(r1, rho, cp + 0.5 * (bh - cp), k, "oracle:middle"))
    for key, obj in (("cL_knapE", "E"), ("cL_knapO", "eH")):
        ck = num(row[key])
        if not math.isnan(ck) and ck > bm + 1e-6:
            for d in (0.005, 0.02):
                x = island_row(r1, rho, min(ck + d, bh - 1e-6), k, obj, f"island:{obj}+{d}")
                if x is not None:
                    out.append(x)
                    break
    return [x for x in out if x is not None]


if __name__ == "__main__":
    with (HERE / "thresholds.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    with Pool(4) as p:
        res = p.map(job, rows, chunksize=1)
    allrows = [x for rs in res for x in rs]
    with (HERE / "threshold_members.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for x in allrows:
            w.writerow({c: fmt(x.get(c, "")) for c in COLS})
    print("threshold_members.csv", len(allrows))
