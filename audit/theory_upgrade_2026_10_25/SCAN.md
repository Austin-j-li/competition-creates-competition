# Theory upgrade of the order-slot manuscript: scan (step 1, read-only)

Date: 25 October 2026. Source state: Overleaf working copy `overleaf/slot/` at commit 69c25f4 (pulled today).
No manuscript file was changed in this step.

## How the scan was done

| Lens | Role | Report |
|---|---|---|
| A3, A4, A5 and Propositions 2 to 4; reduction | scan referee 1 | `scan/reduction_A3_A5.md` |
| Proposition 1, A2, A6, A7, A8 | scan referee 2 | `scan/generality_A1_A2_A6_A8.md` |
| Language and notation | reviewer | `scan/conflation.md` |
| Consumers and numbers pipeline | production reviewer | `scan/downstream.md` |
| Structure, synthesis and spot checks | coordinator | this file |

Coordinator spot checks of the counterexamples: (i) scan referee 1's J counterexample (h = 10, ℓ = 1, p = 1/2, c_H = 2, R ~ U[z − 0.1, z + 0.1]) gives J(7) = 2 and J(7.5) = 1.3 by hand. (ii) scan referee 1's ownership counterexample was recomputed from the model formulas: at r = 11 and r = 12 the research branch holds, entry rises from 0.279883 to 0.282574, and high-class ownership falls from 0.157434 to 0.147305. (iii) scan referee 2's winner-gap counterexample (G_L = δ_1, G_H = δ_2, p = 1/2, F = U[0, r], r > 2) gives W_H − W_L = 1/r, falling in r, by hand.

Scope decision from Austin, applied throughout: the preparation cost stays two-point (zero with probability ρ, c_H otherwise). Nothing below proposes a general cost law or a change to c_H. Proposition A.4 stays the robustness result for other cost laws.

## Headline findings

1. **The reduction lemma holds.** At any incumbent law F with Δ_T(F) > 0 and g_H(F) > g_L(F), the equilibrium set projected onto order laws, posteriors and entry after each order depends on the auction only through (Δ_T(F), τ(F)). With research the same holds for the research intensity, once a and the cap are also fixed. Price levels use t_0 and t_L as well. Ownership (W_H), welfare (g_j, pF(p)) and the value of price access (t_L − t_0) lie outside the reduced outcome. scan referee 1 could not break the claim; the statement it signs is in Part 2. τ ≤ 0 and τ ≥ 1 cause no failure.
2. **Proposition 3 generalizes pointwise without conditions, and to an interval under one stated condition.** No trade and an informative equilibrium coexist at F exactly when J(F) ≥ k, π < τ(F) ≤ M(π) and ρΔ_T(F)max{π, 1 − π} ≤ k, where J = Δ_T(1 − τ). The informative equilibrium is then unique, and its entry is ρ + (1 − ρ)min{(1 − π)bΔ_T/k, b + πλ}, a function of Δ_T alone. Along a stochastically ordered path the set is an interval whenever {J ≥ k} is an up-set. Under rules IM and C1, an equilibrium exists at prior 1/2 at every F with Δ_T > 0, g_H > g_L and τ(F) > 1/2, including τ ≥ 1 (under I0 the set can be empty, as on (r_N, r_S] in the benchmark).
3. **J has no general monotonicity.** scan referee 1 gives a ranked-class, stochastically ordered path on which J falls. The monotone-J condition must be stated, and the benchmark certifies it (Sturm count).
4. **Proposition 4(a) generalizes for research and entry, not for ownership.** λ_R is a smooth, strictly increasing function of Δ_T on Δ_T > 2k, so research and entry on the branch rise with Δ_T. Ownership carries the factor W_H(F), which falls with strength. A research-branch counterexample shows ownership falling while research and entry rise. The rise needs W_H = 1 on the path (the high class outbids every incumbent) or a stated trade-off.
5. **The research branch is not an interval [s_R, s̄_R) under single crossing of φ_a alone.** The branch can end at s_N, where the low class starts to sell, before research reaches the cap. scan referee 1 gives a point-mass, uniform counterexample. The branch ends at the cap exactly when ρ(2aλ̄ + k) ≤ 2k·m_λ̄. The benchmark satisfies this.
6. **Corrections to the preliminary map** (scan referee 2):
   - A.5 is general in the classes and the prior, but its construction uses the uniform incumbent family.
   - A.7 (complementary signals) extends to ranked classes and a continuous stochastically ordered pair; point masses enter only its numerical example.
   - A.9 (payment rule) extends in sign to ranked classes at zero reserve.
   - A.11 and A.12 need prior 1/2 for their tests, not only the reduction. A.11's strict trend also needs A_F(M) = t_L − t_0 + Δ_T·M to rise, which stochastic order does not give.
   - A.13 comes with a counterexample: the winner gap can fall with strength.
7. **Two errors in the current text** (scan referee 1):
   - A2:165–170 says that equal posteriors give equal prices. Under rule CM this fails; the correct claim is that equal posteriors and equal entry give equal prices. scan referee 1 builds an equilibrium counterexample. The A4 and A5 equilibria are unaffected, because their constructions check equal entry.
   - The coexistence figure note (sections/04:302–303) calls T "an equilibrium only when an indifferent high-cost challenger may prepare with any probability". The point r_A, with entry one after a purchase, is a T equilibrium under C1 too.
8. **A2 intro overclaim** (scan referee 2). A2:7–8 says every result holds for every order profile. That is true of the belief lemma only; the price and trading lemmas assume equilibrium conditions.
9. **Stray text from the last Overleaf edit.** Commit 69c25f4 ("Update on Overleaf.", 24 October) put `ty` before `\section{The model}` on line 1 of `sections/02_model.tex`. It prints in the PDF. This is the only difference between `overleaf/slot` and `slot/manuscript`.

## Part 1. Generality table

Two kinds of entry in the column "most general supported statement". Plain entries follow from the current proof text once the benchmark words are removed (the A4 high, low and product lemmas, the A5 per-F lemmas, the set formula of Corollary A.2, A.3, A.4, A.8, A.10). Entries marked **[new]** rest on arguments produced in this scan and need proof text written and checked: the reduction converse, existence at prior 1/2, the up-set interval argument, the sharper Corollary A.2 conditions, λ_R as a function of Δ, the ownership condition, the branch set and the cap-before-selling condition, the general access formulas, A.7 and A.9 extensions, A.11 to A.14 general forms, A.13's formula and condition.

Notation: Δ = Δ_T, γ = g_H − g_L, J = Δ(1 − τ), w_L = t_L − t_0, W_j(F) = E_j[F(θ)1{θ ≥ p}], A_F(μ) = w_L + Δμ. "FOSD path" means a family F_s ordered by first-order stochastic dominance with classes, reserve, costs and slot fixed. Under the class ranking, FOSD makes Δ weakly increasing, each g_j and γ weakly decreasing (Δ + γ is the fixed class-mean gap), and τ and Δτ weakly increasing when c_H ≥ g_L and γ > 0. Strict changes need the strengthening to move mass where D = G_L − G_H > 0.

