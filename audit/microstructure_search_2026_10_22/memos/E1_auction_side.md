# E1: Auction-side extensions under the order slot

## 1. Question

Do the general-prior proposition and extensions X2, X5, X6, and X7 hold under the order slot?
The two-class construction, general price-access result, and payment comparison hold.
The ledger proposition needs a missing hypothesis.
The unrestricted many-class price result fails.
The reserve example needs a change to retain its entry comparison across strengths.

All paper references use `overleaf/paper` commit `01bd5d6`.
Sources are `main.tex`, Sections 2–4, 5.2, 6.1–6.3, and Appendices A.1, A.4, A.6–A.8.
Additional sources are `online_appendix.tex`, A.8–A.10, A.13–A.14, C.4, C.7, and C.10.
The three source tables are `table_class_exhibit.tex`, `table2_equilibrium_controls.tex`, and `table4_reserve_comparisons.tex`.
The required prior memos are `T2_liquidity_trader.md` and `X_check.md`.
This memo checks only the specified coordinator note in the ledger.

## 2. Setup

### 2.1 Slot, information, equilibrium, and ties

The informed menu is $\{-1,0,1\}$.
An informed investor fills the slot with probability $\lambda$.
Otherwise, a liquidity trader uses probabilities $(\beta,1-2\beta,\beta)$.
There is no separate noise.
The identity draw is independent of the class, value, incumbent, and cost.
The investor sees the class, not its realized value.

Write $\eta_q=(\beta,1-2\beta,\beta)$ and $b=(1-\lambda)\beta$.
This $b$ denotes a slot probability, not the paper's noise scale.
The flow is the observed slot order $Q$.
Market makers set $P=\mathbb E[V_T\mid Q]$.
The challenger sees the price and its independent cost.
Preparation reveals its acquisition value.

The equilibrium concept is perfect Bayesian equilibrium with fixed candidate schedules for unilateral deviations.
The domains are $0<\lambda<1$ and $0<\beta<1/2$.
Every order has positive liquidity mass in every class, under every informed strategy.
Thus Bayes' rule applies everywhere on the unit menu.
No result here uses an off-path belief.
Continuous orders are outside scope.

The default investor tie rule, IM, permits mixtures at indifference.
I0 instead requires zero at indifference.
The default challenger rule, C1, requires preparation at indifference, including zero-cost indifference.
CM permits challenger mixtures at indifference.
Strict numerical examples survive both investor rules and both challenger rules.
The general floor and the endpoint reserve require C1 wherever zero-cost preparation has zero profit.

### 2.2 Auction objects

The class laws have finite means, satisfy first-order stochastic dominance, and put no value below $p$.
The incumbent law $F$ is continuous and independent.
Let $D(v)=G_L(v)-G_H(v)\ge0$.
The auction formulas follow directly from truthful bids:

$$
\begin{aligned}
t_0(F)&=p[1-F(p)],\\
g_j(F)&=\int_p^\infty[1-G_j(v)]F(v)\,dv,\\
t_j(F)&=p+\int_p^\infty[1-G_j(v)][1-F(v)]\,dv,\\
\Delta_F&=t_H(F)-t_L(F)=\int_p^\infty D(v)[1-F(v)]\,dv,\\
B_F(\mu)&=g_L(F)+\mu[g_H(F)-g_L(F)],\\
W_H(F)&=\mathbb E_H[F(\theta)\mathbf1\{\theta\ge p\}].
\end{aligned}
\tag{1}
$$

For $\theta\ge p$, the seller receives $\max\{p,\min(R,\theta)\}$.
The challenger receives $(\theta-\max\{p,R\})_+$.
Express each payoff as an integral of indicators, then average over $R$ and $\theta$.
This gives (1), by Tonelli's theorem.
The pointwise identity $t(\theta)+g(\theta)=\theta$ gives $\Delta_F+g_H(F)-g_L(F)=\Gamma$.
Here $\Gamma=\mathbb E_H[\max\{\theta,p\}]-\mathbb E_L[\max\{\theta,p\}]$.

If $F_1\le F_0$, equation (1) gives $g_j(F_1)\le g_j(F_0)$ and $\Delta_1\ge\Delta_0$.
These facts do not depend on the trade stage.
Section 3.5 uses the general-reserve formulas when the support restriction fails.

### 2.3 Calibration and arithmetic

Calibration A is $\lambda=6/17$, $\beta=1/3$, and $b=11/51$.
Hence $u=\lambda/b=18/11$.
Calibration B has $u=\exp(1)-1$.
It matches the paper's posterior bounds at every prior.
Its activity scale matches the unrounded benchmark Laplace entry, not the displayed decimal 0.522757.

For an exact definition of B, set

$$
\begin{aligned}
x_*&=\log(141/59),\\
\alpha_H^*&=1-\tfrac12\exp[(x_*-1)/2],\qquad
\alpha_L^*=\tfrac12\exp[-(x_*+1)/2],\\
E_*&=\tfrac14+\tfrac38(\alpha_H^*+\alpha_L^*),\qquad
d=\frac{E_*-1/4}{3/4},\\
b_B&=\frac d{1+u/2},\qquad \lambda_B=ub_B,\qquad
\beta_B=\frac{b_B}{1-\lambda_B}.
\end{aligned}
\tag{2}
$$

The resulting values are

$$
\begin{aligned}
E_*&=0.522757297259737858044449646920015441,\\
\lambda_B&=0.336122204884249356040053829440440028,\\
\beta_B&=0.294655575684807914696610854717407893,\\
b_B&=0.195615293904192466039239281173133907.
\end{aligned}
$$

The program uses exact fractions for rational inputs and polynomial auction integrals.
It uses `mpmath` at 40 decimal digits for irrational inputs.
It also uses outward interval arithmetic at 40 decimal digits.
The numerical tie tolerance is $10^{-30}$; an interval sign requires exclusion of zero.
The stated strict numerical classifications have much larger margins.
Displayed decimals are summaries; the CSV files retain fractions or 36 significant digits and interval enclosures.

## 3. Results

### 3.1 General-prior Proposition 2 — analytical; holds with change

