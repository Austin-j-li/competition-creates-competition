# P1_core: beliefs, informed trading and the main comparisons (R2, R3, R4)

Proof package: `proofs/P1_core.tex` (PDF in `proofs/build/`). Scripts and run logs: `scripts/P1_core/`.
Registry: `registry/P1_core.csv` (125 rows). Values are at calibration B and prior 1/2 unless stated. Decimals at B
depend on e; they are registry values with status computer-assisted (outward intervals).

## Results

| Label | Result | Status |
|---|---|---|
| Lemma 1 | Every order has positive mass in each class. At ±1 the odds move by at most 1 + u under every strategy (any β < 1/2). At 0 the factor is 1 + λ/b_0 ≤ 1 + u iff β ≤ 1/3; for β > 1/3 a strategy pair breaks the bound. | analytical |
| Lemmas 2–3 | Floor e ≥ ρ; the price reveals the posterior and rises strictly with it. Wrong-sign orders lose at least k; each class compares one gross return with k; ρκΔ ≤ K_j ≤ Δ under every candidate. | analytical |
| Corollary 1 | With β ≤ 1/3, B(M(π)) < c_H excludes high-cost preparation under every profile (the only use of β ≤ 1/3). | analytical |
| Prop. 2 | Under (H1) B_0(π) < c_H < B_1(M), (H2) Δ_0 < k < ρκΔ_1, (H3) B_2(M) < c_H: unique outcomes, the same under all four tie-rule pairs: no trade (entry ρ); full two-sided trade (entry ρ + (1 − ρ)(b + πλ)); full trade with entry ρ and an informative price. Ownership rises iff [ρ + (1 − ρ)(b + λ)]W_H(F_1) > ρW_H(F_0). | analytical |
| Lemmas 4–5 | J = Δ(1 − τ) and Δ(1 − τ)² increase on the path (exact Sturm counts); r_0 < r_A < r_F < r_N < r_J < r_S < r_1 < r_C < r_2 on the whole band. | computer-assisted |
| Prop. 3 | Complete equilibrium set on [1.2, 3.6] at prior 1/2, for every slot in the band (table below). | computer-assisted |
| Prop. 4 | (H1)–(H3) hold at the benchmark iff 82/59 < u < 2686/1559, that is 82β/(59 + 82β) < λ < 2686β/(1559 + 2686β). Prior range at B: (141/(141 + 59e), 4245/(4245 + 1559e)) = (0.467850, 0.500424); parts (i)–(ii) alone: (0.467850, 0.633117). | analytical |
| Prop. 5 | Coexistence set C(π) at every prior (below). | computer-assisted |
| Cross-check | `p1_enumerate.py` rebuilds the equilibrium set from the flow law at 241 strengths, four tie-rule pairs, calibrations A (exact) and B (interval): no difference from Props. 3 and 5. | numerical diagnostic |

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

The low class abstains up to r_N, mixes on (r_N, r_S) and sells fully from r_S. Under CM a threshold branch adds
entry that falls strictly from 0.454185 at r_A to ρ at r_J (0.341462, 0.321311, 0.305208 at 1.55, 1.60, 1.65).
Under I0 the equilibrium set is **empty** on (r_N, r_S].

**Proposition 5 (IM and C1).** C(π) = {r ≥ r_A : π < τ(r) ≤ M(π), ρΔ(r)max{π, 1 − π} ≤ k}.
(a) π < 0.396175: empty. (b) 0.396175 < π < 0.640739: [r_A, min{r_N(π), r_C(π)}], the same start r_A for every
prior and slot. (c) 0.640739 ≤ π < 0.650059: (r_π, min{…}] with τ(r_π) = π. (d) π ≥ 0.650059: empty.

## Margins at calibration B (prior 1/2)

| Hypothesis | Margin | Key |
|---|---|---|
| B_0(π) < c_H | 1.195833 | `margin_weakcost_B` |
| c_H < B_1(M) | 0.217155 (posterior: 0.026059) | `margin_recruit_B` |
| Δ_0 < k | 0.003333 | `margin_kweak_B` |
| k < ρκΔ_1 | 0.024824 | `margin_kstrong_B` |
| B_2(M) < c_H | 0.002689 (posterior: 0.000334) | `margin_return_B` |
| u in (82/59, 2686/1559) | 0.328451 below, 0.004617 above | `margin_u_lo_B`, `margin_u_hi_B` |
| β ≤ 1/3 | 0.038678 | `margin_beta_B` |
| prior in (0.467850, 0.500424) | 0.032150, 0.000424 | `margin_prior_lo_B`, `margin_prior_hi_B` |
| order of the Prop. 3 thresholds | smallest gap r_2 − r_C = 0.007341 | `gap_*_B` |

The smallest margins measure one distance: B sets M = e/(1 + e), 0.000334 below τ(3.6).

## Refuted or corrected

1. **r_F at B.** The brief lists 1.460985; that is calibration A's 𝔯(4/55). At B, r_F = 𝔯(k(1 + e)) = 1.467127.
2. **Coexistence outside the prior window.** The earlier model page says it "can still occur but starts later"
   outside (0.396, 0.641). It starts later only for π ∈ [0.640739, 0.650059). Below 0.396175 and from 0.650059 on,
   no strength on [1.2, 3.6] has coexistence.
3. **Investor rule I0.** The earlier memos give the I0 coexistence interval (r_F, r_N], but not that I0 leaves no
   equilibrium on (r_N, r_S] = (1.747878, 2.124148]: the low class has no admissible rate there.
4. **β ≤ 1/3** enters only the zero-order bound and Corollary 1; Props. 2–5 hold for every β < 1/2.
5. **Threshold-branch entries.** The earlier 0.350846, 0.328628, 0.310872 are calibration A values; at B they are
   0.341462, 0.321311, 0.305208.
6. **Entry at r_1** with the declared β = 0.294655 is 0.5227569 (the unrounded β of E1 gives 0.5227573); both
   display 0.522757.

Confirmed: (H1)–(H3) of E1/XE1 are sufficient and complete; each is used once, and dropping B_0(π) < c_H gives
entry 1 at r_0 (c_H = 47/10 example). Also confirmed: the ownership condition, r_A, r_N, r_C, the prior range,
ownership 0.324401 and the return margin. The shared objects of TEAM_RULES §3 agree with equation (4) of the
pinned manuscript; direct integration over R reproduces them exactly.