| Result | Location | Stated hypotheses | What the proof uses beyond its statement | Most general supported statement | Conditions to add |
|---|---|---|---|---|---|
| Proposition 1, returns (`prop:returns`) | sections/03:41; A1:109–161 | Finite-mean classes, continuous F, FOSD; class ranking for (b) | Nothing; the uniform/point-mass block is a separate example | As stated | None. Strictness: the stated positive integrals |
| Proposition 1(c), weakest restriction | A1:163–203 | Finite means; every continuous F and strengthening | Nothing | As stated (D ≥ 0 above p, D(p⁻) ≤ 0) | None |
| Lemma A.1, beliefs (`lem:beliefs`) | A2:39–91 | Any order laws | β ≤ 1/3 only for the zero-order bound (part c) | Auction-free; (a), (b), (d) for β < 1/2 | Keep β ≤ 1/3 for the all-order bound |
| Corollary A.1, exclusion (`cor:exclusion`) | A2:95–106 | g_H ≥ g_L, B_F(M) < c_H, β ≤ 1/3 | Level of B_F(M) | General F, ranked classes | None |
| Lemma A.2, prices (`lem:prices`) | A2:110–163 | Δ > 0, γ > 0, E1–E4, E6 | w_L ≥ 0 (automatic); C1 at μ = τ | General | Fix the "constructed tuples" paragraph (A2:165–170) for CM: equal posteriors and equal entry give equal prices |
| Lemma A.3, trading (`lem:trading`) | A2:173–230 | Δ ≥ 0, E1, E4, E6, e ∈ [ρ, 1] | Nothing | General; β < 1/2 | None |
| Proposition 2 (`prop:ccc`) | sections/04:11–44; A3:11–109 | Ranked classes, continuous F_0 ≤ F_1 ≤ F_2, interior π, slot, H1–H3 | w_L ≥ 0; W_H for ownership (already stated) | Already general; any β < 1/2 | None. scan referee 1: FOSD can be replaced by the two scalar comparisons used (B_1(π) ≤ B_0(π), Δ_2 ≥ Δ_1) |
| Proposition A.1, region (`prop:region`) | A3:157–221 | Benchmark auction, three strengths; prior 1/2 or 1 + u = e | Exact benchmark Δ_i, τ_i; numerical redundancy of some bounds | Calibration only. General three-point region: τ_0 > 1/2, Δ_0 < k, τ_1 < M < min{τ_2, 1 − k/(ρΔ_1)} at prior 1/2 | Keep as the benchmark slice; cite A.5 as the general counterpart |
| Proposition 3 (`prop:coexistence`) and full statement | sections/04:272–283; A4:287–396 | Benchmark auction and path, prior 1/2, slot in the band, IM/C1 | Path lemma (closed forms, Sturm counts), full threshold order | **[new]** (i) Pointwise criterion and entry formula for any ranked classes (see Headline 2). (ii) Interval along any FOSD path when {J ≥ k} is an up-set: C(1/2) = [s_A, min{s_N, s_C}] ∩ {τ > 1/2}. (iii) Existence at every F with Δ > 0, γ > 0, τ > 1/2 (IM, C1 only). (iv) Entry along the coexisting branch weakly rises; strictly while the purchase is mixed and Δ rises strictly | For the full benchmark table: Δ, J, τ continuous and strictly increasing; Δ > 0, γ > 0, τ(s_0) > 1/2; J(s_0) < k; ρ(1 − M)Δ(s_1) > k; τ(s_1) < M < τ(s_2); M < 1 − ρ/2 (this gives s_F < s_N). These imply s_0 < s_A < s_F < s_N < s_J < s_S < s_1 < s_C < s_2 |
| Path lemma (`lem:a4-path`) | A4:20–62 | Benchmark | Closed forms, Sturm counts | (a), (d) weakly for any FOSD path; (b), (c) have no general sign (counterexample for J) | Becomes "the benchmark satisfies the conditions"; keep the certificates |
| Threshold order (`lem:a4-order`) | A4:85–104 | Benchmark, slot band | ρ = 1/4, τ < 3/4, numerical bounds | Follows from the condition set above | Replace numbers by the scalar conditions; keep the benchmark check |
| High-class lemma (`lem:a4-high`) | A4:159–191 | Fixed r, π < τ | τ < 1 for s* | Pointwise general for Δ > 0, γ > 0, π < τ < 1; for τ ≥ 1, drop R/T and define Q by μ₊(s) < τ | State τ < 1 or the τ ≥ 1 case |
| Low-class lemma (`lem:a4-low`) | A4:193–222 | Fixed r, π < τ | Nothing | Pointwise general | None |
| Product lemma (`lem:a4-product`) | A4:224–256 | π < τ, s ≥ t | w_L ≥ 0 | Pointwise general | None |
| Corollary A.2, priors (`prop:priors`) | A4:440–531 | Benchmark path; any prior and slot; IM/C1 | J, τ, Δτ strictly increasing; τ_A < 3/4 = 1 − ρ | The set formula with "r ≥ r_A" replaced by J(F) ≥ k is general and pointwise | Cases (a)–(d): an attained start J(s_A) = k with {J ≥ k} = [s_A, s_2]; level crossings of τ; ρ·max{π_lo, 1 − π_lo} ≤ 1 − τ_A and ρτ_A < 1 − τ_A, where M(π_lo) = τ_A (sharper than τ_A < 1 − ρ); for π_max: τ_A ≥ 1/2 and ρΔ(s_A)τ_A < k < ρΔ(s_2)τ(s_2). Δτ strict is redundant if τ is strict |
| Proposition 4 (`prop:research`) | sections/05:52–70; A5:233–283 | Benchmark auction, prior 1/2, β ≤ 1/3, a > 0 | (a): Δ′(r) > 0 and W_H = 1. (b): certified margins at six strengths | **[new]** (a) λ_R = Λ(Δ), with dΛ/dΔ = m/(2a − Δm′) > 0; entry on the branch rises with Δ for any β < 1/2; along an FOSD path weakly, strictly where Δ rises strictly; C¹ in s if Δ(s) is C¹ | Ownership: ½W_H(F)[ρ + (1 − ρ)(β + (1 − β)λ_R)] rises only under a stated condition (W_H = 1 on the path, or W_H′/W_H > −(1 − ρ)(1 − β)λ_R′/[ρ + (1 − ρ)(β + (1 − β)λ_R)]); counterexample in scan/reduction_A3_A5.md. (b) stays at the benchmark |
| Joint deviations (`lem:a5-joint`) | A5:64–83 | Benchmark, prior 1/2 | Nothing | General auction and prior, with V = π·max U_H + (1 − π)·max U_L | None |
| Research bounds (`lem:a5-bounds`) | A5:85–103 | Benchmark | β ≤ 1/3 for the zero order | General | None |
| Positive research (`lem:a5-buy`) | A5:105–120 | τ > 1/2 | Prior 1/2 symmetry | General at prior 1/2; τ < 1 not needed | None |
| Intermediate strengths (`lem:a5-middle`) | A5:122–201 | 1/2 < τ < 1, ρΔ < 2k, λ_E ≠ λ̄ | Nothing auction-specific | Pointwise general | λ_E = λ̄ and ρΔ = 2k need separate boundary cases |
| Strong incumbents (`lem:a5-strong`) | A5:203–231 | τ > 1/2, M_λ̄ ≠ τ, condition U | Nothing auction-specific | General; β < 1/2 | U is sufficient, not necessary |
| The branch at calibration B | A5:286–314; sections/05:119–126 | Benchmark, a = 1/40 | Closed forms, a bound on φ_a′, r̄_R < r_N | **[new]** Branch set: 1/2 < τ < 1, φ_a = J − k − 2aλ_E(τ) ≥ 0, λ_R < λ̄, ρΔ ≤ 2k. Every branch point has J > k, so s_R > s_A | Interval [s_R, s̄_R) needs φ_a single-crossing and ρ(2aλ̄ + k) ≤ 2k·m_λ̄ (cap reached before low-class selling). Counterexample without the second condition |
| Proposition A.2, cap and cost (`prop:researchregion`) | A5:316–385 | Benchmark, β fixed | Monotonicity bounds collapse the extrema | **[new]** Calibration only. General finite-point form: max_i (Δ_i m_λ̄ − k)/(2λ̄) < a < min_i (J_i − k)/(2λ_{E,i}) | Keep as benchmark |
| Remark, research ties (`rem:researchties`) | A5:388–408 | Benchmark | Numerical T-entry values | T existence is general (middle lemma); decreasing T-entry is not | Keep as benchmark |
| Access to prices with research | A5:410–421 | Benchmark at r_1 | p²/r_1, W | **[new]** Generalizes under τ > 1/2, M_λ̄ > τ and U: ΔR = (1 − ρ)(b̄ + λ̄/2)[w_L + ΔM_λ̄], ΔW = (1 − ρ)(b̄ + λ̄/2)[γ(M_λ̄ − τ) + pF(p)] | Replace p²/r_1 by pF(p) |
| A.3, fixed information (`prop:control`) | A6:8–35 | General signals, cost law, FOSD | B_F levels; C1 for the exact formula | General | None |
| A.4, cost laws (`prop:atomless`) | A6:70–130 | Two cost components, support gaps, windows | B_F schedule; W_H for ownership; β ≤ 1/3 | General F, classes, components with or without atoms | None (kept as the cost-law robustness result) |
| A.5, classes and priors (`prop:classes`) | A6:157–195 | Ranked classes, mean gap, any π and slot; uniform incumbents | Uniform family: Δ → 0 near v_*, g_j → 0, continuity of W_H | General in classes and prior within the uniform family | For another FOSD family: an endpoint with Δ → 0, γ > 0 and W_H > 0, continuity, eventual B_F(M) < c_H, and the ownership inequality. Correction to the preliminary map |
| A.6, many classes (`prop:manyclasses`) | A6:277–346 | Vector separation conditions | Classwise t_j, g_j vectors | General F and classes under separation | Not reducible to (Δ, τ); keep the vector form |
| A.7, complementary signals (`prop:signals`) | A6:383–465 | Point masses, prior 1/2, p < ℓ < r_0 < r_1 < h | Symbolic inequalities in B_F, Δ, D⁺_F; closed forms only in the example | **[new]** Ranked classes and a continuous FOSD pair, prior 1/2, the stated signal structure | Restate the inequalities in B_{F_i}, Δ(F_i), D⁺_{F_0}; ownership π·e_H·W_H(F_1). Correction to the preliminary map |
| A.8, access to prices (`prop:access`) | A7:14–59 | Proposition 2 hypotheses at F_1 | t_j − t_0; B_1(M) + pF_1(p) for surplus | General | None |
| A.9, payment rule (`prop:payment`) | A7:95–142 | Point masses, zero reserve, R < h | E_F[(R − ℓ)₊] | **[new]** Sign result for ranked classes at zero reserve: Δ_ω = ω(E_Hθ − E_Lθ) + (1 − 2ω)E_F Γ(R), Γ(R) = ∫_0^R D | Optional extension; strictness needs E_F Γ(R) to rise strictly. Correction to the preliminary map |
| A.10, reserves (`prop:reserves`) | A7:144–192 | Fixed reserve, class order, windows | Kernel is an example; t_j, g_j, W_j at that reserve | General | None |
| A.11, spread and entry component (`prop:spread`) | A8:3–11, 45–78 | Benchmark, prior 1/2, band, r_S < r < h | Full orders; M − 1/2 = 1/2 − m; Δ(r) and A_r(M) rising; unique ceiling | **[new]** Formulas general at prior 1/2 under full orders and purchase-only recruitment | For trends: strict rise of Δ and, while recruiting, of A_F(M) (FOSD does not give it, since pF(p) can fall); continuity at the ceiling. The test "purchase impact exceeds sale impact iff a purchase recruits" needs prior 1/2: at prior π, I₊ − I₋ = ρΔ{[M − π] − [π − m]} + recruitment term |
| A.12, informed share (`prop:informedshare`) | A8:85–141 | Benchmark, prior 1/2, full trade | Symmetric counts; τ(r_i) | **[new]** Auction-general given the full-order pattern, at prior 1/2 | Keep prior 1/2; away from 1/2, counts identify λ directly (E[X] = λ(2π − 1)), so nonidentification does not carry over |
| Corollary A.3, purchases only (`cor:purchasesonly`) | A8:144–164 | Benchmark, form F or branch R | Benchmark branch locations | **[new]** Count identities general given the order pattern | At prior π: E[X] = π·s₊ and λ = E[X]/π in form F. Branch locations stay benchmark |
| A.13, orders predict the winner (`prop:winner`) | A8:166–193 | Point-mass benchmark | W_H = 1, W_L = ℓ/r, prior 1/2 | **[new]** w_x = μ(x)W_H(F) + (1 − μ(x))W_L(F); w_1 − w_{−1} = (M − m)(W_H − W_L); W_H − W_L = E_F[D(R)] ≥ 0; post-ceiling covariance (b + λ/2)ρϑ(W_H − W_L) | Rise: E_{F_1}[D(R)] > E_{F_0}[D(R)] (sufficient: D nondecreasing where the strengthening moves mass). Strict signs: W_H > W_L. Counterexample: gap 1/r falls |
| A.14, announcement returns (`prop:announcement`) | A8:198–234 | Benchmark, prior 1/2; (iv) full trade | A_r > 0, B_r(1/2) < c_H | **[new]** (i)–(ii) general; (iii) when Σ_x Pr(X = x)e(x)[1 − e(x)]A_F(μ(x)) > 0; (iv) under full orders and purchase-only recruitment, with f̄ = b + πλ | Δ > 0 and B_F(π) < c_H for strict positivity |

