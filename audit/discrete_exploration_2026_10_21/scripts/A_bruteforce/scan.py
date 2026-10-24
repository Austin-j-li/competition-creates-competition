"""Enumerate exact parameter cells and save compact grid summaries."""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import Counter
from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction as F
import csv
import hashlib
import json
from pathlib import Path
import platform
import time

from solver import Params, auction, entry_bounds, solve, rate_vertices, witness, outcomes, encode, family_record


ROOT = Path(__file__).resolve().parent
LAMBDAS = (F(1), F(19, 20), F(9, 10), F(4, 5), F(3, 5), F(2, 5), F(1, 5))
PRIORS = (F(1, 2), F(1, 3), F(2, 3))
COSTS = tuple(F(n) for n in range(4, 9))
STRENGTHS = tuple(F(n, 20) for n in range(21, 191))
TRADE_COSTS = tuple(sorted({F(n, 1000) for n in range(1, 501)}
                          | {F(n, 100) for n in range(51, 301)}))
FLAGS = ("cases", "none", "unique", "multiple", "investor_continuum",
         "onpath_entry_continuum", "offpath_continuum", "both_N_F")


def classify(p: Params, belief: str, tie: str) -> tuple[str, ...]:
    families = solve(p, belief, tie)
    if not families:
        return ("cases", "none")
    flags = ["cases"]
    supports = {f.support for f in families}
    if any(f.beta_lo < f.beta_hi for f in families):
        flags.append("investor_continuum")
    if {"N", "F"} <= supports:
        flags.append("both_N_F")
    onpath, offpath = False, False
    for family in families:
        if not any(lo < hi for lo, hi in family.rates):
            continue
        vertices = rate_vertices(family)
        beta, rates = witness(family)
        mass = outcomes(p, beta, rates, belief)["flow_mass"]
        for index in range(4):
            distinct = len({v[index] for v in vertices}) > 1
            if distinct and mass[index] > 0:
                onpath = True
            if distinct and mass[index] == 0:
                offpath = True
    if onpath:
        flags.append("onpath_entry_continuum")
    if offpath:
        flags.append("offpath_continuum")
    flags.append("multiple" if len(flags) > 1 or len(families) > 1 else "unique")
    return tuple(flags)


def cost_cells(cuts: tuple[F, ...]):
    previous = F(0)
    for current in cuts:
        if current > previous:
            count = bisect_left(TRADE_COSTS, current) - bisect_right(TRADE_COSTS, previous)
            yield (previous + current) / 2, count, 0
        on_grid = current in TRADE_COSTS
        yield current, int(on_grid), int(not on_grid)
        previous = current
    count = len(TRADE_COSTS) - bisect_right(TRADE_COSTS, previous)
    yield previous + 1, count, 0


def save_examples() -> None:
    cases = (
        ("benchmark", Params()),
        ("investor_cutoff", Params(k=F(1, 18))),
        ("passive_gap", Params(r=F(9, 5))),
        ("lower_flow_tie", Params(k=F(4, 27), pi=F(2, 3), c_H=F(4), lam=F(3, 5))),
        ("full_order_lower_flow_tie", Params(pi=F(2, 3), c_H=F(4), lam=F(121, 214))),
        ("prior_tie", Params(k=F(1, 10), c_H=F(103, 24))),
        ("top_flow_tie", Params(c_H=F(203, 24))),
    )
    records = []
    for name, p in cases:
        for belief in ("IC", "passive"):
            for tie in ("zero", "any"):
                records.append({"name": name, "parameters": vars(p), "belief": belief,
                                "investor_tie": tie,
                                "families": [family_record(p, f, belief) for f in solve(p, belief, tie)]})
    (ROOT / "boundary_examples.json").write_text(json.dumps(encode(records), indent=2) + "\n")


def save_benchmark() -> None:
    with (ROOT / "benchmark.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("r", "lam", "pi", "c_H", "k", "belief", "investor_tie",
                         "support", "beta_H", "E", "O_H", "R_T"))
        for r in (F(6, 5), F(3), F(18, 5)):
            for lam in LAMBDAS:
                p = Params(r=r, lam=lam)
                for belief in ("IC", "passive"):
                    for tie in ("zero", "any"):
                        for family in solve(p, belief, tie):
                            beta, rates = witness(family)
                            out = outcomes(p, beta, rates, belief)
                            writer.writerow((r, lam, p.pi, p.c_H, p.k, belief, tie,
                                             family.support, beta, out["E"], out["O_H"], out["R_T"]))


