"""Print registry rows whose key matches a regular expression. Usage: lookup.py REGEX [REGEX ...]"""
import csv, re, sys, pathlib
REG = pathlib.Path(__file__).resolve().parents[2] / "registry" / "registry.csv"
rows = list(csv.DictReader(REG.open()))
for pat in sys.argv[1:]:
    rx = re.compile(pat)
    for r in rows:
        if rx.search(r["key"]):
            print(f"{r['key']} | {r['display']} | {r['status'][:5]} | {r['note'][:80]}")