## Part 2. The reduction lemma

Statement (scan referee 1; scan referee 2 agrees on the trading stage):

> Fix the independence and information structure, the liquidity law, π ∈ (0, 1), ρ ∈ (0, 1), k > 0, the tie rules, and a slot with 0 < λ < 1 and 0 < β < 1/2. Take two auctions with Δ > 0, g_H > g_L and the same (Δ, τ). Their equilibrium sets, projected onto (σ_H, σ_L, μ, e), coincide. Prices and the price-indexed preparation strategy are recovered in each auction by P(x) = t_0 + e(x)[w_L + Δμ(x)] and ζ(P(x)) = (e(x) − ρ)/(1 − ρ). With research, fix also a > 0 and 0 < λ̄ < 1; the projections onto (λ̂, σ_H, σ_L, μ, e) coincide.

The reduced system is Bayes' rule, threshold entry (e = ρ below τ, 1 above, the tie rule at τ), and the four nonzero-order payoffs U_H(±1), U_L(±1) of Lemma A.3, plus λ̂ = min{λ̄, V/a} with research. The converse construction needs w_L ≥ 0 (automatic: entry cannot lower second-price proceeds) and 0 < μ < 1 (full liquidity support), so w(μ) > 0. Prices agree exactly when (μ, e) agree, and this partition does not depend on the auction levels.

