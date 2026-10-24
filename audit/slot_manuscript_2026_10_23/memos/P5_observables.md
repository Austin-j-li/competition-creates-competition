# P5 observables (R11): summary (round 2)

Package: `proofs/P5_observables.tex` (21 pages; build in `proofs/build/`). Script and log: `scripts/P5_observables/` (`p5_observables.py`, `run_log.txt`; section 12 of the log holds the round 2 computations). Registry: `registry/P5_observables.csv` (135 rows: the 112 rows of round 1 with unchanged keys, values and displays, plus 23 new rows). Interval arithmetic, 60 digits; no assertions, no tests.
Round 1 files for comparison: `scripts/P5_observables/round1_registry.csv`, `round1_run_log.txt`.

## Model objects used

Outcomes at `π = 1/2`: N (no informed trade), U (buys only), F (buys and sales). Notation: `b=(1-λ)β`, `d=b+λ/2`, `M=(1+u)/(2+u)`, `ϑ=u/(2+u)=2M−1`, `A_r(μ)=t_L−t_0+Δ_Tμ`, `J_r=1{B_r(M)≥c_H}`.
Boundary `r_S`: the unique root `r>1` of `ρΔ_T(r)m = k`, that is `r_S = 𝔯(D_S) = 1 + D_S + √(D_S²+2D_S)` with `D_S = k/(ρm) = 2(1+e)/25 = 0.297463`. At B, `r_S = 2.1241481328…` (display 2.124148, which lies below `r_S`). Full orders are unique for `r_S < r < h` (`h = 10`).

## Results (each with proof, status, value at B)

| Result | Statement | Status | At B |
|---|---|---|---|
| Prop. 2 | Volume, mean order, informed share separate N, U, F | analytical; values c.-a. | `v` 0.391230 / 0.559291 / 0.727352; share 0.300489 (U), 0.462117 (F) |
| Prop. 3 | `S = ρΔ_Tϑ + (1−ρ)J A(M)` (conditional execution spread); buy impact − sell impact = entry term; fall at `r_C`; above `r_C` the entry component is zero | analytical; values c.-a. | `S(r_1)` 0.786299; entry share **90.2%**; `r_C` 3.592659; fall 0.861835 |
| Prop. 4 | Counts leave the informed share open on `[ϑ_min, ϑ̄(r))` once F must be an equilibrium; sell impact + volume identify `(ϑ,λ,β)` on F; counts identify them on U | analytical; values c.-a. | range `[0.250299, 0.76)`; band (0.41, 0.462784); alternative pair `u'=8/5` has the same counts and entry, `S` = 0.778935 |
| Prop. 5 | Entry `= ρ + (1−ρ)J·Pr(buy)`; flat at `ρ+(1−ρ)d` on `(r_S,r_C]` and on U; flat `ρ` above `r_C` and with a hidden price (every strength, every profile) | analytical; values c.-a. | plateau 0.522757; rise 0.272757 |
| Prop. 6 | The three Section 7 predictions of the Laplace manuscript in slot form | analytical; values c.-a. | see Props. 5, 7 |
| Prop. 7 | Orders predict the winner among prepared challengers after they stop predicting entry: gap `ϑ(1−ℓ/r)`; `Cov(X,1_A)=0`, `Cov(X,1_W)=dρϑ(1−ℓ/r)>0` above `r_C` | analytical; values c.-a. | gap 0.308078 (`r_1`), 0.333751 (`r_2`); Cov 0.030344 |
| Prop. 8 | Announcement returns `Δ¹=(1−e)A(μ)`, `Δ⁰=−eA(μ)`; mean zero over both announcements; mean positive over preparation announcements alone; a neutral order lowers the price below `r_C` | analytical; values c.-a. | neutral price change −0.257948; preparation sample 0.160592 (dollars), 0.270349 (return) at `r_1` |
| Prop. 9 | On U (1.55–1.65): mean order `λ/2>0`; `P(0)<P(−1)<P(1)`; entry after a buy is 1; under the challenger rule N and U are the only outcomes | analytical; values c.-a. | mean order 0.168061; sale above no-trade price by 0.005363 at 1.60 |

## N1 claims: survive, change, fail

- **Survive** (identity or structure, re-derived with proofs): spread decomposition; entry–spread asymmetry; fall at `r_C`; sell-impact identification; non-identification from counts; winner gap formula; covariance restrictions; zero mean announcement return over both announcements; neutral-order price fall; constancy of volume and informed share from `r_1` to `r_2`.
- **Change** (value only): every number that depends on `(λ,β)`: 90.4% → 90.2%; `ϑ` 9/20 → 0.462117; `r_C` 3.458 → 3.592659; buy-only volume 31/51 → 0.559291, share 9/31 → 0.300489, mean order 3/17 → 0.168061; winner gaps 0.3, 0.325 → 0.308078, 0.333751; event changes (tables).
- **Extended**: full orders are unique on `(r_S, h)`, not only on `[3,18/5]`. Entry equals `ρ+(1−ρ)d` for every low-class sale rate once the high class buys fully and `J=1`.
- **Fail**: N1 §2.1 says each spread component rises strictly while `J` stays fixed. On the regime `J=0` the entry component is identically zero (Prop. 3(v)). The comparison pair with `β'=23/68` lies outside the model (`β' > 1/3`). N1's recomputation at `β=1/3` matches in exact rationals (21 of 21 values; run log §10).
- **Clarified**: the informed share `λ/(λ+2b)` is prior-free; it equals `2M−1` only at `π=1/2`.

