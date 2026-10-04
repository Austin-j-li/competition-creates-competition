"""Lowest entry over all pools under full orders, as a linear program.

Under full orders (1, -1) the pool N may be any Borel set that contains the forced pool Z_0 and has belief
Pr(H | X in N) < tau_L. Entry E and the existence statistic J are linear in the pool's indicator, and so
is the belief constraint (Pr(N|H)(1 - tau_L) - tau_L Pr(N|L) < 0). So

    minimise E(N)   subject to   belief(N) < tau_L,   J(N) >= J_min

is a linear program over cells of the flow line. With J_min = k / (1 - 1/b) the J constraint is the paper's
sufficient test for full orders (A.7), valid for every entry set. The optimum is a lower bound on E over all
full-order equilibria that pass the sufficient test. It is a numerical diagnostic (finite cells). The exact
test can be weaker; exact_floor() tightens J_min until the best-response regret becomes positive.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linprog

from engine import Econ, build_schedule, outcome, pure_pool, regret


def _F(z: float, b: float) -> float:
    return 0.5 * math.exp(z / b) if z <= 0 else 1.0 - 0.5 * math.exp(-z / b)


def cells(ec: Econ, step: float = 0.01, L: float = 14.0) -> dict:
    """Cells of the flow line under full orders with exact edges at the entry thresholds and at +-1."""
    b = ec.b
    xL = 0.5 * b * math.log(ec.tauL / (1 - ec.tauL)) if ec.m < ec.tauL < 1 - ec.m else None
    xH = 0.5 * b * math.log(ec.tauH / (1 - ec.tauH)) if ec.m < ec.tauH < 1 - ec.m else None
    edges = set(np.round(np.arange(-L, L + 1e-9, step), 10).tolist()) | {-1.0, 1.0}
    for v in (xL, xH):
        if v is not None:
            edges.add(float(v))
    e = sorted(edges)
    lo = np.array([-math.inf] + e)
    hi = np.array(e + [math.inf])
    h = np.array([(_F(c - 1, b) if math.isfinite(c) else 1.0) - (_F(a - 1, b) if math.isfinite(a) else 0.0)
                  for a, c in zip(lo, hi)])
    l = np.array([(_F(c + 1, b) if math.isfinite(c) else 1.0) - (_F(a + 1, b) if math.isfinite(a) else 0.0)
                  for a, c in zip(lo, hi)])
    mids = np.array([(a + c) / 2 if math.isfinite(a) and math.isfinite(c) else (c - 1 if math.isfinite(c) else a + 1)
                     for a, c in zip(lo, hi)])
    mu = 1.0 / (1.0 + np.exp(-(np.abs(mids + 1.0) - np.abs(mids - 1.0)) / b))
    ent = ec.rho * (mu >= ec.tauL - 1e-13) + (1 - ec.rho) * (mu >= ec.tauH - 1e-13)
    # exact kappa integrals (Lemma CD.6)
    kap = np.zeros(len(lo))
    for i, (a, c) in enumerate(zip(lo, hi)):
        if c <= -1.0:
            kap[i] = ec.m * ((_F(c + 1, b) if math.isfinite(c) else 1.0) - (_F(a + 1, b) if math.isfinite(a) else 0.0))
        elif a >= 1.0:
            kap[i] = ec.m * ((_F(c - 1, b) if math.isfinite(c) else 1.0) - (_F(a - 1, b) if math.isfinite(a) else 0.0))
        else:
            m1 = 1.0 / (1.0 + math.exp(-2.0 * a / b))
            m2 = 1.0 / (1.0 + math.exp(-2.0 * c / b))
            kap[i] = math.exp(-1.0 / b) / 4.0 * 2.0 * (math.asin(math.sqrt(m2)) - math.asin(math.sqrt(m1)))
    return {"lo": lo, "hi": hi, "h": h, "l": l, "e": ent, "kappa": kap}


def min_entry(ec: Econ, J_min: float, step: float = 0.01, eps: float = 1e-9, objective: str = "E") -> dict | None:
    """Solve the LP. objective 'E' minimises total entry, 'eH' minimises the high type's entry (hence O_H)."""
    c = cells(ec, step)
    n = len(c["h"])
    h, l, e, kap = c["h"], c["l"], c["e"], c["kappa"]
    forced = e == 0.0
    # variables pi_i in [0,1]; forced cells have pi = 1
    cost = -(e * (h + l) / 2.0) if objective == "E" else -(e * h)       # minimise E = E0 - sum pi e mass
    # belief: sum pi (h (1 - tau) - tau l) <= -eps
    A_ub = [h * (1 - ec.tauL) - ec.tauL * l]
    b_ub = [-eps]
    # J: DeltaT sum (1 - pi) e kappa >= J_min  ->  sum pi e kappa <= sum e kappa - J_min / DeltaT
    A_ub.append(e * kap)
    b_ub.append(float((e * kap).sum() - J_min / ec.DeltaT))
    bounds = [(1.0, 1.0) if forced[i] else (0.0, 1.0) for i in range(n)]
    res = linprog(cost, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=bounds, method="highs")
    if res.status != 0:
        return None
    pi = res.x
    E0 = float((e * (h + l) / 2.0).sum())
    E = E0 + float(cost.sum() * 0) - float(((e * (h + l) / 2.0) * pi).sum())
    eH = float((e * h * (1 - pi)).sum())
    return {"pi": pi, "cells": c, "E": E, "eH": eH, "O_H": 0.5 * eH, "E_no_pool": E0,
            "J": float(ec.DeltaT * (e * kap * (1 - pi)).sum()),
            "belief": float((pi * h).sum() / ((pi * h).sum() + (pi * l).sum()))}


