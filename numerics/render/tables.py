"""Main Tables 1 to 4 and the online tables, assembled from validated CSV outputs.

Main tables hold a threeparttable body; latex.py adds the manuscript caption. Online tables
(matched-price panel, extension margins, complete signal grid, reserve details, reserve exploratory
summary) carry their own captions. No numerical solving or parameter changes take place here: every
cell is a validated row value, an exact declared input, or arithmetic on validated values that the
manuscript defines (a difference of two probabilities in percentage points, the matched-price identity),
and every such identity is checked against the source and raises on breach.

Vocabulary (spec 2.2). Evidence is one of analytical, computer-assisted, numerical diagnostic; uniqueness
is a separate field; "control" names an experiment role, never an evidence status. A negative
sufficient-condition margin is "comparison condition not met", never a rejection.
"""
from __future__ import annotations

import re
import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv, write_csv  # noqa: E402
from numerics.params import BENCHMARK, BENCHMARK_EXTRA, BENCHMARK_STRENGTHS, CONTROLS  # noqa: E402

TAB = ROOT / "tables"
MARGIN_KEYS = ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")
SIGNAL_MARGIN_KEYS = ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin")
MARGIN_LABELS = (r"$\zeta_L$", r"$\zeta_{H0}$", r"$\zeta_{H1}$", r"$\zeta_0$", r"$\zeta_1$")
IDENTITY_TOL = Decimal(repr(CONTROLS.independent_formula_acceptance))
RANGE_COLUMNS = ("value_law", "r", "p", "accepted_continuations_found", "E_min_found", "E_max_found", "R_T_min_found", "R_T_max_found",
                 "search_unresolved", "global_envelope_certified", "p_exact", "event_id", "candidates_evaluated", "candidates_accepted_raw",
                 "candidates_rejected", "candidates_unresolved", "duplicates_merged", "search_outcome")
DECLARED_RESERVES = {"binary": ("0.5", BENCHMARK_EXTRA["binary_alternative_reserve"]),
                     "uniform_classes": ("0.5", BENCHMARK_EXTRA["atomless_alternative_reserve"])}
STRENGTH_NAMES = (("r_weak", "Weak incumbent"), ("r_strong", "Strong incumbent"))


# ---------------------------------------------------------------------------------------------
# formatting
# ---------------------------------------------------------------------------------------------
def d6(x: str) -> str:
    if x == "n/a":
        return "n/a"
    if not Decimal(x).is_finite():
        raise ValueError(f"nonfinite table scalar: {x}")
    return format(Decimal(x).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN), "f")


def d2(x: Decimal) -> str:
    if not x.is_finite():
        raise ValueError(f"nonfinite table scalar: {x}")
    return format(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN), "f")


def sci(x: str) -> str:
    if x == "n/a":
        return "n/a"
    if not Decimal(x).is_finite():
        raise ValueError(f"nonfinite table scalar: {x}")
    mantissa, exponent = f"{Decimal(x):.2E}".split("E")
    return rf"${mantissa}\times10^{{{int(exponent)}}}$"


def esc(s: str) -> str:
    return s.replace("_", r"\_").replace("%", r"\%").replace("&", r"\&").replace("|", r"$|$")


def identity_text(s: str) -> str:
    return esc(s).replace(r"\_", r"\_\allowbreak{}").replace(r"$|$", r"$|$\allowbreak{}").replace(";", r";\allowbreak{}")


def evidence(text: str) -> str:
    """Evidence class in the paper's vocabulary. Never returns a role word."""
    t = (text or "").lower()
    if t.startswith("analytical"):
        return "analytical"
    if t.startswith("computer-assisted"):
        return "computer-assisted"
    if t.startswith("numerical diagnostic"):
        return "numerical diagnostic"
    if t.startswith("rejected"):
        return "rejected"
    return "open"


def joint_evidence(*texts: str) -> str:
    classes = {evidence(t) for t in texts}
    if classes == {"analytical"}:
        return "analytical"
    if classes <= {"analytical", "computer-assisted"}:
        return "computer-assisted"
    if "rejected" in classes or "open" in classes:
        return "open"
    return "numerical diagnostic"


def pp_change(strong: str, weak: str) -> Decimal:
    """Change in preparation in percentage points from two validated probabilities (never from rounded text)."""
    return (Decimal(strong) - Decimal(weak)) * 100


def order(q: str) -> str:
    try:
        v = Decimal(q)
        return format(v.normalize(), "f") if v != v.to_integral() else str(int(v))
    except Exception:
        return esc(q)


def trading_outcome(q_H: str, q_L: str) -> str:
    if Decimal(q_H) == 0 and Decimal(q_L) == 0:
        return "no trade"
    if Decimal(q_H) == 1 and Decimal(q_L) == -1:
        return "full orders"
    return f"orders $({order(q_H)},{order(q_L)})$"


def unique_field(text: str) -> str:
    t = (text or "").lower()
    if "unique" in t and "not established" not in t:
        return "yes"
    return "not established"


def one(rows: list[dict], what: str, **keys) -> dict:
    """Exactly one accepted row matching every key (decimal comparison where both sides parse)."""
    def same(a: str, b: str) -> bool:
        try:
            return Decimal(a) == Decimal(b)
        except Exception:
            return a == b
    hits = [r for r in rows if all(same(r.get(k, ""), v) for k, v in keys.items()) and r.get("accepted", "true") == "true"]
    if len(hits) != 1:
        raise ValueError(f"{what}: {len(hits)} accepted rows match {keys}")
    return hits[0]


# ---------------------------------------------------------------------------------------------
# LaTeX assembly
# ---------------------------------------------------------------------------------------------
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


def online_table(caption: str, label: str, body: str, landscape: bool = False) -> str:
    """Online tables carry their own caption (main tables receive theirs from the manuscript marker)."""
    return ((r"\begin{landscape}" + "\n" if landscape else "")
            + r"\begin{table}[tbp]\begingroup\singlespacing\small\centering" + "\n"
            + rf"\caption{{{caption}}}\label{{{label}}}" + "\n" + body + r"\par\endgroup\end{table}" + "\n"
            + (r"\end{landscape}" + "\n" if landscape else ""))


