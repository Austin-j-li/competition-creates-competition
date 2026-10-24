# Composer B report: Sections 2 and 3 (the model, and competition and information)

Scope edited: `slot/manuscript/sections/02_model.tex` and
`slot/manuscript/sections/03_competition_information.tex` only. No mathematical
content changed. Proposition 1 keeps its statement verbatim and still prints as
Proposition 1. All five `% STRUCTURE:` comment lines in the two files are gone.
No commit made. No tests written.

## Paragraph-level summary

### Section 2.1, the decision interval (four paragraphs)

- Paragraph 1 joins the situation to its timing condition with "if" and a
  semicolon (Laplace form): a public sale opportunity while the stock trades and
  a further bidder can still come in. The chronology point stays, with the plain
  forward reference to the empirical section on how to date the interval.
- Paragraph 2 merges the prepared-buyer paragraph and the preparation-cost
  paragraph into one. The diligence tasks are one list inside one sentence. The
  closing contrast ("an entry cost, not the price of an optional report") is now
  positive: a buyer that does not prepare cannot bid its expected value and stays
  out; payment reveals the buyer's value and permits a bid.
- Paragraph 3 merges the two knowledge paragraphs. The model's two information
  extremes and the pointers to the signals and research sections stay, joined by
  a semicolon.
- Paragraph 4 keeps "Public incumbent strength is a distribution, not a bid" and
  joins the two record examples and the valuation citation into one sentence.
  The disclosure sentences (Imprivata; competition before public bids) no longer
  own a paragraph; they close this paragraph, with a forward reference to the
  empirical section on how to test whether prices draw buyers into preparation.

### Section 2.2, values, preparation, and the sale

- Normalization sentences stay next to their objects and say once what changes
  and what stays fixed. The sentence on the investor's lack of control rights
  moved to Section 2.3 (see Deletions, item 1).
- Symbols now enter after their meaning in words. The class-difference symbol
  enters as "the probability that a class-j value falls below the reserve is
  G_j(p^-), and D(y) is the difference between the two class distributions",
  with no "Write" opener.
- The class ranking is two sentences of prose (dominance; both supports above
  the reserve) around the numbered display `eq:classes`, then one sentence
  names the class ranking. The next paragraph gives the weakest restriction and
  equal admissibility in joined sentences, names Proposition 1(c) here as its
  one home, and ends with the selective-entry sentence.
- Benchmark, money normalization, preparation-cost draw, independence, and the
  auction paragraphs keep every fact with light joins only (condition joined to
  consequence; no sentence added or dropped beyond punctuation joins).

### Section 2.3, trading: the order slot

- The investor paragraph now also carries the outsider scope: no net position,
  no control rights, cannot acquire the target, with the full-hedge clause kept.
- The five-item numbered slot list is chronological prose (the voice report's
  Sample B, adapted): investor arrival, liquidity arrival with who the
  liquidity traders are, anonymity and independence, then market makers and the
  investor's profit display `eq:profit`. The liquidity symbol for the order
  distribution stays in Appendix A only, as the structure pass left it.
- Seam handled: the bound on the liquidity probability now lives in one
  footnote at its first appearance (only the zero-order posterior bound, and
  through it the ceiling, uses it; the competition and coexistence propositions
  hold for every such probability below one half; pointer to Appendix A.2, where
  the counterexample also sits).
- The two slot numbers lose the "Two numbers summarize" opener. The posterior
  bounds display `eq:bounds` now names a bottom posterior and a top posterior
  in words before the display.
- Seam handled: the order-size footnote now names Euler's number at its first
  use ("where e is Euler's number").
- The six-item timing list is prose after "The sequence is as follows." The
  research pointer reads "before the investor learns the class"; no step
  numbers remain anywhere.

### Section 2.4, equilibrium

- The equilibrium concept now comes first, in one paragraph: what an
  equilibrium specifies, mixing and wrong-signed orders, Bayes at every order,
  competitive prices, the two preparation rules, the investor's payoff display,
  and one pointer to Definition A.1 for the six conditions. Entry after an order
  and the two proceeds objects are glossed in words after the display.
- The payoff notation follows in one paragraph. The two display-only
  definitions (class expectations; gross profit at a belief) are inline now,
  with identical formulas. Gross profit at a belief keeps the guide's pattern
  sentence ("because its value depends on the price only through its class").
- The price paragraph joins the terminal-payoff argument into one "because"
  sentence and keeps display `eq:price` and the ex ante factor sentence.
