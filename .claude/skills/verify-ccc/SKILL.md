---
name: verify-ccc
description: "Verify affected numerical exercises and derived artifacts, or run the complete research release gate."
---

# verify-ccc

## Verification scope

For a focused edit, run checks that cover the changed behavior. Documentation-only work and read-only assessments need relevant static/source checks, not unrelated full pipeline runs. Use all applicable gates for pipeline-affecting changes, release readiness, or an explicitly requested full verification; report skipped gates and do not label a scoped check as a full PASS.

Keep live/model-backed extraction opt-in. A verification-only request reports failures without editing. When implementation is authorized, the caller fixes failures caused by its changes and reruns the affected checks; unrelated failures or missing access must be reported with evidence. Preserve existing research tolerances, provenance, immutable rulings, and release gates.

Run from the repository root with the project virtual environment. The commands below use
the Unix interpreter path; on Windows use `.venv/Scripts/python.exe`.

1. Gate the completed exercises (fast, about two minutes):
   `.venv/bin/python numerics/verify.py`
   Add `--stage c1 c2 ...` to restrict, `--rerun` to re-execute the cheap exercises first, `--final` to also require every placeholder resolved and run the strict substitution.
2. Render figures and tables: `.venv/bin/python numerics/render/render_all.py`.
3. Build the PDFs: `.venv/bin/python numerics/render/latex.py` (needs pandoc and latexmk).
4. Any FAIL line means the gate failed: report it and handle repairs according to the scope above. Never loosen a tolerance or edit an output file by hand. Output files are hash-checked against `numerics/manifests/*.json`; regenerate them by rerunning the exercise instead.

The long exercises (C.2 and C.6) take about an hour each on 8 cores; run them in the background and gate afterwards.
