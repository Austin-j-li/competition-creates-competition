"""Registry invariants (spec 16.2, T17, T27).

Plain test functions. Run with `.venv/bin/python -m pytest numerics/tests/test_registry_invariants.py` when pytest is
installed, or `.venv/bin/python numerics/tests/test_registry_invariants.py` (the __main__ runner prints one line per
test and exits nonzero on any failure). Subprocess tests run sequentially (never more than one worker).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import traceback
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from numerics.io import read_csv  # noqa: E402
from numerics.registry import (REGISTRY_PRECISION, STATUS_VOCABULARY, VALID_UNITS, build_registry, fmt_display,  # noqa: E402
                               parse_selector)

PLACEHOLDER = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")


class Check(Exception):
    pass


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise Check(msg)


def _manifest() -> list[dict]:
    return read_csv("paper/quantity_manifest.csv")


def _registry() -> tuple[list[dict], list[str]]:
    return build_registry(_manifest())


# --- 1. unique keys ---------------------------------------------------------------------------------------
def test_unique_keys_and_duplicate_is_hard_failure():
    manifest = _manifest()
    names = [m["name"] for m in manifest]
    require(len(set(names)) == len(names), "duplicate keys in the manifest")
    dup = manifest + [dict(manifest[0])]
    try:
        build_registry(dup)
    except ValueError as e:
        require("duplicate manifest keys" in str(e), f"wrong error for a duplicate key: {e}")
    else:
        raise Check("a duplicated manifest key did not fail the build")


# --- 1. unambiguous row selection ---------------------------------------------------------------------------
def test_ambiguous_selector_is_open_and_reported():
    manifest = _manifest()
    # a selector that names only the strength matches several accepted rows (feedback at several branches, controls)
    bad = dict(next(m for m in manifest if m["name"] == "base_entry_strong"))
    bad.update(name="ambiguous_probe", source_row="noise=Laplace; cost_law=atoms")
    rows, problems = build_registry(manifest + [bad])
    probe = next(r for r in rows if r["name"] == "ambiguous_probe")
    require(probe["status"] == "open" and "rows match selector" in probe["branch"], f"ambiguous selector not left open: {probe}")
    require(any("ambiguous_probe" in p for p in problems), "ambiguous selection not reported as a problem")
    # a selector matching no row is also open
    none = dict(bad)
    none.update(name="empty_probe", source_row="noise=Laplace; cost_law=atoms; r=999")
    rows, problems = build_registry(manifest + [none])
    require(next(r for r in rows if r["name"] == "empty_probe")["status"] == "open", "empty selection not left open")


# --- 2. exact identity: every selector on a wide-schema source carries the full parameter vector -----------
def test_full_identity_selectors_on_continuation_sources():
    manifest = _manifest()
    wide = {"numerics/price_pool_regression.csv": ("h", "ell", "p", "rho", "c_L", "c_H", "b", "k", "r", "noise", "cost", "q_H", "q_L",
                                                   "cutoff_exact", "candidate_id"),
            "numerics/reserve_events.csv": ("parameter_set_id", "p_exact", "event_id", "branch")}
    for m in manifest:
        need = wide.get(m["source_file"])
        if need:
            sel = parse_selector(m["source_row"])
            missing = [k for k in need if k not in sel]
            require(not missing, f"{m['name']}: selector lacks identity fields {missing}")
    # the registry branch of a pool key records the candidate identity, not a rounded scalar
    rows, _ = _registry()
    pool = [r for r in rows if r["source_file"] == "numerics/price_pool_regression.csv"]
    require(pool and all(r["branch"].startswith("c6b:") for r in pool), "pool keys do not record the candidate identity")
    require(all(r["candidate_id"] != "n/a" and r["continuation_id"] != "n/a" for r in pool), "complete pool identities omitted")
    expected = {"pool_reserve"} | {f"pool_{quantity}_cutoff_{end}" for quantity in ("posterior", "entry", "revenue") for end in ("low", "high")}
    require(expected == {r["name"] for r in rows if r["name"].startswith("pool_")}, "seven pool keys must all resolve")


# --- 3. required rows accepted, vocabulary -----------------------------------------------------------------
def test_required_rows_resolved_with_vocabulary_status():
    manifest = _manifest()
    rows, problems = _registry()
    by = {r["name"]: r for r in rows}
    for m in manifest:
        r = by[m["name"]]
        require(r["status"] in STATUS_VOCABULARY, f"{m['name']}: status {r['status']!r} outside the vocabulary")
        if m["required_in_main"] == "yes":
            require(r["status"] != "open", f"required key {m['name']} is open ({r['branch']})")
            require(r["display"] != "[[unresolved]]", f"required key {m['name']} unresolved")
        if m["input_value"]:
            require(r["status"] == "input" and r["value"] == m["input_value"], f"declaration {m['name']} not carried exactly")


# --- 4. units ---------------------------------------------------------------------------------------------
def test_units_valid_and_consistent():
    manifest = _manifest()
    for m in manifest:
        require(m["units"] in VALID_UNITS, f"{m['name']}: unknown units {m['units']!r}")
        if m["units"] == "percentage_point":
            require(m["display"].startswith("decimal_") and m["source_row"].startswith("pp_change"),
                    f"{m['name']}: percentage-point keys are differences of probability rows")
        if m["display"] == "percent_integer":
            require(m["units"] == "percentage", f"{m['name']}: percent display requires percentage units")
    bad = dict(manifest[0])
    bad.update(name="unit_probe", units="furlongs")
    try:
        build_registry(manifest + [bad])
    except ValueError as e:
        require("unknown units" in str(e), f"wrong error for an unknown unit: {e}")
    else:
        raise Check("an unknown unit did not fail the build")


def test_percentage_point_change_matches_probability_rows():
    rows, _ = _registry()
    by = {r["name"]: r for r in rows}
    for name, strong, weak in (("base_entry_change_pp", "base_entry_strong", "base_entry_weak"),
                               ("moderate_entry_change_pp", "moderate_entry_strong", "moderate_entry_weak"),
                               ("signal_entry_change_pp", "signal_entry_strong", "signal_entry_weak")):
        r = by[name]
        expected = (Decimal(by[strong]["value"]) - Decimal(by[weak]["value"])) * 100
        require(Decimal(r["value"]) == expected, f"{name}: {r['value']} != 100*({by[strong]['value']} - {by[weak]['value']})")
        require(r["units"] == "percentage_point" and Decimal(r["display"]) == expected.quantize(Decimal("0.01")), f"{name}: display {r['display']}")
        require(r["status"] != "open", f"{name} open")


# --- 5. outward rounding for enclosures, conservative rounding for bounds ----------------------------------
def test_outward_and_conservative_rounding():
    rows, _ = _registry()
    for r in rows:
        if r["status"] == "open":
            continue
        disp = r["display"]
        if disp.startswith("outward_interval_") or r["display"].startswith("["):
            pass
        if r["lower"] not in ("n/a", "") and r["upper"] not in ("n/a", "") and disp.startswith("["):
            lo, hi = disp.strip("[]").replace("\\,", "").split(",")
            require(Decimal(lo) <= Decimal(r["lower"]) and Decimal(hi) >= Decimal(r["upper"]),
                    f"{r['name']}: printed interval {disp} does not enclose [{r['lower']}, {r['upper']}]")
        elif r["lower"] not in ("n/a", "") and r["upper"] in ("n/a", ""):
            require(Decimal(disp) <= Decimal(r["lower"]) and Decimal(disp) > 0, f"{r['name']}: lower bound {disp} rounds inward or is not positive")
        elif r["upper"] not in ("n/a", "") and r["lower"] in ("n/a", ""):
            require(Decimal(disp) >= Decimal(r["upper"]) and Decimal(disp) < 0, f"{r['name']}: upper bound {disp} rounds inward or is not negative")
    # synthetic: rounding never crosses the true value and a sign is never manufactured
    text, ok = fmt_display("outward_interval_3", None, "0.12345", "0.12355")
    require(text == "[0.123,\\,0.124]" and ok, f"outward interval {text}")
    text, ok = fmt_display("lower_bound_3", None, "0.0004", None)
    require(Decimal(text) <= Decimal("0.0004") and Decimal(text) > 0 and ok, f"lower bound {text}")
    text, ok = fmt_display("upper_bound_3", None, None, "-0.0004")
    require(Decimal(text) >= Decimal("-0.0004") and Decimal(text) < 0 and ok, f"upper bound {text}")
    text, ok = fmt_display("lower_bound_3", None, "-0.0004", None)
    require(not ok, "a negative lower enclosure must not support a strict positive sign")
    q = Decimal("0.12345").quantize(Decimal("0.001"), rounding=ROUND_FLOOR)
    require(q == Decimal("0.123") and Decimal("0.12355").quantize(Decimal("0.001"), rounding=ROUND_CEILING) == Decimal("0.124"), "rounding modes")


# --- 6. no unresolved placeholder in the peer-facing manuscripts -----------------------------------------------
def test_no_unresolved_placeholder_in_manuscripts():
    manifest = {m["name"] for m in _manifest()}
    rows, _ = _registry()
    by = {r["name"]: r for r in rows}
    for src in ("paper/main.md", "paper/online_appendix.md"):
        text = (ROOT / src).read_text(encoding="utf-8")
        for key in sorted(set(PLACEHOLDER.findall(text))):
            require(key in manifest, f"{src}: [[{key}]] is not in the manifest")
            require(by[key]["status"] != "open", f"{src}: [[{key}]] is open ({by[key]['branch']})")


# --- 7. no NaN or infinity in finite fields -------------------------------------------------------------------
def test_no_nan_or_inf_in_finite_fields():
    rows, _ = _registry()
    for r in rows:
        if r["status"] == "open" or r["display"] in ("", "[[unresolved]]"):
            continue
        if r["source_file"] == "software metadata":
            continue
        for field in ("value", "lower", "upper"):
            v = r[field]
            if v in ("n/a", ""):
                continue
            d = Decimal(v)
            require(d.is_finite(), f"{r['name']}.{field} = {v} is not finite")
        if r["units"] == "probability" and r["source_file"] != "input manifest":
            require(Decimal("0") <= Decimal(r["value"]) <= Decimal("1"), f"{r['name']}: probability {r['value']} outside [0,1]")


def test_invalid_scalars_and_selectors_fail():
    for value in ("NaN", "Infinity", "-Infinity"):
        for display in ("decimal_6", "exact_input", "percent_integer"):
            try:
                fmt_display(display, value, None, None)
            except ValueError:
                pass
            else:
                raise Check(f"{display} accepted {value}")
    try:
        fmt_display("outward_interval_6", None, "0.4", "0.3")
    except ValueError:
        pass
    else:
        raise Check("reversed enclosure accepted")
    for value in ("-0.1", "1.1"):
        bad = dict(next(m for m in _manifest() if m["units"] == "probability" and m["input_value"]))
        bad.update(name="invalid_probability", input_value=value)
        try:
            build_registry([bad])
        except ValueError:
            pass
        else:
            raise Check(f"declared probability {value} accepted")
    bad = dict(next(m for m in _manifest() if m["name"] == "base_entry_strong"))
    bad["source_row"] += "; typo_field=wrong"
    rows, problems = build_registry([bad])
    require(rows[0]["status"] == "open" and problems, "unknown selector silently ignored")
    try:
        parse_selector("r=1.2; r=3")
    except ValueError:
        pass
    else:
        raise Check("duplicate selector field accepted")


# --- 8. precision invariance under ambient decimal contexts and import orders ----------------------------------
SCRIPT = """
import json, sys
from decimal import getcontext, ROUND_DOWN, ROUND_UP
{imports}
getcontext().prec = {precision}
getcontext().rounding = {rounding}
rows, problems = build_registry()
assert getcontext().prec == {precision} and getcontext().rounding == {rounding}, "registry leaked its context"
print(json.dumps({{"rows": rows, "problems": problems, "prec": getcontext().prec}}, sort_keys=True))
"""


def test_precision_invariance_in_fresh_processes():
    baseline = None
    combos = [("from numerics.registry import build_registry", 7, "ROUND_DOWN"),
              ("import numerics.thresholds\nfrom numerics.registry import build_registry", 28, "ROUND_UP"),
              ("from numerics.registry import build_registry\nimport numerics.thresholds", 100, "ROUND_DOWN")]
    for imports, precision, rounding in combos:  # sequential: one worker
        out = subprocess.check_output([sys.executable, "-c", SCRIPT.format(imports=imports, precision=precision, rounding=rounding)], cwd=ROOT)
        data = json.loads(out)
        require(data["prec"] == precision, "ambient precision was altered by the registry")
        payload = json.dumps({"rows": data["rows"], "problems": data["problems"]}, sort_keys=True)
        if baseline is None:
            baseline = payload
        require(payload == baseline, f"registry differs under ambient precision {precision} / {rounding} / imports {imports!r}")
    require(REGISTRY_PRECISION == 60, "registry precision declaration changed; update the recorded value in the run manifest")


# --- runner -------------------------------------------------------------------------------------------------
def main() -> int:
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL {name}: {e}")
            traceback.print_exc()
    print(f"{len(tests) - failed}/{len(tests)} registry invariant tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
