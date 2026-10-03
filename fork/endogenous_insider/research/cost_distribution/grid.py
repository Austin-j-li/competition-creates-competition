"""Grid best-response checks for pure-order profiles under a general cost law G.

This module generalizes the fork's solver to any CostLaw. A candidate continuation is fixed by pure
orders (q_H, q_L) and a pool: the forced pool Z_0 = {x : G(B_r(mu_X(x))) = 0}, optionally enlarged by a
half-line (-inf, cutoff). Off the pool the price reveals mu_X and entry is G(B_r(mu_X)). The investor's
best response is searched on an order grid against that fixed schedule. Every row it produces is a
numerical diagnostic: a fixed point of a best-response map on a grid, not a certified enclosure.
Nothing here writes files.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from core import CostLaw, Payoffs, Primitives, cost_cdf, gross_profit, payoffs


@dataclass(frozen=True)
class Grid:
    x: np.ndarray
    dx: float
    s: np.ndarray
    kernel: np.ndarray  # kernel[i, j] = f(x_j - s_i)


@dataclass(frozen=True)
class FixedPoint:
    qH: float
    qL: float
    U_H: float
    U_L: float
    eH: float
    eL: float
    E: float
    O_H: float
    pool_prob: float
    pool_belief: float
    pool_ok: bool
    iterations: int


def make_grid(prim: Primitives, half_width: float = 30.0, n_flow: int = 60001, n_orders: int = 201) -> Grid:
    x = np.linspace(-half_width, half_width, n_flow)
    s = np.round(np.linspace(-1.0, 1.0, n_orders), 4)
    kernel = np.exp(-np.abs(x[None, :] - s[:, None]) / prim.b) / (2.0 * prim.b)
    return Grid(x=x, dx=float(x[1] - x[0]), s=s, kernel=kernel)


def _density(prim: Primitives, z: np.ndarray) -> np.ndarray:
    return np.exp(-np.abs(z) / prim.b) / (2.0 * prim.b)


def schedule(prim: Primitives, grid: Grid, pay: Payoffs, law: CostLaw, qH: float, qL: float,
             cutoff: float = -math.inf) -> dict:
    """Candidate continuation at pure orders (qH, qL) with pool Z_0 union (-inf, cutoff)."""
    aH, aL = _density(prim, grid.x - qH), _density(prim, grid.x - qL)
    mu = aH / (aH + aL)
    e_sep = np.asarray(cost_cdf(prim, law, gross_profit(prim, pay, mu)))
    pool = (e_sep <= 0.0) | (grid.x < cutoff)
    e = np.where(pool, 0.0, e_sep)
    if pool.any():
        wH, wL = float(aH[pool].sum()), float(aL[pool].sum())
        mubar = wH / (wH + wL)
        pool_ok = float(cost_cdf(prim, law, gross_profit(prim, pay, mubar))) == 0.0
        pool_prob = 0.5 * (wH + wL) * grid.dx
    else:
        mubar, pool_ok, pool_prob = float("nan"), True, 0.0
    price = pay.t0 + e * (pay.wL + pay.DeltaT * mu)
    VH = pay.t0 + e * (pay.tH - pay.t0)
    VL = pay.t0 + e * (pay.tL - pay.t0)
    eH = float((e * aH).sum() * grid.dx)
    eL = float((e * aL).sum() * grid.dx)
    return {"price": price, "VH": VH, "VL": VL, "eH": eH, "eL": eL, "mubar": mubar, "pool_ok": pool_ok,
            "pool_prob": pool_prob}


def best_response(prim: Primitives, grid: Grid, gain: np.ndarray) -> tuple[float, float]:
    """Global best response against a fixed schedule: coarse order grid, then a local refinement."""
    coarse = grid.s * (grid.kernel @ gain) * grid.dx - prim.k * np.abs(grid.s)
    i = int(coarse.argmax())
    lo, hi = max(-1.0, grid.s[i] - 0.01), min(1.0, grid.s[i] + 0.01)
    fine = np.linspace(lo, hi, 41)
    vals = np.array([s * (_density(prim, grid.x - s) * gain).sum() * grid.dx - prim.k * abs(s) for s in fine])
    j = int(vals.argmax())
    if vals[j] <= 0.0:
        return 0.0, 0.0
    return float(fine[j]), float(vals[j])


def iterate(prim: Primitives, grid: Grid, r: float, law: CostLaw, qH: float, qL: float,
            cutoff: float = -math.inf, max_iter: int = 80, tol: float = 5e-4) -> FixedPoint | None:
    """Best-response iteration from (qH, qL) against recomputed schedules; None if no fixed point."""
    pay = payoffs(prim, r)
    for it in range(max_iter):
        sch = schedule(prim, grid, pay, law, qH, qL, cutoff)
        bH, uH = best_response(prim, grid, sch["VH"] - sch["price"])
        bL, uL = best_response(prim, grid, sch["VL"] - sch["price"])
        if abs(bH - qH) < tol and abs(bL - qL) < tol:
            if not sch["pool_ok"]:
                return None
            return FixedPoint(qH=qH, qL=qL, U_H=uH, U_L=uL, eH=sch["eH"], eL=sch["eL"],
                              E=0.5 * (sch["eH"] + sch["eL"]), O_H=0.5 * sch["eH"], pool_prob=sch["pool_prob"],
                              pool_belief=sch["mubar"], pool_ok=sch["pool_ok"], iterations=it)
        qH, qL = bH, bL
    return None
