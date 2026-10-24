# XN2: Independent check of dynamics and arrivals

## 1. Scope

This memo checks Extensions A–D of `N2_dynamics.md` at the stated benchmark.
It checks the posterior bounds, date choices, price path, entry band, and Poisson result.
It does not verify literature claims or empirical predictions.

**Model.** The primitives are $(h,\ell,p,\rho,c_H,k,\pi)=(10,1,1/2,1/4,6,1/50,1/2)$, with $c_L=0$.
The informed menu is $\{-1,0,1\}$, except where the buy-only menu is explicit.
Fresh arrivals replace the liquidity trader in each slot.
One informed unit instead replaces one liquidity order during the whole window.
Liquidity orders have probabilities $(\beta,1-2\beta,\beta)$ on the two-sided menu.
They have probabilities $(1-\beta,\beta)$ on the buy-only menu $\{0,1\}$.

**Concept.** The equilibrium concept is perfect Bayesian equilibrium in the finite game.
A deviation faces the fixed price and entry schedules.
Market makers price terminal target proceeds, with all future entry decisions included.
The challenger observes the terminal price and its cost.
The terminal price reveals the terminal posterior because $\rho\Delta>0$.

**Beliefs and ties.** Every public history has positive mass from the absent-investor event in C.
Every public history has positive liquidity mass in A and B.
Thus Bayes' rule fixes all public beliefs on the unit menu.
Private information sets after an unexpected delay still need optimal continuation choices.
IM permits date mixtures; C1 requires preparation at a cost tie.
CM permits a challenger mixture at a cost tie.
The threshold date equilibrium needs CM; the other reported access equilibria use strict challenger choices.
An alternative rule that forbids date mixtures excludes the mixed-date constructions.
Continuous order sizes require a separate analysis of unused flows.

**Method and evidence.** I derived the formulas and wrote `scripts/XN2_check/independent.py` from scratch.
I ran it before I read or ran the original programs.
The program uses exact fractions for finite histories, payoffs, and root brackets.
It uses integer recursion for the fresh-arrival tail probabilities.
Logarithms and asymptotic rate displays use floating-point arithmetic.
The program contains no assertions.

I then ran all three N2 programs through the slot wrapper.
Their output agrees with the saved output after removal of the wrapper's process line.
All outputs are in `scripts/XN2_check/`.
No test suite ran. No commit was made.
The auction formulas agree with equation (4) at pinned paper commit `01bd5d6`.
The program computes those objects by direct piecewise integration.

## 2. Verdict table

| Claim | Verdict | Evidence |
|---|---|---|
| C: the likelihood ratio stays within the one-slot bound for every finite horizon | **CONFIRMED** | Pathwise convex-combination proof in §3.2. The buy-only bound is tighter and uses a different effective knob. |
| C: entry returns to $1/4$ at $r=3.6$ | **CONFIRMED** | The posterior cap excludes expensive preparation. The last-date trade margin is positive. |
| C: visibility supports an early buyer; the reported $(1,-0.167)$ outcome has entry $91/204$ | **CONFIRMED WITH CORRECTION** | The equilibrium exists. A second equilibrium reverses the date order: $x_H=0$, $x_L\approx0.837634$, with the same entry. |
| C: the buy-only list at $r=3$ is complete | **CONFIRMED WITH CORRECTION** | Exact signs establish completeness: $x_H=0$, $x_H=1$, and one CM threshold equilibrium. A grid is unnecessary. |
| C: the two-sided examples exhaust the two-slot correspondence | **REFUTED**, if read as exhaustive | The explicit extra equilibrium in §3.4 is absent from the list. N2's C4 states existence; it does not supply a complete two-sided classification. |
| A: $0.871222\le n\log(1+u)<1.001697$ and $u\approx0.93/n$ | **CONFIRMED WITH CORRECTION** | The band holds for $\beta\le1/3$, under C1. The constant $0.93$ is one choice; the limit can be any interior band value. CM needs a strict lower endpoint. |
| A: extra entry decays like $e^{-0.306n}$ | **CONFIRMED WITH CORRECTION** | This is a conservative upper bound. It is not an exact decay rate. At $\beta=1/3$, the least limiting imbalance exponent is about $0.696339$. |
| B: the opening price includes future entry | **CONFIRMED** | $P_0=14747/20736$, against the static prior price $59/96$. All stated price fractions reproduce. |
| B: early informed traders earn 12.8% more | **REFUTED** as a profit comparison | $33/257=12.84\%$ is the early term's share of $D(+)$. The net profit increase is $45.52\%$. N2's detailed formula states the share correctly. |
| B: the complete two-slot list has no rising branch at 1.55–1.65 | **CONFIRMED** | The reduced equilibrium system gives NT, FF, and, under CM, TH. TH entry falls: $0.286077,0.278129,0.271777$. |
| B: the last-date inequality proves a general prohibition on rising entry for every horizon | **NOT CHECKABLE** as a theorem | The inequality holds. It does not determine early-date mixtures or recruitment probabilities for $n\ge3$. |
| D: entry at 3.6 exceeds the floor at every positive Poisson rate | **CONFIRMED** | The contradiction proof holds for every fixed $u>0$. The exact $N=2$ factor is $481/2601$. |

