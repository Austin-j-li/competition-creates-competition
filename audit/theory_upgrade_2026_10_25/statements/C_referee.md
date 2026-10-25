# C. Referee report on the research statements and the open proofs O1 (notation pass), O3, O4 and O8

Report of the referee to the coordinator, 25 October 2026. Under review: `statements/C.tex`, `statements/C_notes.md`, `statements/O1/` (the notation pass, referee fixes 3 to 5 and the boundary sentence added to `O1_notes.md`), `statements/O3/`, `statements/O4/` and `statements/O8/`. The referee wrote none of them. Sources read in full: `plan/PLAN.md` (Parts 2, 4 (S4, S5), 5, 6 and 8), `plan/DECISIONS.md`, `plan/NOTATION.md`, the referee reports `referee/W3.md` and `referee/W2.md`, the W2 and W3 sections and formal statements of `WORKAROUNDS.md`, `O1/O1_referee.md`, the research rows of `plan/lens_theory.md`, and the current `slot/manuscript/appendix/A5_research.tex`. Nothing under review was edited; the builds and computations ran in a private folder outside the repository.

## 1. Verdict

**Accept with listed fixes.** Every statement follows from the proofs of W3 and W2, and from O1, O3, O4 and O8, under exactly its stated hypotheses. No statement is wrong. One statement, the main-text form of Proposition 4, has a missing qualifier and a hypothesis that its full statement does not contain (issues C-01 and C-02). The remaining fixes are a misleading identity in O3, a false sentence about the derivative in O4, one uniqueness claim whose proof covers only part of the path, a duplicated equation label with two domains, and wording. There is no blocker.

The numbering is right: Proposition A.1 is the former Proposition A.2, as decision 7 and Part 6 of the plan imply (Section 4).

## 2. Verdicts on the statements

The rows follow the table of `C_notes.md`. "Accept" means every conclusion follows from the cited proofs under the stated hypotheses, every qualifier of the S4 acceptance list that applies is present, and nothing is overclaimed.

