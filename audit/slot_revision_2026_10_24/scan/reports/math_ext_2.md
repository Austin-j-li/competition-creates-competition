**Part 1: Findings**

I found no Critical or High issue in the extension results. Five statements need corrections to their scope or wording. All 390 referenced registry values match the formulas at the displayed precision.

FINDING:
- Name: The cap region inherits a fixed benchmark outcome
- Severity: Mid
- Location: `slot/manuscript/appendix/A5_research.tex:291`, Proposition `prop:researchregion`; `slot/manuscript/sections/05_research.tex:64`, Proposition `prop:research`(iii).
- Problem: The region proposition invokes all benchmark claims, although the numerical entry value changes with the cap.
- Proposed fix: Specify the qualitative claims and replace the fixed entry number with its formula when the cap varies.
- Evidence: Set the cap to \(\bar\lambda=0.33\) and retain \(a=1/40\) and \(\beta=0.294655\). The four region margins are positive:

  \[
  \begin{aligned}
  \bar\lambda-\lambda_E(r_1)&=0.039461120989455\ldots,\\
  \lambda_E(r_2)-\bar\lambda&=0.006720872993777\ldots,\\
  a-a_{\mathrm{lo}}(\bar\lambda)&=0.002468642208197\ldots,\\
  a_{\mathrm{up}}-a&=0.011763302065145\ldots.
  \end{aligned}
  \]

  Yet entry at \(r_1\) is

  \[
  \mathcal E_1
  =\rho+(1-\rho)\bigl[\beta+(1/2-\beta)\bar\lambda\bigr]
  =0.5218141375,
  \]

  rather than the benchmark value \(0.522757\) stated in Proposition `prop:research`(iii). The region proof correctly preserves the equilibrium patterns. Its reference to the numerical proposition needs this qualification.

FINDING:
- Name: The introduction uses the wrong incumbent regime
- Severity: Mid
- Location: `slot/manuscript/sections/01_introduction.tex:96`, the empirical summary; `slot/manuscript/appendix/A8_empirical.tex:174`, Proposition `prop:winner`(iii).
- Problem: The introduction says orders cease to predict entry against a strong incumbent, but this holds only above the entry ceiling.
- Proposed fix: Replace “Against a strong prepared bidder” with “Above the entry ceiling”.
- Evidence: The manuscript calls \(r_1=3\) the strong-incumbent economy. At that strength,

  \[
  \operatorname{Cov}(X,\mathbf 1_A)
  =(1-\rho)(b+\lambda/2)
  =0.272756943478407\ldots>0.
  \]

  The covariance becomes zero for \(r>r_C=3.592658518794662\ldots\), including the very strong economy \(r_2=3.6\). Appendix A.8 states the correct restriction.

FINDING:
- Name: A shortfall appears with a negative magnitude
- Severity: Low
- Location: `slot/manuscript/appendix/A6_robustness.tex:266`, the fixed-prior comparison.
- Problem: The text says the top profit misses the cost by a negative number.
- Proposed fix: State the signed profit gap directly, or report the positive shortfall.
- Evidence: At \(\pi=0.3\) and \(r_1=3\),

  \[
  B_{r_1}(M(0.3))-c_H=-1.390820614796259\ldots.
  \]

  Thus the shortfall is \(1.390821\), while the registry correctly stores the signed gap as \(-1.390821\). The conclusion of no high-cost entry remains correct.

FINDING:
- Name: A positive-purchase statement includes zero research
- Severity: Low
- Location: `slot/manuscript/appendix/A5_research.tex:172`, Step 5 of Lemma `lem:a5-middle`.
- Problem: The proof claims a strictly positive purchase payoff in every listed equilibrium, including the zero-research equilibrium Z.
- Proposed fix: Restrict that sentence to the equilibria with positive research and refer to Step 1 for Z.
- Evidence: In Z, \(\hat\lambda=0\) and

  \[
  U_H(1)=\rho\Delta_T/2-k<0.
  \]

  At \(r=1.55\), this payoff is \(-0.007802419354839\ldots\). The positive expression \(2a\hat\lambda\) applies to R and T; the cap case gives its lower bound. The classification and the conclusion about strict trade choices remain correct.