## 3. Derivations

### 3.1 Auction objects and terminal values — analytical

Direct integration gives

$$
\begin{aligned}
t_0&=p(r-p)/r,\\
t(v)&=\frac{p^2+\int_p^{\min(v,r)}R\,dR+v(r-v)^+}{r},\\
g(v)&=\frac{p(v-p)+\int_p^{\min(v,r)}(v-R)\,dR}{r}.
\end{aligned}
$$

Here $v\in\{1,10\}$ and $p=1/2<v$.
These expressions give $t_H+g_H=10$ and $t_L+g_L=1$.
At $r=3$ they give

$$
(t_0,t_H,t_L,g_H,g_L)=(5/12,37/24,7/8,203/24,1/8).
$$

Thus $\Delta=2/3$, $\tau(3)=141/200$, and $T_1=\tau(3)/(1-\tau(3))=141/59$.
At $r=18/5$, $\Delta=169/180$, $\tau=4245/5804$, and $T_2=4245/1559$.
Write $w_j=t_j-t_0$ throughout this memo.

### 3.2 C: a pathwise cap for one unit — analytical

Fix a public history $h=(q_1,\ldots,q_n)$ and one class $j$.
Let $a_t(h)$ be its trade hazard, conditional on no earlier trade.
Define

$$
\alpha_t(h)=a_t(h)\prod_{s<t}[1-a_s(h)],\qquad
\alpha_\infty(h)=\prod_{s=1}^n[1-a_s(h)].
$$

These are pathwise strategy weights, rather than probabilities conditional on the completed observed history.
They are nonnegative, and their sum is one.
If the informed investor trades at $t$, its order replaces the liquidity order there.
All other orders retain their liquidity probabilities.
Hence

$$
\Pr(h\mid j)=\prod_s\eta(q_s)
\left[1-\lambda+\lambda\left\{
\alpha_\infty(h)+\sum_t\alpha_t(h)
\frac{\mathbf1\{q_t=o_j\}}{\eta(q_t)}\right\}\right].
$$

The expression in braces is a convex combination of $1$, $0$, and $1/\beta$.
It lies in $[0,1/\beta]$.
Therefore, with $u=\lambda/[(1-\lambda)\beta]$,

$$
\frac1{1+u}\le\frac{\Pr(h\mid H)}{\Pr(h\mid L)}\le1+u.
$$

The result permits adaptive hazards and private randomization.
A mixture over random seeds preserves both bounds.
It also applies to every prefix of a history.
For the buy-only menu, the passive low class always has the pure liquidity law.
Its tighter bound is

$$
1-\lambda\le\frac{\Pr(h\mid H)}{\Pr(h\mid L)}
\le1+\lambda(1-\beta)/\beta.
$$

This distinction matters for the calibration $(\beta,\lambda)=(1/5,9/22)$.
Its buy-only top ratio is $29/11$, and its top posterior is $29/40$.
The common two-sided definition of $u$ would give $u=45/13$, rather than $18/11$.
Use the tighter buy-only ratio for that example.

If the top posterior is below $\tau(3.6)$, entry equals $\rho$ at every history.
An unspent unit then earns at least $\rho\Delta(1-M)-k$ at the last date.
At $M=29/40$ and $r=3.6$, the margin is $1283/28800>0$.
Thus every present investor trades before the finite horizon ends.
Under floor entry, wrong-sign trades lose, so the final order law differs across classes.
Prices therefore remain informative.

