# XP4: independent check of the information package (R5, R7, R8)

## 1. Scope and method

This memo checks four files of workstream P4:

- `proofs/P4_information.tex` (17 pages, built in `proofs/build/`);
- `memos/P4_information.md`;
- `scripts/P4_information/` (derivation script and run log);
- `registry/P4_information.csv` (1,038 rows).

Sources: BRIEF §2–§5, the earlier memos `E2_information_side.md` and `XE2_check.md`, and the Laplace manuscript at commit 01bd5d6.
From that manuscript I read Sections 4.2, 5.1 and 5.3, Proposition A.3, Appendix A.4 and A.5, and Tables 2 and 3.

My script is `scripts/XP4/xp4_check.py`. Its output is `scripts/XP4/run.log`. The method differs from the package script:

- Interval arithmetic with outward rounding at 60 digits. The interval library supplies the enclosure of e; the package uses a Taylor enclosure.
- Auction objects come from direct piecewise integration over `R ~ U[0, r]` in exact fractions.
- Every tuple comes from a brute-force joint law over class, investor signal, challenger signal, slot identity and order.
  Posteriors, challenger beliefs, class entry rates, prices and order payoffs are read from that law. No closed-form entry formula enters a tuple.
- Each order side gets a complete equilibrium enumeration (Section 5.5 gives the argument).

The script prints values and contains no assertions. One run takes about one second.

Tie rules, as in the package and in P1: investor IM (any mixture at indifference) or I0 (abstain at indifference).
Challenger C1 (prepare at equality) or CM (any preparation probability at equality).

## 2. Verdicts

| Item | Verdict | Evidence in one line |
|---|---|---|
| 1. R5, fixed-information control | **confirmed**; sharper statement given | The control matches the Laplace control. Frozen entry is constant on (1, r_C]. Crossing probability 0 for r_0 → r_1, 0.272757 for r_1 → r_2. Price-hidden entry 0.25. |
| 2. R7, atomless costs | **confirmed**; the hypothesis set is larger than the proof needs | Entry 0.522757, ownership 0.324401, entry 0.382711 at 3.6 with half-width 0.1, floor kept with half-width 0.001. The proof never uses atomlessness. |
| 3. R8, private signals | **confirmed, with one correction** | Theorem, S(B) values, six pairs, both B pairs, mixed equilibria and their tie rules: all confirmed. No equilibrium was missed. The pair (0.95, 0.505) does not need the challenger signal. |
| 4. Proofs against BRIEF §5 | **confirmed** | No circular step. One compressed step (the separation of the two order problems) and one absent tie-rule sentence. |
| 5. Registry | **confirmed** | 1,038 of 1,038 rows recomputed. No row differs beyond its display precision. One exact tie at a rounding boundary. Four status labels differ from P1. |

## 3. Item 1: R5, the fixed-information control

### 3.1 What the control holds fixed

The package fixes `λ, β, π, G_H, G_L`, the cost law and both class order laws, with full orders `(q_H, q_L) = (1, −1)`.
The challenger reoptimizes preparation; market makers recompute competitive prices.
This is the Laplace control. Its Table 2 note reads: "imposes full orders at both strengths and lets the challenger reoptimize".
The price-hidden rows are, in the Laplace manuscript and in the package, the reoptimized equilibria with the price withheld from the challenger.

Under frozen orders the prices are strictly increasing in the order posterior at both strengths (my tuples print every increment).
So the price carries the information of the order, and the challenger posterior `μ(X)` has a fixed law.
Proposition A.3 then applies with `S = X`. The package states this correctly (lines 229–233).

### 3.2 Values (computer-assisted)

| Control | E at 1.2 | E at 3 | O_H at 1.2 | O_H at 3 | R_T at 1.2 | R_T at 3 |
|---|---:|---:|---:|---:|---:|---:|
| Frozen full orders | 0.522757 | 0.522757 | 0.324401 | 0.324401 | 0.503998 | 0.872531 |
| Price hidden | 0.250000 | 0.250000 | 0.125000 | 0.125000 | 0.392708 | 0.614583 |
| Laplace frozen (Table 2) | 0.562178 | 0.522757 | 0.350606 | 0.324192 | 0.520039 | 0.872392 |

The frozen weak profile is not an investor equilibrium: the H buy pays −0.015518 and the L sale pays −0.018879.
The frozen strong profile is the unique equilibrium, since `ρκΔ_1 − k = 0.024824 > 0` under every profile.
Every realized entry gap of the four control tuples is strict; the smallest is `B_3(M) − c_H = 0.217155`.

