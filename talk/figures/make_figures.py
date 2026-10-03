"""Talk figures (structure plan, section 7): X1, X2, X3, X4.

Run with the research venv:  .venv/bin/python talk/figures/make_figures.py

Reads only validated CSV output (figures_data/two_returns.csv, figures_data/bargaining.csv,
figures_data/posterior_tails.csv) and
declared inputs from numerics/quantity_registry.csv. Nothing is solved, no parameter is changed,
no branch is dropped: every CSV row is plotted, and a non-finite value or a gap in a series
breaks the line (NaN) instead of being interpolated or replaced with zero.

Writes into talk/figures/:
  two_returns_talk.{pdf,svg,png}          X1  (two panels, 5.53 x 2.03 in = 0.92 linewidth x 0.6 textheight)
  profit_thresholds_talk.{pdf,svg,png}    X2  (one panel, 3.6 x 2.5 in, cost lines inside the figure)
  bargaining_spread_talk.{pdf,svg,png}    X4  (panel (a) of Figure 4 only, 3.3 x 2.3 in)
  posterior_tail_entry.{pdf,png}          X3  (copy of figures/posterior_tail_entry.pdf + 300-dpi PNG; provenance)
  posterior_tail_entry_talk.{pdf,svg,png} X3  (rebuilt from figures_data/posterior_tails.csv at 5.8 x 1.7 in,
                                              10 pt sans text, paper colors and labels; shown on backup A14)

Column meanings (checked against numerics/render/figures.py, figure1 and figure4):
  two_returns.csv: r = incumbent strength; mu = belief Pr(H) at which B_r(mu) = g_L + mu (g_H - g_L)
    is evaluated (mu in {m, 1/2, M}); Delta_T = target-payoff spread t_H - t_L (does not depend on mu,
    so the mu = 1/2 rows give the one Delta_T curve); B_r(mu) = challenger's expected gross profit;
    at mu = 1/2 it is (g_H + g_L)/2, the profit at the prior.
  bargaining.csv: eta = seller bargaining weight; r = incumbent strength (1.2, 3);
    Delta_eta = target-payoff spread under Nash bargaining.
"""
from __future__ import annotations

import csv
import math
import shutil
import subprocess
from decimal import Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "talk" / "figures"

# ---- palette (structure plan, section 5) -----------------------------------------------------
C_INFO = "#AA4B00"   # cInfo: information force, target-payoff spread
C_COST = "#006F50"   # cCost: preparation-cost objects
INK = "#000000"
DARK = "#4D4D4D"
MID = "#808080"
GRID = "#8C8C8C"
SOLID = "-"
DASHED = (0, (5, 2.5))
DOTTED = (0, (1.2, 1.8))

# ---- style: vector PDF, embedded fonts, no titles, Latin-Modern sans like the Beamer text ------
LMSANS = Path("/home/uctpiaj/work/texlive/2026/texmf-dist/fonts/opentype/public/lm/lmsans10-regular.otf")
FONT = "DejaVu Sans"
if LMSANS.exists():
    font_manager.fontManager.addfont(str(LMSANS))
    FONT = font_manager.FontProperties(fname=str(LMSANS)).get_name()

FS = 11  # every text element is >= 11 pt at the planned width (figures are drawn at that width)
plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "path",
    "font.family": FONT, "font.size": FS,
    "mathtext.fontset": "cm", "mathtext.default": "it",
    "axes.edgecolor": INK, "axes.labelcolor": INK, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.labelsize": FS, "xtick.labelsize": FS, "ytick.labelsize": FS,
    "xtick.color": INK, "ytick.color": INK, "xtick.direction": "out", "ytick.direction": "out",
    "xtick.major.size": 3, "ytick.major.size": 3, "axes.grid": False,
    "lines.linewidth": 1.8, "lines.solid_capstyle": "round",
    "savefig.dpi": 300,
})


# ---- inputs -------------------------------------------------------------------------------------
def read_csv(rel: str) -> list[dict]:
    with (ROOT / rel).open(newline="") as fh:
        return list(csv.DictReader(fh))


def registry() -> dict[str, dict]:
    return {r["name"]: r for r in read_csv("numerics/quantity_registry.csv")}


