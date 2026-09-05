# S3 source audit: correspondence (C.2) and reserve (C.6) corpus

Read-only audit of the numerical stack behind Figure 2, `numerics/correspondence.csv`,
`numerics/mixed_supports.csv`, Table 4, `numerics/reserve_continuations.csv`, and
`numerics/reserve_ranges.csv`, against spec section 10 (items 10.1.1 to 10.1.10, 10.2, 10.3)
and tests T24 to T26. Branch `peer-circulation-fix`, working tree as of this audit. No file
under `numerics/` was modified by this audit. `numerics/continuations.py` appeared during the
audit from the concurrent price-pool work and is out of scope here; item 4 is assessed on the
committed `validation.py` / `c6_reserve.py` code paths.

Line numbers refer to the files as read during the audit.

## 1. Full-domain auction payoffs (value/reserve equalities, within-band integration)

Verdict: **sound**.

- `numerics/auction.py:51-67` implement OA.50 pointwise. `T_realized` treats `v == p` as
  admissible (challenger pays `p`), `R >= p` as an incumbent bid at the reserve, matching the
  declared `bid_equal_reserve_is_admissible = yes`.
- `kernel_uniform` (`auction.py:71-82`) covers all four orderings `v < p`, `p <= v < r`,
  `p <= r <= v`, `r < p <= v`; I re-derived each closed form and the cases are continuous at
  `v = r` and agree with OA.51. `t_0 = 0` when `p > r` is right (incumbent never bids).
- `payoffs_class_closed_form` (`auction.py:176-207`) splits each value band at `p` and `r` and
  classifies each segment by its midpoint, so a reserve inside a band uses the partially
  excluded kernel on each sub-segment, as C.6 requires. `payoffs_class_formula_OA52` is only
  used inside its validity domain (`c6_reserve.py:42-44`).
- Independent oracle `payoffs_integrated` / `payoffs_class_integrated` (`auction.py:138-173`)
  splits at `p`, `ell`, `h`, and at `v` inside the inner integral. C.6 manifest reports a max
  oracle error of `1.17e-14` over 844 grid nodes and 816 refinement nodes.

## 2. Conditional density and posterior for pure, asymmetric, mixed orders

Verdict: **sound** (one note).

- `OrderProfile.a` (`information.py:47-54`) builds the state-conditional mixture density with
  independent supports and weights per state; `Schedule.mu` (`information.py:109-113`) forms
  the posterior from these densities. For `(1,-v)` this reproduces OA.56.
- Note: the fundamental prior `1/2` is hard-coded in `mu`, in the marginal `g`
  (`validation.py:190`) and in the pooled posterior (`validation.py:243`), although
  `fundamental_prior_H` is a declared input. Harmless for the declared value; recorded as
  S3-12.
- Breakpoints (`make_schedule`, `information.py:176-194`) include every support point and every
  entry-threshold crossing for each cost atom (or band edge under atomless costs).

## 3. State-conditioned signal entry and pricing (`signals.py`)

Verdict: **sound for its exercise (C.3), not part of the C.2/C.6 corpus**; one note.

- `SignalSchedule.entry_states` (`signals.py:46-52`) mixes the buyer's private signal
  correctly by state; `price` and `A_direct` (`signals.py:58-76`) use the trader-signal
  posterior `Pr(H | T)`.
- Note: `signals.py:49` contains dead code (`... if False else 1.0`) that silently assumes the
  low-cost floor holds. It should be removed or replaced with the actual check (S3-11).

## 4. Price pooling, atom conditioning, continuation deduplication

Verdict: **defect in C.6 (being patched concurrently); not binding in C.2**.

- Pricing is the benchmark inversion on the raw flow posterior everywhere
  (`Schedule.price`, `information.py:134-138`). `validate(..., price_pools=True)`
  (`validation.py:236-245`) handles exactly one pool family: the zero-entry preimage priced at
  `t_0`, with the OA.70 pooled posterior and a consistency check that the pooled posterior
  itself implies zero entry. No alternative cutoff families (spec 7.5) are enumerated, and no
  `pricing_family_coverage` / `exhaustive_pricing_search` fields exist.
- Identity key. Deduplication is on orders only: `c6_reserve.py:118-122` compares
  `(q_H, -q_L)` within `1e-5`; `c2_correspondence.py:149` the same; `search.py:203` uses
  `1e-6`; `asymmetric_roots` rounds roots to 12 digits (`search.py:123`) but tangency roots
  are never compared with bracketed roots (`c2_correspondence.py:130-136`). No pricing-rule or
  atom identity enters the key (spec 7.3).