# ---------------------------------------------------------------------------------------------
# Table 1
# ---------------------------------------------------------------------------------------------
def table1() -> Path:
    rows = [r for r in read_csv("tables/auction_primitives.csv") if r["parameter_set"] == "base"]
    weak = one(rows, "Table 1 weak", r=BENCHMARK_STRENGTHS["r_weak"])
    strong = one(rows, "Table 1 strong", r=BENCHMARK_STRENGTHS["r_strong"])
    body = []
    for key, lab in (("t_0", "Proceeds without a challenger, $t_0$"), ("t_H", "Proceeds with a high-value challenger, $t_H$"),
                     ("t_L", "Proceeds with a low-value challenger, $t_L$"), ("g_H", "Gross profit of a high-value challenger, $g_H$"),
                     ("g_L", "Gross profit of a low-value challenger, $g_L$"), ("Delta_T", r"Information spread, $\Delta_T = t_H - t_L$"),
                     ("B_prior", "Expected gross profit at the prior, $B_r(1/2)$")):
        body.append([lab, d6(weak[key]), d6(strong[key])])
    notes = [r"Benchmark primitives $h=10$, $\ell=1$, $p=0.5$; values are incremental value per target share. $\Delta_T$ is the spread in "
             r"expected target proceeds across challenger types, not total merger value and not the trader's expected profit. Closed forms in "
             r"the text agree with direct integration of the realized sale rule to within $10^{-9}$ (Online Appendix C.1)."]
    out = TAB / "table1_auction_primitives.tex"
    out.write_text(threeparttable(["", "Weak ($r=1.2$)", "Strong ($r=3$)"], body, r"p{0.58\linewidth}rr", notes))
    return out


# ---------------------------------------------------------------------------------------------
# Table 2 and the online matched-price panel
# ---------------------------------------------------------------------------------------------
def _benchmark_controls() -> list[dict]:
    eq = read_csv("tables/equilibrium_controls.csv")
    return [r for r in eq if r["parameter_set"] == "base" and r["accepted"] == "true"]


def table2() -> Path:
    base = [r for r in _benchmark_controls() if r["noise"] == "Laplace" and r["cost_law"] == "atoms"]
    ext = read_csv("tables/extensions.csv")
    fb = read_csv("numerics/feedback_comparisons.csv")
    header = ["", "$q_H$", "$q_L$", r"$\mathsf{E}$", r"$\mathsf{O}_H$", r"$\mathcal{R}_T$", "Evidence", "Unique"]
    body = [["Panel A. Equilibrium outcomes"]]
    for key, name in STRENGTH_NAMES + (("r_collapse", "Very strong incumbent"),):
        rs = BENCHMARK_STRENGTHS[key]
        r = one(base, "Table 2 Panel A", experiment="feedback", r=rs)
        body.append([f"{name} ($r={rs}$)", order(r["q_H"]), order(r["q_L"]), d6(r["E"]), d6(r["O_H"]), d6(r["R_T"]),
                     evidence(r["status"]), unique_field(r["status"])])
    body.append(["\\midrule"])
    body.append(["Panel B. Information controls"])
    for exp, lab in (("frozen", "Frozen informative orders"), ("price_hidden", "Price hidden")):
        for key, _ in STRENGTH_NAMES:
            rs = BENCHMARK_STRENGTHS[key]
            r = one(base, "Table 2 Panel B", experiment=exp, r=rs)
            uniq = "n/a" if exp == "frozen" else unique_field(r["status"])
            body.append([f"{lab}, $r={rs}$", order(r["q_H"]), order(r["q_L"]), d6(r["E"]), d6(r["O_H"]), d6(r["R_T"]), evidence(r["status"]), uniq])
    f = one(fb, "Table 2 Panel C", noise="Laplace", cost_law="atoms", r=BENCHMARK_STRENGTHS["r_strong"])
    welfare = tabular(
        ["", "Price observed", "Price hidden", "Gain"],
        [[f"Panel C. Access to prices at $r={BENCHMARK_STRENGTHS['r_strong']}$"],
         [r"Target proceeds $\mathcal R_T$", d6(f["R_T_feedback"]), d6(f["R_T_hidden"]), d6(f["R_T_gain"])],
         [r"Net acquisition surplus $\mathcal W$", d6(f["W_feedback"]), d6(f["W_hidden"]), d6(f["W_gain"])]],
        r"p{0.46\linewidth}rrr",
    )
    e = one(ext, "Table 2 margins", parameter_set="base", noise="Laplace", cost_law="atoms")
    notes = [
        r"Benchmark primitives, Laplace noise, cost atoms. $\mathsf{E}$ is the preparation probability, $\mathsf{O}_H$ the probability that a "
        r"high-value challenger acquires the target, $\mathcal{R}_T$ expected target proceeds. Evidence is the result status of the row "
        r"(analytical, computer-assisted, or numerical diagnostic); Unique records separately whether the continuation is the unique one under "
        r"the stated bound. Panel A rows are analytical outcomes of Proposition 2.",
        r"Panel B rows are information controls: control is an experiment role, not an evidence class. The frozen rows are a fixed-profile "
        r"control that imposes full orders at both strengths and lets the challenger reoptimize; the profile is not an investor equilibrium at "
        r"$r=1.2$ and coincides with the equilibrium profile at $r=3$ while its role remains that of a control, so its Unique field is not "
        r"applicable. The price-hidden rows are the reoptimized equilibria of the economy in which the price is withheld from the challenger. "
        r"The matched-dividend invariance diagnostic of Section 6.1 is reported in the online matched-price panel.",
        r"Panel C: $\mathcal{W}$ is allocation value net of paid preparation costs, not target revenue. The five strict margins of Proposition 2 at "
        r"$(r_0,r_1)=(1.2,3)$ are " + ", ".join(f"{lab} = {sci(e[k])}" for lab, k in zip(MARGIN_LABELS, MARGIN_KEYS)) + ".",
    ]
    out = TAB / "table2_equilibrium_controls.tex"
    out.write_text(threeparttable(header, body, r"p{0.325\linewidth}rrrrrll", notes, extra=welfare))
    return out


