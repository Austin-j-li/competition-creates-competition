"""CSV rows to ``<table>`` HTML for the handout (handout/README.md, table slots).

Row selection and number formatting mirror ``numerics/render/tables.py`` (``d6``, ``sci``,
``status_word``, ``order``) without importing it. Every numeric cell carries the raw CSV token in
``title`` and its source in ``data-src``. Stdlib only.
"""
from __future__ import annotations

import csv
import html
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from pathlib import Path

MARGIN_KEYS = ("zeta_L", "zeta_H0", "zeta_H1", "zeta_0", "zeta_1")
SIGNAL_MARGIN_KEYS = ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin",
                      "weak_order_margin", "strong_order_margin")


class TableError(ValueError):
    pass


def _rows(root: Path, rel: str) -> list[dict]:
    with open(root / rel, newline="", encoding="utf-8") as fh:
        out = []
        for i, r in enumerate(csv.DictReader(fh), start=2):  # line number in the file
            r = dict(r)
            r["__src"] = f"{rel}:{i}"
            out.append(r)
        return out


# ----------------------------------------------------------------------------------------------
# Formatting (mirrors numerics/render/tables.py)


def d6(x: str) -> str:
    try:
        return format(Decimal(x).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN), "f")
    except (InvalidOperation, ValueError):
        return "n/a"


def sci(x: str) -> str:
    try:
        mantissa, exponent = f"{Decimal(x):.2E}".split("E")
        return f'{mantissa}<span class="times">×</span>10<sup>{int(exponent)}</sup>'
    except (InvalidOperation, ValueError):
        return "n/a"


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
    return html.escape(text.split(" (")[0])


def order(q: str) -> str:
    try:
        v = Decimal(q)
        return format(v.normalize(), "f") if v != v.to_integral() else str(int(v))
    except (InvalidOperation, ValueError):
        return html.escape(q)


# ----------------------------------------------------------------------------------------------
# HTML helpers


class Tokens:
    """Collects every raw token rendered, for the build's number audit."""

    def __init__(self) -> None:
        self.used: set[str] = set()


def cell(shown: str, raw: str, src: str, tokens: Tokens, cls: str = "num") -> str:
    tokens.used.add(raw)
    return f'<td class="{cls}" title="{html.escape(raw)}" data-src="{html.escape(src)}">{shown}</td>'