### 3.3 C: trade-date payoffs and the reported equilibrium — analytical and computer-assisted

Let $x_H,x_L$ be the first-date trade probabilities.
At $r=3$, the posterior cap makes all correctly signed last-date trades strictly profitable.
Thus the remaining units trade at date two after every first order.
For $a,b\in\{-1,0,1\}$, their exact class laws are

$$
f_j(a,b)=(1-\lambda)\eta(a)\eta(b)
+\lambda x_j\mathbf1\{a=o_j\}\eta(b)
+\lambda(1-x_j)\eta(a)\mathbf1\{b=o_j\}.
$$

Bayes' rule gives $\mu_{ab}=f_H/(f_H+f_L)$.
Set $e_{ab}$ from this posterior, then compute

$$
P_2(a,b)=t_0+e_{ab}[w_L+\mu_{ab}\Delta],\qquad
P_1(a)=\frac{\sum_{b,j}f_j(a,b)[t_0+e_{ab}w_j]}{\sum_{b,j}f_j(a,b)}.
$$

The first-date investor knows whether its unit remains unspent.
Its continuation law after an immediate trade is pure liquidity.
Use that private fact in its payoff:

$$
\begin{aligned}
U_j^{\rm now}
 &=o_j\left[t_0+w_j\sum_b\eta(b)e_{o_jb}-P_1(o_j)\right]-k,\\
U_j^{\rm wait}
 &=\sum_a\eta(a)\max\{0,\ o_j[t_0+e_{ao_j}w_j-P_2(a,o_j)]-k\}.
\end{aligned}
$$

These formulas also evaluate delays after a deterministic first-date trade strategy.
They avoid an incorrect substitution of public class beliefs for the investor's private capacity state.

Set $x_H=1$, $\beta=1/3$, and $\lambda=6/17$.
On the relevant interval, only $(+,+)$ and $(+,0)$ recruit.
The seller's date gap is

$$
G_L(x)=\frac{11}{6(28+12x)}
-\frac1{18}\left[\frac{11}{40}+\frac{11}{40-18x}+\frac{29}{58-18x}\right].
$$

Its first term falls strictly in $x$.
Its two variable subtracted terms rise strictly in $x$.
The unique root lies in

$$
x_L\in[0.16723454197003368,\ 0.16723454197003420].
$$

The program prints exact rational endpoints and opposite payoff signs.
At this root, the seller earns $0.041097233$ at either date.
The buyer earns $0.183200916$ now and $0.100009991$ after a delay.
Its date gap is about $0.083190926>0$.
Both wrong-sign first-date trades lose; all last-date correct trades earn positive net payoffs.
These strict signs persist throughout the narrow root bracket.

The recruitment event has probability $40/153$.
Therefore

$$
\mathsf E=\frac14+\frac34\frac{40}{153}=\frac{91}{204}.
$$

The first-date expected orders are $(1,-x_L)$, conditional on presence and class.
Every realized trade still has unit size.
This is a date mixture, rather than a fractional sale within one slot.

### 3.4 C: an additional equilibrium reverses the date order — analytical and computer-assisted

Set $x_H=0$ at the same two-sided calibration.
Let $x=x_L\in[4/5,9/10]$.
Only $(0,+)$ and $(+,+)$ recruit throughout this interval.
The seller's date gap becomes

$$
G_L(x)=\frac{17}{6(34+12x)}
-\frac{11}{720}-\frac{11}{9(40-18x)}
=\frac{12(198x^2-3819x+3060)}{720(34+12x)(40-18x)}.
$$

The denominator is positive.
The numerator falls strictly on $[0,1]$, since $396x-3819<0$.
Its values at $4/5$ and $9/10$ have opposite signs.
It therefore has exactly one root there:

$$
x_L=\frac{3819-\sqrt{12161241}}{396}
\approx0.837633608911.
$$

The program prints exact payoff signs around this root.
The seller earns $0.044318506$ at either date.
The buyer earns $0.005126712$ now and $0.128526016$ after a delay.
Its date gap is about $-0.123399304$.

