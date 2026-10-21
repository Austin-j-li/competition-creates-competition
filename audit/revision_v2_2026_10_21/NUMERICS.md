# Numerical revision: 21 October 2026

**Result: PASS.** All requested exercises and both numerical release gates passed.
The validated numerical commit is `9faf2d70c164f4cc679ccceab7dd27061c0e9fe8` on `revision/alex-2026-10-21`.
The reference commit is `1eb6d2cfd70fdfca98bbf4557d666bd04417e1df`.
All project paths below refer to `/home/uctpiaj/work/Projects/ccc-revision-numerics`.
The source changes, outputs, and commits remain in that worktree. No push occurred.

The shared handoff files are `reconciliation.csv` and this report under the original project's `audit/revision_v2_2026_10_21/` directory.
The legacy Markdown sources support the numerical renderer. The separate manuscript revision clone receives no edit from this work.

**Reconciliation.** The baseline inventory records 50 committed numerical and presentation files, their Git objects, and their SHA-256 values.
`baseline_outputs.csv`, `baseline.json`, and the two baseline quantity files preserve that reference.
The figure reference hashes match the original committed render manifest.
`baseline_figures.json` also preserves their rendered hashes at 150 dpi.

The final reconciliation has 3238 rows and compares 62 output files.
It includes every original registry key, every new key, table source cells, certificate cells, reserve summaries, and artifact hashes.
It retains unchanged quantities. It marks each new requested quantity with the note `new`.
`output_diff.json` also records complete-file hashes, CSV row counts, and exact added or removed row counts.

- 429 existing scalar records differ. This count includes repeated declarations and source cells.
- 17 of the original 128 registered quantities differ.
- Of these, six displayed numbers change: three low-cost inputs and three low-cost margins.
- Seven registered quantities retire with C.6b.
- Four registered values differ only at floating-point roundoff; their displayed values remain unchanged.
- Eight registered quantities are new. The final registry contains 129 entries.

**Economic changes.** Both surplus levels in Table 2, Panel C rise by 0.25.
Observed-price surplus becomes 2.632300868169776; hidden-price surplus becomes 2.552083333333334.
Their difference remains unchanged. Entry, ownership, and target proceeds at the declared benchmark nodes remain unchanged.

The atomless low-cost law is uniform on [0, 0.2]. Its width stays 0.2 and its mean becomes 0.1.
This is the smallest nonnegative translation that preserves the original atomless width.
The high-cost law stays uniform on [5.9, 6.1]. The low support remains below every declared C.1 entry floor.
Its surplus levels rise by 0.225, because the mean low cost falls by 0.9.

**C.2 domain and thresholds.** Proposition A.4 keeps the domain 1 < r < 10.
The old low-cost floor condition already holds throughout that interval.
At its upper limit, the floor margin rises from 0.368760035781476 to 1.368760035781476.
The prior gross profit stays below 6; its upper limit is 4.875.
Figure 2 retains axes [1, 3.8] and mesh 1.005 through 3.800 in steps of 0.005.
The minimum grid floor margin rises from 1.2417226944956457 to 2.2417226944956457.
`domain.json` records both calculations.

| C.2 threshold | Old value | New value |
|---|---:|---:|
| `pooling_unique_sufficient` | 1.220997512422418 | 1.220997512422418 |
| `pooling_existence` | 1.7478775382679625 | 1.7478775382679625 |
| `full_orders_unique_sufficient` | 2.8374169640989404 | 2.8374169640989404 |
| `high_cost_ceiling` | 3.592658518794662 | 3.592658518794662 |

The three interval certificates also retain their brackets and accepted predicates.
C.2 contains 592 nodes: 580 initial nodes and 12 refinement nodes.
Its 6,000 attempts retain 40 open records: 19 mixed-search records and 21 pure-search records.
These counts match the reference. No open record receives a replacement value.

**Reserve changes.** The binary floor event moves from approximately 6.281718171541 to 10.
The uniform-class event moves to 10.05, the upper edge of the high-value band.
At the binary event, preparation is 0.25, sale probability is 0.125, and revenue is 1.25.
At the class event, preparation is 0.25, but sale probability and revenue are zero.
The class endpoint has no probability mass. Its floor event is therefore not at h = 10.
The high-cost event values remain unchanged.

Above the value support, low-cost preparation still occurs under the existing tie rule.
Sale probability and revenue are zero there. The event grid retains all three upper and lower offsets.
The highest revenue found is 1.25 at reserve 10 for binary values.
For uniform classes, it is 1.24375 at reserve 9.95.
These results hold at both declared strengths. They are search results, not a proof of global optimality.

C.6 contains 1,120 nodes, including all 96 planned refinement nodes.
It retains 45 open search flags and finds an accepted continuation at every node.
The ledger contains 2,646 final candidate evaluations, 1,073 rejections, 32 unresolved candidates, and 414 duplicate merges.
The event exercise contains 241 nodes, 506 candidate evaluations, and seven open search flags.
It also finds an accepted continuation at every node. Its prior positive-cost grid contained 257 nodes.
Coincident support and floor events explain the smaller event count.

