# C8. The seller sets the reserve after it observes the price

## 1. Question

The seller sees the price before it sets the reserve.
The seller then holds the market posterior $\mu$ about the challenger class.
The seller chooses a reserve $p(\mu)$ for that posterior.
This memo asks five questions.

- What reserve does the seller choose at each $\mu$ and $r$?
- Does the reserve exploit good news and deter entry?
- Does the investor change its trading in response?
- What is the value of a committed reserve?
- Does a Proposition 2 analog survive?

The main timing sets the reserve before preparation.
Section 3.6 states the change when the reserve follows preparation.
The paper source is the pinned commit in the team rules.
Paper Section 6.3 and Appendix A.7 give the fixed-reserve objects.

## 2. Setup

### 2.1 Base model

The base model is the discrete-Laplace model.
Noise $Z$ has $P(Z=z)=\frac{1-a}{1+a}a^{|z|}$ for integer $z$.
Here $a=e^{-1/b}$ and $b=2$.
Orders are buy-only, $q\in\{0,1\}$.
The investor sees the class $j\in\{H,L\}$ and buys with probability $\beta_j$.
The prior is $\pi=1/2$ and the presence probability is $\lambda=1$.
Preparation costs are $c_L=0$ and $c_H$, with low cost at probability $\rho$.
Benchmark values are $h=10$, $\ell=1$, $\rho=0.25$, $k=0.02$.
The benchmark strengths are $r_0=1.2$, $r_1=3$, and $r_2=3.6$.
The benchmark uses $c_H=5$, as in the team candidate.

Two facts make this base the right one here.
First, every integer flow has positive probability.
No off-path flow belief is then necessary.
Second, posteriors stay inside $(0,1)$.
The seller thus faces real uncertainty at each price.
The three-point base reveals the class at the top flow.
That base would let the seller extract the full class value there.
It would hide the partial hold-up that this memo studies.

Section 3.1 derives the two posteriors for this base.
It does not take the candidate values on trust.

### 2.2 Timing

The main timing has six steps.

1. The investor sees the class and chooses $q$.
2. Flow $X=q+Z$ realizes.
3. The seller observes the price information in $X$.
4. The seller sets the reserve $p$.
5. The challenger sees the price, the reserve, and its cost.
6. The challenger prepares or stays out, and the auction runs.

Step 3 needs one precision.
The share price depends on the reserve rule.
The seller therefore cannot see a final price before the rule exists.
This memo reads "sees the price" as "sees the posterior $\mu_X$".
The flow determines $\mu_X$ under the candidate orders.
An interim quote at any reference reserve reveals the same $\mu_X$.
The final price then adjusts to the reserve that the seller sets.
Market makers set $P(X)=E[V_T\mid X]$ with that adjustment in view.
Proposition C8.2 shows that the final price reveals $\mu_X$.
The seller can thus invert the final price in equilibrium.
Both readings then give the same game.

The seller wants large expected proceeds.
At step 4 the seller takes $\mu$ as given.
The seller cannot change the past flow.
The seller foresees the entry response to the reserve.

### 2.3 Auction objects at a general reserve

The incumbent value is $R\sim U[0,r]$.
The reserve ranges over $p\in[0,h]$.
Paper Appendix A.7 gives three regimes.
This memo uses them with $t_j$ for proceeds and $g_j$ for challenger profit.

Regime I, $0\le p\le\ell$:
$t_0=p(1-p/r)$, $t_H=r/2+p^2/(2r)$,
$t_L=\ell-(\ell^2-p^2)/(2r)$,
$g_H=h-r/2-p^2/(2r)$, $g_L=(\ell^2-p^2)/(2r)$.

Regime II, $\ell<p\le r$:
$t_0=p(1-p/r)$, $t_H=r/2+p^2/(2r)$, $t_L=t_0$,
$g_H=h-t_H$, $g_L=0$.

Regime III, $r<p\le h$:
$t_0=t_L=g_L=0$, $t_H=p$, $g_H=h-p$.

Write $\Delta_T(p)=t_H-t_L$ and $B(p,\mu)=g_L+\mu(g_H-g_L)$.
Write $e(p,\mu)=\rho\mathbf 1\{B\ge 0\}+(1-\rho)\mathbf 1\{B\ge c_H\}$.
A bid at the reserve is admissible.
At $p=\ell$ the low challenger can still bid.
Just above $\ell$ it cannot bid, and $t_L$ jumps down to $t_0$.
At $p=r$ the regime formulas agree.

Conditional expected proceeds at posterior $\mu$ are

$$S(p;\mu,r)=t_0(p)+e(p,\mu)\big[t_L(p)-t_0(p)+\mu\Delta_T(p)\big].$$

