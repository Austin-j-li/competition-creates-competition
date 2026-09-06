# C.2 source repairs and validation

The stopped rewrite was read against specification section 10 and the existing S3 source audit. The initial VM quick run passed its aggregate gate but exposed false multiplicity from near-boundary solver iterates. Its original files remain in `audit/peer_polish/c2_quick_vm/`.

The resumed changes enforce finite error-budget values, require the checked low-residual monotonicity premise before a mixed search is called converged, record actual payoffs and payoff gains for both types, and distinguish numerical mesh gains from enclosed bounds. Search attempts that collapse to pure strategies are polished with the existing continuous pure best-response solver. Endpoint coordinates within its existing 1e-7 convergence tolerance are snapped to the exact known endpoint, then the rebuilt candidate is validated. This prevents a near-zero iterate from counting as an additional equilibrium beside exact pooling. At the high-cost ceiling, exact full orders use the declared symbolic tie rule on every search path.

Complete continuation validation now also gates candidate acceptance, including the adapter's atom beliefs, atom pricing and preparation checks. The interval-certificate rows explicitly record their between-grid coverage. Numerical candidates retain their numerical-diagnostic status and the recorded unclosed Lipschitz error. The mesh support file carries candidate, continuation and parameter IDs. Unavailable scalar values are n/a; unattainable/all-flow cutoff cases have explicit tags. No acceptance tolerance, grid spacing, interval precision or search start was changed.

The first regression run failed 2 of 5 checks on the interrupted code, proving that NaN quadrature errors silently passed and failed residual monotonicity did not prevent a converged label. All six current regressions pass, including a near-pooling duplicate regression; see `c2_tests_final.log`.

For the full VM run, BLAS/OMP/MKL/NUMEXPR threads are one and the process pool has 20 workers, as requested for the 64-vCPU VM. The same immutable schedule reached through repeated search paths is validated once per strength node; every attempt remains in the output. This cache changes no arithmetic or acceptance test. Canonical thresholds and the new quick thresholds are byte-identical; the independent-check run approved their identical rewrite before the full run.

Final-source quick and full run results will be appended after their manifests and row checks are inspected.

## Completed validation

The full run passed in 822.59 seconds with 20 workers. It evaluated 580 declared nodes and 12 local refinements. The row audit found one remaining numerical copy of the symmetric interior root at r=1.79. The source now polishes both held-schedule first-order conditions before validating any interior pure candidate. All 23 nodes containing such a candidate were rerun in 91.51 seconds. The preserved full outputs are in `audit/peer_polish/c2_full_before_interior_polish/`; repaired outputs are in `audit/peer_polish/c2_interior_polish/`.

Replay the bounded rerun and merge with:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 .venv/bin/python -u numerics/exercises/c2_correspondence.py --workers=20 --nodes=1.7479775382679625,1.7488775382679625,1.75,1.755,1.76,1.765,1.77,1.775,1.78,1.785,1.79,1.795,1.8,1.805,1.81,1.815,1.82,1.825,1.83,1.831,1.832,1.833,1.834 --out=audit/peer_polish/c2_interior_polish
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 .venv/bin/python audit/peer_polish/c2_merge_revalidation.py
```

The merge checks both preserved input manifests, refuses changed schemas or newly required refinement nodes, recalculates counts and hashes, and records the source hashes and replay provenance in the final C.2 manifest. A fresh full producer run applies the same root polishing automatically.

Final output: 592 nodes, 6000 attempt rows, 1841 distinct rows, 4159 duplicate attempts, 40 open search rows, and 80 nodes with at least two distinct accepted diagnostic or established continuations. No accepted row breaches an error budget; all six output hashes match; no numeric cell contains NaN or an untagged infinite scalar; no near-duplicate pure profile remains. All 7022 accepted state-support groups pass simplex, support-bound, complete-ID join, support-indifference and tested-deviation checks. Evidence is in `c2_final_row_checks.log`. Eight regressions pass in 74.33 seconds (`c2_tests_final.log`).

One mixed finite-support candidate at the pooling boundary r=1.7478775382679625 passes the declared numerical tolerance. The high type uses orders 0 and 0.025 with weights 0.6224709925 and 0.3775290075; the low type is approximately at zero. Its high-type support-payoff gap is 1.1914e-8 and the largest tested gain relative to a support point is 1.2044e-8. These are below 1e-7, but its between-grid bound remains open. It is retained as a numerical diagnostic, not an exact mixed-equilibrium existence result. The 41 unresolved mixed-search attempts remain recorded; no mixed nonexistence claim is made.