- Why C.2 is unaffected: on the benchmark grid `1.005` to `3.8` the low-cost floor
  `B_r(m) - c_L` is positive at every node (checked from the row margins: e.g. `2.79` at
  `1.005`, `2.24` at `3.8`), so entry is positive at every flow, `P(mu)` is strictly
  increasing, and no positive-mass pool exists. Identity by orders is therefore complete for
  every plotted C.2 row.
- Why C.6 is affected: at `r = 1.2`, reserves `p >= 7.95` produce a zero-entry pool with mass
  about `0.5` (`reserve_continuations.csv`, `no_entry_price_mass`), and the class economy's
  low band `[0.95, 1.05]` shows branch changes. These are exactly the regions where the
  concurrent price-pool/event work (spec 8 and 9) must run before any C.6 sweep row is
  retained (S3-04).

## 5. Unilateral order derivative versus candidate-profile change

Verdict: **sound**.

- `Psi(prim, pay, v)` (`search.py:90-93`) builds the schedule for `(1,-v)` and evaluates
  `dU(sched, "L", v)` against that fixed schedule; the outer Brent iteration over `v`
  (`search.py:114`) rebuilds the schedule per trial. `U`, `dU`, `F`, `dF`
  (`deviations.py:43-92`) take a frozen `Schedule`; `lru_cache` on `_exterior_constants` is
  keyed on the frozen dataclass.
- `pure_fixed_points` and `mixed_support_search` recompute the schedule once per iterate and
  hold it fixed during the best-response evaluation (`search.py:164-166, 227-229`). Final
  candidates are validated once against their own fixed schedule (`validation.py:169`).

## 6. Global / refined best-response checks, wrong-signed orders, doubled resolution

Verdict: **sound as a numerical diagnostic; status labels reflect this**.

- `deviation_scan` (`deviations.py:112-126`) evaluates `U(q)` on `[-1, 1]` with 400 then 800
  intervals (`validation.py:261-272`), so wrong-signed orders are included; `U` handles the
  wrong sign with the correct gross payoff `-s * int f(x+eps s) A` (`deviations.py:67-85`).
  Extra points `x_star`, `-x_star` are added.
- No between-grid enclosure exists in the float stack, so accepted asymmetric, symmetric and
  early full-order rows are correctly labelled `numerical diagnostic`; `computer-assisted` is
  reserved for the three certified nodes; `analytical` is only assigned from the uniform
  derivative bound or the J test (`c2_correspondence.py:95-101`).
- The "refined" pass doubles order intervals and raises the Gauss-Legendre order 48 to 64. It
  does not tighten the declared quadrature targets by 10 because the stack has no adaptive
  target; see item 8.

## 7. Support-indifference and off-support checks for mixed candidates

Verdict: **defect (record and coverage), not a wrong formula**.

- Formulae: a converged mixed candidate is validated with the full `[-1,1]` scan against the
  weighted candidate payoff (`deviations.py:95-105`, `validation.py:261-274`), which enforces
  support indifference (any support point below the maximum makes the gain positive) and
  off-support gains, on the finite grid.
- Restriction: only `H` mixes; `L` plays its unique best response (`search.py:214-219`),
  justified by OA.60. The monotone-residual premise holds structurally here (mixtures of
  Laplace densities with nonnegative centres against a nonpositive centre are MLR-ordered),
  but the code never checks it and OA C.2 promises independent probabilities for each type
  (S3-09).
- Search method: a damped multiplicative-weights (replicator) update with `beta = 40`,
  `iters = 150`, one initialisation (uniform weights, `v = 0.5`) per mesh
  (`search.py:221-240`, `c2_correspondence.py:170-171`). It does not solve the indifference and
  simplex system as OA C.2 describes.
- Outcome in the data (`mixed_supports.csv`): 256 of 597 nodes, all of `r <= 2.145`, have
  `not converged` on both meshes; 183 nodes converged, always to the pure candidate `(1,-1)`;
  no genuine mixed candidate was ever produced. A probe at `r = 1.6` shows the dynamics
  drifting toward pooling `(0,0)` with `v -> 0` and a residual gap `2.4e-3` after 150
  iterations; at that gap the pruning threshold needs roughly `ln(1e7)/(40 * 2.4e-3) > 160`
  iterations, so the budget, not the economics, stops the search.
