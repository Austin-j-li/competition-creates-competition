"""Quantity registry (C.8): every placeholder resolved from validated output rows or exact inputs."""
from __future__ import annotations

import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from numerics.io import ROOT, read_csv, write_csv, write_manifest  # noqa: E402
from numerics.params import (BENCHMARK_STRENGTHS, MODERATE_STRENGTHS, SIGNAL_STRENGTHS)  # noqa: E402

REGISTRY_COLUMNS = ["name", "value", "lower", "upper", "units", "display", "exercise", "parameter_set", "branch", "status",
                    "source_file", "source_row", "definition"]

STRENGTHS = {"base": BENCHMARK_STRENGTHS, "moderate": MODERATE_STRENGTHS, "signal": SIGNAL_STRENGTHS,
             "value classes": BENCHMARK_STRENGTHS, "cost mixture": BENCHMARK_STRENGTHS}

# Column selected for keys whose manifest selector does not name a column.
KEY_COLUMN = {
    "entry": "E", "ownership": "O_H", "spread": "Delta_T", "profit_prior": "B_prior", "revenue": "R_T",
    "matched_dividend": "matched_dividend", "flow_threshold": "x_star", "threshold_noise_sd": "threshold_noise_sd",
    "high_derivative_lower": "Gamma_H_lower", "v_interval": ("v_lower", "v_upper"), "entry_interval": ("E_lower", "E_upper"),
    "psi_left_lower": "Psi_left_lower", "psi_right_upper": "Psi_right_upper",
    "margin_low_cost": "zeta_L", "margin_high_prior": "zeta_H0", "margin_high_ceiling": "zeta_H1",
    "margin_weak_trade": "zeta_0", "margin_strong_trade": "zeta_1",
}
THRESHOLD_KEYS = {"base_m", "base_M", "base_r_pool_unique_sufficient", "base_r_no_trade_exact", "base_r_full_unique_sufficient",
                  "base_r_high_cost_ceiling", "base_laplace_entry_ceiling_left_limit"}


def _column_for(name: str, selector: dict) -> str | tuple[str, str]:
    if "column" in selector:
        return selector["column"]
    if name in THRESHOLD_KEYS:
        return "value"
    for token, col in sorted(KEY_COLUMN.items(), key=lambda kv: -len(kv[0])):
        if f"_{token}_" in f"_{name}_":
            return col
    raise KeyError(f"no column mapping for {name}")


def parse_selector(sel: str) -> dict:
    out = {}
    for part in sel.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _dec(x: str) -> Decimal:
    return Decimal(x)


def fmt_display(display: str, value: str | None, lower: str | None, upper: str | None) -> tuple[str, bool]:
    """Return (text, ok). ok is False when a strict-sign requirement fails."""
    if display in ("exact_input", "literal_string"):
        return value, True
    if display == "percent_integer":
        pct = (_dec(value) * 100).quantize(Decimal(1), rounding=ROUND_HALF_EVEN)
        return f"{pct}\\%", True
    if display.startswith("decimal_"):
        n = int(display.split("_")[1])
        return format(_dec(value).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_EVEN), "f"), True
    if display == "scientific_10":
        d = _dec(value)
        return f"{d:.9E}".replace("E+", "e+").replace("E-", "e-"), d > 0
    if display.startswith("outward_interval_"):
        n = int(display.split("_")[2])
        q = Decimal(1).scaleb(-n)
        lo = format(_dec(lower).quantize(q, rounding=ROUND_FLOOR), "f")
        hi = format(_dec(upper).quantize(q, rounding=ROUND_CEILING), "f")
        return f"[{lo},\\,{hi}]", True
    if display.startswith("lower_bound_"):
        n = int(display.split("_")[2])
        d = _dec(lower if lower is not None else value)
        while True:
            t = d.quantize(Decimal(1).scaleb(-n), rounding=ROUND_FLOOR)
            if t != 0 or n >= 40:
                break
            n += 1  # print additional outward digits rather than a zero sign
        return format(t, "f"), t > 0
    if display.startswith("upper_bound_"):
        n = int(display.split("_")[2])
        d = _dec(upper if upper is not None else value)
        while True:
            t = d.quantize(Decimal(1).scaleb(-n), rounding=ROUND_CEILING)
            if t != 0 or n >= 40:
                break
            n += 1
        return format(t, "f"), t < 0
    raise ValueError(display)


