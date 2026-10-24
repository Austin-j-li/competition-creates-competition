# Opinion R1: trading microstructure

## 1. Pick for the main text

Candidate E: the Dow–Gorton order slot, with the two-sided unit menu, equal liquidity probabilities (1/3 each) and no separate noise.

## 2. Second choice, appendix and remarks

Second choice: A, the current Laplace model. It moves to an appendix.

- **Appendix.** The continuous-order model with score-bounded noise (Prop. A.5, the logistic comparison). It keeps what the slot loses: the interior partial sale, smooth entry, a strictly falling fixed-information control, and the certified triple at 1.55–1.65.
- **Main-text remark.** EGJ's exact block (C) gives Prop. 2(i)–(ii) and welfare (analytical). Only the return to ρ fails, because the top flow reveals class H. This explains why the slot replaces bounded additive noise.
- **Footnote.** Gaussian noise (B) loses the return to ρ.
- **Leave out** D, F, G, H and I. D needs investor mixing at strength 3. G holds only in a box about 0.001 wide. C, D, F, G and H are unchecked.

## 3. Reasons

- **The trade-off is forced.** With unit orders, the return to ρ at 3.6 needs a top posterior of at most 0.731; a rising EGJ-type branch at 1.55–1.65 needs more than 0.755. No discrete design keeps both without a tuned box. So the choice is which secondary feature to give up. Tuning to keep both reads as reverse engineering.
- **Conventionality.** An informed order or a same-size liquidity order is the device of Dow–Gorton (1997), a feedback paper, and of Glosten–Milgrom and PIN models. It keeps EGJ's {−1, 0, 1} menu and presence probability.
- **Analytical strength.** All of Prop. 2 holds in exact fractions, with one equilibrium under every tie rule: entry 1/4, 37/68, 1/4. Coexistence holds on about [1.394, 1.748], from closed-form conditions. Welfare is analytical. Every flow is on path. All of this is checked.
- **Robustness.** The result holds on an open strip in (λ, β). The λ band is narrow, but the benchmark strengths cause this: the recruiting belief moves only 0.026 from 3 to 3.6. The Laplace scale b = 2 sits at the edge of the same band.
- **Survival.** Prop. 2, the ownership rise, the hidden-price control, welfare and coexistence survive. Entry at strength 3 is 0.544 (paper 0.523). In coexistence the low class abstains, so trade stays asymmetric.
- **Plausibility and cost.** The liquidity motive is exogenous, as in every noise-trader model. The rewrite is large (Sections 2.3–5.1, Figures 2–3, Appendix A.2–A.5, numerics), but proofs get shorter.

## 4. Main weakness and presentation

The slot model is proven only at its core. The extensions (dispersed classes, other priors, atomless costs, private signals, payment rule, reserves) are open under it. Its price experiment is also coarse: one order gives three prices, so entry moves in steps. Three results lose force:

- the upward triple at 1.55–1.65 (entry is flat there);
- the interior partial sale;
- the fixed-information control. By my arithmetic, 29/40 exceeds the recruiting belief at 1.2 (0.633) and at 3 (0.705). So frozen full orders give 37/68 at both: flat, not falling.

How to present it:

- Re-derive the extensions under the slot, or attach each to the continuous appendix and say so.
- Restate Prop. 3: no trade coexists with an informative equilibrium on [r_A, r_N]; branch entry rises strictly on [1.394, 1.461), then stays flat. Say that the investor mixes there in place of a partial order. Do not present it as the old result at new strengths.
- State the control as "fixed information cannot raise entry" (Prop. A.3).
- Make the unit menu the model, as in EGJ. Say that divisible orders need EGJ's off-path convention for part (iii).

## 5. What would change my mind

- An extension fails under the slot. Then keep A in the main text and give E a full section.
- The author treats the interior sale and the upward triple as core claims.
- The timetable cannot absorb a full rewrite.
- A discrete design gives rising entry at 1.55–1.65 on an open region, with prices monotone in flow.

## 6. Confidence

Medium. My pick agrees with the author's wish, but does not rest on it.
