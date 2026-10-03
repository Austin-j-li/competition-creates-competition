"""Figure for the information-acquisition track: the insider region and the acquisition profile.

Panel (a): the region of (r, kappa) in which an equilibrium with information acquisition exists, bounded
above by the investor's ex-ante live profit U*(r). Panel (b): the investor's value of acquisition V as a
function of the acquisition probability lambda at fixed strengths, with the jump at the dilution floor.

This module renders only. It reads the solver's CSVs and the fork's thresholds; it never solves, never
changes a parameter, and never drops a branch. Lines break at unresolved nodes.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

from numerics.render.style import (DASHED, DOTTED, FULL_WIDTH, GRAY, INK, MUTED, NAVY, RUST, SOLID,  # noqa: E402
                                   TINT_A, TINT_B, label_line, panel_label, plt, region_label)

GAP = 0.06  # adjacent strengths further apart than this are not connected


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(s: str) -> float:
    return float("nan") if s in ("n/a", "") else float(s)


def truthy(s: str) -> bool:
    return s.strip().lower() == "true"


def _broken(points: list[tuple[float, float]], gap: float = GAP) -> tuple[np.ndarray, np.ndarray]:
    pts = sorted(points)
    xs: list[float] = []
    ys: list[float] = []
    for i, (x, y) in enumerate(pts):
        if i and x - pts[i - 1][0] > gap:
            xs.append(np.nan)
            ys.append(np.nan)
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def _panel_a(ax, region: list[dict], branch: list[dict], th: dict[str, float]) -> None:
    rmin, rmax = 1.0, 3.8
    r_k, r_c = th["trading_impossible_sufficient"], th["preparation_ceiling"]
    ax.axvspan(rmin, r_k, color=TINT_A, lw=0, zorder=0)
    ax.axvspan(r_c, rmax, color=TINT_A, lw=0, zorder=0)
    for value in (r_k, r_c):
        ax.axvline(value, color=MUTED, lw=0.7, ls=DOTTED, zorder=1)

    # closed-form full-order segment: U*(r) = J(r) - k where the sufficient test holds (analytical)
    full = [(num(d["r"]), num(d["U_star_closed"])) for d in region if truthy(d["full_order_test"])]
    lam_edge = [(num(d["r"]), num(d["U_lambda_min"])) for d in region
                if truthy(d["full_order_test"]) and truthy(d["lambda_min_full_orders_optimal"])]
    xf, yf = _broken(full, gap=0.02)
    ax.fill_between(xf, 0.0, yf, color=TINT_B, lw=0, zorder=1)
    ax.plot(xf, yf, color=RUST, ls=SOLID, lw=1.6, zorder=4)

    # partial-order segment of the lambda = 1 branch (numerical diagnostic): U* from the fork's branch rows
    partial = [(num(d["r"]), num(d["U_star"])) for d in branch if not (abs(num(d["qH"]) - 1) < 1e-9
                                                                        and abs(num(d["qL"]) + 1) < 1e-9)]
    if partial:
        xp, yp = _broken(partial)
        ax.fill_between(xp, 0.0, yp, color=TINT_B, lw=0, zorder=1)
        ax.plot(xp, yp, color=RUST, ls=DASHED, lw=1.2, zorder=4)
        ax.scatter([x for x, _ in partial], [y for _, y in partial], s=4, color=RUST, zorder=4)

    # lower edge of the mixed-acquisition band: V at lambda_min (analytical where full orders are optimal there)
    xl, yl = _broken(lam_edge, gap=0.02)
    ax.plot(xl, yl, color=NAVY, ls=DASHED, lw=1.1, zorder=3)

    # game B ceiling: U* minus the non-acquirer's short profit (numerical diagnostic)
    gameb = [(num(d["r"]), num(d["kappa_max_gameB"])) for d in branch if truthy(d["uninformed_short_profitable"])]
    if gameb:
        xb, yb = _broken(gameb)
        ax.plot(xb, yb, color=GRAY, ls=DOTTED, lw=1.3, zorder=3)

    # the cliff at the ceiling
    r_last, u_last = max(full)
    ax.plot([r_c, r_c], [0.0, u_last], color=RUST, ls=SOLID, lw=1.0, zorder=4)

    top = ax.secondary_xaxis("top")
    top.set_xticks([r_k, r_c])
    top.set_xticklabels(["trading impossible\n" + r"$\mathfrak{r}(k)$", "preparation ceiling\n" + r"$r_C$"], fontsize=8)
    top.tick_params(length=3, color=MUTED)
    top.spines["top"].set_visible(False)

    def at(points: list[tuple[float, float]], x0: float) -> tuple[float, float]:
        return min(sorted(points), key=lambda p: abs(p[0] - x0))

    # colour-coded text key in the empty upper-left area, one line per line style
    key_x, key_y = 1.30, 0.117
    ax.text(key_x, key_y, r"solid: $\kappa=U^*(r)=J(r)-k$, ceiling for pure acquisition (closed form)",
            ha="left", va="top", fontsize=8, color=RUST)
    ax.text(key_x, key_y - 0.011, r"dashed: $V(\lambda_{\min},r)$, floor of the mixed-acquisition band",
            ha="left", va="top", fontsize=8, color=NAVY)
    ax.text(key_x, key_y - 0.022, r"dotted: $U^*(r)-U_U(r)$, ceiling when a non-acquirer may trade",
            ha="left", va="top", fontsize=8, color=GRAY)
    if partial:
        label_line(ax, *at(partial, 1.80), "partial orders\n(numerical)", RUST, dx=-2, dy=8, ha="center")
    region_label(ax, (rmin + r_k) / 2 - 0.02, "no insider\nat any cost", y_frac=0.55)
    region_label(ax, (r_c + rmax) / 2 + 0.01, "no insider\nat any cost", y_frac=0.55)
    ax.text(2.75, 0.010, "an equilibrium with acquisition exists;\nthe dead equilibrium coexists",
            ha="center", va="bottom", fontsize=8, color=RUST, linespacing=1.1)
    ax.text(2.42, 0.070, "no equilibrium with acquisition\non this branch", ha="center", va="bottom", fontsize=8,
            color=MUTED, linespacing=1.1)

    ax.set_xlim(rmin, rmax)
    ax.set_ylim(0.0, 0.125)
    ax.set_yticks([0.0, 0.03, 0.06, 0.09, 0.12])
    ax.set_xlabel(r"incumbent strength $r$")
    ax.set_ylabel(r"acquisition cost $\kappa$")


def _panel_b(ax, quad: list[dict], grid: list[dict]) -> None:
    strengths = sorted({num(d["r"]) for d in quad})
    for r in strengths:
        rows = sorted([d for d in quad if num(d["r"]) == r], key=lambda d: num(d["lambda"]))
        lmin = num(rows[0]["lambda_min"])
        dead = [(num(d["lambda"]), num(d["V"])) for d in rows if num(d["lambda"]) < lmin]
        cert = [(num(d["lambda"]), num(d["V"])) for d in rows if num(d["lambda"]) >= lmin and truthy(d["suff_test"])]
        cand = [(num(d["lambda"]), num(d["V"])) for d in rows if num(d["lambda"]) >= lmin and not truthy(d["suff_test"])]
        if dead:
            ax.plot(*_broken(dead, gap=1.0), color=NAVY, ls=SOLID, lw=1.3, zorder=3)
        if cert:
            ax.plot(*_broken(cert, gap=1.0), color=RUST, ls=SOLID, lw=1.6, zorder=4)
        if cand:
            ax.plot(*_broken(cand, gap=1.0), color=GRAY, ls=DOTTED, lw=1.1, zorder=3)
        # the jump at the dilution floor
        v_floor = next((v for lam, v in sorted(cert + cand) if lam >= lmin), float("nan"))
        ax.plot([lmin, lmin], [0.0, v_floor], color=MUTED, lw=0.6, ls=DOTTED, zorder=2)
        ax.plot(lmin, 0.0, "o", mfc="white", mec=NAVY, ms=4, zorder=5)
        ax.plot(lmin, v_floor, "o", color=INK, ms=3.5, zorder=5)
        # grid fixed points (numerical diagnostic), broken at unresolved nodes
        pts = [(num(d["lambda"]), num(d["U"])) for d in grid if num(d["r"]) == r and truthy(d["live"])]
        if pts:
            ax.scatter([x for x, _ in pts], [y for _, y in pts], s=7, facecolors="none", edgecolors=RUST, lw=0.6,
                       zorder=6)
        end = max(cert) if cert else max(cand)
        label_line(ax, *end, rf"$r={r:g}$", INK, dx=4, dy=-3, ha="left", va="center", size=8)

    label_line(ax, 0.66, 0.0, "no live continuation below " + r"$\lambda_{\min}(r)$", NAVY, dx=0, dy=5,
               ha="left")
    ax.text(0.605, 0.108, "solid: full-order candidate, sufficient test holds (quadrature)", ha="left", va="top",
            fontsize=8, color=RUST)
    ax.text(0.605, 0.098, "dotted: candidate where the test fails;  circles: grid fixed points", ha="left",
            va="top", fontsize=8, color=GRAY)
    ax.text(0.605, 0.088, "filled point: the jump at " + r"$\lambda_{\min}(r)$", ha="left", va="top", fontsize=8,
            color=INK)
    ax.set_xlim(0.6, 1.06)
    ax.set_ylim(-0.004, 0.115)
    ax.set_xticks([0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_yticks([0.0, 0.03, 0.06, 0.09])
    ax.set_xlabel(r"acquisition probability $\lambda$")
    ax.set_ylabel(r"value of acquisition $V(\lambda, r)$")


def insider_region() -> Path:
    region = read_csv(HERE / "insider_region.csv")
    branch = read_csv(HERE / "uninformed_short.csv")
    quad = read_csv(HERE / "acquisition_profile_quad.csv")
    grid = read_csv(HERE / "acquisition_profile.csv")
    th = {d["boundary"]: num(d["value"]) for d in read_csv(HERE / "thresholds.csv")}

    fig, (a, b) = plt.subplots(2, 1, figsize=(FULL_WIDTH, 6.4), constrained_layout=True,
                              gridspec_kw={"height_ratios": [1.15, 1.0]})
    _panel_a(a, region, branch, th)
    _panel_b(b, quad, grid)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = HERE / "insider_region.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(insider_region())
