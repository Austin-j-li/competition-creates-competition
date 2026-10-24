# XP2: independent check of the P2 package (R6 and R9)

## 1. Scope and verdict

This memo checks the P2 proof package for R6 (value classes and priors) and R9 (access to prices, payment rule, reserves):

- `proofs/P2_auction.tex` (built PDF in `proofs/build/`),
- `memos/P2_auction.md`,
- `scripts/P2_auction/`,
- `registry/P2_auction.csv` (3,386 rows).

The sources are the pinned Laplace manuscript (`01bd5d6`, Sections 5.2 and 6, Appendices A.4, A.6, A.7, A.8; Online Appendix A.13, A.14, C.4, C.9, C.10), the earlier memos `E1_auction_side.md` and `XE1_check.md`, and `proofs/P1_core.tex`.

**Overall verdict.** Every headline result of P2 is **confirmed**. No claim is refuted. Every one of the 3,386 registry rows agrees with my own recomputation in value and in display. Eight corrections remain. All are about notation, display, scope wording, or one compressed step (Section 7). None changes a number or a conclusion.

| Item | Claim | Verdict |
|---|---|---|
| 1a | Two-class comparison for general `G_H, G_L`, priors, strict conditions | confirmed |
| 1b | Nonempty open region for every ranked pair and every prior | confirmed |
| 1c | Admissible region at B (slot band, prior windows) | confirmed |
| 1d | Every value-class example of the Laplace manuscript, own costs and strengths | confirmed |
| 1e | Many classes under separation; four-class certificate | confirmed |
| 1f | Strict three-class equilibrium, two posteriors at one price | confirmed |
| 2a | Access at B: +0.257948 proceeds, +0.081960 net surplus, break-even scale 6.848394 | confirmed |
| 2b | Access outside the recruitment region lowers both | confirmed |
| 2c | Payment rule: spread response with the sign of `1 − 2η`; `η` as in the Laplace manuscript | confirmed (wording and notation corrected) |
| 2d | Flat entry at the exclusion reserve; 31/20 restores strict deterrence and excludes the weak incumbent | confirmed |
| 3 | Proofs against BRIEF §5 | confirmed; no circular step; one compressed step |
| 4 | Registry recomputation and key collisions | confirmed: 0 value differences, 0 display differences, 0 collisions |

## 2. Method

I wrote my own engine and driver:

- `scripts/XP2/xp2_engine.py`: the auction kernel, the class averages and the two-class slot node.
- `scripts/XP2/xp2_check.py`: every R6 and R9 quantity, the registry comparison and the collision check.
- `scripts/XP2/run.log`: the complete printed record.
- `scripts/XP2/xp2_values.csv`: every recomputed key, with its midpoint and its enclosure.
- `scripts/XP2/xp2_diff.csv`: one comparison row for each registry key.
- `scripts/XP2/manifest.json`: software versions, the registry hash and the output hashes.

Run from the repository root (22 seconds, one process):

```
.venv/bin/python audit/slot_manuscript_2026_10_23/scripts/XP2/xp2_check.py \
  > audit/slot_manuscript_2026_10_23/scripts/XP2/run.log
```

The engine differs from the P2 script in each layer:

1. **Value kernel.** I use closed forms over `R ~ U[0, r]`: `g_v = ∫_p^v F`, `t_v = v − g_v`, allocation `v + E[(R − v)_+]`. P2 integrates realized payoffs by a midpoint rule.
2. **Class averages.** I use Simpson's rule on each piece split at `p` and `r` (exact for degree three). P2 uses an open three-point rule.
3. **Orders and entry.** My node derives the order profile from the all-profile bounds (`Δ < k` forces zeros; `ρκΔ > k` forces full orders). It derives the high-cost pattern from C1 and the sign of `B − c_H`. P2 prescribes the pattern and then checks signs.
4. **Pure-profile scan.** For each node I also test all nine pure profiles against their own prices and entry. Exactly one profile survives at every node.
5. **Arithmetic.** Exact `Fraction` for every rational object; `mpmath.iv` at 60 digits for every quantity with `e`. A sign counts only when the enclosure excludes zero.

I read `scripts/P2_auction/derive.py` only to fix the meaning of these registry fields: `cost_sign_*`, `low_profit_*`, `prior_cost_margin`, `admissible`, `two`, `sale`, `paid_cost`, `surplus`, `choice_*`, the sequence fields `margin0` to `margin3`, `p2_many_low_cost`, and `margin_p2_prior_*_order_B`. I checked each definition against the proof text before use.

