# S4 helper briefs

The briefs of the S4 jobs, as they were given on 25 October 2026. Each job sent the shared brief, then the task brief with the area text. `<role>` is the mathematics writer, the referee or the prose writer, as `PLAN.md` Part 4 assigns.

## Shared brief

```text
You are a helper on the update of the order-slot paper "Competition Creates Competition" by Austin Li. You work for the coordinator, who reviews your work, runs the stage gate, commits and pushes. Your role: <role>.

Repository: /home/user/competition-creates-competition, branch theory-upgrade (already checked out). The plan is audit/theory_upgrade_2026_10_25/plan/PLAN.md, the authority on order, rules and gates. Austin's answers are in plan/DECISIONS.md: all nine decisions as recommended (the comparison note is recast; Overleaf stays untouched until the end). Stage reports are in plan/progress/. The frozen rule card, vocabulary and notation are in plan/NOTATION.md: follow it. Supporting plans: plan/lens_theory.md, plan/lens_maintext.md, plan/lens_delivery.md. PLAN.md overrides them where they differ. They say "the benchmark" and use the path overleaf/slot/; in this work the manuscript under edit is slot/manuscript/. The S3 renames are committed there; they kept every line number, and NOTATION.md names the new symbols. The study: audit/theory_upgrade_2026_10_25/WORKAROUNDS.md, SCAN.md, referee/W1.md to W5.md (the authority on what is true, with full proofs), referee/second_opinion.md, solvers/, scan/, referee/computations/. Numbers pipeline: audit/slot_manuscript_2026_10_23/ (registry/*.csv, scripts/). Style guide: audit/slot_revision_2026_10_24/STYLE_GUIDE.md.

Rules for every word you write into the manuscript (slot/manuscript/), the comparison note, the slides, figure labels, statement drafts, proof packages, and any committed project document:
(1) No status labels anywhere: no "analytical", "computer-assisted", "numerical diagnostic", "certified", or "open" as a status. A proof may name its method as mathematics ("an exact rational computation shows").
(2) No defensive writing: scope sits inside the claim, a condition is a hypothesis stated once, and there are no caveats, hedges, reassurance or paragraphs that end on a limitation.
(3) No development-log writing: the paper reads as written once, with no narration of its own changes ("now", "no longer", "new", "updated", "revised", "corrected", "replaces", "in this version", "previously", when they refer to the paper) and no process words (registry, script, exercise, checker, certificate, run, verified, file names, keys, "calibration B"). Comparative statics across strengths are fine ("above the ceiling, orders no longer predict entry").
(4) The example is neutral: never "the benchmark" (nor "the calibration" or "the main case"); call it "the example" or name it by its primitives. Its results are corollaries, at most three in the main text.
Also: the author writes "I"; every number prints only through \reg{key}, fractions included; follow the style guide except its status rules (its sections 2.4 and 2.7 on status are void, and its advice to say "the benchmark" is void under rule 4); the two-point preparation cost (zero with probability rho, c_H otherwise) stays unchanged, with no general cost law and no rename of c_H; and no tool, agent, model or account names in any committed file or commit message.

How to work:
- Do not commit, push, merge, rebase or switch branches; the coordinator commits. Never push to or pull from Overleaf. Open no pull request.
- Do not write or run tests: no test files, fixtures, frameworks, or scripts with assertions. Verify by building, by running programs through their real interface with real inputs, and by reading the output. A short print-only computation is allowed.
- Do not spawn helpers.
- Build LaTeX only into your private folder <private build folder outside the repository>: for example, from audit/theory_upgrade_2026_10_25/statements run "latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=<private build folder outside the repository>/build FILE.tex". The shared preamble audit/theory_upgrade_2026_10_25/tex/preamble.tex loads the manuscript's packages, macros, theorem environments and numbers; a standalone file starts "\input{../tex/preamble}" and then "\begin{document}". A \reg key that does not exist yet prints "??key"; that is expected in a draft, and every such key is listed with its exact value in your notes. Leave no build product in the repository. Other helpers work in the same checkout at the same time on other files; touch only the files your brief names.
- TeX Live 2023 is installed with the needed fonts; python3 has numpy, mpmath and matplotlib; pdftotext, pdftoppm and pdffonts are available. The print-only language scan is "python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/language_scan.py --no-doc --no-figcode --extra FILE ..."; run it on what you write and judge each hit.
- Reports that go into the repository obey rule (3) and the no-names rule: call roles "the mathematics writer", "the referee", "the prose writer", "the production assistant", "the coordinator".
- Your final answer is data for the coordinator: fill the structured output fully and plainly.
```

