# Independent check of E2

## 1. Scope

This memo checks the four requested claims in [E2_information_side.md](E2_information_side.md).
The source is commit 01bd5d6daca14101afb3ef4b0c9e8035ba912181 of the paper repository.
The relevant statements are Propositions A.3, A.6, and A.7, plus the coexistence formulas.
The cost law and accuracy grid come from Online Appendix C.0, C.1, and C.3.

I read TEAM_RULES, EXTENSIONS_BRIEF, and E2 in full before the calculations.
I also read the project rules, BRIEF, T2's V3 material, and X_check.
I did not consult the excluded opinion files.

The model has one public order slot and the unit menu $\{-1,0,1\}$.
An informed investor fills the slot with probability $\lambda$.
Otherwise, a liquidity trader sells, waits, or purchases with probabilities $\beta,1-2\beta,\beta$.
Write $b=(1-\lambda)\beta$ and $c=1-\lambda-2b$.
The informed payoff conditions on an informed arrival.

I use perfect Bayesian equilibrium with competitive prices and truthful auction bids.
Every flow has positive liquidity mass, so Bayes' rule applies after every permitted deviation.
The default investor rule permits mixtures at indifference (IM).
The challenger prepares at indifference (C1).
I state the consequences of zero orders at investor indifference (I0) and challenger mixtures (CM) where relevant.
Continuous order sizes remain outside the scope.

Calibration A uses exact fractions.
Its parameters are $\lambda=6/17$, $\beta=1/3$, and $b=c=11/51$.
Calibration B uses 70-digit arithmetic and matches the unrounded Laplace entry at strength 3.
Its parameters are

$$
b_B=0.19561529390419246603923928117313390718506789686218,\qquad
\lambda_B=0.33612220488424935604005382944044002760839454424662.
$$

For either calibration, the posterior bounds are

$$
m(\pi)=\frac{\pi b}{b+(1-\pi)\lambda},\qquad
M(\pi)=\frac{\pi(b+\lambda)}{b+\pi\lambda}.
$$

These are E2's explicit parameters, rather than the brief's rounded entry match.
Section 4 records a display difference between these two conventions.
I treat high precision as arithmetic precision, not an interval certificate.

The independent scripts are [independent.py](../scripts/XE2_check/independent.py) and [domains.py](../scripts/XE2_check/domains.py).
Both contain new calculations from the primitives.
The first independent output preceded every E2 program run.
After that output, I ran common, x1_fixed_information, x3_atomless_costs, x4_signals, and coexistence_general_prior from E2.
Their captured outputs reside in the [script folder](../scripts/XE2_check/).
The runs used the slot wrapper, with at most three occupied slots.
The main numerical record is [independent_output.txt](../scripts/XE2_check/independent_output.txt).
The endpoint and antiderivative record is [domains_output.txt](../scripts/XE2_check/domains_output.txt).

**Evidence labels.** Complete arguments below are analytical.
Finite rational calculations are computer-assisted.
The 70-digit calculations support the displayed numbers and strict margins.
The independent Laplace cost calculation also has an elementary antiderivative.
No test suite, assertions, commit, or paper edit forms part of this review.

## 2. Verdict table

| Claim | Verdict | Evidence |
|---|---|---|
| X1: A.3 survives; frozen entry is flat; Laplace entry falls | **CONFIRMED** | Frozen entry equals $37/68$ under A and $0.522757297259738$ under B at both strengths. Laplace gives $0.562178058208428\to0.522757297259738$. See Section 3, X1. |
| X3: the declared atomless law preserves the reversal, but the floor at 3.6 fails | **CONFIRMED** | All five support and order margins are positive. Strong B entry equals its atomic value. Entry at 3.6 equals $0.382711560056650$ under B and $0.376679609378747$ under Laplace. See Section 3, X3. |
| X4: the declared entry and ownership values, and the six sufficient grid pairs | **CONFIRMED** | B gives $0.85\to0.879796646262606$ and $0.425\to0.449238172099428$. The six pairs exactly match the pinned paper. Every pair has $d>a$. See Section 3, X4. |
| Coexistence: the corrected no-trade law, common lower endpoint, and interior entry formula | **CONFIRMED WITH CORRECTION** | The formulas hold on their economic branch. The common endpoint admits $\pi=\pi_{\rm lo}$ under C1/IM. The displayed prior interval does not bound all coexistence priors. The strength interval alone does not define the branch at arbitrary priors. See Section 3, coexistence. |

