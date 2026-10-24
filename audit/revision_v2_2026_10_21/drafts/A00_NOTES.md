# A00 notes: class model and main results (drafter A)

The fragments rewrite the model and the main results for quality classes. The model has
classes `j ∈ {H, L}`, prior `π`, and class value distributions `G_j`. The investor observes the
class, and preparation reveals `θ`. The low cost is zero. The benchmark is the point-mass case
with `π = 1/2`. Line numbers refer to `overleaf/paper-revision/main.tex` as read on
21 October 2026 (2638 lines).

## 1. Fragments, in manuscript order

| File | Replaces (old lines) | Content |
|---|---|---|
| `A01_intro_ownership_sentence.tex` | 155–156 | "high-value challenger" becomes "a challenger from the high-value class" |
| `A02_intro_mechanism.tex` | 158–177 | Mechanism paragraph in class terms: the split of a fixed value gap |
| `A03_intro_main_result_ownership.tex` | 192 | Same wording change in the main-result paragraph; the rest of the line is verbatim |
| `A04_intro_robustness_line.tex` | 197 | First sentence becomes the class statement; the rest of the line is verbatim |
| `A05_intro_selective_entry.tex` | 203 | Three short sentences on selective entry inserted after the first sentence; the rest is verbatim |
| `A06_model_2_2_to_2_4.tex` | 264–384 | Sections 2.2, 2.3, 2.4 (classes, prior, `G_j`, the two restrictions, `C ∈ {0, c_H}`, money unit, trading, information sets, `t(θ)`, `g(θ)`, `t_j`, `g_j`, `B(μ)`) |
| `A07_section3_payoffs_inference_incentives.tex` | 386–564 | Section 3: `t+g=θ`, eq. (4)–(5) as the point-mass case, Proposition 1 with the reserve term and its exact condition, the split identity, Figure 1, eq. (7)–(11) with `m(π)`, `M(π)`, `κ(π)` |
| `A08_section4_1_proposition2.tex` | 566–686 | Section 4.1: Proposition 2 for `F_0`, `F_1`, `F_2`, conditions (A2)–(A3), ownership condition, nonemptiness clause, floor paragraph, eq. (12) with the prior shift |
| `A09_section4_2_benchmark_opening.tex` | 691–693 | Sections 4.2–4.3 are the point-mass benchmark (prior 1/2, unit `ℓ = 1`) |
| `A10_section4_3_point_mass.tex` | 729–740 | Coexistence and Proposition 3 stated at the point-mass benchmark |
| `A11_section5_2_value_classes.tex` | 873–884 | Section 5.2 "Value classes": nonemptiness for every ranked pair; the value classes of Section 6.3 as the nondegenerate example |
| `A12_appendix_A1_payoffs_pricing.tex` | 1254–1397 | Appendix A opening; A.1: proof of Proposition 1 (class formulas, reserve term, exactness), Propositions A.1 and A.2 with `π` |
| `A13_appendix_A2_trading_main_comparison.tex` | 1399–1660 | A.2: global bound with `κ(π)`, (A.7) with `J_H`, `J_L`, proof of Proposition 2 (ownership, part (iii)), Proposition A.3 for classes, Proposition A.4 (point-mass formulas, domain without the low cost, general-prior no-trade condition) |
| `A14_appendix_A3_certificate_scope.tex` | 1666 | A.3 certificates are at the point-mass benchmark with prior 1/2 (one phrase) |
| `A15_appendix_nonemptiness_and_many_classes.tex` | 1925–1948 | Nonemptiness for every ranked pair of classes (Claim 11); new subsection "More than two classes" |

Apply the fragments from the bottom of the file upward, so that the old line numbers stay valid.
The print-only helper `audit/revision_v2_2026_10_21/scripts/A_apply_fragments.py OUTDIR` does
this on a scratch copy and prints the first and last old text of each replaced range.

### Anchors and overlaps with other drafters

- `M1_01` inserts after old line 177. That is the last line of A02, so insert it after A02.
- `M1_03` replaces old lines 337–340. A06 keeps that text verbatim between the comments
  `ANCHOR M1_03 BEGIN` and `ANCHOR M1_03 END`. Replace the text between the anchors with M1_03.
