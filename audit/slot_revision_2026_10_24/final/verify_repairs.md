# Verification of the final audit repairs

**Verdict: FAIL for exact agreement between the main text and Appendix A.** Three repairs still need precise prose: the control condition, the reserve summaries, and the payment support. The theorem statements remain intact. **The removal of result-status vocabulary passes the mathematical preservation check.**

I read `brief_verify2.md` in full and followed its read-only scope. I examined both audit reports, all three commit diffs, and the relevant statements and proofs in Appendix A. All manuscript locations below refer to `slot/manuscript/` at `2eed6b6c90663000cf39b942866e17a49a5d3d7b` on `slot-revision`.

The actual commit order is `c78e2c3` → `9d3c66e` → `da84b08` → `2eed6b6`. Thus the status removal precedes both repair commits; it does not sit between them. I checked the actual diffs, despite that small discrepancy in the brief.

## Core findings

### 1. Fixed-information control — FAIL as an exact statement

Locations: `sections/04_equilibrium_results.tex:188–195` and `sections/08_empirical.tex:16–21`. Appendix: `appendix/A6_robustness.tex:8–35`.

The repair restores the challenger's marginal value restriction and the incumbent's independence from the class and signal. However, it replaces “the two values are independent given the class and the signal” with “the two values are independent.” The sentence begins “Given the class”; it does not clearly condition this last independence on the signal too.

Appendix A requires the joint conditional law

\[
\mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i.
\]

Independence of each value from the signal, plus independence between the values before the signal, does not imply this product law. Even independence between the values conditional on the class is insufficient.

For example, fix a class. Let \(Z\) be a fair binary variable and let \(U\) be independent and uniform on \([0,1]\). Set

\[
\theta=v_j+2Z,\qquad R=2U,\qquad
S=\mathbf 1\{Z=\mathbf 1\{U\ge 1/2\}\}.
\]

Each value is independent of \(S\), and the two values are independent before \(S\). Conditional on \(S=1\), the high challenger value occurs exactly when \(R\ge1\). Thus the conditional product law fails. This example diagnoses the logical gap; it is not a numerical equilibrium exercise.

The intended stronger interpretation is clear from the appendix reference. It is not explicit in the revised prose. Restore “independent given the class and the signal,” or state the product law directly. The proof uses precisely that law at A.6:21–24. The default challenger tie rule remains at `sections/02_model.tex:221`.

### 2. Scope of the gross-return bound — PASS

Locations: `sections/03_competition_information.tex:110–122`; `appendix/A2_beliefs_trading.tex:173–189`.

The revised sentence concerns the **gross return of a correctly signed order**. The next subsection identifies these orders as a purchase in class H and a sale in class L. Thus zero orders and wrong-signed orders are outside the claim. The bound concerns gross returns, before the trade cost:

\[
\rho\kappa(\pi)\Delta_T\le K_H,K_L\le\Delta_T.
\]

This agrees with Lemma A.3. No additional “nonzero” word is necessary in this context.

### 3. Definitions after the objective — PASS for mathematics; accepted editorial exception

Location: `sections/02_model.tex:192–204`.

I agree with the decision to retain the immediate “where” clause. It defines both symbols within the sentence that contains the display. It defines \(e(q)\) as entry after the order and \(t_j\) as expected proceeds after entry in class \(j\). The class expectation follows at line 204. Neither symbol changes meaning.

This does not satisfy a literal requirement that every definition precede its first display. It is a conventional and unambiguous definition at first use, so no mathematical repair is needed.

## Extension findings

### E1. Conditional-law restriction — FAIL

This duplicates core finding 1 at `sections/08_empirical.tex:16–21`. The marginal restriction is repaired. The conditional independence of the two values still needs explicit wording. The same repair applies at both main-text locations.

### E2. Reserve result and flat entry — FAIL overall; Section 7 passes

Locations: `sections/07_welfare.tex:67–71`, `sections/01_introduction.tex:87–89`, and `sections/09_conclusion.tex:18–19`. Appendix: `appendix/A7_welfare.tex:162–191`.

Section 7 now states both required features: full informed trade at both strengths, and recruitment only after a purchase. These features match the appendix proof. Full orders fix the purchase probability at \(b+\pi\lambda\), and hence fix entry at

\[
\mathcal E_i=\rho+(1-\rho)(b+\pi\lambda).
\]

The introduction and conclusion restore only “only a purchase.” Neither summary states full trade. An informative price does not imply full trade. If class H purchases with probability \(a_i\), while class L never purchases, then

\[
\Pr_i(X=1)=b+\pi\lambda a_i.
\]

Recruitment only after a purchase fixes the entry rule, but does not fix this purchase frequency. Therefore it does not alone imply flat entry. Add full trade at both strengths to both summaries. No change to Section 7's repaired condition is needed.

### E3. Sufficient conditions versus necessity — PASS

Locations: `sections/06_robustness.tex:83–88`; `appendix/A6_robustness.tex:433–441,506–519`.

