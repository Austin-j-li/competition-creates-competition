# Final polish pass: report P

Base: commit `2eed6b6` on branch `slot-revision`. I located every hit by content, not by the line numbers in the prose check. I edited only the abstract in `slot/manuscript/main.tex` and `slot/manuscript/sections/*.tex`. I made no commit. I wrote no test.

## Hits

### Category 1: defensive writing

- D1 (08, control repeated from 04): applied. Section 8 now cites the fixed-information control of Section 4.2 and keeps both proposition references; the condition has one home.
- D2 (06, benchmark with the accuracies of S(B)): appendix request. The appendix already states the tuples, entry and the tie-rule facts; only the two rate decimals lack an appendix home, so I left the paragraph in place until the insertion below lands.
- D3 (04, computational bookkeeping): applied. The benchmark paragraph now gives the slot values and one appendix pointer; the upright-e note sits in the model footnote where the letter first enters.
- D4 (02, chronology pre-emption): applied. Only the plain forward reference to Section 8 remains.
- D5 (02, outsider caveats): applied. The investor paragraph now states the positive facts; the hedge clause and the negative source clause are out.
- D6 (02, bid without preparation): applied. One sentence states that a challenger that does not prepare stays out, so its cost is an entry cost.
- D7 (01, investor lead sentence): applied. The lead sentence has no negation; the next sentence carries the contrast.
- D8 (01, signals tour): applied, merged with T5. The tour states the signals result in one sentence; Section 6.3 keeps the scope at the benchmark and at other costs and strengths.
- D9 (09, strict-where-it-mixes tail): applied. The conclusion states the exact path: entry rises while the investor mixes, then stays constant once the high class buys for sure.
- D10 (01, what uniqueness covers): applied. The introduction keeps the headline uniqueness claim in the proposition's own words, "the equilibrium outcome is unique", and drops the coverage commentary.
- D11 (02, tie conventions): applied. The sentence now names ties and points to the appendix tie table.
- D12 (07 and 06, stacked "weakly"): applied. Both places state the exact direction in plain words and keep the strictness condition in full.
- D13 (02, private incumbent value, third use): applied. The distribution sentence stands alone; the two earlier statements remain.
- D14 (03, two restatements): applied. Each place now states the bound or the split once; both appendix pointers remain.
- D15 (02, slot property in negative form): applied. The sentence states the residual advantage directly.

### Category 2: AI tells

- A1 (08, "spread" for two objects): applied. Section 8 now says "the price spread" in the heading, at the definition, in the benchmark values and in the informed-share paragraph; "the spread" alone still names the target-payoff spread.
- A2 (names for the challenger): applied with change. Section 2.1 names the challenger once and then uses it, Section 8 keeps its empirical names after D1, and the abstract uses "challenger" throughout; truly generic "a buyer" statements about any bidder stay.
- A3 (preparation for entry): applied. Section 8 says entry returns to its floor, and the reserve table column now reads "Entry".
- A4 (03, ceiling label closer): applied through R10. The name now opens the ceiling sentence.
- A5 (02, staged opener): applied. One plain sentence states that the identity is common knowledge and only the fit is uncertain.
- A6 (01, count opener and one-use term): applied. The paragraph opens with the two holders; "acquisition claim" is out.
- A7 (07, count label): applied. The reserve paragraph names the three events and then defines each in one sentence.
- A8 (07, not-X-but-Y opener): rejected. Both sides name model objects and the dividend experiment in the same paragraph proves the distinction, so the guide's exception applies.
- A9 (parameters against primitives): applied with change. The introduction and the conclusion now say "parameters", and I also changed "benchmark auction primitives" in the introduction for the same one-word rule.

### Category 3: sentences a reader must restart

