"""Apply the A-fragments to a scratch copy of main.tex and print what was replaced.

Print-only. It never writes into the manuscript clone. It writes a scratch copy for a
compile check:
    .venv/bin/python audit/revision_v2_2026_10_21/scripts/A_apply_fragments.py OUTDIR
Then compile OUTDIR/main.tex (figures/ and tables/ are linked from the clone).
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLONE = ROOT / "overleaf" / "paper-revision"
DRAFTS = ROOT / "audit" / "revision_v2_2026_10_21" / "drafts"

out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)

lines = (CLONE / "main.tex").read_text().split("\n")
header = re.compile(r"^% REPLACES: main\.tex lines? (\d+)(?:[–-](\d+))?")

plans = []
for frag in sorted(DRAFTS.glob("A[0-9][0-9]_*.tex")):
    text = frag.read_text().split("\n")
    m = None
    for t in text[:5]:
        m = header.match(t)
        if m:
            break
    a = int(m.group(1))
    b = int(m.group(2) or m.group(1))
    plans.append((a, b, frag.name, text))

plans.sort(key=lambda x: x[0])
for (a1, b1, n1, _), (a2, _b2, n2, _) in zip(plans[:-1], plans[1:]):
    if a2 <= b1:
        print(f"OVERLAP: {n1} ({a1}-{b1}) and {n2} (starts {a2})")

for a, b, name, text in sorted(plans, key=lambda x: -x[0]):
    old_first = lines[a - 1][:70]
    old_last = lines[b - 1][-70:]
    print(f"{name}: lines {a}-{b}\n    first: {old_first!r}\n    last:  {old_last!r}")
    lines[a - 1:b] = text

(out / "main.tex").write_text("\n".join(lines))
for d in ("figures", "tables"):
    link = out / d
    if not link.exists():
        os.symlink(CLONE / d, link)
print(f"wrote {out / 'main.tex'}")
