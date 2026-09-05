---
bibliography: references.bib
link-citations: true
---

# Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders

**Austin Li**

## Abstract

A stronger acquirer can attract its own challenger. We study a listed target whose prospective buyer learns from stock prices before paying for acquisition diligence. Strengthening an incumbent reduces the challenger's acquisition profit at every fixed belief, but increases the sensitivity of target shareholders' proceeds to challenger quality. This induces informed trading and can reverse entry deterrence. Once the price-information experiment is fixed, conventional deterrence re-emerges. We characterize unique uninformative and informative outcomes and establish coexistence with asymmetric trading. The mechanism survives smooth noise, atomless preparation costs, and complementary signals: the buyer can have the more accurate signal. Holding competitive strength fixed, access to prices raises acquisition surplus net of diligence. A bargaining comparison identifies the payment property behind discovery. We formulate the seller's design problem when sale terms determine both acquisition payments and the information that brings buyers into the contest.

## 1. Introduction {#sec-introduction}

Where does takeover competition come from? A prospective acquirer must decide whether an opportunity warrants investigation before it knows enough to submit an executable bid. A powerful rival makes that investigation less attractive: it reduces the probability of a profitable acquisition and the rents available if the challenger wins. Yet the same rival can make the target's shares more informative about whether the challenger should investigate. We show that this second force can dominate the first. **A stronger acquirer can recruit the challenger it would ordinarily deter.**

The distinction is between the return to acquiring a company and the return to trading its shares. When an excellent challenger faces weak competition, much of its acquisition advantage remains with the challenger. Its quality matters for the value created by a transaction but need not substantially change what target shareholders receive. Stronger competition transfers more of that advantage into the target's sale price. Information about the challenger consequently becomes more valuable to investors trading target equity. Their orders reveal information that the challenger uses before committing resources to diligence and participation.

This mechanism joins a corporate-control contest to a financial market in which prices are rational and traders anticipate the real decisions their orders influence. It does not rely on an unanticipated takeover premium. The market maker prices the entry response. What remains profitable to trade on is the difference between high- and low-quality acquisition outcomes after that response has been priced.

We begin with a committed cash auction whose acquisition payments are disciplined by the strongest competing bid. An incumbent is already prepared to participate. A potential challenger learns from the target's price before paying a privately realized preparation cost and evaluating its acquisition value. An informed investor trades the target's shares against noise demand. The incumbent's value distribution is the comparative-static primitive. We derive the acquisition payoffs, solve inference from the price actually observed by the challenger, and verify global trading incentives over continuous orders, allowing mixed strategies.

The main result compares regions with different equilibrium information. With a weak incumbent, the information-sensitive spread in target proceeds is too small to support informed trading. With a stronger incumbent, informed trading is uniquely optimal and sufficiently favorable prices induce additional challenger entry. Acquisition profits decrease at every fixed posterior throughout this comparison. Entry rises because the information supplied by the market changes.

The equilibrium correspondence contains additional economics. When orders are fixed, the price-information experiment is fixed, and stronger competition weakly reduces entry. Before orders reach their bounds, asymmetric trading can change the experiment: buying after favorable information and selling after unfavorable information need not have equal magnitudes. We establish informative asymmetric equilibria with increasing entry across certified intermediate strengths, coexisting with an uninformative equilibrium. Our correspondence display preserves these distinct outcomes rather than selecting a curve. At still higher strengths, the bounded likelihood ratios of the benchmark noise law can make expensive entry infeasible even though trading remains informative.

The information interpretation is complementary knowledge, not a presumption that outsiders know more than prospective buyers. We give the buyer and the investor different noisy signals. The buyer can have the more accurate signal and still use the incremental information in prices. This extension rederives conditional participation and competitive pricing when the buyer's private information predicts entry even after the public price is observed.

We make the following contributions.

1. **Competition reallocates the returns to information.** We derive an acquisition-stage opposition, general in the incumbent's value distribution: stronger competition raises the information sensitivity of target proceeds while lowering the challenger's acquisition profit at every posterior.
2. **Prices can reverse entry deterrence.** We prove the equilibrium entry reversal, the sufficiency of the observed price, and global best responses. We distinguish a changing information experiment from a fixed informative experiment and characterize both uniquely determined and coexisting outcomes.
3. **Discovery has institutional and real consequences.** We establish complementary-signal and smooth-distribution extensions, a matched surplus gain from access to prices, and a bargaining boundary identifying when runner-up-driven pricing supports the payoff opposition.
4. **Sale design becomes a problem of attracting information as well as buyers.** We specify the seller's continuation game and objective over the full reserve domain. The next result is a characterization of seller-optimal discovery and the role of commitment before information is revealed.

The acquisition mechanism is fixed in the entry theorem; the seller's choice is a separate optimization problem. That separation permits a sharp first result and identifies the next economic question. A seller choosing sale terms changes not only what an entrant pays but also whether investors have a reason to reveal the information that makes entry worthwhile.

## 2. Institutional setting {#sec-institution}

Our setting is a publicly visible, still-contestable opportunity involving a listed target. A lead buyer is prepared to bid, while another prospective buyer has not committed to the full diligence and transaction-preparation process. Target shares trade during that decision interval. An incumbent is an available acquirer, not the target's incumbent management; a challenger is a prospective competing acquirer, not an activist shareholder.

The information relevant to participation can be distributed across organizations. A buyer may know its own technology, operating capabilities, and integration capacity, while specialized investors know the target's customers or product market. Diligence combines these assessments into a transaction-ready valuation. The private signals in our extension capture this division: the investor's signal is different from the buyer's signal, even when the buyer's signal is more accurate.

We distinguish an expression of interest, costly investigation, and a committed bid. The takeover-process literature establishes the importance of competition and uncertainty before the visible final bidding stage [@BooneMulherin2007; @GentryStroup2019]. An illustrative process record is Imprivata's definitive merger proxy: an unsolicited approach was followed by deliberation over potential buyers, confidential outreach, and indications subject to further diligence. The record also describes concerns about disruption and information leakage [@Imprivata2016]. We use this example to motivate the separation between interest and costly participation, not as evidence that stock prices caused entry or that its confidential phase satisfied our public-visibility condition.

The institutional pilot therefore has a specific task: establish when the sale opportunity was public, which potential buyer decisions remained open, and what information prices could add before those decisions. A stock price existing during confidential negotiations is not enough. We require an observable interval in which another buyer could still decide whether to investigate a publicly understood opportunity.

We isolate target equity as the relevant traded claim. The bidders can be privately held; alternatively, their securities contain no additional information about the modeled match. Neither bidder trades the target in the benchmark. The investor has no control rights relevant to the sale. The sale procedure binds the whole company, so the mechanism concerns discovery before participation rather than dispersed-shareholder tendering. These choices separate our channel from toeholds and takeover free riding [@BulowHuangKlemperer1999; @GrossmanHart1980].

## 3. Related literature {#sec-literature}

The closest conceptual comparison is Dow, Goldstein, and Guembel [@DowGoldsteinGuembel2017]. Their real investment decision changes the private incentives to produce information in financial markets. We share the feedback between real decisions and information incentives. Our additional object is the division of acquisition rents between the claim traded by an investor and the buyer deciding whether to enter. We derive opposite movements in those returns from an acquisition contest and establish an entry-deterrence reversal. Information revelation by the investor is endogenous in our benchmark; the investor's acquisition of its signal is not.

Edmans, Goldstein, and Jiang [@EdmansGoldsteinJiang2015] show that corrective real decisions can discourage adverse-information trading even under rational pricing. We instead study how rival strength changes the information sensitivity of target equity and the set of willing acquirers. Their evidence on the effect of prices on takeovers [@EdmansGoldsteinJiang2012] establishes the importance of the price-to-control direction, but its takeover-trigger mechanism is not evidence that a challenger learns its acquisition match from prices. Luo [@Luo2005] studies learning from announcement reactions in completion decisions. Our participation decision occurs before the buyer set is fixed.

Fishman [@Fishman1988] develops preemptive bidding that deters costly competition. Hirshleifer and Png [@HirshleiferPng1989] study costly investigation, competing bids, and whether facilitating competition benefits target owners. Gentry and Stroup [@GentryStroup2019] analyze uncertainty before entry in takeover auctions. We retain the direct deterrence force and endogenize the separate market information available before investigation.

Levin and Smith [@LevinSmith1994] characterize auction entry and the coordination costs associated with potential bidders. Roberts and Sweeting [@RobertsSweeting2013] show how costly selective entry affects a seller's choice of sale procedure. These results make participation an institutional object. We add the effect of sale payments on information revealed through a distinct traded claim. Persico [@Persico2000] studies how auction formats shape bidders' incentives to acquire information. In our mechanism, the relevant financial trader is not an auction participant, and the claim on which it trades differs from an entrant's acquisition profit.

Betton, Eckbo, Thompson, and Thorburn [@BettonEtAl2014] analyze merger negotiations with stock-market feedback and the relation between runups and offer prices. Lin, Ma, Yang, and Zhu [@LinMaYangZhu2025] model negotiated payment methods, trading in the merging firms, and subsequent withdrawal. We study rival discovery and entry under cash consideration rather than choosing payment composition within an initiated bilateral deal. Cornelli and Li [@CornelliLi2002] explain how arbitrageurs' positions affect tendering and generate an informational advantage; our outside investor instead has information about a prospective buyer's match and does not determine tendering.

