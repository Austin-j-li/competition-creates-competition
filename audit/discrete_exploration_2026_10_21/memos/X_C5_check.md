# X_C5. Independent check of the stake extension

## 1. Scope

This check covers the eight stated claims in `C5_stake.md`.
It uses the pinned manuscript at `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
The checked manuscript passages are Sections 2.2–2.4, equation (4), and the appendix material on preparation and surplus.
The order set is $\{0,1\}$.
The low preparation cost is zero.
The prior and presence probability are both as declared: $\pi=1/2$ and $\lambda=1$.

The three-point benchmark uses $c_H=6$.
The discrete-Laplace benchmark uses $c_H=5$ and $b=2$.
The remaining inputs are $(h,\ell,p,\rho,k)=(10,1,1/2,1/4,1/50)$.
The weak and strong strengths are $6/5$ and $3$.

The independent derivation and first calculation preceded any read or run of the original scripts.
The independent script is `scripts/X_C5_check/independent.py`.
Its output is `scripts/X_C5_check/independent.out`.
It constructs payoffs from terminal holdings, prices, and the conditional flow laws.
It uses exact fractions throughout, with rational intervals for the discrete-Laplace constant.

The equilibrium concept is perfect Bayesian equilibrium with competitive prices.
This check separates the following tie systems:

- **T0:** the investor chooses zero at indifference; the challenger prepares at indifference.
- **T1:** the investor may mix at indifference; the challenger prepares at indifference.
- **T2:** both parties may mix at indifference.

The three-point classification below imposes the directional belief $\mu_2=1$ at an unused top flow.
This is the memo's stated implementation of D1.
Section 3.3 separates this implementation from passive beliefs and the Intuitive Criterion.
No unused flow exists in the discrete-Laplace model.

No manuscript, original memo, or original script changed.

## 2. Verdict table

| Claim | Verdict | Evidence |
|---|---|---|
| 1. Complete three-point correspondence under three tie systems | CONFIRMED WITH CORRECTION | Correct for $1/2<\tau<1$ under the directional belief. Endpoints share profiles. The stated $\tau=1$ boundary needs separate treatment. |
| 2. Exact limits for the Proposition 2 analog | CONFIRMED WITH CORRECTION | The fractions and discrete-Laplace values agree. The weak limit includes equality under T0. Strong uniqueness excludes equality under T1 and T2. |
| 3. Low-class purchases, price information, and entry | CONFIRMED WITH CORRECTION | The onset is $152/75$. Under T1, such purchases cease to exist above $2144/825$. The entry hump describes an upper envelope. |
| 4. Informative entry has no interior optimum | CONFIRMED WITH CORRECTION | There is no strict or unique optimum. The upper envelope has a plateau. Other branches fall, and every interior plateau point is an optimum. |
| 5. New types, coexistence, and five discrete-Laplace equilibria at $0.36$ | CONFIRMED | Five distinct equilibria exist under T2. Independent rational intervals certify the required signs. Only three survive T1 at this stake. |
| 6. Manipulation transfers challenger rent to shareholders and destroys most information surplus | REFUTED | The surplus loss is correct. The claimed rent transfer is false. Shareholders receive only $7.80\%$ of the challenger profit loss in the stated comparison. |
| 7. Nonexistence above about $2.6$, repaired by a challenger who can mix | CONFIRMED | At $r=3$, T1 has no equilibrium for $\omega>2144/825$. T2 has the unique branch M′. |
| 8. Corrections to the earlier stake and equality claims | CONFIRMED | The earlier $2.5988$ value concerns a deviation against S. Mixed purchases start at $2.0267$. The zero-order tie preserves S at its upper boundary. |

## 3. Derivations and evidence for each claim

### 3.1 The stake payoff and purchase size

**Status: analytical.**

A holder who starts with $\omega$ units and buys $q$ units ends with $\omega+q$ units.
Its terminal wealth, apart from the sunk purchase cost of the initial stake, is

$$
U_j(q)=(\omega+q)\mathbb E[V_T\mid j,q]-q\mathbb E[P(q+Z)]-kq.
$$

Thus the objective in the original memo is correct:

$$
(\omega+q)V_T-qP-kq=\omega V_T+q(V_T-P)-kq.
$$

The purchase changes terminal holdings.
The term $qV_T$ already includes this change.
No further stake increment belongs in the payoff.

Let $w_j=t_j-t_0$ and $\Delta_T=w_H-w_L$.
Conditional terminal proceeds and prices satisfy

$$
v_j(x)=t_0+e(x)w_j,
\qquad
P(x)=t_0+e(x)[w_L+\Delta_T\mu(x)].
$$

The pinned auction formulas give these objects directly.
The low preparation cost gives $e(x)\ge\rho>0$.
The price therefore reveals the posterior through

$$
\mu(x)=\frac{P(x)-t_0-e(P(x))w_L}{e(P(x))\Delta_T}.
$$

The residuals are

$$
v_H(x)-P(x)=e(x)\Delta_T[1-\mu(x)],
\qquad
v_L(x)-P(x)=-e(x)\Delta_T\mu(x).
$$

For three-point noise, subtract the payoff at $q=0$ from the payoff at $q=1$.
The two common flows cancel from the initial stake term.
This gives

$$
G_j=\frac{\omega w_j[e(2)-e(-1)]}{3}
+\frac{1}{3}\sum_{x=0}^{2}[v_j(x)-P(x)]-k.
$$

The stake pays terminal proceeds, rather than an interim quotation.
An objective that replaces $\omega V_T$ with $\omega P$ describes a different liquidation or valuation rule.
Its stake contribution is $\omega[P(2)-P(-1)]/3$.
That expression generally differs from the formula above.
An extra $\omega P$ alongside the terminal stake would duplicate the stake.

### 3.2 Claim 1: the three-point correspondence

**Status: analytical.**

The complete result below requires $1/2<\tau<1$.
Here $\tau=(c_H-g_L)/(g_H-g_L)$.
The benchmark satisfies both strict inequalities.

For arbitrary purchase probabilities, Bayes' rule gives

$$
\mu_{-1}=\frac{1-\beta_H}{2-\beta_H-\beta_L},
\qquad \mu_0=\mu_1=\frac12,
\qquad \mu_2=\frac{\beta_H}{\beta_H+\beta_L}.
$$

A zero denominator marks an unused flow.
The middle flows always have entry $\rho$.

Suppose $\beta_L>\beta_H$.
Then $\mu_2<1/2$ and $e(2)=\rho\le e(-1)$.
The low class has a nonpositive stake contribution and a negative net trade payoff.
It must choose zero, contrary to $\beta_L>\beta_H$.
Thus every equilibrium has $\beta_L\le\beta_H$.

Complete pooled purchases also fail.
All reached flows then have posterior $1/2$ and entry $\rho$.
The unused bottom flow has entry at least $\rho$.
The low class gains at most $-\rho\Delta_T/2-k<0$ from a purchase.

For every remaining profile, the bottom flow has positive probability and posterior at most $1/2$.
Hence $e(-1)=\rho$.
Subtract the class gains:

$$
G_H-G_L=\frac{\Delta_T}{3}
\{\omega[e(2)-\rho]+2\rho+e(2)\}>0.
$$

Consequently, a positive low-class purchase probability requires $\beta_H=1$.
This reduces all equilibria to two edges of the probability square, plus no trade.

On the edge $\beta_L=0<\beta_H$, the top flow reveals H and has entry one.
The gains reduce to

$$
G_H=\frac{\omega w_H(1-\rho)+\rho\Delta_T}{3}-k,
\qquad
G_L=\frac{\omega w_L(1-\rho)-(1+\rho)\Delta_T}{3}-k.
$$

Define

$$
\omega_H=\frac{3k-\rho\Delta_T}{(1-\rho)w_H},
\quad
\Omega_2=\frac{3k+(\rho+\tau)\Delta_T}{(1-\rho)w_L},
\quad
\Omega_1=\frac{3k+(1+\rho)\Delta_T}{(1-\rho)w_L}.
$$

On the edge $\beta_H=1$, put $\beta=\beta_L$.
The top posterior is $1/(1+\beta)$.
Entry above the floor requires $\beta\le\beta_{\max}=1/\tau-1$.
For $0<\beta<\beta_{\max}$, entry is one and

$$
G_L(\beta)=\frac{\omega w_L(1-\rho)-\rho\Delta_T-\Delta_T/(1+\beta)}{3}-k.
$$

Its derivative is $\Delta_T/[3(1+\beta)^2]>0$.
The unique zero is

$$
\beta^*(\omega)=
\frac{\Delta_T}{\omega w_L(1-\rho)-\rho\Delta_T-3k}-1.
$$

At $\beta_{\max}$, a challenger who can mix permits

$$
e_2=\frac{3k+\rho\Delta_T+\rho\omega w_L}{\omega w_L-\tau\Delta_T}.
$$

This value lies in $(\rho,1]$ exactly when $\omega\ge\Omega_2$.
At this profile, $G_L=0$ and $G_H>0$.
If $\beta>\beta_{\max}$, entry returns to $\rho$ and $G_L<0$.
These facts exclude every other profile.

The corrected T2 list is:

| Profile | Exact domain |
|---|---|
| NT: $(0,0)$ | $\omega\le\omega_H$, under the directional top belief |
| S: $(1,0)$ with top entry one | $\max\{0,\omega_H\}\le\omega\le\Omega_1$ |
| Hm: $(\beta_H,0)$, $0<\beta_H<1$ | $\omega=\omega_H\ge0$ |
| M: $(1,\beta^*(\omega))$ | $\Omega_2<\omega<\Omega_1$ |
| M′: $(1,\beta_{\max})$ with top entry $e_2$ | $\omega\ge\Omega_2$ |

At $\Omega_2$, M's limit equals M′ with $e_2=1$.
At $\Omega_1$, M's limit equals S.
These are shared profiles, rather than additional equilibria.

T1 keeps M′ only at $\Omega_2$, where the challenger prepares with probability one.
T0 removes Hm, M, and M′.
Under T0, NT includes $\omega_H$, and S requires $\omega>\omega_H$.
S still includes $\Omega_1$, because the low class chooses zero at its tie.

The original regime allows $\tau=1$, but its proof then uses $\tau<1$.
At $\tau=1$, $\beta_{\max}=0$ and $\Omega_2=\Omega_1$.
Under T2, the challenger can mix at a revealing H flow even when the low class never buys.
The memo's list omits these preparation choices.
Either impose $\tau<1$ or add a separate boundary result.

### 3.3 The unused top flow: D1, the Intuitive Criterion, and passive beliefs

**Status: analytical, conditional on the stated refinement implementation.**

At no trade, a possible top response $(\mu,e)$ gives

$$
\begin{aligned}
G_H&=\frac{\omega w_H(e-\rho)+\rho\Delta_T+e\Delta_T(1-\mu)}{3}-k,\\
G_L&=\frac{\omega w_L(e-\rho)-\rho\Delta_T-e\Delta_T\mu}{3}-k.
\end{aligned}
$$

Their difference is strictly positive for all $e\ge\rho$.
Every response that weakly benefits L therefore strictly benefits H.
This supports the directional deletion in the memo's D1 implementation.
When neither class can gain, the refinement is silent.
The choice $\mu_2=1$ then acts as a completion.

The response set matters for a formal D1 result.
The memo treats the price setter and challenger as one receiver.
It also permits challenger mixtures when it compares possible responses.
Its program uses this enlarged response set even for T0 and T1 comparisons.
The resulting directional classification is checkable.
An unrestricted D1 theorem for all three restricted games needs an explicit receiver game and response set.

Under the directional belief, $\mu=1$ and $e=1$.
No trade exists exactly when $\omega\le\omega_H$.

Under a passive top belief, $\mu=1/2<\tau$ and $e=\rho$.
The stake contribution is zero at every $\omega$.
The gains are

$$
G_H=\rho\Delta_T/2-k,
\qquad G_L=-\rho\Delta_T/2-k.
$$

At $r=6/5$, these gains are $-43/2400$ and $-53/2400$.
Thus passive beliefs support no trade at every stake.
For any top belief below $\tau$, the high-class gain is at most $2\rho\Delta_T/3-k<0$ at this benchmark.
The pessimistic-belief statement therefore also holds here.

Within the memo's response set, L first has a weakly profitable deviation at $(\mu,e)=(\tau,1)$.
Its gain there equals

$$
\frac{\omega w_L(1-\rho)-\Delta_T(\rho+\tau)}3-k.
$$

It reaches zero at $\Omega_2$.
The Intuitive Criterion excludes L below this point when H can gain.
Above this point, passive beliefs can support no trade again.
This reproduces the memo's IC intervals under its stated interpretation of equilibrium dominance.

The weak-economy conclusion is therefore belief dependent.
The strong-economy and large-stake failure at $r=3$ do not depend on an unused-flow belief.
At that strength, even the least favorable top response leaves $G_H\ge\rho\Delta_T/3-k>0$ at no trade.

### 3.4 Claim 2: thresholds and the return economy

**Status: computer-assisted.**

The independent exact calculation gives:

| Strength | $\omega_H$ | $\Omega_2$ | $\Omega_1$ | $\beta_{\max}$ |
|---|---|---|---|---|
| $6/5$ | $268/1485=0.180471380471$ | $27616/109725=0.251683754842$ | $388/1425=0.272280701754$ | $113/195$ |
| $3$ | $-256/2025$ | $152/75=2.026666666667$ | $2144/825=2.598787878788$ | $59/141$ |

The weak economy sets the joint bound.
Under T1 and T2, unique no trade requires $\omega<268/1485$.
At equality, Hm gives a continuum that includes NT and S as endpoints.
Under T0, unique no trade also holds at equality.

At $r=3$, S is unique for $0\le\omega<152/75$ under T1 and T2.
At $152/75$, S and the threshold manipulation profile are distinct equilibria.
Under T0, S remains unique through $2144/825$.

The return result requires a new strength with $g_H(r)<c_H$ in the three-point model.
Then $e(x)=\rho$ at every belief and the stake term vanishes.
Since $\Delta_T$ rises with $r$, the high class strictly prefers a purchase.
The low class strictly prefers zero.
Thus S is unique for every stake.

For $c_H=6$, this condition requires $r>4+\sqrt{63}/2\simeq7.968627$.
The memo's $r=9$ example satisfies it.
The paper's $r_2=3.6$ does not satisfy it.
The independent gains at $r=9$ are $373/1350$ and $-827/1350$, for both $\omega=0$ and $1000$.

The discrete-Laplace calculation gives:

| Strength | First informative equilibrium $\omega^\star$ | S appears at $\omega_H$ | $\Omega_2$ | $\Omega_1$ |
|---|---|---|---|---|
| $6/5$ | $0.187802094246253$ | $0.199336785373952$ | $0.359635439177902$ | $0.372045287392279$ |
| $3$ | negative | negative | $3.422471113125867$ | $3.587802237166285$ |

These values agree with the original outputs.
The discrete-Laplace weak bound under T1 and T2 is $\omega<\omega^\star$.
Under T0, it is $\omega\le\omega_H$.
The distinction arises because T0 excludes the high-class mixed branch.

At $r=4$, the best possible discrete-Laplace posterior gives

$$
B_r(M_1)\in[4.99561723321460469,\ 4.99561723321460470]<5.
$$

Entry is therefore $\rho$ at every flow and every stake.
The independent gains at S are $0.112189588113397$ and $-0.169060411886603$.
The high-class gain remains positive over its whole probability edge.
Thus S is unique there for every stake.

### 3.5 Claim 3: low-class purchases, information, and total entry

**Status: analytical.**

The low class buys in some T2 equilibrium exactly when $\omega\ge\Omega_2$.
Under T1, it buys in some equilibrium exactly when $\Omega_2\le\omega<\Omega_1$.
There is no T1 equilibrium above $\Omega_1$ in the strong economy.
At $\Omega_1$, the surviving T1 profile is S and the low class chooses zero.
The unqualified claim for all larger stakes therefore needs correction.

No equilibrium has both classes buy with probability one.
M and M′ do have both classes buy with positive probability.
The phrase about both types must distinguish these two statements.

Under M or M′, the posterior law is

$$
\left(0,\frac12,\frac1{1+\beta}\right)
\quad\text{with probabilities}\quad
\left(\frac{1-\beta}{6},\frac23,\frac{1+\beta}{6}\right).
$$

S has the same law at $\beta=0$.
Combine mass $\beta/6$ at posterior zero with mass $1/6$ at posterior one.
Their combined posterior mean is $1/(1+\beta)$.
This construction gives the posterior law above.
Thus S Blackwell-dominates M and M′.
The manipulation profiles retain information and never produce a constant price.

This claim does not exclude a constant price in NT.
NT survives in the weak discrete-Laplace economy at every stake.
It also survives under passive beliefs in the weak three-point economy.

For $\beta_H=1$, the class entry rates are

$$
\bar e_H=\rho+\frac{e_2-\rho}{3},
\qquad
\bar e_L=\rho+\frac{\beta(e_2-\rho)}{3}.
$$

Therefore

$$
\mathsf E=\rho+\frac{(1+\beta)(e_2-\rho)}6,
\qquad
\mathsf O_H=\frac\rho2+\frac{e_2-\rho}{6}.
$$

Under T1 and T2, the maximum over equilibria at $r=3$ is

$$
\rho+\frac{1-\rho}{6\tau}
=\frac{241}{564}=0.427304964539,
$$

at $\omega=152/75$ on the threshold manipulation profile.
S instead keeps total entry at $3/8=0.375$ throughout its domain.
Thus the hump describes the attainable upper envelope, rather than a unique response to the stake.

On M′,

$$
e_2-\rho=\frac{3k+\rho(1+\tau)\Delta_T}{\omega w_L-\tau\Delta_T}.
$$

It strictly falls to zero.
Consequently, total entry tends to $\rho$ and high-class ownership tends to $\rho/2$.

### 3.6 Claim 4: the informative-entry objective

**Status: analytical.**

Define $\mathsf I=\mathsf O_H-\rho/2$.
For an arbitrary surviving three-point profile,

$$
\mathsf I=\frac{\beta_H(e_2-\rho)}6\le\frac{1-\rho}{6}.
$$

Equality requires both $\beta_H=1$ and $e_2=1$.
The original Proposition 6 omits the first requirement in its first bullet.
Its own proof includes the requirement.

The omission matters at $\omega=\omega_H$.
For example, $\beta_H=1/2$ has $e_2=1$ but only half the maximal informative entry.
The independent output gives this profile at $r=6/5$.

Under T1 and T2, S and M attain $\mathsf I=(1-\rho)/6$.
Thus the maximum over equilibria has a plateau on

$$
[\max\{0,\omega_H\},\Omega_1].
$$

In the strong economy, this plateau starts at zero stake.
The stake cannot increase its height.
In the weak economy under the directional belief, the stake creates informative entry at $\omega_H$.
At equality, zero and positive informative entry coexist under T1 and T2.

Every interior point of a nontrivial plateau is an interior optimum.
The correct statement excludes a strict or unique interior optimum.
It must also identify the maximum over equilibria.
Informative entry on M′ falls with the stake.
It is not constant across all equilibria.
Under T0, S gives the same maximal height after the weak lower boundary, which T0 excludes from that plateau.

For discrete-Laplace noise, let $d_0=a/(1+a)$, $d_1=1/(1+a)$, and $\delta=d_1-d_0$.
Then

$$
\mathsf I=\frac{[e_G-\rho][d_0+\delta\beta_H]}2
\le\frac{(1-\rho)d_1}{2}.
$$

S and M attain this bound.
The same plateau logic applies to the maximum over equilibria.
In the weak economy, informative mixed equilibria first appear at $\omega^\star$.
The maximal plateau starts later, at $\omega_H$.

### 3.7 Claim 5: discrete-Laplace reduction and the five equilibria

**Status: computer-assisted.**

Summation of the geometric tails gives

$$
\Pr(X\ge1\mid q=0)=d_0,
\qquad
\Pr(X\ge1\mid q=1)=d_1.
$$

For class $j$, put $s_j=d_0+\delta\beta_j$.
The two posterior values are

$$
M=\frac{s_H}{s_H+s_L},
\qquad
m=\frac{1-s_H}{2-s_H-s_L}.
$$

All positive flows share $M$.
All nonpositive flows share $m$.
Every flow has positive probability, so no belief completion enters this result.

The gain formulas from terminal holdings are

$$
\begin{aligned}
G_H&=\omega w_H\delta(e_G-e_B)
+\Delta_T[d_1e_G(1-M)+d_0e_B(1-m)]-k,\\
G_L&=\omega w_L\delta(e_G-e_B)
-\Delta_T[d_1e_GM+d_0e_Bm]-k.
\end{aligned}
$$

If $\beta_L>\beta_H$, good news is worse news about H.
Then $e_G\le e_B$, so L's stake contribution is nonpositive.
Its trade contribution is negative.
This excludes reversed profiles.
For the remaining profiles, $m\le1/2<\tau$ and $e_B=\rho$.

Subtract the gains:

$$
G_H-G_L=\Delta_T[\omega\delta(e_G-\rho)+d_1e_G+d_0\rho]>0.
$$

Again, a positive low-class purchase probability requires $\beta_H=1$.
The two probability edges contain every possible equilibrium.

On $\beta_L=0$, put $u=\delta\beta_H$.
Then

$$
G_H=\omega w_H\delta(e_G-\rho)
+\Delta_Td_0d_1\left[
\frac{e_G}{2d_0+u}+\frac{\rho}{2d_1-u}\right]-k.
$$

Within a fixed entry regime, its derivative is nonpositive.
The first denominator is at most one, and the second is at least one.
Also $e_G\ge\rho$.
The derivative is therefore bounded above by

$$
\delta\Delta_Td_0d_1\left[
-\frac{e_G}{(2d_0+u)^2}+\frac\rho{(2d_1-u)^2}\right]\le0.
$$

The entry jump occurs at

$$
u^*=\frac{d_0(2\tau-1)}{1-\tau}.
$$

The first informative stake solves $G_H(u^*,e_G=1)=0$.
This gives the reported $\omega^\star$.
A challenger mixture at $u^*$ solves one affine indifference equation.
It gives Hth.

On $\beta_H=1$, the low-class gain with full entry is

$$
G_L(\beta)=\omega w_L\delta(1-\rho)
-\Delta_T\left[
\frac{d_1^2}{1+\delta\beta}
+\frac{\rho d_0^2}{1-\delta\beta}\right]-k.
$$

For $0\le\beta\le1$,

$$
\frac{d_0}{1-\delta\beta}\le
\frac{d_1}{1+\delta\beta}.
$$

Since $\rho<1$, differentiation shows that the expression in square brackets strictly falls.
Thus $G_L$ strictly rises.
It has at most one interior root.
The threshold probability is $(d_1/\tau-1)/\delta$.
At that probability, a challenger mixture solves another affine equation and gives M′.

The independent calculation encloses $a=e^{-1/2}$ between consecutive alternating partial sums.
It uses terms through orders 60 and 61.
The rational enclosure has width below $10^{-102}$.
All subsequent interval operations use exact fractions.
The output rounds displayed endpoints outward.

At $r=6/5$ and $\omega=9/25$, the independent results are:

| Profile | $\beta_H$ | $\beta_L$ | Good-news entry $e_G$ | $\mathsf E$ |
|---|---:|---:|---:|---:|
| NT | 0 | 0 | 0.25 | 0.250000000 |
| S | 1 | 0 | 1 | 0.625000000 |
| Hth | 0.140543592394 | 0 | 0.684314546670 | 0.421446338 |
| M | 1 | 0.758089296914 | 1 | 0.694626331 |
| M′ | 1 | 0.787644049992 | 0.999101069340 | 0.696804602 |

For NT, the gain signs are $(-,-)$.
For S, they are $(+,-)$.
At the low-class threshold, its gain is negative at $e_G=\rho$ and positive at $e_G=1$.
At the high-class threshold, H's gain also changes from negative to positive.
L's gain remains negative there.

The smallest relevant strict margin is L's gain at the high-class threshold with full entry:

$$
G_L\in[-0.000001812308,\ -0.000001812306].
$$

It excludes a low-class deviation from Hth.
The exact sign enclosures support all five profiles.
The monotone edge formulas exclude an additional interior root.
Thus five distinct T2 equilibria exist at this stake.

T1 excludes Hth and M′ because both require a challenger mixture.
It retains NT, S, and M.
T0 also excludes M and retains NT and S.
The five-equilibrium statement must retain its T2 qualifier.

The independent script also certifies strict signs at stakes $0.18$, $3$, $3.5$, and $3.6$.
These are the other four stakes in the original certificate.
The original certificate prints 32 certified inequalities, with no failed sign.
The independent output prints 60 strict sign enclosures over the same five cases.

The weak Hth branch also has a uniform bound.
Let $K_I$ be H's gross trade payoff at $u^*$ with entry $\rho$.
The independent calculation gives

$$
k-K_I\in[0.01795083958380349,\ 0.01795083958380351]>0.
$$

The bound for L's gain at the Hth root is

$$
\frac{w_L}{w_H}(k-K_I)
-\Delta_T\rho[d_1\tau+d_0m^*]-k
\in[-0.00489195311449712,\ -0.00489195311449710]<0.
$$

Therefore Hth exists for all $\omega\ge\omega^\star$ at the weak benchmark under T2.
The point certificates alone would not prove this statement.
The uniform bound supplies the missing all-stake step.

At zero stake, no trade requires $\Delta_T\le2k/\rho$.
Full purchases require $\Delta_T\ge k/[d_0d_1(1+\rho)]$ in the recruiting regime.
These conditions give the stated coexistence interval near $[1.4433,1.7479]$.
The original grid claim about a third equilibrium remains a numerical diagnostic.
It is separate from the certified five-equilibrium example.

### 3.8 Claim 6: welfare and the alleged rent transfer

**Status: computer-assisted.**

Let $a_0=(r^2-p^2)/(2r)$ be expected allocation value without entry.
The allocation increments are

$$
a_H=h-a_0,
\qquad
a_L=\frac{\ell^2+p^2}{2r}.
$$

Given class entry rates, the independent ledger uses

$$
\begin{aligned}
T&=t_0+\frac{\bar e_Hw_H+\bar e_Lw_L}{2},\\
C&=\frac{\bar e_Hg_H+\bar e_Lg_L}{2}
-c_H(\mathsf E-\rho),\\
W&=a_0+\frac{\bar e_Ha_H+\bar e_La_L}{2}
-c_H(\mathsf E-\rho)-\frac{k(\beta_H+\beta_L)}2.
\end{aligned}
$$

The stake is part of target ownership.
It is not an extra social asset.
The ledger therefore does not add its terminal payoff to $T$ again.

The independent values at $r=3$ are:

| Profile | Target proceeds $T$ | Challenger profit $C$ | Total surplus $W$ |
|---|---:|---:|---:|
| Hidden price, entry $\rho$ | 0.614583333333 | 1.072916666667 | 2.542083333333 |
| S | 0.755208333333 | 1.380208333333 | 2.859791666667 |
| M at $\Omega_2$ | 0.779181442080 | 1.072916666667 | 2.552674349882 |

Every displayed value agrees with the original script to its printed precision.
The stated reduction in surplus is real.
It removes the fraction

$$
\frac{W_S-W_M}{W_S-W_{\rm hidden}}
=\frac{207857}{215025}=0.966664341356
$$

of the information surplus in this comparison.

The rent-transfer interpretation does not follow.
Relative to S, the exact changes are

$$
\Delta T=\frac{649}{27072}=0.023973108747,
\qquad
\Delta C=-\frac{59}{192}=-0.307291666667.
$$

Their ratio is

$$
\frac{\Delta T}{-\Delta C}=\frac{11}{141}=0.078014184397.
$$

Shareholders receive only $7.80\%$ of the lost challenger profit.
Extra preparation costs destroy most of the loss.
This is not a transfer of the whole rent to shareholders.

The general challenger identity also corrects the claim about M:

$$
C-C_{\rm hidden}
=\frac{e_2-\rho}{6}
\{g_H-c_H+\beta(g_L-c_H)\}.
$$

The expression is positive on interior M, where $\beta<\beta_{\max}$.
It vanishes at M's lower stake endpoint and along M′.
At $\omega=2.3$, interior M has challenger profit $1.246463643640$.
The hidden-price value is only $1.072916666667$.
The challenger does gain on interior M.

The shareholder comparison also depends on the selected branch.
For discrete-Laplace noise at $\omega=3.5$, S gives target proceeds $0.942073166134$.
M′ gives only $0.933456596515$.
Both exceed hidden-price proceeds, but manipulation does not always raise proceeds relative to S.

The discrete-Laplace figures in the original memo agree with the independent enclosures:

| Profile at $r=3$ | Target proceeds | Challenger profit | Total surplus |
|---|---:|---:|---:|
| S | 0.942073166134 | 1.189977076672 | 2.690393743339 |
| M, $\omega=3.5$ | 0.947706282635 | 1.130061201155 | 2.630163892028 |
| M′, $\omega=3.5$ | 0.933456596515 | 1.072916666667 | 2.570792374952 |
| M′, $\omega=100$ | 0.618942272354 | 1.072916666667 | 2.539897058237 |

The original numerical-diagnostic label is appropriate for its own decimal calculations.
The independent rational enclosures certify the displayed rows.
They do not certify every possible welfare comparison.

### 3.9 Claim 7: nonexistence and its repair

**Status: analytical.**

At $r=3$, let $\omega>\Omega_1=2144/825$.
S fails because L gains from a purchase.
For $0<\beta<\beta_{\max}$, its gain is even larger, since $G_L$ rises with $\beta$.
At $\beta_{\max}$, the T1 challenger chooses full entry, which also gives $G_L>0$.
Above $\beta_{\max}$, expensive entry disappears and $G_L<0$.
Thus no low-class mixed profile can satisfy T1.

H cannot mix while L chooses zero, since its gain is strictly positive.
No trade fails under every possible top belief at this strength.
Reversed profiles and complete pooled purchases already fail.
These exclusions cover every profile.
T1 therefore has no equilibrium above $2144/825$.
T0, which permits fewer profiles, also has none.

T2 permits a challenger mixture at the top posterior $\tau$.
The affine condition $G_L=0$ gives the unique $e_2$ in Section 3.2.
The high class strictly prefers a purchase.
This yields the unique M′ equilibrium for every $\omega>\Omega_1$.

The failure concerns the prescribed tie rule in this discrete game.
It is not a failure of equilibrium existence once the challenger can mix at indifference.

### 3.10 Claim 8: earlier claims and the equality correction

**Status: analytical.**

The earlier sell-only memo's Claim 14 states the buy-side threshold $2.5988$.
Against the fixed separating schedule, the correct condition is indeed

$$
G_L^S>0\quad\Longleftrightarrow\quad\omega>\Omega_1=2144/825.
$$

This is a profitable-deviation threshold.
It is not the first stake with low-class purchases in an equilibrium.
The latter is $\Omega_2=152/75$ under T1 and T2.
The earlier number remains correct for its fixed schedule.
The original correction should preserve this distinction.

At $\omega=\Omega_1$, L is indifferent against S.
T0 prescribes zero for L, so S survives.
The high class strictly prefers its purchase there.
The sell-side equality objection from SYNTHESIS A.2 item 6 therefore does not transfer to this buy-side profile.

The earlier Laplace stake memo proves existence of no trade at every stake in its weak economy.
All flows occur under no trade in that model.
It can retain constant entry after every deviation.
The three-point game has a new top flow after a purchase deviation.
The directional belief assigns H to that flow and can recruit expensive entry.
Thus its no-trade outcome fails above $\omega_H$ under that completion.

Under passive beliefs, three-point no trade still survives every stake.
The comparison therefore concerns the belief rule and support of noise.
It is not a contradiction between the two calculations.

### 3.11 Comparison with the original scripts and status labels

**Status: computer-assisted.**

The comparison runs used these original files after the independent calculation:

- `tp_thresholds.py`;
- `tp_enumerate.py`;
- `dl_thresholds.py`;
- `dl_certify.py`;
- `dl_five.py`;
- `welfare.py`.

Their fresh outputs are `original_*.out` in `scripts/X_C5_check/`.
All runs used the prescribed slot wrapper.
At most three slots ran at once.
The runs returned normally.
Their output agrees with the independent thresholds, profiles, and welfare rows at the stated precision.

The original rational grid does not itself prove a complete correspondence.
Its interior root search is a finite rational bisection.
It prints small nonzero residuals at approximate roots.
The analytical edge reduction supplies completeness in the strict regime.

The original discrete-Laplace certificate does support its stated strict signs.
Its 32 sign certificates include the uniform Hth bound.
It does not prove arbitrary parameter claims from five point cases alone.
The original zero-stake grid and shape scans correctly retain numerical-diagnostic labels.

One original output label is misleading outside the recruiting region.
At $r=4$, `dl_thresholds.py` prints H's zero-stake gain as $0.310473970283$.
That expression imposes full entry after good news, even though its own feasibility flag is false.
The actual gain with entry $\rho$ is $0.112189588113397$.
The memo's equilibrium and ceiling conclusion remain correct.
The output should label the first value as a forced-entry diagnostic or omit it there.

## 4. Errors found and corrections

1. **Rent transfer:** the claimed complete transfer to shareholders is false.
   Extra preparation costs destroy most of the challenger profit loss.
2. **Interior M profit:** the challenger gains above its hidden-price profit on interior M.
   Zero extra profit holds at $\Omega_2$ and on M′.
3. **T1 domain:** low-class purchases exist only on $[\Omega_2,\Omega_1)$ under T1.
   Above $\Omega_1$, T1 has no equilibrium in the strong economy.
4. **Uniqueness endpoints:** strong uniqueness ends strictly before $\Omega_2$ under T1 and T2.
   The weak T0 bound includes equality.
5. **Shared profiles:** M and M′ coincide at $\Omega_2$.
   M coincides with S at $\Omega_1$.
6. **Regime boundary:** the complete correspondence needs $\tau<1$.
   The current $\tau\le1$ statement omits additional T2 preparation choices at equality.
7. **Informative entry:** equality in its upper bound needs $\beta_H=1$ and $e_2=1$.
   The phrase about no interior optimum must exclude only strict or unique optima.
8. **Selection:** the entry hump and informative plateau describe maxima over equilibria.
   They do not describe every selected branch.
9. **Belief rule:** the weak three-point cutoff uses the directional top belief.
   A standard D1 claim needs an explicit admissible response set, especially under T0 and T1.
10. **Return strength:** $r_2=3.6$ does not produce the three-point return with $c_H=6$.
    The memo's $r=9$ example does.
11. **Diagnostic label:** the original threshold output uses an infeasible full-entry formula at $r=4$.
    Its equilibrium gain is $0.112189588113397$.

## 5. What the original memo should change

1. Replace the rent-transfer headline with a statement about costly low-state preparation and lost challenger rent.
2. State positive challenger rent on interior M.
3. Add exact T1 and T2 domains wherever the low-class onset appears.
4. Write the complete three-point result for $1/2<\tau<1$.
5. Count distinct profiles at the branch endpoints.
6. Identify every entry optimum as a maximum over equilibria.
7. Replace the claim about no interior optimum with a flat set of optimal stakes.
8. Add both equality conditions to the informative-entry bound.
9. State the directional belief as an explicit completion.
10. Retain the formal D1 extension as open until the receiver game and response set are specified.
11. Retain the exact thresholds, five-equilibrium example, and strong-economy nonexistence result.
12. Retain numerical-diagnostic labels for unproved shape and grid claims.

## 6. Plain summary

The independent calculations reproduce the main stake thresholds and the five discrete-Laplace equilibria at stake $0.36$.
The stake payoff is correct for shares held until the terminal sale.
The extra purchase already changes terminal holdings.

The three-point classification works in the strict recruiting regime under the stated directional belief.
Its endpoints and tie systems need clearer domains.
Under the paper's challenger tie rule, no equilibrium exists above stake $2.5988$ in the strong economy.
A challenger who can mix restores a unique equilibrium.

The claim about a complete rent transfer is false.
At the peak manipulation profile, shareholders gain $0.024$ while challenger profit falls by $0.307$.
Extra preparation costs destroy most of that loss.
The stated comparison loses $96.67\%$ of the surplus from price information.

The informative-entry plateau concerns the maximum over equilibria.
It does not describe every branch.
Its interior points are non-strict optima.
The weak three-point result depends on the unused-flow belief.
The discrete-Laplace example does not need that belief.
