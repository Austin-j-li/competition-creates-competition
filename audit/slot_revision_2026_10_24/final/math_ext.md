# Final independent audit: extensions

Target: `slot-revision`, commit `c78e2c3f48c8528b60dbed100643653228cde222`.
Baseline: `2c56325`. Scope: the extensions specified in `brief_ext.md`.

The extension propositions and the moved research statements preserve their mathematics. The numerical displays agree with independent calculations.
The main prose still needs the scope and definition repairs below. No finding changes the benchmark numbers or Proposition 4.

The shared branch advanced during this audit. Commit `da84b08` repairs Finding E1 in the live manuscript.
This report retains the requested `c78e2c3` target. All locations below refer to that target, which was the initial working tree.
The later commits are not part of this audit, except for the observed E1 repair.

All repository access was read-only. The audit wrote only files under `/tmp/ccc_slot_scan/final/` and ran no tests.

## Part 1: Findings

FINDING:

- Name: E1. The control prose omits part of the conditional-law restriction.
- Severity: High
- Location: `slot/manuscript/sections/08_empirical.tex:17`; the same statement appears at `sections/04_equilibrium_results.tex:189`.
- Problem: The prose fixes marginal class laws but permits changes in the signal's information about values within a class.
- Proposed fix: Require the conditional product law from Appendix A.6, including signal independence for the challenger's value within each class.
- Evidence: Baseline A.6 required the challenger's value to depend on the signal only through its class. Correction M2 strengthened this to

  \[
  \mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i.
  \]

  Commit `904924f` also printed this condition in Section 4. The target replaces it with fixed class value laws, incumbent-signal independence conditional on class, and conditional independence between values. These statements omit

  \[
  \mathcal L_i(\theta\mid j,S)=G_j.
  \]

  Appendix `A6_robustness.tex:9–24` still requires the full product law. Its proof uses that law to obtain gross profit \(B_{F_i}(\mu(S))\).

  An exact example shows the difference. Let \(p=1\), \(\pi=1/2\), and use equally weighted class laws

  \[
  G_L=\tfrac12\delta_1+\tfrac12\delta_3,
  \qquad
  G_H=\tfrac12\delta_2+\tfrac12\delta_4.
  \]

  Let \(R_0\sim U[0,1/2]\) and \(R_1\sim U[1/2,1]\), independently of all other variables. The second incumbent is stronger.
  Let the independent cost equal zero with probability \(1/4\), and equal two otherwise.
  Keep the same independent, fair binary signal and class law in both economies.
  In economy zero, let the signal be independent of the within-class value draw. In economy one, let it reveal that draw.
  The marginal class laws and the joint law of class and signal remain fixed.
  Gross profit is \(3/2\) in economy zero. It is \(1/2\) or \(5/2\) in economy one.
  Entry rises from \(1/4\) to \(5/8\), despite every independence restriction stated in the target prose.
  The appendix condition excludes this example. The slot control itself remains valid.

  **Later repair observed:** `da84b08` restores signal independence for both values and incumbent independence from class in both main-text locations.

FINDING:

- Name: E2. Recruitment at the top posterior does not alone imply flat entry.
- Severity: Mid
- Location: `slot/manuscript/sections/07_welfare.tex:69–72`; also `sections/01_introduction.tex:87–89` and `sections/09_conclusion.tex:17–18`.
- Problem: The general reserve summary omits exclusion at the prior, which the flat-entry result requires.
- Proposed fix: State that full orders prevail and only a purchase recruits at both strengths, or give the missing prior-profit condition.
- Evidence: The baseline says, “If the top posterior recruits at both strengths, entry is flat in incumbent strength.” The target retains this claim.
  Appendix `A7_welfare.tex:163–184` instead assumes

  \[
  k<\rho\kappa\min\{\Delta_0,\Delta_1\},
  \qquad B_0(\pi)<c_H<B_1(M).
  \]

  The prior restriction excludes recruitment after the zero order at both strengths. Recruitment at the top posterior does not supply that restriction.
  Keep the benchmark inputs, except set \(p=1.1\) and \(c_H=4.3\). The reserve excludes the low class.
  Full orders are uniquely optimal at both strengths. Their global margins are approximately \(0.048076\) and \(0.047572\).
  The prior profits are \(4.447917\) and \(4.149167\). The top profits are \(6.503375\) and \(6.066568\).
  Thus the top posterior recruits at both strengths, but the zero order recruits only at the weak strength.
  Entry falls from \(0.727243\) to \(0.522757\).
  This omission is inherited from the baseline. The stated benchmark reserve examples remain correct.

