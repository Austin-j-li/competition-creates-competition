"""Test of the theory track's thresholds against this folder's exact solvers (r1 = 3, c_H = 6, r0 = 1.2).

  knapsack E and O_H thresholds  (theory/thresholds_r1.csv, columns cL_knapsack_E, cL_knapsack_O)
      theory solves the fractional knapsack under forcing (small k). Here the LP over all full-order pools is
      solved with the sufficient investor test J >= k/(1 - 1/b) at k = 0.005 (forcing holds) and k = 0.02.
  starved thresholds  (theory/starved_r1.csv)
      here: starved.cL_threshold at the same k.

The theory files are read, never written. Writes theory_test.csv. Status of every row: numerical diagnostic.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

from run_sweep import fmt
from thresholds import knap_threshold
import starved

HERE = Path(__file__).resolve().parent
THEORY = HERE.parent / "theory"


def read_theory(name: str) -> list[dict]:
    with (THEORY / name).open() as fh:
        return list(csv.DictReader(fh))


def job(args: tuple) -> dict:
    kind, rho, k, theory = args
    if kind == "knap_E":
        mine = knap_threshold(3.0, rho, k, "E")
    elif kind == "knap_O":
        mine = knap_threshold(3.0, rho, k, "eH")
    else:
        st = starved.cL_threshold(3.0, rho, k)
        mine = st["cL_star"] if st else math.nan
    return {"kind": kind, "rho": rho, "k": k, "mine": mine, "theory": theory,
            "diff": (mine - theory) if not (math.isnan(mine) or math.isnan(theory)) else math.nan}


def num(s: str) -> float:
    return math.nan if s in ("", "nan") else float(s)


if __name__ == "__main__":
    jobs = []
    for r in read_theory("thresholds_r1.csv"):
        rho = float(r["rho"])
        for k in (0.005, 0.02):
            jobs.append(("knap_E", rho, k, num(r["cL_knapsack_E"])))
            jobs.append(("knap_O", rho, k, num(r["cL_knapsack_O"])))
    for r in read_theory("starved_r1.csv"):
        k = float(r["k"])
        if k in (0.02, 0.015, 0.01, 0.0075):
            jobs.append(("starved", 0.25, k, num(r["cL_starved"])))
    with Pool(4) as p:
        out = p.map(job, jobs, chunksize=1)
    cols = ["kind", "rho", "k", "mine", "theory", "diff"]
    with (HERE / "theory_test.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow({c: fmt(r[c]) for c in cols})
    print("theory_test.csv", len(out))
