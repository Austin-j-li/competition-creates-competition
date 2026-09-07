# Manuscript checkpoint, 2026-09-05

Assigned scope: finish S4 online appendix alignment and P29 bibliography/cross-references/prose; own only paper/main.md, paper/online_appendix.md, references.bib and manuscript audit logs. Parent owns build/commit. No subagents. Paused after an atomic edit for the user's tmux migration.

Read VM_START_HERE, HANDOFF_SNAPSHOT, CLAUDE, repository map, prior S4 online edit log, saved author decisions, unslop skill, fixing spec editorial/proof/schema/release sections, E2E review substantial excerpts. Full initial combined spec/review read was output-truncated, so relevant sections were read separately. Preserve singular I as author override. No changes to bibliography so far; all 21 existing entries read. No external bibliographic update or new verification claimed.

## Edits just saved

- main introduction corrected an economic wording error: winning incumbent *pays*, does not collect, low challenger's bid.
- main reserve discussion corrected reserve below both challenger values, not every acquisition value (incumbent support includes zero).
- main A7 removed false claim binary payoff formulas agree across p=ell: t_L jumps on low-type exclusion immediately above ell. OA A10 similarly clarifies kernels' equality/admissibility boundaries.
- main A7 corrected false statement C2=0 at both participation events. Weak floor event excludes incumbent; strong ceiling p_H<r_1 has C2=(1-p_H/r_1)e_H/2>0. Numerical C6c already tests proper outcome measures; manuscript was wrong.
- main and OA corrected positive floor 'no price pool' to no pool combining distinct raw posteriors; constant-posterior price atoms remain.
- OA C6 corrected 'probability below acceptance = null set' to a numerical cutoff subject to error budget, not a mathematical null set.
- OA C1 inserted existing renderer table inputs table_matched_price.tex and table_extensions_margins.tex. OA C6 inserted table_reserve_details.tex. These had already been produced but never inserted. Exploratory reserve summary input is not yet added, awaiting validated scope.
- Main reference to Online Appendix Table 1 replaced with stable linked OA C3 section, because new earlier tables change numbering. OA signal table prose now says table below.
- Minor unslop: removed forced 'Three further results', 'genuinely'.

## Open concrete tasks

1. Finish exact C1/C2 schema alignment. C1 existing output schemas match producers. Matched panel renderer writes tables/matched_price.csv for FOUR noise/cost combinations, not just one. Prose still needs add this derived CSV schema and ensure paragraph after column block accurately describes four combinations.
2. C2 source currently COLUMNS = LEGACY_COLUMNS + IDENTITY_COLUMNS + BUDGET_COLUMNS. Source adds correspondence_attempts.csv and mixed_search_attempts.csv; OA omits both and incorrectly says every mixed start lives in mixed_supports.csv. Actual attempts stored in mixed_search_attempts (ATTEMPT_COLUMNS in numerics/mixed_search.py); support rows in mixed_supports. Full per-row error budgets in numerics/error_budget.py. Source currently calls mesh gain off_support_gain_bound; parent alerted rename to off_support_gain_mesh. Wait final C2 owner's schema contract before finalizing.
3. OA C2 overstates mixed domain: actual H mixes over correctly signed mesh; L restricted pure -v. Numerical check of monotonicity does not prove global low-type concavity; characterize as restricted diagnostic domain, never full mixed search. Source also has repeated meshes 0.05/0.025, three starts, default max_iter=120, stall detection + support solve; actual attempt records retain details. Avoid claim bidirectional warm starts/extra certificates if unimplemented.
4. OA C6 overstates actual sweep: says finite support mixed candidates, warm starts both directions, refinements 0.002. Parent alerted and C6 owner to report final actual method/coverage. Source node solver claims only convenient pricing family; no arbitrary cutoff search. Need align after full/fallback decision. C6 now includes BUDGET_COLUMNS too; OA schema needs shared budget columns reference.
5. Add exploratory table input only if sweep validated; otherwise follow parent fallback removal ledger. Main Figure2 caption and two following numerical-branch paragraphs likewise depend on final scope. Parent warned.
6. P29: mechanically validate all citation keys, labels, equation tags/references, placeholder keys. Generate final label_map with old-to-new appendix section labels/equations from audit/peer_polish/label_map_baseline.md. Current main A.1..A.57 replaces baseline A.1..A.40; OA new OA.53 shifts old53..55 by1, inserts OA57..64, old56..70 shift9. Preserve established proposition identities A1..A9 and add A10/OA3.
7. Consider stable equation/proposition labels: source uses manual numeric references and tags, no raw TeX labels. Existing header anchors stable. At minimum map/check every current reference, fix obvious cross-doc numbering references, avoid risky blanket math rewrites. Final rendered checks parent does.
8. OA E1 VM commands must set OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1, C2/C6 workers8, C6c explicit workers. Remove unverified about-one-hour timings. Clarify source_and_replication directory pointers and final release/reproduce implementation once parent finalizes.
9. Full prose pass remaining. Scientific proof chain read main A2-A7, OA relevant proof extensions, no core theorem contradiction found. Equality/tie and no-entry pool corrections above are manuscript defects, not counterexamples.
10. Write manuscript audit/ref log with exact evidence and known limitations; parent builds/commits. No tests/audits have yet been run after just-saved edits.

Useful files: numerics/render/tables.py matched panel around lines245-308, online_table creates real float with stable label; new inputs will shift OA table numbers. Main line336 old OA Table1 reference now section link. bibliography has 21 keys, all existing versions preserved. Parent has been sent found defect list and schema concerns.
