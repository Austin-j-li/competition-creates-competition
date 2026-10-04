"""Mixed-profile diagnostics at r1 = 3, rho = 0.25. Writes mixed_audit.csv and mixed_bridge.csv.

(1) audit(): local maxima of each type's payoff over random consistent schedules (pure and mixed, half-line and
    island pools). (2) bridge_mixture(): wherever the cutoff scan finds two pure equilibria at the same pool that
    differ in the L order, build the mixed equilibrium that connects them. (3) mixed_search(): lattice two-atom
    mixtures for one type with the other pure, at a few pools.
"""
from __future__ import annotations

import csv
import math
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import make_econ
from mixed import audit, bridge_mixture, mixed_search
from run_sweep import CH, fmt
from scan import scan_point

HERE = Path(__file__).resolve().parent


def audit_job(cL: float) -> dict:
    ec = make_econ(3.0, 0.25, cL, CH)
    return {"cL": cL, **audit(ec, n=1500, seed=1)}


def bridge_job(cL: float) -> list[dict]:
    ec = make_econ(3.0, 0.25, cL, CH)
    res = scan_point(ec, step=0.05)
    by_cut: dict[float, list] = {}
    for c in res.members:
        by_cut.setdefault(round(c.pool_end, 6), []).append(c)
    rows = []
    for end, cs in sorted(by_cut.items()):
        cs = sorted(cs, key=lambda c: c.qL)
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                a, b = cs[i], cs[j]
                if abs(a.qH - b.qH) > 1e-6:
                    continue
                cut = None if not math.isfinite(a.cutoff) else a.cutoff
                m = bridge_mixture(ec, cut, (a.qH, a.qL), (b.qH, b.qL))
                if m is not None:
                    rows.append({"cL": cL, "pool_end": end, "cutoff": a.cutoff, **m})
    return rows


def pool_of(spec) -> tuple[tuple[float, float], ...]:
    """spec: None (minimal pool), a cutoff x (half-line (-inf, x)), or a tuple of (lo, hi) pairs."""
    if spec is None:
        return ()
    if isinstance(spec, tuple):
        return spec
    return ((-math.inf, float(spec)),)


def search_job(args: tuple) -> list[dict]:
    cL, spec, who = args
    ec = make_econ(3.0, 0.25, cL, CH)
    return [{"cL": cL, "pool": str(spec), **r} for r in mixed_search(ec, pool_of(spec), who, lattice=11)]


def write(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("empty\n")
        return
    cols = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: fmt(r.get(c, "")) for c in cols})


if __name__ == "__main__":
    cls = [2.40, 2.50, 2.60, 2.70, 2.80, 2.90, 2.95, 2.98, 3.0, 3.5, 4.0]
    with Pool(4) as pool:
        a = pool.map(audit_job, cls)
        write(HERE / "mixed_audit.csv", a)
        print("audit done")
        b = [r for rs in pool.map(bridge_job, [2.50, 2.70, 2.90, 2.98, 3.0, 3.2, 3.5, 4.0, 4.2]) for r in rs]
        write(HERE / "mixed_bridge.csv", b)
        print("bridge done", len(b))
        pools = [None, 0.3, 0.6, 1.0, -0.5, ((-math.inf, 0.0), (1.0, 1.5)), ((-math.inf, -0.5), (0.5, 1.2))]
        jobs = [(c, spec, who) for c in (2.5, 2.7, 2.9, 2.98, 3.5) for spec in pools for who in ("L", "H")]
        s = [r for rs in pool.map(search_job, jobs) for r in rs]
        write(HERE / "mixed_search.csv", s)
        print("search done", len(s), "pools tested", len(jobs))