An explicit bound also certifies the buyer's preference throughout $[4/5,9/10]$.
Its immediate payoff falls in $x$ on this interval.
Its delay payoff is at least $2(49/300)/3+(31/1200)/3$.
The resulting upper bound on its date gap is $-3823/35040<0$.
Both wrong-sign first-date payoffs are negative at the root.
Each last-date correctly signed payoff is positive.
Thus this profile is an equilibrium under IM and C1.

The recruitment probability is again $40/153$, so entry is again $91/204$.
The buyer now always waits; most sellers trade early.
This example disproves a universal date-order prediction.
It does not invalidate the equilibrium in §3.3.
I do not claim a complete two-sided classification.

### 3.5 C: exact completeness for the buy-only access example — analytical and computer-assisted

Here $(\beta,\lambda)=(1/5,9/22)$ and $x=x_H$.
The low class never trades, so no bad-news seller exists in this menu.
The last-date trade margin is positive, which forces the remaining buyer to trade.
The four terminal likelihood ratios are

$$
R_{++}=29/11,\quad R_{+0}=13/22+45x/22,\quad
R_{0+}=13/22+45(1-x)/22,\quad R_{00}=13/22.
$$

The only entry boundaries are $x=64/531$ and $x=467/531$.
Let $G(x)=U_H^{\rm now}-U_H^{\rm wait}$.
Multiply it by the positive denominator

$$
D(x)=(2+18x/11)(40/11-45x/22).
$$

Direct rational algebra gives:

| Interval | $D(x)G(x)$ | Sign |
|---|---|---|
| $0<x<64/531$ | $(-8559x^2+1599x-26480)/19360$ | Negative |
| $64/531<x<467/531$ | $(-8559x^2+14271x-10992)/19360$ | Negative |
| $467/531<x<1$ | $(27x^2-363x+416)/220$ | Positive |

The program prints exact extrema on each closed interval.
At the lower boundary, both feasible challenger tie choices give a negative date gap.
No equilibrium occurs there.
At the upper boundary, the date gap is affine in the challenger mixture.
It crosses zero once:

$$
x_H=467/531,\qquad
\zeta(+,0)=9659/29415,\qquad
\mathsf E=9451817/25453780\approx0.371332549.
$$

Both boundary strategies $x_H=0$ and $x_H=1$ are equilibria.
Each gives entry $23/44$.
These three strategies exhaust the access equilibria under IM and CM.
Under C1, only the two pure date strategies remain.
Thus an early visible purchase is an equilibrium, not a unique date prediction.

Without price access, the independent root brackets reproduce $x_H\approx0.485948606094$.
For two-sided hidden prices, they reproduce $x_H=x_L\approx0.503992352571$.
The same respective profiles apply at $r=3.6$, where entry is also constant.
These root calculations do not establish a complete hidden-price correspondence.

### 3.6 A: the band and the trade incentives — analytical

Let $b=(1-\lambda)\beta$ and $c_0=(1-\lambda)(1-2\beta)$.
For either signed order, its one-slot likelihood ratio lies within $[(1+u)^{-1},1+u]$.
For zero, the ratio instead lies within $[(1+\lambda/c_0)^{-1},1+\lambda/c_0]$.
Thus the common bound requires $c_0\ge b$, or $\beta\le1/3$.
Products give a maximum terminal posterior

$$
M_n=\frac{(1+u)^n}{1+(1+u)^n}.
$$

For a fresh investor, the future arrival law depends on class and public history alone.
Its public residual spread is

$$
D(h)=\Delta\,\mathbb E[e\mid H,h]
+w_L\{\mathbb E[e\mid H,h]-\mathbb E[e\mid L,h]\}\ge\rho\Delta.
$$

To justify the inequality, set $m=\Pr(H\mid h)$ and use the posterior martingale:

$$
\mathbb E[e\mid H,h]-\mathbb E[e\mid L,h]
=\frac{\operatorname{Cov}(e(\mu_n),\mu_n\mid h)}{m(1-m)}\ge0.
$$

Entry is nondecreasing in the terminal posterior, so this covariance is nonnegative.
A correctly signed order therefore earns at least $\rho\Delta(1-M_n)-k$.
This margin is positive at both $r=3$ and $r=3.6$ when $M_n<\tau(3.6)$.
It forces full correct orders at every node.

