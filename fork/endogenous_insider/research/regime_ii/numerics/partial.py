"""Partial-order equilibria with a half-line pool, and the lowest c_L at which one breaks the reversal.

This replaces the first-order version in starved.py. That version assumed the high type buys 1 and never checked
it; at some (r1, rho) the high type then wants a smaller order and the candidate is not an equilibrium. Here every
candidate is confirmed by the engine: pool belief below tau_L, global best response of both types (regret at most
1e-9). Any short size v is allowed, not only v below the starved bound v_H.

Family: pure orders (1, -v) and the pool (-inf, x') united with the forced pool. For each cutoff x' the low type's
own order v is a fixed point of its best response (found from several starts, so more than one branch can appear).
Along each branch the pool belief grows with x'. The lowest entry on a branch sits at the largest consistent x',
so each branch is followed to the end of its consistent range by bisection. A branch member breaks the reversal
when E <= rho or O_H <= rho/2 (the values at r0).

Numerical diagnostic. It sees half-line pools and pure orders only; islands are in knapsack.py and pool_lp.py.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from engine import Econ, best_response, build_schedule, entry_at_belief, make_econ, outcome, pure, regret
from search import iterate_pure, make_candidate
import starved
from starved import L_fixed_point, _cut

TOL = 1e-9
BACKOFF = 1e-5        # members are placed this far inside the consistent range: the belief bound is strict
STARTS = (0.85, 0.6, 0.35, 0.1)          # full orders (v = 1) are handled by the knapsack module


def _member(ec: Econ, x: float, v: float) -> dict | None:
    """Engine check of the profile (1, -v) with pool (-inf, x). None when it is not an equilibrium."""
    sch = build_schedule(ec, pure(1.0, -v, _cut(x)))
    if not sch.consistent:
        return None
    rH, rL = regret(sch, 1.0, -v)
    if rH > TOL or rL > TOL:
        return None
    o = outcome(sch)
    return {"x": x, "v": v, "E": float(o.E), "O_H": float(o.O_H), "eH": float(o.eH), "regret_H": rH, "regret_L": rL,
            "pool_belief": float(o.pool_belief) if not math.isnan(o.pool_belief) else math.nan}


def _consistent(ec: Econ, x: float, v: float) -> bool:
    return build_schedule(ec, pure(1.0, -v, _cut(x))).consistent


def weak_values(ec: Econ) -> tuple[float, float]:
    """E(r0) and O_H(r0) for the same (rho, c_L, c_H): the no-trade benchmark at r0 = 1.2."""
    ecw = make_econ(1.2, ec.rho, ec.cL, ec.cH, k=ec.k)
    e = entry_at_belief(ecw, 0.5)
    return e, 0.5 * e


def breaks(ec: Econ, m: dict) -> bool:
    e_w, o_w = weak_values(ec)
    return not (m["E"] > e_w + 1e-12 and m["O_H"] > o_w + 1e-12)


def fixed_points(ec: Econ, x: float) -> list[float]:
    """Distinct short sizes v < 0.99 that are fixed points of the low type's best response (H at 1, pool (-inf, x))."""
    out: list[float] = []
    for s0 in STARTS:
        v = L_fixed_point(ec, x, s0)
        if v is not None and v < 0.99 and all(abs(v - u) > 1e-6 for u in out):
            out.append(v)
    return out


def _end_of_branch(ec: Econ, a: float, va: float, b: float) -> tuple[float, float]:
    """Bisect for the largest consistent cutoff between a (consistent, short va) and b (not), staying on the branch."""
    for _ in range(30):
        mid = 0.5 * ((a if math.isfinite(a) else b - 1.0) + b)
        vm = L_fixed_point(ec, mid, va)
        if vm is not None and abs(vm - va) < 0.25 and _consistent(ec, mid, vm):
            a, va = mid, vm
        else:
            b = mid
    return a, va


