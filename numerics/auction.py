"""Auction-payoff layer (main text eq. 4, OA.50 to OA.52, OA.44).

Closed forms and an independent integration oracle over the uniform incumbent.
All functions are pure and take the primitive record first.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy import integrate

from .params import Primitives


@dataclass(frozen=True)
class AuctionPayoffs:
    r: float
    p: float
    t_0: float
    t_H: float
    t_L: float
    g_H: float
    g_L: float

    @property
    def Delta_T(self) -> float:
        return self.t_H - self.t_L

    @property
    def w_H(self) -> float:
        return self.t_H - self.t_0

    @property
    def w_L(self) -> float:
        return self.t_L - self.t_0

    def B(self, mu: float) -> float:
        """Gross challenger profit at posterior mu."""
        return self.g_L + mu * (self.g_H - self.g_L)

    def tau(self, c_H: float) -> float:
        """Expensive-entry posterior threshold (may fall outside (0,1))."""
        if self.g_H == self.g_L:
            return float("inf") if c_H > self.g_L else float("-inf")
        return (c_H - self.g_L) / (self.g_H - self.g_L)


# --- pointwise realized outcomes, OA.50 ---------------------------------------
def T_realized(R: np.ndarray, v: float, p: float) -> np.ndarray:
    """Target proceeds given incumbent value R, challenger value v (entered), reserve p."""
    R = np.asarray(R, dtype=float)
    if v < p:
        return np.where(R >= p, p, 0.0)
    return np.maximum(p, np.minimum(R, v))


def G_realized(R: np.ndarray, v: float, p: float) -> np.ndarray:
    """Challenger gross acquisition profit (v - max(p, R))_+."""
    R = np.asarray(R, dtype=float)
    return np.maximum(v - np.maximum(p, R), 0.0)


def T0_realized(R: np.ndarray, p: float) -> np.ndarray:
    R = np.asarray(R, dtype=float)
    return np.where(R >= p, p, 0.0)


# --- closed forms -----------------------------------------------------------------
def kernel_uniform(r: float, v: float, p: float) -> tuple[float, float]:
    """(t_v, g_v) for uniform R on [0, r] and fixed challenger value v: OA.51."""
    t_0 = p * (1 - p / r) if p <= r else 0.0
    if v < p:
        return t_0, 0.0
    if v < r:  # p <= v < r
        return v - (v * v - p * p) / (2 * r), (v * v - p * p) / (2 * r)
    if p <= r <= v:
        t_v = r / 2 + p * p / (2 * r)
        return t_v, v - t_v
    # r < p <= v
    return p, v - p


def payoffs_closed_form(prim: Primitives, r: float, p: float | None = None) -> AuctionPayoffs:
    """Binary-value payoffs at reserve p (default declared p) using OA.51 for each value."""
    p = prim.fp if p is None else p
    h, ell = prim.fh, prim.fell
    t_0 = p * (1 - p / r) if p <= r else 0.0
    t_H, g_H = kernel_uniform(r, h, p)
    t_L, g_L = kernel_uniform(r, ell, p)
    return AuctionPayoffs(r=r, p=p, t_0=t_0, t_H=t_H, t_L=t_L, g_H=g_H, g_L=g_L)


def payoffs_benchmark_formula(prim: Primitives, r: float) -> AuctionPayoffs:
    """Main-text eq. (4), valid for 0 < p < ell < r < h."""
    p, ell, h = prim.fp, prim.fell, prim.fh
    return AuctionPayoffs(
        r=r, p=p,
        t_0=p * (1 - p / r),
        t_H=r / 2 + p * p / (2 * r),
        t_L=ell - (ell * ell - p * p) / (2 * r),
        g_H=h - r / 2 - p * p / (2 * r),
        g_L=(ell * ell - p * p) / (2 * r),
    )


def Delta_T_formula(prim: Primitives, r: float) -> float:
    ell = prim.fell
    return (r - ell) ** 2 / (2 * r)


def dDelta_T_dr(prim: Primitives, r: float) -> float:
    return 0.5 - prim.fell ** 2 / (2 * r * r)


def dB_dr(prim: Primitives, r: float, mu: float) -> float:
    """d B_r(mu) / dr using eq. (5)."""
    p, ell = prim.fp, prim.fell
    gH_p = -0.5 + p * p / (2 * r * r)
    gL_p = -(ell * ell - p * p) / (2 * r * r)
    return gL_p + mu * (gH_p - gL_p)


# --- independent integration oracle -------------------------------------------
def _integrate_uniform(fun: Callable[[np.ndarray], np.ndarray], r: float, splits: list[float],
                       epsabs: float, epsrel: float) -> tuple[float, float]:
    pts = sorted({0.0, r, *[s for s in splits if 0.0 < s < r]})
    total, err = 0.0, 0.0
    for a, b_ in zip(pts[:-1], pts[1:]):
        val, e = integrate.quad(lambda u: float(fun(np.array([u]))[0]), a, b_,
                                epsabs=epsabs, epsrel=epsrel, limit=200)
        total += val
        err += e
    return total / r, err / r


def payoffs_integrated(prim: Primitives, r: float, p: float | None = None,
                       epsabs: float = 1e-13, epsrel: float = 1e-13) -> tuple[AuctionPayoffs, float]:
    """Integrate OA.50 over R ~ U[0, r], splitting at p and at each value. Returns (payoffs, err)."""
    p = prim.fp if p is None else p
    h, ell = prim.fh, prim.fell
    splits = [p, ell, h]
    t_0, e0 = _integrate_uniform(lambda R: T0_realized(R, p), r, splits, epsabs, epsrel)
    t_H, e1 = _integrate_uniform(lambda R: T_realized(R, h, p), r, splits, epsabs, epsrel)
    t_L, e2 = _integrate_uniform(lambda R: T_realized(R, ell, p), r, splits, epsabs, epsrel)
    g_H, e3 = _integrate_uniform(lambda R: G_realized(R, h, p), r, splits, epsabs, epsrel)
    g_L, e4 = _integrate_uniform(lambda R: G_realized(R, ell, p), r, splits, epsabs, epsrel)
    return AuctionPayoffs(r=r, p=p, t_0=t_0, t_H=t_H, t_L=t_L, g_H=g_H, g_L=g_L), max(e0, e1, e2, e3, e4)


def payoffs_class_integrated(prim: Primitives, r: float, p: float, eps_V: float,
                             epsabs: float = 1e-13, epsrel: float = 1e-13) -> tuple[AuctionPayoffs, float]:
    """Atomless-value class economy: integrate OA.50 over R and over v uniform in each class band."""
    h, ell = prim.fh, prim.fell
    t_0 = _integrate_uniform(lambda R: T0_realized(R, p), r, [p], epsabs, epsrel)[0]

    def class_avg(center: float, fun) -> tuple[float, float]:
        lo, hi = center - eps_V, center + eps_V
        pts = sorted({lo, hi, *[x for x in (p, r) if lo < x < hi]})
        tot, err = 0.0, 0.0
        for a, b_ in zip(pts[:-1], pts[1:]):
            val, e = integrate.quad(lambda v: _integrate_uniform(lambda R: fun(R, v), r, [p, v], epsabs, epsrel)[0],
                                    a, b_, epsabs=epsabs, epsrel=epsrel, limit=200)
            tot += val
            err += e
        return tot / (hi - lo), err / (hi - lo)

    t_H, eH = class_avg(h, lambda R, v: T_realized(R, v, p))
    t_L, eL = class_avg(ell, lambda R, v: T_realized(R, v, p))
    g_H, egH = class_avg(h, lambda R, v: G_realized(R, v, p))
    g_L, egL = class_avg(ell, lambda R, v: G_realized(R, v, p))
    return AuctionPayoffs(r=r, p=p, t_0=t_0, t_H=t_H, t_L=t_L, g_H=g_H, g_L=g_L), max(eH, eL, egH, egL)


def payoffs_class_closed_form(prim: Primitives, r: float, p: float, eps_V: float) -> AuctionPayoffs:
    """Class economy via OA.51 averaged in closed form over each uniform band (exact quadratic averages)."""
    h, ell = prim.fh, prim.fell
    t_0 = p * (1 - p / r) if p <= r else 0.0

    def avg(center: float) -> tuple[float, float]:
        lo, hi = center - eps_V, center + eps_V
        # piecewise integration of the OA.51 kernel over v in [lo, hi]
        pts = sorted({lo, hi, *[x for x in (p, r) if lo < x < hi]})
        tot_t, tot_g = 0.0, 0.0
        for a, b_ in zip(pts[:-1], pts[1:]):
            mid = 0.5 * (a + b_)
            if mid < p:
                tot_t += t_0 * (b_ - a)
            elif mid < r:
                # t_v = v - (v^2 - p^2)/(2r); g_v = (v^2 - p^2)/(2r)
                I1 = (b_ ** 2 - a ** 2) / 2
                I2 = (b_ ** 3 - a ** 3) / 3
                tot_t += I1 - (I2 - p * p * (b_ - a)) / (2 * r)
                tot_g += (I2 - p * p * (b_ - a)) / (2 * r)
            elif p <= r:
                t_v = r / 2 + p * p / (2 * r)
                tot_t += t_v * (b_ - a)
                tot_g += (b_ ** 2 - a ** 2) / 2 - t_v * (b_ - a)
            else:
                tot_t += p * (b_ - a)
                tot_g += (b_ ** 2 - a ** 2) / 2 - p * (b_ - a)
        return tot_t / (hi - lo), tot_g / (hi - lo)

    t_H, g_H = avg(h)
    t_L, g_L = avg(ell)
    return AuctionPayoffs(r=r, p=p, t_0=t_0, t_H=t_H, t_L=t_L, g_H=g_H, g_L=g_L)


def payoffs_class_formula_OA52(prim: Primitives, r: float, p: float, eps_V: float) -> AuctionPayoffs:
    """OA.52, valid for p < ell - eps_V < ell + eps_V < r < h - eps_V."""
    h, ell = prim.fh, prim.fell
    t_0 = p * (1 - p / r)
    t_L = ell - (ell * ell + eps_V ** 2 / 3 - p * p) / (2 * r)
    g_L = (ell * ell + eps_V ** 2 / 3 - p * p) / (2 * r)
    t_H = r / 2 + p * p / (2 * r)
    return AuctionPayoffs(r=r, p=p, t_0=t_0, t_H=t_H, t_L=t_L, g_H=h - t_H, g_L=g_L)


# --- bargaining institution, OA.42 to OA.44 --------------------------------------
def bargaining_transfer(R: np.ndarray, theta: float, eta: float) -> np.ndarray:
    """T_eta(R, theta) = (1-eta) min(R, theta) + eta max(R, theta)."""
    R = np.asarray(R, dtype=float)
    return (1 - eta) * np.minimum(R, theta) + eta * np.maximum(R, theta)


def bargaining_closed_form(prim: Primitives, r: float, eta: float) -> dict:
    """OA.44 for the uniform incumbent on [0, r] with ell < r < h."""
    h, ell = prim.fh, prim.fell
    t_H = (1 - eta) * r / 2 + eta * h
    t_L = (1 - eta) * (ell - ell * ell / (2 * r)) + eta * (r / 2 + ell * ell / (2 * r))
    return {
        "t_0_eta": eta * r / 2,
        "t_H_eta": t_H,
        "t_L_eta": t_L,
        "Delta_eta": eta * (h - ell) + (1 - 2 * eta) * (r - ell) ** 2 / (2 * r),
        "G_H_eta": (1 - eta) * (h - r / 2),
        "G_L_eta": (1 - eta) * ell * ell / (2 * r),
    }
