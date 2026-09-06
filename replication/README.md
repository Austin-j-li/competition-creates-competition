# Replication

Run commands from the source directory. The paper is a theory working paper; the empirical section is a design scaffold. Numerical diagnostics describe the searched continuations and do not establish an exhaustive correspondence or an optimal reserve.

## Environment

The VM uses Python 3.12.13. `requirements.txt` pins the installed Python packages, including NumPy 2.5.2, SciPy 1.18.1, mpmath 1.4.1, matplotlib 3.11.1 and pytest 9.1.1. The typesetting tools are Pandoc 3.9, pdfTeX 3.141592653-2.6-1.40.29 from TeX Live 2026, and latexmk 4.88. Poppler supplies `pdfinfo`, `pdftotext` and `pdftoppm`. Install the TeX packages named in `numerics/render/latex.py`, including newtx, needspace, pdflscape, caption, threeparttable and fvextra.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r replication/requirements.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
```

The release runner also sets these thread limits. On the 64-vCPU / 125 GiB VM, the two broad exercises use 20 workers each. Set `WORKERS` lower on a smaller machine. A worker is a process with one native numerical-library thread; the figure and PDF builds are serial. No scientific grid or acceptance tolerance changes with the worker count.

## Entry points

`make peer-release` checks exercise manifests and numerical validity, runs the tests, builds the registry, fills both manuscripts, generates exhibits, typesets both PDFs, and packages the release. It requires a completed visual-inspection record matching every page of the generated PDFs. For a new revision, `python replication/release.py --build-only` builds the files for inspection; after completing and recording that inspection, `--package-only` rechecks numerical validity and packages them. The package step checks the source and PDF hashes against the validated build.

`make peer-reproduce` creates a separate temporary source copy, removes the generated outputs listed by the exercise manifests, runs every raw producer below, then runs the same numerical/build checks. It compares canonical CSV data and substantive extracted PDF text against the saved release. The fresh directory and comparison report are preserved at the location recorded in `audit/peer_polish/reproduction.json`. The archived source works without Git history or an existing manuscript PDF. PDF timestamps are fixed by `SOURCE_DATE_EPOCH`; comparison does not depend on byte-identical PDFs.

```bash
make peer-release WORKERS=20
make peer-reproduce WORKERS=20
```

## Raw numerical producers

These commands rebuild the calculations. The presentation commands alone do not rebuild their inputs.

| Command, after activating the environment | Outputs |
|---|---|
| `python numerics/exercises/c1_baseline.py` | Auction primitives, baseline equilibria, frozen and hidden-price controls, matched-dividend and welfare comparisons, extension rows, two-return figure data and deviation scans. |
| `python numerics/exercises/c2_correspondence.py --workers=20` | Thresholds, three interval certificates, correspondence representatives, raw candidate attempts, mixed supports and mixed-search attempts. |
| `python numerics/exercises/c3_signals.py` | Declared complementary-signal example, all 25 accuracy pairs at both strengths and both tested profiles, and deviation scans. |
| `python numerics/exercises/c4_moderate.py` | Moderate-value example, controls and nonemptiness construction. |
| `python numerics/exercises/c5_noise.py` | Posterior tails, cutoffs, noise-standardized distances and endpoint values. |
| `python numerics/exercises/c6_reserve.py --workers=20` | Fixed-reserve comparisons, broad reserve continuation attempts, found ranges and coverage records. |
| `python numerics/exercises/c6b_price_pools.py` | The 17-member price-pool family, invalid controls and complete continuation identities. |
| `python numerics/exercises/c6c_reserve_events.py --workers=8` | Exact reserve events, one-sided neighborhoods, preparation/sale/admissibility outcomes and event checks. |
| `python numerics/exercises/c7_bargaining.py` | Acquisition-payment bargaining comparisons and the figure data. |

Each producer writes its manifest in `numerics/manifests/`, with exact inputs, method, tolerances, checks, software versions and output SHA-256 hashes. Search attempts and unresolved nodes remain in the audit data. A diagnostic best-response mesh does not become an interval certificate merely because it is accepted numerically.

## Independent and presentation checks

`python audit/peer_polish/independent_checks.py --workers=8` reconstructs the retained core quantities independently of the numerical implementation. `python audit/peer_polish/certificate_checks.py` compares the preserved seed with the local interval port and checks printed enclosures. The copied legacy seed under `audit/peer_polish/reference_seed/` is unchanged; its `run_seed.sh` refuses optimized Python. The separate companion `reference_oracles.py` mentioned in the fixing specification was not supplied and was not run here.

The presentation sequence is `numerics/registry.py`, `numerics/substitute.py`, `numerics/render/render_all.py`, and `numerics/render/latex.py`. `numerics/verify.py --final` and `numerics/release_checks.py` are the final numerical gates. `python -m pytest -q numerics/tests` includes isolated corruption tests against the release boundary. The peer build does not rebuild the unrelated handout.

`quantity_dictionary.md` defines every scalar key; `quantity_registry.csv` records its source row, units, evidence class and display. Manuscript quantities are substituted from that registry. The actual command records and source/output hashes are in `run_manifest.json`, `build_manifest.json`, the exercise manifests and the audit completion report.
