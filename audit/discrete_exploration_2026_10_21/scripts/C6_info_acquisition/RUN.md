# C6 reproduction record

Status: analytical propositions with high-precision numerical diagnostics.

Source: manuscript commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
The source files are `main.tex` and `online_appendix.tex`.
The literature record is the local `LIT_extracts.md`, Section A3.

Run date, UTC: 2026-10-21T18:00:25.133688+00:00
Runtime version: 3.12.13
Arithmetic package version: 1.4.1
Precision: 90 decimal places; auction inputs use exact fractions.
Run exit code: 0. The calculation completed.

Common inputs: $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_L=0$, $k=1/50$, and $\pi=1/2$.
Discrete-Laplace noise uses $b=2$ and $a=e^{-1/2}$.
The main feedback cases use $c_H=5$; the original-cost cases use $c_H=6$.
The equal-noise cases use $r\in\{1.2,3,3.6,8.5\}$.
The main reversal uses $r\in\{1.2,3,4.2\}$ and $\kappa=0.02$.
The cost correspondence uses $r=3$ and $\kappa\in\{0.02,0.03,0.05,0.09,0.094,0.095\}$.
The strength comparison uses $\kappa=0.06$ and $r\in\{3.98,3.99,4,4.2\}$.
The equal-noise threshold and welfare case uses $\kappa=0.01$.
The original-cost interior case uses $r=3$ and $\kappa=0.03$.

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C6_info_acquisition/calculations.py > audit/discrete_exploration_2026_10_21/scripts/C6_info_acquisition/results.txt
```

One process uses one CPU slot. The observed run took less than one second.
The program prints the declared benchmark cases and the acquisition correspondence.
It also prints the quadratic roots and direct flow sums.
The direct sums use 801 noise values and print the omitted-tail bound.
The closed forms cover the full support.

The branch roots and quadratic roots agree to at least 88 decimal places.
The high-class flow sums agree with the closed form within the printed tail bound.
The low-class purchase payoff is negative at each displayed schedule.
No test suite ran. No assertions appear in the program.
The numerical output is not an interval certificate.

| File | Bytes | SHA-256 |
|---|---:|---|
| `audit/discrete_exploration_2026_10_21/scripts/C6_info_acquisition/calculations.py` | 10022 | `f84b11e869e8c074c3fa4a6a88f384e06ef59286115b4729716cf1047e56fff0` |
| `audit/discrete_exploration_2026_10_21/scripts/C6_info_acquisition/results.txt` | 8755 | `9cdb5e128569a5d17240fc22d0fb0cba38219359a7f11c1db34d1c33396bc898` |
| `audit/discrete_exploration_2026_10_21/memos/C6_info_acquisition.md` | 31222 | `d3eeb9d0615259b001ee85b27bd8e2e6b834ecdd153e8dc53edb2c881e5233c7` |
