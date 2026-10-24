"""Print stake incentives at fixed schedules and on pure candidate profiles.

Run from the project root with .venv/bin/python and this file's relative path.
This program prints numerical diagnostics. It writes no output files.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import math
import platform

import numpy as np
import mpmath as mp
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar


@dataclass(frozen=True)
class Parameters:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    rho: float = 0.25
    c_low: float = 1.0
    c_high: float = 6.0
    b: float = 2.0
    k: float = 0.02


@dataclass(frozen=True)
class Auction:
    r: float
    t0: float
    t_high: float
    t_low: float
    g_high: float
    g_low: float
    delta: float
    tau: float


def auction(p: Parameters, r: float) -> Auction:
    t0 = p.p * (1.0 - p.p / r)
    th = r / 2.0 + p.p**2 / (2.0 * r)
    tl = p.ell - (p.ell**2 - p.p**2) / (2.0 * r)
    gh = p.h - th
    gl = (p.ell**2 - p.p**2) / (2.0 * r)
    return Auction(r, t0, th, tl, gh, gl, th - tl,
                   (p.c_high - gl) / (gh - gl))


def density(p: Parameters, x: float) -> float:
    return math.exp(-abs(x) / p.b) / (2.0 * p.b)


def survival(p: Parameters, x: float) -> float:
    return 0.5 * math.exp(-x / p.b) if x >= 0 else 1 - 0.5 * math.exp(x / p.b)


@dataclass(frozen=True)
class PureSchedule:
    parameters: Parameters
    primitives: Auction
    q_high: float = 1.0
    q_low: float = -1.0

    def posterior(self, x: float) -> float:
        p = self.parameters
        log_odds = (abs(x - self.q_low) - abs(x - self.q_high)) / p.b
        return 1.0 / (1.0 + math.exp(-log_odds))

    def cutoff(self) -> float:
        p, a = self.parameters, self.primitives
        ceiling = 1.0 / (1.0 + math.exp(-(self.q_high - self.q_low) / p.b))
        if a.tau > ceiling + 2e-14:
            return math.inf
        if a.tau <= 1 - ceiling:
            return -math.inf
        return (self.q_high + self.q_low + p.b * math.log(a.tau / (1 - a.tau))) / 2

    def entry(self, x: float) -> float:
        return 1.0 if x >= self.cutoff() else self.parameters.rho

    def entry_mean(self, q: float) -> float:
        p = self.parameters
        return p.rho + (1 - p.rho) * survival(p, self.cutoff() - q)

    def entry_derivative(self, q: float) -> float:
        p = self.parameters
        return (1 - p.rho) * density(p, self.cutoff() - q)

    @lru_cache(maxsize=200000)
    def residual(self, q: float, state: str, derivative: bool = False) -> float:
        p, a = self.parameters, self.primitives
        points = sorted(set([-math.inf, self.q_low, q, self.q_high,
                             self.cutoff(), math.inf]))

        def integrand(x: float) -> float:
            mu = self.posterior(x)
            value = self.entry(x) * a.delta * (1 - mu if state == "H" else mu)
            score = (1.0 if x > q else -1.0) / p.b if derivative else 1.0
            return density(p, x - q) * value * score

        return sum(quad(integrand, left, right, epsabs=2e-12, epsrel=2e-12)[0]
                   for left, right in zip(points[:-1], points[1:]))

    def value(self, q: float, state: str) -> float:
        a = self.primitives
        w = (a.t_high if state == "H" else a.t_low) - a.t0
        return a.t0 + w * self.entry_mean(q)

    def payoff(self, q: float, state: str, omega: float) -> float:
        sign = 1.0 if state == "H" else -1.0
        return (omega * self.value(q, state) + sign * q * self.residual(q, state)
                - self.parameters.k * abs(q))

    def marginal(self, q: float, state: str, omega: float, side: int = 1) -> float:
        p, a = self.parameters, self.primitives
        sign = 1.0 if state == "H" else -1.0
        w = (a.t_high if state == "H" else a.t_low) - a.t0
        cost_sign = math.copysign(1.0, q) if q != 0 else side
        return (omega * w * self.entry_derivative(q)
                + sign * (self.residual(q, state) + q * self.residual(q, state, True))
                - p.k * cost_sign)

    def best_response(self, state: str, omega: float) -> tuple[float, float]:
        grid = np.linspace(-1.0, 1.0, 101)
        candidates = list(grid)
        payoffs = [self.payoff(float(q), state, omega) for q in grid]
        for i in range(1, len(grid) - 1):
            if payoffs[i] >= payoffs[i - 1] and payoffs[i] >= payoffs[i + 1]:
                result = minimize_scalar(lambda q: -self.payoff(q, state, omega),
                                         bounds=(grid[i - 1], grid[i + 1]),
                                         method="bounded", options={"xatol": 2e-11})
                candidates.append(float(result.x))
        q = max(candidates, key=lambda order: self.payoff(float(order), state, omega))
        return float(q), self.payoff(float(q), state, omega)


def main() -> None:
    p = Parameters()
    m = 1.0 / (1.0 + math.exp(2 / p.b))
    print("Status: numerical diagnostic; no interval certificate or completeness claim.")
    print("UTC:", datetime.now(timezone.utc).isoformat())
    print("Python:", platform.python_version(), "numpy:", np.__version__, "scipy:", scipy.__version__)
    source = Path("overleaf/paper/main.tex")
    print("Paper SHA-256:", sha256(source.read_bytes()).hexdigest())
    print("Parameters:", p)
    print("Quadrature: split at all order, density, and entry breakpoints; epsabs=epsrel=2e-12.")
    print("Best response: 101 grid points and local refinements of all grid maxima.")
    print("\nAUCTION PRIMITIVES AND BOUNDS")
    for r in (1.2, 3.0, 3.6):
        a = auction(p, r)
        print(a)
        bp = a.g_low + 0.5 * (a.g_high - a.g_low)
        bm = a.g_low + (1 - m) * (a.g_high - a.g_low)
        margin = (1 - 1 / p.b) * p.rho * m * a.delta - p.k
        unique = 2 * p.b * margin / ((1 - p.rho) * (a.t_high - a.t0))
        bound = ("unbounded: entry is constant" if bm < p.c_high
                 else f"{unique:.12f}" if margin > 0 else "not applicable: negative trade margin")
        print(f"r={r:g} B(prior)={bp:.12f} B(M)={bm:.12f} universal_stake_bound={bound}")
        if a.delta < p.k:
            weak_bound = 2*p.b*(p.k-a.delta)/((1-p.rho)*(a.t_high-a.t0))
            print(f"Weak no-trade uniqueness sufficient bound={weak_bound:.12f}")

    a = auction(p, 3.0)
    s = PureSchedule(p, a)
    wl = a.t_low - a.t0
    local_limit = -s.marginal(-1.0, "L", 0.0) / (wl * s.entry_derivative(-1.0))

    def cutoff_ratio(q: float) -> float:
        if abs(q + 1.0) < 1e-8:
            return local_limit
        return ((s.payoff(-1.0, "L", 0.0) - s.payoff(q, "L", 0.0))
                / (s.value(q, "L") - s.value(-1.0, "L")))

    grid = np.linspace(-1.0, 1.0, 2001)
    ratios = [cutoff_ratio(float(q)) for q in grid]
    j = int(np.argmin(ratios))
    result = minimize_scalar(cutoff_ratio, bounds=(grid[max(0, j - 1)], grid[min(2000, j + 1)]),
                             method="bounded", options={"xatol": 1e-12})
    ratio_candidates = [(-1.0, local_limit), (1.0, cutoff_ratio(1.0)), (result.x, result.fun)]
    q_cut, full_cut = min(ratio_candidates, key=lambda item: item[1])
    buy_sell = cutoff_ratio(1.0)
    buy_zero = ((s.residual(1.0, "L") + p.k)
                / (s.value(1.0, "L") - s.value(0.0, "L")))
    zero_right = (s.residual(0.0, "L") + p.k) / (wl * s.entry_derivative(0.0))
    zero_left = (s.residual(0.0, "L") - p.k) / (wl * s.entry_derivative(0.0))
    buy_boundary = -s.marginal(1.0, "L", 0.0) / (wl * s.entry_derivative(1.0))
    print("\nFULL PROFILE THRESHOLDS AT r=3")
    for name, value in [("x_star", s.cutoff()), ("q_L_ceiling_for_entry", 1 - 2 * s.cutoff()),
                        ("full_profile_limit", full_cut), ("deviation_at_limit", q_cut),
                        ("local_sale_limit", local_limit), ("buy_vs_sell", buy_sell),
                        ("buy_vs_zero", buy_zero), ("zero_left_marginal", zero_left),
                        ("zero_right_marginal", zero_right), ("full_buy_local", buy_boundary)]:
        print(f"{name}={value:.12f}")
    for state in ("H", "L"):
        for q in (-1.0, 0.0, 1.0):
            print(f"state={state} q={q:+.0f} payoff_intercept={s.payoff(q,state,0):.12f} "
                  f"omega_coefficient={s.value(q,state):.12f}")
    print("\nFIXED FULL-PROFILE PAYOFFS: omega state sell zero buy best_q best_value")
    for omega in (0.0, 0.01, 0.1, 0.5, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 10.0):
        for state in ("H", "L"):
            q, val = s.best_response(state, omega)
            print(f"{omega:6.3f} {state} {s.payoff(-1,state,omega):.9f} "
                  f"{s.payoff(0,state,omega):.9f} {s.payoff(1,state,omega):.9f} {q:.9f} {val:.9f}")
    print("\nPURE BRANCH: q_L, omega from own marginal, best_q_L, gain_from_deviation, entry")
    qmax = 1 - 2 * s.cutoff()
    for ql in np.linspace(-1, qmax, 9):
        candidate = PureSchedule(p, a, q_low=float(ql))
        stake_slope = wl * candidate.entry_derivative(float(ql))
        omega = -candidate.marginal(float(ql), "L", 0) / stake_slope
        best, bestval = candidate.best_response("L", omega)
        own = candidate.payoff(float(ql), "L", omega)
        entry = (candidate.entry_mean(1) + candidate.entry_mean(float(ql))) / 2
        print(f"{ql:.12f} {omega:.12f} {best:.12f} {bestval-own:.3e} {entry:.12f}")

    print("\nCLOSED FORM AT 60 DECIMAL DIGITS")
    mp.mp.dps = 60
    mb, mr, mk, md = mp.mpf(2), mp.mpf(1)/4, mp.mpf("0.02"), mp.mpf(2)/3
    mm = 1/(1+mp.exp(2/mb))
    mx = mp.log(mp.mpf(141)/59)
    mj = md/2*((1+mr)*mm+mp.exp(-1/mb)*(
        mr*(mp.atan(mp.exp(mx/mb))-mp.atan(mp.exp(-1/mb)))
        +mp.atan(mp.exp(1/mb))-mp.atan(mp.exp(mx/mb))))
    slope = mp.mpf(11)/24*(1-mr)*mp.exp(-(mx+1)/mb)/(2*mb)
    mlocal = ((1-1/mb)*mj+mr*mm*md/mb-mk)/slope
    print("J =", mp.nstr(mj, 35))
    print("Local full-sale threshold =", mp.nstr(mlocal, 35))
    monotone_ceiling = 2*p.b*math.exp(2/p.b)*((1+1/p.b)*a.delta+p.k)/((1-p.rho)*wl)
    print(f"No nondecreasing-entry equilibrium above sufficient omega={monotone_ceiling:.12f}")
    print(f"Endpoint-mixture entry requires Pr_L(sale)>={(2-1/a.tau)/(1-math.exp(-2/p.b)):.12f}")


if __name__ == "__main__":
    main()