## Mathematics writer, per area

```text
Task: Stage S4, the statement freeze, for area <area> (<area name>), and the open proofs assigned to it (PLAN.md "S4. Statement freeze and the open proofs" and Part 5).

Read first: PLAN.md in full (above all Part 1 "In plain words", S4, the S5 item for your area, Part 6 "Numbering", Part 9), plan/NOTATION.md, plan/DECISIONS.md, the rows of plan/lens_theory.md 3.1 for your results, lens_theory 3.2 for your files, 3.4 (obligations) and 3.7 (wording targets for your area), the WORKAROUNDS.md sections and appendix items for your weakness, the referee report(s) for your area in full, the parts of scan/reduction_A3_A5.md and scan/generality_A1_A2_A6_A8.md that cover your results, and the current manuscript files for your area (main text and appendix).

Deliverable 1: audit/theory_upgrade_2026_10_25/statements/<area>.tex, a standalone file ("\input{../tex/preamble}", then "\begin{document}") that holds the final formal statement of every changed or new result in your area, in the paper's frozen notation, with every hypothesis in place: the prior, the tie rules in their plain phrases, the trading pattern, the named condition, weak against strict. Order them as the appendix will hold them: general results first, then the example. Give each a label and, as a LaTeX comment above it, its source ("% source: referee report W3, section 3, eq. (5)") and the manuscript lines it replaces. Also state the short main-text form of each main-text proposition and corollary of your area, marked as such. No proofs in this file, except that the open proofs below go in their own files. For each result of the example, give every number it prints as \reg{key}; list new keys with exact values in your notes. The file compiles without errors.

Deliverable 2: audit/theory_upgrade_2026_10_25/statements/<area>_notes.md: for each statement, the source (report and section), its scope (prior, tie rules, trading pattern, condition), what it replaces in the manuscript (file:line), its number after the update (decision 7 and PLAN.md Part 6: main-text corollaries 1 to 3 have their own counter; Proposition A.1 becomes the full Corollary 1 and the example part of Proposition 4 the full Corollary 3, so later appendix propositions move up by one; new lemmas go after the trading lemma so Lemmas A.1 to A.3 keep their numbers; no new appendix table before Table A.4), and the new \reg keys with exact values and how each is computed.

Deliverable 3, the open proofs of your area: for each, a folder audit/theory_upgrade_2026_10_25/statements/O<n>/ with O<n>_proof.tex (the statement and a complete proof, as a LaTeX fragment ready for the appendix), O<n>_notes.md (the argument in words, the result, and, if the claim as planned fails, the correct statement with its proof and what it changes in the plan), and a print-only computation if the proof needs one (run it and read the output).

Work at full depth: derive each statement from the model and the referee reports, and do not copy a solver's formula on trust. Where a referee report and the plan disagree, the referee report decides what is true; say so in the notes.
```

### Area A: foundation and ownership: appendix parts A2, A3 and A6; Proposition 2; Corollary 1

