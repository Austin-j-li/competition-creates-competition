# Final independent math audit: core

Target: `slot-revision`, commit `c78e2c3f48c8528b60dbed100643653228cde222`.
Baseline: `2c56325`.
All manuscript paths below start at `slot/manuscript/`.

Verdict: the core propositions, their proofs, the structural moves, and the benchmark numbers remain correct.
The general control paragraph loses one required hypothesis. Two minor prose and notation issues also remain.
No finding requires a change to a core proposition or a registry value.

## Part 1. Findings

FINDING:

- Name: The control paragraph omits the restriction on the challenger's value and the signal
- Severity: High
- Location: `sections/04_equilibrium_results.tex:189` (conditions at lines 189–192; conclusion at lines 193–195)
- Problem: The paragraph omits conditional independence between the challenger's value and the signal, so its explicit conditions do not imply the stated control.
- Proposed fix: Add that, given the class, the signal carries no information about the challenger's value.
- Evidence: The baseline control theorem in `appendix/A6_robustness.tex` said, “Let the value depend on S only through the class.” Correction M2 strengthened this theorem to the product-law condition. Commit `904924f` also stated that exact condition in Section 4. The final paragraph instead fixes the law of the class and signal, the class value laws, and the cost law. It then requires signal–incumbent independence and conditional independence between the two values. It does not require the challenger's conditional value law, given the class and signal, to equal its class law.

  The final appendix retains the necessary condition at `appendix/A6_robustness.tex:11`:

  \[
  \mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i.
  \]

  Thus M2 remains correct in the theorem, but its main-text translation loses the restriction on \(\theta\).

  A counterexample satisfies all conditions explicitly listed in the final paragraph. Let \(j\) and \(S\) be independent, fair binary variables. Fix

  \[
  G_L=\tfrac12\delta_1+\tfrac12\delta_3,\qquad
  G_H=\tfrac12\delta_2+\tfrac12\delta_4,
  \]
  \[
  p=\tfrac12,\qquad \rho=\tfrac14,\qquad c_H=\tfrac{21}{10}.
  \]

  In economy 0, let \(R\sim U[0,1/2]\), and make \(\theta\) independent of \(S\) within each class. In economy 1, let \(R\sim U[0,3/5]\). Let \(S\) select the lower or upper class value there. Keep \(R\) independent of all other draws in each economy.

  The class laws, the joint class–signal law, and the independent cost law stay fixed. The incumbent strengthens. The signal tells nothing about \(R\), and the values remain independent given \((j,S)\). But the omitted conditional law of \(\theta\) changes.

  Economy 0 gives gross profit \(2<21/10\) after either signal. Economy 1 gives gross profits \(119/120\) and \(359/120\). Entry therefore rises from \(1/4\) to \(5/8\). The omitted condition rules out precisely this change in information about values. This example challenges the prose conditions, not the final appendix theorem.

FINDING:

- Name: The return bound extends beyond correctly signed orders
- Severity: Low
- Location: `sections/03_competition_information.tex:111`
- Problem: The sentence applies a positive return bound to every order, although the appendix bounds only correctly signed gross returns.
- Proposed fix: Restrict the sentence to the gross returns of correctly signed, nonzero orders.
- Evidence: The baseline and final text both say that “the investor's return after every order stays at least a fixed share of the spread.” This issue is inherited. Lemma A.3 at `appendix/A2_beliefs_trading.tex:178` instead gives \(U_j(0)=0\) and negative payoffs for wrong-signed orders. Its lower bound at lines 188–189 applies only to

  \[
  K_H=e(1)\Delta_T[1-\mu(1)],\qquad
  K_L=e(-1)\Delta_T\mu(-1).
  \]

  These are gross returns. When \(\Delta_T>0\), the bound \(\rho\kappa\Delta_T\) is positive. It cannot bound abstention or a wrong-signed order from below. Even a correctly signed net payoff can be negative, as it is at the weak benchmark incumbent. The formulas in Section 3.3 remain correct.

FINDING:

- Name: The revised objective precedes its notation
- Severity: Low
- Location: `sections/02_model.tex:194`
- Problem: The objective uses \(e(q)\) and \(t_j\) before the main text defines them, contrary to the brief's notation requirement.
- Proposed fix: Define \(e(q)\) and \(t_j\) before the investor's objective, and keep their current meanings.
- Evidence: The baseline defined \(t_j\) before Definition 1 and defined \(e(x)\) before its investor-optimality condition. The final main text first uses both symbols in the objective at line 194. It explains them at lines 196–198 and defines the class expectation at line 204. The moved definition in `appendix/A1_payoffs.tex:29` still defines \(e(x)\) before its objective at line 41. No formula or object changes; only the main-text order fails the requested definition-before-use rule.

## Part 2. Coverage

### Main-text claim groups

Each line records a checked claim group. Exceptions refer to Part 1.

- `main.tex:85–89`: the opposing auction and information forces agree with Proposition 1 and Lemma A.3; the residual advantage concerns information and correctly signed trade.
- `main.tex:91–94`: the open-set reversal, unique outcomes, higher entry, and higher high-class ownership hold on the benchmark neighborhood of Proposition 2.
- `main.tex:93–95`: the slot control and the rise followed by constant entry agree with A.6 and Proposition 3 under the default tie rules.
- `main.tex:95–97`: the research summary agrees with the merged Proposition 4; the access claim agrees with Proposition A.8 in A.7.
- `sections/01_introduction.tex:3–23`: the direct deterrence force and the transfer of the class value gap agree with A.1.
- `sections/01_introduction.tex:25–32`: alternative arrivals, full support, posterior bounds, and the shareholder proceeds argument agree with A.2 and A.7.
- `sections/01_introduction.tex:34–47`: the three economies, uniqueness, entry recruitment, return to the floor, and the slot control agree with A.3 and A.6.
- `sections/01_introduction.tex:49–59`: the benchmark comparisons, entry ceiling, exact slot band, and posterior thresholds agree with A.3 and the registry.
- `sections/01_introduction.tex:61–66`: coexistence, mixed purchases, the constant segment, and the prior window agree with A.4.
- `sections/01_introduction.tex:91–95`: M8 retains the regime above the entry ceiling; A.8 supports the impact, winner, and identification summaries in that regime.
- `sections/02_model.tex:44–57`: the common payoff shift, monetary rescale, continuous incumbent law, and uniform-strength interpretation preserve the baseline model.
- `sections/02_model.tex:59–85`: the class laws, class ranking, equal admissibility, weakest restriction, and benchmark order agree with A.1.
- `sections/02_model.tex:87–111`: the cost law, independence, truthful bids, reserve admissibility, no-entry proceeds, and absence of value ties agree with Definition A.1 and A.1.
- `sections/02_model.tex:115–157`: the slot probabilities, order payoff, likelihood ratio, and posterior bounds agree with Lemma A.1, including the zero-order restriction on \(\beta\).
- `sections/02_model.tex:164–170`: the moved Laplace remark retains the likelihood-ratio bound and its limited equivalence to the slot.
- `sections/02_model.tex:174–199`: the information sets, sequence, equilibrium conditions, and investor objective preserve Definition A.1; the notation order has Finding 3.
- `sections/02_model.tex:201–219`: the class expectations, gross-profit mixture, price formula, and presence factor agree with A.1–A.2.
- `sections/02_model.tex:221–231`: default ties, fixed-candidate deviations, entry, ownership, and the win probability preserve the baseline definitions.
- `sections/03_competition_information.tex:5–35`: the auction payoffs, value split, closed forms, and derivative signs agree with A.1.
- `sections/03_competition_information.tex:37–58`: Proposition 1 preserves the general integral identities, weak signs, and sufficient conditions for strict signs.
- `sections/03_competition_information.tex:60–83`: the conditional-value proof, reserve term, split identity, and benchmark limit agree with A.1.
- `sections/03_competition_information.tex:87–108`: posterior bounds, price pooling, the ceiling, the threshold equivalence, and price sufficiency agree with Lemmas A.1–A.2 and Corollary A.1.
- `sections/03_competition_information.tex:110–113`: the entry floor is correct; the sentence about returns has Finding 2.
- `sections/03_competition_information.tex:117–143`: the two gross returns, bounds, wrong-signed losses, best responses, prior comparison, cancellation, and split between orders agree with Lemma A.3.
- `sections/04_equilibrium_results.tex:5–44`: Proposition 2 retains every hypothesis and conclusion, including the exact ownership condition.
- `sections/04_equilibrium_results.tex:46–73`: the cost windows, prior effect, open set, sufficient ownership condition, and tie independence agree with A.3.
- `sections/04_equilibrium_results.tex:77–120`: the declarations, auction table, three equilibrium tuples, prices, entry, ownership, and proceeds agree with independent recomputation.
- `sections/04_equilibrium_results.tex:122–166`: the exact region, prior ranges, threshold interpretation, entry ceiling, and hypothesis margins agree with A.3 and A.9.
- `sections/04_equilibrium_results.tex:174–186`: the belief-figure notes preserve the threshold and posterior-band claims.
- `sections/04_equilibrium_results.tex:188–199`: the slot control is correct; the general experiment loses the hypothesis in Finding 1.
- `sections/04_equilibrium_results.tex:203–252`: both control panels and the entry-crossing probabilities agree with A.6 and independent recomputation.
- `sections/04_equilibrium_results.tex:256–282`: the threshold descriptions and shortened Proposition 3 agree with the full statement in A.4.
- `sections/04_equilibrium_results.tex:284–324`: the two computer-assisted steps, threshold values, entry examples, sale rates, branch mechanism, and additional mixed equilibrium agree with A.4.
- `sections/04_equilibrium_results.tex:298–307`: the coexistence-figure notes preserve the default rules and identify the additional threshold branch under the alternative challenger rule.
- `sections/04_equilibrium_results.tex:326–331`: the prior windows and absent-coexistence cases agree with Corollary A.2.