def matched_price_panel() -> list[Path]:
    """Online matched-price panel (spec 14.3). The matched control keeps every hidden-environment quantity except the
    mean financial price, which equals the hidden price plus the external dividend D_0. Both identities are checked."""
    rs = BENCHMARK_STRENGTHS["r_strong"]
    fb = read_csv("numerics/feedback_comparisons.csv")
    rows_out = []
    body = []
    env_label = {"feedback": "Price observed (feedback equilibrium)", "price_hidden": "Price hidden (reoptimized equilibrium)",
                 "matched_dividend": "Hidden plus dividend (control)"}
    for noise in ("Laplace", "logistic"):
        for cost in ("atoms", "uniform_mixture"):
            base = [r for r in _benchmark_controls() if r["noise"] == noise and r["cost_law"] == cost]
            fbk = one(base, "matched panel feedback", experiment="feedback", r=rs)
            hid = one(base, "matched panel hidden", experiment="price_hidden", r=rs)
            mat = one(base, "matched panel matched", experiment="matched_dividend", r=rs)
            f = one(fb, "matched panel comparison", noise=noise, cost_law=cost, r=rs)
            d0 = Decimal(mat["matched_dividend"])
            rt_f, rt_h = Decimal(fbk["R_T"]), Decimal(hid["R_T"])
            # identity checks (raise; never patch)
            if abs(d0 - (rt_f - rt_h)) > IDENTITY_TOL:
                raise ValueError(f"matched dividend identity D_0 = R_T^feedback - R_T^hidden fails for {noise}/{cost}: {d0} vs {rt_f - rt_h}")
            if abs(d0 - Decimal(f["matched_dividend"])) > IDENTITY_TOL:
                raise ValueError(f"matched dividend differs between equilibrium_controls and feedback_comparisons for {noise}/{cost}")
            for key in ("revenue_identity_error", "residual_invariance_error"):
                if not Decimal(f[key]).is_finite() or abs(Decimal(f[key])) > IDENTITY_TOL:
                    raise ValueError(f"{key} exceeds tolerance for {noise}/{cost}")
            for k in ("R_T", "W", "E", "O_H", "q_H", "q_L", "e_H", "e_L"):
                if abs(Decimal(mat[k]) - Decimal(hid[k])) > IDENTITY_TOL:
                    raise ValueError(f"matched control changes {k} relative to the hidden environment for {noise}/{cost}")
            mean_p = {"feedback": rt_f, "price_hidden": rt_h, "matched_dividend": rt_h + d0}
            if abs(mean_p["matched_dividend"] - mean_p["feedback"]) > IDENTITY_TOL:
                raise ValueError(f"E[P^matched] != E[P^feedback] for {noise}/{cost}")
            cost_name = "cost atoms" if cost == "atoms" else "cost mixture"
            body.append([f"{noise} noise, {cost_name}, $r={rs}$"])
            for exp, r in (("feedback", fbk), ("price_hidden", hid), ("matched_dividend", mat)):
                rec = {"parameter_set": "base", "noise": noise, "cost_law": cost, "r": rs, "environment": exp,
                       "mean_financial_price": str(mean_p[exp]), "seller_revenue": r["R_T"],
                       "external_dividend": str(d0) if exp == "matched_dividend" else "0",
                       "preparation_probability": r["E"], "high_value_ownership_probability": r["O_H"], "net_acquisition_surplus": r["W"],
                       "role": "equilibrium outcome" if exp != "matched_dividend" else "analytical invariance diagnostic (control)",
                       "status": r["status"], "accepted": r["accepted"]}
                rows_out.append(rec)
                body.append([env_label[exp], d6(rec["mean_financial_price"]), d6(rec["seller_revenue"]), d6(rec["external_dividend"]),
                             d6(rec["preparation_probability"]), d6(rec["high_value_ownership_probability"]), d6(rec["net_acquisition_surplus"])])
            body.append(["\\midrule"])
    body.pop()  # trailing rule
    csv_path = write_csv("tables/matched_price.csv",
                         ["parameter_set", "noise", "cost_law", "r", "environment", "mean_financial_price", "seller_revenue", "external_dividend",
                          "preparation_probability", "high_value_ownership_probability", "net_acquisition_surplus", "role", "status", "accepted"],
                         rows_out)
    header = ["Environment", r"$\mathbb E[P]$", r"$\mathcal R_T$", "$D_0$", r"$\mathsf E$", r"$\mathsf O_H$", r"$\mathcal W$"]
    notes = [
        r"Strong benchmark strength; the four noise and cost-law combinations of Table 3, Panel A. $\mathbb E[P]$ is the mean financial price, "
        r"$\mathcal R_T$ expected target proceeds (seller revenue), $D_0=\mathcal R_T^{\mathrm{feedback}}-\mathcal R_T^{\mathrm{hidden}}$ the "
        r"external dividend, $\mathsf E$ the preparation probability, $\mathsf O_H$ high-value ownership, $\mathcal W$ net acquisition surplus.",
        r"The matched row adds $D_0$ to the traded claim of the price-hidden economy, so $\mathbb E[P^{\mathrm{matched}}]=\mathcal R_T^{\mathrm{hidden}}"
        r"+D_0=\mathbb E[P^{\mathrm{feedback}}]$, while seller revenue, acquisition surplus, preparation, orders, and investor residuals remain those of "
        r"the hidden-price environment; the renderer verifies each identity to within $10^{-9}$. The dividend is attached to the financial claim, "
        r"is not paid by any bidder, and is not a sale term: the matched row is an analytical invariance diagnostic, not an equilibrium of a new game.",
    ]
    tex = online_table("Matched-price panel: information versus price level at the strong strength.", "tab:oa-matched-price",
                       threeparttable(header, body, r"p{0.395\linewidth}rrrrrr", notes))
    out = TAB / "table_matched_price.tex"
    out.write_text(tex)
    return [out, csv_path]


# ---------------------------------------------------------------------------------------------
# Table 3, the online margins table, and the complete signal grid
# ---------------------------------------------------------------------------------------------
def signal_comparisons() -> list[tuple[dict, dict]]:
    """Pair all declared accuracy combinations at the two incumbent strengths (25 pairs, none dropped)."""
    rows = read_csv("numerics/two_signals.csv")
    pairs = sorted({(r["a"], r["d"]) for r in rows}, key=lambda t: (Decimal(t[0]), Decimal(t[1])))
    result = []
    for a, d in pairs:
        weak = [r for r in rows if (r["a"], r["d"], r["r"]) == (a, d, "1.1") and r["accepted"] == "true"]
        strong = [r for r in rows if (r["a"], r["d"], r["r"]) == (a, d, "2.3") and r["accepted"] == "true"]
        if len(weak) != 1 or len(strong) != 1:
            raise ValueError(f"Signal comparison ({a}, {d}) is not uniquely identified")
        result.append((weak[0], strong[0]))
    if len(result) != 25:
        raise ValueError(f"signal grid has {len(result)} comparisons, expected 25")
    return result


