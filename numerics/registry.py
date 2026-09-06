"""Quantity registry (C.8): every placeholder resolved from validated output rows or exact inputs."""
from __future__ import annotations

import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN, Context, Decimal, getcontext, localcontext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from numerics.io import ROOT, read_csv, write_csv, write_manifest  # noqa: E402
from numerics.params import (BENCHMARK_STRENGTHS, MODERATE_STRENGTHS, SIGNAL_STRENGTHS)  # noqa: E402

REGISTRY_COLUMNS = ["name", "value", "lower", "upper", "units", "display", "exercise", "parameter_set", "branch", "status",
                    "source_file", "source_row", "definition", "candidate_id", "continuation_id", "parameter_set_id",
                    "institution_id", "information_structure_id", "tie_rule_id"]

# Registry decimal context (16.2 item 8): fixed here, independent of the ambient context and import order.
REGISTRY_PRECISION = 60
REGISTRY_ROUNDING = ROUND_HALF_EVEN

# Units vocabulary (16.2 item 4). "percentage_point" is a difference of two probabilities times 100; it is never
# mixed with "probability" or "percentage" in one key.
VALID_UNITS = frozenset({
    "model units", "probability", "percentage", "percentage_point", "payoff per share", "payoff margin", "order units",
    "surplus per share", "standard deviations", "payoff per marginal order", "version", "bound",
})
STATUS_VOCABULARY = ("analytical", "computer-assisted", "numerical diagnostic", "open", "input")

# Sources without a per-row status column: evidence class fixed by the exercise that produces them.
# Every other source must carry a status column; a missing one resolves to open, never to analytical.
SOURCE_DEFAULT_STATUS = {
    "numerics/certificates.csv": "computer-assisted",   # outward interval enclosures with a global deviation cover
    "numerics/thresholds.csv": "analytical",            # closed-form boundaries with independently checked residuals
    "tables/auction_primitives.csv": "analytical",      # closed-form auction payoffs checked against direct integration
}
STATUS_COLUMNS = ("status", "existence_status", "validation_status", "result_status")
# Columns that carry the continuation identity when a source has them; the recorded branch names the exact
# candidate rather than a rounded scalar (16.2 item 2).
IDENTITY_COLUMNS = ("candidate_id", "continuation_id", "parameter_set_id")

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
            if k.strip() in out:
                raise ValueError(f"duplicate selector field: {k.strip()}")
            out[k.strip()] = v.strip()
    return out


def _dec(x: str) -> Decimal:
    return Decimal(x)


def _same_value(cell: str, declared: str) -> bool:
    """Exact comparison of a source cell with a declared selector value: as decimals when both parse, else as strings."""
    try:
        return Decimal(cell) == Decimal(declared)
    except Exception:
        return cell == declared


