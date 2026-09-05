# Repository map (stage S0)

Repository root: `/Users/austinli/Projects/competition-creates-competition`
Branch `peer-circulation-fix`, commit `1cb7475b84835cb7d9793459b1b372b96f401b99`
("Shorten the handout to a ten-minute default path", 2026-09-05 22:24:37 +0100). Tracked tree clean;
no untracked non-ignored files. Interpreter: `.venv/bin/python` (Python 3.12.13, NumPy 2.5.2,
SciPy 1.18.1, mpmath 1.4.1, matplotlib 3.11.1). All commands below run from the repository root
with `PY=.venv/bin/python`.

The spec's companion `reference_material/` folder and `reference_oracles.py` are not present
locally. The two reviewed PDFs are the tracked `paper/main_filled.pdf` and
`paper/online_appendix_filled.pdf` (hashes match spec §1.1 exactly; `docs/` holds byte-identical
copies). The handoff document H is `HANDOFF.md`. The end-to-end review file
`CCC_Assembled_Manuscript_E2E_Review.md` is not in the repository.

Every path is resolved by `numerics/io.py` as `ROOT = Path(__file__).resolve().parent.parent`, so a
copied tree builds against its own files. No script reads an environment variable. No script reads
a results directory other than the paths named below.

## 1. Semantic roles (spec §1.2)