def main() -> None:
    started = time.monotonic()
    totals: dict[tuple, Counter] = {}
    sign_counts = Counter()
    diagnostics = Counter()
    with (ROOT / "cutoffs.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("r", "pi", "c_H", "Delta_T", "B_prior", "g_H", "tau",
                         "K_min", "K_max", "N_passive_min", "N_passive_max",
                         "lambda_beta_lower_tie", "prior_status", "top_status"))
        for r in STRENGTHS:
            for pi in PRIORS:
                for c_h in COSTS:
                    p0 = Params(r=r, pi=pi, c_H=c_h)
                    a = auction(p0)
                    prior = a.gl + pi * (a.gh - a.gl)
                    tau = (c_h - a.gl) / (a.gh - a.gl)
                    e_low, e_high = entry_bounds(p0, pi)
                    factor = 2 * a.delta * (1 - pi) / 3
                    k_low, k_high = factor * e_low, factor * e_high
                    n_low, n_high = 3 * k_low / 2, 3 * k_high / 2
                    root = (pi - tau) / (pi * (1 - tau)) if tau != 1 else "undefined"
                    prior_status = "below" if prior < c_h else "above" if prior > c_h else "equal"
                    top_status = "below" if a.gh < c_h else "above" if a.gh > c_h else "equal"
                    sign_counts[(prior_status, top_status)] += 1
                    writer.writerow((r, pi, c_h, a.delta, prior, a.gh, tau, k_low, k_high,
                                     n_low, n_high, root, prior_status, top_status))
                    cuts = tuple(sorted({k_low, k_high, n_low, n_high}))
                    for lam in LAMBDAS:
                        for k, base_count, added_count in cost_cells(cuts):
                            if not (base_count or added_count):
                                continue
                            p = replace(p0, lam=lam, k=k)
                            for belief in ("IC", "passive"):
                                for tie in ("zero", "any"):
                                    flags = classify(p, belief, tie)
                                    for grid, count in (("base", base_count), ("boundary", added_count)):
                                        if count:
                                            key = (lam, pi, c_h, belief, tie, grid)
                                            tally = totals.setdefault(key, Counter())
                                            for flag in flags:
                                                tally[flag] += count
                            diagnostics["cost_cells"] += 1
            if r.numerator % 10 == 0:
                print(f"Completed r={r}; elapsed={time.monotonic() - started:.1f}s", flush=True)
    with (ROOT / "summary.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("lam", "pi", "c_H", "belief", "investor_tie", "grid") + FLAGS)
        for key, value in sorted(totals.items()):
            writer.writerow(key + tuple(value[flag] for flag in FLAGS))
    aggregate: dict[tuple, Counter] = {}
    for (_, _, _, belief, tie, grid), value in totals.items():
        aggregate.setdefault((belief, tie, grid), Counter()).update(value)
    with (ROOT / "aggregate.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("belief", "investor_tie", "grid") + FLAGS)
        for key, value in sorted(aggregate.items()):
            row = key + tuple(value[flag] for flag in FLAGS)
            writer.writerow(row)
            print(row, flush=True)
    save_examples()
    save_benchmark()
    output_names = ("solver.py", "scan.py", "cutoffs.csv", "summary.csv", "aggregate.csv",
                    "boundary_examples.json", "benchmark.csv")
    manifest = {"date_utc": datetime.now(timezone.utc).isoformat(),
                "paper_commit": "9b9bf3ce1a94d5017042192e61c9ceb800d310ba",
                "status": "computer-assisted", "arithmetic": "exact rational",
                "python": platform.python_version(), "elapsed_seconds": time.monotonic() - started,
                "r_grid": "n/20 for n=21,...,190",
                "k_grid": "n/1000 for n=1,...,500; n/100 for n=51,...,300",
                "extra_k": "all positive K_min, K_max, N_passive_min, N_passive_max",
                "lambda": LAMBDAS, "prior": PRIORS, "c_H": COSTS,
                "fixed": {"h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(1, 4), "c_L": F(0)},
                "base_economic_points": len(STRENGTHS) * len(TRADE_COSTS) * 105,
                "method": "Enumerate rational support cells; count grid intersections exactly.",
                "prior_top_status_counts": {"/".join(k): v for k, v in sign_counts.items()},
                "diagnostics": dict(diagnostics),
                "files": {name: {"bytes": (ROOT / name).stat().st_size,
                                  "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}
                          for name in output_names}}
    (ROOT / "manifest.json").write_text(json.dumps(encode(manifest), indent=2) + "\n")
    print(f"Finished in {time.monotonic() - started:.1f}s", flush=True)


if __name__ == "__main__":
    main()
