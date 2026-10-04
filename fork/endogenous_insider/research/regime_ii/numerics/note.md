# Numerics note: regime II at r1 = 3 and across (r1, rho)

Track: numerics. Folder: `fork/endogenous_insider/research/regime_ii/numerics/`.
Primitives: h = 10, ell = 1, p = 1/2, b = 2, c_H = 6, r0 = 6/5. Unless a table says otherwise: r1 = 3, rho = 1/4, k = 1/50.
At r1 = 3: B(m) = 2.3662, B(1/2) = 4.2917, B(M) = 6.2172, Delta_T = 2/3.

Status words: analytical, computer-assisted, numerical diagnostic, open. A row is "computer-assisted" when an independent
check by adaptive quadrature accepted it at tolerance 1e-8. A search result with no such check is a "numerical diagnostic".
The reversal means E > rho and O_H > rho/2, both strict. At r0 the paper's values are E(r0) = rho and O_H(r0) = rho/2.
Every number below comes from a CSV in this folder. `render.py` reads the CSVs and refreshes the tables; it never solves.
`run_all.sh` replays every step.

## 1. Answers

Replacement of (A1) by (A1'): B_r1(m) < c_L < B_r1(1/2). The lower end is strict: c_L = B(m) is regime I by the tie rule.
At the upper end c_L = B(1/2) the tie rule gives regime II with posterior 1/2.

| Part | Answer from the numerics | Status |
|---|---|---|
| (i) weak incumbent at r0 | Survives. E(r0) = rho and O_H(r0) = rho/2 exactly, for every c_L tested (up to B_r0(1/2) = 1153/240). Zero orders are the only best response because Delta_T(r0) = 1/60 < k = 1/50. | computer-assisted (exact rationals) |
| (ii) at r1: informed trading, informative price, Blackwell order | Survives for c_L in (B(m), 2.9844) at rho = 1/4. Every found equilibrium has orders (1, -1). The price is informative in all of them. At r0 the price is flat, so informative means more informative in the Blackwell order. | numerical diagnostic, rows checked by quadrature |
| (ii) E > rho and O_H > rho/2 | Survives for c_L in (B(m), c*), with c* = 2.9844 at the benchmark. Lowest found values just below c*: E = 0.3764, O_H = 0.2741. [Referee fix: these are the lowest values in the cutoff (half-line) family. Island pools go lower and are accepted at k = 0.02: at c_L = 2.975 the worst pools give E = 0.3444 and O_H = 0.2441, which equal the knapsack infimum, as this note's own all-pool LP reports at c_L = 3.0.] | numerical diagnostic, rows checked by quadrature |
| (ii) uniqueness of the trading outcome | Survives in the same range: (1, -1) is the only trading outcome found. | numerical diagnostic |
| (ii) uniqueness of entry | Fails. Entry is not unique: E runs from 0.376 to 0.423 at c_L = 2.975, over 27 equilibria with different pools. | numerical diagnostic |
| (ii) above c* | Fails. A partial-order equilibrium (1, -v) with a half-line pool has E about 0.11 < rho. First member at c_L = 3.000: v = 0.7344, cutoff 0.461, E = 0.1117, O_H = 0.0773. | numerical diagnostic, member checked by quadrature |
| (iii) collapse at r2 > r1 | Becomes: E <= rho and O_H <= rho/2 whenever B_r2(M) < c_H. Equality holds in regime I. In regime II both are strict. Tested at r2 = 3.8, 4, 5. | numerical diagnostic |
| weakest replacement of (A1) | B_r1(m) < c_L < c*(r1, rho, k). Table in section 7. At the benchmark c* = 2.9844. | numerical diagnostic |
| replacement of (A3) | Left side stays: k > Delta_T(r0). Right side: k must stay below min{k_LT, k_S, k_U} (low-trade edge, starved edge, edge of unique trading). The paper's own right side, (1 - 1/b) rho m Delta_T(r1), is already below k_LT, so it excludes the low-trade band. But at k = 1/50 that right side holds only for rho = 1/4 with r1 >= 2.9 and for rho = 1/2 with r1 >= 2.2, and never for rho = 1/10. Section 9. | numerical diagnostic |

New finding: a low-trade family of equilibria. Both types order less than the full size, the pool is the minimal pool, and
E = rho and O_H = rho/2 exactly. It exists for k between k_LT and rho Delta_T / 2. The no-trade test of the paper is the
top of that band. The paper's (A3) right side lies below the whole band (it is at most 0.37 of k_LT in every row computed),
so a proof under the paper's (A3) never meets this family. The band matters where (A3) fails at k = 1/50. See section 9.

New finding: a high-rho break. For rho >= 0.5154 no equilibrium has E > rho in regime II at r1 = 3. See section 8.

## 2. Method

- Engine (`engine.py`). Auction values, posteriors, entry sets and payoffs by Gauss-Legendre panels (14 nodes, flow range 80,
  panel width 4). Tie rule 1e-13. It reproduces the benchmark: regime I gives E = 0.5228, O_H = 0.3242.
- Cutoff scan (`scan.py`, `search.py`). Best-response iteration for pure orders from 10 starts at every half-line pool
  cutoff (step 0.05), with continuation and bisection at the end of each branch. A candidate is kept when the pool belief is below
  tau_L and both regrets are at most 1e-9. Starts that do not converge are counted and reported as open.
- Exact window solver (`partial.py`). For orders (1, -v) and a half-line pool it follows each fixed point of the low type's
  best response to the end of its consistent range. The engine confirms both types. This finds windows narrower than the scan step.
- Low-trade search (`partial.py`). Symmetric orders (q, -q) on a grid with root finding, then best-response iteration from small starts.
- Island search (`knapsack.py`, `pool_lp.py`). A linear program over all pools for fixed pure orders. `knapsack.py` uses the sufficient
  test J >= k/(1 - 1/b) and full orders. `pool_lp.py` uses the exact deviation conditions on a lattice of orders (a relaxation, so the
  minimum is a lower bound). Every minimiser is polished by best-response iteration and checked by the engine.
- Mixed profiles (`mixed.py`). Count of local maxima of each type's payoff over random consistent schedules, and a lattice search
  for two-atom mixtures.
- Verification (`verify.py`, `verify_csv.py`). Adaptive quadrature (QUADPACK) with no engine code. It rebuilds auction values, the
  posterior, the pool belief and the global best response of both types. A row is accepted only if the pool is consistent and both regrets are below 1e-8.
- Software: Python 3, numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.2.
- Tolerances were never loosened. A node that did not converge stays open.

## 3. Exact values at the weak strength r0 = 6/5

<!-- T:r0 -->
| rho | c_L values tested | E(r0) | O_H(r0) | no trade unique | Delta_T(r0) | k | B_r0(1/2) |
|---|---|---|---|---|---|---|---|
| 1/10 | 6 | 1/10 | 1/20 | yes | 1/60 | 1/50 | 1153/240 = 4.804167 |
| 1/4 | 6 | 1/4 | 1/8 | yes | 1/60 | 1/50 | 1153/240 = 4.804167 |
| 1/2 | 6 | 1/2 | 1/4 | yes | 1/60 | 1/50 | 1153/240 = 4.804167 |
<!-- /T:r0 -->

Both values are rational and equal to rho and rho/2. The price is flat at r0, so the Blackwell comparison at r1 only needs an informative price at r1.

## 4. The sweep at r1 = 3

The grid runs from c_L = 2.30 to 4.35 in steps of 0.025, plus the ties c_L = B(m) and c_L = B(1/2).
Files: `eq_r3_rho0.25.csv` (every equilibrium: orders, E, O_H, pool probability, pool belief, informativeness, reversal flag),
`summary_r3_rho0.25.csv` (one row per c_L). Same files for rho = 0.1 and 0.5.

<!-- T:sweep025 -->
| c_L | regime | equilibria | family at lowest E | orders (q_H;q_L) at lowest E | E range | O_H range | unconverged starts | price informative in all | only (1,-1) found | reversal in all | reversal in some |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.3000 | I | 1 | full-minimal | (1.0000;-1.0000) | 0.5228 to 0.5228 | 0.3242 to 0.3242 | 0 | true | true | true | true |
| 2.3500 | I | 1 | full-minimal | (1.0000;-1.0000) | 0.5228 to 0.5228 | 0.3242 to 0.3242 | 0 | true | true | true | true |
| 2.3662 | I | 1 | full-minimal | (1.0000;-1.0000) | 0.5228 to 0.5228 | 0.3242 to 0.3242 | 0 | true | true | true | true |
| 2.3700 | II | 3 | full-pool | (1.0000;-1.0000) | 0.4331 to 0.4372 | 0.3000 to 0.3012 | 0 | true | true | true | true |
| 2.4000 | II | 8 | full-pool | (1.0000;-1.0000) | 0.4245 to 0.4364 | 0.2974 to 0.3010 | 0 | true | true | true | true |
| 2.5000 | II | 14 | full-pool | (1.0000;-1.0000) | 0.4111 to 0.4339 | 0.2924 to 0.3003 | 0 | true | true | true | true |
| 2.6000 | II | 17 | full-pool | (1.0000;-1.0000) | 0.4019 to 0.4314 | 0.2883 to 0.2996 | 0 | true | true | true | true |
| 2.7000 | II | 20 | full-pool | (1.0000;-1.0000) | 0.3942 to 0.4291 | 0.2845 to 0.2988 | 0 | true | true | true | true |
| 2.8000 | II | 22 | full-pool | (1.0000;-1.0000) | 0.3874 to 0.4268 | 0.2807 to 0.2981 | 0 | true | true | true | true |
| 2.9000 | II | 24 | full-pool | (1.0000;-1.0000) | 0.3810 to 0.4246 | 0.2770 to 0.2974 | 0 | true | true | true | true |
| 2.9500 | II | 26 | full-pool | (1.0000;-1.0000) | 0.3779 to 0.4235 | 0.2751 to 0.2970 | 0 | true | true | true | true |
| 2.9750 | II | 27 | full-pool | (1.0000;-1.0000) | 0.3764 to 0.4230 | 0.2741 to 0.2969 | 0 | true | true | true | true |
| 3.0000 | II | 29 | partial-pool | (1.0000;-0.7344) | 0.1117 to 0.4225 | 0.0773 to 0.2967 | 0 | true | false | false | true |
| 3.0250 | II | 30 | partial-pool | (1.0000;-0.7214) | 0.1105 to 0.4220 | 0.0764 to 0.2965 | 0 | true | false | false | true |
| 3.1000 | II | 33 | partial-pool | (1.0000;-0.6819) | 0.1069 to 0.4204 | 0.0739 to 0.2959 | 0 | true | false | false | true |
| 3.2500 | II | 40 | partial-pool | (1.0000;-0.6005) | 0.0999 to 0.4173 | 0.0687 to 0.2948 | 0 | true | false | false | true |
| 3.5000 | II | 51 | partial-pool | (1.0000;-0.4531) | 0.0883 to 0.4124 | 0.0595 to 0.2929 | 0 | true | false | false | true |
| 3.7500 | II | 68 | partial-pool | (1.0000;-0.2459) | 0.0753 to 0.4077 | 0.0490 to 0.2909 | 9 | true | false | false | true |
| 4.0000 | II | 94 | partial-pool | (1.0000;-0.0000) | 0.0638 to 0.4031 | 0.0397 to 0.2889 | 100 | true | false | false | true |
| 4.2917 | II | 99 | partial-pool | (1.0000;-0.0000) | 0.0638 to 0.3978 | 0.0397 to 0.2863 | 89 | true | false | false | true |
<!-- /T:sweep025 -->

Reading the table.
- Regime I (c_L <= B(m)) is the control. One equilibrium, (1, -1), E = 0.5228, O_H = 0.3242, no pool. It matches the paper.
- Regime II up to 2.975: all 458 equilibria found have orders (1, -1) and a half-line pool. The trading outcome is unique. Entry is not.
  The pool probability runs from 0.342 to 0.585.
- From c_L = 3.000 a partial-order family appears and the lowest E falls to about 0.11, below rho = 0.25. The grid step 0.025 brackets the exact threshold 2.98437.
- At c_L = 3.75 and above, some best-response starts do not converge. Those nodes are open. The lowest E there is taken from the exact window solver and the LP (section 5).
- c_L above B(1/2) is regime III. The no-trade equilibrium appears there.

Same sweep at rho = 0.1 and rho = 0.5 (rows picked):

<!-- T:sweep01 -->
| c_L | regime | equilibria | family at lowest E | orders (q_H;q_L) at lowest E | E range | O_H range | unconverged starts | price informative in all | only (1,-1) found | reversal in all | reversal in some |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.5000 | II | 14 | full-pool | (1.0000;-1.0000) | 0.3826 to 0.3918 | 0.2763 to 0.2795 | 0 | true | true | true | true |
| 3.0000 | II | 26 | full-pool | (1.0000;-1.0000) | 0.3682 to 0.3872 | 0.2686 to 0.2780 | 153 | true | true | true | true |
| 3.5000 | II | 36 | full-pool | (1.0000;-1.0000) | 0.2914 to 0.3832 | 0.2130 to 0.2765 | 288 | true | true | true | true |
| 4.0000 | II | 62 | partial-pool | (1.0000;-0.9050) | 0.1364 to 0.3794 | 0.0984 to 0.2749 | 288 | true | false | true | true |
<!-- /T:sweep01 -->

<!-- T:sweep05 -->
| c_L | regime | equilibria | family at lowest E | orders (q_H;q_L) at lowest E | E range | O_H range | unconverged starts | price informative in all | only (1,-1) found | reversal in all | reversal in some |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.4000 | II | 8 | full-pool | (1.0000;-1.0000) | 0.4854 to 0.5091 | 0.3292 to 0.3363 | 0 | true | true | false | true |
| 2.5000 | II | 14 | full-pool | (1.0000;-1.0000) | 0.4585 to 0.5041 | 0.3191 to 0.3349 | 0 | true | true | false | true |
| 3.0000 | II | 26 | full-pool | (1.0000;-1.0000) | 0.3862 to 0.4813 | 0.2808 to 0.3278 | 0 | true | true | false | false |
| 3.5000 | II | 36 | full-pool | (1.0000;-1.0000) | 0.2914 to 0.4612 | 0.2130 to 0.3202 | 0 | true | true | false | false |
<!-- /T:sweep05 -->

At rho = 0.1 the reversal holds in every found equilibrium up to B(1/2) (E stays above 0.1). Above c_L = 2.6 many starts do not converge (up to 288), so that claim is open
in the sense of completeness. At rho = 0.5 the reversal fails in every found equilibrium from c_L = 2.6, and in some from 2.4.

## 5. All pools, and the order lattice

Pool LP at r1 = 3, rho = 1/4, k = 1/50. For each pair of pure orders on the lattice (q_H in {1, .8, .6, .4, .2, 0}, q_L in steps of 0.05)
the LP gives the lowest E over all measurable pools. Islands are allowed.

<!-- T:lp -->
| c_L | regime | order pairs feasible | lowest E over all pools | lowest O_H over all pools | orders at lowest E | reversal in all |
|---|---|---|---|---|---|---|
| 2.3662 | I | 0 of 125 | nan | nan |  | false |
| 2.4000 | II | 1 of 125 | 0.4250 | 0.2975 | (1; -1) | true |
| 2.5000 | II | 1 of 125 | 0.4109 | 0.2897 | (1; -1) | true |
| 2.6000 | II | 1 of 125 | 0.3983 | 0.2814 | (1; -1) | true |
| 2.7000 | II | 1 of 125 | 0.3853 | 0.2724 | (1; -1) | true |
| 2.8000 | II | 1 of 125 | 0.3713 | 0.2629 | (1; -1) | true |
| 2.9000 | II | 1 of 125 | 0.3565 | 0.2525 | (1; -1) | true |
| 2.9500 | II | 1 of 125 | 0.3486 | 0.2471 | (1; -1) | true |
| 3.0000 | II | 1 of 125 | 0.3405 | 0.2414 | (1; -1) | true |
| 3.0500 | II | 1 of 125 | 0.3322 | 0.2355 | (1; -1) | true |
| 3.1000 | II | 2 of 125 | 0.1075 | 0.0742 | (1; -0.7) | false |
| 3.5000 | II | 7 of 125 | 0.0885 | 0.0596 | (1; -0.45) | false |
| 4.0000 | II | 21 of 125 | 0.0630 | 0.0381 | (1; -0) | false |
<!-- /T:lp -->

- For c_L in (B(m), 3.05] only the orders (1, -1) are feasible. The lowest E over all pools stays above rho. Islands lower E below the half-line value
  (at c_L = 2.7: 0.385 against 0.394) but never to rho. The lowest O_H stays above 0.23, far above rho/2.
- Seventy-eight polished LP minimisers were exported (`lp_polished.csv`). All were accepted by quadrature.
- A slack-relaxed LP on a finer lattice (q_H step 0.1, q_L step 0.025, slack 2e-5 on each deviation) looks for equilibria the coarse lattice could miss:

<!-- T:relaxed -->
| c_L | order pairs epsilon-feasible | near (1,-1) | elsewhere | elsewhere with an exact equilibrium nearby | lowest E there |
|---|---|---|---|---|---|
| 2.400 | 1 | 1 | 0 | 0 | nan |
| 2.500 | 1 | 1 | 0 | 0 | nan |
| 2.550 | 1 | 1 | 0 | 0 | nan |
| 2.600 | 1 | 1 | 0 | 0 | nan |
| 2.700 | 1 | 1 | 0 | 0 | nan |
| 2.800 | 1 | 1 | 0 | 0 | nan |
| 2.900 | 1 | 1 | 0 | 0 | nan |
| 2.950 | 2 | 1 | 1 | 1 | 0.3853 |
| 2.970 | 2 | 1 | 1 | 1 | 0.3838 |
| 2.980 | 2 | 1 | 1 | 1 | 0.3831 |
<!-- /T:relaxed -->

  Below 2.9 only the neighbourhood of (1, -1) is feasible. At 2.95 to 2.98 one more order pair is almost feasible, (1, -0.675). Polishing moves it back to (1, -1), E = 0.385. So no exact partial equilibrium exists there.
  This agrees with the exact threshold 2.98437. Numerical diagnostic: a lattice and a slack cannot rule out a window narrower than both.

## 6. Mixed profiles

<!-- T:mixed -->
| c_L | consistent schedules sampled | schedules where H has two local maxima | schedules where L has two local maxima | most peaks H | most peaks L |
|---|---|---|---|---|---|
| 2.4 | 1500 | 0 | 0 | 1 | 1 |
| 2.5 | 1500 | 0 | 0 | 1 | 1 |
| 2.6 | 1500 | 0 | 0 | 1 | 1 |
| 2.7 | 1500 | 0 | 0 | 1 | 1 |
| 2.8 | 1500 | 0 | 0 | 1 | 1 |
| 2.9 | 1500 | 0 | 0 | 1 | 1 |
| 2.95 | 1500 | 0 | 0 | 1 | 1 |
| 2.98 | 1500 | 0 | 0 | 1 | 1 |
| 3 | 1500 | 0 | 0 | 1 | 1 |
| 3.5 | 1500 | 0 | 0 | 1 | 1 |
| 4 | 1500 | 0 | 0 | 1 | 1 |
<!-- /T:mixed -->

- Audit. Each row samples 1500 consistent schedules (pure and two-atom orders; half-line and island pools). Each type's payoff has exactly one local maximum every time.
  So the best response is a single order, and no mixture can make a type indifferent between two global maxima on these schedules.
- Bridge. Where two pure equilibria share a pool and differ only in the low type's order, the path between them crosses the plateau posterior tau_H.
  The payoff jumps there and the tie rule puts the crossing on the high side. No bridge mixture is an equilibrium (0 found, c_L from 2.5 to 4.2).
- Lattice search. Two-atom mixtures for one type with the other type pure: 70 combinations of c_L in {2.5, 2.7, 2.9, 2.98, 3.5}, 7 pools (minimal, four half-lines, two islands), both types. 0 found.
- Status: numerical diagnostic. Supports with three or more atoms, and both types mixing at once, are covered only by the audit.

## 7. The region map over (r1, rho)

For each (r1, rho) at k = 1/50 the region is the set of c_L in regime II where no breaking equilibrium is found. Five mechanisms can break the reversal:

1. No trade: an equilibrium with zero orders exists when rho Delta_T(r1) <= 2k. Then E = rho exactly.
2. Low trade: orders (q, -q) with q < 1. Entry is the same as at r0. Section 9.
3. Partial orders: (1, -v) with a half-line pool, found by the window solver and the cutoff grid. E or O_H falls to the r0 value or below.
4. Islands: full orders with a pool that has an island. The LP threshold gives the first c_L with E <= rho (knapsack E) or e_H <= rho (knapsack O_H).
5. Ceiling: B_r1(M) < c_H, so the expensive type never enters and E <= rho. At r1 = 3.6 the ceiling holds.

Table: the c_L range where the reversal holds in every found equilibrium (c_L* is the upper end). "Again on" lists a second range above a broken range.
"All of regime II" means no break was found up to B(1/2).
An asterisk marks a cell where the right side of the paper's (A3), (1 - 1/b) rho m Delta_T(r1) with m = 1/(1 + e) at b = 2, is below k = 1/50.
There the paper's proposition does not apply, but the model still has an answer, and the table gives it. Cells without an asterisk satisfy the right side of (A3).
They are rho = 1/4 with r1 >= 2.9 (8 of 22 cells) and rho = 1/2 with r1 >= 2.2 (15 of 22 cells). No cell at rho = 1/10 satisfies it.

<!-- T:region_map -->
| r1 | rho=0.1 | rho=0.25 | rho=0.5 |
|---|---|---|---|
| 1.5 | empty (no-trade) * | empty (no-trade) * | empty at B(m) (low-trade); holds on 4.042-4.708 * |
| 1.6 | empty (no-trade) * | empty (no-trade) * | 2.625-3.164 (partial) * |
| 1.7 | empty (no-trade) * | empty (no-trade) * | 2.602-2.877 (partial) * |
| 1.8 | empty (no-trade) * | empty at B(m) (low-trade); holds on 3.542-4.619 * | 2.581-2.683 (partial) * |
| 1.9 | empty (no-trade) * | 2.561-4.591 (all of regime II) * | 2.561-2.605 (island, exact LP) * |
| 2 | empty (no-trade) * | 2.541-3.931 (island, exact LP) * | 2.541-2.578 (island E) * |
| 2.1 | empty (no-trade) * | 2.522-3.410 (partial) * | 2.522-2.555 (island E) * |
| 2.2 | empty (no-trade) * | 2.503-3.149 (partial) * | 2.503-2.533 (island E) |
| 2.3 | empty (no-trade) * | 2.485-2.976 (partial) * | 2.485-2.511 (island E) |
| 2.4 | empty at B(m) (low-trade); holds on 4.001-4.452 * | 2.467-2.938 (partial) * | 2.467-2.490 (island E) |
| 2.5 | empty at B(m) (low-trade); holds on 3.319-4.425 * | 2.449-2.946 (partial) * | 2.449-2.469 (island E) |
| 2.6 | empty at B(m) (low-trade); holds on 2.932-4.398 * | 2.432-2.960 (partial) * | 2.432-2.449 (island E) |
| 2.7 | 2.415-4.371 (all of regime II) * | 2.415-2.974 (partial) * | 2.415-2.429 (island E) |
| 2.8 | 2.399-4.345 (all of regime II) * | 2.399-2.984 (partial) * | 2.399-2.410 (island E) |
| 2.9 | 2.382-4.318 (all of regime II) * | 2.382-2.987 (partial) | 2.382-2.391 (island E) |
| 3 | 2.366-4.292 (all of regime II) * | 2.366-2.984 (partial) | 2.366-2.373 (island E) |
| 3.1 | 2.350-3.221 (partial); again on 3.332-4.265 * | 2.350-2.974 (partial) | 2.350-2.355 (island E) |
| 3.2 | 2.334-3.082 (partial) * | 2.334-2.957 (partial) | 2.334-2.337 (island E) |
| 3.3 | 2.319-2.963 (partial) * | 2.319-2.932 (partial) | 2.319-2.320 (island E) |
| 3.4 | 2.303-2.857 (partial) * | 2.303-2.900 (partial) | 2.303-2.304 (island E) |
| 3.5 | 2.287-2.764 (partial) * | 2.287-2.861 (partial) | 2.287-2.288 (island E) |
| 3.6 | empty (ceiling) * | empty (ceiling) | empty (ceiling) |
<!-- /T:region_map -->

Rows by mechanism at r1 in steps of 0.5 (full table of 66 rows: `thresholds.csv`). In the tables, nan means no value: no break was found in regime II, or the test could not be run. It never means zero:

<!-- T:thresholds -->
| rho | r1 | B(m) | B(1/2) | no-trade eq. | ceiling | c_L first break (families) | family | c_L island E (sufficient test) | c_L island O_H (sufficient test) | c_L island (exact LP) | c_L* (least) | binding |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 1.5 | 2.6481 | 4.7083 | true | false | nan |  | nan | nan | nan | 2.6481 | no-trade |
| 0.1 | 2 | 2.5407 | 4.5625 | true | false | nan |  | nan | nan | nan | 2.5407 | no-trade |
| 0.1 | 2.5 | 2.4494 | 4.4250 | false | false | 2.4494 | lowtrade | nan | nan | nan | 2.4494 | lowtrade |
| 0.1 | 3 | 2.3662 | 4.2917 | false | false | nan |  | nan | nan | nan | nan |  |
| 0.1 | 3.5 | 2.2875 | 4.1607 | false | false | 2.7639 | partial | nan | nan | nan | 2.7639 | partial |
| 0.1 | 3.6 | 2.2721 | 4.1347 | false | true | nan |  | nan | nan | nan | 2.2721 | ceiling |
| 0.25 | 1.5 | 2.6481 | 4.7083 | true | false | nan |  | nan | nan | nan | 2.6481 | no-trade |
| 0.25 | 2 | 2.5407 | 4.5625 | false | false | 4.0320 | partial | nan | nan | 3.9307 | 3.9307 | lpexact |
| 0.25 | 2.5 | 2.4494 | 4.4250 | false | false | 2.9456 | partial | 3.6172 | nan | 3.0163 | 2.9456 | partial |
| 0.25 | 3 | 2.3662 | 4.2917 | false | false | 2.9844 | partial | 3.4607 | 3.7408 | 3.2440 | 2.9844 | partial |
| 0.25 | 3.5 | 2.2875 | 4.1607 | false | false | 2.8607 | window | 3.2976 | 3.5808 | 2.9753 | 2.8607 | window |
| 0.25 | 3.6 | 2.2721 | 4.1347 | false | true | nan |  | 2.2721 | 2.2721 | 2.2998 | 2.2721 | ceiling |
| 0.5 | 1.5 | 2.6481 | 4.7083 | false | false | 2.6481 | lowtrade | nan | nan | nan | 2.6481 | lowtrade |
| 0.5 | 2 | 2.5407 | 4.5625 | false | false | 3.2497 | partial | 2.5784 | nan | 2.5806 | 2.5784 | knapE |
| 0.5 | 2.5 | 2.4494 | 4.4250 | false | false | 3.8033 | window | 2.4690 | 3.2707 | 2.4819 | 2.4690 | knapE |
| 0.5 | 3 | 2.3662 | 4.2917 | false | false | 3.7831 | partial | 2.3726 | 3.1301 | 2.3965 | 2.3726 | knapE |
| 0.5 | 3.5 | 2.2875 | 4.1607 | false | false | 3.6525 | partial | 2.2877 | 2.9851 | 2.3156 | 2.2877 | knapE |
| 0.5 | 3.6 | 2.2721 | 4.1347 | false | true | nan |  | 2.2721 | 2.2721 | 2.2998 | 2.2721 | ceiling |
<!-- /T:thresholds -->

Findings.
- At rho = 1/4 the region is (B(m), c*) with c* between 2.86 and 2.99 for r1 from 2.3 to 3.5. At r1 = 3 it is (2.3662, 2.9844).
  The partial family binds. The island threshold of the sufficient test (3.2976 to 3.6480) lies above it. So does the exact-LP island threshold, except at r1 = 2.0.
- At rho = 1/4 and r1 = 2.0 the exact LP binds: c* = 3.9307, below the partial value 4.0320. At rho = 1/2 and r1 = 1.9 it binds too: c* = 2.6046, below the partial value 2.9009.
  These are the two cells where the exact LP finds a confirmed island break that the other solvers miss (last table of this section).
- At rho = 1/2 the island bound binds for r1 >= 2.0: c* is only 0.0002 to 0.04 above B(m). At r1 = 3 it is 2.3726.
- At rho = 1/10 the region is all of regime II for r1 from 2.7 to 3.0. It shrinks for r1 >= 3.1 (partial family: c* = 3.22 at 3.1, 2.76 at 3.5).
  The island threshold has no value at rho = 0.1: the sufficient test cannot be met, so the exact LP over the region is the check (below).
- Small r1 breaks the reversal through no-trade (r1 <= 2.3 at rho = 0.1, r1 <= 1.7 at rho = 0.25) or low-trade (see the table).
- r1 >= 3.6: the ceiling empties regime II.
- At rho = 1/4 and r1 = 1.9 no break was found on all of regime II. Treat it as an isolated point: r1 = 1.8 and r1 = 2.0 are broken.

Cross-check of the threshold solvers against the cutoff scan (528 points, summary_region.csv; regime II points only):

<!-- T:region_check -->
| rho | regime I points: reversal in all | regime I points: reversal fails | below c_L*: scan agrees | below c_L*: no eq. found (open) | below c_L*: scan finds a break (conflict) | at or above c_L*: scan finds a break | at or above c_L*: scan sees no break (low-trade basin, narrow window or island) | at or above c_L*: no eq. found (open) |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 12 of 34 | 22 (no-trade eq.: 18) | 50 | 0 | 0 | 71 | 16 | 5 |
| 0.25 | 19 of 27 | 8 (no-trade eq.: 6) | 59 | 0 | 0 | 77 | 13 | 0 |
| 0.5 | 28 of 30 | 2 (no-trade eq.: 0) | 53 | 1 | 0 | 88 | 4 | 0 |
<!-- /T:region_check -->

Below c_L* the scan never finds a break except where it finds no equilibrium at all (one open point: r1 = 1.6, rho = 0.5, c_L = 2.8969, 146 starts did not converge).
Above c_L* the scan misses some breaks. Reasons: the low-trade basin is narrow for best-response iteration; a starved window just above c* is narrower than the cutoff step; islands are outside the cutoff family.
Each missed break was found by the exact solvers instead. 142 members of the region map, each placed just inside the broken range, were exported and checked by quadrature (`threshold_members.csv`): all 142 accepted.
The regime I controls in the table fail only where the paper's own conditions are violated: a no-trade equilibrium (the large majority), a low-trade equilibrium (r1 = 2.4, rho = 0.1), or the ceiling (r1 = 3.6). They do not fail because of regime II.

Exact LP over the region (`lp_summary_region.csv`):

<!-- T:lpregion -->
| rho | LP points (12 per r1) | no feasible order pair (no equilibrium of the lattice) | other solvers say hold | LP agrees: E and O_H stay above r0 | LP lowers E or O_H to the r0 value or below (island break the other solvers missed) | other solvers say break | LP also sees a break |
|---|---|---|---|---|---|---|---|
| 0.1 | 264 | 34 | 69 | 69 | 0 | 161 | 35 |
| 0.25 | 264 | 29 | 76 | 75 | 1 | 159 | 132 |
| 0.5 | 264 | 20 | 2 | 0 | 2 | 242 | 242 |

Pairs where the exact LP finds a confirmed island break below the other solvers' c_L*:

| rho | r1 | c_L (exact LP) | c_L* of the other solvers | E at the break | O_H at the break | orders |
|---|---|---|---|---|---|---|
| 0.5 | 1.9 | 2.6046 | 2.9009 | 0.5000 | 0.3399 | (1; -1) |
| 0.25 | 2 | 3.9307 | 4.0320 | 0.2431 | 0.1622 | (1; -0.508127) |
<!-- /T:lpregion -->

The exact-LP thresholds in `lp_thresholds.csv` (`lp_refine.py`) are upper bounds on c*. The LP runs on a coarse lattice of orders. A pool it finds is polished and confirmed by the engine, so a break exists at that c_L.
A break at a lower c_L, with orders off the lattice, is not excluded. Thirty-three of the 66 pairs have an exact-LP threshold; each member was re-checked by quadrature (section 11).

## 8. High rho

The adversary track gave a closed form: E < rho in every full-order equilibrium of regime II once rho >= a/(a + pi_0) = 0.5154 (r1 = 3).
The numerics test it with the engine at c_L = B(m) + 1e-4, +0.05 and +0.30.

<!-- T:rho -->
| rho | c_L | equilibria | E range | O_H range | E > rho in all | E > rho in some | reversal in all |
|---|---|---|---|---|---|---|---|
| 0.45 | 2.3663 | 1 | 0.4961 to 0.4961 | 0.3297 to 0.3297 | true | true | true |
| 0.45 | 2.4162 | 9 | 0.4681 to 0.4938 | 0.3210 to 0.3291 | true | true | true |
| 0.45 | 2.6662 | 19 | 0.4231 to 0.4828 | 0.3019 to 0.3259 | false | true | false |
| 0.5 | 2.3663 | 1 | 0.5108 to 0.5108 | 0.3368 to 0.3368 | true | true | true |
| 0.5 | 2.4162 | 9 | 0.4797 to 0.5083 | 0.3272 to 0.3361 | false | true | false |
| 0.5 | 2.6662 | 19 | 0.4297 to 0.4961 | 0.3059 to 0.3326 | false | false | false |
| 0.51 | 2.3663 | 1 | 0.5138 to 0.5138 | 0.3382 to 0.3382 | true | true | true |
| 0.51 | 2.4162 | 9 | 0.4820 to 0.5112 | 0.3284 to 0.3375 | false | true | false |
| 0.51 | 2.6662 | 19 | 0.4310 to 0.4987 | 0.3067 to 0.3339 | false | false | false |
| 0.5154 | 2.3663 | 1 | 0.5154 to 0.5154 | 0.3390 to 0.3390 | false | false | false |
| 0.5154 | 2.4162 | 9 | 0.4832 to 0.5127 | 0.3291 to 0.3383 | false | false | false |
| 0.5154 | 2.6662 | 19 | 0.4318 to 0.5002 | 0.3072 to 0.3346 | false | false | false |
| 0.52 | 2.3663 | 1 | 0.5167 to 0.5167 | 0.3397 to 0.3397 | false | false | false |
| 0.52 | 2.4162 | 9 | 0.4843 to 0.5141 | 0.3297 to 0.3389 | false | false | false |
| 0.52 | 2.6662 | 19 | 0.4324 to 0.5014 | 0.3075 to 0.3353 | false | false | false |
| 0.55 | 2.3663 | 1 | 0.5256 to 0.5256 | 0.3439 to 0.3439 | false | false | false |
| 0.55 | 2.4162 | 9 | 0.4912 to 0.5227 | 0.3334 to 0.3432 | false | false | false |
| 0.55 | 2.6662 | 19 | 0.4363 to 0.5093 | 0.3099 to 0.3393 | false | false | false |
| 0.6 | 2.3663 | 1 | 0.5403 to 0.5403 | 0.3511 to 0.3511 | false | false | false |
| 0.6 | 2.4162 | 9 | 0.5028 to 0.5372 | 0.3395 to 0.3502 | false | false | false |
| 0.6 | 2.6662 | 19 | 0.4429 to 0.5226 | 0.3140 to 0.3460 | false | false | false |
| 0.75 | 2.3663 | 1 | 0.5844 to 0.5844 | 0.3724 to 0.3724 | false | false | false |
| 0.75 | 2.4162 | 9 | 0.5376 to 0.5806 | 0.3580 to 0.3714 | false | false | false |
| 0.75 | 2.6662 | 19 | 0.4628 to 0.5623 | 0.3261 to 0.3661 | false | false | false |
<!-- /T:rho -->

- At rho = 0.5154 the single equilibrium at the floor has E = 0.5154. It is not above rho. For every larger rho the largest E found is below rho at all three c_L.
- The largest E is the minimal-pool equilibrium. It is an equilibrium at all 400 c_L values of a fine grid in regime II, and its E falls with c_L (checked for rho = 0.5154 and 0.6).
- Below 0.5154 the break still bites. At rho = 0.5 and c_L = 2.4162 E runs from 0.4797 to 0.5083. At c_L = 2.6662 the largest E is 0.4961, below rho.
- Example from the adversary: rho = 0.6, c_L = 2.4. All 8 equilibria have E in [0.5097, 0.5382], below 0.6. O_H runs from 0.3419 to 0.3505, above 0.3. All 102 equilibria at rho in {0.5154, 0.6, 0.75} and c_L in {2.4, 3.0} were accepted by quadrature (`rho_check_eq.csv`).
- The adversary's all-pool curve was tested with the LP: at (rho, c_L) = (0.4488, 2.5) the lowest E is 0.44877; at (0.395, 2.8) it is 0.39501. Both match the curve to 1e-5.

## 9. Replacing (A3): the role of k

Tests of the theory track's numbers (r1 = 3, c_H = 6):

<!-- T:theorycheck -->
| rho | island E: theory | mine, k = 0.005 | mine, k = 0.02 | island O_H: theory | mine, k = 0.005 | mine, k = 0.02 |
|---|---|---|---|---|---|---|
| 0.1 | 3.9201 | 3.9201 | nan | 4.0036 | 4.0036 | nan |
| 0.2 | 3.6330 | 3.6330 | 3.6330 | 3.8350 | 3.8351 | nan |
| 0.25 | 3.4607 | 3.4607 | 3.4607 | 3.7408 | 3.7408 | 3.7408 |
| 0.3 | 3.2638 | 3.2638 | 3.2638 | 3.6388 | 3.6388 | 3.6388 |
| 0.35 | 3.0366 | 3.0366 | 3.0366 | 3.5280 | 3.5280 | 3.5280 |
| 0.5 | 2.3726 | 2.3726 | 2.3726 | 3.1300 | 3.1301 | 3.1301 |

| k (rho = 0.25) | starved threshold: theory | mine | difference |
|---|---|---|---|
| 0.02 | 2.984373 | 2.984373 | -5.0e-09 |
| 0.015 | 3.395374 | 3.395374 | -2.4e-09 |
| 0.01 | 3.783083 | 3.783083 | -1.3e-09 |
| 0.0075 | 3.936651 | 3.936651 | -1.9e-10 |
<!-- /T:theorycheck -->

The forcing bound K(c_L) of the theory track (the board, theory 4) is sufficient but far from sharp. Random consistent pools, 1500 draws per row:

<!-- T:forcing -->
| c_L | k | theory K(c_L) | consistent random pools | of them not an equilibrium | largest regret |
|---|---|---|---|---|---|
| 2.4 | 0.008 | 0.00975 | 100 | 0 | 0.0e+00 |
| 2.4 | 0.012 | 0.00975 | 100 | 0 | 0.0e+00 |
| 2.4 | 0.02 | 0.00975 | 100 | 0 | 0.0e+00 |
| 2.4 | 0.04 | 0.00975 | 100 | 0 | 0.0e+00 |
| 2.4 | 0.06 | 0.00975 | 100 | 100 | 3.0e-05 |
| 2.5 | 0.008 | 0.00858 | 228 | 0 | 0.0e+00 |
| 2.5 | 0.012 | 0.00858 | 228 | 0 | 0.0e+00 |
| 2.5 | 0.02 | 0.00858 | 228 | 0 | 0.0e+00 |
| 2.5 | 0.04 | 0.00858 | 228 | 0 | 0.0e+00 |
| 2.5 | 0.06 | 0.00858 | 228 | 228 | 1.3e-04 |
| 2.7 | 0.008 | 0.00745 | 387 | 0 | 0.0e+00 |
| 2.7 | 0.012 | 0.00745 | 387 | 0 | 0.0e+00 |
| 2.7 | 0.02 | 0.00745 | 387 | 0 | 0.0e+00 |
| 2.7 | 0.04 | 0.00745 | 387 | 0 | 0.0e+00 |
| 2.7 | 0.06 | 0.00745 | 387 | 387 | 4.1e-04 |
| 2.9 | 0.008 | 0.00676 | 511 | 0 | 0.0e+00 |
| 2.9 | 0.012 | 0.00676 | 511 | 0 | 0.0e+00 |
| 2.9 | 0.02 | 0.00676 | 511 | 0 | 0.0e+00 |
| 2.9 | 0.04 | 0.00676 | 511 | 0 | 0.0e+00 |
| 2.9 | 0.06 | 0.00676 | 511 | 511 | 7.4e-04 |
<!-- /T:forcing -->

At k = 0.02 and k = 0.04 every consistent random pool is a (1, -1) equilibrium. At k = 0.06 none is. So the true limit is near 0.05 to 0.06, five to seven times K(c_L).
The scan gives the edge of unique trading and of the reversal, c_L by c_L:

<!-- T:kscan -->
| c_L | tau_L | no-trade bound rho Delta_T/2 | theory K(c_L) | k_S (no starved eq. below) | k_U (unique trading outcome below) | k_R (reversal below) |
|---|---|---|---|---|---|---|
| 2.40 | 0.2730 | 0.0833 | 0.00975 | 0.06524 | 0.0574 | 0.0618 |
| 2.50 | 0.2850 | 0.0833 | 0.00858 | 0.06524 | 0.0552 | 0.0696 |
| 2.60 | 0.2970 | 0.0833 | 0.00793 | 0.06561 | 0.0537 | 0.0747 |
| 2.70 | 0.3090 | 0.0833 | 0.00745 | 0.06729 | 0.0524 | 0.0747 |
| 2.80 | 0.3210 | 0.0833 | 0.00708 | 0.07040 | 0.0514 | 0.0751 |
| 2.90 | 0.3330 | 0.0833 | 0.00676 | 0.07185 | 0.0503 | 0.0747 |
| 3.00 | 0.3450 | 0.0833 | 0.00648 | 0.01978 | 0.0199 | 0.0199 |
| 3.20 | 0.3690 | 0.0833 | 0.00601 | 0.01718 | 0.0174 | 0.0174 |
| 3.40 | 0.3930 | 0.0833 | 0.00558 | 0.01495 | 0.0150 | 0.0150 |
| 3.60 | 0.4170 | 0.0833 | 0.00494 | 0.01256 | 0.0126 | 0.0126 |
<!-- /T:kscan -->

- k_S: largest k with no starved equilibrium. k_U: largest k with only (1, -1) found.
  [Referee fix: the k_S and k_U entries are too high at c_L = 2.6 and 2.9, because the starved solver only
  looks at pool cutoffs x' >= 0. With x' free, accepted starved equilibria (both best responses verified by
  independent quadrature) exist at (c_L, k) = (2.6, 0.03) with x' = -0.72 and E = 0.161, (2.9, 0.03) with
  x' = -0.33 and E = 0.147, and (2.9, 0.035) with x' = -0.17 and E = 0.145. All three sit above (A3)'s right
  side 0.0224 at rho = 1/4, so the paper's k = 1/50 and the conclusions of this note are not affected. At
  k = 1/50 the same search with x' of either sign finds no starved candidate at all for c_L up to 2.98.] k_R: largest k with the reversal in all found equilibria (cutoff scan).
- For c_L up to 2.9 the binding edge is k_U, about 0.057 at c_L = 2.4 and 0.050 at 2.9.
- From c_L = 3.0 up the reversal edge is the starved edge. It falls from 0.0199 (c_L = 3.0) to 0.0126 (c_L = 3.6). It matches the theory track's starved thresholds (section 9, first table).
- The scan cannot see the low-trade basin, so k_R over-reports where the low-trade band comes first. The band edge is computed directly:

<!-- T:klow -->
| r1 | rho | c_L | Delta_T(r1) | no-trade bound rho Delta_T/2 | k_LT (low-trade band starts) | k_LT / no-trade bound | q* at the edge | k = 0.02 inside the band |
|---|---|---|---|---|---|---|---|---|
| 3 | 0.1 | 2.40 | 0.6667 | 0.0333 | 0.0248 | 0.745 | 0.870 | no |
| 3 | 0.1 | 2.60 | 0.6667 | 0.0333 | 0.0250 | 0.749 | 0.862 | no |
| 3 | 0.1 | 2.80 | 0.6667 | 0.0333 | 0.0266 | 0.799 | 0.749 | no |
| 3 | 0.25 | 2.40 | 0.6667 | 0.0833 | 0.0621 | 0.745 | 0.870 | no |
| 3 | 0.25 | 2.60 | 0.6667 | 0.0833 | 0.0624 | 0.749 | 0.862 | no |
| 3 | 0.25 | 2.80 | 0.6667 | 0.0833 | 0.0666 | 0.799 | 0.749 | no |
| 3 | 0.5 | 2.40 | 0.6667 | 0.1667 | 0.1241 | 0.745 | 0.870 | no |
| 3 | 0.5 | 2.60 | 0.6667 | 0.1667 | 0.1248 | 0.749 | 0.862 | no |
| 3 | 0.5 | 2.80 | 0.6667 | 0.1667 | 0.1332 | 0.799 | 0.749 | no |
| 2.4 | 0.25 | 2.60 | 0.4083 | 0.0510 | 0.0408 | 0.799 | 0.750 | no |
| 2.6 | 0.25 | 2.60 | 0.4923 | 0.0615 | 0.0481 | 0.781 | 0.790 | no |
| 3.2 | 0.25 | 2.60 | 0.7562 | 0.0945 | 0.0716 | 0.758 | 0.842 | no |
| 3.5 | 0.25 | 2.60 | 0.8929 | 0.1116 | 0.0861 | 0.771 | 0.812 | no |
<!-- /T:klow -->

At r1 = 3 and rho = 1/4 the low-trade band is k in [0.062, 0.083]. It is far above the paper's k = 0.02. For rho = 0.1 the edge is 0.0248 to 0.0266. The paper's k = 0.02 is only 20% below it.
For small r1 the band can contain k = 0.02: that is what empties regime II at (r1, rho) = (2.4 to 2.6, 0.1), (1.8, 0.25) and (1.5, 0.5).

The paper's (A3) and the band. The right side of (A3) is (1 - 1/b) rho m Delta_T(r1) = 0.1344 rho Delta_T(r1) at b = 2. The band starts at k_LT, which is at least 0.745 of the no-trade bound rho Delta_T/2, so at least 0.372 rho Delta_T.
The right side of (A3) is therefore at most 0.37 of k_LT in every row computed. A proof that assumes the paper's (A3) never meets the low-trade family.
Two facts keep the family in the picture. First, any replacement of (A3) that relaxes its right side must still keep k below k_LT.
Second, at the paper's k = 1/50 the right side of (A3) holds only for rho = 1/4 with r1 >= 2.9 and for rho = 1/2 with r1 >= 2.2, and never for rho = 1/10 (the asterisks in section 7).
In the other cells the low-trade band can bind. It does at five cells of the region map: r1 = 2.4 to 2.6 at rho = 1/10, r1 = 1.8 at rho = 1/4, and r1 = 1.5 at rho = 1/2. All five carry an asterisk.

Replacement for (A3), as the numerics see it at r1 = 3, rho = 1/4, c_L in (B(m), 2.9]:
Delta_T(r0) = 1/60 < k < about 0.050. For c_L above 2.9 the upper edge is the starved edge: k < 0.0199 at c_L = 3.0.
In general the upper edge is min{k_LT, k_S, k_U}(r1, rho, c_L). The right side as the theory track reads it from the paper (k <= 0.0224 at the benchmark) is below that edge in regime II for c_L up to 2.9,
so there (A3) is sufficient and not sharp. At c_L = 3.0 the starved edge 0.0199 is below 0.0224: (A3) no longer protects the reversal, and the partial family breaks it at k = 1/50.

Sufficient candidate of the theory track, c_L + c_H <= 2 B_r1(1/2):

<!-- T:candidate -->
| rho | r1 | B(m) | 2B(1/2) - c_H | c_L* | candidate range |
|---|---|---|---|---|---|
| 0.1 | 1.5 | 2.6481 | 3.4167 | 2.6481 | fails: no-trade |
| 0.1 | 2 | 2.5407 | 3.1250 | 2.5407 | fails: no-trade |
| 0.1 | 2.5 | 2.4494 | 2.8500 | 2.4494 | fails: lowtrade |
| 0.1 | 3 | 2.3662 | 2.5833 | nan | safe |
| 0.1 | 3.5 | 2.2875 | 2.3214 | 2.7639 | safe |
| 0.1 | 3.6 | 2.2721 | 2.2694 | 2.2721 | candidate range empty |
| 0.25 | 1.5 | 2.6481 | 3.4167 | 2.6481 | fails: no-trade |
| 0.25 | 2 | 2.5407 | 3.1250 | 3.9307 | safe |
| 0.25 | 2.5 | 2.4494 | 2.8500 | 2.9456 | safe |
| 0.25 | 3 | 2.3662 | 2.5833 | 2.9844 | safe |
| 0.25 | 3.5 | 2.2875 | 2.3214 | 2.8607 | safe |
| 0.25 | 3.6 | 2.2721 | 2.2694 | 2.2721 | candidate range empty |
| 0.5 | 1.5 | 2.6481 | 3.4167 | 2.6481 | fails: lowtrade |
| 0.5 | 2 | 2.5407 | 3.1250 | 2.5784 | fails above 2.5784 |
| 0.5 | 2.5 | 2.4494 | 2.8500 | 2.4690 | fails above 2.4690 |
| 0.5 | 3 | 2.3662 | 2.5833 | 2.3726 | fails above 2.3726 |
| 0.5 | 3.5 | 2.2875 | 2.3214 | 2.2877 | fails above 2.2877 |
| 0.5 | 3.6 | 2.2721 | 2.2694 | 2.2721 | candidate range empty |
<!-- /T:candidate -->

The candidate is inside the region at rho = 1/4 for r1 from 2.0 to 3.5. It fails at rho = 1/2 and where no-trade or low-trade binds. At rho = 0.1 and r1 = 3 the verdict "safe" rests on the oracle only, because the island test cannot be run there (see section 7).

## 10. Part (iii): the collapse at r2 > r1

<!-- T:collapse -->
| r2 | c_L | regime at r2 | equilibria | E range | O_H range | E <= rho in all | E < rho in all |
|---|---|---|---|---|---|---|---|
| 3.8 | 1.0000 | I | 1 | 0.2500 to 0.2500 | 0.1250 to 0.1250 | yes | no |
| 3.8 | 2.1917 | I | 1 | 0.2500 to 0.2500 | 0.1250 to 0.1250 | yes | no |
| 3.8 | 2.4258 | II | 8 | 0.1327 to 0.1597 | 0.0907 to 0.1007 | yes | yes |
| 3.8 | 3.1623 | II | 17 | 0.0862 to 0.1430 | 0.0620 to 0.0950 | yes | yes |
| 3.8 | 3.8988 | II | 30 | 0.0412 to 0.1285 | 0.0257 to 0.0888 | yes | yes |
| 4 | 1.0000 | I | 1 | 0.2500 to 0.2500 | 0.1250 to 0.1250 | yes | no |
| 4 | 2.1617 | I | 1 | 0.2500 to 0.2500 | 0.1250 to 0.1250 | yes | no |
| 4 | 2.3936 | II | 8 | 0.1327 to 0.1597 | 0.0907 to 0.1007 | yes | yes |
| 4 | 3.1215 | II | 17 | 0.0847 to 0.1430 | 0.0614 to 0.0950 | yes | yes |
| 4 | 3.8493 | II | 31 | 0.0386 to 0.1285 | 0.0242 to 0.0888 | yes | yes |
| 5 | 1.0000 | I | 1 | 0.2500 to 0.2500 | 0.1250 to 0.1250 | yes | no |
| 5 | 2.0152 | I | 1 | 0.2500 to 0.2500 | 0.1250 to 0.1250 | yes | no |
| 5 | 2.2361 | II | 8 | 0.1327 to 0.1597 | 0.0907 to 0.1007 | yes | yes |
| 5 | 2.9201 | II | 17 | 0.0833 to 0.1430 | 0.0609 to 0.0950 | yes | yes |
| 5 | 3.6040 | II | 34 | 0.0323 to 0.1285 | 0.0212 to 0.0888 | yes | yes |
<!-- /T:collapse -->

At every r2 tested B_r2(M) < c_H, so the expensive type never enters and E <= rho. In regime I the cheap type always enters, and E = rho and O_H = rho/2 exactly.
In regime II the cheap type leaves after bad prices, so E < rho and O_H < rho/2 in every found equilibrium. Only rho = 1/4 was run.

## 11. Verification

<!-- T:verify -->
| equilibrium file | rows | checked by quadrature | accepted | rejected | max regret | max |E - E_quad| |
|---|---|---|---|---|---|---|
| eq_r3_rho0.25.csv | 4534 | 4534 | 4534 | 0 | 2.1e-17 | 9.8e-11 |
| eq_r3_rho0.1.csv | 3281 | 730 | 730 | 0 | 2.1e-17 | 9.8e-11 |
| eq_r3_rho0.5.csv | 3865 | 844 | 844 | 0 | 2.1e-17 | 9.8e-11 |
| eq_region.csv | 9366 | 2290 | 2290 | 0 | 1.4e-16 | 1.0e-10 |
| lp_polished.csv | 78 | 78 | 78 | 0 | 5.2e-18 | 4.9e-11 |
<!-- /T:verify -->

- "Checked" rows were rebuilt by the independent quadrature (no engine code) and accepted. Files with a count below the row count were checked on every fifth row plus the lowest-E and lowest-O_H row at each parameter point.
- 142 of 142 threshold members (partial, window, low-trade, island) accepted; 33 of 33 exact-LP island members accepted (max regret 6.9e-18); 102 of 102 high-rho equilibria accepted. Files: `threshold_members_verified.csv`, `lp_threshold_members_verified.csv`, `rho_check_eq_verified.csv`.
- The quadrature check is floating point, not an interval enclosure. Accepted rows are computer-assisted, not analytical.
- Members at the end of a consistent range are placed 1e-5 inside it, because the belief bound is strict. An earlier export placed some at the boundary and the verifier rejected 15 of them. They were re-placed and accepted.

## 12. Figure

`fig_regime_ii.pdf` (vector, fonts embedded, no title). (a) Entry and ownership against c_L at r1 = 3, rho = 1/4. Lines are the highest and lowest values found; dotted lines are the all-pool LP minima.
Lines break at open nodes. (b) c_L* against r1 for rho = 0.1, 0.25 and 0.5. The grey band is regime II. Open markers mean no break was found up to B(1/2).

## 13. What is not settled (open)

- Completeness. Each cutoff-scan row is a search, not a proof. Starts that did not converge are counted per point (columns n_unresolved). The largest counts are at rho = 0.1 above c_L = 2.6 (288) and at c_L >= 3.75 for rho = 1/4 (up to 100).
- Mixed equilibria beyond two atoms, and both types mixing at once, are not searched. The audit finds one local maximum per type on every sampled schedule.
- Exact-LP island thresholds (`lp_thresholds.csv`) are upper bounds on c*: the LP uses a coarse lattice of orders, and a break with other orders is not excluded. Where they bind (rho = 1/4 at r1 = 2.0, rho = 1/2 at r1 = 1.9) the member is confirmed, so c* is at most that value.
- Thresholds are located to about 1e-4 in c_L (bisection plus LP cells of width 0.01). The theory track's exact knapsack values differ by at most 1.6e-5. Windows narrower than the grid step in x' are placed at both ends and in the middle only.
- The islands LP uses full orders and the sufficient test J >= k/(1 - 1/b). Where that test fails (rho = 0.1 at k = 0.02, rho = 1/4 for r1 <= 2.3) the exact LP over the region (section 7) is the only island check, and it covers a coarse order lattice.
- The low-trade band was computed only at r1 = 3 (three rho values, three c_L) and four other r1 at rho = 1/4, c_L = 2.6. It is not a full map. The statement that the paper's (A3) right side lies below the band rests on those 13 rows.
- Part (iii) was run for rho = 1/4 only.
- The strict upper end of the region: at c_L = c* itself the numerics cannot tell if the break is attained, because the pool belief bound is strict. The region is stated as c_L < c*.
