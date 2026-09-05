---
documentclass: article
fontsize: 12pt
geometry: margin=1in
linestretch: 2
fontfamily: newtxtext
colorlinks: true
linkcolor: paperlink
citecolor: paperlink
urlcolor: paperlink
header-includes:
  - '\usepackage{amsmath,amssymb,amsthm}'
  - '\usepackage{newtxmath}'
  - '\usepackage{booktabs}'
  - '\usepackage{threeparttable}'
  - '\usepackage{graphicx}'
  - '\usepackage{float}'
  - '\usepackage{setspace}'
  - '\usepackage{etoolbox}'
  - '\usepackage[font=small,labelfont=bf,labelsep=period]{caption}'
  - '\usepackage[section]{placeins}'
  - '\definecolor{paperlink}{RGB}{31,59,115}'
  - '\allowdisplaybreaks'
  - '\setlength{\parskip}{0pt}'
  - '\setlength{\parindent}{1.5em}'
  - '\AtBeginEnvironment{CSLReferences}{\interlinepenalty=10000}'
  - '\AfterEndEnvironment{abstract}{\clearpage}'
title: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders"
author: "Austin Li"
date: ""
bibliography: references.bib
link-citations: true
abstract: |
  A stronger incumbent bidder can attract a challenger by making the target's stock price more informative. I study a takeover auction in which a prospective buyer observes the price before paying to learn its acquisition value. Stronger competition reduces the buyer's acquisition profit at every belief but increases the sensitivity of target proceeds to its value. This raises informed investors' trading incentives. On an open set of parameters, a stronger incumbent changes the unique equilibrium from uninformative to informative prices, increasing entry and the probability of acquisition by a high-value challenger. Holding price information fixed restores deterrence. At intermediate strengths, computer-assisted proofs establish informative equilibria that coexist with no trade. The reversal also arises when the buyer's private signal is more accurate than the investor's. Access to prices increases acquisition surplus net of preparation costs, and an alternative bargaining institution identifies how payment rules affect the mechanism.
---


## 1. Introduction {#sec-introduction}

A stronger incumbent bidder usually deters takeover competition. A prospective challenger must incur preparation costs before submitting an executable offer, and a stronger rival reduces its expected return from doing so [@Fishman1988; @HirshleiferPng1989]. This paper shows that the same rival can make the target's stock price more informative about the challenger's acquisition value. If the challenger observes that price before committing to preparation, the information effect can outweigh deterrence. A stronger incumbent then attracts a competing buyer and increases the probability that a high-value challenger acquires the target.

The relevant decision occurs between an expression of interest and a commitment to participate. A listed target may have a prepared lead buyer while other prospective acquirers are still deciding whether to investigate. Takeover records distinguish these stages. Imprivata's definitive proxy describes an unsolicited approach, outreach to potential buyers, and indications of interest conditional on further diligence [@Imprivata2016]. More broadly, much of takeover competition develops before public bidding [@BooneMulherin2007; @GentryStroup2019]. These observations motivate a costly preparation decision. They do not establish learning from prices: the mechanism requires a publicly understood sale opportunity that remains open to a challenger, a condition that an empirical study must verify.

I model a listed target sold through a cash second-price auction. An incumbent is already prepared to bid. A challenger learns its acquisition value only after paying a privately realized preparation cost. Before that decision, an investor who knows the challenger's value trades target shares against noise demand. Competitive market makers price aggregate order flow, anticipating both entry and the auction. The challenger observes the stock price and its preparation cost, then decides whether to become a bidder. Incumbent strength shifts the distribution of the prepared bidder's value upward.

The mechanism follows from the division of acquisition surplus. When the challenger has a high value, it wins and pays the incumbent's bid. When it has a low value, a sufficiently strong incumbent wins and pays the challenger's bid. A stronger incumbent therefore widens the difference in target proceeds between the two challenger types. Target shares become more sensitive to the information the investor holds, even as competition reduces the challenger's acquisition profit. Rational pricing incorporates the anticipated entry response, but noise trading leaves the investor an informational advantage. A larger difference in target proceeds can make that advantage worth trading on.

The main result compares economies in which equilibrium trading is unique, allowing arbitrary mixed orders and all continuous unilateral deviations. With a weak incumbent, the informational advantage is too small to cover trading costs. The price reveals nothing, and only a low-cost challenger prepares. With a stronger incumbent, informed trading becomes profitable, the investor trades to its limit, and favorable prices induce a high-cost challenger to prepare. Entry rises even though acquisition profit falls at every fixed belief. With a sufficiently strong incumbent, expensive preparation becomes unprofitable even at the most favorable attainable belief, and entry falls again. These comparisons hold on a nonempty open set of parameters.

The change in information is essential. If the investor's orders are held fixed at their informative level, stronger competition reduces entry. At intermediate incumbent strengths, the market can also support both informative and uninformative equilibria. I establish three informative equilibria by verified interval computation. In each, the investor buys fully after good news and sells partially after bad news; entry is strictly ordered upward across the three strengths. Numerical continuation describes additional parts of the equilibrium correspondence, but its complete characterization remains open. The distinction separates the entry reversal proved at specified economies from a claim about every equilibrium between them.

The reversal survives logistic noise, atomless preparation costs, and a narrower gap between acquisition values. It also arises when the challenger has a more accurate private signal than the investor: the price supplies complementary information. At fixed incumbent strength, access to prices raises target proceeds and acquisition surplus net of preparation costs. An alternative bargaining institution shows that the effect of competition on target-payoff sensitivity depends on how payments respond to the runner-up's value. Reserve comparisons illustrate how sale terms can change both information and participation; they do not solve the seller's optimization problem.

The paper connects takeover entry to financial-market feedback. In @DowGoldsteinGuembel2017, a firm's investment decision affects incentives to produce information in its stock. Here the sale rule divides acquisition surplus between a traded claim and a buyer deciding whether to enter, producing opposing effects on their returns to information. @EdmansGoldsteinJiang2015 show that corrective real decisions can discourage trading on bad news under rational pricing. I study how rival strength changes the information sensitivity of the claim and participation. Evidence that prices affect takeover activity [@EdmansGoldsteinJiang2012] concerns the direction from prices to control; it does not identify a prospective challenger learning its acquisition value. Learning from announcement returns in completion decisions [@Luo2005] occurs after the participation margin studied here.

The auction-entry literature makes the bidder pool endogenous [@GentryStroup2019; @LevinSmith1994] and shows how selective entry affects the choice of sale procedure [@RobertsSweeting2013]. I retain the direct deterrence force and add information from a market that operates before preparation. Auction formats can also affect bidders' incentives to acquire information [@Persico2000]. In this model, the informed trader is outside the auction, and the payoff it trades differs from the entrant's profit. Recent work studies bidder learning about own values and competitors [@PernoudGleyze2026], post-auction feedback in security-payment design [@LiuBernhardt2022], and bidder-pool choice with correlated values [@CarlinEtAl2026]. My focus is the effect of competition on information available before participation.

Other takeover models connect trading to later stages of a deal. @BettonEtAl2014 study negotiations with stock-market feedback, while @LinMaYangZhu2025 jointly model payment choice and trading within an initiated deal. I hold cash consideration fixed and study entry. Arbitrageurs' positions can affect tendering [@CornelliLi2002]; the investor here has information about a prospective acquirer and no role in tendering. The model excludes toeholds and dispersed-shareholder free riding [@BulowHuangKlemperer1999; @GrossmanHart1980]. Endogenous investor research would introduce additional incentives, including manipulation through the real decision that responds to the price [@GoldsteinGuembel2008].

Section 2 presents the model. Sections 3 and 4 derive the information mechanism and equilibrium results. Sections 5 and 6 examine robustness, welfare, and sale terms. Section 7 discusses empirical implications, and Section 8 concludes. The appendices contain supporting results, proofs, and reproducibility details.

## 2. The model {#sec-model}

### 2.1 Values, preparation, and the sale

The target's known standalone value is normalized to zero. Acquisition values and preparation costs are measured per target share. Adding the same standalone component to every ownership outcome shifts prices and payoffs by a constant without changing incentives. The investor's order is measured in a small reference trading unit and conveys no control rights.

Two potential acquirers face the target. The incumbent has already prepared and incurs no further participation cost. Its acquisition value $R$ is uniform on $[0,r]$, conditional on public information when the sale process begins. An increase in $r$ strengthens the incumbent in the sense of first-order stochastic dominance. The incumbent is a bidder, rather than the target's management, and knows its value before bidding.

The challenger has acquisition value $\theta\in\{\ell,h\}$, with equal prior probabilities. The benchmark restricts values and the reserve $p$ to

$$
0<p<\ell<r<h.
\tag{1}
$$

The challenger initially does not know its value. After observing the stock price, it privately learns its preparation cost $C$, which equals $c_L$ with probability $\rho$ and $c_H$ otherwise. I assume $0<\rho<1$ and $0\le c_L<c_H$. Paying $C$ reveals $\theta$ and permits bidding; declining leaves the challenger outside the sale. Incumbent value, challenger value, preparation cost, and noise demand are mutually independent.

