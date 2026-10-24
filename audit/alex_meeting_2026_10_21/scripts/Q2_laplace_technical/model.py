"""Model objects for the Q2 technical memo (print-only support module).

Auction objects follow eq. (4) of the paper. Posterior, entry and residual
schedules are computed for a pure order profile (q_H, q_L) and any noise law
from noise_laws.py. Entry uses the general rule
    e(mu) = rho 1{B(mu) >= c_L} + (1 - rho) 1{B(mu) >= c_H},
so a failed low-cost floor (possible under Gaussian noise) is handled.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import integrate, optimize, special


@dataclass(frozen=True)
class Primitives:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    rho: float = 0.25
    c_L: float = 1.0
    c_H: float = 6.0
    b: float = 2.0
    k: float = 0.02


BENCH = Primitives()
R0, R1, R2 = 1.2, 3.0, 3.6


def auction(prm: Primitives, r: float) -> dict:
    t0 = prm.p * (1.0 - prm.p / r)
    tH = r / 2.0 + prm.p ** 2 / (2.0 * r)
    tL = prm.ell - (prm.ell ** 2 - prm.p ** 2) / (2.0 * r)
    gH = prm.h - tH
    gL = (prm.ell ** 2 - prm.p ** 2) / (2.0 * r)
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, dT=tH - tL, wL=tL - t0)


def B(prm: Primitives, r: float, mu: float) -> float:
    a = auction(prm, r)
    return a["gL"] + mu * (a["gH"] - a["gL"])


def belief_threshold(prm: Primitives, r: float, cost: float) -> float:
    a = auction(prm, r)
    return (cost - a["gL"]) / (a["gH"] - a["gL"])


def frak_r(ell: float, d: float) -> float:
    return ell + d + math.sqrt(d * d + 2.0 * ell * d)


def logit(x: float) -> float:
    return math.log(x / (1.0 - x))


# ---------------------------------------------------------------- posterior
def log_odds(law, qH: float, qL: float):
    """Flow log-likelihood ratio lambda(x) = log f(x - qH) - log f(x - qL)."""
    return lambda x: law.logpdf(np.asarray(x, dtype=float) - qH) - law.logpdf(np.asarray(x, dtype=float) - qL)


def superlevel_set(fun, c: float, xmax: float = 400.0, n: int = 160001):
    """Intervals where fun(x) >= c, found on a grid and refined by brentq.

    Returns a list of (a, b) with a = -inf or b = +inf for unbounded pieces.
    """
    xs = np.linspace(-xmax, xmax, n)
    g = fun(xs) - c
    inside = g >= 0
    intervals = []
    start = -math.inf if inside[0] else None
    for i in range(1, n):
        if inside[i] and not inside[i - 1]:
            start = optimize.brentq(lambda x: float(fun(x)) - c, xs[i - 1], xs[i], xtol=1e-14)
        elif (not inside[i]) and inside[i - 1]:
            end = optimize.brentq(lambda x: float(fun(x)) - c, xs[i - 1], xs[i], xtol=1e-14)
            intervals.append((start, end))
            start = None
    if start is not None:
        intervals.append((start, math.inf))
    return intervals


def prob_in(law, intervals, shift: float) -> float:
    """Pr(shift + Z in union of intervals)."""
    total = 0.0
    for a, b in intervals:
        sa = 1.0 if a == -math.inf else float(law.sf(a - shift))
        sb = 0.0 if b == math.inf else float(law.sf(b - shift))
        total += sa - sb
    return total


@dataclass
class Outcome:
    tau_H: float
    tau_L: float
    fav_H: list
    fav_L: list
    alpha_H: float
    alpha_L: float
    beta_H: float
    beta_L: float
    E: float
    O_H: float


def outcome(law, prm: Primitives, r: float, qH: float = 1.0, qL: float = -1.0) -> Outcome:
    """Entry and high-value ownership under a fixed pure profile (qH, qL).

    alpha_theta = Pr(mu >= tau_H | theta) (high-cost entry),
    beta_theta  = Pr(mu >= tau_L | theta) (low-cost entry).
    """
    lam = log_odds(law, qH, qL)
    tau_H = belief_threshold(prm, r, prm.c_H)
    tau_L = belief_threshold(prm, r, prm.c_L)

    def fav(tau):
        if tau <= 0.0:
            return [(-math.inf, math.inf)]
        if tau >= 1.0:
            return []
        return superlevel_set(lam, logit(tau))

    fav_H, fav_L = fav(tau_H), fav(tau_L)
    aH, aL = prob_in(law, fav_H, qH), prob_in(law, fav_H, qL)
    bH, bL = prob_in(law, fav_L, qH), prob_in(law, fav_L, qL)
    eH = prm.rho * bH + (1.0 - prm.rho) * aH
    eL = prm.rho * bL + (1.0 - prm.rho) * aL
    return Outcome(tau_H, tau_L, fav_H, fav_L, aH, aL, bH, bL, 0.5 * (eH + eL), 0.5 * eH)


# ------------------------------------------------- fixed-profile deviations
def _integrate_line(fun, points):
    pts = sorted(set(p for p in points if math.isfinite(p)))
    edges = [-math.inf] + pts + [math.inf]
    total, err = 0.0, 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        val, e = integrate.quad(fun, a, b, epsabs=1e-13, epsrel=1e-11, limit=400)
        total += val
        err += e
    return total, err


def deviation_profit(law, prm: Primitives, r: float, qH: float, qL: float, theta: str, q: float):
    """Expected profit of type theta from order q against the schedules of profile (qH, qL).

    Profit = q * int f(x - q) D_theta(x) dx - k|q|, with
    D_H = e(x) dT (1 - mu(x)) and D_L = -e(x) dT mu(x).
    """
    a = auction(prm, r)
    lam = log_odds(law, qH, qL)
    out = outcome(law, prm, r, qH, qL)
    rho = prm.rho

    def entry(x):
        e = 0.0
        if any(lo <= x <= hi for lo, hi in out.fav_L):
            e += rho
        if any(lo <= x <= hi for lo, hi in out.fav_H):
            e += 1.0 - rho
        return e

    def D(x):
        mu = float(special.expit(lam(x)))
        e = entry(x)
        return e * a["dT"] * (1.0 - mu) if theta == "H" else -e * a["dT"] * mu

    pts = [q + kk for kk in law.kinks] + [qH + kk for kk in law.kinks] + [qL + kk for kk in law.kinks]
    for lo, hi in out.fav_H + out.fav_L:
        pts += [lo, hi]
    pts += [q - 30.0, q + 30.0]
    gross, err = _integrate_line(lambda x: math.exp(float(law.logpdf(x - q))) * D(x), pts)
    return q * gross - prm.k * abs(q), q * err
