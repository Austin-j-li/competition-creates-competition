#!/usr/bin/env python
"""Compare the C9 summary.csv (read as data) with values from check_c9.py.

Print-only. Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C9_check/compare_author.py
"""

import csv
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_c9 import BENCH, NOISE_C9, enumerate_eq  # noqa: E402

CSV = HERE.parent / "C9_unequal_mixing" / "summary.csv"
KIND = {"no_trade": "no trade", "both_indifferent": "threshold mixture",
        "rising_entry": "interior mixture", "gap_completion": "threshold mixture"}

rows = list(csv.DictReader(CSV.open()))
mismatch = 0
for row in rows:
    par = dict(BENCH, k=F(row["k"]), cH=F(row["c_H"]), lam=F(row["lambda"]))
    noise = {-1: F(row["z_minus"]), 0: F(row["z_zero"]), 1: F(row["z_plus"])}
    A, res, err = enumerate_eq(par, noise, F(row["r"]))
    mine = {rec["kind"]: rec["prof"] for rec in res}
    P = mine.get(KIND[row["case"]])
    if P is None:
        print(f"{row['case']} r={row['r']} lambda={row['lambda']}: no matching outcome")
        mismatch += 1
        continue
    rho = par["rho"]
    vals = {"beta_H": P["beta"], "alpha": P["alpha"],
            "sigma_at_flow_1": (P["e"][1] - rho) / (1 - rho),
            "Delta_T": A["D"], "tau": A["tau"], "U_H_buy": P["UH1"], "U_L_buy": P["UL1"],
            "E": P["E"], "O_H": P["OH"]}
    bad = [key for key, val in vals.items() if F(row[key]) != val]
    mismatch += len(bad)
    print(f"{row['case']:>16} r={row['r']:>7} lambda={row['lambda']:>5}: "
          f"{len(vals) - len(bad)}/{len(vals)} fields equal" + (f"; differ: {bad}" if bad else ""))
print(f"rows {len(rows)}, differing fields {mismatch}")