### 3.3 The correct statement (analytical)

The strict crossing probability, computed from indicator differences over the frozen order law, is exactly 0 for `r_0 → r_1`.
It is `(1 − ρ)(b + λ/2) = 0.272757` for `r_1 → r_2`. Both match the package rows.

The statement can be sharper than "does not rise". With frozen orders the posteriors are the three atoms `m < 1/2 < M`.
The threshold `τ(r)` rises and exceeds `5/8` for `r > 1`. So only the top atom can recruit.
Frozen entry is therefore a step function of strength:

- `E = ρ + (1 − ρ)(b + λ/2) = 0.522757` for `1 < r ≤ r_C = 3.592659`;
- `E = ρ = 0.25` for `r > r_C`.

My strength grid (1.1, 1.2, 2, 3, 3.5, 3.59, 3.593, 3.6) shows this step, at `r_C ∈ [3.592658518795, 3.592658518795]`.
The package claim "the strict-decrease claim fails at the first two strengths" is correct.
Correct text: "with orders held fixed, entry is unchanged at 0.522757 from 1.2 to 3; it falls to 0.25 only when the threshold passes the top posterior".
The Laplace sentence "entry falls from 0.562178 to 0.522757" has no slot counterpart.

Status labels: the Laplace manuscript marks the frozen rows "numerical diagnostic". In the slot they have closed forms up to e, so "computer-assisted" is right.

## 4. Item 2: R7, atomless preparation costs

### 4.1 Values (computer-assisted)

| Quantity at B | Package | Mine |
|---|---:|---:|
| Entry, weak / strong | 0.250000 / 0.522757 | 0.250000 / 0.522756943 |
| H ownership, strong | 0.324401 | 0.324401303 |
| Entry at 3.6, half-width 0.1 | 0.382711 | 0.382711388 |
| H ownership at 3.6, half-width 0.1 | 0.222020 | 0.222019799 |
| Largest half-width for the floor at 3.6, `c_H − B_{3.6}(M)` | 0.002689 | 0.002688902 |
| Entry at 1.2 / 3 / 3.6, half-width 0.001 | 0.25 / 0.522757 / 0.25 | same, with low support `[0, 1/5]` or `[0, 1/500]` |

With half-width 0.1, entry still falls from 3 to 3.6 (0.522757 → 0.382711), but not to the floor.
So the rise and the later fall survive; only "entry returns to ρ" fails. With half-width 0.001 all three parts hold (return margin 0.001689).
Under the earlier B convention the entry at 3.6 is 0.382711560, displayed 0.382712. The package correction of that display is right.

### 4.2 The hypothesis set against the proof (analytical)

| Hypothesis of Proposition 2 in P4 | Use in the proof (lines 357–409) | Needed? |
|---|---|---|
| `0 < π, ρ, λ < 1` | Bayes' rule; the floor `e ≥ ρ > 0` makes the price invertible | yes |
| `0 < β ≤ 1/3` | posterior bound after a zero order (`b_0 ≥ b`), so the low component prepares there | yes |
| `Δ_0 > 0` | not used; zero weak orders follow from `Δ_0 < k` alone | no |
| `Δ_1 > 0` | implied by `k < ρκΔ_1` | implied |
| `g_H > g_L` | `B` nondecreasing in the belief; price increment | implied by the support chain `B_{F_0}(π) < c_− < c_+ < B_{F_1}(M)` with `B_{F_1} ≤ B_{F_0}` |
| `w_L ≥ 0` | sign of the price increment | automatic: the target receives at least `p·1{R ≥ p}` |
| `supp H^0 ⊂ [0, L]`, `L < B_{F_1}(m)` | the low component prepares at every feasible belief | yes |
| `H^0` atomless or a mass at zero | not used | no |
| `supp H^1 ⊂ [c_−, c_+]`, `B_{F_0}(π) < c_− < c_+ < B_{F_1}(M)` | excludes the high component at the weak prior and the two lower strong beliefs; includes it at the strong top | yes |
| `H^1` atomless | not used in parts (i)–(ii); used only for the continuity of the ramp (eq. `costramp`) | no |
| `Δ_0 < k < ρκ(π)Δ_1` | order bounds under every profile | yes |

