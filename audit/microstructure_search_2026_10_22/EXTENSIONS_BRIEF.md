# Brief: do the paper's extensions hold under the order slot? (23 October 2026)

## 0. The question and the decision rule

The order slot (candidate E) keeps Prop. 2, coexistence and the access-to-prices result at the benchmark.
Before the author moves it into the main text, every extension in the paper must also hold with the slot
as the trading stage. Decision rule from the independent opinions: if one extension fails, keep Laplace in
the main text; if all hold, the order slot can carry the main text.

"Hold" means: the extension's statement, with the slot in place of Laplace noise, is true, and we can prove
it (analytical) or certify the paper's numerical example for it (computer-assisted, exact or interval).
"Holds with change" means a weaker or modified statement is true; say exactly what changes.
"Fails" means a counterexample, or a statement that cannot be true under the slot.

## 1. The order slot (the trading stage to use)

One public order opportunity. With probability `λ` the informed investor fills it; it sees the class `j`
(not the value) and chooses `q ∈ {−1, 0, 1}` at cost `k|q|`. With probability `1 − λ` a liquidity trader
fills it: sell, wait, buy with probabilities `β, 1 − 2β, β` (exogenous motive). Market makers see the order
`Q` and set `P = E[V_T | Q]`; the challenger sees `P`. Write `b = (1 − λ)β`, `u = λ/b`.
A buy has likelihood ratio `1 + u`; the posterior bounds are
`m(π) = π/(π + (1 − π)(1 + u))` and `M(π) = π(1 + u)/(π(1 + u) + 1 − π)` under every strategy.
Calibrations: A (`β = 1/3`, `λ = 6/17`) and B (`u = e − 1`, chosen so that `M(π)` equals the paper's
Laplace bound at every prior; `β ≈ 0.2947`, `λ ≈ 0.3361` matches the benchmark entry 0.522757).
Unit menu only (with continuous orders the slot needs EGJ's off-path belief convention; out of scope).

Source memos (read first): `memos/T2_liquidity_trader.md` (variant V3 two), `memos/X_check.md`,
and the coordinator's general-prior note in `LEDGER.md` (22 Oct, "coordinator (not yet checked)"): it states
a general-prior Prop. 2 under `Δ_0 < k`, `π < τ_1 < M < τ_2`, `π < τ_2`, `ρΔ_i min{1 − M, m} > k` (i = 1, 2),
with `E_1 = ρ + (1 − ρ)(πλ + b)` and `O_H = π[ρ + (1 − ρ)(λ + b)]W_H(F_1)`. It is unchecked: verify or correct it.

## 2. The extensions (paper at `overleaf/paper` commit `01bd5d6`)

| ID | Extension | Where in the paper |
|---|---|---|
| X1 | Fixed-information control (Prop. A.3): with information held fixed, entry does not rise with strength | Sections 4.1–4.2; Appendix A.2 |
| X2 | Value classes: general `G_j` (dispersed) and any prior; the construction "Prop. 2 holds on an open set of strengths and costs for any class pair that differs above the reserve, any prior"; the moderate-value example `h = 2` (entry 0.25 → 0.526805); the dispersed example (uniform half-width 0.05, entry 0.25 → 0.522760); "dispersed classes produce the reversal and point-mass classes with the same means do not"; Cases A, B, C of the class exhibit; more than two classes | Section 5.2; Appendix A.4; Online Appendix A.13, C.4 |
| X3 | Atomless preparation costs (Prop. A.6) | Section 5.1; Online Appendix A.6 |
| X4 | Complementary private signals: investor signal `T` with accuracy `a`, challenger signal `Y` with accuracy `d` | Section 5.3; Appendix A.5 |
| X5 | Access to prices in general (not only the benchmark) | Section 6.1; Appendix A.6 |
| X6 | The payment rule (verifiable-value institution with Nash bargaining, seller share `η`) | Section 6.2; Appendix A.6 |
| X7 | Reserve comparisons (a reserve that excludes the low class) | Section 6.3; Appendix A.7 |

The noise-class result (Prop. A.5) has no slot counterpart and is out of scope.

## 3. Work split

- E1: X2, X5, X6, X7 (the auction-side extensions), and the general-prior Prop. 2 of §1.
- E2: X1, X3, X4 (the extensions that change how information or costs enter), and the general-prior coexistence formulas in the ledger note.
- Then one independent check of each memo by a second, independent member.

For each extension, report: (a) does the statement depend on the trading stage, and how; (b) the slot version
of the statement and its proof or certificate; (c) the paper's numerical example recomputed under calibration
B and, where it differs, A; (d) verdict: holds / holds with change / fails; (e) status label.

## 4. Rules

Follow `TEAM_RULES.md` in this folder (write only in this folder; memos in `memos/`, scripts in
`scripts/<STEM>/`; no tests or assertions; no commit; no hand-off of the task; no browser; slot wrapper for runs over
60 s; at most 3 slots; no AI names; status labels; controlled English). Do not read
`opinions/coordinator_view.md` or the `opinion_*.md` files.
