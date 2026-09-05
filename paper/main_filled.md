---
title: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders"
author: "Austin Li"
date: ""
bibliography: references.bib
link-citations: true
abstract: |
  A stronger acquirer can attract its own challenger. I study a listed target whose prospective buyer learns from the stock price before paying for acquisition diligence. A stronger incumbent lowers the challenger's profit from acquiring at every belief, but it makes target shareholders' proceeds more sensitive to the challenger's quality, and that sensitivity is what informed investors trade on. Against a weak incumbent the spread is too small to support informed trading and the price says nothing. Against a strong one, trading is informative, favorable prices bring the challenger in, and the better challenger owns the target more often. Holding the information in prices fixed, the usual deterrence returns. At intermediate strengths, informative equilibria with asymmetric trading coexist with the uninformative one. The mechanism survives smooth noise, spread-out preparation costs, and a buyer whose own signal is more accurate than the market's. At fixed competitive strength, access to prices raises acquisition surplus net of diligence, and a bargaining comparison shows that runner-up pricing is the payment property behind discovery. I close by setting up the seller's problem when sale terms determine both what a buyer pays and what the market reveals about who should bid.
---

## 1. Introduction {#sec-introduction}

Where does takeover competition come from? Before a prospective acquirer can submit a bid it can live with, it has to spend money finding out what the target is worth to it. Lawyers read contracts, bankers build models, operating people visit plants. A company that has not done this work is not a bidder in any meaningful sense, however interested it may be. The decision to do the work is made under uncertainty, and it is made in the shadow of whoever is already at the table. A powerful rival makes the investigation less attractive. It lowers the chance of winning and, when the challenger does win, it raises the price. That is the deterrence logic of @Fishman1988 and @HirshleiferPng1989, and it is the natural first guess about what a strong incumbent does to the buyer pool.

This paper argues that the first guess can be wrong, and for a reason that has nothing to do with the incumbent being weak in disguise. The same rival that makes investigation less rewarding makes the target's stock more informative about whether investigation is worthwhile. When a prospective buyer can read that stock price before committing to diligence, a stronger incumbent can recruit the very challenger it would otherwise deter.

The setting I have in mind is a publicly visible, still contestable sale of a listed company. A lead buyer is prepared to bid. A second prospective buyer has expressed interest but has not paid for the diligence that would let it submit an executable offer. Target shares trade during that interval. Merger proxies routinely describe such phases. Imprivata's definitive proxy, for instance, records an unsolicited approach, deliberation over who else might buy, confidential outreach, and indications of interest that were explicitly conditional on further diligence, alongside worries about disruption and leakage [@Imprivata2016]. @BooneMulherin2007 and @GentryStroup2019 document how much of takeover competition is decided before the public bidding stage. I use the Imprivata record to motivate the separation between an expression of interest and a costly commitment to participate, not as evidence that its stock price caused anyone to enter.

Which features of the sale determine whether a stronger incumbent deters or attracts a challenger? And what does the challenger actually learn from the price? To study these questions, I develop a model that joins a corporate control contest to a financial market in which prices are rational and traders anticipate the real decisions their orders influence. A seller commits to a cash second-price auction with a reserve. An incumbent bidder is already prepared; its value for the target is drawn from a distribution whose strength is the comparative-static primitive. A potential challenger is either a good match or a poor one. It does not know which until it pays a privately realized preparation cost, low with some probability and high otherwise, after which it learns its value and can bid. Before that decision, an investor who knows the challenger's quality trades the target's shares against noise demand, paying a linear trading cost. Competitive market makers observe order flow and set the price equal to the expected terminal value of a share, anticipating both the challenger's entry decision and the auction. The challenger sees the price, not the flow, and then decides whether to prepare.

The main insight is that competition reallocates the returns to information between the buyer who might acquire the company and the trader who holds its shares, and that this reallocation can reverse entry deterrence. I establish three results.

1. Strengthening the incumbent, in the sense of first-order stochastic dominance, weakly raises the sensitivity of target proceeds to the challenger's quality and weakly lowers the challenger's expected acquisition profit at every belief about its quality. Both movements come from the same sale rule.

2. On a nonempty open set of primitives, a weak incumbent leaves the market silent. The unique equilibrium has no informed trading, an uninformative price, and challenger entry equal to the probability of a low preparation cost, $\rho$. A strong incumbent turns informed trading on. The unique equilibrium has full correctly signed orders, an informative price, entry strictly above $\rho$, and a strictly higher probability that a high-quality challenger ends up owning the target. I solve both economies allowing mixed orders and every continuous deviation. At still stronger incumbents entry falls back to $\rho$, because the noise in order flow bounds how favorable a price can ever look, and beyond some strength no price is favorable enough to justify the expensive preparation cost.

3. Between the silent and the fully informed regions, informative equilibria with asymmetric trading exist alongside no trade. The investor buys as much as it can after good news but sells only part of its capacity after bad news, and entry rises with incumbent strength along this branch. I establish these equilibria by interval arithmetic that encloses an exact solution rather than by a floating-point residual, and the enclosures are tight enough to order entry across the certified strengths.

The mechanism is easiest to see by separating two returns. The return to acquiring the company is what the challenger keeps after paying for it. The return to trading its shares is what an informed investor earns from knowing the challenger's quality before the market does. In a second-price sale the winner pays the runner-up's willingness to pay, so the target's proceeds when the challenger is a good match exceed its proceeds when the challenger is a poor match by exactly the amount by which the incumbent's value exceeds the poor match's value, when it does. A stronger incumbent puts more probability on that event. Its own value moves into the range where the challenger's quality changes what shareholders receive, so the spread of target proceeds across challenger types widens. The same movement shrinks what a good challenger keeps, because it now pays more. Competition transfers part of the challenger's acquisition advantage into the target's sale price, and that transfer is what an informed trader can trade on.

Rational pricing does not undo the effect, but it does discipline it. The market maker knows that a favorable price will bring the challenger in and prices the entry response. What remains profitable to trade on is only the difference between the high- and low-quality outcomes after that response has been priced, scaled by the probability that the buyer enters. With a weak incumbent that residual is smaller than the trading cost at every belief the market could hold, so no order is worth placing and the price says nothing. With a strong incumbent the residual exceeds the trading cost at every belief, and I show that the informed investor's marginal profit is positive over the whole order interval, so it trades to its limit. The price then carries information, and on the favorable tail it crosses the threshold at which even a high-cost challenger finds preparation worthwhile. Acquisition profit falls at every fixed belief throughout this comparison. Entry rises because the information the market supplies changes.

The distinction between a changing information experiment and a fixed one is the core of the paper. If I freeze the investor's orders at their informative level and vary the incumbent, the usual deterrence logic returns and entry falls with strength. What overturns deterrence is that the experiment itself is endogenous to competition. This is why the intermediate region matters. There the investor's two-sided problem has interior solutions, buying fully after good news and shorting partially after bad news, and the resulting experiment is neither silent nor fully revealing. It is also why the effect eventually dies. Order flow noise with bounded likelihood ratios caps how informative any price can be, and once the expensive challenger needs more optimism than any price can deliver, the market keeps trading but the challenger stops coming.

The mechanism does not depend on the particular assumptions I use to make it tractable. It survives smooth logistic noise in place of the two-sided exponential, atomless preparation costs in place of two cost levels, acquisition values that differ by a factor of two rather than ten, and, most importantly for how one should read the model, a buyer whose own private signal about the match is more accurate than the trader's. In that extension the price is complementary information for a well-informed buyer, not a substitute for its judgment. The buyer still uses the increment in the price, and a stronger incumbent still raises entry.

Discovery also has real consequences. Holding competition fixed, giving the challenger access to the price raises expected target proceeds and raises acquisition surplus net of preparation costs, because every additional entrant the price attracts is one who has judged the acquisition worth its cost. A comparison with a verifiable-value bargaining institution isolates the payment property behind all of this. What matters is that the winner's payment is disciplined by the runner-up's value. When the seller instead captures much of the winner's own value, stronger competition need not make the target claim more sensitive to challenger quality at all. That observation reframes sale design. A seller choosing a reserve changes what an entrant pays, and it also changes whether investors have a reason to reveal the information that brings entrants in. I formulate that problem, show that a higher reserve can raise proceeds in a diagnostic economy with atomless values by turning on informative trading against a weak incumbent, and leave its full solution as the next result.

The paper is closest in spirit to @DowGoldsteinGuembel2017, where a firm's real investment decision shapes the incentive to produce information in its stock. I share the feedback from real decisions to information incentives but study a different object, the division of acquisition rents between a traded claim and a buyer deciding whether to enter, and I derive the opposite movements in those returns from the mechanics of a takeover auction. @EdmansGoldsteinJiang2015 show that corrective real decisions can discourage trading on bad news even under rational pricing; here rival strength changes the information sensitivity of the claim and the set of willing acquirers. Their evidence that prices affect takeover activity [@EdmansGoldsteinJiang2012] establishes the direction from prices to control, although a takeover triggered by undervaluation is not a challenger learning its match. @Luo2005 studies learning from announcement returns in completion decisions; my participation decision comes before the buyer set is fixed. @GentryStroup2019 and @LevinSmith1994 make entry into auctions an economic object, and @RobertsSweeting2013 show how selective entry shapes the choice of sale procedure. I keep the direct deterrence force these papers rely on and add the market information available before investigation. @Persico2000 studies how auction formats shape bidders' incentives to acquire information; in my setting the informed party is not a bidder, and the claim it trades is not the entrant's profit.

On the market side, @BettonEtAl2014 analyze negotiations with stock-market feedback and the relation between run-ups and offer prices, and @LinMaYangZhu2025 model payment choice and trading in the merging firms within an initiated deal. I study who shows up in the first place, under cash consideration. @CornelliLi2002 show how arbitrageurs' positions affect tendering; my investor knows something about a prospective buyer and does not determine tendering. Recent auction-information work sharpens the boundary. @PernoudGleyze2026 study bidders learning about their own values and their competitors, @LiuBernhardt2022 use post-auction market feedback in security-payment design, and @CarlinEtAl2026 study bidder-pool choice with correlated values. My market operates before participation, and the sale payment determines what an outside investor has an incentive to reveal. Toeholds and takeover free riding [@BulowHuangKlemperer1999; @GrossmanHart1980] are absent by construction, since the investor holds no control rights and the sale binds the whole company; manipulation through real decisions [@GoldsteinGuembel2008] would enter only once the trader's own information acquisition is endogenous.

Section 2 sets up the model. Section 3 derives the two returns to competition and states Proposition 1. Section 4 works out what the challenger learns from the price and why the price is enough. Section 5 contains the main results, Propositions 2 and 3, the benchmark numbers, and the full map of equilibria across incumbent strengths. Section 6 examines robustness and the buyer who knows more than the trader. Section 7 asks what discovery is worth to the target and which payment property produces it. Section 8 turns to sale design, Section 9 to what an empirical study would have to measure, and Section 10 concludes. Appendix A collects the supporting results and proofs; the online appendix contains complete arguments, the interval certificates, and the numerical contract behind every reported number.

## 2. The model {#sec-model}

### 2.1 Values, preparation, and the sale