### Structural moves and proof attachments

- The class-ranking assumption becomes equation `eq:classes` in Section 2; its two restrictions stay unchanged.
- Definition 1 becomes Definition A.1 in A.1; its statement is identical after whitespace normalization.
- The liquidity law \(\eta\) moves before Definition A.1; its probabilities stay unchanged.
- The order notation \(\delta_q\), the mass \(b_0\), and the odds identity move to A.2; their objects stay unchanged.
- Lemma 1 becomes Lemma A.1; its statement is identical after whitespace normalization, and its four-part proof remains attached.
- Corollary 1 becomes Corollary A.1; its statement is identical after whitespace normalization, including its strict cost comparison.
- Lemma 2 becomes Lemma A.2; its statement is identical after whitespace normalization, and its alternative-rule clause remains present.
- Lemma 3 becomes Lemma A.3; its statement is identical after whitespace normalization, including the profile scope and gross-return bounds.
- Proposition 3's full statement in `appendix/A4_coexistence.tex:289` preserves the baseline threshold order, six-row equilibrium set, entry formulas, and three conclusions.
- Proposition 3's shortened main statement preserves the coexistence interval, branch formula, continuity, strict segment, constant segment, ceiling, and existence claim.
- Corollary 2 becomes Corollary A.2; its statement is identical after whitespace normalization, including all four prior cases.
- The definitions before Corollary A.2 preserve \(r_N(\pi)\), \(r_C(\pi)\), \(r_\pi\), and the three prior boundaries.
- Remark 1 moves to the tie-rule paragraph in A.4; both alternative rules retain their intervals and endpoint conventions.
- The alternative tie definitions move from Section 2 to A.4; the default choices remain explicit in Section 2.
- Proposition 4(a) preserves old Corollary 3; Proposition 4(b) preserves old Proposition 4 and its six-strength equilibrium lists.
- The investor-tie sentence from old Proposition 4 remains in Section 5 immediately after the new proposition; the proof headings now point to parts (a) and (b).
- M7 limits the cap-region result to the equilibrium patterns of Proposition 4(b); it supplies the variable-cap entry formula.
- The continuous-order remark moves from old Section 6.4 to the Section 2.3 footnote without a mathematical change.
- Proposition numbering remains stable; the full statement in A.4 uses an unnumbered environment and adds no proposition number.
- Every source reference in the main manuscript and appendices resolves; the final build reports no undefined or duplicate references.

