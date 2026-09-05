# Handoff: build the numerical layer and the filled manuscript

Date: 2026-09-05. Repository: `AustinJunyuLi/competition-creates-competition` (private),
local worktree `/Users/austinli/Projects/competition-creates-competition`, branch `main`.

## What this is

A second-year PhD upgrade paper by Austin Li. The manuscript and online appendix were
drafted by an external collaborator to a specification; the numbers in the manuscript are
`[[name]]` placeholders that this repository's numerical layer must produce. The author's
brief for the paper is bold framing with ownership of every result; status labels
(analytical, computer-assisted, numerical diagnostic, open) carry the caveats. The prose is
not to be edited by the execution session.

The model in one paragraph: a listed target is sold by second-price cash auction with reserve
$p$; an incumbent bidder has value $R\sim U[0,r]$; a challenger has value $\theta\in\{\ell,h\}$
and must pay a private preparation cost ($c_L$ or $c_H$) to learn it and bid; an informed
speculator trades the target's shares (orders in $[-1,1]$, linear cost $k$, Laplace noise of
scale $b$); a competitive market maker prices order flow; the challenger observes the price,
not the flow. Stronger incumbents lower the challenger's profit at every belief but raise the
information spread of target proceeds $\Delta_T=(r-\ell)^2/(2r)$, which switches informed
trading on and can raise entry.

## What is in the repository

- `paper/main.md`: manuscript with paper appendix; 87 unique placeholders.
- `paper/online_appendix.md`: full proofs (A), interval-certificate method (B), numerical
  contract (C.0 to C.8), empirical pilot design (D), reproducibility (E).
- `paper/quantity_manifest.csv`: 118 placeholder rows; 40 are input declarations with
  values, 78 are derived quantities to compute. Every placeholder in the two Markdown files
  has a manifest row; 27 manifest rows are registry-only (`required_in_main = no`).
- `CLAUDE.md`: conventions distilled from Online Appendix E.

Not delivered yet by the collaborator, and to be requested from the author: `references.bib`
(named in the `main.md` front matter) and the `verification/` directory listed in Online
Appendix E.2 (`review_checks.py`, `explore_asymmetric.py`, `certify_asymmetric.py`,
`results/`). The exercises do not depend on those files, but the interval certificates in
C.2 should reproduce the collaborator's brackets, and porting its `certify_asymmetric.py` is
faster than reimplementing Appendix B from scratch.

## Deliverables of the execution session

1. `numerics/`: a Python package implementing Online Appendix C in the layered structure of
   E.3, with a `verify.py` gate that reruns all acceptance checks and exits nonzero on any
   breach.
2. The output files named in C.1 to C.7 (`tables/`, `numerics/*.csv`, `figures_data/`), each
   with a run manifest.
3. `numerics/quantity_registry.csv` per C.8, and a substitution step that produces
   `paper/main_filled.md` and `paper/online_appendix_filled.md` from the registry, failing
   if any required placeholder is unresolved.
4. Figures 1 to 4 and Tables 1 to 4 as specified in the placeholders of `paper/main.md`
   section 10 and elsewhere (grep `placeholder —` in `paper/main.md`), rendered per E.4.
5. LaTeX conversion of the filled manuscript and online appendix, and a compiled PDF of each,
   once the author supplies `references.bib`.

## Suggested order

The order follows placeholder dependency and reuse of the same solver.

1. **C.1 baseline** (feeds about half the placeholders): auction layer with independent
   integration; pooling and full-order equilibria at $r\in\{1.2,3,3.6\}$; the five theorem
   margins $\zeta$; controls (frozen profile, price hidden, matched dividend); logistic noise;
   uniform-mixture costs; welfare at strong strength.
2. **C.2 thresholds and certificates**: exact boundaries $\mathfrak r(k)$, $r_N$, $r_U$,
   $r_C$, $m$, $M$, the Laplace left limit; then the correspondence on the declared grid; then
   the asymmetric branch $(1,-v)$ by continuation; then interval certificates at the three
   declared nodes (Appendix B); then the pure $(u,-v)$ and finite-support mixed searches with
   open flags where unresolved.
3. **C.4 moderate values** and the nonemptiness construction sequence.
4. **C.3 complementary signals**: the declared example and the $5\times5$ accuracy sweep.
5. **C.5 noise laws and tails**, **C.7 bargaining weights** (both cheap, fixed-profile).
6. **C.6 reserve comparisons** and the exploratory seller continuation sweep (the most
   expensive exercise; run last, in the background, with found-continuation ranges only).
