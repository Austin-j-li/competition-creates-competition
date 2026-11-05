# Point 1, Reading N: numerical exploration

Date: 21 October 2026.

## 1. Question and reading

**Numerical diagnostic.** The main reversal survives small value classes, several wide overlapping classes, and each requested prior in at least one family. It does not follow from the class ranking alone. Values below the reserve add a term that can reverse the spread's comparative static.

This memo uses **Reading N**. Nature selects the distribution. The investor observes the class. The challenger observes neither the class nor its value before preparation. Preparation reveals its value.

The source is `overleaf/paper/main.tex`, Sections 2–4, Section 6.3, and Appendix A.1–A.2. All computations below use an independent script. No existing numerical module supplies a formula or an output.

## 2. Formal setup

Let $\Pr(j=H)=\pi\in(0,1)$ and $\theta\mid j\sim U[a_j,b_j]$. The incumbent value is $R\sim U[0,r]$. Values, preparation costs, and noise are independent, conditional on the class where relevant.

The reserve is $p>0$. The auction uses truthful cash bids and the second-price rule. An indifferent challenger prepares. Costs equal $c_L$ with probability $\rho$ and $c_H$ otherwise. The investor chooses $q\in[-1,1]$, with cost $k|q|$. Noise is Laplace with scale $b>1$.

The primary scans impose $a_H\ge a_L$ and $b_H\ge b_L$. These inequalities give first-order stochastic dominance for uniform distributions. Supports may overlap or cross the reserve. The controls that violate this ranking carry an explicit label.

Write $t_j$ for class-conditional target proceeds after preparation. Write $g_j$ for class-conditional gross challenger profit. Define

$$
\Delta_T=t_H-t_L,\qquad D(u)=G_L(u)-G_H(u),\qquad
B_r(\mu)=g_L+\mu(g_H-g_L).
$$

Entry means **preparation**, not an admissible bid or a successful acquisition. Define $w_j(r)=\Pr(\theta\ge p,\theta>R\mid j)$. The ownership measure is

$$
\mathsf O_H=\Pr(j=H,\text{challenger wins})=\pi e_Hw_H(r).
$$

Thus “high-value ownership” means ownership by a challenger from class $H$. With overlap, it does not identify a fixed realized-value threshold. It also does not mean that every class-$H$ entrant wins.

## 3. Results

### 1. Auction formulas, including the reserve boundary — analytical

First fix the challenger value $\theta$. For $r>p$, direct integration over the incumbent bid gives

$$
t_0=p\left(1-\frac p r\right),
$$

$$
t(\theta)=
\begin{cases}
t_0,&\theta<p,\\
\theta-\dfrac{\theta^2-p^2}{2r},&p\le\theta\le r,\\
\dfrac r2+\dfrac{p^2}{2r},&\theta>r,
\end{cases}
\qquad
g(\theta)=
\begin{cases}
0,&\theta<p,\\
\dfrac{\theta^2-p^2}{2r},&p\le\theta\le r,\\
\theta-\dfrac r2-\dfrac{p^2}{2r},&\theta>r.
\end{cases}
$$

For $p\le\theta\le r$, the target receives $p$ when $R<p$, $R$ when $p\le R\le\theta$, and $\theta$ when $R>\theta$. Hence

$$
t(\theta)=\frac{p^2+\int_p^\theta u\,du+\theta(r-\theta)}r,
\qquad
g(\theta)=\frac{p(\theta-p)+\int_p^\theta(\theta-u)\,du}{r}.
$$

These expressions give the middle branches. Below the reserve, the challenger cannot change the auction. Above $r$, it always wins and pays $\max\{p,R\}$.

For a uniform class, let $w=b_j-a_j$ and define

$$
I_n(u,v)=
\begin{cases}
(v^{n+1}-u^{n+1})/(n+1),&v>u,\\
0,&v\le u.
\end{cases}
$$

Set $u=\max(a_j,p)$, $v=\min(b_j,r)$, $x=\max(a_j,r)$, and $L_0=(\min(b_j,p)-a_j)_+$. Class averages are

$$
\begin{aligned}
t_j={1\over w}\bigg[
L_0t_0+I_1(u,v)-\frac{I_2(u,v)-p^2I_0(u,v)}{2r}
+\left(\frac r2+\frac{p^2}{2r}\right)I_0(x,b_j)
\bigg],\\
g_j={1\over w}\bigg[
\frac{I_2(u,v)-p^2I_0(u,v)}{2r}
+I_1(x,b_j)-\left(\frac r2+\frac{p^2}{2r}\right)I_0(x,b_j)
\bigg],\\
w_j={I_1(u,v)/r+I_0(x,b_j)\over w}.
\end{aligned}
$$

These formulas permit overlap and $a_j<p$. If $r\le p$, the simpler formulas are $t_0=0$, $t_j=p\Pr(\theta\ge p\mid j)$, $g_j=E[(\theta-p)_+\mid j]$, and $w_j=\Pr(\theta\ge p\mid j)$. The script includes this branch.

### 2. The spread needs a reserve correction — analytical

