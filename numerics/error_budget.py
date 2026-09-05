"""Per-row error budget for validated candidates (C.0 numerical controls; spec 10.2, S3-05/S3-06/S3-08).

Every component of the approximation error is recorded as a separate field and compared with its
declared target. A breached target is reported as a breach and never loosened. The between-grid
component is a Lipschitz bound on the deviation payoff between scanned orders; it closes the
finite-grid check only when an analytical cover applies or the bound itself lies inside the
deviation acceptance, and it is otherwise recorded so that the row stays a numerical diagnostic.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .information import Schedule
from .params import Controls, Noise
from .validation import Validation, _marginal_grid

NA = "n/a"

BUDGET_COLUMNS = [
    "quadrature_error", "quadrature_target", "quadrature_error_refined", "quadrature_target_refined", "quadrature_refinement",
    "tail_truncation_bound", "tail_truncation_formula", "between_grid_spacing", "between_grid_lipschitz_bound",
    "between_grid_closed", "between_grid_coverage", "residual_approximation_error", "posterior_inversion_error",
    "entry_independent_error", "deviation_argmax_H", "deviation_gain_H", "deviation_argmax_L", "deviation_gain_L",
    "error_budget_breaches",
]


@dataclass(frozen=True)
class ErrorBudget:
    quadrature_error: float                 # |GL48 - GL24| over the declared order scan (both states)
    quadrature_target: float                # declared absolute target (C.0)
    quadrature_error_refined: float | None  # |GL64 - GL32| over the refined scan; None when no refined scan ran
    quadrature_target_refined: float        # declared target / 10 (refinement rule)
    quadrature_refinement: str              # how the x10 rule is implemented
    tail_truncation_bound: float            # C.0 tail bound of the exterior truncation (0 when tails are analytic)
    tail_truncation_formula: str
    between_grid_spacing: float             # spacing of the finest order grid scanned
    between_grid_lipschitz_bound: float     # (spacing/2) * sup|U'| with sup|U'| <= Delta_T (1 + 1/b) + k
    between_grid_closed: bool               # analytical cover, or grid gain + Lipschitz bound inside the acceptance
    between_grid_coverage: str
    residual_approximation_error: float     # max |A_theta(x) - A_theta^direct(x)| on the marginal flow grid
    posterior_inversion_error: float
    entry_independent_error: float
    deviation_argmax_H: float
    deviation_gain_H: float
    deviation_argmax_L: float
    deviation_gain_L: float
    breaches: tuple[str, ...]

    @property
    def within_targets(self) -> bool:
        return not self.breaches

    def row(self) -> dict:
        return {
            "quadrature_error": self.quadrature_error, "quadrature_target": self.quadrature_target,
            "quadrature_error_refined": NA if self.quadrature_error_refined is None else self.quadrature_error_refined,
            "quadrature_target_refined": self.quadrature_target_refined, "quadrature_refinement": self.quadrature_refinement,
            "tail_truncation_bound": self.tail_truncation_bound, "tail_truncation_formula": self.tail_truncation_formula,
            "between_grid_spacing": self.between_grid_spacing, "between_grid_lipschitz_bound": self.between_grid_lipschitz_bound,
            "between_grid_closed": self.between_grid_closed, "between_grid_coverage": self.between_grid_coverage,
            "residual_approximation_error": self.residual_approximation_error,
            "posterior_inversion_error": self.posterior_inversion_error, "entry_independent_error": self.entry_independent_error,
            "deviation_argmax_H": self.deviation_argmax_H, "deviation_gain_H": self.deviation_gain_H,
            "deviation_argmax_L": self.deviation_argmax_L, "deviation_gain_L": self.deviation_gain_L,
            "error_budget_breaches": "; ".join(self.breaches),
        }


def na_budget_row() -> dict:
    return {c: NA for c in BUDGET_COLUMNS}


def lipschitz_constant_U(sched: Schedule) -> float:
    """sup_{|q| <= 1} |dU/dq| <= sup|F| + sup|s F'| + k with |F| <= Delta_T and |F'| <= Delta_T / b (Laplace density ratio)."""
    Delta = sched.pay.Delta_T
    b = sched.prim.fb
    return Delta * (1.0 + 1.0 / b) + sched.prim.fk


def error_budget(val: Validation, sched: Schedule, controls: Controls, analytical_cover: bool = False) -> ErrorBudget:
    """Assemble the budget from a `validate` record; recompute the residual approximation error on the marginal grid."""
    breaches: list[str] = []
    refined = controls.tightened()
    q_err = float(val.quadrature_error)
    if q_err > controls.quadrature_absolute_target:
        breaches.append(f"quadrature_error={q_err:.3e} exceeds target {controls.quadrature_absolute_target:.1e}")
    q_ref: float | None = None
    ref_scans = [val.scans[k] for k in ("H_refined", "L_refined") if k in val.scans]
    if ref_scans:
        q_ref = float(max(max(rw[4] for rw in sc["rows"]) for sc in ref_scans))
        if q_ref > refined.quadrature_absolute_target:
            breaches.append(f"quadrature_error_refined={q_ref:.3e} exceeds target {refined.quadrature_absolute_target:.1e}")
        spacing = 2.0 / controls.refined_order_intervals
    else:
        breaches.append("refined deviation scan absent")
        spacing = 2.0 / controls.initial_order_intervals
    tb = float(val.tail_bound)
    if sched.prim.noise == Noise.LAPLACE:
        tail_formula = "exterior tails integrated analytically against the constant Laplace residual; truncation bound 0"
    else:
        tail_formula = "A_bar * 2 / (1 + exp((T - 1) / b)) per unit order with the C.0 truncation half-width T"
    if tb > controls.quadrature_absolute_target:
        breaches.append(f"tail_truncation_bound={tb:.3e} exceeds target {controls.quadrature_absolute_target:.1e}")
    L = lipschitz_constant_U(sched)
    lip = 0.5 * spacing * L
    eps_q = max(float(val.epsilon_q), float(val.epsilon_q_refined))
    closed = bool(analytical_cover or (eps_q + lip <= controls.deviation_gain_acceptance))
    coverage = ("analytical cover closes between-grid deviations" if analytical_cover else
                f"finite grid over [-1, 1] at spacing {spacing:.4g}; Lipschitz bound {lip:.3e} on unscanned gains"
                + ("" if closed else " (not enclosed within the deviation acceptance: numerical diagnostic)"))
    xs = _marginal_grid(sched, controls.initial_flow_halfwidth)
    resid = float(max(float(np.max(np.abs(sched.A(xs, s) - sched.A_direct(xs, s)))) for s in "HL"))
    if resid > controls.price_identity_acceptance:
        breaches.append(f"residual_approximation_error={resid:.3e}")
    inv = float(val.posterior_inversion_error)
    ent = float(val.entry_independent_error)
    if ent > controls.independent_formula_acceptance:
        breaches.append(f"entry_independent_error={ent:.3e}")

    def summary(state: str) -> tuple[float, float]:
        sc = val.scans.get(state + "_refined", val.scans.get(state))
        if sc is None:
            return float("nan"), float("nan")
        return float(sc["argmax_q"]), float(sc["max_gain"])

    aH, gH = summary("H")
    aL, gL = summary("L")
    return ErrorBudget(q_err, controls.quadrature_absolute_target, q_ref, refined.quadrature_absolute_target,
                       "Gauss-Legendre order 48 -> 64 and order intervals 400 -> 800; refined estimate checked against target/10",
                       tb, tail_formula, spacing, lip, closed, coverage, resid, inv, ent, aH, gH, aL, gL, tuple(breaches))