def failure_at(ec: Econ, n: int = 31, lo: float = -1.0, hi: float = 3.5) -> dict | None:
    """The partial-order equilibrium with the lowest E that breaks the reversal at this c_L, or None."""
    xs = [-math.inf] + [float(x) for x in np.linspace(lo, hi, n)]
    best = None

    def consider(x: float, v: float) -> None:
        nonlocal best
        m = _member(ec, x, v)
        if m is not None and breaks(ec, m) and (best is None or m["E"] < best["E"]):
            best = m

    prev: list[tuple[float, float]] = []           # consistent (x, v) at the previous grid point
    for x in xs:
        now = []
        for v in fixed_points(ec, x):
            if _consistent(ec, x, v):
                now.append((x, v))
                consider(x, v)
        for (xa, va) in prev:                       # a branch that ended between the two grid points
            if not any(abs(va - v2) < 0.25 for _, v2 in now):
                a, vb = _end_of_branch(ec, xa, va, x)
                if math.isfinite(a):
                    a_in = a - BACKOFF * (1.0 + abs(a))        # stay strictly inside the consistent range
                    v_in = L_fixed_point(ec, a_in, vb)
                    if v_in is not None:
                        consider(a_in, v_in)
        prev = now
    return best


def window_member(ec: Econ) -> dict | None:
    """Breaking member inside the starved window (x_a, x_b) of starved.py, confirmed by the engine (both types).

    The window can be narrower than any cutoff grid, so the candidates are placed at its two ends and its middle.
    starved.window alone is not enough: it does not check the high type, which at some (r1, rho) prefers less than 1.
    """
    w = starved.window(ec)
    if w is None:
        return None
    xa, xb = w
    cands = [xb - BACKOFF * (1.0 + abs(xb))]
    if math.isfinite(xa):
        cands += [0.5 * (xa + xb), xa + BACKOFF * (1.0 + abs(xa))]
    else:
        cands += [-math.inf]
    best = None
    for x in cands:
        v = L_fixed_point(ec, x, 0.5)
        if v is None:
            continue
        m = _member(ec, x, v)
        if m is not None and breaks(ec, m) and (best is None or m["E"] < best["E"]):
            best = m
    return best


LOW_STARTS = ((0.0, 0.0), (0.25, -0.25), (0.05, -0.05), (0.15, -0.15), (0.3, -0.3), (0.5, -0.5), (0.75, -0.75))


def _low_member(ec: Econ, qH: float, qL: float, start: tuple[float, float], it: int) -> dict | None:
    c = make_candidate(ec, qH, qL, None, "pure", it, start)
    if not (c.consistent and c.regret_H <= TOL and c.regret_L <= TOL):
        return None
    m = {"x": -math.inf, "v": -c.qL, "qH": c.qH, "E": float(c.out.E), "O_H": float(c.out.O_H),
         "eH": float(c.out.eH), "regret_H": c.regret_H, "regret_L": c.regret_L,
         "pool_belief": float(c.out.pool_belief) if not math.isnan(c.out.pool_belief) else math.nan}
    return m if breaks(ec, m) else None


def low_trade_member(ec: Econ) -> dict | None:
    """A low-trade equilibrium that breaks the reversal: both types order less than the full size, minimal pool.

    With small orders the posterior stays inside (tau_L, tau_H), so only the cheap type enters and E = rho and
    O_H = rho/2 exactly (the values at r0). It exists when rho Delta_T is a little above 2k. Its basin under
    best-response iteration is narrow, so two searches are used: (a) the symmetric profiles (q, -q) on a grid, where
    a sign change of BR_H(q) - q is refined by root finding; (b) best-response iteration from small starts.
    Every member is confirmed by the engine (both types, global best response).
    """
    best = None

    def keep(m: dict | None) -> None:
        nonlocal best
        if m is not None and (best is None or m["E"] < best["E"]):
            best = m

    qs = np.linspace(0.01, 0.99, 50)

    def h(q: float) -> float:
        return best_response(build_schedule(ec, pure(q, -q, None)), 0)[0] - q

    vals = [h(float(q)) for q in qs]
    for i in range(len(qs) - 1):
        if vals[i] * vals[i + 1] < 0.0:
            try:
                q = brentq(h, float(qs[i]), float(qs[i + 1]), xtol=1e-12)
            except ValueError:
                continue
            keep(_low_member(ec, q, -q, (q, -q), 0))
    for st in LOW_STARTS:
        fp = iterate_pure(ec, st, None)
        if fp is not None and 1e-6 < fp[0] <= 0.99:
            keep(_low_member(ec, fp[0], fp[1], st, fp[2]))
    return best