def _extension_records() -> list[dict]:
    """The six Table 3 rows with their complete parameter vectors, margins, and the percentage-point change."""
    ext = read_csv("tables/extensions.csv")
    mod = read_csv("numerics/moderate_values.csv")
    recs = []
    for row in ext:
        if row["accepted"] != "true" or row["parameter_set"] != "base":
            continue
        margins = {k: row[k] for k in MARGIN_KEYS}
        recs.append({"panel": "A", "label": f"{row['noise']}, {'cost atoms' if row['cost_law'] == 'atoms' else 'cost mixture'}",
                     "parameter_set": "base", "noise": row["noise"], "cost_law": row["cost_law"],
                     "h": BENCHMARK.h, "ell": BENCHMARK.ell, "p": BENCHMARK.p, "rho": BENCHMARK.rho, "c_L": BENCHMARK.c_L, "c_H": BENCHMARK.c_H,
                     "b": BENCHMARK.b, "k": BENCHMARK.k, "a": "n/a", "d": "n/a", "r_weak": row["r_weak"], "r_strong": row["r_strong"],
                     "E_weak": row["E_weak"], "E_strong": row["E_strong"], "O_H_weak": row["O_H_weak"], "O_H_strong": row["O_H_strong"],
                     **margins, "status": row["status"], "accepted": row["accepted"]})
    if len(recs) != 4:
        raise ValueError(f"Table 3 Panel A: {len(recs)} accepted base rows, expected 4")
    m = [r for r in mod if r["accepted"] == "true"]
    if len(m) != 1:
        raise ValueError(f"moderate values: {len(m)} accepted rows")
    row = m[0]
    recs.append({"panel": "B", "label": "Moderate values", "parameter_set": "moderate", "noise": "Laplace", "cost_law": "atoms",
                 "h": row["h"], "ell": row["ell"], "p": row["p"], "rho": row["rho"], "c_L": row["c_L"], "c_H": row["c_H"], "b": row["b"], "k": row["k"],
                 "a": "n/a", "d": "n/a", "r_weak": row["r_weak"], "r_strong": row["r_strong"],
                 "E_weak": row["E_weak"], "E_strong": row["E_strong"], "O_H_weak": row["O_H_weak"], "O_H_strong": row["O_H_strong"],
                 **{k: row[k] for k in MARGIN_KEYS}, "status": row["status"], "accepted": row["accepted"]})
    weak, strong = next((w, s) for w, s in signal_comparisons() if (w["a"], w["d"]) == ("0.70", "0.75"))
    recs.append({"panel": "C", "label": "$a=0.70$, $d=0.75$", "parameter_set": "signal", "noise": "Laplace", "cost_law": "atoms",
                 "h": "10", "ell": "1", "p": "0.5", "rho": "0.85", "c_L": "1", "c_H": "7.14", "b": "2", "k": "0.015",
                 "a": weak["a"], "d": weak["d"], "r_weak": weak["r"], "r_strong": strong["r"],
                 "E_weak": weak["E"], "E_strong": strong["E"], "O_H_weak": weak["O_H"], "O_H_strong": strong["O_H"],
                 **{mk: weak[sk] for mk, sk in zip(MARGIN_KEYS, SIGNAL_MARGIN_KEYS)},
                 "status": joint_evidence(weak["status"], strong["status"]), "accepted": "true"})
    for r in recs:
        r["delta_E_pp"] = str(pp_change(r["E_strong"], r["E_weak"]))
        r["minimum_margin"] = str(min(Decimal(r[k]) for k in MARGIN_KEYS))
        r["comparison_condition"] = "met" if Decimal(r["minimum_margin"]) > 0 else "not met"
        r["evidence"] = evidence(r["status"])
        r["unique"] = "yes" if r["evidence"] == "analytical" and r["comparison_condition"] == "met" else "not established"
    return recs


def table3() -> Path:
    recs = _extension_records()
    header = ["", r"\shortstack{$\mathsf E$\\weak}", r"\shortstack{$\mathsf E$\\strong}", r"\shortstack{$\Delta\mathsf E$\\(pp)}",
              r"\shortstack{$\mathsf O_H$\\weak}", r"\shortstack{$\mathsf O_H$\\strong}", "Evidence", "Unique"]
    body = [["Panel A. Noise and preparation costs"]]
    panel_titles = {"B": r"Panel B. Moderate values ($h=2$, $\ell=1$)", "C": "Panel C. Complementary private information"}
    current = "A"
    for r in recs:
        if r["panel"] != current:
            current = r["panel"]
            body += [["\\midrule"], [panel_titles[current]]]
        body.append([r["label"], d6(r["E_weak"]), d6(r["E_strong"]), d2(Decimal(r["delta_E_pp"])), d6(r["O_H_weak"]), d6(r["O_H_strong"]),
                     r["evidence"], r["unique"]])
    notes = [
        r"$\mathsf E$ is the preparation probability and $\mathsf O_H$ the probability of high-value challenger ownership, both probabilities. "
        r"$\Delta\mathsf E=100(\mathsf E_{\mathrm{strong}}-\mathsf E_{\mathrm{weak}})$ is the change in preparation in percentage points, "
        r"computed from the same validated probabilities as the two preparation columns, not a percentage change.",
        r"Each row is a distinct parameter vector (Appendix A.8): Panel A uses the benchmark vector with strengths $(1.2,3)$; Panel B uses the "
        r"moderate-value vector with $(1.05,1.5)$; Panel C uses the complementary-signal vector with $(1.1,2.3)$, investor accuracy $a$ and buyer "
        r"accuracy $d$. Panels B and C are separate illustrations, not one joint calibration. The cost mixture uses half-width "
        r"$\varepsilon_C=0.1$; noise laws share the scale $b$, not the variance.",
        r"Evidence is the result status of the comparison; Unique records whether the sufficient uniqueness conditions of the relevant "
        r"proposition hold (all five margins strictly positive). The individual margins and their minimum are in the online table of "
        r"sufficient-condition margins; the complete accuracy grid is the online accuracy-grid table.",
    ]
    out = TAB / "table3_extensions.tex"
    out.write_text(threeparttable(header, body, r"p{0.26\linewidth}rrrrrll", notes))
    return out


