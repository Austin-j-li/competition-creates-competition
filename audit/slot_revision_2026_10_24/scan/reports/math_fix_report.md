All eleven math corrections are complete on `slot-revision`. Nine manuscript files changed. No commit was made. No tests were written or run.

All source paths below are relative to `slot/manuscript/`. Line numbers refer to the final source.

1. **M1 — Lower boundary.** Changed `appendix/A3_proposition2.tex`, lines 169–170 and 207–209.

   Old: “orders are uniquely full at all three strengths.” New: orders are uniquely zero at \(r_0\) and uniquely full at \(r_1,r_2\). The proof now states \(\Delta_T(r_0)-k=-1/300<0\). Rule C1 still gives every conclusion of Proposition `prop:ccc`.

   Consumers checked: `sections/04_equilibrium_results.tex:123–125` needs no change; its C1 and CM conclusions remain correct. `appendix/A4_coexistence.tex:3–7` needs no boundary change; it assumes the strict open band.

2. **M2 — Fixed information.** Changed `appendix/A6_robustness.tex`, lines 9–11 and 21–23.

   Old: “Let the value depend on \(S\) only through the class.” New: each economy requires \(\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i\), with the cost independent of the class, both values and signal. The proof cites this condition before it writes gross profit as \(B_{F_i}(\mu(S))\).

   All three listed consumers changed. `sections/04_equilibrium_results.tex:189–191` and `sections/08_empirical.tex:11–12` now state the same conditional law and independent cost requirement. `appendix/A6_robustness.tex:44` now states that the slot has conditional value law \(G_j\otimes F_r\).

3. **M3 — Sale rate.** Changed `appendix/A4_coexistence.tex`, lines 204, 263–264, 270, 275–277, 317 and 321.

   Old: \(t_L(r)\) denotes the sale rate. New: \(s_-^*(r)\) denotes that rate. All rate formulas, order probabilities, posterior arguments and proof comparisons use the new symbol.

   A manuscript search found no earlier use of \(s_-^*\). All remaining uses of \(t_L\) in the sections and appendices denote proceeds. The consumer at `sections/04_equilibrium_results.tex:276–293` already uses \(s_-\) for the sale rate and needs no change.

4. **M4 — Exact signal witness.** Changed `appendix/A6_robustness.tex`, lines 466–479.

   Old: “Nothing in the hypotheses links \(d\) and \(a_T\), so \(d>a_T\) is allowed.” New: the proof retains the values, costs, strengths and accuracies of \(S(B)\), with \((\lambda,\beta)=(1/3,3/10)\). It gives \((a_T,d)=(7/10,3/4)\), \(M=8/11\) and \(m=3/11\).

   I independently recomputed the private, joint, weak-trade, strong-trade and other-pair margins with exact fractions. They are, in that order,

   \[
   \frac{21}{400},\qquad \frac{1363}{36800},\qquad \frac{2}{1375},\qquad
   \frac{603}{31625},\qquad \frac{76753}{18400}.
   \]

   All five are positive. The manuscript now gives each margin beside its formula. No separate consumer was listed. I also checked `sections/06_robustness.tex:59–79`; its feasibility claim remains consistent and needs no M4 change.

5. **M5 — Net sale payoff.** Changed `appendix/A6_robustness.tex`, lines 542–544.

   Old: the sale “earns” \(b/[15(2b+t)]\). New: the net payoff is \(U_-(-1)=b/[15(2b+t)]-1/50\). The text retains the unique zero-profit rate \(t=4b/3\). Exact fraction arithmetic gives zero net payoff at that rate.

   No separate consumer was listed. The general payoff formula at `appendix/A6_robustness.tex:425` and the equilibrium summary at `sections/06_robustness.tex:82–86` remain consistent.

6. **M6 — Dispersion.** Changed `sections/06_robustness.tex`, line 45.

   Old: “raises gross profit at every belief.” New: “weakly raises gross profit at every belief.” The corresponding appendix statement, now at `appendix/A6_robustness.tex:266–267`, already gives the weak inequality and needs no change.

7. **M7 — Variable cap.** Changed `appendix/A5_research.tex`, lines 293, 306–308, 315–316 and 330. Changed `sections/05_research.tex`, lines 167 and 171–172.

   Old: “The claims of Proposition” apply throughout the cap and cost region. New: the reference applies to the “equilibrium patterns.” The proposition now gives entry at \(r_1\) as

   \[
   \rho+(1-\rho)\bigl[\beta+(1/2-\beta)\bar\lambda\bigr].
   \]

   Both listed consumers changed. Section 5 now limits the reference to the patterns and gives the formula. The appendix proof now uses the same scope and derives entry from Lemma `lem:a5-strong`. The fixed benchmark number in Proposition `prop:research` remains valid at its stated cap.

8. **M8 — Entry ceiling.** Changed `sections/01_introduction.tex`, line 98.

   Old: “Against a strong prepared bidder.” New: “Above the entry ceiling.” Both listed consumers need no M8 change. `sections/08_empirical.tex:40–46` distinguishes the entry covariance at \(r_1\) from zero at \(r_2\). `appendix/A8_empirical.tex:174–175` already states the condition \(r>r_C\).

9. **M9 — Signed gap.** Changed `appendix/A6_robustness.tex`, lines 270–272.

   Old: the top posterior “misses the high cost by” a negative registry value. New: the text states the signed profit gap \(B_{r_1}(M(3/10))-c_H\). Both the prior and the gap use their existing registry macros. No separate consumer was listed. The fixed-prior summary at `sections/06_robustness.tex:37–40` remains correct.

10. **M10 — Zero research.** Changed `appendix/A5_research.tex`, lines 172–174.

    Old: “In every equilibrium of the list, the purchase earns” a positive payoff. New: “In each listed equilibrium with positive research” the purchase earns that payoff. The next sentence cites Step 1 for strict abstention in Z.

    No separate consumer was listed. Step 1 at lines 118–122 and the strict-choice conclusion at lines 238–239 remain consistent and need no change.

11. **M11 — Table scope.** Changed `appendix/A6_robustness.tex`, lines 239–240 and 253–254.

    Old: the first five rows satisfy every hypothesis of Proposition `prop:ccc`. New: the moderate-gap row satisfies (H1)–(H2); the other four reversal rows also satisfy (H3). Both listed passages now state this scope. Table `tab:classes` retains its blank third-strength cell for the moderate-gap row.

The required build passed with exit code 0:

```bash
cd slot/manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/ccc_slot_scan/build_fix main.tex
```

The PDF is `/tmp/ccc_slot_scan/build_fix/main.pdf` (102 pages). The build transcript is `/tmp/ccc_slot_scan/fix/latexmk_fix.log`.

The required log scan gave no output:

```bash
grep -E "undefined|multiply" /tmp/ccc_slot_scan/build_fix/main.log
```

Its exit code was 1 because no pattern matched. The log has no undefined references or multiply defined labels.

The required number scan ran from the repository root and passed:

```text
files scanned: 21; distinct keys used: 676; missing keys: 0
literal decimals outside \reg: 0
```

Its output is `/tmp/ccc_slot_scan/fix/number_scan_fix.log`. The exact calculation is `/tmp/ccc_slot_scan/fix/recompute_math_fix.py`; its output is `recompute_math_fix.log` in the same folder. This script prints values and contains no assertions.

`git diff --check` is clean. Every label remains intact. Only the nine approved section and appendix files changed in the repository. `numbers.tex`, the registry, `slides.tex` and `comparison.tex` remain unchanged.