FINDING:

- Name: E3. The signal discussion turns a sufficient-condition failure into a necessity claim.
- Severity: Mid
- Location: `slot/manuscript/sections/06_robustness.tex:85–87`.
- Problem: The prose says that a more accurate buyer signal needs other costs and strengths, while the appendix excludes only the proposition's sufficient conditions.
- Proposed fix: Restore the statement that the sufficient conditions cannot hold at the benchmark when \(d\ge a_T\).
- Evidence: The baseline says, “At the benchmark B, the conditions cannot hold with \(d\ge a_T\).”
  The target instead says, “A buyer signal at least as accurate as the investor's needs other costs and strengths.”
  Appendix `A6_robustness.tex:508–510` derives a contradiction between the two uniform trading bounds of Proposition `prop:signals`.
  It does not characterize all signal equilibria over \(d\ge a_T\), or prove that every entry reversal there is impossible.
  Indeed, `A6_robustness.tex:522–555` studies equilibria after those bounds fail.
  Failure of a sufficient condition is not a necessary condition for the economic phenomenon.
  This is a stronger claim introduced by the rewrite.

FINDING:

- Name: E4. The zero-order statement needs the full-trade regime.
- Severity: Mid
- Location: `slot/manuscript/sections/08_empirical.tex:56–57`.
- Problem: The statement about every strength below the entry ceiling omits the full two-sided trade restriction.
- Proposed fix: Restrict the statement to full two-sided trade on \(r_S<r\le r_C\).
- Evidence: The baseline says that below the ceiling, no order is bad news about entry and no news about class.
  The target retains that statement and adds the symbol \(r_C\).
  Appendix `A8_empirical.tex:208–209` explicitly starts the corresponding result with “Under full two-sided trade.”
  Under that restriction, \(\mu(0)=1/2\), and

  \[
  P(0)-\mathbb E[P(X)]
  =-(1-\rho)\chi_r(b+\lambda/2)A_r(M).
  \]

  The section's opening declares the benchmark and slot band. It states where full trade holds, but does not restrict every subsequent statement to that interval.
  At \(r=1.6<r_C\), the purchases-only equilibrium instead has

  \[
  \mu(0)=\frac{b_0}{2b_0+\lambda}\approx0.309329<\frac12.
  \]

  No order is then bad news about class. Appendix `A8_empirical.tex:240–244` gives this same equilibrium.
  In the no-trade equilibrium, no order carries no news about entry either.
  This scope omission is inherited. The numerical claim at \(r_1\) is correct.

FINDING:

- Name: E5. The payment-rule strictness claim omits its support restriction.
- Severity: Mid
- Location: `slot/manuscript/sections/07_welfare.tex:43–48` and `:55–57`.
- Problem: The prose applies the strictness condition without stating that the high-class value exceeds every incumbent value.
- Proposed fix: State the point-mass classes and the incumbent support condition \(0<\ell<\bar r<h\) before the comparative static.
- Evidence: The baseline and target both claim strictness when \(\mathbb E[(R-\ell)_+]\) changes strictly and \(\omega\ne1/2\).
  The target also says that a high-class challenger wins when \(R>\ell\).
  Appendix `A7_welfare.tex:103–104` imposes point masses and \(0<\ell<\bar r<h\).
  Its proof at `:127–131` uses the support restriction to exclude the case \(R\ge h\).
  Without it, the correct point-mass spread is

  \[
  \Delta_\omega
  =\omega(h-\ell)
   +(1-2\omega)\mathbb E[(\min\{R,h\}-\ell)_+].
  \]

  For \(\ell=1\), \(h=10\), compare continuous laws \(U[11,12]\) and \(U[12,13]\).
  The incumbent strengthens, and \(\mathbb E[(R-\ell)_+]\) rises strictly. The spread stays at \((1-\omega)(h-\ell)\).
  The high-class challenger loses in both economies.
  This is an inherited scope omission. The benchmark coefficient \(13/20\) and the statement at \(\omega=1/2\) remain correct.

FINDING:

- Name: E6. The main text never defines the reference price for an impact.
- Severity: Low
- Location: `slot/manuscript/sections/08_empirical.tex:22–27` and `:43`.
- Problem: The decomposition and identification claims use purchase and sale impacts without defining their reference price in the main text.
- Proposed fix: Define the purchase impact as \(P(1)-P(0)\) and the sale impact as \(P(0)-P(-1)\) before use.
- Evidence: The baseline defines the spread but leaves both impacts implicit. The target moves the impact comparison before even the spread definition.
  Appendix `A8_empirical.tex:41–43` defines both impacts relative to the price after a zero order.
  That price differs from the mean price before the opportunity in the recruitment regime.
  At \(r_1\), the sale impact used by the theorem is approximately \(0.038510\).
  The mean price before the opportunity minus the sale price is approximately \(0.296458\).
  The latter contains an entry component and cannot replace the former in the identification formula.
  This definition gap is inherited, but the reordered prose makes the first use earlier.

FINDING:

- Name: E7. The rewrite removes the definition of the benchmark label B.
- Severity: Low
- Location: `slot/manuscript/sections/06_robustness.tex:67`; definition removed at `sections/04_equilibrium_results.tex:77`.
- Problem: The main text uses \(S(B)\) after it removes the definition of \(B\) as the benchmark parameter vector.
- Proposed fix: Restore the benchmark label at its declaration, or rename the signal vector without the undefined argument.
- Evidence: The baseline starts the benchmark declaration with “The benchmark, which I call \(B\).”
  The target starts it with “The benchmark has” and gives no replacement definition of the label.
  Section 6 nevertheless uses \(S(B)\), while \(B(\mu)\) already denotes gross acquisition profit.
  Appendix `A9_parameters.tex:49–58` retains the calibration label and defines the signal vector relative to it.
  The vector's numerical primitives remain clear. The defect is the missing main-text definition.

## Part 2: Coverage

The following checks passed, subject to the explicit exceptions in Part 1.
The default tie rules remain in `sections/02_model.tex:221`. Their prose definitions preserve IM and C1 without their abbreviations.
Thus removal of repeated tie-rule labels does not by itself remove a hypothesis.

### Main-text claim groups

