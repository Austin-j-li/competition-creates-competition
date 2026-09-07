"""Figure for the endogenous-insider fork: total entry against incumbent strength, and the cutoff family.

The fork is the benchmark model with the low-cost preparation floor removed, so preparation costs the
deterministic c of `solve.py`. This module renders; it reads the solver's CSVs and the validated
benchmark correspondence, and it never solves, never changes a parameter, and never drops a branch.
Lines break at grid gaps and at jumps, so no segment implies a node that was not searched.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from numerics.io import read_csv  # noqa: E402
from numerics.render.style import (DASHED, DOTTED, FULL_WIDTH, GRAY, INK, MUTED, NAVY, RUST, SOLID,  # noqa: E402
                                   TINT_A, TINT_B, label_line, panel_label, plt, region_label)

FORK = "fork/endogenous_insider"
GAP = 0.06   # adjacent searched strengths further apart than this are not connected
JUMP = 0.02  # a larger change in entry between adjacent nodes is a jump, not a segment


def _broken(points: list[tuple[float, float]], gap: float = GAP,
            jump: float = JUMP) -> tuple[np.ndarray, np.ndarray]:
    """Connect only adjacent searched nodes: insert a gap wherever the grid or the value jumps."""
    pts = sorted(points)
    xs: list[float] = []
    ys: list[float] = []
    for i, (x, y) in enumerate(pts):
        if i and (x - pts[i - 1][0] > gap or abs(y - pts[i - 1][1]) > jump):
            xs.append(np.nan)
            ys.append(np.nan)
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def _fork_branch(rows: list[dict], branch: str) -> list[tuple[float, float]]:
    """(r, E) for one fork branch where the solver reports the equilibrium to exist."""
    return [(float(r["r"]), float(r["E"])) for r in rows
            if r["branch"] == branch and r["exists"].strip().lower() == "true"]


def _benchmark_branch(rows: list[dict], branch: str) -> list[tuple[float, float]]:
    """(r, E) for one accepted benchmark branch; unaccepted rows of Figure 2 are never plotted."""
    return [(float(r["r"]), float(r["E"])) for r in rows
            if r["branch"] == branch and r["accepted"].strip().lower() == "true"]


def _at(points: list[tuple[float, float]], x0: float) -> tuple[float, float]:
    """The plotted point nearest x0, used to anchor a direct label on a line."""
    return min(sorted(points), key=lambda p: abs(p[0] - x0))


def _panel_a(ax, branches: list[dict], benchmark: list[dict], th: dict[str, float]) -> None:
    rmin, rmax = 1.0, 3.8
    r_k, r_c = th["trading_impossible_sufficient"], th["preparation_ceiling"]
    ax.axvspan(rmin, r_k, color=TINT_A, lw=0, zorder=0)
    ax.axvspan(r_c, rmax, color=TINT_B, lw=0, zorder=0)
    for value in (r_k, r_c):
        ax.axvline(value, color=MUTED, lw=0.7, ls=DOTTED, zorder=1)

    # benchmark with the cost floor, for comparison only, in one visual key
    for branch in ("full_orders", "pooling", "asymmetric"):
        pts = _benchmark_branch(benchmark, branch)
        if pts:
            ax.plot(*_broken(pts), color=GRAY, ls=DASHED, lw=1.2, zorder=2)

    dead = _fork_branch(branches, "dead")
    live = _fork_branch(branches, "live")
    ax.plot(*_broken(dead), color=NAVY, ls=SOLID, lw=1.6, zorder=3)
    ax.plot(*_broken(live), color=RUST, ls=SOLID, lw=1.6, zorder=4)
    ax.scatter([x for x, _ in live], [y for _, y in live], s=3, color=RUST, zorder=4)

    # threshold names on a secondary top axis, never inside the data area
    top = ax.secondary_xaxis("top")
    top.set_xticks([r_k, r_c])
    top.set_xticklabels(["trading impossible\n" + r"$r(k)$", "preparation ceiling\n" + r"$r_C$"], fontsize=8)
    top.tick_params(length=3, color=MUTED)
    top.spines["top"].set_visible(False)

    label_line(ax, *_at(live, 2.62), "live: informed orders, entry", RUST, dx=0, dy=7, ha="center")
    label_line(ax, *_at(dead, 2.20), "dead: no trade, no entry", NAVY, dx=0, dy=6, ha="center")
    label_line(ax, *_at(_benchmark_branch(benchmark, "full_orders"), 2.30),
               "benchmark with cost floor (paper, Fig. 2)", GRAY, dx=0, dy=8, ha="center")

    ax.set_xlim(rmin, rmax)
    ax.set_ylim(-0.03, 0.62)
    ax.set_yticks([0.0, 0.15, 0.3, 0.45, 0.6])
    ax.set_xlabel(r"incumbent strength $r$")
    ax.set_ylabel(r"total entry $\mathsf{E}$")
    # the shaded bands are narrow: nudge each label away from its dotted boundary
    region_label(ax, (rmin + r_k) / 2 - 0.025, "dead\nunique", y_frac=0.24)
    region_label(ax, (r_c + rmax) / 2 + 0.010, "dead\nunique", y_frac=0.24)


def _panel_b(ax, family: list[dict]) -> None:
    live = [(float(r["cutoff"]), float(r["E"])) for r in family
            if r["live"].strip().lower() == "true" and np.isfinite(float(r["E"]))]
    dead = [(float(r["cutoff"]), float(r["E"])) for r in family
            if r["live"].strip().lower() != "true" and np.isfinite(float(r["E"]))]
    ax.plot(*_broken(live, jump=np.inf), color=RUST, ls=SOLID, lw=1.6, zorder=3)
    ax.scatter([x for x, _ in live], [y for _, y in live], s=3, color=RUST, zorder=3)
    if dead:
        ax.plot(*_broken(dead, jump=np.inf), color=NAVY, ls=SOLID, lw=1.6, zorder=3)
        label_line(ax, float(np.mean([x for x, _ in dead])), dead[0][1], "collapses to dead", NAVY,
                   dx=0, dy=7, ha="center")

    minimal = min(live)
    ax.plot(*minimal, "o", color=INK, ms=4, zorder=5)
    label_line(ax, *minimal, "minimal pool (selected by a vanishing floor)", INK, dx=7, dy=7,
               ha="left", va="bottom")

    cutoffs = [x for x, _ in live + dead]
    ax.set_xlim(min(cutoffs) - 0.14, max(cutoffs) + 0.14)
    ax.set_ylim(-0.03, 0.46)
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])
    ax.set_xlabel(r"pool cutoff $x'$")
    ax.set_ylabel(r"total entry $\mathsf{E}$")


def entry_fork() -> Path:
    branches = read_csv(f"{FORK}/branches.csv")
    family = [row for row in read_csv(f"{FORK}/cutoff_family.csv") if float(row["r"]) == 3.0]
    benchmark = read_csv("numerics/correspondence.csv")
    th = {row["boundary"]: float(row["value"]) for row in read_csv(f"{FORK}/thresholds.csv")}

    fig, (a, b) = plt.subplots(2, 1, figsize=(FULL_WIDTH, 6.0), constrained_layout=True,
                              gridspec_kw={"height_ratios": [1.15, 1.0]})
    _panel_a(a, branches, benchmark, th)
    _panel_b(b, family)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = HERE / "entry_fork.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(entry_fork())
