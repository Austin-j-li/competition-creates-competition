# XN4: Independent check of strategic traders

## 1. Scope

This memo checks the five requested claims in `memos/N4_strategic_traders.md`.
The background sources are T2, variant V3, and `memos/X_check.md`.
The paper source is commit `01bd5d6` in `overleaf/paper`.
I read its auction, information, and payoff definitions.

The benchmark is

$$
(h,\ell,p,\rho,c_L,c_H,k,\pi,\lambda,\beta)
=(10,1,1/2,1/4,0,6,1/50,1/2,6/17,1/3).
$$

The menu is $\{-1,0,1\}$, with one order slot and no separate noise.
An equilibrium uses Bayes' rule, competitive prices, and optimal orders and preparation.
IM permits an order mixture at indifference; I0 requires the zero order at indifference.
C1 requires preparation at indifference; CM permits a preparation mixture.
The holder analysis uses the passive prior at an unused zero flow.
Every counterexample below has positive probability at each flow and three distinct prices.

**Method and evidence.** I wrote the independent arithmetic from scratch.
It uses rational integration, rational formulas, and rational root brackets.
It imports no source solver.
I ran it before any N4 program.
Later, I ran all four N4 programs and replayed the omitted profiles through their interfaces.

The evidence is under `scripts/XN4_check/`:

- `independent.py` and `independent.out.txt`: auction objects, holder outcomes, welfare, liquidity roots, and presence calculations.
- `refinements.py` and `refinements.out.txt`: exact counterexamples for N4.2 and N4.3.
- `algebra.py` and `algebra.out.txt`: polynomial root counts and uniform payoff bounds.
- `boundaries.py` and `boundaries.out.txt`: the stake endpoints and the I0 counterexample.
- `source_replay.py` and `source_replay.out.txt`: the omitted profiles in the source interfaces.
- `n41_holder.rerun.txt` through `n44_liquidity.rerun.txt`: fresh source output.

Every script prints results. No script uses assertions.
All runs used the slot wrapper, with at most three concurrent slots.

## 2. Verdict table

| Claim | Verdict | Evidence |
|---|---|---|
| N4.1: the holder never sells and buys only to recruit | **CONFIRMED** | Section 3.2 removes the assumed order ranking from the proof. |
| N4.1: the phase at 3 and the welfare interpretation | **CONFIRMED WITH CORRECTION** | Both stake thresholds are exact. The endpoint counts, C1 uniqueness, proceeds qualification, and holder trade ledger need corrections. Sections 3.2–3.3. |
| Recovered result: a unique informative equilibrium with rising entry | **REFUTED** | The rising branch exists. Another informative equilibrium survives throughout the proposed window. The source interface accepts it. Section 3.4. |
| N4.4(a): a holder with shocks and a small stake implements V3 | **CONFIRMED WITH CORRECTION** | The implementation works with forced shocks and the stated payoff inequality. The general uniqueness claim fails. Section 3.5. |
| N4.4(b): endogenous participation gives two equilibria near the ceiling | **CONFIRMED WITH CORRECTION** | Under C1 the exact local band is $(3.110599269\ldots,3.783854861\ldots]$. Under CM there are three interior outcomes. Section 3.6. |
| N4.2: challenger orders and presence threshold $352/3417$ | **CONFIRMED WITH CORRECTION** | The fraction marks complete purchase suppression. A partial informed purchase creates multiplicity already above $308000/3830457$. Section 3.7. |
| N4.3: incumbent orders and presence threshold $0.0765$ | **REFUTED** as a threshold claim | Orders reveal the incumbent value. The corrected floor branch starts above $0.059895768\ldots$. A strict counterexample uses $\chi=0.06$. Section 3.8. |

## 3. Derivations

### 3.1 Auction objects and information

**Status: analytical and computer-assisted.**

The independent program integrates the auction payments over $R\sim U[0,r]$.
For example,

$$
\begin{aligned}
t_H&=\frac1r\left[\int_0^p p\,dR+\int_p^r R\,dR\right],\\
t_L&=\frac1r\left[\int_0^p p\,dR+\int_p^1 R\,dR+\int_1^r1\,dR\right],\\
g_H&=\frac1r\left[\int_0^p(10-p)\,dR+\int_p^r(10-R)\,dR\right],\\
g_L&=\frac1r\left[\int_0^p(1-p)\,dR+\int_p^1(1-R)\,dR\right].
\end{aligned}
$$