Under full orders, posterior odds are $(1+u)^D$, where $D$ is buys minus sales.
The all-buy history recruits at $r=3$ exactly when $(1+u)^n\ge T_1$.
No history recruits at $r=3.6$ exactly when $(1+u)^n<T_2$, under C1.
Therefore

$$
\log(141/59)\le n\log(1+u)<\log(4245/1559).
$$

The endpoints are $0.871222446472$ and $1.001697229688$.
The lower endpoint must be strict if the claim must hold for every CM tie choice.
If $n\log(1+u_n)\to a$, then $nu_n\to a$.
The value $a=0.93$ is an admissible choice, rather than a uniquely selected coefficient.

The upper bound is necessary even outside $\beta\le1/3$.
Suppose every terminal history gives floor entry at $r=3.6$.
Every terminal posterior is then at most $\tau(3.6)$; interim posteriors obey the same cap.
The positive purchase margin forces full high-class purchases.
Low-class purchases lose under constant entry.
Each buy has ratio $1+u$, so a sufficiently long all-buy history contradicts the floor.

At $r=1.2$, no trade follows by backward induction.
The last investor cannot recover $k$ because $\Delta=1/60<1/50$.
Its absence of trade makes the last order uninformative.
Apply the same argument to each earlier date.
The conclusion holds, but N2's stronger statement about every arbitrary continuation schedule does not.

### 3.7 A: the exponent is a bound — analytical, with numerical rate displays

Under full orders, define $d^*=\lceil\log(T_1)/\log(1+u)\rceil$.
Recruitment requires $D\ge d^*>\theta n$, where $\theta=0.869746287253$.
This event requires at least $\theta n$ purchases.
The class-H purchase probability is at most $p_n=(1+u)/(2+u)$.
Consequently,

$$
\mathsf E_n(3)-\rho
\le(1-\rho)\exp[-n\operatorname{KL}(\theta\Vert p_n)]
=O\!\left(e^{-0.306278461217n}\right).
$$

Here $p_n=1/2+O(1/n)$ on the band.
The purchase-count argument drops the adverse effect of sales on net imbalance.
It therefore cannot identify the exact decay exponent.

For fixed $\beta$, the limiting order law is $(\beta,1-2\beta,\beta)$.
If $n\log(1+u_n)\to a$, put $d=\log(T_1)/a$.
Exponential tilts give the net-imbalance rate

$$
I_\beta(d)=\sup_{t\ge0}\left\{td-\log[1-2\beta+2\beta\cosh t]\right\}.
$$

For completeness, the tilted probabilities are proportional to $(\beta e^{-t},1-2\beta,\beta e^t)$.
Choose $t$ so their mean is $d$.
A multinomial term with these frequencies has log probability $-nI_\beta(d)+O(\log n)$.
The exponential bound gives the matching upper rate.
The $O(1/n)$ perturbation in the original probabilities does not change this limit.

At the upper band edge, $d\to\theta$.
The independent rate displays give $I_{1/3}(\theta)=0.696339238235$ and $I_{1/2}(\theta)=0.452299992025$.
Thus even the limiting two-sign law has an exponent above $0.306$.
For an interior band choice, the exact decline can be faster still.

The independent integer recursion uses $u_n=93/(100n)$ and $\beta=1/3$.
Its exact tails give extra entry about $1.79\times10^{-6}$ at $n=12$ and $1.04\times10^{-74}$ at $n=192$.
The program retains exact integer arithmetic until the final decimal display.
It also reproduces $\mathsf E_2(3)=305/864$ at $u=3/5$ and $\mathsf E_3(3)=14965/52488$ at $u=3/8$.

### 3.8 B: interim prices and profit shares — analytical and computer-assisted

At $(\beta,\lambda)=(1/3,1/6)$ and $r=3$, only $(+,+)$ recruits.
The exact program sums the terminal proceeds over both classes and all nine histories.
It gives

$$
P_0=14747/20736=0.711178627,\qquad
P_{\rm static}(1/2)=59/96=0.614583333.
$$

After the first buy, $P_1(+)=6749/7488$.
After the second buy, $P_2(+,+)=2893/2136$.
These values confirm that the first price includes future preparation.

After a first buy,

$$
\mathbb E[e\mid H,+]=7/12,\quad
\mathbb E[e\mid L,+]=11/24,\quad
D(+)=7/18+11/192=257/576.
$$