**Shared formulas (TEAM_RULES §3).** The formulas for `t_0, t_H, t_L, g_H, g_L, Δ_T, B_r, τ, e_r, P_r` agree with equations (4), (5), (7) and (9) of the pinned manuscript. My exact kernel reproduces each closed form at `r = 6/5, 3, 18/5`.

## 3. Item 1: R6, value classes and priors

### 3.1 The two-class theorem for general classes and priors — confirmed (analytical)

I re-derived the proof of P2's Proposition 2 (general classes and priors).

- Under every candidate profile, `a_j(±1) ∈ [b, b + λ]`. So `μ_1 ≤ M(π)` and `μ_{−1} ≥ m(π)`. The proof uses only these two bounds.
- The residuals `U_H(1) = e(1)Δ(1 − μ_1) − k` and `U_L(−1) = e(−1)Δμ_{−1} − k` follow from competitive prices at the observed order. The proof needs no price inversion for this step.
- `Δ_0 < k` bounds every correct-sign residual below zero. So zero orders are unique, also against mixtures.
- `ρκΔ_i > k` makes the correct unit order strictly better than zero and zero strictly better than the wrong sign. So full orders are unique, also against mixtures.
- Equal prices imply equal entry and hence equal posteriors (P2 eq. invert). So the price reveals `μ_q`, and the strict cost comparisons fix entry under C1 and CM.
- Ownership: `e_{H,1} = ρ + (1 − ρ)(b + λ)` and `O_H = π e_H W_H`. The exact condition is `[ρ + (1 − ρ)(b + λ)]W_H(F_1) > ρW_H(F_0)`.

**Random diagnostic (numerical diagnostic).** At calibration B I drew random uniform class pairs in first-order order, random priors in (0.05, 0.95) and random strengths. I kept 300 draws that meet the strict hypotheses with interior costs. In all 300 draws:

- the bounds force the predicted orders;
- the cost signs give the predicted patterns `(0,0,0)`, `(0,0,1)` and `(0,0,0)`;
- exactly one pure profile is an equilibrium at each strength;
- as a formula check, the ownership change equals `π` times the ownership condition.

### 3.2 Nonemptiness for every ranked pair — confirmed (analytical)

The construction is correct. I checked each inequality: `Δ(r) = r^{-1}∫_p^r Γ(x)dx`; `Δ'(r) ≥ pΓ(r)/r² > 0` above `v_*`; `g_H − g_L ≥ pΓ/r`; `W_H(v_*) ≥ p/v_* > 0`; `g_j(r) → 0`. The choices of `r_1`, `r_0`, `c_H`, `k`, `r_2` are made in a valid order. Continuity gives the open set.

### 3.3 The admissible region at B — confirmed (analytical, interval endpoints)

| Region | P2 value | XP2 value |
|---|---|---|
| Slot band at fixed prior and costs | `82/59 < u < 2686/1559` | same; `u = 1.718282` inside, margins 0.328451 and 0.004617 |
| Trade bound on `u` | `u < 19/3` (weaker) | same |
| Priors with some trade cost (`κ > 1/10`) | (0.231969, 0.768031) | same |
| Priors with `k = 1/50` (`κ > 3/25`) | (0.270432, 0.729568) | same |
| Priors for parts (i)–(ii) | `(L(τ_1), 1365/2156)` = (0.467850, 0.633117) | same; `1365/2156 = 195/308 = τ_0` |
| Priors for all three strengths | (0.467850, 0.500424) | same |

At 11 interior priors of the last window, every hypothesis has a positive interval sign. The slot window for parts (i)–(ii) is wider than the Laplace window (0.467850, 0.538096). The reason is that the slot trade bound has no factor `1 − 1/b`.

At the fixed benchmark costs and strengths:

- `π = 3/10`: entry `(0.25, 0.25, 0.25)`. The strong upper profit misses cost by −1.390821.
- `π = 7/10`: entry `(1, 0.573175, 0.573175)`. The weak prior profit exceeds cost by 0.600833.

The trade window is nonempty at both priors (0.022698 > 1/60). P2 states all of this correctly.

### 3.4 Every value-class example — confirmed (computer-assisted)

