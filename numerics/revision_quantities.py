"""C.9: gross trade profits, sufficient stake bounds, and fixed-profile entry."""
from __future__ import annotations

from dataclasses import dataclass
from math import atan, atanh, exp, inf, log, pi, sqrt, tanh

import mpmath as mp
from scipy import stats

from .auction import payoffs_closed_form
from .deviations import F
from .information import OrderProfile, make_schedule
from .noise import posterior_bounds, survival
from .params import Controls, Primitives


@dataclass(frozen=True)
class TradingQuantities:
    Pi_acc: float
    Pi_hid: float
    Delta_R_T: float
    break_even_trade_scale: float
    gross_H_acc: float
    gross_L_acc: float
    gross_H_hid: float
    gross_L_hid: float
    alpha_H: float
    alpha_L: float
    quadrature_error: float
    tail_bound: float


@dataclass(frozen=True)
class StakeBounds:
    Omega_U: float
    Omega_0: float
    strong_margin: float
    weak_margin: float
    strong_w_H: float
    weak_w_H: float


@dataclass(frozen=True)
class NoiseEntry:
    noise: str
    scale: float
    nu: float | None
    score_bound: float
    tau: float
    lower: float
    upper: float
    posterior_supremum: float
    alpha_H: float
    alpha_L: float
    E: float


def trading_quantities(prim: Primitives, r: float) -> TradingQuantities:
    """Expected gross profit under full orders; k is not deducted."""
    pay = payoffs_closed_form(prim, r)
    profile = OrderProfile.pure(1.0, -1.0)
    access = make_schedule(prim, pay, profile, "feedback")
    hidden = make_schedule(prim, pay, profile, "price_hidden")
    values = tuple(F(schedule, state, 1.0) for schedule in (access, hidden) for state in ("H", "L"))
    tau = pay.tau(prim.fc_H)
    cutoff = prim.fb / 2 * log(tau / (1 - tau))
    alpha_H = float(survival(prim.noise, cutoff - 1, prim.fb))
    alpha_L = float(survival(prim.noise, cutoff + 1, prim.fb))
    gain = (1 - prim.frho) * (pay.w_H * alpha_H + pay.w_L * alpha_L) / 2
    acc, hid = (values[0].value + values[1].value) / 2, (values[2].value + values[3].value) / 2
    return TradingQuantities(acc, hid, gain, gain / acc, *(v.value for v in values), alpha_H, alpha_L,
                             max(v.error for v in values), max(v.tail_bound for v in values))


def stake_bounds(prim: Primitives, r_weak: float, r_strong: float) -> StakeBounds:
    """Sufficient uniqueness bounds from the stake memo, equations S12 and S14."""
    weak, strong = payoffs_closed_form(prim, r_weak), payoffs_closed_form(prim, r_strong)
    m, _ = posterior_bounds(prim.fb)
    strong_margin = (1 - 1 / prim.fb) * prim.frho * m * strong.Delta_T - prim.fk
    weak_margin = prim.fk - weak.Delta_T
    omega_U = 2 * prim.fb * strong_margin / ((1 - prim.frho) * strong.w_H)
    omega_0 = 2 * prim.fb * weak_margin / ((1 - prim.frho) * weak.w_H)
    return StakeBounds(omega_U, omega_0, strong_margin, weak_margin, strong.w_H, weak.w_H)


def sech_density(prim: Primitives, z: float) -> float:
    """sech(z/b)/(pi b), in a form without hyperbolic overflow."""
    e = exp(-abs(z) / prim.fb)
    return 2 * e / (pi * prim.fb * (1 + e * e))


def sech_log_density(prim: Primitives, z: float) -> float:
    a = abs(z) / prim.fb
    return log(2 / (pi * prim.fb)) - a - log(1 + exp(-2 * a))