The seller value is $V(\mu)=\max_{p\in[0,h]}S(p;\mu,r)$.
A maximizer is $p^*(\mu)$.
Result C8.1 shows that a maximizer exists.

### 2.4 Equilibrium concept and tie rules

An equilibrium has five parts.

- Investor orders $\beta_H,\beta_L\in[0,1]$.
- Flow posteriors $\mu_X$ from Bayes and the orders.
- A seller rule $p^*(\mu)$ that is optimal at each $\mu$.
- A competitive price $P(X)=S(p^*(\mu_X);\mu_X,r)$.
- Optimal preparation at each price, reserve, and cost.

A unilateral investor deviation faces fixed price and reserve schedules.
A seller deviation faces a fixed posterior and a responsive challenger.
Every flow has positive probability, so no flow is off path.

Three tie rules apply.

- The challenger prepares at indifference, at both costs.
- The investor does not trade at indifference.
- The seller takes the smallest optimal reserve.

The second rule is a selection at one point.
The memo also states the standard correspondence at equality.

## 3. Results

### 3.1 Posteriors under buy-only orders

**Lemma C8.0 (analytical).**
Take $\beta_L=0$ and $\beta_H=\beta$.
The posterior $\mu_X$ takes exactly two values.
For $X\ge 1$ it is $\mu_G(\beta)$.
For $X\le 0$ it is $\mu_B(\beta)$.
At $\beta=1$, $\mu_G=M_1=1/(1+a)$ and $\mu_B=m_1=a/(1+a)$.
At $b=2$, $M_1=0.622459$ and $m_1=0.377541$.
Under full buying, good news has unconditional probability $1/2$.

*Derivation.*
The likelihood ratio at flow $x$ is
$[(1-\beta)P_Z(x)+\beta P_Z(x-1)]/P_Z(x)$.
The ratio $P_Z(x-1)/P_Z(x)$ equals $a^{-1}$ for $x\ge1$.
It equals $a$ for $x\le0$.
Bayes with prior $1/2$ then gives two posterior values.
At $\beta=1$ the ratios are $a^{-1}$ and $a$, which give $M_1,m_1$.
Also $P(Z\ge0)=1/(1+a)=M_1$ and $P(Z\ge1)=a/(1+a)=m_1$.
Good news thus has probability $(M_1+m_1)/2=1/2$.
Good news has probability $M_1$ in state $H$ under a purchase.
Good news has probability $m_1$ in state $L$. $\square$

This check confirms the candidate posterior values in the brief.
It uses buy-only orders and $\lambda=1$.

### 3.2 The seller best response

**Proposition C8.1 (analytical).**
Fix $r\in(\ell,h)$ and $\mu\in(0,1)$.

(i) $B(p,\mu)$ falls strictly in $p$ on $(0,h]$.
The set $\{p:B(p,\mu)\ge c_H\}$ is $[0,\bar p(\mu)]$ or empty.
The cap $\bar p(\mu)$ rises weakly in $\mu$ where it exists.
Entry is $1$ on $[0,\bar p(\mu)]$ and $\rho$ above it.

(ii) $S(\cdot;\mu,r)$ attains its maximum on $[0,h]$.
A finite candidate list contains every maximizer.
The list has the points $0,\ell,r,h,\bar p(\mu)$.
It also has at most two interior points, stated below.

(iii) On the entry branch $e=1$, proceeds rise in $p$ in Regime I.
They also rise in Regime III, where $S=\mu p$.
On the floor branch $e=\rho$, proceeds rise in $p$ in Regime III.
There $S=\rho\mu p$, so the branch value at $p=h$ is $\rho\mu h$.

(iv) Define $e^*(\mu)=e(p^*(\mu),\mu)$ and $\Delta^*(\mu)=\Delta_T(p^*(\mu))$.
The price $P=V(\mu)$ rises strictly in $\mu$.
The challenger thus recovers $\mu$ from the price and the reserve.

*Derivation.*
Part (i) uses $dB/dp$ in each regime.
Regime I gives $dg_H/dp=dg_L/dp=-p/r$, so $dB/dp=-p/r$.
Regime II gives $B=\mu(h-r/2-p^2/(2r))$, so $dB/dp=-\mu p/r$.
Regime III gives $B=\mu(h-p)$, so $dB/dp=-\mu$.
Each value is negative for $p>0$, and $B$ is continuous in $p$.
The set $\{B\ge c_H\}$ is then an interval from zero.
A larger $\mu$ raises $B$ at each $p$, since $g_H\ge g_L$.
The cap $\bar p$ thus rises weakly in $\mu$.
Also $B\ge0$ on $[0,h]$, so the low-cost type always prepares.
Entry is then $1$ below the cap and $\rho$ above it.