- `mixed_supports.csv` records `support_gap` and `off_support_gain_bound` from the mesh only
  (`c2_correspondence.py:187-188`); the latter is a mesh maximum, not a bound. Starts,
  stopping rule, iteration count and history are not in the CSV; the manifest method string
  names the meshes only. Non-converged nodes are not written as `open` rows in
  `correspondence.csv` (`c2_correspondence.py:183-184`), so the manifest's `open_rows = 23`
  understates the unresolved search (S3-01).

## 8. Tail/error bounds, breakpoints, warnings, retries

Verdict: **defect (budget not enforced or recorded); breakpoints sound**.

- Breakpoints: `convolve_full_line` (`quadrature.py:41-73`) splits at the shifted density
  centre, the support hull, and every schedule breakpoint (support kinks and entry-threshold
  crossings). Exterior Laplace tails are integrated analytically with the constant residual
  (`quadrature.py:63-65, 76-83`), so `tail_bound = 0` in the CSV is correct for Laplace.
- Error budget: the quadrature error estimate (`|GL48 - GL24|`) is computed and stored on
  `Validation.quadrature_error` (`validation.py:265`) but never compared with
  `quadrature_absolute_target` / `quadrature_relative_target` anywhere in `numerics/`
  (only C.1 and C.3 write it to a CSV). `correspondence.csv` and `reserve_continuations.csv`
  carry `tail_bound` but no quadrature error column. A probe at the certified `r = 1.6`
  candidate gives `4.6e-18`, so enforcement would pass, but the declaration in C.0 is
  currently decorative (S3-05).
- Retries: none are declared; unconverged best-response starts are counted
  (`c2_correspondence.py:160-166`) and unconverged mixed searches are flagged; no bounded
  retry with a documented escalation exists. Acceptable if stated, but the manifest should say
  so.
- Warnings: `scipy` warnings are not captured; `brentq`/`fsolve` failures are handled by
  return flags.

## 9. Full-parameter joins to registry and figure data

Verdict: **sound**.

- `registry.py:150-185` joins on exact `Decimal` equality for `r`, `p`, `epsilon_V`, string
  equality for `value_law`, `branch`, `boundary`, and requires `accepted == true` and exactly
  one match. No rounded scalar is used as a key.
- No registry quantity is sourced from `correspondence.csv`; Figure 2 reads it directly and
  uses `accepted`, `branch`, `multiplicity_found` and `Decimal(r)` (`figures.py:47-60`).
- The C.2 and C.6 CSVs carry only `r` (and `p`, `value_law`) rather than the full parameter
  vector; they are keyed to the manifest's `inputs.benchmark` and output hashes, which C.0
  permits.

## 10. Equality/event handling and status/classification logic

Verdict: **partly defective (inconsistent "no candidate" versus "open")**.

- A negative sufficient-condition margin is never turned into a rejection: a failed J test or
  uniform bound yields `numerical diagnostic` (`c2_correspondence.py:95-101`,
  `c6_reserve.py:94-96`); rejection comes only from `Validation.breaches`. The seven rejected
  asymmetric roots at `1.775` to `1.805` carry an `epsilon_q` witness of about `5e-4`
  (high-type deviation), preserved as required.
- Tie rule at `r_C`: handled symbolically via `tie_at_ceiling` and re-solved in
  post-processing; the full-order line breaks there (E drops from `0.5065` to `0.25`).
- Inconsistency: a local `|Psi|` minimum that is not a root is labelled `rejected` in C.2
  when the minimum exceeds `1e-4` (`TANGENCY_OPEN`, `c2_correspondence.py:29, 137-142`) and
  `open` whenever validation fails in C.6 (`c6_reserve.py:115-117`), with no reference to the
  `Psi` quadrature error in either. Neither exercise has a "no candidate" outcome. In C.6 this
  marks 27 class-economy nodes with `|Psi|` minima up to `4.2e-2` as unresolved. In both
  exercises, `asymmetric_discontinuity` rows (a sign change of `Psi` across the plateau
  boundary, not a root) are labelled `rejected` although no candidate was ever formed
  (S3-02, S3-13).
- `search_unresolved = unresolved or not acc` (`c6_reserve.py:143`) conflates a converged
  search with all candidates rejected and an unconverged search; the data contain no
  zero-accepted nodes, so this is latent.

## T24: plotted Figure 2 rows

