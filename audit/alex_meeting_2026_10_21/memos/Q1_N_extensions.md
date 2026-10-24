# Point 1: Reading N, extensions N2 and N3

## 1. Question and reading

Nature draws the challenger's value distribution. The challenger does not choose it. The investor first observes its class, or its exact value in N3. Preparation reveals the value and permits a bid.

This memo gives an independent two-type cross-check. It then studies several classes and exact value information. No other workstream supplies a premise for the derivations.

The main conclusions have three parts.

- **Analytical:** The reserve adds a boundary term if class supports extend below it. That term can reverse the target-spread comparison.
- **Analytical:** Collinearity characterizes a reduction that works for arbitrary belief vectors. Equilibrium incentives supply a different route to sufficiency under the paper's assumptions.
- **Analytical:** A Proposition 2 analog holds for two separated groups of target proceeds. Its uniform order bound does not cover a general connected continuum.

Sources read: `overleaf/paper/main.tex`, Sections 2–4; Section 6.3, especially lines 1040–1050; Appendices A.1–A.2 and A.5. All source references below refer to this local manuscript. No external literature claim is required.

## 2. Formal setup

Let $R\sim F$ be the incumbent's value. Assume that $F$ is continuous on $[0,\bar r]$. Extend $F$ by zero below zero and by one above $\bar r$.

The reserve is $p>0$. A bid at $p$ is admissible. The target receives zero if neither bid meets $p$.

For N2, nature draws $j\in\{1,\ldots,J\}$ with probabilities $\pi_j>0$. The probabilities sum to one. Conditional on $j$, the value has cdf $G_j$ and a finite first moment. The class cdfs can have atoms, overlap, or extend below $p$.

The investor observes $j$. The challenger knows neither $j$ nor $\theta$. Preparation reveals $\theta$, rather than an additional public signal.

The incumbent, preparation cost, and noise demand are independent of $(j,\theta)$. Conditional on $j$, the investor's order carries no further information about $\theta$.

The investor can use a mixed order law $\sigma_j$ on $[-1,1]$. Noise has the paper's Laplace density with $b>1$. The investor pays $k|q|$, where $k>0$, and has no initial stake.

The challenger sees the price and its independent cost. It does not see flow. As in the paper, preparation occurs at cost indifference.

Write

$$
t_0=\mathbb E[p\mathbf1\{R\ge p\}],\qquad
t_F(\theta)=\mathbb E[V_T\mid\theta,\text{ preparation}],\qquad
\gamma_F(\theta)=\mathbb E[(\theta-\max\{p,R\})_+].
$$

Class means are $t_j=\mathbb E_j[t_F(\theta)]$ and $g_j=\mathbb E_j[\gamma_F(\theta)]$. Reserve admissibility has probability $s_j=1-G_j(p-)$.

Use $\mu_j(x)=\Pr(j\mid X=x)$ and $\nu_j(P)=\Pr(j\mid P)$. Define

$$
T_X=\sum_j\mu_jt_j,\qquad B_X=\sum_j\mu_jg_j,\qquad
B_P=\sum_j\nu_j(P)g_j=\mathbb E[B_X\mid P].
$$

The last equality follows from the tower property. It does not presume price sufficiency.

Most results below impose a **uniform entry floor**: low-cost preparation occurs at every feasible price. Then

$$
e(P)=\rho+(1-\rho)\mathbf1\{B_P\ge c_H\}\ge\rho>0.
$$

This floor must be proved from posterior bounds. It is not a consequence of preparation at the prior.

For N3, replace the class signal with exact observation of $\theta$. Its prior is $G=\sum_j\pi_jG_j$. The original class then has no separate payoff role.

## 3. Results

### Claim 1. General auction formulas, with the reserve boundary — **analytical**

For a given pair $(R,\theta)$, target revenue after preparation is

$$
V_1(R,\theta)
=p\mathbf1\{\max(R,\theta)\ge p\}
+(\min(R,\theta)-p)_+.
$$

The first term is the reserve payment when a sale occurs. The second term adds the competing bid above the reserve. Without preparation, revenue is $V_0(R)=p\mathbf1\{R\ge p\}$.

If $\theta<p$, the challenger changes neither revenue nor its own profit. If $\theta\ge p$, a sale occurs for sure. Indicator integrals therefore give

$$
\begin{aligned}
t_0&=p[1-F(p)],\\
t_F(\theta)
&=\begin{cases}
t_0,&\theta<p,\\
p+\displaystyle\int_p^\theta[1-F(u)]\,du,&\theta\ge p,
\end{cases}\\
\gamma_F(\theta)
&=\begin{cases}
0,&\theta\le p,\\
\displaystyle\int_p^\theta F(u)\,du,&\theta>p.
\end{cases}
\end{aligned} \tag{N.1}
$$

For example, $(\theta-\max\{p,R\})_+=\int_p^\theta\mathbf1\{R<u\}\,du$ when $\theta\ge p$. Tonelli's theorem gives the profit formula. The same argument applies to $(\min(R,\theta)-p)_+$.

A class average now gives

$$
\begin{aligned}
t_j
&=t_0+pF(p)s_j
+\int_p^\infty[1-F(u)][1-G_j(u)]\,du,\\
g_j
&=\int_p^\infty F(u)[1-G_j(u)]\,du.
\end{aligned} \tag{N.2}
$$

The left limit $G_j(p-)$ includes an atom at the reserve correctly. An atom at $p$ contributes to sale revenue but contributes no challenger profit.

For two types, put $D(u)=G_L(u)-G_H(u)$ and $D_p=G_L(p-)-G_H(p-)$. Then

$$
\begin{aligned}
\Delta_T(F)&=t_H-t_L
=pF(p)D_p+\int_p^\infty[1-F(u)]D(u)\,du,\\
\Gamma(F)&=g_H-g_L
=\int_p^\infty F(u)D(u)\,du\\
&=\int\gamma_F(\theta)\,d(G_H-G_L)(\theta).
\end{aligned} \tag{N.3}
$$

These equations prove the requested spread and profit-gap identities, with one correction. The proposed spread integral omits $pF(p)D_p$. The proposed profit integral needs $\gamma_F(\theta)=0$ below $p$; a literal integral from $p$ down to $\theta$ is incorrect.

If both classes lie above the reserve, $D_p=0$. Equation (N.3) then has the proposed integral form. Also, $t_F(\theta)+\gamma_F(\theta)=\theta$ for $\theta\ge p$, by (N.1).

### Claim 2. Type ranking and incumbent strength are separate comparisons — **analytical**

Suppose $G_H$ first-order dominates $G_L$. Then $D(u)\ge0$ and $D_p\ge0$. Equations (N.2)–(N.3) imply $t_H\ge t_L$ and $g_H\ge g_L$.