#### The missing weak-cost hypothesis

The ledger's listed conditions do not imply $B_{F_0}(\pi)<c_H$.
Strength makes gross profit smaller, so $B_{F_1}(\pi)<c_H$ gives no such implication.
The omission can reverse part (i).

Take calibration A and the benchmark point values, prior, reserve, zero-cost probability, and trade cost.
Set $c_H=47/10$ and $(r_0,r_1,r_2)=(6/5,3,8)$.
The following exact margins are positive:

$$
\begin{aligned}
k-\Delta_0&=1/300,\\
c_H-B_1(\pi)&=49/120,\qquad B_1(M)-c_H=22/15,\\
c_H-B_2(M)&=223/640,\\
\rho\Delta_1\min\{1-M,m\}-k&=31/1200,\\
\rho\Delta_2\min\{1-M,m\}-k&=2439/12800.
\end{aligned}
$$

These margins verify every listed ledger inequality, including $\pi<\tau_1<M<\tau_2$.
But $c_H-B_0(\pi)=-5/48$.
Informed orders are uniquely zero at $F_0$, while both cost types prepare.
Weak entry equals one, not $\rho$.
The same example also fails part (i) under B; its interval margins appear in the output.

#### Correct statement

Let $F_1$ strengthen $F_0$, and let $F_2$ strengthen $F_1$.
Fix ranked, admissible classes, $0<\pi,\rho<1$, and an interior slot calibration.
Set

$$
m=\frac\pi{\pi+(1-\pi)(1+u)},\qquad
M=\frac{\pi(1+u)}{\pi(1+u)+1-\pi},\qquad
\kappa=\min\{m,1-M\}.
$$

Sufficient conditions are

$$
\boxed{
B_0(\pi)<c_H<B_1(M),\qquad
\Delta_0<k<\rho\kappa\Delta_1,\qquad
B_2(M)<c_H.}
\tag{3}
$$

The separate strong-prior and second trade conditions in the ledger are redundant under (3).
Indeed $B_1(\pi)\le B_0(\pi)$ and $\Delta_2\ge\Delta_1$.
Equation (3) forces a positive class profit gap at $F_1$.
If that gap vanishes at $F_2$, use $B_2(M)<c_H$ directly; no threshold quotient is necessary.

The outcomes are unique in orders and on-path preparation under C1:

- At $F_0$, informed orders are $(0,0)$ and entry equals $\rho$.
- At $F_1$, informed orders are $(1,-1)$, and only the positive flow recruits the high-cost type.
- At $F_2$, orders stay $(1,-1)$, but entry equals $\rho$ at every flow.

#### Proof and exact formulas

For an arbitrary informed strategy, $a_j(q)=(1-\lambda)\eta_q+\lambda\sigma_j(q)$.
At either nonzero flow, $b\le a_j(q)\le b+\lambda$.
Bayes' rule therefore bounds those two posteriors by $m$ and $M$.

Competitive prices satisfy

$$
P=t_0+e(P)[t_L-t_0+\Delta\mu_Q],\qquad
\mu_Q=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta}.
\tag{4}
$$

When $\Delta>0$, the entry floor makes the denominator positive.
Thus the price reveals the raw flow posterior in every two-class candidate equilibrium.
The conditional class residuals are $e\Delta(1-\mu_Q)$ for a high-class purchase and $e\Delta\mu_Q$ for a low-class sale.
These residuals use the informed slot event, without an extra factor $\lambda$.
Wrong-sign orders have nonpositive gross returns and pay $k$.

At $F_0$, every unit residual is at most $\Delta_0<k$.
Hence zero is the unique informed action in each class.
All posteriors then equal $\pi$, and (3) excludes high-cost preparation.
The constant price from (4) constructs the equilibrium.

At $F_1$ and $F_2$, each correct order earns at least $\rho\kappa\Delta_i>k$ under every candidate schedule.
Thus full orders are the unique best responses, including against mixed candidates.
Their posterior vector is $(m,\pi,M)$.
Since $B_1(\pi)\le B_0(\pi)<c_H<B_1(M)$, only $Q=1$ recruits at $F_1$.
Equation (4), the optimal entry rule, and truthful bids construct the equilibrium.
The final inequality of (3) excludes high-cost preparation at $F_2$.

At $F_1$, the positive-flow probability is $d_+=b+\pi\lambda$.
Its conditional probability in class H is $b+\lambda$.
Therefore

$$
\begin{aligned}
\mathsf E_1&=\rho+(1-\rho)(b+\pi\lambda),\\
e_H&=\rho+(1-\rho)(b+\lambda),\\
\mathsf O_{H,0}&=\pi\rho W_H(F_0),\qquad
\mathsf O_{H,1}=\pi e_HW_H(F_1).
\end{aligned}
\tag{5}
$$

The ledger's two level formulas are correct once (3) holds.
High-class ownership rises exactly when

$$
\boxed{[\rho+(1-\rho)(b+\lambda)]W_H(F_1)>\rho W_H(F_0).}
\tag{6}
$$

This condition matters when high values overlap incumbent support.
The paper's sufficient condition is $(1+\rho)W_H(F_1)\ge2\rho W_H(F_0)>0$.
It also suffices here when $b+\lambda>1/2$, as in A and B.
For other slots, use (6); the paper's proof uses a different conditional recruitment probability.
At $b+\lambda=1/2$, strict ownership needs a strict sufficient inequality or another strict margin.

#### Scope correction for the stated belief bounds

The same $m,M$ bound applies at zero under every strategy only if $1-2\beta\ge\beta$.
Thus the all-strategy bound in the brief needs $\beta\le1/3$.
Both A and B satisfy this restriction.
For $\beta>1/3$, use $u_*=\lambda/[(1-\lambda)\min\{\beta,1-2\beta\}]$ for a bound at every flow.

For example, take $\lambda=6/17$ and $\beta=2/5$ at prior one half.
Let class H wait and class L buy.
The zero-flow posterior is $41/52$, above the stated $M=26/37$.
This is an all-strategy counterexample, not an equilibrium claim.
The proof of (3) needs the original bounds only at the two nonzero orders.
It therefore remains valid on the full interior domain.

