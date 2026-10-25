# Plan for the theory upgrade: numbers, figures and delivery

Read PLAN.md first. Its stage order, staffing roles, cloud-only execution, decision gate and delivery restrictions override the earlier alternatives in this lens. All study-relative source paths below are relative to `audit/theory_upgrade_2026_10_25/`.

25 October 2026. Lens: numbers, figures and delivery. Master: `overleaf/slot/` at 69c25f4. Read-only
planning; the only file written is this one. Scratch evidence was produced outside the repository
(`/tmp/plan_delivery_build`, `/tmp/plan_delivery_repo`, `/tmp/plan_delivery_view`).

Evidence gathered for this plan (25 October, on this Mac):

- A scratch copy of the master builds cleanly: `main.tex` 102 pages, `comparison.tex` 16, `slides.tex` 34;
  no unknown key, no undefined reference. The stray `ty` prints at the end of the introduction's roadmap
  paragraph ("... and proves every result. ty"), just before Section 2.
- In a scratch copy of the pipeline, `make_numbers.py` reproduces `numbers.tex` and `registry.csv`
  byte for byte (5,221 keys, 0 conflicts); `number_scan.py` reports 676 keys used, 0 missing, 0 typed
  decimals. `p1_numbers.py`, `P3_research.py` and `p5_observables.py` reproduce `P1_core.csv`,
  `P3_research.csv` and `P5_observables.csv` byte for byte. Each runs in under a second.
- The committed `XP3/recompute.log` predates the second research round: it lists 65 enclosures that
  exclude the exact value; a rerun lists 0. The committed P1 logs carry the old machine's absolute paths.
- `.venv` does not exist at the repository root. `python3` is Homebrew 3.12.13 with numpy 2.4.4, mpmath
  1.4.1, matplotlib 3.10.8 and fontTools 4.62.1 (the committed figures came from matplotlib 3.11.1).
  TeX Live 2026, latexmk, xelatex, pdffonts, pdftoppm and pdftotext are installed. Fira Sans is at
  `/usr/local/texlive/2026/texmf-dist/fonts/opentype/public/fira/FiraSans-Regular.otf`.
- `p1_numbers.py` fails under `python3 -I` (it imports the sibling module `p1_common`); run it by path
  without `-I`.
- The referee computations behind the memo (114 files, 756 KB) exist only in `/tmp/ccc_wa2/`.

---

## 1. Summary

The upgrade changes what the paper proves, so its numbers, figures and companion documents change with it.
Each new number follows the existing route: an exact or interval computation, checked by a second,
independent one. Most are benchmark margins of the four named conditions; they belong in the appendix
table of margins, and the main text states the fact each supports.

The research figure changes most. Its gray band and broken axis give way to the full map of equilibria:
the equilibrium in which a researched purchase recruits keeps research at the cap until the entry
ceiling, and just above the no-trade bound a second equilibrium has research without recruitment. The
referee located the end of that second equilibrium, about 2.167, numerically; an exact computation must
confirm it before the figure or the text states it. I recommend one more figure: the coexistence region
in the plane of the spread and the threshold, with the benchmark path crossing it.

The new language rules reach beyond the theory. About ninety appendix lines name computation files, logs
or the benchmark's internal label, and the margins table has a column of file codes; all of it goes. The
comparison note carries status labels and a section on computation records, so it needs a recast or a
freeze.

The work runs on new local branches, in the Overleaf copy and in a separate checkout of the project, so
Austin's unfinished edits stay untouched; nothing is pushed without his approval. Each stage ends with the
affected computations rerun, the documents built and read, and a scan for status words, defensive
phrasing and revision-history language. the mathematics writer designs and checks the mathematics behind the new
computations, the production assistant writes code and figures, the prose writer integrates, and the second reader reads the
finished paper once.

---

## 2. Stages in dependency order

### 2.0 Language rules and the per-stage gate

Every stage's acceptance criteria include these rules, quoted from Austin's instructions:

- **L1, status labels.** "No result-status labels anywhere in the manuscript, main text or appendix: no
  'analytical', 'computer-assisted', 'numerical diagnostic', 'certified', or 'open' used as a status, in
  titles, sentences, table notes or captions." STYLE_GUIDE §2.4 (status in the proposition title) and §2.7
  (status once per cluster) are superseded.
- **L2, no defensive writing.** "State each result positively, with its scope as part of the claim. Named
  conditions are hypotheses of results, stated once; they are not apologies. No caveat or reassurance
  paragraphs, no hedges ('may', 'arguably', 'it should be noted', 'only in the benchmark' as a disclaimer),
  no pre-emptive answers to referees, no paragraph that ends on a limitation. the mathematics writer-written prose follows the
  same rule."