The first C.6c attempt failed at the flat price map of the class endpoint.
The corrected validator uses the prior on that constant price's complete preimage when the two state order laws coincide.
The first C.6 attempt stopped at the weak class node with reserve 0.9701.
Bounded first-order refinement now resolves the candidate identity, followed by full validation.
Three nodes use this refinement. All 42 prior candidates remain in the ledger.
The failed attempts and their raw checkpoints remain in the audit record.

**New exercise C.9.** The producer starts only after the first release gates passed.
Its manifest is `numerics/manifests/c9_revision.json`.
Its source definitions are equations S12 and S14 in `Q3_stake.md` and the specified Q2 noise memos.

| Registry name | Full stored value | Meaning |
|---|---:|---|
| `Pi_acc` | 0.1407312272830394 | Gross trade profit with price access; excludes k. |
| `Pi_hid` | 0.06910405796503649 | Gross trade profit with hidden prices; excludes k. |
| `Delta_R_T` | 0.25780871176130704 | Target proceeds gain from price access at r = 3. |
| `break_even_trade_scale` | 1.831922571404858 | Proceeds gain divided by gross profit with price access. |
| `Omega_U` | 0.011433647948640045 | Sufficient stake bound for unique full orders at r = 3. |
| `Omega_0` | 0.04309764309764388 | Sufficient stake bound for unique no trade at r = 1.2. |
| `sech_entry_strong` | 0.3766056093539899 | Entry under full orders and hyperbolic secant noise. |
| `student_t3_entry_strong` | 0.3749945168160299 | Entry under full orders and Student noise with three degrees of freedom. |

All supplied memo targets agree at the requested precision.
The stake bounds are sufficient, not exact equilibrium thresholds. Strict comparisons use the unrounded formulas.
Both additional noise laws have score bound 0.5. The Student scale is 2.3094010767585034.
The Student entry interval is [2.484315631878584, 6.842930818394031].
The hyperbolic secant entry set starts at 2.8174295609811084 and extends to infinity.
These are fixed-profile entry calculations. They do not certify additional equilibria.

Independent scalar formulas agree within 7.8e-16. The proceeds identity error is 2.3e-16 or less.
The largest independent noise formula error is 2.0e-15 or less.
The largest quadrature error estimate is 9.15e-12, below the unchanged 1e-11 target.
Both Laplace price regimes also pass the existing continuation validator.
An initial C.9 write failed because a NumPy Boolean needed conversion for JSON.
That attempt wrote no run manifest. The corrected producer passed in 2.13 seconds.

**Tables and figures.** The project renderer regenerates every numerical table and all four figures.
These six table files change:

- `tables/table2_equilibrium_controls.tex`
- `tables/table_extensions_margins.tex`
- `tables/table_matched_price.tex`
- `tables/table_reserve_details.tex`
- `tables/table_reserve_exploratory.tex`
- `tables/table_signal_grid.tex`

All four figure PDFs remain byte-identical to the reference:

- `figures/two_returns.pdf`
- `figures/equilibrium_correspondence.pdf`
- `figures/posterior_tail_entry.pdf`
- `figures/bargaining_weight.pdf`

The render also rebuilds both legacy manuscript PDFs.
Visual review covers every changed numerical table, the four figures, and the new C.9 section.
The inspected pages show complete rows, readable labels, and no overlap or clipping.
`visual_review.json` records this limited scope and the final PDF hashes.
This is not a review of every manuscript page.

**Runtimes.** These are observed elapsed times for the final numerical runs.
Each worker uses one native library thread. The largest concurrent allocation was 31 workers, below the limit of 32.

| Producer | Workers | Seconds |
|---|---:|---:|
| C.1 baseline | 1 | 79.36 |
| C.2 correspondence | 24 | 677.51 |
| C.3 signals | 1 | 69.80 |
| C.4 moderate values | 1 | 6.58 |
| C.5 noise | 1 | 1.02 |
| C.6 reserves | 24 | 120.13 |
| C.6c exact events | 6 | 79.78 |
| C.7 payment institution | 1 | 0.65 |
| C.9 new quantities | 1 | 2.13 |
| C.8 final registry | 1 | 0.21 |

The final presentation sequence, reconciliation, and two gates took 24.36 seconds.
The first failed C.6 sweep took 119.99 seconds. The first failed C.6c attempt took 78.42 seconds.
The successful intermediate C.6c run took 77.65 seconds; the final solver change required its complete rerun.
C.1 first took 77.68 seconds before the final support declaration entered its manifest.
C.4 first took 6.54 seconds before the construction also fixed zero low cost.
The command logs preserve these earlier runs and the short exercise timings.

**Release gate.** The exact final gate commands were:

```bash
cd /home/uctpiaj/work/Projects/ccc-revision-numerics
/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python numerics/verify.py --final
/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python numerics/release_checks.py
```

The orchestration command was:

```bash
/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python audit/revision_v2_2026_10_21/run_presentation.py accepted
```

It calls the project's registry, substitution, renderer, LaTeX build, and release commands.
All commands exit with code zero. The numerical gate reports `VERIFY PASSED`.
Substitution fills 103 placeholders with zero unresolved and zero unknown keys.
The release checks pass for registry, controls, certificates, endpoints, candidates, and finite accepted results.
`logs/accepted_verify.log` and `logs/accepted_release_checks.log` contain the complete gate output.
`presentation_accepted_runs.json` records each command, directory, duration, log, and exit code.

