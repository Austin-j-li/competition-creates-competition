# Draft text for replication/README.md

(Draft written during the S4/S5 online-appendix pass. Copy into `replication/README.md`;
adjust once the Makefile targets exist. Voice: repository documentation, not manuscript prose.)

---

# Replication

Every number in the two manuscripts comes from one of the exercises below, through the
quantity registry. Nothing is typed by hand. Run everything from the repository root with the
project interpreter, `PY=.venv/bin/python` (Python 3.12, NumPy, SciPy, mpmath, matplotlib;
each run records the versions it used in its manifest).

## Entry points

| Target | What it does |
|---|---|
| `make peer-release` | Validates the required calculations, regenerates the registry, tables, figures, and filled manuscripts, typesets both PDFs, runs `numerics/verify.py --final`, and assembles the peer package. |
| `make peer-reproduce` | Runs the same declared sequence in a fresh working and output directory, with no accepted result carried over, and compares canonical numerical outputs, exact input declarations, certificate validity, resolved references, and extracted manuscript text with the release. PDFs are not compared byte for byte (matplotlib and pdfTeX stamp dates). |

## Producers (raw numerical exercises; Online Appendix C)

| Command | Exercise | Writes | Notes |
|---|---|---|---|
| `$PY numerics/exercises/c1_baseline.py` | C.1 baseline, controls, extensions | `tables/auction_primitives.csv`, `tables/equilibrium_controls.csv`, `tables/extensions.csv`, `numerics/baseline_deviations.csv`, `numerics/feedback_comparisons.csv`, `figures_data/two_returns.csv`, `numerics/manifests/c1_baseline.json` | seconds |
| `$PY numerics/exercises/c2_correspondence.py [--workers=N] [--quick]` | C.2 correspondence and certificates | `numerics/thresholds.csv`, `numerics/certificates.csv`, `numerics/correspondence.csv`, `numerics/mixed_supports.csv`, `numerics/manifests/c2_correspondence.json` | about one hour on 8 workers |
| `$PY numerics/exercises/c3_signals.py` | C.3 complementary signals | `numerics/two_signals.csv`, `numerics/two_signal_deviations.csv`, `numerics/manifests/c3_signals.json` | seconds |
| `$PY numerics/exercises/c4_moderate.py` | C.4 moderate values, nonemptiness | `numerics/moderate_values.csv`, `numerics/moderate_controls.csv`, `numerics/nonemptiness_construction.csv`, `numerics/manifests/c4_moderate.json` | seconds |
| `$PY numerics/exercises/c5_noise.py` | C.5 noise laws, posterior tails | `figures_data/posterior_tails.csv`, `numerics/manifests/c5_noise.json` | seconds |
| `$PY numerics/exercises/c6_reserve.py [--workers=N] [--quick]` | C.6 reserve comparisons and sweep | `tables/reserve_comparisons.csv`, `numerics/reserve_continuations.csv`, `numerics/reserve_ranges.csv`, `numerics/manifests/c6_reserve.json` | about one hour on 8 workers |
| `$PY numerics/exercises/c6b_price_pools.py` | C.6b price-pool regression | `numerics/price_pool_regression.csv`, `numerics/manifests/c6b_price_pools.json` | minutes |
| `$PY numerics/exercises/c6c_reserve_events.py [--workers=N]` | C.6c exact reserve events | `numerics/reserve_events.csv`, `numerics/reserve_event_ranges.csv`, `numerics/manifests/c6c_reserve_events.json` | minutes |
| `$PY numerics/exercises/c7_bargaining.py` | C.7 bargaining weights | `figures_data/bargaining.csv`, `numerics/manifests/c7_bargaining.json` | seconds |

Each producer validates its own candidates (the search layer returns candidates; only the
validation layer marks a row accepted), writes CSV through `numerics/io.write_csv` (shortest
round-trip floats, `n/a` for missing), and writes a manifest with the SHA-256 of every output.
`verify.py` refuses an output whose hash no longer matches its manifest, so rerunning the
producer is the only way to change a number.

