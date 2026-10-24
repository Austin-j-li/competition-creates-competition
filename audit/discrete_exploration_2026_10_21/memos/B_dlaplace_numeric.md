# B1. Discrete-Laplace equilibria: numerical verification

## 1. Question

Verify every candidate claim in the brief, Section 0. Describe all investor mixtures, all relevant challenger mixtures, and their entry outcomes.

The main claims hold at the stated benchmark. The feedback comparison needs a correction: its second net profit is $0.058334571$.
The exact information ceiling is $r_C=3.986096572$.
No trade and full purchases coexist on $[1.443321951,1.747877538]$, under ordinary investor indifference.

## 2. Setup

The base model uses discrete-Laplace noise and buy-only orders, $q\in\{0,1\}$.
Nature draws quality. The investor sees quality. Preparation reveals the acquisition value.
The point masses are $h=10$ and $\ell=1$.
The reserve is $p=0.5$, and $\rho=0.25$.
The benchmark uses $c_L=0$, $c_H=5$, $b=2$, $k=0.02$, $\pi=1/2$, and $\lambda=1$.

The investor is present with probability $\lambda$, independently of the other draws.
Write $\beta_H,\beta_L$ for its conditional purchase probabilities when present.
Absence produces order zero.

The equilibrium concept is Bayesian equilibrium with competitive prices, optimal preparation, and truthful auction bids.
The challenger observes the price alone.
Investor deviations hold the candidate price and preparation schedules fixed.
The main correspondence allows mixtures at investor indifference and at challenger indifference.
The selected challenger tie rule chooses preparation; the memo states each result that depends on this selection.
An investor rule that forces zero at indifference removes genuine investor mixtures.

Full noise support makes every integer flow occur under every investor strategy.
Every unilateral deviation also reaches only these on-path flows.
No off-path flow belief or refinement enters any result.
Prices outside the schedule's image do not affect a feasible deviation.

The paper source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
The auction formulas agree with equation (4), Appendix A.1, and Online Appendix A.2 at that commit.
The price and residual arguments agree with equation (10), Appendix A.2, and Online Appendix A.3.
Paper comparisons below refer to that commit alone.
The prior discrete memos supply context; they do not supply the numerical results below.

## 3. Results

### 3.1 Analytical: an exact reduction of every integer flow

Start with asymmetric geometric counts. Put $u=a_+$ and $v=a_-$, where $0<u,v<1$.
Their difference has probabilities

$$
n(z)=\frac{(1-u)(1-v)}{1-uv}
\begin{cases}u^z,&z\ge0,\\v^{-z},&z\le0.\end{cases}
$$

To derive the first line, sum over the common negative count:

$$
\Pr(G_+-G_-=z)
=(1-u)(1-v)u^z\sum_{j=0}^{\infty}(uv)^j
=\frac{(1-u)(1-v)}{1-uv}u^z.
$$

The second line follows from the same sum with the roles reversed.
The symmetric model sets $u=v=a=e^{-1/b}$.
The noise likelihood ratio is

$$
\frac{n(x-1)}{n(x)}=
\begin{cases}v,&x\le0,\\1/u,&x\ge1.\end{cases}
$$

Call these classes $B$ and $G$.
For arbitrary $(\beta_H,\beta_L)$, define

$$
D_{jB}=1-\lambda\beta_j(1-v),\qquad
D_{jG}=1+\lambda\beta_j(1/u-1).
$$

Each conditional flow probability is $n(x)D_{jc}$ within class $c$.
Bayes' rule therefore gives

$$
\mu_c=
\frac{\pi D_{Hc}}{\pi D_{Hc}+(1-\pi)D_{Lc}},\qquad c\in\{B,G\}.
$$

Every denominator is positive. No tail cutoff appears.
This formula covers the entire square $(\beta_H,\beta_L)\in[0,1]^2$.
The two posterior values need not differ.

The exact class masses are

$$
\begin{aligned}
s&=\Pr(Z\le0)=\frac{1-u}{1-uv},&
t&=\Pr(Z\ge1)=\frac{u(1-v)}{1-uv},\\
w&=\Pr(Z\ge0)=\frac{1-v}{1-uv},&
\eta&=n(0)=\frac{(1-u)(1-v)}{1-uv}.
\end{aligned}
$$

Thus $s+t=1$, $vs+w=1$, and $w-t=\eta$.
A purchase reaches $B$ with probability $vs$ and $G$ with probability $w$.
These probabilities sum all integer tails exactly.

At a challenger tie, entry can differ across flows with the same posterior.
The conditional likelihood ratio remains constant within each class.
All payoffs and outcomes therefore depend only on the noise-weighted class average of entry.
Any admissible average is realized by constant entry within that class.
The reduction remains exact when the challenger can mix.
It characterizes aggregate outcomes, rather than every equivalent price schedule at a tie.

### 3.2 Analytical: dominance, price sufficiency, and one scalar strategy

Use the verified auction objects:

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&g_H&=h-t_H,\\
g_L&=(\ell^2-p^2)/(2r),&\Delta_T&=(r-\ell)^2/(2r).
\end{aligned}
$$

Because $c_L=0$ and $g_L>0$, entry is at least $\rho$ at every posterior.
Competitive pricing implies

$$
P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X],\qquad
\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}.
$$

The denominator is positive. The price reveals the flow posterior, even when the challenger can mix.
Subtract the price from each conditional terminal value:

$$
V_H-P=e(P)\Delta_T(1-\mu_X),\qquad
V_L-P=-e(P)\Delta_T\mu_X.
$$

A low-quality purchase earns at most $-k<0$. Hence $\beta_L=0$ in every equilibrium.
This excludes every candidate with $\beta_L>0$, including mixtures.

