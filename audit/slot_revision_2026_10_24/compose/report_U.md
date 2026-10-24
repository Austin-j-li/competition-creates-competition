# Report U: unification pass over the whole main text

I read the abstract and Sections 1 to 9 in order, in the source and in the built PDF, and read all five
composer reports first. I edited six section files. The abstract, Sections 2, 6 and 9, and every proposition
statement needed no edit. I changed no hypothesis, conclusion, number or result, kept the (H1)–(H3) tags,
and kept every `\label`, every `\ref`/`\eqref`/`\cite`, and every `\reg` macro (verified by file comparison
against `HEAD`: identical `\reg` and `\label` multisets in all nine section files). I did not commit and
wrote no tests.

## Changes by section

### Abstract and Sections 2, 6, 9: no change

The abstract already matches the sections claim by claim: control as "can only lower entry", the branch as
"rises and then stays constant", coexistence in positive form, research comovement, and the access result
qualified to the strong-incumbent economy. Section 2 keeps the one naming of Euler's number, at its first
use in the order-size footnote (see Section 4 below). Section 6 already carries status once per cluster in
the form the other later sections now follow, and its single "weakly" is mathematical content. The
conclusion matches the results as composed, including the strict rise where the investor mixes, and it keeps
the seller's choice of terms in its positive next-step form, nowhere else.

### Section 1, introduction

- The welfare and sale-terms tour now follows the order of Section 7: the payment-rule sentence (Section 7.2)
  comes before the reserve sentence (Section 7.3). Before, the tour ran access, reserves, payment against
  the section's access, payment, reserves. The conclusion already used the section order.
- The empirical tour now says "the sale impact and the volume of orders identify the informed share",
  matching Section 8 ("the sale impact and the volume"). "Frequency of orders" named the same object with a
  second word.

### Section 3, competition and information

- Section 3.3 ended with two appendix-pointer sentences. They are now one sentence: Appendix A.2 gives the
  formal statement and proof of the trading bound, and Appendix A.4 uses the split to list every equilibrium
  along the benchmark path. Composer B flagged this seam.

### Section 4, equilibrium results

- Euler's number no longer has two introductions. Section 2.3's footnote names it at first use; Section 4.2
  now reads "with $\eu$ printed upright to separate it from entry $e(x)$" and does not name it again.
  Composers B and C both flagged this seam.
- The compressed (H3) margin sentence left Section 4.2 (see Deletions). The paragraph now ends: the ceiling
  (H3) holds on $(r_C,h)$; parts (i) and (ii) do not use (H3); Table `tab:margins` records every hypothesis
  and its positive margin at the benchmark.
- The caption of Figure 1 is now "Beliefs and the entry ceiling in the benchmark." The figure plots the
  crossing that defines $r_C$, and its notes already say "entry ceiling"; bare "the ceiling" names (H3)
  elsewhere. Composer C flagged this.
- The fixed-information condition in Section 4.2 was one sentence of about sixty words. It is now two
  sentences, split at the logical joint: the fixed laws first, then the independence clauses. Its wording is
  also now the single wording of the condition in the main text (see Section 8).
- Panel B of the controls: "falls once the ceiling binds" is now "falls above the entry ceiling", the same
  fact the same paragraph states in symbols, with the shared name for $r_C$.
- $r_S$ now has its verbal name at its first main-text mention: "the sale threshold $r_S$" in the strengths
  paragraph of Section 4.3. Section 8 already used that name; Section 4 used the bare symbol in the values
  paragraph, the figure notes and the low-class sentences. Composers C and E flagged this from both sides.

### Section 5, research

- Section 5 was the only one of Sections 5 to 8 with no opening status pointer. The research-optimality
  paragraph now ends: "Appendix A.5 states the equilibrium with research formally and gives each result of
  this section in full, with its status." It replaces the bare parenthetical appendix reference and keeps
  the formal-tuple pointer. Sections 6, 7 and 8 already open with the equivalent sentence.

### Section 7, welfare and sale terms (status)

Composer E left status with one opening pointer, one table note and one tag, and asked the unification pass
to treat Sections 5 to 8 alike. Under the guide (Section 2.7 and Section 4, second point) I read that as
status once per cluster in the reporting sentence or table note, the practice Section 6 already follows.
Section 7 now has, each once: "(Proposition A.8 [access], analytical)"; "(computer-assisted)" on the
benchmark proceeds and surplus gains; "(computer-assisted; Appendix A.7)" on the outside-region values;
"Proposition [payment] (analytical)"; "Proposition [reserves] (analytical)"; and "(computer-assisted;
Appendix A.7)" on the strict-deterrence reserve interval. The reserves table note already carried the status
of the table values. The payment benchmark coefficient (registry status analytical) carries no separate tag;
the proposition tag covers that cluster.

