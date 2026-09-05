"""Tables 1 to 4 as LaTeX threeparttable bodies from the validated CSV outputs.

Each file holds a threeparttable (tabular plus notes) without a caption or table environment;
latex.py wraps it with the caption written in the manuscript. No solving, no parameter changes,
no dropped rows.
"""
from __future__ import annotations

import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv  # noqa: E402

TAB = ROOT / "tables"
MARGIN_KEYS = ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")
SIGNAL_MARGIN_KEYS = ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin")


def d6(x: str) -> str:
    try:
        return format(Decimal(x).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN), "f")
    except Exception:
        return "n/a"


def sci(x: str) -> str:
    try:
        return f"{Decimal(x):.2E}".replace("E", "e")
    except Exception:
        return "n/a"


def esc(s: str) -> str:
    return s.replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def status_word(text: str) -> str:
    t = (text or "").lower()
    if t.startswith("analytical"):
        return "proved"
    if t.startswith("computer-assisted"):
        return "verified computation"
    if "fixed full-order profile" in t or "level-matching" in t:
        return "control"
    if t.startswith("numerical diagnostic"):
        return "illustration"
    if t.startswith("rejected"):
        return "rejected"
    return esc(text.split(" (")[0])


def order(q: str) -> str:
    try:
        v = Decimal(q)
        return format(v.normalize(), "f") if v != v.to_integral() else str(int(v))
    except Exception:
        return esc(q)


