# Brief: the order-slot manuscript, its slides, and a comparison of two set-ups (23 October 2026)

Read `TEAM_RULES.md` in this folder first. This brief has priority if the two differ.
The ledger of workstreams is `LEDGER.md` in this folder.

## 1. Goal

The author has a manuscript where Laplace order-flow noise is the main microstructure
(`overleaf/paper/main.tex` and `online_appendix.tex`, pinned at commit `01bd5d6`; below, "the Laplace manuscript").
The team writes three new documents in the local project `overleaf/competition_slot/`:

1. `main.tex`: a full manuscript in which the **order slot** is the main microstructure. It is a parallel
   version of the paper. It reads as if the order slot were the model from the start. It has a main text of
   about 30 to 40 pages and **one** proof appendix (Appendix A) that proves every result end to end.
   There is no online appendix.
2. `slides.tex`: a Beamer talk for the order-slot manuscript: about 20 main frames plus backup frames.
3. `comparison.tex`: a note of about 10 to 15 pages that compares the two set-ups at a high level. The
   readers are three economists who know the project. The note has a neutral title and no addressee.

Proof packages, the number registry, scripts and checks live in this folder (`audit/slot_manuscript_2026_10_23/`).

## 2. The order-slot model

Everything in the Laplace manuscript's Sections 2.1, 2.2 and 3.1 stays: the decision interval, quality classes
`j ∈ {H, L}` with prior `π` and values `θ ~ G_j`, `G_H` first-order dominates `G_L`, supports above the reserve
`p`, the incumbent value `R ~ F` (`U[0, r]` in the leading case), `c_L = 0`, a preparation cost `c_H > 0` with
probability `1 − ρ`, the second-price auction with reserve `p`, the objects `t_j`, `g_j`, `Δ_T = t_H − t_L`,
`B(μ) = g_L + μ(g_H − g_L)`, `τ = (c_H − g_L)/(g_H − g_L)`, and Proposition 1 (acquisition profits and target
value). Only the trading stage changes.

**Trading stage (the order slot).**

1. One public order opportunity comes before the challenger's decision.
2. With probability `λ ∈ (0, 1)` the informed investor fills it. The investor sees the class `j` and chooses
   `q ∈ {−1, 0, 1}`. A nonzero order costs `k > 0`.
3. With probability `1 − λ` a liquidity trader fills it. It sells, abstains or buys one unit with
   probabilities `β`, `1 − 2β`, `β`, with `0 < β ≤ 1/3`. Its motive is exogenous.
4. No one observes who filled the slot. The identity draw is independent of the class, the costs and `R`.
5. Competitive market makers see the order `X ∈ {−1, 0, 1}` and set `P = E[V_T | X]`. The challenger sees
   the price, then decides whether to prepare.

**Derived objects.** `b = (1 − λ)β`; `u = λ/b` (the informed presence mass relative to the liquidity mass in one direction; `1 + u` is the largest likelihood ratio of an order; under full orders at prior 1/2 the odds that a purchase is informed are `u/2`);
posterior bounds under every investor strategy (this needs `β ≤ 1/3`):

```
M(π) = π(1 + u) / (π(1 + u) + 1 − π)          m(π) = π / (π + (1 − π)(1 + u))
```