These integrals agree with equation (4) of the pinned paper.
At $r=3$ they give

$$
(t_0,t_H,t_L,g_H,g_L,\Delta,W)
=(5/12,37/24,7/8,203/24,1/8,2/3,19/24).
$$

Here $\Delta=t_H-t_L$ and $W=(t_H+t_L)/2-t_0$.
Also,

$$
\tau(r)=\frac{48r-3}{4(20r-r^2-1)},\qquad
b=c=\frac{11}{51},\qquad M=\frac{29}{40}.
$$

The usual price formula requires the original distribution of $R$ conditional on the class and flow.
That condition holds for N4.1 and N4.4.
It fails when the incumbent trades on its private value in N4.3.

### 3.2 The holder's order and the phase at strength 3

**Status: analytical; exact values are computer-assisted.**

Let $s,t$ be the informed purchase and sale probabilities.
Let $m,m_-$ be the free holder's purchase and sale probabilities.
The holder gains, relative to zero, are

$$
\begin{aligned}
G_+&=\omega(e_+-e_0)W+e_+\Delta(1/2-\mu_+)-k,\\
G_-&=\omega(e_--e_0)W+e_-\Delta(\mu_--1/2)-k.
\end{aligned}
$$

The negative flow has $\mu_-\le1/2<\tau$, so $e_-=\rho$.
Since $e_0\ge\rho$, both terms before $-k$ in $G_-$ are nonpositive.
Thus $G_-<0$ at every stake.
This proof does not require $s\ge t$.

It follows that $m_-=0$.
The informed gross returns are then

$$
K_H=e_+\Delta\frac{b+cm}{\lambda s+2(b+cm)},\qquad
K_L=\rho\Delta\frac b{\lambda t+2b}.
$$

Suppose $s<t$.
Then $K_H>K_L$, because $b+cm\ge b$ and $e_+\ge\rho$.
Since $t>0$, optimality requires $K_L\ge k$.
Therefore $K_H>k$, which requires $s=1$ and contradicts $s<t$.
Hence $s\ge t$, so $\mu_0\le1/2$ and $e_0=\rho$.

If $e_+=\rho$, then $G_+=\rho\Delta(1/2-\mu_+)-k<0$.
Thus a free purchase requires extra preparation at its flow.
Both structural claims hold.

At $r=3$, either correctly signed informed order has net return at least

$$
\rho\Delta\frac b{\lambda+2b}-k=\frac{31}{1200}>0.
$$

Therefore $s=t=1$ in every equilibrium at this strength.
Now

$$
\mu_+(m)=\frac{\lambda+b+cm}{\lambda+2b+2cm},\qquad
G_+(m)=\omega(1-\rho)W-\Delta[\mu_+(m)-1/2]-k
$$

on the full-entry piece.
The gain rises strictly in $m$.
Its endpoint conditions give

$$
\Omega_1=\frac{\Delta(M-1/2)+k}{(1-\rho)W}=\frac{136}{475},\qquad
\Omega_2=\frac{\Delta(\tau-1/2)+k}{(1-\rho)W}=\frac{376}{1425}.
$$

The threshold posterior requires

$$
m_{\max}=\frac{80}{451}.
$$

An interior holder mixture on the full-entry piece satisfies

$$
m^*=\frac{\lambda\Delta/(2A)-\lambda-2b}{2c},\qquad
A=\omega(1-\rho)W-k.
$$

At $m=m_{\max}$, holder indifference instead gives

$$
e^*=\frac{k+\rho\omega W}{\omega W-\Delta(\tau-1/2)}.
$$

The complete phase under IM/CM is:

| Stake | Distinct equilibria |
|---|---|
| $\omega<\Omega_2$ | V3 |
| $\omega=\Omega_2$ | V3 and M′, with $e^*=1$ |
| $\Omega_2<\omega<\Omega_1$ | V3, M, and M′ |
| $\omega=\Omega_1$ | V3 and M′; M collapses into V3 |
| $\omega>\Omega_1$ | M′ |

