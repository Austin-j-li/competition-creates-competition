You are working in /Users/austinli/Projects/competition-creates-competition on branch main.
Read HANDOFF.md, then CLAUDE.md, then paper/online_appendix.md sections C and E, then
paper/quantity_manifest.csv, then paper/main.md.

Build the numerical layer that fills the manuscript's [[name]] placeholders: implement
Online Appendix C in the layered structure of E.3, produce every output file named in C.1
to C.7 with run manifests, generate numerics/quantity_registry.csv per C.8, and write the
substitution step that produces paper/main_filled.md and paper/online_appendix_filled.md,
failing if any required placeholder is unresolved. Then render Figures 1 to 4 and Tables 1
to 4 per E.4. Follow the order in HANDOFF.md; C.6 runs last and in the background.

Hard rules: the acceptance thresholds in C.0 are gates, never loosened; every number in the
paper comes from a validated registry row; open nodes stay open; no branch is chosen for its
shape; the prose in paper/main.md is not edited; commit after each exercise; write
numerics/verify.py as the gate and run it before every commit.

Stop and report after C.1 and C.2 are validated, with the registry status for their keys and
any discrepancy against the cross-check table in HANDOFF.md. Then continue through C.7 and
the substitution. Finish with a summary: which placeholders are filled, which are open and
why, and what the author must supply (references.bib, the collaborator's verification
directory) before the LaTeX build.
