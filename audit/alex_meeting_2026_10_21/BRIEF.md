# Shared brief: supervisor meeting of 21 October 2026

Read this file before you start. It holds the model summary, the
supervisor's four points, the fixed specifications for each workstream, the
memo format, and the rules. Your own task prompt names your workstream and
your memo file.

Repository root: `/home/uctpiaj/work/Projects/competition-creates-competition`
(below, paths are relative to this root).

## 0. Rules (all members)

1. Do not edit anything under `overleaf/`, `paper/`, `numerics/`, `figures/`,
   `tables/`, or any other existing project folder. Write only your own memo
   file under `audit/alex_meeting_2026_10_21/memos/` and your own scripts under
   `audit/alex_meeting_2026_10_21/scripts/<your memo stem>/`.
2. Do not commit, push, branch, or stash. Do not run `git` commands that
   change state.
3. Do not write tests of any type. Do not add test files, fixtures, or
   frameworks. A short script that computes and **prints** a result is
   allowed. A script with assertions is a test: do not write it.
4. Do not save downloaded files anywhere (no PDFs, no data). Read web pages
   and papers online only. If a tool saves a download automatically, do not
   copy it into the repository.
5. Use `.venv/bin/python` (numpy, scipy, mpmath are installed; sympy is not).
   Do not install packages. Use mpmath when precision matters.
6. Do not name AI models, agents, or tools in your memo. Write as a research
   memo to the author.
7. State the status of every claim with the paper's vocabulary:
   **analytical** (you proved it), **numerical diagnostic** (you computed it),
   **conjecture** (you believe it but did not prove it), **open**. Show the
   derivation for every analytical claim. Do not hide a gap. A failed attempt
   is a useful result: report it.
8. Cite literature only when you checked the source. Give author, year,
   journal, and the specific section or result. Mark any reference you could
   not verify as "unverified".

## 1. The current model (Overleaf master `overleaf/paper/main.tex`)

Read Sections 2–4 (lines 219–822) and Appendix A.1–A.2 (lines 1254–1660) for
the full text. The summary:

- Target standalone value 0. Values and costs are per share. All agents are
  risk neutral.
- **Incumbent** (already prepared, no further cost): value `R ~ U[0, r]`,
  private to the incumbent. Larger `r` = stronger incumbent (FOSD).
- **Challenger**: value `θ ∈ {ℓ, h}`, prior 1/2 each, with `0 < p < ℓ < r < h`
  (eq. 1). The challenger does not know θ. After it observes the price, it
  learns its preparation cost `C ∈ {c_L, c_H}`, with `Pr(c_L) = ρ`,
  `0 ≤ c_L < c_H`. Paying C reveals θ and lets it bid. C is independent of
  everything.
- **Sale**: cash second-price auction with reserve `p`. Truthful bids are
  weakly dominant.
- **Investor**: observes θ perfectly, no initial position, order
  `q ∈ [-1, 1]`, linear trading cost `k|q|`, profit `q(V_T − P) − k|q|`.
- **Noise**: `Z` Laplace, density `f(z) = e^{−|z|/b}/(2b)`, `b > 1`.
  Flow `X = q + Z`.
- **Market makers**: competitive, `P(X) = E[V_T | X]`, anticipating entry.
- **Timing**: sale rule announced → investor learns θ and trades → price set
  → challenger sees price and its cost, decides to prepare → prepared bidders
  bid truthfully → payoffs.

Auction objects (eq. 4), uniform incumbent:

```
t_0 = p(1 − p/r)                 (target proceeds without entry)
t_H = r/2 + p²/(2r)              t_L = ℓ − (ℓ² − p²)/(2r)
g_H = h − r/2 − p²/(2r)          g_L = (ℓ² − p²)/(2r)
Δ_T(r) = t_H − t_L = (r − ℓ)²/(2r)    (target-payoff spread)
B_r(μ) = g_L + μ(g_H − g_L)            (gross challenger profit at belief μ)
```

