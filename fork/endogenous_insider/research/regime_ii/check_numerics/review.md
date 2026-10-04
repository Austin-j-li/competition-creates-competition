---
title: "Referee report on the regime II numbers"
subtitle: "Numerics referee, regime II team"
date: "2026-10-03"
---

This note belongs to `fork/endogenous_insider/research/regime_ii/check_numerics/`. It checks the numbers
in `theory/note.md`, `numerics/note.md` and `adversary/note.md` with new code. Nothing here is imported
from the other three tracks. Status words follow the paper: analytical, computer-assisted, numerical
diagnostic, open. A number is "computer-assisted" when my own adaptive quadrature accepted the profile
with regret below `1e-9`; it is a floating-point check, not an interval enclosure, so nothing here is
analytical.

## 1. Method

- `model.py`. Auction payoffs, the posterior, the entry function, and the investor's payoff. The entry
  function is a step function of the posterior, so I cut the flow line at the pool edges and at the two
  threshold crossings, and integrate each piece by QUADPACK (`scipy.integrate.quad`, `epsabs=1e-14`).
  Crossings are found on a 2800-point grid and polished by Brent to `1e-14`.
- Global best response. For each type I evaluate the payoff on a 101 to 401 point grid of orders in
  `[-1,1]`, keep every local maximum, polish each one by bounded Brent, and take the largest. The kink at
  `q=0` is kept out of every bracket. A profile is accepted when the pool belief is below `tau_L`, every
  flow with posterior below `tau_L` lies in the pool, and both regrets are below `1e-9`.
- Orders may be finite mixtures. Pools may be any finite union of intervals, so islands and top pools are
  covered.
- `bathtub.py`. My own fractional knapsack over the full-order equilibrium set: cells of width `1e-3`
  (checked against `2.5e-4`), 7-point Gauss-Legendre per cell, cell edges forced at `x*` and at `1`, and a
  tie-break that prefers far cells. Every knapsack pool is then re-tested as a profile by quadrature.
- `starved.py`, `forcing_map.py`, `fixed_point_scan.py`, `refine_fp.py`, `lowtrade.py`, `corner.py`,
  `collapse.py`, `r0check.py`, `rho_check.py`, `rho_curve.py`, `random_tests.py`, `mixed_audit.py`,
  `halfline_check.py`, `table1_check.py`, `starved_thr.py`, `last_bits.py`, `formulas_check.py`,
  `corner_check.py`, `kcheck.py`, `kcheck2.py`, `window_neg.py`, `rho01.py`. Most write a CSV of the same
  name with the rows they report; `corner_check.py`, `kcheck2.py` and `rho01.py` print to the screen.
- Software: Python 3.11, scipy 1.17.1, numpy 2.4.6.

## 2. Verdict in one paragraph

Of the numbers I could reproduce, all agree except one row of one table. The weak-incumbent values at
`r0`, the regime I control, the whole of theory Table 1, all twelve bathtub thresholds of theory Table 2,
the half-line thresholds, the starved thresholds at five trading costs, the starved members, the `v=0`
corner, the forcing map, the break point `2B(1/2)-c_H`, the low-trade band, the collapse at `r2`, the
cheap-type share bounds `rho_E*` and `rho_O*`, and the adversary's `rho=0.6` counterexample all come out
the same in my code. The one disagreement is the small-`rho` end of the adversary's `rho` curve: at
`c_L=4.20` the reversal fails for **every** positive `rho`, not for `rho>0.0007`, and the reversal region
in `(c_L,rho)` has its corner at `c_L=4.1498`, not at `B_{r_1}(1/2)=4.2917`. I also flag one wording point
in the numerics note: its "lowest found" entry just below `c*` is the lowest in the cutoff family, while
island pools reach lower values and are accepted at `k=0.02`.

## 3. Number by number

Benchmark unless a row says otherwise: `h=10, ell=1, p=1/2, b=2, c_H=6, r1=3, rho=1/4, k=1/50`.
My own values of the primitives: `B(m)=2.3661785`, `B(1/2)=4.2916667`, `B(M)=6.2171548`, `Delta_T=2/3`,
`tau_H=0.705`, `x*=0.8712224`, `v_H=0.7424449`, `(1-1/b) rho m Delta_T=0.0224118`, `2B(1/2)-c_H=2.5833333`.
All agree with the three notes.