### Section 8, empirical implications

- The informed-share paragraph had a sentence with no verb: "at $r_1$, every informed share in the interval
  from … to …." It now runs parallel to the appendix: "at $r_1$, the shares that the counts and the
  incentives allow form the interval from … to …." See the math-audit list.
- The fixed-information condition now uses the same clauses as Section 4.2, so the condition has one wording
  in the main text. See the math-audit list.
- Status once per cluster, as in Section 7: "(computer-assisted)" on the entry-rise value; ", analytical" at
  the citations of the spread, informed-share, winner and announcement propositions; "(computer-assisted)"
  once in each of the alternative-slot, winners, announcements and two-clusters paragraphs. The spread
  numbers paragraph already carried its tag. I did not tag the informed-share interval sentence: its upper
  endpoint is registry-analytical (19/25) while the alternative-slot spread values in the next paragraph are
  computer-assisted, so one tag there would mislabel one of them; the analytical proposition tag and the
  value tag cover the cluster between them.
- The two-clusters paragraph no longer ends on the open selection item. "Which equilibrium a process selects
  is open" now stands with the coexistence claim in the first sentence, and the paragraph ends on the cluster
  values. The fact stays once, in the section the guide assigns it to.

## Cross-section checks that needed no edit

- The symbol $z$: no collision remains. Section 5 uses $\lambda$ for the research intensity throughout
  (composer D's change), and $z$ appears only in Section 7.1 for the trade scale, matching Appendix A.7.
- "the entry ceiling" names $r_C$ in Sections 1, 4, 5, 6 and 8; "the ceiling (H3)" and "the ceiling of
  Section 3.2" name the hypothesis and its model fact. The two uses no longer mix within a sentence.
- Table notes: no "Benchmark $B$" remains in the main text. The notes read "The benchmark." (outcomes),
  "The benchmark with …" (research, reserves), and the payoffs and region notes name the objects directly.
  The vector $S(B)$ in Section 6.3 stays, beside "the signal example" in words each time, because it is the
  appendix's own name for that parameter vector.
- Hypothesis names with tags at first use in Section 4.1, and name-plus-tag later ("the trading-cost window
  (H2)" in Section 6.1), are consistent.
- Tour fidelity: the introduction's coexistence, research, robustness and empirical paragraphs match their
  sections' composed claims, strengths, qualifiers and numbers; the abstract, introduction and conclusion
  use the same positive forms for the control and the branch.
- Section and subsection endings: none ends on an open item. The open research interval stands in the scope
  paragraph before the research figure (whose note draws it), the open payment-rule equilibrium stands with
  the scope sentence at the start of Section 7.2, and equilibrium selection stands inside the two-clusters
  paragraph.
- Voice: no section reads in short split sentences, lists, label openers or proof talk after this pass; the
  one sentence I judged a reader must restart was the Section 4.2 control condition, now split. A style scan
  finds no em dash, no "we", and none of the guide's Section 2.10 words or staged forms in the sections.

## Deletions, with appendix locations

One deletion. Section 4.2, the clauses: "Given the auction primitives, the margin at the upper end depends
only on the top posterior and on the place of $r_2$, … records it in cost, posterior and strength units, with
every other hypothesis and its positive margin at the benchmark; in cost units it is the smallest margin of
Proposition 2." Appendix location: `appendix/A9_parameters.tex`, paragraph "The margins table", lines
81–84, as applied by the coordinator ("The margin of (H3) at the upper end of the band is one distance in
three units … it depends only on the top posterior and on the place of $r_2$, and in cost units it is the
smallest margin of Proposition 2"). The deleted text carried no `\reg` macro. The main text keeps the
positive fact and the table pointer in one sentence.

No other sentence left the main text. Every other edit is a join, a reorder within its paragraph, a naming,
or an added status word.

## Appendix requests

One request. Appendix A.8, paragraph "Certificates" (`appendix/A8_empirical.tex`, line 251), as applied by
the coordinator, states: "All benchmark values of this subsection are computer-assisted." The registry lists
at least one value of that subsection as analytical: `theta_max_full_eq_r1_B` = 19/25
(`registry.csv`, status "analytical", note "$1-2k/(\rho\Delta_T(r_1))=19/25$"). Proposed exact text:
replace the sentence with "The benchmark values of this subsection are computer-assisted, except where the
registry records an analytical status, as for $\bar\vartheta(r_1)=19/25$." The coordinator may prefer to
list the analytical exceptions by name; I verified only this one against the registry.

No other appendix change is needed. In particular, the tie-rule names, the proof-comparison sentence, the
A.8 status sentence, the A.6 signal-heading tag and the A.9 three-unit margin are all in place, and the
main text no longer leans on any appendix wording that is not there. One residual item sits outside the
appendix: `figures/coexistence.pdf` still prints "(rule CM)" under the threshold branch, while the figure
notes now describe that branch in words; if the figure is regenerated, the parenthetical can go (composer C
noted the same).

## Places where the mathematics might read differently (for the math audit)

1. Section 8, Entry paragraph, last two sentences, and Section 4.2, control paragraph: the fixed-information
   condition now has one wording in both places ("the challenger's signal tells it nothing about the
   incumbent's value beyond what the class tells it, the two values are independent given the class and the
   signal, and the cost is independent of the class, both values and the signal"). Section 8 before said the
   two values "draw independently from their own laws" given the class and the signal. Both wordings render
   $\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i$ with an independent cost (Proposition `prop:control`,
   Appendix A.6); confirm the unified wording asserts neither more nor less, in particular that $R$'s law
   does not depend on $S$.
2. Section 8, informed-share paragraph: "the shares that the counts and the incentives allow form the
   interval from $\approx\reg{theta_min_counts_B}$ to $\reg{theta_max_full_eq_r1_B}$." The appendix states a
   closed interval under rule IM (the default convention); the main text says neither "closed" nor the rule,
   as composer E left it. Confirm the sentence does not misstate endpoint inclusion under the defaults.
3. Section 4.2, Panel B sentence: "falls above the entry ceiling" replaces "falls once the ceiling binds".
   The same paragraph states entry under fixed full orders at every strength up to $r_C$ and $\rho$ above it,
   so I read the two forms as the same fact; confirm.
4. Status words added in Sections 7 and 8: each "analytical" comes from the cited proposition's appendix
   title (A.7: access, payment, reserves; A.8: spread, informed share, winner, announcement), and each
   "(computer-assisted)" from the registry status of the values in that sentence (`p2_access_*`,
   `p2_outside_*`, `p2_reserve_ph`/`p2_reserve_weak_top`, `entry_jump_B`, `alt_ba_r1_B`, `wgap_*`,
   `pdrop_neutral_r1_B`, `U_gap_r160_B`). A spot check against the registry would confirm no tag was
   attached to the wrong cluster.
5. Pre-existing in the composed commit, repeated from report E: Section 8 writes the sale-threshold equation
   with $m(1/2)$ where the earlier draft had a bare $m$. I did not touch it; it belongs on the audit's list
   against the $r_S$ definition in Appendix A.4/A.8.

## Checks

- Build, fresh output directory: `cd slot/manuscript && latexmk -pdf -interaction=nonstopmode
  -halt-on-error -outdir=/tmp/ccc_slot_scan/build_unify main.tex` exited 0 and wrote a 102-page PDF. I
  confirmed the PDF is the fresh build: it carries the new Figure 1 caption, the repaired informed-share
  sentence ("form the interval from ≈ 0.250299 to 0.760000") and both "sale threshold" namings.
- `grep -E "undefined|multiply" /tmp/ccc_slot_scan/build_unify/main.log`: no output.
- From the repository root, `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`:
  "files scanned: 21; distinct keys used: 676; missing keys: 0" and "literal decimals outside \reg: 0".
- `grep -c "STRUCTURE:" slot/manuscript/sections/*.tex`: 0 in all nine files.
- Page count: the references start on page 34, so the main text (abstract through conclusion) is 33 pages.
  I read the boundary in the PDF: Section 8 ends and the conclusion runs on page 33, and "References" opens
  page 34.
- Consumer read: I read the rendered abstract, introduction opening, Sections 7 and 8 and the conclusion in
  the built PDF. Numbers print through `\reg`, the new status words sit in the reporting sentences as in
  Section 6, cross-references resolve (Propositions A.11–A.14, Appendix A.7), and no section ends on an open
  item.
- Scope: `git diff --stat` shows edits only in `sections/01, 03, 04, 05, 07, 08`. No appendix file,
  `main.tex`, number file or registry changed. No commit made; no tests written.
