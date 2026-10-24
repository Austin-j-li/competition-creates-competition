# E2 independent calculations

Run these commands from the repository root:

    PYTHONDONTWRITEBYTECODE=1 bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh .venv/bin/python audit/microstructure_search_2026_10_22/scripts/XE2_check/independent.py
    PYTHONDONTWRITEBYTECODE=1 bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh .venv/bin/python audit/microstructure_search_2026_10_22/scripts/XE2_check/domains.py

Both programs print their results.
They contain no assertions.
The programs use exact fractions for A and 70-digit arithmetic for B.
The first program integrates the auction pieces and sums the joint signal law.
The second program examines the prior boundaries and computes the Laplace cost integral with elementary antiderivatives.

The saved outputs are independent_output.txt and domains_output.txt.
Files whose names start with e2_ contain later reruns of the original E2 programs.
Those programs ran only after the first independent calculation produced all four headline results.
The independent program later ran again after a label correction.
That correction distinguishes frozen weak Laplace orders from the weak equilibrium.
No E2 source or output file changed.

The runs used no more than three slots at once.
The wrapper guarded every numerical run.
The main memo is ../../memos/XE2_check.md.
The run_manifest.json file records source hashes, output hashes, software, and the calculation method.