FINDING:
- Name: The table claims a third-strength check without a third strength
- Severity: Low
- Location: `slot/manuscript/appendix/A6_robustness.tex:235`, the notes to Table `tab:classes`; also line 250.
- Problem: The text says the first five rows satisfy every hypothesis, although the moderate-gap row specifies only two strengths.
- Proposed fix: State that the moderate-gap row verifies (H1)–(H2), while the other four reversal rows also verify (H3).
- Evidence: The moderate-gap row specifies \(r_0=21/20\) and \(r_1=3/2\), but no \(r_2\). Hypothesis (H3) requires \(B_{r_2}(M)<c_H\). Its two-strength margins and outcomes are correct; no third-strength margin exists for that row.

**Part 2: Coverage**

The audit used the specified manuscript sources and the permitted derivation scripts. I did not read the prohibited verdicts or independent-check files. I made no repository edits and ran no test suite. All new files are under `/tmp/ccc_slot_scan/`.

The calculation records are:

- [recompute.py](scripts/ext_2/recompute.py): closed forms, exact rational class integrals, and interval calculations for all 390 registry keys.
- [recomputed_values.tsv](scripts/ext_2/recomputed_values.tsv): one row per key, with calculated bounds, the displayed value, and the difference.
- [recompute.log](scripts/ext_2/recompute.log): coverage totals and display comparisons.
- [scope_values.py](scripts/ext_2/scope_values.py) and [scope_values.log](scripts/ext_2/scope_values.log): region margins, class examples, collision perturbations, and the private-signal grid.

The scripts use Python `Fraction` and `mpmath.iv` at 80 decimal digits. They compute and print values without assertions. Root brackets use rational endpoints and interval signs.

Research: Section 5 and Appendix A.5

- **Research game and joint deviations.** Re-derived the objective with prices and preparation rules fixed at the candidate:

  \[
  zV-\frac a2z^2,
  \qquad z^*=\min\{\bar\lambda,V/a\}.
  \]

  Strict concavity gives one research choice, including zero and the cap. The condition at zero research correctly retains optimal orders after hypothetical success.

