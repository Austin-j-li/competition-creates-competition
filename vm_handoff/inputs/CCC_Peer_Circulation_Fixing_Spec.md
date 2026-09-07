# Competition Creates Competition
## End-to-end fixing specification for peer circulation

**Owner:** Austin Li  
**Audience:** the local executing agent with access to the assembled manuscript repository  
**Release objective:** a coherent, mathematically faithful, reproducible working paper that Austin can send to research peers for substantive feedback  
**Scope:** revise, audit, rebuild, and package the existing paper; do not restart its research program  
**Specification version:** 1.0

> **Keep the economic claim at the center: a stronger rival can make target shares more informative and thereby recruit the challenger it would ordinarily deter. Make every displayed claim traceable to the result and computation that supports it.**

---

## 0. Execution mandate

Execute this specification in the author's local manuscript repository. Deliver the revised editable sources, regenerated main paper and online appendix, the verified numerical outputs supporting everything shown, and a compact completion report. Do not stop after returning an implementation plan or a list of recommended changes.

This is a **bounded peer-circulation revision**, not a demand to finish a journal paper. The main equilibrium theorem, complementary-information theorem, and selected interval-certified equilibria already provide the foundation. The seller's optimal institution remains the next research result. It is not necessary to solve that open problem, a first-price auction, or a new empirical project to complete this release.

The essential numerical repair is narrower and concrete: outside the positive-preparation-floor region, a continuation can vary in its **price-pooling rule even with the investor orders fixed**. The local representation and validator must support that distinction. The exact regression example and complete acceptance conditions are supplied below.

### 0.1 Order of authority

Use the following sources in this order for this revision:

1. The author's request to polish the assembled paper for peer circulation and this execution specification.
2. The actual current editable manuscript sources and the two reviewed PDFs, matched by content and hash where available.
3. The completed end-to-end review, for its identified repairs and new derivations.
4. The original manuscript-build handoff, for the locked title, framing, status vocabulary, three-tier proof structure, and scaffold-only empirical scope.
5. Preserved numerical verification packages, as independent reference implementations and recorded evidence—not as a substitute for validating the assembled repository.

A source document is evidence, not an instruction to accept its mathematics without checking it. If a new calculation contradicts a retained theorem or certificate, stop the affected release stage, preserve the evidence, and diagnose the discrepancy. Do not choose whichever source has the desired sign.

### 0.2 What this specification does not authorize

Do not change primitives, select a preferred equilibrium, raise tolerances, alter tie rules, truncate inconvenient branches, or relabel calculations solely to retain the headline. Do not add a general hump theorem. Do not claim seller-optimal discovery from a best-found reserve. Do not invent a public price-learning episode in a named acquisition. Do not add coauthors, acknowledgments, departmental approvals, or empirical findings.

Do not send the manuscript, email peers, publish a repository, or upload to a public working-paper service. The final action is to give Austin a release package and an accurate completion report.

---

## 1. Inputs, baseline identification, and source discovery

### 1.1 Reviewed baseline

The review uses these exact PDF versions:

| Input | SHA-256 |
|---|---|
| `main_filled.pdf` | `6568203e5266ffe076ec094ef9768b763f7a227813064418fa680c4b6bff1427` |
| `online_appendix_filled.pdf` | `734a51c2e4ed130e3cb11597c89d2c32d39a01dad64704ee1979a54427e36922` |
| `CCC_Assembled_Manuscript_E2E_Review.md` | `5ff122edbe85af983cb49a03f4e4a6b6d599b05825e9ae3ab970619834d73950` |

In this specification, **M** means the reviewed main PDF, **OA** its online appendix, **ER** the end-to-end review, and **H** the original manuscript-build handoff. Page numbers are anchors into the reviewed PDFs, not permanent positions in the revised files. Locate edits by section, result, and distinctive text as well as by page.

The companion `reference_material/` folder includes the reviewed PDFs, ER, H, the bibliography reference file, and the two preserved verification archives. Those archives have different roles and must be kept in separate directories. Both contain a directory named `verification/`; do not extract them over each other.

### 1.2 Discover the actual repository; do not assume an old project path

At the local task root, identify:

- The editable main manuscript and online appendix, normally `main.md` and `online_appendix.md`.
- The bibliography actually named by their front matter.
- The placeholder manifest, quantity registry, generated tables, figure data, and generated figure files.
- The numerical modules producing the baseline, signal, correspondence, reserve, and certificate exercises.
- The existing build entry points, TeX templates, bibliography processor, and PDF engine.
- Dependency declarations and the interpreter/environment used by the assembled build.
- The preserved independent verification seed and any already-ported certificate implementation.

Inspect repository metadata and the build configuration before importing or running executable project code. Identify configuration side effects and commands that overwrite files. Use a targeted filename search that excludes `.git`, virtual environments, caches, and dependency directories. Do not recursively search unrelated home directories or another research repository.

Record the results in `audit/peer_polish/repository_map.md`. For each semantic role, record the actual path, whether it is source or generated, and the command that produces or consumes it. **Paths mentioned later in this specification are proposed output roles; adapt them through this map rather than guessing that a particular module already exists.**

### 1.3 Protect the starting state

Create a revision branch or worktree only after checking the local Git state. Preserve tracked modifications and relevant untracked files; do not stash, reset, clean, or overwrite the author's work without authorization. If Git is unavailable, make a timestamped snapshot of the affected source and output files.

Store:

- Commit identifier, tracked diff, untracked-file inventory, and repository root.
- SHA-256 hashes of the starting sources, bibliography, input declarations, PDFs, tables, figure data, and preserved seed files.
- Actual interpreter, numerical package, TeX engine, and bibliography processor versions.
- The build commands as argument arrays and their working directories.
- Whether the local source reproduces the reviewed version or contains later changes.

A hash mismatch with a later local PDF is not evidence of corruption. Map the differences and apply only still-relevant fixes. Do not replace a newer local source with the older reference merely to match a hash.

**Hard stop:** if only PDFs are present and editable source or the producing numerical repository cannot be located, do not reconstruct a supposedly authoritative research repository from PDF text. Finish the inventory, identify the missing items precisely, and report the blocked stage. Independent reference checks can still run in an isolated directory.

---

## 2. Locked scientific and editorial decisions

### 2.1 Scientific identity

Keep the title:

**Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders**

Keep the principal objects and notation:

$$
r,\ell,h,p,\rho,c_L,c_H,b,k;
\quad t_0,t_H,t_L,g_H,g_L;
\quad \Delta_T,B_r(\mu),m,M;
\quad \tau,x^*,\alpha_H,\alpha_L,r_N,r_U,r_C.
$$

Keep the current benchmark, the price-only information restriction, truthful second-price implementation, and the distinction between the investor's informational trading decision and the buyer's preparation decision. The complementary-signal model is an extension, not a silent replacement for the benchmark.

The headline is an equilibrium participation reversal on a stated primitive region. The finite rise-and-fall comparison is a supporting implication. The full intermediate equilibrium correspondence is not characterized. The bargaining proposition is an acquisition-payment result, not a complete trading-and-entry equilibrium under bargaining.

### 2.2 Result-status vocabulary

Restore the agreed substantive vocabulary:

- **Analytical:** established by the stated argument under its stated conditions.
- **Computer-assisted:** an analytical argument completed by outward interval enclosures and a global deviation cover.
- **Numerical diagnostic:** validated floating-point calculation or finite search that does not establish the stronger analytical or interval claim.
- **Open:** a precisely stated result not yet established.

State the substantive status once at each formal result statement. For example:

> **Proposition 2 (Competition creates competition; analytical).** *[Statement.]*

> **Proposition 3 (Coexisting informative equilibria; computer-assisted).** *[Statement.]*

Do not repeat warning labels in every paragraph. Tables may carry an evidence classification, but **evidence type and uniqueness are separate fields**. Analytical existence does not imply analytical uniqueness. A negative sufficient-condition margin does not reject a candidate equilibrium.

“Control” is an **experiment role**, not a fifth evidence status. A frozen-order control is not an investor equilibrium. A price-hidden economy must be reoptimized. The matched-dividend calculation is an analytical invariance diagnostic, not a new feasible sale mechanism.

### 2.3 Authorial voice and prose

Restore **first-person plural** consistently in editable manuscript prose, as fixed in H. Austin Li remains the sole named author; rhetorical “we” does not imply coauthorship. Do not mechanically replace letters inside equations, citation fields, quotations, code, or variable names.

Write a paper, not a review response. Neither manuscript should mention assistants, models that reviewed it, the proposal exchange, the critique, this spec, or a local executing agent. Reproducibility may identify software and numerical methods. Internal audit records may identify this specification and its source files.

Conditions define the region of the theorem. Explain their economic roles directly. Keep unresolved seller design as the next result to prove rather than repeatedly apologizing for it.

### 2.4 Source and number discipline

Edit authoritative source manuscripts and generating functions. Never patch a generated PDF, a filled manuscript, or a rendered table to change a result.

Preserve the placeholder-to-registry mechanism. Every reported numerical research quantity must resolve to a validated output row with a complete parameter and continuation identity. Exact model constants, symbolic coefficients, numbered labels, references, and declared numerical inputs remain literal where the existing build contract allows them. Do not turn mathematical constants into numerical placeholders.

Numerical values printed in this spec are acceptance landmarks, not a license to paste them into the paper. Recompute the relevant quantities; populate the manuscript through the registry.

### 2.5 No expanding the empirical scope

Keep empirical work as a design scaffold. Retain the limited Imprivata illustration only for the process stages its cited filing supports. Do not add a sample count, estimated effect, instrument, or claim that a price caused entry. Keep event occurrence and first-public disclosure dates distinct.

---

## 3. Release scope and fail-fast policy

### 3.1 Required scientific content for peer circulation

The peer release must contain:

1. The acquisition-payoff opposition and the main unique-outcome reversal.
2. Price sufficiency and residual-profit logic visible in the main text.
3. The baseline controls, moderate-value example, and complementary-information example.
4. The selected asymmetric certificates, with their correct existence interpretation.
5. The fixed-strength surplus result and the payment-stage bargaining comparison.
6. Supported fixed-reserve comparisons, with preparation distinguished from actual admissible bidding.
7. The seller's joint trading/pricing continuation problem stated correctly.
8. A scaffold-only institutional/empirical section.

Every displayed numerical claim in this content must be reproduced and validated. The release cannot become “sendable” by silently deleting an established result whose implementation fails. A core discrepancy is a blocker until resolved or explicitly returned to Austin as a substantive decision.

### 3.2 Two permitted publication scopes, not two standards of truth

