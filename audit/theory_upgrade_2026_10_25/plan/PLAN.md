# The update of the order-slot paper: one plan

25 October 2026, second version. This plan merges three independent plans, each written from one lens: theory and proofs, main text and story, and numbers, figures and delivery (`lens_theory.md`, `lens_maintext.md`, `lens_delivery.md` beside this file). Those files keep the line-by-line detail; this file fixes the order, the rules, the open proofs and the decisions, and it overrides them where they differ. Where the three disagreed, the choice made here is marked "Merged choice".

Inputs, at the paths of the work branch: `../WORKAROUNDS.md` (what each result can claim), `../SCAN.md` (generality table, reduction, vocabulary), the five referee reports `../referee/W1.md` to `W5.md` (the authority on what is true, with full proofs), the second opinion `../referee/second_opinion.md`, the solver reports they cite in `../solvers/`, and the manuscript at Overleaf commit 69c25f4.

Roles, not people or programs, appear in this plan: the mathematics writer, the independent referee (a fresh reader who did not write the text under review), the prose writer and integrator, the production assistant (figures, numbers code, labels, companion documents), the second reader (one read of the finished paper), and the coordinator. A separate staffing note outside the repository assigns them.

## 1. In plain words

The paper keeps its model, its story, its four propositions and every number it already computes. What changes is the reach of the results. Each result is proved at the most general level its proof supports and sharpened by one named economic condition where a stronger claim needs it.

General first. Sections 2 and 3 and Proposition 2 are general and contain no example. The example (point-mass classes worth h and ℓ, a uniform incumbent, h = 10 and ℓ = 1) enters at the opening of Section 4.2, where it first does work. Its results are stated as corollaries, used sparingly in the main text, as the propositions are: three of them, one after each of Propositions 2, 3 and 4, each with a descriptive title, the intuition after it and the proof in the appendix. The text speaks of the example neutrally: "the example", or the example named by its primitives. The paper never calls it "the benchmark". Everything else the example shows (closed forms, figures, tables, the numbers in Section 8) is prose, figures and tables, not further corollaries. The appendix follows the same order inside each part: general results and proofs first, then the example.

The main text gains:
- a short passage on the two numbers through which the market sees the auction;
- a sentence on the strong type's share of takeovers;
- a general Proposition 3, "Quiet and informative markets";
- a general Proposition 4 at even prior odds;
- the three example corollaries;
- a filled research figure, and a panel that draws the coexistence region;
- a Section 8 of four general predictions.

The appendix gains about 450 lines of proofs, in five places. About ninety appendix lines that name files, logs or the example's internal label are rewritten as mathematics or removed. The comparison note and the slides follow.

Nine steps that no referee has yet proved are settled first, chiefly that research without recruitment ends at a single strength near 2.17, which the filled research figure rests on (Part 5). Nothing reaches Overleaf without Austin's approval.

## 2. Rules for every stage

Every writer brief states these rules in full; a pointer to the style guide is not enough.

1. No status labels anywhere in the manuscript, the comparison note or the slides: no "analytical", "computer-assisted", "numerical diagnostic", "certified", or "open" as a status, in titles, sentences, table notes or captions. Style guide sections 2.4 and 2.7 on status are void. A proof may name its method as mathematics ("an exact rational computation shows").
2. No defensive writing. Scope sits inside the claim. A condition is a hypothesis, stated once. No caveat or reassurance paragraphs, no hedges, no answers to imagined referees, no paragraph that ends on a limitation.
3. No development-log writing. The paper reads as written once. No narration of its own changes ("now", "no longer", "new", "updated", "revised", "corrected", "replaces", "in this version", "previously", when they refer to the paper), no announced upgrades, no process words (registry, script, exercise, checker, certificate, run, verified, file names, keys, "calibration B", weakness codes), no bookkeeping about checks. Comparative statics across strengths stay.
4. The example is neutral. The paper does not call it "the benchmark", "the calibration" or "the main case". Its results are corollaries, at most three in the main text.
5. The style guide otherwise: the Laplace register, "I", one word per object, numbers only through `\reg`, no bold sentences in running text, four propositions and three corollaries in the main text with descriptive titles and intuition after each, no lemma or definition environments in the main text.
6. Fixed choices: the two-point preparation cost (zero with probability ρ, c_H otherwise); no general cost law; no c_H rename.
7. No tool, agent, model, session or account names in the manuscript, the comparison note, the slides, any committed project document or any commit message.

