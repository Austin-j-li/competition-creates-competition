# Ledger: the order-slot manuscript (started 23 October 2026)

Coordinator notes. Each workstream names its output and its checker. Each checker works
independently of the author.

## Phase 1: proof packages (parallel)

| Stem | Scope (BRIEF §4) | Output | Checker |
|---|---|---|---|
| MT | short probe task | `memos/MT_probe.md` | coordinator |
| P1 | R2, R3, R4 at calibration B; core registry; margins table | `proofs/P1_core.tex`, `memos/P1_core.md`, `registry/P1_core.csv` | XP1 |
| P2 | R6, R9 at calibration B | `proofs/P2_auction.tex`, `memos/P2_auction.md`, `registry/P2_auction.csv` | XP2 |
| P3 | R10 at calibration B, general `β` | `proofs/P3_research.tex`, `memos/P3_research.md`, `registry/P3_research.csv` | XP3 |
| P4 | R5, R7, R8 at calibration B | `proofs/P4_information.tex`, `memos/P4_information.md`, `registry/P4_information.csv` | XP4 |
| P5 | R11 (observables) at calibration B | `proofs/P5_observables.tex`, `memos/P5_observables.md`, `registry/P5_observables.csv` | XP5 |
| LA | audit of the Laplace manuscript against the proof standard | `memos/LA_laplace_audit.md` | XLA |
| W1 | manuscript skeleton, Sections 1–3.1, Appendix A.1 (R1) | `overleaf/competition_slot/` | referee (Phase 4) |

## Phase 2: checks

XP1–XP5 and XLA: independent re-derivation of every headline, a recomputation of every registry row, and a
reading of every proof against BRIEF §5.

## Phase 3: documents

- W1 continues: Sections 3.2–9 and Appendix A.2–A.8 from the checked proof packages.
- F: figures from the merged registry.
- W2: slides.
- W3: the comparison note (after the manuscript compiles and LA and XLA are in).

## Phase 4: review

- Referee read of the manuscript.
- Number check: every number in the three documents against `registry/registry.csv`.
- Builds with latexmk; page images for a visual check.

## Log

- 23 Oct: folder, brief, team rules and ledger written. Local project `overleaf/competition_slot/` created
  (style file, latexmkrc and bibliography copied from the paper project). A quick floating-point check at
  calibration B with research cost 1/40 and cap equal to the benchmark presence probability gives a research
  branch with entry about 0.508 < 0.514 < 0.520 at 1.55, 1.60, 1.65 (numerical diagnostic; P3 re-derives).
- 23 Oct: Phase 1 started: P1–P5, LA and W1 (manuscript skeleton, Sections 1–3.1, Appendix A.1). The probe
  task MT returned a correct result quickly, so W2 (slides first draft) started at the same time.
- 23 Oct: `scripts/_coordinator/make_numbers.py` merges `registry/<STEM>.csv` into `registry/registry.csv`
  and writes `overleaf/competition_slot/numbers.tex` (the `\reg{<key>}` macro).
- 23 Oct: W1 round 1 returned. Build of 23 pages; Sections 1, 2, 3.1 and Appendix A.1 in full, stubs elsewhere.
  W1 found that the brief's `r_F = 1.460985` is the calibration A value; at B, `r_F = 1.467127` (agrees with
  `rF_B` in `registry/P1_core.csv`). BRIEF §3 corrected. Open from W1: keys `prim_pi`, `prim_ell`,
  `Bprior_r0`, `Bprior_r1_B` have no registry row; key names for the spread differ between P1 and W2.
- 23 Oct: LA returned. Proposition 2 (i)–(iii) of the Laplace manuscript: direct verification, uniqueness
  through bounds on every profile, no circular step; (iii) gives no explicit tuple and prints no margin
  (return margin 0.002689 in cost, 0.000334 in posterior, r_2 − r_C = 0.00734). Proposition 3: interval
  certificates for existence at three nodes, no uniqueness, no open set stated. Eleven compressed steps,
  none hides a gap. XLA (check) started.
- 23 Oct: W2 returned: 20 main frames plus title, 12 backups; compiles with XeLaTeX; three figure
  placeholders; 75 registry keys listed in `memos/W2_keys.md`. Contact sheet inspected: layout clean;
  numbers wait for the registry.
- 23 Oct: P5 returned: every N1 claim survives in structure; values change at B. Spread at r_1 0.786299 with
  entry share 90.2% (N1: 90.4% at A); full orders unique on (2.124148, 10); informed share identified from
  sell impact and volume. Open: the branch on (r_N, r_S); selection on [r_F, r_N]. XP5 (check) started.