Columns present in `correspondence.csv`: `r, branch, q_H, q_L, v, e_H, e_L, E, O_H, R_T, tau,
x_star, pooling_exists, pooling_unique_bound, full_unique_bound, existence_status,
uniqueness_status, accepted, multiplicity_found, epsilon_P, epsilon_e, epsilon_q, tail_bound,
unresolved_reason`. Absent: quadrature error, posterior-inversion error, entry independent
formula error, per-state deviation argmax/gain, weights (mixed), parameter columns beyond `r`.

Row counts (1837 rows, 597 strength labels, 596 distinct strengths):

| branch | accepted | rejected | open |
|---|---|---|---|
| pooling | 170 (analytical) | 427 | 0 |
| full_orders | 414 analytical + 32 numerical diagnostic | 151 | 0 |
| asymmetric | 3 computer-assisted + 43 numerical diagnostic | 7 (eps_q witness) | 0 |
| symmetric_interior | 23 numerical diagnostic | 0 | 0 |
| asymmetric_discontinuity | 0 | 74 | 0 |
| asymmetric_tangency | 0 | 470 | 2 |
| pure_search | 0 | 0 | 21 |
| mixed | 0 | 0 | 0 (non-convergence only in `mixed_supports.csv`) |

- Input declaration: keyed to `manifests/c2_correspondence.json` (`inputs.benchmark`, mesh,
  offsets, certificate brackets, tolerances, software, output hashes). Complete.
- Continuation identity: `(r, branch, q_H, q_L)`; complete for C.2 because no pool exists on
  the grid (item 4).
- Pricing/preparation checks: `epsilon_P`, `epsilon_e` recorded; `epsilon_P` compares the
  price with the same formula (`validation.py:213-215`) and is tautological; the independent
  checks (`posterior_inversion_error`, `entry_independent_error`) are computed and gate
  acceptance but are not written (S3-06).
- Best responses over the full interval: computed on 400 then 800 intervals over `[-1,1]`
  for both states; only the scalar `epsilon_q` and `tail_bound` are recorded (S3-08).
- Line breaks: `_broken_series` (`figures.py:26-36`) breaks when consecutive accepted nodes
  are more than `0.0075` apart or the value jumps by more than `0.02` (E) or `0.2` (v). The
  asymmetric line is contiguous from `1.508` to `1.679` with no missing node (the branch
  starts at a fold: open tangency at `1.507`, `|Psi| = 9.2e-5`); it ends where `v -> 1`
  (`0.99980` at `1.679`) and `asymmetric_discontinuity` rows take over at `1.68`. The
  full-order line breaks at `r_C`. Existence-status changes along the full-order line
  (`numerical diagnostic` on `1.678` to `1.805`, J test to `2.8375`, uniform bound beyond)
  are not styled differently (S3-07).
- Multiplicity shading: `min` to `max` of nodes with `multiplicity_found` (`figures.py:55-60`).
  In the data this is `1.508` to `1.834` with no interior hole (84 distinct strengths; the
  manifest says 85 because `1.6` and `1.60` were solved as two nodes). `multiplicity_found`
  is `n_acc >= 2` over accepted rows at the node (`c2_correspondence.py:192-194`). It can
  double count: at `1.51` the same root is recorded twice (`v = 0.206753361324` from the sign
  change, `0.2067533615346538` from `|Psi|` minimisation), and at `1.6`/`1.60` every branch is
  duplicated. Neither changes the shaded span (pooling coexists at those nodes), but the
  counting rule is not the continuation-level dedupe spec 7.3 requires (S3-03).

## T25: mixed supports