| Statement, label | Number | Verdict | Basis of the check |
|---|---|---|---|
| Joint deviations, `lem:a5-joint` | Lemma A.12 | accept | W3 §3: at fixed prices and preparation the deviation payoff is the concave quadratic; the minimum with the cap is the unique best choice under all four tie rules. |
| Bounds under every profile, `lem:a5-bounds` | Lemma A.13 | accept | Rechecked: nonzero-order posteriors in [m, M] for every β < 1/2; the zero-order lower bound b_0/(2b_0 + λ) ≥ m_λ holds exactly when b_0 ≥ b, that is β ≤ 1/3. Part (b): equal prices force equal preparation, hence equal entry, and with entry at least ρ > 0 and Δ_T > 0 competitive pricing then forces equal posteriors. |
| Positive research needs a strict full purchase, `lem:a5-buy` | Lemma A.14 | accept | W3 §1: entry at least ρ and posterior at most M_λ give U_H(1) ≥ ρΔ_T m_λ − k, so a profitable sale forces a profitable purchase; strict, so no tie rule is used; β < 1/2. |
| The low class's sale, `lem:a5-sale` | Lemma A.15 | accept | W3 eqs (1)–(3); agrees with `lem:a4-low` of `B.tex` at the prior 1/2 (its middle case b(πρΔ_T/k − 1)/(1 − π) equals b(ρΔ_T/k − 2)). Boundary choices at ρΔ_T = 2k and ρΔ_T m_λ = k as in W3 §2. See issue C-09. |
| Competition creates research, `prop:research` | Proposition 4, full | accept | (a) W3 eq (5); (b) W3 eqs (7)–(10) and W2 Shared Candidates 1 and 3 (class entry, share, pool, kernel with the atom and support qualifications); (c) W2 Shared Candidate 2 and the decisive-advantage proof; (d) O3 and O4. The default tie pair and the full-preparation selection are stated; strict and weak are separated in (b) and (c). See issues C-02 and C-11. |
| Ownership at the same incumbent, `par:a5-ownership-ratio` | paragraph | accept | W2, "the comparison equilibrium": zero research exists wherever ρΔ_T ≤ 2k, its ownership is ρW_H/2 at the boundary as well, and the ratio is e_H/ρ, strictly rising below the cap and constant at it. |
| The three research outcomes, `lem:a5-outcomes` | Lemma A.16 | accept | W3 Candidate 3, eqs (13)–(14), with the boundary family of O8. Rechecked the residual (1 − ρ)Δ_T m at the floor root, the clipping, the empty band when λ_Q ≥ cap, and existence including τ ≥ 1. |
| Strong incumbents, `lem:a5-strong` | Lemma A.17 | accept | The existing proof, read with the nonzero-order bounds only (β < 1/2 suffices); M at the cap ≠ τ removes the challenger tie. |
| Tie rules with research, `rem:researchties` | Remark A.1 | accept | W3 eqs (15)–(17). Rechecked: at e* = ρ the equation forces ρJ > k and λ_E = λ_Q, so the endpoint is floor-entry research at the threshold, as stated. The list is complete when an indifferent high-cost challenger may prepare with any probability. |
| Access to prices with research, `par:a5-access` | paragraph | accept | `scan/reduction_A3_A5.md` §3(f). Rechecked the surplus term: max{θ, R} − R·1{R ≥ p} = (θ − max{p, R})⁺ + p·1{R < p}, so the gain per recruited challenger is B(M) − c_H + pF(p) = γ(M − τ) + pF(p). The O4 program reproduces both displays at r_1. |
| Floor-entry research along the path, `lem:a5-floor` | Lemma A.18 | accept | O1, accepted, and its notation pass (Section 3). The C.tex wording matches the proof fragment's lemma. See issue C-07. |
| Research equilibria in the example, `cor:research` | Corollary 3, full | accept | W3's outcome list for the example, O1 parts (a)–(d), O3, O4, O8. Every interval endpoint is right: [r_R, r_N] closed (zero research exists at r_N with its strategy family; floor-entry research does not), (r_N, r_Q) open, [r_Q, r_C] closed, (r_C, r_2]. Part (b): at 1.55, 1.60, 1.65 ρΔ_T < 2k strictly, so zero research is one tuple and the count "exactly two" is right. See issue C-06 on the example paragraph. |
| The research cap and cost, `prop:researchregion` | Proposition A.1 | accept | The existing proof still holds under the three-outcome classification: uniqueness at r_1 and r_2 comes from condition (U), and floor-entry research cannot arise at the intermediate strengths because ρΔ_T < 2k there. The β endpoint 1/3 is recomputed in Section 6. See issue C-13. |
| Remark A.1 in the example, `rem:researchties-example` | Remark A.1, continued | accept | W3's section on the abstaining investor and the O4 output, parts 3–5: the gap (r_N, r_S] under an abstaining investor lies inside (r_N, r_Q), so floor-entry research is the unique equilibrium there; the pair at r = 2 has both trades strict. |
| Proposition 4, main-text form, `prop:research-short` | Proposition 4 | missing qualifier | Part (c) lacks the restriction to recruiting research; part (d) states a hypothesis (a strictly increasing exact margin) that the full statement does not contain, and leaves τ < 1 to the last sentence. Issues C-01, C-02, C-12. |
| Corollary 3, main-text form, `cor:research-short` | Corollary 3 | accept | Same list and endpoints as the full corollary, in outcome language, so the boundary family at r_N needs no mention. See issue C-14. |

S4 acceptance list, for this area:
- **Prior 1/2 and the mixing investor for research:** present in the Setting, in Propositions 4 (both forms), A.1, Lemmas A.15, A.16, A.18 and both forms of Corollary 3. Lemmas A.12 to A.14 and A.17 and the access paragraph hold under all four tie rules and say so.
- **Tie rules:** the default pair is stated once in each result that needs it; every extension (full preparation at a challenger tie, the threshold pair, the abstaining investor) is inside its claim.
- **Weak against strict:** right in Proposition 4(b) and (c) (strict below the cap for a strict rise in the spread, weak throughout and at the cap) and in the ownership paragraph.
- **The threshold above the prior at the start of a path:** the Setting and every path statement keep τ > 1/2 throughout.
- **Two-sided trade for the tests, a prior below the threshold for the weighted test, prior and slot fixed for the winner trend:** not applicable to area C.

