"""Failure thresholds of the reversal in c_L, for every (r1, rho), by root finding. Writes thresholds.csv.

For each (r1, rho) with c_H = 6, k = 0.02, r0 = 1.2 the reversal needs E > rho and O_H > rho/2 in every
equilibrium. Four separate mechanisms can break it; each has a threshold c_L above which it operates.

  no-trade   an equilibrium with zero orders exists (rho Delta_T <= 2k): entry equals rho at every c_L
  partial    orders (1, -v) with a half-line pool, confirmed for both types (partial.py): E <= rho or O_H <= rho/2
  knapsack E full orders and an island pool that lowers E to rho (knapsack.py, LP over all pools)
  knapsack O full orders and an island pool that lowers the high type's entry to rho
  ceiling    B_{r1}(M) < c_H: the expensive type can never enter, E <= rho

The reversal region is c_L between B(m) and the smallest of these thresholds. This script solves; render.py
reads the CSV. Every number is a numerical diagnostic; the engine confirms each minimiser's best responses.
"""
from __future__ import annotations

import csv
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from engine import make_econ
from knapsack import check_pool, min_entry, pool_intervals
from run_sweep import CH, fmt
import partial

HERE = Path(__file__).resolve().parent


def regime_II_interval(r1: float, rho: float, k: float = 0.02) -> tuple[float, float]:
    ec = make_econ(r1, rho, 1.0, CH, k=k)
    return ec.gL + ec.m * (ec.gH - ec.gL), ec.gL + 0.5 * (ec.gH - ec.gL)


def knap_value(r1: float, rho: float, c: float, k: float, objective: str) -> tuple[float, bool]:
    """LP minimum of E (or O_H) over full-order pools passing the sufficient test, and whether the engine confirms."""
    ec = make_econ(r1, rho, c, CH, k=k)
    sol = min_entry(ec, k / (1.0 - 1.0 / ec.b), objective=objective, eps=1e-6)
    if sol is None:
        return math.nan, False
    chk = check_pool(ec, pool_intervals(sol))
    val = sol["E"] if objective == "E" else sol["eH"]
    return val, bool(chk["consistent"] and chk["regret_H"] <= 1e-9 and chk["regret_L"] <= 1e-9)


def knap_threshold(r1: float, rho: float, k: float, objective: str) -> float:
    """Smallest c_L in regime II with LP minimum <= rho (E) or e_H <= rho. nan if none, B(m) if at the bottom."""
    cm, ch = regime_II_interval(r1, rho, k)
    lo, hi = cm + 1e-6, ch - 1e-6
    f = lambda c: knap_value(r1, rho, c, k, objective)[0] - rho   # noqa: E731
    flo, fhi = f(lo), f(hi)
    if math.isnan(fhi) or fhi > 0.0:
        return math.nan
    if flo <= 0.0:
        return cm
    for _ in range(36):
        mid = 0.5 * (lo + hi)
        v = f(mid)
        if math.isnan(v) or v > 0.0:
            lo = mid
        else:
            hi = mid
    return hi


def partial_columns(r1: float, rho: float, k: float) -> dict:
    """Columns from partial.hold_intervals: where the oracle (partial, window, low-trade families) finds no break."""
    h = partial.hold_intervals(r1, rho, k)
    cm = h["cm"]
    holds = h["holds"]
    bottom = bool(h["flags"][0])
    if bottom:
        mem, first = h["members"][0], cm
    elif h["first_break"] is not None:
        first, mem = h["first_break"]
    else:
        first, mem = math.nan, None
    others = [f"{a:.4f}-{b:.4f}" for a, b in holds if not (abs(a - cm) < 1e-9)]
    return {"cL_partial": first, "bottom_break": bottom, "partial_kind": mem["kind"] if mem else "",
            "partial_v": mem["v"] if mem else math.nan, "partial_x": mem["x"] if mem else math.nan,
            "partial_E": mem["E"] if mem else math.nan, "partial_OH": mem["O_H"] if mem else math.nan,
            "other_holds": ";".join(others), "grid_flags": "".join("B" if f else "." for f in h["flags"])}



def one(args: tuple) -> dict:
    r1, rho, k = args
    ec = make_econ(r1, rho, 1.0, CH, k=k)
    cm, ch = regime_II_interval(r1, rho, k)
    row = {"r1": r1, "rho": rho, "k": k, "B_m": cm, "B_half": ch, "DeltaT": ec.DeltaT,
           "no_trade": ec.DeltaT * rho <= 2 * k, "B_M": ec.gL + ec.M * (ec.gH - ec.gL),
           "ceiling": (ec.gL + ec.M * (ec.gH - ec.gL)) < CH, "tauH": ec.tauH}
    skip = row["no_trade"] or row["ceiling"]        # regime II is already empty; no need to look for a member
    if skip:
        row.update({"cL_partial": math.nan, "bottom_break": "", "partial_kind": "", "other_holds": "", "grid_flags": ""})
    else:
        try:
            row.update(partial_columns(r1, rho, k))
        except Exception as exc:                    # keep the run alive; record the failure
            row["partial_error"] = repr(exc)
    row["cL_knapE"] = knap_threshold(r1, rho, k, "E")
    row["cL_knapO"] = knap_threshold(r1, rho, k, "eH")
    finish(row)
    return row