## Scope (open items, in one place: PDF Section 2, Table 4)

The package proves N, U and F at prior 1/2. Three items stay open:

- **Equilibrium selection.** On `r_F < r < r_N`, `r ≤ r_C`, the outcomes are exactly N and U under the challenger rule (Prop. 9(v)); Prop. 9 states the observables of both. Which one occurs is open. An indifferent challenger who may mix adds one partial-buy outcome (Remark 2).
- **Intermediate branch.** `Δ_T < k` gives N alone and `r > r_S` gives F alone. On `[r_N, r_S]` the low class may mix; Prop. 5(iv) gives entry for every low-class rate and Lemma 5 gives the order law. The equilibrium set for `Δ_T ≥ k` with `r ≤ r_F`, and the spread, winner and announcement formulas on `[r_N, r_S]`, are open.
- **Observation protocols.** The formulas hold under the protocols of PDF §1.4 (Table 3). A data source for each protocol is open.

## Round 2 changes

All XP5 items hold. I re-derived each one and recomputed it in `p5_observables.py` section 12 (interval arithmetic). No rebuttal is needed. The recomputed values agree with the XP5 log to display precision.

| XP5 item | Where | What I did |
|---|---|---|
| Endpoint `r_S`: the literal interval `(2.124148, 10)` is false | PDF §1.1, Remark 1, Prop. 1(b), Table 7, parameter set; registry `rS_p5_B` note and new rows `delta_rS_B`, `rS_cert_hi_B`, `rS_counter_r_B`, `rS_counter_margin_B` | The bound is `r > r_S` with `r_S` defined exactly (root of `ρΔ_T m = k`; `D_S = 2(1+e)/25`). The upper end is `h`. Remark 1 shows the failure: at `r = 2.1241481` the margin is −8.59×10⁻¹⁰ (log §12a). 2.124149 is a sufficient rounded endpoint (margin +2.27×10⁻⁸). `rS_B` already exists in `registry/P1_core.csv` with the same display, so I added no duplicate; `rS_p5_B` keeps its key and value |
| Entry component does not rise above the ceiling | Prop. 3(v), proof, Table 1, §10 Table 7 | Split into two statements: all five quantities rise strictly on `(r_S, r_C]`; above `r_C` the entry component is identically zero and class component, `I_-`, `I_+`, `S` rise strictly. Log §12b: grid of 78 strengths, entry component exactly 0 for `r ≥ 3.6`. N1 §2.1 is recorded as failed on `J=0`; "Fail: none" removed |
| Price sufficiency step | PDF Lemma 4 | Added: equal prices give equal posteriors. Arbitrary candidates with pooled prices are covered |
| Count-based range needs incentives | Prop. 4(c), (d), proof, "At B", Table 7; registry `theta_max_full_eq_r1_B` (19/25), `theta_max_full_eq_r2_B` (701/845), `margin_obs_band_incentive_B` (21563/870600), `theta09_beta_B`, `theta09_lowsale_r1_B` | A full-order pair gives its counts through an F equilibrium only if `ϑ' ≤ 1 − 2k/(ρΔ_T(r))`. The range at B is `[0.250299, 0.76)`, not `[0.250299, 1)`. Example: `ϑ'=0.9` has `β'=0.105296` but a low-class sale payoff of −7/600. Every pair in the band has strict incentives at `r_1` and `r_2` (margin 0.024768) |
| Exhaustive two-cluster claim depends on the challenger tie rule | Prop. 9(v) and proof, Remark 2, tie table, Observable; registry `mix_*_r160_B` | Under the rule "prepare at indifference", N and U are the only outcomes (proof). With a mixing challenger a third outcome exists. Run log §12e verifies the tuple at 1.60 against the fixed tuple: `σ_H(1)=0.492845`, `e_1=0.506106`, mean order 0.082828, entry 0.321311, low-class sale payoff −0.0059375. The tie table restricts "none" to existence and formulas |
| Prop. 9(iv) sentence "In N both are zero" | Prop. 9(iv) and proof | Replaced: in N the buy impact is zero and the entry after a buy is `ρ`, so the entry increment is zero |
| Spread concerns conditional execution prices | §4 opening, Table 3 (model objects and counterparts), Observable paragraphs | "Quoted spread" removed. `P(x)` is the conditional execution price; the model has no quote stage. Table 3 lists twelve objects with their counterpart and condition. `k` is not a dealer charge. Sell impact needs maintained inputs `ρ` and `Δ_T(r)` |
| First-order measurement instruction | §3, §6 Observables, §1.4 | Use the first prespecified public opportunity and record a zero. A sample of first executed trades cannot identify `v`, the neutral price effect or the share |
| Zero mean announcement return needs both outcomes | Prop. 8(i)–(iii), (vi), Observable, "At B"; registry `evprep_*` | The mean is zero over both announcements with their model probabilities, and `Δ⁰` is stated for `e_x < 1`. The preparation-only sample has a positive mean: 0.160592 and 0.270349 at `r_1`; 0.701042 (= 673/960) and 1.045918 at `r_2` |
| `r_F` note | Memo, PDF §10, registry `rF_check_B` | The paragraph "Refuted brief value" is removed from the memo and the PDF. The note of `rF_check_B` now says that `r_F = 1.467127` agrees with the brief and with P1 |
| Open set `Θ` is not open (`β ≤ 1/3`) | PDF §11, Tables 8 and 10 | Replaced by the strict set in Table 10 (`β<1/3`, `λ`-band, `M`-band, `r_S(M)<r<h`, `r_F(M)<r<r_N`) and the consequences (a)–(e). The uniqueness margin tends to zero as `r↓r_S`. `β=1/3`, `r=r_C`, `r=r_N` are boundary cases. Table 8 has `β<1/3` in its first row and gains six rows: `u>82/59`, `M>5/8`, `r_S<r_C`, `r_N<r_C`, `r_S<h`, band incentives (registry `margin_obs_*`) |
| Prop. 3(vi) needs `r_S < r_C` | Prop. 3(vi) | Hypothesis added; margin `r_C − r_S = 1.468510` |
| Prop. 5: plateau on U needs `r ≤ r_C`; hidden price | Prop. 5(iii), (v), (vi) | `r ≤ r_C` stated; hidden price gives `ρ` at every strength and every order profile; comparative statics on a region with `J_r = 1` |
| Prop. 6: F at `r_2` | Prop. 6 | `ρΔ_T(r_2)m > ρΔ_T(r_1)m > k` stated |
| Prop. 7: gap is among prepared challengers | Prop. 7 Observable | The unconditional gap `e_1w_1 − ρw_{-1}` is stated; above `r_C` it equals `ρ(w_1 − w_{-1})` |
| My own correction: Table 1 label | Table 1, Prop. 9 row | The "price gap" value now uses `U_gap_r160_B` (0.005363). Round 1 printed the spread `ba_U_r160_B` under this label |
| My own correction: proof order in Prop. 9(v) | Prop. 9(v) proof | The proof now derives `t = 0` from `μ_{-1} ≤ 1/2` first, and only then states `μ_0 = (1−2b−s)/(2−4b−s) ≤ 1/2`. The first draft used `μ_0 ≤ 1/2` before `t = 0`, which holds only if `s ≥ t` |
| My own correction: Prop. 3(v) framing | Prop. 3(v) | The sentence for `r_C ≤ r_S` is removed; the statement assumes `r_S < r_C`, as Prop. 3(vi) does |
| Open items in one place | PDF §2, Table 4 | See "Scope" above |

