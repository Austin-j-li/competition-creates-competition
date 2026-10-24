# Brief: an EGJ-like microstructure for the paper (22 October 2026)

## 0. The author's request

The author wrote: "Laplace is an unconventional construct for this problem. I want to anchor more around
the EGJ-like microstructure setup; we don't need to be 100% it. Do a literature search and tell me what are
typical microstructure modelling methods when corporate behaviours are in the picture. Discrete modelling
should be a strong candidate, but is there a setup we can fine-tune to find our desired result with
comparable strength."

"EGJ" is Edmans, Goldstein and Jiang (2015, *American Economic Review* 105(12): 3766–3797).

This study is exploratory. It edits no file of the paper.

## 1. What is known (read, do not redo)

The paper: `git -C overleaf/paper show 01bd5d6:main.tex` and `:online_appendix.tex` (the revised paper,
with quality classes, a zero low cost and a section that justifies the noise law). Read Sections 2–4 and
the noise-law passages.

The earlier discrete study is in `audit/discrete_exploration_2026_10_21/`. Its findings:

- `memos/SYNTHESIS.md` and `memos/RED_TEAM.md`: the verdicts.
- `memos/A_three_point.md`, `memos/A_bruteforce.md`: the EGJ-style three-point model with buy-only orders,
  presence `λ`, and a challenger who sees the price. Results:
  - The top flow `x = 2` comes only from a class-H purchase, so it reveals class H. The investor earns
    nothing at the flow that recruits the challenger. Feedback dies.
  - One trade cutoff `k < ρΔ_T/3` (at `π = 1/2`). It does not depend on `λ`.
  - Entry at `r = 3` is 0.375 (paper: 0.523). Entry returns to `ρ` only above `r = 7.97`.
  - Coexistence of no trade and trade only at a knife-edge, with challenger mixing.
  - Under no trade, the flow 2 is unused; existence needs belief 1 there (EGJ's own convention).
- `memos/C9_unequal_mixing.md`: unequal three-point weights with mixing; an upward entry branch only
  0.014 wide; the top flow still reveals class H.
- `memos/C1_two_sided.md`, `memos/B_dlaplace_theory.md`: discrete-Laplace (geometric-count) noise. It
  recovers the paper. The buy-only flow carries information only through the event `X ≥ 1` against `X ≤ 0`
  (Lemma 1 in `memos/C4_sequential.md`). With buy-only orders at `b = 1`, the thresholds equal the paper's
  (`scripts/_coordinator/buyonly_scale.py` and `LEDGER.md`, coordinator note of 22 Oct).
- Literature records: `audit/alex_meeting_2026_10_21/memos/LIT_extracts.md` (verified extracts A1–A7 and
  more), `audit/alex_meeting_2026_10_21/memos/Q2_discrete_literature.md` (EGJ, GG 2008 and others compared
  item by item), and `audit/discrete_exploration_2026_10_21/memos/D_literature.md` (22 ranked sources).

The discrete-Laplace results are the **bar for "comparable strength"**. They are not the design to return
to. The author wants an EGJ-like setup.

## 2. The paper's results to target (the scorecard)

Use the paper's benchmark: `h = 10, ℓ = 1, p = 0.5, ρ = 0.25, c_L = 0, c_H = 6, k = 0.02, π = 1/2`,
strengths `r_0 = 1.2, r_1 = 3, r_2 = 3.6`, auction objects as in TEAM_RULES §3.

Every theory memo fills this scorecard for each candidate setup:

1. Prop. 2(i): no informed trade and entry `ρ` at `r_0`.
2. Prop. 2(ii): informed trade and entry above `ρ` at `r_1`; the entry level.
3. Prop. 2(iii): entry back at `ρ` at `r_2`, with trade still informative (a ceiling `r_C`).
4. Prop. 3: an interval of strengths where no trade and informative trade coexist. Does it contain
   1.55–1.65? Is entry ordered upward across the informative equilibria?
5. Prop. A.9: does access to prices raise target proceeds and net surplus?
6. Off-path beliefs: which claims need a rule at an unused flow? EGJ use the Intuitive Criterion, with the
   belief that a trader at an unused extreme flow is informed. Say explicitly when a claim rests on this
   convention.
7. Tie rules (investor and challenger), knife-edges, and mixed strategies.
8. The tunable knob, its range that works, and its economic meaning.
9. Literature precedent for the exact device (cite a verified record, or mark it "unverified").
10. Status labels: analytical, computer-assisted, numerical diagnostic, conjecture, open.

If the paper's benchmark cannot work, report the smallest parameter move that does. A candidate that needs
`c_H` near `h`, or `λ` near 1, or a knob on a knife-edge, is a documented failure, not a result.

## 3. The key obstacle

With any noise of bounded support, the top flow can come only from an informed purchase. It reveals class
H, the price there equals the value, and the investor earns nothing there. EGJ note (p. 3787) that `λ < 1`
stops revelation at `x = ±1` in their two-sided model. It does not stop revelation at `x = ±2`.
So the question for each lever is:

- Does it make the flow that recruits the challenger interior (a posterior strictly between 0 and 1)?
- Can entry return to `ρ` at `r_2 = 3.6` while a revealing flow still recruits? (If `g_H(r) ≥ c_H`, a
  revealing flow recruits for every `r < 7.97`.)

## 4. Workstreams

| ID | Task | Output |
|---|---|---|
| L1 | Literature: the microstructures of models with corporate decisions. The only browser user. | `memos/L1_survey.md` |
| L2 | Taxonomy of methods and their properties for this mechanism, from the records; no browser. | `memos/L2_taxonomy.md` |
| T1 | EGJ's own menu: two-sided orders `{−1, 0, 1}`, three-point noise, presence `λ < 1`; optional symmetric non-uniform noise weights. | `memos/T1_egj_two_sided.md` |
| T2 | A liquidity or uninformed trader of the same order size as the informed one (EGJ's second and third readings of `λ`; GG's uninformed speculator; one-order arrival as in Glosten–Milgrom), with and without three-point noise; buy-only and two-sided. | `memos/T2_liquidity_trader.md` |
| T3 | Buy-only orders (the one-directional EGJ menu) with bounded noise variants: symmetric non-uniform weights, `N` noise traders (binomial noise), two-unit informed orders, presence `λ`. Excludes T2's device. | `memos/T3_buy_only_bounded.md` |
| X | One independent check of the best candidate, by a second, independent member. | `memos/X_check.md` |
| S | Synthesis: what is conventional (with counts), the recommended EGJ-like setup, its knob, what it reproduces and what it loses. | `memos/SYNTHESIS.md` |

T2 extra requirements:
- Compare both the information structure and the investor's payoffs with the buy-only discrete-Laplace
  base. There the investor trades at every flow. A presence-type trader trades only when it is present, so
  thresholds can differ even when posteriors coincide.
- At most one paragraph on whether the geometric-count model is equivalent to a conventional device.
  The author asked for an EGJ-like setup, not a defense of the Laplace model.

## 5. Rules

See `TEAM_RULES.md`. Effort is high for most members. Only T1 runs at the highest effort.
