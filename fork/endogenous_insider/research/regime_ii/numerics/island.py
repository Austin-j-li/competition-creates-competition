"""Island pools: voluntary pools that are not half-lines.

Lemma CD.2(e) lets the pool N be any measurable set that contains the forced pool and has belief below
tau_L. This module scans pools N = (-inf, x_c) U [y1, y2] under pure orders and records the equilibria it
finds: consistent pool, global best response for both types. Orders are the full pair (1, -1) or the
fixed point of best-response iteration started at it. Numerical diagnostic; verify.py can confirm any row.
"""
from __future__ import annotations

import math

import numpy as np

from engine import Econ, best_response, build_schedule, outcome, pure_pool, regret
from scan import xbar_full


def iterate_pool(ec: Econ, q0: tuple[float, float], pool: tuple[tuple[float, float], ...], max_iter: int = 60,
                 tol: float = 1e-8) -> tuple[float, float] | None:
    for damp, budget in ((1.0, max_iter), (0.5, 40)):
        qH, qL = q0
        hist: list[tuple[float, float]] = []
        for _ in range(budget):
            sch = build_schedule(ec, pure_pool(qH, qL, pool))
            bH, _ = best_response(sch, 0)
            bL, _ = best_response(sch, 1)
            if abs(bH - qH) < tol and abs(bL - qL) < tol:
                return float(bH), float(bL)
            if damp == 1.0:
                if len(hist) >= 2 and abs(bH - hist[-2][0]) < 1e-9 and abs(bL - hist[-2][1]) < 1e-9:
                    break
                hist.append((qH, qL))
            qH, qL = qH + damp * (bH - qH), qL + damp * (bL - qL)
    return None


def island_scan(ec: Econ, n_xc: int = 9, y_step: float = 0.5, y_max: float = 6.0,
                widths: tuple[float, ...] = (0.25, 0.5, 1.0, 2.0, math.inf), iterate: bool = True) -> list[dict]:
    """All equilibria found with pool (-inf, x_c) U [y1, y1 + w], plus the half-line cases (no island)."""
    xb = xbar_full(ec)
    top = min(xb, 4.0) if math.isfinite(xb) else 4.0
    xcs = [-math.inf] + list(np.linspace(-1.0, top, n_xc))
    rows = []
    for xc in xcs:
        base = () if xc == -math.inf else ((-math.inf, float(xc)),)
        ys = [None] + [float(y) for y in np.arange(max(xc, -1.0) + y_step if xc != -math.inf else -0.5, y_max + 1e-9, y_step)]
        for y1 in ys:
            for w in (widths if y1 is not None else (0.0,)):
                pool = base if y1 is None else base + ((y1, y1 + w if math.isfinite(w) else math.inf),)
                starts = [(1.0, -1.0)]
                for st in starts:
                    sch = build_schedule(ec, pure_pool(*st, pool))
                    found = []
                    if sch.consistent:
                        rH, rL = regret(sch, *st)
                        if rH <= 1e-9 and rL <= 1e-9:
                            found.append(st)
                    if iterate:
                        fp = iterate_pool(ec, st, pool)
                        if fp is not None and not any(abs(fp[0] - a) < 1e-5 and abs(fp[1] - c) < 1e-5 for a, c in found):
                            sch2 = build_schedule(ec, pure_pool(fp[0], fp[1], pool))
                            if sch2.consistent:
                                rH, rL = regret(sch2, *fp)
                                if rH <= 1e-9 and rL <= 1e-9:
                                    found.append(fp)
                    for q in found:
                        sch3 = build_schedule(ec, pure_pool(q[0], q[1], pool))
                        o = outcome(sch3)
                        rows.append({"x_c": xc, "y1": math.nan if y1 is None else y1, "w": w, "qH": q[0], "qL": q[1],
                                     "E": o.E, "O_H": o.O_H, "eH": o.eH, "pool_prob": o.pool_prob,
                                     "pool_belief": o.pool_belief})
    return rows
