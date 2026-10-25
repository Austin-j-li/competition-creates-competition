# Foundations and ownership: statements and sources

Mathematics writer's package for area A. The formal statements are in `A.tex`; the complete arguments for the three assigned obligations are in `O2/O2_proof.tex`, the preparation-cost steps in `O2/O2_cost_floor.tex`, `O6/O6_proof.tex` and `O7/O7_proof.tex`. The manuscript locations below are relative to `slot/manuscript/`.

## Statements, labels and numbers

| Statement | Label | Number | Source | Manuscript location |
|---|---|---|---|---|
| Scope of beliefs, prices and trading | `par:a2-scope` | Unnumbered paragraph | Generality report, section 4, item 1 | `appendix/A2_beliefs_trading.tex:7-8` |
| Constructed tuples | `par:constructed-tuples` | Unnumbered paragraph beside Lemma A.2 | Reduction report, sections 2 and 4.1; referee report W3, Shared Candidate 1, section 4 | `appendix/A2_beliefs_trading.tex:165-170` |
| The auction through the spread and threshold | `lem:reduction` | Lemma A.4 | SCAN Part 2; reduction report, section 2 | After `appendix/A2_beliefs_trading.tex:230` |
| The two numbers along a path | `lem:twonumbers` | Lemma A.5 | Reduction report, section 3(a); referee report W1, Solver B 1 | After `appendix/A2_beliefs_trading.tex:230`; supports `appendix/A4_coexistence.tex:24,57-58` |
| Liquidity scope | `par:beta-scope` | Unnumbered paragraph | O2 and the result-by-result inventory in its notes | `appendix/A2_beliefs_trading.tex:232-236`; footnote at `sections/02_model.tex:123-125` |
| Competition creates competition, full statement | `prop:ccc` | Proposition 2 | Existing Proposition 2; referee report W2, Shared Candidate 3 and Proposition 2; O6 | `sections/04_equilibrium_results.tex:11-44`; ownership/share argument at `appendix/A3_proposition2.tex:75-86` |
| Decisive advantage | `lem:decisive` | Lemma A.6 | Referee report W2, Shared Candidate 2, Decisive advantage and the uniform-family calculation | After `appendix/A3_proposition2.tex:110`; the economic sentence belongs at `sections/04_equilibrium_results.tex:63-67` |
| Decisive advantage, main-text sentence | `par:decisive-main` | Unnumbered paragraph | Referee report W2, Shared Candidate 2 | `sections/04_equilibrium_results.tex:63-67` |
| Uniform-family scope of value classes and priors | `par:uniform-classes-scope` | Unnumbered paragraph; refers to Proposition A.4, source number A.5 | Generality report, section 4, item 2; referee report W2, Proposition A.5 | `sections/06_robustness.tex:25-36`; `appendix/A6_robustness.tex:157-195` |
| Complementary private signals | `prop:signals` | Proposition A.6, source number A.7 | Referee report W2, Proposition A.7; generality report, Complementary signals | `appendix/A6_robustness.tex:383-442,481-489` |
| Recruitment and ownership in the example, full statement | `prop:region`, alias `cor:ccc-example` | Corollary 1, source number Proposition A.1 | `appendix/A3_proposition2.tex:157-221`; PLAN S9 and Part 6; O6 and decisive advantage | `appendix/A3_proposition2.tex:157-221` |
| Corollary 1, short main-text form | `form:ccc-example-main` | Corollary 1, same result | Full Corollary 1 in this package | `sections/04_equilibrium_results.tex:69-131`, at the opening of Section 4.2 |
| Exact takeover-share comparison | `eq:a3-share` | Equation number assigned at appendix integration | Referee report W2, Shared Candidate 3; O6 | Inside Proposition 2(ii)'s full statement and its ownership argument |

