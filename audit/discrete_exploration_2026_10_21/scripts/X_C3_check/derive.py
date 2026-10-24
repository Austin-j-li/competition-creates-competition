"""Independent finite-history calculations for the preparation delay option."""

from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone
from math import factorial
import mpmath as mp

mp.mp.dps = 70


@dataclass(frozen=True)
class Parameters:
    h: object
    ell: object
    p: object
    rho: object
    cost: object
    delta: object
    k: object
    r: object


def auction(p: Parameters) -> tuple:
    t0 = p.p * (1 - p.p / p.r)
    th = p.r / 2 + p.p**2 / (2 * p.r)
    tl = p.ell - (p.ell**2 - p.p**2) / (2 * p.r)
    gh = p.h - th
    gl = (p.ell**2 - p.p**2) / (2 * p.r)
    return t0, th, tl, gh, gl


def gain(p: Parameters, mu: object) -> object:
    _, _, _, gh, gl = auction(p)
    return mu * gh + (1 - mu) * gl


def show(name: str, value: object) -> None:
    if isinstance(value, F):
        numerical = mp.mpf(value.numerator) / value.denominator
        print(name, str(value), mp.nstr(numerical, 45))
    elif isinstance(value, tuple):
        print(name, tuple(mp.nstr(x, 35) for x in value))
    else:
        print(name, mp.nstr(value, 45))


def stopping(p: Parameters, mu: object, cells: tuple) -> tuple:
    """Cells contain conditional probabilities under each quality class."""
    now = gain(p, mu) - p.cost
    wait = mu * 0
    for _, ph, pl in cells:
        mass = mu * ph + (1 - mu) * pl
        if mass:
            post = mu * ph / mass
            wait += mass * max(p.delta * gain(p, post) - p.cost, 0)
    action = "now" if now >= max(wait, 0) else "wait" if wait > max(now, 0) else "exit"
    return now, wait, action


def full_history(p: Parameters, cells: tuple, title: str) -> None:
    """Enumerate the joint quality and signal probabilities without tail truncation."""
    t0, th, tl, gh, gl = auction(p)
    spread = th - tl
    half = p.r * 0 + F(1, 2)
    entry = half * 0
    ownership = half * 0
    k1 = half * 0
    k1_low = half * 0
    prices = []
    late = half * 0
    print("\nFULL HISTORY", title)
    for label, ph1, pl1 in cells:
        mass1 = half * (ph1 + pl1)
        if not mass1:
            continue
        u = ph1 / (ph1 + pl1)
        # At a certain class, the on-path investor submits no order.
        continuation = cells if 0 < u < 1 else (("certain", u * 0 + 1, u * 0 + 1),)
        now, wait, action = stopping(p, u, continuation)
        ah = u * 0
        al = u * 0
        k2 = u * 0
        p2_rows = []
        for label2, ph2, pl2 in continuation:
            mass2 = u * ph2 + (1 - u) * pl2
            if not mass2:
                continue
            v = u * ph2 / mass2
            costly = action == "now" or (action == "wait" and p.delta * gain(p, v) >= p.cost)
            e = p.rho + (1 - p.rho) * costly
            actual_h = t0 + e * (th - t0)
            actual_l = t0 + e * (tl - t0)
            price2 = v * actual_h + (1 - v) * actual_l
            ah += ph2 * e
            al += pl2 * e
            k2 += ph2 * (actual_h - price2)
            entry += mass1 * mass2 * e
            ownership += half * ph1 * ph2 * e
            if action == "wait":
                late += mass1 * mass2 * (1 - p.rho) * costly
            p2_rows.append((label2, v, price2))
        value_h = t0 + ah * (th - t0)
        value_l = t0 + al * (tl - t0)
        price1 = u * value_h + (1 - u) * value_l
        residual_h = value_h - price1
        residual_l = value_l - price1
        # A unit purchase reaches each first cell with the full-purchase H law.
        k1 += ph1 * residual_h
        k1_low += ph1 * residual_l
        prices.append(price1)
        print("first", label, "action", action)
        for name, val in (("prior", u), ("now", now), ("wait", wait),
                          ("a_H", ah), ("a_L", al), ("P1", price1),
                          ("R1_H", residual_h)):
            show(name, val)
        if 0 < u < 1:
            show("K2_H", k2)
        elif u == 1:
            show("K2_H", u * 0)
        else:
            print("K2_H", "Class H has zero conditional probability here; omit its off-path continuation.")
        for label2, post, price2 in p2_rows:
            print("second", label2)
            show("posterior", post)
            show("P2", price2)
    show("E", entry)
    show("O_H", ownership)
    show("K1_H", k1)
    show("K1_L_purchase", k1_low)
    show("late_preparation", late)
    show("late_share_of_preparations", late / entry)
    show("proceeds", t0 + (tl - t0) * entry + spread * ownership)


def three_cells(beta: F) -> tuple:
    return (("bottom", (1 - beta) / 3, F(1, 3)),
            ("middle", F(2, 3), F(2, 3)),
            ("top", beta / 3, F(0)))