The independent slot numbers agree with the E2 reruns.
The E2 Laplace quadrature has small errors in its undisplayed digits.
Those errors do not change the requested six-decimal values.

## 3. Derivations

### Common auction objects

For a prepared challenger with value $\theta\ge p$, integrate the auction payments over $R\sim U[0,r]$:

$$
\begin{aligned}
t(\theta)
&=\frac{p^2}{r}
 +\frac1r\int_p^{\min\{\theta,r\}}R\,dR
 +\frac{\theta(r-\theta)_+}{r},\\
g(\theta)
&=\frac{p(\theta-p)}r
 +\frac1r\int_p^{\min\{\theta,r\}}(\theta-R)\,dR.
\end{aligned}
$$

The scripts integrate these pieces separately.
With $h=10$, $\ell=1$, and $p=1/2$, the results are

$$
t_0=\frac12-\frac1{4r},\quad
t_H=\frac r2+\frac1{8r},\quad
t_L=1-\frac3{8r},\quad
g_H=10-t_H,\quad g_L=\frac3{8r}.
$$

Therefore

$$
\Delta_T=\frac{(r-1)^2}{2r},\qquad
B_r(\mu)=g_L+\mu(g_H-g_L),\qquad
\tau(r)=\frac{48r-3}{4(20r-r^2-1)}.
$$

These expressions agree with paper equations (4) and (5).
Both class profits fall with $r$ on $1<r<10$.
The threshold rises because

$$
\tau'(r)=\frac{48r^2-6r+12}{4(20r-r^2-1)^2}>0.
$$

The relevant threshold values are

$$
\tau(6/5)=\frac{195}{308},\qquad
\tau(3)=\frac{141}{200},\qquad
\tau(18/5)=\frac{4245}{5804}.
$$

### X1: the fixed experiment

**Analytical.** Fix the joint law of the signal and class.
Keep the cost independent of both.
For every signal realization, the entry difference is

$$
\mathbf1\{C\le B_{r_0}(\mu)\}
-\mathbf1\{C\le B_{r_1}(\mu)\}
=\mathbf1\{B_{r_1}(\mu)<C\le B_{r_0}(\mu)\}.
$$

The right side is nonnegative.
Its expectation is positive exactly when the cost crossing has positive probability.
This proves A.3 for the slot without a strict-decrease claim.

Freeze full orders and set $\pi=1/2$.
The flow posteriors are

$$
(\mu_{-1},\mu_0,\mu_1)=(1-M,1/2,M),\qquad
M=\frac{b+\lambda}{2b+\lambda}.
$$

Their probabilities do not depend on strength.
At both 1.2 and 3, the threshold lies strictly between $1/2$ and $M$.
Only the purchase flow induces expensive preparation.
Thus

$$
\mathsf E_{\rm frozen}
=\rho+(1-\rho)(b+\lambda/2),\qquad
\mathsf O_{H,\rm frozen}
=\frac12\{\rho+(1-\rho)(b+\lambda)\}.
$$

| Law | Entry at 1.2 | Entry at 3 | High-class ownership at both strengths |
|---|---:|---:|---:|
| Slot A | $37/68$ | $37/68$ | $23/68$ |
| Slot B | 0.522757297259738 | 0.522757297259738 | 0.324401562045666 |
| Laplace | 0.562178058208428 | 0.522757297259738 | 0.350606357934675 / 0.324192425775891 |

