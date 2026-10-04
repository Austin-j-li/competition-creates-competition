"""Test of theory's forcing claim (Prop R.6): if k <= K(c_L) then every consistent pool N (a Borel set containing Z_0
with belief below tau_L) gives an equilibrium with full orders.

For each (k, c_L) this draws random pools (unions of 1 to 4 random intervals, some with a long tail), keeps those the
engine calls consistent, and checks whether (1, -1) is a global best response for both types under that pool. The count
of consistent pools whose regret is positive is the number of counterexamples. r1 = 3, rho = 0.25, c_H = 6.
Writes forcing_test.csv. Numerical diagnostic: random draws, not a proof.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import build_schedule, make_econ, pure_pool, regret
from kscan import K_theory
from run_sweep import CH, fmt

HERE = Path(__file__).resolve().parent


def random_pool(rng: np.random.Generator) -> tuple[tuple[float, float], ...]:
    n = int(rng.integers(1, 5))
    cuts = []
    for _ in range(n):
        a = float(rng.uniform(-3.0, 5.0))
        w = float(rng.choice([0.05, 0.15, 0.4, 1.0, 2.5, math.inf]))
        cuts.append((a, a + w))
    cuts.sort()
    merged: list[list[float]] = []
    for a, d in cuts:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], d)
        else:
            merged.append([a, d])
    return tuple((a, d) for a, d in merged)


def job(args: tuple) -> dict:
    k, cL, n, seed = args
    ec = make_econ(3.0, 0.25, cL, CH, k=k)
    rng = np.random.default_rng(seed)
    cons = bad = 0
    worst = 0.0
    for _ in range(n):
        pool = random_pool(rng)
        sch = build_schedule(ec, pure_pool(1.0, -1.0, pool))
        if not sch.consistent:
            continue
        cons += 1
        rH, rL = regret(sch, 1.0, -1.0)
        worst = max(worst, rH, rL)
        if rH > 1e-9 or rL > 1e-9:
            bad += 1
    return {"k": k, "cL": cL, "K_theory": K_theory(ec), "drawn": n, "consistent": cons, "not_equilibrium": bad,
            "max_regret": worst}


if __name__ == "__main__":
    jobs = [(k, c, 1500, 7) for c in (2.4, 2.5, 2.7, 2.9) for k in (0.008, 0.012, 0.02, 0.04, 0.06)]
    with Pool(4) as p:
        out = p.map(job, jobs, chunksize=1)
    cols = ["k", "cL", "K_theory", "drawn", "consistent", "not_equilibrium", "max_regret"]
    with (HERE / "forcing_test.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow({c: fmt(r[c]) for c in cols})
    print("forcing_test.csv", len(out))