The early term's share is

$$
\frac{11/192}{257/576}=\frac{33}{257}=12.840467\%.
$$

The expected class-H net profits per informed arrival are instead

$$
U_1=28381/187200=0.151607906,\qquad
U_2=216973/2082600=0.104183713.
$$

Therefore $U_1/U_2-1=790125/1735784=45.519777\%$.
The 12.8% figure is not a percentage increase in these profits.
N2's detailed B2 states the spread-share interpretation correctly.

### 3.9 B: complete classification at the three middle strengths — analytical and computer-assisted

The first posterior lies in $[5/13,8/13]$.
At all three strengths, $8/13<\tau(r)$ and $8/5<T(r)$.
A last-date sale cannot recruit and earns at most $\rho\Delta(8/13)<k$.
A first-date sale leaves no possible recruiting continuation and earns at most $\rho\Delta/2<k$.
Thus no low-class investor sells.

After a first wait, a last buy cannot recruit and earns at most $\rho\Delta(8/13)<k$.
After a first sale, it also cannot recruit and earns at most $\rho\Delta/2<k$.
Only $(+,+)$ can recruit.
Let $a_1,a_2\in[0,\lambda]$ be the effective purchase rates at the two remaining nodes.
Then

$$
\frac{\mu_{++}}{1-\mu_{++}}=\frac{(b+a_1)(b+a_2)}{b^2},\qquad b=5/18.
$$

An interior last-date rate with full entry requires $\mu_{++}=1-k/\Delta>M_2=64/89$.
An interior rate with floor entry requires $\mu_{++}=1-k/(\rho\Delta)<1/2$.
Both are impossible.
Thus the last rate is zero, full, or at the entry threshold with CM.

Zero continuation forces $a_1=0$: NT.
Full continuation makes the first purchase strictly profitable and forces $a_1=\lambda$: FF.
The first gross returns are $0.042054384$, $0.045522837$, and $0.049121018$.
The corresponding net margins are $0.022054384$, $0.025522837$, and $0.029121018$.
N2's step 6 quotes gross returns, despite an ambiguous use of the word “return.”

For the threshold case, let

$$
e^*=\frac{k}{\Delta(1-\tau)},\qquad
a_2=\frac{Tb^2}{b+a_1}-b.
$$

The first purchase gross return is

$$
F(a_1)=\frac{b}{2b+a_1}
\left[\rho\Delta+(e^*-\rho)
\left(\frac{w_HTb^2}{b+a_1}-w_Lb\right)\right].
$$

The bracket is the positive spread $D(+)$.
Its derivative is strictly negative.
The prefactor is positive and strictly decreasing.
Thus $F$ falls strictly, and $F(a_1)=k$ has at most one root.
Exact endpoint signs establish one feasible root at each strength.
The program reproduces both purchase rates and all challenger mixtures in N2.

Since $\Pr(+,+)=b^2/[2(1-\tau)]$ at the threshold,

$$
\mathsf E_{\rm TH}=\rho+(e^*-\rho)\frac{b^2}{2(1-\tau)}.
$$

The exact entries are

$$
\frac{27836460787}{97304014368},\quad
\frac{19985233}{71856072},\quad
\frac{1992474573587}{7331294419488}.
$$

They equal $0.286077208$, $0.278128660$, and $0.271776641$.
FF entry is $305/864$ at every strength; NT entry is $1/4$.
Under C1, TH disappears.
The classification is complete for this two-slot calibration.

### 3.10 B: what the general cap proves — analytical limitation

Let every reachable posterior be at most $\bar\mu=\tau(3.6)$.
A last buyer at a full-entry history earns $\Delta(1-\mu)-k$.
For $r>1.467472\ldots$, its lower bound $\Delta(1-\bar\mu)-k$ is strictly positive.
Thus a last-date interior purchase cannot coexist with full entry at its own terminal history.

This result does not force every earlier purchase rate to be full.
It also does not fix the probability of a recruiting history.
Even a declining threshold entry rate can accompany changing probabilities of reaching different thresholds.
The two-slot reduction resolves those issues at its calibration.
N2 does not give a corresponding reduction for every $n$.
Its general statement that rising entry needs another device is therefore unproved.
The valid general result is a local last-date obstacle.