Strict target ranking needs a positive boundary term or a positive survival integral. Strict profit ranking needs a positive profit integral. FOSD alone permits $t_H=t_L$, for example when both classes always exceed $\bar r$.

Now strengthen the incumbent from $F_0$ to $F_1$, with $F_1\le F_0$. Put $\delta F=F_0-F_1\ge0$. Direct subtraction yields

$$
\begin{aligned}
g_j(F_1)-g_j(F_0)
&=-\int_p^\infty\delta F(u)[1-G_j(u)]\,du\le0,\\
\Gamma(F_1)-\Gamma(F_0)
&=-\int_p^\infty\delta F(u)D(u)\,du\le0,\\
\Delta_T(F_1)-\Delta_T(F_0)
&=-p\delta F(p)D_p+\int_p^\infty\delta F(u)D(u)\,du.
\end{aligned} \tag{N.4}
$$

Thus each class's acquisition profit falls. Its posterior average falls at every fixed belief. Under class FOSD, the profit gap also falls.

The target-spread effect has an ambiguous sign when reserve admissibility differs. Its first term is negative; its second term is positive. This ambiguity concerns auction primitives, before any equilibrium response.

Here is an exact counterexample. Set $p=1$, $G_L=U[0,0.5]$, and $G_H=U[2,3]$. Move the incumbent from $U[0,0.5]$ to $U[1,1.5]$.

The weak incumbent never meets the reserve. Hence $t_L=0$, $t_H=1$, and $\Delta_T=1$. The strong incumbent always meets the reserve. Hence $t_L=1$, $t_H=1.25$, and $\Delta_T=0.25$.

The incumbent shift is FOSD. The class shift is also FOSD. Nevertheless, the target spread falls from $1$ to $0.25$.

Two useful weaker assumptions preserve the paper's opposition:

1. Equal reserve admissibility, $D_p=0$, and $D(u)\ge0$ for $u\ge p$ suffice. No ranking below $p$ is needed.
2. If $F_0(p)=F_1(p)$, the same tail ranking suffices even when $D_p>0$.

For a fixed $F$, the two scalar inequalities in (N.3) suffice for strict payoff ranking. Full class FOSD is stronger than necessary. For a specified incumbent shift, the last line of (N.4) is the exact spread condition.

Each individual $t_j$ still rises under incumbent FOSD. Indeed, (N.2) gives

$$
t_j(F_1)-t_j(F_0)
=p\delta F(p)G_j(p-)
+\int_p^\infty\delta F(u)[1-G_j(u)]\,du\ge0.
$$

The ambiguity concerns the difference between two rising revenues.

### Claim 3. Two-type inference and residuals with an unequal prior — **analytical**

Let $\pi=\Pr(H)\in(0,1)$ and $K=\exp(2/b)$. The Laplace likelihood bounds give

$$
m_\pi=\frac{\pi}{\pi+K(1-\pi)}
\le\mu_X\le
M_\pi=\frac{K\pi}{K\pi+1-\pi}. \tag{N.5}
$$

The price posterior has the same bounds by conditional expectation. If $g_H>g_L$, the condition $c_L<g_L+m_\pi(g_H-g_L)$ proves the entry floor.

Assume also $\Delta_T>0$. Conditional competitive pricing then gives

$$
P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X],\qquad
\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}.
$$

The denominator is positive. The price therefore reveals $\mu_X$, exactly as in Proposition A.2. This proof permits values below $p$.

For construction, entry rises with $\mu$ and $t_L-t_0\ge0$. Hence the proposed price rises strictly with $\mu$. The argument uses payoff ranking, rather than disjoint value supports.

The investor's residuals are

$$
A_H=e(P)\Delta_T(1-\mu_X),\qquad
A_L=e(P)\Delta_T\mu_X.
$$

Their common lower bound is $\rho\Delta_T a_\pi$, where

$$
a_\pi=\min\{m_\pi,1-M_\pi\}.
$$

Their upper bound is $\Delta_T$. The paper's translation argument therefore gives

$$
U'(s)\ge(1-1/b)\rho\Delta_Ta_\pi-k.
$$

These formulas provide the independent two-type cross-check. They also show which prior replaces $1/2$ and which lower bound replaces $m$.

For a two-economy comparison, sufficient conditions are

$$
\begin{gathered}
c_L<\min_{s=0,1}B_{F_s}(m_\pi),\qquad
B_{F_0}(\pi)<c_H<B_{F_1}(M_\pi),\\
\Delta_T(F_0)<k<(1-1/b)\rho a_\pi\Delta_T(F_1).
\end{gathered} \tag{N.6}
$$

Here both economies must satisfy $\Delta_T>0$ and $g_H>g_L$. The weak economy has unique zero orders; the strong economy has unique full orders. The proof excludes all smaller and mixed orders by the displayed residual bounds, then constructs the strictly ordered price schedule.

The strong upper posterior occurs on the positive Laplace tail. Its strict cost inequality adds high-cost preparation with positive probability. A third economy needs its own floor, order bound, and expensive-entry ceiling.

High-class ownership requires an extra condition. Let

$$
w_H(F)=\int_{[p,\infty)}F(\theta)\,dG_H(\theta).
$$

If conditional entry in class $H$ is $e_H$, its acquisition probability is $\pi e_Hw_H(F)$. Stronger incumbents reduce $w_H(F)$. Thus greater preparation does not alone prove greater high-class ownership. The paper avoids this issue through $h>r$.

### Claim 4. Every pairwise posterior ratio remains bounded for N2 — **analytical**

Define $a_j(x)=\int f(x-q)\,d\sigma_j(q)$. For every pair of orders, the triangle inequality gives

