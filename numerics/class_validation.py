"""Independent acceptance for C.10, under the unchanged C.0 controls."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import exp, inf

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

from .class_exhibit import ClassCase, ClassNode, Condition, schedule
from .deviations import deviation_scan
from .params import Controls


@dataclass(frozen=True)
class ClassValidation:
    accepted: bool
    formula_error: float
    quadrature_error: float
    quadrature_error_refined: float
    epsilon_P: float
    epsilon_e: float
    epsilon_q: float
    epsilon_q_refined: float
    posterior_inversion_error: float
    probability_error: float
    tail_bound: float
    breaches: tuple[str, ...]
    deviations: tuple[tuple[str, str, str, float, float, float, float, float, float], ...]


def auction_oracle(case: ClassCase, r: float, controls: Controls) -> tuple[tuple[float, ...], float]:
    """Integrate realized auction receipts, profit, and wins over both values."""
    p = case.prim.fp
    errors: list[float] = []

    def integral(fun, lo: float, hi: float, points: list[float]) -> float:
        if hi == lo:
            return 0.0
        cuts = sorted({lo, hi, *(x for x in points if lo < x < hi)})
        total = 0.0
        local_errors = []
        for left, right in zip(cuts[:-1], cuts[1:]):
            value, error = quad(fun, left, right, epsabs=controls.quadrature_absolute_target/len(cuts), epsrel=0)
            total += value
            local_errors.append(error)
        errors.append(sum(local_errors))
        return total

    def conditional(theta: float, component: int) -> float:
        def realized(R: float) -> float:
            if component == 0:
                return max(p, min(R, theta)) / r
            if component == 1:
                return max(theta-max(p, R), 0.0) / r
            return float(theta >= p and theta > R) / r
        return integral(realized, 0.0, r, [p, theta])

    averages = []
    for support in (case.high_support, case.low_support):
        lo, hi = map(float, map(Decimal, support))
        for component in range(3):
            averages.append(conditional(lo, component) if lo == hi else
                            integral(lambda theta: conditional(theta, component)/(hi-lo), lo, hi, [p, r]))
    t0 = integral(lambda R: p*float(R >= p)/r, 0.0, r, [p])
    tH, gH, wH, tL, gL, wL = averages
    return (t0, tH, tL, gH, gL, wH, wL), max(errors, default=0.0)


def validate_case(case: ClassCase, nodes: tuple[ClassNode, ...], conditions: tuple[Condition, ...],
                  controls: Controls) -> ClassValidation:
    """Use direct auction integrals, density Bayes, and all unilateral orders on two grids."""
    prim = case.prim
    pi = float(Decimal(prim.fundamental_prior_H))
    rho, b, cost = prim.frho, prim.fb, prim.fc_H
    formula_errors: list[float] = []
    price_errors: list[float] = []
    entry_errors: list[float] = []
    inversion_errors: list[float] = []
    probability_errors: list[float] = []
    quadrature_errors = [[], []]
    gains = [[], []]
    tails = []
    deviations = []
    breaches = []
    by_name = {c.name: c for c in conditions}
    for condition in conditions:
        if condition.scope == "structural" or case.proposition_required and condition.scope != "diagnostic":
            if not condition.satisfied:
                breaches.append(f"condition {condition.name}")
    for name in ("A1_lower", "A2_lower", "A2_upper", "collapse_exclusion", "collapse_trade"):
        if not by_name[name].satisfied:
            breaches.append(f"outcome condition {name}")

    for item in nodes:
        sched = schedule(case, item)
        qH, qL = sched.profile.q_H[0], sched.profile.q_L[0]
        expected = [float(getattr(item.pay, key)) for key in ("t_0", "t_H", "t_L", "g_H", "g_L", "W_H", "W_L")]
        for pass_index, settings in enumerate((controls, controls.tightened())):
            oracle, error = auction_oracle(case, float(Decimal(item.r)), settings)
            quadrature_errors[pass_index].append(error)
            formula_errors.extend(abs(a-z) for a, z in zip(oracle, expected))
            t0, tH, tL, gH, gL, wH, _ = oracle

            def density(x: float, q: float) -> float:
                return exp(-abs(x-q)/b)/(2*b)

            def posterior(x: float) -> float:
                # Stable density ratio, including the infinite tails.
                aH = pi*exp((abs(x)-abs(x-qH))/b)
                aL = (1-pi)*exp((abs(x)-abs(x-qL))/b)
                return aH/(aH+aL)

            def entry(x: float) -> float:
                return rho + (1-rho)*float(gL+posterior(x)*(gH-gL) >= cost)

            cuts = {qH, qL}
            if qH != qL and gL+posterior(-1)*(gH-gL) < cost < gL+posterior(1)*(gH-gL):
                root = brentq(lambda x: gL+posterior(x)*(gH-gL)-cost, -1, 1, xtol=1e-14)
                cuts.add(root)
                formula_errors.append(abs(root-float(Decimal(item.x_star))))
            elif item.x_star not in ("n/a", "unattainable", "always"):
                breaches.append(f"unresolved threshold {item.node}")
            edges = [-inf, *sorted(cuts), inf]

            def full_integral(fun) -> float:
                pieces = [quad(fun, left, right, epsabs=settings.quadrature_absolute_target/len(edges), epsrel=0)
                          for left, right in zip(edges[:-1], edges[1:])]
                quadrature_errors[pass_index].append(sum(v[1] for v in pieces))
                return sum(v[0] for v in pieces)

            masses = [full_integral(lambda x: density(x, q)) for q in (qH, qL)]
            probability_errors.extend(abs(v-1) for v in masses)
            eH, eL = [full_integral(lambda x: density(x, q)*entry(x)) for q in (qH, qL)]
            mixture = lambda x: pi*density(x, qH)+(1-pi)*density(x, qL)
            average_mu = full_integral(lambda x: mixture(x)*posterior(x))
            price = lambda x: t0+entry(x)*(tL-t0+posterior(x)*(tH-tL))
            mean_price = full_integral(lambda x: mixture(x)*price(x))
            revenue = t0+pi*eH*(tH-t0)+(1-pi)*eL*(tL-t0)
            probability_errors.append(abs(average_mu-pi))
            price_errors.append(abs(mean_price-revenue))
            formula_errors.extend(abs(v-float(getattr(item, key))) for key, v in (
                ("e_H", eH), ("e_L", eL), ("E", pi*eH+(1-pi)*eL), ("O_H", pi*eH*wH), ("R_T", revenue)))
            points = np.array(sorted(set(np.linspace(-40, 40, 1601)) | cuts))
            mu = sched.mu(points)
            P = sched.price(points)
            e = sched.entry(points)
            independent_mu = np.array([posterior(x) for x in points])
            formula_errors.append(float(np.max(abs(mu-independent_mu))))
            direct_price = pi*np.exp(-abs(points-qH)/b)*(t0+e*(tH-t0)) + (1-pi)*np.exp(-abs(points-qL)/b)*(t0+e*(tL-t0))
            direct_price /= pi*np.exp(-abs(points-qH)/b)+(1-pi)*np.exp(-abs(points-qL)/b)
            price_errors.append(float(np.max(abs(P-direct_price))))
            if tH-tL > controls.independent_formula_acceptance:
                inversion_errors.append(float(np.max(abs((P-t0-e*(tL-t0))/(e*(tH-tL))-independent_mu))))
            elif item.branch != "pooling":
                breaches.append(f"nonpositive spread {item.node}")
            B = gL+independent_mu*(gH-gL)
            high_entry = (e-rho)/(1-rho)
            entry_errors.append(float(np.max(np.where(high_entry > 0.5, np.maximum(cost-B, 0), np.maximum(B-cost, 0)))))
            entry_errors.append(float(np.max(np.maximum(-B, 0))))
            intervals = controls.initial_order_intervals if pass_index == 0 else controls.refined_order_intervals
            for state in ("H", "L"):
                scan = deviation_scan(sched, state, intervals, list(cuts), n=48 if pass_index == 0 else 96)
                gains[pass_index].append(scan["max_gain"])
                quadrature_errors[pass_index].extend(row[4] for row in scan["rows"])
                tails.extend(row[5] for row in scan["rows"])
                deviations.extend((item.node, state, "initial" if pass_index == 0 else "refined", *row) for row in scan["rows"])

    maxima = [max(values, default=0.0) for values in (
        formula_errors, quadrature_errors[0], quadrature_errors[1], price_errors, entry_errors,
        gains[0], gains[1], inversion_errors, probability_errors, tails)]
    bounds = (controls.independent_formula_acceptance, controls.quadrature_absolute_target,
              controls.tightened().quadrature_absolute_target, controls.price_identity_acceptance,
              controls.entry_optimality_acceptance, controls.deviation_gain_acceptance,
              controls.deviation_gain_acceptance, controls.probability_acceptance, controls.probability_acceptance, 0.0)
    names = ("formula", "quadrature", "refined quadrature", "price", "entry", "deviation", "refined deviation", "inversion", "probability", "tail")
    for name, value, bound in zip(names, maxima, bounds):
        if not np.isfinite(value) or value > bound:
            breaches.append(f"{name}: {value} exceeds {bound}")
    return ClassValidation(not breaches, *maxima, tuple(breaches), tuple(deviations))


def independent_bounds(case: ClassCase, controls: Controls) -> dict[str, float]:
    """Locate each benchmark prior endpoint directly from its defining inequality."""
    prim = case.prim
    raw = [auction_oracle(case, float(Decimal(r)), controls)[0] for r in case.strengths]
    B = lambda index, mu: raw[index][4]+mu*(raw[index][3]-raw[index][4])
    delta = [row[1]-row[2] for row in raw]
    m = lambda pi: pi/(pi+(1-pi)*exp(2/prim.fb))
    M = lambda pi: pi/(pi+(1-pi)*exp(-2/prim.fb))
    cap = lambda pi: (1-1/prim.fb)*prim.frho*min(m(pi),1-M(pi))*delta[1]
    root = lambda f, left, right: brentq(f, left, right, xtol=1e-14)
    window_lo = root(lambda pi: cap(pi)-delta[0], 1e-6, .5)
    window_hi = root(lambda pi: cap(pi)-delta[0], .5, 1-1e-6)
    fixed_lo = root(lambda pi: cap(pi)-prim.fk, 1e-6, .5)
    fixed_hi = root(lambda pi: cap(pi)-prim.fk, .5, 1-1e-6)
    cost_lo = root(lambda pi: B(1,M(pi))-prim.fc_H, 1e-6, 1-1e-6)
    cost_hi = root(lambda pi: B(0,pi)-prim.fc_H, 1e-6, 1-1e-6)
    collapse_hi = root(lambda pi: B(2,M(pi))-prim.fc_H, 1e-6, 1-1e-6)
    out = dict(base_prior_window_lower=window_lo, base_prior_window_upper=window_hi,
               base_prior_fixed_k_lower=fixed_lo, base_prior_fixed_k_upper=fixed_hi,
               base_prior_A1_lower=cost_lo, base_prior_A1_upper=cost_hi,
               base_prior_prop2_lower=max(fixed_lo,cost_lo), base_prior_prop2_upper=min(fixed_hi,cost_hi),
               base_prior_collapse_upper=collapse_hi,
               base_prior_prop2_all_lower=max(fixed_lo,cost_lo), base_prior_prop2_all_upper=min(fixed_hi,cost_hi,collapse_hi),
               base_trade_cost_lower=delta[0], base_trade_cost_upper=cap(.5),
               base_trade_cost_lower_margin=prim.fk-delta[0], base_trade_cost_upper_margin=cap(.5)-prim.fk,
               base_spread_ratio=delta[0]/delta[1], base_spread_ratio_bound=cap(.5)/delta[1])
    for label, pi in (("03", .3), ("07", .7)):
        out.update({f"base_prior_{label}_cost_lower": B(0,pi), f"base_prior_{label}_cost_upper": B(1,M(pi)),
                    f"base_prior_{label}_trade_upper": cap(pi)})
    return out


@dataclass(frozen=True)
class BoundValidation:
    name: str
    independent_value: float
    absolute_difference: float
    accepted: bool


def validate_bounds(case: ClassCase, values: tuple, noise_entries: tuple[Decimal, ...],
                    controls: Controls) -> tuple[BoundValidation, ...]:
    reference = independent_bounds(case, controls)
    reference.update(four_noise_entry_min=float(min(noise_entries)), four_noise_entry_max=float(max(noise_entries)))
    rows = []
    for value in values:
        difference = abs(float(value.value)-reference[value.name])
        rows.append(BoundValidation(value.name, reference[value.name], difference,
                                    bool(np.isfinite(difference) and difference <= controls.independent_formula_acceptance)))
    return tuple(rows)
