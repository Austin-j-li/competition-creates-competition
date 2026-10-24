# X_C3. Independent check of the delay option

## 1. Scope

This memo checks the eight claims in `C3_delay.md`.
The source paper is fixed at commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
Equation (4) of the pinned manuscript confirms all six shared auction formulas.
The check covers three-point noise and discrete-Laplace noise, with point-mass values and prior $1/2$.
It retains fresh investors, buy-only orders, investor presence one, and $c_L=0$.

The independent calculation uses exact fractions and 70-digit arithmetic.
It sums finite signal partitions, without a noise cutoff or a search grid.
The first derivation and its output preceded inspection of all three source programs.
The source programs then ran unchanged, with their output saved in this check's folder.

The source memo has SHA-256 `67abe6230996440f3e3d8fb1499c6be6dfd14fa1784aafbbad09aa3bfcdc9838`.
Source receipts and output differences appear in [comparison.txt](../scripts/X_C3_check/comparison.txt).
The independent derivation appears in [derive.py](../scripts/X_C3_check/derive.py) and [independent.txt](../scripts/X_C3_check/independent.txt).
The comparison appears in [comparison.py](../scripts/X_C3_check/comparison.py).

The verdicts concern the memo's canonical price schedules.
The uniqueness verdict does not cover a larger class of first-price pools.
They do not extend to public preparation decisions, a retained investor stake, or arbitrary cost distributions.
No source memo or source program changed.

## 2. Verdict table

| Claim | Verdict | Evidence and status |
|---|---|---|
| 1. Two-round prices and the $w_L$ residual term | **CONFIRMED WITH CORRECTION** | **Analytical.** The identities hold when the first preparation decision stays private. Public observation requires different prices. See Sections 3.1–3.2. |
| 2. Exact three-point wait region | **CONFIRMED WITH CORRECTION** | **Analytical.** The interior formula holds. The claimed interior root fails at $c_H=g_L$; the wait region is then empty. Section 3.3 gives complete cutoffs. |
| 3. C3.1: entry path and round-2 bottleneck | **CONFIRMED WITH CORRECTION** | **Analytical.** Entry is $1/4\to11/24\to1/4$, and the bottleneck is $k<\rho\Delta_T/3$. The late ceiling needs a strict endpoint. Absorbing histories have no on-path round-2 order. |
| 4. Discrete-Laplace discount thresholds | **CONFIRMED** | **Analytical**, in the stated region with no late entry at belief $1/2$. The threshold is $\delta^*(3)=0.898962886700027\ldots$. |
| 5. C3.2: entry falls; ceiling moves outward | **CONFIRMED** | **Analytical**, after the bounds in Section 3.6 replace the grids. Entry is $0.625\to0.448747215849$; ceilings are $3.986096571638$ and $5.605890889243$. |
| 6. Delay creates coexistence at the specified point | **CONFIRMED** | **Analytical**, after the exact inequalities in Section 3.7. Both outcomes satisfy strict investor incentives. |
| 7. Intermediate-strength delay and non-monotone timing | **CONFIRMED WITH CORRECTION** | **Analytical** for the benchmark examples. Define timing among actual preparations. A nonempty delay interval is a condition, not a general conclusion. |
| 8. No grading, coexistence, or early ceiling under three-point delay | **CONFIRMED WITH CORRECTION** | **Analytical** within C3.1's region. The claim does not cover every parameter choice. Round-1 feedback is positive; the round-2 bottleneck blocks coexistence. |

## 3. Derivations and evidence for each claim

### 3.1 Game form, sequential choices, and beliefs

**Status: analytical.** The calculation needs the following information sets.

- Each investor observes the class, but not the challenger cost.
- The second investor starts with zero shares and observes the first price.
- Market makers observe both flows by round 2.
- The challenger observes its cost and the price history.
- Preparation, its payment, delay, and exit remain private through round 2.
- The second round occurs after every first decision.

The last two conditions matter.
The memo gives prices conditional on flows alone, so private decisions are the natural interpretation.
It should state that interpretation directly.

The waiting cost is a discount on gross auction profit:

$$
N(u)=B_r(u)-c_H,
\qquad
W(u)=\mathbb E[(\delta B_r(v)-c_H)_+\mid u].
$$

It is neither a sale risk nor a discount on net profit.
Late auction utility is $\delta(\theta-\text{payment})$.
Since $\delta>0$, truthful bids remain optimal and the target receipts stay unchanged.
This is a coherent preference assumption, although the sale date stays fixed.

The equilibrium concept is perfect Bayesian equilibrium with competitive prices and the stated canonical schedules.
An investor deviation holds all price and continuation schedules fixed.
Private preparation also leaves the second investor's information unchanged after a challenger deviation.
Thus $N$ and $W$ compare actual deviations in this game.