For a continuous incumbent cdf $F$, a value at the reserve makes sale possible when $R<p$. Target proceeds therefore jump at $\theta=p$:

$$
t(\theta)=t_0+pF(p)\mathbf1\{\theta\ge p\}
+\mathbf1\{\theta\ge p\}\int_p^\theta[1-F(u)]\,du.
$$

Integrate over each class and subtract. The result is

$$
\boxed{\Delta_T(F)=pF(p)D(p)+\int_p^\infty[1-F(u)]D(u)\,du.}
$$

The integral proposed in the brief omits $pF(p)D(p)$ when the classes differ in reserve admission. Under class FOSD, both terms are nonnegative. However, a stronger incumbent lowers $F(p)$ and therefore lowers the first term.

For the uniform incumbent,

$$
\boxed{\Delta_T'(r)=\frac{\int_p^r uD(u)\,du-p^2D(p)}{r^2}.}
$$

The derivative follows by differentiation of $p^2D(p)/r+\int_p^r(1-u/r)D(u)du$. The upper-limit term is zero. Thus class FOSD does **not** suffice for $\Delta_T'(r)\ge0$.

Gross profit has no admission jump. Tonelli's theorem gives

$$
g_j(F)=\int_p^\infty F(u)[1-G_j(u)]\,du,
\qquad
g_H-g_L=\int_p^\infty F(u)D(u)\,du.
$$

This also equals $\int g(\theta)\,d(G_H-G_L)(\theta)$, with $g(\theta)=0$ below $p$. A stronger incumbent lowers each $g_j$, and therefore lowers $B_r(\mu)$ at every fixed belief. Under class FOSD,

$$
\frac{d(g_H-g_L)}{dr}=-\frac{\int_p^r uD(u)\,du}{r^2}\le0.
$$

**Analytical, weaker conditions.** At a given $r$, the price and order arguments require only $t_H>t_L$ and $g_H\ge g_L$. They do not require pointwise cdf dominance. The two displayed weighted integrals identify the exact payoff restrictions. For an increasing spread along the uniform family, the exact restriction is $\int_p^r uD(u)du\ge p^2D(p)$.

A useful sufficient restriction is class FOSD with $G_H(p)=G_L(p)$. It removes the correction and restores the spread comparison under any FOSD increase in incumbent strength. Both supports above the reserve satisfy this restriction.

### 3. General priors and prices — analytical

The likelihood-ratio bounds do not depend on the prior. Bayes' rule gives

$$
m_\pi=\frac{\pi e^{-2/b}}{1-\pi+\pi e^{-2/b}},\qquad
M_\pi=\frac{\pi e^{2/b}}{1-\pi+\pi e^{2/b}}.
$$

They apply to arbitrary mixed orders. They also apply to the price posterior, which is a conditional average of the flow posterior. Under full orders,

$$
\mu(x)=\operatorname{logit}^{-1}\left(
\operatorname{logit}\pi+\frac{|x+1|-|x-1|}{b}\right).
$$

The posterior equals $m_\pi$ on $x\le-1$ and $M_\pi$ on $x\ge1$. Under no trade, it equals $\pi$ everywhere.

When $c_L<B_r(m_\pi)$ and $g_H\ge g_L$, define

$$
e(\mu)=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\qquad
P(\mu)=t_0+e(\mu)[t_L-t_0+\mu\Delta_T].
$$

The condition $\Delta_T>0$ and the floor $e\ge\rho$ make the price strictly increasing. Entry cannot lower target proceeds, so $t_L-t_0\ge0$. Across an entry jump, the same decomposition as equation (A.3) gives a positive price difference.

For any candidate equilibrium, competitive prices also give

$$
\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}.
$$

The denominator is positive under the floor. Thus the price identifies the posterior that preparation requires.

The script also reports candidate controls outside the floor. It then uses

$$
e(\mu)=\rho\mathbf1\{B_r(\mu)\ge c_L\}
+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\}.
$$

All no-entry flows share price $t_0$. Their pooled posterior remains below the low-cost threshold because $B_r$ is affine. Positive-entry prices remain strictly increasing when $\Delta_T>0$. This construction gives consistent entry controls, but does not establish investor optimality.

### 4. Residuals, order bounds, and the pair conditions — analytical

Conditional on $j$, the distribution of the eventual value does not depend on flow. Subtraction of the competitive price therefore gives

$$
A_H=e\Delta_T(1-\mu_X),\qquad A_L=e\Delta_T\mu_X.
$$

Let $d_\pi=\min\{m_\pi,1-M_\pi\}$. The minimum residual **before the entry floor** is $d_\pi\Delta_T$. Under the floor, both residuals exceed or equal $\rho d_\pi\Delta_T$.

For a correctly signed order of size $s$, let $F_j(s)$ be its expected residual. The Laplace density obeys $|f'|\le f/b$. Differentiate the translated density, with the price and entry schedules fixed:

$$
|F_j'(s)|\le F_j(s)/b,\qquad
U_j'(s)\ge(1-s/b)F_j(s)-k
\ge\boxed{(1-1/b)\rho d_\pi\Delta_T-k}.
$$

