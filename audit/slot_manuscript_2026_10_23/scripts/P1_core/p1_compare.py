"""Round-2 comparisons for registry/P1_core.csv (print only).

1. Round 1 against round 2: keys added or removed, display changes, value changes.
2. Each round-2 enclosure against the independent exact interval of the check XP1
   (scripts/XP1/xp1_registry_recompute.csv, columns low and high as exact rationals):
   'contains' means the printed enclosure contains the whole independent interval.
Run from the repository root:
  .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_compare.py
"""
import csv
import re
from decimal import Decimal
from fractions import Fraction as Fr

from p1_common import HERE, TEAM, REGISTRY, Log

log = Log(HERE / "p1_compare.log")
OLD = HERE / "round1" / "P1_core.csv"
XP1 = TEAM / "scripts" / "XP1" / "xp1_registry_recompute.csv"


def read(path):
    with path.open() as fh:
        return {row["key"]: row for row in csv.DictReader(fh)}


def num(s):
    """Exact Fraction from 'a/b', an integer or a decimal string."""
    s = s.strip()
    if "/" in s:
        a, b = s.split("/")
        return Fr(int(a), int(b))
    return Fr(Decimal(s))


old, new, xp = read(OLD), read(REGISTRY), read(XP1)
log("1. Round 1 against round 2")
added = [k for k in new if k not in old]
removed = [k for k in old if k not in new]
log(f"   rows: round 1 {len(old)}, round 2 {len(new)}")
log(f"   keys removed: {removed if removed else 'none'}")
log(f"   keys added ({len(added)}): {', '.join(added)}")
disp = [(k, old[k]["display"], new[k]["display"]) for k in old if k in new and old[k]["display"] != new[k]["display"]]
log(f"   display changes: {len(disp)}")
for k, a, b in disp:
    log(f"     {k}: {a} -> {b}")
stat = [(k, old[k]["status"], new[k]["status"]) for k in old if k in new and old[k]["status"] != new[k]["status"]]
log(f"   status changes: {len(stat)}")
for k, a, b in stat:
    log(f"     {k}: {a} -> {b}")
vchg = []
for k in old:
    if k in new and old[k]["value"] != new[k]["value"]:
        a, b = num(old[k]["value"]), num(new[k]["value"])
        vchg.append((k, old[k]["value"], new[k]["value"], float(abs(a - b))))
log(f"   value strings that changed: {len(vchg)} (largest absolute change "
    f"{max(v[3] for v in vchg):.3e})" if vchg else "   value strings that changed: 0")
for k, a, b, dv in sorted(vchg, key=lambda v: -v[3])[:12]:
    log(f"     {k}: {a} -> {b} (change {dv:.3e})")

log("\n2. Round-2 enclosures against the independent exact intervals of XP1")
pat = re.compile(r"outward enclosure(?: of the rational bracket)? \[([-0-9.]+), ([-0-9.]+)\]")
counts = {"contains": 0, "overlaps only": 0, "DISJOINT": 0, "no XP1 row": 0}
for k, row in new.items():
    m = pat.search(row["note"])
    if not m:
        continue
    lo, hi = num(m.group(1)), num(m.group(2))
    if k not in xp:
        counts["no XP1 row"] += 1
        log(f"   {k}: enclosure [{m.group(1)}, {m.group(2)}]; no XP1 row (new in round 2)")
        continue
    xlo, xhi = num(xp[k]["low"]), num(xp[k]["high"])
    if lo <= xlo and xhi <= hi:
        verdict = "contains"
    elif hi < xlo or xhi < lo:
        verdict = "DISJOINT"
    else:
        verdict = "overlaps only"
    counts[verdict] += 1
    if verdict != "contains":
        log(f"   {k}: {verdict}; round 2 [{m.group(1)}, {m.group(2)}]; XP1 [{float(xlo)!r}, {float(xhi)!r}]")
    if xp[k]["display"] != row["display"]:
        log(f"   {k}: display {row['display']} differs from the XP1 display {xp[k]['display']}")
log("   " + "; ".join(f"{v} {n}" for v, n in counts.items()))
nodisp = [k for k in new if k in xp and xp[k]["display"] != new[k]["display"]]
log(f"   displays that differ from XP1: {len(nodisp)}" + (f" ({', '.join(nodisp)})" if nodisp else ""))
log.close()
