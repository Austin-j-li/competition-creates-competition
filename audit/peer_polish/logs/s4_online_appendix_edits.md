# S4/S5 online-appendix edits (P20, P21, P28, P30; 13.5, 14.3 online panel, 14.5 online summary, 15.3, 16.3)

File edited: `paper/online_appendix.md` only. Branch `peer-circulation-fix` on top of `84e6b00`.
Not committed. Word count 16.6k to 19.7k. `pandoc paper/online_appendix.md -t plain` parses
(only the pre-existing plain-text math warnings). No `we`/`our`, no mention of reviewers,
spec, or assistants. Voice is first-person singular throughout.

## Placeholders

Before and after: `seed_mpmath_version`, `seed_numpy_version`, `seed_python_version`,
`seed_scipy_version` (all in E.1). The old C.8 tables printed declared values as literal text,
not as `[[placeholders]]`, so condensing C.8 removed no placeholder. **Removed: none. Added:
none.** The manifest needs no `required_in_online` change. C.8 now names the `pool_*` keys
that the paper appendix introduces (`pool_reserve`, `pool_posterior_cutoff_{low,high}`,
`pool_entry_cutoff_{low,high}`, `pool_revenue_cutoff_{low,high}`); they are not printed in
the OA.

## Anchors

Kept: every existing `{#oa-...}`. Added: `{#oa-a-pools}` (A.11), `{#oa-c-price-pools}`
(C.6b), `{#oa-c-reserve-events}` (C.6c). A.10 keeps its number and anchor because
`paper/main.md` A.7 cites "Online Appendix A.10" for the regularity conditions and cites the
new subsection by title.

## Equation tag renumbering (OA.n)

- OA.1 to OA.52: unchanged.
- New OA.53: continuation object in A.10. Old OA.53, OA.54, OA.55 become OA.54, OA.55, OA.56.
- New OA.57 to OA.64: A.11 (densities and posterior; price family; CDF and survival; pooled
  posterior; conditional pricing; residuals; rational bounds; output quantities).
- Old OA.56 to OA.70 become OA.65 to OA.79 (shift +9). In particular the pooled-posterior
  formula in C.6, old OA.70, is now OA.79; old OA.68 (margins) is OA.77; old OA.61/OA.64
  (certificate predicates) are OA.70/OA.73.
- Tag sequence verified contiguous 1..79. `grep "OA\.[0-9]" paper/main.md` returns nothing,
  and `paper/drafts/appendix_A_revised.md` likewise, so no cross-document tag reference needs
  updating.

## Section-by-section

- **A.4.** "unique trading and entry outcome" -> "unique trading and on-path preparation
  outcome" (two places).
- **A.5.** Proposition A.3 paragraph now states cost independence of $(S,\Theta)$ and that the
  signal experiment and cost law are held fixed as strength varies; says why $\Pr(H\mid S)$
  is then the right object and that the correlated-cost version is not claimed (13.4).
- **A.9.** After (OA.46): the contribution statement is in conditional expectation given
  price information and cost; a realized low-value preparation need not be a positive realized
  net gain (13.3).
- **A.10.** New display (OA.53) for the continuation object $\sigma\in\mathcal E(p,r)$;
  paragraph says the C.6 convenient construction is one admissible member, not the only one,
  and points to A.11.
- **A.11 (new).** "Price pooling when preparation can vanish". Inputs block (exact declared
  values), auction objects on the expanded domain, densities and $\mu_X$, the $P_c$ family,
  explicit CDF-versus-survival notation, pooled posterior from the full preimage, buyer
  validation at zero price including the assertion that flows in $(-\log 2,0)$ under $c=0$ are
  not individually observed, buyer validation at positive prices, conditional pricing on both
  regions, residuals, the rational global bound $J_c>7/32$, $U'>143/1600$, **Proposition OA.3
  (price pooling at fixed orders; analytical)** consistent with Proposition A.10 in the paper
  appendix, the non-uniqueness and non-novelty statements (citing @DowGoldsteinGuembel2017
  Lemma 1), closed-form outputs, the 17-cutoff grid, and the four negative controls with the
  reason each fails. No research numbers typed; endpoint values are routed to the `pool_*`
  registry keys.
- **B.** Unchanged (no formal statements without a status; Lemmas OA.1/OA.2 already carry
  "analytical").