def noise_entry(prim: Primitives, r: float, noise: str, nu: float) -> NoiseEntry:
    """Entry under the prescribed orders (1,-1); no equilibrium search."""
    pay = payoffs_closed_form(prim, r)
    tau = pay.tau(prim.fc_H)
    if not 0.5 < tau < posterior_bounds(prim.fb)[1]:
        raise ValueError("C.9 requires an interior high-cost threshold above the prior.")
    if noise == "hyperbolic_secant":
        scale = prim.fb
        lower = scale * atanh(tanh(log(tau / (1 - tau)) / 2) / tanh(1 / scale))
        upper = inf
        alpha_H = 2 / pi * atan(exp(-(lower - 1) / scale))
        alpha_L = 2 / pi * atan(exp(-(lower + 1) / scale))
        ceiling = posterior_bounds(prim.fb)[1]
        degrees = None
        score = 1 / scale
    elif noise == "student_t":
        scale = prim.fb * (nu + 1) / (2 * sqrt(nu))
        a = nu * scale * scale
        ratio = (tau / (1 - tau)) ** (2 / (nu + 1))
        center = (ratio + 1) / (ratio - 1)
        discriminant = center * center - (a + 1)
        if discriminant <= 0:
            raise ValueError("C.9 Student entry requires two distinct finite boundaries.")
        upper = center + sqrt(discriminant)
        lower = (a + 1) / upper
        alpha_H = float(stats.t.sf((lower - 1) / scale, nu) - stats.t.sf((upper - 1) / scale, nu))
        alpha_L = float(stats.t.sf((lower + 1) / scale, nu) - stats.t.sf((upper + 1) / scale, nu))
        peak = sqrt(a + 1)
        odds = ((a + (peak + 1) ** 2) / (a + (peak - 1) ** 2)) ** ((nu + 1) / 2)
        ceiling = odds / (1 + odds)
        degrees = nu
        score = (nu + 1) / (2 * scale * sqrt(nu))
    else:
        raise ValueError(f"Unsupported C.9 noise law: {noise}")
    entry = prim.frho + (1 - prim.frho) * (alpha_H + alpha_L) / 2
    return NoiseEntry(noise, scale, degrees, score, tau, lower, upper, ceiling, alpha_H, alpha_L, entry)


def independent_benchmark(prim: Primitives, r_weak: str, r_strong: str,
                          controls: Controls) -> tuple[tuple[str, float], ...]:
    """Direct density integrals and decimal formulas, separate from the flow code."""
    with mp.workdps(controls.interval_decimal_precision):
        h, ell, p, rho, high_cost, b, k = (mp.mpf(s) for s in
                                         (prim.h, prim.ell, prim.p, prim.rho, prim.c_H, prim.b, prim.k))
        weak, strong = mp.mpf(r_weak), mp.mpf(r_strong)
        t0 = p * (1 - p / strong)
        tH = strong / 2 + p * p / (2 * strong)
        tL = ell - (ell * ell - p * p) / (2 * strong)
        delta = tH - tL
        gL = (ell * ell - p * p) / (2 * strong)
        gH = h - tH
        tau = (high_cost - gL) / (gH - gL)
        cutoff = b / 2 * mp.log(tau / (1 - tau))

        def density(z: mp.mpf) -> mp.mpf:
            return mp.exp(-abs(z) / b) / (2 * b)

        def residual_product(x: mp.mpf) -> mp.mpf:
            aH, aL = density(x - 1), density(x + 1)
            return delta * aH * aL / (aH + aL)

        boundaries = [-mp.inf, -mp.mpf(1), cutoff, mp.mpf(1), mp.inf]
        acc = mp.mpf(0)
        hid = mp.mpf(0)
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            mass = mp.quad(residual_product, [left, right])
            acc += (rho if right <= cutoff else 1) * mass
            hid += rho * mass
        alpha_H = 1 - mp.exp((cutoff - 1) / b) / 2
        alpha_L = mp.exp(-(cutoff + 1) / b) / 2
        gain = (1 - rho) * ((tH - t0) * alpha_H + (tL - t0) * alpha_L) / 2
        m = 1 / (1 + mp.exp(2 / b))
        omega_U = 2 * b * ((1 - 1 / b) * rho * m * delta - k) / ((1 - rho) * (tH - t0))
        weak_delta = (weak - ell) ** 2 / (2 * weak)
        weak_wH = weak / 2 + p * p / (2 * weak) - p * (1 - p / weak)
        omega_0 = 2 * b * (k - weak_delta) / ((1 - rho) * weak_wH)
        return tuple((name, float(value)) for name, value in (
            ("Pi_acc", acc), ("Pi_hid", hid), ("Delta_R_T", gain),
            ("break_even_trade_scale", gain / acc), ("Omega_U", omega_U), ("Omega_0", omega_0)))
