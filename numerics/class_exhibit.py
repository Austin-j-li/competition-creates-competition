"""C.10: exact declarations and closed forms for quality classes and general priors."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext

import numpy as np
from scipy.special import expit

from .auction import AuctionPayoffs
from .information import OrderProfile, Schedule
from .params import BENCHMARK, CONTROLS, Primitives

D = Decimal


@dataclass(frozen=True)
class ClassCase:
    name: str
    prim: Primitives
    strengths: tuple[str, str, str]
    low_support: tuple[str, str]
    high_support: tuple[str, str]
    proposition_required: bool = True

    def columns(self) -> dict[str, str]:
        return {**self.prim.columns(), "case": self.name,
                "fundamental_prior_H": self.prim.fundamental_prior_H,
                "noise": self.prim.noise.value, "cost_law": self.prim.cost_law.value,
                "value_law": "point_mass" if self.low_support[0] == self.low_support[1] else "uniform_classes",
                "a_L": self.low_support[0], "b_L": self.low_support[1],
                "a_H": self.high_support[0], "b_H": self.high_support[1],
                **dict(zip(("r_0", "r_1", "r_2"), self.strengths))}


CASES = (
    ClassCase("prior_03", BENCHMARK.with_(fundamental_prior_H="0.3", c_H="4.5", k="0.01"),
              ("1.1", "3", "3.6"), ("1", "1"), ("10", "10")),
    ClassCase("prior_07", BENCHMARK.with_(fundamental_prior_H="0.7", c_H="7.2", k="0.01"),
              ("1.1", "3", "3.6"), ("1", "1"), ("10", "10")),
    ClassCase("wide_07", BENCHMARK.with_(fundamental_prior_H="0.7", c_H="6.7"),
              ("1", "4.5", "5.5"), ("0.6", "1.4"), ("1", "19")),
    ClassCase("matched_point_07", BENCHMARK.with_(fundamental_prior_H="0.7", c_H="6.7"),
              ("1", "4.5", "5.5"), ("1", "1"), ("10", "10"), False),
)


@dataclass(frozen=True)
class ClassPayoffs:
    t_0: Decimal
    t_H: Decimal
    t_L: Decimal
    g_H: Decimal
    g_L: Decimal
    W_H: Decimal
    W_L: Decimal

    @property
    def Delta_T(self) -> Decimal:
        return self.t_H - self.t_L

    def B(self, mu: Decimal) -> Decimal:
        return self.g_L + mu * (self.g_H - self.g_L)


def class_average(prim: Primitives, r: Decimal, support: tuple[str, str]) -> tuple[Decimal, Decimal, Decimal]:
    """Integrate the auction polynomials for a point or uniform class above the reserve."""
    a, z = map(D, support)
    p = D(prim.p)
    if not p <= a <= z or r <= p:
        raise ValueError("C.10 requires ordered supports above the reserve and r > p")
    cap = (r * r + p * p) / (2 * r)
    if a == z:
        gross = (a * a - p * p) / (2 * r) if a <= r else a - cap
        return a - gross, gross, min(a / r, D(1))
    u = min(z, r)
    gross = win = D(0)
    if u > a:
        gross += (u - a) * ((u * u + u * a + a * a) / 3 - p * p) / (2 * r)
        win += (u - a) * (u + a) / (2 * r)
    v = max(a, r)
    if z > v:
        gross += (z - v) * ((z + v) / 2 - cap)
        win += z - v
    gross /= z - a
    return (a + z) / 2 - gross, gross, win / (z - a)


def payoffs(case: ClassCase, r: Decimal) -> ClassPayoffs:
    prim = case.prim
    tH, gH, wH = class_average(prim, r, case.high_support)
    tL, gL, wL = class_average(prim, r, case.low_support)
    p = D(prim.p)
    return ClassPayoffs(p * (1 - p / r), tH, tL, gH, gL, wH, wL)


def posterior_bounds(prim: Primitives) -> tuple[Decimal, Decimal, Decimal]:
    pi, b = D(prim.fundamental_prior_H), D(prim.b)
    m = pi / (pi + (1 - pi) * (2 / b).exp())
    M = pi / (pi + (1 - pi) * (-2 / b).exp())
    return m, M, min(m, 1 - M)


@dataclass(frozen=True)
class ClassNode:
    r: str
    node: str
    branch: str
    pay: ClassPayoffs
    m: Decimal
    M: Decimal
    kappa: Decimal
    tau: Decimal
    x_star: str
    alpha_H: Decimal
    alpha_L: Decimal
    e_H: Decimal
    e_L: Decimal
    E: Decimal
    O_H: Decimal
    R_T: Decimal

    def columns(self, case: ClassCase) -> dict[str, str]:
        with localcontext() as ctx:
            ctx.prec = CONTROLS.interval_decimal_precision
            return self._columns(case)

    def _columns(self, case: ClassCase) -> dict[str, str]:
        pi = D(case.prim.fundamental_prior_H)
        result = {**case.columns(), "r": self.r, "node": self.node, "branch": self.branch,
                  "q_H": "0" if self.branch == "pooling" else "1",
                  "q_L": "0" if self.branch == "pooling" else "-1", "x_star": self.x_star}
        for key in ("m", "M", "kappa", "tau", "alpha_H", "alpha_L", "e_H", "e_L", "E", "O_H", "R_T"):
            result[key] = str(getattr(self, key))
        for key in ("t_0", "t_H", "t_L", "g_H", "g_L", "Delta_T", "W_H", "W_L"):
            result[key] = str(getattr(self.pay, key))
        result.update(B_m=str(self.pay.B(self.m)), B_prior=str(self.pay.B(pi)), B_M=str(self.pay.B(self.M)))
        return result


def node(case: ClassCase, index: int) -> ClassNode:
    prim = case.prim
    pi, rho, b, cost = map(D, (prim.fundamental_prior_H, prim.rho, prim.b, prim.c_H))
    rs = case.strengths[index]
    pay = payoffs(case, D(rs))
    m, M, kappa = posterior_bounds(prim)
    tau = (cost - pay.g_L) / (pay.g_H - pay.g_L)
    if index == 0:
        branch, x = "pooling", "n/a"
        aH = aL = D(int(pay.B(pi) >= cost))
    else:
        branch = "full_orders"
        if cost <= pay.B(m):
            x, aH, aL = "always", D(1), D(1)
        elif cost > pay.B(M):
            x, aH, aL = "unattainable", D(0), D(0)
        else:
            cutoff = b / 2 * ((tau / (1 - tau)).ln() - (pi / (1 - pi)).ln())
            x = str(cutoff)
            aH = 1 - ((cutoff - 1) / b).exp() / 2
            aL = (-(cutoff + 1) / b).exp() / 2
    eH, eL = rho + (1 - rho) * aH, rho + (1 - rho) * aL
    E = pi * eH + (1 - pi) * eL
    ownership = pi * eH * pay.W_H
    revenue = pay.t_0 + pi * eH * (pay.t_H - pay.t_0) + (1 - pi) * eL * (pay.t_L - pay.t_0)
    return ClassNode(rs, f"r_{index}", branch, pay, m, M, kappa, tau, x, aH, aL, eH, eL, E, ownership, revenue)


@dataclass(frozen=True)
class Condition:
    name: str
    margin: Decimal
    relation: str
    scope: str
    definition: str

    @property
    def satisfied(self) -> bool:
        if self.relation == "=0":
            return self.margin == 0
        if self.relation == ">=0":
            return self.margin >= 0
        return self.margin > D("1e-40")


def evaluate(case: ClassCase) -> tuple[tuple[ClassNode, ...], tuple[Condition, ...]]:
    """Evaluate every hypothesis, the ownership comparisons, and the zero-cost diagnostics."""
    with localcontext() as ctx:
        ctx.prec = CONTROLS.interval_decimal_precision
        nodes = tuple(node(case, i) for i in range(3))
        weak, strong, collapse = nodes
        prim = case.prim
        pi, rho, b, k, c = map(D, (prim.fundamental_prior_H, prim.rho, prim.b, prim.k, prim.c_H))
        aL, zL = map(D, case.low_support)
        aH, zH = map(D, case.high_support)
        coefficient = (1 - 1 / b) * rho * strong.kappa
        conditions = [Condition(name, margin, relation, "structural", definition) for name, margin, relation, definition in (
            ("pi_positive", pi, ">0", "pi"), ("pi_below_one", 1-pi, ">0", "1-pi"),
            ("rho_positive", rho, ">0", "rho"), ("rho_below_one", 1-rho, ">0", "1-rho"),
            ("b_above_one", b-1, ">0", "b-1"), ("k_positive", k, ">0", "k"),
            ("c_H_positive", c, ">0", "c_H"), ("p_positive", D(prim.p), ">0", "p"),
            ("zero_low_cost", D(prim.c_L), "=0", "c_L"),
            ("low_above_reserve", aL-D(prim.p), ">0", "a_L-p"),
            ("high_above_reserve", aH-D(prim.p), ">0", "a_H-p"),
            ("low_width", zL-aL, ">=0", "b_L-a_L"), ("high_width", zH-aH, ">=0", "b_H-a_H"),
            ("FOSD_lower", aH-aL, ">=0", "a_H-a_L"), ("FOSD_upper", zH-zL, ">=0", "b_H-b_L"),
            ("equal_admissibility", D(0), "=0", "G_L(p-)-G_H(p-); both supports exceed p"),
            ("mean_gap", (aH+zH-aL-zL)/2, ">0", "E_H max(theta,p)-E_L max(theta,p)"),
            ("weak_above_reserve", D(weak.r)-D(prim.p), ">0", "r_0-p"),
            ("first_strength_order", D(strong.r)-D(weak.r), ">0", "r_1-r_0"),
            ("second_strength_order", D(collapse.r)-D(strong.r), ">0", "r_2-r_1"),
        )]
        conditions.extend(Condition(*args) for args in (
            ("A1_lower", c-weak.pay.B(pi), ">0", "main", "c_H-B_r0(pi)"),
            ("A1_upper", strong.pay.B(strong.M)-c, ">0", "main", "B_r1(M(pi))-c_H"),
            ("A2_lower", k-weak.pay.Delta_T, ">0", "main", "k-Delta_T(r_0)"),
            ("A2_upper", coefficient*strong.pay.Delta_T-k, ">0", "main", "(1-1/b)rho*kappa(pi)*Delta_T(r_1)-k"),
            ("collapse_exclusion", c-collapse.pay.B(collapse.M), ">0", "collapse", "c_H-B_r2(M(pi))"),
            ("collapse_trade", coefficient*collapse.pay.Delta_T-k, ">0", "collapse", "(1-1/b)rho*kappa(pi)*Delta_T(r_2)-k"),
            ("ownership_sufficient", (1+rho)*strong.pay.W_H-2*rho*weak.pay.W_H, ">=0", "ownership", "(1+rho)W_H(r_1)-2rho*W_H(r_0)"),
            ("ownership_positive_base", 2*rho*weak.pay.W_H, ">0", "ownership", "2rho*W_H(r_0)"),
            ("ownership_exact", strong.e_H*strong.pay.W_H-rho*weak.pay.W_H, ">0", "ownership", "e_H(r_1)W_H(r_1)-rho*W_H(r_0)"),
        ))
        for item in nodes:
            conditions.extend((
                Condition(f"profit_gap_{item.node}", item.pay.g_H-item.pay.g_L, ">0", "structural", "g_H-g_L"),
                Condition(f"spread_{item.node}", item.pay.Delta_T, ">=0", "structural", "Delta_T"),
                Condition(f"low_cost_diagnostic_{item.node}", item.pay.B(item.m), ">=0", "diagnostic", "B_r(m(pi)); zero cost gives entry automatically"),
            ))
        return nodes, tuple(conditions)


@dataclass(frozen=True)
class PriorSchedule(Schedule):
    """The declared pure orders with the general prior in Bayes' rule."""

    def mu(self, x: np.ndarray) -> np.ndarray:
        pi = float(D(self.prim.fundamental_prior_H))
        x = np.asarray(x, dtype=float)
        log_odds = np.log(pi/(1-pi)) + (abs(x-self.profile.q_L[0])-abs(x-self.profile.q_H[0]))/self.prim.fb
        return expit(log_odds)


def schedule(case: ClassCase, item: ClassNode) -> PriorSchedule:
    p = item.pay
    pay = AuctionPayoffs(float(D(item.r)), case.prim.fp, *(float(getattr(p, key)) for key in ("t_0", "t_H", "t_L", "g_H", "g_L")))
    profile = OrderProfile.pure(0, 0) if item.branch == "pooling" else OrderProfile.pure(1, -1)
    points = set(profile.supports)
    if item.x_star not in ("n/a", "unattainable", "always"):
        points.add(float(D(item.x_star)))
    return PriorSchedule(case.prim, pay, profile, breakpoints=tuple(sorted(points)))
