# Formal model and notation advice

Use named symbols, Bayesian beliefs, competitive prices, and formal propositions. Keep one plain intuition sentence below each result. Preserve the required player names.

Source checks: paper §2–§5, §8, and Appendices A.1–A.8; slidepack S1–S16; Beamer backups B1–B15. The [model](../../overleaf/slot/sections/02_model.tex) and [equilibrium definition](../../overleaf/slot/appendix/A1_payoffs.tex) control the drafts. This report concerns mathematical content; it does not assess rendered layout.

## 1. Definitions slide

Put **“Model: values and preparation costs”** immediately before current Slide 4, as the model block's first slide. Move Slide 2's literature table to B12; retain its contribution sentence in the opening. This creates space without a longer deck. Current slide numbers below remain reference labels.

Define primitives here, market objects on Slide 4, and derived objects beside their first equations. Do not put the entire B15 dictionary first.

**Exact face**

**Model: values and preparation costs**

A listed target has standalone value zero. All strategic agents are risk neutral. Values and costs are per target share.

| Object | Definition |
|---|---|
| First buyer's value \(R\) | \(R\sim F\); public continuous distribution \(F\), with support \([0,\bar r]\) and upper bound \(\bar r\). The first buyer is prepared. |
| Second buyer's class \(j\) | \(j\in\{H,L\}\): good synergy \(H\), poor synergy \(L\). Prior \(\pi=\Pr(j=H)\in(0,1)\). |
| Second buyer's value \(\theta\) | Conditional value law \(G_j\): \(\theta\mid j\sim G_j\), with finite means. Preparation reveals \(\theta\) and permits a bid. |
| Preparation cost \(C\) | \(\Pr(C=0)=\rho\in(0,1)\); otherwise \(C=c_H>0\). |
| Reserve \(p>0\) | Cash second-price auction; bids equal to \(p\) are admissible. |

**Class ranking:** \(G_H(y)\le G_L(y)\) for every \(y\), and \(G_H(p^-)=G_L(p^-)=0\).

The pair \((j,\theta)\), value \(R\), cost \(C\), and slot draws are mutually independent.

**End face.** Class ranking orders distributions, not every pair of realized values. Atoms in \(G_j\) are allowed; extend \(F\) by unity above \(\bar r\). The subscript in \(c_H\) means high cost; cost and synergy are independent.

## 2. Streamlined Slide 5

Slide 4 first defines order \(q\), observed order flow \(X\), price \(P\), and terminal payoff \(V_T\). Order values \(-1,0,1\) mean sell, abstain, and buy.

**Exact face**

**Information and choices**

All players know the primitives and the sale rule. The table lists additional information.

| Player | Observes | When | Chooses |
|---|---|---|---|
| Seller | Public primitives | Before trade | Commits to the auction with reserve \(p\) |
| First buyer | Own value \(R\) | Before its bid | Bid \(R\) if \(R\ge p\); otherwise no bid |
| Second buyer | Price \(P\), then own cost \(C\) | Before preparation | Prepare or stay out |
| Second buyer | Own value \(\theta\) | After preparation | Bid \(\theta\) |
| Informed investor | Class \(j\) | Before its order | Order \(q\in\{-1,0,1\}\) if selected |
| Liquidity trader | No private class signal | At its slot | Exogenous order: \((-1,0,1)\) with probabilities \((\beta,1-2\beta,\beta)\) |
| Market makers | Order flow \(X\) | After the order | Price \(P(X)=\mathbb E[V_T\mid X]\); absorb the order |

Before preparation, the second buyer sees neither \(X\), \(j\), \(\theta\), nor \(R\). The informed investor sees \(j\), not \(\theta\).

Market makers and the second buyer do not observe trader identity. Neither buyer trades target shares.

**End face.** The seller's reserve is fixed in the baseline; this row introduces no optimal reserve problem. Beliefs are deductions, not extra observed signals.

## 3. Slides 4–7

