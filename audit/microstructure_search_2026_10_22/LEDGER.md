# Task ledger: search for an EGJ-like microstructure

Started 22 October 2026. The coordinator updates this file after each event.
Rules: `TEAM_RULES.md`. Questions and scorecard: `BRIEF.md`.

Status values: planned, running, done, checked, failed.

## Coordinator notes

- The paper is pinned at `overleaf/paper` commit `01bd5d6` (the revised paper).
- Only L1 uses the shared browser. Other members cite the verified records or mark sources "unverified".
- Effort: high for most members; T1 runs at the highest effort; the check and the synthesis run one step
  below it. No red-team pass and no HTML report in this study.
- L1 returns (15 verified model specifications). Counts: Kyle-normal 3; EGJ/GG three-point 2; one-order
  arrival 1; noisy rational expectations 3; one-sided exponential 1; uniform 0; general density 1; other 4.
  Closest references: EGJ, GG, Dow–Gorton (1997), Admati–Pfleiderer (2009), Faure-Grimaud–Gromb (2004).
  Verified devices that hide the trader's motive: same-size liquidity arrival instead of the informed trader
  (Dow–Gorton p. 1095: information arrival "perfectly negatively correlated with the arrival of a liquidity
  trader"); a liquidity shock that forces the same whole-stake sale (Admati–Pfleiderer); GG's uninformed
  speculator (hides sales, not `Q = 2`). Presence alone (EGJ) leaves the outer flows revealing. Random order
  size and wider bounded noise have no verified corporate-model precedent. Bagnoli–Lipman (1996) is in RAND.
- T2 returns. A same-size liquidity trader makes every posterior interior and every flow on path, in all
  variants. Prop. 2(i)–(iii) hold at the paper's benchmark on the strip
  `82β/(59 + 82β) < λ < 2686β/(1559 + 2686β)` (at `β = 1/3`: `0.3166 < λ < 0.3648`). Best: V3 (one order
  slot, no separate noise), buy-only or two-sided. At `β = 1/3, λ = 6/17`: `M = 29/40`, entry
  `1/4 → 37/68 → 1/4` (paper 0.523 at `r_1`), ownership `23/68`, `r_C ≈ 3.4582`; no trade coexists with an
  informative equilibrium on about `[1.394, 1.748]` (full orders from about 1.461; a partial purchase below),
  which contains 1.55–1.65; entry flat on the full branch (no upward order); A.9 positive.
  With EGJ's separate noise (V1, V2) entry at `r_1` is only `71/204` and coexistence starts at 1.55659.
  The coordinator launched the check X on V3 before T1 and T3 return, to save time. Precedent for V3:
  Dow–Gorton (1997) alternative same-size arrivals (L1, verified), BKT (A7).
- L2 returns. Twelve method classes (M1–M12). The principle holds, with refinements: the top posterior
  must lie in `[0.705, 0.731)` at the benchmark; only the upper likelihood-ratio bound matters; coexistence
  needs the recruitment gain above `ρ` times the information loss. Short-list: (1) the same-size slot
  device (T2); (2) noise that is one-sided in the order's direction (M5/M11; Edmans 2009 precedent), not
  covered by T3, so the coordinator added T4; (3) coarse observation of the flow (weakest). Predictions:
  T1 gets feedback through flow 1 but no return at 3.6; T3 gets no exact return.
- T3 returns. Prop. 2(iii) fails for every bounded noise law (analytical): the top flow reveals class H and
  `g_H(3.6) > 6`; the smallest rescue needs `c_H > 5879/720 ≈ 8.17`, near `h`. Best lever: concentrated
  symmetric weights `(θ, 1 − 2θ, θ)` with `θ ≈ 3/20`, `λ` near 1: the flow 1 recruits with an interior
  posterior, entry 5/8 at `r = 3`, and a mixed branch `α_A` gives entry rising across 1.55, 1.60, 1.65
  (0.495 < 0.550 < 0.617) while it coexists with no trade (computer-assisted). A.9 holds. Binomial and
  two-unit variants are weaker. The coordinator added T5 to combine T2's slot device (fixes (iii)) with T3's
  concentrated noise (keeps the rising branch).
- X returns: all seven claims on T2's V3 confirmed (one with correction: full orders start at about 1.461).
  Scope caveat: with the paper's continuous menu `[−1, 1]`, a 0.99 purchase reaches an unused flow; under the
  prior belief at 3.6 it earns 0.0964 > 0.0446, so the result needs either the discrete unit menu (as in
  EGJ) or EGJ's belief convention. The strip is the posterior band `(τ(3), τ(3.6)) = (0.705, 0.7314)`, width
  0.026; `τ` rises only about 0.043 per unit of strength between the two benchmark strengths.
- T4 returns. Buy-only with noise that only buys (geometric D1, or exponential D2 as in Edmans 2009): every
  flow on path; Prop. 2(i)–(iii) analytical, with the paper's exact ceiling at `a = e^{−1}`; working range
  `1559/4245 < a < 59/141`. Entry at `r = 3` is 0.762955 (a low flow reveals class L, so good news is likely);
  ownership 0.5. Coexistence on `[1.393958, 1.747878]`; no upward order. A.9 holds. At matched posteriors its
  conditional payoff thresholds equal those of T2's V3. Precedent: Edmans (2009) for exponential noise (A6);
  the geometric form is unverified.
- T5 returns. At `(λ, β, θ) = (5/11, 1/2, 71/200)` (noise weights 0.355, 0.29, 0.355: heavier tails than
  EGJ's, not concentrated): Prop. 2(i)–(iii) analytical with uniqueness; entry `1/4 → 0.383125 → 1/4`;
  no trade coexists with an informative branch whose entry rises 0.353471 < 0.382165 < 0.383125 at 1.55,
  1.60, 1.65 (mixed, mixed, full; computer-assisted); A.9 holds; an open box of radii (1/1000, 1/1000,
  1/2000) works. Limits: entry at 3 well below 0.523; the rise is tiny at the top; prices need not rise
  with total flow; a branch with three interior purchase rates was not found. Not independently checked.
- T1 returns. EGJ's block (two-sided, equal weights, presence `λ`): Prop. 2(i) for every `λ`; full two-sided
  trade unique at `r = 3`, entry 1/2 once `λ ≥ 0.582`; Prop. 2(iii) fails for every `λ`, `θ` and `k < 0.0315`
  (analytical; return needs `r_2 > 7.97`, `c_H ∈ (8.17, 8.46]` or `h ∈ [7.54, 7.83)`); coexistence only at
  `r = 1.973`. Second knob `θ = 1/10, λ = 7/10`: the paper's `(1, −v)` at `r = 3` with entry 0.527; no trade
  coexists on [1.44, 1.80]; entry rises 0.419 < 0.450 < 0.484 at 1.55, 1.60, 1.65 (monotonicity analytical,
  certificates computer-assisted); A.9 holds. Needs investor mixing; unequal weights have no verified
  precedent. The coordinator added T6: T1's candidate plus T2's slot device, to restore (iii).
- T6 returns. No point meets every target. Analytical trade-off: Prop. 2(iii) needs the top posterior
  `M ≤ τ(3.6) = 0.731`, which caps `λ ≤ 0.463` for every `β` (so T1's `λ = 7/10` fails); on that cap both
  classes trade fully at `r = 3`, so no `(1, −v)`; T1's rising branch needs `M > 0.755`. Best compromise
  `(λ, β, θ) = (9/20, 12/25, 71/200)`: Prop. 2(i)–(iii) with unique outcomes, entry 0.492 at `r = 3`;
  coexistence on [1.548, 1.748] with entry rising 0.3505 < 0.3789 < 0.3802 (mixed, mixed, full;
  computer-assisted); A.9 holds; certified box of half-width 1/2000. Not independently checked.
- 22 Oct, coordinator (not yet checked by a second member). The explainer page `slot_model.html` now states the
  slot model with the paper's class model (prior `π`, value distributions `G_j`; the investor sees the class).
  A buy has likelihood ratio `1 + u`, so `m(π) = π/(π + (1 − π)(1 + u))` and `M(π) = π(1 + u)/(π(1 + u) + 1 − π)`;
  with `1 + u = e^{2/b}` these equal the paper's Laplace bounds at every prior. Prop. 2 holds under
  `Δ_0 < k`, `π < τ_1 < M < τ_2`, `π < τ_2`, `ρΔ_i min{1 − M, m} > k` (i = 1, 2), with
  `E_1 = ρ + (1 − ρ)(πλ + b)` and `O_H = π[ρ + (1 − ρ)(λ + b)]W_H(F_1)`. With other benchmark inputs fixed, all three
  parts hold for `π ∈ (0.475475, 0.508073)` (calibration A) and `(0.467850, 0.500424)` (calibration B, the paper's
  own Laplace range) (`scripts/_coordinator/slot_prior.py`). No trade iff `ρΔ_T max{π, 1 − π} ≤ k`; `r_A` solves
  `Δ_T(1 − τ) = k` for every prior; interior branch `E = ρ + (1 − ρ)(1 − π)bΔ_T/k`.
- 22 Oct, independent opinions (`opinions/`; neutral brief `opinions/BRIEF.md`; reviewers were barred from every
  synthesis, ledger and recommendation file). Main-text picks: R1 order slot (E), second Laplace (A) in an appendix;
  R2 E, second discrete Laplace (I), Laplace appendix; R3 E, second A; R4 A reframed as the score-bounded noise
  class, second E as an appendix robustness section. All four: medium confidence. The coordinator's view (E main,
  A appendix) was sealed in `opinions/coordinator_view.md` before the reviewers started.

## Phase 1: literature and theory (parallel)

| ID | Task | Output | Status |
|---|---|---|---|
| L1 | Literature: microstructures in models with corporate decisions (browser) | `memos/L1_survey.md` | done |
| L2 | Taxonomy of methods and their properties for this mechanism (no browser) | `memos/L2_taxonomy.md` | done |
| T1 | EGJ two-sided menu, three-point noise, presence `λ < 1` | `memos/T1_egj_two_sided.md` | done |
| T2 | Liquidity or uninformed trader of the informed order's size | `memos/T2_liquidity_trader.md` | done |
| T3 | Buy-only menu with bounded-noise variants | `memos/T3_buy_only_bounded.md` | done |
| T4 | Buy-only menu with one-sided noise in the order's direction (L2's flag; Edmans 2009) | `memos/T4_one_sided_noise.md` | done |
| T5 | T2's slot device plus T3's concentrated noise `(θ, 1 − 2θ, θ)`, buy-only | `memos/T5_slot_plus_noise.md` | done |
| T6 | T1's two-sided candidate plus T2's slot device | `memos/T6_two_sided_slot.md` | done |

## Phase 2: one independent check of the best candidate

| ID | Checks | Output | Status |
|---|---|---|---|
| X | T2 variants V3 buy and V3 two (one order slot: informed with probability `λ`, else a same-size liquidity trader) | `memos/X_check.md` | done |

## Phase 3: synthesis

`memos/SYNTHESIS.md`: what is conventional (with counts), the recommended setup, its knob, what it
reproduces and what it loses. Status: done. Recommended: T2 V3 two-sided (one order slot, informed with
probability `λ`, else a same-size liquidity trader; no separate noise). Alternative: the same slot with EGJ's
equal-weight noise on top. Spot-checks confirm the T6 trade-off and the T4/T2 threshold equivalence.

## Phase 4: extensions under the order slot (23 Oct)

Brief: `EXTENSIONS_BRIEF.md`. Decision rule: if an extension fails under the slot, keep Laplace in the main text.

| ID | Extensions | Output | Status |
|---|---|---|---|
| E1 | general-prior Prop. 2; X2 value classes and priors; X5 access to prices; X6 payment rule; X7 reserves | `memos/E1_auction_side.md` | checked |
| E2 | X1 fixed-information control; X3 atomless costs; X4 private signals; general-prior coexistence | `memos/E2_information_side.md` | checked |
| XE1 | check of E1 | `memos/XE1_check.md` | done |
| XE2 | check of E2 | `memos/XE2_check.md` | done |

## Phase 5: new extensions in the slot set-up (23 Oct, parallel to Phase 4)

Brief: `NEW_EXTENSIONS_BRIEF.md`. Only N1 may use the shared browser.

| ID | Direction | Output | Status |
|---|---|---|---|
| N1 | observables: spread, price impact, informed share, order imbalance, event studies | `memos/N1_observables.md` | done |
| N2 | dynamics: several slots, random arrivals, timing of preparation | `memos/N2_dynamics.md` | done |
| N3 | order size choice (Easley–O'Hara) and endogenous research (Dow–Gorton) | `memos/N3_size_research.md` | done (rerun; the first attempt stopped early and was cancelled) |
| N4 | strategic traders: manipulation, challenger or incumbent trading, liquidity foundation | `memos/N4_strategic_traders.md` | done |

E1 returns (23 Oct). The coordinator's general-prior Prop. 2 (22 Oct note) was wrong: it omitted
`B_{F_0}(π) < c_H` (counterexample: weak entry one). Corrected hypotheses: `B_0(π) < c_H < B_1(M)`,
`Δ_0 < k < ρ min{m, 1 − M} Δ_1`, `B_2(M) < c_H`; ownership rises iff `[ρ + (1 − ρ)(b + λ)]W_H(F_1) > ρW_H(F_0)`.
The all-strategy bound `m ≤ μ ≤ M` needs `β ≤ 1/3` (A and B satisfy it). The explainer page must be corrected.
Verdicts: two-class value classes and priors hold (all paper examples work with paper costs and strengths);
payment rule holds; access to prices holds in the recruiting region; reserves hold with change (flat entry at
the paper's exclusion reserve; `p = 1.55` restores deterrence but excludes the weak incumbent); the paper's
many-class price statement FAILS (exact three-class equilibrium with two posteriors at one price); a restricted
two-group result holds. Under the strict rule, the unchanged slot does not pass. Check XE1 started.

E2 returns (23 Oct). No information-side extension fails. X1 holds with changed wording: frozen full-order
entry is flat under the slot (0.522757 under B, 37/68 under A), so the paper's "falls" must read "does not
rise". X3 atomless costs hold (strong entry 0.522757 under B; part (iii) at 3.6 fails with the declared cost
law, as under Laplace, and the paper does not claim it). X4 complementary signals hold (entry 0.85 → 0.879797,
ownership 0.425 → 0.449238; same six grid pairs as the paper, all with d > a). Coordinator coexistence formulas
corrected: no trade needs `π < τ(r)`; `r_A` formula holds only for priors in about (0.396, 0.641) under B (empty
coexistence at π = 2/5 under A); interior-branch entry exact on `r_A < r < r_F(π)`. Check XE2 started.

XE2 returns (23 Oct): X1, X3, X4 CONFIRMED (exact fractions for A, 70-digit arithmetic for B). Coexistence
formulas CONFIRMED WITH CORRECTION: include the lower prior boundary under C1/IM; the prior interval
(0.396, 0.641) concerns the common endpoint `r_A`, and other priors permit coexistence that starts later; the
interior formula needs its branch conditions. XE2 also notes a display error and small Laplace quadrature errors
in E2 (see `memos/XE2_check.md`).

N2 returns (23 Oct). (C) One informed unit with a choice of date: all likelihood ratios stay in [1/(1+u), 1+u]
for any number of slots, so the return to the floor at 3.6 survives (analytical); with entry feedback the
good-news buyer trades early to be seen and the bad-news seller delays (analytical, buy-only); two slots give
first-date orders (1, −0.167), entry 91/204 (computer-assisted): the paper's (1, −v) returns as a timing pattern.
(A) n slots with fresh informed arrivals: 0.871 ≤ n ln(1+u) < 1.002 (u_n ≈ 0.93/n); extra entry at 3 falls like
e^{−0.306n}; the floor at 3.6 caps total informed volume before the decision. (B) Two slots: the opening price
prices in future entry; early informed traders earn 12.8% more from entry triggered by later trades; rising entry
at 1.55–1.65 is not restored (general obstacle, analytical). (D) Poisson arrivals: entry at 3.6 stays above the
floor at every rate (the return fails). Not independently checked.

N4 returns (23 Oct). N4.1: an uninformed holder with a stake never sells and buys only where its purchase
recruits (analytical); at r = 3 the outcome is unique below Ω₂ = 376/1425, coexists with two manipulation
outcomes up to Ω₁ = 136/475, and above Ω₁ only a challenger-mixing outcome exists; manipulation raises proceeds,
moves the challenger's rent to shareholders, and destroys most of the discovery surplus. With a holder stake in
[0.133, 0.183) and challenger mixing (CM), the unique informative equilibrium at 1.55, 1.60, 1.65 has strictly
rising entry next to no trade (computer-assisted). N4.2: a challenger in the slot abstains where the price
recruits and buys where it does not; its high-cost type sells; above presence 352/3417 a second equilibrium
crowds out the informed purchase. N4.3: the incumbent never buys where the price recruits; jams discovery only
above presence 0.0765. N4.4(a): the slot's liquidity trader is the reduced form of a holder with liquidity shocks
and a small stake (analytical); (b) price-sensitive participation softens the ceiling, two equilibria on
r ∈ [3.11, 3.78]. Not independently checked.

XE1 returns (23 Oct): all six E1 claims CONFIRMED (E1's script output byte-identical). The missing condition
`B_0(π) < c_H` is already in the paper's own Prop. 2 hypotheses. The paper's sufficient ownership condition
carries over only when `b + λ > 1/2` (exact counterexample otherwise). The many-class failure is a knife-edge:
a ±1/1000 change separates the prices; the pooled flows have equal gross profit, so entry is unchanged; it
disappears if the challenger sees the order. Excluding the weak incumbent at `p = 1.55` is forced (grid scan).
Section 6.1's break-even trade scale becomes about 6.85 instead of 1.83. Judgment: literally the slot fails the
rule (many-class sentence; strict deterrence at the paper's reserve), but neither failure is material; two
sentence rewrites fix them. The real cost: slot entry moves in steps, so every strict entry comparison at fixed
orders becomes flat (also X1 and X3's levels).

N3 returns (23 Oct). (B, analytical) Costly research with a success ceiling 6/17: zero research unique at 1.2;
at 1.55, 1.60, 1.65 research success 0.2502 → 0.2933 → 0.3326 and entry 0.5313 → 0.5367 → 0.5416 (strictly
rising, strict purchase after good news, no investor mixing), with zero research also an equilibrium; at 3 and
3.6 research at the ceiling uniquely, entry 0.5441 and 0.25; price access raises proceeds and surplus at 3.
(A, computer-assisted) Size choice restores a rising branch and smaller expected sales, but another equilibrium
keeps extra entry at 3.6. (C) Without the ceiling, floor entry at 3.6 is impossible at the same cost.

Ranking of new extensions for checks: (1) N3-B research with a ceiling; (2) N4.1 manipulation by a holder
(rising entry for stakes in [0.133, 0.183) with CM); (3) N2-C informed timing (partial sale as timing); (4) N4.4(a)
liquidity foundation; (5) N1 observables. Checks started: XN3, XN4, XN2.

| ID | Checks | Output | Status |
|---|---|---|---|
| XN3 | N3, Extension B first | `memos/XN3_check.md` | done |
| XN4 | N4.1, N4.4, N4.2–N4.3 | `memos/XN4_check.md` | done |
| XN2 | N2, Extension C first | `memos/XN2_check.md` | done |

XN2 returns (23 Oct). C: CONFIRMED WITH CORRECTION — the cap, floor entry and the reported equilibrium hold,
but another equilibrium has a late buyer and an early-sale probability of 0.837634, so the date-order prediction
is not general; the buy-only list is complete, the two-sided list is not. A: CONFIRMED WITH CORRECTION (0.93 is
one admissible choice; 0.306 is a conservative bound). B: CONFIRMED WITH CORRECTION (12.8% is a spread share;
early expected net profit is 45.5% higher; the long-horizon impossibility is unproved). D: CONFIRMED.

XN4 returns (23 Oct). N4.1 CONFIRMED WITH CORRECTION (the holder never sells; both stake thresholds hold;
endpoint counts and holder profits corrected; proceeds rise only near the onset of manipulation). The recovered
rising-entry result is REFUTED as unique: the rising branch exists, but another informative equilibrium survives
throughout the stake window. N4.4(a) CONFIRMED WITH CORRECTION (forced liquidity shocks implement V3; the
general uniqueness claim fails). N4.4(b) CONFIRMED WITH CORRECTION (two equilibria on (3.1106, 3.7839] under C1;
CM adds a third). N4.2 CONFIRMED WITH CORRECTION (352/3417 marks full suppression; multiplicity starts above
0.0804). N4.3 REFUTED as a threshold claim (corrected floor branch above 0.0599; counterexample at 0.06).

XN3 returns (23 Oct). N3 Extension B CONFIRMED (N3's output byte-identical; every tested number matches).
Model coherent, with two wording fixes (the ceiling caps the informed share of slot orders; research removes
liquidity cover because a failed search is replaced by a liquidity trader, as in Dow–Gorton). Zero research unique
at 1.2; at 1.55, 1.60, 1.65 research success 0.2502, 0.2933, 0.3326 and entry 0.5313, 0.5367, 0.5416 with a
strict purchase, zero research coexisting; the list is complete (two equilibria under C1; CM adds a falling
branch). At 3 and 3.6 research at the ceiling is unique (= calibration A): entry 37/68 then 1/4. Price access
+113/408 proceeds, +5/68 surplus at 3. Without a ceiling below 2686/7363, no research cost gives unique
recruitment at 3 with floor entry at 3.6 (new). Robustness: the ceiling must lie in (0.3166, 0.3648); the rising
branch needs the research cost a in about (0.0155, 0.0333); the quadratic cost is an added assumption.

Coordinator summary (23 Oct): the slot with costly research (Dow–Gorton) reproduces Prop. 2 with unique outcomes,
coexistence with strictly rising entry at 1.55, 1.60, 1.65, and the welfare result, all checked; every old
extension holds in substance under the fixed-λ slot (checked), with wording changes. Remaining losses: the
partial sale (1, −v) (only as one timing equilibrium, N2), strict fixed-information decline, strict deterrence at
the paper's reserve. The old extensions have not been re-checked with endogenous research.