The proof uses nothing outside the hypothesis set, so the set is sufficient. It is not minimal.
The conclusion holds for every cost law `ρH^0 + (1 − ρ)H^1` with these supports, atomless or not.
The atomic benchmark (`H^0 = δ_0`, `H^1 = δ_6`) is a special case; my script gives the same 0.25 and 0.522757 for it.
Uniqueness under CM does not need atomlessness either: the order bounds hold for any entry rate in `[ρ, 1]`, and every realized gap is then strict.

Recommendation: state the robustness result as "any independent cost law with these supports". Keep atomlessness only for the ramp statement.

## 5. Item 3: R8, complementary private signals

### 5.1 The theorem (analytical)

I rederived the belief identities `μ_x = (1 − a_T) + (2a_T − 1)ν_x` and `Pr(H | P, Y = y) = φ_y(μ_x)`.
My script confirms both from the joint law at every tuple (challenger beliefs are read directly from the law).
The price loading obeys `ρΔ ≤ Δ_P ≤ Δ + (1 − ρ)(2d − 1)w_H` under every profile, also under CM, because `I_+ ≥ I_−`.
Correct gross returns lie between `(2a_T − 1)mρΔ` and `(2a_T − 1)D^+`. The four inequalities then force zero weak orders and full strong orders.
The one-pair condition `B_{r_1}(φ_−(μ_+)) < c_H` leaves exactly one pair that recruits, `(X, Y) = (1, +)`.

The hypothesis `β ≤ 1/3` in Proposition 3 is not used. The proof bounds `ν_x` only at `x = ±1`; at `x = 0` it uses `1 − ν ≤ 1`.
It is harmless at B. The B continuation below does use it, for the posterior after a zero order.

### 5.2 S(B), the separate signal vector (computer-assisted)

S(B) keeps B's slot parameters and uses `ρ = 0.85, c_H = 7.14, k = 0.015, r_0 = 1.1, r_1 = 2.3`.
The Laplace manuscript also treats its signal example as a separate vector (Table 3 notes), so this label matches the source.

- Margins at (0.70, 0.75): private 0.052500, joint 0.045265, weak 0.001455, strong 0.018594, one-pair 4.159475.
- Entry 0.850000 → 0.879797 (0.8797966076); ownership 0.425000 → 0.449238 (0.4492381407).
- Under the earlier B convention: 0.8797966463 and 0.4492381721. The displays do not change.
- Controls: investor sees J, no Y: 0.85 → 0.85. Investor sees T, no Y: 0.85 → 0.85. Both confirmed with their margins.
- Exactly six of the 25 grid pairs meet the four inequalities: (0.69, 0.75), (0.70, 0.75), (0.71, 0.74), (0.71, 0.75), (0.72, 0.74), (0.72, 0.75).
  Their minimum margins are 0.002132, 0.001455, 0.000959, 0.000777, 0.000616 and 0.000100. All six meet the one-pair condition and have `d > a_T`.
- My enumeration finds exactly one equilibrium at each strength at all 25 pairs: zero weak orders, full strong orders.
  At the ten pairs with `d ≥ 0.76`, entry falls from 0.925 to about 0.880, as E2 reported.

### 5.3 Unchanged B, earlier pair (0.70, 0.75): the mixed equilibria (analytical; values computer-assisted)

Three of the four inequalities fail (private −1.05, weak −0.048542, strong −0.002071); joint entry holds (0.903775). I rederived every rational in the package continuation:

- `Δ_P(r_0) = 311/1920` and `Δ_P(r_1) = 137/192` (class entry 13/16 and 7/16 at both strengths);
- weak zero-profit rate `s = t = 119b/96`, so the order probability is 0.721409 after each signal;
- favorable-signal threshold at `r_1`: `μ* = 47/106`, `ν* = 19/53`, `t* = 15b/19`;
- floor sale return at the threshold `19/795`, which exceeds `k` by 0.003899;
- strong sale rate `t = 4b/3` (probability 0.775969), with `ν_{−1} = 3/10` and `μ_{−1} = 21/50 < 47/106`.

At the strong tuple a zero order still recruits after `Y = +`: the gap is 0.219556.
Entry: 0.625000 → 0.512521. Ownership: 0.406250 → 0.329227. The closed forms `5/8 − 23b/40` and `13/32 − 63b/160` match the joint law to 4e-60.

Tie rules. My enumeration covers both challenger rules at every threshold.