def extensions_margins() -> list[Path]:
    recs = _extension_records()
    cols = ["panel", "label", "parameter_set", "noise", "cost_law", "h", "ell", "p", "rho", "c_L", "c_H", "b", "k", "a", "d", "r_weak", "r_strong",
            "E_weak", "E_strong", "delta_E_pp", "O_H_weak", "O_H_strong", *MARGIN_KEYS, "minimum_margin", "comparison_condition", "evidence", "unique",
            "status", "accepted"]
    csv_path = write_csv("tables/extensions_margins.csv", cols, recs)
    header = ["", *MARGIN_LABELS, "Minimum", "Evidence", "Unique"]
    body = []
    current = None
    titles = {"A": "Panel A. Noise and preparation costs (benchmark vector)", "B": "Panel B. Moderate values",
              "C": "Panel C. Complementary private information"}
    for r in recs:
        if r["panel"] != current:
            if current is not None:
                body.append(["\\midrule"])
            current = r["panel"]
            body.append([titles[current]])
        body.append([r["label"], *[sci(r[k]) for k in MARGIN_KEYS], sci(r["minimum_margin"]), r["evidence"], r["unique"]])
    notes = [
        r"The five strict sufficient inequalities of the relevant proposition (low cost, high cost at the prior, high cost at the ceiling, weak-economy "
        r"trade, strong-economy trade), in the order of \eqref{eq:oa-oa-77} for Panels A and B and of \eqref{eq:oa-oa-29} for Panel C, and their minimum. A positive minimum "
        r"places the row inside the analytical uniqueness region; a nonpositive minimum would mean the comparison condition is not met, not that a "
        r"candidate is rejected.",
        r"Parameter vectors: Panel A $(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02)$ with $(r_0,r_1)=(1.2,3)$; Panel B "
        r"$(2,1,0.5,0.25,0.3,0.89,2,0.002)$ with $(1.05,1.5)$; Panel C $(10,1,0.5,0.85,1,7.14,2,0.015)$ with $(1.1,2.3)$ and $(a,d)=(0.70,0.75)$. "
        r"The complete records, including the preparation change in percentage points, are in \texttt{tables/extensions\_margins.csv}.",
    ]
    tex = online_table("Sufficient-condition margins behind Table 3.", "tab:oa-margins",
                       threeparttable(header, body, r"p{0.24\linewidth}rrrrrrll", notes), landscape=True)
    out = TAB / "table_extensions_margins.tex"
    out.write_text(tex)
    return [out, csv_path]


def signal_grid() -> Path:
    pairs = signal_comparisons()
    header = ["Investor $a$", "Buyer $d$", r"\shortstack{$\mathsf E$\\weak}", r"\shortstack{$\mathsf E$\\strong}",
              r"\shortstack{$\Delta\mathsf E$\\(pp)}", r"\shortstack{$\mathsf O_H$\\weak}", r"\shortstack{$\mathsf O_H$\\strong}",
              r"\shortstack{Minimum\\margin}", "Evidence", r"\shortstack{Comparison\\condition}"]
    n = len(header)
    heading = " & ".join(header) + r" \\"
    lines = [r"\begin{landscape}\begingroup\singlespacing\footnotesize\setlength{\tabcolsep}{3pt}",
             rf"\begin{{longtable}}{{@{{\extracolsep{{\fill}}}}{'r' * 8}ll@{{}}}}",
             r"\caption{Complementary private information: complete accuracy grid.}\label{tab:oa-signals}\\",
             r"\toprule", heading, r"\midrule", r"\endfirsthead",
             r"\caption[]{Complementary private information: complete accuracy grid (continued).}\\",
             r"\toprule", heading, r"\midrule", r"\endhead",
             rf"\midrule\multicolumn{{{n}}}{{r}}{{\textit{{Continued on next page}}}}\\", r"\endfoot",
             r"\bottomrule", r"\endlastfoot"]
    n_met = 0
    for weak, strong in pairs:
        margin = min((weak[k] for k in SIGNAL_MARGIN_KEYS), key=Decimal)
        condition = "met" if Decimal(margin) > 0 else "not met"
        n_met += condition == "met"
        mark = r"$^{*}$" if (weak["a"], weak["d"]) == ("0.70", "0.75") else ""
        lines.append(" & ".join([weak["a"] + mark, weak["d"], d6(weak["E"]), d6(strong["E"]), d2(pp_change(strong["E"], weak["E"])),
                                  d6(weak["O_H"]), d6(strong["O_H"]), sci(margin), joint_evidence(weak["status"], strong["status"]), condition]) + r" \\")
    notes = (r"\textit{Notes.} All " + str(len(pairs)) + r" accuracy combinations in the declaration in Section C.3 are reported; none is dropped. "
             r"Other parameters are $h=10$, $\ell=1$, $p=0.5$, $\rho=0.85$, $c_L=1$, $c_H=7.14$, $b=2$, $k=0.015$, "
             r"with strengths $r_0=1.1$ and $r_1=2.3$. $\mathsf E$ and $\mathsf O_H$ are probabilities; $\Delta\mathsf E$ is the change in "
             r"preparation in percentage points from the same validated probabilities. "
             r"The minimum margin is the smallest of the five conditions in \eqref{eq:oa-oa-29}; the comparison condition is met when it is strictly positive "
             r"(" + str(n_met) + r" rows), which places the row inside the analytical uniqueness region. A condition that is not met is not a "
             r"rejection: every row is a validated equilibrium of the finite check, and its evidence is then numerical diagnostic unless a separate "
             r"analytical or interval argument supports more. The asterisk marks the example used in the main text. All rows pass the declared "
             r"numerical acceptance checks.")
    lines += [rf"\multicolumn{{{n}}}{{@{{}}p{{0.97\linewidth}}@{{}}}}{{{notes}}}\\", r"\end{longtable}", r"\endgroup\end{landscape}"]
    out = TAB / "table_signal_grid.tex"
    out.write_text("\n".join(lines) + "\n")
    return out


