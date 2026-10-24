"""Two exact flow classes and the full buy-only equilibrium correspondence."""

from dataclasses import dataclass, replace
from typing import NamedTuple
import argparse
import csv
import hashlib
import json
from pathlib import Path
from mpmath import mp

mp.dps = 60
ROOT = Path(__file__).resolve().parent
TOL = mp.mpf("1e-48")


@dataclass(frozen=True)
class Parameters:
    h: str = "10"
    ell: str = "1"
    p: str = "0.5"
    rho: str = "0.25"
    b: str = "2"
    k: str = "0.02"
    c_H: str = "5"
    pi: str = "0.5"
    lam: str = "1"
    a_plus: str = ""
    a_minus: str = ""


class Auction(NamedTuple):
    t_0: object
    t_H: object
    t_L: object
    g_H: object
    g_L: object
    Delta_T: object


class Noise(NamedTuple):
    a_plus: object
    a_minus: object
    zero_bad: object
    zero_good: object
    buy_bad: object
    buy_good: object
    mass_zero: object


def number(value):
    return mp.mpf(value)


def auction(par, r):
    r = number(r)
    h, ell, p = map(number, (par.h, par.ell, par.p))
    t_0 = p * (1 - p / r)
    t_H = r / 2 + p * p / (2 * r)
    t_L = ell - (ell * ell - p * p) / (2 * r)
    return Auction(t_0, t_H, t_L, h - t_H,
                   (ell * ell - p * p) / (2 * r), (r - ell) ** 2 / (2 * r))


def noise(par):
    a = mp.exp(-1 / number(par.b))
    u = number(par.a_plus) if par.a_plus else a
    v = number(par.a_minus) if par.a_minus else a
    normal = (1 - u) * (1 - v) / (1 - u * v)
    zero_bad = (1 - u) / (1 - u * v)
    buy_good = (1 - v) / (1 - u * v)
    return Noise(u, v, zero_bad, u * buy_good, v * zero_bad, buy_good, normal)


def posteriors(par, d):
    pi = number(par.pi)
    n = noise(par)
    bad_factor = 1 - d * (1 - n.a_minus)
    good_factor = 1 + d * (1 / n.a_plus - 1)
    return (pi * bad_factor / (1 - pi + pi * bad_factor),
            pi * good_factor / (1 - pi + pi * good_factor))


def gain(par, r, mu):
    obj = auction(par, r)
    return obj.g_L + mu * (obj.g_H - obj.g_L)


def entry(par, r, mu):
    gap = gain(par, r, mu) - number(par.c_H)
    return mp.one if gap >= -TOL else number(par.rho)


def gross(par, r, d, e_bad, e_good):
    n = noise(par)
    m, M = posteriors(par, d)
    return auction(par, r).Delta_T * (
        n.buy_bad * e_bad * (1 - m) + n.buy_good * e_good * (1 - M))


def outcome(par, r, d, e_bad, e_good, branch, extent="point"):
    n = noise(par)
    obj = auction(par, r)
    pi, lam, k, rho = map(number, (par.pi, par.lam, par.k, par.rho))
    m, M = posteriors(par, d)
    high_good = n.zero_good + n.mass_zero * d
    e_H = (1 - high_good) * e_bad + high_good * e_good
    e_L = n.zero_bad * e_bad + n.zero_good * e_good
    total_entry = pi * e_H + (1 - pi) * e_L
    price_bad = obj.t_0 + e_bad * (obj.t_L - obj.t_0 + obj.Delta_T * m)
    price_good = obj.t_0 + e_good * (obj.t_L - obj.t_0 + obj.Delta_T * M)
    u_L = -obj.Delta_T * (n.buy_bad * e_bad * m + n.buy_good * e_good * M) - k
    revenue = obj.t_0 + pi * e_H * (obj.t_H - obj.t_0) + (1 - pi) * e_L * (obj.t_L - obj.t_0)
    reserve_gain = number(par.p) ** 2 / number(r)
    baseline = (number(r) ** 2 - number(par.p) ** 2) / (2 * number(r))
    welfare = (baseline + pi * e_H * (obj.g_H + reserve_gain)
               + (1 - pi) * e_L * (obj.g_L + reserve_gain)
               - number(par.c_H) * (total_entry - rho) - pi * d * k)
    return dict(r=number(r), branch=branch, extent=extent, beta_H=d / lam,
                beta_L=mp.zero, d=d, m=m, M=M, e_bad=e_bad, e_good=e_good,
                e_H=e_H, e_L=e_L, E=total_entry, O_H=pi * e_H, R_T=revenue,
                W=welfare, U_H=gross(par, r, d, e_bad, e_good) - k,
                U_L=u_L, P_bad=price_bad, P_good=price_good)


