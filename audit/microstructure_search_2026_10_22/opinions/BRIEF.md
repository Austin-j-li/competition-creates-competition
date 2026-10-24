# Request for an independent opinion: which trading microstructure should this paper use?

You are an outside reviewer with expertise in economic theory (market microstructure, feedback effects,
auctions, corporate finance). Give your own judgment. Other reviewers answer the same question
separately; you will not see their answers, and they will not see yours.

## 1. The paper

"Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders". Read the current
version at this commit (read-only):

- `git -C overleaf/paper show 01bd5d6:main.tex`
- `git -C overleaf/paper show 01bd5d6:online_appendix.tex`

In short: a target is sold by a second-price auction with a reserve. An incumbent bidder is present.
A challenger of quality class `j ∈ {H, L}` (prior `π`, values drawn from `G_j`) must pay a preparation
cost to bid (zero with probability `ρ`, else `c_H`). Before it decides, an informed investor who knows the
class trades the target's stock; competitive market makers set the price from order flow; the challenger
sees the price. A stronger incumbent raises the spread of target proceeds across classes, which
raises the return to informed trade, which makes the price more informative, which can raise entry
("competition creates competition"). Main results: Prop. 2 (no informed trade and entry at the floor
`ρ` against a weak incumbent; informative trade and higher entry against a strong one; entry back at `ρ`
against a very strong one, while trade stays informative), Prop. 3 (no trade and informative equilibria
coexist at intermediate strengths; the paper certifies three informative equilibria with entry ordered
upward at strengths 1.55, 1.60, 1.65), and a welfare result (access to prices raises target proceeds
and net surplus). Benchmark: `h = 10, ℓ = 1, p = 0.5, ρ = 0.25, c_L = 0, c_H = 6, k = 0.02, π = 1/2`,
strengths `1.2, 3, 3.6`.

The current paper uses continuous orders `q ∈ [−1, 1]` with a linear trading cost and additive Laplace
noise (scale `b = 2`), justified in its Section 2 by three constructions.

## 2. The author's stated wish

"Laplace is an unconventional construct for this problem. I want to anchor more around the EGJ-like
microstructure setup [Edmans, Goldstein and Jiang 2015, AER]; we don't need to be 100% it. … Discrete
modelling should be a strong candidate, but is there a setup we can fine-tune to find our desired result
with comparable strength."

Give your honest view even if it disagrees with this wish.

## 3. Facts gathered so far

The facts below come from a team's working memos. Status labels: analytical (complete proof),
computer-assisted (exact or interval arithmetic), numerical diagnostic (floating point), open.
"Checked" means a second member reproduced it independently. The candidates are listed in no
particular order. You may read the underlying memos listed in §5 to verify any fact.

**Literature (15 corporate-finance models with a real decision, model sections verified):** Kyle-type
with normal noise 3; noisy rational expectations 3; EGJ/Goldstein–Guembel three-point noise 2; one-order
arrival (Dow–Gorton 1997: the informed trader or a same-size liquidity trader arrives, never both) 1;
one-sided exponential noise (Edmans 2009) 1; general density 1; other 4. None of the 15 uses Laplace
noise. The sample was chosen, not random.

**A structural fact (analytical).** With any noise of bounded support added to unit orders, the top flow
can come only from an informed purchase, so it reveals class H. At the benchmark a revealed class H still
recruits the high-cost challenger at strength 3.6, so entry cannot return to `ρ` there (Prop. 2(iii)
fails) for any presence probability, noise weights or trading cost.

**A second fact (analytical; spot-checked, not independently re-derived).** With unit orders at the
benchmark, the return to `ρ` at 3.6 requires the highest posterior to be at most 0.731, while an
EGJ-type informative branch with entry that rises across 1.55–1.65 needs a highest posterior above 0.755.

