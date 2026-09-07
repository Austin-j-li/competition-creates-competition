# Fork: the endogenous insider

A fork of the benchmark model in `paper/main.md`, recorded on 2026-09-07 after a supervisory meeting. The stochastic preparation cost is replaced by one deterministic cost, which removes the participation floor. Whether the investor's knowledge of the challenger's value is information about the target's stock is then decided in equilibrium.

This directory is not part of the manuscript, its numerical contract, or its release gate. Nothing here is a validated exercise in the sense of Online Appendix C; every live equilibrium reported is a numerical diagnostic.

## Files

- `mechanism.md`: the model, equilibrium definition, results F.1 to F.5 with proofs, the taxonomy of what "information" means here, the selection discussion, and the numerical illustration.
- `solve.py`: solver. Benchmark primitives with `rho = 0` and `c = 6`. Writes `branches.csv`, `cutoff_family.csv`, `thresholds.csv`. Solves only.
- `render.py`: renders `entry_fork.pdf` from the three CSVs and the paper's validated `numerics/correspondence.csv`. Renders only.
- `solve.log`: the solver's console output from the recorded run.

## Run

```bash
python3 fork/endogenous_insider/solve.py
```

```bash
python3 fork/endogenous_insider/render.py
```

The solver takes about a minute with NumPy. The renderer imports the shared figure style from `numerics/render/style.py`.