- Abstract, `main.tex:93–97`: the slot control, research comovement, and welfare comparison agree with A.5–A.7 under their stated regimes.
- Introduction, `01_introduction.tex:68–74`: the weak and strong research outcomes, three intermediate values, and branch comovement agree with A.5.
- Introduction, `01_introduction.tex:76–81`: ranked classes, arbitrary priors, cost laws, group separation, and the complementary-signal example agree with A.6.
- Introduction, `01_introduction.tex:83–89`: welfare and payment summaries agree with A.7; the general reserve summary has exception E2.
- Introduction, `01_introduction.tex:91–95`: the spread share, winner prediction above the ceiling, and identification formula agree with A.8 in the full-trade regime.
- Research, `05_research.tex:3–19`: research technology, cost, cap, success independence, and replacement of liquidity orders agree with A.5.
- Research, `05_research.tex:21–27`: hidden research, optimal orders after a hypothetical success, and the unique best research response preserve E7.
- Research, `05_research.tex:29–42`: posterior bounds, the recruitment intensity, the root equation, and root uniqueness agree with A.5.
- Research, Proposition 4(a), `05_research.tex:53–58`: the derivative, entry formula, ownership formula, and strict signs match the former Corollary 3.
- Research, Proposition 4(b), `05_research.tex:59–68`: all six strengths, equilibrium counts, strict inequalities, cap outcomes, and entry values match the former Proposition 4.
- Research, `05_research.tex:73–82`: the weak bound, the intermediate self-confirmation argument, the strong bound, and investor tie independence match their proofs.
- Research, Table 4, `05_research.tex:84–107`: every research, threshold, posterior, entry, and ownership display agrees with independent calculations.
- Research, `05_research.tex:109–118`: research and entry rise across the three strengths; the purchase probability and positive entry derivative are correct.
- Research, `05_research.tex:120–127`: the interval endpoints, cap transition, zero-research coexistence, and cap entry agree with A.5.
- Research, `05_research.tex:129–145`: the sufficient strong-incumbent threshold and the unresolved interval retain their scope; the caption retains C1.
- Research, `05_research.tex:149–153`: the later research onset and the distinction between an order mixture and research intensity agree with the two constructions.
- Research, `05_research.tex:155–161`: the cap strip, cost window, beta interval, and cap-dependent entry formula preserve M7.
- Robustness, `06_robustness.tex:9–15`: the cost-support restrictions preserve the floor, unique orders, and the two-strength reversal.
- Robustness, `06_robustness.tex:17–23`: the narrow-band return, wider-band entry at the third strength, and continuous weak decrease under atomlessness agree with A.6.
- Robustness, `06_robustness.tex:27–36`: the quantifiers over ranked classes, distinct means, priors, and slots match the construction near the first class difference.
- Robustness, `06_robustness.tex:38–43`: the wide-class comparison and weak convexity claim agree with the auction kernel and preserve M6.
- Robustness, `06_robustness.tex:45–53`: group separation, fixed within-group proportions, posterior-vector revelation, and the three-class collision agree with A.6.
- Robustness, `06_robustness.tex:57–73`: the signal theorem, price sufficiency, exact witness, separate signal vector, and two-source complementarity agree with A.6.
- Robustness, `06_robustness.tex:75–81`: the mixed orders, unique IM outcomes, lower entry, and nonexistence under I0 agree with A.6.
- Robustness, `06_robustness.tex:83–85`: the accurate-investor example and its no-buyer-signal control agree with A.6; the next sentence has exception E3.
- Welfare, `07_welfare.tex:5–22`: the access comparison, common orders and trade costs, positive total gains, and gains under capped research agree with A.5 and A.7.
- Welfare, `07_welfare.tex:24–27`: the liquidity transfer, trade scale, and shareholder threshold agree with A.7.
- Welfare, `07_welfare.tex:29–37`: the specified outside-region example and the external-dividend comparison agree with A.7.
- Payment rule, `07_welfare.tex:41–57`: the Nash transfer, profit effect, spread coefficient, and half-weight identity agree within the appendix support restriction; see E5.
- Reserves, `07_welfare.tex:61–65`: preparation, sale, and two admissible bidders remain distinct events.
- Reserves, `07_welfare.tex:74–109`: all table rows, proceeds gains, narrow-band comparison, exclusion requirement, and threshold values agree with A.7.
- Empirical, `08_empirical.tex:3–9`: the exact sale threshold and informed-share formula agree with A.8.
- Empirical, `08_empirical.tex:11–20`: the benchmark entry increase and hidden-price comparison are correct; the general control paraphrase has exception E1.
- Empirical, `08_empirical.tex:22–32`: the spread decomposition, asymmetry equivalence, hidden-price spread, and ceiling jump agree in the full-trade regime; see E6.
- Empirical, `08_empirical.tex:34–43`: the benchmark count interval, allowed upper endpoint under the default IM rule, alternative slot, and identification formulas agree with A.8.
- Empirical, `08_empirical.tex:45–51`: selection among prepared challengers, conditional winner gaps, and the order covariances agree with A.8.
- Empirical, `08_empirical.tex:53–58`: positive selected announcement returns and the zero unconditional mean agree with A.8; the zero-order sentence has exception E4.
- Empirical, `08_empirical.tex:60–65`: both cluster patterns and their order means and price difference agree under the default rules.
- Empirical, `08_empirical.tex:67–80`: the timing and measurement discussion preserves the need for scheduled opportunities and observed zeros.
- Conclusion, `09_conclusion.tex:3–18`: the mechanism, coexistence, research comovement, and welfare summary remain supported; the reserve summary has exception E2.

### Structural moves and proof attachments

- A.5 research tuple, `A5_research.tex:7–20`: the tuple, E1–E6, the zero-research continuation, E7, and fixed prices under joint deviations preserve the baseline Section 5 statement.
- A.5 posterior functions, `A5_research.tex:35–45`: the moved definitions of the intensity ratio, posterior bounds, and recruitment intensity preserve the baseline formulas.
- Proposition 4 merger: part (a) preserves former Corollary 3; part (b) preserves former Proposition 4, with its investor-tie statement retained in the following prose.
- Proposition 4 proof attachments, `A5_research.tex:233–283`: the former benchmark proof now proves part (b), and the former corollary proof now proves part (a).
- Remark A.1, `A5_research.tex:388–407`: the moved remark preserves the extra CM equilibrium, falling threshold-branch entry, ceiling exception, and full entry interval.
- The removed research-table row remains in Remark A.1, with all three threshold-equilibrium entry values unchanged.
- Continuous order sizes: former Section 6.4 appears in the footnote at `02_model.tex:164–170`, including the Laplace likelihood ratio and the different mass at the bound.
- Full Proposition 3, `A4_coexistence.tex:289–316`: the threshold order, equilibrium table, entry formulas, coexistence interval, and existence clause preserve the old main-text statement.
- A.6–A.8 proof attachments: every scoped proposition retains its proof and its substantive conditions; the corrections add no unsupported numerical conclusion.
- Cross-references: all references in the included manuscript resolve to source labels; no duplicate source label remains.
- Retired labels: the included source has no reference to `prop:researchbranch`, `rem:ties`, `rem:sizes`, `sec:sizes`, or `ass:classes`.
- Notation: all main-text symbols in the scoped extensions retain their definitions, except the benchmark label in E7; impact terminology has exception E6.

