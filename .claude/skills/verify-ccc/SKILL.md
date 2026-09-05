---
name: verify-ccc
description: Run the numerical verification gate for this repository (acceptance checks, output hashes, registry, placeholder substitution, figures, tables, LaTeX build) before any commit or completion claim.
---

# verify-ccc

Run from the repository root with the project virtual environment.

1. Gate the completed exercises (fast, about two minutes):
   `.venv/bin/python numerics/verify.py`
   Add `--stage c1 c2 ...` to restrict, `--rerun` to re-execute the cheap exercises first, `--final` to also require every placeholder resolved and run the strict substitution.
2. Render figures and tables: `.venv/bin/python numerics/render/render_all.py`.
3. Build the PDFs: `.venv/bin/python numerics/render/latex.py` (needs pandoc and latexmk).
4. Any FAIL line means stop: report it, never loosen a tolerance or edit an output file by hand. Output files are hash-checked against `numerics/manifests/*.json`; regenerate them by rerunning the exercise instead.

The long exercises (C.2 and C.6) take about an hour each on 8 cores; run them in the background and gate afterwards.