Under C1/IM, M′ survives only at $\Omega_2$.
Thus two equilibria exist at $\Omega_2$, contrary to the corollary's weak uniqueness bound.
Two also exist on $(\Omega_2,\Omega_1)$: V3 and M.
At $\Omega_1$, only V3 remains under C1/IM.
Above $\Omega_1$, C1/IM gives no equilibrium.
Under I0, only V3 remains for $\omega\le\Omega_1$; none exists above it.

There is a small algebra error in Proposition 1's proof.
At $e=\rho$, the holder gain is

$$
G_+(\rho)=-\rho\Delta(\tau-1/2)-k<0,
$$

rather than $-k$.
The formula for $e^*$ remains correct.

### 3.3 Proceeds, rents, and welfare

**Status: computer-assisted, with an analytical accounting identity.**

For class $j$ and flow $x$, the program sums target payments and bidder profits separately.
Let $S_0=\mathbb E[R\mathbf1\{R\ge p\}]$ and $S_j=\mathbb E[\max(R,\theta_j)]$.
The social payoff is

$$
\mathcal W=\frac12\sum_{j,x}a_j(x)
\{S_0+e_x(S_j-S_0)-6(e_x-\rho)\}
-k[\lambda+2b+cm].
$$

The exact auction identity is

$$
S-\text{preparation}=T+\Pi_{\rm challenger}+\Pi_{\rm incumbent}.
$$

The independent program prints zero for its residual in every welfare row.
The main source welfare values reproduce:

| Outcome | Target proceeds | Challenger net | Social payoff |
|---|---:|---:|---:|
| Hidden price | 0.614583333 | 1.072916667 | 2.536397059 |
| V3 | 0.891544118 | 1.121936275 | 2.609926471 |
| M, $\omega=0.27$ | 0.907620147 | 1.087245895 | 2.576386796 |
| M′, $\omega=\Omega_2$ | 0.914260521 | 1.072916667 | 2.562532879 |
| M′, $\omega=0.3$ | 0.829228151 | 1.072916667 | 2.554899812 |
| M′, $\omega=10$ | 0.617365255 | 1.072916667 | 2.535881598 |

Thus manipulation raises proceeds near its onset, but not at every stake.
At $\Omega_2$, the proceeds gain over V3 is $95/4182$.
The challenger loses $5/102$, which exceeds that proceeds gain.
This change is not an equal transfer of the whole rent to shareholders.

The discovery gain falls from $5/68$ to $1093/41820$ at $\Omega_2$.
Only $1093/3075$, or 35.5%, remains.
At stake 10, the social payoff falls below the hidden-price value.
The claim about the loss of most discovery surplus therefore holds.

**Holder trade correction.** Let $\ell_q=q(v_U(q)-P(q))-k|q|$.
The correct trade profit is

$$
\Pi_U^{\rm trade}=b(\ell_++\ell_-)+cm\ell_+.
$$

The source multiplies the last term by $1-\lambda$ a second time.
For example, the correct value at $\Omega_2$ is $-43649/836400=-0.052186753$.
The memo reports about $-0.0501$.
This error affects holder trade profit and total profit.
It does not affect the reported proceeds or social payoff.

### 3.4 The recovered entry rise: existence holds; uniqueness fails

**Status: analytical refutation, with exact counterexamples.**

The full-purchase M′ branch reproduces the reported entry values:

| Stake | Entry at 1.55 | Entry at 1.60 | Entry at 1.65 |
|---|---:|---:|---:|
| $7/50$ | 0.526748274 | 0.535757909 | 0.546267367 |
| $3/20$ | 0.503570286 | 0.510910199 | 0.519453757 |

However, another informative equilibrium survives.
Set $m=t=0$, and choose

$$
s_T=\frac{b(2\tau-1)}{\lambda(1-\tau)},\qquad
e_T=\frac{k}{\Delta(1-\tau)}.
$$

Then $\mu_+=\tau$ and the informed H is indifferent.
The informed L strictly prefers zero at each requested strength.
The free holder's purchase gain is

$$
G_+=(e_T-\rho)W(\omega-\bar\omega_H),\qquad
\bar\omega_H=\frac{k\Delta}{2W[k-\rho\Delta(1-\tau)]}.
$$

Therefore this partial-purchase equilibrium exists whenever $\omega\le\bar\omega_H$ under IM/CM.
Its entry does not depend on the stake:

| Strength | $s_T$ | $e_T$ | Entry |
|---|---|---|---:|
| $31/20$ | $5093/10026$ | $195548/336985$ | 0.350846408 |
| $8/5$ | $517/999$ | $2528/4995$ | 0.328627877 |
| $33/20$ | $38819/73638$ | $1545852/3456895$ | 0.310872117 |

At stake $7/50$, the source payoff interface accepts every row as an equilibrium.
It returns optimal choices for both informed classes, the holder, and the challenger.
The source candidate list omits all these partial informed purchases.
Thus the proposed window has at least two informative equilibria at each strength.
No trade also remains an equilibrium.

**Endpoints.** The exact proposed bounds are

$$
\omega_a=\frac{859}{6445}=0.133281613654\ldots,\qquad
\omega_b=\frac{94645232}{516885327}=0.183106826710\ldots.
$$

The other upper bounds are $20224/86989$ and $1044995952/3514475257$.
They exceed $\omega_b$.
At $\omega_a$, V3 also survives at strength 1.65 under IM.
At $\omega_b$, the full-purchase M′ branch still exists under IM.
The informed H becomes indifferent there at strength 1.55.
A continuum then connects that outcome to the partial-purchase outcome.

To see the continuum, fix $e=e_T$ and let $s\in[s_T,1]$.
Set

$$
m(s)=\frac{\lambda s(1-\tau)/(2\tau-1)-b}{c}.
$$

The posterior stays at $\tau$.
Both the holder and the informed H remain indifferent.
Thus the closed upper endpoint supports additional outcomes.
It is not an equilibrium failure.

The entry rise on M′ holds throughout $[\omega_a,\omega_b]$.
Write $d_i=\Delta_i(\tau_i-1/2)$ and

$$
A_i=\frac{\lambda[k+\rho d_i]}{2(2\tau_i-1)}.
$$

Then $\mathsf E_i=\rho+A_i/(\omega W_i-d_i)$.
Each adjacent entry difference has a linear numerator in $\omega$.
The exact program prints positive values at both interval endpoints.
The denominators are positive, so both differences stay positive throughout the interval.

CM is essential for this M′ branch because $\rho<e^*<1$ throughout the proposed window.
IM is also essential because the free holder uses both zero and purchase.
The corrected result is an ascending equilibrium selection, not a unique informative equilibrium.

### 3.5 Exact conditions for the liquidity foundation

**Status: analytical, with an exact counterexample to the broad uniqueness claim.**

The holder implements the exogenous V3 law only if its free choice is zero.
The forced purchase and sale shocks must retain probability $\beta$ each.
They must force the unit order and remain independent of the class and cost.
The stake must pay terminal proceeds, with no control right or extra information.
The identity probability and the trade cost must match V3.

At a full-purchase recruiting V3 outcome, free abstention requires exactly

$$
\omega\le\Omega_1(r).
$$

This condition makes V3 an equilibrium; it does not establish uniqueness.
Within the full-purchase region, $\omega<\Omega_2(r)$ rules out the holder's extra purchase branches.
It does not remove the original V3 multiplicity at intermediate strengths.
At stake zero, for example, no trade and informative V3 outcomes coexist at 1.55–1.65.

At strength 3, the exact uniqueness conditions follow from Section 3.2.
At strength 1.2, informed trade loses against every schedule, so the free holder also abstains at every stake.
At strength 3.6, full informed orders hold and the maximum posterior falls below $\tau$.
Therefore the free holder abstains at every stake there too.

The I0 statement also needs a qualification near the lower full-purchase threshold.
When $m_{\max}>1$, a pure free purchase can recruit.
I0 permits that strict purchase.
At $r=1.47$ and $\omega=0.1$, both $m=0$ and $m=1$ support informative outcomes.
For the latter, the holder's purchase gain is

$$
\frac{73719}{24304000}>0.
$$

The informed H also earns strictly positive profit.
Thus I0 does not ensure uniqueness throughout $\omega\le\Omega_1(r)$.

The liquidity foundation is conditional on forced shocks.
It does not derive those shocks from a freely chosen trade motive.
The literature status of the forced purchase shock stays open.

### 3.6 Price-sensitive liquidity and the ceiling

**Status: analytical local classification; endpoint values are computer-assisted.**

Let $\widehat B=(1-\lambda)\widehat\beta=22/85$ and $\bar v=51/50$.
For full informed orders, a purchase motive accepts the order when its benefit exceeds