Proposition 1 (general continuous incumbent cdf F on [0, r̄]):
`Δ_T(F) = E_F[(R − ℓ)_+] = ∫_ℓ^r̄ [1 − F(u)] du` rises under an FOSD
strengthening; `G_θ(F) = E_F[(θ − max{p, R})_+] = ∫_p^θ F(u) du` falls.

Posterior bounds (eqs. 7–8): for any mixed orders on [−1, 1], the Laplace
likelihood ratio of any two orders lies in `[e^{−2/b}, e^{2/b}]`, so the
flow posterior satisfies `m ≤ μ_X ≤ M`, with `m = 1/(1 + e^{2/b})`, `M = 1 − m`.

Entry and price (eq. 9), when `c_L < B_r(m)`:
`e_r(μ) = ρ + (1 − ρ)·1{B_r(μ) ≥ c_H}`,
`P_r(μ) = t_0 + e_r(μ)[t_L − t_0 + Δ_T μ]`. The price is strictly increasing
in μ, so it reveals μ (price sufficiency, Prop. A.2).

Residual advantages (eq. 11): `A_H = e Δ_T (1 − μ_X)`, `A_L = e Δ_T μ_X`,
bounded by `ρ m Δ_T ≤ A ≤ Δ_T`. Note that `t_0` and `e·(t_L − t_0)` cancel
from the investor's residual.

Global order bound (A.6): `|f′| ≤ f/b` gives
`U′(s) ≥ (1 − s/b) F(s) − k ≥ (1 − 1/b) ρ m Δ_T − k`.

Proposition 2 (main result). Fix `0 < p < ℓ < r_0 < r_1 < h`, and assume
- (A1) `0 ≤ c_L < B_{r_1}(m)`;
- (A2) `B_{r_0}(1/2) < c_H < B_{r_1}(M)`;
- (A3) `Δ_T(r_0) < k < (1 − 1/b) ρ m Δ_T(r_1)`.

Then (i) at r_0 the unique outcome is no trade, entry ρ; (ii) at r_1 the
unique outcome is full orders (1, −1), an informative price, entry above ρ,
and a higher probability of high-value ownership; (iii) at a strong enough
r_2 the orders stay full but entry returns to ρ.

Closed forms under full orders (eq. 12):
`τ = (c_H − g_L)/(g_H − g_L)`, `x* = (b/2) log(τ/(1 − τ))`,
`α_H = 1 − ½ e^{(x* − 1)/b}`, `α_L = ½ e^{−(x* + 1)/b}`,
`E = ρ + (1 − ρ)(α_H + α_L)/2`, `O_H = ½[ρ + (1 − ρ) α_H]`.

Prop. A.3: at a fixed information experiment, a stronger incumbent weakly
lowers entry (deterrence). Prop. A.4: no trade is an equilibrium iff
`ρ Δ_T(r)/2 ≤ k`.

Benchmark vector (Appendix A.8):
`(h, ℓ, p, ρ, c_L, c_H, b, k) = (10, 1, 0.5, 0.25, 1, 6, 2, 0.02)`,
`(r_0, r_1, r_2) = (1.2, 3, 3.6)`. Reported values: entry 0.25 → 0.522757;
high-value ownership 0.125 → 0.324192; at r_2 entry 0.25.
Moderate vector: `(2, 1, 0.5, 0.25, 0.3, 0.89, 2, 0.002)`, `(r_0, r_1) = (1.05, 1.5)`.

Existing material that is relevant to the four points:
- Section 6.3 (lines 1040–1050): **value classes**. Quality identifies a low
  or high value class (prob. 1/2 each); values are uniform around ℓ and h
  with half-width 0.05; the investor observes the class; preparation reveals
  the exact value. This is a first version of point 1.
- Section 6.1 (lines 958–967): the **dividend-invariance diagnostic**. A
  deterministic dividend added to the traded claim shifts V_T and P by the
  same amount and leaves trading, entry, and seller revenue unchanged. This
  is relevant to point 3.
- Section 5.1: logistic noise also works, because its log-density derivative
  is bounded by 1/b.
- Section 5.3 / A.5: complementary private signals.
- Lines 1254–1400: Prop. 1 proof, Prop. A.1 (posterior bounds), Prop. A.2
  (price sufficiency).

## 2. The supervisor's four points (verbatim from the author)

