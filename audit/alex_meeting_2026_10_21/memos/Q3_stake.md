# Point 3: an informed investor with an initial stake

## 1. Question and reading

This memo studies the stake extension in Section 3.3 of the shared brief.
The investor owns $\omega\geq0$ shares before it learns the challenger state.
Its payoff is

$$
\omega V_T+q\{V_T-P(X)\}-k|q|,
\qquad q\in[-1,1].
$$

**Main result — analytical.** A positive stake adds an incentive to induce preparation.
This incentive favors purchases in both states when entry increases with flow.
Small stakes preserve the paper's unique full orders under an explicit bound.
Large stakes require a new equilibrium analysis.
In particular, both types buying the same order is not an equilibrium.

**Important premise correction — analytical.** The paper's weak economy excludes expensive entry at the prior, not at every feasible belief.
The stronger exclusion in the task cannot hold alongside Proposition 2(A2).
Section 3, Result 3 separates the hypothetical exclusion from the actual benchmark.

The source is `overleaf/paper/main.tex`, Sections 2–4, 6.1, and Appendix A.1–A.2.
All derivations below use fixed price and entry schedules for unilateral deviations.
Prices and beliefs are recomputed only for a new candidate equilibrium.

## 2. Formal setup

All assumptions remain as in the paper, except for the initial stake.
The stake is a known, fixed parameter and carries no control rights.
The investor cannot buy the target or intervene directly in its operations.
The stake does not reveal the state before trade.
Short positions remain feasible under the pinned order interval.

One unit is the paper's small order unit.
Thus, $\omega=2$ means twice the maximum order size, not twice the target's outstanding shares.
The cost of the initial stake is sunk and does not affect order choice.
Its omission affects payoff levels but not the comparisons below.

Write $\Delta=\Delta_T=t_H-t_L$ and

$$
w_\theta=t_\theta-t_0,\qquad
w_H=w_L+\Delta.
$$

For the uniform incumbent,

$$
w_L=\frac{(\ell-p)(2r-\ell-p)+2p^2}{2r}>0,
\qquad
w_H=\frac{(r-p)^2+2p^2}{2r}>0.
\tag{S1}
$$

The inequalities follow from $r>\ell>p>0$.
Entry raises target proceeds in both states.

Maintain the low-cost floor $c_L<B_r(m)$, where

$$
m=\frac{1}{1+e^{2/b}},\quad M=1-m,\quad
\tau=\frac{c_H-g_L}{g_H-g_L}.
$$

For a candidate order profile, define

$$
D=\{x:\mu_X(x)\geq\tau\},\qquad
e(x)=\rho+(1-\rho)\mathbf1_D(x),
$$

$$
a(q)=\int_D f(x-q)\,dx,\qquad
\bar e(q)=\rho+(1-\rho)a(q).
\tag{S2}
$$

Here $a(q)$ is the probability of a flow that induces expensive entry.
It is not the unconditional probability that the challenger enters.
For arbitrary mixed profiles, $D$ need not be a half-line.

Define the residual integrals

$$
G_H(q)=\int f(x-q)e(x)\Delta[1-\mu_X(x)]\,dx,
$$

$$
G_L(q)=\int f(x-q)e(x)\Delta\mu_X(x)\,dx.
\tag{S3}
$$

Both are positive.
The paper's notation satisfies $F_H(s)=G_H(s)$ and $F_L(s)=G_L(-s)$.
All primes below denote derivatives with respect to the signed order $q$.

## 3. Results

### Result 1 — analytical: the marginal payoff has two distinct parts

The stake does not change the auction identities or Bayesian price sufficiency.
Conditional on the state and flow,

$$
v_\theta(x):=\mathbb E[V_T\mid\theta,x]
=t_0+w_\theta e(x).
$$

Competitive prices still satisfy

$$
P(x)=t_0+e(x)[w_L+\Delta\mu_X(x)].
$$

Subtract these expressions.
The residuals remain exactly those in equation (11):

$$
v_H-P=e\Delta(1-\mu_X),\qquad
v_L-P=-e\Delta\mu_X.
$$

The initial stake does not create a second residual on the new trade.
Instead, expected total payoffs become

$$
U_H(q;\omega)=\omega[t_0+w_H\bar e(q)]+qG_H(q)-k|q|,
$$

$$
U_L(q;\omega)=\omega[t_0+w_L\bar e(q)]-qG_L(q)-k|q|.
\tag{S4}
$$

For $q\neq0$, their derivatives are

