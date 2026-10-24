## Part 1: findings

No findings in the reviewed core. The main statements agree with Appendix A.1–A.4, and the reviewed proofs are correct.

The review used branch `slot`, commit `2c56325c6c99a6db51dadb0bfe144575be28b170`. No repository file changed. No test or test suite ran.

## Part 2: coverage

The review covered the abstract, the introduction's core claims, Sections 2–4, Appendix A.1–A.4, and the core declarations and margins in A.9. Earlier audit verdicts were not read.

Independent computations are in `scripts/core_1/recompute.py`. Its output is in `recompute.log` in the same folder. `recomputed_values.csv` records each reviewed display. `rational_endpoints.json` records the exact rational endpoints.

**Model and auction payoffs**

- `sections/02_model.tex:43`: Checked the reserve, admissible bids, information, independence, preparation, and sale rules against all subsequent payoff formulas. The assumptions suffice.
- `sections/02_model.tex:88`: Checked the benchmark order restriction, money units, and common rescale claim. All three incumbent strengths satisfy the restriction.
- `sections/02_model.tex:140`: Re-derived the investor's profit and its conditional expectation. The arrival probability multiplies every available order payoff equally.
- `sections/02_model.tex:198`: Re-derived gross profit as the class-weighted average, with the posterior as its only information argument.
- `sections/02_model.tex:206`: Checked all six equilibrium conditions, price-based challenger beliefs, full support, and the fixed zero-cost preparation choice. Deviations retain the candidate's prices and preparation rule.
- `sections/02_model.tex:251`: Re-derived the competitive price from conditional terminal proceeds and independent preparation costs.
- `sections/02_model.tex:273`: Re-derived high-class ownership and its factorization into the prior, class-conditional entry, and the probability of an auction win. For the uniform incumbent, \(W_H(r)=\mathbb E_H[\min\{\theta/r,1\}\mathbf1\{\theta\ge p\}]\). It equals one in the benchmark.
- `appendix/A1_payoffs.tex:8`: Checked truthful bids against every competing bid, including values at and below the reserve. The weak-dominance argument is correct.
- `sections/03_competition_information.tex:20` and `appendix/A1_payoffs.tex:26`: Re-derived all six benchmark payoff formulas through direct integration. The script recomputes their values at all three strengths.
- `sections/03_competition_information.tex:31` and `appendix/A1_payoffs.tex:49`: Re-derived all derivatives. The spread rises strictly, and gross profit falls strictly at every fixed belief on the benchmark path.
- Proposition 1, `sections/03_competition_information.tex:41`, and `appendix/A1_payoffs.tex:59`: Checked the indicator integrals, Tonelli steps, finite integrals, and treatment of class atoms. The general formulas are correct:

  \[
  \Delta_T(F)=pF(p)D(p^-)+\int_p^\infty[1-F(y)]D(y)\,dy,
  \qquad
  g_j(F)=\int_p^\infty[1-G_j(y)]F(y)\,dy.
  \]

- Proposition 1(a)–(b), `appendix/A1_payoffs.tex:97`: Subtracted the formulas at the two incumbent distributions. The weak comparisons and stated strictness conditions follow with the correct signs.
- `sections/03_competition_information.tex:75` and `appendix/A1_payoffs.tex:89`: Checked the surplus split, its reserve term, and its simplification under equal admissibility.
- Proposition 1(c), `appendix/A1_payoffs.tex:113`: Re-derived the conditional payoff difference, including its jump at the reserve. The necessary and sufficient restrictions are correct:

  \[
  D(y)\ge0\quad(y>p),\qquad D(p^-)\le0.
  \]

  The shifted uniform distributions establish necessity. Right continuity converts the almost-everywhere restriction to the stated pointwise restriction. Without reserve atoms, the restrictions imply equal admissibility.

**Beliefs, prices, and trade**

- The belief lemma, `sections/03_competition_information.tex:97` and `appendix/A2_beliefs_trading.tex:28`: Checked every branch under arbitrary mixed profiles, including wrong-signed orders. Full support and both posterior bounds hold.
- The zero-order branch, `appendix/A2_beliefs_trading.tex:46`: Checked the likelihood-ratio bound with liquidity mass \(b_0\). The primitive restriction \(\beta\le1/3\) gives \(b_0\ge b\). For \(\beta>1/3\), the stated one-sided profile violates the bound exactly as claimed.
- `appendix/A2_beliefs_trading.tex:57`: Re-derived the posterior at a price that pools orders. It lies between the posteriors of those orders.
- The preparation-exclusion corollary, `sections/03_competition_information.tex:124` and `appendix/A2_beliefs_trading.tex:70`: Checked the upper posterior bound and the monotonicity of gross profit. The strict exclusion conclusion follows under both challenger rules.
- The price lemma, `sections/03_competition_information.tex:139` and `appendix/A2_beliefs_trading.tex:79`: Checked the entry floor, price formula, posterior sufficiency, entry threshold, and strict price order. Equal prices imply equal entry and equal posteriors.
- The trade lemma, `sections/03_competition_information.tex:168` and `appendix/A2_beliefs_trading.tex:126`: Re-derived all six order payoffs against fixed candidate prices and entry. Wrong-signed orders are strictly dominated.
- The trade bounds, `sections/03_competition_information.tex:183`: Checked every factor under arbitrary candidate profiles. The manuscript uses exactly

  \[
  \kappa(\pi)=\min\{m(\pi),1-M(\pi)\}.
  \]

  Thus \(\rho\kappa(\pi)\Delta_1\) is a valid common lower bound. The weak-economy upper bound \(\Delta_0\) is also valid.