```text
Your results:
- A2: the reduction lemma (trading, posteriors and entry depend on the auction only through the spread and the threshold; with research, the same for the research intensity once the research cost and cap are fixed; prices follow from P = t_0 + e(w_L + Delta mu)); the lemma on the two numbers along a path (a stronger incumbent raises the spread and, where the threshold is nonnegative, the threshold and their product; the class mean gap is fixed; strictness conditions; J carries no sign along a path, stated positively with the example of scan/reduction_A3_A5.md); the repaired paragraph on constructed tuples (under the tie rule in which an indifferent challenger may prepare with any probability, equal posteriors give equal prices only with equal entry); the narrowed opening sentence (the belief lemma holds for every order profile; the price and trading lemmas for every tuple that meets their conditions). Sources: SCAN.md Part 2, scan/reduction_A3_A5.md sections 2, 3(a) and 4.1, referee/W1.md "Solver B 1", referee/W3.md and W5.md on pooled orders.
- A3 and the main text: Proposition 2 part (ii) gains class H's share of the takeovers that go to a challenger, under outbidding, with its exact strictness condition (obligation O6); a decisive-advantage lemma (wherever preparation at c_H pays for a challenger known to be class H, that challenger beats every incumbent value; for point classes and the whole uniform family it holds exactly when c_H >= (h^2 - p^2)/(2h); with the cost window 399/80 <= c_H <= 32/5 that contains the example's c_H = 6), stated for a family of incumbent laws. Sources: referee/W2.md "Shared Candidate 3", "Decisive advantage", "Benchmark verification", "Do the same workarounds cover Proposition 2"; WORKAROUNDS.md W2 and appendix W2.5 and W2.7.
- The full Corollary 1, which takes the place of the present Proposition A.1 (appendix/A3_proposition2.tex, around line 157): in the example, Proposition 2's conditions hold together on a stated window of slots, with the entry and ownership values; and its short main-text form (PLAN.md S9, "Section 4.2 introduces the example").
- A6: Proposition A.7 (complementary signals) extended to ranked classes and a continuous stochastically ordered pair, with ownership (1/2) e_H W_H(F_1) (referee/W2.md "Proposition A.7"; scan/generality_A1_A2_A6_A8.md); the one scope sentence for A.5 (it stays on the uniform family).
Open proofs: O2 (which results of the whole paper hold for every liquidity share beta < 1/2 and which use beta <= 1/3; go through every result, main text and appendix, and give the list the footnote at sections/02_model.tex around lines 123 to 125 and the A2 paragraph around lines 232 to 236 need), O6 (the exact condition for class H's takeover share to rise strictly; the plan's derivation says strictly exactly when the weak type wins with positive probability against the weaker incumbent; check against referee/W2.md), O7 (pooled orders: when the sale and the zero order share a posterior during mixed selling, as at r = 1.9118 in referee/W3.md section 4, the construction must check equal entry; state the lemma A2 needs and show the A5 construction meets it).
```

### Area B: coexistence: appendix part A4; Proposition 3; Corollary 2

```text
Your results, general first:
- The lemmas at a fixed incumbent law (the high-class, low-class and product lemmas of A4, restated at a fixed F, with the threshold below one for the mixing rate and the case of a threshold at or above one).
- The full statement of Proposition 3, "Quiet and informative markets": (a) the region: the quiet market and an informative market coexist exactly when pi < tau <= M(pi) and k/(1 - tau) <= Delta <= k/(rho max{pi, 1 - pi}); the informative equilibrium is then unique when an indifferent high-cost challenger prepares; its entry rho + (1 - rho) min{(1 - pi) b Delta/k, b + pi lambda} depends on the spread alone and rises strictly until the investor buys for sure; the region is convex; the prior ceiling pi < 1/(1 + rho) is necessary; (b) along any path the strengths at which the quiet market coexists with a sure purchase form one interval, and every internal gap lies at spreads too narrow for a sure purchase to pay; (c) the whole coexistence set is one interval under the balance condition (the spread times class H's margin over c_H does not fall along the path, with that margin positive at the start), whose primitive case is the uniform, separated and affordable incumbent, subject to O9 (decision 4: if O9 fails, the two conditions appear side by side); the squared balance form for the threshold branch; (d) existence of an equilibrium at prior 1/2 (obligation O5). Path statements need tau > pi at the start of the path. Sources: referee/W1.md "Shared Candidate 1" eqs (1) and (2), "Solver B 1" eq (3) with its wording corrections, "Solver A 2 and Solver C 3" eqs (4) to (8), "Solver B 2" eqs (10) to (12); WORKAROUNDS.md W1 and appendix W1.1 to W1.4; scan/reduction_A3_A5.md section 3(d).
- The two-interval economy as a stated fact (referee/W1.md "Solver A's example", eq (20)).
- The tie-rule paragraph for a general F: when an indifferent challenger may prepare with any probability, the threshold pair adds informative equilibria inside the region and the point tau = pi joins it; when an indifferent investor abstains, coexistence needs k/(1 - M(pi)) < Delta.
Then the example:
- the path lemma with hand proofs in place of both polynomial root counts (margins 2/5 for the uniform condition, 9667/8280 for the balance condition, 937/5520 for the squared form on the whole path [r_0, r_2]); the threshold order;
- the full Corollary 2: in the example, coexistence on [r_A, r_N], and entry that rises, flattens and returns to the floor above r_C (the present named full statement of Proposition 3 in A4 and its table become this corollary's full form); and its short main-text form;
- Corollary A.2 (coexistence at other priors in the example) with a shorter proof from the region theorem;
- the corrected figure-note claim: at r_A the threshold branch has entry one and is an equilibrium when an indifferent challenger prepares, too.
Open proofs: O5 (existence of an equilibrium at prior 1/2 for every incumbent distribution with a positive spread, g_H > g_L and tau > 1/2, including tau >= 1, under the default rules; referee it again as a full proof from scan/reduction_A3_A5.md section 3(d)), O9 (whether the uniform, separated and affordable incumbent implies the balance condition; plan/lens_maintext.md Stage 1 item (i) sketches a two-line derivation; prove it or show where it fails, and give Proposition 3(c) in the form decision 4 then requires).
```