Recent auction-information work sharpens the distinction. Pernoud and Gleyze [@PernoudGleyze2026] study buyers' learning about their own values and competitors. Liu and Bernhardt [@LiuBernhardt2022] use post-auction market feedback in security-payment design. Carlin, Liu, Officer, Pernoud, and Tu [@CarlinEtAl2026] study bidder-pool choice and correlated acquisition values. Our market operates before participation, and the sale payment determines which information an outside investor has an incentive to reveal. The seller-design problem combines these margins rather than taking either the information experiment or the buyer pool as given.

## 4. Model {#sec-model}

### 4.1 Values, preparation, and the sale institution

We normalize the target's known standalone value to zero and express acquisition values and preparation costs per target share. Restoring the same known standalone component to every ownership outcome adds a constant to prices and payoffs without changing incentives. The informed order is measured in a small reference trading unit, not as ownership of the whole target.

The incumbent has private acquisition value $R\sim U[0,r]$. The distribution is conditional on public information at the start of the sale process. Increasing $r$ is a first-order stochastic strengthening. The incumbent learns its realization before bidding and incurs no further participation cost at this stage.

The challenger has acquisition value $\theta\in\{\ell,h\}$ with equal prior probabilities. We impose

$$
0<p<\ell<r<h.
\tag{1}
$$

The challenger initially does not know $\theta$. After observing the target price it privately learns a preparation cost $C$, equal to $c_L$ with probability $\rho$ and $c_H$ otherwise, where $0<\rho<1$ and $0\le c_L<c_H$. Paying the cost reveals its acquisition value and permits participation. Declining means absence. Preparation is sunk before bidding. Incumbent value, challenger value, preparation cost, and noise demand are mutually independent.

The seller commits publicly before trading to a cash second-price auction with reserve $p$. The highest admissible bidder acquires the target and pays the larger of the reserve and the highest competing bid. Without an admissible bid there is no sale. We implement truthful, weakly dominant bidding. Conditional on the competing bid, a bidder wants to win exactly when its value covers the payment required to win. Its own bid cannot lower that payment conditional on winning. A bid equal to the reserve is admissible; acquisition-value ties have no effect in the interior benchmark. Entry at an exactly zero net preparation payoff is prescribed, a convention that matters at a posterior plateau.

### 4.2 Trading, information, and timing

The investor observes $\theta$ and chooses $q\in[-1,1]$. It has no initial position, cannot bid for the target, and pays $k|q|$, where $k>0$. Its profit is

$$
q\{V_T-P(X)\}-k|q|,
\qquad X=q+Z,
\qquad f(z)=\frac{1}{2b}e^{-|z|/b},\quad b>1.
\tag{2}
$$

Here $V_T$ is the terminal target-share payoff and $Z$ is independent noise demand. Competitive market makers observe $X$ and set

$$
P(X)=\mathbb E[V_T\mid X],
\tag{3}
$$

anticipating preparation and the auction. The challenger observes $P$, not $X$.

The sale opportunity and rule are announced first. The investor then learns and trades. Market makers price aggregate demand. The challenger observes the price and cost, chooses preparation, and learns its value if it prepares. The bidders submit truthful bids, ownership changes if an admissible bid exists, and financial payoffs are realized.

### 4.3 Equilibrium and notation

An equilibrium comprises conditional probability distributions $\sigma_H,\sigma_L$ over orders, a measurable price function, Bayesian beliefs based on the observed price, optimal preparation for each cost realization, and truthful auction bidding. The investor optimizes over the entire order interval. A unilateral deviation holds the equilibrium pricing and preparation schedules fixed while changing the distribution of order flow reaching them. A comparison across values of $r$ instead resolves the entire equilibrium.

We use $t_0$ for expected target proceeds without entry, $t_H,t_L$ for proceeds conditional on entry and challenger quality, and $g_H,g_L$ for gross challenger acquisition profits. The payoff spread is $\Delta_T=t_H-t_L$, and $B_r(\mu)$ is gross challenger profit at posterior $\mu$. The posterior bounds are $m,M$; the expensive-entry threshold is $\tau$ and its order-flow counterpart is $x^*$. Favorable-flow probabilities conditional on quality are $\alpha_H,\alpha_L$. We denote total entry by $\mathsf E$, high-quality ownership by $\mathsf O_H$, and target revenue by $\mathcal R_T$. The boundaries $r_N,r_U,r_C$ distinguish pooling existence, sufficient full-order uniqueness, and expensive-entry feasibility.

## 5. Acquisition payoffs and the returns to information {#sec-payoffs}

### 5.1 The payment identities

A high-value challenger wins and pays $\max\{p,R\}$. With a low-value challenger, the winner pays $\max\{p,\min(R,\ell)\}$. Without a challenger, the incumbent pays the reserve exactly when it meets that reserve. Integration gives

$$
\begin{aligned}
t_0&=p\left(1-\frac p r\right),&
t_H&=\frac r2+\frac{p^2}{2r},&
t_L&=\ell-\frac{\ell^2-p^2}{2r},\\
g_H&=h-\frac r2-\frac{p^2}{2r},&
g_L&=\frac{\ell^2-p^2}{2r},&
\Delta_T(r)&=\frac{(r-\ell)^2}{2r}.
\end{aligned}
\tag{4}
$$

At posterior $\mu$, the challenger's gross profit and the relevant derivatives are

$$
\begin{aligned}
B_r(\mu)&=g_L+\mu(g_H-g_L),\\
\Delta_T'(r)&=\frac12-\frac{\ell^2}{2r^2}>0,\\
g_H'(r)&=-\frac12+\frac{p^2}{2r^2}<0,
\qquad g_L'(r)=-\frac{\ell^2-p^2}{2r^2}<0.
\end{aligned}
\tag{5}
$$

Thus $\partial B_r(\mu)/\partial r<0$ for every fixed posterior. The decline in acquisition profitability and the increase in target-payoff sensitivity are different implications of the same sale rule.

### 5.2 General incumbent distributions {#prop-payoffs}

**Proposition 1 (analytical).** *Let the incumbent have a continuous distribution $F$ on $[0,\bar r]$, with $0<p<\ell<\bar r<h$. A first-order stochastic strengthening of $F$ weakly increases the high–low spread of target proceeds and weakly decreases the challenger's gross acquisition profit at every fixed posterior. The comparisons are strict when the distribution change has positive integral over the corresponding ranges below:*

$$
\Delta_T(F)=\mathbb E_F[(R-\ell)_+]
=\int_\ell^{\bar r}[1-F(u)]\,du,
\qquad
G_\theta(F)=\mathbb E_F[(\theta-\max\{p,R\})_+]
=\int_p^\theta F(u)\,du.
\tag{6}
$$

*We extend $F$ by unity above its support.*

