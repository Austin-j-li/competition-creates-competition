**Part 1: findings**

FINDING:
- Name: The general control omits independence from incumbent value
- Severity: High
- Location: [A6_robustness.tex:8–22](/Users/austinli/Projects/competition-creates-competition/slot/manuscript/appendix/A6_robustness.tex:8), Proposition “Fixed information”; the definition of the fixed experiment.
- Problem: The stated experiment does not restrict the dependence between the signal and incumbent value, so marginal incumbent dominance does not suffice.
- Proposed fix: Require the signal to be independent of incumbent value conditional on class, and retain the stated independence of challenger value and cost.
- Evidence: The proof substitutes unconditional auction profits into the decision after each signal. This requires the conditional incumbent law to equal its unconditional law. The stated law of `(class, S)` does not impose that restriction.

  A continuous counterexample uses reserve \(p=1/2\), class values \(12\) and \(11\), equal class priors, and costs \(0\) and \(6\). The zero-cost probability is \(1/4\). Let \(F_0\) mix \(U[0,1]\) and \(U[8,9]\), with equal weights. Let \(F_1\) mix \(U[0,1]\) and \(U[9,10]\), with equal weights. Then \(F_1\le F_0\).

  In economy zero, the fair binary signal reports the mixture component. In economy one, it is independent of that component. In both economies, the signal is independent of class. Thus the joint law of class and signal stays fixed. Challenger value depends on the signal only through class, as required.

  Conditional gross profits are \(87/8\) and \(3\) in economy zero. They are \(103/16\) after either signal in economy one. Entry therefore rises from \(5/8\) to \(1\). Exact calculations appear in [analytic_examples.py](scripts/ext_1/analytic_examples.py). The intended order-slot control satisfies the missing independence restriction and remains correct.

FINDING:
- Name: The private-signal feasibility argument lacks an analytical witness
- Severity: Mid
- Location: [A6_robustness.tex:430–463](/Users/austinli/Projects/competition-creates-competition/slot/manuscript/appendix/A6_robustness.tex:430), Proposition “Complementary private signals,” especially its final proof sentence.
- Problem: The absence of an explicit order restriction between the accuracies does not prove that the joint inequalities admit a more accurate challenger signal.
- Proposed fix: Add an exact rational witness to the analytical proof.
- Evidence: The benchmark calculation at lines 492–494 itself shows that the joint inequalities can exclude \(d\ge a_T\). The existence claim is correct, but the stated inference does not establish it.

  Keep the values, costs, strengths and accuracies of \(S(B)\). Replace its slot by \((\lambda,\beta)=(1/3,3/10)\). Then \((a_T,d)=(7/10,3/4)\), \(M=8/11\), and \(m=3/11\). The private, joint, weak-trade, strong-trade and other-pair margins are, respectively,

  \[
  \frac{21}{400},\quad
  \frac{1363}{36800},\quad
  \frac{2}{1375},\quad
  \frac{603}{31625},\quad
  \frac{76753}{18400}.
  \]

  All are strictly positive. This supplies an analytical witness without a numerical existence argument. The exact calculation appears in [analytic_examples.py](scripts/ext_1/analytic_examples.py).

FINDING:
- Name: A sale payoff omits its execution cost
- Severity: Mid
- Location: [A6_robustness.tex:527–528](/Users/austinli/Projects/competition-creates-competition/slot/manuscript/appendix/A6_robustness.tex:527), the benchmark with the accuracies of \(S(B)\).
- Problem: The displayed sale return omits the cost, although the next clause calls its solution a zero-profit rate.
- Proposed fix: Write the net payoff as \(U_-(-1)=b/[15(2b+t)]-k\), or label the existing expression as a gross return.
- Evidence: Above the preparation threshold, the correct net payoff is

  \[
  U_-(-1)=\frac{1}{15}\frac{b}{2b+t}-\frac1{50}.
  \]

  At \(t=4b/3\), the printed expression equals \(1/50\), while the net payoff equals zero. The stated equilibrium rate remains correct. [analytic_examples.py](scripts/ext_1/analytic_examples.py) prints both values exactly.