def exact_cutoffs(p: Parameters, beta: F) -> None:
    _, _, _, gh, gl = auction(p)
    spread = gh - gl
    threshold = (p.cost / p.delta - gl) / spread
    low_activation = threshold / (1 - beta + beta * threshold)
    knots = sorted(set([F(0), F(1)] + [v for v in (threshold, low_activation) if 0 < v < 1]))
    cells = three_cells(beta)
    print("\nEXACT CUTOFF", "delta", p.delta, "beta", beta, "cost", p.cost)
    show("tau_late", threshold)
    for left, right in zip(knots[:-1], knots[1:]):
        nl, wl, _ = stopping(p, left, cells)
        nr, wr, _ = stopping(p, right, cells)
        dl, dr = wl - nl, wr - nr
        if dl == 0:
            show("root", left)
        if dl * dr < 0:
            root = left - dl * (right - left) / (dr - dl)
            show("root", root)
    for u in (F(1, 10), F(1, 2), F(4, 5), F(9, 10)):
        now, wait, action = stopping(p, u, cells)
        print("belief", u, "action", action, "N", now, "W", wait)


def ceiling(p: Parameters, mu: object, cost: object) -> object:
    linear = mu * p.h - cost
    return (linear + mp.sqrt(linear**2 + mu * ((1 - mu) * p.ell**2 - p.p**2))) / mu


def dlaplace_cells(a: object, beta: object) -> tuple:
    high_good = (a + beta * (1 - a)) / (1 + a)
    low_good = a / (1 + a)
    return (("G", high_good, low_good), ("B", 1 - high_good, 1 - low_good))


def floor_average(u: object, beta: object, a: object) -> object:
    cells = dlaplace_cells(a, beta)
    buy = dlaplace_cells(a, mp.mpf(1))
    result = u * 0
    for (_, ph, pl), (_, bought, _) in zip(cells, buy):
        posterior = u * ph / (u * ph + (1 - u) * pl)
        result += bought * (1 - posterior)
    return result


