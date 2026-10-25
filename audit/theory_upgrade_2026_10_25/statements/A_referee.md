# Area A: referee assessment

Every conclusion in area A follows from the referee reports' proofs under the stated hypotheses. I found no mathematical error and no overclaim, so no issue is a blocker. Three statements need repairs before the freeze (A-01 to A-03), and the pooling paragraph of O7 lacks the mixing-investor qualifier that `PLAN.md` S4 lists for research (A-04). **O2: accept. O6: accept. O7: accept, with A-04.** Every number the area adds reproduces by an independent method.

Locations are relative to `audit/theory_upgrade_2026_10_25/statements/` unless a path says otherwise. The manuscript is `slot/manuscript/`.

## Verdict per statement

| # | Statement (label) | Verdict | Reason or required repair |
|---|---|---|---|
| 1 | Scope of beliefs, prices and trading (`par:a2-scope`) | accept | The belief lemma is a statement about every profile; the price and trading lemmas hold for every tuple that meets their conditions. |
| 2 | Constructed tuples (`par:constructed-tuples`) | accept | Positive spread and full support give `w(mu) > 0` at every posterior, so equal prices force equal posterior and equal entry, and conversely. Both challenger rules are covered. O7 gives the same paragraph with its proof; S5 should take that version. |
| 3 | Lemma A.4, the auction through the spread and the threshold (`lem:reduction`) | accept | `B(mu) - c_H = gamma (mu - tau)`, the payoffs of Lemma A.3 and the price partition depend on the auction only through the spread and `tau`; with research, `Psi` and the best reply `min{lambda-bar, Psi/a}` use the same payoffs. Minor wording, A-12. |
| 4 | Lemma A.5, the two numbers along a path (`lem:twonumbers`) | accept | `t_j + g_j = E_j theta` gives the fixed mean gap; both integral identities, the threshold increment, the product increment and the formula for `J'` check by direct algebra. The translated-uniform economy has `J(7) = 2 > J(15/2) = 13/10`. A-06, A-07. |
| 5 | The liquidity share (`par:beta-scope`) | accept | Its claims are true, but it is incomplete where completeness is its purpose, and a second version of the same paragraph stands in O2. A-03. |
| 6 | Proposition 2, full statement (`prop:ccc`) | accept | Proof steps 0 to 6 of `appendix/A3_proposition2.tex` use only nonzero-order bounds, so `0 < beta < 1/2` holds. The share condition (1) is the cross-product of the two shares, with positive denominators from (H1). Under outbidding the share is nondecreasing and rises strictly exactly when `W_L(F_0) > 0` (O6). Weak and strict are right. |
| 7 | Lemma A.6, decisive advantage (`lem:decisive`) | accept | A recruited challenger has `c_H <= B(mu) < g_H` at every interior belief when `gamma > 0`. For point classes and the full uniform family, `g_H(r) = (h^2 - p^2)/(2r)` for `r >= h` has supremum `(h^2 - p^2)/(2h)`, not attained above `h`, so the weak inequality is exact. |
| 8 | Proposition 2, main-text form (`form:ccc-main`) | missing qualifier | Its content matches the full statement, but it names (H1) to (H3) "of Proposition 2" from inside Proposition 2 and never states them. A-02. |
| 9 | Decisive advantage, main-text paragraph (`par:decisive-main`) | accept | Matches Lemma A.6. |
| 10 | Value classes and priors, scope sentence (`par:uniform-classes-scope`) | accept | Matches the existence proposition (`prop:classes`, A.4 after renumbering), which stays on uniform incumbents. Minor, A-14. |
| 11 | Proposition A.6, complementary private signals (`prop:signals`) | accept | The order bounds use signal posteriors at nonzero orders only; price revelation uses `Delta_P >= rho Delta_T > 0`; entry given class is independent of the values, so `Own_{H,1} = e_H W_H(F_1)/2`. The one-pair case needs `B_{F_1}(mu^C_-(M^I)) < c_H` and `B_{F_1}(alpha_C) <= B_{F_0}(alpha_C) < c_H`, both available. Minor wording, A-13. |
| 12 | Corollary 1, full statement (`prop:region`, `cor:ccc-example`) | accept | Parts (a) to (e) reproduce exactly. The environment prints the wrong number in the manuscript. A-01, A-11. |
| 13 | Corollary 1, main-text form (`form:ccc-example-main`) | accept | Prior one half, the slot band, the example slot and all four tie rules are stated. Minor, A-08. |
| 14 | Exact takeover-share comparison (`eq:a3-share`) | accept | Exact, including zero low-class win probabilities. |