7. Registry, substitution, figures, tables, verification gate, LaTeX.

## Cross-checks available from an earlier independent implementation

These values were computed independently of the collaborator's code and reproduce its
reports. Use them as a first sanity gate for C.1 and C.2; the acceptance checks in C.0 remain
the standard.

| Quantity | Value |
|---|---|
| Entry at $r=1.2$, $r=3$ (feedback) | 0.250000, 0.522757 |
| Frozen-profile entry at $r=1.2$ | 0.562178 |
| High-quality ownership at $r=3$ | 0.324192 |
| Revenue at $r=3$, feedback / hidden | 0.872392 / 0.614583 |
| Net-surplus gain at $r=3$ | 0.080217534 |
| Logistic threshold, entry at $r=3$ | 5.4246, 0.301509 |
| Reserve 1.01 entry at $r=1.2$, $r=3$ | 0.543573 / 0.513373 |
| $r_N$, $r_U$, $r_C$ | 1.7478775, 2.8374170, 3.5926585 |
| Asymmetric $v^*$ at $r=1.55,1.60,1.65$ | 0.460316, 0.707475, 0.903332 |
| Entry on that branch | 0.545053, 0.548756, 0.551361 |
| Full-order entry at $r=1.70$, $3.55$ | 0.552, 0.508 |
| Moderate example entry ($h=2$, $k=0.002$) at $r=1.5$ | 0.526805 |

Known structure of the correspondence under the benchmark: no trade is the unique outcome
below $\mathfrak r(k)=1.221$; no trade exists up to $r_N=1.748$; the asymmetric branch
begins between $r=1.50$ and $1.55$ with $v$ rising to 1 near $r=1.70$; full orders are a best
response from about $r=1.70$ and unique from $r_U$; expensive entry is infeasible above
$r_C$. A second fixed point at $r=1.55$ ($v\approx0.21$, cutoff on the region boundary) was
seen and should be classified, not discarded.

## Manuscript rewrite (2026-09-05)

After the numerical layer was delivered, the author asked for the manuscript to be rewritten in a
single-author voice with the structure and prose style of a finance journal paper (reference:
Gorbenko's JF 2024 "Auctions with Endogenous Initiation" and his 2025 handbook chapter). The main
text keeps three numbered propositions (two returns to information; competition creates
competition; coexisting informative equilibria) and states all other results as Propositions A.1
to A.9 in Appendix A. Evidentiary status is carried in prose, not in headings. Every `[[name]]`
placeholder is unchanged and the numerical contract in Online Appendix C is untouched apart from
pronouns. Figures and tables are placed by `<!-- FIGURE N: path -->` / `<!-- TABLE N: path -->`
markers followed by a caption blockquote.

## Rules for the session

- Numbers in the paper come only from validated registry rows. No hand-typed values.
- Report failures as failures; open nodes stay open; a branch is never selected for its shape.
- Prose in `paper/main.md` changes only at the author's request (the 2026-09-05 rewrite was one).
  Structural fixes (a broken cross-reference, a placeholder key mismatch) are reported to the
  author, not silently patched.
- Commit after each exercise. Never commit `.venv` or intermediate PDFs.
- No tool internals in project documents.

## Suggested skills

- `token-saver`: work from this file and the appendix sections named above; do not re-read
  the whole manuscript for each exercise.
- `ringer`: delegate C.2's correspondence and C.6's reserve sweep as one task each with the
  acceptance checks as executed checks; keep the certificate port on a high-effort worker;
  in-run checks must stay under the runner's time cap, so re-solve post-run.
- `dataviz`: before writing the figure layer.
- `unslop`: on any prose the session writes (captions, README, run notes).
- A repository-local verify skill modelled on the blockholder repo's `verify-blockholder`
  (data, figures, LaTeX compiles, gates) should be written once `numerics/verify.py` exists.

## Related material outside this repository

- Earlier independent scripts: session scratchpad `ccc/` (`verify.py`, `partial.py`,
  `mild2.py`, `asym.py`) under the blockholder project's Claude scratchpad directory.
- Memory notes in `~/.claude/projects/-Users-austinli-Projects-blockholder/memory/`:
  `astra-ccc-proposal.md`, `bold-framing-brief.md`. This repository has its own memory
  directory once a session starts here; copy the two notes across.
- The blockholder repository's `empirics/` EDGAR pipeline (stdlib only) can be reused for
  the Appendix D pilot when a case list is drawn.