- `M1_02` inserts after old line 349. A06 has the comment `ANCHOR M1_02` at that place.
- `M1_04` inserts after old line 564. A07 ends with the comment `ANCHOR M1_04`.
- Lines 173–177 (in A02) and 197 (A04) also hold investor or noise sentences. A02 and A04 keep
  them verbatim, except "knows the challenger's value" becomes "knows the challenger's class".
  If another fragment edits the same sentences, merge both edits.
- `B02` (Proposition A.5) depends on A08, A13, and A15 and uses the same names: (A2), (A3),
  `κ(π)`, `W_H`, the nonemptiness label. One wording point: B02 says part (iii) keeps "its
  stated order condition". Proposition 2(iii) has no separate order condition. Under the class
  ranking, the order bound at `F_2` follows from (A3) through Proposition 1(b). B02 should read
  "the order bound, which follows from (A3)".

## 2. Labels and tags

- **Removed:** `eq:paper-a1` (condition (A1)). Its references were at old lines 612, 1476, 1494,
  and 1538 (all inside A08 and A13, where they are gone) and at 1860 (inside B02, which
  replaces that line). No other main-text reference remains. The Online Appendix has
  hard-coded "(A1)" text; the M2 fragments handle it.
- **Added:** `more-than-two-classes` (new subsubsection in A15; nothing references it yet).
- **Kept with generalized content:** `result-proposition-1`, `eq:paper-6`, `eq:paper-7`,
  `eq:paper-9` to `eq:paper-12`, `result-proposition-2`, `eq:paper-a2`, `eq:paper-a3`,
  `result-proposition-a-1` to `result-proposition-a-4`, `eq:paper-a-2`, `eq:paper-a-6` to
  `eq:paper-a-9`, `eq:paper-a-25`, `nonemptiness-for-every-value-gap` (new title),
  `sec-acquisition-values` (new title "Value classes"). Every other label in my regions is
  unchanged.
- **Tags:** no equation number changes. New displays are unnumbered. (A2) and (A3) keep their
  tags, so there is a gap where (A1) was. To close the gap, retag (A2)→(A1) and (A3)→(A2) after
  integration. All main-text references use `\eqref`. The hard-coded "(A2)" and "(A3)" in the
  Online Appendix and in the M2 fragments then need the same change.

## 3. `\NUM` placeholders

None. My regions print no new number, and every number they keep is unchanged:

- The low cost is zero, which lies inside the slack window of the old benchmark. At every
  strength in Sections 4.2–4.3, gross profit at the lowest feasible belief is far above both the
  old low cost 1 and zero: `B_r(m)` = 2.728490, 2.366179, 2.272133 at `r` = 1.2, 3, 3.6, and
  2.636, 2.625, 2.613 at the certified strengths 1.55, 1.60, 1.65. So orders, prices, entry,
  ownership, and proceeds are the same under both declarations (normalization memo, Claim 3).
- Section 5.2 prints only numbers already in the manuscript: 0.250000 and 0.526805 (moderate
  vector, Table 3) and 0.250000 and 0.522760 (value classes at `p = 0.5`, Table 4, Panel B). The
  moderate vector's old low cost 0.3 lay inside its own window `[0, 0.4965)`.

Cross-check against `audit/revision_v2_2026_10_21/reconciliation.csv`, which appeared after
drafting. These rows show `changed = no`: benchmark entry and ownership, frozen and hidden
entry, the four thresholds `r_N`, `𝔯(k)`, `r_U`, `r_C`, the moderate entries, and the three
Proposition 3 entry enclosures. The value-class entry at `p = 0.5` (0.522760…) changes only in
its last floating-point digit. Every printed value in my regions is therefore unchanged.

For the numerics owner: Table 2 (inside Section 4.2) is pipeline output. Its net-surplus levels
rise by `ρ` times the old low cost (0.25) when the declarations switch to cost zero; its other
entries do not move. The Proposition 3 certificate run declared the old low cost 1. The
certified quantities do not depend on it, but the run record should say which value it used.

## 4. Notation

New or changed symbols (each fragment header lists its own):

- `j ∈ {H, L}`, `π`, `G_j`, `G_j(p^-)`, `D(u) = G_L(u) − G_H(u)`, `\bar r` (end of the incumbent
  support), `t(θ)`, `g(θ)`, `t_j`, `g_j`.