- Under IM, each strength has exactly one equilibrium, under C1 and under CM. The CM threshold at `t = 15b/19` gives returns in [0.023899, 0.102319], all above `k`, so no threshold mixture exists.
- Under I0 no equilibrium exists at either strength. The four pure corners fail.
- The no-Y control at B: zero orders at `r_0`; `s = t = 4b/3` at `r_1`; entry 0.25 at both. This interior tuple also needs IM.
  Under I0 the no-Y control has no equilibrium at `r_1`: zero orders leave a buy return of 0.033333 > k, and full orders give 0.017929 < k.
  The package states the IM dependence for the signal tuples (line 823). It does not state it for this control (lines 835–840).

### 5.4 Unchanged B, new pair (0.95, 0.505): correction

The package values are right. Margins: private 1.150917, joint 0.058923, weak 0.002216, strong 0.020341, one-pair 0.009997.
Entry 0.250000 → 0.386946; ownership 0.125000 → 0.222515. The equilibria are unique under all four tie-rule pairs.

**Correction.** This pair does not show that the challenger's signal is needed.
At `a_T = 0.95` the top public posterior alone recruits: `c_H − B_{r_1}(μ_+) = −0.024606`, with `μ_+ = 0.05 + 0.9M`.
I computed the no-Y control at this pair. Its equilibria are unique: zero orders at `r_0`, full orders at `r_1`.

| (0.95, ·) at B | E at r_0 | E at r_1 | O_H at r_0 | O_H at r_1 |
|---|---:|---:|---:|---:|
| Investor sees J, no Y (the benchmark) | 0.250000 | 0.522757 | 0.125000 | 0.324401 |
| Investor sees T, no Y | 0.250000 | 0.522757 | 0.125000 | 0.318099 |
| Investor sees T, challenger sees Y (d = 0.505) | 0.250000 | 0.386946 | 0.125000 | 0.222515 |

So the challenger signal lowers strong entry from 0.522757 to 0.386946: after `Y = −`, the buy price no longer recruits.
The package gives no control row for this pair. A reader of the S(B) table would infer the opposite pattern.

**A pair at B that needs both sources.** I searched exact-interval margins on the grid `a_T ∈ {0.900, 0.902, …, 0.950}`, `d ∈ {0.5005, 0.5010, …, 0.5100}`.
The search adds one condition to the theorem: `B_{r_1}(μ_+) < c_H`, so the no-Y control has no reversal.
85 grid pairs qualify, all with `a_T` between 0.926 and 0.942. The upper end cannot pass 0.94361, where `μ_+` reaches `τ(3)`.
Example (0.94, 0.505), computer-assisted:

- margins: private 1.150917, joint 0.020731, weak 0.002611, strong 0.019445, one-pair 0.048822, no-Y top exclusion 0.013904;
- with Y: unique zero orders at `r_0`, unique full orders at `r_1`; entry 0.250000 → 0.386933; ownership 0.125000 → 0.221878;
- without Y: unique zero and full orders; entry 0.25 at both strengths;
- investor sees J: the benchmark, 0.25 → 0.522757.

Its smallest margin (0.002611) is larger than the new pair's (0.002216). Every comparison is strict, so all four tie-rule pairs give the same outcome.
The region is thin: `d` must stay below about 0.51. That is a property of B, since `d ≥ a_T` is impossible there (margin 0.049030).
The package proof of that impossibility is right; it also follows from `d < τ(r_0) = 0.633117` and `a_T > (1 + z_*)/2 = 0.723097`.

### 5.5 Search for missed equilibria (computer-assisted)

The argument behind the enumeration:

1. A wrong-signed order loses under every profile. After `T = +`, `E[V | T, X = q] − P_q = (a_T − μ_q)Δ_P(q) ≥ 0` because `μ_q ≤ a_T`, and `Δ_P ≥ ρΔ > 0`.
2. Then the buy return depends only on the buy rate `s`, and the sale return only on the sale rate `t`.
3. On each interval of `s` between the challenger thresholds the entry configuration is fixed. The gross return is `(2a_T − 1)·b/(2b + s)·Δ_P`, strictly decreasing.
4. So the equilibria on a side are of four kinds:
   - `s = 0` if the return there is at most `k`;
   - `s = λ` if the return there is at least `k`;
   - one interior root per interval (IM only);
   - threshold points under CM.

I applied this enumeration to every economy in the package and on the extra controls above:

- benchmark at 1.2, 3 and 3.6; the price-hidden economies; the atomless economies (orders fixed by the bounds `Δ − k` and `ρκΔ − k`);
- S(B) at all 25 grid pairs, with both of its controls;
- B with the earlier pair, the new pair, the pair (0.94, 0.505), and the no-Y controls.

