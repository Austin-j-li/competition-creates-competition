"""Information and price construction (Lemma 1, Lemma 2, eq. 9 to 11, OA.35).

A `Schedule` is a candidate: order profile plus the pricing and entry rules it induces.
It is held fixed during unilateral-deviation calculations (C.0).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from scipy import optimize

from .auction import AuctionPayoffs
from .noise import pdf, posterior_bounds
from .params import CostLaw, Noise, Primitives

Regime = Literal["feedback", "price_hidden"]


@dataclass(frozen=True)
class OrderProfile:
    """Finite-support mixed orders per state. Pure profiles have a single support point."""

    q_H: tuple[float, ...]
    w_H: tuple[float, ...]
    q_L: tuple[float, ...]
    w_L: tuple[float, ...]

    @staticmethod
    def pure(q_H: float, q_L: float) -> "OrderProfile":
        return OrderProfile((float(q_H),), (1.0,), (float(q_L),), (1.0,))

    @property
    def is_pure(self) -> bool:
        return len(self.q_H) == 1 and len(self.q_L) == 1

    @property
    def supports(self) -> list[float]:
        return sorted(set(self.q_H) | set(self.q_L))

    def label(self) -> str:
        if self.is_pure:
            return f"({self.q_H[0]:.10g},{self.q_L[0]:.10g})"
        return "mixed"

    def a(self, noise: Noise, b: float, x: np.ndarray, state: str) -> np.ndarray:
        qs, ws = (self.q_H, self.w_H) if state == "H" else (self.q_L, self.w_L)
        x = np.asarray(x, dtype=float)
        out = np.zeros_like(x)
        for q, w in zip(qs, ws):
            if w > 0:
                out += w * pdf(noise, x - q, b)
        return out


# --- entry rules -------------------------------------------------------------------
def uniform_cdf(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if hi <= lo:
        return (x >= lo).astype(float)
    return np.clip((x - lo) / (hi - lo), 0.0, 1.0)


def cost_cdf(prim: Primitives, c: np.ndarray) -> np.ndarray:
    """H_C(c): probability that the preparation cost is at most c."""
    c = np.asarray(c, dtype=float)
    rho, cL, cH = prim.frho, prim.fc_L, prim.fc_H
    if prim.cost_law == CostLaw.ATOMS:
        return rho * (c >= cL) + (1 - rho) * (c >= cH)
    e = prim.feps_C
    return rho * uniform_cdf(c, cL - e, cL + e) + (1 - rho) * uniform_cdf(c, cH - e, cH + e)


def entry_at_posterior(prim: Primitives, pay: AuctionPayoffs, mu: np.ndarray) -> np.ndarray:
    """e(mu) = H_C(B_r(mu)); entry at exact indifference is prescribed (tie rule)."""
    return cost_cdf(prim, pay.B(np.asarray(mu, dtype=float)))


def expected_paid_cost_at_posterior(prim: Primitives, pay: AuctionPayoffs, mu: np.ndarray) -> np.ndarray:
    """E[C 1{C <= B_r(mu)}] under the cost law."""
    B = pay.B(np.asarray(mu, dtype=float))
    rho, cL, cH = prim.frho, prim.fc_L, prim.fc_H
    if prim.cost_law == CostLaw.ATOMS:
        return rho * cL * (B >= cL) + (1 - rho) * cH * (B >= cH)
    e = prim.feps_C

    def comp(c0: float) -> np.ndarray:
        lo, hi = c0 - e, c0 + e
        top = np.clip(B, lo, hi)
        # integral of c/(2e) from lo to top
        return (top ** 2 - lo ** 2) / (2 * (hi - lo))

    return rho * comp(cL) + (1 - rho) * comp(cH)


# --- schedule ----------------------------------------------------------------------
@dataclass(frozen=True)
class Schedule:
    prim: Primitives
    pay: AuctionPayoffs
    profile: OrderProfile
    regime: Regime = "feedback"
    dividend: float = 0.0
    breakpoints: tuple[float, ...] = field(default_factory=tuple)
    tie_at_ceiling: bool = False  # C.2: at r_C treat tau = M symbolically; the whole upper plateau enters

    # posterior and its constant tails ---------------------------------------
    def mu(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        aH = self.profile.a(self.prim.noise, self.prim.fb, x, "H")
        aL = self.profile.a(self.prim.noise, self.prim.fb, x, "L")
        return aH / (aH + aL)

    def public_posterior(self, x: np.ndarray) -> np.ndarray:
        """Posterior the buyer acts on: flow posterior with feedback, prior when hidden."""
        if self.regime == "price_hidden":
            return np.full_like(np.asarray(x, dtype=float), 0.5)
        return self.mu(x)

    def entry(self, x: np.ndarray) -> np.ndarray:
        e = entry_at_posterior(self.prim, self.pay, self.public_posterior(x))
        if self.tie_at_ceiling and self.regime == "feedback":
            m, M = posterior_bounds(self.prim.fb)
            e = np.where(self.mu(x) >= M - 1e-9, 1.0, e)
        return e

    def price(self, x: np.ndarray) -> np.ndarray:
        """P = t_0 + e [w_L + Delta_T mu_X] + dividend (eq. 9 / OA.35 with common entry)."""
        e = self.entry(x)
        return self.pay.t_0 + e * (self.pay.w_L + self.pay.Delta_T * self.mu(x)) + self.dividend

    def A(self, x: np.ndarray, state: str) -> np.ndarray:
        """Residual advantage: A_H = E[V_T|H,x] - P, A_L = P - E[V_T|L,x] (eq. 10)."""
        e = self.entry(x)
        mu = self.mu(x)
        if state == "H":
            return e * self.pay.Delta_T * (1 - mu)
        return e * self.pay.Delta_T * mu

    def A_direct(self, x: np.ndarray, state: str) -> np.ndarray:
        """Residual by direct subtraction of the price from the conditional terminal value."""
        e = self.entry(x)
        P = self.price(x)
        if state == "H":
            return self.pay.t_0 + e * self.pay.w_H + self.dividend - P
        return P - (self.pay.t_0 + e * self.pay.w_L + self.dividend)

    def hull(self) -> tuple[float, float]:
        s = self.profile.supports
        return min(s), max(s)


def _threshold_crossings(mu_fn, tau: float, lo: float, hi: float, n: int = 4001) -> list[float]:
    """Locate x where mu(x) crosses tau on [lo, hi] by scanning and bracketing."""
    if not (0.0 < tau < 1.0):
        return []
    xs = np.linspace(lo, hi, n)
    g = mu_fn(xs) - tau
    out = []
    for i in range(n - 1):
        if g[i] == 0.0:
            out.append(float(xs[i]))
        elif g[i] * g[i + 1] < 0:
            out.append(float(optimize.brentq(lambda x: float(mu_fn(np.array([x]))[0]) - tau, xs[i], xs[i + 1], xtol=1e-14)))
    return out


def make_schedule(prim: Primitives, pay: AuctionPayoffs, profile: OrderProfile,
                  regime: Regime = "feedback", dividend: float = 0.0, tie_at_ceiling: bool = False) -> Schedule:
    """Build the candidate schedule and its integration breakpoints (support kinks, entry jumps)."""
    sched = Schedule(prim, pay, profile, regime, dividend, tie_at_ceiling=tie_at_ceiling)
    bps = set(profile.supports)
    if regime == "feedback":
        lo, hi = sched.hull()
        pad = 0.0 if prim.noise == Noise.LAPLACE else 40.0 * prim.fb
        rho, cL, cH = prim.frho, prim.fc_L, prim.fc_H
        if prim.cost_law == CostLaw.ATOMS:
            costs = [cL, cH]
        else:
            e = prim.feps_C
            costs = [cL - e, cL + e, cH - e, cH + e]
        for c in costs:
            tau = pay.tau(c)
            for xc in _threshold_crossings(sched.mu, tau, lo - pad - 1e-9, hi + pad + 1e-9):
                bps.add(xc)
    return Schedule(prim, pay, profile, regime, dividend, tuple(sorted(bps)), tie_at_ceiling)


def laplace_full_order_objects(prim: Primitives, pay: AuctionPayoffs) -> dict:
    """Closed forms (14) and OA.16/OA.17 for full Laplace orders, atomic costs."""
    b, rho = prim.fb, prim.frho
    m, M = posterior_bounds(b)
    tau = pay.tau(prim.fc_H)
    out = {"tau": tau, "m": m, "M": M}
    if tau <= m:
        x_star, aH, aL = -np.inf, 1.0, 1.0
    elif tau > M:
        x_star, aH, aL = np.inf, 0.0, 0.0
    elif tau == M:
        x_star, aH, aL = 1.0, 0.5, 0.5 * np.exp(-2 / b)  # tie rule: entire upper plateau enters
    else:
        x_star = b / 2 * np.log(tau / (1 - tau))
        aH = 1 - 0.5 * np.exp((x_star - 1) / b) if x_star < 1 else 0.5 * np.exp(-(x_star - 1) / b)
        aL = 0.5 * np.exp(-(x_star + 1) / b) if x_star > -1 else 1 - 0.5 * np.exp((x_star + 1) / b)
    out.update(x_star=x_star, alpha_H=aH, alpha_L=aL)
    out["e_H"] = rho + (1 - rho) * aH
    out["e_L"] = rho + (1 - rho) * aL
    out["E"] = rho + (1 - rho) * (aH + aL) / 2
    out["O_H"] = 0.5 * (rho + (1 - rho) * aH)
    return out


def logistic_full_order_objects(prim: Primitives, pay: AuctionPayoffs) -> dict:
    """Eq. (20): logistic threshold and favorable-flow probabilities."""
    b, rho = prim.fb, prim.frho
    m, M = posterior_bounds(b)
    tau = pay.tau(prim.fc_H)
    out = {"tau": tau, "m": m, "M": M}
    if tau <= m:
        x_star, aH, aL = -np.inf, 1.0, 1.0
    elif tau >= M:
        x_star, aH, aL = np.inf, 0.0, 0.0  # unattainable endpoint: zero mass
    else:
        A = np.exp(1 / b)
        w = np.sqrt(tau / (1 - tau))
        x_star = b * np.log((A * w - 1) / (A - w))
        aH = 1 / (1 + np.exp((x_star - 1) / b))
        aL = 1 / (1 + np.exp((x_star + 1) / b))
    out.update(x_star=x_star, alpha_H=aH, alpha_L=aL)
    out["e_H"] = rho + (1 - rho) * aH
    out["e_L"] = rho + (1 - rho) * aL
    out["E"] = rho + (1 - rho) * (aH + aL) / 2
    out["O_H"] = 0.5 * (rho + (1 - rho) * aH)
    return out