No test or assertion script was written. No test suite ran.
The historical peer-release wrapper includes a test suite and an old positive-cost seed.
The direct numerical release commands define this revision's acceptance.
No tolerance was loosened. Open search results remain open.

**Contract changes.** The complete record follows. It also exists in `CONTRACT.md`.

New symbols: `Pi_acc`, `Pi_hid`, `Delta R_T`, `Omega_U`, and `Omega_0` follow the requested memo definitions.
For the additional noise law, `nu` denotes degrees of freedom and `s` denotes its scale.

The reference is commit `1eb6d2cfd70fdfca98bbf4557d666bd04417e1df`.
The author sets the low preparation cost to zero.
No numerical tolerance changes.
No unresolved result receives a replacement value.

1. The benchmark, moderate, and complementary-signal vectors now declare zero low cost.
   The three input rows in the quantity manifest use the same declaration.
   The legacy CSV column `c_L` remains for compatibility.
2. The atomless low-cost component is uniform on `[0, 0.2]`.
   Its width remains `2 epsilon_C = 0.2`; its mean is `0.1`.
   The high-cost component remains uniform on `[5.9, 6.1]`.
   All C.1 gross-profit floors exceed the low component's upper endpoint.
   The cost CDF, paid-cost integral, breakpoints, independent integral, and margins use the same support.
3. C.4's nonemptiness sequence also fixes zero low cost.
   The former positive-low-cost requirement disappears.
   The other choices, grid, and strict inequalities remain.
4. Exercise C.6b is retired, with its output, manifest, and seven quantity keys.
   The prior commit preserves them.
   The release stages and renderer no longer consume them.
   Minimal retirement notices replace their legacy manuscript source sections so substitution remains strict.
   The live manuscript clone receives no edit here.
5. The binary floor event is `p_L = h = 10`.
   For uniform value classes, zero gross profit first occurs at `h + epsilon_V = 10.05`.
   The class endpoint has zero mass; its sale probability and revenue are zero.
   The binary endpoint remains admissible under the existing bid tie rule.
   Exact floor events take precedence over coincident support labels.
6. The event grid retains all three offsets on each side of the floor endpoint.
   Upper offsets extend beyond the value support for this check alone.
   Above the support, gross profit and low cost both equal zero.
   Preparation remains `rho` under the existing tie rule; sale and revenue are zero.
   No negative-floor classification applies there.
7. The reserve solver no longer excludes full orders solely because challenger gross profit equals zero.
   Zero spread or impossible preparation still permits the constant-price shortcut.
   At a zero-spread constant-price node with identical state order laws, Bayes' rule gives the prior on the full preimage.
   A constant price map has no inverse.
8. The class-payoff integrals use factored polynomial differences near the support endpoint.
   This avoids cancellation of nearly equal squares without a tolerance change.
9. C.2 retains its domain, mesh, refinements, certificates, and four thresholds.
   `domain.json` records the old and new margins and threshold outputs.
10. Verification uses the producer commands and the two release gates directly.
    No test suite runs, and no test or assertion script is written.
    The historical release wrapper and independent seed do not define this revision's acceptance.
11. The first C.6 sweep stopped at the weak class node `p=0.9701`.
    Interior pure starts differed by about `4e-8` in orders and failed the stricter atom identity comparison.
    The bounded refinement now solves both held-schedule first-order equations, as C.2 already does.
    A proposal requires residual below `1e-10` and movement within the unchanged order identity tolerance.
    Every proposal faces the complete validation again.
    The raw prior candidates and all unconverged starts remain in the ledger.
    An unresolved identity still stops the exercise.
12. C.9 adds eight quantities after the first release gates passed.
    Gross trade profit excludes the trade cost. The stake bounds are sufficient bounds.
    Additional noise laws keep the prescribed full orders and score bound `1/b`.
    The Student law has three degrees of freedom and scale `b*(nu+1)/(2*sqrt(nu))`.
    Its entry set has two finite endpoints. The hyperbolic secant set is a half-line.
    C.9 has its own producer, independent acceptance layer, manifest, and registry rows.
    The final gate now requires this stage. C.0 tolerances remain unchanged.

**Commits.** The numerical and presentation commits through the validated state are:

| Commit | Subject |
|---|---|
| `11df9ca4a773fa333b0024f382ecfcd9dc89ca29` | Record committed numerical outputs before the zero-cost revision |
| `130af6a7868f25cd6d3ad37ec88e30793d8e39f3` | Adopt zero preparation cost and revise reserve endpoint contracts |
| `1b673896ae67b7d4dade55053d000d331f5532aa` | Recompute baseline controls and surplus at zero low cost |
| `94af1b884bf63c4ca7d367961112eb851cc10307` | Recompute complementary-signal outcomes at zero low cost |
| `79c03dc30f3a6e7e70707e4e882a4564c21cb6d2` | Recompute moderate values and the zero-cost construction |
| `2ce792cd7ef0591559a410b5aad9dfeb62b26ac1` | Reproduce posterior-tail outcomes under the revised declaration |
| `41609f07d5a5628db8ac4ccbb2a8ae579689e997` | Recompute exact reserve events and preserve the failed first attempt |
| `a74fc527b57c10c200e9730ea7d238a2d5128245` | Reproduce acquisition-payment outcomes under the revised declaration |
| `197a089d9ea9787d6fdf703e808ca04b2280fd94` | Recompute the correspondence and preserve all certificate and search outcomes |
| `79969299ec103320e031538b6f0cc890800aee1d` | Complete the zero-cost reserve sweep with bounded identity refinement |
| `f57f846da62514be0012b37a6af6c989be190395` | Validate all reserve events with the final reserve solver |
| `a6610090d4e19d0fa233cab77b195146152cc68a` | Render and reconcile all zero-cost exercises after the first release gate |
| `9faf2d70c164f4cc679ccceab7dd27061c0e9fe8` | Add and validate gross profits, stake bounds, and two fixed-profile noise laws |