| Candidate | Specification | Holds | Fails or costs | Precedent | Checked |
|---|---|---|---|---|---|
| A. Current Laplace | continuous `q ∈ [−1,1]`, additive Laplace noise | all of Prop. 2 (entry 0.523 at strength 3), Prop. 3 with upward-ordered entry (computer-assisted), partial sales `(1, −v)`, welfare | unconventional noise law; continuous order sizes | none of the 15 sampled models | paper's own proofs |
| B. Kyle-type Gaussian noise | continuous orders, normal noise | coexistence (numerical diagnostic in an earlier discrete-Gaussian test) | the likelihood ratio is unbounded, so posteriors approach 0 and 1 and the return to `ρ` (Prop. 2(iii)) fails; outside the paper's score-bounded noise class | most common in the literature | — |
| C. EGJ block as is | unit orders `{−1,0,1}`, noise `{−1,0,1}` equal weights, presence `λ < 1` | Prop. 2(i)–(ii) (entry 0.5 at strength 3 once `λ ≥ 0.58`), welfare (analytical) | Prop. 2(iii) fails; coexistence only at one strength (knife-edge) | EGJ 2015, Goldstein–Guembel 2008 | no |
| D. EGJ with tuned noise weights | as C, noise weights (0.1, 0.8, 0.1), `λ = 0.7` | Prop. 2(i)–(ii) with the paper's `(1, −v)` pattern and entry 0.527; coexistence on [1.44, 1.80] with entry rising 0.419 < 0.450 < 0.484 at 1.55–1.65 (computer-assisted); welfare | Prop. 2(iii) fails; needs investor mixing (no equilibrium at strength 3 under EGJ's pure-strategy tie rule); unequal noise weights have no verified precedent | EGJ (weights changed) | no |
| E. Order slot | one order; informed with probability `λ`, else a same-size liquidity trader (sell, wait, buy with `β, 1 − 2β, β`); no separate noise | all of Prop. 2 with unique outcomes (analytical): entry 0.544 at strength 3 (a second calibration gives 0.523 and the paper's ceiling, numerical diagnostic); coexistence on [1.394, 1.748] (contains 1.55–1.65); welfare; no off-path beliefs on the unit menu | entry is flat across 1.55–1.65 (it rises strictly only on [1.394, 1.461), with investor mixing); no partial sale at 1.55–1.65; needs an exogenous liquidity motive; with continuous orders an off-path belief rule is needed; the working band for `λ` is narrow (0.317–0.365 at `β = 1/3`), which the benchmark strengths impose on any discrete version | Dow–Gorton 1997 (verified); also close to Glosten–Milgrom / PIN arrival models | yes |
| F. Order slot plus EGJ noise | E plus noise `{−1,0,1}` with equal weights | all of Prop. 2 (entry 0.35–0.5 at strength 3); coexistence from 1.557; a closed-form rising branch on [1.557, 1.609] | misses strength 1.55; lower entry | two verified parts; combination new | no |
| G. Order slot plus tuned noise | E plus noise weights (0.355, 0.29, 0.355), knobs tuned | all of Prop. 2; coexistence with entry rising at 1.55–1.65 (computer-assisted); welfare | works only in a parameter box about 0.001 wide; entry 0.38–0.49 at strength 3; prices need not rise with total flow | new | no |
| H. One-sided noise | buy-only; noise traders only buy (geometric or exponential) | all of Prop. 2 with the paper's exact ceiling at one parameter value; coexistence; welfare | entry 0.763 at strength 3; flat entry at 1.55–1.65; Edmans's noise runs opposite to the informed order, so the match is partial | Edmans 2009 (exponential; verified) | no |
| I. Discrete Laplace | unit orders `{−1,0,1}`; noise = difference of two geometric counts | all of Prop. 2 at the paper's `c_H = 6` with the paper's exact posterior bounds, ceiling and no-trade boundary (analytical); coexistence on [1.516, 1.748] | flat entry at 1.55–1.65; still a Laplace-type law | none in the sample | yes (earlier study) |

## 4. Your task

Write `audit/microstructure_search_2026_10_22/opinions/opinion_<ID>.md` (your reviewer ID, R1 to R4, is in
your task message), at most 700 words:

1. **Your pick for the main text** (one candidate from A–I, or your own design), in one sentence.
2. **Second choice**, and what, if anything, belongs in an appendix or a remark.
3. **Reasons** (at most six bullets): weigh conventionality, analytical strength, robustness (no knife-edge,
   no tuned box), how much of Props. 2–3 and the welfare result survive, economic plausibility of each
   device, and the cost of rewriting the paper.
4. **The main weakness of your pick**, and how the paper should present it.
5. **What would change your mind.**
6. **Confidence** in your pick: low, medium or high.

## 5. Rules

- Read-only, except your own opinion file. Do not commit. Do not hand the task to others. No browser or web search.
- You may read: the paper at commit `01bd5d6`; the memos `audit/microstructure_search_2026_10_22/memos/T1_egj_two_sided.md`,
  `T2_liquidity_trader.md`, `T3_buy_only_bounded.md`, `T4_one_sided_noise.md`, `T5_slot_plus_noise.md`,
  `T6_two_sided_slot.md`, `X_check.md`, `L1_survey.md`; and
  `audit/discrete_exploration_2026_10_21/memos/C1_two_sided.md`, `B_dlaplace_theory.md`, `A_three_point.md`.
- Do **not** read any synthesis, ledger, red-team memo, taxonomy short-list, report, explainer page, or any
  other file in the `opinions/` folder: `SYNTHESIS.md`, `LEDGER.md`, `RED_TEAM.md`, `L2_taxonomy.md`,
  `report.html`, `slot_model.html`, and other `opinion_*.md` or `coordinator_view.md` files. They contain
  other people's recommendations, and your opinion must be independent.
- Do not name AI models, agents or tools in your file.
- Write in plain English: short sentences, simple words.