def status_class(text: str) -> str:
    t = (text or "").lower()
    if t.startswith("analytical"):
        return "analytical"
    if t.startswith("computer-assisted"):
        return "computer-assisted"
    if t.startswith("numerical diagnostic"):
        return "numerical diagnostic"
    return "open"


def resolve_row(man: dict, tables: dict) -> dict:
    name, src, sel_text = man["name"], man["source_file"], man["source_row"]
    reg = {"name": name, "units": man["units"], "display": man["display"], "exercise": man["exercise"],
           "parameter_set": man["parameter_set"], "branch": "n/a", "source_file": src, "source_row": sel_text,
           "definition": man["definition"], "lower": "n/a", "upper": "n/a"}
    if man["input_value"]:
        text, _ = fmt_display(man["display"], man["input_value"], None, None)
        reg.update(value=man["input_value"], status="input", display=text)
        return reg
    if src == "input manifest":  # percentage views of declared inputs
        base = {"a": "signal_trader_accuracy_value", "d": "signal_buyer_accuracy_value"}[sel_text.strip()]
        inp = next(m for m in tables["__manifest__"] if m["name"] == base)["input_value"]
        text, _ = fmt_display(man["display"], inp, None, None)
        reg.update(value=inp, status="input", display=text)
        return reg
    if src == "numerics/quantity_registry.csv":  # minimum of the five margins, computed from resolved rows
        prefix = name.replace("minimum_theorem_margin", "margin_")
        comps = [tables["__registry__"].get(prefix + s) for s in ("low_cost", "high_prior", "high_ceiling", "weak_trade", "strong_trade")]
        if any(c is None or c["status"] == "open" for c in comps):
            reg.update(value="n/a", status="open", display="[[unresolved]]", branch="component margin unresolved")
            return reg
        vals = [Decimal(c["value"]) for c in comps]
        mn = min(vals)
        text, ok = fmt_display(man["display"], str(mn), None, None)
        classes = {c["status"] for c in comps}
        reg.update(value=str(mn), status=("analytical" if classes == {"analytical"} and ok else "open" if not ok else "numerical diagnostic"),
                   display=text if ok else "[[unresolved]]", branch="min of five margins")
        return reg
    if src not in tables:
        reg.update(value="n/a", status="open", display="[[unresolved]]", branch=f"source file missing: {src}")
        return reg
    rows = tables[src]
    sel = parse_selector(sel_text)
    if src == "tables/equilibrium_controls.csv" and "experiment" not in sel:
        sel["experiment"] = "feedback"  # C.8: distributional keys refer to the equilibrium, not the fixed-profile control
    strengths = STRENGTHS.get(man["parameter_set"], BENCHMARK_STRENGTHS)
    filt = []
    for r in rows:
        ok = True
        for k, v in sel.items():
            if k == "column":
                continue
            if k == "boundary":
                ok &= r.get("boundary") == v
                continue
            if k == "r":
                v = strengths.get(v, v)
                ok &= Decimal(r["r"]) == Decimal(v) if r.get("r") not in (None, "", "n/a") else False
                continue
            if k == "tau" and v == "benchmark strong threshold":
                ok &= r.get("tau_label") == "benchmark"
                continue
            if k in ("epsilon_V", "p") and k in r:
                ok &= Decimal(r[k]) == Decimal(v)
                continue
            if k in r:
                ok &= r[k] == v
            elif k in ("a", "d") and k in r:
                ok &= Decimal(r[k]) == Decimal(v)
            elif k in ("declared moderate comparison", "benchmark inputs", "all certificate predicates", "all predicates accepted",
                       "declared comparison", "tau"):
                pass
        if "accepted" in r and ok:
            ok &= r["accepted"] == "true"
        if src == "tables/extensions.csv" and ok:
            ok &= r.get("parameter_set") == man["parameter_set"]
        if src == "figures_data/posterior_tails.csv" and ok and sel.get("tau") == "benchmark strong threshold":
            ok &= r.get("tau_label") == "benchmark"
        if ok:
            filt.append(r)
    if len(filt) != 1:
        reg.update(value="n/a", status="open", display="[[unresolved]]",
                   branch=f"{len(filt)} accepted rows match selector" if filt or rows else "no rows")
        return reg
    row = filt[0]
    col = _column_for(name, sel)
    if isinstance(col, tuple):
        lower, upper = row[col[0]], row[col[1]]
        value = str((Decimal(lower) + Decimal(upper)) / 2)
        reg.update(lower=lower, upper=upper)
    else:
        value = row[col]
        lower = upper = None
        if col.endswith("_lower") or col == "Psi_left_lower":
            lower = value
        if col.endswith("_upper"):
            upper = value
        if src == "numerics/certificates.csv":
            reg.update(lower=lower or "n/a", upper=upper or "n/a")
    if value in ("", "n/a", "nan"):
        reg.update(value="n/a", status="open", display="[[unresolved]]", branch="source value not applicable")
        return reg
    text, ok = fmt_display(man["display"], value, lower, upper)
    st_text = row.get("status") or row.get("existence_status") or ("computer-assisted" if src == "numerics/certificates.csv" else "analytical")
    if src == "numerics/thresholds.csv":
        st_text = "analytical"
    st = status_class(st_text)
    if not ok:
        st = "open"
        text = "[[unresolved]]"
        reg["branch"] = "displayed sign does not support the strict inequality"
    else:
        reg["branch"] = row.get("branch") or row.get("experiment") or (f"({row['q_H']},{row['q_L']})" if "q_H" in row else "n/a")
    reg.update(value=value, status=st, display=text)
    return reg