# ---------------------------------------------------------------------------------------------
# Table 4, the online reserve details, and the online exploratory summary
# ---------------------------------------------------------------------------------------------
def _declared_reserve_nodes() -> list[dict]:
    """The eight declared fixed-reserve nodes, joined on the full parameter identity, the exact reserve, the event
    label, and the branch, with outcome measures from numerics/reserve_events.csv and margins from
    tables/reserve_comparisons.csv. A missing or ambiguous node is left as an unresolved placeholder."""
    from numerics.continuations import parameter_set_id
    comp = read_csv("tables/reserve_comparisons.csv")
    events = read_csv("numerics/reserve_events.csv")
    nodes = []
    for law, lawname in (("binary", "binary"), ("uniform_classes", "uniform_classes")):
        eps_v = BENCHMARK_EXTRA["value_band_halfwidth"] if law == "uniform_classes" else "0"
        for key, name in STRENGTH_NAMES:
            rs = BENCHMARK_STRENGTHS[key]
            for ps in DECLARED_RESERVES[law]:
                ps_id = parameter_set_id(BENCHMARK, rs, ps, law, eps_v)
                node = {"value_law": law, "r": rs, "p": ps, "label": f"{name.removesuffix(' incumbent')} ($r={rs}$), $p={ps}$", "parameter_set_id": ps_id,
                        "unresolved": ""}
                c = [x for x in comp if x.get("parameter_set_id") == ps_id and x["value_law"] == law and Decimal(x["r"]) == Decimal(rs) and Decimal(x["p"]) == Decimal(ps)
                     and Decimal(x["epsilon_V"]) == Decimal(eps_v) and x["accepted"] == "true"]
                ev = [x for x in events if x["parameter_set_id"] == ps_id and x["p_exact"] == ps and x["accepted"] == "true"
                      and x["event_id"] == f"declared_reserve_{ps}"]
                if len(c) != 1 or len(ev) != 1:
                    node["unresolved"] = f"{len(c)} comparison rows and {len(ev)} event rows match the declared node"
                    nodes.append(node)
                    continue
                c, ev = c[0], ev[0]
                for identity in ("continuation_id", "institution_id", "information_structure_id", "p_exact", "branch"):
                    if c.get(identity) != ev[identity]:
                        raise ValueError(f"reserve comparison {identity} disagrees with event identity at {law}, r={rs}, p={ps}")
                if ev["branch"] != ("pooling" if Decimal(c["q_H"]) == 0 else "full_orders"):
                    node["unresolved"] = f"branch mismatch: comparisons {c['q_H']},{c['q_L']} versus events {ev['branch']}"
                    nodes.append(node)
                    continue
                for a, b_, what in ((c["E"], ev["preparation_probability"], "E"), (c["R_T"], ev["seller_revenue"], "R_T")):
                    if abs(Decimal(a) - Decimal(b_)) > IDENTITY_TOL:
                        raise ValueError(f"{what} differs between reserve_comparisons and reserve_events at {law}, r={rs}, p={ps}: {a} vs {b_}")
                node.update({"branch": ev["branch"], "q_H": c["q_H"], "q_L": c["q_L"], "E": ev["preparation_probability"],
                             "S": ev["sale_probability"], "C2": ev["two_admissible_bidders_probability"], "A": ev["admissible_challenger_probability"],
                             "O_H": ev["high_value_ownership_probability"], "R_T": ev["seller_revenue"],
                             "low_cost_floor_margin": c["low_cost_floor_margin"], "trading_margin": c["trading_margin"],
                             "status": joint_evidence(c["status"], ev["result_status"]), "result_status": ev["result_status"], "existence_scope": ev["existence_scope"],
                             "uniqueness_scope": ev["uniqueness_scope"], "candidate_id": ev["candidate_id"], "tie_rule_id": ev["tie_rule_id"],
                             "institution_id": ev["institution_id"], "information_structure_id": ev["information_structure_id"]})
                nodes.append(node)
    return nodes


def table4() -> Path:
    nodes = _declared_reserve_nodes()
    header = ["Economy and reserve", "Preparation", "Sale", r"\shortstack{Two admissible\\bidders}", r"\shortstack{Expected target\\proceeds}",
              "Trading outcome"]
    body = []
    unresolved = []
    for law, title in (("binary", "Panel A. Binary values"), ("uniform_classes", r"Panel B. Atomless values with class information ($\varepsilon_V=0.05$)")):
        if body:
            body.append(["\\midrule"])
        body.append([title])
        for n in (x for x in nodes if x["value_law"] == law):
            if n["unresolved"]:
                unresolved.append(f"{n['label']}: {n['unresolved']}")
                body.append([n["label"], "[[unresolved]]", "[[unresolved]]", "[[unresolved]]", "[[unresolved]]", "[[unresolved]]"])
                continue
            body.append([n["label"], d6(n["E"]), d6(n["S"]), d6(n["C2"]), d6(n["R_T"]), trading_outcome(n["q_H"], n["q_L"])])
    supported = [n for n in nodes if not n["unresolved"] and evidence(n["status"]) == "analytical"
                 and unique_field(n["uniqueness_scope"]) == "yes"]
    if len(supported) == len(nodes):
        support = (r"Analytical support: at every listed node the trading outcome is the unique continuation under the global bound "
                   r"($k-\Delta_T>0$ for no trade; the uniform derivative bound with a positive low-cost floor for full orders).")
    else:
        lacking = [n["label"] for n in nodes if n not in supported]
        support = (r"Analytical support: the trading outcome is the unique continuation under the global bound ($k-\Delta_T>0$ for no trade; "
                   r"the uniform derivative bound with a positive low-cost floor for full orders) at every listed node except " + "; ".join(lacking) + ".")
    notes = [
        r"Preparation is the probability that the challenger pays its preparation cost. Sale is the probability that at least one bidder submits "
        r"an admissible bid, whether the incumbent or a prepared challenger whose realized value meets the reserve. Two admissible bidders is the "
        r"probability that both do. Expected target proceeds are seller revenue per share. All are validated outcome measures of the listed "
        r"continuation at the declared reserve.",
        r"Benchmark primitives, Laplace noise, cost atoms; Panel B draws values uniformly around $\ell$ and $h$ with half-width "
        r"$\varepsilon_V=0.05$ and gives the investor class information only. " + support + r" Order magnitudes, margins, evidence status, uniqueness scope, and "
        r"the complete parameter identity of each node are in the online reserve-details table. The exploratory reserve "
        r"summary (highest revenue among continuations found) is the online exploratory table.",
    ]
    if unresolved:
        notes.append("Unresolved nodes: " + "; ".join(esc(u) for u in unresolved) + ".")
    out = TAB / "table4_reserve_comparisons.tex"
    out.write_text(threeparttable(header, body, r"p{0.28\linewidth}rrrrl", notes))
    if unresolved:
        print("table4 unresolved:", *unresolved, sep="\n  ")
    return out