Every order is on path, so no off-path belief is needed. State both tie rules (the investor's and the
challenger's) and show which results depend on them.

**A remark, not a section.** Continuous order sizes need a convention for unused order sizes (as in
Edmans, Goldstein and Jiang 2015). Laplace noise with scale `s` gives the same top posterior when
`1 + u = e^{2/s}`. One remark in Section 6 records this. No other text mentions Laplace noise.

## 3. The benchmark (calibration B): primitives

Auction and cost primitives as in the Laplace manuscript: `h = 10, ℓ = 1, p = 1/2, ρ = 1/4, c_L = 0,
c_H = 6, k = 1/50, π = 1/2`; incumbent strengths `r_0 = 6/5, r_1 = 3, r_2 = 18/5`.

Slot primitives (declared, exact):

- `1 + u = e`, so `M(1/2) = e/(1 + e) = 0.731059`;
- `β = 0.294655` (an exact decimal);
- `λ = uβ/(1 + uβ) = 0.336122` (derived; it is not rounded in any computation).

The manuscript states these as primitives. It does not justify them by another model.
The certificate for any statement that depends on `e` uses interval arithmetic (`mpmath.iv` or
rational bounds on `e`).

Known values at B (from the earlier study; every one must be recomputed and registered):
entry at `r_1` 0.522757, ownership 0.3244, ceiling `r_C` 3.592659, return margin at 3.6 of about 0.0003 in
posterior, prior range for Proposition 2 `(0.467850, 0.500424)`, `r_A = 1.393958`, `r_F = 1.467127` (1.460985 is the calibration A value),
`r_N = 1.747878`.

## 4. Results the manuscript proves

Sources: `audit/microstructure_search_2026_10_22/` (below, "the earlier study"). Start from its memos.
Read `memos/EXTENSIONS_SUMMARY.md`, `memos/SYNTHESIS.md` §5.1, `memos/T2_liquidity_trader.md`, and the memo
named in each row. Re-derive each result. Do not copy a claim without its proof.

| # | Result | Earlier memos | Note |
|---|---|---|---|
| R1 | Proposition 1 (payoffs, target value) | Laplace manuscript A.1 | unchanged; port the proof |
| R2 | Posterior bounds and informed trading under every strategy | T2 §3.1–3.3 | needs `β ≤ 1/3` |
| R3 | Proposition 2 for general classes and priors | E1, XE1 | corrected hypotheses: `B_0(π) < c_H < B_1(M)`; `Δ_0 < k < ρ·min{m, 1 − M}·Δ_1`; `B_2(M) < c_H`. Ownership rises iff `[ρ + (1 − ρ)(b + λ)]W_H(F_1) > ρW_H(F_0)` |
| R4 | Proposition 3: coexistence on an interval at fixed `λ` | T2 §3.6, X | `r_A`, `r_F`, `r_N`; the prior window where `r_A` is the common start; entry rises weakly |
| R5 | Fixed-information control: entry does not rise | E2, XE2 | the manuscript says "does not rise" |
| R6 | Value classes and other priors; more than two classes | E1, XE1 | many-class statement needs a separation condition |
| R7 | Atomless preparation costs | E2, XE2 | |
| R8 | Complementary private signals | E2, XE2 | |
| R9 | Access to prices; payment rule; reserves | E1, XE1, T2 §3.10 | reserve deterrence is flat at the exclusion reserve |
| R10 | Competition creates research | N3, XN3 | **re-derive at calibration B** (N3 used `β = 1/3`) |
| R11 | Empirical implications | N1 (unchecked) | only checked claims enter the manuscript |

Wording changes against the Laplace manuscript go in as stated results, not as apologies: the
fixed-information control "does not rise"; entry is flat at the exclusion reserve; the many-class result
holds under a separation condition.

## 5. The proof standard (every proof package and Appendix A)

The comparison note will point to this standard, so every proof follows it.

1. **Equilibrium object.** State each equilibrium as an explicit tuple: the class-contingent order
   distributions, the price function on every order, the beliefs, the entry rule, the bids.
2. **Conditions.** List the equilibrium conditions: Bayes consistency, competitive prices, entry
   optimality, investor optimality, truthful bids (and research optimality in R10).
3. **Verification against the fixed object.** Check each condition by direct computation against the
   stated tuple. A deviation holds the candidate's price function and entry rule fixed. No step assumes the
   conclusion. No step uses "by symmetry", "it is easy to show", or "similarly" without the computation.
4. **Uniqueness through bounds on every profile.** A uniqueness claim uses bounds that hold for every
   candidate profile (for example the posterior bounds `m ≤ μ ≤ M`), not only for the proposed one.
5. **Strict margins.** Every hypothesis is a strict inequality. Record its margin at the benchmark in a
   margins table. State the open parameter set that the hypotheses define. A computer-assisted step uses
   exact rational or interval arithmetic and names its script and run log.

The admissible region (the `(λ, β)` set, the prior range, the research cost and cap ranges) is a result.
Present it as a table, not as a caveat.

## 6. The number registry

One registry holds every number that any of the three documents prints:
`audit/slot_manuscript_2026_10_23/registry/registry.csv` with columns
`key, value, display, status, source_script, run_log, note`.

- `status` uses: input, analytical, computer-assisted, numerical diagnostic, open.
- Scripts that write rows live in `scripts/<STEM>/` and write a run log beside their output.
- Each workstream writes its own rows to `registry/<STEM>.csv`. The coordinator merges them.
- The documents print only registry values, in the registry's display format.
- The coordinator converts the merged registry into `overleaf/competition_slot/numbers.tex`. The documents
  print a number with the macro `\reg{<key>}` (it works in text and in math). An unknown key prints `??<key>`
  in bold and writes a warning to the log.

**Starter keys** (use these names where they apply; add new keys with the same pattern):

| Key | Meaning |
|---|---|
| `u_B`, `beta_B`, `lambda_B`, `b_B` | slot primitives and `b = (1 − λ)β` at B |
| `M_half_B`, `m_half_B` | posterior bounds at `π = 1/2` |
| `tau_r0`, `tau_r1`, `tau_r2` | thresholds `τ(r)` at the three strengths |
| `entry_r0`, `entry_r1_B`, `entry_r2` | entry at the three strengths |
| `own_r0`, `own_r1_B`, `own_r2_B` | H-class ownership at the three strengths |
| `rC_B`, `rA`, `rF_B`, `rN` | ceiling, start of coexistence, end of the rising branch, no-trade boundary |
| `prior_lo_B`, `prior_hi_B` | prior range for Proposition 2 at B |
| `u_lo`, `u_hi`, `M_lo`, `M_hi` | the band for `u` and for `M(1/2)` |
| `margin_<condition>_B` | margins table entries |
| `res_a`, `res_cap` | research cost parameter and cap |
| `res_lambda_r155`, `res_entry_r155`, … | research and entry at `r = 1.55` (and `r160`, `r165`) |

## 7. Manuscript outline (`overleaf/competition_slot/main.tex`)

Same title as the Laplace manuscript; author Austin Li. A new abstract and introduction for the slot model.

1. Introduction
2. The model: 2.1 decision interval; 2.2 values, preparation and costs; 2.3 trading: the order slot;
   2.4 equilibrium (the explicit object)
3. Competition and information: 3.1 acquisition profits and target value; 3.2 what the challenger learns from
   the price; 3.3 informed trading
4. Equilibrium results: 4.1 competition creates competition (R3); 4.2 the benchmark and the fixed-information
   control (R5); 4.3 coexistence (R4)
5. Competition creates research (R10)
6. Robustness: 6.1 preparation costs (R7); 6.2 value classes and priors (R6); 6.3 complementary private
   signals (R8); 6.4 order sizes (the remark of §2)
7. Welfare and sale terms (R9)
8. Empirical implications (R11, checked claims only)
9. Conclusion
Appendix A: proofs (A.1 payoffs; A.2 beliefs and trading; A.3 Proposition 2; A.4 coexistence; A.5 research;
A.6 robustness; A.7 welfare and sale terms; A.8 parameter declarations and the margins table)

LaTeX: `article`, 12 pt, `newtxtext`/`newtxmath`, `amsthm`, `natbib` with `references.bib`, numbered sections,
`booktabs` tables, vector PDF figures. pdfLaTeX. Figures: no in-figure titles, `(a)/(b)` panel labels,
embedded fonts, data from the registry.

## 8. Slides and comparison note

**Slides (`slides.tex`).** The style of `overleaf/talk/talk.tex` (moloch theme, UCL palette, Fira Sans, XeLaTeX,
`econ-slides-compat.sty`). About 20 main frames and backups. No first person. No status labels on slides.

**Comparison note (`comparison.tex`).** Sections:

1. The two set-ups in one page each (primitives, timing, what the challenger learns).
2. Main results side by side (a table, then text).
3. Trade-offs: the dynamics each set-up generates (the partial sale; strictly rising entry; research;
   timing) and the conclusions each supports.
4. The proof method: the equilibrium object as a proof artifact; non-circular verification; uniqueness
   through bounds on every profile; strict margins and the open parameter set; interval certificates.
   One worked proof for each set-up, side by side, written to the standard in §5.
5. Where each set-up stands against the standard (from the audit of the Laplace manuscript, workstream LA).
6. Decision points for the authors. No verdict.

## 9. Writing

- Controlled English (TEAM_RULES §8) and the anti-defensive rules (TEAM_RULES §9).
- No first person on slides. "We" is allowed in the manuscript and the note.
- No names of AI models, agents, assistants or tools in any document, memo, script or comment.
