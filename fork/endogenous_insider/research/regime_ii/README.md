# Regime II test of Proposition 2

Question: replace the floor (A1), $0\le c_L<B_{r_1}(m)$, by the regime II condition (A1'), $B_{r_1}(m)<c_L<B_{r_1}(\tfrac12)$, and decide which parts of Proposition 2 survive. The classification of cost laws by regime is in `../cost_distribution/note.md`.

## Reading order

1. `note.md` (this folder): the verdict, Proposition 2', the counterexamples, the map over $(c_L,r_1)$, the recommendation and draft wording for the paper, open items, and the list of refuted claims. Read this first.
2. `check_theory/review.md` and `check_numerics/review.md`: the two referee reports. Every claim in `note.md` is stated as these reports left it.
3. `theory/note.md`: results R.1 to R.12, Proposition 2', the proofs, Tables 1 to 3. Referee fixes are marked in place.
4. `adversary/note.md`: Theorem AD.1 (the cheap-type share), the verified $\rho=0.6$ example, the $\rho$ curve, the attack ledger, the economics, and a draft paragraph. Referee fixes are marked in place.
5. `numerics/note.md`: the sweeps, the all-pool LP, the mixed audit, the region map over $(r_1,\rho)$, the low-trade family, part (iii). Referee fixes are marked in place.
6. `board.md`: the dated coordination log of all tracks.

## Files by folder

| folder | contents |
|---|---|
| `note.md`, `README.md` | synthesis: verdict note and this file |
| `synthesis/map.py`, `synthesis/map.csv` | (A4') thresholds, $\sup K$ and the largest $r_0$ for (A3') over $r_1$ at $\rho=0.25$; reuses `theory/formulas.py`; run `python3 map.py` in that folder |
| `board.md` | team board, append-only |
| `theory/` | `note.md`; `formulas.py` (closed forms: levels, pool cap, forcing bound $K$, knapsack, half-line and starved families); `thresholds.py` (writes `constants_r1.csv`, `knapsack_r1.csv`, `thresholds_r1.csv`, `starved_r1.csv`, `starved_checks.csv`, `example_r1.csv`); `checks.py` (writes `checks_roc.csv`, `checks_forcing.csv`, `checks_forcing_map.csv`, `checks_island.csv`, `checks_break.csv`) |
| `numerics/` | `note.md`, `tables.txt`, `fig_regime_ii.pdf`; engine and solvers (`engine.py`, `scan.py`, `search.py`, `partial.py`, `starved.py`, `knapsack.py`, `pool_lp.py`, `mixed.py`, `island.py`, `thresholds.py`, `lp_map.py`, `lp_refine.py`, `kscan.py`, `klow.py`, `rho_check.py`, `run_*.py`); independent verifier (`verify.py`, `verify_csv.py`); renderer (`render.py`); `run_all.sh`; equilibrium, summary, threshold, LP and verification CSVs |
| `adversary/` | `note.md`; `model.py` (economy, closed forms, knapsack, quadrature, certificate); `attack.py` (writes `rho_star.csv`, `rho_floor.csv`, `rho_curve.csv`, `halfline_thresholds.csv`, `a3prime_feasible.csv`, `counterexamples.csv`, `starved_hcheck.csv`, `mixed_window.csv`) |
| `check_theory/` | `review.md`; `referee.py`, `run_checks.py` (writes `table1_check.csv`, `thresholds_check.csv`, `starved_a3.csv`, `starved_closed.csv`, `starved_closed_confirm.csv`, `candidate_counter.csv`, `partial_outside_a3.csv`, `jgap.csv`, `random_forcing.csv`) |
| `check_numerics/` | `review.md`; `model.py`, `bathtub.py`, `starved.py` and one script per CSV (`thr_bathtub`, `table1_check`, `sweep_k02`, `starved_members`, `starved_thr`, `forcing_map`, `break_check`, `fixed_point_scan*`, `refine_fp`, `mixed_audit`, `random_tests`, `rho_check`, `rho_curve`, `halfline_check`, `lowtrade`, `collapse`, `r0check`, `last_bits`, `kcheck`, `window_neg`) |

## Status rule

Analytical, computer-assisted, numerical diagnostic, open, as in the paper. By Online Appendix C.2 a floating-point quadrature check without an interval enclosure is a numerical diagnostic. Where a track note says "computer-assisted" for such a check, read "numerical diagnostic". No number in this folder is an interval enclosure.

## Benchmark

$h=10$, $\ell=1$, $p=\tfrac12$, $b=2$, $c_H=6$, $r_0=1.2$, $r_1=3$, $k=0.02$, $\rho=0.25$. At $r_1=3$: $B(m)=2.3662$, $B(\tfrac12)=4.2917$, $B(M)=6.2172$, $\Delta_T=\tfrac23$. Regime II at $r_1$ is $c_L\in(2.3662,4.2917)$; the paper's $c_L=1$ is regime I.