- **L3, no development log.** The paper "is written once, as a finished paper, with no trace of its revision
  history or its production." Banned in the main text, appendix, captions, `comparison.tex` and
  `slides.tex` alike: narrating changes ("now", "no longer", "new", "updated", "revised", "corrected",
  "replaces", "in this version", "unlike the earlier draft", "previously") when they refer to the paper;
  announcing upgrades ("this generalizes the earlier result", "the benchmark restriction is removed");
  process and pipeline words ("registry, script, exercise, checker, certificate, run, verified,
  recomputed, Sturm-count 'certificates' as objects, file names, keys, 'calibration B', workstream or
  weakness codes"); and bookkeeping sentences about what was checked. Comparative statics across strengths
  stay. "Proof methods inside appendix proofs are stated as mathematics ('an exact rational computation
  shows'), not as a record of work." This later rule narrows L1's allowance: a proof method appears only as
  mathematics, never as a file or program.
- **L0, unchanged house rules.** "I"; numbers only through `\reg{}`; no bold sentences in running text; no
  tool, reviewers or model names in the manuscript or any project document.

Per-stage gate: the language scan of S2 runs on every file the stage touched; a person or reviewers reads each
hit and records the judgment (many hits are economic, for example "orders no longer predict entry", "an
open set", "an indifferent investor may mix"). The humanizing and anti-defensive pass runs on all new prose
of the stage, the mathematics writer-written prose included.

Shell names used below:

```bash
REPO=/Users/austinli/Projects/competition-creates-competition
MASTER=$REPO/overleaf/slot                     # Overleaf master, its own Git repository
WT=/Users/austinli/Projects/ccc-theory-upgrade # parent-repository worktree, new branch
TEAM=$WT/audit/slot_manuscript_2026_10_23
BR=theory-upgrade-2026-10-25                   # branch name in both repositories
```

Standard build (inside `$MASTER`, with `build/` in `$MASTER/.git/info/exclude`):

```bash
cd $MASTER
latexmk -pdf    -interaction=nonstopmode -halt-on-error -outdir=build main.tex
latexmk -pdf    -interaction=nonstopmode -halt-on-error -outdir=build comparison.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build slides.tex
grep -n -E "Unknown registry key|undefined|Overfull" build/main.log build/comparison.log build/slides.log
pdftotext -layout build/main.pdf - | grep -n -E "\?\?|in preparation"
pdffonts build/main.pdf | grep -c "Type 3"      # expect 0
```

### Stage overview

| Stage | Name | Lens | Depends on |
|---|---|---|---|
| S0 | Preflight: archive, pull, branches, baselines | delivery | none |
| S1 | Austin's decisions | all | S0 |
| S2 | Tooling: output folder, scans, font, label map | delivery | S0 |
| S3 | Notation and vocabulary fixed | theory, main text | S1 |
| S4 | Appendix statements and proofs | theory | S3 |
| S5 | New benchmark numbers and their independent checks | delivery | S1, S2; final rows after S4 |
| S6 | Figures | delivery | S3, S5 |
| S7 | Main text | main text | S4, S5, S6 |
| S8 | Numbers in the appendix: margins table, benchmark paragraphs, proof-method sentences | delivery with theory | S4, S5 |
| S9 | Consumers: slides, comparison note, key lists | delivery | S7, S8 frozen |
| S10 | Final sweep and the one second-opinion read | delivery | S9 |
| S11 | Mirror sync, commits, delivery note; push on approval | delivery | S10, Austin |

### S0. Preflight: archive, pull, branches, baselines

- **Goal.** Secure the referee computations, start from Austin's latest Overleaf state on new branches,
  and record a baseline that every later diff is read against.
- **Files.** `audit/theory_upgrade_2026_10_25/workarounds/scratch/` (archive, untracked); `$MASTER` branch;
  `$WT` worktree; refreshed logs in `$TEAM/scripts/*`.
- **Source.** RUN_LOG; this plan's evidence list.
- **Writer and checker.** Coordinator alone; mechanical, with judgment on each diff.
- **Commands.**

  ```bash
  # 0.1 The only copy of the referee computations lives in /tmp.
  mkdir -p $REPO/audit/theory_upgrade_2026_10_25/workarounds/scratch
  cp -Rp /tmp/ccc_wa2/. $REPO/audit/theory_upgrade_2026_10_25/workarounds/scratch/
  find $REPO/audit/theory_upgrade_2026_10_25/workarounds/scratch -type f | wc -l   # 114
  # 0.2 Overleaf master: pull Austin's edits, then branch.
  git -C $MASTER fetch origin
  git -C $MASTER status --short                      # expect empty
  git -C $MASTER log --oneline HEAD..origin/main     # Austin's newer Overleaf edits, if any
  git -C $MASTER merge --ff-only origin/main
  git -C $MASTER switch -c $BR
  printf 'build/\n' >> $MASTER/.git/info/exclude
  # 0.3 Parent repository: a separate worktree on a new branch from Austin's last commit.
  git -C $REPO worktree add -b $BR $WT slot-revision   # 487619f; the main checkout stays as it is
  # 0.4 Baseline reruns in the worktree (print-only programs; run by path, without -I).
  cd $WT
  python3 audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_numbers.py
  python3 audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_certificates.py
  python3 audit/slot_manuscript_2026_10_23/scripts/P1_core/p1_enumerate.py
  (cd $TEAM/scripts/P3_research && python3 P3_research.py > P3_research.log)
  python3 audit/slot_manuscript_2026_10_23/scripts/P5_observables/p5_observables.py
  for s in xp1_numbers xp1_equilibria xp1_boundary; do python3 $TEAM/scripts/XP1/$s.py > $TEAM/scripts/XP1/$s.stdout; done
  python3 $TEAM/scripts/XP1/xp1_signs.py
  python3 $TEAM/scripts/XP1b/xp1b_recompute.py
  (cd $WT && python3 audit/slot_manuscript_2026_10_23/scripts/XP3/recompute.py > $TEAM/scripts/XP3/recompute.log)
  (cd $WT && python3 audit/slot_manuscript_2026_10_23/scripts/XP5/recompute.py > $TEAM/scripts/XP5/run_log.txt)
  git -C $WT diff --stat -- audit/slot_manuscript_2026_10_23/registry   # expect no change
  git -C $WT diff --stat                                                 # logs and receipts only
  python3 $TEAM/scripts/_coordinator/make_numbers.py                     # 5,221 keys, 0 conflicts
  python3 $TEAM/scripts/_coordinator/number_scan.py | tee $REPO/audit/theory_upgrade_2026_10_25/plan/baseline_number_scan.txt
  ```

  Then the standard build in `$MASTER`, a label map of `build/main.aux` saved beside the scan, and the
  language scan's baseline counts (after S2 exists). Do not rerun `P2_auction/derive.py`: it restores the
  display `0.000000` for `p2_reserve_points_deter_r0_two`, which the coordinator fixed by hand to `0`.
- **Acceptance.** Archive count 114. `$MASTER` on `$BR` at the pulled commit, clean. `$WT` on `$BR` at
  487619f, clean; the main checkout untouched (`git -C $REPO status` shows only Austin's own changes). No
  registry CSV changes after the reruns. Builds 102/16/34 pages (more if Austin's pulled edits add pages),
  no unknown key. One baseline commit in `$WT`: "Rerun the order-slot numbers and checks on this machine",
  with logs added by path (`git add -f` for any `.log` file, since `*.log` is ignored globally).
- **Size.** About an hour; no manuscript text.

### S1. Austin's decisions

Section 6 lists them. The delivery stages need answers to D1 (stray text), D2 (region figure), D3 (research
figure), D8 (script output folder), D9 (comparison note), D12 (numbers from non-benchmark economies) and D14
(placeholder macros) before S5 and S6 finish.

### S2. Tooling: output folder, scans, figure font, label map

- **Goal.** Make every generated file land in the master, and make the silent failure modes visible.
- **Files and changes (all print-only programs, no assertions).**
  1. `_coordinator/make_numbers.py:14`: an `--out DIR` argument (default: the mirror, as now); it prints the
     target path and the SHA-256 of the `numbers.tex` it wrote.
  2. `_coordinator/number_scan.py:9`: a `--doc DIR` argument, and three more printed lists: (a) numbers
     outside `\reg{}` with one decimal place or a fraction with a multi-digit numerator or denominator
     (the current pattern flags only two or more decimal places, so `0.4`, `6.4` or `9667/8280` pass
     unseen); (b) keys used at baseline and no longer used (orphans), read from
     `baseline_number_scan.txt`; (c) keys whose display in the folder's `numbers.tex` differs from
     `registry.csv`, or that are missing from it. List (c) catches a stale `numbers.tex`, which the
     current scan cannot see: it checks keys against the registry, while the PDF prints from `numbers.tex`.
  3. `F_figures/make_figures.py:35-39`: `--out DIR`; the Fira Sans path from `kpsewhich FiraSans-Regular.otf`
     in place of the old machine's path (today the slide figures would fall back to DejaVu Sans without a
     message); figure metadata `Creator` set to the paper title.
  4. New `_coordinator/language_scan.py --doc DIR [--pdf FILE ...]`: prints every match with file, line
     and context, by category: status words; hedges and defensive forms; revision-history words;
     process words, file names, `\nolinkurl`, `\texttt{` with an underscore, "calibration B", "at B",
     workstream codes (`P[1-5]`, `XP[1-5]`, `W[1-5]`, `LA`); tool and model names; `we`/`our`;
     `\textbf` outside headings and table heads; with `--pdf`, the text of built PDFs and figure PDFs
     (captures captions and in-figure labels) and the strings `??` and `in preparation`. It strips comment
     lines and has no exit status.
  5. New `_coordinator/label_map.py AUX [--before FILE]`: prints label, printed number and page from a
     `.aux` file, and with `--before` the labels whose printed number changed.
  6. Optional: `_coordinator/slot_rerun.sh`, which runs every exercise and checker of S0.4, then
     make_numbers, number_scan, the language scan and the three builds, prints each summary, and stops at
     the first program that exits nonzero. It replaces nothing; it saves typing.
- **Source.** Pipeline findings in SCAN Part 5 and `scan/downstream.md` §0 and §6; this plan's
  evidence list.
- **Writer and checker.** the production assistant writes; the prose writer and integrator reviews the diff and runs each tool on the baseline.
- **Verification.** Each tool on the unchanged master: make_numbers with `--out $MASTER` reproduces
  `$MASTER/numbers.tex` (`git -C $MASTER diff --stat` empty); number_scan lists (a) to (c) printed and read;
  make_figures with `--out` to a scratch folder writes eight PDFs whose talk versions embed `FiraSans`
  (`pdffonts`); the language scan's baseline counts saved.
- **Acceptance.** Defaults unchanged for the website and study guide; no assertion in any tool; L0 for
  the code comments (no model names).
- **Size.** About 250 lines of code in six files.

### S3. Notation and vocabulary (theory and main-text lenses)

Needed from this stage before S6 and S8 finish: (i) the symbol that replaces `\bar r_R` (it collides with the
support bound `\bar r`, `02_model.tex:53`); (ii) the name and subscript of the strength 2.167 where research
without recruitment ends (the independent referee writes `r_X`; `X` is the observed order, so another subscript is safer;
registry keys never print, so the key can stay `res_rX`); (iii) the words for the three research
outcomes in figure labels and notes; (iv) "the benchmark" for "calibration B" and "the signal example" for
"the vector S(B)" (SCAN Part 3, pattern 1); (v) whether the four tie phrases replace the codes IM, I0, C1
and CM in the appendix. Acceptance for my lens: one symbol per object across text, figures and A9.

### S4. Appendix statements and proofs (theory lens)

Needed from this stage: the final statement of each named condition and of each benchmark check, so that
every A9 row matches a hypothesis; which benchmark numbers each proof prints; and whether Corollary A.2,
the cap-before-selling corollary, the small-trading-cost condition (Solver A 3) and the abstaining-investor
remark stay. I ask the theory writers to apply L3 while they rewrite A4, A5 and A8: each computational step
becomes a mathematical statement of its method. S8 then handles A2, A3, A6, A7 and A9 and sweeps the rest.

### S5. New benchmark numbers and their independent checks

- **Goal.** Every number the upgraded paper prints has a registry row computed in exact rational or
  rational-interval arithmetic, a run log, and an agreeing independent recomputation.
- **Structure.** Two new exercise folders and two new checkers; existing exercises stay as they are.
  - `scripts/TU_conditions/tu_conditions.py` writes `registry/TU_conditions.csv` and its log: the margins
    of the four named conditions and the other benchmark facts of W1, W2, W4 and W5 (Section 3.1, part A).
  - `scripts/TU_research/tu_research.py` writes `registry/TU_research.csv` and its log: the research map
    (part B). It imports the interval class, the bounds on e, the auction and the tuple check `verify()`
    from `P3_research.py`, which has a main guard (line 1111), so the import writes nothing.
  - `scripts/XTU_conditions/recompute.py` and `scripts/XTU_research/recompute.py`: independent
    recomputations that import no checked module, with a comparison CSV (key, registry display,
    independent enclosure, agreement) and a coverage list of new keys without a comparison row.
  - `make_numbers.py` globs every registry CSV, so the new files merge without code change. A key that
    already exists is reused, not duplicated (Section 3.2).
- **The certificate the research figure needs.** the independent referee's report gives the end of research without
  recruitment, r_X = 2.166995158219, as a floating-point root, and the outcome list for the whole path. Before
  the figure or the text says "the two equilibria coexist exactly from r_N to r_X, and the recruiting
  equilibrium is alone from r_X to r_C", the exercise proves the sign pattern of
  g(r) = M at q(Δ(r)) minus τ(r) on [r_N, r_C]: negative on (r_N, r_X), positive on (r_X, r_C]. Both terms rise
  with r, so a crossing count is not automatic. Method: partition [r_N, r_C] finely; on each piece, bound
  g with monotone endpoint values (Q rises with Δ, Δ with r, M with research, τ with r); near r_X, enclose g′
  and show it positive, which gives one root; bisect r_X with exact interval signs. The same exercise checks
  the full equilibrium tuples of the three outcomes at sample strengths (1.70, 1.80, 1.90, 2.00, 2.12,
  2.13, 2.30, 3.00, 3.59, 3.60) under the default tie rules, under an abstaining investor (the gap on
  (r_N, r_S]) and under a challenger who may prepare with any probability where the text states a fact.
  Above r_C research without recruitment sits at the cap because the existing strong-incumbent margin
  ρΔ(r_1)m − k − aλ̄ (`margin_res_bound_r1_B`, 0.016421) is positive and Δ rises; no new number is needed
  for that fact.
- **Sources.** W1 the independent referee eqs. (4) to (12) and "Consolidated benchmark numerical check"; W2 the independent referee
  "Benchmark verification" and "Numerical audit"; W3 the independent referee §§2 to 6, "Solver B/Solver D Candidate 3", "The
  benchmark" and "Primitive margins"; W4 the independent referee on the uniform condition; W5 the independent referee "Benchmark margins" and
  line 586; WORKAROUNDS "Conditions, one per result" and "What changes in the benchmark story".
- **Writer and checker.** Certificate design for g: the independent referee (who found r_X). Exercise code: Solver B,
  reusing the P3 interval code. Independent checkers: the mathematics writer, with a different method (for example
  closed-form quadratic roots with integer square-root bounds for Q, a different e enclosure, and its own
  auction cash-flow integration). Definitions of the new rows against the final statements of S4: one
  the independent referee pass.
- **Verification.**

  ```bash
  cd $WT
  python3 audit/slot_manuscript_2026_10_23/scripts/TU_conditions/tu_conditions.py > $TEAM/scripts/TU_conditions/tu_conditions.log
  python3 audit/slot_manuscript_2026_10_23/scripts/TU_research/tu_research.py > $TEAM/scripts/TU_research/tu_research.log
  python3 audit/slot_manuscript_2026_10_23/scripts/XTU_conditions/recompute.py > $TEAM/scripts/XTU_conditions/run_log.txt
  python3 audit/slot_manuscript_2026_10_23/scripts/XTU_research/recompute.py > $TEAM/scripts/XTU_research/run_log.txt
  python3 $TEAM/scripts/_coordinator/make_numbers.py --out $MASTER    # 0 conflicts
  python3 $TEAM/scripts/_coordinator/number_scan.py --doc $MASTER
  git -C $WT diff --stat -- audit/slot_manuscript_2026_10_23/registry/P1_core.csv \
    audit/slot_manuscript_2026_10_23/registry/P3_research.csv audit/slot_manuscript_2026_10_23/registry/P5_observables.csv   # empty
  ```

- **Acceptance.** Each new row: value exact or to at least 10 significant digits; display as printed;
  internal status (the registry column only); source script; run log; a note with the definition and
  the outward enclosure, with no model or tool name. Every new key has an agreeing checker row (coverage
  list empty). Existing CSVs unchanged. The sign certificate prints, piece by piece, a bound that excludes
  zero, and one piece with a positive derivative enclosure around r_X. The run logs print Python and mpmath
  versions and the SHA-256 of each output. Commits in `$WT`, one per exercise and one per checker.
- **Size.** About 600 lines of exercise code, 550 of checker code, 15 to 35 rows (by decision D12).

### S6. Figures

- **Goal.** The research figure shows the full map of equilibria on a continuous axis; the coexistence
  figure's threshold label matches its note; and, if Austin agrees (D2), a region figure shows the
  general coexistence theorem with the benchmark path.
- **Research figure (`fig_research`, `make_figures.py:526-670`).** Content under the default tie rules,
  at prior 1/2:
  - zero research on [r_0, r_N], entry ρ, closed at r_N;
  - the recruiting equilibrium: research from λ_E(r_R) at r_R (`res_lambda_rR`) to the cap at the cap
    strength (`res_rcap`), then at the cap up to r_C, closed at r_C; entry from `res_entry_rR` to
    `res_entry_cap`, constant to r_C;
  - research without recruitment on (r_N, r_X): research q(r) rising from 0 at r_N to `res_floor_rX` at
    r_X, open at both ends; entry ρ;
  - above r_C: research at the cap, entry ρ, open at r_C;
  - marks at r_R, the cap strength, r_N, r_X and r_C; r_U leaves the figure (its bound is sufficient, and
    uniqueness starts at r_X); r_S appears in the note in words;
  - no gray band, no broken axis, no "equilibrium set not characterized";
  - recommended layout, matching the coexistence figure: four panels, research on the whole path (a) and
    enlarged around [1.45, 2.25] (b), entry on the whole path (c) and enlarged (d); black dots at r_0,
    the three strengths of Table 4, r_1 and r_2.
  - Slide version (`talk=True`, today `xr = (1.2, 2.0)` with no right panel): two panels on the whole path
    [1.2, 3.6], research and entry, few labels. Frame F13's text changes with it (S9).
- **Coexistence figure (`fig_coexistence`, lines 443-522).** In-figure label "T: threshold branch (rule
  CM)" (line 498) becomes "T: threshold branch"; the slide legend "T threshold (CM)" (line 517) becomes
  "T threshold". Curves unchanged.
- **Region figure (new `fig_region`, if D2 is yes).** One panel in the plane of the spread Δ (horizontal,
  about [0, 0.2]) and the threshold τ (vertical, about [0.45, 0.76]), at prior 1/2 and the benchmark slot:
  the shaded set 1/2 < τ ≤ M, k/(1 − τ) ≤ Δ ≤ 2k/ρ; a dashed line at Δ = k/(1 − M) between mixed and full
  purchases; the benchmark path (Δ(r), τ(r)) from r_0, with markers at r_0, r_A, r_F and r_N and an arrow
  where it leaves the window toward r_1 and r_2. No numbers in the figure beyond axis ticks. Slide version
  for a backup frame. Placement: Section 4.3 after Proposition 3; label `fig:region`. Figures then number
  beliefs 1, region 2, coexistence 3, research 4; no consumer cites a figure by number.
- **Run log.** The comparison table of `main()` (lines 686-726) gains rows for r_X, floor research at
  r_X, and the region path's crossings (r_A, r_F, r_N) against the registry displays.
- **Facts sheet.** The figure stage writes `audit/theory_upgrade_2026_10_25/plan/FIGURE_FACTS.md`: each
  plotted object, its formula, its keys, open and closed ends, and the tie rules, for the caption writers.
- **Writer and checker.** the production assistant writes the figure code; the prose writer and integrator reviews the PNG previews and the run log;
  Austin approves the look.
- **Verification.**

  ```bash
  cd $WT
  python3 audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py --out $MASTER/figures
  grep -c DIFFERENT $TEAM/scripts/F_figures/run_log.txt     # 0
  for f in $MASTER/figures/*.pdf; do pdffonts $f | tail -n +3; done   # TrueType, embedded, no Type 3
  python3 $TEAM/scripts/_coordinator/language_scan.py --doc $MASTER --pdf $MASTER/figures/*.pdf
  ```

  PNG previews in `F_figures/png/` (untracked) viewed by the reviewer; the beliefs figure, regenerated with
  a different matplotlib version, compared visually with the committed one.
- **Acceptance.** Vector PDFs; embedded TrueType fonts (STIX for the paper, Fira Sans for slides); no
  in-figure titles; panel labels (a) to (d); open markers at open ends; every plotted boundary equal to its
  registry display at six places; no banned word in any figure text; L1 to L3 hold for captions and notes.
- **Size.** About 300 changed lines in `make_figures.py`; eight PDFs (ten with the region figure).

### S7. Main text (main-text lens)

Needed from my lens: the keys of Section 3.1 and the facts sheet. My recommendation for the main text's
numbers: margins print in A9 only, and the main text states the positive fact each supports
(STYLE_GUIDE §2.7, fifth bullet); the main text adds no new number beyond the research-figure facts (the
strength r_X if named) and any rows Austin adds to Tables 3 and 4 (D12). The main-text lens owns the
captions and notes; Section 3.5 gives compliant drafts.

### S8. Numbers in the appendix: margins table, benchmark paragraphs, proof-method sentences

- **Goal.** A9 records the margin of every named condition at the benchmark; the benchmark paragraphs of
  A4, A5 and A8 print the new numbers through `\reg{}`; no appendix line names a file, program, log, key or
  "calibration B".
- **A9 (`appendix/A9_parameters.tex`).** Lines 3-6 and 61-79: drop the script list, the "registry keys"
  note (40-42) and the sentence on independent recomputations; the lead-in states the method as
  mathematics (draft in Section 3.5). Margins table (86-220): drop the "Source" column; header "Value at
  B" becomes "Benchmark value"; panel heads lose "calibration B"; rows added per Section 3.1 for the four
  conditions, the preparation-cost bracket, the research map and the empirical conditions; rows removed
  where S4 retires a hypothesis (for example `Q_J(r_0) > 0`, line 123, once part (b) of the path lemma has a
  direct proof; `τ(r_2) < 3/4`, line 121, if the step that used it goes). Declarations table: "Declarations
  at calibration B" becomes "Declarations at the benchmark"; the "Kind" column reads input or derived,
  the registry's vocabulary; the sweep judges it (my suggestion: "declared" or "derived").
- **Proof-method sentences.** Every line in Section 3.6's list. Each becomes a statement of method, or goes
  when it only records what was checked (for example A5:435-439, the grid scan that "enters no proof").
- **Writer and checker.** A9 rows: the production assistant writes, Solver B checks each against its registry note and sign;
  the independent referee checks each hypothesis row against the final statement. Method sentences: the prose writer and integrator writes; Solver E
  runs the language scan and the humanizing pass; the independent referee reads the method sentences of A4 and A5 once, to
  confirm each still states a valid proof step.
- **Verification.** make_numbers with `--out $MASTER`; number_scan `--doc $MASTER` (lists a to c read);
  standard build; every changed appendix page read in the PDF; language scan on A1 to A9 with zero hits in
  the process-word and file-name categories.
- **Acceptance.** Every named condition and every new benchmark fact in the text has its A9 row; no
  `\nolinkurl`, file name or key in the appendix; L1 to L3.
- **Size.** A9 about 80 changed lines (25 rows added, 15 lines removed); about 90 lines across A2 to A8.

### S9. Consumers: slides, comparison note, key lists

- **Goal.** `slides.tex` and `comparison.tex` state the upgraded results with the final numbering, and the
  key lists are current.
- **Slides.** F12 (456-468): the coexistence region in words, the benchmark interval as its instance,
  "class H" for "the high class" (465). F13 (476-486): research at the cap up to r_C; the old branch
  sentence (484) and "Proposition 4(a)" go; the takeaway follows the figure. F16 (545-550): the weighted
  test in words; the winner sign; "with a hidden price, entry does not rise" becomes "with the price
  hidden, entry stays at the floor". A2 notation (602-640): J, W_H, the four conditions if a frame
  uses them. A8 (747-763) and A9 (773-776): the research map; "Proposition 4(a)" re-pointed. "High class"
  at 753 and 829. A backup frame with `region_talk.pdf` if D2 is yes. `memos/W2_keys.md` gains the new
  keys.
- **Comparison note.** Per D9. Under the recast, `tab:results` rows 199-215 lose their status labels;
  rows 205 to 207 and 215 and the prose at 219-305 and 351-358 state the slot's upgraded results; §4.5
  "Certificates for finite steps" (448-467), the checklist (602-620) and §5 (622-704) become one short
  section on how each set-up's proofs work, in mathematical terms; decision points 705-737 follow.
  Hard-coded slot numbers are updated from the label map, and Laplace citations (inside `\lap{}` and the
  Laplace column) are left alone: the note mixes two numbering systems, so a global replace corrupts it.
- **Records.** `LABELS.md` gains a dated section with the added labels; `LEDGER.md` gains dated log lines.
  Neither names a worker or assignment.
- **Writer and checker.** Slides: the production assistant writes, Solver B checks the build and a contact sheet of all frames.
  Comparison recast: the prose writer and integrator writes, Solver E checks keys, numbers, label map and language.
- **Verification.** Standard build; `pdftoppm -r 50 build/slides.pdf` contact sheet viewed; label map
  `--before` diff applied to every hard-coded citation; language scan on both files.
- **Acceptance.** No reference in either file to a superseded number or claim; zero status labels; L1 to
  L3; slide count within the 20 main frames plus backups.
- **Size.** Slides about 60 lines. Comparison: recast 250 to 350 lines; freeze about 10.

### S10. Final sweep and the one second-opinion read

- **Goal.** One consistent finished paper.
- **Steps.** (1) `slot_rerun.sh` or the S0.4 list, plus the new exercises and checkers: registry CSVs
  unchanged since S8. (2) make_numbers `--out $MASTER`; number_scan `--doc $MASTER`: 0 missing, 0 typed
  decimals, lists (a) to (c) read, every orphan intended. (3) Standard builds: no unknown key, no undefined
  reference, no overfull box, no Type 3 font, no `??`, no "in preparation". (4) Language scan on the master
  and on the three PDFs; every hit judged; the humanizing and anti-defensive pass on all new prose.
  (5) Label map `--before` baseline: every changed number propagated to the slides and the comparison note.
  (6) Read every changed page of the three PDFs. (7) One second-opinion read of `main.pdf` (then the slides,
  then the comparison note if recast): language rules, consistency of statements, numbers and figures;
  findings go to the owning writer, and the read does not repeat.
- **Writer and checker.** Coordinator runs the gate; the production assistant runs the humanizing pass; the second reader reads once.
- **Acceptance.** All of S0 to S9's acceptance lines hold at once on the final state; the scan's
  judged-hit list is saved beside this plan.

### S11. Mirror sync, commits, delivery note; push on approval

- **Goal.** The master, the mirror and the records agree, on local branches, ready for Austin.
- **Commands.**

  ```bash
  git -C $MASTER fetch origin
  git -C $MASTER log --oneline $BR..origin/main        # Austin's Overleaf edits made during the update
  git -C $MASTER rebase origin/main                     # only if that list is nonempty; then S10 again
  diff -rq --exclude=.git --exclude=build $MASTER $WT/slot/manuscript   # read in full before copying
  rsync -a --exclude .git --exclude build $MASTER/ $WT/slot/manuscript/   # no --delete
  diff -rq --exclude=.git --exclude=build $MASTER $WT/slot/manuscript   # expect no output
  git -C $WT add slot/manuscript
  git -C $WT commit -m "Sync slot/manuscript with the Overleaf master"
  ```

  A plain copy is the primary route. A subtree pull would conflict: the parent never merged the commits
  it pushed to Overleaf, so its merge base with the Overleaf history is 001a620, the first Overleaf
  commit, and every line edited since then and edited again in the upgrade conflicts. A squash pull finds
  the same join (a992481) and the same base. The route that keeps the Overleaf commits in the parent
  history, untested here: in the clean worktree, check that `git -C $WT subtree split --prefix=slot/manuscript`
  prints 428805093e9f (the last commit pushed from the parent); if it does, `git -C $WT subtree split
  --prefix=slot/manuscript --rejoin` records that join, and `git -C $WT subtree pull --prefix=slot/manuscript
  $MASTER $BR` then merges against it. `git subtree` refuses a tree with modifications, so neither runs in
  Austin's checkout. The README's documented `git subtree pull` from Overleaf has the same base problem.
- **Delivery note for Austin.** Branch names and head commits in both repositories; the list of commits;
  page counts; scan results; the decisions taken; the consumers left stale (D7); the push commands, to run
  on approval: `git -C $MASTER switch main && git -C $MASTER merge --ff-only $BR && git -C $MASTER push
  origin main`; and for GitHub, `git -C $WT push origin $BR`.
- **Acceptance.** The parity diff read before the copy (a file that exists only in the mirror is deleted
  by hand after reading, never by `--delete`) and empty after it; every commit staged by explicit path
  (never `git add -A`); no file of Austin's in any commit; nothing pushed.

---

## 3. File-by-file change list (numbers, figures, delivery)

### 3.1 Registry rows to add

"If printed" rows exist only when S4 or S7 prints the number (decision D12). Values come from the referee
reports or follow from existing registry values; the exercise recomputes each, and exact values are given
where they are rational.

**A. `TU_conditions.csv` (exact rationals unless noted)**

| Key | Value | Definition | Source | Printed where |
|---|---|---|---|---|
| `margin_unif_afford_B` | 2/5 | h − r_2 − c_H: class H's value exceeds the strongest incumbent's top value by at least the preparation cost (point masses) | W1 the independent referee eq. (4), (8); memo condition 2 | A9 |
| `cH_unif_cap_B` | 32/5 | h − r_2, the cost ceiling of the coexistence-interval condition | memo "two conditions bracket" | A9; main text in words |
| `cH_unif_weak_B`, `margin_unif_weak_B` | 4943/720 (6.865278); 623/720 | the weaker point-mass bound h − r_2 + ℓ/2 − p²/(2r_2), and its distance to c_H | W1 the independent referee eq. (9) | A9, if S4 keeps the weaker bound |
| `margin_balance_B`, `margin_balance_B_frac` | 9667/8280 (1.167512) | min over the path of (g_H − c_H) − ηΔ, attained at r_2 | W1 the independent referee eq. (11) | A4 direct proof of path lemma (b); A9 |
| `margin_balance_sq_B`, `margin_balance_sq_B_frac` | 937/5520 (0.169746) | min of (g_H − c_H) − 2ηΔ, at r_2 | W1 the independent referee eq. (12) | A4 path lemma (c) on the whole path; A9 |
| `lip_L_B`, `margin_smallk_B` | 119/44; dρ²/4 − kL = 0.086534 | the small-trading-cost condition | W1 the independent referee eq. (14) | A9, if S4 keeps Solver A 3 |
| `cH_decisive_B` | 399/80 (4.9875) | (h² − p²)/(2h), the cost floor of decisive advantage | W2 the independent referee "Benchmark verification" | A9; main text in words |
| `margin_decisive_B` | 81/80 (1.0125) | c_H − (h² − p²)/(2h) | same | A9 |
| `r_decisive_B`, `margin_decisive_r_B` | 4 + √63/2 (7.968627, interval); h − r_* = 2.031373 | the strength above which no benchmark-family economy recruits | same | A5 or A9 |
| `margin_winsep_r1_B`, `margin_winsep_r2_B` | 1/3; 5/18 | class separation at r minus its average, D(r) − Ω(r), the uniform winner-gap condition | W4 the independent referee; memo W4.3 | A8; A9 |
| `Omega_r0_B` | 1/6 | W_H − W_L at r_0, where the order gap is zero | memo W4 | A8, if printed |
| `margin_reserve_unif_B` | 1/4 | ℓ² − 3p², the uniform reserve condition for a rising entry component | W5 the independent referee "Benchmark margins" | A8; A9 |
| `wtest_r1_B` | 0.257948 (interval) | the frequency-weighted impact difference at r_1, P̄ − P(0) (equal to `res_dR_r1` and to −`pdrop_neutral_r1_B`) | W5 the independent referee line 630 | Section 8 or A8 |
| `share_H_r0`, `share_H_r1_B`, `share_H_r2_B` | 6/11; 0.830691 (interval); 18/23 | class H's share of challenger acquisitions, πe_HW_H / (πe_HW_H + (1 − π)e_LW_L) | brief, Proposition 2 line | Table 3, if Proposition 2 adds the share |
| `cov_win_recruit_share_r1_B` | about 0.89 (interval) | the entry channel's share of `cov_win_r1_B` | memo W4 | A8, if the two-channel form prints its split |

**B. `TU_research.csv` (intervals in e)**

| Key | Value | Definition | Source | Printed where |
|---|---|---|---|---|
| `res_rX` | 2.166995 | end of research without recruitment beside capped recruiting (S5 certificate) | W3 the independent referee "The benchmark" | Section 5, figure, A5, A9 |
| `res_floor_rX` | 0.234257 | research without recruitment at r_X | W3 the independent referee line 528 | A5, if printed |
| `margin_res_floorsign_B` | smallest bound on the partition | the sign certificate's margin away from r_X | S5 | A9 |
| `res_phi_r0` | −0.022693 (exact rational) | recruitment margin φ_a at r_0, the start of the path | W3 the independent referee "Primitive margins" | A9, cheap-research row |
| `res_phi_rcap` | 0.017446 | φ_a at the cap strength | same | A9, cheap-research row |
| `res_eH_r155`, `res_eH_r160`, `res_eH_r165`; `res_eL_r155`, `res_eL_r160`, `res_eL_r165` | about 0.597 at 1.55 (twice `res_own_r155`); about 0.418 at 1.55 | class-H and class-L entry on the research branch, the improving pool | W2 the independent referee numerical audit; WORKAROUNDS W2.2 | Table 4, if Austin adds the two rows |
| `res_eH_rR`, `res_eH_cap`, `res_eL_rR`, `res_eL_cap` | 0.573541, 0.648803; 0.428151, 0.396711 | the same at the start and at the cap | same | Section 5 or A5, if printed |
| `res_I0CM_lambda_r200`, `res_I0CM_e1_r200`, `res_I0CM_entry_r200` | 0.223835; 0.359944; 0.287449 | the threshold equilibrium that survives an abstaining investor at r = 2 | W3 the independent referee lines 431-439 | A5 tie-rule remark, only if numbers print there |

### 3.2 Existing keys that already cover "new" numbers (reuse; no duplicate)

| Number in the memo | Existing key | Display |
|---|---|---|
| minimum of c_H − B_r(1/2) on the path, 1.196 (announcement condition) | `margin_res_half_B` | 1.195833 (287/240; B_r(1/2) falls in r) |
| the full-sale strength 2.124 | `rS_B` | 2.124148 |
| a_mono 0.162 and the cheap-research margin 0.137 | `res_amono`, `margin_res_amono_B` | 0.161713; 0.136713 |
| the cap-before-selling condition (0.0016 in spread units) | `margin_res_rN_B` (r_N − cap strength, the same condition in strength units) | 0.070245 |
| start, cap and ceiling of the recruiting equilibrium | `res_rR`, `res_rcap`, `res_rC` (= `rC_B`), `res_rN` (= `rN`) | 1.501023; 1.677633; 3.592659; 1.747878 |
| entry with research at the cap | `res_entry_cap` | 0.522757 |
| research without recruitment at the cap above r_C | `margin_res_bound_r1_B` (with Δ rising) | 0.016421 |
| the winner gap and covariance at r_1, r_2 | `wgap_r1_B`, `wgap_r2_B`, `cov_win_r1_B`, `cov_win_r2_B` | 0.308078, 0.333751, 0.251863, 0.030344 |

### 3.3 Keys likely to fall out of the text (orphans; keep the rows, confirm each is intended)

`QJ_r0` (A4:48, A9:123) when path-lemma (b) gets a direct proof; `margin_tau_r2_3q_B_frac` (A9:121) if the
3/4 step goes; `res_rUR` if r_U leaves Section 5 and the figure (it may stay in A5); `res_bound_*`,
`res_dphi_lead`, `res_phip_lb` if S4 replaces the bound-based monotonicity proof of φ_a; the slide keys of
F13's old branch sentence. The S2 orphan list prints them all.

### 3.4 Scripts

| File | Change |
|---|---|
| `_coordinator/make_numbers.py` | `--out DIR` (line 14); prints target and hash |
| `_coordinator/number_scan.py` | `--doc DIR` (line 9); one-decimal and fraction list; orphan list; stale `numbers.tex` list |
| `_coordinator/language_scan.py` | new |
| `_coordinator/label_map.py` | new |
| `_coordinator/slot_rerun.sh` | new, optional |
| `F_figures/make_figures.py` | `--out` (line 35); Fira via `kpsewhich` (line 39); `fig_research` redraw (526-670); labels at 498 and 517; new `fig_region`; run-log rows (686-726); `Creator` metadata (330) |
| `TU_conditions/`, `TU_research/`, `XTU_conditions/`, `XTU_research/` | new exercises and checkers with logs (`git add -f` for logs) |
| `P1_core/`, `P3_research/`, `P5_observables/`, `XP*/` | rerun only; no edit |

### 3.5 Figures and their text in the master (compliant drafts for the caption writers)

- `figures/research.pdf`, `research_talk.pdf`: redrawn (S6). Caption: "Research and entry along the benchmark
  path." Note draft: "The benchmark with a = `\reg{res_a}` and λ̄ = `\reg{res_cap}`, when an indifferent
  investor may mix over its best orders and an indifferent high-cost challenger prepares. Panels (a) and
  (c) show research and entry from r_0 to r_2, and panels (b) and (d) enlarge the strengths around the start
  of research. Zero research is an equilibrium from r_0 to r_N. In the recruiting equilibrium, research rises
  from r_R, reaches the cap at [cap strength] and stays at the cap up to the entry ceiling r_C, and entry
  rises to `\reg{res_entry_cap}` and keeps that value up to r_C. From r_N to [r_X] a second equilibrium
  coexists with it: both classes trade after a success, no order recruits, and entry stays at ρ, while its
  research rises with strength. Above r_C research stays at the cap and entry equals ρ. In the recruiting
  equilibrium the low class sells just often enough to break even from r_N to r_S and sells with certainty
  above r_S. Black dots mark r_0, the strengths of Table 4, r_1 and r_2. Filled markers belong to a curve,
  and open markers do not." (The current note is `05_research.tex:138-144`; the text at 119-130 changes
  with it.)
- `figures/coexistence.pdf`, `coexistence_talk.pdf`: label only. Note fix at `04_equilibrium_results.tex:302-303`:
  "The thin dashed line is the threshold branch T: at r_A its purchase brings entry one and is an
  equilibrium under these rules, and above r_A the branch needs a high-cost challenger that may prepare
  with any probability."
- `figures/region.pdf`, `region_talk.pdf` (D2): caption "The coexistence region and the benchmark path."
  Note draft: "The prior 1/2 and the benchmark slot. The shaded set holds the pairs of target-payoff spread
  Δ and preparation threshold τ at which the equilibrium without informed trade and an informative
  equilibrium coexist: the threshold lies above the prior and at most at the top posterior M(1/2), a
  recruiting purchase covers the trading cost (left boundary), and an uninformed order does not pay (right
  boundary, Δ = 2k/ρ). The dashed line Δ = k/(1 − M(1/2)) separates mixed from full purchases. The curve
  traces the benchmark incumbent from r_0: it enters the set at r_A, reaches full purchases at r_F and
  leaves at r_N."
- `figures/beliefs.pdf`, `beliefs_talk.pdf`: regenerated, content unchanged.
- A9 lead-in draft (replaces lines 61-79): "Table~\ref{tab:margins} lists every strict hypothesis of the paper with its
  margin at the benchmark, signed so that a positive number means that the hypothesis holds; a negative
  entry marks a condition that fails by design, and the table says which. Each margin that depends on
  Euler's number is evaluated with rational bounds on it, and its sign holds because the whole enclosure
  lies on one side of zero. The structural bound β ≤ 1/3 is a domain restriction; the table records its
  distance."
- Method-sentence pattern (A4:107-112, A5:423-434): "Each threshold is the unique root of a strictly
  monotone function on the path; bisection with exact rational signs at both ends encloses it, and
  Table~\ref{tab:a4-thresholds} rounds each enclosure outward to six places." "Every rational quantity is computed exactly, and
  every quantity that depends on Euler's number is enclosed by rational intervals from
  Σ_{n≤60} 1/n! < e < Σ_{n≤60} 1/n! + 62/(61·61!); at each strength the tuples of Lemmas~\ref{lem:a5-middle} and~\ref{lem:a5-strong}
  satisfy (E1) to (E7) under each pair of tie rules, and each printed value is an outward rounding of its
  enclosure."

### 3.6 Lines in the master that name files, programs, logs, keys or "calibration B"

From a scan of the master (comment lines excluded; "open set", "open interval" and "open band" are
mathematics and stay, and "superscript" is a false hit): `main.tex` and the sections: none; `A2:26-27`;
`A3:124, 134-147, 155, 226-231`; `A4:45-62, 107-116, 399-414, 529`; `A5:40, 61, 255, 286, 317, 339,
423-439`; `A6:61-64, 237, 248-256, 354, 360, 491-522, 557`; `A7:79, 87, 241`; `A8:142, 251-259`; `A9:4, 10,
40-42, 49-58, 63-79, 94, 96, 169, 192-199, 260`. `comparison.tex`: 103 lines. `slides.tex`: none (two
`\scriptsize` false hits). `main.tex:61-71`: the `\slotfigure` and `\slotappendix` macros print "is in
preparation" when a file is missing (D14).

### 3.7 Other master files

`numbers.tex` regenerated each stage; `sections/02_model.tex:1` (D1); `START_HERE.txt` only if D9 freezes
the comparison note.

### 3.8 Consumers outside scope, left stale until Austin's own work is committed (D7)

`slot/study_guide/` (chapters 08, 09 and C; `verify/*.py` read `slot/manuscript/numbers.tex`), the website
(`handout/sections/03-result.html`, `04-path.html`, `slot_data.py`, `charts.js`; `handout/build.py` builds
the PDFs from `slot/manuscript/`), the web slides (`presentation/content.js`, `figdata.py`), the discussion
notes (`discussion/2026-10-26/`, excluded from Git). Each restates the old research figure or the
benchmark-only statements.

---

## 4. Label and numbering map

### 4.1 Before: the current build (scratch build of 69c25f4)

Main text. Propositions 1 `prop:returns`, 2 `prop:ccc`, 3 `prop:coexistence`, 4 `prop:research`. Tables 1
`tab:payoffs`, 2 `tab:region`, 3 `tab:outcomes`, 4 `tab:research`, 5 `tab:reserves`. Figures 1 `fig:beliefs`, 2
`fig:coexistence`, 3 `fig:research`. Equations (1) to (9), with (9) `eq:research`.

Appendix. Definition A.1 `def:equilibrium`. Lemmas A.1 `lem:beliefs`, A.2 `lem:prices`, A.3 `lem:trading`,
A.4 `lem:a4-path`, A.5 `lem:a4-order`, A.6 `lem:a4-high`, A.7 `lem:a4-low`, A.8 `lem:a4-product`, A.9
`lem:a5-joint`, A.10 `lem:a5-bounds`, A.11 `lem:a5-buy`, A.12 `lem:a5-middle`, A.13 `lem:a5-strong`.
Corollaries A.1 `cor:exclusion`, A.2 `prop:priors`, A.3 `cor:purchasesonly`. Propositions A.1 `prop:region`,
A.2 `prop:researchregion`, A.3 `prop:control`, A.4 `prop:atomless`, A.5 `prop:classes`, A.6
`prop:manyclasses`, A.7 `prop:signals`, A.8 `prop:access`, A.9 `prop:payment`, A.10 `prop:reserves`, A.11
`prop:spread`, A.12 `prop:informedshare`, A.13 `prop:winner`, A.14 `prop:announcement`. Remark A.1
`rem:researchties`. Tables A.1 `tab:a4-thresholds`, A.2 `tab:a4-set`, A.3 `tab:a4-ties`, A.4
`tab:classes`, A.5 `tab:a9-declarations`, A.6 `tab:margins`. Appendix sections A.1 to A.9.

### 4.2 Expected additions and a placement rule that keeps the cited numbers

| Expected addition (theory lens confirms) | Kind | Effect if placed naively | Placement that keeps cited numbers |
|---|---|---|---|
| Reduction lemma (two-number summary) | lemma, A2 | shifts every Lemma A.n after it | after `lem:trading`, so A.1 to A.3 keep their numbers |
| Path lemma for the two numbers (Δ, γ, τ along a path) | lemma, A1 | shifts all lemmas | inside A4's path lemma, or after `lem:trading` |
| General coexistence region, full-purchase interval | part of the full statement of Proposition 3, or a lemma in A4 | a new appendix proposition shifts A.2 to A.14 | named full statement (no counter) or lemma |
| Uniform interval corollary; balance condition | corollary, lemma in A4 | a corollary before `prop:priors` shifts Corollary A.2 and A.3 | after Corollary A.2, or as lemma |
| Research continuation, three-outcome map, ownership factorization, fixed-value statement | lemmas in A5; full statement of Proposition 4 | lemma shifts only | lemmas after `lem:a5-strong` or as parts |
| Same-incumbent ratio; unweighted-test remark | remarks | Remark A.1 shifts if placed before it | after `rem:researchties` |
| Ownership level under outbidding | corollary | shifts Corollary A.3 if before it | after Corollary A.3 |
| Weighted test, identification, winner sign, announcement condition | restated A.11 to A.14 | none if restated in place | keep `prop:spread` to `prop:announcement` and their order |
| Three-outcome research table (if any) | table in A5 | shifts Tables A.4 to A.6; the comparison note cites A.3, A.4 and A.6 | in the figure note and text, no table |
| `fig:region` | figure, Section 4.3 | figures 2 and 3 become 3 and 4 | no consumer cites figures by number |

Labels stay as they are even where a title changes (`prop:coexistence`, `prop:research` keep their
labels), so `\ref` inside the manuscript needs no edit.

### 4.3 Consumers that cite by printed number

`comparison.tex` (slot citations only): Lemmas A.1 to A.3 (138, 141, 144, 200, 201, 658); Corollary A.2 (206);
Definition A.1 (380, 654); Propositions 1 to 4 (67, 86, 117, 151, 167, 169, 199-207, 232-292, 381, 384, 470,
480, 572, 624, 637, 656, 667, 724); Propositions A.1 to A.14 (67, 104-107, 200-215, 278, 287, 323, 338,
353-358, 386, 406, 464, 633); Tables 2, 3, 4, 5, A.3, A.4, A.6 (117, 151, 203, 204, 209, 214, 323, 333, 338,
445, 632, 659, 660); Appendix A.1 to A.13 and Sections 2.3 to 8 (66, 78, 98, 112, 128, 129, 169, 203-215,
233, 254, 294, 302, 318, 345, 351, 381, 404, 460, 472, 473, 521, 599, 651, 655). Several of these are Laplace
citations; read each in context. `slides.tex`: Lemma A.3 (328); Propositions 1 to 4 (239, 370-375, 456, 476,
484, 652, 691, 702, 773, 776, 794); Propositions A.3 (429), A.8 (517), A.11 to A.14 (545). Out of scope:
`presentation/content.js` (196, 265, 314), the study guide, the website.

### 4.4 Procedure

Freeze S7 and S8; build; `label_map.py build/main.aux --before baseline_labels.txt`; update each consumer
citation from that diff; rebuild the consumers; repeat once after the final Overleaf pull of S11.

---

## 5. Risks and traps

**Numbers**

1. A stale `numbers.tex` in the master passes `number_scan.py` (it checks keys against `registry.csv`) and
   prints `??key` in bold. Mitigation: S2 list (c), and the PDF check for `??`.
2. Typed numbers with one decimal place or fractions such as `9667/8280` pass the current scan.
   Mitigation: S2 list (a).
3. Duplicate keys with equal displays merge silently in `make_numbers.py`, first file wins, so a second
   definition hides. Mitigation: reuse the keys of 3.2; the coverage list names every new key once.
4. Rerunning `P2_auction/derive.py` reverts a hand-fixed display. Mitigation: do not rerun it; if it must
   run, restore `0`.
5. The memo's new numbers are floating-point evaluations from the referee, not interval results.
   Mitigation: S5 recomputes every one; nothing prints from the memo directly.
6. r_X has no certificate yet, and both terms of its defining difference rise with strength. Mitigation:
   the S5 sign certificate; until it passes, neither the figure nor the text states the coexistence
   stretch.
7. New logs are ignored (`*.log` in `.gitignore`). Mitigation: `git add -f` by path.
8. Committed checker logs can predate the last round (XP3). Mitigation: S0 baseline commit first.

**Figures**

9. The Fira path points at the old machine; slide figures fall back to DejaVu Sans without a message.
   Mitigation: S2 item 3 and a `pdffonts` check.
10. matplotlib 3.10.8 here against 3.11.1 for the committed figures: every PDF changes bytes. Mitigation:
    regenerate all figures in one run, compare the unchanged beliefs figure visually.
11. `\slotfigure` prints "Figure file ... is in preparation" and the build succeeds when a figure file is
    missing or misnamed (for example `region.pdf`). Mitigation: D14, and the PDF check for the phrase.
12. The figure carries a tie-rule code in its own text ("(rule CM)"). Mitigation: S6 label change; the
    language scan reads figure PDFs.

**Language**

13. About ninety appendix lines and 103 lines of the comparison note break L1 or L3 before any theory
    changes. Mitigation: S8 and S9 as stages of their own, and the S10 sweep.
14. the mathematics writer-written proofs tend to carry bookkeeping sentences ("one checks that", "a computation verifies").
    Mitigation: the per-stage scan and humanizing pass apply to the mathematics writer prose too.
15. "may" is a hedge in prose but the tie phrase "an indifferent investor may mix" is model content.
    Mitigation: the scan flags both; the judge keeps the tie phrases.

**Version control and environment**

16. `git subtree` refuses a working tree with modifications (Xcode's `git-subtree`, `ensure_clean` in
    `cmd_pull` and `cmd_merge`), so it cannot run in Austin's checkout, and a stash would touch his work.
    Its merge base with the Overleaf history is 001a620, so a pull conflicts on every line edited twice.
    Mitigation: the separate worktree; the plain copy of S11, or `split --rejoin` after the split-head
    check.
17. `$MASTER` has no ignore rule for `build/`; `git add -A` there would push build files to the Overleaf
    project. Mitigation: `build/` in `.git/info/exclude`; stage by path; one committer per repository.
18. Both Overleaf remotes carry a token in their URL. Mitigation: never print `git remote -v` or `.git/config`
    into a log, memo or chat.
19. Austin may edit on Overleaf during the update. Mitigation: S11 fetch and rebase, then S10 again.
20. `python3 -I` breaks `p1_numbers.py`; `.venv` is absent and the documented commands use it. Mitigation:
    `python3` by path, without `-I`; versions printed in every log.
21. The the numerical verification procedure skill gates the earlier manuscript's numerics layer (`numerics/verify.py`), not the slot
    registry. Its default run rewrites `numerics/quantity_registry.csv`, and `--stage handout` rebuilds
    `docs/index.html`, which holds Austin's uncommitted work. Mitigation: do not use it as the gate here;
    use S10. Run plain `numerics/verify.py` only if a file under `numerics/` or `paper/` changes (none
    planned), and never with `--rerun`, `--final` or `--stage handout` in the main checkout.
22. `slot/README.md` has Austin's uncommitted edit. Mitigation: no README change in this update, or one
    sentence in the Numbers section on the branch, for Austin to merge after committing his own.

**Concurrency and consumers**

23. Several writers edit the same master files. Mitigation: one writer per file at a time (theory lens:
    A1 to A8; main-text lens: sections and captions; delivery: A9, figures, `numbers.tex`, slides, comparison);
    the coordinator commits.
24. The comparison note mixes Laplace and slot numbering. Mitigation: update slot citations by reading
    context, never by global replace.
25. Once the mirror is synced and merged, the website would publish the new PDFs beside prose that
    describes the old research figure. Mitigation: D7; Austin publishes both together.

---

## 6. Decision points for Austin

| # | Decision | Recommendation |
|---|---|---|
| D1 | The stray `ty` at `sections/02_model.tex:1` | Remove it. It prints "ty" at the end of the introduction's roadmap paragraph, before Section 2. One commit. |
| D2 | The region panel | Yes, as its own figure after Proposition 3: the fixed region in the spread-threshold plane with the benchmark path entering at r_A and leaving at r_N; slide version as a backup frame. No second path (the two-piece example stays in the appendix, in words or formulas). No new number. |
| D3 | Filling the research figure | Yes: continuous axis, three outcomes, r_X marked, r_U dropped; after the S5 certificate. |
| D4 | Corollary A.2 at other priors | Keep it at the benchmark, as now: its ten keys exist, and generalizing it needs new crossing and attainment margins and checker rows for no new economics. |
| D5 | Identification in Section 8 | Prose in Section 8, statement in the appendix; it needs no benchmark number (the benchmark prior is 1/2, where counts do not identify). Print the noise factor as the formula 1/(2π − 1)², not as 100. |
| D6 | A.7 extended, A.9 skipped, A.5 on the uniform family | Agree. None needs a new number; A.7's example keeps its keys; the ownership line after A.7 (A6:489) carries W_H(F_1) in words. |
| D7 | Consumers limited to `comparison.tex` and `slides.tex` | Yes. Record the study guide, website, web slides and discussion notes as stale (3.8), and update them after Austin commits his own work in those folders. |
| D8 | Scripts write to the master or the mirror | The master. `make_numbers.py` and `make_figures.py` take an explicit output folder (default the mirror, unchanged) and this update passes the master; the mirror follows from the master once, in S11. One direction of flow: registry to master to mirror. |
| D9 | Status labels in `comparison.tex` | They go, like everything L3 bans there. Then choose: (a) recast, 250 to 350 lines: results rows and slot prose updated, a short mathematical section on how each set-up's proofs work in place of §4.5, the checklist and §5; about a day of writing and checking. (b) Freeze it as a dated record outside the Overleaf project; about ten lines, but `handout/build.py` builds `comparison.pdf` from the mirror, so freezing needs a website change in Austin's own folder. Recommendation: (a) if the note will circulate with the upgraded paper; otherwise (b), with the website change scheduled with D7. |
| D10 | Archive the referee computations | Yes, first action of S0 (`/tmp` is cleared on restart). |
| D11 | The untracked folder `audit/theory_upgrade_2026_10_25/` | It names execution identities (RUN_LOG, provenance lines, scratch folder names). Keep it out of Git (`/audit/theory_upgrade_2026_10_25/` in `.git/info/exclude`), or commit a copy with those names removed (Section 8 of this plan included). |
| D12 | Numbers from economies other than the benchmark (two-piece endpoints, the ownership fall from 11 to 12, the kink example, the bias percentages) and optional benchmark rows (class shares in Tables 3 and 4) | Main text: words and formulas only. Appendix: print such a number only with its own row, exercise and checker. Add the two class-entry rows to Table 4 (they show the improving pool); add the takeover share to Table 3 only if Proposition 2 states it. |
| D13 | Proof provenance once the appendix names no file | The registry's source and log columns carry it, and a replication note outside the manuscript maps tables and statements to programs if Austin wants one. |
| D14 | `\slotfigure` and `\slotappendix` placeholders | Replace them with `\includegraphics` and `\input`, so a missing file stops the build instead of printing "is in preparation". |
| D15 | Keep 1 + u = e | Keep. A rational u would recompute every e-dependent row (about 3,400), the slot band and every figure, with no gain for this update. |
| D16 | Commit messages that reach the Overleaf history | Plain descriptions of the paper change, as now; no workstream or weakness codes. |

---

## 7. What the other two lenses might miss

1. The development-log rule bites before any theory changes: about ninety appendix lines name programs,
   logs, keys or "calibration B", and A9 has a source column of file codes. Theory writers should state
   each computational step as mathematics while they rewrite A4, A5 and A8.
2. The filled research figure asserts a fact nobody has proved yet: the second research equilibrium ends at
   r_X and nowhere else between r_N and r_C. Both sides of its defining comparison rise with strength.
3. The referee computations exist only in `/tmp`.
4. the numerical verification procedure does not cover the slot registry, and its handout stage rebuilds a file with Austin's
   uncommitted work.
5. Silent failures: a missing figure prints "in preparation"; an unknown key prints `??key`; a stale
   `numbers.tex` passes the number scan.
6. Several numbers the memo lists as new already have keys (1.196, 2.124, a_mono and its margin, the
   cap-before-selling condition in strength units).
7. Placement decides consumer churn: a new appendix proposition before A.11 renumbers every empirical
   citation in the slides and the comparison note; lemmas after `lem:trading` and corollaries after A.3
   shift nothing cited.
8. The coexistence figure's own label "(rule CM)" is a tie code inside the figure, and the figure note's
   claim about T is wrong at r_A.
9. The `\bar r_R` rename and the subscript of r_X reach the figure code and A9; the figure waits for them.
10. `git subtree` needs a clean tree, and Austin's checkout is not clean; the mirror's only join with the
    Overleaf history is the first Overleaf commit, so the README's subtree pull would conflict; and his
    `slot/README.md` edit sits in the file that documents the pipeline.
11. The comparison note mixes two numbering systems.
12. The website builds its PDFs from the mirror, so syncing the mirror is a publishing decision.

---

## 8. Staffing

The merged PLAN.md governs stage numbering and dependencies. The mathematics writer develops proofs and research computations; the independent referee checks work it did not write. The prose writer and integrator prepares statements, integrates proofs and checks language. The production assistant handles numbers, figures, labels and companion documents. The second reader reads the finished paper once. The coordinator maintains the stage reports and gates. Austin supplies decisions and final delivery approval.
