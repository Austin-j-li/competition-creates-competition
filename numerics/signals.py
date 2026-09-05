"""Complementary private signals (Section 8.3, OA A.7): schedule construction and objects."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize

from .auction import AuctionPayoffs
from .information import OrderProfile
from .noise import pdf, posterior_bounds, survival
from .params import Noise, Primitives


def phi(mu: np.ndarray, d: float, y: str) -> np.ndarray:
    mu = np.asarray(mu, dtype=float)
    if y == "+":
        return d * mu / (d * mu + (1 - d) * (1 - mu))
    return (1 - d) * mu / ((1 - d) * mu + d * (1 - mu))


@dataclass(frozen=True)
class SignalSchedule:
    """Candidate schedule for signal-contingent orders q(T=+) = q_H, q(T=-) = q_L (profile fields reused)."""

    prim: Primitives
    pay: AuctionPayoffs
    profile: OrderProfile
    a: float
    d: float
    breakpoints: tuple[float, ...] = field(default_factory=tuple)

    def lam(self, x: np.ndarray) -> np.ndarray:
        ap = self.profile.a(self.prim.noise, self.prim.fb, x, "H")
        am = self.profile.a(self.prim.noise, self.prim.fb, x, "L")
        return ap / (ap + am)

    def mu(self, x: np.ndarray) -> np.ndarray:
        return (1 - self.a) + (2 * self.a - 1) * self.lam(x)

    def indicators(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        mu = self.mu(x)
        cH = self.prim.fc_H
        return (self.pay.B(phi(mu, self.d, "+")) >= cH).astype(float), (self.pay.B(phi(mu, self.d, "-")) >= cH).astype(float)

    def entry_states(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        rho, d = self.prim.frho, self.d
        Ip, Im = self.indicators(x)
        low = float(self.prim.fc_L <= self.pay.B(phi(self.mu(np.array([x]).ravel() if np.isscalar(x) else x), d, "-")).min()) if False else 1.0
        eH = rho + (1 - rho) * (d * Ip + (1 - d) * Im)
        eL = rho + (1 - rho) * ((1 - d) * Ip + d * Im)
        return eH, eL

    def D(self, x: np.ndarray) -> np.ndarray:
        eH, eL = self.entry_states(x)
        return eH * self.pay.w_H - eL * self.pay.w_L

    def price(self, x: np.ndarray) -> np.ndarray:
        mu = self.mu(x)
        eH, eL = self.entry_states(x)
        return self.pay.t_0 + mu * eH * self.pay.w_H + (1 - mu) * eL * self.pay.w_L

    def A(self, x: np.ndarray, state: str) -> np.ndarray:
        """Residuals (OA.37): state 'H' is the favorable trader signal T=+, 'L' is T=-."""
        lam = self.lam(x)
        D = self.D(x)
        if state == "H":
            return (2 * self.a - 1) * (1 - lam) * D
        return (2 * self.a - 1) * lam * D

    def A_direct(self, x: np.ndarray, state: str) -> np.ndarray:
        eH, eL = self.entry_states(x)
        P = self.price(x)
        a = self.a if state == "H" else 1 - self.a  # Pr(H | T)
        EV = self.pay.t_0 + a * eH * self.pay.w_H + (1 - a) * eL * self.pay.w_L
        return EV - P if state == "H" else P - EV

    def hull(self) -> tuple[float, float]:
        s = self.profile.supports
        return min(s), max(s)


def required_lambda(pay: AuctionPayoffs, c_H: float, a: float, d: float, y: str) -> float:
    """OA.39: public lambda at which the buyer with private signal y is indifferent (may be outside [0,1])."""
    tau = pay.tau(c_H)
    if tau <= 0:
        return -np.inf
    if tau >= 1:
        return np.inf
    if y == "+":
        mu_req = tau * (1 - d) / (d * (1 - tau) + tau * (1 - d))
    else:
        mu_req = tau * d / ((1 - d) * (1 - tau) + tau * d)
    return (mu_req - (1 - a)) / (2 * a - 1)


def make_signal_schedule(prim: Primitives, pay: AuctionPayoffs, profile: OrderProfile, a: float, d: float) -> SignalSchedule:
    sched = SignalSchedule(prim, pay, profile, a, d)
    bps = set(profile.supports)
    lo, hi = sched.hull()
    if hi - lo > 1e-14:
        xs = np.linspace(lo - 40 * prim.fb, hi + 40 * prim.fb, 20001)
        for y in ("+", "-"):
            lam_req = required_lambda(pay, prim.fc_H, a, d, y)
            g = sched.lam(xs) - lam_req
            for i in range(len(xs) - 1):
                if g[i] * g[i + 1] < 0:
                    bps.add(float(optimize.brentq(lambda x: float(sched.lam(np.array([x]))[0]) - lam_req, xs[i], xs[i + 1], xtol=1e-15)))
                elif g[i] == 0:
                    bps.add(float(xs[i]))
    return SignalSchedule(prim, pay, profile, a, d, tuple(sorted(bps)))


def full_order_signal_objects(prim: Primitives, pay: AuctionPayoffs, a: float, d: float) -> dict:
    """OA.39 to OA.41 closed forms for full Laplace orders by trader signal."""
    b, rho = prim.fb, prim.frho
    m, M = posterior_bounds(b)
    out = {}
    Q = {}
    for y in ("+", "-"):
        lam_req = required_lambda(pay, prim.fc_H, a, d, y)
        if lam_req <= m:
            x_star, kind = -np.inf, "always"
        elif lam_req > M:
            x_star, kind = np.inf, "never"
        elif lam_req == M:
            x_star, kind = 1.0, "plateau_tie"
        else:
            x_star, kind = b / 2 * np.log(lam_req / (1 - lam_req)), "interior"
        out[f"x_star_Y{'plus' if y == '+' else 'minus'}"] = x_star
        out[f"kind_Y{'plus' if y == '+' else 'minus'}"] = kind
        # Q_{theta,y} = Pr(X >= x* | Theta) with f_H^X = a f(x-1) + (1-a) f(x+1)
        if np.isinf(x_star):
            qp = qm = 1.0 if x_star < 0 else 0.0
        else:
            qp = float(survival(prim.noise, x_star - 1, b))   # Pr(X >= x* | T=+)
            qm = float(survival(prim.noise, x_star + 1, b))   # Pr(X >= x* | T=-)
        Q[("H", y)] = a * qp + (1 - a) * qm
        Q[("L", y)] = (1 - a) * qp + a * qm
    eH = rho + (1 - rho) * (d * Q[("H", "+")] + (1 - d) * Q[("H", "-")])
    eL = rho + (1 - rho) * ((1 - d) * Q[("L", "+")] + d * Q[("L", "-")])
    out.update(e_H=eH, e_L=eL, E=0.5 * (eH + eL), O_H=0.5 * eH, R_T=pay.t_0 + 0.5 * (eH * pay.w_H + eL * pay.w_L), Q=Q)
    return out


def signal_margins(prim: Primitives, pay0: AuctionPayoffs, pay1: AuctionPayoffs, a: float, d: float) -> dict:
    """The five strict margins of (OA.29)."""
    b, rho, k = prim.fb, prim.frho, prim.fk
    m, M = posterior_bounds(b)
    mu_m = (1 - a) + (2 * a - 1) * m
    mu_p = (1 - a) + (2 * a - 1) * M
    return {
        "mu_lower": mu_m, "mu_upper": mu_p,
        "phi_minus_mu_lower": float(phi(mu_m, d, "-")), "phi_plus_mu_upper": float(phi(mu_p, d, "+")),
        "low_cost_margin": pay1.B(float(phi(mu_m, d, "-"))) - prim.fc_L,
        "private_only_exclusion_margin": prim.fc_H - pay0.B(d),
        "joint_entry_margin": pay1.B(float(phi(mu_p, d, "+"))) - prim.fc_H,
        "weak_order_margin": k - (2 * a - 1) * (pay0.Delta_T + (1 - rho) * (2 * d - 1) * pay0.w_H),
        "strong_order_margin": (1 - 1 / b) * m * (2 * a - 1) * rho * pay1.Delta_T - k,
    }
