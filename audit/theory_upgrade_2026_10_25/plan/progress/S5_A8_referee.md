# S5, package A8: referee report

The referee to the coordinator, 25 October 2026.

## Verdict

One blocker and one minor notation issue. All frozen statements are intact relative to the supplied `statements/D.tex`, with the agreed substitution of `cor:example-coexistence` for its placeholder label. The standing paragraph, indicator paragraph and event paragraph are intact as well.

The general ceiling statement lacks the mixing-investor qualifier in both `statements/D.tex:169` and `slot/manuscript/appendix/A8_empirical.tex:142`. The qualifier is present in the example at `D.tex:359` and `A8_empirical.tex:572`. The proposed qualifier is sufficient, and the proof at `A8_empirical.tex:269-277` proves that qualified statement. The unqualified statement is wrong under the abstaining investor rule at the zero purchase margin described below.

The package was read in full against the frozen statements, their notes and referee report, the W4 and W5 proofs, the O2 and O7 arguments, the plan, decisions, notation and style rules, and the preceding version of A8. No manuscript file was edited.

## Per-result decisions

Locations in this table are in `slot/manuscript/appendix/A8_empirical.tex`.

| Result | Statement fidelity | Proof verdict | Reason |
|---|---|---|---|
| Standing paragraph and full-trade identities, lines 3-59 | intact | accept | Bayes' rule gives the order frequencies and balance identity. The difference between the denominator and numerator of the posterior-gap ratio is `b(b+lambda)(1-2pi)^2`, which is nonnegative and vanishes exactly at the prior one half. Entry-floor and positivity arguments carry their hypotheses. |
| A.10(i), lines 63-66, 151-161 | intact | accept | The price identity follows by adding and subtracting the price component with constant entry and using Bayes plausibility. It holds without full trade. |
| A.10(ii), lines 67-76, 162-167 | intact | accept | Full trade makes the zero-order posterior the prior. Below the preparation threshold the sale and zero-order entries equal the floor, leaving exactly the recruitment term. Its sign uses the strictly positive entry gain. |
| A.10(iii), lines 77-99, 168-183 | intact | accept | The four strict regimes and all three threshold ties follow from the preparation rule. At a prior-threshold tie, changing entry after no order changes no investor payoff; the constructed-tuples argument supplies price beliefs for every stated entry. |
| A.10(iv), lines 100-109, 184-204 | intact | accept | The price-gap decomposition follows by subtraction and the balance identity. The strict trading bound forces both correct orders in the visible-price and hidden-price economies. The hidden-price conclusion retains the prior-below-threshold hypothesis. |
| A.10(v), lines 110-117, 205-224 | intact | accept | The unweighted difference follows from the frequency difference. The proof examines every threshold regime under the stated prior, zero-cost probability and preparing rule; the recruiting regime is strictly positive and every other regime is nonpositive. |
| A.10(vi)(a)-(c), lines 118-134, 225-255 | intact | accept | The reserve-rescue decomposition and its exact increment are correct. The uniform-law derivative includes the reserve term and remains valid with class atoms. Fixed prior and slot keep the frequencies and posteriors constant for the component trends. See the minor notation issue below. |
| A.10(vi)(d), lines 135-143, 256-277 | intact relative to supplied D; authorized mixing qualifier absent | wrong as stated; accept with the proposed qualifier | Dominated convergence, the closed recruitment set, the threshold equality and all preparing-rule jump formulas are correct. The entire entry interval at the ceiling needs the mixing investor at a zero floor-entry purchase margin. The existing proof explicitly uses that investor at the endpoint. |
| A.11(a), lines 285-292, 314-319 | intact | accept | The mean order identifies presence at a known asymmetric prior; volume identifies liquidity. The variance follows from `X^2=1{X nonzero}` and independent opportunities. The price-scale inversion uses floor entry where required. See the minor notation issue below. |
| A.11(b), lines 293-300, 320-337 | intact | accept | The feasibility bound is exactly the model's liquidity restriction. At even prior odds the low-class sale binds before the high-class purchase; weak and strict investor rules give the stated included and excluded endpoints. |
| A.11(c), lines 301-310, 338-348 | intact | accept | The positive root of the quadratic identifies presence, then the prior. The root argument includes zero mean order, and the prior-one-half formulas follow. |
| Corollary A.3(a), lines 351-356, 367-376 | intact | accept | Counts give liquidity and realized informed order share. Purchase intensity and presence retain their known-prior and sure-purchase qualifiers. |
| Corollary A.3(b), lines 357-364, 377-399 | intact | accept | Every point of the full segment has feasible liquidity and buying probabilities, identical conditional order laws and identical deviation payoffs. The mixing rule permits the endpoint with sure purchase while indifferent. Prices and acquisition probabilities are unchanged. |
| A.12(i)-(ii), lines 408-415, 444-459 | intact | accept | Independence preserves the class posterior and conditional value law after preparation. Continuity removes acquisition ties. The expected class-CDF difference gives the exact strictness condition; full trade gives ordered posteriors and prices. |
| A.12(iii)-(iv), lines 416-431, 460-480 | intact | accept | Centering gives the general-prior covariance coefficient. The second difference contains both class and entry terms away from even prior odds. At even odds the class term cancels, and positive gross profit proves the strict recruitment sign. |
| A.12(v)-(vi), lines 432-441, 481-499 | intact | accept | Outbidding removes the high-class win decline; strict widening is exactly a loss of low-class wins. The uniform-law right derivative uses right-continuous CDFs, and absolute continuity supplies the exact almost-everywhere monotonicity condition. |
| A.13(i)-(iv), lines 505-538 | intact | accept | Report-contingent prices use cost independence. The conditional mean cancels. Preparation-report weights give the exact positivity condition, and Bayes plausibility proves the prior-profit sufficient condition. The final identity is the same unrestricted moment as A.10(i). |
| Example (a)-(d), lines 540-586, 623-683 | intact | accept | Closed-form payoffs give the entry ceiling, forcing interval, price components and jump. The count-feasible band and strict incentive bound imply the stated unique outcomes at both observation strengths. The example's ceiling sentence explicitly names the mixing investor. |
| Example (e)-(h), lines 587-620, 684-728 | intact after agreed label substitution | accept | The coexistence classification supplies the purchases-only intervals and equilibrium count. The win probabilities, covariance terms, announcement means and third threshold equilibrium follow from the general results and the displayed cash flows. Every quoted value agrees with the independent evaluation. |

