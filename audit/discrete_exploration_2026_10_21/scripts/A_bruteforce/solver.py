"""Exact equilibrium correspondence for equal three-point noise.

The public interface is the command line. All economic arithmetic is rational.
Each family describes an entire set, rather than a sample of possible mixtures.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json
from typing import Any


@dataclass(frozen=True)
class Params:
    r: F = F(3)
    k: F = F(1, 50)
    lam: F = F(1)
    pi: F = F(1, 2)
    c_H: F = F(6)
    h: F = F(10)
    ell: F = F(1)
    p: F = F(1, 2)
    rho: F = F(1, 4)


@dataclass(frozen=True)
class Auction:
    t0: F
    th: F
    tl: F
    gh: F
    gl: F
    delta: F


@dataclass(frozen=True)
class Family:
    support: str
    beta_lo: F
    beta_hi: F
    left_closed: bool
    right_closed: bool
    rates: tuple[tuple[F, F], ...]
    coefficients: tuple[F, ...]
    relation: str
    rhs: F


def auction(p: Params) -> Auction:
    t0 = p.p * (1 - p.p / p.r)
    th = p.r / 2 + p.p**2 / (2 * p.r)
    tl = p.ell - (p.ell**2 - p.p**2) / (2 * p.r)
    return Auction(t0, th, tl, p.h - th,
                   (p.ell**2 - p.p**2) / (2 * p.r), th - tl)


def entry_bounds(p: Params, mu: F) -> tuple[F, F]:
    a = auction(p)
    gain = a.gl + mu * (a.gh - a.gl)
    if gain < p.c_H:
        return p.rho, p.rho
    if gain > p.c_H:
        return F(1), F(1)
    return p.rho, F(1)


def posteriors(p: Params, beta: F, belief: str) -> tuple[F, ...]:
    lower = p.pi * (1 - p.lam * beta) / (1 - p.pi * p.lam * beta)
    upper = F(1) if beta > 0 or belief == "IC" else p.pi
    return lower, p.pi, p.pi, upper


def beta_cells(p: Params) -> tuple[tuple[F, F, bool, bool], ...]:
    a = auction(p)
    tau = (p.c_H - a.gl) / (a.gh - a.gl)
    cuts = {F(0), F(1)}
    if tau != 1:
        root = (p.pi - tau) / (p.pi * p.lam * (1 - tau))
        if 0 < root < 1:
            cuts.add(root)
    ordered = sorted(cuts)
    cells = []
    for left, right in zip(ordered, ordered[1:]):
        cells.append((left, right, False, False))
        cells.append((right, right, True, True))
    return tuple(cells)


def feasible(rates: tuple[tuple[F, F], ...], coeff: tuple[F, ...],
             relation: str, rhs: F) -> bool:
    low = sum((c * bounds[0] for c, bounds in zip(coeff, rates)), F(0))
    high = sum((c * bounds[1] for c, bounds in zip(coeff, rates)), F(0))
    if relation == "<=":
        return low <= rhs
    if relation == ">":
        return high > rhs
    if relation == ">=":
        return high >= rhs
    return low <= rhs <= high


def solve(p: Params, belief: str = "IC", investor_tie: str = "any") -> tuple[Family, ...]:
    if not (0 < p.p < p.ell < p.r < p.h and 0 < p.pi < 1
            and 0 < p.lam <= 1 and 0 < p.rho < 1 and p.k > 0 and p.c_H > 0):
        raise ValueError("The declared domain requires positive cost and interior auction values.")
    a = auction(p)
    answer = []
    mu = posteriors(p, F(0), belief)
    rates = tuple(entry_bounds(p, m) for m in mu)
    coeff = (F(0), a.delta * (1 - p.pi) / 3,
             a.delta * (1 - p.pi) / 3, a.delta * (1 - mu[3]) / 3)
    if feasible(rates, coeff, "<=", p.k):
        answer.append(Family("N", F(0), F(0), True, True, rates, coeff, "<=", p.k))
    for left, right, lc, rc in beta_cells(p):
        pure = left == right == 1
        if investor_tie == "zero" and not pure:
            continue
        beta = (left + right) / 2
        mu = posteriors(p, beta, belief)
        rates = tuple(entry_bounds(p, m) for m in mu)
        coeff = (F(0), a.delta * (1 - p.pi) / 3,
                 a.delta * (1 - p.pi) / 3, F(0))
        relation = (">" if investor_tie == "zero" else ">=") if pure else "="
        if feasible(rates, coeff, relation, p.k):
            answer.append(Family("F" if pure else "M", left, right, lc, rc,
                                 rates, coeff, relation, p.k))
    return tuple(answer)


def rate_vertices(family: Family) -> tuple[tuple[F, ...], ...]:
    """Vertices of the closure of a box intersected with one linear constraint."""
    def dot(v: tuple[F, ...]) -> F:
        return sum((c * x for c, x in zip(family.coefficients, v)), F(0))

    def keep(v: tuple[F, ...]) -> bool:
        d = dot(v)
        if family.relation == "<=":
            return d <= family.rhs
        if family.relation in (">", ">="):
            return d >= family.rhs
        return d == family.rhs

    vertices = set()
    for vertex in product(*family.rates):
        if keep(vertex):
            vertices.add(vertex)
    for axis, c in enumerate(family.coefficients):
        if not c:
            continue
        for corner in product(*family.rates):
            value = (family.rhs - dot(corner) + c * corner[axis]) / c
            if family.rates[axis][0] <= value <= family.rates[axis][1]:
                vertex = tuple(value if j == axis else x for j, x in enumerate(corner))
                vertices.add(vertex)
    return tuple(sorted(vertices))


def witness(family: Family) -> tuple[F, tuple[F, ...]]:
    vertices = rate_vertices(family)
    rates = tuple(sum((v[j] for v in vertices), F(0)) / len(vertices) for j in range(4))
    beta = (family.beta_lo + family.beta_hi) / 2
    return beta, rates


def partitions(n: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    if n == 0:
        return ((),)
    result = []
    for old in partitions(n - 1):
        result.append(old + ((n - 1,),))
        for i in range(len(old)):
            result.append(old[:i] + (old[i] + (n - 1,),) + old[i + 1:])
    return tuple(result)


def price_partitions(p: Params, family: Family, belief: str) -> tuple:
    """Enumerate the 15 partitions and retain every feasible price pattern."""
    beta = (family.beta_lo + family.beta_hi) / 2
    mu = posteriors(p, beta, belief)
    result = []
    for partition in partitions(4):
        if any(len({mu[i] for i in block}) > 1 for block in partition):
            continue
        bounds = tuple((max(family.rates[i][0] for i in block),
                        min(family.rates[i][1] for i in block)) for block in partition)
        if any(lo > hi for lo, hi in bounds):
            continue
        coeff = tuple(sum((family.coefficients[i] for i in block), F(0)) for block in partition)
        if not feasible(bounds, coeff, family.relation, family.rhs):
            continue
        collapsed = Family(family.support, family.beta_lo, family.beta_hi,
                           family.left_closed, family.right_closed, bounds, coeff,
                           family.relation, family.rhs)
        vertices = rate_vertices(collapsed)
        forced_alias = any(mu[first[0]] == mu[second[0]]
                           and all(v[i] == v[j] for v in vertices)
                           for i, first in enumerate(partition)
                           for j, second in enumerate(partition) if i < j)
        if not forced_alias:
            result.append(tuple(tuple(i - 1 for i in block) for block in partition))
    return tuple(result)


def outcomes(p: Params, beta: F, rates: tuple[F, ...], belief: str) -> dict[str, Any]:
    a = auction(p)
    mu = posteriors(p, beta, belief)
    f_h = ((1 - p.lam * beta) / 3, F(1, 3), F(1, 3), p.lam * beta / 3)
    f_l = (F(1, 3), F(1, 3), F(1, 3), F(0))
    mass = tuple(p.pi * h + (1 - p.pi) * l for h, l in zip(f_h, f_l))
    price = tuple(a.t0 + e * (a.tl - a.t0 + a.delta * m) for e, m in zip(rates, mu))
    e_h = sum((f * e for f, e in zip(f_h, rates)), F(0))
    e_l = sum((f * e for f, e in zip(f_l, rates)), F(0))
    entry = p.pi * e_h + (1 - p.pi) * e_l
    ownership = p.pi * e_h
    receipts = a.t0 + ownership * (a.th - a.t0) + (1 - p.pi) * e_l * (a.tl - a.t0)
    high_profit = sum((a.t0 + rates[i] * (a.th - a.t0) - price[i]
                       for i in (1, 2, 3)), F(0)) / 3 - p.k
    low_profit = sum((a.t0 + rates[i] * (a.tl - a.t0) - price[i]
                      for i in (1, 2, 3)), F(0)) / 3 - p.k
    groups: dict[F, list[int]] = {}
    for flow, pr in zip((-1, 0, 1, 2), price):
        groups.setdefault(pr, []).append(flow)
    return {"beta_H": beta, "beta_L": F(0), "posteriors": mu,
            "entry_rates": rates, "sigma": tuple((e - p.rho) / (1 - p.rho) for e in rates),
            "prices": price, "price_partition": tuple(groups.values()), "flow_mass": mass,
            "E": entry, "O_H": ownership, "R_T": receipts,
            "U_H_buy": high_profit, "U_L_buy": low_profit}


def family_record(p: Params, family: Family, belief: str) -> dict[str, Any]:
    beta, rates = witness(family)
    vals = [outcomes(p, b, v, belief) for b in (family.beta_lo, family.beta_hi)
            for v in rate_vertices(family)]
    ranges = {key: (min(v[key] for v in vals), max(v[key] for v in vals))
              for key in ("E", "O_H", "R_T")}
    return {"support": family.support,
            "beta_interval": (family.beta_lo, family.beta_hi),
            "closed": (family.left_closed, family.right_closed),
            "entry_rate_bounds": family.rates,
            "rate_constraint": {"coefficients": family.coefficients,
                                "relation": family.relation, "rhs": family.rhs},
            "feasible_price_partitions": price_partitions(p, family, belief),
            "outcome_closure_ranges": ranges,
            "representative": outcomes(p, beta, rates, belief)}


def encode(value: Any) -> Any:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name, default in (("r", "3"), ("k", "1/50"), ("lam", "1"),
                          ("pi", "1/2"), ("c-H", "6")):
        parser.add_argument("--" + name, default=default, type=F)
    parser.add_argument("--belief", choices=("IC", "passive"), default="IC")
    parser.add_argument("--investor-tie", choices=("any", "zero"), default="any")
    args = parser.parse_args()
    p = Params(r=args.r, k=args.k, lam=args.lam, pi=args.pi, c_H=args.c_H)
    answer = {"parameters": vars(p), "belief": args.belief, "investor_tie": args.investor_tie,
              "challenger_tie": "any mixture", "rate_order": (-1, 0, 1, 2),
              "families": [family_record(p, f, args.belief)
                           for f in solve(p, args.belief, args.investor_tie)]}
    print(json.dumps(encode(answer), indent=2))


if __name__ == "__main__":
    main()
