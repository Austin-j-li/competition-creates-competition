"""Print registry differences and exact containment counts. This program writes no files."""
import argparse
import csv
import json
import re
from fractions import Fraction
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--published", action="store_true", help="Read the final registries instead of the candidates.")
args = parser.parse_args()
team = Path(__file__).resolve().parents[2]
pattern = re.compile(r"enclosure[= ]+\[([^,]+),\s*([^\]]+)\]", re.I)

for package in ("P2_auction", "P5_observables"):
    folder = team / "scripts" / package
    path = team / "registry" / f"{package}.csv" if args.published else folder / "EX_candidate.csv"
    with (folder / "EX_before.csv").open(newline="") as fh:
        old = list(csv.DictReader(fh))
    with path.open(newline="") as fh:
        new = list(csv.DictReader(fh))
    exact = json.loads((folder / "EX_exact_enclosures.json").read_text())
    print(f"\nPACKAGE {package}: old rows={len(old)}, new rows={len(new)}")
    print("key order unchanged:", [r["key"] for r in old] == [r["key"] for r in new])
    for column in old[0]:
        changes = [(a["key"], a[column], b[column]) for a, b in zip(old, new) if a[column] != b[column]]
        print(f"COLUMN {column}: {len(changes)} differences")
        for key, before, after in changes:
            print(f"  {key}: {before!r} -> {after!r}")
    count = contained = equal = exact_equal = 0
    for row in new:
        match = pattern.search(row["note"])
        if match is None:
            continue
        count += 1
        a, b = map(Fraction, match.groups())
        lower, upper = (Fraction(exact[row["key"]][k]) for k in ("lo", "hi"))
        contains = a <= lower <= upper <= b
        contained += contains
        equal += a == b
        exact_equal += a == b == lower == upper
        if not contains or (a == b and not a == lower == upper):
            print("ENCLOSURE EXCEPTION", row["key"], row["note"], exact[row["key"]])
    old_count = old_equal = 0
    for row in old:
        match = pattern.search(row["note"])
        if match:
            old_count += 1
            old_equal += Fraction(match[1]) == Fraction(match[2])
    print(f"SUMMARY {package}: old notes={old_count}, old equal={old_equal}, new notes={count}, "
          f"contain exact interval={contained}, equal={equal}, equal and exact={exact_equal}")
    if package == "P5_observables":
        by_key = {r["key"]: r for r in new}
        for row in old:
            if row["key"] in ("vol_full_B", "theta_max_full_eq_r1_B"):
                print("MANUAL NOTE", row["key"], "unchanged:", row["note"] == by_key[row["key"]]["note"])
