# FAIL — final prose review against Appendix A

Branch: `slot-revision`. Base: `2eed6b6`. Reviewed final HEAD: `62117e55aed11ec5c2c9635839ab304ad7c74f2e`.

Two summaries need explicit scope. Neither finding concerns a changed formula or number. Items 9 and 11 pass.

I read the full brief, the composer report, every manuscript diff, and the relevant statements and proofs in Appendix A. The review began at `e0e65a9`. HEAD then advanced to `62117e5`, which deletes one source comment from A.1. I also reviewed that deletion.

The repository stayed read-only. I wrote only this report. I ran no tests or builds. A short command printed registry displays and evaluated the two transferred signal rates without assertions.

Paths below are relative to `slot/manuscript/`. Related clauses share an entry where one appendix argument establishes each clause.

## Required corrections

**F1 — FAIL: the introduction no longer confines signal complementarity to the example.**

Location: `sections/01_introduction.tex:80–82`.

The sentence joins the general signal result to “the rise then needs both signals.” It removes the previous explicit example scope and its separate costs and strengths. Appendix A.6 does not establish necessity of both signals for every instance of its proposition. Lines 517–519 expressly allow the theorem without that complementarity. A.9 also distinguishes the example vector from calibration B.

Replace that sentence with these exact sentences:

> It also survives private signals that the buyer and the investor hold about different facts (Section~\ref{sec:signals}). In an example with its own costs and strengths, the buyer's signal is more accurate than the investor's. The rise in that example needs both signals.

This restores the former scope. It does not alter the signal proposition or either example.

**F2 — FAIL: the conclusion does not delimit the constant-entry claim.**

Location: `sections/09_conclusion.tex:10–13`; composer item 13.

The preceding sentence now names three economies. “Between the two economies” therefore leaves the relevant pair unclear. The subsequent clause says entry “stays constant once the high class buys for sure.” Appendix A.4 limits that plateau to strengths at or below the entry ceiling. The high class still buys for sure above the ceiling, but entry drops to its floor.

The earlier prose also needed a narrow interpretation. The final wording does not make that interpretation secure after the antecedent changes to three economies. This is a scope failure, not a new error in Proposition 3.

Replace the sentence from “Between the two economies” through “for sure” with these exact sentences:

> Between the weak and strong benchmark economies, informative and uninformative equilibria coexist on an interval of strengths. On the informative branch that coexists with no trade, entry rises strictly while the high class mixes between a purchase and abstention. Entry stays constant from full purchases to the entry ceiling, then falls to its floor above that ceiling.

Appendix A.4, full Proposition 3, gives the exact intervals: strict rise on \([r_A,r_F]\), a plateau on \([r_F,r_C]\), and the floor on \((r_C,r_2]\).

## All changed mathematical statements

### Abstract and introduction

1. **PASS — abstract, “buyer” becomes “challenger.”** The same agent sees the price, pays for preparation, and receives auction profit. A.1 and A.3 support each clause. The change adds no restriction or claim of strictness.

2. **PASS — introduction, the two claims on acquisition surplus.** The new sentence still assigns auction rent to the challenger and cash proceeds to target shareholders. A.1 gives their split. The following class-gap explanation keeps its original assumptions.

3. **PASS — introduction, three economies and unique equilibrium outcomes; composer item 1.** A.3 derives the unique tuples at the weak, strong, and very strong incumbents. Its open-set paragraph supports the parameter claim. Recruitment stops in the third economy while prices remain informative.

4. **PASS — introduction, high-class ownership condition; composer item 1.** A.3, Step 4, requires

   \[
   [\rho+(1-\rho)(b+\lambda)]W_H(F_1)>\rho W_H(F_0).
   \]

   The new prose restores this qualification. The benchmark has \(W_H(F_0)=W_H(F_1)=1\), so the condition holds strictly.

5. **PASS — introduction, benchmark ceiling and admissible band.** The deleted sentence duplicates the third-economy result. The remaining ceiling and “exactly when” band agree with A.3, admissible-region proposition, and A.4. All registry references retain their values.

6. **PASS — introduction, complete equilibrium set along the benchmark path.** A.4 supplies that set on \([r_0,r_2]\). The revised pointer preserves the benchmark scope and the inclusive coexistence interval.