> 1. the distribution of the challenger of being high and low with 1/2 of the
> prob. This is unconventional. He said since this is second price auction,
> asymmetric info wouldn't cause too much of a headache. it'd be a nice idea
> to model such that the challenger before entering will be choosing from a
> few different distributions, and only when they receive information can
> they actually know what distributions they end up at, this will change a
> lot of the technical details but is worth exploring to see whether a clear
> neat result can be derived.
>
> 2. for the microstructure, laplace density of the noise trade is largely
> unconventional. we need to provide very very clear justification for it
> from both technical (for a clean linear posterior that gives rise to a clean
> eqm) and economic perspective. we should also explore the possibility of
> modelling the microstructure in a purely discrete setup like the edmans
> paper and a few others (more conventional than laplace). for the discrete
> trading menu we can shut off either the short or long such that the trading
> is one directional, so that when we deal with the eqm proof the out of the
> support strategies will not be too tricky to discuss. (the bayesian
> updating mechanism will remain similar.)
>
> 3. we have a t_0, target proceedings when no entry happens, this leads to a
> question that asks who the investors really are: if they are the target firm
> shareholders, shouldn't they benefit from the stock price change
> nonetheless, if they are outsiders, who can they be? is there any modelling
> device we should introduce to patch up this part of the story?
>
> 4. for the low/high cost, can we normalize c_L to be 1 and simplify some of
> the calculation?

## 3. Fixed specifications (so that paired derivations can be compared)

### 3.1 Point 1: challenger value distributions

Two readings of "choosing from a few different distributions" exist. Report
under the reading your task names; do not decide for the supervisor.

- **Reading N (nature draws the distribution; main line).** The challenger's
  type is `j ∈ {H, L}` with prior `π ∈ (0, 1)` (not necessarily 1/2). Given
  j, the value θ is drawn from cdf `G_j`. The challenger knows neither j nor θ
  before preparation. The investor observes **j** (the distribution), not θ.
  Preparation reveals θ. The incumbent is as in the paper (general cdf F, with
  the uniform as the leading case). Main ranking assumption: `G_H` first-order
  dominates `G_L`; also report what weaker ranking suffices. Supports may
  overlap and may include values below the reserve p.
  - Extension N2: `J > 2` types with prior vector π.
  - Extension N3: the investor observes θ itself instead of j.
- **Reading C (the challenger chooses).** Before preparation, the challenger
  chooses one distribution from a menu (for example, an integration plan with
  a given risk profile). It learns the realized value only after it receives
  information (diligence). Examine what the auction implies for that choice
  and for the traded claim.

Discriminating checks to verify (not given answers):
- Does the target-payoff spread between types take the form
  `∫ [1 − F(θ)] [G_L(θ) − G_H(θ)] dθ`, and the profit gap the form
  `∫ (∫_p^θ F(u) du) d(G_H − G_L)(θ)`? If so, does Prop. 1 generalize with the
  same sign pattern under an FOSD strengthening of F?
- With J > 2: Prop. A.2 recovers a one-dimensional statistic from the price.
  Does the price still identify the statistic that the entry decision needs?
  Or do target proceeds and challenger profit load on different linear
  functionals of the belief vector? Under which condition on
  `{(t_j, g_j)}` does sufficiency survive?
- What happens to the posterior bounds `m, M` with a general prior π?

### 3.2 Point 2: microstructure

**Laplace justification.** Map each property of the Laplace density to the
proof step that uses it: eq. (8) bounded likelihood ratio → posterior bounds;
`|f′| ≤ f/b` → global order bound (A.6); piecewise-linear log-odds under full
orders (A.8) → closed forms (12); posterior plateaus with positive mass → tie
rule at r_C (A.14). Identify the general class of noise laws for which each
step holds, and what is lost outside the Laplace case. Check the textbook
facts: the difference of two independent exponential variables is Laplace;
a normal variance mixture with exponential mixing variance is Laplace;
Brownian motion at an independent exponential time is Laplace.