`mixed_supports.csv` columns: `r, branch, state, support_index, q, weight, U(q), support_gap,
off_support_gain_bound, accepted, status`. Present: per-support payoff (mesh lookup), weight,
mesh gap, mesh off-support maximum, mesh spacing (in `branch`). Absent: simplex check (weights
are renormalised but no residual is written), search domain beyond the mesh label, start
(single implicit start), iteration count, stopping condition, attempt history, quadrature
error. The sentence at `paper/main.md:294` ("They found no mixed equilibrium, which remains a
search result...") is not supported by these records under spec 10.3: on the whole informative
region (`r <= 2.145`) the search did not converge, and where it converged it reached `(1,-1)`.
The honest statement is that the mixed search is unresolved there.

## T26: reserve counts

- Counts in Table 4 Panel C are computed from `reserve_ranges.csv` rows at render time
  (`tables.py:252-265`): number of reserves, nodes with `accepted_continuations_found >= 2`,
  nodes with `search_unresolved`. Not hard-coded.
- Distinctions: `reserve_continuations.csv` distinguishes `rejected` (with breach witness) from
  `open`; analytical exclusion of other candidates is inferable only from the pooling or
  full-order status string; `reserve_ranges.csv` has no reason column. Of the 497 unresolved
  nodes, 27 are open tangencies visible in the continuations file and 470 are mixed/pure
  non-convergence recorded only in an in-memory `diag` that is never written
  (`c6_reserve.py:137-138, 265`). "No candidate" is not a category. `global_envelope_certified`
  is `false` throughout, and no global maximum is inferred; the "revenue maximum" is a sampled
  best (`p = 6.280` at `r = 1.2`, one grid step below the low-cost floor event
  `p = h - 1/m = 6.2817`, which the grid does not contain; spec 9.1 events are the concurrent
  task).
- Declared comparisons (Panels A and B): all eight rows `analytical` with the actual floor
  `e(m)` in the full-order bound, oracle error `<= 1.2e-14`, exactly one accepted continuation
  each. These do not depend on the sweep.

## Verdict table

| item | verdict | severity | recommended patch |
|---|---|---|---|
| 1 auction payoffs | sound | note | none |
| 2 densities/posteriors | sound | note | make the prior an explicit parameter (S3-12) |
| 3 signals | sound (C.3 scope) | note | remove dead floor assumption (S3-11) |
| 4 pools/identity | defect (C.6); not binding (C.2) | must-fix-before-retaining C.6 sweep | concurrent price-pool/event work; identity on orders plus pool set plus outcome enclosure (S3-04) |
| 5 derivative separation | sound | note | none |
| 6 global BR checks | sound as diagnostic | note | none beyond recording (S3-08) |
| 7 mixed checks | defect (coverage, records) | must-fix-before-retaining sentence | rerun with adequate budget and multiple starts, write open rows and attempt records, or delete the sentence (S3-01, S3-09) |
| 8 error budget | defect (not enforced/recorded) | must-fix-before-retaining | add quadrature_error column and check against declared targets; document GL refinement as the x10 rule (S3-05) |
| 9 joins | sound | note | none |
| 10 status logic | partly defective | must-fix-before-retaining C.6 Panel C; note for C.2 | unify tangency rule tied to Psi error; add "no candidate"; persist C.6 diag reasons (S3-02, S3-13) |
| T24 duplicates | defect | must-fix-before-retaining | normalise grid keys, dedupe tangency roots against bracketed roots, recompute multiplicity, refresh manifest (S3-03) |
| T24 line styling | minor | note | style diagnostic segments; group multiple roots per node (S3-07) |
| T25 records | defect | must-fix-before-retaining | S3-01 |
| T26 reasons | defect | must-fix-before-retaining Panel C | S3-02 |

## Recommendation

**C.2 Figure 2: retain after a targeted rerun.** The payoff, posterior, deviation and
validation layers behind every plotted row are correct, every plotted line is supported by
accepted rows, and the low-cost floor holds at every node so price pools do not arise. Required
before retaining: (i) S3-03 (normalise `1.6`/`1.60`, dedupe the `1.51` root, recompute
`multiplicity_found`, refresh manifest counts); (ii) S3-05 and S3-06 (write quadrature and
independent pricing errors and check the declared targets); (iii) S3-01 for the mixed search:
either rerun with a convergence-based budget and at least three documented starts and write
`open` rows where it still stalls, or remove the sentence at `paper/main.md:294` and say the
mixed search is unresolved; (iv) S3-07 styling (dash the finite-grid segment of the full-order
line; shade only contiguous multiplicity runs). Only (iii) touches the manuscript. None of these
requires the hour-long sweep; (i), (ii), (iv) are post-processing plus a re-validation of the
affected nodes, and (iii) is a per-node rerun of the mixed search only.

**C.6 Panels A and B: retain as they stand.** Analytically classified, oracle-checked, single
accepted continuation each.

**C.6 Panel C (exploratory sweep): do not retain in the current form.** Its identity key
ignores price pools (S3-04, concurrent work), its unresolved counts mix non-root tangencies with
budget-limited searches and record no reason (S3-02), and its regions of interest (`p` in the
low band, `p >= 7.95`) are exactly where the spec 8 and 9 regressions must run first. If the
price-pool/event patches and a rerun of the affected reserve intervals complete within the
bounded scope, Panel C can return with per-node reasons; otherwise apply the spec 3.2 fallback
to Panel C only (keep Panels A and B, archive the sweep files and this ledger, and let Table 4's
note say the sweep is withheld pending the audited rerun).
