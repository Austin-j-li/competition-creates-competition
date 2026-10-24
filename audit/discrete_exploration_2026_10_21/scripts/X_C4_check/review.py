"""Independent finite-tree calculation. All outputs are descriptive."""

from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import json
import mpmath as mm


STATES = ("HH", "HL", "LH", "LL")
PROFILES = tuple(product((0, 1), repeat=4))
ENTRY = tuple(product((0, 1), repeat=2))


class Economy:
    def __init__(self, r, cost, correlation="0", interval=False):
        self.interval = interval
        self.ctx = mm.iv if interval else mm.mp
        self.ctx.dps = 45 if interval else 75
        self.r = self.number(r)
        self.cost = self.number(cost)
        self.correlation = self.number(correlation)
        self.h = self.number(10)
        self.ell = self.number(1)
        self.reserve = self.number("1/2")
        self.rho = self.number("1/4")
        self.k = self.number("1/50")
        self.a = self.ctx.exp(-self.number("1/2"))
        self.up = 1 / (1 + self.a)
        self.down = self.a / (1 + self.a)
        self.prior = tuple(
            (1 + self.correlation * (1 if s in ("HH", "LL") else -1)) / 4
            for s in STATES
        )
        self.delta = (self.r - self.ell) ** 2 / (2 * self.r)
        self.t0 = self.reserve * (1 - self.reserve / self.r)
        self.tH = self.r / 2 + self.reserve ** 2 / (2 * self.r)
        self.tL = self.ell - (self.ell ** 2 - self.reserve ** 2) / (2 * self.r)
        self.gH = self.h - self.tH
        self.gL = self.ell - self.tL
        self.rent = self.gH - self.gL
        self.both = (self.h, self.ell + self.delta, self.ell + self.delta, self.ell)
        self.no_allocation = (self.r ** 2 - self.reserve ** 2) / (2 * self.r)

    def number(self, value):
        f = Fraction(str(value))
        return self.ctx.mpf(f.numerator) / f.denominator

    def sign(self, x):
        if self.interval:
            return 1 if x.a > 0 else (-1 if x.b < 0 else 0)
        return 1 if x > self.ctx.mpf("1e-60") else (-1 if x < -self.ctx.mpf("1e-60") else 0)

    def text(self, x):
        if self.interval:
            return str(x)
        return self.ctx.nstr(x, 18)

    def probabilities(self, orders):
        good = tuple(self.down + q * (self.up - self.down) for q in orders)
        return good, tuple(1 - p for p in good)

    def update(self, prior, orders):
        likelihood = self.probabilities(orders)
        masses = tuple(sum(prior[s] * likelihood[y][s] for s in range(4)) for y in range(2))
        posterior = tuple(
            tuple(prior[s] * likelihood[y][s] / masses[y] for s in range(4))
            for y in range(2)
        )
        return likelihood, masses, posterior

    def rate(self, choice):
        return self.rho + (1 - self.rho) * choice

    def gain2(self, posterior, prepared):
        if prepared:
            return self.rent * posterior[2]
        return self.gL + self.rent * (posterior[0] + posterior[2])

    def terminal(self, state, prepared, rate2):
        s = STATES[state]
        if prepared:
            first = self.tH if s[0] == "H" else self.tL
            return first + rate2 * (self.both[state] - first)
        second = self.tH if s[1] == "H" else self.tL
        return self.t0 + rate2 * (second - self.t0)

    def solve2(self, prior, prepared):
        candidates = []
        unresolved = 0
        smallest = None
        for orders in PROFILES:
            likelihood, masses, posterior = self.update(prior, orders)
            for expensive in ENTRY:
                rates = tuple(self.rate(e) for e in expensive)
                values = tuple(
                    tuple(self.terminal(s, prepared, rates[y]) for s in range(4))
                    for y in range(2)
                )
                prices = tuple(sum(posterior[y][s] * values[y][s] for s in range(4)) for y in range(2))
                margins = tuple(
                    self.up * (values[0][s] - prices[0])
                    + self.down * (values[1][s] - prices[1]) - self.k
                    for s in range(4)
                )
                gains = tuple(self.gain2(posterior[y], prepared) for y in range(2))
                conditions = tuple((2 * orders[s] - 1) * margins[s] for s in range(4))
                conditions += tuple((2 * expensive[y] - 1) * (gains[y] - self.cost) for y in range(2))
                signs = tuple(self.sign(c) for c in conditions)
                if -1 in signs:
                    continue
                gap = self.sign(prices[0] - prices[1])
                uninformative = len(set(orders)) == 1
                if not gap and not uninformative:
                    unresolved += 1
                    continue
                if 0 in signs:
                    unresolved += 1
                    continue
                if not gap and expensive[0] != expensive[1]:
                    continue
                lower = min(float(c.a) if self.interval else float(c) for c in conditions)
                smallest = lower if smallest is None else min(smallest, lower)
                mean_entry = tuple(sum(likelihood[y][s] * rates[y] for y in range(2)) for s in range(4))
                continuation = tuple(sum(likelihood[y][s] * values[y][s] for y in range(2)) for s in range(4))
                candidates.append(dict(
                    orders=orders, expensive=expensive, rates=rates, prices=prices,
                    margins=margins, gains=gains, posterior=posterior,
                    likelihood=likelihood, mean_entry=mean_entry, continuation=continuation,
                ))
        return candidates, unresolved, smallest

    def pooled2(self, prior, prepared):
        counts = {"considered": 0, "price_excludes": 0, "margin_excludes": 0, "unresolved": 0}
        entry_sign = self.sign(self.gain2(prior, prepared) - self.cost)
        if entry_sign:
            rate = self.number(1) if entry_sign > 0 else self.rho
        elif self.interval:
            rate = self.ctx.mpf([self.rho.a, 1])
        else:
            counts["unresolved"] += 14
            return counts
        values = tuple(self.terminal(s, prepared, rate) for s in range(4))
        for orders in PROFILES:
            if len(set(orders)) == 1:
                continue
            counts["considered"] += 1
            likelihood, masses, posterior = self.update(prior, orders)
            prices = tuple(sum(posterior[y][s] * values[s] for s in range(4)) for y in range(2))
            if self.sign(prices[0] - prices[1]):
                counts["price_excludes"] += 1
                continue
            conditions = tuple((2 * orders[s] - 1) * (
                self.up * (values[s] - prices[0])
                + self.down * (values[s] - prices[1]) - self.k
            ) for s in range(4))
            if any(self.sign(c) < 0 for c in conditions):
                counts["margin_excludes"] += 1
            else:
                counts["unresolved"] += 1
        return counts

    def solve(self):
        equilibria = []
        diagnostics = {"subgames": 0, "unresolved_subgame_candidates": 0,
                       "subgame_counts": {}, "unresolved_first_candidates": 0,
                       "unseparated_surviving_first_candidates": 0, "smallest_margin": 100.0,
                       "second_pools": {"considered": 0, "price_excludes": 0,
                                        "margin_excludes": 0, "unresolved": 0}}
        for orders in PROFILES:
            likelihood, masses, posterior = self.update(self.prior, orders)
            branches = {}
            for y, prepared in product(range(2), range(2)):
                solutions, unresolved, smallest = self.solve2(posterior[y], prepared)
                branches[y, prepared] = solutions
                pools = self.pooled2(posterior[y], prepared)
                for key,value in pools.items():
                    diagnostics["second_pools"][key] += value
                diagnostics["subgames"] += 1
                diagnostics["unresolved_subgame_candidates"] += unresolved
                n = len(solutions)
                diagnostics["subgame_counts"][n] = diagnostics["subgame_counts"].get(n, 0) + 1
                if smallest is not None:
                    diagnostics["smallest_margin"] = min(diagnostics["smallest_margin"], smallest)
            branch_keys = tuple(branches)
            for combination in product(*(branches[key] for key in branch_keys)):
                continuation = dict(zip(branch_keys, combination))
                gains1 = tuple(sum(
                    posterior[y][s] * (
                        (1 - continuation[y, 1]["mean_entry"][s])
                        * (self.gH if STATES[s][0] == "H" else self.gL)
                        + continuation[y, 1]["mean_entry"][s] * self.rent * (s == 1)
                    ) for s in range(4)
                ) for y in range(2))
                for expensive in ENTRY:
                    rates = tuple(self.rate(e) for e in expensive)
                    values = tuple(tuple(
                        rates[y] * continuation[y, 1]["continuation"][s]
                        + (1 - rates[y]) * continuation[y, 0]["continuation"][s]
                        for s in range(4)
                    ) for y in range(2))
                    prices = tuple(sum(posterior[y][s] * values[y][s] for s in range(4)) for y in range(2))
                    margins = tuple(
                        self.up * (values[0][s] - prices[0])
                        + self.down * (values[1][s] - prices[1]) - self.k
                        for s in range(4)
                    )
                    conditions = tuple((2 * orders[s] - 1) * margins[s] for s in range(4))
                    conditions += tuple((2 * expensive[y] - 1) * (gains1[y] - self.cost) for y in range(2))
                    signs = tuple(self.sign(c) for c in conditions)
                    if -1 in signs:
                        continue
                    if 0 in signs:
                        diagnostics["unresolved_first_candidates"] += 1
                        continue
                    if not self.sign(prices[0] - prices[1]):
                        diagnostics["unseparated_surviving_first_candidates"] += 1
                        continue
                    lower = min(float(c.a) if self.interval else float(c) for c in conditions)
                    diagnostics["smallest_margin"] = min(diagnostics["smallest_margin"], lower)
                    eq = dict(orders=orders, expensive=expensive, rates=rates,
                              prices=prices, margins=margins, gains=gains1,
                              posterior=posterior, likelihood=likelihood,
                              masses=masses, branches=continuation)
                    eq["outcomes"] = self.outcomes(eq)
                    equilibria.append(eq)
        return equilibria, diagnostics

    def outcomes(self, eq):
        total = {key: self.number(0) for key in
                 ("E1", "E2", "both", "owner_H", "proceeds", "allocation", "trade_cost")}
        for s, y in product(range(4), range(2)):
            mass1 = self.prior[s] * eq["likelihood"][y][s]
            rate1 = eq["rates"][y]
            total["E1"] += mass1 * rate1
            total["trade_cost"] += mass1 * self.k * eq["orders"][s]
            for d1 in range(2):
                massd = mass1 * (rate1 if d1 else 1 - rate1)
                branch = eq["branches"][y, d1]
                total["trade_cost"] += massd * self.k * branch["orders"][s]
                for z, d2 in product(range(2), range(2)):
                    rate2 = branch["rates"][z]
                    mass = massd * branch["likelihood"][z][s] * (rate2 if d2 else 1 - rate2)
                    total["E2"] += mass * d2
                    total["both"] += mass * d1 * d2
                    j1, j2 = STATES[s]
                    high = (d1 and j1 == "H") or (d2 and j2 == "H")
                    low = (d1 and j1 == "L") or (d2 and j2 == "L")
                    allocation = self.h if high else (self.ell + self.delta if low else self.no_allocation)
                    if d1 and d2:
                        payment = self.both[s]
                    elif d1:
                        payment = self.tH if j1 == "H" else self.tL
                    elif d2:
                        payment = self.tH if j2 == "H" else self.tL
                    else:
                        payment = self.t0
                    total["owner_H"] += mass * int(high)
                    total["allocation"] += mass * allocation
                    total["proceeds"] += mass * payment
        total["preparation_cost"] = self.cost * (total["E1"] + total["E2"] - 2 * self.rho)
        total["net_surplus"] = total["allocation"] - total["preparation_cost"]
        total["E2_given_1"] = total["both"] / total["E1"]
        if self.sign(1 - total["E1"]):
            total["E2_given_0"] = (total["E2"] - total["both"]) / (1 - total["E1"])
        return total

    def serial(self, eq):
        return dict(
            orders=eq["orders"], expensive=eq["expensive"],
            prices=[self.text(x) for x in eq["prices"]],
            margins=[self.text(x) for x in eq["margins"]],
            gains=[self.text(x) for x in eq["gains"]],
            posterior=[[self.text(x) for x in p] for p in eq["posterior"]],
            outcomes={k: self.text(v) for k, v in eq["outcomes"].items()},
            branches={f"{y},{d}": dict(
                orders=b["orders"], expensive=b["expensive"],
                prices=[self.text(x) for x in b["prices"]],
                gains=[self.text(x) for x in b["gains"]],
                margins=[self.text(x) for x in b["margins"]],
            ) for (y, d), b in eq["branches"].items()},
        )


