"""The starved branch (first version; partial.py supersedes it for thresholds, it reuses L_fixed_point and window).

The starved branch: orders (1, -v) with v small enough that the expensive type never enters.

Under pure orders (q_H, q_L) = (1, -v) the largest posterior is M_v = 1 / (1 + e^{-(1+v)/b}). While
M_v < tau_H the expensive type never enters, so e = rho on the entry set and E = rho Pr(entry set) < rho:
the reversal fails. This module finds, for a half-line pool (-inf, x'), the L-type's own fixed point v(x')
by best-response iteration (type H fixed at q_H = 1), then asks when the equilibrium conditions hold:

    A(x') = v(x') - v_H < 0     (starved: M_v < tau_H),  v_H = b logit(tau_H) - 1
    B(x') = mubar(x'; v(x')) - tau_L < 0   (pool consistent)

A is decreasing and B increasing in x', so a starved candidate exists iff x_a <= x_b, where A(x_a) = 0 and
B(x_b) = 0. The threshold in c_L is where x_a = x_b. window() does not check the high type's best response; partial.window_member does, through the engine.
Every candidate must be confirmed with the exact engine (both types' global best responses) before it is reported. Numerical diagnostic.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from engine import Econ, best_response, build_schedule, make_econ, outcome, pool_belief, pure, regret, payoff


def _cut(xp: float) -> float | None:
    return None if xp == -math.inf else xp


def L_fixed_point(ec: Econ, xp: float, v0: float = 0.5, iters: int = 80, tol: float = 1e-10) -> float | None:
    """The L-type's own order -v given H at 1 and the pool (-inf, xp); xp = -inf means no voluntary pool.

    Damped best-response iteration.
    """
    v = v0
    for it in range(iters):
        sch = build_schedule(ec, pure(1.0, -v, _cut(xp)))
        q, _ = best_response(sch, 1)
        nv = -q
        if abs(nv - v) < tol:
            return nv
        v = v + (0.5 if it > 10 else 1.0) * (nv - v)
    return None


def pool_belief_full(ec: Econ, xp: float, v: float) -> float:
    """Pool belief under orders (1, -v): the forced pool united with the voluntary half-line (-inf, xp).

    Taken from the engine's schedule, so a cutoff below the forced end gives the forced pool's own belief.
    """
    sch = build_schedule(ec, pure(1.0, -v, _cut(xp)))
    mb = pool_belief(sch)
    return mb if not math.isnan(mb) else 0.0


def _pool_belief_halfline_only(ec: Econ, xp: float, v: float) -> float:
    """Pr(H | X < xp) under orders (1, -v), ignoring the forced pool (kept for reference)."""
    b = ec.b

    def F(z: float) -> float:
        return 0.5 * math.exp(z / b) if z <= 0 else 1.0 - 0.5 * math.exp(-z / b)
    a, c = F(xp - 1.0), F(xp + v)
    return a / (a + c)


def v_H(ec: Econ) -> float:
    """Largest v with M_v < tau_H (starved bound)."""
    return ec.b * math.log(ec.tauH / (1.0 - ec.tauH)) - 1.0


def _vfun(ec: Econ, xp: float) -> float:
    for v0 in (0.5, 0.2, 0.8, 0.05):
        v = L_fixed_point(ec, xp, v0)
        if v is not None:
            return v
    return math.nan


def window(ec: Econ, lo: float = -1.0, hi: float = 4.0, n: int = 51) -> tuple[float, float] | None:
    """(x_a, x_b), x_a <= x_b, when a starved equilibrium exists on a half-line pool (-inf, x'), else None.

    The grid starts at x' = -inf (no voluntary pool). A(x') = v(x') - v_H and B(x') = pool belief - tau_L
    (B = -1 when the pool is empty) are evaluated on the grid; grid points where the L fixed point does not
    exist are skipped. A window narrower than the grid step is found from the sign changes of A (start of
    the window) and B (end of the window). x_a = -inf means that the pool-free profile is an equilibrium.
    """
    vh = v_H(ec)
    if vh <= 0.0:
        return None
    xs = np.array([-math.inf] + list(np.linspace(lo, hi, n)))
    N = len(xs)
    A = np.full(N, math.nan)
    Bv = np.full(N, math.nan)

    def bel(x: float, v: float) -> float:
        sch = build_schedule(ec, pure(1.0, -v, _cut(x)))
        mb = pool_belief(sch)
        return -1.0 if math.isnan(mb) else mb - ec.tauL

    for i, x in enumerate(xs):
        v = _vfun(ec, float(x))
        if math.isfinite(v):
            A[i] = v - vh
            Bv[i] = bel(float(x), v)
    Af = lambda x: _vfun(ec, x) - vh                       # noqa: E731
    Bf = lambda x: bel(x, _vfun(ec, x))                    # noqa: E731
    feas = np.nonzero((A < 0.0) & (Bv < 0.0))[0]
    if len(feas):
        i0, i1 = int(feas[0]), int(feas[-1])
        x_a = float(xs[i0])
        if i0 > 1 and math.isfinite(A[i0 - 1]) and A[i0 - 1] >= 0.0:
            x_a = brentq(Af, float(xs[i0 - 1]), float(xs[i0]), xtol=1e-9)
        x_b = float(xs[i1])
        if i1 < N - 1 and math.isfinite(Bv[i1 + 1]) and Bv[i1 + 1] >= 0.0 and i1 >= 1:
            x_b = brentq(Bf, float(xs[i1]), float(xs[i1 + 1]), xtol=1e-9)
        return x_a, x_b
    for i in range(1, N - 1):
        if math.isfinite(A[i]) and math.isfinite(A[i + 1]) and A[i] > 0.0 >= A[i + 1]:
            x_a = brentq(Af, float(xs[i]), float(xs[i + 1]), xtol=1e-9)
            if Bf(x_a) < 0.0:
                x_b = float(xs[-1])
                left = x_a
                for j in range(i + 1, N):
                    if math.isfinite(Bv[j]) and Bv[j] >= 0.0:
                        x_b = brentq(Bf, left, float(xs[j]), xtol=1e-9)
                        break
                    if math.isfinite(Bv[j]):
                        left = float(xs[j])
                return x_a, max(x_a, x_b)
    return None


def confirm(ec: Econ, xp: float) -> dict | None:
    """Exact engine check of the starved candidate at cutoff xp."""
    v = L_fixed_point(ec, xp, 0.5)
    if v is None:
        return None
    sch = build_schedule(ec, pure(1.0, -v, _cut(xp)))
    rH, rL = regret(sch, 1.0, -v)
    o = outcome(sch)
    return {"x": xp, "v": v, "consistent": sch.consistent, "regret_H": rH, "regret_L": rL, "E": o.E, "O_H": o.O_H,
            "pool_belief": o.pool_belief, "pool_prob": o.pool_prob, "eH": o.eH}


def cL_threshold(r: float, rho: float, k: float = 0.02, cH: float = 6.0, n: int = 24) -> dict | None:
    """Smallest c_L with a starved equilibrium (existence on a grid, then bisection on the first transition).

    The grid starts in regime I (c_L = B(m) - 0.05). Existence need not be monotone in c_L, so the result also
    reports whether every later grid point has a starved equilibrium. None when none exists on the grid.
    """
    ec0 = make_econ(r, rho, 1.0, cH, k=k)
    cm = ec0.gL + ec0.m * (ec0.gH - ec0.gL)
    ch = ec0.gL + 0.5 * (ec0.gH - ec0.gL)
    grid = [cm - 0.05] + list(np.linspace(cm + 1e-3, ch - 1e-6, n - 1))
    flags = [window(make_econ(r, rho, float(c), cH, k=k)) is not None for c in grid]
    if not any(flags):
        return None
    i = flags.index(True)
    if i == 0:
        return {"cL_star": cm, "regime_I": True, "monotone": all(flags), "window": None}
    a, b_ = float(grid[i - 1]), float(grid[i])
    for _ in range(40):
        mid = 0.5 * (a + b_)
        if window(make_econ(r, rho, mid, cH, k=k)) is not None:
            b_ = mid
        else:
            a = mid
    ec = make_econ(r, rho, b_, cH, k=k)
    w = window(ec)
    return {"cL_star": b_, "regime_I": False, "monotone": all(flags[i:]), "window": w}