$$
\kappa_+=e\Delta\frac{\lambda}{2(\lambda+2b_+)}+k.
$$

The fixed point is

$$
b_+=\widehat B\left(1-\frac{\kappa_+}{\bar v}\right).
$$

After multiplication by its positive denominator, it becomes

$$
2b_+^2+[\lambda-2\widehat B(1-k/\bar v)]b_+
-\widehat B(1-k/\bar v)\lambda
+\frac{\widehat B e\Delta\lambda}{2\bar v}=0.
$$

The sale mass solves the same equation with $e=\rho$.
Thus the sale side is separable in this full-order region.

On $r\in[3,4]$, any equilibrium has each liquidity mass at least $385/3468$.
This bound follows from $\kappa\le\Delta(4)/2+k$.
Either correctly signed informed order then has net return at least $3643/299100>0$.
Thus full informed orders are necessary throughout this local interval.
The quadratic has negative constant term, so it has exactly one positive root on each entry piece.

Define

$$
b_\tau(r)=\frac{\lambda(1-\tau(r))}{2\tau(r)-1}.
$$

The recruiting root requires $b_+\le b_\tau$ under C1.
The other root requires $b_+>b_\tau$.
Substitution into the quadratic gives one endpoint equation for each piece.
Exact Sturm counts give one root in $(3,4)$ for each equation.
The rational brackets are

$$
\begin{aligned}
r_-&\in(3.11059926916,3.11059926918),\\
r_+&\in(3.78385486063,3.78385486064).
\end{aligned}
$$

Therefore C1 gives two equilibria exactly on $(r_-,r_+]$ within $[3,4]$.
The lower endpoint is open because the floor rule fails at posterior equality under C1.
The upper endpoint is closed because C1 permits full preparation at equality.
The source memo incorrectly closes both endpoints.

At strength 3.6:

| Piece | Purchase mass | Purchase posterior | Entry |
|---|---:|---:|---:|
| Recruiting | 0.197543994 | 0.735914048 | 0.530510937 |
| Floor | 0.241165025 | 0.711273396 | 0.250000000 |

Both share sale mass $0.241165025$.
The informed net returns are $0.227947366$ and $0.047770550$ on the recruiting outcome.
On the floor outcome, both returns equal $0.047770550$.
Thus both outcomes satisfy the informed incentives.

CM adds a third outcome throughout $(r_-,r_+)$:

$$
b_+=b_\tau,\qquad
e_\tau=\frac{\bar v(1-b_\tau/\widehat B)-k}{\Delta(\tau-1/2)}.
$$

Its entry at the purchase flow is strictly between $\rho$ and 1.
At strength 3.6, $e_\tau=10290492/11602019=0.886957003\ldots$.
The informed purchase remains strictly profitable there.
At either endpoint this outcome joins a pure entry piece.

The soft ceiling result holds.
The unqualified statement about uniqueness below $r_-$ needs the local full-order scope.
Also, the calibration nests the original purchase mass at 3, not the complete liquidity law.
Its sale mass at 3 is $0.244892548$, rather than $11/51$.
The existence proof's condition $\Delta/2+k<\bar v$ also needs an explicit domain.
It holds throughout $[3,4]$.

### 3.7 Challenger orders: the fraction is correct, but multiplicity starts earlier

**Status: analytical and computer-assisted.**

The challenger in the slot knows that its own order contains no class information.
At the benchmark strengths, the low-cost type prepares and the high-cost type abstains.
Their rare-arrival trade gains reproduce:

| Strength | Low-cost purchase | High-cost sale |
|---|---:|---:|
| 1.2 | $453/1600$ | $389/4800$ |
| 3 | $-17/100$ | $337/2400$ |
| 3.6 | $6031/9600$ | $4633/28800$ |

For the complete suppression profile at 3, write

$$
v_U=59/96,\qquad v_C=29/24,\qquad v_H=67/96.
$$

At $s=0$, the purchase price is $(bv_U+\chi\rho v_C)/(b+\chi\rho)$.
The informed H abstains exactly when

$$
\chi\ge\frac{b(v_H-k-v_U)}{\rho(v_C-v_H+k)}
=\frac{352}{3417}.
$$

This fraction is correct for complete suppression.
It is not the first presence that supports a second equilibrium.

On the floor purchase piece, let the low-cost challenger buy and the high-cost challenger sell.
An interior informed purchase satisfies