### 3.11 D: Poisson arrivals — analytical

Let $N$ have a Poisson law with mean $\Lambda>0$, independent of class and orders.
Assume, for contradiction, that entry equals $\rho$ at every terminal history at $r=3.6$.
Every terminal posterior is then at most $\tau(3.6)$.
Public interim posteriors obey the same cap by conditional expectation.
Constant entry makes the correct purchase residual at least $\rho\Delta[1-\tau(3.6)]>k$.
Thus every fresh high-class arrival buys; no low-class arrival buys.

Choose an integer $n$ with $n\log(1+u)>\log T_2$.
The event $N=n$ has positive probability.
Its all-buy history also has positive probability and posterior odds $(1+u)^n>T_2$.
That history requires full entry, which contradicts the assumed floor.
The strict choice of $n$ removes all challenger tie issues.
Therefore entry exceeds $\rho$ for every $\Lambda>0$ and fixed $u>0$.

At calibration A, the $N=2$ event gives an explicit bound.
Its first and second purchase margins are positive under every continuation strategy.
Both low-class purchase deviations lose.
Thus the two buys give

$$
\mu_{++}=841/962,\qquad
\Pr(+,+\mid N=2)=\frac12\left[(29/51)^2+(11/51)^2\right]=481/2601.
$$

Hence

$$
\mathsf E(3.6)\ge\frac14+\frac34 e^{-\Lambda}\frac{\Lambda^2}{2}\frac{481}{2601}.
$$

At $\Lambda=1/2,1,2$, the bounds are $0.260515472$, $0.275511824$, and $0.287541102$.
The conclusion does not need the final count to be known before the first order.
It needs an exogenous count, its observed termination, and the stated independent arrivals.
The bound is not a uniform positive gap as $\Lambda$ tends to zero or infinity.

## 4. Errors and corrections

1. **Date order is equilibrium-specific.** Keep C4 as an existence result.
   Add the equilibrium $x_H=0$, $x_L\approx0.837634$.
   Qualify the claim that good news arrives early and bad news arrives late.
2. **Menus differ.** C3's buy-only menu has no seller.
   C4's delayed seller belongs to the two-sided menu.
   Use the tighter buy-only likelihood ratio for its separate calibration.
3. **Completeness needs the right scope.** The buy-only access list is complete by exact cell signs.
   The full two-sided date correspondence remains open.
   A grid cannot establish that correspondence.
4. **The exponent is a bound.** Replace “falls like $e^{-0.306n}$” with an explicit upper-bound statement.
   Do not present $0.93$ as a unique coefficient.
5. **The profit percentage needs its denominator.** The 12.8% figure divides the early term by $D(+)$.
   The expected net profit comparison gives 45.5%.
6. **The general impossibility claim exceeds the proof.** Keep the last-date inequality.
   Leave the $n\ge3$ entry correspondence open.
7. **Weak-incumbent proof needs backward induction.** The conclusion of no trade at $r=1.2$ survives.
   The claim that every trade loses under every arbitrary schedule is false.
   At the two-slot full-order schedule, an early buy nets $1037/374400>0$ at $r=1.2$.
   That continuation schedule fails equilibrium because its last-date traders lose.
8. **Date mixtures differ from order-size mixtures.** The reported first-date order $-0.167$ is an expected order.
   Every realized sale has size one.
   State explicitly whether the investor tie convention permits mixtures between profitable dates.

## 5. Plain summary

The one-unit posterior cap holds for every finite number of dates.
It preserves floor entry at 3.6.
The reported early-buyer equilibrium also holds, with entry $91/204$.

The date prediction is not general.
Another equilibrium has a late buyer and mostly early sellers.
Its seller trades early with probability about $0.837634$.
Entry remains $91/204$.
The buy-only access list is complete, as exact signs now show.
The two-sided list is incomplete.

Fresh arrivals require the stated information band.
The coefficient $0.93$ is one admissible choice.
The exponent $0.306$ describes a conservative upper bound, rather than the exact decay rate.

The opening price includes future entry.
The early term is 12.8% of the payoff spread.
The expected net profit increase is 45.5%.
The two-slot middle-strength classification holds, but its general extension remains open.

Poisson arrivals keep entry strictly above the floor at every positive arrival rate.
The stated exact lower bound also holds.
