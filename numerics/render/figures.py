"""Figures 1 to 4 from the validated CSV outputs. Renderers never solve, alter parameters, or drop a branch."""
from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv  # noqa: E402
from numerics.render.style import INK, MUTED, REGION_A, REGION_B, SERIES, panel_label, plt  # noqa: E402

FIG = ROOT / "figures"


def _f(x: str) -> float:
    try:
        return float(x)
    except ValueError:
        return float("nan")


def _broken_series(rows: list[dict], xkey: str, ykey: str, gap: float, jump: float = 0.02) -> tuple[np.ndarray, np.ndarray]:
    """Sort by x and insert NaN where consecutive accepted nodes are farther apart than `gap` or the value jumps (line breaks)."""
    pts = sorted(((float(Decimal(r[xkey])), _f(r[ykey])) for r in rows), key=lambda t: t[0])
    xs, ys = [], []
    for i, (x, y) in enumerate(pts):
        if i and (x - pts[i - 1][0] > gap * 1.5 or abs(y - pts[i - 1][1]) > jump):
            xs.append(np.nan)
            ys.append(np.nan)
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def figure1() -> Path:
    rows = read_csv("numerics/correspondence.csv")
    certs = read_csv("numerics/certificates.csv")
    th = {r["boundary"]: float(r["value"]) for r in read_csv("numerics/thresholds.csv") if r["value"] not in ("nan", "n/a")}
    acc = [r for r in rows if r["accepted"] == "true"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)
    rmin, rmax = 1.0, 3.8
    for ax in (a, b):
        ax.axvspan(rmin, th["pooling_unique_sufficient"], color=REGION_A, lw=0, zorder=0)
        ax.axvspan(th["full_orders_unique_sufficient"], rmax, color=REGION_B, lw=0, zorder=0)
        for key, lab in (("pooling_existence", r"$r_N$"), ("full_orders_unique_sufficient", r"$r_U$"), ("high_cost_ceiling", r"$r_C$")):
            ax.axvline(th[key], color=MUTED, lw=0.6, ls=(0, (3, 2)), zorder=1)
            ax.text(th[key], 1.0, lab, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=MUTED)
        ax.set_xlim(rmin, rmax)
        ax.set_xlabel(r"incumbent strength $r$")
    branches = [("pooling", SERIES[0], "pooling (no trade)", "-"), ("full_orders", SERIES[1], "full orders", "-"),
                ("asymmetric", SERIES[2], "asymmetric $(1,-v)$, numerical continuation", "-"),
                ("symmetric_interior", SERIES[3], "symmetric interior $(u,-u)$, entry $\\rho$", (0, (4, 2))),
                ("pure", SERIES[4], "other pure profiles found", "-"), ("mixed", SERIES[4], "mixed profiles found", (0, (1, 2)))]
    for br, col, lab, ls in branches:
        sub = [r for r in acc if r["branch"] == br]
        if not sub:
            continue
        x, y = _broken_series(sub, "r", "E", 0.005)
        a.plot(x, y, color=col, label=lab, ls=ls, zorder=3 if br != "symmetric_interior" else 4)
        if br == "asymmetric":
            xv, yv = _broken_series(sub, "r", "v", 0.005, jump=0.2)
            b.plot(xv, yv, color=col, label=lab, zorder=3)
        if br == "symmetric_interior":
            xv, yv = _broken_series(sub, "r", "q_H", 0.005, jump=0.2)
            b.plot(xv, yv, color=col, ls=ls, label="symmetric interior magnitude $u$", zorder=3)
    # certified points with interval bars (kept even where visually small)
    cx = [float(c["r"]) for c in certs if c["accepted"] == "true"]
    if cx:
        eL = np.array([float(c["E_lower"]) for c in certs if c["accepted"] == "true"])
        eU = np.array([float(c["E_upper"]) for c in certs if c["accepted"] == "true"])
        vL = np.array([float(c["v_lower"]) for c in certs if c["accepted"] == "true"])
        vU = np.array([float(c["v_upper"]) for c in certs if c["accepted"] == "true"])
        a.errorbar(cx, (eL + eU) / 2, yerr=(eU - eL) / 2, fmt="o", ms=4, color=INK, ecolor=INK, elinewidth=0.8, capsize=3,
                   label="certified asymmetric equilibria (interval enclosures)", zorder=4)
        b.errorbar(cx, (vL + vU) / 2, yerr=(vU - vL) / 2, fmt="o", ms=4, color=INK, ecolor=INK, elinewidth=0.8, capsize=3, zorder=4)
    b.axhline(1.0, color=SERIES[1], lw=1.0, ls="-", zorder=2, label="full orders ($v=1$) boundary")
    a.set_ylabel(r"total entry $\mathsf{E}$")
    b.set_ylabel(r"unfavorable-state order magnitude $v$")
    b.set_ylim(0, 1.05)
    a.legend(loc="center right", fontsize=6.5)
    b.legend(loc="center right", fontsize=6.5)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "equilibrium_correspondence.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def figure2() -> Path:
    rows = read_csv("figures_data/two_returns.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8), constrained_layout=True)
    mus = sorted({r["mu"] for r in rows}, key=float)
    d = [r for r in rows if r["mu"] == mus[0]]
    x = np.array([float(r["r"]) for r in d])
    a.plot(x, [float(r["Delta_T"]) for r in d], color=SERIES[0])
    a.set_ylabel(r"information spread $\Delta_T(r)$")
    labels = {mus[0]: r"$\mu=m$", mus[1]: r"$\mu=1/2$", mus[2]: r"$\mu=M$"}
    for i, mu in enumerate(mus):
        d = [r for r in rows if r["mu"] == mu]
        b.plot([float(r["r"]) for r in d], [float(r["B_r(mu)"]) for r in d], color=SERIES[i], label=labels[mu])
    b.set_ylabel(r"challenger gross profit $B_r(\mu)$")
    b.legend(loc="center right")
    for ax in (a, b):
        ax.set_xlabel(r"incumbent strength $r$")
        ax.set_xlim(x.min(), x.max())
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "two_returns.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def figure3() -> Path:
    rows = read_csv("figures_data/posterior_tails.csv")
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8), constrained_layout=True)
    for i, noise in enumerate(("Laplace", "logistic")):
        sub = sorted([r for r in rows if r["noise"] == noise and r["tau_label"] == "grid"], key=lambda r: float(r["M_minus_tau"]))
        x = np.array([float(r["M_minus_tau"]) for r in sub])
        mass = np.array([float(r["posterior_upper_tail_mass"]) for r in sub])
        E = np.array([float(r["E"]) for r in sub])
        aH = np.array([float(r["alpha_H"]) for r in sub])
        aL = np.array([float(r["alpha_L"]) for r in sub])
        interior = x > 0
        a.plot(x[interior], mass[interior], color=SERIES[i], label=noise)
        b.plot(x[interior], E[interior], color=SERIES[i], label=f"{noise}: entry $\\mathsf{{E}}$")
        b.plot(x[interior], aH[interior], color=SERIES[i], lw=0.9, ls=(0, (4, 2)), label=f"{noise}: $\\alpha_H$")
        b.plot(x[interior], aL[interior], color=SERIES[i], lw=0.9, ls=(0, (1, 2)), label=f"{noise}: $\\alpha_L$")
        # endpoint convention at tau = M
        end = [r for r in sub if float(r["M_minus_tau"]) == 0.0]
        if end:
            a.plot([0.0], [float(end[0]["posterior_upper_tail_mass"])], marker="o" if noise == "Laplace" else "x", color=SERIES[i], ms=5)
            b.plot([0.0], [float(end[0]["E"])], marker="o" if noise == "Laplace" else "x", color=SERIES[i], ms=5)
    a.set_ylabel(r"$\Pr(\mu_X\geq\tau)$ under full orders")
    b.set_ylabel("probability")
    for ax in (a, b):
        ax.set_xlabel(r"threshold distance $M-\tau$")
    a.text(0.02, 0.98, r"at $M-\tau=0$: Laplace plateau enters (tie rule, dot); logistic mass is zero (cross)", transform=a.transAxes,
           ha="left", va="top", fontsize=6.5, color=MUTED)
    a.set_ylim(top=max(a.get_ylim()[1], 0.62))
    a.legend(loc="lower right")
    b.legend(loc="lower right", fontsize=6.5, ncol=2)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "posterior_tail_entry.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def figure4() -> Path:
    rows = [r for r in read_csv("figures_data/bargaining.csv") if r["eta"] != "1"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 2.8), constrained_layout=True)
    strengths = sorted({r["r"] for r in rows}, key=float)
    names = {strengths[0]: f"weak incumbent ($r={strengths[0]}$)", strengths[1]: f"strong incumbent ($r={strengths[1]}$)"}
    for i, rs in enumerate(strengths):
        sub = sorted([r for r in rows if r["r"] == rs], key=lambda r: float(r["eta"]))
        eta = np.array([float(r["eta"]) for r in sub])
        a.plot(eta, [float(r["Delta_eta"]) for r in sub], color=SERIES[i], label=names[rs])
        b.plot(eta, [float(r["G_H_eta"]) for r in sub], color=SERIES[i], label=f"$G_{{H,\\eta}}$, {names[rs]}")
        b.plot(eta, [float(r["G_L_eta"]) for r in sub], color=SERIES[i], ls=(0, (4, 2)), lw=1.0, label=f"$G_{{L,\\eta}}$, {names[rs]}")
    for ax in (a, b):
        ax.axvline(0.5, color=MUTED, lw=0.6, ls=(0, (3, 2)))
        ax.text(0.5, 1.0, r"$\eta=1/2$", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=8, color=MUTED)
        ax.set_xlabel(r"seller bargaining weight $\eta$")
        ax.set_xlim(0, 1)
    a.set_ylabel(r"information spread $\Delta_\eta$")
    b.set_ylabel(r"challenger profit $G_{\theta,\eta}$")
    b.set_yscale("log")
    a.legend(loc="lower right")
    b.legend(loc="lower left", fontsize=6.5)
    panel_label(a, "(a)")
    panel_label(b, "(b)")
    out = FIG / "bargaining_weight.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def render_all() -> list[Path]:
    FIG.mkdir(exist_ok=True)
    out = [figure2(), figure3(), figure4()]
    if (ROOT / "numerics/correspondence.csv").exists():
        out.append(figure1())
    return out


if __name__ == "__main__":
    for p in render_all():
        print(p)