def main() -> None:
    print("UTC", datetime.now(timezone.utc).isoformat())
    print("precision_decimal_digits", mp.mp.dps)
    print("paper_commit", "9b9bf3ce1a94d5017042192e61c9ceb800d310ba")
    print("method", "Exact fractions and finite signal partitions; no tail cutoff or search grid.")
    for item in (Path(__file__), Path("audit/discrete_exploration_2026_10_21/memos/C3_delay.md")):
        print("SHA256", item.name, sha256(item.read_bytes()).hexdigest())

    three = Parameters(F(10), F(1), F(1, 2), F(1, 4), F(6), F(19, 20), F(1, 50), F(3))
    full_history(three, three_cells(F(1)), "three-point r=3")
    _, th, tl, gh, gl = auction(three)
    show("three_round2_bottleneck", three.rho * (th - tl) / 3)
    show("three_discount_threshold", three.cost / gh)
    for delta in (F(9, 10), F(19, 20)):
        for beta in (F(1), F(2, 5)):
            p = Parameters(three.h, three.ell, three.p, three.rho, three.cost, delta, three.k, three.r)
            exact_cutoffs(p, beta)
    edge = Parameters(three.h, three.ell, three.p, three.rho, gl, F(19, 20), three.k, three.r)
    exact_cutoffs(edge, F(1))
    tied = Parameters(three.h, three.ell, three.p, three.rho, three.cost, three.cost / gh, three.k, three.r)
    full_history(tied, three_cells(F(1)), "three-point exact late tie")
    show("three_public_wait_round2_profit", F(0))
    show("three_no_delay_entry", F(3, 8))
    print("\nTHREE-POINT STRENGTH PATH")
    for r in (F(6, 5), F(3), F(18, 5), F(15, 2), F(17, 2)):
        pp = Parameters(three.h, three.ell, three.p, three.rho, three.cost, three.delta, three.k, r)
        _, t_h, t_l, g_h, _ = auction(pp)
        trade = pp.k < pp.rho * (t_h - t_l) / 3
        middle_wait = trade and pp.delta * g_h > pp.cost
        e = pp.rho + (1 - pp.rho) * ((F(1, 6) if trade and g_h >= pp.cost else F(0))
                                    + (F(1, 9) if middle_wait else F(0)))
        print("r", r, "trade", trade, "middle_wait", middle_wait, "E", e)
    spread_target = mp.mpf(6) / 25
    show("three_trade_strength", 1 + spread_target + mp.sqrt(spread_target**2 + 2 * spread_target))
    for discount in (mp.mpf(19) / 20, mp.mpf(1)):
        level = 10 - 6 / discount
        show("three_ceiling_delta_" + str(discount), level + mp.sqrt(level**2 - mp.mpf(1) / 4))

    x = mp.mpf
    p = Parameters(x(10), x(1), x("0.5"), x("0.25"), x(5), x("0.95"), x("0.02"), x(3))
    a = mp.exp(-x(1) / 2)
    upper = 1 / (1 + a)
    lower = 1 - upper
    upper2 = 1 / (1 + a**2)
    lower2 = 1 - upper2
    q = upper**2 + lower**2
    for name, value in (("a", a), ("M1", upper), ("m1", lower), ("M2", upper2), ("m2", lower2),
                        ("Pr_GG", q / 2), ("delta_star_3", (p.cost + (gain(p, upper) - p.cost) / q) / gain(p, upper2)),
                        ("delta_zero_3", p.cost / gain(p, upper2)),
                        ("ceiling_one", ceiling(p, upper, p.cost)),
                        ("ceiling_two", ceiling(p, upper2, p.cost / p.delta))):
        show(name, value)
    full_history(p, dlaplace_cells(a, x(1)), "discrete-Laplace r=3 c=5")
    coexist = Parameters(p.h, p.ell, p.p, p.rho, x("5.5"), p.delta, x("0.09"), p.r)
    full_history(coexist, dlaplace_cells(a, x(1)), "discrete-Laplace coexistence candidate")
    t0, th, tl, gh, gl = auction(p)
    spread = th - tl
    show("one_round_E", p.rho + (1 - p.rho) / 2)
    show("one_round_O_H", p.rho / 2 + (1 - p.rho) * upper / 2)
    show("one_round_K", spread * lower * upper * (1 + p.rho))
    show("no_trade_K", p.rho * spread / 2)
    show("universal_K1_bound", p.rho * spread * lower)
    show("universal_K2_bound", p.rho * spread * lower2)
    for u in (lower, x("0.5"), upper):
        minimizing_beta = min(x(1), 1 / (2 * u))
        print("exact_minimum", "prior", mp.nstr(u, 20), "beta", mp.nstr(minimizing_beta, 20))
        show("K2_floor_minimum", p.rho * spread * floor_average(u, minimizing_beta, a))
    show("public_wait_K2_G", spread * upper * lower2)
    show("public_exit_K2_B", x(0))
    derivative_one = -upper / 2 - ((1 - upper) * p.ell**2 - p.p**2) / (2 * p.r**2)
    derivative_two = -upper2 / 2 - ((1 - upper2) * p.ell**2 - p.p**2) / (2 * p.r**2)
    show("gain_derivative_M1", derivative_one)
    show("gain_derivative_M2", derivative_two)
    show("wait_minus_now_derivative_delta_09", x("0.9") * q * derivative_two - derivative_one)

    print("\nSTRENGTH AND TIMING")
    for r in ("1.2", "2", "2.5", "3", "3.6", "4.2", "5", "6"):
        for delta in ("0.9", "0.95"):
            pp = Parameters(p.h, p.ell, p.p, p.rho, p.cost, x(delta), p.k, x(r))
            now, wait, action = stopping(pp, upper, dlaplace_cells(a, x(1)))
            print("r", r, "delta", delta, "full-purchase_branch_G", action,
                  "N", mp.nstr(now, 24), "W", mp.nstr(wait, 24))
    print("The full-purchase branch at r=1.2 is counterfactual; both rounds choose no order there.")
    for delta in ("0.9", "0.95"):
        dd = x(delta)
        switch = mp.findroot(lambda r: dd * (upper**2 * (p.h - r / 2 - p.p**2 / (2 * r))
                                    + lower**2 * (p.ell**2 - p.p**2) / (2 * r))
                                    - (upper * (p.h - r / 2 - p.p**2 / (2 * r))
                                    + lower * (p.ell**2 - p.p**2) / (2 * r))
                                    + 2 * lower * upper * p.cost, (x(2), x(3)))
        show("now_wait_switch_delta_" + delta, switch)
    print("\nRATIONAL BOUNDS")
    terms = [F((-1)**n, 2**n * factorial(n)) for n in range(6)]
    show("exp_minus_half_lower", sum(terms))
    show("exp_minus_half_upper", sum(terms[:-1]))
    m_min = F(3, 8)
    big_min = F(100, 161)
    two_min = F(10000, 13721)
    tiny_min = F(9, 34)
    show("W5_lower", F(1, 2) * (F(19, 20) * (F(1, 8) + F(25, 3) * two_min) - 5))
    show("N5_upper", F(1, 3))
    show("late_surplus_5_5_lower", F(19, 20) * (F(1, 8) + F(25, 3) * two_min) - F(11, 2))
    show("K2_wait_lower", F(2, 3) * (big_min * tiny_min + m_min / 8))
    show("K2_exit_lower", F(1, 6) * (big_min / 2 + m_min * two_min))
    show("K1_coexist_lower", F(15, 64) * (F(1, 3) + big_min / 2))
    show("late_r6_upper", F(19, 20) * (F(1, 16) + F(83, 12) * F(25, 34)))
    show("entry_r6_early_upper", F(1, 16) + F(83, 12) * F(5, 8))


if __name__ == "__main__":
    main()