- 23 Oct: P3 returned. At B with a = 1/40 and cap λ_B: zero research unique at 6/5; branch on
  [1.501023, 1.677633) with research 0.237901, 0.279037, 0.316683 and entry 0.507630 < 0.513965 < 0.519763 at
  1.55, 1.60, 1.65, beside zero research; cap unique at 3 and 18/5 (entry 0.522757, 0.25). Admissible: cap in
  (0.290539, 0.336721), a in (0.021469, 0.036763). Open: equilibrium set on (1.747878, 2.434046) under rule IM.
  Notation: P3 uses f_j(q) for order masses (P1's a_j(x) clashes with the cost a). XP3 (check) started.
- 23 Oct: P4 returned. R5: frozen entry 0.522757 from 1.2 to 3 (does not rise); price-hidden entry 0.25.
  R7: strong entry 0.522757, ownership 0.324401; a cost band of half-width 0.1 breaks the return at 3.6
  (entry 0.382711), half-width 0.001 keeps it (the return margin is 0.002689 in cost). R8: the signal example
  needs its own vector S(B) (ρ = 0.85, c_H = 7.14, k = 0.015, r_0 = 1.1, r_1 = 2.3): entry 0.85 → 0.879797;
  at unchanged B the pair (0.95, 0.505) gives entry 0.25 → 0.386946. XP4 (check) started.
- 23 Oct: P2 returned. Value classes and priors hold under strict conditions; every source example keeps its
  own costs and strengths; many classes hold under separation, with a strict three-class counterexample to
  unrestricted recovery. Price access at B: proceeds +0.257948, surplus +0.081960, break-even scale 6.848394.
  Payment rule: sign of 1 − 2η. Reserves: flat at the exclusion reserve; 31/20 restores strict deterrence and
  excludes the weak incumbent. Open: mixed class profiles, the full payment game, global reserve choice.
  XP2 (check) started.
- 23 Oct: XP5 returned. All 112 P5 rows match. Confirmed: spread decomposition, 90.2% entry share, sell-impact
  identification, winner gap, announcement formulas. Corrected: uniqueness holds for r > r_S = 2.1241481328…
  (not the rounded interval); count-based range needs incentives; two-cluster claim depends on the challenger
  tie rule; spread is about conditional execution prices. Refuted: the entry component does not rise above the
  ceiling (it is zero there; N1 had the same error). P5 round 2 started to apply the check.
- 23 Oct: XLA returned (check of LA). Propositions 2 and 3 of the Laplace manuscript survive; the audit
  needs scope corrections. Confirmed: all Proposition 2 margins (return 0.002689 in cost, 0.000334 in
  posterior, r_2 − r_C = 0.00734; prior window (0.467850, 0.500424)); Proposition 3 certifies an exact root
  per bracket, unique best responses against each fixed schedule, coexistence and strict entry order at three
  nodes, with no continuous-branch certificate and no parameter box. Refuted: "the return margin is the
  thinnest" (the strong-trade margin 0.002412 is smaller); "numbers reproduce only on a branch" (they follow
  from the pinned primitives). Corrected: LA's margins CSV rounds to nearest, so it is not an interval
  certificate (XLA's CSV replaces it); welfare step 6 uses a conditional expectation; LA_worked.tex uses
  "symmetrically" once (computation supplied in XLA §5) and mixes structural and strict hypotheses.
  The comparison writer uses LA and XLA together.
- 23 Oct: P1 returned. Lemmas 1–3 and Proposition 2 analytical, the same under all four tie-rule pairs;
  (H1)–(H3) right and complete. Proposition 3: complete equilibrium set on [1.2, 3.6] at prior 1/2 for every
  slot in the band (Sturm counts): r_A 1.393958, r_F 1.467127, r_N 1.747878, r_J 1.966097, r_S 2.124148,
  r_C 3.592659. Proposition 4: band 82/59 < u < 2686/1559; prior range (141/(141 + 59e), 4245/(4245 + 1559e)).
  Proposition 5: coexistence at every prior (empty below 0.396175 and from 0.650059). Refuted: β ≤ 1/3 is
  needed only for the zero-order bound and Corollary 1; rule I0 has no equilibrium on (r_N, r_S]; the
  threshold-branch entries at B are 0.341462, 0.321311, 0.305208. XP1 (check) started.
- 23 Oct: LABELS.md written (notation: f_j(x) for order probabilities; equilibrium concept IM with C1 in
  main statements; labels for every statement; appendix A.1–A.9 with A.8 empirical). Phase 3 started in
  parallel with the remaining checks: W1 round 2 (main text), W4 (appendix), F (figures). Writers apply each
  check memo that exists before they finish; a correction pass follows for checks that arrive later.
- 23 Oct: XP3 returned. Every calibrated research claim confirmed (complete sets at six strengths under four
  rule pairs; branch, slope, uniqueness, cap/cost/β bounds, access gains; 138 rows agree). Corrections: 65
  registry enclosure notes are not outward-rounded; the broad uniqueness claim fails under CM at the entry
  ceiling; the general weak-incumbent statement needs a prior-entry hypothesis; cap and posterior margins
  differ in units. P3 round 2 started.
- 23 Oct: P3 round 2 returned: all four XP3 corrections applied; values, displays and keys unchanged; every
  enclosure outward-rounded. Weak incumbent now assumes B_r(1/2) < c_H. Strong incumbents unique on (r_U^R, h)
  under C1; under CM unique except at r_C, where entry fills [1/4, 0.522757]. Cap margin 0.000599 (intensity),
  posterior margin 0.000334. Research package closed.
- 23 Oct: XP1 returned. Core theorems hold: Proposition 2, ownership and uniqueness for every β < 1/2; IM is
  the standard concept; I0 has no equilibrium on (r_N, r_S]; equilibrium sets, band, thresholds and margins
  confirmed; 125 displays agree. Corrected: 55 enclosures not outward; CM coexistence at π = π_max omitted;
  summary row on (r_N, r_S] split; CM entry interval at r_C; Lemma 3 premises; zero-order mass in the no-trade
  case. Refuted: "u is the odds that an order is informed" (under full orders the odds are πu for a purchase,
  (1 − π)u for a sale). BRIEF §2 and LABELS §1 corrected. P1 round 2 started.
- 23 Oct: XP4 returned. R5, R7, R8 confirmed; 1038 rows agree; no circular step. Corrections: frozen entry is
  0.522757 on all of (1, r_C], then 0.25; the R7 proof never uses atomlessness; the B pair (0.95, 0.505) fails
  its no-challenger-signal control (entry 0.522757 there), so the checker proposes (0.94, 0.505) (entry
  0.25 → 0.386933, control 0.25); I0 has no equilibrium at the no-signal control at strength 3.
  P4 round 2 started.
- 23 Oct: P5 round 2 returned: every XP5 correction applied. Full orders unique on r_S < r < h (r_S the exact
  root of ρΔ_T m = k); the entry component rises on (r_S, r_C] and is zero above r_C; the count-based informed
  share ranges over [0.250299, 0.76) at r_1 with incentives; mean announcement return zero over both
  announcements. Open, stated once: selection between N and U; the low-class mixture on [r_N, r_S];
  observation protocols. (Earlier ledger line: uniqueness holds on (r_S, h), not (r_S, 10).) Observables closed.
- 23 Oct: XP2 returned. Every P2 headline confirmed; 3,386 rows agree; nothing refuted. Eight minor
  corrections (notation clashes on η, b, A, D, Γ; a tie-dependence list; one compressed step; "weakly" in the
  payment statement; small-number displays; a limit-row note; registry scope). No number changes. The
  writers apply them directly; LABELS §1 now fixes ω for the seller's share and the other clashes.
- 23 Oct: W3 (comparison note) started; inputs LA + XLA, P1–P5 + checks.
- 23 Oct: F returned: beliefs, coexistence and research figures (paper and slide versions), vector PDF with
  embedded TrueType fonts; plotted boundaries equal the registry at six decimals. Coordinator viewed the PNGs:
  readable, no overlaps; the research figure shades (r_N, r_U) as "equilibrium set not characterized" and uses
  a broken axis. Notation in the research figure (r_R, r̄_R, r_U) must match the manuscript's Section 5.
- 23 Oct: P4 round 2 returned: frozen entry 0.522757 on (1, r_C], then 0.25 under C1; the support theorem covers
  any independent cost law (atoms allowed); the B signal pair is now (0.94, 0.505): entry 0.25 → 0.386933,
  0.25 without the challenger's signal, both controls with strict margins. 1,332 rows; original keys kept.
  Information side closed.
- 23 Oct: W1 round 2 returned: full main text (43 pages) with all five checks applied; 20 numbered
  propositions in the main text. Coordinator note: the Laplace manuscript states Propositions 1–3 in the main
  text and the extensions as Propositions A.x. A consolidation round after W4 and P1 round 2 will match that
  scheme (headline propositions in the main text; region, control, robustness, welfare and observables as
  A-numbered statements), bring the main text to 40 pages or fewer, and apply P1 round 2 and LABELS §1.
- 23 Oct: P1 round 2 returned: all eleven XP1 repairs applied; numbering unchanged; 147 rows, no display
  changes, all enclosures outward. New Remark 1 (CM coexistence at π = π_max, margin 0.000343). Correction:
  "no coexistence from 0.650059" holds under C1 only. The low-class rate is now t̄(r). XP1b (short check of
  four new rows and the repairs) started.
- 23 Oct: W4 finished A.2–A.9 and its memo (the task then ended early; the files are
  complete). Build: 101 pages, every reference resolves, 436 keys, every check memo applied. Proofs: 24, each
  with the tuple, the conditions and bounds on every candidate. W1 round 3 (consolidation) started: Laplace
  numbering scheme (Propositions 1–4 in the main text, the rest as A.x), main text ≤ 40 pages, W4's fixes.
- 23 Oct: XP1b returned: the four new core rows agree with independent outward bounds; Remark 1 holds under
  both CM pairs (margin 0.000343); all eleven repairs pass. Correction: the exclusion of coexistence needs the
  exact π_max; at the literal decimal 0.650059, C1 still permits coexistence (state the cut point by its exact
  definition, not its decimal). Core closed.
- 23 Oct: W3 ended early after a full draft: comparison.tex, 17 pages, six sections,
  compiles, Laplace numbers in `registry/W3_laplace.csv`. Stale: it says the slot manuscript has only
  Sections 1–4 drafted; it cites slot results by section. A finishing round (W3 round 2) follows W1 round 3,
  with the new proposition map, the length target (10–15 pages) and a memo of sources.
- 23 Oct: W3 round 2 started.
- 23 Oct: W1 round 3 returned: main text 36 pages (pages 2–37), appendix 61 pages, 101 in all; no warning of
  any kind in the build. Propositions 1–4 and Corollaries 2–3 in the main text; Propositions A.1–A.14 in the
  appendix; tables and figures in the appendix numbered A.x. Map from old to new numbers in
  `memos/W1_keys.md` (Round 3). Coordinator: two exact zeros now print as 0 (registry displays changed for
  `p4_control_crossing_r0_r1` and `p2_reserve_points_deter_r0_two`).
- 23 Oct: Phase 4 started: W2 round 2 (slides aligned to the final manuscript, figures in, keys remapped)
  and R (referee read of the manuscript).
- 23 Oct: R returned: revise before circulation; Propositions 1–4 survive; benchmark, research and Sturm
  values confirmed independently. Major: Proposition A.12(a) lacks the admissible-slot restriction; Section 6.3
  states the wrong investor support at the strong strength; Section 8 excludes the 0.76 endpoint allowed under
  IM; Proposition A.9's strictness needs ω ≠ 1/2. Ten minor and editorial items. Four economics questions: the
  source of the research cap and cost; an operational public order opportunity; the source of the admissible
  range and its narrow upper margin; a shorter literature account. W1 round 4 started to apply all of it.
- 23 Oct: W3 round 2 returned: comparison.tex, 15 pages, clean build, 145 keys (52 Laplace keys), memo with
  sources. Coordinator read Sections 1–3: accurate and direct. To align after W1 round 4: the count range
  endpoint 0.76 (closed under IM, referee finding 3) and any wording that changes in Propositions A.9 and
  A.12; the title line break.
- 23 Oct: W1 round 4 returned: all 14 referee findings applied, none rebutted; four economics answers added
  (research cap and cost, an operational order opportunity, the source of the admissible range, a shorter
  literature account). Main text 37 pages; 102 pages in all; clean build. Part (e) of A.12 is now Corollary
  A.1. Open from W1: P5's and P2's scripts export enclosures rounded to nearest (P2: 334 notes, P5: 121 with
  equal decimal endpoints). EX (outward enclosures for P2 and P5) started.
- 23 Oct: Coordinator aligned comparison.tex with the referee fixes (ω ≠ 1/2 in the payment row; the closed
  count interval under IM; admissible slots) and fixed the title break. 15 pages of text plus a reference
  page; clean build. LABELS §1 strictness clause corrected.
- 23 Oct: EX returned: both exporters now round outward from exact rational endpoints; every one of 2,269 P2
  and 128 P5 enclosures contains its exact interval. EX stopped before replacement because one P2 display
  differed (`p2_reserve_points_deter_r0_two`: the coordinator's "0" against the exporter's "0.000000").
  Coordinator installed both candidates (notes only: 2,136 in P2, 126 in P5; values, statuses unchanged),
  kept the display "0", and merged: 5,221 keys, no conflicts. A rerun of the P2 exporter restores
  "0.000000" for that one key; keep "0".
- 23 Oct: W2 round 2 returned: slides aligned to the final manuscript; 20 main and 12 backup frames; figures in;
  no missing keys. Coordinator added ω ≠ 1/2 on two payment-rule slides (W2 ran beside W1 round 4).
- 23 Oct: Final state. number_scan: 676 keys used, 0 missing, 0 typed decimals. Builds: main 102 pages
  (main text 37), comparison 15 pages plus references, slides 34 pages; no overfull box, no undefined
  reference, no unknown key; no Type 3 fonts. "Laplace" appears once in the manuscript (rem:sizes) and once in
  a backup slide. Local commits in overleaf/competition_slot: 28f39f9 (documents), d28f8c2 (start note). Not
  pushed: the Overleaf project does not exist yet.
