"""Shared figure style (E.4): vector PDF, embedded fonts, no in-figure titles, recessive axes."""
from __future__ import annotations

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402

# Validated categorical palette, fixed slot order (never cycled): blue, orange, aqua, yellow, magenta.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
INK = "#0b0b0b"
MUTED = "#52514e"
GRID = "#d9d8d3"
REGION_A = "#e8eef8"  # analytical uniqueness shading
REGION_B = "#fbe9df"

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "serif", "font.size": 9,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK, "ytick.labelcolor": INK,
    "grid.color": GRID, "grid.linewidth": 0.5, "axes.grid": True, "axes.axisbelow": True,
    "legend.frameon": False, "legend.fontsize": 8, "lines.linewidth": 1.4,
})


def panel_label(ax, text: str) -> None:
    ax.text(0.0, 1.02, text, transform=ax.transAxes, ha="left", va="bottom", fontsize=10, color=INK)
