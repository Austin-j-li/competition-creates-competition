# Accuracy review

1. **High — W3: the seller's incentive does not establish an uninformative message.**

   The claim “a seller gains from entry in either class” turns a weak inequality into a strict gain. The claim about the message also exceeds the result.

   Source: `flashcards.tex:158–160`; `overleaf/slot/appendix/A7_welfare.tex:145–159`; `overleaf/slot/sections/03_competition_information.tex:15–17`. Card locations in this report refer to `audit/upgrade_cards_2026_11_03/flashcards.tex`.

   Under full admissibility,
   \[
   t_L-t_0=pF(p)+\int_p^\infty[1-F(y)][1-G_L(y)]\,dy\ge0.
   \]
   Equality is possible. In the point-value example, for \(p=1/2\) and \(r>1\),
   \[
   t_L-t_0=\frac12-\frac1{8r}>0.
   \]
   Thus the baseline example does give a strict gain in both classes. But when the reserve excludes the entire low class, \(t_L=t_0\). Low-class preparation then adds no proceeds.

   Even strict gains do not specify the information in a message. The paper specifies neither seller messages nor banker incentives. A claim that such messages carry little news needs a separate communication argument. The tag “My reasoning, not in the paper” is appropriate, but it does not cure the inference.

   **Replace with:** “A credible direct signal can support the same preparation decision. In the baseline example, the seller gains from preparation in both classes. This gives a reason to question an unsupported good-fit claim. It does not prove that the claim carries no news. If the reserve excludes the low class, low-class preparation adds no proceeds. I do not solve seller communication or banker incentives. My result concerns the return to information conveyed through trade.”

2. **High — W1 and J9: the reserve range omits its cost condition and extends beyond the calculation.**

   W1 says, “Below \(0.10\), the price still recruits, but entry is already high at the weak strength.” The reserve note does not establish this for all smaller ready shares. J9 states rounded cutoffs as exact inequalities and omits the choice of \(k\).

   Source: `flashcards.tex:151,237`; `audit/upgrade_cards_2026_11_03/reserve_check.md:157–171,193–211`.

   The calculation requires
   \[
   \frac1{60}<k<\frac{2\rho\kappa}{3},\qquad
   \rho>\frac1{40\kappa}=0.0929570457\ldots.
   \]
   With \(k=0.02\) fixed, H2 instead requires \(\rho>0.1115484549\ldots\). The note changes \(k\) to \(0.017\) at \(\rho=0.10\).

   The exact crossover values are \(\rho_a=0.1040612952\ldots\) and \(\rho_b=0.2145281832\ldots\). At either crossover, the endpoint \(p=10\) can create tied optimal entry outcomes. The calculation does not classify all equilibria below \(0.0929570457\ldots\).

   **Replace the W1 ready-share answer with:** “For point values, the pattern holds between ready shares of about \(0.1041\) and \(0.2145\), with the stated endpoint convention. The order cost must lie in the theorem's window. Between about \(0.0930\) and \(0.1041\), optimal entry exceeds the floor at both first strengths. Below that range, this calculation gives no general conclusion. Narrow bands preserve the pattern at \(\rho=0.15\); their exact range remains open.”

   **Replace J9 with:** “Choose \(1/60<k<2\rho\kappa/3\). Under the reserve note's limiting-endpoint convention, the pattern is floor, above floor, floor for \(\rho_a<\rho\le\rho_b\). Here \(\rho_a\approx0.1040612952\) and \(\rho_b\approx0.2145281832\). If \(p=10\) is allowed, tied optima change the endpoint conclusions. H2 admits some \(k\) exactly when \(\rho>1/(40\kappa)\approx0.0929570457\).”