7. **PASS — introduction, other cost laws.** A.6 permits both atoms and atomless components under its support gaps. The revised sentence keeps this existence claim.

8. **PASS — introduction, every ranked pair and prior; many classes under separation.** A.6 proves the two-class existence result and states the separate sufficient condition for many classes. See entry 36 for the equivalence of the two-class hypotheses.

9. **FAIL — introduction, private signals and necessity of both signals.** Apply F1. The existence claim survives; the scope of the necessity claim needs repair.

10. **PASS — introduction, reserve summary.** The added full-trade condition is necessary for the stated argument. With full orders and recruitment only after a purchase at both strengths,

    \[
    \operatorname{Ent}_i=\rho+(1-\rho)(b+\pi\lambda).
    \]

    A.7, reserves proposition and proof, give this same value at both strengths.

11. **PASS — introduction, purchase and sale impacts; composer item 2.** Both impacts now use the price after no order. A.8 gives

    \[
    I_+-I_-=(1-\rho)\chi_r A_r(M).
    \]

    This is exactly the entry component. The benchmark share remains 90.2%. The pointer leads to Section 8's benchmark and full-trade scope.

12. **PASS — introduction, outside investor and appendix roadmap.** The investor still earns only the trade residual. A.1 defines that payoff. A.4–A.8 contain the full coexistence, research, robustness, welfare, and empirical results named in the revised roadmap.

### Model and information

13. **PASS — model, preparation as an entry cost.** The shorter sentence preserves both consequences: no preparation means no bid; preparation reveals value and permits a bid. A.1 uses precisely this auction participation rule.

14. **PASS — model, investor information and challenger identity.** The name changes preserve exact class information for the investor and no initial class signal for the challenger. A.6 supplies the signal extension; A.5 supplies research. The identity-versus-fit sentence concerns uncertainty about the challenger. The next paragraph still states that the incumbent's realized value is private.

15. **PASS — model, public incumbent distribution.** The deleted duplicate does not remove private realized value from the model. Section 2.1 still states that condition. A.1–A.3 continue to integrate over the incumbent distribution.

16. **PASS — model, weakest restriction.** A.1, Proposition 1(c), gives the same equivalence when neither class has an atom at the reserve. The change only merges the proposition pointer into the sentence. “Rises” retains its nondecreasing sense; no strict claim is added.

17. **PASS — model, outside investor.** The removal of the hedge example and the negative source clause changes no payoff or information variable. The retained conditions exclude an initial net position, control rights, and acquisition by the investor.

18. **PASS — model, residual advantage after every order.** A.2, order-probability lemma, gives positive order probabilities in both classes. Every posterior remains interior. The deleted “no order is conclusive” clause repeats that implication.

19. **PASS — model, Laplace comparison and upright Euler constant.** Only the typographic explanation moves here. The likelihood-ratio formula and its equivalence to the slot bound remain unchanged.

20. **PASS — model, default tie rules.** A.1 uses IM and C1. A.4's table records their alternatives on the benchmark path. The new table reference changes no tie choice.

21. **PASS — Section 3, payment at a fixed incumbent value.** For \(R\ge p\), A.1 gives the payment \(\min\{R,\max\{\theta,p\}\}\) and class difference \(\int_p^R D(y)\,dy\). The revised slice explanation preserves that conditional statement.

22. **PASS — Section 3, posterior ceiling; composer item 3.** A.2's exclusion corollary uses \(g_H\ge g_L\) and \(B(M)<c_H\). It excludes high-cost preparation under every admissible profile, in or out of equilibrium. The model's bound on the liquidity probability remains in force.

23. **PASS — Section 3, residual uncertainty and class separation of returns.** A.2 gives each correct-order return as entry times the spread times residual uncertainty. Its final lemma makes each class's return depend only on its own nonzero order. Entry after the zero order enters no investor payoff.

### Equilibrium and research

24. **PASS — Proposition 2 frame; composer item 4.** The two-sentence frame retains continuity, the ordered incumbent distributions, all parameter restrictions, and every strict inequality in (H1)–(H3). A.3 proves the same result.

25. **PASS — benchmark slot declarations.** A.9 retains the exact decimal liquidity probability and the unrounded definitions of derived values. The likelihood ratio, presence probability, liquidity mass, and posterior bounds are unchanged.

