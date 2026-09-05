"""Render figures and tables from validated CSV outputs and write the render manifest."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT, write_manifest  # noqa: E402
from numerics.render import figures, tables  # noqa: E402


def main() -> int:
    figs = figures.render_all()
    tabs = tables.render_all()
    outs = [str(p.relative_to(ROOT)) for p in figs + tabs]
    checks = {"figures": [str(p.name) for p in figs], "tables": [str(p.name) for p in tabs],
              "figure1_present": any(p.name == "equilibrium_correspondence.pdf" for p in figs),
              "table4_present": any(p.name == "table4_reserve_comparisons.tex" for p in tabs)}
    write_manifest("render", {"sources": ["figures_data/*.csv", "tables/*.csv", "numerics/correspondence.csv", "numerics/certificates.csv",
                                          "numerics/thresholds.csv", "numerics/moderate_values.csv", "numerics/two_signals.csv",
                                          "numerics/reserve_ranges.csv"]},
                   "matplotlib PDF backend, embedded Type 42 fonts, no in-figure titles, (a)/(b) panel labels, broken lines at gaps in accepted "
                   "nodes, interval bars at certified points; booktabs LaTeX tables assembled from validated rows only.", {}, outs, checks, True)
    for o in outs:
        print(o)
    return 0


if __name__ == "__main__":
    sys.exit(main())
