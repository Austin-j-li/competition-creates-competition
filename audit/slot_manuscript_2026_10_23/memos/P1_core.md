# P1_core: beliefs, informed trading and the main comparisons (R2, R3, R4)

Proof package: `proofs/P1_core.tex` (PDF `proofs/build/P1_core.pdf`, 24 pages). Scripts and run logs:
`scripts/P1_core/`. Registry: `registry/P1_core.csv` (147 rows). Values are at calibration B and prior 1/2 unless
stated. Decimals at B depend on e; they are registry values with status computer-assisted (outward intervals).
Round 2 (23 October 2026) applies the check `memos/XP1_check.md`; the last section lists each change.
The round-1 files are in `scripts/P1_core/round1/`.

Notation (LABELS §1): `f_j(x) = (1 − λ)η(x) + λσ_j(x)` is the probability of order x in class j. The number
`u = λ/b` is the informed presence mass relative to the liquidity mass in one direction; `1 + u` is the largest
likelihood ratio of an order. The low-class sale rate is `t̄(r)` (round 1 wrote `t_L(r)`, which clashed with the
proceeds `t_L`).

## Results

| Label | Result | Status |
|---|---|---|
| Lemma 1 | Every order has positive mass in each class. At ±1 the odds move by at most 1 + u under every strategy (any β < 1/2). At 0 the factor is 1 + λ/b_0 ≤ 1 + u iff β ≤ 1/3; for β > 1/3 a strategy pair breaks the bound. | analytical |
| Lemma 2 | Floor e ≥ ρ; the price reveals the posterior and rises strictly with it. New part (f): the same price algebra for a constructed tuple, with no equilibrium premise. | analytical |
| Lemma 3 | Premises: Δ ≥ 0, Bayes posteriors (E1), competitive prices (E4), entry in [ρ, 1]. Wrong-sign orders lose at least k; each class compares one gross return with k; ρκΔ ≤ K_j ≤ Δ under every candidate. | analytical |
| Corollary 1 | With β ≤ 1/3, B(M(π)) < c_H excludes high-cost preparation under every profile with Bayes beliefs and optimal preparation (the only use of β ≤ 1/3). | analytical |
| Prop. 2 | Under (H1) B_0(π) < c_H < B_1(M), (H2) Δ_0 < k < ρκΔ_1, (H3) B_2(M) < c_H: unique outcomes, the same under all four tie-rule pairs: no trade (entry ρ); full two-sided trade (entry ρ + (1 − ρ)(b + πλ)); full trade with entry ρ and an informative price. Ownership rises iff [ρ + (1 − ρ)(b + λ)]W_H(F_1) > ρW_H(F_0). | analytical |
| Lemmas 4–5 | J = Δ(1 − τ) and Δ(1 − τ)² increase on the path (exact Sturm counts); r_0 < r_A < r_F < r_N < r_J < r_S < r_1 < r_C < r_2 on the whole band. | computer-assisted |
| Prop. 3 | Complete equilibrium set on [1.2, 3.6] at prior 1/2, for every slot in the band (table below). | computer-assisted |
| Prop. 4 | (H1)–(H3) hold at the benchmark iff 82/59 < u < 2686/1559, that is 82β/(59 + 82β) < λ < 2686β/(1559 + 2686β). Prior range at B: (141/(141 + 59e), 4245/(4245 + 1559e)) ≈ (0.467850, 0.500424); parts (i)–(ii) alone: (141/(141 + 59e), 195/308). | analytical |
| Prop. 5 | Coexistence set C(π) at every prior under IM and C1 (below). | computer-assisted |
| Remark 1 | Coexistence under (IM, CM), (I0, C1) and (I0, CM) at every prior, including the CM endpoint at π = π_max. | analytical; values at B computer-assisted |
| Cross-check | `p1_enumerate.py` rebuilds the equilibrium sets from the flow law: 1,928 cases at prior 1/2 and 50,024 cases at 13 other priors, four rule pairs, calibrations A (exact) and B (interval). No difference from Props. 3, 5 and Remark 1; no undecided comparison. | numerical diagnostic |

