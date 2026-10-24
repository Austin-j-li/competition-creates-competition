# P3: Competition creates research (R10 at general β and calibration B)

Status: complete, round 2, 23 October 2026. Proof package: `proofs/P3_research.tex` (15 pages, compiles to
`proofs/build/P3_research.pdf`). Scripts and logs: `scripts/P3_research/`. Registry: `registry/P3_research.csv`
(138 rows). Receipt with hashes: `scripts/P3_research/run_receipt.json`.

## Model and equilibrium

Before it learns the class, the investor chooses a private research intensity λ ∈ [0, λ̄] at cost (a/2)λ².
With probability λ it learns the class and fills the slot. Otherwise a liquidity trader fills it. Market makers
price with the conjectured intensity λ̂. The equilibrium is the tuple (λ̂, σ_H, σ_L, P, μ, ζ, bids). It
satisfies P1's conditions E1–E6 at intensity λ̂ and a seventh condition, E7 (research optimality). A joint
deviation (z, σ′) holds P and ζ fixed. Lemma 1 reduces it to z* = min{λ̄, V/a}, where V is the expected optimal
trading payoff after a success. Calibration B: cap λ̄ = λ_B = 0.336122, cost a = 1/40 (kept: every claim holds
at B).

Notation: the package follows LABELS §1 and P1 (IM/I0, C1/CM, b, b₀, M, m, the condition numbers). The
probability of order x in class j is f_j(x); the posterior, the price and entry are μ(x), P(x) and e(x). P1 writes
a_j(x) for f_j(x). The letter a is the research cost. A proof that names the investor's order uses q as the
argument, as in U_j(q) and P(q). The preparation probability after order x is ζ_x = ζ(P(x)).

## Results

| Result | Status |
|---|---|
| Joint-deviation lemma; posterior bounds for every profile; positive research needs a strict full purchase | analytical |
| r₀ = 6/5: zero research is unique (every tie rule); the general statement needs B_r(1/2) < c_H | analytical |
| r = 1.55, 1.60, 1.65: the equilibrium set is {zero research, research branch} under C1, plus one threshold equilibrium under CM; investor rule irrelevant | analytical; values computer-assisted |
| Branch: λ_R′(r) > 0 and entry ρ + (1−ρ)[β + (1/2 − β)λ_R] rises strictly (general β ≤ 1/3) | analytical |
| Branch interval at B: [r_R, r̄_R) = [1.501023, 1.677633); zero research coexists on all of it (r_N = 1.747878) | computer-assisted |
| r₁ = 3 and r₂ = 18/5: research at the cap is unique; entry 0.522757 and 0.25 (the fixed-λ outcome) | analytical, interval margins |
| r ∈ (r_U^R, h), r_U^R = 2.434046: research at the cap is unique. The full tuple is unique under C1, and under CM at every r ≠ r_C = 3.592659. At r_C under CM, each ζ₁ ∈ [0, 1] is an equilibrium, and entry fills [1/4, 0.522757] | analytical, interval margins |
| Admissible region: the claims hold with strict margins iff λ_E(3) < λ̄ < λ_E(18/5) and a_lo(λ̄) < a < a_up | computer-assisted |
| General β (cap λ_B(β), u = e − 1, a = 1/40): the claims hold for every β ∈ (0.236157, 1/3] | computer-assisted |
| Price access at r₁: proceeds +0.257948, net surplus +0.081960; research and trading costs equal in both economies | analytical, interval values |

Values at B:

| r | λ_E | research λ_R | purchase posterior | entry | threshold e* (CM) | threshold entry (CM) |
|---|---|---|---|---|---|---|
| 1.55 | 0.196741 | 0.237901 | 0.673142 | 0.507630 | 0.865703 | 0.456294 |
| 1.60 | 0.199698 | 0.279037 | 0.698206 | 0.513965 | 0.758777 | 0.420777 |
| 1.65 | 0.202664 | 0.316683 | 0.720112 | 0.519763 | 0.673748 | 0.392494 |

Along the branch, research rises from 0.193853 at r_R to the cap at r̄_R. Entry rises from 0.500846 to 0.522757.
On [r̄_R, r_N) research sits at the cap, and entry is flat at the fixed-λ level. The threshold entry under CM falls
across the three points, as at calibration A.

## Admissible region at B

- Cap strip: (0.290539, 0.336721). λ_B sits 0.045583 above the lower end and 0.000599 below the upper end.
- The upper end is the tightest hypothesis, λ̄ < λ_E(18/5). Its margin has two coordinates:
  - in research intensity: λ_E(18/5) − λ_B = 0.000599;
  - in posterior probability: τ(18/5) − M = 0.000334.
- The two numbers measure the same boundary and are not equal. They have the same sign because M_λ rises strictly
  in λ. The margin comes from the fixed-λ calibration. Research does not change it, because research sits at the
  cap at 18/5.
- Cost window at λ_B: (0.021469, 0.036763). a = 1/40 has margins 0.003531 and 0.011763.
- At a = 1/40 the cap range is (0.316683, 0.336721).
- The window is nonempty on the whole strip. The endpoint cost limits (uniform bound at 3: ≥ 0.073556; cap at
  18/5: ≥ 0.127845) never bind. Table 3 of the package lists the window at seven caps.

## What the quadratic cost does

1. Strict concavity gives a unique research response, so no equilibrium needs indifference over research.
2. The zero marginal cost at zero makes zero research an equilibrium exactly when ρΔ_T ≤ 2k, given B_r(1/2) < c_H
   (floor entry at the uninformative price). This condition does not involve a.
3. The rising marginal cost meets the falling research value (more research removes camouflage) once. The root moves
   smoothly with r, so entry rises strictly. A linear cost gives a bang-bang choice, so the branch would need investor
   indifference over research.

