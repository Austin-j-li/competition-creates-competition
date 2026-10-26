"""The slot registry and the data script of the handout (order-slot version).

    import slot_data
    registry = slot_data.read_registry(ROOT)        # key -> row
    payload = slot_data.build_data(ROOT, registry)  # -> window.CCC_DATA

Every number on the page comes from one file, the registry of the order-slot manuscript:
audit/slot_manuscript_2026_10_23/registry/registry.csv, with the columns key, value, display,
status, source_script, run_log and note. The manuscript prints the same rows through \\reg{key}
(slot/manuscript/numbers.tex). The page prints each row's display, so a number on the page and
the same number in the PDF agree to the last digit.

The data script carries the declared primitives and the marked strengths of the example's path.
The charts draw curves from the closed forms of the manuscript at these declarations; markers and
labels use the registry rows themselves. Nothing here solves for an equilibrium. Stdlib only.
"""
from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

REGISTRY = "audit/slot_manuscript_2026_10_23/registry/registry.csv"
COLUMNS = ["key", "value", "display", "status", "source_script", "run_log", "note"]

# Declarations that the charts and the explorer read, by the name the scripts use.
INPUTS = {
    "h": "prim_h", "ell": "prim_ell", "p": "prim_p", "pi": "prim_pi", "rho": "prim_rho",
    "c_H": "prim_cH", "k": "prim_k", "r0": "prim_r0", "r1": "prim_r1", "r2": "prim_r2",
    "beta": "beta_B", "a": "res_a",
}
# Rows derived from the declarations: the slot, the posterior bounds, the marked strengths of the
# example's path and of its research equilibria, and the points that the figures label.
DERIVED = {
    "lambda": "lambda_B", "b": "b_B", "b0": "b0_B", "u": "u_B", "M": "M_half_B", "m": "m_half_B",
    "cap": "res_cap", "rA": "rA", "rF": "rF_B", "rN": "rN", "rJ": "rJ", "rS": "rS_B", "rC": "rC_B",
    "rR": "res_rR", "rRbar": "res_rcap", "rU": "res_rUR",
    "entry_floor": "entry_r0", "entry_plateau": "entry_r1_B", "entry_rA": "entry_rA_B",
    "entry_rR": "res_entry_rR", "lambda_rR": "res_lambda_rR", "entry_cap": "res_entry_cap",
    "rQ": "res_rQ", "lambda_floor_rQ": "res_lambda_floor_rQ",
    "tau_r0": "tau_r0", "tau_r1": "tau_r1", "tau_r2": "tau_r2",
    "Delta_r0": "Delta_r0", "Delta_r1": "Delta_r1", "Delta_r2": "Delta_r2",
    "Bprior_r0": "Bprior_r0", "Bprior_r1": "Bprior_r1_B", "Bprior_r2": "Bprior_r2",
    "r140": "str_r140", "r160": "str_r160",
}
# The three intermediate strengths of the research proposition and their registry rows.
NODES = [("str_r155", "res_lambda_r155", "res_entry_r155"), ("str_r160", "res_lambda_r160", "res_entry_r160"),
         ("str_r165", "res_lambda_r165", "res_entry_r165")]


class DataError(RuntimeError):
    pass


def sha256(root: Path, rel: str = REGISTRY) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


def read_registry(root: Path) -> dict[str, dict]:
    with (root / REGISTRY).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != COLUMNS:
            raise DataError(f"{REGISTRY}: columns {reader.fieldnames}, expected {COLUMNS}")
        rows = list(reader)
    out: dict[str, dict] = {}
    for row in rows:
        if row["key"] in out:
            raise DataError(f"{REGISTRY}: duplicate key {row['key']}")
        out[row["key"]] = row
    return out


def to_float(value: str) -> float:
    """A registry value is a decimal or an exact fraction; parse it exactly, then round once."""
    return float(Fraction(value.strip()))


def entry(registry: dict, key: str) -> dict:
    row = registry.get(key)
    if row is None:
        raise DataError(f"registry has no row {key}")
    return {"key": key, "value": row["value"], "display": row["display"], "x": to_float(row["value"])}


def build_data(root: Path, registry: dict | None = None) -> dict:
    registry = registry or read_registry(root)
    payload = {
        "registry": {"path": REGISTRY, "sha256": sha256(root)},
        "inputs": {name: entry(registry, key) for name, key in INPUTS.items()},
        "derived": {name: entry(registry, key) for name, key in DERIVED.items()},
        "nodes": [{"r": entry(registry, r), "lambda": entry(registry, lam), "entry": entry(registry, e)}
                  for r, lam, e in NODES],
    }
    return payload


def emit_js(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
