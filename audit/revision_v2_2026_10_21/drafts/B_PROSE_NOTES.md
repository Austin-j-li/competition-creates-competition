# Prose pass on the B fragments

Each `Bxx_name.prose.tex` file sits beside its source fragment.
The header block is unchanged in every file.
No equation, condition, quantifier, label, cross-reference, citation key, or `\NUM` placeholder changes.
No claim changes status.
In particular, the common-variance comparison in B02 remains a numerical diagnostic.
The statement of Proposition A.5 in B02 and the lemma statement in B03 keep their wording.
Only the prose around them changes.
The original fragments do not change.

## Changes by fragment

### B01_main_noise.prose.tex

- The one-sentence paragraph on the unattained supremum joins the paragraph that defines it.
- "Contain" becomes "denote" for the class, and "gives" becomes "yields" for the score bound.
- The Gaussian sentence splits into two sentences, one for the score bound and one for the posterior bounds.
- The figure paragraph states the two probability claims in separate sentences.
- The last two claims now stand as separate sentences: the Laplace experiment is more informative, and informativeness does not order entry.
- All four numbers and the commented optional sentence are unchanged.

### B02_main_class_noise.prose.tex

- The proposition statement is unchanged, word for word.
- Compound proof sentences split at their logical joints.
  Examples: the bound `f(z) <= L/2`, the density-versus-entry differentiation, and the constant-likelihood-ratio step.
- "Obeys" becomes "satisfies", and "contains" replaces "include" for the other class members.
- The common-variance sentence loses the repeated word "comparison" in its first clause.
  The next sentence still names it a numerical diagnostic.
- "Concerns" becomes "turns on" in the final sentence.
- Every proof step remains, in the same order.

### B03_oa_laplace_extreme.prose.tex

- The lemma statement is unchanged, word for word.
- The ROC definition splits into two sentences.
- Semicolon chains in proofs (ii) and (iii) split into single-claim sentences.
- The closing scope sentences state directly what part (ii) does not assert and what part (iii) supplies.
- "The density in the paper" becomes "the logistic density in the paper" in proof (iii).
- Every proof step in (i), (ii), and (iii) remains.

### B04_oa_c5_instruction.prose.tex

- Edits stay minimal by design, because the fragment is a set of instructions.
- Articles now read "the benchmark strong strength" and "the tie convention".
- "Form 401 points" becomes "take 401 points".
- "Rather than unstable logarithms" becomes "not unstable logarithms".
- The two prohibitions keep their imperative form: do not claim equal variance, and do not infer an entry order.

### B05_oa_quality_scope.prose.tex

- Two opening sentences split, so observation of the class and revelation of the value stand apart.
- "Give integrable payoffs" becomes "imply integrable auction payoffs".
- Item 2 splits the entry and ownership formulas into separate sentences.
- Item 3 uses "not `J_H = J_L`" in place of "rather than".
- Item 4 drops the repeated "still" and splits the list of arguments that carry over.
  The final scope sentence of item 4 is unchanged.
  It states a real limit on the note, so the pass keeps it.
- Item 5 and the closing paragraph split at the semicolons.
  Each fact now has its own sentence.

## Points for the reviewers

No item below changes in the prose files.
Each item needs a mathematical decision, not a prose edit.

1. **The symbol `\pi` has two meanings inside B03.**
   In proof (ii) it is the class prior, in the posterior call formula.
   In proof (iii) it is the circle constant, in `\pi bt/\sinh(\pi bt)`.
   The fragment header records the clash, but the printed text does not.
   A reader meets both meanings within one lemma.

2. **The class `\mathcal C_L` has no location condition, but the tail claim needs one.**
   B01, B02, and B03 define the class by positivity and the score bound alone.
   Part (i) of the B03 lemma assumes median zero.
   The B01 sentence on thinnest tails "about the median" therefore rests on a restriction that the main text never states.
   Either the class needs a centering condition, or the sentence needs the restriction in words.

3. **The price comparison in B03 states no price-construction hypotheses.**
   Parts (ii) and (iii) pass from flow experiments to price experiments by price sufficiency.
   B02 obtains sufficiency at full orders from a price that increases strictly in the posterior, under its maintained conditions.
   The B03 lemma states the price comparison at every pure order profile without those conditions.
   The B01 sentence on "the most informative price at every pure order profile" has the same gap.
   The reviewers should check which standing assumptions close it.

4. **"Part (iii)" in B02 has no clear antecedent.**
   Proposition A.5 as printed has no numbered parts.
   The statement and the proof both cite "part (iii)".
   The likely target is Proposition 2, part (iii).
   The prose pass does not guess, because the wrong guess changes the claim.

5. **The nonemptiness and ownership paragraph in B02 compresses a joint choice.**
   The proof fixes a threshold at a continuity point, then moves the two incumbent strengths close together.
   The threshold, the entry probabilities, and the cost window all move with the strong strength and with `c_H`.
   The paragraph does not spell out the single choice that keeps all strict inequalities at once.
   The referenced nonemptiness argument may supply it.
   The phrase "remaining primitives" in the statement also leaves the open set's coordinates unnamed.

6. **Two smaller compressions deserve a check.**
   In B03 proof (i), one sentence passes from equality in the integrated tail bound to the full right tail.
   The step from an almost-everywhere identity to every point rests on continuity, which the text names only for the value at `t`.
   In B02, the essential supremum names no base measure.
   Lebesgue measure follows from the next use, and continuity of the posterior makes the essential supremum a supremum.
   Neither point looks wrong.
   Both ask the reader to fill a step that the surrounding proofs usually state.