A positive bound makes full orders uniquely optimal against every candidate schedule. Wrong-signed orders have negative gross profit. Thus this bound excludes mixed and partial alternatives as well.

The direct analogues of (A1)–(A3) are

$$
\begin{array}{ll}
\text{(N1)}&0\le c_L<B_{r_1}(m_\pi),\\
\text{(N2)}&B_{r_0}(\pi)<c_H<B_{r_1}(M_\pi),\\
\text{(N3)}&\Delta_T(r_0)<k<(1-1/b)\rho d_\pi\Delta_T(r_1).
\end{array}
$$

Use $r_0<r_1$, positive spreads, and the maintained class ranking. Gross profits decrease in $r$, so (N1) also gives the floor at $r_0$. At $r_0$, every nonzero order earns at most $|q|(\Delta_T(r_0)-k)<0$. At $r_1$, the global derivative bound forces full orders. Condition (N2) then adds high-cost entry on a positive-probability tail.

Unlike the binary case, ownership requires the further comparison

$$
\text{(N4)}\qquad
e_H(r_1)w_H(r_1)>\rho w_H(r_0).
$$

The examples below satisfy (N4). It does not follow from higher entry alone.

**Analytical, a sharper no-trade bound.** Let $\bar e=e(M_\pi)$ and $d^+_\pi=\max\{M_\pi,1-m_\pi\}$. Every candidate has $e\le\bar e$ and $A_j\le\bar e d^+_\pi\Delta_T$. Therefore

$$
k>\bar e d^+_\pi\Delta_T
$$

also proves unique no trade. This bound can apply without the low-cost floor. The pair search retains the more conservative (N3), for direct comparison with the paper.

### 5. Candidate outcomes and exact no-trade existence — analytical

Under no trade, set $e_\pi=e(\pi)$. Prices are constant:

$$
P_N=t_0+e_\pi[t_L-t_0+\pi\Delta_T].
$$

A unilateral trade faces this fixed schedule. Its favorable per-unit residual is $e_\pi\Delta_T(1-\pi)$ in class $H$, or $e_\pi\Delta_T\pi$ in class $L$. Hence

$$
\boxed{\text{No trade is an equilibrium}\iff
k\ge e_\pi\Delta_T\max\{\pi,1-\pi\}.}
$$

Equality permits investor indifference. It does not imply uniqueness.

Under full orders and an interior high-cost threshold, define

$$
\tau=\frac{c_H-g_L}{g_H-g_L},\qquad
x^*=\frac b2[\operatorname{logit}\tau-\operatorname{logit}\pi].
$$

For $m_\pi<\tau\le M_\pi$, $x^*\in(-1,1]$ and

$$
\alpha_H=1-\tfrac12 e^{(x^*-1)/b},\qquad
\alpha_L=\tfrac12 e^{-(x^*+1)/b}.
$$

Set both probabilities to one if $c_H\le B(m_\pi)$, and to zero if $c_H>B(M_\pi)$. At $c_H=B(M_\pi)$, retain the upper tail. The preparation tie rule applies to its positive mass. The low-cost atom uses the same calculation if the floor fails.

Under the floor,

$$
\begin{aligned}
e_j&=\rho+(1-\rho)\alpha_j,\\
\mathsf E_F&=\pi e_H+(1-\pi)e_L,\\
\mathsf O_{H,F}&=\pi e_Hw_H,\\
E[V_T]&=t_0+\pi e_H(t_H-t_0)+(1-\pi)e_L(t_L-t_0).
\end{aligned}
$$

High-cost entry under full orders has positive probability exactly when $c_H\le B(M_\pi)$. If $c_H>B(M_\pi)$, it is impossible under every strategy.

For completeness, the probability of two admissible bidders is

$$
\left(1-\frac pr\right)
\{\pi e_H[1-G_H(p)]+(1-\pi)e_L[1-G_L(p)]\},\qquad r>p.
$$

This differs from preparation when values can fall below $p$.

**Analytical, general-prior asymmetry.** Let $f_H=f(x-1)$, $f_L=f(x+1)$, and $a=\pi f_H+(1-\pi)f_L$. At full orders,

$$
J_H=\Delta_T(1-\pi)\int e\frac{f_Hf_L}{a}\,dx,\qquad
J_L=\Delta_T\pi\int e\frac{f_Hf_L}{a}\,dx.
$$

Thus $J_H/J_L=(1-\pi)/\pi$, when the integral is positive. The equality in equation (A.7) is specific to the equal prior.

### 6. Independent integration and the primary scans — numerical diagnostic

The script integrates realized auction payments over $(R,\theta)$. It splits the integrals at the reserve and bid ties. It uses no class-average formula inside that calculation.

The run covers 166 economies and 332 class distributions. These include the six primary families at eleven strengths and 100 seeded parameter draws. The draws include values below zero, reserve crossings, and $r\le p$. Absolute and relative quadrature tolerances are $2\times10^{-12}$.