### Area C: research: appendix part A5; Proposition 4; Corollary 3

```text
Your results, at prior 1/2 when an indifferent investor may mix, general first:
- positive research forces a strict full purchase by class H, for every beta < 1/2 (referee/W3.md section 1);
- the low class's sale lemma: its sale rate, the sale posterior b/(2b + lambda z), and its best sale profit (rho Delta m_lambda - k)^+ (W3 section 2, eqs (1) to (3));
- the full statement of Proposition 4: (a) existence and the research schedule (the recruiting equilibrium exists exactly when Delta > 2k and 1/2 < tau <= M at the capped root of 2 a lambda = Delta m_lambda - k + (rho Delta m_lambda - k)^+); (b) research, entry and class-H entry rise with the spread until the cap, class-L entry falls, the pool of prepared challengers improves, the acquisition chance at a fixed incumbent value rises wherever class H can win at that value (almost every value; atoms by the auction's tie rule); the weak type's selling adds the sale's profit to the research equation and does not interrupt the rise; the upward kink where a sure sale starts to pay; (c) ownership rises under outbidding, weakly, strictly where research is below its cap and the spread rises strictly, with the exact trade-off across incumbents and the decisive-advantage route; (d) along a path, the cheap-research condition, stated on the exact research margin (obligation O4), keeps the recruiting equilibrium on one interval, which ends at the last point where the cap posterior reaches the threshold (obligation O3). Sources: referee/W3.md "Shared Candidate 1" sections 1 to 6 and "Shared Candidate 2"; referee/W2.md "Shared Candidate 1" and "Shared Candidate 2"; WORKAROUNDS.md W2, W3 and appendix W2.2 to W2.5, W3.1 to W3.7.
- the three-outcome lemma (zero research, recruiting research, research at the entry floor exhaust the outcomes under the default rules; the coexistence band) (W3 "Solver B/Solver D Candidate 3"; obligation O8 for the boundary rho Delta = 2k);
- the strong-incumbent lemma (condition U), unchanged in substance;
- the remark on other tie rules: when an indifferent challenger may prepare with any probability (the interior threshold tuple and the cap family) and when an indifferent investor abstains (the gap on (r_N, r_S] in the example, and the threshold equilibrium at r = 2);
- access to prices with research in general form (scan/reduction_A3_A5.md section 3(f)).
Then the example:
- the full Corollary 3: no research at the weakest strength, two equilibria at middle strengths, the recruiting equilibrium with research at the cap up to the entry ceiling r_C; with the three-outcome list along the path (zero research and recruiting research coexist from r_R to r_N; capped recruiting and research at the entry floor coexist on (r_N, r_Q); capped recruiting alone on [r_Q, r_C]; research at the cap with entry rho above r_C); and its short main-text form;
- the present Proposition A.2 (research cap and cost), renumbered, referring to the example's list;
- one sentence after the proof of Proposition 4 on the same-incumbent ownership ratio e_H/rho;
- the abstaining-branch result (cap before selling) is dropped.
Obligation O1 (the single end r_Q of floor-entry research) is proved and refereed in audit/theory_upgrade_2026_10_25/statements/O1/ (O1_proof.tex, O1_notes.md, o1_bounds.py, O1_referee.md). Its mathematics is accepted and does not change. Do this first: bring O1_proof.tex and O1_notes.md to the frozen notation of plan/NOTATION.md (part (d), S5, the paragraph on the O1 draft: lambda_Q(Delta_T) for Lambda_rho, min{lambda_Q, lambda-bar} written out for lambda*_rho, sigma_L(-1) = hat-s_-(r)/lambda-bar for s(r), the gap written out, "floor-entry research" and "recruiting research at the cap"), and apply fixes 3, 4 and 5 of O1_referee.md section 3 (equal entry in Step 5 (E2); the falling denominator in Step 2; the placement comments go). Rebuild the fragment, and add a short section "Notation pass" to O1_notes.md that lists the changes. Then fit Corollary 3 and the three-outcome lemma to O1; do not redo its proof. Name the folder statements/O1/ in your notes, so that the referee also checks the notation pass.
Open proofs: O3 (the right end of the capped recruiting segment is the last point where the cap posterior reaches the threshold; in the example that point is r_C), O4 (the cheap-research condition on the exact research margin, which includes the sale's profit (rho J - k)^+; the start of a path can lie where a sure sale already pays), O8 (zero research at the boundary rho Delta = 2k, where the hypothetical-success orders are not unique when an indifferent investor may mix: the lemma classifies outcomes, not strategy profiles).
```