- `sections/03_competition_information.tex:197`: Checked the symmetry identity, the expression through the smaller prior, and the maximum at prior one half.
- `appendix/A2_beliefs_trading.tex:163`: Checked where the liquidity restriction enters. The main equilibrium and coexistence proofs use only nonzero-order bounds and remain valid for \(0<\beta<1/2\).

**The three economies and the admissible region**

- Proposition “Competition creates competition,” `sections/04_equilibrium_results.tex:11` and `appendix/A3_proposition2.tex:11`: Checked each implication of (H1)–(H3). The uniqueness arguments bound every candidate before they impose the proposed orders.
- The weak tuple, `appendix/A3_proposition2.tex:23`: Checked all six conditions. Both classes abstain, every posterior equals the prior, and entry equals the floor. The common price correctly includes no-entry proceeds:

  \[
  P=t_0+\rho[t_L-t_0+\Delta_0\pi].
  \]

- The strong tuple, `appendix/A3_proposition2.tex:47`: Checked Bayes consistency, distinct competitive prices, challenger beliefs, preparation, all investor deviations, and truthful bids. Only a purchase recruits.
- The ownership comparison, `appendix/A3_proposition2.tex:75`: Re-derived

  \[
  \mathsf E_1=\rho+(1-\rho)(b+\pi\lambda),\qquad
  e_H=\rho+(1-\rho)(b+\lambda).
  \]

  The exact ownership condition and its stated sufficient condition are correct. In the benchmark, the high class always wins after preparation.
- The very strong tuple, `appendix/A3_proposition2.tex:88`: Checked all six conditions. Full orders remain optimal, all expensive preparation stops, and prices remain distinct.
- The tie-rule claim, `appendix/A3_proposition2.tex:107`: Checked strict investor and high-cost preparation comparisons in all three economies. All four stated rule pairs give the same outcome.
- The necessity example, `appendix/A3_proposition2.tex:124`: Recomputed the example with \(c_H=47/10\) and \(r_2=8\). Its weak-cost margin is \(-5/48\). Entry falls from one to approximately \(0.522757\). The weaker prior condition cannot replace (H1).
- The admissible-region proposition, `appendix/A3_proposition2.tex:157`: Re-derived both exact slot endpoints, the trade-cost endpoint, the prior intervals, and the boundary cases. The strict slot band is

  \[
  \frac{82}{59}<u<\frac{2686}{1559}.
  \]

  The separate trade-cost bound is \(u<19/3\). The stated conversions to presence probabilities and priors are correct.
- `sections/04_equilibrium_results.tex:188`: Re-derived the fixed-information comparison from the fall in gross profit at each posterior. Checked both information controls and all entries of the outcome table.
- The abstract and `sections/01_introduction.tex:36`: Checked the core claims against the propositions, their conditions, and the benchmark. The claims about uniqueness, entry, ownership, the open set, and coexistence agree.

**Coexistence and priors**