Put $d=\lambda\beta_H\in[0,\lambda]$.
The remaining posteriors are

$$
m(d)=\frac{\pi[1-d(1-v)]}{1-\pi d(1-v)},\qquad
M(d)=\frac{\pi[1+d(1/u-1)]}{1+\pi d(1/u-1)}.
$$

The first decreases and the second increases with $d$.
For $u=v=a$, $\pi=1/2$, and $\lambda=1$, their extreme values are

$$
m_1=\frac{a}{1+a},\qquad M_1=\frac1{1+a}.
$$

The bounds $[m_1,M_1]$ also cover arbitrary investor profiles before dominance, because their likelihood ratios lie in $[a,1/a]$.

### 3.3 Analytical: all equilibrium conditions and all interior roots

Let $e_B,e_G$ denote class entry probabilities, including any challenger mixtures.
The high-quality investor's gross purchase gain is

$$
J_r(d;e_B,e_G)
=\Delta_T(r)\{vs\,e_B[1-m(d)]+w\,e_G[1-M(d)]\}.
\tag{1}
$$

Its net gain is $J_r-k$. Zero earns zero.
The complete investor conditions are

$$
\begin{array}{c|c}
\beta_H=0&J_r(0)\le k\\
0<\beta_H<1&J_r(\lambda\beta_H)=k\\
\beta_H=1&J_r(\lambda)\ge k.
\end{array}
\tag{2}
$$

The challenger chooses $e_c=\rho$ when $B_r(\mu_c)<c_H$ and $e_c=1$ when $B_r(\mu_c)>c_H$.
At equality, $e_c$ can be any value in $[\rho,1]$.
The selected tie rule sets $e_c=1$ there.

For fixed entry rates, define

$$
A=\pi(1-v),\quad D=\pi(1/u-1),\quad
C_B=vs(1-\pi)e_B,\quad C_G=w(1-\pi)e_G.
$$

Equation (1) becomes

$$
J_r(d)=\Delta_T\left(\frac{C_B}{1-Ad}+\frac{C_G}{1+Dd}\right).
$$

Both denominators are positive on $[0,\lambda]$.
Multiply $J_r(d)=k$ by their product:

$$
-kADd^2+
\{k(D-A)-\Delta_T(C_BD-C_GA)\}d
+k-\Delta_T(C_B+C_G)=0.
\tag{3}
$$

Every interior root is therefore a root of an explicit quadratic.
Only roots inside the corresponding entry interval survive.
There is no search mesh over investor probabilities.

Write $\tau_r=(c_H-g_L)/(g_H-g_L)$.
When $\tau_r>\pi$, the only possible entry change occurs at

$$
d_\tau=\frac{\tau_r-\pi}{\pi(1/u-1)(1-\tau_r)},\qquad M(d_\tau)=\tau_r.
\tag{4}
$$

It matters only when $d_\tau\in[0,\lambda]$.
When $\tau_r<\pi$, the possible change instead satisfies

$$
d_\tau=\frac{\pi-\tau_r}{\pi(1-v)(1-\tau_r)},\qquad m(d_\tau)=\tau_r.
$$

At an interior good-class tie, solve equation (1) for entry:

$$
e_G^*=\frac{k/\Delta_T-vs\,\rho[1-m(d_\tau)]}{w(1-\tau_r)}.
\tag{5}
$$

Retain the outcome exactly when $e_G^*\in[\rho,1]$.
The expensive challenger's preparation probability is $(e_G^*-\rho)/(1-\rho)$.
The bad-class tie follows from the same linear equation.
Pure strategies at a cost tie use the weak inequalities in equation (2).

Equations (2)–(5), plus the entry inequalities, exhaust every aggregate equilibrium outcome.
The enumeration includes all pure endpoints, all quadratic roots, and all threshold mixtures.

### 3.4 Analytical: uniqueness at both candidate strengths

At $r_0=1.2$, the residual bound holds for every posterior in $[0,1]$:

$$
J_{r_0}\le\Delta_T(r_0)=\frac1{60}<\frac1{50}=k.
$$

Every high-quality purchase loses money under every candidate belief and entry schedule.
Every low-quality purchase loses money by dominance.
Both types must choose zero.
Bayes' rule then gives the prior at every integer flow.
Since $B_{1.2}(1/2)=4.804166667<5$, entry is uniquely $\rho$.
This is uniqueness over the full strategy square, with no off-path rule.

At $r_1=3$, dominance first gives $\beta_L=0$.
Every remaining posterior is at most $M_1$.
Since entry is at least $\rho$, every purchase satisfies

$$
J_3\ge\rho(1-M_1)\Delta_T(3)
=0.06292344479969090589351657237574858687445343911518164>k.
$$

Thus $\beta_H=1$ is mandatory in every equilibrium.
The inequality is strict, so investor indifference cannot add a mixture.
The two resulting challenger gains differ strictly from $c_H$.
Challenger mixtures cannot add an outcome either.
The competitive schedule constructs existence.

The same lower bound rises with $r$.
It forces full purchases at $r=3.6$ and $r=4.2$ as well.
The discrete proof requires $b>0$, rather than the paper's sufficient restriction $b>1$.
There is no derivative over continuous order sizes.

### 3.5 Numerical diagnostic: candidate arithmetic and the cost window

All reported calculations use 60 decimal digits. Saved scalar results retain 52 significant digits.
The posterior endpoints are

$$
\begin{aligned}
m_1&=0.3775406687981454353610994342544915212467206346910898,\\
M_1&=0.6224593312018545646389005657455084787532793653089102.
\end{aligned}
$$

The exact candidate window is