def reserve_details() -> Path:
    nodes = _declared_reserve_nodes()
    header = ["Economy and reserve", "$q_H$", "$q_L$", r"$\mathsf E$", r"$\mathsf A$", r"$\mathsf O_H$", r"$\mathcal R_T$",
              r"\shortstack{Floor\\margin}", r"\shortstack{Trading\\margin}", "Evidence", "Unique"]
    body = []
    ids = set()
    for law, title in (("binary", "Panel A. Binary values"), ("uniform_classes", r"Panel B. Atomless values with class information")):
        if body:
            body.append(["\\midrule"])
        body.append([title])
        for n in (x for x in nodes if x["value_law"] == law):
            if n["unresolved"]:
                body.append([n["label"]] + ["[[unresolved]]"] * 8 + ["open", "n/a"])
                continue
            ids.add((n["institution_id"], n["information_structure_id"], n["tie_rule_id"]))
            body.append([n["label"], order(n["q_H"]), order(n["q_L"]), d6(n["E"]), d6(n["A"]), d6(n["O_H"]), d6(n["R_T"]),
                         sci(n["low_cost_floor_margin"]), sci(n["trading_margin"]), evidence(n["status"]), unique_field(n["uniqueness_scope"])])
    resolved = [n for n in nodes if not n["unresolved"]]
    ident = resolved[0]["parameter_set_id"] if resolved else ""
    common = "|".join(part for part in ident.split("|") if not part.startswith(("p=", "r=", "value_law=", "eps_V=")))
    notes = [
        r"Complete parameter identity of every node: \texttt{" + identity_text(common) + r"} with \texttt{r}, \texttt{p}, \texttt{value\_law} "
        r"$\in\{$binary, uniform\_classes$\}$ and \texttt{eps\_V} $\in\{0, 0.05\}$ as listed. Institution, information structure, and tie rule: "
        + "; ".join(r"\texttt{" + identity_text(a) + r"}, \texttt{" + identity_text(b_) + r"}, \texttt{" + identity_text(t) + "}" for a, b_, t in sorted(ids)) + ".",
        r"$\mathsf A$ is the probability of an admissible prepared challenger. Floor margin is $B_r(m)-c_L$; trading margin is $k-\Delta_T$ for "
        r"no trade and $(1-1/b)\,e(m)\,m\,\Delta_T-k$ for full orders. Evidence is the result status; Unique reports the uniqueness scope recorded "
        r"with the continuation (unique within all continuations under the stated bound, or not established). Each node is a validated row of "
        r"\texttt{numerics/reserve\_events.csv} joined with \texttt{tables/reserve\_comparisons.csv} on the full parameter identity, the exact "
        r"reserve, and the branch.",
    ]
    tex = online_table("Reserve comparisons: orders, margins, evidence, and identity behind Table 4.", "tab:oa-reserve-details",
                       threeparttable(header, body, r"p{0.24\linewidth}rrrrrrrrll", notes), landscape=True)
    out = TAB / "table_reserve_details.tex"
    out.write_text(tex)
    return out


def _read_ranges(path: str) -> list[dict]:
    rows = read_csv(path)
    if not rows:
        raise ValueError(f"{path} is empty")
    missing = [c for c in RANGE_COLUMNS if c not in rows[0]]
    if missing:
        raise ValueError(f"{path} lacks the widened C.6 range schema (missing {missing}); rerun numerics/exercises/c6_reserve.py. "
                         "The exploratory table is not rendered from the narrow schema.")
    identities = set()
    for row in rows:
        identity = row["value_law"], Decimal(row["r"]), row["p_exact"]
        if identity in identities:
            raise ValueError(f"duplicate reserve range node: {identity}")
        identities.add(identity)
        counts = {k: int(row[k]) for k in ("candidates_evaluated", "candidates_accepted_raw", "candidates_rejected",
                                         "candidates_unresolved", "duplicates_merged", "accepted_continuations_found")}
        if (min(counts.values()) < 0
                or counts["candidates_evaluated"] != sum(counts[k] for k in ("candidates_accepted_raw", "candidates_rejected", "candidates_unresolved"))
                or counts["candidates_accepted_raw"] - counts["duplicates_merged"] != counts["accepted_continuations_found"]):
            raise ValueError(f"inconsistent reserve attempt ledger: {identity}")
    return rows


def _is_event(event_id: str) -> bool:
    return event_id not in ("grid", "") and not event_id.startswith("offset")


def _p_display(row: dict) -> str:
    """Exact decimal reserves verbatim; symbolic event reserves by their symbol, offsets by their exact size, with the decimal value."""
    pe = row["p_exact"]
    try:
        Decimal(pe)
        return f"${pe}$"
    except Exception:
        pass
    m = re.match(r"^(p_[LH])=.*?(?:([+-])(0\.0*1))?$", pe)
    if not m:
        return r"\texttt{" + esc(pe) + f"}} ($\\approx {d6(row['p'])}$)"
    sym = f"{m.group(1)}"
    if m.group(2):
        sym += f"{m.group(2)}10^{{{Decimal(m.group(3)).adjusted()}}}"
    return f"${sym}$ ($\\approx {d6(row['p'])}$)"