def quadratic_roots(c0, c1, c2):
    if abs(c2) < TOL:
        return [] if abs(c1) < TOL else [-c0 / c1]
    discriminant = c1 * c1 - 4 * c2 * c0
    if discriminant < -TOL:
        return []
    rad = mp.sqrt(max(mp.zero, discriminant))
    return [(-c1 - rad) / (2 * c2), (-c1 + rad) / (2 * c2)]


def constant_entry_roots(par, r, e_bad, e_good):
    n = noise(par)
    pi, k = map(number, (par.pi, par.k))
    spread = auction(par, r).Delta_T
    A = pi * (1 - n.a_minus)
    D = pi * (1 / n.a_plus - 1)
    cb = n.buy_bad * (1 - pi) * e_bad
    cg = n.buy_good * (1 - pi) * e_good
    return quadratic_roots(k - spread * (cb + cg),
                           k * (D - A) - spread * (cb * D - cg * A), -k * A * D)


def entry_break(par, r):
    obj = auction(par, r)
    pi, lam = map(number, (par.pi, par.lam))
    tau = (number(par.c_H) - obj.g_L) / (obj.g_H - obj.g_L)
    n = noise(par)
    if tau <= 0 or tau >= 1 or abs(tau - pi) < TOL:
        return None
    if tau > pi:
        d = (tau - pi) / (pi * (1 / n.a_plus - 1) * (1 - tau))
        side = "good"
    else:
        d = (pi - tau) / (pi * (1 - n.a_minus) * (1 - tau))
        side = "bad"
    return (d, side) if -TOL <= d <= lam + TOL else None


def equilibria(par, r, challenger_mix=True):
    rho, lam, pi, k = map(number, (par.rho, par.lam, par.pi, par.k))
    rows = []
    prior_gap = gain(par, r, pi) - number(par.c_H)
    prior_tie = abs(prior_gap) < TOL
    if prior_tie and challenger_mix:
        n = noise(par)
        scale = auction(par, r).Delta_T * (1 - pi)
        vertices = [(eb, eg) for eb in (rho, mp.one) for eg in (rho, mp.one)
                    if scale * (n.buy_bad * eb + n.buy_good * eg) <= k + TOL]
        for eb in (rho, mp.one):
            eg = (k / scale - n.buy_bad * eb) / n.buy_good
            if rho - TOL <= eg <= 1 + TOL:
                vertices.append((eb, min(mp.one, max(rho, eg))))
        for eg in (rho, mp.one):
            eb = (k / scale - n.buy_good * eg) / n.buy_bad
            if rho - TOL <= eb <= 1 + TOL:
                vertices.append((min(mp.one, max(rho, eb)), eg))
        rows += [outcome(par, r, mp.zero, eb, eg, "no_trade", "tie_polytope_vertex")
                 for eb, eg in vertices]
    else:
        e_prior = mp.one if prior_gap >= -TOL else rho
        if gross(par, r, mp.zero, e_prior, e_prior) <= k + TOL:
            rows.append(outcome(par, r, mp.zero, e_prior, e_prior, "no_trade"))
    crossing = entry_break(par, r)
    cuts = [mp.zero, lam]
    if crossing and TOL < crossing[0] < lam - TOL:
        cuts.append(crossing[0])
    cuts = sorted(cuts)
    for left, right in zip(cuts[:-1], cuts[1:]):
        middle = (left + right) / 2
        m, M = posteriors(par, middle)
        eb, eg = entry(par, r, m), entry(par, r, M)
        for d in constant_entry_roots(par, r, eb, eg):
            if left + TOL < d < right - TOL:
                label = "mixed_floor" if eb == rho and eg == rho else "mixed_entry"
                if eb == mp.one and eg == mp.one:
                    label = "mixed_all_entry"
                rows.append(outcome(par, r, d, eb, eg, label))
    m, M = posteriors(par, lam)
    eb, eg = entry(par, r, m), entry(par, r, M)
    full_at_tie = bool(crossing and abs(crossing[0] - lam) < TOL)
    if gross(par, r, lam, eb, eg) >= k - TOL:
        extent = "tie_interval_upper" if full_at_tie and challenger_mix else "point"
        rows.append(outcome(par, r, lam, eb, eg, "full_buy", extent))
    if crossing and challenger_mix:
        d, side = crossing
        d = min(lam, max(mp.zero, d))
        m, M = posteriors(par, d)
        eb, eg = entry(par, r, m), entry(par, r, M)
        low = gross(par, r, d, rho if side == "bad" else eb,
                    rho if side == "good" else eg)
        high = gross(par, r, d, mp.one if side == "bad" else eb,
                     mp.one if side == "good" else eg)
        needed = rho + (1 - rho) * (k - low) / (high - low)
        if TOL < d < lam - TOL and rho - TOL <= needed <= 1 + TOL:
            needed = min(mp.one, max(rho, needed))
            rows.append(outcome(par, r, d, needed if side == "bad" else eb,
                                needed if side == "good" else eg, "mixed_threshold"))
        if abs(d - lam) < TOL and high >= k - TOL:
            minimum = max(rho, needed)
            if minimum <= 1 + TOL:
                rows.append(outcome(par, r, lam, minimum if side == "bad" else eb,
                                    minimum if side == "good" else eg,
                                    "full_buy", "tie_interval_lower"))
    unique = []
    for row in sorted(rows, key=lambda z: (z.get("beta_H", mp.zero), z.get("e_good", mp.zero))):
        duplicate = any(abs(row["beta_H"] - old["beta_H"]) < TOL
                        and abs(row["e_bad"] - old["e_bad"]) < TOL
                        and abs(row["e_good"] - old["e_good"]) < TOL for old in unique)
        if not duplicate:
            unique.append(row)
    return unique


