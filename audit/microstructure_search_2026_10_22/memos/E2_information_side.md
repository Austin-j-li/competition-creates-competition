# E2: The information-side extensions under the order slot

Workstream E2 of `EXTENSIONS_BRIEF.md`. Scripts and outputs: `scripts/E2_information_side/`. Not yet checked by a second member.

## 1. Question

Replace Laplace noise by the order slot as the trading stage.
Do the extensions X1, X3 and X4 of the paper still hold? Are the general-prior coexistence formulas in the ledger note right?

## 2. Setup

**Paper source.** `overleaf/paper` at commit `01bd5d6`: `main.tex` Sections 2–5.3, Appendix A.2, A.4 (atomless costs), A.5;
`online_appendix.tex` A.5–A.7, C.0, C.1, C.3. Copies of both files are in the script folder.

**Trading stage: the order slot (variant V3 two of T2).**

- One public order opportunity. With probability $\lambda$ the informed investor fills it.
- The investor sees the class $j$ (or, in X4, a signal $T$) and chooses $q\in\{-1,0,1\}$ at cost $k|q|$.
- With probability $1-\lambda$ a liquidity trader fills it. It sells, waits or buys with probabilities $\beta,1-2\beta,\beta$.
- Market makers see the order $Q$ and set $P=\mathbb E[V_T\mid Q]$. The challenger sees $P$ (and, in X4, its signal $Y$).
- Write $b=(1-\lambda)\beta$, $c=(1-\lambda)(1-2\beta)$, $u=\lambda/b$.

**Menu.** Two-sided unit menu $\{-1,0,1\}$. Continuous order sizes are out of scope (X_check §4, item 2).

**Liquidity device.** The liquidity trader has an exogenous motive. T2 §3.7 shows that a free uninformed trader would not trade.

**Classes and costs.** Reading N with point masses $h=10$, $\ell=1$, reserve $p=1/2$, uniform incumbent on $[0,r]$.
The low cost is zero ($c_L=0$). The prior is $\pi=1/2$ unless a section states otherwise.

**Posterior bounds.** A buy has likelihood ratio between $1/(1+u)$ and $1+u$ under every strategy. So at $Q=\pm1$ every posterior lies in
$[m(\pi),M(\pi)]$, with $m(\pi)=\pi/(\pi+(1-\pi)(1+u))$ and $M(\pi)=\pi(1+u)/(\pi(1+u)+1-\pi)$.
At $Q=0$ the ratio bound is $1+\lambda/c$, not $1+u$.
If $\beta\le1/3$, then $c\ge b$, and the zero-flow posterior also lies in $[m(\pi),M(\pi)]$.
Both calibrations satisfy $\beta\le1/3$. Section 3.2 uses this domain condition.

**Calibrations.**

| | $\beta$ | $\lambda$ | $b$ | $c$ | $u$ | $M(1/2)$ |
|---|---|---|---|---|---|---|
| A (exact) | $1/3$ | $6/17$ | $11/51$ | $11/51$ | $18/11$ | $29/40$ |
| B (40 digits) | 0.294655575685 | 0.336122204884 | 0.195615293904 | 0.272647207307 | $e-1$ | $e/(1+e)=0.731058578630$ |

Calibration B fixes $1+u=e$, so $M(\pi)$ equals the paper's Laplace bound at every prior.
I fix its second degree of freedom by an exact match: $b+\lambda/2=(\alpha_H+\alpha_L)/2$, with $\alpha_H,\alpha_L$ from paper eq. (12) at $r=3$.
The Laplace entry is $0.5227572972597\ldots$ to 40 digits. The closed form is $b=2\bar\alpha/(1+e)$, $\lambda=(e-1)b$, $\bar\alpha=(\alpha_H+\alpha_L)/2$.
The coordinator matched the six-digit display 0.522757 instead. The two versions differ by at most $4.9\times10^{-7}$ in $\beta$, $\lambda$ and $b$.
No displayed number in this memo changes between them.

**Equilibrium concept.** Perfect Bayesian equilibrium of the finite order game. A unilateral deviation faces fixed price and preparation schedules.
The informed payoff conditions on an informed arrival (T2 §2.4).

**Belief rule.** For $0<\beta<1/2$ and $0<\lambda<1$, every flow has positive liquidity mass in each class. Bayes' rule applies everywhere.
No result in this memo needs an off-path belief.

**Tie rules.**