### Area D: empirical predictions: appendix part A8

```text
Your results (decision 5: keep the known-prior result and the sale-price inversion; leave the unknown-prior local result out):
- the standing paragraph: the results hold for a general incumbent at every prior under the trading pattern each names, for one target at one strength; the informed share is lambda/v in general, and u/(2 + u) = 2M - 1 = M - m only at prior 1/2 (appendix/A8_empirical.tex line 8 states these equalities without the prior);
- A.11, retitled for the price gap and the weighted test: the weighted price test at every prior below the threshold under full two-sided trade in one public state; the sign table when an indifferent challenger prepares; the identity of the weighted difference with the average price after an opportunity minus the price after no order, the same moment as A.14(iv), stated once; the unweighted test kept as a part when pi >= 1/2 and rho <= 1/2 and an indifferent challenger prepares; the entry-component split into competition and reserve rescue, and its trend when the chance that the incumbent misses the reserve stays fixed, or, with a uniform incumbent, when the reserve is below 1/sqrt(3) of the lowest challenger value and of the smallest incumbent upper bound (the example has ell^2 - 3p^2 = 1/4). Sources: referee/W5.md "Shared candidate 1" eqs (1) to (6), "Primitive rescue" eqs (15) and (16), "Entry-component trend" eqs (17) to (19), "Ceiling jumps";
- A.12, identification: at a known prior other than one half, order counts identify the informed presence and the slot, and prices then identify rho Delta; the prior-1/2 count fact with the example's interval; the sale-price inversion when entry after a sale and after no order sits at rho and rho Delta is known (W5 "Shared candidate 2");
- Corollary A.3, purchases only, at any prior (W5 "Purchases only and Corollary A.3");
- A.13, orders predict the winner: the sign under full two-sided trade at every prior, w_1 - w_{-1} = (M - m) E_F[D(R)], positive exactly when the incumbent's value sometimes falls where the two classes differ in their chance of beating it; the covariance after the ceiling at every prior, 2 pi (1 - pi) rho lambda E_F[D(R)], with zero covariance with entry; the two channels and the second difference at prior 1/2; the trend with the prior and slot fixed under outbidding; the example's numbers (referee/W4.md "Solver C 1, Solver B 3, and Solver E 1(a)-(b)", "the covariance constants agree", "Solver E 1(c)-(d)", "High-class outbidding", "Exact uniform-family condition");
- A.14, announcements: (i) and (ii) as now; (iii) the mean return to a preparation report is positive exactly when preparation is still uncertain after some order, at every prior and in every equilibrium, with B_F(pi) < c_H sufficient (the example clears it by the margin 1.196); (iv) refers to A.11 (W5 "Announcement returns" eqs (21) and (22)); the proofs of (iii) and (iv) use the prior pi where the present text uses the even prior.
No open proof is assigned to this area, but check every hypothesis of W4 and W5 with care: two-sided trade, one public state, the prior below the threshold for the weighted test, the prior and slot fixed for the winner trend.
```

