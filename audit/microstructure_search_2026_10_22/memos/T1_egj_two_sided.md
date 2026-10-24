# T1. EGJ's own menu: two-sided unit orders, three-point noise, presence $\lambda$

Workstream T1. Scripts: `scripts/T1_egj_two_sided/`. Status of this file: complete, 22 October 2026.

## 1. Question

The author wants an EGJ-like trading block. This memo puts the trading block of Edmans, Goldstein and Jiang (2015, "EGJ") into the paper without changes, except that the challenger sees the price. It asks four things:

1. Which parts of the scorecard (BRIEF §2) does EGJ's own block reproduce?
2. Can entry return to $\rho$ at $r_2=3.6$? If not, what weaker statement holds, and what is the smallest change that restores it?
3. Can no trade coexist with an informative equilibrium on an interval of strengths that contains $1.55$ to $1.65$, with entry ordered upward?
4. What is the working range of the knob $\lambda$, and what does a second knob, symmetric noise weights $(\theta,1-2\theta,\theta)$, add?

Part A answers these for EGJ's equal weights, $\theta=1/3$. Part B adds the second knob.

## 2. Setup

### 2.1 Model

- **Classes and values (Reading N).** The class is $j\in\{H,L\}$ with prior $\pi=1/2$. Values are point masses at $h$ and $\ell$. The investor sees the class.
- **Costs.** The challenger's preparation cost is $0$ with probability $\rho$ and $c_H$ otherwise; $c_L=0$.
- **Auction.** The paper's cash second-price auction with reserve $p$; the incumbent's value is $R\sim U[0,r]$. The auction objects are those of TEAM_RULES §3. I checked them against eq. (4) of the pinned paper and against piecewise integration (`t1_equal_weights.out.txt`, Section A: the difference is exactly zero at six strengths).
- **Menu.** The investor, when present, chooses $q\in\{-1,0,1\}$ and pays $k|q|$. It has no initial position. Each class decides separately.
- **Noise law.** $Z\in\{-1,0,1\}$ with $\Pr(Z=\pm1)=\theta$ and $\Pr(Z=0)=\phi:=1-2\theta$, $\theta\in(0,1/2)$. EGJ's case is $\theta=1/3$. Write $d:=\phi-\theta=1-3\theta$.
- **Presence device.** The investor is present with probability $\lambda\in(0,1]$, independently of everything else. An absent investor sends $q=0$.
- **Flow and price.** $X=q+Z\in\{-2,\dots,2\}$. Competitive market makers set $P(X)=\mathbb E[V_T\mid X]$.
- **Challenger.** It sees the price and its cost, not the flow. It then prepares or stays out.

**Why this setup.** It copies EGJ's trading block item by item (`audit/alex_meeting_2026_10_21/memos/Q2_discrete_literature.md`, Table 2.1 and R1–R2): orders and noise on $\{-1,0,1\}$, equal noise weights, presence $\lambda$, a linear cost per unit, competitive pricing. The only change is that the challenger sees the price, as in the paper. The weights $(\theta,1-2\theta,\theta)$ with $\theta\neq1/3$ have no template in EGJ or Goldstein and Guembel (2008); that memo (notes to Table 2.2) records that neither paper uses unequal noise weights.

### 2.2 Strategies and notation

After Result 1 (dominance), a strategy profile is a pair of effective rates
$$a=\lambda\Pr(H\text{ buys}\mid\text{present}),\qquad b=\lambda\Pr(L\text{ sells}\mid\text{present}),\qquad (a,b)\in[0,\lambda]^2 .$$
The four pure profiles are no trade $\mathrm{NT}=(0,0)$, full orders $\mathrm T=(\lambda,\lambda)$, buy-not-sell $\mathrm{BNS}=(\lambda,0)$ and sell-not-buy $\mathrm{SNB}=(0,\lambda)$. The labels follow EGJ.

Other notation:

- $w_L=t_L-t_0$, $w_H=t_H-t_0$, $\Delta=\Delta_T$, $B(\mu)=g_L+\mu(g_H-g_L)$, $\tau=(c_H-g_L)/(g_H-g_L)$.
- Entry at a flow is $e_x=\rho+(1-\rho)\sigma_x$, where $\sigma_x$ is the high-cost type's preparation probability at the price of $x$.
- $\mathsf E$ is entry, $\mathsf O_H$ is high-class ownership, $\mathcal R_T$ is expected target proceeds, $\mathcal W$ is acquisition surplus net of preparation costs (the convention of `A_three_point.md`; the trading cost is excluded).
- $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$ solves $\Delta_T(r)=d$; $r_C(\mu)$ is the larger root of $B_r(\mu)=c_H$.

### 2.3 Equilibrium concept, beliefs and tie rules

