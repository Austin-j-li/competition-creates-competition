"""Produce or revalidate C.10 through the numerical release interface."""
from __future__ import annotations

import argparse
from dataclasses import asdict
from decimal import Decimal
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.class_bounds import BENCHMARK_CASE, benchmark_bounds
from numerics.class_exhibit import CASES, evaluate
from numerics.class_validation import validate_bounds, validate_case
from numerics.io import ROOT, read_csv, sha256, write_csv, write_manifest
from numerics.params import CONTROLS

OUTPUTS = ("numerics/class_exhibit.csv", "numerics/class_conditions.csv", "numerics/class_bounds.csv",
           "numerics/class_deviations.csv", "numerics/class_diagnostics.json")
SOURCES = ("numerics/class_exhibit.py", "numerics/class_bounds.py", "numerics/class_validation.py",
           "numerics/exercises/c10_classes.py", "numerics/params.py", "numerics/deviations.py",
           "numerics/quadrature.py", "tables/equilibrium_controls.csv", "numerics/revision_quantities.csv")


def noise_entries() -> tuple[Decimal, ...]:
    selected = []
    for law in ("Laplace", "logistic"):
        matches = [r for r in read_csv("tables/equilibrium_controls.csv") if r["parameter_set"] == "base"
                   and r["noise"] == law and r["cost_law"] == "atoms" and r["r"] == "3"
                   and r["experiment"] == "feedback" and r["accepted"] == "true"]
        if len(matches) != 1:
            raise ValueError(f"C.10 noise source identity: {law}")
        selected.append(Decimal(matches[0]["E"]))
    for law in ("hyperbolic_secant", "student_t"):
        matches = [r for r in read_csv("numerics/revision_quantities.csv") if r["noise"] == law
                   and r["quantity"] == "E" and r["profile"] == "fixed_full_orders" and r["accepted"] == "true"]
        if len(matches) != 1:
            raise ValueError(f"C.10 noise source identity: {law}")
        selected.append(Decimal(matches[0]["value"]))
    return tuple(selected)


def compute() -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict], bool]:
    rows, conditions, deviations, diagnostics = [], [], [], []
    passed = True
    for case in CASES:
        nodes, margins = evaluate(case)
        result = validate_case(case, nodes, margins, CONTROLS)
        passed &= result.accepted
        summary = asdict(result)
        summary.pop("deviations")
        diagnostics.append({"case": case.name, **summary})
        all_conditions = all(c.satisfied for c in margins if c.scope != "diagnostic")
        for node in nodes:
            rows.append({**node.columns(case), "proposition_required": case.proposition_required,
                         "proposition_satisfied": all_conditions, "status": "analytical" if result.accepted else "open",
                         "uniqueness_status": "unique" if result.accepted else "not established", "accepted": result.accepted})
        for margin in margins:
            conditions.append({**case.columns(), "condition": margin.name, "margin": str(margin.margin),
                               "relation": margin.relation, "scope": margin.scope, "definition": margin.definition,
                               "satisfied": margin.satisfied, "accepted": result.accepted,
                               "status": "analytical" if result.accepted else "open"})
        for record in result.deviations:
            deviations.append({"case": case.name, **dict(zip(("node", "state", "pass", "q", "U_q", "U_candidate",
                               "deviation_gain", "quadrature_error", "tail_bound"), record))})
        print(case.name, "accepted="+str(result.accepted), "proposition="+str(all_conditions),
              "formula_error="+str(result.formula_error), "breaches="+str(result.breaches), flush=True)
    entries = noise_entries()
    values = benchmark_bounds(BENCHMARK_CASE, entries)
    checks = validate_bounds(BENCHMARK_CASE, values, entries, CONTROLS)
    bounds = []
    for value, check in zip(values, checks):
        bounds.append({**BENCHMARK_CASE.columns(), "quantity": value.name, "value": str(value.value),
                       "definition": value.definition, "display_format": value.display, "units": value.units,
                       "branch": value.scope, "independent_value": check.independent_value,
                       "absolute_difference": check.absolute_difference, "accepted": check.accepted,
                       "status": ("numerical diagnostic" if value.scope == "fixed-profile noise range" else "analytical")
                                 if check.accepted else "open"})
        passed &= check.accepted
    return rows, conditions, bounds, deviations, diagnostics, bool(passed)


def run(revalidate: bool = False) -> bool:
    started = time.monotonic()
    rows, conditions, bounds, deviations, diagnostics, passed = compute()
    if revalidate:
        from numerics.io import fmt
        for path, fresh in zip(OUTPUTS[:4], (rows, conditions, bounds, deviations)):
            stored = read_csv(path)
            exact = [{key:fmt(value,key) for key,value in row.items()} for row in fresh]
            same = len(stored) == len(exact) and all(a == b for a,b in zip(stored,exact))
            print("PASS" if same else "FAIL", "C.10 saved output", path)
            passed &= same
    else:
        for path, data in zip(OUTPUTS[:4], (rows, conditions, bounds, deviations)):
            write_csv(path, list(data[0]), data)
        (ROOT/OUTPUTS[4]).write_text(json.dumps(diagnostics,indent=2)+"\n")
        write_manifest("c10_classes", {"cases":[{**c.columns(),"proposition_required":c.proposition_required} for c in CASES],
                       "benchmark": BENCHMARK_CASE.columns(), "source_hashes":{p:sha256(p) for p in SOURCES},
                       "arithmetic_digits":CONTROLS.interval_decimal_precision, "sign_resolution":"1e-40",
                       "tie_rule":"entry_at_indifference; upper Laplace plateau enters at equality", "workers":1},
                       "Decimal auction polynomials and general-prior Laplace formulas; independent realized-auction integrals, "
                       "density roots, full-line flow integrals, and held-schedule deviations at both declared resolutions. "
                       "Benchmark prior endpoints use closed inverse maps and independent roots of the defining margins.",
                       CONTROLS.as_dict(), list(OUTPUTS), {"cases":diagnostics,"bounds":[asdict(c) for c in validate_bounds(BENCHMARK_CASE,
                       benchmark_bounds(BENCHMARK_CASE,noise_entries()),noise_entries(),CONTROLS)],
                       "elapsed_seconds":time.monotonic()-started}, passed,
                       ["The matched point-mass comparison retains its failed recruiting condition and its unchanged entry.",
                        "Every accepted outcome has an analytical global uniqueness argument. Order meshes are numerical diagnostics.",
                        "The four-noise range retains the fixed-profile status of the two additional noise laws.",
                        "No tolerance changes. Thresholds outside the feasible posterior range remain tagged."])
    print("C.10 PASSED" if passed else "C.10 FAILED", "elapsed_seconds="+str(time.monotonic()-started), flush=True)
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revalidate",action="store_true")
    sys.exit(0 if run(parser.parse_args().revalidate) else 1)