Gate at the end of every stage: build, read every changed page, run the language scan (rules 1 to 4) and judge each hit in context, run the numbers scripts if any number moved, write the stage report, commit and push the work branch.

## 3. Where the work runs

The work runs in the cloud, so it continues while Austin's computer is closed. The project's virtual machine is not used.

- **State lives on GitHub.** One work branch, `theory-upgrade`, in `Austin-j-li/competition-creates-competition`, holds the study files, this plan, the stage reports in `plan/progress/` and the manuscript under edit. Every stage ends by pushing that branch, so nothing depends on one session's memory.
- **The manuscript under edit is the repository copy `slot/manuscript/`.** At S0 it is refreshed from Overleaf (it differs from Overleaf 69c25f4 only by the stray "ty"). The numbers and figure scripts already write there, so they need no repointing during the update. Overleaf receives the finished paper in S13, on approval.
- **Austin and Overleaf during the run.** Austin leaves the Overleaf project untouched until S13, or S13 merges his intervening edits by a diff against 69c25f4 before the push.
- **Sessions.** The work runs as cloud sessions in the existing project, which is linked to this repository. A session reads this plan, the latest stage report and its stage section, does the work with fresh-context helpers for refereeing, and ends each stage at the gate above. A later session resumes from the last stage report. Sessions stop at the two points that need Austin: S1, the decisions, and S13, the push to Overleaf. No scheduled routine is used.

## 4. Stages

| Stage | Content | Depends on | Writes | Checks |
|---|---|---|---|---|
| S0 | Preflight: refresh the manuscript copy, baselines | setup | coordinator | coordinator |
| S1 | Austin's decisions (Part 8), recorded in `plan/DECISIONS.md` | S0 | Austin | coordinator |
| S2 | Tooling | S0 | production assistant | prose writer |
| S3 | Notation and vocabulary freeze, rule card | S1 | prose writer | referee (symbols), production assistant (collisions) |
| S4 | Statement freeze and the open proofs | S3 | mathematics writer | referee; prose writer drafts wording targets |
| S5 | Appendix proofs, five packages | S4 | mathematics writer | referee; prose writer (fidelity) |
| S6 | Example numbers | S4 statements; final rows after S5 | mathematics writer (research extension), production assistant (other rows) | an independent recomputation by a different helper |
| S7 | Figures | S3, S6 | production assistant | prose writer |
| S8 | Appendix integration and process-text removal | S5, S6 | prose writer | production assistant (labels), referee (statements transcribed intact) |
| S9 | Main text, Sections 2 to 8 | S8 | prose writer | referee (statements match the appendix) |
| S10 | Introduction, abstract, conclusion | S9 | prose writer | production assistant (claims match the propositions) |
| S11 | Consumers: slides, comparison note | S9, S10 | production assistant | prose writer |
| S12 | Build, verification, final language sweep | S11 | prose writer | coordinator |
| S13 | Second reader, fixes, delivery note, Overleaf on approval | S12 | second reader (read), prose writer (fixes) | coordinator |

S5's packages run in parallel once the foundation package (A2) is done; each writes its own file, so parallel sessions do not collide. A referee never reviews text it wrote.

### S0. Preflight

- Already done in setup: the referee computations are archived in `../referee/computations/`.
- Refresh `slot/manuscript/` from Overleaf (or confirm it equals Overleaf 69c25f4 apart from the "ty"); re-anchor every line reference in the lens plans if lines moved.
- Baselines: build the current paper, record the printed number of every proposition, corollary, remark, lemma, table and figure (the label map), and run the numbers scripts.
- Record the open local commit that removed status words from the manuscript copy on a side branch (80804f0), so S8's sweep covers the same ground.

### S2. Tooling

