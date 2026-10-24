"""Write exact pure-profile outcomes and selected interior outcomes."""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import csv
import hashlib
import json

from solver import Params, entry_bounds, posteriors, outcomes, encode
from scan import LAMBDAS, PRIORS, COSTS, STRENGTHS


def main() -> None:
    root = Path(__file__).resolve().parent
    output = root / "outcomes.csv"
    rows = 0
    with output.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("r", "lam", "pi", "c_H", "profile", "E_min", "E_max",
                         "O_H_min", "O_H_max", "R_T_min", "R_T_max"))
        for r, lam, pi, c_h in product(STRENGTHS, LAMBDAS, PRIORS, COSTS):
            p = Params(r=r, lam=lam, pi=pi, c_H=c_h)
            for beta in (F(0), F(1)):
                bounds = tuple(entry_bounds(p, m) for m in posteriors(p, beta, "IC"))
                values = [outcomes(p, beta, v, "IC") for v in product(*bounds)]
                ranges = tuple(value for key in ("E", "O_H", "R_T")
                               for value in (min(o[key] for o in values), max(o[key] for o in values)))
                writer.writerow((r, lam, pi, c_h, "N" if beta == 0 else "F") + ranges)
                rows += 1
    examples = (
        ("lower_threshold", Params(k=F(4, 27), pi=F(2, 3), c_H=F(4), lam=F(3, 5)),
         F(605, 642), (F(5, 8), F(1), F(1), F(1))),
        ("different_prices_same_posterior", Params(k=F(1, 10), c_H=F(103, 24)),
         F(1, 2), (F(1, 4), F(1, 4), F(13, 20), F(1))),
        ("top_threshold", Params(c_H=F(203, 24)),
         F(1), (F(1, 4), F(1, 4), F(1, 4), F(5, 8))),
    )
    details = []
    for name, p, beta, rates in examples:
        record = {"name": name, "parameters": vars(p), "outcome": outcomes(p, beta, rates, "IC")}
        details.append(record)
        print(json.dumps(encode(record)), flush=True)
    (root / "selected_outcomes.json").write_text(json.dumps(encode(details), indent=2) + "\n")
    info = {"status": "computer-assisted", "rows": rows,
            "scope": "Pure-profile outcomes; use the cutoffs to select equilibrium profiles.",
            "mixed_profiles": "Use the exact family constraints and outcome formulas.",
            "output_bytes": output.stat().st_size,
            "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest()}
    (root / "outcome_manifest.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info), flush=True)


if __name__ == "__main__":
    main()
