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
