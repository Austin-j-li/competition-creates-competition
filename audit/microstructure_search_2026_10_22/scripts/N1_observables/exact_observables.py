"""Print exact market observables for the one-slot benchmark.

Use from the repository root with --output-dir to save the same report.
This program uses rational arithmetic and prints economic quantities.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
from pathlib import Path
import platform


@dataclass(frozen=True)
class Parameters:
    h: F = F(10)
    ell: F = F(1)
    reserve: F = F(1, 2)
    rho: F = F(1, 4)
    high_cost: F = F(6)
    trade_cost: F = F(1, 50)
    prior: F = F(1, 2)
    presence: F = F(6, 17)
    beta: F = F(1, 3)


@dataclass(frozen=True)
class Auction:
    no_entry: F
    high: F
    low: F
    high_gain: F
    low_gain: F
    delta: F


@dataclass(frozen=True)
class Flow:
    order: int
    mass: F
    posterior: F
    entry: F
    price: F
    prepared_price: F
    win_if_prepared: F
    challenger_win: F
    incumbent_win: F
    no_sale: F
    high_ownership: F


def auction(par: Parameters, strength: F) -> Auction:
    p = par.reserve
    no_entry = p * (1 - p / strength)
    high = strength / 2 + p * p / (2 * strength)
    low = par.ell - (par.ell**2 - p**2) / (2 * strength)
    return Auction(no_entry, high, low, par.h - high, par.ell - low, high - low)


def flow_rows(par: Parameters, strength: F, buy_rate: F, sell_rate: F,
              hide_price: bool = False) -> tuple[Flow, ...]:
    a = auction(par, strength)
    b = (1 - par.presence) * par.beta
    rows = []
    for order in (-1, 0, 1):
        if order == 1:
            h_mass, l_mass = b + buy_rate, b
        elif order == -1:
            h_mass, l_mass = b, b + sell_rate
        else:
            h_mass = 1 - 2 * b - buy_rate
            l_mass = 1 - 2 * b - sell_rate
        mass = par.prior * h_mass + (1 - par.prior) * l_mass
        mu = par.prior * h_mass / mass
        decision_mu = par.prior if hide_price else mu
        gain = a.low_gain + decision_mu * (a.high_gain - a.low_gain)
        entry = par.rho + (1 - par.rho) * int(gain >= par.high_cost)
        prepared_price = a.low + a.delta * mu
        price = a.no_entry + entry * (prepared_price - a.no_entry)
        win_if_prepared = mu + (1 - mu) * par.ell / strength
        challenger_win = entry * win_if_prepared
        incumbent_win = ((1 - entry) * (1 - par.reserve / strength)
                         + entry * (1 - mu) * (1 - par.ell / strength))
        no_sale = (1 - entry) * par.reserve / strength
        rows.append(Flow(order, mass, mu, entry, price, prepared_price,
                         win_if_prepared, challenger_win, incumbent_win,
                         no_sale, entry * mu))
    return tuple(rows)


def display(value: F) -> str:
    return f"{value} [{float(value):.10f}]"


def describe(par: Parameters, strength: F, buy_rate: F, sell_rate: F,
             branch: str, hide_price: bool = False) -> str:
    a = auction(par, strength)
    rows = flow_rows(par, strength, buy_rate, sell_rate, hide_price)
    minus, zero, plus = rows
    mean_price = sum((x.mass * x.price for x in rows), F(0))
    mean_order = sum((x.mass * x.order for x in rows), F(0))
    volume = minus.mass + plus.mass
    informed_orders = par.prior * buy_rate + (1 - par.prior) * sell_rate
    informed_share = informed_orders / volume
    entry = sum((x.mass * x.entry for x in rows), F(0))
    own = sum((x.mass * x.high_ownership for x in rows), F(0))
    win = sum((x.mass * x.challenger_win for x in rows), F(0))
    eq_entry = sum((x.mass * x.order * x.entry for x in rows), F(0))
    eq_win = sum((x.mass * x.order * x.challenger_win for x in rows), F(0))
    cov_entry = eq_entry - mean_order * entry
    cov_win = eq_win - mean_order * win
    threshold = (par.high_cost - a.low_gain) / (a.high_gain - a.low_gain)
    lines = [f"\nCASE {branch}; r={strength}; s={buy_rate}; t={sell_rate}"]
    for name, value in (("delta", a.delta), ("entry_threshold", threshold),
                        ("volume", volume), ("informed_orders_per_slot", informed_orders),
                        ("informed_share_of_orders", informed_share), ("mean_order", mean_order),
                        ("normalized_imbalance", mean_order / volume),
                        ("entry", entry), ("high_ownership", own),
                        ("challenger_ownership", win), ("mean_price_before_slot", mean_price),
                        ("neutral_price", zero.price), ("conditional_spread", plus.price - minus.price),
                        ("buy_impact_from_neutral", plus.price - zero.price),
                        ("sell_impact_from_neutral", zero.price - minus.price),
                        ("cov_order_entry", cov_entry), ("cov_order_challenger_win", cov_win),
                        ("winner_gap_given_preparation", plus.win_if_prepared - minus.win_if_prepared)):
        lines.append(f"{name}={display(value)}")
    for x in rows:
        lines.append(f"Q={x.order}")
        for name, value in (("mass", x.mass), ("posterior", x.posterior), ("entry", x.entry),
                            ("price", x.price), ("price_change_from_before_slot", x.price - mean_price),
                            ("winner_if_prepared", x.win_if_prepared),
                            ("challenger_win", x.challenger_win),
                            ("incumbent_win", x.incumbent_win), ("no_sale", x.no_sale),
                            ("prepared_price", x.prepared_price),
                            ("preparation_price_change", x.prepared_price - x.price)):
            lines.append(f"  {name}={display(value)}")
        if x.entry < 1:
            lines.append(f"  no_preparation_price_change={display(a.no_entry - x.price)}")
        else:
            lines.append("  no_preparation_event_has_zero_probability")
    for class_name, class_price in (("H", a.high), ("L", a.low)):
        for x in rows:
            terminal_mean = a.no_entry + x.entry * (class_price - a.no_entry)
            payoff = x.order * (terminal_mean - x.price) - par.trade_cost * abs(x.order)
            lines.append(f"informed_{class_name}_payoff_q{x.order}={display(payoff)}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    par = Parameters()
    b = (1 - par.presence) * par.beta
    m = (b + par.presence) / (2 * b + par.presence)
    lines = ["ONE-SLOT OBSERVABLES: EXACT RATIONAL REPORT", str(par),
             "Only decimal displays use floating point.",
             f"b={b}; M={m}; full_order_informed_share={2 * m - 1}",
             "Investor ties permit mixtures; challenger prepares at equality."]
    cases = [(F(6, 5), F(0), F(0), "weak, no informed orders"),
             (F(7, 5), F(0), F(0), "coexistence, no informed orders"),
             (F(7, 5), b * (auction(par, F(7, 5)).delta / par.trade_cost - 2), F(0),
              "coexistence, partial informed buy"),
             (F(31, 20), par.presence, F(0), "coexistence, full informed buy"),
             (F(8, 5), par.presence, F(0), "coexistence, full informed buy"),
             (F(33, 20), par.presence, F(0), "coexistence, full informed buy"),
             (F(3), par.presence, par.presence, "strong, full two-sided orders"),
             (F(69, 20), par.presence, par.presence, "below entry ceiling"),
             (F(173, 50), par.presence, par.presence, "above entry ceiling"),
             (F(18, 5), par.presence, par.presence, "very strong, full two-sided orders")]
    for strength, buy_rate, sell_rate, label in cases:
        lines.append(describe(par, strength, buy_rate, sell_rate, label))
    lines.append(describe(par, F(3), par.presence, par.presence,
                          "strong, price hidden", hide_price=True))
    lines.append("\nSPREAD DECOMPOSITION AT r=3")
    a = auction(par, F(3))
    base = par.rho * a.delta * (2 * m - 1)
    feedback = (1 - par.rho) * (a.low - a.no_entry + a.delta * m)
    lines += [f"posterior_component={display(base)}", f"entry_component={display(feedback)}",
              f"entry_component_fraction={display(feedback / (base + feedback))}"]
    lines.append("\nIDENTIFICATION FROM FULL TWO-SIDED ORDERS AT r=3")
    minus, zero, plus = flow_rows(par, F(3), par.presence, par.presence)
    volume = minus.mass + plus.mass
    theta = 2 * (zero.price - minus.price) / (par.rho * a.delta)
    presence = volume * theta
    beta = volume * (1 - theta) / (2 * (1 - presence))
    lines += [f"informed_share={display(theta)}", f"presence={display(presence)}",
              f"liquidity_activity_each_direction={display(beta)}"]
    lines.append("\nSAME ORDER FREQUENCIES, DIFFERENT INFORMATION")
    for presence, beta in ((par.presence, par.beta), (F(1, 3), F(23, 68))):
        bb = (1 - presence) * beta
        vol = presence + 2 * bb
        mm = (bb + presence) / vol
        lines.append(f"presence={presence}; beta={beta}; volume={vol}; M={mm}; informed_share={presence / vol}")
    lines.append("\nENTRY CEILING: EXACT SIGNS AT RATIONAL ENDPOINTS")
    for r in (F("3.45824702905933"), F("3.45824702905934")):
        a = auction(par, r)
        excess = a.low_gain + m * (a.high_gain - a.low_gain) - par.high_cost
        lines.append(f"r={r}; B_r(M)-c_H={display(excess)}")
    report = "\n".join(lines) + "\n"
    print(report, end="")
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        output = args.output_dir / "exact_results.txt"
        output.write_text(report)
        manifest = ["Inputs and method appear in exact_results.txt.",
                    f"Python: {platform.python_version()}",
                    "Method: finite flow sums with fractions.Fraction; no simulation.",
                    f"Script SHA-256: {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}",
                    f"Report SHA-256: {hashlib.sha256(report.encode()).hexdigest()}"]
        (args.output_dir / "run_receipt.txt").write_text("\n".join(manifest) + "\n")


if __name__ == "__main__":
    main()
