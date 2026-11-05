# Prose pass on the A fragments

Each `Axx_name.prose.tex` file sits beside its source fragment.
The header block is unchanged in every file.
No equation, condition, quantifier, assumption, label, tag, cross-reference, citation key, `\NUM` placeholder, or anchor comment changes.
No claim changes status.
Proposition statements keep their wording. Only the prose around them changes.
The original fragments do not change.

Total change: 243 fewer words across the fifteen fragments.
At the manuscript's double spacing that is about one page.
The appendix fragments (A12, A13, A15) supply 87 of those words, about a third of a page.
The six-page growth in Appendix A comes from new proof content: the exactness argument in Proposition 1(c), the nonemptiness construction, and the many-class subsection.
A prose pass cannot recover those pages without deleting proof steps, so it does not try.

## Changes by fragment

### A01_intro_ownership_sentence.prose.tex

- No change. The fragment is one clause and already reads plainly.

### A02_intro_mechanism.prose.tex

- The auction sentence splits in two. Bidding comes first, then the split of value between the two claims.
- "A challenger that wins pays more" becomes "a winning challenger pays more".
- The fixed-gap point and the reallocation point now stand as separate sentences.

### A03_intro_main_result_ownership.prose.tex

- No change. The line is verbatim manuscript text apart from the class wording.

### A04_intro_robustness_line.prose.tex

- The first sentence leads with the reversal. The class conditions follow in the same sentence.
- "Equally likely to fall below the reserve" becomes "equal chances of a value below the reserve". The condition itself is unchanged.

### A05_intro_selective_entry.prose.tex

- The selective-entry sentence splits. The placement claim stands alone, then the definition follows.
- "Paying the entry cost reveals the value" becomes "the entry cost reveals the value".
- Every citation stays with its claim.

### A06_model_2_2_to_2_4.prose.tex

- The risk-neutrality paragraph states each restriction in its own sentence. Tendering and holdout "stay outside the model" in place of "are outside the modeled continuation".
- The class-ranking paragraph names Proposition 1 after the condition, not before it. The selective-entry identification gets its own sentence.
- The normalization paragraph uses one rescale sentence in place of a compound conditional.
- The equilibrium paragraph drops the warning frame ("must not be confused"). The deviation comparison and the cross-economy comparison each keep their full content.

### A07_section3_payoffs_inference_incentives.prose.tex

- Section 3.1 drops one sentence that restates the win/loss split. The payoff formulas and the identity `t+g=θ` already carry that content.
- The slice account after Proposition 1 shortens. Each step remains: the fixed-`R` difference, the slice allocation, the reserve term, and its removal under equal admissibility.
- The price-sufficiency lead loses its contrast frame. The floor point follows as its own sentence.
- The residual paragraph in Section 3.3 uses short sentences. "Cannot identify the class perfectly because of noise demand" becomes "noise demand still hides the class".

### A08_section4_1_proposition2.prose.tex

- The floor paragraph and the slack-low-cost sentence merge into one paragraph. All three uses of the floor remain, in order.
- "Is never negative" becomes "never falls below zero".
- The trading paragraph states the weak-economy bound and its consequence in separate sentences.

### A09_section4_2_benchmark_opening.prose.tex

- No change. Three short sentences, already in the manuscript voice.

### A10_section4_3_point_mass.prose.tex

- No change. The fragment is two sentences and the opening of Proposition 3.

### A11_section5_2_value_classes.prose.tex

- "Needs neither … nor … nor" becomes a plain list of three "no" phrases.
- The class-pair choice and the prior choice now take separate sentences.
- The profit-gap point splits: the gap stays near the full value gap, and the high cost fits inside it.

### A12_appendix_A1_payoffs_pricing.prose.tex

- The appendix opening drops the sentence about definitions. The status list, the benchmark rule, and the Online Appendix inventory remain.
- The proof of Proposition 1 opens with the payoff cases directly. Each case keeps its formula.
- The closing point-mass paragraph states the kernel's scope in one sentence. The Section 6.2 pointer remains.
- Every integral representation, Tonelli step, and the part (c) construction remain in full.

### A13_appendix_A2_trading_main_comparison.prose.tex

- The absolute-continuity passage names its two inputs in separate sentences: absolute continuity of the density, then Fubini's theorem with its bound.
- The road map for Proposition 2 now names the steps instead of "necessity" and "existence" labels.
- "The formulas belong to the point-mass case. The arguments do not." becomes a direct scope statement.
- All six steps, part (iii), and both later propositions remain complete.

### A14_appendix_A3_certificate_scope.prose.tex

- No change. The fragment is one sentence.

### A15_appendix_nonemptiness_and_many_classes.prose.tex

- The opening splits its definitions into single-claim sentences: the region, `Γ(x)`, the differ-above-the-reserve condition, and `u_0`.
- The construction itself is unchanged. Its inequalities carry the argument and admit no shorter prose.

## Points for the reviewers

No item below changes in the prose files. Each item needs a mathematical decision.

1. **Many classes: one measurability step stays compressed (A15).**
   The text passes from "equality forces a constant likelihood ratio" to "the posterior is a measurable function of `T_X`".
   The level-set argument behind that step does not appear.
   The drafter's notes (A00 §5, item 5) record the same gap.

2. **Many classes: the two-group result states sufficient conditions only (A15).**
   The fragment does not claim that its conditions hold on a nonempty set.
   A reader cannot tell from the appendix whether the two-group case has an example.

3. **The slack-low-cost sentence rests on a sketched argument (A08).**
   "Any low cost below `B_F(m(π))` … would give the same orders, prices, and entry" extends a benchmark claim to classes and a general prior.
   The text gives the two inputs (posterior floor, monotone `B`) but no proof pointer.

4. **The general-prior no-trade condition has a numerical check behind it (A13).**
   The condition `e(π)Δ_T max{π,1−π} ≤ k` reads as a direct derivation in the text.
   The drafter's notes record confirmation at two prior values by script.
   The derivation looks complete on its face. The reviewers may still want the residual computation spelled out for `π ≠ 1/2`.

5. **The index `j` does double duty near Proposition 3 (A10, outside these fragments in Appendix A.3).**
   `j` is the quality class throughout the A fragments. The certificate material uses `r_j`, `v_j`, `E_j` for strengths.
   The uses are local. A rename of the certificate index would remove the clash.