I normalize the target's known standalone value to zero and measure acquisition values and preparation costs per target share. Adding the same standalone component to every ownership outcome shifts prices and payoffs by a constant and changes no incentive. The informed order is measured in a small reference trading unit, not as a claim on the whole company.

Two potential acquirers face the target. The incumbent is an available acquirer that has already done its preparation and knows its value $R$, drawn uniformly on $[0,r]$. The distribution is conditional on public information at the start of the sale process, and raising $r$ is a first-order stochastic strengthening. The incumbent is not the target's management, and it incurs no further participation cost.

The challenger is a prospective competing acquirer, not an activist shareholder. Its value is $\theta\in\{\ell,h\}$ with equal prior probabilities, and I impose

$$
0<p<\ell<r<h.
\tag{1}
$$

The challenger begins without knowing $\theta$. After observing the target's price it privately learns its preparation cost $C$, equal to $c_L$ with probability $\rho$ and $c_H$ otherwise, with $0<\rho<1$ and $0\le c_L<c_H$. Paying the cost reveals the acquisition value and permits participation. Declining means the challenger is absent from the sale. Preparation is sunk before bidding. Incumbent value, challenger value, preparation cost, and noise demand are mutually independent.

The seller commits publicly, before trading begins, to a cash second-price auction with reserve $p$. The highest admissible bidder acquires the target and pays the larger of the reserve and the highest competing bid; without an admissible bid there is no sale. I implement truthful, weakly dominant bidding. Conditional on the competing bid, a bidder wants to win exactly when its value covers the payment required to win, and its own bid cannot lower that payment conditional on winning. A bid equal to the reserve is admissible, and acquisition-value ties have no effect in the interior benchmark. A challenger that is exactly indifferent about preparing prepares. That convention is harmless almost everywhere but matters at one boundary of the analysis, where the posterior sits on a plateau with positive probability.

### 2.2 Trading, prices, and timing

The investor observes $\theta$ and submits an order $q\in[-1,1]$. It has no initial position, cannot bid for the target, and pays a linear cost $k|q|$ with $k>0$. Its profit is

$$
q\{V_T-P(X)\}-k|q|,
\qquad X=q+Z,
\qquad f(z)=\frac{1}{2b}e^{-|z|/b},\quad b>1,
\tag{2}
$$

where $V_T$ is the terminal payoff of a target share and $Z$ is independent noise demand with the two-sided exponential (Laplace) density $f$. The Laplace law has one property I use repeatedly, a likelihood ratio between any two feasible orders that is bounded above and below, and it delivers closed forms for everything the challenger needs to compute. Section 6 replaces it by the logistic law, which has the same bounded log-density slope, and shows that nothing of substance changes.

Competitive market makers observe aggregate order flow $X$ and set

$$
P(X)=\mathbb E[V_T\mid X],
\tag{3}
$$

anticipating both the challenger's preparation decision and the auction. The challenger observes $P$, not $X$. This is the informational restriction that makes the price the object of study. The buyer reads a price, not a tape.

The sequence is as follows. The sale opportunity and its rule are announced. The investor learns $\theta$ and trades. Market makers price aggregate demand. The challenger observes the price and its cost, decides whether to prepare, and learns its value if it does. Bidders submit truthful bids, ownership changes if there is an admissible bid, and financial payoffs are realized.

### 2.3 Equilibrium

An equilibrium consists of conditional probability distributions $\sigma_H,\sigma_L$ over orders, a measurable price function, Bayesian beliefs based on the observed price, optimal preparation for each cost realization, and truthful bidding. The investor optimizes over the entire order interval, and I allow it to mix. A unilateral deviation holds the equilibrium pricing and preparation schedules fixed while changing the distribution of order flow that reaches them. A comparison across values of $r$, by contrast, re-solves the whole equilibrium, including the schedules. Keeping these two exercises apart is what separates a fixed information experiment from an endogenous one, and much of Section 5 turns on the difference.

I write $t_0$ for expected target proceeds without entry, $t_H$ and $t_L$ for proceeds conditional on entry by a high- or a low-value challenger, and $g_H$ and $g_L$ for the challenger's gross acquisition profits. The payoff spread is $\Delta_T=t_H-t_L$, and $B_r(\mu)$ denotes gross challenger profit at posterior $\mu$. The posterior bounds are $m$ and $M$; the belief at which an expensive challenger is willing to prepare is $\tau$, and $x^*$ is the order flow at which the belief reaches $\tau$. Favorable-flow probabilities conditional on quality are $\alpha_H$ and $\alpha_L$. Total entry is $\mathsf E$, the probability that a high-quality challenger acquires the target is $\mathsf O_H$, and expected target revenue is $\mathcal R_T$. Three boundaries on incumbent strength, $r_N$, $r_U$, and $r_C$, mark where no trade stops being an equilibrium, where full orders become the unique outcome, and where expensive entry becomes infeasible.

## 3. Competition and the two returns to information {#sec-payoffs}

Start with the auction itself, before any trading. A high-value challenger wins and pays $\max\{p,R\}$. Against a low-value challenger the winner pays $\max\{p,\min(R,\ell)\}$. Without a challenger the incumbent pays the reserve exactly when its value meets it. Integrating over the uniform incumbent gives

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

At a posterior $\mu$ that the challenger is a good match, its gross profit from preparing is a weighted average of the two conditional profits, and the derivatives that matter are

$$
\begin{aligned}
B_r(\mu)&=g_L+\mu(g_H-g_L),\\
\Delta_T'(r)&=\frac12-\frac{\ell^2}{2r^2}>0,\\
g_H'(r)&=-\frac12+\frac{p^2}{2r^2}<0,
\qquad g_L'(r)=-\frac{\ell^2-p^2}{2r^2}<0.
\end{aligned}
\tag{5}
$$

So $\partial B_r(\mu)/\partial r<0$ at every fixed posterior, while the spread $\Delta_T$ rises with $r$. The decline in acquisition profitability and the increase in the sensitivity of target proceeds are two consequences of the same payment rule, and neither depends on the uniform distribution. The next result states the general version.

**Proposition 1 (competition and the two returns to information).** *Let the incumbent's value have a continuous distribution $F$ on $[0,\bar r]$ with $0<p<\ell<\bar r<h$, and extend $F$ by unity above its support. A first-order stochastic strengthening of $F$ weakly increases the spread of target proceeds between a high- and a low-value challenger and weakly decreases the challenger's gross acquisition profit at every fixed posterior, where*

$$
\Delta_T(F)=\mathbb E_F[(R-\ell)_+]
=\int_\ell^{\bar r}[1-F(u)]\,du,
\qquad
G_\theta(F)=\mathbb E_F[(\theta-\max\{p,R\})_+]
=\int_p^\theta F(u)\,du.
\tag{6}
$$

*Both comparisons are strict when the change in $F$ has positive integral over the corresponding range.*

The proof is in Appendix A, and it is short because the result is a statement about payments, not about beliefs. Fix a realization $R$ of the incumbent's value. If $R\le\ell$, the target receives the same amount whether the challenger is a good match or a poor one, because either type outbids the incumbent and pays the same competing bid. If $R>\ell$, a good match pays $R$ while a poor match loses and the incumbent pays $\ell$. The difference in target proceeds is therefore $(R-\ell)_+$, realization by realization. Its expectation is the survival integral in equation (6), and a stronger incumbent, having a smaller distribution function, has more mass in the region where the challenger's quality matters to shareholders. That is the first return to information: the claim that an investor can trade becomes more sensitive to what the investor knows.

The profit integrand moves the other way for the same reason. The challenger keeps $\theta-\max\{p,R\}$ when that is positive, so its expected profit is the integral of $F$ over $[p,\theta]$. Shifting mass upward lowers $F$ pointwise and shrinks the integral. What the challenger loses when the incumbent is stronger is exactly what the target gains in the states where quality matters. Competition does not create information; it moves the return to information from the buyer who would act on it to the shareholders who own the claim, and a fixed-posterior average of the two profit integrals inherits the ordering.

This opposition is worth dwelling on because it is the whole reason the rest of the paper can go the way it does. Deterrence works through $B_r(\mu)$, since at any belief a stronger incumbent makes preparation less attractive. Discovery works through $\Delta_T$, since at any level of trading a stronger incumbent makes the target's shares a better bet for someone who knows the challenger. Which force wins depends on whether the second is large enough to change what the market reveals, and that is a question about equilibrium, taken up in Sections 4 and 5.

<!-- FIGURE 2: figures/two_returns.pdf -->
> **Figure 2.** The two returns to competition at the benchmark specification ($h=10$, $\ell=1$, $p=0.5$, $b=2$), with all other primitives fixed and values measured per target share. Panel (a) plots the information spread of target proceeds, $\Delta_T(r)=(r-\ell)^2/(2r)$, against incumbent strength $r$. Panel (b) plots the challenger's gross acquisition profit $B_r(\mu)$ at the lowest attainable belief $\mu=m$, the prior $\mu=1/2$, and the highest attainable belief $\mu=M$. A stronger incumbent raises what an informed trader can earn from knowing the challenger's quality while lowering what the challenger can earn from acquiring the target at every belief.

Figure 2 draws the two functions under the benchmark parameters used throughout the paper. Panel (a) shows the spread $\Delta_T(r)$ starting from zero at $r=\ell$, where the incumbent never outbids a poor match and the challenger's quality never reaches shareholders, and rising without bound as the incumbent strengthens. Panel (b) shows $B_r(\mu)$ declining in $r$ at each of the three beliefs the analysis will use. The vertical distance between the top and bottom lines is how much the most favorable attainable belief adds to expected acquisition profit relative to the least favorable one, and it is that distance, set against a fixed preparation cost, that will make the challenger's entry decision responsive to the price.

## 4. Learning from prices {#sec-inference}

The challenger cannot see the order flow, only a price that competitive market makers have set knowing how the challenger will react. Two questions have to be answered before anything can be said about equilibrium trading. How much can any pattern of informed trading move the market's belief? And does a price computed by rational market makers reveal that belief to the challenger? This section answers both; the exact statements are Propositions A.1 and A.2 in Appendix A.

Take any mixed strategies $\sigma_H$ and $\sigma_L$ over orders in $[-1,1]$. Order flow has conditional densities and a posterior

$$
\begin{aligned}
a_H(x)&=\int f(x-q)\,d\sigma_H(q),\quad
a_L(x)&=\int f(x-q)\,d\sigma_L(q),\\
\mu_X(x)&=\frac{a_H(x)}{a_H(x)+a_L(x)},\qquad
m=\frac1{1+e^{2/b}},\quad M=1-m,
\end{aligned}
\tag{7}
$$

and the posterior lies in $[m,M]$ whatever the investor does. The reason is the shape of the noise. For any two feasible orders $q$ and $q'$, the triangle inequality gives