26. **PASS — width of the posterior band.** The payment remains \(r/2+p^2/(2r)\). Its derivative is \(1/2-p^2/(2r^2)<1/2\). A.1 and A.4 support the explanation; the edit changes its subject only.

27. **PASS — parts (i) and (ii) without the ceiling; composer item 8.** A.3 uses (H3) only to exclude high-cost preparation in the third economy. “Hold without the ceiling” therefore preserves “do not use (H3).”

28. **PASS — figure pointer to the posterior band.** The table and A.3's admissible-region proposition describe the same open band. Removing the part letter changes no endpoint or prior.

29. **PASS — control independence condition; composer item 5 and coordinator repair.** The final conditional independence clause now matches

    \[
    \mathcal L_i(\theta,R\mid j,S)=G_j\otimes F_i.
    \]

    The cost remains independent of the class, both values, and the signal. A.6 uses the same fixed laws and the same conditional product law.

30. **PASS — control decrease and Panel B; composer item 6.** Under C1, A.6 gives the precise event

    \[
    B_{F_1}(\mu(S))<C\le B_{F_0}(\mu(S)).
    \]

    The prose word “between” retains this convention through the proposition reference. The two displays remain 0 and 0.272757. No atom or endpoint convention changes.

31. **PASS — coexistence setup, threshold definitions, and Proposition 3 frame; composer item 7.** The auction, prior, slot band, path, and inclusive interval \([r_A,r_N]\) remain unchanged. A.4 gives the definitions of all six thresholds and slot independence of \(r_A,r_N,r_J\). Removing “(a)” does not add the variable-prior case, since the sentence fixes the prior at one half.

32. **PASS — no-trade terminology in the proposition, figure note, and explanations.** Pattern N remains the equilibrium without informed trade. It includes \(r_N\) and fails above it. A.4 gives precisely that boundary and the unchanged mixed-order patterns.

33. **PASS — other-prior explanation.** A.4's corollary gives the same lower and upper prior cutoffs. The repeated displays remain approximately 0.396175 and 0.650059. They refer to the exact cutoffs, not new decimal endpoints.

34. **PASS — research equilibrium and posterior notation.** A.5, condition (E7) and the joint-deviation lemma, fix prices and the entry rule during a deviation. They also require an optimal order after success, including a deviation from zero research. The prior stays one half; the posterior notation is unchanged.

35. **PASS — equilibrium without research at intermediate strengths.** A.5 gives the zero-research tuple and the strict inequality \(\rho\Delta_T/2-k<0\) below \(r_N\). The replacement of “no research” by its equilibrium description preserves that claim.

### Robustness

36. **PASS — “differ above the reserve”; composer item 9.** Section 2's class ranking requires both supports at or above the reserve and \(D=G_L-G_H\ge0\). Finite means then give

    \[
    \mathbb E_H\theta-\mathbb E_L\theta=\int_p^\infty D(y)\,dy.
    \]

    If the distributions differ above the reserve, right continuity makes \(D>0\) on an interval of positive length. The integral is strictly positive. Conversely, a positive integral requires a difference above the reserve. Thus the new phrase is equivalent to A.6's strict mean inequality under the retained class ranking. The arbitrary prior, slot, reserve, and zero-cost probability keep their admissible domains. Uniform incumbents and the open set of strengths and costs remain explicit.

37. **PASS — “never lowers gross profit at any belief”; composer item 9.** A.6 establishes convexity of \((\theta-\max\{p,R\})_+\). A mean-preserving spread raises each affected class profit weakly. Every fixed-belief average therefore cannot fall. Equality remains allowed.

38. **PASS — separation into high and low groups; composer item 9.** A.6 partitions the classes before its many-class proposition. Its inequalities apply to every feasible posterior mean and every class in each group. The revised sentence preserves those quantifiers. The proof gives prior proportions within groups and full recovery of the posterior vector in the strong equilibrium.

39. **PASS — transfer of the benchmark signal paragraph to A.6.** The appendix already states the tuples, entry values, uniqueness under IM, and nonexistence under I0. The new sentences transfer the two conditional trade probabilities. From its exact rates and \(u=\mathrm e-1\), they are

    \[
    \frac{119}{96(\mathrm e-1)}\approx0.721409,
    \qquad
    \frac{4}{3(\mathrm e-1)}\approx0.775969.
    \]

    The first applies after either signal at the weak strength. At the strong strength, the favorable signal gives a certain purchase; the second rate applies after the unfavorable signal. Entry remains 0.625000 and 0.512521. The move loses no number or tie restriction.