The full choice rule is

$$
\begin{cases}
\text{now},&N(u)\ge0\text{ and }N(u)\ge W(u),\\
\text{wait},&W(u)>\max\{N(u),0\},\\
\text{exit},&\text{otherwise}.
\end{cases}
$$

Late preparation occurs when $\delta B_r(v)\ge c_H$, conditional on an earlier wait.
An indifferent investor submits zero.
These rules exclude an investor mixture at zero net profit.
The source's conventional mixtures therefore concern a different tie convention.

The low-cost challenger enters immediately.
Its immediate payoff is $B_r(u)>0$.
The posterior martingale gives a late value of $\delta B_r(u)<B_r(u)$.

For three-point noise, an unused upper flow receives posterior one.
This directional completion is an assumption, not a proof of a unique refinement.
The continuation respects prior commitments: exit still implies no expensive entry after a revealing second flow.
An early preparation remains effective after bad second news.

The continuation below covers every attainable first price and every unused upper flow.
At other unattainable first quotes, posterior zero and optimal continuation supply a belief completion.
Discrete-Laplace noise has full support, so every integer flow history uses Bayes' rule.
Neither example needs a free belief at an integer flow history.

**Public observation changes the game.** Let $A$ be the observed first decision.
Conditional on the first price, $A$ reveals cost or preparation status, not additional class information.
Cost is independent of class, and the challenger has no further class signal before preparation.
Yet $A$ changes the chance of eventual entry.
Round-2 prices must then condition on $A$:

$$
P_2(u,v,A)=t_0+e_A(v)(w_L+\Delta_Tv),
\qquad
e_A(v)=
\begin{cases}
1,&A=\text{now},\\
0,&A=\text{exit},\\
\mathbf1\{\delta B_r(v)\ge c_H\},&A=\text{wait}.
\end{cases}
$$

The floor $\rho$ disappears conditional on an observed wait or exit.
This is not a harmless addition to the public history.

For example, take the three-point benchmark after $u=1/2$.
An observed wait identifies the high-cost challenger.
Middle second flows cannot induce its entry, and the upper flow reveals $H$ completely.
Every purchase residual is zero, so round-2 purchase profit is $-k$.
No second information arrives, and waiting cannot be optimal.
The private-decision delay outcome $11/24$ therefore does not survive this public-decision interpretation.

The corresponding discrete-Laplace gross profit after an observed wait is $0.111603398186$ at the coexistence point.
It differs from the memo's $0.143065120585$.
After observed exit, gross profit is zero, instead of $0.097872335051$.
This check does not claim a full equilibrium characterization for that alternative game.

### 3.2 Claim 1: prices and residuals

**Status: analytical.** Write $u=\mu_1$, $v=\mu_{12}$, and $w_\theta=t_\theta-t_0$.
Because the first decision stays private, the market averages over the independent cost draw.
The eventual entry rate is

$$
e_2(u,v)=
\begin{cases}
1,&\text{high cost enters now},\\
\rho,&\text{high cost exits},\\
\rho+(1-\rho)\mathbf1\{\delta B_r(v)\ge c_H\},&\text{high cost waits}.
\end{cases}
$$

Therefore

$$
V_\theta^2=t_0+e_2w_\theta,
\qquad P_2=t_0+e_2(w_L+\Delta_Tv).
$$

Subtracting the price gives

$$
R_H^2=e_2\Delta_T(1-v),
\qquad R_L^2=-e_2\Delta_Tv.
$$

The low-class investor never buys because $k>0$.
For a fixed first history, $e_2$ is nondecreasing in $v$ and stays at least $\rho$.
For $v'>v$,

