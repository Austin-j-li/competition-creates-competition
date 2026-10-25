# Plan for the theory upgrade: theory and proofs lens

Read PLAN.md first. Its stage order, staffing roles, cloud-only execution, decision gate and delivery restrictions override the earlier alternatives in this lens. All study-relative source paths below are relative to `audit/theory_upgrade_2026_10_25/`.

25 October 2026. Planner for theory and proofs (one of three lenses). Read-only planning; the only file written is this one.
Line numbers refer to the master `overleaf/slot/` at commit 69c25f4.

Source abbreviations used throughout:

- **W1A … W5A**: the referee reports `referee/W1.md` … `W5.md`, cited by section heading and equation number as printed there.
- **WA**: `WORKAROUNDS.md`; "WA W3.5" is item 5 under W3 in its appendix of formal statements.
- **RED**: `scan/reduction_A3_A5.md` (the reduction lemma, existence at prior 1/2, the CM error). **GEN**: `scan/generality_A1_A2_A6_A8.md`. **SCAN**: `SCAN.md`. **FAB**: `referee/second_opinion.md`.
- Tie rules (plan shorthand only; the manuscript uses the plain phrases): IM, an indifferent investor may mix; I0, it abstains; C1, an indifferent high-cost challenger prepares; CM, it may prepare with any probability. Defaults: IM and C1.
- Strength names: r_R (research starts), r_λ̄ (research reaches its cap; today written r̄_R), r_N (no trade ends, low class starts to sell), r_S (sure sale), r_Q (floor-entry research stops coexisting with capped recruiting; the memo's r_X ≈ 2.167), r_U (condition U), r_C (entry ceiling).

---

## 1. Summary

The upgrade proves each result at the generality its proof supports; the benchmark (point classes h = 10, ℓ = 1, uniform incumbent) stays as the worked example that checks each condition and supplies numbers and figures.

The appendix gains five blocks of mathematics. A2: trading, beliefs and entry depend on the auction only through the spread Δ and the threshold τ, and a stronger incumbent raises both. A4: coexistence holds exactly in a fixed region of the (Δ, τ) plane, entry rises with the spread, the sure-purchase stretch is one interval along any path, and the uniform-incumbent condition gives one interval of strengths; that corollary and a squared balance inequality replace both polynomial root counts of the benchmark path lemma by hand proofs. A5, at prior 1/2 when an indifferent investor may mix: research and entry rise with the spread through the low class's selling up to the cap, the equilibrium exists exactly while the top posterior reaches the threshold, ownership rises under outbidding, and cheap research gives one interval along a path; a three-outcome lemma fills the research figure. A3 and A6: Proposition 2 gains the takeover share under outbidding and a decisive-advantage lemma; A.7 extends to ranked classes. A8: a weighted price test at every prior, the winner sign under two-sided trade, identification at a known prior, the exact announcement condition.

the mathematics writer writes each package from the referee reports and the independent referee referees it; the prose writer integrates, writes prose and sweeps the language; the second reader reads last. Every number a consumer cites for a proposition, corollary, remark or definition stays fixed. Script, registry, certificate and calibration-B text leaves the appendix. Part 3.4 assigns eight proof obligations no referee report discharged, chiefly the uniqueness of r_Q ≈ 2.167. Fourteen stages; about 450 net lines of LaTeX.

---

## 2. Stages in dependency order

### Language acceptance (LA), part of every stage's acceptance criteria

These rules come from Austin through the coordinator and override `STYLE_GUIDE.md` §2.4 and §2.7 wherever they conflict.

- **LA1, no status labels.** No "analytical", "computer-assisted", "numerical diagnostic", "certified", "certificate", or "open" used as a status, in any title, sentence, table note or caption, in the main text, the appendix, `comparison.tex` or `slides.tex`. A proof method appears inside an appendix proof as mathematics: "an exact rational computation gives", "evaluating the closed form at r_2 gives", "the quadratic formula gives".
- **LA2, no defensive writing.** Each result is stated positively, with its scope inside the claim. A named condition is a hypothesis, stated once. No caveat, reassurance or pre-emptive referee paragraph; no hedge ("arguably", "it should be noted", "only in the benchmark" as a disclaimer; "may" survives only in the tie-rule phrases); no paragraph ends on a limitation.
- **LA3, no development log.** No narration of change that refers to the paper ("now", "no longer", "new", "updated", "revised", "corrected", "replaces", "in this version", "unlike the earlier draft", "previously"); no upgrade announcement ("this generalizes the earlier result", "the benchmark restriction is removed"); no process words (registry, script, run log, exercise, checker, certificate, run, verified, recomputed, Sturm-count certificates as objects, file names, keys, "calibration B", "Value at B", "S(B)", weakness or workstream codes); no sentence about what was checked. Comparative statics across strengths stay ("above the ceiling, orders no longer predict entry").
- **LA4.** "I"; every number through `\reg{key}`, fractions included; no bold sentence in running text; no tool, reviewers or model name.
- **LA5.** Each stage runs the sweep patterns of Appendix B on everything it wrote. Every hit is fixed, or justified in one line of the stage report ("may mix" as a tie rule, "open interval" as mathematics, "no longer predict entry" as comparative statics).
- **LA6.** All prose written by any model gets an anti-defensive and humanizing pass before it enters the master.

### Stage overview

| Stage | Content | Depends on | Writer | Checker |
|---|---|---|---|---|
| S0 | Decisions, Overleaf pull, branches, `ty` | none | coordinator, Austin | coordinator |
| S1 | Notation freeze, rule card | S0 | the prose writer and integrator | the independent referee (math symbols), the production assistant (collision grep) |
| S2 | A2 foundation lemmas | S1 | the mathematics writer | the independent referee; the prose writer and integrator fidelity read |
| S3 | Proposition 2 share, decisive advantage, A.7 | S2 | the mathematics writer | the independent referee |
| S4 | Coexistence (A4) and Proposition 3 | S2 | the mathematics writer | the independent referee; the prose writer and integrator fidelity read |
| S5 | Research (A5) and Proposition 4 | S2; S3 lemma statement | the mathematics writer | the independent referee; the prose writer and integrator fidelity read |
| S6 | Empirical results (A8) | S2 | the mathematics writer | the independent referee |
| S7 | Benchmark numbers: keys, exercises, independent recomputations | S4–S6 statements | the mathematics writer (P3 extension), the production assistant (P1, P5 rows) | the independent reader recomputes (XP1, XP3, XP5) |
| S8 | Appendix integration and removal of process text | S2–S7 | the prose writer and integrator | the production assistant (labels), the independent referee (transcription read of changed statements) |
| S9 | Main text | S8 | the prose writer and integrator (prose) | the independent referee (statements match the appendix) |
| S10 | Figures | S5, S7 | the production assistant | the prose writer and integrator |
| S11 | Consumers: `comparison.tex`, `slides.tex` | S9, S10 | the production assistant | the prose writer and integrator |
| S12 | Verification and final language sweep | all | the prose writer and integrator | coordinator |
| S13 | Second opinion, fixes, local commits, report | S12 | the second reader (read), the prose writer and integrator (fixes) | coordinator |

S3, S4 and S6 run in parallel after S2. S5 needs only the statement of the decisive-advantage lemma from S3 to start. S7 starts as soon as each package lists its keys.

the mathematics writer packages are standalone LaTeX articles that compile and use the manuscript's macros (`\DT`, `\Ent`, `\Own`, `\lb`, `\reg`), one file per appendix subsection, for example under `audit/theory_upgrade_2026_10_25/theorems/` with referee reports beside them. Integration is then a transplant. The mathematics writer and the independent referee work in separate work periods; the independent referee never reviews text it wrote.

### S0. Decisions and setup

- **Goal.** Settle the decision points of Part 6, the numbering policy (decision D9) and the mirror policy before anyone writes.
- **Files.** `sections/02_model.tex:1` (remove `ty` once Austin agrees). Nothing else.
- **Steps.** Pull Austin's latest Overleaf edits into `overleaf/slot/` first; note the new base commit and diff it against 69c25f4, since every line reference in this plan must be re-anchored if Austin edited the same files. Create a local branch (for example `theory-upgrade`) in `overleaf/slot/` and in the parent repository. Leave Austin's uncommitted parent-repository changes (handout/, docs/, presentation/, slot/study_guide/) unstaged.
- **Verification.** `git status` and `git log -1` in both repositories; diff of the pulled commit.
- **Acceptance.** Every decision in Part 6 answered or set to its recommendation; numbering policy D9 adopted; base commit recorded in the stage report.
- **Size.** One deleted token.

### S1. Notation freeze and rule card

- **Goal.** One symbol per object before any the mathematics writer writing; a rule card that every brief carries.
- **Files.** An audit note (for example `audit/theory_upgrade_2026_10_25/NOTATION.md`). No manuscript edits.
- **Content.** The symbol table of Part 3.6; SCAN Part 3 patterns 1 to 8; the rule card of Appendix A.
- **Source.** SCAN Part 3; the symbols of W1A–W5A; LA1–LA6.
- **Writer/checker.** the prose writer and integrator drafts; the independent referee confirms the mathematical symbols; the production assistant greps each chosen symbol in `sections/`, `appendix/`, `comparison.tex`, `slides.tex` for a second meaning.
- **Acceptance.** No chosen symbol has two meanings in the master or in the planned text; the collisions in Part 3.6 are resolved; the rule card covers LA1–LA6 and gives two compliant example sentences per rule.
- **Size.** About 80 lines of notes.

### S2. Foundation lemmas (A2)

- **Goal.** State and prove the reduction lemma and the two-numbers-along-a-path lemma; repair the CM shortcut and the scope sentence; remove the script convention.
- **Files and labels.** `appendix/A2_beliefs_trading.tex`: 7–8 (scope), 26–27 (script convention, delete), 165–170 (constructed tuples), 232–236 (β scope list). New `lem:reduction` (Lemma A.4) and `lem:twonumbers` (Lemma A.5) after `lem:trading`.
- **Sources.**
  - Lemma A.4: RED §2 (statement, the reduced system, the converse construction with w_L ≥ 0 and full liquidity support, the CM remark); SCAN Part 2.
  - Lemma A.5: RED §3(a) (Δ↑, g_j↓, γ↓, Δ + γ fixed, τ↑ and Δτ↑ when γ > 0 and c_H ≥ g_L; strictness needs a positive integral); W1A §Solver B 1, second correction (τ can fall when τ < 0); RED §3(a) shifted-uniform example (J falls).
  - CM repair: RED §4.1 (equal posteriors and equal entry give equal prices; the U[0, 2], c_H = 73/16 counterexample).
  - Scope sentence: SCAN headline 8 (GEN).
- **Writer/checker.** the mathematics writer writes; the independent referee referees; the prose writer and integrator reads each statement against the RED equation it cites.
- **Verification.** the independent referee's verdict per statement with proofs; a print-only consumer script recomputes the RED §4.1 equilibrium (prices 15/16 and 33/64, returns 1/8 and 1/32).
- **Acceptance.**
  1. Lemma A.4 states the projection of the equilibrium set onto (σ_H, σ_L, μ, e), and with research, for fixed a and λ̄, onto (λ̂, σ_H, σ_L, μ, e); prices follow from P = t_0 + e(w_L + Δμ). It holds at every prior and for each pair of tie rules.
  2. Lemma A.5 states the monotonicity facts and their strictness conditions, and that the fixed sum Δ + γ is the class mean gap. The fact that J carries no sign along a path enters as one positive sentence with the example, inside the proof or after it, not as a closing paragraph.
  3. The constructed-tuple paragraph says equal posteriors with equal entry give equal prices.
  4. The opening says the belief lemma holds for every profile and the price and trading lemmas for every tuple that meets their stated conditions.
  5. LA1–LA6.
- **Size.** +70 lines, −10.

### S3. Proposition 2 additions, decisive advantage, and A.7

- **Goal.** Add class H's share of challenger takeovers under outbidding to Proposition 2(ii); add a decisive-advantage lemma; extend Proposition A.7 to ranked classes and a continuous stochastically ordered pair.
- **Files and labels.** `sections/04_equilibrium_results.tex:35–39` (part (ii)) and 63–67; `appendix/A3_proposition2.tex:75–86` (Step 4), new `lem:decisive` (Lemma A.6) after the proof at A3:110; `prop:region` title at A3:157; `appendix/A6_robustness.tex:395` (point-mass standing sentence), 433–442 (statement), 481–489 (ownership line, "since h > r_1" at 489).
- **Sources.**
  - Share: W2A §Shared Candidate 3 (takeover odds (e_H/e_L)(W_H/W_L); nonincreasing W_L/W_H suffices; strict growth needs a positive low-class win probability); WA W2.7.
  - Ownership condition and its sufficient form: W2A §"Proposition 2" (Proposition 2's condition is exact; its no-trade floor is not an equilibrium of Proposition 2's game, so the same-incumbent ratio does not transfer).
  - Decisive advantage: W2A §Shared Candidate 2, "Decisive advantage" and "Benchmark verification" (g_H(F) > c_H ⇒ W_H(F) = 1; for point classes and the whole uniform family it holds exactly when c_H ≥ (h² − p²)/(2h); recruitment needs r < 4 + √63/2); the two-part incumbent of the same section (the condition is a property of the incumbent family).
  - A.7: GEN table row "Complementary signals"; W2A §"Proposition A.7" (ownership ½ e_H W_H(F_1)).
- **Writer/checker.** the mathematics writer; the independent referee.
- **Verification.** the independent referee's verdicts; print-only recomputation of the benchmark share at r_0 and r_1 (if printed) and of 399/80 and 81/80.
- **Acceptance.**
  1. Proposition 2(ii) adds: if class H outbids both incumbents, ownership rises and class H's share of challenger takeovers rises, strictly when a low-class challenger beats F_0 with positive probability. the independent referee confirms the strictness condition (obligation O6).
  2. Lemma A.6 is stated for an incumbent family, with the point-class and uniform-family equivalence and the benchmark margin.
  3. A.7's hypotheses read in B_{F_i}, Δ_T(F_i) and D⁺ at F_0; the benchmark example keeps its numbers.
  4. LA1–LA6.
- **Size.** +45 lines.

### S4. Coexistence (A4) and the statement of Proposition 3

- **Goal.** General results first, the benchmark path second; hand proofs replace both polynomial root counts.
- **Files and labels.** `appendix/A4_coexistence.tex` throughout (map in Part 3.2); draft of the formal statement for `sections/04_equilibrium_results.tex:272–283`.
- **Sources.**
  - Region, uniqueness under C1, entry formula, convexity, necessary prior ceiling: W1A §Shared Candidate 1, eqs (1)–(2); WA W1.1.
  - Sure-purchase interval and the location of gaps: W1A §Solver B 1, eq (3) and its wording corrections; WA W1.2.
  - Uniform-incumbent interval: W1A §Solver A 2 and Solver C 3, eqs (4)–(8); weaker bound (9) optional; endpoint conditions at prior 1/2 ("Recovering the endpoint formula"); WA W1.3.
  - Balance conditions: W1A §Solver B 2, eqs (10)–(12), "On the CM threshold branch" (entry on T weakly falls); WA W1.4.
  - Existence at prior 1/2 for every F with Δ > 0, γ > 0, τ > 1/2, including τ ≥ 1: RED §3(d). This is not in W1–W5; the independent referee re-referees it here (obligation O5).
  - Pointwise lemmas at a fixed F: RED §1 table rows "High-class lemma", "Low-class lemma", "Product lemma" (τ < 1 for s*; the τ ≥ 1 case).
  - Corollary A.2 conditions: RED §3(e).
  - Two-interval path: W1A §"Solver A's example", eq (20).
  - Figure-note repair (T at r_A under C1): W1A §"Consolidated benchmark numerical check", last paragraph; RED §4.2.
- **Writer/checker.** the mathematics writer; the independent referee; the prose writer and integrator fidelity read.
- **Verification.** the independent referee's verdicts; print-only recomputation of 2/5, 9667/8280, 937/5520, J(r_0), τ(r_0), τ(r_2) and the two-interval endpoints; LaTeX build of the package.
- **Acceptance.**
  1. The full statement of Proposition 3 contains (a) the region with uniqueness under C1 and entry ρ + (1 − ρ) min{(1 − π)bΔ/k, b + πλ}; (b) the sure-purchase interval with gaps only at Δ < k/(1 − M(π)); (c) the uniform-incumbent interval at every prior and the balance condition for general families, with the squared form for the threshold branch; (d) existence at prior 1/2 under IM, with either challenger rule (a CM tie admits the C1 choice).
  2. The benchmark path lemma proves (b) from (c) with margin 2/5 and proves (c) on the whole path [r_0, r_2] with margin 937/5520; no root count remains.
  3. The benchmark equilibrium table, the threshold order and Corollary A.2 keep their content; Corollary A.2's set formula cites the region theorem.
  4. The tie-rule paragraph states for general F: under CM the threshold pair adds informative equilibria inside the region and the point τ = π joins it; under I0 coexistence needs k/(1 − M(π)) < Δ.
  5. Every statement carries its prior and tie-rule scope as in Part 3.1.
  6. LA1–LA6.
- **Size.** A4 from 598 to about 720 lines.

### S5. Research (A5) and the statement of Proposition 4

- **Goal.** General research results at prior 1/2 first, the benchmark path second; the recruiting equilibrium continues through the low class's selling; three outcomes characterized.
- **Files and labels.** `appendix/A5_research.tex` throughout (map in Part 3.2); draft of the formal statement for `sections/05_research.tex:52–71`. New `lem:a5-sale`, `lem:a5-outcomes`, `tab:a5-set`; `lem:a5-middle` retired.
- **Sources.**
  - Positive research forces a strict full purchase, for every β < 1/2: W3A §1.
  - The low class's sale rate, sale posterior b/(2b + λz), and max U_L = (ρΔm_λ − k)⁺: W3A §2, eqs (1)–(3); WA W3.1.
  - Research equation 2aλ = Δm_λ − k + (ρΔm_λ − k)⁺, unique root, existence condition Δ > 2k and 1/2 < τ ≤ M at the capped root (necessary and sufficient): W3A §3, eqs (4)–(5); WA W3.2–W3.3.
  - Prices, pooled sale and zero-order prices, E1–E7: W3A §4, eq (6).
  - Slopes, the switch λ_S = (1 − ρ)k/(2aρ), the upward kink, the cap spread, entry: W3A §5, eqs (7)–(10); WA W3.4.
  - What ends the branch, the exact margin φ_a*, the capped segment: W3A §6; path derivative and cheap research: W3A §Shared Candidate 2, eq (12); WA W3.7.
  - Entry, class entry, improving pool, fixed-value acquisition kernel (almost every value; atoms; counterfactual outside the support): W2A §Shared Candidate 1; WA W2.2–W2.3.
  - Same-incumbent ratio e_H/ρ (one sentence): W2A §"The comparison equilibrium"; WA W2.4.
  - Ownership level, exact trade-off, outbidding, decisive advantage: W2A §Shared Candidate 2; WA W2.5.
  - Three outcomes, coexistence band (14), exhaustion under IM/C1: W3A §Candidate 3, eqs (13)–(14); WA W3.5.
  - CM interior threshold tuple (15), cap family (16), I0 filter (17), the benchmark I0 gap and the I0/CM threshold equilibrium at r = 2: W3A §CM and §I0.
  - Benchmark strengths and the outcome list: W3A §"The benchmark" (table and IM/C1 list); WA W3.6.
  - Access to prices with research, general formulas: RED §3(f), last display.
- **Writer/checker.** the mathematics writer; the independent referee; the prose writer and integrator fidelity read.
- **Verification.** the independent referee's verdicts; print-only recomputation of r_R, r_λ̄, r_N, r_S, r_Q, r_U, r_C, the research and entry values at the six strengths, φ_a at r_0 and at the cap, and the I0/CM tuple at r = 2 against W3A's tables.
- **Acceptance.**
  1. The full statement of Proposition 4 holds for every auction with Δ > 0 and γ > 0 at prior 1/2 under IM, with C1 or the full-preparation selection under CM, and contains: (a) existence and the research schedule; (b) monotonicity in the spread of research, entry and class-H entry, the fall of class-L entry, the first-order improvement of prepared values, the acquisition kernel at a fixed incumbent value wherever class H can win; (c) ownership rising under outbidding (weakly, strictly below the cap where the spread rises strictly), with the exact trade-off and the decisive-advantage route; (d) the path statement.
  2. The four obligations O1, O3, O4 and O8 of Part 3.4 are discharged in the text.
  3. `lem:a5-middle` is gone and every reference to it (A5:241, 246, 250, 262, 278, 302, 313, 343, 348, 400; 427 and 439 sit in the deleted certificates paragraph) points to its successor.
  4. The benchmark list matches W3A: Z alone below r_R; Z and recruiting from r_R through r_N; capped recruiting and floor-entry research on (r_N, r_Q); capped recruiting alone on [r_Q, r_C]; research at the cap with entry ρ above r_C.
  5. Proposition A.2 keeps its content and refers to the benchmark list.
  6. LA1–LA6.
- **Size.** A5 from 439 to about 560 lines.

### S6. Empirical results (A8)

- **Goal.** Restate A.11 to A.14 and Corollary A.3 at the generality the referee reports prove, with the benchmark as the worked example.
- **Files and labels.** `appendix/A8_empirical.tex` throughout; labels unchanged.
- **Sources.**
  - Weighted test, sign table, identity with the zero-order discount, the general-pattern formula: W5A §Shared candidate 1, eqs (1)–(6); WA W5.1.
  - Unweighted test and its sufficient condition π ≥ 1/2, ρ ≤ 1/2 under C1: W5A §"Primitive rescue", eqs (15)–(16); WA W5.2.
  - Identification: W5A §Shared candidate 2, eqs (8)–(12), the variance formula, purchases-only eqs (13)–(14); WA W5.3.
  - Entry component: W5A §"Entry-component trend", eqs (17)–(19), §"Ceiling jumps"; WA W5.4.
  - Announcements: W5A §"Announcement returns", eqs (21)–(22); WA W5.5.
  - Winners: W4A §"Solver C 1, Solver B 3, and Solver E 1(a)–(b)" (sign), §"the covariance constants agree" (every prior), §"Solver E 1(c)–(d)" (two channels, second difference at prior 1/2), §"High-class outbidding" (trend), §"Exact uniform-family condition"; WA W4.1–W4.3.
  - Manuscript errors: WA W5 "manuscript points" (ϑ = M − m only at prior 1/2; A.14(iii) and (iv) proofs use the even prior).
- **Writer/checker.** the mathematics writer; the independent referee.
- **Verification.** the independent referee's verdicts; print-only recomputation of the purchases-only counterexample (π = 0.3, r = 2), the weighted statistic at the benchmark (equal to −pdrop_neutral_r1_B), D − Ω at r_1 and r_2, ℓ² − 3p².
- **Acceptance.**
  1. A.11 states the weighted test at every prior below the threshold under full two-sided trade in one public state, the C1 sign table, the identity T = P̄ − P(0), the unweighted test as a part with its sufficient condition, the entry-component split, and the benchmark trends and jump.
  2. A.12 states identification at a known prior other than one half, the prior-1/2 count fact with the benchmark interval, and the sale-price inversion when entry after a sale and after no order sits at ρ and ρΔ is known.
  3. A.13 states the sign under two-sided trade at every prior, the post-ceiling covariance at every prior, the two-channel covariance and second difference at prior 1/2, and the trend with the prior and slot fixed under outbidding.
  4. A.14(iii) states the exact condition; the zero-order discount appears once, in A.11, and A.14 refers to it.
  5. The informed share is λ/v at every prior; no identity valid only at prior 1/2 appears without that scope.
  6. LA1–LA6.
- **Size.** A8 from 259 to about 340 lines.

### S7. Benchmark numbers

The numbers lens owns the mechanics; theory supplies the key list (Part 3.5) and the facts each key carries.

- **Writers.** the mathematics writer extends the research exercise (continuation through selling, floor-entry root, r_Q, φ_a at the cap, the I0/CM tuple). the production assistant adds the closed-form rational keys of P1 and P5. The independent recomputation of each extension is written by the independent reader.
- **Verification.** `make_numbers.py` (no display conflicts), `number_scan.py` (zero missing keys, no typed decimals), the affected exercises and their independent recomputations, the numerical verification procedure skill for P1, P3, P5.
- **Acceptance.** Every `\reg` key in the theory packages exists; each value agrees with the referee report's number to the displayed precision; each independent recomputation agrees.

### S8. Appendix integration and removal of process text

- **Goal.** Transplant S2–S6 into the master and leave no trace of production in the appendix.
- **Files.** `appendix/A1`–`A9` (Part 3.2 lists every passage); A9 margins table.
- **Writer/checker.** the prose writer and integrator integrates; the production assistant checks labels and references; the independent referee reads every changed statement against its package for transcription errors.
- **Verification.** `latexmk` build of `main.tex`; zero undefined references, zero multiply defined labels; every changed page read in the PDF; Appendix B sweep on `appendix/`.
- **Acceptance.** Labels and numbers as in Part 4; no `\nolinkurl`, script, run log, registry, certificate, Sturm, "calibration B", "S(B)" or "Value at B" anywhere in the appendix; the margins table has no source column and carries the rows of Part 3.5; LA1–LA6.
- **Size.** Net about −60 lines of process text against +450 lines of mathematics from S2–S6.

### S9. Main text

- **Goal.** Statements of Propositions 2 to 4 that follow from the appendix full statements; prose to Austin's lineup.
- **Files.** `sections/02`–`08`, then `01`, `09` and the abstract in `main.tex:84–98`. The main-text lens owns the prose; theory requires the items in Part 3.2 "main text".
- **Writer/checker.** the prose writer and integrator composes; the independent referee checks each proposition against its full statement (hypotheses, prior, tie rule, trading pattern, condition).
- **Acceptance.** Each main-text proposition is implied by its full statement; no sentence claims more than its result's row in Part 3.1; wording targets of Part 3.7 or equivalents; LA1–LA6.

### S10. Figures

- **Goal.** Research figure with the three outcomes and no broken axis; optional region panel; corrected coexistence note.
- **Theory input.** Λ(Δ) and its cap; the floor-entry root Λ_ρ(Δ) from aQ = ρΔm_Q − k; r_Q; the plateau at the cap from r_λ̄ to r_C; region boundaries τ = π, τ = M(π), Δ = k/(1 − τ), Δ = k/(ρ max{π, 1 − π}); the path (Δ(r), τ(r)).
- **Writer/checker.** the production assistant edits `scripts/F_figures/make_figures.py`; the prose writer and integrator checks curves against the S7 keys.
- **Acceptance.** Curves match the keys at r_R, r_λ̄, r_N, r_Q, r_C; notes follow Part 3.7; LA1–LA6.

### S11. Consumers

- **Goal.** `comparison.tex` and `slides.tex` carry the upgraded results with valid numbers and no status or process language.
- **Theory input.** Part 4 consumer list; the `comparison.tex` scope decision (D19).
- **Writer/checker.** the production assistant; the prose writer and integrator.
- **Acceptance.** Every cited number and claim matches Part 3.1; Table A.4 and Table A.6 citations moved (Part 4); Appendix B sweep clean on both files; XeLaTeX build of the slides and pdfLaTeX build of the comparison.

### S12. Verification and final language sweep

- Build `main.tex`, `slides.tex`, `comparison.tex`; read every changed page.
- `number_scan.py`: zero missing keys, no typed decimals; orphan list reviewed (Part 3.5).
- Appendix B sweep over the main text, appendix, captions, table notes, `comparison.tex` and `slides.tex`, with every hit fixed or justified.
- An anti-defensive pass and a humanizing pass over all prose written in S2–S11.
- the numerical verification procedure for the affected exercises.
- **Acceptance.** All of the above clean; a one-page stage report lists every justified hit.

### S13. Second opinion and close

- the second reader reads the upgraded appendix and main text against `WORKAROUNDS.md` and Part 3.1 (scope drift, missing hypotheses, language).
- the prose writer and integrator fixes; the independent referee re-referees any changed mathematical statement.
- Local commits on both branches with informative subjects; no push to Overleaf or GitHub; a report to Austin.

---

## 3. File-by-file change list (theory lens)

### 3.1 Result-by-result scope table

"Any prior" means any interior prior. "Ranked" means classes under the class ranking. The tie-rule column gives the rules under which the statement as written holds.

**Main text**

| Result | After the upgrade | Incumbent and classes | Prior | Tie rules | Trading pattern | Named condition | Source | Change | Write / check |
|---|---|---|---|---|---|---|---|---|---|
| Prop 1 `prop:returns` | as now | continuous F; finite means; (b) ranked | none | none | none | none | SCAN Part 1 | unchanged | none |
| Prop 2 `prop:ccc` | as now; (ii) adds takeover share under outbidding | ranked; continuous ordered triple | any | all four pairs | forced by (H2) | (H1)–(H3); outbidding for the share | W2A §Shared C3, §Prop 2 | part added | mathematics writer / independent referee |
| Prop 3 `prop:coexistence`, "Quiet and informative markets" | (a) region, unique informative equilibrium, entry a function of Δ; (b) sure-purchase stretch an interval; (c) one interval of strengths | (a)(b) ranked, any continuous F; (c) uniform incumbent, separated classes | any | IM, C1 | no trade against purchases only | (c) uniform incumbent with separated classes and affordability | W1A eqs (1)–(8) | restated, general | mathematics writer / independent referee |
| Prop 4 `prop:research` | (a) existence and research schedule; (b) monotone in Δ through selling; (c) ownership under outbidding; (d) one interval along a path | ranked, Δ > 0, γ > 0 | 1/2 | IM; C1, or CM with full preparation | class H buys; class L abstains, mixes, then sells | (c) outbidding; (d) cheap research with end signs | W3A eqs (1)–(12); W2A §C1–C2 | restated, general | mathematics writer / independent referee |

**Appendix**

| Result | After the upgrade | Incumbent and classes | Prior | Tie rules | Trading pattern | Named condition | Source | Change |
|---|---|---|---|---|---|---|---|---|
| Def A.1 `def:equilibrium` | as now | general | any | stated | any | none | none | unchanged |
| Prop 1(c) (named) | as now | general | none | none | none | none | none | unchanged |
| Lemma A.1 `lem:beliefs` | as now | none | any | none | any profile | β ≤ 1/3 for (c) | none | unchanged |
| Cor A.1 `cor:exclusion` | as now | g_H ≥ g_L | any | both challenger rules | any profile | β ≤ 1/3 | none | unchanged |
| Lemma A.2 `lem:prices` | as now; constructed-tuple paragraph repaired | Δ > 0, γ > 0 | any | C1 at μ = τ; CM clause | any tuple | none | RED §4.1 | repaired |
| Lemma A.3 `lem:trading` | as now | Δ ≥ 0 | any | IM and I0 in (b) | any tuple | none | none | unchanged |
| Lemma A.4 `lem:reduction` | equilibrium projection depends on the auction only through (Δ, τ) | Δ > 0, γ > 0 | any | each pair | any | with research: a, λ̄ fixed | RED §2; SCAN Part 2 | new |
| Lemma A.5 `lem:twonumbers` | a stronger incumbent raises Δ and, where τ ≥ 0, τ and Δτ; Δ + γ fixed | ranked; ordered family | none | none | none | γ > 0, c_H ≥ g_L for τ | RED §3(a); W1A §Solver B 1 | new |
| Prop 2 proof (A3) | Step 4 adds the share | as Prop 2 | any | all | full orders | outbidding | W2A §C3 | part added |
| Lemma A.6 `lem:decisive` | decisive advantage ⇒ W_H = 1 at every recruiting economy; point classes and uniform family: c_H ≥ (h² − p²)/(2h) | a family of laws | any | none | any recruiting economy | decisive advantage | W2A §C2 | new |
| Prop A.1 `prop:region` | as now, retitled | benchmark | 1/2, or 1 + u = e | C1 at the boundary | forced | none | none | retitled |
| Lemma A.7 `lem:a4-high` | pairs (N, Q, R, T, F) at a fixed F; s* for τ < 1; τ ≥ 1 case | Δ > 0, γ > 0, π < τ | any | as stated per form | no wrong-signed order | none | RED §1 table | restated at fixed F |
| Lemma A.8 `lem:a4-low` | as now at a fixed F | π < τ | any | IM; I0 gap | no wrong-signed order | none | RED §1 table | restated |
| Lemma A.9 `lem:a4-product` | as now at a fixed F | π < τ, s ≥ t | any | as stated | rates s ≥ t | none | RED §1 table | restated |
| Prop 3 full statement (named) | (a) region, uniqueness, entry, convexity, prior ceiling; (b) sure-purchase interval; (c) uniform interval, balance, squared balance; (d) existence | (a)(b)(d) any continuous F; (c) uniform family or balance on a path | (a)–(c) any; (d) 1/2 | (a)–(c) IM, C1, with CM and I0 in the tie paragraph; (d) IM with either challenger rule | as Prop 3 | (c) as Prop 3 | W1A; RED §3(d) | new full statement |
| Two-interval path (paragraph) | a two-part incumbent path keeps every benchmark primitive and has coexistence on two disjoint intervals | two-part mixture | 1/2 | IM, C1 | as Prop 3 | none | W1A eq (20) | new paragraph |
| Lemma A.10 `lem:a4-path`, "The benchmark path" | (a) τ↑; (b) J↑ by Prop 3(c); (c) Δ(1 − τ)²↑ on [r_0, r_2]; (d) Δτ↑ | benchmark | none | none | none | margins 2/5 and 937/5520 | W1A eqs (8), (12) | hand proofs |
| Lemma A.11 `lem:a4-order` | as now | benchmark, slot band | 1/2 | none | none | band | none | unchanged |
| Benchmark path at prior 1/2 (named) | the present full table, entry formulas, existence | benchmark | 1/2 | IM, C1; CM and I0 rows in Table A.3 | all forms | slot band | A4:288–397 | moved from "full statement" |
| Cor A.2 `prop:priors` | as now; set formula from Prop 3(a) | benchmark path | any | IM, C1; CM point | as Prop 3 | none | RED §3(e) | proof shortened |
| Lemma A.12 `lem:a5-joint` | V = π max U_H + (1 − π) max U_L | general | any | none | any | none | SCAN Part 1 | stated at any prior |
| Lemma A.13 `lem:a5-bounds` | as now | general | 1/2 | none | any profile | β ≤ 1/3 for the zero order | none | unchanged |
| Lemma A.14 `lem:a5-buy` | as now for β < 1/2 | general, τ > 1/2 | 1/2 | both | positive research | none | W3A §1 | scope widened |
| Lemma A.15 `lem:a5-sale` | low-class sale rate, sale posterior, max U_L | general | 1/2 | IM; I0 filter | full purchase by H | none | W3A §2 | new |
| Prop 4 full statement (named) | (a)–(d) as in S5 | general | 1/2 | IM; C1 or full-preparation CM | H buys; L by the sale lemma | (c) outbidding; (d) cheap research | W3A §§3–6; W2A §C1–C2 | new full statement |
| Lemma A.16 `lem:a5-outcomes` | zero research, recruiting research, floor-entry research exhaust the outcomes; coexistence band | general | 1/2 | IM, C1 | as listed | none | W3A §Candidate 3 | new; succeeds `lem:a5-middle` |
| Lemma A.17 `lem:a5-strong` | as now (condition U) | general | 1/2 | every pair | forced full orders | U | none | unchanged |
| Rem A.1 `rem:researchties` | CM threshold tuples (interior and cap family); I0 filter and the benchmark I0 gap | general, then benchmark | 1/2 | CM, I0 | as listed | none | W3A §CM, §I0 | restated |
| Benchmark research list (named) + Table A.4 `tab:a5-set` | outcome list on the path; the six strengths as instances | benchmark, a = 1/40 | 1/2 | IM, C1 | as listed | path condition holds | W3A §"The benchmark" | new; absorbs Prop 4(b) |
| Prop A.2 `prop:researchregion` | as now; refers to the benchmark list | benchmark | 1/2 | none | as listed | none | none | referent updated |
| Access with research (paragraph) | gains (1 − ρ)(b̄ + λ̄/2)[w_L + ΔM_λ̄] and [γ(M_λ̄ − τ) + pF(p)] | general under U | 1/2 | every pair | forced | U | RED §3(f) | stated generally |
| Prop A.3 `prop:control` | as now | general | any | C1 for the exact formula | fixed signal law | none | none | unchanged |
| Prop A.4 `prop:atomless` | as now | ranked, any F pair | any | every pair | forced | support windows | none | unchanged |
| Prop A.5 `prop:classes` | as now | uniform family; ranked | any | every pair | forced | none | GEN row 15 | unchanged |
| Prop A.6 `prop:manyclasses` | as now | general | any | either challenger rule | forced | separation | none | symbol rename only |
| Prop A.7 `prop:signals` | ranked classes, continuous pair F_0 ≤ F_1 | ranked | 1/2 | every pair (orders) | forced | as stated | GEN row 17; W2A §A.7 | extended |
| Prop A.8 `prop:access` | as now | Prop 2 at F_1 | any | every pair | full orders | none | none | unchanged |
| Prop A.9 `prop:payment` | as now (two values) | point classes, zero reserve | none | none | none | none | none | unchanged |
| Prop A.10 `prop:reserves` | as now | general reserve | any | every pair | forced | windows | none | unchanged |
| Prop A.11 `prop:spread` | weighted test, sign table, unweighted test, entry-component split, benchmark trends and jump | general; trends need the auction | any below τ for the test | C1 for the sign table | full two-sided, one public state | entry trend: fixed reserve-failure probability, or uniform with ℓ_0² > 3p² | W5A eqs (1)–(6), (15)–(19) | restated, general |
| Prop A.12 `prop:informedshare` | known-prior identification; prior-1/2 counts; sale-price inversion | general | known π ≠ 1/2; or floor entry with ρΔ known | IM for boundary shares | full two-sided | none | W5A eqs (8)–(12) | restated |
| Cor A.3 `cor:purchasesonly` | counts at any prior; mixed branch leaves λ open to observation | general | any | IM | purchases only | none | W5A eqs (13)–(14) | restated |
| Prop A.13 `prop:winner` | sign; covariance at every prior; two channels and second difference at 1/2; trend under outbidding | general | sign and covariance any; channels 1/2 | C1 for χ | full two-sided | trend: outbidding, prior and slot fixed | W4A | restated, general |
| Prop A.14 `prop:announcement` | (i)–(ii) as now; (iii) positive mean iff preparation uncertain; (iv) refers to A.11 | general | any | both challenger rules | any equilibrium | B_F(π) < c_H sufficient | W5A eqs (21)–(22) | restated |
| `lem:a5-middle` | retired | | | | | | | retired |

### 3.2 File by file, with line references

**main.tex**

- 54, 57: macro comments; rename `\fr` comment to "root of Δ_T(r) = Δ" if S1 renames the argument (the argument `d` collides with the class mean gap and the signal accuracy).
- 84–98 abstract (main-text lens): 92–93 "challenger from the high-value class" → class H; 93–95 coexistence and 95–96 research sentences must match Props 3 and 4 as stated (general region; research and entry rise with the spread).
- 121–144 counters: no change; the numbering policy keeps proposition, corollary, remark and definition numbers fixed.

**sections/02_model.tex**

- 1: delete `ty`.
- 52–55: "In the main case R is uniform on [0, r]" → the benchmark sentence ("In the benchmark, R is uniform on [0, r] …").
- 62: delete "or high-value class".
- 123–125: footnote on β. Replace the list by the β scope each result actually needs (obligation O2): from the referee reports, Propositions 2 and 3 and the recruiting research equilibrium hold for every β < 1/2; the zero-order bound enters through Corollary A.1, Lemma A.13(a) and condition U.
- 216–218: the default tie sentence stays; Proposition 4 names IM in its statement because I0 removes the continuation.
- 225–228: define W_j(F) for both classes (A.13 and the ownership factorization use W_L).

**sections/03_competition_information.tex**

- 72–78: name the profit gap γ = g_H − g_L and the fixed class mean gap (Lemma A.5 and Prop 3(c) use both).
- 80–82: "approaches zero as r approaches ℓ" → benchmark sentence.
- 94: "the ceiling of the model" → "the posterior bound on preparation" (SCAN Part 3).
- After 107 (or at the end of 3.3): the two-numbers paragraph, wording target T1.

**sections/04_equilibrium_results.tex**

- 35–39 and 63–67: add the takeover share under outbidding (S3).
- 155–160: "a high-class challenger outbids every incumbent on the path" becomes the check of the outbidding condition in the benchmark, with the margin key.
- 254–270: lead-in to Proposition 3 (main-text lens), wording target T2's lead-in.
- 272–283: Proposition 3 statement (target T2).
- 285–290: benchmark numbers stay, as the worked example of the region.
- 297–308: figure note; 302–303 must say T at r_A is an equilibrium under the default rules (target T5).
- 311–333: prose; 326–332 "Coexistence also holds away from the even prior" becomes a direct reading of the region at every prior, with Corollary A.2 for the benchmark cases.

**sections/05_research.tex**

- 22: "throughout this section the prior is 1/2" stays; add the investor rule.
- 29–34: λ_E as a function of τ.
- 36–42: research condition display; theory recommends the full equation 2aλ = Δ_T m_λ − k + (ρΔ_T m_λ − k)⁺ with one sentence on the second term.
- 44–46: "research, entry and high-class ownership then rise together with incumbent strength" must carry the outbidding condition for ownership.
- 52–71: Proposition 4 (target T3). Part (b) of the present statement leaves the proposition; its content goes to the text and to Table 4.
- 73–81: intuition paragraphs rewritten for the general statement.
- 83–106: Table 4 stays (the six-strength worked example).
- 108–126: benchmark prose rewritten (target T4): [r_R, r_C] with the cap at r_λ̄.
- 128–130: r_U stays as the strength above which the full tuple is unique under every tie rule; uniqueness under the defaults starts at r_Q.
- 132–146: figure note (target T6); no broken axis.
- 148–152: comparison with the fixed-presence branch stays.
- 154–160: Prop A.2 paragraph; "admissible region" → "parameter region".

**sections/06_robustness.tex**

- 56–81: A.7 holds for ranked classes and a continuous pair; the benchmark example keeps point masses.
- 61: a_T and d symbols (optional rename, S1).

**sections/08_empirical.tex**

- 3–9: standing paragraph: the results hold for a general incumbent at every prior under full two-sided trade in one public state, with the benchmark as the worked example; "u/(2 + u)" is the informed share at prior 1/2, λ/v in general.
- 19–26: the weighted test replaces the unweighted statement; the sentence "this test needs no knowledge of the auction objects" holds for the weighted test at every prior; "ρΔ_T times the informed share" and "half of the class component" are prior-1/2 statements and go.
- 33–42: identification (known prior; sale price).
- 44–50: winners: the sign holds whenever the incumbent's value sometimes falls where the two classes differ in their chance of beating it; the widening holds under outbidding; the benchmark sentence at 49–50 is the benchmark's outbidding check.
- 52–57: announcements: exact condition.

**sections/01_introduction.tex, 09_conclusion.tex** (main-text lens): 61 and 9:10–15 interval sentences follow Prop 3 (region in general, one interval under the uniform condition); 69–75 and 9:14–15 research sentences follow Prop 4; 93–98 and 9:25–26 the test is the weighted one.

**appendix/A1_payoffs.tex**

- 1–3: keep; "A statement that needs the point-mass benchmark says so" stays.
- No mathematical change. The path lemma goes to A2 so that Lemmas A.1–A.3 keep their numbers.

**appendix/A2_beliefs_trading.tex**

- 7–8: scope sentence (S2 acceptance 4).
- 26–27: delete the script convention.
- 165–170: equal posteriors and equal entry give equal prices.
- After 230: insert Lemma A.4 `lem:reduction` and Lemma A.5 `lem:twonumbers` with proofs.
- 232–236: β paragraph lists the results that hold for every β < 1/2 after the upgrade (O2).

**appendix/A3_proposition2.tex**

- 3–4: "the admissible region" → "the parameter region at the benchmark".
- 75–86: Step 4 adds the share under outbidding.
- After 110: Lemma A.6 `lem:decisive` with proof and the benchmark margin.
- 124: "Keep calibration B" → "Keep the benchmark".
- 134–147: keep the tuples and prices; delete 139–147 (scripts, interval arithmetic, rational endpoints as a record).
- 155, 226: "calibration B" → "the benchmark".
- 157: title "The parameter region at the benchmark".
- 229–231: delete the script reference.

**appendix/A4_coexistence.tex**

- 1–8: opening: general first, benchmark second (target T7).
- New first part (before 10): Lemmas A.7–A.9 (present 159–256, restated at a fixed F; "Fix r" → "Fix F"; 149–157 "On the path τ(r) < 3/4" → the τ < 1 condition for s* and the τ ≥ 1 case), the full statement of Proposition 3 with proof, the two-interval path paragraph, the general tie-rule sentences.
- 10–63: present path lemma becomes Lemma A.10 in the benchmark part; (b) proved from Prop 3(c); (c) on [r_0, r_2] from the squared balance inequality; delete 41–62 (root counts, scripts, "Parts (b) and (c) rest on …").
- 65–83: thresholds stay; uniqueness of r_A and r_J follows from the hand proofs.
- 85–105: order lemma (A.11) unchanged in substance.
- 107–112: delete (scripts and bisection record).
- 114–130: Table A.1; caption and column: "at the benchmark", "Benchmark value".
- 258–286: forms at prior 1/2 stay in the benchmark part.
- 288–314: the present full statement becomes the named benchmark result.
- 316–397: proof stays; Step 7 (378–391) uses (c) on the whole path, so the sentence on r_J < 2 and its key go.
- 399–410: keep the entry values; delete the scripts and the enumeration cross-check (405–410).
- 412–429: Table A.2 caption without "calibration B".
- 431–531: Corollary A.2; the proof's Step 1 cites Prop 3(a); cases (a)–(d) keep their argument with J increasing from Lemma A.10(b); 529–530 delete the script reference.
- 533–598: tie paragraph and Table A.3: add the general statements (CM: T within the region and the τ = π point; I0: Δ > k/(1 − M(π))); keep the benchmark table.

**appendix/A5_research.tex**

- 1–4: opening (target T12).
- 22–33: standing assumptions: general auction with Δ > 0, γ > 0; prior 1/2; β ≤ 1/3 only where the zero-order bound enters.
- 35–62: derived functions; λ_E as a function of τ; 40–41 and 61 "calibration B" → benchmark sentences in the benchmark part; F_r(λ) renamed per S1 and kept as the benchmark form of the general research equation.
- 64–83: Lemma A.12 at any prior.
- 105–120: Lemma A.14 for β < 1/2.
- New after 120: Lemma A.15 `lem:a5-sale`; Proposition 4 full statement and proof; Lemma A.16 `lem:a5-outcomes`.
- 122–201: `lem:a5-middle` retired; its Z part goes to Lemma A.16, its R and R̄ parts to the full statement, its T part to Remark A.1.
- 203–231: Lemma A.17 (U) unchanged.
- 233–284: proofs of the present Prop 4(b) and (a): (a) is subsumed by the full statement; (b) becomes the proof of the benchmark list; 280–282 "W_H = 1 because h > r" becomes the benchmark check of outbidding.
- 286–314: replaced by the benchmark research list and Table A.4: [r_R, r_C] recruiting with the cap at r_λ̄; the present [r_R, r̄_R) claim leaves.
- 316–385: Prop A.2 unchanged in substance; "primitives of B" (317) and "calibration B" (339) → "the benchmark".
- 387–408: Remark A.1 rewritten generally (CM eqs (15)–(16), I0 eq (17)) with the benchmark numbers.
- 410–421: access with research: general formulas; p²/r_1 → pF(p).
- 423–439: delete the certificates paragraph.

**appendix/A6_robustness.tex**

- 38–66: keep the control in the slot; delete 60–66 (scripts).
- 72–77: optional rename of the cost-law letters H_C, H^0, H^1, L (SCAN Part 3, A6:73).
- 237, 360: "slot of B", "slot of calibration B" → "the benchmark slot".
- 248–257: replace the script paragraph by the mathematical statement (piecewise polynomial integrals of degree at most three; exact values give the margins).
- 351–357: the 16-vertex evaluation stated as mathematics; the separation distance γ renamed (S1).
- 395, 433–442, 481–489: A.7 extension (S3).
- 467, 491–504: "S(B)" → "the signal example"; 506: "The benchmark B" → "The benchmark".
- 557–560: delete script references.

**appendix/A7_welfare.tex**

- 79–81, 195, 241–243: delete script references; keep the mathematics.

**appendix/A8_empirical.tex**

- 3–12: standing paragraph general (S6); 8: ϑ = λ/v; M − m = ϑ only at prior 1/2.
- 14–43: full two-sided trade on (r_S, h) stays as the benchmark part.
- 45–83: A.11 restated (S6 acceptance 1).
- 85–142: A.12 restated; delete 141–142 script reference.
- 144–164: Cor A.3 restated.
- 166–193: A.13 restated.
- 195–237: A.14 restated; (iv) refers to A.11.
- 239–249: two clusters stay.
- 251–259: delete the certificates paragraph.

**appendix/A9_parameters.tex**

- 4, 10, 96: "calibration B" → "the benchmark".
- 39–46: delete the registry-key note; keep the sentence on Euler's number and on the cap.
- 49–58: "The vector S(B)" → "The signal example".
- 60–79: delete the script codes and the certification sentences; replace by one convention sentence (target T8).
- 86–158: margins table: delete the Source column; "Value at B" → "Benchmark value"; remove the rows "Q_J(r_0) > 0" (123) and "ρJ(2) > k (so r_J < 2)" (120); add the rows of Part 3.5.
- 192–199: "S(B)" and "B" cells → "signal example" and "benchmark".
- 251–270: open-parameter-set paragraph: add the research path condition and the new margins to the list of sections through the benchmark.

### 3.3 Benchmark facts that become hand proofs, and computational passages that leave

| Present passage | Present basis | After the upgrade | Source |
|---|---|---|---|
| A4 Lemma (b): J increasing on [r_0, r_2] (A4:41–48) | exact root count of a degree-6 polynomial | Prop 3(c): every incumbent value lies below h and h − r_2 − c_H = 2/5 > 0, so J′ ≥ AΔ²/γ² > 0 | W1A eq (8) |
| A4 Lemma (c): Δ(1 − τ)² increasing on [r_0, 2] (A4:50–58) | exact root count of a degree-10 polynomial | squared balance: X − 2ηΔ has minimum 937/5520 > 0 at r_2; holds on all of [r_0, r_2] | W1A eqs (11)–(12) |
| Q_J(r_0) > 0 (A4:48; A9:123) | registry value | not needed | none |
| ρJ(2) > k so r_J < 2 (A4:390; A9:120) | registry value | not needed once (c) holds on the whole path | none |
| r_A, r_J bracketed by exact bisection (A4:107–112) | script | unique roots by Lemma A.10(b); values printed as displays | none |
| A5 φ_a increasing on [r_0, 7/4] (A5:291–298) | exact rational derivative bounds | unchanged argument, stated as mathematics; supplies the cheap-research condition | W3A §Shared C2 |
| research roots at six strengths (A5:252–253) | bisection with exact signs | quadratic formula for the research root | none |
| r_U (A5:257) | closed form | unchanged | none |
| equilibrium enumeration at 241 strengths (A4:405–410) | script cross-check | deleted (not a proof step) | none |
| floating grid of research tuples (A5:436–439) | script cross-check | deleted (not a proof step) | none |
| four-class separation (A6:351–357) | script over 16 vertices | evaluation at the 16 vertices of the weight box, stated as mathematics | none |
| Table A.4 economies (A6:248–257) | script integrals | piecewise polynomial integrals, stated as mathematics | none |
| r_Q, end of floor-entry coexistence | none yet | obligation O1 | W3A §"The benchmark" (value only) |

### 3.4 Proof obligations that no referee report discharged

- **O1. Uniqueness of r_Q.** Both τ(r) and M at the floor-entry research level rise with strength, so one sign change of τ(r) − M_{λ_ρ*(Δ(r))} on (r_N, r_C) needs its own argument. W3A §"The benchmark" gives only the value 2.166995 and the outcome list; `W3_D.md` (Candidate 3, conditions) names this single crossing as an assumption; no report proves it. Suggested route: on the stretch where the floor-entry root is below the cap, compare the two derivatives with exact rational bounds on short subintervals (the technique of the present a_mono argument); beyond the point where the floor-entry root reaches the cap, M_λ̄ ≥ τ up to r_C. Writer: the mathematics writer (S5); referee the independent referee; key `res_rQ`.
- **O2. β scope of each result.** Confirm per result which statements hold for every β < 1/2 and which use the zero-order bound (β ≤ 1/3), for the footnote at 02:123–125 and the A2 paragraph at 232–236. Writer: the mathematics writer across S2–S6; referee the independent referee.
- **O3. Right end of the capped segment.** W3A §6: under merely nondecreasing τ the end is the last point of {τ ≤ M_λ̄}; the benchmark has strictly increasing τ, so the end is r_C, included under C1. The full statement must use the last-point form.
- **O4. Path condition on the exact margin.** The cheap-research hypothesis of Prop 4(d) must be stated on the exact uncapped margin φ_a* = J − k + (ρJ − k)⁺ − 2aλ_E(τ), or with ρJ ≤ k on the uncapped stretch, since the start can lie where a sure sale already pays (W3A §6; the a = 0.2 benchmark variant starts above r_N).
- **O5. Existence at prior 1/2 for every F.** Source RED §3(d), outside W1–W5. the independent referee re-referees it in S4.
- **O6. Strictness of the takeover share in Prop 2(ii).** Planner's derivation: under outbidding the odds ratio between F_1 and F_0 is (e_H/e_L)(W_L(F_0)/W_L(F_1)) when W_L(F_1) > 0, and the share is one at F_1 when W_L(F_1) = 0; so the share rises strictly exactly when W_L(F_0) > 0. the independent referee confirms.
- **O7. Pooled sale and zero-order prices.** During mixed selling the sale and the zero order can share a posterior (W3A §4, r = 1.9118); the tuple construction must check equal entry there, which the repaired Lemma A.2 paragraph requires.
- **O8. Zero research at ρΔ = 2k.** Under IM the hypothetical-success orders are not unique (W3A §Candidate 3, item 1); Lemma A.16 classifies outcomes, not tuples.

### 3.5 Registry keys the theory needs (names proposed; the numbers lens fixes them)

New rows:

| Proposed key | Value | Carries | Exercise / recomputation |
|---|---|---|---|
| `margin_afford_uniform_B` | 2/5 | h − r_2 − c_H, Prop 3(c) at the benchmark | P1 / XP1 |
| `margin_balance_sq_B` | 937/5520 | squared balance, Lemma A.10(c) | P1 / XP1 |
| `margin_balance_B` | 9667/8280 | plain balance (optional; implied by the squared form) | P1 / XP1 |
| `margin_outbid_path_B` | 32/5 | h − r_2: class H outbids every incumbent on the path | P1 / XP1 |
| `cH_floor_decisive_B` | 399/80 | (h² − p²)/(2h), lower end of the cost bracket | P2 or P4 / XP |
| `margin_decisive_B` | 81/80 | c_H − (h² − p²)/(2h) | same |
| `r_decisive_B` | 7.968627 | 4 + √63/2, no recruitment above it in the uniform family | same |
| `res_rQ` | 2.166995 | end of floor-entry coexistence; uniqueness under the defaults from here | P3 / XP3 |
| `res_phi_r0_B`, `res_phi_cap_B` | −0.022693, 0.017446 | end signs of the recruitment margin | P3 / XP3 |
| `res_i0cm_lam_r2`, `res_i0cm_e1_r2`, `res_i0cm_entry_r2` | 0.223835, 0.359944, 0.287449 | I0/CM threshold equilibrium at r = 2 (only if Remark A.1 prints it) | P3 / XP3 |
| `margin_wtrend_r1_B`, `margin_wtrend_r2_B` | 1/3, 5/18 | D − Ω at r_1 and r_2 | P5 / XP5 |
| `margin_reserve_uniform_B` | 1/4 | ℓ² − 3p² | P5 / XP5 |
| `twopath_lo`, `twopath_hi` | 0.482764, 1.150106 | two-interval path endpoints (only if printed) | P1 / XP1 |
| `share_H_r0_B`, `share_H_r1_B` | to compute | class H's share of challenger takeovers (only if printed) | P2 / XP2 |

Existing keys reused: `margin_weakcost_B` (= c_H − B_{r_0}(1/2) = 1.196, the announcement condition), `rS_B` (sure sale on the capped branch), `res_rcap`, `res_rN`, `res_rC`, `res_rUR`, `res_entry_cap`, `margin_res_amono_B`, `margin_res_rN_B` (cap before the first sale, which explains why the second return never moves benchmark research).

Keys that leave the text (rows may stay): `QJ_r0`, `margin_rhoJ_2_B_frac`. Not printed, by recommendation: the cap-before-selling margin 0.001556, the critical research cost 0.408, the weaker uniform cost ceiling 6.865.

### 3.6 Notation decisions for S1

| Object | Recommended symbol | Collision avoided |
|---|---|---|
| profit gap g_H − g_L | γ | rename the A6 separation distance (A6:354) to words or ς |
| class mean gap Δ + γ | Γ̄ (as at A6:165) | d (signal accuracy, `\fr` argument, E[X] in A8) |
| sure-purchase and no-trade spreads | Δ^{F}, Δ^{N} (roman superscripts) | Δ_T(F), the spread at the law F |
| win-probability gap W_H − W_L | Ω(F) | none |
| max{π, 1 − π} | written out | q, the order |
| low-class informed sale rate | s₋ = λσ_L(−1), as in A4 | z (A6, A7), t (proceeds) |
| recruiting research root, capped | Λ(Δ), λ*(Δ) = min{Λ(Δ), λ̄} | L (class, cost bound) |
| floor-entry research root, capped | Λ_ρ(Δ), λ_ρ*(Δ) | Q (form, statistic) |
| research outcomes | Z, R, Q in A5 (zero, recruiting, floor entry) | R̄ and T as A5 tuple names |
| strength at the cap | r_λ̄ | r̄, the support bound |
| end of floor-entry coexistence | r_Q | r_X reads as the order X |
| research polynomial F_r(λ) | any free letter fixed in S1 | the law F |
| exact recruitment margin | φ_a* | φ_± in A6 is local; acceptable |
| recruitment intensity | λ_E(τ) | λ_E(r) as a function of strength |

### 3.7 Wording targets (each obeys LA1–LA4)

- **T1, Section 3, the two numbers.** "The trading stage sees the auction through two numbers: the spread Δ_T, which sets what an investor who knows the class gains from a correct order, and the preparation threshold τ, which sets the belief a high-cost challenger needs. Two auctions with the same spread and the same threshold have the same orders, posteriors and entry; prices, ownership and welfare also depend on the proceeds and profits themselves. A stronger incumbent widens the spread and, wherever the prior alone fails to recruit a high-cost challenger, raises the threshold, because it lowers the low class's profit and narrows the profit gap between the classes (Appendix A.2)."
- **T2, Proposition 3.** "Let the classes satisfy the class ranking, let the incumbent distribution F give a positive spread and g_H(F) > g_L(F), and let 0 < π < 1. (a) The equilibrium without informed trade and an informative equilibrium coexist against F exactly when π < τ(F) ≤ M(π) and k/[1 − τ(F)] ≤ Δ_T(F) ≤ k/[ρ max{π, 1 − π}]. The informative equilibrium is then unique, and its entry, ρ + (1 − ρ) min{(1 − π)bΔ_T(F)/k, b + πλ}, rises strictly with the spread until the investor buys with probability one. (b) Along a family of incumbent distributions ordered by first-order stochastic dominance, the distributions at which no trade coexists with a certain informed purchase form an interval. (c) If the incumbent is uniform on [0, r] for r in [r_0, r_2], with every low-class value in [p, r_0], every high-class value at least r_2, and a mean high-class value at least r_2 + c_H, the strengths at which the two equilibria coexist form one interval at every prior." Lead-in sentence: "A stronger incumbent widens the spread and raises the threshold, so the economy can enter this region, leave it and return."
- **T3, Proposition 4.** "Let the prior be one half, let an indifferent investor mix over its best orders, and let the incumbent distribution give a positive spread and g_H > g_L. Consider the equilibrium in which a purchase after successful research recruits the high-cost challenger. (a) It exists exactly when Δ_T > 2k and 1/2 < τ ≤ M_{λ*}, where research λ* is the smaller of the cap and the root of 2aλ = Δ_T m_λ − k + (ρΔ_T m_λ − k)⁺. (b) Research, entry and entry given class H rise with the spread until research reaches its cap, and entry given class L falls. The low class sells after bad news once the spread exceeds 2k/ρ; while it mixes, its sale earns exactly the trading cost, so research follows the same schedule. Where a sure sale pays before research reaches its cap, the sale profit adds a second return to research, and the research schedule steepens at that point. (c) Along a family ordered by first-order stochastic dominance on which class H outbids every incumbent, high-class ownership rises weakly with strength, and strictly where research is below its cap and the spread rises strictly. (d) Along such a family, if the recruitment margin rises with strength, is negative against the weakest incumbent and positive where research reaches its cap, the equilibrium holds on one interval of strengths, which ends where the threshold reaches the top posterior at the cap." The recruitment margin is defined in words in the lead-in: the return to a purchase that just recruits, net of the trading cost and of the research it must pay for.
- **T4, Section 5, the worked example.** "In the benchmark, research starts at r_R ≈ \reg{res_rR}, where a purchase that just recruits pays for its research, reaches the cap at r_λ̄ ≈ \reg{res_rcap}, and stays there, with entry \reg{res_entry_cap}, up to the entry ceiling r_C ≈ \reg{rC_B}. The low class starts to sell at r_N ≈ \reg{res_rN} and sells with probability one from r_S ≈ \reg{rS_B}; research is at its cap at both strengths, so the second return to research leaves the benchmark schedule unchanged. Zero research is an equilibrium up to r_N, research at the entry floor coexists with recruiting research up to r_Q ≈ \reg{res_rQ}, and from r_Q on the equilibrium is unique under the default rules." (At r_C, an indifferent challenger that may prepare with any probability spreads entry over an interval; Remark A.1 states it, and the main text needs no more than "under the default rules".)
- **T5, coexistence figure note.** "The thin dashed line is the threshold branch T. At r_A its purchase recruits with probability one and it is an equilibrium under the default rules; on (r_A, r_J] it is an equilibrium when an indifferent high-cost challenger may prepare with any probability."
- **T6, research figure note.** "The benchmark with a = \reg{res_a} and cap λ̄ = \reg{res_cap}, when an indifferent investor may mix and an indifferent high-cost challenger prepares. Panel (a) shows research and panel (b) entry in each equilibrium. Zero research holds from r_0 to r_N. Recruiting research starts at r_R, reaches the cap at r_λ̄ and stays there up to the entry ceiling r_C, with entry \reg{res_entry_cap}. Research at the entry floor, with both classes trading after a success, holds on (r_N, r_Q) and above r_C, with entry ρ. Black dots mark the six strengths of Table 4."
- **T7, A4 opening.** "This subsection states in full and proves Proposition 3 and Corollary A.2. The first part holds for every incumbent distribution and every prior; the second part applies it to the benchmark path."
- **T8, A9 convention.** "Each margin is the exact difference between the two sides of its inequality, signed so that a positive number means the hypothesis holds; decimals round exact values. A negative entry marks a comparison economy built to fail its hypothesis."
- **T9, A2 opening.** "This subsection states and proves the results behind Sections 3.2 and 3.3. The belief lemma holds for every order profile, in or out of equilibrium; the price and trading lemmas hold for every tuple that meets the conditions they list."
- **T10, Proposition 2(ii) addition.** "If class H outbids both incumbents, W_H(F_0) = W_H(F_1) = 1, high-class ownership rises, and so does class H's share of the takeovers that a challenger wins, strictly when a low-class challenger beats the weak incumbent with positive probability."
- **T11, a method inside a proof.** "Since every incumbent value lies below h and h − r_2 − c_H = \reg{margin_afford_uniform_B} > 0, Proposition 3(c) applies, and J rises strictly on the path."
- **T12, A5 opening.** "This subsection states in full and proves Proposition 4 and the equilibria with research at the prior 1/2, then applies them to the benchmark path."

---

## 4. Label and numbering map

**Numbering policy (decision D9).** No new numbered proposition, corollary or remark environment enters the appendix. New general results enter as named full statements of main-text propositions (unnumbered, like the present "Proposition 3 (full statement)"), as lemmas placed after Lemma A.3, or as parts of existing propositions. Then Propositions A.1–A.14, Corollaries A.1–A.3, Remark A.1 and Definition A.1 keep their numbers, and so do Propositions 1–4, Tables 1–5 and Figures 1–3. Only lemmas from A.4 on and the appendix tables after Table A.3 renumber.

**Labels added**

| Label | Object | Number | Placement |
|---|---|---|---|
| `lem:reduction` | the auction through two numbers | Lemma A.4 | A2, after `lem:trading` |
| `lem:twonumbers` | the two numbers along a path | Lemma A.5 | A2 |
| `lem:decisive` | decisive advantage | Lemma A.6 | A3, after the proof of Prop 2 |
| `lem:a5-sale` | the low class's sale under IM | Lemma A.15 | A5 |
| `lem:a5-outcomes` | the equilibria with research at prior 1/2 | Lemma A.16 | A5 |
| `tab:a5-set` | research equilibria on the benchmark path | Table A.4 | A5 |
| `eq:region`, `eq:entry-inf`, `eq:research-im`, `eq:research-exist` (names fixed in S1) | displays of the full statements | (A.n) | A4, A5 |

**Labels removed**

| Label | Successor | Internal references to update |
|---|---|---|
| `lem:a5-middle` | `lem:a5-outcomes` (Z), Prop 4 full statement (R, R̄), `rem:researchties` (T) | A5:241, 246, 250, 262, 278, 302, 313, 343, 348, 400 (427, 439 deleted with the certificates paragraph) |

**Labels renumbered or retitled**

| Label | Before | After | Note |
|---|---|---|---|
| `lem:a4-path` | Lemma A.4, "The path" | Lemma A.10, "The benchmark path" | hand proofs |
| `lem:a4-order` | Lemma A.5 | Lemma A.11 | |
| `lem:a4-high` | Lemma A.6 | Lemma A.7 | at a fixed F |
| `lem:a4-low` | Lemma A.7 | Lemma A.8 | |
| `lem:a4-product` | Lemma A.8 | Lemma A.9 | |
| `lem:a5-joint` | Lemma A.9 | Lemma A.12 | |
| `lem:a5-bounds` | Lemma A.10 | Lemma A.13 | |
| `lem:a5-buy` | Lemma A.11 | Lemma A.14 | |
| `lem:a5-strong` | Lemma A.13 | Lemma A.17 | |
| `tab:classes` | Table A.4 | Table A.5 | only if `tab:a5-set` is added |
| `tab:a9-declarations` | Table A.5 | Table A.6 | same |
| `tab:margins` | Table A.6 | Table A.7 | same |
| `prop:coexistence` | "Coexistence on the benchmark path" | "Quiet and informative markets" | number 3 unchanged |
| `prop:region` | "The admissible region" | "The parameter region at the benchmark" | A.1 unchanged |
| `prop:researchregion` | "The admissible cap and cost" | "The research cap and cost at the benchmark" | A.2 unchanged |
| `prop:spread` | "The spread and its entry component" | "The price gap and the weighted test" | A.11 unchanged |
| `prop:informedshare` | "Identification of the informed share" | "What order counts and prices identify" | A.12 unchanged |

Lemma order after the upgrade: A2 holds A.1–A.5; A3 holds A.6; A4 holds A.7–A.9 (general) and A.10–A.11 (benchmark); A5 holds A.12–A.17. The named results are "Proposition 1(c)", "Proposition 3 (full statement)", the benchmark path at prior 1/2, "Proposition 4 (full statement)" and the benchmark research list.

**Consumers that cite numbers or content**

| Consumer line | Cites | Action |
|---|---|---|
| `comparison.tex:138, 141, 144, 200, 201, 658` | Lemma A.1, A.2, A.3 | numbers stable; content stable |
| `comparison.tex:206` | Corollary A.2 | number stable; text: set formula from the region theorem |
| `comparison.tex:380, 654` | Definition A.1 | stable |
| `comparison.tex:209` | Table A.4 (value classes) | → Table A.5 if `tab:a5-set` is added |
| `comparison.tex:445, 659` | Table A.6 (margins) | → Table A.7 if `tab:a5-set` is added |
| `comparison.tex:660` | Table A.3 (tie rules) | stable |
| `comparison.tex:205, 207, 232–305, 351–358` | Props 3, 4, A.2, A.11–A.13 content | rewrite to Part 3.1; remove status words |
| `slides.tex:328` | Lemma A.3 | stable |
| `slides.tex:456–468` (F12) | Prop 3 content | region in words; [r_A, r_N] as the benchmark instance |
| `slides.tex:476–486` (F13), 773–776 | Prop 4 and "Proposition 4(a)"; [r_R, r̄_R) | parts relabelled (a)–(d); [r_R, r_C] with the cap at r_λ̄ |
| `slides.tex:545–550` (F16) | A.11–A.14 | weighted test; winner sign condition |
| `slides.tex:501–504, 687–692, 794–795` | Propositions A.1, A.2, A.4–A.7, A.9 by number | stable |
| main text | `\ref{prop:priors}`, `\ref{prop:region}`, `\ref{prop:researchregion}`, `\ref{tab:margins}`, `\ref{tab:a4-ties}` | automatic |
| out of scope | 19 files in `slot/study_guide/`, 2 in `presentation/` cite appendix numbers | stale; list for a later pass |

---

## 5. Risks and traps

1. **Tie-rule drift.** The region and its uniqueness hold under IM and C1; CM adds the threshold pair inside the region and the point τ = π; I0 needs Δ > k/(1 − M(π)). The research continuation holds under IM only; under I0 full recruitment disappears on (r_N, r_S] in the benchmark, and under I0 with CM a threshold equilibrium survives at r = 2. *Mitigation:* the tie column of Part 3.1 is part of each Solver A brief and each the independent referee check.
2. **Prior drift.** Research results, the two-channel covariance, the winner second difference and the prior-1/2 count fact hold at prior 1/2 only; the unweighted test needs π ≥ 1/2 and ρ ≤ 1/2 under C1; identification by counts needs a known prior other than 1/2. *Mitigation:* the prior column; the independent referee rejects any statement without its prior.
3. **Interval language.** Along an arbitrary path only the sure-purchase stretch is an interval; the whole coexistence set needs the uniform condition or the balance condition; the research set is pointwise and needs the cheap-research condition. A sentence that says "on an interval of strengths" without its condition is false. *Mitigation:* the two-interval example sits in A4 as a stated fact, and the sweep searches for "interval".
4. **Weak and strict.** Entry on the informative branch rises strictly only while the purchase is mixed and the spread rises strictly; class entry and ownership rise strictly only below the cap; the winner gap widens strictly only where W_L falls strictly; the takeover share rises strictly only when W_L(F_0) > 0. *Mitigation:* the independent referee checks every "strictly".
5. **τ boundaries.** s* needs τ < 1; τ ≥ 1 removes recruitment; τ monotone needs τ ≥ 0. *Mitigation:* the restated A4 lemmas carry the cases (RED §1 table).
6. **The CM shortcut.** Constructions that pool orders at one posterior (the research continuation pools the sale and the zero order) must check equal entry. *Mitigation:* fix A2:165–170 in S2, before S5 writes.
7. **Uniqueness claims after the continuation.** Uniqueness under every tie rule holds above r_U (condition U); under the defaults it holds from r_Q; neither extends to I0 or CM below r_U. *Mitigation:* both statements appear, each with its rule.
8. **Fixed-value acquisition kernel.** True almost everywhere and wherever class H can win; at atoms the auction's tie rule decides; outside the support it is a counterfactual. *Mitigation:* the statement carries "almost every value at which class H can win".
9. **Decisive advantage as a family property.** It holds for point classes and the whole uniform family; a two-part incumbent with benchmark h, ℓ, p, c_H lowers ownership. *Mitigation:* Lemma A.6 is stated for a family.
10. **Numbering.** Any numbered proposition, corollary or remark inserted before A.14 shifts every consumer citation. *Mitigation:* policy D9.
11. **Symbol collisions** (γ, d, Δ_F, L, Q, z, r̄_R, r_X). *Mitigation:* S1 before any writing.
12. **Main text ahead of the appendix.** A main-text statement written before the full statement drifts. *Mitigation:* S9 starts after S8; the independent referee signs each statement.
13. **Removing scripts removes the only stated basis of some numbers.** *Mitigation:* every number that a proof uses is either an exact closed form or a root whose existence and uniqueness the text proves; displays carry no logical role; the registry keeps the source of each value.
14. **the mathematics writer prose breaking the language rules** ("we", "certified", "new lemma", "generalizes the result of the previous version", hedges). *Mitigation:* the rule card in every brief; Appendix B sweep on each package; LA6 pass before integration.
15. **Benchmark story change.** Section 5's narrative, Table 4 notes, the figure, slides F13, comparison row 207 and the introduction all describe the branch ending at the cap; each must say the recruiting equilibrium runs to the entry ceiling. *Mitigation:* the consumer table in Part 4 and a sweep for `res_rcap` and r̄_R.
16. **Austin's Overleaf edits.** A pull after 69c25f4 can move every line reference here. *Mitigation:* S0 re-anchors references before S2.
17. **Typed fractions.** 937/5520, 9667/8280, 81/80, 2/5, 1/3, 5/18, 1/4 must print through `\reg`. *Mitigation:* keys in S7 before S8.

---

## 6. Decision points for Austin

| # | Decision | Recommendation |
|---|---|---|
| D1 | Delete the stray `ty` at `sections/02_model.tex:1` | Yes. |
| D2 | Region panel in the (Δ, τ) plane | Yes, as panel (c) of Figure 2, so no figure renumbers; closed-form boundaries and the benchmark path, entering at r_A and leaving at r_N. |
| D3 | Fill the research figure | Yes, with the three outcomes and no broken axis. |
| D4 | Corollary A.2 at other priors | Keep; its proof shortens to the region theorem plus the benchmark monotonicity, all by hand. |
| D5 | Identification in Section 8 | Keep known-prior identification and the sale-price inversion; leave the unknown-prior local result and the incentive-collapse example out of the paper. |
| D6 | A.7 extended; A.9 skipped; A.5 on the uniform family | Yes to all three. |
| D7 | Keep 1 + u = e | Keep; every benchmark number and the comparison with the Laplace version rest on it. |
| D8 | Consumers limited to `comparison.tex` and `slides.tex` | Yes; record the stale passages in the study guide and the presentation for a later pass. |
| D9 | Numbering policy | Adopt: no new numbered proposition, corollary or remark in the appendix. |
| D10 | Numbers and figure scripts write to the master or the mirror | Write to the master `overleaf/slot/` (one constant each in `make_numbers.py`, `number_scan.py`, `make_figures.py`); resync the mirror after an approved push. |
| D11 | The abstaining-branch corollary (cap before selling, margin 0.0016) | Drop; the recruiting equilibrium continues under IM. |
| D12 | An example economy for the second return to research (Solver D's c_H = 5 economy) | Leave out; the kink is part of the full statement, and the benchmark explains why its schedule has one piece. |
| D13 | Small-trading-cost and boundary-derivative conditions for coexistence | Leave out; the uniform and balance conditions cover the paper's needs. |
| D14 | Same-incumbent ownership ratio | One sentence after the Proposition 4 proof, no environment. |
| D15 | Decisive-advantage lemma | Include (Lemma A.6); it gives the cost bracket 399/80 ≤ c_H ≤ 32/5 with the benchmark's 6 inside. |
| D16 | The research list as Table A.4 | Add it, and move three table citations in `comparison.tex` (Part 4); otherwise state the list as a paragraph. |
| D17 | Two-interval path in A4 | Include as a paragraph with its two endpoints through `\reg`. |
| D18 | Vocabulary: "the benchmark" or "the worked example" | Declare the benchmark once as the worked example in Section 2 and say "the benchmark" everywhere after, as SCAN Part 4 proposes. |
| D19 | Scope of `comparison.tex` | Keep the set-ups, results and trade-offs; cut the method, verification and certificate sections and every status column, since the language rules leave them nothing to say. |
| D20 | Winner second difference and unweighted test | Keep both as parts of A.13 and A.11. |

---

## 7. What the other two lenses might miss

1. **`comparison.tex` is a method-and-status document by construction**: 29 hits for "analytical", 24 for "computer-assisted", 5 for "numerical diagnostic", 33 for "script", 19 for "certif", plus sections `sec:method`, `sec:verification` and `sec:certificates`. A sweep cannot fix it; it needs the scope decision D19 before S11.
2. **The research figure needs new curve functions** in `make_figures.py`: the floor-entry root, r_Q, the plateau at the cap up to r_C, and the removal of the broken axis. The code today stops the recruiting branch at the cap. This depends on S5 and on obligation O1.
3. **The appendix tables shift** if `tab:a5-set` is added, and `comparison.tex` cites Table A.4 and Table A.6 by number.
4. **Removing script text exposes numbers with no stated basis.** Before deleting a script sentence, S8 checks that the number is a display or an exact closed form argued in the text (Part 3.3).
5. **The A9 margins table** carries a Source column, a note listing registry keys, and "Value at B"; the language rules remove all three, and the table must gain the rows of Part 3.5.
6. **Orphaned keys and lines.** `QJ_r0` and `margin_rhoJ_2_B_frac` leave the text, and the A4 Step 7 sentence on r_J < 2 goes with them.
7. **The β footnote** at `02_model.tex:123–125` lists results by name and must be re-derived per result (O2).
8. **Prop A.2's referent.** Its statement cites "the equilibrium patterns of Proposition 4(b)", which leave the main-text proposition; the reference must point to the benchmark research list.
9. **Slides F13 relabel parts.** "Proposition 4(a)" there cites benchmark content; after the upgrade part (a) is the existence condition.
10. **The slides' "At $B$"** (rows at 503 and 797) and comparison.tex's "calibration B" (2 hits) fall under LA3.
11. **The registry status column** (analytical, computer-assisted) stays internal; nothing may copy it into a table note or caption.
12. **The study guide and the presentation** cite appendix numbers in 21 files and describe the research branch ending at the cap; outside scope, but Austin should know they go stale.

---

## Appendix A. Rule card for every writer and reviewer

Paste this into every brief, the mathematics writer and the prose writer alike.

1. Write the paper once, as a finished paper. Never narrate its history or production: no "now", "new", "updated", "revised", "corrected", "replaces", "in this version", "previously", "generalizes the earlier result"; no registry, script, run log, exercise, checker, certificate, recomputation, verification record, file name, key, "calibration B", "S(B)" or workstream code. Comparative statics across strengths are economics and stay.
2. No result-status labels anywhere: not "analytical", "computer-assisted", "numerical diagnostic", "certified", or "open" as a status. Inside an appendix proof, state a method as mathematics: "an exact rational computation gives", "the quadratic formula gives".
3. State every result positively, with its scope inside the claim. A named condition is a hypothesis, stated once. No caveat, reassurance or referee-answer paragraph; no hedge; no paragraph ends on a limitation. "May" appears only in the tie-rule phrases.
4. Single author: "I". Every number through `\reg{key}`, fractions included. No bold sentence in running text. No tool, reviewers or model name.
5. Use the plain tie-rule phrases in prose ("an indifferent investor may mix", "an indifferent high-cost challenger prepares"); codes appear nowhere in the manuscript.
6. Use the symbols of the notation table; one symbol per object.

## Appendix B. Sweep patterns (case-insensitive; every hit is fixed or justified)

- Status: `\b(analytical(ly)?|computer[- ]assisted|numerical diagnostic|certif(y|ied|icate|icates|ication))\b`; `\b(remains? open|is open|open (question|problem|item|result))\b`.
- Defensive: `\b(arguably|it should be noted|it is worth noting|of course|to be clear|we do not claim|this is not to say|in some cases|not necessarily|could be argued|admittedly|caveat|only in the benchmark)\b`; `\bmay\b` (allowed in the tie-rule phrases).
- Development log: `\b(now|no longer|new(ly)?|updated?|revis(e|ed|ion)|correct(ed|ion)|replac(e|es|ed|ement)|in this version|earlier (draft|version)|previous(ly)?|upgrade)\b`; `generaliz\w* (the )?(earlier|previous)`; `restriction is removed`.
- Process: `\b(registry|script|run log|exercise|checker|recomput\w*|verifi(ed|cation)|calibration B|Sturm|workstream|enclosure|interval arithmetic|bisection)\b`; `\\nolinkurl`; `\.py\b`; `\.log\b`; `\b(XP|P)[1-5]\b`; `\bW[1-5]\b`; `S\(B\)`; `Value at B`; `\bat \$?B\$?\b`.
Review names and voice manually under PLAN.md Part 2; use the first-person singular.
- Bold: `\\textbf\{` outside proposition heads, table panel heads and slide labels.
- Interval claims: `interval of strengths` (each hit must carry its condition or be the sure-purchase stretch or the benchmark).