For Laplace scale 2, full orders give posterior log odds $x$ on $-1<x<1$.
The threshold flow is $x^*=\log[\tau/(1-\tau)]$.
Integration of each shifted density gives

$$
\alpha_H=1-\frac12e^{(x^*-1)/2},\qquad
\alpha_L=\frac12e^{-(x^*+1)/2},\qquad
\mathsf E=\rho+\frac{1-\rho}{2}(\alpha_H+\alpha_L).
$$

These formulas produce the Laplace row.
They also define the independent calibration B through

$$
b_B=\frac{\alpha_H(3)+\alpha_L(3)}{1+e},\qquad
\lambda_B=(e-1)b_B.
$$

The frozen weak profile is not an equilibrium.
Under A, its high-class purchase payoff is $-37/2400$.
The strong profile is an equilibrium.
Therefore the slot control requires “does not rise” between 1.2 and 3.
Between 3 and 3.6, the same full orders remain optimal and frozen entry falls to $1/4$.

### X3: the declared atomless cost law

**Analytical.** Let $U_{[v,w]}$ denote the uniform CDF on $[v,w]$.
The preparation probability is

$$
e_r(\mu)=\frac14U_{[0,1/5]}(B_r(\mu))
 +\frac34U_{[59/10,61/10]}(B_r(\mu)).
$$

Both calibrations have $c\ge b$.
Every flow posterior under any candidate lies between $m(\pi)$ and $M(\pi)$.
The low cost component always prepares when $B_3(m)>1/5$.
This gives the floor $e\ge\rho$ under every candidate at both strengths.

A correctly signed unit order reaches a known extreme flow.
Its residual is at least $\rho\Delta_T\min\{m,1-M\}$.
A weak order earns at most $\Delta_T$ before its fee.
Thus the following positive margins force zero weak orders and full strong orders:

| Margin | A, exact | B |
|---|---:|---:|
| $B_3(m)-1/5$ | $133/60$ | 2.166178511416626 |
| $59/10-B_{6/5}(1/2)$ | $263/240$ | 1.095833333333333 |
| $B_3(M)-61/10$ | $1/15$ | 0.117154821916707 |
| $1/50-\Delta_T(6/5)$ | $1/300$ | 0.003333333333333 |
| $\rho(1-M)\Delta_T(3)-1/50$ | $31/1200$ | 0.024823570228333 |

At strength 3, gross profit at the top posterior covers the whole high cost support.
Gross profits at the other two posteriors fall below its lower endpoint.
No posterior's gross profit lies inside either cost band.
Therefore the entry and ownership values equal their atomic-cost values exactly.
Under B, equilibrium entry rises from $1/4$ to $0.52275729725973785804444964692001544074194887673912$.
High-class ownership rises from $1/8$ to $0.32440156204566568327973491648009022554754841541580$.

At strength 3.6, the top profits are

$$
B_{18/5}(M_A)=\frac{42829}{7200}=5.948472222222222\ldots,
\qquad
B_{18/5}(M_B)=5.997311097734094887741289221574914\ldots .
$$

Both values lie strictly inside $[5.9,6.1]$.
Hence some challengers from the high cost component prepare at the purchase flow.
Full orders remain unique because the strong order margin grows with $\Delta_T$.
The floor conclusion of part (iii) therefore fails:

| Law | Entry at 3.6 | High-class ownership |
|---|---:|---:|
| Slot A | $1573/4896=0.321282679738562$ | $34601/195840=0.176679942810458$ |
| Slot B | 0.382711560056650 | 0.222019924462785 |
| Laplace | 0.376679609378747 | 0.217602665615690 |

The paper's A.6 expressly covers parts (i) and (ii).
The failure of part (iii) is not a refutation of A.6.
The Laplace upper plateau also has posterior $M_B$.
Its top profit lies inside the same cost band, so its entry also exceeds the floor.

