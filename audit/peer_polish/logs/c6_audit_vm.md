# C.6 VM audit

## Scope and commands

The first full VM run used twenty process workers; the event regression used eight. Both set `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1`. The VM has 64 virtual CPUs and 125 GiB RAM. The workers' numerical operations stay single-threaded. Default worker counts in both C6 entry points now cap at eight when no explicit count is supplied.

The fixed-reserve producer is `numerics/exercises/c6_reserve.py --declared-only --workers=8 --out=audit/peer_polish/c6_fixed_vm`. Its separate output and manifest let the independent core checker pin freshly validated fixed comparisons while the full sweep runs. The eight supported comparisons passed, with maximum payoff-oracle difference 1.7763568394002505e-15. Its early output predates the final full price-atom adapter; the final canonical C6 outputs include that repair and complete row identifiers.

Final sweep command: `.venv/bin/python numerics/exercises/c6_reserve.py --workers=20`, log `c6_full_vm_refined.log`. Final event command: `.venv/bin/python numerics/exercises/c6c_reserve_events.py --workers=8`, log `c6c_vm_refined.log`.

## Repairs

The C6 row builder now applies the shared separate numerical error budget before acceptance. A root-discontinuity rejection cannot retain `accepted=true`. Allocation outcomes are validated before continuation conversion; legacy high-value ownership uses the actual allocation probability. Unavailable pooled posteriors use `n/a`.

Every pure solver initialization is retained before economic deduplication. The shared pure search deduplicates within a call, so C6 submits its nine declared starts separately. Node diagnostics retain their original endpoints, unsuccessful starts, the asymmetric scan, and mixed supports, weights, payoffs, and iteration history. Converged mixed search that ends pure receives full validation. The support simplex, order bounds, and support-payoff gap are checked. Search failures are counted as open attempts, not rejected candidates or empty equilibria.

The completed node ledger is flushed incrementally to JSONL. Counts come from attempted nodes and validated economic identities. The fixed comparison selector removes duplicates and includes full parameter, institution, information, continuation, and candidate identifiers. A quick or fixed-only run records zero executed refinements.

## Preserved first attempt and bounded refinement

The first event run passed T21–T23 on 257 nodes, but its broad diagnostic coverage revealed solver endpoint artifacts. At binary r=1.2, p=6.2817191715409547646397125286473, a pure solver endpoint near 0.9999999046 differed enough in induced atom prices from exact full orders to exceed the stricter identity tolerance. It generated an apparent count of three continuations. These were floating-point solver approximations, not evidence of three equilibria.

I preserved the original source, event outputs, manifest, and full initial ledger. The first full sweep was stopped before refinement with 1,039 completed initial nodes and one unfinished node, uniform classes r=3,p=8. The exact stop record is `audit/peer_polish/c6_20260905T233226530208Z/interrupted_for_endpoint_refinement.json`. Its original ledger remains beside it.

The bounded repair follows C2. An order within the existing solver convergence tolerance 1e-7 of -1, 0, or 1 proposes that exact endpoint. The candidate schedule is rebuilt and fully revalidated. Original solver profiles remain in diagnostics. No acceptance or identity tolerance changes. The target regression now finds one continuation and retains ten absorbed duplicates. This is an additional validated candidate construction, never a claim that rounding preserves an equilibrium without checking deviations.

`numerics/tests/test_c6_audit.py` passes three regression checks. Log `c6_audit_tests_vm.log` records 3 passed in 13.85 seconds. The preceding S2 regression run passed all eight checks; shared adapter tests are recorded separately by their owner.

## Scientific limits

The reserve search constructs the benchmark price rule, whose zero-entry preimage forms a pool. It does not search arbitrary alternative price cutoffs. The explicit fixed-order price-pool family is separately validated by C6b. Full continuation identity includes price atoms and preparation rules through the repaired shared adapter.

Pure starts are (u,v) in {0.2,0.6,0.95} squared, at most forty damped best-response iterations with bounded fsolve polishing. Mixed search uses high-type supports on the 0.05 mesh, initially uniform weights, low-type magnitude 0.5, and at most 150 multiplicative-update iterations. It has no bidirectional warm starts. Final investor deviations use both signs and initial/refined 400/800 interval grids. Finite-grid evidence remains numerical diagnostic unless a stated analytical bound applies.

