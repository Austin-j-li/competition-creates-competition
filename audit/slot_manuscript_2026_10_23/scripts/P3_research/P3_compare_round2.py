"""Print a comparison of the round-2 registry of P3 with round 1 and with the exact enclosures of the check XP3.

Usage: python P3_compare_round2.py  (from the team folder). The program prints counts and every exception."""
import csv
import json
import re
from fractions import Fraction as Fr
from pathlib import Path

TEAM = Path(__file__).resolve().parents[2]
old = {r["key"]: r for r in csv.DictReader(open(TEAM / "scripts/P3_research/round1_P3_research.csv"))}
new = {r["key"]: r for r in csv.DictReader(open(TEAM / "registry/P3_research.csv"))}
xp3 = json.load(open(TEAM / "scripts/XP3/exact_enclosures.json"))
bad = {r["key"]: r for r in csv.DictReader(open(TEAM / "scripts/XP3/invalid_enclosures.csv"))}
own = json.load(open(TEAM / "scripts/P3_research/P3_enclosures.json"))["rows"]

print(f"keys: round 1 {len(old)}, round 2 {len(new)}, same key list in the same order: {list(old) == list(new)}")
for col in ("value", "display", "status", "source_script", "run_log"):
    diff = [k for k in old if k in new and old[k][col] != new[k][col]]
    print(f"  column {col}: {len(diff)} differences {diff}")
notes = [k for k in old if old[k]["note"] != new[k]["note"]]
print(f"  column note: {len(notes)} rows changed")


def frac(s):
    return Fr(s)


def contains(lo, hi, xlo, xhi):
    return lo <= xlo and xhi <= hi


pat = re.compile(r"enclosure \[([-0-9.]+), ([-0-9.]+)\]|enclosure ([-0-9.]+)$")
n_enc = n_ok = 0
fails = []
for k, r in new.items():
    m = pat.search(r["note"])
    if not m:
        continue
    n_enc += 1
    lo, hi = (frac(m.group(1)), frac(m.group(2))) if m.group(1) else (frac(m.group(3)), frac(m.group(3)))
    x = xp3[k]
    xlo, xhi = frac(x["lo"]), frac(x["hi"])
    if contains(lo, hi, xlo, xhi):
        n_ok += 1
    else:
        fails.append((k, str(lo), str(hi), x["lo"], x["hi"]))
print(f"enclosure notes in round 2: {n_enc}; contain the exact XP3 interval: {n_ok}; fail: {len(fails)}")
for f in fails:
    print("  FAIL", f)
listed = [k for k in bad if pat.search(new[k]["note"])]
okl = sum(1 for k in listed if k not in {f[0] for f in fails})
print(f"keys of invalid_enclosures.csv: {len(bad)}; with a round-2 enclosure note: {len(listed)}; now valid: {okl}")
for k in bad:
    if k not in listed:
        print(f"  listed key without a round-2 enclosure note: {k}: {new[k]['note']}")

n_j = n_jok = 0
for k, e in own.items():
    if k not in xp3:
        continue
    n_j += 1
    lo, hi = frac(e["lo"]), frac(e["hi"])
    xlo, xhi = frac(xp3[k]["lo"]), frac(xp3[k]["hi"])
    # both enclose the same exact number, so the two intervals must intersect
    if lo <= xhi and xlo <= hi:
        n_jok += 1
    else:
        print(f"  DISJOINT {k}: own [{e['lo']}, {e['hi']}] vs XP3 [{xp3[k]['lo']}, {xp3[k]['hi']}]")
print(f"P3_enclosures.json rows: {len(own)}; compared with XP3: {n_j}; intervals intersect: {n_jok}")