## 3. The O1 notation pass and fixes 3 to 5

**Verdict: accept. The pass changed no mathematics.**

No copy of the fragment from before the pass exists: the commit that first holds `O1/` already contains it, and the private folders hold none. The check was therefore made in three ways.

1. **Step-by-step comparison with the accepted report.** Each of Steps 0 to 6 of `O1_proof.tex` was read against the referee's account in `O1_referee.md` §2.2. Every case split, inequality and conclusion that report lists is present, in the same order, with the same strength intervals, and no step was added or removed. The lemma's parts (a) to (d) say what §1 of that report accepts.
2. **The program.** `o1_bounds.py` is unchanged in the working tree. Run with `python3 -I` from the private folder, it exits 0 and prints 344 lines, as the accepted report records: the smallest piece bound is 5993292043494701003/510152171246294601024 on [6/5, 13/10], r_Q lies in [2.166995158219285882282487, 2.166995158219285882282488], and the other brackets agree with the report to its 22 places.
3. **A fresh read of each step**, with these points rechecked in the frozen notation:
   - Step 2 with fix 4: the denominator {β + (1 − 2β)[1 − τ]}² falls as τ rises, so on [r_−, r_+] it is at least its value at r_+, and the last term is at least −aβT/{…}²(r_+). Right.
   - Step 5 with the frozen sale rate: f_L = (b̄ + ŝ_−, b̄_0 + λ̄ − ŝ_−, b̄) is the order law at σ_L(−1) = ŝ_−/λ̄. The three cases give U_L(−1) ≤ 0 at ŝ_− = 0, U_L(−1) = 0 from 2b̄ + ŝ_− = b̄ρΔ_T/k in the middle case, and U_L(−1) ≥ 0 at ŝ_− = λ̄, since ŝ_− = λ̄ exactly when ρΔ_T m_λ̄ ≥ k. Right, and equal to the accepted s(r) argument.
   - Fix 3: "(E2) … orders with equal posteriors have equal entry ρ and share a price" is present and true (both nonpurchase posteriors are at most 1/2 < τ).
   - Fix 5: the fragment opens with its paragraph title; the two comment lines are gone.
   - Step 6 names the rate s_− = λ̄σ_L(−1) and ends with s_− = ŝ_−(r). The sign argument is the accepted one.
   - The renames are those listed in §9 of `O1_notes.md` and in `NOTATION.md` part (d): λ_Q, min{λ_Q, λ̄} written out, "floor-entry research", "recruiting research at the cap", φ_ρ, ŝ_−. Referee fix 2 is met by the φ_ρ and ŝ_− rows in `NOTATION.md`.

The boundary sentences added to §6 and §9 of `O1_notes.md` are correct (outcome uniqueness at ρΔ_T = 2k with the strategy family of O8) and touch neither the lemma nor the proof.

The pass leaves issues C-07 and C-08 for integration.

## 4. Numbering

Confirmed: decision 7 and Part 6 of the plan imply exactly the numbers of `C.tex`.

- The former Proposition A.1 (`prop:region`) becomes the full Corollary 1 (`A.tex` keeps the label and gives it the corollary counter). The proposition counter then moves up by one throughout the appendix, so the former Proposition A.2 (`prop:researchregion`) is Proposition A.1. The other areas apply the same shift: `A.tex` sets the counter so that the former A.7 (`prop:signals`) prints A.6, and `D.tex` so that the former A.11 (`prop:spread`) prints A.10. `A_notes.md` lists the research region as Proposition A.1.
- The example part of Proposition 4 becomes the full Corollary 3, on the independent counter of Corollaries 1 to 3; the build prints "Corollary 3".
- Lemmas: `A.tex` adds A.4 to A.6, `B.tex` has A.7 to A.11, so area C begins at A.12, as `C.tex` sets. Lemmas A.1 to A.3 keep their numbers. The lemmas beyond the former set (A.15 the sale, A.16 the outcomes in place of the retired `lem:a5-middle`, A.18 the floor-entry path) are the ones planned in the research rows of `lens_theory.md` and in the O1 rows of `NOTATION.md`. No proposition, corollary, remark or table is added, so Part 6's "no other new numbered results" holds.
- Remark A.1 stays A.1: no other area adds a remark before A.5.
- Proposition 4, full statement, prints "Proposition 4"; the main-text form carries the same number through its fixed label.