$$
\left(B_{1.2}(1/2),B_3(M_1)\right]
=\left(\frac{1153}{240},\frac18+\frac{25}{3(1+e^{-1/2})}\right].
$$

Its numerical values are

$$
\boxed{c_H\in(4.804166666666666667,\;5.312161093348788039].}
$$

Thus the brief's $(4.80,5.31]$ is a rounded description.
It is not an exact admissible interval: some costs between $4.80$ and $4.804166667$ fail its lower condition.

The upper endpoint uses preparation at indifference.
If all challenger mixtures are permitted there, unique entry fails at that endpoint.
The robust open interval uses a strict upper inequality.

This window concerns the weak-to-strong increase.
For a return at the specified third strength $4.2$, the lower endpoint must also exceed $B_{4.2}(M_1)$:

$$
\boxed{c_H\in(4.932612129446811232,\;5.312161093348788039].}
$$

The benchmark $c_H=5$ satisfies both windows.

### 3.6 Analytical: entry, ownership, and the information ceiling

For any equilibrium, the conditional good-class probabilities are

$$
\Pr(G\mid H)=t+\eta d,\qquad \Pr(G\mid L)=t.
$$

Hence

$$
\begin{aligned}
e_H&=(1-t-\eta d)e_B+(t+\eta d)e_G,\\
e_L&=se_B+te_G,\\
\mathsf E&=\pi e_H+(1-\pi)e_L,\qquad
\mathsf O_H=\pi e_H.
\end{aligned}
\tag{6}
$$

The ownership formula uses $h>r$: a prepared high-value challenger always acquires the target.
It does not count investor shareholdings.

At symmetric full purchases with $\pi=1/2$ and $\lambda=1$,

$$
\Pr(G\mid H)=M_1,\qquad \Pr(G\mid L)=m_1,\qquad \Pr(G)=\frac12.
$$

When good news alone recruits expensive preparation,

$$
\mathsf E=\frac{1+\rho}{2}=0.625,\qquad
\mathsf O_H=\frac12[\rho+(1-\rho)M_1]
=0.3584222492006954617395877121545656795324797619908413.
$$

At no trade, these outcomes are $0.25$ and $0.125$.
Thus both ownership numbers in the brief are correct.

At a fixed posterior $M$,

$$
B_r(M)=Mh-\frac{Mr}{2}+\frac{(1-M)\ell^2-p^2}{2r}.
$$

Its derivative is negative on the auction domain.
Set this expression equal to $c_H$ and multiply by $2r$:

$$
Mr^2-2(Mh-c_H)r-[(1-M)\ell^2-p^2]=0.
$$

The relevant root is

$$
r_C=\frac{Mh-c_H+\sqrt{(Mh-c_H)^2+M[(1-M)\ell^2-p^2]}}{M}.
\tag{7}
$$

Use $M=M_1$ at the benchmark:

$$
\boxed{r_C=3.986096571638404418765878024201187426378462232326056.}
$$

Strictly above this strength, no equilibrium posterior can justify expensive preparation.
Entry returns to $\rho$, while full purchases and informative prices remain.
At equality, the selected preparation tie preserves entry $0.625$.
With challenger mixtures, every entry rate in $[0.25,0.625]$ occurs there.
The floor purchase profit at this strength exceeds $k$, so full purchases hold throughout that interval.

### 3.7 Numerical diagnostic: the feedback discrepancy

Compare two economies at $r=3$, with the same full-purchase experiment.
In the feedback economy, $(e_B,e_G)=(\rho,1)$.
In the price-hidden economy, entry stays at $\rho$.
The uniform purchase bound also forces full purchases in the latter economy.
Thus the comparison does not hold an unprofitable order profile fixed.

For a present high-quality investor, equation (1) simplifies to

$$
J_3(e_B,e_G)=\frac{\Delta_T(3)a}{(1+a)^2}(e_B+e_G).
$$

The exact gross and net gains are:

| Entry policy | Gross gain $J_3$ | Net gain $J_3-k$ |
|---|---:|---:|
| Entry after good news | 0.195836426834662074224419 | 0.175836426834662074224419 |
| Entry fixed at $\rho$ | 0.078334570733864829689768 | 0.058334570733864829689768 |

The feedback increment is

$$
(1-\rho)\frac{\Delta_T(3)a}{(1+a)^2}
=0.1175018561007972445346513475105034720950357794761544.
$$

These are conditional purchase profits, rather than unconditional investor profits or welfare gains.
Unconditional expected investor profit multiplies each net figure by $\pi\lambda=1/2$.

The claimed $+0.176$ is correct to three decimals.
The claimed $+0.060$ is not correct to three decimals; the correct value is $+0.058$.
At two decimals, the latter number rounds to $+0.06$.
No separate profit definition in this comparison produces $+0.060$ at the stated inputs.

### 3.8 Analytical: coexistence and the complete branch construction

At the benchmark, $B_r(1/2)<5$ throughout $r\in[1.05,5]$.
Thus $e_B=\rho$ on every equilibrium branch.
Write $J_0(r)=\rho\Delta_T(r)/2$ for the no-trade deviation gain.
Write $J_F(r)=J_r(1;\rho,1)$ while full purchases recruit entry.

Under symmetric noise and equal priors,

$$
\frac{J_r(d;e_B,e_G)}{\Delta_T}
=\frac1{1+a}\left[
\frac{ae_B}{2-(1-a)d}+\frac{e_G}{2+(1/a-1)d}
\right].
\tag{8}
$$

For constant entry rates, the second derivative in $d$ is strictly positive.
At $d=1$, the first derivative is