### 3.2 X2: Value classes

#### Any ranked class pair and any prior — analytical; holds

Fix an interior slot, ranked admissible classes with $\Gamma>0$, and any $0<\pi,\rho<1$.
This fixes $M>\pi$ and $\kappa>0$.
The construction needs no change in the slot parameters.
It chooses the strengths and costs separately for each class pair and prior.

Set $\Gamma(x)=\int_p^xD(v)\,dv$ and $u_0=\inf\{x\ge p:\Gamma(x)>0\}$.
For uniform incumbents on $[0,r]$, Tonelli's theorem gives

$$
\begin{aligned}
\Delta(r)&=\frac1r\int_p^r\Gamma(x)\,dx,\\
\Delta'(r)&=\frac{r\Gamma(r)-\int_p^r\Gamma(x)\,dx}{r^2}
\ge\frac{p\Gamma(r)}{r^2}>0\quad(r>u_0),\\
g_H(r)-g_L(r)&=\Gamma-\Delta(r)\ge\frac{p\Gamma}{r}>0.
\end{aligned}
\tag{7}
$$

Thus $\Delta(r)\to0$ as $r\downarrow u_0$.
At that limit, $B_{u_0}(M)-B_{u_0}(\pi)=(M-\pi)\Gamma>0$.
Finite means give continuity of $B_r$ and $W_H(r)$, by dominated convergence.
They also give $g_j(r)\to0$ as $r\to\infty$.
Moreover $W_H(u_0)\ge p/u_0>0$ under admissibility.

Let $e_H$ be the fixed slot coefficient in (5); it exceeds $\rho$.
Choose $r_1>u_0$ near enough that $B_{r_1}(M)>B_{u_0}(\pi)$ and $e_HW_H(r_1)>\rho W_H(u_0)$.
The paper's strict sufficient ownership inequality also holds for $r_1$ sufficiently near $u_0$.
Choose $r_0\in(u_0,r_1)$ near enough that $\Delta(r_0)<\rho\kappa\Delta(r_1)$.
Choose $k$ inside that strict interval and $c_H\in(B_{r_0}(\pi),B_{r_1}(M))$.
These choices satisfy (3), (6), and the paper's sufficient ownership condition.

Finally choose $r_2>r_1$ with $B_{r_2}(M)<c_H$.
Such a strength exists because gross profits tend to zero.
The spread at $r_2$ is at least the spread at $r_1$.
All inequalities have strict slack and continuous left sides.
They therefore hold on a nonempty open set of strengths and costs.
Near a degenerate prior or a small class gap, the required trade cost can be very small.

#### Moderate values and narrow uniform classes — computer-assisted; holds

Use the paper's moderate vector: $(h,\ell,p,\rho,c_H,k)=(2,1,1/2,1/4,89/100,1/500)$.
The strengths are $(21/20,3/2)$.
At the weak strength, $k-\Delta_0=17/21000>0$.
The strong lower return margin is $179/48000>0$ under A and $0.003602946279\ldots>0$ under B.
The strong upper cost margins are $59/2400>0$ and $0.030137030411\ldots>0$, respectively.
The other strict margins appear in `margins.csv`.

Entry rises from $1/4$ to $37/68$ under A and to $E_*$ under B.
The paper's corresponding Laplace level is 0.526805.
Both slot examples use the paper's costs and strengths without adjustment.

For uniform classes with half-width $\varepsilon=1/20$, direct integration gives

$$
\begin{aligned}
t_L&=\ell-\frac{\ell^2+\varepsilon^2/3-p^2}{2r},\qquad
g_L=\frac{\ell^2+\varepsilon^2/3-p^2}{2r},\\
t_H&=\frac r2+\frac{p^2}{2r},\qquad
g_H=h-t_H,\qquad
\Delta=\frac{(r-\ell)^2+\varepsilon^2/3}{2r}.
\end{aligned}
\tag{8}
$$

All benchmark support conditions hold at the three stated strengths.
Under B, the weak trade margin is $0.002986111111\ldots$ and the collapse cost margin is $0.002657774787\ldots$.
Under A, the corresponding margins are $0.002986111111\ldots$ and $0.051495949074\ldots$.
The remaining required margins are positive.
Entry is $(1/4,E_*,1/4)$ under B and $(1/4,37/68,1/4)$ under A.
The paper's strong Laplace level is 0.522760.

These different levels follow from the discrete experiment.
With strict full orders and only positive-flow recruitment, entry depends on the prior and slot parameters alone.
A change in the high cost cannot adjust that level while the same strict entry pattern persists.
To match another target entry $E^\dagger$ at fixed $u$, set

$$
b^\dagger=\frac{(E^\dagger-\rho)/(1-\rho)}{1+\pi u},\qquad
\lambda^\dagger=ub^\dagger,\qquad
\beta^\dagger=\frac{b^\dagger}{1-\lambda^\dagger}.
\tag{9}
$$

Each reported target lies inside the admissible local activity range.
Such adjustments preserve the two-class posterior bounds and trade margins.
They require separate activity choices for separate examples.
They do not generally match ownership, proceeds, or surplus at the same time.

For example, the following choices use the exact unrounded Laplace target and retain $u=\exp(1)-1$.
The program prints the defining calculations at 40 decimal digits.

| Target example | Required $\lambda$ | Required $\beta$ |
|---|---:|---:|
| Moderate values | 0.341109822957 | 0.301291441825 |
| Narrow classes | 0.336125837362 | 0.294660372298 |
| Exhibit A | 0.324368240261 | 0.279404805294 |
| Exhibit B | 0.334699704883 | 0.292781219950 |
| Exhibit C | 0.325959429663 | 0.281438245406 |

#### The constructive sequence in C.4 — computer-assisted; holds

The program also repeats the paper's five gap examples and its declared sequence.
It sets $\delta_n=(h-1)2^{-n}$, $r_1=1+\delta_n$, and $r_0=1+\delta_n^2/(h-1)$.
It retains the paper's cost recipe, including its extra factor one half in the upper trade bound.
Both slots admit the same first feasible member, $n=3$, for every reported ratio.
No slot adjustment is necessary.