Each side has exactly one equilibrium rate in every economy. No equilibrium is missing from the package.

## 6. Item 4: the proofs against BRIEF §5

| Proof | Tuple | Conditions | Verification against the fixed tuple | Uniqueness from bounds on every profile | Strict margins |
|---|---|---|---|---|---|
| Prop. 1 (R5) and the four control tuples | yes, eq. `full` and `construction` | six, listed | yes; the weak frozen tuple is labelled a control | strong frozen and hidden tuples: `Δ_0 < k < ρκΔ_1`, `B_i(π) < c_H` | yes |
| Prop. 2 (R7) | yes | six | yes | yes, with `e ∈ [ρ, 1]` | yes; one margin is negative by design (return with half-width 0.1) |
| Prop. 3 (R8) | yes, eq. `signalfull` with beliefs and entry indicators | six | yes | yes, eq. `signalbounds` | yes |
| B continuation, earlier pair | yes, eq. `mixedlaws` and the rates | six | yes; the zero payoffs follow from exact cancellation | yes, monotone returns plus endpoint signs | yes |

No step assumes its conclusion. No step uses "by symmetry" or "similarly" without the computation.
The checks found two weak points; neither hides a gap:

1. **Compressed step.** Line 733 says "after wrong orders are excluded". The exclusion holds for every candidate by eq. `signalpayoffs` and eq. `signalbounds`.
   The proof does not say that the buy return then depends on `s` alone. One sentence closes this (Section 5.5, steps 1–2).
2. **Absent tie-rule sentence.** The no-Y control at B, strength 3, also needs IM and has no I0 equilibrium (Section 5.3).

The hypothesis redundancies in Section 4.2 and the unused `β ≤ 1/3` in Proposition 3 do not affect correctness.

## 7. Item 5: the registry

- My script regenerates all 1,038 keys from its own computation and compares value and display.
- No row differs from my enclosure by more than half a unit of its last displayed digit.
- The largest absolute difference is 4.8e-40. It comes from the package's 40-digit midpoints.
- The Taylor enclosure of e in rows `p4_e_lo` and `p4_e_hi` is valid: at 250 digits, `e` minus the Taylor sum is 2.0e-84, and the stated upper end exceeds `e`.
- Group-minimum rows (`margin_p4_min_*`) agree when I recompute them from their listed members.
- **One exact tie.** `p4_b_signal_r0_sell_price` equals `40968/76800 = 0.5334375` exactly. The display 0.533438 is correct under half-up and half-even rounding.
  A writer who truncates or rounds half-down would print 0.533437.
- **Status labels.** `entry_r0`, `own_r0`, `entry_r2` and `own_r2_B` carry "computer-assisted" with 40-digit decimals in P4.
  P1 gives "analytical" with 1/4 and 1/8. The merged registry carries the P1 rows. The P4 labels should follow P1.
- The shared B rows (`u_B` to `m_half_B`, `tau_r*`, `entry_r1_B`, `own_r1_B`) agree with P1 in value, display and status.

## 8. Corrections

1. **R8, new pair.** Add the no-Y control for (0.95, 0.505): entry 0.25 → 0.522757, ownership 0.125 → 0.318099.
   Or replace the pair with (0.94, 0.505), whose no-Y control stays at 0.25. Do not present (0.95, 0.505) as complementary information.
2. **R8, tie rules.** State that the no-Y control at B, strength 3, needs IM and has no I0 equilibrium.
3. **R8, separate order problems.** Add one sentence after line 733: the buy return depends only on `s`, the sale return only on `t`.
4. **R7, hypotheses.** Drop atomlessness from the hypotheses of parts (i)–(ii), or say that the proof does not use it. Keep it for the ramp.
5. **R5, text.** Use "unchanged at 0.522757 from 1.2 to 3" in place of "does not rise", where the sharper form fits. Give the step at `r_C = 3.592659`.
6. **Registry labels.** Align the four shared rows of Section 7 with P1.

No claim of the package is refuted. The earlier memos E2 and XE2 also survive: their S(B) values and grid pairs are confirmed.
Their B ownership display 0.324402 belongs to the earlier B convention; at the current B it is 0.324401, as P4 states.

## 9. Files

- `scripts/XP4/xp4_check.py`: the independent derivation.
- `scripts/XP4/run.log`: all tuples, side enumerations, margins, grids and the registry comparison.