$$
\frac{J_r'(1)}{\Delta_T}
=\frac{a(1-a)}{(1+a)^3}(e_B-e_G)\le0.
$$

Therefore $J_r'(d)<0$ for $0\le d<1$ whenever $e_G\ge e_B$.
Each constant-entry interval contains at most one root.
The only upward jump comes from good-class recruitment at $d_\tau$.
Equation (5) fills that jump when challenger mixtures are allowed.
This proves that the listed branch types exhaust the benchmark correspondence.

Define $\mathfrak r(z)=\ell+z+\sqrt{z^2+2\ell z}$.
This is the root above $\ell$ of $\Delta_T(r)=z$.
The exact pure-branch endpoints are

$$
r_N=\mathfrak r(2k/\rho),\qquad
r_F=\mathfrak r\left(\frac{k(1+a)^2}{(1+\rho)a}\right).
\tag{9}
$$

No trade exists exactly when $r\le r_N$.
Full purchases first exist at $r_F$.
They persist after the information ceiling because the floor purchase gain already exceeds $k$ there.
Consequently,

$$
\boxed{\text{No trade and full purchases coexist exactly on }[r_F,r_N].}
$$

This is the proposed condition $J_0(r)\le k\le J_F(r)$, with the entry regime stated explicitly.
The upper inequality is weak under ordinary investor indifference.
If the investor must choose zero at indifference, the coexistence interval becomes $(r_F,r_N]$.
Pure coexistence does not require challenger mixtures.

Define two further endpoints through the exact entry threshold:

$$
J_{r_S}(d_\tau;\rho,1)=k,\qquad
J_{r_Q}(d_\tau;\rho,\rho)=k.
\tag{10}
$$

Their numerical values and the resulting intervals follow below.

### 3.9 Numerical diagnostic: every branch on $[1.05,5]$

The five boundaries are:

| Boundary | Value | Meaning |
|---|---:|---|
| $r_S$ | 1.405429758473252102 | Two interior branches meet at full costly entry. |
| $r_F$ | 1.443321951458308189 | Full purchases first become an equilibrium. |
| $r_N$ | 1.747877538267962744 | No trade ceases to be an equilibrium. |
| $r_Q$ | 1.762507287865237541 | The two remaining interior branches meet at floor entry. |
| $r_C$ | 3.986096571638404419 | Expensive entry reaches its information ceiling. |

The exact equations define the boundaries. The decimals are high-precision evaluations, rather than interval certificates.

Use these branch names:

- $N$: no trade; entry is $\rho$.
- $F$: full purchases; entry is $0.625$ below the ceiling.
- $T$: an investor mixture at $M(d)=\tau_r$, with entry from equation (5).
- $I_G$: an interior quadratic root with $(e_B,e_G)=(\rho,1)$.
- $I_\rho$: an interior quadratic root with both entry rates equal to $\rho$.

| Strength interval | All aggregate equilibria |
|---|---|
| $[1.05,r_S)$ | $N$ |
| $\{r_S\}$ | $N,T$; here $T$ has $e_G=1$ |
| $(r_S,r_F)$ | $N,T,I_G$ |
| $[r_F,r_N]$ | $N,T,F$ |
| $(r_N,r_Q)$ | $I_\rho,T,F$ |
| $\{r_Q\}$ | $T,F$; here $T$ has $e_G=\rho$ |
| $(r_Q,r_C)$ | $F$ |
| $\{r_C\}$ | Full purchases, with $e_G\in[\rho,1]$ |
| $(r_C,5]$ | Full purchases, with entry $\rho$ |

At $r_F$, the $I_G$ root reaches full purchases.
At $r_N$, the $I_\rho$ root reaches no trade.
At $r_S$ and $r_Q$, the coincident branch descriptions count as one outcome.

Representative outcomes are:

| $r$ | Branch | $\beta_H$ | $e_G$ | $\mathsf E$ | $\mathsf O_H$ |
|---:|---|---:|---:|---:|---:|
| 1.42 | $N$ | 0 | 0.25 | 0.25 | 0.125 |
| 1.42 | $T$ | 0.195877323 | 0.932593553 | 0.524080202 | 0.270226789 |
| 1.42 | $I_G$ | 0.470999178 | 1 | 0.576414185 | 0.309836434 |
| 1.60 | $N$ | 0 | 0.25 | 0.25 | 0.125 |
| 1.60 | $T$ | 0.240748886 | 0.444215213 | 0.329049984 | 0.167387914 |
| 1.60 | $F$ | 1 | 1 | 0.625 | 0.358422249 |
| 1.75 | $I_\rho$ | 0.035613612 | 0.25 | 0.25 | 0.125 |
| 1.75 | $T$ | 0.278419636 | 0.261050368 | 0.254548727 | 0.127462745 |
| 1.75 | $F$ | 1 | 1 | 0.625 | 0.358422249 |

The threshold branch's entry falls as strength rises in this example.
The $I_G$ branch instead has entry $0.558559101$, $0.576414185$, and $0.595796898$ at $r=1.41,1.42,1.43$.
Each strength also admits no trade.
Thus an increasing-entry informative family also coexists with no trade.
It uses high-quality investor mixtures, rather than the paper's partial low-quality sales.
The full-purchase branch has flat entry before the ceiling.

The selected challenger tie removes $T$ except where $e_G=1$.
The rule that forces zero at investor indifference removes every genuine interior investor mixture.
These selections leave the strict pure coexistence result intact.

### 3.10 Analytical: an open robustness region

Let $M_\lambda=M(\lambda)$ after low-quality dominance.
For any $\pi\in(0,1)$ and asymmetric geometric parameters, sufficient conditions are

$$
\begin{aligned}
&\Delta_T(r_0)<k<\rho(1-M_\lambda)\Delta_T(r_1),\\
&B_{r_0}(\pi)<c_H<B_{r_1}(M_\lambda),\\
&B_{r_2}(M_\lambda)<c_H,\qquad \ell<r_0<r_1<r_2<h.
\end{aligned}
\tag{11}
$$

The first inequality forces zero purchases at $r_0$ and full purchases at $r_1,r_2$.
The second excludes expensive preparation at the weak prior and induces it at the strong good-class posterior.
The third removes expensive preparation at every feasible equilibrium posterior at $r_2$.
Every good class has positive probability because $0<u,v<1$.
Equation (6) gives a strict increase in high-class ownership.
All inequalities are strict and continuous, so this region is open.
No equality of noise parameters is required.

For symmetric noise, fixed strengths $(1.2,3,4.2)$, and $\pi=1/2$, equation (11) gives the explicit region

$$
\frac1{60}<k<\frac16(1-M_\lambda),\qquad
\max\{B_{1.2}(1/2),B_{4.2}(M_\lambda)\}<c_H<B_3(M_\lambda),
$$

where

$$
M_\lambda=
\frac{1+\lambda(e^{1/b}-1)}{2+\lambda(e^{1/b}-1)}.
$$

The upper cost endpoint can be included under selected preparation at indifference.
It cannot be included in a claim of unique entry under all challenger mixtures.

### 3.11 Analytical: the exact cost region within the strict entry window

The sufficient region leaves useful parameter values outside it.
An exact characterization follows from the decreasing profit in equation (8).
This subsection assumes symmetric noise, $\pi=1/2$, and the strict cost inequalities in equation (11).
It allows every $\lambda\in(0,1]$.

At each strength, let $d_\tau$ denote the threshold in equation (4), when it lies in $[0,\lambda]$.
The following conditions are necessary and sufficient for the three stated unique outcomes:

1. At $r_0$, require $k\ge J_{r_0}(0;\rho,\rho)$.
2. If the weak economy has a reachable entry threshold, also require $k>J_{r_0}(d_\tau;\rho,1)$.
3. At $r_1$, require $k<J_{r_1}(d_\tau;\rho,\rho)$ and $k\le J_{r_1}(\lambda;\rho,1)$.
4. At $r_2$, require $k\le J_{r_2}(\lambda;\rho,\rho)$.

For necessity in step 2, a violation produces either a threshold mixture or full purchases at the weak strength.
For sufficiency, both decreasing segments then lie below $k$ for every positive purchase probability.
In step 3, a violation of the first inequality produces either no trade, a floor root, or a threshold mixture.
The second inequality is exactly the full-purchase condition.
Above the ceiling, equation (8) decreases throughout the strategy interval, which proves step 4.
These arguments also prove necessity in steps 1 and 4.

At $b=2$, $c_H=5$, and $\lambda=1$, the exact region reduces to

$$
\boxed{0.005769913955558236223<k<0.078978043567274165019.}
$$

The lower endpoint is the weak economy's profit just after entry recruitment.
The upper endpoint is the strong economy's floor profit at its entry threshold.
These are numerical evaluations of exact formulas.
This interval is wider than the sufficient interval $(0.016666667,0.062923445)$.

### 3.12 Numerical diagnostic: robustness calculations and asymmetric noise

The main parameter grid has 1,600 cases:

- $b\in\{0.5,1,1.5,2,2.5,3,4,5\}$.
- $\lambda\in\{0.1,0.25,0.5,0.75,1\}$.
- $k\in\{0.017,0.02,0.03,0.04,0.05\}$.
- $c_H\in\{4.81,4.9,5,5.1,5.2,5.3,5.5,6\}$.

The sufficient region, with selected preparation at its upper cost endpoint, contains 193 cases.
Every one gives the three requested unique outcomes.
Two further cases give those outcomes outside the sufficient region.
This comparison confirms sufficiency on the grid; it does not establish necessity.
The exact scalar conditions above provide the sharper characterization within their stated cost window.

At fixed $b=2$, $k=0.02$, and $c_H=5$, costly entry at $r=3$ requires

$$
\lambda\ge0.6314554073042306224151508085791023819707905307545059.
$$

The inequality is strict if unique entry must survive every challenger mixture.
Above this presence threshold, the return occurs before $4.2$.
Presence below this threshold still supports full purchases, but the good-class posterior cannot induce costly entry at $3$.

At $\lambda=1$ and fixed $(k,c_H)=(0.02,5)$, a three-strength reversal holds throughout

$$
1.862112711570552738<b<2.912621412941443390.
$$

Include the upper endpoint only under selected preparation at indifference.
The lower endpoint has a costly-entry tie at $4.2$, so it cannot deliver a unique return to the floor.
Smaller $b$ can move the return beyond $4.2$.
Larger $b$ can make prices too weak to recruit entry at $3$.

For asymmetric noise with $\lambda=1$, the same three-strength result holds on the explicit region

$$
\boxed{0.584484848484848485<u<0.709401709401709402,\qquad 0<v<1.}
$$

The exact bounds are $u>2411/4125$ and $u<83/117$.
They follow from $B_{4.2}(1/(1+u))<5<B_3(1/(1+u))$.
The purchase bound in equation (11) holds throughout this region.
Thus the sell-count parameter can differ arbitrarily from the buy-count parameter within its open domain.
It changes the frequency of good news and the size of the entry gain.

Examples with $u\ne v$ illustrate both persistence and movement of the ceiling:

| $(u,v)$ | Entry at $1.2$ | Entry at $3$ | Entry at $3.6$ | Entry at $4.2$ |
|---|---:|---:|---:|---:|
| $(0.4,0.7)$ | 0.25 | 0.468750 | 0.468750 | 0.468750 |
| $(0.7,0.4)$ | 0.25 | 0.781250 | 0.25 | 0.25 |
| $(0.55,0.65)$ | 0.25 | 0.566634 | 0.566634 | 0.566634 |
| $(0.65,0.55)$ | 0.25 | 0.683366 | 0.25 | 0.25 |

Each displayed strength has a unique investor outcome.
The first and third rows retain entry at $4.2$ because their information ceiling lies later.
This is a timing change, rather than a failure of the economic mechanism.

### 3.13 Analytical: general priors

At symmetric full purchases with $\lambda=1$,

$$
m_\pi=\frac{\pi a}{1-\pi+\pi a},\qquad
M_\pi=\frac{\pi}{\pi+(1-\pi)a}.
\tag{12}
$$

The conditional good-class probabilities remain $M_1$ and $m_1$.
They depend on noise and orders, rather than on the prior.
If good news alone induces costly entry, then

$$
\begin{aligned}
\Pr(G)&=\frac{\pi+(1-\pi)a}{1+a},\\
\mathsf E&=\rho+(1-\rho)\Pr(G),\\
\mathsf O_H&=\pi\left[\rho+\frac{1-\rho}{1+a}\right].
\end{aligned}
\tag{13}
$$

The candidate cost window becomes

$$
B_{r_0}(\pi)<c_H\le B_{r_1}(M_\pi).
\tag{14}
$$

Its upper endpoint again depends on the challenger tie rule.
Equation (7), with $M=M_\pi$, gives the information ceiling when the root lies in $(\ell,h)$.
A formal root below $\ell$ is outside the auction domain.
It does not represent a later return of entry.

For the fixed $b=2$ and strengths $1.2,3$, put $D_i=g_H(r_i)-g_L(r_i)$ and $\delta=g_L(r_1)-g_L(r_0)$.
Multiply the difference between the endpoints of equation (14) by $a+(1-a)\pi$:

$$
\delta a+[\delta(1-a)+D_1-aD_0]\pi-D_0(1-a)\pi^2.
$$

The cost window is nonempty exactly when this expression is positive.
Its numerical root interval is

$$
0.042757471378711618<\pi<0.752477650664080343.
$$

This condition concerns the existence of some suitable $c_H$.
The purchase inequalities remain separate requirements.
For example, the uniform strong purchase bound fails at $\pi=0.9$, $b=2$, and $k=0.02$.

At a prior-cost tie $B_r(\pi)=c_H$, no trade can support several entry schedules.
All flows retain the prior, but price-dependent challenger mixtures can create different prices.
The exact no-trade aggregate set is

$$
(e_B,e_G)\in[\rho,1]^2,\qquad
\Delta_T(1-\pi)(vs\,e_B+we_G)\le k.
$$

The correspondence stores the vertices of this polygon.
Their convex hull describes every aggregate outcome in this set.
This exception explains why strict prior-cost inequalities accompany uniqueness statements.

### 3.14 Numerical diagnostic: prior windows and entry paths

At fixed $c_H=5$, costly entry rises from the weak prior to the strong good-class price exactly within

$$
0.460913245960234679\le\pi<0.521799628942486085,
$$

under selected preparation at the lower boundary.
Use a strict lower inequality if entry must be unique under all challenger mixtures.
For the return to occur strictly before $4.2$, strengthen the upper restriction to

$$
\pi<0.509255047930127174.
$$

These intervals solve $M_\pi\ge\tau_3$, $\pi<\tau_{1.2}$, and $M_\pi<\tau_{4.2}$ directly.
They do not follow from a grid.

| $\pi$ | Full-purchase $m_\pi$ | Full-purchase $M_\pi$ | Cost window at $1.2,3$ | $r_C$ at $c_H=5$ |
|---:|---:|---:|---|---:|
| 0.40 | 0.287928712 | 0.523616138 | $(3.905833333,4.488467815]$ | 1.248369461 |
| 0.48 | 0.358922767 | 0.603473030 | $(4.624500000,5.153941919]$ | 3.498651122 |
| 0.50 | 0.377540669 | 0.622459331 | $(4.804166667,5.312161093]$ | 3.986096572 |
| 0.52 | 0.396526970 | 0.641077233 | $(4.983833333,5.467310278]$ | 4.439526611 |
| 0.60 | 0.476383862 | 0.712071288 | $(5.702500000,6.058927400]$ | 5.965391327 |
| 0.90 | 0.845171901 | 0.936862674 | Empty | 9.304640884 |

The corresponding entry paths at fixed $c_H=5$ are:

| $\pi$ | $r=1.2$ | $r=3$ | $r=3.6$ | $r=4.2$ |
|---:|---:|---:|---:|---:|
| 0.40 | 0.25 | 0.25 | 0.25 | 0.25 |
| 0.48 | 0.25 | 0.621326220 | 0.25 | 0.25 |
| 0.50 | 0.25 | 0.625000000 | 0.625000000 | 0.25 |
| 0.52 | 0.25 | 0.628673780 | 0.628673780 | 0.628673780 |
| 0.60 | 1 | 0.643368900 | 0.643368900 | 0.643368900 |
| 0.90 | 1 | 1 | 1 | 1 |

The $\pi=0.60$ row lacks the required weak-economy entry floor outcome because the prior already supports expensive entry.
The $\pi=0.52$ row has the initial rise but a later return.
The $\pi=0.40$ row never recruits expensive entry at the displayed strong strengths.

### 3.15 Analytical: ownership and a matched welfare calculation

Expected target proceeds follow directly from conditional entry:

$$
\mathcal R_T=t_0+\pi e_H(t_H-t_0)+(1-\pi)e_L(t_L-t_0).
$$

Without challenger preparation, expected acquisition value is $(r^2-p^2)/(2r)$.
For either challenger class, preparation adds expected acquisition value $g_j+p^2/r$.
To derive the last term, distinguish $R<p$ from $R\ge p$.
For $R<p$, entry creates acquisition value $v_j$, while challenger profit is $v_j-p$.
Their difference is $p$, and this event has probability $p/r$.
For $R\ge p$, the allocation gain equals challenger profit.

Net acquisition surplus, including the investor's real trading cost, is therefore

$$
\mathcal W=\frac{r^2-p^2}{2r}
+\pi e_H(g_H+p^2/r)+(1-\pi)e_L(g_L+p^2/r)
-c_H(\mathsf E-\rho)-\pi d k.
$$

At $r=3$, full purchases hold with and without price access.
The change in trading cost is zero.
Every added expensive preparation contributes $B_r(\mu)-c_H+p^2/r>0$ in conditional expectation.
Thus the matched welfare gain is positive.
The numerical values are $\mathcal R_T=0.942073166134$ and $\mathcal W=2.690393743339$ with feedback.
Without price access, they are $0.614583333333$ and $2.542083333333$.
The welfare gain is $0.148310410006$; it differs from the investor's feedback increment.

## 4. What it recovers or loses relative to the Laplace paper

The following comparisons concern this buy-only model, rather than a replacement manuscript specification.

| Paper item | Result here | Status |
|---|---|---|
| Proposition 1 | The auction formulas and both comparative statics stay unchanged. | analytical |
| Proposition 2(i)–(ii) | Unique no trade and unique full purchases survive on an open region. | analytical |
| Proposition 2(iii) | Bounded beliefs restore the ceiling; the benchmark return occurs above $3.986096572$. | analytical |
| Proposition 3 | Pure coexistence survives; interior branches also appear. Increasing entry occurs on $I_G$. | analytical conditions; numerical diagnostic endpoints |
| Proposition A.3 | Entry weakly falls at every fixed experiment because $\partial_rB_r(\mu)<0$. | analytical |
| Proposition A.4 | The no-trade boundary and information ceiling survive. The global derivative bound becomes unnecessary. | analytical |
| Proposition A.5 | The result needs full support and bounded discrete likelihood ratios. Logistic comparisons need another calculation. | analytical here; open for a new noise comparison |
| Proposition A.6 | Narrow cost perturbations preserve the strict reversal. A complete atomless-cost correspondence is outside this calculation. | analytical local persistence; open full extension |
| Proposition A.7 | Complementary private signals require state-dependent entry and new posterior formulas. | open |
| Proposition A.8 | The auction-stage institution comparison is unchanged. Its trading continuation requires separate work. | analytical auction comparison; open continuation |
| Proposition A.9 | The benchmark matched price-access welfare comparison survives; the external-dividend cancellation remains exact. | analytical |
| Proposition A.10 | A positive entry floor excludes the paper's zero-entry price pools in this domain. | analytical |
| Section 5 | Asymmetric geometric noise and general priors preserve a strict open region. Other noise and signal extensions need separate work. | analytical conditions; numerical diagnostic examples |
| Section 6 | The matched welfare result survives. Reserve choice and a seller's continuation remain outside this exercise. | analytical fixed reserve; open reserve choice |

The model loses endogenous purchase-sale asymmetry because sales are unavailable.
Its informative price has two posterior values, rather than a continuous interior range.
Full-purchase entry is flat before its ceiling, then jumps down.
The two classes restore feedback because recruitment occurs where the investor retains a positive residual advantage.
Unlike the three-point equal-noise model, every flow remains on path and every posterior remains strictly between zero and one.

For cost perturbations in Proposition A.6, preserve the strict inequalities in equation (11).
Any sufficiently narrow high-cost support then excludes entry at the weak prior and permits entry after strong good news.
A low-cost distribution with nonnegative support below all feasible challenger gains preserves the floor.
The same purchase bounds force the same order profiles.
This proves local persistence, without a full atomless-cost branch calculation.

The external-dividend diagnostic adds the same constant to terminal share payoff and price.
The constant cancels in $V_T-P$, so orders, entry, acquisition proceeds, and acquisition surplus stay unchanged.
This argument does not require continuous noise.

## 5. Numerical example and reproducible outputs

### Benchmark path

**Numerical diagnostic.** These are unique trading and entry outcomes at the stated benchmark inputs.

| $r$ | $(\beta_H,\beta_L)$ | $(e_B,e_G)$ | $\mathsf E$ | $\mathsf O_H$ |
|---:|---|---|---:|---:|
| 1.2 | $(0,0)$ | $(0.25,0.25)$ | 0.25 | 0.125 |
| 3 | $(1,0)$ | $(0.25,1)$ | 0.625 | 0.358422249200695462 |
| 3.6 | $(1,0)$ | $(0.25,1)$ | 0.625 | 0.358422249200695462 |
| 4.2 | $(1,0)$ | $(0.25,0.25)$ | 0.25 | 0.125 |

The good-class posterior at $3.6$ still justifies costly preparation.
Thus $3.6$ cannot replace $4.2$ as the return strength at $c_H=5$.

### Files

All files below are in `audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_numeric/`.

| File | Contents |
|---|---|
| `finite_classes.py` | Exact class masses, all quadratic roots, all entry thresholds, and tie outcomes. |
| `summary.json` | Inputs, 52-digit scalar results, branch boundaries, and precision records. |
| `equilibrium_branches.csv` | The Figure 2 analog: 480 outcome rows at 401 strengths, including every boundary. |
| `benchmark_points.csv` | Detailed outcomes at 16 sample strengths and the five boundaries. |
| `strength_entry_path.csv` | The four benchmark strengths requested in the task. |
| `robustness_windows.csv` | Sufficient cost windows at 40 noise-presence pairs. |
| `exact_cost_windows.csv` | Exact purchase-cost conditions at 39 feasible noise-presence-preparation-cost cases. |
| `asymmetric_examples.csv` | 72 outcomes for six asymmetric laws and three presence probabilities. |
| `prior_windows.csv` | Posterior bounds, cost windows, and formal ceilings for 11 priors. |
| `general_priors.csv` | Entry, ownership, prices, and profits at four strengths for each prior. |
| `receipt.json` | Inputs, method, pinned commit, output sizes, and file hashes. |

The strength grid is $1.05,1.06,\ldots,5$.
It supplements the exact branch construction; it does not replace the quadratic enumeration.
At $r_C$, two CSV rows describe the endpoints of the full challenger-mixture interval.
Every intermediate entry value is also an equilibrium there.
At a prior-cost tie, polygon vertices describe a continuum of no-trade aggregate outcomes.

Run from the repository root:

```bash
.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_numeric/finite_classes.py point --r 1.6
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_numeric/finite_classes.py report
```

The point command also accepts `--pi`, `--lam`, `--b`, `--k`, `--c-H`, `--a-plus`, and `--a-minus`.
The report command uses the benchmark for its branch endpoints and parameter summaries.

The real command interface produced the benchmark, interior branches, asymmetric examples, and prior-cost-tie outcomes.
The output was examined directly.
No test suite or assertion was used.
Long report runs used one shared CPU slot and one process.

The largest saved interior-profit residual is $4.87\times10^{-63}$.
The largest low-quality purchase payoff is $-0.020148809524$ on the strength grid.
The classification tolerance is $10^{-48}$.
Arithmetic uses 60 decimal digits, with decimal inputs parsed directly.
The output is a numerical diagnostic, rather than an interval certificate.

## 6. Open issues

### Comparison with the paired theory memo

**Analytical.** The paired memo exists as a skeleton at the comparison time.
The comparison time is 21 October 2026, 18:05 UTC.
Its SHA-256 is `d04d3a80b634a859711f20e0426248cdd4b0dddb7d5e4dd27e134836692f301d`.
Its completed theory, welfare, and numerical sections remain empty.
The following comparison concerns its explicit planned formulas alone.

- The half-line reduction agrees exactly.
- Its binary channel parameter $\gamma=1/(1+a)$ agrees with the conditional good-class probability here.
- Its purchase formula agrees after the substitution $s=d$, $N_+=t+\pi\eta d$, and $N_-=s_{\mathrm{noise}}-\pi\eta d$.
- Its coexistence inequality agrees in the strict interior. Equation (2) adds the full-purchase boundary under ordinary investor indifference.

The symbol $s_{\mathrm{noise}}$ in this comparison means the class mass called $s$ in Section 3.1.
It distinguishes that mass from the paired memo's effective order probability.
For symmetric noise, the common payoff is

$$
\Delta_T(1-\pi)\gamma(1-\gamma)
\left(\frac{e_G}{N_+}+\frac{e_B}{N_-}\right).
$$

**Analytical.** Its planned upper bound $J_r\le(1-\pi)\Delta_T$ also follows from this calculation.
Use $e_B,e_G\le1$ and

$$
N_+N_-=\gamma(1-\gamma)+\pi\eta^2d(1-\pi d)
\ge\gamma(1-\gamma).
$$

Since $N_++N_-=1$, the claimed bound follows by addition of the two fractions.
The paired memo's lower-bound symbol is not yet defined, so its precise lower bound remains unchecked.
No substantive disagreement appears in the formulas that it currently states.
Its final propositions and welfare convention remain unavailable for comparison.

### Remaining scope

**Open.** The general asymmetric correspondence is exact through equations (2)–(5), but its full parameter geometry is not tabulated.
The explicit open sufficient region and asymmetric examples answer the robustness question without that larger map.

**Open.** The decimal branch endpoints lack directed interval enclosures.
The finite reduction and quadratic completeness arguments are analytical.
The numerical endpoint evaluations retain their diagnostic label.

**Open.** The private-signal extension, reserve-choice continuation, and full atomless-cost correspondence remain separate tasks.
The current results concern fixed auction values and the stated reserve.

No browser, outside fetch, manuscript edit, or commit forms part of this calculation.

## 7. Plain summary

The discrete-Laplace proposal works at the benchmark.
The weak incumbent gives unique no trade and entry of 0.25.
The strong incumbent gives unique high-quality purchases and entry of 0.625.
High-class challenger ownership rises from 0.125 to 0.358422.
Entry returns to 0.25 strictly above incumbent strength 3.986097.

The infinite noise support creates no numerical tail problem.
All nonpositive flows share one likelihood ratio.
All positive flows share another.
Two exact classes therefore replace the infinite sum.
Every investor mixture reduces to a quadratic equation within each entry regime.
Challenger mixtures fill the entry jump at indifference.

No trade and full purchases coexist from 1.443322 through 1.747878.
Other interior equilibria appear before and after part of that interval.
One informative branch has entry that rises with incumbent strength.
Another has entry that falls.
The full-purchase branch has flat entry before the ceiling.

The feedback profit with entry is 0.175836 after trading cost.
Without an entry response, it is 0.058335.
The brief's 0.060 is incorrect at three-decimal precision.

Equal noise parameters are unnecessary.
An open region permits unequal geometric buy and sell counts.
Investor presence must be high enough for good news to justify costly entry.
General priors shift both the cost window and the return strength.

The cost window in the brief describes the initial entry rise.
A return specifically at strength 4.2 requires the narrower window stated above.
Boundary entry depends on the challenger tie rule.
