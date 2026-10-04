"""Run the independent quadrature check (verify.py) on every row of an equilibrium CSV.

  python3 verify_csv.py eq_r3_rho0.25.csv          writes eq_r3_rho0.25_verified.csv
  python3 verify_csv.py eq_region.csv --every 5     checks every 5th row plus every extreme row

A row is accepted only when verify.verify() accepts it at tolerance 1e-8. The output keeps every input
column and adds the verifier's numbers. Rows that fail stay in the file with accepted = false.
"""
from __future__ import annotations

import csv
import json
import math
import sys
from multiprocessing import Pool
from pathlib import Path

from verify import Case, verify

HERE = Path(__file__).resolve().parent
TOL = 1e-8


def _f(s: str) -> float:
    return float(s)


def _pool_from_json(text: str) -> tuple[tuple[float, float], ...]:
    """Pool as a JSON list of [lo, hi] pairs; the strings "-inf" and "inf" mark the open ends."""
    out = []
    for a, b in json.loads(text):
        out.append((-math.inf if a == "-inf" else float(a), math.inf if b == "inf" else float(b)))
    return tuple(out)


def case_of(row: dict) -> Case:
    if row.get("pool"):
        pool = _pool_from_json(row["pool"])             # arbitrary pool (island minimisers of the pool LP)
    else:
        cutoff = _f(row["cutoff"])
        pool = () if not math.isfinite(cutoff) else ((-math.inf, cutoff),)
    return Case(h=10.0, ell=1.0, p=0.5, b=2.0, k=0.02, r=_f(row["r"]), rho=_f(row["rho"]), cL=_f(row["cL"]),
                cH=_f(row["cH"]), H=((_f(row["qH"]), 1.0),), L=((_f(row["qL"]), 1.0),), pool=pool)


def check(row: dict) -> dict:
    v = verify(case_of(row), tol=TOL)
    return {"ver_accepted": v.accepted, "ver_pool_consistent": v.pool_consistent, "ver_regret_H": v.regret_H,
            "ver_regret_L": v.regret_L, "ver_wrong_sign_max": v.wrong_sign_max, "ver_E": v.E, "ver_O_H": v.O_H,
            "ver_pool_belief": v.pool_belief,
            "ver_dE": abs(v.E - _f(row["E"])), "ver_dOH": abs(v.O_H - _f(row["O_H"]))}


def main(path: Path, every: int = 1) -> None:
    with path.open() as fh:
        rows = list(csv.DictReader(fh))
    todo = []
    for i, row in enumerate(rows):
        if every == 1 or i % every == 0:
            todo.append(i)
    # always check the extreme rows of each parameter point (lowest E and lowest O_H)
    if every != 1:
        groups: dict[tuple, list[int]] = {}
        for i, row in enumerate(rows):
            groups.setdefault((row["r"], row["rho"], row["cL"]), []).append(i)
        for idx in groups.values():
            todo.append(min(idx, key=lambda j: _f(rows[j]["E"])))
            todo.append(min(idx, key=lambda j: _f(rows[j]["O_H"])))
        todo = sorted(set(todo))
    with Pool(4) as pool:
        res = pool.map(check, [rows[i] for i in todo], chunksize=4)
    out = []
    done = dict(zip(todo, res))
    for i, row in enumerate(rows):
        extra = done.get(i, {"ver_accepted": "unchecked"})
        out.append({**row, **extra})
    cols = list(rows[0].keys()) + ["ver_accepted", "ver_pool_consistent", "ver_regret_H", "ver_regret_L",
                                   "ver_wrong_sign_max", "ver_E", "ver_O_H", "ver_pool_belief", "ver_dE", "ver_dOH"]
    dst = path.with_name(path.stem + "_verified.csv")
    with dst.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in out:
            w.writerow({c: (("true" if row[c] else "false") if isinstance(row.get(c), bool) else row.get(c, ""))
                        for c in cols})
    acc = sum(1 for r in done.values() if r["ver_accepted"] is True)
    print(f"{path.name}: checked {len(done)} of {len(rows)} rows, accepted {acc}, rejected {len(done) - acc}")
    bad = [rows[i] for i, r in done.items() if r["ver_accepted"] is not True]
    for row in bad[:10]:
        print("  rejected:", {k: row[k] for k in ("r", "rho", "cL", "family", "cutoff", "qH", "qL")})
    if res:
        print(f"  max |E - E_ver| = {max(r['ver_dE'] for r in res):.2e}, max |O_H - O_H_ver| = {max(r['ver_dOH'] for r in res):.2e}, "
              f"max regret = {max(max(r['ver_regret_H'], r['ver_regret_L']) for r in res):.2e}")


if __name__ == "__main__":
    p = HERE / sys.argv[1]
    ev = 1
    if "--every" in sys.argv:
        ev = int(sys.argv[sys.argv.index("--every") + 1])
    main(p, ev)