- Fix the hard-coded font path in `make_figures.py`, so figures build in the cloud.
- Replace the `\slotfigure` and `\slotappendix` placeholders with `\includegraphics` and `\input`, so a missing file stops the build instead of printing "in preparation".
- A language scan that prints matches for rules 1 to 4 across main text, appendix, captions, figure scripts (in-figure labels such as "(rule CM)" and "equilibrium set not characterized" live there), the comparison note and the slides. It prints; it asserts nothing.
- The slot numbers have their own checkers in the slot pipeline; S12 uses them.

### S3. Notation and vocabulary freeze

From SCAN Part 3, applied once before any proof is written:
- **The example.** It is introduced once, at the opening of Section 4.2, and named neutrally. Before that point the text speaks of "a stronger incumbent", not of the strength r.
- **"Spread"** means only the target-payoff spread; the difference between purchase and sale prices is the "price gap".
- **"Admissible"** applies only to bids.
- **"Quiet market"** names the equilibrium without informed trade.
- **Renames:**
  - F_r(λ) becomes Λ_r(λ);
  - the research value V becomes Ψ;
  - C(π) becomes 𝒞(π);
  - the rate pair becomes s₊ and s₋;
  - the cap strength r̄_R becomes r_{λ̄}, or words;
  - r_Q marks the end of floor-entry research;
  - α_I and α_C are the signal accuracies.

The rename of r̄_R reaches the figure code and A9, so the figure waits for this stage. Number keys that end in `_B` keep their names; keys never print. Details: `lens_theory.md` 3.6, `lens_maintext.md` 3.6.

### S4. Statement freeze and the open proofs

The mathematics writer drafts the final formal statement of every changed result, including the three corollaries, before any proof or prose. The referee checks each statement against the referee reports.

The prose writer drafts the main-text wording targets (`lens_maintext.md` 3.1). The referee reads each target and marks it "match", "missing qualifier" or "overclaim".

Acceptance requires no overclaim and every qualifier present:
- prior 1/2 and the mixing investor for research;
- two-sided trade for the tests;
- a prior below the threshold for the weighted test;
- prior and slot fixed for the winner trend.

The open proofs of Part 5 are settled here, before S5 and S7 depend on them.

### S5. Appendix proofs

Each package is a standalone LaTeX file that compiles with the manuscript's macros, refereed beside it, then transplanted.

1. **A2, the foundation.**
   - The reduction lemma: trading, posteriors and entry depend on the auction only through the spread and the threshold, and a stronger incumbent raises both.
   - Repair the paragraph that says equal posteriors give equal prices: under the tie rule CM, equal entry is also needed.
   - Narrow the opening sentence to the belief lemma.
   - Sources: SCAN Part 2, and the referee reports W3 and W5 on pooled orders.
2. **A3 and A6, ownership and robustness.**
   - Proposition 2 gains the strong type's share of takeovers under outbidding.
   - A decisive-advantage lemma gives the cost window 399/80 ≤ c_H ≤ 32/5. In the example, c_H = 6 lies inside it.
   - A.7 (complementary signals) extends to ranked classes.
   - The full statement and proof of Corollary 1, from the current Proposition A.1, follows Proposition 2's proof.
   - Source: referee report W2.
3. **A4, coexistence.**
   - The region theorem: coexistence holds exactly when the two numbers lie in a fixed region, and entry rises with the spread.
   - The sure-purchase stretch is one interval along any path.
   - The whole set is one interval under the balance condition. Its primitive case is the uniform, separated and affordable incumbent, subject to proof O9.
   - Then the example: the full Corollary 2, with coexistence on [r_A, r_N] and the shape of entry. Two hand proofs replace both root counts of the current path lemma. Corollary A.2, coexistence at other priors in the example, gets a shorter proof.
   - The two-interval economy is a stated fact.
   - The figure note's claim about the threshold branch at r_A is corrected.
   - Source: referee report W1.
4. **A5, research, at prior 1/2 under the mixing rule.**
   - Research and entry rise with the spread until the cap. The weak type's selling adds the sale's profit to the research equation and does not interrupt the rise.
   - The recruiting equilibrium exists exactly while the top posterior reaches the threshold.
   - Ownership rises under outbidding.
   - The cheap-research condition keeps the recruiting equilibrium on one interval along a path.
   - Then the example: the full Corollary 3 (no research at the weakest strength, two equilibria at middle strengths, the recruiting equilibrium at the cap up to the entry ceiling) and the three-outcome lemma that fills the research figure, followed by the current Proposition A.2 (research cap and cost).
   - The abstaining-branch result (cap before selling) is dropped.
   - The same-incumbent ownership ratio gets one sentence after the proof.
   - Sources: referee reports W2 and W3.