REG = registry()


def reg_dec(name: str) -> Decimal:
    """Exact decimal of a declared input or registry value (never through a binary float)."""
    return Decimal(REG[name]["value"])


def reg(name: str) -> float:
    return float(reg_dec(name))


R_WEAK, R_STRONG, R_COLLAPSE = reg("base_r_weak"), reg("base_r_strong"), reg("base_r_collapse")
C_LOW, C_HIGH = reg("base_c_low"), reg("base_c_high")
M_LOW, M_HIGH = reg("base_m"), reg("base_M")


def fnum(x: str) -> float:
    v = float(x)
    return v if math.isfinite(v) else math.nan


def series(rows: list[dict], xkey: str, ykey: str, max_gap: float) -> tuple[np.ndarray, np.ndarray]:
    """Sorted series; a gap wider than max_gap or a non-finite value becomes NaN (broken line)."""
    pts = sorted(((fnum(r[xkey]), fnum(r[ykey])) for r in rows), key=lambda t: t[0])
    xs: list[float] = []
    ys: list[float] = []
    for i, (x, y) in enumerate(pts):
        if i and x - pts[i - 1][0] > max_gap:
            xs.append((x + pts[i - 1][0]) / 2)
            ys.append(math.nan)
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def at(xs: np.ndarray, ys: np.ndarray, x0: float) -> float:
    """Value at a grid node (the declared strengths are on the CSV grid; no interpolation)."""
    i = int(np.argmin(np.abs(xs - x0)))
    if abs(xs[i] - x0) > 1e-9 or not math.isfinite(ys[i]):
        raise ValueError(f"declared node {x0} is not a finite grid point of the figure data")
    return float(ys[i])


def two_returns() -> dict[str, tuple[np.ndarray, np.ndarray]]:
    rows = read_csv("figures_data/two_returns.csv")
    mus = sorted({float(r["mu"]) for r in rows})
    want = {"m": M_LOW, "prior": 0.5, "M": M_HIGH}
    if len(mus) != 3 or any(abs(mus[i] - v) > 1e-12 for i, v in enumerate(want.values())):
        raise ValueError(f"unexpected mu grid {mus}; expected m, 1/2, M from the registry")
    out = {}
    for tag, mu in want.items():
        sub = [r for r in rows if abs(float(r["mu"]) - mu) < 1e-12]
        out[tag] = series(sub, "r", "B_r(mu)", max_gap=0.0051)
    sub = [r for r in rows if abs(float(r["mu"]) - 0.5) < 1e-12]
    out["spread"] = series(sub, "r", "Delta_T", max_gap=0.0051)
    return out


def save(fig, stem: str) -> None:
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"{stem}.{ext}", facecolor="white")
    plt.close(fig)


def panel_label(ax, text: str) -> None:
    ax.text(-0.02, 1.0, text, transform=ax.transAxes, ha="right", va="bottom", fontsize=FS, color=INK,
            fontweight="bold")


def vline(ax, x: float) -> None:
    ax.axvline(x, color=GRID, lw=0.9, ls=DOTTED, zorder=1)


def axes_in(fig, w: float, h: float, x0: float, y0: float, aw: float, ah: float):
    """Axes placed by inch coordinates on a w x h inch canvas (so 11 pt text is 11 pt on the slide)."""
    return fig.add_axes([x0 / w, y0 / h, aw / w, ah / h])