def reserve_exploratory(path: str = "numerics/reserve_ranges.csv") -> Path:
    rng = _read_ranges(path)
    laws = (("binary", "Binary values"), ("uniform_classes", "Class values"))
    strengths = [BENCHMARK_STRENGTHS[k] for k, _ in STRENGTH_NAMES]
    # Panel 1: highest revenue among continuations found
    best_body = [["Panel A. Highest revenue among continuations found"]]
    cover_body = [["Panel B. Search coverage from the final-pass attempt ledger"]]
    event_body = []
    for law, lawname in laws:
        for rs in strengths:
            sub = [x for x in rng if x["value_law"] == law and Decimal(x["r"]) == Decimal(rs)]
            if not sub:
                continue
            found = [x for x in sub if x["accepted_continuations_found"] != "0" and x["R_T_max_found"] != "n/a"]
            if found:
                top = max(Decimal(x["R_T_max_found"]) for x in found)
                ties = sorted((x for x in found if Decimal(x["R_T_max_found"]) == top), key=lambda x: Decimal(x["p"]))
                best = ties[0]
                kind = "event: " + esc(best["event_id"].replace("_", " ")) if _is_event(best["event_id"]) else ("grid" if best["event_id"] == "grid" else esc(best["event_id"].replace("_", " ")))
                best_body.append([f"{lawname}, $r={rs}$", _p_display(best), kind, best["accepted_continuations_found"],
                                  *[d6(best[f"{q}_min_found"]) if Decimal(best[f"{q}_min_found"]) == Decimal(best[f"{q}_max_found"])
                                    else d6(best[f"{q}_min_found"]) + "--" + d6(best[f"{q}_max_found"]) for q in ("E", "R_T")],
                                  esc(best["search_outcome"]) + (f" ({len(ties)} nodes tie)" if len(ties) > 1 else "")])
            else:
                best_body.append([f"{lawname}, $r={rs}$", "none", "n/a", "0", "n/a", "n/a", "no accepted continuation found at any node"])
            n_multi = sum(1 for x in sub if int(x["accepted_continuations_found"]) >= 2)
            n_unres = sum(1 for x in sub if x["search_unresolved"] == "true")
            n_none = sum(1 for x in sub if x["accepted_continuations_found"] == "0")
            n_event = sum(1 for x in sub if _is_event(x["event_id"]))
            cover_body.append([f"{lawname}, $r={rs}$", str(len(sub)), str(n_event), str(n_multi), str(n_unres), str(n_none),
                               str(sum(int(x["candidates_evaluated"]) for x in sub)), str(sum(int(x["candidates_rejected"]) for x in sub)),
                               str(sum(int(x["candidates_unresolved"]) for x in sub)), str(sum(int(x["duplicates_merged"]) for x in sub))])
            for x in sorted((x for x in sub if _is_event(x["event_id"])), key=lambda x: Decimal(x["p"])):
                event_body.append([f"{'Binary' if law == 'binary' else 'Classes'}, $r={rs}$", esc(x["event_id"].replace("_", " ")), _p_display(x), x["accepted_continuations_found"],
                                   d6(x["R_T_max_found"]) if x["R_T_max_found"] != "n/a" else "n/a",
                                   "yes" if x["search_unresolved"] == "true" else "no", esc(x["search_outcome"])])
    if any(x["global_envelope_certified"] == "true" for x in rng):
        raise ValueError("a range row claims a certified global envelope; the exploratory table does not report certified envelopes")
    best = tabular(["", "Reserve", "Node", "Found", r"$\mathsf E$ range", r"$\mathcal R_T$ range", "Search outcome"], best_body, r"p{0.15\linewidth}lp{0.14\linewidth}rrrp{0.24\linewidth}")
    cover = tabular(["", "Nodes", "Events", r"\shortstack{Several\\found}", "Unresolved", r"\shortstack{None\\found}",
                     r"\shortstack{Candidates\\evaluated}", "Rejected", r"\shortstack{Cand.\\unresolved}", r"\shortstack{Duplicates\\merged}"],
                    cover_body, r"p{0.17\linewidth}rrrrrrrrr")
    notes = [
        r"Highest revenue among continuations found, not an optimal reserve: Panel A selects, for each economy, the node (grid point or exact "
        r"event) whose highest accepted continuation revenue is largest among the continuations the declared searches found, and reports the "
        r"ranges of preparation and revenue across the accepted continuations at that node. Range endpoints need not belong to the same "
        r"continuation; a single value denotes a singleton found range. No global envelope is certified; a node without an accepted continuation is not a nonexistence result, and an "
        r"unresolved node does not imply an empty equilibrium set.",
        r"Panel B counts come from the final-pass attempt and validation ledger of \texttt{numerics/reserve\_ranges.csv}, one record per solved node: nodes "
        r"attempted, exact-event nodes among them, nodes with several accepted continuations, nodes left unresolved, nodes with no accepted "
        r"continuation, candidates evaluated, rejected, unresolved, and duplicates merged by the continuation identity. The following exact-event table lists every "
        r"exact-event node (reserve at zero, at $\ell$, at $r$, at $h$, at the class-band edges, at the declared reserves, at the published sampled "
        r"weak reserve, at the weak-incumbent floor equality $p_L=h-c_L/m$, and at the high-cost ceiling equality $p_H$) with the candidates found "
        r"there; one-sided offsets from each event are separate nodes counted in Panel B. Earlier attempts that triggered identity refinement "
        r"are preserved separately in the numerical diagnostics archive. Known limits: the searches "
        r"cover the declared candidate families and the declared pricing family only (Online Appendix C.6).",
    ]
    body = (r"\begin{threeparttable}" + "\n" + r"\setlength{\tabcolsep}{3pt}" + "\n" + best + "\n" + r"\par\medskip" + "\n" + cover + "\n"
            + r"\begin{tablenotes}\footnotesize" + "\n"
            + "\n".join(f"\\item {n}" for n in notes) + "\n" + r"\end{tablenotes}" + "\n" + r"\end{threeparttable}" + "\n")
    tex = online_table("Highest revenue among continuations found: exploratory reserve summary with coverage counts.",
                       "tab:oa-reserve-exploratory", body, landscape=True)
    heading = " & ".join(["", "Event", "Reserve", "Found", r"$\mathcal R_T$ max", "Unresolved", "Search outcome"]) + r" \\"
    events = [r"\begin{landscape}\begingroup\singlespacing\small\setlength{\tabcolsep}{3pt}",
              r"\begin{longtable}{@{}p{0.13\linewidth}p{0.19\linewidth}lrrlp{0.24\linewidth}@{}}",
              r"\caption{Exact-event candidates in the exploratory reserve search.}\label{tab:oa-reserve-events}\\",
              r"\toprule", heading, r"\midrule\endfirsthead",
              r"\caption[]{Exact-event candidates in the exploratory reserve search (continued).}\\",
              r"\toprule", heading, r"\midrule\endhead",
              r"\midrule\multicolumn{7}{r}{\textit{Continued on next page}}\\\endfoot",
              r"\bottomrule\endlastfoot"]
    events += [" & ".join(row) + r" \\" for row in event_body]
    events += [r"\end{longtable}\endgroup\end{landscape}"]
    tex += "\n".join(events) + "\n"
    out = TAB / "table_reserve_exploratory.tex"
    out.write_text(tex)
    return out


# ---------------------------------------------------------------------------------------------
def render_main() -> list[Path]:
    return [table1(), table2(), table3(), table4()]


def render_online() -> list[Path]:
    out = [*matched_price_panel(), *extensions_margins(), signal_grid(), reserve_details(), reserve_exploratory()]
    return out


def render_all() -> list[Path]:
    return render_main() + render_online()


if __name__ == "__main__":
    for p in render_all():
        print(p)
