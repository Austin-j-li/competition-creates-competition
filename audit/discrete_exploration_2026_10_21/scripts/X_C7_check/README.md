# Reproduce the C7 check

Run these commands from the repository root:

```sh
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C7_check/reproduce.py
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C7_check/certificates.py
```

The first script uses 70 decimal digits.
It prints benchmark payoffs, mixed branches, and the continuous-Laplace comparison.
It saves those values in `independent_output.txt`.
Surplus comes from allocation values less preparation costs.
The script separately prints its difference from the sum of financial payoffs.

The second script uses exact rational interval endpoints.
It bounds the exponential with consecutive alternating partial sums.
It prints cutoff signs, benchmark intervals, deviations, and two signs for a mixed equilibrium.
It saves those values in `rational_output.txt`.

Both scripts print results without assertions.
Neither script reads the original calculations.
After these calculations, a fresh run of the original benchmark supplies `original_benchmark_comparison.txt`.
The review memo is `../../memos/X_C7_check.md`.
