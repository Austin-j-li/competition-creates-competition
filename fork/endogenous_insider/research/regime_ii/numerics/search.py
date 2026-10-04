"""Equilibrium search for the two-point-cost economy. Returns candidates; verify.py accepts or rejects.

Layers. (1) best-response iteration for pure orders under a half-line voluntary pool (cutoff family),
from many starts. (2) a 2D regret scan over a pure-order lattice for a fixed pool, which finds fixed points
that best-response iteration cannot reach (unstable ones). (3) mixed profiles with small supports.
Every record here is a numerical diagnostic. A search never assigns "accepted".
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from engine import (Econ, Profile, Schedule, best_response, build_schedule, outcome, payoff, pure, regret,
                    Outcome, no_trade_exists)

# starts: (qH, qL). Zero start, full, interior, one-sided, and both wrong-signed starts.
STARTS: tuple[tuple[float, float], ...] = (
    (1.0, -1.0), (1.0, -0.5), (1.0, 0.0), (0.5, -0.5), (0.25, -0.25), (0.0, 0.0), (0.05, -0.05), (0.5, 0.0),
    (0.0, -0.5), (0.75, -1.0), (0.3, -1.0), (1.0, -0.25), (0.6, -0.9), (-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5),
)


@dataclass(frozen=True)
class Candidate:
    """One candidate equilibrium: pure orders plus a voluntary-pool cutoff (-inf for the minimal pool)."""
    family: str
    cutoff: float
    qH: float
    qL: float
    consistent: bool
    regret_H: float
    regret_L: float
    out: Outcome
    pool_end: float            # upper end of the zero-entry half-line (forced plus voluntary)
    iterations: int
    start: tuple[float, float]


def pool_end_of(sch: Schedule) -> float:
    """Upper end of the leftmost zero-entry run of panels (the half-line pool); -inf if no pool."""
    if sch.e[0] > 0.0:
        return -math.inf
    nz = np.nonzero(sch.e > 0.0)[0]
    return float(sch.edges[nz[0]]) if len(nz) else math.inf


def iterate_pure(ec: Econ, q0: tuple[float, float], cutoff: float | None, max_iter: int = 60,
                 tol: float = 1e-8) -> tuple[float, float, int] | None:
    """Best-response iteration. Undamped first (with 2-cycle detection), then damped.

    Returns (qH, qL, iterations) at a fixed point of the best-response map, or None.
    """
    for damp, budget in ((1.0, max_iter), (0.5, 40)):
        qH, qL = q0
        hist: list[tuple[float, float]] = []
        for it in range(budget):
            sch = build_schedule(ec, pure(qH, qL, cutoff))
            bH, _ = best_response(sch, 0)
            bL, _ = best_response(sch, 1)
            if abs(bH - qH) < tol and abs(bL - qL) < tol:
                return float(bH), float(bL), it
            if damp == 1.0:
                if len(hist) >= 2 and abs(bH - hist[-2][0]) < 1e-9 and abs(bL - hist[-2][1]) < 1e-9:
                    break      # 2-cycle: switch to damping
                hist.append((qH, qL))
            qH, qL = qH + damp * (bH - qH), qL + damp * (bL - qL)
    return None


def make_candidate(ec: Econ, qH: float, qL: float, cutoff: float | None, family: str, iters: int,
                   start: tuple[float, float]) -> Candidate:
    sch = build_schedule(ec, pure(qH, qL, cutoff))
    rH, rL = regret(sch, qH, qL)
    return Candidate(family=family, cutoff=-math.inf if cutoff is None else float(cutoff), qH=qH, qL=qL,
                     consistent=sch.consistent, regret_H=rH, regret_L=rL, out=outcome(sch),
                     pool_end=pool_end_of(sch), iterations=iters, start=start)


def search_cutoff(ec: Econ, cutoff: float | None, starts: tuple[tuple[float, float], ...] = STARTS,
                  extra: tuple[tuple[float, float], ...] = (), reg_tol: float = 1e-9) -> tuple[list[Candidate], int]:
    """All pure fixed points found at one cutoff, and the number of starts that did not converge."""
    found: list[Candidate] = []
    unresolved = 0
    for st in tuple(starts) + tuple(extra):
        res = iterate_pure(ec, st, cutoff)
        if res is None:
            unresolved += 1
            continue
        qH, qL, it = res
        if abs(qH) < 1e-9 and abs(qL) < 1e-9 and not no_trade_exists(ec):
            # zero orders can pass the grid test only if the schedule gives no gain; keep it and let regret decide
            pass
        if any(abs(qH - c.qH) < 1e-5 and abs(qL - c.qL) < 1e-5 for c in found):
            continue
        cand = make_candidate(ec, qH, qL, cutoff, "pure", it, st)
        if cand.consistent and cand.regret_H <= reg_tol and cand.regret_L <= reg_tol:
            found.append(cand)
    return found, unresolved


def regret_scan(ec: Econ, cutoff: float | None, n: int = 21, top: int = 12) -> list[tuple[float, float, float]]:
    """Lattice scan of total regret over pure orders (qH in [0,1], qL in [-1,0]) under one pool.

    Returns the `top` lowest-regret lattice points as (qH, qL, regret). Used as a cross-check on the
    best-response search: every equilibrium should sit next to a low-regret lattice point.
    """
    rows = []
    for qH in np.linspace(0.0, 1.0, n):
        for qL in np.linspace(-1.0, 0.0, n):
            sch = build_schedule(ec, pure(qH, qL, cutoff))
            if not sch.consistent:
                continue
            rH, rL = regret(sch, float(qH), float(qL))
            rows.append((float(qH), float(qL), rH + rL))
    rows.sort(key=lambda t: t[2])
    return rows[:top]