5. **A8, empirical.**
   - The weighted price test at every prior, shown to be the same moment as the announcement result.
   - Orders predict the winner: the sign is general, the covariance holds after the ceiling, the gap widens under outbidding, and the winner second difference holds at prior 1/2.
   - The informed share is identified at a known prior and by the sale price.
   - The exact announcement condition.
   - The entry-component trend, under the reserve condition.
   - The unweighted test, kept as a part at π ≥ 1/2.
   - Sources: referee reports W4 and W5.

Full file-by-file list with line references: `lens_theory.md` 3.2.

### S6. Example numbers

- **New rows:**
  - the margins of each named condition;
  - the end r_Q of floor-entry research;
  - the takeover shares;
  - the class-entry rows that show the improving pool.
- **Existing keys to reuse:** 1.196, 2.124, the cheap-research margin, the cap-before-selling strength.
- **Fractions:** every fraction a proof uses (937/5520, 9667/8280, 81/80 and others) prints through `\reg`.
- **Checking:** each new number comes from an exact or interval computation, plus a second, independent recomputation by a different helper.
- **Other economies:** numbers from economies other than the example appear in the main text as words or formulas only, and in the appendix only with their own row and check.

Details: `lens_delivery.md` 3.1 to 3.3.

### S7. Figures

- **The research figure.** One continuous axis, no gray band. The recruiting equilibrium with research at the cap runs to the entry ceiling. Just above the no-trade bound, a second equilibrium has research without recruitment, ending at r_Q. It is drawn only after proof O1.
- **The coexistence figure.** Merged choice: the region in the spread-threshold plane, with the example's path entering at r_A and leaving at r_N, becomes a panel of the existing coexistence figure, so no figure renumbers.
- **Labels and captions.** In-figure labels obey rules 1 to 4. Compliant caption drafts are in `lens_delivery.md` 3.5.

### S8. Appendix integration

- Transplant the packages.
- Rewrite as mathematics, or remove, the roughly ninety lines that name files, logs, keys or the example's internal label.
- Drop the source column of the A9 margins table; the numbers files keep provenance.
- Add the new margins to A9.
- Give A9 a neutral title, such as "Parameters of the example".

### S9 and S10. Main text

The lineup agreed with Austin; wording targets are in `lens_maintext.md` 3.1, adjusted for rule 4.

- **Sections 2 and 3 contain no example.** The example's declaration (02:78–88), the uniform main case (02:54–55), and the closed forms with their remarks (03:19–34, 76, 80, 99) move to the opening of Section 4.2.
- **Section 3** gains the two-numbers passage. The intuition for Proposition 1 comes in words from the general formula.
- **Section 4.1.** Proposition 2 gains the takeover-share sentence and the decisive-advantage sentence.
- **Section 4.2 introduces the example.** Corollary 1: in the example, Proposition 2's conditions hold together on a stated window of slots, with the entry and ownership values. The two numbers follow in closed form, then the comparison with information held fixed.
- **Section 4.3.** Proposition 3, "Quiet and informative markets", then Corollary 2: in the example, coexistence on [r_A, r_N], and entry that rises, flattens and returns to the floor above r_C. The figure, with its region panel, follows.
- **Section 5.** Proposition 4 is stated generally, at even prior odds and under the mixing rule. Corollary 3 gives the example's list of equilibria, followed by the filled figure.
- **Sections 6 and 7** change little.
- **Section 8** states four general predictions in prose, with the example's numbers as illustrations.

S10 then writes the introduction, abstract and conclusion, which come last and match the propositions. The introduction states each result in its general form, with numbers from the example only as illustrations, marked as such. There is no empirical sentence in the abstract.

### S11. Consumers

- **Slides.**
  - Every reference to the old Proposition 4(b) moves to Corollary 3, including the slides at lines 484 and 776.
  - Frames F12, F13 and F16, and the notation and appendix frames, follow the new statements.
  - The research story ends at the entry ceiling.
  - "Benchmark" leaves the slides as well.
