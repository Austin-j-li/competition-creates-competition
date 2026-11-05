# Q2. Discrete microstructure: the sell-only menu, with an independent check of the buy-only menu

Memo to the author. Supervisor point 2 (discrete trading menu). 21 October 2026.

Status labels follow the paper: **analytical** (proved here, derivation shown), **numerical diagnostic** (computed by the scripts in Section 5), **conjecture**, **open**.

---

## 1. Question and reading

The supervisor asks whether the microstructure can be discrete, as in Edmans, Goldstein and Jiang (2015; "EGJ" below), with one trading direction shut off, so that off-path order flows are easy to handle.

This memo studies the **sell-only** menu $q\in\{-1,0\}$: purchases are shut off. The investor holds no shares, so a sale is a short sale. In the supervisor's words, this menu "shuts off the long".

- Leading case: noise $z\in\{-1,0,+1\}$ with probability $1/3$ each; the investor is always present.
- Extensions: general noise $(\pi_-,\pi_0,\pi_+)$; investor presence with probability $\lambda\in(0,1)$.
- Independent check: the **buy-only** menu $q\in\{0,1\}$ in the leading case, and a comparison of the two menus.

I did not coordinate with the member who builds the buy-only menu in full. Section 3, Claim 12, gives my own derivation so that the team can compare.

## 2. Formal setup

**Auction stage.** As in the paper (Section 2.2 and eq. (4)): $0<p<\ell<r<h$; the incumbent value is uniform on $[0,r]$; the challenger value is $\theta\in\{\ell,h\}$ with prior $1/2$ each; the preparation cost is $C\in\{c_L,c_H\}$ with $\Pr(c_L)=\rho\in(0,1)$ and $0\le c_L<c_H$. The cost is independent of everything. Notation from the paper: $t_0,t_H,t_L,g_H,g_L$, $\Delta_T=t_H-t_L$, $B_r(\mu)=g_L+\mu(g_H-g_L)$, $w_L=t_L-t_0>0$, and $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$, the root above $\ell$ of $\Delta_T(r)=d$ (eq. (A.10)).

**Investor.** Observes $\theta$. Present with probability $\lambda\in(0,1]$; the leading case is $\lambda=1$. A present investor chooses $q\in\{-1,0\}$ (sell-only) or $q\in\{0,1\}$ (buy-only). It pays $k>0$ per unit traded and earns $q(V_T-P)-k|q|$. It holds no initial position (Claim 14 relaxes this). Write $s_\theta\in[0,1]$ for the probability that a present investor of type $\theta$ trades (sells in the sell-only menu; I write $b_\theta$ in the buy-only menu). Mixed strategies are allowed. An indifferent investor does not trade.

**Noise.** $z\in\{-1,0,+1\}$ with probabilities $(\pi_-,\pi_0,\pi_+)$, all positive, independent of everything. Leading case: $1/3$ each.

**Pricing.** Flow $X=q+z$. Competitive market makers see $X$ only and set $P(X)=\mathbb E[V_T\mid X]$. They anticipate preparation and the auction.

**Challenger.** Sees the price $P$ and its cost $C$, not $X$. It prepares iff $B_r(\Pr(H\mid P))\ge C$ (an indifferent challenger prepares, as in the paper). Cost-averaged preparation at belief $\mu$ is
$$e_r(\mu)=\rho\,\mathbf 1\{c_L\le B_r(\mu)\}+(1-\rho)\,\mathbf 1\{c_H\le B_r(\mu)\}\in\{0,\rho,1\}.$$
Belief thresholds: $\tau_L=(c_L-g_L)/(g_H-g_L)$ and $\tau_H=(c_H-g_L)/(g_H-g_L)$.

**Equilibrium.** Perfect Bayesian equilibrium. On-path beliefs follow Bayes' rule. Off-path flows receive beliefs that satisfy the Intuitive Criterion (Cho and Kreps 1987), as in EGJ (their Section 2.3). Claim 3 shows that D1 gives the same belief, and which results depend on the rule.

**Accounting identity (used throughout).** Entry depends only on $(P(x),C)$, and $C$ is independent of $\theta$. So $\mathbb E[V_T\mid\theta,x]=t_0+e(x)(t_\theta-t_0)$, and $P(x)=t_0+e(x)[w_L+\Delta_T\mu(x)]$ for the belief $\mu(x)$ used at $x$. A sale at $x$ therefore earns $A_L(x)=e(x)\Delta_T\mu(x)$ in state $L$ and $-A_H(x)=-e(x)\Delta_T[1-\mu(x)]$ in state $H$. These are the paper's residuals (eq. (11)). The identity does not use the noise law. It holds at off-path flows for any belief.

**Vocabulary.** A flow is **revealing** if its posterior is 0 or 1. A **camouflage flow** is a non-revealing flow that the trader reaches. Define the camouflage residual
$$\kappa(r)=\frac{e_r(1/2)\,\Delta_T(r)}{3}.$$

---

## 3. Results

### Claim 1. Posteriors under every profile (analytical)

Sell-only, equal noise, $\lambda=1$, any $(s_H,s_L)\in[0,1]^2$:

| flow $x$ | $\Pr(x\mid\theta)$ | posterior $\mu(x)$ | off path iff |
|---|---|---|---|
| $+1$ | $(1-s_\theta)/3$ | $(1-s_H)/(2-s_H-s_L)$ | $s_H=s_L=1$ |
| $0$ | $1/3$ | $1/2$ | never |
| $-1$ | $1/3$ | $1/2$ | never |
| $-2$ | $s_\theta/3$ | $s_H/(s_H+s_L)$ | $s_H=s_L=0$ |

*Derivation.* $X=0$ arises from $(q,z)=(0,0)$ or $(-1,+1)$, with probability $(1-s_\theta)/3+s_\theta/3=1/3$. $X=-1$ arises from $(0,-1)$ or $(-1,0)$, also $1/3$. $X=+1$ needs $(0,+1)$; $X=-2$ needs $(-1,-1)$. Bayes' rule with prior $1/2$ gives the posteriors. $\square$

Consequences:

1. The interior flows never carry information, under any pure or mixed profile. All information sits in the two extreme flows.
2. $X=+1$ reveals $H$ iff $s_L=1>s_H$. $X=-2$ reveals $L$ iff $s_L>0=s_H$.
3. With presence $\lambda$, replace $s_\theta$ by $\lambda s_\theta$. The interior rows do not change.

With $s_H=0$ (Claim 2) and $s_L=s$: $\mu(+1)=1/(2-s)$, $\mu(0)=\mu(-1)=1/2$, and $\mu(-2)=0$ for $s>0$.

Revealing and off-path flows by variant (Claims 1, 10, 12):

| menu, presence | profile | reveals $H$ | reveals $L$ | off path |
|---|---|---|---|---|
| sell-only, $\lambda=1$ | no trade | none | none | $X=-2$ |
| sell-only, $\lambda=1$ | mixed $s_L\in(0,1)$ | none ($\mu(1)=1/(2-s_L)$) | $X=-2$ | none |
| sell-only, $\lambda=1$ | full selling | $X=+1$ | $X=-2$ | none |
| sell-only, $\lambda<1$ | full selling | none ($\mu(1)=1/(2-\lambda)$) | $X=-2$ | none |
| buy-only, $\lambda=1$ | no trade | none | none | $X=+2$ |
| buy-only, $\lambda=1$ | mixed $b_H\in(0,1)$ | $X=+2$ | none ($\mu(-1)=(1-b_H)/(2-b_H)$) | none |
| buy-only, $\lambda=1$ | full buying | $X=+2$ | $X=-1$ | none |
| buy-only, $\lambda<1$ | full buying | $X=+2$ | none ($\mu(-1)=(1-\lambda)/(2-\lambda)$) | none |

### Claim 2. The high-value investor never sells (analytical)

In every candidate equilibrium, for every belief system on and off path, every noise law, every $\lambda$ and every $r$, a sale by the high-value investor earns at most $-k<0$. Hence $s_H=0$ in every equilibrium. In the buy-only menu, the low-value investor never buys, for the same reason.