For an independent Laplace calculation, integrate over cost rather than flow.
Set $v=(C-g_L)/(g_H-g_L)$ and $K=e^{-1/2}/2$.
On the interior posterior region,

$$
\alpha_H(C)=1-K\sqrt{\frac v{1-v}},\qquad
\alpha_L(C)=K\sqrt{\frac{1-v}{v}}.
$$

The required antiderivatives are

$$
\int\sqrt{\frac v{1-v}}\,dv
=\arcsin\sqrt v-\sqrt{v(1-v)},\qquad
\int\sqrt{\frac{1-v}{v}}\,dv
=\arcsin\sqrt v+\sqrt{v(1-v)}.
$$

Below $B_r(m)$, every flow permits preparation.
Above $B_r(M)$, no flow permits preparation.
Split the cost integral at these two values.
The antiderivative and split quadrature agree within $1.2\times10^{-70}$ for the reported entry and ownership values.

### X4: complementary private signals

**Analytical.** Write $\nu_Q=\Pr(T=+\mid Q)$ to distinguish it from the arrival probability $\lambda$.
Conditional independence implies

$$
\mu_Q=(1-a)+(2a-1)\nu_Q,\qquad
\phi_+(\mu)=\frac{d\mu}{d\mu+(1-d)(1-\mu)},\qquad
\phi_-(\mu)=\frac{(1-d)\mu}{(1-d)\mu+d(1-\mu)}.
$$

The extreme flows satisfy $\nu_Q\in[m,M]$ under every candidate.
Write $w_j=t_j-t_0$ and $I_y=\mathbf1\{B_r(\phi_y(\mu))\ge c_H\}$.
The price-specific preparation probabilities satisfy

$$
\begin{aligned}
e_H&=\rho+(1-\rho)\{dI_++(1-d)I_-\},\\
e_L&=\rho+(1-\rho)\{(1-d)I_++dI_-\},\\
\Delta_P&=e_Hw_H-e_Lw_L
=e_L\Delta_T+(e_H-e_L)w_H\ge\rho\Delta_T.
\end{aligned}
$$

The price is

$$
P=t_0+e_L(P)w_L+\mu_Q\Delta_P(P).
$$

The positive coefficient permits inversion for $\mu_Q$.
Thus the price supplies the flow posterior.
Conditional investor payoffs use beliefs $a$ and $1-a$.
Their correctly signed residuals are

$$
A_+=(2a-1)(1-\nu_Q)\Delta_P,\qquad
A_-=(2a-1)\nu_Q\Delta_P.
$$

The upper residual bound is

$$
A^+=(2a-1)\{\Delta_T+(1-\rho)(2d-1)w_H\}.
$$

Therefore $A^+(r_0)<k$ forces zero weak orders.
The bound $(2a-1)m\rho\Delta_T(r_1)>k$ forces full strong orders.
The slot needs no Laplace convolution factor.
The two preparation conditions exclude private-only entry and permit joint entry.
These arguments permit arbitrary investor mixtures and both challenger tie rules.

For $(a,d)=(0.70,0.75)$, the four B margins are

$$
(0.0525,\ 0.0452651534173,\ 0.00145454545455,\ 0.0185942914607).
$$

Only $(Q=1,Y=+)$ induces high-cost preparation at strong strength.
The class-specific probabilities of this event are $d(b+a\lambda)$ and $(1-d)(b+(1-a)\lambda)$.
Consequently,

$$
\begin{aligned}
\bar e_H&=\rho+(1-\rho)d(b+a\lambda),\\
\bar e_L&=\rho+(1-\rho)(1-d)(b+(1-a)\lambda),\\
\mathsf E&=(\bar e_H+\bar e_L)/2,\qquad
\mathsf O_H=\bar e_H/2.
\end{aligned}
$$

The independent program sums the full joint law over class, both signals, slot identity, and order.
It also prints each investor's payoff for every permitted unilateral order.
These direct calculations give

