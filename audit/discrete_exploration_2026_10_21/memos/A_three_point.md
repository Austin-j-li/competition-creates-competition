# A1. The three-point model, consolidated

Workstream A1 (brief, Question A). Scripts: `scripts/A_three_point/`. Checker: A2 (`memos/A_bruteforce.md`).

## 1. Question

The brief asks for a consolidated account of the three-point model:

- equal noise $Z\in\{-1,0,1\}$, each value with probability $1/3$;
- buy-only orders $q\in\{0,1\}$;
- an informed investor present with probability $\lambda\in(0,1]$;
- Reading N with prior $\pi$ on the high class;
- $c_L=0$;
- a challenger that sees the price, not the flow.

This memo gives four things:

1. the complete equilibrium set, with mixed investor strategies, challenger mixing, both investor tie rules, and explicit off-path beliefs;
2. entry, ownership, proceeds, price informativeness, investor profit and welfare in every region of the parameter space;
3. a verdict on every paper result (Props. 1–3, A.1–A.10, Sections 4–7);
4. the exact mechanism of each loss, stated as what a modification must supply.

**Base model.** This is the three-point model of TEAM_RULES §4, item 1. It is Question A itself. The other workstreams measure their modifications against it.

## 2. Setup

### 2.1 Primitives

**Auction stage.** The auction is the one in the paper (Section 2.2). I checked the objects against equation (4) of the pinned `main.tex`. With $0<p<\ell<r<h$,

$$
t_0=p\Big(1-\frac pr\Big),\quad t_H=\frac r2+\frac{p^2}{2r},\quad t_L=\ell-\frac{\ell^2-p^2}{2r},\quad
g_H=h-\frac r2-\frac{p^2}{2r},\quad g_L=\frac{\ell^2-p^2}{2r},\quad \Delta_T=\frac{(r-\ell)^2}{2r}.
$$

Write $w_H=t_H-t_0$, $w_L=t_L-t_0>0$, and $B_r(\mu)=g_L+\mu(g_H-g_L)$. The script `tp_first_principles.py` computes all of these from the piecewise integrals of Appendix (A.1). It does not use the closed forms.

**Reading N.** Nature draws the class $j\in\{H,L\}$ with $\Pr(H)=\pi\in(0,1)$. The investor sees the class. Preparation reveals the value. The benchmark uses point masses at $h$ and $\ell$.

- Scope. Every trading-stage argument below uses only $(t_0,t_H,t_L,g_H,g_L)$.
- With general value laws $G_j$, replace these by class averages. The results then hold verbatim if $\Delta_T>0$, $g_H>g_L$ and $g_L>0$.
- Ownership and welfare formulas use point masses with $h>r$. A prepared high-class challenger then always wins.

**Costs.** The preparation cost is $c_L=0$ with probability $\rho\in(0,1)$ and $c_H>0$ otherwise. Since $p<\ell$, $g_L>0$, so $B_r(\mu)\ge g_L>0=c_L$ at every belief. The low-cost type therefore strictly prefers to prepare after every price.

**Investor.** The investor is present with probability $\lambda$, sees the class, and chooses $q\in\{0,1\}$.

- Its payoff is $q(V_T-P)-kq$ with $k>0$. It has no initial stake.
- A present investor of class $j$ buys with probability $\beta_j$. Write $s_j=\lambda\beta_j$ for the effective purchase probability.
- An absent investor sends $q=0$.

**Noise, pricing and the challenger.** The noise $Z$ is independent of everything. The flow is $X=q+Z\in\{-1,0,1,2\}$. Competitive market makers see $X$ and set $P(X)=\mathbb E[V_T\mid X]$. The challenger sees $P$ and its own cost, not $X$.

**The menu is imposed.** I impose buy-only orders and do not derive them. The prior check of the two-sided menu (`V_discrete_check.md`, §3.3–3.5) finds three problems: a partial-trade cost interval, mixed equilibria inside it, and two price schedules for the same trades at $c_L=1$.

### 2.2 Equilibrium concept

I use perfect Bayesian equilibrium (PBE). It has four parts:

1. the investor best-responds to the fixed candidate price and entry schedule;
2. the price at each flow is competitive, given the entry that this price induces;
3. preparation is optimal, given the challenger's posterior at the observed price;
4. beliefs follow Bayes' rule at every price that has positive probability.

### 2.3 Off-path beliefs

Result 1 shows that only one flow can be unused: $X=2$ under no trade. At this flow I use one belief $v\in[0,1]$, which market makers and the challenger share.

- The price at $X=2$ is then $t_0+e(v)(w_L+\Delta_Tv)$. It reveals the deviation unless $v=\pi$, because Result 3 makes prices strictly increasing in beliefs.
- PBE alone does not force a shared belief. I adopt this as a modelling choice.

I compare three belief rules:

- the Intuitive-Criterion completion, $v=1$ (Result 5 justifies it);
- the passive belief, $v=\pi$;
- a general belief $v$.

### 2.4 Tie rules

- **Investor, rule Z:** a tied investor chooses $q=0$. This is the prior work's rule.
- **Investor, rule M:** a tied investor may mix in any proportion.
- **Challenger, rule E:** a tied challenger prepares. This is the paper's rule.
- **Challenger, rule X:** a tied challenger may mix. The mixing probability can differ across prices.

Ties of the low-cost type never occur when $p<\ell$. They occur only in the reserve case $p>\ell$, where $g_L=0$, at posterior $0$ (Result 13).

### 2.5 Notation

- Threshold belief: $\tau=(c_H-g_L)/(g_H-g_L)$, so that $B_r(\mu)\ge c_H\iff\mu\ge\tau$.
- Lowest posterior under full buying: $m_\lambda=\pi(1-\lambda)/(1-\pi\lambda)$, which is $0$ at $\lambda=1$.
- Trading cutoffs: $K_\rho=\tfrac23\rho(1-\pi)\Delta_T$ and $K_1=\tfrac23(1-\pi)\Delta_T$.
- Spread inverse: $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$, the root above $\ell$ of $\Delta_T(r)=d$.
- Cost crossing: $r_C(\mu)$ is the larger root of $B_r(\mu)=c_H$,
$$
r_C(\mu)=\frac{\mu h-c_H+\sqrt{(\mu h-c_H)^2+\mu[(1-\mu)\ell^2-p^2]}}{\mu}\ (\mu>0),\qquad r_C(0)=\frac{\ell^2-p^2}{2c_H},\qquad r_C(1)=h-c_H+\sqrt{(h-c_H)^2-p^2}.
$$
  The formula follows from $B_r(\mu)=\mu h-\mu r/2+[(1-\mu)\ell^2-p^2]/(2r)$. $B_r(\mu)$ is strictly decreasing in $r$ for $r>p$.
- Entry $\mathsf E$ is the preparation probability. High-class ownership is $\mathsf O_H=\pi e_H$, where $e_H$ is entry conditional on the high class.
- Target proceeds are $\mathcal R_T=t_0+\pi e_Hw_H+(1-\pi)e_Lw_L$.
- Welfare $\mathcal W$ is acquisition surplus net of preparation costs (Online Appendix (OA.49)), with only the $c_H$ cost term because $c_L=0$:
$$
\mathcal W=\frac{r^2-p^2}{2r}+\pi e_H\Big(g_H+\frac{p^2}r\Big)+(1-\pi)e_L\Big(g_L+\frac{p^2}r\Big)-c_H\Pr(\text{high-cost preparation}).
$$
  As in the paper, $\mathcal W$ excludes the trading cost. I report the trading cost $\lambda\pi\beta_Hk$ separately.
- Price informativeness is reported two ways: the price experiment in the Blackwell order, and the posterior variance $\mathrm{Var}(\mu_P)$.

## 3. Results

### Result 1 (analytical). Flow laws and posteriors for every profile

For every $(\beta_H,\beta_L)\in[0,1]^2$, the flow laws are:

| Flow $x$ | $\Pr(x\mid j)$ | Posterior $\mu_x$ |
|---|---|---|
| $-1$ | $(1-s_j)/3$ | $\pi(1-s_H)/[\pi(1-s_H)+(1-\pi)(1-s_L)]$ |
| $0$ | $1/3$ | $\pi$ |
| $1$ | $1/3$ | $\pi$ |
| $2$ | $s_j/3$ | $\pi s_H/[\pi s_H+(1-\pi)s_L]$ |

*Derivation.* $X=0$ arises from $(q,z)=(0,0)$ or $(1,-1)$, so its probability is $(1-s_j)/3+s_j/3=1/3$. $X=1$ arises from $(0,1)$ or $(1,0)$, also with probability $1/3$. $X=-1$ needs $(0,-1)$. $X=2$ needs $(1,1)$. Bayes' rule with prior $\pi$ gives the posteriors. $\square$

Three consequences follow:

- The interior flows $0$ and $1$ carry no information under every pure or mixed profile, for every $\lambda$ and $\pi$.
- Flow $2$ is unused if and only if $s_H=s_L=0$.
- Flow $-1$ is unused if and only if $s_H=s_L=1$.

### Result 2 (analytical). The low class never buys

**Claim.** In every PBE, under every belief system and both tie rules, $\beta_L=0$.

*Proof.* Let $e(x)\in[0,1]$ be cost-averaged entry at the price of flow $x$. It depends only on the price and the cost, and the cost is independent of the class, so $\mathbb E[V_T\mid j,x]=t_0+e(x)(t_j-t_0)$. Challenger mixing does not change this, because the mixing probability is a function of the price.