Part (ii) first shows that a maximum exists.
The function $S$ can jump only at $p=\ell$ and at $p=\bar p$.
At $\ell$ the value uses Regime I, and the right limit is smaller.
At $\bar p$ the value uses $e=1$ by the challenger tie rule.
The right limit uses $e=\rho$.
The gap is $(1-\rho)[t_L-t_0+\mu\Delta_T]\ge0$.
So $S$ is upper semicontinuous on a compact set.
A maximum exists.

For the candidate list, fix a regime and an entry branch.
Proceeds are then quadratic or linear in $p$.
In Regime I, $S_e'(p)=(1-e)+(p/r)(3e-2)$.
At $e=1$ this is $p/r>0$, so only endpoints can be optimal.
At $e=\rho$ the interior point is $r(1-\rho)/(2-3\rho)$ when $\rho<2/3$.
When $\rho\ge2/3$ the branch is convex or linear, so endpoints suffice.
In Regime II, $S_e'(p)=(1-e\mu)+(p/r)(3e\mu-2)$.
When $e\mu<2/3$ the interior point is $r(1-e\mu)/(2-3e\mu)$.
When $e\mu\ge2/3$ the branch is convex or linear, so endpoints suffice.
The benchmark has $\rho=1/4$ and $\mu\le M_1<2/3$ on path.
In Regime III, $S_e=e\mu p$, which rises in $p$.
Endpoints, regime bounds, and these points exhaust the maxima.
A candidate counts only on its own regime and entry branch.

Part (iii) restates the Regime I and III derivatives.

