# S4/S5 manuscript and reference audit on the VM

The authoritative edits are in `paper/main.md` and `paper/online_appendix.md`. The bibliography is unchanged. The author-approved singular voice overrides specification P21; no plural author voice was introduced. This record completes the source-level editorial work. Fresh exploratory outputs are aligned; the parent owns final PDF inspection and the release gate.

## Scientific corrections

The prior rewrite contained four inaccurate descriptions; none is a change to the numerical primitives or a counterexample to a retained theorem.

- The introduction said the incumbent collected the low challenger's bid. A winning incumbent pays that bid to the target; the sentence now says so.
- The reserve discussion said the benchmark reserve lay below every acquisition value. It lies below both challenger values; the incumbent support includes zero.
- Paper A.7 said payoff formulas agreed at all support boundaries. At a binary value atom equal to the reserve, the challenger is admissible at zero rent, whereas just above the atom it is excluded. Target proceeds can jump. The paper and online payoff descriptions now preserve this distinction, including at `p = ell`.
- Paper A.7 said neither participation event could produce two admissible bidders. This is true at the weak floor event, which excludes the incumbent, but false at the strong ceiling event below incumbent support. The strong event now gives its positive two-admissible probability from the actual allocation events.

Both appendices now distinguish a no-entry pool combining distinct raw posteriors from a positive-entry price atom on a constant-posterior tail. A positive preparation floor excludes the former, not the latter. The online continuation identity discussion also distinguishes a numerical mass cutoff from a mathematical null set. The price-pool example is an existence example, not a claim that every reserve supports a family of pools.

The central proof review checked the payoff opposition, mixture posterior bound, preparation floor before inversion, fixed candidate schedules under unilateral deviations, necessity and construction in Proposition 2, conditional-cost independence in Proposition A.3, certificate root versus unilateral derivative distinction, logistic inverse, atomless-cost support conditions, signal-conditioned entry and residuals, institution-specific bargaining payment, conditional rather than realized welfare contribution, and full reserve-domain payoff definitions. No core proof contradiction was found in this review. Numerical sign-off comes from the independent and exercise checks, not from this source reading.

## Online method and schema alignment

C.1 now contains the existing matched-price panel and full extension-margin table. Its schema includes the renderer's derived matched-price CSV and distinguishes four noise/cost-law combinations, each with feedback, hidden-price, and matched-dividend environments. C.6 contains the declared-reserve detail table. Main references to the signal table name the stable C.3 section, because adding tables before it changes its display number.

C.2 now describes the actual restricted mixed search: the high type mixes on the declared correctly signed meshes, while the low type uses a pure magnitude. It does not claim to have searched both-type mixing. A numerical monotonicity check does not establish the Stieltjes lemma's global premise. The text records the three initializations, stopping budget, support solve, and revalidation of polished pure profiles. It identifies both the raw correspondence-attempt file and the separate mixed-search-attempt file; the support CSV is not described as the complete start ledger. Mesh payoff gaps are named as estimates, not rigorous bounds. Unexecuted bidirectional warm starts and additional interval certificates are no longer claimed.

C.6 describes its actual nine pure starts and single restricted mixed search with its separate budget. It no longer claims C.2's multiple-start method or bidirectional warm starts. The pricing family remains the convenient zero-entry preimage construction; arbitrary alternative pools are not claimed searched. Its event nodes and one-sided offsets, branch/open/maximizer refinement criterion, and `0.002` reserve refinement are stated. Both C.2 and C.6 reference the complete shared per-row error-budget schema in C.0. Fresh C.6 outputs support the inserted exploratory summary table, whose counts describe the final pass; earlier identity-refinement attempts remain archived. The summary remains a search result within the stated price-rule family, not a seller optimum.

E.1 sets numerical-library threads to one and uses twenty workers for the broad C.2/C.6 exercises and eight for C.6c, matching the final VM runbook. It identifies both C.2 attempt outputs, drops inherited runtime claims, and separates quick diagnostics from the release corpus. The release/reproduce description now matches the implemented entry points, metadata settings, and required visual-inspection record.

## References and prose

Every existing bibliography entry was preserved, including the known working-paper versions. No DOI, manuscript date, author list, title, or current-version claim was added or changed. This audit establishes local key resolution and rendering, not a fresh external bibliography/version verification. Pandoc parsed citations in both authoritative sources without warnings.

Every displayed equation now has a persistent TeX label; local prose references use `eqref`. Formal results have persistent Markdown anchors, and references link to those anchors. Section links use stable section anchors. Main figure/table references use the renderer's existing labels. Cross-document source links retain named section/result references in the separately compiled PDFs. `label_map_final.md` maps all old appendix equations, relocated sections, and unchanged result identities.

The prose pass retained the empirical section and OA D as a design scaffold. It added no sample, causal claim, transaction chronology, or claimed price-learning episode. It removed task-oriented phrasing from the theoretical price-pool subsection and corrected unnecessary qualifiers without changing the model's technical terms.

## Verification evidence

`manuscript_source_audit.json` reports:

- 21 bibliography keys, no duplicate or missing keys; bibliography unchanged.
- Main: 74 unique equation tags/labels, 91 resolved local equation references, 98 distinct placeholders all defined in the manifest.
- Online appendix: 79 unique equation tags/labels, 67 resolved local equation references, 4 defined placeholders.
- No unresolved stable anchor links, plural author voice, or em dashes.
- Abstract below the 150-word ceiling.

Both sources passed independent Pandoc-to-LaTeX citation parsing. These are source checks. Final substitution, data provenance, PDF reference resolution, and page inspection remain the parent's build gate.

## Final corpus and layout alignment

C.2's frozen output retains a numerical-diagnostic mixed candidate at the no-trade existence boundary. The paper states this status and the figure caption identifies its preparation diamond and weighted support triangles. The caption also distinguishes searched-node multiplicity ticks from analytical shading, and the filled expensive-entry equality point from its hollow right-hand limit. `manuscript_c2_claim_checks.json` verifies the retained qualitative branch descriptions directly from the final rows: increasing asymmetric short magnitudes and preparation, coexistence with pooling, symmetric-interior preparation at its floor, and the mixed candidate's boundary location and diagnostic status. No mixed nonexistence claim remains.

`manuscript_schema_audit.json` checks exact column ordering and membership against final CSV headers: correspondence 50 columns, mixed supports 25, mixed attempts 28, matched prices 14, reserve continuations 83, and reserve ranges 18. The C.2 support schema includes candidate, continuation, and parameter foreign keys.

Layout-preview corrections split paper equations A.44 and A.52 and online OA.57 without changing their expressions or labels. The repeated matched-control field list is now ordinary economic prose. C.8 uses a three-column quantity-group table, with full keys and provenance preserved in the distributed dictionary; its mathematical definitions remain. Long file paths use short visible links. The two pure-initialization sets are mathematical sets instead of verbatim code.