$$
s(\chi)=\frac{2\{b(v_H-v_U-k)-\chi\rho(v_C-v_H+k)\}}{k\lambda}.
$$

The purchase flow stays below the recruitment threshold when $s<451/531$.
This branch starts just above

$$
\chi_A=\frac{308000}{3830457}=0.080408160175\ldots,
$$

and reaches $s=0$ at $352/3417$.
At $\chi=9/100$, take

$$
s=84493/172800,\qquad t=1.
$$

The independent calculation gives

$$
\mu_{\rm out}(1)=190093/295693<\tau,\qquad
\mu_{\rm out}(0)=149843/211379>\tau.
$$

The prices are

$$
(P_-,P_0,P_+)=(62285/112524,6836447/5073096,1627/2400).
$$

The H purchase payoff is exactly zero.
The L sale payoff is $51229/22504800>0$.
The low-cost purchase and high-cost sale payoffs are positive.
All opposite orders lose.
Entry is $537779/1305600=0.411901808\ldots$.

The discovery equilibrium also exists at this same presence.
Thus uniqueness below $352/3417$ is false, even under IM/C1 and pure challenger orders.
The source interface accepts the omitted profile.
Its search misses the profile because it brackets the whole purchase interval across an entry jump.
The payoff can have the same sign at both interval endpoints and still have an interior root.

The informed sale rate at $\chi=2/17$ also reproduces: $t=437/864$.
Mixed challenger orders remain outside this brief classification.
They are not needed for this counterexample.

### 3.8 Incumbent orders: preparation must condition on the value signal

**Status: analytical correction and computer-assisted brackets.**

An incumbent purchase selects high values of $R$.
The outside challenger must condition on that selection.
Its preparation payoff is

$$
\mathbb E[(\theta_j-\max\{p,R\})^+\mid Q],
$$

rather than $g_L(r)+\mu(Q)[g_H(r)-g_L(r)]$.
The source uses the latter expression in `slot3.py` and `n43_incumbent.py`.
It therefore discards information about the rival's value.

On a floor outcome at 3, the incumbent's conditional target value is

$$
f(R)=
\begin{cases}
1/8,&0\le R<1/2,\\
3/8+R/4,&1/2\le R<1,\\
1/2+R/8,&1\le R\le3.
\end{cases}
$$

Let $d$ be its purchase cutoff, and write $a=\lambda/2+b$.
The purchase cutoff satisfies $f(d)-P_+-k=0$, where

$$
P_+=\frac{(\lambda/2)(67/96)+b(59/96)
+\chi(3-d)[1/2+(3+d)/16]/3}
{a+\chi(3-d)/3}.
$$

The correct preparation return at this flow is

$$
B_+=\frac{(\lambda/2)(203/24)+b(103/24)
+\chi(3-d)(17-d)/12}
{a+\chi(3-d)/3}.
$$

The final numerator term integrates $(10-R)/2$ over incumbent buyers.
This is the missing value-selection term.

Without an incumbent purchase, the numerator of $B_+-6$ equals $10/153$.
The correct threshold therefore satisfies

$$
\chi_* =\frac{40}{51(3-d_*)(7+d_*)},\qquad
300d_*^2+1787d_*-3223=0.
$$

The positive root is unique because the polynomial rises strictly for $d>0$.
Exact brackets give

$$
d_*=1.450413981402\ldots,\qquad
\chi_*=0.059895768377\ldots.
$$

C1 requires $\chi>\chi_*$ for this strict floor branch.
Even the source's class-only criterion has continuous threshold $0.074873895166\ldots$.
Its $0.0765$ is only the first accepted point on its grid.

**Strict counterexample.** At $\chi=3/50$, the two rational cutoff brackets give

$$
R_s=0.681822026916\ldots,\qquad R_b=1.450532025905\ldots.
$$

The prices are $0.565455507$, $0.615523228$, and $0.661316503$.
The correct purchase-flow preparation return is $5.999740831<6$.
Both endpoints of the rational cutoff bracket give this strict inequality.
The informed net purchase and sale returns are $0.016600163$ and $0.014205507$.