The competitive price is $P(x)=t_0+e(x)[w_L+\Delta_T\mu(x)]$, where $\mu(x)$ is the belief at $x$, on or off path. Subtraction gives

$$
V_H(x)-P(x)=e(x)\Delta_T[1-\mu(x)]\ge0,\qquad V_L(x)-P(x)=-e(x)\Delta_T\mu(x)\le0.
$$

So a purchase by the low class earns at most $-k<0$, and zero earns zero. $\square$

From now on, write $s=\lambda\beta_H$. Result 1 then gives

$$
\mu_{-1}(s)=\frac{\pi(1-s)}{1-\pi s},\quad \mu_0=\mu_1=\pi,\quad \mu_2=1\ (s>0);\qquad
w_{-1}=\frac{1-\pi s}3,\quad w_0=w_1=\frac13,\quad w_2=\frac{\pi s}3,
$$

where $w_x$ is the unconditional flow probability. Flow $-1$ is always used, because the low class reaches it with probability $1/3$. Only flow $2$ can be unused, and only under no trade.

### Result 3 (analytical). With $c_L=0$ the price reveals the flow posterior, unconditionally

**Claim.** In every candidate equilibrium:

- (a) entry is at least $\rho$ at every price;
- (b) two flows share a price only if they share a posterior, so no zero-entry pool exists;
- (c) the price is strictly increasing in the posterior, under either challenger rule;
- (d) the challenger's posterior at the price of flow $x$ equals $\mu_x$.

Flows with equal posteriors share one price under rule E. Under rule X, flows whose posterior equals $\tau$ may carry different prices with different mixing.

*Proof.*

