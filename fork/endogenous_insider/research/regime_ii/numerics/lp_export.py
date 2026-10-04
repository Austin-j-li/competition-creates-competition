"""Turn the pool-LP minimisers into an equilibrium CSV that verify_csv.py can check by independent quadrature.

Reads lp_summary_r3_rho0.25.csv (written by lp_map.py). For each c_L and each objective (lowest E, lowest O_H) whose
polished profile is an exact fixed point of the engine, one row is written with the full pool as JSON.
Writes lp_polished.csv. Rows whose polish did not converge are not exported; they stay "open" in the LP summary.
"""
from __future__ import annotations

import csv
from pathlib import Path

from run_sweep import CH

HERE = Path(__file__).resolve().parent

COLS = ["r", "rho", "cL", "cH", "regime", "family", "cutoff", "pool", "qH", "qL", "E", "O_H", "which"]


def main() -> None:
    with (HERE / "lp_summary_r3_rho0.25.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        for tag in ("E", "OH"):
            if r.get(f"polished_{tag}") == "true":
                out.append({"r": r["r"], "rho": r["rho"], "cL": r["cL"], "cH": CH, "regime": r["regime"],
                            "family": "lp-pool", "cutoff": "", "pool": r[f"pool_{tag}"],
                            "qH": r[f"qH_polished_{tag}"], "qL": r[f"qL_polished_{tag}"],
                            "E": r[f"E_polished_{tag}"], "O_H": r[f"OH_polished_{tag}"], "which": tag})
    with (HERE / "lp_polished.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    print("lp_polished.csv", len(out))


if __name__ == "__main__":
    main()
