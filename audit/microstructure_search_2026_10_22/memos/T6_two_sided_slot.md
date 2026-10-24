# T6. Two-sided orders, a same-size liquidity slot, and symmetric noise

Workstream T6. Scripts: `scripts/T6_two_sided_slot/`. Status of this file: complete, 22 October 2026.

## 1. Question

T1's Part B candidate ($\theta=1/10$, $\lambda=7/10$, two-sided unit orders, presence $\lambda$) reproduces Prop. 2(i)–(ii), Prop. 3 with rising entry, and Prop. A.9. It fails Prop. 2(iii), because the flow $+2$ reveals class $H$. T2's liquidity slot makes every flow interior and restores Prop. 2(iii). This memo combines the two devices and asks:

1. What are the posteriors at each flow, and is every flow on path?
2. Is there a point $(\lambda,\beta,\theta)$, and an open region, where Prop. 2(i)–(iii), Prop. 3 at $31/20,8/5,33/20$ with rising entry, entry near $0.522757$ at $r=3$ (with the paper's $(1,-v)$ if possible), and Prop. A.9 all hold at the paper's benchmark?
3. If not, what is the precise trade-off, and what is the best compromise?

**Answer in brief.**

- No point achieves all items. Prop. 2(iii) caps the top posterior at $\tau(18/5)=0.7314$, so $\lambda\le0.463$ for every $\beta$; T1's $\lambda=7/10$ is excluded (analytical).
- On the cap, full two-sided trade is unique at $r_1$, so the paper's $(1,-v)$ is impossible (analytical).
- T1's rising branch needs the recruiting posterior above $0.755$. For $\theta\le1/3$ it cannot coexist with Prop. 2(iii) at the paper's strengths (analytical).
- Best compromise: $(\lambda,\beta,\theta)=(9/20,12/25,71/200)$. Prop. 2(i)–(iii), Prop. 3 with rising entry at $31/20,8/5,33/20$, and A.9 hold on an open box; entry at $r_1$ is $0.492$ (computer-assisted).

## 2. Setup

### 2.1 Model

- **Classes, values, costs, auction.** Reading N with point masses $h=10$, $\ell=1$, prior $\pi=1/2$; $c_L=0$, $c_H=6$ with probability $1-\rho$; the paper's cash second-price auction with reserve $p=1/2$; $R\sim U[0,r]$. The auction objects are those of TEAM_RULES §3. `t6_bounds.out.txt`, Section A, checks them against piecewise integration (difference exactly zero at six strengths).
- **Menu.** Two-sided unit orders $q\in\{-1,0,1\}$ with cost $k|q|$, $k=1/50$, as in EGJ and T1.
- **Order slot (T2's device).** One public order opportunity. With probability $\lambda$ the informed investor fills it and sees the class. With probability $1-\lambda$ a liquidity trader fills it; it sells, abstains, buys with probabilities $(\beta,1-2\beta,\beta)$, $0<\beta\le1/2$. The identity draw is independent of everything else and unobserved.
- **Separate noise (T1's second knob).** $Z\in\{-1,0,1\}$ with weights $(\theta,\phi,\theta)$, $\phi=1-2\theta$, $0<\theta<1/2$. Write $d=\phi-\theta=1-3\theta$.
- **Flow and price.** $X=Q+Z\in\{-2,\dots,2\}$, where $Q$ is the slot order. Competitive market makers set $P(X)=\mathbb E[V_T\mid X]$.
- **Challenger.** It sees the price and its cost, then prepares or stays out.

**Why this setup.** It is the smallest change to T1's block that removes revelation at $\pm2$. EGJ's presence draw (T1) leaves the slot empty with probability $1-\lambda$; here a same-size liquidity order can fill it instead. This is EGJ's second reading of $\lambda$ with a liquidity motive that trades, and Dow–Gorton's alternative arrivals (Result 9).

### 2.2 Strategies and notation

After Result 1(b), a profile is a pair of effective rates
$$A=\lambda\alpha,\qquad S=\lambda\sigma,\qquad (A,S)\in[0,\lambda]^2,$$
where $\alpha$ is class $H$'s purchase probability and $\sigma$ is class $L$'s sale probability, conditional on an informed slot. The liquidity rate on each side is $c=(1-\lambda)\beta$. Labels: NT $=(0,0)$; T $=(\lambda,\lambda)$; BNS $=(\lambda,0)$; "partial buy" means $0<A<\lambda$.

Other notation: $\Delta=\Delta_T$, $B(\mu)=g_L+\mu(g_H-g_L)$, $\tau(r)=(c_H-g_L)/(g_H-g_L)$, $\kappa(r)=k/\Delta(r)$. Entry at flow $x$ is $e_x=\rho+(1-\rho)\varsigma_x$, where $\varsigma_x$ is the high-cost type's preparation probability. The top full-purchase posterior is
$$M=\frac{c+\lambda}{2c+\lambda}=\frac{1+u}{2+u},\qquad u=\frac{\lambda}{c}=\frac{\lambda}{(1-\lambda)\beta}.$$

### 2.3 Equilibrium concept, beliefs and tie rules

- **Concept.** Perfect Bayesian equilibrium of the finite order game. A deviation faces the fixed price and entry schedule. Preparation is optimal given the posterior read from the price.
- **Beliefs.** For $\lambda<1$ and $\beta>0$ every flow is on path under every strategy (Result 1). No claim uses an off-path belief.
- **Investor tie rules.** Rule M: a tied class may mix. Rule Z (EGJ's rule): a tied class does not trade.
- **Challenger tie rules.** Rule E: a tied high-cost type prepares (the paper's rule). Rule X: it may mix.
- The scan (Result 6) uses rules M and X. The certificate (Result 7) reports all four rule pairs.

### 2.4 Benchmark values (exact, `t6_bounds.out.txt`, Section A)

| $r$ | $\Delta$ | $\kappa=k/\Delta$ | $\tau$ |
|---|---|---|---|
| $6/5$ | $1/60$ | $6/5$ | $195/308=0.633117$ |
| $31/20$ | $121/1240$ | $124/605=0.204959$ | $1020/1577=0.646798$ |
| $8/5$ | $9/80$ | $8/45=0.177778$ | $205/316=0.648734$ |
| $33/20$ | $169/1320$ | $132/845=0.156213$ | $7620/11711=0.650670$ |
| $3$ | $2/3$ | $3/100$ | $141/200=0.705$ |
| $18/5$ | $169/180$ | $18/845=0.021302$ | $4245/5804=0.731392$ |

No trade is an equilibrium exactly when $\rho\Delta/2\le k$, that is $r\le r_N=1.747878$ (Result 5).

## 3. Results

### Result 1 (analytical). Flow laws, posteriors, and full support

**(a) Flow laws.** With $L_1:=c\phi+(1-2c)\theta$ and $L_0:=2c\theta+(1-2c)\phi$:

| $x$ | $f_H(x)$ | $f_L(x)$ | $\mu_x$ at $\pi=1/2$ |
|---|---|---|---|
| $2$ | $(c+A)\theta$ | $c\theta$ | $\dfrac{c+A}{2c+A}$ |
| $1$ | $L_1+Ad$ | $L_1-S\theta$ | $\dfrac{L_1+Ad}{2L_1+Ad-S\theta}$ |
| $0$ | $L_0-Ad$ | $L_0-Sd$ | $\dfrac{L_0-Ad}{2L_0-(A+S)d}$ |
| $-1$ | $L_1-A\theta$ | $L_1+Sd$ | $\dfrac{L_1-A\theta}{2L_1-A\theta+Sd}$ |
| $-2$ | $c\theta$ | $(c+S)\theta$ | $\dfrac{c}{2c+S}$ |

*Derivation.* Class $H$'s slot order is $+1$ with probability $c+A$ (liquidity buy or informed buy), $0$ with probability $1-2c-A$, and $-1$ with probability $c$. Class $L$'s is $+1$ with probability $c$, $0$ with $1-2c-S$, $-1$ with $c+S$. Convolution with $(\theta,\phi,\theta)$ gives the table; for example $f_H(1)=(c+A)\phi+(1-2c-A)\theta=L_1+A(\phi-\theta)$. Each column sums to $2\theta+\phi=1$. Bayes' rule at $\pi=1/2$ gives the last column. $\square$

**(b) Every flow is on path and every posterior is interior when $0<\beta\le1/2$ and $\lambda<1$.** The liquidity component of each class's flow mass is $(1-\lambda)\sum_q\eta(q)n(x-q)$ with $\eta=(\beta,1-2\beta,\beta)$. It is positive at every $x\in\{-2,\dots,2\}$: $x=\pm2$ need $q=\pm1$ and $z=\pm1$; $x=\pm1$ need $q=\pm1$ and $z=0$; $x=0$ needs $q=\pm1$ and $z=\mp1$. These use only $\eta(\pm1)=\beta>0$ and $\theta,\phi>0$. Informed orders add nonnegative mass. So $f_H(x),f_L(x)>0$ for every strategy, and $0<\mu_x<1$. At $\beta=1/2$ the slot never abstains under T, but every flow stays on path. $\square$

Consequences:

- Residuals $\mathbb E[V_T\mid H,x]-P(x)=e_x\Delta(1-\mu_x)>0$ and $P(x)-\mathbb E[V_T\mid L,x]=e_x\Delta\mu_x>0$ at every flow. A sale by $H$ or a purchase by $L$ loses at least $k$. So only $(A,S)$ matters.
- The price reveals the posterior (T1 Result 1(b); T2 eq. (7)): $c_L=0<g_L$ gives $e\ge\rho>0$.
- Payoffs, per unit $\Delta$ and before the cost:
$$\frac{G_H}{\Delta}=\theta e_0(1-\mu_0)+\phi e_1(1-\mu_1)+\theta e_2(1-\mu_2),\qquad \frac{G_L}{\Delta}=\theta e_0\mu_0+\phi e_{-1}\mu_{-1}+\theta e_{-2}\mu_{-2}.$$
A purchase reaches $x=0,1,2$ with weights $\theta,\phi,\theta$; a sale reaches $x=0,-1,-2$.

**(c) Two orderings used below (for $\theta\le1/3$, so $d\ge0$).**

1. Every posterior at $x=1,2$ is at most $M$, for every $(A,S)$. Indeed $\mu_2=(c+A)/(2c+A)\le M$. For $x=1$ the likelihood ratio is $[(c+A)\phi+(1-2c-A)\theta]/[c\phi+(1-2c-S)\theta]$. Its numerator rises in $A$ and its denominator falls in $S$, so it is at most $[(c+\lambda)\phi+\chi\theta]/[c\phi+\chi\theta]$ with $\chi=1-2c-\lambda=(1-\lambda)(1-2\beta)\ge0$. Adding $\chi\theta$ to both terms of a ratio above one moves it toward one, so the bound is at most $(c+\lambda)/c$. The inequality is strict when $A<\lambda$.
2. By the mirror argument, every posterior at $x=-1,-2$ is at least $1-M$, for every $(A,S)$.

### Result 2 (analytical). Prop. 2(iii) caps the presence probability for every $\beta$ and $\theta$

**Claim.** Suppose an equilibrium at $r_2=18/5$ has entry $\rho$. Then class $H$ buys fully and $M\le\tau(18/5)$ (strictly under rule E). Hence
$$u=\frac{\lambda}{(1-\lambda)\beta}\le\frac{2686}{1559},\qquad \lambda\le\frac{2686\beta}{1559+2686\beta}\le\frac{1343}{2902}=0.462784 .$$
In particular **$\lambda=7/10$ fails Prop. 2(iii) for every $\beta\in(0,1/2]$ and every $\theta$**: it would need $\beta>10913/8058=1.354$.

*Proof.* Entry $\rho$ at every flow requires $\mu_x\le\tau(18/5)$ at every flow (any strict excess forces $e_x=1$). Then a purchase earns at least $\rho\Delta(18/5)[1-\tau(18/5)]-k=899467/20894400>0$, so $A=\lambda$. Under $A=\lambda$, $\mu_2=M$, so $M\le\tau(18/5)$. The cap on $\lambda$ follows from $c=(1-\lambda)\beta$ and $\beta\le1/2$. $\square$

The cap does not involve $\theta$: the flow $+2$ arises only from a slot purchase plus a noise purchase. So the brief's start point ($\lambda$ near $7/10$, small $\beta$) is infeasible. The slot must be filled by liquidity trade often: at $\lambda=1/2$ Prop. 2(iii) needs $\beta>0.580$, outside the domain; at $\lambda=0.46$ it needs $\beta>0.4944$. Prop. 2(ii) with recruitment at $x=2$ needs $u\ge82/59$ (T2 eq. (18)).

### Result 3 (analytical). On the strip: full two-sided trade is unique at $r=3$ and $r=18/5$; the $(1,-v)$ pattern is impossible

**Claim.** Let $M\le\tau(18/5)$ and $0<\theta<1/2$. At $r\in\{3,18/5\}$, T is the unique equilibrium under every tie rule, with prices seen or hidden. Entry at $r=3$ is
$$\mathsf E(3)=\rho+(1-\rho)\Big[\mathbf 1\{M\ge\tau(3)\}\frac{\theta w}{2}+\mathbf 1\{\mu_1^{\mathrm T}\ge\tau(3)\}\Big(\frac{\phi w}{2}+\theta\chi\Big)\Big],\qquad w=2c+\lambda,$$
with $\mu_1^{\mathrm T}=[(c+\lambda)\phi+\chi\theta]/[w\phi+2\chi\theta]$, and entry at $18/5$ is $\rho$ when $M<\tau(18/5)$.

*Proof.* Both bounds below use only $e\ge\rho$, so they hold for every candidate schedule, with or without price access.

- *Case $\theta\le1/3$.* By Result 1(c), every profile has $1-\mu_1,1-\mu_2\ge1-M$ and $\mu_{-1},\mu_{-2}\ge1-M$. With the flow-0 term dropped,
$$\frac{G_H}{\Delta},\ \frac{G_L}{\Delta}\ \ge\ \rho(\phi+\theta)(1-M)\ \ge\ \rho\cdot\tfrac23\cdot\tfrac{1559}{5804}=\frac{1559}{34824}=0.044768 .$$
- *Case $\theta>1/3$ ($d<0$).* Drop the flow-1 and flow-$(-1)$ terms. Always $\mu_2\le M$ and $\mu_{-2}\ge1-M$. At $x=0$ the likelihood ratio is $(L_0+A|d|)/(L_0+S|d|)$, which lies between $1/R_0$ and $R_0$ with $R_0=1+\lambda|d|/L_0$. Since $L_0>2c\theta$ and $|d|<\theta$, $\lambda|d|/L_0<u/2$. So $1-\mu_0,\mu_0\ge1/(2+u/2)$, and
$$\frac{G_H}{\Delta},\ \frac{G_L}{\Delta}\ \ge\ \rho\theta\Big[\frac{1}{2+u/2}+1-M\Big]\ >\ \frac14\cdot\frac13\Big[\frac{1}{2+1343/1559}+\frac{1559}{5804}\Big]=0.0515 .$$

Both bounds exceed $\kappa(3)=0.03$ and $\kappa(18/5)=0.0213$. So both classes strictly prefer to trade at every candidate: $A=S=\lambda$. Under T, $\mu_0=1/2$ and $\mu_{-x}=1-\mu_x$; only $x=1,2$ can recruit. The bound $\mu_1^{\mathrm T}\le M$ holds for every $\theta$ (add $\chi\theta$ to both terms of $(c+\lambda)\phi/(c\phi)$). The unconditional masses are $\Pr(X=2)=\theta w/2$ and $\Pr(X=1)=\phi w/2+\theta\chi$. $\square$

So **the paper's $(1,-v)$ at $r_1$ cannot coexist with Prop. 2(iii)** in this family, for any $\theta$. The seller earns at least $0.0448\Delta$ at every candidate, above $k=0.03\Delta$. In T1 the seller mixes at $r_1$ because $\mu_{-1}$ falls toward $0$; the slot keeps $\mu_{-2}\ge1-M$, and Prop. 2(iii) keeps $1-M\ge0.2686$.

At $\beta=1/2$ ($\chi=0$) the slot never abstains under T, so $\mu_1^{\mathrm T}=M$ and $\mathsf E(3)=\tfrac14+\tfrac38(1-\theta)$. This equals the paper's $0.522757$ at $\theta=0.272648$. Examples (`t6_bounds.out.txt`, Section D): $(\lambda,\beta,\theta)=(2/5,9/20,1/10)$ gives $2287/4000=0.571750$; $(1/3,3/10,1/10)$ gives $207/400=0.5175$; $(9/20,49/100,3/10)$ gives $40967/80000=0.512088$.

### Result 4 (analytical). The trade-off: T1's rising branch cannot survive Prop. 2(iii) when $\theta\le1/3$

T1's coexistence branch (its Result 13) is a buyer-mixing branch with no sale, $(A,0)$ with $0<A<\lambda$, on which the challenger prepares at $x=1$ and $x=2$. Entry rises because $A$ rises with $r$.

**Claim.** Let $\theta\le1/3$, $S=0$, $0<A<\lambda$, and pure entry (no challenger mixing). For $\theta\le1/3$, $\mu_0\le1/2<\tau$ and $\mu_{-1},\mu_{-2}\le1/2$ under $(A,0)$, so only $x\in\{1,2\}$ can recruit; and $\mu_1<\mu_2$, so the recruiting set is $\varnothing$, $\{2\}$ or $\{1,2\}$.

- **(a) Set $\{1,2\}$ (T1's branch).** Indifference $G_H=k$ needs
$$\kappa(r)=\theta\rho(1-\mu_0)+\phi(1-\mu_1)+\theta(1-\mu_2)\ >\ (1-\theta)(1-\bar\mu)+\frac{\rho\theta}2,$$
where $\bar\mu=\max(\mu_1,\mu_2)<M$. So the branch needs
$$M\ >\ 1-\frac{\kappa(r)-\rho\theta/2}{1-\theta}.$$
At $r=31/20$ the right side is $0.786$ at $\theta=1/10$ and $0.755$ at $\theta=1/3$; at $r=33/20$ it is $0.840$ at $\theta=1/10$. **Prop. 2(iii) needs $M\le0.7314$.** With $M\le\tau(18/5)$ the bound reads $\kappa(r)>(1-\theta)\tfrac{1559}{5804}+\tfrac\theta8\ge\tfrac{7687}{34824}=0.220739$, which holds only for $r<1.525828$.
- **(b) Set $\{2\}$.** For every $(\lambda,\beta)$, without using Prop. 2(iii),
$$\theta(1-\mu_0)+\phi(1-\mu_1)<\frac{1-\theta}{2}\qquad\text{under }(A,0),\ 0<A\le\lambda .$$
So the purchase earns $\Delta[\rho\frac{1-\theta}2+\theta(1-\mu_2)]<\Delta[\rho\frac{1-\theta}2+\theta(1-\tau)]\le\Delta\frac{\rho+1-\tau}{3}$. At $r=31/20$ this is $3805/18924\,\Delta=0.201067\,\Delta<k$. No purchase, partial or full, is optimal with this set at $31/20$.
- **(c) No recruitment.** The payoff is below $\rho\Delta/2<k$ for $r<r_N$.

*Proof of the inequality in (b).* Under $(A,0)$, $1-\mu_0=L_0/(2L_0-Ad)$ and $1-\mu_1=L_1/(2L_1+Ad)$. Then
$$\theta(1-\mu_0)+\phi(1-\mu_1)-\frac{1-\theta}2=\frac{Ad}{2}\cdot\frac{\theta(2L_1+Ad)-\phi(2L_0-Ad)}{(2L_0-Ad)(2L_1+Ad)} .$$
Expansion gives $\theta L_1-\phi L_0=-c\theta\phi-(1-2c)d(1-\theta)$, so the numerator is $-2c\theta\phi-d(1-\theta)[2(1-2c)-A]$. Since $A\le\lambda\le1-2c$, the bracket is at least $1-2c>0$. With $d\ge0$ and $c,\theta,\phi>0$ the numerator is negative. $\square$

*Proof of (a).* By Result 1(c), $1-\mu_1,1-\mu_2>1-M$ for $A<\lambda$; $1-\mu_0\ge1/2$ because $\mu_0\le1/2$. The weights are $\theta\rho$, $\phi$, $\theta$, and $\phi+\theta=1-\theta$. The right side decreases in $\theta$ (slope $-(1-\tau(18/5))+\rho/2<0$), so its minimum over $\theta\le1/3$ is at $\theta=1/3$. $\square$

**Corollary (analytical).** Let $\theta\le1/3$ and $M\le\tau(18/5)$. At $r=31/20$ the only informative equilibrium with no sale and pure entry is BNS with recruiting set $\{1,2\}$, when it exists. Entry under $(A,0)$ with recruiting set in $\{1,2\}$ is at most $\rho+(1-\rho)[\Pr(X=1)+\Pr(X=2)]$, and this mass, $(2L_1+Ad)/2+\theta(2c+A)/2$, rises in $A$. This maximum is attained by BNS with set $\{1,2\}$. So no selection of no-sale equilibria at $31/20,8/5,33/20$ that starts from a pure-entry equilibrium at $31/20$ has strictly rising entry, whatever happens at the later strengths. A rising selection would have to start from a challenger-mixing equilibrium at $31/20$; it would not be one branch (Result 6 reports these cases).

**The trade-off in one line.** T1's feedback needs the recruiting posterior to be high, so that the buyer's residual $1-\mu$ falls to about $\kappa/\phi$; Prop. 2(iii) needs every full-purchase posterior below $\tau(18/5)$. At the paper's strengths the first needs $M>0.755$, the second $M\le0.731$.

### Result 5 (analytical). No trade and the coexistence boundary

Under NT every posterior is $1/2<\tau$, so entry is $\rho$ at every flow. A deviation earns $\rho\Delta/2$ in either class, whatever $\theta$ and $\beta$, and no unused flow exists. So NT is an equilibrium exactly when $r\le r_N=\mathfrak r(2k/\rho)=1.747878$ (bracket in `t6_bounds.out.txt`), the paper's $r_N$, under every belief rule and every tie rule (at equality rule Z also keeps NT). At $r_0=6/5$, $\Delta=1/60<k$: every order loses under every schedule, so NT is the unique equilibrium (Prop. 2(i), analytical, every $(\lambda,\beta,\theta)$).

### Result 6 (computer-assisted at grid points; numerical diagnostic between points). The scan

**Method.** `t6_core.py` enumerates every equilibrium at a rational point, under rules M and X:

- corners, with free entry at tied flows (exact one-dimensional feasibility in $e_0$);
- edges (one class mixes), split at the five lines $\mu_x=\tau$, with exact univariate roots;
- open cells (both classes mix): elimination of one rate by a pseudo-remainder sequence, Sturm isolation of the eliminant's roots with rational endpoints, the other rate as a rational function on the bracket; where a leading coefficient may vanish, interval bisection excludes the strip;
- challenger mixing on each line, and crossings of two lines.

Rule-E and rule-Z results come from the same code with the stricter rules. Two checks support it:

- At $\beta=1/1000$, $\lambda=7/10$, $\theta=1/10$ it reproduces T1's candidate within the size of the slot: entry $0.527402$ at $r=3$ (T1: $0.527345$), branch entry $0.450787$ at $8/5$ (T1: $0.450297$), T at $18/5$ with entry $0.508907$ (T1: $0.50875$).
- `t6_crosscheck.py` is an independent floating-point search that shares no code with the enumerator. At the near-T1 point and at the final point (all six strengths) it finds the same equilibria, with entry equal to six decimals.

**Grids** (all inside the strip $82/59\le u<2686/1559$, which Results 2–3 require):

- main: $u\in\{1.40,1.42,\dots,1.72\}$, $\beta\in\{0.05,0.10,\dots,0.50\}$, $\theta\in\{0.02,0.04,\dots,0.48\}$; 4,080 points;
- pocket: $u\in\{1.60,1.61,\dots,1.72,1.7225\}$, $\beta\in\{0.44,0.46,0.48,0.49,0.495,0.50\}$, $\theta\in\{0.340,0.345,\dots,0.400\}$; 1,092 points.

Each point is solved at $r\in\{6/5,31/20,8/5,33/20,3,18/5\}$. There are **zero undecided cases**. Summaries: `t6_scan_main_summary.out.txt`, `t6_scan_pocket_summary.out.txt`.

**Findings.**

1. Prop. 2(i)–(iii) hold with a unique outcome at all 5,172 points. At $r=3$ the outcome is always T, never $(1,-v)$ (Result 3).
2. Entry at $r=3$ ranges over $[0.2512,0.6175]$. It is near the paper's $0.523$ for many points with small $\theta$ and $\beta$ near $1/2$.
3. No trade coexists with an informative equilibrium at all three middle strengths for $\theta\le0.18$ (through BNS with recruitment at $x=1,2$; entry flat) and for $\theta\ge0.35$ (through a partial purchase that recruits at $x=2$). At all 1,528 grid points with $\theta\in[0.20,0.345]$ there is no informative equilibrium at $31/20$.
4. **A pure-entry, no-sale branch with strictly rising entry exists only for $\theta\in[0.35,0.365]$**, with $u$ near the top of the strip ($u\ge1.64$ at $\theta=0.35$, $u\ge1.70$ at $\theta=0.36$, $u\ge1.72$ at $\theta=0.365$). It exists for every $\beta$ on the grid. It never exists for $\theta\le1/3$ (Result 4). Every such branch is mixed, mixed, full (BNS at $33/20$). The largest final gap is $0.0029$.
5. Entry at $r=3$ near $0.49$ on that branch region needs $\beta\ge0.46$, so that the flow $+1$ also recruits at $r=3$. Below, entry at $r=3$ drops to about $0.37$.
6. Weaker "rising" selections exist at 95 main points, but they combine different branches. For example, at $\theta=0.44$, $1.65$ adds SNB with recruitment at $x=\pm1$: with heavy-tailed noise a sale can be good news. These are not used. No full purchase with a partial sale appears at any middle strength.

### Result 7 (computer-assisted). The best compromise: $(\lambda,\beta,\theta)=(9/20,\,12/25,\,71/200)$

The point is the most balanced rational point of a small candidate set (margins of the branch at both ends near $0.0019$ in strength). Then $c=33/125$, $u=75/44$, $M=119/163=0.730061$, noise weights $(0.355,0.29,0.355)$, $d=-13/200$. All numbers below are exact or rational enclosures of width below $10^{-12}$ (`t6_certify_9-20_12-25_71-200.out.txt`).

**Prop. 2.** Result 3's bound is $\rho\theta[1/(2+\lambda|d|/L_0)+1-M]=0.066417$, against $\kappa(3)=0.03$ and $\kappa(18/5)=0.0213$. The enumerator agrees: one equilibrium at each of $6/5$, $3$, $18/5$ under all four rule sets.

| $r$ | Unique outcome | Entry by flow $x=-2,\dots,2$ | $\mathsf E$ |
|---|---|---|---|
| $6/5$ | NT | all $1/4$ | $1/4$ |
| $3$ | T | $(\tfrac14,\tfrac14,\tfrac14,1,1)$; posteriors $(0.2699,0.2819,0.5,0.7181,0.7301)$ | $393929/800000=0.492411$ |
| $18/5$ | T | all $1/4$; same posteriors | $1/4$ |

At $r=3$: $M-\tau(3)=817/32600$, $\mu_1^{\mathrm T}-\tau(3)=19529/1496200$; at $18/5$: $\tau(18/5)-M=1259/946052$. Entry falls in two steps: the flow $+1$ stops recruiting at $r_C(\mu_1^{\mathrm T})=3.301604$ (entry $0.380196$ above it), the flow $+2$ at $r_C(M)=3.570674$ (paper's ceiling $3.592659$).

**Prop. 3.** All equilibria at the middle strengths (rules M and X):

| $r$ | NT | Branch (pure entry, recruitment at $x=2$) | Challenger-mixing branch |
|---|---|---|---|
| $31/20$ | yes | partial buy, $\alpha\in[0.5036490912,\,0.5036490913]$, $\mathsf E\in[0.3504617283,\,0.3504617284]$ | $\mathsf E=0.348246$ |
| $8/5$ | yes | partial buy, $\alpha\in[0.9788371838,\,0.9788371839]$, $\mathsf E\in[0.3789284650,\,0.3789284651]$ | $\mathsf E=0.320434$ |
| $33/20$ | yes | BNS, $\mathsf E=304157/800000=0.380196$ | $\mathsf E=0.298072$ |

The certificate:

- *Branch payoff.* On $(A,0)$ with recruitment only at $x=2$, the purchase earns $\Delta K_2(A)$ with $K_2(A)=\rho[\theta L_0/(2L_0-Ad)+\phi L_1/(2L_1+Ad)]+\theta c/(2c+A)$. With $d<0$ each term is convex in $A$, and $K_2'(\lambda)=-0.096595<0$. So $K_2$ falls strictly on $[0,\lambda]$, the root on the recruiting segment $(A_2(r),\lambda)$ is unique, and $A(r)$ rises with $r$ (implicit differentiation, $\kappa'<0$).
- *Roots.* Exact payoff signs $(+,-)$ at the segment ends bracket the roots at $31/20$ and $8/5$. At $33/20$ the full purchase earns $0.020636\,\Delta$ net of $k$: BNS.
- *Pattern.* At $A=\lambda$, $\mu_0=35357/67789=0.5216<\tau$, $\mu_1<1/2$, $\mu_{-1}<1/2$, $\mu_{-2}=1/2$. So only $x=2$ recruits on the segment.
- *No sale.* Over $A\in[0,\lambda]$ the sale earns at most $0.125249\,\Delta$, below $\kappa$ at all three strengths (interval bound on 64 cells).
- *No trade.* $\rho\Delta/2-k=-387/49600,\,-19/3200,\,-211/52800$.
- *Order.* Entry on the branch is $\rho+(1-\rho)\theta(2c+A)/2$. The enclosures are disjoint: $0.350462<0.378928<0.380196$, gaps at least $0.0285$ and $0.0013$.

The branch lives on $[r_A,r_F]=[1.548026,\,1.601938]$: an adaptive rational-interval check shows $K_2(A_2(r))>\kappa(r)$ on the whole interval (39 cells). It continues as BNS (entry $0.380196$). BNS keeps the seller out up to $r_N$ (its sale earns $0.109286\,\Delta<\rho\Delta/2$). So no trade coexists with an informative equilibrium on $[1.548026,\,1.747878]$, which contains $1.55$–$1.65$. The challenger-mixing branch moves down, as in T1 and T5.

**Prop. A.9 at $r=3$.** With hidden prices, entry is $\rho$ at every flow, and Result 3's bound gives T uniquely again. The order flow and the trading cost ($9/1000$) are the same in both regimes. Price access raises proceeds by $1460417/6400000=0.228190$ (paper $0.257809$) and net surplus by $381423/6400000=0.059597$. Both gains are positive for the reason of T5 Result 6: extra preparation occurs only at recruiting flows, where $B(\mu)-c_H+p^2/r>0$.

**Open region.** On the closed box $|\lambda-9/20|,|\beta-12/25|,|\theta-71/200|\le1/2000$, all fourteen sign conditions behind Prop. 2, Prop. 3 and Prop. A.9 have positive rational lower bounds (64 cells; Section E of the output). The smallest margins are $\tau(18/5)-M\ge5.0\times10^{-4}$, $K_2(A_2(31/20))-\kappa(31/20)\ge7.1\times10^{-4}$ and $\kappa(8/5)-K_2(\lambda)\ge4.0\times10^{-4}$. The box of half-width $1/1000$ fails the first and the third. So the region is open but small.

**Dow–Gorton's liquidity law.** At $\beta=1/2$ the liquidity trader always trades. The point $(23/50,1/2,71/200)$ gives the same scorecard (`t6_certify_23-50_1-2_71-200.out.txt`, zero undecided): entry $787/1600=0.491875$ at $r=3$; branch entry $0.352761<0.381919<0.383125$ (mixed, mixed, full); $\Delta\mathcal R_T=73143/320000=0.228572$, $\Delta\mathcal W=903/12800=0.070547$. No box is claimed there, because $\beta=1/2$ is the edge of the domain.

### Result 8 (analytical branch; computer-assisted enumeration). Two variants that show the trade-off

**(a) EGJ's equal weights, $\theta=1/3$: the branch is closed-form but starts at $1.5566$.** With $d=0$, $\mu_0=\mu_1=1/2$ under $(A,0)$, so $K_2(A)=\rho/3+c/(3(2c+A))$. Indifference gives
$$A(r)=c\Big[\frac{4}{12\kappa(r)-1}-2\Big],\qquad \mathsf E(r)=\frac14+\frac{c}{2(12\kappa(r)-1)},$$
both strictly rising in $r$. At $(9/20,12/25,1/3)$ the branch lives on $[1.556594,\,1.609476]$, so it misses $31/20$ by $0.0066$. Result 4(b) proves that no branch with recruitment at $x=2$ exists at $31/20$ for $\theta\le1/3$; the exact enumeration finds no informative equilibrium of any kind there (`t6_path_9-20_12-25_1-3.out.txt`). At the shifted strengths $1.56,1.58,1.60$ all three purchase rates are interior ($\alpha=0.5176,0.6973,0.8973$) and entry rises $0.345118<0.355225<0.366471$ (rational values; `t6_certify_9-20_12-25_1-3_shifted.out.txt`). Entry at $r=3$ is exactly $1/2$ (Result 3: $\Pr(X\ge1)=1/3$). Prop. 2(i)–(iii) and A.9 hold as in Result 3.

**(b) Concentrated noise, $\theta=1/10$ (T1's knob): entry at $r_1$ near the paper, but no rising branch at the paper's strengths.** At $(1/3,3/10,1/10)$: entry at $r=3$ is $207/400=0.5175$; at $1.44$–$1.74$ no trade coexists with BNS (recruitment at $x=1,2$, entry $0.53$, flat). The rising branch lives on about $[1.40,1.44]$ (`t6_path_1-3_3-10_1-10.out.txt`, grid step $0.02$; numerical diagnostic between grid points). At $(9/20,49/100,1/10)$ it lives on about $[1.408,1.443]$ with entry $0.555\to0.601$ (`t6_path_9-20_49-100_1-10.out.txt`, step $0.005$). Result 4(a) explains why it cannot reach $1.55$: it needs $\kappa(r)>0.2207$, that is $r<1.5258$.

**The trade-off, summarised.** Along $\theta$, with $(\lambda,\beta)$ in the strip:

| $\theta$ | Entry at $r=3$ ($\beta$ near $1/2$) | Rising branch | Where |
|---|---|---|---|
| $0.10$ | $0.55$–$0.59$ | yes, recruits at $x=1,2$ | $r<1.526$ (about $1.41$–$1.44$) |
| $0.20$–$0.345$ | $0.498$–$0.55$ | none at $31/20$ | — |
| $1/3$ (EGJ) | $1/2$ | yes, closed form | $[1.5566,1.6095]$ |
| $0.35$–$0.365$ | $0.489$–$0.495$ | yes, recruits at $x=2$ | covers $1.55$–$1.60$, BNS at $1.65$ |
| $\ge0.37$ | $\le0.488$ | none on the grids | — |

Low $\theta$ gives the paper's entry level and T1's strong feedback, at strengths below $1.53$. High $\theta$ moves the branch to the paper's strengths, with weaker feedback (only $x=2$ recruits) and lower entry.

### Result 9 (interpretation). The knobs, and the distance to EGJ and Dow–Gorton

**The knobs at the final point.**

- $\lambda=9/20$: the chance that the order opportunity carries information. Prop. 2(iii) caps it at $0.463$ (Result 2).
- $\beta=12/25$: an arriving liquidity trader buys or sells with probability $0.48$ each and abstains with probability $0.04$. Under full trade, $88/163=54\%$ of slot purchases are uninformed ($c/(c+\lambda/2)$).
- $\theta=71/200$: noise trades with probability $0.71$ (EGJ: $2/3$). The weights $(0.355,0.29,0.355)$ have slightly heavier tails than EGJ's equal weights.
- The binding combination is $u=\lambda/c$: it sets the top posterior $M=(1+u)/(2+u)$, and the strip $1.39\le u<1.72$ is T2's.

**Distance to EGJ** (`L1_survey.md` C01; Q2 memo Tables 2.1–2.2):

- Same: two-sided unit orders, a linear cost per unit, additive three-point noise, competitive pricing, a probability $\lambda$ that the informed trader acts.
- Changed: when the informed trader does not act, a same-size liquidity order fills the slot, instead of a zero order. The noise weights move from $1/3$ each to $(0.355,0.29,0.355)$. The challenger sees the price (the paper's change).
- With EGJ's exact weights (Result 8(a)) every item that holds at the final point also holds, except that the branch starts at $1.5566$, not $1.55$.

**Distance to Dow–Gorton (1997)** (`L1_survey.md` C09 and §5.3, verified): informed and liquidity arrivals are mutually exclusive and of the same size; the liquidity trader buys or sells with equal probability. The slot here is that device. The differences:

- Dow–Gorton's liquidity trader always trades; here it abstains with probability $1-2\beta=0.04$ ($0$ at the variant $\beta=1/2$).
- Dow–Gorton's information arrives through costly research; here $\lambda$ is fixed.
- Dow–Gorton has no separate additive noise and a dynamic position reversal; here EGJ's noise is added and trade is one-shot.

The exact combination (Dow–Gorton's slot plus EGJ's additive noise with near-equal weights) has no verified precedent in the team's records (`L1_survey.md` §5.6). It is a combination of two verified devices.

**Price monotonicity.** With $\theta>1/3$ the zero flow is good news and the flow $+1$ is bad news on the branch. At $31/20$ the posteriors at $x=-2,\dots,2$ are $(0.5,0.401,0.511,0.484,0.650)$. The price is not monotone in the flow there. Under T at $r=3$ the posteriors are monotone ($0.270<0.282<0.5<0.718<0.730$). T5 reports the same feature.

## 4. Scorecard (BRIEF §2)

### 4.1 The brief's start point: $\lambda=7/10$, $\theta=1/10$, small $\beta$

| # | Item | Verdict | Status |
|---|---|---|---|
| 1 | Prop. 2(i) | Holds ($\Delta(r_0)<k$) | analytical |
| 2 | Prop. 2(ii) | Holds: unique full buy with partial sale, entry $0.5274$ at $\beta=1/1000$ | computer-assisted |
| 3 | Prop. 2(iii) | **Fails for every $\beta\le1/2$**: needs $\beta>1.354$ | analytical (Result 2) |
| 4–10 | | as T1 Part B | see T1 |

### 4.2 Final point $(\lambda,\beta,\theta)=(9/20,12/25,71/200)$; open box of half-width $1/2000$

| # | Item | Verdict | Status |
|---|---|---|---|
| 1 | Prop. 2(i) | Holds: NT unique, entry $\rho$; belief-free, tie-free | analytical |
| 2 | Prop. 2(ii) | Holds: T unique, entry $0.492411$ (paper $0.522757$), $\mathsf O_H=0.300627$ (paper $0.324192$), $\mathcal R_T=0.842773$ (paper $0.872392$). **The paper's $(1,-v)$ is impossible** on the strip | analytical (uniqueness, every $\theta$); exact values |
| 3 | Prop. 2(iii) | Holds: T unique, entry $\rho$, prices informative; ceiling $r_C(M)=3.570674$ | analytical |
| 4 | Prop. 3 | Holds at $31/20,8/5,33/20$: NT coexists with an informative equilibrium on $[1.548026,1.747878]$ (branch, then BNS); branch entry $0.350462<0.378928<0.380196$ (mixed, mixed, full; paper $0.545<0.549<0.551$). Recruitment only at $x=2$; small final gap $0.0013$. Challenger-mixing branch falls | computer-assisted |
| 5 | Prop. A.9 | Holds: $\Delta\mathcal R_T=0.228190$, $\Delta\mathcal W=0.059597$, same trading cost | analytical (sign); exact values |
| 6 | Off-path beliefs | None: every flow is on path under every strategy | analytical |
| 7 | Ties and mixing | Prop. 2 and A.9: no tie, every rule. Prop. 3: investor rule M needed at $31/20$ and $8/5$; either challenger rule. Under rule Z only NT remains at $31/20$ and $8/5$ | computer-assisted |
| 8 | Knobs | $\lambda$: informed share of the slot ($\le0.463$); $\beta$: liquidity activity ($\ge0.46$ for entry near $0.49$); $\theta$: noise activity ($0.35$–$0.365$). Box of half-width $1/2000$ certified; the grid region is $\theta\in[0.35,0.365]$, $u\in[1.64,1.7229)$ | computer-assisted (box); numerical diagnostic (grid region) |
| 9 | Precedent | Slot: Dow–Gorton (verified). Noise: EGJ's form, weights near equal (unequal weights unverified). Combination: unverified | literature fact / unverified |
| 10 | Labels | as listed | — |

### 4.3 Variant with EGJ's equal weights, $(9/20,12/25,1/3)$

| # | Item | Verdict | Status |
|---|---|---|---|
| 1–3 | Prop. 2 | Holds; entry $1/2$ at $r=3$; T unique | analytical |
| 4 | Prop. 3 | **Fails at $31/20$**: no informative equilibrium there. Holds at $1.56,1.58,1.60$ with three interior purchase rates and entry $0.3451<0.3552<0.3665$; branch on $[1.5566,1.6095]$ | analytical (branch formula; no pure-entry no-sale branch at $31/20$, Result 4); computer-assisted (no informative equilibrium of any kind at $31/20$, exact enumeration in `t6_path_9-20_12-25_1-3.out.txt`; the three shifted strengths) |
| 5 | Prop. A.9 | Holds | analytical |
| 6–7 | Beliefs, ties | As in 4.2 | — |
| 9 | Precedent | EGJ's noise exactly plus Dow–Gorton's slot | literature fact (parts) |

### 4.4 Variant with concentrated noise, $(1/3,3/10,1/10)$

| # | Item | Verdict | Status |
|---|---|---|---|
| 1–3 | Prop. 2 | Holds; entry $0.5175$ at $r=3$ | analytical |
| 4 | Prop. 3 | NT coexists with BNS at $1.55$–$1.65$, entry flat $0.53$. Rising branch only near $1.40$–$1.44$ | analytical (no rising branch at $\ge1.526$); numerical diagnostic (window) |
| 5 | Prop. A.9 | Holds | analytical |
| 8 | Knob | $\theta$ far from EGJ's; no verified precedent | — |

**Against the bar.** The two-sided discrete-Laplace companion reproduces Prop. 2 exactly with entry $0.569$ and a flat coexistence branch (T1 memo). The final point reproduces items 1–5 at the paper's strengths, with rising entry; no earlier two-sided EGJ-like candidate did (T1 loses Prop. 2(iii); T2's V3 has flat entry). T5 did it with a buy-only menu and entry $0.383$ at $r_1$. The final point's entry levels are below the paper's ($0.49$ at $r_1$; $0.35$–$0.38$ on the branch), and its rising branch is thin.

## 5. Numerical example

Final point $(9/20,12/25,71/200)$; benchmark primitives; rules M and E. Values are exact or certified enclosures shown to six decimals.

| $r$ | Equilibrium | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | $\mathcal W$ |
|---|---|---|---|---|---|
| $6/5$ | NT (unique) | $0.250000$ | $0.125000$ | $0.392708$ | $1.748958$ |
| $1.55$ | partial buy, $\alpha=0.503649$ (and NT) | $0.350462$ | $0.190317$ | $0.504249$ | $1.927179$ |
| $1.60$ | partial buy, $\alpha=0.978837$ (and NT) | $0.378928$ | $0.218783$ | $0.528224$ | $2.040761$ |
| $1.65$ | BNS (and NT) | $0.380196$ | $0.220051$ | $0.537953$ | $2.064367$ |
| $3$ | T (unique) | $0.492411$ | $0.300627$ | $0.842773$ | $2.611681$ |
| $18/5$ | T (unique) | $0.250000$ | $0.125000$ | $0.664236$ | $2.816319$ |

The strength path (`t6_path_9-20_12-25_71-200.out.txt`, grid step $0.02$ or $0.05$; numerical diagnostic between grid points):

- NT alone up to $r_A=1.548026$;
- NT with the rising branch up to $r_F=1.601938$, then NT with BNS up to $r_N=1.747878$;
- BNS, then a full purchase with a partial sale near $1.85$–$1.90$ (entry $0.380$);
- T with entry $0.492411$ from about $1.95$ to $3.301604$;
- T with entry $0.380196$ up to $3.570674$;
- T with entry $\rho$ above.

**Scripts** (folder `scripts/T6_two_sided_slot/`, print-only, no assertions; run from the repository root with `.venv/bin/python`):

| File | Content | Time |
|---|---|---|
| `t6_core.py` | exact primitives and the exhaustive enumerator | module |
| `t6_branch.py` | the branch payoff $K_2$, its derivative, endpoints, roots | module |
| `t6_bounds.py` → `t6_bounds.out.txt` | exact numbers of Results 2–5 | < 1 s |
| `t6_scan.py` → `scan_main_*.csv`, `scan_pocket_*.csv` | the grids (three slots each) | 13 min, 5 min |
| `t6_summarize.py` → `t6_scan_*_summary.out.txt` | scan summaries | < 1 s |
| `t6_certify.py` → `t6_certify_*.out.txt` | complete enumeration, branch certificate, A.9, open box | 3 s |
| `t6_crosscheck.py` → `t6_crosscheck_*.out.txt` | independent floating-point search | 2 s |
| `t6_windows.py` → `t6_path_*.out.txt` | equilibria along a strength grid (final point and the two variants) | seconds |
| `dev/probe.py` → `dev/probe_near_T1.out.txt` | development probe; the near-T1 check | seconds |
| `run_receipt.json` | benchmark, pinned source, software versions, file sizes and SHA-256 hashes | — |

## 6. Open issues

1. **Thin branch (computer-assisted at the point, small box).** The certified box has half-width $1/2000$. The branch starts $0.002$ below $1.55$ and reaches full purchase $0.002$ above $1.60$. The paper's ordering is also thin ($0.0037$ and $0.0026$), but at higher entry levels.
2. **Entry levels.** Entry at $r_1$ is $0.492$ (paper $0.523$); on the branch it is $0.35$–$0.38$ (paper $0.545$–$0.551$). Within the family, raising entry at $r_1$ needs lower $\theta$, which removes the branch at $1.55$ (Result 8).
3. **No $(1,-v)$.** The paper's partial sale cannot appear at $r_1$ while Prop. 2(iii) holds (Result 3). No full purchase with a partial sale appears at $1.55$–$1.65$ at any of the 5,172 grid points (Result 6). At the final point one appears only near $1.85$–$1.90$.
4. **$\theta\in(1/3,1/2)$: Result 4 is not proved analytically there.** The scan covers it at grid points only.
5. **Rule Z (EGJ's tie rule)** removes the branch at $31/20$ and $8/5$. Investor mixing is essential, as in T1 and T5.
6. **Continuous order sizes.** X_check notes that a $0.99$ purchase can reach an unused price in T2's V3. Here every flow of the unit menu is used, but a continuous menu creates new flows; this is not studied.
7. **Independent check.** The enumerator and the cross-check are by the same member. A check by another member would raise confidence.
8. Other priors, dispersed classes, atomless costs and private signals are not studied.

## 7. Plain summary

T6 joins T1's two-sided EGJ block to T2's liquidity slot: when the informed investor does not trade, a liquidity trader of the same size buys or sells instead. Then every price is used and no price reveals the class.

The brief's start point cannot work. To bring entry back to the floor at $r=3.6$, the top posterior must stay below $0.731$. That caps the informed share of the slot at $0.463$, for every liquidity rate. T1's $\lambda=0.7$ is excluded.

The same cap removes two of T1's features:

- At $r=3$ both classes always trade fully, so the paper's partial sale cannot appear.
- T1's rising branch needs a recruiting posterior above $0.755$. With noise weights at or below EGJ's $1/3$, it cannot reach the paper's strengths.

A small move toward heavier-tailed noise restores the coexistence result. At $\lambda=0.45$, $\beta=0.48$ and noise weights $(0.355,0.29,0.355)$:

- the weak incumbent gives no trade; the strong one gives full trade and entry $0.492$; at $3.6$ entry is back at $0.25$ with informative prices;
- at $1.55$, $1.60$, $1.65$, no trade coexists with a branch whose entry rises: $0.3505<0.3789<0.3802$;
- price access raises proceeds and net surplus.

Exact rational arithmetic certifies these results on a small box around the point. With EGJ's exact equal weights the branch has a closed form, but it starts at $1.557$.

The costs: entry is lower than the paper's; the rise is thin; only the top flow recruits on the branch; investor mixing is needed; prices are not monotone in the flow on the branch. The slot is Dow–Gorton's verified device; its combination with EGJ's noise has no verified precedent.