# ---- X1 -----------------------------------------------------------------------------------------
def fig_x1() -> None:
    d = two_returns()
    W, H = 5.53, 2.03   # 0.92 linewidth x 0.6 textheight of the 16:9 Madrid frame (433.3 pt x 243.4 pt)
    fig = plt.figure(figsize=(W, H))
    fs = 12   # X1 ticks, labels and annotations at 12 pt for projection
    a = axes_in(fig, W, H, 0.84, 0.58, 1.72, 1.18)
    b = axes_in(fig, W, H, 3.68, 0.58, 1.80, 1.18)
    xs, ys = d["spread"]
    xb, yb = d["prior"]
    a.plot(xs, ys, color=C_INFO, ls=SOLID, lw=2.0, zorder=3)
    b.plot(xb, yb, color=INK, ls=SOLID, lw=2.0, zorder=3)
    for ax, (x, y), ylim, col in ((a, (xs, ys), (0, 1.45), C_INFO), (b, (xb, yb), (0, 10.0), INK)):
        for r in (R_WEAK, R_STRONG):
            vline(ax, r)
            ax.plot([r], [at(x, y, r)], "o", ms=4.5, color=col, zorder=4)
        ax.set_xlim(1.0, 3.8)
        ax.set_ylim(*ylim)
        ax.set_xticks([1.0, 2.0, 3.0])
        ax.set_xticklabels(["1", "2", "3"])
        ax.tick_params(labelsize=fs)
        ax.set_xlabel(r"incumbent strength $r$", labelpad=2, fontsize=fs)
        top = ax.get_ylim()[1]
        # two-line labels as on X2 ("weak" / "r0 = 1.2"), each set 0.08 to the right of its own vertical so
        # neither touches a dotted line and the two never meet (r1's label uses the free band r > 3)
        ax.text(R_WEAK + 0.08, top, "weak\n$r_{\\mathrm{0}}$ = 1.2", ha="left", va="top", fontsize=fs - 1,
                color=DARK, linespacing=1.1)
        ax.text(R_STRONG + 0.08, top, "strong\n$r_{\\mathrm{1}}$ = 3", ha="left", va="top", fontsize=fs - 1,
                color=DARK, linespacing=1.1)
    a.set_yticks([0, 0.5, 1.0])
    a.set_yticklabels(["0", "0.5", "1"])
    b.set_yticks([0, 2, 4, 6, 8])
    a.set_ylabel("target-payoff\nspread $\\Delta_T$", labelpad=3, fontsize=fs)
    b.set_ylabel("expected profit\nat the prior", labelpad=6, fontsize=fs, linespacing=1.05)
    # panel labels at the same offset left of each panel's axes (above its y-label), clear of panel (a)'s x-axis end
    for ax, tag in ((a, "(a)"), (b, "(b)")):
        x_in = ax.get_position().x0 * W - 0.80
        fig.text(x_in / W, 1 - 0.03 / H, tag, ha="left", va="top", fontsize=fs, color=INK, fontweight="bold")
    save(fig, "two_returns_talk")


# ---- X2 -----------------------------------------------------------------------------------------
def fig_x2() -> None:
    """Left column of frame 8, drawn at its final size (3.6 x 2.5 in, 10 pt text), so no rescaling on the
    slide shrinks the labels; the plot area is 1.72 in tall so the best-price curve and the c_H line
    visibly separate at r1 and cross before r2."""
    d = two_returns()
    fs = 10
    W, H = 3.6, 2.5
    fig = plt.figure(figsize=(W, H))
    ax = axes_in(fig, W, H, 0.52, 0.40, 2.05, 1.72)
    for r in (R_WEAK, R_STRONG, R_COLLAPSE):
        vline(ax, r)
    ax.axhline(C_HIGH, color=C_COST, lw=1.8, ls=SOLID, zorder=2)
    ax.axhline(C_LOW, color=C_COST, lw=1.8, ls=DASHED, zorder=2)
    xm, ym = d["m"]
    xp, yp = d["prior"]
    xM, yM = d["M"]
    ax.plot(xM, yM, color=INK, ls=SOLID, lw=2.0, zorder=3)
    ax.plot(xp, yp, color=DARK, ls=DASHED, lw=1.8, zorder=3)
    ax.plot(xm, ym, color=MID, ls=DOTTED, lw=2.2, zorder=3)
    ax.set_xlim(1.0, 3.8)
    ax.set_ylim(0.5, 7.5)
    ax.set_xticks([1.0, 2.0, 3.0])
    ax.set_xticklabels(["1", "2", "3"])
    ax.set_yticks([2, 4, 6])
    ax.tick_params(labelsize=fs)
    ax.set_xlabel(r"incumbent strength $r$", labelpad=2, fontsize=fs)
    ax.set_ylabel("challenger's profit $B_r(\\mu)$", labelpad=3, fontsize=fs)
    # direct curve labels just past the right end of each curve
    for (x, y), text, col in ((d["M"], "best price ($M$)", INK), (d["prior"], "prior", DARK),
                              (d["m"], "worst price ($m$)", "#595959")):
        ax.annotate(text, (x[-1], y[-1]), xytext=(4, 0), textcoords="offset points", ha="left", va="center",
                    fontsize=fs, color=col, annotation_clip=False)
    # cost labels inside the picture, in the free bands next to their lines
    ax.text(1.62, C_HIGH - 0.25, "expensive cost $c_H$", ha="left", va="top", fontsize=fs, color=C_COST)
    ax.text(1.27, C_LOW + 0.2, "cheap cost $c_L$", ha="left", va="bottom", fontsize=fs, color=C_COST)
    # strength labels above the axes; the r2 label sits on the right of its vertical, away from the crossing
    trans = ax.get_xaxis_transform()
    ax.text(R_WEAK - 0.04, 1.03, "weak\n$r_{\\mathrm{0}}$ = 1.2", transform=trans, ha="left", va="bottom",
            fontsize=fs, color=DARK, linespacing=1.05)
    ax.text(R_STRONG - 0.04, 1.03, "strong\n$r_{\\mathrm{1}}$ = 3", transform=trans, ha="right", va="bottom",
            fontsize=fs, color=DARK, linespacing=1.05)
    ax.text(R_COLLAPSE + 0.04, 1.03, "stronger still\n$r_{\\mathrm{2}}$ = 3.6", transform=trans, ha="left",
            va="bottom", fontsize=fs, color=DARK, linespacing=1.05)
    save(fig, "profit_thresholds_talk")