**Default target: audited working-paper release.** Retain the existing exploratory curves and online reserve summaries only after the actual source, inputs, output rows, and deviation checks have been inspected and rerun as specified.

**Preauthorized fallback: core-validated peer release.** If the expanded search corpus is unavailable or remains unresolved within the bounded work below, remove its unsupported numerical claims from both peer-facing PDFs. Replace the correspondence plot with analytically classified regions and the certified nodes; do not connect those nodes with an inferred equilibrium curve. Preserve all removed data, code, and claims in the internal audit archive, with an exact removal ledger. The manuscript then says which equilibria are established and leaves broader characterization open.

This fallback is allowed for **optional exploratory coverage**, not for a failed core theorem, certificate, or required regression. It must be conspicuous in `completion_report.md`; it must never be used to hide a discovered counterexample or an unfavorable valid branch.

A known valid negative entry comparison remains visible. A failed candidate is retained as rejected. A search that cannot resolve a node is retained as open. These are different outcomes.

### 3.3 Fail-fast distinctions

| Event | Required handling |
|---|---|
| A retained theorem's conditions or proof fail | Stop scientific sign-off; write a minimal counterexample or exact failed step. |
| A retained interval certificate fails | Stop the affected claim; preserve all enclosures and distinguish inconclusive enclosure from a contradiction. |
| A new trial candidate has a profitable deviation | Record rejected candidate and its witness; the search may continue. |
| A declared local solve does not converge | Record an open node with method and residuals; use bounded documented retries, not interpolation. |
| Unexpected exception, schema mismatch, missing quantity, NaN, or code bug | Stop the stage with traceback and inputs. Do not substitute zero, a nearby row, or cached output. |
| Tight numerical enclosure is inconclusive | Increase precision or subdivide within the declared escalation budget; retain every attempt. |
| Missing optional search corpus | Use the controlled fallback only after recording precisely what cannot be audited. |
| External bibliography site temporarily unavailable | Preserve the existing sourced version; record failed access. Do not fabricate an updated version. |

Use explicit exceptions for new acceptance checks, not only Python `assert`. The legacy seed uses assertions: preserve it byte-for-byte and refuse to run that seed under Python optimization or `PYTHONOPTIMIZE`. Legitimate arithmetic refinement is not permission to loosen an acceptance tolerance.

---

## 4. Execution sequence and gates

| Stage | Work | Gate before proceeding |
|---|---|---|
| S0 | Discover repository, protect starting files, reproduce the current build | G0: inventory and source/generated separation are complete; discrepancies are recorded. |
| S1 | Freeze result/claim ledger, reproduce core numbers and the three interval certificates | G1: every retained core claim has correct conditions, status, and numerical evidence. |
| S2 | Add explicit price-pool validation and exact reserve-event tests; audit existing continuation representation | G2: regressions pass; continuation identity includes prices and pools, not only orders. |
| S3 | Validate the displayed exploratory corpus or apply the controlled fallback | G3: every remaining displayed search result has inspected source and validated rows. |
| S4 | Revise introduction, institution, model completeness, wording, and proof placement | G4: scientific meaning is unchanged except for explicitly recorded corrections. |
| S5 | Regenerate tables and figures; shorten the printed registry; reconcile citations | G5: rendering consumes only validated data; all links and references resolve. |
| S6 | Clean rebuild, numerical cross-check, full visual inspection, and fresh-directory reproduction | G6: sources, data, PDFs, and instructions are mutually consistent. |
| S7 | Assemble peer-facing files and source/replication bundle; write completion report | G7: release checklist passes and the delivery is accurately labeled. |

S4 drafting may proceed while independent numerical runs execute, but final prose, captions, and numerical claims cannot be signed off before G1–G3. Work in checkpointed stages; do not make all changes in one opaque commit.

Create a single executable release entry point, preferably `make peer-release`, using the existing build architecture. If an equivalent task runner already exists, wrap it rather than replacing it. The entry point must run validations before rendering and propagate failures. It is a required interface to implement, **not a claim that this target currently exists**.

Record the actual commands in a runbook. Commands guessed from PDF descriptions are not reproducibility instructions.

---

## 5. Task S0 — Baseline and build provenance

### S0-A. Source map and baseline build

Run the existing build in an isolated output directory using the discovered environment. Record exit status, standard output/error, runtime, and input/output hashes. Separate running the raw numerical exercises from rebuilding presentation from existing accepted outputs.

Establish whether the current build reproduces the starting PDFs' substantive contents. PDF bytes may differ because of timestamps or metadata. Compare extracted text, numerical tables, figure inputs, and selected rendered pages before calling this a substantive mismatch. Record any intentionally nondeterministic PDF metadata; do not use that explanation to dismiss numerical differences.

### S0-B. Build graph

Document the actual directed graph:

$$
\text{exact inputs + numerical source}
\to \text{raw candidates}
\to \text{independent validation}
\to \text{accepted numerical tables}
\to \text{quantity registry}
\to \text{filled sources / figures}
\to \text{typesetting}
\to \text{PDFs}.
$$

Every step must have a producing command. A figure renderer must not solve an equilibrium. A registry must not silently read an unrelated old results directory. A filled manuscript must not be the authoritative location of a corrected formula.

### S0-C. Internal records

Create these logical records, mapping to existing paths where appropriate:

```text
audit/peer_polish/
    repository_map.md
    baseline_manifest.json
    claim_ledger.csv
    issue_ledger.csv
    source_output_map.csv
    run_manifest.json
    logs/
    raw_failures/
    visual_checks/
    completion_report.md
```

Do not create parallel canonical datasets merely to match these suggested names. An adapter or documented path map is sufficient. Internal records must not leak into manuscript prose.

**Acceptance:** a fresh implementer can identify the authoritative sources, actual producing commands, reviewed baseline, and exact local revision without relying on this conversation.

---

## 6. Task S1 — Protect and reproduce the scientific core

### S1-A. Claim ledger

Before changing prose, create one row per formal result and per distinct numerical/search claim, including captions. Use:

```text
claim_id, source_anchor, short_claim, maintained_conditions,
result_status, experiment_role, existence_scope, uniqueness_scope,
proof_location_main, proof_location_online,
parameter_set_id, continuation_id, producing_exercise,
independent_validation, retained_in_peer_release, change_reason
```

The current principal map is:

| Current result | Retained scope | Required evidence |
|---|---|---|
| Proposition 1 | Distributional payoff opposition under the stated sale institution | Pointwise payment difference and FOSD integrals. |
| Proposition 2(i)–(ii) | Unique trading/on-path preparation outcomes at the compared strengths | All (A1)–(A3) hypotheses; posterior inversion; global bounds; construction. |
| Proposition 2(iii) | Conditional finite decline at a further strength | Extra low-cost, full-order, and expensive-entry-infeasibility conditions. |
| Proposition 3 | Exact informative equilibria at declared nodes; coexistence; ordered entry | Root enclosures, low-type concavity, high-type global cover, pooling margin. |
| Proposition A.3 | Deterrence at a fixed information experiment | Complete buyer information and pointwise entry comparison. |
| Proposition A.4 | Distinct threshold concepts on their maintained domain | Defining equations, support and floor checks, boundary tie rule. |
| Propositions A.5–A.6 | Smooth-noise and atomless-cost extensions in stated regions | Bounded log-density slope and appropriate cost-support conditions. |
| Proposition A.7 | Complementary private signals | State-conditioned entry, public-price inversion, correct residuals and bounds. |
| Proposition A.8 | Acquisition-stage bargaining comparison | Verifiable values, enforceable fallback, correct no-entry payoff. |
| Proposition A.9 | Surplus and target proceeds from price access at fixed strength | Same-trading coupling, paid preparation costs, conditional expected surplus. |
| Selected reserve comparisons | Specified supported continuations, not optimal reserves | Full-domain auction oracle and correct continuation validation. |
| Search curves and summaries | Only the candidates and coverage actually validated | Inspected numerical source, complete rows, method/tolerance records. |

Keep stable internal labels even if display numbering changes. Produce an old-to-new result/equation/figure/table label map when reorganizing.

### S1-B. Baseline numerical exercises

Run the actual local producers and an independent implementation of the key quantities. Reproduce the exact declarations in OA C.0; never reuse a parameter vector because two experiments have similar names.

Required comparisons:

- Weak, strong, and very strong benchmark economies.
- Frozen informative orders at both weak and strong strength.
- Price-hidden equilibria at both strengths.
- Matched external dividend at fixed strength.
- Logistic noise and atomless preparation-cost variants.
- The moderate-value example.
- Complementary-signal declared example and every displayed row of its accuracy grid.
- All stated fixed-reserve binary and atomless-class comparisons.
- All threshold quantities actually printed.

Reference landmarks, evaluated under the parameters in the PDFs, are:

| Quantity | Decimal landmark |
|---|---:|
| Strong benchmark preparation | 0.5227572973 |
| Strong high-value challenger ownership | 0.3241924258 |
| Strong target proceeds | 0.8723920451 |
| Frozen informative-profile preparation at weak strength | 0.5621780582 |
| Strong price-hidden target proceeds | 0.6145833333 |
| Fixed-strength net acquisition-surplus gain | 0.0802175348 |
| Logistic strong preparation | 0.3015088516 |
| Atomless-cost Laplace strong preparation | 0.5227147164 |
| Atomless-cost logistic strong preparation | 0.3013741277 |
| Moderate-value strong preparation | 0.5268046622 |
| Complementary-signal strong preparation | 0.8794375516 |

These are not substitute inputs and are not interval bounds. Agreement with them is necessary for unchanged experiments but not sufficient to validate an implementation. Independent payoff integration, Bayesian identities, and deviation checks are also required.

### S1-C. Numerical acceptance contract

Retain the OA C.0 tolerances or stricter ones, without treating ordinary quadrature estimates as rigorous certificates:

| Diagnostic | Initial target / acceptance |
|---|---:|
| Absolute and relative quadrature target | `1e-11` each |
| Probability normalization and posterior mean identities | `1e-8` |
| Conditional price identity | `1e-8` |
| Buyer preparation deviation gain | `1e-8` |
| Ordinary numerical investor deviation gain | `1e-7` |
| Independent formula/oracle agreement | `1e-9` |
| Initial / refined order intervals | `400 / 800` |
| Initial interval-certificate decimal precision | `50` |
| Initial / refined certificate derivative intervals | `200 / 400` |

For ordinary integration, tighten both integration targets by a factor of ten and double the order resolution. Record the refined results, not just the existence of a refinement option. If machine precision obstructs the tightened target, use a documented higher-precision method or mark the required check unresolved. Do not suppress integration warnings or print that an unachieved target passed.