| Object | Maximum absolute discrepancy |
|---|---:|
| $t_0$ | $4.44\times10^{-16}$ |
| $t_L,t_H$ | $1.78\times10^{-15}$ |
| $g_L,g_H$ | $3.55\times10^{-15}$ |
| $w_L,w_H$ | $3.33\times10^{-16}$ |
| $\Delta_T$ | $1.78\times10^{-15}$ |
| $B_r(\mu)$, five beliefs | $3.55\times10^{-15}$ |

These are numerical discrepancies, not interval error certificates.

Each main family uses $p=0.5$, $\rho=0.25$, $c_L=1$, $b=2$, and each requested prior. The fixed-cost scan uses $c_H=6$ and $k=0.02$. Each scan contains 9,001 strengths from $1.000001$ to $10$, with spacing about $0.001$. The total is 270,030 family-prior-strength nodes.

The nominal $\ell=1$ and $h=10$ set the scan range for the wide families. Their class means need not equal these labels.

| Code | $G_L$ | $G_H$ | $\Delta_T(1^+)$ | $\Delta_T(3)$ | $\Delta_T(10)$ |
|---|---|---|---:|---:|---:|
| N05 | $U[0.95,1.05]$ | $U[9.95,10.05]$ | .00020833 | .66680556 | 4.05002083 |
| N50 | $U[0.5,1.5]$ | $U[9.5,10.5]$ | .02083333 | .68055556 | 4.05208333 |
| N100 | $U[0,2]$ | $U[9,11]$ | .10416667 | .68750000 | 4.00416667 |
| W20 | $U[0.2,4]$ | $U[1,19]$ | .03508772 | .29256010 | 2.49627193 |
| W40 | $U[0.4,4]$ | $U[1,19]$ | .01620370 | .24768519 | 2.42037037 |
| W50 | $U[0.5,4]$ | $U[1,19]$ | .00595238 | .22332451 | 2.37916667 |

Every primary spread increases at every grid step. The smallest increase is $1.253\times10^{-5}$. Every profit gap is positive; the smallest is $4.939583$. At every prior, all three curves $B_r(m_\pi)$, $B_r(\pi)$, and $B_r(M_\pi)$ decrease at every grid step. The largest step among those curves is $-4.479\times10^{-5}$.

The following table reports all prior bounds. Its last column multiplies $\Delta_T$ in the full-order uniqueness bound.

| $\pi$ | $m_\pi$ | $M_\pi$ | $d_\pi$ | $(1-1/b)\rho d_\pi$ |
|---:|---:|---:|---:|---:|
| .20 | .084224 | .404610 | .084224 | .010528 |
| .35 | .165337 | .594105 | .165337 | .020667 |
| .50 | .268941 | .731059 | .268941 | .033618 |
| .65 | .405895 | .834663 | .165337 | .020667 |
| .80 | .595390 | .915776 | .084224 | .010528 |

**Numerical diagnostic: profits and candidate outcomes at $r=3$.** Each outcome pair is preparation / class-$H$ ownership. “Full” and “No” denote fixed candidate profiles. They are equilibrium outcomes only where the relevant conditions hold. In particular, the low-cost floor fails for the first three families at $\pi=.20$ and $r=3$.

| Family | $\pi$ | $B(m_\pi)$ / $B(\pi)$ / $B(M_\pi)$ | Full: $\mathsf E$ / $\mathsf O_H$ | No: $\mathsf E$ / $\mathsf O_H$ |
|---|---:|---|---|---|
| N05 | .20 | .8270 / 1.7918 / 3.4968 | .1282 / .0396 | .2500 / .0500 |
| N05 | .35 | 1.5029 / 3.0418 / 5.0759 | .2500 / .0875 | .2500 / .0875 |
| N05 | .50 | 2.3663 / 4.2917 / 6.2172 | .5228 / .3242 | .2500 / .1250 |
| N05 | .65 | 3.5075 / 5.5417 / 7.0805 | .6400 / .4823 | .2500 / .1625 |
| N05 | .80 | 5.0866 / 6.7917 / 7.7565 | .7682 / .6594 | 1.0000 / .8000 |
| N50 | .20 | .8396 / 1.8028 / 3.5050 | .1289 / .0397 | .2500 / .0500 |
| N50 | .35 | 1.5144 / 3.0507 / 5.0815 | .2500 / .0875 | .2500 / .0875 |
| N50 | .50 | 2.3763 / 4.2986 / 6.2209 | .5231 / .3244 | .2500 / .1250 |
| N50 | .65 | 3.5157 / 5.5465 / 7.0828 | .6402 / .4825 | .2500 / .1625 |
| N50 | .80 | 5.0922 / 6.7944 / 7.7576 | .7684 / .6595 | 1.0000 / .8000 |
| N100 | .20 | .8841 / 1.8417 / 3.5340 | .1319 / .0400 | .2500 / .0500 |
| N100 | .35 | 1.5550 / 3.0823 / 5.1012 | .2500 / .0875 | .2500 / .0875 |
| N100 | .50 | 2.4119 / 4.3229 / 6.2340 | .5241 / .3251 | .2500 / .1250 |
| N100 | .65 | 3.5446 / 5.5635 / 7.0909 | .6412 / .4832 | .2500 / .1625 |
| N100 | .80 | 5.1119 / 6.8042 / 7.7617 | .7693 / .6601 | 1.0000 / .8000 |
| W20 | .20 | 1.5211 / 2.4013 / 3.9568 | .2500 / .0481 | .2500 / .0481 |
| W20 | .35 | 2.1378 / 3.5416 / 5.3973 | .2500 / .0843 | .2500 / .0843 |
| W20 | .50 | 2.9254 / 4.6819 / 6.4385 | .5409 / .3242 | .2500 / .1204 |
| W20 | .65 | 3.9665 / 5.8223 / 7.2261 | .6573 / .4759 | .2500 / .1565 |
| W20 | .80 | 5.4071 / 6.9626 / 7.8427 | .7827 / .6446 | 1.0000 / .7704 |
| W40 | .20 | 1.5659 / 2.4404 / 3.9859 | .2500 / .0481 | .2500 / .0481 |
| W40 | .35 | 2.1786 / 3.5734 / 5.4172 | .2500 / .0843 | .2500 / .0843 |
| W40 | .50 | 2.9612 / 4.7064 / 6.4516 | .5421 / .3250 | .2500 / .1204 |
| W40 | .65 | 3.9956 / 5.8394 / 7.2342 | .6584 / .4766 | .2500 / .1565 |
| W40 | .80 | 5.4269 / 6.9724 / 7.8469 | .7837 / .6452 | 1.0000 / .7704 |
| W50 | .20 | 1.5903 / 2.4617 / 4.0017 | .2500 / .0481 | .2500 / .0481 |
| W50 | .35 | 2.2008 / 3.5907 / 5.4280 | .2500 / .0843 | .2500 / .0843 |
| W50 | .50 | 2.9806 / 4.7197 / 6.4588 | .5427 / .3254 | .2500 / .1204 |
| W50 | .65 | 4.0114 / 5.8487 / 7.2386 | .6590 / .4770 | .2500 / .1565 |
| W50 | .80 | 5.4377 / 6.9777 / 7.8491 | .7842 / .6455 | 1.0000 / .7704 |