- **Comparison note.** It carries 56 status labels and is framed as version history, so it needs a recast or a freeze (decision 8).
- **Later pass.** The study guide, website, web slides and presentation are listed as stale and left for after Austin commits his own work in those folders.

### S12. Verification

- Build the manuscript, slides and comparison note, and read every changed page.
- Run the numbers pipeline: zero missing keys, no typed decimals, orphans confirmed.
- Rerun every affected numerical exercise and its independent checker.
- Compare the label map with the S0 baseline, and update every consumer citation that moved.
- Run the full language scan and judge every hit.

### S13. Close

- The second reader reads the finished paper once, and the fixes follow.
- The coordinator writes a short delivery note to Austin.
- On approval, the finished manuscript is copied into the Overleaf project, after merging any edits Austin made there, and pushed.
- Merging the work branch into the main line of the repository, and anything that feeds the website, waits for Austin as well.

## 5. Proofs no referee has supplied yet

The mathematics writer settles these in S4, and the referee checks each one.

- **O1. Where research without recruitment ends.** The research figure claims it ends once, at r_Q ≈ 2.167, and nowhere else before the entry ceiling. Both sides of the defining comparison rise with strength, so one crossing needs an exact argument, such as bounds on short subintervals, as in the existing cheap-research argument.
- **O2. The liquidity share.** Which results hold for every liquidity share β < 1/2, and which use β ≤ 1/3.
- **O3. The end of the capped segment.** The right end of the capped recruiting segment is the last point where the cap posterior reaches the threshold. In the example that point is r_C.
- **O4. The cheap-research margin.** The cheap-research condition is stated on the exact research margin, which includes the sale's profit.
- **O5. Existence.** Existence of an equilibrium at prior 1/2, for every incumbent distribution, is refereed again.
- **O6. The takeover share.** The exact condition for the takeover share to rise strictly: the weak type must win with positive probability against the weaker incumbent.
- **O7. Pooled orders.** When the sale and the zero order share a posterior during mixed selling, the construction must check equal entry.
- **O8. Zero research at the sale boundary.** At the boundary where a sale starts to pay, the lemma classifies outcomes, not strategy profiles.
- **O9. The uniform case.** Whether the uniform, separated and affordable incumbent implies the balance condition. A two-line derivation exists but is unrefereed. If it fails, Proposition 3 lists the two conditions as alternatives.

## 6. Numbering

- **Main text.** Four propositions and three corollaries. Corollaries 1 to 3 have their own counter.
- **Appendix example results.** Where an example result in the appendix is the full version of a main-text corollary, it is stated as that corollary:
  - Proposition A.1 becomes the full Corollary 1;
  - the example part of Proposition 4 becomes the full Corollary 3.

  Later appendix propositions then move up by one (decision 7).
- **Everything else** follows the placement rule of the three lens plans. There are no other new numbered results. New lemmas go after the trading lemma, so Lemmas A.1 to A.3 keep their numbers. No new appendix table goes before Table A.4.
- **Checking.** The S0 baseline label map is compared with the final build in S12, and every hard-coded number in the slides and comparison note is updated from that comparison.

## 7. Main risks

1. Scope qualifiers lost when a statement is compressed into a main-text sentence: the prior, the tie rule, two-sided trade, weak against strict. The statement freeze, the referee's fidelity read and a sweep for "interval" and "strictly" guard against it.
2. Main-text prose written before its appendix statement is fixed. S9 starts only after S8.
3. Mathematical prose breaking the language rules ("we", "certified", "new lemma", hedges). The rule card goes into every brief, and the scan runs on every package.
4. Removing process text removes the only stated basis of some numbers. Every number a proof uses is an exact closed form, or a root whose existence and uniqueness the text proves.
5. Silent failures: a missing figure printing "in preparation", an unknown key printing `??key`, a stale numbers file passing the scan. S2 tooling removes the first, and S12 checks the others.
6. Overleaf edits made during the run. S13 merges them by diff before any push.
7. The research story change in Section 5 reaching the introduction, Table 4, the slides and the comparison note. A sweep for the cap strength and the old branch end catches the stragglers.
8. A cloud session ending mid-stage. Every stage writes its report and pushes before it ends, and the next session resumes from the last report.