| $h/\ell$ | First $n$ | $k$ | $c_H$ |
|---|---:|---:|---:|
| 1.05 | 3 | $4.78727292167222\times10^{-7}$ | 0.404458327034 |
| 1.10 | 3 | $1.90637768119299\times10^{-6}$ | 0.433917093296 |
| 1.25 | 3 | $1.17585845948951\times10^{-5}$ | 0.522295959655 |
| 1.50 | 3 | $4.60391046767497\times10^{-5}$ | 0.669602245428 |
| 2.00 | 3 | $1.76824201315770\times10^{-4}$ | 0.964242894678 |

The selected costs contain $\exp(1)$ and therefore use 40-digit interval arithmetic under both slots.
The output preserves the margins for $n=1,2,3$.
The table illustrates the construction's cost scale; it supplies no uniform positive lower bound on $k$.

#### Cases A, B, C, and the same-means control D — computer-assisted; holds

All cases use $(h,\ell,p,\rho)=(10,1,1/2,1/4)$ and zero low cost.
The class-exhibit letters below differ from the slot-calibration letters.

| Exhibit | Prior | $c_H$ | $k$ | $(r_0,r_1,r_2)$ | Class laws |
|---|---:|---:|---:|---|---|
| A | $3/10$ | $9/2$ | $1/100$ | $(11/10,3,18/5)$ | Point masses at 1 and 10 |
| B | $7/10$ | $36/5$ | $1/100$ | $(11/10,3,18/5)$ | Point masses at 1 and 10 |
| C | $7/10$ | $67/10$ | $1/50$ | $(1,9/2,11/2)$ | $U[3/5,7/5]$ and $U[1,19]$ |
| D | $7/10$ | $67/10$ | $1/50$ | $(1,9/2,11/2)$ | Point masses at 1 and 10 |

For each uniform class, the program splits its support at $p$ and $r$.
It integrates the exact quadratic payment and profit formulas on each piece.
This gives exact rational auction objects and win probabilities.
It then applies the finite slot law and prints investor payoffs and the inequalities in (3).

| Exhibit | Paper strong entry | Slot B strong entry | Slot A strong entry | Slot B strong ownership | Slot A strong ownership |
|---|---:|---:|---:|---:|---:|
| A | 0.464564 | 0.472338967 | 0.491176471 | 0.194640937 | 0.202941176 |
| B | 0.571808 | 0.573175628 | 0.597058824 | 0.454162187 | 0.473529412 |
| C | 0.563404 | 0.573175628 | 0.597058824 | 0.419819676 | 0.437722404 |
| D | 0.250000 | 0.250000000 | 0.250000000 | 0.175000000 | 0.175000000 |

Cases A–C have zero informed orders and entry $1/4$ at their weak strength.
They have full informed orders at both higher strengths.
Entry returns to $1/4$ at the final strength.
Case D also has these order profiles, but its entry stays at $1/4$ throughout.
All strict classifications hold under both tie rules for each player.

The decisive strong cost margins, $B_1(M)-c_H$, are

| Exhibit | Slot B | Slot A |
|---|---:|---:|
| A | 0.109179385204 | 0.045731707317 |
| B | 0.123412738148 | 0.093079096045 |
| C | 0.058890816750 | 0.030785424078 |
| D | -0.018121656697 | -0.045927495292 |

In C, $W_H(r_0)=1$ and $W_H(r_1)=599/648=0.924382716049\ldots$.
The paper's sufficient ownership margin is $0.655478395062\ldots>0$.
The exact slot margins in (6) are $0.349742394029\ldots$ under B and $0.375317719680\ldots$ under A.
Thus high-class ownership rises despite overlap with incumbent support.
At $r_2$, $W_H=79/88$ and ownership equals $553/3520$ under either slot.

For fixed $R$, the function $\theta\mapsto(\theta-\max\{p,R\})_+$ is convex.
Therefore dispersion around a fixed class mean weakly raises gross profit at every belief.
The positive C margin and negative D margin establish the requested distinction under both slots.
The paper's own costs and strengths suffice; no extra slot parameter is necessary.

#### More than two classes: whole-posterior sufficiency — analytical; fails

Equation (4) generalizes only to the posterior mean $\bar t_Q$ of class proceeds.
For several classes it gives

$$
P=t_0+e(P)(\bar t_Q-t_0),\qquad
\bar t_Q=t_0+\frac{P-t_0}{e(P)}.
\tag{10}
$$

The paper's A.13 uses the Laplace likelihood law to recover the whole posterior from that mean.
The slot does not retain that implication.
The following exact equilibrium is a counterexample, with calibration A unchanged.

Take $R\sim U[0,8]$, $p=1$, $\rho=1/4$, $c_H=10$, and $k=1/8$.
Use three classes with prior $(1/4,1/2,1/4)$.
Their value laws are

$$
G_1=\delta_1,\qquad
G_2=\frac{11}{102}\delta_1+\frac{91}{102}\delta_{10},\qquad
G_3=\delta_{10}.
$$

These classes satisfy strict stochastic order and admissibility.
Their proceeds are $(1,6091/1632,65/16)$, and $t_0=7/8$.
No high-cost type prepares, because every class gross profit is below 10.
Every zero-cost type prepares strictly, because each price leaves positive probability on a class with positive profit.
Consider informed orders $(-1,0,1)$ by class.

| Flow | Posterior over the three classes | Posterior mean proceeds | Price |
|---|---|---:|---:|
| $-1$ | $(29/62,11/31,11/62)$ | $63565/25296$ | $129967/101184$ |
| $0$ | $(11/80,29/40,11/80)$ | $347/102$ | $2459/1632$ |
| $1$ | $(11/62,11/31,29/62)$ | $347/102$ | $2459/1632$ |

The two last posterior vectors differ, but their prices coincide.
The challenger uses their pooled posterior when it sees that price.
Its preparation choice stays $\rho$, so both displayed prices remain competitive.
The investor's net payoffs establish strict optimality:

| Class | Sell | Wait | Buy |
|---|---:|---:|---:|
| 1 | $25621/101184$ | 0 | $-37/51$ |
| 2 | $-86987/202368$ | 0 | $-277/6528$ |
| 3 | $-6481/12648$ | 0 | $131/3264$ |

Each prescribed action is the unique best response on the entire unit menu.
All flows have positive liquidity mass, so no off-path rule or tie choice supports the example.
This refutes the unrestricted slot counterpart of A.13, not the paper's Laplace result.

The same construction also works under B, with a different middle-class mixture.
Write $b_0=(1-\lambda)(1-2\beta)$ and replace $91/102$ by

$$
w=\frac{(b+\lambda)/(4b+\lambda)-b_0/(4b_0+2\lambda)}
{(b_0+\lambda)/(2b_0+\lambda)-2b/(4b+\lambda)}.
\tag{10a}
$$

Normalize proceeds to $(0,w,1)$; their prior mean is $w/2+1/4$.
The two conditional means are

$$
\bar t_0=\frac{b_0(w/2+1/4)+\lambda w/2}{b_0+\lambda/2},\qquad
\bar t_+=\frac{b(w/2+1/4)+\lambda/4}{b+\lambda/4}.
$$

The equality $\bar t_0=\bar t_+$ rearranges to

$$
\left[\frac{b_0+\lambda}{2b_0+\lambda}-\frac{2b}{4b+\lambda}\right]w
=\frac{b+\lambda}{4b+\lambda}-\frac{b_0}{4b_0+2\lambda},
$$

which gives (10a).
Their posterior vectors still differ because the informed masses belong to different classes.
The 40-digit interval calculation gives $w=0.9407083097494903899014945229335121718\ldots\in(0,1)$.
The unique chosen-action net payoffs are $0.260795010719\ldots$, zero, and $0.024767959395\ldots$.
The middle class's purchase payoff is $-0.020627240953\ldots$; its sale payoff is also negative.
All other nonzero deviations lose, and the output encloses their signs.
Thus the B counterexample is **computer-assisted**, with price equality supplied by the exact formula.

#### More than two classes: the restricted two-group result — analytical; holds with change

The two-group comparison survives under a separation condition.
The incumbent law must strengthen, with the same class laws and preparation costs in both economies.
For A and B, let $\mathcal M$ contain posterior vectors with pairwise likelihood ratios bounded by $1+u$.
The common liquidity mass gives this bound under every informed strategy.
For $\beta>1/3$, replace $u$ by $u_*$ from Section 3.1.

Suppose every high-group proceeds value exceeds every feasible posterior mean by at least $\gamma>0$.
Suppose every low-group proceeds value lies below every feasible posterior mean by at least $\gamma$.
Require weak proceeds range below $k$ and $k<\rho\gamma$ in the strong economy.
Also require weak prior gross profit below $c_H$.
At the strong economy, require the high group's mean profit above the low group's mean profit.
Its gross profit at $M(\bar\pi)$ must exceed $c_H$.

The weak residual bound forces zero orders.
The strong residual bound forces every high-group class to buy and every low-group class to sell.
Under these orders, the flow identifies only the group.
Within each group, relative class probabilities stay at their prior proportions.
Thus the group posterior determines the whole posterior vector in this restricted equilibrium.
The entry formula is (5), with high-group prior $\bar\pi$.

Ownership needs the corresponding sum of class win probabilities and the comparison in (6).
The slot trade bound omits the paper's factor $1-1/b_{\rm noise}$.
This theorem covers separated groups, not arbitrary intermediate classes.
The unrestricted many-class extension therefore fails even though this restricted extension holds.

### 3.3 X5: Access to prices — analytical; holds in the proposition's region

This is a general result for every class pair and prior under (3).
It does not require uniform incumbents or point values.
It does require the strong economy's recruiting region, as the paper states.

Hide the price from the challenger, but retain it for trade and competitive market makers.
The challenger then uses $\pi$ and entry equals $\rho$.
The same strict lower return bounds force full informed orders in both economies.
Thus the slot experiment, informed trade probability, and realized trade cost are identical.
Any resource interpretation of the trade cost cancels.

Let $d_+=b+\pi\lambda$.
With access, only $Q=1$ adds high-cost preparation.
For general admissible classes,

$$
\begin{aligned}
\Delta\mathcal R_T
&=(1-\rho)\{\pi(b+\lambda)(t_H-t_0)+(1-\pi)b(t_L-t_0)\}>0,\\
\Delta\mathcal W
&=(1-\rho)d_+\{B_1(M)-c_H+pF_1(p)\}>0.
\end{aligned}
\tag{11}
$$

For each admissible value, the extra allocation value is

$$
\max(R\mathbf1\{R\ge p\},\theta)-R\mathbf1\{R\ge p\}
=(\theta-\max\{p,R\})_++p\mathbf1\{R<p\}.
$$

Conditional on $Q=1$, average this identity and subtract the preparation cost.
This gives the second line of (11).
Its bracket is strictly positive because $B_1(M)>c_H$.
For revenue, $t_H-t_0\ge\Delta_1>0$ and $t_L-t_0\ge0$.
The positive high-class mass proves the first strict inequality.
Under equal admissibility, replace the reserve term by $pF_1(p)[1-G_L(p^-)]$.

The proof depends on the trade stage through the bound that fixes full orders and through $d_+$.
The allocation identity and revenue gains do not depend on that stage.
An external deterministic dividend still cancels from $V_T-P$ and changes none of these real outcomes.

At the strong benchmark, the recomputed results are

| Quantity | Paper access | Paper hidden | Slot B access | Slot B hidden | Slot A access | Slot A hidden |
|---|---:|---:|---:|---:|---:|---:|
| Proceeds | 0.872392 | 0.614583 | 0.872531469 | 0.614583333 | $485/544$ | $59/96$ |
| Net surplus | 2.632301 | 2.552083 | 2.634043670 | 2.552083333 | $4285/1632$ | $245/96$ |