Integrate infinite tails or bound their omitted payoff contribution. Split at every shifted density center, posterior kink, entry threshold, and price-pool boundary. Thresholds at unattained limits require analytical handling, not a very large finite replacement.

Separate error budgets for residual approximation, quadrature, tail truncation, and between-grid deviation coverage. Never report one solver residual as an upper bound on all four.

### S1-D. Interval-certificate port

Extract the legacy certificate into a reference-only directory. Run it without optimization and without altering its source. Run the local port separately.

For each declared strength and exact decimal bracket, verify:

1. Support conditions, prior high-cost exclusion, and low-cost participation.
2. Threshold location throughout the entire bracket.
3. Strictly positive outward enclosure for the left endpoint of the low-type root equation.
4. Strictly negative outward enclosure for its right endpoint.
5. Global strict concavity of the low-type problem under the proved regularity.
6. The high-type derivative cover for **every point in the root bracket**, not just a midpoint.
7. Positive pooling-existence margin at the same strength.
8. Outward entry enclosure and strictly ordered nonoverlapping entry intervals across the nodes.

The legacy decimal brackets are:

```text
r = 1.55 : v in [0.46031618, 0.46031620]
r = 1.60 : v in [0.70747537, 0.70747539]
r = 1.65 : v in [0.90333198, 0.90333201]
```

Compare the port's full endpoint objects with the preserved result file, not only printed digits. Different valid enclosures are acceptable if they establish the same statement and the manuscript's displayed intervals enclose them. Do not shrink an interval to reproduce an old display. Recompute the display outward if a legitimate enclosure is wider.

A failed interval enclosure is not automatically a counterexample. Try, in order, higher precision, refined derivative coverage, and mathematically justified bracket subdivision, retaining each attempt. Recommended finite escalation: `50`, `80`, then `120` decimal digits; derivative meshes `200`, `400`, then `800`. Exhausting that schedule produces an open certificate, not a pass. Never increase the admissible strategic deviation gain to make a certificate succeed.

**Acceptance:** the three selected exact equilibria remain supported with the printed bound directions correct. This does not clear any continuous curve between them.

---

## 7. Task S2 — Represent complete pricing-and-trading continuations

### 7.1 Required conceptual correction

Inside the main theorem's positive preparation-floor region, the price-sufficiency lemma identifies the relevant flow posterior from the price. Outside that region, the same order profile can admit different price pools and therefore different preparation decisions.

Do not let the local continuation object be only `(q_H, q_L)`, or only a pair of mixed supports. It must also describe pricing, beliefs at price atoms, and preparation. ER §3 provides an explicit example; OA C.6 currently describes pools but its convenient construction must not be treated as the only admissible one.

The baseline theorem and its controls are unchanged. The correction applies to expanded sale-design continuations, where their denominator can vanish.

### 7.2 Required continuation data model

Use the existing architecture where sound, but require these semantic fields:

```text
Continuation
    parameter_set_id
    institution_id
    information_structure_id
    tie_rule_id
    investor_strategy
        state/signal supports and weights
    pricing_rule
        rule_family
        piecewise domain or explicit pool sets
        positive-entry price mapping
        exact event identifiers where relevant
    price_information
        each positive-mass price atom and its full flow preimage
        state-conditional atom masses
        total atom mass and pooled posterior
        posterior map on nonpooled prices
    preparation_rule
        actions by observed price, cost, and private signal when present
    validation
        pricing, belief, entry, investor, support, and arithmetic evidence
    result_status
    existence_scope
    uniqueness_scope
    search_coverage_scope
```

Names can differ in code; no semantic component may be omitted. Class information is not exact within-class value information. A noisy trader signal is not the fundamental state. Keep those tags distinct.

### 7.3 Identity and deduplication

Create an immutable parameter identity from canonical exact input declarations. Create separate raw-candidate and continuation identities. A candidate identity records how the calculation was obtained; economic equivalence requires comparing complete strategies and induced price information.

Never deduplicate solely on:

- rounded incumbent strength or reserve;
- investor orders or mixed supports;
- entry probability alone;
- mean price or seller revenue alone;
- a solver's branch name.

Two identical-order candidates with different non-null price pools must survive as different continuations. Conversely, multiple solver initializations converging to the same complete outcome should not inflate multiplicity counts. Differences only on null sets are not economically distinct. Use canonical rules, explicit tolerances, and—when relevant—disjoint outcome/error enclosures to justify distinctness. Preserve the raw attempts even after deduplication.

### 7.4 Price-atom validation

For each positive-mass pool $A\subseteq\mathbb R$ with a common observed price, calculate

$$
\mu_P(A)=
\frac{\pi\int_A a_H(x)\,dx}
{\pi\int_A a_H(x)\,dx+(1-\pi)\int_A a_L(x)\,dx}.
$$

The benchmark has $\pi=1/2$. Use the actual buyer posterior at the observed price, including the buyer's private signal in the signal extension. Do not use $\mu_X(x)$ separately inside a pooled set.

Then verify, for every relevant state/flow region:

1. The buyer's preparation decision is optimal at its price information set.
2. The resulting conditional target payoff equals the price conditional on order flow.
3. Positive-price and zero-price regions do not accidentally collide; any collision is treated as one actual price preimage.
4. Every unilateral investor deviation is evaluated against the entire fixed price and preparation schedule.

Average price equal to average payoff is a necessary identity, not enough. An incorrect pointwise price schedule can pass that average check.

### 7.5 Search coverage for the polish release

Implement explicit candidate evaluation for alternative lower-tail pool cutoffs at fixed orders, including the exact test family below. A finite cutoff scan is useful but is not a complete search over all measurable pool sets. Record `pricing_family_coverage` and `exhaustive_pricing_search = false` unless a separate exhaustive argument justifies more.

For general pure or mixed orders whose posterior is not monotone, do not assert that every pool is a lower interval. Support explicit unions of intervals or keep the unsearched alternatives marked open. No complete pricing-correspondence theorem is required in this release.

**Acceptance:** both endpoints of the regression family survive validation and deduplication; invalid controls fail for the correct economic reasons; the existing positive-floor benchmark is unchanged.

---

## 8. Required regression: identical orders, distinct rational price pools

This section is self-contained. It is the smallest mandatory test for the repaired continuation representation. It also supplies the result to be written in a new online appendix subsection, with a concise argument in the paper's seller appendix.

### 8.1 Inputs and institution

Use the existing benchmark, changing only reserve and holding incumbent strength as follows:

```text
h = 10; ell = 1; r = 1.2; p = 7;
rho = 0.25; c_L = 1; c_H = 6;
b = 2; k = 0.02; prior_H = 0.5;
q_H = 1; q_L = -1;
entry_at_indifference = yes;
bid_equal_reserve_is_admissible = yes.
```

Both the incumbent and low-value challenger are excluded by the reserve. The exact auction objects are

$$
t_0=t_L=g_L=0,\qquad t_H=7,\qquad g_H=3.
$$

This is the expanded reserve domain, not the benchmark support $p<\ell$. Do not run it through a payoff function that assumes $p<\ell$.

### 8.2 Conditional densities and observed-price policy

Let

$$
f(z)=\frac14e^{-|z|/2},\quad
 a_H(x)=f(x-1),\quad a_L(x)=f(x+1),
$$

$$
\mu_X(x)=\frac{a_H(x)}{a_H(x)+a_L(x)}
=\left[1+\exp\left\{-\frac{|x+1|-|x-1|}{2}\right\}\right]^{-1}.
$$

For each $c\in[-\log 2,0]$, define

$$
P_c(x)=
\begin{cases}
0,&x<c,\\
\frac74\mu_X(x),&x\ge c.
\end{cases}
$$

At price zero, neither cost type prepares. At every positive price, the low-cost type prepares and the high-cost type does not. The upper posterior plateau is also an actual positive-price atom; it must be conditioned on correctly.

### 8.3 Buyer validation from the actual price

Here $F_Z$ denotes the noise **CDF**, not its survival function:

$$
F_Z(z)=
\begin{cases}
\frac12e^{z/2},&z\le0,\\
1-\frac12e^{-z/2},&z>0.
\end{cases}
$$

The zero-price posterior is

$$
\bar\mu_c=\frac{F_Z(c-1)}{F_Z(c-1)+F_Z(c+1)}.
$$

For the declared cutoff family,

$$
\bar\mu_c\le\bar\mu_0=\tfrac12e^{-1/2}<\tfrac13.
$$

Consequently $3\bar\mu_c<1$, so zero-price nonpreparation is strictly optimal. At positive prices,

$$
\mu_X(x)\ge\mu_X(-\log2)=\tfrac13,
$$

which supports low-cost preparation under the equality convention. High-cost preparation is impossible because gross profit is at most $3$, below $6$.

For $c=0$, raw flow posteriors on $(-\log2,0)$ would justify preparation if individually observed, but those flows are **not individually observed**. They produce price zero and the pooled posterior governs the buyer's action. This is a critical regression assertion.

### 8.4 Conditional pricing

For $x<c$, no entrant is prepared and no bidder meets the reserve, so expected terminal value is zero. For $x\ge c$, preparation occurs with probability $\rho$, and a sale at $p$ occurs only in state $H$. Thus

$$
\mathbb E[V_T\mid X=x]=\rho p\mu_X(x)=\tfrac74\mu_X(x).
$$

The proposed rule satisfies conditional competitive pricing in both regions. Do not argue from only the unconditional average.

### 8.5 Global investor validation

The correctly signed residual advantages are

$$
A_H(x)=\rho p[1-\mu_X(x)]\mathbf1\{x\ge c\},\qquad
A_L(x)=\rho p\mu_X(x)\mathbf1\{x\ge c\}.
$$

They vanish in the price pool and are nonnegative elsewhere. Against each complete candidate schedule, define

$$
J_c=F_H(1)=F_L(1).
$$

Bayes' rule gives this equality pointwise inside the integral. The Laplace density-ratio bound yields

$$
F_\theta(s)\ge e^{-(1-s)/b}J_c,\qquad
|F_\theta'(s)|\le F_\theta(s)/b,
$$

and therefore

$$
U_\theta'(s)\ge(1-1/b)J_c-k.
$$

Every declared pool leaves $x\ge1$ active. On that region $1-\mu_X=m=(1+e)^{-1}>1/4$, and its high-state probability is $1/2$. Hence

$$
J_c\ge\frac{\rho p m}{2}>\frac7{32},\qquad
U_\theta'(s)>\frac7{64}-\frac1{50}=\frac{143}{1600}>0
$$

for every $s\in[0,1]$ and both types. Wrong-signed orders are dominated by zero. This supplies **analytical existence** for the whole cutoff family, with globally optimal full orders against each price rule. It does not establish uniqueness of that family within the entire reserve game.

