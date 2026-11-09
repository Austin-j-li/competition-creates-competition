"""Slide figure for frame 14: the close-up of the threshold belief between the strong incumbent r_1 and the
very strong incumbent r_2, drawn at the width of the frame's figure column (9 November 2026).

It replaces the crop of panel (b) of beliefs_talk.pdf on frame 14. The crop scaled a 7.4-inch figure down to the
column, so the band label ran across the curve and the axis. This figure is drawn at its printed size, on the
white slide paper, with free space for each label. It draws no text other than the tick labels: slides.tex sets
the axis titles, the band label and the three printed values with \\FigText, the values through the registry.
The script prints the anchor of each label in bp from the top-left corner, the coordinates \\FigText takes.

Usage: python3 make_band_talk.py [--out DIR]   (default DIR: slot/manuscript/figures)
"""
import argparse
import hashlib
import pathlib

import numpy as np
import matplotlib.pyplot as plt

import make_figures as mf

W_IN, H_IN = 1.86, 2.05          # printed size: the 0.31 column of a 16:9 frame (15.2 cm text width)
AX = (0.235, 0.20, 0.725, 0.76)  # axes box in figure fractions: left, bottom, width, height
PAPER = "#ffffff"                # journal look: white paper


def draw():
    mf.ARCHIVO_OK = mf.register_archivo()
    S = mf.Style(True)
    S.apply()
    info, cost = mf.INFO_T, mf.COST_T
    plt.rcParams.update({"figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
                         "xtick.labelsize": 7.0, "ytick.labelsize": 7.0,
                         "xtick.major.size": 3.0, "ytick.major.size": 3.0})
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=72)
    ax = fig.add_axes(AX)
    t1, t2 = float(mf.tau(mf.PF, mf.R1)), float(mf.tau(mf.PF, mf.R2))
    Mv, rC = float(mf.PM.M), mf.BF["rC"]
    rr = np.linspace(mf.R1, mf.R2, 400)
    ax.axhspan(t1, t2, color=mf.BAND_INFO_T, lw=0, zorder=0)
    ax.axhline(t1, color=info, lw=1.0, zorder=1)
    ax.axhline(t2, color=info, lw=1.0, zorder=1)
    ax.axhline(Mv, color=info, ls=(0, (5, 2)), lw=1.4, zorder=2)
    ax.plot(rr, mf.tau(mf.PF, rr), color=cost, lw=2.2, solid_capstyle="butt", zorder=4)
    ax.axvline(rC, color="0.3", ls=":", lw=0.8, zorder=1)
    mf.dot(ax, rC, Mv, S, color="k", open_=True, size=4.6)
    mf.dot(ax, mf.R1, t1, S, color=cost, size=5.0)
    mf.dot(ax, mf.R2, t2, S, color=cost, size=5.0)
    ax.set_xlim(mf.R1, mf.R2)
    ax.set_ylim(0.7000, 0.7350)
    ax.set_xticks([3.0, 3.2, 3.4, 3.6])
    ax.set_xticklabels([r"$r_1$", "3.2", "3.4", r"$r_2$"])
    ax.set_yticks([0.700, 0.710, 0.720, 0.730])
    ax.set_yticklabels(["0.70", "0.71", "0.72", "0.73"])

    H = H_IN * 72.0

    def bp(x, y):
        """Data point to bp from the figure's top-left corner."""
        X, Y = ax.transData.transform((x, y))
        return round(X, 1), round(H - Y, 1)

    def bp_axes(fx, fy):
        X, Y = ax.transAxes.transform((fx, fy))
        return round(X, 1), round(H - Y, 1)

    fig.canvas.draw()
    anchors = {
        "tau_r2 label (anchor=south west)": bp(3.012, t2 + 0.0004),
        "M_half label (anchor=north west)": bp(3.012, Mv - 0.0007),
        "band label line 1 (anchor=north west)": bp(3.012, 0.7270),
        "band label line 2 (anchor=north west)": bp(3.012, 0.7248),
        "band label line 3 (anchor=north west)": bp(3.012, 0.7226),
        "tau_r1 label (anchor=south east)": bp(3.555, t1 + 0.0005),
        "x title (anchor=north), below the ticks": bp_axes(0.5, -0.14),
        "y title (rotate=90, anchor=south), left of the ticks": bp_axes(-0.235, 0.5),
        "curve at x=3.35 (clearance check)": bp(3.35, float(mf.tau(mf.PF, 3.35))),
    }
    return fig, anchors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(mf.ROOT / "slot" / "manuscript" / "figures"))
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fig, anchors = draw()
    path = out / "band_talk.pdf"
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None, "Creator": "Competition Creates Competition"})
    plt.close(fig)
    print(f"figure size {W_IN*72:.1f} x {H_IN*72:.1f} bp")
    for k, v in anchors.items():
        print(f"  {k:<52} {v[0]:>6} {v[1]:>6}")
    print(f"sha256 {hashlib.sha256(path.read_bytes()).hexdigest()}  {path}")


if __name__ == "__main__":
    main()
