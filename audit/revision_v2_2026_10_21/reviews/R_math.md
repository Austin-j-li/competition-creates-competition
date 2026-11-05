Mathematical review of revision `ac4e37e1f85bbf60034663c58e141c1bc264d6ea`, against base `9b9bf3c`.
Line numbers refer to the revised sources in `overleaf/paper-revision/`.
Review date: 21 October 2026.

**Counts: 1 blocking, 7 should fix, 4 minor.**

Propositions 1 and 2, the bounded-score proposition, both nonemptiness constructions, and the Laplace-extremal lemma pass the mathematical review.
The atomless-cost proposition needs a scope correction before its stated general-prior conclusion is valid.
The welfare theorem remains valid for quality classes, but its displayed proof does not cover that scope.
The benchmark values and all three certificate enclosures reproduce.

No manuscript file changed. No test suite ran. The calculations below use print-only scripts.
The proposed corrections introduce no new economic primitive.
In item 6, $\mu_j(x)$ denotes a component of the posterior over classes.

1. **Blocking — Proposition A.6 is false at a general prior under its printed support conditions.**

   **Locations:** `main.tex:2655–2687`; `online_appendix.tex:224–238,961–980`.
   **Verdict:** incorrect as a general-prior statement. The equal-prior benchmark is correct.

   Equation (A.24) uses $B_{r_0}(1/2)$, $m=m(1/2)$, and $M=M(1/2)$.
   Proposition A.6 cites the now-general Proposition 2 without a prior restriction.
   The Online Appendix scope note instead says that these cost windows use the actual prior.
   These are different hypotheses.

   A counterexample uses point masses at $1$ and $10$, with $p=0.5$, $b=2$, and $\rho=0.25$.
   Set $r_0=1.05$, $r_1=3$, $\pi=0.7$, $c_H=6$, $\varepsilon_C=0.1$, and $k=0.005$.
   Use uniform cost components on $[0,0.2]$ and $[5.9,6.1]$.
   Every printed support inequality holds:

   $$
   0.2<2.366178511417,
   \qquad
   4.856547619048<5.9<6.1<6.217154821917.
   $$

   The actual general-prior order inequality also holds:

   $$
   0.001190476190<0.005<0.011349205952.
   $$

   But $B_{r_0}(0.7)=6.656309523810>6.1$.
   Zero orders are uniquely optimal because $\Delta_T(r_0)<k$.
   At their constant price, every preparation cost is below gross profit.
   Weak-economy entry therefore equals $1$, rather than $\rho$.

   **Exact correction:** replace (A.24) and the corresponding Online Appendix support conditions by

   $$
   2\varepsilon_C<B_{r_1}(m(\pi)),
   \qquad
   B_{r_0}(\pi)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{r_1}(M(\pi)).
   $$

   Replace the conclusion of Proposition A.6 by:

   > Retain the class assumptions of Proposition 2 and condition (A2).
   > Under either Laplace or logistic noise, the unique trading outcomes and the entry reversal in parts (i) and (ii) hold.
   > High-class ownership rises exactly when $e_HW_H(r_1)>\rho W_H(r_0)$.
   > This condition holds automatically when $W_H=1$ in both economies.

   In its proof, replace $e(1/2)=\rho$ by $e(\pi)=\rho$.
   Replace the lowest and highest beliefs by $m(\pi)$ and $M(\pi)$ throughout.
   The same proof then works for ranked quality classes with finite means.
   A simpler alternative is an explicit restriction to the point-mass benchmark and $\pi=1/2$.

2. **Should fix — The independence sentence excludes the intended class model.**

   **Location:** `main.tex:358–362`.
   **Verdict:** incorrect as written; the proofs use the correct joint independence assumption.

   The sentence makes the class and its conditional value mutually independent.
   Independence would imply $G_H=G_L$.
   It excludes the point-mass benchmark and every pair with a positive class gap.
   The source memo correctly treats $(j,\theta)$ as one joint object.

   **Exact replacement for the sentence:**

   > The pair $(j,\theta)$, the incumbent's value, the preparation cost, and noise demand are mutually independent.
   > Conditional on the class, the challenger's value is independent of flow.

   The statement at `online_appendix.tex:894–895` already has this form.