Each example keeps its own costs and strengths, as declared in the Laplace manuscript (A.48, A.49, the class-exhibit notes, C.4). My forced profiles and entry patterns agree with P2 at every node.

| Example | Orders `r_0 / r_1 / r_2` | High-cost pattern at `r_1` | `E_1` | `O_{H,1}` | Smallest margin |
|---|---|---|---:|---:|---|
| Benchmark | 0 / full / full | `(0,0,1)` | 0.522757 | 0.324401 | `C_2` = 0.002689 |
| Moderate | 0 / full | `(0,0,1)` | 0.522757 | 0.324401 | `T_0` = 0.000810 |
| Narrow | 0 / full / full | `(0,0,1)` | 0.522757 | 0.324401 | `C_2` = 0.002658 |
| A | 0 / full / full | `(0,0,1)` | 0.472339 | 0.194641 | `T_0` = 0.005455 |
| B | 0 / full / full | `(0,0,1)` | 0.573175 | 0.454162 | `T_0` = 0.005455 |
| C | 0 / full / full | `(0,0,1)` | 0.573175 | 0.419819 | `T_0` = 0.006667 |
| D | 0 / full / full | `(0,0,0)` | 0.250000 | 0.175000 | `C_1` = −0.018122 (control) |

- In C, `W_H = 1, 599/648, 79/88` at the three strengths. Ownership rises from 0.175000 to 0.419819. The exact ownership margin is 0.349742.
- The class order in C holds: `G_L − G_H ≥ 0` everywhere, with equality only outside `(3/5, 19)`.
- The `C_0, C_1, T_0, C_2` margins equal the Laplace table values. This agreement is expected: `1 + u = e` makes `M(π)` and `m(π)` equal to the Laplace bounds.

**Constructive sequence (C.4 recipe, factor 1/2 kept).** The first feasible member is `n = 3` for all five ratios, with the same `r_0`, `r_1`, `k_n`, `c_{H,n}` as P2. The `n = 1, 2` margins agree. A slot-native recipe without the factor 1/2 is feasible at `n = 2` for the ratios 21/20, 11/10 and 5/4. P2 states that the factor is a declaration for these examples. That statement is accurate.

### 3.5 Many classes under separation — confirmed (analytical; certificate computer-assisted)

The group proposition is correct.

- The weak residual bound forces zero orders.
- The separation bounds force `+1` in group H and `−1` in group L under every profile.
- The group posterior then fixes the whole posterior vector.

For the four-class certificate, I enumerated the 16 vertices of the weight box myself:

| Quantity | Value |
|---|---|
| Largest feasible mean `ν·t` at `r_1` | 1.362462 |
| Smallest feasible mean `ν·t` at `r_1` | 1.054538 |
| `γ_H`, `γ_L` | 0.179205, 0.178871 (binding) |
| `ργ − k` | 0.024718 |

I also built the strong group tuple directly. Its entry pattern is `(ρ, ρ, 1)`, its prices are 0.576134, 0.614625 and 1.362462, and the smallest class choice margin is 0.024718. That margin equals `ργ − k`.

### 3.6 The three-class collision — confirmed (computer-assisted; equality analytical)

- I re-derived `w = (2b + 3b_0 + 2λ)/(2(2b + b_0 + λ)) = (1 + 2b_0 + λ)/2` by hand. The identity `z_0 = z_1` holds exactly at 200 random rational pairs `(λ, β)`. At B, `w = 0.940709` and `1 − w = (1 − λ)(4β − 1)/2 = 0.059291`.
- Orders zero and one have posteriors (0.154664, 0.690671, 0.154664) and (0.174878, 0.349755, 0.475367). Both give the mean 3.463429 and the price 1.522107.
- The strict choice margins are 0.260795, 0.020627 and 0.024768.
- Entry is `ρ` at every price. Every class profit is at most 95/16 < 10. Class 3 has posterior at least 0.154664 at every order, so zero-cost profit is strictly positive.
- At `w ± 1/1000`, the mean gap is ±0.001044. All three prices are distinct, and every choice stays strict.

P2's `p2_many_low_cost` uses the bound `(1/4)b/(b_0 + λ/2)` for the class-3 posterior. That bound (0.110966) is valid but loose. The actual minimum is 0.154664. The row's claim, positive zero-cost profit at every price, holds.

## 4. Item 2: R9

### 4.1 Price access at B — confirmed (analytical comparison; levels computer-assisted)

