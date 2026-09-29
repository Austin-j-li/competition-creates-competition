"""Talk exhibit X5 (structure plan, section 7): Figure 2 of the paper as two single-panel files.

Run with the research venv:  .venv/bin/python talk/figures/make_correspondence_figure.py

Writes into talk/figures/:
  equilibrium_correspondence_a_talk.{pdf,svg,png}   (a) entry against incumbent strength r   (backup A24)
  equilibrium_correspondence_b_talk.{pdf,svg,png}   (b) order size |q_L| against r            (backup A25)

Each file is drawn at its final size on the slide, \\includegraphics[width=\\linewidth] in the 16:9 Madrid
frame (linewidth 433.3 pt = 6.0 in, textheight 243.4 pt = 3.37 in), so every text element is 10 pt on the slide.

Source and rules. The plotting calls are those of figure2() in numerics/render/figures.py, reused through its own
helpers (_correspondence_rows validates the continuation ledger, _broken_series builds the broken lines), on the
same inputs: numerics/correspondence.csv, mixed_supports.csv, thresholds.csv, certificates.csv. Nothing is solved,
no parameter is changed and no branch or node is dropped; lines stay broken at unresolved nodes; certified points
keep their interval bars; the analytical shading, the multiplicity ticks and the r_N, r_U, r_C markers are kept.
Only text changes (paper-sync #16 and F05, F11, F41, F48, F52): "(1, q_L)" for "(1, -v)", "q_H = -q_L < 1" for
"(u, -u)", axis "order size |q_L|"; thresholds annotated by meaning; a status key with visible "computer-assisted"
and "numerical diagnostic" entries and the note that certified enclosures are narrower than the marker. The r_P
tick marks the edge of the existing no-trade shading. No number is printed in the figure: threshold values appear
on the slide, tagged with their registry keys.

After drawing, the script rebuilds the paper's Figure 2 in memory (its PDF goes to a temporary directory; figures/
is never written) and checks that the data artists of each talk panel (lines with their breaks, scatter points,
interval bars, shading, threshold lines, multiplicity ticks) equal those of the matching source panel. It also
checks every accepted continuation row, certificate and mixed support against the plotted points, and the
thresholds and certificates against numerics/quantity_registry.csv. Any mismatch exits nonzero.
"""
from __future__ import annotations

import sys
import tempfile
from collections import Counter
from decimal import Decimal
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from numerics.io import read_csv  # noqa: E402
from numerics.render import figures as paper  # noqa: E402  (source renderer; its helpers are reused)
from numerics.render.style import (DASHED, DOTTED, GRAY, INK, MUTED, NAVY, RUST, SOLID, TINT_A, TINT_B,  # noqa: E402
                                   plt)
from matplotlib import font_manager  # noqa: E402

OUT = ROOT / "talk" / "figures"

# ---- slide style: Latin Modern Sans like the Beamer text, 11 pt at the planned width -------------------------
LMSANS = Path("/home/uctpiaj/work/texlive/2026/texmf-dist/fonts/opentype/public/lm/lmsans10-regular.otf")
FONT = "DejaVu Sans"
if LMSANS.exists():
    font_manager.fontManager.addfont(str(LMSANS))
    FONT = font_manager.FontProperties(fname=str(LMSANS)).get_name()
FS = 10
TALK_RC = {
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "path",
    "font.family": [FONT, "DejaVu Sans"], "font.size": FS,
    "mathtext.fontset": "cm", "mathtext.default": "it",
    "axes.labelsize": FS, "xtick.labelsize": FS, "ytick.labelsize": FS,
    "axes.linewidth": 0.8, "savefig.dpi": 300,
}
W, H = 5.99, 2.42        # inches: width = linewidth; height 0.71 textheight (natural size on the slide)
AX = (0.58, 0.82, 5.30, 1.24)   # axes left, bottom, width, height in inches; the status key is a row below
RMIN, RMAX = 1.0, 3.8          # as in the source figure