Uses of auction objects other than (Δ, τ):

| Use | Location | Effect |
|---|---|---|
| t_0, t_j in prices | A2:128–143; A3:31–35; A4:273–285 | Price levels only; cancel from incentives |
| g_L, γ, c_H in entry optimality | A2:151–154 | Enter only through τ and the sign of γ |
| w_L ≥ 0 in price ordering | A2:156–170; A3:66–70; A4:244–253; A5:150–170 | Automatic in this auction |
| w(τ) > 0 under CM | A2:122–123, 153–162 | Automatic at a reachable threshold |
| B_i and class integrals across laws | A1:139–158; A3:15–20 | Say how (Δ, τ) move along a path; a path condition, not a break |
| Closed forms and constants | A3:183–219; A4:15–62; A5:291–300 | Benchmark path properties |
| W_H(F) | A3:75–86; A5:280–282; A6 (A.4, A.5, A.7); A8 (A.13) | Ownership and winners lie outside the reduced outcome |
| t_L − t_0 | A5:410–417; A7 (A.8); A8 (A.11, A.14) | Price-gap and proceeds magnitudes |
| g_j, c_H, pF(p) | A5:418–421; A7 (A.8) | Welfare magnitudes |
| Vector t_j, g_j | A6 (A.6) | Many classes: no scalar reduction |
| Class-specific entry e_H, e_L, D⁺_F | A6 (A.7) | Complementary signals: entry depends on the class through the signal, so the scalar reduction does not apply |
| a, λ̄ | A5:7–20 | Non-auction primitives; must be fixed |

Conclusion: the reduction is the right organizing device for Propositions 2 to 4, Corollary A.2, A.11, A.12 and A.14. Ownership statements carry W_H(F), welfare and price-gap statements carry levels, and A.6 and A.7 sit outside it.


## Part 3. Conflation list

From the reviewer scan, with Austin's cost decision applied: no item about c_H remains. The one cost-related item left (A6:73, the A.4 cost-law symbols reusing the letters H and L) is a symbol rename only and is optional. Each item reads: file:line, quoted text, category (1 atoms vs distributions; 2 slot vs Laplace; 3 benchmark as general; 4 symbol with two meanings; 5 inconsistent naming), proposed fix. Negative result: b has one meaning throughout, (1 − λ)β; the only Laplace words outside the permitted footnote are at 08:79 and A4:409. Coordinator additions: A2:7–8 overclaims scope (scan referee 2); A2:165–170 equal-posterior shortcut fails under CM (scan referee 1); sections/04:302–303 figure note omits the C1 point r_A of T (scan referee 1).

### main.tex
- 92–93 "a challenger from the high-value class acquires" [1/5]. Use "a class-H challenger acquires".
- 93–95 "informative and uninformative equilibria coexist … rises and then stays constant" [3]. `prop:coexistence` assumes the benchmark auction at prior 1/2. Use "In the benchmark auction, …".
- 95–96 "research and entry rise together over a range of strengths" [3]. `prop:research` has the same benchmark restriction. Add the qualifier.
- 54 and 57, the macro comments "(entry is e(x))" and "root of Delta_T(r) = d" [4]. These are the three E's (`\mathbb E`, `\mathsf E`, `e(x)`) and `d` (also the signal accuracy). See patterns 2 and 5.

### sections/01_introduction.tex
- 9, 41 "challenger from the high-value class" [1/5]. Use "class-H challenger".
- 13–14 "Incumbent strength is the public distribution" [5]. Elsewhere strength is the scalar `r` (04:79). Use "the incumbent's value law F; for the uniform family, its strength r".
- 19 "from a high-value or a low-value quality class" [1/5]. Use "from one of two quality classes, H and L, with ranked value distributions".
- 54 "the entry ceiling, the strength r_C" [5]. Pattern 4.
- 61 "Informative and uninformative equilibria coexist on an interval of strengths" [3]. Use "Along the benchmark path, …".
- 70–75 "The unique outcome has no research … at the cap", "for every liquidity probability" [3]. Use "In the benchmark auction at prior 1/2, …".
- 81–82 "the buyer and the investor", "the buyer's signal" [5]. Use "challenger".
- 87–89 "the effect of competition on the target-payoff spread depends on the weight" [3]. `prop:payment` covers point-mass classes with zero reserve only. Add "With point-mass classes, …".
- 89 "A reserve that excludes the low-value class" [1]. Use "A reserve above every low-class value".
- 93–96 "the entry component of the spread between purchase and sale prices … of the spread" [4/5]. Use "purchase–sale price gap" and keep "spread" for Δ_T.
- 108–109 "learns about its own acquisition value from the target's price" [1]. Use "learns about its class, and so about the distribution of its value".

### sections/02_model.tex
- 30 "Public incumbent strength is a distribution" [5]. Same issue as 01:13.
- 52–53 "F on [0,\bar r]" [4]. Collides with `\bar r_R` (05:119).
- 54–55 "In the main case R is uniform on [0,r]" [3]. Use "In the benchmark, R is uniform on [0,r]".
- 62 "The high class, or high-value class," [1/5]. Delete "or high-value class".
- 69–73 "the spread rises under every strengthening" [4]. Used before its definition at 02:199. Define `t_j` and Δ_T earlier, or forward-reference.
- 123–124 "the ceiling of Section~\ref{sec:inference}" [5]. Use "the posterior bound".
- 162–163 footnote, "\eu … printed upright to separate it from entry e(x)" [2/4]. The footnote itself is permitted. The upright e is needed only because the benchmark sets 1+u=e (pattern 2). The footnote's `s` also collides with the purchase rate `s` in A4.
- 191 "e(q) is entry after the order q" [4]. Entry appears as `e(x)`, `\Ent`, `e_H` and `\Ent_F`, alongside `\E` and `\eu`.
- 203–204 "g_j(F), \DT(F), B_F; … g_j(r), \DT(r), B_r" [4]. The argument switches between a law and a scalar, and `F_r` (A5), `\Ent_F` (A4) and `B_i` (A3) then read as instances.
- 228 "W_H(F)" [4]. Near-collision with `w_H` (A2:23), `w_x` (A8:167) and `\mathcal W` (A7:10).