## 8. Decisions for Austin

Sessions wait at S1 until these are answered. Each has a recommendation.

1. **Delete the stray "ty"** before the model section. Yes.
2. **Fill the research figure**, after proof O1. Yes.
3. **Add the coexistence-region panel** to the coexistence figure. Yes.
4. **The condition in Proposition 3.** The balance condition (the spread grows at least as fast as the strong type's margin over the preparation cost shrinks), with the uniform incumbent as its primitive case, if proof O9 holds. Otherwise the two side by side.
5. **Identification in Section 8.** Keep the known-prior result and the sale-price inversion; leave the unknown-prior local result out.
6. **Which example results become main-text corollaries.** Three: after Proposition 2 (its conditions hold together), after Proposition 3 (coexistence and entry in the example), after Proposition 4 (the example's research equilibria). Everything else stays prose.
7. **Appendix example propositions.** State Proposition A.1 and the example part of Proposition 4 as the full Corollaries 1 and 3, accepting that later appendix propositions move up by one, with the slides and comparison note updated from the label map. The alternative keeps every appendix number and cites the old propositions from the corollaries.
8. **The comparison note.** Its status labels and method sections go. Then either recast it (about 300 lines, results side by side for the two set-ups; recommended if it circulates with the paper) or freeze it as a dated record outside the Overleaf project (it then needs a website change in Austin's own folder).
9. **Overleaf during the run.** Leave the Overleaf project untouched until the final step, or accept a merge of edits at the end.

Settled by the move to the cloud:
- The study files are committed to the work branch, with model and account names removed.
- The scripts write to the repository copy during the update.

Defaults applied unless Austin objects:
- A.7 is extended; A.9 keeps two class values; A.5 stays on the uniform family.
- 1 + u = e is kept.
- Consumers are limited to the comparison note and the slides.
- The decisive-advantage lemma and its cost window go in.
- The takeover-share sentence goes in Proposition 2.
- "Quiet market" becomes a fixed name.
- There is no empirical sentence in the abstract.
- The abstaining-branch result is dropped.
- The example of the second return to research is left out.
- The ownership ratio gets one sentence.
- The placeholders become real includes.
- Commit messages stay plain.

## 9. Where the three lens plans differed

- **Region panel placement.** The theory plan put it as panel (c), the main-text plan as panel (a) with entry as (b), and the delivery plan as a separate figure. Merged: a panel of the existing figure, so no figure renumbers.
- **Proposition 3's condition.** The theory plan led with the uniform condition, the main-text plan with the balance condition. Merged: the balance condition, with the uniform case as its instance, conditional on O9.
- **Order of consumers and the final sweep.** The plans differed. Merged: consumers come before the sweep, so the sweep covers them.
- **The example's list of research equilibria.** The theory plan proposed a new appendix table, which would renumber tables the comparison note cites. Merged: Corollary 3 in the main text, and its full version as a paragraph in A5.
- **Where the scripts write.** The lens plans pointed them at the Overleaf copy. Merged: in the cloud setting, the repository copy is the copy under edit, and Overleaf receives the result at the end.

## 10. Changes after Austin's review

- 25 October: general properties first. The example leaves Sections 2 and 3 and enters at the opening of Section 4.2, after Proposition 2.
- 25 October: the example is neutral and its results are corollaries, at most three in the main text, treated like the propositions. The word "benchmark" leaves the paper.
- 25 October: the work runs in the cloud from the GitHub work branch, so it continues while the computer is closed. The virtual machine is not used.
- 25 October: the sessions run inside the existing project; no scheduled routine.

## 11. Size

| Part | Size |
|---|---|
| Appendix | about 450 net lines of new or rewritten LaTeX, plus about 90 lines of process text rewritten |
| Main text | about a fifth of its lines; Propositions 3 and 4 about a page each; three short corollaries |
| Statements | six to eight pages, frozen before any proof |
| Numbers | a few dozen rows |
| Figures | two figures change |
| Comparison note | about 300 lines if recast |