FINDING:
- Name: The dispersion claim omits “weakly”
- Severity: Mid
- Location: [06_robustness.tex:44–45](/Users/austinli/Projects/competition-creates-competition/slot/manuscript/sections/06_robustness.tex:44), compared with [A6_robustness.tex:263–264](/Users/austinli/Projects/competition-creates-competition/slot/manuscript/appendix/A6_robustness.tex:263).
- Problem: The main text states an unqualified increase in gross profit, while convexity establishes only a weak increase.
- Proposed fix: Replace “raises gross profit at every belief” with “weakly raises gross profit at every belief.”
- Evidence: At \(r=3\) and \(p=1/2\), compare a high-class point mass at \(10\) with \(U[199/20,201/20]\). Both laws lie wholly above incumbent values. The acquisition-profit kernel is affine on that interval. Both laws therefore give \(g_H=203/24\). With the low class unchanged, gross profit stays unchanged at every belief. The appendix correctly states the weak conclusion.

**Part 2: coverage**

The reviewed checkout is commit `2c56325c6c99a6db51dadb0bfe144575be28b170`. The repository stayed unchanged. I read every specified extension file and the model and equilibrium sections that supply their definitions. I did not read the excluded verdict files. I did not run a test suite or compile the manuscript.

The numerical calculation uses exact fractions, rational root brackets, and outward interval arithmetic at 85 decimal digits. A rational Taylor enclosure supplies Euler's number. The independent program is [recompute.py](scripts/ext_1/recompute.py). Its output files are [recompute.log](scripts/ext_1/recompute.log) and [recomputed_values.csv](scripts/ext_1/recomputed_values.csv) in the same folder.

The program recomputes all **390 distinct registry keys** used in Sections 5–8 and Appendices A.5–A.8. All values agree at the displayed precision. Every corresponding macro in `numbers.tex` also agrees with the registry. The CSV records a separate enclosure for each key. No numerical discrepancy remains.

