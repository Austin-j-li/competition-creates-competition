# Equilibrium set of the endogenous-insider fork

Research track on the fork's open items 1 and 2: certify $J(3)$, find the exact existence region of the full-order equilibrium, locate the lower edge of the live branch, and search outside the cutoff family. The results and proofs are in `note.md`. Nothing here is part of the manuscript or its release gate.

## Files

Code. Every function is pure and typed. Solvers write CSV only. The renderer never solves.

- `core.py`: model layer. Payoffs (4), posteriors (7), residual integrals (A.4) by piecewise Gauss–Legendre with exact tails, best responses on $[-1,1]$, and the closed forms (ES.1) to (ES.4).
- `certify.py`: outward interval arithmetic (mpmath.iv, 40 digits) on exact decimal inputs. Writes `certificates.csv`.
- `solve_branch.py`: full-order region, refined live branch, the region below the edge, and a scan of pure profiles. Writes `full_order_region.csv`, `live_branch.csv`, `below_edge.csv`, `pure_scan.csv`.
- `solve_outside.py`: entry sets with holes, entry ranges, a scan of mixed profiles, and the identity check. Writes `holes_r3.csv`, `holes_range.csv`, `mixed_scan.csv`, `identity_check.csv`.
- `solve_zrange.py`: supported low-type orders, least-entry sets, the entry band, and the tie branch. Writes `z_range.csv`, `least_entry.csv`, `entry_band.csv`, `tie_branch.csv`.
- `render.py`: reads the CSVs and writes `equilibrium_set.pdf` and `tables.md`.

Status. Rows of `certificates.csv` are computer-assisted, except one row marked analytical. Every other CSV row is a numerical diagnostic.

## Run

From the repository root, in this order (about five minutes in total):

```bash
cd fork/endogenous_insider/research/equilibrium_set
python3 certify.py
python3 solve_branch.py
python3 solve_outside.py
python3 solve_zrange.py
python3 render.py
```

The renderer imports the shared figure style from `numerics/render/style.py`.

## Main numbers (benchmark $h=10$, $\ell=1$, $p=0.5$, $b=2$, $k=0.02$, $c=6$)

- $J(3)\in[0.0955028924240038,\,0.0955028924240039]$. $(1-1/b)J(3)\ge m/6>1/24>k$ holds analytically.
- The minimal-pool full-order equilibrium exists exactly on $[r_J,r_C]$, with $r_J=2.0155164410601$ and $r_C=3.5926585$.
- Live equilibria with $q_H=1$ exist exactly on $[r_e,r_C]$, with $r_e=1.6585908245511$. At $r_e$ the entry set is the top price atom, and entry jumps from $0.384$ to $0$.