| Role | Actual path | Source or generated | Produced by | Consumed by |
|---|---|---|---|---|
| Main manuscript (editable) | `paper/main.md` | source (author prose, `[[name]]` placeholders, `<!-- FIGURE N: path -->` / `<!-- TABLE N: path -->` markers with caption blockquotes) | author | `numerics/substitute.py`, `handout/build.py` (indirectly through filled copy) |
| Online appendix (editable) | `paper/online_appendix.md` | source; section C is the numerical contract, C.8 the registry spec, E the implementation contract | author | `numerics/substitute.py` |
| Bibliography | `references.bib` (named in `paper/main.md` front matter `bibliography: references.bib`) | source | author | pandoc `--citeproc --bibliography references.bib` inside `numerics/render/latex.py` |
| Placeholder manifest | `paper/quantity_manifest.csv` (118 rows: 40 input declarations with `input_value`, 78 derived) | source (input declarations are the C.0 contract) | author/collaborator | `numerics/registry.py`, `numerics/substitute.py`, `numerics/verify.py`, `handout/build.py` |
| Quantity registry (C.8) | `numerics/quantity_registry.csv` (+ manifest `numerics/manifests/c8_registry.json`) | generated | `$PY numerics/registry.py` (also rewritten by `verify.py`) | `substitute.py`, `verify.py`, `handout/build.py` |
| Filled manuscripts | `paper/main_filled.md`, `paper/online_appendix_filled.md` | generated (tracked) | `$PY numerics/substitute.py` (also rewritten by `verify.py --final`) | `numerics/render/latex.py` |
| Pandoc input with figure/table environments | `paper/main_filled.tex.md`, `paper/online_appendix_filled.tex.md` | generated (tracked) | `latex.py` `convert()` | pandoc |
| LaTeX sources | `paper/main_filled.tex`, `paper/online_appendix_filled.tex` | generated (tracked) | pandoc via `latex.py` | latexmk |
| LaTeX aux dir | `paper/build/` (`.aux .log .fls .fdb_latexmk`) | generated, gitignored | latexmk | latexmk (incremental) |
| PDFs | `paper/main_filled.pdf`, `paper/online_appendix_filled.pdf` (tracked with `git add -f`; `paper/*.pdf` is gitignored); copies in `docs/` | generated | `latex.py` moves `paper/build/<name>.pdf` to `paper/<name>.pdf` | readers; `handout/build.py` links them |
| Tables: validated CSV | `tables/auction_primitives.csv`, `tables/equilibrium_controls.csv`, `tables/extensions.csv` (C.1); `tables/reserve_comparisons.csv` (C.6) | generated, hash-locked by exercise manifests | `c1_baseline.py`, `c6_reserve.py` | `registry.py`, `render/tables.py`, `handout/data.py` |
| Tables: LaTeX | `tables/table1_auction_primitives.tex`, `table2_equilibrium_controls.tex`, `table3_extensions.tex`, `table4_reserve_comparisons.tex`, `table_signal_grid.tex` | generated (tracked), hash-locked by `render.json` | `$PY numerics/render/render_all.py` (`numerics/render/tables.py`) | `\input{}` from the `.tex.md` environments built by `latex.py` |
| Figure data | `figures_data/two_returns.csv` (C.1), `figures_data/posterior_tails.csv` (C.5), `figures_data/bargaining.csv` (C.7) | generated, hash-locked | `c1_baseline.py`, `c5_noise.py`, `c7_bargaining.py` | `render/figures.py`, `registry.py`, `handout/data.py` |
| Figures | `figures/two_returns.pdf`, `equilibrium_correspondence.pdf`, `posterior_tail_entry.pdf`, `bargaining_weight.pdf` (gitignored; hashes recorded in tracked `numerics/manifests/render.json`) | generated | `render_all.py` (`numerics/render/figures.py`, matplotlib PDF backend, Type 42 fonts, STIXGeneral) | `\includegraphics` in the compiled PDFs |
| Exercise C.1 baseline | `numerics/exercises/c1_baseline.py` | source | — | writes the three `tables/*.csv`, `numerics/baseline_deviations.csv`, `numerics/feedback_comparisons.csv`, `figures_data/two_returns.csv`, `manifests/c1_baseline.json` |
| Exercise C.2 correspondence and certificates | `numerics/exercises/c2_correspondence.py` (flags `--workers=N`, `--quick`) | source | — | writes `numerics/thresholds.csv`, `certificates.csv`, `correspondence.csv`, `mixed_supports.csv`, `manifests/c2_correspondence.json`; about one hour on 8 workers (default workers = cpu_count-2) |
| Exercise C.3 signals | `numerics/exercises/c3_signals.py` | source | — | writes `numerics/two_signals.csv`, `two_signal_deviations.csv`, `manifests/c3_signals.json` |
| Exercise C.4 moderate values | `numerics/exercises/c4_moderate.py` | source | — | writes `numerics/moderate_values.csv`, `moderate_controls.csv`, `nonemptiness_construction.csv`, `manifests/c4_moderate.json` |
| Exercise C.5 noise laws | `numerics/exercises/c5_noise.py` | source | — | writes `figures_data/posterior_tails.csv`, `manifests/c5_noise.json` |
| Exercise C.6 reserve | `numerics/exercises/c6_reserve.py` (flags `--workers=N`, `--quick`) | source | — | writes `tables/reserve_comparisons.csv`, `numerics/reserve_continuations.csv`, `reserve_ranges.csv`, `manifests/c6_reserve.json`; about one hour on 8 workers; committed manifest was produced on Linux x86_64 (others on macOS arm64) |
| Exercise C.7 bargaining | `numerics/exercises/c7_bargaining.py` | source | — | writes `figures_data/bargaining.csv`, `manifests/c7_bargaining.json` |
| Shared numerical layers (E.3) | `numerics/params.py` (exact decimal declarations, `Controls` tolerances), `auction.py`, `quadrature.py`, `information.py`, `noise.py`, `signals.py`, `deviations.py`, `search.py`, `validation.py`, `thresholds.py`, `exercises/common.py` | source | — | imported by exercises, `verify.py` |
| Certificate port (Appendix B) | `numerics/certificates.py` (`certify()`; ported from `verification/certify_asymmetric.py`, predicates recorded not asserted; mpmath interval arithmetic from decimal strings) | source | — | `c2_correspondence.py`, `verify.py` (re-certifies `CERTIFICATE_BRACKETS` from `params.py`) |
| Legacy verification seed (E.2) | `verification/review_checks.py`, `explore_asymmetric.py`, `certify_asymmetric.py`, `requirements.txt`, `results/` (7 files) | reference, kept as delivered; not imported by `numerics/` | collaborator | manual reproduction per OA E.1 (`python review_checks.py --out results --mode core|signals`, etc.); nothing in the build reads it |
| Build entry points | `numerics/check_registry.py`, `numerics/registry.py`, `numerics/substitute.py`, `numerics/render/render_all.py`, `numerics/render/latex.py`, `numerics/verify.py`, `handout/build.py` | source | — | see build graph |
| TeX template | none as a file; `HEADER_META`, `HEADER_INCLUDES`, `APPENDIX_INCLUDES` dicts/lists in `numerics/render/latex.py` become pandoc YAML front matter (article, 12pt/11pt, newtxtext+newtxmath, geometry margin=1in, linestretch 2 / 1.15) | source | — | pandoc `--standalone` default LaTeX template |
| Bibliography processor | pandoc citeproc (`--citeproc --bibliography references.bib`; CSL default); bibtex/biber are installed but not used | tool | — | — |
| PDF engine | `latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=paper/build <tex>` → pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026); no `latexmkrc` in repo or `$HOME` | tool | — | — |
| Dependency declarations | none pinned in-repo for `numerics/`: `README.md` says `pip install numpy scipy mpmath matplotlib`; `verification/requirements.txt` is for the legacy seed only; versions are recorded per run in each `numerics/manifests/*.json` (`software` field) and in OA E.1 placeholders `seed_*_version` | source/doc | — | — |
| Run manifests | `numerics/manifests/c1_baseline.json` … `c7_bargaining.json`, `c8_registry.json`, `render.json`, `handout.json` | generated (tracked) | `numerics.io.write_manifest` from each producer; `handout/build.py` writes `handout.json` without a timestamp | `numerics/verify.py` (checks `passed` and every output SHA-256) |
| Handout (supervisor page) | `handout/*` (source), `docs/index.html`, `docs/.nojekyll` (generated) | source / generated | `$PY handout/build.py --quiet` (also run by `verify.py --final`) | GitHub Pages |
| Verify skill | `.claude/skills/verify-ccc/SKILL.md` | source | — | operator |
| Author notes | `paper/polish_notes.md`, `KICKOFF_PROMPT.md`, `HANDOFF.md`, `CLAUDE.md`, `README.md` | source | author | — |
| Ignored local material | `paper/drafts/part{1,2,3}.md`, `.venv/`, `paper/build/`, `figures/*.pdf`, `__pycache__/`, `.claude/settings.local.json`, `.DS_Store` | untracked | — | — |

