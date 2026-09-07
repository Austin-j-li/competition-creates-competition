# C.6 final VM checkpoint

C6 numerical work is complete. No C6 process is running. Parent owns commits and final manuscript/presentation packaging.

- Full source: `numerics/exercises/c6_reserve.py`.
- Event source: `numerics/exercises/c6c_reserve_events.py`.
- Regressions: `numerics/tests/test_c6_audit.py`, four passing checks.
- Run/retry narrative: `audit/peer_polish/logs/c6_audit_vm.md`.
- Final ledger audit: `audit/peer_polish/check_c6_ledger.py`, output `c6_ledger_verification.json`, passing both exercises.
- Final source/output hashes: `audit/peer_polish/c6_final_vm_manifest.json`.

Canonical full outputs contain 1,664 nodes, 11,414 final-pass candidate attempts, 9,607 raw acceptances, 1,323 rejected candidates, 484 unresolved solver attempts, and 7,344 merged duplicates. There are 503 open searches. Every node has an accepted candidate; 599 nodes have two distinct accepted continuations. No node has more than two after bounded refinement. Twenty-eight preceding identity-refinement candidates are separately preserved in the ledger and manifest.

The final event corpus contains 257 nodes, 634 attempts, 447 raw acceptances, 187 rejected candidates, zero unresolved solver attempts, 190 duplicates, and seven open searches. Every node has exactly one accepted continuation. T21–T23 and the payoff oracle pass. The fixed eight reserve comparisons pass and carry full parameter/continuation identifiers.

No C6 scope fallback is needed. Retained broad search remains a finite numerical diagnostic of the benchmark price-rule family; it is not an exhaustive arbitrary-pool continuation search or seller-optimal reserve result.

The full numerical run used twenty workers with all four native thread limits set to one. It completed under log `c6_full_vm_refined.log`. Exact raw ledgers are in `c6_20260905T233640627218Z/`. Status and bounded two-node identity repair used the producer's `--replay` path; final log `c6_vm_identity_replay.log`. Event raw results are in `c6c_20260905T233647072695Z.jsonl`; final event status replay log `c6c_vm_status_replay.log`.

The first optional VM sweep was interrupted after 1,039 initial nodes when endpoint artifacts were found; all its records and exact unfinished node are preserved. The sixty-second p=8 diagnostic profile deliberately timed out; the full producer subsequently completed that node. These are historical attempts, not hidden release failures.