| Slide | Formal content | Speech |
|---|---|---|
| 4: Order flow and sequence | Define presence probability \(\lambda\in(0,1)\), liquidity probability \(0<\beta\le1/3\), order \(q\in\{-1,0,1\}\), and nonzero-order cost \(k>0\). Define observed order flow \(X\), price \(P(X)\), and terminal share payoff \(V_T\). The investor supplies the whole order when selected; otherwise liquidity supplies it. Sequence: commitment; order; price; cost and preparation; bids and payoffs. | The informed investor's research concerns customers, technology, and demand. Explain alternative arrival; do not describe additive noise. |
| 5: Information | Use the face above. | Explain why class information can precede value discovery. Remove industry stories and “portfolio gaps.” |
| 6: Auction payoffs | Show the definitions below. | Explain target proceeds and the second buyer's gross auction profit. Remove “two pockets” from faces. |
| 7: Equilibrium | Use the tuple and conditions below; B8 supplies Bayes fractions. | Prices anticipate the real preparation decision. A unilateral order deviation faces fixed price and preparation rules. |

Slide 6, for a prepared second buyer with value \(\theta\ge p\):

\[
t(\theta)=\mathbb E_R[\max\{p,\min(R,\theta)\}],\quad
g(\theta)=\mathbb E_R[(\theta-\max\{p,R\})_+],\quad t(\theta)+g(\theta)=\theta.
\]

Name \(t\) “expected target proceeds” and \(g\) “gross auction profit.” Define class means \(t_j=\mathbb E_j[t(\theta)]\), \(g_j=\mathbb E_j[g(\theta)]\), no-entry proceeds \(t_0=p[1-F(p)]\), shareholder spread \(\Delta_T=t_H-t_L\), and expected buyer profit \(B(\mu)=g_L+\mu(g_H-g_L)\). These are expectations, not realized payments.

**Slide 7: Equilibrium with competitive prices.** Follow Definition A.1 exactly:

\[
\mathcal E=(\sigma_H,\sigma_L,\mu,P,\bar\mu,\zeta),
\qquad e(x)=\rho+(1-\rho)\zeta(P(x)).
\]

Here \(\sigma_j\) is the class's order distribution; \(\zeta\) is high-cost preparation probability; \(e(x)\) is entry after price \(P(x)\).

1. **Order beliefs:** \(\mu(x)=\Pr(H\mid X=x)\), by Bayes' rule.
2. **Price beliefs:** \(\bar\mu(\bar P)=\Pr(H\mid P(X)=\bar P)\), by Bayes' rule over all orders with that price.
3. **Preparation:** zero cost always prepares; \(\zeta(\bar P)=\mathbf1\{B(\bar\mu(\bar P))\ge c_H\}\).
4. **Prices:** \(P(x)=t_0+e(x)[t_L-t_0+\Delta_T\mu(x)]\).
5. **Orders:** \(\operatorname{supp}\sigma_j\subseteq\arg\max_{q\in\{-1,0,1\}}U_j(q)\), where \(U_j(q)=q[t_0+e(q)(t_j-t_0)-P(q)]-k\lvert q\rvert\).
6. **Bids:** prepared buyers bid their values when admissible.

An indifferent investor may mix; an indifferent high-cost second buyer prepares. Liquidity gives every order positive probability. Do not assert that prices reveal orders. With \(\rho>0\) and \(\Delta_T>0\), prices reveal order beliefs: \(\bar\mu(P(x))=\mu(x)\).

B8 should define liquidity probabilities \(\eta=(\beta,1-2\beta,\beta)\), class order probabilities \(f_j(x)=(1-\lambda)\eta(x)+\lambda\sigma_j(x)\), and both Bayes formulas:

\[
\mu(x)=\frac{\pi f_H(x)}{\pi f_H(x)+(1-\pi)f_L(x)},\quad
\bar\mu(\bar P)=\frac{\pi\sum_{x:P(x)=\bar P}f_H(x)}{\sum_{x:P(x)=\bar P}[\pi f_H(x)+(1-\pi)f_L(x)]}.
\]

“Equilibrium with competitive prices” matches the paper. “Perfect Bayesian equilibrium” alone omits the zero-profit price restriction and suggests a fully specified strategic market-maker game.

## 4. Results and backups