A separate documentation commit records this report with the subject `Document the validated numerical revision and reconciliation`.
The complete branch sequence is available with `git log --reverse 1eb6d2c..revision/alex-2026-10-21`.


## Round 2

**Result: PASS.** The presentation pipeline and both full numerical release gates passed.
All numerical values remain unchanged from Round 1.
The comparison starts at commit `d28acdc9b43e816df9eb4d322e75d1373278afd0`.
This section supersedes the earlier presentation hashes in this report.

**U1: margin notes.** The revised manuscript has two high-cost bounds in (A1) and two trade bounds in (A2).
Table 2 now calls these the four strict margins of Proposition 2.
Its note reports the same low-cost value separately as a diagnostic.
Table 3 distinguishes the four atomic-cost conditions from the additional support condition for the cost mixture.

No margin column was removed.
Online Appendix (OA.77) still records the low-cost diagnostic, and C.3 retains its counterpart for the signal example.
Proposition A.6 still requires the low-support margin for atomless costs.
The online margins note states these distinct roles and retains the minimum of all five recorded quantities.
The diagnostic never attains that minimum in the six extension rows or the 25 signal pairs.
Thus each reported minimum also equals the minimum of the four surviving sufficient margins.

The margins table drops the low-cost slot from its displayed parameter vectors and states the zero atom in words.
The signal note uses the same convention and describes the four conditions in (OA.29).
The reserve note defines the floor diagnostic as gross profit at the lowest feasible belief.
Table 4 describes the automatic entry floor from zero-cost preparation.
Table 1 uses "challenger classes".

**U2: profit labels.** Figure 4 uses lowercase \(g_{\theta,\eta}\) on the profit axis.
Its four curve labels use \(g_{H,\eta}\) and \(g_{L,\eta}\).
The alternate caption in the renderer uses the same notation.
The data columns `G_H_eta` and `G_L_eta` keep their source schema; their values and file hash remain unchanged.
All edits originate in the renderer. No generated table received a hand edit.

**Numerical comparison.** `round2_before.json` records the 80 files present before this round.
`round2_comparison.json` records their final hashes and the following comparisons:

- All 30 numerical CSV files remain byte-identical, including both registry copies and all figure data.
- All 129 registry entries remain unchanged.
- All nine generated table bodies remain byte-identical; only seven sets of notes change.
- All three other figure PDFs remain byte-identical.
- Reconciliation changes 11 artifact or raster hash rows and zero scalar rows.
- Every current file hash recorded in the reconciliation matches its artifact.
- The registry manifest changes only its timestamp.
- The render manifest changes only its timestamp and output hashes.

The baseline reconciliation still compares this release with the original pre-revision reference.
The separate Round 2 comparison isolates this round from the numerical changes in Round 1.
No producer, parameter, tolerance, grid, result status, or open search record changes.

**Release gate.** This command ran the complete presentation sequence and both gates:

```bash
cd /home/uctpiaj/work/Projects/ccc-revision-numerics
/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python audit/revision_v2_2026_10_21/run_presentation.py round2
```

The sequence checks and builds the registry, substitutes quantities, renders all exhibits, builds both legacy PDFs, and updates the reconciliation.
It then runs `numerics/verify.py --final` and `numerics/release_checks.py`.
All eight commands exit with code zero.
The numerical gate reports `VERIFY PASSED`; all six release-boundary categories pass.
Substitution fills 103 placeholders, with zero unresolved and zero unknown keys.
The full sequence takes 24.39 seconds and uses no worker pool; native numerical threads are limited to one.

`presentation_round2_runs.json` records each command, duration, exit code, and log path.
The eight command logs have the prefix `logs/round2_`.
No test was written or extended. No test suite ran.

**Visual inspection.** Figure 4 and every affected table were inspected in the actual presentation output.
The inspected main-PDF pages are 19, 20, 28, 31, and 33.
The inspected appendix-PDF pages are 27, 33, and 37.
All revised notes and labels are readable, with no clipping or overlap.
`round2_visual_review.json` records the scope, PDF hashes, and preview hashes.
This review covers the affected exhibits, not every manuscript page.
The separate revised manuscript clone remains read-only throughout this work.

**Changed artifacts.** The table lists every changed pre-existing file in the Round 2 inventory.
`round2_artifacts.csv` also records each previous hash.
The generated Figure 4 remains at its usual ignored path; the commit includes its renderer and recorded hash.
The two legacy manuscript PDFs are tracked build outputs.

