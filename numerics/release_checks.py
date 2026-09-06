"""Semantic checks at the source-to-display boundary; no files are changed."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def rows(path: str) -> list[dict]:
    with (ROOT / path).open(newline="") as stream:
        return list(csv.DictReader(stream))


def number(value: str) -> Decimal:
    result = Decimal(value)
    require(result.is_finite(), f"nonfinite scalar {value}")
    return result


def registry() -> None:
    from numerics.registry import build_registry
    result, problems = build_registry()
    by_name = {row["name"]: row for row in result}
    for path in ("paper/main.md", "paper/online_appendix.md"):
        for key in re.findall(r"\[\[([A-Za-z0-9_]+)\]\]", (ROOT / path).read_text()):
            require(key in by_name and by_name[key]["status"] != "open", f"required key {key} missing/open")
    require(not problems, f"registry problems: {problems}")


def controls() -> None:
    data = [r for r in rows("tables/equilibrium_controls.csv") if r["accepted"] == "true"]
    keys = [(r["parameter_set"], r["noise"], r["cost_law"], r["r"], r["experiment"]) for r in data]
    require(len(keys) == len(set(keys)), "duplicate control parameter/experiment row")
    indexed = dict(zip(keys, data))
    tolerance = Decimal("1e-9")
    for noise in ("Laplace", "logistic"):
        for cost in ("atoms", "uniform_mixture"):
            for strength in ("1.2", "3"):
                def get(experiment: str) -> dict:
                    key = ("base", noise, cost, strength, experiment)
                    require(key in indexed, f"missing exact control identity {key}")
                    row = indexed[key]
                    require(row["accepted"] == "true", f"control {key} not accepted")
                    return row
                feedback, hidden, matched = (get(e) for e in ("feedback", "price_hidden", "matched_dividend"))
                for field in ("R_T", "W", "E", "O_H", "q_H", "q_L", "e_H", "e_L", "expected_preparation_cost"):
                    require(abs(number(matched[field]) - number(hidden[field])) <= tolerance,
                            f"external dividend changes {field} in {noise}/{cost}/{strength}")
                require(abs(number(matched["matched_dividend"]) - number(feedback["R_T"]) + number(hidden["R_T"])) <= tolerance,
                        "matched dividend fails financial-price identity")


def certificates() -> None:
    from numerics.certificates import certify, endpoint_str
    from numerics.params import BENCHMARK, CERTIFICATE_BRACKETS, CONTROLS
    data = rows("numerics/certificates.csv")
    require(len(data) == len(CERTIFICATE_BRACKETS), "certificate count")
    for strength, lower, upper in CERTIFICATE_BRACKETS:
        found = [r for r in data if number(r["r"]) == number(strength)]
        require(len(found) == 1, f"certificate identity {strength}")
        row = found[0]
        require(row["accepted"] == "true" and row["v_lower"] == lower and row["v_upper"] == upper, "certificate bracket/acceptance")
        fresh = certify(BENCHMARK, strength, lower, upper, CONTROLS)
        require(fresh.accepted, f"fresh certificate fails {strength}: {fresh.failures}")
        for column, key, side in (("Psi_left_lower", "Psi_left", "lower"), ("Psi_left_upper", "Psi_left", "upper"),
                                  ("Psi_right_lower", "Psi_right", "lower"), ("Psi_right_upper", "Psi_right", "upper"),
                                  ("Gamma_H_lower", "Gamma_H", "lower"), ("E_lower", "E", "lower"), ("E_upper", "E", "upper")):
            stored, computed = number(row[column]), number(endpoint_str(fresh.values[key], side))
            require(stored <= computed if side == "lower" else stored >= computed, f"inward certificate enclosure {strength}/{column}")
        require(number(row["Psi_left_lower"]) > 0 and number(row["Psi_right_upper"]) < 0 and number(row["Gamma_H_lower"]) > 0,
                f"certificate sign {strength}")


def pools() -> None:
    from numerics.exercises.c6b_price_pools import closed_forms, cutoff_family, evaluate_member
    import mpmath as mp
    data = [r for r in rows("numerics/price_pool_regression.csv") if r["accepted"] == "true"]
    require(len(data) == 17, "price-pool family must retain all17 members")
    require(len({r["continuation_id"] for r in data}) == 17, "distinct price pools merged by orders")
    family = dict(cutoff_family())
    for row in data:
        for key, expected in {"h":"10", "ell":"1", "p":"7", "r":"1.2", "rho":"0.25", "c_L":"1", "c_H":"6", "b":"2", "k":"0.02", "q_H":"1", "q_L":"-1"}.items():
            require(number(row[key]) == number(expected), f"pool parameter {key}")
        with mp.workdps(60):
            expected = closed_forms(mp.mpf(row["cutoff_decimal"]))
        for column, key in (("pool_posterior", "pool_posterior"), ("preparation_probability", "E"),
                            ("sale_probability", "sale"), ("seller_revenue", "revenue")):
            require(abs(number(row[column]) - Decimal(str(expected[key]))) <= Decimal("1e-9"), f"pool price-information identity {column}")
        require(number(row["buyer_slack_zero_price_c_L"]) >= 0, "buyer deviation inside observed-price pool")
        require(row["cutoff_exact"] in family, "undeclared price-pool cutoff")
        expected_row, _, validation = evaluate_member(row["cutoff_exact"], family[row["cutoff_exact"]])
        require(expected_row["accepted"] and row["continuation_id"] == expected_row["continuation_id"],
                "pool preparation/pricing policy differs from validated observed-price policy")


def endpoints() -> None:
    data = rows("figures_data/posterior_tails.csv")
    for row in data:
        if row["noise"] == "logistic" and number(row["M_minus_tau"]) <= 0:
            require(row["x_star"] == "unattainable", "finite cutoff at unattained logistic bound")
            require(all(number(row[k]) == 0 for k in ("alpha_H", "alpha_L", "posterior_upper_tail_mass")), "positive logistic mass at unattained bound")
            require(number(row["E"]) == Decimal("0.25"), "logistic endpoint preparation")


def candidates() -> None:
    for path in ("numerics/correspondence.csv", "numerics/reserve_continuations.csv", "numerics/reserve_events.csv"):
        for row in rows(path):
            if row["accepted"] != "true":
                continue
            status = row.get("result_status", row.get("existence_status", row.get("status", "")))
            require(status.startswith(("analytical", "computer-assisted", "numerical diagnostic")), f"unvalidated candidate accepted in {path}")
            require(row.get("error_budget_breaches", "") == "", f"accepted candidate breached error budget in {path}")
            for key in ("candidate_id", "continuation_id", "parameter_set_id"):
                require(row.get(key, "") not in ("", "n/a"), f"missing {key} in {path}")
            for key, bound in (("epsilon_P", "1e-8"), ("epsilon_e", "1e-8"), ("epsilon_q", "1e-7")):
                require(0 <= number(row[key]) <= Decimal(bound), f"accepted candidate fails {key} in {path}")


def finite() -> None:
    # Only numerical boundary files; audit attempts retain their explicit failure witnesses.
    for path in ("tables/equilibrium_controls.csv", "tables/reserve_comparisons.csv", "numerics/certificates.csv",
                 "numerics/price_pool_regression.csv", "figures_data/posterior_tails.csv", "tables/auction_primitives.csv",
                 "tables/extensions.csv", "numerics/two_signals.csv", "numerics/moderate_values.csv",
                 "figures_data/bargaining.csv", "figures_data/two_returns.csv"):
        for index, row in enumerate(rows(path), 2):
            for key, value in row.items():
                try:
                    parsed = Decimal(value)
                except InvalidOperation:
                    continue
                require(parsed.is_finite(), f"nonfinite untagged field {path}:{index}/{key}")


CHECKS = {fn.__name__: fn for fn in (registry, controls, certificates, pools, endpoints, candidates, finite)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", choices=CHECKS, nargs="+", default=list(CHECKS))
    args = parser.parse_args()
    for name in args.check:
        CHECKS[name]()
        print(f"PASS release boundary: {name}", flush=True)
