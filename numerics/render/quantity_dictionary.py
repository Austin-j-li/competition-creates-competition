"""Generate replication/quantity_dictionary.md: every registry key with its definition, units, exercise, source
file, selector, status, and displayed value (spec 13.5, 16.2).

The dictionary is a lookup companion generated from paper/quantity_manifest.csv and the resolved registry
numerics/quantity_registry.csv. It never types a value: the registry is rebuilt here from the manifest with the
registry's own decimal context, and an open row is printed as open. The machine-readable counterparts are the
manifest and registry CSVs themselves.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv, write_csv  # noqa: E402
from numerics.registry import REGISTRY_COLUMNS, REGISTRY_PRECISION, REGISTRY_ROUNDING, build_registry  # noqa: E402

OUT_DIR = ROOT / "replication"
OUT_MD = OUT_DIR / "quantity_dictionary.md"
OUT_CSV = OUT_DIR / "quantity_registry.csv"


def _cell(text: str) -> str:
    return (text or "").replace("|", r"\|").replace("\n", " ").strip()


def _code(text: str) -> str:
    t = (text or "").replace("|", r"\|")
    return f"`{t}`" if t else ""


def render() -> list[Path]:
    manifest = read_csv("paper/quantity_manifest.csv")
    registry, problems = build_registry(manifest)
    by_name = {r["name"]: r for r in registry}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(OUT_CSV, REGISTRY_COLUMNS, registry)
    groups: dict[str, list[dict]] = {}
    for m in manifest:
        groups.setdefault(m["exercise"], []).append(m)
    n_open = sum(1 for r in registry if r["status"] == "open")
    lines = [
        "# Quantity dictionary",
        "",
        "Every `[[key]]` placeholder used by the manuscript and the online appendix, generated from "
        "`paper/quantity_manifest.csv` (declarations, selectors, display rules) and the resolved registry "
        "`numerics/quantity_registry.csv` (a copy is `replication/quantity_registry.csv`). Each key resolves from one "
        "validated output row selected by the full parameter declaration and, where the source carries it, the "
        "continuation identity; rows with an input value are declarations. Status uses the paper's vocabulary "
        "(analytical, computer-assisted, numerical diagnostic, open) plus `input` for declarations. Displays are "
        "formatted after validation: outward rounding for interval enclosures, conservative rounding for one-sided "
        "bounds, half-even rounding otherwise.",
        "",
        f"Registry decimal context: precision {REGISTRY_PRECISION}, rounding {REGISTRY_ROUNDING} (established locally by "
        f"`numerics/registry.py`, independent of the ambient context). Keys: {len(registry)}; open: {n_open}.",
        "",
        "Units: `probability` (a probability in [0,1]); `percentage` (a probability times 100, shown with a percent sign); "
        "`percentage_point` (a difference of two probabilities times 100); `payoff per share`, `surplus per share`, "
        "`payoff margin`, `payoff per marginal order` (model value units per target share); `order units` (investor order "
        "scale); `model units` (declared primitives); `standard deviations`; `version` (software metadata).",
        "",
    ]
    if problems:
        lines += ["Unresolved keys at generation time:", ""] + [f"- {p}" for p in problems] + [""]
    for exercise in sorted(groups, key=lambda e: (e.split("/")[0], e)):
        lines += [f"## Exercise {exercise}", "",
                  "| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |",
                  "|---|---|---|---|---|---|---|---|"]
        for m in groups[exercise]:
            r = by_name[m["name"]]
            selector = m["input_value"] and f"declared input {m['input_value']}" or m["source_row"]
            value = r["display"] if r["status"] != "open" else "open"
            if r["lower"] not in ("n/a", "") and r["upper"] not in ("n/a", ""):
                value += f" (enclosure [{r['lower']}, {r['upper']}])"
            lines.append("| " + " | ".join([_code(m["name"]), _cell(m["definition"]), _code(m["units"]), _code(m["display"]),
                                             _code(m["source_file"]), _code(selector), _code(r["status"]),
                                             _cell(value)]) + " |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    return [OUT_MD, OUT_CSV]


if __name__ == "__main__":
    for p in render():
        print(p)