- R1 (04, "no informed trade" as subject): applied at all five places. Each sentence now uses "the equilibrium without informed trade" as its subject; the pattern name stays where it is not a subject.
- R2 (05, "no research" as subject): applied. The sentence uses "the equilibrium without research".
- R3 (04, ordinal priors): applied. The sentence names the two priors by their registry values and has a comma after "on".
- R4 (01, "this entry component" without antecedent): applied. The introduction now defines the gap from the price after no order before it names the entry component.
- R5 (08, impacts undefined in the main text): applied with change. The definitions now sit inside the first sentence, in words and with the formulas \(P(1)-P(0)\) and \(P(0)-P(-1)\) kept exactly.
- R6 (07, "To see why" two paragraphs late): applied. The worked argument now sits directly after the sign result; the benchmark number and the literature contrast follow it.
- R7 (04, "the statement" and \(r_J\) twice): applied. The paragraph names the entry ceiling by its home section and marks each strength once.
- R8 (06, high group undefined): applied. The separation sentence now states the split into the two groups before it uses the names.
- R9 (04, "the probability in Proposition A.x"): applied. The sentence states what the probability is and keeps the proposition reference at the end.
- R10 (03, "follows no price" and label closer): applied. The first sentence is plain, and the ceiling name opens the second.
- Further 1 (04, band width): applied. The threshold's slow rise is the subject.
- Further 2 (05, scope inside a conjecture sentence): applied. The prior scope is its own clause, and the equilibrium sentence has one main verb.
- Further 3 (07, "contributes the sales", "each term"): applied. The sentence adds gross profit minus cost and the unblocked-sale value to net surplus, and ends on the nonnegative form that the appendix states.
- Further 4 (08, shares that counts allow): applied. The incentives "narrow" the shares, and "consistent with both" replaces the repeated phrase.
- Further 5 (04, control condition as one sentence): applied. The condition is now three sentences with every independence statement kept in full; see the mathematics list below.
- Further 6 (09, "the comparison"): applied. The conclusion names the weak, strong and very strong incumbent.
- Further 7 (01, "at which recruitment stops"): applied. The phrase now reads "against which recruitment stops".
- Further 8 (04, Proposition 2 frame): applied with change. The first "Let" sentence ends at the strengthenings, and a second "Let ... be given, and suppose that" sentence carries the hypotheses in words, unchanged in content.

### Category 4: math-paper apparatus

- P1 (02, "Proposition 1(c)"): applied. The appendix pointer now joins the sentence that states the weakest restriction in words.
- P2 (04, "Proposition region(a)" three times): applied with change. Each place keeps `\ref{prop:region}` and drops the part letter, and one place names the band of the region table. I rejected the proposed tau wording inside Proposition 3, because Proposition region assumes \(\beta\le1/3\) while the coexistence appendix frame allows \(\beta<1/2\); that scope needs a mathematics decision, not a prose change.
- P3 (04, corollary by name): applied with change. The main clause gives the appendix in words and the corollary reference stays in parentheses, so no cross-reference is lost.
- P4 (03, proof step as subject): applied. The paragraph runs at one incumbent value, with no command and no proof subject.
- P5 (04, "do not use (H3)"): applied. The text now says parts (i) and (ii) hold without the ceiling.
- P6 (05, imperative "write"): applied. The sentence reads "I write".
- P7 (07, "Hold the incumbent"): applied. The comparison is a plain first-person sentence at \(F_1\).
- P8 (proposition frames): applied with change. Proposition 2 uses the split frame of Further 8, and Proposition 3 opens with "Let the auction be ... and let the slot lie in the band", with the band reference kept.
- Optional 1 (02, equilibrium definition pointer): rejected. The guide allows this single pointer, and it carries a live cross-reference.
- Optional 2 (03, "Consider a prepared challenger"): rejected. The command opens a derivation, which the guide allows.

### Category 5: tour, abstract and section mismatches

- T1 (01, complete set "between and beyond"): applied. The introduction credits Appendix A.4 with the complete set along the benchmark path.
- T2 (ownership without its condition): applied with change. The introduction now attaches the condition on the high class's chance to win and says the benchmark meets it, in the direction of Proposition 2(ii). I left the abstract sentence as it stands, because its open-set claim is existential and the benchmark meets the condition on an open set; the final mathematics check should confirm this reading.
- T3 (01, roadmap): applied. The roadmap names welfare and sale terms, and the appendix range now starts at the research section. This is the one place where a `\ref` changes target: `\ref{sec:robustness}` in that range becomes `\ref{sec:research}`, and the full form of Proposition 3 is named.
- T4 (01, benchmark paragraph repeats the result): applied. The paragraph now goes straight to the entry-ceiling number.
- T5 (01 against Section 6 order): applied, merged with D8. The tour now runs costs, classes, signals, as Section 6 does.
- T6 (06, "different means" against "differ above the reserve"): applied. Section 6.2 uses the introduction's wording; the conditions agree under the class ranking.
- T7 (four wordings of uniqueness): applied through D10. The introduction, the proposition and the conclusion now use one form, and the abstract keeps its plain two-outcome form.
- T8 (04, coexistence opener): applied. The opener ties the comparison at \(r_0\) and \(r_1\) to the benchmark.

Non-hit notes in Section 6 of the prose check (figure-note wording, two scope statements that the status removal took out): no action. The author removed that vocabulary and I do not bring any of it back.

## Sentences that state mathematics and changed wording

Each item keeps its hypotheses, conclusion, quantifiers and numbers. I list them for the final check.

