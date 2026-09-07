# C.2 checkpoint for tmux migration

2026-09-05. Work paused on the parent's request during a quick run. No commit, full rerun, or completion claim.

## Running job

- Parent PID 42686, shell PID 42660, workers 42714 and 42715. Unified exec session 92136.
- Command: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 .venv/bin/python -u numerics/exercises/c2_correspondence.py --quick --workers=2 --out=audit/peer_polish/c2_quick_vm > audit/peer_polish/logs/c2_quick_vm.log 2>&1`
- At checkpoint: elapsed 2m53s, each worker ~99% CPU and 76 MB RSS. Log not yet written; original code only prints at completion. Certificates/thresholds already written to the distinct audit directory.
- This process imported code BEFORE the edits below. Preserve its outputs and log as the initial quick diagnostic. It is not a validated run of the final source. Do not kill it merely to migrate the terminal.

## Files changed

- `numerics/error_budget.py`: nonfinite quadrature, tail, residual, inversion, and independent-entry errors now breach validation; previously NaN comparisons silently passed.
- `numerics/mixed_search.py`: final convergence now requires checked low-residual monotonicity, valid simplex and nonnegative weights; actual low support payoff and gain saved in immutable attempt record and CSV. Previously monotonicity was informational only, low-state support payoff absent.
- `numerics/exercises/c2_correspondence.py`: rejected/open/no-candidate statuses cannot remain accepted merely because scan passed; actual low support payoff/gap and refined high/low gaps recorded; duplicate-grid acceptance assertion replaced by explicit exception; quick reports no unexecuted refinement nodes; run records workers/thread limits/runtime; future quick/full prints progress.
- New `numerics/tests/test_s3_c2.py`: five regressions for canonical Decimal node identity, status distinctions, NaN budget rejection, mixed premise/records, certificate-root deduplication.
- `numerics/status_rules.py` unchanged this session.

Tests: original WIP 2 failed / 3 passed in 5.50s (`logs/c2_tests_before.log`); patched code 5 passed in 5.68s (`logs/c2_tests_after.log`). After subsequent high-support reporting and progress/runtime edits, final-source rerun passed 5/5 in 5.45s; the after log holds that result. No scientific tolerance/grid/budget altered.

## Resume

1. Inspect running PID/log and await quick result. Any failure must be diagnosed; do not treat old CSVs as current.
2. Rerun `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python -m pytest -q numerics/tests/test_s3_c2.py`.
3. Coordinate with continuation adapter owner: that agent is repairing complete price atoms and preparation identity in `numerics/continuations.py`. C2 depends on its adapter and deduplication. I flagged near-pooling/near-full pure candidates within 1e-7 potentially getting distinct pricing/preparation identities. Read their checkpoint for final changes before new process.
4. Run final-source quick in another distinct audit directory if needed, inspect manifests, accepted budget errors, certified roots, near-boundary statuses and multiplicity. Initial quick does not include current data-record repairs.
5. Launch full `.venv/bin/python -u numerics/exercises/c2_correspondence.py --workers=20` with all four thread env limits 1 after quick validation. User authorized VM optimization: 64 vCPU,125 GiB RAM; budget C2 20 workers, C6 20, independent checks8. Record log under audit. Do not change tolerances, scientific grid, or search starts. Full outputs use numerics default and manifest `numerics/manifests/c2_correspondence.json`.
6. Inspect accepted rows and complete manifest, notify parent and figure owner. No fallback without bounded repair evidence. Parent owns commits and final gate.

Figure owner informed: correspondence.csv drops `duplicate_of` rows, attempts CSV preserves all; `n_distinct_accepted` and multiplicity count complete continuation identities per canonical r. Across-r continuation ID is not stable because parameters enter identity. Conservative plots connect a branch only with a unique accepted row at each adjacent global node and break missing/ambiguous intervals.

Known broader caution: mixed search is a finite mesh heuristic with explicit unresolved attempts, not a nonexistence theorem. Support gap checks are numerical diagnostics. Missing independent companion package remains the project's declared limitation.

## Resumed run update

The pre-migration quick completed. Patched quick completed in193.7s and passed all manifest/certificate/budget/finite-scalar checks. Detailed row inspection then found near-asymmetric duplicates due to the stricter complete-atom identity. These are now polished to the existing accurately bracketed root and the rebuilt schedules are revalidated. A targeted run at1.51,1.55,1.8 passed with exactly2 distinct accepted continuations at each node. Seven regression tests pass in23.85s; `logs/c2_tests_final.log`.

The full final process is active with20workers, all thread limits1. Current unified session77701; log `logs/c2_full_vm_final.log`. Source snapshot hashes and start time are in `c2_full_source_snapshot.json`. At312.1s it had finished150/580 base nodes. Further refinement follows. Do not treat canonical correspondence output as new until the final manifest is written. No additional source edits are planned during this run.

Final changes also exclude duplicate attempt labels from the refinement branch-set comparison. This prevents unnecessary refinements triggered solely by a repeated search path. Mixed support schema has `off_support_gain_mesh`, both-state payoff/gain records and complete IDs. C2 uses the final continuation adapter's acceptance result for atom validity. Mathematical nonfinite cutoffs are tagged `always` or `unattainable`.

## Final state

Full run and bounded interior-root replay complete. Canonical C.2 outputs and manifest are frozen and validated. No running C.2 process remains. See `logs/s3_c2_revision.md`, `logs/c2_final_row_checks.log`, and the manifest validation_replay/source hashes for reproduction. Eight regression tests pass. Parent owns the final release gate and commits. No fallback was used.
