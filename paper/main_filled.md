---
title: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders"
author: "Austin Li"
date: ""
bibliography: references.bib
link-citations: true
abstract: |
  A stronger incumbent bidder can attract a challenger by making the target's stock price more informative. I study a takeover auction in which a prospective buyer observes the price before committing to acquisition preparation. Stronger competition lowers the buyer's acquisition profit at every fixed belief but increases the sensitivity of target shareholders' proceeds to its value. This raises the incentive to trade on information about the challenger. On an open set of primitives, strengthening the incumbent changes uninformative prices into informative prices, with unique trading and on-path preparation outcomes in each economy. Challenger participation and high-value challenger ownership increase. Holding the price experiment fixed restores deterrence. The reversal also arises when the buyer has a more accurate private signal than the investor. The mechanism connects acquisition payments to the information that brings buyers into a takeover contest.
---

## 1. Introduction {#sec-introduction}

At fixed information, a stronger incumbent reduces a prospective challenger's expected return from entering a takeover contest. The challenger must pay preparation costs before it can submit an executable offer, and a stronger rival lowers what that preparation earns [@Fishman1988; @HirshleiferPng1989]. I study a force in the opposite direction. Competition can make the target's stock more informative about the challenger. When a potential buyer observes that price before committing to acquisition preparation, the information effect can outweigh the loss of acquisition profits. A stronger incumbent then attracts a competing buyer and raises the probability that a high-value challenger acquires the target.

The mechanism runs through two claims on the same acquisition surplus. The challenger holds the acquisition claim, what it keeps if it prepares, bids, and wins. Target shareholders hold the traded claim, what the auction pays them. In a cash second-price auction, a high-value challenger wins and pays the larger of the reserve and the incumbent's bid. A low-value challenger wins only against an incumbent whose value is below its own, and then pays the larger of the reserve and that bid; against a stronger incumbent it loses, and its own bid sets what the incumbent pays. A stronger incumbent therefore raises the payment a high-value challenger must make, which lowers acquisition profit at every belief. The same shift widens the gap in target proceeds between the two challenger types, because a winning incumbent pays the low-value challenger's bid while a high-value challenger must outbid the incumbent. Target shares become more sensitive to information about the challenger at the same time as the challenger's own return to preparation falls. An investor who knows the challenger's value trades on that sensitivity against noise demand. Competitive market makers price order flow and anticipate the preparation that each price will induce, but noise leaves the investor a residual advantage. A larger gap in target proceeds can make that advantage worth the cost of trading.

The relevant information is complementary rather than necessarily superior. A prospective buyer may know its integration capabilities while investors specializing in the target hold different information about customers, technology, or product demand. The stock price can add to the buyer's assessment before it commits resources to an executable acquisition proposal. I first isolate the mechanism with a perfectly informed investor and an initially uninformed challenger, then establish the reversal with distinct imperfect signals, including a buyer signal that is more accurate than the investor's.

