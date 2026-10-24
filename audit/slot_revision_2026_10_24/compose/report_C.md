# Report C: Section 4, equilibrium results

Scope file: `slot/manuscript/sections/04_equilibrium_results.tex`. I edited only this file.
No hypothesis, conclusion, number or label changed. All five `% STRUCTURE:` lines in the file
are gone.

## What I changed, paragraph by paragraph

**Lead-in to Proposition 2.** One paragraph in plain words: weak incumbent, strong incumbent,
very strong incumbent, joined by semicolons, with the entry and price outcome in each economy.
The notation sentence for \(F_0,F_1,F_2\) stands last, directly before the statement.

**Proposition 2 statement.** One "Let ... and suppose that" frame now states the three
hypotheses in words (high cost between gross profit at the prior and at the top posterior;
trading cost between the two spreads; gross profit at the top posterior against \(F_2\) short
of the high cost), then the tagged (H1)--(H3) displays, unchanged. Parts (i)--(iii) state
outcomes in words (who trades, posteriors after a sale, no order and a purchase, who prepares,
entry and ownership). The formulas that words cannot carry stay: the price in (i), entry and
entry given class \(H\) in (ii), and the if-and-only-if ownership condition. Part heads now read
"the weak incumbent", "the strong incumbent", "the very strong incumbent".

**Discussion of Proposition 2.** The intuition now comes first. The first paragraph reads the
hypotheses as decisions, with the name beside each tag at first use: the high-cost window (H1)
through acquisition profit, the trading-cost window (H2) through the return to a correct order
against its cost, and the ceiling (H3) through the top posterior. The second paragraph states
when the window is nonempty in words first (competition widens the target-payoff spread
enough), then as the ratio, then the open set. The third paragraph states the ownership
sufficient condition in words first (the stronger incumbent leaves the high class a good chance
to win, and the high class places a purchase more often than not), with the two formulas after
the words. The fourth paragraph closes the rise-and-fall pattern at the very strong incumbent.
The discussion ends with the appendix pointer and one plain sentence on tie independence:
every comparison is strict, so the unique outcome is the same however ties are broken (guide
Section 4, first point). The tie paragraph no longer stands directly after the proposition.

**Benchmark opening.** The benchmark primitives and the slot primitives now read as two plain
paragraphs. "The benchmark, which I call \(B\)" is gone; the text says "the benchmark"
throughout. Euler's number, the exact decimal for \(\beta\), unrounded \(\lambda\), and interval
arithmetic all stay, with the pointer to Appendix A.9.

**Payoffs and the admissible region.** The table paragraph states the pattern first (gross
profit at the prior falls, the spread rises), then the entry and ownership numbers. The
admissible region reads as a result with no label sentence: Proposition `prop:region` gives it,
the band follows in thresholds and in priors, and one sentence says what fails below and above
the band. The band-width paragraph keeps the positive reason: both ends are preparation
thresholds, and the threshold rises slowly because the expected payment rises by less than one
half per unit of strength. The margin paragraphs are now one paragraph that states the positive
facts: the ceiling (H3) holds at every strength in \((r_C,h)\), parts (i) and (ii) do not use
(H3), and Table `tab:margins` records every margin. Distances to the boundary stay in
Table `tab:region`, in the notes to Figure `fig:beliefs`, and in Appendix A.9.

**The two controls.** The fixed-information control now states its condition in words: the
experiment fixes the class and signal laws, the class value laws and the cost law; the
challenger's signal tells it nothing about the incumbent's value beyond what the class tells
it; the two values are independent given the class and the signal; and the cost is independent
of the class, both values and the signal. Proposition `prop:control` is named as the formal
condition. The conclusion is in positive form: at fixed information a stronger incumbent can
only lower entry, and entry falls by exactly the crossing probability. "Under rule C1" and the
product-law formula left the main text. The slot paragraph keeps the fixed objects and the same
posterior fact, with a pointer to Appendix `app:beliefs` and no lemma part letter. Panel B
reads as "entry stays constant, then falls once the ceiling binds"; Panel C ends the subsection
on the joint conclusion of the two controls.

**Coexistence.** The subsection opens with coexistence as a result between \(r_0\) and \(r_1\).
The strengths paragraph defines in words only what the main text uses: the start of coexistence
\(r_A\), the start of full purchases \(r_F\), the end of no informed trade \(r_N\), and the entry
ceiling \(r_C\) from Section `sec:benchmark` (guide Section 4, third point). Proposition 3 keeps
its short form; part (b) now reads "rises strictly and then stays constant". The method sentence
after it stays as a proof idea (exact Sturm counts; the rest analytical). The values paragraph
keeps every `\reg` value, with "entry on the informative branch" in place of "on R". The intuition
paragraphs keep their arguments in joined form: no informed trade survives to \(r_N\) because a
unit order earns \(\rho\DT/2<k\); entry rises strictly while the high class mixes because the
purchase rate adjusts, and stays constant from \(r_F\); above \(r_N\) the investor can mix in both
directions without recruitment until \(r_J\). The other-priors paragraph keeps its three prior
values and its two boundary reasons, with the pointer to Corollary `prop:priors`.

