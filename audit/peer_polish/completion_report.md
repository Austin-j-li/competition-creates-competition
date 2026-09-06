# Peer-circulation revision

Completed on 2026-09-06. The audited working-paper package is ready for peer circulation. All 33 release tests passed, with zero failed, zero open and zero not-in-release tests; exploratory search limitations remain recorded separately.

## Scope and provenance

The retained scope is the audited working paper, including the C.2 correspondence and C.6 reserve diagnostics. No core-only fallback was applied. The empirical section remains a research design. The revision began at `dfea7f9a01c46a92f1d2c678bfe775217ccaf51d` on branch `peer-circulation-fix`. The validated source revision is `6aac3caacb7a0fc819795a423d4fb7363eb58371` (663 revision files). Final audit/package records are a separate delivery commit. Exact file hashes are recorded in `replication/run_manifest.json`; command records are in `replication/build_manifest.json`.

The editable manuscripts are `paper/main.md` and `paper/online_appendix.md`; the bibliography is `references.bib`. Changes cover these manuscripts, the continuation and search validation layers, registry and exhibit rendering, numerical outputs and manifests, release checks, and the audit evidence. The issue-level source/output map is `issue_ledger.csv`; `source_output_map.csv` records the build graph and `claim_ledger.csv` records retained claims and their proof locations. Foreign handout, `docs/`, and `learn/` work was preserved.

## Reader-facing changes

The abstract and introduction now lead with the economic question and distinguish trading-outcome uniqueness from uniqueness of every off-path price rule. The model states its reserve, preparation, information and trading assumptions explicitly. The paper appendix groups definitions, results and proof steps, and both manuscripts describe complete price-and-trading continuations, rational price atoms and exact reserve ties.

The main control table removes redundant dividend rows. The online appendix retains the matched-price comparison, full extension margins and all 25 signal-accuracy pairs. The main reserve table keeps supported alternatives; the online appendix contains detailed outcomes, finite-search ranges and exact events. The full scalar definitions remain in `replication/quantity_dictionary.md` and the registry CSV. Figure 2 distinguishes analytical regions, certificates, found branches, mixed diagnostics and unresolved search coverage. The logistic and bargaining endpoints are corrected.

The author's saved decision to use first-person singular "I" overrides P21's plural-voice instruction. All 21 bibliography entries were preserved; citation keys and relocated references resolve. The abstract has 137 words.

## Executed validation

- Fresh core producers C.1, C.3, C.4, C.5 and C.7 passed. C.1, C.3 and C.4 passed again after cutoff-only serialization changes.
- The independent implementation completed 5,870 records: 5,802 passes, 68 information records, zero failures. It includes 364 global/refined state scans. Current-output bindings passed 5,638 checks against ten preserved input snapshots, with declared identity and serialization differences recorded explicitly.
- The supplied certificate seed ran with assertions enabled and unchanged source bytes. The delivery certificate audit passed 186 checks, including 30 checks of outward-rounded registry and manuscript displays. The promised separate `reference_oracles.py` companion package was not supplied and was not run.
- C.6b passed its seven gates for 17 valid fixed-order price pools, invalid controls, observed-price preparation, complete identity and analytical deviation bounds. Exact reserve regressions T21–T23 passed on 257 nodes. The repaired continuation adapter passed its six tests and the eight original S2 regressions.
- The registry contains 128 quantities and zero unresolved required values. Twelve fresh-process precision/import-order combinations agree. The presentation tests and separate table layout checks passed.
- All eleven isolated corruption cases were rejected by the release boundary, after checking that each uncorrupted copied baseline passed.

The final full suite passes 47 tests, including the new statement-layout regression. Fresh reproduction reran all nine raw producers successfully and matched all 29 compared CSVs and both substantive manuscript texts. C.2 took 824.736 seconds and C.6 took 763.615 seconds on 20 workers each. After the final table-reference correction, both working and isolated presentation builds passed again. The final comparison has zero mismatches, and both copies have identical hashes for all 61 source files. All 129 PDF pages pass individual visual review: 72 in the main paper and 57 in the online appendix. No overflows, unresolved references, missing characters or unembedded fonts remain. `test_catalogue.csv` separately records T01–T33; unresolved exploratory coverage is not counted as a failed release test or as a proof of nonexistence.

## Retained search evidence and limits

C.2 evaluated 592 nodes with 6,000 recorded attempts, 1,841 distinct rows and 4,159 duplicate attempts. Eighty nodes have multiple found accepted continuations. Forty open search rows and 41 unresolved mixed-search attempts remain visible. All 7,022 accepted state-support groups passed the recorded support and deviation checks. One mixed candidate at the pooling boundary is retained as a numerical diagnostic; its finite-support and tested-deviation residuals do not establish exact mixed-equilibrium existence or close its between-grid bound.