A positive derivative found on a finite grid is not the proof. The common rational lower bound above is the proof; integrations and meshes check its implementation.

### 8.6 Output quantities

Write $S_Z=1-F_Z$. Then

$$
\Pr(P=0)=\frac{F_Z(c-1)+F_Z(c+1)}2,
$$

$$
\mathsf E_c=\frac\rho2\{S_Z(c-1)+S_Z(c+1)\},
\qquad
\Pr(\text{sale})=\frac\rho2S_Z(c-1),
$$

$$
\mathcal R_{T,c}=\frac{\rho p}{2}S_Z(c-1),
\qquad \Pr(\text{two admissible bidders})=0.
$$

The required endpoint landmarks are:

| Cutoff | Pool posterior | Preparation | Sale | Seller revenue |
|---|---:|---:|---:|---:|
| $-\log2$ | 0.2729788130 | 0.1518051214 | 0.0981948786 | 0.6873641502 |
| $0$ | 0.3032653299 | 0.1250000000 | 0.0870918338 | 0.6096428364 |

Recompute these through both closed forms and independent conditional integration. Preserve CDF versus survival notation explicitly.

### 8.7 Positive and negative acceptance tests

Run the endpoints and the seventeen-cutoff grid

$$
c_j=-\log2\left(1-\frac{j}{16}\right),\qquad j=0,\ldots,16.
$$

Require every grid member to pass price, buyer, and global-investor validation. Require preparation and revenue to decrease as the cutoff increases over this grid. That ordered numerical check is not a new continuum theorem.

Negative controls must fail as follows:

- **Cutoff $c=-1$:** some positive prices imply $3\mu_X<1$, so prescribed low-cost preparation is not optimal.
- **Cutoff $c=1$:** the zero-price pooled posterior makes low-cost preparation profitable, so prescribed nonpreparation fails.
- **Incorrect raw-posterior buyer inside the $c=0$ pool:** the altered policy is rejected as inconsistent with the specified observed-price information structure.
- **Deduplication by orders alone:** a test must expose that it incorrectly merges the two valid endpoint continuations.

Export a regression table with complete parameters, cutoff, price-pool mass, both state masses, pooled posterior, buyer slacks, global bound, preparation, sale, admissible challenger probability, two-bidder probability, revenue, and validation status. Store negative-control failure reasons as expected failures, not accepted rows.

### 8.8 Manuscript placement

Add a short paragraph to the seller discussion and a concise derivation in the paper appendix. Put the full argument above in an online subsection titled **“Price pooling when preparation can vanish.”** Label the formal online result analytical after its local proof and implementation checks pass.

Do not promote this example into the new headline or claim novelty for price-pooling multiplicity itself. Its role is to specify the continuation correspondence the seller must face and to discipline the numerical exercise.

---

## 9. Required regression: exact reserve events and admissible-bid outcomes

### 9.1 Add events, not only grid points

Retain the declared reserve grid but augment it with all known relevant support and participation events. At minimum include:

$$
0,\ \ell,\ r,\ h;
\qquad
\ell\pm\varepsilon_V,\ h\pm\varepsilon_V
$$

where applicable, the declared reserve alternatives, and the exact $p_L,p_H$ below. Add valid one-sided offsets such as `1e-4`, `1e-6`, and `1e-8` to test regime classification. Do not assume the same continuation remains supported on both sides of an event.

A numerical tolerance for residual acceptance is not a rule for treating all nearby inequalities as equality. For a non-event input, evaluate the actual sign using adequate precision. If an interval straddles zero, refine or mark it unresolved. For an exact declared event, evaluate the defining identity algebraically and apply the explicit tie convention.

### 9.2 Weak-incumbent floor event

When the reserve exceeds incumbent support and excludes the low class,

$$
g_H=h-p,\quad g_L=0,\quad t_H=p,\quad t_0=t_L=0.
$$

The low-cost floor reaches equality at

$$
p_L=h-\frac{c_L}{m}.
$$

At the declared weak benchmark,

$$
p_L=6.2817181715\ldots,
\quad \mathsf E=\rho=0.25,
\quad \Pr(\mathrm{sale})=\frac\rho2=0.125,
\quad \mathcal R_T=\frac{\rho p_L}{2}=0.7852147714\ldots.
$$

Check the payoff regime, all cost comparisons, and the positive full-order derivative margin. The equality $B(m)=c_L$ is admitted under the stated tie rule. Do not say this point satisfies the benchmark's **strict** low-cost inequality: support it by the same inversion/global-bound proof using $e\ge\rho$ under equality. Record it as an analytically supported event candidate, not as an interior point of an open strict-inequality region.

### 9.3 Strong-incumbent expensive-entry event

With the low class excluded and $\ell<p<r$,

$$
g_H=h-\frac r2-\frac{p^2}{2r},\qquad g_L=0.
$$

The upper-posterior entry event is

$$
M\left(h-\frac r2-\frac{p_H^2}{2r}\right)=c_H,
\qquad
p_H=\sqrt{2r(h-c_H/M)-r^2}.
$$

At the declared strong benchmark,

$$
p_H=1.3252698283\ldots.
$$

Evaluate the event as $\tau=M$ and $x^*=1$, so

$$
\alpha_H=\frac12,\qquad
\alpha_L=\frac12e^{-2/b},
$$

$$
\mathsf E=0.5064773952\ldots,
\qquad \mathcal R_T=1.0688544444\ldots.
$$

The plateau has positive probability. Entry-at-indifference admits the expensive type there. Check the strictly positive low-cost floor and global full-order bound separately from this equality. Record exact event identity, not merely a rounded reserve and an accidental floating-point comparison.

### 9.4 Atomless-class version

The same event formulas apply to the declared narrow class-value economy only after verifying that the low band is entirely excluded and the high band lies entirely above the reserve and incumbent support. In that region, the class mean $h$ determines $g_H$, and $t_H$ has the same formula. Similar-looking binary and class outcomes there need not be a copy error.

For reserves inside a value band, integrate the actual value distribution. The event formulas above are not generic shortcuts for those rows.

### 9.5 Preparation is not synonymous with two admissible bidders

Add the following numerical quantities to reserve outputs. Let $I$ indicate that the challenger pays for preparation, and let $V$ be its realized value after preparation:

$$
\begin{aligned}
\mathsf E&=\Pr(I=1),\\
\mathsf A&=\Pr(I=1,V\ge p),\\
\mathsf S&=\Pr(R\ge p\ \text{or}\ [I=1,V\ge p]),\\
\mathsf C_2&=\Pr(R\ge p,I=1,V\ge p).
\end{aligned}
$$

Here $\mathsf A$ is admissible-challenger probability, $\mathsf S$ is sale probability, and $\mathsf C_2$ is the probability of two admissible bidders. Avoid notation collisions in the final paper; these symbols need not become new main-text primitives if the measures remain online.

Validate

$$
\mathsf S=\Pr(R\ge p)+\mathsf A-\mathsf C_2,
\qquad
0\le\mathsf C_2\le\mathsf A\le\mathsf E\le1,
\qquad 0\le\mathsf S\le1.
$$

Compute high-value challenger ownership from the actual allocation event. Outside the original support, do not automatically use $e_H/2$ if a high-class value can fail the reserve or lose to the incumbent.

At the published sampled weak reserve `6.280`, require `E = 0.25`, `sale = 0.125`, `two_admissible = 0`, and seller revenue `0.785`. At the exact floor event the same probabilities hold with the event revenue above. This test prevents relabeling preparation as increased competition when the incumbent is excluded.

### 9.6 Search and reporting limits

The exact event candidates improve the published sampled maxima. They do not prove global optimality, envelope completeness, or a seller's chosen continuation. Keep the selected maxima and coverage counts out of the main paper; place any audited updates in the online numerical-results subsection.

If optional reserve exploration remains in the release, rerun it with repaired continuation identity and event coverage. Compute counts from the actual attempt/validation ledger, not a hard-coded grid length. Distinguish rejected candidates, unresolved searches, no candidates found, and analytically established nonexistence. Do not infer the last from any of the first three.

---

## 10. Task S3 — Audit the new correspondence and reserve corpus

The preserved verification seed establishes selected nodes. It does not independently clear the assembled repository's wider curves, mixed-support attempts, or reserve summaries. Audit the actual implementation.

### 10.1 Source inspection priorities

Inspect at least:

1. Full-domain auction-payoff routines, including value/reserve equalities and within-band integration.
2. Conditional density and posterior construction for pure, asymmetric, and mixed orders.
3. State-conditioned signal entry and pricing.
4. Price pooling, atom conditioning, and continuation deduplication.
5. Correct separation of the unilateral order derivative from a change in a candidate profile.
6. Global or numerically refined best-response checks, including wrong-signed orders.
7. The support-indifference and off-support checks for mixed candidates.
8. Tail/error bounds, integration breakpoints, warnings, and retry behavior.
9. Full-parameter joins from accepted rows to registry and figure data.
10. Equality/event handling and the final status/classification logic.

Do not rewrite an otherwise sound numerical stack. Patch the incorrect component, add a regression that fails before the patch, and rerun its dependents.

### 10.2 Validate every displayed correspondence row

For each plotted candidate, require an immutable complete input declaration, a complete continuation identity, conditional pricing and preparation checks, and investor best responses over the full allowed order interval. A finite-grid check remains a numerical diagnostic unless an analytical or interval cover closes between-grid deviations.

Where the low-type Stieltjes concavity lemma applies, use it correctly. It requires a bounded nondecreasing residual; do not import it into a nonmonotone mixed profile without checking that property.

Where the high-type marginal-profit certificate fails, do not reject automatically: a positive derivative is sufficient, not necessary, for a boundary optimum. Evaluate the global payoff gap with justified coverage, or leave the candidate's status diagnostic/open. Preserve a found profitable deviation as a witness.

Every connected plotted line must be supported by accepted nodes and must break at discontinuities, changed branch identities, or unresolved gaps. Certified endpoints do not certify the intervening line. Multiplicity shading means **distinct continuations found**, not exhaustive knowledge of the equilibrium set.

### 10.3 Mixed profiles

For every positive-weight support action, record its payoff and gap to the best tested or enclosed deviation. Check the probability simplex and support bounds. Candidate schedules are recomputed once per candidate and then held fixed during unilateral deviations.

“No mixed equilibrium found” is allowed only if the release includes the actual search domains, supports, starts, stopping conditions, and attempt records. It is never a nonexistence theorem. If those records are missing, remove that sentence from the peer PDFs and state only that the complete correspondence is open.