1. 01, main-result paragraph: "the equilibrium outcome is unique" replaces the trading and on-path preparation wording, and the ownership rise now carries the condition on the high class's chance to win, which the benchmark meets.
2. 01, empirical paragraph: the purchase and sale comparison now states both impacts from the price after no order, and the gap is the entry component; the registry share is unchanged.
3. 03, inference: the ceiling passage is two sentences; the conditions \(g_H\ge g_L\) and gross profit at the top posterior below \(c_H\), and the "in or out of equilibrium" scope, are unchanged.
4. 04, Proposition 2 frame: the frame is two "Let" sentences. Every hypothesis in words and displays (H1) to (H3) is unchanged.
5. 04, fixed-information control: the condition is three sentences. Content in full: given the class, the signal tells the challenger nothing more about either value; its own value depends on the signal only through the class; the incumbent's value is independent of the class and the signal; the two values are independent; the cost is independent of the class, both values and the signal.
6. 04, Panel B control: the sentence now states that entry falls by the probability that the cost lies between gross profit at the two strengths, with both registry values unchanged.
7. 04, Proposition 3: the frame uses "Let" and keeps the band citation without the part letter, and part (a) uses "the equilibrium without informed trade" as subject. The interval \([r_A,r_N]\) and part (b) are unchanged.
8. 04, ceiling note: parts (i) and (ii) "hold without the ceiling" replaces "do not use (H3)".
9. 06, classes: "differ above the reserve" replaces "have different means" under the class ranking; the mean-preserving-spread sentence now reads "never lowers gross profit at any belief"; the separation sentence now states the split into a high group and a low group.
10. 07, price access: the added-preparation sentence now ends "so no added preparation lowers net surplus", the nonnegative form in Appendix A.7; Proposition access itself is unchanged.
11. 07, payment rule: "never raises the challenger's profit" and "moves the spread only in the direction of the sign of \(1-2\omega\)" replace the two "weakly" forms; the strictness condition and the \(\omega=1/2\) value are unchanged, and the worked argument moved up without a change to its sentences. The point-mass condition \(0<\ell<\bar r<h\) is untouched.
12. 08, price spread paragraph: the impact definitions moved into the test sentence, with \(P(1)-P(0)\) and \(P(0)-P(-1)\) kept; the component statements and every registry value are unchanged. The entry-floor sentence now says "entry returns to its floor".
13. 09, conclusion: "entry rises with incumbent strength while the investor mixes between a purchase and abstention, and it stays constant once the high class buys for sure" replaces the tail qualifier.

No other sentence that states mathematics changed. In particular, untouched: the gross-return lower bound for a correctly signed order in Section 3.2; the reserves sentences that flat entry needs full informed trade and that only a purchase recruits at both strengths (introduction, Section 7.3, conclusion); the signals scope in Section 6.3; and the zero-order claim under full two-sided trade on \((r_S,r_C]\) in Section 8.

Macro check against `HEAD`: every `\reg{}`, `\label`, `\eqref` and citation in the edited files is preserved with the same count, with three additions only: `\ref{tab:a4-ties}`, `\ref{prop:coexistence}` in the roadmap, and two `\reg{}` values repeated in R3 where the same sentence group already printed them. The single target change is the T3 roadmap range noted above.

## Appendix requests

One request, for D2.

- Location: `slot/manuscript/appendix/A6_robustness.tex`, the paragraph headed "The benchmark B with the accuracies of \(S(B)\)", at the end of that paragraph's item list, before the sentence "Each mixed tuple is unique under rule IM ...".
- Exact text to insert: "At \(r_0\), the investor mixes between trade and abstention after either signal, and it trades with probability \(\reg{p4_b_signal_r0_buy_rate}\). At \(r_1\), it buys with probability one after a favorable signal, and after an unfavorable signal it sells with probability \(\reg{p4_b_signal_r1_sell_rate}\)."
- After that insertion lands, delete from `slot/manuscript/sections/06_robustness.tex` the paragraph that begins "With the accuracies of the signal example, the benchmark has a unique equilibrium at each strength when an indifferent investor may mix over its best orders." and ends "When an investor that is indifferent between abstention and a nonzero order must abstain, neither strength has an equilibrium." Its entry values, mixed tuples and tie-rule facts already stand in that appendix paragraph; the two sentences above carry the only numbers it lacks. Until the insertion lands, the paragraph stays in the main text, so no number is lost at any stage.

## Checks

- Build: `cd slot/manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/ccc_slot_scan/build_polish main.tex` completed. Output: 102 PDF pages in total.
- `grep -E "undefined|multiply" /tmp/ccc_slot_scan/build_polish/main.log`: empty.
- `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py` from the repository root: clean. It reports 21 files scanned, 676 distinct keys used, 0 missing keys, and 0 literal decimals outside `\reg{}`.
- `grep -niE "analytical|computer-assisted|numerical diagnostic" slot/manuscript/main.tex slot/manuscript/sections/*.tex`: empty.
- `git diff --check`: clean. No em dashes and no "we" in the edited text.
- Numerical exercise gate: not run. This pass changes prose only, with no change to any numerical exercise, registry value or derived artifact, so this is a scoped check, not a full release pass.
- Main-text page count: 33 printed pages. The conclusion ends on printed page 33 and the references start on printed page 34; the title and abstract sit on printed page 1.