Part (iv) fixes $p$ and varies $\mu$.
Between entry jumps, $\partial S/\partial\mu=e\Delta_T(p)$.
Now $\Delta_T(p)>0$ in all regimes.
In Regime I it is $(r-\ell)^2/(2r)$.
In Regime II it is $r/2-p+3p^2/(2r)$, with minimum $r/3$ at $p=r/3$.
In Regime III it is $p>r>0$.
Entry jumps up in $\mu$, and the jump term is nonnegative.
So each $S(p;\cdot)$ rises strictly.
For $\mu'>\mu$, $V(\mu')\ge S(p^*(\mu);\mu')>S(p^*(\mu);\mu)=V(\mu)$.
The price thus reveals $\mu$. $\square$

Three lessons follow from Proposition C8.1.

- Good news raises the cap $\bar p$ that entry can bear.
- The seller still may not use that cap.
- The floor branch always offers the value $\rho\mu h$ at $p=h$.

The last point drives the benchmark result.
At $p=h$ the incumbent and the low challenger cannot bid.
A prepared high challenger pays $h$ and earns zero.
The low-cost type prepares only by $c_L=0$ and its tie rule.
Section 6 returns to this fragility.

**Corollary C8.1a (computer-assisted).**
At $c_H=5$ and $r\in\{1.2,\,3\}$, $p^*(\mu)=h$ for $\mu\in[m_1,M_1]$.
Entry is then $\rho$ and the spread is $h$ at every such price.
At $r=3$ and $\mu=M_1$, $\bar p=1.674539$.
Accommodation at $\bar p$ gives $1.503915$.
Exclusion at $h$ gives $\rho M_1 h=1.556148$.
The gap is $0.052233$.
At $r=3$ and $\mu=m_1$, the best incumbent reserve gives $0.858129$.
Exclusion gives $0.943852$, a gap of $0.085723$.

*Computation.*
Two routes give the same maximizer.
Route G searches a reserve grid with step $0.005$.
Route C values the finite candidate list of Proposition C8.1.
Only feasible candidates count in route C.
Both routes use 50-digit arithmetic.
The script also checks $25$ posterior points in $[m_1,M_1]$.
Each point has its grid maximizer at the top grid point $h$.
On each regime $|\partial S/\partial p|\le 3$ at these values.
A step of $0.005$ thus misses at most $0.0075$ between kinks.
Route C values every kink exactly.
The gaps above exceed the grid error by a factor of seven.
Exact fractions check the fixed-reserve objects at $p=1/2$.
For example, at $r=3$, $(t_0,t_H,t_L,g_H,g_L)=(5/12,37/24,7/8,203/24,1/8)$. $\square$

The seller does not always exclude.
At large $r$ the incumbent alone yields up to $r/4$ at $p=r/2$.
Exclusion yields only $\rho\mu h\le1.556$ at the posteriors here.
The script finds interior Regime II optima at $r\ge5$ for most $\mu$.
At $r=7$, $p^*$ is $3.692,3.769,3.855$ at $m_1,1/2,M_1$.
At $r=9$, $p^*$ is $4.747,4.846,4.957$ at the same posteriors.
There the reserve rises with good news, but entry stays at $\rho$.
Expensive entry is not feasible at any reserve at those strengths.

One case breaks reserve monotonicity in $\mu$.
At $r=3.6$, $p^*(m_1)=1.899$ and $p^*(1/2)=h$.
But $p^*(M_1)=\ell=1$, with value $1.584420$ against $1.556148$ at $h$.
Good news there makes the seller cut the reserve.
The cut buys expensive entry, since $B(\ell,M_1)=5.018\ge5$ at $r=3.6$.
Section 5 gives the $r=3.6$ numbers in full.
The general pattern has two forces.

- Within the floor branch, a larger $\mu$ raises the optimal reserve.
- At the top posterior, accommodation can require a reserve cut.

The first force is in the Regime II formula of Proposition C8.1.
The point $r(1-\rho\mu)/(2-3\rho\mu)$ rises in $\mu$.
The second force appears only when $\bar p(\mu)$ exists.
It also needs incumbent revenue large enough to beat $\rho\mu h$.

### 3.3 Trading with an anticipated reserve rule

**Proposition C8.2 (analytical).**
In every equilibrium $\beta_L=0$.
Write $\beta=\beta_H$ and let $\mu_G,\mu_B$ be as in Lemma C8.0.
Write $e_s^*,\Delta_s^*$ for the seller objects at $\mu_s$, $s\in\{G,B\}$.
The gross profit of a purchase in state $H$ is

$$K(\beta)=M_1 e_G^*\Delta_G^*(1-\mu_G)+m_1 e_B^*\Delta_B^*(1-\mu_B).$$

With the investor tie rule, the equilibrium orders are as follows.
No trade holds exactly when $K(0)\le k$.
Full buying holds exactly when $K(1)>k$.
An interior $\beta$ is never selected.
In the standard correspondence, interior orders require $K(\beta)=k$.
There full buying requires only $K(1)\ge k$.

*Derivation.*
Fix a flow $x$ with posterior $\mu$, reserve $p^*(\mu)$, entry $e^*$.
Type values and the price are
$E[V_T\mid H,x]=t_0+e^*(t_H-t_0)$,
$E[V_T\mid L,x]=t_0+e^*(t_L-t_0)$, and
$P=t_0+e^*[t_L-t_0+\mu\Delta^*]$.
Subtraction gives the two residual advantages.

- In state $H$: $e^*\Delta^*(1-\mu)\ge0$.
- In state $L$: $-e^*\Delta^*\mu\le0$.

A purchase in state $L$ thus earns at most $-k$.
Zero earns zero, so $\beta_L=0$ in every equilibrium.
This step holds for every reserve rule.

A purchase in state $H$ reaches good news with probability $M_1$.
It reaches bad news with probability $m_1$, by Lemma C8.0.
Its gross profit is the stated weighted sum of residuals.
Net profit is $K(\beta)-k$.
The investor has two actions, so the stated comparisons are exact.
The candidate $\beta$ enters only via $\mu_G,\mu_B$ and the seller rule.
A deviation does not change those schedules. $\square$

Two useful bounds follow at once.
Since $1-\mu_G\ge m_1$ and $1-\mu_B\ge1/2$, and $e^*\ge\rho$,

$$K(\beta)\ge\rho\,\underline\Delta^*\,(M_1m_1+m_1/2),$$

where $\underline\Delta^*$ is the smallest seller spread on $[m_1,M_1]$.
Also $K(\beta)\le\bar\Delta^*$, the largest seller spread there.
The weights sum to one, $e^*\le1$, and $1-\mu\le1$.

**Corollary C8.2a (analytical, given Corollary C8.1a).**
At $r\in\{1.2,3\}$ and $c_H=5$, full buying is the unique outcome.
No trade is not an equilibrium.
Entry equals $\rho$ and ownership $O_H$ equals $\rho/2$ in both economies.
Expected proceeds equal $\rho h/2=1.25$ in both economies.

*Derivation.*
Corollary C8.1a gives $p^*=h$, $e^*=\rho$, $\Delta^*=h$ on $[m_1,M_1]$.
Every candidate posterior pair lies in that interval.
So $K(\beta)\ge\rho h(M_1m_1+m_1/2)$ for every $\beta$.
The values $M_1m_1=0.235004$ and $m_1=0.377541$ give $K(\beta)\ge1.059$.
This exceeds $k=0.02$ by a wide margin.
In particular $K(0)=\rho h/2=1.25>k$, so no trade fails.
And $K(1)=2\rho h M_1m_1=1.175019>k$, so full buying holds.
No $\beta$ has $K(\beta)=k$, so no interior order is an equilibrium.
Entry is $\rho$ since $B(h,\mu)=0<c_H$.
Ownership is $P(H,\text{entry})=\rho/2$, since a prepared $H$ wins.
Proceeds are $(V(M_1)+V(m_1))/2=\rho h/2$. $\square$

The investor response has a clear sign here.
The contingent reserve raises trading profit.
At $r_1$ with fixed $p=0.5$, $K(1)=0.195836$.
With the contingent reserve, $K(1)=1.175019$.
Exclusion widens the spread from $2/3$ to $10$.
Entry feedback no longer supports trading.
Reserve feedback supports trading instead.
Good and bad prices both lead to $\Delta^*=h$ at $r_0,r_1$.
The price stays informative, because $P=\rho\mu h$ rises in $\mu$.
But no price in $[m_1,M_1]$ recruits expensive entry.

At $r=5$ the reserve feedback is visible in $K$ itself.
The script gives $K(0)=0.247604$ and $K(1)=0.702125$.
Stronger candidate buying moves $\mu_G$ to a point with $p^*=h$.
The spread jump then raises the return to buying.
This raising can in principle support coexistence at larger $k$.
Section 6 states that point as an open issue, with its exact need.

### 3.4 Commitment against a price-contingent reserve

A committed reserve is one number $p^c$ for all posteriors.
The seller chooses it before trading.
Trading and entry then follow the fixed-reserve model at $p^c$.
This section uses one selection for fair comparison.
It takes full buying when $K(1)>k$ at that reserve.
It takes no trade when $K(1)\le k$ and $K(0)\le k$.

**Proposition C8.3 (analytical).**
Fix the orders and thus the posterior law.
The contingent rule yields weakly more proceeds than any $p^c$.
The gain at posterior $\mu$ is $V(\mu)-S(p^c;\mu,r)\ge0$.
A committed reserve can still yield strictly more entry.
Take $p^c\le\bar p(M_1)<p^*(M_1)$.
Take also expensive entry off at $m_1$ under $p^c$.
Entry under full buying is then $(1+\rho)/2$ against $\rho$.

*Derivation.*
The first claim is the definition of $V$ as a maximum.
A constant rule is one feasible contingent rule.
The second claim uses Proposition C8.1(i).
Expensive entry at $M_1$ holds exactly for $p\le\bar p(M_1)$.
It fails at $m_1$ when $\bar p(m_1)$ does not exist or $p^c$ exceeds it.
Full buying then gives entry $(1+\rho)/2$, by Lemma C8.0.
The contingent rule with $p^*(M_1)>\bar p(M_1)$ gives $\rho$. $\square$

Proposition C8.3 holds orders fixed.
Equilibrium orders can change with $p^c$, so scan them as well.
The script scans $p^c$ on a $0.25$ grid with the selection above.

- At $r=1.2$ and $r=3$, the best committed reserve is $p^c=10$.
- Its proceeds are $1.25$ and its entry is $\rho$.
- At $r=9$, the best grid point is $p^c=4.75$, with proceeds $2.681858$.
- The contingent proceeds at $r=9$ are $2.683678$.

The seller value of commitment is thus zero or negative here.
It is $0$ at $r_0,r_1$ and about $-0.0018$ at $r=9$ on the grid.
The contingent rule is constant at $r_0,r_1$, so commitment copies it.
Commitment does not help a seller who wants only proceeds.

Commitment to the paper reserve $p^c=0.5$ tells a different story.
At $r_1$ it yields proceeds $0.942073$ against $1.25$.
It yields entry $0.625$ against $0.25$.
It yields ownership $0.358422$ against $0.125$.
The value of that commitment is in entry, not in proceeds.
A seller who valued entry could strictly prefer to commit low.
The memo keeps seller payoffs as proceeds, as in paper Appendix A.7.

### 3.5 A Proposition 2 analog, and its benchmark failure

**Proposition C8.4 (analytical).**
Fix $\ell<r_0<r_1<h$ and the seller objects $p^*,e^*,\Delta^*$.
Suppose the conditions below hold.

- (C8-A1) At $r_0$, $B(p^*(1/2),1/2)<c_H$.
- (C8-A1) At $r_1$, $B(p^*(M_1),M_1)\ge c_H>B(p^*(m_1),m_1)$, as one entry condition.
- (C8-A2) At $r_0$, $k>\bar\Delta^*(r_0)$.
- (C8-A3) At $r_1$, $k<\rho\,\underline\Delta^*(r_1)(M_1m_1+m_1/2)$.

Then three conclusions hold.

(i) At $r_0$ the unique outcome is no trade with entry $\rho$.

(ii) At $r_1$ the unique outcome is full buying.
Entry is $(1+\rho)/2>\rho$.
Ownership exceeds the $r_0$ level $\rho/2$.

(iii) Take $r_2>r_1$ with $B(p^*(M_1),M_1)<c_H$ at $r_2$.
Assume (C8-A3) also holds at $r_2$.
Then full buying is unique at $r_2$ and entry returns to $\rho$.

*Derivation.*
At $r_0$, (C8-A2) and $K(\beta)\le\bar\Delta^*$ give $K(\beta)<k$.
Proposition C8.2 then gives unique no trade.
The posterior stays at $1/2$, and (C8-A1) gives entry $\rho$.
At $r_1$, (C8-A3) and the lower bound give $K(\beta)>k$ for all $\beta$.
Proposition C8.2 then gives unique full buying.
Good news has probability $1/2$ and recruits expensive entry.
Bad news does not recruit it.
Entry is thus $(1+\rho)/2$.
Ownership is $\tfrac12[M_1\cdot1+m_1\rho]$, which exceeds $\rho/2$.
Part (iii) repeats the $r_1$ trading step at $r_2$.
No posterior now recruits expensive entry, so entry is $\rho$. $\square$

**Benchmark failure (computer-assisted).**
Proposition C8.4 does not apply at $(r_0,r_1)=(1.2,3)$, $c_H=5$.
Condition (C8-A1) fails at $r_1$, since $B(h,M_1)=0<5$.
Condition (C8-A2) fails at $r_0$, since $\bar\Delta^*=10>k$.
Both economies instead have full buying with entry $\rho$.
This is Corollary C8.2a.
So competition does not create entry at the benchmark pair.
A stronger incumbent also does not create trading there.
Trading is already full at the weak incumbent.

The conditions show what an open survival region would need.
The seller must accommodate at $(r_1,M_1)$, so $p^*(M_1)\le\bar p(M_1)$.
The seller spreads at $r_0$ must stay below $k$ in the $K$ bound.
Exclusion must thus be unattractive at both strengths.
That points to small $\rho h$ against incumbent revenue.
It also points to small $c_H$, so $\bar p$ is large.
Section 6 leaves the construction of such a region open.
The benchmark has $\rho h=2.5$, which makes exclusion too attractive.

One intermediate case shows accommodation is not empty talk.
At $r=3.6$ the seller accommodates at $M_1$ with $p^*=1$.
Entry under full buying is then $0.625$, as with fixed $p=0.5$.
But at $r_0=1.2$ the seller still excludes and trading is full.
The $r_0$ to $r=3.6$ pair thus still fails part (i).
Accommodation at one strength does not restore the proposition.

### 3.6 If the reserve follows preparation

Two sub-cases matter.

First, preparation is not observable to the seller.
The seller then sets $p^*(\mu)$ on the posterior alone.
The challenger foresees that same reserve when it prepares.
Every outcome of the main timing carries over without change.
Only the calendar order of two moves changes.

Second, preparation is observable to the seller.
The seller sets one reserve after entry and one after no entry.
After no entry the seller faces only the incumbent.
Its best reserve is $r/2$, with proceeds $r/4$.
After entry the seller maximizes $\mu t_H(p)+(1-\mu)t_L(p)$.
At $r=3$ the script finds $p=h$ after entry at $m_1,1/2,M_1$.
The challenger gain at that reserve is $B=0$.
Expensive entry is zero, and floor entry stays by its tie rule.
Expected proceeds at $\mu$ are $\rho\mu h+(1-\rho)r/4$.
At $r=3$ and $M_1$ this is $1.556148+0.5625=2.118648$.
The main timing gives $1.556148$ at that posterior.
Observability thus raises seller proceeds in the no-entry state.
It does not restore expensive entry at the benchmark.

The investor residual is the same in this benchmark sub-case.
No entry gives a type-free payoff with mean $r/4$.
Entry gives $h$ in state $H$ and $0$ in state $L$.
The state spread is again $\rho h$.
Prices are $(1-\rho)r/4+\rho\mu h$ and trading stays full.

In general, observability weakly raises seller proceeds at fixed entry.
The seller can copy the main-timing reserve in both entry states.
Its effect on entry runs through the after-entry reserve alone.
That reserve ignores the entry margin, since entry is sunk.
Hold-up is therefore at least as stark in the after-entry branch.
The benchmark makes the point with $B=0$ after entry.

## 4. What it recovers or loses relative to the Laplace paper

Proposition 1 survives in a reserve-dependent form.
At fixed $p$, a stronger incumbent raises $\Delta_T$ and lowers $B$.
The reserve adds a third margin to that opposition.
In Regime I, $\Delta_T$ does not depend on $p$.
In Regime II it rises in $p$ for $p>r/3$, and in Regime III it is $p$.
In all regimes $B$ falls in $p$.
A higher reserve can thus widen the trading spread and cut entry gain.
A fixed reserve in Regime I cannot widen the spread.

Proposition 2 fails at the benchmark pair, as Section 3.5 shows.
Part (i) fails, since exclusion makes trading pay at $r_0$.
Part (ii) fails on entry, since no price recruits expensive entry.
Part (iii) has no content at the pair, since entry never left $\rho$.
The conditional analog is Proposition C8.4.
Its conditions name seller accommodation as the missing step.

Proposition 3 loses its entry-feedback source at the benchmark.
Entry does not respond to the price at $r_0,r_1$.
A new source appears in its place.
Candidate buying can move $\mu_G$ across a seller branch switch.
The spread $\Delta^*$ then jumps, and $K(\beta)$ can rise in $\beta$.
At $r=5$, $K$ rises from $0.247604$ at $\beta=0$ to $0.702125$ at $\beta=1$.
Coexistence at larger $k$ is a conjecture, not a result here.
Section 6 states the step that a proof would need.

The fixed-experiment control of Proposition A.3 needs care.
Fixed orders fix $\mu_G,\mu_B$ in this discrete model.
They do not fix the reserve, since $p^*(\mu)$ moves with $r$.
Entry at a fixed posterior can then rise or fall with $r$.
At $M_1$ it is $\rho$ at $r=3$ and $1$ at $r=3.6$ in the script.
The control holds only if the reserve rule is also held fixed.

Price sufficiency survives in the form of Proposition C8.1(iv).
The price $V(\mu)$ rises strictly, so the challenger recovers $\mu$.
The entry floor $\rho$ also survives at every reserve in $[0,h]$.
It survives because $B\ge0=c_L$ and the tie rule prepares.
No price pooling of the Appendix A.10 kind arises in this base.
Every flow has positive probability and entry never hits zero.
Distinct posteriors thus never need to share a price.

Paper Section 6.3 compares committed reserves $0.5$ and $1.1$.
The higher reserve there supports trading at a weak incumbent.
A contingent reserve pushes that force to its limit at the benchmark.
It supports trading at both strengths, with spread $h$.
It also cuts the sale margin that Section 6.3 tracks with care.
Preparation is $0.25$, sale is $0.125$, and two bidders have probability $0$.
At fixed $p=0.5$ and $r_1$, the three numbers are $0.625,0.9375,0.520833$.
Preparation alone would thus overstate competition under exclusion.
The seller problem of Appendix A.7 also changes form.
The choice is now a function $p^*(\mu)$, not one number $p$.
Its value $V(\mu)$ is the price itself.
Sections 5 and 6 of the paper on noise and welfare keep their logic.
Access to prices has no entry value at the benchmark pair here.
The price is informative, but entry does not respond to it.

## 5. Numerical example

Values are $h=10$, $\ell=1$, $\rho=0.25$, $b=2$, $k=0.02$, $c_H=5$.
Posteriors are $m_1=0.377541$ and $M_1=0.622459$.
The table uses equilibrium outcomes, not forced full buying.
"Cont." is the price-contingent reserve.
"Fixed" is the committed reserve $p^c=0.5$.

| $r$ | Rule | Orders | $p^*$ at $m_1,M_1$ | Proceeds | Entry | $O_H$ | Sale | Two bidders |
|---|---|---|---|---|---|---|---|---|
| 1.2 | Cont. | full buy | $10,10$ | 1.250000 | 0.250 | 0.125000 | 0.125 | 0.000 |
| 1.2 | Fixed | no trade | $0.5,0.5$ | 0.392708 | 0.250 | 0.125000 | 0.688 | 0.146 |
| 3.0 | Cont. | full buy | $10,10$ | 1.250000 | 0.250 | 0.125000 | 0.125 | 0.000 |
| 3.0 | Fixed | full buy | $0.5,0.5$ | 0.942073 | 0.625 | 0.358422 | 0.938 | 0.521 |
| 3.6 | Cont. | full buy | $1.899,1$ | 1.306395 | 0.625 | 0.358422 | 0.761 | 0.384 |
| 3.6 | Fixed | full buy | $0.5,0.5$ | 1.057873 | 0.625 | 0.358422 | 0.948 | 0.538 |
| 5.0 | Cont. | full buy | $2.637,10$ | 1.493181 | 0.250 | 0.125000 | 0.339 | 0.022 |
| 7.0 | Cont. | full buy | $3.692,3.855$ | 2.087305 | 0.250 | 0.125000 | 0.529 | 0.057 |
| 9.0 | Cont. | full buy | $4.747,4.957$ | 2.683678 | 0.250 | 0.125000 | 0.529 | 0.057 |

Trading profits explain the order column.
At $r=1.2$ with fixed $p$, $K(1)=0.004896<k$.
At $r=3$ with fixed $p$, $K(1)=0.195836>k$.
With the contingent reserve, $K(1)=1.175019$ at both strengths.
The minimum of $K(\beta)$ on a $0.02$ grid is $1.175019$ there.
Corollary C8.2a gives the analytic lower bound $1.059$ for all $\beta$.

At $r=3.6$ the grid seller values are $1.029755$ and $1.583035$.
The candidate list gives $V(M_1)=1.584420$ at exactly $p^*=\ell$.
The table uses grid values, so its proceeds differ by $0.0007$.
The second value uses accommodation at $p^*=\ell$.
Exclusion at $M_1$ would give $1.556148$.
Accommodation wins by $0.028272$ at that posterior.
Entry thus matches the fixed-reserve level at $r=3.6$.
Proceeds still exceed the fixed-reserve level.

At $c_H=6$ the benchmark conclusion does not change.
The script again finds $p^*=h$ at $r=3$ for $m_1$ and $M_1$.
At fixed $p=0.5$, $B(M_1)=5.312<6$, so entry stays at $\rho$ there too.
The $c_H=5$ case is the sharp one for the entry comparison.
It is the case where the fixed reserve recruits entry at $r_1$.

## 6. Open issues

- The exclusion reserve $p=h$ rests on $c_L=0$ and one tie rule.
  At $p=h$ the low-cost gain is exactly zero.
  Any $c_L>0$ gives zero entry at $p=h$ and zero proceeds there.
  The seller then keeps a reserve with $B(p,\mu)\ge c_L$.
  A full $c_L>0$ version is open.
  It should replace $h$ by an interior extraction reserve.

- Proposition C8.4 needs an open set of values.
  No such set is built here.
  A build needs $p^*(M_1)\le\bar p(M_1)$ at $r_1$ with strict gaps.
  It also needs small seller spreads at $r_0$.
  Small $\rho$, small $h/r$, and small $c_H$ point the right way.
  The status of that build is **open**.

- Coexistence via reserve feedback is a **conjecture**.
  At $r=5$, $K(0)<K(1)$ in the script.
  A proof needs the full shape of $K(\beta)$ on $[0,1]$.
  The seller rule jumps at branch switches, so $K$ can jump.
  Interior orders at a jump need a mixed seller or entry response.
  This memo does not settle that step.

- The seller objective is proceeds only.
  A seller who values entry or total surplus can prefer commitment.
  That trade-off is outside the stated objective.
  Welfare ranks are therefore not claimed here.

- The model uses point values $\ell,h$ and $\lambda=1$, $\pi=1/2$.
  Value bands as in paper Section 6.3 would smooth the jump at $\ell$.
  Presence $\lambda<1$ would move $\mu_G,\mu_B$ toward the prior.
  Both changes keep the seller problem of Proposition C8.1.
  Their benchmark outcomes are open.

- The seller sees only $\mu$, not the challenger cost or value.
  A reserve after bids would be a different sale rule.
  This memo does not study that rule.

## 7. Plain summary

Let the seller set the reserve after it learns the price signal.
At the benchmark values, the seller sets the highest reserve, $10$.
Only a prepared high challenger can then buy, at a price of $10$.
Expensive preparation never pays, so entry stays at $0.25$.
The price still carries news, and informed buying earns a large profit.
It earns more than with a fixed reserve, not less.
Trading is full at both a weak and a strong incumbent.
So a stronger incumbent creates neither trading nor entry here.
A fixed reserve of $0.5$ would raise entry to $0.625$ at $r=3$.
It would cut seller proceeds from $1.25$ to $0.94$.
The best committed reserve is also $10$, so commitment adds no proceeds.
Commitment helps entry only if the seller commits to a low reserve.
At $r=3.6$ the seller instead cuts the reserve after good news.
That cut restores expensive entry at that one strength.
The general lesson is a hold-up with a twist.
The seller exploits the price signal and kills the entry response.
At the same time it widens the share payoff spread.
Trading thrives while takeover competition does not.

---

Evidence note.
All numbered values come from one print-only script.
Its path is `scripts/C8_reserve/c8_reserve.py` in the team folder.
Its full output is `scripts/C8_reserve/output.txt`.
The script uses 50-digit arithmetic and exact fractions at $p=1/2$.
It values the seller optimum by a dense grid and by a candidate list.
Status labels in the text mark which claims rest on that computation.

