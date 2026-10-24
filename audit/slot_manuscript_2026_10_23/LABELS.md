# Shared notation, equilibrium concept and labels for the three documents

Every writer and the figure workstream follow this file. It has priority over the proof packages where they differ.

## 1. Notation (the core package `proofs/P1_core.tex` is canonical, with one change)

- `σ_j(q)`: the class-j investor's order distribution on `{−1, 0, 1}`.
- `η(x)`: the liquidity trader's order law, `(β, 1 − 2β, β)`.
- `f_j(x) = (1 − λ)η(x) + λσ_j(x)`: the probability of order `x` in class `j`. (P1 writes `a_j(x)`; the
  documents use `f_j(x)` because `a` is the research cost.)
- `b = (1 − λ)β`, `b_0 = (1 − λ)(1 − 2β)`, `u = λ/b`, `M(π)`, `m(π)`, `κ = min{m(π), 1 − M(π)}`.
  Describe `u` as the informed presence mass relative to the liquidity mass in one direction; `1 + u` is the
  largest likelihood ratio of an order. Do not call `u` "the odds that an order is informed" (under full orders
  those odds are `πu` for a purchase and `(1 − π)u` for a sale).
- The seller's bargaining share in the payment rule (Section 7.2) is `ω`, not `η` (`η(x)` is the liquidity
  law). Write the spread response as "weakly has the sign of `1 − 2ω`; strictly when `ω ≠ 1/2` and `E[(R − ℓ)_+]` changes
  strictly". The row `ω = 1` is a payment-stage limit outside `0 ≤ ω < 1`.
- `b` is only `(1 − λ)β`. Do not use `b_R`, `b_θ` for bids; say "bids equal values" or use `\mathrm{bid}`.
- `A` is not used for three objects: keep `A_j = Pr_j(θ ≥ p)` if needed and name the preparation rule `e`.
  `D(v)` is the class CDF gap; do not use `D_0` for a dividend. `Γ` names one object only.
- Very small numbers print in scientific form (`4.787273 \times 10^{-7}`), never as `0.000000` or `e-7` text.
- `μ(x)`: the posterior after order `x`; `P(x)`: the price; the entry rule and the bids as in P1's tuple.
- Research: intensity `λ ∈ [0, λ̄]`, cost `(a/2)λ²`, conjectured intensity `λ̂`.
- Boundaries on the benchmark path: `r_A < r_F < r_N < r_J < r_S < r_1 < r_C < r_2`.

## 2. Equilibrium concept

- The investor may mix over its maximizers (rule IM). This is the equilibrium concept of the documents.
- The challenger prepares at indifference (rule C1) in the main statements. Where the challenger's rule CM
  (mixing at indifference) adds equilibria, a sentence or a remark says so.
- Proposition 2 holds under all four tie-rule pairs. Say so once, in Section 4.1.
- A pure selection in which the investor abstains at indifference (rule I0) has no equilibrium on
  `(r_N, r_S]`. One remark in Section 4.3 records this. (Pending the core check XP1.)

## 3. Labels

Main-text statements carry these labels. Appendix proofs open with
`\begin{proof}[Proof of Proposition~\ref{...}]`.

| Label | Statement | Section | Proof | Package |
|---|---|---|---|---|
| `prop:returns` | Proposition 1, payoffs and target value | 3.1 | A.1 | (done) |
| `lem:beliefs` | flow laws, full support, posterior bounds | 3.2 | A.2 | P1 Lemma 1 |
| `cor:exclusion` | high-cost preparation excluded under every profile | 3.2 | A.2 | P1 Corollary 1 |
| `lem:prices` | entry floor; the price reveals the posterior | 3.2 | A.2 | P1 Lemma 2 |
| `lem:trading` | informed trading: one comparison with `k` | 3.3 | A.2 | P1 Lemma 3 |
| `prop:ccc` | Proposition 2, competition creates competition | 4.1 | A.3 | P1 Prop. 2 |
| `prop:region` | the admissible region and the prior range | 4.2 | A.3 | P1 Prop. 4 |
| `prop:control` | the fixed-information control | 4.2 | A.6 | P4 R5 |
| `prop:coexistence` | Proposition 3, the equilibrium set on the benchmark path | 4.3 | A.4 | P1 Prop. 3, Lemmas 4–5 |
| `prop:priors` | coexistence at every prior | 4.3 | A.4 | P1 Prop. 5 |
| `prop:research` | research equilibria at the benchmark strengths | 5 | A.5 | P3 |
| `prop:researchbranch` | entry rises strictly along the research branch | 5 | A.5 | P3 |
| `prop:researchregion` | the admissible cap and cost | 5 | A.5 | P3 |
| `prop:atomless` | atomless preparation costs | 6.1 | A.6 | P4 R7 |
| `prop:classes` | value classes and other priors | 6.2 | A.6 | P2 R6 |
| `prop:manyclasses` | more than two classes under separation | 6.2 | A.6 | P2 R6 |
| `prop:signals` | complementary private signals | 6.3 | A.6 | P4 R8 |
| `rem:sizes` | continuous order sizes (the one Laplace remark) | 6.4 | — | — |
| `prop:access` | access to prices | 7.1 | A.7 | P2 R9 |
| `prop:payment` | the payment rule | 7.2 | A.7 | P2 R9 |
| `prop:reserves` | reserve comparisons | 7.3 | A.7 | P2 R9 |
| `prop:spread` | the spread and its entry component | 8 | A.8 | P5 |
| `prop:informedshare` | identification of the informed share | 8 | A.8 | P5 |
| `prop:winner` | orders predict the winner | 8 | A.8 | P5 |
| `prop:announcement` | announcement returns | 8 | A.8 | P5 |

Appendix sections: A.1 `app:payoffs`, A.2 `app:beliefs`, A.3 `app:prop2`, A.4 `app:coexistence`,
A.5 `app:research`, A.6 `app:robustness`, A.7 `app:welfare`, A.8 `app:empirical` (new), A.9 `app:parameters`
(declarations and the margins table; the file `appendix/A8_parameters.tex` becomes `appendix/A9_parameters.tex`).

Tables: `tab:payoffs`, `tab:outcomes`, `tab:region`, `tab:research`, `tab:margins`.
Figures: `fig:beliefs` (`figures/beliefs.pdf`), `fig:coexistence` (`figures/coexistence.pdf`),
`fig:research` (`figures/research.pdf`); slide versions `figures/*_talk.pdf`.