C.6 evaluated 1,664 nodes and 11,414 final-pass candidate attempts: 9,607 raw acceptances, 1,323 rejections, 484 unresolved attempts and 7,344 duplicates. It retains 503 open search scopes. All attempted nodes have an accepted continuation; 599 have two distinct accepted continuations. C.6c records 634 attempts, 447 raw acceptances, 187 rejections, 190 duplicates and seven open searches. The eight fixed reserve comparisons pass. Maximum payoff-oracle disagreement across C.6 is approximately 2.13e-14.

The broad reserve search covers its declared pricing family and initializations, not arbitrary rational pools. Found revenue extrema are not seller optima. Finite-grid global deviations remain numerical diagnostics unless a separate analytical or interval argument supplies the stated bound. No acceptance tolerance or scientific grid was loosened for the VM.

## Discrepancies and repaired attempts

The interrupted C.2 rewrite initially failed regressions for nonfinite error budgets and false mixed-search convergence. Quick/full audits also exposed near-endpoint and near-interior numerical copies of the same economic continuation. Exact endpoint proposals and root polishing now rebuild and revalidate the schedule. The original outputs, 23-node C.2 revalidation and 28 preceding C.6 identity records remain in the audit archive. Fresh producers contain the same repairs used for bounded replay.

The first full C.6 sweep was interrupted for the endpoint repair, with its ledger preserved. A separate 60-second profiling probe timed out; the final full sweep completed those nodes. Terminal profile rejection is now recorded separately from an open search. `logs/c6_audit_vm.md` and `logs/s3_c2_revision.md` identify the earlier attempts and final counts.

An initial current-input binding check was too broad for an unused C.2 declaration rename. The final checker records the four declaration blocks and nine registry values used by its independent implementation; all original CSV quantities agree. Its earlier failure log is preserved. Cutoff infinities are now explicit `unattainable`/`always` tags; ordinary nonfinite numerical fields still fail validation.

The first complete test run reported 45 passes and one negative-test diagnostic failure: removing a required key was rejected through a dependent registry quantity. The gate now reports the missing required key first, and all eleven corruption cases pass. The failed log remains under `raw_failures/`. Preview typesetting exposed a fragile inline-code wrapper and several overflowing displays/table columns; the wrapper was removed and the affected expressions and printed registry were reformatted without removing definitions. Page-image review then found literal reference tildes and orphaned headings before propositions. References now use nonbreaking spaces and the statement-space rule includes adjacent headings. Input-declaration labels are kept with their code blocks. Six landscape-page bounding-box warnings were rotation-coordinate artifacts; the tables were fully visible in the inspected images, and the helper now accounts for page rotation. Its new regression first caught a double insertion at a regex boundary; after correction both release-build regressions pass. The final presentation-only sources were copied into the still-running isolated reproduction before its build, with hashes recorded in `reproduction_layout_refresh.json`; no numerical producer or declaration changed. A table note still cited the old margin-equation number OA.68; it now uses the manuscript equation label for OA.77. The unchanged fresh numerical outputs were rebuilt through the final presentation gate and compared again; the first successful reproduction remains preserved in `reproduction_before_table_reference.json`.

## Reproduction and delivery

The VM has 64 virtual CPUs and 125 GiB RAM. Broad C.2 and C.6 jobs use 20 workers each; event and independent jobs use eight. Each worker uses one BLAS/OpenMP/MKL/NumExpr thread. Python and package versions are pinned in `replication/requirements.txt`, and TeX/Pandoc requirements are documented in `replication/README.md`.

The executed release commands are `.venv/bin/python replication/release.py --build-only`, `.venv/bin/python replication/release.py --reproduce --workers=20`, and `.venv/bin/python replication/release.py --package-only`; the Make targets invoke the same runner. The build runs manifest/semantic checks, current-input bindings, the full test suite, registry invariance, substitution, exhibit rendering, LaTeX and a final numerical/PDF check. Fresh reproduction reruns every raw producer in an isolated source copy and compares CSV content and substantive manuscript text. Full commands and outcomes are retained in the build and reproduction manifests.

The source archive inventory was checked for missing inputs, source/PDF hash differences, path escapes, secrets, caches, bundled fonts and foreign project material. The archive contains no generated PDFs; its two peer PDFs are delivered separately. `package_inventory.json` lists archived source-file hashes, and `replication/delivery_checksums.json` records the final archive/PDF checksums.

Delivery paths are `peer_release/main.pdf`, `peer_release/online_appendix.pdf`, `peer_release/README.md`, and `source_and_replication.tar.gz`. The separate source archive includes editable sources, exact declarations, tests, dependencies, validated data, certificate evidence, manifests and retained failed/search attempts. Nothing was emailed, published or pushed.

Open research questions are seller optimization over unrestricted continuations, the full equilibrium correspondence, and commitment to reserve or information policies. These are distinct from unresolved release defects.