## Issues

| ID | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| A8-R1 | blocker | `slot/manuscript/appendix/A8_empirical.tex:142`; `audit/theory_upgrade_2026_10_25/statements/D.tex:169` | The general any-probability challenger sentence still permits the abstaining investor. At a zero floor-entry purchase margin, the endpoint entry rho cannot support a full purchase. The coordinator's specified qualifier is absent at both general statements, although present in their example counterparts. | Begin the general sentence in both locations: "When an indifferent investor may mix over its best orders and an indifferent high-cost challenger may prepare with any probability, ...". The proof already covers this scope. |
| A8-R2 | minor | `slot/manuscript/appendix/A8_empirical.tex:234`; same source, line 317 | The proofs use `S(y)` for the mixture survival probability and `n` for sample size. `plan/NOTATION.md:268` reserves S for signals, and line 357 requires sample size in words. Neither affects the mathematics. | Write the mixture survival probability as `Pr_mu(theta>y)` throughout lines 234-245, defining its equality with `1-(1-mu)G_L(y)-mu G_H(y)` once. At lines 317-318, express the variance multiplier divided by the number of independent opportunities in words, as in the frozen statement. Leave the frozen statements unchanged. |

### Exact obstruction for A8-R1

Take point classes at 1 and 10, reserve one half, incumbent uniform on `[0,r]`, prior `3/5`, presence and liquidity probabilities both `1/4`, and zero-cost probability `1/4`. Fix the trading cost at `1/27` and the high preparation cost at `1427/216`. These are two fixed preparation costs with the prescribed two-point probability law.

At `r_C=3`, the full-trade posteriors are `M=7/9` and `m=9/23`, the spread is `2/3`, the low-class profit is `1/8`, and the high-class profit is `203/24`. Thus gross profit at M equals `1427/216`, the preparation threshold equals M and exceeds the prior, and

\[
\rho\Delta_T(r_C)(1-M)-k=0,
\qquad
\rho\Delta_T(r_C)m-k=\frac{35}{1242}>0.
\]

Under the preparing challenger rule the high-class purchase margin at the ceiling is `1/9>0`. Gross profit at M falls strictly through the high cost as r increases through 3. Above 3 the floor-entry purchase margin is strictly positive because the spread rises strictly; the sale margin stays strictly positive on both sides. Full two-sided trade therefore holds on a neighborhood under the abstaining investor and preparing challenger rules, as the ceiling hypotheses require.