def scalar_root(fun, left, right):
    left, right = number(left), number(right)
    fleft, fright = fun(left), fun(right)
    if fleft * fright > 0:
        print("unresolved root bracket", mp.nstr(left, 12), mp.nstr(right, 12))
        return mp.nan
    for _ in range(205):
        middle = (left + right) / 2
        fmid = fun(middle)
        if fleft * fmid <= 0:
            right = middle
        else:
            left, fleft = middle, fmid
    return (left + right) / 2


def r_from_spread(par, spread):
    ell = number(par.ell)
    return ell + spread + mp.sqrt(spread ** 2 + 2 * ell * spread)


def exact_k_window(par):
    rho, pi, lam = map(number, (par.rho, par.pi, par.lam))
    _, M = posteriors(par, lam)
    cost = number(par.c_H)
    if not max(gain(par, "1.2", pi), gain(par, "4.2", M)) < cost < gain(par, "3", M):
        return None
    weak_crossing = entry_break(par, "1.2")
    lower = gross(par, "1.2", mp.zero, rho, rho)
    lower_open = False
    if weak_crossing:
        jump = gross(par, "1.2", weak_crossing[0], rho, mp.one)
        if jump >= lower:
            lower, lower_open = jump, True
    strong_crossing = entry_break(par, "3")
    upper = gross(par, "3", strong_crossing[0], rho, rho)
    upper_open = True
    for other in (gross(par, "3", lam, rho, mp.one), gross(par, "4.2", lam, rho, rho)):
        if other < upper:
            upper, upper_open = other, False
    return dict(k_lower=lower, lower_open=lower_open, k_upper=upper, upper_open=upper_open,
                nonempty=lower < upper)


def ceiling(par, mu):
    h, ell, p, c = map(number, (par.h, par.ell, par.p, par.c_H))
    top = mu * h - c
    rad = top * top + mu * ((1 - mu) * ell * ell - p * p)
    return (top + mp.sqrt(rad)) / mu if rad >= 0 else mp.nan


