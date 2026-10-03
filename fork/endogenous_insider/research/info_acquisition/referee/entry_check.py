"""Referee scratch: preparation probability at lambda < 1 versus the informed-only entry in Table 3.

Pure functions; prints only. Status: numerical diagnostic.
"""
from __future__ import annotations

import math

from check import BENCH, Prim, V_exogenous, lam_min_direct, threshold


def SZ(pr: Prim, z: float) -> float:
    """Laplace survival function Pr(Z >= z)."""
    return 0.5 * math.exp(-z / pr.b) if z >= 0 else 1 - 0.5 * math.exp(z / pr.b)


def entry(pr: Prim, r: float, lam: float) -> tuple[float, float, float]:
    xs = threshold(pr, r, lam)
    informed = 0.5 * (SZ(pr, xs - 1) + SZ(pr, xs + 1))
    total = lam * informed + (1 - lam) * SZ(pr, xs)
    return xs, informed, total


if __name__ == "__main__":
    pr = BENCH
    lm = lam_min_direct(pr, 3.0)
    for lam in (lm + 1e-12, 0.8897, 0.9298, 0.9699, 1.0):
        xs, inf_, tot = entry(pr, 3.0, lam)
        print(f"r=3 lam={lam:.4f} x*={xs:.4f} entry given acquisition={inf_:.4f} preparation probability={tot:.4f}")
    for lam in (0.0, 0.25, 0.5, 0.75, 1.0):
        print(f"Remark G.1 V({lam}) = {V_exogenous(pr, 3.0, lam):.6f}")