- Investor: IM (any mixture at indifference, default) and I0 (zero at indifference).
- Challenger: C1 (prepare at indifference, the paper's rule, default) and CM (any mixture at indifference).

**Evidence.** Calibration A uses `fractions.Fraction` throughout. Calibration B uses `mpmath` at 40 significant digits.
For B, I report a sign only when the printed value exceeds $10^{-30}$ in absolute value; every reported margin exceeds $10^{-6}$.
The auction objects of paper eq. (4) agree exactly with a direct integration over $R$ at $r\in\{1.1,1.2,2.3,3,3.6\}$ (`common.py`, output `common_results.txt`).

## 3. Results

### 3.1 X1: the fixed-information control

**(a) Does the statement depend on the trading stage?**
Proposition A.3 does not. Its proof uses only a fixed joint law of signal and class, a cost independent of both, and Proposition 1(a).
The slot under frozen full orders is such an experiment: the laws of $Q$ given the class depend on $(\lambda,\beta)$ only, not on $r$.
The *size* of the effect depends on the stage.
The Laplace posterior has a continuous part on $(m,M)$. A rising threshold $\tau(r)$ then removes entry mass at every strength.
The slot posterior has three atoms $\{m(\pi),\pi,M(\pi)\}$. Entry changes only when $\tau(r)$ crosses an atom.

**(b) Slot statement and proof.**

**Result X1.1 (analytical).** Freeze full orders $(q_H,q_L)=(1,-1)$, atomic costs $\{0,c_H\}$, and rule C1. Then

$$
\mathsf E_{\rm frozen}(r)=\rho+(1-\rho)\sum_{x\in\{-1,0,1\}}\Pr(Q=x)\,\mathbf 1\{\mu_x\ge\tau(r)\},
\qquad \mu_1=M(\pi),\ \mu_0=\pi,\ \mu_{-1}=m(\pi).
$$

In the benchmark, $\tau(r)=(48r-3)/[4(20r-r^2-1)]$. Its derivative has numerator $4(48r^2-6r+12)>0$, so $\tau$ rises, from $\tau(1^+)=5/8$.
Hence $\tau(r)>1/2$ at every $r>1$, and only the top atom can recruit. So

$$
\mathsf E_{\rm frozen}(r)=\rho+(1-\rho)(b+\lambda/2)\ \text{ for } 1<r\le r_C(M),\qquad
\mathsf E_{\rm frozen}(r)=\rho\ \text{ for } r>r_C(M).
$$

*Proof.* With frozen orders, $\Pr(Q=x)$ and $\mu_x$ do not depend on $r$. The challenger prepares at cost $c_H$ exactly when $B_r(\mu_x)\ge c_H$, that is $\mu_x\ge\tau(r)$.
The zero-cost type always prepares, since $B_r(\mu)\ge g_L>0$. Sum over the three flows.
At $\pi=1/2$, $\Pr(Q=1)=b+\lambda/2$. Monotone $\tau$ gives one step, at $\tau(r)=M$. $\square$

The strictness set of Proposition A.3, $\{B_{r_1}(\mu(Q))<C\le B_{r_0}(\mu(Q))\}$, has these probabilities (`x1_results.txt`):

| Comparison | Calibration A | Calibration B |
|---|---|---|
| $r_0=1.2\to r_1=3$ | $0$ | $0$ |
| $r_1=3\to r_2=3.6$ | $5/17$ | $0.272757297$ |

The first comparison has zero probability because $\tau(1.2)=195/308$ and $\tau(3)=141/200$ both lie between the atoms $1/2$ and $M$.
Both are below $29/40$ and below $e/(1+e)$, so the top atom recruits at both strengths.

**(c) The paper's control recomputed.** Frozen full orders, prior $1/2$, atomic costs:

| | Entry at 1.2 | Entry at 3 | $\mathsf O_H$ at 1.2 | $\mathsf O_H$ at 3 | $\mathcal R_T$ at 1.2 | $\mathcal R_T$ at 3 |
|---|---|---|---|---|---|---|
| Paper, Laplace (recomputed here) | 0.562178 | 0.522757 | 0.350606 | 0.324192 | — | — |
| Slot A | $37/68=0.544118$ | $37/68$ | $23/68=0.338235$ | $23/68$ | $2789/5440=0.512684$ | $485/544=0.891544$ |
| Slot B | 0.522757 | 0.522757 | 0.324402 | 0.324402 | 0.503998 | 0.872531 |

My Laplace cross-check reproduces the paper's four control values to six decimals. It confirms that I read eq. (12) correctly.
As in the paper, the frozen profile is an equilibrium only in the strong economy.
At $r=1.2$, a full class-$H$ buy nets $\Delta_T(1-M)-k=-37/2400$ (A) and $-0.015518$ (B); a full class-$L$ sale also loses.
Under the slot, entry and high-class ownership are flat from 1.2 to 3. Proceeds rise, because the spread rises.

With the declared atomless cost law (Section 3.2), the slot control is still flat from 1.2 to 3: $B_r(M)>c_H+\varepsilon_C=6.1$ at both strengths.

**Where the slot does show deterrence at fixed information.** From $r_1=3$ to $r_2=3.6$ the equilibrium orders are full in both economies (Prop. 2(iii)).
That comparison is a fixed experiment, and entry falls: $37/68\to1/4$ (A) and $0.522757\to0.25$ (B).
So the slot gives a deterrence comparison in which the frozen profile is an equilibrium at both strengths. The Laplace control lacks this property.

**(d) Verdict: holds with change.**

- Proposition A.3 holds without change. It is a statement about any fixed experiment.
- Three sentences fail as written, because entry is flat, not falling, at $(r_0,r_1)=(1.2,3)$:
  - abstract (`main.tex` line 141): "If the information in the price is held fixed, stronger competition lowers participation";
  - introduction (lines 202–204): "If the investor's orders are held fixed ... preparation falls";
  - Section 4.2 (lines 977–979) and Table 2, Panel B: "entry falls from 0.562178 to 0.522757".
- A slot version that is true: "If the investor's orders are held fixed at their informative level, stronger competition never raises preparation.
  From $r_0$ to $r_1$ preparation stays at 0.522757. From $r_1$ to $r_2$, where the same orders are the equilibrium, it falls to 0.25."
- The identification argument of Section 4.2 survives. The control still shows that the rise needs a change in information.
  It no longer shows a direct deterrence effect between $r_0$ and $r_1$; that effect is zero there under the slot.

**(e) Status.** Result X1.1: analytical. Table values: computer-assisted (exact for A; 40 digits for B).

### 3.2 X3: atomless preparation costs

**(a) Does the statement depend on the trading stage?**
Partly. The entry rule $e(\mu)=H_C(B_F(\mu))$, the floor argument and the ownership identity do not use the stage.
Two parts do:

- The trading bound. Laplace uses the convolution bound with the factor $(1-1/b)$. The slot needs no factor, because a unit order reaches a known flow.
- The entry level. Laplace posteriors fill $[m,M]$, so some posterior mass falls inside the cost band and entry changes (0.522757 to 0.522715).
  Slot posteriors are three atoms. Under the support conditions, no atom falls inside the band, so entry does not change at all.

**(b) Slot statement and proof.**

**Result X3.1 (slot version of Prop. A.6; analytical).**
Keep the class assumptions of Proposition 2 (general $G_j$, prior $\pi$). Use the slot with $0<\lambda<1$ and $0<\beta\le1/3$.
Let $H_C=\rho H^0+(1-\rho)H^1$ with atomless components supported within $[0,2\varepsilon_C]$ and $[c_H-\varepsilon_C,c_H+\varepsilon_C]$. Suppose

$$
\Delta_T(F_0)<k<\rho\,\kappa(\pi)\,\Delta_T(F_1),\qquad \kappa(\pi)=\min\{m(\pi),1-M(\pi)\},
\tag{S-A2}
$$

$$
2\varepsilon_C<B_{F_1}(m(\pi)),\qquad B_{F_0}(\pi)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{F_1}(M(\pi)).
\tag{S-A24}
$$

Then:

1. At $F_0$ the unique informed orders are zero, and entry is $\rho$.
2. At $F_1$ the unique informed orders are $(q_H,q_L)=(1,-1)$. Entry is
   $\mathsf E_1=\rho+(1-\rho)(\pi\lambda+b)>\rho$, with $e_H=\rho+(1-\rho)(\lambda+b)$.
3. High-class ownership rises exactly when $e_HW_H(F_1)>\rho W_H(F_0)$. This holds when $W_H=1$ in both economies.
4. $\mathsf E_1$, $e_H$ and $e_L$ equal their atomic-cost values exactly.

*Proof.*

1. *Entry rule and price.* The challenger prepares when $C\le B_F(\mu)$, so $e(\mu)=H_C(B_F(\mu))$. It is continuous and nondecreasing, because $g_H\ge g_L$.
   The price $P(\mu)=t_0+e(\mu)(w_L+\Delta_T\mu)$ is then strictly increasing whenever $e\ge\rho$. So the price reveals the flow posterior.
2. *Floor.* With $\beta\le1/3$, every posterior at every flow, under every strategy, lies in $[m(\pi),M(\pi)]$ (Section 2).
   Gross profit falls in strength (Prop. 1(a)), so $B_F(\mu)\ge B_{F_1}(m(\pi))>2\varepsilon_C$ in both economies.
   Hence $H^0=1$ and $e\ge\rho$ at every flow.
3. *Weak economy.* A unit order has gross residual at most $e\,\Delta_T\le\Delta_T(F_0)<k$. Every nonzero order loses. Zero is the unique order.
   All posteriors equal $\pi$. Since $B_{F_0}(\pi)<c_H-\varepsilon_C$, $H^1=0$ and entry is $\rho$.
4. *Strong economy.* A class-$H$ buy reaches $Q=1$ with certainty. Its gross residual is $e(\mu_1)\Delta_T(1-\mu_1)\ge\rho\Delta_T(F_1)(1-M(\pi))>k$.
   A class-$L$ sale reaches $Q=-1$. Its residual is $e(\mu_{-1})\Delta_T\mu_{-1}\ge\rho\Delta_T(F_1)m(\pi)>k$.
   A wrong-signed order has a negative gross residual. So every candidate, mixed or not, has $q_H=1$ and $q_L=-1$ with probability one.
5. *Entry at $F_1$.* The posteriors are $M(\pi)$, $\pi$, $m(\pi)$ at $Q=1,0,-1$.
   $B_{F_1}(M(\pi))>c_H+\varepsilon_C$ gives $H^1=1$ at $Q=1$.
   $B_{F_1}(m(\pi))<B_{F_1}(\pi)\le B_{F_0}(\pi)<c_H-\varepsilon_C$ gives $H^1=0$ at $Q=0,-1$.
   So $e=1$ at $Q=1$ and $e=\rho$ elsewhere, which is the atomic-cost entry rule at these three posteriors.
   With $\Pr(Q=1\mid H)=b+\lambda$ and $\Pr(Q=1\mid L)=b$, the stated $\mathsf E_1$ and $e_H$ follow.
6. *Ownership.* Given its class and preparation, the challenger's value is independent of the price.
   So ownership is $\pi\rho W_H(F_0)$ at $F_0$ and $\pi e_HW_H(F_1)$ at $F_1$. Since $e_H>\rho$, $W_H=1$ gives the rise. $\square$

The tie rules C1 and CM give the same result, because $H_C$ has no atom.
If $1/3<\beta<1/2$, replace $m(\pi)$ in the first condition of (S-A24) by $\pi/(\pi+(1-\pi)(1+\lambda/c))$, the zero-flow lower bound.

**Result X3.2 (the ramp that replaces the ceiling jump; analytical).**
Keep the slot and full orders on a strength interval where (S-A2)'s right inequality, the floor $2\varepsilon_C<B_r(m(\pi))$, and $B_r(\pi)<c_H-\varepsilon_C$ hold. Then

$$
\mathsf E(r)=\rho+(1-\rho)\Pr(Q=1)\,H^1\big(B_r(M(\pi))\big),
$$

which is continuous and nonincreasing in $r$. With atomic costs, entry jumps from $\mathsf E_1$ to $\rho$ at $r_C$.
With a uniform $H^1$, entry instead falls linearly in $B_r(M)$, from $\mathsf E_1$ where $B_r(M)=c_H+\varepsilon_C$ to $\rho$ where $B_r(M)=c_H-\varepsilon_C$.
*Proof.* Step 5 above, with $H^1$ evaluated at the top atom only. $B_r(M)$ falls strictly in $r$. $\square$

This is where "entry becomes a smooth function of the posterior" shows up under the slot: in strength, near the ceiling, not at $r_1$.

**(c) The paper's declared example recomputed** ($\varepsilon_C=0.1$, low support $[0,0.2]$, benchmark vector, `x3_results.txt`):

| | $\mathsf E$ weak | $\mathsf E$ strong | $\Delta\mathsf E$ (pp) | $\mathsf O_H$ weak | $\mathsf O_H$ strong |
|---|---|---|---|---|---|
| Paper, Laplace, cost mixture (recomputed here) | 0.250000 | 0.522715 | 27.27 | 0.125000 | 0.324148 |
| Slot A, cost mixture | $1/4$ | $37/68=0.544118$ | 29.41 | $1/8$ | $23/68=0.338235$ |
| Slot B, cost mixture | 0.250000 | 0.522757 | 27.28 | 0.125000 | 0.324402 |

Under B, slot entry with the cost mixture equals the Laplace entry with cost atoms, to 40 digits. This follows from Result X3.1, item 4, and the definition of B.
An independent integration of the preparation probability over each uniform cost component agrees to $6\times10^{-41}$.

The five margins of (S-A2) and (S-A24) are all strictly positive:

| Margin | Slot A | Slot B | Paper (Laplace, B-equivalent $M$) |
|---|---|---|---|
| $\zeta_L=B_3(m)-2\varepsilon_C$ | $133/60=2.216667$ | 2.166179 | 2.166179 |
| $\zeta_{H0}=c_H-\varepsilon_C-B_{1.2}(1/2)$ | $263/240=1.095833$ | 1.095833 | 1.095833 |
| $\zeta_{H1}=B_3(M)-c_H-\varepsilon_C$ | $1/15=0.066667$ | 0.117155 | 0.117155 |
| $\zeta_0=k-\Delta_T(1.2)$ | $1/300$ | $1/300$ | $1/300$ |
| $\zeta_1$ (trading bound at 3) | $31/1200=0.025833$ | 0.024824 | 0.002412 (with $1-1/b$) |

The slot's strong trading margin is about ten times the Laplace margin. The factor $1-1/b=1/2$ is absent.

Direct investor payoffs confirm the orders. At $r=3$ under A, a class-$H$ buy nets $49/300$ and a class-$L$ sale nets $31/1200$.
At $r=1.2$, the best nonzero order nets $-43/2400$.

**Part (iii) with the declared law (an observation, not a claim of the paper).**
Proposition A.6 covers parts (i) and (ii) only. Part (iii) with atomless costs would need $c_H-\varepsilon_C>B_{3.6}(M)$.
This margin is $-349/7200$ (A) and $-0.097311$ (B), so it fails at both calibrations. Result X3.2 gives the ramp:

| | Ramp in $r$ ($B_r(M)$ from 6.1 to 5.9) | $\mathsf E$ at 3.6 | $\mathsf O_H$ at 3.6 |
|---|---|---|---|
| Slot A | $[3.183246, 3.733374]$ | $1573/4896=0.321283$ | $0.176680$ |
| Slot B | $[3.319676, 3.865725]$ | 0.382712 | 0.222020 |
| Laplace, cost mixture (my quadrature) | — | 0.376680 | 0.217603 |

The paper's own Laplace model has the same feature. Its posterior reaches $M$ on the plateau $x\ge1$, where $B_{3.6}(M)=5.9973$ lies inside the cost band.
So this is not a slot-specific problem. Part (iii) with these atomless costs needs $\varepsilon_C<6-B_{3.6}(M)$: that is $\varepsilon_C<0.002689$ under B and Laplace, or $\varepsilon_C<371/7200=0.051528$ under A.

**(d) Verdict: holds.** Proposition A.6, with the slot in place of Laplace or logistic noise, is true and proved above.
Its content becomes sharper: inside (S-A24) the atomless law changes no outcome at all. Two text items change:

- Section 5.1, "strong-incumbent entry is 0.522715 under Laplace noise and 0.301374 under logistic noise": becomes 0.522757 (B) or 37/68 (A). The logistic rows have no slot counterpart.
- Section 5.1, "Its preparation therefore occurs only after sufficiently favorable prices": under the slot, only after a buy order.

**(e) Status.** Results X3.1 and X3.2: analytical. Slot table values: computer-assisted (exact for A; 40 digits for B).
The Laplace quadrature values in the last table: numerical diagnostic (adaptive quadrature at 40 digits, not interval-certified).

### 3.3 X4: complementary private signals

**Model.** The paper's Appendix A.5 with the slot as the trading stage. Prior $\pi=1/2$, point-mass classes.
The investor sees $T\in\{+,-\}$ with accuracy $a$ and, when informed, chooses $q(T)\in\{-1,0,1\}$ (mixtures allowed).
The challenger sees $Y$ with accuracy $d$, its cost, and the price. $T$ and $Y$ are independent given the class.
The identity draw and the liquidity order are independent of $(J,T,Y,C)$.

**(a) Does the statement depend on the trading stage?**
Most of the argument does not:

- $J\perp Q\mid T$ and $Y\perp Q\mid J$ hold for the slot. So (A.27), (A.30) and (A.31) hold with $\lambda_Q=\Pr(T=+\mid Q)$.
- The entry rates (A.28), loading bounds (A.32)–(A.33), inversion (A.34) and residuals (A.35) need only these two relations and the cost floor.

Two parts depend on the stage:

- The strong trading bound. Laplace uses the convolution bound $U'(s)\ge(1-1/b)m(2a-1)\rho\Delta_T-k$. Under the slot, a unit order reaches one known flow. The bound is the residual bound itself, without $1-1/b$.
- The entry closed forms (OA.39)–(OA.41) are Laplace tail probabilities. Under the slot they become sums over three flows.

**(b) Slot statement and proof.**

**Result X4.1 (slot version of Prop. A.7; analytical).** Use the slot with $0<\lambda<1$, $0<\beta<1/2$, and $\pi=1/2$.
Put $M=(1+u)/(2+u)$, $m=1-M$, $\mu_\pm=(1-a)+(2a-1)\{M,m\}$. Choose $0<p<\ell<r_0<r_1<h$ and suppose

$$
B_{r_0}(d)<c_H<B_{r_1}(\phi_+(\mu_+)),
\tag{S-A29a}
$$

$$
(2a-1)\{\Delta_T(r_0)+(1-\rho)(2d-1)w_H(r_0)\}<k<(2a-1)\,\rho\, m\,\Delta_T(r_1).
\tag{S-A29b}
$$

Then the weak economy has unique zero informed orders and entry $\rho$.
The strong economy has unique orders $q(+)=1$, $q(-)=-1$, and entry strictly above $\rho$.
The conclusions allow arbitrary mixed signal-contingent orders and either challenger tie rule. They do not need $a\ge d$.
At full orders, $\Pr(Q=1\mid H)=b+a\lambda$, $\Pr(Q=1\mid L)=b+(1-a)\lambda$, $\Pr(Q=0\mid j)=c$, and $\Pr(Q=-1\mid H)=b+(1-a)\lambda$, $\Pr(Q=-1\mid L)=b+a\lambda$.
If only $(Q=1,Y=+)$ recruits, as in the declared example, then

$$
e_H=\rho+(1-\rho)\,d\,(b+a\lambda),\qquad e_L=\rho+(1-\rho)(1-d)(b+(1-a)\lambda),\qquad \mathsf E=(e_H+e_L)/2,\quad \mathsf O_H=e_H/2.
$$

*Proof.*

1. *Beliefs.* Flow depends on the class only through $T$, so $\mu_Q=(1-a)+(2a-1)\lambda_Q$.
   $Y$ is independent of $Q$ given the class, so $\Pr(H\mid P,Y=y)=\phi_y(\mu_P)$.
   At $Q=\pm1$, the likelihood ratio of $T$ lies in $[1/(1+u),1+u]$ under every strategy. With $\Pr(T=+)=1/2$, $\lambda_Q\in[m,M]$ there.
2. *Floor and price.* Gross profit is at least $g_L>0$ at every belief, so the zero-cost type prepares after every price and signal.
   Hence $e_H\ge e_L\ge\rho$ and $\Delta_P=e_L\Delta_T+(e_H-e_L)w_H\ge\rho\Delta_T>0$.
   The price $P(\mu)$ of (OA.35) is strictly increasing by (OA.36). So the price reveals $\mu_Q$.
3. *Residuals.* As in (A.35): $A_+=(2a-1)(1-\lambda_Q)\Delta_P$ for a buy after $T=+$, and $A_-=(2a-1)\lambda_Q\Delta_P$ for a sale after $T=-$.
   Each is at most $A^+=(2a-1)\{\Delta_T+(1-\rho)(2d-1)w_H\}$.
4. *Weak economy.* A buy after $T=+$ reaches $Q=1$ and nets $A_+(1)-k\le A^+(r_0)-k<0$. A sale after $T=-$ is the same.
   Wrong-signed orders have negative gross residuals. So zero is the unique order.
   The public posterior is $1/2$ at every flow. The favorable joint posterior is $\phi_+(1/2)=d$, and $B_{r_0}(d)<c_H$. Entry is $\rho$.
5. *Strong economy.* A buy after $T=+$ reaches $Q=1$ with certainty. There $1-\lambda_1\ge1-M=m$, so $A_+(1)\ge(2a-1)m\rho\Delta_T(r_1)>k$.
   A sale after $T=-$ reaches $Q=-1$, where $\lambda_{-1}\ge m$, so $A_-(-1)>k$ too.
   So every candidate has $q(+)=1$ and $q(-)=-1$ with probability one. Then $\lambda_1=M$ and $\mu_1=\mu_+$.
   The right inequality of (S-A29a) gives $I_+(1)=1$. Since $\Pr(Q=1,Y=+\mid j)>0$ in both classes, entry exceeds $\rho$.
   The argument never compares $a$ with $d$. $\square$

**(c) The paper's example recomputed** (declared vector: $\rho=0.85$, $c_H=7.14$, $k=0.015$, $r_0=1.1$, $r_1=2.3$, $a=0.70$, $d=0.75$; `x4_results.txt`):

| | $\mathsf E$ weak | $\mathsf E$ strong | $\Delta\mathsf E$ (pp) | $\mathsf O_H$ weak | $\mathsf O_H$ strong |
|---|---|---|---|---|---|
| Paper, Laplace (recomputed here) | 0.850000 | 0.879438 | 2.94 | 0.425000 | 0.448942 |
| Slot A | $17/20$ | $2999/3400=0.882059$ | 3.21 | $17/40$ | $3067/6800=0.451029$ |
| Slot B | 0.850000 | 0.879797 | 2.98 | 0.425000 | 0.449238 |

At $r_1$ only the pair $(Q=1,Y=+)$ recruits: $\phi_+(\mu_+)=177/218=0.811927$ (A) and 0.813453 (B) exceed $\tau(2.3)=16047/19855=0.808210$.
$\phi_-(\mu_+)$ is about 0.32, and $\phi_+(1/2)=d=0.75$ is below $\tau$.
So "a favorable private signal alone does not justify high-cost preparation; combined with a favorable price, it does" holds as stated.

The margins of (S-A29a)–(S-A29b) and the low-cost diagnostic:

| Margin | Slot A | Slot B | Paper (Laplace) |
|---|---|---|---|
| Private-only exclusion $c_H-B_{1.1}(d)$ | $21/400=0.0525$ | 0.0525 | 0.0525 |
| Joint entry $B_{2.3}(\phi_+(\mu_+))-c_H$ | $16089/501400=0.032088$ | 0.045265 | 0.045265 |
| Weak order | $2/1375=0.001455$ | 0.001455 | 0.001455 |
| Strong order | $17803/920000=0.019351$ | 0.018594 | 0.001797 (with $1-1/b$) |
| Low-cost diagnostic $B_{2.3}(\phi_-(\mu_-))$ | 1.786607 | 1.773430 | 1.773430 |

The binding margin is the weak-order margin, as in the paper. The strong-order margin is about ten times larger under the slot.

**The declared example has $d=0.75>a=0.70$.** All four slot conditions hold, so the reversal with a buyer signal more accurate than the investor's holds under the slot.

**The accuracy grid of Online Appendix C.3** (25 pairs, both strengths, both calibrations):

- My Laplace closed forms reproduce all 25 of the paper's strong-entry values to six decimals.
- Under the slot, every pair has exactly one C1/IM equilibrium at each strength, and no extra CM threshold mixture.
  Weak orders are zero; strong orders are full by signal. A brute-force sum over $(J,T,\text{identity},Q,Y,C)$ confirms each one:
  best-response gains are zero, prices match to $10^{-40}$ (B) or exactly (A), and price inversion recovers the posterior.
- Under B, the slot conditions hold at exactly the paper's six pairs: $(0.69,0.75)$, $(0.70,0.75)$, $(0.71,0.74)$, $(0.71,0.75)$, $(0.72,0.74)$, $(0.72,0.75)$.
  All six have $d>a$. Entry rises in each, from 0.85 to between 0.879671 and 0.880049.
- Under A, the conditions hold at five pairs. At $(0.71,0.74)$, $\phi_+(\mu_+)<\tau(2.3)$ because $M_A=0.725<M_B$: the joint-entry margin is $-0.0132$, and entry stays at 0.85.
- In the ten pairs with $d\ge0.76$, the favorable private signal alone recruits in the weak economy, so entry falls (0.925 to about 0.880). The paper's grid shows the same pattern.

The full slot grid is in `x4_results.txt`. Entry under B at the met pairs:

| $(a,d)$ | Slot B: $\mathsf E$ strong | Paper (Laplace) | Slot B minimum margin | Paper minimum margin |
|---|---|---|---|---|
| $(0.69,0.75)$ | 0.879671 | 0.878570 | $2.13\times10^{-3}$ | $9.57\times10^{-4}$ |
| $(0.70,0.75)$ | 0.879797 | 0.879438 | $1.45\times10^{-3}$ | $1.45\times10^{-3}$ |
| $(0.71,0.74)$ | 0.879817 | 0.878066 | $9.59\times10^{-4}$ | $9.59\times10^{-4}$ |
| $(0.71,0.75)$ | 0.879923 | 0.880215 | $7.77\times10^{-4}$ | $7.77\times10^{-4}$ |
| $(0.72,0.74)$ | 0.879938 | 0.878915 | $6.16\times10^{-4}$ | $6.16\times10^{-4}$ |
| $(0.72,0.75)$ | 0.880049 | 0.880919 | $1.00\times10^{-4}$ | $1.00\times10^{-4}$ |

At $(0.69,0.75)$ the paper's binding margin is its strong-order margin, which the slot relaxes.

**(d) Verdict: holds.** Proposition A.7 with the slot is true and proved above. Its strong trading condition is weaker (no factor $1-1/b$).
The numbers change: Table 3, Panel C becomes $0.850000\to0.879797$ with $\mathsf O_H$ $0.425000\to0.449238$ (B). The C.3 grid values change slightly; its pattern does not.

**(e) Status.** Result X4.1: analytical. Example and grid under A: computer-assisted (exact). Under B: computer-assisted (40 digits).
The smallest positive margin on the grid is the weak-order margin at $(0.72,0.75)$. It is exactly $1/10000$ and has no slot parameter, so it is the same under A and B.
Every other reported margin exceeds $6\times10^{-4}$ in absolute value.

### 3.4 The general-prior coexistence formulas

The ledger note (22 Oct, coordinator, not yet checked) states three formulas for the slot at a general prior $\pi$:

- (N) no trade is an equilibrium iff $\rho\Delta_T\max\{\pi,1-\pi\}\le k$;
- (A) $r_A$ solves $\Delta_T(1-\tau)=k$ for every prior;
- (E) on the interior branch, $\mathsf E=\rho+(1-\rho)(1-\pi)b\Delta_T/k$.

**Setting.** The slot with the benchmark auction, atomic costs, investor rule IM, challenger rule C1, prior $\pi\in(0,1)$.

**(a) Stage dependence.** These formulas are slot formulas. The Laplace counterparts differ (paper Prop. 3 and Appendix A.3). The question is only whether they are right for the slot.

**(b) Derivation (analytical).**

*Step 0: the two order problems separate.* Let $s=\lambda\Pr(q=1\mid H)$ and $t=\lambda\Pr(q=-1\mid L)$.
Wrong-signed orders have negative gross residuals and are never used. A buy reaches $Q=1$ and a sale reaches $Q=-1$. So

$$
K_H(s)=e(\mu_1)\Delta_T(1-\mu_1),\quad 1-\mu_1(s)=\frac{(1-\pi)b}{b+\pi s};\qquad
K_L(t)=e(\mu_{-1})\Delta_T\mu_{-1},\quad \mu_{-1}(t)=\frac{\pi b}{b+(1-\pi)t}.
$$

*(N).* At $s=t=0$ every posterior equals $\pi$. If $\pi<\tau(r)$, entry is $\rho$ at every flow.
A deviating buy earns $\rho\Delta_T(1-\pi)$ and a deviating sale earns $\rho\Delta_T\pi$. No trade is an equilibrium iff both are at most $k$.
That is (N), under IM and I0 alike. If $\pi\ge\tau(r)$, entry at the prior is one and $\rho$ in (N) becomes 1.
In the benchmark $\tau(r)>5/8$, so (N) holds as stated for every $\pi\le5/8$. Equivalently, $r\le r_N(\pi)=\mathfrak r\big(k/(\rho\max\{\pi,1-\pi\})\big)$, with $\mathfrak r(D)=1+D+\sqrt{D^2+2D}$.

*(A).* Take $r\le r_N(\pi)$ and $\pi<\tau(r)$.

1. The low class never sells. $\mu_{-1}(t)\le\pi<\tau$ gives $e=\rho$, so $K_L(t)\le\rho\Delta_T\pi\le k$, with strict inequality for $t>0$.
2. Without recruitment, a class-$H$ buy earns $\rho\Delta_T(1-\mu_1)<\rho\Delta_T(1-\pi)\le k$ for $s>0$. So an informative outcome needs $\mu_1(s)\ge\tau$.
3. Recruitment starts at $s^*=b(\tau-\pi)/[\pi(1-\tau)]$. It is reachable iff $s^*\le\lambda$, that is $\tau(r)\le M(\pi)$.
4. On the recruiting piece $K_H$ falls in $s$. At $s^*$, $b+\pi s^*=b(1-\pi)/(1-\tau)$, so $K_H(s^*)=\Delta_T(1-\tau)$.
5. Hence an informative equilibrium exists iff $\tau(r)\le M(\pi)$ and $J(r):=\Delta_T(r)(1-\tau(r))\ge k$. This holds under C1; under CM the threshold mixture needs the same inequality.

$J$ does not involve $\pi$. It rises on $[6/5,7/4]$ (T2 §3.6; X_check §3.5), and $r_N(\pi)\le r_N(1/2)<7/4$ for every prior.
So the lower end is the root $r_A\in[1.3939579202792,1.3939579202793]$ of $J=k$, for every prior with $\pi<\tau(r_A)\le M(\pi)$.
If $M(\pi)<\tau(r_A)$, then $r_C(M(\pi))<r_A$, and no informative equilibrium coexists with no trade.
With $\tau(r_A)=0.640739$, the condition $M(\pi)\ge\tau(r_A)$ means $\pi\ge\pi_{\rm lo}=\tau_A/[(1+u)(1-\tau_A)+\tau_A]$:
$\pi_{\rm lo}=0.403518$ (A) and $0.396175$ (B). Also $r_A<r_N(\pi)$ at every prior, since $\rho\Delta_T(r_A)\le0.0139<k$.

*(E).* On the recruiting interior branch, $K_H(s)=k$ gives $b+\pi s=(1-\pi)b\Delta_T/k$. This is $\Pr(Q=1)=\pi(b+s)+(1-\pi)b$.
Entry is one at $Q=1$. At $Q=0$, $\mu_0<\pi<\tau$; at $Q=-1$, $\mu_{-1}=\pi<\tau$. So entry is $\rho$ there, and

$$
\mathsf E=\rho+(1-\rho)\Pr(Q=1)=\rho+(1-\rho)(1-\pi)\,b\,\Delta_T/k .
$$

The branch needs $s^*<s<\lambda$. That is $r_A<r<r_F(\pi)$, where $\Delta_T(r_F)(1-M(\pi))=k$, so $r_F(\pi)=\mathfrak r\big(k/(1-M(\pi))\big)$.
At $\pi=1/2$ this is T2 eq. (34). Under I0 the branch does not exist. Coexistence then needs full orders: $r_F(\pi)<r\le r_N(\pi)$.

**(c) Computer check** (`coexistence_results.txt`). I classified every C1/IM equilibrium on the grid $r=1.200,1.205,\ldots,1.900$ (141 points).
The classifier enumerates zero, full, every interior root on each entry piece, and every CM threshold mixture (`slot_solver.py`).

| Calibration, prior | $r_N(\pi)$ | $r_F(\pi)$ | No-trade set: mismatches with (N) | Coexistence set found | Mismatches | Grid points on the branch of (E) | Max error of (E) |
|---|---|---|---|---|---|---|---|
| A, $1/2$ | 1.747878 | 1.460985 | 0 | $[1.395,1.745]$ | 0 | 14 | 0 |
| A, $12/25$ | 1.729486 | 1.445578 | 0 | $[1.395,1.725]$ | 0 | 11 | 0 |
| A, $51/100$ | 1.738525 | 1.469044 | 0 | $[1.395,1.735]$ | 0 | 15 | 0 |
| A, $3/5$ | 1.666667 | 1.555162 | 0 | $[1.395,1.665]$ | 0 | 33 | 0 |
| A, $2/5$ | 1.666667 | (not reached) | 0 | empty | 0 | 0 | — |
| B, $1/2$ | 1.747878 | 1.467127 | 0 | $[1.395,1.745]$ | 0 | 15 | $1\times10^{-41}$ |
| B, $0.48$ | 1.729486 | 1.451357 | 0 | $[1.395,1.725]$ | 0 | 12 | $1\times10^{-41}$ |
| B, $0.52$ | 1.729486 | 1.483886 | 0 | $[1.395,1.725]$ | 0 | 18 | $1\times10^{-41}$ |

"Mismatches" compares the computed set with the set predicted by Steps (N) and (A), point by point. Errors for A are exact zeros.
At $\pi=2/5$, $M(2/5)=58/91=0.637<\tau(r_A)$. No trade holds up to $r_N=5/3$, but no informative equilibrium exists below it.
The informative equilibria there start at $r=1.67$, with mixed buys and no recruitment.
The grid also reproduces the two interior entries of X_check at $\pi=1/2$: $229/476=0.481092$ at 1.40 and $8399/15776=0.532391$ at 1.45.

**(d) Verdict: holds with change.** All three formulas are right, but each needs its domain:

- (N) needs $\pi<\tau(r)$; otherwise replace $\rho$ by 1. At the benchmark this holds for every $\pi\le5/8$.
- (A) is false "for every prior". It holds for $\pi_{\rm lo}<\pi<\tau(r_A)$: $(0.403518,0.640739)$ under A and $(0.396175,0.640739)$ under B.
  Below $\pi_{\rm lo}$, coexistence is empty.
- (E) holds on $r_A<r<r_F(\pi)$ with $r_F(\pi)=\mathfrak r(k/(1-M(\pi)))$, under IM.

**(e) Status.** Derivation: analytical. Grid check: computer-assisted (exact for A; 40 digits for B). The grid only tests the derivation; the proof does not rest on it.

## 4. Scorecard

The brief's report items (a)–(e) for each extension. Full derivations are in Section 3.

| Item | X1 fixed-information control | X3 atomless costs | X4 complementary signals | Ledger coexistence formulas |
|---|---|---|---|---|
| (a) Depends on the stage? | Prop. A.3: no. The size of the control's fall: yes (three posterior atoms). | Trading bound and entry level: yes. Entry rule and floor: no. | Belief algebra and pricing: no. Strong trading bound and entry closed forms: yes. | Slot formulas by construction. |
| (b) Slot statement | Result X1.1: frozen entry is a step function; flat on $(1,r_C(M)]$. | Result X3.1 (Prop. A.6 with (S-A2), (S-A24), $\beta\le1/3$); Result X3.2 (ramp near the ceiling). | Result X4.1 (Prop. A.7 with (S-A29a)–(S-A29b), no $1-1/b$). | (N), (A), (E) with domains. |
| (c) Example, B | Frozen entry 0.522757 at 1.2 and at 3 (paper: 0.562178 to 0.522757). | Entry $0.25\to0.522757$, $\mathsf O_H$ $0.125\to0.324402$ (paper: 0.522715, 0.324148). | Entry $0.85\to0.879797$, $\mathsf O_H$ $0.425\to0.449238$ (paper: 0.879438, 0.448942). Met set = paper's six pairs. | $r_A=1.393958$ at every tested prior with $\pi>\pi_{\rm lo}$; (E) exact. |
| (c) Example, A | Frozen entry $37/68$ at both. | $1/4\to37/68$, $\mathsf O_H$ $1/8\to23/68$. | $17/20\to2999/3400$, $\mathsf O_H$ $17/40\to3067/6800$. Met set loses $(0.71,0.74)$. | Same $r_A$; $\pi_{\rm lo}=0.403518$. |
| (d) Verdict | Holds with change: A.3 holds; "entry falls" (abstract, intro, Sec. 4.2, Table 2B) fails at $(1.2,3)$. | Holds. Text numbers change. | Holds. Text numbers change. | Holds with change: (A) fails "for every prior"; each formula needs its domain. |
| (e) Status | Analytical; numbers computer-assisted. | Analytical; numbers computer-assisted; Laplace quadrature numerical diagnostic. | Analytical; numbers computer-assisted. | Analytical; grid computer-assisted. |

**Tie rules and knife-edges.** No result needs an off-path belief on the unit menu.
X1 and X3 are strict at the benchmark under C1 and CM. X4 is strict at every met grid pair. The ledger formulas use IM; I0 removes the interior branch of (E).

## 5. Numerical examples

All numbers use the paper's declared vectors. A values are exact; B values are 40-digit computations shown to six decimals.

| Exercise | Quantity | Paper (Laplace) | Slot A | Slot B |
|---|---|---|---|---|
| X1 frozen control | Entry at 1.2 / 3 | 0.562178 / 0.522757 | $37/68$ / $37/68$ | 0.522757 / 0.522757 |
| X1 frozen control | $\mathsf O_H$ at 1.2 / 3 | 0.350606 / 0.324192 | $23/68$ / $23/68$ | 0.324402 / 0.324402 |
| X1 frozen control | Prop. A.3 strictness probability, 1.2→3 / 3→3.6 | positive / positive | $0$ / $5/17$ | $0$ / 0.272757 |
| X3 cost mixture | Entry weak / strong | 0.250000 / 0.522715 | $1/4$ / $37/68$ | 0.250000 / 0.522757 |
| X3 cost mixture | $\mathsf O_H$ weak / strong | 0.125000 / 0.324148 | $1/8$ / $23/68$ | 0.125000 / 0.324402 |
| X3 cost mixture | Entry at 3.6 (not claimed by A.6) | 0.376680 (my quadrature) | $1573/4896=0.321283$ | 0.382712 |
| X4 declared | Entry weak / strong | 0.850000 / 0.879438 | $17/20$ / $2999/3400=0.882059$ | 0.850000 / 0.879797 |
| X4 declared | $\mathsf O_H$ weak / strong | 0.425000 / 0.448942 | $17/40$ / $3067/6800=0.451029$ | 0.425000 / 0.449238 |
| X4 grid | Pairs meeting the sufficient conditions | 6 | 5 | 6 (same as paper) |
| Coexistence, $\pi=1/2$ | $r_A$, $r_F$, $r_N$ | — | 1.393958, 1.460985, 1.747878 | 1.393958, 1.467127, 1.747878 |

**Program use.** Run from the repository root:

```bash
S=audit/microstructure_search_2026_10_22/scripts
for f in common x1_fixed_information x3_atomless_costs x4_signals coexistence_general_prior; do
  bash $S/_slots/run_slot.sh .venv/bin/python $S/E2_information_side/$f.py
done
```

The saved outputs are `x1_results.txt`, `x3_results.txt`, `x4_results.txt` and `coexistence_results.txt`. Each run takes a few seconds.
I ran each program and examined its printed output. The scripts print values; they contain no assertions.

## 6. Open issues

- **open.** Continuous order sizes. The paper lets the investor deviate to any order in $[-1,1]$. Under the slot this needs EGJ's off-path belief (X_check §4, item 2). All results here use the unit menu.
- **open.** The logistic rows of Section 5.1 and Table 3 have no slot counterpart. Proposition A.5 is out of scope.
- **open.** X1: a strict frozen fall between $r_0$ and $r_1$ needs cost mass in $(B_{r_1}(M),B_{r_0}(M)]$, for example a wide atomless law. I did not search for such a calibration.
- **open.** X3 with $1/3<\beta<1/2$: the floor condition must use the zero-flow bound. Not computed.
- **open.** X3 in the coexistence region: with atomless costs the CM threshold mixture becomes a pure-strategy branch. Not analyzed.
- **open.** X4 at priors other than $1/2$. The paper also states A.7 only at $\pi=1/2$.
- **analytical.** X3 part (iii) with the declared atomless law fails at $r_2=3.6$ under both calibrations and under Laplace. The paper does not claim it.
- **analytical.** The ledger's general-prior formulas need the domains in Section 3.4. The sibling general-prior Prop. 2 ($\mathsf E_1$, $\mathsf O_H$) is workstream E1.

## 7. Plain summary

I checked three extensions and one ledger note with the order slot as the trading stage.
Calibration B matches the paper's posterior bound and its strong entry to 40 digits.

The fixed-information control (X1) changes. Proposition A.3 still holds, because it covers any fixed experiment.
But the slot posterior has only three values. Between strengths 1.2 and 3, the recruiting threshold stays below the top value.
So frozen full orders give flat entry, 0.522757 at both strengths, not a fall from 0.562178.
The abstract, the introduction, Section 4.2 and Table 2 say "falls" and must say "does not rise".
The slot shows a fixed-information fall from 3 to 3.6, where the same orders are the equilibrium.

Atomless costs (X3) hold. With the declared law, no slot posterior falls inside the cost band, so outcomes equal the atomic case exactly.
Strong entry is 0.522757, not 0.522715. Near the ceiling, atomless costs turn the entry jump into a ramp.
At 3.6 entry stays above the floor, in the slot and in the paper's Laplace model alike. The paper does not claim that part.

Complementary signals (X4) hold, including a buyer signal more accurate than the investor's.
The slot's trading condition is weaker, because it has no factor $1-1/b$.
The declared example gives entry 0.85 to 0.879797. The same six grid pairs meet the sufficient conditions as in the paper.

The ledger's coexistence formulas are right with domains.
The no-trade condition needs the prior below the recruiting threshold.
The lower end $r_A=1.393958$ holds only for priors from 0.396 (B) to 0.641. At prior 0.4 under A, coexistence is empty.
The interior-branch entry formula is exact between $r_A$ and $r_F(\pi)$.

No extension fails. X1 and the ledger formulas need changed statements.