The B gains are $0.257948135941\ldots$ and $0.081960337085\ldots$.
The A gains are $113/408$ and $5/68$.
These levels need no new slot or cost choice.
Matching the benchmark entry in B does not match the paper's class-conditioned entry probabilities.
Thus its ownership, proceeds, and surplus differ slightly.

#### An unconditional interpretation fails — analytical

The paper does not claim that access always raises proceeds.
If $B_1(m)<c_H\le B_1(\pi)$, hidden entry equals one.
Access instead removes preparation at the negative flow.
With the same strict trade bounds, proceeds fall by

$$
-(1-\rho)\{\pi b(t_H-t_0)+(1-\pi)(b+\lambda)(t_L-t_0)\}<0.
\tag{12}
$$

For an exact example, retain calibration A and the strong benchmark but set $c_H=49/20$.
Access changes proceeds by $-77/408$ and net surplus by $-1/68$.
The removed preparation has positive allocation value net of its cost, because of the reserve term.
Under B, $c_H=12/5$ gives gains $-0.173917584720\ldots$ and $-0.013504716956\ldots$.
Their interval enclosures exclude zero.
Thus the correct general statement retains the paper's recruiting-region hypothesis.

### 3.4 X6: The payment rule — analytical; holds

This result concerns the acquisition stage only.
The slot leaves that stage unchanged.
The institution requires verifiable values, a zero reserve, and an enforceable sale to the next buyer at its value.
It is not an unspecified private-value bargaining game.
Assume the incumbent support is $[0,\bar r]$, with $0<\ell<\bar r<h$, as in the paper.

For fallback $z$ and winning value $V>z$, maximize $(P-z)^\eta(V-P)^{1-\eta}$ over $[z,V]$.
For $0<\eta<1$, the first-order condition is

$$
\frac\eta{P-z}-\frac{1-\eta}{V-P}=0
\quad\Longleftrightarrow\quad
\eta(V-P)=(1-\eta)(P-z).
$$

The second derivative of the log objective is negative.
Hence $P=(1-\eta)z+\eta V$ is the unique interior solution.
At $V=z$, feasibility fixes the transfer.
At $\eta=0$, use the continuous limit $P=z$.
Without a challenger, $z=0$ and the seller receives $\eta R$.

With a challenger, the winner has value $\max\{R,\theta\}$ and the fallback is $\min\{R,\theta\}$.
Therefore

$$
\begin{aligned}
T_\eta(R,\theta)&=(1-\eta)\min\{R,\theta\}+\eta\max\{R,\theta\},\\
g_{\theta,\eta}&=(1-\eta)\mathbb E[(\theta-R)_+],\\
\Delta_\eta&=\eta(h-\ell)+(1-2\eta)\mathbb E[(R-\ell)_+].
\end{aligned}
\tag{13}
$$

The last identity follows by subtracting the payments separately on $R\le\ell$ and $R>\ell$.
First-order stochastic strength reduces the expectation of $(\theta-R)_+$.
It raises the expectation of $(R-\ell)_+$.
Thus profit weakly falls, and the spread response has the sign of $1-2\eta$.
Strictness requires a positive change in the relevant expectation.

At the paper's strengths, exact values are

$$
\begin{array}{c|cc}
&r=6/5&r=3\\\hline
\Delta_\eta&1/60+(269/30)\eta&2/3+(23/3)\eta\\
g_{H,\eta}&(47/5)(1-\eta)&(17/2)(1-\eta)\\
g_{L,\eta}&(5/12)(1-\eta)&(1/6)(1-\eta)
\end{array}
$$

In particular, $\Delta_\eta(3)-\Delta_\eta(6/5)=(13/20)(1-2\eta)$.
The program prints every paper weight from 0 to 0.99 in steps of 0.01.
It also records $\eta=1$ as a payment-stage limit with zero buyer rents.
All 202 rows use exact fractions.
Calibrations A and B give identical acquisition-stage numbers and need no adjustment.
The paper leaves the full trade and preparation game under this institution open; this memo preserves that boundary.

### 3.5 X7: Reserve comparisons — computer-assisted; holds with change

#### General accounting and continuation statements — analytical

For any reserve, a value below $p$ gives $(t_v,g_v)=(t_0,0)$.
For $v\ge p$, the payments and profits in Section 2.2 apply.
For $R\sim U[0,r]$, the program uses

$$
(t_v,g_v,W_v)=
\begin{cases}
(t_0,0,0),&v<p,\\
(p,v-p,1),&p\ge r,\ v\ge p,\\
(v-v^2/(2r)+p^2/(2r),(v^2-p^2)/(2r),v/r),&p\le v\le r,\\
(r/2+p^2/(2r),v-r/2-p^2/(2r),1),&v\ge r\ge p.
\end{cases}
\tag{14}
$$

Integrate these formulas over each class, with a split at every support boundary.
The bid-equals-reserve convention applies at point values.
The continuous bands have no exclusion atom.
The zero-cost type still prepares at every belief under C1.
When $\Delta>0$, equation (4) still makes the price sufficient for the binary posterior.
These statements do not require equal admissibility.

Let $A_j=\Pr_j(\theta\ge p)$ and $e_j$ be conditional preparation.
Independence of $R$ gives

$$
\begin{aligned}
\mathsf E&=\pi e_H+(1-\pi)e_L,\\
\mathsf A&=\pi e_HA_H+(1-\pi)e_LA_L,\\
\mathsf C_2&=[1-F(p)]\mathsf A,\qquad
\mathsf S=1-F(p)+\mathsf A-\mathsf C_2,\\
\mathcal R_T&=t_0+\pi e_H(t_H-t_0)+(1-\pi)e_L(t_L-t_0).
\end{aligned}
\tag{15}
$$

Thus preparation, admissibility, sale, and two bidders remain distinct events.
The seller still needs a complete equilibrium selection after every reserve.
The slot does not by itself establish that selection, existence at every reserve, or a global optimum.

The local revenue decomposition also survives on a regular branch below every class value:

$$
\mathcal R_T'=(1-\mathsf E)(1-2p/r)+\mathsf E\,p/r
+\sum_j\pi_j e_j'(t_j-t_0).
\tag{16}
$$