The proposition counter excludes the example statement of Proposition A.1. Hence the research parameter region is Proposition A.1, fixed information A.2, preparation cost laws A.3, value classes and priors A.4, many classes A.5 and complementary signals A.6. The full Corollary 1 uses the named environment with fixed label value 1 for `prop:region` and its alias `cor:ccc-example`; it leaves the appendix corollary counter untouched. The main-text form has fixed label value 1 as well. Proposition 2 stands in full in Section 4.1, with (H1) to (H3) displayed, as in wording target T-4.1. Lemmas A.1 to A.3 retain their numbers; the reduction, path and decisive-advantage lemmas are A.4 to A.6. No table is added by this package.

## Scope by statement

- The scope paragraph assigns every-profile generality to the belief lemma. The price lemma requires its tuple conditions, and the trading lemma its price, bid and entry-floor conditions.
- Constructed tuples require positive spread, the nonnegative entry gain supplied by the cash auction, an interior prior, full liquidity support, entry in `[rho,1]`, and monotonicity across distinct posteriors. At a common posterior, equal entry is the exact additional condition for a common price. Both investor rules and both challenger rules are covered.
- The reduction fixes the two-point preparation cost, prior, trading cost, liquidity law and chosen tie pair. Both auctions satisfy the class ranking and have positive spread and profit gap. Trading patterns are endogenous, including mixed orders. With research, the same quadratic coefficient and cap are fixed, and optimal hypothetical-success orders are required at zero research. The equality of projected equilibrium sets includes every equality case under the selected tie rule.
- The path lemma fixes both class laws, the reserve and preparation cost. Its auction-only comparisons have no prior or trading pattern. The spread and profit changes have exact integral strictness conditions. Threshold and product monotonicity require positive profit gap and spread and a nonnegative threshold. Their strictness follows the displayed increments, including a zero threshold. J's derivative has two opposing terms.
- Proposition 2 keeps arbitrary interior priors, the two-point cost, continuous stochastically ordered laws, and all three strict windows. It forces abstention, then full informed trade, then full informed trade with floor entry. It holds under all four tie rules. Outbidding at the stronger law suffices for the additional ownership and share conclusions. Strict share growth is exactly `W_L(F_0)>0`.
- Decisive advantage is a property of a family of incumbent laws at fixed class laws, reserve and high cost. At a recruiting law its conclusion requires a positive profit gap and interior beliefs; fixed presence and research with a cap below one supply the latter. It covers all priors and all four tie rules. Its equivalence for point classes is for the full uniform family `r>0`; a restricted family satisfies the sufficient direction.
- The uniform-family scope sentence concerns the existing existence proposition for all ranked finite-mean classes with a positive mean gap, a positive reserve, any interior prior and slot, and any interior rho. It keeps that proposition on uniform incumbents.
- Complementary signals use prior one half, ranked finite-mean classes, a continuous FOSD pair, the two-point preparation cost, the stated binary accuracies, and conditional independence of both signals and both values given class. Cost and slot draws are independent. Its strict profit and trading windows force abstention at F_0 and full purchases/sales by signal at F_1 under all four tie rules. Orders are unique; preparation at a remaining private-signal threshold follows the selected challenger rule. The optional one-pair inequality is strict. Ownership includes `W_H(F_1)`.
- Corollary 1 fixes the example's auction and cost primitives and strengths. Parts (a), (b) and (d) have prior one half; part (c) fixes `1+u=e` and gives its entire prior interval. The interior band holds under all four tie rules. The lower-band equality explicitly distinguishes certain preparation from arbitrary preparation at indifference. Part (e)'s cost window describes the simultaneous decisive-advantage and affordability restrictions for the point values and strength range; its statement does not assign (H1)--(H3) to every cost in that window.

## Derivations

### Reduction and path

Subtracting the competitive price from the class payoff cancels `t_0` and the common `e w_L`. Preparation optimality becomes the threshold rule because `B(mu)-c_H=gamma(mu-tau)`. At every interior posterior `w_L+Delta_T mu>0`, so the price partition is exactly the posterior-entry partition. This partition survives a change in auction levels at fixed spread and threshold. Bayes' rule at a price is then the ratio of sums of identical likelihood ratios. A research deviation holds these prices and entry fixed, so its maximum payoff is `lambda_tilde Psi-(a/2)lambda_tilde^2`; strict concavity gives the stated intensity condition.