The initial reserve grid has spacing 0.05 plus the declared support/participation events and one-sided offsets 1e-4,1e-6,1e-8. Intervals next to a found revenue maximum, a branch-set change, or an unresolved endpoint are refined to spacing 0.002. Found extrema are not global optima. Final counts and validation outcomes are to be appended after the current reruns finish.

A separate profiling diagnostic at uniform classes r=3,p=8 was deliberately limited to sixty seconds. It timed out inside the pooling candidate's refined deviation scan. Its log `c6_p8_profile.log` records millions of small interval-construction calls caused by a large threshold-breakpoint list. The full run subsequently completed both class p=8 nodes without error. This profiling timeout is not an equilibrium rejection or a failed release regression. I made no further numerical changes for that performance issue.

The final event rerun passed T21, T22, T23 and the payoff oracle on all 257 nodes. It records 634 candidate attempts, 447 raw acceptances, 180 rejections, seven open tangency candidates, and 190 merged duplicates. All 257 nodes have an accepted continuation; none has multiple accepted distinct continuations. The event CSVs contain no ordinary NaN or infinity scalar fields. The standalone `audit/peer_polish/check_c6_ledger.py` reconciles these counts with the retained JSONL records and verifies economic range calculations, deduplication targets, and accepted-row budgets.

## Final classification and retained evidence

The producer now separates a rejected terminal candidate from an unresolved search. `finalize_node` uses recorded validation breaches to mark the terminal profile rejected and retains the independent search-unresolved flag. The same finalizer runs in fresh solves and deterministic replay. A targeted regression confirms that the original raw record remains unchanged.

Two refined class-economy nodes, r=1.2 with p=0.9621 and p=0.9641, also needed bounded identity refinement. Their pure solver endpoints lay about 1.1e-7 from independently solved asymmetric roots, producing tiny atom differences that exceeded the stricter identity tolerance. When this ambiguity is detected, the producer proposes the already-solved nearby asymmetric root, rebuilds the schedule, and repeats full validation. Both now have two distinct continuations, pooling and informative. Each preceding fourteen-candidate pass remains in `prior_identity_attempt`; the manifest records 28 preceding candidates separately from the final-pass counts. No tolerance changed.

The final raw producer source automatically applies both refinements. Replay uses exactly the same logic. Actual finalization commands were:

```
.venv/bin/python numerics/exercises/c6_reserve.py --workers=20 --replay=audit/peer_polish/c6_20260905T233640627218Z
.venv/bin/python numerics/exercises/c6c_reserve_events.py --workers=8 --replay=audit/peer_polish/c6c_20260905T233647072695Z.jsonl
.venv/bin/python audit/peer_polish/check_c6_ledger.py
```

All use the same four thread limits stated above. The root-refinement replay log is `c6_vm_identity_replay.log`; the event status replay log is `c6c_vm_status_replay.log`. The previous raw ledger and CSV snapshots remain under `audit/peer_polish/`.

The following are final-pass counts. They supersede the earlier status counts while preserving the earlier attempts as audit evidence.

| Exercise | Nodes | Candidate attempts | Raw accepted | Rejected | Unresolved attempts | Duplicates | Open searches |
|---|---:|---:|---:|---:|---:|---:|---:|
| c6_reserve | 1664 | 11414 | 9607 | 1323 | 484 | 7344 | 503 |
| c6c_reserve_events | 257 | 634 | 447 | 187 | 0 | 190 | 7 |

The full sweep has 392 nodes in each binary economy, 464 in the weak class economy, and 416 in the strong class economy. Their open-search counts are 116,116,155,116 respectively. Every attempted node has an accepted candidate. There are 599 full-sweep nodes with two distinct accepted continuations and none with more than two after refinement. All accepted rows satisfy the separate arithmetic budgets. The maximum payoff-oracle difference over the sweep is 2.1269444538951632e-14. Eight fixed comparisons and event regressions T21–T23 pass. The four C6 unit regressions pass in 13.72 seconds; the ledger check also passes.

The weak found revenue maximum in both value laws occurs at the exact floor event, with revenue 0.7852147714426196. The strong found maximum occurs at the exact expensive-entry ceiling event, with revenue 1.0688544444308778. Those are found maxima in the declared pricing-family search, not seller optima over arbitrary continuations. The negative strong-reserve preparation comparison remains in the fixed comparison table.

C6 supports the audited exploratory scope; no C6 fallback is needed. T26 covers the retained finite search and counts, with 503 open search scopes explicitly retained. No statement of exhaustive mixed-search nonexistence or arbitrary-pool/global reserve optimality follows from these results.