At the ceiling, allowing the high-cost challenger any preparation probability permits entry rho in its own optimization problem, but that entry leaves the informed high class indifferent between purchase and abstention. The abstaining investor then cannot buy surely. Hence the lower endpoint of the asserted full-trade entry and price-gap intervals is unavailable. A mixing investor can buy surely while indifferent, which proves that the proposed qualifier resolves the issue. Values strictly above rho give a strictly positive purchase margin.

## Independent evaluation

An 80-digit print-only evaluation starts from the exact example inputs and computes the cash flows, full-order laws, preparation threshold and root equations directly. It evaluates all 51 distinct numerical quantities printed through `reg` in A8, including its three proof-only quantities. All agree with their stored displays. Every numerical quantity in A8 resolves.

Selected values:

| Quantity | Independent value |
|---|---|
| Full-trade volume | 0.727351849275751124559049312110 |
| Informed share | 0.462117157260009758502318483644 |
| End of the sale margin, r_S | 2.124148132815450673539019415310 |
| Entry ceiling, r_C | 3.592658518794661833335916059883 |
| Weighted impact difference at r_1 | 0.257947801368128764778115708271 |
| Price gap immediately below the ceiling | 0.969913046653425916825577230311 |
| Price gap immediately above the ceiling | 0.108077876964490166067483397538 |
| Ceiling price-gap fall | 0.861835169688935750758093832773 |
| Class term of winner covariance at r_1 | 0.028010147409593433116431962492 |
| Entry term of winner covariance at r_1 | 0.223853183433327930814410271765 |
| Winner second difference at r_1 | 0.615529289315002439625579620911 |
| Volume bound | 200/259 |
| Volume margin | 0.044848922925021076213151460091 |
| Band incentive margin | 0.024767976108430967149092579830 |
| Preparation-report mean at r_1 | 0.160591936090535205300927678803 |
| Preparation-report mean at r_2 | 0.701041666666666666666666666667 |
| Threshold-pair buying probability at 1.60 | 0.492845139150600755785497193516 |
| Threshold-pair purchase entry at 1.60 | 0.506106106106106106106106106106 |
| Threshold-pair mean order at 1.60 | 0.082827989986259489083818427134 |
| Threshold-pair sale payoff at 1.60 | -0.0059375 |
| Threshold-pair total entry at 1.60 | 0.321310960228346420134411033246 |

The independent root evaluations also give `r_A=1.393957920279251333027115442`, `r_F=1.467127041293093798614599488` and `r_N=1.747877538267962743567348178`, confirming the intervals used by the example.

At prior `3/5` and strength 3, the sale-price inversion recovers presence `0.336121768915121197397183549903` and the prior exactly to the evaluation precision. The balance residual has magnitude below `10^-80`. In the purchases-only construction at prior `3/5` and strength `7/5`, the two segment endpoints and the example's slot give identical class-conditional order laws. At the left endpoint the buying probability is one; at the right endpoint the liquidity probability is one third. Exact rational arithmetic supplies the ceiling obstruction above.

## Earlier text, language and notation

The comparison with the preceding A8 accounts for every mathematical result needed by S5. The example's conclusions and their proofs are present, with their broader general statements before them. The rounding illustration at the sale boundary, the shares 0.9 and ratio 0.1 illustrations, and the paragraphs naming numerical implementation artifacts are absent as the statement notes direct. No result or needed fact retained by the plan is missing. The boundary distinction between mixing and abstention remains in A.11(b) and the example's identification interval.

The package contains no implementation artifact names, internal example label, tie-rule codes, forbidden status labels, defensive passage or account of its own drafting. The language scan reports one mathematical interval-expression match, at line 437, and 21 permitted tie phrases. The interval expression states the exact derivative condition within its claim and is acceptable. The notation issue A8-R2 requires a separate source read; it is absent from the scan's matches.

## Build and page reading

The private manuscript build completes successfully as a 146-page document. Every page containing A8, pages 122-141 inclusive, was read as a rendered page image. The sign table, long displays, proof continuations and example are legible and have no clipping or overlap. A8 has no overfull boxes, undefined references or unknown numerical quantities. Its propositions print A.10-A.13, and its corollary prints A.3.

The supplied coexistence label resolves to Corollary 2 in this build. The unknown numerical quantity `margin_rho2Delta_r1_B_frac` belongs to A4 at line 627 and is outside this package. It is not an A8 issue.

The manuscript and frozen statement have the same contents at the initial and final fidelity readings. No tests or assertions were written or executed. All build products and calculation materials are confined to the private scratch folder named by the brief.

The language review of this report treats source locations, the requested stage and proof references, and the evidence descriptions as report metadata. Its remaining matches identify those requested fields and the permitted tie-rule phrases. No personal, account or software-assistant name appears.