# ---- data (identical selection to paper.figure2) ---------------------------------------------------------------
def load() -> dict:
    rows = read_csv("numerics/correspondence.csv")
    certs = [c for c in read_csv("numerics/certificates.csv") if c["accepted"] == "true"]
    th = {r["boundary"]: float(r["value"]) for r in read_csv("numerics/thresholds.csv") if r["value"] not in ("nan", "n/a")}
    acc = paper._correspondence_rows(rows)
    nodes = sorted({Decimal(r["r"]) for r in rows})
    multi = sorted({float(Decimal(r["r"])) for r in acc if r["multiplicity_found"] == "true"})
    series = {
        "pooling": (NAVY, SOLID, 1.6), "full_orders": (RUST, SOLID, 1.6),
        "asymmetric": (NAVY, DASHED, 1.6), "symmetric_interior": (GRAY, DOTTED, 2.0),
        "pure": (GRAY, SOLID, 1.2), "mixed": (GRAY, DASHED, 1.2),
    }
    for branch in sorted({row["branch"] for row in acc} - series.keys()):
        series[branch] = (GRAY, DASHED, 1.2)
    kept = {br: [r for r in acc if r["branch"] == br] for br in series}
    kept = {br: sub for br, sub in kept.items() if sub}
    mixed = [r for r in acc if r["q_H"] == "mixed"]
    support_rows = read_csv("numerics/mixed_supports.csv") if mixed else []
    supports = {}
    for row in mixed:
        sub = [s for s in support_rows if s["accepted"] == "true"
               and s.get("continuation_id") == row["continuation_id"] and s.get("candidate_id") == row["candidate_id"]]
        if not sub:
            raise ValueError("mixed continuation has no identified support records")
        supports[row["candidate_id"]] = sub
    return dict(rows=rows, certs=certs, th=th, acc=acc, nodes=nodes, multi=multi, series=series, kept=kept,
                mixed=mixed, supports=supports)


def check_registry(d: dict) -> None:
    """Thresholds and certificates equal their registry rows (exact decimal strings, never re-rounded)."""
    reg = {r["name"]: r for r in read_csv("numerics/quantity_registry.csv")}
    thr = {r["boundary"]: r for r in read_csv("numerics/thresholds.csv")}
    pairs = {"pooling_unique_sufficient": "base_r_pool_unique_sufficient", "pooling_existence": "base_r_no_trade_exact",
             "full_orders_unique_sufficient": "base_r_full_unique_sufficient", "high_cost_ceiling": "base_r_high_cost_ceiling"}
    for boundary, key in pairs.items():
        if Decimal(thr[boundary]["value"]) != Decimal(reg[key]["value"]):
            raise ValueError(f"threshold {boundary} differs from registry {key}")
    for tag, cert in zip("abc", sorted(d["certs"], key=lambda c: Decimal(c["r"]))):
        if Decimal(reg[f"cert_{tag}_r"]["value"]) != Decimal(cert["r"]):
            raise ValueError(f"certificate r differs from registry cert_{tag}_r")
        v, e = reg[f"cert_{tag}_v_interval"], reg[f"cert_{tag}_entry_interval"]
        if (Decimal(v["lower"]), Decimal(v["upper"])) != (Decimal(cert["v_lower"]), Decimal(cert["v_upper"])):
            raise ValueError(f"certificate order interval differs from registry cert_{tag}_v_interval")
        if (Decimal(e["lower"]), Decimal(e["upper"])) != (Decimal(cert["E_lower"]), Decimal(cert["E_upper"])):
            raise ValueError(f"certificate entry interval differs from registry cert_{tag}_entry_interval")


# ---- drawing helpers --------------------------------------------------------------------------------------------
KEY = [("cert", "computer-assisted; enclosures narrower\nthan the marker (exact intervals in A21)"),
       ("broken", "colored curves: numerical\ndiagnostic; gaps at unresolved nodes")]
# The shading (unique, analytical) is named on the slide next to the threshold values.


def label(ax, x: float, y: float, text: str, color: str, dx: float = 0, dy: float = 0, ha: str = "center",
          va: str = "bottom") -> None:
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=FS, color=color,
                linespacing=1.05)


def new_axes():
    fig = plt.figure(figsize=(W, H))
    x0, y0, aw, ah = AX
    ax = fig.add_axes([x0 / W, y0 / H, aw / W, ah / H])
    return fig, ax