3. **High — E7 and script frame 16: the research condition needs the optimal capped intensity, not just the cap.**

   E7 uses \(\hat\lambda\) without a definition. It also omits the quadratic cost and the condition \(\tau>1/2\). The script says “the top belief at capped research reaches tau” without defining that research level. A feasible cap alone does not establish optimal research or recruitment.

   Source: `flashcards.tex:127`; `overleaf/slot/slides_script.md:267–271`; `overleaf/slot/sections/05_research.tex:4–5,38–58`; `overleaf/slot/slides.tex:590–606`.

   **Replace E7 with:** “Assume ranked classes, \(\pi=1/2\), \(g_H>g_L\), \(\tau>1/2\), and the default tie rules. Private research costs \(a\lambda^2/2\) and has cap \(\bar\lambda<1\). For \(\Delta_T>2k\), define \(\lambda_R\) by
   \[
   2a\lambda_R=\Delta_Tm_{\lambda_R}-k+
   (\rho\Delta_Tm_{\lambda_R}-k)_+.
   \]
   Set \(\hat\lambda=\min\{\lambda_R,\bar\lambda\}\). The equilibrium with recruitment exists exactly when \(\Delta_T>2k\) and \(\tau\le M_{\hat\lambda}\). On this branch, research rises with the spread until the cap. As research rises, total and high-class entry rise, while low-class entry falls.”

   **Replace script line 269 with:** “Keep ranked classes, prior one half, a positive rival profit gap, and tau above one half. Use the default tie rules. Research equals the smaller of the optimal interior root and the cap. The equilibrium with recruitment exists exactly when the spread exceeds twice the order cost and the top belief at that research level reaches tau.”

4. **High — W2: the legal answer lacks support and has the wrong tag.**

   “Research with no breach at the source is lawful in the US; a tip from the deal team is not” states categorical legal conclusions. The cited paper passages establish neither conclusion. The final “In the paper” tag conflicts with the card's own source note. The source note identifies an outside note but gives no inspectable legal authority.

   Source: `flashcards.tex:156–157`; `overleaf/slot/sections/02_model.tex:106–109` describes the trader's research, without those legal conclusions.

   **Replace that follow-up with:** “The paper assumes independent research on the target. It does not establish the legal status of a particular trade or source. I cannot give a legal defence from this paper.”

   Tag that follow-up **“No full defence”**. Keep **“In the paper”** only on the economic statements that the cited sections support.

5. **Medium — W8, W16, and the ‘Do not say’ guidance: weak class ranking is insufficient.**

   “For every ranked pair of classes and every prior” omits the strictly positive mean gap and the interior prior. C3 defines ranking with weak dominance, which permits identical classes. Identical classes give \(\Delta_T=0\), so H2 cannot hold with \(k>0\).

   Source: `flashcards.tex:96,175,197,247`; `overleaf/slot/appendix/A6_robustness.tex:159–169`.

   **Replace the general claim in each location with:** “For every ranked pair with finite means and a strictly higher high-class mean, and every interior prior, suitable strengths and costs exist. This result uses uniform incumbents and preserves the other stated primitives.”

