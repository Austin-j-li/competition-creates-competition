# Scan of the order-slot manuscript (24 October 2026)

Target: `slot/manuscript/` on branch `slot`, commit `2c56325`. The Overleaf project
`6adbcf95d3bcdaeacca72fcf` was at the same state (`001a620`). The scan changed no manuscript file.

The author's request: check the mathematics, remove defensive writing, and change the main text from
"math paper" prose to the prose of the earlier Laplace draft. That draft is `laplace/manuscript/main.tex`
on branch `laplace` (Overleaf `6abd31b3b1fcb8e38afbb670`, commit `01bd5d6`). Formal environments stay
in Appendix A, with very few in the main text.

## 1. Method

- Mathematics: two independent auditors for each half of the paper. The core is Sections 2-4 and
  Appendix A.1-A.4 and A.9. The extensions are Sections 5-8 and Appendix A.5-A.8. The auditors did not
  read the earlier check memos or the referee memo. After the first round, each auditor judged every finding
  of the other auditor in the same half. Reports: `reports/math_*.md`, `reports/reconcile_*.md`.
- Numbers: the auditors recomputed every `\reg` key from closed forms with exact fractions and outward
  interval arithmetic (scripts in `scripts/`; they print values and assert nothing). The number scan
  (`audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`) found 676 keys, no missing
  key and no decimal typed directly in the source.
- Prose: three scans of the abstract and Sections 1-9. Reports: `reports/prose_defensive.md`
  (defensive writing, 63 rows), `reports/prose_apparatus.md` (formal environments, notation, a proposed
  skeleton), `reports/prose_voice.md` (comparison with the Laplace draft, three sample rewrites).

## 2. Mathematics

### 2.1 Result

The main result, the coexistence result and every number are correct. The auditors recomputed 194 core
displays and 390 extension keys. All values agree with `numbers.tex` at the displayed precision. The
certificates for the small margins use rational bounds on e:

- return margin at `r_2`: `tau(r_2) - M = 0.000333564719409...`;
- `r_2 - r_C = 0.007341481205338...`.

The (H2) bound `rho * kappa * Delta_1` is a lower bound under every candidate profile, with
`kappa = min{m, 1 - M}`. The zero-order branch needs `beta <= 1/3`, and Section 2 states it.

Both auditors in each half agree on all eleven findings below. No finding changes a number, a figure or
the statement of Propositions 1-4.

### 2.2 Findings