- **Concept.** Perfect Bayesian equilibrium. A deviation faces the fixed candidate price and entry schedule. Prices are competitive given the entry they induce. Preparation is optimal given the posterior read from the price. Beliefs follow Bayes' rule at every used price.
- **Off-path flows.** Under NT both $X=\pm2$ are unused. Under BNS, $X=-2$ is unused. Under SNB, $X=+2$ is unused. T leaves no flow unused. I compare two rules:
  - **IC completion (EGJ's rule):** belief $1$ at an unused $X=+2$ and $0$ at an unused $X=-2$. EGJ use the Intuitive Criterion and the belief that the trader "knows the state" (Q2 memo, Table 2.2). A purchase by class $L$ and a sale by class $H$ lose at least $k$ under every response (Result 1), so the criterion removes them whenever some response makes the correct trade profitable. As in `A_bruteforce.md`, I call the belief the "directional completion" when the criterion is silent.
  - **Passive belief:** posterior $1/2$ at every unused flow.
  - Market makers and the challenger share the off-path belief.
- **Investor tie rules.** Rule Z: a tied class does not trade (EGJ's rule). Rule M: a tied class may mix.
- **Challenger tie rules.** Rule E: a tied high-cost type prepares (the paper's rule). Rule X: it may mix, possibly with different probabilities at different prices.

### 2.4 Benchmark

$h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_L=0$, $c_H=6$, $k=1/50$, $\pi=1/2$; $r_0=6/5$, $r_1=3$, $r_2=18/5$. At these strengths (exact, `t1_equal_weights.out.txt`, Section A):

| $r$ | $\Delta_T$ | $g_L$ | $g_H$ | $B_r(1/2)$ | $\tau$ | $b^*=2-1/\tau$ | $\kappa=3k/(\rho\Delta_T)$ |
|---|---|---|---|---|---|---|---|
| $6/5$ | $1/60$ | $5/16$ | $2231/240$ | $4.804167$ | $195/308=0.633117$ | $82/195$ | $72/5$ |
| $3$ | $2/3$ | $1/8$ | $203/24$ | $4.291667$ | $141/200=0.705$ | $82/141=0.581560$ | $9/25$ |
| $18/5$ | $169/180$ | $5/48$ | $5879/720$ | $4.134722$ | $4245/5804=0.731392$ | $2686/4245=0.632744$ | $216/845$ |

$B_r(1/2)=5-r/4+1/(8r)<6$ on $(1,10)$, so $\tau>1/2$ at every strength. $g_H(r)\ge c_H$ exactly when $r\le r_C(1)=4+\tfrac32\sqrt7=7.968627$.

## 3. Results

### Part A. Every $\theta$, and EGJ's equal weights $\theta=1/3$

#### Result 1 (analytical). Dominance and price sufficiency

**Claim.** In every equilibrium, under every belief rule and every tie rule: (a) class $H$ never sells and class $L$ never buys; (b) the price reveals the flow posterior.

*Proof.* (a) Fix any candidate schedule: a price at each flow, entry $e_x\in[\rho,1]$ at each price, and a belief $\mu_x\in[0,1]$ at each flow, used or not. The cost is independent of the class, and preparation depends only on the price and the cost. So $\mathbb E[V_T\mid j,x]=t_0+e_x(t_j-t_0)$. The competitive price is $P(x)=t_0+e_x(w_L+\Delta\mu_x)$. Subtraction gives
$$\mathbb E[V_T\mid H,x]-P(x)=e_x\Delta(1-\mu_x)\ge0,\qquad \mathbb E[V_T\mid L,x]-P(x)=-e_x\Delta\mu_x\le0 .$$
A sale by $H$ therefore earns $-\sum_z n(z)e_{z-1}\Delta(1-\mu_{z-1})-k\le-k<0$. A purchase by $L$ earns at most $-k<0$. Zero earns zero.

(b) $c_L=0<g_L\le B(\mu)$, so the low-cost type prepares at every price and $e_x\ge\rho>0$. Equal prices then force equal posteriors, because $P=t_0+e(P)(w_L+\Delta\mu)$ with $e(P)>0$. Optimal entry is nondecreasing in the belief, so for $\mu<\mu'$, $P'-P=e'\Delta(\mu'-\mu)+(e'-e)(w_L+\Delta\mu)\ge\rho\Delta(\mu'-\mu)>0$. This is Result 3 of `A_three_point.md`; it does not use the menu. $\square$

The scripts print the wrong-way payoffs at every reported equilibrium; all are below $-k$.

#### Result 2 (analytical). Flow laws and posteriors

With effective rates $(a,b)$ and $\pi=1/2$, the class-conditional flow laws are $f_H(x)=(1-a)n(x)+a\,n(x-1)$ and $f_L(x)=(1-b)n(x)+b\,n(x+1)$:

| $x$ | $f_H(x)$ | $f_L(x)$ | $\mu_x=f_H/(f_H+f_L)$ |
|---|---|---|---|
| $2$ | $a\theta$ | $0$ | $1$ if $a>0$; unused if $a=0$ |
| $1$ | $\theta+ad$ | $(1-b)\theta$ | $\dfrac{\theta+ad}{(2-b)\theta+ad}$ |
| $0$ | $\phi-ad$ | $\phi-bd$ | $\dfrac{\phi-ad}{2\phi-(a+b)d}$ |
| $-1$ | $(1-a)\theta$ | $\theta+bd$ | $\dfrac{(1-a)\theta}{(2-a)\theta+bd}$ |
| $-2$ | $0$ | $b\theta$ | $0$ if $b>0$; unused if $b=0$ |

*Derivation.* $X=1$ arises from $(q,z)=(0,1)$ or $(1,0)$ for class $H$, with probability $(1-a)\theta+a\phi=\theta+ad$, and from $(0,1)$ only for class $L$, with probability $(1-b)\theta$, because a sale cannot reach $X=1$. The other rows follow in the same way. Bayes' rule at prior $1/2$ gives the last column. $\square$

**The four pure profiles** (posteriors at $x=-2,\dots,2$):

| Profile | $\mu_{-2}$ | $\mu_{-1}$ | $\mu_0$ | $\mu_1$ | $\mu_2$ |
|---|---|---|---|---|---|
| T $(\lambda,\lambda)$ | $0$ | $\dfrac{(1-\lambda)\theta}{2(1-\lambda)\theta+\lambda\phi}$ | $\dfrac12$ | $\dfrac{(1-\lambda)\theta+\lambda\phi}{2(1-\lambda)\theta+\lambda\phi}$ | $1$ |
| BNS $(\lambda,0)$ | unused | $\dfrac{1-\lambda}{2-\lambda}$ | $\dfrac{(1-\lambda)\phi+\lambda\theta}{(2-\lambda)\phi+\lambda\theta}$ | $\dfrac{(1-\lambda)\theta+\lambda\phi}{(2-\lambda)\theta+\lambda\phi}$ | $1$ |
| SNB $(0,\lambda)$ | $0$ | $\dfrac{\theta}{(2-\lambda)\theta+\lambda\phi}$ | $\dfrac{\phi}{(2-\lambda)\phi+\lambda\theta}$ | $\dfrac1{2-\lambda}$ | unused |
| NT $(0,0)$ | unused | $\dfrac12$ | $\dfrac12$ | $\dfrac12$ | unused |

At equal weights ($\theta=\phi=1/3$) these become:

| Profile | $\mu_{-2}$ | $\mu_{-1}$ | $\mu_0$ | $\mu_1$ | $\mu_2$ |
|---|---|---|---|---|---|
| T | $0$ | $\dfrac{1-\lambda}{2-\lambda}$ | $\dfrac12$ | $\dfrac1{2-\lambda}$ | $1$ |
| BNS | unused | $\dfrac{1-\lambda}{2-\lambda}$ | $\dfrac12$ | $\dfrac12$ | $1$ |
| SNB | $0$ | $\dfrac12$ | $\dfrac12$ | $\dfrac1{2-\lambda}$ | unused |
| NT | unused | $\dfrac12$ | $\dfrac12$ | $\dfrac12$ | unused |

Under full orders and equal weights the flow $+1$ gives $1/(2-\lambda)$. These values match EGJ's posteriors as recorded in the Q2 memo (claim C1). The script prints them at $\lambda\in\{1/2,3/5,1\}$ (Section B).

Three facts follow:

- The extreme flows reveal the class whenever they are used. No choice of $\lambda$ or $\theta$ changes this.
- With $\lambda<1$, the flows $\pm1$ are interior under full orders. At $\lambda=1$ they reveal the class (EGJ's remark, Q2 memo R1).
- Under BNS the flow $+1$ stays interior even at $\lambda=1$, because class $L$ reaches it through noise. At equal weights its posterior is the prior. With $\theta<1/3$ it is above the prior.

#### Result 3 (analytical). Equal weights separate the two payoffs

Take $\theta=1/3$. A purchase reaches $X=0,1,2$ with probability $1/3$ each; a sale reaches $X=-2,-1,0$. Write $u(x)=(1-x)/(2-x)$. With the IC completion at unused extreme flows,
$$G_H(a,b)=\frac\Delta3\Big[\frac{e_0}2+e_1u(b)\Big],\qquad G_L(a,b)=\frac\Delta3\Big[e_{-1}u(a)+\frac{e_0}2\Big],$$
where $G_H$ is the gross payoff of a purchase by $H$ and $G_L$ of a sale by $L$.

*Derivation.* By Result 2, $\mu_0=1/2$, $1-\mu_1=u(b)$, $\mu_{-1}=u(a)$, and the residual at a revealing flow is zero. $\square$

So **the buyer's payoff depends only on the seller's rate, and the seller's payoff only on the buyer's rate.** Each class is camouflaged by the other's orders. On the benchmark domain $\tau>1/2$, so $e_0=e_{-1}=\rho$ at every profile. Only $e_1$ can exceed $\rho$, and only when $1/(2-b)\ge\tau$, that is $b\ge b^*:=2-1/\tau$.

Normalize by $\rho\Delta/3$. Define $\kappa=3k/(\rho\Delta)$ and
$$\gamma_H(b)=\tfrac12+\tfrac{e_1}{\rho}u(b),\qquad \gamma_L(a)=\tfrac12+u(a).$$
$\gamma_L$ falls strictly from $1$ at $a=0$ to $\ell_\lambda:=\tfrac12+u(\lambda)=\dfrac{4-3\lambda}{2(2-\lambda)}$ at $a=\lambda$. $\gamma_H$ equals $\gamma_L$ below $b^*$ and jumps up by the factor $1/\rho$ on its second term at $b^*$.

#### Result 4 (analytical). The complete equilibrium correspondence at equal weights

Assume $\theta=1/3$, $\pi=1/2$, $c_L=0$ and $1/2<\tau\le1$ (the benchmark domain). Let $s(\kappa)=u^{-1}(\kappa-\tfrac12)$ and $b_R(\kappa)=u^{-1}(\rho(\kappa-\tfrac12))$, where $u^{-1}(y)=(1-2y)/(1-y)$.

**(a) Full-order region, $\kappa<\ell_\lambda$.** T is the unique equilibrium. It has no unused flow and no tie, so this holds under every belief rule and every tie rule.

**(b) No-trade region, $\kappa>1$.** Under the IC completion, NT is the unique equilibrium, under every tie rule.

**(c) The band, $\ell_\lambda\le\kappa\le1$ (IC completion).** The equilibria are:

1. BNS, for every $\kappa$ in the band under rule M, and for $\kappa\in[\ell_\lambda,1)$ under rule Z.
2. SNB, if and only if $\gamma_H(\lambda)\le\kappa$. If $\lambda<b^*$ this holds on the whole band. If $\lambda>b^*$ (or $\lambda=b^*$ under rule E) it needs $\kappa\ge\tfrac12+u(\lambda)/\rho$, which is possible only if $\lambda\ge6/7$ (at $\rho=1/4$).
3. Rule M adds mixed equilibria with $a=s(\kappa)\in(0,\lambda)$ and:
   - $b=s(\kappa)$, if $s(\kappa)<b^*$ (no recruitment at $X=1$);
   - $b=b_R(\kappa)$, if $b^*\le b_R(\kappa)\le\lambda$ (recruitment at $X=1$);
   - $b=b^*$ with challenger mixing at $X=1$ (rule X), if $\tfrac12+u(b^*)\le\kappa\le\tfrac12+u(b^*)/\rho$.
4. At the knife-edges $\kappa\in\{\ell_\lambda,1,\gamma_H(\lambda)\}$, rule M adds continua that join the outcomes above.

**(d) Coexistence.** No trade coexists with an informative equilibrium only at $\kappa=1$, and only under rule M. Under rule Z the equilibrium at $\kappa=1$ is NT alone.

**(e) Passive beliefs.** T is unique for $\kappa<\ell_\lambda$. NT is an equilibrium if and only if $\kappa\ge3/2$. **No equilibrium exists for $\kappa\in(1,3/2)$.** On the open band $(\ell_\lambda,1)$, no pure profile is an equilibrium, except at $\lambda=1$ and $\kappa=1$; only the mixed equilibria of (c3), which use no unused flow, survive. Under rule Z and passive beliefs, the open band has no equilibrium.

*Proof.* Each class has two relevant actions. $H$ buys fully if $\gamma_H(b)>\kappa$, abstains if $\gamma_H(b)<\kappa$, and may mix only at equality (rule M). The same holds for $L$ with $\gamma_L(a)$.

- (a) $\gamma_L(a)\ge\ell_\lambda>\kappa$ for every $a$, so $b=\lambda$. Then $\gamma_H(\lambda)\ge\tfrac12+u(\lambda)=\ell_\lambda>\kappa$, so $a=\lambda$. No inequality is tight.
- (b) $\gamma_L(a)\le1<\kappa$, so $b=0$. Then $\gamma_H(0)=\tfrac12+u(0)=1<\kappa$, because $e_1=\rho$ at the posterior $1/2<\tau$. So $a=0$. Under NT the unused flows $\pm2$ carry beliefs $1$ and $0$; their residuals are zero, so the deviation payoffs are the same formulas.
- (c) $\gamma_L$ is strictly decreasing, with $\gamma_L(s(\kappa))=\kappa$. So $L$ sells fully for $a<s(\kappa)$, is indifferent at $a=s(\kappa)$, and abstains for $a>s(\kappa)$. If $a\ne s(\kappa)$, then $b\in\{0,\lambda\}$:
  - $a=\lambda>s(\kappa)$ forces $b=0$, and $\gamma_H(0)=1\ge\kappa$ supports $a=\lambda$: this is BNS.
  - $a=0<s(\kappa)$ forces $b=\lambda$; this is an equilibrium iff $\gamma_H(\lambda)\le\kappa$: this is SNB. With recruitment, $\gamma_H(\lambda)=\tfrac12+u(\lambda)/\rho\le1$ iff $u(\lambda)\le\rho/2=1/8$ iff $\lambda\ge6/7$.
  - Interior $a\ne s(\kappa)$ needs $\gamma_H(b)=\kappa$ with $b\in\{0,\lambda\}$: only the knife-edges $\kappa=1$ or $\kappa=\gamma_H(\lambda)$.

  If $a=s(\kappa)\in(0,\lambda)$, $H$ must be indifferent, so $\gamma_H(b)=\kappa$. Below $b^*$ this gives $b=s(\kappa)$. Above $b^*$ it gives $\tfrac12+u(b)/\rho=\kappa$, that is $b=b_R(\kappa)$. At $b^*$, rule X lets $e_1$ take any value in $[\rho,1]$; $\gamma_H(b^*)$ then covers $[\tfrac12+u(b^*),\tfrac12+u(b^*)/\rho]$.
- (d) For $\kappa>1$, part (b) leaves NT alone. For $\kappa<1$, NT fails because $\gamma_H(0)=1>\kappa$ under the IC completion. At $\kappa=1$, rule Z makes both tied classes abstain.
- (e) Under passive beliefs an unused extreme flow adds $\tfrac12$ to the deviating class's $\gamma$: the residual there is $e(1/2)\Delta/2=\rho\Delta/2$ with weight $1/3$. NT needs $\gamma_H(0)+\tfrac12=\tfrac32\le\kappa$. For $\kappa\in(1,3/2)$: any $b>0$ needs $\gamma_L(a)\ge\kappa>1$, which is impossible, so $b=0$. Then any $a>0$ needs $\gamma_H(0)=1\ge\kappa$, which fails, so $a=0$. But then NT needs $\kappa\ge3/2$. BNS needs $\ell_\lambda+\tfrac12\le\kappa\le1$, so $\ell_\lambda\le1/2$, which holds only at $\lambda=1$ and $\kappa=1$. SNB needs $\gamma_H(\lambda)+\tfrac12\le\kappa\le1$; since $\gamma_H(\lambda)\ge1/2$, this is the same knife-edge. The mixed equilibria of (c3) use every flow, so they are unchanged. $\square$

**Exact check.** The script evaluates every predicted equilibrium of (c) at rational points of the band. The mixed rates are rational there, so the check is exact (`t1_equal_weights.out.txt`, Section F). Example at $\lambda=1$, $r=2$ ($\kappa=24/25$): BNS, SNB, $(s,s)$ with $s=4/27$, $(s,b_R)$, and $(s,b^*)$ with $e_1=0.3426$ are all equilibria. Their entry levels are $0.375$, $0.375$, $0.2685$, $0.4098$ and $0.2917$.

**EGJ's asymmetry, in this model.** For $\lambda\in[b^*,6/7)$ recruitment at $X=1$ removes SNB from the band, and BNS remains. This is the direction of EGJ's feedback result (buying is more profitable than selling; Q2 memo C7), here produced by the entry jump. The exact window $\lambda\in[82/141,6/7)$ at $r=3$ agrees with `V_discrete_check.md` §3.4, now at $c_L=0$ and with mixed equilibria included.

#### Result 5 (analytical; exact values). Proposition 2 at the benchmark, equal weights

**(i) Weak incumbent, $r_0=6/5$.** Every order's gross payoff is at most $\Delta_T(6/5)=1/60<k=1/50$. So NT is the unique equilibrium, entry is $\rho$, and the price is constant. This holds for every $\lambda$ and every $\theta$, under every belief rule and every tie rule.

**(ii) Strong incumbent, $r_1=3$.** $\kappa=9/25<1/2\le\ell_\lambda$, so T is the unique equilibrium for **every** $\lambda\in(0,1]$ (Result 4a). The trading outcome holds under every belief rule and every tie rule. The entry table below uses rule E; at exactly $\lambda=82/141$ the posterior at $X=1$ equals $\tau$, so rule X admits any entry in $[\tfrac14+\tfrac\lambda8,\tfrac12]$. The flow $+2$ always recruits, because $g_H(3)=203/24>6$. The flow $+1$ recruits if and only if $1/(2-\lambda)\ge\tau(3)=141/200$, that is $\lambda\ge82/141=0.581560$. Hence

| | $\lambda<82/141$ | $\lambda\ge82/141$ |
|---|---|---|
| $\mathsf E(r_1)$ | $\tfrac14+\tfrac\lambda8$ | $\tfrac12$ |
| $\mathsf O_H(r_1)$ | $\tfrac18+\tfrac\lambda8$ | $\tfrac14+\tfrac\lambda8$ |
| $\mathcal R_T(r_1)$ | $\tfrac{59}{96}+\tfrac{9\lambda}{64}$ | $\tfrac{13}{16}+\tfrac\lambda{12}$ |

*Derivation.* Under T the unconditional flow probabilities are $(\lambda,2-\lambda,2,2-\lambda,\lambda)/6$ at $x=-2,\dots,2$. Entry is $1$ at recruiting flows and $\rho$ elsewhere, so $\mathsf E=\rho+(1-\rho)[\lambda/6+\mathbf 1\{\lambda\ge b^*\}(2-\lambda)/6]$. Class $H$ reaches $(2,1,0,-1)$ with probabilities $(\lambda,1,1,1-\lambda)/3$, which gives $\mathsf O_H$. $\mathcal R_T=t_0+\mathsf O_Hw_H+(\mathsf E-\mathsf O_H)w_L$ with $t_0=5/12$, $w_H=9/8$, $w_L=11/24$. $\square$

At $\lambda=1$: $\mathsf E=1/2$, $\mathsf O_H=3/8$, $\mathcal R_T=43/48$. The paper has $0.522757$, $0.324192$, $0.872392$. With $\lambda\ge82/141$ the entry level is flat in $\lambda$, because $\Pr(X\ge1)=1/3$ for every $\lambda$; presence only moves recruiting mass between the flows $+1$ and $+2$. The exact rows for 13 values of $\lambda$ are in Sections C–D of the output.

**(iii) Return, $r_2=18/5$.** $\kappa=216/845<1/2$, so T is again unique. The flow $+2$ still recruits ($g_H=5879/720>6$). Entry is $\tfrac12$ if $\lambda\ge2686/4245=0.632744$, and $\tfrac14+\tfrac\lambda8>\tfrac14$ otherwise. **Entry never returns to $\rho$.** Result 6 shows that no $\lambda$ and no $\theta$ repairs this.

#### Result 6 (analytical). Proposition 2(iii) fails for every $\lambda$ and every $\theta$

**Claim.** Fix $r_2$ with $g_H(r_2)>c_H$ and $k<\tfrac12\rho\Delta(r_2)[1-\tau(r_2)]$. Then for every $\lambda\in(0,1]$ and every $\theta\in(0,1/2)$, every equilibrium at $r_2$ has entry strictly above $\rho$. This holds under every off-path belief and every tie rule. At the benchmark the bound is $\tfrac12\rho\Delta(18/5)[1-\tau(18/5)]=263471/8357760=0.031524>1/50$.

*Proof.* Suppose an equilibrium at $r_2$ has entry $\rho$. Then every used flow has $e_x=\rho$.

1. $a=0$. Otherwise $X=2$ is used, its posterior is $1$, and $B(1)=g_H(r_2)>c_H$ forces $e_2=1$ under either challenger rule.
2. With $a=0$ the flows $0$ and $1$ are used ($f_H(0)=\phi>0$, $f_H(1)=\theta>0$). Entry $\rho$ there requires $\mu_0,\mu_1\le\tau$; strict excess would force $e=1$.
3. A purchase by $H$ then earns at least
$$\theta\rho\Delta(1-\mu_0)+\phi\rho\Delta(1-\mu_1)+\theta e_2\Delta(1-v_+)-k\ \ge\ \rho\Delta(1-\theta)(1-\tau)-k\ \ge\ \tfrac12\rho\Delta(1-\tau)-k>0,$$
because $\theta+\phi=1-\theta>1/2$ and the residual at the unused $X=2$ is nonnegative for every belief $v_+$.
4. So $H$ strictly prefers to buy, which contradicts $a=0$. $\square$

**A stronger version at equal weights.** At $\theta=1/3$ the claim holds for **every** $k$ at which $r_1=3$ has an informative equilibrium. Informative trade at $r_1$ needs $\kappa(r_1)\le1$, that is $k\le\rho\Delta(3)/3=1/18$ (Result 4b). With $a=0$ and no recruiting flow at $18/5$, $u(b)\ge1-\tau$, so $G_H\ge\tfrac{\rho\Delta}3(\tfrac12+1-\tau)=251303/4178880=0.060136>1/18$. So no trading cost restores the return at equal weights.

#### Result 7 (analytical; exact brackets). What holds instead: two ceilings

Under T there are two recruiting flows with two ceilings:

- the interior flow $+1$, with posterior $\nu=1/(2-\lambda)$ at equal weights, recruits up to $r_C(\nu)$;
- the revealing flow $+2$ recruits up to $r_C(1)=4+\tfrac32\sqrt7=7.968627$.

So, along the full-order region, entry is a step function of strength:
$$\mathsf E_{\mathrm T}(r)=\begin{cases}\tfrac12,& r\le r_C(\nu)\ \text{and}\ \lambda\ge b^*(r),\\[2pt] \tfrac14+\tfrac\lambda8,& r_C(\nu)<r\le r_C(1),\\[2pt] \tfrac14,& r>r_C(1).\end{cases}$$

**The weaker statement that holds.** For $\lambda\in[82/141,\,2686/4245)=[0.581560,0.632744)$, entry falls from $\tfrac12$ at $r_1=3$ to $\tfrac14+\tfrac\lambda8\in[0.3227,0.3291)$ at $r_2=18/5$, while trade stays full and informative. Entry keeps the fraction $(\mathsf E(r_2)-\rho)/(\mathsf E(r_1)-\rho)=\lambda/2\approx0.3$ of its rise. Outside this window, entry at $r_2$ equals entry at $r_1$.

**A calibration that matches the paper's ceiling.** Set $\lambda=1-e^{-2/b}$. At $b=2$ this is $0.632121$, inside the window. Then $1/(2-\lambda)=1/(1+e^{-2/b})=M$, the paper's upper posterior bound, and the interior ceiling equals the paper's $r_C=3.592658519$ (bracketed in Section G of the output). Entry is $\tfrac12$ on $(2.1616,3.5927]$, then $0.329015$ up to $7.968627$, then $\tfrac14$.

Ceilings of the flow $+1$ for other $\lambda$ (Section G): $3.000$ at $\lambda=82/141$, $3.216$ at $3/5$, $3.509$ at $5/8$, $3.600$ at $2686/4245$, $4.394$ at $7/10$, $5.582$ at $4/5$, $7.969$ at $1$. For $\lambda\le1/2$ the flow $+1$ recruits only below $r\approx2.06$, inside or below the band.

#### Result 8 (analytical). The smallest changes that restore Proposition 2(iii)

Results 6–7 leave three ways to return entry to $\rho$ at $r_2$ while trade stays full. Each is exact at equal weights; the trading region is unchanged because T is unique whenever $\kappa<1/2$.

1. **Move $r_2$ above $r_C(1)=7.968627$.** The paper's $r_2=3.6$ is replaced by a strength more than twice $r_1$.
2. **Raise $c_H$ into $(g_H(r_2),g_H(r_1)]=(5879/720,\,203/24]=(8.1653,\,8.4583]$.** Then nothing recruits at $r_2$. At $r_1$ the threshold belief is at least $0.9648$: the flow $+2$ recruits, and the flow $+1$ recruits only if $\lambda\ge2-1/\tau$, that is $\lambda>0.9635$. Entry is $\tfrac14\to\tfrac14+\tfrac\lambda8\to\tfrac14$ below that presence level, and $\tfrac14\to\tfrac12\to\tfrac14$ at $\lambda=1$. This needs $c_H/h\in(0.817,0.846]$: **a documented failure** under BRIEF §2 ("$c_H$ near $h$").
3. **Lower $h$ into $[181/24,\,5641/720)=[7.5417,\,7.8347)$ with $c_H=6$.** This is the same condition, $g_H(r_2)<c_H\le g_H(r_1)$, read through $h$. The expensive challenger must barely cover its cost when it is sure of class $H$.

No choice of $\lambda$, $\theta$ or $k$ works at the paper's $(h,c_H)$ and strengths (Result 6). The obstacle is the one the brief names: a revealing flow recruits whenever $g_H(r)\ge c_H$.

#### Result 9 (analytical). Proposition 3 fails at equal weights

By Result 4(d), no trade coexists with an informative equilibrium only on the knife-edge $\kappa=1$, that is $r=\mathfrak r(3k/\rho)=1.973212$ at $k=1/50$, and only under rule M. The paper's strengths $1.55$–$1.65$ have $\kappa\in(1.87,2.46)$: NT is the unique equilibrium there.

*Why.* At equal weights the seller's payoff never benefits from recruitment: a sale reaches $X\in\{-2,-1,0\}$, where the posterior is at most $1/2<\tau$. Under T the seller's payoff is $\gamma_L(\lambda)=\ell_\lambda<1$, the value of its deviation from NT. Under BNS the flow $+1$ sits at the prior, so the buyer earns $\gamma_H(0)=1$, again the NT deviation value. So every informative profile pays at most what a deviation from NT pays. Feedback cannot lift the informative payoffs above the no-trade deviation value, which is what coexistence needs.

#### Result 10 (analytical; exact values). Proposition A.9 at $r_1$, equal weights

With hidden prices the challenger's belief is $1/2<\tau$, so entry is $\rho$ at every flow. The payoffs become $\gamma_H=\tfrac12+u(b)$ and $\gamma_L=\tfrac12+u(a)$, both at least $\ell_\lambda>\kappa(3)=9/25$. So T is again the unique outcome. Both economies have the same order-flow experiment and the same trading cost. Access to prices adds preparation exactly at the recruiting flows:
$$\Delta\mathcal R_T=\begin{cases}\tfrac{9\lambda}{64},&\lambda<82/141,\\[2pt] \tfrac{19+8\lambda}{96},&\lambda\ge82/141,\end{cases}\qquad
\Delta\mathcal W=(1-\rho)\sum_x w_x\sigma_x\Big[B(\mu_x)-c_H+\frac{p^2}r\Big]>0 .$$
At $\lambda=1$: $\Delta\mathcal R_T=9/32=0.28125$ and $\Delta\mathcal W=61/96=0.635417$ (paper: $0.257809$ for proceeds). At $\lambda=3/5$: $119/480$ and $7/32$. Hidden-price proceeds are $59/96=0.614583$, the paper's value. Both differences are positive for every $\lambda$ (Section I of the output). Prop. A.9 survives.

#### Result 11 (analytical). Which claims need EGJ's "informed" belief

| Claim | Unused flows | Needs the IC completion? | Under passive beliefs |
|---|---|---|---|
| Prop. 2(i) at the benchmark | $\pm2$ | No: $\Delta_T(r_0)<k$ beats every belief | NT unique |
| Prop. 2(ii) at the benchmark | none (T) | No | unchanged |
| Result 6 (no return) | $+2$ if $a=0$ | No: the bound uses a nonnegative residual | unchanged |
| NT near its boundary, $\kappa\in[1,3/2)$, i.e. $r\in(1.7479,1.9732]$ | $\pm2$ | Yes | **no equilibrium** on $\kappa\in(1,3/2)$ |
| BNS and SNB in the band | one extreme flow | Yes | fail, except the knife-edge $\lambda=1$, $\kappa=1$ |
| Existence in the band under rule Z | one extreme flow | Yes | **no equilibrium** |
| Coexistence at $\kappa=1$ | $\pm2$ | Yes | fails |

The passive no-trade boundary is $\mathfrak r(2k/\rho)=1.747878$, the paper's $r_N$; the IC boundary is $\mathfrak r(3k/\rho)=1.973212$. These are the three-point values of `A_three_point.md`, Result 5; the two-sided menu does not change them.

### Part B. The second knob: symmetric weights $\theta\ne1/3$

Part A shows why EGJ's equal weights lose Proposition 3: each class's payoff depends only on the other class's rate, and the recruiting flow $+1$ sits at the prior under BNS. Unequal weights break both facts. With $\theta<1/3$ ("hump-shaped" noise, more mass at zero), the flow $+1$ under a purchase is informative even when class $L$ never sells, so it can recruit while class $L$ still reaches it through noise.

#### Result 12 (analytical). Payoffs and the no-trade boundary for general $\theta$

With the posteriors of Result 2,
$$\frac{G_H}{\Delta}=\theta e_0(1-\mu_0)+\phi e_1(1-\mu_1)\ [+\theta e(v_+)(1-v_+)\text{ if }a=0],\qquad
\frac{G_L}{\Delta}=\phi e_{-1}\mu_{-1}+\theta e_0\mu_0\ [+\theta e(v_-)v_-\text{ if }b=0].$$
For $\theta\ne1/3$ both payoffs depend on both rates, so the camouflage is no longer separable.

**No-trade boundary.** NT is an equilibrium if and only if $k\ge\rho\Delta(1-\theta)/2$ under the IC completion, and $k\ge\rho\Delta/2$ under passive beliefs.

*Proof.* Under NT every used posterior is $1/2<\tau$, so entry is $\rho$ there. A purchase by $H$ reaches $X=0,1$ with probabilities $\theta,\phi$ and posterior $1/2$, and $X=2$ with probability $\theta$. Under the IC completion the residual at $X=2$ is zero, so the purchase earns $\rho\Delta(\theta+\phi)/2=\rho\Delta(1-\theta)/2$. Under passive beliefs the third flow adds $\theta\rho\Delta/2$, so the total is $\rho\Delta/2$. A sale by $L$ is the mirror image. $\square$

In strength: $r\le\mathfrak r\big(2k/(\rho(1-\theta))\big)$ (IC; exactly $9/5$ at $\theta=1/10$) and $r\le\mathfrak r(2k/\rho)=1.747878$ (passive, for every $\theta$). The IC boundary rises from $1.7479$ at $\theta\to0$ to $1.9732$ at $\theta=1/3$.

#### Result 13 (analytical). The partial-buy branch: entry rises with strength

Take $\theta<1/3$, $\rho<1$, the benchmark domain $1/2<\tau\le1$, and profiles $(a,0)$: class $H$ buys with rate $a\in(0,\lambda)$, class $L$ never sells. Suppose the flow $+1$ recruits and the flows $0,-1$ do not, so $e=(\rho,\rho,1)$ at $x=(-1,0,1)$. Define
$$K(a)=\frac{\rho\theta\phi}{2\phi-ad}+\frac{\theta\phi}{2\theta+ad},\qquad
J(a)=\rho\Big[\frac{\phi(1-a)}{2-a}+\frac{\theta(\phi-ad)}{2\phi-ad}\Big],\qquad
a_\tau(r)=\frac{\theta(2\tau-1)}{d(1-\tau)} .$$

**Claim.**

- (a) $K$ is strictly decreasing on $[0,1]$.
- (b) $(a,0)$ with this entry pattern is an equilibrium (rule M; either challenger rule; IC completion) if and only if $K(a)=k/\Delta$, $a>a_\tau(r)$ and $J(a)\le k/\Delta$. Under passive beliefs, replace $J(a)$ by $J(a)+\theta\rho/2$.
- (c) On every interval of strengths on which (b) holds with strict inequalities, the buying rate $a(r)$ and entry
$$\mathsf E(r)=\rho+(1-\rho)\Big(\theta+\frac{a(r)\phi}2\Big),\qquad \mathsf O_H(r)=\tfrac12\big[\theta+\rho(1-\theta)+a(r)\phi(1-\rho)\big]$$
are strictly increasing in $r$.
- (d) The branch does not depend on $\lambda$, except through the cap $a<\lambda$.

*Proof.*

- (a) $K'(a)=\theta\phi d\,[\rho(2\phi-ad)^{-2}-(2\theta+ad)^{-2}]$. It is negative if and only if $\sqrt\rho(2\theta+ad)<2\phi-ad$, that is $ad(1+\sqrt\rho)<2(\phi-\sqrt\rho\,\theta)$. At $a=1$ the left side is $(\phi-\theta)(1+\sqrt\rho)$, and the inequality reduces to $\sqrt\rho(\phi+\theta)<\phi+\theta$, which holds. The left side increases in $a$, so $K'<0$ on $[0,1]$.
- (b) At $b=0$, $1-\mu_0=\phi/(2\phi-ad)$ and $1-\mu_1=\theta/(2\theta+ad)$ by Result 2, so $G_H/\Delta=K(a)$. Interior $a$ needs indifference, $K(a)=k/\Delta$. The flow $+1$ recruits iff $\mu_1=(\theta+ad)/(2\theta+ad)>\tau$, that is $a>a_\tau$. The flows $0,-1$ have posteriors below $1/2<\tau$ because $d>0$. The flow $+2$ has posterior $1$ and recruits because $\tau\le1$. Class $L$ must not gain from a sale: $G_L/\Delta=J(a)\le k/\Delta$, with the residual at the unused $X=-2$ equal to $0$ (IC) or $\rho/2$ (passive).
- (c) $\Delta$ is strictly increasing in $r$, so $k/\Delta$ falls. By the implicit function theorem $a'(r)=-k\Delta'(r)/[\Delta(r)^2K'(a)]>0$. Under $(a,0)$ the unconditional probabilities of the flows $+2$ and $+1$ are $a\theta/2$ and $(2\theta+ad)/2$; they sum to $\theta+a\phi/2$, which gives $\mathsf E$. Class $H$ reaches the recruiting flows with probability $\theta+a\phi$, which gives $\mathsf O_H$.
- (d) $\lambda$ enters none of $K$, $J$, $a_\tau$. $\square$

The branch is a buyer's mixing branch, the mirror image of the paper's partial sales: as the incumbent strengthens, the buying probability rises toward one, and entry rises with it. It ends at $a=\lambda$, where it joins BNS with entry $\rho+(1-\rho)(\theta+\lambda\phi/2)$. At its lower end the flow $+1$ posterior reaches $\tau$; there it meets a second branch on which the challenger mixes at $X=1$.

#### Result 14 (computer-assisted at each grid point; numerical diagnostic between points). Maps over $(\theta,\lambda)$

**Method.** `t1_solver.py` enumerates every equilibrium at a rational parameter point:

- corners (pure profiles), with free entry rates at ties (exact linear feasibility);
- edges (one class mixes), split at the lines $\mu_x=\tau$, with exact univariate quadratics;
- open cells (both classes mix): the resultant of the two indifference conditions in $a$ (degree $\le4$ in $b$), real roots isolated by Sturm sequences with rational endpoints, and $a=(A_2B_0-A_0B_2)/(A_1B_2-A_2B_1)$ evaluated in rational interval arithmetic;
- line segments (the challenger mixes at one flow) and line crossings (it mixes at two).

The grid has $\theta\in\{1/50,\dots,24/50\}$, $\lambda\in\{1/20,\dots,1\}$, $r\in\{6/5,31/20,8/5,33/20,3,18/5\}$ and four rule sets: 11,520 runs, **zero undecided cases**.

Two checks support the enumeration:

- An independent brute-force search in floating point (`t1_crosscheck.py`) shares no code with the solver. At all 10 test points it finds the same number of equilibria. Entry levels agree to six decimals, except at one interior challenger-mixing point ($r=2$, $\theta=0.333$), where they agree to three decimals because the brute force samples the line and does not solve for the root.
- `t1_certificates.py` re-verifies each reported equilibrium of the candidate by direct Bayes-rule evaluation in rational interval arithmetic.

**Findings** (`t1_summary.out.txt`):

1. **Prop. 2(i).** NT is the unique equilibrium at $r_0=6/5$ at every grid point, under every rule set (Result 5(i)).
2. **Prop. 2(ii), rule M.** At $r_1=3$ every grid point has an equilibrium, none has NT, and every equilibrium has entry in $[0.25075,0.6997]$, above $\rho$. The equilibrium is unique except at 35 points with $\theta\in[0.04,0.28]$ and $\lambda\ge0.80$. The unique profile is:
   - T for $\theta\ge0.30$ at every $\lambda$, and for small $\lambda$ at every $\theta$;
   - **full buy with partial sale (the paper's $(1,-v)$)** on a band of $\lambda$ for $\theta\le0.18$ (for example $\lambda\in[0.55,0.85]$ at $\theta=0.10$);
   - BNS at a few points near the upper edge of that band.
3. **Rule Z (EGJ's tie rule).** At $r_1$, **69 grid points have no equilibrium**. At 65 of them the unique rule-M equilibrium has a mixing seller: 59 full buy with partial sale (the $(1,-v)$ band) and 6 with both classes mixing ($\theta=0.02$, $\lambda\ge0.75$). The other 4 have several rule-M equilibria. Existence there needs mixing.
4. **Prop. 2(iii).** The minimum entry at $r_2=18/5$ over all equilibria, grid points and rule sets is $0.25075>\rho$, as Result 6 requires.
5. **Prop. 3, rule M, IC.** At all three strengths $1.55,1.60,1.65$, NT coexists with an informative equilibrium for $\theta\le0.24$ (with a $\lambda$-dependent lower bound). A pure-entry branch with strictly rising entry exists for $\theta\le0.18$ and $\lambda$ above a threshold: $0.10$ at $\theta=0.02$, $0.45$ at $\theta=0.10$, $0.80$ at $\theta=0.16$, $1.0$ at $\theta=0.18$. The same holds under rule E and under passive beliefs (all three strengths lie below $1.7479$).
6. **Prop. 3, rule Z.** Coexistence survives only through pure BNS, whose entry is flat across strengths (for example $\theta=0.20$, $\lambda=0.6$: NT and BNS with entry $0.535$ at all three strengths). No upward branch exists. So pure coexistence does occur with symmetric unequal weights; the T1 row of `L2_taxonomy.md` ("no coexistence in pure profiles") holds at equal weights only.
7. For $\theta\ge0.26$ no grid point has coexistence at all three strengths. Three points have it at one strength: $(\theta,\lambda)=(0.26,1)$ at $1.55$, and $(0.40,0.95)$, $(0.40,1)$ at $1.65$ (U-shaped noise).
8. **Joint region** (a unique informative equilibrium at $r_1$ and an upward branch at $1.55$–$1.65$): $\theta\in[0.02,0.16]$ with a band of $\lambda$. On the finer grids of `t1_refine.out.txt`: $\lambda\in[0.42,0.86]$ at $\theta=1/10$ (45 contiguous points of the $1/100$ grid) and $\theta\in[0.01,0.14]$ at $\lambda=7/10$.

#### Result 15 (computer-assisted). The candidate $\theta=1/10$, $\lambda=7/10$

Noise weights $(1/10,4/5,1/10)$; the investor is present with probability $0.7$. Every number below is exact or a rational enclosure of width below $10^{-25}$ (`t1_certificates_theta1-10_lam7-10.out.txt`). Rules M, X, IC unless stated.

| $r$ | Equilibria (entry $\mathsf E$) | Notes |
|---|---|---|
| $6/5$ | NT ($1/4$) | unique under all four rule sets |
| $31/20$ | NT ($1/4$); partial buy, challenger mixes at $X=1$ ($0.315140$); partial buy, pure entry, $a=0.314319$ ($0.419296$) | rule Z: NT only |
| $8/5$ | NT; $0.302316$; $a=0.417656$ ($0.450297$) | same structure |
| $33/20$ | NT; $0.292078$; $a=0.531020$ ($0.484306$) | same structure |
| $3$ | **full buy, partial sale**, $b=0.204137$, $v=b/\lambda=0.291625$ ($0.527345$) | unique; rule Z: **no equilibrium** |
| $18/5$ | T ($407/800=0.508750$) | unique under all four rule sets |

- **Prop. 2(i)** holds. **Prop. 2(ii)** holds with the paper's pattern $(1,-v)$: entry $0.527345$ (paper $0.522757$), $\mathsf O_H=149/400=0.3725$ (paper $0.324192$), $\mathcal R_T=0.906700$ (paper $0.872392$). **Prop. 2(iii)** fails: entry $0.50875$ at $18/5$.
- **Prop. 3.** The upward certificate: $\mathsf E=0.419296<0.450297<0.484306$ at $31/20,8/5,33/20$, with gaps of at least $0.0310$ and $0.0340$ between the enclosures. The second informative branch (challenger mixing) moves down: $0.315140>0.302316>0.292078$.
- **Intervals** (exact brackets, `t1_refine.out.txt` Section C):
  - NT exists for $r\le9/5$ (IC) and $r\le1.747878$ (passive);
  - the pure partial-buy branch lives on $[1.438562,\,1.715767]$, with entry rising from about $0.36$ to $107/200=0.535$;
  - BNS (entry $0.535$, flat) follows up to $r=2.322153$, where class $L$ starts to sell;
  - so NT coexists with an informative equilibrium on $[1.438562,1.8]$ (IC) or $[1.438562,1.747878]$ (passive). Both contain $1.55$–$1.65$.

#### Result 16 (computer-assisted). Prop. A.9 at the candidate

With hidden prices, entry is $\rho$ at every flow. The hidden-price game has three equilibria: full buy with partial sale (the same orders as with feedback, because the seller's indifference never involves a recruiting flow), its mirror image, and a symmetric mixed profile. All three have $\mathcal R_T=59/96$ and $\mathcal W=245/96$, because entry $\rho$ does not depend on the order flow. Against each of them, price access raises proceeds by $0.292116$ and net surplus by $0.456211$. Against the matched profile the trading cost is identical ($0.009041$). **Prop. A.9 survives.** The paper's external-dividend diagnostic is therefore $0.292116$ (paper $0.257809$).

#### Result 17 (analytical; summary). What the second knob costs

1. **Investor mixing is essential.** The unique equilibrium at $r_1$ has a seller who mixes, and the upward branch has a buyer who mixes. Under EGJ's rule Z the first has no equilibrium at all, and the second disappears. EGJ themselves use pure strategies; Goldstein and Guembel (2008) use mixed strategies (Q2 memo, Table 2.1).
2. **The noise is far from EGJ's.** The working range needs $\theta\le0.14$–$0.16$: noise traders trade in at most 28–32 per cent of periods, against two thirds in EGJ. No verified source uses unequal EGJ weights (Q2 memo, notes to Table 2.2; `L1_survey.md` §5.6).
3. **The patterns are swapped.** The paper's partial sale appears at $r_1$; the upward coexistence branch is a partial purchase.
4. **Prop. 2(iii) still fails** (Result 6).

#### Result 18 (interpretation). The knob $\lambda$ and its working range

EGJ give three readings of $\lambda$ (Q2 memo R2; `L1_survey.md` §5.1): the trader is present with probability $\lambda$; it is always present but a liquidity shock stops its trade with probability $1-\lambda$; or it is informed only with probability $\lambda$.

- The first two readings give the same game here. An absent investor and a blocked investor both send $q=0$, and no one observes which. Every result in this memo holds under either reading.
- The third reading lets an uninformed investor trade, possibly to manipulate. It is a different game; workstream T2 studies it.

What $\lambda$ does:

- **Equal weights.** $\lambda$ sets the posterior $1/(2-\lambda)$ of the interior flow $+1$. Prop. 2(i)–(ii) hold for every $\lambda\in(0,1]$. The interior flow recruits at $r_1$ iff $\lambda\ge82/141=0.582$ (entry $1/2$). Entry falls between $r_1$ and $r_2$ only for $\lambda\in[0.582,0.633)$. The value $\lambda=1-e^{-2/b}=0.632$ reproduces the paper's $M$ and $r_C$ for the interior flow. At $\lambda=1$ the flows $\pm1$ reveal the class under full orders (EGJ's remark, Q2 memo R1).
- **Second knob, $\theta=1/10$.** $\lambda\in[0.42,0.86]$. Below $0.42$ the buying rate reaches its cap before $1.65$, and entry on the branch stops rising. Below $0.55$ the outcome at $r_1$ is T rather than $(1,-v)$. Above $0.86$, $r_1$ has several equilibria. On the coexistence branch $\lambda$ only caps the buying rate (Result 13d).

## 4. Scorecard (BRIEF §2)

### 4.1 EGJ's own block: two-sided menu, equal weights $\theta=1/3$, presence $\lambda$

| # | Item | Verdict | Status |
|---|---|---|---|
| 1 | Prop. 2(i) at $r_0=1.2$ | Holds: NT unique, entry $\rho$, every $\lambda$; belief-free and tie-free ($\Delta_T(r_0)<k$) | analytical |
| 2 | Prop. 2(ii) at $r_1=3$ | Holds: T unique for every $\lambda$; entry $\tfrac14+\tfrac\lambda8$ ($\lambda<82/141$) or $\tfrac12$ ($\lambda\ge82/141$); $\mathsf O_H=\tfrac18+\tfrac\lambda8$ or $\tfrac14+\tfrac\lambda8$ ($3/8$ at $\lambda=1$); paper $0.523$, $0.324$ | analytical |
| 3 | Prop. 2(iii) at $r_2=3.6$ | **Fails** for every $\lambda$ (and every $\theta$, every $k<0.0315$; at equal weights every $k$ with trade at $r_1$). Weaker statement: for $\lambda\in[0.582,0.633)$ entry falls from $\tfrac12$ to $\tfrac14+\tfrac\lambda8\approx0.325$ while trade stays full; return to $\rho$ only above $r_C(1)=7.969$ | analytical |
| 4 | Prop. 3 | **Fails**: coexistence only on the knife-edge $r=1.9732$ under rule M; NT is unique at $1.55$–$1.65$ | analytical |
| 5 | Prop. A.9 at $r_1$ | Holds: same full orders with hidden prices; $\Delta\mathcal R_T=(19+8\lambda)/96$, $\Delta\mathcal W>0$ ($9/32$, $61/96$ at $\lambda=1$) | analytical |
| 6 | Off-path beliefs | Needed only for NT near its boundary ($r\in(1.7479,1.9732]$) and for BNS/SNB in the band. Passive beliefs: no equilibrium on $\kappa\in(1,3/2)$ | analytical |
| 7 | Ties and mixing | No tie at the benchmark strengths. In the band, rule M adds mixed equilibria, rule X adds challenger mixing at $X=1$; rule Z with passive beliefs leaves the band empty | analytical |
| 8 | Knob $\lambda$ | Range $(0,1]$ for (i)–(ii); $[0.582,1]$ for entry $1/2$; $[0.582,0.633)$ for a partial fall; meaning: presence or a liquidity shock (identical here) | analytical |
| 9 | Precedent | EGJ (2015) item by item (Q2 memo R1–R2, Tables 2.1–2.2; `L1_survey.md` C01) | literature fact |
| 10 | Labels | as listed | — |

### 4.2 Second knob: $\theta=1/10$, $\lambda=7/10$ (working ranges $\lambda\in[0.42,0.86]$ at $\theta=1/10$; $\theta\in[0.01,0.14]$ at $\lambda=7/10$)

| # | Item | Verdict | Status |
|---|---|---|---|
| 1 | Prop. 2(i) | Holds: NT unique, belief-free, tie-free | analytical |
| 2 | Prop. 2(ii) | Holds under rule M: unique full buy with partial sale ($v=0.2916$), the paper's pattern; entry $0.527345$ (paper $0.522757$), $\mathsf O_H=0.3725$. **Under rule Z there is no equilibrium at $r_1$** | computer-assisted |
| 3 | Prop. 2(iii) | **Fails**: unique T with entry $0.50875$ at $3.6$ | analytical (Result 6); computer-assisted value |
| 4 | Prop. 3 | Holds under rule M (either challenger rule, either belief rule): NT coexists with informative equilibria on $[1.4386,1.8]$; the pure-entry partial-buy branch has strictly rising entry $0.4193<0.4503<0.4843$ at $1.55,1.60,1.65$; a second (challenger-mixing) branch falls. Under rule Z: NT only | analytical (monotonicity, Result 13); computer-assisted (existence, ordering) |
| 5 | Prop. A.9 | Holds: $\Delta\mathcal R_T=0.292116$, $\Delta\mathcal W=0.456211$ against every hidden-price equilibrium | computer-assisted |
| 6 | Off-path beliefs | NT needs the IC belief only on $(1.7479,1.8]$; the branch leaves $X=-2$ unused but survives passive beliefs; the $r_1$ and $r_2$ equilibria use every flow | computer-assisted |
| 7 | Ties and mixing | Investor mixing (rule M) is essential at $r_1$ and on the upward branch; challenger mixing only adds the falling branch | computer-assisted |
| 8 | Knobs | $\lambda$: presence or liquidity shock; $\theta$: noise-trading intensity ($2\theta$ is the chance that noise trades). Ranges above (grid) | computer-assisted at grid points |
| 9 | Precedent | Menu, presence, cost and pricing: EGJ (verified). Unequal noise weights: **no verified precedent** (Q2 memo; `L1_survey.md` §5.6). Mixed informed strategies: GG (2008) (verified record) | literature fact / unverified device |
| 10 | Labels | as listed | — |

**Against the bar.** The two-sided discrete-Laplace companion (`C1_two_sided.md`) reproduces Prop. 2(i)–(iii) exactly, with entry $0.569$ and flat entry on its coexistence interval $[1.516,1.748]$. The second-knob candidate reproduces Prop. 2(i)–(ii), Prop. 3 with upward entry at $1.55$–$1.65$, and Prop. A.9, with entry closer to the paper ($0.527$). It loses Prop. 2(iii) and needs investor mixing. EGJ's own block (4.1) loses both Prop. 2(iii) and Prop. 3.

## 5. Numerical example

All values are exact unless shown as decimals of a certified enclosure. Benchmark: $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_L=0$, $c_H=6$, $k=1/50$, $\pi=1/2$.

**EGJ's own block, $\lambda=3/5$** (inside the window of a partial fall; `t1_equal_weights.out.txt`, Section C):

| $r$ | Equilibrium | Entry by flow $x=-2,\dots,2$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | $\mathcal W$ |
|---|---|---|---|---|---|---|
| $6/5$ | NT | $(\cdot,\tfrac14,\tfrac14,\tfrac14,\cdot)$ | $1/4$ | $1/8$ | $377/960$ | $1679/960$ |
| $3$ | T | $(\tfrac14,\tfrac14,\tfrac14,1,1)$ | $1/2$ | $13/40$ | $69/80$ | $133/48$ |
| $18/5$ | T | $(\tfrac14,\tfrac14,\tfrac14,\tfrac14,1)$ | $13/40$ | $1/5$ | $22163/28800$ | $85937/28800$ |

At $r=3$ the posteriors are $(0,2/7,1/2,5/7,1)$; $5/7\ge\tau=141/200$, so the flow $+1$ recruits. At $18/5$, $5/7<\tau=0.7314$. The strength path is:

- NT up to $1.973212$;
- the band (BNS and mixed profiles; SNB fails because $\lambda<6/7$) up to $2.144628$;
- T with entry $1/2$ up to $r_C(5/7)=3.215549$;
- T with entry $13/40$ up to $7.968627$;
- T with entry $1/4$ above.

**Second-knob candidate, $\theta=1/10$, $\lambda=7/10$** (Result 15):

| $r$ | Equilibrium | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | $\mathcal W$ |
|---|---|---|---|---|---|
| $6/5$ | NT | $0.250000$ | $0.125000$ | $0.392708$ | $1.748958$ |
| $1.55$ | partial buy, $a=0.314319$ (coexists with NT) | $0.419296$ | $0.256796$ | $0.539602$ | $2.133754$ |
| $1.60$ | partial buy, $a=0.417656$ (coexists with NT) | $0.450297$ | $0.287797$ | $0.566096$ | $2.253785$ |
| $1.65$ | partial buy, $a=0.531020$ (coexists with NT) | $0.484306$ | $0.321806$ | $0.595149$ | $2.381908$ |
| $3$ | full buy, partial sale, $v=0.291625$ | $0.527345$ | $0.372500$ | $0.906700$ | $3.008294$ |
| $18/5$ | T | $0.508750$ | $0.372500$ | $1.017002$ | $3.303866$ |

**Scripts** (folder `scripts/T1_egj_two_sided/`, all print-only, no assertions; run from the repository root):

| File | Content | Time |
|---|---|---|
| `t1_core.py` | exact auction objects (checked by integration), flow laws, posteriors, payoffs, outcomes, rational interval arithmetic | module |
| `t1_equal_weights.py` → `.out.txt` | Part A: every closed form at rational points; band equilibria; ceilings; the Result 6 bounds; Prop. A.9; passive beliefs | < 1 s |
| `t1_solver.py` | exhaustive exact enumeration for $\theta\ne1/3$ | module |
| `t1_crosscheck.py` → `.out.txt` | independent brute-force check at 10 points | 2 min (slot) |
| `t1_scan.py` → `scan_bench_*.csv`, `scan_interval_*.csv` | the $(\theta,\lambda,r)$ scans | 2 + 7 min (slots) |
| `t1_summarize.py` → `t1_summary.out.txt` | maps and summaries of the scans | 5 s |
| `t1_certificates.py` → `t1_certificates_theta1-10_lam7-10.out.txt` | the candidate: all equilibria, independent re-verification, ordering, Prop. A.9 | 1 s |
| `t1_refine.py` → `t1_refine.out.txt` | working ranges on $1/100$ grids; branch endpoints; trading costs | 2 min (slot) |
| `dev/probe_solver.py`, `dev/probe2.py` | development probes used before the scans | seconds |
| `dev/check_claims.py` | checks three statements of Result 14 against the scan | seconds |

## 6. Open issues

1. **Completeness of the enumeration (computer-assisted, not analytical).** The enumeration is exhaustive by construction, and two checks support it (Result 14). A third check by another member would raise confidence. The θ-maps hold at grid points only.
2. **Exact boundaries of the working ranges.** The ranges $\lambda\in[0.42,0.86]$ and $\theta\in[0.01,0.14]$ come from $1/100$ grids. Their exact endpoints are not derived.
3. **A second partial-buy branch.** For $\theta\ge0.20$ the interval scan finds a low-entry partial-buy branch near $r\approx1.9$–$2.0$, after NT has ended. It does not affect Prop. 3. It is not analysed.
4. **Prior $\pi\ne1/2$, value classes, atomless costs, private signals** (paper Sections 5.1–5.3) are not studied for this block.
5. **Reading (iii) of $\lambda$** (informed only with probability $\lambda$) belongs to T2.
6. **Existence under rule Z.** In the $(1,-v)$ band no pure equilibrium exists at $r_1$. A modified pure-strategy concept, for example a finer order menu, might restore existence; this is open.
7. **Prop. 2(iii)** has no fix inside this family at the paper's $(h,c_H)$ (Results 6 and 8).

## 7. Plain summary

EGJ's trading block can be put into the paper almost unchanged. The investor buys, sells or waits. Noise traders buy, sell or wait with equal chances. The investor is present with probability $\lambda$.

The weak-incumbent result survives at every $\lambda$, and so does the strong-incumbent result: full two-sided trade is the unique outcome, and entry rises to $0.5$ once $\lambda$ exceeds $0.58$ (paper $0.523$). With $\lambda$ below one, the flow $+1$ hides the investor and still attracts the expensive challenger.

Entry never returns to the floor at $r_2=3.6$. The extreme flow $+2$ reveals the high class, and the expensive challenger still covers its cost there until $r=7.97$. No choice of $\lambda$, noise weights or trading cost repairs this. A weaker statement holds: for $\lambda$ between $0.58$ and $0.63$, entry falls from $0.5$ to about $0.33$. At $\lambda=1-e^{-2/b}$ the drop occurs exactly at the paper's ceiling, $3.593$. A full return needs $r_2$ above $7.97$ or $c_H$ above $8.17$.

With equal noise weights, no trade and informative trade coexist only at one strength. Each trader's profit depends only on the other side's trading, and the seller never benefits from recruited entry.

A second knob changes this. With noise that trades less often ($\theta=0.1$) and $\lambda=0.7$:

- no trade coexists with an informative equilibrium on $[1.44,1.80]$;
- on one branch the buying probability, and with it entry, rises with strength ($0.419<0.450<0.484$ at $1.55,1.60,1.65$);
- at $r_1$ the unique outcome is the paper's full purchase with partial sale, with entry $0.527$;
- access to prices raises proceeds and net surplus.

The costs are three:

- both results need mixed strategies; under EGJ's pure-strategy tie rule the strong economy has no equilibrium;
- unequal noise weights have no precedent in the verified literature;
- the return to the floor still fails.
