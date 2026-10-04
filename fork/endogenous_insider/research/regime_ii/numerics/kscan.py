"""How small must the trading cost k be? Numerical replacement for the right half of (A3) in regime II.

For each c_L in regime II (r1 = 3, rho = 0.25, c_H = 6) find, by bisection in k:

  k_S    the largest k with no starved equilibrium (starved.window is empty): the reversal cannot fail through
         the expensive type being shut out
  k_U    the largest k with a unique trading outcome (1, -1) in everything the cutoff scan finds
  k_R    the largest k with the reversal E > rho and O_H > rho/2 in everything the cutoff scan finds
  K_th   theory's forcing bound K(c_L) = (1 - 1/b) rho Delta_T min{tau_L S(xbar + 1), m S(xbar)} (board, theory #4)

and writes kscan.csv. The scan is the cutoff scan of scan.py (numerical diagnostic, windows narrower than
the cutoff step can be missed); k_S uses the exact window solver. The left half of (A3), k > Delta_T(r0), is
independent of c_L and is checked in weak_r0.py.
"""
from __future__ import annotations

import csv
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import entry_at_belief, make_econ
from run_sweep import CH, R0, fmt
from scan import regime_of, row_of, scan_point, xbar_full
import starved

HERE = Path(__file__).resolve().parent


def S(z: float, b: float) -> float:
    return 0.5 * math.exp(-z / b) if z > 0 else 1.0 - 0.5 * math.exp(z / b)


def K_theory(ec) -> float:
    xb = xbar_full(ec)
    if not math.isfinite(xb):
        return math.nan
    return (1.0 - 1.0 / ec.b) * ec.rho * ec.DeltaT * min(ec.tauL * S(xb + 1.0, ec.b), ec.m * S(xb, ec.b))


def k_starved(r: float, rho: float, cL: float, lo: float = 1e-4, hi: float = 0.2) -> float:
    """Largest k with no starved equilibrium at this c_L (existence is increasing in k)."""
    ex = lambda k: starved.window(make_econ(r, rho, cL, CH, k=k)) is not None   # noqa: E731
    if ex(lo):
        return lo
    if not ex(hi):
        return hi
    a, b = lo, hi
    for _ in range(36):
        m = 0.5 * (a + b)
        if ex(m):
            b = m
        else:
            a = m
    return a


def scan_flags(r: float, rho: float, cL: float, k: float) -> tuple[bool, bool]:
    """(unique trading outcome (1,-1), reversal in all found) from the cutoff scan at this k."""
    ec = make_econ(r, rho, cL, CH, k=k)
    ecw = make_econ(R0, rho, cL, CH, k=k)
    res = scan_point(ec, step=0.05)
    rows = [row_of(ec, c, ecw) for c in res.members]
    if not rows:
        return False, False
    uniq = all(abs(x["qH"] - 1.0) < 1e-6 and abs(x["qL"] + 1.0) < 1e-6 for x in rows)
    rev = all(x["reversal"] for x in rows)
    return uniq, rev


def k_by_scan(r: float, rho: float, cL: float, which: int, lo: float = 2e-3, hi: float = 0.08) -> float:
    """Largest k (to 1e-4) whose scan still has the property: which = 0 unique trading, 1 reversal."""
    ok = lambda k: scan_flags(r, rho, cL, k)[which]   # noqa: E731
    if not ok(lo):
        return 0.0
    if ok(hi):
        return hi
    a, b = lo, hi
    while b - a > 1e-4:
        m = 0.5 * (a + b)
        if ok(m):
            a = m
        else:
            b = m
    return a


def one(args: tuple) -> dict:
    r, rho, cL = args
    ec = make_econ(r, rho, cL, CH)
    return {"r1": r, "rho": rho, "cL": cL, "tauL": ec.tauL, "k_S": k_starved(r, rho, cL), "k_U": k_by_scan(r, rho, cL, 0),
            "k_R": k_by_scan(r, rho, cL, 1), "K_th": K_theory(ec), "DeltaT": ec.DeltaT,
            "no_trade_k": ec.DeltaT * rho / 2.0}


def main() -> None:
    r, rho = 3.0, 0.25
    cls = [2.40, 2.50, 2.60, 2.70, 2.80, 2.90, 3.00, 3.20, 3.40, 3.60]
    with Pool(4) as pool:
        rows = pool.map(one, [(r, rho, c) for c in cls], chunksize=1)
    cols = ["r1", "rho", "cL", "tauL", "DeltaT", "no_trade_k", "K_th", "k_S", "k_U", "k_R"]
    with (HERE / "kscan.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: fmt(row[c]) for c in cols})
    print("kscan.csv written")


if __name__ == "__main__":
    main()