| File | SHA-256 after Round 2 |
|---|---|
| `audit/revision_v2_2026_10_21/output_diff.json` | `b68e2c51c4b362f99815c55064aea8ea941b8044b86e4992fe7e68f9afdf9779` |
| `audit/revision_v2_2026_10_21/reconciliation.csv` | `e9cee1778ae02a75b55ae3719d70f88de7be9d90c09b6161023b1ef18713ecb8` |
| `audit/revision_v2_2026_10_21/reconciliation_summary.json` | `b74480b96e4038d28d92e35396d895939e5e17c73e15659dbe1716d1af5f58bb` |
| `figures/bargaining_weight.pdf` | `e981d3f27d7858904b862b8769eddae251f27db697b287f1d2b0d11a2d39f7b6` |
| `numerics/manifests/c8_registry.json` | `544cca660629bad45af6158d0bbe1084c470037b89f0032a92ed77c2752a8533` |
| `numerics/manifests/render.json` | `98b805b5f493c096c1d28764952456042c251e27c8cca427249199ba48fd6a56` |
| `numerics/render/figures.py` | `c0bdde5a1863c70c23b5be741811bf89da042ca26d6556648caa72bcf2257ec9` |
| `numerics/render/latex.py` | `14b8e1ec37cbac842d5654ae5fd79ad23858652a64df3e0bc95823725b1c8153` |
| `numerics/render/tables.py` | `1b896883cbb96aaea43af778ba46eb3fa708772923025d9b18ed46b71f20a9d8` |
| `paper/main_filled.pdf` | `c9229dc878d212b25c46304c6d5e97e4cb1233ee9801fa55a79dd2ed438c4d48` |
| `paper/online_appendix_filled.pdf` | `fee9ce24362ecc5922492ca6776650adc44f58df90ffcb4192352694b1498778` |
| `tables/table1_auction_primitives.tex` | `ebeade4fb8bd116881e61880f8478eab7f83ac5a2c54da30e990f117545906a7` |
| `tables/table2_equilibrium_controls.tex` | `533ef7e15f77f4f74f80ab82ada3291d2d2aa7cd4fef6e8cff19ece23dcea3d9` |
| `tables/table3_extensions.tex` | `323bfed91e995a32734d5bf1b3002ddaa40c6818a963569ae9327b37c9bf3bf3` |
| `tables/table4_reserve_comparisons.tex` | `c5128fb2f6d2bd8051d18f1cb5530d54d1435e1cbe6de3b741ace75c0728dc9d` |
| `tables/table_extensions_margins.tex` | `cb53d3547cbce8dc7cb5b41537ed6912cac4e0a6a5648c14f5698036b25eebf0` |
| `tables/table_reserve_details.tex` | `fcee1a14685b35eb07b7213774fe08c0aa3fb042cd387714719d6a5337353bdf` |
| `tables/table_signal_grid.tex` | `a183760be44695670ed5109a6af92a082e6db56f2b51fdfd3d1f5b6884843c32` |

New audit files are `round2_before.json`, `round2_comparison.json`, `round2_artifacts.csv`,
`round2_visual_review.json`, `presentation_round2_runs.json`, and the eight `logs/round2_*.log` files.
This report receives the present section.
The shared handoff copies receive the updated report and reconciliation, plus the Round 2 evidence files.

**Commits.** Commit `259f528b7957527f263f7081b4e10bd3ea67e465` contains the renderer changes, generated outputs, reconciliation, and verification evidence.
Its subject is `Align rendered margins and profit labels with the zero-cost manuscript`.
A separate documentation commit records this section with the subject `Document Round 2 numerical presentation checks`.
Both commits are on `revision/alex-2026-10-21`. No push occurred.

## Round 3

**Result: PASS.** C.10, the presentation pipeline, and both full release gates passed.
The comparison starts at `0444ad22ec7e7ef6ea2adcd897bcbe8326825d28`.
All 129 earlier registry entries retain their complete records.
All 27 earlier numerical CSV files, all nine earlier tables, and all four figures remain byte-identical.
The legacy main PDF also remains byte-identical.
The revised manuscript clone received no edit.

**Inputs and choice.** All cases retain $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$, $c_L=0$, and $b=2$.
The supports in C have means $\ell$ and $h$; D replaces them with point masses.

| Case | Prior | High cost | Trade cost | Strengths $(r_0,r_1,r_2)$ | Low class | High class |
|---|---:|---:|---:|---|---|---|
| A | 0.3 | 4.5 | 0.01 | (1.1,3,3.6) | $\delta_{1}$ | $\delta_{10}$ |
| B | 0.7 | 7.2 | 0.01 | (1.1,3,3.6) | $\delta_{1}$ | $\delta_{10}$ |
| C | 0.7 | 6.7 | 0.02 | (1,4.5,5.5) | $U[0.6,1.4]$ | $U[1,19]$ |
| D | 0.7 | 6.7 | 0.02 | (1,4.5,5.5) | $\delta_{1}$ | $\delta_{10}$ |

A and B each change three of the five adjustable inputs: $c_H$, $k$, and $r_0$.
Both higher strengths retain their benchmark values.
The new high costs lie between the collapse ceiling and the favorable strong-economy return.
The weak strength moves toward the low value, so the weak spread falls below the new trade cost.
The original trade window is empty at either prior; a cost change alone cannot repair it.
With the trade cost fixed instead, the strong strength must exceed the original collapse strength.
That choice also requires three changes: the high cost and both higher strengths.