6. **Medium — W6: distinguish the no-entry equilibrium from an uninformative equilibrium, and retain the tie conditions.**

   The interval and the rise-then-flat branch survive direct derivation. The sentence “It removes the silent equilibrium” is too broad. The positive-floor theorem still has an uninformative equilibrium at the weak strength. Also, zero floor alone does not imply a no-entry equilibrium: the prior must fail to justify preparation.

   Source: `flashcards.tex:168–170`; `overleaf/slot/sections/04_equilibrium_results.tex:19–29,43–44`; `overleaf/slot/appendix/A1_payoffs.tex:81–96`; `overleaf/slot/appendix/A4_coexistence.tex:18–33,47–63,89–103`. The last appendix assumes a positive floor; its conclusions cannot simply be cited at \(\rho=0\).

   Here is the direct zero-floor calculation. Keep the example's other primitives and its default tie rules. Write \(s\) for the high class's purchase probability, conditional on its slot. The low class abstains. For \(1<r<10\),
   \[
   \Delta(r)=\frac{(r-1)^2}{2r},\quad
   g_H=10-\frac r2-\frac1{8r},\quad
   g_L=\frac3{8r},\quad
   \tau=\frac{6-g_L}{g_H-g_L}.
   \]
   Bayes' rule after a purchase gives
   \[
   \mu_+(s)=\frac{b+\lambda s}{2b+\lambda s},\qquad
   1-\mu_+(s)=\frac b{2b+\lambda s}.
   \]
   A purchase recruits fully. High-class indifference therefore requires
   \[
   \Delta\frac b{2b+\lambda s}=k,
   \qquad
   s=\frac b\lambda\left(\frac\Delta k-2\right).
   \]
   The branch starts where \(\Delta(1-\tau)=k\), at \(r_A=1.3939579203\ldots\). It reaches \(s=1\) where \(\Delta(1-M)=k\), at \(r_F=1.4671270413\ldots\). Full purchases recruit through \(\tau=M\), at \(r_C=3.5926585188\ldots\).

   Sale and no order both have price \(t_0\) and zero entry. The rival therefore pools these orders. Its belief at that price is
   \[
   \mu_{\mathrm{pool}}=
   \frac{1-b-\lambda s}{2-2b-\lambda s}<\frac12<\tau.
   \]
   The purchase price is \(t_L+\Delta\mu_+>t_0\), so the rival distinguishes it from the pooled price. The low class's deviations give
   \[
   U_L(-1)=-k<0,\qquad
   U_L(1)=-\Delta\mu_+-k<0,
   \]
   against zero from abstention. A high-class sale also gives \(-k\). These deviations do not destroy the branch.

   Entry on this branch is
   \[
   E(r)=\begin{cases}
   b\Delta(r)/(2k),&r_A\le r\le r_F,\\
   b+\lambda/2,&r_F\le r\le r_C.
   \end{cases}
   \]
   It rises from \(0.2722464746\ldots\) to \(0.3636759246\ldots\), then stays flat. The mixed part requires the informed trader to mix at indifference. The endpoints require full preparation at the purchase threshold.

   In this example, the silent no-entry equilibrium also exists: prior gross profit never exceeds the prior mean value \(5.5<6\). All prices then equal \(t_0\), and either nonzero deviation loses \(k\). The active branch therefore establishes possible entry, not a unique prediction.

   **Replace W6's main answer with:** “In this example, zero floor permits a silent no-entry equilibrium at every strength. It also permits an active branch under the default tie rules. Entry rises from about 0.2722 at \(r=1.394\) to 0.3637 at \(r=1.467\). It stays there through \(r=3.593\). The low class abstains throughout this branch. Thus zero floor does not rule out the rise, but it leaves coexistence. The positive floor and the main conditions give one outcome at the three comparison strengths. The weak outcome remains uninformative.”

7. **Medium — W2: “the trader never does” contradicts the point-value example.**

   The answer says the rival learns its exact value after preparation, “and the trader never does.” With point values, knowledge of the class already reveals the value. C6 and the current script state this exception correctly.

   Source: `flashcards.tex:99,154`; `overleaf/slot/slides_script.md:127`; `overleaf/slot/numbers.tex:5073–5074`.

   **Replace with:** “After preparation, the rival knows its exact value. The trader knows the class and has no further value information. In the point-value example, class knowledge already identifies the value.”

8. **Medium — W15: the payment-rule result is narrower than general negotiation.**

   The sign claim omits verifiable values, the enforceable fallback, point classes, and the support restriction. “The second-price case is \(\omega=0\)” also omits the zero reserve. At the example's positive reserve, the second-price transfer is not simply \(\min\{R,\theta\}\).

   Source: `flashcards.tex:194–195`; `overleaf/slot/appendix/A7_welfare.tex:95–111,115–136`.

   **Replace with:** “The paper studies one negotiation rule with verifiable values, zero reserve, and an enforceable fallback at the next bidder's value. Each class has one value, with \(0<\ell<\bar r<h\). With seller weight \(\omega\), the spread changes weakly with the sign of \(1-2\omega\). At \(\omega=0\), the rule matches a second-price auction with zero reserve. This is a result for that institution, not for negotiation in general.”

   Keep the tag **“In the paper”** on this narrower statement.

