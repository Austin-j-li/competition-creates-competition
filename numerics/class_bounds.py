"""C.10 registry scalars from the manuscript's exact benchmark definitions."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext

from .class_exhibit import ClassCase, payoffs, posterior_bounds
from .params import BENCHMARK, CONTROLS

D = Decimal
BENCHMARK_CASE = ClassCase("benchmark_bounds", BENCHMARK, ("1.2", "3", "3.6"), ("1", "1"), ("10", "10"))


@dataclass(frozen=True)
class Bound:
    name: str
    value: Decimal
    definition: str
    display: str
    units: str
    scope: str


def benchmark_bounds(case: ClassCase, noise_entries: tuple[Decimal, ...]) -> tuple[Bound, ...]:
    with localcontext() as ctx:
        ctx.prec = CONTROLS.interval_decimal_precision
        prim = case.prim
        weak, strong, collapse = (payoffs(case, D(r)) for r in case.strengths)
        coefficient = (1-1/D(prim.b))*D(prim.rho)
        cost, k = D(prim.c_H), D(prim.k)
        exp_score = (2/D(prim.b)).exp()
        inverse_m = lambda q: q*exp_score/(1-q+q*exp_score)
        inverse_M = lambda q: q/(q+(1-q)*exp_score)
        window_lo = inverse_m(weak.Delta_T/(coefficient*strong.Delta_T))
        fixed_lo = inverse_m(k/(coefficient*strong.Delta_T))
        cost_lo = inverse_M((cost-strong.g_L)/(strong.g_H-strong.g_L))
        cost_hi = (cost-weak.g_L)/(weak.g_H-weak.g_L)
        collapse_hi = inverse_M((cost-collapse.g_L)/(collapse.g_H-collapse.g_L))
        lower, upper = max(fixed_lo,cost_lo), min(1-fixed_lo,cost_hi)
        bound = coefficient*posterior_bounds(prim)[2]
        values = (
            ("base_prior_window_lower", window_lo, "Lower prior endpoint for a nonempty A2 cost window; c_H and k are not fixed by this criterion.", "trade window"),
            ("base_prior_window_upper", 1-window_lo, "Upper prior endpoint for a nonempty A2 cost window; c_H and k are not fixed by this criterion.", "trade window"),
            ("base_prior_fixed_k_lower", fixed_lo, "Lower prior endpoint from A2 at the fixed benchmark k.", "fixed trade cost"),
            ("base_prior_fixed_k_upper", 1-fixed_lo, "Upper prior endpoint from A2 at the fixed benchmark k.", "fixed trade cost"),
            ("base_prior_A1_lower", cost_lo, "Lower prior endpoint from c_H < B_r1(M(pi)).", "fixed high cost"),
            ("base_prior_A1_upper", cost_hi, "Upper prior endpoint from B_r0(pi) < c_H.", "fixed high cost"),
            ("base_prior_prop2_lower", lower, "Lower prior endpoint for all Proposition 2(i)-(ii) hypotheses with the fixed benchmark vector.", "fixed benchmark pair"),
            ("base_prior_prop2_upper", upper, "Upper prior endpoint for all Proposition 2(i)-(ii) hypotheses with the fixed benchmark vector.", "fixed benchmark pair"),
            ("base_prior_collapse_upper", collapse_hi, "Upper prior endpoint for B_r2(M(pi)) < c_H at the fixed benchmark collapse strength.", "fixed collapse strength"),
            ("base_prior_prop2_all_lower", lower, "Lower prior endpoint for Proposition 2(i)-(iii) with all three benchmark strengths fixed.", "fixed benchmark triple"),
            ("base_prior_prop2_all_upper", min(upper,collapse_hi), "Upper prior endpoint for Proposition 2(i)-(iii) with all three benchmark strengths fixed.", "fixed benchmark triple"),
        )
        rows = [Bound(name,value,definition,"decimal_6","probability",scope) for name,value,definition,scope in values]
        for name, value, definition, units, display in (
            ("base_trade_cost_lower", weak.Delta_T, "Strict lower bound Delta_T(r_0) on the benchmark trade cost.", "payoff per marginal order", "decimal_4"),
            ("base_trade_cost_upper", bound*strong.Delta_T, "Strict upper bound (1-1/b)rho*kappa(1/2)*Delta_T(r_1) on the benchmark trade cost.", "payoff per marginal order", "decimal_4"),
            ("base_trade_cost_lower_margin", k-weak.Delta_T, "Benchmark k minus its strict lower bound.", "payoff margin", "decimal_6"),
            ("base_trade_cost_upper_margin", bound*strong.Delta_T-k, "Benchmark strict upper trade bound minus k.", "payoff margin", "decimal_6"),
            ("base_spread_ratio", weak.Delta_T/strong.Delta_T, "Benchmark Delta_T(r_0)/Delta_T(r_1).", "bound", "decimal_3"),
            ("base_spread_ratio_bound", bound, "Benchmark (1-1/b)rho*kappa(1/2).", "bound", "decimal_3"),
        ):
            rows.append(Bound(name,value,definition,display,units,"benchmark window"))
        for label, pi in (("03","0.3"),("07","0.7")):
            _, M, kappa = posterior_bounds(prim.with_(fundamental_prior_H=pi))
            for suffix, value, definition in (
                ("cost_lower", weak.B(D(pi)), "B_r0(pi) at the benchmark strengths"),
                ("cost_upper", strong.B(M), "B_r1(M(pi)) at the benchmark strengths"),
                ("trade_upper", coefficient*kappa*strong.Delta_T, "A2 upper trade bound at the benchmark strengths"),
            ):
                rows.append(Bound(f"base_prior_{label}_{suffix}",value,definition+f" and prior {pi}.","decimal_6","payoff margin","benchmark prior variant"))
        for suffix, value in (("min",min(noise_entries)),("max",max(noise_entries))):
            rows.append(Bound(f"four_noise_entry_{suffix}",value,
                              f"{suffix.capitalize()} strong entry across Laplace, logistic, hyperbolic secant, and Student t3; atomic costs; additional laws use fixed full orders.",
                              "decimal_6","probability","fixed-profile noise range"))
        return tuple(rows)