C uses broad classes above the reserve and a prior away from one half.
Its high class can lose to the incumbent, which makes the ownership condition substantive.
D isolates dispersion: class means, costs, prior, and incumbent strengths all match C.

**Outcomes.** The table gives the unique outcome at each strength.
A dash means no trade and no operative flow threshold.
“Unattainable” means the high-cost threshold exceeds the largest feasible posterior.

| Case | Strength | Entry | High-class ownership | $W_H$ | Threshold flow |
|---|---:|---:|---:|---:|---|
| A | 1.1 | 0.250000 | 0.075000 | 1.000000 | — |
| A | 3 | 0.464564 | 0.190421 | 1.000000 | 0.947381 |
| A | 3.6 | 0.250000 | 0.075000 | 1.000000 | unattainable |
| B | 1.1 | 0.250000 | 0.175000 | 1.000000 | — |
| B | 3 | 0.571808 | 0.452851 | 1.000000 | 0.879481 |
| B | 3.6 | 0.250000 | 0.175000 | 1.000000 | unattainable |
| C | 1 | 0.250000 | 0.175000 | 1.000000 | — |
| C | 4.5 | 0.563404 | 0.411984 | 0.924383 | 0.936639 |
| C | 5.5 | 0.250000 | 0.157102 | 0.897727 | unattainable |
| D | 1 | 0.250000 | 0.175000 | 1.000000 | — |
| D | 4.5 | 0.250000 | 0.175000 | 1.000000 | unattainable |
| D | 5.5 | 0.250000 | 0.175000 | 1.000000 | unattainable |

All weak rows have orders $(0,0)$. Both higher strengths have orders $(1,-1)$.
C raises strong-economy entry to 0.563404; D stays at 0.250000.
C raises strong-economy ownership to 0.411984; D stays at 0.175000.
At the collapse strength, C has lower ownership than at the weak strength because $W_H$ falls.

**All conditions.** The numerical condition file has 38 rows per case.
It records parameter domains, support widths, class order, equal admissibility, the mean gap, and the strength order.
It also records all four strict margins, collapse conditions, ownership conditions, and low-cost diagnostics.
A, B, and C satisfy every required condition.
A zero equality or weak-inequality margin has its stated relation; it is not treated as a failed strict inequality.

| Case | (A1) lower | (A1) upper | (A2) lower | (A2) upper |
|---|---:|---:|---:|---:|
| A | 1.460455 | 0.109179 | 0.005455 | 0.001349 |
| B | 0.562273 | 0.123413 | 0.005455 | 0.001349 |
| C | 0.021000 | 0.058891 | 0.006667 | 0.001770 |
| D | 0.025000 | -0.018122 | 0.020000 | 0.003171 |

| Case | Collapse exclusion | Collapse trade | Sufficient ownership | Exact ownership |
|---|---:|---:|---:|---:|
| A | 0.058137 | 0.005983 | 0.750000 | 0.384737 |
| B | 0.132569 | 0.005983 | 0.750000 | 0.396930 |
| C | 0.314551 | 0.008810 | 0.655478 | 0.338549 |
| D | 0.447727 | 0.011339 | 0.750000 | 0.000000 |

D retains its negative (A1) upper margin and zero exact ownership change.
Its analytical outcome label does not claim satisfaction of the complete proposition.
The global trade bounds still establish uniqueness at all three nodes.

**Registry intervals.** The referee’s approximate interval describes only a nonempty trade-cost window.
It does not describe the complete conditions at fixed benchmark costs.
The three open intervals are:

| Scope | Lower endpoint | Upper endpoint |
|---|---:|---:|
| Nonempty (A2) window | 0.40460967519168966482107943244773370178875092640359 | 0.59539032480831033517892056755226629821124907359641 |
| Fixed benchmark vector; parts (i)–(ii) | 0.46785002968614851183510213549029473648121592947564 | 0.53809590165309027184560734770108902187925039997012 |
| Fixed benchmark vector and collapse strength; parts (i)–(iii) | 0.46785002968614851183510213549029473648121592947564 | 0.50042430732006322816216753996977594675353215510280 |

The exact endpoint formulas are $(e/(4+e),4/(4+e))$,
$\left(141/(141+59e),19/(19+6e)\right)$, and
$\left(141/(141+59e),4245/(4245+1559e)\right)$, respectively.
The middle interval binds through the high-cost ceiling at its lower end and the fixed trade cost at its upper end.
The final interval binds through the collapse condition at its upper end.
The files retain fifty-digit evaluations; display rules use six decimals for the prior endpoints.

The benchmark trade-cost window is $(1/60,1/[12(1+e)])$.
Its bounds are 0.0166666666666666666666666666666666666666666666667 and 0.022411785114166260062403396514846977136237946652913.
The fixed $k=0.02$ has lower and upper margins 0.003333 and 0.002412.
The four-decimal display is $(0.0167,0.0224)$.
The spread ratio is 0.025 against the displayed bound 0.034.

The four-law entry range is $[0.301509,0.522757]$.
The endpoints come from logistic and Laplace noise with atomic costs.
The hyperbolic secant and Student values retain their status as diagnostics at fixed full orders.
No new equilibrium claim applies to those two laws.