## 2. Build graph (spec §5 S0-B), in producing order

Steps 1–7 are the raw numerical exercises; steps 8–13 are the presentation rebuild that OA E.1
documents. Each exercise writes its CSVs through `numerics.io.write_csv` (repr floats, `n/a` for
missing) and then its manifest with SHA-256 of every output; `verify.py` refuses any output whose
hash no longer matches its manifest, so outputs are never edited by hand and a rerun of an
exercise is the only way to change them.

1. `exact inputs + numerical source → raw candidates → independent validation → accepted tables`
   - Inputs: `numerics/params.py` (decimal strings, `Controls` tolerances = OA C.0) and
     `paper/quantity_manifest.csv` `input_value` rows (parsed as `Decimal`, never through float
     where a certificate depends on them).
   - `$PY numerics/exercises/c1_baseline.py` → `tables/{auction_primitives,equilibrium_controls,extensions}.csv`, `numerics/{baseline_deviations,feedback_comparisons}.csv`, `figures_data/two_returns.csv`, `numerics/manifests/c1_baseline.json`.
   - `$PY numerics/exercises/c2_correspondence.py` (about 1 h, 8 workers; `--quick` for a reduced run; NOT run in S0) → `numerics/{thresholds,certificates,correspondence,mixed_supports}.csv`, `manifests/c2_correspondence.json`. Search (`search.py`) returns candidates and unresolved nodes; `validation.py` assigns `accepted`; `certificates.py` produces outward intervals.
   - `$PY numerics/exercises/c3_signals.py` → `numerics/{two_signals,two_signal_deviations}.csv`, `manifests/c3_signals.json`.
   - `$PY numerics/exercises/c4_moderate.py` → `numerics/{moderate_values,moderate_controls,nonemptiness_construction}.csv`, `manifests/c4_moderate.json`.
   - `$PY numerics/exercises/c5_noise.py` → `figures_data/posterior_tails.csv`, `manifests/c5_noise.json`.
   - `$PY numerics/exercises/c6_reserve.py` (about 1 h, 8 workers; NOT run in S0) → `tables/reserve_comparisons.csv`, `numerics/{reserve_continuations,reserve_ranges}.csv`, `manifests/c6_reserve.json`.
   - `$PY numerics/exercises/c7_bargaining.py` → `figures_data/bargaining.csv`, `manifests/c7_bargaining.json`.