Qualifiers checked against `PLAN.md` S4. Tie rules: every result of the area states them or holds under all four. Weak against strict: Proposition 2(ii), Lemma A.5, Lemma A.6 and Corollary 1(e) carry the right inequality. A nonnegative threshold for the path monotonicity: present in Lemma A.5. Prior one half and the mixing investor for research: present everywhere except the O7 pooling paragraph (A-04). Two-sided trade, the weighted test and the winner trend do not arise in this area.

Numbering follows decision 7 and `PLAN.md` Part 6. The added lemmas are A.4 to A.6, so Lemmas A.1 to A.3 keep their numbers. The appendix propositions move up by one: research parameter region A.1, fixed information A.2, preparation cost laws A.3, value classes A.4, many classes A.5, complementary signals A.6. No table is added. The one numbering defect is the counter of the full Corollary 1 (A-01).

## The proofs O2, O6 and O7

### O2, the liquidity share: accept

I checked the argument line by line.

1. **Price preimage.** A price whose preimage contains a nonzero order has liquidity mass at least `b`, and each class adds informed mass between zero and `lambda`. The likelihood ratio therefore lies in `[1/(1+u), 1+u]`, and the price posterior in `[m(pi), M(pi)]`. No comparison of `b_0` with `b` enters. Correct.
2. **Preparation cost laws (`prop:atomless`), the extension to `beta < 1/2`.** I read the manuscript proof (`appendix/A6_robustness.tex:84-130`). Its Step 1 is the only use of the all-price floor. Under the preimage bound, the low-cost component prepares at both nonzero-order prices, because its costs are at most `L < B_1(m) <= B_i(m)`. That floor `rho` at the orders `-1` and `1` is all that Step 2 needs at `F_1`. At `F_0`, `Delta_0 < k` forces abstention for any entry in `[0, 1]`. Every posterior is then the prior, and `L < B_1(m) <= B_0(pi) < c_-` gives entry `rho`. At `F_1`, full orders give posteriors in `{m, pi, M}`; every price belief averages these, so the low component prepares everywhere, and price sufficiency and the strict cost windows give the tuple. The third-economy paragraph extends the same way. The extension holds, and the earlier survey's restriction of this proposition to `beta <= 1/3` is unnecessary.
3. **Exclusion above one third.** I recomputed the example by hand in exact fractions. `b = 1/5`, `b_0 = 1/10`, `u = 5/2`, `m = 18/25`, `M = 63/65`, `tau = 39/40`, `mu(0) = 54/55`, `c_H - B(M) = 5/104`. The purchase earns `-1/30` and the sale `7/100`; every comparison is strict. The general construction is also right: as `pi` tends to one, `m(pi)` tends to one, so `1 - pi < m(pi)` is attainable, and any `c_H` in `(B(M), B(mu(0)))` is positive. Corollary A.1 therefore needs `beta <= 1/3`, and the needed bound is exactly the zero-order bound.
4. **The remaining inventory.** I read the following proofs and found only nonzero-order bounds or explicitly computed posteriors:
   - Proposition 2 (`appendix/A3_proposition2.tex:11-110`);
   - many classes (`appendix/A6_robustness.tex:277-346`), where the order payoffs use the order posteriors `mu(q)` at `q = +1, -1` and `e(q) >= rho`, and the price-belief bound is never used to force orders;
   - complementary signals (`appendix/A6_robustness.tex:383-470`);
   - the research lemmas `lem:a5-buy` and `lem:a5-strong` (`appendix/A5_research.tex:105-230`), where uniqueness under (U) bounds `U_H(1)` and `U_L(-1)` only;
   - the research parameter region (`appendix/A5_research.tex:316-384`), which fixes `beta` at the example value or ranges over `(beta_lo, 1/3]` and so keeps its domain.

   Referee report W3, Shared Candidate 1, section 1, independently proves the extension of positive research to `beta < 1/2`. In Proposition 3, the low class cannot sell profitably in the coexistence region, because `rho Delta_T m(pi) < rho Delta_T max{pi, 1-pi} <= k`. The zero order is therefore never the recruiting order there, and the region theorem needs no zero-order bound.
