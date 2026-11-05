# Point 2: discrete microstructure with purchases only

## 1. Question and reading

This memo studies the pinned buy-only variant. The investor chooses $q\in\{0,1\}$ and starts with no shares. The challenger observes the price, not the flow. The leading case has an investor in every economy and equal noise probabilities.

**Main result — analytical.** Equal noise gives a complete equilibrium description. Under the cost floor, one threshold separates no trade from purchases. Both interior flows retain the prior. Full purchases reveal quality at the two extreme flows. A Proposition 2 analog holds under the conditions below.

**Main qualification — analytical.** Full revelation changes both participation bounds. The sufficient low-cost floor becomes $c_L<g_L$, and the expensive-entry ceiling becomes $c_H>g_H$. The paper's benchmark satisfies neither restriction at $r_2=3.6$. Its discrete outcomes therefore differ from its Laplace outcomes.

The source for the auction and information sets is [the current paper](../../../overleaf/paper/main.tex), Sections 2–4 and Appendix A.1–A.2. The specification and document rules follow [the shared brief](../BRIEF.md), Sections 0, 3.2, and 4. This memo derives a separate model. It does not revise the manuscript.

The checked literature source is Edmans, Goldstein, and Jiang (2015), *American Economic Review* 105(12), 3766–3797. Section I.B specifies equal noise, uncertain investor presence, and no trade at investor indifference. Section I.C uses the Intuitive Criterion. Section II.C applies extreme-flow beliefs. Their decision maker observes flow. Section I.B also warns that price observation can admit other equilibria. These details matter for the floor below. [Published text](https://alexedmans.com/wp-content/uploads/2024/06/LTA.pdf). The April 2015 version labels the corresponding setup Sections 2.2–2.3. [Author version](https://www.ecgi.global/sites/default/files/2026-10/fin-318-2011_feedback_effects_asymmetric_trading_and_the_limits_to_arbitr.pdf).

## 2. Formal setup

Maintain $0<p<\ell<r<h$, equal priors on $H,L$, and $0<\rho<1$. The incumbent has $R\sim U[0,r]$. Preparation costs satisfy $0\le c_L<c_H$. All independence assumptions in the paper remain in force.

The investor observes quality perfectly. It buys one share with probability $\beta_H$ in state $H$ and probability $\beta_L$ in state $L$. Its payoff is $q(V_T-P)-kq$, with $k>0$. Noise is independent of quality and the investor's action.

The leading case has $\Pr(Z=-1)=\Pr(Z=0)=\Pr(Z=1)=1/3$. Market makers observe $X=q+Z$. They set a competitive price. The challenger observes that price and its cost. It then decides whether to prepare.

An indifferent challenger prepares. The prescribed investor rule selects $q=0$ at indifference. This rule excludes a genuine mixture between zero and one. I also report the usual equilibrium correspondence when mixtures at indifference are permitted.

Use the paper's auction objects:

$$
\begin{aligned}
t_0&=p(1-p/r), &t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),
&g_H&=h-r/2-p^2/(2r),\\
g_L&=(\ell^2-p^2)/(2r),
&\Delta_T&=(r-\ell)^2/(2r).
\end{aligned}
$$

Put $w_L=t_L-t_0>0$ and $B_r(\mu)=g_L+\mu(g_H-g_L)$. For a price that reveals posterior $\mu$, define

$$
e_r(\mu)=\rho\mathbf1\{B_r(\mu)\ge c_L\}
 +(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},
\qquad
P_r(\mu)=t_0+e_r(\mu)(w_L+\Delta_T\mu).
$$

This definition permits zero entry. Under $c_L<g_L=B_r(0)$, it reduces to the paper's formula with the new posterior range $[0,1]$. Write $\bar e=e_r(1/2)$, $e_0=e_r(0)$, and $e_1=e_r(1)$.

Entry $\mathsf E$ is the preparation probability. Ownership $\mathsf O_H$ is the probability that the high-value **challenger** acquires the target. Since $h>r$, $\mathsf O_H=\Pr(H,\text{entry})$.

## 3. Results

### Claim 1 — analytical: all leading-case flow posteriors

For arbitrary pure or mixed orders, the conditional laws and Bayesian posteriors are

| Flow $x$ | $\Pr(x\mid H)$ | $\Pr(x\mid L)$ | $\mu_x=\Pr(H\mid x)$ |
|---|---:|---:|---:|
| $-1$ | $(1-\beta_H)/3$ | $(1-\beta_L)/3$ | $(1-\beta_H)/(2-\beta_H-\beta_L)$ |
| $0$ | $1/3$ | $1/3$ | $1/2$ |
| $1$ | $1/3$ | $1/3$ | $1/2$ |
| $2$ | $\beta_H/3$ | $\beta_L/3$ | $\beta_H/(\beta_H+\beta_L)$ |

Each posterior is the first conditional probability divided by the sum of both probabilities. A zero denominator marks an off-path flow. Thus $0$ and $1$ carry no information under **any** pair of strategies.

The four pure candidates give:

| $(\beta_H,\beta_L)$ | $\mu_{-1}$ | $\mu_0$ | $\mu_1$ | $\mu_2$ | Off-path flow |
|---|---:|---:|---:|---:|---|
| $(0,0)$ | $1/2$ | $1/2$ | $1/2$ | unspecified | $2$ |
| $(1,0)$ | $0$ | $1/2$ | $1/2$ | $1$ | none |
| $(0,1)$ | $1$ | $1/2$ | $1/2$ | $0$ | none |
| $(1,1)$ | unspecified | $1/2$ | $1/2$ | $1/2$ | $-1$ |

For mixtures, $2$ reveals $H$ exactly when $\beta_H>0=\beta_L$. It reveals $L$ exactly when $\beta_L>0=\beta_H$. Flow $-1$ reveals $L$ when $\beta_H=1>\beta_L$. It reveals $H$ when $\beta_L=1>\beta_H$.

After Claim 2, write $\beta=\beta_H$ and set $\beta_L=0$. For $\beta>0$,