*Proof.* By the accounting identity, a sale in state $H$ earns $\sum_x\Pr(x\mid\text{sale})\,[-A_H(x)]-k$. Here $A_H(x)=e(x)\Delta_T[1-\mu(x)]\ge0$ for every $e(x)\in[0,1]$ and every $\mu(x)\in[0,1]$. $\square$

Claim 14 shows that an initial stake does not change this.

### Claim 3. Off-path flows and the belief rule (analytical)

**(a)** Given Claim 2, the only flow that can be off path in a candidate equilibrium is $X=-2$ under no trade. ($X=+1$ is off path only when $s_H=s_L=1$, which Claim 2 excludes for every belief.)

**(b)** The Intuitive Criterion and D1 both set $\mu(-2)=0$. Under no trade, type $H$ earns 0, and a sale earns it at most $-k$ under every belief, so a sale is equilibrium-dominated for $H$. If a sale is not equilibrium-dominated for $L$, the Intuitive Criterion puts zero weight on $H$. D1 does the same: the set of market responses that make a sale weakly profitable is empty for $H$ and nonempty for $L$. If a sale is equilibrium-dominated for both types, neither rule restricts the belief; but then no belief can break no trade. EGJ use this belief (proof of their Proposition 1: "the only belief that is consistent with the Intuitive Criterion").

**(c)** The no-trade region does not depend on the rule, provided the rule allows $\mu(-2)=0$. A deviation to a sale reaches $X\in\{-2,-1,0\}$ with probability $1/3$ each and earns
$$U_L^{\rm dev}(\mu_{\rm off})=\tfrac13\big[e_r(\tfrac12)\Delta_T+e_r(\mu_{\rm off})\,\Delta_T\,\mu_{\rm off}\big]-k .$$
This is nondecreasing in $\mu_{\rm off}$, and $\mu_{\rm off}=0$ minimizes it. So: no trade is a PBE outcome for some belief $\iff$ it survives the Intuitive Criterion $\iff$ it survives D1 $\iff$ $\kappa(r)\le k$.

**(d)** Other rules shrink the region and open a gap with no equilibrium.

- Passive belief $\mu_{\rm off}=1/2$: no trade needs $e_r(\tfrac12)\Delta_T/2\le k$. This is exactly the Laplace condition of Proposition A.4. At the benchmark the boundary is $\mathfrak r(2k/\rho)=1.747878=r_N$.
- Adverse belief $\mu_{\rm off}=1$ (with $e_r(1)=1$): no trade needs $(1+\rho)\Delta_T/3\le k$; boundary $\mathfrak r(3k/(1+\rho))=1.361535$.
- Between such a boundary and $r^\ast=\mathfrak r(3k/\rho)=1.973212$, no equilibrium exists under that rule: no trade fails, and every $s_L>0$ fails because the seller earns $\kappa-k<0$ (Claim 5).

Numerical diagnostic: at $r=1.8$ and $r=1.9$ the exact grid search finds no equilibrium under the passive and adverse rules and exactly one (no trade) under the Intuitive Criterion (script section G).

**(e)** Dependence. Only part (i) of Proposition 2d (Claim 6) uses the rule. Parts (ii) and (iii) are belief-free: full selling has no off-path flow, and when $\kappa>k$ the no-trade candidate fails under every belief. Part (i) is also belief-free when $(1+\rho)\Delta_T(r_0)/3<k$. The benchmark satisfies this ($0.006944<0.02$), and also the passive-belief condition ($0.002083<0.02$).

### Claim 4. Price sufficiency and shared prices (analytical)

**(a)** Two on-path flows with different posteriors can share a price only at $P=t_0$, with zero entry.

