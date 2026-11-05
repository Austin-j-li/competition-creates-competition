# Workaround research: common brief for solvers

You are one of several independent solvers, each from a different model family, working on one weakness of an economic theory paper. Work alone: do not read any other file in the `workarounds/raw/` folder named below, apart from your own output file.

## Paths and permissions (all absolute)

- Repository root: `/Users/austinli/Projects/competition-creates-competition`
- Manuscript (LaTeX master, read-only): `/Users/austinli/Projects/competition-creates-competition/overleaf/slot/` (`sections/*.tex`, `appendix/A1_payoffs.tex` … `appendix/A9_parameters.tex`)
- Scan report (read first): `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/SCAN.md` (headline findings, Part 1 generality table, Part 2 reduction lemma)
- Raw math reports from the scan: `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/raw/astra_A3_A5_reduction.md` and `.../raw/sol_generality_A1_A2_A6_A8.md`
- Your weakness brief and your output file are named in your task message.
- Scratch directory for your own scripts: `/tmp/ccc_wa2/<weakness>/<your model>/` (create it).

READ-ONLY on everything under the repository root, except the single output file named in your task. Do not edit, create, delete, stage or commit anything else. Do not run git commands that change state. Use absolute paths for every write.

You may run short python3 calculations to explore parameter values. Print results. Do not write assertions, test files or test frameworks.

## The paper

"Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders", order-slot version. Single author (Austin).

The model in brief. A challenger belongs to class j ∈ {H, L}, with prior π = Pr(H). Its value θ is drawn from G_j. Class ranking: G_H ≤ G_L pointwise, and every value is at least the reserve p; D = G_L − G_H ≥ 0. The incumbent's value R ~ F is continuous; F varies along a first-order stochastically ordered family F_s ("a stronger incumbent"). The sale is a second-price auction with reserve p. t_j and g_j are the target's proceeds and the challenger's gross profit given entry by class j; t_0 is the proceeds without entry. The spread is Δ = Δ_T = t_H − t_L = ∫_p^∞ [1 − F] D; γ = g_H − g_L = ∫_p^∞ F D; Δ + γ is the fixed class-mean gap. Preparation cost C = 0 with probability ρ and c_H otherwise. This two-point cost is FIXED: do not propose a general cost law and do not rename c_H (Proposition A.4 is the robustness result for other cost laws). The preparation threshold is τ = (c_H − g_L)/γ: a challenger with posterior μ prepares at cost c_H when μ > τ. W_j(F) = E_j[F(θ)] is the win probability of a prepared class-j challenger.

Trading is an order slot, a modification of Dow and Gorton (1997): with probability λ an informed investor, who learns the class, places q ∈ {−1, 0, 1} at cost k|q|; otherwise a liquidity trader sells, abstains or buys with probabilities β, 1 − 2β, β. b = (1 − λ)β. M(π) and m(π) are the top and bottom posteriors after an order. Entry after order x is e(x) = ρ below τ and 1 above (with a tie rule at τ). J = Δ(1 − τ). With research, an informed investor is present with intensity λ chosen at cost (a/2)λ² up to a cap λ̄.

The benchmark: point-mass classes h = 10, ℓ = 1, R ~ U[0, r], p = 1/2, ρ = 1/4, c_H = 6, k = 1/50, prior 1/2, strengths r ∈ [6/5, 18/5].

Key established fact (the reduction lemma, SCAN.md Part 2): orders, posteriors, entry and research intensity depend on the auction only through (Δ, τ). Under the class ranking a stronger incumbent weakly raises Δ and τ (τ when c_H ≥ g_L and γ > 0). Ownership (W_H), welfare and price levels lie outside the reduced outcome.

## Austin's goals

One unified model. Every theorem at the generality its proof supports. Conditions named in economic terms, not "in the benchmark". He prefers bold, plain economic statements to defensive caveats, but every statement must be true. The preparation cost stays two-point.

## Your task

For the weakness in your brief, do three things.

A. Reformulate. Find a different statement that holds with no extra condition and is at least as interesting economically as the original claim. Possible moves: state the result in the (Δ, τ) plane instead of along a strength path; compare with a counterfactual at the same incumbent (fixed information, no research) so that the direct competition effect cancels; decompose an outcome into an information channel and a direct channel; replace a level by a ratio or a conditional probability; replace an interval claim by a monotone comparative-statics claim on the set where the branch exists. Say exactly what is lost relative to the original.

B. Primitive condition. Keep the original claim and find the most natural sufficient condition on primitives (G_H, G_L, p, the family F_s, costs, slot) that guarantees it, ideally one with economic meaning (for example: class H outbids every incumbent on the path; D nondecreasing on the incumbent support; an elasticity comparison; a bound on c_H relative to the class gap). Check whether the benchmark satisfies it and with what margin. Say whether it is necessary, or how far from necessary.

C. Importance. Are the parameters in the known counterexample reasonable or extreme? How much does the weakness matter for the paper's economics?

Work the mathematics yourself: derive, do not assert. Read the relevant manuscript passages before proposing. Check numbers with python. Return one to three candidates, best first.

## Output file format (Markdown)

```
# <weakness key>: <your model name>

## Candidate 1: <short name>
Angle: reformulate | primitive condition | both
Intuition: 2 to 4 plain sentences.
Formal statement: ...
Derivation: the key steps, actually derived.
Conditions: ...
Benchmark check: with numbers.
What is lost: ...

## Candidate 2 ...

## Importance of the weakness
## Other findings (errors in the manuscript, anything surprising)
```

Your final reply to the task (not the file) must be at most 150 words: the output path, your best candidate in one or two sentences, and your confidence in it.