def text_cell(shown: str, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return f"<td{c}>{shown}</td>"


def head(cols: list[str], first: str = "") -> str:
    ths = [f'<th scope="col">{first}</th>'] + [f'<th scope="col" class="num">{c}</th>' for c in cols]
    return "<thead><tr>" + "".join(ths) + "</tr></thead>"


def panel(label: str, n: int) -> str:
    return f'<tr class="panel"><td colspan="{n}">{label}</td></tr>'


def table(caption_id: str, thead: str, body_rows: list[str], cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    return (f'<div class="table-wrap"><table{c} data-table="{caption_id}">{thead}<tbody>'
            + "".join(body_rows) + "</tbody></table></div>")


# ----------------------------------------------------------------------------------------------
# Tables


def t_auction_primitives(root: Path, tk: Tokens) -> str:
    rows = [r for r in _rows(root, "tables/auction_primitives.csv") if r["parameter_set"] == "base"]
    cols = {rs: next((r for r in rows if r["r"] == rs), None) for rs in ("1.2", "3", "3.6")}
    if any(v is None for v in cols.values()):
        raise TableError("auction_primitives: missing base rows at r = 1.2, 3, 3.6")
    labels = (("t_0", "t<sub>0</sub>, proceeds without a challenger"),
              ("t_H", "t<sub>H</sub>, proceeds with a high-value challenger"),
              ("t_L", "t<sub>L</sub>, proceeds with a low-value challenger"),
              ("g_H", "g<sub>H</sub>, gross profit of a high-value challenger"),
              ("g_L", "g<sub>L</sub>, gross profit of a low-value challenger"),
              ("Delta_T", "Δ<sub>T</sub> = t<sub>H</sub> − t<sub>L</sub>, target-payoff spread"),
              ("B_prior", "B<sub>r</sub>(1/2), expected gross profit at the prior"))
    body = []
    for key, lab in labels:
        tds = [f'<th scope="row">{lab}</th>']
        for rs in ("1.2", "3", "3.6"):
            r = cols[rs]
            tds.append(cell(d6(r[key]), r[key], r["__src"], tk))
        body.append("<tr>" + "".join(tds) + "</tr>")
    return table("auction_primitives", head(["Weak (r = 1.2)", "Strong (r = 3)", "Very strong (r = 3.6)"]), body)


def _controls_base(root: Path) -> list[dict]:
    eq = _rows(root, "tables/equilibrium_controls.csv")
    return [r for r in eq if r["noise"] == "Laplace" and r["cost_law"] == "atoms" and r["accepted"] == "true"]


def _eq_row(base: list[dict], exp: str, rs: str) -> dict:
    hits = [x for x in base if x["experiment"] == exp and x["r"] == rs]
    if len(hits) != 1:
        raise TableError(f"equilibrium_controls: {len(hits)} rows for experiment={exp}, r={rs}")
    return hits[0]


def t_equilibrium_controls(root: Path, tk: Tokens) -> str:
    base = _controls_base(root)
    cols = ["q<sub>H</sub>", "q<sub>L</sub>", "E", "O<sub>H</sub>", "R<sub>T</sub>", "Basis"]
    n = len(cols) + 1
    body = [panel("Panel A. Equilibrium", n)]

    def line(label: str, r: dict) -> str:
        return ("<tr>" + f'<th scope="row">{label}</th>'
                + cell(order(r["q_H"]), r["q_H"], r["__src"], tk) + cell(order(r["q_L"]), r["q_L"], r["__src"], tk)
                + cell(d6(r["E"]), r["E"], r["__src"], tk) + cell(d6(r["O_H"]), r["O_H"], r["__src"], tk)
                + cell(d6(r["R_T"]), r["R_T"], r["__src"], tk) + text_cell(status_word(r["status"]), "basis") + "</tr>")

    for rs, name in (("1.2", "Weak incumbent"), ("3", "Strong incumbent"), ("3.6", "Very strong incumbent")):
        body.append(line(f"{name} (r = {rs})", _eq_row(base, "feedback", rs)))
    body.append(panel("Panel B. Information controls", n))
    for exp, lab in (("frozen", "Frozen informative orders"), ("price_hidden", "Price hidden from the challenger"),
                     ("matched_dividend", "Matched dividend")):
        for rs in ("1.2", "3"):
            body.append(line(f"{lab}, r = {rs}", _eq_row(base, exp, rs)))
    return table("equilibrium_controls", head(cols), body)


def t_welfare(root: Path, tk: Tokens) -> str:
    fb = _rows(root, "numerics/feedback_comparisons.csv")
    hits = [x for x in fb if x["noise"] == "Laplace" and x["cost_law"] == "atoms" and x["r"] == "3"]
    if len(hits) != 1:
        raise TableError(f"feedback_comparisons: {len(hits)} rows for Laplace/atoms/r=3")
    f = hits[0]
    body = [panel("Panel C. Access to prices at r = 3", 4)]
    for lab, keys in (("Target proceeds R<sub>T</sub>", ("R_T_feedback", "R_T_hidden", "R_T_gain")),
                      ("Net acquisition surplus W", ("W_feedback", "W_hidden", "W_gain"))):
        body.append("<tr>" + f'<th scope="row">{lab}</th>' + "".join(cell(d6(f[k]), f[k], f["__src"], tk) for k in keys) + "</tr>")
    return table("welfare", head(["Price observed", "Price hidden", "Gain"]), body)


def t_extensions(root: Path, tk: Tokens) -> str:
    ext = _rows(root, "tables/extensions.csv")
    mod = _rows(root, "numerics/moderate_values.csv")
    cols = ["Entry weak", "Entry strong", "O<sub>H</sub> weak", "O<sub>H</sub> strong", "Minimum margin", "Basis"]
    n = len(cols) + 1
    body = [panel("Panel A. Noise and preparation costs (r = 1.2 and 3)", n)]

    def line(label: str, r: dict, margin_keys: tuple, status: str, ew="E_weak", es="E_strong", ow="O_H_weak", os_="O_H_strong") -> str:
        mkey = min(margin_keys, key=lambda k: Decimal(r[k]))
        return ("<tr>" + f'<th scope="row">{label}</th>'
                + cell(d6(r[ew]), r[ew], r["__src"], tk) + cell(d6(r[es]), r[es], r["__src"], tk)
                + cell(d6(r[ow]), r[ow], r["__src"], tk) + cell(d6(r[os_]), r[os_], r["__src"], tk)
                + cell(sci(r[mkey]), r[mkey], r["__src"], tk) + text_cell(status_word(status), "basis") + "</tr>")

    for row in ext:
        cost = "cost atoms" if row["cost_law"] == "atoms" else "cost mixture"
        body.append(line(f"{row['noise']}, {cost}", row, MARGIN_KEYS, row["status"]))
    body.append(panel("Panel B. Moderate values (h = 2, ℓ = 1; r = 1.05 and 1.5)", n))
    if len(mod) != 1:
        raise TableError(f"moderate_values: expected 1 row, found {len(mod)}")
    body.append(line("Moderate values", mod[0], MARGIN_KEYS, mod[0]["status"]))
    # Panel C: the declared signal example (a = 0.70, d = 0.75) at r = 1.1 and 2.3
    sig = _rows(root, "numerics/two_signals.csv")
    weak = [r for r in sig if (r["a"], r["d"], r["r"], r["accepted"]) == ("0.70", "0.75", "1.1", "true")]
    strong = [r for r in sig if (r["a"], r["d"], r["r"], r["accepted"]) == ("0.70", "0.75", "2.3", "true")]
    if len(weak) == 1 and len(strong) == 1:
        w, s = weak[0], strong[0]
        mkey = min(SIGNAL_MARGIN_KEYS, key=lambda k: Decimal(w[k]))
        body.append(panel("Panel C. Complementary private information (r = 1.1 and 2.3)", n))
        body.append("<tr>" + '<th scope="row">Investor accuracy a = 0.70, buyer accuracy d = 0.75</th>'
                    + cell(d6(w["E"]), w["E"], w["__src"], tk) + cell(d6(s["E"]), s["E"], s["__src"], tk)
                    + cell(d6(w["O_H"]), w["O_H"], w["__src"], tk) + cell(d6(s["O_H"]), s["O_H"], s["__src"], tk)
                    + cell(sci(w[mkey]), w[mkey], w["__src"], tk) + text_cell(status_word(s["status"]), "basis") + "</tr>")
    else:
        raise TableError(f"two_signals: declared example not uniquely identified (weak {len(weak)}, strong {len(strong)})")
    return table("extensions", head(cols), body)


def t_reserve_comparisons(root: Path, tk: Tokens) -> str:
    comp = _rows(root, "tables/reserve_comparisons.csv")
    cols = ["q<sub>H</sub>", "q<sub>L</sub>", "E", "R<sub>T</sub>", "Margin", "Basis"]
    n = len(cols) + 1
    body = []
    for law, label in (("binary", "Panel A. Binary values"),
                       ("uniform_classes", "Panel B. Atomless values with class information (ε<sub>V</sub> = 0.05)")):
        body.append(panel(label, n))
        for r in comp:
            if r["value_law"] != law:
                continue
            basis = status_word(r["status"]) + ("" if r["accepted"] == "true" else " (not accepted)")
            body.append("<tr>" + f'<th scope="row">r = {html.escape(r["r"])}, reserve p = {html.escape(r["p"])}</th>'
                        + cell(order(r["q_H"]), r["q_H"], r["__src"], tk) + cell(order(r["q_L"]), r["q_L"], r["__src"], tk)
                        + cell(d6(r["E"]), r["E"], r["__src"], tk) + cell(d6(r["R_T"]), r["R_T"], r["__src"], tk)
                        + cell(sci(r["trading_margin"]), r["trading_margin"], r["__src"], tk)
                        + text_cell(basis, "basis") + "</tr>")
    return table("reserve_comparisons", head(cols), body)


def _direction(vals: list[str]) -> str:
    """Glyph for the movement across r = 1.2, 3, 3.6; blank when any value is not finite."""
    try:
        ds = [Decimal(v) for v in vals]
    except InvalidOperation:
        return ""
    steps = [(b > a) - (b < a) for a, b in zip(ds, ds[1:])]
    if all(s == 0 for s in steps):
        return "="
    if all(s >= 0 for s in steps):
        return "↑"
    if all(s <= 0 for s in steps):
        return "↓"
    return "↑ then ↓" if steps[0] > 0 else "↓ then ↑"


def t_comparative_statics(root: Path, tk: Tokens) -> str:
    prim = {r["r"]: r for r in _rows(root, "tables/auction_primitives.csv") if r["parameter_set"] == "base"}
    base = _controls_base(root)
    eq = {rs: _eq_row(base, "feedback", rs) for rs in ("1.2", "3", "3.6")}
    for rs in ("1.2", "3", "3.6"):
        if rs not in prim:
            raise TableError(f"auction_primitives: no base row at r={rs}")
    spec = (("Δ<sub>T</sub>, target-payoff spread", prim, "Delta_T"),
            ("B<sub>r</sub>(1/2), gross profit at the prior", prim, "B_prior"),
            ("B<sub>r</sub>(M), gross profit at the posterior ceiling", prim, "B_M"),
            ("τ, threshold belief for high-cost preparation", eq, "tau"),
            ("x*, threshold order flow", eq, "x_star"),
            ("E, total entry", eq, "E"),
            ("O<sub>H</sub>, high-value challenger ownership", eq, "O_H"),
            ("R<sub>T</sub>, expected target proceeds", eq, "R_T"))
    body = []
    for label, src, key in spec:
        raws = [src[rs][key] for rs in ("1.2", "3", "3.6")]
        tds = [f'<th scope="row">{label}</th>']
        for rs, raw in zip(("1.2", "3", "3.6"), raws):
            shown = "∞" if raw == "inf" else ("n/a" if raw == "nan" else d6(raw))
            tds.append(cell(shown, raw, src[rs]["__src"], tk))
        tds.append(text_cell(_direction(raws), "dir"))
        body.append("<tr>" + "".join(tds) + "</tr>")
    return table("comparative_statics", head(["r = 1.2", "r = 3", "r = 3.6", "Across r"]), body)


def t_thresholds(root: Path, tk: Tokens) -> str:
    thr = {r["boundary"]: r for r in _rows(root, "numerics/thresholds.csv")}
    spec = (("pooling_unique_sufficient", "r(k)", "no trade uniquely optimal below"),
            ("pooling_existence", "r<sub>N</sub>", "no trade exists up to"),
            ("full_orders_unique_sufficient", "r<sub>U</sub>", "full orders uniquely optimal above"),
            ("high_cost_ceiling", "r<sub>C</sub>", "high-cost entry infeasible above"))
    body = []
    for key, sym, role in spec:
        if key not in thr:
            raise TableError(f"thresholds: missing {key}")
        r = thr[key]
        try:
            shown = format(Decimal(r["value"]).quantize(Decimal("0.000000001"), rounding=ROUND_HALF_EVEN), "f")
        except InvalidOperation:
            shown = "n/a"
        body.append("<tr>" + f'<th scope="row">{sym}</th>' + text_cell(role)
                    + cell(shown, r["value"], r["__src"], tk) + text_cell(html.escape(r["interpretation"]), "note") + "</tr>")
    thead = ('<thead><tr><th scope="col">Boundary</th><th scope="col">Role</th>'
             '<th scope="col" class="num">Value</th><th scope="col">Definition</th></tr></thead>')
    return table("thresholds", thead, body)


def t_certificates(root: Path, tk: Tokens) -> str:
    certs = sorted(_rows(root, "numerics/certificates.csv"), key=lambda x: Decimal(x["r"]))
    body = []
    for c in certs:
        v = f"[{html.escape(c['v_lower'])}, {html.escape(c['v_upper'])}]"
        e = f"[{html.escape(c['E_lower'])}, {html.escape(c['E_upper'])}]"
        for k in ("v_lower", "v_upper", "E_lower", "E_upper", "r"):
            tk.used.add(c[k])
        body.append("<tr>" + f'<th scope="row">r = {html.escape(c["r"])}</th>'
                    + f'<td class="num interval" data-src="{html.escape(c["__src"])}">{v}</td>'
                    + f'<td class="num interval" data-src="{html.escape(c["__src"])}">{e}</td>'
                    + text_cell("yes" if c["accepted"] == "true" else "no", "basis") + "</tr>")
    thead = ('<thead><tr><th scope="col">Strength</th><th scope="col" class="num">Enclosure of v</th>'
             '<th scope="col" class="num">Enclosure of E</th><th scope="col">All predicates true</th></tr></thead>')
    return table("certificates", thead, body, cls="intervals")


GENERATORS = {
    "auction_primitives": t_auction_primitives,
    "equilibrium_controls": t_equilibrium_controls,
    "welfare": t_welfare,
    "extensions": t_extensions,
    "reserve_comparisons": t_reserve_comparisons,
    "comparative_statics": t_comparative_statics,
    "thresholds": t_thresholds,
    "certificates": t_certificates,
}


def render_tables(root: Path | str) -> tuple[dict[str, str], set[str]]:
    """Return ``({slot: html}, raw_tokens_used)``."""
    root = Path(root)
    tk = Tokens()
    out = {name: gen(root, tk) for name, gen in GENERATORS.items()}
    return out, tk.used


if __name__ == "__main__":
    tables, used = render_tables(Path(__file__).resolve().parents[1])
    for name, h in tables.items():
        print(f"{name}: {len(h)} bytes")
    print(f"{len(used)} raw tokens")
