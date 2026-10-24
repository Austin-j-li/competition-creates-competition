# Exact schedules for C9

Run this command from the repository root:

```text
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C9_unequal_mixing/certificates.py
```

The program evaluates eleven schedules with exact rational arithmetic.
It prints every investor action payoff and each preparation margin.
It holds the candidate price and entry schedules fixed for each unilateral action.
It also derives the challenger posterior from the groups of equal prices.

The first nine schedules use the benchmark auction values and noise probabilities $(2/5,2/5,1/5)$.
At each of three strengths, the program evaluates no trade and both informative branches.
The tenth schedule uses presence probability $49/50$.
The last schedule exhibits the equilibrium that fills a preparation gap.

The files are:

- `summary.csv`: parameters, purchase probabilities, entry, ownership, and action payoffs.
- `flows.csv`: conditional flow probabilities, beliefs, entry, prices, residuals, and preparation margins.
- `run.txt`: the saved console output from the final run.
- `receipt.json`: source commit, command, date, sizes, and hashes.

Every number in the CSV files is an integer or an exact fraction.
The program does not convert decimal strings through binary floats.
The memo gives separate proofs of general existence and the entire upward branch.