def serial(value):
    if isinstance(value, dict):
        return {key: serial(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(val) for val in value]
    if hasattr(value, "_mpf_"):
        return mp.nstr(value, 52)
    return value


def write_csv(name, rows):
    if not rows:
        return
    columns = list(dict.fromkeys(key for row in rows for key in row))
    with (ROOT / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(serial(row) for row in rows)
    print(name, len(rows), "rows")


def point(par, r):
    print(json.dumps(serial(dict(parameters=par.__dict__, r=number(r),
                                 auction=auction(par, r)._asdict(), noise=noise(par)._asdict(),
                                 equilibria=equilibria(par, r))), indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["point", "report"])
    parser.add_argument("--r", default="3")
    parser.add_argument("--pi", default="0.5")
    parser.add_argument("--lam", default="1")
    parser.add_argument("--b", default="2")
    parser.add_argument("--k", default="0.02")
    parser.add_argument("--c-H", default="5")
    parser.add_argument("--a-plus", default="")
    parser.add_argument("--a-minus", default="")
    args = parser.parse_args()
    par = Parameters(pi=args.pi, lam=args.lam, b=args.b, k=args.k, c_H=args.c_H,
                     a_plus=args.a_plus, a_minus=args.a_minus)
    if args.mode == "point":
        point(par, args.r)
        return
    if par != Parameters():
        print("The report uses the benchmark. Use point for other inputs.")
        return
    report(par)


def report(par):
    rho, k, pi, lam = map(number, (par.rho, par.k, par.pi, par.lam))
    n = noise(par)
    m, M = posteriors(par, lam)
    summary = dict(parameters=par.__dict__, decimal_precision=mp.dps,
                   pinned_commit="9b9bf3ce1a94d5017042192e61c9ceb800d310ba",
                   posteriors_full=[m, M], c_H_window=[gain(par, "1.2", pi), gain(par, "3", M)],
                   low_spread=auction(par, "1.2").Delta_T,
                   strong_uniform_lower=rho * (1 - M) * auction(par, "3").Delta_T,
                   feedback_gross=gross(par, "3", lam, rho, mp.one),
                   fixed_floor_gross=gross(par, "3", lam, rho, rho))
    summary["feedback_net"] = summary["feedback_gross"] - k
    summary["fixed_floor_net"] = summary["fixed_floor_gross"] - k
    summary["feedback_increment"] = summary["feedback_gross"] - summary["fixed_floor_gross"]
    r_N = r_from_spread(par, k / (rho * (1 - pi)))
    full_coefficient = gross(par, "3", lam, rho, mp.one) / auction(par, "3").Delta_T
    r_F = r_from_spread(par, k / full_coefficient)
    r_C = ceiling(par, M)
    def threshold_profit(r, e):
        crossing = entry_break(par, r)
        return gross(par, r, crossing[0], rho, e) - k if crossing else mp.nan
    r_S = scalar_root(lambda r: threshold_profit(r, mp.one), "1.25", "1.5")
    r_Q = scalar_root(lambda r: threshold_profit(r, rho), r_N, "1.85")
    summary["boundaries"] = dict(r_S=r_S, r_F=r_F, r_N=r_N, r_Q=r_Q, r_C=r_C)
    summary["boundary_residuals"] = dict(
        r_S=threshold_profit(r_S, mp.one), r_F=gross(par, r_F, lam, rho, mp.one) - k,
        r_N=gross(par, r_N, mp.zero, rho, rho) - k,
        r_Q=threshold_profit(r_Q, rho), r_C=gain(par, r_C, M) - number(par.c_H))
    summary["exact_k_window_at_fixed_noise_cost"] = exact_k_window(par)
    points = [number(x) for x in ("1.2", "1.4", "1.41", "1.42", "1.43", "1.45", "1.55", "1.6", "1.65", "1.74", "1.75", "1.76", "1.8", "3", "3.6", "4.2")]
    points += [r_S, r_F, r_N, r_Q, r_C]
    rows = [row for r in sorted(points) for row in equilibria(par, r)]
    write_csv("benchmark_points.csv", rows)
    grid = [number("1.05") + number("0.01") * i for i in range(396)]
    grid += [r_S, r_F, r_N, r_Q, r_C]
    path_rows = [row for r in sorted(set(grid)) for row in equilibria(par, r)]
    write_csv("equilibrium_branches.csv", path_rows)
    summary["branch_counts"] = {label: sum(row["branch"] == label for row in path_rows)
                                 for label in sorted(set(row["branch"] for row in path_rows))}
    summary["largest_mixed_profit_residual"] = max(
        [abs(row["U_H"]) for row in path_rows if row["branch"].startswith("mixed")] + [mp.zero])
    summary["smallest_low_type_loss"] = max(row["U_L"] for row in path_rows)
    write_csv("strength_entry_path.csv", [row for row in rows if row["r"] in map(number, ("1.2", "3", "3.6", "4.2"))])
    robustness(par, summary)
    general_priors(par, summary)
    (ROOT / "summary.json").write_text(json.dumps(serial(summary), indent=2) + "\n")
    print(json.dumps(serial(summary), indent=2))
    files = sorted(path for path in ROOT.iterdir() if path.is_file() and path.name != "receipt.json")
    receipt = dict(pinned_commit=summary["pinned_commit"], parameters=par.__dict__,
                   decimal_precision=mp.dps, method="exact two-class reduction; quadratic roots; cost-tie mixtures",
                   outputs={path.name: dict(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in files})
    (ROOT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


def robustness(par, summary):
    rows = []
    for b in ("0.5", "1", "1.5", "2", "2.5", "3", "4", "5"):
        for lam in ("0.1", "0.25", "0.5", "0.75", "1"):
            alt = replace(par, b=b, lam=lam)
            m, M = posteriors(alt, number(lam))
            lower_c = max(gain(alt, "1.2", number(alt.pi)), gain(alt, "4.2", M))
            upper_c = gain(alt, "3", M)
            lower_k = auction(alt, "1.2").Delta_T
            upper_k = number(alt.rho) * (1 - M) * auction(alt, "3").Delta_T
            rows.append(dict(b=b, lam=lam, k_lower=lower_k, k_upper=upper_k,
                             c_H_lower=lower_c, c_H_upper=upper_c,
                             k_window_nonempty=lower_k < upper_k,
                             c_H_window_nonempty=lower_c < upper_c,
                             fixed_k_inside=lower_k < number(alt.k) < upper_k,
                             fixed_c_H_inside=lower_c < number(alt.c_H) <= upper_c))
    write_csv("robustness_windows.csv", rows)
    asym_rows = []
    for u, v in (("0.4", "0.7"), ("0.7", "0.4"), ("0.55", "0.65"),
                 ("0.65", "0.55"), ("0.2", "0.8"), ("0.8", "0.2")):
        for lam in ("0.5", "0.75", "1"):
            alt = replace(par, a_plus=u, a_minus=v, lam=lam)
            _, M = posteriors(alt, number(lam))
            for r in ("1.2", "3", "3.6", "4.2"):
                for row in equilibria(alt, r):
                    asym_rows.append(dict(a_plus=u, a_minus=v, lam=lam,
                                          uniform_strong_bound=number(alt.rho) * (1 - M) * auction(alt, "3").Delta_T,
                                          **row))
    write_csv("asymmetric_examples.csv", asym_rows)
    obj1, obj2 = auction(par, "3"), auction(par, "4.2")
    cost, pi, rho = map(number, (par.c_H, par.pi, par.rho))
    tau1 = (cost - obj1.g_L) / (obj1.g_H - obj1.g_L)
    tau2 = (cost - obj2.g_L) / (obj2.g_H - obj2.g_L)
    required_factor = tau1 * (1 - pi) / (pi * (1 - tau1))
    u_max = pi * (1 - tau1) / ((1 - pi) * tau1)
    u_min = pi * (1 - tau2) / ((1 - pi) * tau2)
    summary["fixed_parameter_noise_region"] = dict(
        lambda_entry_min=(required_factor - 1) / (1 / noise(par).a_plus - 1),
        a_plus_return_min=u_min, a_plus_entry_max=u_max,
        b_return_min=-1 / mp.log(u_min), b_entry_max=-1 / mp.log(u_max),
        three_strength_cost_lower=max(gain(par, "1.2", pi), gain(par, "4.2", posteriors(par, number(par.lam))[1])))
    parameter_counts = dict(cases=0, sufficient_region=0, all_requested_outcomes=0,
                            sufficient_but_unresolved=0, outside_but_outcomes=0)
    for b in ("0.5", "1", "1.5", "2", "2.5", "3", "4", "5"):
        for lam in ("0.1", "0.25", "0.5", "0.75", "1"):
            for k in ("0.017", "0.02", "0.03", "0.04", "0.05"):
                for cost in ("4.81", "4.9", "5", "5.1", "5.2", "5.3", "5.5", "6"):
                    alt = replace(par, b=b, lam=lam, k=k, c_H=cost)
                    _, M = posteriors(alt, number(lam))
                    sufficient = (auction(alt, "1.2").Delta_T < number(k)
                                  < number(alt.rho) * (1 - M) * auction(alt, "3").Delta_T
                                  and max(gain(alt, "1.2", number(alt.pi)), gain(alt, "4.2", M))
                                  < number(cost) <= gain(alt, "3", M))
                    eqs = [equilibria(alt, r) for r in ("1.2", "3", "4.2")]
                    desired = (len(eqs[0]) == 1 and eqs[0][0]["branch"] == "no_trade"
                               and eqs[0][0].get("E") == number(alt.rho)
                               and len(eqs[1]) == 1 and eqs[1][0]["branch"] == "full_buy"
                               and eqs[1][0].get("E", mp.zero) > number(alt.rho)
                               and len(eqs[2]) == 1 and eqs[2][0]["branch"] == "full_buy"
                               and eqs[2][0].get("E") == number(alt.rho))
                    parameter_counts["cases"] += 1
                    parameter_counts["sufficient_region"] += int(sufficient)
                    parameter_counts["all_requested_outcomes"] += int(desired)
                    parameter_counts["sufficient_but_unresolved"] += int(sufficient and not desired)
                    parameter_counts["outside_but_outcomes"] += int(not sufficient and desired)
    summary["robustness_grid"] = parameter_counts
    exact_rows = []
    for b in ("0.5", "1", "1.5", "2", "2.5", "3", "4", "5"):
        for lam in ("0.1", "0.25", "0.5", "0.75", "1"):
            for cost in ("4.81", "4.9", "5", "5.1", "5.2", "5.3", "5.5", "6"):
                alt = replace(par, b=b, lam=lam, c_H=cost)
                window = exact_k_window(alt)
                if window:
                    exact_rows.append(dict(b=b, lam=lam, c_H=cost, **window))
    write_csv("exact_cost_windows.csv", exact_rows)


def general_priors(par, summary):
    rows, windows = [], []
    for prior in ("0.1", "0.25", "0.4", "0.46", "0.48", "0.5", "0.52", "0.55", "0.6", "0.75", "0.9"):
        alt = replace(par, pi=prior)
        m, M = posteriors(alt, number(alt.lam))
        windows.append(dict(pi=prior, m=m, M=M,
                            c_H_lower=gain(alt, "1.2", number(prior)),
                            c_H_upper=gain(alt, "3", M), r_C=ceiling(alt, M),
                            strong_uniform_lower=number(alt.rho) * (1 - M) * auction(alt, "3").Delta_T))
        for r in ("1.2", "3", "3.6", "4.2"):
            rows += [dict(pi=prior, **row) for row in equilibria(alt, r)]
    write_csv("general_priors.csv", rows)
    write_csv("prior_windows.csv", windows)
    obj0, obj1 = auction(par, "1.2"), auction(par, "3")
    tau0 = (number(par.c_H) - obj0.g_L) / (obj0.g_H - obj0.g_L)
    tau1 = (number(par.c_H) - obj1.g_L) / (obj1.g_H - obj1.g_L)
    factor = 1 + number(par.lam) * (1 / noise(par).a_plus - 1)
    summary["fixed_cost_prior_window"] = dict(lower=tau1 / (factor * (1 - tau1) + tau1), upper=tau0)
    obj2 = auction(par, "4.2")
    tau2 = (number(par.c_H) - obj2.g_L) / (obj2.g_H - obj2.g_L)
    summary["fixed_cost_prior_window"]["upper_for_return_at_4_2"] = tau2 / (factor * (1 - tau2) + tau2)
    diff = obj1.g_L - obj0.g_L
    a = noise(par).a_plus
    spread0 = obj0.g_H - obj0.g_L
    spread1 = obj1.g_H - obj1.g_L
    summary["prior_range_for_nonempty_cost_window"] = sorted(quadratic_roots(
        diff * a, diff * (1 - a) + spread1 - a * spread0, -spread0 * (1 - a)))


if __name__ == "__main__":
    main()
