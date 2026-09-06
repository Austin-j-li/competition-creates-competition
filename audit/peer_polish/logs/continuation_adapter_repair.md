# Shared continuation adapter repair

Completed on the VM on 2026-09-05. Source: `numerics/continuations.py`; regression checks: `numerics/tests/test_continuation_adapter.py`.

The adapter now partitions flow at the candidate's support and threshold breakpoints. It records each constant-price preimage as an interval or interval union, merges equal-price pieces, calculates state masses from analytic tails, and checks these against segment quadrature. This replaces the 200001-point estimate of a lower no-entry cutoff. Laplace lower and upper plateaus and disconnected mixed-profile plateaus are represented explicitly. The resulting pooled posterior determines atom preparation and the atom-conditional price check. Exact floor/ceiling ties remain admitted.

Preparation on nonatom prices records the two sides of each cost threshold; uniform costs use the declared support and individual cost cutoff. Each atom has its own preparation actions. Economic identity now includes the positive-entry price map, full atom preimages and posterior, and posterior information map, in addition to orders and preparation. Rejected atom checks clear analytical status, existence/uniqueness claims and the zero rigorous deviation bound.

The investor-deviation implementation already holds the candidate schedule fixed. A new independent integration check verifies both types and both order signs using the held candidate's price and preparation, while changing only the deviator's density center and signed exposure.

Validation: all six new regressions and all eight original S2 regressions passed, 14/14 in 16.80 seconds, with single-thread numerical libraries. Log: `continuation_adapter_tests.log`. Fresh C.6b producer passed all seven gates (auction domain, whole family, monotonic outcomes, rational global bound, endpoint landmarks, complete identity, and expected negative controls). Log: `c6b_vm_repair.log`. `git diff --check` passed. No acceptance tolerance was changed. C.2 and C.6 were notified to start their fresh runs using this source.

The atom finder uses the candidate's existing root-solved threshold partition. This remains a numerical diagnostic for general searched profiles; it does not establish exhaustive pool search or a continuum certificate for the displayed search curves. Alternative pool searches retain their existing declared coverage limitations.
