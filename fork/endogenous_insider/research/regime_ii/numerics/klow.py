"""The low-trade band in k. Low-trade equilibria (both types order less than the full size; E = rho, O_H = rho/2
exactly) exist for k between k_LT and the no-trade bound rho Delta_T / 2. Below k_LT they are gone.

For (r1, rho, c_L) this finds k_LT by bisection on the existence of a confirmed low-trade member (partial.py), and
reports the symmetric order q* at the edge. Writes klow.csv. Numerical diagnostic: the search sees pure orders
and the minimal pool only.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

from engine import make_econ
from partial import low_trade_member
from run_sweep import CH, fmt

HERE = Path(__file__).resolve().parent


def exists(r: float, rho: float, c: float, k: float) -> dict | None:
    return low_trade_member(make_econ(r, rho, c, CH, k=k))


def one(args: tuple) -> dict:
    r, rho, c = args
    ec = make_econ(r, rho, c, CH)
    top = rho * ec.DeltaT / 2.0
    hi = top * 0.999
    mh = exists(r, rho, c, hi)
    row = {"r1": r, "rho": rho, "cL": c, "DeltaT": ec.DeltaT, "k_no_trade": top, "k_LT": math.nan, "q_edge": math.nan,
           "k_paper": 0.02}
    if mh is None:
        return row
    lo = 1e-3
    if exists(r, rho, c, lo) is not None:
        row["k_LT"] = lo
        return row
    a, b = lo, hi
    for _ in range(40):
        mid = 0.5 * (a + b)
        if exists(r, rho, c, mid) is not None:
            b = mid
        else:
            a = mid
    m = exists(r, rho, c, b)
    row["k_LT"] = b
    row["q_edge"] = m["qH"] if m else math.nan
    return row


if __name__ == "__main__":
    jobs = [(3.0, rho, c) for rho in (0.1, 0.25, 0.5) for c in (2.40, 2.60, 2.80)]
    jobs += [(r, 0.25, 2.60) for r in (2.4, 2.6, 3.2, 3.5)]
    with Pool(4) as p:
        out = p.map(one, jobs, chunksize=1)
    cols = ["r1", "rho", "cL", "DeltaT", "k_no_trade", "k_LT", "q_edge", "k_paper"]
    with (HERE / "klow.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow({c: fmt(r[c]) for c in cols})
    print("klow.csv", len(out))
