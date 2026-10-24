# Brief: new extensions that the order slot makes possible (23 October 2026)

## 0. The request

The author: "while it is useful to check whether the old extensions hold, I'm sure there could be new
extensions found in the slot set up; in parallel, [start a team] to search for additional
interesting extensions."

The old extensions (value classes, priors, atomless costs, private signals, access to prices, payment
rule, reserves, fixed-information control) are checked elsewhere (`EXTENSIONS_BRIEF.md`). Do not redo them.

## 1. The order slot

One public order opportunity before the challenger decides. With probability `λ` the informed investor
fills it; it sees the class `j ∈ {H, L}` (prior `π`, values from `G_j`) and chooses `q ∈ {−1, 0, 1}` at
cost `k|q|`. With probability `1 − λ` a liquidity trader fills it: sell, wait, buy with probabilities
`β, 1 − 2β, β`. Competitive market makers see the order `Q` and set `P = E[V_T | Q]`; the challenger sees
`P` and its cost (`0` with probability `ρ`, else `c_H`), then decides whether to prepare; the paper's
second-price auction with reserve `p` follows. Write `b = (1 − λ)β`, `u = λ/b`; a buy has likelihood ratio
`1 + u`; `M(π) = π(1 + u)/(π(1 + u) + 1 − π)`.

Known results (read `memos/T2_liquidity_trader.md`, variant V3, and `memos/X_check.md`): Prop. 2 holds at
the benchmark on the band `τ(3) < M < τ(3.6)`; coexistence on about [1.394, 1.748]; access to prices
raises proceeds and surplus; no off-path beliefs on the unit menu. Lost: partial sales `(1, −v)` and the
strict rise of entry across 1.55, 1.60, 1.65 (entry is flat there). Benchmark: `h = 10, ℓ = 1, p = 0.5,
ρ = 0.25, c_L = 0, c_H = 6, k = 0.02, π = 1/2`, strengths 1.2, 3, 3.6; calibration A `β = 1/3, λ = 6/17`.
The paper: `git -C overleaf/paper show 01bd5d6:main.tex` (and `:online_appendix.tex`).

## 2. What counts as a good new extension

An extension is worth reporting if it does at least one of these:
- gives a new testable prediction, especially in observables that microstructure work measures
  (spreads, price impact, order imbalance, the probability of informed trade, volume, timing);
- recovers a result the slot loses (partial sales, entry that rises across coexisting equilibria);
- adds new economics that the slot makes tractable and the Laplace model does not (closed forms,
  dynamics, strategic roles for other traders);
- connects the paper to a verified literature (see `memos/L1_survey.md`).

For each extension: the question; the model change; the main result with its derivation (a proof, or an
exact or interval computation at the benchmark); the economic reading; the testable prediction if any;
the status label; and what stays open. A documented failure is a result.

## 3. Directions (one member each)

| ID | Direction | Examples (not exhaustive) |
|---|---|---|
| N1 | Market observables and empirical content | bid–ask spread and price impact as functions of incumbent strength; the probability of informed trade (`2M − 1`, a PIN-like statistic) before contests; order imbalance; what the slot predicts for event studies of takeover targets |
| N2 | Dynamics and arrivals | several order slots before the decision (sequential Glosten–Milgrom trading); a random number of arrivals (PIN-style event days, Poisson); speed of discovery and the timing of preparation; whether a richer price path restores rising entry at 1.55–1.65 while keeping the return to the floor |
| N3 | Order size and research | order size choice (one or two units) with size-dependent liquidity trade, in the spirit of Easley and O'Hara (1987); whether size choice brings back partial sales and rising entry; endogenous research: `λ` as the probability that costly research succeeds, as in Dow and Gorton (1997) ("competition creates research") |
| N4 | Other strategic traders | a strategic uninformed trader who can buy to trigger entry (manipulation, as in Goldstein and Guembel 2008); the challenger or the incumbent trading through the slot (toeholds; Kyle and Vila 1991; Bagnoli and Lipman 1996); a long-lived liquidity motive versus a free choice |

Members may add other ideas in their direction. Avoid the other members' directions.

## 4. Rules

Follow `TEAM_RULES.md` in this folder (write only in this folder; memos in `memos/`, scripts in
`scripts/<STEM>/`; no tests or assertions; no commit; no hand-off of the task; slot wrapper for runs over 60 s;
at most 3 slots; no AI names; status labels; controlled English). Only N1 may use the shared browser, and
only to verify a precedent (its own tab; never close the user's tabs; no logins; no downloads). Others cite
`memos/L1_survey.md` and the earlier verified records, or mark sources "unverified". Do not read
`opinions/coordinator_view.md` or `opinions/opinion_*.md`.

Memo format: 1. Question. 2. Extensions developed (each with model change, result, derivation, status,
reading, prediction). 3. Ideas considered and dropped, with the reason. 4. Ranking of your extensions by
interest and strength. 5. Open issues. 6. Plain summary, 300 words at most.