## Tie rules

Every trade choice at the six strengths is strict, so the investor rule (IM or I0) plays no role there. At the six
strengths, the challenger rule matters only for the threshold equilibrium, which exists under CM on (r_R, r_N).
Among strong incumbents, the challenger rule matters only at the entry ceiling r_C. Research never has a tie.

## Checks

- The shared formulas of TEAM_RULES §3 agree with equations (4) and (9) of the pinned manuscript. The program also
  checks t₀, t_H, t_L, g_H, g_L, S₀, S_H and S_L against direct integration over R at the six strengths. No
  difference.
- At calibration A (β = 1/3, cap 6/17) the program reproduces N3 and XN3: research 0.250249, 0.293325, 0.332615
  and entry 0.531281, 0.536666, 0.541577.
- At r₁ the research model gives entry 0.522757 and r_C = 3.592659, the brief's fixed-λ values. It also gives
  r_A = 1.393958 and r_N = 1.747878.
- A floating-point scan (numerical diagnostic, rule C1) does not use the classification. At each of the six strengths
  it finds exactly the equilibria of the exact enumeration.

## Relation to the brief and the earlier memos

No claim of the brief or of N3, XN3 and EXTENSIONS_SUMMARY is refuted.

- The brief's quick check (research ≈ 0.24, 0.28, 0.32; entry ≈ 0.508, 0.514, 0.520) is confirmed.
- The cap and cost ranges of N3, XN3 and EXTENSIONS_SUMMARY ((0.3166, 0.3648) and about (0.0155, 0.0333)) are the
  calibration-A values. At B they become (0.290539, 0.336721) and (0.021469, 0.036763) at λ_B.
- The general list of equilibria at intermediate strengths states the condition λ_E(r) ≠ λ̄. At λ_E(r) = λ̄, rule CM
  admits an interval of threshold equilibria at the cap; the XN3 enumerator carries this case as a separate type.
  At B, λ_E(r) < λ̄ on (1, r_N].
- The research branch starts at r_R = 1.501023, after the fixed-λ start r_A = 1.393958. At r_R the purchase must
  also pay the marginal research cost: Δ_T(1 − τ) = k + 2aλ_E.

## Open

The equilibrium set on (r_N, r_U^R) = (1.747878, 2.434046) is outside the claims. Exact enumeration with the same
type list (printed only, section J of the run log) gives this. At 1.8 and 2.0, rule IM has two equilibria: research
at the cap with a low-class sale mixture (entry 0.522757), and low research with floor entry. Rule I0 keeps only the
second. At 2.2 and 2.4, research at the cap is unique. This package proves no claim on that interval.

## Round 2 changes

The check XP3 (`memos/XP3_check.md`) confirmed every calibrated claim and asked for four corrections. Each XP3 item
and the change it caused:

| XP3 item | Verdict | Change in round 2 |
|---|---|---|
| 1. Equilibrium and joint deviations | confirmed | None. |
| 2. Complete sets at six strengths | confirmed | None. |
| 3. Branch values, interval and slope | confirmed | None. |
| 4. Endpoint uniqueness (§5.4) | corrected | Accepted. Proposition 4 (strong incumbents) now has a case for M_λ̄ = τ(r). At B the scope is r ∈ (r_U^R, h). Under C1 the tuple is unique there. Under CM it is unique for r ≠ r_C. At r_C, each ζ₁ ∈ [0, 1] is an equilibrium, and entry fills [1/4, 0.522757]. The proof shows that τ rises strictly on (ℓ, h), so r_C is the only exception. The run log prints the margin of (U) at r_C. |
| §5.5 Weak incumbent (under item 4) | corrected | Accepted. Proposition 1 now assumes B_r(1/2) < c_H. A new paragraph shows that entry is 1 without this hypothesis. The margins table lists Proposition 1 under this hypothesis. The memo states the same hypothesis for the zero-research condition ρΔ_T ≤ 2k. |
| 5. Admissible region (§6.3) | corrected | Accepted. The memo and the package now give the two margins of λ̄ < λ_E(18/5) separately: 0.000599 in research intensity and 0.000334 in posterior probability. The word "equals" is gone. The package no longer ranks margins of different units. |
| §6.1 Strict growth alone (under item 5) | remark | No change. Proposition 5 names its claim set: three interior research choices. XP3 shows that strict entry growth alone permits a wider cost window. The narrower window is correct for the stated claims. |
| 6. Price access | confirmed | None. |
| 7. Registry enclosures (§8.2) | corrected | Accepted. The function `enc` now rounds outward from the exact rational endpoints: the lower end down, the upper end up. An exact value prints as one decimal if it terminates. The program writes the new file `scripts/P3_research/P3_enclosures.json` with the endpoints of all 138 values. |

The program ran again through the slot wrapper. The new program `scripts/P3_research/P3_compare_round2.py` prints
this comparison (log `P3_compare_round2.log`):

- Keys: 138 in both rounds, in the same order.
- The columns value, display, status, source_script and run_log: no differences.
- Notes: 67 rows changed, and every change is in an enclosure. 65 are the keys of the XP3 list. In the other two
  (`res_rA`, `res_entry_r2`), the outward pair is one unit wider. The note of `res_rUR` also states the scope
  correction.
- All 67 enclosure notes contain the exact XP3 interval. This includes all 65 keys of
  `scripts/XP3/invalid_enclosures.csv`.
- All 138 rows of `P3_enclosures.json` intersect the exact XP3 intervals.

The notation follows LABELS §1: f_j(x), μ(x), P(x) and e(x). The PDF compiles, and no registry key is unknown.
Round-1 copies of the registry, the log, the package source and this memo are in `scripts/P3_research/` with the
prefix `round1_`.