def finish(row: dict) -> dict:
    """Combine the mechanisms into c_L* (the end of the hold interval that starts at B(m)) and name the binding one.

    no-trade and ceiling empty the whole of regime II (E = rho in the no-trade equilibrium; E <= rho when the
    expensive type can never enter), so their threshold is B(m). A nan threshold means the mechanism was not
    found, not that it is excluded. 'partial' is named by the family of the first breaking member: partial
    (grid), window (starved window) or lowtrade (small symmetric orders).
    """
    def t(x):
        return math.nan if x in ("", None) else float(x)
    bm = t(row["B_m"])
    kind = row.get("partial_kind") or "partial"
    c = {"no-trade": bm if str(row["no_trade"]).lower() == "true" else math.nan,
         "ceiling": bm if str(row["ceiling"]).lower() == "true" else math.nan,
         kind: t(row["cL_partial"]), "knapE": t(row["cL_knapE"]), "knapO": t(row["cL_knapO"]),
         "lpexact": t(row.get("cL_lpexact"))}
    order = ["no-trade", "ceiling", "lowtrade", "window", "partial", "knapE", "knapO", "lpexact"]
    live = {k_: v for k_, v in c.items() if not math.isnan(v)}
    if live:
        name = min(live, key=lambda k_: (live[k_], order.index(k_)))
        row["cL_star"], row["binding"] = live[name], name
    else:
        row["cL_star"], row["binding"] = math.nan, ""
    return row


COLS = ["r1", "rho", "k", "DeltaT", "no_trade", "ceiling", "tauH", "B_m", "B_half", "B_M", "cL_partial", "bottom_break",
        "partial_kind", "partial_v", "partial_x", "partial_E", "partial_OH", "other_holds", "grid_flags", "cL_knapE",
        "cL_knapO", "cL_lpexact", "cL_star", "binding"]


def write(rows: list[dict]) -> None:
    with (HERE / "thresholds.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: fmt(r.get(c, "")) for c in COLS})


def main(k: float = 0.02) -> None:
    jobs = [(float(r), rho, k) for rho in (0.1, 0.25, 0.5) for r in np.round(np.arange(1.5, 3.6001, 0.1), 4)]
    with Pool(4) as pool:
        rows = pool.map(one, jobs, chunksize=1)
    write(rows)
    print("thresholds.csv written", len(rows))


def _partial_row(args: tuple) -> dict:
    """Partial-order columns for one row of an existing thresholds.csv (the knapsack columns are kept)."""
    row = dict(args)
    r1, rho, k = float(row["r1"]), float(row["rho"]), float(row["k"])
    skip = str(row["no_trade"]).lower() == "true" or str(row["ceiling"]).lower() == "true"
    row.update({"cL_partial": math.nan, "bottom_break": "", "partial_kind": "", "partial_v": math.nan,
                "partial_x": math.nan, "partial_E": math.nan, "partial_OH": math.nan, "other_holds": "",
                "grid_flags": ""})
    if not skip:
        try:
            row.update(partial_columns(r1, rho, k))
        except Exception as exc:
            row["partial_error"] = repr(exc)
    return row


def mergelp() -> None:
    """Add the exact-LP island threshold (lp_thresholds.csv, written by lp_refine.py) and recompute c_L* and the binding family."""
    with (HERE / "thresholds.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    with (HERE / "lp_thresholds.csv").open() as fh:
        lp = {(round(float(r["r1"]), 4), round(float(r["rho"]), 6)): r["cL_lpexact"] for r in csv.DictReader(fh)}
    for r in rows:
        r["cL_lpexact"] = lp.get((round(float(r["r1"]), 4), round(float(r["rho"]), 6)), "")
    write([finish(r) for r in rows])
    print("thresholds.csv merged with lp_thresholds.csv", len(rows))


def repartial() -> None:
    """Recompute only the partial-order columns of thresholds.csv (knapsack columns are kept), then finish."""
    with (HERE / "thresholds.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    with Pool(4) as pool:
        out = pool.map(_partial_row, [tuple(r.items()) for r in rows], chunksize=1)
    write([finish(r) for r in out])
    print("thresholds.csv partial columns recomputed", len(out))


def refinish() -> None:
    """Recompute c_L* and the binding mechanism from the columns already in thresholds.csv (no solving)."""
    with (HERE / "thresholds.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    write([finish(r) for r in rows])
    print("thresholds.csv refinished", len(rows))


if __name__ == "__main__":
    if "--finish" in sys.argv:
        refinish()
    elif "--merge-lp" in sys.argv:
        mergelp()
    elif "--partial-only" in sys.argv:
        repartial()
    else:
        main(float(sys.argv[1]) if len(sys.argv) > 1 else 0.02)