- **Model inputs and inherited definitions:** Checked the auction kernels, cost independence, order likelihoods, posterior bounds, entry floor and fixed-price deviation convention. Re-derived the payoff expressions used by the extensions.
- **Abstract, introduction and conclusion:** Matched the research comovement, robust reversal, fixed-information control and access claims to their stated results. The general control needs the restriction in the first finding. The extension-related numerical claims in the introduction agree with the registry.
- **Research game and joint deviations, A.5:40–59:** Re-derived \(zV-az^2/2\) with the candidate's prices and preparation rule fixed. Strict concavity gives the unique response \(\min\{\bar\lambda,V/a\}\), including zero and the cap.
- **Research posterior functions, A.5:17–38:** Re-derived \(m_\lambda\), \(M_\lambda\), \(\lambda_E\), its derivative, the polynomial \(F_r\), and the recruitment margin. The factor in \(F_r(\lambda_E)=-[2\beta+\lambda_E(1-2\beta)]\varphi_a\) is correct.
- **Bounds under every profile, A.5:61–79:** Checked the zero-order bound using \(\beta\le1/3\), price sufficiency, wrong-order exclusion and the full-purchase posterior. These bounds cover every candidate profile.
- **Positive research lemma, A.5:81–96:** Reproduced the implication from a profitable low-class sale to a strictly profitable high-class purchase. Positive research therefore forces a strict full purchase under either investor rule.
- **Intermediate equilibrium set, A.5:98–176:** Checked each tuple Z, R, capped R and T against the likelihoods, beliefs, prices, entry, order payoffs and research response. Checked the exhaustive case split at \(\lambda_E\). The lemma explicitly excludes \(\lambda_E=\bar\lambda\).
- **Intermediate entry and ownership formulas:** Re-derived the purchase probability \(\beta+(1/2-\beta)\lambda\), class-H purchase probability \(\beta+(1-\beta)\lambda\), and threshold entry formula. Recomputed all `res_*_r155`, `res_*_r160` and `res_*_r165` families.
- **Research at the six strengths:** Recomputed the weak-trade gap, prior-cost gap, recruitment gaps, cap gaps and strong-incumbent bounds. The stated C1 counts and the additional CM threshold tuple follow. The investor choices are strict at those strengths.
- **Strong research lemma, A.5:178–206:** Checked the common lower bound \(\rho\Delta_Tm_{\bar\lambda}-k>a\bar\lambda\). It forces both full orders and research at the cap under every candidate. Checked the separate tuple construction and the exclusion of a challenger tie.
- **Research comovement corollary:** Re-derived both partial derivatives of \(F_r\) and the implicit derivative of \(\lambda_R\). Research, entry and high-class ownership rise strictly along the stated branch.
- **Research branch boundaries:** Recomputed \(r_R=1.501022966\ldots\), \(\bar r_R=1.677632834\ldots\), and \(r_U=2.434045527\ldots\). Checked the derivative bound for \(\varphi_a\), its unique initial root, and the argument that excludes an interior recruiting branch after the cap point.
- **Research status and open ranges:** The benchmark lists and branch boundaries use numerical certificates and carry the computer-assisted label. The general lemmas and slope result use algebra. The text leaves the full research equilibrium set on \((r_N,r_U)\) open.
- **Admissible research region:** Re-derived the cap strip and the lower and upper cost bounds. Checked necessity, sufficiency, the nonempty cost window, and both endpoint bounds for strong research. Recomputed `res_cap_*`, `res_a_*`, `res_region_*`, and their margins.
- **Research across liquidity probabilities:** Checked the cap transformation, the lower liquidity cutoff, the upper cost cutoff and the monotonicity bound. The interval \((0.236157\ldots,1/3]\) supports the stated six-strength conclusions.
- **Research tie remark and access comparison:** Checked the CM threshold entries and the continuum at the ceiling. Checked that hidden prices also force full orders and research at the cap at \(r_1\). Research and trade costs coincide across that access comparison.
- **Fixed-information indicator identity:** With the independence restriction in the first finding, the pointwise indicator difference and its exact crossing probability are correct. The common tie-probability extension also preserves weak deterrence.
- **Fixed full-order control in the slot:** Checked the frozen order law, sufficient prices and ceiling. Entry is \(0.522757\ldots\) below the ceiling and \(1/4\) above it. The crossing probability from \(r_0\) to \(r_1\) is zero. The frozen weak tuple is correctly described as a control rather than an equilibrium.
- **Hidden-price control:** Checked the prior belief, entry floor, weak zero orders and strong full orders. The stated entry \(1/4\) is correct.
- **Preparation cost laws proposition:** Checked the low-cost floor under every profile, forced orders, support gaps, tuple construction and ownership condition. Atoms and atomless components both satisfy the proof. The equilibrium comparisons are strict.
- **Atomless benchmark and return to the floor:** Recomputed all `p4_atomless_*` values and margins. The half-width \(0.1\) gives entry \(0.382711\ldots\) at \(r_2\), rather than the floor. Every half-width below \(0.002688902\ldots\) preserves strict exclusion there. The stated continuous, nonincreasing entry formula is correct under its stated floor and full-order conditions.
- **Value classes and priors proposition:** Re-derived the integral for \(\Delta_T(r)\), its positive derivative after \(v_*\), the profit-gap identity and the large-\(r\) limits. Checked the constructive choice of strengths and costs, ownership continuity and openness.
- **Six class economies:** Recomputed every displayed primitive and outcome in the value-class table from exact piecewise auction integrals. This includes the moderate gap, narrow bands, altered priors, wide classes and point masses with the same means. The ownership comparison correctly includes the chance that a high-class challenger loses.
- **Benchmark costs under altered priors:** Recomputed the \(0.3\) and \(0.7\) prior outcomes and cost margins. These differ from the examples with separately chosen costs, as the text states.
- **Dispersion comparison:** Verified Jensen's weak inequality and the wide-class comparison. The main-text wording needs the qualification in the fourth finding.
- **Many-class separation proposition:** Checked the feasible posterior set, its convexity, candidate payoff formula and uniform separation bounds. Full group orders preserve within-group prior proportions. The resulting prices reveal the whole posterior vector.
- **Four-class example:** Evaluated all 16 weight vertices. Recomputed the separation distance \(0.178871\ldots\), trade margin, weak range, prior-cost margin and group profit margins.
- **Three-class price collision:** Re-derived the weight that equates the two posterior means. Recomputed both posterior vectors, the common price, the distinct sale price and every choice margin. A perturbation of \(1/1000\) in either direction separates the prices and preserves strict choices.
- **Private-signal beliefs and prices:** Re-derived the affine public posterior, the private posterior maps, class-specific entry and \(\rho\Delta_T\le\Delta_P\le D^+\). Checked price sufficiency and the fixed-candidate order payoffs.
- **Private-signal proposition:** Checked the weak and strong order bounds, the constructed tuples, strict price order and positive recruitment event. The additional condition correctly reduces recruitment to the pair \((X,Y)=(1,+)\). The second finding concerns only the final feasibility argument.
- **Private-signal vectors and controls:** Recomputed every displayed `sig_*`, `p4_s_*`, `p4_comp_b_*` and associated margin. Section 6 explicitly identifies \(S(B)\) as a separate parameter vector. Both selected examples require the challenger signal for their entry rise.
- **Signal impossibility and grid:** Re-derived the benchmark contradiction for \(d\ge a_T\). Recomputed all 25 grid pairs. Exactly six qualify, and their smallest margin is \(1/10000\).
- **Benchmark with the accuracies of \(S(B)\):** Re-derived the constant price slopes, the rates \(119b/96\) and \(4b/3\), the preparation threshold, and all entry and ownership values. Checked uniqueness under IM and nonexistence under I0. The omitted cost in the third finding does not change those rates.
- **Laplace comparison:** Re-derived the likelihood ratio \(\exp((|x+1|-|x-1|)/s)\) for full informed orders with additive Laplace noise. Its maximum is \(e^{2/s}\). Thus \(1+u=e^{2/s}\) matches posterior bounds. The remark correctly stops short of a claim that the order laws or equilibria coincide.
- **Access proposition:** Checked both equilibrium tuples, the positive proceeds gain and the allocation identity. The surplus gain correctly includes the blocked-sale term \(pF_1(p)\). Recomputed the proceeds gain \(0.257948\ldots\) and net surplus gain \(0.081960\ldots\).
- **Transfers and trade scale:** Re-derived the informed investor's gross transfer, liquidity traders' offsetting loss and the shareholder break-even ratio \(6.848394\ldots\). Checked the deterministic dividend comparison and the equality of execution costs across access economies.
- **Access outside recruitment:** Checked entry \((\rho,1,1)\), the removed preparation event and both gain formulas. At \(c_H=12/5\), proceeds and surplus fall by the stated amounts.
- **Payment rule:** Re-derived the Nash transfer, acquisition profit and spread. The comparative effect has the sign of \(1-2\omega\). Checked zero seller weight, equal weights, strictness conditions and the benchmark coefficient \(13/20\). The continuation equilibrium remains explicitly open.
- **Reserve kernels and proposition:** Checked every kernel piece, boundary agreement, admissibility and the full-order bounds. Re-derived flat entry under recruitment at both strengths and strict deterrence under strong-incumbent exclusion.
- **Reserve numbers:** Recomputed all table entries for preparation, sale, two admissible bidders and proceeds. Checked the narrow-band comparison and every reserve margin. The deterrence reserve \(31/20\) lies between \(p_H=1.325269828\ldots\) and \(1.792723353\ldots\).
- **Reserve range and boundaries:** Verified the polynomial bounds for reserves below \(r_0\), the need to exclude the weak incumbent for strict deterrence, and the CM boundary at \(p_H\). Checked the endpoint \(p=h\). The seller's reserve choice remains open.
- **Empirical full-order range:** Re-derived the ceiling equation and the all-candidate full-order bound. Recomputed \(r_S=2.1241481328\ldots<r_1<r_C<r_2<h\). Checked the negative margin at \(2.1241481\) and the sufficient rounded endpoint \(2.124149\).
- **Spread proposition:** Re-derived the class and entry components, both impacts, the hidden-price spread, all slope signs and the ceiling jump. Recomputed every `ba_*` value, including the entry share \(90.2\%\).
- **Informed-share proposition:** Solved the count equations and the liquidity restriction. Re-derived the incentive upper bound, recruitment band and price identification formulas. Checked the endpoint under IM and its exclusion under I0. The count-compatible interval is \([0.2502991475\ldots,0.76]\).
- **Alternative slot and purchases-only counts:** Recomputed the alternative spread, the inadmissible low-ratio example and the unprofitable \(0.9\)-share example. Re-derived identification under full purchases only and nonidentification of presence on the mixed-purchase branch.
- **Winner proposition:** Re-derived the posterior among prepared challengers, the conditional win probability, its order gap and both covariances. The win gap stays positive after order-entry covariance becomes zero.
- **Announcement proposition:** Checked both report payoffs, the probability-weighted zero mean, the positive mean among preparation reports and the inactive-opportunity discount. Recomputed all announcement values and both benchmark preparation-sample means.
- **Intermediate empirical clusters:** Re-derived the order imbalance, the reversed sale-versus-zero price order and the CM threshold tuple. The exhaustive two-cluster claim correctly uses C1. Equilibrium selection remains open.
- **Numerical provenance:** Traced the relevant formulas in the permitted P2, P3, P4 and P5 scripts. I used independent scratch implementations rather than execute scripts that write repository outputs.

**Not checked:** I did not audit bibliography claims, empirical datasets, figure construction, PDF layout or the compiled PDF's source freshness. I did not audit Appendices A.1–A.4 or A.9 beyond the inherited definitions and results needed here. I did not audit every line of the upstream proof packages or rerun their certificate programs. I did not solve the research range or seller-choice problems that the manuscript labels open.
