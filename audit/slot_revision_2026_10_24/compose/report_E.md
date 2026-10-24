# Compose report E: Sections 7 and 8

Scope: `slot/manuscript/sections/07_welfare.tex` and `slot/manuscript/sections/08_empirical.tex`. I edited no other
file. I changed no mathematical content. Every `\reg{}` macro and every `\label` of both files is intact (see
Checks). Neither file held a `% STRUCTURE:` line before or after my edit.

## 1. What I changed, paragraph by paragraph

### Section 7.1, Access to prices

- Paragraph 1 joins the comparison into two sentences ("Hold the incumbent at \(F_1\) and compare ..."). The claim
  and the Proposition reference stay. One sentence now states that Appendix A.7 states the results of this section in
  full, with their status. That is the section's one status pointer.
- Paragraph 2 joins "trading costs coincide" to its reason with "so", and joins the last two sentences with a
  semicolon. Facts are unchanged.
- Paragraph 3 (benchmark gains) only joins "and net surplus rises by ...". All four `\reg` values stay.
- Paragraph 4 drops "informed" before "investor" ("the investor", per shared vocabulary). "Suppose that one order
  unit is ..." is now an "If ..." clause inside its consequence sentence. The \(V_T\) contrast stays verbatim.
- The old last paragraph is now two paragraphs, per defensive row 54. The first states the recruitment region in
  positive form ("Inside the recruitment region ..., price access adds preparation"). It is the section's one scope
  condition. "Keep the strong benchmark and set ..." is now "with the strong benchmark and \(c_H=...\)". The second
  paragraph holds the dividend sentence alone. All values stay.

### Section 7.2, The payment rule

- The open trading equilibrium now stands once, with the scope sentence at the start: "Proposition A.9 isolates this
  dependence at the payment stage, in a verifiable-value institution with zero reserve; the trading and preparation
  equilibrium under this rule is open." This follows the guide, Section 4, fifth point.
- "at \(\omega=1/2\) the spread does not depend on the incumbent" is now the positive exact form from the appendix
  statement: "the spread equals \((h-\ell)/2\) at every incumbent distribution" (defensive row 55).