9. **Medium — E8: the counterexample outside the theorem becomes a universal claim.**

   “Outside this region, the prior already pays” does not follow. The paper supplies one region where the prior pays. Other departures from the main conditions can leave prior profit below the high cost.

   Source: `flashcards.tex:128`; `overleaf/slot/appendix/A7_welfare.tex:81–91`.

   **Replace the last sentence with:** “Outside this region, the prior can already justify preparation. If a sale then deters preparation, price access can lower expected proceeds.”

10. **Medium — A1 and A3: the mechanism uses weak changes, not necessary strict changes.**

   A1 says strength “cuts the rival's profit at every belief.” A3 says proceeds “then depend more” on synergy. Both changes can be zero. Strict changes require the positive integrals stated in Proposition 1.

   Source: `flashcards.tex:53,55`; `overleaf/slot/sections/03_competition_information.tex:34–41`.

   **Replace A1's second substantive sentence with:** “A stronger incumbent weakly lowers the rival's profit at every belief, but it can widen what shareholders gain from good synergy.”

   **Replace A3 with:** “The sale splits one rival value between shareholders and the rival. A stronger incumbent can move that split toward shareholders. Shareholder proceeds can then depend more on synergy, so information about synergy can become more valuable in the stock. If trade covers its cost, a purchase can raise the rival's belief enough to justify diligence.”

11. **Low — F8: a value equal to the reserve can win.**

   “A rival win needs its bid above the incumbent's and the reserve” excludes an admissible bid equal to the reserve. Such a rival wins when the incumbent fails the reserve.

   Source: `flashcards.tex:141`; `overleaf/slot/appendix/A1_payoffs.tex:60–74`; `overleaf/slot/sections/02_model.tex:92–102`.

   **Replace with:** “Preparation, sale and rival ownership are different events. Preparation pays the cost. A sale needs an admissible bid. The rival wins when its value meets the reserve and exceeds the incumbent's value, apart from zero-probability value ties.”

12. **Low — Set B: nine ‘Next’ quotes are shortened sentences, not exact script cues.**

   Source: `flashcards.tex:72,78–83,87–88`. The exact replacements below use the current script. The card numbers are those printed in set B.

   | Card | Script source | Exact replacement after “Next:” |
   |---|---|---|
   | B2 | `overleaf/slot/slides_script.md:69` | “Dow, Goldstein and Guembel are the closest antecedent: real decisions feed back into information production.” |
   | B8 | `overleaf/slot/slides_script.md:157` | “This is a perfect Bayesian equilibrium with break-even prices set by competitive market makers.” |
   | B9 | `overleaf/slot/slides_script.md:171` | “Proposition one compares two distributions for incumbent value.” |
   | B10 | `overleaf/slot/slides_script.md:185` | “Define liquidity mass b as beta times the quantity one minus lambda.” |
   | B11 | `overleaf/slot/slides_script.md:199` | “These are gross gains before order cost k, for any order plan with Bayes beliefs, competitive prices and truthful bids.” |
   | B12 | `overleaf/slot/slides_script.md:213` | “Proposition two compares three economies with the same class laws, reserve, costs, prior and order opportunity.” |
   | B13 | `overleaf/slot/slides_script.md:241` | “The example fixes good-synergy value at ten and poor-synergy value at one.” |
   | B16 | `overleaf/slot/slides_script.md:277` | “Use Proposition two at the strong incumbent F one.” |
   | B17 | `overleaf/slot/slides_script.md:287` | “Keep ranked classes, positive spread and rival gross-profit gap, full informed orders, and prior pi below threshold tau.” |

Fully checked: A, B, C, D, E, F, G, H against the paper's local citations, and J; also the specified script diff, current speech, word counts, and cumulative times.
