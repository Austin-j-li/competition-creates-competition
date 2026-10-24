"""Merge the workstream registry files and write numbers.tex for the three documents.

Reads registry/<STEM>.csv (every file except HEADER.csv and registry.csv), writes
registry/registry.csv, and writes slot/manuscript/numbers.tex with one
\reg{<key>} entry per row. Prints duplicate keys whose display values differ.
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
TEAM = ROOT / "audit/slot_manuscript_2026_10_23"
REG = TEAM / "registry"
OUT_TEX = ROOT / "slot/manuscript/numbers.tex"
COLS = ["key", "value", "display", "status", "source_script", "run_log", "note"]

rows = {}
conflicts = []
for path in sorted(REG.glob("*.csv")):
    if path.name in ("HEADER.csv", "registry.csv"):
        continue
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            key = (row.get("key") or "").strip()
            if not key:
                continue
            row = {c: (row.get(c) or "").strip() for c in COLS}
            row["note"] = (row["note"] + f" [from {path.stem}]").strip()
            if key in rows and rows[key]["display"] != row["display"]:
                conflicts.append((key, rows[key]["display"], row["display"], path.stem))
                continue
            rows.setdefault(key, row)

with (REG / "registry.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    for key in sorted(rows):
        w.writerow(rows[key])

lines = [
    "% numbers.tex: generated from audit/slot_manuscript_2026_10_23/registry/registry.csv.",
    "% Do not edit by hand. Print a number with \\reg{<key>}.",
    "\\makeatletter",
    "\\providecommand{\\reg}[1]{\\ifcsname reg@#1\\endcsname\\csname reg@#1\\endcsname"
    "\\else\\textbf{??\\detokenize{#1}}\\PackageWarning{numbers}{Unknown registry key #1}\\fi}",
]
for key in sorted(rows):
    lines.append(f"\\expandafter\\def\\csname reg@{key}\\endcsname{{{rows[key]['display']}}}")
lines.append("\\makeatother")
OUT_TEX.write_text("\n".join(lines) + "\n")

print(f"keys: {len(rows)}; conflicts: {len(conflicts)}")
for c in conflicts:
    print("CONFLICT", *c)
sys.exit(1 if conflicts else 0)