- **Derived functions.** Re-derived \(m_\lambda\), \(\lambda_E\), its derivative, the quadratic \(F_r\), the recruitment margin \(\varphi_a\), and threshold entry \(e^*\). The polynomial signs and root equivalences are correct.
- **Bounds under every profile.** Checked all four parts of Lemma `lem:a5-bounds`, including the zero order and price sufficiency. The restriction \(\beta\le1/3\) supplies the zero-order bound.
- **Strict full purchase.** Checked Lemma `lem:a5-buy`. Positive research implies positive trade value; a profitable low-class sale also forces a profitable high-class purchase.
- **Intermediate equilibrium set.** Checked the tuples Z, R, capped R, and T, including beliefs, entry, prices, order payoffs, and research optimality. The three cases relative to \(\lambda_E\) exhaust positive research. The exclusion of \(\lambda_E=\bar\lambda\) is explicit.
- **Strong incumbents.** Checked Lemma `lem:a5-strong` against arbitrary candidates. Its lower bound forces both full orders and research at the cap. It does not assume the proposed order profile.
- **Six benchmark strengths.** Recomputed all strict margins and the equilibrium outcomes. Under C1, each intermediate strength has exactly Z and R. Under CM, T adds one equilibrium. The investor tie rule has no effect there.
- **Research and entry slopes.** Re-derived the implicit derivative in Corollary `prop:researchbranch`:

  \[
  \lambda_R'(r)
  =\frac{\beta(1-\lambda_R)\Delta_T'(r)}{\partial_\lambda F_r}>0.
  \]

  The entry and ownership coefficients are positive. The ownership formula correctly uses \(h>r\).

- **Branch endpoints.** Recomputed \(r_R=1.501023\), \(\bar r_R=1.677633\), \(r_N=1.747878\), and \(r_U=2.434046\), to six places. Checked the monotonicity bound and the argument that excludes an interior recruiting branch above its cap endpoint.
- **Cap and cost region.** Checked necessity and sufficiency for the qualitative patterns, subject to the first finding. The benchmark cost window is approximately \((0.021469,0.036763)\). The lower liquidity threshold is \(0.236156685530381\ldots\).
- **Tie rules and open sets.** Verified the threshold-entry values and the CM continuum at \(r_C\). The manuscript correctly leaves the research equilibrium set on \((r_N,r_U)\) open.
- **Access with research.** Checked that both access economies have the same cap, order law, research cost, and trade cost. Their proceeds and surplus differences equal the Section 7 differences.
- **Status labels.** The research classifications have analytical proofs; the benchmark signs and branch certificates use exact or interval calculations. The computer-assisted labels correctly describe these numerical specializations.

Robustness: Section 6 and Appendix A.6

- **Fixed information.** Re-derived Proposition `prop:control` pointwise under C1:

  \[
  \mathcal E_0-\mathcal E_1
  =\Pr\{B_{F_1}(\mu(S))<C\le B_{F_0}(\mu(S))\}.
  \]

  The frozen object is the joint law of class and signal, the class distributions, and the independent cost law. A common tie probability also preserves weak monotonicity.

- **Slot controls.** Checked the frozen full-order and hidden-price tuples. The order experiment stays fixed; competitive prices need not stay numerically fixed. Entry is unchanged from \(r_0\) to \(r_1\) under the frozen full-order control.
- **Preparation cost laws.** Checked Proposition `prop:atomless`, including the entry floor under every candidate. The support gaps force the entire low component to enter and give strict comparisons for the high component.
- **Return to the floor.** Recomputed the uniform cost-band example. Half-width \(0.1\) gives entry \(0.382711\) at \(r_2\). Every half-width below \(0.002688902265905\ldots\) restores the floor. The atomless ramp formula is correct under its stated floor, prior, and full-order restrictions.
- **Value classes and priors.** Re-derived Proposition `prop:classes` using \(\Gamma(x)=\int_p^x(G_L-G_H)\). Checked the derivative of \(\Delta_T\), the positive profit gap, continuity, the ownership condition, and the open-set construction.
- **Six class examples.** Recomputed point and uniform class integrals, entry, ownership, and the available hypothesis margins. The wide-class row recruits; the same-means point row fails recruitment. The convexity argument for a mean-preserving spread is correct.
- **Fixed priors.** Recomputed the \(0.3\) and \(0.7\) cases with unchanged benchmark costs. Their order bounds and entry outcomes are correct, subject to the shortfall wording above.
- **Many classes.** Checked the posterior-vector bounds, convexity of the feasible set, separation inequalities, and deviations at fixed prices. Forced group orders preserve prior proportions within each group, so three distinct prices reveal the posterior vector.
- **Four-class example.** Recomputed the 16 weight vertices and all stated margins. The separation distance is \(0.178871\) to six places.
- **Three-class collision.** Re-derived the collision weight and both posterior vectors. The common price and strict choices are correct. Perturbations of \(\pm0.001\) separate the prices and retain positive choice margins.
- **Private-signal proposition.** Re-derived the posterior updates, class-specific entry, price sufficiency, and order returns. The bounds use every candidate profile. The additional condition for recruitment only after \((X,Y)=(1,+)\) is correct.
- **Signal examples and controls.** Recomputed the separate parameter vector \(S(B)\), its no-buyer-signal control, and its class-information control. Section 6 clearly identifies its separate costs and strengths.
- **Signals at unchanged B.** Checked the impossibility bound for \(d\ge a_T\), the complementary pair \((0.94,0.505)\), and its control. Checked both mixed equilibria under \((0.70,0.75)\), including uniqueness under IM and nonexistence under I0.
- **Accuracy grid.** Recomputed all 25 declared pairs. Six satisfy the four sufficient inequalities; the smallest stated margin is exactly \(0.0001\).
- **Laplace remark.** For full orders and additive Laplace noise, re-derived

  \[
  \frac{f(x\mid H)}{f(x\mid L)}
  =\exp\!\left(\frac{|x+1|-|x-1|}{s}\right)
  \in[e^{-2/s},e^{2/s}].
  \]

  Thus \(1+u=e^{2/s}\) matches the posterior bounds. The text correctly avoids a claim of equivalent order probabilities or equilibria.

Welfare and sale terms: Section 7 and Appendix A.7

- **Price access.** Checked both equilibrium tuples, their uniqueness bounds, and the coupling argument. The proceeds gain is strictly positive under the stated hypotheses.
- **Surplus identity.** Re-derived the allocation gain for every admissible challenger:

  \[
  \max\{R\mathbf1_{\{R\ge p\}},\theta\}
  -R\mathbf1_{\{R\ge p\}}
  =(\theta-\max\{p,R\})_++p\mathbf1_{\{R<p\}}.
  \]

  This gives the stated surplus gain net of preparation costs. Identical trade costs cancel from the comparison.

- **Benchmark gains.** Recomputed the proceeds gain \(0.257948\), surplus gain \(0.081960\), gross transfer \(0.037665\), and conditional trade-scale threshold \(6.848394\).
- **Outside the recruitment region.** Checked the changed entry pattern at \(c_H=12/5\). Proceeds change by \(-0.173917\) and surplus by \(-0.013505\), to six places. The deterministic dividend leaves order incentives and information unchanged.
- **Payment rule.** Re-derived the Nash transfer, challenger profit, and spread. The spread responds with the sign of \(1-2\omega\), subject to the stated strictness condition. The benchmark coefficient is exactly \(13/20\). The continuation with trade and preparation remains explicitly open.
- **Reserve kernel.** Checked all four cases, admissibility at equality, and agreement at the shared boundaries. The formulas correctly distinguish preparation, sale, and two admissible bidders.
- **Reserve proposition.** Checked full-order uniqueness from the bound under every profile. Both the flat-entry and strict-deterrence conclusions follow from the stated profit inequalities.
- **Reserve examples.** Recomputed every table cell, point-class margin, narrow-band margin, and proceeds comparison. The exclusion reserves give flat entry. Reserve \(31/20\) gives strict deterrence and higher proceeds at both strengths.
- **Reserve intervals and boundaries.** Re-derived \(p_H=1.325269828309721\ldots\) and \(h-c_H/M=1.792723352971346\ldots\). Checked the interval below \(r_0\), the tie at \(p_H\), and the endpoint \(p=h\). The seller's optimal reserve remains open.

Empirical implications: Section 8 and Appendix A.8

- **Full-order range.** Checked the bound for every candidate on \((r_S,h)\), with the exact root \(r_S=2.124148132815451\ldots\). The rounded counterexample and sufficient endpoint are correct. The boundary at \(r_C\) follows C1.
- **Spread and impacts.** Re-derived the class and entry components, both impacts, their slopes, and the jump at the ceiling. At \(r_1\), the spread is \(0.786299\); its entry share rounds to \(90.2\%\).
- **Counts and informed share.** Re-derived the unique slot for given volume and share, including the constraint \(\vartheta'\ge3-2/v\). The sale incentive supplies the upper bound \(1-2k/(\rho\Delta_T)\).
- **Share band.** Checked existence and unique full orders throughout the strict recruitment/exclusion band. The volume condition also follows analytically from \(\beta<0.3\) and \(e<3\), which imply \(v<3/4<200/259\).
- **Identification endpoint.** Checked the closed interval \([0.250299147528850\ldots,0.76]\) at benchmark volume and \(r_1\). IM admits its upper endpoint; I0 does not. The arguments exclude an alternative interior sale rate at that endpoint.
- **Price identification.** Re-derived \(\vartheta=2I_-/(\rho\Delta_T)\), \(\lambda=v\vartheta\), and the formula for \(\beta\). These claims correctly condition on the entry floor and the target-payoff spread.
- **Purchases only.** Checked identification of \(\lambda\) and \(b\) in F. On R, counts identify only the actual purchase mass and \(b\). A nearby slot preserves those counts.
- **Winner predictions.** Checked that preparation leaves the class posterior unchanged in the benchmark. Re-derived the conditional win probability, its purchase-sale gap, and both covariance statements.
- **Announcement returns.** Checked both report-specific returns, their zero unconditional mean, and the positive mean conditional on preparation. The proof supplies a positive-probability order with entry below one.
- **Inactive opportunity and two clusters.** Recomputed the neutral-price drop, the mean order, and the sale-neutral price gap. The third threshold pattern correctly requires CM. Equilibrium selection remains open.

Numerical and cross-layer coverage

- The 390 values comprise 164 P2-prefixed keys, 82 research keys, 70 P4-prefixed keys, and 74 remaining keys.
- These include all inputs, research roots, thresholds, cost windows, signal outcomes, reserve outcomes, welfare values, identification bounds, and signed margins in the eight target files.
- Every manuscript macro equals its registry display. No calculated value differs beyond the displayed precision. The signed-shortfall finding concerns prose, not the stored number.
- The abstract and conclusion correctly describe the conditional research and welfare results. The introduction needs the regime correction above.
- The audited proofs preserve the distinction between a unilateral deviation and a comparison across economies. No uniqueness argument relies only on the proposed tuple.

Items not checked

- I did not independently audit Appendix A.1–A.4 or A.9. I read Sections 2–4 for definitions and dependencies.
- I used the Section 4 classification where the extensions cite it. I did not reproduce its separate Sturm certificates.
- I did not inspect the compiled PDF, figures, bibliography, citations, or page layout.
- I did not execute the repository derivation programs, which can write repository artifacts. I read their permitted formulas and produced separate calculations.
- I did not infer new equilibria on the open research interval, select among coexisting equilibria, or solve the seller's reserve problem.
- I checked the mathematical empirical predictions, not identification or causal validity in an external dataset.

Report path: `reports/math_ext_2.md`.