5. **Not read line by line.** I took the remaining inventory rows on the writer's argument and the referee reports: fixed information, welfare and payment (A7), the empirical results (A8), Proposition 1, and the internals of areas B and C beyond the lemmas named above. Nothing I read contradicts them.
6. **Integration point.** `C.tex:62` already narrows the zero-order part of the research bounds to `beta <= 1/3`, as O2 requires.

Required changes: A-03 and A-05 (structure), A-10 (lemma numbers). O2's footnote is broader than wording target T-2.3, and correct (A-17).

### O6, the takeover share: accept

The cross-multiplication criterion is exact for nonnegative terms with positive sums. Positive sums come from (H1): `B_1(M) > c_H > 0` gives some `g_{j,1} > 0`, hence `W_j(F_1) > 0`, and stochastic dominance gives `W_j(F_0) >= W_j(F_1)`. Under `W_H(F_1) = 1` the condition is `e_H W_L(F_0) > e_L W_L(F_1)`, which holds strictly whenever `W_L(F_0) > 0`, since `e_H - e_L = (1-rho) lambda > 0`. When `W_L(F_0) = 0`, both shares are one. The plan's condition on the weaker incumbent is exact. Referee report W2's condition on the stronger incumbent is sufficient, and the writer says so. The computation executes cleanly, and its values agree with mine (table below). Minor, A-16.

### O7, pooled orders: accept, with A-04

The constructed-tuples paragraph and its proof are correct under both challenger rules. The research paragraph is correct: both nonpurchase posteriors are at most one half, below `tau`, so both have entry `rho`. They coincide exactly when `sigma_L(-1) = b_hat/(b_hat + b_hat_0) = beta/(1 - beta)`, whatever the research intensity. In the example the sale probability `(rho Delta_T/k - 2)/(e - 1)` rises strictly from zero at `r_N` to one at `r_S`, because the spread `(r - ell)^2/(2r)` rises for `r > ell`. My recomputed ordering `r_lambda-bar = 1.67763283439 < r_N = 1.74787753827 < r_S = 2.12414813282 < r_C = 3.59265851879` puts the unique crossing on the capped recruiting segment. The mixed sale exists only when an indifferent investor may mix: with an abstaining investor there is no recruiting research on `(r_N, r_S]`. The example sentence therefore needs that qualifier (A-04). The sentence "Each construction below applies this paragraph..." (`O7/O7_proof.tex:35-37`) binds every S5 construction to give equal entry to orders that share a posterior; S5 must keep that property.

## Issues

### A-01: should fix: the counter of the full Corollary 1

**Location:** `A.tex:287-288`; `A_notes.md:112`.
The full Corollary 1 uses the shared `corollary` environment after `\setcounter{corollary}{0}`. Standalone it prints "Corollary 1". In the manuscript, `slot/manuscript/main.tex:118-120` sets the appendix corollary counter to `A.\arabic`, so the same source would print "Corollary A.1", colliding with `cor:exclusion` and resetting the appendix corollary sequence. The notes' statement that it has an independent counter is not what the file does.
**Fix:** state it as `\begin{named}{Corollary 1 (Recruitment and ownership in the example, full statement)}` with `\fixedlabel{prop:region}{1}` (and the alias), as the main-text forms already do. Do the same for the full Corollary 3 in area C. Correct the sentence in the notes.

### A-02: should fix: the main-text form of Proposition 2

**Location:** `A.tex:199-211`; the table rows of `A_notes.md` for `prop:ccc` and `form:ccc-main`, both placed at `sections/04_equilibrium_results.tex:11-44`.
The hypotheses (H1) to (H3) are not stated where the proposition is stated. The short form says the primitives "satisfy the high-cost window, the trading-cost window and the exclusion condition of Proposition 2", but in the main text that sentence is Proposition 2 itself. Wording target T-4.1 instead keeps the full main-text proposition and adds the share sentence. The two plans conflict.
**Fix:** follow T-4.1. The full statement (`prop:ccc`) stays in Section 4.1, and the short form is dropped, or kept only as a reading aid in the notes. If the coordinator prefers the short form in the main text, it must display (H1) to (H3), and the full statement is then restated in A3 under a named heading.