3. **Should fix — The welfare proof retains full admissibility and equal prior weights.**

   **Locations:** `main.tex:3061–3068,3073–3127`; `online_appendix.tex:1327–1402`.
   **Verdict:** Proposition A.9 is correct, but its proof has a gap at its stated class scope.
   Equations (A.40)–(A.41) are incorrect for some admitted class distributions.

   The proof assumes $\theta>p$, even though the model allows equal positive mass below $p$.
   It also replaces the actual prior weights by $1/2$ in target proceeds.
   The general incumbent version requires $pF_1(p)$ in place of $p^2/r_1$.

   The pointwise allocation increment for every challenger value is

   $$
   \mathcal V_\theta(R)-\mathcal V_0(R)
   =(\theta-\max\{p,R\})_+
   +p\mathbf1\{R<p,\theta\ge p\}.
   $$

   For example, let $G_L=(\delta_0+\delta_1)/2$ and $G_H=(\delta_0+\delta_{10})/2$.
   Keep $p=0.5$, $b=2$, $\rho=0.25$, $\pi=1/2$, $r_0=1.2$, and $r_1=3$.
   Set $c_H=3$ and $k=0.01$.
   Both strict condition windows of Proposition 2 hold.
   The actual surplus gain is $0.040108767418$.
   The printed first line of (A.41) gives $0.051473654804$.
   It overstates the gain by $0.011364887386$ because half the values cannot meet the reserve.

   **Exact replacement for (A.40):**

   $$
   B_{F_1}(\mu_X)-C+pF_1(p)[1-G_L(p^-)].
   $$

   Equal admissibility makes the last factor the same in both classes.
   **Exact replacement for (A.41):**

   $$
   \begin{aligned}
   \Delta\mathcal W
   &=(1-\rho)\mathbb E\!\left[
   \left\{B_{F_1}(\mu_X)-c_H+pF_1(p)[1-G_L(p^-)]\right\}
   \mathbf1\{\mu_X\ge\tau\}\right]>0,\\
   \Delta\mathcal R_T
   &=(1-\rho)\left[
   \pi\alpha_H(t_H-t_0)+(1-\pi)\alpha_L(t_L-t_0)\right]>0.
   \end{aligned}
   $$

   **Missing strictness step:** the strict upper cost bound gives positive probability to $\mu_X>\tau$.
   On that event, $B_{F_1}(\mu_X)-c_H>0$.
   Also $t_H>t_L\ge t_0$, and the additional-entry event has positive probability in class $H$.
   These facts prove both strict inequalities, including when $F_1(p)=0$.

   For atomless high costs, integrate these expressions against the high-cost distribution.
   For the uniform incumbent, $pF_1(p)=p^2/r_1$ when $p\le r_1$.
   For the benchmark, $G_L(p^-)=0$ and $\pi=1/2$, so the existing numerical formulas remain correct.
   Apply the same replacements in Online Appendix A.9, or label its printed calculation explicitly as the benchmark specialization.
   At `main.tex:3125–3127`, replace the logistic-only formula reference with:

   > Under Proposition A.5, use the integrals over the entry set in that proposition.

