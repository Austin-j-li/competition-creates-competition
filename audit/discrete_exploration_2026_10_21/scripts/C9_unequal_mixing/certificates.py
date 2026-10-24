"""Compute exact equilibrium schedules and their unilateral payoffs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Iterable


F = Fraction
ZERO = F(0)
ONE = F(1)
HALF = F(1, 2)
FLOW = (-1, 0, 1, 2)
PIN = "9b9bf3ce1a94d5017042192e61c9ceb800d310ba"


@dataclass(frozen=True)
class Parameters:
    h: Fraction = F(10)
    ell: Fraction = F(1)
    p: Fraction = F(1, 2)
    rho: Fraction = F(1, 4)
    c_high: Fraction = F(6)
    k: Fraction = F(1, 50)
    presence: Fraction = ONE
    r: Fraction = F(63, 40)
    noise: tuple[Fraction, Fraction, Fraction] = (F(2, 5), F(2, 5), F(1, 5))


@dataclass(frozen=True)
class Auction:
    t_none: Fraction
    t_high: Fraction
    t_low: Fraction
    g_high: Fraction
    g_low: Fraction
    spread: Fraction


@dataclass(frozen=True)
class Schedule:
    name: str
    beta: Fraction
    entry: tuple[Fraction, Fraction, Fraction, Fraction]


@dataclass(frozen=True)
class Evaluation:
    alpha: Fraction
    f_high: tuple[Fraction, ...]
    f_low: tuple[Fraction, ...]
    probability: tuple[Fraction, ...]
    posterior: tuple[Fraction, ...]
    price: tuple[Fraction, ...]
    gain_high: tuple[Fraction, ...]
    gain_low: tuple[Fraction, ...]
    high_net: Fraction
    low_net: Fraction
    entry_mean: Fraction
    high_ownership: Fraction
    price_belief_difference: tuple[Fraction, ...]
    price_equation_difference: tuple[Fraction, ...]


def auction(params: Parameters) -> Auction:
    r, p, ell = params.r, params.p, params.ell
    t_none = p * (ONE - p / r)
    t_high = r / 2 + p * p / (2 * r)
    t_low = ell - (ell * ell - p * p) / (2 * r)
    g_high = params.h - t_high
    g_low = (ell * ell - p * p) / (2 * r)
    return Auction(t_none, t_high, t_low, g_high, g_low, t_high - t_low)


def gross_preparation(params: Parameters, belief: Fraction) -> Fraction:
    values = auction(params)
    return values.g_low + belief * (values.g_high - values.g_low)


def threshold(params: Parameters) -> Fraction:
    values = auction(params)
    return (params.c_high - values.g_low) / (values.g_high - values.g_low)


def flow_laws(params: Parameters, beta: Fraction) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    u, v, w = params.noise
    alpha = params.presence * beta
    high = ((ONE - alpha) * u, v + alpha * (u - v), w + alpha * (v - w), alpha * w)
    low = (u, v, w, ZERO)
    return high, low


def evaluate(params: Parameters, schedule: Schedule) -> Evaluation:
    values = auction(params)
    high, low = flow_laws(params, schedule.beta)
    probability = tuple((fh + fl) / 2 for fh, fl in zip(high, low))
    posterior = tuple(fh / (fh + fl) if fh + fl else ONE for fh, fl in zip(high, low))
    price = tuple(
        values.t_none + entry * (values.t_low - values.t_none + values.spread * belief)
        for entry, belief in zip(schedule.entry, posterior)
    )
    gain_high = tuple(
        values.t_none + entry * (values.t_high - values.t_none) - quote
        for entry, quote in zip(schedule.entry, price)
    )
    gain_low = tuple(
        values.t_none + entry * (values.t_low - values.t_none) - quote
        for entry, quote in zip(schedule.entry, price)
    )
    high_net = sum((mass * gain_high[index + 1] for index, mass in enumerate(params.noise)), ZERO) - params.k
    low_net = sum((mass * gain_low[index + 1] for index, mass in enumerate(params.noise)), ZERO) - params.k
    entry_mean = sum((mass * entry for mass, entry in zip(probability, schedule.entry)), ZERO)
    high_ownership = sum((mass * entry / 2 for mass, entry in zip(high, schedule.entry)), ZERO)
    belief_difference = []
    equation_difference = []
    for index, quote in enumerate(price):
        same_price = tuple(i for i, other in enumerate(price) if other == quote)
        high_mass = sum((high[i] for i in same_price), ZERO)
        all_mass = sum((high[i] + low[i] for i in same_price), ZERO)
        price_belief = high_mass / all_mass if all_mass else posterior[index]
        belief_difference.append(price_belief - posterior[index])
        expected_quote = values.t_none + schedule.entry[index] * (
            values.t_low - values.t_none + values.spread * price_belief
        )
        equation_difference.append(quote - expected_quote)
    return Evaluation(
        params.presence * schedule.beta,
        high,
        low,
        probability,
        posterior,
        price,
        gain_high,
        gain_low,
        high_net,
        low_net,
        entry_mean,
        high_ownership,
        tuple(belief_difference),
        tuple(equation_difference),
    )


def rising_schedule(params: Parameters) -> Schedule:
    u, v, w = params.noise
    spread = auction(params).spread
    alpha = (u * w / (params.k / spread - params.rho * u / 2) - 2 * w) / (v - w)
    return Schedule("rising_entry", alpha / params.presence, (params.rho, params.rho, ONE, ONE))


def threshold_schedule(params: Parameters) -> Schedule:
    u, v, w = params.noise
    tau = threshold(params)
    alpha = w * (2 * tau - ONE) / ((ONE - tau) * (v - w))
    d_none = 2 * v + alpha * (u - v)
    d_one = 2 * w + alpha * (v - w)
    first_gain = u * v / d_none
    second_gain = v * w / d_one
    entry_one = (params.k / auction(params).spread - params.rho * first_gain) / second_gain
    return Schedule("both_indifferent", alpha / params.presence, (params.rho, params.rho, entry_one, ONE))


def no_trade_schedule(params: Parameters) -> Schedule:
    return Schedule("no_trade", ZERO, (params.rho, params.rho, params.rho, ONE))


def gap_parameters() -> Parameters:
    return replace(Parameters(), r=F(3), c_high=F(83, 24), k=F(1, 10), noise=(F(1, 5), F(1, 5), F(3, 5)))


def gap_schedule(params: Parameters) -> Schedule:
    return Schedule("gap_completion", HALF, (params.rho, ONE, F(5, 12), ONE))


def polynomial(params: Parameters) -> Fraction:
    r = params.r
    return -45 * r**4 + 514 * r**3 - 980 * r**2 + 454 * r - 15


def exact_records(params: Parameters, schedule: Schedule) -> tuple[dict[str, str], tuple[dict[str, str], ...]]:
    result = evaluate(params, schedule)
    values = auction(params)
    summary = {
        "case": schedule.name,
        "r": str(params.r),
        "h": str(params.h),
        "ell": str(params.ell),
        "p": str(params.p),
        "rho": str(params.rho),
        "c_L": "0",
        "c_H": str(params.c_high),
        "k": str(params.k),
        "lambda": str(params.presence),
        "z_minus": str(params.noise[0]),
        "z_zero": str(params.noise[1]),
        "z_plus": str(params.noise[2]),
        "beta_H": str(schedule.beta),
        "beta_L": "0",
        "alpha": str(result.alpha),
        "sigma_at_flow_1": str((schedule.entry[2] - params.rho) / (ONE - params.rho)),
        "Delta_T": str(values.spread),
        "tau": str(threshold(params)),
        "U_H_buy": str(result.high_net),
        "U_H_zero": "0",
        "U_L_buy": str(result.low_net),
        "U_L_zero": "0",
        "E": str(result.entry_mean),
        "O_H": str(result.high_ownership),
    }
    detail = tuple(
        {
            "case": schedule.name,
            "r": str(params.r),
            "lambda": str(params.presence),
            "x": str(flow),
            "f_H": str(result.f_high[index]),
            "f_L": str(result.f_low[index]),
            "probability": str(result.probability[index]),
            "mu": str(result.posterior[index]),
            "entry": str(schedule.entry[index]),
            "price": str(result.price[index]),
            "B_minus_c_H": str(gross_preparation(params, result.posterior[index]) - params.c_high),
            "H_residual": str(result.gain_high[index]),
            "L_residual": str(result.gain_low[index]),
            "price_belief_difference": str(result.price_belief_difference[index]),
            "price_equation_difference": str(result.price_equation_difference[index]),
        }
        for index, flow in enumerate(FLOW)
    )
    return summary, detail


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    material = tuple(rows)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(material[0]))
        writer.writeheader()
        writer.writerows(material)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    flows = []
    rising_entries = []
    threshold_entries = []
    print("Exact schedules. All payoffs use the fixed candidate price and entry schedules.")
    for strength in (F(63, 40), F(79, 50), F(317, 200)):
        params = replace(Parameters(), r=strength)
        for schedule in (no_trade_schedule(params), threshold_schedule(params), rising_schedule(params)):
            summary, detail = exact_records(params, schedule)
            summaries.append(summary)
            flows.extend(detail)
            print(
                f"r={strength} case={schedule.name} beta={summary['beta_H']} "
                f"sigma_1={summary['sigma_at_flow_1']} E={summary['E']} "
                f"U_H={summary['U_H_buy']} U_L={summary['U_L_buy']}"
            )
            print("  posteriors=" + ", ".join(row["mu"] for row in detail))
            print("  preparation margins=" + ", ".join(row["B_minus_c_H"] for row in detail))
            print("  price-belief differences=" + ", ".join(row["price_belief_difference"] for row in detail))
            print("  price equation differences=" + ", ".join(row["price_equation_difference"] for row in detail))
            if schedule.name == "rising_entry":
                rising_entries.append(F(summary["E"]))
            if schedule.name == "both_indifferent":
                threshold_entries.append(F(summary["E"]))
        no_trade_margin = params.k - params.rho * auction(params).spread * sum(params.noise[:2]) / 2
        print(f"  P(r)={polynomial(params)}; no-trade margin={no_trade_margin}")
    print("Strict entry differences=" + ", ".join(str(right - left) for left, right in zip(rising_entries, rising_entries[1:])))
    print("Threshold entry differences=" + ", ".join(str(right - left) for left, right in zip(threshold_entries, threshold_entries[1:])))
    params = replace(Parameters(), r=F(317, 200), presence=F(49, 50))
    summary, detail = exact_records(params, rising_schedule(params))
    summaries.append(summary)
    flows.extend(detail)
    print(f"Uncertain presence: lambda={params.presence}, beta={summary['beta_H']}, E={summary['E']}")
    params = gap_parameters()
    summary, detail = exact_records(params, gap_schedule(params))
    summaries.append(summary)
    flows.extend(detail)
    print("Gap completion=" + json.dumps(summary, sort_keys=True))
    print("  posteriors=" + ", ".join(row["mu"] for row in detail))
    print("  preparation margins=" + ", ".join(row["B_minus_c_H"] for row in detail))
    before_threshold_bound = auction(params).spread * F(1, 5)
    after_threshold_bound = auction(params).spread * (F(1, 10) + params.rho * F(3, 20))
    print(
        f"Gap regime bounds: before threshold, gross >= {before_threshold_bound}; "
        f"after threshold, gross <= {after_threshold_bound}; k={params.k}."
    )
    lower_derivative_bound = -180 * F(8, 5)**3 + 1542 * F(3, 2)**2 - 1960 * F(8, 5) + 454
    print(f"Polynomial derivative lower bound on [3/2,8/5]={lower_derivative_bound}")
    summary_path = args.output_dir / "summary.csv"
    flow_path = args.output_dir / "flows.csv"
    write_csv(summary_path, summaries)
    write_csv(flow_path, flows)
    receipt = {
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "status": "computer-assisted",
        "method": "Exact rational arithmetic for fixed schedules, all feasible investor actions, and price groups.",
        "tolerances": "None. Every calculation uses exact fractions.",
        "paper_commit": PIN,
        "source": "Pinned main.tex Sections 2-4 and Appendix A.3; pinned online_appendix.tex A.3 and B.6.",
        "inputs": "All parameter declarations appear as exact rational strings in summary.csv.",
        "runtime": sys.version,
        "command": sys.argv,
        "outputs": {
            summary_path.name: {"sha256": file_hash(summary_path), "bytes": summary_path.stat().st_size},
            flow_path.name: {"sha256": file_hash(flow_path), "bytes": flow_path.stat().st_size},
        },
        "program_sha256": file_hash(Path(__file__)),
        "scope": "Finite exact schedules; the memo gives separate proofs of general existence and the continuous branch.",
    }
    receipt_path = args.output_dir / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Wrote {summary_path}, {flow_path}, and {receipt_path}.")


if __name__ == "__main__":
    main()
