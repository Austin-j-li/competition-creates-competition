"""Tables 1 to 4 as LaTeX (booktabs) from the validated CSV outputs. No solving, no parameter changes, no dropped rows."""
from __future__ import annotations

import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv  # noqa: E402

TAB = ROOT / "tables"


def d6(x: str) -> str:
    try:
        return format(Decimal(x).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN), "f")
    except Exception:
        return "n/a"


def sci(x: str) -> str:
    try:
        return f"{Decimal(x):.3E}".replace("E+", "e+").replace("E-", "e-")
    except Exception:
        return "n/a"


def esc(s: str) -> str:
    return s.replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def tabular(header: list[str], rows: list[list[str]], align: str, caption: str, label: str, notes: str = "") -> str:
    lines = [r"\begin{table}[htbp]", r"\centering", r"\small", f"\\caption{{{caption}}}", f"\\label{{{label}}}",
             f"\\begin{{tabular}}{{{align}}}", r"\toprule", " & ".join(header) + r" \\", r"\midrule"]
    for r in rows:
        if r == ["\\midrule"]:
            lines.append(r"\midrule")
        elif len(r) == 1:
            lines.append(f"\\multicolumn{{{len(header)}}}{{l}}{{\\emph{{{r[0]}}}}} \\\\")
        else:
            lines.append(" & ".join(r) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    if notes:
        lines.append(f"\\begin{{minipage}}{{0.95\\linewidth}}\\vspace{{4pt}}\\footnotesize {notes}\\end{{minipage}}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


def table1() -> Path:
    rows = [r for r in read_csv("tables/auction_primitives.csv") if r["parameter_set"] == "base" and r["r"] in ("1.2", "3")]
    weak = next(r for r in rows if r["r"] == "1.2")
    strong = next(r for r in rows if r["r"] == "3")
    body = []
    for key, lab in (("t_0", "$t_0$"), ("t_H", "$t_H$"), ("t_L", "$t_L$"), ("g_H", "$g_H$"), ("g_L", "$g_L$"), ("Delta_T", r"$\Delta_T$"), ("B_prior", "$B_r(1/2)$")):
        body.append([lab, d6(weak[key]), d6(strong[key])])
    cap = (r"Auction primitives at the benchmark specification ($h=10$, $\ell=1$, $p=0.5$), per target share, for the weak ($r=1.2$) and strong ($r=3$) incumbent economies. "
           r"Closed forms in (4), checked against direct integration of the realized sale rule (Online Appendix C.1).")
    tex = tabular(["Quantity", "Weak ($r=1.2$)", "Strong ($r=3$)"], body, "lrr", cap, "tab:auction_primitives")
    out = TAB / "table1_auction_primitives.tex"
    out.write_text(tex)
    return out


def table2() -> Path:
    eq = read_csv("tables/equilibrium_controls.csv")
    ext = read_csv("tables/extensions.csv")
    fb = read_csv("numerics/feedback_comparisons.csv")
    base = [r for r in eq if r["noise"] == "Laplace" and r["cost_law"] == "atoms" and r["accepted"] == "true"]
    body = [["Panel (a): equilibrium at weak, strong, and collapse strengths (Laplace noise, cost atoms)"]]
    for rs in ("1.2", "3", "3.6"):
        r = next(x for x in base if x["experiment"] == "feedback" and x["r"] == rs)
        body.append([f"feedback, $r={rs}$", r["q_H"], r["q_L"], d6(r["E"]), d6(r["O_H"]), d6(r["R_T"]), esc(r["status"].split(" (")[0])])
    e = next(x for x in ext if x["noise"] == "Laplace" and x["cost_law"] == "atoms")
    body.append([r"Theorem 1 margins $(\zeta_L,\zeta_{H0},\zeta_{H1},\zeta_0,\zeta_1)$",
                 r"\multicolumn{6}{l}{" + ", ".join(sci(e[k]) for k in ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")) + "}"])
    body.append(["\\midrule"])
    body.append(["Panel (b): fixed-profile and information controls"])
    for exp, lab in (("frozen", "frozen full orders"), ("price_hidden", "price hidden"), ("matched_dividend", "matched dividend")):
        for rs in ("1.2", "3"):
            r = next(x for x in base if x["experiment"] == exp and x["r"] == rs)
            body.append([f"{lab}, $r={rs}$", r["q_H"], r["q_L"], d6(r["E"]), d6(r["O_H"]), d6(r["R_T"]), esc(r["status"].split(" (")[0])])
    body.append(["\\midrule"])
    body.append(["Panel (c): fixed-strength gains from access to prices ($r=3$)"])
    f = next(x for x in fb if x["noise"] == "Laplace" and x["cost_law"] == "atoms" and x["r"] == "3")
    body.append([r"target proceeds $\mathcal R_T$: feedback / hidden / gain", r"\multicolumn{5}{l}{" + f"{d6(f['R_T_feedback'])} / {d6(f['R_T_hidden'])} / {d6(f['R_T_gain'])}" + "}", esc(f["status"].split(" (")[0])])
    body.append([r"net acquisition surplus $\mathcal W$: feedback / hidden / gain", r"\multicolumn{5}{l}{" + f"{d6(f['W_feedback'])} / {d6(f['W_hidden'])} / {d6(f['W_gain'])}" + "}", esc(f["status"].split(" (")[0])])
    cap = (r"Equilibrium outcomes, information controls, and ownership at the benchmark. Panel (a) reports validated equilibria; panel (b) reports the frozen "
           r"informative profile (a fixed-profile control that is not an equilibrium at $r=1.2$), the reoptimized price-hidden equilibrium, and the level-matching "
           r"dividend diagnostic; panel (c) reports fixed-strength gains from access to prices. $\mathcal W$ is allocation value net of paid preparation costs, not target revenue "
           r"(Online Appendix C.1).")
    tex = tabular(["Experiment", "$q_H$", "$q_L$", r"$\mathsf E$", r"$\mathsf O_H$", r"$\mathcal R_T$", "Status"], body, "lrrrrrl", cap, "tab:equilibrium_controls")
    out = TAB / "table2_equilibrium_controls.tex"
    out.write_text(tex)
    return out


def table3() -> Path:
    ext = read_csv("tables/extensions.csv")
    mod = read_csv("numerics/moderate_values.csv")
    sig = read_csv("numerics/two_signals.csv")
    body = [["Panel (a): noise law crossed with preparation-cost law (benchmark, $r_0=1.2$, $r_1=3$)"]]
    for r in ext:
        body.append([f"{r['noise']}, {esc(r['cost_law'].replace('_', ' '))}", d6(r["E_weak"]), d6(r["E_strong"]), d6(r["O_H_weak"]), d6(r["O_H_strong"]),
                     sci(min((r[k] for k in ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")), key=lambda v: Decimal(v))), esc(r["status"].split(" (")[0])])
    body.append(["\\midrule"])
    body.append(["Panel (b): moderate acquisition values ($h=2$, $\\ell=1$, $r_0=1.05$, $r_1=1.5$)"])
    for r in mod:
        body.append(["moderate values", d6(r["E_weak"]), d6(r["E_strong"]), d6(r["O_H_weak"]), d6(r["O_H_strong"]),
                     sci(min((r[k] for k in ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")), key=lambda v: Decimal(v))), esc(r["status"].split(" (")[0])])
        body.append([r"Theorem 1 margins $(\zeta_L,\zeta_{H0},\zeta_{H1},\zeta_0,\zeta_1)$",
                     r"\multicolumn{6}{l}{" + ", ".join(sci(r[k]) for k in ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")) + "}"])
    body.append(["\\midrule"])
    body.append(["Panel (c): complementary signals ($r_0=1.1$, $r_1=2.3$); rows are accuracy pairs $(a,d)$"])
    acc = [r for r in sig if r["accepted"] == "true"]
    pairs = sorted({(r["a"], r["d"]) for r in acc}, key=lambda t: (Decimal(t[0]), Decimal(t[1])))
    for a, d in pairs:
        w = [r for r in acc if r["a"] == a and r["d"] == d and r["r"] == "1.1"]
        s = [r for r in acc if r["a"] == a and r["d"] == d and r["r"] == "2.3"]
        if len(w) != 1 or len(s) != 1:
            body.append([f"$({a},{d})$", r"\multicolumn{6}{l}{multiple or no accepted candidates at a node; see numerics/two\_signals.csv}"])
            continue
        w, s = w[0], s[0]
        margin_min = min((w[k] for k in ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin")), key=lambda v: Decimal(v))
        tag = "declared example" if (a, d) == ("0.70", "0.75") else ""
        body.append([f"$({a},{d})$ {tag}".strip(), d6(w["E"]), d6(s["E"]), d6(w["O_H"]), d6(s["O_H"]), sci(margin_min),
                     "Theorem R2 region" if s["status"].startswith("analytical") else "outside theorem region (validated candidates)"])
    body.append([r"public and joint posterior bounds at the declared example: $[\mu_-,\mu_+]$, $\phi_-(\mu_-)$, $\phi_+(\mu_+)$",
                 r"\multicolumn{6}{l}{" + ", ".join(d6(next(r for r in acc if r["a"] == "0.70" and r["d"] == "0.75")[k]) for k in ("mu_lower", "mu_upper", "phi_minus_mu_lower", "phi_plus_mu_upper")) + "}"])
    cap = (r"Extensions and information complementarities. Entry $\mathsf E$ and high-quality ownership $\mathsf O_H$ at the weak and strong strengths, with the minimum of the "
           r"five strict theorem margins. Panel (a): Laplace or logistic noise crossed with cost atoms or the uniform cost mixture ($\varepsilon_C=0.1$). Panel (b): the moderate-value "
           r"declaration. Panel (c): complementary-signal economies; each accuracy pair is a separate equilibrium computation, and the theorem region marks pairs for which every "
           r"strict margin of (27) is positive (Online Appendix C.1, C.3, C.4).")
    tex = tabular(["Economy", r"$\mathsf E$ weak", r"$\mathsf E$ strong", r"$\mathsf O_H$ weak", r"$\mathsf O_H$ strong", "min margin", "Status"], body, "lrrrrrl", cap, "tab:extensions")
    out = TAB / "table3_extensions.tex"
    out.write_text(tex)
    return out


def table4() -> Path:
    comp = read_csv("tables/reserve_comparisons.csv")
    rng = read_csv("numerics/reserve_ranges.csv") if (ROOT / "numerics/reserve_ranges.csv").exists() else []
    body = [["Panel (a): binary values, original and alternative reserves"]]
    for r in comp:
        if r["value_law"] == "binary":
            body.append([f"$r={r['r']}$, $p={r['p']}$", r["q_H"], r["q_L"], d6(r["E"]), d6(r["R_T"]), sci(r["trading_margin"]), esc(r["status"].split(" (")[0]) + ("" if r["accepted"] == "true" else " (not accepted)")])
    body.append(["\\midrule"])
    body.append([r"Panel (b): atomless values with class information ($\varepsilon_V=0.05$)"])
    for r in comp:
        if r["value_law"] == "uniform_classes":
            body.append([f"$r={r['r']}$, $p={r['p']}$", r["q_H"], r["q_L"], d6(r["E"]), d6(r["R_T"]), sci(r["trading_margin"]), esc(r["status"].split(" (")[0]) + ("" if r["accepted"] == "true" else " (not accepted)")])
    body.append(["\\midrule"])
    body.append(["Panel (c): exploratory reserve sweep, ranges across continuations found"])
    if rng:
        for law in ("binary", "uniform_classes"):
            for rs in ("1.2", "3"):
                sub = [x for x in rng if x["value_law"] == law and x["r"] == rs]
                if not sub:
                    continue
                found = [x for x in sub if x["accepted_continuations_found"] != "0"]
                best = max(found, key=lambda x: Decimal(x["R_T_max_found"])) if found else None
                n_unres = sum(1 for x in sub if x["search_unresolved"] == "true")
                n_multi = sum(1 for x in sub if int(x["accepted_continuations_found"]) >= 2)
                body.append([f"{esc(law.replace('_', ' '))}, $r={rs}$: {len(sub)} reserves", r"\multicolumn{6}{l}{"
                             + (f"highest found revenue {d6(best['R_T_max_found'])} at $p={best['p']}$, entry there {d6(best['E_min_found'])}--{d6(best['E_max_found'])}" if best else "no accepted continuation")
                             + "}"])
                body.append(["", r"\multicolumn{6}{l}{" + f"{n_multi} reserves with several continuations found; {n_unres} unresolved reserves; envelope not certified" + "}"])
    else:
        body.append([r"\multicolumn{7}{l}{sweep not available}"])
    cap = (r"Sale terms and discovery. Panels (a) and (b) compare the original reserve with the declared alternative at each strength under binary values and under atomless "
           r"class values with class-only investor information; the trading margin is the strict bound supporting the stated continuation. Panel (c) summarizes the exploratory "
           r"reserve sweep as ranges across continuations found; a highest found revenue is not a global optimum, and an unresolved reserve is not an empty equilibrium set "
           r"(Online Appendix C.6).")
    tex = tabular(["Economy", "$q_H$", "$q_L$", r"$\mathsf E$", r"$\mathcal R_T$", "trading margin", "Status"], body, "lrrrrrl", cap, "tab:reserve_comparisons")
    out = TAB / "table4_reserve_comparisons.tex"
    out.write_text(tex)
    return out


def render_all() -> list[Path]:
    out = [table1(), table2(), table3()]
    if (ROOT / "tables/reserve_comparisons.csv").exists():
        out.append(table4())
    return out


if __name__ == "__main__":
    for p in render_all():
        print(p)