## Referee, per area

```text
Task: referee the Stage S4 statement freeze for area <area> (<area name>). You did not write the text under review. Files: audit/theory_upgrade_2026_10_25/statements/<area>.tex, <area>_notes.md, and every folder statements/O<n>/ that the notes name (the open proofs of this area).

Read PLAN.md (S4, Part 5, Part 6), plan/NOTATION.md, the referee report(s) for this area in full, and the WORKAROUNDS.md sections for it. For each statement, decide: does every conclusion follow from the referee reports' proofs under exactly the stated hypotheses? Is every qualifier present (PLAN.md S4 acceptance: prior 1/2 and the mixing investor for research; two-sided trade for the tests; a prior below the threshold for the weighted test; prior and slot fixed for the winner trend; tie rules; weak against strict; the threshold above the prior at the start of a path)? Is anything overclaimed? Does the numbering follow decision 7 and PLAN.md Part 6? Do the language rules hold? Mark each statement "accept", "missing qualifier", "overclaim" or "wrong", with the fix. For each open proof, check every step as a referee would, run its computation if there is one, and give a verdict. Build the statements file into <private folder>/ref<area>/build and read the PDF.

Write audit/theory_upgrade_2026_10_25/statements/<area>_referee.md with your verdicts, each issue with severity (blocker, should fix, minor) and location, and what you recomputed. Do not edit the files under review.
```

## Mathematics writer, fixes after the referee

```text
Task: apply the referee's findings to your Stage S4 work for area <area>. The referee's report is audit/theory_upgrade_2026_10_25/statements/<area>_referee.md; its issues (JSON): <the referee's issues>
Fix every blocker and "should fix", and a minor one when it is cheap; where you disagree, give the mathematical reason in <area>_notes.md. Rebuild the statements file into <private folder>/w<area>/build2 and read it, rerun any changed computation, and add a short "Changes after the referee" section to <area>_notes.md.
```

## Prose writer: main-text wording targets

