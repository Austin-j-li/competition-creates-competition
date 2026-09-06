"""Render figures and tables from validated CSV outputs and write the render manifest.

Usage:
    python numerics/render/render_all.py                 # figures, tables, quantity dictionary
    python numerics/render/render_all.py --tables-only   # tables and quantity dictionary only
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, read_csv, sha256, write_manifest  # noqa: E402
from numerics.render import quantity_dictionary, tables  # noqa: E402

MAIN_TABLES = ("table1_auction_primitives.tex", "table2_equilibrium_controls.tex", "table3_extensions.tex", "table4_reserve_comparisons.tex")
ONLINE_TABLES = ("table_matched_price.tex", "table_extensions_margins.tex", "table_signal_grid.tex", "table_reserve_details.tex",
                 "table_reserve_exploratory.tex")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    tables_only = "--tables-only" in argv
    figs = []
    if not tables_only:
        from numerics.render import figures
        figs = figures.render_all()
    tabs = tables.render_all()
    dictionary = quantity_dictionary.render()
    outs = [str(p.relative_to(ROOT)) for p in figs + tabs + dictionary]
    names = {p.name for p in tabs}
    checks = {"figures": [str(p.name) for p in figs], "tables": [str(p.name) for p in tabs],
              "dictionary": [str(p.relative_to(ROOT)) for p in dictionary], "tables_only": tables_only,
              "figure1_present": any(p.name == "two_returns.pdf" for p in figs),
              "figure2_present": any(p.name == "equilibrium_correspondence.pdf" for p in figs),
              "figure3_present": any(p.name == "posterior_tail_entry.pdf" for p in figs),
              "figure4_present": any(p.name == "bargaining_weight.pdf" for p in figs),
              "table_quantities_resolved": all("[[unresolved]]" not in p.read_text() for p in tabs if p.suffix == ".tex"),
              "dictionary_resolved": all(r["status"] != "open" for r in read_csv("replication/quantity_registry.csv")),
              "main_tables_present": all(n in names for n in MAIN_TABLES),
              "online_tables_present": all(n in names for n in ONLINE_TABLES)}
    passed = (checks["main_tables_present"] and checks["online_tables_present"] and checks["table_quantities_resolved"]
              and checks["dictionary_resolved"] and (tables_only or all(checks[f"figure{n}_present"] for n in range(1, 5))))
    inputs = ["figures_data/two_returns.csv", "figures_data/posterior_tails.csv", "figures_data/bargaining.csv",
              "tables/auction_primitives.csv", "tables/equilibrium_controls.csv", "tables/extensions.csv", "tables/reserve_comparisons.csv",
              "numerics/correspondence.csv", "numerics/mixed_supports.csv", "numerics/certificates.csv", "numerics/thresholds.csv", "numerics/moderate_values.csv",
              "numerics/two_signals.csv", "numerics/feedback_comparisons.csv", "numerics/reserve_events.csv", "numerics/reserve_ranges.csv",
              "numerics/price_pool_regression.csv", "numerics/quantity_registry.csv", "paper/quantity_manifest.csv"]
    write_manifest("render", {"sources": ["figures_data/*.csv", "tables/*.csv", "numerics/correspondence.csv", "numerics/certificates.csv",
                                          "numerics/thresholds.csv", "numerics/moderate_values.csv", "numerics/two_signals.csv",
                                          "numerics/feedback_comparisons.csv", "numerics/reserve_events.csv", "numerics/reserve_ranges.csv",
                                          "numerics/quantity_registry.csv", "paper/quantity_manifest.csv"],
                              "source_hashes": {p: sha256(p) for p in inputs}},
                   "matplotlib PDF backend, embedded Type 42 fonts, no in-figure titles, (a)/(b) panel labels, broken lines at gaps in accepted "
                   "nodes, interval bars at certified points; booktabs LaTeX tables assembled from validated rows only, with identity checks "
                   "(matched price, reserve outcome cross-source agreement) that raise on breach; quantity dictionary generated from the "
                   "manifest and the resolved registry.", {}, outs, checks, passed)
    for o in outs:
        print(o)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
