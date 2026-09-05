"""Figures 1 to 4 from the validated CSV outputs. Renderers never solve, alter parameters, or drop a branch."""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv  # noqa: E402
from numerics.render.style import (DASHED, DOTTED, FULL_WIDTH, GRAY, INK, MUTED, NAVY, RUST, SOLID, TINT_A,  # noqa: E402
                                   TINT_B, TINT_C, label_line, panel_label, plt, region_label)

FIG = ROOT / "figures"


def _f(x: str) -> float:
    try:
        return float(x)
    except ValueError:
        return float("nan")


def _broken_series(rows: list[dict], xkey: str, ykey: str, gap: float, jump: float = 0.02) -> tuple[np.ndarray, np.ndarray]:
    """Sort by x and insert NaN where consecutive accepted nodes are farther apart than `gap` or the value jumps."""
    pts = sorted(((float(Decimal(r[xkey])), _f(r[ykey])) for r in rows), key=lambda t: t[0])
    xs, ys = [], []
    for i, (x, y) in enumerate(pts):
        if i and (x - pts[i - 1][0] > gap * 1.5 or abs(y - pts[i - 1][1]) > jump):
            xs.append(np.nan)
            ys.append(np.nan)
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def _at(xs: np.ndarray, ys: np.ndarray, x0: float) -> tuple[float, float]:
    """Point on a (possibly broken) series nearest to x0, used to anchor direct labels."""
    ok = ~np.isnan(ys)
    i = int(np.argmin(np.abs(xs[ok] - x0)))
    return float(xs[ok][i]), float(ys[ok][i])