### A-03: should fix: the liquidity-share paragraph

**Location:** `A.tex:127-133`; `O2/O2_proof.tex:12-19`.
Four problems.
1. "Its consequences include the exclusion bound and the zero-order part of the research posterior bound" is not exhaustive, while the point of the paragraph is the exact list.
2. The closing sentence lists Propositions 1 to 4, the corollaries, the reduction, the path comparisons and the signal result. It omits fixed information, value classes, many classes, the welfare and payment results, the empirical results and Lemma A.6, which O2 shows hold for every `beta < 1/2`. A reader would infer that they stay at `beta <= 1/3`.
3. "Their three main-text corollaries hold for every `0 < beta < 1/2`" does not fit Corollary 3, which fixes `beta` at the example's value (`C.tex:314`).
4. `O2_proof.tex` gives a second, different version of the same paragraph for the same place (`appendix/A2_beliefs_trading.tex:232-236`).

**Fix:** keep one version. Suggested: "The bound `beta <= 1/3` is the inequality `b_0 >= b`. It extends the posterior bounds of the nonzero orders to the zero order, and through it enters only Corollary A.1 and the zero-order part of the research bounds. The research parameter region and the slot-feasibility parts of identification range over the slots with `beta <= 1/3`. Every other result holds for every `0 < beta < 1/2`; a corollary that fixes the slot holds at that slot."

### A-04: should fix: the mixing investor in the pooling paragraph

**Location:** `O7/O7_proof.tex:40-52`; `O7/O7_notes.md`, "Scope and argument".
"In the example, during recruiting research at the cap, this happens at exactly one strength" needs low-class mixing on `(r_N, r_S)`. When an indifferent investor abstains, recruiting research does not exist on `(r_N, r_S]` (referee report W3; `WORKAROUNDS.md`, W3 item 5), so there is no pooling strength. `PLAN.md` S4 lists "prior 1/2 and the mixing investor for research" as an acceptance qualifier, so this fix gates the freeze.
**Fix:** "At the prior `1/2`, when an indifferent investor may mix, let `tau > 1/2`, ...". The general sentence (equal posteriors exactly when `sigma_L(-1) = beta/(1 - beta)`) holds for any profile with that sale probability and needs no rule.

### A-05: should fix: the proof environment of the price-preimage claim

**Location:** `O2/O2_proof.tex:21-48`.
The proof of "A price reached by a nonzero order" is its first paragraph. The rest of the environment re-proves Proposition A.3 at `beta < 1/2` and then surveys the many-class, signal, research, welfare and empirical results. It ends with "These arguments account for every use of a posterior bound in the remaining results", a sentence of bookkeeping (rule 3) that no proof supports.
**Fix:** end the proof after the likelihood-ratio paragraph. Move the Proposition A.3 argument into Step 1 of that proof, as `A_notes.md:112` intends. Make the floor at the two nonzero orders the first step, and move the low component's preparation at every price to after the orders are forced. Move the survey to `O2_notes.md`, which already lists the matching manuscript sentences (`appendix/A6_robustness.tex:306-308,402-404`).

### A-06: minor: unsupported example sentence in Lemma A.5

**Location:** `A.tex:122`.
"In the uniform-incumbent example below, `J` rises on `[r_0, r_2]`" is an example claim inside a general lemma, with no proof or reference.
**Fix:** cite the existing path lemma (`lem:a4-path`, `appendix/A4_coexistence.tex:20-62`) or the uniform case of Proposition 3, or move the sentence to the example part.

### A-07: minor: the translated-uniform economy prints through the example's names

**Location:** `A.tex:109-111`.
`\reg{prim_h}`, `\reg{prim_ell}` and `\reg{prim_p}` print the class values and reserve of a different economy. `PLAN.md` S6 gives other economies their own rows.
**Fix:** add `twonum_h`, `twonum_ell` and `twonum_p` (10, 1, 1/2), or write "the example's class values and reserve" and keep the names.

### A-08: minor: decimals beside symbols in the main-text Corollary 1

**Location:** `A.tex:346-348`.
"Entry rises from `\reg{entry_r0}`" prints 0.250000, and "ownership rises from `\reg{own_r0}`" prints 0.125000, beside the symbolic `rho + (1 - rho)(b + lambda/2)` and `[rho + (1 - rho)(b + lambda)]/2`. These values are `rho` and `rho/2`.
**Fix:** write `rho` and `rho/2`, as part (a) of the full corollary does.