# ---- X4 -----------------------------------------------------------------------------------------
def fig_x4() -> None:
    rows = read_csv("figures_data/bargaining.csv")  # all rows, including the eta = 1 payment-stage limit
    strengths = {Decimal(r["r"]) for r in rows}
    if strengths != {reg_dec("base_r_weak"), reg_dec("base_r_strong")}:
        raise ValueError(f"bargaining strengths {strengths} differ from the declared r0, r1")
    W, H = 3.3, 2.3   # left column of backup A9 at final size; 10 pt text
    fs = 10
    fig = plt.figure(figsize=(W, H))
    ax = axes_in(fig, W, H, 0.50, 0.42, 1.80, 1.78)
    data = {}
    for rs, ls, name in ((reg_dec("base_r_weak"), DASHED, "weak"), (reg_dec("base_r_strong"), SOLID, "strong")):
        sub = [r for r in rows if Decimal(r["r"]) == rs]
        x, y = series(sub, "eta", "Delta_eta", max_gap=0.0101)
        data[name] = (x, y)
        ax.plot(x, y, color=C_INFO, ls=ls, lw=2.0, zorder=3)
    vline(ax, 0.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 10.5)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1"])
    ax.tick_params(labelsize=fs)
    ax.set_yticks([0, 5, 10])
    ax.set_xlabel(r"seller bargaining weight $\eta$", labelpad=2, fontsize=fs)
    ax.set_ylabel("target-payoff spread $\\Delta_\\eta$", labelpad=3, fontsize=fs)
    ax.text(0.5, 0.03, r"$\eta$ = 1/2", transform=ax.get_xaxis_transform(), ha="center", va="bottom",
            fontsize=fs, color=DARK, bbox=dict(fc="white", ec="none", pad=1.0), zorder=5)
    xw, yw = data["weak"]
    xs, ys = data["strong"]
    ax.annotate("weak $r_{\\mathrm{0}}$ = 1.2", (xw[-1], yw[-1]), xytext=(6, 3), textcoords="offset points", ha="left",
                va="bottom", fontsize=fs, color=C_INFO, annotation_clip=False)
    ax.annotate("strong $r_{\\mathrm{1}}$ = 3", (xs[-1], ys[-1]), xytext=(6, -3), textcoords="offset points", ha="left",
                va="top", fontsize=fs, color=C_INFO, annotation_clip=False)
    save(fig, "bargaining_spread_talk")


# ---- X3 -----------------------------------------------------------------------------------------
def copy_x3() -> None:
    src = ROOT / "figures" / "posterior_tail_entry.pdf"
    dst = OUT / "posterior_tail_entry.pdf"
    shutil.copyfile(src, dst)
    subprocess.run(["pdftocairo", "-png", "-r", "300", "-singlefile", str(dst), str(OUT / "posterior_tail_entry")],
                   check=True)