$$
(\mu_{-1},\mu_0,\mu_1,\mu_2)
=\left(\frac{1-\beta}{2-\beta},\frac12,\frac12,1\right),
\qquad
(\Pr(-1),\Pr(0),\Pr(1),\Pr(2))
=\left(\frac{2-\beta}{6},\frac13,\frac13,\frac\beta6\right).
$$

Only $2$ reveals quality for $0<\beta<1$. Both extremes reveal quality at $\beta=1$. All four flows have positive probability when $\beta>0$.

### Claim 2 — analytical: the low-quality investor never buys

Let $e(P)$ be actual entry at price $P$, averaged over costs. This notation does not assume price sufficiency. Independence and competitive prices imply

$$
\begin{aligned}
\mathbb E[V_T\mid\theta,x]&=t_0+e(P(x))(t_\theta-t_0),\\
P(x)&=t_0+e(P(x))(w_L+\Delta_T\mu_x).
\end{aligned}
$$

Subtract the price from each type's expected terminal value:

$$
V_H(x)-P(x)=e(P(x))\Delta_T(1-\mu_x)\ge0,
\qquad
V_L(x)-P(x)=-e(P(x))\Delta_T\mu_x\le0.
$$

Buying therefore gives the low-quality investor at most $-k<0$. Zero gives it zero. Hence $\beta_L=0$ in every equilibrium. This argument also holds at off-path flows with competitive prices and beliefs in $[0,1]$.

The investor cannot earn the public gain from extra entry on an existing stake. Its initial stake is zero. Rational prices already include that public gain. At a revealing high-quality flow, the high-quality investor's gross residual is also zero.

### Claim 3 — analytical: prices reveal posteriors under the floor

Suppose $c_L<g_L$. Every posterior makes low-cost preparation profitable, so $e(P)\ge\rho$. Competitive prices yield

$$
\mu_x=
\frac{P(x)-t_0-e(P(x))w_L}{e(P(x))\Delta_T}.
$$

The denominator is positive. The right side depends only on the price. Thus the challenger recovers $\mu_x$ from the price in every candidate equilibrium. This proves the discrete analog of Proposition A.2.

The construction is also unique. For $\mu'>\mu$,