The proof is the payment identity $T_H(R)-T_L(R)=(R-\ell)_+$. Stronger competition puts more weight where a high challenger, rather than a low challenger, changes the price paid to the target. The profit integrand moves in the opposite direction. Appendix [A.1](#pa-payoffs) supplies the case split and integral argument.

> **Figure 2 placeholder — The two returns.** File: `figures/two_returns.pdf`. Panel (a): $\Delta_T(r)$. Panel (b): $B_r(\mu)$ for $\mu\in\{m,1/2,M\}$. Hold all other primitives at the benchmark specification. Caption: “Incumbent strength raises the sensitivity of target proceeds while reducing challenger acquisition profit at every displayed belief.” Use common horizontal limits; no in-panel titles. Data specification: Online Appendix [C.1](online_appendix.md#oa-c-baseline).

## 6. Inference, participation, and residual trading profits {#sec-inference}

### 6.1 Posterior bounds before imposing a trading profile {#lemma-beliefs}

**Lemma 1 (analytical).** *For arbitrary mixed state-contingent orders on $[-1,1]$, the order-flow posterior and the posterior based on price lie in $[m,M]$, where*

$$
\begin{aligned}
a_H(x)&=\int f(x-q)\,d\sigma_H(q),\quad
a_L(x)=\int f(x-q)\,d\sigma_L(q),\\
\mu_X(x)&=\frac{a_H(x)}{a_H(x)+a_L(x)},\qquad
m=\frac1{1+e^{2/b}},\quad M=1-m.
\end{aligned}
\tag{7}
$$

**Proof.** For any feasible $q,q'$, the triangle inequality gives

$$
e^{-2/b}\le\frac{f(x-q)}{f(x-q')}\le e^{2/b}.
\tag{8}
$$

Integrating against $d\sigma_H(q)d\sigma_L(q')$ preserves both inequalities. Equal priors yield the bounds for $\mu_X$. Because $P$ is a function of $X$, the price posterior is $\mathbb E[\mu_X\mid P]$ and lies in the same interval. $\square$

### 6.2 Price sufficiency and optimal preparation {#lemma-price}

At a price-based posterior $\mu$, preparation is optimal exactly when $C\le B_r(\mu)$. Whenever $c_L<B_r(m)$, entry probability at every feasible price is at least $\rho$.

**Lemma 2 (analytical).** *Suppose $c_L<B_r(m)$. The observed price reveals $\mu_X$ almost surely. Entry and competitive pricing can be written as*

$$
\begin{aligned}
e_r(\mu)&=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\\
P_r(\mu)&=t_0+e_r(\mu)[t_L-t_0+\Delta_T\mu].
\end{aligned}
\tag{9}
$$

*The residual advantage of an informed buyer of shares in state $H$, and of an informed short seller in state $L$, is*

$$
\begin{aligned}
A_H(x)&=\mathbb E[V_T\mid H,x]-P(x)=e_r(\mu_X(x))\Delta_T[1-\mu_X(x)],\\
A_L(x)&=P(x)-\mathbb E[V_T\mid L,x]=e_r(\mu_X(x))\Delta_T\mu_X(x),\\
\rho m\Delta_T&\le A_H(x),A_L(x)\le\Delta_T.
\end{aligned}
\tag{10}
$$

**Proof.** Write $e(P)$ for entry averaged over the independent preparation cost. Conditional pricing implies

$$
P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X],
\qquad
\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}.
\tag{11}
$$

The denominator is positive, so the posterior is a measurable function of the price. Conditioning it again on price leaves it unchanged. The optimal preparation rule therefore gives (9). For construction, $P_r(\mu)$ is strictly increasing: the entry probability is nondecreasing and positive, while the bracket is positive and strictly increasing because $t_L\ge p>t_0$. Subtract the price from $t_0+e_r(\mu)(t_H-t_0)$ in state $H$, and reverse the subtraction in state $L$, to obtain (10). $\square$

This identity is the core feedback calculation. A publicly anticipated increase in acquisition proceeds cancels from the informed trader's profit. The remaining profit is the state-dependent component that noise trading prevents the market maker from fully identifying.

## 7. Competition creates competition {#sec-results}

### 7.1 The entry-reversal theorem {#thm-entry}

**Theorem 1 (analytical).** *Fix $0<p<\ell<r_0<r_1<h$, $0<\rho<1$, $b>1$, and $k>0$. Suppose*

$$
0\le c_L<B_{r_1}(m),
\tag{A1}
$$

$$
B_{r_0}(1/2)<c_H<B_{r_1}(M),
\tag{A2}
$$

$$
\Delta_T(r_0)<k<\left(1-\frac1b\right)\rho m\Delta_T(r_1).
\tag{A3}
$$

*At $r_0$, the unique equilibrium trading outcome is $q_H=q_L=0$, prices are uninformative, and entry is $\rho$. At $r_1$, the unique equilibrium trading outcome is $(q_H,q_L)=(1,-1)$, the price is informative, and entry strictly exceeds $\rho$. The probability that a high-value challenger acquires the target strictly increases. The strong-incumbent price experiment strictly Blackwell dominates the weak-incumbent experiment at the same noise law. These comparisons hold on a nonempty open set of primitives. Uniqueness concerns trading and on-path entry under truthful auction implementation and permits arbitrary mixed orders and continuous deviations.*

The conditions describe a region with inexpensive opportunities that are always worth investigating, expensive opportunities that need favorable information, and a trading wedge between the weak and strong economies' information incentives. None assumes that rivalry directly increases acquisition profit; equation (5) establishes the opposite.

The proof has a short economic sequence. The likelihood-ratio bound first controls beliefs under every possible trading strategy. The inexpensive preparation opportunity then ensures a positive entry floor. That floor makes the observed price sufficient and leaves a positive residual information advantage. At weak strength, even the largest possible advantage cannot cover the trading wedge. At strong strength, a global marginal-profit bound makes increasing the correctly signed order profitable throughout the order interval. Finally, the informative price crosses the expensive preparation threshold with positive probability.

For the central bound, fix a candidate equilibrium's residual schedules and set

$$
F_H(s)=\int f(x-s)A_H(x)\,dx,
\qquad F_L(s)=\int f(x+s)A_L(x)\,dx,
\qquad U_\theta(s)=sF_\theta(s)-ks.
\tag{12}
$$

The density satisfies $|f'|\le f/b$, giving $|F_\theta'|\le F_\theta/b$. Consequently,

$$
U_\theta'(s)\ge\left(1-\frac{s}{b}\right)F_\theta(s)-k
\ge\left(1-\frac1b\right)\rho m\Delta_T-k>0
\tag{13}
$$

almost everywhere in the strong economy. This controls every continuous deviation, not merely candidate first-order conditions. Appendix [A.2](#pa-entry) supplies each logical step, including equilibrium construction and the information ordering.

Under full orders the expensive buyer enters for $X\ge x^*$, where

$$
\begin{aligned}
\tau&=\frac{c_H-g_L}{g_H-g_L},&
x^*&=\frac b2\log\frac\tau{1-\tau},\\
\alpha_H&=1-\frac12e^{(x^*-1)/b},&
\alpha_L&=\frac12e^{-(x^*+1)/b},\\
\mathsf E&=\rho+\frac{1-\rho}{2}(\alpha_H+\alpha_L),&
\mathsf O_H&=\frac12[\rho+(1-\rho)\alpha_H].
\end{aligned}
\tag{14}
$$

Condition (A2) places $\tau\in(1/2,M)$ and $x^*\in(0,1)$.

### 7.2 Fixed information and exact boundaries {#prop-fixed}

**Proposition R1 (analytical).** *Hold the joint distribution of a signal, challenger quality, and preparation cost fixed as $r$ changes. If the posterior generated by that signal does not change with $r$, entry is weakly decreasing in $r$. It decreases strictly when the decline in gross profit crosses preparation costs on a positive-probability set of signal–cost realizations.*

The proof is pointwise: $\mathbf1\{C\le B_r(\mu)\}$ cannot switch from nonentry to entry as $B_r(\mu)$ falls. This applies within a region of fixed full orders. It does not apply merely because prices are informative: changing orders changes the information experiment.

### 7.3 Pooling, full orders, and expensive-entry feasibility {#prop-thresholds}

**Proposition 3 (analytical).** *Restrict attention to strengths in $(\ell,h)$ for which $c_L<B_r(m)$ and $B_r(1/2)<c_H$. Define*

$$
\begin{aligned}
\mathfrak r(d)&=\ell+d+\sqrt{d^2+2\ell d},\\
r_N&=\mathfrak r(2k/\rho),\qquad
r_U=\mathfrak r\left(\frac{k}{(1-1/b)\rho m}\right).
\end{aligned}
\tag{15}
$$

*Pooling exists exactly when $\rho\Delta_T(r)/2\le k$, equivalently $r\le r_N$. The stronger restriction $r<\mathfrak r(k)$ guarantees its uniqueness. The restriction $r>r_U$ guarantees unique full orders. Expensive entry is impossible in every equilibrium when $B_r(M)<c_H$. If the equality $B_r(M)=c_H$ has a solution in the specified domain, its unique crossing is $r_C$, given by the relevant root*

$$
r_C=\frac{Mh-c_H+\sqrt{(Mh-c_H)^2+M[(1-M)\ell^2-p^2]}}{M}.
\tag{16}
$$

*At $r_C$, the prescribed tie rule is retained.*

The exact pooling-existence boundary, a sufficient uniqueness boundary, and the expensive-entry feasibility boundary answer different questions. In particular, pooling existence does not exclude an informative equilibrium at the same strength. Under Laplace noise the maximum posterior occurs on a positive-probability tail, so indifference at $r_C$ cannot be discarded as a null event. Appendix [A.3](#pa-thresholds) derives the formulas and specifies their domain.

### 7.4 A rise and fall across uniquely determined economies {#cor-three}

**Corollary 3 (analytical).** *Let $r_0,r_1$ satisfy Theorem 1 and choose $r_2\in(r_1,h)$ such that $c_L<B_{r_2}(m)$, $B_{r_2}(M)<c_H$, and $k<(1-1/b)\rho m\Delta_T(r_2)$. Then each economy has a unique trading and entry outcome and*

$$
\mathsf E(r_0)=\rho<\mathsf E(r_1),
\qquad \mathsf E(r_2)=\rho.
\tag{17}
$$

We implement this comparison at $r_0=1.2$, $r_1=3$, and $r_2=3.6$. Entry is respectively 0.250000, 0.522757, and 0.250000. This finite nonmonotonicity result does not assign a unique outcome throughout the intermediate correspondence.

### 7.5 Asymmetric informative equilibria {#prop-certified}

**Proposition 4 (computer-assisted).** *At the benchmark primitives specified in Appendix [A.9](#pa-parameters), there exist informative equilibria $(q_H,q_L)=(1,-v_j)$ at strengths $r_j$ whose certified enclosures are*

$$
\begin{aligned}
r_{\mathrm a}&=1.55,&v_{\mathrm a}&\in[0.46031618,\,0.46031620],&\mathsf E_{\mathrm a}&\in[0.5450528898,\,0.5450528922],\\
r_{\mathrm b}&=1.60,&v_{\mathrm b}&\in[0.70747537,\,0.70747539],&\mathsf E_{\mathrm b}&\in[0.5487563062,\,0.5487563085],\\
r_{\mathrm c}&=1.65,&v_{\mathrm c}&\in[0.90333198,\,0.90333201],&\mathsf E_{\mathrm c}&\in[0.5513607988,\,0.5513608020].
\end{aligned}
\tag{18}
$$

*The entry intervals are strictly ordered upward. Each economy also admits pooling with entry $\rho$.*

The investor buys maximally after favorable information but chooses an interior short after unfavorable information. The latter problem is globally strictly concave. Interval sign changes establish exact interior best responses, and interval bounds on the favorable type's marginal profit exclude all smaller purchases. We therefore certify continuous-action equilibria rather than equating a small residual with equilibrium. Appendix [A.4](#pa-certificate) contains the proof steps and the inequalities completing the certificates. The online appendix gives the exact integration formulas and arithmetic protocol.

> **Figure 1 placeholder — The equilibrium correspondence.** File: `figures/equilibrium_correspondence.pdf`. Panel (a): entry against $r$, preserving separate pooling, full-order, asymmetric, and any mixed outcomes found. Distinguish analytically established regions, certified points, and numerical continuation; a failure to find another branch is not a uniqueness label. Mark $r_N,r_U,r_C$ with their distinct meanings. Panel (b): the low-information order magnitude $v$ along asymmetric candidates and certified enclosures, with full orders as the boundary. Do not interpolate across failed validation or a change of branch. Data specification: Online Appendix [C.2](online_appendix.md#oa-c-correspondence).

## 8. Information and institutions beyond the benchmark {#sec-extensions}

### 8.1 Smooth noise and atomless preparation {#cor-logistic}

**Corollary 1 (analytical).** *Replace Laplace noise by logistic noise with density*

$$
f_{\mathrm{log}}(z)=\frac{1}{4b}\operatorname{sech}^{2}\left(\frac z{2b}\right),\qquad b>1.
\tag{19}
$$

*Under (A1)–(A3), the unique trading outcomes and the entry and ownership comparisons of Theorem 1 remain valid.*

The log-density derivative is bounded in absolute value by $1/b$, which preserves the global trading argument. Under full orders, the posterior is strictly increasing and ranges over $(m,M)$. It approaches the bounds smoothly rather than becoming constant in the tails. If $A=e^{1/b}$ and $w=\sqrt{\tau/(1-\tau)}$, the entry threshold and favorable-flow probabilities are

$$
x^*_{\mathrm{log}}=b\log\frac{Aw-1}{A-w},\qquad
\alpha_H^{\mathrm{log}}=\frac1{1+e^{(x^*_{\mathrm{log}}-1)/b}},\qquad
\alpha_L^{\mathrm{log}}=\frac1{1+e^{(x^*_{\mathrm{log}}+1)/b}}.
\tag{20}
$$

### 8.2 Preparation-cost heterogeneity {#cor-costs}

**Corollary 2 (analytical).** *Replace the cost atoms by atomless low- and high-cost distributions with probabilities $\rho$ and $1-\rho$, supported respectively within $[c_L-\varepsilon_C,c_L+\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$. Suppose*

$$
\begin{gathered}
c_L-\varepsilon_C\ge0,\qquad c_L+\varepsilon_C<B_{r_1}(m),\\
B_{r_0}(1/2)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{r_1}(M),
\end{gathered}
\tag{21}
$$

*and retain (A3). Theorem 1's conclusions hold under either noise specification.*

Every low-cost realization participates at every feasible belief. High-cost realizations stay out at the weak prior and participate after sufficiently favorable strong-economy prices. The price is still strictly increasing in the posterior because the preparation-cost distribution generates a nondecreasing entry rule with a positive floor. Appendix [A.5](#pa-smooth) gives both corollary proofs.

The effect is not confined to widely separated acquisition values. The moderate-value specification has $h=2$, $\ell=1$, and satisfies each strict inequality of Theorem 1. Entry rises from 0.250000 to 0.526805. Appendix [A.5](#pa-smooth) also constructs a nonempty region for every $h>\ell$ by choosing the strengths near $\ell$ and a compatible trading wedge.

### 8.3 Complementary private information {#thm-signals}

We now give both the trader and the buyer imperfect private information. Let $T,Y\in\{+,-\}$ be conditionally independent given challenger quality, with

$$
\Pr(T=+\mid H)=\Pr(T=-\mid L)=a,\qquad
\Pr(Y=+\mid H)=\Pr(Y=-\mid L)=d,
\qquad a,d\in(1/2,1).
\tag{22}
$$

The trader observes $T$ but not $Y$. The buyer observes $Y$ and the target price before preparation. The buyer's signal may be more accurate: $d>a$ is allowed. Diligence still reveals the acquisition value before bidding. All remaining independence and timing assumptions are unchanged.

Let $\lambda_X=\Pr(T=+\mid X)$. Public and joint buyer posteriors are

$$
\begin{aligned}
\mu_X&=(1-a)+(2a-1)\lambda_X,\quad
\mu_-=(1-a)+(2a-1)m,\quad \mu_+=(1-a)+(2a-1)M,\\
\phi_+(\mu)&=\frac{d\mu}{d\mu+(1-d)(1-\mu)},\qquad
\phi_-(\mu)=\frac{(1-d)\mu}{(1-d)\mu+d(1-\mu)}.
\end{aligned}
\tag{23}
$$

Write $w_H=t_H-t_0$ and $w_L=t_L-t_0$. The buyer's private signal changes entry conditional on fundamental quality. With $I_y=\mathbf1\{B_r(\phi_y(\mu))\ge c_H\}$,

$$
\begin{aligned}
e_H&=\rho+(1-\rho)[dI_++(1-d)I_-],\\
e_L&=\rho+(1-\rho)[(1-d)I_++dI_-],\\
D&=e_Hw_H-e_Lw_L,\qquad
\rho\Delta_T\le D\le\Delta_T+(1-\rho)(2d-1)w_H.
\end{aligned}
\tag{24}
$$

We cannot replace these conditional probabilities by a common entry rate. Competitive pricing instead gives

$$
P=t_0+e_L(P)w_L+\mu_XD(P),\qquad
\mu_X=\frac{P-t_0-e_L(P)w_L}{D(P)}.
\tag{25}
$$

The price reveals the public posterior; the buyer combines it with its private information. The favorable and unfavorable trader-signal residuals become

$$
A_+=(2a-1)(1-\lambda_X)D,
\qquad A_-=(2a-1)\lambda_XD.
\tag{26}
$$

**Theorem R2 (analytical).** *In the complementary-signal economy, choose $0<p<\ell<r_0<r_1<h$ and suppose*

$$
\begin{gathered}
c_L<B_{r_1}(\phi_-(\mu_-)),\qquad
B_{r_0}(d)<c_H<B_{r_1}(\phi_+(\mu_+)),\\
(2a-1)\{\Delta_T(r_0)+(1-\rho)(2d-1)w_H(r_0)\}<k\\
<\left(1-\frac1b\right)m(2a-1)\rho\Delta_T(r_1).
\end{gathered}
\tag{27}
$$

*The weak economy has unique zero informed orders and entry $\rho$. The strong economy has unique orders $q(T=+)=1$ and $q(T=-)=-1$, and entry strictly exceeds $\rho$. The conclusions permit arbitrary mixed signal-contingent orders and every continuous unilateral deviation.*

The proof controls public beliefs before imposing any order profile, proves the price inversion with state-dependent entry, and applies global trading bounds to (26). In the weak economy, even the buyer's favorable private signal is insufficient for expensive preparation. In the strong economy, that private signal combined with a favorable price makes preparation worthwhile. Appendix [A.6](#pa-signals) states every step.

Our example uses buyer accuracy 75\% and trader accuracy 70\%. Entry rises from 0.850000 to 0.879438. The mechanism uses complementary information, not an investor whose information uniformly dominates that of the buyer.

### 8.4 What payment property supports discovery? {#lemma-bargaining}

To isolate the role of payment design, we consider a separate verifiable-value bargaining institution. We set the reserve to zero. After diligence, values are publicly verifiable and the highest-value buyer acquires the target. A sale to the next-best buyer at its value is an enforceable fallback, with zero-surplus acceptance prescribed. The seller receives share $\eta$ of the winning buyer's surplus above that fallback in Nash bargaining. Without a challenger, its fallback is zero and it receives $\eta R$.

**Lemma 3 (analytical).** *Let $R$ have any distribution supported on $[0,R_{\max}]$, where $0<\ell<R_{\max}<h$. For $0\le\eta<1$, this institution generates*

$$
\begin{aligned}
T_\eta(R,\theta)&=(1-\eta)\min\{R,\theta\}+\eta\max\{R,\theta\},\\
G_{\theta,\eta}&=(1-\eta)\mathbb E[(\theta-R)_+],\\
\Delta_\eta&=\eta(h-\ell)+(1-2\eta)\mathbb E[(R-\ell)_+].
\end{aligned}
\tag{28}
$$

*A first-order stochastic strengthening of the incumbent weakly reduces challenger profits. It weakly increases the target's information spread for $\eta<1/2$, leaves that spread unchanged at $\eta=1/2$, and weakly decreases it for $\eta>1/2$. Strictness follows from a positive integral change in the corresponding payoff function.*

Runner-up discipline, rather than the auction label alone, drives the original opposition. When the seller already captures much of the winner's own value, stronger competition need not make the target claim more sensitive to challenger quality. This result characterizes the acquisition stage of a specified alternative institution; solving its complete trading and entry game is part of the sale-design program. The case split is in Appendix [A.7](#pa-bargaining).

> **Figure 4 placeholder — Bargaining and the division of information-sensitive returns.** File: `figures/bargaining_weight.pdf`. Panel (a): $\Delta_\eta$ against $\eta$ at the weak and strong incumbent distributions. Panel (b): $G_{H,\eta}$ and $G_{L,\eta}$ at those distributions. Mark the boundary $\eta=1/2$; distinguish acquisition-stage comparisons from equilibrium entry predictions. Data specification: Online Appendix [C.7](online_appendix.md#oa-c-bargaining).

## 9. The real value of discovery {#sec-welfare}

### 9.1 Access to prices and acquisition surplus {#prop-welfare}

**Proposition 2 (analytical).** *Hold $r=r_1$ and all other primitives fixed under Theorem 1. Compare the feedback equilibrium with the equilibrium in which the challenger cannot observe the target price, reoptimizing trading and pricing in both. Access to prices strictly increases expected target proceeds and acquisition surplus net of preparation costs. The comparison also holds under Corollaries 1 and 2.*

The no-feedback buyer enters only at low cost. The same global trading bound supports full orders in both economies, so the financial information experiment and real trading costs are matched. What changes is the buyer's access to that experiment.

Without entry the incremental ownership value is $W_0(R)=R\mathbf1\{R\ge p\}$. With a challenger of value $\theta>p$ it is $W_\theta(R)=\max\{R,\theta\}$. The key identity is

$$
W_\theta(R)-W_0(R)
=(\theta-\max\{p,R\})_++p\mathbf1\{R<p\}.
\tag{29}
$$

Thus an additional preparation decision at posterior $\mu$ and cost $C$ produces conditional expected net surplus $B_r(\mu)-C+p^2/r$. Whenever the buyer chooses that additional entry, its first term is nonnegative and the second is positive. Low-cost entry is unchanged. For cost atoms,

$$
\begin{aligned}
\Delta\mathcal W&=(1-\rho)\mathbb E\left[
\left(B_r(\mu_X)-c_H+\frac{p^2}{r}\right)\mathbf1\{\mu_X\ge\tau\}\right]>0,\\
\Delta\mathcal R_T&=\frac{1-\rho}{2}
\left[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\right]>0.
\end{aligned}
\tag{30}
$$

Payments between bidders and target owners are transfers in this surplus calculation. Appendix [A.8](#pa-welfare) completes the comparison and integrates over atomless costs. The result concerns access to prices at fixed incumbent strength, not a welfare ordering over all changes in competition or sale rules.

### 9.2 Separating information from price levels

At strong incumbent strength, mean target proceeds are 0.872392 with price feedback and 0.614583 when the buyer cannot observe the price. We attach a deterministic external dividend of 0.257809 to the traded claim in the latter economy. This matches the mean financial payoff and price while leaving every trading residual and entry decision unchanged. The dividend is a level-matching diagnostic, not a sale term available to the seller or a resource gain in the welfare calculation.

## 10. Numerical illustration {#sec-numerics}

We quantify the mechanism using a benchmark, a moderate-value economy, and separate extensions. Each exercise begins with its own primitive vector and resolves the relevant equilibrium; the different extensions are not treated as a single jointly solved economy. The full input ledger, acceptance checks, and quantity definitions are in Online Appendix [C](online_appendix.md#oa-c).

In the benchmark, strengthening the incumbent lowers prior gross challenger profit from 4.804167 to 4.291667, while increasing the target's information spread from 0.016667 to 0.666667. Entry nevertheless rises from 0.250000 to 0.522757. The probability of high-quality ownership rises from 0.125000 to 0.324192.

> **Table 1 placeholder — Auction primitives.** File: `tables/auction_primitives.csv`. Columns: weak and strong incumbent economies. Rows: $t_0,t_H,t_L,g_H,g_L,\Delta_T,B_r(1/2)$. Panel labels: none. The caption states the primitive specification and units. Feed: Online Appendix [C.1](online_appendix.md#oa-c-baseline).

The frozen-information control imposes the same informative order profile at both strengths while allowing the buyer to reoptimize. Its entry decreases from 0.562178 to 0.522757. Removing access to prices yields entry 0.250000 and 0.250000. These controls distinguish the direct deterrence effect from the endogenous supply and use of price information. The frozen informative profile is not an equilibrium in the weak economy.

> **Table 2 placeholder — Equilibrium, information controls, and ownership.** File: `tables/equilibrium_controls.csv`. Panel (a): full equilibrium at weak, strong, and collapse strengths; $q_H,q_L,\mathsf E,\mathsf O_H,\mathcal R_T$ and analytical condition margins. Panel (b): frozen informative profile, price-hidden equilibrium, and matched-dividend control. Panel (c): fixed-strength feedback gains in target proceeds and net acquisition surplus. Feed: Online Appendix [C.1](online_appendix.md#oa-c-baseline).

Under logistic noise, strong-economy entry is 0.301509, compared with 0.522757 under Laplace noise. The order-flow threshold is 5.424598398, and its distance in noise standard deviations is 1.495369. Both experiments have the same posterior bounds at the same scale parameter, but they place different mass near those bounds. We therefore compare upper-tail probabilities directly rather than treating scale or variance as an information ordering.

> **Figure 3 placeholder — The upper tail of price information.** File: `figures/posterior_tail_entry.pdf`. Panel (a): $\Pr(\mu_X\ge\tau)$ against the threshold distance $M-\tau$ under full orders, separately for Laplace and logistic noise. Panel (b): the implied total entry $\rho+(1-\rho)\Pr(\mu_X\ge\tau)$ and conditional favorable-flow probabilities. Keep $b$ fixed across the laws; do not label the comparison a liquidity experiment. These are fixed-profile information diagnostics unless the accompanying equilibrium checks validate the corresponding changed cost. Include the endpoint convention explicitly. Feed: Online Appendix [C.5](online_appendix.md#oa-c-noise).

Atomless preparation costs yield strong-economy entry 0.522715 with Laplace noise and 0.301374 with logistic noise. The moderate-value and complementary-signal cases retain positive margins in their respective analytical conditions.

> **Table 3 placeholder — Extensions and information complementarities.** File: `tables/extensions.csv`. Panel (a): Laplace/logistic noise crossed with atomic/atomless preparation costs. Panel (b): moderate acquisition values and Theorem 1 condition margins. Panel (c): complementary-signal economies, accuracies $a,d$, public and joint posterior bounds, Theorem R2 margins, entry, and high-quality ownership. Feeds: Online Appendix [C.1](online_appendix.md#oa-c-baseline), [C.3](online_appendix.md#oa-c-signals), and [C.4](online_appendix.md#oa-c-moderate).

## 11. Sale design as information policy {#sec-design}

### 11.1 The seller's continuation problem {#open-design}

**Research question A (open).** *Which sale rules maximize target proceeds when they change the information revealed before bidder participation? We seek a characterization of seller-optimal discovery, its dependence on incumbent strength, and the conditions under which it reverses or reinforces entry deterrence.*

We begin with a reserve chosen publicly before trading. For every reserve $p$, let $\mathcal E(p,r)$ be the set of trading, pricing, and entry continuations. If $\sigma\in\mathcal E(p,r)$, write $e_H(p,r;\sigma),e_L(p,r;\sigma)$ for state-specific entry. Seller revenue is

$$
\mathcal R_T(p,r;\sigma)
=t_0(p,r)+\frac12\sum_{\theta\in\{H,L\}}e_\theta(p,r;\sigma)
[t_\theta(p,r)-t_0(p,r)].
\tag{31}
$$

A seller equilibrium specifies a continuation after every feasible reserve, not only after its chosen reserve. Given such a selection $\sigma^*(p)\in\mathcal E(p,r)$, the reserve must satisfy

$$
p^*\in\arg\max_{p\in[0,h]}\mathcal R_T(p,r;\sigma^*(p)).
\tag{32}
$$

Existence, attainment, and continuation selection are part of the result to establish. Optimistic and pessimistic revenue envelopes describe the retained correspondence; neither envelope is automatically an equilibrium objective. The strongest comparative-static target is an entry reversal under seller-optimal terms. A characterization of when an optimal seller instead eliminates the reversal would answer the same design question.

### 11.2 Payoffs over the complete reserve domain

The reliable starting point is the realized sale rule. For any realized challenger value $v$,

$$
\begin{aligned}
t_0(p,r)&=\mathbb E[p\mathbf1\{R\ge p\}],\\
t_v(p,r)&=
\begin{cases}
\mathbb E[\max\{p,\min(R,v)\}],&v\ge p,\\
t_0(p,r),&v<p,
\end{cases}\\
g_v(p,r)&=\mathbb E[(v-\max\{p,R\})_+].
\end{aligned}
\tag{33}
$$

For $p<\ell$, equation (4) applies. For $\ell<p<r$, $t_L=t_0$, $g_L=0$, $t_H=r/2+p^2/(2r)$, and $g_H=h-t_H$. For $r\le p<h$, $t_0=t_L=g_L=0$, $t_H=p$, and $g_H=h-p$. Equality at an acquisition-value atom is evaluated using the stated admissibility convention. A reserve above the highest possible value prevents a sale.

These regimes change the claim traded by investors. Excluding a low-value buyer can increase the target's high–low payoff spread, making information valuable even against a weak incumbent. With atomless acquisition values, we integrate (33) over the conditional value distribution rather than extending a formula through an exclusion boundary.

### 11.3 The local extraction–discovery decomposition

On a differentiable continuation branch with atomless preparation costs and $0<p<\ell$, let $\mathsf E=(e_H+e_L)/2$. Differentiating seller revenue gives

$$
\frac{d\mathcal R_T}{dp}
=(1-\mathsf E)\left(1-\frac{2p}{r}\right)+\mathsf E\frac p r
+\frac12\sum_\theta\frac{de_\theta}{dp}(t_\theta-t_0).
\tag{34}
$$

If the cost CDF is $H_C$ with density $h_C$, and $\mu_\theta(z;p)$ is the posterior reached by fundamental state $\theta$ at noise realization $z$, then

$$
\frac{de_\theta}{dp}
=\int f(z)h_C(B_{p,r}(\mu_\theta))
\left[-\frac p r+(g_H-g_L)\frac{d\mu_\theta(z;p)}{dp}\right]dz.
\tag{35}
$$

The first term inside the bracket is direct rent extraction. The second is the change in information generated by equilibrium trading. It vanishes locally on a fixed full-order branch, but not generally when orders adjust. Equations (34)–(35) are local decompositions, not global sign restrictions. Appendix [A.10](#pa-design) gives the differentiability conditions and derivation.

### 11.4 A reserve diagnostic with atomless acquisition values {#diagnostic-reserve}

**Diagnostic 1 (numerical diagnostic).** *Let challenger quality indicate a low or high value class, with equally likely classes. Conditional on class, acquisition value is uniform on $[\ell-\varepsilon_V,\ell+\varepsilon_V]$ or $[h-\varepsilon_V,h+\varepsilon_V]$. The investor observes the class; preparation reveals the exact value. At the specifications in Online Appendix C.6, the tested reserve increase raises seller proceeds at both strengths and produces informative trading in both economies. The stated trading outcomes satisfy the corresponding analytical global bounds.*

The value half-width is 0.05. Raising the reserve from 0.5 to 1.1 raises weak-economy revenue from 0.392665 to 0.432173, and strong-economy revenue from 0.872367 to 1.014500. Entry under the higher reserve is 0.540309 and 0.511638, respectively. This profitable alternative identifies a substantive seller-design margin with atomless acquisition values. Its optimization is the next result, not a property inferred from this comparison.

> **Table 4 placeholder — Sale terms and discovery.** File: `tables/reserve_comparisons.csv`. Panel (a): binary values, original and alternative reserves, entry and target proceeds at each strength. Panel (b): atomless values with class information, the same outcomes and the applicable global trading margins. Panel (c): exploratory reserve sweep, retained revenue/entry ranges, number of distinct continuations found, and unresolved nodes. Do not label the revenue envelope an optimum or treat a missing continuation as an empty equilibrium set. Feed: Online Appendix [C.6](online_appendix.md#oa-c-reserve).

## 12. Research program and empirical design {#sec-program}

We pursue the seller-design problem first, retaining the complete continuation problem at each reserve and making challenger values continuous. The objective is an institutional result about how a seller obtains informative participation. The comparison between a fixed institution and an optimized one determines whether the seller uses, strengthens, or substitutes for the incumbent-induced information effect.

Next we characterize the intermediate equilibrium correspondence. The certified asymmetric points provide exact anchors, not a complete branch. Continuation must allow changing buy–sell asymmetry and mixed orders. We seek conditions for branch existence, local continuation, and multiplicity, followed by a selection argument where one is economically justified.

The next institutional result concerns commitment. **Research question B (open).** *When does fixing sale terms before trading improve the seller's ex ante proceeds relative to revising them after observing the price but before preparation?* Anticipated repricing can change the return to revealing information and the return to becoming an informed buyer. We will solve that timing rather than impose a price-indexed penalty with the desired sign.

We then solve an alternative acquisition institution in full. The bargaining lemma identifies the payment property to study. In a first-price alternative, bids and expected payments depend on the incumbent's posterior about a challenger selected through price-dependent entry; those posteriors belong in the auction continuation. Endogenous investor research likewise requires solving the uninformed trader's incentives, including potential manipulation through real decisions [@GoldsteinGuembel2008]. These are separate games, not substitutions into unchanged payoff formulas.

The empirical component begins with an institutional pilot. We will select publicly visible, still-open sale opportunities involving listed targets and reconstruct the timing of initial approaches, public visibility, contacts, diligence, substantive proposals, revisions, and final selection. At each event we record what was publicly known at that time, separating later retrospective disclosure from contemporaneous availability. Online Appendix [D](online_appendix.md#oa-d) defines the selection rule, coding fields, source hierarchy, and adjudication protocol. The pilot is a design scaffold: it does not report a selected sample, measured effect, or identified causal instrument.

The measurement priorities follow directly from the theory. Entry is a decision to investigate or submit a substantive bid, not simply a count of public offers. Incumbent strength must be measured using information preceding the challenger's decision; a final winning bid is not an exogenous initial threat. Financial information must also precede entry. A relation between returns and subsequent bidders can reflect anticipation of entry as well as learning from prices. The first empirical task is therefore to establish the modeled decision interval and its information sets. A targeted causal or structural exercise follows the final institutional theorem.

## 13. Conclusion {#sec-conclusion}

Competition changes both acquisition profits and the financial return to revealing acquisition information. We show that the second effect can make a stronger incumbent attract another buyer, even though it reduces that buyer's profit at every fixed belief. The result survives complementary private information and smooth distributions. The intermediate correspondence shows why informative markets need not behave like a fixed information experiment, while the bargaining comparison identifies the relevant division of acquisition value.

A company is not sold to a fixed list of fully informed buyers. Its sale rules and stock market help determine who becomes an informed, willing buyer. **How should corporate-control institutions be designed once their effect on discovery is taken seriously?** That is the seller-design question our equilibrium results make concrete.

## References {#references}

::: {#refs}
:::

## Paper appendix {#paper-appendix}

### A.1. Acquisition payoffs and Proposition 1 {#pa-payoffs}

1. **Determine payments before taking expectations.** Without entry, payment is $p\mathbf1\{R\ge p\}$. With high quality, the challenger wins and pays $\max\{p,R\}$. With low quality, target proceeds are $\max\{p,\min(R,\ell)\}$ and the challenger obtains $(\ell-\max\{p,R\})_+$. Truthful bidding is weakly dominant conditional on every competing bid, so these payoffs do not depend on a conjectured shading strategy.
2. **Integrate the uniform realization.** We obtain

$$
\begin{aligned}
t_H&=\frac1r\left[\int_0^p p\,du+\int_p^r u\,du\right],\\
t_L&=\frac1r\left[\int_0^p p\,du+\int_p^\ell u\,du+\int_\ell^r\ell\,du\right],\\
g_L&=\frac1r\left[\int_0^p(\ell-p)\,du+\int_p^\ell(\ell-u)\,du\right].
\end{aligned}
\tag{A.1}
$$

   Evaluating gives (4), and differentiating gives (5).
3. **Establish the distribution-free opposition.** If $R\le\ell$, high and low target payments coincide. If $R>\ell$, their difference is $R-\ell$. Hence the difference is $(R-\ell)_+$. Tonelli's theorem applied to nonnegative indicators gives both integrals in (6). A stronger distribution has a smaller CDF, increasing the survival integral and decreasing the profit integral. Positive integral differences give strictness. A fixed-posterior weighted average preserves the profit ordering. Online Appendix [A.2](online_appendix.md#oa-a-payoffs) provides the measure formulation.

### A.2. Theorem 1: inference and global equilibrium verification {#pa-entry}

1. **Bound beliefs under all mixed orders.** Positivity of $f$ makes every conditional order-flow density positive. Integrating the pairwise inequality (8) gives $m\le\mu_X\le M$. Conditional expectation gives the same bound for beliefs based on price. Both $g_H$ and $g_L$ decrease with $r$, so (A1) implies $c_L<B_r(m)$ in both economies.
2. **Recover the buyer's actual information.** The low-cost type enters at every feasible price, so $e(P)\ge\rho$. Conditional pricing gives (11), whose positive denominator makes $\mu_X$ measurable with respect to $P$. Therefore $\Pr(H\mid P)=\mu_X$ almost surely. The conditional-payoff subtraction yields (10). This uses independence of $R,C$ from trading, not an assumption that the buyer sees order flow.
3. **Eliminate every nonzero weak-economy order.** A correctly signed order with magnitude $s>0$ yields at most $s[\Delta_T(r_0)-k]<0$. A wrong-signed order has negative gross payoff and also pays its cost. Thus zero is the only best response against every candidate equilibrium, including mixed ones. Under zero orders, $\mu_X=1/2$, and (A1)–(A2) give entry $\rho$. Constant pricing constructs that equilibrium.
4. **Control the entire strong-economy order interval.** For a bounded residual $A$, the translation formula

$$
F(s_2)-F(s_1)
=\int_{s_1}^{s_2}\int \partial_u f(x\mp u)A(x)\,dx\,du
\tag{A.2}
$$

   follows by the fundamental theorem for the absolutely continuous density and Fubini: the absolute double integral is bounded by $\|A\|_\infty|s_2-s_1|\|f'\|_1$. Thus $F$ is absolutely continuous, with $|F'|\le F/b$ almost everywhere. Equation (10) gives $F\ge\rho m\Delta_T$. Differentiating $U=sF-ks$ and applying (A3) yields (13). Integrating the positive lower derivative bound shows that the full correctly signed order strictly dominates every smaller magnitude. Wrong signs are dominated by zero. Hence every equilibrium has full correctly signed orders; mixing cannot introduce another optimal action.
5. **Construct and verify the informative equilibrium.** Full orders give

$$
\mu_X(x)=\left[1+\exp\left\{-\frac{|x+1|-|x-1|}{b}\right\}\right]^{-1}.
\tag{A.3}
$$

   Define entry and price by (9). The strict monotonicity of $P_r(\mu)$ gives a measurable inverse on its image, including across its upward jump. The buyer therefore recovers the required posterior from price, optimizes preparation, and subsequently bids truthfully. The preceding global bounds verify investor optimality and market-maker pricing, proving existence and the stated uniqueness.
6. **Compute entry, ownership, and the information comparison.** Since $B_r$ increases with $\mu$ and decreases with $r$, (A2) gives $1/2<\tau<M$. In the central likelihood region, solving $\mu_X=\tau$ gives $x^*$ in (14). The Laplace survival function at $x^*-1$ and $x^*+1$ gives $\alpha_H,\alpha_L$ and the entry and ownership formulas. The favorable event has positive probability. Ignoring the strong-economy price reproduces the uninformative experiment; no state-independent transformation of a constant experiment can reproduce its nonconstant state-dependent law. The strong experiment therefore strictly Blackwell dominates the weak one. Strict primitive margins establish an open region. Online Appendix [A.1–A.4](online_appendix.md#oa-a-foundations) supplies conditional-probability versions, null-set invariance under deviations, and full convolution regularity.

### A.3. Fixed information, thresholds, and Corollary 3 {#pa-thresholds}

1. **Fixed experiment.** Couple the economies using the same realization of the signal and cost. Since $B_{r_1}(\mu)\le B_{r_0}(\mu)$, the entry indicator is pointwise weakly smaller at the stronger rival. A strict decrease in expected entry occurs exactly when the set $\{B_{r_1}(\mu)<C\le B_{r_0}(\mu)\}$ has positive probability. This proves Proposition R1 under the stated entry-at-indifference convention.
2. **Exact pooling existence.** In the domain of Proposition 3, pooling implies entry $\rho$ and constant price. A correctly signed deviating order earns

$$
s\left(\frac{\rho\Delta_T(r)}2-k\right).
\tag{A.4}
$$

   Thus zero is optimal exactly when its coefficient is nonpositive. Solving $\Delta_T(r)=d$ on $r>\ell$ gives $\mathfrak r(d)$. This proves the exact $r_N$ boundary. In contrast, $\Delta_T<k$ eliminates nonzero orders against every candidate schedule and establishes the smaller sufficient uniqueness region.
3. **Full orders and entry feasibility.** The derivative bound (13) is uniform across candidate equilibria whenever $r>r_U$ and the low-cost floor holds. For expensive entry, the largest feasible belief is $M$. Its profitability is

$$
B_r(M)=Mh-\frac{Mr}{2}+\frac{(1-M)\ell^2-p^2}{2r}.
\tag{A.5}
$$

   It is strictly decreasing on the auction-support domain. Multiplying $B_r(M)=c_H$ by $2r$ gives a quadratic; selecting a root within that domain gives (16). When the discriminant or domain requirement fails, the feasibility comparison is made directly rather than assigning an artificial crossing. The formula in (16) selects the larger algebraic root; any other root cannot provide another crossing in the specified domain because of strict monotonicity.
4. **Endpoint behavior.** Under full Laplace orders, $\mu_X=M$ for $x\ge1$, an event with positive probability. Our tie rule admits expensive entry at $r_C$ on that event. As $r$ approaches $r_C$ from below,

$$
\mathsf E(r)\longrightarrow\rho+\frac{1-\rho}{4}(1+e^{-2/b}).
\tag{A.6}
$$

   For strengths strictly above $r_C$, expensive entry is impossible. With logistic noise the posterior reaches $M$ only at an infinite flow limit, so expensive entry instead converges to zero continuously. These statements concern their respective information experiments.
5. **The finite nonmonotonicity corollary.** Apply Theorem 1 at $r_0,r_1$. At $r_2$, the low-cost floor and full-order derivative bound establish unique full orders, while $B_{r_2}(M)<c_H$ excludes every expensive entrant. Hence entry returns to $\rho$. This proves (17) without assigning a unique branch at intermediate strengths. Full derivations are in Online Appendix [A.5](online_appendix.md#oa-a-thresholds).

### A.4. The computer-assisted asymmetric result {#pa-certificate}

1. **Candidate beliefs and entry.** Fix $(q_H,q_L)=(1,-v)$, $0<v<1$. Bayes' rule gives $\mu_v(x)=\operatorname{logistic}((|x+v|-|x-1|)/b)$. The posterior ranges from $m_v=(1+e^{(1+v)/b})^{-1}$ to $M_v=1-m_v$. In the certified region $1/2<\tau<M_v$, and

$$
x^*(r,v)=\frac{b\operatorname{logit}(\tau)+1-v}{2},\qquad
\mathsf E(r,v)=\rho+\frac{1-\rho}{2}
\left[1-\frac12e^{(x^*-1)/b}+\frac12e^{-(x^*+v)/b}\right].
\tag{A.7}
$$

2. **A globally optimal interior short.** The residual $A_L=e(\mu_v)\Delta_T\mu_v$ is bounded, nonconstant, and nondecreasing. Its finite positive Stieltjes measure gives

$$
F_L'(s)=-\int f(x+s)\,dA_L(x)<0,
\qquad |F_L''(s)|\le-\frac1bF_L'(s).
\tag{A.8}
$$

   Therefore $U_L''(s)\le(2-s/b)F_L'(s)<0$ for $s\in[0,1]$ when $b>1/2$. The measure includes the entry jump; no derivative of that jump is omitted. A root of the unilateral marginal-profit equation is thus the unique global short magnitude against its candidate schedule.
3. **An exact root, not a small residual.** Let $\Psi(r,v)=U_L'(v;1,-v)$, with the unilateral derivative taken holding the candidate schedule fixed. Recomputing the schedule as the candidate parameter $v$ varies gives a continuous $\Psi$ on each certified bracket. Outward interval evaluation proves positive $\Psi$ at the left endpoint and negative $\Psi$ at the right endpoint. The intermediate value theorem gives an exact root inside. Throughout each bracket, the entry threshold stays strictly between $-v$ and $1$. The endpoints $v_{j,-},v_{j,+}$ are those of the corresponding bracket in (18). The enclosures completing the sign tests are

$$
\begin{aligned}
\Psi(r_{\mathrm a},v_{\mathrm a,-})&\ge0.000000000114>0,&
\Psi(r_{\mathrm a},v_{\mathrm a,+})&\le-0.000000000096<0,\\
\Psi(r_{\mathrm b},v_{\mathrm b,-})&\ge0.000000000123>0,&
\Psi(r_{\mathrm b},v_{\mathrm b,+})&\le-0.000000000121<0,\\
\Psi(r_{\mathrm c},v_{\mathrm c,-})&\ge0.000000000172>0,&
\Psi(r_{\mathrm c},v_{\mathrm c,+})&\le-0.000000000242<0.
\end{aligned}
\tag{A.9}
$$

4. **Exclude every smaller purchase.** For any bounded residual $A_H\in[0,\Delta_T]$, the Laplace kernel satisfies $f''=(f-\delta_0)/b^2$ in distributions. Consequently

$$
F_H''(s)=\frac{F_H(s)-A_H(s)}{b^2}\quad\text{a.e.},\qquad
|U_H''(s)|\le L_U:=\frac{2\Delta_T}{b}+\frac{\Delta_T}{b^2}.
\tag{A.10}
$$

   On the mesh $s_j=j/n$, interval arithmetic bounds $U_H'(s_j)$ uniformly over the entire root bracket. Every untested magnitude is within $1/(2n)$ of a mesh point, so

$$
\inf_{s\in[0,1]}U_H'(s)
\ge\min_j\underline{U_H'(s_j)}-\frac{L_U}{2n}>0.
\tag{A.11}
$$

   The certified global lower margins at the ordered strengths are 0.0000761777, 0.0027531948, and 0.0054921767. Thus the favorable type chooses its maximum purchase. All wrong-signed trades have negative gross profit and are dominated by zero.
5. **Integrate exactly and conclude.** Split each convolution at $-v,x^*,1$, and the deviation center. On the central region put $c=(1-v)/2$ and $t=e^{(x-c)/b}$, so $\mu_v=t^2/(1+t^2)$. The primitives of $e^{x/b}(1-\mu_v)$, $e^{-x/b}(1-\mu_v)$, $e^{x/b}\mu_v$, and $e^{-x/b}\mu_v$ are respectively

$$
b e^{c/b}\arctan t,\quad
b e^{-c/b}(-t^{-1}-\arctan t),\quad
b e^{c/b}(t-\arctan t),\quad
b e^{-c/b}\arctan t.
\tag{A.12}
$$

   Constant-posterior tails integrate as exponentials. Interval arithmetic applied to these expressions encloses the root tests, (A.11), and the entry probabilities. The pooling margins are positive at the same strengths, and the entry enclosures in (18) are disjoint and ordered. This proves Proposition 4. Online Appendix [B](online_appendix.md#oa-b) specifies the interval arithmetic, parameter brackets, endpoint ordering, and every regularity argument needed for replication.

### A.5. Smooth distributions and moderate acquisition values {#pa-smooth}

1. **Log-density control.** If a positive density is absolutely continuous and $|f'|\le Lf$ almost everywhere with $L<1$, log-density integration gives the pairwise likelihood bound $e^{-2L}\le f(x-q)/f(x-q')\le e^{2L}$. The convolution proof in A.2 yields $U'(s)\ge(1-L)\rho m_L\Delta_T-k$, where $m_L=(1+e^{2L})^{-1}$. Logistic noise has $(\log f)'=-\tanh(z/(2b))/b$ and therefore $L=1/b$.
2. **Attainable informative beliefs.** Under full logistic orders the posterior log odds are

$$
2\log\cosh\left(\frac{x+1}{2b}\right)
-2\log\cosh\left(\frac{x-1}{2b}\right).
\tag{A.13}
$$

   Its derivative is positive and its limits are $-2/b,2/b$. It spans the posterior interval $(m,M)$. Solving for the interior threshold gives (20); the positive density assigns positive probability above it. The uniform no-trade and full-order arguments and the ownership/Blackwell comparisons follow as in Theorem 1. This proves Corollary 1.
3. **Atomless preparation costs.** Under (21), all low-cost realizations participate at all feasible prices, preserving the residual lower bound. At the weak prior all high-cost realizations stay out. At prices sufficiently close to the upper feasible posterior all high-cost realizations enter. That event has positive probability under either noise law. The cost CDF is nondecreasing, so the price construction remains strictly increasing. The global trading bounds are unchanged. This proves Corollary 2.
4. **Nonemptiness with any strict value gap.** At $r=\ell$, $g_H-g_L=h-\ell$ and

$$
B_\ell(M)-B_\ell(1/2)=(M-1/2)(h-\ell)>0.
\tag{A.14}
$$

   Choose $r_1>\ell$ sufficiently close that $B_{r_1}(M)>B_\ell(1/2)$. Next choose $r_0\in(\ell,r_1)$ sufficiently close to $\ell$ that $\Delta_T(r_0)<(1-1/b)\rho m\Delta_T(r_1)$. Choose $k$ strictly between these bounds, $c_H$ strictly between $B_{r_0}(1/2)$ and $B_{r_1}(M)$, and $c_L$ positive and below $B_{r_1}(m)$. These intervals are nonempty. Continuity preserves all strict inequalities in a neighborhood. Online Appendix [A.6](online_appendix.md#oa-a-extensions) supplies full regularity, the logistic inversion, and further prior/cost extensions.

### A.6. Theorem R2: the buyer and trader have distinct private signals {#pa-signals}

1. **Control public and private posteriors.** Marginal trader signals are equally likely. Arbitrary orders mixed conditional on those signals obey the same likelihood-ratio bound as in Lemma 1, so $m\le\lambda_X\le M$. Conditional independence gives $\mu_X=(1-a)+(2a-1)\lambda_X$ and the public interval $[\mu_-,\mu_+]$. The buyer's posterior is $\phi_Y(\mu_P)$ because $Y$ is independent of $X$ conditional on fundamental quality. Its lowest feasible posterior is $\phi_-(\mu_-)$. The first restriction in (27) makes low-cost entry optimal in both economies.
2. **Price state-dependent participation.** Since $\phi_+\ge\phi_-$, optimal high-cost entry satisfies $I_+\ge I_-$. Formula (24) follows by averaging over $Y$ conditional on $H$ or $L$. Thus $e_H\ge e_L\ge\rho$, and

$$
D=e_L\Delta_T+(e_H-e_L)w_H,
\quad 0\le e_H-e_L\le(1-\rho)(2d-1).
\tag{A.15}
$$

   This proves the bounds in (24). Equation (25) then makes the public posterior measurable with respect to price. For construction, entry is nondecreasing in the public posterior for each private signal. Between entry changes the price slope is $D>0$; at an entry change the price increases because the added conditional target payoffs $w_H,w_L$ are positive. The buyer can therefore recover public information and combine it with $Y$.
3. **Derive residuals for the trader's information.** Conditional on $T=+$, the probability of $H$ is $a$ even after observing any flow generated by a signal-contingent unilateral order; for $T=-$ it is $1-a$. This follows because order randomization and noise add no information about $\theta$ conditional on $T$. Subtracting the competitive price from the appropriate conditional target payoff gives (26), with

$$
m(2a-1)\rho\Delta_T\le A_+,A_-
\le(2a-1)[\Delta_T+(1-\rho)(2d-1)w_H].
\tag{A.16}
$$

4. **Establish necessity and existence in both economies.** The lower cost inequality in (27) makes the upper residual at $r_0$ smaller than $k$, excluding every nonzero correctly signed order; wrong signs are dominated. Public beliefs are then the prior, and the buyer's highest private posterior is $d$. Since $B_{r_0}(d)<c_H$, entry is $\rho$ and constant pricing constructs the equilibrium. At $r_1$, the convolution argument gives

$$
U'(s)\ge(1-1/b)m(2a-1)\rho\Delta_T(r_1)-k>0.
\tag{A.17}
$$

   Full correctly signed orders are necessary against every candidate schedule. Bayes' rule, optimal private-signal entry, and the strictly increasing price construction establish existence. Finally, $c_H<B_{r_1}(\phi_+(\mu_+))$ makes expensive entry worthwhile for a favorable private signal and a positive-probability set of sufficiently favorable prices. This proves the strict entry comparison. Online Appendix [A.7](online_appendix.md#oa-a-signals) gives the joint conditional laws, measurable construction, and complete probability formulas.

### A.7. Bargaining and Lemma 3 {#pa-bargaining}

1. **Derive the price from a feasible fallback.** Let $V$ be the winner's value and $z$ the next-best buyer's value. The seller's disagreement payoff is $z$ because the fallback sale is enforceable. The winner's disagreement payoff is zero. The Nash solution maximizes $(P-z)^\eta(V-P)^{1-\eta}$ on $[z,V]$. For interior weights its first-order condition gives $P=z+\eta(V-z)$; continuity covers the zero-weight endpoint.
2. **Allocate the challenger surplus.** A challenger wins only if $\theta\ge R$ and then keeps $(1-\eta)(\theta-R)$. Hence $G_{\theta,\eta}$ in (28). Without entry the same institution has $z=0$, giving target payment $\eta R$.
3. **Subtract the target payments state by state.** If $R\le\ell$, the high–low difference is $\eta(h-\ell)$. If $R>\ell$, it is $\eta(h-\ell)+(1-2\eta)(R-\ell)$. Taking expectations proves (28). FOSD applies to the increasing function $(R-\ell)_+$ and the decreasing function $(\theta-R)_+$. The coefficient $1-2\eta$ determines the information-spread ordering. These are payment-stage conclusions for the specified verifiable-value institution. Online Appendix [A.8](online_appendix.md#oa-a-bargaining) supplies the full bargaining construction and endpoint treatment.

### A.8. Proposition 2: a matched surplus comparison {#pa-welfare}

1. **Resolve the price-hidden game.** The buyer's posterior stays at the prior, so (A1)–(A2) give entry $\rho$. The strong global bound still applies with constant $e=\rho$, establishing full orders. The same investor order magnitudes and noise distribution therefore occur with and without feedback.
2. **Compute incremental allocation value pointwise.** If $R<p$, entry replaces no sale by a sale to $\theta$, and the right-hand side of (29) equals $\theta-p+p=\theta$. If $R\ge p$, it equals $(\theta-R)_+$, the improvement over incumbent ownership. This proves (29). Integrating over $R$ gives $g_\theta+p\Pr(R<p)=g_\theta+p^2/r$.
3. **Condition on the information used to enter.** Every additional entrant satisfies $B_r(\mu)-C\ge0$. Its conditional net contribution is therefore at least $p^2/r>0$. The additional-entry event has positive probability; low-cost participation is unchanged. Averaging gives the first expression in (30), or its integral over high costs for Corollary 2. Noise-trader transfers and acquisition payments do not alter total allocation surplus; identical real trading costs cancel.
4. **Compare target proceeds and match price levels.** Since $t_H,t_L>t_0$, additional entry raises target proceeds by the second expression in (30). Adding a deterministic external dividend to the price-hidden traded claim increases its rational price by the same amount and leaves $V_T-P$ unchanged. It therefore preserves trading and entry. Online Appendix [A.9](online_appendix.md#oa-a-welfare) states the probability coupling and the cost-distribution integral explicitly.

### A.9. Numerical primitive vectors {#pa-parameters}

The benchmark parameter vector is

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.25,1,6,2,0.02),\\
(r_0,r_1,r_2)&=(1.2,3,3.6).
\end{aligned}
\tag{A.18}
$$

The moderate-value vector is

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(2,1,0.5,0.25,0.3,0.89,2,0.002),\\
(r_0,r_1)&=(1.05,1.5).
\end{aligned}
\tag{A.19}
$$

For complementary signals we use

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.85,1,7.14,2,0.015),\\
(r_0,r_1,a,d)
&=(1.1,2.3,0.70,0.75).
\end{aligned}
\tag{A.20}
$$

The atomless-cost half-width is $\varepsilon_C=0.1$ and the atomless-value half-width is $\varepsilon_V=0.05$. These are separate experiments. Online Appendix C defines exact input values, derived quantities, formatting, and acceptance criteria for every placeholder.

### A.10. Sale-domain identities and local differentiation {#pa-design}

1. **Condition on reserve admissibility.** When $v<p$, the challenger never meets the reserve, so its presence leaves target proceeds at $t_0$ and its acquisition profit at zero. When $v\ge p$, the target sells to the larger of $R,v$ and receives $\max\{p,\min(R,v)\}$. These cases prove (33), including the stated equality convention. Averaging over $v$ gives conditional class payoffs for atomless values.
2. **Derive seller revenue.** Conditional on challenger quality, entry changes target proceeds by $t_\theta-t_0$. Independence of $R$ from entry justifies (31). Within $0<p<\ell$, $\partial_pt_0=1-2p/r$, $\partial_pt_H=\partial_pt_L=p/r$, and $\partial_pB_{p,r}(\mu)=-p/r$ at a fixed posterior. Applying the product rule to (31) gives (34).
3. **Differentiate entry only on a regular branch.** Assume an atomless cost CDF that is continuously differentiable on the reached profit range, differentiable state-contingent orders and posteriors almost everywhere in the noise realization, and an integrable common bound for the differentiated entry integrand in a neighborhood of the reserve. Dominated differentiation of $e_\theta=\int f(z)H_C(B_{p,r}(\mu_\theta(z;p)))dz$ yields (35). At reserve/value boundaries, nondifferentiable order branches, or atomic cost thresholds, use the level objective rather than this derivative.
4. **Keep the optimization problem separate.** A valid seller optimum must compare continuations after all feasible reserve choices. The payment identities and local decomposition do not select a continuation or prove attainment of that optimum. Online Appendix [A.10](online_appendix.md#oa-a-design) gives the continuous-class formulas and sufficient differentiation conditions; Appendix C.6 specifies the exploratory correspondence calculation that supports the next theorem.
