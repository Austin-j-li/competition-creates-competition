"""Shared figure style (E.4): vector PDF, embedded fonts, no in-figure titles, print-safe palette."""
from __future__ import annotations

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402

# Print-safe palette: navy, rust, mid gray, black for certified points. Line styles differ so every
# figure survives grayscale printing.
NAVY = "#1f3b73"
RUST = "#b5533c"
GRAY = "#656565"
INK = "#000000"
MUTED = "#6b6b6b"
TINT_A = "#e9edf5"   # analytical uniqueness region, no trade
TINT_B = "#f6e9e5"   # analytical uniqueness region, full orders
TINT_C = "#efefef"   # several equilibria found
SOLID = "-"
DASHED = (0, (5, 2.5))
DOTTED = (0, (1.2, 1.8))

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "STIXGeneral", "font.size": 10,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "axes.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK, "ytick.color": INK, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "xtick.direction": "out", "ytick.direction": "out", "xtick.major.size": 3, "ytick.major.size": 3,
    "axes.grid": False, "legend.frameon": False, "lines.linewidth": 1.6, "lines.solid_capstyle": "round",
    "mathtext.fontset": "stix",
})

FULL_WIDTH = 6.5


def panel_label(ax, text: str) -> None:
    """Panel label outside the axes, top left, clear of tick labels on any secondary axis."""
    ax.text(-0.11, 1.02, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=11, color=INK)


def label_line(ax, x: float, y: float, text: str, color: str, dx: float = 4, dy: float = 4, ha: str = "left",
               va: str = "bottom", size: float = 9) -> None:
    """Direct label at a point on a line, offset in points; the caller tunes dx, dy after viewing the render."""
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=size, color=color)


def region_label(ax, x: float, text: str, y_frac: float = 0.04) -> None:
    ax.text(x, y_frac, text, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=MUTED,
            linespacing=1.1)
