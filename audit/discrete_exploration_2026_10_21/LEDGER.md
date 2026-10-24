# Task ledger: exploratory study of discrete trading

Started 21 October 2026. The coordinator updates this file after each phase.
Rules for every member: `TEAM_RULES.md`. Questions: `BRIEF.md`, Section 1.

Status values: planned, running, done, checked, failed.

## Coordinator notes

- 21 Oct, before phase 1. A print-only check (`scripts/_coordinator/quick_dlaplace.py`) reproduces the
  arithmetic of the discrete-Laplace candidate:
  - posteriors `m₁ = 0.377541`, `M₁ = 0.622459`;
  - `c_H` window `(B_{r_0}(1/2), B_{r_1}(M₁)] = (4.804167, 5.312161]`;
  - `ρ m₁ Δ_T(r_1) = 0.062923`; `Δ_T(r_0) = 0.016667 < k = 0.02`;
  - entry `0.625` and high-class ownership `0.358422` at `r_1` (good news has probability 1/2 exactly);
  - `B_{r}(M₁)` falls below 5 between `r = 3.6` (5.1219) and `r = 4.0` (4.9956);
  - feedback at `r_1`: a purchase earns `+0.175836` with entry after good news, `+0.058335` without.
    The brief states `+0.060` for the second number. Workstream B must resolve this.
- 21 Oct, phase 1 returns. Points for the synthesis and the checkers:
  - B1 confirms the candidate fix; ceiling `r_C = 3.986097`; buy-only coexistence on about `(1.443, 1.748)`;
    the brief's `+0.060` is `+0.058335`.
  - B2 agrees with B1 to every printed digit and with an independent brute-force check at 2,000 strengths.
    Prop. 3 analog: no trade and full buying coexist on `[1.4433, 1.7479]` (contains 1.55, 1.60, 1.65); with
    challenger mixing a third outcome lies between, and entry is strictly ordered. Price access raises
    proceeds by 0.327 and net surplus by 0.148. Open: single crossing of `r_I`, `r_U` (grid only).
  - C1 (two-sided orders) gives posterior bounds `1/(1+e^{∓2/b})`, the same as the paper's Laplace bounds.
    Its thresholds at `c_H = 6` match the paper: ceiling `3.592659` (paper `r_C = 3.592658519`) and
    no-trade boundary `1.747878` (paper `r_N = 1.747877538`). Check that this match is exact and say why.
  - C8 (reserve after the price) kills entry at `p = h`. This rests on `c_L = 0` plus the tie rule; check it.
    X_C8: for `0 < c_L ≤ 0.1` the seller sets `p = h − c_L/μ` and entry stays at `ρ`; at `c_L = 1`, `c_H = 5`,
    `r = 3` entry returns to 0.625 (proceeds 1.181022). The "unobservable equivalence" claim is refuted.
  - C7 reports interior mixed equilibria of the base discrete-Laplace model at `r ∈ [1.41, 1.44]`, just below
    B1's coexistence interval. The red team must reconcile this with B1 and B2.
    X_C7: the base-model memos agree once their branches and challenger tie rules are explicit. The
    "silence pooling" claim is refuted. Selection matters: another weak-incumbent equilibrium gives entry
    0.5625, which reverses C7's selected comparison.
  - X_C9 confirms C9 (existence with both mixings; exactly three outcomes on [1.575, 1.585]; certificates).
    Limits: the top-flow belief 1 is necessary; under "indifferent challenger prepares" only two outcomes
    remain; the rising branch is about 0.014 wide and uses mixing at indifference; no `(1, −v)` pattern.
  - X_C5: C5 thresholds confirmed (Prop. 2 analog for `ω < 268/1485`; L buys from 2.0267; no equilibrium
    above 2.5988 under T1, repaired by challenger mixing; five equilibria at 0.36). REFUTED: the
    "rent transfer" reading (shareholders gain 0.024 while challenger profit falls 0.307); the 96.67%
    loss of information surplus is confirmed.
  - X_C6 confirms every C6 claim. "c_H = 6 blocks expensive entry" needs `b > 1.9576` (margin 0.023 at
    `b = 2`). The welfare sign depends on `κ`. Challenger mixing adds a third equilibrium for some `κ`.
  - X_C1: all eight C1 claims hold. The matches with the paper are EXACT: `r_C` (the discrete law is the
    Laplace density on the integers, so `M` is identical), `r_N` (it never depends on the noise law),
    `𝔯(k)` and the window ends. `r_U`, entry levels and the Prop. 3 values do not match. New: for `c_H = 5`
    a partial-buy branch on `(1.405430, 1.443322)` has entry rising with strength (0.551 to 0.625) and
    coexists with no trade; for `c_H = 6` a second full-buy/partial-sell branch (entry `ρ`) on `(1.819, 1.840)`.
  - A1 and A2 agree on every comparison target (exact grid counts 1,332,674, 1,332,478 and 196).
    A1 corrections to the brief: the existence of equilibrium needs a top-flow belief near 1 (passive
    beliefs fail for `K < k < 3K/2`); "all-or-nothing" holds at the top flow only; the fixed-experiment
    control is flat at the benchmark.
  - C10: optimal disclosure (a test that passes every H) raises entry to 0.786 at `r_1`, but under optimal
    disclosure entry falls with incumbent strength, so the reversal does not survive disclosure.
    X_C10: the `r = 3` numbers stand; entry under optimal disclosure is not globally monotone (it jumps up at
    a switch near `r = 1.413`), but it still falls from `r = 1.2` to `r = 3`. Concavification needs a stated
    selection; D3 evidence is numerical, not interval-based; T1 is a fixed-bid partial result.
  - C4 returns: no entry cascade (analytical under (NC); for `κ ≥ 0`, `b ≥ 1.82` it follows from `c_H > B_r(1/2)`).
    A second potential challenger makes round-1 trading informative at every strength, so Prop. 2(i) is lost.
    At `c_H = 5` challenger 2's entry falls with strength (0.497 to 0.378); the lone-challenger window does not carry over.
    Open: existence at `κ = −0.5`, `r = 3.6`, `c_H = 4.4` (search found none; the finer search was stopped);
    uniqueness over mixtures at `r = 3, 3.6`. Process note: one 2.5-minute diagnostic ran outside the slot wrapper.
  - X_C4: six claims confirmed, two with correction. No cascade under (NC) holds with pooled prices and mixed
    orders. Corrections: welfare gains are weak (equality at `c_H = 5.8`, `r = 1.2` and `3.6`); C4.3 proves informed
    orders, not a general separation of round-1 prices; the broad scans admit challenger mixing at a tie, which
    the main tie rule excludes; off-path `d_1 = 0` needs a stated completion; "high-class", not "same-class", first
    entrant maximizes the spread.