**Numerical diagnostic: regions at fixed benchmark costs.** All intervals below show accepted grid points, rounded to three decimals. The left endpoint “1” means $1.000001$. A dash means an empty set on this grid.

- $U_N$: the sharper sufficient bound for unique no trade in Result 4.
- $N$: the exact no-trade equilibrium condition, evaluated on the grid.
- $U_F$: the positive global bound and the low-cost floor.
- $H_F$: positive high-cost entry under the full-order candidate.

The intersection $U_F\cap H_F$ gives unique full orders with high-cost entry. Outside $U_N$ and $U_F$, uniqueness remains unresolved by these bounds.

| Family | $\pi$ | $U_N$ | $N$ | $U_F$ | $H_F$ |
|---|---:|---|---|---|---|
| N05 | .20 | 1–1.513 | 1–1.557 | — | — |
| N05 | .35 | 1–1.543 | 1–1.633 | 3.663–8.328 | — |
| N05 | .50 | 1–1.261 | 1–1.747 | 2.838–10 | 1–3.592 |
| N05 | .65 | 1–1.242 | 1–1.279; 1.633 | 3.663–10 | 1–5.604 |
| N05 | .80 | 1–1.229 | 1–1.248 | 5.622–10 | 1–6.870 |
| N50 | .20 | 1–1.402 | 1–1.455 | — | — |
| N50 | .35 | 1–1.438 | 1–1.544 | 3.638–8.375 | — |
| N50 | .50 | 1–1.057 | 1–1.672 | 2.804–10 | 1–3.601 |
| N50 | .65 | 1–1.028 | 1–1.085 | 3.638–10 | 1–5.607 |
| N50 | .80 | 1–1.009 | 1–1.037 | 5.607–10 | 1–6.871 |
| N100 | .20 | — | — | — | — |
| N100 | .35 | — | 1–1.172 | 3.650–8.539 | — |
| N100 | .50 | — | 1–1.398 | 2.775–10 | 1–3.630 |
| N100 | .65 | — | — | 3.650–10 | 1–5.618 |
| N100 | .80 | — | — | 5.660–10 | 1–6.875 |
| W20 | .20 | 1–1.696 | 1–1.809 | — | — |
| W20 | .35 | 1.470–1.773 | 1–1.995 | 5.405–10 | 1–1.469 |
| W20 | .50 | — | 1–2.257 | 4.218–10 | 1–4.140 |
| W20 | .65 | — | — | 5.405–10 | 1–6.169 |
| W20 | .80 | — | — | 8.164–10 | 1–7.637 |
| W40 | .20 | 1–1.954 | 1–2.062 | — | — |
| W40 | .35 | 1–1.186; 1.545–2.027 | 1–2.241 | 5.601–10 | 1–1.544 |
| W40 | .50 | 1–1.250 | 1–2.495 | 4.416–10 | 1–4.167 |
| W40 | .65 | 1–1.186 | 1–1.309 | 5.601–10 | 1–6.180 |
| W40 | .80 | 1–1.142 | 1–1.207 | 8.384–10 | 1–7.641 |
| W50 | .20 | 1–2.102 | 1–2.207 | — | — |
| W50 | .35 | 1–1.393; 1.584–2.173 | 1–2.382 | 5.709–10 | 1–1.583 |
| W50 | .50 | 1–1.446 | 1–2.631 | 4.525–10 | 1–4.181 |
| W50 | .65 | 1–1.393 | 1–1.497 | 5.709–10 | 1–6.187 |
| W50 | .80 | 1–1.358 | 1–1.410 | 8.505–10 | 1–7.644 |