def fmt_display(display: str, value: str | None, lower: str | None, upper: str | None) -> tuple[str, bool]:
    """Return (text, ok). ok is False when a strict-sign requirement fails."""
    if display != "literal_string":
        for scalar in (value, lower, upper):
            if scalar is not None and not Decimal(scalar).is_finite():
                raise ValueError(f"nonfinite registry scalar: {scalar}")
    if lower is not None and upper is not None and Decimal(lower) > Decimal(upper):
        raise ValueError(f"reversed enclosure: [{lower}, {upper}]")
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
    if src == "numerics/quantity_registry.csv" and sel_text.strip().startswith("pp_change"):
        # change in preparation in percentage points, 100 (E_strong - E_weak), from the resolved probability rows
        sel = parse_selector(sel_text)
        strong, weak = tables["__registry__"].get(sel.get("strong", "")), tables["__registry__"].get(sel.get("weak", ""))
        if strong is None or weak is None or strong["status"] == "open" or weak["status"] == "open":
            reg.update(value="n/a", status="open", display="[[unresolved]]", branch="component probability unresolved")
            return reg
        if strong["units"] != "probability" or weak["units"] != "probability" or man["units"] != "percentage_point":
            raise ValueError(f"{name}: percentage-point change requires two probability rows and units percentage_point")
        val = (Decimal(strong["value"]) - Decimal(weak["value"])) * 100
        text, _ = fmt_display(man["display"], str(val), None, None)
        classes = {strong["status"], weak["status"]}
        st = "analytical" if classes == {"analytical"} else "computer-assisted" if "computer-assisted" in classes and "numerical diagnostic" not in classes else "numerical diagnostic"
        reg.update(value=str(val), status=st, display=text, branch=f"{sel['strong']} minus {sel['weak']}")
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
                ok &= _same_value(r[k], v)
            elif k in ("declared moderate comparison", "benchmark inputs", "all certificate predicates", "all predicates accepted",
                       "declared comparison", "tau"):
                pass
            else:
                ok = False
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
    for key in REGISTRY_COLUMNS[13:]:
        reg[key] = row.get(key, "n/a")
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
    if value in ("", "n/a"):
        reg.update(value="n/a", status="open", display="[[unresolved]]", branch="source value not applicable")
        return reg
    text, ok = fmt_display(man["display"], value, lower, upper)
    if man["units"] in ("probability", "percentage") and not Decimal(0) <= Decimal(value) <= Decimal(1):
        raise ValueError(f"{name}: probability {value} outside [0,1]")
    st_text = next((row[c] for c in STATUS_COLUMNS if row.get(c)), None) or SOURCE_DEFAULT_STATUS.get(src, "open")
    st = status_class(st_text)
    if not ok:
        st = "open"
        text = "[[unresolved]]"
        reg["branch"] = "displayed sign does not support the strict inequality"
    else:
        ident = next((row[c] for c in IDENTITY_COLUMNS if row.get(c)), None)
        reg["branch"] = row.get("branch") or row.get("experiment") or ident or (f"({row['q_H']},{row['q_L']})" if "q_H" in row else "n/a")
        if ident and reg["branch"] != ident:
            reg["branch"] = f"{reg['branch']}; {ident}"
    reg.update(value=value, status=st, display=text)
    return reg


def registry_context() -> Context:
    return Context(prec=REGISTRY_PRECISION, rounding=REGISTRY_ROUNDING)


def build_registry(manifest: list[dict] | None = None) -> tuple[list[dict], list[str]]:
    """Resolve quantities with fixed precision, independent of import order and of the ambient context.

    Hard failures (raised): duplicate manifest keys, an unknown unit, an unknown display rule. Soft failures
    (returned in `problems`, row left open): a selector matching zero or several accepted rows, a missing source.
    """
    with localcontext(registry_context()):
        if getcontext().prec != REGISTRY_PRECISION or getcontext().rounding != REGISTRY_ROUNDING:
            raise RuntimeError("registry context not established")
        if manifest is None:
            manifest = read_csv("paper/quantity_manifest.csv")
        names = [m["name"] for m in manifest]
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            raise ValueError(f"duplicate manifest keys: {dupes}")
        bad_units = sorted({m["units"] for m in manifest if m["units"] not in VALID_UNITS})
        if bad_units:
            raise ValueError(f"unknown units in manifest: {bad_units}")
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
        problems = []
        for r in registry:
            if r["status"] not in STATUS_VOCABULARY:
                raise ValueError(f"{r['name']}: status {r['status']!r} outside the vocabulary")
            if r["status"] == "open":
                problems.append(f"open: {r['name']} ({r['branch']})")
            elif r["units"] in ("probability", "percentage") and not Decimal(0) <= Decimal(r["value"]) <= Decimal(1):
                raise ValueError(f"{r['name']}: probability {r['value']} outside [0,1]")
        return registry, problems

def main() -> bool:
    registry, problems = build_registry()
    write_csv("numerics/quantity_registry.csv", REGISTRY_COLUMNS, registry)
    n_open = sum(1 for r in registry if r["status"] == "open")
    print(f"registry: {len(registry)} rows, {n_open} open")
    for p in problems:
        print("  ", p)
    write_manifest("c8_registry", {"manifest": "paper/quantity_manifest.csv"}, "Resolve each manifest row from its declared "
                   "source file and selector; use a local 60-digit decimal context; require a unique accepted source row; "
                   "format only after validation.",
                   {}, ["numerics/quantity_registry.csv"],
                   {"open_rows": n_open, "problems": problems, "registry_precision": REGISTRY_PRECISION,
                    "registry_rounding": REGISTRY_ROUNDING, "ambient_precision_at_call": getcontext().prec}, n_open == 0)
    return n_open == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