### 3.1 Part (i) at the weak incumbent (`r0check.csv`)

| claim | source | my value | verdict |
|---|---|---|---|
| `Delta_T(r0)=1/60`, `B_{r0}(1/2)=1153/240=4.804167` | numerics, theory | `0.0166667`, `4.8041667` | agrees |
| zero orders, `E=rho`, `O_H=rho/2` exactly, for `rho` in {0.1,0.25,0.5} and `c_L` up to `B_{r0}(1/2)` | numerics (i), theory R.1 | `E=rho` and `O_H=rho/2` to `1e-12` at all 15 cells; the best nonzero deviation of either type is strictly negative (at most `-1.6e-4`), and the per-unit bound `Delta_T(r0)-k=-0.00333` is negative, so zero is the unique best response | agrees |

Part (i) is confirmed. The bound is structural: with `Delta_T(r0)<k` no order of either sign can pay,
whatever the schedule, so this does not depend on the grid.

### 3.2 The full-order equilibrium set at `r1` (`table1_check.csv`, `thr_bathtub.csv`)

Theory Table 1, `rho=0.25`, all ten rows: I reproduce `pibar`, `K(c_L)`, `E_0`, `inf E`, `e_{H,0}`,
`inf e_H` to the four printed decimals at every row (largest difference `1e-4`, which is rounding). For
example `c_L=3.00`: mine `pibar=0.5913`, `K=0.00648`, `E_0=0.4225`, `inf E=0.3403`, `e_{H,0}=0.5934`,
`inf e_H=0.4824`. Theory's `c_L=4.20` row `inf E=0.0158` comes out `0.0159`.