## Presentation (in order)

| Command | Role |
|---|---|
| `$PY numerics/check_registry.py` | Regenerates the registry in fresh processes under several ambient decimal precisions and import orders; asserts identical output; writes nothing. |
| `$PY numerics/registry.py` | Builds `numerics/quantity_registry.csv` and `numerics/manifests/c8_registry.json` from `paper/quantity_manifest.csv` and the validated CSVs. Exits 1 if any required row is open. |
| `$PY numerics/substitute.py` | Fills `paper/main_filled.md` and `paper/online_appendix_filled.md` from the registry. Writes nothing if a placeholder is unknown or open. |
| `$PY numerics/render/render_all.py` | Renders `figures/*.pdf` and `tables/table*.tex` from the CSVs; records hashes in `numerics/manifests/render.json`. No solving. |
| `$PY numerics/render/latex.py` | Converts the filled Markdown to LaTeX with pandoc (citeproc, `references.bib`) and typesets with latexmk/pdfTeX into `paper/main_filled.pdf` and `paper/online_appendix_filled.pdf`. |
| `$PY numerics/verify.py --final` | The gate: every manifest passed, every hash matches, the C.1 declared nodes revalidate, the three C.2 certificates and threshold residuals recompute, the registry rebuilds, strict substitution succeeds, the handout builds. Exit 1 on any failure. `--rerun` also re-executes C.1, C.3, C.4, C.5, C.7 and the renderer. |

## File roles

| Path | Role |
|---|---|
| `paper/main.md`, `paper/online_appendix.md` | Editable manuscript sources with `[[name]]` placeholders. |
| `paper/quantity_manifest.csv` | Placeholder specification: definition, exercise, source file, row selector, display, units; exact values for declared inputs. |
| `numerics/quantity_registry.csv` | Generated registry: one row per placeholder with value, bounds, status, source row. |
| `replication/quantity_dictionary.md` | Generated, human-readable version of the manifest and registry: every key with its definition and provenance. |
| `replication/run_manifest.json` | Generated summary of the producing runs (inputs, methods, tolerances, software, output hashes, pass/fail). |
| `numerics/params.py` | Exact decimal input declarations (Online Appendix C.0) and the `Controls` tolerances. |
| `numerics/*.py` | Numerical layers: `auction.py`, `noise.py`, `information.py`, `deviations.py`, `quadrature.py`, `search.py`, `validation.py`, `continuations.py`, `reserve_events.py`, `certificates.py`, `thresholds.py`, `signals.py`, `io.py`. |
| `numerics/render/` | Figure and table renderers and the LaTeX driver. |
| `numerics/manifests/` | One JSON manifest per exercise, plus registry, render, and handout manifests. |
| `tables/*.csv`, `figures_data/*.csv`, `numerics/*.csv` | Validated outputs (the only boundary between numerics and presentation). |
| `tables/*.tex`, `figures/*.pdf` | Rendered tables and figures. |
| `paper/*_filled.md`, `paper/*_filled.tex`, `paper/*_filled.pdf` | Generated manuscripts. |
| `references.bib` | Bibliography. |
| `verification/` | Independent seed checks delivered before the numerical layer; not read by the build. Reproduce with `python review_checks.py --out results --mode core|signals`, `explore_asymmetric.py`, `certify_asymmetric.py` from inside that directory. |
| `audit/peer_polish/` | Audit records: claim ledger, issue ledger, source-output map, logs, completion report. |

## Statuses

Rows carry one of `analytical`, `computer-assisted`, `numerical diagnostic`, `open`
(declarations carry `input`). A failed or unresolved node stays open; it is never interpolated,
replaced with zero, or dropped. Negative controls and duplicate starts stay in the CSVs with
`accepted = false` and their reason.