**Validation and gate.** Exact decimal inputs enter the declared fifty-digit context directly.
Independent realized-auction integrals validate receipts, profits, and win probabilities.
Independent density roots and full-line integrals validate the threshold, entry, mean posterior, and mean price.
Both order signs use the 400- and 800-interval grids against each fixed candidate schedule.
The refined pass uses the required tighter quadrature target.
The analytical bounds cover every order and arbitrary mixtures; the mesh supplies a diagnostic.
Maximum independent formula discrepancy: 1.88738e-15.
Maximum initial quadrature estimate: 2.44725e-12.
Maximum refined quadrature estimate: 5.91825e-13.
Maximum posterior inversion error: 4.64073e-14.
Both deviation passes report zero profitable deviation.
The analytic Laplace tails have zero truncation error.
Every C.0 tolerance remains unchanged.

The first full gate stopped at a serialization mismatch.
Four derived CSV columns used ambient decimal precision instead of the declared local context.
The standalone producer used 28 digits; the gate used 50 after an earlier stage.
The serializer now applies the local fifty-digit context to the complete row.
The final producer and full pipeline then passed.
The first manifest, failed gate log, and repair note remain in the audit record.

The final producer took 3.60 seconds.
The full presentation sequence and both gates took 27.85 seconds.
All eight commands returned zero.
The numerical gate reports `VERIFY PASSED`.
Substitution fills 115 placeholders, with zero unresolved and zero unknown keys.
All seven release-boundary categories pass, including the new class category.
C.10 direct revalidation reproduces every saved CSV row.
The registry has 253 entries, including 124 new entries.
No test was written or extended. No test suite ran.
All work used one process and one native numerical thread.

The final commands were:

    /home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python numerics/exercises/c10_classes.py
    /home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python audit/revision_v2_2026_10_21/run_presentation.py round3_accepted

The presentation command invokes both final gates after the registry, substitution, renderer, typeset build, and reconciliation.
The run record is `presentation_round3_accepted_runs.json`.
The final logs have the prefix `logs/round3_accepted_`.

**Presentation and reconciliation.** The project renderer produces `tables/table_class_exhibit.tex`.
The legacy appendix contains the C.10 contract and the table.
Visual inspection covers appendix pages 47–49, including the table on page 48.
The inspected rows, notes, equations, and labels are readable, with no clipping or overlap.
The scope and final hashes appear in `round3_visual_review.json`.
This review covers the new material, not every manuscript page.

The reconciliation adds 3685 rows with the note “new, round 3”.
Every current file hash in that reconciliation matches its artifact.
The separate `round3_comparison.json` isolates this round from the earlier numerical revision.
The full condition margins are in `numerics/class_conditions.csv`.
The outcomes, bounds, deviations, and diagnostic records have the common prefix `numerics/class_`.
The run manifest is `numerics/manifests/c10_classes.json`.

**Commits.** `9e7ab4df4c69209c0429577db29cceaffe8747a4` contains the exercise, validated outputs, renderer, registry, contract, reconciliation, and gate evidence.
Its subject is “Add validated general-prior class exhibits and benchmark windows”.
A separate documentation commit records this section with the subject “Document Round 3 class results and benchmark intervals”.
Both commits belong to `revision/alex-2026-10-21`. No push occurred.

## Round 4: zero-cost controls and reserve table layout

**Result: PASS.** The final presentation pipeline and both numerical release gates passed.
The implementation commit is `8eb6c2ea0a96e9f4ad8c56de9917b049015eab70` on `revision/alex-2026-10-21`.
The reference for this round is `0ee9c02a4eff21337543e838a0c9d0e803ff3baf`.
No push occurred.

**C15.** The C.0 contract now states that the lower plateau enters at $B(m) \ge 0$.
The reserve table note states the same rule when $c_L=0$.
A source comment explains the zero-cost rule beside the legacy serialized identifier.
That identifier stays unchanged to preserve the numerical records and their joins.
No solver, parameter, tolerance, or numerical value changes.

**Table layout.** The renderer already allowed breaks after semicolons, underscores, and vertical separators.
It now also allows breaks after equals signs.
The parameter-identity note uses left alignment with a ragged right edge.
This removes the three underfull lines in that note without extra space between words.
The appendix has two other underfull paragraphs outside the table.
It also reports an overfull line at the unchanged release command in Appendix E.
These paragraphs remain outside this small revision.

**Verification.** All 35 numerical CSV files remain byte-identical to the reference for this round.
All 253 registry rows remain identical in every field, including values, intervals, and displays.
The complete reserve table body also remains byte-identical.
The four figure PDFs and the main manuscript PDF remain byte-identical.
The registry manifest changes only its timestamp.
The render manifest records its new timestamp and the reserve table hash.
`round4_before.json` preserves the reference hashes and registry rows.
`round4_comparison.json` records the final comparison and command results.

The final command was:

    /home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python audit/revision_v2_2026_10_21/run_presentation.py round4_accepted

All eight commands returned zero in 28.23 seconds.
The numerical gate reports `VERIFY PASSED`.
All seven release-boundary categories pass.
Substitution fills 115 placeholders, with zero unresolved and zero unknown keys.
The run record is `presentation_round4_accepted_runs.json`.
The final logs have the prefix `logs/round4_accepted_`.
No test was written or extended. No test suite ran.
The sequence used one numerical process at a time, with one native numerical thread.