Maintain short glosses: “buyer profit \(B_F(\mu)\),” “shareholder spread \(\Delta_T\),” and “top belief \(M(\pi)\).” Keep the opening question and each result's intuition in plain words.

| Slides | Required formal statement or revision |
|---|---|
| 1–3 | Keep the question and feedback to a real decision. Replace pockets with target proceeds and auction profit. State seller commitment and the public decision interval. Move the literature table to B12. |
| 8 | **Proposition 1:** for a stronger distribution \(\widetilde F\le F\), \(B_{\widetilde F}(\mu)\le B_F(\mu)\) at every fixed belief. Under class ranking, \(\Delta_T(\widetilde F)\ge\Delta_T(F)\). Show \(\Delta_T+g_H-g_L=\mathbb E_H\theta-\mathbb E_L\theta\). Intuition: “Strength shifts the class value gap from buyer profit to target proceeds.” Use weak signs. |
| 9 | **Lemmas A.1–A.2:** every order belief lies in \([m(\pi),M(\pi)]\); define their formulas from §2.3. The common bound needs \(\beta\le1/3\). Define threshold \(\tau=(c_H-g_L)/(g_H-g_L)\) only for \(g_H>g_L\). State price sufficiency with \(\rho>0,\Delta_T>0\). |
| 10 | **Proposition 2:** show (H1)–(H3) below and \(F_2\le F_1\le F_0\). All other primitives stay fixed. Unique outcomes satisfy \(\mathsf E_0=\mathsf E_2=\rho<\mathsf E_1=\rho+(1-\rho)(b+\pi\lambda)\). Define total entry \(\mathsf E\). Keep the order/price outcome table. |
| 11 | **Lemma A.3:** correct-order gross returns are \(K_H=e(1)\Delta_T[1-\mu(1)]\), \(K_L=e(-1)\Delta_T\mu(-1)\), and \(\rho\kappa\Delta_T\le K_j\le\Delta_T\). Define \(\kappa=\min\{m,1-M\}\) on Slide 9, before its use on 10. Wrong-signed orders earn at most \(-k\). |
| 12 | **Corollary 1:** define example values \(h,\ell\) and strength \(r\), with \(R\sim U[0,r]\). Keep the first example numbers here. Distinguish this family from general \(F\). |
| 13 | **Proposition A.2:** fix the joint law of class and signal, class value laws, and independent cost law. Then \(\mathsf E_0-\mathsf E_1=\Pr\{B_1(\mu(S))<C\le B_0(\mu(S))\}\ge0\), where \(S\) is the fixed signal. Require \((\theta,R)\mid(j,S)\sim G_j\otimes F_i\). Keep “The reversal requires endogenous price informativeness.” |
| 14 | **Proposition 4:** at \(\pi=1/2\), \(\Delta_T>0\), \(g_H>g_L\), \(\tau>1/2\), and default ties, the recruitment equilibrium exists iff \(\Delta_T>2k\) and \(\tau\le M_\lambda\) at \(\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}\). Define research cost \(a\lambda^2/2\), cap \(\bar\lambda\), and \(\lambda_R\) via B11's full equation. Research is unobserved; deviations hold conjectures fixed. Research rises strictly with the spread below the cap. Entry equals \(\rho+(1-\rho)[\beta+(1/2-\beta)\lambda]\), with positive slope in research. |
| 15 | **Proposition A.10:** under full two-sided trade and \(\pi<\tau\), \(\bar f(1)I_+-\bar f(-1)I_->0\iff e(1)>\rho\). Define order frequency \(\bar f(x)=\Pr(X=x)\), purchase impact \(I_+=P(1)-P(0)\), and sale impact \(I_-=P(0)-P(-1)\). Raw impacts suffice at \(\pi=1/2\). |
| 16 | Keep the conclusion verbal and conditional. Price-access welfare concerns \(F_1\) under Proposition 2, not optimal disclosure or sale design. |
| B1 | Repeat exact hypotheses. Ownership rises iff \(e_HW_H(F_1)>\rho W_H(F_0)\). Define \(W_j(F)=\mathbb E_j[F(\theta)\mathbf1\{\theta\ge p\}]\). |
| B2 | Use the paper's outside research description. Remove biotech and legal claims. |
| B3 | Retain Proposition 3's exact coexistence inequalities and default ties. Replace “moods” with equilibria. Interval claims require the stated path conditions. |
| B4 | Restore each appendix proposition's hypotheses. “Any ranked classes” requires a positive mean gap and suitable uniform first-buyer distributions and costs. Private-signal notation must distinguish \(S_I,S_C,\alpha_I,\alpha_C\). |
| B5 | Proposition A.7: \(\mathcal R^1>\mathcal R^0\), \(\mathcal W^1>\mathcal W^0\) at \(F_1\); define proceeds and net surplus. Separate the payment-rule model. Its spread is \(\Delta_\omega=\omega(h-\ell)+(1-2\omega)\mathbb E[(R-\ell)_+]\), with \(R<h\), zero reserve, and point-mass classes. |
| B6–B8 | Retain the slot and expected payoffs. B7's equal-admissibility claim also needs dominance above the reserve and no class atom at the reserve. Replace B8 with all six conditions above, including \(\bar\mu\). |
| B9–B11 | Separate general distributions from example inputs. B10's threshold inequality does not replace (H2). B11 must retain \(2a\lambda=\Delta_Tm_\lambda-k+(\rho\Delta_Tm_\lambda-k)^+\) for interior research. Distinguish branch existence from uniqueness. |
| B12–B13 | Align literature emphasis with Slide 2. Continuous orders require their own belief conventions. Print Euler's constant upright: \(1+u=\mathrm e^{2/\xi}\). |
| B14–B15 | The winner gap conditional on preparation is \((M-m)(W_H-W_L)\); strict prediction requires \(W_H>W_L\). Distinguish presence \(\lambda\) from the informed share of nonzero orders. Correct B15: general \(R\sim F\); order belief \(\mu(x)\); price belief \(\bar\mu(P)\); order-conditioned entry \(e(x)\). Define \(e_r(\mu)\) separately when used. |

