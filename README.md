# Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders

Research repository for the paper and its numerical layer.

- `paper/main.md`: manuscript with paper appendix (Markdown with LaTeX math; `[[name]]` placeholders are filled from validated numerical output).
- `paper/online_appendix.md`: online appendix (full proofs, computer-assisted certificate method, numerical exercise contract in section C, empirical pilot design in D, reproducibility in E).
- `paper/quantity_manifest.csv`: specification of every placeholder (name, definition, exercise, source file and row selector, display format). Inputs carry values; derived rows are filled only by validated output.
- `paper/main_filled.md`, `paper/online_appendix_filled.md`: generated copies with placeholders substituted from `numerics/quantity_registry.csv`.
- `numerics/`: the numerical layer (Online Appendix C, layered per E.3). Exercise scripts live in `numerics/exercises/`, renderers in `numerics/render/`, run manifests in `numerics/manifests/`.
- `tables/`, `figures/`, `figures_data/`: generated CSV outputs, LaTeX tables, and vector figures.
- `verification/`: the collaborator's distributed node checks and interval certificates (E.2), kept as delivered.

## Working across machines

`main` is the shared branch for the current paper, supervisor handout, and teaching course.
Before changing machines, commit the intended files and push them. On the other laptop,
run these commands from your existing checkout:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
```

Commit or stash any local edits before switching branches. A new clone checks out `main`.
Install the local environment using `replication/README.md`; virtual environments, caches,
and private Claude settings stay on each machine. Shared Claude instructions, skills, and
preview configuration are tracked.

The supervisor brief is at https://austinjunyuli.github.io/competition-creates-competition/.
Its sources and build instructions are in `handout/README.md`; the course is in `learn/`.
The current delivery PDFs are in `peer_release/` and the site copies in `docs/`.
Publishing the website still requires updating `gh-pages` after building the handout.

Both VM checkouts were reconciled on 2026-09-07. Their previous working states, including
historical source archives, are preserved as Git stashes:

| VM checkout | Backup stash commit |
|---|---|
| `/home/uctpiaj/work/competition-creates-competition` | `8531dae98d683d794335ad2db29ce493f93ea383` |
| `/home/uctpiaj/work/Projects/competition-creates-competition` | `b04462a0f4f8c6b803b6d765dae749038d19f3e8` |

These backups remain on the VM. Unique review inputs and audit records are tracked here;
the archived source packages duplicate earlier revisions. Inspect a backup with
`git stash show --include-untracked --stat <commit>` in its VM checkout. Do not apply the
old state over current work without reviewing the differences.

## Running

```bash
python3 -m venv .venv && .venv/bin/pip install numpy scipy mpmath matplotlib
.venv/bin/python numerics/exercises/c1_baseline.py        # C.1
.venv/bin/python numerics/exercises/c2_correspondence.py  # C.2 (about an hour on 8 cores)
.venv/bin/python numerics/exercises/c3_signals.py         # C.3
.venv/bin/python numerics/exercises/c4_moderate.py        # C.4
.venv/bin/python numerics/exercises/c5_noise.py           # C.5
.venv/bin/python numerics/exercises/c6_reserve.py         # C.6 (about an hour on 8 cores)
.venv/bin/python numerics/exercises/c7_bargaining.py      # C.7
.venv/bin/python numerics/check_registry.py               # precision and import-order regression
.venv/bin/python numerics/registry.py                     # C.8 registry
.venv/bin/python numerics/substitute.py                   # filled manuscripts (fails on an open required placeholder)
.venv/bin/python numerics/render/render_all.py            # Figures 1-4, Tables 1-4, appendix signal grid
.venv/bin/python numerics/render/latex.py                 # LaTeX conversion and PDFs (needs pandoc, latexmk)
.venv/bin/python numerics/verify.py --final               # the gate: acceptance checks, hashes, registry, substitution
```

`numerics/verify.py` exits nonzero on any breached acceptance bound, any output file that differs from its manifest hash, or any unresolved required placeholder.

To rebuild the paper from the validated exercise outputs, start with `numerics/check_registry.py`; no new equilibrium search is needed. Registry arithmetic uses a local 60-digit decimal context. The final gate checks the registry and presentation manifests as well as the numerical exercises.