Visual inspection covers appendix page 20 for the controls and page 37 for the reserve table.
Both pages show readable text, complete rows, and no clipping or overlap.
`round4_visual_review.json` records the scope, PDF hash, and page-image hashes.

**Changed artifacts.** The implementation files and their SHA-256 hashes follow.
The full list, including audit evidence and both handoff files, is `round4_artifacts.sha256`.
Paths in that index are relative to this worktree; the index omits its own hash.
The reconciliation adds one Round 4 row per changed source, output, or evidence artifact.
It omits itself and the checksum index to avoid circular hashes.
The final checksum index includes the reconciliation hash.
Both copies of this report and `reconciliation.csv` are byte-identical.

```text
7ed01bea92b258764fa4b2e646605d1255ed0d24f669eff30d07cca81b93aa0a  numerics/continuations.py
2f2bc5df4a9b21174b2bc2ec8511084f5b5f4dea7aafe6b58618143700dfc6a0  numerics/manifests/c8_registry.json
b52d0a5bd5eb2fa866c66043e54847f0b2299e0e80545e9b3e4637ce5b178a79  numerics/manifests/render.json
c76238fe4cfdc740ea80a3b3b06d961855c854ea2cb1015491e3ab0e5cb2674a  numerics/render/tables.py
99a9426dab5ae574a2b3ee8e44c8098c910ba02510e8acd54963799c68c54409  paper/online_appendix.md
ae0c8caf2f18753636e788efebcf1a11e799be3df86c0fbb6e1374e911010dd5  paper/online_appendix_filled.md
79e375ab1f97e9a7252b29557fb383c8eadc8e0ddf0e33100918fb00324376d5  paper/online_appendix_filled.pdf
b71af561cfec0450766a4a2ea4a5e1ef00c76af969f4dd0fcb598790abfe5d86  paper/online_appendix_filled.tex
46f08b3f6af4156d76455f982ac05217f415518e967ac48923bb0b84197c7dcf  paper/online_appendix_filled.tex.md
a6b42e5c5b2871b401bbcc3e1482220a08efdb85c043b04b146205639c09031b  tables/table_reserve_details.tex
```

A separate documentation commit records this section, the reconciliation, and the complete audit evidence.

## Round 5: final manuscript sync

**Result: PASS.** The full presentation pipeline and both numerical release gates passed.
The implementation commit is `7eedc08c9e97a586bfced9f4bd5af29813c60ebb` on `revision/alex-2026-10-21`.
The reference for this round is `f222ba3f83b389660fa3a818b5302d4032c88e33`.
The manuscript reference is `f94b10de76f50ca724029e6800623769588ca18b` in the separate revision clone.
Every tracked file in that clone remains unchanged. No push occurred.

**Source sync.** The reserve-details caption now refers to Table 5.
The other generated table notes correctly refer to Table 3.
The generated figures contain no table-number reference.
The class exhibit remains Table 4 in the manuscript.
The contract now includes these manuscript edits:

- C.8 includes C.10 in the exercise list.
- C.8 states the C.10 display rules and includes both quantity-family rows.
- E.1 includes the C.10 producer command.
- C.6 points to Table 5.
- C.10 points to Table 4 of the paper, including its declaration notes and feed line.
- The C.10 pointer replaces the local table input, as in the manuscript clone.

The legacy reserve-table filename and the class-table label remain unchanged.
The historical reserve-event identifier remains unchanged in the numerical records.
The existing Round 4 reserve-note layout remains in the generated table.

**Numerical invariance.** All 36 CSV files in the recorded numerical scope remain byte-identical.
This scope includes the numerical outputs, table inputs, figure inputs, verification outputs, both registries, and the quantity manifest.
All 253 registry rows remain identical in every field, including values, intervals, and displays.
The complete reserve table remains byte-identical except for its caption reference.
The class table and all four figure PDFs remain byte-identical.
No numerical value, parameter, solver, or tolerance changes.
The registry manifest changes only its timestamp.
The render manifest changes its timestamp and reserve-table hash.
`round5_before.json` records the reference hashes and registry rows.
`round5_comparison.json` records the comparison, source checks, and command results.

**Verification.** The command was:

    /home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python audit/revision_v2_2026_10_21/run_presentation.py round5

All eight commands returned zero in 30.21 seconds.
The numerical gate reports `VERIFY PASSED`.
All seven release-boundary categories pass, including direct revalidation of C.10.
Substitution fills 115 placeholders, with zero unresolved and zero unknown keys.
The generated appendix text contains every requested addition and the corrected reserve caption.
The run record is `presentation_round5_runs.json`; the logs use the prefix `logs/round5_`.
No test was written or extended. No test suite ran.
The sequence used one numerical process at a time and one native numerical thread.

**Artifacts and handoff.** `round5_artifacts.sha256` lists every changed source, output, and audit artifact with its SHA-256.
Its paths are relative to this worktree. The index omits its own hash.
The reconciliation retains the prior rows and adds one Round 5 row per changed artifact.
All file-hash rows use the current artifact hash; their old-value columns retain their original references.
The reconciliation omits itself and the checksum index to avoid circular hashes.
The checksum index includes the final reconciliation hash.
Both copies of this report and `reconciliation.csv` are byte-identical.
A separate documentation commit records this section, the reconciliation, and the audit evidence.