| # | Name | Severity | Location | Problem | Proposed fix |
|---|---|---|---|---|---|
| M1 | Boundary of the admissible region | Critical | `appendix/A3_proposition2.tex:169`, proof at `:208` | At `u = 82/59` the text says orders are uniquely full at all three strengths; at `r_0`, `Delta_0 = 1/60 < k = 1/50`, so orders are uniquely zero. | State zero orders at `r_0` and full orders at `r_1`, `r_2`, in the statement and the proof. |
| M2 | Fixed-information control without independence from the incumbent value | Critical (one auditor: High) | `appendix/A6_robustness.tex:8-22`; main text `sections/04_equilibrium_results.tex:188-190` | The general experiment does not make the signal independent of the incumbent value; an exact example with `F_1 <= F_0` gives entry 5/8 to 1. | Require that `(theta, R)` given `(j, S)` has law `G_j x F_i`, with the independent cost law; change "for every information experiment" in Section 4 to match. The slot control satisfies this condition. |
| M3 | `t_L(r)` for two objects | Mid | `appendix/A4_coexistence.tex:204`, `:263-277`, `:317-322` | The low-class sale rate reuses `t_L`, which Section 2 defines as low-class target proceeds; one tuple uses both. | Rename the sale rate (for example `s_-^*(r)`) in A.4. |
| M4 | Private signals: no explicit witness | Mid | `appendix/A6_robustness.tex:462-463` | The last step infers that a challenger signal more accurate than the investor's is feasible, but gives no example. | Add the exact witness `(lambda, beta) = (1/3, 3/10)`, `(a_T, d) = (7/10, 3/4)`, with five positive rational margins. |
| M5 | Sale payoff without its cost | Mid | `appendix/A6_robustness.tex:527` | The displayed sale return omits `k`, but the next clause calls its root a zero-profit rate. | Display `b/[15(2b+t)] - 1/50`; the rate `4b/3` is unchanged. |
| M6 | Dispersion "raises" gross profit | Mid | `sections/06_robustness.tex:44-45` | Convexity gives a weak increase; the appendix says "weakly". | Write "weakly raises". |
| M7 | Research region cites a fixed entry number | Mid | `appendix/A5_research.tex:291-294`; `sections/05_research.tex:64-65` | The region proposition invokes the whole benchmark proposition, but entry at `r_1` changes with the cap (0.5218 at cap 0.33). | Limit the reference to the equilibrium pattern and give entry as `rho + (1-rho)[beta + (1/2 - beta) * cap]`. |
| M8 | Introduction: wrong regime for the winner prediction | Mid | `sections/01_introduction.tex:98` | "Against a strong prepared bidder, orders no longer predict entry" is false at `r_1 = 3`; it holds above `r_C`. | Write "Above the entry ceiling". |
| M9 | Shortfall with a negative value | Low | `appendix/A6_robustness.tex:266-268` | The text says top profit misses the cost by -1.390821. | Report the signed gap, or the shortfall 1.390821. |
| M10 | Positive purchase payoff in the zero-research equilibrium | Low | `appendix/A5_research.tex:172` | Step 5 says the purchase payoff is positive in every listed equilibrium; in Z it is negative. | Restrict the sentence to positive research; cite Step 1 for Z. |
| M11 | Third-strength check without a third strength | Low | `appendix/A6_robustness.tex:235-237`, `:250-252` | The notes say five rows satisfy every hypothesis, but the moderate-gap row has no `r_2`. | Say that this row satisfies (H1)-(H2) and the other four rows also satisfy (H3). |

Propagation: M2 touches the general claim in the main-text sentence at `04:188-190`. The abstract states
the slot control, which satisfies the condition, so the abstract does not change. M1, M3-M5 and M9-M11 are
local to the appendix. M6-M8 are local to the main text. A fix of M7 changes the text of Proposition
`prop:researchregion` only. The audit did not cover `slides.tex` and `comparison.tex`; when M6 and M8 are
fixed, search both documents for the same wording.

## 3. Prose

### 3.1 Defensive writing (`reports/prose_defensive.md`)

63 rows, 56 need action. By pattern: repeated scope 15, referee pre-emption 11, negative framing 10,
high-impact caveat 7, not-X-but-Y 6, stacked hedge 4, limitation-first paragraph 4, apology framing 3,
non-claim 3. Three habits cause most rows:

1. Proof notes in the main text: the tie rules in sixteen places outside Section 2.4, margins to each
   boundary, the use of `beta <= 1/3`, "each hypothesis is used once".
2. Results that changed against the Laplace draft read as concessions: "entry does not rise" and "rises
   weakly". The positive forms are "a stronger incumbent can only lower entry" and "rises, then stays
   constant". Both are exact: Proposition `prop:control` gives a nonnegative decrease, and the coexistence
   branch rises strictly on `[r_A, r_F]` and is constant on `[r_F, r_N]`.
3. One scope condition at every position: abstract, introduction, section and conclusion.

The ten hits with the most effect are in the abstract (`main.tex:93-95`), the conclusion (`09:9-13`), the
introduction (`01:43-47`, `01:57`, `01:130`), the paragraph after the main result (`04:42-43`), the margins
paragraph (`04:160-164`), and the openings and endings of Sections 6 and 7.

### 3.2 Formal apparatus (`reports/prose_apparatus.md`)

The main text has 15 formal environments: 1 assumption, 1 definition, 4 propositions, 3 lemmas,
3 corollaries and 3 remarks. It also has four label systems: (H1)-(H3), (E1)-(E7), the tie-rule names
IM/I0/C1/CM and the form letters N/R/F/Q/T. It defines about 100 symbols. The Laplace draft has three
propositions in the main text and no other environment.

Proposal: four numbered propositions, one for each claim of the abstract.