**Figure 2 notes.** I checked the figure file itself. `figures/coexistence.pdf` prints all six
strengths (\(r_A,r_F,r_N,r_J,r_S,r_C\)) and the five pattern labels with verbal glosses ("F:
full purchase", "R: mixed purchase that recruits", "N: no informed trade", "Q: mixed orders at
the floor", "T: threshold branch (rule CM)"). The notes therefore keep \(r_J\) and \(r_S\), name
each pattern in words with its figure letter, state the default tie conventions in words (an
indifferent investor may mix over its best orders; an indifferent high-cost challenger prepares),
and describe the dashed threshold branch in words (an equilibrium only when an indifferent
high-cost challenger may prepare with any probability). No tie acronym (IM, I0, C1, CM) and no
bare form letter remains anywhere in Section 4 outside those figure-label references.

Tables `tab:payoffs` and `tab:region` and their notes are otherwise unchanged. In the notes to
Table `tab:outcomes` and Figure `fig:coexistence`, "Benchmark \(B\)" became "the benchmark";
in the notes to Figure `fig:beliefs`, "the ceiling" became "the entry ceiling".

## Deleted sentences, with the appendix location that already states each fact

1. "Every investor comparison in the proof is strict, and every equilibrium posterior lies
   strictly on one side of the threshold. No tie rule is therefore used, and the same unique
   outcome holds under all four pairs of tie rules." Appendix A.3, Step 6 "tie rules"
   (`appendix/A3_proposition2.tex`, proof of Proposition 2). One plain sentence on tie
   independence stays at the end of the Section 4.1 discussion.
2. "Appendix ... states the three equilibrium tuples and checks each condition of
   Definition `def:equilibrium` against them." The tuples and the (E1)--(E6) checks are Steps
   1--5 of the same proof in Appendix A.3. A pointer sentence stays at the end of the discussion.
3. "Appendix ... shows that the proof uses each hypothesis once and that (H1) cannot be weakened
   to \(B_{F_1}(\pi)<c_H\)." Appendix A.3, paragraph "Each hypothesis is used once" and the
   paragraph after it ("The weaker condition \(B_1(\pi)<c_H\) cannot replace
   \(B_0(\pi)<c_H\)") in `appendix/A3_proposition2.tex`.
4. "The admissible region is a result." and "The band is exact." Label sentences with no fact of
   their own. Exactness stands in Proposition `prop:region` (Appendix A.3) and in the notes to
   Table `tab:region` ("the exact open set").
5. "At the lower end \(u=\reg{u_lo_frac}\), the conclusions still hold under rule C1, but under
   rule CM entry at \(r_1\) can stay at \(\rho\)." Proposition `prop:region` in Appendix A.3
   (`appendix/A3_proposition2.tex`: "At \(u=\reg{u_lo_frac}\) ... Rule C1 gives every conclusion
   of Proposition `prop:ccc`. Under rule CM, entry after a purchase at \(r_1\) can take any
   value ..."), and again in its proof. The macro `\reg{u_lo_frac}` still prints in Section 4.2.
6. The three distance sentences at the upper margin ("the benchmark top posterior lies
   \(\reg{margin_return_post_B}\) below \(\tau(r_2)\); in cost units
   \(c_H-B_{r_2}(M(1/2))=\reg{margin_return_B}\); \(r_2\) lies \(\reg{gap_r2_rC_B}\) above the
   ceiling"). The three values print in Table `tab:margins`, Appendix A.9
   (`appendix/A9_parameters.tex`: the (H3) rows and the order row \(r_C<r_2\)).
   `\reg{margin_return_post_B}` also still prints twice in Section 4.2 (Table `tab:region` and
   the notes to Figure `fig:beliefs`). Two interpretive claims of that paragraph (the margin
   depends only on the top posterior and the place of \(r_2\); in cost units it is the smallest
   margin) do not print in the appendix, so I kept them in one compressed main-text sentence;
   see the appendix request below.
7. The formal experiment condition "\(\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i\)" and
   "Under rule C1, entry then does not rise." Proposition `prop:control`, Appendix A.6
   (`appendix/A6_robustness.tex`, first statement), which also gives the exact decrease. The
   main text now states the condition in words and the result in positive form.
8. "Lemma `lem:prices`(c) in Appendix `app:beliefs` ensures that the competitive prices reveal
   the same posterior at each strength." Lemma `lem:prices` (Lemma A.2) in
   `appendix/A2_beliefs_trading.tex`. The fact and a pointer to Appendix `app:beliefs` stay in
   the main text, without the part letter.
9. "Full orders are not an equilibrium at \(r_0\), since a purchase earns less than its cost
   there; this row is a control." The notes to Table `tab:outcomes` in the same file state it:
   "at \(r_0\) this profile is a control, not an equilibrium."
10. The \(r_J\) and \(r_S\) earning clauses of the old five-strengths sentence ("at \(r_J\), a
    purchase that just reaches the threshold without recruitment earns it; and at \(r_S\), a
    full sale earns it"). The threshold definitions in Appendix A.4
    (`appendix/A4_coexistence.tex`, items for \(r_J\) and \(r_S\) before the full statement of
    Proposition 3). The symbols stay where Figure 2 prints them: the values paragraph, the
    figure notes, and the two figure-reading paragraphs.
11. "Figure `fig:coexistence` labels the equilibrium forms N, R, F, Q and T, and Appendix
    `app:coexistence` defines each of them." The patterns are now named in words in the figure
    notes; their definitions stand in the full statement of Proposition 3 in Appendix A.4 (the
    `named` environment in `appendix/A4_coexistence.tex`).
12. "Entry therefore rises weakly along the informative branch, and strictly where the investor
    mixes." No new fact: Proposition 3(b) and the purchase-rate paragraph now state the strict
    rise on \([r_A,r_F]\) and the constant part from \(r_F\).

`\reg` audit against `HEAD`: exactly four keys print fewer times, each covered above:
`gap_r2_rC_B` 1 to 0 and `margin_return_B` 1 to 0 (both in Table `tab:margins`),
`margin_return_post_B` 3 to 2 (still in Section 4.2), `u_lo_frac` 2 to 1 (still in Section 4.2).
Every `\label` in the file is unchanged.

## Appendix requests

One request. In Appendix A.9 (`appendix/A9_parameters.tex`, paragraph "The margins table."),
add the sentence below, so that the compressed margin sentence in Section 4.2 can then leave the
main text in the unification pass. Until then I kept the claims in the main text, since the
appendix table lists the three values but no appendix sentence states them. Exact proposed
text:

> The margin of (H3) at the upper end of the band is one distance in three units:
> \(c_H-B_{r_2}(M)=\reg{margin_return_B}\) in cost units,
> \(\tau(r_2)-M=\reg{margin_return_post_B}\) in posterior units, and
> \(r_2-r_C=\reg{gap_r2_rC_B}\) in strength units. Given the auction primitives it depends only
> on the top posterior and on the place of \(r_2\), and in cost units it is the smallest margin
> of Proposition~\ref{prop:ccc}.

No other appendix change is needed from this section. In particular, Proposition 3's full
statement in Appendix A.4 already carries its computer-assisted status in its heading, and the
threshold definitions there already define \(r_J\) and \(r_S\).

## Term choices for the unification pass

- Hypothesis names beside tags at first use in Section 4.1: "the high-cost window (H1)", "the
  trading-cost window (H2)", "the ceiling (H3)". Later references in the section use the name
  with the tag, as in "the ceiling (H3) holds".
- "The entry ceiling" for \(r_C\) throughout, including both figure notes. The caption of
  Figure `fig:beliefs` still reads "Beliefs and the ceiling in the benchmark"; I left the caption
  short. Unification may harmonize it.
- "The benchmark" in running text and in both notes that I touched. The letter \(B\) for the
  benchmark no longer appears in Section 4. It still appears outside my scope (table notes and
  appendix text such as "calibration B", and registry key names), which I did not touch.
- Equilibrium patterns in words in the text: "no informed trade", "a mixed purchase that
  recruits", "a full purchase", "mixed orders without recruitment", "the threshold branch",
  "the informative branch", "coexistence". The letters N, R, F, Q, T appear only in the notes to
  Figure `fig:coexistence`, each tied to its verbal name, because the figure prints them.
- \(r_J\) and \(r_S\) stay in Section 4 only where the figure needs them (values, figure notes,
  and the sentences that read the figure above \(r_N\) and for the low class). Their earning
  definitions live in Appendix A.4. The figure file itself prints "(rule CM)" under the
  threshold branch; the notes now explain that branch in words. If the figure is ever
  regenerated, the parenthetical in the figure can go.
- Positive forms used consistently: "at fixed information a stronger incumbent can only lower
  entry" and "entry rises strictly and then stays constant". "Entry" is the probability that
  the challenger prepares; "preparation" is the act and its cost ("preparation threshold",
  "high-cost preparation"). No "participation".
- Defaults in words in the Figure 2 notes: "when an indifferent investor may mix over its best
  orders and an indifferent high-cost challenger prepares". The alternative appears in words
  only: "only when an indifferent high-cost challenger may prepare with any probability".

## Checks

- `cd slot/manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error
  -outdir=/tmp/ccc_slot_scan/build_compose_C main.tex`: success, `main.pdf` built. The first two
  attempts stopped on two stray math delimiters in my own file; I fixed both and the third build
  completed. Other composers' files changed during the session; the successful build used their
  files as they stood at build time, with no error outside my scope.
- `grep -E "undefined|multiply" /tmp/ccc_slot_scan/build_compose_C/main.log`: no output.
- `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py` from the
  repository root: 21 files scanned, 676 distinct keys used, missing keys 0, literal decimals
  outside `\reg` 0.
- Label check: the sorted `\label` list of the file is identical to `HEAD`. `\reg` check: the
  four reduced keys listed above, each with its appendix home. No commit made.
