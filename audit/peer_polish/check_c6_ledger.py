"""Reconcile C6 numerical CSVs with every completed-node attempt ledger."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_csv(path):
    with (ROOT / path).open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(exercise, continuation_file, range_file):
    manifest = json.loads((ROOT / f"numerics/manifests/{exercise}.json").read_text())
    ledger = ROOT / manifest["inputs"]["attempt_ledger"]
    files = sorted(ledger.glob("*.jsonl")) if ledger.is_dir() else [ledger]
    results = [json.loads(line) for file in files for line in file.read_text().splitlines()]
    require(all(isinstance(record, list) and len(record) == 3 for record in results), f"{exercise}: failed node present")
    rows, ranges = read_csv(continuation_file), read_csv(range_file)
    require(len(ranges) == len(results), f"{exercise}: node ledger length")
    require(len(rows) == sum(len(record[0]) for record in results), f"{exercise}: candidate rows lost")
    require(len({r["candidate_id"] for r in rows}) == len(rows), f"{exercise}: duplicate candidate id")
    by_id = {r["candidate_id"]: r for r in rows}
    by_node = defaultdict(list)
    for row in rows:
        by_node[(row["value_law"], row["r"], row["p_exact"])].append(row)
        require(not any(value.lower() in ("nan", "inf", "-inf", "infinity", "-infinity") for value in row.values()), "nonfinite ordinary scalar")
        if row["accepted"] == "true":
            require(not row["rejection_reason"] and not row["error_budget_breaches"], "accepted row with validation breaches")
            require(not row["identity_note"], "unresolved identity in the benchmark-only reserve search")
            require(row["result_status"] != "rejected", "accepted/rejected status conflict")
            require(float(row["epsilon_q"]) <= 1e-7 and float(row["pricing_error"]) <= 1e-8, "accepted row exceeds strategic bound")
            require(0 <= float(row["two_admissible_bidders_probability"]) <= float(row["admissible_challenger_probability"]) + 1e-15
                    <= float(row["preparation_probability"]) + 2e-15 <= 1 + 3e-15, "admissible-bid bounds")
        if row["duplicate_of"]:
            target = by_id.get(row["duplicate_of"])
            require(target is not None and target["accepted"] == "true" and row["parameter_set_id"] == target["parameter_set_id"], "invalid deduplication target")
    identities = set()
    for rng in ranges:
        key = (rng["value_law"], rng["r"], rng["p_exact"])
        require(key not in identities, "duplicate reserve node")
        identities.add(key)
        rr = by_node[key]
        accepted = [r for r in rr if r["accepted"] == "true"]
        distinct = [r for r in accepted if not r["duplicate_of"]]
        require(int(rng["candidates_evaluated"]) == int(rng["candidates_accepted_raw"]) + int(rng["candidates_rejected"]) + int(rng["candidates_unresolved"]), "attempt count partition")
        require(int(rng["candidates_accepted_raw"]) == len(accepted), "accepted raw count")
        require(int(rng["accepted_continuations_found"]) == len(distinct), "distinct continuation count")
        require(int(rng["duplicates_merged"]) == len(accepted) - len(distinct), "duplicate count")
        for quantity in ("E", "R_T"):
            for bound, fun in (("min", min), ("max", max)):
                value = rng[f"{quantity}_{bound}_found"]
                require((value == "n/a") if not distinct else abs(float(value) - fun(float(r[quantity]) for r in distinct)) < 1e-14, "found range disagrees with accepted rows")
    totals = {name: sum(int(r[name]) for r in ranges) for name in ("candidates_evaluated", "candidates_accepted_raw", "candidates_rejected", "candidates_unresolved", "duplicates_merged")}
    return {"exercise": exercise, "nodes": len(ranges), "csv_candidate_rows": len(rows), **totals,
            "open_nodes": sum(r["search_unresolved"] == "true" for r in ranges),
            "nodes_without_accepted": sum(int(r["accepted_continuations_found"]) == 0 for r in ranges),
            "multiple_nodes": sum(int(r["accepted_continuations_found"]) > 1 for r in ranges),
            "nodes_by_economy": dict(Counter(r["value_law"] + ":r=" + r["r"] for r in ranges)), "passed": True}


if __name__ == "__main__":
    results = [check("c6_reserve", "numerics/reserve_continuations.csv", "numerics/reserve_ranges.csv"),
               check("c6c_reserve_events", "numerics/reserve_events.csv", "numerics/reserve_event_ranges.csv")]
    (ROOT / "audit/peer_polish/c6_ledger_verification.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