4. **Should fix — Several retained benchmark statements lack their prior and value restrictions.**

   **Locations:** `main.tex:1647–1651,2825–2847,2871–2879,3013–3026,3138–3159,3189–3194,3324–3343`.
   **Verdict:** correct under the benchmark restrictions, but overbroad under the appendix's stated default scope.

   The appendix says that every statement which needs the point-mass benchmark states that restriction.
   The signal formulas instead use equal priors without an explicit restriction in the main paper.
   For zero orders and $\pi=0.7$, (A.27) yields $\mu_X=1/2$.
   The actual posterior is $0.7$.
   The Online Appendix states the equal-prior restriction at lines 251–257, but the main proposition must state it too.

   The seller formulas also use point masses at $\ell,h$, equal prior weights, and a finite upper value $h$.
   These objects do not describe every permitted pair $G_H,G_L$.
   The bargaining spread has the same point-mass restriction.

   **Exact scope additions:**

   - Before `main.tex:2825`, insert: “This subsection uses the point-mass benchmark with prior $\pi=1/2$.”
   - At `main.tex:2873`, use: “In the point-mass complementary-signal economy with $\pi=1/2$, choose $0<p<\ell<r_0<r_1<h$ and suppose”.
   - Before `main.tex:3013`, insert: “The displayed bargaining formulas use point-mass challenger values $\ell$ and $h$.”
   - Before `main.tex:3138`, insert: “This subsection uses the point-mass benchmark with $\pi=1/2$. Its stated class extension uses the uniform value bands of Section 5.2.”
   - In Section 5.3, state: “The displayed sufficient conditions use the point-mass benchmark and prior $\pi=1/2$.”

   These additions preserve the valid proofs and declared numerical exercises.
   They do not require a new general-prior signal theorem.

5. **Should fix — The Online Appendix's auction proof does not cover the new incumbent and class scope.**

   **Locations:** `online_appendix.tex:196–200,260–269,444–464,1429–1431`.
   **Verdict:** the main proof is correct; the retained Online Appendix proof has an unstated support restriction.

   Lines 444–464 use $(R-\ell)_+$ as the payment difference for a general continuous $F$.
   That formula requires $R<h$.
   The revised Proposition 1 allows incumbent support above $h$, even in its point-mass special case.
   For $R\sim U[0,20]$, $h=10$, $\ell=1$, and $p=0.5$, the actual spread is $6.525$.
   The untruncated formula in this paragraph gives $9.025$.

   **Exact replacement for lines 444–464:**

   > For a general continuous incumbent distribution, let $D=G_L-G_H$.
   > At a fixed incumbent value, the expected class difference in payments is

   $$
   \xi(R)=
   \begin{cases}
   pD(p^-),&R<p,\\
   \displaystyle\int_p^R D(u)\,du,&R\ge p.
   \end{cases}
   $$

   > Class expectation and Tonelli's theorem give

   $$
   \Delta_T(F)=pF(p)D(p^-)+\int_p^\infty[1-F(u)]D(u)\,du,
   \qquad
   g_j(F)=\int_p^\infty[1-G_j(u)]F(u)\,du.
   $$

   > Appendix A.1 of the paper proves the comparison, its strictness conditions, and the necessity result.
   > With point masses at $\ell$ and $h$, the kernel is $\min\{(R-\ell)_+,h-\ell\}$.
   > It reduces to $(R-\ell)_+$ when incumbent support lies below $h$.

   A related scope sentence calls both payoff kernels bounded at lines 1429–1431.
   The profit kernel is unbounded when the permitted value distribution is unbounded.
   **Exact replacement there:**

   > The revenue kernel is bounded by $\max\{p,\bar r\}$.
   > The profit kernel satisfies $0\le G(R,v,p)\le v$.
   > Finite class means therefore make both kernels integrable.

6. **Should fix — Complete the level-set step in the many-class sufficiency proof.**

   **Location:** `main.tex:2779–2788`; review point R2.
   **Verdict:** correct, but the proof omits the measurability step.

   A constant likelihood ratio implies equal posteriors at two flows.
   The proof must also establish constancy on whole level sets and construct a measurable function of their levels.
   Equal proceeds across some classes also need one explicit sentence.

   **Insert after the covariance argument:**

   > If two classes have equal proceeds, compare each with a class whose proceeds differ.
   > Equality then forces the same likelihood ratio on their supports too.
   > Thus the posterior vector is constant on each level set of $T_X$.
   > Each flow density and each posterior component are continuous.
   > The covariance inequality makes $T_X$ nondecreasing.
   > Under Laplace noise, all posterior components are constant outside $[-1,1]$.
   > On this compact interval, the left endpoint of each level set is a Borel function of its level.
   > For each class, the Borel map

   $$
   t\longmapsto
   \mu_j\!\left(\inf\{x\in[-1,1]:T_X(x)\ge t\}\right),
   \qquad t\in T_X([-1,1]),
   $$

   > therefore recovers its posterior component.
   > Continuity ensures that the endpoint belongs to the required level set.
   > Since the price reveals $T_X$, the tower property gives $\Pr(j\mid P)=\mu_j(X)$ almost surely.

   The argument uses the maintained Laplace law and $b>1$.
   It does not establish this many-class result for every bounded-score density.