### 10.4 Bounded scope for optional re-exploration

Do not spend the entire revision on a new global equilibrium algorithm. After the required core tests and price-pool/event regressions:

- Reproduce existing displayed exploratory rows and local boundary neighborhoods.
- Repair identified errors and rerun affected rows.
- Rebuild the retained figure from accepted evidence.
- If a broader sweep remains unreliable or unauditable, apply the controlled fallback in §3.2.

The full search over arbitrary price pools, all mixed supports, and globally optimal reserves belongs to the next research phase. A more modest audited display is preferable to an apparently complete but unsupported curve.

---
## 11. Task S4 — Rewrite the reader's entry into the paper

### 11.1 Replacement abstract

Use the following as the target abstract, with only edits needed to fit the house style. It avoids incidental numerical results and keeps the fixed-information contrast explicit:

> A stronger incumbent bidder can attract a challenger by making the target's stock price more informative. We study a takeover auction in which a prospective buyer observes the price before committing to acquisition preparation. Stronger competition lowers the buyer's acquisition profit at every fixed belief but increases the sensitivity of target shareholders' proceeds to its value. This raises the incentive to trade information about the challenger. On an open set of primitives, strengthening the incumbent changes uninformative prices into informative prices, with unique trading and on-path preparation outcomes in each economy. Challenger participation and high-value challenger ownership increase. Holding the price experiment fixed restores deterrence. The reversal also arises when the buyer has a more accurate private signal than the investor. The mechanism connects acquisition payments to the information that brings buyers into a takeover contest.

Count the final abstract mechanically and enforce the original ceiling of 150 words. Do not add a separate caveat paragraph or preview every robustness result. The open-set claim must remain tied to the established primitive region.

### 11.2 Introduction: order the argument, do not list the audit

Reorganize the existing introduction into this sequence. A practical target is roughly 1,000–1,400 words, but clarity and the existing style take precedence over an exact count.

**Opening:** state the fixed-information deterrence force, then the reversal. Replace “usually deters” because it reads as an unsupported empirical frequency claim.

Suggested opening:

> At fixed information, a stronger incumbent reduces a prospective challenger's expected return from entering a takeover contest. We study a force in the opposite direction: competition can make the target's stock more informative about the challenger. When a potential buyer observes that price before committing to acquisition preparation, the information effect can outweigh the loss of acquisition profits.

Reuse the existing `Fishman1988` and `HirshleiferPng1989` citations for the described deterrence/participation literature; do not insert a new factual claim about how frequently deterrence occurs.

**Economic engine:** distinguish the acquisition claim from the traded claim. Explain the auction payments before explaining Laplace noise, mixed strategies, or certificates. Correct the high-quality payment to **the larger of the reserve and the incumbent's bid**. For a low-quality challenger, explain separately when it wins and when its bid sets the incumbent's payment.

**Complementary information:** introduce the interpretation immediately, without changing the simple benchmark. Use the following paragraph or a faithful concise version:

> The relevant information is complementary rather than necessarily superior. A prospective buyer may know its integration capabilities while investors specializing in the target hold different information about customers, technology, or product demand. The stock price can add to the buyer's assessment before it commits resources to an executable acquisition proposal. We first isolate the mechanism with a perfectly informed investor and an initially uninformed challenger, then establish the reversal with distinct imperfect signals, including a buyer signal that is more accurate than the investor's.

The customer/technology examples are interpretations, not verified facts about a specific transaction. Avoid language suggesting that the noisy binary signals literally decompose value into additive integration and product-demand components; they are different signals about the modeled match value.

**Institution:** describe the public, still-contestable decision interval, then the simple model's timing. Separate a public distribution of incumbent strength from a strategically chosen incumbent bid. In this model the realized bid is not the primitive being varied.

**Main result:** preview the unique-outcome weak/strong comparison and the fixed-experiment control. State that rational prices anticipate the entry response. One sentence about continuous deviations and mixed strategies is enough here; the argument appears later.

**Scope and implications:** summarize complementary information, selected coexistence, and the fixed-strength surplus result. Mention the finite decline at a further strength only as an implication; do not organize the paper around a hump or announce complete activation thresholds.

**Seller question:** frame sale design as the next theorem: terms shape both acquisition payments and the information available before participation. Say that its continuation includes price rules as well as orders. Do not lead with the largest sampled reserve or unresolved-node counts.

**Literature and road map:** keep the central contrast with Dow–Goldstein–Guembel, followed by auction entry, information acquisition, and M&A feedback. Use prose rather than a long contribution checklist. Describe the increment as the acquisition-derived opposition and participation reversal, not generic market learning.

### 11.3 Add a compact institutional subsection

Add a titled subsection **“The decision interval”** near the end of the opening motivation or immediately before the model. Prefer a subsection within the introduction so the existing main section numbers need not all shift.

It must answer these questions in approximately three or four paragraphs:

1. What sale opportunity is publicly understood while the target still trades?
2. Which buyer is already prepared, and which preparation decision remains open?
3. What can the outside investor know that is not fully contained in the buyer's information?
4. Why must a buyer incur preparation costs before making an executable bid?
5. What does the public incumbent distribution represent, as distinct from a realized public bid?

The institution is a publicly visible and contestable opportunity involving a listed target. A disclosed approach, public strategic review, or open contest can fit; none qualifies automatically. A wholly confidential process whose existence becomes public only after the buyer set is fixed is not established evidence for this timing.

Retain the Imprivata example only for the separation of approach, outreach, and diligence-contingent proposals. Keep the statement that it does not establish price-driven entry. Do not perform a new case search or populate the empirical pilot in this revision. A future descriptive chronology is a research task, not a missing numerical placeholder to invent.

**Acceptance:** an informed reader should understand the sequence and the complementary-information interpretation before encountering condition (A3).

---

## 12. Task S4 — Make the main model self-contained

### 12.1 Add the omitted model restrictions explicitly

Insert a compact paragraph in Section 2, adapted to the author's voice:

> All strategic agents are risk neutral. The target share is the only traded claim conveying information about the acquisition match in the benchmark, and neither bidder trades it. The investor has no control rights and cannot acquire the target. The sale mechanism binds all target shares, so shareholder tendering and holdout are outside the modeled continuation. The incumbent's value distribution is public, conditional on the information available when the sale opportunity becomes visible, but its realized value is not disclosed to the challenger before preparation.

This aligns the main model with OA A.1. It does not introduce a second stock, bidder toeholds, legal conclusions, or an unexplained contracting restriction.

### 12.2 Clarify preparation

Immediately after “Paying C reveals theta and permits bidding,” state:

> Preparation is required to submit an executable acquisition proposal. The cost represents verification and transaction preparation as well as learning; a buyer that declines it does not submit an uninformed bid based on its current expected value.

Do not call $C$ solely the optional purchase price of a research report. Do not allow a no-preparation bidding action in code unless explicitly developing a different model outside this revision.

Clarify that there is **one challenger with a realized cost**, not simultaneously a low-cost buyer and a high-cost buyer. Keep cost independent of values and information in the benchmark.

### 12.3 Clarify the trading wedge

Identify $k|q|$ as a separate trading or position-carrying wedge. The adverse-selection price impact is already generated by the competitive pricing rule. Do not describe $k$ as that same spread again. The order bound is a normalized small trading unit, not ownership of the whole target.

### 12.4 Explain the participation floor at (A1)

Use a short economic explanation beside the formal conditions:

> Some preparation-cost realizations make investigation worthwhile even after an unfavorable price. Their participation makes the target's proceeds sensitive to challenger quality before favorable information recruits additional preparation. This supplies a base return to revealing that quality through trading. Without any such participation or another source of state-sensitive target value, no preparation and no informative trading can remain mutually consistent.

Do not imply that a positive floor is an innocuous numerical regularizer. Do not change $\rho$ in the calibration to make the explanation sound more plausible.

### 12.5 Preserve complete information sets

State the chronology unambiguously. The market maker observes aggregate flow; the challenger observes price and its cost, and in the extension its own private signal. The investor does not observe the buyer's private signal. The incumbent's actual value is not publicly disclosed before preparation.

A unilateral investor deviation changes the distribution of flow reaching a **fixed candidate price and preparation schedule**. A comparison across economies re-solves the schedule. Make that distinction once clearly in the equilibrium definition and use it consistently in every proof and validator.

### 12.6 Wording of unique outcomes

Search the abstract, introduction, result previews, captions, table notes, and conclusion for “unique equilibrium.” Replace overbroad uses with the precise trading/on-path preparation scope. Retain correctly qualified uniqueness statements in the propositions.

Do not replace “unique” with “one possible” in a region where the proof actually establishes uniqueness. Precision is not blanket hedging.

---

## 13. Task S4 — Reorganize and check the proofs

### 13.1 Three-tier placement

**Main text:** show the acquisition-payoff opposition, the price inversion, the residual-profit identities, the main statement and its economic logic, and selected numerical evidence. These are the essential mechanism, not dispensable technicalities.

**Paper appendix:** provide the complete chain of steps and inequalities for every result stated in the paper, with definitions adjacent to the statement or proof. A referee must not need the online appendix merely to learn what a symbol means or find the central inequality.

**Online appendix:** retain the probability-space construction, regular conditional distributions, null-set equivalence under deviations, convolution regularity, Stieltjes argument, interval endpoint ordering, complete signal laws, exact integration methods, and numerical definitions.

Do not abbreviate a central proof with “standard arguments.” Do not copy the entire online appendix into the paper to avoid making placement decisions.

### 13.2 Recommended paper-appendix order

Use the following order, preserving internal result labels and updating cross-references mechanically:

| Subsection | Contents |
|---|---|
| A.1 Acquisition payoffs and Bayesian pricing | Proposition 1; posterior-bound and price-sufficiency supporting statements and short arguments. |
| A.2 Global trading and the main comparison | Convolution bound; complete main proof; fixed-experiment proposition; threshold distinctions and the further-strength comparison. |
| A.3 Certified asymmetric equilibria | Root definition; low-type concavity; interval signs; high-type cover; no-trade coexistence. |
| A.4 Distributional extensions and nonemptiness | Logistic density and inverse; atomless-cost conditions; moderate-value construction. |
| A.5 Complementary private information | Definitions, full statement, and compact complete proof together. |
| A.6 Bargaining and access to prices | Institution-specific transfer derivation, then the matched conditional-surplus proof. |
| A.7 Seller continuation | Full-domain payoffs; complete continuation object; price-pool argument; selected-continuation objective and local regularity conditions. |
| A.8 Numerical parameter declarations | Exact vectors for each separate exercise. |

