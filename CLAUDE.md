# CLAUDE.md

Research repository for "Competition Creates Competition: Stock Prices and the Discovery of
Takeover Bidders". Three layers: the paper (`paper/`), the numerical layer (`numerics/`),
and the figure and table layer (`figures/`, `tables/`, `figures_data/`, generated).

## Source of truth

- `paper/online_appendix.md` section C is the numerical contract for numerical work: input declarations
  (C.0), one subsection per exercise (C.1 to C.7), the scalar registry (C.8). Section E is the
  implementation contract and rendering rules. Consult those sections for changes to numerics or rendering.
- `paper/quantity_manifest.csv` defines every `[[name]]` placeholder in `paper/main.md`:
  definition, exercise, source file, row selector, display format. Rows with `input_value`
  are declarations; every other row is filled only from validated output.
- From 30 September 2026, the editable manuscript masters are the Overleaf Git
  working copy at `overleaf/paper/main.tex` and `overleaf/paper/online_appendix.tex`.
  Read `overleaf/README.md` and the working copy's `AGENTS.md`; pull the author's
  latest Overleaf edits before revising. The parent repository ignores these
  independent Git working copies through its local `.git/info/exclude`.
- `paper/main.md` and `paper/online_appendix.md` are preserved migration records;
  the latter still defines the existing numerical contract in sections C and E.
  The numerical layer fills placeholders into its historical generated copies
  (`paper/*_filled.md`). Do not regenerate over the editable Overleaf LaTeX from
  these older Markdown files. Numerical updates and exports to published paper
  copies require an explicit, validated reconciliation step.
  In the preserved Markdown, figure and table positions are marked by `<!-- FIGURE N: path -->` or `<!-- TABLE N: path -->`
  followed by a `> **Figure N.** caption` blockquote; captions are the author's text.

## Conventions (from Online Appendix E.3 and E.4)

- Pure functions with full type hints; every function takes the parameter record first and
  returns immutable records. Exact decimal inputs are parsed as decimals, never through a
  binary float, wherever a certificate depends on them.
- Layers are separate modules: auction payoffs; information and price construction;
  unilateral-deviation evaluation; equilibrium search; independent validation; rendering. A
  search returns candidates and unresolved nodes; only the validation layer assigns
  `accepted`. Renderers never solve, never change a parameter, never drop a branch.
- CSV is the only boundary between numerics and presentation. Column names are the
  transliterations fixed in C.0 (`h, ell, p, rho, c_L, c_H, b, k, r, Delta_T, B_prior, q_H,
  q_L, e_H, e_L, E, O_H, R_T, tau, x_star`). Join on the full parameter declaration and
  branch label, never on a rounded scalar.
- Tolerances are the numerical-controls declaration in C.0. A breached acceptance bound
  terminates validation; a tolerance is never loosened to obtain an accepted row.
- Result status uses the paper's vocabulary: analytical, computer-assisted, numerical
  diagnostic, open; declarations carry `input`. A failed or unresolved node stays open and is
  never interpolated or replaced with zero.
- Figures: vector PDF, embedded fonts, no in-figure titles, `(a)/(b)` panel labels, broken
  lines at unresolved nodes, interval bars on certified points.
- Every completed exercise writes a run manifest: inputs, method, tolerances, software
  versions, output hashes, pass/fail.

## Working rules

- Use the GitHub repository and remote specified in `README.md` for source control, issues,
  and pull requests. Website publishing is a separate Cloudflare action under `handout/README.md`.

- Verification for numerical changes and full release/readiness claims: a single script under `numerics/`
  that reruns every acceptance check and the placeholder substitution and exits nonzero on
  any breach or unresolved required placeholder.
- Commit at the end of each exercise with an informative subject. Never commit the virtual
  environment or generated PDFs other than the built manuscript at delivery.
- Tool internals (agent names, delegation tooling, session mechanics) stay out of this file,
  the paper, and any project document.

## Verification scope

For documentation-only changes or read-only assessments, use relevant static/source checks.
For focused implementation changes, run the affected checks and dependent renders. Full
release/readiness claims require all applicable gates. Keep verification-only requests
read-only; an authorized implementation caller repairs failures caused by its changes and
reruns the affected checks. Preserve tolerances, provenance, and unresolved-result labels.

## Related work

For the supervisor handout, read `handout/README.md`. For the teaching course, read
`learn/MISSION.md`. For cross-machine updates, use the instructions in `README.md`.
The completed peer-circulation revision is recorded in `audit/peer_polish/completion_report.md`;
`VM_START_HERE.md` retains the historical transfer instructions.