The gap integrals give `Delta_T+gamma=bar Gamma`, with `bar Gamma` fixed. For two ordered laws the profit gap falls by the spread increment. Subtracting the two threshold ratios gives the displayed threshold-increment formula, which proves its exact strictness condition. Expanding the product gives the product-increment formula. Differentiation of `J=Delta_T(g_H-c_H)/gamma` gives the two terms in its derivative.

For the translated uniform law every incumbent lies above ell and below h. Thus low-class profit is zero, high-class profit is `h-r`, the spread is `r-ell`, and J falls from 2 to `13/10`. The print-only computation gives derivatives `-1` and `-47/25` at the endpoints. The uniform-incumbent example's positive J direction follows from the affordability argument in referee report W1, equations (4)--(8), with cost margin `2/5`. Thus the direction of J has genuine auction dependence.

### Ownership and decisive advantage

O6 gives the complete share argument. Its cross-product comparison avoids dividing by a zero low-class winning probability. Outbidding at F_1 implies outbidding at F_0, and `e_H>e_L` gives strict share growth exactly before complete saturation at the weaker endpoint.

Any price posterior is below one. A recruited high-cost challenger therefore satisfies `c_H<=B(mu)<g_H` when the profit gap is positive. Decisive advantage gives `W_H=1`, including a challenger preparation tie. For point classes and `r>h`, uniform integration gives `W_H=h/r<1` and `g_H=(h^2-p^2)/(2r)`, whose supremum as r approaches h from above is `(h^2-p^2)/(2h)`. This proves both directions of the full-family criterion. At the example's cost the actual profit crossing on the middle uniform piece is `4+sqrt(63)/2`, below h.

### Corollary 1

Exact auction integration gives spreads `(1/60,2/3,169/180)` and thresholds `(195/308,141/200,4245/5804)`. The weak high-cost and trading margins are `287/240` and `1/300`. At prior one half the recruitment condition at r_1 is `u>82/59`; exclusion at r_2 is `u<2686/1559`. The strong trading bound is `u<19/3`, and is redundant in this band. Each equality case follows from full orders, the threshold entry rule and strict trading payoffs.

With `1+u=e`, the inverse of the top posterior at a threshold tau is `tau/[tau+(1-tau)e]`. Applying it at the two thresholds gives the stated endpoints. The remaining prior bound is `pi<195/308`; the trading window `(0.270432341937604,0.729567658062396)` contains the resulting prior intervals. Class entry gives total entry and ownership directly; O6 evaluates the shares from class ownership probabilities.

### Complementary signals

Conditional independence gives public class belief `(1-alpha_I)+(2alpha_I-1)nu_I(x)`. Signal-specific entry gives `e_H(mu)>=e_L(mu)>=rho`, and `rho Delta_T<=Delta_P<=bar Delta_P`. The nonzero signal-posterior bounds therefore give the stated upper and lower trading returns. Their strict signs force the unique signal orders. At the weak law, the private posterior alpha_C cannot recruit; FOSD preserves that exclusion at a prior public belief against the stronger law. The favorable purchase/signal pair strictly recruits, so both class entry and total entry exceed rho. At the stronger law the positive spread orders the three prices strictly.

Preparation and both values are independent given class: signals and orders select class but do not select values within class. Averaging conditional entry over the class-specific order law therefore gives `Own_{H,1}=bar e_H W_H(F_1)/2`. This supplies the ownership factor absent from the point-class expression. In the one-pair case the probability of `(X,S_C)=(1,+)` in class H is `alpha_C(b+alpha_I lambda)`; the displayed class-average entries `bar e_H` and `bar e_L` follow.

## Numerical-table additions

Every quantity printed in an example statement uses `\reg`. Mathematical constants in general identities and endpoint hypotheses keep their usual notation. The following 20 names are absent from the numerical table. The first 17 occur in `A.tex`; the final three occur in `O7_proof.tex`.