The displayed proposition numbers can remain Proposition 1–3 and A.1–A.9 even when their location changes. Do not let subsection renumbering create accidental changes in theorem identity. Maintain an explicit old-to-new reference map and validate every use.

### 13.3 Required checks for each proof unit

**Payoff opposition.** Retain the reserve in the winning payment. Show the pointwise high–low difference and the two integral representations. Make clear that distributional generality is conditional on the given sale institution.

**Posterior bound.** Apply the density-ratio inequality to arbitrary conditional mixtures, then use conditional expectation to carry the bound to price information. Do not assume monotone pure strategies in this step.

**Price sufficiency.** Establish the low-cost floor before dividing by the coefficient. Derive inversion from conditional pricing, then recover the buyer's posterior by the tower property. Construct a strictly increasing price in the posterior, allowing jumps and posterior plateaus.

**Residual profits.** Subtract the rational price after incorporating preparation. Keep no-entry proceeds and the public entry effect in the calculation until they cancel. Do not attach an extra unanticipated premium.

**Global order bound.** State the translated-density integral, the integrability condition for Fubini, absolute continuity, and the inequality on its derivative. Explain why a jump in entry does not require differentiating entry during an individual deviation. The online appendix retains the full $W^{1,1}$ and null-set details.

**Main equilibrium.** Distinguish necessity from construction. Excluding every competing order profile is not, by itself, an existence proof; constructing prices and preparation under the forced profile supplies existence. Keep the further-strength conditions separate from (A1)–(A3).

**Thresholds.** Preserve the separate meanings of pooling existence, sufficient pooling uniqueness, sufficient full-order uniqueness, and the high-cost posterior ceiling. Their maintained domain must be visible. Equality on the Laplace plateau follows the stated tie rule.

**Asymmetric certificates.** Keep the unilateral derivative separate from changing the candidate magnitude. Include root-sign enclosures and the uniform high-type lower bound in the paper appendix. The proof uses the entire bracket and between-grid cover. Full antiderivatives and endpoint-order regularity remain online.

**Distributional extensions.** Put $f_{\log}$, $m,M$, $\tau$, the inverse formula, and support conditions near their result. Logistic and Laplace at common scale are not claimed to have common variance or a Blackwell order.

**Complementary signals.** The paper appendix must explicitly show:

$$
\Theta\perp X\mid T,\qquad Y\perp X\mid\Theta,
$$

$$
\mu_X=(1-a)+(2a-1)\lambda_X,
\quad
\Pr(H\mid P,Y=y)=\phi_y(\mu_P),
$$

$$
e_H\ge e_L\ge\rho,
\qquad
D=e_Hw_H-e_Lw_L\ge\rho\Delta_T>0,
$$

$$
P=t_0+e_L(P)w_L+\mu_XD(P),
$$

and the appropriate investor residuals and upper/lower bounds. Then give the weak exclusion, strong global derivative inequality, construction, and positive-probability additional preparation event. Define $\phi_y,\mu_-,\mu_+,w_H,w_L,D$ before they appear in the proposition. Do not reuse the benchmark's common state-independent preparation rate in this extension.

**Bargaining.** State verifiable values, enforceable runner-up fallback, zero-reserve no-entry payoff, and seller bargaining weight. The boundary at one-half is a result of this institution. Do not describe it as a solved private-value first-price or bargaining/trading equilibrium.

**Welfare.** Use a matched fixed-strength information-access comparison, preserve the same trading-cost realization, and distinguish transfer payments from allocation surplus. Change “every additional entrant contributes at least” to **“each additional preparation decision contributes at least that amount in conditional expectation, given price information and preparation cost.”** Realized low-value preparation need not generate a positive realized net gain.

### 13.4 Clarify the fixed-information proposition

Choose the minimal correction consistent with the benchmark: state explicitly that preparation cost remains independent of the signal and quality, and hold the signal–quality experiment and cost law fixed as strength varies. The buyer's posterior is then $\Pr(H\mid S)$, and the pointwise comparison is valid.

Do not leave a statement claiming arbitrary dependence among signal, quality, and observed cost while conditioning only on the signal. A generalized correlated-cost version would require $\Pr(H\mid S,C)$ and independence of incumbent value from the buyer's full information. That further generalization is not required for this release.

### 13.5 Online appendix changes

Retain existing full proof content unless it duplicates a now-central definition. Add the complete price-pooling example and exact reserve-event treatment to the sale-design portion. Amend OA C.6 to require complete pricing continuations and actual pooled beliefs. Add the new data fields and tests to the numerical specifications.

Condense the long printed scalar registry into a concise quantity-definition and provenance subsection. Preserve the **complete registry and every key definition** in a generated `replication/quantity_dictionary.md` and machine-readable manifest distributed with the paper. The online PDF must still define every mathematical object, input vector, computation, and acceptance rule needed to implement the exercises. A companion file is a lookup convenience, not permission to omit the model or the numerical recipe.

Replace stale future-tense production instructions where an exercise has actually been run with an accurate description of its method and output. Keep the empirical pilot in future tense. Do not rewrite unexecuted searches as completed work.

---

## 14. Task S5 — Tables, figures, and numerical communication

### 14.1 General data rule

Every table cell and plotted coordinate must come from a validated row or an exact analytical expression with recorded inputs. Do not read values from a plot image. Do not join solely by rounded $r$, rounded $p$, or a short experiment name.

At minimum, a displayed numerical row identifies the full parameter set, institution, noise law, cost law, information structure, tie convention, experiment role, and complete continuation. Mixed strategies and price-pool rules require separate referenced records.

### 14.2 Table 1 — acquisition primitives

Retain the existing table and checked values. Define units as incremental value per target share. Distinguish $\Delta_T$ from total merger value and from the trader's expected profit. Retain the comparison to independent auction integration. Do not fill an unexecuted numerical-agreement claim from the review's run; the local run must supply its own check.

### 14.3 Table 2 — make the control visible without widening the main table

**Default edit:** remove the two redundant matched-dividend rows from Panel B. Retain the frozen-profile and price-hidden rows, the fixed-strength welfare panel, and the explanation of the matched-dividend control in Section 6.1.

Add a compact **online** matched-price panel with:

```text
environment, mean_financial_price, seller_revenue,
external_dividend, preparation_probability,
high_value_ownership_probability, net_acquisition_surplus
```

For the strong comparison require:

$$
D_0=\mathcal R_T^{\mathrm{feedback}}-\mathcal R_T^{\mathrm{hidden}},
$$

$$
\mathbb E[P^{\mathrm{matched}}]
=\mathcal R_T^{\mathrm{hidden}}+D_0
=\mathbb E[P^{\mathrm{feedback}}],
$$

while seller revenue, acquisition surplus, preparation, and investor residuals in the matched control remain those of the hidden-price environment.

**Forbidden fix:** changing the matched row's seller revenue to include the external dividend. The dividend is attached to the financial claim and is not paid by the bidder or available as a seller instrument.

Table notes must distinguish “analytical outcome” from “fixed-profile control”; do not call every table row a unique equilibrium. The strong frozen profile happens to coincide with the equilibrium but its role remains a control.

### 14.4 Table 3 — foreground the size of the economic comparison

Replace the main-table minimum theorem margin with **change in preparation, in percentage points**, calculated from the same validated probability rows. Keep weak/strong preparation and high-quality ownership where space permits. Preserve the complete individual margins and their minimum in the online table and numerical archive.

For every row,

$$
\Delta \mathsf E_{\mathrm{pp}}=100(\mathsf E_{\mathrm{strong}}-\mathsf E_{\mathrm{weak}}).
$$

Do not mix probability units, percentage points, and percentage changes. Keep distinct parameter vectors visible in the notes: the moderate-value and complementary-signal illustrations are not one joint robustness calibration.

Retain **all** twenty-five rows of the online accuracy grid, including negative comparisons and rows outside sufficient theorem conditions. A failed comparison condition is not an equilibrium rejection. A finite-check candidate remains diagnostic unless a separate analytical or interval validation supports a stronger classification.

### 14.5 Table 4 — supported reserve alternatives in the main paper

Move Panel C's selected exploratory maxima and its long coverage counts out of the main paper. Retain the binary and atomless-class fixed-reserve comparisons.

Default main columns:

```text
Economy and reserve | Preparation | Sale | Two admissible bidders |
Expected target proceeds | Trading outcome
```

Identify analytical support in the notes for the validated listed nodes. Retain order magnitudes, margins, evidence status, and complete parameters online. If the table becomes too wide, use panels or a landscape online table; do not shrink it into unreadability.

Define preparation probability explicitly. Use the actual sale and admissibility outcomes from §9.5. Do not describe an excluded incumbent plus one potentially admissible challenger as a contest between two admissible bidders.

If the exploratory reserve summary passes audit, report it online with exact-event candidates included. Its heading must read **“highest revenue among continuations found”** or equivalent, not “optimal reserve.” Search-unresolved counts and known limits accompany it. Remove all associated quantitative summary claims from both PDFs if this corpus is withheld under the controlled fallback.

### 14.6 Figure 1 — two returns

Keep the two-panel structure. Verify axis definitions, parameter values, posterior levels, and units. The curves concern acquisition-stage payoffs before financial-market equilibrium. Do not describe them as the full entry mechanism by themselves.

### 14.7 Figure 2 — equilibrium correspondence

Retain an audited correspondence figure only when each line has validated source rows. Otherwise use the core-only display specified in §3.2.

Required visual rules:

- Separate analytical uniqueness shading from shading indicating **found multiplicity; search not exhaustive**.
- Give analytical bounds their actual names: existence, sufficient uniqueness, and preparation feasibility are different concepts.
- Show selected computer-assisted nodes with interval bars even if visually tiny; do not exaggerate their width to make them visible.
- Use distinct line styles for numerical branches; no fitted line bridges unresolved gaps.
- Preserve all accepted distinct displayed branches, not only the branch with the headline sign.
- Where a plotting boundary has a positive-probability tie, show the value at equality consistently with the declared tie rule and distinguish one-sided limits.
- Do not relabel the sufficient full-order uniqueness threshold as the first existence of informative trade.

Caption language must distinguish established nodes, analytical regions, and numerical continuations. A caption footnote cannot repair a visually incorrect continuity or uniqueness claim.

### 14.8 Figure 3 — posterior tails

Change the logistic marker at zero threshold distance to a **closed point** at zero upper-tail mass in Panel A and at baseline preparation $\rho$ in Panel B. The bound is not attained as a posterior realization, but the tail-probability function is defined there.

At the Laplace endpoint, the plateau mass and preparation at equality remain positive under the tie rule. Preserve the distinction. State that common scale, not common variance, is held fixed. Do not describe this as a Blackwell ranking of the noise laws.