- **C.0.** New declaration block "continuation, event, and outcome controls"
  (`pool_reserve = 7`, cutoff grid, negative controls, `pricing_family_coverage`,
  `exhaustive_pricing_search = false`, identity tolerances 1e-6/1e-8, event arithmetic 50
  digits, sign resolution 1e-40, offsets, tie rule, outcome measures, minimum mixed starts 3);
  price-atom validation rule (7.4); exact-event evaluation with the symbolic tie rule; outcome
  measures E, A, S, C2, O_H with the identity $S=\Pr(R\ge p)+A-C_2$ and bounds; four separate
  error budgets with their columns and the refinement rule (S1-C).
- **C.1.** New "Matched-price panel (online)" paragraph: columns `environment,
  mean_financial_price, seller_revenue, external_dividend, preparation_probability,
  high_value_ownership_probability, net_acquisition_surplus`, the $D_0$ identities, the
  invariance requirements, and the forbidden fix (dividend never in seller revenue).
  Assembled by the renderer from `tables/equilibrium_controls.csv` and
  `numerics/feedback_comparisons.csv`. **The parent must add the rendered table input once
  the renderer produces it; no `\input{}` was added.**
- **C.2.** New paragraphs "Mixed-search attempt records" (>= 3 starts, convergence-based
  budget, open rows written to `correspondence.csv`, per-start columns) and "Continuation
  identity and deduplication" (identity by complete strategies plus price information,
  normalized strength labels, tangency roots merged against bracketed roots,
  `multiplicity_found` after merge). Output schemas extended: `correspondence.csv` gains
  `quadrature_error, posterior_inversion_error, entry_independent_error, candidate_id,
  continuation_id, duplicate_of`; `mixed_supports.csv` gains `init_id, off_support_gain_mesh
  (renamed from off_support_gain_bound), simplex_residual, iterations, stop_reason, final_gap,
  quadrature_error`. Written as the method; search outcomes described only as what the
  records will show. **The C.2 code must be brought in line with these columns (S3-01,
  S3-03, S3-05, S3-06) before the rerun.**
- **C.6.** Rewritten: complete continuations required (OA.53), actual pooled beliefs (OA.79),
  raw-posterior-in-pool rejected as non-measurable, `pricing_family_coverage` /
  `exhaustive_pricing_search` per row, regime classification, event grid (0, ell, r, h,
  ell+-eps_V, h+-eps_V, declared alternatives, p_L, p_H, offsets 1e-4/1e-6/1e-8), identity and
  deduplication rules of 7.3, four search outcomes, the online summary heading "highest revenue
  among continuations found" with ledger-computed counts, full continuation schema (16.1) as
  implemented in `numerics/continuations.py` `SCHEMA_COLUMNS` plus the legacy and
  classification columns of `c6_reserve.py`, range schema, and a data dictionary.
- **C.6b (new).** Price-pool regression: inputs, method as implemented in
  `c6b_price_pools.py`, acceptance (family validated, monotone decrease, rational bounds,
  identity checks, negative controls fail with the named breach), output schema of
  `numerics/price_pool_regression.csv`.
- **C.6c (new).** Exact reserve events: inputs (event grid, sampled reserve 6.280), method and
  acceptance as implemented in `c6c_reserve_events.py` (floor event, ceiling event, sampled
  reserve outcomes, union identity, bounds), outputs.
- **C.8.** Replaced the long printed registry with "Quantity definitions and provenance":
  rules, units and rounding, a family table (keys, exercise, source file, units), shared
  definitions, production order, pointer to `replication/quantity_dictionary.md` and
  `numerics/quantity_registry.csv`. All display-rule names and status rules retained.
- **D.** Untouched; already in design (future) tense with no sample or identification claim.
- **E.1.** Actual producer commands c1..c7, c6b, c6c with outputs and run times; presentation
  sequence check_registry, registry, substitute, render_all, latex, verify --final; `make
  peer-release` / `make peer-reproduce` described as the release entry points; pointer to
  `replication/README.md`; `verification/` described as the independent seed not read by the
  build.
- **E.3.** Module-by-module description of the implemented layers; CSV writer conventions;
  verify.py failure conditions; retained records (negative controls, duplicate starts).

## Open items for the parent

1. Create the Makefile targets `peer-release` and `peer-reproduce` and `replication/README.md`
   (draft in `replication_readme_draft.md`) and `replication/quantity_dictionary.md`.
2. Add the matched-price panel renderer and its `\input{}` in C.1.
3. Implement the C.2 column changes listed above before rerunning C.2.
4. Add the `pool_*` keys to `paper/quantity_manifest.csv` (see `s4_appendix_edits.md`).
5. Unslop pass applied to all new prose; no em dashes, no `we`.
