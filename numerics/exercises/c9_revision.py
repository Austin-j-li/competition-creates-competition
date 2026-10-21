"""C.9 producer: profit, stake, and fixed-profile noise quantities for the revision."""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, sha256, write_csv, write_manifest  # noqa: E402
from numerics.params import BENCHMARK, BENCHMARK_STRENGTHS, CONTROLS, REVISION_EXTRA  # noqa: E402
from numerics.revision_quantities import independent_benchmark, noise_entry, stake_bounds, trading_quantities  # noqa: E402
from numerics.revision_validation import validate_noise_entry, validate_trading_and_stakes  # noqa: E402


def run() -> bool:
    started = time.monotonic()
    prim, controls = BENCHMARK, CONTROLS
    weak, strong = BENCHMARK_STRENGTHS["r_weak"], BENCHMARK_STRENGTHS["r_strong"]
    trades = trading_quantities(prim, float(strong))
    stakes = stake_bounds(prim, float(weak), float(strong))
    reference = independent_benchmark(prim, weak, strong, controls)
    trading_check = dict(validate_trading_and_stakes(prim, float(strong), trades, stakes, reference, controls))
    values = {**asdict(trades), **asdict(stakes)}
    rows = []
    for name, independent in reference:
        rows.append({**prim.columns(), "r": weak if name == "Omega_0" else strong, "noise": prim.noise.value,
                     "noise_scale": prim.b, "noise_scale_rule": "declared_b", "nu": "n/a",
                     "cost_law": prim.cost_law.value, "fundamental_prior_H": prim.fundamental_prior_H,
                     "profile": "sufficient_bound" if name.startswith("Omega") else "full_orders",
                     "quantity": name, "value": values[name], "independent_value": independent,
                     "absolute_difference": abs(values[name] - independent),
                     "quadrature_error": trades.quadrature_error if name.startswith("Pi") else 0.0,
                     "accepted": trading_check["accepted"],
                     "status": "numerical diagnostic" if trading_check["accepted"] else "open"})
    noise_records = []
    for law in ("hyperbolic_secant", "student_t"):
        result = noise_entry(prim, float(strong), law, float(REVISION_EXTRA["student_degrees_freedom"]))
        check = validate_noise_entry(prim, result, controls)
        noise_records.append({"result": asdict(result), "validation": asdict(check)})
        rows.append({**prim.columns(), "r": strong, "noise": law, "cost_law": prim.cost_law.value,
                     "noise_scale": result.scale, "noise_scale_rule": "equal_score_bound",
                     "nu": REVISION_EXTRA["student_degrees_freedom"] if law == "student_t" else "n/a",
                     "fundamental_prior_H": prim.fundamental_prior_H, "profile": "fixed_full_orders",
                     "quantity": "E", "value": result.E, "independent_value": check.E,
                     "absolute_difference": abs(result.E - check.E), "quadrature_error": check.quadrature_error,
                     "accepted": check.accepted, "status": "numerical diagnostic" if check.accepted else "open"})
    write_csv("numerics/revision_quantities.csv", list(rows[0]), rows)
    diagnostics = {"trading": asdict(trades), "stake_bounds": asdict(stakes), "trading_validation": trading_check,
                   "noise": noise_records}
    # The half-line endpoint is structural, not a nonfinite computed quantity.
    diagnostics["noise"][0]["result"]["upper"] = "infinity (half-line)"
    (ROOT / "numerics/revision_diagnostics.json").write_text(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
    passed = all(row["accepted"] for row in rows)
    source_files = ["numerics/revision_quantities.py", "numerics/revision_validation.py", "numerics/exercises/c9_revision.py",
                    "numerics/params.py", "numerics/auction.py", "numerics/information.py", "numerics/deviations.py"]
    write_manifest("c9_revision", {**prim.columns(), "strengths": {"r_weak": weak, "r_strong": strong},
                   "prior_H": prim.fundamental_prior_H, "student_degrees_freedom": REVISION_EXTRA["student_degrees_freedom"],
                   "student_scale": "b*(nu+1)/(2*sqrt(nu))", "hyperbolic_secant_density": "sech(z/b)/(pi*b)",
                   "source_hashes": {file: sha256(file) for file in source_files}},
                   "Full-order convolution before trade cost; independent decimal density integrals; S12 and S14 stake formulas; "
                   "closed-form entry boundaries and CDF masses versus independent density roots and quadrature.",
                   controls.as_dict(), ["numerics/revision_quantities.csv", "numerics/revision_diagnostics.json"],
                   {"trading_and_stakes": trading_check, "noise": noise_records, "elapsed_seconds": time.monotonic() - started},
                   passed, ["Gross trade profits exclude k. Stake bounds are sufficient, not exact transition values.",
                            "Noise comparisons hold orders fixed. The Student entry set has two finite boundaries.",
                            "No memo value enters the calculation or its acceptance."])
    for row in rows:
        print(row["quantity"], row["noise"], row["value"], "accepted=" + str(row["accepted"]))
    print("C.9 passed" if passed else "C.9 FAILED")
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
