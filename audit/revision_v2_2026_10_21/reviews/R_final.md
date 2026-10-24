**Verdict: ready after listed fixes.**

Review date: 21 October 2026. Sources: `overleaf/paper-revision`, commit
`f94b10de76f50ca724029e6800623769588ca18b`, branch
`revision-alex-2026-10-21`, against base `9b9bf3c`.
All locations below refer to this commit.

The principal mathematical repairs are correct. The round-3 numbers reproduce.
Five small problems remain. They do not change the reported equilibria or the main theorem.

1. **The collapse paragraph still treats the floor diagnostic as a strict condition.**
   Location: `overleaf/paper-revision/online_appendix.tex:2403`.
   Related findings: R_consistency 2 and R_math 7.

   The paragraph says that the collapse node additionally requires
   $B_{r_2}(m)>0$. Proposition 2(iii) requires no such condition.
   The zero-cost challenger prepares even when gross profit is zero.
   The preceding sentence correctly calls this quantity a diagnostic.

   Exact fix: replace the sentence from “The collapse node additionally requires”
   through “its full-order margin” with:

   > The collapse node additionally requires $c_H-B_{r_2}(M)>0$ and its full-order margin.
   > Record $B_{r_2}(m)$ as a diagnostic; zero-cost preparation also occurs at equality.

2. **The general weak-economy proof claims a strict sign for gross profit.**
   Location: `overleaf/paper-revision/online_appendix.tex:558`.

   An incorrectly signed order can earn zero gross profit when
   $\Delta_T(F_0)=0$. Case D at $r_0=1$ supplies this example.
   The positive trade cost makes its net profit strictly negative.
   The main proof already states the correct weak gross-profit sign at `main.tex:2114`.

   Exact fix: replace “An incorrectly signed order has strictly negative gross expected profit.” with:

   > An incorrectly signed order has nonpositive gross expected profit and strictly negative net expected profit.

3. **The replacement class variable remains undefined in the paper.**
   Location: `overleaf/paper-revision/main.tex:2930`; first mathematical use at line 2934.
   Related finding: R_consistency 5.

   The replacement removes the collision with the value $\theta$.
   However, the paper never defines capital $J$, which also appears at line 3042.
   The Online Appendix defines it correctly at line 285.

   Exact fix: insert this sentence before the first sentence of Step 1:

   > Let $J\in\{H,L\}$ denote the challenger's class.

4. **C.10 omits the prior from its count of changed inputs.**
   Location: `overleaf/paper-revision/online_appendix.tex:3552`.

   Cases A and B change four benchmark inputs, including the prior.
   Their priors are 0.3 and 0.7; the benchmark prior is 0.5.
   The table declarations and the numerical record are correct.

   Exact fix: replace the sentence that starts “Cases A and B each change three benchmark inputs” with:

   > Cases A and B each change four benchmark inputs: the prior, the high cost, the trade cost, and the weak strength.

5. **The reserve-details caption points to the new class exhibit.**
   Location: `overleaf/paper-revision/tables/table_reserve_details.tex:3`.

   The caption still says “behind Table 4”. The reserve comparisons now form Table 5.
   Table 4 contains the class exhibit. INTEGRATION.md R3.9 already records this open item.

   Exact fix: change “behind Table 4” to “behind Table 5” in the source that produces this table.
   Regenerate the table and copy it into the manuscript clone.

The checks below support the verdict.

- **R_math blocking item 1:** resolved. Equation (A.24) uses
  $m(\pi)$, $\pi$, and $M(\pi)$ at `main.tex:2762`.
  Proposition A.6 and its proof establish the floor, weak entry, strong entry, and the exact ownership condition.
  The corresponding support conditions and proof agree at `online_appendix.tex:938`.
  Both noise laws reach beliefs near their upper bound with positive probability.
- **R_consistency blocking item 1:** resolved. Bargaining profits use lowercase $g$ in (14), Proposition A.8, (OA.44), and C.7.
  The realized profit kernel also uses $g$ in (OA.50).
  Figure 4 uses the same lowercase labels. C.7 explicitly maps the retained column names to these objects.
- **R_consistency blocking item 2:** the generated notes now distinguish four strict conditions from the floor diagnostic.
  They retain the additional support condition for atomless costs.
  The parameter notes omit the retired cost symbol.
  Item 1 above identifies the remaining contradiction in the adjacent C.1 text.
- **R_consistency blocking item 3:** resolved. The welfare formula (A.41) uses the actual prior weights.
  The atomless windows use the actual prior in both documents.
  The logistic log odds and inverse include prior odds at `online_appendix.tex:910` and line 928.
  Appendix A.5 explicitly restricts its signal formulas to the point-mass benchmark and equal prior.
- **R_consistency blocking item 4:** resolved. A.11 and C.6b use the general nonnegative-profit argument and the tie rule.
  Neither passage uses the removed example's undefined posterior or its numerical profit.

The SHOULD-FIX sample covers all seven R_math items, 2–8.
It also covers ten of fourteen R_consistency items: 5–11, 14, 15, and 17.
The remaining defects from that sample appear in items 1–3 above.
The welfare proof now covers inadmissible values, the reserve term, general priors, and strictness.
The auction proof uses the truncated payment kernel and finite-mean integrability.
The many-class proof supplies the level-set argument and a measurable posterior map in Online Appendix A.13.
The other sampled scope, notation, density, tie-rule, and general-incumbent repairs are correct.

I read the abstract, introduction, and Sections 2–4 as one model.
They consistently use quality classes, the prior $\pi$, an independent zero preparation cost, and the point-mass benchmark.
Their remaining halves represent benchmark priors, Laplace tail probabilities, or algebraic constants.
No general statement there substitutes one half for $\pi$.
No live mathematical use of the retired low-cost symbol, old three-condition system, or “perfect information” remains there.
The Online Appendix retains explicit legacy column names with zero values.

For round 3, all 63 displayed outcome and margin values in Table 4 match the relevant reconciliation rows.
The table's SHA-256 also matches its “new, round 3” record.
Every numerical statement in the new introduction sentence, Section 4.2 paragraph, Section 5.2 paragraph, and C.10 agrees with its record.
The declarations agree, including the priors, supports, costs, strengths, and unchanged inputs.

Independent calculations from the auction payoffs reproduce 87 class outcomes and condition quantities.
Their largest absolute difference from the stored values is below $2.2\times10^{-49}$.
The benchmark trade window, spread ratio, sufficient bound, and all three prior intervals also reproduce.
Cases A–C satisfy the class restrictions, both condition windows, part (iii), and the sufficient ownership condition.
Case D has upper (A1) margin $-0.0181216566973$ at $r_1$.
Its trade bounds still give unique full orders and no high-cost entry at both higher strengths.
The comparison of C and D correctly isolates dispersion at fixed means and other inputs.
The ownership claim for C concerns $r_1$, as required; it makes no increase claim at $r_2$.

Both documents compiled from an empty scratch copy of the committed sources under `/home/uctpiaj/work/tmp`.
The main paper contains 94 pages; its final log has zero errors, undefined references, undefined citations, and overfull boxes.
The Online Appendix contains 63 pages and has the same zero counts.
Neither final log has a reference-rerun request or a LaTeX warning.
The appendix retains five underfull boxes, which the integration record already identifies.
The scratch folder was deleted after the checks.

No manuscript source changed. No test was written or run.