- (a) The low-cost type strictly prepares, by §2.1.
- (b) Suppose $P(x)=P(x')$. Entry $e$ is a function of the price, so it is common to both flows. Then $e[w_L+\Delta_T\mu_x]=e[w_L+\Delta_T\mu_{x'}]$ with $e\ge\rho>0$. So $\mu_x=\mu_{x'}$.
- (c) Every best response is nondecreasing in the belief. The low-cost type always prepares. The high-cost type prepares above $\tau$, stays out below, and may mix at $\tau$. Take $\mu<\mu'$ with best-response entry $e\le e'$. Then
$$P'-P=e'\Delta_T(\mu'-\mu)+(e'-e)(w_L+\Delta_T\mu)\ge\rho\Delta_T(\mu'-\mu)>0.$$
- (d) Under rule E, entry is a function of the posterior, so equal posteriors give equal prices. Under rule X, a price with posterior $\tau$ leaves the high-cost type indifferent, so any mixing probability is optimal there. Different probabilities give different prices, and each price is consistent. $\square$

**Comparison.**

- The paper's Proposition A.2 needs $c_L<B_r(m)$.
- At $c_L=1$, the prior work needs the pooled-posterior condition $c_L\le B_r(1/3)$. It finds extra zero-entry pools when that condition fails (`Q2_discrete_buy_only.md`, Claim 6).
- At $c_L=0$, no condition is needed. This is an effect of $c_L$, not of discreteness: Laplace noise with $c_L=0$ also excludes all zero-entry pools.

### Result 4 (analytical). The buyer's payoff does not depend on the purchase probability

**Claim.** Let $e_0$ and $e_1$ denote entry at the prices of flows $0$ and $1$. For every $s>0$,

$$
U_H(\text{buy})=\frac{e_0+e_1}3(1-\pi)\Delta_T-k.
$$

*Proof.* A purchase reaches flows $0,1,2$ with probability $1/3$ each. The residual at flow $x$ is $e_x\Delta_T(1-\mu_x)$ (Result 2). Here $\mu_0=\mu_1=\pi$, and $\mu_2=1$ makes the third residual zero. $\square$

Three corollaries follow:

1. $U_H(\text{buy})$ depends on neither $s$, $\lambda$, $e_{-1}$ nor $e_2$.
2. Under rule E, $e_0=e_1=\bar e:=\rho+(1-\rho)\mathbf 1\{\tau\le\pi\}$. So $U_H(\text{buy})=K-k$ with $K=\tfrac23\bar e(1-\pi)\Delta_T\in\{K_\rho,K_1\}$.
3. **No feedback.** Suppose the challenger cannot see the price. It then uses the prior and prepares with probability $e_r(\pi)$ at every flow. The market maker still sees flow $2$, so the residual there is still zero. The purchase payoff is again $K-k$. Anticipated entry neither raises nor lowers the gain from buying on good news.

### Result 5 (analytical). Off-path beliefs at the unused top flow

This result concerns no trade, $s=0$, in which flow $2$ is unused. Let $e(v)$ be entry at the off-path price under belief $v$ (rule E: $e(v)=\rho+(1-\rho)\mathbf 1\{v\ge\tau\}$).

**(a) Deviation value.** A purchase earns
$$
U^{\rm dev}_H(v)=\frac13\big[(e_0+e_1)(1-\pi)+e(v)(1-v)\big]\Delta_T-k.
$$

**(b) Intuitive Criterion and D1.**

- A purchase by the low class is equilibrium-dominated. It earns at most $-k$ under every response (Result 2), and the low class earns $0$ in no trade.
- If some response makes the high-class purchase profitable, the criterion gives the low class zero weight, so $v=1$.
- If no response does, the criterion is silent, and every $v$ supports no trade.
- D1 gives $v=1$ in the same cases. When the set of responses that make the purchase weakly profitable is nonempty for the high class, it is empty for the low class. When it is empty for both, D1 is silent, like the criterion.
- I complete the belief with $v=1$ in every case. Then $U^{\rm dev}_H(1)=K-k$, the same as the purchase payoff for every $s>0$ (Result 4).

**(c) Existence of no trade.** Under rule E, the following are equivalent:

- no trade is a PBE outcome for some belief;
- no trade survives the Intuitive Criterion;
- $k\ge K$.

The reason is that $e(v)(1-v)\ge0$, with equality at $v=1$.

**(d) The supporting set.** Write $\delta=3(k-K)/\Delta_T\ge0$. No trade is supported by belief $v$ if and only if $e(v)(1-v)\le\delta$. Under rule E, the supporting set is
$$
\{v\ge\tau:\ v\ge1-\delta\}\ \cup\ \{v<\tau:\ v\ge1-\delta/\rho\}.
$$
It always contains $v=1$.

**(e) Passive beliefs.** With $v=\pi$, no trade requires $k\ge\bar e(1-\pi)\Delta_T=\tfrac32K$. For $K<k<\tfrac32K$, **no equilibrium exists under passive beliefs**:

- trade fails, because $k>K$ (Result 4);
- no trade fails, because the deviation earns $\tfrac32K-k>0$.

At $k=K$ the two investor rules differ:

- under rule Z there is again no equilibrium, because the tied investor must choose zero, and no trade fails;
- under rule M every $\beta_H\in(0,1]$ is an equilibrium.

This is the prior work's factor $3/2$, now shown for every $\pi$ and $\lambda$. At $\pi=1/2$ the passive condition is $\rho\Delta_T/2\le k$, which is the paper's Laplace condition in Proposition A.4. Under Laplace noise every flow that a deviation reaches is on path and keeps the prior.

**(f) Other beliefs.**

- The adverse belief $v=0$ has $e(0)=\rho$, because $c_L=0$. No trade then requires $k\ge\tfrac13[2\bar e(1-\pi)+\rho]\Delta_T$.
- No trade survives every belief if and only if $k\ge\tfrac13[2\bar e(1-\pi)+\max_ve(v)(1-v)]\Delta_T$. Here $\max_ve(v)(1-v)$ equals $\max\{\rho,1-\tau\}$ if $0<\tau\le1$, $\rho$ if $\tau>1$, and $1$ if $\tau\le0$.

**(g) Benchmark cutoffs in $r$** ($\bar e=\rho$; `tp_cutoffs.out.txt`):

| Belief rule | No-trade boundary | Value |
|---|---|---|
| Intuitive Criterion, $v=1$ | $\mathfrak r(6/25)$ | $1.973212111$ |
| passive, $v=\pi$ | $\mathfrak r(4/25)$ | $1.747877538$ (the paper's $r_N$) |
| adverse, $v=0$ | $\mathfrak r(3/25)$ | $1.624380809$ |
| robust to every belief | root of $\tfrac13[\rho+\max(\rho,1-\tau(r))]\Delta_T(r)=k$ | $1.556594423$ |

At $r_0=1.2$ the largest deviation value is $\tfrac13[2\rho(1-\pi)+1]\Delta_T=1/144<k=1/50$. So Proposition 2(i) at the benchmark holds under every belief rule.

**Correction to the brief.** The brief says that "the Intuitive-Criterion belief at the off-path top flow is needed for existence". The precise statement has three parts:

- On $k\in(K,\tfrac32K)$, and at $k=K$ under rule Z, existence needs a belief in the supporting set (d): a belief close to $1$.
- PBE with $v=1$ suffices. The Intuitive Criterion and D1 select that belief.
- Passive beliefs leave no equilibrium there.

### Result 6 (analytical). The complete equilibrium correspondence

**Regions.** Order the threshold belief $\tau$ against the three attainable posteriors $m_\lambda\le\pi<1$:

| Region | Condition on $\tau$ | Condition on $c_H$ | Condition on $r$ |
|---|---|---|---|
| I | $\tau\le m_\lambda$ | $c_H\le B_r(m_\lambda)$ | $r\le r_C(m_\lambda)$ |
| II | $m_\lambda<\tau<\pi$ | $B_r(m_\lambda)<c_H<B_r(\pi)$ | $r_C(m_\lambda)<r<r_C(\pi)$ |
| III (knife-edge) | $\tau=\pi$ | $c_H=B_r(\pi)$ | $r=r_C(\pi)$ |
| IV | $\pi<\tau\le1$ | $B_r(\pi)<c_H\le g_H(r)$ | $r_C(\pi)<r\le r_C(1)$ |
| V | $\tau>1$ | $c_H>g_H(r)$ | $r>r_C(1)$ |

**How to read the region table.**

- $\tau$ is strictly increasing in $r$, because $B_r(\mu)$ is strictly decreasing in $r$ at every $\mu$. It is linear and increasing in $c_H$.
- If a crossing $r_C(\mu)$ lies outside $(\ell,h)$, the corresponding region is empty or fills the whole domain.
- Region I includes $\tau\le0$, that is, $c_H\le g_L$. There the high-cost type prepares at every belief.
- At $\lambda=1$, Region I is $\{c_H\le g_L\}$, because $m_1=0$.
- $\lambda$ enters only through $m_\lambda$. $\pi$ enters through $m_\lambda$, the boundary at $\pi$, and the cutoff $K$.
- The cutoff is $K=K_1$ in Regions I–III and $K=K_\rho$ in Regions IV–V.
- In $r$: trade occurs if and only if $r>\mathfrak r\big(3k/(2(1-\pi))\big)$ in Regions I–III, and if and only if $r>\mathfrak r\big(3k/(2\rho(1-\pi))\big)$ in Regions IV–V.
- So the trade set in $r$ need not be an interval. Suppose $r_C(\pi)$ lies between the two spread thresholds. Then trade switches on, stops at $r_C(\pi)$ where $K$ drops from $K_1$ to $K_\rho$, and resumes later. Example with $c_H=4$, $k=1/5$, $\pi=1/2$: trade at $r=3$, no trade at $r=5$, trade at $r=7$ (`tp_check_pair.out.txt`, item 6).

**Theorem.** Assume the Intuitive-Criterion completion.

**(a) Rules Z and E.** The equilibrium is unique for every parameter vector:
$$
\beta_L=0,\qquad \beta_H=\begin{cases}1,&k<K,\\0,&k\ge K.\end{cases}
$$
On-path prices and entry are unique.

**(b) Rules M and E.** The equilibrium is the same as in (a), except at $k=K$. There every $\beta_H\in[0,1]$ is an equilibrium.

**(c) Challenger rule X.** Rule X adds equilibria only where an on-path posterior equals $\tau$:

- **(c1) Region III ($\tau=\pi$).** Entry at flows $0$ and $1$ is $e_x=\rho+(1-\rho)\xi_x$, with $\xi_x\in[0,1]$. The two values may differ only if the two prices differ. Under no trade, flow $-1$ also has posterior $\pi$, so its entry is free as well. The purchase payoff $\tfrac13(e_0+e_1)(1-\pi)\Delta_T-k$ then ranges over $[K_\rho-k,K_1-k]$. Consequently:
  - no trade is an equilibrium if and only if $k\ge K_\rho$;
  - full buying is an equilibrium if and only if $k<K_1$ (rule Z) or $k\le K_1$ (rule M);
  - interior $\beta_H$ (rule M only) is an equilibrium if and only if $K_\rho\le k\le K_1$.

  So no trade and full buying **coexist for $k\in[K_\rho,K_1)$**, but only at the single strength $r=r_C(\pi)$.
- **(c2) Region IV boundary ($\tau=1$).** For $s>0$, entry at flow $2$ can take any value in $[\rho,1]$. Investor behavior does not change, because the residual at flow $2$ is zero.
- **(c3) The point $\mu_{-1}(s)=\tau$.** This holds at $s^*=(\pi-\tau)/[\pi(1-\tau)]$, which lies in $(0,\lambda]$ when $m_\lambda\le\tau<\pi$. Entry at flow $-1$ can take any value in $[\rho,1]$, and investor behavior does not change.
  - Under full buying, this case arises only at $\tau=m_\lambda$.
  - Under rule M at $k=K_1$, it arises at $\beta_H=s^*/\lambda$.

**(d) Passive beliefs.** No trade is an equilibrium if and only if $k\ge\tfrac32K$, and full buying if and only if $k<K$. Under rule Z, no equilibrium exists for $K\le k<\tfrac32K$. Under rule M, $k=K$ admits every $\beta_H\in(0,1]$, and no equilibrium exists for $K<k<\tfrac32K$. At the prior tie (c1) with rule X, no trade needs $k\ge\tfrac32K_\rho$, so coexistence holds for $k\in[\tfrac32K_\rho,K_1)$.

*Proof.*

- Result 2 gives $\beta_L=0$, and Result 3 gives the price posteriors.
- For $s>0$, the purchase payoff is constant in $s$ (Result 4). Under no trade, it equals the deviation value under the completion (Result 5).
- There are only two actions, so this comparison decides every case. For $k<K$, buying beats zero against every candidate schedule, so no trade fails and $s=\lambda$. For $k>K$, zero is strictly better, so $s=0$. At $k=K$ the investor is tied, and the tie rule decides.
- Existence: the canonical schedule $P_x=t_0+e_x(w_L+\Delta_T\mu_x)$ with $e_x=e_r(\mu_x)$ is consistent, by Result 3(c).
- For (c): ties occur only at on-path posteriors in $\{\mu_{-1}(s),\pi,1\}$. Only $e_0$ and $e_1$ enter $U_H$. $\square$

**Checks** (computer-assisted, exact rationals; `tp_compare.out.txt`). The first-principles solver enumerates every partition of the used flows into price blocks. It does so on a grid of $(\beta_H,\beta_L)$ that includes $\beta_L>0$. At all 33 listed points it finds exactly the equilibria of the theorem. At every rule-E point, the closed forms differ from it by exactly zero. The rule-X points reproduce the ranges in (c). The points cover:

- the knife-edges $k=K$, $\tau=\pi$, $\tau=1$ and $\mu_{-1}=\tau$;
- the passive-belief gap;
- the prior-work values at $c_L=1$.

### Result 7 (analytical). Outcomes in every region

**Common to every region.** Let $s$ be the effective purchase probability: $s=\lambda$ under full buying, $s=0$ under no trade, $s=\lambda\beta_H$ under a mixture.

- **Price informativeness.** $\mathrm{Var}(\mu_P)=\pi s(1-\pi)^2/[3(1-\pi s)]$, which is $1/12$ at $\pi=1/2,\ s=1$.
- **Blackwell order.** The experiment is Blackwell-increasing in $s$. The experiment at $s'<s$ is a garbling of the one at $s$: send flow $2$ to flow $-1$ with probability $1-s'/s$. This reproduces both class laws of Result 1.
- *Derivation of the variance.* $\mathbb E[\mu^2]-\pi^2=\tfrac13[\pi^2(1-s)^2/(1-\pi s)+\pi s]-\tfrac13\pi^2$. Over the common denominator, the numerator is $\pi s(1-\pi)^2$.
- **Investor profit.** The ex ante profit is $\lambda\pi\beta_H(K-k)$. Noise traders lose the gross profit $\lambda\pi\beta_HK$ in expectation, and the trading cost is $\lambda\pi\beta_Hk$.

**Base levels.** Write

$$
\mathcal R_\rho=t_0+\rho[\pi w_H+(1-\pi)w_L],\qquad \mathcal W_\rho=\frac{r^2-p^2}{2r}+\rho\Big[\pi g_H+(1-\pi)g_L+\frac{p^2}r\Big],
$$
$$
\mathcal R_1=\pi t_H+(1-\pi)t_L,\qquad \mathcal W_1=\mathcal W_\rho+(1-\rho)\Big[B_r(\pi)-c_H+\frac{p^2}r\Big].
$$

**General identity.** $\mathcal W=\mathcal W_\rho+\sum_xw_x(e_x-\rho)[B_r(\mu_x)-c_H+p^2/r]$, because $\sum_xw_xe_xB_r(\mu_x)=\pi e_Hg_H+(1-\pi)e_Lg_L$.

**Outcomes under rule E:**

| Region | Entry by flow $(-1,0,1,2)$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | $\mathcal W$ |
|---|---|---|---|---|---|
| I | $(1,1,1,1)$ | $1$ | $\pi$ | $\mathcal R_1$ | $\mathcal W_1$ |
| II, III; trade with $s>s^*$ | $(\rho,1,1,1)$ | $1-\tfrac{(1-\rho)(1-\pi s)}3$ | $\pi\big[1-\tfrac{(1-\rho)(1-s)}3\big]$ | $\mathcal R_1-\tfrac{1-\rho}3[\pi(1-s)w_H+(1-\pi)w_L]$ | $\mathcal W_1+(1-\rho)w_{-1}[c_H-\tfrac{p^2}r-B_r(\mu_{-1})]$ |
| II, III; no trade, or $s\le s^*$ | $(1,1,1,\cdot)$ | $1$ | $\pi$ | $\mathcal R_1$ | $\mathcal W_1$ |
| IV | $(\rho,\rho,\rho,1)$ | $\rho+\tfrac{(1-\rho)\pi s}3$ | $\pi\big[\rho+\tfrac{(1-\rho)s}3\big]$ | $\mathcal R_\rho+\tfrac{(1-\rho)\pi s}3w_H$ | $\mathcal W_\rho+\tfrac{(1-\rho)\pi s}3\big(g_H-c_H+\tfrac{p^2}r\big)$ |
| V | $(\rho,\rho,\rho,\rho)$ | $\rho$ | $\pi\rho$ | $\mathcal R_\rho$ | $\mathcal W_\rho$ |

Region III under rule E behaves like Region II with $s^*=0$. Under rule X, add the ranges of Result 6(c).

**What information does in each region:**

- **Region IV: information creates competition.** Trading raises $\mathsf E$, $\mathsf O_H$, $\mathcal R_T$ and $\mathcal W$. The welfare gain per added preparation is at least $p^2/r$. All added entrants have high class: $\alpha_H=s/3$ and $\alpha_L=0$.
- **Region II: information deters.** Trading lowers $\mathsf E$ and $\mathcal R_T$. It also lowers $\mathsf O_H$ when $\lambda<1$. At $\lambda=1$, $\mathsf O_H$ is unchanged, because the high class never reaches flow $-1$. Welfare rises if and only if $c_H-B_r(\mu_{-1})>p^2/r$: the deterred preparation would lose more than the reserve gain $p^2/r$.
- **Regions I and V: information is irrelevant for entry.**

### Result 8 (analytical). Proposition 2-D: exact conditions

**Statement.** Use equal noise, buy-only orders and $c_L=0$, with any prior $\pi\in(0,1)$ and presence $\lambda\in(0,1]$. Use rules Z and E and the Intuitive-Criterion completion. Fix $\ell<r_0<r_1<h$.

- **(i) Weak incumbent.** At $r_0$, the unique equilibrium is no trade with entry $\rho$ **if and only if**
$$B_{r_0}(\pi)<c_H\quad\text{and}\quad k\ge K_\rho(r_0)=\tfrac23\rho(1-\pi)\Delta_T(r_0).$$
- **(ii) Strong incumbent.** Given (i): at $r_1$, the unique equilibrium is $(\beta_H,\beta_L)=(1,0)$ with entry above $\rho$ **if and only if**
$$k<K_\rho(r_1)\quad\text{and}\quad c_H\le g_H(r_1).$$
  Then $\mathsf E(r_1)=\rho+(1-\rho)\pi\lambda/3$ and $\mathsf O_H(r_1)=\pi\rho+(1-\rho)\pi\lambda/3>\pi\rho=\mathsf O_H(r_0)$. The price at $r_1$ strictly Blackwell-dominates the constant price at $r_0$.
- **(iii) Return.** Given (ii), take $r_2\in(r_1,h)$. Full buying is the unique equilibrium at $r_2$. Entry equals $\rho$ **if and only if** $g_H(r_2)<c_H$, that is, $r_2>r_C(1)$. Such an $r_2<h$ exists if and only if $c_H>h/2-p^2/(2h)$.
- **(iv) Nonemptiness.** The conditions of (i)–(ii) hold on a nonempty set for every $h>\ell$, $\rho$, $\pi$ and $\lambda$. Their strict versions define an open set.

*Proof.*

- (i) If $B_{r_0}(\pi)\ge c_H$, then $\bar e=1$, and every equilibrium has entry above $\rho$. Otherwise $K=K_\rho(r_0)$, and Result 6(a) gives no trade if and only if $k\ge K_\rho(r_0)$.
- (ii) $B_{r_1}(\pi)<B_{r_0}(\pi)<c_H$, so $K(r_1)=K_\rho(r_1)$. Full buying is unique if and only if $k<K_\rho(r_1)$. Entry exceeds $\rho$ if and only if $e_2=1$, that is, $\tau(r_1)\le1$, that is, $c_H\le g_H(r_1)$. Result 7, Region IV, gives the levels.
  - Blackwell: at $r_1$, the price $P(2)$ has probability $\lambda/3$ under $H$ and $0$ under $L$. No garbling of a constant experiment produces a state-dependent law. A constant garbling of the $r_1$ experiment produces the $r_0$ experiment.
- (iii) $K_\rho(r_2)>K_\rho(r_1)>k$, because $\Delta_T$ increases in $r$. Entry is $\rho$ if and only if $e_2=\rho$, that is, $g_H(r_2)<c_H$. $g_H$ decreases to $g_H(h)=h/2-p^2/(2h)$.
- (iv) As $r\downarrow\ell$, $\Delta_T\to0$ and $g_H-g_L\to h-\ell$. So $g_H(\ell)-B_\ell(\pi)=(1-\pi)(h-\ell)>0$.
  - Choose $r_1$ near $\ell$ with $g_H(r_1)>B_\ell(\pi)$. Every $r_0\in(\ell,r_1)$ then has $B_{r_0}(\pi)<B_\ell(\pi)<g_H(r_1)$.
  - Choose $c_H\in(B_{r_0}(\pi),g_H(r_1)]$ and $k\in[K_\rho(r_0),K_\rho(r_1))$. This interval is nonempty because $\Delta_T$ is strictly increasing.
  - Strict inequalities persist under small perturbations. $\square$

**Tie rules and belief rules.**

- Under rule M, the left inequality must be strict: $k>K_\rho(r_0)$.
- Under rule X, part (ii) needs $c_H<g_H(r_1)$ for unique entry.
- Under passive beliefs, part (i) needs $k\ge\tfrac32K_\rho(r_0)$.
- With strict inequalities, no result depends on either tie rule.

**Benchmark** ($\pi=1/2$, $\lambda=1$, $c_H=6$, $k=1/50$):

- $B_{r}(1/2)<6$ on all of $(1,10)$.
- $K_\rho(1.2)=1/720$ and $K_\rho(3)=1/18$.
- $g_H(3)=203/24\ge6$.
- Entry is $1/4\to3/8\to1/4$ at $r=1.2,\ 3,\ 8.5$. At $r=3.6$, entry is still $3/8$, because $r_C(1)=4+\tfrac32\sqrt7=7.968627$.

### Result 9 (analytical). Controls: fixed experiment, hidden price, access to prices

**(a) Fixed experiment (Proposition A.3 analog).** Fix the order profile and the noise law. By Result 3 the price experiment is then fixed. Entry is weakly decreasing in $r$, because each $B_r(\mu_x)$ falls.

- It falls strictly only when $r$ crosses $r_C(\mu)$ for an attained posterior $\mu\in\{\mu_{-1}(s),\pi,1\}$.
- At the benchmark, frozen full buying gives entry $3/8$ at both $r_0=1.2$ and $r_1=3$. The control is flat. The whole rise from $1/4$ to $3/8$ comes from the change of experiment.

**(b) Hidden price.** The challenger uses the prior, so entry is $e_r(\pi)$ at every flow, which equals $\rho$ at both benchmark strengths. By Result 4(3), the purchase incentive is the same as with feedback. Trading is therefore identical in the two economies: no trade at $r_0$, full buying at $r_1$.

**(c) Access to prices (Proposition A.9 analog).** Compare the same $r$ with and without price access. Orders coincide by (b).

- **Region IV:**
$$
\Delta\mathcal R_T=\frac{(1-\rho)\pi\lambda}3w_H>0,\qquad
\Delta\mathcal W=\frac{(1-\rho)\pi\lambda}3\Big(g_H-c_H+\frac{p^2}r\Big)\ge\frac{(1-\rho)\pi\lambda}3\frac{p^2}r>0.
$$
  At the benchmark $r_1$: $\Delta\mathcal R_T=9/64=0.140625$ and $\Delta\mathcal W=61/192=0.317708$. The paper's external-dividend diagnostic is therefore $0.140625$ (paper: $0.257809$).
- **Region II:**
$$
\Delta\mathcal R_T=-\frac{1-\rho}3[\pi(1-\lambda)w_H+(1-\pi)w_L]<0,\qquad \Delta\mathcal W=(1-\rho)w_{-1}\Big[c_H-\frac{p^2}r-B_r(m_\lambda)\Big].
$$
  Example: $c_H=4$, $r=3$, $\lambda=1$ gives $\Delta\mathcal R_T=-11/192$ and $\Delta\mathcal W=+91/192$. Price access then lowers proceeds but raises welfare.

### Result 10 (analytical). Equal noise is a knife-edge

**Setting.** Let the noise take values $-1,0,1$ with probabilities $(a,d,c)$, all positive. Keep $\beta_L=0$; Result 2 holds for any noise. Then

$$
1-\mu_0(s)=\frac{(1-\pi)d}{d+\pi s(a-d)},\qquad 1-\mu_1(s)=\frac{(1-\pi)c}{c+\pi s(d-c)}.
$$

A purchase reaches flows $0,1,2$ with probabilities $a,d,c$, and $\mu_2=1$. So, with entry $e_0,e_1$ at the interior flows,

$$
K(s)=(1-\pi)\Delta_T\Big[\frac{ad\,e_0}{d+\pi s(a-d)}+\frac{dc\,e_1}{c+\pi s(d-c)}\Big],\qquad
K_{\rm dev}(0)=(1-\pi)\Delta_T\,\bar e\,(a+d),
$$

where $K_{\rm dev}(0)$ is the no-trade deviation value under the completion $v=1$.

**Lemma.** Suppose entry at flows $0$ and $1$ is constant on $[0,\lambda]$. Then:

- $K$ is constant on $[0,\lambda]$ **if and only if** $a=d=c$;
- if $a\le d\le c$, with one inequality strict, $K$ is strictly increasing;
- if $a\ge d\ge c$, with one inequality strict, $K$ is strictly decreasing.

*Proof.*

- Write $u=\pi s$ and $F(u)=A/(d+u(a-d))+B/(c+u(d-c))$, with $A=ade_0>0$ and $B=dce_1>0$. Then $F'(u)=-A(a-d)/(\cdot)^2-B(d-c)/(\cdot)^2$. The monotone cases follow from the signs.
- Suppose $F'\equiv0$ on an interval.
  - If $a=d$, then $B(d-c)=0$, so $d=c$.
  - If $d=c$, then $a=d$ by the same argument.
  - If $a\ne d$ and $d\ne c$, the identity $A(a-d)(c+u(d-c))^2\equiv-B(d-c)(d+u(a-d))^2$ must hold. The coefficient of $u$ gives $2A(a-d)c(d-c)=-2B(d-c)d(a-d)$, so $Ac=-Bd$. This is impossible, because $A,B,c,d>0$. $\square$

**Consequences.** Use the Intuitive-Criterion completion.

- **$K$ increasing:** for $k\in[K_{\rm dev}(0),K(\lambda))$, no trade and full buying both exist, even under rule Z. Rule M adds an interior root.
- **$K$ decreasing:** for $k\in(K(\lambda),K_{\rm dev}(0))$, no pure equilibrium exists. Rule M has a mixed root. **Rule Z has no equilibrium.**
- An interior posterior can cross $\tau$ as $s$ rises. Recruitment at a camouflage flow then adds a jump in $K$: a strategic complementarity.

**Examples** at $r=3$, benchmark costs, $\pi=1/2$, $\lambda=1$ (`tp_extensions.out.txt`, Section H):

| Noise $(a,d,c)$ | $K_{\rm dev}(0)$ | $K(1)$ | Equilibria at $k=\tfrac12[K_{\rm dev}(0)+K(1)]$, on a 1/20 grid |
|---|---|---|---|
| $(1/3,1/3,1/3)$ | $1/18$ | $1/18$ | knife-edge $k=K$ |
| $(3/10,1/3,11/30)$ | $19/360$ | $199/3591$ | $\beta_H\in\{0,1\}$: coexistence |
| $(1/10,1/5,7/10)$ | $1/40$ | $1/27$ | $\beta_H\in\{0,1\}$: coexistence |
| $(1/4,1/2,1/4)$ | $1/16$ | $1/18$ | none on the grid; rule Z: no equilibrium |
| $(7/10,1/5,1/10)$ | $3/40$ | $31/270$ | $\beta_H\in\{0,1\}$: coexistence through recruitment at flow $0$ for $s\ge164/295$ |

**Reading the examples.**

- The second row moves probability $1/30$ from noise value $-1$ to noise value $+1$. This small change opens a coexistence interval of width $0.0026$ in $k$.
- The fourth row is symmetric and unimodal. Its mixed root under rule M lies off the grid, between two grid points of opposite sign.

### Result 11 (analytical). Complementary private signals (Proposition A.7 analog)

**Setting.** Take $\pi=1/2$. The investor sees $T$ with accuracy $a$, and the buyer sees $Y$ with accuracy $d$; both lie in $(1/2,1)$. Let $\phi_\pm$ be the buyer's posterior maps of (A.27).

**Claim.** In the buy-only three-point model with $c_L=0$:

- (a) After $T=-$ the investor never buys. Its residual is $-(2a-1)\lambda_XD\le0$, as in (A.35).
- (b) After $T=+$, a purchase earns $\tfrac13(2a-1)D(1/2)-k$, with $D=e_L\Delta_T+(e_H-e_L)w_H$ evaluated at public belief $1/2$. Flows $0$ and $1$ keep $\Pr(T=+\mid X)=1/2$. Flow $2$ reveals $T=+$ and pays zero.
- (c) If $B_r(d)<c_H$, then $D(1/2)=\rho\Delta_T$, and the cutoff is $K_{\rm sig}=(2a-1)\rho\Delta_T/3$.
- (d) Under full buying, flow $2$ has public belief $a<1$. High-cost preparation follows $(X=2,Y=+)$ if and only if $B_r(\phi_+(a))\ge c_H$.

**Analog of A.7.** The weak economy has no trade if $k\ge K_{\rm sig}(r_0)$ and $B_{r_0}(d)<c_H$. The strong economy has unique orders $(1,0)$ by signal if $k<K_{\rm sig}(r_1)$ and $B_{r_1}(d)<c_H\le B_{r_1}(\phi_+(a))$. Then
$$
\mathsf E=\rho+(1-\rho)\frac\lambda6[ad+(1-a)(1-d)],
$$
if $B_{r_1}(\phi_-(a))<c_H$.

*Derivation.* Steps 1–3 of the paper's A.7 proof carry over. The flow laws of Result 1 apply with $T$ in place of the class.

**Paper example with $c_L=0$** (A.57; $\rho=0.85$, $c_H=7.14$, $a=0.7$, $d=0.75$):

- $B_{1.1}(0.75)=7.0875<7.14$, so the weak economy has no recruitment at the prior.
- $K_{\rm sig}(1.1)=0.000515<k=0.015<K_{\rm sig}(2.3)=0.041638$.
- $B_{2.3}(0.875)=7.7166\ge7.14>B_{2.3}(0.75)=6.6375$.
- Entry is $0.85\to0.865$ (paper: $0.879438$). The first-principles check gives the same values (Section F).

**Two consequences.**

- An imperfect investor signal ($a<1$) restores an attainable public posterior below one. The recruitment ceiling is then $B_r(\phi_+(a))$, not $g_H$.
- Feedback stays absent, because the revealing flow still pays zero.

### Result 12 (analytical). Bargaining (Proposition A.8) and the discrete trading game

**(a) Survival.** Proposition A.8 concerns the payment stage only. It survives unchanged.

**(b) New: the trading game under bargaining is solvable.** Results 1–6 use only the five auction objects, with $\Delta>0$, $g_H>g_L$ and $g_L>0$. So they apply to the verifiable-value institution with zero reserve:

- $t_0=\eta\,\mathbb E R$;
- $t_\theta=\mathbb E[(1-\eta)\min(R,\theta)+\eta\max(R,\theta)]$;
- $g_\theta=G_{\theta,\eta}$;
- $\Delta_\eta=\eta(h-\ell)+(1-2\eta)\mathbb E(R-\ell)_+$.

For $r>\ell$ and $\eta\in[0,1)$, these objects satisfy the conditions:

- $\Delta_\eta>0$. For $\eta\le1/2$, $\Delta_\eta\ge\eta(h-\ell)+(1-2\eta)\mathbb E(R-\ell)_+>0$. For $\eta>1/2$, $\Delta_\eta\ge(1-\eta)(h-\ell)>0$, because $\mathbb E(R-\ell)_+<h-\ell$.
- $G_{L,\eta}=(1-\eta)\ell^2/(2r)>0$.

**(c) Cutoff.** The cutoff is $K_\eta=\tfrac23\bar e(1-\pi)\Delta_\eta$. Within a region of fixed $\bar e$:

- $K_\eta$ rises with $r$ if and only if $\eta<1/2$, so a stronger incumbent makes trade easier only then;
- $K_\eta$ does not depend on $r$ at $\eta=1/2$;
- $K_\eta$ falls with $r$ if $\eta>1/2$.

**(d) Numbers** ($k=1/50$, benchmark $h,\ell,\rho,c_H$; Section E). At $\eta=1/4$, $K_\eta=0.188$ at $r=1.2$, so even the weak incumbent supports trade. The competition effect on trading then needs $k\in[0.188,0.215)$.

The paper does not solve the trading game under bargaining. The discrete stage makes it solvable in closed form.

### Result 13 (analytical; exact evaluation). The reserve comparison of Section 6.3

**Low class excluded.** With $p=1.1>\ell$, the low class cannot bid. Then $g_L=0$ and $w_L=0$, so $\mathcal R_T=t_0+\pi e_Hw_H$.

- The low-cost type is tied only at posterior $0$. This occurs at flow $-1$ under full buying with $\lambda=1$.
- Rule E keeps $e\ge\rho$, so Results 1–7 apply.
- Under rule X, entry at flow $-1$ can fall to $0$. Proceeds do not change, because $P(-1)=t_0$ at every entry level and $w_L=0$.

**Comparison** (rule E, benchmark otherwise, $c_L=0$; `tp_extensions.out.txt`, Section C):

| | $r_0=1.2$, $p=0.5$ | $r_0=1.2$, $p=1.1$ | $r_1=3$, $p=0.5$ | $r_1=3$, $p=1.1$ |
|---|---|---|---|---|
| $\Delta_T$, value bands $\pm0.05$ | $0.017014$ | $1.0125$ | $0.666806$ | $1.005$ |
| orders | none | full buying | full buying | full buying |
| $\mathsf E$ | $0.25$ | $0.375$ | $0.375$ | $0.375$ |
| $\mathcal R_T$, value bands $\pm0.05$ | $0.392665$ | $0.344792$ | $0.755191$ | $0.947917$ |
| $\mathcal R_T$, paper (Laplace) | $0.392665$ | $0.432173$ | $0.872367$ | $1.014500$ |

**Reading the comparison.**

- The first column is a like-for-like row. Both models have no trade there, and the value matches the paper exactly.
- At $p=1.1$, point masses and the paper's value bands give identical objects. The low band lies below $p$, and the high band lies above $r$.
- The higher reserve still makes trading informative in the weak economy. But it **lowers** weak-economy proceeds in the discrete model.
- The reason: $t_0$ falls from $0.2917$ to $0.0917$, and the discrete experiment recruits only at the top flow, so $e_H=1/2$. The paper's claim "it raises expected proceeds in both economies" fails at $r_0$.

### Result 14 (analytical). Atomless preparation costs (Proposition A.6 analog)

**Setting.** Let costs come from atomless components:

- a low component on $[0,\varepsilon_L]$, with probability $\rho$;
- a high component on $[c_H-\varepsilon_C,c_H+\varepsilon_C]$, with probability $1-\rho$.

Then $e(\mu)=H_C(B_r(\mu))$.

**Claim.**

- (a) If $\varepsilon_L\le g_L(r)$ at every strength used, then $e\ge\rho$ at every price. Price sufficiency holds, and $U_H(\text{buy})=\tfrac23e(\pi)(1-\pi)\Delta_T-k$ for every $s>0$. The single cutoff survives.
  - The bound $g_L$ matters because full buying with $\lambda=1$ reaches posterior $0$.
  - With $\lambda<1$, $\varepsilon_L\le B_r(m_\lambda)$ suffices.
- (b) If $\varepsilon_L>g_L(r)$, entry at flow $-1$ falls below $\rho$, and part (iii) returns below $\rho$.
- (c) The return in part (iii) becomes gradual. Entry falls continuously from $\rho+(1-\rho)\pi\lambda/3$ to $\rho$ as $g_H(r)$ crosses the high-cost support. Example with $\varepsilon_L=1/50$, $\varepsilon_C=1/10$: entry is $0.3307$, $0.3121$, $0.3027$, $0.25$ at $r=7.91,\ 7.97,\ 8,\ 9$.
- (d) Challenger ties have probability zero, so rule X is irrelevant.

### Result 15 (analytical). What $c_L=0$ changes relative to the prior work ($c_L=1$)

| Item | Prior work, $c_L=1$ | This memo, $c_L=0$ | Source of the change |
|---|---|---|---|
| Entry at the bad-news flow $-1$, $\lambda=1$ | $0$, since $c_L>g_L(r)$ for $r>0.375$ | $\rho$ | $c_L$ |
| Entry at $r_1=3$ | $1/3$ | $3/8$ | $c_L$ |
| Entry after the return, $r>r_C(1)$ | $5/24<\rho$ | $\rho$ | $c_L$ |
| Price sufficiency | needs $c_L\le B_r(1/3)$; zero-entry pools otherwise | unconditional; no pools | $c_L$ |
| Presence | floor needs $\lambda\le158/179$ at $r=3$ | no restriction | $c_L$ |
| Adverse off-path belief $v=0$ | $e(0)=0$; supports no trade like $v=1$ | $e(0)=\rho$; supports no trade only above $\tfrac13[2\bar e(1-\pi)+\rho]\Delta_T$ | $c_L$ |
| Strict fixed-experiment deterrence between $r_0$ and $r_1$ | iff $c_L\in(g_L(r_1),g_L(r_0)]$ | never at the benchmark | $c_L$ |
| Proposition A.10 price-pool family | exists ($c_L=1$) | impossible | $c_L$ (also under Laplace) |
| Welfare level at $r=3$ | $191/72=2.6528$ (cost $c_L$ paid; no low-cost entry at flow $-1$) | $551/192=2.8698$ | $c_L$ |
| Trading cutoff, ownership $\mathsf O_H$ at $\lambda=1$ | $\rho\Delta_T/3$; $1/4$ at $r_1$ | same | none |

The prior-work values at $c_L=1$ reproduce exactly with the first-principles solver:

- $\mathsf E=1/3$ and $\mathsf O_H=1/4$ at $r=3$;
- $(11/32,7/32)$ at $\lambda=3/4$;
- $(19/60,7/30)$ at $\lambda=0.9$;
- $5/24$ at $r=8.5$.

## 4. What it recovers or loses relative to the Laplace paper

### 4.1 Verdict on every paper result

The last column names the source of each change:

- D: discreteness of the noise;
- C: $c_L=0$;
- M: the imposed buy-only menu;
- none: the result is unchanged.

| Paper result | Verdict | Derivation or reason | Source |
|---|---|---|---|
| Prop. 1 (spread rises, profit falls) | survives | auction stage; unchanged | none |
| Eqs. (7)–(8), Prop. A.1 (posterior bounds $m\le\mu\le M$) | dies | posteriors $\{\mu_{-1}(s),\pi,1\}$; top flow reveals $H$ whenever $s>0$; bottom flow reveals $L$ at $s=1$; $\lambda<1$ restores only the lower bound $m_\lambda$ (Result 1) | D |
| Eqs. (9)–(10), Prop. A.2 (price sufficiency) | survives, strengthened | unconditional at $c_L=0$ (Result 3) | C |
| Eq. (11) residual identities | survive | Result 2 | none |
| Eq. (11) floor $\rho m\Delta_T$ | dies | residual is $0$ at the revealing flow | D |
| (A.4)–(A.6) global order bound | not applicable | binary menu; the payoff is exact (Result 4) | M, D |
| (A.7) identity $F_H(1)=F_L(1)$ | not applicable | the low class does not trade; the sell-only mirror keeps it (prior work, Claim 13) | M |
| Prop. 2(i) | survives | iff $B_{r_0}(\pi)<c_H$ and $k\ge K_\rho(r_0)$ (Result 8); near the cutoff it needs a supporting off-path belief (Result 5); belief-free at the benchmark | D (belief rule) |
| Prop. 2(ii) | survives, weaker | orders $(1,0)$; iff $k<K_\rho(r_1)$ and $c_H\le g_H(r_1)$; $\mathsf E=0.375$ (paper $0.523$) | D, M |
| Prop. 2(iii) | changes | return iff $r_2>r_C(1)=7.97$ (paper $r_2=3.6$ fails); possible before $h$ iff $c_H>h/2-p^2/(2h)$; returns exactly to $\rho$ | D (ceiling), C (level) |
| (A1)–(A3) | change | (A1) void; (A2) becomes $B_{r_0}(\pi)<c_H\le g_H(r_1)$; (A3) becomes $K_\rho(r_0)\le k<K_\rho(r_1)$, which is necessary and sufficient | C, D |
| Blackwell sentence after Prop. 2 | survives | Result 8(ii); experiments Blackwell-increasing in $s$ | none |
| Eq. (12): $\tau$, $x^*$, $\alpha_H$, $\alpha_L$ | changes | $x^*$ disappears; $\alpha_H=\lambda/3$, $\alpha_L=0$ (pure tilt); entry flat in $c_H$ on $(B_r(\pi),g_H]$ | D |
| Section 4.2 numbers | change | $\mathsf E$: $0.25\to0.375$ (paper $0.5228$); $\mathsf O_H$: $0.125\to0.25$ (paper $0.3242$) | D |
| Section 4.2 frozen-orders control | changes | flat, $0.375\to0.375$ (paper $0.5622\to0.5228$) | D, C |
| Section 4.2 hidden-price control | survives | entry $\rho$ at both strengths | none |
| Prop. A.3 | survives (weak form) | strict only at crossings $r_C(\mu)$ for attained $\mu$ (Result 9a) | D |
| Prop. A.4 ($r_N$, $\mathfrak r(k)$, $r_U$, $r_C$) | changes | three bounds collapse into one exact cutoff $\mathfrak r(3k/(2\rho(1-\pi)))=1.9732$; passive beliefs give $r_N=1.7479$ exactly; $r_C\to r_C(1)=7.9686$; at $r_C(1)$ entry jumps from $\rho+(1-\rho)\pi\lambda/3$ to $\rho$ | D |
| Prop. 3 (coexistence) | dies | generic uniqueness (Result 6); coexistence only at $r=r_C(\pi)$ under rule X | D |
| Section 4.3 asymmetric $(1,-v)$ family, trading asymmetry | not applicable | menu has no sales; at equal noise even a two-sided menu has no feedback | M, D |
| Section 4.3 "no trade survives because $\rho\Delta_T/2\le k$" | changes | discrete condition $\tfrac23\rho(1-\pi)\Delta_T\le k$ (IC); $\rho(1-\pi)\Delta_T\le k$ (passive) | D |
| Prop. A.5 (logistic noise) | not applicable | the noise law is fixed; across three-point laws the clean result fails (Result 10) | D |
| Section 5.1 tail comparison (Laplace $0.523$ vs logistic $0.302$) | not applicable | no continuum of posteriors | D |
| Prop. A.6 (atomless costs) | survives | single cutoff; low support must lie below $g_L(r)$, because posterior $0$ is attained; gradual return (Result 14) | D (condition) |
| Section 5.2, A.4 nonemptiness for every value gap | survives | easier: any $r_0<r_1$ near $\ell$ (Result 8iv) | none |
| Section 5.2 moderate example ($h=2$) | survives in part | (i)–(ii): $0.25\to0.375$; (iii) fails before $h$, since $c_H=0.89<15/16$ | D |
| Section 5.3, Prop. A.7 | survives | cutoff $(2a-1)\rho\Delta_T/3$; example $0.85\to0.865$ (paper $0.8794$) (Result 11) | none |
| Section 6.2, Prop. A.8 | survives | payment stage; plus a solvable trading game (Result 12) | none |
| Section 6.1, Prop. A.9 | survives | $\Delta\mathcal R_T=9/64$, $\Delta\mathcal W=61/192$ at $r_1$; same order-flow experiment (Result 9) | none |
| Section 6.1 dividend diagnostic | survives | dividend $0.140625$ (paper $0.257809$) | none |
| Section 6.1 outside the conditions of Prop. 2 (prior already recruits) | not a paper claim | Region II: access lowers proceeds and can raise welfare (Result 9c); this agrees with the prior work's caveat | none |
| Section 6.3 reserve comparison | changes | proceeds fall at $r_0$ ($0.3927\to0.3448$) and rise at $r_1$; trading informative in both (Result 13) | D |
| Prop. A.10, Section 6.3 "pooling when preparation can vanish" | dies | zero entry needs $B<c_L=0$; also dies under Laplace with $c_L=0$ | C |
| (A.50)–(A.51) exact reserve events | change | the floor event needs $c_L>0$; the ceiling event uses posterior $1$ ($g_H=c_H$) | C, D |
| Section 7, predictions 1–2 | survive | entry rises with strength when prices reach the buyer; prepared buyers after the top flow all have high class | none |
| Section 7, prediction 3 | survives, later | requires $r>r_C(1)$ | D |

### 4.2 Mechanisms of each loss, and what a modification must supply

**M1. All-or-nothing information (bounded noise support).**

- *Losses:* the posterior bounds (A.1), the residual floor in (11), the early ceiling in 2(iii), and most of the entry gain.
- *Mechanism:*
  - Flow $2$ needs a purchase, so it reveals the high class whenever $s>0$.
  - Flow $-1$ needs no purchase, so it reveals the low class at $s=1$.
  - The interior flows are reached with equal probability by both classes.
  - Only flow $2$, with mass $\pi\lambda/3$, can push a belief above $\tau>\pi$.
- *Qualification of the brief's phrase "information is all-or-nothing".* The top flow is all-or-nothing whenever $s>0$. The bottom flow is partially informative, with posterior $\mu_{-1}(s)\in(0,\pi)$, unless $s=1$; that is, unless $\lambda=1$ and full buying.
- *A modification must supply* a top flow that noise alone can reach: $\Pr(Z\ge2)>0$ for unit buy orders. More generally, the noise support must be unbounded above. The largest attainable posterior is then below one. The ceiling becomes $B_r(\max\mu)$, and the residual floor is positive.
- An imperfect investor signal also bounds the top posterior, at $a$ (Result 11). It does not restore a positive residual at the top flow.

**M2. No feedback (equal noise).**

- *Losses:* Proposition 3, the feedback from entry to trading, and the endogenous trading asymmetry.
- *Mechanism:* $U_H(\text{buy})=\tfrac13(e_0+e_1)(1-\pi)\Delta_T-k$ for all $s>0$ (Result 4). Two facts produce this:
  - the camouflage flows $0$ and $1$ keep posterior $\pi$ for every $s$;
  - the recruiting flow $2$ is revealing, so it pays zero.

  The payoff is the same with and without price access.
- *A modification must supply* two things:
  - (a) a camouflage flow, one that the buyer reaches and that does not reveal, whose posterior moves with $s$. For three points this holds if and only if the noise is not uniform (Result 10).
  - (b) for coexistence, $K_{\rm dev}(0)<K(\lambda)$. This holds when the camouflage posterior falls with $s$ (increasing noise), or when it crosses $\tau$ and recruits.
- Consider a robust analog of Proposition 3 with challenger mixing. There the investor's strategy must hold a camouflage posterior at $\tau$ over an open set of strengths. At equal noise, only flow $-1$ moves with $s$, and the buyer never visits it.

**M3. An off-path flow under no trade (bounded noise support).**

- *Losses:* belief-free uniqueness, and existence under passive beliefs on $k\in(K,\tfrac32K)$, and at $k=K$ under rule Z (Result 5).
- *Mechanism:* noise alone cannot produce flow $2$, so Bayes' rule is silent there.
- *A modification must supply* full support of the flow under no trade: every flow that a deviation reaches must also be reachable by noise. Bayes' rule then fixes the deviation belief at the prior. The no-trade condition becomes the Laplace-type $\bar e(1-\pi)\Delta_T\le k$, which is the discrete passive condition.

**M4. Knife-edge equal noise.**

- *Loss:* the robustness of the single cutoff.
- *Mechanism:* Result 10. Any non-uniform three-point law gives either a coexistence interval or a nonexistence interval under rule Z. Its width is $|K(\lambda)-K_{\rm dev}(0)|$, which is of the order of the perturbation.
- *A modification must supply* a noise family in which the cutoff structure is stable under perturbation, or a reason to fix the law.

**M5. Finitely many posteriors and cost atoms.**

- *Losses:* strict fixed-experiment deterrence between nearby strengths, the threshold flow $x^*$, and continuous comparative statics in $c_H$ and $r$.
- *Mechanism:* three attained posteriors. Entry is a step function of $(r,c_H)$.
- *A modification must supply* many attained posteriors, or atomless costs. Result 14 restores continuity in $r$ at the top flow only.

**M6. The imposed buy-only menu.**

- *Losses:* the low class's sale, the asymmetric $(1,-v)$ equilibria, and identity (A.7).
- *A modification must supply* two-sided orders (workstream C1).
- The price-pool multiplicity found at intermediate presence (`V_discrete_check.md`, §3.5) needs a zero-entry price. That cannot exist at $c_L=0$, because the argument of Result 3 does not use the menu.

**M7. $c_L=0$ (a modelling decision, not a loss of mechanism).**

- *Losses:* Proposition A.10 and every zero-entry pool.
- *A modification must supply* $c_L>B_r(\mu)$ at some attained posterior if it wants pooling continuations.

## 5. Numerical example

All numbers in this section are computer-assisted, with exact rational arithmetic. The first-principles solver and the closed forms agree exactly at every point (`tp_compare.out.txt`).

**Scripts and commands.** All scripts are under `scripts/A_three_point/`. They are print-only, and each runs in under 10 seconds, so none needed the slot wrapper. Run them from the repository root:

```bash
.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_compare.py
.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_cutoffs.py
.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_extensions.py
.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_check_pair.py
```

| File | Content |
|---|---|
| `tp_first_principles.py` | auction objects by piecewise integration; flow laws; every price partition; both tie rules; off-path rules; outcomes |
| `tp_closed_form.py` | the memo's closed forms (Results 4–7) |
| `tp_compare.py` | 33 parameter points; first-principles equilibria next to closed forms |
| `tp_cutoffs.py` | irrational cutoffs at 40 digits, each bracketed by exact rational evaluations |
| `tp_extensions.py` | presence table, controls, reserve, moderate values, bargaining, signals, atomless costs, unequal noise |
| `tp_check_pair.py` | the paired memo's targets and a recount of its grid |
| `*.out.txt` | the printed output of each script |

**Benchmark** ($h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_L=0$, $c_H=6$, $k=1/50$, $\pi=1/2$, $\lambda=1$; rules Z, E; Intuitive-Criterion completion):

| $r$ | Region | $K$ | $\beta_H$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | $\mathcal W$ | $\mathrm{Var}(\mu_P)$ | Investor profit |
|---|---|---|---|---|---|---|---|---|---|
| $6/5$ | IV | $1/720$ | $0$ | $1/4$ | $1/8$ | $377/960=0.392708$ | $1679/960=1.748958$ | $0$ | $0$ |
| $3$ | IV | $1/18$ | $1$ | $3/8$ | $1/4$ | $145/192=0.755208$ | $551/192=2.869792$ | $1/12$ | $4/225=0.017778$ |
| $18/5$ | IV | $169/2160$ | $1$ | $3/8$ | $1/4$ | $4837/5760=0.839757$ | $17831/5760=3.095660$ | $1/12$ | $629/21600=0.029120$ |
| $17/2$ | V | $75/272$ | $1$ | $1/4$ | $1/8$ | $547/544=1.005515$ | $2701/544=4.965074$ | $1/12$ | $1739/13600=0.127868$ |

At $r=3$, the flows $(-1,0,1,2)$ have:

- posteriors $(0,1/2,1/2,1)$;
- entry $(1/4,1/4,1/4,1)$;
- prices $(17/32,\ 59/96,\ 59/96,\ 37/24)$;
- purchase payoffs $U_H=8/225$ and $U_L=-67/225$.

The strength path at $k=1/50$ is:

- no trade with entry $1/4$ for $r\le1.973212$;
- full buying with entry $3/8$ for $1.973212<r\le7.968627$;
- full buying with entry $1/4$ above.

**Presence** ($r=3$; $\mathsf E=\rho+(1-\rho)\lambda/6$):

| $\lambda$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | $\mathcal W$ | $\mathrm{Var}(\mu_P)$ | Profit |
|---|---|---|---|---|---|---|
| $1/10$ | $21/80$ | $11/80$ | $1207/1920$ | $4961/1920$ | $1/228$ | $2/1125$ |
| $1/2$ | $5/16$ | $3/16$ | $263/384$ | $347/128$ | $1/36$ | $2/225$ |
| $3/4$ | $11/32$ | $7/32$ | $553/768$ | $2143/768$ | $1/20$ | $1/75$ |
| $9/10$ | $29/80$ | $19/80$ | $1423/1920$ | $5449/1920$ | $3/44$ | $2/125$ |

**Prior** ($r=3$, $\lambda=1$):

- At $\pi=1/3$: $K=2/27$, $\mathsf E=1/3$, $\mathsf O_H=1/6$, $\mathcal R_T=49/72$, $\mathcal W=29/12$, $\mathrm{Var}=2/27$, $r_T=1.806418$.
- At $\pi=2/3$: $K=1/27$, $\mathsf E=5/12$, $\mathsf O_H=1/3$, $\mathcal R_T=239/288$, $\mathcal W=319/96$, $\mathrm{Var}=2/27$, $r_T=2.281737$.

### 5.1 Comparison numbers for A2

Exact values. The benchmark applies except for the changes listed. Unless stated, the rules are Z and E with the Intuitive-Criterion completion.

1. **Benchmark rows above.** These cover $r=6/5,3,18/5,17/2$, the presence table and the two priors.
2. **Investor knife-edge, $r=3$, $k=1/18$.**
   - Rule Z: no trade only.
   - Rule M: every $\beta_H\in[0,1]$, with $\mathsf E=1/4+\beta_H/8$, $\mathsf O_H=1/8+\beta_H/8$, $\mathcal R_T=59/96+9\beta_H/64$.
   - Grid values at $\beta_H=1/4$: $\mathsf E=9/32$, $\mathsf O_H=5/32$, $\mathrm{Var}=1/84$.
3. **Region II, $c_H=4$, $r=3$ ($\tau=93/200$, $K=K_1=2/9$).**
   - $k=1/50$, $\lambda=1$: full buying; entry by flow $(1/4,1,1,1)$; $\mathsf E=7/8$, $\mathsf O_H=1/2$, $\mathcal R_T=221/192$, $\mathcal W=635/192$.
   - $\lambda=1/2$: $\mathsf E=13/16$, $\mathsf O_H=7/16$, $\mathcal R_T=415/384$, $\mathcal W=387/128$.
   - $k=2/9$, rule M: every $\beta_H$. Entry is $1$ for $\beta_H\le s^*=14/107$ and $1-(1-\rho)(1-\beta_H/2)/3$ above. Under rule X at $\beta_H=14/107$, entry at flow $-1$ lies in $[1/4,1]$, and $\mathsf E$ lies in $[82/107,1]$.
4. **Region III knife-edge, $c_H=103/24=B_3(1/2)$, $r=3$.**
   - Rule E: $K=2/9$. At $k=1/10$: full buying, $\mathsf E=7/8$.
   - Rule X: no trade and full buying coexist for $k\in[1/18,2/9)$.
   - At $k=1/10$, no trade needs $e_0+e_1\le9/10$, with every rate in $[1/4,1]$. Its entry $(e_{-1}+e_0+e_1)/3$ ranges over $[1/4,19/30]$.
   - At $k=1/10$, full buying needs $e_0+e_1>9/10$. Its entry $\tfrac13[\tfrac18+e_0+e_1+\tfrac12]$ ranges over $(61/120,7/8]$.
5. **Top knife-edge, $c_H=203/24=g_H(3)$, $r=3$.**
   - Rule E: $\mathsf E=3/8$.
   - Rule X: $\mathsf E\in[1/4,3/8]$; the grid gives $1/4$, $5/16$ and $3/8$.
6. **Passive beliefs, $r=3$.**
   - $k=1/15$: no equilibrium; under the Intuitive-Criterion completion, no trade.
   - $k=1/12=\tfrac32K$: no trade under both rules.
7. **Region I, $\lambda=1/2$, $c_H=2$, $r=3$:** full buying, $\mathsf E=1$, $\mathsf O_H=1/2$, $\mathcal R_T=29/24$, $\mathcal W=13/3$.
8. **Cutoffs at the benchmark:** $1.973212111$ (Intuitive Criterion), $1.747877538$ (passive), $1.624380809$ (adverse), $1.556594423$ (every belief), $7.968626967$ ($r_C(1)$).
9. **Prior-work check at $c_L=1$:** the values listed in Result 15.

### 5.2 Comparison with A2

I read `memos/A_bruteforce.md` after my derivations and numbers were complete. The script `tp_check_pair.py` recomputes A2's comparison targets with this folder's first-principles solver (`tp_check_pair.out.txt`).

**Agreements** (exact values, computer-assisted):

1. $\beta_L=0$ in every equilibrium.
2. The cutoff $K=\tfrac23\bar e(1-\pi)\Delta_T$, which does not depend on $\lambda$.
3. The passive boundary $N=\tfrac32K$, and the passive investor table:
   - rule Z: empty on $[K,N)$;
   - rule M: $(0,1]$ at $k=K$ and empty on $(K,N)$.
4. The passive gap at $r=9/5$, $k=1/50$: $K=2/135$ and $N=1/45$; no equilibrium at $\lambda=1$ and $\lambda=1/5$.
5. The benchmark rows $(3/8,1/4,145/192)$ at $r=3$, $(1/4,1/8,377/960)$ at $r=6/5$, and $\mathcal R_T=4837/5760$ at $r=18/5$. The return at $4+\tfrac32\sqrt7$.
6. All seven presence rows of A2, for example $(7/20,9/40,349/480)$ at $\lambda=4/5$.
7. The lower-flow tie at $c_H=4$, $\pi=2/3$, $\lambda=3/5$, $k=4/27$:
   - $\tau=93/200$ and $\beta_*=605/642$;
   - with $\sigma_{-1}=1/2$, prices $(287/320,95/72,95/72,37/24)$ and outcomes $(296/321,1619/2568,1213/963)$.
8. The prior tie at $c_H=103/24$, $r=3$, $k=1/10$:
   - distinct middle prices $59/96\ne149/160$ at equal posteriors;
   - outcomes $(107/240,61/240,4553/5760)$;
   - coexistence of strict no trade and strict full buying, also under passive beliefs.
9. The top tie at $c_H=203/24$ with $\sigma_2=1/2$: $(5/16,3/16,263/384)$.
10. The non-interval trade set at $c_H=4$, $k=1/5$.
11. A2's base-grid counts, recomputed from my closed forms over the same 13,387,500-point grid:
    - $1{,}332{,}674$ passive failures under rule Z;
    - $1{,}332{,}478$ passive failures under rule M;
    - $196$ multiple-equilibrium points under the Intuitive Criterion and rule M.

    All three match exactly. The grid contains no prior tie.

**Differences in label or scope (no substantive disagreement):**

- A2 marks Prop. 2(i) and Prop. A.6 "changes". I mark them "survives", with the changed conditions stated. Both memos give the same conditions.
- A2 leaves Props. A.7 and A.8 and Sections 5.2, 5.3, 6.2 and 6.3 outside its exercise. This memo evaluates them (Results 11–14 and Section 4.1).
- A2 adds the qualification that the bottom flow is partially informative unless $s=1$. I agree, and I adopted it in M1.

**Disagreements:** none found.

## 6. Open issues

1. **Two-sided menu.** Buy-only orders are imposed. The full two-sided correspondence at $c_L=0$ is open here; it belongs to workstream C1. One part is settled. The prior price-pool example pools distinct posteriors at a zero-entry price, which Result 3 excludes for every menu at $c_L=0$.
2. **General three-point noise.** Result 10 proves the knife-edge lemma and gives exact examples. A full region-by-region correspondence for unequal noise with challenger mixing is open; it belongs to workstream C9.
3. **The shared off-path belief.** I assume that market makers and the challenger share one belief at the unused flow. A PBE with different off-path beliefs could add no-trade outcomes. It cannot remove the Intuitive-Criterion outcome.
4. **Reading N with general value laws.** The trading-stage results extend under $\Delta_T>0$, $g_H>g_L$ and $g_L>0$. Ownership and welfare formulas with value bands that straddle $p$ or $r$ are not derived here.
5. **Bargaining (Result 12).** The trading game is solved only with the uniform incumbent and point-mass values. Entry under bargaining needs its own region map, because $G_{H,\eta}$ falls with $\eta$.
6. **The size of the effect** ($0.375$ against $0.523$) is a fact of the specification. No result here says which noise law is empirically closer.

## 7. Plain summary

The three-point model can be solved completely. Noise orders take three values with equal chances. The informed investor can only buy, and it is sometimes absent. The low-cost challenger prepares for free.

Prices always reveal what the market maker believes, because the cheap challenger always prepares. The investor with bad news never buys. The investor with good news profits only on the two middle flows. Those flows keep the prior belief, whatever the investor does. So one cost cutoff decides everything. It equals two thirds of the cheap-entry rate, times the prior chance of a low-value challenger, times the spread. It does not depend on how often the investor is present.

Five regions describe entry. They depend on where the expensive challenger's belief threshold lies. In the main region, a stronger incumbent switches trading on, and the top flow then attracts the expensive challenger. Entry rises from 0.25 to 0.375 at the benchmark, against 0.523 under Laplace noise. Entry falls back only for a very strong incumbent (above 7.97, against 3.59). Where the prior already attracts the expensive challenger, information deters entry instead.

Most robustness results survive: atomless costs, investor and buyer signals, access to prices, and nonemptiness for every value gap. New: the trading game under bargaining becomes solvable. Three things are lost. Coexisting equilibria and feedback from entry to trading disappear, because the top flow reveals the class and pays nothing. A belief rule is needed at the unused top flow; with passive beliefs, some costs have no equilibrium. Equal noise is a knife-edge; any small change brings back coexistence or nonexistence.

Setting the cheap cost to zero removes the price-pooling result. It also makes entry return exactly to the floor.
