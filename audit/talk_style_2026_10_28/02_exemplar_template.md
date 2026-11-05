# Exemplar theory decks and the model template

The decks support a common set of model ingredients, but not one fixed slide order. Present the agents, information, choices, payoffs, and equilibrium before the audience must interpret a formal result. A timeline helps when the sequence matters. An example can precede the general model.

## Sources and counts

The sample contains two research presentations, a recent job-market draft, a special lecture, and a symposium keynote. It does not establish a universal seminar format. No source states the speaking duration; a 45–90-minute duration remains unverified.

All five files, extracted text, and individual download receipts are in [the RDSS source folder](/mnt/rdss/austin/data/competition-creates-competition/talk_guides_2026_10_28/exemplar_decks/). Each receipt records the URL, date, bytes, and SHA-256. An additional Li deck is archived but excluded from the five-deck count.

**Count convention.** Page numbers below count the title as page 1. Main totals count file pages, including incremental reveals and section dividers, through the conclusion. They exclude appendices and final references. Thus these totals are not counts of distinct teaching units. Formal results mean explicitly labelled theorems, propositions, lemmas, or corollaries; repeated statements count once. Zero does not mean no substantive results.

| Deck and source | Duration | Main pages | Model starts | First labelled result; total | Leading example | Literature slide |
|---|---|---:|---|---|---|---|
| [Bergemann–Brooks–Morris, First Price Auctions, December 2016](https://campuspress.yale.edu/dirkbergemann/files/2010/12/nyu-abu-dhabi-07dec2016dbv1-258e6ll.pdf) | Unstated | 40 | Toy model 4; general model 17 | 26; **3** | Before general model, 4–14 | None; citations within example, 5–6 |
| [Bergemann–Brooks–Morris, Search, Information, and Prices, July 2020](https://campuspress.yale.edu/dirkbergemann/files/2020/07/sb-gtc-final.pdf) | Unstated | 37 | 7; divider 6 | 30; **1** | After model, 12–25 | None; context citation on 2 |
| [Quint, UTokyo Lecture II, February 2023](https://users.ssc.wisc.edu/~dquint/speciallectures/special%20lecture%202.pptx) | Unstated | 45 | Auction 4; entry model 8 | None; **0** | Entry example follows auction setup, 7–13 | References after model, 46; local citations throughout |
| [Goldstein, Financial Market Feedback, Cambridge, September 2019](https://www.dropbox.com/scl/fi/fmkyvf7gff954rgz9ev2i/Cambridge-Keynote.pdf?rlkey=2bqbwb7un5p0cu8fjmmb9lr80&dl=1) | Unstated | 41 | 13 | None; **0** | Application after model/results, 25–26 | Before model, 8 |
| [Iakovlev, Adversarial Elicitation, job-market slides, October 2025 archive](https://sites.northwestern.edu/andreiiakovlev/files/2025/10/Slides.pdf) | Unstated | 28 | 10 | 16; **2** | After model, 15 | Before model, 8 |

The first deck states an unlabelled example bound on page 13. Quint states the externality result on page 5 and the entry implication on page 10. Goldstein describes the equilibrium on page 17 and disclosure results on pages 20–22. These precede or replace labelled propositions.

**Notation count.** Count case-sensitive symbol families in each stated block. Collapse subscripts, primes, and accents; exclude indices, operators, constants, and prose abbreviations. Distinguish calligraphic letters. These reproducible counts measure notation families, not every mathematical glyph.

| Deck; model block | Distinct families | Inventory |
|---|---:|---|
| First Price Auctions, 17–19 | **14** | N, P, v, V, calligraphic S, S, π, σ, B, U, b, s, R, T |
| Search, 7–10 | **15** | v, N, n, K, k, μ, T, π, t, F, x, p, calligraphic K, R, S |
| Quint, entry block 8–9 | **6** | n, c, π, m, r, q |
| Goldstein, first model 13–17 | **20** | t, A, F, k, c, β, f, a, σ, τ, d, ξ, P, x, y, ε, ω, μ, φ, g |
| Iakovlev, 10–13 | **6** | a, n, Q, π, χ, E |

Quint's count covers the entry model, not all models in the lecture. Goldstein's count covers the first model only. The job-market source contains visible draft comments on page 14; use its structure, not its editorial finish.

## Reconstructed sequence

1. **Question and stakes.** Name the decision and the force that changes it.
2. **Answer in words.** State the contribution before theorem notation. Search does this on page 5; Iakovlev does so on pages 6–7.
3. **Minimal environment.** Introduce agents, the object, uncertainty, and the key restriction.
4. **Sequence and information.** State who observes what before each choice. Use a timeline when actions occur in distinct stages.
5. **Actions, payoffs, and solution.** Define feasible choices, the relevant objective, and equilibrium. These need not occupy separate slides.
6. **Leading example or benchmark.** Make the mechanism visible before the general result. First Price Auctions places this before steps 3–5 instead.
7. **Main result and intuition.** State conditions beside the claim. Follow with the decisive deviation, payoff comparison, or figure.
8. **Extensions and conclusion.** Return to the question; distinguish the main mechanism from extra cases.

This is a proposed template, not a rule inferred by majority vote. Search has model, information, strategies, payoffs, and equilibrium on pages 7–10. First Price Auctions combines strategies, payoffs, and equilibrium on page 18. Iakovlev separates incentives, partial commitment, and equilibrium/objective on pages 10–13. Goldstein orders technology, market, information, and equilibrium on pages 14–17. A separate timeline or literature slide is not universal.

**Best exemplar for this paper: Goldstein, page 13.** The slide has three setup bullets and a short timeline. It names a firm with a finance need, a traded claim on its cash flow, and private/public information. Then it gives three dates: asset trade and price; capital provision; cash flow and payoffs. The timeline is a list of dates, not a drawn game tree. It defers distributions and equations to later slides.

For a graphical alternative, Iakovlev page 11 places a one-line arrow sequence below the mechanism and action rules. It distinguishes private information, a message, an action, and payoffs.

## Current deck and proposed model block

The current deck already has the ingredients. S5 introduces the setting and auction. S6 combines primitives, information, independence, and the strength path. S7 combines the market sequence with posterior-bound notation. S8 combines payoff definitions with ownership. S9 combines equilibrium conditions with outcomes and comparative statics. The main problem is density and sequence within these slides.

Two repairs matter. S8 writes realized expressions as t(θ) and g(θ), although the paper defines these functions as expectations over R. S9 must distinguish the challenger's price belief from the market makers' order belief until price sufficiency applies.

The following six proposed faces replace the functions of S5–S9. They require author approval before any deck edit. Keep Madrid and the names incumbent, challenger, and investor.

### 1. Players and values

- A listed target has standalone value zero. All strategic agents are risk neutral.
- The incumbent is ready. Its value R has public continuous distribution F and remains private before bids.
- The challenger has class j ∈ {H,L}, with prior Pr(H) = π. Its value θ has distribution G_j.
- The high class first-order dominates the low class. Every challenger value meets reserve p > 0.
- An outside investor knows the class, but not θ. Neither bidder trades target shares.

Speech: values and costs are per share; class distributions have finite means and may contain atoms. A stronger incumbent means a first-order stochastic strengthening of F. [Paper §2.2–2.3.]

### 2. Timeline and information

Use one timeline with these stages:

1. The seller commits to a cash second-price auction with reserve p.
2. The investor learns j. One selected trader submits an order.
3. Market makers observe the order and set the stock price P.
4. The challenger observes P, then its cost C, and chooses whether to prepare.
5. Preparation reveals θ and permits a bid. Prepared bidders learn their values and bid; the sale determines payoffs.

Below: C = 0 with probability ρ ∈ (0,1); otherwise C = c_H > 0. The challenger sees neither the order nor j, θ, or R before preparation. The pair (j,θ), R, C, and the slot draws are mutually independent. [Paper §2.2–2.3.]

### 3. The order slot

- With probability λ ∈ (0,1), the investor selects q ∈ {−1,0,1}: sell, abstain, or buy.
- A nonzero order costs k > 0.
- Otherwise, a liquidity trader selects those orders with probabilities β, 1−2β, β; 0 < β ≤ 1/3.
- Market makers see X, but not the trader's identity. They absorb the order at P(X) = E[V_T | X].
- V_T is the terminal target payoff per share. The investor receives q[V_T − P(q)] − k|q|.

Show the two possible traders as alternative branches into one slot. Do not draw additive informed and liquidity orders. [Paper §2.3.]

### 4. Auction payoffs

The highest admissible bid wins and pays the larger of p and the rival bid. Without an admissible bid, no sale occurs.

For a prepared challenger, θ ≥ p:

\[
t(\theta)=\mathbb E_R[\max\{p,\min(R,\theta)\}],\qquad
g(\theta)=\mathbb E_R[(\theta-\max\{p,R\})_+].
\]

The target receives t; the challenger receives g before preparation costs. Their sum is θ.

Class means: t_j = E_j[t(θ)], g_j = E_j[g(θ)]. Without entry, t_0 = p[1−F(p)]. The spread Δ_T = t_H − t_L measures how strongly target proceeds reflect class. [Paper §2.4, §3.1.]

### 5. Preparation and the stock price

At class belief μ, expected gross challenger profit is B(μ) = g_L + μ(g_H − g_L).

- A zero-cost challenger prepares after every price.
- A high-cost challenger prepares when B at its **price belief** is at least c_H.
- Let e(x) denote preparation probability after price P(x); e(x) ≥ ρ.
- Market makers use μ(x) = Pr(H | X = x):

\[
P(x)=t_0+e(x)[t_L-t_0+\Delta_T\mu(x)].
\]

Speech: the stock price anticipates preparation, which changes the traded claim's payoff. If Δ_T > 0, the positive entry floor makes the price reveal the order posterior. If g_H > g_L, introduce τ = (c_H−g_L)/(g_H−g_L) when the entry threshold first matters. [Paper §2.4, §3.2; Appendix A2, price-sufficiency proof.]

### 6. Equilibrium

- Each class chooses a distribution over the three orders to maximize expected investor payoff.
- Bayes' rule determines order beliefs and beliefs conditional on the observed price.
- Prices equal expected terminal payoffs; preparation follows the rule above.
- Each prepared bidder whose value meets p bids its value.
- Investor deviations face the candidate price and entry rules. An indifferent investor may mix; an indifferent high-cost challenger prepares.

Speech: every order occurs in both classes because of liquidity trade. Equal prices require pooled price beliefs unless sufficiency applies. Equilibrium specifies strategies, beliefs, prices, and preparation jointly. [Paper §2.4; Appendix A1, Definition “Equilibrium,” E1–E6.]

## Notation to defer and limits of the template

Move bar r, D(y), distribution integrals, the full strategy tuple, and U_j's expanded formula to backups B2, B3, and B5. Explain support and independence in speech where appropriate. Introduce b, u, m, M, κ, and τ only when the bounds need them. Introduce W_j, ownership, and takeover share at the ownership result. Reserve {F_r}, r, and example values h and ℓ for the path or example. These are deferred objects, not changed assumptions.

This paper couples market prices and a later real decision. A conventional game tree alone hides that dependence. Goldstein separates the asset market from the later capital decision, then states their equilibrium relation (pages 13–17). His price clears noisy supply; this paper instead uses competitive market makers and conditional expected value. Borrow the separation, not his price equation.

Search places price strategies and revenue beside equilibrium (page 9). Follow that principle here: display the traded payoff before the equilibrium conditions. The order slot also requires an explicit identity draw; the price reveals information about class, not a posted bid from the incumbent.

## Questions for the author

1. Does this sequence match the faculty reader's template, particularly the separate timeline and equilibrium slides?
2. Can the model block use six concise faces instead of the current five dense faces?
3. Should a symbolic two-class example precede the general distributions, as in First Price Auctions?
4. Can the model reserve ownership notation for its result and correct S8's missing expectations?