I also tested that the knapsack pools are equilibria where the theory says they are: at `k=0.9K(c_L)`,
all ten worst pools are accepted with regret `0` for both types. That is the content of Proposition R.6
plus R.7 at a point inside (A3'), and it holds in my code.

Theory Table 2, the (A4') thresholds, by my own bisection on `c_L` (three cell widths, same answer):

| `rho` | entry: theory | mine | ownership: theory | mine |
|---|---|---|---|---|
| 0.10 | 3.9201 | 3.92009 | 4.0036 | 4.00355 |
| 0.20 | 3.6330 | 3.63296 | 3.8350 | 3.83505 |
| 0.25 | 3.4607 | 3.46068 | 3.7408 | 3.74079 |
| 0.30 | 3.2638 | 3.26379 | 3.6388 | 3.63877 |
| 0.35 | 3.0366 | 3.03660 | 3.5280 | 3.52798 |
| 0.50 | 2.3726 | 2.37257 | 3.1300 | 3.13004 |

All twelve agree to `5e-5`. The closed-form sufficient condition (A4'') comes out `3.3357416`, against
theory's `3.3357`: agrees. The theory track's statement that the worst pool at `c_L=3` takes `13%` of the
top plateau also agrees: my knapsack takes the tail above `5.0695`, whose probability is `13.13%` of the
plateau `Pr(X>=1)=0.34197`.

### 3.3 The worst pools at the paper's trading cost (`sweep_k02.csv`)

Nine values of `c_L`, four members each (minimal pool, the half-line at the pool cap, and the two worst
knapsack pools), every one re-checked by quadrature:

| `c_L` | minimal pool `E` | half-line `E` | worst pool `E` | worst `O_H` | accepted at `k=0.02` |
|---|---|---|---|---|---|
| 2.40 | 0.43639 | 0.42453 | 0.42453 | 0.29738 | yes |
| 2.60 | 0.43144 | 0.40189 | 0.39813 | 0.28263 | yes |
| 2.80 | 0.42683 | 0.38736 | 0.37115 | 0.26395 | yes |
| 2.95 | 0.42354 | 0.37793 | 0.34846 | 0.24799 | yes |
| 2.98 | 0.42290 | 0.37613 | 0.34363 | 0.24458 | yes |
| 3.00 | 0.42248 | 0.37494 | 0.34036 | 0.24228 | yes |
| 3.20 | 0.41834 | 0.36251 | 0.30494 | 0.21716 | yes |
| 3.50 | 0.41243 | 0.29136 | 0.24089 | 0.17140 | yes |
| 4.00 | 0.40308 | — | 0.09194 | 0.06402 | no (low type's regret `1.2e-3`) |

This confirms three statements at once. The numerics track's LP minimum `0.3405` at `c_L=3.0` matches my
`0.34036`. The theory track's island claim at `c_L=3.5`, `E=0.2408`, matches my `0.24089`, and its
threshold `3.4607` gives `inf E=0.24999` against `rho=0.25`. And the adversary's re-check `inf E=0.250001`
at `3.4607` is the same number.

One correction of my own to the ledgers: the worst pools stop being equilibria somewhere between
`c_L=3.5` and `c_L=4.0` at `k=0.02`, since at `4.00` the low type wants a short of `0.9832` rather than `1`.
The island branch of the failure therefore covers `c_L` from about `3.46` to somewhere below `4.0`, and
above that the starved and half-line branches carry the failure. No note states otherwise, but none says
where the island branch ends.

### 3.4 Clarification on the numerics note's "lowest found" (`last_bits.csv`)

At `c_L=2.975` I get: minimal pool `E=0.42301`, `O_H=0.29686`; half-line at the cap `E=0.37643`,
`O_H=0.27415`; worst pools `E=0.34444`, `O_H=0.24414`, all four accepted at `k=0.02` with regret `0`.
The numerics note's "lowest found values just below `c*`: `E=0.3764`, `O_H=0.2741`" is exactly the
half-line member. The infimum over the equilibria I can verify is `0.34444` and `0.24414`, which is the
knapsack value. The numerics note's own all-pool LP reports the lower number at `c_L=3.0`, so this is a
wording point, not a contradiction. I marked it in that note as a referee fix.

### 3.5 The starved family (`starved_members.csv`, `starved_thr.csv`, `refine_fp.csv`, `corner.py`)

The low type's first-order condition and the pool-belief test give the family. My threshold, found by
solving `B(pool belief at the limit v -> v_H) = c_L`:

| `k` | theory | mine | difference |
|---|---|---|---|
| 0.0224 | 2.8326 | 2.832591 | `-8.8e-6` |
| 0.0200 | 2.9844 | 2.984373 | `-2.7e-5` |
| 0.0150 | 3.3954 | 3.395375 | `-2.5e-5` |
| 0.0100 | 3.7831 | 3.783083 | `-1.7e-5` |
| 0.0075 | 3.9367 | 3.936652 | `-4.8e-5` |

All five agree, and the limiting member at `k=0.02` has `x'=0.43885` and pool belief `0.343125`, against
the theory track's `0.4388` and `0.34312` and the numerics track's `2.984373`.

Members, each checked by global best response of both types (401 order points plus polish):

| source claim | my value | verdict |
|---|---|---|
| numerics: `c_L=3.000`, `q_L=-0.7344`, cutoff `0.461`, `E=0.1117`, `O_H=0.0773` | `v=0.7344`, `x'=0.4606`, `E=0.11166`, `O_H=0.07727`, both regrets below `2e-18`, high type's best response `1.0000` | agrees |
| adversary: numerics' `c_L=3.5` member `x'=0.5`, `q_L=-0.7196`, `E=0.11029`, belief `0.3484` | my family at `c_L=3.5` runs `E` from `0.0957` (`v=0.55`) to `0.1124` (`v -> v_H`), all accepted; the `x'=0.5` member sits inside it | agrees |
| theory: the family at `c_L=3.0` is the narrow window `v` in `[0.7344,0.7424]`, `x'` in `[0.4388,0.4607]`, `E` about `0.112` | mine: `v=0.7344` to `0.7423`, `x'=0.4606` down to `0.4391`, `E=0.11166` to `0.11240` | agrees |
| theory and numerics: the `v=0` corner at `c_L>=3.95`, cutoff `1.906`, `E=0.0638` | cutoff `1.9061`, pool belief `0.45801`, `E=0.06383`, `O_H=0.03973`, accepted for `c_L=3.95, 4.0, 4.2` and **not** at `c_L=3.90` (belief `0.45801` above `tau_L=0.453`) | agrees, including the `3.95` edge |
| adversary: the high type's full purchase holds along the family | my global best response gives `q_H=1` at all 21 members I checked (`c_L` in {3.0,3.5,4.0}), with regret `0` | agrees (my check is a dense grid plus polish, not an enclosure, so this stays computer-assisted) |

### 3.6 Is the window below `c*` really clean? (`fixed_point_scan_*.csv`, `refine_fp.csv`, `mixed_audit.csv`, `random_tests.csv`)

I ran my own search for partial-order equilibria with a half-line pool, independent of both searches in the
other folders: for each cutoff on a grid of step `0.01` from `-1` to `1.5` and each `q_H` in {1, 0.8, 0.6},
I follow the low type's global best response `s*(v)` along `v` on a grid of step `0.01` and bracket every
sign change of `s*(v)-v`, then refine by Brent and test the high type.

- `q_H=1`, `c_L` in {2.6, 2.7, 2.8, 2.9, 2.95, 2.98}: **no** fixed point with `v<1`. At `c_L=3.0` the
  scan finds the starved window and nothing else. This is an independent confirmation of the numerics
  track's "only `(1,-1)` up to `2.975`" and of the theory track's threshold `2.9844`.
- `q_H` in {0.8, 0.6}, `c_L` in {2.8, 2.98}: 118 brackets, 75 distinct refined fixed points of the low type. Every
  one fails the high type: its best response is `1.0000` and its regret is `0.0045` to `0.0259`. So no pure
  partial-buy equilibrium there.
- Mixtures: 960 random consistent schedules (one or two atoms per type, random pools including islands and
  half-lines pushed to the pool cap) at `c_L` in {2.6, 2.8, 2.95, 2.98}. Every schedule gives each type
  exactly one local maximum, and never two orders within `1e-9` of the top. So no two-atom mixed best
  response appears on my sample either. This agrees with the adversary's 745 lattice schedules and the
  numerics track's 1500-draw audit.

Status: numerical diagnostic. The window `c_L` in `(2.59, 2.9844]` at `k=0.02` stays open as a theorem, as
all three notes say. My search adds a third independent class of starting points and finds nothing.

### 3.7 Forcing and the break point (`forcing_map.csv`, `break_check.csv`, `random_tests.csv`)

The forcing level over pure schedules with half-line pools (the smallest marginal payoff `d/ds[s F_theta(s)]`
over both types and `s` in `(0,1]`, minimised over non-full consistent schedules):

| `c_L` | theory `k_pure` | mine |
|---|---|---|
| 2.37 | 0.0596 | 0.05958 |
| 2.45 | 0.0572 | 0.05599 |
| 2.55 | 0.0538 | 0.05335 |
| 2.65 | 0.0192 | 0.01889 |
| 2.75 | 0.0175 | 0.01694 |
| 2.95 | 0.0147 | 0.01441 |

The two tracks differ by `0.0006` at most; the shape is the same, and so is the drop between `2.55` and
`2.65`. My order grid is `q_H` in {1,0.8,0.6,0.4} and `q_L` in steps of `0.05`, so small differences in the
lattice explain the gap. The break itself (`c_L+c_H<=2B(1/2)`, Lemma R.11) is confirmed sharply: scanning
`(1,-v)` with `v` in `[0.65,v_H)` and three cutoffs per schedule, no schedule pools at `c_L=2.55`, `2.58`
or `2.5833`, and pooled schedules appear at `2.585` (six of them) with forcing level `0.02047`, then
`0.02012` at `2.59`, `0.01968` at `2.60`, `0.01908` at `2.62`. Theory reports `0.0205`, `0.0199`, `0.0193`
at `2.59`, `2.60`, `2.62`. Same picture, same crossing of `k=0.02` between `2.585` and `2.60`.

The forcing bound `K(c_L)` is confirmed as a formula (`0.01068`, `0.00975`, `0.00858`, `0.00648`, `0.00529`
at `c_L=2.37, 2.4, 2.5, 3.0, 3.5`; `K=0.008` at `c_L=2.5867`; the floor limit `0.011206` is exactly half of
(A3)'s `0.022412`). It is also confirmed to be conservative: on 2800 random mixed-order draws with random
consistent pools, the residual integrals `F_L(s)` and `F_H(s)` never fall below the bounds used in the proof
of R.6; the tightest ratios are `F_L/bound = 1.83` and `F_H/bound = 1.31` at `c_L=3.5`, and `5.88` and `3.15`
at `c_L=2.4`. The pool caps of Lemma R.5 are never violated either: the largest ratio of a left side to its
bound is `1 - 4e-10` (the half-line pool pushed to the cap attains it, as the theory note says).

### 3.8 The cheap-type share (`rho_check.csv`, `rho_curve.py`)

| adversary claim | my value | verdict |
|---|---|---|
| `pi_0=0.34197`, `a=0.36368` | `0.341971`, `0.363680` | agrees |
| `rho_E*=0.51538`, `rho_O*=0.74278` at `r1=3` | `0.515381`, `0.742785` | agrees |
| `rho_E*` `0.5262` at `r1=2.5`, `0.5026` at `3.5`; `rho_O*` `0.7506` and `0.7331` | `0.526218`, `0.502628`; `0.750606`, `0.733115` | agrees |
| verified example: `rho=0.6`, `c_L=2.4`, `k=0.02`: `K(2.4)=0.0234>=k`, minimal pool accepted, `E=0.5382`, `e_H=0.701`, `e_L=0.375`, `O_H=0.350` | `K=0.02341`, accepted with regret `0`, `E=0.53819`, `e_H=0.70097`, `e_L=0.37540`, `O_H=0.35048`; all consistent pools give at most `0.50973` | agrees |
| `rho=0.75` and `0.8` at `c_L=2.4` also break ownership (`0.372<0.375`, `0.379<0.4`) | `0.37171` and `0.37878` | agrees |
| numerics #5: `E=0.5154` at `rho=0.5154` just above the floor; `E=0.5108` at `rho=0.5` | `0.51538` and `0.51085` at `c_L=B(m)+1e-4` | agrees |
| numerics #5: at `rho=0.5`, `c_L=2.4162` the reversal holds in some equilibria and fails in others | minimal pool `0.50827>0.5`, worst pool `0.47966<0.5` | agrees |
| numerics #5: at `rho=0.5`, `c_L=2.6662` it fails in every equilibrium | minimal pool `0.49608<0.5` | agrees |
| adversary `rho` curve, entry, all pools: `0.5145` at `2.3662`, `0.4488` at `2.5`, `0.3950` at `2.8`, `0.3574` at `3.0`, `0.2502` at `3.46`, `0.1654` at `3.74`, `0.0676` at `4.0` | `0.5145`, `0.4488`, `0.3950`, `0.3574`, `0.2502`, `0.1654`, `0.0676` | agrees |
| same, minimal pool: `0.5151`, `0.5056`, `0.4866`, `0.4755`, `0.4535`, `0.4418`, `0.4317` | identical to four decimals | agrees |
| adversary: `c_L<=2.7716` at `rho=0.4`; `c_L<=2.4` holds up to `rho=0.4807` | roots `0.39999` at `2.7716` and `0.48068` at `2.4` | agrees |

### 3.9 The one disagreement: the small-`rho` end of the `rho` curve

The adversary's Table 1, last row, reads `c_L=4.20`, entry all pools `0.0007`, ownership all pools
`0.0010`, and the text says the reversal region is a triangle with its corner at `(B_{r_1}(1/2),0)`.

My numbers say both entries should be zero and the corner is elsewhere.

- At `c_L=4.20` my knapsack gives `inf E = 0.0635 rho` and `inf e_H = 0.0841 rho` for every `rho` I tried
  (`1e-7` to `0.02`), so `inf E < rho` for every positive `rho`. Cell widths `1e-3` and `2.5e-4` give the
  same values to six digits.
- A decisive single check, not a root find: at `(c_L,rho)=(4.20,0.0007)` the worst pool has belief
  `0.488901`, below `tau_L=0.489`, so it is consistent, and quadrature gives `E=4.4942e-5`, far below
  `rho=0.0007`. The same pool is an accepted equilibrium (regret `0` for both types) at `k=0.9K(4.20)`,
  that is, inside (A3'). So an equilibrium with `E<rho` exists at that point.
- The limit of the entry threshold as `rho` falls is `c_L=4.14978` at `rho=1e-5`, `4.14959` at `1e-4`,
  `4.14773` at `1e-3`, `4.12891` at `1e-2`, `4.04099` at `0.05`, `3.92009` at `0.1`. So the corner of the
  region is at about `c_L=4.1498`, not at `B_{r_1}(1/2)=4.2917`.

The reason is structural, not numerical. As `rho` falls, the knapsack's value per unit of belief cost
rises faster above `x*` than below it, so the worst pool removes expensive entry as well as cheap entry. The
removed share does not vanish with `rho`, and near `B_{r_1}(1/2)` the budget `B_0` is large enough to
remove almost all of it. The ratio `inf E / rho` therefore stays near `0.06` at `c_L=4.20` instead of
rising to `1`. I marked both places in `adversary/note.md` with a referee fix. Theory Table 2 is not
affected: its lowest `rho` is `0.10`, where my threshold agrees to `5e-5`.

### 3.10 The half-line family and the end of the investor test (`halfline_check.csv`)

`x_E=1.62652`, `x_O=2.38629`, `x_k=2.61400`, thresholds `B(mubar(x_E))=3.64984` and
`B(mubar(x_O))=3.89453`: these are the theory track's `1.6265`, `2.3863`, `2.6140`, `3.6498`, `3.8945` and
the adversary's re-check. Agrees. Members just past each threshold are accepted by quadrature: at
`c_L=3.66` and `x'=1.6285`, `E=0.24975<rho`; at `c_L=3.90` and `x'=2.3883`, `O_H=0.12488<rho/2`. The
investor test does end at `x_k`: the member at `x'=2.604` is accepted at `c_L=4.2`, the member at `x'=2.664`
is not (the low type's best short is `0.9832`).

### 3.11 The low-trade family and the collapse (`lowtrade.csv`, `collapse.csv`)

The low-trade family exists as the numerics track describes it. For symmetric orders `(q,-q)` the trading
cost that makes `q` a fixed point of the low type's problem falls from `0.08323` at `q=0.05` to `0.06207`
at `q=0.87`, so at `r1=3`, `rho=0.25` the band is `k` in about `[0.062, 0.083]`, exactly the note's
`[0.062,0.083]`, and the top of the band is the no-trade bound `rho Delta_T/2 = 0.08333`. Four members
checked at their own `k` are accepted with regret below `3e-17` and have `E=rho` and `O_H=rho/2` to twelve
digits, as claimed. The paper's `k=0.02` is far below the band at `r1=3`.

One detail to keep in mind when reading the band: for `c_L` high enough the symmetric schedule starts to
pool, and then the fixed-point cost drops sharply (at `c_L=2.8` it is `0.0684` at `q=0.7` but `0.0282` at
`q=0.8`). So "the band" is the pool-free part of the family; the pooled part reaches down toward `k=0.026`
at `c_L=2.8`. That is still above `k=0.02`, so it does not change any conclusion, and the numerics note's
own `k_LT` column is the pool-free edge.

Collapse at `r2>r1` (full orders, minimal pool, `rho=0.25`, `k=0.02`): at `r2=3.6, 3.8, 4.0, 5.0` with
`B_{r2}(M)<c_H`, a regime I cost (`c_L=2.0`) gives `E=rho` and `O_H=rho/2` exactly, and regime II costs
(`c_L=2.4` and `3.0`) give `E` between `0.1412` and `0.1612` and `O_H` between `0.0944` and `0.1011`, all
strictly below `rho` and `rho/2`. This matches both notes: equality in regime I, strict inequality in
regime II.

### 3.12 (A3') feasibility

`K(c_L)` at `rho=0.25` never reaches `0.02`, and `Delta_T(1.2)=0.0166667`, so (A3') is empty at the paper's
`(r0,k,rho)=(1.2,0.02,0.25)`, as the adversary says. `K` is linear in `rho`: at `rho=0.6` and `c_L=2.4`,
`K=0.02341>k`. Both facts are confirmed by direct evaluation.

### 3.13 Starved equilibria with a pool cutoff below zero (`kcheck.csv`, `window_neg.csv`)

The theory referee reported starved equilibria at `(c_L,k)=(2.6,0.03)`, `(2.9,0.03)` and `(2.9,0.035)`,
which sit below the numerics track's `k_U` of `0.050` to `0.054`. I confirm all three with my own code,
once the pool cutoff is allowed to be negative. The theory note's Proposition R.10 assumes `x'>=0`, and
with that restriction my search finds nothing at `(2.6,0.03)` or `(2.9,0.035)`; with `x'` free I find
accepted members (both regrets below `4e-18`, high type's best response `1`):

| `c_L` | `k` | `v` | `x'` | `E` | theory referee's `E` |
|---|---|---|---|---|---|
| 2.6 | 0.030 | 0.7309 | `-0.7227` | 0.16083 | 0.161 |
| 2.9 | 0.030 | 0.6270 | `-0.3330` | 0.14680 | 0.146 |
| 2.9 | 0.035 | 0.4193 | `-0.1691` | 0.14531 | 0.155 (a different member) |

So the `k_S` and `k_U` columns of the numerics note's `kscan` table are too high at `c_L=2.6` and `2.9`:
they rest on a starved solver that only looks at nonnegative cutoffs. Both points are outside (A3) at
`rho=0.25` (`k=0.03>0.0224`), so Proposition 2' and the (A3) discussion are untouched, and so is the
reversal at `k=0.02`.

The same test at the paper's `k=0.02` is reassuring rather than damaging. Scanning `v` on 121 points and
solving the low type's condition for `x'` in `(-2,0)` as well as `(0,8)`, there is **no** consistent
starved candidate at `c_L=2.5, 2.6, 2.7, 2.8, 2.9, 2.95, 2.98`, and the first candidates appear at
`c_L=3.0` (two of them, both accepted, lowest `E=0.11185`). Pools that end below zero therefore do not
break the open window, which is what the adversary's lattice also found.

## 4. What I could not check

1. Everything here is floating-point quadrature. No row is an interval enclosure, so no row upgrades a
   status to analytical. The three notes say the same about their own numbers.
2. Order mixtures with three or more atoms, and both types mixing at once, are outside my audit as well.
3. My partial-order search covers `q_H` in {1, 0.8, 0.6} with half-line pools (cutoffs of either sign), at
   four values of `c_L` in the open window. Partial buys with island pools in that window are not covered
   by my code.
4. The region map over `(r1,rho)` in the numerics note, its two exact-LP cells, and the `rho=0.1` cells
   with unconverged starts are not re-run here. I checked `rho=0.1` only at `r1=3`, where I confirm that no
   starved member with `x'>=0` exists at `c_L=3.0, 3.5, 4.0` (the low type's marginal payoff at `s=v` is
   negative at every `v` on my grid), which is consistent with the note's "no break found at `rho=0.1`".
5. The adversary's certificate method for the high type (envelope plus derivative bound) is not
   re-implemented. I checked the same conclusion with a dense global best response instead.

## 5. Files

`model.py`, `bathtub.py`, `starved.py` are the engine. Each script writes the CSV of the same name:
`thr_bathtub.csv`, `table1_check.csv`, `sweep_k02.csv`, `starved_members.csv`, `starved_thr.csv`,
`forcing_map.csv`, `break_check.csv`, `fixed_point_scan_*.csv`, `refine_fp.csv`, `mixed_audit.csv`,
`random_tests.csv`, `rho_check.csv`, `rho_curve.csv`, `halfline_check.csv`, `lowtrade.csv`,
`collapse.csv`, `r0check.csv`, `last_bits.csv`, `kcheck.csv`, `window_neg.csv`. Reruns: `python3 <script>.py`; the two scans take about
four minutes each on four cores, everything else is seconds.