### Welfare, sale terms, and empirical statements

40. **PASS — price-access comparison; composer item 10.** A.7 compares both economies at the same strong distribution. Both have unique full orders. Expected target proceeds and net acquisition surplus rise strictly.

41. **PASS — no added preparation lowers net surplus; composer item 10.** The statement concerns expected surplus conditional on the information that permits preparation. A.7 gives the gain per added preparation as

    \[
    B_1(M)-c_H+pF_1(p)>0.
    \]

    The revised nonnegative conclusion is valid and removes the former claim that each separate term must be positive. It does not assert a gain in every realized auction.

42. **PASS — payment-rule support; coordinator repair.** The final support is \([0,\bar r]\) with \(0<\ell<\bar r<h\), exactly as in A.7. The earlier assertion that all incumbent values lie between the two class values was incorrect. The repair restores the appendix hypothesis.

43. **PASS — “never raises the challenger's profit”; composer item 11.** A.7 gives \(g_{\theta,\omega}=(1-\omega)\mathbb E[(\theta-R)_+]\). A first-order stochastic increase of \(R\) cannot raise this quantity. This is precisely weak decrease, with equality allowed.

44. **PASS — spread moves only in the stated direction; composer item 11.** A.7 gives

    \[
    \Delta_\omega=\omega(h-\ell)+(1-2\omega)\mathbb E[(R-\ell)_+].
    \]

    The expectation cannot fall with incumbent strength. At seller weights below one half, the spread cannot fall. At weights above one half, it cannot rise. At one half, it remains constant. A zero change remains possible. The strictness condition and \((h-\ell)/2\) value are unchanged.

45. **PASS — moved payment example.** For \(R>\ell\), the support restriction still gives \(R<h\). A.7 supplies both payments and sensitivities \(1-\omega\) and \(\omega\). The “exactly when” comparison remains valid. The benchmark coefficient remains \(13/20\).

46. **PASS — reserve event definitions and table header.** Preparation, sale, and two admissible bidders retain their different definitions. “Entry” names the preparation probability throughout the model and A.7. No table cell changes.

47. **PASS — empirical entry floor and control pointer; composer item 12.** A.3 establishes the return to the floor with informative prices. Section 4 now supplies A.6's full control condition. Deleting its duplicate in Section 8 does not broaden the referenced control.

48. **PASS — price spread and impact definitions; composer item 12.** A.8 defines the same execution-price spread and both impacts. Section 8 retains the benchmark, prior, band, and full-trade interval. The exact recruitment equivalence and both component claims are unchanged.

49. **PASS — empirical spread numbers; composer item 12.** The unchanged displays are 0.786299, 90.2%, 0.077020, 0.108469, and the ceiling drop 0.861835. “Price spread” distinguishes this object from the target-payoff spread without changing either formula.

50. **PASS — counts and incentives.** A.8 gives the closed feasible-share interval under IM, from approximately 0.250299 to 0.760000. The revised prose preserves both restrictions and the upper endpoint. The alternative share remains 0.444444 and its price spread remains 0.778935.

### Conclusion and source-only deletion

51. **PASS — three unique outcomes on an open parameter set.** A.3 establishes the claim, including the very strong incumbent. “Parameters” does not change its domain.

52. **FAIL — entry rises during mixed purchases and stays constant after full purchases; composer item 13.** The strict-rise part agrees with A.4. The plateau needs its upper limit and an unambiguous comparison pair. Apply F2.

53. **PASS — conclusion, full-trade reserve condition.** This is the same repaired implication as entry 10. A.7 supports it.

54. **PASS — A.1 source-comment deletion in `62117e5`.** The deleted comment proposed a future extension. It was not rendered manuscript text. No mathematical statement or scope changes.

## Disposition

The control repair, reserve repairs, payment support repair, and transfer to Appendix A.6 pass. No formula or numerical display changes incorrectly. Apply F1 and F2 before certifying every revised summary against Appendix A.
