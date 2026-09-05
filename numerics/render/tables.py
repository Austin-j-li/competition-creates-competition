"""Main Tables 1 to 4 and the appendix signal grid from validated CSV outputs.

Main tables hold a threeparttable body; latex.py adds the manuscript caption.
The complete signal grid is a longtable with repeated headers. No numerical solving
or parameter changes; the main summary and full appendix grid use the same accepted rows.
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
        mantissa, exponent = f"{Decimal(x):.2E}".split("E")
        return rf"${mantissa}\times10^{{{int(exponent)}}}$"
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


def tabular(header: list[str], rows: list[list[str]], align: str) -> str:
    n = len(header)
    lines = [rf"\begin{{tabular*}}{{\linewidth}}{{@{{\extracolsep{{\fill}}}}{align}@{{}}}}", r"\toprule", " & ".join(header) + r" \\", r"\midrule"]
    for r in rows:
        if r == ["\\midrule"]:
            lines.append(r"\midrule")
        elif len(r) == 1:
            lines.append(f"\\multicolumn{{{n}}}{{l}}{{\\emph{{{r[0]}}}}} \\\\")
        else:
            lines.append(" & ".join(r) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular*}"]
    return "\n".join(lines)


def threeparttable(header: list[str], rows: list[list[str]], align: str, notes: list[str], size: str = "", extra: str = "") -> str:
    lines = [r"\begin{threeparttable}", r"\setlength{\tabcolsep}{3pt}"] + ([size] if size else [])
    lines += [tabular(header, rows, align)]
    if extra:
        lines += [r"\par\medskip", extra]
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
    out.write_text(threeparttable(["", "Weak ($r=1.2$)", "Strong ($r=3$)"], body, r"p{0.58\linewidth}rr", notes))
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
    f = next(x for x in fb if x["noise"] == "Laplace" and x["cost_law"] == "atoms" and x["r"] == "3")
    welfare = tabular(
        ["", "Price observed", "Price hidden", "Gain"],
        [["Panel C. Access to prices at $r=3$"],
         [r"Target proceeds $\mathcal R_T$", d6(f["R_T_feedback"]), d6(f["R_T_hidden"]), d6(f["R_T_gain"])],
         [r"Net acquisition surplus $\mathcal W$", d6(f["W_feedback"]), d6(f["W_hidden"]), d6(f["W_gain"])]],
        r"p{0.46\linewidth}rrr",
    )
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
    out.write_text(threeparttable(header, body, r"p{0.40\linewidth}rrrrrl", notes, extra=welfare))
    return out


def signal_comparisons() -> list[tuple[dict, dict]]:
    """Pair all declared accuracy combinations at the two incumbent strengths."""
    rows = read_csv("numerics/two_signals.csv")
    pairs = sorted({(r["a"], r["d"]) for r in rows}, key=lambda t: (Decimal(t[0]), Decimal(t[1])))
    result = []
    for a, d in pairs:
        weak = [r for r in rows if (r["a"], r["d"], r["r"]) == (a, d, "1.1") and r["accepted"] == "true"]
        strong = [r for r in rows if (r["a"], r["d"], r["r"]) == (a, d, "2.3") and r["accepted"] == "true"]
        if len(weak) != 1 or len(strong) != 1:
            raise ValueError(f"Signal comparison ({a}, {d}) is not uniquely identified")
        result.append((weak[0], strong[0]))
    return result


def table3() -> Path:
    ext = read_csv("tables/extensions.csv")
    mod = read_csv("numerics/moderate_values.csv")
    header = ["", r"\shortstack{Entry\\weak}", r"\shortstack{Entry\\strong}",
              r"\shortstack{$\mathsf O_H$\\weak}", r"\shortstack{$\mathsf O_H$\\strong}",
              r"\shortstack{Minimum\\margin}", "Basis"]
    body = [["Panel A. Noise and preparation costs"]]
    for row in ext:
        cost = "cost atoms" if row["cost_law"] == "atoms" else "cost mixture"
        body.append([f"{row['noise']}, {cost}", d6(row["E_weak"]), d6(row["E_strong"]),
                     d6(row["O_H_weak"]), d6(row["O_H_strong"]),
                     sci(min((row[k] for k in MARGIN_KEYS), key=Decimal)), status_word(row["status"])])
    body += [["\\midrule"], [r"Panel B. Moderate values ($h=2$, $\ell=1$)"]]
    row = mod[0]
    body.append(["Moderate values", d6(row["E_weak"]), d6(row["E_strong"]),
                 d6(row["O_H_weak"]), d6(row["O_H_strong"]),
                 sci(min((row[k] for k in MARGIN_KEYS), key=Decimal)), status_word(row["status"])])
    weak, strong = next((w, s) for w, s in signal_comparisons() if (w["a"], w["d"]) == ("0.70", "0.75"))
    body += [["\\midrule"], ["Panel C. Complementary private information"]]
    body.append([r"$a=0.70$, $d=0.75$", d6(weak["E"]), d6(strong["E"]),
                 d6(weak["O_H"]), d6(strong["O_H"]),
                 sci(min((weak[k] for k in SIGNAL_MARGIN_KEYS), key=Decimal)), status_word(strong["status"])])
    notes = [
        r"Entry and high-value challenger ownership $\mathsf O_H$ are probabilities. Each row uses its own parameter vector "
        r"from Appendix A.6. Weak and strong strengths are $(1.2,3)$ in Panel A, $(1.05,1.5)$ in Panel B, and $(1.1,2.3)$ in Panel C. "
        r"The cost mixture uses half-width $\varepsilon_C=0.1$; noise laws have the same scale, not the same variance.",
        r"The minimum is taken over the five sufficient inequalities for the relevant result. All displayed rows satisfy them; "
        r"\emph{proved} denotes the corresponding analytical uniqueness region. Panel C has investor accuracy $a$ and buyer accuracy $d$. "
        r"Online Appendix Table 1 reports the complete accuracy grid, including validated outcomes outside that region.",
    ]
    out = TAB / "table3_extensions.tex"
    out.write_text(threeparttable(header, body, r"p{0.24\linewidth}rrrrrl", notes))
    return out


def signal_grid() -> Path:
    pairs = signal_comparisons()
    header = ["Investor $a$", "Buyer $d$", r"\shortstack{Entry\\weak}", r"\shortstack{Entry\\strong}",
              r"\shortstack{$\mathsf O_H$\\weak}", r"\shortstack{$\mathsf O_H$\\strong}",
              r"\shortstack{Minimum\\margin}", "Basis"]
    heading = " & ".join(header) + r" \\"
    lines = [r"\begingroup\singlespacing\setlength{\tabcolsep}{3pt}",
             r"\begin{longtable}{@{\extracolsep{\fill}}rrrrrrrl@{}}",
             r"\caption{Complementary private information: complete accuracy grid.}\label{tab:oa-signals}\\",
             r"\toprule", heading, r"\midrule", r"\endfirsthead",
             r"\caption[]{Complementary private information: complete accuracy grid (continued).}\\",
             r"\toprule", heading, r"\midrule", r"\endhead",
             r"\midrule\multicolumn{8}{r}{\textit{Continued on next page}}\\", r"\endfoot",
             r"\bottomrule", r"\endlastfoot"]
    for weak, strong in pairs:
        margin = min((weak[k] for k in SIGNAL_MARGIN_KEYS), key=Decimal)
        basis = "proved" if strong["status"].startswith("analytical") else "diagnostic"
        mark = r"$^{*}$" if (weak["a"], weak["d"]) == ("0.70", "0.75") else ""
        lines.append(" & ".join([weak["a"] + mark, weak["d"], d6(weak["E"]), d6(strong["E"]),
                                  d6(weak["O_H"]), d6(strong["O_H"]), sci(margin), basis]) + r" \\")
    notes = (r"\textit{Notes.} All accuracy combinations in the declaration in Section C.3 are reported. "
             r"Other parameters are $h=10$, $\ell=1$, $p=0.5$, $\rho=0.85$, $c_L=1$, $c_H=7.14$, $b=2$, $k=0.015$, "
             r"with strengths $r_0=1.1$ and $r_1=2.3$. Entry and $\mathsf O_H$ are probabilities. "
             r"The minimum margin is the smallest of the five conditions in (OA.29). "
             r"\emph{Proved} identifies the analytical uniqueness region; \emph{diagnostic} identifies validated equilibria "
             r"outside those sufficient conditions. A negative margin does not reject an equilibrium. "
             r"The asterisk marks the example used in the main text. All rows pass the declared numerical acceptance checks.")
    lines += [rf"\multicolumn{{8}}{{@{{}}p{{0.97\linewidth}}@{{}}}}{{{notes}}}\\", r"\end{longtable}", r"\endgroup"]
    out = TAB / "table_signal_grid.tex"
    out.write_text("\n".join(lines) + "\n")
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
    sweep = ""
    if rng:
        sweep_body = [["Panel C. Reserve with highest revenue among continuations found"]]
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
                    entry_range = d6(best["E_min_found"]) + "--" + d6(best["E_max_found"])
                    revenue_range = d6(best["R_T_min_found"]) + "--" + d6(best["R_T_max_found"])
                    sweep_body.append([f"{lawname}, $r={rs}$", best["p"], entry_range, revenue_range])
                sweep_notes.append(f"{lawname.lower()} at $r={rs}$: {len(sub)} reserves, {n_multi} with several continuations found, {n_unres} unresolved")
        sweep = tabular(["", "Reserve", "Entry range", "Revenue range"], sweep_body, "lrrr")
        notes.append(r"Panel C selects the reserve with the highest found revenue in each economy, then reports entry and revenue ranges "
                     r"across continuations found at that reserve. Their endpoints need not belong to the same continuation. "
                     r"These are numerical diagnostics, not global optima. Unresolved reserves do not imply empty equilibrium sets. "
                     r"Sweep coverage: " + "; ".join(sweep_notes) + ". The envelope is not certified (Online Appendix C.6).")
    out = TAB / "table4_reserve_comparisons.tex"
    out.write_text(threeparttable(header, body, r"p{0.31\linewidth}rrrrrl", notes, extra=sweep))
    return out


def render_all() -> list[Path]:
    out = [table1(), table2(), table3(), signal_grid()]
    if (ROOT / "tables/reserve_comparisons.csv").exists():
        out.append(table4())
    return out


if __name__ == "__main__":
    for p in render_all():
        print(p)