$$
\begin{aligned}
U_H'(q;\omega)
&=\underbrace{G_H(q)+qG_H'(q)-k\operatorname{sgn}(q)}_{\text{trade and its cost}}
+\underbrace{\omega w_H\bar e'(q)}_{\text{initial stake}},\\
U_L'(q;\omega)
&=\underbrace{-G_L(q)-qG_L'(q)-k\operatorname{sgn}(q)}_{\text{trade and its cost}}
+\underbrace{\omega w_L\bar e'(q)}_{\text{initial stake}}.
\end{aligned}
\tag{S5}
$$

Use the appropriate cost derivative on each side of zero.
The stake term is $\omega\,\partial_q\mathbb E[V_T\mid\theta,q]$.
It measures a change in terminal proceeds through entry.
It is not $\omega P'(X)$.

In particular, $t_0$ still cancels from the trading residual.
It remains relevant to the stake through $w_\theta=t_\theta-t_0$.
The constant component $\omega t_0$ has zero derivative.

### Result 2 — analytical: the Laplace density gives a global stake bound

For almost every $x$,

$$
\partial_q f(x-q)
=\frac{\operatorname{sgn}(x-q)}{b}f(x-q).
$$

The entry set stays fixed during a deviation.
The same absolute-continuity argument as (A.5) therefore gives

$$
a'(q)=\frac1b\left[
\int_{D\cap(q,\infty)}f(x-q)\,dx
-\int_{D\cap(-\infty,q)}f(x-q)\,dx
\right].
\tag{S6}
$$

Each integral lies between zero and $1/2$.
Their sum is $a(q)$.
The difference also has absolute value at most $1-a(q)$.
Thus

$$
|a'(q)|\leq\frac{\min\{a(q),1-a(q)\}}b
\leq\frac1{2b},
$$

$$
\boxed{\quad
|\omega w_\theta\bar e'(q)|
\leq\frac{\omega(1-\rho)w_\theta}{2b}.
\quad}
\tag{S7}
$$

This bound holds for arbitrary mixed candidate orders and nonmonotone entry sets.
It improves the direct bound $\omega(1-\rho)w_\theta/b$ by a factor of two.
The derivative falls on the density, not on an entry indicator or a price jump.

The same argument gives

$$
|G_\theta'(q)|\leq G_\theta(q)/b,\qquad
\rho m\Delta\leq G_\theta(q)\leq\Delta.
\tag{S8}
$$

For full orders $(1,-1)$, $D=[x^*,\infty)$ and

$$
x^*=\frac b2\log\frac\tau{1-\tau}\in(0,1).
$$

Then the formulas sharpen to

$$
a(q)=
\begin{cases}
\frac12 e^{(q-x^*)/b},&q\leq x^*,\\
1-\frac12e^{(x^*-q)/b},&q\geq x^*,
\end{cases}
\qquad a'(q)=f(x^*-q)>0.
\tag{S9}
$$

Thus, for this schedule, every increase in the order raises the initial stake's expected payoff in both states.

### Result 3 — analytical, with an open uniqueness issue: the weak economy needs a premise correction

**Hypothetical stronger exclusion.** Suppose $B_{r_0}(M)<c_H$ and the low-cost floor holds.
Then every candidate schedule has $e(x)=\rho$.
Consequently,

$$
\bar e'(q)=0,\qquad
U_\theta(q;\omega)-U_\theta(0;\omega)
=U_\theta(q;0)-U_\theta(0;0).
\tag{S10}
$$

If $\Delta_T(r_0)<k$, the original proof makes zero the unique optimal order.
This conclusion holds for every $\omega$ under that stronger exclusion.

**Actual Proposition 2.** Its assumption is only $B_{r_0}(1/2)<c_H$.
Moreover, $B_r(M)$ decreases strictly with $r$.
Assumption (A2) therefore implies

$$
B_{r_0}(M)>B_{r_1}(M)>c_H.
\tag{S11}
$$

Expensive entry is feasible at favorable beliefs in the weak economy.
The hypothetical stronger exclusion cannot describe the paper's $r_0$ in this comparison.
At the benchmark,

$$
B_{1.2}(1/2)=4.804167<6,
\qquad B_{1.2}(M)=6.879843>6.
$$

**No-trade existence survives for every stake.** Under zero orders, the posterior is $1/2$ at every flow.
Price and entry are constant, including for every unilateral deviation.
The stake term is therefore zero against this schedule.
Correctly signed deviations earn

$$
|q|\left(\frac{\rho\Delta_T(r_0)}2-k\right)<0.
$$

Thus, the original no-trade equilibrium survives for every $\omega$.
This argument does not establish uniqueness across other candidate schedules.

**A sufficient uniqueness bound.** Equations (S7)–(S8) imply

$$
U_\theta(q;\omega)-U_\theta(0;\omega)
\leq |q|\left[
\Delta_T(r_0)-k+
\frac{\omega(1-\rho)w_H(r_0)}{2b}
\right].
$$

Consequently, no trade is uniquely optimal against every candidate schedule if

$$
\boxed{\quad
0\leq\omega<\Omega_0
:=\frac{2b[k-\Delta_T(r_0)]}{(1-\rho)w_H(r_0)}.
\quad}
\tag{S12}
$$

The benchmark value is $\Omega_0=0.0430976431$.
The exact loss of weak-economy uniqueness, if any, remains **open**.
Failure of this sufficient bound does not prove another equilibrium exists.

### Result 4 — analytical: an explicit bound preserves unique full orders

At $r_1$, define the positive trading margin

$$
\delta_1=\left(1-\frac1b\right)\rho m\Delta_T(r_1)-k>0.
$$

Equations (S5), (S7), and (S8) imply, on both sides of zero,

$$
U_H'(q;\omega)\geq
\delta_1-\frac{\omega(1-\rho)w_H}{2b},
$$

$$
U_L'(q;\omega)\leq
-\delta_1+\frac{\omega(1-\rho)w_L}{2b}.
\tag{S13}
$$

For example, $G_H+qG_H'\geq(1-|q|/b)G_H$.
The least favorable cost derivative is $-k$ for $H$ and $+k$ for $L$.
These observations give (S13) without a monotonicity assumption on entry.

Since $w_H>w_L$, the following condition makes both inequalities strict:

$$
\boxed{\quad
0\leq\omega<\Omega_U
:=\frac{2b\{(1-1/b)\rho m\Delta_T(r_1)-k\}}
{(1-\rho)[t_H(r_1)-t_0(r_1)]}.
\quad}
\tag{S14}
$$

Integrate the derivative inequalities across the order interval.
The only optimal orders are $q_H=1$ and $q_L=-1$.
Mixed strategies cannot support another optimal action.
The paper's full-order price construction then supplies existence.
This proves uniqueness among arbitrary mixed profiles.

The benchmark bound is

$$
\Omega_U=0.0114336479.
$$

This is the upper endpoint of the stated sufficient region.
It is not the largest stake that actually permits uniqueness.
For the full three-economy proposition, $\omega<\min\{\Omega_0,\Omega_U\}$ suffices.
At the benchmark, the minimum is $\Omega_U$.

### Result 5 — analytical formulas and numerical diagnostic: when the low type stops selling

Now fix the full-order price schedule at $r_1$.
The entry schedule is nondecreasing.
Hence, the stake reinforces the high type's positive derivative.
The high type uniquely buys one unit for every $\omega$ against this schedule.

Let $G=G_L$ and let $U_L^0(q)=-qG(q)-k|q|$.
For every $q>-1$,

$$
U_L(q;\omega)-U_L(-1;\omega)
=U_L^0(q)-U_L^0(-1)
+\omega w_L(1-\rho)[a(q)-a(-1)].
$$

The denominator below is strictly positive.
Thus, the exact full-profile existence cutoff is

$$
\boxed{\quad
\Omega_F=
\inf_{-1<q\leq1}
\frac{G(-1)-k+qG(q)+k|q|}
{w_L(1-\rho)[a(q)-a(-1)]}.
\quad}
\tag{S15}
$$

Full orders form an equilibrium precisely when $0\leq\omega\leq\Omega_F$.
Strict inequality makes $-1$ the unique low-type response to this schedule.
This condition does not exclude other equilibrium schedules.

For a local departure from $-1$, define $J=G_L(-1)=G_H(1)$.
Equation (S6), applied to the residual, gives

$$
G_L'(-1)=\frac{J-\rho m\Delta}{b}.
$$

The left tail contributes $\rho m\Delta/2$ to $J$.
Its density score has the opposite sign from the remaining integral.
Therefore, the local departure threshold is

$$
\Omega_{\mathrm{loc}}
=\frac{(1-1/b)J+\rho m\Delta/b-k}
{w_L(1-\rho)f(x^*+1)}.
\tag{S16}
$$

There is also an elementary expression for $J$:

$$
\begin{aligned}
J=\frac\Delta2\Big\{&(1+\rho)m+e^{-1/b}\big[
\rho\{\arctan(e^{x^*/b})-\arctan(e^{-1/b})\}\\
&\hspace{40mm}+\arctan(e^{1/b})-\arctan(e^{x^*/b})\big]\Big\}.
\end{aligned}
\tag{S17}
$$

To derive it, split the integral at $-1,x^*,1$.
The two tails contribute $\Delta(1+\rho)m/2$.
In the interior, use $y=e^{x/b}$.
The remaining integral is proportional to $\int(1+y^2)^{-1}\,dy$.

**Numerical diagnostic.** At the benchmark,

$$
J=0.14073122728303938,
\qquad \Omega_{\mathrm{loc}}=2.15846298141705929.
$$

The numerical infimum in (S15) occurs as $q\downarrow-1$.
It gives $\Omega_F\simeq2.1584629814$.
The integral and the closed form agree to twelve decimal places.
The global infimum is a numerical diagnostic, not an interval certificate.
For $\omega>\Omega_{\mathrm{loc}}$, failure of the full profile follows analytically from its positive low-type derivative at $-1$.

Buying eventually becomes attractive to the low type at the old schedule.
For example,

$$
U_L(1;\omega)>U_L(-1;\omega)
\iff
\omega>
\frac{G(1)+G(-1)}{w_L(1-\rho)[a(1)-a(-1)]}.
\tag{S18}
$$

The threshold is $3.7535763708$.
Full purchase also beats zero when $\omega>4.3623412231$.
These are comparisons between named actions, not global optimum thresholds.

The local derivatives at zero change signs at

$$
\frac{G(0)-k}{w_L(1-\rho)f(x^*)}=3.2636360919,
\qquad
\frac{G(0)+k}{w_L(1-\rho)f(x^*)}=3.9831858414.
$$

The first value concerns the derivative from the sale side.
The second concerns the derivative from the purchase side.
The numerical optima pass from a partial sale through zero to a partial purchase.
At $\omega=4$, the low type buys about $0.024650$ units.
At $\omega=5$, it buys about $0.981306$ units.

These purchases sacrifice the low type's trading residual to improve its initial stake.
They demonstrate a manipulation incentive against the old schedule.
They do not establish an equilibrium with low-type purchases.

### Result 6 — analytical restrictions and numerical diagnostic: the pure branch cannot reach pooled purchases

Under (A1)–(A3), every pure equilibrium at $r_1$ must have $q_H>q_L$.
To see this, first suppose $q_H<q_L$.
The Laplace posterior and entry schedule are then nonincreasing in flow.
The low type's trading derivative is strictly negative by the original bound.
Its stake derivative is nonpositive.
Thus, its unique response is $q_L=-1$, which contradicts $q_H<q_L$.

Equal orders give a constant posterior and constant entry.
The high type then chooses $1$, while the low type chooses $-1$.
Thus, equal orders cannot form a pure equilibrium.

For $q_H>q_L$, entry is nondecreasing.
The high type's trade and stake derivatives imply $q_H=1$.
Write the low order as $v<1$.
The largest posterior and the entry threshold are

$$
M(v)=\frac1{1+e^{-(1-v)/b}},
\qquad
x_c(v)=\frac{1+v}{2}+x^*.
\tag{S19}
$$

An equilibrium must induce expensive entry.
Otherwise, constant entry forces full orders, which themselves induce expensive entry by (A2).
Hence $M(v)\geq\tau$, or

$$
v\leq v_{\max}=1-b\log\frac\tau{1-\tau}=1-2x^*.
\tag{S20}
$$

At the benchmark, $v_{\max}=-0.7424448929$.
Thus, **every pure equilibrium still requires a substantial low-type sale**.
Low-type purchases cannot form a pure equilibrium at this vector.

For each candidate $v\in[-1,v_{\max}]$, recompute its posterior and residual integral $G_{L,v}$.
An interior low-type order must satisfy

$$
\omega(v)=
\frac{G_{L,v}(v)+vG_{L,v}'(v)-k}
{w_L(1-\rho)f(x_c(v)-v)}.
\tag{S21}
$$

This equation is a necessary condition.
A global order comparison is still required.

**Numerical diagnostic.** The computed pure branch runs from

$$
(\omega,v)=(2.1584629814,-1)
\quad\text{to}\quad
(2.4988548726,-0.7424448929).
$$

At nine displayed candidates, the global search returns the prescribed low order within numerical precision.
Entry falls from $0.5227572973$ to $0.5159574468$ along these candidates.
The high order remains $1$ by the derivative argument above.
At the final candidate, the upper posterior plateau equals $\tau$.
The paper's entry-at-indifference rule admits expensive entry on that entire tail.
For a slightly larger $v$, expensive entry disappears.

The apparent pure-branch endpoint is a numerical diagnostic.
A proof of its monotonicity and exhaustive pure-equilibrium coverage remains open.

### Result 7 — analytical exclusions; large-stake equilibrium remains open

**Pooled purchases fail for every stake.** Suppose both types buy one unit.
Then $a_H=a_L$, $\mu_X=1/2$, and entry equals $\rho$.
All flows have positive density, so there is no unused flow at which beliefs can punish a deviation.
The low type faces the fixed payoff

$$
U_L(q;\omega)=\omega[t_0+\rho w_L]
-q\frac{\rho\Delta}{2}-k|q|.
$$

Its gain from a deviation from $1$ to $0$ is $\rho\Delta/2+k>0$.
Its gain from $1$ to $-1$ is $\rho\Delta>0$.
Neither comparison depends on $\omega$.
The benchmark gains are $0.1033333333$ and $0.1666666667$.

More generally, identical conditional order distributions give constant beliefs and entry.
The distinct optimal orders then contradict those identical distributions.
Thus, an equilibrium at $r_1$ cannot lose all price information.

**A simple mixed purchase story also faces a strong restriction.** Suppose $H$ buys one unit.
Suppose $L$ sells one unit with probability $\beta$ and buys one unit otherwise.
Its upper posterior is

$$
\mu_+=\frac1{2-\beta+\beta e^{-2/b}}.
$$

Expensive entry requires

$$
\beta\geq\frac{2-1/\tau}{1-e^{-2/b}}=0.9200148224.
\tag{S22}
$$

Thus, low-type purchase probability cannot exceed about eight percent in this candidate family.
This is only an entry-feasibility restriction.
It does not establish low-type indifference or equilibrium.

**Very large stakes rule out every equilibrium with nondecreasing entry.** Suppose such an equilibrium exists.
The high type must choose $1$ by the positive derivative argument.
Entry cannot be constant, so it has a threshold $x_c\in[-1,1]$.
The posterior is constant outside that interval because all orders lie within it.
For every feasible $q$,

$$
\bar e'(q)=(1-\rho)f(x_c-q)
\geq\frac{1-\rho}{2b}e^{-2/b}.
$$

Equations (S5) and (S8) imply

$$
U_L'(q;\omega)
\geq
\frac{\omega w_L(1-\rho)}{2b}e^{-2/b}
-(1+1/b)\Delta-k.
$$

Hence, if

$$
\omega>
\frac{2be^{2/b}[(1+1/b)\Delta+k]}{(1-\rho)w_L},
\tag{S23}
$$

the low type must also choose $1$.
That contradicts the pooled-purchase calculation.
The benchmark sufficient threshold is $32.2635341385$.
Any equilibrium above this threshold must have nonmonotone entry and non-pure orders.
This statement does not prove such an equilibrium exists.

**Open.** The unrestricted large-stake equilibrium correspondence is unresolved.
The atom in preparation cost and the Laplace posterior plateaus also raise an existence issue.
Continuity arguments cannot simply ignore the entry jump at a plateau.

**Numerical diagnostic: failed attempt.** A bounded search considered a pure interior $H$ order and an $L$ mixture on $\{-1,1\}$.
It imposed the high-type marginal condition and low-type indifference.
At stakes $3,5,10,30,100$, the search found no valid candidate.
The smallest equation norm was about $0.7385$, well above zero.
The returned candidates also had profitable low-type deviations.
This failure does not exclude other mixed supports or establish nonexistence.

### Result 8 — analytical: part (iii) survives every stake

At $r_2$, the proposition explicitly assumes $B_{r_2}(M)<c_H$ and $c_L<B_{r_2}(m)$.
Thus, every candidate equilibrium has $e(x)=\rho$.
The stake term is identically zero for all deviations and all $\omega$.
The original global order argument remains valid because $\Delta_T(r_2)>\Delta_T(r_1)$.
The unique orders remain $(1,-1)$ and entry remains $\rho$.

There is no finite stake threshold at which part (iii) fails within this pinned model.
At the benchmark, $B_{3.6}(M)=5.9973110977<6$.
Its strict exclusion applies to every feasible belief, unlike the condition at $r_0$.

### Result 9 — analytical: shareholder gains, transfers, and welfare

The payoff identity

$$
\omega V_T+q(V_T-P)=(\omega+q)V_T-qP
\tag{S24}
$$

already counts the initial shareholder's proceeds correctly.
For a sale of $s$ units, it becomes $sP+(\omega-s)V_T$.
The shareholder receives the price on shares sold and terminal proceeds on the retained position.
An additional $\omega P$ term would count the same asset twice.

A higher transaction price transfers cash from the purchaser to the seller.
A price revision can also reflect news about expected terminal proceeds.
Neither observation implies a new aggregate payoff from the price level alone.
By contrast, a change in entry alters the auction outcome and $V_T$.
The initial shareholder gains $\omega w_\theta$ per unit increase in entry probability.
This gain is positive in both states.

The model's roles can therefore be stated as follows:

| Role | Interpretation and payoff exposure |
|---|---|
| Informed investor | A noncontrolling specialist investor with private information about acquisition quality; initial stake $\omega$ and final position $\omega+q$. |
| Noise traders | Investors whose liquidity or portfolio demand produces $Z$; their demand is independent of the acquisition state. |
| Market makers | Competitive counterparties who infer quality from aggregate flow and quote expected terminal proceeds. |
| Other shareholders | Owners who retain shares through the sale and receive $V_T$ on those shares. |

These are distinct economic roles.
An informed investor can also be an initial shareholder.
An outsider to the firm need not be a shareholder with zero holdings.
The pinned extension excludes direct control, voting effects, and bidder toeholds.

**Target proceeds.** At a fixed $r$, the price-hidden economy has entry $\rho$.
For any feedback equilibrium, its expected revenue gain is

$$
\frac{1-\rho}{2}
\left[w_H\Pr(D\mid H)+w_L\Pr(D\mid L)\right]\geq0.
\tag{S25}
$$

This is strictly positive whenever expensive entry occurs with positive probability.
At $r_1$, every equilibrium must have such entry by Result 6's constant-entry contradiction.
Thus, if an equilibrium exists, price access still raises target proceeds and high-value ownership.
The ownership gain is $(1-\rho)\Pr(D\mid H)/2>0$.

**Acquisition surplus.** Shareholder proceeds include transfers from bidders and are not themselves total surplus.
Let $W_\theta$ be the expected increase in realized asset value from challenger preparation, before its cost.
For $R\geq p$, the gain equals $(\theta-R)_+$.
For $R<p$, entry creates a sale worth $\theta$, while the challenger retains only $\theta-p$.
Therefore,

$$
W_\theta=g_\theta+pF_R(p)
=g_\theta+\frac{p^2}{r}.
$$

At every price that induces expensive entry,

$$
\mathbb E[W_\theta-c_H\mid P]
=B_r(\mu(P))-c_H+\frac{p^2}{r}
\geq\frac{p^2}{r}>0.
\tag{S26}
$$

This conditional inequality uses equilibrium beliefs, including any stake-induced distortion of orders.
It does not apply to a unilateral low-type deviation evaluated by the investor's private information.
For example, expensive entry in state $L$ costs more than its allocation benefit at the benchmark.
That state-specific loss does not reverse the positive conditional inequality in equilibrium.

At $r_1$, hidden prices imply constant entry and full orders for every stake.
Their expected trading cost is $k$.
Any feedback profile has expected cost at most $k$, since $|q|\leq1$.
Thus, any existing feedback equilibrium improves total surplus relative to hidden prices, including the trading cost if it is a resource cost.
The full-order uniqueness claim is less robust than this welfare comparison.

**Dividend invariance.** Add the same deterministic external dividend $d$ to the traded claim and its price.
The residual remains $V_T-P$, while the initial stake gains the constant $\omega d$.
Every order comparison remains unchanged.
Section 6.1's diagnostic therefore survives the stake extension.

### Result 10 — analytical comparison, with source checks: the closest literature does not supply the missing equilibrium

The records below distinguish a checked statement from an unverified derivation.
Their model comparisons follow from the payoff split in (S5).

1. **Kyle and Vila (1991), RAND Journal of Economics 22(1), 54–71, “Noise Trading and Takeovers.”**
   The bibliographic record is verified on [Kyle's faculty page](https://www.rhsmith.umd.edu/directory/albert-pete-kyle) and the [journal issue record](https://www.jstor.org/stable/i344676).
   The primary article text was not accessible.
   Its specific camouflage mechanism and theorem statements remain **unverified** here.
   The brief identifies it as the takeover antecedent.
   Do not use it as evidence that this paper's passive shareholder extension has a particular equilibrium.

2. **Edmans, Goldstein, and Jiang (2015), American Economic Review 105(12), 3766–3797.**
   The published location is Section II.E, “Zero Initial Position,” pp. 3787–3788, rather than Section 3.5.
   The [published paper](https://alexedmans.com/wp-content/uploads/2024/06/LTA.pdf) and [online Appendix B.2, pp. 14–18](https://www.aeaweb.org/articles/materials/4583) are verified.
   The appendix studies positive initial holdings and compares the buy-not-sell and sell-not-buy equilibria.
   Equation (14) removes the initial stake from their cutoff difference.
   Correct investment and correct disinvestment both increase the initial stake's value there.
   Here, a low-type sale deters entry and reduces target proceeds.
   The cancellation in their equation (14) therefore does not carry over.
   Their appendix also explicitly restricts its analysis to those two equilibrium forms.

3. **Goldstein and Guembel (2008), Review of Economic Studies 75(1), 133–164, “Manipulation and the Allocational Role of Prices.”**
   [Proposition 2 and Sections 4.2 and 6](https://www.bauer.uh.edu/nlangberg/papers_shiva/Goldstein%20Guembel%202007%20JFE.pdf) are verified.
   Their uninformed trader sells to distort investment and profit through a short position.
   Their profit argument uses multiple trade dates.
   Proposition 4 excludes profitable purchase-induced manipulation in their specified environment.
   Our stake creates a different source of gain: higher auction proceeds on an existing long position.
   Thus, “manipulation” describes the incentive in (S18), not an equilibrium established by their theorem.

4. **Maug (1998), Journal of Finance 53(1), 65–98, “Large Shareholders as Monitors.”**
   The [publisher's abstract](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.35053) is verified.
   It states that liquidity facilitates larger holdings and additional purchases, which can strengthen costly monitoring.
   This supports a stake-based governance interpretation.
   It concerns direct monitoring, whereas the pinned investor acts only through the price.
   Detailed proposition-level correspondence remains **unverified**.

5. **Kahn and Winton (1998), Journal of Finance 53(1), 99–129, “Ownership Structure, Speculation, and Shareholder Intervention.”**
   The [publisher's abstract](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.45483) is verified.
   It separates gains on existing holdings from gains on informed trades.
   It states that speculation can increase or reduce the incentive for intervention.
   That distinction matches the two terms in (S5).
   Its direct intervention choice is absent here; detailed theorem-level correspondence remains **unverified**.

6. **Back, Collin-Dufresne, Fos, Li, and Ljungqvist (2018), Econometrica 86(4), 1431–1463, “Activism, Strategic Trading, and Liquidity.”**
   The [publisher's abstract and bibliographic record](https://onlinelibrary.wiley.com/doi/abs/10.3982/ECTA14917) are verified.
   The paper solves dynamic trade with costly activism and reports technology-dependent liquidity effects.
   It also identifies an initial-stake invariance result for a broad class of activism technologies.
   This is a useful comparison for endogenous firm value.
   It does not establish stake invariance for the present price-induced entry mechanism.
   Detailed theorem-level correspondence remains **unverified**.

## 4. What changes relative to the current paper

| Paper item | Status under the stake extension |
|---|---|
| Auction formulas (4)–(6), Proposition 1 | **Analytical: unchanged.** The stake has no auction or control effect. |
| Posterior bounds (7)–(8), Proposition A.1 | **Analytical: unchanged.** The order interval and noise law stay fixed. |
| Price sufficiency (9)–(10), Proposition A.2 | **Analytical: unchanged** under the same low-cost floor. |
| Residual advantage (11) | **Analytical: unchanged as a trading residual.** Add the separate stake payoff in (S4). |
| Deviation regularity (A.5) | **Analytical: unchanged method.** Apply it also to the entry set, as in (S6). |
| Global order bound (A.6) | **Analytical: modified.** Deduct the worst-case stake derivative to obtain (S13). |
| Proposition 2(i), actual $r_0$ | **Analytical:** no trade exists for every stake; uniqueness holds under (S12). The exact uniqueness boundary is **open**. |
| Proposition 2(ii) | **Analytical:** unique full orders survive under (S14). The computed existence cutoff is about $2.158463$, a **numerical diagnostic**. |
| Equation (12) | **Analytical:** valid whenever full orders remain an equilibrium. Recompute it once the orders change. |
| Proposition 2(iii) | **Analytical: unchanged for every stake** under its stated entry exclusion. |
| Proposition A.3, fixed-experiment deterrence | **Analytical: unchanged.** The challenger still compares its gross profit with its cost. |
| Proposition A.4, no-trade existence condition | **Analytical: unchanged:** $\rho\Delta/2\leq k$, because a constant schedule gives no marginal stake effect. |
| Proposition 3 and its certificates | **Open for $\omega>0$.** The old marginal equations and concavity arguments omit the stake term. |
| Section 6.1, dividend diagnostic | **Analytical: unchanged incentives.** The initial stake gains only a constant. |
| Section 6.1, welfare comparison at $r_1$ | **Analytical:** the comparison survives for any existing equilibrium, by (S25)–(S26) and the order bound. |

The proposed general statement “all shareholders gain, so trading incentives are unchanged” is false.
Shareholders gain through the entry response, but this gain changes the investor's order choice.

## 5. Numerical example

**Status: numerical diagnostic**, except for the analytical formulas identified above.
The benchmark is

$$
(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02).
$$

The incumbent strengths are $(r_0,r_1,r_2)=(1.2,3,3.6)$.
At $r_1$,

$$
t_0=5/12,\quad t_L=7/8,\quad t_H=37/24,
\quad w_L=11/24,\quad w_H=9/8,\quad\Delta=2/3.
$$

Also, $\tau=141/200$ and $x^*=\log(141/59)=0.8712224465$.

Scripts:

- `audit/alex_meeting_2026_10_21/scripts/Q3_stake/stake_diagnostics.py`
- `audit/alex_meeting_2026_10_21/scripts/Q3_stake/mixed_diagnostic.py`

Run each command from the repository root:

```bash
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q3_stake/stake_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q3_stake/mixed_diagnostic.py
```

Both programs compute and print their results.
They contain no assertions and write no output files.
The calculations ran through these CLI commands on 21 October 2026.
The first program splits every integral at the order and entry breakpoints.
It uses absolute and relative quadrature tolerances of $2\times10^{-12}$.
The global order search uses 101 grid points and refines all grid maxima.

The cutoff calculation uses 2,001 trial orders and local refinement.
The closed form for $J$ and the local cutoff use 60 decimal digits.
These methods do not prove the global minimum or exclude every equilibrium.
The environment reports Python 3.12.13, NumPy 2.5.2, and SciPy 1.18.1.
The paper's SHA-256 at execution was `467a31f78467b50e6216a15b2f4d0c63e9db094681d20730b2a2e6d686bf774c`.

### Thresholds with different meanings

| Quantity | Stake $\omega$ | Meaning |
|---|---:|---|
| $\Omega_U$ | 0.011433648 | Sufficient uniqueness bound across all candidate schedules at $r_1$. |
| $\Omega_0$ | 0.043097643 | Sufficient uniqueness bound for no trade at the actual $r_0$. |
| $\Omega_F\simeq\Omega_{\mathrm{loc}}$ | 2.158462981 | Full-order existence cutoff at $r_1$; numerical global minimum, explicit local formula. |
| Computed pure-branch endpoint | 2.498854873 | The low order reaches the entry-feasibility ceiling. |
| Purchase beats full sale | 3.753576371 | Pairwise deviation comparison at the original full-order schedule. |
| Positive derivative at $0+$ | 3.983185841 | Local incentive to start a purchase at that fixed schedule. |
| Full purchase beats zero | 4.362341223 | Another pairwise comparison at that fixed schedule. |
| Full-purchase endpoint derivative | 5.081367956 | Local boundary condition at that fixed schedule. |
| Bound in (S23) | 32.263534139 | Sufficient exclusion of every equilibrium with nondecreasing entry. |

The gap between $0.011434$ and $2.158463$ reflects different claims.
The first excludes all competing schedules.
The second concerns existence of the full-order candidate alone.

### Payoffs at the fixed full-order schedule

The following affine formulas make every reported payoff reproducible:

$$
\begin{array}{c|rrr}
&q=-1&q=0&q=1\\ \hline
U_H(q;\omega)
&-0.144021935+0.863437628\omega
&0.970814596\omega
&0.120731227+1.146099625\omega\\
U_L(q;\omega)
&0.120731227+0.598684466\omega
&0.642430638\omega
&-0.311525340+0.713843057\omega
\end{array}
$$

These are total terminal payoffs under (S4), including the initial stake.
They are not profits net of that stake's historical purchase cost.

| $\omega$ | State | Sell one | No trade | Buy one | Best signed order |
|---:|:---:|---:|---:|---:|---:|
| 0 | H | -0.144022 | 0.000000 | 0.120731 | 1.000000 |
| 0 | L | 0.120731 | 0.000000 | -0.311525 | -1.000000 |
| 1 | H | 0.719416 | 0.970815 | 1.266831 | 1.000000 |
| 1 | L | 0.719416 | 0.642431 | 0.402318 | -1.000000 |
| 3 | H | 2.446291 | 2.912444 | 3.559030 | 1.000000 |
| 3 | L | 1.916785 | 1.927292 | 1.830004 | -0.245680 |
| 3.5 | H | 2.878010 | 3.397851 | 4.132080 | 1.000000 |
| 3.5 | L | 2.216127 | 2.248507 | 2.186925 | 0.000000 |
| 4 | H | 3.309729 | 3.883258 | 4.705130 | 1.000000 |
| 4 | L | 2.515469 | 2.569723 | 2.543847 | 0.024650 |
| 5 | H | 4.173166 | 4.854073 | 5.851229 | 1.000000 |
| 5 | L | 3.114154 | 3.212153 | 3.257690 | 0.981306 |
| 10 | H | 8.490354 | 9.708146 | 11.581727 | 1.000000 |
| 10 | L | 6.107576 | 6.424306 | 6.826905 | 1.000000 |

Rows beyond the full-order cutoff are deviation diagnostics.
They must not be read as equilibrium outcomes at those stakes.

### Pure candidates with recomputed prices

| $\omega$ | $q_H$ | $q_L$ | Expected entry |
|---:|---:|---:|---:|
| 2.158462981 | 1 | -1.000000000 | 0.522757297 |
| 2.248537059 | 1 | -0.935611223 | 0.521098159 |
| 2.335345877 | 1 | -0.871222446 | 0.519412097 |
| 2.418811329 | 1 | -0.806833670 | 0.517698674 |
| 2.498854873 | 1 | -0.742444893 | 0.515957447 |

These candidates satisfy the own-order marginal condition.
The numerical deviation search found gains no larger than floating-point roundoff at the displayed candidates.
This is evidence for the branch, not a completeness or uniqueness proof.

## 6. Open issues and risks

1. **Open: exact uniqueness limits.** The bounds $\Omega_0$ and $\Omega_U$ are sufficient.
   Their failure does not locate a new equilibrium.
   The first appearance of another mixed equilibrium remains unresolved.
2. **Open: large-stake existence.** Pooled purchases fail, and sufficiently large stakes exclude nondecreasing entry.
   A general existence result must address mixed orders, nonmonotone entry, and posterior plateaus.
3. **Open: global proof at the computed cutoff.** The local formula is explicit.
   The equality $\Omega_F=\Omega_{\mathrm{loc}}$ at this vector currently rests on numerical minimization.
4. **Open: exhaustive pure continuation.** The displayed branch has strong numerical support.
   Its monotonicity and the exclusion of other pure roots need proof.
5. **Conjecture: cost smoothing may ease existence analysis.** An atomless cost distribution would remove the discrete entry jump.
   It would change the pinned model and would not itself prove uniqueness.
6. **Model boundary.** The order unit is not a fraction of outstanding equity.
   Large numerical $\omega$ does not establish a realistic blockholder size without a separate scale choice.
7. **Literature boundary.** Several sources were checked only at the abstract level.
   Kyle and Vila's primary mechanism remains unverified in this review.

## 7. Recommendation

1. Explain the four investor and shareholder roles in Section 2.3.
   State that the baseline investor starts with no shares and has no control rights.
   Explain that retained shares receive the auction payoff.
2. Add the payoff split (S4)–(S5) as a short stake extension.
   Use (S14) as the initial analytical robustness result.
   State its sufficient nature and report its scale in order units.
3. Correct the weak-economy premise before any broader stake claim.
   Retain the distinction between no-trade existence and uniqueness.
   Part (iii) requires no new stake restriction.
4. Present the $2.158463$ cutoff and the partial-sale branch as numerical diagnostics.
   Separate fixed-schedule deviations from candidates with recomputed prices.
5. Do not describe both types buying as a manipulation equilibrium.
   The pinned model rejects that outcome.
   Treat unrestricted large-stake equilibrium as a separate research question.
6. Cite Edmans, Goldstein, and Jiang's actual appendix and explain the different low-state incentive.
   Use Goldstein and Guembel for the feedback-manipulation question, not as a theorem that resolves this extension.

## 8. Plain summary

An existing shareholder does benefit when another bidder raises the sale proceeds.
The current model omits that incentive because its informed investor starts with no shares.
An initial stake adds the missing gain explicitly.

The new gain changes behavior.
When a purchase makes bidder entry more likely, it raises the stake's value in both states.
A low-value investor can then prefer a purchase despite a loss on the new shares.
It can recover that loss through better proceeds on its initial shares.

Small stakes preserve the paper's result under an analytical bound.
At the benchmark, a stake below 0.011434 order units guarantees unique full orders.
The original full-order equilibrium appears to survive until about 2.158463 units.
These thresholds answer different questions.

After that cutoff, the computed candidate branch has smaller low-type sales.
It reaches an entry-feasibility boundary near 2.498855 units.
The behavior beyond that branch remains unresolved.
Both types buying the same amount cannot be an equilibrium: that makes prices uninformative, and the low type prefers to sell.

The weak-economy premise also needs correction.
The paper rules out expensive entry at its uninformative price, not at every possible belief.
No trade remains an equilibrium for every stake, but its unrestricted uniqueness is not proved.
In the strongest economy, expensive entry really is impossible at every belief.
Its original result survives every stake.

The best immediate revision is a clear description of who owns the shares, plus the small-stake result.
A higher transaction price is a transfer.
The substantive shareholder gain comes from the bidder's effect on the final auction payoff.