$$
e^{-2/b}\le\frac{f(x-q)}{f(x-q')}\le e^{2/b},
\tag{8}
$$

so no realization of order flow can be more than $e^{2/b}$ times as likely under one quality as under the other. Integrating over the mixed strategies preserves the bounds, and equal priors turn them into $[m,M]$. Because the price is a function of order flow, the belief based on the price is a conditional expectation of $\mu_X$ and lives in the same interval. This bound is the reason the strong-incumbent result in Section 5 eventually undoes itself. However much the investor trades, the market can never be more than a fixed amount more optimistic than the prior, and a challenger whose preparation cost requires more optimism than $M$ delivers will never enter.

Now suppose that the low-cost challenger always finds preparation worthwhile, that is, $c_L<B_r(m)$, so that entry has a positive floor at every feasible price. This is a mild restriction in the applications I have in mind. It says only that a cheap opportunity is worth investigating even after the worst news the market can deliver. At a price-based belief $\mu$, a challenger with cost $C$ prepares exactly when $C\le B_r(\mu)$. Averaging over the cost, entry and the competitive price can be written as

$$
\begin{aligned}
e_r(\mu)&=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\\
P_r(\mu)&=t_0+e_r(\mu)[t_L-t_0+\Delta_T\mu].
\end{aligned}
\tag{9}
$$

The price has a transparent structure. Without entry, shareholders receive $t_0$. Entry adds the low-quality increment $t_L-t_0$ for certain and the additional spread $\Delta_T$ with probability $\mu$. Both the entry probability and the bracket are nondecreasing in $\mu$, and the bracket is strictly increasing because $t_L\ge p>t_0$, so $P_r$ is strictly increasing in the belief. It jumps upward where the expensive challenger starts to enter, but it never goes down.

That monotonicity is what makes the price sufficient for the buyer. Write $e(P)$ for entry averaged over the cost realization. Conditional pricing implies

$$
P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X],
\qquad
\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T},
\tag{10}
$$

and the denominator is positive because entry has a floor and the spread is positive. The market's belief is therefore a measurable function of the price, and conditioning it again on the price leaves it unchanged. The challenger, who sees only $P$, recovers exactly what a market maker who saw $X$ believed. Nothing is lost by hiding the tape. This uses the independence of incumbent value and preparation cost from trading; it does not require the challenger to see order flow, and it does not require the price function to be differentiable or even continuous.

The last object is the one the investor cares about. Subtract the price from the terminal value a share is worth to someone who knows the challenger is a good match, and reverse the subtraction for a poor match. The residual advantages of an informed buyer of shares in state $H$ and an informed short seller in state $L$ are

$$
\begin{aligned}
A_H(x)&=\mathbb E[V_T\mid H,x]-P(x)=e_r(\mu_X(x))\Delta_T[1-\mu_X(x)],\\
A_L(x)&=P(x)-\mathbb E[V_T\mid L,x]=e_r(\mu_X(x))\Delta_T\mu_X(x),\\
\rho m\Delta_T&\le A_H(x),A_L(x)\le\Delta_T.
\end{aligned}
\tag{11}
$$

This identity is the core feedback calculation of the paper, and it is worth reading slowly. A publicly anticipated increase in acquisition proceeds cancels from the informed trader's profit. If the market already expects entry and already expects the entrant to pay more, the price reflects it and there is nothing to earn. What remains is the state-dependent component that noise trading prevents the market maker from identifying, namely the entry probability times the spread times the market's remaining uncertainty about which state it is in. Both bounds in equation (11) are independent of the investor's strategy. The lower bound comes from the entry floor $\rho$ and the belief floor $m$; the upper bound is the spread itself. Everything in Section 5 follows from comparing these two bounds with the trading cost $k$. If even the upper bound falls short of $k$, no informed trade is ever profitable and the price is silent. If the lower bound exceeds $k$ by enough to cover the way an order shifts the noise, informed trade is profitable at every belief the market could hold, and the investor trades to its limit.

## 5. Competition creates competition {#sec-results}

### 5.1 The entry reversal

I can now put the two returns of Section 3 and the inference of Section 4 together. The result is the paper's central claim. Strengthening the incumbent lowers the challenger's acquisition profit at every belief, and yet it can raise the probability that the challenger enters, because it changes what the challenger learns before deciding.

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

The proof is in Appendix A, with the full measure-theoretic argument in Online Appendix A. Here I explain why the result holds, because the logic is the economics of the paper.

The three conditions describe an economy in which some opportunities are always worth investigating, some are worth investigating only after good news, and information is expensive enough to produce in the weak economy but cheap enough in the strong one. Condition (A1) says that the low preparation cost is covered even at the most pessimistic belief a price can ever induce. Condition (A2) says that the high preparation cost is not covered at the prior when the incumbent is weak, but is covered at the most optimistic belief when the incumbent is strong. Condition (A3) is the trading wedge. It compares the trading cost $k$ with the largest residual profit an informed trader can earn in the weak economy and the smallest marginal profit the trader can earn in the strong one. None of the three conditions says that rivalry raises acquisition profit. Equation (5) says it lowers it.

The argument runs in a short sequence. First, whatever the investor does, beliefs based on the price stay inside $[m,M]$, because the likelihood ratio of any two feasible orders is bounded by the tail behavior of the noise. Second, condition (A1) means that the inexpensive challenger prepares at every price, so entry is at least $\rho$ on every path. That floor is what makes the price sufficient for the buyer's decision and leaves the trader a residual profit of at least $\rho m\Delta_T$ per unit traded. Third, in the weak economy even the largest possible residual, $\Delta_T(r_0)$, falls short of $k$, so any nonzero order loses money against any candidate price schedule. The market is silent, beliefs stay at the prior, and by (A2) only the cheap challenger prepares. Fourth, in the strong economy the residual is large enough that increasing a correctly signed order is profitable at every magnitude and against every candidate schedule, so the trader buys the maximum after good news and sells the maximum after bad news. Finally, the informative price crosses the expensive challenger's threshold with positive probability, so entry exceeds $\rho$ and the better challenger owns the target more often.

The fourth step deserves a closer look, because it is what makes the strong-economy outcome unique rather than merely an equilibrium. Fix any candidate equilibrium and its residual schedules $A_H$ and $A_L$. A trader who has seen good news and buys $s$ units earns

$$
F_H(s)=\int f(x-s)A_H(x)\,dx,
\qquad F_L(s)=\int f(x+s)A_L(x)\,dx,
\qquad U_\theta(s)=sF_\theta(s)-ks.
\tag{12}
$$

The Laplace density satisfies $|f'|\le f/b$, so shifting the order changes the convolution by at most a fraction $1/b$ of itself. Differentiating gives

$$
U_\theta'(s)\ge\left(1-\frac{s}{b}\right)F_\theta(s)-k
\ge\left(1-\frac1b\right)\rho m\Delta_T-k>0
\tag{13}
$$

almost everywhere. The bound holds for every candidate schedule at once, which is why mixed orders and interior deviations cannot support any other outcome. This is a stronger statement than a first-order condition at a conjectured profile. It says that against anything the market could be pricing, a larger correctly signed order is better.

With full orders in place, the rest is arithmetic. Writing $\tau$ for the belief at which the expensive challenger is indifferent and $x^*$ for the order flow that produces it,

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

Condition (A2) places $\tau$ strictly between $1/2$ and $M$ and therefore $x^*$ strictly between $0$ and $1$. The probability $\alpha_H$ that a good challenger generates a flow above the threshold exceeds the probability $\alpha_L$ that a poor one does, so the additional entry is tilted toward the challenger the target wants.

Part (iii) is the other side of the same coin. Beliefs based on prices can never exceed $M$, whatever the investor does. Once the incumbent is strong enough that even the belief $M$ does not cover the high preparation cost, the expensive challenger stays out on every path. Trading remains informative and full, but it no longer moves anyone across a threshold, and entry falls back to $\rho$. Entry therefore rises and then falls as the incumbent gets stronger. The rise is not an artifact of the two points I picked in (i) and (ii). It is what happens when information first becomes worth producing and later stops being able to clear the bar.

### 5.2 The benchmark economy

Appendix A.4 lists the primitive vector I use for the benchmark. The weak incumbent has $r_0=1.2$, the strong incumbent $r_1=3$, and the collapse strength of part (iii) is $r_2=3.6$. Strengthening the incumbent from $r_0$ to $r_1$ lowers the challenger's gross profit at the prior from 4.804167 to 4.291667 and raises the information spread of target proceeds from 0.016667 to 0.666667. Entry nevertheless rises from 0.250000 to 0.522757 and falls back to 0.250000 at $r_2$. The probability that the high-value challenger ends up owning the target rises from 0.125000 to 0.324192.

<!-- TABLE 1: tables/table1_auction_primitives.tex -->
> **Table 1.** Auction primitives at the benchmark specification for the weak ($r=1.2$) and strong ($r=3$) incumbent economies, per target share. Expected target proceeds without entry ($t_0$) and with a high- or low-value challenger ($t_H$, $t_L$), the challenger's gross acquisition profits ($g_H$, $g_L$), the information spread $\Delta_T=t_H-t_L$, and gross profit at the prior belief $B_r(1/2)$. The closed forms in (4) are checked against direct integration of the realized sale rule; Online Appendix C.1 gives the procedure.

<!-- TABLE 2: tables/table2_equilibrium_controls.tex -->
> **Table 2.** Equilibrium outcomes and information controls at the benchmark. Panel (a) reports the validated equilibrium at the weak, strong, and collapse strengths (Laplace noise, cost atoms): orders $q_H,q_L$, total entry $\mathsf E$, the probability of high-quality ownership $\mathsf O_H$, and target proceeds $\mathcal R_T$. Panel (b) reports three controls. The frozen profile imposes full orders at both strengths and lets the buyer reoptimize; it is not an equilibrium at the weak strength and is reported as a control. The price-hidden economy reoptimizes trading and pricing while the buyer uses the prior. The matched-dividend economy adds a deterministic payment to the traded claim in the price-hidden economy so that mean prices coincide with the feedback economy. Panel (c) reports the fixed-strength gains from access to prices in target proceeds and in allocation value net of paid preparation costs. Online Appendix C.1 defines every column.

Table 1 collects the auction primitives and Table 2 the equilibrium outcomes. Two features of the strong and collapse economies are worth noticing. In the strong economy the threshold flow $x^*$ lies strictly inside the unit interval, so the expensive challenger enters after favorable flow and stays out otherwise. In the collapse economy trading is still full, but the belief the expensive challenger needs lies above $M$ and no flow reaches it; the price is informative, but it informs nobody who can act on it.

### 5.3 Holding the information experiment fixed

It is tempting to read the reversal as "informative prices raise entry." That reading is wrong, and Table 2 shows why. Suppose the informed trader placed full orders at both strengths, so that the price is equally informative in the weak and the strong economy, and let the buyer reoptimize against that fixed information. Entry then falls from 0.562178 to 0.522757. Holding the signal fixed, a stronger incumbent lowers gross profit at every belief, so every belief-cost pair that entered before still enters only if profit remains above cost. Entry can only fall. Proposition A.3 in Appendix A states this monotonicity for any fixed joint distribution of the signal, the challenger's quality, and the preparation cost.

Removing access to prices produces the same entry at both strengths, 0.250000 and 0.250000, because the buyer then acts on the prior and only the cheap challenger prepares. The comparison isolates what drives the reversal. It is neither the level of information nor the strength of the incumbent alone. It is that the incumbent's strength changes which information experiment the market runs. In the weak economy the experiment is silent, in the strong economy it speaks, and the buyer's response to a speaking market outweighs the direct deterrence that the frozen control measures. The frozen profile is not an equilibrium in the weak economy, since the trader would rather not trade at all, which is precisely the point. The informative experiment has to be paid for by someone, and a weak incumbent does not make it worth paying for.