| Quantity at `r_1 = 3` | Access | Hidden | Gain |
|---|---:|---:|---:|
| Target proceeds | 0.872531 | 0.614583 | 0.257948 |
| Net surplus | 2.634044 | 2.552083 | 0.081960 |

Both gains also follow from P2's closed forms (difference below `10^{-60}`). The hidden tuple has unique full orders: both choice margins are 0.024824, and entry is `ρ` at every order.

**The trade scale.** A trade scale `z` means that one order unit trades `z` shares per share of float. The scale multiplies the informed position, the liquidity positions and the fee. The investor's choice, the order experiment, the prices and entry do not change. The expected transfer from liquidity traders to the informed investor is then `zG`, where `G` is the unconditional expected gross profit per unit:

```
G = λΔ_1{π(1 − M) + (1 − π)ρm} = 0.037665.
```

`G` already contains the factor `λ`. I checked `G` against the liquidity side: the liquidity traders' expected gross loss is −0.037665, and the sum is below `10^{-62}`. The comparison economy has no informed investor. Its posterior is `π`, its entry is `ρ` because `B_1(π) < c_H`, and its proceeds equal the hidden level 0.614583. Initial shareholders who bear the whole transfer gain `ΔR − zG`. This gain is positive exactly for

```
z < z* = ΔR / G = 6.848394.
```

At `z = 6.8483` the gain is +3.5 × 10⁻⁶; at `z = 6.8484` it is −2.3 × 10⁻⁷. The conditional figure `G/λ = 0.112059` is the gross profit given an informed slot. It is not the break-even denominator: it would give 2.301894. The Laplace value 1.831923 uses an investor who is always present. P2's definition and value are correct.

The execution-fee resource cost `λk = 0.006722` is the same in both economies, so it cancels from the surplus gain. P2 states this.

### 4.2 Access outside the recruitment region — confirmed

With `c_H = 12/5`, the strict signs are `B_1(m) − c_H = −0.033821` and `B_1(π) − c_H = 1.891667`. The access pattern is `(0, 1, 1)`, and the hidden pattern is `(1, 1, 1)`. Full orders are unique in both. Access changes proceeds by −0.173917 and surplus by −0.013505. Both values equal P2's closed forms.

### 4.3 The payment rule — confirmed (analytical); definition of `η` checked

- **Definition.** The Laplace manuscript defines `η` as the seller's Nash bargaining weight (Section 6.2, "seller share η"; A.38: `P = z + η(V − z)`). P2 uses the same definition, with the same domain `0 ≤ η < 1`, the zero reserve and the enforceable runner-up fallback.
- **Formulas.** I integrated `T_η(R, θ) = (1 − η)min(R, θ) + η max(R, θ)` directly over `R ~ U[0, r]`. The result equals the closed form (13) at all 202 grid points.
- **Coefficients.** `Δ_η(6/5) = 1/60 + (269/30)η` and `Δ_η(3) = 2/3 + (23/3)η`. The difference is `(13/20)(1 − 2η)`, which is zero exactly at `η = 1/2`.
- **Sign.** `(θ − R)_+` falls in `R`, and `(R − ℓ)_+` rises in `R`. So the spread response weakly has the sign of `1 − 2η`.

### 4.4 Reserves — confirmed (computer-assisted)

| Law, `p` | `E(r_0)` | `E(r_1)` | `R(r_0)` | `R(r_1)` | Global order margin `r_0`, `r_1` |
|---|---:|---:|---:|---:|---|
| Points, 1/2 | 0.250000 | 0.522757 | 0.392708 | 0.872531 | 0.003333 (zero), 0.024824 |
| Points, 101/100 | 0.522757 | 0.522757 | 0.440564 | 0.994384 | 0.038167, 0.047239 |
| Points, 31/20 | 0.522757 | 0.250000 | 0.502822 | 0.893073 | 0.084215, 0.057405 |
| Bands, 1/2 | 0.250000 | 0.522757 | 0.392665 | 0.872504 | 0.002986 (zero), 0.024833 |
| Bands, 11/10 | 0.522757 | 0.522757 | 0.420123 | 1.022690 | 0.048076, 0.047572 |
| Bands, 31/20 | 0.522757 | 0.250000 | 0.502822 | 0.893073 | 0.084215, 0.057405 |