**Discrete model (pinned).** Use this common base so that the two builders'
results compare:
- Noise trader: `z ∈ {−1, 0, +1}` with probabilities `(π_−, π_0, π_+)`. The
  leading case is equal probabilities 1/3 each (Edmans, Goldstein and Jiang,
  2015, AER, Section 2.2). Also report the general case.
- Investor: always present in the leading case. Also report the extension in
  which the investor is present with probability λ ∈ (0, 1), as in Edmans,
  Goldstein and Jiang (2015).
- **Buy-only variant:** `q ∈ {0, 1}` (short sales shut off).
  **Sell-only variant:** `q ∈ {−1, 0}` (purchases shut off).
  Mixed strategies over the two actions are allowed.
- Flow `X = q + z`; market makers see X; `P(X) = E[V_T | X]`.
- Trading cost `k > 0` per unit traded; an indifferent investor does not
  trade (state if a different tie rule changes a result).
- The challenger observes the **price** (as in the paper), not X. Check
  whether two flows can share a price and what that does.
- Entry, auction, costs, and values as in Section 1 of this brief.
- Off-path flows: state the belief rule you use (for example, the Intuitive
  Criterion, as in Edmans, Goldstein and Jiang 2015, or D1), and show which
  results depend on it.

Discriminating checks to verify:
- With a small noise support, extreme flows reveal the state, so the `m, M`
  machinery collapses. At a revealing flow the investor's residual is zero.
  Handle revealing flows explicitly, and state which flows reveal the state
  in each variant and each equilibrium.
- With equal noise probabilities, check whether interior flows carry any
  information at all. If they do not, information comes only from revealing
  flows. Report what a general `(π_−, π_0, π_+)` adds.
- Does a Prop. 2 analog hold: (i) unique no trade at r_0, (ii) unique trading
  equilibrium with entry above ρ at r_1, (iii) entry back to ρ at r_2? Are
  the no-trade and trade regions separated by one cutoff, or do they overlap
  (multiplicity, as in Prop. 3)?
- Does the fixed-experiment control (Prop. A.3) carry over?

### 3.3 Point 3: who the investors are, and t_0

Baseline facts: the investor has no initial position; `t_0` cancels from the
residual advantage (eq. 11 and the proof of Prop. A.2).

**Stake extension (pinned).** The informed investor holds an initial stake
`ω ≥ 0` shares and has payoff `ω V_T + q(V_T − P) − k|q|`. Note
`t_L > t_0` (entry raises proceeds even with a low-value challenger). Check
whether an investor with information L now wants to buy to induce entry, and
find the ω at which each part of Prop. 2 fails. Kyle and Vila (1991, RAND
Journal of Economics) is the nearest antecedent on camouflaged trading
before a takeover; Edmans, Goldstein and Jiang (2015, Section 3.5 and
Appendix B.2) treat a positive initial stake.

Questions to answer: who are the informed investors, the noise traders, the
market makers, and the holders who receive V_T? Do target shareholders gain
from price-induced entry? Which modelling device best closes the gap in the
story?

### 3.4 Point 4: normalization

Facts to verify: `c_L` appears only in condition (A1) (and in the weaker
floor variants of Section 4.1), not in eq. (12). Only one monetary unit can
be normalized; the benchmark already uses `ℓ = 1`, and also has `c_L = 1`.
The flow unit is fixed by the order bound `|q| ≤ 1`, so `b` is in flow units.
Compare `c_L = 1` (a unit choice), `c_L = 0` (removes A1), `p → 0`
(removes t_0), and other normalizations.

## 4. Memo format

Write Markdown with LaTeX math (`$…$`). Use these sections in this order:

1. **Question and reading** (which question, which reading or variant).
2. **Formal setup** (all assumptions, notation consistent with the paper).
3. **Results** (numbered claims, each with a status label and a derivation).
4. **What changes relative to the current paper** (which propositions,
   equations, and proof steps survive, change, or fail).
5. **Numerical example** at the benchmark vector (or a stated variant), with
   the script path. Print-only scripts.
6. **Open issues and risks.**
7. **Recommendation** (what the author should do, in priority order).
8. **Plain summary** (at most 300 words, for a reader who is not a theorist).

Write clearly. Use short sentences. Prefer simple words.