$$
P_2(v')-P_2(v)
=e_2(v')\Delta_T(v'-v)
 +[e_2(v')-e_2(v)](w_L+\Delta_Tv)>0.
$$

Thus the second price reveals its posterior, conditional on the first history.

Let $a_\theta(u)=\mathbb E[e_2(u,v)\mid\theta,u]$.
The first price is

$$
P_1(u)=t_0+u a_H(u)w_H+(1-u)a_L(u)w_L.
$$

Hence

$$
\begin{aligned}
R_H^1(u)
&=(1-u)[a_Hw_H-a_Lw_L]\\
&=(1-u)[\Delta_Ta_H+w_L(a_H-a_L)],\\
R_L^1(u)&=-u[\Delta_Ta_H+w_L(a_H-a_L)].
\end{aligned}
$$

Both noise laws have nondecreasing likelihood ratios under high-class purchases and low-class zero orders.
Couple the classes to the same second noise draw.
The high-class flow is weakly larger, so its entry chance is weakly larger.
Thus $a_H\ge a_L\ge\rho$, and the low-class first investor also never buys.

The extra term is positive when future entry differs across classes.
Relative to immediate entry rate $e_r(u)$, the difference is exactly

$$
(1-u)\{\Delta_T[a_H-e_r(u)]+w_L(a_H-a_L)\}.
$$

The sign of the first term can differ from the second.
The source decomposition is correct.
Its generality is conditional on private decisions, fresh investors, and the monotone experiments just specified.

### 3.3 Claim 2: the exact three-point wait region

**Status: analytical.** Fix the second purchase probability $b_2\in(0,1]$.
This is a conditional stopping result; it does not choose $b_2$ endogenously.
Set $c=c_H$, $S=g_H-g_L$, $A=\delta g_H-c$, and $C=c-g_L$.

At prior $u$, second posteriors and probabilities are

$$
\begin{array}{c|c}
\text{posterior}&\text{probability}\\\hline
1&ub_2/3\\
u&2/3\\
u^-={u(1-b_2)\over1-ub_2}&(1-ub_2)/3.
\end{array}
$$

Direct conditional expectation yields

$$
W(u)=\frac{ub_2}{3}A_+
 +\frac23(\delta B_r(u)-c)_+
 +\frac{1-ub_2}{3}(\delta B_r(u^-)-c)_+.
$$

Each probability-weighted term is the positive part of an affine function of $u$.
For example, the last term is

$$
\frac13\left[(\delta g_L-c)(1-ub_2)
                   +\delta S u(1-b_2)\right]_+.
$$

Consequently $W-N$ is convex.
If $A\le0$, then $W=0$ and the strict wait rule excludes waiting.
If $b_2=0$, the experiment adds no information and also excludes waiting.

Suppose now that $g_L<c<g_H$ and $A>0$.
At $u=\tau=C/S$, $W-N>0$.
At $u=1$, $W-N=-(1-\delta)g_H<0$.
Convexity gives one crossing in $(\tau,1)$.
There cannot be a second crossing before a negative endpoint, because convex secant slopes are nondecreasing.

Put $t=\tau_\delta=(c/\delta-g_L)/S$.
For $u<t$, only the upper signal can justify late entry.
The crossing in this region is

$$
u_0=\frac{C}{S-b_2A/3}.
$$

If $W(t)\le N(t)$, this is the cutoff.
Otherwise the middle signal also permits late entry at the cutoff.
The low signal cannot permit entry there.
If every signal permits late entry, then $W=\delta B_r(u)-c<N(u)$ already.
Solving in the remaining region gives

$$
u_1=\frac{c-(3-2\delta)g_L}{(3-2\delta)S-b_2A}.
$$

In this case, the denominator is positive because $W-N$ crosses from positive to negative on that linear segment.

Thus the complete interior cutoff is

$$
\bar u=
\begin{cases}
u_0,&(tb_2/3)A\le c(1-\delta)/\delta,\\
u_1,&(tb_2/3)A>c(1-\delta)/\delta.
\end{cases}
$$

Waiting occurs exactly for $0<u<\bar u$.
At $u=\bar u$, the challenger enters now.
At $u=0$, it exits when $c>g_L$.

The source permits $c=g_L$ but then claims an interior root.
That boundary claim is false.
Here $(W-N)(0)=0$ and $(W-N)(1)<0$.
Convexity makes $W-N<0$ for every $u\in(0,1)$.
The wait region is empty; at $u=0$, immediate preparation wins the tie.

The exact benchmark cutoffs reproduce:

$$
\begin{array}{c|c|c}
\delta&b_2&\bar u\\\hline
9/10&1&1410/1871=0.753607696419\ldots\\
19/20&1&134/163=0.822085889571\ldots\\
9/10&2/5&3525/4871=0.723670704168\ldots\\
19/20&2/5&21150/29023=0.728732384660\ldots
\end{array}
$$

At $r=3$, $c=6$, and $u=1/2$, the discount threshold is $144/203$.
At $\delta=19/20$, the wait value is $977/2880$.

### 3.4 Claim 3: C3.1, the bottleneck, and endpoints

**Status: analytical.** Maintain $B_r(1/2)<c_H$ and the directional completion.
A purchase reaches the two middle flows and the upper flow, each with probability $1/3$.
The upper flow has zero residual.
At a waiting middle history, expensive entry fails at the unchanged belief.
Thus

$$
K_2(1/2)=\frac23\rho\Delta_T(1-1/2)
=\frac{\rho\Delta_T}{3}.
$$

This formula also gives a deviation's gross profit when second purchases are zero.
The upper off-path flow then receives posterior one.
It cannot reverse a prior exit, so its purchase residual remains zero.

If $k\ge\rho\Delta_T/3$, no second information arrives at the middle belief.
The challenger exits there.
First-round purchase profit then equals the same bound, for every first purchase probability.
The investor tie rule selects no trade at equality.

If $k<\rho\Delta_T/3$ and $\delta g_H>c_H$, full purchases occur at the middle history.
The high-cost challenger waits there, enters now at belief one, and exits at belief zero.
At the middle history,

$$
a_H=\frac{1+2\rho}{3},\qquad a_L=\rho.
$$

Therefore

$$
K_1=\frac{\Delta_T(1+2\rho)+w_L(1-\rho)}9
=\frac{\rho\Delta_T}3+\frac{(1-\rho)w_H}{9}
>\frac{\rho\Delta_T}3.
$$

The second comparison is the binding one.
These first-round profits do not depend on the positive first purchase probability.
The directional completion gives the same deviation comparison at zero.
Hence neither an interior first mixture nor a no-trade outcome coexists with this strict full-purchase outcome.

Expensive preparation occurs after first revelation, with probability $1/6$.
It also occurs after a middle first price and second revelation, with probability $1/9$.
All such preparation concerns class $H$.
Consequently

$$
\mathsf E=\rho+(1-\rho)\frac5{18}=\frac{11}{24},
\qquad
\mathsf O_H=\frac\rho2+(1-\rho)\frac5{18}=\frac13.
$$

At $r=3$, the independent calculation gives

$$
K_1=\frac{43}{288},\quad K_2=\frac1{18},\quad
P_1(1/2)=\frac{145}{192}.
$$

First prices at beliefs zero and one are $17/32$ and $37/24$.
All three prices differ, so the challenger recovers the first posterior.
Second prices on the wait branch are $17/32$, $59/96$, and $37/24$.
All three second choices therefore use the correct posterior.

At absorbing first histories, the on-path investor already faces a certain class.
It earns zero gross profit and submits no second order.
The source's table entry “full, full” must mean full second purchases only at the middle history.

The corrected entry plateaus at $\delta=0.95$ are

$$
\mathsf E(r)=
\begin{cases}
1/4,&r\le r_T,\\
11/24,&r_T<r<r_C(\delta),\\
3/8,&r_C(\delta)\le r\le r_C^D,\\
1/4,&r>r_C^D,
\end{cases}
$$

where

$$
r_T=1.973212111193\ldots,\quad
r_C(0.95)=7.334334798476\ldots,\quad
r_C^D=7.968626966597\ldots.
$$

At $r_C(\delta)$, the wait value is zero and immediate entry at the middle belief loses money.
The strict wait rule selects exit, even though late preparation would win a tie after an actual wait.
The source's closed upper endpoint for the $11/24$ plateau is wrong.
The independent exact case $r=3$, $\delta=144/203$ gives entry $3/8$, not $11/24$.

The stated rise and fall hold, for example, at strengths $1.2$, $3$, and $8.5$.
They do not hold at the paper's original third strength $3.6$.
Entry at $3.6$ remains $11/24$, as the source table correctly reports.

### 3.5 Claim 4: discrete-Laplace wait thresholds

**Status: analytical.** Put

$$
a=e^{-1/2},\quad M=\frac1{1+a},\quad m=\frac a{1+a},
\quad M_2=\frac1{1+a^2},\quad m_2=1-M_2,\quad Q=M^2+m^2.
$$

The likelihood ratio for a purchase versus no purchase is $1/a$ for $x\ge1$ and $a$ for $x\le0$.
Thus full high-class purchases give first posteriors $M$ and $m$.
Both first news cells have probability $1/2$.
Two full rounds give posteriors $M_2$, $1/2$, and $m_2$.
The probability of two good prices is $Q/2$.

Conditional on good first news, good second news has probability $Q$.
Therefore

$$
W(M)=Q(\delta B_r(M_2)-c_H)_+
 +(1-Q)(\delta B_r(1/2)-c_H)_+.
$$

Conditional on bad first news,

$$
W(m)=2mM(\delta B_r(1/2)-c_H)_+
 +(1-2mM)(\delta B_r(m_2)-c_H)_+.
$$

The maintained benchmark has $\delta B_r(1/2)<c_H$.
Thus $W(m)=0$ and only two good prices can cause late preparation.
If $B_r(M)\ge c_H$, comparison with now gives

$$
\delta^*(r)=\frac{c_H+[B_r(M)-c_H]/Q}{B_r(M_2)}.
$$

If $B_r(M)<c_H$, comparison with exit gives

$$
\delta_0(r)=\frac{c_H}{B_r(M_2)}.
$$

Both wait inequalities are strict.
At equality with now, the challenger prepares now.
At equality with exit, it exits.
At $r=3$, $c_H=5$,

$$
\delta^*=0.898962886700027\ldots,
\qquad \delta_0=0.804226393457986\ldots.
$$

At $\delta=0.95$, $N(M)=0.312161093349$ and $W(M)=0.480330724120$.
After bad first news, $N(m)=-1.728827760015$ and $W(m)=0$.
This checks all first-price stopping choices in C3.2.

### 3.6 Claim 5: C3.2 without grids

**Status: analytical.** The source's numerical label is cautious but unnecessary for these benchmark conclusions.
The following global bounds exclude every mixed purchase candidate within the stated canonical game.

With high-class purchase probability $\beta$, one round has likelihood ratios

$$
L^+(\beta)=1+\beta(a^{-1}-1),\qquad
L^-(\beta)=1-\beta(1-a).
$$

Each ratio lies between $a$ and $1/a$.
After one round, $u\in[m,M]$.
After two rounds, $v\in[m_2,M_2]$, even if the second strategy depends on the first price.
The residual formulas therefore imply

$$
K_1\ge\rho\Delta_Tm,
\qquad K_2(u)\ge\rho\Delta_Tm_2.
$$

At $r=3$, these bounds are $0.062923444800$ and $0.044823570228$.
Both exceed $k=0.02$.
Thus high-class purchases are strict in both rounds at every possible first posterior.
The low-class orders are zero by Section 3.2.

These signs need no decimal approximation.
The alternating series for $e^{-1/2}$ gives

$$
\frac35<\frac{2329}{3840}<a<\frac{233}{384}<\frac{61}{100}.
$$

Hence $m>3/8$ and $m_2>9/34$.
Since $\rho\Delta_T(3)=1/6$,

$$
K_1>\frac1{16}>\frac1{50},\qquad
K_2>\frac3{68}>\frac1{50}.
$$

The challenger comparisons also admit rational bounds.
Here $B_3(u)=1/8+(25/3)u$ and $M<5/8$.
Therefore $N(M)<1/3$.
Since $M_2>10000/13721$ and $Q\ge1/2$,

$$
W(M)>
\frac12\left[\frac{19}{20}
 \left(\frac18+\frac{25}{3}\frac{10000}{13721}\right)-5\right]
=\frac{5851697}{13172160}>\frac13.
$$

Also $\delta B_3(1/2)=1957/480<5$, so bad first news leads to exit.
These inequalities prove the stopping choices without a grid.

Direct history probabilities give

$$
\begin{aligned}
\mathsf E_{\rm one}&=\rho+\frac{1-\rho}{2}=0.625,\\
\mathsf E_{\rm delay}&=\rho+(1-\rho)\frac Q2
=0.448747215848804\ldots,\\
\mathsf O_{H,\rm delay}&=\frac\rho2+(1-\rho)\frac{M^2}{2}
=0.270295857125098\ldots.
\end{aligned}
$$

The independent gross profits are

$$
K_1=0.171259845727829\ldots,\quad
K_2(M)=0.143065120585474\ldots,\quad
K_2(m)=0.097872335051253\ldots.
$$

The first prices are $1.010905979229$ and $0.594173444800$.
They differ and reveal the two first posteriors.
Second prices are $1.362372385753$, $0.614583333333$, and $0.576073570228$.
They reveal the relevant second posterior within each first history.
After an initial exit, the entry rate remains $\rho$ even when the second price improves.

At $r=1.2$, $\Delta_T=1/60<k$.
Every second purchase has gross profit at most $\Delta_T$, so no second investor buys.
There is then no gain from delay.
First-round entry has no further class-dependent continuation, so the same upper bound excludes first purchases.
The prior gain is below five, and entry is $1/4$.

At $r=6$, the lower profit bounds increase because $\Delta_T$ increases.
Full purchases remain strict.
The same rational bound for $a$ gives

$$
B_6(M)<\frac{421}{96}<5,
\qquad
\frac{19}{20}B_6(M_2)<\frac{79819}{16320}<5.
$$

Expensive preparation is impossible now or late, and entry returns to $1/4$.
This proves the three-economy conclusion.

The ceilings also have closed forms.
For a fixed posterior $u$,

$$
B_r(u)=uh-\frac{ur}{2}+\frac{(1-u)\ell^2-p^2}{2r}.
$$

Solving $B_r(u)=C$ gives the root in the maintained domain:

$$
R(u,C)=\frac{uh-C+
\sqrt{(uh-C)^2+u[(1-u)\ell^2-p^2]}}{u}.
$$

Both class gains strictly decrease with $r$, so the relevant root is unique.
Therefore

$$
r_{C1}=R(M,5)=3.986096571638404\ldots,
\qquad
r_{C2}=R(M_2,5/0.95)=5.605890889243172\ldots.
$$

Full purchases hold throughout $r\in[3,6]$ by the same bounds.
Thus the roots describe equilibrium ceilings on this interval.
At $r=4.2$, delay creates entry $0.448747215849$ after one-round entry reaches its floor.

At the late ceiling itself, the wait value is zero and now loses money.
Entry therefore equals $\rho$ at $r_{C2}$, under the source's strict wait rule.
By contrast, the one-round preparation rule admits costly entry at $r_{C1}$ itself.

For completeness, the grid minima also admit exact minimizers.
At prior $u$, define the floor-free purchase residual

$$
D(u,\beta)=(1-u)\left[
\frac{M}{1+u\beta(1-a)/a}
+\frac{m}{1-u\beta(1-a)}\right].
$$

Write $d_G=1+u\beta(1-a)/a$ and $d_B=1-u\beta(1-a)$.
Direct differentiation gives

$$
\partial_\beta D
=\frac{u(1-u)(1-a)}{1+a}
\left[\frac{a}{d_B^2}-\frac1{a d_G^2}\right].
$$

The bracket has the sign of $a d_G-d_B=(1-a)(2u\beta-1)$.
Hence the minimizer is $\beta=1$ when $u\le1/2$, and $\beta=1/(2u)$ otherwise.
For $u\ge1/2$, the minimum is $4mM(1-u)$.
At $u=M$, the exact profit bound is

$$
\rho\Delta_T\,4m^2M=0.059148972449758\ldots,
\qquad \beta=0.803265329856317\ldots.
$$

The source grid returns $0.059148972836878$ at $\beta=0.803$.
Its approximation has the expected direction and does not affect any incentive verdict.

### 3.7 Claim 6: exact coexistence inequalities

**Status: analytical.** Use $(r,c_H,\delta,k)=(3,5.5,0.95,0.09)$.
First consider the one-round game.
The bound $B_3(M)<16/3<11/2$ excludes expensive entry for every purchase probability.
Thus

$$
K(\beta)=\rho\Delta_T H(\beta),\qquad
H(\beta)=\frac{M}{2+\beta(a^{-1}-1)}
+\frac{m}{2-\beta(1-a)}.
$$

Differentiation shows $H'(\beta)\le0$ for $0\le\beta\le1$.
The sign comparison reduces to

$$
a[2+\beta(a^{-1}-1)]-[2-\beta(1-a)]
=2(1-a)(\beta-1)\le0.
$$

Therefore $K(\beta)\le K(0)=1/12<9/100$.
One-round no trade is unique, including against mixed purchase candidates.

In the two-round game, choose no purchases in both rounds.
Every flow history leaves belief $1/2$ because both noise laws coincide across classes.
The high-cost challenger exits, and entry is $\rho$.
Each investor deviation earns gross $1/12<9/100$.
This establishes the no-trade equilibrium.

For the informative outcome, choose full high-class purchases after both first prices.
Now after good first news loses money:

$$
N(M)<\frac{16}{3}-\frac{11}{2}=-\frac16.
$$

Late surplus after two good prices is strictly positive:

$$
\delta B_3(M_2)-\frac{11}{2}
>\frac{2558657}{6586080}>0.
$$

Thus the challenger waits after good news.
After bad news, even a good second price only returns belief to $1/2$.
Its late gain is below $11/2$, so the challenger exits.
The entry policy and all prices equal those in C3.2.

The three gross profit conditions have rational lower bounds:

$$
\begin{aligned}
K_2(M)&=\frac23\left[Mm_2+\frac m8\right]
>\frac{12337}{87584}>\frac9{100},\\
K_2(m)&=\frac16\left[\frac M2+mM_2\right]
>\frac{644900}{6627243}>\frac9{100},\\
K_1&=mM\left\{\Delta_T[2\rho+(1-\rho)M]
+w_L(1-\rho)(M-m)\right\}\\
&>\frac{15}{64}\left(\frac13+\frac{50}{161}\right)
=\frac{1555}{10304}>\frac9{100}.
\end{aligned}
$$

The bounds use $M>100/161$, $m>3/8$, $m_2>9/34$, and $M_2>10000/13721$.
They also use $mM=a/(1+a)^2>15/64$.
This follows from $a>3/5$ and derivative $(1-a)/(1+a)^3>0$ on the stated interval.
All low-class purchases lose money, by the residual signs.
Every challenger action is optimal after each first and second price.
The prices distinguish the relevant posteriors.
These facts complete the informative equilibrium construction.

The two entry rates are therefore $0.25$ and $0.448747215849$ at the same primitives.
Both equilibria use strict investor comparisons.
Continuity preserves them in a neighborhood of this parameter point.
The result needs no grid and deserves the label **analytical** after this proof is added.

### 3.8 Claims 7 and 8: timing, grading, and the coexistence explanation

**Status: analytical, with the benchmark scope stated.** Fix the informative second experiment.
Every $B_r(v)$ strictly decreases with $r$.
Thus $W$ decreases while it is positive.
However, the relative benefit of wait versus now can increase.

In the discrete-Laplace region with only good second news permitting entry,

$$
W(M)-N(M)
=\delta(M^2g_H+m^2g_L)-(Mg_H+mg_L)+2mMc_H.
$$

Its derivative is

$$
\frac{d(W-N)}{dr}
=M(\delta M-1)g_H'+m(\delta m-1)g_L'>0.
$$

Both coefficients and both gain derivatives are negative.
Also $\partial(W-N)/\partial\delta=Q B_r(M_2)>0$.
Implicit differentiation gives $\delta^{*\prime}(r)<0$.
In contrast,

$$
\delta_0'(r)=-\frac{c_H B_r'(M_2)}{B_r(M_2)^2}>0.
$$

The thresholds meet exactly where $B_r(M)=c_H$.
Thus their combined threshold has its minimum exactly at $r_{C1}$, within this region.
The source's “near” can be replaced with “at.”

At $\delta=0.9$, the full-purchase stopping switch is $r=2.976187631856\ldots$.
At $r=2.5$, the challenger enters now after good news.
At $r=3$, it waits.
At $r=5$, it exits.
Full purchases are strict at all three points by Section 3.6's bounds.

At $\delta=0.95$, waiting occurs at $r=2$ and $r=3$, and disappears by $r=6$.
At $r=2$, the exact residual minimum gives a second profit bound above $0.02$.
Indeed $4m^2M>225/644$, so $K_2>225/10304>1/50$ there.
The first profit bound is $K_1>3/128>1/50$.
At $r=1.2$, both rounds have no trade and no wait.

The three-point delay interval is exactly $(r_T,r_C(0.95))$ in C3.1.
These benchmark examples establish delay at intermediate strengths.
They do not prove a nonempty delay interval for every primitive vector.
For example, $\delta h\le c_H$ prevents profitable late preparation at every strength.

The source must define its timing statistic.
The probability of a wait is not the mean time of actual preparation.
Set preparation time to zero for early preparation and one for late preparation.
Condition on eventual preparation, which has positive probability because $\rho>0$.
On the two delay plateaus,

$$
\begin{aligned}
\mathbb E[T\mid\text{prepare}]_{\rm three}
&=\frac{(1-\rho)/9}{11/24}=\frac2{11},\\
\mathbb E[T\mid\text{prepare}]_{\rm dLaplace}
&=\frac{(1-\rho)Q/2}{\rho+(1-\rho)Q/2}
=0.442893479512456\ldots.
\end{aligned}
$$

It is zero in the low-strength and high-strength benchmark outcomes.
This gives a precise non-monotone timing result.
The source's conditional high-cost wait probabilities, $2/3$ and $1/2$, are also correct.
They count challengers who later exit as well as those who prepare.

For Claim 8, full three-point purchases preserve final beliefs $\{0,1/2,1\}$.
The extra round changes their probabilities, so it adds no new belief grade.
The strict second purchase comparison at $1/2$ prevents an open coexistence region under C3.1's assumptions.
Full revelation remains feasible, and costly immediate entry survives until $g_H=c_H$.
Thus the early ceiling associated with a strict posterior bound below one is absent.

One source explanation is wrong: delay does raise first-round purchase profit through future entry.
The exact increase is $(1-\rho)w_H/9>0$.
At $r=3$, it is $3/32$.
Zero residual at the recruiting second flow blocks round-2 feedback, not round-1 feedback.
The bottleneck, rather than absence of all feedback, explains the lack of coexistence here.

### 3.9 Source outputs, numerical agreement, and one calculation error

**Status: numerical diagnostic.** All three source programs completed through their normal command interface.
Their captured output is in this check's folder:

- [source_three_point.txt](../scripts/X_C3_check/source_three_point.txt).
- [source_dlaplace.txt](../scripts/X_C3_check/source_dlaplace.txt).
- [source_welfare.txt](../scripts/X_C3_check/source_welfare.txt).

The exact three-point fractions agree, including $11/24$, $1/3$, $43/288$, $977/2880$, and $145/192$.
The main discrete-Laplace probabilities, profits, and discount threshold agree to at least 48 decimal places.
The two main ceiling roots also agree to at least 48 decimal places.
Every rounded headline number in the source memo matches its program output.

The ancillary proceeds and challenger profits also agree:

| Quantity at $r=3$ | One round | Delay |
|---|---:|---:|
| Three-point target proceeds | $145/192$ | $163/192$ |
| Three-point profit, conditional on high cost | $59/144$ | $2747/4320$ |
| Discrete-Laplace target proceeds | $0.942073166134$ | $0.802539712014$ |
| Discrete-Laplace profit, conditional on high cost | $0.156080546674$ | $0.240165362060$ |

The source welfare program uses saved decimal constants for several discrete-Laplace quantities.
The independent calculation derives those quantities from the signal probabilities.
Their agreement checks the constants; the source program alone does not independently derive them.

There is one separate source calculation error.
For $\delta=0.8$, the ceiling routine starts on $[3,8]$, which contains no root.
Both endpoint residuals have the same sign.
The routine nevertheless returns eight.
The closed-form root is instead

$$
R(M_2,5/0.8)=2.910409369040242\ldots.
$$

At the reported value eight,

$$
0.8B_8(M_2)-5=-1.489971751507477\ldots,
$$

so eight cannot be a root.
This error does not affect the reported roots at $\delta=0.9$ or $0.95$.
The $0.8$ root concerns late feasibility; immediate entry still survives to the one-round ceiling.
Thus the total entry ceiling at $\delta=0.8$ remains $3.986096571638$, not the late root or eight.

## 4. Errors found and corrections

1. **State privacy explicitly.** The source prices average over cost after round 1.
   Public preparation decisions require prices conditional on those decisions.
   The three-point delay equilibrium fails under that public interpretation.

2. **Correct the wait-region boundary.** The interior crossing theorem requires $c_H>g_L$.
   At $c_H=g_L$, waiting never wins.

3. **Open the late-entry endpoint.** At $\delta g_H=c_H$, the high-cost challenger does not wait at the middle belief.
   Entry is $3/8$, not $11/24$.
   At the discrete-Laplace late ceiling, the same strict wait rule gives entry $\rho$.

4. **Open the entry-creation cost window.** At fixed $r$, the window is
   $B_r(M)<c_H<\delta B_r(M_2)$.
   The source's closed upper endpoint gives zero option value and therefore exit.

5. **Complete the trade labels.** Full second purchases apply only to nonabsorbing histories in the three-point outcome.
   At a certain class, the on-path investor submits zero.

6. **Separate tie conventions.** The declared investor rule excludes zero-profit mixtures.
   Conventional mixtures at equality require an explicit change to that rule.

7. **Correct the coexistence explanation.** Round-1 feedback is strictly positive under three-point delay.
   Round 2 remains the bottleneck.

8. **Qualify timing.** The non-monotone timing result needs the benchmark conditions and a defined timing statistic.
   A wait does not always lead to late preparation.

9. **Repair the extra ceiling row.** The source's $\delta=0.8$ root is $2.910409369040$, not eight.
   A closed-form calculation avoids the invalid interval.

## 5. What the original memo should change

Add an explicit statement that preparation decisions and their payments remain private until after round 2.
Retain fresh investors and the gross-profit discount as separate maintained assumptions.
Do not transfer these conclusions to one investor with a retained stake.

Replace Result 4's boundary statement with Section 3.3's complete cutoff formula.
Correct the two late-ceiling endpoints and the cost window.
Revise the three-point table labels to identify the middle history.

Replace the grid argument for C3.2 with the uniform residual bounds in Section 3.6.
Add the rational inequalities in Section 3.7 to the coexistence result.
Those additions justify **analytical** labels for the benchmark uniqueness and coexistence claims.
Keep the broader mixed equilibrium correspondence **open**.

Add the derivative proof for the discount threshold and define mean preparation time conditional on preparation.
Limit the three-point no-coexistence statement to C3.1's region and price convention.
Replace the claim of absent feedback with the exact round-1 feedback increment.

Correct the extra ceiling calculation and label late feasibility separately from the total entry ceiling.
The source memo's central numerical examples can stay.

## 6. Plain summary

The central results survive when the first preparation decision stays private.
Three-point delay raises benchmark entry to $11/24$.
Its second round remains the binding trade condition.
Discrete-Laplace delay lowers entry at strength three to $0.448747$ and extends the ceiling to $5.605891$.
The stated coexistence example also works.

Exact inequalities replace the grid arguments for the benchmark uniqueness and coexistence claims.
The independent calculations reproduce all headline numbers.

Several corrections are necessary.
Public observation of preparation changes second prices and defeats the three-point delay construction.
Zero option value selects exit under the stated wait rule, so the late ceilings have strict endpoints.
The general three-point cutoff also needs a separate case when the high cost equals the low-class gain.
The investor tie rule excludes conventional zero-profit mixtures.

Three-point delay does create first-round feedback.
The second round prevents that feedback from creating coexistence in the stated region.
The timing result needs a precise statistic and benchmark scope.
One extra source calculation is wrong: the late ceiling at discount $0.8$ is $2.910409$, not eight.