- The two default tie conventions are one sentence, in words, with no acronyms.
- The two comparisons are two sentences. The sentence about what proofs use is
  deleted from the main text (Appendix request R2 below).
- Outcomes lose the "Two outcomes summarize" opener. The high-class win
  probability leads with its meaning in words and keeps its formula.

### Section 3.1, acquisition profits and target value

- The auction-split paragraph and the adds-up display now form one paragraph;
  the gloss follows. Benchmark displays `eq:payoffs` and `eq:derivatives` are
  untouched.
- The lead-in to Proposition 1 joins the two opposing effects with "while".
  Proposition 1's statement, display `eq:spread`, parts, and strictness
  conditions are verbatim.
- After the proposition, intuition comes first: the slices paragraph (light
  colon join), then one paragraph for the movement of slices, the reserve term,
  its disappearance under the class ranking, and one appendix pointer for the
  proof. The duplicate weakest-restriction sentence is deleted here (Deletion
  item 10); its home is Section 2.2.
- The class-gap identity and the closing spread paragraphs keep their facts
  with "while" and semicolon joins; the subsection still ends on the dependency
  of entry on price information.

### Section 3.2, what the challenger learns from the price

- Opens with the object ("The challenger sees one price"), then the bounds
  argument in causal order: liquidity arrival in each class, likelihood-ratio
  bounds, the posterior interval of `eq:bounds` under every strategy, the three
  full-order posteriors, the belief at a price as an average, and the ceiling
  in positive words ("needs a belief above the top posterior"). The weak
  hypothesis on gross profits is kept exactly.