| Main-text result | Status | Source |
|---|---|---|
| Proposition 1: competition and the two returns to information | analytical | current Proposition 1 |
| Proposition 2: competition creates competition | analytical | current Proposition 2, statement in words where possible |
| Proposition 3: coexistence on the benchmark path | computer-assisted | current Proposition 3, short form; full form in A.4 |
| Proposition 4: competition creates research | (a) analytical, (b) computer-assisted | current Proposition 4 merged with Corollary 3 |

Everything else changes:

- Assumption 1 (class ranking) and Definition 1 (equilibrium) become prose, as in the Laplace draft. The
  formal tuple goes to the opening of Appendix A.
- Lemmas 1-3 and Corollary 1 become prose with two displays; their statements go to A.2.
- Corollary 2 and Remarks 1-2 go to A.4 and A.5, with two sentences left in the main text. Remark 3 becomes a
  footnote in Section 2.3, and Section 6.4 goes.
- Seven inline status tags in Sections 5-8 go; the status stays with each appendix statement and in the
  four proposition titles.
- About 35 symbols leave the main text (about 65 remain).

Estimate: the main text goes from about 38 pages to about 30. Proposition A.1-A.14 numbering stays, so the
hand-typed numbers in `slides.tex` and `comparison.tex` stay correct. The label changes to carry are listed
in Section 6 of the report.

Fallback with three propositions: Proposition 4 moves to A.5, and Section 5 states the comovement in prose.

### 3.3 Voice (`reports/prose_voice.md`)

| Measure | Slot draft | Laplace draft |
|---|---|---|
| Lists (`enumerate`, `itemize`) in the main text | 14 | 0 |
| Inline math in the introduction | 12 | 1 |
| Median words in an introduction paragraph | 93 | 130 |
| Sentences of 30 words or more | about 1% (introduction 0%) | about 7% (introduction 9%) |
| Semicolons per 100 sentences | 4 (introduction 2) | 10 (introduction 25) |
| Paragraphs that open with "Two ..." or "Three ..." | 8 | 2 |

The slot draft adapts much of the Laplace text, and the adaptation split its sentences. The connectives
went, and the logic went with them. Other habits: one argument spread over several paragraphs; numbered
lists for the trading stage and the timing; the formal object before the economics; proof talk in the main
text. The report gives three sample rewrites in the Laplace register: the opening of the introduction, the
order-slot subsection, and the main result.

Keep from the slot draft: every number through `\reg`; one topic for each paragraph in the introduction's
tour of results; the complete equilibrium set where the Laplace draft said "open"; the intuition passages at
`03:60-69`, `03:80-81`, `03:198-199`, `04:352` and `05:16-19`.

The scans did not copy the Laplace draft's own defensive passages (for example ref. 858-860, 866-867,
999-1000, 1089).

### 3.4 Points where the scans differ

- Class ranking: the defensive-writing scan keeps Assumption 1 as the one place for this condition; the
  apparatus scan moves it into prose. The author's request favors prose.
- Sample C of the voice scan keeps references to lemmas, a corollary and the assumption, because its scope
  was the voice. Under the apparatus plan these references become prose or appendix references.

## 4. Decisions for the author

1. Register: for manuscript text, use the Laplace draft's register (longer sentences where one thought
   needs them, semicolons, participles) instead of the short-sentence controlled style.
2. Number of main-text propositions: four (with research) or three.
3. Order of work: see Section 5.
4. Slides and comparison note: change them in the same pass, or after the manuscript.

## 5. Proposed order of work

1. Mathematics. Apply M1-M11. They are small and independent of the prose. A check confirms each fix and
   its consumers.
2. A pilot section. Rewrite Section 1 and Section 4.1 in the target register, with the apparatus plan
   applied there. The author approves the register before the other sections change.
3. Structure. Move the environments as in Section 3.2, and carry every label and reference.
4. Prose, section by section, from the defensive-writing rows and the voice samples. One reading for voice
   across all sections at the end.
5. Checks: build, number scan, no undefined references, page count, and a final math audit of every
   changed statement. Send to Overleaf only after the author approves.