## 5. The open proofs

### O3. The segment at the cap

**Verdict: accept, with issue C-03.**

- The cap condition Δ_T m_λ̄ − k + (ρΔ_T m_λ̄ − k)⁺ ≥ 2aλ̄ is the cap side of the research root: the residual falls in λ, so the root is at least the cap exactly when the residual at the cap is nonnegative. The left side rises strictly from −k, so the cap spread is unique. Its two pieces agree at λ̄ = (1 − ρ)k/(2aρ). Since m_λ̄ < 1/2, the residual at Δ_T = 2k is k(2m_λ̄ − 1) − 2aλ̄ < 0, so the cap spread exceeds 2k and the equilibrium root exists.
- At or above the cap spread the purchase is strict (a nonpositive purchase payoff makes the sale term zero). The sale rule, the pooled-price clause with equal entry ρ, and the challenger's preparation at τ = M under the default rule complete the pointwise description.
- Path step: g_L falls, γ falls (γ' = −Δ_T' along the path), and c_H − g_L = τγ > 0, so τ is nondecreasing. Hence an upper set (cap research) and a lower set (τ ≤ M at the cap), both closed. The intersection is empty, a singleton or a closed interval [first strength at or above the cap spread, max{τ ≤ M at the cap}]. A plateau of τ at M belongs to it through its last point. Right.
- Example: Δ_T, g_L, g_H are the closed forms on [r_0, r_2] (ℓ = 1 ≤ r ≤ h), and γ' = −Δ_T' holds there. The margins at r_1 and r_2 bracket r_C uniquely.

### O4. Cheap research on the exact margin

**Verdict: accept, with issues C-04 and C-06. The computation ran and agrees.**