7. **Should fix — The table notes still count the retired cost condition as a hypothesis.**

   **Locations:** `tables/table2_equilibrium_controls.tex:32`; `tables/table3_extensions.tex:23`;
   `tables/table_extensions_margins.tex:24`; `tables/table_signal_grid.tex:42`.
   See also `online_appendix.tex:2296–2302` and unresolved item U1.
   **Verdict:** the reported values are correct, but the descriptions of the mathematical conditions are incorrect.

   Proposition 2 and the signal proposition each have four strict scalar conditions.
   Their gross-profit floor is a diagnostic because zero-cost preparation also occurs at equality.
   The atomless-cost result retains a substantive lower-support condition, so its five margins still matter.

   **Exact replacement for the Table 2 note's margin sentences:**

   > The four strict margins of Proposition 2 are $\zeta_{H0}=1.20\times10^0$, $\zeta_{H1}=2.17\times10^{-1}$, $\zeta_0=3.33\times10^{-3}$, and $\zeta_1=2.41\times10^{-3}$.
   > The quantity $\zeta_L=2.37\times10^0$ records gross profit at the lowest feasible belief; it is not an additional hypothesis.

   **Exact replacement for the parenthesis in Table 3:**

   > four strict margins for atomic costs; five for the atomless cost mixture

   **Exact replacement for the first sentence of the margins table note:**

   > For atomic costs and complementary signals, the four strict conditions concern high-cost entry at the prior and ceiling, and trade in each economy.
   > Their low-cost column is a gross-profit diagnostic.
   > For the atomless cost mixture, that column is the additional strict support margin.

   **Exact replacement in the signal-grid note:**

   > The minimum margin is the smallest of the four strict conditions in (OA.29); the low-cost column is a separate gross-profit diagnostic.

   Update the renderer and regenerate these notes rather than alter generated tables by hand.
   Keep five components for atomless costs.
   The displayed rows have a nonbinding gross-profit diagnostic, so this correction does not change their printed minima or uniqueness labels.
   The reserve-details definition can read “Floor diagnostic is $B_r(m)$ under the declared zero cost.”

8. **Should fix — The introductory existence claim omits a positive gap above the reserve.**

   **Location:** `main.tex:207`; review point R21.
   **Verdict:** incorrect if “stochastically higher” includes classes that differ only below the reserve.

   Consider $p=0.5$, $G_L=(\delta_0+\delta_2)/2$, and $G_H=(\delta_{0.25}+\delta_2)/2$.
   The high class strictly dominates the low class, and both have probability $1/2$ below the reserve.
   But their admissible values have the same law.
   Hence $D(u)=0$ for every $u>p$, $\Gamma=0$, and $\Delta_T(F)=0$ for every incumbent distribution.
   Positive trading costs force zero orders at every strength, so no reversal exists.
   Proposition 2 and Section 5.2 already state the necessary positive-gap qualification.

   **Exact replacement for the first sentence at line 207:**

   > The reversal holds on a nonempty region for every prior and every ranked class pair with equal admissibility.
   > The classes must differ above the reserve:

   $$
   \mathbb E_H[\max\{\theta,p\}]>
   \mathbb E_L[\max\{\theta,p\}].
   $$

9. **Minor — The noise explanation repeats the same derivations.**

   **Locations:** `main.tex:409–425,427–429,459–463,1073–1078`; review point R18.
   **Verdict:** correct; no additional mathematical claim follows from the repetition.

   **Exact replacement for lines 1073–1078:**

   > Section 2.3 gives the full-order Laplace log odds and the Gaussian comparison.

   At lines 427–429, replace the count and the repeated exponential-volume example with:

   > Two further constructions give a Laplace law.

   Keep the two constructions that follow and the exponential-volume explanation in the institutional paragraph.