def figure2() -> Path:
    rows = read_csv("numerics/correspondence.csv")
    certs = [c for c in read_csv("numerics/certificates.csv") if c["accepted"] == "true"]
    th = {r["boundary"]: float(r["value"]) for r in read_csv("numerics/thresholds.csv") if r["value"] not in ("nan", "n/a")}
    acc = [r for r in rows if r["accepted"] == "true"]
    rmin, rmax = 1.0, 3.8
    fig, (a, b) = plt.subplots(2, 1, figsize=(FULL_WIDTH, 5.2), sharex=True, constrained_layout=True,
                               gridspec_kw={"height_ratios": [1.15, 1.0]})
    # regions: analytical uniqueness tints and the multiplicity window found in the data
    multi = sorted(float(Decimal(r["r"])) for r in acc if r["multiplicity_found"] == "true")
    for ax in (a, b):
        ax.axvspan(rmin, th["pooling_unique_sufficient"], color=TINT_A, lw=0, zorder=0)
        ax.axvspan(th["full_orders_unique_sufficient"], rmax, color=TINT_B, lw=0, zorder=0)
        if multi:
            ax.axvspan(min(multi), max(multi), color=TINT_C, lw=0, zorder=0)
        for key in ("pooling_existence", "full_orders_unique_sufficient", "high_cost_ceiling"):
            ax.axvline(th[key], color=MUTED, lw=0.7, ls=DOTTED, zorder=1)
        ax.set_xlim(rmin, rmax)
    # threshold names on a secondary top axis of the upper panel, never inside the data area
    top = a.secondary_xaxis("top")
    top.set_xticks([th["pooling_existence"], th["full_orders_unique_sufficient"], th["high_cost_ceiling"]])
    top.set_xticklabels([r"$r_N$", r"$r_U$", r"$r_C$"], fontsize=9)
    top.tick_params(length=3, color=MUTED)
    top.spines["top"].set_visible(False)

    series = {
        "pooling": (NAVY, SOLID, 1.6), "full_orders": (RUST, SOLID, 1.6),
        "asymmetric": (NAVY, DASHED, 1.6), "symmetric_interior": (GRAY, DOTTED, 2.0),
        "pure": (GRAY, SOLID, 1.2), "mixed": (GRAY, DASHED, 1.2),
    }
    kept = {}
    for br, (col, ls, lw) in series.items():
        sub = [r for r in acc if r["branch"] == br]
        if not sub:
            continue
        x, y = _broken_series(sub, "r", "E", 0.005)
        a.plot(x, y, color=col, ls=ls, lw=lw, zorder=3 if br != "symmetric_interior" else 4)
        kept[br] = sub
    # certified equilibria: black markers with interval bars, kept even where the bars are tiny
    if certs:
        cx = np.array([float(c["r"]) for c in certs])
        eL = np.array([float(c["E_lower"]) for c in certs])
        eU = np.array([float(c["E_upper"]) for c in certs])
        vL = np.array([float(c["v_lower"]) for c in certs])
        vU = np.array([float(c["v_upper"]) for c in certs])
        a.errorbar(cx, (eL + eU) / 2, yerr=(eU - eL) / 2, fmt="o", ms=4.5, color=INK, ecolor=INK, elinewidth=0.8, capsize=3, zorder=5)
        b.errorbar(cx, (vL + vU) / 2, yerr=(vU - vL) / 2, fmt="o", ms=4.5, color=INK, ecolor=INK, elinewidth=0.8, capsize=3, zorder=5)
    # direct labels, upper panel
    if "pooling" in kept:
        x, y = _at(*_broken_series(kept["pooling"], "r", "E", 0.005), 1.30)
        label_line(a, x, y, "no trade", NAVY, dx=0, dy=5, ha="center")
    if "full_orders" in kept:
        xs, ys = _broken_series(kept["full_orders"], "r", "E", 0.005)
        x, y = _at(xs, ys, 2.5)
        label_line(a, x, y, "full orders", RUST, dx=0, dy=6, ha="center")
        x, y = _at(xs, ys, 3.72)
        label_line(a, x, y, "full orders,\nno expensive entry", RUST, dx=0, dy=6, ha="center")
    if "asymmetric" in kept:
        x, y = _at(*_broken_series(kept["asymmetric"], "r", "E", 0.005), 1.60)
        label_line(a, x, y, "asymmetric orders\n$(1,-v)$", NAVY, dx=0, dy=-14, ha="center", va="top")
    if "symmetric_interior" in kept:
        xs, ys = _broken_series(kept["symmetric_interior"], "r", "E", 0.005)
        x, y = _at(xs, ys, 1.834)
        label_line(a, x, y, "symmetric interior orders $(u,-u)$", GRAY, dx=6, dy=0, ha="left", va="center")
    if certs:
        label_line(a, float(cx[1]), float(eU[1]), "certified equilibria", INK, dx=0, dy=9, ha="center", va="bottom")
    a.set_ylabel(r"total entry $\mathsf{E}$")
    a.set_ylim(0.12, 0.60)
    a.set_yticks([0.25, 0.35, 0.45, 0.55])
    a.text(rmin + 0.012, 0.03, "no trade\nunique", transform=a.get_xaxis_transform(), ha="left", va="bottom", fontsize=8,
           color=MUTED, linespacing=1.1)
    region_label(a, (th["full_orders_unique_sufficient"] + rmax) / 2, "full orders unique")
    if multi:
        region_label(a, (min(multi) + max(multi)) / 2, "several\nequilibria")

    # lower panel: order magnitudes along the informative branches
    if "pooling" in kept:
        x, y = _broken_series(kept["pooling"], "r", "q_H", 0.005)
        b.plot(x, y, color=NAVY, ls=SOLID, lw=1.6, zorder=3)
        label_line(b, 1.30, 0.0, "no trade ($q=0$)", NAVY, dx=0, dy=5, ha="center")
    if "full_orders" in kept:
        x, y = _broken_series(kept["full_orders"], "r", "q_H", 0.005)
        b.plot(x, y, color=RUST, ls=SOLID, lw=1.6, zorder=3)
        label_line(b, 2.9, 1.0, "full orders ($v=1$)", RUST, dx=0, dy=5, ha="center")
    if "asymmetric" in kept:
        xv, yv = _broken_series(kept["asymmetric"], "r", "v", 0.005, jump=0.2)
        b.plot(xv, yv, color=NAVY, ls=DASHED, lw=1.6, zorder=3)
        x, y = _at(xv, yv, 1.60)
        label_line(b, x, y, "$v$, asymmetric", NAVY, dx=-8, dy=0, ha="right", va="center")
    if "symmetric_interior" in kept:
        xu, yu = _broken_series(kept["symmetric_interior"], "r", "q_H", 0.005, jump=0.2)
        b.plot(xu, yu, color=GRAY, ls=DOTTED, lw=2.0, zorder=3)
        x, y = _at(xu, yu, 1.80)
        label_line(b, x, y, "$u$, symmetric interior", GRAY, dx=8, dy=-2, ha="left", va="top")
    b.set_ylabel("order magnitude")
    b.set_ylim(-0.05, 1.12)
    b.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    b.set_xlabel(r"incumbent strength $r$")
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "equilibrium_correspondence.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def figure1() -> Path:
    rows = read_csv("figures_data/two_returns.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL_WIDTH, 2.9), constrained_layout=True)
    mus = sorted({r["mu"] for r in rows}, key=float)
    d = [r for r in rows if r["mu"] == mus[0]]
    x = np.array([float(r["r"]) for r in d])
    a.plot(x, [float(r["Delta_T"]) for r in d], color=NAVY, ls=SOLID)
    a.set_ylabel(r"information spread $\Delta_T(r)$")
    styles = {mus[2]: (NAVY, SOLID, r"$\mu = M$"), mus[1]: (RUST, DASHED, r"$\mu = 1/2$"), mus[0]: (GRAY, DOTTED, r"$\mu = m$")}
    for mu, (col, ls, lab) in styles.items():
        d = [r for r in rows if r["mu"] == mu]
        xs = np.array([float(r["r"]) for r in d])
        ys = np.array([float(r["B_r(mu)"]) for r in d])
        b.plot(xs, ys, color=col, ls=ls, lw=2.0 if ls == DOTTED else 1.6)
        label_line(b, float(xs[-1]), float(ys[-1]), lab, col, dx=-2, dy=5, ha="right")
    b.set_ylabel(r"challenger gross profit $B_r(\mu)$")
    for ax in (a, b):
        ax.set_xlabel(r"incumbent strength $r$")
        ax.set_xlim(1.0, 3.8)
        ax.set_xticks([1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    a.set_ylim(0, 1.1)
    b.set_ylim(1.5, 7.5)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "two_returns.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def figure3() -> Path:
    rows = read_csv("figures_data/posterior_tails.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL_WIDTH, 2.9), constrained_layout=True)
    styles = {"Laplace": (NAVY, SOLID), "logistic": (RUST, DASHED)}
    for noise, (col, ls) in styles.items():
        sub = sorted([r for r in rows if r["noise"] == noise and r["tau_label"] == "grid"], key=lambda r: float(r["M_minus_tau"]))
        x = np.array([float(r["M_minus_tau"]) for r in sub])
        mass = np.array([float(r["posterior_upper_tail_mass"]) for r in sub])
        E = np.array([float(r["E"]) for r in sub])
        interior = x > 0
        a.plot(x[interior], mass[interior], color=col, ls=ls)
        b.plot(x[interior], E[interior], color=col, ls=ls)
        end = [r for r in sub if float(r["M_minus_tau"]) == 0.0]
        if end:
            mk = dict(marker="o", ms=5.5, color=col, mfc=col if noise == "Laplace" else "white", mew=1.4, ls="none", zorder=5)
            a.plot([0.0], [float(end[0]["posterior_upper_tail_mass"])], **mk)
            b.plot([0.0], [float(end[0]["E"])], **mk)
        # direct labels away from the right end, where the two laws meet
        i = int(np.argmin(np.abs(x - (0.06 if noise == "Laplace" else 0.10))))
        if noise == "Laplace":
            label_line(a, float(x[i]), float(mass[i]), "Laplace", col, dx=0, dy=6, ha="center")
            label_line(b, float(x[i]), float(E[i]), "Laplace", col, dx=0, dy=6, ha="center")
        else:
            label_line(a, float(x[i]), float(mass[i]), "logistic", col, dx=7, dy=-9, ha="left", va="top")
            label_line(b, float(x[i]), float(E[i]), "logistic", col, dx=7, dy=-9, ha="left", va="top")
    a.set_ylabel(r"$\Pr(\mu_X \geq \tau)$ under full orders")
    b.set_ylabel(r"total entry $\mathsf{E}$")
    for ax in (a, b):
        ax.set_xlabel(r"threshold distance $M - \tau$")
        ax.set_xlim(-0.01, 0.24)
        ax.set_xticks([0, 0.05, 0.10, 0.15, 0.20])
    a.set_ylim(-0.02, 0.55)
    b.set_ylim(0.22, 0.66)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "posterior_tail_entry.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def figure4() -> Path:
    rows = [r for r in read_csv("figures_data/bargaining.csv") if r["eta"] != "1"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL_WIDTH, 2.9), constrained_layout=True)
    strengths = sorted({r["r"] for r in rows}, key=float)
    styles = {strengths[0]: (NAVY, "weak"), strengths[1]: (RUST, "strong")}
    for rs, (col, name) in styles.items():
        sub = sorted([r for r in rows if r["r"] == rs], key=lambda r: float(r["eta"]))
        eta = np.array([float(r["eta"]) for r in sub])
        D = np.array([float(r["Delta_eta"]) for r in sub])
        GH = np.array([float(r["G_H_eta"]) for r in sub])
        GL = np.array([float(r["G_L_eta"]) for r in sub])
        a.plot(eta, D, color=col, ls=SOLID if name == "weak" else DASHED)
        b.plot(eta, GH, color=col, ls=SOLID)
        b.plot(eta, GL, color=col, ls=DASHED)
        i30 = int(np.argmin(np.abs(eta - 0.55)))
        i05 = int(np.argmin(np.abs(eta - 0.05)))
        if name == "weak":
            label_line(a, float(eta[i30]), float(D[i30]), f"weak incumbent\n($r={rs}$)", col, dx=4, dy=-8, ha="left", va="top")
            label_line(b, float(eta[i05]), float(GH[i05]), "$G_{H,\\eta}$, weak", col, dx=0, dy=8, ha="left", va="bottom")
            label_line(b, float(eta[i05]), float(GL[i05]), "$G_{L,\\eta}$, weak", col, dx=0, dy=8, ha="left", va="bottom")
        else:
            label_line(a, float(eta[i05]), float(D[i05]), f"strong incumbent\n($r={rs}$)", col, dx=0, dy=40, ha="left", va="bottom")
            label_line(b, float(eta[i05]), float(GH[i05]), "$G_{H,\\eta}$, strong", col, dx=0, dy=-12, ha="left", va="top")
            label_line(b, float(eta[i05]), float(GL[i05]), "$G_{L,\\eta}$, strong", col, dx=0, dy=-10, ha="left", va="top")
    for ax in (a, b):
        ax.axvline(0.5, color=MUTED, lw=0.7, ls=DOTTED)
        ax.set_xlabel(r"seller bargaining weight $\eta$")
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    a.text(0.5, 0.02, r"$\eta = 1/2$", transform=a.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=MUTED)
    b.text(0.5, 0.02, r"$\eta = 1/2$", transform=b.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=MUTED)
    a.set_ylabel(r"information spread $\Delta_\eta$")
    a.set_ylim(0, 10.5)
    b.set_ylabel(r"challenger profit $G_{\theta,\eta}$")
    b.set_yscale("log")
    b.set_ylim(3e-3, 60)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "bargaining_weight.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def render_all() -> list[Path]:
    FIG.mkdir(exist_ok=True)
    out = [figure1()]
    if (ROOT / "numerics/correspondence.csv").exists():
        out.append(figure2())
    out.extend([figure3(), figure4()])
    return out


if __name__ == "__main__":
    for p in render_all():
        print(p)