Let `beta=294655/1000000`, `u=e-1`, `lambda=u beta/(1+u beta)` and `b=beta/(1+u beta)`. In the last three rows, `fr(y)=1+y+sqrt(y^2+2y)`.

| Name | Exact value | Proposed display | Computation |
|---|---|---|---|
| `twonum_h` | `10` | `10` | High-class value of the translated-uniform economy. |
| `twonum_ell` | `1` | `1` | Low-class value. |
| `twonum_p` | `1/2` | `1/2` | Reserve. |
| `twonum_cH` | `2` | `2` | Preparation cost of the translated-uniform example. |
| `twonum_halfwidth` | `1/10` | `1/10` | Half-width of its incumbent law. |
| `twonum_rlo` | `7` | `7` | Lower center of its incumbent interval. |
| `twonum_rhi` | `15/2` | `15/2` | Upper center. |
| `twonum_Jlo` | `2` | `2` | `(7-1)(1-2/(10-7))`. |
| `twonum_Jhi` | `13/10` | `13/10` | `(15/2-1)(1-2/(10-15/2))`. |
| `share_H_r0` | `6/11` | `0.545455` | `pi/[pi+(1-pi)ell/r_0]`. |
| `share_H_r1_B` | `[3+(12e-3)beta]/[4+(13e-1)beta]` | `0.830691` | `e_H/[e_H+e_L/3]` at prior one half. |
| `share_H_r2_B` | `18/23` | `0.782609` | The floor-entry takeover share at r_2. |
| `decisive_cost_lo_frac` | `399/80` | `399/80` | `(h^2-p^2)/(2h)`. |
| `afford_cost_hi_frac` | `32/5` | `32/5` | `h-r_2`. |
| `margin_decisive_B_frac` | `81/80` | `81/80` | `6-399/80`. |
| `margin_afford_uniform_B_frac` | `2/5` | `2/5` | `10-18/5-6`. |
| `decisive_rmax_B` | `4+sqrt(63)/2` | `7.968627` | Upper root of `g_H(r)=6` on the piece `p<=r<=h`. |
| `r_pool_B` | `fr((k/rho)[2+(e-1)beta/(1-beta)])` | `1.911775` | Unique capped mixed-sale strength with sale probability `beta/(1-beta)`. |
| `pool_mu_B` | `k/[rho Delta_T(r_pool_B)]` | `0.367944` | Zero net return on the mixed sale. |
| `pool_price_B` | `t_0(r_pool_B)+rho[t_L(r_pool_B)-t_0(r_pool_B)]+k` | `0.497885` | Price identity at that posterior. |

Existing entries supply all other example inputs, slot bands, prior endpoints, entry levels and ownership levels. In particular, `own_r0` supplies the same ownership value at r_2. The share names follow the delivery lens; `own_share_r0` and `own_share_r1_B` in the wording targets refer to `share_H_r0` and `share_H_r1_B`. The single proposed names at the numbers stage are `margin_unif_afford_B` for `2/5`, `cH_afford_ceiling_B` for `32/5`, and `cH_DA_floor_B` for `399/80`; `share_H_r0`, `share_H_r1_B` and `share_H_r2_B` name the takeover shares. Their fraction and decimal displays describe the same quantities. The present fraction displays in `A.tex` retain `margin_afford_uniform_B_frac`, `afford_cost_hi_frac` and `decisive_cost_lo_frac` until that stage.

## O2, O6 and O7 verdicts

- O2: the inventory covers every main-text and appendix result. The common zero-order bound and all-profile exclusion have the smaller liquidity domain. The preparation-cost proposition has the larger domain by the price-preimage argument, which also covers prices pooling zero. The research parameter-region and identification feasibility bounds retain the model's parameter domain. The footnote and appendix paragraph are supplied in O2.
- O6: the planned weaker-endpoint strictness condition holds exactly under outbidding. The proof treats saturation explicitly and gives the cross-product condition without outbidding.
- O7: the required equal-entry condition holds in recruiting research, because both nonpurchase posteriors lie below one half and hence below tau. The unique pooling strength on its capped mixed-sale stretch is supplied in exact form.