| Calibration | Weak entry | Strong entry | Weak ownership | Strong ownership |
|---|---:|---:|---:|---:|
| A | $17/20$ | $2999/3400$ | $17/40$ | $3067/6800$ |
| B | 0.85 | 0.879796646262606 | 0.425 | 0.449238172099428 |

The B pairs that satisfy all four sufficient conditions are

$$
\{(0.69,0.75),(0.70,0.75),(0.71,0.74),
  (0.71,0.75),(0.72,0.74),(0.72,0.75)\}.
$$

These are exactly the six rows marked “met” in the pinned paper's signal table.
Every pair has $d>a$.
A loses $(0.71,0.74)$.
The B strong entries at the six pairs are

$$
(0.879670600435774,\ 0.879796646262606,\ 0.879816813594899,\
 0.879922692089437,\ 0.879937817588657,\ 0.880048737916269).
$$

The unique order profiles also hold at the other accuracy pairs under these calibrations.
For a sharper weak bound, use $1-\nu_1\le M$ and $\nu_{-1}\le M$.
The maximum weak residual is then bounded by $MA^+$.
Across all 25 pairs, $k-MA^+$ is at least $0.0034493$ under A and $0.003352774725267$ under B.
The strong margins are at least $0.015915978260870$ under A and $0.015234862314626$ under B.
These strict bounds rule out extra order mixtures on the complete grid.

### Coexistence: domains and endpoints

**Analytical.** At no informed trade, every flow posterior equals $\pi$.
Define

$$
e_\pi=\rho+(1-\rho)\mathbf1\{\pi\ge\tau(r)\}.
$$

A high-class purchase earns $e_\pi\Delta_T(1-\pi)-k$.
A low-class sale earns $e_\pi\Delta_T\pi-k$.
Thus the exact condition is

$$
e_\pi\Delta_T\max\{\pi,1-\pi\}\le k.
$$

The coefficient is $\rho$ only when $\pi<\tau(r)$.
At $\pi=\tau(r)$, C1 sets the coefficient to one.
IM and I0 both permit no trade at investor indifference.

Now impose $\pi<\tau(r)$ and the no-trade condition.
Let $s$ denote the effective high-class purchase probability and $t$ the effective low-class sale probability.
Each lies in $[0,\lambda]$.
Bayes' rule gives

$$
1-\mu_1(s)=\frac{(1-\pi)b}{b+\pi s},\qquad
\mu_{-1}(t)=\frac{\pi b}{b+(1-\pi)t}.
$$

Low-class sales reduce both their posterior and their preparation probability.
Their return falls strictly below $\rho\Delta_T\pi\le k$ when $t>0$.
Therefore $t=0$ in every informative coexistence outcome.

The high-class purchase return is

$$
K_H(s)=e(\mu_1(s))\Delta_T\frac{(1-\pi)b}{b+\pi s}.
$$

Without high-cost entry, this return falls below its no-trade value.
Recruitment first occurs at

$$
s^*=\frac{b(\tau-\pi)}{\pi(1-\tau)}.
$$

It is reachable exactly when $\tau(r)\le M(\pi)$.
At this threshold, C1 gives return

$$
J(r)=\Delta_T(r)(1-\tau(r)).
$$

Above the threshold, the return falls continuously with $s$.
If the full purchase returns at least $k$, full purchase is optimal.
Otherwise, an interior rate exists exactly when $J(r)\ge k$.
This proves the following complete coexistence condition for C1/IM:

$$
\boxed{\quad
\pi<\tau(r)\le M(\pi),\qquad
\rho\Delta_T(r)\max\{\pi,1-\pi\}\le k\le J(r).
\quad}
$$

If $\pi\ge\tau(r)$, no-trade coexistence cannot occur.
The purchase return then starts at its largest value and decreases with the purchase rate.
The sale return also decreases with its rate.
When no trade is optimal, neither direction permits a positive equilibrium rate.