# ---- X3 (rebuilt at slide size) ----------------------------------------------------------------
NAVY, RUST = "#1f3b73", "#b5533c"   # the paper's Figure 3 palette (numerics/render/style.py), kept


def fig_x3() -> None:
    """Figure 3 rebuilt from figures_data/posterior_tails.csv at the size backup A14 shows it
    (5.8 x 1.7 in, 10 pt sans text), with the paper's colors, line styles, labels (F43) and endpoint
    markers. Same rows as numerics/render/figures.py figure3: every tau_label == "grid" row of each law."""
    rows = read_csv("figures_data/posterior_tails.csv")
    if {Decimal(r["b"]) for r in rows} != {reg_dec("base_b")}:
        raise ValueError("Figure 3 noise laws must share the declared scale b")
    W, H = 5.8, 1.7
    fs = 10
    fig = plt.figure(figsize=(W, H))
    a = axes_in(fig, W, H, 0.78, 0.46, 1.95, 1.13)
    b = axes_in(fig, W, H, 3.62, 0.46, 1.95, 1.13)
    for noise, col, ls in (("Laplace", NAVY, SOLID), ("logistic", RUST, DASHED)):
        sub = sorted((r for r in rows if r["noise"] == noise and r["tau_label"] == "grid"),
                     key=lambda r: float(r["M_minus_tau"]))
        x = np.array([fnum(r["M_minus_tau"]) for r in sub])
        mass = np.array([fnum(r["posterior_upper_tail_mass"]) for r in sub])
        entry = np.array([fnum(r["E"]) for r in sub])
        if not all(np.all(np.isfinite(v)) for v in (x, mass, entry)):
            raise ValueError("Figure 3 requires finite plotted coordinates")
        for ax, y in ((a, mass), (b, entry)):
            ax.plot(x, y, color=col, ls=ls, lw=1.8, zorder=3)
            if x[0] == 0.0:
                ax.plot([0.0], [y[0]], "o", ms=5, color=col, zorder=5)
            i = int(np.argmin(np.abs(x - (0.06 if noise == "Laplace" else 0.10))))
            if noise == "Laplace":
                ax.annotate("Laplace", (x[i], y[i]), xytext=(0, 6), textcoords="offset points", ha="center",
                            va="bottom", fontsize=fs, color=col)
            else:
                ax.annotate("logistic", (x[i], y[i]), xytext=(7, -9), textcoords="offset points", ha="left",
                            va="top", fontsize=fs, color=col)
    a.set_ylabel("$\\Pr(\\mu_X \\geq \\tau)$\nunder full orders", fontsize=fs, labelpad=4, linespacing=1.1)
    b.set_ylabel("total entry $\\mathsf{E}$", fontsize=fs, labelpad=4)
    for ax in (a, b):
        ax.set_xlabel("threshold distance $M - \\tau$", fontsize=fs, labelpad=2)
        ax.set_xlim(-0.01, 0.24)
        ax.set_xticks([0, 0.05, 0.10, 0.15, 0.20])
        ax.set_xticklabels(["0", "0.05", "0.10", "0.15", "0.20"])
        ax.tick_params(labelsize=fs)
    a.set_ylim(-0.02, 0.55)
    a.set_yticks([0, 0.25, 0.5])
    a.set_yticklabels(["0", "0.25", "0.5"])
    b.set_ylim(0.22, 0.66)
    b.set_yticks([0.3, 0.4, 0.5, 0.6])
    for ax, tag in ((a, "(a)"), (b, "(b)")):
        x_in = ax.get_position().x0 * W - 0.74
        fig.text(x_in / W, 1 - 0.02 / H, tag, ha="left", va="top", fontsize=fs + 1, color=INK, fontweight="bold")
    save(fig, "posterior_tail_entry_talk")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig_x1()
    fig_x2()
    fig_x4()
    copy_x3()
    fig_x3()
    print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir() if p.suffix in {".pdf", ".svg", ".png"})))


if __name__ == "__main__":
    main()