Validate the logistic standardized cutoff using the noise standard deviation $b\pi/\sqrt3$, not the aggregate-flow standard deviation. The current landmark is approximately `1.495369` noise standard deviations.

### 14.9 Figure 4 — bargaining

Retain the acquisition-stage interpretation. Plot the spread comparison and challenger profits under the specified institution, including the boundary at seller weight one-half. The log-profit panel must not attempt to plot zero as a finite logged value at seller weight one. Use the declared domain below one or show a separately labeled payment-stage limit where mathematically meaningful.

Do not attach a trading, preparation, or welfare conclusion that has not been derived for this bargaining game.

### 14.10 Typesetting and caption checks

Keep the existing restrained style. No in-figure titles; captions name the figure and explain its comparison. Retain `(a)` and `(b)` panel labels, readable axis labels, and consistent decimal formatting.

Keep the proposition opening and its conditions together using the actual typesetting system's page-space control. Do not introduce arbitrary manual line breaks throughout the manuscript. Avoid stranded headings, captions separated from their figure, and table notes running off the page.

Figure notes specify parameters, units, information regime, and evidentiary interpretation. Main-table notes should explain the economic distinction rather than list dozens of implementation counts. Detailed grids, retry histories, and tolerances belong online or in replication documentation.

---

## 15. Task S5 — Bibliography, cross-references, and empirical scaffold

### 15.1 Preserve and validate the bibliography

Use the existing bibliography as the starting point. Its reference copy contains the following keys; the local file may use a documented equivalent mapping:

```text
BettonEtAl2014                 BooneMulherin2007
BulowHuangKlemperer1999       CarlinEtAl2026
CornelliLi2002                DowGoldsteinGuembel2017
EdmansGoldsteinJiang2012      EdmansGoldsteinJiang2015
Fishman1988                  GentryStroup2019
GoldsteinGuembel2008         GrossmanHart1980
HirshleiferPng1989            Imprivata2016
LevinSmith1994               LinMaYangZhu2025
LiuBernhardt2022             Luo2005
PernoudGleyze2026            Persico2000
RobertsSweeting2013
```

Check that every in-text key resolves, every bibliography entry used in the paper is present, author names and titles render correctly, and no DOI is invented for a record without a verified DOI. Do not add new literature merely to lengthen the list.

If a bibliographic detail or asserted current version is changed, verify it against a primary author, publisher, DOI, or institutional record and preserve the retrieval date and evidence internally. A conference or repository posting date is not a manuscript revision date. If no new version is obtained, cite the known version instead of claiming to have cleared an unseen update.

Keep the comparison with the payment-methods paper about payment choice and learning within an initiated deal. Do not use criticism of another paper's proof as a novelty claim or insert the prior audit dispute into the manuscript.

### 15.2 Cross-reference validation

Use stable labels, not manually typed page numbers, for internal results, equations, tables, and figures. Check both the sources and the rendered PDFs after reorganization. In particular:

- Main result references still point to its own hypotheses and proof.
- Complementary-signal definitions precede their proposition.
- Every certificate reference points to actual enclosures and the global bound.
- Numerical parameter references point to the relocated exact declarations.
- The shortened registry points to a file included in the replication bundle.
- All new price-pooling and reserve-event references resolve in both appendices.

An online cross-reference must not be a substitute for the key argument required in the paper appendix.

### 15.3 Empirical scaffold

Keep the main empirical section short and aimed at observable implications. Maintain OA D's selection and coding design, including the distinction between occurrence dates and first-public dates. Remove wording that implies a sample has been assembled or any causal identification has been established.

No new empirical work is part of this fixing sprint. A missing empirical result is not a failed numerical build. The open empirical task is to establish the public, still-contestable decision interval before designing a causal or structural exercise.

---

## 16. Task S6 — Numerical provenance, registry, and build hardening

### 16.1 Complete output schemas

Extend the existing schemas rather than creating unjoined parallel files. Require either full columns or a foreign key to an immutable complete parameter declaration. The new fields needed for reserve/pricing work are:

```text
candidate_id, continuation_id, parameter_set_id, institution_id,
information_structure_id, order_rule_id, price_rule_id,
pricing_family_coverage, exhaustive_pricing_search,
pool_id, pool_set_definition, pool_cutoff_exact,
price_atom_value, state_H_pool_mass, state_L_pool_mass,
pool_probability, pool_posterior,
preparation_rule_id, tie_rule_id, event_id, event_defining_relation,
preparation_probability, admissible_challenger_probability,
sale_probability, two_admissible_bidders_probability,
high_value_ownership_probability, seller_revenue, mean_financial_price,
pricing_error, belief_error, entry_deviation_gain,
investor_deviation_gain_estimate, investor_deviation_gain_upper_bound,
error_budget, result_status, existence_scope, uniqueness_scope,
accepted, rejection_reason, unresolved_reason, run_id
```

Use explicit null/not-applicable semantics. An unavailable rigorous upper bound is not zero. A positive price atom in a flat posterior tail is not a no-entry pool. Store enough information to distinguish them.

The wide logical schema can be normalized into linked tables. Use actual identifiers and definitions, not an opaque hash with no accompanying content.

### 16.2 Registry invariants

The registry must enforce:

1. Unique keys and unambiguous source-row selection.
2. Exact parameter, institution, information, and continuation identity.
3. Required source row accepted under the evidence status appropriate to the claim.
4. Correct units: probability, percentage, percentage-point change, normalized value, bound, or exact input.
5. Outward rounding for enclosures and conservative rounding for one-sided bounds.
6. No unresolved placeholder in the peer-facing build.
7. No renderer-side replacement with cached or manually typed quantities.
8. No accidental dependence on decimal context inherited from module import order.

Test registry generation in a fresh process under several ambient decimal precisions. The generator must establish its own local context and produce invariant declared outputs. Record actual precision, not an unverified comment in a source file.

Add keys for newly displayed preparation changes, sale/admissibility measures, and any price-pool or event illustration inserted into the appendices. Keep old key aliases only where needed for compatibility; ambiguous or duplicate keys are a hard failure.

### 16.3 Clean and fresh-directory builds

Provide two commands or task-runner targets:

- **Peer release:** validate required calculations, generate registry/tables/figures, fill manuscripts, typeset, run final checks, and assemble deliverables.
- **Peer reproduce:** perform the same declared sequence in a fresh working/output directory without relying on untracked accepted results from the previous run.

Use the discovered existing commands. The OA's current presentation rebuild commands are not sufficient documentation of how to regenerate raw numerical exercises. Include the actual producer for every displayed exercise in `replication/README.md` and the run manifest.

Do not require byte-identical PDFs when the existing engine inserts documented timestamps, but do require identical canonical numerical outputs, exact input declarations, certificate validity, resolved references, and substantive extracted manuscript text. Record or fix reproducible metadata where feasible.

### 16.4 Negative tests for fail-fast behavior

In isolated temporary copies, deliberately introduce each of these errors and require rejection before a peer-facing PDF is released:

- Remove a required registry key.
- Duplicate a parameter/continuation row used by a scalar selector.
- Substitute the same $r$ row with a different cost or information structure.
- Mark an open candidate accepted without passing validation.
- Replace a certificate lower bound with an inward-rounded or zero-containing enclosure.
- Merge the two valid price-pool endpoints because orders match.
- Use raw $\mu_X$ for preparation inside a common zero-price pool.
- Treat the matched external dividend as seller revenue or welfare.
- Replace a logistic unattained threshold with a large finite number and falsely positive tail mass.
- Disable legacy assertions with optimized Python; the reference runner must refuse to run.
- Introduce NaN or infinity into an ordinary finite scalar field without an explicit mathematical endpoint tag.

These are tests of the validation boundary, not changes to the scientific inputs. Restore the unmodified source after each test and retain only the diagnostic logs.

### 16.5 Full PDF review

Render **every page** of both regenerated PDFs. Inspect contact sheets, then individual pages containing main statements, all tables and figures, certificate intervals, and new appendix material at reading resolution. Check:

- No clipped equations, labels, notes, or off-page content.
- No missing glyphs, black squares, unresolved citations, or `??` references.
- No literal `[[name]]` tokens or stale production instructions in peer-facing prose.
- Proposition openings and conditions remain together.
- Readable font sizes and consistent table/figure styles.
- Correct interval brackets, superscripts, signs, and scientific notation.
- Every caption describes the actual plotted object and evidentiary scope.
- Consistent author name, title, authorial voice, and revision metadata.
- Legible bibliography links and no accidental local filesystem paths in reader-facing text.

Compare targeted before/after pages, but do not demand pixel identity after justified reflow. Preserve screenshots of all corrected exhibits and a short page-by-page inspection log. Automated text-boundary detection supplements visual review; it does not replace it.

---

## 17. Concrete test catalogue

Implement these tests using the existing test framework or a small explicit validator. Do not add a large framework solely to satisfy the naming convention. The IDs appear in the machine-readable task matrix and completion report.