def pool_intervals(sol: dict, round_frac: float = 0.5) -> tuple[tuple[float, float], ...]:
    """Merge pooled cells into intervals. Fractional cells are rounded at round_frac."""
    c, pi = sol["cells"], sol["pi"]
    out: list[list[float]] = []
    for a, d, p in zip(c["lo"], c["hi"], pi):
        if p >= round_frac:
            if out and abs(out[-1][1] - a) < 1e-12:
                out[-1][1] = d
            else:
                out.append([a, d])
    return tuple((float(a), float(d)) for a, d in out)


def check_pool(ec: Econ, pool: tuple[tuple[float, float], ...]) -> dict:
    """Build the full-order schedule for this pool and report consistency, regrets, and outcomes."""
    sch = build_schedule(ec, pure_pool(1.0, -1.0, pool))
    rH, rL = regret(sch, 1.0, -1.0)
    o = outcome(sch)
    return {"consistent": sch.consistent, "regret_H": rH, "regret_L": rL, "E": o.E, "O_H": o.O_H, "eH": o.eH,
            "pool_prob": o.pool_prob, "pool_belief": o.pool_belief}


def exact_floor(ec: Econ, J_hi: float, objective: str = "E", iters: int = 22) -> dict | None:
    """Bisect J_min between 0 and J_hi: the smallest J_min whose LP optimum is a full-order equilibrium.

    J_hi must pass (the sufficient test). Returns the best equilibrium found; its E is a numerical
    diagnostic for the infimum of E over full-order equilibria with this pool structure.
    """
    best = None
    lo, hi = 0.0, J_hi
    sol = min_entry(ec, J_hi, objective=objective)
    if sol is None:
        return None
    chk = check_pool(ec, pool_intervals(sol))
    if not (chk["consistent"] and chk["regret_H"] <= 1e-9 and chk["regret_L"] <= 1e-9):
        return None
    best = {**chk, "J_min": J_hi, "pool": pool_intervals(sol)}
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        sol = min_entry(ec, mid, objective=objective)
        if sol is None:
            lo = mid
            continue
        pool = pool_intervals(sol)
        chk = check_pool(ec, pool)
        if chk["consistent"] and chk["regret_H"] <= 1e-9 and chk["regret_L"] <= 1e-9:
            best = {**chk, "J_min": mid, "pool": pool}
            hi = mid
        else:
            lo = mid
    return best