- The research residual at λ_E(τ) equals φ*_a because m at λ_E(τ) is 1 − τ, so recruitment at the capped root is φ*_a ≥ 0 together with λ_E ≤ cap. A nonnegative margin forces J > k and so Δ_T > 2k (since 1 − τ < 1/2), so the root exists.
- φ*_a is absolutely continuous: J is continuously differentiable, and the positive part of a continuously differentiable function is Lipschitz with derivative ρJ'·1{ρJ > k} almost everywhere, because J' = 0 almost everywhere on the level set ρJ = k. Condition (CR) then gives strict increase on every subinterval. (On a level set of positive measure, (CR) would need τ' < 0, so (CR) itself rules such sets out; the argument is consistent.)
- At r_λ̄ the spread equals the cap spread by continuity, so λ_R = cap, and φ*_a(r_λ̄) > 0 gives λ_E(τ(r_λ̄)) < cap. τ nondecreasing makes the cap posterior reach τ on all of [r_−, r_λ̄]. Below r_λ̄ the spread is strictly below the cap spread, so research is below the cap; from r_λ̄ on, O3 gives the rest. Right.
- The proof uses only continuity and strict increase of φ*_a; (CR) is one sufficient condition for the latter. This is what makes the main-text form of part (d) true (issue C-02).
- Example bounds, recomputed with exact fractions: Δ_T'(6/5) = 11/72, 1 − τ(7/4) = 19/55, Δ_T(7/4) = 9/56, T = 16875/211288, J' ≥ 21266929/532445760, φ_a' ≥ 46061709624985094449/1364098973371103914560 ≈ 0.033767 at a = 1/40, cost bound 54484791118735094449/336923259750000000000 ≈ 0.161713. The proof's route (−g_L'(r_0) + τ(7/4)Δ_T'(7/4))/γ(7/4) = 11309/207900 ≈ 0.054396 is below 16875/211288, as it says.
- `o4_margins.py`, run with `python3 -I` from the private folder: exit 0, 158 lines, no assertions. Every compared display agrees with the numbers table (section 8 of its output: 22 displays "same", the 8 proposed rows listed). The cost variant a = 1/5: the exact-margin start lies in [2.203523115209391, 2.203523115209392], the sale profit there in [0.006925573540, 0.006925573541], the purchase-only zero in [2.279293267130884, 2.279293267130885], and the smallest piece bound on φ_a' is 0.030751008; these agree with W3 (2.203523115209) and with `O4_notes.md`.

### O8. Zero research at the sale boundary

**Verdict: accept.**

- At conjectured research zero, f_H = f_L = η whatever the hypothetical-success orders, so every posterior and every price belief is 1/2. With τ > 1/2 the high-cost challenger strictly declines under either challenger tie rule, entry is ρ, and the common price is t_0 + ρ[t_L − t_0 + Δ_T/2].
- Correct orders earn ρΔ_T/2 − k, wrong-signed orders −ρΔ_T/2 − k. Ψ = (ρΔ_T/2 − k)⁺, so zero research is research-optimal exactly when ρΔ_T ≤ 2k. At equality each class may mix its correct order with abstention. These mixtures leave the order law, beliefs, prices, entry and ownership ρW_H/2 unchanged. The abstaining rule selects abstention.
- The exhaustion paragraph is right: a strict full purchase, then either full recruitment (the sale lemma and the research equation) or entry ρ (a strict full sale and the floor equation, whose root is positive exactly when ρΔ_T > 2k). The residual identity (1 − ρ)Δ_T m at λ_Q, the strict ordering of the clipped roots below the cap, and the empty band when both roots reach the cap all check.
- The claim "unique complete strategy tuple at the boundary" would be false; the lemma and Corollary 3 state outcome uniqueness and the strategy family, as W2 (item 3 of "the comparison equilibrium") and W3 (Candidate 3, outcome 1) require.

## 6. What the referee recomputed

A print-only computation in a private folder, written independently of `o1_bounds.py` and `o4_margins.py`. Rationals use exact fractions, with τ built from g_H and g_L (not from the closed form T(r)); irrational quantities use 60-digit arithmetic; r_Q comes from 220 bisection steps on φ_ρ, and the floor root at r_Q is solved directly from aλ = ρΔ_T m_λ − k, not through λ_E.

| Row | Notes' value | Referee's value and method | Agreement |
|---|---|---|---|
| `res_bound_strength` | 7/4 | r_λ̄ = 1.677633 < r_N = 1.747878 < 7/4; ρJ(7/4) − k = −377/61600 < 0 | yes |
| `res_phi_r0_frac` | −1369550353/60351152400 | exact: J(6/5) = 113/18480, λ_E(τ(6/5)) = 2416171/13716171, φ_a(r_0) = −1369550353/60351152400 ≈ −0.0226930274; ρJ(r_0) − k = −6827/369600 < 0, so φ*_a = φ_a there | yes |
| `res_phi_rcap` | in (0.01744574845681505714, 0.01744574845681505715), display 0.017446 | 0.0174457484568150571464 at r_λ̄ = 1.677632834385080818823; ρJ(r_λ̄) − k = −0.00808 < 0 | yes |
| `res_beta_upper` | 1/3 | at β = 1/3, a = 1/40: cap 0.3641753, λ_E(r_1) = 0.3166023 < cap < λ_E(r_2) = 0.3647970; a_lo = 0.0198155 < 1/40 < a_up = 0.0333367; condition (U) margins 0.015719 at r_1 and 0.034022 at r_2 | the endpoint is inside the six-strength region |
| `str_r200` | 2 | the strength 2 | yes |
| `res_I0CM_lambda_r200` | 1355413/6055413 | exact: τ(2) = 93/140, λ_E(2) = 1355413/6055413 ≈ 0.2238349391 | yes |
| `res_I0CM_e1_r200` | 292690607/813155460 | exact: J(2) = 47/560, (ρJ − k)⁺ = 11/11200, e* = 292690607/813155460 ≈ 0.3599442190; U_H(1) = 0.0102096 > 0, U_L(−1) = 0.0009821 > 0, Ψ/a = λ_E(2) | yes |
| `res_I0CM_entry_r200` | 40439906511409/140685489814428 | exact, ≈ 0.2874490224; the notes' formula gives the same fraction | yes |
| `res_rQ` | in (2.166995158219285882282487, …488), display 2.166995 | 2.16699515821928588228248724493; φ_ρ(r_N) = −0.0113912 < 0 < φ_ρ(r_U) = 0.0073464 | yes |
| `res_lambda_floor_rQ` | in (0.234257256065633848, …849), display 0.234257 | λ_E(τ(r_Q)) = floor root at r_Q = 0.2342572560656338486369 | yes |
| `res_floor_step`, `res_floor_dphi_lb` | 1/10, 1/100 | 24 pieces, smallest bound 5993292043494701003/510152171246294601024 ≈ 0.0117480 on the first piece; all exceed 1/100 | yes |
| cap | 0.336122 | 0.3361217689151211973972; m at the cap times 1 + e equals 1 | yes |
| r_R, λ_E(r_R) | 1.501023, 0.193853 | 1.5010229662625721456, 0.193853381910659 | yes |
| r_N, r_S, r_U, r_C | 1.747878, 2.124148, 2.434046, 3.592659 | 1.7478775382679627436, 2.1241481328154506735, 2.4340455267120011353, 3.5926585187946618333 | yes |
| entry at r_R and at the cap | 0.500846, 0.522757 | 0.500846367031, 0.522756943478 | yes |
| order of the marked strengths | r_0 < r_R < r_λ̄ < r_N < r_S < r_Q < r_U < r_1 < r_C < r_2 | holds | yes |
| kink intensity (1 − ρ)k/(2aρ) | > 1 | exactly 6/5 | yes (see issue C-03) |

The C_notes definition of q, the unique root in (1.747877538267962, 2.434045526712002) of J(q)/4 − 1/50 − L(T(q))/40, is the zero of φ_ρ at a = 1/40 and ρ = 1/4; the decimal endpoints bracket (r_N, r_U), and O1's derivative bound gives uniqueness on the whole path. The definition of `res_phi_rcap` through c = 1 + y + √(y² + 2y), y = (cap/20 + 1/50)(1 + e), is the cap strength r_λ̄. Both definitions are exact.

## 7. Build and language

- `C.tex` built with the shared preamble into the private folder: exit 0, 8 pages, all fonts embedded, no overfull or underfull box, no undefined reference. Exactly seven keys print as missing: `res_rQ`, `res_lambda_floor_rQ`, `res_beta_upper`, `str_r200`, `res_I0CM_lambda_r200`, `res_I0CM_e1_r200` and `res_I0CM_entry_r200`, all defined in `C_notes.md` and recomputed above. The other five proposed rows are used only in the proof fragments. All eight pages were rendered and read: displays, case braces, interval brackets and cross-references are legible; Corollary 3 prints as "Corollary 3", the region proposition as "Proposition A.1", the lemmas as A.12 to A.18, the remark as "Remark A.1".
- Language scan on `C.tex`, `O1_proof.tex`, `O3_proof.tex`, `O4_proof.tex` and `O8_proof.tex`: zero counted hits; 22 allowed tie phrases. A read of the five sources finds no status label, hedge, narration of changes, process word in printed text, retired name of the example, tool or personal name, or tie code. Every number in printed text goes through `\reg`.
- Language scan on the five notes: 139 counted hits, of which 138 are source paths, file names and obligation codes in their provenance tables and handoff sections, and one is the word "open" for the interval (r_N, r_Q) in `O8_notes.md`. These are documentary metadata in reports to the coordinator, the same judgment as `O1_referee.md` remark 6. No tool, model, account or personal name appears.
- Language scan on this report: its hits are source paths, file names, obligation codes and the words for the referee's own checks (recomputed, run, program), all documentary. "Open proofs" in the title and in Section 5 is the phrase of the brief and of Part 5 of the plan for the obligations O1 to O9, not a status of a result; "open" elsewhere names an interval.
- `C.tex` carries 37 comment lines with source paths and manuscript line numbers. They do not print, and they leave at the transplant (issue C-15).

## 8. Issues

Severity: "blocker" (the statement freeze cannot pass), "should fix" (the mathematics writer changes the text before S5 builds on it), "minor" (wording or integration, fixable at S5 or S8).

| Id | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| C-01 | should fix | `C.tex:457–460`, main-text Proposition 4(c) | The ownership claim lacks its scope: "along a path of stronger incumbents that class H always outbids, high-class ownership rises weakly" does not say that the comparison is between strengths where recruiting research exists. The full statement has "along the recruiting part of the path". With zero research coexisting, the bare sentence reads as a claim about equilibrium ownership in general. The same holds for the "exactly when" trade-off sentence. | Write "In recruiting research, across strengths of a path that class H always outbids, …" and "Between two such strengths, ownership rises exactly when …". |
| C-02 | should fix | `C.tex:461–467` against `C.tex:184–201`, Proposition 4(d), both forms | The main-text form takes as hypothesis that the exact margin is strictly increasing before the cap. The full statement has only (CR) on a continuously differentiable path. The main-text claim is true, since the O4 proof uses only continuity and strict increase, but it is not a consequence of the full statement as written, so the S9 fidelity check will fail. The main-text first sentence also leaves out τ < 1 before the cap, which the margin's λ_E(τ) needs. | In the full (d), state the monotone form first: "If φ*_a is strictly increasing on [r_−, r_λ̄] and φ*_a(r_−) < 0 < φ*_a(r_λ̄), the full recruiting set is …; on a continuously differentiable path with τ < 1, (CR) makes φ*_a strictly increasing." In the main-text (d), add "with τ < 1 before the cap" to the first sentence. |
| C-03 | should fix | `O3/O3_proof.tex:77` | "The ratio (1 − ρ)k/(2aρ) = r_0 > 1" sets a research intensity equal to a strength. The equality is a numerical coincidence (60k = 6/5 = r_0). | Write "The ratio (1 − ρ)k/(2aρ) exceeds one, and so the cap", or print the value through an added row (exact value 6/5). |
| C-04 | should fix | `O4/O4_proof.tex:69–72`, paragraph "The research margin" | "The positive part joins the two expressions continuously at ρJ = k" refers to the two derivative expressions just displayed. They do not join: the derivative jumps up by ρJ' there. "Consequently the path can start its recruiting interval with a strictly profitable sure sale" does not follow from the sentence before it. | "The margin is continuous at ρJ = k, and its derivative jumps up by ρJ' there. The condition applies as stated where the recruiting interval starts with a strictly profitable sure sale." |
| C-05 | minor | `O3/O3_proof.tex:55–56` | The monotonicity of the spread, the profit gap and the threshold along a path is stated without a reference. | Cite Lemma A.5 (`lem:twonumbers`). |
| C-06 | should fix | `C.tex:330` with `O4/O4_proof.tex:74–107` | "The roots are the unique roots on the path of their stated equations" covers r_R, defined by φ_a(r_R) = 0. The package proves that φ_a rises only on [r_0, 7/4]. Uniqueness on all of [r_0, r_2] is true: the O4 program's 1/50 pieces bound φ_a' ≥ 0.052 at a = 1/40 over the whole path. But no proof text supplies it. | Add one line to the O4 example: by Lemma A.10(b), J rises on the path, so for r ≥ 7/4, φ_a(r) ≥ J(7/4) − k − 2aλ_E(r_2) > 0 (J(7/4) = 171/3080). Or define r_R as the unique zero of φ_a on [r_0, r_λ̄]. |
| C-07 | should fix | `C.tex:228` and `O1/O1_proof.tex:4–5`; `C.tex:350` | The label `eq:a5-floor` is defined twice, with different domains: ρΔ_T > 2k with root in (0, 1) in Lemma A.16, and ρΔ_T ≥ 2k with root in [0, 1) and λ_Q = 0 at equality in O1. Lemma A.18(b) in `C.tex` says the floor root "rises strictly from zero" on [r_N, r_Q], which needs O1's extended domain, but `C.tex` defines λ_Q only on ρΔ_T > 2k. | Define λ_Q once, on ρΔ_T ≥ 2k with λ_Q = 0 at equality (O1's form), with one `eq:a5-floor`. Let Lemma A.16(c) use it for ρΔ_T > 2k. This changes the λ_Q row of `NOTATION.md`, so the coordinator enters the domain there with its date; otherwise keep the freeze and write Lemma A.18(b) as "rises strictly to λ_E(r_Q), from zero as r falls to r_N". |
| C-08 | minor | `C.tex:177`, `O4/O4_proof.tex:6`, `O1/O1_proof.tex:90–97` | r_− and r_+ name the endpoints of the path in Proposition 4(d) and O4, and the ends of a piece in O1's Step 2. Both sit in A.5, and `NOTATION.md` has no row for them. | The coordinator enters r_± for the path ends in the freeze and gives O1's pieces another pair, for example [r', r'']. |
| C-09 | minor | `C.tex:83–102`; `O1/O1_proof.tex:19–20` | Lemma A.15 restates the rate of `lem:a4-low` (Lemma A.8) at the prior 1/2 with research. The O1 proof cites Lemma A.8 for ŝ_−, so the same rate has two sources in the appendix. | At S5, prove A.15's rate by citing Lemma A.8 at presence λ, and keep A.15 for the posteriors, the boundary choices and max U_L. Or let the O1 proof cite A.15. |
| C-10 | minor | `C.tex:444–448`, main-text Proposition 4(a) | λ_R(Δ_T) appears in the existence condition before the sentence that defines it, and that sentence does not name the root. | "… where λ_R(Δ_T) is the unique root of 2aλ = …; research is min{λ_R(Δ_T), λ̄}." |
| C-11 | minor | `C.tex:184`, `C.tex:461` | "The cap spread" is used as a term but defined only implicitly, by "The cap is reached at spread …" in part (b). | Name it in (b): "the cap spread, the spread at which research reaches its cap, is …". In the main text, write it out. |
| C-12 | minor | `C.tex:173–175` | Decisive advantage is invoked without citing its lemma. | Cite Lemma A.6 (`lem:decisive`). |
| C-13 | minor | `C.tex:394`, `C.tex:410–411`, Proposition A.1 | The first sentence fixes β at its example value; the last sentence varies β. The six-strength pattern at another β has a different entry at r_1 (the formula, not `res_entry_r1`). | "With β varying, λ̄ = λ̄(β) and a = 1/40, the six-strength pattern, with entry ρ + (1 − ρ)[β + (1/2 − β)λ̄] at r_1, holds for β ∈ (β_lo, 1/3]." |
| C-14 | minor | `C.tex:474`, `C.tex:406`; `C.tex:480–481` | "λ̄ = \reg{res_cap}" prints an equality with a rounded irrational. "The weakest strength" and "the strong and very strong strengths" drift from the frozen "the weak, the strong and the very strong incumbent". | Write "λ̄ ≈ \reg{res_cap}", or drop it from the main-text corollary (it is a primitive of the example). Use the frozen phrases. |
| C-15 | minor | `C.tex`, 37 comment lines (e.g. lines 17–18, 44–45) | Source and placement comments with file paths and line numbers do not print, but they are development notes in a committed statement draft. | Remove them at the transplant, as O1 fix 5 did. |
| C-16 | minor | `O8/O8_proof.tex:7` | The statement writes the prior as π in "μ(x) = μ̄(P(x)) = π" while its hypotheses and Lemma A.16(a) write 1/2. | Write 1/2. |

## 9. For the coordinator

- The statement freeze for area C passes once C-01 and C-02 are fixed (main-text Proposition 4) and C-03, C-04, C-06 and C-07 are fixed in the proof fragments. None of the fixes changes a claim's truth or a number.
- The twelve number definitions in `C_notes.md` are exact and recomputed; they can enter the numbers table as written. S6's independent recomputation can use Section 6 above as one of its two sources only if a different helper does the other.
- Proposition A.1 is the former A.2 (decision 7); the slides and the comparison note take it from the label map at S12.
- For the research figure (S7): zero research to r_N, closed; recruiting research below the cap on [r_R, r_λ̄) and at the cap on [r_λ̄, r_C], both ends included; floor-entry research on (r_N, r_Q), both ends excluded, rising from 0 to 0.234257, and at the cap on (r_C, r_2]; entry ρ on the floor-entry pieces and 0.522757 on the capped recruiting segment.
- Only this report was added to the repository. The builds, renders, program runs and the referee's computation are in a private folder outside it.