**Proposition 3 at B (rules IM and C1).** r_A = 1.393958 (J = k), r_F = 1.467127, r_N = 1.747878, r_J = 1.966097
(ρJ = k), r_S = 2.124148, r_C = 3.592659.

| Strengths | Equilibria | Entry |
|---|---|---|
| [1.2, r_A) | no informed trade (N) | 0.250000 |
| r_A | N; threshold pair (investor and challenger both indifferent) | 0.250000; 0.454185 |
| (r_A, r_F) | N; mixed purchase that recruits (R) | 0.250000; rises to 0.522757 |
| [r_F, r_N] | N; full purchase (F) | 0.250000; 0.522757 |
| (r_N, r_J) | F; mixed orders at the entry floor (Q) | 0.522757; 0.250000 |
| [r_J, r_C] | F | 0.522757 |
| (r_C, 3.6] | F | 0.250000 |

The low class abstains up to r_N, mixes on (r_N, r_S) and sells fully from r_S. So "full purchase" in F refers to
the high class. Under CM the threshold pair T adds entry that falls strictly from 0.454185 at r_A to ρ at r_J
(0.341462, 0.321311, 0.305208 at 1.55, 1.60, 1.65); at r_C, entry can take every value in [0.25, 0.522757].
Under I0 the equilibrium set is **empty** on (r_N, r_S].

| Strengths | IM, C1 | IM, CM | I0, C1 or I0, CM |
|---|---|---|---|
| (r_N, r_J) | F; Q | F; Q; T | empty |
| r_J | F | F; T | empty |
| (r_J, r_S] | F | F | empty |

**Proposition 5 (IM and C1).** C(π) = {r ≥ r_A : π < τ(r) ≤ M(π), ρΔ(r)max{π, 1 − π} ≤ k}.
(a) π < 0.396175: empty. (b) 0.396175 < π < 0.640739: [r_A, min{r_N(π), r_C(π)}], the same start r_A for every
prior and slot. (c) 0.640739 ≤ π < 0.650059: (r_π, min{…}] with τ(r_π) = π. (d) π ≥ 0.650059: empty.
The tie point r_π exists only for τ(r_0) ≤ π ≤ τ(r_2); the ceiling r_C(π) exists only for M(π) ≥ τ(r_0).

**Remark 1 (other tie rules).** (IM, CM): C(π) ∪ {r_π} when τ_A < π ≤ π_max. (I0, C1): the strengths of C(π)
with Δ(r)[1 − M(π)] > k. (I0, CM): the (I0, C1) set ∪ {r_π} when π ≤ π_max and Δ(r_π)[1 − M(π)] > k. At
π = π_max = 0.650059 the C1 set is empty, but CM gives {r_*} = {1.634218} under both investor rules: the full
purchase earns Δ(r_*)[1 − M(π_max)] − k = 0.000343 > 0, M(π_max) = 0.834698, the zero-order posterior is 0.454140,
and entry is 0.560586.

## Margins at calibration B (prior 1/2)

Strict hypotheses (they define the open parameter set):

| Hypothesis | Margin | Key |
|---|---|---|
| B_0(π) < c_H | 1.195833 | `margin_weakcost_B` |
| c_H < B_1(M) | 0.217155 (posterior: 0.026059) | `margin_recruit_B` |
| Δ_0 < k | 0.003333 | `margin_kweak_B` |
| k < ρκΔ_1 | 0.024824 | `margin_kstrong_B` |
| B_2(M) < c_H | 0.002689 (posterior: 0.000334) | `margin_return_B` |
| 82/59 < u < 2686/1559 | 0.328451 below, 0.004617 above | `margin_u_lo_B`, `margin_u_hi_B` |
| λ_lo(β) < λ < λ_hi(β) | 0.045583, 0.000599 | `margin_lambda_lo_B`, `margin_lambda_hi_B` |
| π_lo < π < π_hi (exact cutoffs 141/(141 + 59e), 4245/(4245 + 1559e)) | 0.032150, 0.000424 | `margin_prior_lo_B`, `margin_prior_hi_B` |