### Corrections M1–M11

- M1: retained in the A.3 statement and proof; the lower band boundary gives zero orders at the weak strength and full orders at the other two.
- M2: retained in A.6, including the slot-control product law; incomplete in the target main prose as E1 records, then repaired by the later live commit.
- M3: retained; the low-class sale rate is \(s_-^*(r)\), and \(t_L\) retains its target-proceeds meaning.
- M4: retained; exact rational arithmetic reproduces all five witness margins: \(21/400\), \(1363/36800\), \(2/1375\), \(603/31625\), and \(76753/18400\).
- M5: retained; the sale payoff includes \(-1/50\), and substitution of \(t=4b/3\) gives zero.
- M6: retained; the main text says that a mean-preserving spread weakly raises gross profit.
- M7: retained in A.5 and Section 5; the region concerns equilibrium patterns, and entry at the first strong strength depends on the cap.
- M8: retained; the introduction places the loss of entry prediction above the entry ceiling.
- M9: retained; A.6 states a signed profit gap, which is negative at the low prior.
- M10: retained; the positive purchase-payoff claim applies only to positive research, while the zero-research tuple has strict abstention.
- M11: retained; the moderate-gap row claims H1–H2 only, while the other four reversal rows also claim H3.

### Numerical evidence and limits

- `numbers.tex` is unchanged from the baseline through the target. It also remained unchanged through the observed later live commit.
- Independent calculations cover every derived display in Sections 5–8. Declared inputs were read separately from the registry.
- Appendices A.5–A.8 use 330 distinct registry keys: 257 derived displays and 73 declared inputs. Each is accounted for.
- The selected research and extension rows in A.9 use 132 keys. Each is covered by a calculation or an input declaration.
- The calculation file prints 574 derived registry values, including useful adjacent quantities. Every checked decimal agrees at its displayed precision.
- The research branch gives intensities \(0.237901\), \(0.279037\), and \(0.316683\); its entry values are \(0.507630\), \(0.513965\), and \(0.519763\).
- At cap \(0.33\), the corrected entry formula gives \(0.5218141375\), not the benchmark entry \(0.522757\).
- The access gains are \(0.257948\) in proceeds and \(0.081960\) in surplus. The spread at the first strong strength is \(0.786299\).
- The rounded-threshold example gives a sale margin of approximately \(-8.586806\times10^{-10}\), consistent with its printed negative sign.
- The source-label scan found no unresolved reference. The only apparent missing registry key was `<key>` in a source comment.

Calculation artifacts:

- `/tmp/ccc_slot_scan/final/scripts_ext/recompute.py`
- `/tmp/ccc_slot_scan/final/scripts_ext/numeric_values.tsv`
- `/tmp/ccc_slot_scan/final/scripts_ext/recompute.log`
- `/tmp/ccc_slot_scan/final/source_ext_c78e2c3/slot/manuscript/`

The decimal recomputation uses 70-digit arithmetic. It does not replace the manuscript's outward interval certificates.
The exact M4 fractions were also derived with rational arithmetic.
No test suite, assertion script, or original certificate program ran.
No PDF build or visual figure audit ran. Figure captions were read, but the plotted curves were not independently regenerated.
The core proofs in A.1–A.4 were read only for definitions, correction checks, and the structural comparison stated above.
This report does not repeat their full independent audit or their Sturm certificates.
It does not audit literature claims, `slides.tex`, `comparison.tex`, the later status-removal commit, or the full `da84b08` revision.
