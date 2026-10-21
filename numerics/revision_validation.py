"""Independent acceptance for the bounded C.9 calculation."""
from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite, sqrt

from scipy import integrate, optimize, special, stats

from .auction import payoffs_closed_form
from .params import Controls, Primitives
from .revision_quantities import NoiseEntry, StakeBounds, TradingQuantities, sech_density, sech_log_density
from .search import full_order_candidate
from .validation import validate


@dataclass(frozen=True)
class NoiseValidation:
    E: float
    quadrature_error: float
    formula_error: float
    boundary_error: float
    boundary_residual: float
    accepted: bool


def validate_noise_entry(prim: Primitives, row: NoiseEntry, controls: Controls) -> NoiseValidation:
    """Locate the entry boundaries from densities, then integrate over the complete set."""
    if row.noise == "hyperbolic_secant":
        def density(z: float) -> float:
            return sech_density(prim, z)

        def posterior(x: float) -> float:
            return float(special.expit(sech_log_density(prim, x - 1) - sech_log_density(prim, x + 1)))

        right = prim.fb
        while posterior(right) <= row.tau:
            right *= 2
        lower = float(optimize.brentq(lambda x: posterior(x) - row.tau, 0, right, xtol=1e-13))
        upper = inf
    else:
        def density(z: float) -> float:
            return float(stats.t.pdf(z / row.scale, row.nu) / row.scale)

        def posterior(x: float) -> float:
            return float(special.expit(stats.t.logpdf((x - 1) / row.scale, row.nu)
                                      - stats.t.logpdf((x + 1) / row.scale, row.nu)))

        peak = sqrt(row.nu * row.scale ** 2 + 1)
        lower = float(optimize.brentq(lambda x: posterior(x) - row.tau, 0, peak, xtol=1e-13))
        right = 2 * peak
        while posterior(right) >= row.tau:
            right *= 2
        upper = float(optimize.brentq(lambda x: posterior(x) - row.tau, peak, right, xtol=1e-13))
    masses = tuple(integrate.quad(lambda x: density(x - q), lower, upper,
                                 epsabs=controls.quadrature_absolute_target,
                                 epsrel=controls.quadrature_relative_target) for q in (1.0, -1.0))
    entry = prim.frho + (1 - prim.frho) * (masses[0][0] + masses[1][0]) / 2
    formula_error = max(abs(masses[0][0] - row.alpha_H), abs(masses[1][0] - row.alpha_L), abs(entry - row.E))
    boundary_error = max(abs(lower - row.lower), abs(upper - row.upper) if isfinite(upper) else 0.0)
    boundary_residual = max(abs(posterior(x) - row.tau) for x in (lower, upper) if isfinite(x))
    quadrature_error = max(mass[1] for mass in masses)
    accepted = (formula_error <= controls.independent_formula_acceptance
                and boundary_error <= controls.independent_formula_acceptance
                and boundary_residual <= controls.probability_acceptance
                and quadrature_error <= controls.quadrature_absolute_target
                and abs(row.score_bound - 1 / prim.fb) <= controls.independent_formula_acceptance
                and 0 <= row.E <= 1 and row.posterior_supremum > row.tau)
    return NoiseValidation(entry, quadrature_error, formula_error, boundary_error, boundary_residual, bool(accepted))


def validate_trading_and_stakes(prim: Primitives, r: float, trades: TradingQuantities,
                               stakes: StakeBounds, reference: tuple[tuple[str, float], ...],
                               controls: Controls) -> tuple[tuple[str, float | bool], ...]:
    """Revalidate both price regimes and compare the independent scalar formulas."""
    pay = payoffs_closed_form(prim, r)
    access = validate(full_order_candidate(prim, pay, "feedback").sched, controls)
    hidden = validate(full_order_candidate(prim, pay, "price_hidden").sched, controls)
    values = {**trades.__dict__, **stakes.__dict__}
    formula_error = max(abs(values[name] - value) for name, value in reference)
    outcome_error = abs(trades.Delta_R_T - (access.outcome.R_T - hidden.outcome.R_T))
    state_profit_error = max(abs(trades.gross_H_acc - trades.gross_L_acc), abs(trades.gross_H_hid - trades.gross_L_hid))
    accepted = (access.accepted and hidden.accepted and formula_error <= controls.independent_formula_acceptance
                and outcome_error <= controls.independent_formula_acceptance
                and state_profit_error <= controls.independent_formula_acceptance
                and trades.quadrature_error + trades.tail_bound <= controls.quadrature_absolute_target
                and stakes.strong_margin > 0 and stakes.weak_margin > 0 and trades.Pi_acc > 0)
    return tuple(dict(access_accepted=access.accepted, hidden_accepted=hidden.accepted,
                      independent_formula_error=formula_error, proceeds_identity_error=outcome_error,
                      state_profit_error=state_profit_error, quadrature_error=trades.quadrature_error,
                      tail_bound=trades.tail_bound, accepted=bool(accepted)).items())