### 5.4 The equilibrium correspondence

Proposition 2 compares two, or three, strengths. What happens in between is richer, and I compute it rather than assume it away. Figure 1 plots every equilibrium branch found and validated on a fine grid of strengths at the benchmark primitives.

<!-- FIGURE 1: figures/equilibrium_correspondence.pdf -->
> **Figure 1.** The equilibrium correspondence at the benchmark primitives (Laplace noise, cost atoms). Panel (a) plots total entry $\mathsf E$ against incumbent strength $r$ for every accepted branch: no trade, full orders, the asymmetric family $(q_H,q_L)=(1,-v)$ traced by numerical continuation, and a symmetric interior family $(u,-u)$. Shaded regions are the strengths where uniqueness is established analytically, no trade below $\mathfrak r(k)$ and full orders above $r_U$. The dotted verticals mark $r_N$, the exact boundary of no-trade existence, $r_U$, the sufficient boundary for full-order uniqueness, and $r_C$, beyond which expensive entry is infeasible. The three certified equilibria of Proposition 3 carry interval enclosures; the bars are drawn even where they are too narrow to see. Panel (b) plots the unfavorable-state order magnitude $v$ along the asymmetric branch and $u$ along the symmetric interior branch, with full orders at $1$. Lines are broken at unresolved nodes and at branch changes, and a branch that does not appear at a strength is a branch the search did not find, not a uniqueness claim. Online Appendix C.2 specifies the grid, the searches, and the validation.

Three boundaries organize the picture, and each answers a different question. Write $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$ for the strength at which the information spread equals $d$, that is, $\Delta_T(\mathfrak r(d))=d$. Against a silent market a correctly signed order of size $s$ earns $s(\rho\Delta_T/2-k)$, so no trade is an equilibrium exactly when $\rho\Delta_T(r)/2\le k$, that is, when $r\le r_N=\mathfrak r(2k/\rho)$. Below $\mathfrak r(k)$ the spread itself is smaller than the trading cost, so no order is profitable against any price schedule and no trade is the only outcome. Above $r_U=\mathfrak r(k/[(1-1/b)\rho m])$ the marginal-profit bound (13) holds against every schedule and full orders are the only outcome. Finally, the belief $M$ is the most optimistic belief any price can carry, and the strength $r_C$ at which $B_r(M)=c_H$ is the last strength at which the expensive challenger can be brought in by any equilibrium. In the benchmark these boundaries are $r_N=1.747877538$, $\mathfrak r(k)=1.220997512$, $r_U=2.837416964$, and $r_C=3.592658519$. Proposition A.4 in Appendix A states these characterizations and their domain. I keep them separate on purpose. The exact existence boundary $r_N$ is not the strength at which informative trading appears, and a sufficient uniqueness boundary is not a boundary at which anything happens to the economy.

Reading Figure 1 from left to right, no trade is the only branch below $\mathfrak r(k)$ and remains available up to $r_N$. Well before $r_N$, informative equilibria appear. The first to appear are asymmetric. The trader buys the full amount after good news but sells only part of the way after bad news, and the magnitude $v$ of the short rises with the incumbent's strength until it reaches one. Along this branch entry rises even though acquisition profit falls at every belief, which is the reversal again, now inside the correspondence rather than across two isolated points. When $v$ reaches one the asymmetric branch merges into full orders, at a strength below $r_N$, so from there to $r_N$ full orders coexist with no trade. Just above $r_N$, where no trade stops being an equilibrium, the computation finds a second informative family in which both trader types place small orders of equal size in opposite directions. Prices are informative on that branch, but the posterior never reaches the expensive challenger's threshold, so entry stays at $\rho$. That family disappears a little further along, and from there full orders are the only branch the search finds, well before $r_U$ makes uniqueness a theorem. At $r_C$ the expensive challenger drops out and entry falls to $\rho$ while trading stays full. Under Laplace noise the top belief $M$ is reached on a whole tail of flows, so the equality at $r_C$ is not a null event; I keep the convention that an indifferent challenger enters, which is why entry at $r_C$ itself is the left limit rather than $\rho$.

Figure 1 establishes less than it might appear to, and the distinctions matter. The shaded regions are theorems. The certified points of Proposition 3 are exact equilibria enclosed in intervals. Everything else, including the asymmetric branch between the certified points, the symmetric interior family, and the location of every branch change, is a numerical continuation. Each plotted point is a candidate profile that passed the full set of unilateral-deviation, pricing, and entry checks at the stated tolerances, and the searches include pure, asymmetric, and finite-support mixed profiles. A branch that is absent at a strength was not found, which is not the same as not existing. The mixed-strategy searches found no mixed equilibrium at any strength, and I report that as a search outcome, not as a proof. The complete intermediate correspondence remains an open characterization, and I return to it in Section 10.

### 5.5 Coexisting informative equilibria

The asymmetric branch is the part of Figure 1 that a two-point comparison would miss entirely, and it changes how one should think about the reversal. On that branch prices are informative, entry exceeds $\rho$, and the economy also admits no trade. Competition does not force information out of the market at intermediate strengths. It makes information possible. I establish three points on the branch exactly.

**Proposition 3 (coexisting informative equilibria at intermediate strength).** *At the benchmark primitives of Appendix A.4, there exist equilibria $(q_H,q_L)=(1,-v_j)$ at strengths $r_j$ whose certified enclosures are*

$$
\begin{aligned}
r_{\mathrm a}&=1.55,&v_{\mathrm a}&\in[0.46031618,\,0.46031620],&\mathsf E_{\mathrm a}&\in[0.5450528898,\,0.5450528922],\\
r_{\mathrm b}&=1.60,&v_{\mathrm b}&\in[0.70747537,\,0.70747539],&\mathsf E_{\mathrm b}&\in[0.5487563062,\,0.5487563085],\\
r_{\mathrm c}&=1.65,&v_{\mathrm c}&\in[0.90333198,\,0.90333201],&\mathsf E_{\mathrm c}&\in[0.5513607988,\,0.5513608020].
\end{aligned}
\tag{15}
$$

*The entry intervals are strictly ordered upward. Each of the three economies also admits no trade with entry $\rho$.*

Existence here is established by verified interval computation rather than by a pen-and-paper proof. Appendix A.3 reports the enclosures that complete the argument and Online Appendix B gives the method. The logic is the following. Against its own price schedule, the trader who has seen bad news faces a strictly concave problem, because the residual it trades against is bounded and nondecreasing in the order flow. Its best short is therefore the unique root of a marginal-profit equation, and an equilibrium on this branch is a fixed point in which the conjectured short $v$ equals that root. Interval arithmetic with exact antiderivatives shows that the marginal profit is strictly positive at one end of each bracket in (15) and strictly negative at the other, with every rounding error accounted for, so an exact root lies inside. For the trader who has seen good news the problem is not concave, and I instead bound its marginal profit from below on a fine mesh over the whole bracket, correct for what can happen between mesh points using a Lipschitz constant, and verify that the bound is positive. The favorable trader therefore buys the maximum. Wrong-signed trades lose money outright. The result is a proof whose arithmetic was done by a machine, and I label it that way.

Why does the trader buy fully after good news but only partly after bad news? The asymmetry comes from the buyer's response. After favorable flow the expensive challenger is close to entering, and each additional unit bought pushes the price posterior toward the threshold at which entry jumps; the residual profit of a buyer is large exactly where the jump happens. After unfavorable flow the expensive challenger is already out, so further selling moves the posterior along a flat part of the entry schedule and earns only the fundamental spread. Selling has a smaller marginal return, and the trader stops before the bound. As the incumbent gets stronger the spread grows, the return to selling rises, and $v$ moves toward one. That is the continuation Figure 1 traces.

Why does entry rise along the branch when profits are falling? Because the market's experiment is improving faster than acquisition profits deteriorate. A larger short after bad news makes good news more distinguishable from bad news, so the favorable flows that induce the expensive challenger to enter become more likely conditional on a good challenger. The certified entry intervals in (15) are disjoint and ordered, which is the cross-economy comparison the branch supports at these three points. Between them the branch is a numerical continuation, and I do not read a derivative off it.

Why does no trade survive alongside these informative equilibria? Because at these strengths $\rho\Delta_T/2\le k$: against a silent market, a single trader who deviates to a small order earns the fundamental spread times the entry floor, and that is not enough to cover the trading cost. Informative trading is self-supporting once it is in place, because it changes the buyer's behavior and thereby the residual profit, but nobody has a unilateral reason to start it. This multiplicity is not an inconvenience. It is the sense in which competition creates the conditions for information without guaranteeing it.

## 6. Robustness and richer information {#sec-extensions}

The mechanism does not depend on the sharp features of the benchmark, the Laplace noise with its flat posterior tails, the two preparation-cost atoms, the wide gap between the challenger's possible values, or the assumption that the investor knows more than the buyer. I relax each in turn.

### 6.1 Smooth noise and atomless preparation costs

Replace the Laplace noise by logistic noise with density

$$
f_{\mathrm{log}}(z)=\frac{1}{4b}\operatorname{sech}^{2}\left(\frac z{2b}\right),\qquad b>1.
\tag{16}
$$

The derivative of the log density is bounded by $1/b$ in absolute value, which is all the global trading argument used, so Proposition 2 holds unchanged under (A1) to (A3); Proposition A.5 in Appendix A states the result. What changes is the shape of the price experiment. Under full logistic orders the posterior is strictly increasing in the order flow and approaches the bounds $m$ and $M$ only in the limit, instead of sitting on them over whole tails. With $A=e^{1/b}$ and $w=\sqrt{\tau/(1-\tau)}$,

$$
x^*_{\mathrm{log}}=b\log\frac{Aw-1}{A-w},\qquad
\alpha_H^{\mathrm{log}}=\frac1{1+e^{(x^*_{\mathrm{log}}-1)/b}},\qquad
\alpha_L^{\mathrm{log}}=\frac1{1+e^{(x^*_{\mathrm{log}}+1)/b}}.
\tag{17}
$$

In the strong benchmark economy, logistic noise gives entry 0.301509 against 0.522757 under Laplace noise. The order-flow threshold is 5.424598398, which is 1.495369 standard deviations of the noise from its center. The two laws share the same posterior bounds at the same scale parameter, but they put very different mass near those bounds. Under Laplace noise the top belief is reached on a positive-probability tail, so a challenger with a threshold just below $M$ still enters often. Under logistic noise the same threshold is crossed only by extreme flows. Figure 3 makes this comparison directly.

<!-- FIGURE 3: figures/posterior_tail_entry.pdf -->
> **Figure 3.** The upper tail of price information under full orders at the strong benchmark strength and scale $b=2$. Panel (a) plots $\Pr(\mu_X\ge\tau)$ against the threshold distance $M-\tau$ for Laplace and logistic noise. Panel (b) plots the implied total entry $\rho+(1-\rho)\Pr(\mu_X\ge\tau)$. At $M-\tau=0$ the Laplace plateau enters under the tie rule, so its mass is positive (filled marker), while the logistic mass is zero because the bound is never attained (open marker). These are information-experiment comparisons at a fixed order profile; Online Appendix C.5 records, for each threshold, whether the corresponding economy with the implied high preparation cost is a validated equilibrium. Scale, not variance, is held fixed, and the comparison is not a liquidity or Blackwell ordering between the laws.