Derived strict inequalities (used in the proofs; new rows in round 2): Δ ≥ 1/60 on the path; g_H − g_L ≥ 1451/180;
k − J(r_0) = 1283/92400; ρJ(r_1) − k = 7/240; ρJ(r_2) − k = 0.043048; ρJ(2) − k = 11/11200 (so r_J < 2);
3/4 − τ(r_2) = 27/1451; τ(r_N) − 1/2 = 0.154463; 3/4 − τ_A = 0.109261; π_max − τ_A = 0.009320; 19/3 − u = 4.615052;
the CM endpoint margin 0.000343. Keys `margin_<condition>_B`, with `_frac` rows for the exact forms. The threshold
gaps (`gap_*_B`) now enclose the true differences; the smallest is r_2 − r_C = 0.007341.

Primitive domains and structural restrictions are listed apart: β ≤ 1/3 is a structural weak restriction with
slack 0.038678 (`margin_beta_B`), not a strict hypothesis. Boundary equilibria at exact ties (r_A, r_F, r_N, r_J,
r_S, r_C, π_A^lo, π_max) stay in the sets. The smallest margins measure one distance: B sets M = e/(1 + e),
0.000334 below τ(3.6).

## Refuted or corrected (against the brief and the earlier memos)

1. **r_F at B.** The earlier study reports 1.460985; that is calibration A's 𝔯(4/55), correct at A. At B,
   r_F = 𝔯(k(1 + e)) = 1.467127, as the brief now states.
2. **Coexistence outside the prior window.** The earlier model page says it "can still occur but starts later" outside
   (0.396, 0.641). Under C1 it starts later only for π ∈ [0.640739, 0.650059). Below 0.396175 and from 0.650059 on,
   no strength on [1.2, 3.6] has coexistence under C1; under CM the single point r_* joins at π = π_max.
3. **Investor rule I0.** The earlier memos give the I0 coexistence interval (r_F, r_N], but not that I0 leaves no
   equilibrium on (r_N, r_S] = (1.747878, 2.124148]: the low class has no admissible rate there.
4. **β ≤ 1/3** enters only the zero-order bound and Corollary 1; Props. 2–5 hold for every β < 1/2.
5. **Threshold-branch entries.** The earlier 0.350846, 0.328628, 0.310872 are calibration A values; at B they are
   0.341462, 0.321311, 0.305208.
6. **Entry at r_1** with the declared β = 0.294655 is 0.5227569 (the unrounded β of the earlier study gives
   0.5227573); both display 0.522757.
7. **The meaning of u** (round 1 of this package and the first brief): u is not the odds that an order is informed.
   Under full orders those odds are πu after a purchase and (1 − π)u after a sale.

Confirmed: (H1)–(H3) of the earlier study are sufficient and complete; each is used once, and dropping
B_0(π) < c_H gives entry 1 at r_0 (c_H = 47/10 example). Also confirmed: the ownership condition, r_A, r_N, r_C,
the prior range, ownership 0.324401 and the return margin. The shared objects of TEAM_RULES §3 agree with equation
(4) of the pinned manuscript; direct integration over R reproduces them exactly.

## Round 2 changes

Each item of `memos/XP1_check.md` §10, and what this round did. No item needed a rebuttal.

