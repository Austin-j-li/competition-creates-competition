"""Spec16.4: corrupt isolated copies and require the real release boundary to reject."""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def change_csv(root: Path, path: str, mutate) -> None:
    file = root / path
    with file.open(newline="") as stream:
        reader = csv.DictReader(stream)
        fields, data = reader.fieldnames, list(reader)
    mutate(data)
    with file.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def test_negative_release_copies() -> None:
    checks = []
    with tempfile.TemporaryDirectory(prefix="ccc-negative-") as temporary:
        baseline = Path(temporary) / "baseline"
        for directory in ("numerics", "paper", "tables", "figures_data"):
            shutil.copytree(ROOT / directory, baseline / directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pdf", "build", "drafts"))
        def selected(data):
            return next(r for r in data if r.get("accepted") == "true" and r.get("experiment") == "feedback")
        def missing(data):
            data[:] = [r for r in data if r["name"] != "base_entry_strong"]
        def duplicate(data):
            data.append(dict(selected(data)))
        def wrong_information(data):
            selected(data)["noise"] = "different-information-law"
        def open_accepted(data):
            row = next(r for r in data if r.get("result_status") == "open")
            row["accepted"] = "true"
        def certificate(data):
            data[0]["Gamma_H_lower"] = "0"
        def merged(data):
            accepted = [r for r in data if r["accepted"] == "true"]
            accepted[-1]["continuation_id"] = accepted[0]["continuation_id"]
        def raw_belief(data):
            row = next(r for r in data if r["accepted"] == "true")
            row["continuation_id"] += "|INVALID_raw_posterior_inside_pool:c_L=prepare"
        def dividend(data):
            row = next(r for r in data if r["experiment"] == "matched_dividend" and r["r"] == "3")
            row["R_T"] = str(float(row["R_T"]) + float(row["matched_dividend"]))
        def logistic(data):
            row = next(r for r in data if r["noise"] == "logistic" and float(r["M_minus_tau"]) == 0)
            row.update(x_star="1000", posterior_upper_tail_mass="1e-6")
        def nan(data):
            selected(data)["E"] = "nan"
        cases = [
            ("missing_required_key", "registry", "paper/quantity_manifest.csv", missing),
            ("duplicate_selected_row", "controls", "tables/equilibrium_controls.csv", duplicate),
            ("wrong_information_same_r", "controls", "tables/equilibrium_controls.csv", wrong_information),
            ("open_candidate_accepted", "candidates", "numerics/correspondence.csv", open_accepted),
            ("zero_containing_certificate", "certificates", "numerics/certificates.csv", certificate),
            ("merged_price_pool_endpoints", "pools", "numerics/price_pool_regression.csv", merged),
            ("raw_flow_posterior_inside_pool", "pools", "numerics/price_pool_regression.csv", raw_belief),
            ("external_dividend_as_revenue", "controls", "tables/equilibrium_controls.csv", dividend),
            ("finite_logistic_limit", "endpoints", "figures_data/posterior_tails.csv", logistic),
            ("nan_ordinary_scalar", "finite", "tables/equilibrium_controls.csv", nan),
        ]
        for check in dict.fromkeys(case[1] for case in cases):
            result = subprocess.run([sys.executable, "numerics/release_checks.py", "--check", check],
                                    cwd=baseline, text=True, capture_output=True)
            if result.returncode:
                raise AssertionError(f"pristine boundary {check} already fails: {result.stderr}")
        expected_errors = {
            "missing_required_key": "base_entry_strong", "duplicate_selected_row": "duplicate control",
            "wrong_information_same_r": "missing exact control identity", "open_candidate_accepted": "unvalidated candidate accepted",
            "zero_containing_certificate": "certificate sign", "merged_price_pool_endpoints": "distinct price pools merged",
            "raw_flow_posterior_inside_pool": "pool preparation/pricing policy", "external_dividend_as_revenue": "external dividend changes",
            "finite_logistic_limit": "finite cutoff at unattained", "nan_ordinary_scalar": "nonfinite untagged field",
        }
        for name, check, path, mutate in cases:
            copy = Path(temporary) / name
            shutil.copytree(baseline, copy)
            change_csv(copy, path, mutate)
            result = subprocess.run([sys.executable, "numerics/release_checks.py", "--check", check],
                                    cwd=copy, text=True, capture_output=True)
            checks.append({"case": name, "exit_code": result.returncode,
                           "diagnostic": (result.stdout + result.stderr)[-2000:]})
            if result.returncode == 0 or expected_errors[name] not in result.stderr:
                raise AssertionError(f"wrong rejection for {name}: {result.stdout} {result.stderr}")
        result = subprocess.run(["sh", str(ROOT / "audit/peer_polish/reference_seed/run_seed.sh")],
                                env={**os.environ, "PYTHONOPTIMIZE": "1", "PYTHON": sys.executable},
                                cwd=temporary, text=True, capture_output=True)
        if result.returncode == 0 or "refusing to run" not in result.stderr:
            raise AssertionError("legacy assertions can be disabled")
        checks.append({"case": "optimized_legacy_seed", "exit_code": result.returncode, "diagnostic": result.stderr})
    target = ROOT / "audit/peer_polish/logs/s6_negative_tests.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"passed": len(checks), "failed": 0, "checks": checks}, indent=2) + "\n")


if __name__ == "__main__":
    test_negative_release_copies()
    print("PASS11 isolated release-boundary corruptions rejected")
