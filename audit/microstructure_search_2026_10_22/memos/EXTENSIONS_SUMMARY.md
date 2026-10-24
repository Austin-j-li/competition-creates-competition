# Extensions under the order slot: summary (coordinator, 23 October 2026)

This is the coordinator's summary of Phases 4 and 5 (`LEDGER.md`). It is not a team member's memo.
Every verdict below comes from one member's memo and an independent check by a second, independent member.

## 1. The paper's extensions under the slot (fixed λ)

| Extension | Verdict | Change to the paper | Memos |
|---|---|---|---|
| General-prior Prop. 2 | holds with corrected hypotheses: `B_0(π) < c_H < B_1(M)`, `Δ_0 < k < ρ min{m, 1 − M} Δ_1`, `B_2(M) < c_H`; ownership rises iff `[ρ + (1 − ρ)(b + λ)]W_H(F_1) > ρW_H(F_0)` | none (the first condition is already in the paper's Prop. 2) | E1, XE1 |
| Value classes and any prior (two classes) | holds; every paper example works with its own costs and strengths | entry levels differ | E1, XE1 |
| More than two classes | fails at a knife-edge (two orders share one price; a 0.001 change separates them; entry unchanged) | rewrite one sentence | E1, XE1 |
| Fixed-information control | holds as "does not rise" (entry flat at fixed information) | wording in abstract, introduction, Section 4.2, Table 2B | E2, XE2 |
| Atomless preparation costs | holds (strong entry 0.522757 at calibration B) | none | E2, XE2 |
| Complementary private signals | holds (entry 0.85 → 0.879797; the same six signal pairs) | none | E2, XE2 |
| Access to prices | holds where a buy recruits | break-even trade scale about 6.85 instead of 1.83 | E1, XE1 |
| Payment rule | holds | none | E1, XE1 |
| Reserve comparisons | holds, weaker: flat at the paper's exclusion reserve; strict deterrence needs reserve 1.55, which excludes the weak incumbent | rewrite one sentence | E1, XE1 |

The common cost: with only three prices, entry moves in steps, so strict entry comparisons at fixed orders become flat.

## 2. New extensions in the slot set-up

| Extension | Result | Status after check | Memos |
|---|---|---|---|
| Costly research with a success cap (Dow–Gorton) | Zero research unique at 1.2; at 1.55, 1.60, 1.65 research 0.2502 → 0.2933 → 0.3326 and entry 0.5313 → 0.5367 → 0.5416, beside a no-research equilibrium (two equilibria under the paper's tie rule); research at the cap uniquely at 3 and 3.6 (entry 37/68, then 1/4) | analytical; confirmed; list complete. Needs cap in (0.3166, 0.3648) and cost in about (0.0155, 0.0333); quadratic cost assumed | N3, XN3 |
| Informed timing (choice of date) | the cap on beliefs and the return to the floor survive any number of slots; a delayed sale appears | confirmed with correction: the early-buy, late-sale pattern is one of two equilibria | N2, XN2 |
| Several informed arrivals | the floor at 3.6 caps total informed volume before the decision | confirmed with correction | N2, XN2 |
| Poisson arrivals | the return to the floor fails at every arrival rate | confirmed | N2, XN2 |
| Manipulation by an uninformed holder | the holder never sells; manipulation raises proceeds only near its onset and destroys most discovery surplus; a rising-entry branch exists | rising entry refuted as unique | N4, XN4 |
| Liquidity foundation | a holder with forced liquidity shocks implements the slot's liquidity trader | confirmed without uniqueness | N4, XN4 |
| Challenger and incumbent trading in the slot | thresholds corrected (multiplicity above 0.0804; incumbent threshold 0.0599, not 0.0765) | corrected / refuted as stated | N4, XN4 |
| Observables (spread, informed share, winner prediction, event returns) | the spread at 3 is 90.4% the value of entry and collapses at the ceiling | not checked | N1 |

## 3. Recommendation

The order slot with costly research keeps Prop. 2 (unique outcomes), coexistence with strictly rising entry at
1.55, 1.60, 1.65, the welfare result, and every old extension in substance. It still loses the partial sale
(1, −v), except as one timing equilibrium. Added assumptions: an exogenous liquidity motive (with a forced-shock
foundation), a research cap inside the benchmark band, a quadratic research cost, and a unit order menu.

Open: the research result is verified at calibration A only (β = 1/3, cap 6/17), not at calibration B; the old
extensions were checked with fixed λ, not re-derived with endogenous research; entry levels differ from the paper's.