Define the floor-region boundary by

$$
r_N(\pi)=1+D_N+\sqrt{D_N^2+2D_N},\qquad
D_N=\frac{k}{\rho\max\{\pi,1-\pi\}}.
$$

It never exceeds $r_N(1/2)=1.747877538267963\ldots<7/4$.
To locate the common root, set $y=r-1$.
Then

$$
J(r)=\frac{y^2(27+24y-4y^2)}{144+288y+136y^2-8y^3}.
$$

Its derivative has the sign of

$$
y(972+2268y+1440y^2+3y^3-136y^4+4y^5).
$$

On $0<y<3/4$, the negative term has magnitude below $1377/32<972$.
All other coefficients are positive.
Therefore $J$ rises on $1<r<7/4$.
Also $J(1)=0$ and $J(5/3)-k=151/5700>0$.
The root is unique on the whole possible coexistence region.

Exact rational signs give

$$
\begin{aligned}
J(1.3939579202792)-k&<0,\\
J(1.3939579202793)-k&>0.
\end{aligned}
$$

The high-precision values are

$$
r_A=1.393957920279251333027115442253274\ldots,\qquad
\tau_A=0.640739075708409578001426306807851\ldots .
$$

For $r_A$ itself to be a coexistence endpoint, the prior must satisfy

$$
\pi_{\rm lo}\le\pi<\tau_A,\qquad
\pi_{\rm lo}=\frac{\tau_A}{(1+u)(1-\tau_A)+\tau_A}.
$$

The lower limits are

$$
\pi_{{\rm lo},A}=0.403518191170848328978908610041865\ldots,\qquad
\pi_{{\rm lo},B}=0.396175423610453726718233525785327\ldots .
$$

**Endpoint correction.** Under C1/IM, equality at $\pi_{\rm lo}$ is admissible.
Then $s^*=\lambda$ and the full purchase return equals $k$.
No trade also remains optimal.
Only $r=r_A$ supports coexistence at that prior.
For larger strengths, $\tau(r)>M(\pi_{\rm lo})$ prevents recruitment.

The prior interval above concerns the common attained endpoint.
It does not describe every prior with coexistence.
For example, $\pi=321/500=0.642>\tau_A$ admits coexistence at $r=3/2$ under both calibrations.
Under A, the informative equilibrium has

$$
s=\frac{16225}{98226},\quad t=0,\quad
\mathsf E=\frac{4009}{8160},\quad
U_H(1)=0,\quad U_L(-1)=-\frac{53}{8000}.
$$

The no-trade margin is $53/8000>0$.
Under B, the informative entry is $0.468844610055315321381398945812444\ldots$.
Its lower endpoint occurs after $r_A$, when $\tau(r)$ passes the prior.
The general coexistence condition retains the upper restriction $\tau(r)\le M(\pi)$ at every strength.

At $\pi=2/5$ under A, $M=58/91<\tau_A$.
Below $r_A$, $J<k$ prevents informative coexistence.
At or above $r_A$, $\tau>M$ prevents recruitment.
Hence coexistence is empty, as E2 states.

For the interior branch with entry one at $Q=1$, indifference gives

$$
b+\pi s=\frac{(1-\pi)b\Delta_T}{k}.
$$

The other posteriors satisfy $\mu_0<\pi<\tau$ and $\mu_{-1}=\pi<\tau$.
They retain entry $\rho$.
Therefore

$$
\boxed{\quad
\mathsf E=\rho+(1-\rho)\frac{(1-\pi)b\Delta_T}{k}.
\quad}
$$

Its branch conditions are $t=0$, $s^*<s<\lambda$, and $\pi<\tau(r)$.
On the open prior domain $\pi_{\rm lo}<\pi<\tau_A$, these reduce to

$$
r_A<r<r_F(\pi),\qquad
r_F(\pi)=1+D_F+\sqrt{D_F^2+2D_F},\qquad
D_F=\frac{k}{1-M(\pi)}.
$$

