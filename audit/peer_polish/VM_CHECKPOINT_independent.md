# Independent core checks checkpoint

Saved 2026-09-05 23:23 UTC for the tmux migration. No jobs were killed.

## Work and ownership

Own `audit/peer_polish/independent_checks.py`, its results/logs, and canonical producer outputs from C1/C3/C4/C5/C7. Parent approved those output writes. No manuscript or renderer edits. No numerical producer source changes made. Other workers own C2, C6, continuations, manuscript and presentation.

Read the handoff, VM guide, CLAUDE, S1 acceptance and independent checker. The existing checker implements T02–T15 including 25 accuracy pairs and both profiles at both strengths. Added explicit `--workers`, input CSV SHA256/change detection, exact signal row counts, and analytical/diagnostic/rejected status checks. Corrected an unfinished checker assumption: rejected informative signal candidates intentionally omit reported cutoffs in C3, so only accepted informative rows require a cutoff. Independent entry/payoff checks still cover all 100 rows. The modified script passes `py_compile`; its full run has NOT started.

## Live producer batch

- Exec session ID `56634`; parent shell PID `44192`, Python supervisor PID `44279`.
- Currently C3 PID `45392` at checkpoint, C1 already completed successfully.
- Full log `audit/peer_polish/logs/s1_core_producers_vm.log`.
- Supervisor runs C1, C3, C4, C5, C7 sequentially and stops on the first nonzero exit.
- Environment uses `.venv/bin/python -u` and `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1`.
- C1 passed in 74 seconds, at `2026-09-05T23:22:42Z`. C3 began then.

Use the log and `ps` to determine whether the existing batch survived. Do not duplicate running producers. Completed producer outputs and manifests are canonical. No commits made.

## Next steps

1. Wait for all five producers or diagnose a nonzero exit, preserving this log.
2. Coordinate with C6 before the independent run. `reserve_comparisons.csv` must remain consistent throughout the run. C6 worker says schema stays, supported ownership is corrected, and offered early fixed-node output. I requested either canonical fixed output held unchanged during independent run or a separate audit copy. Await their reply.
3. Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 .venv/bin/python -u audit/peer_polish/independent_checks.py --workers=8 > audit/peer_polish/logs/s1_independent_checks_vm.log 2>&1`, retain exit status/full output. Expected roughly 15 minutes. The script writes `independent_checks.json` and `logs/s1_independent_checks.md` only at completion.
4. Diagnose any failure without relaxing tolerances; any source change outside checker needs coordination. In particular the run has never previously reached final signal-object tests, so there may be other unfinished checker assumptions.
5. Existing `logs/s1_certificates.md` reports 186 passes, full seed/port endpoint comparison, independent quadrature, T17 outward display checks. Preserve the historical evidence and missing-companion limitation. `certificate_checks.py` should be rerun after final registry/substitution to check final displayed intervals. Parent was told this.
6. Report actual pass/fail counts, environment, changed files, producer completion and unresolved limitations to parent. Parent commits.

The promised external `reference_oracles.py` package was not supplied. The independent implementation here must not be described as that missing package.