$$
K^{-1}\le\frac{f(x-q)}{f(x-q')}\le K.
$$

Integrate against $d\sigma_j(q)d\sigma_l(q')$. Bayes' rule then gives, for every pair of classes,

$$
K^{-1}\frac{\pi_j}{\pi_l}
\le\frac{\mu_j(x)}{\mu_l(x)}
\le K\frac{\pi_j}{\pi_l}. \tag{N.7}
$$

No pure or monotone order assumption enters this proof. The inequalities also hold for price posteriors: condition the equivalent linear inequalities on $P$.

In particular,

$$
\frac{\pi_j}{\pi_j+K(1-\pi_j)}
\le\mu_j,\nu_j\le
\frac{K\pi_j}{K\pi_j+1-\pi_j}.
$$

These coordinate bounds are not independent restrictions. Use the joint set

$$
\mathcal M_\pi=
\left\{\mu\in\Delta^{J-1}:
K^{-1}\le\frac{\mu_j/\pi_j}{\mu_l/\pi_l}\le K
\text{ for all }j,l\right\}. \tag{N.8}
$$

A sufficient floor condition is $c_L<\underline B$, where $\underline B=\min_{\mu\in\mathcal M_\pi}\mu\cdot g$. It applies before any price inversion. The set is a posterior bound; an arbitrary strategy need not attain every member.

### Claim 5. What the price identity does, and what collinearity does — **analytical**

Under the floor, common entry conditional on price gives

$$
P=t_0+e(P)(T_X-t_0),\qquad
T_X=t_0+\frac{P-t_0}{e(P)}. \tag{N.9}
$$

Thus the price always reveals $T_X$. Equation (N.9) alone says nothing about the other linear functional $B_X$.

For an arbitrary set of posterior vectors $S$, the exact condition for $B$ to be a function of $T$ is

$$
\mu,\eta\in S,\quad \mu\cdot t=\eta\cdot t
\quad\Longrightarrow\quad
\mu\cdot g=\eta\cdot g. \tag{N.10}
$$

For the whole simplex, or any open neighborhood of $\pi$, this condition holds if and only if

$$
g_j=a+d\,t_j\quad\text{for every }j. \tag{N.11}
$$

To prove necessity, let $v\cdot\mathbf1=v\cdot t=0$. Small vectors $\pi\pm\epsilon v$ remain in the neighborhood. Condition (N.10) forces $v\cdot g=0$. Thus $g$ lies in the row span of $(\mathbf1,t)$. This is (N.11). Sufficiency follows from $B=a+dT$.

The joint bound set $\mathcal M_\pi$ contains such a neighborhood. Hence posterior ratio bounds alone do not remove this requirement. A vertical set of payoff points does not qualify: if all $t_j$ coincide, all $g_j$ must coincide for (N.10).

For existence by direct price construction, $d\ge0$ is a useful sufficient restriction. Then $e(T)$ is nondecreasing, $T-t_0\ge0$, and

$$
P(T_2)-P(T_1)
=e(T_2)(T_2-T_1)+[e(T_2)-e(T_1)](T_1-t_0)
\ge\rho(T_2-T_1)>0.
$$

Collinearity with $d<0$ still identifies the profit statistic. It does not ensure this monotone price construction; entry can produce a downward jump.

An order supplies another sufficient condition on a given order profile. Assume $t_1\le\cdots\le t_J$, with $t_1<t_J$. Suppose that the conditional flow densities satisfy the monotone likelihood ratio property in that order.

For $x_1<x_2$, put $r_j=a_j(x_2)/a_j(x_1)$. Then $r_j$ is nondecreasing, and

$$
T_X(x_2)-T_X(x_1)
=\frac{\operatorname{Cov}_{\mu(x_1)}(t_j,r_j)}
{\mathbb E_{\mu(x_1)}r_j}.
$$

All classes have positive posterior mass. If the posterior changes, $r_1<r_J$, so the covariance is strictly positive. Thus $T$ identifies the posterior along that curve. If $g_j$ shares the order, $B$ also rises along the curve, and the price construction is strictly ordered.

Pure orders that rise with class satisfy this likelihood ratio condition. For $q_j\le q_l$ and $x_1<x_2$, the Laplace location family gives

$$
f(x_2-q_l)f(x_1-q_j)
\ge f(x_1-q_l)f(x_2-q_j).
$$

This follows because $q\mapsto f(x_2-q)/f(x_1-q)$ is nondecreasing. It also holds for mixtures with ordered supports, by integration. Mere FOSD between mixed order laws does not supply this argument.

**A threshold needs less than a profit statistic.** At a fixed $T$, take a compact feasible set, such as $\mathcal M_\pi$. Define the minimum and maximum $B$ on its level set. The high-cost decision is constant there exactly when

$$
B_{\min}(T)\ge c_H\quad\text{or}\quad B_{\max}(T)<c_H. \tag{N.12}
$$

This is weaker than (N.10). The strict inequality in the second case respects preparation at indifference.

The price can also encode an entry decision in its level. For an arbitrary flow experiment, define $e^X$ from $B_X$ and propose $P^X=t_0+e^X(T_X-t_0)$. This flow-based continuation is valid exactly when its high-cost decision is measurable from $P^X$, up to null sets.

For sufficiency, every posterior in a price fiber then has $B_X$ on the same side of $c_H$. Its conditional average has the same decision. Necessity follows because the challenger must use one decision at each observed price.

For finite costs, a useful special case is disjoint price ranges:

$$
t_0+\rho(t_{\max}-t_0)<t_{\min}. \tag{N.13}
$$

Low-only entry prices and full-entry prices then cannot coincide. Within either regime, equal prices imply equal $T$ and the same entry decision. Thus the flow-based entry policy is implementable, even if $B_X$ itself is not recovered.

Consequently, no necessary condition based only on collinearity characterizes entry from the actual price in every experiment. The exact conditions are (N.10) for the statistic, (N.12) for a decision based on $T$, and the price-fiber condition for the actual continuation.

### Claim 6. Counterexamples to an arbitrary-profile extension of A.2 — **analytical**

First consider $R\sim U[0,3]$, $p=1/2$, and values $(1,2,10)$. The payoff vectors are

$$
t=\frac1{24}(21,33,37),\qquad
g=\frac1{24}(3,15,203).
$$

Take $\pi=(9,9,42)/60$ and two posterior vectors

$$
\mu^+=(8,13,39)/60,\qquad
\mu^-=(10,5,45)/60.
$$

Direct substitution gives

$$
\mu^+\cdot t=\mu^-\cdot t=17/12,\qquad
\mu^+\cdot g=113/20<6<77/12=\mu^-\cdot g.
$$

For $b=2$, both vectors lie inside $\mathcal M_\pi$. Their largest likelihood-weight ratios are $13/8$ and $2$, both below $\exp(1)$. This refutes the claim that the bounds alone make $B$ a function of $T$. It does not assert that these two vectors arise in one Laplace experiment.

A second example gives an actual Laplace price collision. Retain $(p,r,b,\rho)=(1/2,3,2,1/4)$. Use three uniform distributions:

$$
G_1=U[0,0.1],\qquad G_2=U[3,3.1],\qquad
G_3=U[101.95,102.05].
$$

Their exact payoffs are

$$
t=(5/12,37/24,37/24),\qquad
g=(0,181/120,12055/120).
$$

Set $c_L=0$, $c_H=1.61$, and

$$
a=\frac b4\log(117/17)<1,\qquad
O=\sqrt{\frac{183}{17}\frac{61}{39}},\qquad
\alpha=\frac O{1+O}.
$$

Use prior $\pi=(60\alpha/61,1-\alpha,\alpha/61)$ and orders $(a,-a,a)$. The two extreme flow tails have posteriors

$$
\mu^{\mathrm{pos}}=(0.9,0.085,0.015),\qquad
\mu^{\mathrm{neg}}=(0.6,0.39,0.01).
$$

To verify these vectors, the prior odds of the order-$a$ group equal $O$. The positive and negative tails multiply these odds by $\exp(2a/b)$ and $\exp(-2a/b)$. The resulting group probabilities are $0.915$ and $0.61$. Inside that group, class probabilities retain the ratio $60:1$.

The corresponding gross profits are

$$
B_{\mathrm{pos}}=1.63508333\ldots>1.61,
\qquad B_{\mathrm{neg}}=1.59283333\ldots<1.61.
$$

Thus entry based on flow is $1$ and $\rho$, respectively. Yet its proposed prices coincide:

$$
\begin{aligned}
P^{X}_{\mathrm{pos}}&=T_{\mathrm{pos}}=127/240,\\
P^{X}_{\mathrm{neg}}&=t_0+\rho(T_{\mathrm{neg}}-t_0)
=5/12+\tfrac14(13/15-5/12)=127/240.
\end{aligned}
$$

Both tails have positive probability. The challenger cannot choose entry $1$ and entry $\rho$ at the same price. Its posterior at that price combines both tails, while the market maker has distinct flow posteriors.

The construction from flow therefore fails Bayesian consistency. It is **not** an equilibrium counterexample. In particular, its orders violate the incentive restriction in Claim 7. This distinction is essential: a failed flow-based construction does not establish failure in equilibrium.

### Claim 7. Equilibrium incentives restore price sufficiency under the maintained assumptions — **analytical**

This result uses $b>1$, the order bound, the positive entry floor, and common entry conditional on price. It does not need collinearity. It also permits equal target proceeds across some classes.

Fix any candidate equilibrium schedule, including its price-based entry. For a deviation $q$, let

$$
\begin{aligned}
A(q)&=\int e(P(x))f(x-q)\,dx,\\
H(q)&=qA(q),\\
K_0(q)&=q\int e(P(x))T_X(x)f(x-q)\,dx+k|q|.
\end{aligned}
$$

The class-$j$ investor's payoff is

$$
U_j(q)=t_jH(q)-K_0(q). \tag{N.14}
$$

This follows from (N.9): its residual at flow $x$ is $e(P(x))[t_j-T_X(x)]$. The constants $t_0$ cancel. Schedules remain fixed during a unilateral deviation, as in Section 2.4.

The translation bound $|f'|\le f/b$ gives $|A'(q)|\le A(q)/b$ almost everywhere. Therefore

$$
H'(q)=A(q)+qA'(q)
\ge(1-|q|/b)A(q)
\ge(1-1/b)\rho>0. \tag{N.15}
$$

Absolute continuity permits integration of this bound across any two orders. Hence $H$ is strictly increasing, including across entry jumps.

If $t_j<t_l$ and optimal orders satisfy $q_j>q_l$, add their two optimality inequalities. Equation (N.14) would imply

$$
(t_l-t_j)[H(q_l)-H(q_j)]\ge0,
$$

which contradicts (N.15). Thus every optimal order for the lower payoff is below every optimal order for the higher payoff. This restriction also applies to supports of equilibrium mixtures.

Now fix $x_1<x_2$. On the joint equilibrium support of class and order, define

$$
r(q)=\frac{f(x_2-q)}{f(x_1-q)}.
$$

The Laplace family makes $r(q)$ nondecreasing. The optimal-order restriction makes class proceeds and orders move in the same weak order. Under the posterior at $x_1$,

$$
T_X(x_2)-T_X(x_1)
=\frac{\operatorname{Cov}_{x_1}(t_j,r(q))}
{\mathbb E_{x_1}[r(q)]}\ge0. \tag{N.16}
$$

The covariance equals half the expectation of
$(t_j-t_l)[r(q)-r(q')]$ for two independent posterior draws. Every product is nonnegative. This proves the inequality without a pure-strategy assumption.

If the proceeds are nonconstant, equality forces $r(q)$ to be constant on the entire joint support. Here is the reason for the strictness step. Each pair with distinct proceeds must have the same $r$. Any two orders with equal proceeds can each be compared with a class of different proceeds. They must then share that same $r$ as well.

Since $f$ is positive, the posterior retains every class and every order in its equilibrium support. Hence $T_X(x_1)=T_X(x_2)$ implies equality of the whole class posterior at those flows. Equal proceeds across some classes cause no exception.

The functions $a_j$ and $T_X$ are continuous. The monotone function $T_X$ has interval level sets, and the posterior is constant on each such set. Thus each $\mu_j$ is a measurable function of $T_X$.

Finally, (N.9) makes $T_X$ measurable from price. The tower property gives

$$
\nu_j(P)=\mathbb E[\mu_j(X)\mid P]=\mu_j(X)
\quad\text{almost surely}. \tag{N.17}
$$

If all $t_j$ coincide, the residual is zero for every class and every order. Positive $k$ forces zero orders. Both flow and price then retain the prior, so (N.17) also holds.

**Scope.** Claim 7 proves sufficiency in every equilibrium of this model with the stated floor. It does not prove equilibrium existence for every parameter vector. It also does not validate an arbitrary proposed order profile.

This result explains why collinearity is not necessary here. Collinearity permits arbitrary beliefs. Optimal orders restrict beliefs to a curve on which expected proceeds reveal the full posterior. Claims 5–6 concern the former question; Claim 7 answers the equilibrium question.

### Claim 8. A precise many-type analog of Proposition 2 — **analytical**

A useful sufficient theorem allows several classes inside each of two separated groups. It does not require collinear class payoffs.

Consider incumbent cdfs $F_0,F_1$, where $F_1$ first-order dominates $F_0$. Keep all other primitives fixed. For each economy, define

$$
\begin{aligned}
\underline T_s&=\min_{\mu\in\mathcal M_\pi}\mu\cdot t_s,&
\overline T_s&=\max_{\mu\in\mathcal M_\pi}\mu\cdot t_s,\\
\underline B_s&=\min_{\mu\in\mathcal M_\pi}\mu\cdot g_s,&
\overline B_s&=\max_{\mu\in\mathcal M_\pi}\mu\cdot g_s.
\end{aligned}
$$

Choose a nonempty partition $L,H$. Put $\alpha=\sum_{j\in H}\pi_j$, and let $\bar t_{s,D},\bar g_{s,D}$ denote prior means within group $D$.

Assume $\bar t_{1,H}>\bar t_{1,L}$ and $\bar g_{1,H}>\bar g_{1,L}$. Define

$$
\begin{aligned}
D_0&=\max_j t_{0,j}-\min_jt_{0,j},\\
d_1&=\min\left\{
\underline T_1-\max_{j\in L}t_{1,j},\ 
\min_{j\in H}t_{1,j}-\overline T_1
\right\}>0.
\end{aligned} \tag{N.18}
$$

The subscript $0,j$ here means economy zero and class $j$. It does not denote no-entry revenue.

The sufficient conditions are

$$
\begin{gathered}
c_L<\min\{\underline B_0,\underline B_1\},\qquad
\pi\cdot g_0<c_H,\\
\bar g_{1,L}+M_\alpha(\bar g_{1,H}-\bar g_{1,L})>c_H,\\
D_0<k<(1-1/b)\rho d_1.
\end{gathered} \tag{N.19}
$$

Then the weak economy has unique zero orders and entry $\rho$. The strong economy has unique orders $q_j=-1$ on $L$ and $q_j=1$ on $H$. Its price is informative, and entry exceeds $\rho$.

**Proof: weak economy.** The residual is $e(P)(t_{0,j}-T_X)$. Its absolute value is at most $D_0$. Any nonzero order earns at most $|q|(D_0-k)<0$. Hence every class chooses zero, including under mixed candidates. The prior cost conditions give entry $\rho$ and a constant competitive price.

**Proof: strong economy.** Every posterior lies in $\mathcal M_\pi$. Thus every low-group residual is negative with magnitude at least $\rho d_1$. Every high-group residual is positive with the same lower bound. Wrong signs lose before costs.

For a correctly signed magnitude $s$, define its expected residual magnitude $R_j(s)$. Density translation gives $|R_j'(s)|\le R_j(s)/b$. Therefore

$$
U_j'(s)\ge(1-1/b)\rho d_1-k>0.
$$

The full correct order strictly dominates every smaller magnitude. This argument applies to every candidate schedule, so it excludes other pure and mixed order outcomes.

Under the forced profile, flow contains information only about group membership. With $\lambda=\Pr(H\mid X)$,

$$
\begin{aligned}
T_X&=\bar t_{1,L}+\lambda(\bar t_{1,H}-\bar t_{1,L}),\\
B_X&=\bar g_{1,L}+\lambda(\bar g_{1,H}-\bar g_{1,L}).
\end{aligned}
$$

Both expressions rise with $\lambda$. The price construction from Claim 3 is strictly increasing. It supplies a Bayesian price and entry schedule, while the global bound proves investor optimality. The positive tail reaches $M_\alpha$, so the strict cost inequality adds expensive preparation with positive probability.

The theorem retains two informed order sizes. It permits several different class distributions, but it does not produce a separate order for each class.

If $F_2$ further strengthens the incumbent, the return to entry $\rho$ follows under three extra conditions:

$$
c_L<\underline B_2,\qquad
k<(1-1/b)\rho d_2,\qquad
\overline B_2<c_H. \tag{N.20}
$$

Use the same partition in $d_2$. The previous order proof then forces the same full orders. The last inequality excludes every expensive entrant. A stronger incumbent alone does not guarantee all three conditions.

The theorem has a nonempty strict region. At two point values, $d_1=\min(m_\alpha,1-M_\alpha)\Delta_T$. The binary benchmark supplies an exact starting point. Its weak range is $1/60<k=1/50$. Its strong marginal bound is $m/12>1/48>1/50$, since $\exp(1)<3$.

Its weak prior profit is $1153/240<6$. Its strong upper profit is $1/8+25M/3>6$, since $\exp(1)>5/2$. At $r_2=18/5$, its minimum profit exceeds $763/360>1$. Its maximum profit is $5/48+1451M/180<6$, since $\exp(1)<4245/1559$.

The bounds $5/2<\exp(1)<2719/1000<4245/1559$ follow from the exponential series. For the upper bound, sum through $1/6!$ and bound the remaining sum by $1/4410$. Thus these premises do not rely on decimal output.

Split either class into nearby classes. All payoff ranges, posterior extrema, and strict margins vary continuously, so sufficiently small splits preserve (N.19)–(N.20). The binary target spread rises with incumbent strength, so the third-economy marginal bound also exceeds the strong bound before the split.

**Ownership limitation.** The theorem proves preparation and information conclusions. It also proves increased high-group ownership if every high-group value exceeds the incumbent's support in both economies. Otherwise the acquisition probability needs a separate comparison, as in Claim 3.

### Claim 9. Why the same proof does not cover arbitrary intermediate classes — **analytical**

The residual in class $j$ is $e(P)[t_j-T_X]$. If $t_j$ lies inside $[\underline T,\overline T]$, its sign can change with flow. There is no strategy-independent positive lower bound for one fixed order direction.

Therefore the step $|R_j'|\le R_j/b$ for a nonnegative residual does not establish full orders for that class. Replacing $R_j$ with an absolute value changes the deviation payoff and is invalid.

Claim 7 still proves price sufficiency. It does not supply this missing incentive bound. A general theorem would need optimal partial orders, zero orders, or additional restrictions on intermediate classes.

Extreme classes can still satisfy a separate bound. For the lowest class, its residual magnitude is at least $\rho(\underline T-t_{\min})$. For the highest class, it is at least $\rho(t_{\max}-\overline T)$. If these gaps are positive and the corresponding marginal bounds exceed $k$, the extremes use full orders. This does not determine intermediate orders.

**Open:** A general uniqueness theorem for the many-class order profile remains unresolved here. **Conjecture:** Price feedback can still produce the entry reversal with intermediate classes that do not satisfy (N.18).

### Claim 10. N3 preserves posterior bounds and the residual formula — **analytical**

Let $G$ be the value prior. Conditional order laws can depend on exact $\theta$. For every pair of values, the conditional flow likelihood ratio remains between $K^{-1}$ and $K$.

For any measurable event $A$ with prior probability $a\in(0,1)$, average the likelihood within $A$ and its complement. Claim 4's argument gives

$$
\frac a{a+K(1-a)}\le\Pr(A\mid X),\Pr(A\mid P)
\le\frac{Ka}{Ka+1-a}. \tag{N.21}
$$

There is no positive lower posterior probability for an individual value with zero prior mass. The event bounds replace the binary bounds.

Define $\mathcal M_G$ as the posterior laws whose likelihood weights relative to $G$ have essential ratio at most $K$. The flow posterior has this property by the pairwise density bound. Its density conditional on price is the conditional average of its flow density. Pairwise linear density inequalities survive that average, as in Claim 4. Thus the price posterior also lies in $\mathcal M_G$.

A sufficient entry floor is

$$
c_L<\inf_{\eta\in\mathcal M_G}\int\gamma_F(\theta)\,d\eta(\theta).
$$

Under this floor,

$$
P=t_0+e(P)(T_X-t_0),\qquad
T_X=\mathbb E[t_F(\theta)\mid X],
$$

and exact-value information gives residual

$$
A_\theta(x)=e(P(x))[t_F(\theta)-T_X(x)]. \tag{N.22}
$$

The residual concerns the target claim, rather than $\gamma_F(\theta)$ or $\theta$ itself. For $\theta\ge\bar r$, all values share $t_F(\theta)=\mathbb E[\max\{p,R\}]$ if $\bar r\ge p$. Their acquisition profits still rise one-for-one with $\theta$.

### Claim 11. N3 price sufficiency survives in equilibrium — **analytical**

For arbitrary posterior laws, exact recovery of the profit statistic from expected target proceeds requires

$$
\gamma_F(\theta)=a+d\,t_F(\theta)\quad G\text{-almost surely}. \tag{N.23}
$$

Necessity follows from a bounded density perturbation. Write $z=(1,t_F)^\top$ and $Q=\mathbb E[zz^\top]$. Target proceeds are bounded. If they are nonconstant, $Q$ is invertible.

For any event $A$, define $v_A=Q^{-1}\mathbb E[z\mathbf1_A]$ and $h_A=\mathbf1_A-v_A^\top z$. Then $h_A$ is bounded and $\mathbb E[zh_A]=0$. Small density changes $1\pm\epsilon h_A$ preserve probability and the target mean. They also satisfy the likelihood-weight bound for sufficiently small $\epsilon$.

Profit-statistic sufficiency forces $\mathbb E[h_A\gamma_F]=0$. Set $(a,d)^\top=Q^{-1}\mathbb E[z\gamma_F]$, which exists because profits are integrable. Substitution gives $\mathbb E[\mathbf1_A(\gamma_F-a-dt_F)]=0$ for every event $A$. Hence (N.23) holds almost surely. If target proceeds are constant, use $h_A=\mathbf1_A-\Pr(A)$; profits must then be constant too. Sufficiency follows by direct expectation of (N.23).

The condition usually fails. Where $p<\theta<\bar r$ and $F$ is continuous,

$$
t_F'(\theta)=1-F(\theta),\qquad \gamma_F'(\theta)=F(\theta).
$$

An affine relation on an interval would require $F(\theta)/(1-F(\theta))=d$ throughout it. A strictly increasing $F$ cannot satisfy that requirement. A high-value plateau with different acquisition profits also violates (N.23).

However, equilibrium orders satisfy Claim 7's increasing-differences restriction with $t_j$ replaced by $t_F(\theta)$. That proof depends only on the common price-based entry schedule and (N.15). Thus larger target proceeds cannot have smaller optimal orders.

The covariance proof also extends. Use the posterior joint law of $(\theta,q)$ and the bounded ratio $r(q)$. Equation (N.16) holds with $t_F(\theta)$ in place of $t_j$.

If the covariance is zero, every pair with distinct target proceeds has equal $r(q)$. Two positive-probability sets with different proceeds then force the same ratio throughout the support, including within any payoff plateau. Thus the entire value posterior is constant on a level set of $T_X$.

The monotone continuous $T_X$ makes these posterior kernels measurable from $T_X$. A countable collection of intervals determines a probability law on the real value space. Apply the argument to each interval, then use (N.9). The posterior given price equals the posterior given flow almost surely.

If target proceeds are constant under the prior, positive $k$ forces zero orders, as before. No price information then exists to lose.

**Scope:** Exact-value observation does not by itself destroy price sufficiency under $b>1$ and the uniform entry floor. It changes the investor's order problem. Without the floor, (N.9) and the strict bound (N.15) need not hold.

### Claim 12. N3 permits monotone orders, but a connected payoff support has a region with no trade — **analytical**

On a support where $t_F(\theta)$ is strictly increasing, all optimal orders rise weakly with $\theta$. A pure selection is monotone. Mixed supports cannot cross across distinct target proceeds. On payoff plateaus, exact values have identical investor preferences, so their orders need not have a strict value order.

A monotone order rule need not be one full-order threshold. Positive $k$ creates a nontrivial region where zero is optimal when the target-payoff support is connected.

Here is a global argument. Fix an equilibrium schedule, and define

$$
A(q)=\int e(P(x))f(x-q)\,dx,\qquad
M(q)=\frac{\int e(P(x))T_X(x)f(x-q)\,dx}{A(q)}.
$$

Claim 11 makes $T_X$ nondecreasing. The Laplace location family has monotone likelihood ratios. Multiplication by the positive function $e(P(x))$ preserves this order. Hence $M(q)$ is nondecreasing in $q$.

For completeness, the change in $M$ between two orders equals a covariance between increasing $T_X(x)$ and their increasing density ratio, under the first weighted law. The covariance identity in Claim 7 proves its sign.

The value-$\theta$ deviation payoff is

$$
U_\theta(q)=qA(q)[t_F(\theta)-M(q)]-k|q|.
$$

Zero is optimal exactly when $t_F(\theta)\in[t_-,t_+]$, where

$$
\begin{aligned}
t_-&=\sup_{q<0}\{M(q)-k/A(q)\},\\
t_+&=\inf_{q>0}\{M(q)+k/A(q)\}.
\end{aligned} \tag{N.24}
$$

This follows by dividing the inequality $U_\theta(q)\le0$ separately for positive and negative $q$. Since $A(q)\le1$ and $M(q)$ is nondecreasing,

$$
t_-\le M(0)-k<M(0)+k\le t_+. \tag{N.25}
$$

Every type with $|t_F(\theta)-M(0)|<k$ therefore strictly prefers zero to every nonzero order. This conclusion uses all deviations, rather than a derivative at zero.

If the target-payoff support is a nondegenerate interval with positive probability in every interior neighborhood, $M(0)$ lies inside it. The posterior is equivalent to the prior because the noise density is positive. Therefore $T_X$ and its weighted mean cannot equal either payoff endpoint. There is positive prior mass in the zero-order region.

Consequently, a connected nondegenerate target-payoff support cannot have the paper's literal full-order outcome for almost every type. This condition holds when values fill an interval strictly inside $(p,\bar r)$ and $F<1$ there. A value interval that crosses the reserve can instead produce a gap in target proceeds through (N.1). Partial orders can also occur, but this memo does not prove their occurrence or uniqueness. A step from sales to zero to purchases is consistent with the order restriction.

### Claim 13. What survives of Proposition 2 in N3 — **analytical; open scope stated below**

The weak-economy proof survives. Let $D_F=\operatorname{ess\,sup}t_F(\theta)-\operatorname{ess\,inf}t_F(\theta)$. If $k>D_{F_0}$, every nonzero order loses against every candidate schedule. With the prior cost conditions, unique zero orders and entry $\rho$ follow.

A sharper no-trade existence condition also survives. Let $\bar t=\mathbb E[t_F(\theta)]$ and let $e_\pi$ be entry at the prior. Against its constant price, every order has payoff

$$
q e_\pi[t_F(\theta)-\bar t]-k|q|.
$$

Hence no trade is an equilibrium exactly when

$$
e_\pi\operatorname{ess\,sup}_\theta|t_F(\theta)-\bar t|\le k. \tag{N.26}
$$

For a strong-economy analog, Claim 8 extends to two separated value groups. Replace class extrema with essential extrema and $\mathcal M_\pi$ with $\mathcal M_G$. Define $d_1$ as in (N.18), using the maximum low-group proceeds and minimum high-group proceeds.

If $d_1>0$ and the same strict inequalities hold, every exact-value investor in the low group sells fully. Every investor in the high group buys fully. The residual bound proves this for all exact values, rather than only their group means.

Under these orders, flow reveals only group membership. Conditional value laws within each group remain their prior laws. Their mean auction payoffs supply the binary construction in Claim 8. Thus entry rises above $\rho$ and can return to $\rho$ under (N.20).

This extension has a nonempty strict region with genuine continuous values. Replace each point value in the strict binary benchmark by a sufficiently narrow uniform interval. Auction payoffs converge uniformly within each group. The weak range, strong separation, cost margins, and third-economy margins therefore retain their strict signs.

The group gap can contain $M(0)$ and the region in (N.25), with no type mass there. Thus this result does not conflict with Claim 12.

**Open:** For a connected continuum, this memo does not prove a general Proposition 2 analog with a unique nonzero order function. **Conjecture:** An entry reversal can survive with monotone partial orders and a zero-order region. Its proof needs a new existence and incentive argument, rather than the binary uniform lower bound.

### Claim 14. Deterrence at a fixed experiment survives all these extensions — **analytical**

Hold fixed a signal and its joint law with $(j,\theta)$. Under incumbent FOSD, (N.4) gives $\gamma_{F_1}(\theta)\le\gamma_{F_0}(\theta)$ pointwise. Conditional expectations preserve this inequality at every signal.

For every realized cost, the preparation indicator can only fall. Its expectation therefore falls weakly. This is Proposition A.3's argument with a general conditional value law. It applies to both N2 and N3.

The experiment must include the actual signal received by the challenger. If a fixed order profile creates a different price partition across economies, holding orders fixed alone does not hold the price experiment fixed. Under Claim 7's equilibrium sufficiency, the flow experiment and price experiment are equivalent within each economy.

## 4. What changes relative to the current paper

- **Equation (4), Proposition 1, and A.1:** Replace point-value auction means with (N.1)–(N.3). Keep the reserve boundary term. Profit deterrence survives. A larger target spread needs (N.4), rather than unrestricted incumbent FOSD.
- **Equations (7)–(8) and Proposition A.1:** Pairwise likelihood bounds survive for every class pair. Prior odds replace equal odds. N3 uses event bounds and likelihood-weight restrictions.
- **Equation (10) and Proposition A.2:** The direct identity reveals expected target proceeds. Affine payoff geometry extends the identity without extra incentive work. Claim 7 supplies a stronger equilibrium result through the order of optimal trades.
- **Equation (11):** Replace the two residuals with $e(P)(t_j-T_X)$, or (N.22). Middle values do not have a fixed residual sign.
- **A.2 and its global order bound:** Density translation survives. Its positive uniform lower bound survives for separated groups. It fails for general middle values because the residual changes sign.
- **Proposition 2:** Claim 8 gives an explicit many-class version. Claim 13 gives a continuous-value version with separated groups. A connected continuum requires a different conclusion about the order function.
- **Equation (12):** Under full group orders, replace $g_H,g_L,t_H,t_L$ with group means. Replace the prior $1/2$ with $\alpha$ and set $x^*=(b/2)[\operatorname{logit}(\tau)-\operatorname{logit}(\alpha)]$.
- **Ownership statement:** Preparation and admissible participation differ if some values lie below $p$. High-group acquisition also needs its probability of victory, not only its preparation rate.
- **Section 6.3:** Its two uniform value classes are a direct N main-line example. They preserve a binary investor signal. They do not by themselves settle N2 or exact-value observation in N3.
- **Appendix A.5:** Its common binary public statistic and state-dependent entry coefficients explain why its inversion works. Our proof uses common entry conditional on price. It cannot be transferred unchanged to a many-class private buyer signal.

## 5. Numerical example

**Status: numerical diagnostic.** The script uses 45-digit arithmetic and prints its results. It writes no output files and contains no assertions. The numerical margins below are diagnostics, not interval certificates.

Script: [`../scripts/Q1_N_extensions/illustrate.py`](../scripts/Q1_N_extensions/illustrate.py).

Run from the project root:

```bash
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_extensions/illustrate.py
```

### 5.1 Three uniform classes with sufficient equilibrium information

Use the paper's $(p,\rho,c_L,c_H,b,k)=(0.5,0.25,1,6,2,0.02)$. Split its low class into two nearby uniform classes:

$$
G_1=U[0.95,1.05],\quad G_2=U[0.97,1.07],\quad
G_3=U[9.95,10.05],\quad \pi=(0.25,0.25,0.5).
$$

The means are $(1,1.02,10)$ and the half-width is $0.05$. Keep $(r_0,r_1,r_2)=(1.2,3,3.6)$. The first two classes overlap, and the second FOSD-dominates the first.

| Quantity | $r_0=1.2$ | $r_1=3$ | $r_2=3.6$ |
|---|---:|---:|---:|
| Target range | 0.017013888889 | 0.666805555556 | 0.939004629630 |
| Minimum feasible gross profit | 2.734897351462 | 2.368741277878 | 2.274268985428 |
| Maximum feasible gross profit | 6.882199870761 | 6.218097611011 | 5.998096755312 |
| Gross profit at prior | 4.808548611111 | 4.293419444444 | 4.136182870370 |
| Group separation $d_s$ | 0.002566582210 | 0.170914322460 | 0.243407911206 |
| $(1-1/b)\rho d_s$ | 0.000320822776 | 0.021364290308 | 0.030425988901 |

The weak target range is below $k=0.02$. The strong and third-economy marginal bounds exceed $k$. Every reported minimum profit exceeds $c_L=1$. The weak prior excludes high-cost preparation, while the strong upper posterior permits it. The third-economy ceiling is below $c_H=6$.

Thus the diagnostics place this vector inside Claim 8's sufficient region. The proposed outcomes are zero orders at $r_0$ and $(-1,-1,1)$ at $r_1,r_2$.

At $r_1$, the printed auction means are

$$
\begin{aligned}
t&=(0.874861111111,\ 0.888127777778,\ 1.541666666667),\\
g&=(0.125138888889,\ 0.131872222222,\ 8.458333333333).
\end{aligned}
$$

Their collinearity determinant is $0.106063888889$, not zero. Nevertheless, the forced orders make classes 1 and 2 share an order. The within-low-group prior proportions remain fixed, so one posterior group probability determines both auction means.

The printed threshold and outcomes are

$$
\tau=0.704875851108,\quad x^*=0.870625578075,\quad
\mathsf E_1=0.522831713974,\quad
\mathsf O_{H,1}=0.324244884940.
$$

The entry sequence is $0.25\to0.522831713974\to0.25$. Every high-class value exceeds all three incumbent supports. Thus the ownership comparison in this example has the extra condition needed in Claim 8.

To compute posterior extrema, the script writes $\mu_j=\pi_jw_j/\sum_l\pi_lw_l$ with $1\le w_j\le K$. This represents exactly $\mathcal M_\pi$. A linear fractional mean has an extremum at a box vertex: with other weights fixed, it is monotone or constant in each weight. The script enumerates the eight vertices.

### 5.2 A concrete failure of profit-statistic sufficiency under arbitrary orders

Use uniform classes centered at $(1,2,10)$, with half-width $0.05$. Set $\pi=(0.15,0.15,0.7)$ and $q=(1,-1,0)$ at $r=3$. This is a stated prior and order variant.

The script finds two flows with the same target mean:

| Quantity | Left branch | Right branch |
|---|---:|---:|
| Flow | -0.950000000000 | 0.176805670171 |
| Target mean $T_X$ | 1.444313707098 | 1.444313707098 |
| Challenger profit $B_X$ | 5.923917179653 | 6.660290917860 |
| Posterior class 1 | 0.088654507994 | 0.120698598707 |
| Posterior class 2 | 0.229234817663 | 0.101138498335 |
| Posterior class 3 | 0.682110674343 | 0.778162902958 |

At the benchmark $c_H=6$, flow-based entry decisions differ. This does not prove that their prices coincide, since entry itself can affect price.

For an exact competitive continuation with a shared price, change $c_H$ to $20$. Then only low-cost preparation occurs at every flow. The price is $t_0+\rho(T_X-t_0)=0.673578426775$ on this level set. Its posterior combines both branches.

The conditional branch weights are $0.769896614642$ and $0.230103385358$. They use $h_X(x)/|T_X'(x)|$, rather than equal weights. The resulting price posterior is

$$
\nu(P)=(0.096027961748,\ 0.199759420933,\ 0.704212617319),
\qquad B_P=6.093359269704.
$$

It differs from each flow posterior. The two-branch formulas hold on an interval of target means; this is not a claim about a single null flow event.

The low-cost floor is valid in this continuation. The posterior probability of class 3 is at least $m_{0.7}$ from (N.5), so its profit contribution alone exceeds $1$. Also, $20>\max_jg_j$, which excludes high-cost preparation.

Investor optimality is not imposed. The nonmonotone orders violate Claim 7. This example shows exactly what the price identity alone fails to recover; it does not contradict equilibrium sufficiency.

### 5.3 A failure of the flow-based entry construction

The last script block prints Claim 6's exact Laplace construction. Its order magnitude is $0.964480295371$. Its two tail prices both equal $0.529166666667$.

At that price, the flow-based rule requires entry $1$ on one tail and $0.25$ on the other. Their gross profits are $1.635083333333$ and $1.592833333333$, around the stated cost $1.61$. Thus the construction cannot supply a price-based entry strategy.

Again, this is a failed candidate, not an equilibrium. It identifies the Bayesian object that breaks.

## 6. Open issues and risks

1. **Analytical scope:** Claim 7 needs $b>1$, bounded orders, common price-based entry, and a uniform positive floor. The covariance argument alone does not supply these premises.
2. **Analytical scope:** Incumbent FOSD does not generally increase the class target spread when reserve admissibility differs. Equal admissibility or the exact condition in (N.4) repairs that claim.
3. **Open:** A general existence and uniqueness theorem for intermediate classes is absent here. The separated-group theorem is a sufficient construction, not a complete equilibrium correspondence.
4. **Open:** For a connected continuum, a full order function requires further analysis. Claim 12 rules out a literal full-buy/full-sell rule almost everywhere under its support conditions.
5. **Conjecture:** The qualitative entry reversal survives with intermediate values and a region with no trade. No numerical equilibrium solution for that case appears in this memo.
6. **Numerical diagnostic:** The reported inequalities use high precision but no interval enclosure. They do not constitute a formal parameter certificate.
7. **Analytical scope:** Preparation, admissible participation, and acquisition differ when values can fall below the reserve. They require distinct outcome measures.
8. **Analytical scope:** The failed profiles are not equilibrium counterexamples under the maintained floor and $b>1$. Claim 7 rules out such a counterexample. Their role is to audit an unrestricted extension of the price identity.
9. **Open outside this reading:** A private buyer signal can make entry depend on the true class conditional on price. Appendix A.5 handles a binary version. The common-entry proof here does not settle its many-class extension.

## 7. Recommendation

1. Present the two-distribution N model first. Use (N.1)–(N.3) and an unequal prior. Separate reserve admissibility from preparation.
2. Keep equal reserve admissibility for the main competition comparison. State the broader boundary formula as a qualification.
3. Add the equilibrium order argument in Claim 7 before any claim that several classes destroy price sufficiency. Collinearity is sufficient for arbitrary beliefs but unnecessary in this equilibrium model.
4. Use Claim 8 as a clean N2 extension. The three-uniform example shows that class heterogeneity can survive without a new order solver.
5. Treat exact-value observation in two narrow groups as the first N3 result. It admits a full proof with continuous values.
6. Reserve a connected continuum for a separate extension. State the zero-order region and the unresolved order function clearly. Do not attach the binary global order proof to it.
7. Keep ownership claims conditional on the high group's victory probability. Report preparation separately when the reserve can exclude a class.

## 8. Plain summary

Nature can choose a distribution instead of a fixed challenger value. The auction still gives simple expected payments and profits. But values below the reserve add a term that the usual spread formula omits. This term can reverse the effect of a stronger incumbent.

Several distributions create two different averages. The target share reflects expected sale proceeds. Preparation depends on expected acquisition profit. For arbitrary beliefs, one average determines the other only under a special geometric condition.

Equilibrium imposes more structure. Investors with higher target proceeds cannot prefer smaller orders under the paper's assumptions. This order makes the price reveal the relevant posterior. Thus several distributions do not automatically destroy price sufficiency.

A three-uniform example preserves the paper's entry pattern: $0.25$, then about $0.523$, then $0.25$. Its payoff points are not collinear. Its two low classes share an order, which keeps the information problem simple.

If the investor sees the exact value, price sufficiency can still survive. The harder problem is the order choice. A connected range of target proceeds contains investors who prefer no trade. The binary full-order proof cannot cover all those values.

Two narrow, separated value groups admit a complete extension. A general connected continuum remains open. The failed order examples in this memo expose a faulty price construction; they are not equilibrium counterexamples.