Before trading, the seller publicly commits to a cash second-price auction with reserve $p$. The highest admissible bidder acquires the target and pays the larger of the reserve and the highest competing bid. There is no sale without an admissible bid. Both bidders use truthful, weakly dominant bids. A bid equal to the reserve is admissible, and a challenger indifferent about preparation enters. Acquisition-value ties have probability zero in the benchmark. Preparation indifference matters at a posterior plateau considered in Section 4.

### 2.2 Trading and timing

An investor observes $\theta$ and submits an order $q\in[-1,1]$. It has no initial position, cannot acquire the target, and pays a linear trading cost $k|q|$, where $k>0$. Its profit and aggregate order flow are

$$
\begin{gathered}
q\{V_T-P(X)\}-k|q|,\qquad X=q+Z,\\
f(z)=\frac{1}{2b}e^{-|z|/b},\qquad b>1.
\end{gathered}
\tag{2}
$$

Here $V_T$ is the terminal payoff of a target share and $Z$ is independent noise demand with a Laplace density. The bounded likelihood ratios of this density limit the information that any order can reveal. Section 5 also considers logistic noise.

Competitive market makers observe aggregate flow and set

$$
P(X)=\mathbb E[V_T\mid X],
\tag{3}
$$

anticipating preparation and auction outcomes. The challenger observes $P$, but not $X$.

The sequence is therefore: the seller announces the sale rule; the investor learns quality and trades; market makers set the price; the challenger observes the price and its cost and decides whether to prepare; informed bidders submit truthful bids; ownership and financial payoffs are realized.

### 2.3 Equilibrium

An equilibrium specifies conditional order distributions $\sigma_H,\sigma_L$, a measurable price function, Bayesian beliefs conditional on the observed price, optimal preparation, and truthful bidding. The investor can mix and can deviate to any order in $[-1,1]$. A unilateral deviation changes the distribution of order flow while holding the candidate equilibrium's pricing and preparation schedules fixed. A comparison across incumbent strengths instead re-solves these schedules.

Write $t_0$ for expected target proceeds without entry, $t_H,t_L$ for proceeds conditional on entry and quality, and $g_H,g_L$ for the challenger's corresponding gross acquisition profits. The target-payoff spread is $\Delta_T=t_H-t_L$. At a belief $\mu=\Pr(\theta=h)$, the challenger's expected gross profit is $B_r(\mu)=g_L+\mu(g_H-g_L)$.

## 3. Competition and information {#sec-payoffs}

### 3.1 Acquisition profits and target proceeds

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
\tag{4}
$$

The relevant derivatives are

$$
\begin{aligned}
B_r(\mu)&=g_L+\mu(g_H-g_L),\\
\Delta_T'(r)&=\frac12-\frac{\ell^2}{2r^2}>0,\\
g_H'(r)&=-\frac12+\frac{p^2}{2r^2}<0,
\qquad g_L'(r)=-\frac{\ell^2-p^2}{2r^2}<0.
\end{aligned}
\tag{5}
$$

Thus a stronger incumbent lowers acquisition profit at every fixed belief while making target proceeds more sensitive to challenger quality. Proposition 1 extends this opposition beyond the uniform distribution.

**Proposition 1 (competition and the two returns to information).** *Let the incumbent's value have a continuous distribution $F$ on $[0,\bar r]$ with $0<p<\ell<\bar r<h$, and extend $F$ by unity above its support. A first-order stochastic strengthening of $F$ weakly increases the spread of target proceeds between a high- and a low-value challenger and weakly decreases the challenger's gross acquisition profit at every fixed posterior, where*

$$
\begin{aligned}
\Delta_T(F)&=\mathbb E_F[(R-\ell)_+]
=\int_\ell^{\bar r}[1-F(u)]\,du,\\
G_\theta(F)&=\mathbb E_F[(\theta-\max\{p,R\})_+]
=\int_p^\theta F(u)\,du.
\end{aligned}
\tag{6}
$$

*Both comparisons are strict when the change in $F$ has positive integral over the corresponding range.*

The result follows directly from the payment rule. If $R\le\ell$, either challenger type outbids the incumbent and pays the same amount. If $R>\ell$, a high-value challenger wins and pays $R$, whereas a low-value challenger loses and the incumbent pays $\ell$. The difference in target proceeds is therefore $(R-\ell)_+$. A stronger incumbent increases its expectation. The same shift raises the payment required for the challenger to win and reduces its expected acquisition profit. Appendix A gives the proof.

```{=latex}
\setcounter{figure}{0}
\begin{figure}[tbp]\centering\begingroup\singlespacing
\includegraphics[width=\linewidth]{figures/two_returns.pdf}
\caption{Competition and the two returns to information.}\label{fig:1}
\par\medskip\begin{minipage}{\linewidth}\footnotesize\singlespacing\noindent \textit{Notes.} Panel (a) plots the target-payoff spread \(\Delta_T(r)\); panel (b)
plots gross challenger profit \(B_r(\mu)\) at the posterior bounds
\(m,M\) and the prior \(1/2\). Benchmark values are \(h=10\),
\(\ell=1\), \(p=0.5\), and \(b=2\). Values are per target share. These
are acquisition-stage payoffs, before solving trading and entry.\end{minipage}
\endgroup\end{figure}
```

Figure 1 shows both effects within the benchmark support. The target-payoff spread approaches zero as $r$ approaches $\ell$, since the incumbent then almost never outbids a low-value challenger. As $r$ increases, the spread rises while gross acquisition profit falls at each displayed belief. Whether entry rises depends on how this change in payoffs affects equilibrium information.

### 3.2 What the challenger learns from the price {#sec-inference}

Noise demand bounds the posterior under every feasible trading strategy. For arbitrary mixed orders, define

$$
\begin{aligned}
a_H(x)&=\int f(x-q)\,d\sigma_H(q),\qquad
&a_L(x)&=\int f(x-q)\,d\sigma_L(q),\\
\mu_X(x)&=\frac{a_H(x)}{a_H(x)+a_L(x)},\qquad
&m&=\frac1{1+e^{2/b}},\quad M=1-m.
\end{aligned}
\tag{7}
$$

The posterior satisfies $m\le\mu_X\le M$. For any two orders $q,q'\in[-1,1]$, the Laplace density obeys