The incumbent's floor payoff uses the same auction term at every order.
Its value $f(R)$ is nondecreasing, and the two price thresholds do not overlap.
Thus its cutoff orders are optimal for every $R$, including the reserve discontinuity.
At the other flows, the class-prior incumbent contribution to preparation is at most 5.
The informed sale contribution is still smaller.
Neither flow recruits.
This is a floor equilibrium below the reported threshold.

The recruiting outcome also survives at this presence.
The absence of incumbent purchases on that outcome remains valid for $\zeta\ge1$.
For $R\ge1$, its purchase gain is

$$
G_+(R;\zeta)=\frac{1+R}{2}-\frac{163}{120}-k
-\zeta(1-\rho)\frac R2.
$$

At $\zeta=1$, the maximum on $[1,3]$ is $-151/300<0$.
For $R<1$, the trade alone loses, and the auction effect cannot help.
The gain falls pointwise as $\zeta$ rises.
The source's claim that its slope turns negative for every $\zeta>1$ is incorrect.
The slope turns negative only above $4/3$; the conclusion still holds.

The low-value sale cutoffs also reproduce.
The corrected entry calculation does not establish uniqueness against every possible preparation mixture.
It does refute the reported minimum presence and the uniqueness conclusion below $0.0765$.

## 4. Errors and corrections

| Priority | Location | Error | Correction |
|---|---|---|---|
| Major | N4 §2.1, intermediate strengths; `n41_holder.py`, `candidates` | The search fixes $s=1$ for every informative holder outcome. | Add the partial informed threshold branch. The claimed unique informative outcome is false. |
| Major | N4 §2.3; `slot3.py`, `engine`; `n43_incumbent.py`, `solve_cutoffs` | Preparation uses an unconditional incumbent value distribution after a value-dependent order. | Integrate the joint class and value distribution conditional on the order. The floor cutoff becomes $\chi_*=0.059895768\ldots$. |
| Major | N4 §2.2; `n42_challenger.py`, `root_in_unit` | A single bracket spans an entry jump and misses an interior informed root. | Solve each continuous piece separately. Multiplicity already occurs at $\chi=0.09<352/3417$. |
| Material | N4 §2.4(a) | Free abstention is treated as global uniqueness. | Separate implementation, exclusion of holder purchases, and uniqueness of the underlying V3 outcome. I0 also permits strict pure purchases near $r_F$. |
| Material | N4 §2.4(b) | Both coexistence endpoints are closed under C1. | Use $(r_-,r_+]$. CM adds a third interior outcome. |
| Material | N4 §2.1 welfare; `n41_holder.py`, `ledger` | The free holder mass receives the identity probability twice. | Use $cm\ell_+$, not $(1-\lambda)cm\ell_+$. Revise holder profits. |
| Minor | N4 §2.1 corollary | C1 uniqueness includes $\Omega_2$. | Two outcomes exist there. At $\Omega_1$, only V3 survives under C1/IM. |
| Minor | N4 §2.1, recovered stake window | Rounded bounds obscure ties. | Use $859/6445$ and $94645232/516885327$. Explain the extra outcomes at both endpoints. |
| Minor | N4 §2.4(b) calibration | The purchase calibration is described as a full nesting of calibration A. | Only its purchase mass matches. The sale mass differs. |

The source replays reproduce the published numbers.
They also confirm the source searches' omissions.
No source file requires an arithmetic change to accept the two omitted informed profiles.
The incumbent case requires a change to the information used for preparation.

## 5. Plain summary

The holder results at strength 3 largely hold.
It never sells, and it buys only to recruit.
Both stake thresholds are exact.
The endpoint counts and the holder profit ledger need corrections.
Proceeds rise near manipulation's onset, but fall below V3 at larger stakes.
Most discovery surplus disappears.

The recovered entry rise exists, but its uniqueness claim fails.
CM also supports a partial informed purchase at each strength.
That second informative outcome survives throughout the proposed stake window.

A holder with forced shocks can implement V3 when its free choice stays zero.
That implementation does not establish uniqueness.

Price-sensitive participation creates the claimed soft ceiling.
C1 gives two outcomes on an interval with an open lower endpoint.
CM adds a third outcome inside that interval.

The challenger threshold $352/3417$ marks complete purchase suppression.
A partial purchase creates multiplicity earlier, above about 0.0804.

The incumbent threshold omits the value information in its order.
The corrected floor branch starts above about 0.05990.
A floor equilibrium at presence 0.06 refutes the reported minimum of 0.0765.