### sections/03_competition_information.tex
- 80–82 "approaches zero as r approaches ℓ … low-value challenger. As r increases" [1/3]. Use "In the benchmark, … a class-L challenger (value ℓ). As the incumbent strengthens, …".
- 94 "This gives the ceiling of the model" [5]. Use "the posterior bound on preparation".

### sections/04_equilibrium_results.tex
- 52 "The ceiling (H3)" [5]. Use "the exclusion condition (H3)".
- 83, 124 "1+u=\eu" [2/4]. Pattern 2.
- 121, 131 "the admissible region at the benchmark auction" [4/5]. "Admissible" already means a bid that meets the reserve (02:101). Use "hypothesis region".
- 158–160 "a high-class challenger outbids every incumbent on the path … r/2+p^2/(2r)" [1/3]. Use "in the benchmark h exceeds every strength on the path, so a class-H challenger always wins and pays r/2+p^2/(2r)".
- 194 "gross profit at the two strengths" [5]. This is the general `prop:control`. Use "at the two incumbent laws".
- 220, plus A6:50 and 53: "Full orders held fixed", "frozen profile", "fixed-information control" [5]. Pick one name.
- 267 "the sale threshold r_S" [5]. "Threshold" names τ, the strengths r_A to r_C (A4:116) and the pair T. Keep it for τ and say "marked strengths" for the r's.
- 301–302 figure labels N, R, F, Q, T [4]. R, F and T collide with R, F and Δ_T/the signal T, and A5 reuses R and T for different tuples.

### sections/05_research.tex
- 1, 52 Section and proposition title "Competition creates research" [3]. The hypothesis is the benchmark auction at prior 1/2. Title the proposition "… at the benchmark auction".
- 5 "cost (a/2)λ^2, where a>0" [4]. Collides with the accuracy `a_T` (06:61).
- 32, 42 "λ_E(r)", "λ_R(r)" [4]. The subscripts read as `\Ent` and the incumbent value R.
- 119 "[r_R,\bar r_R)" [4]. Collides with `\bar r`. Use `r_R^{cap}`.
- 154 "admissible region of the research parameters" [4/5]. Use "parameter region".
- 158 "With 1+u=\eu" [2]. Pattern 2.

### sections/06_robustness.tex
- 42 "a mean-preserving spread within a class" [4/5]. A third sense of "spread". Use "a mean-preserving increase in risk".
- 61 "accuracy a_T … accuracy d" [4]. `a` is the research cost, T the target subscript, `d` the argument of `\fr`. Use `α_I` and `α_C` (α is unused).
- 79 "a buyer signal" [5]. Use "the challenger's signal".

### sections/07_welfare.tex
- 30 "recruitment region" [5]. A third name for the H1–H3 set, after "admissible region" and "band".
- 32 "with the strong benchmark" (also A7:90) [5]. Use "in the benchmark at r_1".
- 42–45 "The effect of competition on the target-payoff spread depends on the sale payment" [3]. Use "With point-mass classes and zero reserve, …".
- 52–53 "A high-class challenger wins and pays (1−ω)R+ωh" [1]. Use "A class-H challenger, whose value h exceeds the incumbent's support, …".
- 70–71 "A reserve that excludes the low class … adds nothing" [1/3]. Use "A reserve above every low-class value (in the benchmark, p>ℓ)".

### sections/08_empirical.tex
- 19, 22, 28–30, 40 "The price spread" against "target-payoff spread" at 42 [4/5]. Use "price gap".
- 49–50 "A prepared high-class challenger always outbids the incumbent" [1/3]. Use "In the benchmark, where h exceeds every strength, a prepared class-H challenger always wins".
- 79 "such as flow from sector specialists" [2]. Use "orders from sector specialists".

### sections/09_conclusion.tex
- 10–13 the coexistence and entry-path sentence [3]. Use "Along the benchmark path, …".
- 14–15 "research and entry rise together" [3]. Add "in the benchmark auction".
- 19–21 the payment-rule claim and "A reserve that excludes the low class" [3/1]. Add "with point-mass classes" and "above every low-class value".

### appendix/A1_payoffs.tex
- 13 "\mathcal{E}=(σ_H,…)" [4]. A fourth E. Use Σ (unused).
- 22 "\bar P in the image of P" [4]. A8:229 uses `\bar P` for the expected price.
- 27 "f_j(x)=(1-λ)η(x)+λσ_j(x)" [4]. Reads as the density of F. Use `ψ_j(x)`.
- 59 "Y≥0 the highest competing admissible bid" [4]. `Y` is also the signal (A6:385) and an indicator (A8:188).
- 77–78 "the high-value challenger always wins", "The low-value challenger" [1/5]. Use "the class-H challenger (value h)" and "the class-L challenger (value ℓ)".
- 178, and A7:147 "kernel ξ" against "kernel (t_v,g_v,W_v)" [5]. Two objects share the name.
- 213–214 "g_j=∫_p^θ F at θ=h and θ=ℓ" [1]. Write `g_H=∫_p^h F` and `g_L=∫_p^ℓ F`.

### appendix/A2_beliefs_trading.tex
- 23–24 "w_j=t_j−t_0 … w(μ)" [4]. Collides with `W_H`, `w_x` (A8), the weights `w_j` and `w` (A6) and `\mathcal W`. Keep `w` here and rename the others.

### appendix/A3_proposition2.tex
- 4, 157 "the admissible region" [4/5].
- 79 "e_H, e_L" class entry [4/5]. A6 writes `\bar e_H` and `e_H(μ)`. Use `\Ent_j`.
- 124, 134–135, 155, 226, 231 "calibration B" [4/5]. Pattern 1.
- 142 "every quantity that depends on \eu" [2]. Pattern 2.
- 226 "trade bound" against "trading bound" [5].

### appendix/A4_coexistence.tex
- 17 "\fr(d) … root of \DT(r)=d" [4]. Use `\fr(Δ)`.
- 32 "D_τ" [4]. Collides with `D(y)`.
- 107, 116, 120, 399–400, 414 "calibration B", "Value at B" [4/5].
- 135 "s=s_+=λσ_H(1) and t=s_-=λσ_L(−1)" [4]. `t` is proceeds (`t_0` at 231 in the same lemma). Use `s_+` and `s_-` only.
- 204 "s_-^*(r)" against "s^*" (152) [4/5]. The star has two meanings. Use `\hat s_-(r)`.
- 166 "e^*:=k/J(r)" [4]. A5:57 redefines it. Write `e^*_a`.
- 305 "\Ent_R, \Ent_F, \Ent_T" [4]. The subscript F means the law in `B_F`. Use `\Ent^{\rm F}`.
- 409 "from the flow law" [2]. Use "the order law".
- 441 "C(π)" [4]. Collides with the cost variable `C` and the rules C1/CM. Use `\mathcal C(π)`.
- 551, 595 "no admissible (sale) rate" [4/5]. Use "no qualifying rate".