- The path lemma, `appendix/A4_coexistence.tex:19`: Re-derived the threshold derivative and the rational expressions for \(J\) and \(\Delta_T(1-\tau)^2\). Their derivative polynomials match the manuscript.
- The polynomial certificates, `appendix/A4_coexistence.tex:40`: Independently built exact rational Sturm sequences. The degree-six polynomial has zero roots on \((6/5,18/5]\). The degree-ten polynomial has zero roots on \((6/5,2]\). Both are positive at the left endpoint.
- `sections/04_equilibrium_results.tex:324`: Also checked the degree-ten polynomial on the full path through \(18/5\). It remains positive, so the broader main-text statement is correct.
- The threshold definitions and order, `appendix/A4_coexistence.tex:65`: Re-derived the inverse spread formula, the ceiling formula, and every threshold comparison. Exact rational intervals preserve every strict order.
- The high-class lemma, `appendix/A4_coexistence.tex:159`: Checked all five forms, their inequalities, interior roots, full-order boundaries, and dependence on both tie rules.
- The low-class lemma, `appendix/A4_coexistence.tex:193`: Re-derived the unique rate under IM and the interval with no admissible rate under I0.
- The product lemma, `appendix/A4_coexistence.tex:224`: Checked both directions and all six equilibrium conditions. The proof correctly establishes price-based beliefs and the preparation rule.
- The coexistence proposition, `appendix/A4_coexistence.tex:287`: Checked every branch interval and endpoint. The proof establishes \(s\ge t\) for every qualifying pair, so zero-order entry stays at the floor.
- The branch entry formulas, `appendix/A4_coexistence.tex:338`: Re-derived entry from order probabilities. Entry rises strictly on R, joins F continuously, and stays constant through the coexistence interval. The CM threshold branch falls strictly to the floor.
- The alternative rule sets, `appendix/A4_coexistence.tex:326` and `:496`: Checked the added CM equilibria and the absent I0 equilibria on \((r_N,r_S]\). The main text and appendix agree.
- The prior corollary, `appendix/A4_coexistence.tex:402`: Checked the necessary and sufficient coexistence conditions, all four prior cases, and the open lower endpoint at \(r_\pi\). Re-derived the general-prior entry formula.
- The CM endpoint, `appendix/A4_coexistence.tex:477`: Checked the added strength at a prior tie and the endpoint at \(\pi_{\max}\). Its full-purchase return exceeds the cost by approximately \(0.000342952490\).
- Result status: The core general propositions are analytical. The coexistence proposition and prior corollary correctly carry computer-assisted status. The finite-grid enumeration has diagnostic status and supplies no proof step.

**Numbers, certificates, and notation**

- The independent script recomputes 161 core displays from Sections 1–4 and A.1–A.4, plus 33 additional core displays from A.9. All 194 displays match their closed forms at the printed precision. Each also matches `numbers.tex`.
- The checked families include primitives, auction payoffs, prior profits, preparation thresholds, posterior bounds, prices, entry, ownership, proceeds, information controls, parameter regions, strict margins, and coexistence thresholds. They also include branch entry, prior windows, the necessity example, and the CM endpoint.
- The numerical entry component in the introduction also matches its display of \(90.2\%\). The separate empirical proposition is outside this review.
- Exact bounds on Euler's number use

  \[
  S_{110}<\mathrm e<S_{110}+\frac{112}{111\cdot111!},
  \qquad S_{110}=\sum_{n=0}^{110}\frac1{n!}.
  \]

  All dependent computations use rational intervals. Decimal conversion occurs only for displays.
- The five strict margins of the main proposition are positive:

  \[
  \begin{aligned}
  c_H-B_0(\pi)&=287/240,\\
  B_1(M)-c_H&\approx0.217154821917,\\
  k-\Delta_0&=1/300,\\
  \rho\kappa\Delta_1-k&\approx0.024823570228,\\
  c_H-B_2(M)&\approx0.002688902266.
  \end{aligned}
  \]

- The small return margin is certified:

  \[
  0.000333564719409317854285
  <\tau(r_2)-M<
  0.000333564719409317854286.
  \]

- The ceiling and its distance from the third strength are certified:

  \[
  \begin{aligned}
  3.592658518794661833335916&<r_C<3.592658518794661833335917,\\
  0.007341481205338166664083&<r_2-r_C<0.007341481205338166664084.
  \end{aligned}
  \]

- The recomputed thresholds round to \(r_A=1.393958\), \(r_F=1.467127\), \(r_N=1.747878\), \(r_J=1.966097\), and \(r_S=2.124148\). Their exact intervals appear in the scratch artifacts.
- `appendix/A9_parameters.tex:16` and `:91`: Checked the core declarations, core margins, their signs, and the relative-open-set qualification. The recorded margins agree.
- `P1_core/p1_numbers.py`, `p1_common.py`, and `p1_certificates.py`: Inspected the permitted source scripts and relevant run logs. They use outward interval arithmetic or exact rational arithmetic, including the certificate for the small return margin. These repository scripts were not executed.
- Notation: Order masses use \(f_j(x)\). The earlier \(a_j(x)\) notation does not survive in the reviewed files. Euler's number and entry use distinct notation.

**Not checked**

- Sections 5–9 and Appendix A.5–A.8, including their research, robustness, welfare, and empirical proofs.
- The six research displays in the introduction: `res_lambda_r155`, `res_lambda_r160`, `res_lambda_r165`, `res_entry_r155`, `res_entry_r160`, and `res_entry_r165`.
- The noncore declarations and margins in A.9 for those later sections.
- The compiled PDF's layout, figures, citations, slide deck, and comparison note. No manuscript build ran.
- The 241-strength enumeration was not rerun. The equilibrium classification was checked from its proof, including all stated boundaries.
