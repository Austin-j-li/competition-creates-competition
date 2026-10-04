"""Exact entry and O_H at the weak strength r0 = 6/5, in rational arithmetic (item 3 of the task).

At r0 the investor's gross advantage per unit is at most Delta_T(r0) = 1/60 < k = 1/50, so zero orders are
the unique best response to every schedule (paper, proof of Proposition 2, step 3). Then X = Z, the
posterior is 1/2, the price is constant, and entry is G(B_r0(1/2)) = rho when c_L <= B_r0(1/2) < c_H.
Writes weak_r0.csv. The solver for r1 never reads this file; render.py and the note do.
"""
from __future__ import annotations

import csv
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent


def weak_values(r: Fr, h: Fr = Fr(10), ell: Fr = Fr(1), p: Fr = Fr(1, 2)) -> dict:
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - tH
    gL = (ell * ell - p * p) / (2 * r)
    return {"t0": t0, "tH": tH, "tL": tL, "gH": gH, "gL": gL, "DeltaT": tH - tL, "B_half": (gL + gH) / 2}


def main() -> None:
    r0 = Fr(6, 5)
    k = Fr(1, 50)
    v = weak_values(r0)
    cH = Fr(6)
    rows = []
    for rho in (Fr(1, 10), Fr(1, 4), Fr(1, 2)):
        for cL in (Fr(1), Fr(5, 2), Fr(3), Fr(7, 2), Fr(4), Fr(17, 4)):
            e = rho * (cL <= v["B_half"]) + (1 - rho) * (cH <= v["B_half"])
            rows.append({"r0": str(r0), "rho": str(rho), "cL": str(cL), "cH": str(cH),
                         "B_r0_half": str(v["B_half"]), "B_r0_half_dec": f"{float(v['B_half']):.6f}",
                         "DeltaT_r0": str(v["DeltaT"]), "k": str(k), "no_trade_unique": v["DeltaT"] < k,
                         "E_r0": str(e), "E_r0_dec": f"{float(e):.6f}", "OH_r0": str(e / 2),
                         "OH_r0_dec": f"{float(e / 2):.6f}"})
    with (HERE / "weak_r0.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow(row)
    print({k_: str(x) for k_, x in v.items()})
    print("rows", len(rows))


if __name__ == "__main__":
    main()