### appendix/A5_research.tex
- 4, 316 "the admissible cap and cost" [4/5].
- 18 "research value V" [4]. Collides with `V_T`. Use Ψ.
- 40, 61, 255, 286, 317, 339 "calibration B" [4]. 61 and 317 sit next to `B_r`.
- 47–54, 267–276, 346, 364 "F_r(λ)", "F_{1.65}(\lb)" [4]. These read as the uniform law. Use `Λ_r(λ)`.
- 57 "φ_a(r)" [4]. Collides with `φ_±(μ)` (A6:392).
- 127–135 forms (Z), (R), (\bar R), (T) [4]. R and T mean different tuples in A4.
- 373 "λ_B(β)" [4]. Use `λ_\star(β)`.
- 419 "allocation value" against "acquisition surplus" [5].

### appendix/A6_robustness.tex
- 31 "A tie probability q" [4]. `q` is the order. Use `\bar ζ`.
- 73 "H_C=ρH^0+(1−ρ)H^1, supp H^0⊂[0,L]" [4]. The symbols in Proposition A.4 reuse the class letters H and L. Rename the letters only and leave the result unchanged; for example `Φ, Φ^0, Φ^1` and bound `c_0`. The same applies to A9:30 "Cost law L".
- 128 "\bar e_H" [5]. See A3:79.
- 237, 360, 467, 491, 506–507, 521–522 "slot of B", "S(B)", "The benchmark B", "At B" [4/5]. Pattern 1.
- 245 "t_v, g_v, W_v for a point value v" [1]. Use `t(v)`, `g(v)`, `W(v)` (02:196).
- 254, A7:158 and 163 "class order" [5]. Use "class ranking".
- 279 "classes j=1,…,J" [4]. Collides with `J(r)` and `r_J`. Use `n`.
- 285 "\mathcal L low group" [4]. A6:11 uses `\mathcal L_i` for a law.
- 332, 371, 507 "z" as group posterior, conditional means and 2a_T−1 [4]. `z` also has meanings at 07:27, A5:65 and A7:119.
- 352, 362 "weights w_j", "w=(1+2b_0+λ)/2" [4]. Use `υ_j` and `υ`.
- 361–364 "t_0=7/8, (t_1,t_2,t_3)" [4]. Index the classes a, b, c.
- 385–389 "T∈{+,−} with accuracy a_T … Y" [4]. Use `S_I`, `S_C` and `α_I`, `α_C`.
- 391 "μ_-=…, μ_+=…" are numbers here but functions in A4:142 [4].
- 393 "D^+(r)" [4]. Collides with `D(y)`.
- 397 "f_t(x) … given T=t" [4].
- 519 "satisfy the theorem" [5]. Use "the proposition".
- 524 "t=λσ_-(−1)" [4]. Same as A4:135.

### appendix/A7_welfare.tex
- 10–11 superscripts 1/0 for access/hidden [4]. Subscripts 0/1 mean weak/strong elsewhere. Use `^{\rm acc}` and `^{\rm hid}`.
- 47 "\mathcal V_0(R)" [4]. Collides with `V_T` and `V`.
- 69 "G=λΔ_1{…}" [4]. Collides with `G_j`. Use `Π_I`.
- 103 "Let the challenger's values be the point masses ℓ and h" [1]. Use "Let the classes be point masses at h and ℓ".
- 107–108 "T_ω(R,θ)", "g_{θ,ω}" [1/4]. Write `g_{j,ω}`.
- 119–120 "(P−z)^ω(V−P)" [4]. `P` is the stock price. Write `(T−y)^ω(v−T)^{1−ω}`.
- 146–157 "(t_v,g_v,W_v)" [1]. Same fix as A6:245.
- 196 "T=…, C=c_H−B(1/2) and J=B(M)−c_H" [4]. The margin names collide with the signal T, the cost variable C and `J(r)`. Name them in words.
- 222 "p_H" [4, minor].

### appendix/A8_empirical.tex
- 5 "A_r(μ) … is the function w(μ)" [4/5]. One object has two names, and `A` is also the event at 166. Use `w_r(μ)`.
- 8 "\vartheta=u/(2+u)", "v=Pr(X≠0)", "\bar f" [4]. Use `ι` for the informed share.
- 15 "D_S=k/(ρm)" [4].
- 21 "The tuple \mathcal F" [4]. Collides with the law F and the form F. Use `\Sigma_{\rm full}`.
- 41, 45, 80, 82 "The spread S=P(1)−P(−1)" and the proposition title "The spread and its entry component" [4/5]. Section 8 says "price spread", and `S` is the signal. Use "price gap".
- 98 "and the spread \DT(r)" [4/5]. The second sense of "spread" in the same subsection. Use "target-payoff spread".
- 42 "I_+, I_-" [4, minor]. Collides with `I_y` (A6) and the rules IM/I0.
- 166–167 "w_x=Pr(W|X=x,A)" [4]. `w_1` against `w_1(μ)` in A3:61. Use `ϖ_x`.
- 229 "\bar P=∑_x …" [4]. Collides with A1:22.
- 243 "v_U=2b+λ/2" [5]. A second name for `v`.

### appendix/A9_parameters.tex
- 4, 10, 94, 96, 169 "calibration B", "Value at B" [4/5].
- 23 "u=\eu−1" [2]. Pattern 2.
- 30 "Cost law L; ε" [4]. The letter only; see A6:73.
- 32 "Four-class values θ_1,…,θ_4" [1]. Use `v_1..v_4`.
- 49–58, 192–199 "The vector S(B)" and the "S(B): …; B: …" cells beside `B_{r_0}(d)` [4]. Call it "the signal example".
- 201, 231, 244 "T, C, J", "C_0, C_1, T_0, T_H, T_L, C_2, O" [4]. Use word-labelled columns.