The script also prints the conservative $\Delta_T<k$ region. Its upper limits are 1.218914 for N05, 1.101393 for W40, and 1.326062 for W50. It is empty for N50, N100, and W20 at $k=.02$. These limits do not depend on the prior.

The low-cost floor can bind before full orders meet the global bound. At $\pi=.20$, its upper endpoints are 1.506593, 1.636794, 2.062717, 6.138789, 6.359370, and 6.477205, respectively. At $\pi=.35$, the N-family endpoints are 8.328612, 8.375933, and 8.539321. All remaining floor regions reach $r=10$.

### 7. Pair search and concrete vectors — numerical diagnostic

The pair search keeps $p=.5$, $\rho=.25$, $c_L=1$, and $b=2$. It varies only $c_H$, $k$, and the two strengths. It searches (N1)–(N3), then computes ownership using (N4).

For each $r_1$, the cost window gives a lower bound on the $r_0$ index. The spread window gives an upper bound. The script compares these bounds across the entire grid. Thus it need not form a matrix of all ordered pairs.

“Yes” means at least one strict pair on the grid. “A” means that (N1) and (N3) have no joint solution on the grid. “B” means that the cost window (N2) fails for every remaining grid pair.

| Family | $\pi=.20$ | $.35$ | $.50$ | $.65$ | $.80$ |
|---|---|---|---|---|---|
| N05 | Yes | Yes | Yes | Yes | Yes |
| N50 | A | Yes | Yes | Yes | B |
| N100 | A | A | B | A | A |
| W20 | A | B | Yes | B | A |
| W40 | A | Yes | Yes | B | B |
| W50 | Yes | Yes | Yes | Yes | B |

There are 15 successful family-prior combinations. Each displayed successful pair also raises class-$H$ ownership. A failed sufficient-window search does not establish that the economic reversal is impossible.

The following simple vectors all use $\pi=.5$. The $c_H$ and $k$ columns lie strictly inside the two windows in the next table.

| Family | $r_0$ | $r_1$ | $c_H$ | $k$ | $\mathsf E_0\to\mathsf E_1$ | $\mathsf O_{H,0}\to\mathsf O_{H,1}$ |
|---|---:|---:|---:|---:|---|---|
| N05 | 1.20 | 3.00 | 6.00 | .0200 | .250000 → .522760 | .125000 → .324195 |
| N50 | 1.05 | 4.00 | 5.50 | .0320 | .250000 → .533794 | .125000 → .331870 |
| W20 | 1.01 | 5.70 | 5.45 | .0356 | .250000 → .507534 | .125000 → .279547 |
| W40 | 1.05 | 4.80 | 5.60 | .0210 | .250000 → .521786 | .124992 → .296473 |
| W50 | 1.10 | 4.00 | 5.80 | .0125 | .250000 → .528995 | .124968 → .308022 |

| Family | $B_{r_1}(m_\pi)-c_L$ | Open $c_H$ window | Open $k$ window |
|---|---:|---|---|
| N05 | 1.366280 | (4.804340, 6.217192) | (.017013889, .022416454) |
| N50 | 1.219279 | (4.869157, 5.853638) | (.026408730, .038170072) |
| W20 | 1.306938 | (5.435122, 5.461084) | (.035467292, .035843028) |
| W40 | 1.497298 | (5.462316, 5.773269) | (.017949735, .023902532) |
| W50 | 1.692999 | (5.466043, 6.067417) | (.009342232, .015057918) |

W20 works, but its trading-cost window has width only .000375737. Its class-$H$ win probability falls from .999997 to .892349. The entry increase still dominates this loss.

Concrete N05 vectors also cover all other requested priors. Here $c_H$ and $k$ are midpoint choices from the script; displayed inputs are rounded.

| $\pi$ | $r_0$ | $r_1$ | $c_H$ | $k$ | $\mathsf E_1$ | $\mathsf O_{H,1}$ |
|---:|---:|---:|---:|---:|---:|---:|
| .20 | 1.015001 | 1.503001 | 3.013402683 | .000670002 | .474762 | .139021 |
| .35 | 1.051001 | 2.013001 | 4.444257385 | .003452968 | .518193 | .244323 |
| .65 | 1.039001 | 1.753001 | 6.900761262 | .002239103 | .607781 | .458745 |
| .80 | 1.024001 | 1.719001 | 7.944257366 | .001122592 | .646119 | .561424 |

For these four rows, $\mathsf E_0=.25$ and $\mathsf O_{H,0}=.25\pi$. The floor margin for the $.20$ row is only .000680020. The unrounded inputs appear in the `pairs` command output.