### The eleven corrections

- M1: retained at `appendix/A3_proposition2.tex:169` and `:207`; the lower boundary gives zero orders at \(r_0\) and full orders at \(r_1,r_2\).
- M2: retained in the A.6 statement, proof, and slot application; its general main-text translation has Finding 1.
- M3: retained throughout A.4; \(s_-^*(r)\) denotes the sale rate, while \(t_L\) denotes low-class proceeds.
- M4: retained at `appendix/A6_robustness.tex:468`; independent arithmetic reproduces all five positive rational margins.
- M5: retained at `appendix/A6_robustness.tex:543`; the net sale payoff subtracts \(1/50\), and its root remains \(4b/3\).
- M6: retained at `sections/06_robustness.tex:42`; dispersion weakly raises gross profit.
- M7: retained at `appendix/A5_research.tex:317` and `sections/05_research.tex:155`; the reference concerns patterns, and entry depends on the cap.
- M8: retained at `sections/01_introduction.tex:93`; the winner prediction uses the regime above the entry ceiling.
- M9: retained at `appendix/A6_robustness.tex:270`; the negative quantity is a signed profit gap.
- M10: retained at `appendix/A5_research.tex:196`; the positive purchase payoff requires positive research, and the zero-research case cites Step 1.
- M11: retained at `appendix/A6_robustness.tex:239` and `:253`; only the four rows with a third strength claim (H3).

### Numbers, signs, and notation

- The core main text uses 127 distinct registry keys, after comments are removed; every key exists, and `numbers.tex` has no change from the baseline.
- Independent arithmetic reproduces the auction payoffs, posterior values, prices, entry, ownership, proceeds, region bounds, margins, thresholds, and branch examples.
- The introduction's three research intensities and entry values agree with the research equation and registry.
- The core panels of A.9 agree with independent arithmetic, including all threshold gaps and the alternative-rule endpoint margin.
- Exact rational bounds on Euler's number give \(\tau(r_2)-M=0.00033356471940931785\ldots>0\).
- The same calculation gives \(c_H-B_{r_2}(M)=0.00268890226590511226\ldots>0\) and \(r_2-r_C=0.00734148120533816666\ldots>0\).
- Independent rational algebra reproduces both derivative polynomials in A.4; Sturm variations are 3 to 3 for \(J\), and 5 to 5 for \(\Delta_T(1-\tau)^2\), on their stated intervals.
- The main core keeps distinct meanings for prices, posteriors, the two entry objects, ownership, Euler's number, and the payoff spread; Finding 3 records the definition-order exception.
- The sale-rate rename resolves M3 in the formulas, equilibrium tuple, and proof; no residual use of \(t_L\) for that rate remains in A.4.

### Method and limits

I read the brief in full, the project rules, all assigned core files, and A.9 in full.
I compared the core changes with `git diff 2c56325 -- slot/manuscript` and the baseline source.
I also read the extension passages needed for M2 and M4–M11, the Proposition 4 merge, and the abstract summaries.

I built the real manuscript with the specified `latexmk` interface and its real source inputs.
The output is `/tmp/ccc_slot_scan/final/build_core/main.pdf`, with 102 pages.
The final log contains no undefined-reference, duplicate-label, or unknown-registry-key warning.
This build verifies compilation and references; it is not evidence for the mathematics.

The independent calculations are in `/tmp/ccc_slot_scan/final/scripts_core/`:
`source_core.py`, `numbers_core.py`, `polynomials_core.py`, and `intervals_core.py`, with their logs.
These scripts print source comparisons or mathematical values; none contains an assertion.
No test suite ran. No repository file changed, and the checkout remained clean.

I did not conduct a full independent audit of Sections 5–9 or Appendices A.5–A.8.
I did not recompute the extension-only panels of A.9, beyond the cited correction checks.
I did not audit `slides.tex`, `comparison.tex`, empirical source material, or figure geometry.