Slide 10's face must include:

\[
\begin{array}{ll}
\text{(H1)}&B_0(\pi)<c_H<B_1(M(\pi)),\\
\text{(H2)}&\Delta_0<k<\rho\kappa(\pi)\Delta_1,\\
\text{(H3)}&B_2(M(\pi))<c_H.
\end{array}
\]

Here \(B_i=B_{F_i}\), \(\Delta_i=\Delta_T(F_i)\), and \(b=(1-\lambda)\beta\). On Slide 9, define liquidity mass \(b\), relative informed mass \(u=\lambda/b\), and the belief bounds:

\[
m(\pi)=\frac{\pi}{\pi+(1-\pi)(1+u)},\qquad M(\pi)=\frac{\pi(1+u)}{\pi(1+u)+1-\pi}.
\]

Open-set existence refers to the paper's parameter construction, not every distribution path.

## 5. Notation budget

Replace seven symbols overall with **about ten recurring result objects**, plus local notation:

- Core: distribution \(F\), prior \(\pi\), belief \(\mu\), price \(P\), profit \(B\), spread \(\Delta_T\), bounds \(m,M\), threshold \(\tau\), and entry \(\mathsf E\).
- Local prerequisites: values and costs on Definitions; slot objects on 4; payoff functions on 6; strategies and price beliefs on 7.
- Result-specific objects: \(b,u,\kappa\) on 9; \(K_j\) on 11; example values on 12; research objects on 14; impacts on 15.

Allow about 40–45 symbol families across the main talk, including local objects; ten is the recurring core. Repeat short glosses after a slide gap. Every backup must define its local symbols. Keep \(p\) distinct from \(P\), \(R\) from \(r\), and \(e(x)\) from \(e_j\) and \(\mathsf E\).

The trade-off is more notation and model time for exact deductions. Recover that time from literature and repeated verbal explanations, not smaller type.

## Questions for the author

1. Can the literature table move to B12 to fund the definitions slide?
2. Can Slide 7 use “Equilibrium with competitive prices,” with the full six conditions in B8?
3. Keep “first buyer” and “second buyer” throughout? They are clear, although finance theory often uses role-based bidder names.