- **Exclusion reserves.** At both strengths the pattern is `(0, 0, 1)`. So entry equals `ρ + (1 − ρ)(b + λ/2) = 0.522757`, and entry is flat. Proceeds rise at both strengths.
- **Reserve 31/20.** Entry falls from 0.522757 to 0.25, and proceeds exceed the levels at reserve 1/2. The reserve lies inside `(p_H, 10 − 6/M) = (1.325270, 1.792723)`, with margins 0.224730 and 0.242723. Since `p_H − r_0 = 0.125270 > 0`, the weak incumbent is excluded.
- **Necessity of the exclusion.** On `p ∈ (1, 6/5]` with point values, a scan at step 1/200 finds the pattern `(0,0,1)` at both strengths. On `p ∈ (21/20, 6/5]` with bands, a scan at step 1/400 finds the same pattern. There the band objects equal the point objects exactly.
- **Exact events.** At `p_H` the identity gives `B(M) = c_H`, and the full-order margin is 0.050792. At `p = 10`, entry is 0.25, sale 0.125, two bidders 0 and proceeds 1.25. At the band endpoint `p = 201/20`, entry is 0.25 and sale and proceeds are 0.

The surplus rows at the reserve nodes come from my own allocation kernel. An inadmissible value leaves the allocation at `s_0 = E[R 1{R ≥ p}]`. So the factor `1 − G_L(p⁻)` of Laplace A.40 enters by construction, and the registry match covers the excluded low class.

The reserve derivative formula agrees with Laplace A.46 and A.47, with general `π` and a finite sum over orders.

## 5. Item 3: the proofs against BRIEF §5

| Result | Tuple | Conditions | Verification against the fixed tuple | Uniqueness by all-profile bounds | Strict margins |
|---|---|---|---|---|---|
| Auction lemma | n/a | n/a | direct integration | n/a | n/a |
| General two-class proposition | eqs. weak-tuple, full-tuple, bids | six, listed | yes | yes (bounds at ±1) | margins table; open set stated |
| Nonemptiness | via the two-class proposition | — | — | — | open set in five coordinates |
| Admissible region at B | — | — | endpoint margins; monotone `m`, `1 − M` | — | yes |
| Examples | yes | yes | yes, script prints every payoff | yes | yes; D negative by design |
| Two separated groups | weak: explicit; strong: `P_q`, `e`, `z_q` | yes | yes | yes | four-class certificate |
| Three-class collision | explicit, with pooled price belief | yes | yes | not claimed (existence) | yes |
| Access, both regions | access and hidden tuples | yes | yes | yes | yes |
| Payment rule | acquisition stage only | — | yes | — | `η = 1/2` boundary |
| General reserves | explicit `ζ_i`, `P_{i,q}`, beliefs | yes | yes | yes | node margins |
| Exclusion, deterrence, `p_H`, endpoints | yes | yes | yes | yes | yes |

**Circular steps.** I found none. Each uniqueness argument starts from bounds that hold for every candidate: the bounds at ±1, the entry floor `ρ`, and `e ≤ 1`. It then derives the orders, the posteriors, the entry and the prices in that order.

**Compressed steps.** I found one. Line 1133 of the proof says "the same argument applies once `p > 21/20`" for the bands. The text omits the required computation: for `21/20 < p ≤ 6/5`, the low band lies below `p` and the high band lies above `r_1 = 3`. So every band object equals the point object. My scan confirms a difference of exactly zero. Correction 3 supplies the sentence.

The other summary sentences ("the cost comparison and the payoff calculation verify all conditions", "these calculations verify D directly") follow a displayed computation or a registered margin.

**Tie rules.** P2 states both investor rules (IM, I0) and both challenger rules (C1, CM). Every strict example survives all four.

- The `p_H` row depends on C1 or CM. P2 says so.
- The two endpoint rows (`p = 10` for points, `p = 201/20` for bands) have zero gross profit at every belief. Their entry `ρ` rests on the zero-cost preparation convention of P1's equilibrium definition, not on C1 or CM. The proof text names this convention at the endpoint. The memo's scope paragraph lists only `p_H` (Correction 2).

**The domain `β ≤ 1/3`.** The two-class and group proofs use the posterior bounds only at the orders ±1. These bounds hold for every `β ∈ (0, 1/2)`. Thus `β ≤ 1/3` enters only through the brief's model restriction and the all-order statement (eq. bounds). P2 calls it a structural domain restriction. That is accurate. This is a possible refinement, not an error.