## Build, reading and language

The statements build to six pages; the liquidity-scope fragment, preparation-cost steps and takeover-share fragment each build to one page, and the pooling fragment to two. All eleven pages have been rendered and read. There are no errors, undefined references or box warnings. The only build warnings are the 17 pending numerical names in the statements and three in the pooling fragment, with exact values in the table above.

The five TeX sources have zero counted language findings. Their six allowed phrases are the frozen tie-rule wording: four arbitrary-preparation phrases and two mixing-investor phrases. The notes' matches name source locations, integration destinations, obligation identifiers, precision or this required language judgement; each is coordination metadata, outside manuscript prose. The source-heading word at issue A-15 names the cited example calculation. Every counted notes match has this provenance or reporting role. Status, defensive phrasing, history, example naming, personal or system names, house-style findings, interval claims and placeholders have zero findings.

All three print-only computations finish with exit status zero. They give the exclusion economy's strict optimal orders and recruitment at zero, translated-uniform return endpoints 2 and 13/10, takeover shares 0.545455, 0.830691 and 0.782609, and the pooling posterior and price with positive recruitment, mixed-sale and cap margins.

## Integration dependencies

The three numerical additions associated with pooling are used by its example sentence in A.5. The statements have 17 unknown numerical names pending the numbers stage. Their exact values are all in the table above. Formal example statements also have their own numerical rows, including the translated-uniform J comparison.

The full Corollary 1 and its main-text form use named environments and fixed label value 1 without changing the appendix counter. O2 supplies the nonzero-price argument and narrows the many-class and signal bounds to nonzero orders. `O2_cost_floor.tex` supplies Steps 1 and 2 of the preparation-cost proof. The research parameter-region necessity step cites the full-purchase result. Its identification part letters follow the empirical package's final arrangement.

The coordinator owns the statement freeze and numbers-stage reconciliation.

## Changes after the referee

All proposed findings within area A have their stated resolution; there is no mathematical disagreement.

| Issue | Resolution |
|---|---|
| A-01 | Full Corollary 1 has a named environment and fixed value 1 for both labels; the appendix corollary counter is untouched. |
| A-02 | Section 4.1 takes the full `prop:ccc` statement with (H1)--(H3), as T-4.1 requires. There is no short Proposition 2 form in `A.tex`. |
| A-03 | `A.tex` and `O2_proof.tex` have the same exhaustive liquidity-scope paragraph, including the fixed-slot qualifier for corollaries. |
| A-04 | The pooling paragraph and its notes state the prior one half and the mixing-investor rule. |
| A-05 | The price-preimage proof ends at its likelihood-ratio argument. `O2_cost_floor.tex` supplies Steps 1 and 2 of the preparation-cost proof; the broader inventory is in `O2_notes.md`. |
| A-06 | The uniform example's direction of J cites Proposition 3(c). |
| A-07 | The translated-uniform economy has its own `twonum_h`, `twonum_ell`, `twonum_p` rows, with exact values 10, 1, 1/2. |
| A-08 | Main-text Corollary 1 expresses floor entry as rho and floor ownership as rho/2. |
| A-09 | The proposed single names and exact values are in Numerical-table additions; reconciliation belongs to the numbers stage. |
| A-10 | The O2 inventory cites the affected coexistence and research lemmas by label. |
| A-11 | Part (e) names affordability and cites Proposition 3(c); its recruitment bound quantifies over slots, priors, rho, k and research at the fixed class values, reserve and cost. |
| A-12 | The reduction distinguishes fixed presence lambda from research presence lambda_hat. |
| A-13 | Complementary signals use bar e_H and bar e_L for class averages; decisive advantage holds at F_1. |
| A-14 | The value-class scope sentence includes the reserve p>0. |
| A-15 | The notes describe print-only computations, contain the required source and precision information, and the W2 source comment names the verification for the example. |
| A-16 | The ownership intuition follows the O6 proof. |
| A-17 | The wording-target referee owns the dependency; no area-A edit is assigned. |
