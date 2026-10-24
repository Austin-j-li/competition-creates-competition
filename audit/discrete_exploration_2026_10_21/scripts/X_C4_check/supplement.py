"""Exact auction integrals and interval bounds for the review."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import mpmath as mm
from review import Economy, STATES


def auction_integral(strength, state, first, second, priority):
    r, p = F(strength), F(1, 2)
    values = {"I": None}
    if first:
        values["1"] = F(10 if state[0] == "H" else 1)
    if second:
        values["2"] = F(10 if state[1] == "H" else 1)
    cutoffs = sorted(set((F(0), p, F(1), r)))
    cutoffs = [x for x in cutoffs if 0 <= x <= r]
    total = {k: F(0) for k in ("payment", "allocation", "I", "1", "2")}
    for left, right in zip(cutoffs, cutoffs[1:]):
        midpoint = (left + right) / 2
        bids = dict(values)
        bids["I"] = midpoint
        active = [b for b in bids if bids[b] >= p]
        if not active:
            continue
        active.sort(key=lambda b: (-bids[b], priority.index(b)))
        winner = active[0]
        payment = max(p, bids[active[1]]) if len(active) > 1 else p
        weight = (right - left) / r
        total["payment"] += weight * payment
        total["allocation"] += weight * bids[winner]
        total[winner] += weight * (bids[winner] - payment)
    return total


def exact_auctions():
    for strength in ("6/5", "3", "18/5"):
        for state, d1, d2 in product(STATES, range(2), range(2)):
            left = auction_integral(strength, state, d1, d2, ("1", "2", "I"))
            right = auction_integral(strength, state, d1, d2, ("2", "1", "I"))
            difference = {k: str(left[k] - right[k]) for k in left}
            print(json.dumps(dict(kind="auction", r=strength, state=state, d1=d1, d2=d2,
                                  values={k: str(v) for k, v in left.items()},
                                  tie_rule_difference=difference)))


def bounds_at_weak_incumbent():
    for cost in ("5", "29/5"):
        e = Economy("6/5", cost, interval=True)
        min_first_HH = e.a / (e.a + 3)
        min_second_HH = e.a ** 2 / (e.a ** 2 + 3)
        max_first_HH = 1 / (1 + 3 * e.a)
        max_second_HH = 1 / (1 + 3 * e.a ** 2)
        mid_upper = (1-min_first_HH) * e.delta - min_first_HH * e.rho ** 2 * e.rent - e.k
        hh_lower = e.rho ** 2 * (1-max_first_HH) * e.rent - e.k
        high_second_lower = (1-max_second_HH) * e.rho * e.rent - e.k
        hl_second_upper = (1-min_second_HH) * e.delta - min_second_HH * e.rho * e.rent - e.k
        values = dict(NC_slack=e.cost-max_second_HH*e.rent,
                      no_second_trade_slack=e.k-e.delta,
                      first_middle_margin_upper=mid_upper,
                      first_HH_margin_lower=hh_lower,
                      second_HH_margin_lower=high_second_lower,
                      second_HL_margin_upper=hl_second_upper)
        print(json.dumps(dict(kind="weak_incumbent_bounds", cost=cost,
                              values={k:e.text(v) for k,v in values.items()})))


def interval_window():
    e = Economy("3", "5", interval=True)
    after_two_good = (1 + e.a) / (1 + e.a + 2 * e.a ** 2)
    for r in ("3", "18/5"):
        x = Economy(r, "5", interval=True)
        print(json.dumps(dict(kind="window_endpoint", r=r,
                              threshold=x.text(x.gL+x.rent*after_two_good))))


def hidden_outcomes(e):
    orders = (0, 0, 0, 0)
    likelihood, masses, posterior = e.update(e.prior, orders)
    branches = {}
    for y,d in product(range(2),range(2)):
        branches[y,d] = dict(orders=orders, rates=(e.rho,e.rho),
                             likelihood=e.probabilities(orders))
    eq = dict(orders=orders, rates=(e.rho,e.rho), likelihood=likelihood, branches=branches)
    return e.outcomes(eq)


def access_comparison():
    for strength,cost in product(("6/5", "3", "18/5"), ("5", "29/5")):
        e = Economy(strength,cost)
        observed, diagnostics = e.solve()
        hidden = hidden_outcomes(e)
        for result in observed:
            visible = result["outcomes"]
            delta = {key: visible[key]-hidden[key] for key in ("E1","E2","proceeds","net_surplus")}
            print(json.dumps(dict(kind="price_access",r=strength,cost=cost,
                hidden={k:e.text(hidden[k]) for k in ("E1","E2","proceeds","net_surplus")},
                difference={k:e.text(v) for k,v in delta.items()})))


if __name__ == "__main__":
    exact_auctions()
    bounds_at_weak_incumbent()
    interval_window()
    access_comparison()
