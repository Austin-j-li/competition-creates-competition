"""Island thresholds from the exact pool LP: where does an all-pool equilibrium first break the reversal?

Reads lp_summary_region.csv (12 values of c_L per (r1, rho), from lp_map.py region). A grid point has a confirmed break
when the polished LP minimiser is an exact fixed point of the engine and its E is at most E(r0), or its O_H at most
O_H(r0). For every (r1, rho) with a confirmed break the first such grid point is refined by bisection on c_L (the LP is
solved again at each step). Writes lp_thresholds.csv: r1, rho, cL_lpexact (nan if none), the E and O_H at the break,
and the orders. Numerical diagnostic: the LP lattice is coarse (q_H in {1, .7, .4}, q_L in steps of 0.1).
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

from lp_map import solve_point
from run_sweep import fmt

HERE = Path(__file__).resolve().parent


def num(x: str) -> float:
    return math.nan if x in ("", "nan") else float(x)


def broken(summ: dict) -> tuple[bool, float, float, float, float, str]:
    """(confirmed break, E, O_H, qH, qL, pool as JSON) from one solve_point summary."""
    ew, ow = summ["E_weak"], summ["OH_weak"]
    for tag in ("E", "OH"):
        if summ.get(f"polished_{tag}") and (summ[f"E_polished_{tag}"] <= ew + 1e-9 or summ[f"OH_polished_{tag}"] <= ow + 1e-9):
            return (True, summ[f"E_polished_{tag}"], summ[f"OH_polished_{tag}"], summ[f"qH_polished_{tag}"],
                    summ[f"qL_polished_{tag}"], summ[f"pool_{tag}"])
    return False, math.nan, math.nan, math.nan, math.nan, ""


def job(args: tuple) -> dict:
    r1, rho, lo, hi = args                    # lo: last grid point without a confirmed break; hi: first with one
    _, s, _ = solve_point((r1, rho, hi, None, True))
    best = broken(s)
    for _ in range(9):
        mid = 0.5 * (lo + hi)
        _, s, _ = solve_point((r1, rho, mid, None, True))
        b = broken(s)
        if b[0]:
            hi, best = mid, b
        else:
            lo = mid
    return {"r1": r1, "rho": rho, "cL_lpexact": hi, "E": best[1], "O_H": best[2], "qH": best[3], "qL": best[4],
            "pool": best[5]}


if __name__ == "__main__":
    with (HERE / "lp_summary_region.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    pairs: dict[tuple[float, float], list[float]] = {}
    for r in rows:
        pairs.setdefault((num(r["r"]), num(r["rho"])), []).append(num(r["cL"]))
    # the first confirmed break is found from the stored summaries; only the bracket is re-solved
    jobs = []
    for (r1, rho), cs in sorted(pairs.items()):
        cs = sorted(cs)
        first = None
        for c in cs:
            row = next(x for x in rows if num(x["r"]) == r1 and num(x["rho"]) == rho and abs(num(x["cL"]) - c) < 1e-12)
            ew, ow = num(row["E_weak"]), num(row["OH_weak"])
            hit = (row["polished_E"] == "true" and (num(row["E_polished_E"]) <= ew + 1e-9 or num(row["OH_polished_E"]) <= ow + 1e-9)) or \
                  (row["polished_OH"] == "true" and (num(row["E_polished_OH"]) <= ew + 1e-9 or num(row["OH_polished_OH"]) <= ow + 1e-9))
            if hit:
                first = c
                break
        if first is not None:
            prev = [c for c in cs if c < first]
            jobs.append((r1, rho, prev[-1] if prev else cs[0] - 0.05, first))
    with Pool(4) as p:
        out = p.map(job, jobs, chunksize=1)
    allrows = [{"r1": r1, "rho": rho, "cL_lpexact": math.nan, "E": math.nan, "O_H": math.nan, "qH": math.nan, "qL": math.nan,
                "pool": ""} for (r1, rho) in sorted(pairs)]
    for o in out:
        for a in allrows:
            if a["r1"] == o["r1"] and a["rho"] == o["rho"]:
                a.update(o)
    cols = ["r1", "rho", "cL_lpexact", "E", "O_H", "qH", "qL", "pool"]
    with (HERE / "lp_thresholds.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in allrows:
            w.writerow({c: fmt(r[c]) for c in cols})
    # the same breaks as equilibrium rows, for verify_csv.py (independent quadrature)
    ecols = ["r", "rho", "cL", "cH", "regime", "family", "cutoff", "pool", "qH", "qL", "E", "O_H", "which"]
    with (HERE / "lp_threshold_members.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ecols)
        w.writeheader()
        for r in allrows:
            if not math.isnan(r["cL_lpexact"]):
                w.writerow({"r": fmt(r["r1"]), "rho": fmt(r["rho"]), "cL": fmt(r["cL_lpexact"]), "cH": 6.0, "regime": "II",
                            "family": "lp-pool", "cutoff": "", "pool": r["pool"], "qH": fmt(r["qH"]), "qL": fmt(r["qL"]),
                            "E": fmt(r["E"]), "O_H": fmt(r["O_H"]), "which": "exact LP first break"})
    print("lp_thresholds.csv", len(allrows), "with a break:", len(out))