- `B_F`, `g_j(F)`, `Δ_T(F)` for a general incumbent law; `B_r`, `g_j(r)`, `Δ_T(r)` for the
  uniform case. `e(μ)`, `P(μ)` lose the old subscript `r`.
- Proposition 1's old `G_θ(F)` (gross profit) is now `g_j(F)`, because `G_j` is the value cdf.
- `m(π)`, `M(π)`, `κ(π) = min{m(π), 1 − M(π)} = m(min{π, 1 − π})`; `m = m(1/2)`, `M = M(1/2)`.
- `F_0`, `F_1`, `F_2` (incumbent laws of the three economies), `e_H`, `e_L`,
  `W_H(F) = E_H[F(θ) 1{θ ≥ p}]`, `O_H = π e_H W_H(F_1)`.
- In the appendix: `F_j`, `U_j` replace `F_θ`, `U_θ` (class index); `J_H`, `J_L`, `K` in (A.7);
  `ξ(R)` (kernel in the proof of Proposition 1); `Γ(x)`, `Γ`, `u_0`, `F_r` (nonemptiness);
  `π_j`, `T_X`, `\bar e(q)`, `\bar π`, `\mathcal M_π`, `γ` (many classes).
- The memo letter for the trading-bound constant is not used anywhere. The memo letters `φ`,
  `Ψ`, `α`, `D_0`, `d_1`, `H(q)`, `r(q)` are replaced because they collide with `φ_±` (A.5),
  `Ψ(r,v)` (A.3), `α_H`, `D(u)`, the class `H`, and the strength `r`.

Notation points outside my regions:

- Appendix A.6 uses `W_0(R)`, `W_θ(R)` for allocation values. The notation sheet assigns
  `W_H` to the win probability, which A08, A13, A15, and B02 use. Rename the A.6 objects.
- Appendix A.7 indexes `e_θ`, `t_θ`, `μ_θ` by `θ ∈ {H, L}`. In the class model, index by `j`.
- The index `j` also labels the certified strengths `r_j`, `v_j`, `E_j` (Proposition 3) and the
  mesh points `s_j` (A.3). The uses are local, but the prose pass may rename the certificate
  index.
- I kept "low-cost" for the zero-cost realization (the M2 inventory suggested "zero-cost" at
  old lines 188, 573, 646), because "high-cost" stays and Section 2.2 states that the low cost
  is zero.

## 5. Steps not fully verified, and statements sharpened during transcription

1. **Exactness in Proposition 1(c).** The memo's iff is "`D ≥ 0` almost everywhere above `p` and
   `D(p^-) ≤ 0`". It equals the brief's "dominance above the reserve and equal admissibility"
   only when neither class has an atom at `p`. Proof: by right-continuity, `D ≥ 0` above `p`
   gives `D(p) ≥ 0`, and `D(p^-) = D(p)` without atoms at `p`. The proposition states both
   forms. It does not claim the brief's phrase as an unrestricted iff.
2. **Split identity.** The `F`-free form needs equal admissibility, or `F(p) = 0` (the
   correction in SYNTHESIS row 2). The text states the clean form under equal admissibility.
   A12 gives the general form with the reserve term `pF(p)D(p^-)`.
3. **Condition (R) of Claim 10** is not a separate hypothesis. Under the class ranking,
   `g_H ≥ g_L` and `Δ_T ≥ 0` hold in every economy. (A3) with `k > 0` gives `Δ_T(F_1) > 0`.
   (A2), with `B_{F_1}(π) ≤ B_{F_0}(π)` from Proposition 1(a), gives `g_H(F_1) > g_L(F_1)`. The
   weak economy needs no strict ranking. Step 3 uses only the upper bound `A ≤ Δ_T(F_0)`,
   which holds without price inversion.
4. **"Unconditional" means the floor.** With cost zero, entry is at least `ρ` at every price.
   The inversion in Proposition A.2 still needs `Δ_T > 0`. If `Δ_T = 0`, residuals vanish, no
   one trades, and the constant price reveals the prior.