**Numerical diagnostic: why N100 fails the displayed windows.** Its minimum spread is .104166667. At priors .20, .35, .65, and .80, the largest permitted upper bound under the floor is .003498, .068095, .082755, and .042156. Each lies below that minimum. At prior .50, the maximum cost-window gap among (N1)/(N3)-feasible grid pairs is $-.583814487$. Thus no $c_H$ fits those remaining grid pairs.

The other B failures have maximum cost-window gaps of $-1.077176$ for N50/.80, $-.223264$ for W20/.35, and $-1.095366$ for W20/.65. They are $-.229379$ for W40/.65, $-1.695917$ for W40/.80, and $-.587533$ for W50/.80. The `pairs` command prints the corresponding strengths and all A-failure bounds.

**Numerical diagnostic: direct use of the order objective.** For each simple vector, the script evaluates 401 correctly signed magnitudes against the fixed full-order schedule. It uses exact Laplace tails and 48-point quadrature on each smooth segment. Each state's largest objective occurs at magnitude one.

| Family | Minimum numerical marginal, $H$ | Minimum numerical marginal, $L$ | Analytical lower bound, evaluated numerically |
|---|---:|---:|---:|
| N05 | .106984 | .072797 | .002416454 |
| N50 | .188054 | .128664 | .006170072 |
| W20 | .163164 | .109488 | .000243028 |
| W40 | .114205 | .077805 | .002902532 |
| W50 | .073630 | .050422 | .002557918 |

The objective grid is a diagnostic. The global bound supplies the argument over all feasible order sizes.

### 8. Sign failures and lost binary simplifications — numerical diagnostic

The following list includes every sign failure found in the reported scans and controls. The last two controls deliberately violate the main class ranking.

| Case | Parameters | Departure |
|---|---|---|
| Reserve .9 | $G_L=U[.2,4]$, $G_H=U[1,19]$, $p=.9$ | FOSD holds, but $\Delta_T$ falls on $(1,1.420027554)$; it then rises. |
| Reserve straddle | $G_L=U[.2,.4]$, $G_H=U[.3,.6]$, $p=.5$ | FOSD holds, but $\Delta_T$ falls throughout $1<r\le10$. |
| Crossing cdfs | $G_L=U[1,3]$, $G_H=U[0,3.8]$, $p=.5$ | $g_H-g_L$ changes from negative to positive at $r=1.510612559$. The spread stays negative over the scan. |
| Reversed labels | $G_L=U[9,11]$, $G_H=U[0,2]$, $p=.5$ | Both gaps are negative throughout the scan; the target spread falls throughout. |

In the reserve-.9 case, the spread equals .150175 at $r=1$, .132175 at $r=1.2$, and .127123 at $r=1.5$. It reaches its minimum near 1.420028. In the reserve-straddle case, it falls from .091111 at $r=1$ to .024111 at $r=10$.

In the crossing-cdf control, the profit gap is $-.045175$ near $r=1$ and $.076170$ at $r=3$. The target spread falls until $r=2.985967883$ and then rises. It remains negative even after the profit gap becomes positive. Therefore a favorable profit ranking alone does not justify the proposed order signs.

The omitted reserve term is quantitatively material. At $r=1.2$, it equals .052083333 for N100, .016447368 for W20, and .005787037 for W40. The full spreads there are .126944444, .045040611, and .024629630, respectively.

Several further binary simplifications fail without a sign reversal:

- **Numerical diagnostic:** the spread need not approach zero as $r\downarrow\ell$. Every class family in Result 6 has a positive limit.
- **Numerical diagnostic:** under N05 at $r=3$, $J_H/J_L$ equals 4, 1.857143, 1, .538462, and .25 across the five priors. Thus equation (A.7)'s equality fails away from $.5$.
- **Numerical diagnostic:** W20 has unique full orders at both $r=5$ and $r=10$, with entry $.25$. Class-$H$ ownership falls from .113889 to .096875.
- **Numerical diagnostic:** N05 with $\pi=.65$ and fixed benchmark costs has disconnected no-trade existence intervals: $(1,1.279067184]$ and $(1.632949964,1.633438013]$. The second interval starts when high-cost entry at the prior stops. This lies outside the paper's maintained condition $B_r(1/2)<c_H$ with equal priors.
- **Numerical diagnostic:** information can reduce entry when the floor fails or when costly entry already occurs at the prior. The candidate-outcome table reports both cases. It does not identify those candidate controls as equilibria.

**Open.** The list is exhaustive for these reported runs, not for all uniform supports or all parameter values.

## 4. What changes relative to the current paper

**Analytical, from Results 1–5.** The following changes concern the two-class version only.