- 22 Oct, after the report (coordinator check, not yet reviewed by a second member). Buy-only orders at noise scale
  `b = 1` with the paper's `c_H = 6` (`scripts/_coordinator/buyonly_scale.py`, 40-digit flow sums, pure strategies):
  `M₁ = 0.731059` (the paper's `M`), `c_H` window `(4.804167, 6.217155]` (the two-sided window), `r_C = 3.592658519`,
  `r_N = 1.747878`; entry `0.25 → 0.625 → 0.25` at `(1.2, 3, 3.6)`; coexistence `[1.492936, 1.747878]`; full purchases
  unique above `1.872986`. Reason: what matters is the order gap between the classes divided by `b` (one unit
  buy-only, two units two-sided). B2's proofs are stated for any `b > 0`, so they cover `b = 1`.
- Before phase 1, not yet checked (now covered by B1, B2 and the red team, except the items in SYNTHESIS §5): uniqueness against mixed purchases, the no-trade argument at `r_0` over all beliefs,
  truncation error in any numerical solver, and the existence of a Proposition 3 analog.

## Phase 1: derivations, verification, modifications, literature

| ID | Question (brief §1) | Output | Status | Checker |
|---|---|---|---|---|
| A1 | A: three-point model, full characterization with mixed strategies and presence `λ`; table of every paper result | `memos/A_three_point.md` | checked | A2 |
| A2 | A: brute-force enumeration of all equilibria (pure and mixed) of the three-point model, `λ ∈ (0,1]` | `memos/A_bruteforce.md` | checked | A1 |
| B1 | B: discrete-Laplace model, numerical verification of every claim in brief §0 | `memos/B_dlaplace_numeric.md` | checked | B2 |
| B2 | B: discrete-Laplace model, Prop. 2 analog with proof, Prop. 3 analog, welfare, ownership, general prior | `memos/B_dlaplace_theory.md` | checked | B1 |
| C1 | C.1: geometric-count noise with two-sided orders `{−1, 0, 1}` | `memos/C1_two_sided.md` | checked | X (phase 2) |
| C2 | C.2: two trading rounds before entry; does information aggregate? | `memos/C2_two_rounds.md` | checked | X (phase 2) |
| C3 | C.3: option to delay preparation and watch another price | `memos/C3_delay.md` | checked | X (phase 2) |
| C4 | C.4: several potential challengers in sequence; cascades | `memos/C4_sequential.md` | checked | X (phase 2) |
| C5 | C.5: informed investor with a stake; manipulation by buying | `memos/C5_stake.md` | checked | X (phase 2) |
| C6 | C.6: costly information acquisition by the investor | `memos/C6_info_acquisition.md` | checked | X (phase 2) |
| C7 | C.7: incumbent responds to the price (jump bids, preemption) | `memos/C7_incumbent.md` | checked | X (phase 2) |
| C8 | C.8: seller sets the reserve after it observes the price | `memos/C8_reserve.md` | checked | X (phase 2) |
| C9 | C.9: unequal noise with challenger mixing; discrete Prop. 3 | `memos/C9_unequal_mixing.md` | checked | X (phase 2) |
| C10 | C.10: other modifications (challenger trades before entry; target disclosure) | `memos/C10_other.md` | checked | X (phase 2) |
| D1 | D: literature on discrete feedback models, dynamics, sequential entry, real options, manipulation | `memos/D_literature.md` | done | red team |

## Phase 2: independent checks

Each headline proposition of A–C gets a second derivation or a brute-force check by a second,
independent member. The checker reproduces or refutes the claim. It does not explore further.
A1 and A2, and B1 and B2, check each other.

| ID | Checks | Output | Status |
|---|---|---|---|
| X_C1 | C1 headline claims; exact match of thresholds with the paper's `r_N`, `r_C` | `memos/X_C1_check.md` | done |
| X_C2 | C2 headline claims | `memos/X_C2_check.md` | done |
| X_C6 | C6 headline claims | `memos/X_C6_check.md` | done |
| X_C8 | C8 headline claims; robustness of `p = h` for `c_L > 0` | `memos/X_C8_check.md` | done |
| X_C9 | C9 headline claims; existence proof; exact certificates | `memos/X_C9_check.md` | done |
| X_C7 | C7 headline claims; belief rule for the bid; base-model mixed branches near `r = 1.41–1.44` vs B1 | `memos/X_C7_check.md` | done |
| X_C10 | C10 headline claims; concavification with several equilibria | `memos/X_C10_check.md` | done |
| X_C3 | C3 headline claims; game form after waiting; grid-based claims | `memos/X_C3_check.md` | done |
| X_C5 | C5 headline claims; stake payoff; belief at the unused flow; nonexistence above 2.6 | `memos/X_C5_check.md` | done |
| X_C4 | C4 headline claims (Props. C4.1–C4.4, Results 8 and 10) | `memos/X_C4_check.md` | done |

## Phase 3: red team and synthesis (done)

`memos/RED_TEAM.md` (verdict table, reconciliation points 1–6, refuted claims) and `memos/SYNTHESIS.md`
(verdicts, survival table, ranked modifications, recommendation, open items). Check scripts in `scripts/RED_TEAM/`.
X_C4 was complete when the red team reached C4, so no item is pending. The coordinator clarified one sentence in
each plain summary ("the five claims named for review": one number in the brief, four claims in the memos).

## Phase 4: report (done)

- Round 1 (`scripts/REPORT/report_qa_r1.md`): 0 high, 0 medium, 3 low (memo filenames broke at 390 px; chart
  subscripts about 9 px; favicon 404). The coordinator applied the fixes: the memo index uses stacked rows,
  subscripts use 0.9em, and a data-URI favicon. The page before the fixes is `scripts/REPORT/report_r1_before_fixes.html`.
- Round 2 (`scripts/REPORT/report_qa_r2.md`): all three fixes confirmed at 728 px and 390 px, light and dark;
  no new problems; zero console errors.
- After round 2 the coordinator spelled out the tie rule that the page labelled "(C1)" in two places, so that it does
  not collide with the name of workstream C1. This is a text change only.

`report.html` in the style of `audit/alex_meeting_2026_10_21/report.html`. Visual check at 728 px and
390 px, light and dark, through the shared browser. Then fixes and a second check.
