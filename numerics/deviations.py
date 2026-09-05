"""Unilateral-deviation evaluation (eq. 12, OA.57): U_theta(s) against a fixed schedule."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .information import Schedule
from .params import Noise
from .quadrature import convolve_full_line


@dataclass(frozen=True)
class Convolution:
    value: float
    error: float
    tail_bound: float


def _exterior_constants(sched: Schedule, state: str) -> tuple[float | None, float | None]:
    if sched.prim.noise != Noise.LAPLACE:
        return None, None
    lo, hi = sched.hull()
    bps = [p for p in sched.breakpoints]
    lo = min([lo, *bps])
    hi = max([hi, *bps])
    aL = float(sched.A(np.array([lo - 1.0]), state)[0])
    aR = float(sched.A(np.array([hi + 1.0]), state)[0])
    return aL, aR


def _hull_ext(sched: Schedule) -> tuple[float, float]:
    lo, hi = sched.hull()
    bps = list(sched.breakpoints)
    return min([lo, *bps]), max([hi, *bps])


def F(sched: Schedule, state: str, s: float, n: int = 48, tail_target: float = 1e-14) -> Convolution:
    """F_eps(s) = int f(x - eps s) A_eps(x) dx with eps = +1 for H (buy), -1 for L (sell)."""
    eps = 1.0 if state == "H" else -1.0
    b = sched.prim.fb
    center = eps * s
    cl, cr = _exterior_constants(sched, state)
    v, e, tb = convolve_full_line(sched.prim.noise, b, "pdf", 1.0, lambda x: sched.A(x, state), list(sched.breakpoints),
                                  center, _hull_ext(sched), cl, cr, n=n, tail_target=tail_target,
                                  A_bar=sched.pay.Delta_T)
    return Convolution(v, e, tb)


def dF(sched: Schedule, state: str, s: float, n: int = 48, tail_target: float = 1e-14) -> Convolution:
    """F_eps'(s) = -eps int f'(x - eps s) A_eps(x) dx (OA.12)."""
    eps = 1.0 if state == "H" else -1.0
    b = sched.prim.fb
    center = eps * s
    cl, cr = _exterior_constants(sched, state)
    v, e, tb = convolve_full_line(sched.prim.noise, b, "dpdf", -eps, lambda x: sched.A(x, state), list(sched.breakpoints),
                                  center, _hull_ext(sched), cl, cr, n=n, tail_target=tail_target,
                                  A_bar=sched.pay.Delta_T / b)
    return Convolution(v, e, tb)


def U(sched: Schedule, state: str, q: float, n: int = 48) -> Convolution:
    """Expected trading profit of a unilateral order q (any sign) against the schedule.

    For a correctly signed magnitude s = |q|: s F_eps(s) - k s. For a wrong-signed order the
    gross payoff is -s int f(x + eps s) A_eps(x) dx and the cost is still paid.
    """
    k = sched.prim.fk
    if q == 0.0:
        return Convolution(0.0, 0.0, 0.0)
    eps = 1.0 if state == "H" else -1.0
    s = abs(q)
    correct = (q > 0) == (eps > 0)
    b = sched.prim.fb
    center = q  # the order actually placed shifts the flow by q
    cl, cr = _exterior_constants(sched, state)
    v, e, tb = convolve_full_line(sched.prim.noise, b, "pdf", 1.0, lambda x: sched.A(x, state), list(sched.breakpoints),
                                  center, _hull_ext(sched), cl, cr, n=n, A_bar=sched.pay.Delta_T)
    gross = s * v if correct else -s * v
    return Convolution(gross - k * s, s * e, s * tb)


def dU(sched: Schedule, state: str, s: float, n: int = 48) -> Convolution:
    """U_eps'(s) = F(s) + s F'(s) - k for a correctly signed magnitude s."""
    f = F(sched, state, s, n)
    df = dF(sched, state, s, n)
    return Convolution(f.value + s * df.value - sched.prim.fk, f.error + s * df.error, f.tail_bound + s * df.tail_bound)


def payoff_of_profile(sched: Schedule, state: str, n: int = 48) -> Convolution:
    """Expected payoff of the candidate's own (possibly mixed) order in `state`."""
    qs, ws = (sched.profile.q_H, sched.profile.w_H) if state == "H" else (sched.profile.q_L, sched.profile.w_L)
    tot, err, tb = 0.0, 0.0, 0.0
    for q, w in zip(qs, ws):
        if w > 0:
            u = U(sched, state, q, n)
            tot += w * u.value
            err += w * u.error
            tb += w * u.tail_bound
    return Convolution(tot, err, tb)


def order_grid(intervals: int) -> np.ndarray:
    return np.linspace(-1.0, 1.0, intervals + 1)


def deviation_scan(sched: Schedule, state: str, intervals: int, extra_points: list[float] | None = None,
                   n: int = 48) -> dict:
    """Evaluate U(q) on the declared grid plus special points; return arrays and the maximal gain."""
    qs = list(order_grid(intervals))
    if extra_points:
        qs.extend([float(x) for x in extra_points if -1.0 <= x <= 1.0])
    qs = sorted(set(qs))
    base = payoff_of_profile(sched, state, n)
    rows = []
    for q in qs:
        u = U(sched, state, q, n)
        rows.append((q, u.value, base.value, u.value - base.value, u.error + base.error, u.tail_bound + base.tail_bound))
    gains = np.array([r[3] for r in rows])
    return {"rows": rows, "max_gain": float(gains.max()), "argmax_q": float(qs[int(gains.argmax())]),
            "candidate_payoff": base.value}
