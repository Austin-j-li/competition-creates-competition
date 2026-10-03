"""Renderer for the cost-distribution track: reads the solver's CSVs, writes tables.md and cost_regimes.pdf.

It never solves, never changes a parameter, and never drops a branch. Lines break at grid gaps and at jumps,
so no segment implies a node that was not searched.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3]))

from numerics.render.style import (DASHED, DOTTED, FULL_WIDTH, GRAY, INK, MUTED, NAVY, RUST, SOLID,  # noqa: E402
                                   panel_label, plt)

GAP = 0.06
JUMP = 0.05


def read(name: str) -> list[dict]:
    with (HERE / name).open() as fh:
        return list(csv.DictReader(fh))


def num(v: str, digits: int = 4) -> str:
    x = float(v)
    if math.isnan(x):
        return "n/a"
    if math.isinf(x):
        return "+inf" if x > 0 else "-inf"
    return f"{x:.{digits}f}"


def yes(v: str) -> str:
    return "yes" if v.strip().lower() == "true" else "no"


def table(header: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def laws_r3_table() -> str:
    rows = []
    for r in read("laws_r3.csv"):
        rows.append([r["law"], r["regime"], num(r["G_at_B_m"], 3), num(r["G_at_B_half"], 3), num(r["G_at_B_M"], 3),
                     yes(r["dead_exists"]), yes(r["no_trade_exists"]), num(r["pool_prob"], 3), num(r["J"], 4),
                     num(r["E"], 4), num(r["entry_gain_vs_uninformative"], 4), num(r["O_H"], 4),
                     num(r["materiality_min_price"], 3), f"{r['grid_starts_to_live']}/5"])
    return table(["law", "regime", "G(B(m))", "G(B(1/2))", "G(B(M))", "D exists", "no trade exists",
                  "Pr(pool)", "J", "E", "E - G(B(1/2))", "O_H", "min materiality", "starts to live"], rows)


def certificates_table() -> str:
    rows = []
    for r in read("certificates.csv"):
        rows.append([r["law"], r["regime"], r["G_at_B_half_exact"], yes(r["no_trade_exists_exact"]),
                     num(r["J_lower_bound"], 5), num(r["existence_margin_lower"], 5),
                     yes(r["full_order_minimal_pool_certified"]), yes(r["unique_full_certified"]), r["status"]])
    return table(["law", "regime", "G(B(1/2)) exact", "no trade exists", "J lower bound",
                  "(1-1/b)J - k, lower", "full-order equilibrium", "unique full orders", "status"], rows)


def eps_table() -> str:
    rows = []
    for r in read("eps_r3.csv"):
        rows.append([r["eps"], yes(r["dead_exists"]), num(r["z0"], 4), num(r["pool_prob"], 4),
                     num(r["pool_belief"], 4), num(r["J"], 6), num(r["E"], 4), num(r["O_H"], 4),
                     num(r["sufficient_cutoff_end"], 3), num(r["ceiling_strength"], 3),
                     yes(r["grid_full_fixed_point"])])
    return table(["eps", "D exists", "pool end x_-", "Pr(pool)", "pool belief", "J", "E", "O_H",
                  "sufficient cutoff end", "r_C(c - eps)", "grid fixed point"], rows)


def floor_table() -> str:
    rows = []
    for r in read("floor_rho.csv"):
        rows.append([r["rho"], yes(r["no_trade_exists"]), num(r["r_N"], 3), num(r["r_U"], 3),
                     yes(r["unique_full_sufficient"]), num(r["J"], 5), num(r["E"], 4),
                     num(r["E_minus_fork_E"], 4), num(r["sup_price_gap_to_fork"], 4), num(r["pool_prob"], 3)])
    return table(["rho", "no trade exists at r=3", "r_N(rho)", "r_U(rho)", "unique full orders", "J", "E",
                  "E - fork E", "sup price gap", "Pr(pool)"], rows)


def lowest_cost_table() -> str:
    rows = []
    for r in read("lowest_cost_r3.csv"):
        rows.append([num(r["c_low"], 4), num(r["mu_low"], 4), r["regime"], num(r["forced_pool_end"], 3),
                     num(r["largest_consistent_cutoff"], 3), r["selection"],
                     f"[{num(r['limit_cutoffs_low'], 3)}, {num(r['limit_cutoffs_high_sufficient'], 3)}]",
                     yes(r["no_trade_exists"])])
    return table(["lowest added cost c'", "mu'", "regime", "forced pool end", "largest consistent cutoff",
                  "limit set as eta -> 0", "limit cutoffs (sufficient test)", "no trade exists"], rows)


def family_table() -> str:
    rows = []
    fam = read("family_r3.csv")
    for law in ("fork_point_6", "noise_eps_0.5", "two_point_3.5"):
        sub = [r for r in fam if r["law"] == law]
        live = [r for r in sub if r["live"].strip().lower() == "true"]
        incons = [r for r in sub if r["challenger_consistent"].strip().lower() != "true"]
        dead = [r for r in sub if r["fixed_point"].strip().lower() == "true" and r["live"].strip().lower() != "true"]
        rows.append([law, num(sub[0]["cutoff"], 3), num(live[-1]["cutoff"], 3) if live else "n/a",
                     num(live[0]["E"], 4) if live else "n/a", num(live[-1]["E"], 4) if live else "n/a",
                     num(incons[0]["cutoff"], 3) if incons else "none",
                     num(dead[0]["cutoff"], 3) if dead else "none"])
    return table(["law", "first cutoff", "last live cutoff", "E at first", "E at last live",
                  "first inconsistent cutoff", "first cutoff collapsing to D"], rows)


def branch_table() -> str:
    br = read("branches.csv")
    rows = []
    for law in ("fork_point_6", "noise_eps_0.1", "noise_eps_0.5", "uniform_3_9", "uniform_0_12"):
        sub = [r for r in br if r["law"] == law]
        nt = [float(r["r"]) for r in sub if r["branch"] == "no_trade" and r["exists"].strip().lower() == "true"]
        lv = sorted((r for r in sub if r["branch"] == "live"), key=lambda r: float(r["r"]))
        last = lv[-1] if lv else None
        at3 = [r for r in lv if abs(float(r["r"]) - 3.0) < 1e-9]
        e_max = max(lv, key=lambda r: float(r["E"])) if lv else None
        rows.append([law, f"[{min(nt):.2f}, {max(nt):.2f}]" if nt else "none",
                     f"[{float(lv[0]['r']):.2f}, {float(last['r']):.2f}]" if lv else "none",
                     f"{float(e_max['E']):.4f} at {float(e_max['r']):.2f}" if e_max else "n/a",
                     num(at3[0]["E"], 4) if at3 else "n/a", num(last["E"], 4) if last else "n/a",
                     num(at3[0]["O_H"], 4) if at3 else "n/a"])
    return table(["law", "no trade exists on r in", "live found on r in", "max live E", "live E at r=3",
                  "live E at last r", "live O_H at r=3"], rows)


def regime2_table() -> str:
    br = read("branches.csv")
    rows = []
    for r in br:
        if r["law"] == "uniform_3_9" and r["branch"] == "live" and 1.7 <= float(r["r"]) <= 2.3 + 1e-9:
            nt = [x for x in br if x["law"] == "uniform_3_9" and x["branch"] == "no_trade" and x["r"] == r["r"]][0]
            rows.append([num(r["r"], 2), num(r["qH"], 3), num(r["qL"], 3), num(r["pool_prob"], 3), num(r["E"], 4),
                         num(nt["E"], 4), num(r["O_H"], 4), num(r["U_H"], 4), num(r["U_L"], 4)])
    return table(["r", "q_H", "q_L", "Pr(pool)", "E", "G(B(1/2))", "O_H", "U_H", "U_L"], rows)


def ceiling_table() -> str:
    br = read("branches.csv")
    rows = []
    for law in ("fork_point_6", "noise_eps_0.1", "noise_eps_0.5"):
        lv = sorted((r for r in br if r["law"] == law and r["branch"] == "live"), key=lambda r: float(r["r"]))
        if not lv:
            continue
        last = lv[-1]
        rs = sorted({float(r["r"]) for r in br if r["law"] == law})
        nxt = [x for x in rs if x > float(last["r"])]
        rows.append([law, num(last["r"], 4), num(nxt[0], 4) if nxt else "n/a", num(last["E"], 4),
                     num(last["U_H"], 4), num(last["qL"], 3)])
    return table(["law", "last strength with a live fixed point", "next searched strength", "E there",
                  "U_H there", "q_L there"], rows)


def write_tables() -> None:
    parts = ["# Tables for the cost-distribution track", "",
             "Generated by `render.py` from the CSV files in this folder. Do not edit by hand.", "",
             "## T1. Cost laws at r = 3 (closed forms by quadrature; grid checks)", "", laws_r3_table(), "",
             "## T2. Interval certificates at r = 3", "", certificates_table(), "",
             "## T3. Uniform cost noise U[6 - eps, 6 + eps] at r = 3", "", eps_table(), "",
             "## T4. Benchmark floor rho -> 0 at r = 3 (c_L = 1, c_H = 6)", "", floor_table(), "",
             "## T5. Lowest added cost and the limit set of pools at r = 3 (eta = 0.05)", "",
             lowest_cost_table(), "",
             "## T6. Grid cutoff families at r = 3", "", family_table(), "",
             "## T7. Live branches across strengths", "", branch_table(), "",
             "## T8. Regime II example U[3, 9]: pool-free and pooled live equilibria", "", regime2_table(), "",
             "## T9. Where the live branch ends", "", ceiling_table(), ""]
    (HERE / "tables.md").write_text("\n".join(parts))


def broken(points: list[tuple[float, float]]) -> tuple[np.ndarray, np.ndarray]:
    pts = sorted(points)
    xs: list[float] = []
    ys: list[float] = []
    for i, (x, y) in enumerate(pts):
        if i and (x - pts[i - 1][0] > GAP or abs(y - pts[i - 1][1]) > JUMP):
            xs.append(np.nan)
            ys.append(np.nan)
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)


def figure() -> None:
    reg = read("regime_map.csv")
    fork_rows = [r for r in reg if r["law"] == "fork_point_6"]
    r_vals = np.array([float(r["r"]) for r in fork_rows])
    B_m = np.array([float(r["B_m"]) for r in fork_rows])
    B_h = np.array([float(r["B_half"]) for r in fork_rows])
    B_M = np.array([float(r["B_M"]) for r in fork_rows])

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(FULL_WIDTH, 2.9))
    ax_a.fill_between(r_vals, 0.0, B_m, color="#e9edf5", lw=0)
    ax_a.fill_between(r_vals, B_m, B_h, color="#f2f2f2", lw=0)
    ax_a.fill_between(r_vals, B_h, B_M, color="#f6e9e5", lw=0)
    ax_a.plot(r_vals, B_M, color=INK, lw=1.1, ls=DOTTED, label=r"$B_r(M)$")
    ax_a.plot(r_vals, B_h, color=INK, lw=1.1, ls=DASHED, label=r"$B_r(1/2)$")
    ax_a.plot(r_vals, B_m, color=INK, lw=1.1, ls=SOLID, label=r"$B_r(m)$")
    marks = ((6.0, "fork"), (5.5, "U[5.5, 6.5]"), (3.0, "U[3, 9]"), (1.0, r"$c_L$"))
    for c0, _ in marks:
        ax_a.axhline(c0, color=GRAY, lw=0.7, ls=(0, (2, 2)))
    right = ax_a.secondary_yaxis("right")
    right.set_yticks([c0 for c0, _ in marks])
    right.set_yticklabels([lab for _, lab in marks], fontsize=7, color=MUTED)
    right.tick_params(length=0, pad=2)
    for y, lab in ((1.85, "I"), (3.75, "II"), (5.17, "III"), (7.5, "IV")):
        ax_a.text(1.2, y, lab, fontsize=8.5, color=MUTED, ha="center", va="center")
    ax_a.set_xlim(1.0, 4.0)
    ax_a.set_ylim(0.0, 8.2)
    ax_a.set_xlabel(r"incumbent strength $r$")
    ax_a.set_ylabel(r"lowest preparation cost $c_0$")
    ax_a.legend(fontsize=7.5, loc="upper right", handlelength=2.6, borderaxespad=0.2)
    panel_label(ax_a, "(a)")

    br = read("branches.csv")
    styles = (("uniform_0_12", GRAY, SOLID, "U[0, 12]", 2), ("fork_point_6", RUST, SOLID, "fork", 3),
              ("noise_eps_0.1", NAVY, DASHED, r"U[5.9, 6.1]", 4), ("noise_eps_0.5", NAVY, DOTTED, r"U[5.5, 6.5]", 4))
    for law, color, ls, lab, z in styles:
        pts = [(float(r["r"]), float(r["E"])) for r in br if r["law"] == law and r["branch"] == "live"]
        xs, ys = broken(pts)
        ax_b.plot(xs, ys, color=color, ls=ls, lw=1.5, label=lab, zorder=z)
        if law != "uniform_0_12":
            last = max(pts)
            ax_b.plot([last[0]], [last[1]], marker="o", ms=3.5, color=color, zorder=z + 1)
    dead = sorted({float(r["r"]) for r in br if r["law"] == "fork_point_6"})
    ax_b.plot(dead, np.zeros(len(dead)), color=INK, lw=1.0, ls=SOLID, label=r"dead $\mathcal{D}$ (regime III laws)")
    ax_b.set_xlim(1.0, 5.0)
    ax_b.set_ylim(-0.01, 0.45)
    ax_b.set_xlabel(r"incumbent strength $r$")
    ax_b.set_ylabel(r"entry $\mathsf{E}$ on the live branch")
    ax_b.legend(fontsize=7.5, loc="center left", bbox_to_anchor=(0.0, 0.42), handlelength=2.6)
    panel_label(ax_b, "(b)")
    fig.tight_layout(w_pad=2.0)
    fig.savefig(HERE / "cost_regimes.pdf")


def main() -> None:
    write_tables()
    figure()


if __name__ == "__main__":
    main()
