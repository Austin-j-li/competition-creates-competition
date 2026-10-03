"""Re-run the interval certificates in memory (no file written by certify.py) and compare with certificates.csv."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import certify  # noqa: E402

with (HERE.parent / "certificates.csv").open() as fh:
    stored = {row["law"]: row for row in csv.DictReader(fh)}
for law in certify.LAWS:
    row = certify.certify_law(*law)
    s = stored[row["law"]]
    print(row["law"], row["regime"], f"{row['J_lower_bound']:.10g}", s["J_lower_bound"],
          f"{row['existence_margin_lower']:.10g}", s["existence_margin_lower"], row["status"], flush=True)