The setting is a listed target whose sale opportunity is publicly understood while its stock still trades and while a further bidder can still come in. One buyer is already prepared. Another has not committed to the diligence and transaction work that an executable proposal requires. [Section 1.1](#sec-the-decision-interval) describes that interval. The model's timing follows it. The seller commits to a cash second-price auction with a reserve; the investor trades; market makers set the price; the challenger observes the price and its privately realized preparation cost and decides whether to prepare; prepared bidders bid truthfully. Incumbent strength is the public distribution of the prepared bidder's value, conditional on what is known when the opportunity becomes visible. It is not a realized bid. A stronger incumbent shifts that distribution upward, and no offer is announced before the challenger decides.

The main result compares a weak-incumbent economy with a strong-incumbent economy on a nonempty open set of primitives. In each economy the trading outcome and the on-path preparation outcome are unique. With the weak incumbent, the investor's residual advantage cannot cover trading costs, the price reveals nothing, and only a low-cost challenger prepares. With the strong incumbent, informed trading pays, the investor trades to its limit, and favorable prices bring in a high-cost challenger. Preparation rises even though acquisition profit falls at every fixed belief, and the probability that a high-value challenger owns the target rises with it. Prices are rational throughout. Market makers anticipate the preparation each price induces, so the reversal is not an artifact of mispricing. Uniqueness allows arbitrary mixed orders and every continuous unilateral deviation; a global bound on marginal trading profit controls them, so no candidate order profile has to be assumed. The change in information does the work. If the investor's orders are held fixed at their informative level while the incumbent strengthens, preparation falls, as the fixed-information benchmark predicts.

Further results delimit the mechanism. The reversal survives complementary private signals, logistic noise, atomless preparation costs, and a narrower gap between acquisition values. At intermediate incumbent strengths, informative and uninformative equilibria coexist. I establish three informative equilibria by computer-assisted proof, with preparation strictly ordered upward across them, while the complete intermediate correspondence stays open. At fixed incumbent strength, access to prices raises expected target proceeds and acquisition surplus net of preparation costs. One implication is that participation is not monotone in strength. At a strength high enough that even the most favorable feasible price cannot justify expensive preparation, participation falls back to its floor while trading stays informative.

The seller's choice of terms is the next theorem rather than a result of this paper. Terms shape both what a winning buyer pays and what the stock price can reveal before anyone decides to prepare. A reserve that excludes a low-value challenger, for instance, can support informative trading against an incumbent that would otherwise leave the price uninformative. Each choice of terms induces a continuation that specifies price rules as well as investor orders, and several continuations can share the same orders. I report fixed-reserve comparisons whose trading continuations are established, and an alternative bargaining institution shows that the effect of competition on target-payoff sensitivity depends on the weight the payment rule places on the runner-up's value.

The closest antecedent is @DowGoldsteinGuembel2017, where a firm's investment decision feeds back into the incentive to produce information about its stock. Here the sale rule divides acquisition surplus between a traded claim and a buyer deciding whether to participate, and the two returns to information move in opposite directions as competition changes. That opposition, and the participation reversal it produces, is the increment over generic learning from prices. @EdmansGoldsteinJiang2015 show that corrective real decisions can discourage trading on bad news under rational pricing; I study how rival strength changes the information sensitivity of the claim and, through it, participation. Evidence that prices affect takeover activity [@EdmansGoldsteinJiang2012] runs from prices to control and does not identify a prospective challenger learning its acquisition value. Learning from announcement returns in completion decisions [@Luo2005] occurs after the participation margin studied here. The auction-entry literature makes the bidder pool endogenous [@LevinSmith1994; @GentryStroup2019] and shows how selective entry affects the choice of sale procedure [@RobertsSweeting2013]; I keep the direct deterrence force and add a market that operates before preparation. Auction formats also affect bidders' incentives to acquire information [@Persico2000], but the informed trader here is outside the auction and trades a payoff that differs from the entrant's profit. Recent work studies bidder learning about own values and competitors [@PernoudGleyze2026], post-auction feedback in security-payment design [@LiuBernhardt2022], and bidder-pool choice with correlated values [@CarlinEtAl2026]. In takeovers, @BettonEtAl2014 study negotiations with stock-market feedback and @LinMaYangZhu2025 model payment choice and trading within an initiated deal; I hold cash consideration fixed and study entry. Arbitrageurs' positions can affect tendering [@CornelliLi2002], whereas the investor here has information about a prospective acquirer and no role in tendering. The model excludes toeholds and dispersed-shareholder free riding [@BulowHuangKlemperer1999; @GrossmanHart1980]. It also excludes endogenous investor research, which would add manipulation through the real decision that responds to the price [@GoldsteinGuembel2008].

[Section 2](#sec-model) sets out the model. [Section 3](#sec-payoffs) derives the two returns to information and what the challenger can learn from the price. [Section 4](#sec-results) states the main result, the fixed-experiment control, and the coexisting equilibria. [Section 5](#sec-extensions) covers robustness and complementary private information, [Section 6](#sec-welfare) welfare and sale terms, and [Section 7](#sec-program) empirical implications. [Section 8](#sec-conclusion) concludes. [Appendix A](#paper-appendix) contains supporting results and proofs; the Online Appendix contains the measure-theoretic arguments, the numerical contract, and the reproducibility record.

### 1.1 The decision interval {#sec-the-decision-interval}

The model applies to a listed target whose sale opportunity is publicly understood while its stock still trades and while a further bidder can still come in. A disclosed approach, an announced strategic review, or an open contest can create such an interval. None does so automatically. A wholly confidential process whose existence becomes public only after the buyer set is fixed does not, because no prospective buyer could have watched the price during the period that matters. Whether a given transaction fits is a question about its chronology, and this paper does not settle it for any transaction.

Within the interval, one buyer is already prepared. It may be the approaching party or a bidder that has completed diligence, and its strength is what the public can infer about its acquisition value from the disclosed record. Another buyer has not decided whether to prepare. Preparation is required for an executable proposal. Before a buyer can submit a binding offer it must verify the target's contracts, liabilities, and technology, arrange financing and approvals, and commit evaluation capacity that has other uses. Those costs are sunk once incurred, and they differ across buyers. Prior familiarity, existing capacity, or a small deal relative to the buyer's size make preparation cheap for some buyers and expensive for others. A buyer that declines to prepare cannot bid its current expected value instead; it stays out. The challenger's cost is a participation cost, not the price of an optional report.

The investor's information need not dominate the buyer's. A buyer knows its own integration plans. A specialist investor may know what the target's customers are doing, how its technology compares with alternatives, or where its product demand is heading. These are different facts about the same acquisition match, and a more accurate signal about one need not contain the other. The benchmark suppresses the buyer's initial information and gives the investor perfect information so that the mechanism is easy to see; [Section 5.3](#sec-complementary-private-information) removes both extremes.

Public incumbent strength is a distribution, not a bid. The record can reveal that a strategic acquirer with clear synergies is at the table, or that the prepared party is a financial buyer with a leveraged capital structure, without revealing what either would pay. The model varies that distribution and keeps the incumbent's realized value private until it bids. It does not vary an announced offer, whose choice would raise signaling and negotiation questions outside this paper. Disclosure records support the stage structure. Imprivata's definitive proxy separates an unsolicited approach, outreach to potential buyers, and indications of interest conditional on further diligence [@Imprivata2016], and takeover competition develops before public bidding more generally [@BooneMulherin2007; @GentryStroup2019]. This supports the existence of a costly preparation stage. It is not evidence that a price drew any buyer into that process, which is the question an empirical study would have to answer.

## 2. The model {#sec-model}

### 2.1 Values, preparation, and the sale {#sec-values-preparation-and-the-sale}

The target's known standalone value is normalized to zero. Acquisition values and preparation costs are measured per target share. Adding the same standalone component to every ownership outcome shifts prices and payoffs by a constant without changing incentives.

All strategic agents are risk neutral. The target share is the only traded claim that conveys information about the acquisition match in the benchmark, and neither bidder trades it. The investor has no control rights and cannot acquire the target. The sale mechanism binds all target shares, so shareholder tendering and holdout are outside the modeled continuation. The incumbent's value distribution is public, conditional on the information available when the sale opportunity becomes visible, but its realized value is not disclosed to the challenger before preparation.

Two potential acquirers face the target. The incumbent has already prepared and incurs no further participation cost. Its acquisition value $R$ is uniform on $[0,r]$, conditional on public information when the sale process begins. An increase in $r$ strengthens the incumbent in the sense of first-order stochastic dominance. The incumbent is a bidder, rather than the target's management, and knows its value before bidding.

The challenger has acquisition value $\theta\in\{\ell,h\}$, with equal prior probabilities. The benchmark restricts values and the reserve $p$ to

$$
0<p<\ell<r<h.
\tag{1}\label{eq:paper-1}
$$

The challenger initially does not know its value. After observing the stock price, it privately learns its preparation cost $C$, which equals $c_L$ with probability $\rho$ and $c_H$ otherwise. I assume $0<\rho<1$ and $0\le c_L<c_H$. There is one challenger with one realized cost, not a low-cost buyer and a high-cost buyer at the same time; $\rho$ is the probability that the realized cost is the low one. Paying $C$ reveals $\theta$ and permits bidding; declining leaves the challenger outside the sale. Preparation is required to submit an executable acquisition proposal. The cost represents verification and transaction preparation as well as learning, and a buyer that declines it does not submit an uninformed bid at its current expected value. Incumbent value, challenger value, preparation cost, and noise demand are mutually independent, so the cost carries no information about values.

Before trading, the seller publicly commits to a cash second-price auction with reserve $p$. The highest admissible bidder acquires the target and pays the larger of the reserve and the highest competing bid. There is no sale without an admissible bid. Both bidders use truthful, weakly dominant bids. A bid equal to the reserve is admissible, and a challenger indifferent about preparation enters. Acquisition-value ties have probability zero in the benchmark. Preparation indifference matters at a posterior plateau considered in Section 4.

### 2.2 Trading and timing {#sec-trading-and-timing}

An investor observes $\theta$ and submits an order $q\in[-1,1]$. The bound is a normalized small trading unit, not ownership of the target. The investor has no initial position and pays a linear trading cost $k|q|$, where $k>0$. This cost is a separate friction, such as an execution or position-carrying cost. It is distinct from adverse-selection price impact, which the competitive pricing rule below already generates. Its profit and aggregate order flow are

$$
\begin{gathered}
q\{V_T-P(X)\}-k|q|,\qquad X=q+Z,\\
f(z)=\frac{1}{2b}e^{-|z|/b},\qquad b>1.
\end{gathered}
\tag{2}\label{eq:paper-2}
$$

Here $V_T$ is the terminal payoff of a target share and $Z$ is independent noise demand with a Laplace density. The bounded likelihood ratios of this density limit the information that any order can reveal. [Section 5](#sec-extensions) also considers logistic noise.

Competitive market makers observe aggregate flow and set

$$
P(X)=\mathbb E[V_T\mid X],
\tag{3}\label{eq:paper-3}
$$

anticipating preparation and auction outcomes.

The information sets are as follows. Market makers observe aggregate flow $X$ and nothing else. The challenger observes the price $P$ and its own cost $C$, but not $X$, $\theta$, or the incumbent's realized value; in the extension of [Section 5.3](#sec-complementary-private-information) it also observes a private signal, which the investor does not see. The investor observes $\theta$ and nothing about the incumbent's realized value beyond its public distribution. The incumbent knows its own value. The sequence is: the seller announces the sale rule; the investor learns $\theta$ and trades; market makers set the price from flow; the challenger observes the price and its cost and decides whether to prepare; prepared bidders learn their values and submit truthful bids; ownership and financial payoffs are realized.

### 2.3 Equilibrium {#sec-equilibrium}

An equilibrium specifies conditional order distributions $\sigma_H,\sigma_L$, a measurable price function, Bayesian beliefs conditional on the observed price, optimal preparation, and truthful bidding. The investor can mix and can deviate to any order in $[-1,1]$. Two comparisons recur and must not be confused. A unilateral investor deviation changes the distribution of flow that reaches a fixed candidate price function and preparation schedule; the deviation is evaluated against those fixed schedules. A comparison across economies, for instance across incumbent strengths, re-solves the price function and the preparation schedule in each economy. Proofs and validation checks use the first when testing a candidate equilibrium and the second when comparing outcomes.

Write $t_0$ for expected target proceeds without entry, $t_H,t_L$ for proceeds conditional on entry and quality, and $g_H,g_L$ for the challenger's corresponding gross acquisition profits. The target-payoff spread is $\Delta_T=t_H-t_L$. At a belief $\mu=\Pr(\theta=h)$, the challenger's expected gross profit is $B_r(\mu)=g_L+\mu(g_H-g_L)$.

## 3. Competition and information {#sec-payoffs}

### 3.1 Acquisition profits and target proceeds {#sec-acquisition-profits-and-target-proceeds}

The auction determines both the return to preparation and the claim that informed investors trade. A high-value challenger wins and pays $\max\{p,R\}$. With a low-value challenger, the target receives $\max\{p,\min(R,\ell)\}$. Without entry, the incumbent pays the reserve if its value meets it. Integrating over the uniform incumbent gives

$$
\begin{aligned}
t_0&=p\left(1-\frac p r\right),&
t_H&=\frac r2+\frac{p^2}{2r},\\
t_L&=\ell-\frac{\ell^2-p^2}{2r},&
g_H&=h-\frac r2-\frac{p^2}{2r},\\
g_L&=\frac{\ell^2-p^2}{2r},&
\Delta_T(r)&=\frac{(r-\ell)^2}{2r}.
\end{aligned}
\tag{4}\label{eq:paper-4}
$$

The relevant derivatives are

$$
\begin{aligned}
B_r(\mu)&=g_L+\mu(g_H-g_L),\\
\Delta_T'(r)&=\frac12-\frac{\ell^2}{2r^2}>0,\\
g_H'(r)&=-\frac12+\frac{p^2}{2r^2}<0,
\qquad g_L'(r)=-\frac{\ell^2-p^2}{2r^2}<0.
\end{aligned}
\tag{5}\label{eq:paper-5}
$$

Thus a stronger incumbent lowers acquisition profit at every fixed belief while making target proceeds more sensitive to challenger quality. [Proposition 1](#result-proposition-1) extends this opposition beyond the uniform distribution.

[**Proposition 1 (competition and the two returns to information; analytical).**]{#result-proposition-1} *Let the incumbent's value have a continuous distribution $F$ on $[0,\bar r]$ with $0<p<\ell<\bar r<h$, and extend $F$ by unity above its support. A first-order stochastic strengthening of $F$ weakly increases the spread of target proceeds between a high- and a low-value challenger and weakly decreases the challenger's gross acquisition profit at every fixed posterior, where*

$$
\begin{aligned}
\Delta_T(F)&=\mathbb E_F[(R-\ell)_+]
=\int_\ell^{\bar r}[1-F(u)]\,du,\\
G_\theta(F)&=\mathbb E_F[(\theta-\max\{p,R\})_+]
=\int_p^\theta F(u)\,du.
\end{aligned}
\tag{6}\label{eq:paper-6}
$$

*Both comparisons are strict when the change in $F$ has positive integral over the corresponding range.*

The result follows directly from the payment rule. If $R\le\ell$, either challenger type outbids the incumbent and pays the same amount. If $R>\ell$, a high-value challenger wins and pays $R$, whereas a low-value challenger loses and the incumbent pays $\ell$. The difference in target proceeds is therefore $(R-\ell)_+$. A stronger incumbent increases its expectation. The same shift raises the payment required for the challenger to win and reduces its expected acquisition profit. [Appendix A](#paper-appendix) gives the proof.

<!-- FIGURE 1: figures/two_returns.pdf -->
> **Figure 1.** Competition and the two returns to information.
>
> **Notes.** Panel (a) plots the target-payoff spread $\Delta_T(r)$; panel (b) plots gross challenger profit $B_r(\mu)$ at the posterior bounds $m,M$ and the prior $1/2$. Benchmark values are $h=10$, $\ell=1$, $p=0.5$, and $b=2$. Values are per target share. These are acquisition-stage payoffs, before solving trading and entry.

Figure \ref{fig:1} shows both effects within the benchmark support. The target-payoff spread approaches zero as $r$ approaches $\ell$, since the incumbent then almost never outbids a low-value challenger. As $r$ increases, the spread rises while gross acquisition profit falls at each displayed belief. Whether entry rises depends on how this change in payoffs affects equilibrium information.

### 3.2 What the challenger learns from the price {#sec-inference}

Noise demand bounds the posterior under every feasible trading strategy. For arbitrary mixed orders, define

$$
\begin{aligned}
a_H(x)&=\int f(x-q)\,d\sigma_H(q),\qquad
&a_L(x)&=\int f(x-q)\,d\sigma_L(q),\\
\mu_X(x)&=\frac{a_H(x)}{a_H(x)+a_L(x)},\qquad
&m&=\frac1{1+e^{2/b}},\quad M=1-m.
\end{aligned}
\tag{7}\label{eq:paper-7}
$$

The posterior satisfies $m\le\mu_X\le M$. For any two orders $q,q'\in[-1,1]$, the Laplace density obeys

$$
e^{-2/b}\le\frac{f(x-q)}{f(x-q')}\le e^{2/b},
\tag{8}\label{eq:paper-8}
$$

Integrating over the conditional order distributions preserves these inequalities. Equal priors then give the posterior bounds. Since the price is a function of flow, the price-based posterior is a conditional expectation of $\mu_X$ and has the same bounds. A preparation decision requiring a belief above $M$ cannot be induced by any equilibrium price.

Suppose $c_L<B_r(m)$, so the low-cost challenger prepares at every feasible belief. Averaging over preparation costs gives the entry rule and candidate competitive price

$$
\begin{aligned}
e_r(\mu)&=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\\
P_r(\mu)&=t_0+e_r(\mu)[t_L-t_0+\Delta_T\mu].
\end{aligned}
\tag{9}\label{eq:paper-9}
$$

Both entry and the expected increment in target proceeds increase weakly with $\mu$. The increment is strictly increasing, and entry is bounded below by $\rho>0$, so $P_r(\mu)$ is strictly increasing. The price can jump when high-cost preparation becomes worthwhile.

Price sufficiency also holds in any candidate equilibrium, rather than only in this construction. Let $e(P)$ denote entry conditional on the observed price, averaged over costs. Competitive pricing implies

$$
\begin{aligned}
P&=t_0+e(P)[t_L-t_0+\Delta_T\mu_X],\\
\mu_X&=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}.
\end{aligned}
\tag{10}\label{eq:paper-10}
$$

The positive denominator makes $\mu_X$ a measurable function of $P$. The challenger can therefore recover the market maker's posterior from the price alone. This argument permits price atoms and entry jumps; it does not require differentiable prices. Propositions A.1 and A.2 give the formal statements.

### 3.3 Informed trading incentives {#sec-informed-trading-incentives}

Rational pricing removes the anticipated increase in proceeds from the investor's informational advantage. What remains depends on challenger quality. The residual advantages of buying in state $H$ and selling in state $L$ are

$$
\begin{aligned}
A_H(x)&=\mathbb E[V_T\mid H,x]-P(x)=e_r(\mu_X(x))\Delta_T[1-\mu_X(x)],\\
A_L(x)&=P(x)-\mathbb E[V_T\mid L,x]=e_r(\mu_X(x))\Delta_T\mu_X(x),\\
\rho m\Delta_T&\le A_H(x),A_L(x)\le\Delta_T.
\end{aligned}
\tag{11}\label{eq:paper-11}
$$

The market maker prices the entry response, but cannot identify quality perfectly because of noise demand. The investor's advantage is the entry probability times the target-payoff spread times the market's residual uncertainty. The lower bound uses the entry floor $\rho$ and posterior floor $m$; the upper bound is $\Delta_T$. Both hold for every candidate order distribution. Comparing these bounds with the trading cost determines when information can be sustained in equilibrium.

## 4. Equilibrium results {#sec-results}

### 4.1 Competition creates competition {#sec-competition-creates-competition}

The main result identifies an open set of economies in which stronger competition changes the unique trading and on-path preparation outcome from an uninformative price with low-cost preparation only to an informative price with additional high-cost preparation.

[**Proposition 2 (competition creates competition; analytical).**]{#result-proposition-2} *Fix $0<p<\ell<r_0<r_1<h$, $0<\rho<1$, $b>1$, and $k>0$, and suppose that*

$$
0\le c_L<B_{r_1}(m),
\tag{A1}\label{eq:paper-a1}
$$

$$
B_{r_0}(1/2)<c_H<B_{r_1}(M),
\tag{A2}\label{eq:paper-a2}
$$

$$
\Delta_T(r_0)<k<\left(1-\frac1b\right)\rho m\Delta_T(r_1).
\tag{A3}\label{eq:paper-a3}
$$

*(i) With the weak incumbent $r_0$, the unique equilibrium trading outcome is $q_H=q_L=0$, the price carries no information, and entry equals $\rho$. (ii) With the strong incumbent $r_1$, the unique equilibrium trading outcome is $(q_H,q_L)=(1,-1)$, the price is informative, entry strictly exceeds $\rho$, and the probability that the high-value challenger acquires the target is strictly higher than at $r_0$. The strong-incumbent price experiment strictly Blackwell dominates the weak-incumbent experiment at the same noise law. (iii) For any $r_2\in(r_1,h)$ with $c_L<B_{r_2}(m)$, $B_{r_2}(M)<c_H$, and $k<(1-1/b)\rho m\Delta_T(r_2)$, the unique trading outcome is again $(1,-1)$, but entry returns to $\rho$. These comparisons hold on a nonempty open set of primitives. Uniqueness refers to trading and on-path entry under truthful bidding and allows arbitrary mixed orders and every continuous deviation.*

Condition \eqref{eq:paper-a1} ensures that low-cost preparation is worthwhile even at the lowest feasible belief. Its economic role is a participation floor. Some preparation-cost realizations make investigation worthwhile even after an unfavorable price. Their participation makes the target's proceeds sensitive to challenger quality before favorable information recruits additional preparation, which supplies a base return to revealing that quality through trading. Without any such participation, or another source of state-sensitive target value, no preparation and no informative trading would remain mutually consistent: nobody prepares, proceeds do not depend on challenger quality, and the investor has nothing to trade on. The floor is therefore part of the mechanism, not a numerical regularizer. Condition \eqref{eq:paper-a2} excludes high-cost preparation at the weak-incumbent prior but permits it at favorable strong-incumbent prices. Condition \eqref{eq:paper-a3} places the trading cost above every possible informational return in the weak economy and below a global bound on marginal trading profits in the strong economy.

These inequalities determine trading before imposing a particular order profile. In the weak economy, the investor's gross advantage per unit is at most $\Delta_T(r_0)<k$, so every nonzero order loses money. With no informed trading, the posterior stays at the prior and only low-cost preparation occurs. In the strong economy, the residual lower bound is large enough to make every increase in a correctly signed order profitable. The bound controls the full order interval, including deviations from mixed candidate strategies. Full correctly signed orders are therefore necessary in every equilibrium. [Appendix A](#paper-appendix) derives the bound and constructs the associated price and entry schedules.

Under full orders, favorable prices cross the expensive challenger's preparation threshold with positive probability. Define the threshold belief $\tau$, its corresponding flow $x^*$, the conditional probabilities of crossing it $\alpha_H,\alpha_L$, total entry $\mathsf E$, and the probability of high-value challenger ownership $\mathsf O_H$ by

$$
\begin{aligned}
\tau&=\frac{c_H-g_L}{g_H-g_L},&
x^*&=\frac b2\log\frac\tau{1-\tau},\\
\alpha_H&=1-\frac12e^{(x^*-1)/b},&
\alpha_L&=\frac12e^{-(x^*+1)/b},\\
\mathsf E&=\rho+\frac{1-\rho}{2}(\alpha_H+\alpha_L),&
\mathsf O_H&=\frac12[\rho+(1-\rho)\alpha_H].
\end{aligned}
\tag{12}\label{eq:paper-12}
$$

Throughout, entry $\mathsf E$ is the preparation probability, the probability that the challenger pays its preparation cost. In the benchmark every prepared challenger has a value above the reserve, so a prepared challenger is always an admissible bidder, and the auction has two admissible bidders whenever the incumbent's value also meets the reserve. [Section 6.3](#sec-design) separates preparation from sale and from two admissible bidders when the reserve is raised. Condition \eqref{eq:paper-a2} places $\tau$ in $(1/2,M)$ and $x^*$ in $(0,1)$. Since $\alpha_H>\alpha_L$, the additional entry is tilted toward high-value challengers. At a sufficiently strong incumbent satisfying part (iii), even the largest feasible belief fails to justify high-cost preparation. Trading remains informative, but entry returns to $\rho$. The proposition establishes a rise and a subsequent fall across the specified economies; it does not impose a monotone path between them.

### 4.2 Benchmark and information controls {#sec-benchmark-and-information-controls}

The benchmark uses incumbent strengths $r_0=1.2$, $r_1=3$, and $r_2=3.6$; [Appendix A.8](#pa-parameters) lists the full parameter vectors. From $r_0$ to $r_1$, gross acquisition profit at the prior falls from 4.804167 to 4.291667, while the target-payoff spread rises from 0.016667 to 0.666667. Entry nevertheless rises from 0.250000 to 0.522757, and high-value challenger ownership rises from 0.125000 to 0.324192. At $r_2$, entry returns to 0.250000.

<!-- TABLE 1: tables/table1_auction_primitives.tex -->
> **Table 1.** Acquisition-stage payoffs in the benchmark.

<!-- TABLE 2: tables/table2_equilibrium_controls.tex -->
> **Table 2.** Equilibrium outcomes, information controls, and welfare.
>
> **Notes.** Panel A reports the unique trading and on-path preparation outcomes of [Proposition 2](#result-proposition-2) at each strength (analytical). Panel B reports fixed-profile controls: the frozen-order rows hold the investor's orders at their informative level and are not investor equilibria in the weak economy; the price-hidden rows re-solve trading with the price withheld from the challenger. The matched-dividend control is explained in Section 6.1. Panel C reports the fixed-strength welfare comparison of [Proposition A.9](#result-proposition-a-9). Rows are labeled by the role they play in the comparison; only the Panel A rows are equilibrium outcomes.

Table \ref{tab:1} reports the acquisition payoffs. Table \ref{tab:2} separates the analytical outcomes of [Proposition 2](#result-proposition-2) from fixed-profile controls. Holding informative orders fixed restores deterrence: entry falls from 0.562178 to 0.522757 as the incumbent strengthens. At every belief and cost realization, the decline in gross acquisition profit can only remove a preparation incentive. [Proposition A.3](#result-proposition-a-3) states this result for any fixed information experiment. The frozen profile is a control and not an investor equilibrium in the weak economy, since full orders are unprofitable there; in the strong economy it coincides with the equilibrium profile, but its role in the table is still that of a control.

Hiding prices from the challenger produces entry 0.250000 and 0.250000 at the two strengths. The buyer uses its prior and prepares only at low cost. Together, these comparisons identify the source of the reversal: incumbent strength changes the information generated by trading, and the resulting entry response can exceed the direct deterrence effect.

### 4.3 Coexistence and the equilibrium correspondence {#sec-coexistence-and-the-equilibrium-correspondence}

Informative trading need not be unique at intermediate strengths. [Proposition 3](#result-proposition-3) establishes three equilibria with full purchases and partial sales that coexist with no trade.

[**Proposition 3 (coexisting informative equilibria; computer-assisted).**]{#result-proposition-3} *At the benchmark parameters of [Appendix A.8](#pa-parameters), there exist equilibria $(q_H,q_L)=(1,-v_j)$ at strengths $r_j$ whose certified enclosures are*

$$
\begin{array}{c@{\qquad}c@{\qquad}c}
r_j&v_j&\mathsf E_j\\[3pt]
1.55&[0.46031618,\,0.46031620]&[0.5450528898,\,0.5450528922]\\
1.60&[0.70747537,\,0.70747539]&[0.5487563062,\,0.5487563085]\\
1.65&[0.90333198,\,0.90333201]&[0.5513607988,\,0.5513608020]
\end{array}
\tag{13}\label{eq:paper-13}
$$

*The entry intervals are strictly ordered upward. Each of the three economies also admits no trade with entry $\rho$.*

The proof uses interval arithmetic to enclose exact solutions. For the low-value investor, global strict concavity reduces optimality to a marginal-profit root. Opposite endpoint signs place a root inside each reported interval. For the high-value investor, a uniform derivative bound verifies that full purchases dominate every smaller order throughout the root bracket. Wrong-signed orders are unprofitable. The resulting entry enclosures are disjoint, which establishes the cross-economy ordering. [Appendix A](#paper-appendix) reports the certificate margins; [Online Appendix B](online_appendix.md#oa-b) supplies the complete method.

<!-- FIGURE 2: figures/equilibrium_correspondence.pdf -->
> **Figure 2.** Trading and entry across incumbent strengths.
>
> **Notes.** Benchmark parameters. Panel (a) shows preparation; panel (b) shows order magnitudes. Shading marks analytical uniqueness regions. Axis ticks mark nodes with distinct accepted continuations, labeled "multiplicity found; search not exhaustive"; they do not classify intervening strengths. $r_N$ is the no-trade existence boundary, $r_U$ the sufficient full-order uniqueness bound, and $r_C$ the high-cost preparation ceiling. Black points carry the certified intervals of [Proposition 3](#result-proposition-3). Other curves are numerical continuations, broken at unresolved nodes and branch changes; ambiguously matched roots remain isolated. A hollow diamond marks a mixed candidate's preparation. Upward and downward triangles show its high- and low-type support magnitudes, with size increasing in probability weight. At $r_C$, the filled circle includes preparation at indifference, while the hollow circle marks the right-hand limit after expensive preparation disappears. Absence of a branch does not establish nonexistence. [Online Appendix C.2](online_appendix.md#oa-c-correspondence) gives the methods and acceptance criteria.

Figure \ref{fig:2} places the certified equilibria within the numerical correspondence. No trade remains an equilibrium up to $r_N=1.747877538$ and is uniquely optimal below the sufficient bound $\mathfrak r(k)=1.220997512$. Full orders are uniquely optimal above the sufficient bound $r_U=2.837416964$. High-cost entry becomes infeasible above $r_C=3.592658519$. [Proposition A.4](#result-proposition-a-4) defines these thresholds. An existence boundary, a sufficient uniqueness bound, and a participation ceiling answer different questions and need not coincide.

The numerical continuation finds asymmetric informative equilibria before no trade disappears. On this family, the investor buys fully after good news and sells partially after bad news. The short magnitude increases toward one as the incumbent strengthens, and entry rises along the accepted continuation. Full orders subsequently coexist with no trade. The search also finds a symmetric interior family whose price information is insufficient to induce high-cost preparation, so entry remains $\rho$. The finite-support search also retains a mixed candidate at the no-trade existence boundary, shown as a numerical diagnostic. These descriptions concern the branches found and validated; the search is not exhaustive.

The trading asymmetry reflects the entry response. Around the high-cost preparation threshold, orders change both the posterior and the probability of entry, and thus the residual payoff to information. The low-value investor faces a different residual schedule from the high-value investor and can stop at an interior short while full purchases remain optimal. The certified points establish this behavior at three strengths. They do not prove a differentiable branch or a monotonicity result between the points.

No trade survives at the certified strengths because $\rho\Delta_T/2\le k$. Against an uninformative price with entry $\rho$, a unilateral informed order cannot cover its cost. An informative equilibrium instead changes the preparation response and the residual return to trading. The two outcomes can therefore be self-consistent at the same parameters.

At $r_C$, the Laplace posterior reaches its upper bound on a positive-probability tail. The convention that an indifferent challenger prepares preserves high-cost entry at the boundary itself; strictly above it, that entry disappears. The numerical searches also examined additional pure and finite-support mixed profiles. What they returned is a set of continuations found, not an exhaustive map. The complete intermediate correspondence is open.


## 5. Robustness and private information {#sec-extensions}

### 5.1 Noise and preparation costs {#sec-noise-and-preparation-costs}

The reversal extends beyond the benchmark's Laplace noise and two preparation-cost levels. Logistic noise also has a log-density derivative bounded in absolute value by $1/b$, so the global trading bounds remain valid. [Proposition A.5](#result-proposition-a-5) establishes the corresponding equilibrium and entry comparisons. Unlike the Laplace posterior, the logistic posterior reaches its bounds only as order flow tends to infinity.

In the strong benchmark economy, entry is 0.301509 under logistic noise, compared with 0.522757 under Laplace noise. The logistic flow threshold is 5.424598398, or 1.495369 noise standard deviations from the center. Thus the same posterior bounds can support different participation rates: the probability of favorable information near the upper bound also matters.

<!-- FIGURE 3: figures/posterior_tail_entry.pdf -->
> **Figure 3.** Posterior tails and high-cost entry.
>
> **Notes.** Full orders at the strong benchmark strength and scale $b=2$. Panel (a) plots $\Pr(\mu_X\ge\tau)$ against $M-\tau$; panel (b) plots implied entry. At zero threshold distance, the Laplace plateau carries positive mass and induces entry under the tie rule. The logistic tail probability is zero there and is drawn as a closed point at zero mass in panel (a) and at baseline preparation $\rho$ in panel (b); the bound is unattained by any posterior realization, but the plotted function is defined at it. Common scale $b$, not common variance, is held fixed across the two noise laws. These are fixed-profile comparisons; [Online Appendix C.5](online_appendix.md#oa-c-noise) records equilibrium validation for each implied cost. The figure is not a Blackwell ranking of the noise laws.

Figure \ref{fig:3} compares the probability of crossing a preparation threshold close to $M$. Laplace noise assigns positive probability to the upper posterior bound; logistic noise does not. The comparison concerns the location of posterior mass at a common scale parameter, and cannot be interpreted as a general ordering of informativeness.

The result also holds when low and high preparation costs are drawn from atomless distributions with sufficiently narrow supports. The support conditions ensure that every low-cost realization prepares at every feasible belief, while high-cost preparation occurs only after sufficiently favorable prices in the strong economy. This preserves the entry floor and the global trading bounds. [Proposition A.6](#result-proposition-a-6) states the result, and [Appendix A](#paper-appendix) gives the support restrictions. With the declared cost half-width, strong-incumbent entry is 0.522715 under Laplace noise and 0.301374 under logistic noise.

### 5.2 Acquisition values {#sec-acquisition-values}

The reversal does not require the benchmark's tenfold gap between high and low acquisition values. With $h=2$ and $\ell=1$, the moderate-value specification satisfies all strict inequalities of [Proposition 2](#result-proposition-2). Entry rises from 0.250000 to 0.526805. More generally, for any $h>\ell$, the proof constructs weak and strong incumbent strengths sufficiently close to $\ell$, together with costs satisfying the strict inequalities. The relevant requirement is the placement of incumbent strength relative to the low acquisition value. [Appendix A](#paper-appendix) provides the construction; [Online Appendix C.4](online_appendix.md#oa-c-moderate) records the numerical examples.

### 5.3 Complementary private information {#sec-complementary-private-information}

The challenger can benefit from prices even when its own information is more accurate than the investor's. A buyer may know its integration technology, while investors following the target hold information about its customers or product market. Diligence combines these sources. I represent this possibility with conditionally independent binary signals: the investor observes $T$ with accuracy $a$, and the buyer observes $Y$ with accuracy $d$, where $a,d\in(1/2,1)$. The buyer observes its signal and the price before preparing; preparation still reveals the exact acquisition value.

Private information makes entry state-dependent even conditional on the price. A high-value challenger is more likely to receive favorable private information and therefore more likely to prepare. Competitive pricing incorporates both conditional entry rates. Nevertheless, the positive entry floor leaves a strictly positive coefficient on public beliefs, so the price still reveals the market's posterior. The buyer combines that posterior with its own signal. [Appendix A](#paper-appendix) derives the posterior formulas, state-dependent pricing, and trading bounds.

[Proposition A.7](#result-proposition-a-7) gives sufficient conditions for unique zero orders and entry $\rho$ in the weak economy, and unique full orders by investor signal with entry above $\rho$ in the strong economy. These conditions allow arbitrary mixed signal-contingent orders and every continuous deviation. They do not require the investor's signal to be more accurate than the buyer's.

The declared example has buyer accuracy 75\% and investor accuracy 70\%. Entry rises from 0.850000 to 0.879438. A favorable private signal alone does not justify high-cost preparation against the weak incumbent; combined with a favorable price, it does against the strong incumbent. Table \ref{tab:3} reports this example with the other robustness checks. The full accuracy grid, including validated economies outside the sufficient uniqueness region, appears in [Online Appendix C.3](online_appendix.md#oa-c-signals).

<!-- TABLE 3: tables/table3_extensions.tex -->
> **Table 3.** Robustness and complementary private information.
>
> **Notes.** The main comparison column is the change in preparation from the weak to the strong economy, in percentage points, computed from the same validated preparation probabilities that the weak and strong columns report. The moderate-value and complementary-signal rows use distinct parameter vectors and are separate illustrations, not one joint calibration. The individual theorem margins and their minimum are in the online table.

## 6. Welfare and sale terms {#sec-welfare}

### 6.1 Access to prices {#sec-access-to-prices}

Access to prices improves acquisition outcomes at a fixed level of competition. Hold the incumbent at $r_1$ and compare the feedback equilibrium with an economy in which the challenger cannot observe the price. All other parameters are unchanged, and trading and pricing are reoptimized in both economies. [Proposition A.9](#result-proposition-a-9) establishes that price access increases expected target proceeds and acquisition surplus net of preparation costs. The comparison also holds with logistic noise and atomless preparation costs.

The two economies generate the same order-flow experiment. The global trading bound forces full orders even when the challenger cannot use the price and entry remains $\rho$. Trading costs therefore coincide. Price access changes which high-cost challengers prepare. Each additional preparation decision contributes at least the preparation cost it incurs in conditional expectation, given the price information and the cost realization that induce it; a challenger prepares only when expected gross acquisition profit covers that cost. The allocation gain includes that profit and the value of sales that would otherwise fail the reserve. [Appendix A](#paper-appendix) gives the accounting identities. Transfers between bidders, shareholders, and traders are excluded from acquisition surplus.

Table \ref{tab:2} reports the fixed-strength comparison. Expected target proceeds are 0.872392 with price access and 0.614583 without it. This is a welfare result about access to information under a given sale rule and incumbent distribution; it does not rank different incumbent strengths or sale mechanisms.

The information effect can be separated from the average price level by an analytical invariance diagnostic. Add a deterministic external dividend of 0.257809 to the traded claim in the price-hidden economy. The dividend raises both the terminal financial payoff and its price by the same amount, leaving $V_T-P$, trading incentives, seller revenue, acquisition surplus, and entry unchanged. The mean financial price then matches that of the feedback economy, while entry still differs. What separates the two economies is the information the price carries, not its level. The dividend is attached to the financial claim, is not paid by any bidder, and is not a sale term the seller could choose. It is a diagnostic, not a feasible sale mechanism, and it is excluded from acquisition surplus. The online matched-price panel reports it beside the hidden and feedback rows.

### 6.2 The payment rule {#sec-the-payment-rule}

The effect of competition on target-payoff sensitivity depends on the sale payment. To isolate this dependence, consider a verifiable-value institution with zero reserve. After diligence, the highest-value buyer acquires the target. A sale to the next-best buyer at its value is an enforceable fallback, accepted at zero surplus. The seller and winner divide the surplus above this fallback by Nash bargaining, with seller share $\eta$.

Without a challenger, the seller receives $\eta R$. For an incumbent distribution supported on $[0,R_{\max}]$, with $\ell<R_{\max}<h$ and $0\le\eta<1$, the transfer, challenger profit, and target-payoff spread are

$$
\begin{aligned}
T_\eta(R,\theta)&=(1-\eta)\min\{R,\theta\}+\eta\max\{R,\theta\},\\
G_{\theta,\eta}&=(1-\eta)\mathbb E[(\theta-R)_+],\\
\Delta_\eta&=\eta(h-\ell)+(1-2\eta)\mathbb E[(R-\ell)_+].
\end{aligned}
\tag{14}\label{eq:paper-14}
$$

[Proposition A.8](#result-proposition-a-8) establishes the comparative statics. A stronger incumbent weakly reduces challenger profit for every bargaining weight. Its effect on the target-payoff spread is positive for $\eta<1/2$, zero at $\eta=1/2$, and negative for $\eta>1/2$, with strictness determined by the change in the incumbent distribution.

To see why, take $R>\ell$. A high-value challenger wins and pays $(1-\eta)R+\eta h$, whose sensitivity to $R$ is $1-\eta$. A low-value challenger loses, and the incumbent pays $(1-\eta)\ell+\eta R$, whose sensitivity is $\eta$. Competition widens the difference precisely when the first sensitivity exceeds the second. Thus the benchmark's opposition between acquisition profit and target-payoff sensitivity depends on the weight placed on the runner-up's value.

<!-- FIGURE 4: figures/bargaining_weight.pdf -->
> **Figure 4.** Bargaining and the division of acquisition surplus.
>
> **Notes.** Zero-reserve verifiable-value institution, $h=10$, $\ell=1$, and uniform incumbents with $r=1.2$ or $r=3$. Panel (a) plots $\Delta_\eta$ against seller weight $\eta$; panel (b) plots conditional challenger profits on a log scale. Values are per target share. The comparison is confined to the payment stage: it concerns acquisition-stage payoffs under this institution, and trading, preparation, and welfare under bargaining are not solved. The log-scale panel uses the declared domain of seller weights below one.

Figure \ref{fig:4} illustrates these payment-stage results. They identify a condition under which stronger competition increases the sensitivity of target shares to challenger quality. They do not establish an entry reversal under bargaining, which would require solving its trading and participation game.

### 6.3 Reserve comparisons {#sec-design}

A reserve affects both the payment required to win and the information embedded in target shares. A reserve that excludes the low-value challenger can widen the difference in target proceeds across challenger types. This can support informative trading even against a weak incumbent. I illustrate this possibility with two reserve levels; the seller's continuation problem and local revenue decomposition appear in Appendix A.7.

Once the reserve can exclude bidders, preparation, sale, and competition come apart. The preparation probability is the probability that the challenger pays its preparation cost. The sale probability is the probability that at least one bidder submits an admissible bid, whether the incumbent or a prepared challenger whose realized value meets the reserve. The probability of two admissible bidders is the probability that both do. In the benchmark of [Section 4](#sec-results) the reserve lies below both challenger values, so every prepared challenger is admissible. At a reserve above the low value, a prepared challenger can learn that it cannot bid, and at a reserve above the incumbent's support the incumbent is excluded. An excluded incumbent facing one challenger that may or may not be admissible is not a two-bidder contest, and a positive preparation probability in that case is not evidence of more acquisition competition. Table \ref{tab:4} reports all three probabilities beside expected target proceeds.

To avoid making exclusion depend on an acquisition-value atom, let quality identify a low or high value class, each with probability one half. Conditional values are uniform around $\ell$ and $h$ with half-width $\varepsilon_V=0.05$. The investor observes the class, and preparation reveals the exact value. Increasing the reserve from 0.5 to 1.1 raises weak-incumbent expected proceeds from 0.392665 to 0.432173 and strong-incumbent expected proceeds from 0.872367 to 1.014500. At the higher reserve, the preparation probability is 0.540309 and 0.511638, respectively, and trading is informative in both economies. The global bounds establish unique trading continuations at the reported reserve choices.

<!-- TABLE 4: tables/table4_reserve_comparisons.tex -->
> **Table 4.** Reserve comparisons.
>
> **Notes.** Columns report the preparation probability, the sale probability, the probability of two admissible bidders, expected target proceeds, and the trading outcome at each listed economy and reserve. Panel A uses binary acquisition values; Panel B uses atomless value classes. The listed nodes have analytical support from the global trading bounds; order magnitudes, margins, evidence status, and complete parameters are in the online table. The exploratory reserve summary, headed by the highest revenue among continuations found, is reported online with its unresolved counts.

Table \ref{tab:4} reports the declared comparisons. The higher reserve excludes the low-value class and changes both acquisition incentives and the target-payoff spread. Its revenue advantage demonstrates a feasible improvement over the original reserve. It does not identify an optimal reserve, and I do not report a best reserve in the main text. The audited exploratory summary over the reserve domain is reported online among continuations found; neither an envelope of found revenues nor a missing continuation establishes the seller's solution.

Away from the region with a positive preparation floor, a continuation specifies a price-pooling rule as well as investor orders. Different pooling regions can support different buyer posteriors and different preparation decisions at the same order profile, because the buyer sees only the price and the pool determines what the price reveals. I therefore treat orders, price pools, beliefs, and preparation as joint equilibrium objects. Numerical continuations are distinguished by their complete price and trading schedules, and a single candidate pricing construction is not an equilibrium-selection rule for the seller. [Appendix A.7](#pa-design) gives the derivation, and the Online Appendix subsection "Price pooling when preparation can vanish" gives the full argument and a worked example.

## 7. Empirical implications {#sec-program}

The model concerns a decision to prepare, made before the set of executable bids is fixed. An empirical counterpart is the start of substantive diligence or the submission of a proposal requiring costly preparation, rather than the number of public offers. Incumbent strength would have to be measured from information public before that decision, and the relevant price information would have to precede preparation. Later target returns can reflect anticipated bidder arrival, so an association between returns and later entry would not by itself show learning from prices.

[Online Appendix D](online_appendix.md#oa-d) proposes an institutional pilot that reconstructs the timing of approaches, public visibility, buyer contacts, diligence, proposals, and final selection from disclosure records. It separates the date on which an event occurred from the date on which it first became public. The first requirement is a publicly understood sale opportunity that remains contestable while a prospective challenger decides whether to investigate. A traded stock during confidential negotiations is insufficient. The pilot is a design only. No sample has been assembled, and no effect, instrument, or identification strategy is reported.

## 8. Conclusion {#sec-conclusion}

The bidder pool in a takeover depends on the information available before buyers commit to participation. A stronger incumbent can increase the sensitivity of target proceeds to challenger quality, making informed trading profitable and bringing a challenger into the auction. This connects the division of acquisition surplus to the formation of competition. Sale terms therefore affect participation through both the buyer's expected payment and the information supplied by the stock market.

The next theoretical step is to characterize the seller's choice of terms with the full pricing-and-trading continuation correspondence retained, including the price-pooling rules that can differ at identical orders. The reserve comparisons show why this choice matters, while multiplicity prevents identifying the seller's objective with an envelope of found revenues. A related question is whether committing before trading improves outcomes relative to revising terms after observing prices. Solving alternative auction formats and endogenous investor research would clarify the role of payment rules and manipulation incentives [@GoldsteinGuembel2008]. Empirical work would first have to establish the decision interval and information sets under which buyers can learn from prices.

```{=latex}
\clearpage
```

## References {#references}

::: {#refs}
:::


```{=latex}
\clearpage
```

## Appendix A {#paper-appendix}

This appendix contains the complete chain of steps for every result stated in the paper. Definitions sit next to the statements that use them. Each formal statement carries its status once: analytical, computer-assisted, numerical diagnostic, or open. The Online Appendix retains the probability-space construction, regular conditional distributions, null-set invariance under deviations, the full convolution regularity, the Stieltjes argument, interval endpoint ordering, the complete signal laws, and the numerical definitions. Equation numbers \eqref{eq:paper-1} to \eqref{eq:paper-14} refer to the main text.

### A.1 Acquisition payoffs and Bayesian pricing {#pa-results}

#### Proof of [Proposition 1](#result-proposition-1)

The realized sale rule determines every payoff. Without entry the target receives $p\mathbf1\{R\ge p\}$. With a high-value challenger the challenger wins and pays $\max\{p,R\}$, so the reserve stays in the winning payment. With a low-value challenger the target receives $\max\{p,\min(R,\ell)\}$ and the challenger keeps $(\ell-\max\{p,R\})_+$. Truthful bidding is weakly dominant conditional on every competing bid, so none of this depends on a conjectured shading strategy. For the uniform incumbent,

$$
\begin{aligned}
t_H&=\frac1r\left[\int_0^p p\,du+\int_p^r u\,du\right],\\
t_L&=\frac1r\left[\int_0^p p\,du+\int_p^\ell u\,du+\int_\ell^r\ell\,du\right],\\
g_L&=\frac1r\left[\int_0^p(\ell-p)\,du+\int_p^\ell(\ell-u)\,du\right],
\end{aligned}
\tag{A.1}\label{eq:paper-a-1}
$$

which evaluate to \eqref{eq:paper-4} and differentiate to \eqref{eq:paper-5}.

The distribution-free opposition rests on one pointwise observation. If $R\le\ell$, the high and low target payments coincide at $\max\{p,R\}$; if $R>\ell$, the high-value challenger pays $R$ while the incumbent pays $\ell$. The pointwise difference is $(R-\ell)_+$. Writing the positive parts as integrals of indicators,

$$
(R-\ell)_+=\int_\ell^{\bar r}\mathbf1\{R>u\}\,du,
\qquad
(\theta-\max\{p,R\})_+=\int_p^\theta\mathbf1\{R<u\}\,du,
\tag{A.2}\label{eq:paper-a-2}
$$

and Tonelli's theorem applied to the nonnegative integrands gives both integrals in \eqref{eq:paper-6}, with $F$ extended by unity above its support so that the second integral runs to $\theta=h>\bar r$. A first-order stochastic strengthening lowers $F$ pointwise, which raises the survival integral and lowers the profit integral. Positive integral differences make the comparisons strict, and a weighted average at a fixed posterior preserves the profit ordering. The generality is conditional on the stated cash second-price institution with reserve. The pointwise difference $(R-\ell)_+$ is a property of that payment rule, and [Section 6.2](#sec-the-payment-rule) shows that another institution changes it. [Online Appendix A.2](online_appendix.md#oa-a-payoffs) gives the measure formulation. $\square$

#### Posterior bounds

[**Proposition A.1 (posterior bounds; analytical).**]{#result-proposition-a-1} *For arbitrary mixed state-contingent orders on $[-1,1]$, the order-flow posterior $\mu_X$ and the posterior based on the price lie in $[m,M]$, where $a_H$, $a_L$, $\mu_X$, $m$, and $M$ are defined in \eqref{eq:paper-7}.*

For any feasible orders $q,q'$ the triangle inequality gives $\big||x-q|-|x-q'|\big|\le|q-q'|\le2$, which is \eqref{eq:paper-8}. Integrating against $d\sigma_H(q)\,d\sigma_L(q')$ preserves both inequalities, so $e^{-2/b}a_L\le a_H\le e^{2/b}a_L$ for arbitrary conditional mixtures, and equal priors turn this into $m\le\mu_X\le M$. No monotone or pure strategy is assumed. Because the price is a function of $X$, the price posterior is $\mathbb E[\mu_X\mid P]$ by the tower property and inherits the interval. [Online Appendix A.1](online_appendix.md#oa-a-foundations) gives the measure-theoretic version, including the null-set invariance under unilateral deviations. $\square$

#### Price sufficiency and residual profits

[**Proposition A.2 (price sufficiency and residual profits; analytical).**]{#result-proposition-a-2} *Suppose $c_L<B_r(m)$. In every candidate equilibrium the observed price reveals $\mu_X$ almost surely. Entry and competitive pricing take the form \eqref{eq:paper-9}, and the residual advantages of an informed buyer of shares in state $H$ and of an informed short seller in state $L$ are given by \eqref{eq:paper-11}, with $\rho m\Delta_T\le A_H(x),A_L(x)\le\Delta_T$.*

*Floor.* By [Proposition A.1](#result-proposition-a-1) every feasible price posterior is at least $m$, so the low-cost type enters at every price that can be reached; cost-averaged entry conditional on the price, $e(P)$, is at least $\rho$. This is established before any division.

*Inversion.* Competitive pricing gives the first line of \eqref{eq:paper-10} pointwise in flow, with $e(P)$ a function of the price. Since $e(P)\Delta_T\ge\rho\Delta_T>0$, the second line of \eqref{eq:paper-10} expresses $\mu_X$ as a Borel function of $P$. Conditioning $\mu_X$ on the price therefore leaves it unchanged, and $\Pr(H\mid P)=\mathbb E[\mu_X\mid P]=\mu_X$ almost surely. Entry is then \eqref{eq:paper-9} with the buyer's own posterior.

*Construction.* Put $w_L=t_L-t_0>0$. For $\mu_2>\mu_1$, \eqref{eq:paper-9} gives

$$
P_r(\mu_2)-P_r(\mu_1)
=e_r(\mu_2)\Delta_T(\mu_2-\mu_1)+[e_r(\mu_2)-e_r(\mu_1)](w_L+\Delta_T\mu_1)
\ge\rho\Delta_T(\mu_2-\mu_1)>0,
\tag{A.3}\label{eq:paper-a-3}
$$

because entry is nondecreasing and the bracket is positive. The price is therefore strictly increasing in the posterior, including across the jump where high-cost preparation becomes worthwhile, and its inverse on its image is measurable. A price value inside the skipped interval is generated by no flow. A flat posterior tail maps into an actual price atom, which is conditioned on as an atom.

*Residuals.* Conditional on quality $\theta$ and flow $x$, expected terminal value is $t_0+e(P(x))(t_\theta-t_0)$, in which the no-entry proceeds and the public entry effect both appear. Subtracting the rational price $t_0+e(P(x))[w_L+\Delta_T\mu_X(x)]$ in state $H$, and reversing the subtraction in state $L$, the terms $t_0$ and $e\,w_L$ cancel and leave \eqref{eq:paper-11}. No unanticipated premium is attached. The bounds follow from $\rho\le e\le1$ and $m\le\mu_X\le M=1-m$. [Online Appendix A.3](online_appendix.md#oa-a-inference) supplies the conditional-probability argument. $\square$

### A.2 Global trading and the main comparison {#pa-proofs}

#### The global order bound

Fix a candidate pricing and preparation schedule. For a correctly signed order of magnitude $s\in[0,1]$ define

$$
\begin{aligned}
F_H(s)&=\int f(x-s)A_H(x)\,dx,\qquad
F_L(s)=\int f(x+s)A_L(x)\,dx,\\
U_\theta(s)&=sF_\theta(s)-ks.
\end{aligned}
\tag{A.4}\label{eq:paper-a-4}
$$

The residual $A_\theta$ is bounded and measurable but need not be continuous, since it jumps where entry jumps. The deviation enters only through the translated density. For $s_1<s_2$,

$$
F_\theta(s_2)-F_\theta(s_1)
=\int_{s_1}^{s_2}\int \partial_u f(x\mp u)\,A_\theta(x)\,dx\,du,
\tag{A.5}\label{eq:paper-a-5}
$$

by the fundamental theorem of calculus for the absolutely continuous Laplace density and Fubini's theorem, which applies because the absolute double integral is at most $\|A_\theta\|_\infty\,|s_2-s_1|\,\|f'\|_1$. Thus $F_\theta$ is absolutely continuous, and $|f'|\le f/b$ gives $|F_\theta'|\le F_\theta/b$ almost everywhere. A jump in entry therefore never has to be differentiated during a unilateral deviation. The derivative falls on the density, not on the schedule. With the residual lower bound in \eqref{eq:paper-11},

$$
U_\theta'(s)=F_\theta(s)+sF_\theta'(s)-k
\ge\left(1-\frac sb\right)F_\theta(s)-k
\ge\left(1-\frac1b\right)\rho m\Delta_T-k>0
\tag{A.6}\label{eq:paper-a-6}
$$

under the strong-incumbent inequality in \eqref{eq:paper-a3}, for every $s\in[0,1]$. Integrating the positive lower bound shows that the full correctly signed order strictly dominates every smaller magnitude; this is global optimality, not a first-order condition. [Online Appendix A.3](online_appendix.md#oa-a-inference) retains the $W^{1,1}$ and null-set details.

A sharper existence test applies to a fixed full-order candidate. Substituting Bayes' rule into both residuals gives

$$
J=F_H(1)=F_L(1)
=\Delta_T\int e(x)\frac{f(x-1)f(x+1)}{f(x-1)+f(x+1)}\,dx,
\tag{A.7}\label{eq:paper-a-7}
$$

and the pointwise ratio $f(x-s)/f(x-1)\ge e^{-(1-s)/b}$ gives $F_\theta(s)\ge e^{-(1-s)/b}J$. Since $(1-s/b)e^{-(1-s)/b}$ is decreasing on $[0,1]$, the inequality $k<(1-1/b)J$ makes every correctly signed marginal profit positive against that candidate. This verifies existence of the full-order profile; it says nothing about other candidate schedules.

#### Proof of [Proposition 2](#result-proposition-2)

The proof first restricts trading in every candidate equilibrium, then constructs prices and preparation under the forced profile. Excluding competing order profiles is necessity; the construction supplies existence.

*Step 1: beliefs.* Positivity of $f$ makes every conditional flow density positive, and [Proposition A.1](#result-proposition-a-1) gives $m\le\mu_X\le M$ under every trading strategy; the price posterior obeys the same bound. Because $g_H$ and $g_L$ both fall with $r$, condition \eqref{eq:paper-a1} gives $c_L<B_r(m)$ in both economies, so [Proposition A.2](#result-proposition-a-2) applies in both.

*Step 2: the buyer's information.* By [Proposition A.2](#result-proposition-a-2), $\Pr(H\mid P)=\mu_X$ almost surely, entry is \eqref{eq:paper-9}, and the residuals are \eqref{eq:paper-11}. This uses the independence of $R$ and $C$ from trading, not an assumption that the buyer sees order flow.

*Step 3: the weak economy.* A correctly signed order of size $s>0$ earns $s[F_\theta(s)-k]\le s[\Delta_T(r_0)-k]<0$ by the upper bound in \eqref{eq:paper-11} and the first inequality in \eqref{eq:paper-a3}. A wrong-signed order has negative gross payoff and still pays its cost. Zero is therefore the only best response against every candidate schedule, and a mixture placing positive probability on nonzero orders averages strictly negative payoffs with zero. Under zero orders $X=Z$, $\mu_X=1/2$, and \eqref{eq:paper-a1} and \eqref{eq:paper-a2} give entry $\rho$; the constant price $t_0+\rho[(t_H+t_L)/2-t_0]$ is competitive. This constructs the unique outcome of part (i).

*Step 4: the strong economy.* Against every candidate schedule, \eqref{eq:paper-a-6} holds on the whole order interval. Every equilibrium therefore has $(q_H,q_L)=(1,-1)$, and mixing cannot introduce another optimal action.

*Step 5: existence.* Full orders give

$$
\mu_X(x)=\left[1+\exp\left\{-\frac{|x+1|-|x-1|}{b}\right\}\right]^{-1},
\tag{A.8}\label{eq:paper-a-8}
$$

equal to $m$ on $x\le-1$, strictly increasing on $(-1,1)$, and equal to $M$ on $x\ge1$. Define entry and price by \eqref{eq:paper-9}. The strict monotonicity \eqref{eq:paper-a-3} gives a measurable inverse on the price's image, including across its upward jump and at the two plateau atoms. The buyer recovers the posterior from the price, prepares optimally, and bids truthfully; \eqref{eq:paper-a-6} verifies investor optimality; the price is competitive by construction.

*Step 6: comparisons.* Since $B_r$ increases in $\mu$ and decreases in $r$, condition \eqref{eq:paper-a2} places $\tau$ in $(1/2,M)$ and $x^*$ in $(0,1)$. The Laplace survival function evaluated at $x^*-1$ and $x^*+1$ gives $\alpha_H$ and $\alpha_L$ in \eqref{eq:paper-12}, both positive, so entry exceeds $\rho$ and high-value ownership $\mathsf O_H=e_H/2$ exceeds $\rho/2$ because $h>r$. Applying a constant kernel to the strong-economy price reproduces the weak economy's constant experiment, while no state-independent kernel applied to a constant experiment can produce the nonconstant state-dependent price law of the strong economy; the strong experiment therefore strictly Blackwell dominates the weak one. All inequalities are strict and continuous in the primitives away from the support boundaries, so the region is open; [Appendix A.4](#pa-calculations) shows it is nonempty for every $h>\ell$.

*Part (iii).* At $r_2$ the low-cost floor and the derivative bound give unique full orders exactly as in Steps 4 and 5, while $B_{r_2}(M)<c_H$ excludes every expensive entrant because $M$ is the largest attainable belief under any strategy. Entry returns to $\rho$. These conditions are separate from \eqref{eq:paper-a1} to \eqref{eq:paper-a3} and establish a rise and a subsequent fall across three economies, not a monotone path. $\square$

#### Deterrence at a fixed experiment

[**Proposition A.3 (deterrence at a fixed information experiment; analytical).**]{#result-proposition-a-3} *Let a signal $S$ and quality $\Theta$ have a fixed joint distribution, and let the preparation cost $C$ be independent of $(S,\Theta)$ with a fixed law, as in the model. Hold this experiment and cost law fixed as $r$ changes, so the buyer's posterior $\Pr(H\mid S)$ does not depend on $r$. Then entry is weakly decreasing in $r$. It decreases strictly when the decline in gross profit crosses preparation costs on a positive-probability set of signal and cost realizations.*

Write $\mu(S)=\Pr(H\mid S)$; cost independence makes this the buyer's complete posterior about quality. For $r_1>r_0$, $B_{r_1}(\mu)\le B_{r_0}(\mu)$ at every $\mu$ by \eqref{eq:paper-5}, so

$$
\mathbf1\{C\le B_{r_0}(\mu(S))\}-\mathbf1\{C\le B_{r_1}(\mu(S))\}
=\mathbf1\{B_{r_1}(\mu(S))<C\le B_{r_0}(\mu(S))\}\ge0.
\tag{A.9}\label{eq:paper-a-9}
$$

Taking expectations proves the weak decrease and the exact strictness condition, without an atomless cost distribution. The result applies within a region of fixed full orders, where the conditional flow laws do not depend on $r$; it does not apply across order profiles that change with $r$, because changing orders change the experiment. A version with cost correlated with the signal would condition on $\Pr(H\mid S,C)$ and is not needed here. $\square$

#### Threshold distinctions

[**Proposition A.4 (pooling, full orders, and expensive-entry feasibility; analytical).**]{#result-proposition-a-4} *Restrict attention to the maintained domain $\mathcal D=\{r\in(\ell,h):c_L<B_r(m),\ B_r(1/2)<c_H\}$. Define*

$$
\begin{aligned}
\mathfrak r(d)&=\ell+d+\sqrt{d^2+2\ell d},\\
r_N&=\mathfrak r(2k/\rho),\qquad
r_U=\mathfrak r\left(\frac{k}{(1-1/b)\rho m}\right).
\end{aligned}
\tag{A.10}\label{eq:paper-a-10}
$$

*No trade is an equilibrium exactly when $\rho\Delta_T(r)/2\le k$, that is, when $r\le r_N$. The stronger restriction $r<\mathfrak r(k)$ guarantees that it is the unique outcome. The restriction $r>r_U$ guarantees unique full orders. Expensive entry is impossible in every equilibrium when $B_r(M)<c_H$. If the equality $B_r(M)=c_H$ has a solution in $\mathcal D$, its unique crossing is*

$$
r_C=\frac{Mh-c_H+\sqrt{(Mh-c_H)^2+M[(1-M)\ell^2-p^2]}}{M}.
\tag{A.11}\label{eq:paper-a-11}
$$

*At $r_C$ the tie rule of [Section 2](#sec-model) is retained.*

Under no trade the posterior is $1/2$ and entry is $\rho$, so a unilateral correctly signed order of size $s$ sees the constant residual $\rho\Delta_T/2$ and earns

$$
s\left(\frac{\rho\Delta_T(r)}{2}-k\right).
\tag{A.12}\label{eq:paper-a-12}
$$

Zero is optimal exactly when the coefficient is nonpositive. Solving $\Delta_T(r)=d$ gives $(r-\ell)^2=2rd$, whose root above $\ell$ is $\mathfrak r(d)$; since $\Delta_T$ is increasing, the pooling-existence boundary is $r_N$. Equality at $r_N$ leaves the investor indifferent among correctly signed sizes against that constant schedule; it does not make every other profile an equilibrium with recomputed prices. The sufficient uniqueness boundary $\mathfrak r(k)$ comes from $\Delta_T<k$, which defeats any nonzero order against every candidate schedule by Step 3 above. The full-order boundary $r_U$ comes from \eqref{eq:paper-a-6}. The ceiling profit is

$$
B_r(M)=Mh-\frac{Mr}{2}+\frac{(1-M)\ell^2-p^2}{2r},
\tag{A.13}\label{eq:paper-a-13}
$$

strictly decreasing on $r>\ell>p$, so it crosses $c_H$ at most once; \eqref{eq:paper-a-11} is the larger root of $Mr^2-2(Mh-c_H)r-[(1-M)\ell^2-p^2]=0$ and is the crossing when it lies in $\mathcal D$. Because $M$ is the largest posterior under any strategy, $B_r(M)<c_H$ excludes expensive entry regardless of orders. The four objects answer different questions: an existence boundary, two sufficient uniqueness bounds, and a participation ceiling; none identifies the first appearance of an informative equilibrium.

Under full Laplace orders $\mu_X=M$ on the positive-probability tail $x\ge1$, so indifference at $r_C$ is not a null event and the tie rule admits expensive entry on that tail. As $r\uparrow r_C$, the threshold $x^*\to1$ and

$$
\alpha_H\to\frac12,\qquad\alpha_L\to\frac12e^{-2/b},\qquad
\mathsf E(r)\to\rho+\frac{1-\rho}{4}\left(1+e^{-2/b}\right),
\tag{A.14}\label{eq:paper-a-14}
$$

whereas strictly above $r_C$ expensive entry is impossible. Under logistic noise the posterior reaches $M$ only in the limit, so expensive entry converges to zero continuously ([Appendix A.4](#pa-calculations)). [Online Appendix A.5](online_appendix.md#oa-a-thresholds) has the domain checks. $\square$

### A.3 Certified asymmetric equilibria {#pa-certificate}

#### Root definition

Fix the benchmark primitives and a strength $r$. Candidate orders are $(q_H,q_L)=(1,-v)$ with $0<v<1$. Bayes' rule gives $\mu_v(x)=\operatorname{logistic}((|x+v|-|x-1|)/b)$, which ranges from $m_v=(1+e^{(1+v)/b})^{-1}$ to $M_v=1-m_v$. In the certified region $1/2<\tau<M_v$, and

$$
\begin{aligned}
x^*(r,v)&=\frac{b\operatorname{logit}(\tau)+1-v}{2}\in(-v,1),\\
\mathsf E(r,v)&=\rho+\frac{1-\rho}{2}
\left[1-\frac12e^{(x^*-1)/b}+\frac12e^{-(x^*+v)/b}\right].
\end{aligned}
\tag{A.15}\label{eq:paper-a-15}
$$

The entry rule is $e(x)=\rho+(1-\rho)\mathbf1\{x\ge x^*\}$ and the residuals are $A_H=e\Delta_T(1-\mu_v)$ and $A_L=e\Delta_T\mu_v$. Let $\Psi(r,v)=U_L'(v;1,-v)$, where the derivative is taken in the deviating magnitude $s$ at $s=v$ while the candidate schedule is held fixed; recomputing the schedule as $v$ varies is the outer operation that makes $\Psi$ a function of $v$. The first is the unilateral condition; the second changes the candidate.

#### Low-type concavity

The unfavorable type's problem is globally concave. Its residual $A_L$ is bounded, nonconstant, and nondecreasing in $x$, so it defines a finite positive Stieltjes measure $dA_L$, and integration by parts gives

$$
F_L'(s)=-\int f(x+s)\,dA_L(x)<0,
\qquad |F_L''(s)|\le-\frac1bF_L'(s)
\tag{A.16}\label{eq:paper-a-16}
$$

almost everywhere. The measure includes the entry jump as an atom, so no derivative of that jump is omitted. Therefore $U_L''(s)=2F_L'+sF_L''\le(2-s/b)F_L'(s)<0$ on $[0,1]$ whenever $b>1/2$, and $U_L'$ is strictly decreasing. A root of the unilateral marginal-profit equation is thus the unique global short magnitude against its candidate schedule, including against the endpoints.

#### Interval signs

Existence follows from an interval sign change. On a bracket $[v_-,v_+]$ that keeps $1/2<\tau<M_v$, the threshold $x^*(r,v)$ is continuous in $v$, and dominated convergence makes $\Psi(r,\cdot)$ continuous. Outward interval evaluation proves that $\Psi$ is positive at the left endpoint of each bracket in [Proposition 3](#result-proposition-3) and negative at the right endpoint, so the intermediate value theorem places an exact root inside. Writing $v_{j,-}$ and $v_{j,+}$ for the endpoints of the bracket at $r_j$, the enclosures completing the sign tests are

$$
\begin{aligned}
\Psi(r_{\mathrm a},v_{\mathrm a,-})&\ge0.000000000114>0,&
\Psi(r_{\mathrm a},v_{\mathrm a,+})&\le-0.000000000096<0,\\
\Psi(r_{\mathrm b},v_{\mathrm b,-})&\ge0.000000000123>0,&
\Psi(r_{\mathrm b},v_{\mathrm b,+})&\le-0.000000000121<0,\\
\Psi(r_{\mathrm c},v_{\mathrm c,-})&\ge0.000000000172>0,&
\Psi(r_{\mathrm c},v_{\mathrm c,+})&\le-0.000000000242<0.
\end{aligned}
\tag{A.17}\label{eq:paper-a-17}
$$

Throughout each bracket the entry threshold stays strictly between $-v$ and $1$. The sign change proves a root of $\Psi(r,\cdot)$ on the bracket, and the concavity result proves optimality at that root against its own schedule; no uniqueness of the root across candidate schedules is needed.

#### High-type cover over the whole bracket

A uniform derivative bound establishes optimality for the high-value investor. For any bounded residual $A_H\in[0,\Delta_T]$ the Laplace kernel satisfies $f''=(f-\delta_0)/b^2$ in the sense of distributions, so

$$
F_H''(s)=\frac{F_H(s)-A_H(s)}{b^2}\quad\text{a.e.},\qquad
|U_H''(s)|\le L_U:=\frac{2\Delta_T}{b}+\frac{\Delta_T}{b^2}.
\tag{A.18}\label{eq:paper-a-18}
$$

On the mesh $s_j=j/n$, interval arithmetic bounds $U_H'(s_j)$ uniformly over the whole root bracket $[v_-,v_+]$, not at a floating-point midpoint. The exact root is known only to lie inside the bracket, so the cover must hold for every candidate in it. Every untested magnitude lies within $1/(2n)$ of a mesh point, so

$$
\inf_{s\in[0,1]}U_H'(s)
\ge\min_j\underline{U_H'(s_j)}-\frac{L_U}{2n}>0.
\tag{A.19}\label{eq:paper-a-19}
$$

The certified global lower margins at the three strengths are 0.0000761777, 0.0027531948, and 0.0054921767. The favorable type therefore chooses its maximum purchase, and all wrong-signed trades have negative gross profit and are dominated by zero.

The integrals are elementary. Split each convolution at $-v$, $x^*$, $1$, and the deviation center. On the central region put $c=(1-v)/2$ and $t=e^{(x-c)/b}$, so that $\mu_v=t^2/(1+t^2)$. The primitives of $e^{x/b}(1-\mu_v)$, $e^{-x/b}(1-\mu_v)$, $e^{x/b}\mu_v$, and $e^{-x/b}\mu_v$ are respectively

$$
\begin{gathered}
b e^{c/b}\arctan t,\qquad
b e^{-c/b}(-t^{-1}-\arctan t),\\
b e^{c/b}(t-\arctan t),\qquad
b e^{-c/b}\arctan t.
\end{gathered}
\tag{A.20}\label{eq:paper-a-20}
$$

Constant-posterior tails integrate as exponentials without truncation. Endpoint ordering is certified. When the low trader is evaluated at $s=v$ the center coincides with $-v$ and is coalesced algebraically, and distinct uncertain endpoints are ordered by disjoint interval bounds. [Online Appendix B](online_appendix.md#oa-b) has the full antiderivatives and the endpoint-order rules.

#### No-trade coexistence and the proof of [Proposition 3](#result-proposition-3)

No trade is also an equilibrium at each certified strength because $\rho\Delta_T(r_j)/2\le k$ there, by [Proposition A.4](#result-proposition-a-4); the pooling margin is enclosed with the same outward arithmetic. Interval arithmetic applied to \eqref{eq:paper-a-20} encloses the root tests \eqref{eq:paper-a-17}, the derivative cover \eqref{eq:paper-a-19}, the pooling margin, and the entry probabilities \eqref{eq:paper-a-15} throughout each bracket. The entry enclosures in \eqref{eq:paper-13} are disjoint and ordered upward, which establishes the cross-economy ordering. This is a computer-assisted existence proof in the sense of [Online Appendix B](online_appendix.md#oa-b), with outward interval arithmetic on exact decimal inputs. It does not prove uniqueness of the informative profile, exclude mixed equilibria, or certify a continuous branch between the nodes. $\square$

### A.4 Distributional extensions and nonemptiness {#pa-calculations}

#### Logistic noise

Replace the Laplace density in \eqref{eq:paper-2} by

$$
f_{\mathrm{log}}(z)=\frac{1}{4b}\operatorname{sech}^{2}\left(\frac z{2b}\right)
=\frac{e^{-z/b}}{b(1+e^{-z/b})^2},\qquad b>1,
\tag{A.21}\label{eq:paper-a-21}
$$

whose log-density derivative is $-\tanh(z/2b)/b$, bounded in absolute value by $1/b$. Under full orders the posterior log odds are

$$
\log\frac{\mu_X}{1-\mu_X}
=2\log\cosh\left(\frac{x+1}{2b}\right)
-2\log\cosh\left(\frac{x-1}{2b}\right),
\tag{A.22}\label{eq:paper-a-22}
$$

with derivative $[\tanh((x+1)/2b)-\tanh((x-1)/2b)]/b>0$ and limits $-2/b$ and $2/b$. The posterior therefore spans the open interval $(m,M)$ and crosses every interior threshold with positive probability, but attains neither bound. With $A=e^{1/b}$ and $w=\sqrt{\tau/(1-\tau)}$, the square root of the likelihood ratio is $(Ay+1)/(y+A)$ in $y=e^{x/b}$, and solving $w=(Ay+1)/(y+A)$ gives the threshold and the conditional tail probabilities

$$
\begin{aligned}
x^*_{\mathrm{log}}&=b\log\frac{Aw-1}{A-w},\\
\alpha_H^{\mathrm{log}}&=\frac1{1+e^{(x^*_{\mathrm{log}}-1)/b}},\qquad
\alpha_L^{\mathrm{log}}=\frac1{1+e^{(x^*_{\mathrm{log}}+1)/b}},
\end{aligned}
\tag{A.23}\label{eq:paper-a-23}
$$

valid for $m<\tau<M$, with $\mathsf E=\rho+(1-\rho)(\alpha_H+\alpha_L)/2$.

[**Proposition A.5 (logistic noise; analytical).**]{#result-proposition-a-5} *Replace Laplace noise by logistic noise with density \eqref{eq:paper-a-21}. Under conditions \eqref{eq:paper-a1} to \eqref{eq:paper-a3}, the unique trading outcomes and the entry and ownership comparisons of [Proposition 2](#result-proposition-2) remain valid, with the threshold and favorable-flow probabilities given by \eqref{eq:paper-a-23}.*

The bound $|f'|\le f/b$ is all that the posterior bounds, the translation formula \eqref{eq:paper-a-5}, and the derivative bound \eqref{eq:paper-a-6} use, and $f_{\mathrm{log}}$ is positive, smooth, and in $W^{1,1}$. Steps 1 to 5 of the proof of [Proposition 2](#result-proposition-2) therefore go through unchanged. Under full orders \eqref{eq:paper-a-22} is strictly increasing, and \eqref{eq:paper-a2} places $\tau$ strictly inside $(m,M)$, so the threshold \eqref{eq:paper-a-23} is finite and both tail probabilities are positive; the information ordering argument is unchanged. $\square$

Laplace and logistic noise are compared at a common scale parameter $b$. They do not have a common variance, and neither experiment Blackwell dominates the other in general; the comparison concerns where posterior mass sits relative to the common bounds $m,M$.

#### Atomless preparation costs

For atomless low- and high-cost component distributions with probabilities $\rho$ and $1-\rho$, supported within $[c_L-\varepsilon_C,c_L+\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$, the sufficient support restrictions are

$$
\begin{gathered}
c_L-\varepsilon_C\ge0,\qquad c_L+\varepsilon_C<B_{r_1}(m),\\
B_{r_0}(1/2)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{r_1}(M),
\end{gathered}
\tag{A.24}\label{eq:paper-a-24}
$$

together with \eqref{eq:paper-a3}.

[**Proposition A.6 (atomless preparation costs; analytical).**]{#result-proposition-a-6} *Replace the cost atoms by atomless distributions satisfying \eqref{eq:paper-a-24} and retain \eqref{eq:paper-a3}. The unique trading outcomes and the entry and ownership reversal in parts (i) and (ii) of [Proposition 2](#result-proposition-2) hold under either noise law.*

Let $H_C$ be the mixed cost CDF; the entry rule is $e(\mu)=H_C(B_r(\mu))$, continuous and nondecreasing. The first line of \eqref{eq:paper-a-24} makes every low-cost realization prepare at every feasible belief in both economies, so $e\ge\rho$ and the residual bounds in \eqref{eq:paper-11} are unchanged. The price increment \eqref{eq:paper-a-3} stays strictly positive because $H_C$ is nondecreasing, so the inversion and the global trading bounds apply. At the weak prior, $e(1/2)=\rho$ by the second line of \eqref{eq:paper-a-24}. In the strong economy, beliefs close enough to $M$ satisfy $B_r(\mu)>c_H+\varepsilon_C$, an event of positive probability under either noise law, and there $e=1$. The proof needs an atomless distribution, not a density. [Online Appendix A.6](online_appendix.md#oa-a-extensions) has the details. $\square$

#### Nonemptiness for every value gap

The parameter region of [Proposition 2](#result-proposition-2) does not require a large gap between $h$ and $\ell$. At the continuous limit $r=\ell$,

$$
g_H-g_L=h-\ell>0,\qquad
B_\ell(M)-B_\ell(1/2)=(M-1/2)(h-\ell)>0.
\tag{A.25}\label{eq:paper-a-25}
$$

Choose $r_1\in(\ell,h)$ close enough to $\ell$ that $B_{r_1}(M)>B_\ell(1/2)$; since $B_r(1/2)$ decreases in $r$, every $r_0\in(\ell,r_1)$ then satisfies $B_{r_0}(1/2)<B_{r_1}(M)$. Choose $r_0$ close enough to $\ell$ that $\Delta_T(r_0)<(1-1/b)\rho m\Delta_T(r_1)$, which is possible because $\Delta_T(r)\to0$ as $r\to\ell$. Select $k$ strictly inside that interval, $c_H$ strictly between the two profit bounds, and $c_L$ strictly between zero and $B_{r_1}(m)>0$; then $c_L<c_H$ because $B_{r_1}(m)<B_{r_0}(1/2)$. All inequalities have strict slack and persist under small perturbations. This is a mathematical nonemptiness construction, not a statement about effect size at every value ratio.

### A.5 Complementary private information {#pa-signals}

#### Definitions

The investor observes a signal $T\in\{+,-\}$ and the buyer a signal $Y\in\{+,-\}$, conditionally independent given quality, with accuracies

$$
\begin{aligned}
\Pr(T=+\mid H)&=\Pr(T=-\mid L)=a,\\
\Pr(Y=+\mid H)&=\Pr(Y=-\mid L)=d,
\qquad a,d\in(1/2,1).
\end{aligned}
\tag{A.26}\label{eq:paper-a-26}
$$

Orders are contingent on $T$: $a_\pm(x)=\int f(x-q)\,d\sigma_\pm(q)$ and $\lambda_X=a_+/(a_++a_-)=\Pr(T=+\mid X)$. Public beliefs about quality, their bounds, and the buyer's combined posteriors are

$$
\begin{aligned}
\mu_X&=(1-a)+(2a-1)\lambda_X,\\
\mu_-&=(1-a)+(2a-1)m,\qquad \mu_+=(1-a)+(2a-1)M,\\
\phi_+(\mu)&=\frac{d\mu}{d\mu+(1-d)(1-\mu)},\qquad
\phi_-(\mu)=\frac{(1-d)\mu}{(1-d)\mu+d(1-\mu)}.
\end{aligned}
\tag{A.27}\label{eq:paper-a-27}
$$

Set $w_H=t_H-t_0$, $w_L=t_L-t_0$, and $I_y=\mathbf1\{B_r(\phi_y(\mu))\ge c_H\}$ for $y\in\{+,-\}$. State-conditioned entry rates and the coefficient on public beliefs are

$$
\begin{aligned}
e_H&=\rho+(1-\rho)[dI_++(1-d)I_-],\\
e_L&=\rho+(1-\rho)[(1-d)I_++dI_-],\\
D&=e_Hw_H-e_Lw_L.
\end{aligned}
\tag{A.28}\label{eq:paper-a-28}
$$

Entry is state-dependent even conditional on the price, so the benchmark's common preparation rate is not reused here; $D$ carries the two rates separately.

[**Proposition A.7 (complementary private signals; analytical).**]{#result-proposition-a-7} *In the complementary-signal economy, choose $0<p<\ell<r_0<r_1<h$ and suppose*

$$
\begin{gathered}
c_L<B_{r_1}(\phi_-(\mu_-)),\qquad
B_{r_0}(d)<c_H<B_{r_1}(\phi_+(\mu_+)),\\
(2a-1)\{\Delta_T(r_0)+(1-\rho)(2d-1)w_H(r_0)\}<k
<\left(1-\frac1b\right)m(2a-1)\rho\Delta_T(r_1).
\end{gathered}
\tag{A.29}\label{eq:paper-a-29}
$$

*The weak economy has unique zero informed orders and entry $\rho$. The strong economy has unique orders $q(T=+)=1$ and $q(T=-)=-1$, and entry strictly exceeds $\rho$. The conclusions permit arbitrary mixed signal-contingent orders and every continuous unilateral deviation, and do not require $a\ge d$.*

#### Proof

*Step 1: joint beliefs.* Flow depends on quality only through $T$, and $Y$ is drawn from quality alone, so

$$
\Theta\perp X\mid T,\qquad Y\perp X\mid\Theta .
\tag{A.30}\label{eq:paper-a-30}
$$

The first relation gives $\Pr(H\mid X)=a\lambda_X+(1-a)(1-\lambda_X)$, which is the first line of \eqref{eq:paper-a-27}. [Proposition A.1](#result-proposition-a-1) applied to the signal-contingent mixtures gives $\lambda_X\in[m,M]$, hence $\mu_X\in[\mu_-,\mu_+]$, and the price posterior $\mu_P=\mathbb E[\mu_X\mid P]$ lies in the same interval. The second relation survives any measurable function of $X$, so Bayes' rule at the price gives

$$
\Pr(H\mid P,Y=y)=\phi_y(\mu_P).
\tag{A.31}\label{eq:paper-a-31}
$$

Both maps $\phi_y$ are continuous and strictly increasing, with $\phi_+>\phi_-$. The lowest joint posterior is $\phi_-(\mu_-)$, so the first condition in \eqref{eq:paper-a-29}, with $B_{r_0}\ge B_{r_1}$, makes low-cost preparation optimal at every reachable price in both economies under any candidate equilibrium.

*Step 2: state-conditioned entry and price inversion.* Because the law of $Y$ given quality does not depend on $X$, true-state entry conditional on the price is \eqref{eq:paper-a-28} with $I_y=I_y(P)$. Since $I_+\ge I_-$,

$$
e_H-e_L=(1-\rho)(2d-1)(I_+-I_-)\ge0,\qquad e_H\ge e_L\ge\rho,
\tag{A.32}\label{eq:paper-a-32}
$$

and, using $w_H-w_L=\Delta_T$ and $w_L>0$,

$$
D=e_L\Delta_T+(e_H-e_L)w_H\ \in\ \big[\rho\Delta_T,\ \Delta_T+(1-\rho)(2d-1)w_H\big],
\qquad D\ge\rho\Delta_T>0.
\tag{A.33}\label{eq:paper-a-33}
$$

Conditional competitive pricing is

$$
P=t_0+e_L(P)w_L+\mu_XD(P),
\qquad
\mu_X=\frac{P-t_0-e_L(P)w_L}{D(P)}.
\tag{A.34}\label{eq:paper-a-34}
$$

Both entry rates are functions of the price, so the positive coefficient $D(P)$ makes $\mu_X$ a Borel function of $P$, the tower property gives $\mu_P=\mu_X$, and the affine map in \eqref{eq:paper-a-27} also reveals $\lambda_X$. For construction, write $P(\mu)=t_0+\mu e_H(\mu)w_H+(1-\mu)e_L(\mu)w_L$; for $\mu_2>\mu_1$ its increment is $(\mu_2-\mu_1)D(\mu_1)+\mu_2[e_H(\mu_2)-e_H(\mu_1)]w_H+(1-\mu_2)[e_L(\mu_2)-e_L(\mu_1)]w_L>0$, so the price is strictly increasing even when both indicators jump at once, and the measurable inverse of [Proposition A.2](#result-proposition-a-2) applies.

*Step 3: residual bounds.* Conditional on $T=+$ the investor assigns quality probability $a$, and conditional on $T=-$ it assigns $1-a$; a unilateral order adds no quality information beyond the signal. Its expected terminal payoff at flow $x$ is $t_0+e_L(P(x))w_L+aD(P(x))$ after $T=+$, and the same expression with $1-a$ after $T=-$. Subtracting \eqref{eq:paper-a-34} and using \eqref{eq:paper-a-27},

$$
A_+=(2a-1)(1-\lambda_X)D,\qquad A_-=(2a-1)\lambda_XD,
\tag{A.35}\label{eq:paper-a-35}
$$

and \eqref{eq:paper-a-33} with $\lambda_X\in[m,M]$ gives

$$
m(2a-1)\rho\Delta_T\le A_+,A_-
\le(2a-1)[\Delta_T+(1-\rho)(2d-1)w_H]=:\overline A.
\tag{A.36}\label{eq:paper-a-36}
$$

*Step 4: exclusion, global inequality, construction, and additional entry.* In the weak economy the lower bound on $k$ in \eqref{eq:paper-a-29} makes any correctly signed order of magnitude $s>0$ earn at most $s(\overline A(r_0)-k)<0$; wrong signs have negative gross payoff. Zero is therefore necessary under every candidate schedule. With zero orders the public posterior is $1/2$, the buyer's favorable posterior is $\phi_+(1/2)=d$, and $B_{r_0}(d)<c_H$ excludes expensive preparation after either private signal; entry is $\rho$ and constant pricing constructs the equilibrium. In the strong economy the translation formula \eqref{eq:paper-a-5} applies to either bounded residual, and the lower bound in \eqref{eq:paper-a-36} with the upper bound on $k$ in \eqref{eq:paper-a-29} gives

$$
U'(s)\ge\left(1-\frac1b\right)m(2a-1)\rho\Delta_T(r_1)-k>0
\tag{A.37}\label{eq:paper-a-37}
$$

on the whole order interval, so the unique trading profile is full correctly signed orders by signal. Bayes' rule, the price in Step 2, and optimal preparation using \eqref{eq:paper-a-31} construct the equilibrium. Under full orders $\lambda_X=M$ on the positive-probability tail $x\ge1$, where $\mu_X=\mu_+$; the condition $c_H<B_{r_1}(\phi_+(\mu_+))$ then gives $I_+=1$, and $\Pr(Y=+\mid\Theta)>0$ in both states. Additional preparation therefore has positive probability and entry strictly exceeds $\rho$. [Online Appendix A.7](online_appendix.md#oa-a-signals) gives the complete conditional laws and the closed-form entry probabilities. $\square$

### A.6 Bargaining and access to prices {#pa-welfare}

#### The verifiable-value institution

The institution of [Section 6.2](#sec-the-payment-rule) has four elements: buyer values are verifiable after diligence; a sale to the runner-up at its value is an enforceable fallback, accepted at zero surplus; without a challenger the reserve is zero and the seller bargains against a fallback of zero; and the seller's Nash bargaining weight is $\eta$.

[**Proposition A.8 (bargaining; analytical).**]{#result-proposition-a-8} *In the verifiable-value institution, let $R$ have any distribution supported on $[0,R_{\max}]$ with $0<\ell<R_{\max}<h$. For $0\le\eta<1$ the institution generates \eqref{eq:paper-14}. A first-order stochastic strengthening of the incumbent weakly reduces challenger profits. It weakly increases the target's information spread for $\eta<1/2$, leaves that spread unchanged at $\eta=1/2$, and weakly decreases it for $\eta>1/2$. Strictness follows from a positive integral change in the corresponding payoff function.*

With fallback $z$ and winning value $V>z$, the transfer solves

$$
\max_{P\in[z,V]}(P-z)^\eta(V-P)^{1-\eta},
\tag{A.38}\label{eq:paper-a-38}
$$

whose log objective is strictly concave, giving $P=z+\eta(V-z)=(1-\eta)z+\eta V$; at $V=z$ the feasible set is the point $z$, and at $\eta=0$ I use the continuous limit $z$. Without a challenger the same rule with fallback zero pays the seller $\eta R$. The highest-value buyer receives the target and a challenger wins only if $\theta\ge R$, keeping $(1-\eta)(\theta-R)$, which gives $G_{\theta,\eta}$ in \eqref{eq:paper-14}. For $R\le\ell$ the high and low target payments are $(1-\eta)R+\eta h$ and $(1-\eta)R+\eta\ell$; for $R>\ell$ they are $(1-\eta)R+\eta h$ and $(1-\eta)\ell+\eta R$. The state-by-state difference is $\eta(h-\ell)+(1-2\eta)(R-\ell)_+$, whose expectation is $\Delta_\eta$. First-order stochastic dominance applied to the increasing function $(R-\ell)_+$ and the decreasing function $(\theta-R)_+$ gives the signs, and the sign of $1-2\eta$ places the boundary at one half. That boundary is a property of this institution's payment rule; the proposition does not solve a private-value first-price auction or a bargaining-and-trading equilibrium. [Online Appendix A.8](online_appendix.md#oa-a-bargaining) treats the endpoints. $\square$

#### Access to prices

Without a challenger, ownership value is $W_0(R)=R\mathbf1\{R\ge p\}$. With challenger value $\theta>p$ it is $W_\theta(R)=\max\{R,\theta\}$. Splitting at $R=p$ and $R=\theta$,

$$
W_\theta(R)-W_0(R)
=(\theta-\max\{p,R\})_++p\mathbf1\{R<p\}.
\tag{A.39}\label{eq:paper-a-39}
$$

[**Proposition A.9 (access to prices; analytical).**]{#result-proposition-a-9} *Hold $r=r_1$ and all other primitives fixed under the conditions of [Proposition 2](#result-proposition-2). Compare the feedback equilibrium with the equilibrium in which the challenger cannot observe the target price, reoptimizing trading and pricing in both. Access to prices strictly increases expected target proceeds and acquisition surplus net of preparation costs. The comparison also holds under Propositions A.5 and A.6.*

Couple the two economies on the same realization of $(\Theta,R,C,Z)$. In the price-hidden game the buyer's posterior stays at the prior, so entry is $\rho$ by \eqref{eq:paper-a2}; the residuals are then $\rho\Delta_T(1-\mu_X)$ and $\rho\Delta_T\mu_X$, and the bound \eqref{eq:paper-a-6} still applies, so orders are full in both games. The order-flow experiment and the realized trading cost therefore coincide, and any resource interpretation of that cost cancels. Price access changes only whether a high-cost challenger prepares.

Conditional on the price information and preparation cost that induce an additional preparation decision, $R$ retains its independent uniform law, so by \eqref{eq:paper-a-39} the decision contributes expected allocation value net of cost

$$
B_r(\mu_X)-C+p\Pr(R<p)=B_r(\mu_X)-C+\frac{p^2}{r}.
\tag{A.40}\label{eq:paper-a-40}
$$

Optimal preparation requires $B_r(\mu_X)\ge C$, so each additional preparation decision contributes at least $p^2/r$ in conditional expectation, given price information and preparation cost. A realized low-value preparation may cost more than the allocation value it creates; the inequality is conditional, not realized. Low-cost preparation is unchanged in the matched comparison. Averaging over the positive-probability event of additional preparation, for cost atoms,

$$
\begin{aligned}
\Delta\mathcal W&=(1-\rho)\,\mathbb E\left[
\left(B_r(\mu_X)-c_H+\frac{p^2}{r}\right)\mathbf1\{\mu_X\ge\tau\}\right]>0,\\
\Delta\mathcal R_T&=\frac{1-\rho}{2}
\left[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\right]>0,
\end{aligned}
\tag{A.41}\label{eq:paper-a-41}
$$

where the second line averages $t_\theta-t_0>0$ over each state's additional-entry probability. Transfers among bidders, shareholders, market makers, and noise traders cancel and are not allocation surplus. Under [Proposition A.6](#result-proposition-a-6) the same argument integrates the high-cost component over $\{c\le B_r(\mu_X)\}$; under [Proposition A.5](#result-proposition-a-5) the tail probabilities are \eqref{eq:paper-a-23}. The external dividend of [Section 6.1](#sec-access-to-prices) shifts the price by a constant and leaves $V_T-P$, trading, and entry unchanged. [Online Appendix A.9](online_appendix.md#oa-a-welfare) states the coupling and the atomless-cost integral. $\square$

### A.7 Seller continuation {#pa-design}

#### Payoffs over the reserve domain

For a realized challenger value $v$ and reserve $p\in[0,h]$, the sale rule gives

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
\tag{A.42}\label{eq:paper-a-42}
$$

For the uniform incumbent the closed forms depend on where the reserve sits. For $p\le\ell$, \eqref{eq:paper-4} applies. For $\ell<p\le r$, the low-value challenger cannot meet the reserve: $t_L=t_0=p(1-p/r)$, $g_L=0$, $t_H=r/2+p^2/(2r)$, and $g_H=h-t_H$. For $r<p\le h$, the incumbent also fails the reserve: $t_0=t_L=g_L=0$, $t_H=p$, and $g_H=h-p$. Above $h$ there is no sale. A bid equal to the reserve is admissible. At $p=\ell$ the low-value challenger can still buy when the incumbent fails the reserve, whereas immediately above $\ell$ it cannot; target proceeds therefore jump at that exclusion boundary. The applicable formulas agree at $p=r$, and at $p=h$ the high-value challenger remains admissible at zero acquisition rent. For atomless acquisition values, integrate \eqref{eq:paper-a-42} over each conditional value distribution, including when the reserve cuts through a value band. A payoff function written for $p<\ell$ must not be applied outside that support.

#### The continuation object

Let $\mathcal E(p,r)$ denote the set of continuation equilibria after reserve $p$. A continuation is the complete object

$$
\sigma=(\sigma_H,\sigma_L;\ P(\cdot);\ \mu_P;\ \text{preparation rule})\in\mathcal E(p,r):
\tag{A.43}\label{eq:paper-a-43}
$$

conditional order distributions, the price mapping on flow, the buyer's beliefs at every realized price including price atoms, and the preparation rule at every price and cost. Two continuations with the same orders but different price mappings are different elements of $\mathcal E(p,r)$; identity is by the whole object, not by orders alone. Write $e_H(p,r;\sigma)$ and $e_L(p,r;\sigma)$ for state-conditioned entry. Expected seller revenue and the seller's problem are

$$
\begin{aligned}
\mathcal R_T(p,r;\sigma)
&=t_0(p,r)+\frac12\sum_{\theta\in\{H,L\}}e_\theta(p,r;\sigma)
[t_\theta(p,r)-t_0(p,r)],\\
p^*&\in\arg\max_{p\in[0,h]}\mathcal R_T(p,r;\sigma^*(p)).
\end{aligned}
\tag{A.44}\label{eq:paper-a-44}
$$

for a selection $\sigma^*(p)\in\mathcal E(p,r)$ specified after every reserve, including reserves the seller does not choose. Existence of a feasible selection and attainment of the maximum require separate arguments; the optimistic and pessimistic envelopes of $\mathcal E(p,r)$ are not the seller's objective. In the atomless-value extension the reserve domain extends to $h+\varepsilon_V$.

#### Price pooling at fixed orders

On the benchmark support, $c_L<B_r(m)$ gives entry at least $\rho$ at every price, and [Proposition A.2](#result-proposition-a-2) then ties the price experiment to the orders, so fixed orders imply a fixed price experiment. Outside that support entry can vanish on a set of flows, those flows can pool at the no-entry price, and the pooled posterior can support more than one price mapping at the same orders. The following example, in the reserve game itself, shows this and is the regression that the numerical continuation record must reproduce. The phenomenon itself is not new; @DowGoldsteinGuembel2017 already distinguish continuations with different pooling regions.

Take the benchmark primitives with $r=r_0$ and reserve $p=7$, so $p>r>\ell$ and the auction objects are $t_0=t_L=g_L=0$, $t_H=7$, $g_H=3$, and $\Delta_T=7$. Fix full orders $(q_H,q_L)=(1,-1)$ and $b=2$, so that $f(z)=\tfrac14e^{-|z|/2}$ and $\mu_X$ is \eqref{eq:paper-a-8} with $b=2$; on $(-1,1)$ it equals $\operatorname{logistic}(x)$. Let $F_Z$ be the noise CDF, $F_Z(z)=\tfrac12e^{z/2}$ for $z\le0$ and $1-\tfrac12e^{-z/2}$ for $z>0$, and $S_Z=1-F_Z$ its survival function. For each cutoff $c\in[-\log2,0]$ define the price rule

$$
P_c(x)=
\begin{cases}
0,&x<c,\\
\tfrac74\mu_X(x),&x\ge c,
\end{cases}
\tag{A.45}\label{eq:paper-a-45}
$$

with no preparation at price zero, low-cost preparation at every positive price, and no high-cost preparation.

[**Proposition A.10 (price pooling at fixed orders; analytical).**]{#result-proposition-a-10} *For every $c\in[-\log2,0]$, the price rule \eqref{eq:paper-a-45} with the stated preparation policy and full orders $(1,-1)$ is a continuation equilibrium in $\mathcal E(7,r_0)$. The orders are the same in all members of the family; prices, beliefs, and entry differ.*

*Buyer at price zero.* The zero price is the pool $\{X<c\}$. Conditioning on the whole pool, not on the raw flow,

$$
\bar\mu_c=\Pr(H\mid X<c)=\frac{F_Z(c-1)}{F_Z(c-1)+F_Z(c+1)}.
\tag{A.46}\label{eq:paper-a-46}
$$

By the monotone likelihood ratio, $\bar\mu_c$ is nondecreasing in $c$, so for the whole family $\bar\mu_c\le\bar\mu_0=\tfrac12e^{-1/2}<\tfrac13$. Gross profit at the pool is $3\bar\mu_c<1=c_L$, so nonpreparation is strictly optimal at price zero even for the low-cost type. For $c=0$, raw flow posteriors on $(-\log2,0)$ exceed $1/3$ and would justify low-cost preparation if those flows were observed separately; they are not, and the pooled posterior governs.

*Buyer at positive prices.* On $x\ge c$ the price $\tfrac74\mu_X$ is strictly increasing in the posterior on $(-1,1)$, with the plateau $x\ge1$ forming an actual atom at $\tfrac74M$; it never collides with zero. The buyer recovers $\mu_X$ and $\mu_X(x)\ge\mu_X(-\log2)=\tfrac13$, so $3\mu_X\ge c_L$ and low-cost preparation is optimal under the tie rule. High-cost preparation is impossible because gross profit is at most $3<6=c_H$.

*Conditional pricing.* For $x<c$ no entrant is prepared and neither the incumbent nor a low-value challenger meets the reserve, so $\mathbb E[V_T\mid X=x]=0$. For $x\ge c$ preparation occurs with probability $\rho$ and a sale at $7$ occurs only in state $H$, so $\mathbb E[V_T\mid X=x]=\rho\,7\,\mu_X(x)=\tfrac74\mu_X(x)$. Competitive pricing holds on both regions; the unconditional average is not the test.

*Global investor bound.* Against each member of the family the residuals are

$$
A_H(x)=\rho p[1-\mu_X(x)]\mathbf1\{x\ge c\},\qquad
A_L(x)=\rho p\,\mu_X(x)\mathbf1\{x\ge c\},
\tag{A.47}\label{eq:paper-a-47}
$$

zero in the pool and nonnegative elsewhere, so wrong-signed orders are dominated by zero. Let $J_c=F_H(1)=F_L(1)$ as in \eqref{eq:paper-a-7}. Every $c\le0$ leaves the tail $x\ge1$ active, on which $1-\mu_X=m=(1+e)^{-1}>\tfrac14$ and whose probability in state $H$ is $\tfrac12$. Hence

$$
J_c\ge\frac{\rho p\,m}{2}>\frac{7}{32},
\qquad
U_\theta'(s)\ge\left(1-\frac1b\right)J_c-k>\frac{7}{64}-\frac{1}{50}=\frac{143}{1600}>0
\tag{A.48}\label{eq:paper-a-48}
$$

for every $s\in[0,1]$ and both types, using the ratio bound $F_\theta(s)\ge e^{-(1-s)/b}J_c$ and the derivative bound of Appendix A.2. Full correctly signed orders are globally optimal against every price rule in the family. $\square$

The common rational lower bound in \eqref{eq:paper-a-48} is the proof; a positive derivative found on a grid only checks its implementation. The proposition establishes analytical existence for the whole cutoff family. It does not establish uniqueness of that family within $\mathcal E(7,r_0)$, and it does not arise on the benchmark support, where the positive floor $c_L<B_r(m)$ rules out pooling distinct raw posteriors at one price. Constant-posterior tail atoms remain possible. The outcome measures are

$$
\Pr(P=0)=\frac{F_Z(c-1)+F_Z(c+1)}{2},\qquad
\mathsf E_c=\frac\rho2\{S_Z(c-1)+S_Z(c+1)\},\qquad
\mathcal R_{T,c}=\frac{\rho p}{2}S_Z(c-1),
\tag{A.49}\label{eq:paper-a-49}
$$

with sale probability $\tfrac\rho2S_Z(c-1)$ and probability zero of two admissible bidders. At the endpoints $c=-\log2$ and $c=0$ the pooled posteriors are 0.272979 and 0.303265, preparation probabilities are 0.151805 and 0.125000, and expected seller revenues are 0.687364 and 0.609643. The less informative price rule suppresses preparation at flows that would justify it if observed separately, and both preparation and revenue fall as the cutoff rises.

#### Exact reserve events

Two reserves at which a participation inequality holds with equality are analytically supported event candidates. They are not interior points of a strict-inequality region, and the same continuation need not be supported on both sides of either event.

*Weak-incumbent floor.* When the reserve exceeds incumbent support and excludes the low class, $g_H=h-p$, $g_L=0$, $t_H=p$, and $t_0=t_L=0$. The low-cost floor $B_p(m)=m(h-p)=c_L$ holds with equality at

$$
p_L=h-\frac{c_L}{m}.
\tag{A.50}\label{eq:paper-a-50}
$$

At $r=r_0$ the benchmark has $r_0<p_L<h$. Every price posterior is at least $m$ under any strategy, so $B(\mu)\ge c_L$ at every price and the tie rule admits the low-cost type there; under full orders the equality holds on the positive-probability lower plateau $x\le-1$. Since $B(M)=Mc_L/m<c_H$, the high-cost type stays out. Entry is therefore $\rho$ at every price, no pool combines distinct raw posteriors, and the inversion and global bound of [Appendix A.2](#pa-proofs) apply with $e\ge\rho$ under equality, giving unique full orders. Then $\mathsf E=\rho$, the sale probability is $\rho/2$, and $\mathcal R_T=\rho p_L/2$. Preparation here never produces two admissible bidders: the incumbent is excluded.

*Strong-incumbent expensive entry.* With the low class excluded and $\ell<p<r$, $g_H=h-r/2-p^2/(2r)$ and $g_L=0$. The upper-posterior entry event $Mg_H=c_H$ occurs at

$$
p_H=\sqrt{2r\left(h-\frac{c_H}{M}\right)-r^2},
\tag{A.51}\label{eq:paper-a-51}
$$

which at $r=r_1$ lies in $(\ell,r_1)$. There $\tau=M$ and $x^*=1$, so $\alpha_H=\tfrac12$ and $\alpha_L=\tfrac12e^{-2/b}$: the plateau has positive probability and entry at indifference admits the expensive type on it. The strictly positive low-cost floor $mg_H=mc_H/M>c_L$ and the global full-order bound are checked separately from this equality. Both events are evaluated from their defining identities, not from a rounded reserve and a floating-point comparison.

#### Outcome measures

Let $I$ indicate that the challenger pays for preparation and $V$ its realized value. Define

$$
\begin{aligned}
\mathsf E&=\Pr(I=1),\qquad \mathsf A=\Pr(I=1,V\ge p),\\
\mathsf S&=\Pr(R\ge p\ \text{or}\ [I=1,V\ge p]),\\
\mathsf C_2&=\Pr(R\ge p,I=1,V\ge p),
\end{aligned}
\tag{A.52}\label{eq:paper-a-52}
$$

the preparation, admissible-challenger, sale, and two-admissible-bidder probabilities. Inclusion and exclusion give $\mathsf S=\Pr(R\ge p)+\mathsf A-\mathsf C_2$, and $0\le\mathsf C_2\le\mathsf A\le\mathsf E\le1$. Preparation is not the same event as two admissible bidders. At the weak-incumbent floor event, $\mathsf C_2=0$ while $\mathsf E>0$. At the strong-incumbent ceiling event, $p_H<r_1$ and $\mathsf C_2=(1-p_H/r_1)e_H/2>0$, because a prepared high-value challenger and the incumbent can both be admissible. Outside the benchmark support, high-value ownership is computed from the actual allocation event rather than as $e_H/2$.

#### Selected continuation and local regularity

On a differentiable continuation branch with atomless preparation costs and $0<p<\ell$, let $\mathsf E=(e_H+e_L)/2$. Differentiating \eqref{eq:paper-a-44} gives

$$
\frac{d\mathcal R_T}{dp}
=(1-\mathsf E)\left(1-\frac{2p}{r}\right)+\mathsf E\frac p r
+\frac12\sum_\theta\frac{de_\theta}{dp}(t_\theta-t_0).
\tag{A.53}\label{eq:paper-a-53}
$$

The first two terms hold entry fixed; the last accounts for participation. If $H_C$ is the cost CDF with density $h_C$, and $\mu_\theta(z;p)$ is the posterior reached in state $\theta$ at noise realization $z$, then

$$
\frac{de_\theta}{dp}
=\int f(z)\,h_C(B_{p,r}(\mu_\theta))
\left[-\frac p r+(g_H-g_L)\frac{d\mu_\theta(z;p)}{dp}\right]dz.
\tag{A.54}\label{eq:paper-a-54}
$$

The term $-p/r$ is the direct effect on acquisition profit; the posterior derivative is the change in information generated by trading, which vanishes locally when orders stay at their bounds and can be nonzero when they adjust. The decomposition requires a continuously differentiable pure branch, a continuously differentiable cost CDF, and an integrable dominating function for the integrand in \eqref{eq:paper-a-54}; [Online Appendix A.10](online_appendix.md#oa-a-design) states these conditions. There is no general sign restriction on the information term. At an atomic preparation threshold, at a price pool, or on a nonregular continuation, the level objective \eqref{eq:paper-a-44} with the complete conditional laws is the correct object.

The reserve sweep in [Online Appendix C.6](online_appendix.md#oa-c-reserve) records continuations found under the declared searches, with continuation identity taken from the full object \eqref{eq:paper-a-43} and with the event reserves \eqref{eq:paper-a-50} and \eqref{eq:paper-a-51} included. It does not prove existence at unresolved reserves, exhaust $\mathcal E(p,r)$, or establish a global seller optimum. Characterizing seller-optimal terms, their commitment timing, and whether they preserve the entry reversal remains open.

### A.8 Numerical parameter declarations {#pa-parameters}

The benchmark parameter vector is

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.25,1,6,2,0.02),\\
(r_0,r_1,r_2)&=(1.2,3,3.6).
\end{aligned}
\tag{A.55}\label{eq:paper-a-55}
$$

The moderate-value vector is

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(2,1,0.5,0.25,0.3,0.89,2,0.002),\\
(r_0,r_1)&=(1.05,1.5).
\end{aligned}
\tag{A.56}\label{eq:paper-a-56}
$$

For complementary signals I use

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.85,1,7.14,2,0.015),\\
(r_0,r_1,a,d)
&=(1.1,2.3,0.70,0.75).
\end{aligned}
\tag{A.57}\label{eq:paper-a-57}
$$

The atomless-cost half-width is $\varepsilon_C=$ 0.1 and the atomless-value half-width is $\varepsilon_V=$ 0.05. These are separate experiments.

The price-pool family of [Proposition A.10](#result-proposition-a-10) uses the benchmark vector \eqref{eq:paper-a-55} with $r=r_0$, reserve $p=$ 7, full orders $(1,-1)$, entry at indifference, and admissible bids at the reserve. The declared cutoffs are the endpoints $c\in\{-\log2,0\}$ and the grid $c_j=-\log2\,(1-j/16)$ for $j=0,\dots,16$; the negative controls $c=-1$ and $c=1$ are declared as expected failures. The exact reserve events are $p_L=h-c_L/m$ at $r=r_0$ and $p_H=\sqrt{2r_1(h-c_H/M)-r_1^2}$ at $r=r_1$, evaluated from these identities under the benchmark vector, with the tie rule of Section 2. [Online Appendix C](online_appendix.md#oa-c) defines the exact input values, the derived quantities, their formatting, and the acceptance criteria behind every number reported in the text.