### A-09: minor: one quantity, several numerical names

**Location:** the table in `A_notes.md` ("Numerical-table additions"); `B_notes.md:391,441`; `wording_targets.md:1178-1181`.
Several quantities carry more than one name:
- 2/5: `margin_afford_uniform_B_frac` (A) and `margin_unif_afford_B` (B);
- 32/5: `afford_cost_hi_frac` (A), `cH_unif_cap_B` (B) and `cH_afford_ceiling_B` (wording targets);
- 399/80: `decisive_cost_lo_frac` (A) and `cH_DA_floor_B` (wording targets);
- the shares: `share_H_*` (A) and `own_share_*` (wording targets).

**Fix:** in S6, keep one name per quantity, with a fraction and a decimal display where both are needed, and change the other areas to match.

### A-10: minor: provisional lemma numbers in the O2 inventory

**Location:** `O2/O2_notes.md:46-50`.
"Lemmas A.7 to A.11", "Lemma A.12", "Lemma A.13" and "Lemmas A.14 to A.17" will shift when areas B and C add lemmas before them.
**Fix:** cite labels (`lem:a4-path` ... `lem:a5-strong`) and leave numbers to the S12 label map.

### A-11: minor: part (e) of Corollary 1

**Location:** `A.tex:329-337`.
The second condition, `h - r_2 >= c_H`, is not named, so the reader of Corollary 1 cannot see why it is there. It is the affordability condition of the uniform case of Proposition 3. "A recruiting uniform incumbent has `r < ...`" is loose.
**Fix:** name the condition and cite it. Write "for these class values, reserve and cost, every economy with a uniform incumbent `U[0, r]` in which some order recruits a high-cost challenger has `r < ...`, whatever the slot, prior, `rho`, `k` and research".

### A-12: minor: presence in Lemma A.4