def bounds():
    mm.iv.dps = 45
    for corr in ("-1/2", "0", "1/2"):
        for strength in ("6/5", "3", "18/5", "10"):
            e = Economy(strength, "5", corr, True)
            def psi(pi, rounds):
                return pi / (pi + e.a ** rounds * (1 - pi))
            after_entry = e.rent * psi(e.prior[2], 2)
            first_buy = e.rho ** 2 * (1 - psi(e.prior[0], 1)) * e.rent
            second_buy = e.rho * (1 - psi(e.prior[0], 2)) * e.rent
            second_no = e.a ** 2 * (e.prior[0] / e.prior[3]) * (
                (1 - e.rho) * e.delta + e.rho * e.rent) - e.rho * e.delta
            print(json.dumps(dict(r=strength, correlation=corr,
                                  a=e.text(e.a), NC_threshold=e.text(after_entry),
                                  first_buy_bound=e.text(first_buy),
                                  second_buy_bound=e.text(second_buy),
                                  LH_no_buy_slack=e.text(second_no))))


def thresholds():
    mm.mp.dps = 75
    a = mm.mp.exp(-mm.mp.mpf(1) / 2)
    for r in ("6/5", "3", "18/5"):
        e = Economy(r, "5")
        mu_good = (1 + a) / (1 + 3 * a)
        mu_gg = (1 + a) / (1 + a + 2 * a * a)
        mu_bg = (1 + a) / (1 + 3 * a)
        print(json.dumps(dict(r=r,
            first_good_gain=e.text((1-e.rho)*e.gL+e.rent*(1-e.rho+a)/(1+3*a)),
            second_after_good_no_trade=e.text(e.gL+e.rent*mu_good),
            second_after_good_good=e.text(e.gL+e.rent*mu_gg),
            second_after_bad_good=e.text(e.gL+e.rent*mu_bg))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("point", "benchmarks", "bounds", "thresholds"))
    parser.add_argument("--r", default="3")
    parser.add_argument("--cost", default="5")
    parser.add_argument("--correlation", default="0")
    parser.add_argument("--interval", action="store_true")
    args = parser.parse_args()
    if args.mode == "bounds":
        bounds()
        return
    if args.mode == "thresholds":
        thresholds()
        return
    points = [(args.r, args.cost)] if args.mode == "point" else list(product(("6/5", "3", "18/5"), ("5", "29/5")))
    for r, cost in points:
        e = Economy(r, cost, args.correlation, args.interval)
        solutions, diagnostic = e.solve()
        print(json.dumps(dict(r=r, cost=cost, correlation=args.correlation,
                              interval=args.interval, a=e.text(e.a), diagnostic=diagnostic,
                              equilibria=[e.serial(s) for s in solutions])), flush=True)


if __name__ == "__main__":
    main()