10. **Minor — Lemma OA.2 duplicates the general-prior Proposition 2.**

   **Location:** `online_appendix.tex:1023–1043`; review point R19.
   **Verdict:** correct, but redundant.

   The posterior bounds, cost window, residual bound, and entry formula all follow from the revised Proposition 2.
   The phrase “benchmark entry reversal” also obscures that the prior varies here.

   **Exact replacement for this block:**

   > Proposition 2 of the paper already states the general-prior comparison.
   > Lemma OA.1 is not required for any reported numerical value.

   No source reference points to the removed lemma label.

11. **Minor — The new value cdf conflicts with the old bargaining-profit notation.**

    **Locations:** `main.tex:1288,3046`; `online_appendix.tex:1309–1310`; unresolved item U2.
    **Verdict:** the formulas are correct, but the notation now assigns different meanings to $G$.

    **Exact replacement:** use $g_{\theta,\eta}$ for bargaining profit, and $g_{H,\eta},g_{L,\eta}$ for its point-mass values.
    Keep $G_j$ for the class value cdf.
    Apply the same substitution to the generated Figure 4 labels and its source.
    The substitution changes no value or proof.

12. **Minor — The retired pooling example is absent, but its numerical profit remains in the explanation.**

    **Locations:** `online_appendix.tex:1586–1590,3154–3161`; review point R23.
    **Verdict:** the exclusion argument is correct; the unexplained factor $3$ is unnecessary.

    **Exact replacement for lines 1586–1590:**

    > Entry is therefore at least $\rho$ at every price.
    > Any candidate that prescribes zero preparation at a pooled price violates the zero-cost buyer's optimality condition and the tie rule.

    In C.6b, replace the sentences about $3\bar\mu_c$ with the same general argument.

**Coverage and decisions without a new finding**

The review covers every mathematical statement and proof paragraph in the requested sections.
The ranges below identify the results that pass, and the qualifications above identify their exceptions.