### Systematic patterns
1. **"Calibration B", "B", "S(B)", "λ_B" against gross profit B(μ)** (about 35 items in A3–A6 and A9). Use "the benchmark" and "the signal example". The registry keys don't print and stay as they are.
2. **1+u=e is the Laplace s=2 inheritance.** It is the only reason the main text needs Euler's e set apart from `e(x)`. The author decides whether to say so once in the benchmark declaration or to choose a rational u.
3. **Class letters H and L on non-class objects.** These are the Proposition A.4 cost-law symbols `H_C, H^0, H^1, L`, the margins `T_H`/`T_L`, and `p_H`. This is a symbol rename only.
4. **One word, several meanings.** "Spread" should mean Δ_T only; the others become "price gap" and "increase in risk". "Admissible" should mean a bid that meets the reserve only; the others become "parameter region" and "qualifying rate". "Ceiling" should mean `r_C` only; the others become "posterior bound" and "exclusion condition". "High-value class" becomes "class H".
5. **Letter collisions across sections.** `t`/`s` as rates, `F_r(λ)`, `w`/`W`/`w_x`/`\mathcal W`, `V` against `V_T`, T/C/J as margins, `A_r=w`, `G`, `\bar P`, `\mathcal E`/`\mathcal F`, R/T/F form labels, `e^*` and `μ_±` each defined twice, and `z`, `v`, `d`, `a`, `Y`, `D_*`. Unused letters available: ψ, Ψ, ι, Φ, Λ, Σ, α, υ, ϖ, `\mathcal C`.
6. **Benchmark-only results stated generally.** `prop:coexistence`, `prop:region`, `prop:research`, `prop:researchregion`, `prop:payment`, `prop:priors`, all of A8 and the reserves table carry benchmark or point-mass hypotheses. The general results are returns, ccc, control, atomless, classes, manyclasses, access and reserves. The abstract, intro, conclusion, 02:54, 03:80, 07:42/70, 08:49 and the Section 5 title need qualifiers.
7. **Value used as a class index.** `t_v`, `g_v`, `W_v`, `g_{θ,ω}`, `θ_1..θ_4`, and `g_j` "at θ=h". Use `t(v)` and the subscript j.
8. **Synonyms for one object.** Entry given class (`e_H`, `\bar e_H`, `e_H(μ)`); `w` against `A_r`; held-fixed, frozen and control; "class order" against "class ranking"; "strength" for both F and r; "buyer" against "challenger".

### Notation table
| Symbol | Meaning | First defined | Uses to retire |
|---|---|---|---|
| j∈{H,L} | challenger class | 02:57 | "high-value class"; H/L letters in the Proposition A.4 cost law and the A9 margins |
| π | prior Pr(j=H) | 02:57 | — |
| G_j | value law of class j | 02:58 | G as investor profit (A7:69) |
| θ | value drawn from G_j | 02:58 | θ_1..θ_4 (A9:32), g_{θ,ω} (A7:108) |
| D(y) | G_L−G_H | 02:60 | D_τ, D^+, D_S |
| p | reserve | 02:59 | P as a bargaining payment (A7:120), p_H |
| F, \bar r | incumbent law, support bound | 02:52 | F_r(λ), \mathcal F, form F, \bar r_R |
| r | uniform benchmark strength | 02:55 | "strength" = F (01:13, 02:30) |
| R | incumbent value | 02:52 | form label R (A4/A5) |
| h, ℓ | benchmark point masses | 02:78 | "high/low-value challenger" |
| C, ρ, c_H | preparation cost (kept as is) | 02:91 | C(π) (A4:441) and margin C (A7:196) only; c_H itself unchanged |
| λ, β | presence, liquidity probability | 02:119 | λ_B |
| b, b_0, u | liquidity masses, λ/b | 02:142, A2:32 | — (single meaning) |
| M(π), m(π) | top and bottom posterior | 02:146 | μ_± as numbers (A6:391) |
| q, x, X | own order, generic order, observed order | 02:120, 130 | q as tie probability (A6:31) |
| k, κ(π) | trading cost, trading-bound fraction | 02:120, 03:121 | — |
| μ, P, \bar μ | posterior, price, belief at a price | 02:181 | \bar P as expected price |
| e(x), \Ent, \Ent_j | entry by order, total entry, entry by class | 02:191, 225, A3:79 | \bar e_H, e_H(μ), e_r, \Ent_F |
| \eu | Euler's number | 02:163 | tied to 1+u=e |
| t(θ), g(θ), t_0 | proceeds and profit at a value; no entry | 02:196, 107 | t_v/g_v/W_v; t as a rate or signal |
| t_j, g_j | class expectations | 02:199 | (t_1,t_2,t_3) next to t_0 |
| Δ_T | target-payoff spread | 02:199 | "price spread", "the spread S" |
| w_j, w(μ) | entry gain | A2:23 | A_r, w_x, weights w |
| B(μ), B_F, B_r | gross profit | 02:202 | "calibration B", S(B), λ_B |
| τ | preparation threshold | 03:99 | "threshold" for r_A..r_S |
| K_j | gross return of a correct order | 03:119 | — |
| W_H(F) | class-H win probability | 02:228 | \mathcal W, w_x |
| \Own_H | high-class ownership | 02:225 | margin O |
| r_A…r_C | marked benchmark strengths | 04:262 | "ceiling" other than r_C |
| a, \bar λ | research cost, cap | 05:4 | a_T → α_I |
| λ_E, λ_R | recruitment intensity, research choice | 05:32, 42 | F_r → Λ_r, V → Ψ |
| Σ (now \mathcal E) | equilibrium tuple | A1:13 | collides with \E, \Ent |
| ψ_j (now f_j) | order probability by class | A1:27 | reads as the density of F |
## Part 4. Proposed unified structure

One model, stated once in Section 2: class j indexes G_j (class ranking), the price moves beliefs about the class, preparation reveals θ ~ G_j, the incumbent law F varies along a stochastically ordered family, and trading is the order slot (Dow and Gorton 1997 modified). The benchmark (h = 10, ℓ = 1, R ~ U[0, r]) is declared once, as the worked example, and every later use says "in the benchmark".

### Main text (plain prose, few labels)

| Section | Content after the upgrade |
|---|---|
| 2 The model | As now. Define t_j and Δ_T before their first use (02:69–73 uses the spread before 02:199). "In the main case R is uniform" becomes "In the benchmark". Remove "or high-value class". |
| 3 Competition and information | Proposition 1 (general). New paragraph, the reduction in words: the trading stage sees the auction through two numbers, the spread and the preparation threshold, and a stronger incumbent raises both. Point to the appendix lemma. Move the benchmark closed forms (eq. payoffs) to 4.2, or label them as the benchmark. |
| 4.1 Competition creates competition | Proposition 2, unchanged (already general). |
| 4.2 The benchmark | Closed forms, Table 1, the region (A.1), the fixed-information control. Labelled as the worked example. |
| 4.3 Coexistence | Proposition 3, general: (a) pointwise criterion and uniqueness, with entry a nondecreasing function of the spread; (b) along a stochastically ordered path the coexistence set is an interval when J crosses k once from below; (c) existence at prior 1/2. Then one paragraph: the benchmark satisfies the condition, the marked strengths, the figure. Corollary A.2 is cited in prose. |
| 5 Competition creates research | Proposition 4: (a) general: research and entry rise with the spread wherever the branch exists; ownership rises when the high class outbids every incumbent (or under the stated trade-off). (b) the benchmark. The branch interval is stated with its two conditions. |
| 6 Robustness | A.3, A.4, A.5 (note: uniform family), A.6, A.7 (restated for ranked classes). |
| 7 Welfare and sale terms | A.8 general; A.9 sign result for ranked classes at zero reserve (optional); A.10 general. |
| 8 Empirical implications | A.11 to A.14 stated for general F under the full-order pattern, with the prior-1/2 and monotonicity conditions named; A.13 with W_H − W_L. Benchmark numbers as illustration. |
| 1, 9, abstract | Qualify the coexistence and research claims ("along a path on which…", "in the benchmark") and use class H/L wording. |