def combined_failure(ec: Econ) -> dict | None:
    """A breaking equilibrium from the cutoff grid, the starved window or the low-trade family, else None.

    Returns the one with the lowest E, and names the family under the key 'kind'.
    """
    found = []
    for kind, fn in (("partial", failure_at), ("window", window_member), ("lowtrade", low_trade_member)):
        m = fn(ec)
        if m is not None:
            found.append({**m, "kind": kind})
    return min(found, key=lambda m: m["E"]) if found else None


def cL_threshold(r: float, rho: float, k: float = 0.02, cH: float = 6.0, n: int = 12, steps: int = 18) -> dict:
    """Smallest c_L in regime II with a breaking partial equilibrium (grid, then bisection on the first transition).

    cL_star is nan when none is found on the grid. 'monotone' tells whether every later grid point also has one.
    """
    ec0 = make_econ(r, rho, 1.0, cH, k=k)
    cm = ec0.gL + ec0.m * (ec0.gH - ec0.gL)
    ch = ec0.gL + 0.5 * (ec0.gH - ec0.gL)
    grid = [float(c) for c in np.linspace(cm + 1e-3, ch - 1e-6, n)]
    flags = [combined_failure(make_econ(r, rho, c, cH, k=k)) is not None for c in grid]
    if not any(flags):
        return {"cL_star": math.nan, "monotone": True, "member": None}
    i = flags.index(True)
    if i == 0:
        mem = combined_failure(make_econ(r, rho, grid[0], cH, k=k))
        return {"cL_star": cm, "monotone": all(flags), "member": mem}
    a, b = grid[i - 1], grid[i]
    for _ in range(steps):
        mid = 0.5 * (a + b)
        if combined_failure(make_econ(r, rho, mid, cH, k=k)) is not None:
            b = mid
        else:
            a = mid
    return {"cL_star": b, "monotone": all(flags[i:]), "member": combined_failure(make_econ(r, rho, b, cH, k=k))}


def hold_intervals(r: float, rho: float, k: float = 0.02, cH: float = 6.0, n: int = 14, steps: int = 18) -> dict:
    """Intervals of c_L in regime II where no breaking equilibrium of these families is found.

    Flags on a grid of n points across (B(m), B(1/2)); every flag change is located by bisection. Returns the hold
    intervals as (lo, hi) pairs, the flags, and the member at the first break above a hold interval (if any).
    """
    ec0 = make_econ(r, rho, 1.0, cH, k=k)
    cm = ec0.gL + ec0.m * (ec0.gH - ec0.gL)
    ch = ec0.gL + 0.5 * (ec0.gH - ec0.gL)
    grid = [float(c) for c in np.linspace(cm + 1e-3, ch - 1e-6, n)]
    mem = [combined_failure(make_econ(r, rho, c, cH, k=k)) for c in grid]
    flags = [m is not None for m in mem]

    def edge(a: float, b: float, fa: bool) -> float:
        for _ in range(steps):
            mid = 0.5 * (a + b)
            if (combined_failure(make_econ(r, rho, mid, cH, k=k)) is not None) == fa:
                a = mid
            else:
                b = mid
        return 0.5 * (a + b)

    holds: list[tuple[float, float]] = []
    start = cm if not flags[0] else None
    first_break = None
    for i in range(1, n):
        if flags[i] != flags[i - 1]:
            e = edge(grid[i - 1], grid[i], flags[i - 1])
            if flags[i]:                              # hold -> break at e
                if start is not None:
                    holds.append((start, e))
                    if first_break is None:
                        first_break = (e, mem[i])
                start = None
            else:                                     # break -> hold at e
                start = e
    if start is not None:
        holds.append((start, ch))
    return {"holds": holds, "flags": flags, "first_break": first_break, "cm": cm, "ch": ch, "grid": grid, "members": mem}