## 6. Item 4: registry recomputation and key collisions

| Check | Result |
|---|---|
| Rows recomputed | 3,386 of 3,386 |
| Value differences beyond `10^{-40}` relative | 0 |
| Displays that are not a correct rounding of my enclosure | 0 |
| Sign disagreements | 0 |
| Duplicate keys within the file | 0 |
| Keys printed by `P2_auction.tex` | 151; all present in the registry |

**Collisions.** P2 shares 13 keys with `P1_core.csv`: `u_B`, `beta_B`, `lambda_B`, `b_B`, `M_half_B`, `m_half_B`, `tau_r0..2`, `u_lo`, `u_hi`, `prior_lo_B` and `prior_hi_B`. It shares 9 keys with `P4_information.csv`. All shared keys agree in value and display. No key is shared with `P3_research.csv` or `P5_observables.csv`. The merged `registry.csv` carries every P2 row unchanged. The same quantity under different keys also agrees: for example, `entry_r1_B` (P1) and `p2_base_r1_entry` (P2) differ by 3 × 10⁻¹⁷, which is P1's 16-digit rounding.

**Display observations (no value error).**

- Six rows show `0.000000` or `-0.000000` for nonzero values: `p2_seq_21_20_n3_margin2` (1.74 × 10⁻⁷), `p2_seq_21_20_weak_delta` (1/3279360), `p2_seq_21_20_weak_pay_h_2`, `_weak_choice_h`, `_weak_pay_l_0`, `_weak_choice_l` (±4.41 × 10⁻⁷). The document does not print them.
- The six `p2_payment_1_1_*` rows (`η = 1`) lie outside the proposition's domain `0 ≤ η < 1`. Laplace OA C.7 allows this endpoint as a separate payment-stage limit. The rows carry no such note.
- The proof's sequence table prints `k_n` as raw text such as `4.78727292167e-7`.
- The file holds 3,386 rows; the proof prints 151. TEAM_RULES §7 asks for one row per printed number. The extra rows are correct.

## 7. Corrections

None of these changes a number or a conclusion.

1. **Notation clash on `η`** (proof lines 33–34 and 847). `η(q)` is the liquidity order law, and `η` is also the seller's share. The Laplace manuscript uses `η` only for the seller's share. The brief writes the liquidity law as `(β, 1 − 2β, β)`, with no letter. Use that form, or give the law another letter. Other clashes in the same file are:
   - `b` for `(1 − λ)β` and for the bids `b_R, b_θ`;
   - `A` for the preparation rule `A(P, C)`, for `A_j = Pr_j(θ ≥ p)` and for the event `𝖠`;
   - `D(v)` for the class CDF gap and `D_0` for the dividend;
   - `Γ` for both the function `Γ(x)` and the constant `Γ`.
2. **Tie dependence list** (`memos/P2_auction.md`, scope paragraph). Add the two endpoint rows to the tie-dependent results. Their entry `ρ` rests on the zero-cost preparation convention at zero gross profit.
3. **Compressed step** (proof line 1133). Replace "the same argument applies" with the computation: "For `21/20 < p ≤ 6/5`, the low band lies below `p` and the high band lies above `r_1`; every band object then equals the point-value object."
4. **Proposition wording** (payment rule). "Its effect on the spread has the sign of `1 − 2η`" should read "weakly has the sign of `1 − 2η`; strictly when `E[(R − ℓ)_+]` changes strictly". The proof already says this; the statement should match.
5. **Tiny displays.** Give the six rows of Section 6 a scientific display, for example `1.74e-7`, if any document prints them.
6. **Typesetting.** In the sequence table, typeset `k_n` as `4.787273 × 10^{-7}` (and similar), not as raw `e-7` text.
7. **Limit rows.** Keep the six `p2_payment_1_1_*` rows, as Laplace OA C.7 allows. Add the note "payment-stage limit `η = 1`, outside `0 ≤ η < 1`; no entry equilibrium".
8. **Registry scope.** The coordinator can keep the 151 printed rows and those that the manuscript or slides will print, and archive the rest. The values are correct either way.

## 8. Open items (as P2 states them)

- Generic full-posterior recovery under mixed class profiles.
- The full order and preparation game under the bargaining rule.
- Existence of a continuation selection at every reserve, and a global optimal reserve.

This check adds no new open item.