def threeparttable(header: list[str], rows: list[list[str]], align: str, notes: list[str], size: str = "") -> str:
    n = len(header)
    lines = [r"\begin{threeparttable}"] + ([size] if size else []) + [f"\\begin{{tabular}}{{{align}}}", r"\toprule", " & ".join(header) + r" \\", r"\midrule"]
    for r in rows:
        if r == ["\\midrule"]:
            lines.append(r"\midrule")
        elif len(r) == 1:
            lines.append(f"\\multicolumn{{{n}}}{{l}}{{\\emph{{{r[0]}}}}} \\\\")
        else:
            lines.append(" & ".join(r) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    if notes:
        lines.append(r"\begin{tablenotes}\footnotesize")
        for note in notes:
            lines.append(f"\\item {note}")
        lines.append(r"\end{tablenotes}")
    lines.append(r"\end{threeparttable}")
    return "\n".join(lines) + "\n"


def table1() -> Path:
    rows = [r for r in read_csv("tables/auction_primitives.csv") if r["parameter_set"] == "base" and r["r"] in ("1.2", "3")]
    weak = next(r for r in rows if r["r"] == "1.2")
    strong = next(r for r in rows if r["r"] == "3")
    body = []
    for key, lab in (("t_0", "Proceeds without a challenger, $t_0$"), ("t_H", "Proceeds with a high-value challenger, $t_H$"),
                     ("t_L", "Proceeds with a low-value challenger, $t_L$"), ("g_H", "Gross profit of a high-value challenger, $g_H$"),
                     ("g_L", "Gross profit of a low-value challenger, $g_L$"), ("Delta_T", r"Information spread, $\Delta_T = t_H - t_L$"),
                     ("B_prior", "Expected gross profit at the prior, $B_r(1/2)$")):
        body.append([lab, d6(weak[key]), d6(strong[key])])
    notes = [r"Benchmark primitives $h=10$, $\ell=1$, $p=0.5$; values per target share. Closed forms in the text agree with "
             r"direct integration of the realized sale rule to within $10^{-9}$ (Online Appendix C.1)."]
    out = TAB / "table1_auction_primitives.tex"
    out.write_text(threeparttable(["", "Weak ($r=1.2$)", "Strong ($r=3$)"], body, "lrr", notes))
    return out


def table2() -> Path:
    eq = read_csv("tables/equilibrium_controls.csv")
    ext = read_csv("tables/extensions.csv")
    fb = read_csv("numerics/feedback_comparisons.csv")
    base = [r for r in eq if r["noise"] == "Laplace" and r["cost_law"] == "atoms" and r["accepted"] == "true"]
    header = ["", "$q_H$", "$q_L$", r"$\mathsf{E}$", r"$\mathsf{O}_H$", r"$\mathcal{R}_T$", "Basis"]
    body = [["Panel A. Equilibrium"]]
    for rs, name in (("1.2", "Weak incumbent"), ("3", "Strong incumbent"), ("3.6", "Very strong incumbent")):
        r = next(x for x in base if x["experiment"] == "feedback" and x["r"] == rs)
        body.append([f"{name} ($r={rs}$)", order(r["q_H"]), order(r["q_L"]), d6(r["E"]), d6(r["O_H"]), d6(r["R_T"]), status_word(r["status"])])
    body.append(["\\midrule"])
    body.append(["Panel B. Information controls"])
    for exp, lab in (("frozen", "Frozen informative orders"), ("price_hidden", "Price hidden from the challenger"), ("matched_dividend", "Matched dividend")):
        for rs in ("1.2", "3"):
            r = next(x for x in base if x["experiment"] == exp and x["r"] == rs)
            body.append([f"{lab}, $r={rs}$", order(r["q_H"]), order(r["q_L"]), d6(r["E"]), d6(r["O_H"]), d6(r["R_T"]), status_word(r["status"])])
    body.append(["\\midrule"])
    body.append(["Panel C. Gains from access to prices at $r=3$"])
    f = next(x for x in fb if x["noise"] == "Laplace" and x["cost_law"] == "atoms" and x["r"] == "3")
    body.append([r"Target proceeds $\mathcal{R}_T$, feedback", "", "", "", "", d6(f["R_T_feedback"]), status_word(f["status"])])
    body.append([r"Target proceeds $\mathcal{R}_T$, price hidden", "", "", "", "", d6(f["R_T_hidden"]), ""])
    body.append([r"Gain in target proceeds", "", "", "", "", d6(f["R_T_gain"]), ""])
    body.append([r"Net acquisition surplus $\mathcal{W}$, feedback", "", "", "", "", d6(f["W_feedback"]), status_word(f["status"])])
    body.append([r"Net acquisition surplus $\mathcal{W}$, price hidden", "", "", "", "", d6(f["W_hidden"]), ""])
    body.append([r"Gain in net acquisition surplus", "", "", "", "", d6(f["W_gain"]), ""])
    e = next(x for x in ext if x["noise"] == "Laplace" and x["cost_law"] == "atoms")
    notes = [
        r"Benchmark primitives, Laplace noise, cost atoms. $\mathsf{E}$ is total entry, $\mathsf{O}_H$ the probability that a high-value challenger "
        r"acquires the target, $\mathcal{R}_T$ expected target proceeds. Basis: proved means the outcome is the unique equilibrium in the analytical "
        r"region; control means a fixed-profile or level-matching calculation that is not an equilibrium claim.",
        r"Panel B: the frozen profile imposes full orders at both strengths and lets the challenger reoptimize; it is not an equilibrium at $r=1.2$. "
        r"The matched dividend adds the feedback-minus-hidden difference in proceeds to the hidden-price claim; residuals, orders, and entry are unchanged.",
        r"Panel C: $\mathcal{W}$ is allocation value net of paid preparation costs, not target revenue. The five strict margins of Proposition 2 at "
        r"$(r_0,r_1)=(1.2,3)$ are $\zeta_L$, $\zeta_{H0}$, $\zeta_{H1}$, $\zeta_0$, $\zeta_1$ = " + ", ".join(sci(e[k]) for k in MARGIN_KEYS) + ".",
    ]
    out = TAB / "table2_equilibrium_controls.tex"
    out.write_text(threeparttable(header, body, "lrrrrrl", notes))
    return out


def table3() -> Path:
    ext = read_csv("tables/extensions.csv")
    mod = read_csv("numerics/moderate_values.csv")
    sig = read_csv("numerics/two_signals.csv")
    header = ["", r"$\mathsf{E}$ weak", r"$\mathsf{E}$ strong", r"$\mathsf{O}_H$ weak", r"$\mathsf{O}_H$ strong", "Min.\\ margin", "Basis"]
    body = [["Panel A. Noise law and preparation-cost law (benchmark, $r_0=1.2$, $r_1=3$)"]]
    for r in ext:
        cost = "cost atoms" if r["cost_law"] == "atoms" else "uniform cost mixture"
        body.append([f"{r['noise']} noise, {cost}", d6(r["E_weak"]), d6(r["E_strong"]), d6(r["O_H_weak"]), d6(r["O_H_strong"]),
                     sci(min((r[k] for k in MARGIN_KEYS), key=lambda v: Decimal(v))), status_word(r["status"])])
    body.append(["\\midrule"])
    body.append(["Panel B. Moderate acquisition values ($h=2$, $\\ell=1$, $r_0=1.05$, $r_1=1.5$)"])
    mrow = mod[0]
    body.append(["Moderate values", d6(mrow["E_weak"]), d6(mrow["E_strong"]), d6(mrow["O_H_weak"]), d6(mrow["O_H_strong"]),
                 sci(min((mrow[k] for k in MARGIN_KEYS), key=lambda v: Decimal(v))), status_word(mrow["status"])])
    body.append(["\\midrule"])
    body.append(["Panel C. Complementary signals ($r_0=1.1$, $r_1=2.3$), by accuracy pair $(a,d)$"])
    acc = [r for r in sig if r["accepted"] == "true"]
    pairs = sorted({(r["a"], r["d"]) for r in acc}, key=lambda t: (Decimal(t[0]), Decimal(t[1])))
    decl = None
    for a, d in pairs:
        w = [r for r in acc if r["a"] == a and r["d"] == d and r["r"] == "1.1"]
        s = [r for r in acc if r["a"] == a and r["d"] == d and r["r"] == "2.3"]
        if len(w) != 1 or len(s) != 1:
            body.append([f"$({a},{d})$", "n/a", "n/a", "n/a", "n/a", "n/a", "several candidates"])
            continue
        w, s = w[0], s[0]
        if (a, d) == ("0.70", "0.75"):
            decl = w
        margin_min = min((w[k] for k in SIGNAL_MARGIN_KEYS), key=lambda v: Decimal(v))
        tag = ", declared example" if (a, d) == ("0.70", "0.75") else ""
        basis = "proved" if s["status"].startswith("analytical") else "outside region"
        body.append([f"$({a},{d})${tag}", d6(w["E"]), d6(s["E"]), d6(w["O_H"]), d6(s["O_H"]), sci(margin_min), basis])
    notes = [
        r"Each row is a separate equilibrium computation at its own primitives; the minimum margin is the smallest of the five strict inequalities "
        r"that the corresponding result requires, so a positive value places the row inside the analytical region.",
        r"Panel A margins $(\zeta_L,\zeta_{H0},\zeta_{H1},\zeta_0,\zeta_1)$ with cost atoms: " + ", ".join(sci(next(x for x in ext if x["cost_law"] == "atoms")[k]) for k in MARGIN_KEYS)
        + r"; with the uniform cost mixture ($\varepsilon_C=0.1$): " + ", ".join(sci(next(x for x in ext if x["cost_law"] != "atoms")[k]) for k in MARGIN_KEYS) + ".",
        r"Panel B margins: " + ", ".join(sci(mrow[k]) for k in MARGIN_KEYS) + ".",
    ]
    if decl is not None:
        notes.append(r"Panel C, declared example: public posterior bounds $[\mu_-,\mu_+]=[" + d6(decl["mu_lower"]) + ", " + d6(decl["mu_upper"])
                     + r"]$, joint posterior bounds $\phi_-(\mu_-)=" + d6(decl["phi_minus_mu_lower"]) + r"$ and $\phi_+(\mu_+)=" + d6(decl["phi_plus_mu_upper"])
                     + r"$; margins " + ", ".join(sci(decl[k]) for k in SIGNAL_MARGIN_KEYS)
                     + r". Basis \emph{outside region}: validated equilibria whose margins are not all positive; the strong-economy "
                     r"outcome is still full orders, and weak-strength entry exceeds $\rho$ when the buyer's favorable private signal alone justifies expensive preparation.")
    out = TAB / "table3_extensions.tex"
    out.write_text(threeparttable(header, body, "lrrrrrl", notes, size=r"\footnotesize"))
    return out


def table4() -> Path:
    comp = read_csv("tables/reserve_comparisons.csv")
    rng = read_csv("numerics/reserve_ranges.csv") if (ROOT / "numerics/reserve_ranges.csv").exists() else []
    header = ["", "$q_H$", "$q_L$", r"$\mathsf{E}$", r"$\mathcal{R}_T$", "Margin", "Basis"]
    body = [["Panel A. Binary values"]]
    for r in comp:
        if r["value_law"] == "binary":
            body.append([f"$r={r['r']}$, reserve $p={r['p']}$", order(r["q_H"]), order(r["q_L"]), d6(r["E"]), d6(r["R_T"]), sci(r["trading_margin"]),
                         status_word(r["status"]) + ("" if r["accepted"] == "true" else " (not accepted)")])
    body.append(["\\midrule"])
    body.append([r"Panel B. Atomless values with class information ($\varepsilon_V=0.05$)"])
    for r in comp:
        if r["value_law"] == "uniform_classes":
            body.append([f"$r={r['r']}$, reserve $p={r['p']}$", order(r["q_H"]), order(r["q_L"]), d6(r["E"]), d6(r["R_T"]), sci(r["trading_margin"]),
                         status_word(r["status"]) + ("" if r["accepted"] == "true" else " (not accepted)")])
    notes = [
        r"Margin: the strict bound supporting the stated continuation, $k-\Delta_T$ for no trade and $(1-1/b)\,e(m)\,m\,\Delta_T-k$ for full orders. "
        r"Basis: proved means the continuation is the unique equilibrium under that bound."]
    if rng:
        body.append(["\\midrule"])
        body.append(["Panel C. Exploratory reserve sweep, highest revenue among continuations found"])
        sweep_notes = []
        for law, lawname in (("binary", "Binary values"), ("uniform_classes", "Class values")):
            for rs in ("1.2", "3"):
                sub = [x for x in rng if x["value_law"] == law and x["r"] == rs]
                if not sub:
                    continue
                found = [x for x in sub if x["accepted_continuations_found"] != "0"]
                best = max(found, key=lambda x: Decimal(x["R_T_max_found"])) if found else None
                n_unres = sum(1 for x in sub if x["search_unresolved"] == "true")
                n_multi = sum(1 for x in sub if int(x["accepted_continuations_found"]) >= 2)
                if best:
                    body.append([f"{lawname}, $r={rs}$, reserve $p={best['p']}$", "", "", d6(best["E_max_found"]), d6(best["R_T_max_found"]), "", "illustration"])
                sweep_notes.append(f"{lawname.lower()} at $r={rs}$: {len(sub)} reserves, {n_multi} with several continuations found, {n_unres} unresolved")
        notes.append(r"Panel C reports, for each economy, the reserve with the highest revenue among the continuations found and the entry there. "
                     r"These are ranges across continuations found, not a global optimum, and an unresolved reserve is not an empty equilibrium set. "
                     r"Sweep coverage: " + "; ".join(sweep_notes) + ". The envelope is not certified (Online Appendix C.6).")
    out = TAB / "table4_reserve_comparisons.tex"
    out.write_text(threeparttable(header, body, "lrrrrrl", notes))
    return out


def render_all() -> list[Path]:
    out = [table1(), table2(), table3()]
    if (ROOT / "tables/reserve_comparisons.csv").exists():
        out.append(table4())
    return out


if __name__ == "__main__":
    for p in render_all():
        print(p)
