# S0 setup — 25 October 2026

The work branch `theory-upgrade` starts from `487619f35033ef6774601a5655f2ee26ab83aa23`. The side-branch commit `80804f0` is not an ancestor. The study, solver reports, referee reports and archived computations were copied into role-based paths. The latest PLAN.md includes the existing-project workflow and no scheduled routine. The lens plans are supporting historical proposals; PLAN.md overrides their earlier execution arrangements.

The main checkout's manuscript was not changed. The branch's `slot/manuscript/` was compared recursively with the existing Overleaf working copy at `69c25f4704f30d9b999856d85d3dbafa1e0bee41`. The only difference is line 1 of `sections/02_model.tex`: the branch begins with the section command; the working copy prefixes it with `ty`. The full recursive comparison excluded only Git metadata and found no other differences. Its exact output is retained in the local setup report. No manuscript synchronization or delivery push was performed.

The dependency installer is `plan/cloud_setup.sh` at the repository root. It is supplied for the author to append to the existing environment's setup; existing settings and variables are left unchanged. The figure program still has its original machine-specific Fira font path. Resolving that path belongs to S2. No research computation or proof revision was performed during setup.

The nine decisions remain unanswered. The next permitted work is the document build and numbers-pipeline run recorded in `S0_smoke.md`, followed by the remaining S0 baseline and the S1 decision gate. Build success has not yet been established by this setup record.