- The benchmark paragraph (the \(\reg{pay_gap_coef}\) value, the case \(\omega=0\), the Bulow and Klemperer contrast) now
  comes before the worked argument. The subsection therefore ends on the payment-sensitivity argument ("To see why,
  take \(R>\ell\) ... Competition widens the difference exactly when the first sensitivity exceeds the second.").
  No sentence was added or lost in the swap.

### Section 7.3, Reserves

- The two text paragraphs and the table are unchanged in content. Two small joins: "entry is flat ..., and strict
  deterrence needs ..."; "... at both \(r_0\) and \(r_1\), while this reserve raises expected proceeds ...".
- Table note: "Benchmark \(B\)" is now "The benchmark" (shared vocabulary). "Values are computer-assisted" stays.
  That note carries the status of the reserves numbers, once.
- The last paragraph drops the two endpoint formulas and the section-ending "open" (see Section 2 below). Section 7
  now ends on the strict-deterrence interval.

### Section 8, opening paragraph

- "This section states them" is now "I state them". The appendix sentence now reads "states each result in full,
  with its status, and proves it".
- \(r_S\) now enters in words as "the sale threshold", with its exact equation kept:
  \(\rho\DT(r)m(1/2)=k\). I wrote \(m(1/2)\) for the old bare \(m\), since the prior in this section is \(1/2\).
- \(r_C\) is named "the entry ceiling". The symbol \(\vartheta\) is gone: "the informed share of nonzero orders is
  \(u/(2+u)\)". The symbol stays in Appendix A.8 (line 8).

### Section 8, Entry and incumbent strength

- The predictions now come first, in order: price reaches the buyer (rise, with
  \(\reg{entry_jump_B}\)); price does not reach the buyer ("can only lower it", positive form); strong enough bidder
  (floor, informative price). The source sentence follows: Proposition 2 gives the first and third comparisons,
  Proposition A.3 the second.
- The fixed-information condition of the control is now in words, in the last sentence of the paragraph. It says
  that the joint law of the class and the signal, the class value laws and the cost law are the same at both
  strengths; that, given the class and the signal, the two values draw independently from their own laws; and that
  the cost is independent of the class, the two values and the signal. The tensor-product formula left the main text
  (see Section 2).

### Section 8, The spread and its entry component

- The prediction now opens the paragraph: the purchase impact exceeds the sale impact exactly when a purchase
  recruits, and the test needs no auction objects. The definition of the spread and its two components follow. The
  class component is written as \(\rho\DT\) times the informed share. The last clause states that the whole entry
  component sits in the purchase impact. That is part (ii) of the cited proposition in words.
- The numbers paragraph is unchanged except that \(r_C\) is named "the entry ceiling". The tag "(computer-assisted)"
  stays on the benchmark spread numbers. It is the one status tag in this section's text.

### Section 8, The informed share

- The paragraph now opens "Prices separate slots that order counts cannot" (defensive row 60). The old opener
  "Order frequencies alone leave the slot open" is gone. Its substance stays in the same paragraph: the order law
  depends on the slot only through the volume, and the allowed shares form a non-trivial interval.
- "under rule IM" and "closed" left the interval sentence, and the endpoint sentence left the section (see
  Section 2). The interval holds under the paper's default tie conventions, so a reader loses no testable content.
- The duplicate "Prices therefore separate slots that counts cannot" at the end of the second paragraph is gone.
  The sentence survives once, as the opener.

### Section 8, Winners and Announcements

- Winners now opens with the prediction ("Orders predict the winner even where they no longer predict entry"),
  then the two gaps and the two covariances, then the posterior fact and its proposition. All values stay.
- Announcements now opens with the prediction inside its condition ("If a public event after the price reveals only
  whether the challenger prepared, the mean price change in a sample of preparation reports alone is positive").
  The zero-mean sentence follows it. "Below the ceiling" is now "Below the entry ceiling \(r_C\)". All values stay.

### Section 8, Two clusters and Measurement

- The prediction now opens the paragraph: "At one public strength in the range \((r_F,r_N)\) ..., processes can
  form two clusters." The two patterns follow, with all values. The two old paragraphs are now one. The paragraph
  ends "Which equilibrium a process selects is open." Selection stays once, where it limits a test. The rule names
  and the third pattern under the alternative rule left the section (see Section 2).
- Measurement has only joins: one semicolon in the call-auction sentences. The sentence on samples of first executed
  trades stays verbatim (defensive row 62, keep).

## 2. Deleted sentences, with the appendix location that already states the fact

1. 07, Reserves, last sentence: "The seller's choice of a reserve with the whole continuation retained is open."
   Appendix: `A7_welfare.tex`, closing paragraph (lines 243–244): "A selection of the equilibrium at every reserve,
   and the seller's optimal reserve, are outside these results." The conclusion also states it as the next step
   (`09_conclusion.tex`, line 21, pre-compose text), and the guide assigns it there.
2. 07, Reserves, endpoint formulas: "\(p_H\approx\)" and "\(h-c_H/M\approx\)" in "Strict deterrence holds for
   reserves between ...". The two `\reg` values stay in the main text. The formulas are at `A7_welfare.tex`,
   lines 221–223: \(p_H=\sqrt{2r_1(h-c_H/M)-r_1^2}\) and the weak upper profit at \(h-c_H/M\), with the same
   `\reg` macros. The symbol \(p_H\) had no main-text definition.
3. 08, Entry: "The control requires \(\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i\) and an independent cost law."
   The condition is now in words in the same paragraph. The formula is at `A6_robustness.tex`, Proposition
   `prop:control` (lines 9–12).
4. 08, The informed share: "At the upper end the low-class sale earns exactly zero, so strict incentives, or rule
   I0, exclude this endpoint." Appendix: `A8_empirical.tex`, lines 136–140 (zero sale at the upper share; rule IM
   admits it; rule I0 excludes it). The words "under rule IM" and "closed" in the interval sentence go with it:
   line 141 states the closed interval under rule IM.
5. 08, Two clusters: "Under rule CM, the threshold equilibrium of Appendix~\ref{app:coexistence} adds a third
   pattern." Appendix: `A8_empirical.tex`, lines 245–249, with its values. The exhaustive "two equilibria under
   rule C1" in the same paragraph is at lines 239–241 ("exactly two equilibria under rules IM and C1"), and in
   Section `sec:coexistence`, which my text still cites. My text keeps the existence prediction, which does not
   depend on the tie rule.

Not deletions: "The trading and preparation equilibrium under the bargaining rule is open" moved within 7.2, from
the end to the start. "Prices therefore separate slots that counts cannot" moved within Section 8, from the end of
the informed-share example to the paragraph opener. "Order frequencies alone leave the slot open" has no appendix
home as a sentence; its fact (counts do not pin down the slot) stays in the same main-text paragraph, as the
volume-only dependence and the width of the allowed interval.

## 3. Appendix requests

One request. I made no appendix edit.

- `A8_empirical.tex`, paragraph "Certificates" (line 251). The benchmark spread numbers of Section 8 carry a
  "(computer-assisted)" tag in the main text, but Appendix A.8 states no status for its benchmark values (structure
  report, Section 5, records this exception). Proposed exact change: replace the first sentence "All values of this
  subsection come from the script \nolinkurl{P5_observables/p5_observables.py}." with "All benchmark values of this
  subsection are computer-assisted. They come from the script \nolinkurl{P5_observables/p5_observables.py}."

## 4. Term choices for the unification pass

- "the sale threshold" names \(r_S\) at its entry in Section 8, with \(m(1/2)\) written out. If Section 4 now uses
  another name for \(r_S\), align the two.
- "the entry ceiling" names \(r_C\) at all three Section 8 uses. "the informed share" replaces \(\vartheta\)
  throughout Section 8.
- Table 5's note now says "The benchmark", not "Benchmark \(B\)". Other main-text table notes may still differ.
- Section 8 keeps the institutional pair "a stronger prepared bidder" / "the further buyer" in the Entry paragraph
  and in Measurement. The model-facing paragraphs keep "the challenger" and "the incumbent". Section 7 uses "the
  investor" without "informed" in the transfer sentence.
- The control condition in words uses "the challenger's class and its signal". Align it with the control wording
  that Section 4 adopts.
- Status: each of my sections opens with one sentence that points to its appendix "in full, with its status".
  Section 7 carries one more status location, the Table 5 note. Section 8 carries one tag in the text, on the
  benchmark spread numbers. I added no "analytical" tags to running text; the appendix titles carry them. The
  guide, Section 4, second point, asks for status once per cluster in the reading path. If the unification pass
  reads that as a tag in each first reporting sentence, Sections 5 to 8 need the same treatment at once.
- I kept \(z\) for the trade scale in 7.1. It matches `A7_welfare.tex`, line 72. The collision with the research
  intensity \(z\) sits in Section 5, which is not mine.

## 5. Checks

- `\reg` multisets, old against new, per file: identical for both files. `\label` sets: identical. References and
  citations: identical except Section 7 gains one `\ref{app:welfare}` (the status pointer) and Section 8 loses one
  `\ref{app:coexistence}` (the deleted third-pattern sentence). Both labels still resolve.
- `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`: 21 files, 676 keys, missing
  keys 0, literal decimals outside `\reg` 0.
- In-tree build, `latexmk -pdf -interaction=nonstopmode -halt-on-error
  -outdir=/tmp/ccc_slot_scan/build_compose_E main.tex`: fails, twice (once at once, once after a 90-second wait).
  The first error is outside my scope, in the concurrently edited `04_equilibrium_results.tex`, log line: "!
  LaTeX Error: Bad math environment delimiter" at its line 168, "...st margin of Proposition~\ref{prop:ccc}\)".
  Per the brief, I report it and do not fix it. `git status` confirms that file is mid-edit by another composer.
- Because the shared tree cannot build, I verified my scope in an isolated copy: `/tmp/ccc_slot_scan/isolated_E`,
  the current tree with only `04_equilibrium_results.tex` restored from HEAD inside the copy, and my two files as
  submitted. `latexmk` exits 0 and produces the PDF. `grep -E "undefined|multiply"` on its log gives 0 lines, and
  no reference or citation warning remains. I read the rendered Sections 7 and 8 (pages 29–32 of that build):
  numbers print through `\reg`, cross-references resolve (Propositions A.8 to A.14, Table 5, Sections 3.3, 4.2,
  4.3, 5), and the two sections end on the deterrence interval and on Measurement, with no "open" at either end.
- Style scan of my two files: no em dash, no "not only", no "crucial/pivotal/showcase/underscore/delve/highlight",
  no typed decimal (the scan's only hit is the pre-existing `0.92\linewidth` in Table 5). No tie-rule acronym
  (IM, I0, C1, CM) and no \(\vartheta\) remains in either file.