| Test | Required check | Failure condition |
|---|---|---|
| T01 | Reviewed baseline and current source provenance | Wrong file silently substituted; mismatch unexplained. |
| T02 | Main auction payoff integration at declared nodes | Independent outcome integral differs beyond budget. |
| T03 | Full-domain reserve/value cases and equality | Wrong regime, missing no-sale state, incorrect equality. |
| T04 | Density normalization and posterior tower identities | Probability or posterior errors exceed tolerance. |
| T05 | Benchmark price inversion | Buyer implicitly receives flow or inversion fails in claimed region. |
| T06 | Benchmark weak/strong/further-strength margins | Any required condition fails for an analytical classification. |
| T07 | Global and refined order deviations | A retained candidate has an unexplained profitable deviation. |
| T08 | Frozen-profile versus hidden-price controls | Frozen weak profile mislabeled equilibrium; hidden game not reoptimized. |
| T09 | External-dividend invariance | Dividend changes revenue, welfare, information, or investor residuals. |
| T10 | Conditional welfare identity | Paid cost selection ignored or fixed-strength comparison changed. |
| T11 | Logistic inverse, threshold and endpoint | Unattained bound yields false tail probability or wrong standardized distance. |
| T12 | Atomless preparation-cost CDF and paid costs | Mean cost multiplied by selected entry or atomic formula reused. |
| T13 | Moderate-value example | Original strict conditions or reported comparison fail. |
| T14 | Complementary-signal joint laws and residuals | Buyer-private information treated as public or conditional entry miscomputed. |
| T15 | Complete displayed accuracy grid | Negative or out-of-region rows dropped; status conflated with existence. |
| T16 | Three interval certificates | Root signs, bracket-wide cover, ordering, or pooling coexistence fail. |
| T17 | Certificate display rounding | Printed interval misses certified enclosure or bound rounds inward. |
| T18 | Valid fixed-order price-pool family | Any declared family member wrongly rejected or assigned a single canonical price rule. |
| T19 | Invalid price-pool controls | Cutoffs -1 or 1 accepted despite buyer deviation. |
| T20 | Continuation identity | Same orders/different pools incorrectly merged; duplicates inflate multiplicity. |
| T21 | Exact floor-event reserve | Rounded comparison chooses tie behavior or event mislabeled strict-interior. |
| T22 | Exact high-cost ceiling reserve | Plateau preparation at equality evaluated incorrectly. |
| T23 | Sale/admissible/competitive probabilities | Union identity, bounds, or high-reserve reference outcomes fail. |
| T24 | Every retained correspondence row | Missing source/inputs or unvalidated plotted candidate. |
| T25 | Mixed support indifference/off-support checks | Search result overstated; support payoff or normalization fails. |
| T26 | Reserve counts and found ranges | Counts hard-coded; unresolved treated as empty; global maximum inferred. |
| T27 | Registry uniqueness and full-row keys | Missing, duplicated, ambiguous, stale, or incorrectly classified scalar. |
| T28 | Citation and cross-reference graph | Missing key, broken link, wrong relocated proof. |
| T29 | Prose/scientific consistency | Global hump, overbroad uniqueness/welfare, invented evidence, or wrong voice. |
| T30 | Figures and tables | Wrong endpoints, units, branch connection, or matched quantity. |
| T31 | Fresh-directory reproduction | Depends on untracked prior results or undocumented producer commands. |
| T32 | Full rendered PDF inspection | Clipping, unresolved fields, unreadable exhibits, or orphaned statement. |
| T33 | Release package completeness and safety | Missing required files, secrets, caches, or undisclosed unsupported results. |

T24–T26 may be marked **not in peer release under the documented core-only scope**, never “passed,” if their exploratory material is withheld. All tests supporting retained content remain required. T18–T23 are mandatory small regressions regardless of whether a broad reserve sweep is shown.

---

## 18. Release checklist and deliverables

### 18.1 Peer-facing package

Produce a clean folder containing:

```text
peer_release/
    main.pdf
    online_appendix.pdf
    README.md
```

The README states the paper title, author, revision identifier/date, and how the two PDFs relate. It can identify the work as a theory working paper with an empirical design scaffold. Do not put an internal bug ledger, review exchange, or misleading “journal-ready” certification in this folder.

### 18.2 Source and replication package

Produce a separate archive containing the actual equivalents of:

```text
source_and_replication/
    main.md
    online_appendix.md
    references.bib
    source templates / styles needed by the existing build
    dependency lock or exact environment declarations
    numerical source and validation tests
    exact input declarations
    validated tables and figure data
    certificate inputs and full interval outputs
    quantity manifest / registry
    replication/
        README.md
        quantity_dictionary.md
        run_manifest.json
    verification/
        preserved reference seed or a clearly mapped reference location
    audit/peer_polish/
        completion_report.md
        issue_ledger.csv
        claim_ledger.csv
        source_output_map.csv
        relevant manifests and validation summaries
```

Do not include API keys, `.env` files, personal account credentials, virtual environments, unrelated research files, caches, or operating-system font files. The repository's failed candidates and logs should remain available in the research audit archive; a large optional exploratory archive can be separate from the compact peer package, but it must not be destroyed.

### 18.3 Completion report

The final local-agent response and report must state:

1. The actual repository revision and files changed.
2. Whether the release is the audited working-paper scope or the core-validated fallback.
3. Each issue ID completed, its exact source/output locations, and the passing test evidence.
4. What was moved from the main paper to the online appendix or replication package, and why.
5. The actual commands executed, numerical/certificate outcomes, and limits of any retained search.
6. Every discrepancy, failed attempt, unresolved node, or withheld corpus material relevant to the release.
7. The paths to the peer PDFs, editable sources, bibliography, and replication archive.
8. A small list of open research results—seller optimization, full correspondence, commitment—clearly separated from unresolved release defects.

Do not say “all tests passed” when tests were not run or exploratory material was removed instead. Report passed, failed, open, and not-in-release counts separately.

### 18.4 Definition of done

The revision is complete when a peer can read the paper's institutional question before its technical apparatus, verify the central theorem from the paper appendix, understand precisely what the figures establish, and reproduce every reported numerical illustration from the supplied source and manifests.

The release must pass the core proof/numerical gates, the new pricing/event regressions, source-to-display provenance, citation/reference checks, and visual inspection. It need not resolve the next research theorem.

**Final outcome:** a sendable working paper with a strong central claim, not an inflated claim, an unfinished build, or a large new modeling project disguised as polishing.

---

## Appendix I. Issue-to-edit map

These are stable work IDs for the local completion report. Use the detailed instructions above rather than treating the short descriptions as sufficient implementation recipes.

| ID | Baseline anchor | Required edit or action | Gate |
|---|---|---|---|
| P01 | Entire repository | Discover and snapshot authoritative source/build/data chain | G0 |
| P02 | All claims and captions | Create claim/status/uniqueness ledger | G1 |
| P03 | OA C.1, C.3, C.4 | Reproduce core scalars, controls, extensions, and complete signal grid | G1 |
| P04 | M Proposition 3; OA B | Compare local interval-certificate port with preserved seed | G1 |
| P05 | OA C.6; ER §3 | Add complete price-rule/pool continuation representation | G2 |
| P06 | ER §3 | Implement valid/invalid fixed-order pool regressions | G2 |
| P07 | OA C.6; ER §4.4 | Add exact reserve events and symbolic equality treatment | G2 |
| P08 | M Table 4; OA C.6 | Add preparation/sale/admissibility outcomes and checks | G2 |
| P09 | M Figure 2; OA C.2 | Audit all retained exploratory correspondence rows | G3 |
| P10 | M Table 4 Panel C | Audit reserve summaries or withhold them transparently | G3 |
| P11 | M p. 1 | Replace overloaded/overbroad abstract; enforce word ceiling | G4 |
| P12 | M pp. 2–5 | Reorder introduction; exact fixed-information opening | G4 |
| P13 | M pp. 2, 22 | Introduce complementary information and decision interval early | G4 |
| P14 | M p. 3 | Include the reserve in the high-challenger payment | G4 |
| P15 | M pp. 5–7 | State all model restrictions and preparation interpretation | G4 |
| P16 | M p. 13 | Explain the positive preparation floor economically | G4 |
| P17 | M Appendix A | Group definitions, statements, and proof steps | G4 |
| P18 | M p. 35 | Clarify cost independence in fixed-information proposition | G4 |
| P19 | M p. 38 | Correct welfare wording to conditional expectation | G4 |
| P20 | M Appendix A.5; OA A.10/C.6 | State joint price/trading correspondence; add proof and event notes | G4 |
| P21 | Both manuscripts | Restore plural voice and consistent status vocabulary | G4 |
| P22 | M Table 2 | Remove redundant dividend rows; add online matched-price panel | G5 |
| P23 | M Table 3 | Show entry change; preserve full margins and signal grid online | G5 |
| P24 | M Table 4 | Retain supported alternatives; move exploratory maxima online | G5 |
| P25 | M Figure 2 | Correct evidence shading, endpoints, labels, and gaps | G5 |
| P26 | M Figure 3 | Close the logistic endpoint and validate units | G5 |
| P27 | M Figure 4 | Preserve payment-stage scope and correct log endpoint | G5 |
| P28 | OA C.8 | Shorten printed registry; distribute full definitions | G5 |
| P29 | References and all labels | Verify key resolution and relocated proof references | G5 |
| P30 | OA E; local commands | Document actual raw numerical producers and clean build | G6 |
| P31 | Numerical validation boundary | Execute destructive-on-copy negative tests | G6 |
| P32 | Both rendered PDFs | Inspect every page and corrected exhibits | G6 |
| P33 | All final assets | Package peer files, sources, replication evidence, and truthful completion report | G7 |

---

## Appendix II. Starter instruction for the local executing agent

The author can paste the following instruction with the package available locally:

> Execute `CCC_Peer_Circulation_Fixing_Spec.md` end to end in the current manuscript repository. Read it fully before changing files. Discover the authoritative sources and build graph, preserve the starting state, and work through the gates in order. Keep the paper's title, mechanism, primitive vectors, and established result scopes. Reproduce the retained core results and certificate port; implement the fixed-order price-pool and exact-reserve-event regressions; audit the displayed search corpus or use only the explicitly authorized core-validated fallback. Apply the manuscript, proof-placement, table, figure, and bibliography edits in the spec. Rebuild from validated numerical outputs, inspect every PDF page, and deliver the peer PDFs plus complete source/replication package and completion report. Do not return merely a plan, silently suppress failures, choose a favorable branch, invent missing quantities, or attempt to solve the entire seller-optimal research program as a prerequisite to this release.

---

## Appendix III. Evidence and interpretation of this fixing package

This specification is based on the assembled PDFs, the author's build handoff, and the completed end-to-end review. It is an instruction for future local execution, not a claim that the local repository has already been patched or that its entire numerical layer has been rerun.

The companion `reference_oracles.py` was executed when preparing this package. It uses standard-library decimal arithmetic to evaluate selected baseline profiles, the complementary-signal example, the exact reserve events, and the price-pool family and invalid controls. Its outputs are in `oracle_run/oracle_results.json`. These are **numerical diagnostics for specified analytical constructions**, not new interval certificates or a port of the assembled solver.

The preserved review and seed archives contain their own historical execution records. Keep those records distinct from the local agent's new execution. The local agent must create fresh outputs and manifests rather than claiming the preserved results as its own rerun.

For traceability, the substantive instructions map to sources as follows:

- Scientific core and proof scope: M §§3–5 and Appendix A; OA A–B; ER §2.
- Complete pricing continuation and its analytical regression: ER §3; OA C.6's existing price-pool definitions.
- Exact reserve events and additional outcome measures: ER §§4.4 and 5.5; M Table 4 and Appendix A.5.
- Institutional and model clarifications: ER §§5–6; M §§1–2 and 5.3.
- Table, figure, and proof-placement edits: ER §6; the corresponding exhibits in M.
- Locked voice, status, proof tiers, numerical registry, and empirical scope: H, as made executable by this specification.

The editorial defaults—moving selected maxima online, replacing the main robustness margin column with an effect-size column, restoring plural voice, and shortening the printed registry—are decisions in this specification. They preserve the underlying results and evidence; they are not claims that the existing PDFs already implement those choices.
