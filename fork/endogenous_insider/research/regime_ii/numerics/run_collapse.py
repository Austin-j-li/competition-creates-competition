"""Part (iii) of Proposition 2 in regime II: the collapse at r2 > r1.

At r2 with B_{r2}(M) < c_H the expensive type cannot enter in any equilibrium, so E <= rho. In regime I at r2
the cheap type enters at every belief and E = rho exactly (the paper). In regime II at r2 the cheap type exits
after bad prices, so E < rho. This script scans r2 in {3.8, 4, 5} for rho = 0.25 and writes collapse.csv.
"""
from __future__ import annotations

import csv
from multiprocessing import Pool
from pathlib import Path

from engine import make_econ
from run_sweep import CH, R0, fmt
from scan import regime_of, row_of, scan_point

HERE = Path(__file__).resolve().parent


def job(args):
    r2, rho, cL = args
    ec = make_econ(r2, rho, cL, CH)
    ecw = make_econ(R0, rho, cL, CH)
    res = scan_point(ec, step=0.1)
    rows = [row_of(ec, c, ecw) for c in res.members]
    return rows


if __name__ == "__main__":
    jobs = []
    for r2 in (3.8, 4.0, 5.0):
        ec = make_econ(r2, 0.25, 1.0, CH)
        cm = ec.gL + ec.m * (ec.gH - ec.gL)
        ch = ec.gL + 0.5 * (ec.gH - ec.gL)
        for c in (1.0, cm - 0.05, cm + 0.1 * (ch - cm), cm + 0.5 * (ch - cm), cm + 0.9 * (ch - cm)):
            jobs.append((r2, 0.25, float(c)))
    with Pool(4) as p:
        out = p.map(job, jobs, chunksize=1)
    rows = [r for rs in out for r in rs]
    cols = ["r", "rho", "cL", "regime", "family", "cutoff", "qH", "qL", "E", "O_H", "pool_prob", "reversal"]
    with (HERE / "collapse.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: fmt(r.get(c, "")) for c in cols})
    print("collapse.csv", len(rows))