5. **Many classes (A15).** I re-derived three steps of Claim 7 in the extensions memo: orders
   are monotone in class proceeds, the covariance identity holds, and equality forces a constant
   likelihood ratio. I did not write out in full the measurability of the map from `T_X` to the
   posterior (level sets of the monotone `T_X` are intervals, and the posterior is constant on
   each). SYNTHESIS row 25 records the same scope. The two-group statement gives sufficient
   conditions only. The memo argues that these conditions hold on a nonempty set: the
   point-mass benchmark with exact rational bounds, then small splits of each class. I did not
   transcribe or recheck that argument, and the remark does not claim nonemptiness.
6. **Selective-entry sentences (A05).** In the literature memo, Gentry and Li (2014) and
   Marmer, Shneyerov and Xu (2013) were read in working-paper versions. Samuelson's
   assumption (values known before the entry cost) is known through Levin and Smith (1994,
   footnote 7). The citation check should confirm the published versions. The text
   attributes no "nests both limits" statement to Gentry and Li.
7. **Slack low cost (A08, one sentence).** "Any low cost below `B_F(m(π))` in every economy
   compared would give the same orders, prices, and entry." This generalizes Claim 3 of the
   normalization memo to classes and a prior. The argument: every posterior is at least
   `m(π)` under any strategy, and `B` is nondecreasing under the ranking, so such a low-cost
   type prepares at every reachable price, and the entry function is unchanged.
8. **No-trade condition at a general prior (A13).** "No trade is an equilibrium exactly when
   `e(π) Δ_T max{π, 1 − π} ≤ k`." Section 5 of the check script confirms the two residuals
   against a direct computation at `π` = 0.3 and 0.7.

## 6. Items outside my regions for other drafters or the integrator

- Abstract: "high-value challenger ownership increase" should name the high-value class.
- Section 2.1, old lines 244–248: "gives the investor perfect information". In the class model
  the investor observes the class, not the value. The phrase is true only in the point-mass
  benchmark.
- `M1_04`: "Each gain is positive." Always `t_j ≥ t_0`. Strict positivity holds when the class
  is admissible with positive probability and `F(p) > 0` (for example, a uniform incumbent with
  `r > p`). Under equal admissibility with `Γ > 0`, both classes are admissible with the same
  positive probability.
- Section 6.3 (Claim 4(e) of the main memo): at `p = 1.1` the low class is inadmissible, and
  the spread falls in `r` on `(p, √3 p)`. A11 points to Section 6.3 for this deterrence case.
- The Online Appendix sections A.1–A.5 cited from my appendix text are written for the point-mass
  case. Drafter B's scope note B05 records which arguments carry over to classes.

## 7. Checks run (print-only; no tests)

- `audit/revision_v2_2026_10_21/scripts/A_reading_n_checks.py` (output saved next to it as
  `A_reading_n_checks.out.txt`). It checks these items:
  - formula (6) against direct integration of the payment rule, in five class pairs,
    including a pair with `D(p^-) ≠ 0`;
  - the split identity with and without the reserve term, and `t(θ) + g(θ) = θ`;
  - `m`, `M`, `κ` at `π` = 0.3, 0.5, 0.7 (they match the memo);
  - `x*` against a direct root of `μ_X(x) = τ`, and `J_H = (1 − π)K`, `J_L = πK`;
  - the Proposition 2 margins for the point masses and for the value classes at the benchmark
    vector (all strict; the part (iii) margin for the value classes is 0.002658);
  - the nonemptiness construction for two ranked pairs, at `π` = 0.7 and 0.3;
  - the ownership caveat in case 2c (entry 0.95 → 0.970117 while ownership falls,
    0.422906 → 0.416476).
- Compile check: A_apply_fragments.py writes a scratch copy with my fragments only, and
  `latexmk` builds it with no errors and no overfull boxes. The remaining warnings are expected:
  the two new citation keys (`ref-MarmerShneyerovXu2013` and `ref-GentryLi2014`; bibitems
  come from `F_bibitems.tex`), and `eq:paper-a1` at old line 1860 (B02 replaces that line).
  The PDF grows from 73 to 82 pages at double spacing: about 3 pages in Sections 2–3 and
  6 pages in Appendix A (the proof of Proposition 1(c), the nonemptiness construction, and the
  new subsection on more than two classes). The scratch copies were deleted after the check.
