"""Test of the adversary's high-rho claim: at the floor of regime II the largest entry E_0 is below rho
once rho >= a / (a + pi_0) = 0.5154 (r1 = 3, k = 0.02, c_H = 6). Scans c_L just above B(m) and two more values.
The engine finds every pure-order equilibrium on the cutoff family and the E range it reaches. Writes rho_check.csv.
Status of every row: numerical diagnostic.
"""
from __future__ import annotations

import csv
from multiprocessing import Pool
from pathlib import Path

from engine import make_econ
from run_sweep import CH, R0, fmt
from scan import regime_of, row_of, scan_point

HERE = Path(__file__).resolve().parent


def job(args: tuple) -> dict:
    rho, off = args
    ec0 = make_econ(3.0, rho, 1.0, CH)
    cm = ec0.gL + ec0.m * (ec0.gH - ec0.gL)
    cL = cm + off
    ec = make_econ(3.0, rho, cL, CH)
    ecw = make_econ(R0, rho, cL, CH)
    res = scan_point(ec, step=0.05)
    rows = [row_of(ec, c, ecw) for c in res.members]
    if not rows:
        return {"rho": rho, "cL": cL, "n_eq": 0}
    return {"rho": rho, "cL": cL, "regime": regime_of(ec), "n_eq": len(rows),
            "E_min": min(x["E"] for x in rows), "E_max": max(x["E"] for x in rows),
            "OH_min": min(x["O_H"] for x in rows), "OH_max": max(x["O_H"] for x in rows),
            "E_gt_rho_all": all(x["E_gt_weak"] for x in rows), "E_gt_rho_any": any(x["E_gt_weak"] for x in rows),
            "OH_gt_all": all(x["OH_gt_weak"] for x in rows), "reversal_all": all(x["reversal"] for x in rows),
            "reversal_any": any(x["reversal"] for x in rows), "unresolved": res.unresolved}


if __name__ == "__main__":
    jobs = [(rho, off) for rho in (0.45, 0.5, 0.51, 0.5154, 0.52, 0.55, 0.6, 0.75) for off in (1e-4, 0.05, 0.3)]
    with Pool(4) as p:
        out = p.map(job, jobs, chunksize=1)
    cols = ["rho", "cL", "regime", "n_eq", "E_min", "E_max", "OH_min", "OH_max", "E_gt_rho_all", "E_gt_rho_any",
            "OH_gt_all", "reversal_all", "reversal_any", "unresolved"]
    with (HERE / "rho_check.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in out:
            w.writerow({c: fmt(r.get(c, "")) for c in cols})
    print("rho_check.csv", len(out))