$$
P_r(\mu')-P_r(\mu)
=e_r(\mu')\Delta_T(\mu'-\mu)
 +[e_r(\mu')-e_r(\mu)](w_L+\Delta_T\mu)>0.
$$

Two flows share a price if and only if they share a posterior. In particular, $P(0)=P(1)$ in the leading case. This equality loses no information. Under full purchases, prices have three values, corresponding to $0,1/2,1$.

Without the floor, the inversion remains valid at every price with positive entry. At zero entry, the price equals $t_0$. Different posteriors can then share that price. The challenger uses their pooled posterior. Claim 6 classifies those additional equilibria.

### Claim 4 — analytical: off-path beliefs and their exact role

The only off-path flow in a surviving strategy profile is $2$ under no trade. I use the Intuitive Criterion, completed by the belief $\mu_2=1$ wherever the criterion is silent. This is the following explicit rule: attribute an unused purchase to $H$, then set its price and entry consistently.

Claim 2 rules out a profitable purchase deviation by $L$ under every receiver response. If some response makes a purchase profitable for $H$, the criterion excludes $L$. If no response benefits either type, the criterion imposes no restriction. The stated completion still assigns probability one to $H$.

Under the floor, let an arbitrary alternative completion assign $\mu_2=v$. A high-quality purchase from the no-trade candidate gives

$$
U_H(1;\beta=0)
=\frac{\Delta_T\bar e}{3}
 +\frac{\Delta_T}{3}e_r(v)(1-v)-k.
$$

The first term comes from flows $0,1$. The second term comes from the new flow $2$. It is nonnegative and vanishes at $v=1$.

Consequently, no trade is impossible under every completion if $k<\Delta_T\bar e/3$. It is an equilibrium under the stated completion if $k\ge\Delta_T\bar e/3$. Full-purchase equilibria use Bayes' rule at every flow and need no off-path belief.

The cutoff and every positive-trade outcome therefore survive the stated criterion and completion. An arbitrary optimistic price at flow $2$ can invalidate a proposed no-trade schedule. It cannot create no trade below the cutoff. Beliefs after flow $-1$ in candidate $(1,1)$ never affect the result: Claim 2 already excludes that candidate.

### Claim 5 — analytical: the complete equilibrium set under the floor

For any $\beta>0$, a high-quality purchase reaches $0,1,2$ with probability $1/3$ each. Their posteriors are $1/2,1/2,1$. Claim 3 therefore gives

$$
U_H(1;\beta)
=\frac13\bar e\Delta_T\left(1-\frac12\right)
 +\frac13\bar e\Delta_T\left(1-\frac12\right)
 +\frac13e_1\Delta_T(1-1)-k
=K_2(r)-k,
\qquad
K_2(r)=\frac{\bar e\Delta_T(r)}3.
$$

This profit does not depend on $\beta$. Claim 4 gives the same expression at $\beta=0$ under the stated completion. Zero always earns zero. These are the only two actions.

With the prescribed investor tie rule, **all** equilibrium outcomes satisfy

$$
\boxed{
\beta_L=0,\qquad
\beta_H=
\begin{cases}
0,& k\ge K_2(r),\\
1,& k<K_2(r).
\end{cases}}
$$

Prices and on-path entry are unique under the floor. Off-path completions can remain nonunique. There is no interval of coexistence at a fixed $r$.

If indifferent investors may mix, the complete correspondence becomes

$$
\beta_H\in
\begin{cases}
\{0\},& k>K_2(r),\\
[0,1],& k=K_2(r),\\
\{1\},& k<K_2(r).
\end{cases}
$$

Thus mixed equilibria form a continuum only at the threshold. A rule that selects purchases at indifference instead selects $\beta_H=1$ there.

For the paper's intended region, $B_r(1/2)<c_H$ and $c_L<g_L$, we have $\bar e=\rho$. Define

$$
\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d},
\qquad
\boxed{r_T=\mathfrak r(3k/\rho).}
$$

Solving $\Delta_T(r)=d$ gives $(r-\ell)^2=2rd$, whose root above $\ell$ is $\mathfrak r(d)$. Since $\Delta_T'(r)>0$, no trade occurs exactly at $r\le r_T$. Purchases occur exactly at $r>r_T$, within the maintained domain.

For unrestricted $c_H$, the precise cutoff is still $K_2(r)$, but $\bar e$ can change. Under the floor,

$$
\bar e=
\begin{cases}
1,&B_r(1/2)\ge c_H,\\
\rho,&B_r(1/2)<c_H.
\end{cases}
$$

The two spread thresholds are $\mathfrak r(3k)$ and $\mathfrak r(3k/\rho)$. If a prior-cost crossing lies in $(\ell,h)$, its root is

$$
r_P=h-2c_H+\sqrt{(h-2c_H)^2+\ell^2-2p^2}.
$$

This follows from $B_r(1/2)=h/2-r/4+(\ell^2-2p^2)/(4r)$. Entry at the prior falls just above $r_P$. Consequently, the global path can switch from trade to no trade and then back to trade. This occurs if

$$
\mathfrak r(3k)<r_P<\mathfrak r(3k/\rho),
$$

with all points inside the floor domain. The single increasing cutoff applies after expensive entry at the prior is excluded. It is not a claim about every possible $c_H$.

### Claim 6 — analytical: complete leading-case outcomes without the floor

This claim retains equal noise and certain investor presence. It covers the benchmark's failed floor. It also identifies the extra price equilibria that the floor excludes.

First suppose $B_r(1/2)<c_L$. Claim 2 still gives $\beta_L=0$. Every positive-entry price reveals its flow posterior by the inversion in Claim 3. The interior posterior is $1/2$, which cannot support entry. The only possible entry after a purchase is then at posterior one, where its residual is zero. Every purchase loses $k$. No trade and zero entry are the unique outcome.

Now suppose $c_L\le B_r(1/2)$, so $\bar e>0$. For every $\beta>0$, a **canonical schedule** sets prices and entry from each flow's own posterior. It allows zero entry at $-1$. It remains consistent because no other flow shares $t_0$ in this schedule. The high-quality purchase profit is $K_2-k$, as before.

To find every other schedule, collect all zero-entry flows into a set $S$. They all have price $t_0$. If flow $2$ belongs to $S$, the pooled posterior is at least $1/2$. To see this, its only lower-posterior partner is $-1$, and those two flows together have posterior $1/2$. The interior flows also have posterior $1/2$. Such a pool would induce low-cost entry, a contradiction.

If an interior flow belongs to $S$, the pool must also contain $-1$. Otherwise its posterior is at least $1/2$. A pool with both interior flows leaves no positive gross purchase payoff. It cannot support trade because $k>0$.

Thus every additional trading equilibrium pools $-1$ with **exactly one** interior flow. The other interior flow retains posterior $1/2$ and positive entry. The zero-entry pool has posterior

$$
\nu_1(\beta)=\frac{2-\beta}{4-\beta}.
$$

The numerator is the high-state mass of these two flows, in units of $1/6$. The denominator is their total mass in those units. Such a pool is consistent exactly when

$$
B_r(\nu_1(\beta))<c_L.
$$

The inequality is strict because the challenger prepares at indifference. Only one interior flow now earns a residual. The purchase profit becomes

$$
K_1(r)-k,\qquad K_1(r)=\frac{\bar e\Delta_T(r)}6=\frac{K_2(r)}2.
$$

This gives the exhaustive classification:

| Schedule | Feasibility | Investor condition with the prescribed tie rule |
|---|---|---|
| No trade | stated completion at $2$ | $k\ge K_2$ |
| Canonical full purchases | $c_L\le B_r(1/2)$ | $k<K_2$ |
| Full purchases with one inactive interior flow | $B_r(1/3)<c_L\le B_r(1/2)$ | $k<K_1$ |

The third row gives two price functions. Either $0$ or $1$ can join $-1$ at price $t_0$. Both give the same entry and ownership. Under the floor, the third row is impossible since $B_r(1/3)>g_L>c_L$.

With conventional mixing, replace each full-purchase inequality by a weak inequality. Add canonical mixtures $0<\beta<1$ exactly when $k=K_2$. Add pooled mixtures exactly when $k=K_1$ and $B_r(\nu_1(\beta))<c_L$. These conditions are necessary and sufficient by the preceding pool classification and the two-action payoff comparison.

For an explicit mixed-support restriction, put $\eta=(c_L-g_L)/(g_H-g_L)$. When $1/3<\eta\le1/2$, pooled mixtures require

$$
\beta>\frac{2-4\eta}{1-\eta}.
$$

This follows by solving $(2-\beta)/(4-\beta)<\eta$. There are no such mixtures when $\eta\le1/3$. These extra price equilibria explain why a failed floor cannot simply be ignored.

### Claim 7 — analytical: closed forms for entry and ownership

For the canonical schedule, let $a_\beta=e_r((1-\beta)/(2-\beta))$. Direct sums over the four flows give

$$
\boxed{
\begin{aligned}
\mathsf E(\beta)
 &=\frac{(2-\beta)a_\beta+4\bar e+\beta e_1}{6},\\
\mathsf O_H(\beta)
 &=\frac{(1-\beta)a_\beta+2\bar e+\beta e_1}{6}.
\end{aligned}}
$$

The ownership formula uses the conditional high-state flow probabilities, then multiplies by the prior $1/2$. The formulas also hold at $\beta=0$, where $a_0=\bar e$.

For full purchases, these simplify to

$$
\mathsf E(1)=\frac{e_0+4\bar e+e_1}{6},
\qquad
\mathsf O_H(1)=\frac{2\bar e+e_1}{6}.
$$

Under $c_L<g_L$ and $B_r(1/2)<c_H$, put $I_r=\mathbf1\{g_H(r)\ge c_H\}$. Then $a_\beta=\bar e=\rho$ and $e_1=\rho+(1-\rho)I_r$, so

$$
\boxed{
\mathsf E(\beta)=\rho+\frac{(1-\rho)\beta}{6}I_r,
\qquad
\mathsf O_H(\beta)=\frac\rho2+\frac{(1-\rho)\beta}{6}I_r.}
$$

Additional preparation occurs only in state $H$, at flow $2$. Its unconditional probability is $\beta/6$. Thus the entry increase equals the ownership increase.

For a schedule with one inactive interior flow, the corresponding formulas are

$$
\mathsf E_{\mathrm{pool}}(\beta)=\frac{\bar e}{3}+\frac{\beta e_1}{6},
\qquad
\mathsf O_{H,\mathrm{pool}}(\beta)=\frac{\bar e}{6}+\frac{\beta e_1}{6}.
$$

The zero-entry pool contributes nothing. The remaining interior flow has unconditional probability $1/3$ and high-state joint probability $1/6$.

### Claim 8 — analytical: a Proposition 2 analog

Fix $0<p<\ell<r_0<r_1<r_2<h$. The following three conditions suffice:

$$
\tag{A1-D}
0\le c_L<g_L(r_2),
$$

$$
\tag{A2-D}
B_{r_0}(1/2)<c_H<g_H(r_1),
\qquad g_H(r_2)<c_H,
$$

$$
\tag{A3-D}
\frac{\rho\Delta_T(r_0)}3<k<\frac{\rho\Delta_T(r_1)}3.
$$

Condition (A1-D) gives the cost floor at all three strengths because $g_L$ decreases in $r$. Condition (A2-D) excludes expensive entry at the prior for all $r\ge r_0$. It permits expensive entry at posterior one at $r_1$ and excludes it at $r_2$.

Claim 5 and (A3-D) force no trade at $r_0$ and full high-quality purchases at $r_1$. Since $\Delta_T$ increases, full purchases also remain unique at $r_2$. Claim 3 gives unique on-path prices and entry. The outcomes are

$$
\begin{array}{c|c|c|c}
& (q_H,q_L)&\mathsf E&\mathsf O_H\\ \hline
r_0&(0,0)&\rho&\rho/2\\
r_1&(1,0)&\rho+(1-\rho)/6&\rho/2+(1-\rho)/6\\
r_2&(1,0)&\rho&\rho/2
\end{array}
$$

The $r_1$ price strictly improves on the constant $r_0$ experiment in the Blackwell order. A constant signal cannot generate different price laws across states. The full-purchase experiment can reproduce a constant signal by discarding its realization.

These conditions describe an open region. For example, take the benchmark values except $c_L=0.02$ and $r_2=8.5$. The exact inequalities are

$$
\frac1{50}<\frac3{68}=g_L(8.5),\qquad
\frac{1153}{240}=B_{1.2}(1/2)<6<\frac{203}{24}=g_H(3),
$$

$$
g_H(8.5)=\frac{195}{34}<6,\qquad
\frac1{720}=\frac{\rho\Delta_T(1.2)}3
<\frac1{50}=k<\frac1{18}=\frac{\rho\Delta_T(3)}3.
$$

All gaps are strict, and all functions are continuous in the primitives. A neighborhood therefore satisfies the same inequalities. The left inequality in (A3-D) can be weak under the prescribed investor rule.

The exact expensive-entry crossing, if it lies in $(\ell,h)$, is

$$
\boxed{r_C^{D}=h-c_H+\sqrt{(h-c_H)^2-p^2}.}
$$

This follows from $r^2-2(h-c_H)r+p^2=0$. Choose the root above $p$. Expensive entry persists **at** the crossing because the challenger enters at indifference. Strictly above it, that entry disappears.

A return before $r=h$ requires $c_H>h/2-p^2/(2h)$, in addition to $c_H<g_H(r_1)$. Otherwise even the strongest permitted incumbent cannot deter preparation after posterior one. This restriction has no counterpart based on the Laplace ceiling $M<1$.

### Claim 9 — analytical: the fixed-experiment control

Hold the investor's strategy and the noise law fixed. Under the floor, Claim 3 makes the price reveal the unchanged flow posterior. For $r'>r$ and each flow,

$$
B_{r'}(\mu_x)<B_r(\mu_x),
\qquad
\mathbf1\{C\le B_{r'}(\mu_x)\}
\le\mathbf1\{C\le B_r(\mu_x)\}.
$$

The inequality follows because both $g_H$ and $g_L$ decrease. Average over flows and costs. Entry weakly falls. It falls strictly if a crossed cost has positive probability. This is the Proposition A.3 analog, without a restriction to pure orders.

The same argument applies without the floor if the price still reveals each flow posterior. It therefore applies to every canonical leading-case schedule. A change in the numerical price level does not change that experiment.

Outside the floor, a fixed investor strategy alone need not fix the **price** experiment. For example, take $c_L=3$ and retain the other benchmark parameters. At $r=3$, full purchases support the pool $\{-1,0\}$ because

$$
B_3(1/3)=2.902777\ldots<3<B_3(1/2)=4.291666\ldots,
\qquad
\rho\Delta_T(3)/6-k=0.007777\ldots>0.
$$

This equilibrium has $\mathsf E=\rho/3+1/6=1/4$. At $r=3.1$, the canonical full-purchase equilibrium has $\mathsf E=1/3$. Orders remain $(1,0)$, but the price partition changes. This does not contradict Proposition A.3: the challenger's experiment changes. A global fixed-strategy control needs the floor or a fixed sufficient price partition.

### Claim 10 — analytical: general noise and its full finite characterization

Let $(a,d,c)=(\pi_-,\pi_0,\pi_+)$, with all three probabilities positive and $a+d+c=1$. The letter $d$ here denotes the middle noise probability. It is not the spread argument in $\mathfrak r(\cdot)$.

Allow investor presence with probability $\lambda\in(0,1]$. Put $s_j=\lambda\beta_j$. The conditional likelihoods are

| Flow | $\Pr(x\mid j)$ |
|---|---:|
| $-1$ | $a(1-s_j)$ |
| $0$ | $d+s_j(a-d)$ |
| $1$ | $c+s_j(d-c)$ |
| $2$ | $cs_j$ |

Bayes' rule gives

$$
\begin{aligned}
\mu_{-1}&=\frac{1-s_H}{2-s_H-s_L},\\
\mu_0&=\frac{d+s_H(a-d)}{2d+(s_H+s_L)(a-d)},\\
\mu_1&=\frac{c+s_H(d-c)}{2c+(s_H+s_L)(d-c)},\\
\mu_2&=\frac{s_H}{s_H+s_L}.
\end{aligned}
$$

Claim 2 again gives $s_L=0$. Write $s=\lambda\beta_H$. A positive purchase strategy still makes flow $2$ reveal $H$. Flow $-1$ reveals $L$ only at $s=1$.

The interior flow $0$ is informative exactly when $s>0$ and $a\ne d$. Flow $1$ is informative exactly when $s>0$ and $d\ne c$. For arbitrary type strategies, replace $s>0$ by $s_H\ne s_L$. Cross multiplication shows that the two interior posteriors agree exactly when

$$
(s_H-s_L)(ac-d^2)=0.
$$

Thus geometric noise probabilities can give equal informative interior prices. Equal noise is the special case in which both posteriors equal the prior. Price sufficiency still holds under the floor. A monotone price as a function of numerical flow is not required.

For $s_L=0$, define

$$
D_0(s)=2d+s(a-d),\qquad D_1(s)=2c+s(d-c).
$$

A high-quality purchase reaches $0,1,2$ with probabilities $a,d,c$. Its gross payoff under the floor is therefore

$$
\boxed{
K_r(s)=\Delta_T(r)\left[
\frac{ad\,e_r(\mu_0(s))}{D_0(s)}
+\frac{dc\,e_r(\mu_1(s))}{D_1(s)}\right].}
$$

The revealing flow contributes zero. The posterior identities $1-\mu_0=d/D_0$ and $1-\mu_1=c/D_1$ give the formula. At zero purchases, the stated off-path completion gives

$$
K_r(0)=\frac{\Delta_T(r)\bar e}{2}(a+d)
=\frac{\Delta_T(r)\bar e}{2}(1-c).
$$

Here is the complete equilibrium characterization under the floor:

| High-quality strategy | Prescribed investor rule | Conventional mixing rule |
|---|---|---|
| $\beta_H=0$ | $k\ge K_r(0)$ | same |
| $\beta_H=1$ | $k<K_r(\lambda)$ | $k\le K_r(\lambda)$ |
| $0<\beta_H<1$ | excluded at indifference | $k=K_r(\lambda\beta_H)$ |

In every row, $\beta_L=0$. These conditions compare the only two feasible actions. The price construction in Claim 3 proves sufficiency. Claim 2 and the same payoff comparison prove necessity.

This characterization is algebraically finite. Let $\tau=(c_H-g_L)/(g_H-g_L)$. Each interior entry indicator changes only where $\mu_i(s)=\tau$. The candidate changes are

$$
s_0=\frac{d(2\tau-1)}{(1-\tau)(a-d)},
\qquad
s_1=\frac{c(2\tau-1)}{(1-\tau)(d-c)}.
$$

Retain only defined values in $(0,\lambda]$. A zero denominator or a threshold outside $[0,1]$ gives no interior crossing. At a valid crossing, use the challenger's entry-at-indifference rule.

Within each resulting interval, let $e^0,e^1\in\{\rho,1\}$ denote the fixed interior entry rates. A conventional mixed equilibrium solves the quadratic equation

$$
\frac{k}{\Delta_T}D_0(s)D_1(s)
=ad e^0D_1(s)+dc e^1D_0(s).
$$

Retain roots only in the interval whose entry rates were used. Constant coefficients can make the equation linear or identically zero. This procedure gives every mixed root, including a continuum in the equal-noise threshold case.

For any fixed $s$, the relevant incumbent crossings also have closed forms. A cost crossing $B_r(\mu)=c_H$, for $\mu>0$, has the root

$$
r_C(\mu)=\frac{\mu h-c_H+
\sqrt{(\mu h-c_H)^2+\mu[(1-\mu)\ell^2-p^2]}}{\mu},
$$

when that root lies in the model's domain. Between cost crossings, write $K_r(s)=\Delta_T(r)L(s)$ with fixed entry rates. The trading boundary there is $r=\mathfrak r(k/L(s))$. Hence general noise gives several explicit boundaries, rather than one universal cutoff.

For closed forms of the outcomes, set

$$
\begin{aligned}
f_H&=((1-s)a,\ d+s(a-d),\ c+s(d-c),\ sc),\\
w&=((2-s)a/2,\ D_0(s)/2,\ D_1(s)/2,\ sc/2).
\end{aligned}
$$

The vectors list flows in the order $-1,0,1,2$. Then

$$
\boxed{\mathsf E=\sum_x w_x e_r(\mu_x),
\qquad \mathsf O_H=\frac12\sum_x f_{H,x}e_r(\mu_x).}
$$

When $B_r(1/2)<c_H$ and the floor holds, define $I_i=\mathbf1\{B_r(\mu_i)\ge c_H\}$ for $i=0,1$. Also define $I_2=\mathbf1\{g_H\ge c_H\}$. Since $\mu_{-1}\le1/2$, these become

$$
\begin{aligned}
\mathsf E
 &=\rho+\frac{1-\rho}{2}[D_0 I_0+D_1 I_1+scI_2],\\
\mathsf O_H
 &=\frac\rho2+\frac{1-\rho}{2}
 \{[d+s(a-d)]I_0+[c+s(d-c)]I_1+scI_2\}.
\end{aligned}
$$

General noise can therefore recruit expensive preparation in either interior flow. Unlike the equal-noise case, some additional entrants can have low quality.

For completeness, the finite characterization also extends outside the floor. For each $s>0$, choose a set $S$ of flows with price $t_0$. Define its pooled belief by

$$
\nu_S(s)=\frac{\sum_{x\in S}w_x\mu_x}{\sum_{x\in S}w_x}.
$$

Require $B_r(\nu_S)<c_L$ for a nonempty $S$. For every flow outside $S$, require $e_r(\mu_x)>0$ and use its own-posterior price. These conditions construct every possible price partition: all zero-entry prices equal $t_0$, and every positive-entry price reveals its posterior.

Replace each interior entry term in $K_r(s)$ by zero when that flow belongs to $S$. Use zero entry for those flows in the outcome sums as well. Use the same investor conditions above. Enumerate the at most sixteen sets $S$, including the canonical empty set. For $s=0$, use the no-trade completion in Claim 4. This is an exact finite description; it does not assume that the challenger sees flow.

Zero noise probabilities require support conventions. The likelihood table remains valid. Omit flows with zero total probability before division. Complete every unused flow reachable by a purchase with belief $H$. The no-trade payoff then becomes

$$
K_r(0)=\frac{\Delta_T\bar e}{2}
\left[a\mathbf1\{d>0\}+d\mathbf1\{c>0\}\right].
$$

Only flows shared by a purchase and no trade contribute this prior residual. A newly reached flow reveals $H$ under the stated completion. For $s>0$, the formula for $K_r(s)$ still applies, with a zero numerator contributing zero. The finite partition description uses only positive-mass flows.

For example, if noise takes only $-1$ and $1$, the two actions have disjoint flow supports. Every purchase flow reveals $H$, so its gross residual is zero. No trade is then the unique outcome for $k>0$. Thus the positive-noise assumption matters for the nontrivial cutoff formulas.

### Claim 11 — analytical: unequal noise destroys general clean uniqueness

In an interval with fixed interior entry rates, differentiation gives

$$
K_r'(s)=-\Delta_T\left[
\frac{ad e^0(a-d)}{D_0(s)^2}
+\frac{dc e^1(d-c)}{D_1(s)^2}\right].
$$

If $a<d<c$ and expensive entry at the prior is excluded, both interior posteriors lie below the prior. Thus $e^0=e^1=\rho$ under the floor, and $K_r'(s)>0$. It follows that $K_r(\lambda)>K_r(0)$. Every cost in

$$
K_r(0)\le k<K_r(\lambda)
$$

supports both no trade and full purchases, even under the prescribed tie rule. This proves multiplicity on an interval. Arbitrarily small increasing perturbations of equal noise create such an interval.

For an exact illustration, set $(a,d,c)=(1/10,1/5,7/10)$, $\lambda=1$, and $\Delta_T=1$. Retain $\rho=1/4$, $c_H=6$, and use $c_L=0.02$. This spread occurs at $r=2+\sqrt3$ for $\ell=1$. Both interior beliefs remain below the prior. The endpoint payoffs are

$$
K_r(0)=\frac{3}{80}=0.0375,
\qquad
K_r(1)=\frac1{18}=0.055555\ldots.
$$

At $k=0.045$, both pure outcomes exist. Under conventional mixing, the strictly increasing continuous function also gives one interior root.

The reverse ordering can require mixing. Set $(a,d,c)=(7/10,1/5,1/10)$ and choose $c_H=12$, so entry remains $\rho$ at every belief. Then $K_r'(s)<0$,

$$
K_r(0)=\frac9{80}=0.1125,
\qquad K_r(1)=\frac1{18}.
$$

At $k=0.08$, neither pure outcome is an equilibrium. A unique conventional mixture exists by strict monotonicity and continuity. The prescribed rule forbids that mixture. It therefore leaves **no equilibrium** for these parameters. This is a consequence of the tie selection, not a failed computation.

**Numerical diagnostic.** The script gives mixed probabilities $0.5160395534$ in the first example and $0.3856157589$ in the second. The existence and uniqueness arguments above do not depend on those numerical roots.

### Claim 12 — analytical: uncertain investor presence preserves the equal-noise structure

For equal noise and $\beta_L=0$, put $s=\lambda\beta_H$. Claim 10 reduces to

$$
\mu_{-1}=\frac{1-s}{2-s},\quad \mu_0=\mu_1=\frac12,\quad\mu_2=1,
\qquad
K_r(s)=\frac{\bar e\Delta_T}3.
$$

Conditional on a purchase, the three reached flows retain probabilities $1/3$. Their posteriors remain $1/2,1/2,1$. Hence $\lambda$ does not change the trading cutoff. It changes how often the revealing purchase flow occurs.

For full purchases when present, the lowest on-path posterior is

$$
m_\lambda=\frac{1-\lambda}{2-\lambda}>0\quad\text{if }\lambda<1.
$$

This is also a lower bound for every flow posterior after Claim 2 excludes low-quality purchases. For the interior flows, their likelihood ratios are at least $1-s$. Flow $-1$ attains that bound. Therefore $c_L<B_r(m_\lambda)$ suffices for the equilibrium-wide participation floor in this extension.

Under that floor and $B_r(1/2)<c_H$, the full-purchase outcomes become

$$
\boxed{
\mathsf E=\rho+\frac{(1-\rho)\lambda}{6}\mathbf1\{g_H\ge c_H\},
\qquad
\mathsf O_H=\frac\rho2+\frac{(1-\rho)\lambda}{6}\mathbf1\{g_H\ge c_H\}.}
$$

For mixtures, replace $\lambda$ by $\lambda\beta_H$. For a three-strength proposition, replace (A1-D) by $c_L<B_{r_2}(m_\lambda)$. Conditions (A2-D) and (A3-D) stay the same. Flow $-1$ ceases to reveal $L$, while flow $2$ still reveals $H$. The expensive-entry ceiling remains $g_H$, not the Laplace bound $B_r(M)$.

The degenerate case $\lambda=0$ has no informed investor. Its entry is based on the prior. It should not be inferred from the conditional incentive statement for $\lambda>0$.

## 4. What changes relative to the current paper

The following comparisons are **analytical**. Claims 1–12 give their derivations.

| Paper object | Discrete buy-only result |
|---|---|
| Proposition 1 and equation (4) | All auction objects and their derivatives survive unchanged. |
| Equations (7)–(8), Proposition A.1 | No common interior posterior interval survives when presence is certain. Full purchases attain $0$ and $1$. |
| Equation (9), low-cost floor | The sufficient floor becomes $c_L<g_L$. With uncertain presence, the equilibrium-wide floor can use $m_\lambda$. |
| Equation (10), Proposition A.2 | The same inversion proves price sufficiency under the floor. Interior flows can share a price because their posteriors agree. |
| Equation (11) | The residual identities survive. Their positive pointwise lower bound fails at revealing flows. |
| Equation (A.6) | No density derivative is needed. A single comparison, $K_r(s)-k$, covers every feasible unilateral deviation. |
| Proposition 2 | Conditions (A1-D)–(A3-D) yield the same three-economy qualitative pattern. Orders become $(1,0)$. |
| Equation (12) | Finite sums replace Laplace tails. In the equal-noise region, entry and ownership increments are $(1-\rho)/6$. |
| Proposition A.3 | It survives under a fixed sufficient experiment. A fixed strategy alone needs a price-information condition outside the floor. |
| Proposition A.4 | The exact trading boundary is $\mathfrak r(3k/\rho)$ when expensive entry at the prior is excluded. |
| Proposition 3 | Equal noise has no open interval of coexistence under the floor. Unequal noise can restore such an interval. |
| Expensive-entry ceiling | The relevant posterior ceiling is one. Entry persists through $g_H(r)=c_H$ and disappears strictly above it. |

Several arguments become shorter. Bayesian inference uses four rows. Global deviations reduce to two actions. The high-quality investor's profit does not depend on its purchase probability under equal noise. This makes the complete correspondence available analytically.

Other issues become harder. New flows can appear after deviations, so beliefs need a rule. Revealing flows invalidate a positive residual bound. Zero-entry prices can hide different beliefs without the floor. Unequal noise creates informative interior flows and several entry thresholds.

The equal-noise model also changes the mechanism's detail. In the intended region, extra expensive entry occurs only at a revealing high-quality flow. The investor earns zero residual there. Its trading cutoff depends on $\rho\Delta_T$, not on that extra entry. Greater incumbent strength still activates information, which then attracts preparation. The direct contribution of expensive entry to trading incentives disappears in this special case.

The information experiment has only three posterior values under full purchases. The entry path is a set of jumps and plateaus. It does not preserve the paper's smooth variation through interior Laplace beliefs. Clean uniqueness also depends on equal noise; Claim 11 proves that nearby noise probabilities can restore multiplicity.

## 5. Numerical example

**Status: numerical diagnostic.** The script is [compute.py](../scripts/Q2_discrete_buy_only/compute.py). Run it from the repository root:

```bash
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_discrete_buy_only/compute.py
```

The program uses decimal inputs and 60-digit arithmetic. It prints finite flow sums, prices, entry, ownership, purchase payoffs, and the equilibrium set. It also prints the presence extension and the unequal-noise examples. Display classification treats cost gaps below $10^{-50}$ and the trading-cutoff gap below $10^{-45}$ as ties. The exact boundary conventions follow the analytical results. The results below come from that direct run.

### Original benchmark

Use $(h,\ell,p,\rho,c_L,c_H,k)=(10,1,0.5,0.25,1,6,0.02)$. The Laplace scale $b=2$ has no role in this model.

| Strength | High-quality purchase probability | Entry $\mathsf E$ | Ownership $\mathsf O_H$ | High-quality purchase payoff |
|---:|---:|---:|---:|---:|
| $r_0=1.2$ | $0$ | $0.2500000000$ | $0.1250000000$ | $-0.0186111111$ |
| $r_1=3$ | $1$ | $0.3333333333$ | $0.2500000000$ | $0.0355555556$ |
| $r_2=3.6$ | $1$ | $0.3333333333$ | $0.2500000000$ | $0.0582407407$ |
| $r=8.5$ | $1$ | $0.2083333333$ | $0.1250000000$ | $0.2557352941$ |

The low-quality purchase payoff is strictly negative in all four rows. At $r=3$, the observed flow details are

| Flow | Unconditional probability | Posterior | Entry | Price |
|---:|---:|---:|---:|---:|
| $-1$ | $1/6$ | $0$ | $0$ | $0.4166666667$ |
| $0$ | $1/3$ | $1/2$ | $1/4$ | $0.6145833333$ |
| $1$ | $1/3$ | $1/2$ | $1/4$ | $0.6145833333$ |
| $2$ | $1/6$ | $1$ | $1$ | $1.5416666667$ |

**Analytical interpretation of these diagnostics.** Here $c_L=1>g_L(r)$ throughout $1<r<10$. The revealing low flow therefore deters low-cost entry. Yet $B_r(1/3)>1$ throughout that interval: its limiting minimum is $1.6875$. Claim 6 rules out all additional price-pool equilibria. The canonical equilibrium remains unique under the prescribed investor rule.

Expensive entry at the prior is absent throughout this interval. Also, $c_L<B_r(1/2)$ throughout it. The exact equilibrium path is therefore

$$
r_T=1.973212111192934401\ldots,
\qquad
r_C^D=7.968626966596885886\ldots,
$$

$$
(\mathsf E,\mathsf O_H)=
\begin{cases}
(1/4,1/8),&1<r\le r_T,\\
(1/3,1/4),&r_T<r\le r_C^D,\\
(5/24,1/8),&r_C^D<r<10.
\end{cases}
$$

The last row lies **below** baseline entry $\rho=1/4$. Expensive preparation disappears, but low-cost preparation remains absent at the revealing low flow.

The printed grid gives:

| $r$ | Equilibrium $\beta_H$ under the prescribed rule | $\mathsf E$ | $\mathsf O_H$ |
|---:|---:|---:|---:|
| $1.05,1.2,1.5,1.8,1.95$ | $0$ | $0.25$ | $0.125$ |
| $r_T$ | $0$ | $0.25$ | $0.125$ |
| $2,2.5,3,3.6,5,7.9$ | $1$ | $1/3$ | $0.25$ |
| $r_C^D$ | $1$ | $1/3$ | $0.25$ |
| $8,8.5,9.9$ | $1$ | $5/24$ | $0.125$ |

At $r_T$, conventional indifference permits all $\beta\in[0,1]$. Claim 7 gives their outcomes, including the loss of low-cost entry at the lower flow. The script prints examples:

| $\beta_H$ at $r_T$ | $\mathsf E$ | $\mathsf O_H$ |
|---:|---:|---:|
| $0$ | $0.25$ | $0.125$ |
| $0.25$ | $0.28125$ | $0.15625$ |
| $0.5$ | $0.3125$ | $0.1875$ |
| $0.75$ | $0.34375$ | $0.21875$ |
| $1$ | $1/3$ | $0.25$ |

Entry need not increase along this mixed continuum. The low-cost entrant exits after a sufficiently unfavorable lower-flow posterior. The full-purchase point therefore has less entry than the displayed $\beta=0.75$ point.

### A variant that satisfies the discrete proposition

Change only $c_L$ to $0.02$ and choose the later comparison strength $r_2=8.5$. Retain $r_0=1.2$ and $r_1=3$. The conditions (A1-D)–(A3-D) then hold strictly.

| Strength | $\beta_H$ | $\mathsf E$ | $\mathsf O_H$ |
|---:|---:|---:|---:|
| $1.2$ | $0$ | $0.25$ | $0.125$ |
| $3$ | $1$ | $0.375$ | $0.25$ |
| $8.5$ | $1$ | $0.25$ | $0.125$ |

At $r=3.6$, this variant still has entry $0.375$. Lower cost restores the floor. It does not restore the paper's early expensive-entry ceiling.

For the presence extension at $r=3$ and $c_L=0.02$, the script gives:

| Presence $\lambda$ | Lower posterior | $\mathsf E$ | $\mathsf O_H$ |
|---:|---:|---:|---:|
| $0.1$ | $0.4736842105$ | $0.2625$ | $0.1375$ |
| $0.5$ | $1/3$ | $0.3125$ | $0.1875$ |
| $0.9$ | $0.0909090909$ | $0.3625$ | $0.2375$ |
| $1$ | $0$ | $0.375$ | $0.25$ |

## 6. Open issues and risks

1. **Analytical:** The original benchmark does not establish the requested three-point pattern. It gives $0.25\to1/3\to1/3$ at $1.2,3,3.6$. At later strengths, entry falls below $\rho$ because its low-cost floor fails.
2. **Analytical:** The strong uniqueness result needs a stated scope. Equal noise and the floor give unique prices and entry. Without the floor, Claim 6 permits extra price equilibria. Unequal noise permits coexistence even under the floor.
3. **Analytical:** The prescribed investor tie rule excludes every genuine mixed order. Under some unequal noise laws, it removes the only conventional equilibrium. A general-noise extension should permit mixtures at indifference.
4. **Analytical:** Full revelation can prevent the final return within $r<h$. The condition $c_H>h/2-p^2/(2h)$ is necessary for that return when the floor holds.
5. **Analytical:** A fixed flow experiment need not imply a fixed price experiment outside the floor. Claim 9 gives a concrete failure of the stronger assertion.
6. **Open:** The empirical or institutional case for exactly equal noise probabilities needs separate support. This memo gives a tractable benchmark, not an estimate of noise demand.
7. **Open:** General noise has an exact finite characterization, but no universal one-cutoff theorem. Further restrictions on noise and participation would be needed for such a theorem. Claims 10–11 already rule it out without restrictions.
8. **Open:** The author must decide whether certain revelation and the resulting step changes fit the intended sale interval. This is a model choice, not a computational issue.

No result in this memo rests on a conjecture. The analytical scope and the numerical diagnostics are stated separately.

## 7. Recommendation

1. Present equal-noise purchases as a transparent alternative benchmark. Use the exact threshold $\rho\Delta_T/3=k$ and state the investor tie rule.
2. State price sufficiency explicitly. Use $c_L<g_L$, or prove the weaker condition for the particular parameter region. Do not assume that the challenger sees flow.
3. Use conditions (A1-D)–(A3-D) for a three-strength proposition. Declare the later $r_2$ and smaller $c_L$ as changed primitives.
4. Keep the original benchmark as a separate comparison. Its failed floor and later ceiling are substantive results.
5. Include the unequal-noise formula and a multiplicity example in an appendix. Permit conventional mixtures if the extension needs equilibrium existence.
6. Retain the Laplace model if the paper needs orders over an interval or a uniqueness argument that survives a broader class of noise laws. The discrete benchmark answers the supervisor's tractability question, but changes the information mechanism.

## 8. Plain summary

The buy-only model can reproduce the paper's main message. A stronger incumbent makes information more valuable to an investor. The investor starts to buy after good news. A sufficiently high price then attracts an expensive challenger.

Equal noise makes the proof short. The two interior flows reveal nothing, even when the investor mixes. The largest flow reveals good news. Under full purchases, the smallest flow reveals bad news. The investor earns its profit only at the interior flows.

A single threshold separates no trade from purchases when cheap preparation always occurs and expensive preparation fails at the prior. There is no coexistence interval in that region. If indifferent investors may mix, all purchase probabilities are possible exactly at the threshold.

The original numerical benchmark changes. Entry is $0.25$, $1/3$, and $1/3$ at the paper's three strengths. Full revelation keeps expensive preparation profitable for much longer. Bad news also deters the nominally cheap challenger.

A smaller low cost and a later third strength restore the exact rise and return. Unequal noise can restore multiplicity. The author should treat equal noise as a useful discrete benchmark, with its assumptions stated clearly.