The strength interval alone is insufficient at arbitrary priors.
For $\pi=0.642$ and $r=1.4$, it holds under A, but $\pi>\tau(r)$.
The same algebraic purchase rate gives direct entry $6869/11900$, while the proposed formula gives $1236/2975$.
Their difference is $11/68$.
The low-class sale also earns $73/4375>0$, so this profile is not an equilibrium.
This example shows why the economic branch conditions must accompany the formula.

Under I0, the investor cannot use the interior branch.
Within the floor region, coexistence then requires full purchases with a strictly positive payoff.
It also requires $\tau(r)\le M(\pi)$.
Thus the condition $r_F(\pi)<r\le r_N(\pi)$ needs the recruitment restriction when the prior approaches $\pi_{\rm lo}$.

The independent grids reproduce E2's displayed branch counts at the common priors.
Under A, the entry formula differs from direct entry by exactly zero.
Under B, the largest printed discrepancy is below $2\times10^{-71}$.
At prior $1/2$, the A entries are $229/476$ at 1.4 and $8399/15776$ at 1.45.

## 4. Errors and corrections

1. **Coexistence endpoints and domains.**

   E2 Section 3.4 excludes $\pi_{\rm lo}$ from the endpoint domain.
   C1/IM admits this prior and gives singleton coexistence at $r_A$.
   Use $\pi_{\rm lo}\le\pi<\tau_A$ for the common attained endpoint.
   Do not interpret this interval as the full set of coexistence priors.
   Attach $\pi<\tau(r)$, feasible rates, and the absence of low-class sales to the interior formula.
   Retain $\tau(r)\le M(\pi)$ on any full-order coexistence claim.

2. **The two B conventions can change a displayed number.**

   E2 Section 2 says no displayed number changes between the exact and rounded entry matches.
   With the rounded entry match, high-class ownership is $0.324401344731384\ldots$.
   With E2's exact match, it is $0.324401562045666\ldots$.
   Their six-decimal displays are 0.324401 and 0.324402.
   The headline entry and signal results stay as reported under the explicit exact-match convention.

3. **The Laplace quadrature needs the cost-band breakpoints.**

   E2's x3_atomless_costs function laplace_mixture_entry splits flow at $-1,0,1$.
   It omits the interior flows where gross profit crosses the cost-band endpoints.
   The rerun gives entry $0.522714874037$ at 3 and $0.376679595131$ at 3.6.
   The independent antiderivative gives $0.522714716381306$ and $0.376679609378747$.
   Split at the reachable flows $\log[\tau_C/(1-\tau_C)]$, where $\tau_C=(C-g_L)/(g_H-g_L)$.
   The six-decimal entry displays and the failure of the floor at 3.6 remain correct.

These corrections do not refute X1, X3, or X4.
The no-trade coefficient and the interior entry identity are correct on their economic domains.
The older claim of a common coexistence endpoint for every prior is false.

## 5. Plain summary

X1 is confirmed.
The fixed-information proposition holds, but frozen slot entry is flat between strengths 1.2 and 3.
It equals 0.522757 under B and 37/68 under A.
The paper must use “does not rise” for this slot comparison.

X3 is confirmed.
The declared atomless costs preserve the reversal.
Strong B entry equals the atomic value.
Entry stays above the floor at strength 3.6 under both the slot and Laplace.
The paper's atomless-cost proposition does not claim that floor result.

X4 is confirmed.
Entry rises from 0.85 to 0.879797, and ownership rises from 0.425 to 0.449238.
The same six accuracy pairs meet the conditions under B.
Every pair has a more accurate challenger signal.

Coexistence needs precise domains.
The common lower endpoint includes the lower prior boundary under C1/IM.
Other priors can admit coexistence with a later endpoint.
The interior entry formula is exact on its economic branch.
I also found a display error and small errors in E2's Laplace quadrature.

