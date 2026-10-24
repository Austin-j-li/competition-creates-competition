# Opinion R2: the trading block for the main text

## 1. Pick

Use candidate E, the order slot of Dow and Gorton (1997): one unit order per opportunity, filled by the informed investor with probability λ and otherwise by a same-size liquidity trader who sells, waits, or buys; a two-sided menu; a competitive price; no separate noise.

## 2. Second choice and the appendix

Second choice: candidate I, the discrete Laplace law with two-sided unit orders. It reproduces the paper's exact bounds, ceiling, and no-trade boundary at c_H = 6 (analytical; checked), but it has no precedent, and it keeps a Laplace law.

Keep the current Laplace analysis (A) as an online appendix on continuous orders. It is already proved, and it is the only version in which the partial sales and the certified upward triple survive. Add one remark: EGJ's additive noise can join the slot with the same qualitative results (F; computer-assisted; unchecked).

## 3. Reasons

- The mechanism needs a bounded posterior at the flow that recruits the expensive challenger. With bounded additive noise and unit orders, the top flow reveals class H, so entry cannot return to ρ at 3.6 for any presence probability, weights, or cost (analytical). This rules out C and D, whatever the author's wish. E is the smallest step from EGJ: its liquidity-shock reading of λ, where the shock makes the slot trade instead of stay empty.
- E has the strongest proofs. All three parts of Proposition 2 hold with unique outcomes on an open strip, by two bounds and no derivative argument. Coexistence holds on [1.394, 1.748], which contains 1.55 to 1.65, and every outcome in that range is classified (analytical; checked). The welfare result at strength 3 is analytical. No off-path belief is needed on the unit menu.
- E has the best precedent and the clearest knob. The arrival device is verified in Dow–Gorton and matches the Glosten–Milgrom structure. The top posterior is M = (1+u)/(2+u) with u = λ/[(1−λ)β], an informed-share statistic. G needs a box of width 0.001 (reject). H uses noise that only buys, which does not fit a target whose shareholders sell; its entry is 0.763.
- The narrow λ band comes from two fixed strengths: it is exactly τ(3) < M < τ(3.6). The paper's own Laplace M = 0.731059 sits 0.0003 below τ(3.6), because the paper set 3.6 just above its ceiling 3.5927. Any device has the same freedom: choose M, then set r_2 above r_C(M).
- The exogenous liquidity motive is the standard assumption of Dow–Gorton, Glosten–Milgrom, and EGJ's own noise traders. A free uninformed trader would not trade (analytical; checked). State the motive; do not derive it.
- The rewrite is mostly a deletion: the global order bound, the interval certificates, and the noise-class apparatus leave the main text. Entry at strength 3 is 0.544 against 0.523 now.

## 4. Main weakness and how to present it

Entry is a step function of strength. On the informative branch at 1.55 to 1.65 it is flat at 0.544; the branch where entry rises lives only on [1.394, 1.461) and needs investor mixing. The partial-sale pattern (1, −v) does not appear. Present Proposition 3 as analytical coexistence on an interval, with entry on the informative branch above the no-trade entry. Drop the three-strength order, or move it to the Laplace appendix. State the unit menu, because a fractional deviation would need an off-path belief at 3.6 (checked). Use β below one half, so that the zero flow stays on path.

## 5. What would change my mind

- The author ranks the partial-sale asymmetry and the certified upward triple as headline results. Then keep A in the main text and put E in an appendix.
- The open extensions (dispersed classes, a general prior, private signals, atomless costs, the reserve comparison) fail under E.
- An independent check overturns the slot classification, or no stated belief rule handles the continuous-order deviation at 3.6.
- The author drops the return to ρ as a result. Then D becomes viable, though it needs investor mixing and unprecedented noise weights.

## 6. Confidence

Medium.