def build_registry() -> tuple[list[dict], list[str]]:
    manifest = read_csv("paper/quantity_manifest.csv")
    tables = {"__manifest__": manifest, "__registry__": {}}
    for src in sorted({m["source_file"] for m in manifest}):
        if (ROOT / src).exists() and src.endswith(".csv") and src != "numerics/quantity_registry.csv":
            tables[src] = read_csv(src)
    registry = []
    deferred = []
    for m in manifest:
        if m["source_file"] == "numerics/quantity_registry.csv":
            deferred.append(m)
            continue
        row = resolve_row(m, tables)
        registry.append(row)
        tables["__registry__"][row["name"]] = row
    for m in deferred:
        row = resolve_row(m, tables)
        registry.append(row)
        tables["__registry__"][row["name"]] = row
    names = [r["name"] for r in registry]
    problems = []
    if len(set(names)) != len(names):
        problems.append("duplicate registry names")
    for r in registry:
        if r["status"] == "open":
            problems.append(f"open: {r['name']} ({r['branch']})")
    return registry, problems


def main() -> bool:
    registry, problems = build_registry()
    write_csv("numerics/quantity_registry.csv", REGISTRY_COLUMNS, registry)
    n_open = sum(1 for r in registry if r["status"] == "open")
    print(f"registry: {len(registry)} rows, {n_open} open")
    for p in problems:
        print("  ", p)
    write_manifest("c8_registry", {"manifest": "paper/quantity_manifest.csv"}, "Resolve each manifest row from its declared "
                   "source file and selector; require a unique accepted source row; format only after validation.",
                   {}, ["numerics/quantity_registry.csv"], {"open_rows": n_open, "problems": problems}, n_open == 0)
    return n_open == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