| Paper object | What survives or changes |
|---|---|
| Equation (4) | Replace point values with the class averages in Result 1. |
| Proposition 1, target spread | Add $pF(p)D(p)$. Its FOSD comparative static can fail when reserve admission differs. |
| Proposition 1, gross profits | The fixed-belief deterrence result survives. Class FOSD also keeps the profit gap nonnegative. |
| Equations (7)–(8), Proposition A.1 | Keep the likelihood bound; replace symmetric posterior endpoints with $m_\pi,M_\pi$. |
| Equations (9)–(11), Proposition A.2 | Keep the two-class inversion and cancellation when the floor and positive spread hold. |
| Global bound (A.6) | Replace $m$ with $\min(m_\pi,1-M_\pi)$. |
| Candidate equality (A.7) | Replace one common $J$ with $J_H,J_L$. Their ratio is $(1-\pi)/\pi$. |
| Proposition 2(i)–(ii) | Use (N1)–(N3) for trade and entry. Add (N4) for class-$H$ ownership. |
| Proposition 2(iii) | Recheck the global bound at $r_2$ if the spread need not rise. Also recheck the floor. |
| Equation (12) | Shift log odds by $\operatorname{logit}\pi$; use prior weights and $w_H$. |
| Proposition A.3 | Fixed-experiment deterrence survives because each $g_j$ falls. |
| Proposition A.4 | No-trade existence becomes $k\ge e(\pi)\Delta_T\max(\pi,1-\pi)$. Its region can be disconnected. |
| Section 6.3 | The small-class case fits this framework. Larger widths need fresh cost windows and reserve terms. |

**Open.** The computations do not map intermediate or mixed equilibria outside the sufficient uniqueness regions. They do not cover more than two classes or an investor who observes the exact value.

## 5. Numerical example

**Numerical diagnostic.** At the benchmark vector, use N05 and $\pi=.5$. The small class extension gives

| Strength and profile | $\Delta_T$ | Entry | Class-$H$ ownership | Expected target proceeds |
|---|---:|---:|---:|---:|
| $r=1.2$, unique no trade | .017013889 | .250000000 | .125000000 | .392664931 |
| $r=3$, unique full orders | .666805556 | .522760245 | .324194504 | .872367203 |
| $r=3.6$, unique full orders | .939004630 | .250000000 | .125000000 | .664221644 |

At $r=3$, prices at $(m_\pi,\pi,M_\pi)$ are $(.576048186,.614565972,1.362335033)$. The upper price includes high-cost entry. At $r=3.6$, $B(M_\pi)=5.997342225<6$, so high-cost entry stops.

The half-width matters at this boundary. With N50, high-cost entry remains at $r=3.6$ because $B(M_\pi)=6.000423846$. Its ceiling occurs at $r=3.601154502$. For N100, the ceiling is $3.630581180$.

The independent script is:

`audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py`

Run these exact commands from the repository root:

```bash
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py quadrature
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py scan
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py pairs
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py examples
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py failures
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py deviations
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py boundaries
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py memo_tables
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q1_N_numerics/explore.py features
```

The commands print results and do not write output files. The script contains no assertions. The run used Python 3.12.13, NumPy 2.5.2, and SciPy 1.18.1. The quadrature seed is 20261021. The source contains all parameter declarations, tolerances, and grid sizes.

## 6. Open issues and risks

1. **Open:** the bounds do not exhaust the equilibrium correspondence. An empty uniqueness region does not imply multiplicity or nonexistence.
2. **Open:** a failed (N1)–(N3) grid search does not rule out a pair under sharper bounds or intermediate orders. N100 is the clearest case.
3. **Numerical diagnostic:** W20's successful windows are narrow. Rounded or altered parameters can close them. Use the full declared inputs for replication.
4. **Analytical:** class-$H$ entry and class-$H$ ownership differ by $w_H(r)$. A class label cannot replace a realized-value welfare criterion.
5. **Numerical diagnostic:** all reported arithmetic uses floating-point quadrature and root calculations. It is not an interval certificate.
6. **Open:** the numerical work does not address distribution choice, more than two classes, or exact-value observation.

## 7. Recommendation

1. Use the general-prior, two-class version for the first extension. Retain the low-cost floor for the main theorem.
2. State the reserve correction before any comparative static. Either impose equal admission probabilities or use the exact derivative condition.
3. Present N05 as the direct benchmark extension. Present W20 as a distinct, narrow-window example with overlap and reserve exclusion.
4. State ownership separately from entry. Include the factor $w_H$ and condition (N4).
5. Report the N100 failure as a limit of the current sufficient windows. Leave the wider equilibrium question open.

These recommendations use the analytical conditions and numerical diagnostics above. They do not require a change to the current manuscript before discussion.

## 8. Plain summary

**Numerical diagnostic.** The main idea survives when the investor knows a value class rather than an exact acquisition value. Small classes reproduce the benchmark. Several wide, overlapping classes also produce more preparation and more ownership by the high class after incumbent strength rises.

The distributional extension needs two corrections. First, a value above the reserve can create a sale when the incumbent cannot bid. This effect adds a term to the target-payoff spread. A stronger incumbent reduces that term. In one example, the spread falls even though the high class dominates the low class.

Second, a high-class challenger can lose. Its ownership probability equals its entry probability times its chance of victory. Higher entry alone does not prove higher ownership.

The calculations find successful parameter pairs in 15 of 30 family-prior combinations. Each requested prior works for small classes. The widest symmetric class finds no pair within the paper's sufficient windows on the chosen grid.

**Open.** That failed search does not reject the mechanism. It leaves open whether sharper arguments or other equilibrium orders support the reversal.