- The price paragraph runs threshold, entry floor, price formula
  `\eqref{eq:price}`, strict price increase, then the worked step ("Suppose two
  orders have one price"), and ends with preparation following exactly the
  orders that reach the threshold. One appendix pointer closes the paragraph.
- The zero-cost paragraph drops "does three jobs in the proofs" and states the
  same three facts as floors and consequences.

### Section 3.3, informed trading

- The gross-trading-returns display and its bound are untouched. Correct-order
  and wrong-signed comparisons stay in words.
- The intuition paragraph now runs in causal order: market makers price the
  entry response; residual uncertainty survives because a same-direction
  liquidity order is always possible; the return is entry times spread times
  that uncertainty; then the two bounds and their comparison with the trading
  cost.
- The bound-shape paragraph keeps the two identities (they are not in the
  appendix; grep confirms) but leads with the economics: largest at an even
  prior, and the favored class binds because the price already leans toward it.
- Cancellation of no-entry proceeds is one semicolon sentence. The closing
  paragraph keeps the split of the investor's problem, keeps the forward use in
  the coexistence appendix, and adds this subsection's formal pointer to
  Appendix A.2.

## Deleted sentences, with the location that already states the fact

Moves within my two files are marked "in scope"; appendix locations name the
file and the paragraph.

1. Section 2.2: "The investor has no control rights and cannot acquire the
   target." Moved in scope to the investor paragraph of Section 2.3 ("has no
   control rights, and cannot acquire the target"). A related loss of words:
   Section 2.3's "not ownership of the target" after "a normalized small trading
   unit" is gone, since the investor paragraph in the same subsection now says
   the investor cannot acquire the target.
2. Section 2.1: the clause "not the price of an optional report" (contrast
   tail only). No appendix location states this contrast. The positive content
   of the sentence (entry cost; no bid without payment; payment reveals the
   value) is stated in the same paragraph and again in Section 2.2. No model
   fact is lost; the deleted words were a contrast, not a condition.
3. Section 2.3: the duplicate liquidity paragraph as a standalone paragraph.
   Its sentences survive merged in scope (shareholder sale, outside purchase,
   empty opportunity, exogenous motive in the slot paragraph; absorption at the
   order's price and market-maker inventory in the market-maker paragraph).
   List items of the old slot and timing enumerations likewise survive as
   prose in the same subsection; "before step (2)" is now "before the investor
   learns the class", which matches the research section's own opening.
4. Section 2.4: the tail "and no off-path belief enters" in the Bayes sentence.
   Appendix: `appendix/A1_payoffs.tex`, paragraph after Definition A.1 ("Every
   order therefore occurs with positive probability in both classes. Bayes' rule
   defines the posterior after every order, and no off-path belief enters the
   definition."). The same point also stays in scope in the order-size footnote
   of Section 2.3.
5. Section 2.4: "Two indifferences remain: an investor can be indifferent among
   orders, and a high-cost challenger can be indifferent about preparation."
   Appendix: `appendix/A1_payoffs.tex`, same paragraph ("The two indifferences
   in (E3) and (E5) ...").
6. Section 2.4: "The equilibrium concept lets an indifferent investor mix over
   its best orders in any proportion. This is the standard best-response
   condition, and I call it rule IM." The convention itself stays in the one
   default sentence of Section 2.4. "Any mixture" is in
   `appendix/A2_beliefs_trading.tex`, proof of Lemma A.3, part (b); the
   best-response form is condition (E5) of Definition A.1 in
   `appendix/A1_payoffs.tex`. The acronym itself needs Appendix request R1.
7. Section 2.4: "An indifferent high-cost challenger prepares, and I call this
   rule C1." The convention stays in the default sentence; at equality,
   Definition A.1, condition (E3), in `appendix/A1_payoffs.tex` applies the
   challenger's tie rule. The acronym needs Appendix request R1.
8. Section 2.4: "The results use IM and C1." plus the alternatives sentence
   (the two alternatives stated, with the tie-dependence table reference).
   Appendix: `appendix/A4_coexistence.tex`, paragraph "Other tie rules" (the
   two alternatives, and "states each place on the benchmark path where" they
   change a conclusion) with its tie-dependence table; also
   `appendix/A1_payoffs.tex` after Definition A.1.
9. Section 2.4: "Proofs use the first comparison to test a candidate
   equilibrium and the second to compare outcomes." No appendix sentence states
   this verbatim (grep of `appendix/` for the comparison language is empty).
   Deleted under the style guide (proof talk leaves the main text; guide
   Section 4, fourth point). It must land through Appendix request R2.
   Neighbouring appendix text: the deviation convention in
   `appendix/A2_beliefs_trading.tex`, "Conventions for Appendices A.2 to A.9",
   and the check-each-condition sentence at the head of
   `appendix/A1_payoffs.tex`.
10. Section 3.1: "It also gives, in Proposition 1(c), the weakest restriction
    under which the spread rises for every strengthening." Stated in scope in
    Section 2.2 (weakest restriction named as Proposition 1(c), with the exact
    no-atom conditions), and in `appendix/A1_payoffs.tex`, the named statement
    "Proposition 1(c) (the weakest restriction; analytical)".
11. Section 3.2 opener: "This section states what that price can reveal under
    every investor strategy, and what it reveals in equilibrium." This was a
    meta sentence; its content is the two paragraphs that follow. Appendix
    home: `appendix/A2_beliefs_trading.tex`, opening paragraph ("states and
    proves the results behind" Sections 3.2 and 3.3; "Each result holds for
    every order profile, in or out of equilibrium.").
12. Label sentences with no fact of their own, content retained after them:
    "Two restrictions rank the classes." (2.2), "Two numbers summarize the
    slot." (2.3), "Two comparisons recur." and "Two outcomes summarize an
    equilibrium." (2.4), "The zero-cost challenger does three jobs in the
    proofs." (3.2), "The bound has a simple form." (3.3). No appendix copy is
    needed; each following sentence is unchanged in content.

Nothing else was deleted. In particular, both `\reg` macros of Section 2
(`prim_pi`, `prim_ell`) survive; Section 3 has none. Every `\label` of the two
files survives (10 in Section 2, 8 in Section 3, checked against HEAD). Every
citation key survives. Two display-only definitions in Section 2.4 became
inline formulas, word for word; display `eq:profit` ends with a full stop
instead of a comma, since the sentence now ends at the display.

## Appendix requests

R1. Introduce the tie-rule acronyms in the appendix, since Section 2.4 now
states the defaults in words only.
  - (a) `appendix/A1_payoffs.tex`, paragraph after Definition A.1. Current
    text: "The two indifferences in (E3) and (E5) follow rules IM and C1 of
    Section~\ref{sec:equilibrium}; Appendix~\ref{app:coexistence} states the
    alternatives I0 and CM."
    Proposed exact text: "The two indifferences in (E3) and (E5) follow the
    default tie conventions of Section~\ref{sec:equilibrium}: an indifferent
    investor may mix over its best orders (rule IM), and an indifferent
    high-cost challenger prepares (rule C1).
    Appendix~\ref{app:coexistence} states the alternatives I0 and CM."
  - (b) `appendix/A4_coexistence.tex`, paragraph "Other tie rules", first
    sentence. Current text: "The results use rules IM and C1 of
    Section~\ref{sec:equilibrium}."
    Proposed exact text: "The results use the default rules IM and C1."
    (Coherent once R1(a) lands; harmless to skip if the coordinator prefers
    the cross-reference kept.)

R2. Receive the proof-comparison sentence deleted from Section 2.4.
  Location: `appendix/A2_beliefs_trading.tex`, the item list under
  "Conventions for Appendices A.2 to A.9", as a new item after the deviation
  item ("A deviation by the investor holds the candidate's price function ...
  fixed.").
  Proposed exact text: "\item Proofs use the deviation comparison to test a
  candidate equilibrium and re-solve the equilibrium in each economy to
  compare outcomes across economies."

No other appendix change is needed by my rewrite. The liquidity-probability
footnote in Section 2.3 cites the existing paragraph "Where the bound enters"
at the end of `appendix/A2_beliefs_trading.tex`, which already states the
zero-order role, the every-below-one-half scope, and (in the proof of Lemma
A.1, part (c)) the counterexample.

## Term choices for the unification pass

- Top and bottom posteriors are named at `eq:bounds` in Section 2.3 ("between
  a bottom posterior and a top posterior"). Section 3.2 uses "the top
  posterior" for the ceiling.
- No tie acronym appears in Sections 2-3. The defaults read: "An indifferent
  investor may mix over its best orders, and an indifferent high-cost
  challenger prepares." Any acronym that survives elsewhere in the main text
  now has no Section 2.4 definition to lean on; per shared vocabulary it must
  be words, or a table or figure note that explains it. The appendix home for
  the names is R1.
- "The class ranking" with `\eqref{eq:classes}` is used at every mention in my
  files. Proposition 1(c) is named once, in Section 2.2; Section 3.1 no longer
  names it.
- The liquidity-probability bound's one home is the new footnote in Section
  2.3. Hypothesis uses of the bound in later proposition statements are for the
  unification pass to judge; my files state the scope nowhere else.
- Section 2.4 order changed: equilibrium concept first, payoff notation second.
  The proceeds objects are glossed in words right after the payoff display and
  defined in the next paragraph. Nothing outside my files refers to the old
  order, but the introduction should not assume the notation precedes the
  concept.
- My `\ref{tab:a4-ties}` and `\ref{app:coexistence}` mentions in Section 2.4
  are gone (the table is still cited inside Appendix A.4 itself). I added
  references to Propositions 2 and 3 (by `\ref`) in the Section 2.3 footnote;
  both labels exist in the concurrent Section 4 file.
- Section 3.3 ends with two appendix sentences: the retained forward-use
  sentence (coexistence appendix) and the formal pointer (beliefs appendix).
  If "one appendix pointer per subsection" is enforced as a literal count, the
  forward-use sentence is the one to convert to a section reference; I kept it
  because the fact it states is about the appendix list itself.
- The order-size footnote now introduces Euler's number, so the later sentence
  that introduces it in Section 4.2 may read as a second introduction; the
  Section 4 composer and the unification pass should check that seam.
- The disclosure paragraph's last sentence ("states how to test whether prices
  draw buyers into that preparation stage", by `\ref`) should be checked
  against the empirical section's final wording.

## Check results

- Build: `cd slot/manuscript && latexmk -pdf -interaction=nonstopmode
  -halt-on-error -outdir=/tmp/ccc_slot_scan/build_compose_B main.tex` exited 0,
  103 pages. Run twice; the second run (fresh PDF) already included the other
  composers' concurrent edits to Sections 1, 4, 5, 7, 8, 9 and `main.tex`.
  No error came from outside my scope.
- Log: `grep -E "undefined|multiply"
  /tmp/ccc_slot_scan/build_compose_B/main.log` printed nothing.
- Number scan, from the repository root:
  `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`
  reported 21 files scanned, 676 distinct keys used, missing keys 0, literal
  decimals outside `\reg` 0.
- Preservation checks against HEAD: identical label sets, `\reg` sets, and
  citation-key multisets in both files; display mathematics identical except
  the two inlined definitions of Section 2.4 (formulas unchanged inline) and
  the terminal punctuation of `eq:profit`. Proposition 1 prints as number 1;
  the class ranking prints as display (1); the two new footnotes print in
  place (read on PDF pages 8-9, and Sections 2-3 read in full from the PDF
  text).
- Not run: the numerical exercise pipeline. The change is prose-only; no
  number, key, or result changed, and the number scan above covers the
  manuscript's numerical surface.
