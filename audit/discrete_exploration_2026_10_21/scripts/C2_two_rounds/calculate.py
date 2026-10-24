"""Print finite histories, action values, and entry outcomes for two rounds."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import exp, factorial


def record(value):
    if isinstance(value, F):
        return {"exact": str(value), "decimal": float(value)}
    if isinstance(value, dict):
        return {str(key): record(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [record(item) for item in value]
    return value


def auction(r):
    p, ell, h, rho = F(1, 2), F(1), F(10), F(1, 4)
    t0 = p * (1 - p / r)
    th = r / 2 + p * p / (2 * r)
    tl = ell - (ell * ell - p * p) / (2 * r)
    gh = h - th
    gl = ell - tl
    return dict(r=r, t0=t0, th=th, tl=tl, gh=gh, gl=gl,
                wh=th-t0, wl=tl-t0, delta=th-tl, rho=rho)


def entry(v, mu, cost):
    return F(1) if v["gl"] + mu * (v["gh"] - v["gl"]) >= cost else v["rho"]


def price(v, mu, cost):
    return v["t0"] + entry(v, mu, cost) * (v["wl"] + mu * v["delta"])


def finite_case(name, noise, r, k, cost, beta, continuation, a=None, life="long"):
    """Enumerate real action payoffs against one fixed candidate schedule."""
    v = auction(r)
    states = ("H", "L")
    signals = (-1, 0, 1, 2) if noise == "three" else (-1, 1)
    prior = F(1, 2)

    def mass(x, q):
        if noise == "three":
            return F(1, 3) if x - q in (-1, 0, 1) else F(0)
        positive = (1 if q else a) / (1 + a)
        return positive if x == 1 else 1-positive

    def policy(j, n, x):
        if j == "L" or continuation == "none":
            return 0
        if noise == "three" and x in (-1, 2):
            return 0
        if continuation == "inventory":
            return n
        if continuation == "good":
            return int(x == 1)
        return 1

    def stock_value(j, e):
        return v["t0"] + e * v["wh" if j == "H" else "wl"]

    joint = {}
    mu1, terminal, p1, raw2 = {}, {}, {}, {}
    for x in signals:
        for j in states:
            b = beta if j == "H" else F(0)
            for n in (0, 1):
                joint[j, n, x] = prior * (b if n else 1-b) * mass(x, n)
        total = sum(joint[j, n, x] for j in states for n in (0, 1))
        high = sum(joint["H", n, x] for n in (0, 1))
        mu1[x] = high / total if total else F(1)
        for y in signals:
            weights = {
                j: sum(joint[j, n, x] * mass(y, policy(j, n, x)) for n in (0, 1))
                for j in states
            }
            den = sum(weights.values())
            mu = weights["H"] / den if den else (F(1) if y == 2 else mu1[x])
            e = entry(v, mu, cost)
            terminal[x, y] = dict(mu=mu, entry=e, price=price(v, mu, cost), mass=den)
            raw2[x, y] = weights
        if total:
            p1[x] = sum(
                joint[j, n, x] * sum(
                    mass(y, policy(j, n, x)) * stock_value(j, terminal[x, y]["entry"])
                    for y in signals
                ) for j in states for n in (0, 1)
            ) / total
        else:
            p1[x] = price(v, mu1[x], cost)

    values2, choices2, margins2 = {}, {}, []
    for j in states:
        for n in (0, 1):
            for x in signals:
                actions = []
                for q in (0, 1):
                    actions.append(sum(
                        mass(y, q) * ((n+q)*stock_value(j, terminal[x, y]["entry"])
                                      - q*(terminal[x, y]["price"]+k))
                        for y in signals
                    ))
                values2[j, n, x] = actions
                choices2[j, n, x] = int(actions[1] > actions[0])
                if joint[j, n, x] > 0:
                    chosen = policy(j, n, x)
                    if life == "long":
                        margin = actions[chosen] - actions[1-chosen]
                    else:
                        profit = sum(mass(y, 1) * (stock_value(j, terminal[x, y]["entry"])
                                                   - terminal[x, y]["price"]-k)
                                     for y in signals)
                        margin = profit if chosen else -profit
                    margins2.append(dict(state=j, prior_purchase=n,
                                         current_inventory=n if life == "long" else 0,
                                         first=x, order=chosen, margin=margin))

    values1 = {}
    for j in states:
        actions = []
        for n in (0, 1):
            if life == "long":
                value = sum(mass(x, n) * (max(values2[j, n, x])-n*(p1[x]+k)) for x in signals)
            else:
                value = n * sum(mass(x, n) * (
                    sum(mass(y, policy(j, n, x)) * stock_value(j, terminal[x, y]["entry"])
                        for y in signals) - p1[x] - k) for x in signals)
            actions.append(value)
        values1[j] = dict(zero=actions[0], buy=actions[1], buy_minus_zero=actions[1]-actions[0])

    total_entry = sum(row["mass"] * row["entry"] for row in terminal.values())
    ownership = sum(raw2[x, y]["H"] * terminal[x, y]["entry"] for x in signals for y in signals)
    high_units = sum(joint["H", n, x] * (n+policy("H", n, x)) / prior
                     for n in (0, 1) for x in signals)
    high_profit = sum(
        joint["H", n, x] / prior * (
            values2["H", n, x][policy("H", n, x)] - n*(p1[x]+k)
        ) for n in (0, 1) for x in signals
    )
    reported_choices = choices2 if life == "long" else {
        (j, x): choices2[j, 0, x] for j in states for x in signals
    }
    return dict(name=name, life=life, noise=noise, r=r, k=k, c_H=cost, beta=beta, a=a,
                auction=v, posterior1=mu1, price1=p1, terminal=terminal,
                first_action_values=values1, terminal_choice_margins=margins2,
                private_best_orders=reported_choices, entry=total_entry, high_ownership=ownership,
                high_expected_units=high_units, high_total_cost=k*high_units,
                high_total_net_profit=high_profit)


def discrete_laplace_formulas(a, r, k, cost):
    v = auction(r)
    u, d = 1/(1+a), a/(1+a)
    mu2 = 1/(1+a*a)
    D = v["rho"] * v["delta"]
    ehigh, emid, elow = (entry(v, m, cost) for m in (mu2, F(1,2), 1-mu2))
    cminus = v["delta"] * (u*emid/2+d*elow*mu2)
    cplus = v["delta"] * (u*ehigh*(1-mu2)+d*emid/2)
    dplus = v["wh"]*(u*ehigh+d*emid)-v["wl"]*(d*ehigh+u*emid)
    dminus = v["wh"]*(u*emid+d*elow)-v["wl"]*(d*emid+u*elow)
    cfirst = u*d*(dplus+dminus)
    ceiling = (v["wh"]-v["rho"]*v["wl"]-k)
    ceiling /= ceiling+k*a*a
    return dict(kind="full_schedule_payoffs", a=a, r=r, k=k,
                schedule="full purchases in both rounds; feasibility is separate",
                first_good=u, posterior_two_good=mu2,
                B_one_good=v["gl"]+u*(v["gh"]-v["gl"]),
                B_two_good=v["gl"]+mu2*(v["gh"]-v["gl"]),
                no_trade_cost_floor=D/2, second_bad_gross=cminus,
                second_good_gross=cplus, first_gross=cfirst,
                full_gross_lower_bound=D*(1-mu2),
                endogenous_posterior_bound=ceiling,
                upper_posterior_supports_entry=entry(v, mu2, cost)==1)


def benchmark_bounds():
    alo = sum(F(-1,2)**n / factorial(n) for n in range(10))
    ahi = sum(F(-1,2)**n / factorial(n) for n in range(11))
    lo, hi = F(606530, 1000000), F(606531, 1000000)
    mlo, mhi = 1/(1+hi*hi), 1/(1+lo*lo)
    weak, strong, final = (auction(r) for r in (F(6,5), F(3), F(18,5)))
    return dict(exp_lower=alo, exp_upper=ahi,
                coarse_lower_gap=alo-lo, coarse_upper_gap=hi-ahi,
                weak_no_trade_margin=F(1,50)-weak["delta"],
                weak_prior_entry_gap=F(6)-(weak["gl"]+(weak["gh"]-weak["gl"])/2),
                strong_full_trade_margin=strong["rho"]*strong["delta"]*(1-mhi)-F(1,50),
                final_full_trade_margin=final["rho"]*final["delta"]*(1-mhi)-F(1,50),
                strong_extra_entry_margin=strong["gl"]+mlo*(strong["gh"]-strong["gl"])-F(6),
                final_entry_ceiling_gap=F(6)-final["gl"]-mhi*(final["gh"]-final["gl"]))


def interval_margins(r=F(3), k=F(9,100)):
    lo, hi = F(3, 5), F(61, 100)
    umin, vmax, vmin = 1/(1+hi), hi/(1+hi), lo/(1+lo)
    v = auction(r)
    cost = F(6)
    D = v["rho"] * v["delta"]
    cminus = D*(umin/2+vmin/(1+hi*hi))
    cplus = v["delta"]*(umin*lo*lo/(1+lo*lo)+vmin*v["rho"]/2)
    cfirst = umin*vmin*(2*D+(1-v["rho"])*(v["wh"]*umin-v["wl"]*vmax))
    low_second_upper = v["wl"]*(1-v["rho"])*(1-lo)/(1+lo)-v["delta"]*umin/(1+hi*hi)-k
    result = dict(r=r, k=k, a_interval=(lo, hi), no_trade_margin=k-D/2,
                second_bad_margin_lower=cminus-k, second_good_margin_lower=cplus-k,
                first_margin_lower=cfirst-k,
                good_minus_bad_gross_lower=cplus-D*(1/(1+lo)/2+vmax/(1+lo*lo)),
                one_good_below_cost=cost-(v["gl"]+(1/(1+lo))*(v["gh"]-v["gl"])),
                two_good_above_cost=(v["gl"]+(1/(1+hi*hi))*(v["gh"]-v["gl"]))-cost,
                retained_low_second_purchase_upper=low_second_upper)
    if r == F(3):
        result.update(good_only_no_order_margin=F(11,100)-D/(1+lo),
                      good_only_good_order_margin=cplus-F(11,100),
                      good_only_first_order_margin=cfirst-F(11,100))
    return result


def equal_horizons():
    v = auction(F(3))
    k, pi, s = F(1, 50), F(1, 2), F(2, 3)
    rows = []
    for T in (1, 2, 3, 5, 10, 25):
        units = 3*(1-s**T)
        profits = sum(s**(t-1)*(s*(1-pi)*(v["rho"]*v["delta"]+
                      (1-v["rho"])*v["wh"]*(1-s**(T-t)))-k) for t in range(1, T+1))
        rows.append(dict(T=T, entry=v["rho"]+(1-v["rho"])*pi*(1-s**T),
                         high_ownership=pi*v["rho"]+(1-v["rho"])*pi*(1-s**T),
                         high_expected_units=units, high_total_cost=k*units,
                         high_total_net_profit=profits))
    return rows


def run(group):
    rows = []
    if group in ("all", "three"):
        for k, beta, policy in ((F(1,50), F(1), "full"),
                                (F(1,10), F(1), "full"),
                                (F(3,20), F(26,81), "inventory"),
                                (F(3,20), F(0), "none"),
                                (F(17,100), F(0), "none")):
            rows.append(finite_case("three_retained", "three", F(3), k, F(6), beta, policy))
        rows.append(finite_case("three_short", "three", F(3), F(1,50), F(6), F(1), "full", life="short"))
        rows.append({"equal_horizons": equal_horizons()})
    if group in ("all", "laplace"):
        for a in (F(3,5), exp(-0.5)):
            for life in ("short", "long"):
                for k, policy in ((F(9,100), "full"), (F(9,100), "none"), (F(11,100), "good")):
                    beta = F(0) if policy == "none" else F(1)
                    rows.append(finite_case("laplace_coexistence", "laplace", F(3), k,
                                            F(6), beta, policy, a=a, life=life))
                for beta, policy in ((F(0), "none"), (F(1), "full")):
                    rows.append(finite_case("laplace_original_cost_coexistence", "laplace", F(17,10),
                                            F(1,50), F(6), beta, policy, a=a, life=life))
            for r in (F(6,5), F(3), F(18,5), F(21,5)):
                rows.append(discrete_laplace_formulas(a, r, F(1,50), F(6)))
                policy = "none" if r == F(6,5) else "full"
                beta = F(0) if policy == "none" else F(1)
                rows.append(finite_case("laplace_benchmark", "laplace", r, F(1,50),
                                        F(6), beta, policy, a=a, life="short"))
        rows.append({"rational_interval_margins": interval_margins()})
        rows.append({"original_cost_interval_margins": interval_margins(F(17,10), F(1,50))})
        rows.append({"benchmark_rational_bounds": benchmark_bounds()})
    for row in rows:
        print(json.dumps(record(row), sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("all", "three", "laplace"), default="all")
    args = parser.parse_args()
    run(args.case)
