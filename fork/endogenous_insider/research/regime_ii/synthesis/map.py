"""Synthesis map over r1 at rho = 0.25: where the regime II reversal holds in every equilibrium.

Reuses the theory track's closed forms (theory/formulas.py). For each strong strength r1 it writes:
  B_m, B_half, B_M            profit levels at r1 (regime II is B_m < c_L < B_half; ceiling if B_M < c_H)
  a3_right                    right side of the paper's (A3), (1 - 1/b) rho m Delta_T(r1)
  supK                        sup of the forcing bound K(c_L) over regime II (its floor limit, Lemma C.1)
  r0_max                      largest r0 with Delta_T(r0) < supK: (A3') is empty for r0 above it
  a4_entry, a4_own            largest c_L with inf E >= rho and inf e_H >= rho over all consistent
                              full-order pools (Proposition R.7 knapsack); these are the (A4') thresholds
Status of every number: numerical diagnostic (double-precision root of a closed form).
Run from this folder: python3 map.py  (writes map.csv)
"""
from __future__ import annotations

import csv
import math
import os
import sys
from dataclasses import replace

from scipy import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "theory"))
import formulas as fm  # noqa: E402

BASE = fm.Params(rho=0.25, k=0.02)
R1_GRID = (2.0, 2.3, 2.5, 2.7, 2.9, 3.0, 3.1, 3.3, 3.5, 3.6)


def a4_threshold(prm: fm.Params, target: str) -> float:
    """Largest c_L in regime II at prm.r with inf over consistent pools >= rho (bisection on c_L)."""
    lv0 = fm.levels(prm)
    lo, hi = lv0.B_m + 1e-6, lv0.B_half - 1e-6

    def gap(cL: float) -> float:
        p = replace(prm, c_L=cL)
        lv = fm.levels(p)
        return fm.knapsack(p, lv, target).inf_value - prm.rho

    if gap(lo) <= 0.0:
        return float("nan")  # fails already at the floor
    if gap(hi) >= 0.0:
        return hi
    return optimize.brentq(gap, lo, hi, xtol=1e-9)


def sup_forcing(prm: fm.Params) -> float:
    """Floor limit of K(c_L): (1/2)(1 - 1/b) rho m Delta_T(r1) (Lemma C.1 of the theory referee)."""
    lv = fm.levels(prm)
    return 0.5 * (1.0 - 1.0 / prm.b) * prm.rho * lv.m * lv.DeltaT


def r0_max(prm: fm.Params, K: float) -> float:
    """Largest r0 with Delta_T(r0) = (r0 - ell)^2 / (2 r0) < K."""
    return prm.ell + K + math.sqrt(K * K + 2.0 * prm.ell * K)


def row(r1: float) -> dict:
    prm = replace(BASE, r=r1, c_L=3.0)
    lv = fm.levels(prm)
    K = sup_forcing(prm)
    ceiling = lv.B_M < prm.c_H
    return {
        "r1": r1,
        "B_m": lv.B_m,
        "B_half": lv.B_half,
        "B_M": lv.B_M,
        "ceiling": ceiling,
        "DeltaT": lv.DeltaT,
        "a3_right": (1.0 - 1.0 / prm.b) * prm.rho * lv.m * lv.DeltaT,
        "k002_in_a3": (1.0 - 1.0 / prm.b) * prm.rho * lv.m * lv.DeltaT > prm.k,
        "supK": K,
        "r0_max": r0_max(prm, K),
        "a4_entry": float("nan") if ceiling else a4_threshold(prm, "E"),
        "a4_own": float("nan") if ceiling else a4_threshold(prm, "eH"),
    }


def main() -> None:
    rows = [row(r) for r in R1_GRID]
    with open(os.path.join(HERE, "map.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for rw in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in rw.items()})
    for rw in rows:
        print({k: (round(v, 5) if isinstance(v, float) else v) for k, v in rw.items()})


if __name__ == "__main__":
    main()