I resist the temptation to summarize Figure 3 as one law being more informative than the other. The two experiments are not Blackwell ordered, and holding the scale parameter fixed is not the same as holding variance fixed. What the figure shows is where the mass sits. The Laplace experiment concentrates favorable evidence in a plateau at the top belief, and the logistic experiment spreads it out. For a challenger whose threshold is near the top of the feasible range, that difference decides whether prices bring it in.

Atomless preparation costs work the same way as atoms once the conditions are restated for the supports. Let the low and high costs be drawn from atomless distributions with probabilities $\rho$ and $1-\rho$, supported within $[c_L-\varepsilon_C,c_L+\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$. If

$$
\begin{gathered}
c_L-\varepsilon_C\ge0,\qquad c_L+\varepsilon_C<B_{r_1}(m),\\
B_{r_0}(1/2)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{r_1}(M),
\end{gathered}
\tag{18}
$$

and (A3) holds, then every low-cost realization prepares at every feasible belief, every high-cost realization stays out at the weak prior, and every high-cost realization prepares after sufficiently favorable strong-economy prices. The entry rule becomes the cost distribution evaluated at gross profit, which is continuous and nondecreasing in the belief with a positive floor, and that is all the price construction needs. Proposition A.6 in Appendix A states the result under either noise law. In the strong benchmark economy with the cost half-width of Appendix A.4, entry is 0.522715 under Laplace noise and 0.301374 under logistic noise, slightly below the values with cost atoms.

### 6.2 Moderate acquisition values

The benchmark uses a wide gap between the challenger's possible values. That is a convenience, not a requirement. With $h=2$ and $\ell=1$, the moderate-value specification of Appendix A.4 satisfies every strict inequality of Proposition 2, and entry rises from 0.250000 to 0.526805 between its weak and strong strengths.

The general argument is short. At $r=\ell$ the profit gap between a good and a poor challenger is $h-\ell$, so the gap between the profit at the top belief and at the prior is $(M-1/2)(h-\ell)$, which is positive for any $h>\ell$. Choosing the strong strength close enough to $\ell$ keeps the top-belief profit above the prior profit, and choosing the weak strength closer still makes the weak spread smaller than the fraction $(1-1/b)\rho m$ of the strong spread. A trading cost strictly between those two spreads and a high preparation cost strictly between the two profits then satisfy (A2) and (A3), and any positive low cost below the floor satisfies (A1). All the inequalities are strict, so they survive small perturbations. Appendix A gives the construction and Online Appendix C.4 reports it numerically for several value ratios. The lesson is that the reversal is about where the strengths sit relative to the challenger's low value, not about how dramatic the challenger's upside is.

### 6.3 A buyer who knows more than the market

A natural objection to the benchmark is that it gives the investor knowledge of the challenger's value while the challenger itself knows nothing. That is not the interpretation I have in mind. The information relevant to a takeover is dispersed. A buyer knows its own technology and integration capacity; investors who follow the target know its customers and product market. Diligence combines the two. To capture this, I give the trader and the buyer different noisy signals and let the buyer's signal be the more accurate one.

Let $T,Y\in\{+,-\}$ be conditionally independent given the challenger's quality, with

$$
\Pr(T=+\mid H)=\Pr(T=-\mid L)=a,\qquad
\Pr(Y=+\mid H)=\Pr(Y=-\mid L)=d,
\qquad a,d\in(1/2,1).
\tag{19}
$$

The trader observes $T$; the buyer observes $Y$ and the price before preparing, and diligence still reveals the exact value before bidding. Writing $\lambda_X=\Pr(T=+\mid X)$ for the market's belief about the trader's signal, the public belief about quality and the buyer's joint posteriors are

$$
\begin{aligned}
\mu_X&=(1-a)+(2a-1)\lambda_X,\quad
\mu_-=(1-a)+(2a-1)m,\quad \mu_+=(1-a)+(2a-1)M,\\
\phi_+(\mu)&=\frac{d\mu}{d\mu+(1-d)(1-\mu)},\qquad
\phi_-(\mu)&=\frac{(1-d)\mu}{(1-d)\mu+d(1-\mu)}.
\end{aligned}
\tag{20}
$$

The new element is that the buyer's private signal makes entry depend on the state even conditional on the price. Write $w_H=t_H-t_0$ and $w_L=t_L-t_0$ and let $I_y=\mathbf1\{B_r(\phi_y(\mu))\ge c_H\}$ indicate expensive entry after private signal $y$. Then

$$
\begin{aligned}
e_H&=\rho+(1-\rho)[dI_++(1-d)I_-],\\
e_L&=\rho+(1-\rho)[(1-d)I_++dI_-],\\
D&=e_Hw_H-e_Lw_L,\qquad
\rho\Delta_T\le D\le\Delta_T+(1-\rho)(2d-1)w_H.
\end{aligned}
\tag{21}
$$

A good challenger enters more often than a poor one at the same price, because its buyer is more likely to have seen a favorable private signal. The market maker cannot use a common entry rate. Competitive pricing becomes

$$
P=t_0+e_L(P)w_L+\mu_XD(P),\qquad
\mu_X=\frac{P-t_0-e_L(P)w_L}{D(P)},
\tag{22}
$$

and the price still reveals the public belief, because the coefficient $D$ is bounded away from zero. The buyer combines that belief with its own signal. The trader's residual profits after a favorable and an unfavorable signal become

$$
A_+=(2a-1)(1-\lambda_X)D,
\qquad A_-=(2a-1)\lambda_XD.
\tag{23}
$$

These are the benchmark residuals scaled by the trader's own informativeness $2a-1$ and by a spread $D$ that now includes the state-dependent entry response. Proposition A.7 in Appendix A gives the exact conditions, the analogues of (A1) to (A3) in which the buyer's most pessimistic joint posterior $\phi_-(\mu_-)$ replaces $m$, the buyer's favorable private posterior at the prior, $d$, replaces $1/2$ in the weak-economy exclusion, and the trading wedge is scaled by $2a-1$. Under those conditions the weak economy has unique zero orders and entry $\rho$, the strong economy has unique full orders by trader signal and entry above $\rho$, and both conclusions allow arbitrary mixed signal-contingent orders and every continuous deviation. Nothing in the argument requires $a\ge d$.

The example uses buyer accuracy 75\% and trader accuracy 70\%. The buyer's private signal is the more accurate one, and entry still rises from 0.850000 to 0.879438. In the weak economy even a favorable private signal does not justify expensive preparation; in the strong economy the favorable private signal combined with a favorable price does. The price adds something the buyer does not have, which is the incremental information in the market's signal, and that increment is what the stronger incumbent makes worth producing. Table 3 collects the robustness results.

<!-- TABLE 3: tables/table3_extensions.tex -->
> **Table 3.** Extensions and information complementarities. Each row is a separate economy solved from its own primitive vector; entry $\mathsf E$ and the probability of high-quality ownership $\mathsf O_H$ are reported at the weak and strong strengths together with the smallest of the five strict margins that support the analytical result. Panel (a) crosses Laplace and logistic noise with cost atoms and the uniform cost mixture at the benchmark. Panel (b) reports the moderate-value specification. Panel (c) reports the complementary-signal economies for a grid of trader and buyer accuracies $(a,d)$; the declared example is marked, and rows outside the region where every margin in Proposition A.7 is positive are validated equilibria without the analytical uniqueness label. Online Appendix C.1, C.3, and C.4 define the columns.

## 7. What discovery is worth {#sec-welfare}

### 7.1 Access to prices and acquisition surplus

Proposition 2 is a statement about who shows up. It does not say whether anyone is better off when the prospective buyer can read the target's price. The answer is not obvious. Informed trading redistributes money from noise traders to the investor, extra entry moves money from bidders to target shareholders, and the challenger pays preparation costs that would otherwise be saved. None of these transfers is a gain by itself. I therefore compare two economies that differ only in whether the buyer sees the price.

Hold the incumbent at the strong strength $r_1$ and every other primitive at the values of Proposition 2. In the first economy the challenger observes the target price before deciding whether to prepare. In the second it cannot, and it decides on the prior. Trading and pricing are reoptimized in both. Proposition A.9 in Appendix A states the result. Access to prices strictly raises expected target proceeds and strictly raises acquisition surplus net of preparation costs, and both statements survive smooth noise and atomless costs.

The comparison is clean because the two economies differ in exactly one thing. A buyer who cannot see the price keeps its prior, and at the prior the expensive opportunity is not worth investigating, so it enters only when its cost happens to be low. The investor's problem, by contrast, is the same in both economies. The trading bound that forces full orders under feedback applies just as well when entry is stuck at $\rho$, because that bound only uses the floor on entry. The investor therefore trades fully in both economies, the order-flow experiment is the same, and the real trading costs are the same. What changes is whether the buyer can use the experiment.

Why does using it create surplus rather than a transfer? Without a challenger, the ownership value of the target is $W_0(R)=R\mathbf1\{R\ge p\}$. With a challenger of value $\theta>p$ it is $W_\theta(R)=\max\{R,\theta\}$. The difference has a simple form,

$$
W_\theta(R)-W_0(R)
=(\theta-\max\{p,R\})_++p\mathbf1\{R<p\}.
\tag{24}
$$

If the incumbent's value is below the reserve, entry replaces no sale with a sale to a buyer worth $\theta$. If it is above, entry improves ownership by $(\theta-R)_+$, which is the challenger's gross acquisition profit. Integrating over $R$, an additional preparation decision taken at posterior $\mu$ and cost $C$ produces conditional expected net surplus $B_r(\mu)-C+p^2/r$. The buyer takes that decision only when $B_r(\mu)-C\ge0$, so every additional entrant adds at least $p^2/r$, the value of sales that would otherwise not have happened. Low-cost entry is unchanged across the two economies. For cost atoms the gains in surplus and in target proceeds are

$$
\begin{aligned}
\Delta\mathcal W&=(1-\rho)\mathbb E\left[
\left(B_r(\mu_X)-c_H+\frac{p^2}{r}\right)\mathbf1\{\mu_X\ge\tau\}\right]>0,\\
\Delta\mathcal R_T&=\frac{1-\rho}{2}
\left[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\right]>0.
\end{aligned}
\tag{25}
$$

Payments among bidders, target shareholders, market makers, and noise traders are transfers in this calculation and drop out. The result is about access to prices at a fixed level of competition. It is not a welfare ranking of weak against strong incumbents, and it is not a ranking of sale rules. I return to the seller's problem in Section 8.

### 7.2 Separating information from price levels

At the strong strength, mean target proceeds are 0.872392 when the buyer sees the price and 0.614583 when it does not. A skeptic could argue that the buyer responds to a higher price level rather than to information. To rule this out I attach a deterministic external dividend of 0.257809 to the traded claim in the price-hidden economy. The competitive price shifts up by exactly that amount, $V_T-P$ is unchanged, and so is every trading residual and every entry decision. The two economies now have the same mean price and the same mean financial payoff, and they still differ in entry. The difference is information, not level. The dividend is a diagnostic. It is not a sale term the seller can offer and it does not count as a resource gain in the surplus calculation.

### 7.3 Which payment property supports discovery

The auction of Section 2 pays the target whatever the strongest competing bid is. Which part of that rule drives the opposition in Proposition 1? To find out I change the institution and keep everything else. Set the reserve to zero. After diligence, values are publicly verifiable and the highest-value buyer acquires the target. A sale to the next-best buyer at its own value is an enforceable fallback, accepted at zero surplus. The seller and the winning buyer then split the winner's surplus above that fallback by Nash bargaining, with the seller receiving share $\eta$. Without a challenger the fallback is zero and the seller receives $\eta R$. For an incumbent distribution on $[0,R_{\max}]$ with $\ell<R_{\max}<h$ and $0\le\eta<1$, the transfer, the challenger's profit, and the information spread of target proceeds are

$$
\begin{aligned}
T_\eta(R,\theta)&=(1-\eta)\min\{R,\theta\}+\eta\max\{R,\theta\},\\
G_{\theta,\eta}&=(1-\eta)\mathbb E[(\theta-R)_+],\\
\Delta_\eta&=\eta(h-\ell)+(1-2\eta)\mathbb E[(R-\ell)_+].
\end{aligned}
\tag{26}
$$

Proposition A.8 in Appendix A records the comparative statics. A stronger incumbent weakly reduces challenger profits at every $\eta$, as in the auction. The spread behaves differently. It rises with competition for $\eta<1/2$, does not respond to competition at $\eta=1/2$, and falls with competition for $\eta>1/2$.

The mechanics are worth spelling out. Suppose the incumbent's value exceeds $\ell$. If the challenger turns out to be worth $h$, it wins and pays $(1-\eta)R+\eta h$, which rises with $R$ at rate $1-\eta$. If the challenger turns out to be worth $\ell$, the incumbent wins and pays $(1-\eta)\ell+\eta R$, which rises with $R$ at rate $\eta$. A stronger incumbent therefore raises the high-quality payment faster than the low-quality payment exactly when $1-\eta>\eta$. When the seller keeps most of the surplus, the target claim is already close to a claim on the winner's value, and competition adds nothing to how much that claim depends on who the challenger is. When the seller keeps little, the claim is close to the runner-up's value, and a stronger incumbent makes the runner-up matter more precisely when the challenger is good. It is runner-up discipline, the tie between the target's payment and the loser's value, that makes competition raise the information sensitivity of the target's shares. The auction label plays no role.

<!-- FIGURE 4: figures/bargaining_weight.pdf -->
> **Figure 4.** Bargaining weight and the division of information-sensitive returns in the verifiable-value institution with a zero reserve, benchmark values $h=$ 10 and $\ell=$ 1, and uniform incumbents with $r=$ 1.2 (weak) and $r=$ 3 (strong). Panel (a) plots the information spread $\Delta_\eta$ against the seller's bargaining weight $\eta$; the two lines cross at $\eta=1/2$, where competition stops affecting the spread. Panel (b) plots the challenger's expected profits $G_{H,\eta}$ and $G_{L,\eta}$ on a log scale; a stronger incumbent lowers both at every weight. Values are per target share. The figure compares acquisition-stage payoffs only; the trading and entry game under this institution is not solved here.

Figure 4 shows the two forces at the benchmark values. In panel (a) the strong incumbent produces the larger spread to the left of $\eta=1/2$ and the smaller spread to the right, with the two lines crossing exactly at the midpoint. Panel (b) shows challenger profits falling with strength at every weight, so the profit side of Proposition 1 does not depend on the institution at all. The lesson for the design question is direct. An institution that lets competition raise the target's information sensitivity must tie the target's payment to the losing bidder. This is a payment-stage statement about a specified alternative institution. Solving the trading and entry game under it, with the different residual profits that (26) implies, is part of the program in Section 8.

## 8. Sale design as information policy {#sec-design}

### 8.1 The seller's continuation problem

Proposition 2 holds the sale mechanism fixed. That is what makes the result sharp, and it also points at the next question. A seller who chooses sale terms changes what an entrant pays, and it also changes whether investors have a reason to reveal the information that makes entry worthwhile. Which sale rules maximize target proceeds once they are understood to shape the information revealed before participation? How does the answer depend on the incumbent's strength, and does an optimizing seller reinforce the entry reversal or remove it? These are the questions the model makes concrete, and I set them up here without yet answering them.

I begin with a reserve chosen publicly before trading. For every reserve $p$ let $\mathcal E(p,r)$ be the set of trading, pricing, and entry continuations. For a continuation $\sigma\in\mathcal E(p,r)$ write $e_H(p,r;\sigma)$ and $e_L(p,r;\sigma)$ for entry in the two quality states. Seller revenue is

$$
\mathcal R_T(p,r;\sigma)
=t_0(p,r)+\frac12\sum_{\theta\in\{H,L\}}e_\theta(p,r;\sigma)
[t_\theta(p,r)-t_0(p,r)].
\tag{27}
$$

A seller equilibrium has to specify a continuation after every feasible reserve, not only after the one chosen, because the seller's deviations are evaluated against those continuations. Given a selection $\sigma^*(p)\in\mathcal E(p,r)$, the chosen reserve satisfies

$$
p^*\in\arg\max_{p\in[0,h]}\mathcal R_T(p,r;\sigma^*(p)).
\tag{28}
$$

Existence, attainment, and the selection itself are part of the result to be established. The optimistic envelope that picks the best continuation at each reserve and the pessimistic envelope that picks the worst describe the correspondence, but neither is automatically the seller's objective. The strongest comparative-static target is an entry reversal under seller-optimal terms. A characterization of when an optimizing seller instead eliminates the reversal would answer the same design question.

### 8.2 Payoffs over the complete reserve domain

The reliable starting point is the realized sale rule. For a realized challenger value $v$,

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
\tag{29}
$$

Four regimes follow. For $p<\ell$ the closed forms in (4) apply. For $\ell<p<r$ the low-value challenger never meets the reserve, so $t_L=t_0$ and $g_L=0$, while $t_H=r/2+p^2/(2r)$ and $g_H=h-t_H$. For $r\le p<h$ the incumbent never meets the reserve either, so $t_0=t_L=g_L=0$, $t_H=p$, and $g_H=h-p$. A reserve above $h$ prevents any sale. Equality at an acquisition-value atom is evaluated with the admissibility convention of Section 2.

These regimes change the claim investors trade. Excluding the low-value buyer widens the gap between what the target receives when the challenger is good and when it is poor, and it can do so enough to make information valuable even against a weak incumbent. This is why a reserve is an information instrument and not only an extraction instrument. With atomless acquisition values I integrate (29) over the conditional value distribution rather than extending a formula through an exclusion boundary; a reserve that cuts through a value band is handled by the integral, not by a case.

### 8.3 A local extraction-discovery decomposition

On a differentiable continuation branch with atomless preparation costs and $0<p<\ell$, write $\mathsf E=(e_H+e_L)/2$. Differentiating (27) gives

$$
\frac{d\mathcal R_T}{dp}
=(1-\mathsf E)\left(1-\frac{2p}{r}\right)+\mathsf E\frac p r
+\frac12\sum_\theta\frac{de_\theta}{dp}(t_\theta-t_0).
\tag{30}
$$

The first two terms are the familiar reserve trade-off with the entry probability as a weight. The last term is where sale design meets discovery. If the cost distribution has CDF $H_C$ with density $h_C$, and $\mu_\theta(z;p)$ is the posterior reached in state $\theta$ at noise realization $z$, then

$$
\frac{de_\theta}{dp}
=\int f(z)h_C(B_{p,r}(\mu_\theta))
\left[-\frac p r+(g_H-g_L)\frac{d\mu_\theta(z;p)}{dp}\right]dz.
\tag{31}
$$

The first term in the bracket is direct rent extraction. A higher reserve lowers every challenger's gross profit and pushes marginal preparers out. The second term is the change in the information generated by equilibrium trading. On a branch where orders are fixed at their bounds it vanishes locally, because the posterior reached at each noise realization does not move with the reserve. When orders adjust it does not vanish, and its sign is not pinned down. Equations (30) and (31) are local decompositions, not global sign restrictions, and Appendix A gives the regularity they need. At an atomic cost threshold or a nonregular continuation, the level objective (27) is the right object.

### 8.4 A reserve diagnostic with atomless acquisition values

To see the design margin at work I compute a comparison rather than an optimum. Let the challenger's quality indicate a low or a high value class, equally likely. Conditional on class, the acquisition value is uniform on $[\ell-\varepsilon_V,\ell+\varepsilon_V]$ or $[h-\varepsilon_V,h+\varepsilon_V]$ with half-width $\varepsilon_V=$ 0.05. The investor observes the class and nothing more. Preparation reveals the exact value. Raising the reserve from 0.5 to 1.1 raises weak-economy revenue from 0.392665 to 0.432173, and strong-economy revenue from 0.872367 to 1.014500. Under the higher reserve entry is 0.540309 in the weak economy and 0.511638 in the strong one, and trading is informative in both. Each stated trading outcome satisfies the corresponding global bound, so the continuations behind these numbers are the unique ones at those reserves.

<!-- TABLE 4: tables/table4_reserve_comparisons.tex -->
> **Table 4.** Sale terms and discovery. Panel (a) compares the original reserve with the declared alternative at each incumbent strength under binary acquisition values, reporting the trading profile, total entry, target proceeds per share, and the strict bound that supports the stated continuation. Panel (b) repeats the comparison with atomless class values and class-only investor information. Panel (c) summarizes an exploratory sweep over reserves from zero to the highest acquisition value as ranges across the continuations found, with the number of reserves at which several continuations were found and the number left unresolved. The highest found revenue is not an optimum, and a reserve without a found continuation is not an empty equilibrium set. Online Appendix C.6 specifies the computation.

The higher reserve excludes the low-value class from the sale. That is the extraction motive, and by itself it would not make a weak-incumbent economy informative. What the reserve also does is widen the spread between the target's proceeds with a good challenger and with a poor one, which switches informed trading on against the weak incumbent as well. Revenue rises at both strengths for that combined reason. Panel (c) of Table 4 reports what an exploratory sweep over the full reserve domain finds, reserve by reserve, keeping every accepted continuation and flagging the reserves the search could not resolve. I read it as a map of the problem in (28), not as its solution. The profitable alternative identifies a design margin worth optimizing. Its optimization is the next result, and I do not infer any property of the optimum from a two-point comparison.

### 8.5 Open questions

The seller's problem is the first item on the agenda that follows from this paper. I intend to solve it with the complete continuation problem retained at every reserve and with continuous challenger values. The object is an institutional result about how a seller obtains informative participation, and the comparison between a fixed institution and an optimized one decides whether the seller uses, strengthens, or replaces the effect of the incumbent's strength.

The second item is commitment. When does fixing sale terms before trading raise the seller's expected proceeds relative to revising them after observing the price but before preparation? Anticipated repricing changes both the return to revealing information and the return to becoming an informed buyer. That timing has to be solved, not imposed through a price-indexed penalty with a convenient sign.

The third item is the acquisition institution itself. Section 7.3 identifies the payment property to study. In a first-price alternative, bids and expected payments depend on the incumbent's belief about a challenger selected through price-dependent entry, and those beliefs belong inside the auction continuation. Endogenous investor research adds the uninformed trader's incentives, including manipulation through the real decision the price feeds into [@GoldsteinGuembel2008]. Each of these is a different game, not a substitution into the payoff formulas of Section 3.

The fourth item is the middle of the correspondence. The certified points of Proposition 3 are exact anchors, not a branch. Continuation between them must allow changing buy-sell asymmetry and mixed orders, and the conditions for branch existence, local continuation, and multiplicity are open, as is any selection argument where one is economically justified.

## 9. Empirical implications {#sec-program}

The model's decision is not a bid. It is the decision to investigate, taken by a buyer who has not yet committed to the diligence and preparation that a bid requires, during an interval in which the target's shares trade. That is where the empirical work has to start. An empirical entry variable is a decision to investigate or to submit a substantive proposal, not a count of public offers. Incumbent strength has to be measured from information available before the challenger's decision, because the final winning bid is not the initial threat the challenger faced. And the financial information has to precede entry. A relation between target returns and the later arrival of bidders can reflect anticipation of entry as easily as learning from prices, so the first task is to establish the decision interval and its information sets rather than to run a regression across deals.

The pilot in Online Appendix D is built for that task. It selects publicly visible, still-open sale opportunities involving listed targets and reconstructs, from disclosure records, the timing of initial approaches, public visibility, contacts, diligence, substantive proposals, revisions, and final selection. At each event it records what was publicly known at that time, separating later retrospective disclosure from contemporaneous availability. The Imprivata process record shows the shape of what the pilot looks for, an unsolicited approach followed by deliberation over potential buyers and indications subject to further diligence, but a stock price that exists during a confidential negotiation is not enough. The model needs an observable interval in which another buyer could still decide whether to investigate a publicly understood opportunity. The pilot is a design. It does not report a sample, a measured effect, or an instrument, and a targeted causal or structural exercise follows the institutional results rather than preceding them.

## 10. Conclusion {#sec-conclusion}

Competition changes two returns at once. It lowers what a challenger can earn from acquiring the target and raises what an investor can earn from knowing the challenger's quality. I have shown that the second effect can dominate the first, so that a stronger incumbent recruits the very buyer it would ordinarily deter, and that the reversal is a property of the equilibrium information rather than of the auction alone. Holding the information experiment fixed, deterrence returns. Letting the market choose it, entry rises with competition over a certified range and coexists with an uninformative equilibrium in between. The mechanism survives smooth noise, atomless preparation costs, and a buyer whose private signal is better than the market's. At fixed competition, access to prices raises acquisition surplus net of diligence. And the payment property behind all of this is runner-up discipline, not the auction label.

A company is not sold to a fixed list of fully informed buyers. Its sale rules and its stock market decide who becomes an informed, willing buyer. How should the institutions of corporate control be designed once their effect on discovery is taken seriously? That is the question these results make concrete, and it is the one I turn to next.

## References {#references}

::: {#refs}
:::

## Appendix A {#paper-appendix}

### A.1 Supporting results {#pa-results}

The main text states three propositions. The arguments behind them, and the extensions discussed in Sections 4 to 7, rest on the results collected here. Complete proofs are in the Online Appendix; each statement names the section that proves it.

**Proposition A.1 (posterior bounds).** *For arbitrary mixed state-contingent orders on $[-1,1]$, the order-flow posterior $\mu_X$ and the posterior based on the price lie in $[m,M]$, where $a_H$, $a_L$, $\mu_X$, $m$, and $M$ are defined in (7).*

The proof is short. For any feasible orders $q,q'$ the triangle inequality gives $e^{-2/b}\le f(x-q)/f(x-q')\le e^{2/b}$, which is (8). Integrating against $d\sigma_H(q)\,d\sigma_L(q')$ preserves both inequalities, and equal priors turn them into bounds on $\mu_X$. Because the price is a function of $X$, the price posterior is $\mathbb E[\mu_X\mid P]$ and inherits the interval. Online Appendix A.1 and A.3 give the measure-theoretic version.

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
\tag{32}
$$

*No trade is an equilibrium exactly when $\rho\Delta_T(r)/2\le k$, that is, when $r\le r_N$. The stronger restriction $r<\mathfrak r(k)$ guarantees that it is the unique outcome. The restriction $r>r_U$ guarantees unique full orders. Expensive entry is impossible in every equilibrium when $B_r(M)<c_H$. If the equality $B_r(M)=c_H$ has a solution in the specified domain, its unique crossing is*

$$
r_C=\frac{Mh-c_H+\sqrt{(Mh-c_H)^2+M[(1-M)\ell^2-p^2]}}{M}.
\tag{33}
$$

*At $r_C$ the tie rule of Section 2 is retained.*

Under no trade the posterior is $1/2$, entry is $\rho$, and a correctly signed order of size $s$ earns (A.5) below; zero is optimal exactly when the coefficient is nonpositive, which gives $r_N$. The sufficient uniqueness boundary $\mathfrak r(k)$ comes from $\Delta_T<k$, which defeats any nonzero order against every candidate schedule. The full-order boundary $r_U$ comes from the derivative bound (13). The function $B_r(M)$ in (A.6) is strictly decreasing on the auction-support domain, so there is at most one crossing of $c_H$, and (33) selects the larger algebraic root. Under Laplace noise the maximum posterior is attained on the positive-probability tail $x\ge1$, so indifference at $r_C$ is not a null event and the tie rule matters there. Online Appendix A.5 derives the formulas and their domain.

**Proposition A.5 (logistic noise).** *Replace Laplace noise by logistic noise with the density in (16). Under conditions (A1) to (A3), the unique trading outcomes and the entry and ownership comparisons of Proposition 2 remain valid, with the threshold and favorable-flow probabilities given by (17).*

The log-density derivative of the logistic law is bounded in absolute value by $1/b$, which is all the global trading argument uses. Under full orders the posterior is strictly increasing with log odds (A.13) below, spans the open interval $(m,M)$, and reaches every interior threshold with positive probability. Online Appendix A.6 has the inversion.

**Proposition A.6 (atomless preparation costs).** *Replace the cost atoms by atomless low- and high-cost distributions with probabilities $\rho$ and $1-\rho$, supported respectively within $[c_L-\varepsilon_C,c_L+\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$. Suppose the support conditions (18) hold and retain (A3). The conclusions of Proposition 2 hold under either noise law.*

Every low-cost realization participates at every feasible belief, which preserves the residual lower bound. At the weak prior all high-cost realizations stay out; at prices close enough to the upper feasible posterior all of them enter, and that event has positive probability under either noise law. The price construction stays strictly increasing because the cost CDF is nondecreasing. Online Appendix A.6 proves it without assuming a density.

**Proposition A.7 (complementary private signals).** *In the complementary-signal economy of Section 6.3, choose $0<p<\ell<r_0<r_1<h$ and suppose*

$$
\begin{gathered}
c_L<B_{r_1}(\phi_-(\mu_-)),\qquad
B_{r_0}(d)<c_H<B_{r_1}(\phi_+(\mu_+)),\\
(2a-1)\{\Delta_T(r_0)+(1-\rho)(2d-1)w_H(r_0)\}<k\\
<\left(1-\frac1b\right)m(2a-1)\rho\Delta_T(r_1).
\end{gathered}
\tag{34}
$$

*The weak economy has unique zero informed orders and entry $\rho$. The strong economy has unique orders $q(T=+)=1$ and $q(T=-)=-1$, and entry strictly exceeds $\rho$. The conclusions permit arbitrary mixed signal-contingent orders and every continuous unilateral deviation.*

The proof controls public beliefs before imposing any order profile, proves the price inversion with state-dependent entry, and applies the global trading bounds to the residuals (23), which satisfy (A.16) below. In the weak economy even the buyer's favorable private signal is not enough for expensive preparation; in the strong economy that signal together with a favorable price is. Online Appendix A.7 gives the joint conditional laws and the probability formulas.

**Proposition A.8 (bargaining).** *In the verifiable-value institution of Section 7.3, let $R$ have any distribution supported on $[0,R_{\max}]$ with $0<\ell<R_{\max}<h$. For $0\le\eta<1$ the institution generates (26). A first-order stochastic strengthening of the incumbent weakly reduces challenger profits. It weakly increases the target's information spread for $\eta<1/2$, leaves that spread unchanged at $\eta=1/2$, and weakly decreases it for $\eta>1/2$. Strictness follows from a positive integral change in the corresponding payoff function.*

With fallback $z$ and winning value $V>z$, the Nash solution maximizes $(P-z)^\eta(V-P)^{1-\eta}$ on $[z,V]$ and gives $P=z+\eta(V-z)$; the zero-weight endpoint follows by continuity. A challenger wins only if $\theta\ge R$ and keeps $(1-\eta)(\theta-R)$. Subtracting target payments state by state gives a high-low difference of $\eta(h-\ell)$ when $R\le\ell$ and $\eta(h-\ell)+(1-2\eta)(R-\ell)$ when $R>\ell$; taking expectations gives (26), and first-order stochastic dominance applied to the increasing function $(R-\ell)_+$ and the decreasing function $(\theta-R)_+$ gives the signs. Online Appendix A.8 treats the endpoints.

**Proposition A.9 (access to prices).** *Hold $r=r_1$ and all other primitives fixed under the conditions of Proposition 2. Compare the feedback equilibrium with the equilibrium in which the challenger cannot observe the target price, reoptimizing trading and pricing in both. Access to prices strictly increases expected target proceeds and acquisition surplus net of preparation costs. The comparison also holds under Propositions A.5 and A.6.*

In the price-hidden game the buyer's posterior stays at the prior, so entry is $\rho$; the strong trading bound still applies with constant entry, so orders are full in both games and the noise distribution and order magnitudes coincide. Identity (24) gives the pointwise allocation gain, every additional entrant contributes at least $p^2/r$, and averaging over the positive-probability event of additional entry gives the first line of (25). Since $t_H,t_L>t_0$, the second line follows. The dividend argument of Section 7.2 shifts the price by a constant and leaves $V_T-P$ unchanged. Online Appendix A.9 states the coupling and the atomless-cost integral.

### A.2 Proofs of Propositions 1 to 3 {#pa-proofs}

*Proposition 1.* Payments have to be determined before expectations are taken. Without entry the target receives $p\mathbf1\{R\ge p\}$. With a high-quality challenger the challenger wins and pays $\max\{p,R\}$. With a low-quality challenger the target receives $\max\{p,\min(R,\ell)\}$ and the challenger obtains $(\ell-\max\{p,R\})_+$. Truthful bidding is weakly dominant conditional on every competing bid, so none of this depends on a conjectured shading strategy. For the uniform incumbent,

$$
\begin{aligned}
t_H&=\frac1r\left[\int_0^p p\,du+\int_p^r u\,du\right],\\
t_L&=\frac1r\left[\int_0^p p\,du+\int_p^\ell u\,du+\int_\ell^r\ell\,du\right],\\
g_L&=\frac1r\left[\int_0^p(\ell-p)\,du+\int_p^\ell(\ell-u)\,du\right],
\end{aligned}
\tag{A.1}
$$

which evaluate to (4) and differentiate to (5). The distribution-free opposition rests on one observation. If $R\le\ell$, the high and low target payments coincide; if $R>\ell$, they differ by $R-\ell$; hence the difference is $(R-\ell)_+$. Tonelli's theorem applied to the nonnegative indicators gives both integrals in (6). A stronger distribution has a smaller CDF, which raises the survival integral and lowers the profit integral, and positive integral differences make the comparisons strict. A weighted average at a fixed posterior preserves the profit ordering. Online Appendix A.2 gives the measure formulation.

*Proposition 2.* The argument runs through six steps, each of which I sketch; Online Appendix A.1 to A.4 supply the conditional-probability versions, the null-set invariance under deviations, and the convolution regularity.

First, beliefs are bounded under every trading strategy. Positivity of $f$ makes every conditional flow density positive, and integrating (8) gives $m\le\mu_X\le M$; the price posterior obeys the same bound by conditional expectation. Because $g_H$ and $g_L$ both fall with $r$, condition (A1) gives $c_L<B_r(m)$ in both economies.

Second, the buyer's actual information can be recovered. The low-cost type enters at every feasible price, so entry is at least $\rho$ and (10) has a positive denominator. The posterior is therefore measurable with respect to the price and $\Pr(H\mid P)=\mu_X$ almost surely. Subtracting conditional payoffs yields the residuals (11). This uses the independence of $R$ and $C$ from trading, not an assumption that the buyer sees order flow.

Third, every nonzero order is eliminated in the weak economy. A correctly signed order of size $s>0$ earns at most $s[\Delta_T(r_0)-k]<0$, and a wrong-signed order has negative gross payoff and still pays its cost. Zero is therefore the only best response against every candidate equilibrium, including mixed ones. Under zero orders $\mu_X=1/2$, and (A1) and (A2) give entry $\rho$; constant pricing constructs the equilibrium.

Fourth, the entire order interval is controlled in the strong economy. For a bounded residual $A$, the translation formula

$$
F(s_2)-F(s_1)
=\int_{s_1}^{s_2}\int \partial_u f(x\mp u)A(x)\,dx\,du
\tag{A.2}
$$

follows from the fundamental theorem for the absolutely continuous density and Fubini, since the absolute double integral is at most $\|A\|_\infty|s_2-s_1|\|f'\|_1$. Thus $F$ is absolutely continuous with $|F'|\le F/b$ almost everywhere, (11) gives $F\ge\rho m\Delta_T$, and differentiating $U=sF-ks$ under (A3) yields (13). Integrating the positive lower bound on the derivative shows that the full correctly signed order strictly dominates every smaller magnitude; wrong signs are dominated by zero. Every equilibrium therefore has full correctly signed orders, and mixing cannot introduce another optimal action.

Fifth, the informative equilibrium exists. Full orders give

$$
\mu_X(x)=\left[1+\exp\left\{-\frac{|x+1|-|x-1|}{b}\right\}\right]^{-1}.
\tag{A.3}
$$

Defining entry and price by (9), the strict monotonicity of $P_r(\mu)$ gives a measurable inverse on its image, including across its upward jump. The buyer recovers the posterior from the price, prepares optimally, and bids truthfully. The bounds above verify investor optimality and market-maker pricing.

Sixth, the comparisons follow. Since $B_r$ increases in $\mu$ and decreases in $r$, condition (A2) places $\tau$ in $(1/2,M)$ and $x^*$ in $(0,1)$, and the Laplace survival function evaluated at $x^*-1$ and $x^*+1$ gives $\alpha_H$, $\alpha_L$, and the entry and ownership formulas in (14). The favorable event has positive probability. Ignoring the strong-economy price reproduces the uninformative experiment, while no state-independent transformation of a constant experiment can reproduce a nonconstant state-dependent law, so the strong experiment strictly Blackwell dominates the weak one. Strict margins make the region open.

For part (iii), the low-cost floor and the derivative bound at $r_2$ give unique full orders exactly as in the fourth and fifth steps, while $B_{r_2}(M)<c_H$ excludes every expensive entrant because $M$ is the largest attainable belief, so entry returns to $\rho$. Two facts about the boundary $r_C$ are worth recording. Under full Laplace orders $\mu_X=M$ on $x\ge1$, an event of positive probability, and the tie rule admits expensive entry at $r_C$ on that event. As $r$ approaches $r_C$ from below,

$$
\mathsf E(r)\longrightarrow\rho+\frac{1-\rho}{4}(1+e^{-2/b}),
\tag{A.4}
$$

whereas strictly above $r_C$ expensive entry is impossible. Under logistic noise the posterior reaches $M$ only in the limit, so expensive entry converges to zero continuously. Online Appendix A.5 has the derivations, together with the no-trade deviation payoff

$$
s\left(\frac{\rho\Delta_T(r)}2-k\right)
\tag{A.5}
$$

and the ceiling profit

$$
B_r(M)=Mh-\frac{Mr}{2}+\frac{(1-M)\ell^2-p^2}{2r}
\tag{A.6}
$$

used in Proposition A.4.

*Proposition 3.* The proof is computer-assisted and is laid out in the next subsection.

### A.3 The certified equilibria {#pa-certificate}

Fix $(q_H,q_L)=(1,-v)$ with $0<v<1$. Bayes' rule gives $\mu_v(x)=\operatorname{logistic}((|x+v|-|x-1|)/b)$, which ranges from $m_v=(1+e^{(1+v)/b})^{-1}$ to $M_v=1-m_v$. In the certified region $1/2<\tau<M_v$, and

$$
x^*(r,v)=\frac{b\operatorname{logit}(\tau)+1-v}{2},\qquad
\mathsf E(r,v)=\rho+\frac{1-\rho}{2}
\left[1-\frac12e^{(x^*-1)/b}+\frac12e^{-(x^*+v)/b}\right].
\tag{A.7}
$$

The unfavorable type's problem is globally concave. Its residual $A_L=e(\mu_v)\Delta_T\mu_v$ is bounded, nonconstant, and nondecreasing, so it defines a finite positive Stieltjes measure and

$$
F_L'(s)=-\int f(x+s)\,dA_L(x)<0,
\qquad |F_L''(s)|\le-\frac1bF_L'(s).
\tag{A.8}
$$

Therefore $U_L''(s)\le(2-s/b)F_L'(s)<0$ on $[0,1]$ whenever $b>1/2$. The measure includes the entry jump, so no derivative of that jump is omitted. A root of the unilateral marginal-profit equation is thus the unique global short magnitude against its candidate schedule.

The root is exact, not a small residual. Let $\Psi(r,v)=U_L'(v;1,-v)$ with the derivative taken in the deviating magnitude while the candidate schedule is held fixed; recomputing the schedule as $v$ varies makes $\Psi$ continuous on each bracket. Outward interval evaluation proves that $\Psi$ is positive at the left endpoint of each bracket in Proposition 3 and negative at the right endpoint, so the intermediate value theorem places an exact root inside. Throughout each bracket the entry threshold stays strictly between $-v$ and $1$. Writing $v_{j,-}$ and $v_{j,+}$ for the endpoints of the bracket at $r_j$, the enclosures completing the sign tests are

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

Every smaller purchase by the favorable type is excluded as well. For any bounded residual $A_H\in[0,\Delta_T]$ the Laplace kernel satisfies $f''=(f-\delta_0)/b^2$ in the sense of distributions, so

$$
F_H''(s)=\frac{F_H(s)-A_H(s)}{b^2}\quad\text{a.e.},\qquad
|U_H''(s)|\le L_U:=\frac{2\Delta_T}{b}+\frac{\Delta_T}{b^2}.
\tag{A.10}
$$

On the mesh $s_j=j/n$, interval arithmetic bounds $U_H'(s_j)$ uniformly over the whole root bracket, not only at a floating-point midpoint. Every untested magnitude lies within $1/(2n)$ of a mesh point, so

$$
\inf_{s\in[0,1]}U_H'(s)
\ge\min_j\underline{U_H'(s_j)}-\frac{L_U}{2n}>0.
\tag{A.11}
$$

The certified global lower margins at the three strengths are 0.0000761777, 0.0027531948, and 0.0054921767. The favorable type therefore chooses its maximum purchase, and all wrong-signed trades have negative gross profit and are dominated by zero.

The integrals are elementary. Split each convolution at $-v$, $x^*$, $1$, and the deviation center. On the central region put $c=(1-v)/2$ and $t=e^{(x-c)/b}$, so that $\mu_v=t^2/(1+t^2)$. The primitives of $e^{x/b}(1-\mu_v)$, $e^{-x/b}(1-\mu_v)$, $e^{x/b}\mu_v$, and $e^{-x/b}\mu_v$ are respectively

$$
b e^{c/b}\arctan t,\quad
b e^{-c/b}(-t^{-1}-\arctan t),\quad
b e^{c/b}(t-\arctan t),\quad
b e^{-c/b}\arctan t.
\tag{A.12}
$$

Constant-posterior tails integrate as exponentials. Interval arithmetic applied to these expressions encloses the root tests, the derivative cover (A.11), and the entry probabilities in Proposition 3. The no-trade margins are positive at the same strengths, and the entry enclosures are disjoint and ordered upward. This is a computer-assisted existence proof in the sense of Online Appendix B, which specifies the outward interval arithmetic on exact decimal inputs, the parameter brackets, the endpoint ordering, and every regularity argument needed to replicate it.

Two further formulas from the extensions are used above. Under full logistic orders the posterior log odds are

$$
2\log\cosh\left(\frac{x+1}{2b}\right)
-2\log\cosh\left(\frac{x-1}{2b}\right),
\tag{A.13}
$$

with derivative positive and limits $-2/b$ and $2/b$. At the continuous limit $r=\ell$ of the nonemptiness construction,

$$
B_\ell(M)-B_\ell(1/2)=(M-1/2)(h-\ell)>0,
\tag{A.14}
$$

so a strength $r_1$ close enough to $\ell$ has $B_{r_1}(M)>B_\ell(1/2)$, a strength $r_0\in(\ell,r_1)$ close enough to $\ell$ has $\Delta_T(r_0)<(1-1/b)\rho m\Delta_T(r_1)$, and $k$, $c_H$, and $c_L$ can be chosen strictly inside the resulting intervals for any $h>\ell$. In the complementary-signal economy the price coefficient satisfies

$$
D=e_L\Delta_T+(e_H-e_L)w_H,
\quad 0\le e_H-e_L\le(1-\rho)(2d-1),
\tag{A.15}
$$

the residuals obey

$$
m(2a-1)\rho\Delta_T\le A_+,A_-
\le(2a-1)[\Delta_T+(1-\rho)(2d-1)w_H],
\tag{A.16}
$$

and at the strong strength the convolution argument gives

$$
U'(s)\ge(1-1/b)m(2a-1)\rho\Delta_T(r_1)-k>0,
\tag{A.17}
$$

which is what makes full signal-contingent orders necessary against every candidate schedule.

### A.4 Numerical primitives {#pa-parameters}

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

For complementary signals I use

$$
\begin{aligned}
(h,\ell,p,\rho,c_L,c_H,b,k)
&=(10,1,0.5,0.85,1,7.14,2,0.015),\\
(r_0,r_1,a,d)
&=(1.1,2.3,0.70,0.75).
\end{aligned}
\tag{A.20}
$$

The atomless-cost half-width is $\varepsilon_C=$ 0.1 and the atomless-value half-width is $\varepsilon_V=$ 0.05. These are separate experiments. Online Appendix C defines the exact input values, the derived quantities, their formatting, and the acceptance criteria behind every number reported in the text.
