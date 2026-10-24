# W1: the main text of the order-slot manuscript (round 2)

Workstream W1, round 2, 23 October 2026. Files written in this round:

- `overleaf/competition_slot/main.tex` (abstract, guarded appendix inputs, figure macro, notation macros);
- `overleaf/competition_slot/sections/01_introduction.tex` to `09_conclusion.tex` (all nine; Sections 3.2–9 new,
  Sections 1, 2.3, 2.4, 3.1 revised);
- `registry/W1.csv` (37 rows) from `scripts/W1/w1_registry.py` (run log `scripts/W1/w1_registry.log`);
- `scripts/W1/lookup.py` (prints registry rows by key pattern);
- this memo.

I did not edit any appendix file. I ran `scripts/_coordinator/make_numbers.py` after each registry change
(last run: 5138 keys, 0 conflicts).

## 1. Build and page counts

`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`: exit 0 at 15:08, 93 pages. (At 15:04
the build stopped once in W4's `appendix/A6_robustness.tex`, line 278, `\DT_P`; W4 fixed it by 15:06.)

| Part | Pages |
|---|---|
| Title and abstract | 1 |
| Main text (Sections 1–9) | 2–44 (43 pages) |
| References | 45–47 |
| Appendix A (W4: A.1–A.7 written, A.8 and A.9 stubs at 15:08) | 48–93 (46 pages so far) |

- Undefined references: `tab:margins` only (cited in §4.2 and by W4; W4 defines it in A.9).
- Undefined `\reg` keys: none.
- The main text is 3 pages above the 30–40 target at one-and-a-half spacing. Two trimming passes removed about two
  pages. A further cut would remove stated content (tables `tab:payoffs`, `tab:classes`, `tab:reserves`, or the
  Section 8 propositions beyond the spread). The author can choose.
- Appendix inputs use `\slotappendix{A1_payoffs}` … `\slotappendix{A9_parameters}` (LABELS names). A missing file
  prints a framed placeholder. A check build of the main text alone skips the appendix:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build -jobname=main_w1check -usepretex='\def\slotskipappendix{1}' main.tex`.
- Figures use `\slotfigure{figures/<name>.pdf}{height}` at the full line width, as `memos/F_figures.md` asks; a
  missing file prints a framed placeholder. The three figures are included: `fig:beliefs` in §4.2 (page 23),
  `fig:coexistence` in §4.3 (page 26), `fig:research` in §5 (page 31).

## 2. Checks applied, and checks that did not exist

All five check memos existed before I finished, and I applied each one.

| Check | Applied in the main text |
|---|---|
| XP1 | u is described as the presence probability relative to one-direction liquidity mass; 1 + u is the largest likelihood ratio (§2.3, §1). `lem:trading` states its premises (E1), (E4), e ∈ [ρ, 1], Δ_T ≥ 0. `cor:exclusion` is stated for profiles that satisfy (E1)–(E3). `prop:priors`: r_π defined only for τ(r_0) ≤ π ≤ τ(r_2); r_C(π) only when it exists; under CM the set gains r_π for every π ∈ (π_A^hi, π_max], and at π_max this point is the whole set. CM entry at r_C fills [ρ, 1] after a purchase (`rem:ties`). I0 table as corrected (empty on (r_N, r_S]). Decimal endpoints of exact intervals carry ≈ or "to six places". |
| XP2 | Seller weight renamed ω (η is the liquidity law). `prop:payment`: "weakly has the sign of 1 − 2ω, and strictly when E[(R − ℓ)_+] changes strictly". Exclusion reserves give flat entry; 31/20 excludes the low class and the weak incumbent. |
| XP3 | Research uniqueness above r_U^R: unique under C1, and under CM except at r_C, where entry fills [ρ, 0.522757] (`rem:researchties`). The weak-incumbent case is stated at the benchmark, where B_r(1/2) < c_H holds. The cap margin 0.000599 "corresponds to" the posterior margin 0.000334. The cost window is exact for three interior research choices; strict entry growth alone holds on a wider window (no number printed). |
| XP4 | `prop:atomless` allows any component laws with the stated supports, atoms included; atomlessness is used only for the continuous ramp. The control text gives the step: frozen entry 0.522757 up to r_C, ρ above. Signals: S(B) is its own vector; at B the pair (0.94, 0.505) (P4 round-2 keys `p4_comp_b_*`) replaces (0.95, 0.505), which is not presented as complementary information; the mixed B equilibria need IM. |
| XP5 | Uniqueness of full trade on (r_S, h) with the exact r_S; the entry component is zero above r_C (split statement); "conditional execution prices", no quote stage; count-based range limited by incentives [0.250299, 0.76) and the band (0.41, 0.462784); maintained inputs ρ and Δ_T in identification; zero-mean announcement return over both reports, positive mean in a sample of preparation reports (P5 round-2 key `evprep_mean_r1_B`); measurement records the zero order; the two-cluster claim stated under C1, with CM adding a third pattern. |

P4 and P5 round-2 packages landed during this round; the text uses their new keys. No check for the P5 round-2
package existed when I finished.

## 3. Registry keys

The main text prints 360 keys (counted from the source): P1 49 (+20 shared with P2/P4), P2 138, P3 47, P4 33,
P5 37, W1 36. Every key resolves. The full list is reproducible with
`grep -o '\\reg{[^}]*}' overleaf/competition_slot/sections/*.tex | sort -u`.

### New keys in `registry/W1.csv` (please keep in the merge)

| Key | Display | Status | Meaning |
|---|---|---|---|
| `prim_h`, `prim_ell`, `prim_p`, `prim_rho`, `prim_cH`, `prim_k`, `prim_pi`, `prim_r0`, `prim_r1`, `prim_r2` | 10, 1, 1/2, 1/4, 6, 1/50, 1/2, 6/5, 3, 18/5 | input | benchmark primitives (same names as W2) |
| `Bprior_r0`, `Bprior_r1_B`, `Bprior_r2` | 4.804167, 4.291667, 4.134722 | analytical | B_r(1/2) = 1153/240, 103/24, 2977/720 |
| `B_r1_half` | 103/24 | analytical | exact form of `Bprior_r1_B` |
| `str_r140` … `str_r165` | 1.40, 1.45, 1.55, 1.60, 1.65 | input | strengths named in keys of P1, P3, P5 |
| `u_kstrong_frac` | 19/3 | analytical | right side of (H2) at r_1 (P1 `u_kstrong` prints 6.333333) |
| `atom_L`, `atom_eps`, `atom_eps_small` | 1/5, 1/10, 1/1000 | input | P4 cost law (P4 prints them as 0.200000, …) |
| `sig_rho`, `sig_cH`, `sig_k`, `sig_r0`, `sig_r1`, `sig_aT`, `sig_d` | 0.85, 7.14, 0.015, 1.1, 2.3, 0.70, 0.75 | input | the vector S(B) and its accuracies |
| `sig_comp_aT`, `sig_comp_d` | 0.94, 0.505 | input | the complementary pair at B (P4 `p4_input_comp_*`) |
| `access_out_cH` | 12/5 | input | high cost outside the recruitment region (P2) |
| `pay_gap_coef` | 13/20 | analytical | Δ_ω(r_1) − Δ_ω(r_0) = (13/20)(1 − 2ω) |
| `rsv_points_excl`, `rsv_bands_excl`, `rsv_deter` | 101/100, 11/10, 31/20 | input | the three reserves of P2 |

The script prints a check of `pay_gap_coef` from E[(R − ℓ)_+] = (r − ℓ)²/(2r).

### Notes on other workstreams' keys

- The P1 keys that I print include rows whose enclosure notes XP1 lists as non-outward (for example `lambda_B`,
  `rC_B`, `price_r1_p1_B`). Their displays are correct (XP1); only the notes need repair by P1.
- `ba_share_r1_B` contains `\%`; it prints "90.2%".
- `pdrop_neutral_r2_B` and `cov_entry_r2_B` display "0.00"; the text prints them as values at r_2.

## 4. Notation and drafting decisions (for W4 and W3)

1. **Definition 1 (§2.4) now follows P1.** Tuple (σ_H, σ_L, μ, P, μ̄, ζ) plus bids; ζ is the high-cost preparation
   probability, and the zero-cost challenger prepares after every price. Conditions: (E1) Bayes, (E2) challenger
   beliefs, (E3) entry optimality, (E4) competitive prices, (E5) investor optimality, (E6) truthful bids; Section 5
   adds (E7) research optimality. W4's A.2 and A.3 use the same numbers.
2. **Tie rules (§2.4, LABELS §2).** IM is the concept; C1 in all main statements; I0 and CM in remarks
   (`rem:ties` in §4.3, `rem:researchties` in §5) and in short sentences next to the statements they change.
   Proposition 2 "holds under all four tie-rule pairs" is said once, in §4.1.
3. **Symbols.** f_j(x) order probabilities; b_0 = (1 − λ)(1 − 2β); κ(π); τ; J(r); 𝔯(d) (`\fr`); s_+ = λσ_H(1) and
   s_− = λσ_L(−1) (P1 writes s, t; t clashes with t_j); Euler's number upright `\eu`; entry 𝖤 (`\Ent`), ownership
   𝖮 (`\Own`); seller weight ω (P2 writes η); research cap λ̄ (`\lb`), conjectured intensity λ̂; λ_E(r), λ_R(r),
   M_λ, m_λ; signals T, Y with accuracies a_T, d; φ_±; μ_±; D^+(r). Section 8 writes b + λ/2 in place of P5's d.
4. **Names.** The benchmark vector is called B in the text ("The benchmark, which I call B"); the signal vector is
   S(B). Value-class examples A–D of P2 appear as "Low prior", "High prior", "Wide classes", "Same means, points"
   (the letter B is taken). P1's forms N, R, F, Q, T keep their letters in §4.3.
5. **Labels I own beyond LABELS:** `tab:classes`, `tab:reserves`, `rem:ties`, `rem:researchties`, `eq:odds`,
   `eq:research`. Section 8 cites `app:empirical`; Section 6 cites `app:robustness` for the three-class collision.
6. **Status labels in headers.** `prop:research`, `prop:researchregion`, `prop:coexistence`, `prop:priors` are
   computer-assisted; every other main-text result is analytical. Benchmark values in the text carry
   "(computer-assisted)" where they rest on interval arithmetic.
7. **Parallel universe.** "Laplace" and "noise" occur only in `rem:sizes`. No sentence refers to another set-up,
   an earlier study or a calibration A. `rem:sizes` does not state the scale that matches B.

## 5. Open items

1. **Page count.** Main text 43 pages against 30–40 (see §1).
2. **Figure captions (closed).** The notes now describe the panels that F drew (read from `memos/F_figures.md` and
   the PNG previews): `fig:beliefs` plots τ(r) with the posterior band and a zoom on [r_1, r_2], so it moved from §3.2
   to §4.2; `fig:coexistence` has panels (a) path and (b) zoom, with T under CM; `fig:research` has panels (a)
   research and (b) entry, a broken axis and a gray band on (r_N, r_U). The text uses F's symbol r_U (P3: r_U^R).
3. **`tab:margins`** waits for W4's A.9.
4. **Results that stay open in the text, each stated once:** the equilibrium set with research on (r_N, r_U^R);
   the trading game under the bargaining rule; the seller's reserve choice with the whole continuation; equilibrium
   selection between no trade and purchases only on (r_F, r_N).
5. **Bibliography.** Unchanged from round 1. New citations in this round use existing entries only
   (`BulowKlemperer1996`, `Schwert1996`).

## 6. Claims refuted or corrected in this round

- None of the brief's claims is refuted by this round. Corrections that change wording against earlier memos:
  the pair (0.95, 0.505) is not complementary information (XP4); u is not "the odds that an order is informed"
  (XP1); the entry component of the spread does not rise above r_C (XP5); the decimal interval (2.124148, 10) is not
  the uniqueness region (XP5).

## Round 3 changes (consolidation, 23 October 2026)

Files changed in this round: `main.tex`; `sections/01_introduction.tex` to `09_conclusion.tex`; and, for the moved
statements only, the appendix files `A2_beliefs_trading.tex`, `A3_proposition2.tex`, `A4_coexistence.tex`,
`A5_research.tex`, `A6_robustness.tex`, `A7_welfare.tex`, `A8_empirical.tex`, `A9_parameters.tex`. Scripts and logs in
`scripts/W1/`: `pagemap.py` (prints the page of each heading), `build_r3.log`, `main_r2.aux` (the round-2 numbering,
kept for the map), `main_keys_r3.txt` (keys that the main text prints), `png/` (page renders). No registry row changed.

### R3.1 Build and page counts

`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`: exit 0, 101 pages.

| Part | Pages |
|---|---|
| Title and abstract | 1 |
| Main text (Sections 1–9) | 2–37 (36 pages; round 2: 43) |
| References | 38–40 |
| Appendix A | 41–101 (61 pages) |

The log has no warning of any kind: no overfull box, no undefined reference, no unknown `\reg` key, no float warning
and no duplicate hyperlink destination. (The last one was pre-existing: the tagged display (U) in A.5 used a numbered
`equation`, so its anchor collided with equation (A.8); it now uses `equation*` with `\tag{U}`.)
The main text prints 253 distinct keys (round 2: 360); the appendix prints 507.

### R3.2 Numbering scheme

The main text states Propositions 1–4. Every other proposition is stated in full in the appendix, as Proposition A.x,
just before its proof, with its label and its statement unchanged. The main text keeps one short paragraph per result,
with its key numbers and the reference. Decisions:

- `prop:priors` is **Corollary 2** (statement unchanged, status label computer-assisted).
- `prop:researchbranch` is **Corollary 3** (statement unchanged). A corollary keeps its own status label
  (analytical); a part of Proposition 4 would carry the computer-assisted label of the benchmark claims.
- The lemmas and the corollary of Section 3 stay in the main text: the discussion of Proposition 2 uses Lemma 3 and
  Lemma 2(c).
- Every reference to `prop:priors` or `prop:researchbranch` now reads "Corollary" (main text, A.2, A.4, A.5, A.9).
- The appendix numbers tables and figures A.x (`\thetable`, `\theHtable`, `\thefigure`, `\theHfigure` reset at
  `\appendix`).

### R3.3 Map from the round-2 numbers to the round-3 numbers

For the slides and the comparison note. "Where" is the place of the statement in round 3.

| Label | Round 2 | Round 3 | Where |
|---|---|---|---|
| `prop:returns` | Proposition 1 | Proposition 1 | §3.1 |
| `lem:beliefs` | Lemma 1 | Lemma 1 | §3.2 |
| `cor:exclusion` | Corollary 1 | Corollary 1 | §3.2 |
| `lem:prices` | Lemma 2 | Lemma 2 | §3.2 |
| `lem:trading` | Lemma 3 | Lemma 3 | §3.3 |
| `prop:ccc` | Proposition 2 | Proposition 2 | §4.1 |
| `prop:region` | Proposition 3 | Proposition A.1 | A.3 |
| `prop:control` | Proposition 4 | Proposition A.3 | A.6 |
| `prop:coexistence` | Proposition 5 | Proposition 3 | §4.3 |
| `prop:priors` | Proposition 6 | Corollary 2 | §4.3 |
| `prop:research` | Proposition 7 | Proposition 4 | §5 |
| `prop:researchbranch` | Proposition 8 | Corollary 3 | §5 |
| `prop:researchregion` | Proposition 9 | Proposition A.2 | A.5 |
| `prop:atomless` | Proposition 10 | Proposition A.4 | A.6 |
| `prop:classes` | Proposition 11 | Proposition A.5 | A.6 |
| `prop:manyclasses` | Proposition 12 | Proposition A.6 | A.6 |
| `prop:signals` | Proposition 13 | Proposition A.7 | A.6 |
| `prop:access` | Proposition 14 | Proposition A.8 | A.7 |
| `prop:payment` | Proposition 15 | Proposition A.9 | A.7 |
| `prop:reserves` | Proposition 16 | Proposition A.10 | A.7 |
| `prop:spread` | Proposition 17 | Proposition A.11 | A.8 |
| `prop:informedshare` | Proposition 18 | Proposition A.12 | A.8 |
| `prop:winner` | Proposition 19 | Proposition A.13 | A.8 |
| `prop:announcement` | Proposition 20 | Proposition A.14 | A.8 |
| `rem:ties`, `rem:researchties`, `rem:sizes` | Remarks 1, 2, 3 | Remarks 1, 2, 3 | §4.3, §5, §6.4 |
| `lem:a4-path` … `lem:a5-strong` | Lemmas A.1–A.10 | Lemmas A.1–A.10 | A.4, A.5 |
| `tab:payoffs`, `tab:region`, `tab:outcomes`, `tab:research` | Tables 1–4 | Tables 1–4 | §4.2, §5 |
| `tab:classes` | Table 5 | Table A.4 | A.6 (moved from §6.2) |
| `tab:reserves` | Table 6 | Table 5 | §7.3 |
| `tab:a4-thresholds`, `tab:a4-set`, `tab:a4-ties` | Tables 7, 8, 9 | Tables A.1, A.2, A.3 | A.4 |
| `tab:a9-declarations`, `tab:margins` | Tables 10, 11 | Tables A.5, A.6 | A.9 |
| `fig:beliefs`, `fig:coexistence`, `fig:research` | Figures 1–3 | Figures 1–3 | §4.2, §4.3, §5 |

### R3.4 What moved, what was cut

- **Moved with their statements:** the setup that each statement needs went to the appendix with it: the cost law
  `H_C` (A.6), the class set `𝓜_π` and the groups (A.6), the signals `T`, `Y`, `μ_±`, `φ_+`, `D^+` (A.6, before W4's
  paragraph on beliefs), the access economy and `𝓡`, `𝓦` (A.7), the bargaining institution (A.7), the indicator `J_r`,
  the volume `v`, the spread and impacts, the events `A`, `W` and the announcement event (A.8). Each appendix
  subsection opens with "states and proves".
- **Table `tab:classes`** now has two panels (primitives, outcomes) in `\footnotesize`; the round-2 overfull box of
  130 pt is gone. Its values and notes are unchanged.
- **Cut from the main text because the appendix already states it:** the list "each hypothesis is used once" and the
  `nec_cH` example (§4.1; A.3 keeps both); the tie remark on the band endpoint (A.3 part (b)); the detail of the
  research cost window (A.5); the narrow-band proceeds and the boundary reserves (A.7); per-order win probabilities,
  announcement increments and the alternative slot's λ′, β′ (A.8).
- **Sections 6–8** are prose summaries in the style of the pinned manuscript's Sections 5–7: one paragraph per result,
  its key numbers, and "Proposition A.x".

### R3.5 Fixes from W4's memo §3 and the other items of the task

- **u (§2.3, §1):** "the informed presence mass relative to the liquidity mass in one direction"; `1 + u` is the
  largest likelihood ratio of an order. §4.2 calls `1 + u = e` "the largest likelihood ratio of an order"; Table 2 row
  "Mass ratio u" (was "Odds ratio u").
- **Zero-cost preparation:** Definition 1 unchanged ("A challenger with the zero cost prepares after every price"),
  with the paragraph after it that gives the reason; §3.2 states its three uses.
- **Overfull boxes:** `tab:classes` (130 pt, now in A.6), the region display (3.9 pt, `\qquad` → `\quad` in the moved
  statement), the signal display (18.9 pt, split in A.6). The float of Table A.6 was 3.8 pt too tall; its
  `\arraystretch` is now 1.04.
- **Figures:** §5 defines `λ̄` (the cap), `r_R` and `r̄_R` (start and end of the branch), and
  `r_U = 𝔯((k + aλ̄)(1 + e)/ρ) ≈ 2.434046`, the symbol in the figure. A.5 wrote `r_U^R`; it now writes `r_U`. The three
  captions describe the panels of `memos/F_figures.md` and carry no status label. (Table notes of `tab:classes` and
  `tab:reserves` keep "Values are computer-assisted".)
- **Parallel universe:** `grep -i laplace` over `main.tex`, `sections/`, `appendix/` and `references.bib` finds only
  `rem:sizes` (`sections/06_robustness.tex`).
- **XP1b (applied):** the prior cutoff is the exact symbol `π_max`, with the decimal as an approximation, in §4.3 and
  in A.4 (`π_max ≈ 0.650059`; also `π_A^lo ≈`, `π_A^hi ≈`). The four new rows and Remark 1 need no text change.
- **Style pass:** abstract, introduction and conclusion rewritten to TEAM_RULES §8–9 (sentences of 25 words at most in
  new text; mechanism paragraphs merged; open items stated once, in their sections; the conclusion names one next
  step and two tests). `scripts/W1/style_report.py` flags only table rows, figure notes and pre-existing paragraphs of
  seven sentences.

### R3.6 Points for the coordinator

1. Two exact zeros print as `0.000000` from their registry displays: `p4_control_crossing_r0_r1` (§4.2) and
   `p2_reserve_points_deter_r0_two` (Table 5). They are exact (analytical) zeros, not small numbers; a display `0`
   would read better.
2. Proposition 3 still cites "the band of Proposition A.1(a)" in its statement; the main text states the band in
   §4.2, so the reference resolves to a statement the reader has seen in summary.
3. Pages rendered and inspected (`scripts/W1/png/`): 1, 20, 30, 31, 35, 51, 78, 82, 92, 99. No clipped table, no
   overlap; Table A.4 fits the text width; Figure 3 shows `r_R`, `r̄_R`, `r_N`, `r_U`, `r_C` as §5 defines them.

### R3.7 Claims refuted or corrected in this round

None refuted. XP1b's correction ("from 0.650059" → `π_max`) is applied.

## Round 4 changes (referee report, 23 October 2026)

Source: `memos/R_referee.md`. Every demonstrated finding is applied; none is rebutted. Line numbers refer to the
round-4 files in `overleaf/competition_slot/`. The round-3 sources are in `scripts/W1/round3_src/`, and the diffs are
`scripts/W1/round4_sections.diff`, `round4_appendix.diff` and `round4_main.diff`.

### R4.1 Findings

| # | Finding | Result | Where |
|---|---|---|---|
| 1 | A.12(a) omits admissibility | applied: a slot with ratio u′ and volume v exists iff 3v ≤ 2 + u′(1 − v), equivalently ϑ′ ≥ 3 − 2/v; unique when it exists. Proof derives the equivalence; the text gives u′ = 1/10 as a ratio with no slot | `appendix/A8_empirical.tex:88–91`, proof `:107–112`, `:132–135` |
| 2 | §6.3 wrong support at r_1 | applied: at r_0 both signal types mix (trade probability 0.721409); at r_1 the investor buys fully after T = + and sells with probability 0.775969 after T = −; "neither strength has an equilibrium" under I0. A.6 now says each equilibrium has a mixed order and names which. Checked against `proofs/P4_information.tex:855–890` (s = λ, t = 4b/3) | `sections/06_robustness.tex:83–88`, `appendix/A6_robustness.tex:507–509` |
| 3 | §8 excludes 0.76 under IM | applied: closed interval [≈0.250299, 0.76] under IM; strict incentives or I0 exclude the endpoint. A.8 adds the endpoint argument: under IM full trade is the unique outcome at ϑ′ = 19/25; under I0 this slot has no equilibrium at r_1. Registry note of `theta_max_full_eq_r1_B` corrected (note only) | `sections/08_empirical.tex:30–33`, `appendix/A8_empirical.tex:136–143`, `registry/P5_observables.csv` |
| 4 | A.9 strictness needs ω ≠ 1/2 | applied: strict when E[(R − ℓ)_+] changes strictly and ω ≠ 1/2; at ω = 1/2 the spread is (h − ℓ)/2 for every incumbent. Proof ends with the ω = 1/2 case | `appendix/A7_welfare.tex:112–115`, `:137`; `sections/07_welfare.tex:39–42` |
| 5 | A.12(e) vacuous under r_S < r < h | applied: (e) removed from A.12 and restated as Corollary A.1 (`cor:purchasesonly`): counts identify the slot when σ_H = δ_1, σ_L = δ_0 (form F on [r_F, r_N]); on branch R they identify s_+ = 2E[X] and b, not λ (proof: s_+ = b[Δ_T/k − 2] on R does not depend on λ) | `appendix/A8_empirical.tex:144–169`; corollary counter reset to A.x in `main.tex:130–132` |
| 6 | s* undefined outside π < τ < M(π) | applied: s* defined for π < τ < 1 (τ < 3/4 on the path by Lemma A.1(a)); s* < λ iff τ < M(π), s* = λ iff τ = M(π); (R) and (T) empty when τ ≥ M(π) | `appendix/A4_coexistence.tex:148–157` |
| 7 | Lemma 3 premises omit (E6) | applied: (E1), (E4) and (E6) in the statement and the proof; A.2 part (b) of Lemma 2 and the A.7 reserves proof now name (E6); A.1 "(E5)" → "(E6)" | `sections/03_competition_information.tex:169`, `appendix/A2_beliefs_trading.tex:97, 127`, `appendix/A7_welfare.tex:176`, `appendix/A1_payoffs.tex:18` |
| 8 | A.14(iii) proof covers only 𝓕 | applied: statement now names the pooled sample and says a report after e(x) = 1 changes the price by zero; proof adds the general step (E[μ(X)] = 1/2 < τ(r) gives an order with e = ρ, positive probability, positive term) | `appendix/A8_empirical.tex:199–212`, proof `:222–229` |
| 9 | `vol_full_B` labelled as an enclosure | applied (note only, value unchanged): the note says the value is a nearest-rounded point and gives the outward enclosure from `scripts/R_referee/recompute.log` and the XP5 certificate. `make_numbers.py` rerun: 5221 keys, 0 conflicts | `registry/P5_observables.csv` (script `scripts/W1/r4_registry_notes.py`, log `r4_registry_notes.log`) |
| 10 | open-set paragraph includes failure rows | applied: the claim covers the rows that hold at B, with their required sign; it excludes the atomless third economy at ε = 1/10, the same-means control, the d ≥ a_T impossibility row, and exact ties (stated valid under their tie rules). Duplicate tie sentence in the margins paragraph removed | `appendix/A9_parameters.tex:246–262` |
| 11 | four-class inputs missing | applied: values 1, 1001/1000 (low group), 9999/1000, 10 (high group), prior 1/4 each, beside the certificate and in Table A.5 (new input rows `four_v1`–`four_v4`, `four_prior` in `registry/W1.csv`) | `appendix/A6_robustness.tex:346–348`, `appendix/A9_parameters.tex:32–33` |
| 12 | lower boundary of the band | applied: A.1(b) says the open band is exact; at u = 82/59 orders are uniquely full and C1 gives every conclusion, while CM allows entry after a purchase anywhere in [ρ, 1]. §4.2 states the same in one paragraph | `appendix/A3_proposition2.tex:168–172`, proof `:207–210`; `sections/04_equilibrium_results.tex:123–125` |
| 13 | reserve and cluster summaries | applied: "can make the price informative … If the top posterior then recruits at both strengths, entry is flat"; "the model permits two clusters" | `sections/01_introduction.tex:90–92`, `sections/09_conclusion.tex:17–19`, `sections/08_empirical.tex:60` |
| 14 | notation and repetition | applied: "Slot mass ratio" (A9:23); external dividend without a symbol (A7:76); A.8 indicator J_r → χ_r and order mass d → f̄ (A8:7–8 and every use); Γ(·) function only, total mean gap Γ̄ (A6:162–181); "let F_2 strengthen F_1 in the same sense" (§4.1:13); "best nonzero order" (§5:75). Repetition: the lead-in before Definition 1 and the uniqueness sentence after Proposition 2 removed; roadmap shortened; full script prefix kept once in the A.2 conventions (`appendix/A2_beliefs_trading.tex:24–25`), all other 54 appendix paths relative | as listed |

### R4.2 The four economics questions

1. **Research cap and cost (§5, `sections/05_research.tex:9–20`).** The cap is the probability that the specialist's
   own research can reveal the class before the challenger decides; some facts become visible only through the buyer's
   diligence. The marginal cost rises because cheap sources come first and costly ones later; the quadratic is the
   simplest such form. A success takes the place of a liquidity order because the opportunity has room for one order:
   after a failure the investor knows no more than the market, so an order would lose at least k.
2. **Operational opportunity (§8, `sections/08_empirical.tex:68–73`).** A scheduled call auction, such as the opening
   auction on the first trading day after disclosure; its time is fixed in advance; the sign of the net imbalance is
   the order, and an imbalance below a size fixed in advance is the zero order. No institution-specific claim, no
   citation.
3. **Admissible range and upper margin (§4.2, `sections/04_equilibrium_results.tex:153–168`).** Both band ends are
   preparation thresholds; the band is narrow because the high-class challenger's expected payment r/2 + p²/(2r) rises
   by less than 1/2 per unit of strength, small next to g_H − g_L. The upper margin is one distance in three units
   (posterior 0.000334, cost 0.002689, strength 0.007341); given the auction primitives it depends only on M(1/2) and the
   place of r_2; (H3) holds at every strength in (r_C, h), and parts (i)–(ii) do not use it. No new number printed.
4. **Literature (§1, `sections/01_introduction.tex:102–140`).** Seven paragraphs became four plus the roadmap; four
   footnotes carry the secondary detail. Kept in the text: real effects and the closest antecedent, learning from
   prices, selective entry with the price as the pre-entry signal, and the investor without stake or control. Every
   citation key of round 3 is still cited (checked by a sorted key list).

### R4.3 Build and page counts

`latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`: exit 0; log copy
`scripts/W1/main_r4.log`. No overfull box, no undefined reference, no unknown `\reg` key, no `??` in the PDF text,
and no line with "warning" in the log except package names (`grep -i warning`, microtype lines excluded).

| Part | Pages |
|---|---|
| Title and abstract | 1 |
| Main text (Sections 1–9) | 2–38 (37 pages; round 3: 36) |
| References | 39–41 |
| Appendix A | 42–102 (61 pages) |

Main text prints 254 distinct keys; the appendix prints 512. Rendered and inspected at 80 dpi
(`scripts/W1/png/r4/`): pages 4, 5, 17, 19, 26, 28, 33, 34, 36, 37, 38, 42, 46, 47, 52, 53, 57, 77, 81, 85, 88, 89,
94–99; pages 97 and 99 again from the final build. One defect found and fixed on inspection: "1/2 > μ(x)" in the
A.14 proof is now "1/2 ≥ μ(x)". The later uses of s* in A.4 (lines 260–432) sit in cases with τ < M(π) or state
the domain, so the wider definition needs no other change.

### R4.4 Registry

- `registry/P5_observables.csv` (P5's file): note fields of `vol_full_B` (finding 9) and `theta_max_full_eq_r1_B`
  (finding 3) corrected; values, displays, statuses unchanged; CRLF line ends kept. Rerunning
  `scripts/P5_observables/p5_observables.py` would restore both old notes; its formatter still rounds endpoints to
  nearest, so other rows with "Enclosure [x, x]" notes (for example `theta_min_counts_B`) carry the same defect. Only
  `vol_full_B` was in scope.
- `registry/W1.csv`: five new input rows (`four_v1`–`four_v4`, `four_prior`), 42 rows in all.

### R4.5 For other workstreams (not edited here)

- `comparison.tex:213` states the payment strictness without ω ≠ 1/2; `comparison.tex:356` prints the half-open
  interval `[theta_min_counts_B, theta_max_full_eq_r1_B)`; under IM it is closed.
- LABELS §1 states the payment strictness clause without ω ≠ 1/2 (finding 4).
- New label `cor:purchasesonly` (Corollary A.1); Proposition A.12 now has parts (a)–(d). Numbering of A.1–A.14 and
  Lemmas A.1–A.10 is unchanged. A.8 now writes χ_r (entry indicator) and f̄ = b + λ/2.

### R4.6 Claims refuted or corrected

None of the brief refuted. Two corrections beyond the report: Lemma 2's proof, part (b), also rests on (E6) through
Step 0 (same root as finding 7); and at the share 19/25, full two-sided trade is the unique IM outcome at r_1, while
rule I0 has no equilibrium for that slot (both proved in A.8).