### Appendix

| Part | Content |
|---|---|
| A1 Payoffs | Proposition 1 and 1(c). New lemma, "The two numbers along a path": Δ ↑, g_j ↓, γ ↓, τ ↑, Δτ ↑ under FOSD; strictness conditions; remark that J has no general sign, with scan referee 1's counterexample. |
| A2 Beliefs and trading | Lemmas A.1 to A.3. New lemma: the reduction (statement of Part 2). Fix the constructed-tuple paragraph for CM. Narrow the opening claim to the belief lemma. |
| A3 Proposition 2 | As now; A.1 kept as the benchmark slice. |
| A4 Coexistence | General part first: high/low/product lemmas at a fixed F; the pointwise criterion; existence at prior 1/2; the path interval; Corollary A.2 with its conditions. Then "The benchmark path": the path lemma recast as "the benchmark satisfies the conditions" (Sturm counts kept), the threshold order, the full equilibrium table, tie-rule table. |
| A5 Research | General part first: the research lemmas at a fixed F; Proposition 4(a) with the ownership condition; the branch set and the two interval conditions. Then the benchmark: 4(b), A.2, the remark, access to prices with research (pF(p) in place of p²/r). |
| A6 to A8 | Restatements listed in Part 1. |
| A9 Parameters | Add the margins of the new conditions at the benchmark (Part 5). |

Numbering: a new lemma in A1 or A2 shifts every later "Lemma A.n". `comparison.tex`, `slides.tex`, the study guide, the website and the web slides hard-code these numbers.

## Part 5. Downstream consumers (summary; details in scan/downstream.md)

- **comparison.tex.**
  - Rows 205 (coexistence), 206 (other priors), 207 (research) and 215 (empirical) of `tab:results` need new scope wording.
  - The prose at 219–234, 253, 266–305 and 351–358 needs the same.
  - Margins section 436–446 and 654–675.
  - Decision points 1, 2 and 7.
  - Renumbering at 66–67, 133–144 and 200–201.
  - Result-status labels appear only in this file. The general statements would be analytical; the benchmark instances keep "computer-assisted".
  - "High class" at 90, 116, 150 and 382 in slot text should become "class H"/"class L".
- **slides.tex.** Frames F12 (456–468), F13 (476, 484: "Proposition 4(a)" there cites benchmark content), F16 (545–550: the winner bullet needs W_H > W_L), notation A2 (602–640), A8 (747–763), A9 (776). "High class" at 465, 753 and 829.
- **Registry.** The affected statements read P1_core.csv (Proposition 3, Corollary A.2), P3_research.csv (Proposition 4, A.2), P5_observables.csv (A.11–A.14) and own_* (P1_core) and margin_p4_ownership_rise_B (P4_information.csv).
  - J monotonicity and the Δ(1 − τ)², Δτ signs are certified only in logs (p1_certificates.log), with no registry key.
  - Candidate new keys:
    - `margin_tauA_half_B`: 7/8 − τ_A.
    - `margin_M_78_B`: 7/8 − M, which gives s_F < s_N.
    - A Sturm-count key for J.
    - `margin_WH_B`: h − r_2.
    - `WL_r1_B` and `WL_r2_B`.
    - The cap-before-selling margin: 2k·m_λ̄ − ρ(2aλ̄ + k).
  - Each new key needs a checker row (XP1, XP3, XP5).
  - make_numbers.py globs every registry CSV, so a new CSV file merges without code change.
- **Pipeline direction.** make_numbers.py:14, number_scan.py:9 and make_figures.py:36 write to `slot/manuscript/`, not to the Overleaf master. make_figures.py:38 hard-codes a Linux font path.
- **Figures.** coexistence.pdf, research.pdf and beliefs.pdf stay valid as the worked example; only captions change.
- **Out of scope but restating the benchmark scope:** slot/study_guide/, handout/, presentation/content.js, discussion notes.

## Part 6. Change list, ordered by dependency

1. **Decisions for Austin** (below). Everything after depends on them.
2. **Housekeeping.** Remove the stray `ty` (02_model.tex:1). Sync `slot/manuscript/` to the Overleaf master. Decide whether the numbers and figure scripts write to the master or to the mirror.
3. **Notation and vocabulary conventions** (Part 3 patterns), fixed once before any proof is rewritten: "calibration B" → "the benchmark"; "spread" only for Δ_T; "admissible" only for bids; "ceiling" only for r_C; class H/L wording; renames such as F_r(λ) → Λ_r(λ), the research value V → Ψ, C(π) → 𝒞(π), s/t rates → s₊/s₋; the A.4 cost-law letters (optional).
4. **A1:** path lemma for (Δ, γ, τ, Δτ) with the J remark.
5. **A2:** reduction lemma; constructed-tuple fix; opening sentence.
6. **A4:** general coexistence (pointwise criterion, existence, interval, Corollary A.2 with conditions), then the benchmark path. Fix the figure-note T/C1 exception.
7. **A5:** general research part (Proposition 4(a) with the ownership condition; branch set and interval conditions), then the benchmark.
8. **A6–A8:** A.5 scope sentence; A.7 restated for ranked classes; A.9 extension (if wanted); A.11–A.14 with the named conditions and A.13's new formula.
9. **Main text:** Sections 2–5 first (statements must match the appendix), then 6–8, then introduction, conclusion and abstract.
10. **A9 and the registry:** new margin keys and checker rows; regenerate numbers.tex; number_scan (0 missing, no typed decimals); orphan check.
11. **Build and read:** latexmk main.tex; read every changed page; verify-ccc for the affected exercises.
12. **Consumers:** comparison.tex, then slides.tex (and W2_keys.md), then presentation/content.js; study guide and website only if Austin wants them.
13. **Sync and commit** on a local branch in both repositories; no push.

## Decisions for Austin

1. **Stray `ty`** in `sections/02_model.tex:1` from the last Overleaf edit: remove it? (Recommended: yes.)
2. **Where the reduction lives**: prose in Section 3 and a formal lemma in A2 (recommended), or a labelled lemma in the main text.
3. **Ownership in Proposition 4(a)**: state the rise under "the high class outbids every incumbent on the path" (W_H = 1; simple, the benchmark satisfies it), or under the general trade-off inequality.
4. **Scope of the optional extensions**: A.5 to general FOSD families, A.7 and A.9 to ranked classes. The proofs support A.7 and A.9 directly; A.5 needs new conditions.
5. **1 + u = e**: Euler's number enters only through this benchmark choice, which matches the Laplace comparison. Keep and say so once, or pick a rational u (changes registry numbers).
6. **Consumers in scope**: comparison.tex and slides.tex (planned); study guide, website and web slides (not planned).