*Proof* (the argument of Proposition A.2). If $P(x)=P(x')=\bar P$, entry $e(\bar P)$ is common. Then $e(\bar P)[w_L+\Delta_T\mu(x)]=e(\bar P)[w_L+\Delta_T\mu(x')]$, so $e(\bar P)=0$ or $\mu(x)=\mu(x')$. If $e(\bar P)=0$, then $\bar P=t_0$, and the challenger must stay out at its pooled posterior $\bar\mu$: $B_r(\bar\mu)<c_L$. $\square$

**(b)** Pooled-posterior floor. With $s_H=0$, every set of on-path flows that contains $X=-2$ and at least one other flow has pooled posterior at least $1/(2+\lambda s_L)\ge1/3$.

*Derivation.* The pair $\{-2,-1\}$ has $H$-mass $\tfrac12\cdot\tfrac13$ and $L$-mass $\tfrac12(\tfrac13+\tfrac{\lambda s_L}{3})$, so $\bar\mu=1/(2+\lambda s_L)$; the pair $\{-2,0\}$ is the same. $\{-2,-1,0\}$ gives $2/(4+\lambda s_L)\ge2/5$. Any set that contains $X=+1$ and $X=-2$ gives $1/2$ or more. Sets without $X=-2$ contain only posteriors of at least $1/2$. $\square$

So under
$$\textbf{(S1)}\qquad 0\le c_L\le B_r(1/3)$$
no zero-entry pool exists, and the price reveals $\mu_X$ at every on-path flow. The only possible zero-entry price is $X=-2$ alone, when $c_L>g_L(r)$. Its price $t_0$ is unique, so it hides nothing.

**(c)** $X=0$ and $X=-1$ always share a price, because they share the posterior $1/2$. This is harmless.

**(d)** Without (S1) the price can hide information. If $B_r(1/(2+s_L))<c_L\le B_r(1/2)$, a self-fulfilling schedule prices $X=-2$ and $X=-1$ (or $X=0$) at $t_0$. The challenger sees $t_0$, holds posterior $1/(2+s_L)$, and stays out, which confirms the price. Under full selling the seller then earns $\rho\Delta_T/6-k$ instead of $\rho\Delta_T/3-k$, and entry is $(1+2\rho)/6$ instead of $(1+4\rho)/6$. When $\rho\Delta_T(r)/6>k$ this is a second equilibrium. EGJ avoid exactly this problem: they let the manager observe order flow, and they note that price observation allows self-fulfilling prices (their Section 2.2). The paper keeps price observation, so the discrete version needs (S1).

**(e)** Benchmark: $B_r(1/3)\ge1=c_L$ for all $r\le14.0887$, so (S1) holds on all of $(\ell,h)=(1,10)$. (S1) is weaker than the paper's (A1) at $b=2$, because $1/3>m=0.2689$.

### Claim 5. All equilibria in the leading case (analytical)

Assume (S1) at $r$. Every equilibrium has $s_H=0$. For every $s_L>0$, and for $s_L=0$ under the Intuitive-Criterion belief, the low-value investor's net payoff from a sale is
$$U_L(s_L)=\tfrac13\big[A_L(-2)+A_L(-1)+A_L(0)\big]-k=\tfrac13\Big[0+2\,e_r(\tfrac12)\,\frac{\Delta_T}{2}\Big]-k=\kappa(r)-k,$$
which does not depend on $s_L$. (At $X=-2$ the posterior is 0; at $X\in\{-1,0\}$ it is $1/2$, and by Claim 4 the challenger reads $1/2$ from the price.) Therefore:

- **$\kappa(r)<k$:** the unique equilibrium is no trade. The price is constant at $t_0+e_r(\tfrac12)[w_L+\Delta_T/2]$; entry is $e_r(\tfrac12)$.
- **$\kappa(r)>k$:** the unique equilibrium is full selling $(s_H,s_L)=(0,1)$. The posteriors are $(1,\tfrac12,\tfrac12,0)$ at $X=(+1,0,-1,-2)$, and
$$\mathsf E(r)=\frac{e_r(1)+e_r(0)}{6}+\frac{2\,e_r(1/2)}{3},\qquad \mathsf O_H(r)=\frac{e_r(1)+2\,e_r(1/2)}{6}.$$
- **$\kappa(r)=k$:** every $s_L\in[0,1]$ is an equilibrium, a continuum of mixed equilibria. The tie rule selects $s_L=0$. Another tie rule changes only this knife edge. Entry is not constant along the continuum: at the benchmark strength $r=3$ with $k=1/18$ it ranges from about $0.226$ to $0.403$, with a jump where $1/(2-s_L)$ crosses $\tau_H$.

Uniqueness covers prices and entry, by Claim 4.

**As a function of $(r,k,\rho,c_H)$.** On the domain $\mathcal D^d=\{r\in(\ell,h): c_L\le B_r(1/3),\ B_r(1/2)<c_H\}$, $e_r(1/2)=\rho$, so $\kappa(r)=\rho\Delta_T(r)/3$ rises strictly in $r$. One cutoff
$$r^\ast=\mathfrak r(3k/\rho)$$
separates unique no trade ($r<r^\ast$) from unique full selling ($r>r^\ast$). **There is single crossing and no overlap: no coexistence of no trade and trade.** Above $r^\ast$, entry is a step function:

- $e_r(1)=1$ iff $c_H\le g_H(r)$, i.e. iff $r\le r_C^d:=(h-c_H)+\sqrt{(h-c_H)^2-p^2}$ (when this root is below $h$);
- $e_r(0)=\rho$ iff $c_L\le g_L(r)$, i.e. iff $r\le(\ell^2-p^2)/(2c_L)$; otherwise $e_r(0)=0$.

Outside $\mathcal D^d$, where $B_r(1/2)\ge c_H$, $e_r(1/2)=1$ and $\kappa=\Delta_T/3$. Because $e_r(1/2)$ drops from 1 to $\rho$ where $B_r(1/2)$ crosses $c_H$, the trade set $\{\kappa>k\}$ need not be an interval in $r$. In that region information can only lower entry.

Numerical diagnostic: with exact rational arithmetic, a $21\times21$ grid over $(s_H,s_L)$ finds exactly one equilibrium at each of $r\in\{1.2,3,3.6,9\}$ for both menus, and all 21 grid points $(0,s_L)$ at the knife edge $k=1/18$, $r=3$ (script sections C–E). A sweep of $r$ over $[1.01,9.99]$ (step 0.005) finds one switch, between $1.970$ and $1.975$, which brackets $r^\ast=1.973212$.

### Claim 6. Proposition 2 analog for the sell-only menu (analytical)

**Proposition 2d.** Fix $0<p<\ell<r_0<r_1<h$, $\rho\in(0,1)$, $k>0$, equal noise and $\lambda=1$. Suppose
$$\textbf{(S1)}\quad 0\le c_L\le B_{r_1}(1/3),$$
$$\textbf{(S2)}\quad B_{r_0}(1/2)<c_H\le B_{r_1}(1)=g_H(r_1),$$
$$\textbf{(S3)}\quad \frac{\rho\,\Delta_T(r_0)}{3}<k<\frac{\rho\,\Delta_T(r_1)}{3}.$$

(i) At $r_0$ the unique equilibrium outcome is no trade. The price carries no information. Entry is $\rho$. The one off-path flow, $X=-2$, has belief 0 under the Intuitive Criterion and under D1.

(ii) At $r_1$ the unique equilibrium is $(s_H,s_L)=(0,1)$. $X=+1$ reveals $H$ and recruits the high-cost challenger. $X=-2$ reveals $L$. $X\in\{0,-1\}$ carry no information. Entry and high-value ownership are
$$\mathsf E=\rho+\frac{1-\rho}{6}\ \ \text{if } c_L\le g_L(r_1),\qquad \mathsf E=\rho+\frac{1-2\rho}{6}\ \ \text{if } c_L>g_L(r_1),\qquad \mathsf O_H=\frac{1+2\rho}{6}>\frac\rho2 .$$
Entry exceeds $\rho$ always in the first case, and in the second case iff $\rho<1/2$. All additional high-cost preparation occurs in state $H$.

(iii) For any $r_2\in(r_1,h)$ with $c_L\le B_{r_2}(1/3)$ and $g_H(r_2)<c_H$, the unique equilibrium is again full selling. Entry is $\rho$ if $c_L\le g_L(r_2)$, and $5\rho/6$ otherwise.

Given (S1)–(S2), (S3) is necessary as well as sufficient for the trading outcomes in (i)–(ii). Parts (ii) and (iii) hold under every off-path belief rule; part (i) does too if $(1+\rho)\Delta_T(r_0)/3<k$. The conditions hold on a nonempty open set: the benchmark vector satisfies (S1)–(S3) with strict inequalities at $(r_0,r_1)=(1.2,3)$, and (iii) holds for every $r_2\in(7.968627,10)$.

*Proof.*

*Step 1 (who trades).* Claim 2 gives $s_H=0$ in both economies.

*Step 2 (entry at camouflage flows; prices).* $B_r(\mu)$ falls in $r$ (eq. (5)). So (S1) at $r_1$ gives (S1) at $r_0$, and (S2) gives $B_r(1/2)\le B_{r_0}(1/2)<c_H$ for $r\ge r_0$. With $c_L\le B_r(1/3)\le B_r(1/2)$, $e_r(1/2)=\rho$ at $r_0$ and $r_1$. Claim 4 gives price sufficiency in both economies.

*Step 3 (weak economy).* By Claim 5, $U_L(s)=\rho\Delta_T(r_0)/3-k<0$ for every $s>0$, so $s_L=0$. Against no trade with $\mu(-2)=0$, the deviation earns the same negative amount. All on-path flows have posterior $1/2$, entry is $\rho$, and the constant price $t_0+\rho[w_L+\Delta_T/2]$ is competitive.

*Step 4 (strong economy).* $U_L(s)=\rho\Delta_T(r_1)/3-k>0$ for every $s>0$. Against no trade, a sale earns at least this amount under every belief, because the off-path residual is nonnegative. So $s_L=1$. Claim 1 gives the posteriors $(1,\tfrac12,\tfrac12,0)$. (S2) gives $e_{r_1}(1)=1$; Step 2 gives $e_{r_1}(1/2)=\rho$; and $e_{r_1}(0)=\rho\,\mathbf 1\{c_L\le g_L(r_1)\}$, because $c_H>B_{r_1}(1/2)>g_L(r_1)$. Substitution in Claim 5 gives $\mathsf E$ and $\mathsf O_H$; a prepared high-value challenger always wins because $h>r_1$. Then $\mathsf O_H-\rho/2=(1-\rho)/6>0$. The price takes three values with state-dependent probabilities, so the strong experiment strictly Blackwell-dominates the constant one.

*Step 5 (part iii).* $\Delta_T$ rises in $r$, so $\rho\Delta_T(r_2)/3>k$ and full selling is unique. The largest feasible posterior is 1, so $g_H(r_2)<c_H$ excludes high-cost preparation at every price. Low-cost preparation occurs at posteriors 1 and $1/2$, and at 0 iff $c_L\le g_L(r_2)$. Substitution gives the stated entry.

*Step 6 (necessity, openness).* Claim 5 gives necessity. All inequalities are strict at the benchmark (Section 5) and continuous in the primitives. $\square$

**Comparison with (A1)–(A3).**

- (S1) replaces (A1). It is a price-sufficiency condition at the pooled posterior $1/3$. It is weaker than (A1) at $b=2$. It does **not** keep low-cost preparation at the $L$-revealing flow; that needs $c_L\le g_L(r)$, which the benchmark ($c_L=1$) violates for every $r>0.375$.
- (S2) moves the ceiling from $B_{r_1}(M)$ to $B_{r_1}(1)=g_H(r_1)$, because the posterior can reach 1.
- (S3) replaces (A3). Both sides are exact, not merely sufficient. The weak-economy side, $\rho\Delta_T(r_0)/3<k$, is much weaker than $\Delta_T(r_0)<k$. The strong-economy coefficient $1/3$ exceeds the Laplace coefficient $(1-1/b)m=0.1345$ at $b=2$.

### Claim 7. The economics of the sell-only menu (analytical)

1. **Favorable news is the absence of selling.** Under full selling, $X=+1$ needs $q=0$, so it reveals $H$. The challenger is recruited by an inference about a sale that did not happen.
2. **The residual advantage sits on the $L$ side.** The seller earns $A_L=e\,\Delta_T\,\mu$ at its camouflage flows $X\in\{0,-1\}$, where $\mu=1/2$. The high-value investor's information never trades. It reaches the price only through the low-value investor's strategy.
3. **Recruited entry and trading profit are decoupled.** The seller never reaches $X=+1$, so high-cost preparation there never enters its payoff. This is why the leading case has one cutoff and no analog of Proposition 3. The buy-only menu has the same property: its recruiting flow $X=+2$ is revealing, so the buyer's residual there is zero.
4. **Mechanism.** A stronger incumbent raises $\Delta_T$ and so the camouflage residual $\rho\Delta_T/2$. At $r^\ast$ the bad-news investor starts to sell. The absence of selling then becomes informative, and the expensive challenger prepares after $X=+1$. At a fixed experiment, the direct effect of strength on entry is weakly negative (Claim 9). Entry rises only because the experiment changes.

### Claim 8. Feedback and the EGJ asymmetry (analytical, with numerical diagnostics)

**(a) Leading case: feedback is neutral.** For every $\lambda$ and in both menus, the trader's payoff equals its payoff when the challenger cannot see the price (entry $e_r(1/2)$ at every flow): $\kappa-k$ in both cases. The trader reaches only the revealing flow (residual 0 whatever the entry) and flows with posterior $1/2$ (entry $e_r(1/2)$ with or without feedback). **Anticipated entry makes selling on bad news neither more nor less profitable.**

EGJ make the same observation for their model (Section 3.5.2): feedback changes trading profits only at $X=\pm1$; at $X=\pm2$ the speculator is revealed and earns zero; at $X=0$ the price is uninformative. In EGJ the asymmetry runs through deviations in the *opposite* direction: the positively informed speculator's deviation to buying in their sell-not-buy equilibrium, and the negatively informed speculator's deviation to selling in their buy-not-sell equilibrium (their Proposition 1 and Section 3.3.2). A one-directional menu deletes those deviations, so the asymmetry has no channel.

**(b) The model has EGJ's structure.** EGJ's driving inequality (their eq. (1)) says the real action raises the state sensitivity of firm value. Here $V_T(H)-V_T(L)=e\,\Delta_T$, so preparation plays the role of investment, and it rises with the posterior. Two channels act at camouflage flows once these flows carry information (general noise, Claim 11):

- **Recruitment at a favorable camouflage flow** ($X=0$ when $\mu_0\ge\tau_H$) raises $A_L(0)$ from $\rho\Delta_T\mu_0$ to $\Delta_T\mu_0$. Anticipated entry then makes selling on bad news **more** profitable. The seller gains from the market's overvaluation, and entry scales up the component that the market overvalues. This is the reverse of EGJ's corrective channel.
- **Deterrence at an unfavorable camouflage flow** ($X=-1$ when $\mu_{-1}<\tau_L$) sets $A_L(-1)=0$. Anticipated deterrence then makes selling **less** profitable. This is EGJ's direction: the real response at a low price removes the claim's state sensitivity. It needs the low-cost floor to fail at that flow. It cannot occur if $c_L\le g_L(r)$; under (S1) it needs $\mu_{-1}<\tau_L\le1/3$.

**(c) Under the paper's floor the EGJ reduction cannot occur.** Under (A1)–(A2), and here under (S2) with $c_L\le g_L(r)$, preparation is at least $\rho=e_r(1/2)$ at every price. At a fixed experiment, feedback therefore weakly raises every residual relative to the hidden-price benchmark. An EGJ-type *absolute* reduction in the profit from informed selling cannot occur in the paper's maintained domain, with Laplace or discrete noise. Any asymmetry there is *relative*: it depends on which flows each trader visits.

**(d) Numerical diagnostics** (general-noise script, cases E3 and E5).

- Noise $(0.2,0.6,0.2)$, benchmark costs, $r=1.7$: full selling earns $U_L=+0.00702$ with feedback. With the price hidden it would earn $-0.00919$. Recruitment at $X=0$ makes selling profitable.
- Noise $(0.2,0.6,0.2)$, $c_L=2.5$, $c_H=7$, $r=3$, $k=0.03$: deterrence at $X=-1$ for $s_L>0.7544$ cuts $U_L$ from $+0.0208$ (at $s_L=0.75$) to $-0.0050$ (at $s_L=1$).

### Claim 9. Fixed-experiment control (analytical; numerical diagnostic)

Proposition A.3 applies without change: its proof uses only a fixed joint law of signal and quality. With full selling frozen,
$$\mathsf E^{\rm fix}(r)=\frac{e_r(1)+e_r(0)}{6}+\frac{2\,e_r(1/2)}{3},$$
a weakly decreasing step function of $r$. It steps only where $B_r(\mu)$ crosses $c_L$ or $c_H$ at $\mu\in\{0,\tfrac12,1\}$. Under (S1)–(S2), the steps at $\mu=\tfrac12$ and $\mu=1$ cannot fall in $[r_0,r_1]$. So **strict deterrence at the fixed experiment between $r_0$ and $r_1$ occurs iff $c_L\in(g_L(r_1),g_L(r_0)]$.**

Benchmark (numerical diagnostic, script section I):

| $c_L$ | frozen full selling $r_0\to r_1$ | equilibrium $r_0\to r_1$ | price hidden |
|---|---|---|---|
| 1 (benchmark) | 0.333333 → 0.333333 | 0.25 → 0.333333 | 0.25 → 0.25 |
| 0 | 0.375 → 0.375 | 0.25 → 0.375 | 0.25 → 0.25 |
| 0.2 $\in(0.125,0.3125]$ | 0.375 → 0.333333 | 0.25 → 0.333333 | 0.25 → 0.25 |

At the benchmark the direct effect is zero, and the whole rise in entry comes from the change of experiment. The paper's "deterrence despite" decomposition (Table 2) has a strict discrete analog only for a tuned $c_L$.

### Claim 10. Investor presence $\lambda<1$ (analytical; numerical diagnostic)

Equal noise, presence probability $\lambda\in(0,1]$.

**Sell-only.** $\Pr(X=+1\mid L)=(1-\lambda s_L)/3$ and $\Pr(X=-2\mid L)=\lambda s_L/3$; the interior rows stay at $1/3$. So $\mu(+1)=1/(2-\lambda s_L)<1$ and $\mu(-2)=0$. The present seller still earns $\kappa-k$: **the cutoff $r^\ast$ does not depend on $\lambda$.** Under full selling the top posterior is $M_\lambda=1/(2-\lambda)$: state $H$ is no longer revealed; state $L$ still is. (S2) becomes $B_{r_0}(1/2)<c_H\le B_{r_1}(M_\lambda)$, and
$$\mathsf E=\frac{(2-\lambda)\,e_r(M_\lambda)+\lambda\,e_r(0)}{6}+\frac{2\,e_r(1/2)}{3},\qquad \mathsf O_H=\frac{e_r(M_\lambda)+2\,e_r(1/2)}{6}.$$
With $e_r(M_\lambda)=1$: $\mathsf E=\rho+(1-\rho)(2-\lambda)/6$ if $c_L\le g_L(r)$, otherwise $(2-\lambda)/6+2\rho/3$; and $\mathsf O_H=(1+2\rho)/6$. Part of the additional entry is now low-value entry: after $X=+1$ in state $L$ with the investor absent.

**Buy-only.** $\Pr(X=+2\mid H)=\lambda b_H/3$ and $\Pr(X=-1\mid H)=(1-\lambda b_H)/3$. So $\mu(+2)=1$ and $\mu(-1)=(1-\lambda b_H)/(2-\lambda b_H)\ge m_\lambda:=(1-\lambda)/(2-\lambda)>0$. The $L$-revealing flow disappears; the $H$-revealing flow stays. The condition
$$\textbf{(B1)}\quad c_L\le B_{r_1}(m_\lambda)$$
keeps low-cost preparation at every on-path price and gives price sufficiency by the argument of Proposition A.2. The ceiling condition stays $c_H\le g_H(r_1)$, and
$$\mathsf E=\rho+\frac{\lambda(1-\rho)}{6},\qquad \mathsf O_H=\frac\rho2+\frac{\lambda(1-\rho)}{6}.$$
All additional entry is high-value entry.

*Derivation of the buy-only forms.* In state $H$ the flows $(-1,0,1,2)$ have probabilities $((1-\lambda)/3,1/3,1/3,\lambda/3)$ and entry $(\rho,\rho,\rho,1)$; in state $L$ the flows $(-1,0,1)$ have probability $1/3$ each and entry $\rho$. Average over states. $\square$

Benchmark, $r_1=3$ (script sections J and L):

| $\lambda$ | sell-only top posterior, $B_3$ | sell-only $\mathsf E$ ($c_L=1$ / $c_L=0$) | buy-only bottom posterior, $B_3$ | buy-only $\mathsf E$, $\mathsf O_H$ ($c_L=1$) |
|---|---|---|---|---|
| 1 | 1, 8.4583 | 0.333333 / 0.375 | 0, 0.1250 | 0.333333, 0.25 |
| 3/4 | 0.8, 6.7917 | 0.375 / 0.40625 | 0.2, 1.7917 | 0.34375, 0.21875 |
| 1/2 | 0.6667, 5.6806 (< 6: no recruitment) | 0.229167 / 0.25 | 0.3333, 2.9028 | 0.3125, 0.1875 |

The buy-only menu with $\lambda=3/4$ satisfies (i)–(iii) at the benchmark with $c_L=1$ unchanged: entry $0.25$ at $r_0=1.2$, $0.34375$ at $r_1=3$, and $0.25$ at $r=9$.

In EGJ, $\lambda<1$ is necessary for their asymmetry (Section 3.5.2). Here $\lambda$ does not change the trading cutoff in either menu. It changes which extreme flow reveals the state.

### Claim 11. General noise $(\pi_-,\pi_0,\pi_+)$ (analytical, with numerical diagnostics)

Sell-only, $s_H=0$, $\sigma=\lambda s_L$:

| $x$ | $\Pr(x\mid H)$ | $\Pr(x\mid L)$ | $\mu(x)$ |
|---|---|---|---|
| $+1$ | $\pi_+$ | $(1-\sigma)\pi_+$ | $1/(2-\sigma)$ |
| $0$ | $\pi_0$ | $(1-\sigma)\pi_0+\sigma\pi_+$ | $\mu_0=\pi_0/[2\pi_0-\sigma(\pi_0-\pi_+)]$ |
| $-1$ | $\pi_-$ | $(1-\sigma)\pi_-+\sigma\pi_0$ | $\mu_{-1}=\pi_-/[2\pi_-+\sigma(\pi_0-\pi_-)]$ |
| $-2$ | $0$ | $\sigma\pi_-$ | $0$ |

The present seller earns
$$U(\sigma)=\Delta_T\big[\pi_+\,e(\mu_0)\,\mu_0+\pi_0\,e(\mu_{-1})\,\mu_{-1}\big]-k .$$

**(a) Camouflage flows carry information unless the noise is uniform.** $X=0$ is informative iff $\pi_0\ne\pi_+$; $X=-1$ iff $\pi_0\ne\pi_-$. Equal probabilities are exactly the case in which neither carries information. Under unimodal noise ($\pi_0>\pi_\pm$), $X=0$ is mildly favorable and $X=-1$ mildly unfavorable.

**(b) Symmetric noise, constant entry: strategic substitutes.** Let $\pi_-=\pi_+=\pi_1\ne\pi_0$, $d=\pi_0-\pi_1$, and suppose entry at both camouflage flows is a constant $\bar e>0$. Then
$$U'(\sigma)=\bar e\,\Delta_T\,\pi_0\pi_1\,d\,\Big[(2\pi_0-\sigma d)^{-2}-(2\pi_1+\sigma d)^{-2}\Big].$$
Since $(2\pi_0-\sigma d)-(2\pi_1+\sigma d)=2d(1-\sigma)$ has the sign of $d$, the bracket has the sign of $-d$, so $U'<0$ on $[0,1)$. The equilibrium is unique. It is interior (partial selling) when $U(0)>0>U(1)$.

**(c) Asymmetric noise, constant entry.** With $H(a,b)=ab/(a+b)\le(a+b)/4$,
$$U(1)-U(0)=\bar e\Delta_T\big[H(\pi_0,\pi_+)+H(\pi_0,\pi_-)-(\pi_0+\pi_+)/2\big]\le\bar e\Delta_T\,(\pi_--\pi_+)/4,$$
with equality only for uniform noise. So no trade and full selling can coexist at constant entry only if $\pi_->\pi_+$. Numerical diagnostic (E4): noise $(0.4,0.4,0.2)$, $c_H=7$, $r=2$: no trade, full selling ($\mathsf E=0.275$) and a mixed equilibrium at $s_L=2/3$ coexist; multiplicity holds for $r\in[1.975,2.040]$. The buy-only menu has a unique equilibrium at every $r$ in that case.

**(d) Entry jumps.** Recruitment at $X=0$ raises $U$ by $(1-\rho)\Delta_T\pi_+\mu_0$ where $\mu_0$ crosses $\tau_H$: a strategic complementarity. It creates coexistence even with symmetric noise (numerical diagnostics, E2 and E3, grid step 0.005 in $r$):

| noise | no trade and full selling coexist | more than one equilibrium | full-selling entry |
|---|---|---|---|
| $(1/3,1/3,1/3)$ | never | never | 0.3333 ($r<7.97$), 0.2083 |
| $(1/4,1/2,1/4)$ | $r\in[1.545,1.900]$ | $r\in[1.545,1.970]$ | 0.5938 ($r\le2.06$), 0.3125, 0.2188 |
| $(0.2,0.6,0.2)$ | $r\in[1.585,1.860]$ | $r\in[1.585,2.030]$ | 0.6000 ($r\le4.00$), 0.3000, 0.2250 |

At $r=1.7$ with $(0.2,0.6,0.2)$: no trade ($\mathsf E=0.25$), full selling ($\mathsf E=0.60$, $\mathsf O_H=0.425$), and a third equilibrium at $s_L=0.7015$ in which the high-cost challenger mixes at $X=0$. This is a discrete analog of Proposition 3. Deterrence at $X=-1$ lowers $U$ by $\rho\Delta_T\pi_0\mu_{-1}$ where $\mu_{-1}$ crosses $\tau_L$.

**(e) Existence and the tie rule.** A jump of $U$ across zero supports an equilibrium only if the indifferent challenger mixes at that flow. The paper's tie rule (an indifferent challenger prepares) forbids this. Numerical diagnostic (E5): noise $(0.2,0.6,0.2)$, $c_L=2.5$, $c_H=7$, $r=3$, $k=0.03$. Then $U>0$ for $s_L<0.7544$ and $U<0$ above, so **no equilibrium exists under the tie rule**. One exists if the low-cost challenger prepares with probability $0.27$ at $X=-1$ ($s_L=0.7544$, $\mathsf E=0.1672$). Analytical: if the challenger may mix at indifference, an equilibrium always exists. $U$ is continuous between finitely many jumps; at a jump the relevant posterior equals a threshold, so mixing fills the jump with an interval; if $U(0)>0>U(1)$, the intermediate-value argument gives a zero.

**(f) A Proposition 2 analog under general noise needs sufficient bounds, as with Laplace.** (i) holds if $\Delta_T(r_0)\max_\sigma[\pi_+\mu_0+\pi_0\mu_{-1}]<k$. (ii) holds if the low-cost type prepares at both camouflage flows for every $\sigma$, a pooled-posterior condition as in Claim 4 holds, and $\rho\Delta_T(r_1)\min_\sigma[\pi_+\mu_0+\pi_0\mu_{-1}]>k$. Items (b)–(e) live in the gap between the two bounds. Entry keeps the form of the paper's eq. (12), plus a deterrence term:
$$\mathsf E=\rho+\frac{1-\rho}{2}(\alpha_H+\alpha_L)-\frac\rho2(\beta_H+\beta_L),\qquad \mathsf O_H=\frac12\big[\rho(1-\beta_H)+(1-\rho)\alpha_H\big],$$
with $\alpha_\theta=\Pr(\mu_X\ge\tau_H\mid\theta)$ and $\beta_\theta=\Pr(\mu_X<\tau_L\mid\theta)$. In the leading case $\alpha_H=1/3$, $\alpha_L=0$, $\beta_H=0$, $\beta_L=\mathbf 1\{c_L>g_L\}/3$.

### Claim 12. Buy-only leading case, derived independently (analytical)

Buy-only, equal noise, $\lambda=1$, $b_\theta=\Pr(\text{buy}\mid\theta)$:

| flow $x$ | $\Pr(x\mid\theta)$ | posterior $\mu(x)$ | off path iff |
|---|---|---|---|
| $+2$ | $b_\theta/3$ | $b_H/(b_H+b_L)$ | $b_H=b_L=0$ |
| $+1$ | $1/3$ | $1/2$ | never |
| $0$ | $1/3$ | $1/2$ | never |
| $-1$ | $(1-b_\theta)/3$ | $(1-b_H)/(2-b_H-b_L)$ | $b_H=b_L=1$ |

1. The low-value investor never buys (Claim 2): a purchase in state $L$ earns $-\sum_x\Pr(x)A_L(x)-k\le-k$.
2. With $b_L=0$, the buyer reaches $X\in\{0,+1,+2\}$ and earns $\tfrac13[2\,e_r(\tfrac12)\Delta_T/2+e_r(1)\Delta_T\cdot0]-k=\kappa-k$ for every $b_H>0$. Against no trade, the Intuitive-Criterion belief is $\mu(+2)=1$ (a purchase is equilibrium-dominated for $L$), which makes the off-path residual $e(\mu)\Delta_T(1-\mu)$ zero. This is again the most supportive belief, so the no-trade region is the same under every rule that allows it.
3. The equilibrium set is Claim 5 with $b_H$ in place of $s_L$: one cutoff $r^\ast=\mathfrak r(3k/\rho)$, a knife-edge continuum at $\kappa=k$, and a unique equilibrium otherwise.
4. Full buying: posteriors $(0,\tfrac12,\tfrac12,1)$ at $X=(-1,0,1,2)$; entry $(e_r(0),\rho,\rho,e_r(1))$; $\mathsf E$ and $\mathsf O_H$ equal those of Claim 6.
5. Pooled-posterior floor: the smallest pool with a non-revealing flow is $\{-1,0\}$ (or $\{-1,+1\}$), with posterior $(2-b_H)/(4-b_H)\ge1/3$. So (S1) is again the price-sufficiency condition.
6. **Proposition 2d holds verbatim for the buy-only menu under (S1)–(S3).** The only change is the off-path flow ($X=+2$, belief 1).

Numerical diagnostic: script section D reproduces these tables (one equilibrium at each strength; entry $0.25$, $0.333333$, $0.333333$, $0.208333$ at $r=1.2,3,3.6,9$).

### Claim 13. Buy-only versus sell-only (analytical)

**(a) Shift identity.** Under full trading, the buy-only experiment is the sell-only experiment shifted up by one unit of flow, for every noise law. Sell-only gives $X=z$ in $H$ and $X=z-1$ in $L$; buy-only gives $X=z+1$ in $H$ and $X=z$ in $L$. Posteriors, prices, entry, $\mathsf E$ and $\mathsf O_H$ coincide. The trader's gross profit is the same in both menus:
$$\sum_x\Pr(x\mid L)\,A_L(x)=\sum_x\Pr(x\mid H)\,A_H(x)=\Delta_T\sum_x e(x)\,\frac{\Pr(x\mid H)\Pr(x\mid L)}{\Pr(x\mid H)+\Pr(x\mid L)},$$
by Bayes' rule, $\Pr(x\mid L)\mu(x)=\Pr(x\mid H)[1-\mu(x)]$. This is the discrete counterpart of the paper's identity (A.7), $F_H(1)=F_L(1)=J$. Numerical diagnostic: section E6 of the general-noise script shows equal full-trading payoffs for four noise laws.

**(b) Where the menus differ.** (1) The no-trade deviation under asymmetric noise: $e_r(\tfrac12)\Delta_T(\pi_0+\pi_+)/2$ for sell-only, $e_r(\tfrac12)\Delta_T(\pi_0+\pi_-)/2$ for buy-only. (2) Mixed profiles. (3) Presence $\lambda<1$ (Claim 10).

**(c) Leading case.** With equal noise and $\lambda=1$ the two menus are outcome-equivalent, and the proofs are the same.

**Which menu is more natural for this paper.**

- *Short-sale constraints.* With no initial position, the sell-only menu is a short-only menu. No standard friction blocks purchases while it allows short sales. The buy-only menu matches the usual constraint. EGJ list borrowing costs for short sales among trading costs (their Section 2.2).
- *Direction of the recruiting information.* In the paper, favorable prices recruit an expensive challenger. In the buy-only menu, informed buying produces the recruiting flow. In the sell-only menu, the recruiting flow is the absence of a sale, an inference from silence. The two give the same entry in the leading case. The buy-only story is easier to state and to test: abnormal buying and positive returns before a second bidder prepares.
- *Proof.* Equal in the leading case. With $\lambda<1$ the buy-only menu is cleaner: it has no $L$-revealing flow, it has a positive posterior floor $m_\lambda$, its floor condition (B1) has the paper's form, and the benchmark $c_L=1$ works. The sell-only menu with $\lambda<1$ keeps the $L$-revealing flow (so low-cost preparation there still needs $c_L\le g_L$) and loses the $H$-revealing flow (so recruitment needs $c_H\le B_{r_1}(1/(2-\lambda))$, which fails at the benchmark for $\lambda=1/2$).
- *General noise.* Neither menu is cleaner. At constant entry, complementarity is possible in the sell-only menu only if $\pi_->\pi_+$, and in the buy-only menu only if $\pi_+>\pi_-$ (Claim 11(c) and its mirror).

### Claim 14. Sales from a stake (analytical; brief, because point 3 owns this)

Read the sell-only menu as sales from a stake of $\omega\ge1$ shares, so no short sale is needed. The payoff becomes $\omega V_T+q(V_T-P)-k|q|$. Against full selling, a sale in state $L$ moves the flow from $\{-1,0,1\}$ to $\{-2,-1,0\}$. Expected preparation falls by $[e_r(1)-e_r(0)]/3$, and the stake loses $\omega(t_L-t_0)[e_r(1)-e_r(0)]/3$. Full selling survives iff
$$\omega\le\frac{\kappa(r)-k}{(t_L-t_0)\,[e_r(1)-e_r(0)]/3}.$$
At the benchmark $r_1=3$, the bound is $\omega\le0.2327$ ($c_L=1$) or $\omega\le0.3103$ ($c_L=0$). **A holder who sells one unit out of its own shares does not sell at the benchmark.** If it does not sell, the flow $X=+1$ can occur; the expensive challenger then prepares, and the value of the holder's shares rises. A stake makes a sale in state $H$ even less attractive, so Claim 2 survives. In the buy-only menu a stake creates the opposite motive: a low-value holder buys to fake good news only if $\omega>1.9491$ ($c_L=1$) or $\omega>2.5988$ ($c_L=0$).

---

## 4. What changes relative to the current paper

| Item in the paper | Discrete menu, equal noise (both menus at $\lambda=1$) |
|---|---|
| Prop. 1, eqs. (4)–(6) | Unchanged (auction stage). |
| Eqs. (7)–(8), Prop. A.1 ($m\le\mu\le M$) | **Fails.** Posteriors reach 0 and 1. The posterior set is $\{0,\tfrac12,1/(2-\lambda s)\}$. The minimal pooled posterior $1/3$ plays the role of $m$ for price sufficiency. |
| Eqs. (9)–(10), Prop. A.2 | **Survives** under (S1), same proof. The low-cost floor at *every* price needs $c_L\le g_L(r)$, which the benchmark violates. |
| Eq. (11) bounds $\rho m\Delta_T\le A\le\Delta_T$ | Lower bound **fails** (residual 0 at revealing flows). Replaced by the exact camouflage residual $e_r(\tfrac12)\Delta_T/2$. |
| (A.4)–(A.6) global order bound, $\lvert f'\rvert\le f/b$ | **Not needed.** The binary menu gives exact payoffs. |
| (A.7) identity $F_H(1)=F_L(1)=J$ | **Survives** as the cross-menu identity, Claim 13(a). |
| Prop. 2, (A1)–(A3) | **Analog holds** (Claim 6) under (S1)–(S3); (S3) is exact. Part (iii) needs $g_H(r_2)<c_H$: the ceiling moves from $r_C=3.592659$ to $r_C^d=7.968627$, so $r_2=3.6$ no longer works. |
| Eq. (12): $\tau,x^\ast,\alpha_H,\alpha_L$ | $x^\ast$ disappears. $\alpha_H=1/3$, $\alpha_L=0$. $\mathsf E=\rho+(1-\rho)/6$ (with $c_L\le g_L$), $\mathsf O_H=(1+2\rho)/6$. Entry does not vary with $c_H$ on $(B_{r}(\tfrac12),g_H(r)]$. |
| Prop. 3 (coexistence) | **No analog** in the leading case. Analogs appear with unequal noise (Claim 11(d)). |
| Prop. A.3 | **Survives** (any fixed experiment). Flat between $r_0$ and $r_1$ at the benchmark (Claim 9). |
| Prop. A.4 ($r_N$, $\mathfrak r(k)$, $r_U$, $r_C$) | $r_N$, $\mathfrak r(k)$ and $r_U$ collapse to one cutoff $r^\ast=\mathfrak r(3k/\rho)=1.973212$. Passive off-path beliefs reproduce $r_N=1.747878$ exactly. At $r_C^d$ the tie rule matters as in (A.14), because posterior 1 has positive probability. |
| Blackwell comparison | Survives. |
| Section 4.1, weaker floors | Becomes the default at the benchmark ($c_L=1>g_L(r)$ for $r>0.375$): the entry gain is $(1-2\rho)/6$, not $(1-\rho)/6$. |
| Section 4.3, asymmetric partial orders | No analog in the leading case. One-directional menus remove the cross-direction deviations (Claim 8(a)). |
| Hidden-price control (Section 4.2) | Unchanged: entry $\rho$. |
| Sections 5.1–5.3, 6 | Not studied here. |

---

## 5. Numerical example

**Scripts** (print-only; no assertions). Run from the repository root with `.venv/bin/python <path>`.

- `audit/alex_meeting_2026_10_21/scripts/Q2_discrete_sell_only/q2_leading_case.py`: exact rational arithmetic. Leading case, both menus, off-path belief rules, floors, fixed-experiment control, $\lambda$, stake, and the buy-only menu with $\lambda=3/4$. About 3 seconds.
- `audit/alex_meeting_2026_10_21/scripts/Q2_discrete_sell_only/q2_general_noise.py`: floating point. General noise, an equilibrium finder that handles entry jumps and challenger mixing, and sweeps over $r$. About 2 minutes.

Benchmark vector $(h,\ell,p,\rho,c_L,c_H,k)=(10,1,0.5,0.25,1,6,0.02)$. The discrete model has no $b$. All entries below are numerical diagnostics of the closed forms above.

**Table A. Auction objects and conditions.**

| | $r_0=1.2$ | $r_1=3$ | $r=3.6$ | $r=9$ |
|---|---|---|---|---|
| $\Delta_T$ | 0.016667 | 0.666667 | 0.938889 | 3.555556 |
| $g_L=B(0)$ | 0.312500 | 0.125000 | 0.104167 | 0.041667 |
| $B(1/3)$ | 3.306944 | 2.902778 | 2.791204 | 1.856481 |
| $B(1/2)$ | 4.804167 | 4.291667 | 4.134722 | 2.763889 |
| $g_H=B(1)$ | 9.295833 | 8.458333 | 8.165278 | 5.486111 |
| $\kappa=\rho\Delta_T/3$ vs $k=0.02$ | 0.001389 | 0.055556 | 0.078241 | 0.296296 |

Checks: (S1) $1\le2.902778$. (S2) $4.804167<6\le8.458333$. (S3) $0.001389<0.02<0.055556$. The strong floor $c_L\le g_L(r)$ fails at every strength shown. Part (iii) fails at $r=3.6$ ($g_H=8.165>6$) and holds at $r=9$ ($g_H=5.486<6$).

**Table B. Equilibrium outcomes.**

| | Laplace (paper) | sell-only, $c_L=1$ | sell-only, $c_L=0$ | buy-only, $c_L=1$ | buy-only, $\lambda=3/4$, $c_L=1$ |
|---|---|---|---|---|---|
| $r_0=1.2$: trade; $\mathsf E$ | none; 0.25 | none; 0.25 | none; 0.25 | none; 0.25 | none; 0.25 |
| $r_1=3$: trade | $(1,-1)$ | $(s_H,s_L)=(0,1)$ | $(0,1)$ | $(b_H,b_L)=(1,0)$ | $(1,0)$ |
| $r_1$: $\mathsf E$ | 0.522757 | 0.333333 | 0.375000 | 0.333333 | 0.343750 |
| $r_1$: $\mathsf O_H$ | 0.324192 | 0.250000 | 0.250000 | 0.250000 | 0.218750 |
| $r=3.6$: $\mathsf E$ | 0.25 | 0.333333 | 0.375000 | 0.333333 | 0.343750 |
| $r=9$: $\mathsf E$ | 0.25 ($r>r_C$) | 0.208333 | 0.250000 | 0.208333 | 0.250000 |

Prices at $r_1$ (sell-only, $c_L=1$): $X=-2$: 0.416667 ($=t_0$, no preparation); $X\in\{-1,0\}$: 0.614583; $X=+1$: 1.541667 ($=t_H$). The high-value investor's payoff from a sale is $-0.075556$; the low-value investor's payoff is $+0.035556$.

**Table C. Cutoffs.**

| | Laplace (paper, $b=2$) | discrete (both menus) |
|---|---|---|
| no-trade existence boundary | $r_N=1.747878$ | $r^\ast=1.973212$ (IC, D1); 1.747878 (passive); 1.361535 (adverse) |
| unique no trade below | $\mathfrak r(k)=1.220998$ | $r^\ast=1.973212$ |
| unique full trade above | $r_U=2.837417$ | $r^\ast=1.973212$ |
| high-cost ceiling | $r_C=3.592659$ | $r_C^d=7.968627$ |
| price-sufficiency condition | (A1) $c_L<B_r(m)$: all of $(1,10)$ | (S1) $c_L\le B_r(1/3)$: $r\le14.0887$, i.e. all of $(1,10)$ |
| low-cost preparation at every price | all of $(1,10)$ (same as above) | $c_L\le g_L(r)$: $r\le0.375$, never in $(1,10)$ |

**Knife edge.** At $k=1/18$ and $r=3$, every $s_L\in[0,1]$ is an equilibrium (21 of 21 grid points). Along this continuum entry is $0.25$ at $s_L=0$, $0.2292$ at $s_L=1/2$, $0.375$ at $s_L=3/4$ and $0.3333$ at $s_L=1$.

**General noise.** See the tables in Claim 11(d) and the cases E3–E5 in Claims 8 and 11.

---

## 6. Open issues and risks

1. **The benchmark's $c_L=1$ breaks the low-cost floor at revealing flows.** In both menus at $\lambda=1$, $c_L>g_L(r)$ for every $r>0.375$, so the low-cost challenger stays out after the $L$-revealing flow. The entry gain falls from $(1-\rho)/6$ to $(1-2\rho)/6$ and turns negative for $\rho>1/2$; part (iii) gives $5\rho/6<\rho$. This interacts with point 4: in the discrete model with $\lambda=1$, $c_L=1$ is not a harmless unit choice. $c_L=0$, or the buy-only menu with $\lambda<1$, avoids the problem.
2. **The high-cost ceiling moves.** Part (iii) needs $r_2>7.968627$ at the benchmark.
3. **The clean leading case is a knife edge in the noise law.** The single cutoff and the absence of feedback rely on exactly equal noise probabilities. A small asymmetry makes camouflage flows informative. If a preparation threshold lies near a camouflage posterior, coexistence and challenger mixing return (Claim 11). A referee may call the leading case non-generic. The sufficient bounds of Claim 11(f) answer this only in part.
4. **Price observation needs (S1).** Without it, self-fulfilling pooled prices add equilibria. EGJ sidestep the issue by letting the decision maker see order flow.
5. **Off-path beliefs.** Only part (i) uses the Intuitive-Criterion belief, and at the benchmark part (i) holds under every belief. In general, a passive belief leaves a gap of strengths with no equilibrium (at the benchmark, $(1.748,1.973)$).
6. **The sell-only menu has a weak economic reading.** It is a short-only menu. The stake reading breaks full selling at the benchmark (Claim 14).
7. **What the discrete leading case cannot show:** Proposition 3 and the asymmetric continuation; the smooth comparative statics through $x^\ast$; a continuous response of entry to $c_H$; the Laplace-versus-logistic tail comparison of Section 5.1.
8. **Not studied:** atomless costs and value classes in the discrete model; complementary signals (Section 5.3); welfare and price access (Section 6.1) beyond the hidden-price entry; reserve comparisons (Section 6.3). The general-noise correspondence is a numerical diagnostic only: grid step 0.005 in $r$, roots by bisection, jumps detected by sign changes. **Open.**
9. **Citation.** EGJ section and equation numbers come from the April 2015 working-paper version; check them against the AER version before you cite them.

---

## 7. Recommendation

In priority order:

1. **If the paper adds a discrete model, use the buy-only menu with equal noise probabilities and investor presence $\lambda\in(0,1)$** (EGJ's device). State Proposition 2d for it under (B1) $c_L\le B_{r_1}(m_\lambda)$, (S2) $B_{r_0}(1/2)<c_H\le g_H(r_1)$, and (S3). Report $r^\ast=\mathfrak r(3k/\rho)$, $\mathsf E=\rho+\lambda(1-\rho)/6$ and $\mathsf O_H=\rho/2+\lambda(1-\rho)/6$. Reasons: it matches short-sale constraints; informed buying produces the recruiting flow; the bad-news flow is not revealing, so the floor keeps the paper's form; the benchmark $c_L=1$ works without change; and all additional entry is high-value entry.
2. **Keep the Laplace model as the main model and present the discrete model as a transparent companion** (one subsection after Proposition 2, or an appendix section). The discrete leading case shuts down the feedback from entry to trading. So it cannot carry Proposition 3, the asymmetric continuation, or the tail comparison of Section 5.1. Say this in the text. It also helps with the first half of point 2: the discrete model shows that the main result does not need Laplace noise, and it shows what Laplace adds (informative camouflage flows, hence feedback and coexistence).
3. **Mention the sell-only menu in one paragraph as the mirror case** (Claim 13). At $\lambda=1$ the outcomes are identical, so the result does not depend on which side can trade. Do not lead with it: it is a short-only menu, and the stake reading fails at the benchmark.
4. **State the off-path rule** (Intuitive Criterion; D1 gives the same belief here) and note that only part (i) uses it.
5. **State the price-sufficiency condition explicitly** (the pooled-posterior floor) and cite EGJ's Section 2.2 remark on self-fulfilling prices to explain why it is needed when the challenger sees only the price.
6. **If the author keeps $\lambda=1$,** report entry with and without $c_L\le g_L(r)$, and do not normalize $c_L=1$ without a comment (point 4).
7. **For a discrete analog of Proposition 3,** use symmetric unimodal noise, for example $(1/4,1/2,1/4)$, and allow the challenger to mix at indifference. This loses the clean cutoff, so treat it as an extension.

**What the discrete specification costs relative to the Laplace model:** off-path flows and a refinement; posteriors at 0 and 1, which move the floor and the ceiling; a coarse entry response with no $x^\ast$; no feedback from entry to trading in the leading case, hence no coexistence result; a flat fixed-experiment control at the benchmark; lower entry gains at the benchmark (0.333 to 0.375 against 0.523). **What it gains:** an exact cutoff with single crossing, uniqueness without a global derivative bound, two-line closed forms, a standard and familiar setup, and no need to justify Laplace noise for the main result.

---

## 8. Plain summary

The supervisor asked whether the paper can use a simple discrete order-flow model, as in Edmans, Goldstein and Jiang (2015), with trades in one direction only. I studied the version in which the informed investor can only sell.

In the simplest version, noise traders buy, sell, or do nothing, with equal chances. Only the two extreme flows are informative. A very low flow shows that the investor sold, so the news is bad. A high flow can occur only if nobody sold, so the news is good. The challenger learns good news from the absence of a sale.

This model gives a clean version of the main result. With a weak incumbent, nobody trades and only the low-cost challenger prepares. With a strong incumbent, the investor with bad news always sells, and the expensive challenger prepares after the high flow. One cutoff separates the two cases, and each case has exactly one equilibrium. At the paper's benchmark, entry rises from 0.25 to 0.333 (0.375 if the low cost is zero), and the chance that a high-value challenger wins rises from 0.125 to 0.25.

The model has costs. Beliefs can reach certainty. So the low-cost challenger stays out after clearly bad news, and the expensive challenger keeps preparing until the incumbent is much stronger. The flows that recruit the challenger never pay the trader, so entry never feeds back into trading. That removes the paper's coexisting equilibria. Unequal noise chances bring the feedback back, but also multiple equilibria and, under the paper's tie rule, cases with no equilibrium.

A buy-only menu gives the same results and is more natural, because short sales are the restricted trade. I recommend a buy-only discrete model, with an investor who is present only sometimes, as a companion to the Laplace model, not a replacement.

---

### References checked

- Edmans, A., I. Goldstein and W. Jiang (2015). "Feedback Effects, Asymmetric Trading, and the Limits to Arbitrage." *American Economic Review* 105(12): 3766–3797. I read the April 2015 ECGI working-paper version (Finance Working Paper 318/2011): Section 2.2 (presence probability $\lambda$; noise $z\in\{-1,0,1\}$ with equal probability; trading cost $\kappa$ with no trade at indifference; the manager observes order flow, not the price, to avoid self-fulfilling prices), Section 2.3 (PBE with the Intuitive Criterion), the proof of Proposition 1 (off-path beliefs at $X=\pm2$; posterior tables for the four equilibria), Sections 3.3.2, 3.5.2 (feedback affects profits only at $X=\pm1$; $\lambda=1$ removes the asymmetry), 3.5.3 (initial stake, Appendix B.2) and 3.5.4 (corrective versus amplifying actions). Section numbers in the journal version may differ.
- Cho, I.-K. and D. M. Kreps (1987). "Signaling Games and Stable Equilibria." *Quarterly Journal of Economics* 102: 179–221. Bibliographic record checked; I did not re-read the text of the Intuitive Criterion or D1 definitions.
- Banks, J. S. and J. Sobel (1987). "Equilibrium Selection in Signaling Games." *Econometrica* 55(3): 647–661. Abstract checked (divine equilibrium). Cited only as background for D1-type refinements.