For atomless costs, write $e_j=\sum_q a_j(q;p)H_C(B_q(p))$.
Differentiation gives

$$
e_j'=\sum_q\left[a_j' H_C(B_q)+a_j h_C(B_q)
\{-p/r+(g_H-g_L)\mu_q'\}\right].
\tag{17}
$$

This finite sum replaces the paper's integral.
It requires differentiable strategies and cost laws.
The current cost atoms instead give constant entry between thresholds and jumps at thresholds, when full orders persist.
The level objective (15) applies at those jumps.

#### The paper's two reserve choices

The point example uses $p=1/2$ and $p=101/100$.
The band example uses $p=1/2$ and $p=11/10$.
All other costs and strengths stay at their paper values.
Every listed zero-order node has $k>\Delta$.
Every listed full-order node has both global return floors above $k$.
The output gives exact A signs and outward B enclosures for these facts.

| Values | Slot | $r$ | $p$ | Preparation | Sale | Two bidders | Proceeds |
|---|---|---:|---:|---:|---:|---:|---:|
| Point | B | 1.2 | 0.5 | 0.250000000 | 0.687500000 | 0.145833333 | 0.392708333 |
| Point | B | 1.2 | 1.01 | 0.522757297 | 0.431371315 | 0.051363581 | 0.440564568 |
| Point | B | 3 | 0.5 | 0.522757297 | 0.920459550 | 0.435631081 | 0.872531469 |
| Point | B | 3 | 1.01 | 0.522757297 | 0.772548526 | 0.215186369 | 0.994384449 |
| Band | B | 1.2 | 0.5 | 0.250000000 | 0.687500000 | 0.145833333 | 0.392664931 |
| Band | B | 1.2 | 1.1 | 0.522757297 | 0.380701432 | 0.027033464 | 0.420123248 |
| Band | B | 3 | 0.5 | 0.522757297 | 0.920459550 | 0.435631081 | 0.872503920 |
| Band | B | 3 | 1.1 | 0.522757297 | 0.752280573 | 0.205454323 | 1.022690237 |
| Point | A | 1.2 | 0.5 | 0.250000000 | 0.687500000 | 0.145833333 | 0.392708333 |
| Point | A | 1.2 | 1.01 | 0.544117647 | 0.443014706 | 0.053553922 | 0.452532475 |
| Point | A | 3 | 0.5 | 0.544117647 | 0.924019608 | 0.453431373 | 0.891544118 |
| Point | A | 3 | 1.01 | 0.544117647 | 0.777205882 | 0.224362745 | 1.008218873 |
| Band | A | 1.2 | 0.5 | 0.250000000 | 0.687500000 | 0.145833333 | 0.392664931 |
| Band | A | 1.2 | 1.1 | 0.544117647 | 0.393382353 | 0.028186275 | 0.434129902 |
| Band | A | 3 | 0.5 | 0.544117647 | 0.924019608 | 0.453431373 | 0.891515523 |
| Band | A | 3 | 1.1 | 0.544117647 | 0.757352941 | 0.214215686 | 1.036593137 |

Every revenue comparison across the two stated reserves keeps the paper's positive sign.
The higher reserve excludes the low class and supports informative orders even at the weak strength.
The stronger incumbent can still narrow the proceeds spread after exclusion.
For the bands at $p=11/10$, it falls from $81/80$ to $201/200$.
That acquisition-stage statement survives.

The preparation comparison across strengths changes.
At the higher reserve, both slots give equal preparation at the two strengths.
The paper instead reports 0.540309 and 0.511638 for the bands, and 0.543573 and 0.513373 for points.
The reason is exact: both slot nodes have full orders and recruit only at the same positive order.
Equation (5) then forces equal entry.
No activity choice common to the two economies can produce those distinct interior entry levels with that pattern.

#### A separate reserve choice restores strict deterrence

The qualitative deterrence example can use another reserve, without a change in costs or slot parameters.
Take $p=31/20$ for the point values or the narrow bands.
The weak incumbent is then excluded; the low class is also excluded.
The high class remains above the reserve and incumbent support.
At the weak strength, only the positive flow recruits.
At the strong strength, no flow recruits the high-cost type.

Full orders remain strict best responses.
For A, the weak top-profit margin is $101/800>0$ and the strong exclusion margin is $12269/96000>0$.
The weak lower trade margin is $277/3200>0$.
The strong lower trade margin is $7571/128000>0$.
B has the same strict signs, with strong lower trade margin $0.057404702838\ldots>0$.

| Slot | Weak preparation | Strong preparation | Weak proceeds | Strong proceeds |
|---|---:|---:|---:|---:|
| A | $37/68$ | $1/4$ | $713/1360$ | $17147/19200$ |
| B | 0.522757297 | 0.250000000 | 0.502822421 | 0.893072917 |

Both proceeds exceed their respective values at reserve one half.
This recovers strict deterrence and higher proceeds, but changes the paper's reserve and excludes the weak incumbent.
The original reserve 1.1 therefore needs a change for its strict cross-strength entry conclusion.

#### Exact reserve events

For point values at $r=3$, the slot event remains

$$
p_H=\sqrt{2r(10-6/M)-r^2}.
\tag{18}
$$

It equals $\sqrt{39/29}=1.159667015228\ldots$ under A and $1.325269828310\ldots$ under B.
At the exact equality, C1 admits the high-cost type at the positive flow.
Preparation is $37/68$ under A and $E_*$ under B.
Immediately above the event, it falls to $1/4$ while full orders persist locally.
Under CM, preparation at the equality can vary; the displayed endpoint uses C1.

At $p_L=h=10$, high-class gross profit is zero and the incumbent is excluded.
C1 preserves zero-cost preparation at every price.
The slot has unique full orders, preparation $1/4$, sale $1/8$, two bidders zero, and proceeds $5/4$.
These endpoint quantities agree under A and B.
The endpoint statement concerns point values; it is not the upper endpoint of the uniform high band.

## 4. Scorecard

### Calibration A

| Brief item | Result | Status |
|---|---|---|
| 1. Proposition 2(i) | Unique zero informed orders at 1.2; entry $1/4$. | analytical |
| 2. Proposition 2(ii) | Full orders at 3; entry $37/68$; high-class ownership $23/68$. | analytical |
| 3. Proposition 2(iii) | Full orders at 3.6; entry $1/4$; general statement needs (3). | analytical |
| 4. Coexistence | Prior checked memo gives coexistence at 1.55–1.65; its informative entry order is flat or downward. E2 owns the extension audit. | computer-assisted |
| 5. Price access | General theorem (11); benchmark gains $113/408$ and $5/68$. | analytical |
| 6. Off-path beliefs | Every unit flow has positive liquidity mass. | analytical |
| 7. Ties and mixtures | All strict example outcomes survive both investor rules; zero-cost equalities require the stated challenger convention. | analytical |
| 8. Knob | $\beta=1/3$, $\lambda=6/17$; no adjustment for the two-class examples. The strict reserve comparison uses another reserve. | computer-assisted |
| 9. Exact device precedent | Not established by this workstream; the prior memo leaves it unverified. | open |
| 10. Extension decision | X2 fails its unrestricted many-class statement; X7 changes at the paper's reserve. | analytical |

### Calibration B

| Brief item | Result | Status |
|---|---|---|
| 1. Proposition 2(i) | Unique zero informed orders at 1.2; entry $1/4$. | analytical |
| 2. Proposition 2(ii) | Full orders at 3; entry $E_*$; ownership 0.324401562. | computer-assisted |
| 3. Proposition 2(iii) | Full orders at 3.6; entry $1/4$; collapse cost margin 0.002688902266. | computer-assisted |
| 4. Coexistence | General-prior coexistence belongs to E2. No complete extension claim is made here. | open |
| 5. Price access | General theorem (11); benchmark gains 0.257948135941 and 0.081960337085. | computer-assisted |
| 6. Off-path beliefs | Every unit flow has positive liquidity mass. | analytical |
| 7. Ties and mixtures | Strict example signs have outward enclosures; the reserve event uses C1 explicitly. | computer-assisted |
| 8. Knob | Equation (2); same posterior bounds as Laplace, and one matched entry level. Other Laplace levels require separate activity choices. | analytical |
| 9. Exact device precedent | Not established by this workstream; the prior memo leaves it unverified. | open |
| 10. Extension decision | The unrestricted many-class claim fails under B as well; (10a) and outward payoff bounds give its counterexample. | computer-assisted |

## 5. Numerical examples and reproducible use

The source program is `scripts/E1_auction_side/calculate.py`.
Use its real command-line interface from the repository root:

```bash
bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh \
  .venv/bin/python \
  audit/microstructure_search_2026_10_22/scripts/E1_auction_side/calculate.py \
  --output-dir audit/microstructure_search_2026_10_22/scripts/E1_auction_side \
  > audit/microstructure_search_2026_10_22/scripts/E1_auction_side/results.txt
```

I ran this interface on the declared paper inputs and the stated counterexamples.
The run used one slot and finished in less than one second.
I examined the auction objects, conditional payoffs, entry, ownership, revenue, surplus, reserve measures, and interval signs.
The program contains no assertions and runs no test suite.

The output files are:

- `results.txt`: complete printed economic calculations, counterexamples, sequence margins, and exact reserve events.
- `examples.csv`: all two-class and original-reserve outcomes, with rational A values.
- `margins.csv`: theorem margins and their exact or outward-enclosed values.
- `outcome_intervals.csv`: outward enclosures for the B outcomes at the original numerical nodes.
- `bargaining.csv`: 202 exact payment-stage rows, including the endpoint limit.
- `manifest.json`: input location, source commit, precision, software versions, and file hashes.

For the fixed benchmark, the corrected prior windows remain

$$
\begin{aligned}
\text{A: }&\left(\frac{1551}{3262},\frac{46695}{91906}\right),\\
\text{B: }&(0.467850029686148511835102135490294736,
\ 0.500424307320063228162167539969775947).
\end{aligned}
$$

The missing weak-cost inequality is slack throughout these intervals.
Their binding inequalities are the strong recruitment condition and the final exclusion condition.
Thus the ledger's benchmark windows remain correct despite its incomplete general statement.

## 6. Open issues

- **open.** A full many-class characterization of the slot, beyond separated groups, remains unavailable.
  Whole-posterior sufficiency is false, so such a characterization must use the actual price information set.
- **open.** The full trade and preparation game under the bargaining institution remains open, as in the paper.
- **open.** The global seller reserve problem needs a complete continuation selection and an existence argument.
- **open.** E2 owns coexistence, fixed-information controls, continuous costs, and complementary private signals.
- **open.** An independent second-member check of this memo remains necessary.

The brief's replacement rule requires every extension to hold.
The exact many-class counterexample prevents that conclusion for the unchanged slot specification.

## 7. Plain summary

The slot supports the paper's two-class reversal for any ranked class pair and any interior prior.
Its proof uses the same auction objects but a simpler unit-order return bound.
Every requested two-class numerical example works with its paper costs and strengths under both calibrations.
The dispersed class exhibit raises entry, while point values with the same means do not.

The general ledger proposition omits a necessary weak-prior cost inequality.
An exact counterexample meets its listed conditions but gives weak entry of one.
The corrected theorem includes that inequality and the actual ownership comparison.
The brief's universal posterior bound also needs care at zero when liquidity abstention is rare.

Access to prices raises proceeds and net surplus throughout the corrected recruiting region.
Outside that region, access can reduce both quantities.
The verifiable-value payment comparison holds unchanged because it concerns the acquisition stage alone.

The original reserve choices still raise proceeds and support informative weak-incumbent trade.
They give flat entry across the two strengths, rather than the paper's strict deterrence.
A different reserve restores strict deterrence and higher proceeds but excludes the weak incumbent.

The broad many-class price statement fails.
An exact three-class equilibrium has two different posteriors at the same price.
The restricted two-group theorem survives under a separation condition.
Thus the unchanged slot does not satisfy the brief's rule for replacement in the main text.