2. `$PY numerics/check_registry.py` — regression only, writes nothing. Spawns 12 subprocesses (3 import orders × ambient decimal precision 12/28/60/80) calling `numerics.registry.build_registry()` and asserts identical JSON and an untouched ambient context. About 3.4 s.
3. `accepted tables → quantity registry`: `$PY numerics/registry.py` — reads `paper/quantity_manifest.csv` and every CSV it names, resolves each row under `decimal.localcontext(Context(prec=60, rounding=ROUND_HALF_EVEN))`, formats displays (`decimal_n`, `outward_interval_n`, `lower_bound_n`, …). OVERWRITES `numerics/quantity_registry.csv` and `numerics/manifests/c8_registry.json` (timestamp changes every run). Exit 1 if any row is open.
4. `registry → filled sources`: `$PY numerics/substitute.py` — OVERWRITES `paper/main_filled.md` and `paper/online_appendix_filled.md`; exits 1 and writes nothing if a placeholder is unknown or open (`--force` writes anyway).
5. `accepted tables → figures and tables`: `$PY numerics/render/render_all.py` — `figures.py` reads `numerics/{correspondence,certificates,thresholds}.csv` and `figures_data/*.csv`; `tables.py` reads `tables/*.csv`, `numerics/{feedback_comparisons,two_signals,moderate_values,reserve_ranges}.csv`. OVERWRITES `figures/*.pdf` (4), `tables/table*.tex` (5), and `numerics/manifests/render.json`. No solving. About 1 s.
6. `filled sources + figures + tables → typesetting → PDFs`: `$PY numerics/render/latex.py` — for each of `paper/main_filled.md`, `paper/online_appendix_filled.md`: replaces `<!-- FIGURE/TABLE -->` markers by raw-LaTeX float environments (captions converted with `pandoc -f markdown+tex_math_dollars -t latex`), strips cross-document links, prepends generated YAML front matter, and OVERWRITES `paper/<name>.tex.md`; then `pandoc <tex.md> -o paper/<name>.tex --standalone --citeproc --bibliography references.bib --resource-path <ROOT> -f markdown+tex_math_dollars+raw_attribute --shift-heading-level-by=-1`; then `latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=paper/build paper/<name>.tex` (cwd = ROOT, pdfTeX); then moves `paper/build/<name>.pdf` to `paper/<name>.pdf` (OVERWRITES the tracked PDFs). About 3 s with warm `paper/build/`.
7. Gate: `$PY numerics/verify.py --final` — checks every manifest `passed` and every output hash; re-validates the C.1 declared nodes (r = 1.2, 3, 3.6), re-runs the three C.2 certificates and threshold residuals; rebuilds the registry and OVERWRITES `numerics/quantity_registry.csv`; runs strict substitution and OVERWRITES both `paper/*_filled.md`; runs `handout/build.py --quiet`, which OVERWRITES `docs/index.html`, `docs/.nojekyll`, `numerics/manifests/handout.json`. `--rerun` additionally re-executes C.1, C.3, C.4, C.5, C.7 and `render_all.py`. Exit 1 on any FAIL.

## 3. Side effects and gotchas for later stages

- Decimal context: only `registry.py` touches it, and only through `localcontext`; the ambient
  context is left unchanged (asserted by `check_registry.py`). Nothing sets `getcontext().prec`
  globally.
- Nondeterministic metadata: matplotlib stamps `/CreationDate` in each `figures/*.pdf`, so every
  `render_all.py` run changes the four figure hashes and therefore the tracked
  `numerics/manifests/render.json`; `verify.py` then requires the local figure PDFs to match that
  manifest. pdfTeX stamps `/CreationDate`, `/ModDate`, and `/ID` in the manuscript PDFs, and the
  re-stamped figures are embedded, so the PDFs are never byte-reproducible. `SOURCE_DATE_EPOCH`
  is not set anywhere; matplotlib and pdfTeX would honor it if a later stage wants reproducible
  bytes.
- `latex.py` does not run `latexmk -C`; it relies on `paper/build/` for incremental passes. A
  cold `paper/build/` needs several pdflatex passes (longer runtime, same result).
- `verify.py --final` writes tracked files (registry, filled Markdown, `docs/index.html`,
  `handout.json`) even when it only verifies; run it in a copy if the tree must stay clean.
- `handout/build.py` is part of the final gate and reads the registry, manifest, and validated
  CSVs; the handout's `vendor.lock.json` pins CDN assets and `--verify-vendor` fetches them.
- The exercise manifests record `platform`; C.6 was produced on Linux x86_64, C.1–C.5, C.7 on
  macOS arm64. A rerun of C.6 on this Mac is expected to change its manifest even when the CSVs
  agree; the hash check is on outputs, not on the platform string.
- `c2_correspondence.py` and `c6_reserve.py` default to `cpu_count - 2` workers and take about
  an hour each on 8 workers.

## 4. Working-tree observation during S0

The tree was clean at commit `1cb7475b` when S0 started and when the isolated copy was taken
(copy verified byte-equal to HEAD for the manuscript, appendix, manifest, bibliography, and
handout sections). From about 22:34 local time another process began editing the working tree:
`paper/main.md` and `handout/sections/*.html` now differ from HEAD, and untracked `learn/` and an
empty `audit/peer_polish/reference_seed/` appeared. S0 made none of these changes and did not
touch them. The baseline in `baseline_manifest.json` is defined by the HEAD blobs, not by the
current working tree; later stages must check `git status` before building.