Nothing the checker refuted remains in the package. No XP5 item is rejected.

## For the coordinator and for W1, W3

- Re-run `scripts/_coordinator/make_numbers.py`. `registry/registry.csv` holds a copy of `rS_counter_margin_B` with the display `$-8.59\times10^{-10}$`. The final display is `\ensuremath{-8.59\times10^{-10}}`, which works in text and in math. Round 2 also renamed three keys: `DS_B` is now `delta_rS_B`, `mix_EX_r160_B` is `mix_mean_order_r160_B`, `margin_obs_M_over_58_B` is `margin_obs_post_over_58_B`.
- LEDGER line 60 says "full orders unique on (2.124148, 10)". Read it as `(r_S, h)` with the exact `r_S`.
- Section 8 can use Props. 3, 5, 7 as headline results and Props. 4, 8, 9 as supporting results. State the spread as the conditional execution spread.
- The `ba_*` keys (spread, impacts) stay as they are; the prefix is a historical name for the conditional execution spread. Keep `ba_*` apart from W2's `spread_*` keys (`Δ_T`).
- P1 (`memos/P1_core.md` item 3) states that under its investor rule I0 the equilibrium set is empty on `(r_N, r_S]`. P5 uses the rule "an indifferent investor chooses any mixture" and keeps that branch open. A document must name the investor rule next to any statement about this interval.
- One sentence for the comparison note: the slot gives a conditional execution spread for a unit order with a direct informed-share link; the Laplace set-up prices aggregate net flow, so its maximum price gap is not a unit spread.