$$
e^{-2/b}\le\frac{f(x-q)}{f(x-q')}\le e^{2/b},
\tag{8}
$$

Integrating over the conditional order distributions preserves these inequalities. Equal priors then give the posterior bounds. Since the price is a function of flow, the price-based posterior is a conditional expectation of $\mu_X$ and has the same bounds. A preparation decision requiring a belief above $M$ cannot be induced by any equilibrium price.

Suppose $c_L<B_r(m)$, so the low-cost challenger prepares at every feasible belief. Averaging over preparation costs gives the entry rule and candidate competitive price

$$
\begin{aligned}
e_r(\mu)&=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\\
P_r(\mu)&=t_0+e_r(\mu)[t_L-t_0+\Delta_T\mu].
\end{aligned}
\tag{9}
$$

Both entry and the expected increment in target proceeds increase weakly with $\mu$. The increment is strictly increasing, and entry is bounded below by $\rho>0$, so $P_r(\mu)$ is strictly increasing. The price can jump when high-cost preparation becomes worthwhile.

Price sufficiency also holds in any candidate equilibrium, rather than only in this construction. Let $e(P)$ denote entry conditional on the observed price, averaged over costs. Competitive pricing implies

$$
\begin{aligned}
P&=t_0+e(P)[t_L-t_0+\Delta_T\mu_X],\\
\mu_X&=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}.
\end{aligned}
\tag{10}
$$

The positive denominator makes $\mu_X$ a measurable function of $P$. The challenger can therefore recover the market maker's posterior from the price alone. This argument permits price atoms and entry jumps; it does not require differentiable prices. Propositions A.1 and A.2 give the formal statements.

### 3.3 Informed trading incentives

Rational pricing removes the anticipated increase in proceeds from the investor's informational advantage. What remains depends on challenger quality. The residual advantages of buying in state $H$ and selling in state $L$ are

$$
\begin{aligned}
A_H(x)&=\mathbb E[V_T\mid H,x]-P(x)=e_r(\mu_X(x))\Delta_T[1-\mu_X(x)],\\
A_L(x)&=P(x)-\mathbb E[V_T\mid L,x]=e_r(\mu_X(x))\Delta_T\mu_X(x),\\
\rho m\Delta_T&\le A_H(x),A_L(x)\le\Delta_T.
\end{aligned}
\tag{11}
$$

The market maker prices the entry response, but cannot identify quality perfectly because of noise demand. The investor's advantage is the entry probability times the target-payoff spread times the market's residual uncertainty. The lower bound uses the entry floor $\rho$ and posterior floor $m$; the upper bound is $\Delta_T$. Both hold for every candidate order distribution. Comparing these bounds with the trading cost determines when information can be sustained in equilibrium.

## 4. Equilibrium results {#sec-results}

### 4.1 Competition creates competition

The main result identifies an open set of economies in which stronger competition changes the unique equilibrium from an uninformative price to an informative price and raises challenger entry.

**Proposition 2 (competition creates competition).** *Fix $0<p<\ell<r_0<r_1<h$, $0<\rho<1$, $b>1$, and $k>0$, and suppose that*

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

*(i) With the weak incumbent $r_0$, the unique equilibrium trading outcome is $q_H=q_L=0$, the price carries no information, and entry equals $\rho$. (ii) With the strong incumbent $r_1$, the unique equilibrium trading outcome is $(q_H,q_L)=(1,-1)$, the price is informative, entry strictly exceeds $\rho$, and the probability that the high-value challenger acquires the target is strictly higher than at $r_0$. The strong-incumbent price experiment strictly Blackwell dominates the weak-incumbent experiment at the same noise law. (iii) For any $r_2\in(r_1,h)$ with $c_L<B_{r_2}(m)$, $B_{r_2}(M)<c_H$, and $k<(1-1/b)\rho m\Delta_T(r_2)$, the unique trading outcome is again $(1,-1)$, but entry returns to $\rho$. These comparisons hold on a nonempty open set of primitives. Uniqueness refers to trading and on-path entry under truthful bidding and allows arbitrary mixed orders and every continuous deviation.*

Condition (A1) ensures that low-cost preparation is worthwhile even at the lowest feasible belief. Condition (A2) excludes high-cost preparation at the weak-incumbent prior but permits it at favorable strong-incumbent prices. Condition (A3) places the trading cost above every possible informational return in the weak economy and below a global bound on marginal trading profits in the strong economy.

These inequalities determine trading before imposing a particular order profile. In the weak economy, the investor's gross advantage per unit is at most $\Delta_T(r_0)<k$, so every nonzero order loses money. With no informed trading, the posterior stays at the prior and only low-cost preparation occurs. In the strong economy, the residual lower bound is large enough to make every increase in a correctly signed order profitable. The bound controls the full order interval, including deviations from mixed candidate strategies. Full correctly signed orders are therefore necessary in every equilibrium. Appendix A derives the bound and constructs the associated price and entry schedules.

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
\tag{12}
$$

Condition (A2) places $\tau$ in $(1/2,M)$ and $x^*$ in $(0,1)$. Since $\alpha_H>\alpha_L$, the additional entry is tilted toward high-value challengers. At a sufficiently strong incumbent satisfying part (iii), even the largest feasible belief fails to justify high-cost preparation. Trading remains informative, but entry returns to $\rho$. The proposition establishes a rise and a subsequent fall across the specified economies; it does not impose a monotone path between them.

### 4.2 Benchmark and information controls

The benchmark uses incumbent strengths $r_0=1.2$, $r_1=3$, and $r_2=3.6$; Appendix A lists the full parameter vectors. From $r_0$ to $r_1$, gross acquisition profit at the prior falls from 4.804167 to 4.291667, while the target-payoff spread rises from 0.016667 to 0.666667. Entry nevertheless rises from 0.250000 to 0.522757, and high-value challenger ownership rises from 0.125000 to 0.324192. At $r_2$, entry returns to 0.250000.

```{=latex}
\setcounter{table}{0}
\begin{table}[tbp]\begingroup\singlespacing\small\centering
\caption{Acquisition-stage payoffs in the benchmark.}\label{tab:1}
\input{tables/table1_auction_primitives.tex}
\par\endgroup\end{table}
```

```{=latex}
\setcounter{table}{1}
\begin{table}[tbp]\begingroup\singlespacing\small\centering
\caption{Equilibrium outcomes, information controls, and welfare.}\label{tab:2}
\input{tables/table2_equilibrium_controls.tex}
\par\endgroup\end{table}
```

Table 1 reports the acquisition payoffs. Table 2 separates equilibrium outcomes from controls. Holding informative orders fixed restores deterrence: entry falls from 0.562178 to 0.522757 as the incumbent strengthens. At every belief and cost realization, the decline in gross acquisition profit can only remove a preparation incentive. Proposition A.3 states this result for any fixed information experiment. The frozen profile is a control, since full orders are unprofitable against the weak incumbent.

Hiding prices from the challenger produces entry 0.250000 and 0.250000 at the two strengths. The buyer uses its prior and prepares only at low cost. Together, these comparisons identify the source of the reversal: incumbent strength changes the information generated by trading, and the resulting entry response can exceed the direct deterrence effect.

### 4.3 Coexistence and the equilibrium correspondence

Informative trading need not be unique at intermediate strengths. Proposition 3 establishes three equilibria with full purchases and partial sales that coexist with no trade.

**Proposition 3 (coexisting informative equilibria at intermediate strength).** *At the benchmark parameters of Appendix A.6, there exist equilibria $(q_H,q_L)=(1,-v_j)$ at strengths $r_j$ whose certified enclosures are*

$$
\begin{array}{c@{\qquad}c@{\qquad}c}
r_j&v_j&\mathsf E_j\\[3pt]
1.55&[0.46031618,\,0.46031620]&[0.5450528898,\,0.5450528922]\\
1.60&[0.70747537,\,0.70747539]&[0.5487563062,\,0.5487563085]\\
1.65&[0.90333198,\,0.90333201]&[0.5513607988,\,0.5513608020]
\end{array}
\tag{13}
$$

*The entry intervals are strictly ordered upward. Each of the three economies also admits no trade with entry $\rho$.*

The proof uses interval arithmetic to enclose exact solutions. For the low-value investor, global strict concavity reduces optimality to a marginal-profit root. Opposite endpoint signs place a root inside each reported interval. For the high-value investor, a uniform derivative bound verifies that full purchases dominate every smaller order throughout the root bracket. Wrong-signed orders are unprofitable. The resulting entry enclosures are disjoint, which establishes the cross-economy ordering. Appendix A reports the certificate margins; Online Appendix B supplies the complete method.

```{=latex}
\setcounter{figure}{1}
\begin{figure}[tbp]\centering\begingroup\singlespacing
\includegraphics[width=\linewidth]{figures/equilibrium_correspondence.pdf}
\caption{Trading and entry across incumbent strengths.}\label{fig:2}
\par\medskip\begin{minipage}{\linewidth}\footnotesize\singlespacing\noindent \textit{Notes.} Benchmark parameters. Panel (a) shows entry for every accepted branch;
panel (b) shows the associated order magnitudes. Shading marks
analytical uniqueness regions and the range in which several equilibria
were found. The thresholds \(r_N,r_U,r_C\) respectively mark no-trade
existence, sufficient full-order uniqueness, and the ceiling for
high-cost entry. Black points carry the certified intervals of
Proposition 3. Other curves are numerical continuations, with breaks at
unresolved nodes and branch changes. Absence of a plotted branch does
not establish nonexistence. Online Appendix C.2 gives the search and
acceptance criteria.\end{minipage}
\endgroup\end{figure}
```

Figure 2 places the certified equilibria within the numerical correspondence. No trade remains an equilibrium up to $r_N=1.747877538$ and is uniquely optimal below the sufficient bound $\mathfrak r(k)=1.220997512$. Full orders are uniquely optimal above the sufficient bound $r_U=2.837416964$. High-cost entry becomes infeasible above $r_C=3.592658519$. Proposition A.4 defines these thresholds. An existence boundary, a sufficient uniqueness bound, and a participation ceiling answer different questions and need not coincide.

The numerical continuation finds asymmetric informative equilibria before no trade disappears. On this family, the investor buys fully after good news and sells partially after bad news. The short magnitude increases toward one as the incumbent strengthens, and entry rises along the accepted continuation. Full orders subsequently coexist with no trade. The search also finds a symmetric interior family whose price information is insufficient to induce high-cost preparation, so entry remains $\rho$. These descriptions concern the branches found and validated; the search is not exhaustive.

The trading asymmetry reflects the entry response. Around the high-cost preparation threshold, orders change both the posterior and the probability of entry, and thus the residual payoff to information. The low-value investor faces a different residual schedule from the high-value investor and can stop at an interior short while full purchases remain optimal. The certified points establish this behavior at three strengths. They do not prove a differentiable branch or a monotonicity result between the points.

No trade survives at the certified strengths because $\rho\Delta_T/2\le k$. Against an uninformative price with entry $\rho$, a unilateral informed order cannot cover its cost. An informative equilibrium instead changes the preparation response and the residual return to trading. The two outcomes can therefore be self-consistent at the same parameters.

At $r_C$, the Laplace posterior reaches its upper bound on a positive-probability tail. The convention that an indifferent challenger prepares preserves high-cost entry at the boundary itself; strictly above it, that entry disappears. The numerical searches also examined additional pure and finite-support mixed profiles. They found no mixed equilibrium, which remains a search result rather than a nonexistence theorem. The complete intermediate correspondence is open.


## 5. Robustness and private information {#sec-extensions}

### 5.1 Noise and preparation costs

The reversal extends beyond the benchmark's Laplace noise and two preparation-cost levels. Logistic noise also has a log-density derivative bounded in absolute value by $1/b$, so the global trading bounds remain valid. Proposition A.5 establishes the corresponding equilibrium and entry comparisons. Unlike the Laplace posterior, the logistic posterior reaches its bounds only as order flow tends to infinity.

In the strong benchmark economy, entry is 0.301509 under logistic noise, compared with 0.522757 under Laplace noise. The logistic flow threshold is 5.424598398, or 1.495369 noise standard deviations from the center. Thus the same posterior bounds can support different participation rates: the probability of favorable information near the upper bound also matters.

```{=latex}
\setcounter{figure}{2}
\begin{figure}[tbp]\centering\begingroup\singlespacing
\includegraphics[width=\linewidth]{figures/posterior_tail_entry.pdf}
\caption{Posterior tails and high-cost entry.}\label{fig:3}
\par\medskip\begin{minipage}{\linewidth}\footnotesize\singlespacing\noindent \textit{Notes.} Full orders at the strong benchmark strength and scale \(b=2\). Panel
(a) plots \(\Pr(\mu_X\ge\tau)\) against \(M-\tau\); panel (b) plots
implied entry. At zero threshold distance, the Laplace plateau induces
entry under the tie rule, whereas the logistic bound is unattained.
Scale, rather than variance, is held fixed. These are fixed-profile
comparisons; Online Appendix C.5 records equilibrium validation for each
implied cost. The figure does not establish a Blackwell ranking.\end{minipage}
\endgroup\end{figure}
```

Figure 3 compares the probability of crossing a preparation threshold close to $M$. Laplace noise assigns positive probability to the upper posterior bound; logistic noise does not. The comparison concerns the location of posterior mass at a common scale parameter, and cannot be interpreted as a general ordering of informativeness.

The result also holds when low and high preparation costs are drawn from atomless distributions with sufficiently narrow supports. The support conditions ensure that every low-cost realization prepares at every feasible belief, while high-cost preparation occurs only after sufficiently favorable prices in the strong economy. This preserves the entry floor and the global trading bounds. Proposition A.6 states the result, and Appendix A gives the support restrictions. With the declared cost half-width, strong-incumbent entry is 0.522715 under Laplace noise and 0.301374 under logistic noise.

### 5.2 Acquisition values

The reversal does not require the benchmark's tenfold gap between high and low acquisition values. With $h=2$ and $\ell=1$, the moderate-value specification satisfies all strict inequalities of Proposition 2. Entry rises from 0.250000 to 0.526805. More generally, for any $h>\ell$, the proof constructs weak and strong incumbent strengths sufficiently close to $\ell$, together with costs satisfying the strict inequalities. The relevant requirement is the placement of incumbent strength relative to the low acquisition value. Appendix A provides the construction; Online Appendix C.4 records the numerical examples.

### 5.3 Complementary private information

The challenger can benefit from prices even when its own information is more accurate than the investor's. A buyer may know its integration technology, while investors following the target hold information about its customers or product market. Diligence combines these sources. I represent this possibility with conditionally independent binary signals: the investor observes $T$ with accuracy $a$, and the buyer observes $Y$ with accuracy $d$, where $a,d\in(1/2,1)$. The buyer observes its signal and the price before preparing; preparation still reveals the exact acquisition value.

Private information makes entry state-dependent even conditional on the price. A high-value challenger is more likely to receive favorable private information and therefore more likely to prepare. Competitive pricing incorporates both conditional entry rates. Nevertheless, the positive entry floor leaves a strictly positive coefficient on public beliefs, so the price still reveals the market's posterior. The buyer combines that posterior with its own signal. Appendix A derives the posterior formulas, state-dependent pricing, and trading bounds.

Proposition A.7 gives sufficient conditions for unique zero orders and entry $\rho$ in the weak economy, and unique full orders by investor signal with entry above $\rho$ in the strong economy. These conditions allow arbitrary mixed signal-contingent orders and every continuous deviation. They do not require the investor's signal to be more accurate than the buyer's.

The declared example has buyer accuracy 75\% and investor accuracy 70\%. Entry rises from 0.850000 to 0.879438. A favorable private signal alone does not justify high-cost preparation against the weak incumbent; combined with a favorable price, it does against the strong incumbent. Table 3 reports this example with the other robustness checks. The full accuracy grid, including validated economies outside the sufficient uniqueness region, appears in Online Appendix Table 1.

```{=latex}
\setcounter{table}{2}
\begin{table}[tbp]\begingroup\singlespacing\small\centering
\caption{Robustness and complementary private information.}\label{tab:3}
\input{tables/table3_extensions.tex}
\par\endgroup\end{table}
```

## 6. Welfare and sale terms {#sec-welfare}

### 6.1 Access to prices

Access to prices improves acquisition outcomes at a fixed level of competition. Hold the incumbent at $r_1$ and compare the feedback equilibrium with an economy in which the challenger cannot observe the price. All other parameters are unchanged, and trading and pricing are reoptimized in both economies. Proposition A.9 establishes that price access increases expected target proceeds and acquisition surplus net of preparation costs. The comparison also holds with logistic noise and atomless preparation costs.

The two economies generate the same order-flow experiment. The global trading bound forces full orders even when the challenger cannot use the price and entry remains $\rho$. Trading costs therefore coincide. Price access changes which high-cost challengers prepare. Conditional on the information and cost that induce an additional entrant, expected gross acquisition profit covers preparation cost. The allocation gain includes that profit and the value of sales that would otherwise fail the reserve. Appendix A gives the accounting identities. Transfers between bidders, shareholders, and traders are excluded from acquisition surplus.

Table 2 reports the fixed-strength comparison. Expected target proceeds are 0.872392 with price access and 0.614583 without it. This is a welfare result about access to information under a given sale rule and incumbent distribution; it does not rank different incumbent strengths or sale mechanisms.

The information effect can be separated from the average price level. Add a deterministic external dividend of 0.257809 to the traded claim in the price-hidden economy. The dividend raises both the terminal financial payoff and its price by the same amount, leaving $V_T-P$, trading incentives, and entry unchanged. Mean prices then match those in the feedback economy, while entry still differs. This dividend is a diagnostic payment, excluded from acquisition surplus and from the seller's feasible sale terms.

### 6.2 The payment rule

The effect of competition on target-payoff sensitivity depends on the sale payment. To isolate this dependence, consider a verifiable-value institution with zero reserve. After diligence, the highest-value buyer acquires the target. A sale to the next-best buyer at its value is an enforceable fallback, accepted at zero surplus. The seller and winner divide the surplus above this fallback by Nash bargaining, with seller share $\eta$.

Without a challenger, the seller receives $\eta R$. For an incumbent distribution supported on $[0,R_{\max}]$, with $\ell<R_{\max}<h$ and $0\le\eta<1$, the transfer, challenger profit, and target-payoff spread are

$$
\begin{aligned}
T_\eta(R,\theta)&=(1-\eta)\min\{R,\theta\}+\eta\max\{R,\theta\},\\
G_{\theta,\eta}&=(1-\eta)\mathbb E[(\theta-R)_+],\\
\Delta_\eta&=\eta(h-\ell)+(1-2\eta)\mathbb E[(R-\ell)_+].
\end{aligned}
\tag{14}
$$

Proposition A.8 establishes the comparative statics. A stronger incumbent weakly reduces challenger profit for every bargaining weight. Its effect on the target-payoff spread is positive for $\eta<1/2$, zero at $\eta=1/2$, and negative for $\eta>1/2$, with strictness determined by the change in the incumbent distribution.

To see why, take $R>\ell$. A high-value challenger wins and pays $(1-\eta)R+\eta h$, whose sensitivity to $R$ is $1-\eta$. A low-value challenger loses, and the incumbent pays $(1-\eta)\ell+\eta R$, whose sensitivity is $\eta$. Competition widens the difference precisely when the first sensitivity exceeds the second. Thus the benchmark's opposition between acquisition profit and target-payoff sensitivity depends on the weight placed on the runner-up's value.

```{=latex}
\setcounter{figure}{3}
\begin{figure}[tbp]\centering\begingroup\singlespacing
\includegraphics[width=\linewidth]{figures/bargaining_weight.pdf}
\caption{Bargaining and the division of acquisition surplus.}\label{fig:4}
\par\medskip\begin{minipage}{\linewidth}\footnotesize\singlespacing\noindent \textit{Notes.} Zero-reserve verifiable-value institution, \(h=10\), \(\ell=1\), and
uniform incumbents with \(r=1.2\) or \(r=3\). Panel (a) plots
\(\Delta_\eta\) against seller weight \(\eta\); panel (b) plots
conditional challenger profits on a log scale. Values are per target
share. The comparison concerns acquisition-stage payoffs; trading and
entry under this institution are not solved.\end{minipage}
\endgroup\end{figure}
```

Figure 4 illustrates these payment-stage results. They identify a condition under which stronger competition increases the sensitivity of target shares to challenger quality. They do not establish an entry reversal under bargaining, which would require solving its trading and participation game.

### 6.3 Reserve comparisons {#sec-design}

A reserve affects both the payment required to win and the information embedded in target shares. A reserve that excludes the low-value challenger can widen the difference in target proceeds across challenger types. This can support informative trading even against a weak incumbent. I illustrate this possibility with two reserve levels; the seller's complete continuation problem and local revenue decomposition appear in Appendix A.

To avoid making exclusion depend on an acquisition-value atom, let quality identify a low or high value class, each with probability one half. Conditional values are uniform around $\ell$ and $h$ with half-width $\varepsilon_V=0.05$. The investor observes the class, and preparation reveals the exact value. Increasing the reserve from 0.5 to 1.1 raises weak-incumbent revenue from 0.392665 to 0.432173 and strong-incumbent revenue from 0.872367 to 1.014500. At the higher reserve, entry is 0.540309 and 0.511638, respectively, and trading is informative in both economies. The global bounds establish unique trading continuations at the reported reserve choices.

```{=latex}
\setcounter{table}{3}
\begin{table}[tbp]\begingroup\singlespacing\small\centering
\caption{Reserve comparisons and exploratory continuations.}\label{tab:4}
\input{tables/table4_reserve_comparisons.tex}
\par\endgroup\end{table}
```

Table 4 reports the declared comparisons and an exploratory sweep over the reserve domain. The higher reserve excludes the low-value class and changes both acquisition incentives and the target-payoff spread. Its revenue advantage demonstrates a feasible improvement over the original reserve. It does not identify an optimal reserve. The sweep reports outcomes among continuations found and records unresolved reserves; neither an envelope of found revenues nor a missing continuation establishes the seller's solution.

## 7. Empirical implications {#sec-program}

The model concerns a decision to prepare, made before the set of executable bids is fixed. An empirical counterpart is the start of substantive diligence or the submission of a proposal requiring costly preparation, rather than the number of public offers. Incumbent strength must be measured using information available before that decision. The relevant price information must also precede entry. Later target returns can reflect anticipated bidder arrival, so a return-entry association alone does not identify learning.

Online Appendix D proposes an institutional pilot that reconstructs the timing of approaches, public visibility, buyer contacts, diligence, proposals, and final selection from disclosure records. It separates contemporaneous public information from facts disclosed only retrospectively. The first requirement is a publicly understood sale opportunity that remains contestable while a prospective challenger decides whether to investigate. A traded stock during confidential negotiations is insufficient. The pilot specifies a research design; no sample, estimated effect, or instrument is reported here.

## 8. Conclusion {#sec-conclusion}

The bidder pool in a takeover depends on the information available before buyers commit to participation. A stronger incumbent can increase the sensitivity of target proceeds to challenger quality, making informed trading profitable and bringing a challenger into the auction. This connects the division of acquisition surplus to the formation of competition. Sale terms therefore affect participation through both the buyer's expected payment and the information supplied by the stock market.

The next theoretical step is to characterize the seller's choice of terms with the full equilibrium continuation correspondence retained. The reserve comparisons show why this choice matters, while multiplicity prevents a direct identification of the seller's objective with an envelope of found revenues. A related question is whether committing before trading improves outcomes relative to revising terms after observing prices. Solving alternative auction formats and endogenous investor research would further clarify the role of payment rules and manipulation incentives [@GoldsteinGuembel2008]. Empirical work must first establish the decision interval and information sets required for buyers to learn from prices.

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

### A.1 Supporting results {#pa-results}


These supporting results supply the inference, comparative statics, and extensions used in the main text. The indicated sections of the Online Appendix provide complete proofs.

**Proposition A.1 (posterior bounds).** *For arbitrary mixed state-contingent orders on $[-1,1]$, the order-flow posterior $\mu_X$ and the posterior based on the price lie in $[m,M]$, where $a_H$, $a_L$, $\mu_X$, $m$, and $M$ are defined in (7).*

For any feasible orders $q,q'$ the triangle inequality gives $e^{-2/b}\le f(x-q)/f(x-q')\le e^{2/b}$, which is (8). Integrating against $d\sigma_H(q)\,d\sigma_L(q')$ preserves both inequalities, and equal priors turn them into bounds on $\mu_X$. Because the price is a function of $X$, the price posterior is $\mathbb E[\mu_X\mid P]$ and inherits the interval. Online Appendix A.1 and A.3 give the measure-theoretic version.

**Proposition A.2 (price sufficiency and residual profits).** *Suppose $c_L<B_r(m)$. The observed price reveals $\mu_X$ almost surely. Entry and competitive pricing take the form (9), and the residual advantages of an informed buyer of shares in state $H$ and of an informed short seller in state $L$ are given by (11), with $\rho m\Delta_T\le A_H(x),A_L(x)\le\Delta_T$.*

The low-cost buyer enters at every feasible price, so entry is at least $\rho$ and the denominator in (10) is positive. The posterior is then a measurable function of the price, and conditioning it on the price again leaves it unchanged. The price construction in (9) is strictly increasing in the posterior because entry is nondecreasing and positive while the bracket $t_L-t_0+\Delta_T\mu$ is positive and increasing. Subtracting the price from $t_0+e(t_H-t_0)$ in state $H$, and reversing the subtraction in state $L$, gives (11). Online Appendix A.3 supplies the conditional-probability argument and the convolution regularity used later.

**Proposition A.3 (fixed information experiment).** *Hold the joint distribution of a signal, challenger quality, and preparation cost fixed as $r$ changes. If the posterior generated by that signal does not change with $r$, entry is weakly decreasing in $r$. It decreases strictly when the decline in gross profit crosses preparation costs on a positive-probability set of signal and cost realizations.*

The argument is pointwise. Since $B_{r_1}(\mu)\le B_{r_0}(\mu)$ for $r_1>r_0$, the indicator $\mathbf1\{C\le B_r(\mu)\}$ cannot switch from nonentry to entry as $r$ rises. This applies within a region of fixed full orders, where the conditional flow laws do not depend on $r$. It does not apply across order profiles that change with $r$, because changing orders change the experiment. Online Appendix A.5 gives the strictness condition.

**Proposition A.4 (pooling, full orders, and expensive-entry feasibility).** *Restrict attention to strengths in $(\ell,h)$ for which $c_L<B_r(m)$ and $B_r(1/2)<c_H$. Define*

$$
\begin{aligned}
\mathfrak r(d)&=\ell+d+\sqrt{d^2+2\ell d},\\
r_N&=\mathfrak r(2k/\rho),\qquad
r_U=\mathfrak r\left(\frac{k}{(1-1/b)\rho m}\right).
\end{aligned}
\tag{A.1}
$$

*No trade is an equilibrium exactly when $\rho\Delta_T(r)/2\le k$, that is, when $r\le r_N$. The stronger restriction $r<\mathfrak r(k)$ guarantees that it is the unique outcome. The restriction $r>r_U$ guarantees unique full orders. Expensive entry is impossible in every equilibrium when $B_r(M)<c_H$. If the equality $B_r(M)=c_H$ has a solution in the specified domain, its unique crossing is*

$$
r_C=\frac{Mh-c_H+\sqrt{(Mh-c_H)^2+M[(1-M)\ell^2-p^2]}}{M}.
\tag{A.2}
$$

*At $r_C$ the tie rule of Section 2 is retained.*

Under no trade the posterior is $1/2$, entry is $\rho$, and a correctly signed order of size $s$ earns (A.25) below; zero is optimal exactly when the coefficient is nonpositive, which gives $r_N$. The sufficient uniqueness boundary $\mathfrak r(k)$ comes from $\Delta_T<k$, which defeats any nonzero order against every candidate schedule. The full-order boundary $r_U$ comes from the derivative bound (A.5). The function $B_r(M)$ in (A.26) is strictly decreasing on the auction-support domain, so there is at most one crossing of $c_H$, and (A.2) selects the larger algebraic root. Under Laplace noise the maximum posterior is attained on the positive-probability tail $x\ge1$, so indifference at $r_C$ is not a null event and the tie rule matters there. Online Appendix A.5 derives the formulas and their domain.

**Proposition A.5 (logistic noise).** *Replace Laplace noise by logistic noise with the density in (A.6). Under conditions (A1) to (A3), the unique trading outcomes and the entry and ownership comparisons of Proposition 2 remain valid, with the threshold and favorable-flow probabilities given by (A.7).*

The log-density derivative of the logistic law is bounded in absolute value by $1/b$, which is all the global trading argument uses. Under full orders the posterior is strictly increasing with log odds (A.8) below, spans the open interval $(m,M)$, and reaches every interior threshold with positive probability. Online Appendix A.6 has the inversion.

**Proposition A.6 (atomless preparation costs).** *Replace the cost atoms by atomless low- and high-cost distributions with probabilities $\rho$ and $1-\rho$, supported respectively within $[c_L-\varepsilon_C,c_L+\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$. Suppose the support conditions (A.9) hold and retain (A3). The unique trading outcomes and the entry and ownership reversal in parts (i) and (ii) of Proposition 2 hold under either noise law.*

Every low-cost realization participates at every feasible belief, which preserves the residual lower bound. At the weak prior all high-cost realizations stay out; at prices close enough to the upper feasible posterior all of them enter, and that event has positive probability under either noise law. The price construction stays strictly increasing because the cost CDF is nondecreasing. Online Appendix A.6 proves it without assuming a density.

**Proposition A.7 (complementary private signals).** *In the complementary-signal economy of Section 5.3, choose $0<p<\ell<r_0<r_1<h$ and suppose*

$$
\begin{gathered}
c_L<B_{r_1}(\phi_-(\mu_-)),\qquad
B_{r_0}(d)<c_H<B_{r_1}(\phi_+(\mu_+)),\\
(2a-1)\{\Delta_T(r_0)+(1-\rho)(2d-1)w_H(r_0)\}<k\\
<\left(1-\frac1b\right)m(2a-1)\rho\Delta_T(r_1).
\end{gathered}
\tag{A.3}
$$

*The weak economy has unique zero informed orders and entry $\rho$. The strong economy has unique orders $q(T=+)=1$ and $q(T=-)=-1$, and entry strictly exceeds $\rho$. The conclusions permit arbitrary mixed signal-contingent orders and every continuous unilateral deviation.*

The proof controls public beliefs before imposing any order profile, proves the price inversion with state-dependent entry, and applies the global trading bounds to the residuals (A.15), which satisfy (A.17) below. In the weak economy even the buyer's favorable private signal is not enough for expensive preparation; in the strong economy that signal together with a favorable price is. Online Appendix A.7 gives the joint conditional laws and the probability formulas.

**Proposition A.8 (bargaining).** *In the verifiable-value institution of Section 6.2, let $R$ have any distribution supported on $[0,R_{\max}]$ with $0<\ell<R_{\max}<h$. For $0\le\eta<1$ the institution generates (14). A first-order stochastic strengthening of the incumbent weakly reduces challenger profits. It weakly increases the target's information spread for $\eta<1/2$, leaves that spread unchanged at $\eta=1/2$, and weakly decreases it for $\eta>1/2$. Strictness follows from a positive integral change in the corresponding payoff function.*

With fallback $z$ and winning value $V>z$, the Nash solution maximizes $(P-z)^\eta(V-P)^{1-\eta}$ on $[z,V]$ and gives $P=z+\eta(V-z)$; the zero-weight endpoint follows by continuity. A challenger wins only if $\theta\ge R$ and keeps $(1-\eta)(\theta-R)$. Subtracting target payments state by state gives a high-low difference of $\eta(h-\ell)$ when $R\le\ell$ and $\eta(h-\ell)+(1-2\eta)(R-\ell)$ when $R>\ell$; taking expectations gives (14), and first-order stochastic dominance applied to the increasing function $(R-\ell)_+$ and the decreasing function $(\theta-R)_+$ gives the signs. Online Appendix A.8 treats the endpoints.

**Proposition A.9 (access to prices).** *Hold $r=r_1$ and all other primitives fixed under the conditions of Proposition 2. Compare the feedback equilibrium with the equilibrium in which the challenger cannot observe the target price, reoptimizing trading and pricing in both. Access to prices strictly increases expected target proceeds and acquisition surplus net of preparation costs. The comparison also holds under Propositions A.5 and A.6.*

In the price-hidden game the buyer's posterior stays at the prior, so entry is $\rho$; the strong trading bound still applies with constant entry, so orders are full in both games and the noise distribution and order magnitudes coincide. Identity (A.19) gives the pointwise allocation gain, every additional entrant contributes at least $p^2/r$, and averaging over the positive-probability event of additional entry gives the first line of (A.20). Since $t_H,t_L>t_0$, the second line follows. The dividend argument of Section 6.1 shifts the price by a constant and leaves $V_T-P$ unchanged. Online Appendix A.9 states the coupling and the atomless-cost integral.


### A.2 Trading bounds and extension formulas {#pa-calculations}

#### Trading incentives

Fix a candidate pricing and preparation schedule. For a correctly signed order of magnitude $s\in[0,1]$, define

$$
\begin{aligned}
F_H(s)&=\int f(x-s)A_H(x)\,dx,\\
F_L(s)&=\int f(x+s)A_L(x)\,dx,\\
U_\theta(s)&=sF_\theta(s)-ks.
\end{aligned}
\tag{A.4}
$$

The Laplace bound $|f'|\le f/b$ implies $|F_\theta'|\le F_\theta/b$. Together with the residual lower bound, this gives

$$
U_\theta'(s)\ge\left(1-\frac{s}{b}\right)F_\theta(s)-k
\ge\left(1-\frac1b\right)\rho m\Delta_T-k>0
\tag{A.5}
$$

under the strong-incumbent inequality in (A3). The derivative bound holds over the entire order interval. The proof below justifies differentiation with discontinuous entry and establishes global optimality.

#### Logistic noise and atomless costs

The logistic density and full-order threshold probabilities are

$$
f_{\mathrm{log}}(z)=\frac{1}{4b}\operatorname{sech}^{2}\left(\frac z{2b}\right),\qquad b>1.
\tag{A.6}
$$

$$
\begin{aligned}
x^*_{\mathrm{log}}&=b\log\frac{Aw-1}{A-w},\\
\alpha_H^{\mathrm{log}}&=\frac1{1+e^{(x^*_{\mathrm{log}}-1)/b}},\\
\alpha_L^{\mathrm{log}}&=\frac1{1+e^{(x^*_{\mathrm{log}}+1)/b}}.
\end{aligned}
\tag{A.7}
$$

where $A=e^{1/b}$ and $w=\sqrt{\tau/(1-\tau)}$. Under full orders, the posterior log odds are

$$
2\log\cosh\left(\frac{x+1}{2b}\right)
-2\log\cosh\left(\frac{x-1}{2b}\right),
\tag{A.8}
$$

The derivative is positive, and the limits are $-2/b$ and $2/b$. The posterior therefore spans $(m,M)$ and crosses every interior preparation threshold with positive probability.

For atomless low- and high-cost distributions supported within $[c_L-\varepsilon_C,c_L+\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$, the sufficient support restrictions are

$$
\begin{gathered}
c_L-\varepsilon_C\ge0,\qquad c_L+\varepsilon_C<B_{r_1}(m),\\
B_{r_0}(1/2)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{r_1}(M),
\end{gathered}
\tag{A.9}
$$

together with (A3). Every low-cost realization then prepares at every feasible belief. All high-cost realizations stay out at the weak-incumbent prior and enter at sufficiently favorable strong-incumbent prices. Monotonicity of the cost CDF preserves the price construction.

The nonempty parameter region does not require a large value gap. At the continuous limit $r=\ell$,

$$
B_\ell(M)-B_\ell(1/2)=(M-1/2)(h-\ell)>0,
\tag{A.10}
$$

Choose $r_1$ sufficiently close to $\ell$ that $B_{r_1}(M)>B_\ell(1/2)$. Then choose $r_0\in(\ell,r_1)$ sufficiently close to $\ell$ that $\Delta_T(r_0)<(1-1/b)\rho m\Delta_T(r_1)$. Trading and preparation costs can be selected strictly inside the resulting bounds for any $h>\ell$. Strict inequalities preserve the result under small perturbations.

#### Complementary private signals

The investor and buyer observe signals $T,Y\in\{+,-\}$, conditionally independent given quality, with accuracies

$$
\begin{aligned}
\Pr(T=+\mid H)&=\Pr(T=-\mid L)=a,\\
\Pr(Y=+\mid H)&=\Pr(Y=-\mid L)=d,
\qquad a,d\in(1/2,1).
\end{aligned}
\tag{A.11}
$$

Write $\lambda_X=\Pr(T=+\mid X)$. Public beliefs about quality, their bounds, and the buyer's combined posteriors are

$$
\begin{aligned}
\mu_X&=(1-a)+(2a-1)\lambda_X,\\
\mu_-&=(1-a)+(2a-1)m,\qquad \mu_+=(1-a)+(2a-1)M,\\
\phi_+(\mu)&=\frac{d\mu}{d\mu+(1-d)(1-\mu)},\\
\phi_-(\mu)&=\frac{(1-d)\mu}{(1-d)\mu+d(1-\mu)}.
\end{aligned}
\tag{A.12}
$$

Set $w_H=t_H-t_0$, $w_L=t_L-t_0$, and $I_y=\mathbf1\{B_r(\phi_y(\mu))\ge c_H\}$. Conditional entry rates and the coefficient on public beliefs are

$$
\begin{aligned}
e_H&=\rho+(1-\rho)[dI_++(1-d)I_-],\\
e_L&=\rho+(1-\rho)[(1-d)I_++dI_-],\\
D&=e_Hw_H-e_Lw_L,\\
\rho\Delta_T&\le D\le\Delta_T+(1-\rho)(2d-1)w_H.
\end{aligned}
\tag{A.13}
$$

The difference in entry rates is nonnegative: the high-value challenger is more likely to receive a favorable private signal. Competitive pricing and inversion give

$$
\begin{aligned}
P&=t_0+e_L(P)w_L+\mu_XD(P),\\
\mu_X&=\frac{P-t_0-e_L(P)w_L}{D(P)}.
\end{aligned}
\tag{A.14}
$$

The strictly positive coefficient $D$ lets the buyer recover the public posterior and combine it with its signal. The investor's residuals are

$$
A_+=(2a-1)(1-\lambda_X)D,
\qquad A_-=(2a-1)\lambda_XD.
\tag{A.15}
$$

The useful bounds follow from

$$
D=e_L\Delta_T+(e_H-e_L)w_H,
\quad 0\le e_H-e_L\le(1-\rho)(2d-1),
\tag{A.16}
$$

and therefore

$$
m(2a-1)\rho\Delta_T\le A_+,A_-
\le(2a-1)[\Delta_T+(1-\rho)(2d-1)w_H],
\tag{A.17}
$$

At the strong incumbent strength, the convolution argument yields

$$
U'(s)\ge(1-1/b)m(2a-1)\rho\Delta_T(r_1)-k>0,
\tag{A.18}
$$

under Proposition A.7. This bound forces full signal-contingent orders against every candidate equilibrium schedule. Online Appendix A.7 supplies the joint probability laws and the complete price-sufficiency argument.

#### Acquisition surplus

Without a challenger, ownership value is $W_0(R)=R\mathbf1\{R\ge p\}$. With challenger value $\theta>p$, it is $W_\theta(R)=\max\{R,\theta\}$. The pointwise difference is

$$
W_\theta(R)-W_0(R)
=(\theta-\max\{p,R\})_++p\mathbf1\{R<p\}.
\tag{A.19}
$$

At belief $\mu$ and preparation cost $C$, additional entry contributes conditional expected net surplus $B_r(\mu)-C+p^2/r$. Optimal preparation requires $B_r(\mu)\ge C$, so the contribution is positive. Low-cost entry is unchanged in the matched comparison. For cost atoms, the surplus and target-proceeds gains are

$$
\begin{aligned}
\Delta\mathcal W&=(1-\rho)\mathbb E\left[
\left(B_r(\mu_X)-c_H+\frac{p^2}{r}\right)\mathbf1\{\mu_X\ge\tau\}\right]>0,\\
\Delta\mathcal R_T&=\frac{1-\rho}{2}
\left[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\right]>0.
\end{aligned}
\tag{A.20}
$$

Transfers among bidders, shareholders, market makers, and noise traders cancel. Full orders imply equal trading costs in the two economies. The comparison holds incumbent strength and the sale rule fixed.

### A.3 Proofs of Propositions 1 to 3 {#pa-proofs}


*Proposition 1.* The realized sale rule determines the payoff formulas. Without entry the target receives $p\mathbf1\{R\ge p\}$. With a high-quality challenger the challenger wins and pays $\max\{p,R\}$. With a low-quality challenger the target receives $\max\{p,\min(R,\ell)\}$ and the challenger obtains $(\ell-\max\{p,R\})_+$. Truthful bidding is weakly dominant conditional on every competing bid, so none of this depends on a conjectured shading strategy. For the uniform incumbent,

$$
\begin{aligned}
t_H&=\frac1r\left[\int_0^p p\,du+\int_p^r u\,du\right],\\
t_L&=\frac1r\left[\int_0^p p\,du+\int_p^\ell u\,du+\int_\ell^r\ell\,du\right],\\
g_L&=\frac1r\left[\int_0^p(\ell-p)\,du+\int_p^\ell(\ell-u)\,du\right],
\end{aligned}
\tag{A.21}
$$

which evaluate to (4) and differentiate to (5). The distribution-free opposition rests on one observation. If $R\le\ell$, the high and low target payments coincide; if $R>\ell$, they differ by $R-\ell$; hence the difference is $(R-\ell)_+$. Tonelli's theorem applied to the nonnegative indicators gives both integrals in (6). A stronger distribution has a smaller CDF, which raises the survival integral and lowers the profit integral, and positive integral differences make the comparisons strict. A weighted average at a fixed posterior preserves the profit ordering. Online Appendix A.2 gives the measure formulation.

*Proposition 2.* The proof has six steps; Online Appendix A.1 to A.4 supply the conditional-probability versions, the null-set invariance under deviations, and the convolution regularity.

First, beliefs are bounded under every trading strategy. Positivity of $f$ makes every conditional flow density positive, and integrating (8) gives $m\le\mu_X\le M$; the price posterior obeys the same bound by conditional expectation. Because $g_H$ and $g_L$ both fall with $r$, condition (A1) gives $c_L<B_r(m)$ in both economies.

Second, the buyer's actual information can be recovered. The low-cost type enters at every feasible price, so entry is at least $\rho$ and (10) has a positive denominator. The posterior is therefore measurable with respect to the price and $\Pr(H\mid P)=\mu_X$ almost surely. Subtracting conditional payoffs yields the residuals (11). This uses the independence of $R$ and $C$ from trading, not an assumption that the buyer sees order flow.

Third, every nonzero order is eliminated in the weak economy. A correctly signed order of size $s>0$ earns at most $s[\Delta_T(r_0)-k]<0$, and a wrong-signed order has negative gross payoff and still pays its cost. Zero is therefore the only best response against every candidate equilibrium, including mixed ones. Under zero orders $\mu_X=1/2$, and (A1) and (A2) give entry $\rho$; constant pricing constructs the equilibrium.

Fourth, the entire order interval is controlled in the strong economy. For a bounded residual $A$, the translation formula

$$
F(s_2)-F(s_1)
=\int_{s_1}^{s_2}\int \partial_u f(x\mp u)A(x)\,dx\,du
\tag{A.22}
$$

follows from the fundamental theorem for the absolutely continuous density and Fubini, since the absolute double integral is at most $\|A\|_\infty|s_2-s_1|\|f'\|_1$. Thus $F$ is absolutely continuous with $|F'|\le F/b$ almost everywhere, (11) gives $F\ge\rho m\Delta_T$, and differentiating $U=sF-ks$ under (A3) yields (A.5). Integrating the positive lower bound on the derivative shows that the full correctly signed order strictly dominates every smaller magnitude; wrong signs are dominated by zero. Every equilibrium therefore has full correctly signed orders, and mixing cannot introduce another optimal action.

Fifth, the informative equilibrium exists. Full orders give

$$
\mu_X(x)=\left[1+\exp\left\{-\frac{|x+1|-|x-1|}{b}\right\}\right]^{-1}.
\tag{A.23}
$$

Defining entry and price by (9), the strict monotonicity of $P_r(\mu)$ gives a measurable inverse on its image, including across its upward jump. The buyer recovers the posterior from the price, prepares optimally, and bids truthfully. The bounds above verify investor optimality and market-maker pricing.

Sixth, the comparisons follow. Since $B_r$ increases in $\mu$ and decreases in $r$, condition (A2) places $\tau$ in $(1/2,M)$ and $x^*$ in $(0,1)$, and the Laplace survival function evaluated at $x^*-1$ and $x^*+1$ gives $\alpha_H$, $\alpha_L$, and the entry and ownership formulas in (12). The favorable event has positive probability. Ignoring the strong-economy price reproduces the uninformative experiment, while no state-independent transformation of a constant experiment can reproduce a nonconstant state-dependent law, so the strong experiment strictly Blackwell dominates the weak one. Strict margins make the region open.

For part (iii), the low-cost floor and the derivative bound at $r_2$ give unique full orders exactly as in the fourth and fifth steps, while $B_{r_2}(M)<c_H$ excludes every expensive entrant because $M$ is the largest attainable belief, so entry returns to $\rho$. The boundary $r_C$ depends on how the posterior attains its upper bound. Under full Laplace orders $\mu_X=M$ on $x\ge1$, an event of positive probability, and the tie rule admits expensive entry at $r_C$ on that event. As $r$ approaches $r_C$ from below,

$$
\mathsf E(r)\longrightarrow\rho+\frac{1-\rho}{4}(1+e^{-2/b}),
\tag{A.24}
$$

whereas strictly above $r_C$ expensive entry is impossible. Under logistic noise the posterior reaches $M$ only in the limit, so expensive entry converges to zero continuously. Online Appendix A.5 has the derivations, together with the no-trade deviation payoff

$$
s\left(\frac{\rho\Delta_T(r)}2-k\right)
\tag{A.25}
$$

and the ceiling profit

$$
B_r(M)=Mh-\frac{Mr}{2}+\frac{(1-M)\ell^2-p^2}{2r}
\tag{A.26}
$$

used in Proposition A.4.

*Proposition 3.* The proof is computer-assisted and is laid out in the next subsection.


### A.4 The certified equilibria {#pa-certificate}


Fix $(q_H,q_L)=(1,-v)$ with $0<v<1$. Bayes' rule gives $\mu_v(x)=\operatorname{logistic}((|x+v|-|x-1|)/b)$, which ranges from $m_v=(1+e^{(1+v)/b})^{-1}$ to $M_v=1-m_v$. In the certified region $1/2<\tau<M_v$, and

$$
\begin{aligned}
x^*(r,v)&=\frac{b\operatorname{logit}(\tau)+1-v}{2},\\
\mathsf E(r,v)&=\rho+\frac{1-\rho}{2}
\left[1-\frac12e^{(x^*-1)/b}+\frac12e^{-(x^*+v)/b}\right].
\end{aligned}
\tag{A.27}
$$

The unfavorable type's problem is globally concave. Its residual $A_L=e(\mu_v)\Delta_T\mu_v$ is bounded, nonconstant, and nondecreasing, so it defines a finite positive Stieltjes measure and

$$
F_L'(s)=-\int f(x+s)\,dA_L(x)<0,
\qquad |F_L''(s)|\le-\frac1bF_L'(s).
\tag{A.28}
$$

Therefore $U_L''(s)\le(2-s/b)F_L'(s)<0$ on $[0,1]$ whenever $b>1/2$. The measure includes the entry jump, so no derivative of that jump is omitted. A root of the unilateral marginal-profit equation is thus the unique global short magnitude against its candidate schedule.

Existence follows from an interval sign change. Let $\Psi(r,v)=U_L'(v;1,-v)$ with the derivative taken in the deviating magnitude while the candidate schedule is held fixed; recomputing the schedule as $v$ varies makes $\Psi$ continuous on each bracket. Outward interval evaluation proves that $\Psi$ is positive at the left endpoint of each bracket in Proposition 3 and negative at the right endpoint, so the intermediate value theorem places an exact root inside. Throughout each bracket the entry threshold stays strictly between $-v$ and $1$. Writing $v_{j,-}$ and $v_{j,+}$ for the endpoints of the bracket at $r_j$, the enclosures completing the sign tests are

$$
\begin{aligned}
\Psi(r_{\mathrm a},v_{\mathrm a,-})&\ge0.000000000114>0,&
\Psi(r_{\mathrm a},v_{\mathrm a,+})&\le-0.000000000096<0,\\
\Psi(r_{\mathrm b},v_{\mathrm b,-})&\ge0.000000000123>0,&
\Psi(r_{\mathrm b},v_{\mathrm b,+})&\le-0.000000000121<0,\\
\Psi(r_{\mathrm c},v_{\mathrm c,-})&\ge0.000000000172>0,&
\Psi(r_{\mathrm c},v_{\mathrm c,+})&\le-0.000000000242<0.
\end{aligned}
\tag{A.29}
$$

A uniform derivative bound establishes optimality for the high-value investor. For any bounded residual $A_H\in[0,\Delta_T]$ the Laplace kernel satisfies $f''=(f-\delta_0)/b^2$ in the sense of distributions, so

$$
F_H''(s)=\frac{F_H(s)-A_H(s)}{b^2}\quad\text{a.e.},\qquad
|U_H''(s)|\le L_U:=\frac{2\Delta_T}{b}+\frac{\Delta_T}{b^2}.
\tag{A.30}
$$

On the mesh $s_j=j/n$, interval arithmetic bounds $U_H'(s_j)$ uniformly over the whole root bracket, not only at a floating-point midpoint. Every untested magnitude lies within $1/(2n)$ of a mesh point, so

$$
\inf_{s\in[0,1]}U_H'(s)
\ge\min_j\underline{U_H'(s_j)}-\frac{L_U}{2n}>0.
\tag{A.31}
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
\tag{A.32}
$$

Constant-posterior tails integrate as exponentials. Interval arithmetic applied to these expressions encloses the root tests, the derivative cover (A.31), and the entry probabilities in Proposition 3. The no-trade margins are positive at the same strengths, and the entry enclosures are disjoint and ordered upward. This is a computer-assisted existence proof in the sense of Online Appendix B, which specifies the outward interval arithmetic on exact decimal inputs, the parameter brackets, the endpoint ordering, and every regularity argument needed to replicate it.


### A.5 The seller's continuation problem {#pa-design}

Let $\mathcal E(p,r)$ denote the set of trading, pricing, and preparation continuations after reserve $p$. For a continuation $\sigma\in\mathcal E(p,r)$, write $e_H(p,r;\sigma)$ and $e_L(p,r;\sigma)$ for conditional entry. Expected seller revenue is

$$
\mathcal R_T(p,r;\sigma)
=t_0(p,r)+\frac12\sum_{\theta\in\{H,L\}}e_\theta(p,r;\sigma)
[t_\theta(p,r)-t_0(p,r)].
\tag{A.33}
$$

A seller equilibrium specifies a feasible continuation after every reserve, including deviations from the chosen reserve. Given a selection $\sigma^*(p)\in\mathcal E(p,r)$, its reserve satisfies

$$
p^*\in\arg\max_{p\in[0,h]}\mathcal R_T(p,r;\sigma^*(p)).
\tag{A.34}
$$

Existence of a feasible selection and attainment of the maximum require separate arguments. The optimistic and pessimistic envelopes of the continuation set are not automatically the seller's objective. In the atomless-value extension, the feasible reserve domain extends to the upper endpoint $h+\varepsilon_V$; equation (A.34) describes the binary-value benchmark.

#### Payoffs over the reserve domain

For a realized challenger value $v$, the sale rule gives

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
\tag{A.35}
$$

For $p<\ell$, the benchmark closed forms apply. If $\ell<p<r$, the low-value challenger cannot meet the reserve: $t_L=t_0$, $g_L=0$, $t_H=r/2+p^2/(2r)$, and $g_H=h-t_H$. If $r\le p<h$, then $t_0=t_L=g_L=0$, $t_H=p$, and $g_H=h-p$. A reserve above $h$ prevents a sale. Equality at a value atom follows the admissibility convention in Section 2. For atomless acquisition values, integrate the realized sale rule over each conditional value distribution, including when the reserve cuts through a value band.

#### Local revenue decomposition

On a differentiable continuation branch with atomless preparation costs and $0<p<\ell$, let $\mathsf E=(e_H+e_L)/2$. Differentiating seller revenue gives

$$
\frac{d\mathcal R_T}{dp}
=(1-\mathsf E)\left(1-\frac{2p}{r}\right)+\mathsf E\frac p r
+\frac12\sum_\theta\frac{de_\theta}{dp}(t_\theta-t_0).
\tag{A.36}
$$

The first two terms hold entry fixed. The last term accounts for the change in participation. If $H_C$ is the cost CDF with density $h_C$, and $\mu_\theta(z;p)$ is the posterior reached in state $\theta$ at noise realization $z$, then

$$
\frac{de_\theta}{dp}
=\int f(z)h_C(B_{p,r}(\mu_\theta))
\left[-\frac p r+(g_H-g_L)\frac{d\mu_\theta(z;p)}{dp}\right]dz.
\tag{A.37}
$$

The term $-p/r$ is the direct effect on acquisition profit. The posterior derivative captures the change in information generated by equilibrium trading. It vanishes locally when orders remain fixed at their bounds, but can be nonzero when orders adjust. Online Appendix A.10 states sufficient regularity and domination conditions. These are local decompositions, with no general sign restriction on the information term. At an atomic preparation threshold or a nonregular continuation, use the level objective and complete conditional laws.

The reserve sweep in Online Appendix C.6 records continuations found under the declared searches. It does not prove existence at unresolved reserves, exhaust the correspondence, or establish a global seller optimum. Characterizing seller-optimal terms, their commitment timing, and whether they preserve the entry reversal remains open.

### A.6 Numerical parameters {#pa-parameters}


The benchmark parameter vector is

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.25,1,6,2,0.02),\\
(r_0,r_1,r_2)&=(1.2,3,3.6).
\end{aligned}
\tag{A.38}
$$

The moderate-value vector is

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(2,1,0.5,0.25,0.3,0.89,2,0.002),\\
(r_0,r_1)&=(1.05,1.5).
\end{aligned}
\tag{A.39}
$$

For complementary signals I use

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.85,1,7.14,2,0.015),\\
(r_0,r_1,a,d)
&=(1.1,2.3,0.70,0.75).
\end{aligned}
\tag{A.40}
$$

The atomless-cost half-width is $\varepsilon_C=$ 0.1 and the atomless-value half-width is $\varepsilon_V=$ 0.05. These are separate experiments. Online Appendix C defines the exact input values, the derived quantities, their formatting, and the acceptance criteria behind every number reported in the text.