| Claim or review point | Decision and reason |
|---|---|
| Sections 2–3, `main.tex:284–772` | Correct apart from item 2 and the stated scope qualifications. The auction formulas permit value atoms. Posterior bounds use the actual prior. Both entry gains are nonnegative; supports strictly above the reserve make them positive. |
| Proposition 1 and proof, `main.tex:582–637,1665–1802`; R6 | Correct. The kernel is nondecreasing exactly when $D\ge0$ above $p$ and $D(p^-)\le0$. Right continuity upgrades almost-everywhere positivity to pointwise positivity. The two narrow uniform laws prove necessity. With no atom at $p$, these conditions imply equal admissibility. |
| Split identity; R7 | Correct. The main proof retains $pF(p)D(p^-)$ before it imposes equal admissibility. It also states the alternative sufficient condition $F(p)=0$. |
| Posterior and price proofs, `main.tex:1808–1898`; R9 | Correct. The floor holds at every belief. The inversion explicitly requires $\Delta_T>0$. The final paragraph treats $\Delta_T=0$ through zero residuals and unique zero orders. |
| Global bounds, `main.tex:1905–1968` | Correct. Fubini differentiates the translated density. The bound holds against arbitrary mixtures and all feasible deviations. For the full-order calculation, $J_H=(1-\pi)K$ and $J_L=\pi K$. |
| Proposition 2 and proof, `main.tex:786–911,1974–2079`; R8 | Correct under joint independence. The strong positive spread follows from (A2). The strong profit gap follows from (A1) and stochastic strengthening. The weak proof requires neither gap to be strictly positive. Thus the extra ranking condition from the earlier memo is unnecessary. |
| Ownership condition | Correct. Value and preparation are independent conditional on the class. Ownership is $\pi e_HW_H$. The Laplace threshold lies in $(0,1)$, so $e_H>(1+\rho)/2$. The sufficient condition therefore has the stated weak inequality and positive right side. |
| Slack positive low cost; R4 and R11 | Correct. The price posterior lies above $m(\pi)$. Since $B_F$ is nondecreasing, a low cost below $B_F(m(\pi))$ prepares at every price under every candidate. If this holds in each compared economy, the preparation, price, and investor response problems coincide with those at zero cost. Only paid preparation costs and net surplus levels can differ. |
| Fixed-experiment deterrence, `main.tex:2086–2118` | Correct. The indicator identity includes the specified equality convention. It needs no atomless cost law. |
| General-prior no trade; R5 and R11 | Correct. The two signed gains against the constant schedule are $s[e(\pi)\Delta_T(1-\pi)-k]$ and $s[e(\pi)\Delta_T\pi-k]$. Both are nonpositive exactly under the printed maximum condition. No equal-prior assumption enters. |
| Point-mass thresholds, `main.tex:2124–2217` | Correct within their explicit benchmark domain. The ceiling equation is decreasing on that domain. Laplace plateau entry at equality and the logistic limiting comparison have the stated different boundary behavior. |
| Proposition 3 and A.3, `main.tex:965–992,2223–2366` | Correct. The Stieltjes derivative includes the entry atom. The four antiderivatives and the convolution identity have the stated signs and constants. The full-bracket interval evaluation reproduces every endpoint sign, entry enclosure, and positive derivative floor. These certify three nodes, rather than a continuous branch. |
| General bounded-score result, `main.tex:2374–2583` | Correct. Absolute continuity gives $f\in W^{1,1}$ and the translation bounds. Positivity makes flow laws equivalent to Lebesgue measure. The actual full-order essential supremum gives positive entry probability even when it is unattained. No monotone likelihood ratio is assumed. |
| Bounded-score nonemptiness; R12 | Correct. Choose the threshold outside the countable union of atoms of the two posterior laws. At that point, both conditional probabilities of entry are continuous in the threshold. The threshold is continuous in $(r_1,c_H)$ because the profit gap is positive. Thus the strict ownership inequality persists on a neighborhood. The other strict inequalities are continuous there too. |
| Logistic formulas, `main.tex:2585–2644` | Correct. The inverse includes prior odds. The posterior range is open. The common-scale Blackwell claim uses an additive garbling. The common-variance statement is expressly a numerical diagnostic. |
| Ranked-class nonemptiness, `main.tex:2694–2743` | Correct, including $u_0=p$, atoms at the reserve, common mass below the reserve, and unbounded value supports with finite means. The derivative bound gives a strictly positive spread above $u_0$. The split gives a positive profit gap at every finite strength. Dominated convergence supplies $g_j(r)\to0$. The ownership ratio remains favorable near $u_0$. |
| Many-class sufficiency, `main.tex:2747–2788`; R2 | Correct after the proof completion in item 6. Ordered supports follow from increasing differences. With different proceeds, equality in the nonnegative covariance forces one likelihood ratio across all supports. |
| Two-group theorem, `main.tex:2790–2819`; R3 | Correct as a sufficient theorem. It does not claim a result for every class vector. Its conditions are nonvacuous: split a benchmark class into two sufficiently near classes. Payoffs and posterior extrema are continuous in the split, so strict binary margins persist. The printed calculation also gives a distinct three-class example: values $(0.99,1.01,10)$, priors $(0.25,0.25,0.5)$, and the benchmark strengths and costs. The weak range is $0.018375<0.02$, the strong trade bound is $0.021579012075>0.02$, and the strong upper profit is $6.217159304274>6$. No new existence claim is needed. |
| Section 5.2 | Correct. The uniform-band spread adds $\varepsilon_V^2/(6r)$. The benchmark satisfies the strict margins. Failure of equal admissibility can reverse the spread comparison. |
| A.5 after the zero-cost change | Correct within the explicit benchmark and equal-prior scope requested in item 4. The floor requires only nonnegative rents and the equality convention. The state-specific rates, positive price coefficient, and residual bounds are unchanged. |
| Bargaining calculation in A.6 | Correct for its point-mass values. The transfer solves the stated Nash problem, and the factor $1-2\eta$ gives the competition comparison. The statement does not solve a trading equilibrium under bargaining. |
| A.7 and reserve changes; R16 | Correct in the stated point-mass and uniform-band exercises. A zero cost preserves preparation at $p=h$ and above support. A point mass at $h$ permits a sale at that endpoint. An atomless class has zero sale probability at its upper endpoint. The fixed-order inversion explicitly uses the two-point cost law. An atomless low-cost component need not preserve its floor when gross profit is zero. |
| Online scope note | The prior-weight, residual, ownership, reserve-boundary, and signal qualifications are correct. Items 1 and 5 identify places where the retained body does not implement that scope. |
| Laplace-extremal lemma, `online_appendix.tex:799–919` | Correct in all three parts. Median zero is needed only for the tail comparison. Equality at a positive distance fixes both exponential tails. The decision-rule ODE bounds the ROC curve at every pure profile. Posterior call values then give the binary Blackwell order. The logistic characteristic-function product supplies an independent additive garbling for mixed profiles as well. The price hypotheses are sufficient. |
| Informed shareholder, `online_appendix.tex:1615–1744` | Correct under the Proposition 2 comparison. The stake affects entry proceeds, rather than the interim price. The signed-order derivatives obey $U_H'\ge\delta-\omega(1-\rho)w_H/(2b)$ and $U_L'\le-\delta+\omega(1-\rho)w_L/(2b)$ on both sides of zero, where $\delta=(1-1/b)\rho\kappa(\pi)\Delta_T-k$. Integration proves global optimality and excludes mixtures. No trade retains existence for every stake where the baseline admits it; uniqueness uses $\Omega_0$. Part (iii) has constant entry under every candidate, so it needs no stake bound. |
| New exercise C.9 | Correct. Gross profit excludes $k$ and has no missing factor of two at the equal prior. Both stake bounds and the proceeds ratio reproduce. The Student scale has score bound $1/b$. Its full entry set has two endpoints; the secant set is a half-line. Both entry values reproduce. Their status remains a fixed-profile numerical diagnostic. |
| R10 | The local source extracts support the stated information sequence and the broad selective-entry description. The review does not certify published equation numbers or journal-version passages from working-paper extracts. No proof uses an imported affiliation or uniqueness theorem. |
| R1, R13, and R14 | The uncited records and legal description require a citation or legal review. They supply no mathematical hypothesis or proof step here. |
| R15 and R17 | The new profit and stake calculations have the stated transfer interpretation. Legacy column names do not impose a positive low cost. The current declarations set that cost to zero. |
| R20 and R22 | The repeated class example uses the same value bands and prior. The local density symbol and the strength subscripts are defined. These points do not change a mathematical claim. |
| R18 and R19 | Both mathematical claims are correct. Items 9 and 10 remove duplication only. |
| U2–U4 | Item 11 addresses the notation collision. Class labels written as $\theta\in\{H,L\}$ are a local notation problem, rather than a different mathematical assumption. The talk and script files are outside this review. |

**Calculations and source integrity**

- `scripts/R_math/print_math_review.py` prints the benchmark calculations, counterexamples, stake bounds, additional noise values, and three-class margins.
- `scripts/R_math/calculations.txt` records its output and the source hashes.
- `scripts/R_math/print_certificate_values.py` calls the existing interval and auction evaluators with zero low cost and the manuscript's real inputs.
- `scripts/R_math/certificate_values.txt` records the three certificate enclosures and reserve endpoint payoffs.

The interval evaluator reproduces the three global derivative floors:
$0.0000761777420772$, $0.0027531948554801$, and $0.0054921767316432$.
All printed endpoint signs and entry enclosures agree with Proposition 3 after outward decimal rounding.
The new C.9 values agree with their registered values at every displayed digit.
This use of the existing evaluator does not independently certify its implementation.

The source hashes remain:

- `main.tex`: `eaa0ceae4b5660b28de818868411a3d7f9581f0732722e27ab9cc42f4a93c4d3`.
- `online_appendix.tex`: `46c29540049aa909a14ac1f0cb08a59897b9115994a80dc1b8336ca411814459`.