The revised paragraph says that the **conditions** cannot hold at the benchmark when the buyer signal is at least as accurate. It no longer claims that every reversal with such a signal requires different costs and strengths. The two incompatible bounds in A.6 establish exactly the stated failure of sufficient conditions. The separate example retains its own parameters.

### E4. Zero-order announcement claim — PASS

Locations: `sections/08_empirical.tex:55–60`; `appendix/A8_empirical.tex:14–28,198–232`.

The sentence now requires full two-sided trade and the interval \((r_S,r_C]\). On that interval the zero-order posterior equals the prior, while a purchase recruits. Therefore no order conveys no class news and lowers the price relative to its prior mean through entry. The inclusive upper endpoint agrees with the default challenger tie rule. The purchases-only and no-trade counterexamples from the audit are outside this claim.

### E5. Payment-rule support — FAIL for exact agreement; the missing upper bound is repaired

Locations: `sections/07_welfare.tex:41–57`; `appendix/A7_welfare.tex:102–136`.

The repair states point-mass classes and the inequality \(0<\ell<\bar r<h\). This repairs the missing upper bound and supports the strictness claim. However, its prose says that the incumbent's **values lie between the low and high class value**. That statement restricts realized values to above \(\ell\).

Appendix A instead gives support \([0,\bar r]\). It explicitly includes \(R\le\ell\), as its proof at lines 127–131 shows. The benchmark uniform law also includes values below \(\ell\). The displayed inequality restricts the upper support endpoint; it does not impose a lower bound of \(\ell\) on realized values.

Replace the support phrase with “an incumbent distribution on \([0,\bar r]\), where \(0<\ell<\bar r<h\).” The formulas and strictness result need no change. This is a new, narrower support description, not a remaining claim about incumbents above \(h\).

### E6. Reference price for impacts — PASS

Locations: `sections/08_empirical.tex:23–29`; `appendix/A8_empirical.tex:41–55`.

The paragraph now explicitly defines the purchase impact as \(P(1)-P(0)\) and the sale impact as \(P(0)-P(-1)\). Both use the zero-order price, exactly as Appendix A requires. Neither uses the mean price before the opportunity.

The definitions follow the first comparison sentence, rather than precede it. As with the objective's “where” clause, this local order does not create mathematical ambiguity. The strict editorial request for definitions before use remains an exception.

### E7. Undefined benchmark label — PASS

Locations: `sections/06_robustness.tex:67–80`; `appendix/A9_parameters.tex:49–58`.

The main text removes both uses of \(S(B)\). It specifies the example through its retained benchmark primitives and its explicit replacement parameters. This implements the audit's permitted alternative to restoration of the label B. Appendix A retains its own defined vector. No primitive or reported value changes.

## Status-removal commit `9d3c66e` — PASS for mathematics

I examined every changed file in this commit. The edits remove status labels, proof-method summaries, and three statements about unresolved scope. They do not change a formal hypothesis, conclusion, quantifier, equation, model input, or reported numerical value. The registry `numbers.tex` has no change from `c78e2c3` through `2eed6b6`. Neither repair commit changes Appendix A.

The proofs retain their exact Sturm arguments, interval calculations, scripts, and logs. The A.4 cross-check still “enters no step of the proof.” The A.5 scan still “enters no proof.” Thus removal of the diagnostic label does not promote either scan into proof evidence. A.9 retains the distinction between declared inputs and derived quantities.

The deletions of “open” statements need separate scope checks:

1. **Research interval — PASS.** Section 5 retains the bound above \(r_U\) at lines 128–130. Its figure notes retain both cap ranges and identify the gap \((r_N,r_U)\) at lines 140–144. No new equilibrium classification is asserted inside that gap. A.5:203–231 and 255–260 retain the sufficient bound. The deletion makes the unresolved scope less explicit, but it does not extend the theorem across the gap.
2. **Payment equilibrium — PASS.** Section 7 still restricts the comparison to “the payment stage” at line 42. The paragraph states payment, profit, and spread results. It does not assert an order or preparation equilibrium under the alternative rule. Appendix A.7:97–137 proves that continuation only. The support wording defect identified under E5 comes from the later repair, not this deletion.
3. **Selection between clusters — PASS.** Section 8:62–67 still says processes “can form two clusters.” It does not select an equilibrium or assign cluster frequencies. Appendix A.8:239–249 retains the equilibrium set and the default-rule restriction. Removal of the selection sentence does not create a selection theorem.

The removed prose also includes references to two proof steps and one repeated interval. Their mathematical content remains in the appendix and figure notes. Thus “unchanged mathematics” describes retained results and scope, not literal preservation of every source token.

## Method and limits

This was a static source review. I read the real Git diffs and manuscript sources; I ran no tests, certificate programs, numerical exercises, or PDF build. I did not edit, commit, or check out repository files. This report is the only file I wrote.

The tracked checkout remained at `2eed6b6`. The untracked `slot/study_guide/` directory was present at the start. An untracked `audit/slot_revision_2026_10_24/final/prose_check.md` appeared during the review. I did not alter either path.

The failures concern exact prose correspondence. They do not invalidate the unchanged appendix theorems or establish a numerical error. Resolve the three wording defects before approval of exact main-text agreement.