```text
Task: Stage S4, the main-text wording targets (PLAN.md "S4. Statement freeze and the open proofs": "The prose writer drafts the main-text wording targets (lens_maintext.md 3.1)").

Read first: PLAN.md in full (Part 1, Part 2, S4, S9 and S10, Part 6, Part 9), plan/DECISIONS.md, plan/NOTATION.md (the rule card, the vocabulary and the symbols bind every word you write), plan/lens_maintext.md in full (above all 2.0, 3.1, 3.3, 3.6 and 3.7), the style guide, the current main text slot/manuscript/sections/*.tex and the abstract in slot/manuscript/main.tex, and the referee reports referee/W1.md to W5.md for the scope of each result (their statements are the authority on what is true).

At the same time, the mathematics writer drafts the formal statements in statements/A.tex, B.tex, C.tex and D.tex. Do not read or wait for them, and do not edit them. Your targets are checked against them later by an independent referee, who marks each target "match", "missing qualifier" or "overclaim".

Deliverable: audit/theory_upgrade_2026_10_25/statements/wording_targets.md. It holds the target wording of every main-text claim that the update changes or adds, in the order of the paper, written as LaTeX source as it will stand in the manuscript:
- the four propositions in their short main-text form, with descriptive titles (Proposition 3 is "Quiet and informative markets");
- Corollaries 1, 2 and 3, the example's results (Corollary 1 after Proposition 2, Corollary 2 after Proposition 3, Corollary 3 after Proposition 4), with the example introduced once at the opening of Section 4.2 and named neutrally ("the example", or by its primitives);
- the sentences of lens_maintext.md 3.1 that state a result: the intuition sentence after each result, the two-numbers passage of Section 3, the takeover-share and decisive-advantage sentences of Section 4.1, the four predictions of Section 8, and the result sentences of the introduction, the abstract and the conclusion.
For each target give: the location (section, and the current file:line it replaces, or "added after file:line"), the LaTeX text, the formal result it must match (by the PLAN.md S5 item and the referee report section), and its scope list (prior, tie rules in the plain phrases of NOTATION.md, trading pattern, named condition, weak against strict). Every number prints through \reg{key}; where a key does not exist yet, write \reg{NEW:short_name} and list it at the end with the quantity it stands for.

Adjust lens_maintext.md 3.1 for the rules: it says "the benchmark" (rule 4 replaces it), it uses some retired words (NOTATION.md part (b) decides), and it may leave a qualifier implicit. Acceptance, from PLAN.md S4: no overclaim and every qualifier present: prior 1/2 and the mixing investor for research; two-sided trade for the tests; a prior below the threshold for the weighted test; prior and slot fixed for the winner trend. Numbers from economies other than the example appear in the main text as words or formulas only. The introduction states each result in its general form, with numbers from the example only as illustrations, marked as such; there is no empirical sentence in the abstract.

End the file with a list of open points for the referee: each target whose scope you could not settle from the referee reports, with the reason.

Run the language scan on the file and judge each hit; report the counts and your judgements in notes_for_coordinator.
```

## Referee of the wording targets

```text
Task: referee the main-text wording targets of Stage S4. You did not write them. File under review: audit/theory_upgrade_2026_10_25/statements/wording_targets.md (the prose writer's). The frozen formal statements are statements/A.tex, B.tex, C.tex and D.tex with their notes A_notes.md to D_notes.md and referee reports A_referee.md to D_referee.md, and the open proofs in statements/O<n>/.

Read PLAN.md (Part 1, S4, S9 and S10, Part 6), plan/NOTATION.md, and the four statement files in full. For each target, compare it with the formal statement it must match and mark it:
- "match": every conclusion follows from the formal statement under the hypotheses the target states;
- "missing qualifier": a hypothesis of the formal statement is absent (prior 1/2 and the mixing investor for research; two-sided trade for the tests; a prior below the threshold for the weighted test; prior and slot fixed for the winner trend; tie rules; weak against strict; the threshold above the prior at the start of a path; any named condition);
- "overclaim": the target says more than the formal statement proves;
- "wrong": the target contradicts it.
Give the fix for each mark other than "match". Settle the open points at the end of the file from the formal statements and the open proofs (O2, O3, O4, O6, O9 and the others). Check the language rules and NOTATION.md vocabulary in every LaTeX target, and that every number prints through \reg. Acceptance (PLAN.md S4) requires no overclaim and every qualifier present.

Write audit/theory_upgrade_2026_10_25/statements/wording_referee.md: a table of every target with its mark and fix, the settled open points, and any formal statement that itself looks inconsistent with another (report it; do not edit the statement files). Do not edit the file under review.
```

## Prose writer: fixes to the wording targets

```text
Task: apply the referee's findings to the main-text wording targets of Stage S4, which you wrote earlier in statements/wording_targets.md. The referee's report is audit/theory_upgrade_2026_10_25/statements/wording_referee.md; its issues (JSON): <the referee's issues>
Read the frozen statements statements/A.tex to D.tex where a fix needs them. Fix every mark other than "match" and every settled open point; where you disagree, give the reason in a section "Changes after the referee" at the end of wording_targets.md, which also lists every change. Replace a \reg{NEW:...} placeholder by the key the statement notes give, where they give one. Run the language scan on the file and judge each hit.
```