| XP1 item | Change |
|---|---|
| 1. Interpretation of u | §1.2 now defines u as the informed presence mass relative to the liquidity mass in one direction, with 1 + u the largest likelihood ratio, and states the odds πu and (1 − π)u under full orders. Listed as difference 7. |
| 2. Lemma 3 premises | The lemma now assumes Δ ≥ 0, Bayes posteriors (E1), competitive prices (E4) and entry in [ρ, 1], and says which parts use which premise. Corollary 1 now states that "every profile" keeps Bayes beliefs and optimal preparation. |
| 3. Zero-order mass in Prop. 2 | Step 1 now uses f_H(x) = f_L(x) = (1 − λ)η(x) + λ1{x = 0}. No value changes. |
| 4. Product construction | New Lemma 2(f): the price algebra for any μ and any e that is nondecreasing in μ, with no equilibrium premise. The product lemma now has separate "only if" (Lemma 2(a)–(e) on an equilibrium) and "if" (Lemma 2(f), then E2, E3, E4 by direct computation) parts. Prop. 2 Steps 1, 3 and 5 and Prop. 3 Step 6 verify their tuples the same way. Lemma numbering is unchanged. |
| 5. Summary row on (r_N, r_S] | The tie-rule table now has three rows: (r_N, r_J), r_J and (r_J, r_S], with the sets of XP1. |
| 6. CM entry at r_C | The entry formula in Prop. 3 has a third case: at r_C under CM, entry is ρ + [e(1) − ρ](b + λ/2) ∈ [ρ, 𝖤_1]. Statement (b), form F, Step 7 and the B table say the same. |
| 7. Domains of r_π and r_C(π) | r_C(π) is defined only when M(π) ≥ τ(r_0); r_π only for τ(r_0) ≤ π ≤ τ(r_2). Step 3 and case (d) of Prop. 5 treat π > τ(r_2) and π = τ(r_0) explicitly. |
| 8. CM endpoint at π_max | The old paragraph is replaced by Remark 1 with a proof and a table of the two tuples at r_*, π_max (new keys `M_pimax_B`, `mu0_pimax_B`, `margin_cmend_B`, `entry_cmend_B`). The values agree with XP1 to 24 places. (I0, C1) and (I0, CM) now have separate sets. |
| 9. Interval serialization and gaps | `p1_common.py` converts interval ends exactly to fractions and prints the lower end rounded down and the upper end up (24 places). Displays come from the exact ends. Root brackets now have width at most 1e-40. Each gap subtracts the whole root brackets. `p1_compare.py`: all 70 shared enclosures contain XP1's exact intervals; 0 display changes; 0 removed keys; 21 value strings change in the last digits (at most 6.2e-14). |
| 10. Stale r_F attribution | Difference 1 now attributes 1.460985 to the earlier study (calibration A) and states that the brief gives 1.467127. |
| 11. Derived margins, exact cutoffs, domains, ties | 22 new registry rows (11 derived margins, 7 exact forms, 4 CM endpoint values). The margins table has three groups: strict hypotheses (Table 4, exact cutoffs λ_lo(β), λ_hi(β), π_lo, π_hi), derived strict inequalities (Table 5, including 3/4 − τ_A = 0.109261), and primitive domains with structural weak restrictions (β ≤ 1/3 as slack). A paragraph keeps the boundary equilibria at exact ties. Prop. 4(c) prints its decimal endpoints with ≈. |

Other changes in round 2:

- Notation switched to LABELS §1 (`f_j(x)`); the low-class rate is now `t̄(r)`.
- `p1_enumerate.py` dropped the no-trade candidate at a challenger tie under CM; this is how round 1 missed the CM
  endpoint. The script now keeps it, checks full orders at a CM tie against the return condition, decides exact ties
  at zero rates in exact arithmetic, and scans all four rule pairs at 13 priors. The prior 69/107 = τ(3/2) gives an
  exact case of Remark 1(a) away from the endpoint: coexistence at r = 3/2 under CM, not under C1.
- `p1_numbers.py` checks the mpmath enclosure of e against the series bracket S_110 < e < S_110 + 112/(111·111!).
- Prop. 3 Step 7 now prints ρJ(2) − k = 11/11200 > 0, which gives r_J < 2.
- Statement wording of Lemmas 1–3, Props. 2–5 and Corollary 1 is unchanged except where an item above required it.

Run log of round 2: all five scripts ran through `scripts/_slots/run_slot.sh` (each under one minute).

For the writers (W1, W4): re-read these statement texts, which changed in round 2:

- Lemma 2: new part (f) (additive);
- Lemma 3: the premise block;
- the low-class lemma (Lemma 7): the rate is now `t̄(r)`;
- Proposition 3: the entry formula for F (third case at r_C under CM) and statement (b);
- Proposition 4(c): exact cutoffs π_lo, π_hi, with ≈ for the decimals;
- Proposition 5: the domains of r_π and r_C(π); Remark 1 replaces the paragraph on other tie rules.

Open: no independent recomputation exists yet for four new rows: `entry_cmend_B`, `margin_tau_rN_half_B`,
`margin_pimax_tauA_B` and `margin_u_kstrong_B`. The other new interval rows (`M_pimax_B`, `mu0_pimax_B`,
`margin_cmend_B`, `margin_tauA_3q_B`) agree to 24 places with values in the text of `memos/XP1_check.md`.
