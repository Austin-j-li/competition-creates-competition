---
name: numerics-build-status
description: "State of the numerical layer build (2026-09-05): what runs, how long, run-time gotchas, and what the collaborator delivered"
metadata: 
  node_type: memory
  type: project
  originSessionId: 06d99d85-bea9-4c4f-b9d2-0dbbd46f50cc
  modified: 2026-09-05T14:18:29.591Z
---

On 2026-09-05 the execution session built `numerics/` (layers per OA E.3) and ran C.1 to C.7. The collaborator's `verification/` directory and `references.bib` arrived mid-session and were committed; `numerics/certificates.py` is a port of `verification/certify_asymmetric.py` with predicates recorded instead of asserted, and it reproduces the three interval certificates bit-for-bit.

**Why:** Future sessions should not re-derive the run economics or re-debug the same traps.

**How to apply:**
- Run everything from `.venv` (Python 3.12.13, NumPy 2.5.2, SciPy 1.18.1, mpmath 1.4.1). Gate before commits: `.venv/bin/python numerics/verify.py --stage ...` or `--final`.
- C.2 (`numerics/exercises/c2_correspondence.py`) and C.6 (`c6_reserve.py`) use 8 worker processes and take roughly an hour each; a node with full searches costs about 40 s. Kill orphaned `Python -c from` workers if a run is aborted.
- Registry selectors without an `experiment` field resolve to `experiment=feedback` in `tables/equilibrium_controls.csv` (C.8 convention adopted here); `tau=benchmark strong threshold` maps to `tau_label=benchmark` in `figures_data/posterior_tails.csv`.
- A Ψ sign change at v≈0.21 (r=1.55) is a discontinuity where the cutoff hits the plateau boundary τ=M_v, not a root; it is recorded as branch `asymmetric_discontinuity`.
- On 2026-09-05 the author had the manuscript rewritten (single-author voice, three propositions, Appendix A results A.1 to A.9). `paper/main.md` is now the rewritten source; figures and tables are placed by `<!-- FIGURE N: path -->` / `<!-- TABLE N: path -->` markers followed by a `> **Figure N.** caption` blockquote that `numerics/render/latex.py` parses. The assembler used for the rewrite lives only in the session scratchpad; equation tags are sequential in order of appearance, conditions keep labels (A1) to (A3).
- Related: [[astra-ccc-proposal]], [[working-style-feedback]].
