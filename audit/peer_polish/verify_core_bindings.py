#!/usr/bin/env python3
"""Bind the completed independent scans to current CSVs and recheck objects.

Only cutoff spellings may change in ordinary inputs. Registry comparison covers
the nine value fields actually tested; all other registry fields need the release gate.
This check does not repeat global scans or replace independent_checks.json.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import independent_checks as c

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "audit/peer_polish"
FIXED_RESERVES = "audit/peer_polish/c6_fixed_vm/tables/reserve_comparisons.csv"
REGISTRY_KEYS = (
    "base_r_pool_unique_sufficient", "base_r_no_trade_exact",
    "base_r_full_unique_sufficient", "base_r_high_cost_ceiling", "base_m", "base_M",
    "base_laplace_entry_ceiling_left_limit", "logistic_flow_threshold",
    "logistic_threshold_noise_sd",
)
CUTOFF_COLUMNS = {"x_star", "x_star_Yplus", "x_star_Yminus"}
TAGS = {"inf": "unattainable", "-inf": "always", "nan": "n/a"}
RESERVE_ID_COLUMNS = {"event_id", "information_structure_id", "branch", "candidate_id",
                      "p_exact", "institution_id", "continuation_id", "parameter_set_id"}
DECLARATIONS = ("benchmark", "moderate acquisition values", "complementary signals", "numerical controls")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reserve-comparisons", default=FIXED_RESERVES)
    args = parser.parse_args()
    original = json.loads((AUDIT / "independent_checks.json").read_text())
    L = c.Ledger()
    L.require("binding", "original full run has no required failure",
              sum(v["required_fail"] for v in original["summary"].values()) == 0)
    L.require("binding", "the four C.0 declarations used by these checks equal the tested declarations",
              all(c.DECL[name] == original["declarations_parsed_from_C0"][name] for name in DECLARATIONS))
    bindings = []
    for path, old_hash in original["input_sha256"].items():
        snapshot = AUDIT / "independent_inputs" / path
        current_path = args.reserve_comparisons if path == FIXED_RESERVES else path
        current = ROOT / current_path
        L.require("binding", f"snapshot hash: {path}", digest(snapshot) == old_hash)
        before, after = rows(snapshot), rows(current)
        changed_columns = sorted({key for old, new in zip(before, after)
                                  for key in old if old.get(key) != new.get(key)})
        if path == "numerics/quantity_registry.csv":
            old_values = {r["name"]: r["value"] for r in before if r["name"] in REGISTRY_KEYS}
            new_values = {r["name"]: r["value"] for r in after if r["name"] in REGISTRY_KEYS}
            same = len(old_values) == len(REGISTRY_KEYS) and old_values == new_values
            scope = {"keys": REGISTRY_KEYS, "columns": ["value"]}
        elif path == FIXED_RESERVES:
            added = set(after[0]) - set(before[0])
            projected = [{key: row.get(key) for key in before[0]} for row in after]
            same = before == projected and added <= RESERVE_ID_COLUMNS
            scope = {"columns": list(before[0]), "added_metadata": sorted(added),
                     "metadata_validation": "C6 continuation identity and ledger audit"}
        else:
            normalized = [{key: TAGS.get(value, value) if key in CUTOFF_COLUMNS else value
                           for key, value in row.items()} for row in before]
            same = normalized == after
            scope = {"columns": "all", "permitted_change": "cutoff endpoint spellings only"}
        L.require("binding", f"tested fields preserved: {path}", same)
        bindings.append({"tested_path": path, "current_path": current_path,
                         "tested_sha256": old_hash, "current_sha256": digest(current),
                         "changed_columns": changed_columns, "scope": scope, "passed": same})

    producer_serialization = []
    for path in ("tables/equilibrium_controls.csv", "numerics/two_signals.csv", "numerics/moderate_controls.csv"):
        before_path, current = AUDIT / "pre_cutoff_tags" / path, ROOT / path
        before, after = rows(before_path), rows(current)
        normalized = [{key: TAGS.get(value, value) if key in CUTOFF_COLUMNS else value
                       for key, value in row.items()} for row in before]
        same = normalized == after
        L.require("serialization", f"only cutoff tags changed after producer rerun: {path}", same)
        producer_serialization.append({"path": path, "before_sha256": digest(before_path),
                                       "current_sha256": digest(current), "passed": same})

    # Recompute the mathematical objects after serialization, using the independent
    # formulas. The original full run retains every expensive global scan.
    c.RESERVE_COMPARISONS = args.reserve_comparisons
    c.t02_t03_auction(L)
    c.thresholds(L)
    objects = c.t04_t05_t06_t08_t09_t10(L, {})
    c.t11_logistic(L)
    c.t12_atomless(L, objects)
    c.t13_moderate(L, {})
    c.reserve_rows(L, {})
    c.t14_t15_signals(L, {})
    for binding in bindings:
        L.require("binding", f"current input unchanged during check: {binding['current_path']}",
                  digest(ROOT / binding["current_path"]) == binding["current_sha256"])
    for binding in producer_serialization:
        L.require("serialization", f"producer output unchanged during check: {binding['path']}",
                  digest(ROOT / binding["path"]) == binding["current_sha256"])
    failed = sum(r["status"] == "FAIL" and r["required"] for r in L.rows)
    result = {"summary": {"checks": len(L.rows), "required_fail": failed},
              "original_run_sha256": digest(AUDIT / "independent_checks.json"),
              "bindings": bindings, "declaration_scope": DECLARATIONS,
              "producer_serialization": producer_serialization, "checks": L.rows,
              "note": "Fresh object checks; global scans are the original hash-bound run."}
    (AUDIT / "independent_input_bindings.json").write_text(json.dumps(result, indent=1, default=str) + "\n")
    print(json.dumps(result["summary"]))
    for row in L.rows:
        if row["status"] == "FAIL":
            print(row)
    return int(failed > 0)


if __name__ == "__main__":
    raise SystemExit(main())