**Location:** `A.tex:46`.
"Fix `0 < lambda < 1`" also governs the research part, where presence is the conjectured research.
**Fix:** "At fixed presence, fix `0 < lambda < 1`; with research, presence is `lambda_hat`" (the reduction report's wording).

### A-13: minor: wording in Proposition A.6

**Location:** `A.tex:270-280`.
1. `e_H` denotes both the function `e_H(mu)` and its class average.
2. "The family has decisive advantage at `F_1`" mixes a family property with a single law.

**Fix:** write `\bar e_H` for the class average, as `prop:atomless` does, and write "or if decisive advantage holds at `F_1`".

### A-14: minor: the reserve in the value-classes sentence

**Location:** `A.tex:220-224`.
`prop:classes` assumes a reserve `p > 0`; the sentence omits it.
**Fix:** add "a reserve `p > 0`".

### A-15: minor: notes language

**Location:** `A_notes.md:46,102,106`; `O6/O6_notes.md:37`; `O7/O7_notes.md:27`; `A.tex:177`.
1. The notes say "the CLI", point to a "private area-A folder", and close with "No test suite is part of this work".
2. The source comment at `A.tex:177` quotes a W2 heading that uses the retired word for the example.

**Fix:** write "the print-only computation" and drop the folder pointers and the closing sentence. Cite the heading as "W2, Shared Candidate 2, the verification for the example".

### A-16: minor: intuition inside the O6 proof

**Location:** `O6/O6_proof.tex:48-50`.
The last sentence of the proof, "With outbidding, the stronger incumbent changes only the low class's chance to win...", is intuition.
**Fix:** move it after the proof, or to the main-text reading of Proposition 2.

### A-17: minor: dependency for the wording-target referee

**Location:** `wording_targets.md:236-246` (T-2.3).
The target footnote keeps the older claim for Propositions 2 and 3 only. O2 supports the broader footnote in `O2/O2_proof.tex:7-10`, which is correct.
**Fix:** for the referee of the wording targets: adopt the O2 footnote text after A-03 is settled.

## Recomputed values

Each value comes from an independent print-only computation in the referee's private build folder at 50 digits. Proceeds, profits and win probabilities come from numerical integration of the second-price auction with reserve over the incumbent's law, not from the closed forms. Each root comes from bisection on its defining equation, not from a closed-form inverse.

| Name | Writer's exact value, display | Recomputed | Agreement |
|---|---|---|---|
| `twonum_cH`, `twonum_halfwidth`, `twonum_rlo`, `twonum_rhi` | 2, 1/10, 7, 15/2 | inputs of the translated-uniform economy | n/a |
| `twonum_Jlo` | 2 | `Delta_T = 6`, `g_L = 0`, `g_H = 3`, `tau = 2/3`, `J = 2` | exact |
| `twonum_Jhi` | 13/10 | `Delta_T = 13/2`, `g_H = 5/2`, `tau = 4/5`, `J = 1.3`; `J` falls at every tenth in between (2, 1.8931, 1.7714, 1.6333, 1.4769, 1.3) | exact |
| `share_H_r0` | 6/11, 0.545455 | 0.545454545454545 (entry `rho` in both classes, `W_H = 1`, `W_L = 5/6`) | exact |
| `share_H_r1_B` | `[3 + (12e - 3) beta]/[4 + (13e - 1) beta]`, 0.830691 | 0.83069094523037421444; the closed form agrees to 20 digits | yes |
| `share_H_r2_B` | 18/23, 0.782609 | 0.782608695652174 | exact |
| `decisive_cost_lo_frac` | 399/80 | `g_H(U[0, 10]) = 4.9875`; `g_H` at `10 + 10^-6` is 4.98749950, decreasing above `h` | exact |
| `afford_cost_hi_frac` | 32/5 | `h - r_2 = 32/5` | exact |
| `margin_decisive_B_frac` | 81/80 | `6 - 399/80 = 81/80` | exact |
| `margin_afford_uniform_B_frac` | 2/5 | `32/5 - 6 = 2/5` | exact |
| `decisive_rmax_B` | `4 + sqrt(63)/2`, 7.968627 | bisection on the integrated `g_H(r) = 6` over `(1, 10)`: 7.9686269665968858858; the other quadratic root lies below `p`, where `g_H = 9.5` | yes, 20 digits |
| `r_pool_B` | `fr((k/rho)[2 + (e-1) beta/(1-beta)])`, 1.911775 | bisection on equal sale and zero-order posteriors, with the sale probability itself found by bisection on the sale's zero return: 1.9117746293707232488 | yes |
| `pool_mu_B` | `k/[rho Delta_T(r_pool)]`, 0.367944 | 0.367943952645577 (sale and zero order) | yes |
| `pool_price_B` | 0.497885 | 0.497885379019505 (sale and zero order) | yes |

Also recomputed, and in agreement with the writer:
- **Corollary 1.** The slot band is `82/59 < u < 2686/1559`, with `u < 19/3` redundant. The thresholds are `tau = 195/308`, `141/200` and `4245/5804`. The weak margins are 287/240 and 1/300. The prior endpoints are 0.467850029686 and 0.500424307320, inside the trading window (0.270432, 0.729568). At the example slot `lambda = 0.336121768915`, `b = 0.195615040180`, entry at `r_1` is 0.522756943478 and high-class ownership 0.324401303411. At `r_1`, `B(M) - c_H = 0.21715` and `c_H - B(1/2) = 1.70833`; at `r_2`, `B(M) - c_H = -0.00269`.
- **The pooling strength.** The sale probability is 0.417745925753 = `beta/(1 - beta)`. The purchase posterior exceeds `tau` by 0.070222. The research return at the cap exceeds its marginal cost by 0.021668.
- **The exclusion economy above one third.** All values are listed under O2 above.

The writer's three computations (`O2/o2_exclusion.py`, `O6/o6_shares.py`, `O7/o7_pool.py`) execute with exit status zero, and their output matches the values above.

## Build and language

`A.tex` builds without errors, undefined references or box warnings into the referee's private build folder: six pages, each rendered and read. Exactly the 14 pending names of `A_notes.md` print as unknown. The three proof fragments build in private wrappers to two, one and two pages. Only `r_pool_B`, `pool_mu_B` and `pool_price_B` print as unknown. The language scan of `A.tex` and the three proof fragments counts zero findings; its five matches are the allowed tie-rule phrases. The same scan of this report finds no status, history, defensive, naming or example-naming words. Its remaining matches are file locations, plan codes and the words that describe the recomputation, each required by the referee's task. No build product or cache file is in the repository.