def decorate(ax, d: dict) -> None:
    """Shading, multiplicity ticks and threshold lines exactly as in the source; thresholds annotated by meaning."""
    from matplotlib.transforms import ScaledTranslation
    th, multi = d["th"], d["multi"]
    ax.axvspan(RMIN, th["pooling_unique_sufficient"], color=TINT_A, lw=0, zorder=0)
    ax.axvspan(th["full_orders_unique_sufficient"], RMAX, color=TINT_B, lw=0, zorder=0)
    if multi:
        ax.vlines(multi, 0, 0.018, transform=ax.get_xaxis_transform(), color=GRAY, lw=0.7, zorder=2)
    for key in ("pooling_existence", "full_orders_unique_sufficient", "high_cost_ceiling"):
        ax.axvline(th[key], color=MUTED, lw=0.7, ls=DOTTED, zorder=1)
    ax.set_xlim(RMIN, RMAX)
    ax.set_xticks([1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    ax.set_xlabel(r"incumbent strength $r$", labelpad=2)
    # threshold names by meaning on a top axis, outside the data area (F41, F52); r_P is the shading edge.
    # The last number is a horizontal nudge in points so neighbouring names do not touch.
    ticks = [("pooling_unique_sufficient", "no trade unique\nbelow $r_P$", -12),
             ("pooling_existence", "no trade exists\nup to $r_N$", 4),
             ("full_orders_unique_sufficient", "full orders unique\nabove $r_U$", -12),
             ("high_cost_ceiling", "expensive entry\nimpossible above $r_C$", -14)]
    top = ax.secondary_xaxis("top")
    top.set_xticks([th[k] for k, _, _ in ticks])
    top.set_xticklabels([t for _, t, _ in ticks], fontsize=FS, color=INK, linespacing=1.0)
    top.tick_params(length=3, color=MUTED, pad=2)
    top.spines["top"].set_visible(False)
    for lab, (_, _, dx) in zip(top.get_xticklabels(), ticks):
        lab.set_transform(lab.get_transform() + ScaledTranslation(dx / 72, 0, ax.figure.dpi_scale_trans))


def status_key(fig, ax, *_unused):
    """Status key as one row of two entries below the x-axis label, in its own axes, so it never covers data
    or in-plot labels and no key artist can be mistaken for data."""
    lh = FS * 1.1
    pad = 2.5
    lines = max(t.count("\n") + 1 for _, t in KEY)
    height_pt = lh * lines + 2 * pad
    x0_in, width_in = 0.08, W - 0.14   # the key row spans the figure width
    k = fig.add_axes([x0_in / W, 0.02 / H, width_in / W, height_pt / 72 / H], label="status key")
    k.set_xlim(0, width_in * 72)
    k.set_ylim(0, height_pt)
    k.axis("off")
    k.add_patch(plt.Rectangle((0, 0), width_in * 72, height_pt, facecolor="white", lw=0.5, edgecolor="#bdbdbd",
                              zorder=0))
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    FigureCanvasAgg(fig)
    rend = fig.canvas.get_renderer()
    x = 4.0
    for kind, text in KEY:
        yc = height_pt - pad - lh / 2
        if kind == "cert":
            k.errorbar([x + 8], [yc], yerr=[4], fmt="o", ms=4.5, color=INK, ecolor=INK, elinewidth=0.8, capsize=3)
        elif kind == "broken":   # one navy and one rust segment with a gap: the colored curves, broken
            k.plot([x, x + 6.5], [yc, yc], color=NAVY, lw=1.6, solid_capstyle="butt")
            k.plot([x + 10, x + 16.5], [yc, yc], color=RUST, lw=1.6, solid_capstyle="butt")
        else:
            k.add_patch(plt.Rectangle((x, yc - 4), 8, 8, color=TINT_A, lw=0))
            k.add_patch(plt.Rectangle((x + 8.5, yc - 4), 8, 8, color=TINT_B, lw=0))
        t = k.text(x + 21, height_pt - pad, text, ha="left", va="top", fontsize=FS, color=INK, linespacing=1.1)
        x = t.get_window_extent(rend).transformed(k.transData.inverted()).x1 + 12   # next entry after a gap
    return k


# ---- panel (a): entry --------------------------------------------------------------------------------------------
def draw_entry(d: dict):
    from numerics.params import BENCHMARK
    fig, a = new_axes()
    decorate(a, d)
    th, kept, series, certs, nodes = d["th"], d["kept"], d["series"], d["certs"], d["nodes"]
    for br, (col, ls, lw) in series.items():
        sub = kept.get(br)
        if not sub:
            continue
        x, y = paper._broken_series(sub, "r", "E", 0.005, nodes=nodes)
        a.plot(x, y, color=col, ls=ls, lw=lw, zorder=3 if br != "symmetric_interior" else 4)
        a.scatter([float(r["r"]) for r in sub], [float(r["E"]) for r in sub], s=2, color=col, zorder=3)
    cx = np.array([float(c["r"]) for c in certs])
    eL = np.array([float(c["E_lower"]) for c in certs])
    eU = np.array([float(c["E_upper"]) for c in certs])
    a.errorbar(cx, (eL + eU) / 2, yerr=(eU - eL) / 2, fmt="o", ms=4.5, color=INK, ecolor=INK, elinewidth=0.8, capsize=3, zorder=5)
    if "pooling" in kept:
        x, y = paper._at(*paper._broken_series(kept["pooling"], "r", "E", 0.005), 1.30)
        label(a, x, y, "no trade", NAVY, dy=4)
    if "full_orders" in kept:
        xs, ys = paper._broken_series(kept["full_orders"], "r", "E", 0.005)
        x, y = paper._at(xs, ys, 3.1)
        label(a, x, y, "full orders", RUST, dy=5)
        # sits over the r > r_C segment it names; a background in the shading color hides the r_C line under it
        a.annotate("full orders,\nno expensive entry", (RMAX, float(BENCHMARK.rho)), xytext=(-2, 5),
                   textcoords="offset points", ha="right", va="bottom", fontsize=FS, color=RUST, linespacing=1.05,
                   bbox=dict(fc=TINT_B, ec="none", pad=0.5), zorder=6)
        boundary = [r for r in kept["full_orders"] if abs(float(r["r"]) - th["high_cost_ceiling"]) < 1e-12]
        if len(boundary) != 1 or abs(float(boundary[0]["E"]) - th["laplace_entry_left_limit"]) > 1e-8:
            raise ValueError("requires the validated full-order equality outcome at the high-cost ceiling")
        a.plot(float(boundary[0]["r"]), float(boundary[0]["E"]), "o", color=RUST, ms=4, zorder=6)
        a.plot(th["high_cost_ceiling"], float(BENCHMARK.rho), "o", color=RUST, mfc="white", ms=4, zorder=6)
    if "asymmetric" in kept:
        x, y = paper._at(*paper._broken_series(kept["asymmetric"], "r", "E", 0.005), 1.60)
        # right-aligned so it ends before the r_N line
        label(a, 1.70, y, "asymmetric orders\n" r"$(\mathrm{1}, q_L)$", NAVY, dy=-8, ha="right", va="top")
    if "symmetric_interior" in kept:
        xs, ys = paper._broken_series(kept["symmetric_interior"], "r", "E", 0.005)
        x, y = paper._at(xs, ys, 1.834)
        label(a, x, y, "symmetric interior orders\n" r"$q_H = -q_L < \mathrm{1}$", GRAY, dx=6, dy=4, ha="left", va="bottom")
    # the black certified points are identified by the status key below the axes (no in-plot label, which
    # crowded the threshold names above the axes)
    for row in d["mixed"]:
        color = series[row["branch"]][0]
        a.scatter(float(row["r"]), float(row["E"]), s=22, marker="D", facecolors="white", edgecolors=color, zorder=6)
    a.set_ylabel("entry")
    a.set_ylim(0.04, 0.62)
    a.set_yticks([0.25, 0.35, 0.45, 0.55])
    if d["multi"]:
        # centred between the y-axis and the r_N line, clear of both
        a.text(1.375, 0.03, "multiplicity found;\nsearch not exhaustive",
               transform=a.get_xaxis_transform(), ha="center", va="bottom", fontsize=FS, color=MUTED, linespacing=1.0)
    key = status_key(fig, a, 2.02, 0.226, 3.22)
    return fig, a, key


# ---- panel (b): order size |q_L| ---------------------------------------------------------------------------------
def draw_orders(d: dict):
    fig, b = new_axes()
    decorate(b, d)
    kept, series, certs, nodes = d["kept"], d["series"], d["certs"], d["nodes"]
    cx = np.array([float(c["r"]) for c in certs])
    vL = np.array([float(c["v_lower"]) for c in certs])
    vU = np.array([float(c["v_upper"]) for c in certs])
    b.errorbar(cx, (vL + vU) / 2, yerr=(vU - vL) / 2, fmt="o", ms=4.5, color=INK, ecolor=INK, elinewidth=0.8, capsize=3, zorder=5)
    if "pooling" in kept:
        x, y = paper._broken_series(kept["pooling"], "r", "q_H", 0.005, nodes=nodes)
        b.plot(x, y, color=NAVY, ls=SOLID, lw=1.6, zorder=3)
        label(b, 1.28, 0.0, "no trade", NAVY, dy=4)   # (0, 0) is stated in the slide text under the panel
    if "full_orders" in kept:
        x, y = paper._broken_series(kept["full_orders"], "r", "q_H", 0.005, nodes=nodes)
        b.plot(x, y, color=RUST, ls=SOLID, lw=1.6, zorder=3)
        label(b, 2.45, 1.0, r"full orders $(\mathrm{1}, {-\mathrm{1}})$", RUST, dy=-4, va="top")
    if "asymmetric" in kept:
        xv, yv = paper._broken_series(kept["asymmetric"], "r", "v", 0.005, jump=0.2, nodes=nodes)
        b.plot(xv, yv, color=NAVY, ls=DASHED, lw=1.6, zorder=3)
        x, y = paper._at(xv, yv, 1.60)
        label(b, x, y, "asymmetric\n" r"$(\mathrm{1}, q_L)$", NAVY, dx=-9, ha="right", va="center")
    if "symmetric_interior" in kept:
        xu, yu = paper._broken_series(kept["symmetric_interior"], "r", "q_H", 0.005, jump=0.2, nodes=nodes)
        b.plot(xu, yu, color=GRAY, ls=DOTTED, lw=2.0, zorder=3)
        x, y = paper._at(xu, yu, 1.83)
        label(b, x, y, "symmetric interior\n" r"$q_H = -q_L < \mathrm{1}$", GRAY, dx=8, ha="left", va="center")
    for branch, sub in kept.items():
        pure = [r for r in sub if r["q_H"] != "mixed"]
        color = series[branch][0]
        if branch in ("pooling", "full_orders", "symmetric_interior", "asymmetric"):
            key = "v" if branch == "asymmetric" else "q_H"
            b.scatter([float(r["r"]) for r in pure], [abs(float(r[key])) for r in pure], s=2, color=color, zorder=3)
        else:
            for key, marker in (("q_H", "^"), ("q_L", "v")):
                b.scatter([float(r["r"]) for r in pure], [abs(float(r[key])) for r in pure], s=8, marker=marker, color=color, zorder=4)
    if d["mixed"]:
        for row in d["mixed"]:
            color = series[row["branch"]][0]
            sup = d["supports"][row["candidate_id"]]
            for state, marker in (("H", "^"), ("L", "v")):
                sub = [s for s in sup if s["state"] == state]
                b.scatter([float(s["r"]) for s in sub], [abs(float(s["q"])) for s in sub],
                          s=[8 + 16 * float(s["weight"]) for s in sub], marker=marker, color=color, zorder=4)
        last = d["mixed"][-1]
        top_q = max(abs(float(s["q"])) for s in d["supports"][last["candidate_id"]])
        # text just right of the symmetric-interior branch (which ends before r = 1.85), level with the
        # supports it names; no leader line, which would cross that branch at slide scale
        b.annotate("mixed candidate at $r_N$:\n" r"$\blacktriangle$ $q_H$ and $\blacktriangledown$ $q_L$ supports",
                   (1.87, top_q), xytext=(0, 3), textcoords="offset points", fontsize=FS, color=GRAY,
                   ha="left", va="bottom", linespacing=1.05)
    b.set_ylabel(r"order size $|q_L|$")
    b.set_ylim(-0.05, 1.12)
    b.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    key = status_key(fig, b, 2.10, 0.955, 3.22)
    return fig, b, key


# ---- layout check: nothing clipped, no text on text, no data under text or the key ---------------------------------
def layout_problems(fig, ax, key) -> list[str]:
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    FigureCanvasAgg(fig)
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    fbox = fig.bbox
    texts = []
    texts += key.texts
    for axis_owner in [ax, *ax.child_axes]:
        texts += axis_owner.texts
        for axis in (axis_owner.xaxis, axis_owner.yaxis):
            texts += [t for t in axis.get_ticklabels() if t.get_visible() and t.get_text()]
            if axis.label.get_text():
                texts.append(axis.label)
    boxes = [(t.get_text().replace("\n", " "), t.get_window_extent(rend)) for t in texts]
    probs = []
    for name, bb in boxes:
        if bb.x0 < fbox.x0 - 0.5 or bb.y0 < fbox.y0 - 0.5 or bb.x1 > fbox.x1 + 0.5 or bb.y1 > fbox.y1 + 0.5:
            probs.append(f"clipped: {name}")
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (n1, b1), (n2, b2) = boxes[i], boxes[j]
            if b1.x0 < b2.x1 - 1 and b2.x0 < b1.x1 - 1 and b1.y0 < b2.y1 - 1 and b2.y0 < b1.y1 - 1:
                probs.append(f"text overlap: '{n1}' / '{n2}'")
    pts = []
    for ln in ax.lines:
        if ln.get_transform() != ax.transData:
            continue
        x, y = (np.asarray(t, dtype=float) for t in ln.get_data())
        ok = np.isfinite(x) & np.isfinite(y)
        pts.append(ax.transData.transform(np.c_[x[ok], y[ok]]))
    for coll in ax.collections:
        if type(coll).__name__ == "PathCollection":
            pts.append(ax.transData.transform(np.asarray(coll.get_offsets(), dtype=float)))
    pts = np.vstack(pts)
    kbox = key.get_window_extent(rend)
    for t in key.texts:
        bb = t.get_window_extent(rend)
        if bb.x0 < kbox.x0 or bb.x1 > kbox.x1 or bb.y0 < kbox.y0 or bb.y1 > kbox.y1:
            probs.append(f"outside the key box: {t.get_text()!r}")
    for name, bb in boxes + [("status key", kbox)]:
        inside = (pts[:, 0] > bb.x0) & (pts[:, 0] < bb.x1) & (pts[:, 1] > bb.y0) & (pts[:, 1] < bb.y1)
        if inside.any():
            probs.append(f"data under text: '{name}' ({int(inside.sum())} points)")
    return probs


# ---- preservation check against the paper's Figure 2 -------------------------------------------------------------
def _r(v) -> tuple:
    a = np.asarray(v, dtype=float).ravel()
    return tuple(np.round(np.where(np.isnan(a), np.inf, a), 12))


def signature(ax) -> Counter:
    """Every data artist of an axes (lines with their NaN breaks, scatter points, bars, shading); text excluded."""
    from matplotlib.colors import to_hex
    sig = Counter()
    for ln in ax.lines:
        x, y = (np.asarray(t, dtype=float) for t in ln.get_data())
        sig[("line", to_hex(ln.get_color()), str(ln.get_linestyle()), round(ln.get_linewidth(), 6), str(ln.get_marker()),
             round(ln.get_markersize(), 6), str(ln.get_markerfacecolor()), _r(x), _r(y))] += 1
    for coll in ax.collections:
        kind = type(coll).__name__
        if kind == "PathCollection":
            sig[("scatter", _r(coll.get_offsets()), _r(coll.get_sizes()), _r(coll.get_facecolors()),
                 _r(coll.get_edgecolors()), len(coll.get_paths()))] += 1
        else:
            sig[(kind, tuple(_r(s) for s in coll.get_segments()) if hasattr(coll, "get_segments") else None,
                 _r(coll.get_colors()) if hasattr(coll, "get_colors") else None)] += 1
    for p in ax.patches:
        if p is ax.patch:
            continue
        sig[("patch", type(p).__name__, _r(p.get_path().vertices), _r(p.get_facecolor()))] += 1
    return sig


def source_axes():
    """Rebuild the paper's Figure 2 in memory with the source renderer; its PDF goes to a temporary directory."""
    captured = []
    real_close, real_fig = paper.plt.close, paper.FIG
    with tempfile.TemporaryDirectory() as tmp:
        paper.FIG = Path(tmp)
        paper.plt.close = lambda fig=None: captured.append(fig)
        try:
            paper.figure2()
        finally:
            paper.plt.close, paper.FIG = real_close, real_fig
    fig = captured[0]
    a, b = fig.axes[:2]
    return fig, a, b


def rows_plotted(d: dict, a, b) -> None:
    """Every accepted row, certificate and mixed support appears among the plotted points of its panel."""
    def pts(ax):
        s = set()
        for coll in ax.collections:
            if type(coll).__name__ == "PathCollection":
                s |= {tuple(np.round(p, 12)) for p in np.asarray(coll.get_offsets(), dtype=float)}
        for ln in ax.lines:
            x, y = (np.asarray(t, dtype=float) for t in ln.get_data())
            s |= {(round(float(u), 12), round(float(w), 12)) for u, w in zip(x, y) if np.isfinite(u) and np.isfinite(w)}
        return s
    pa, pb = pts(a), pts(b)
    for row in d["acc"]:
        if (round(float(row["r"]), 12), round(float(row["E"]), 12)) not in pa:
            raise ValueError(f"panel (a) misses accepted row {row['candidate_id']}")
        if row["q_H"] != "mixed":
            key = "v" if row["branch"] == "asymmetric" else "q_H"
            if (round(float(row["r"]), 12), round(abs(float(row[key])), 12)) not in pb:
                raise ValueError(f"panel (b) misses accepted row {row['candidate_id']}")
    for c in d["certs"]:
        ya = (float(c["E_lower"]) + float(c["E_upper"])) / 2
        yb = (float(c["v_lower"]) + float(c["v_upper"])) / 2
        if (round(float(c["r"]), 12), round(ya, 12)) not in pa or (round(float(c["r"]), 12), round(yb, 12)) not in pb:
            raise ValueError(f"certificate at r={c['r']} not plotted")
    for sup in d["supports"].values():
        for s in sup:
            if (round(float(s["r"]), 12), round(abs(float(s["q"])), 12)) not in pb:
                raise ValueError("mixed support not plotted")


def preserve(d: dict, a_talk, b_talk) -> str:
    src_fig, a_src, b_src = source_axes()
    report = []
    for name, talk, src in (("(a)", a_talk, a_src), ("(b)", b_talk, b_src)):
        st, ss = signature(talk), signature(src)
        if st != ss:
            missing, extra = ss - st, st - ss
            raise ValueError(f"panel {name}: data artists differ from the source; missing {len(missing)}, extra {len(extra)}")
        report.append(f"panel {name}: {sum(ss.values())} data artists identical to source "
                      f"({sum(1 for k in ss if k[0] == 'line')} lines, {sum(1 for k in ss if k[0] == 'scatter')} scatter sets, "
                      f"{sum(1 for k in ss if k[0] == 'patch')} shaded spans, "
                      f"{sum(1 for k in ss if k[0] not in ('line', 'scatter', 'patch'))} bar/tick collections)")
    plt.close(src_fig)
    rows_plotted(d, a_talk, b_talk)
    report.append(f"accepted rows {len(d['acc'])} ({dict(Counter(r['branch'] for r in d['acc']))}), "
                  f"certificates {len(d['certs'])}, mixed supports {sum(len(s) for s in d['supports'].values())}: all plotted")
    return "\n".join(report)


def save(fig, stem: str) -> None:
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"{stem}.{ext}", facecolor="white")


def main() -> int:
    d = load()
    check_registry(d)
    plt.rcParams.update(TALK_RC)
    fig_a, a, key_a = draw_entry(d)
    fig_b, b, key_b = draw_orders(d)
    save(fig_a, "equilibrium_correspondence_a_talk")
    save(fig_b, "equilibrium_correspondence_b_talk")
    print(preserve(d, a, b))
    probs = [f"(a) {p}" for p in layout_problems(fig_a, a, key_a)] + [f"(b) {p}" for p in layout_problems(fig_b, b, key_b)]
    for p in probs:
        print("LAYOUT", p)
    plt.close(fig_a)
    plt.close(fig_b)
    for stem in ("equilibrium_correspondence_a_talk", "equilibrium_correspondence_b_talk"):
        for ext in ("pdf", "svg", "png"):
            print(OUT / f"{stem}.{ext}")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
