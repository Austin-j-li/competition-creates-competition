# X_C2 check: two rounds before entry

## 1. Scope

This memo checks five headline claims in `C2_two_rounds.md`.
Each claim gets an independent derivation and an independent calculation.
The independent calculation came first.
Only then did this check read the saved original output records.

The independent files are in `audit/discrete_exploration_2026_10_21/scripts/X_C2_check/`.
The file `check.py` uses exact rational arithmetic for rational inputs.
The file `check2.py` uses fifty digit arithmetic for $b=2$ decimals.
The file `compare.py` only reads the saved original output records.
Outputs are `output.txt`, `output2.txt`, and `compare_output.txt`.

The check covers these items:

- Graded beliefs and coexistence with two discrete-Laplace rounds.
- Benchmark entry with separate investors at three strengths.
- All-or-nothing information with equal three-point noise.
- The exact mixed equilibrium with a retained share.
- The horizon-free posterior ceiling with separate investors.
- Costs, equilibrium concept, off-path beliefs, and tie rules.
- Second-order optimality after each first history.
- Status labels and agreement between memo numbers and saved outputs.

The check does not search for new equilibria beyond each verdict.
It does not re-derive the full retained-share correspondence.
It does not solve uncertain presence or an infinite retained-share game.

### 1.1 Shared setup

The auction inputs are $h=10$, $\ell=1$, $p=1/2$, and $\rho=1/4$.
The prior is $\pi=1/2$ in each numerical example.
Presence is $\lambda=1$ in each round.
Orders satisfy $q_t\in\{0,1\}$.
Each purchased unit costs $k$.

For $0<p<\ell<r<h$, the auction objects are

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&g_H&=h-r/2-p^2/(2r),\\
g_L&=(\ell^2-p^2)/(2r),&\Delta&=t_H-t_L=(r-\ell)^2/(2r).
\end{aligned}
$$

Write $w_j=t_j-t_0$ and $D=\rho\Delta$.
Preparation gain and entry are

$$
B_r(\mu)=g_L+\mu(g_H-g_L),\qquad
e(\mu)=\rho+(1-\rho)\mathbf 1\{B_r(\mu)\ge c_H\}.
$$

The final price at posterior $\mu$ is $P(\mu)=t_0+e(\mu)(w_L+\Delta\mu)$.
The pinned paper gives the same objects in its equation (4).
This check used commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` only.

Independent exact values include:

- At $r=6/5$: $\Delta=1/60$ and $B_r(1/2)=1153/240$.
- At $r=17/10$: $\Delta=49/340$, $w_H=97/170$, and $w_L=29/68$.
- At $r=3$: $\Delta=2/3$, $w_H=9/8$, $w_L=11/24$, and $D=1/6$.
- At $r=18/5$: $\Delta=169/180$ and $B_r(1/2)=2977/720$.

These values match the original memo where it states them.

### 1.2 Costs

The phrase "original costs" needs one correction.
The original memo uses $c_H=6$ and $k=1/50$ in its $r=1.7$ corollary.
Those two values equal the paper benchmark values.
The memo uses $c_L=0$ throughout.
The paper benchmark uses $c_L=1$.

The main coexistence proposition uses $r=3$ and $k=9/100$.
That trade cost is not the original trade cost.
Only the corollary at $r=17/10$ uses $k=1/50$.
The timing corollary uses $r=3$ and $k=11/100$.

With $c_L=0$, entry has floor $\rho$ at each belief.
With $c_L=1$, that floor can fail near belief zero.
The discrete-Laplace examples never reach belief zero.
At $b=2$, $B_r(m_2)$ is $2.728$, $2.602$, $2.366$, and $2.272$ at $r=1.2,1.7,3,3.6$.
Here $m_2$ is the lowest two-round posterior under full orders.
So the discrete-Laplace numbers coincide under $c_L=1$ on path.
The proofs as written still use the $c_L=0$ floor for each belief.
The three-point results use belief zero on path.
There $B_r(0)=g_L<1$ at $r=3$, so $c_L$ changes the result.

### 1.3 Equilibrium concept and tie rules

The original memo states perfect Bayesian equilibrium.
Prices are competitive conditional means given the flow history.
Investor deviations face fixed candidate price and entry schedules.
Auction bids are truthful.
This concept matches the paper equilibrium idea, extended to two rounds.

An indifferent challenger prepares.
An indifferent investor may mix over optimal orders.
The first rule matches the paper preparation tie rule.
The second rule matters only at stated equalities below.
Strict coexistence and strict benchmark comparisons do not need it.

Discrete-Laplace noise gives each finite flow history positive probability.
Bayes rule then pins each public belief.
Sequential rationality still needs checks at each private history.
Section 3 checks those histories by full plan enumeration.

Equal noise has one unused public flow in the no-trade candidate.
The completion assigns belief one after unused upper flow $2$.
It retains the prior belief after any other unused next flow.
The memo does not claim that a refinement forces this rule.
Uniqueness for equal noise holds under this stated completion.
No tremble sequence in the memo proves sequential equilibrium there.

## 2. Verdict table

| Claim | Verdict | Evidence in one line |
|---|---|---|
| 1. Two discrete-Laplace rounds give graded beliefs and coexistence at $r=1.7$ in both designs | CONFIRMED WITH CORRECTION | Exact gross values and interval bounds hold; costs are $(c_H,k,c_L)=(6,1/50,0)$ |
| 2. Separate investors give entry $0.25\to0.448747\to0.25$ at $r=1.2,3,3.6$ | CONFIRMED | Rational enclosure gives each strict margin; fifty digit entry is $0.4487472158\ldots$ |
| 3. Equal noise with separate investors stays all-or-nothing with no open coexistence interval | CONFIRMED WITH CORRECTION | Threshold proof holds for $k\ne K(\pi)$ under the completion; equality needs an exclusion |
| 4. Retained share gives exact mixed equilibrium with graded bad news and inventory-based orders | CONFIRMED | $\beta=26/81$ gives $\mu_-=55/136$ and zero first-order gain at each feasible history |
| 5. Separate discrete-Laplace investors face a horizon-free posterior ceiling when $k>0$ | CONFIRMED | One-step gross bound and induction give the stated bound for fixed $r$ |

No headline claim is refuted.
No headline claim is not checkable within its stated scope.
Sequential equilibrium for equal noise stays unproven in the memo.
The memo claims only perfect Bayesian equilibrium, so that gap changes no verdict.

## 3. Derivations and evidence

### 3.1 Final prices and purchase residuals

Let $\mu_T$ be the public posterior after the last flow history.
The challenger sees prices, while market makers see flows.
The final competitive price is $P(\mu_T)$ as defined in Section 1.
Function $P$ rises strictly in $\mu$.
Between entry jumps, its slope is $e(\mu)\Delta>0$.
At the entry threshold, $e$ jumps from $\rho$ to $1$.
The bracket $w_L+\Delta\mu$ is positive, so the jump goes up.
Hence the final price reveals $\mu_T$ to the challenger.

An early price must forecast later entry.
It equals $\mathbb E[t_0+e(\mu_T)w_j\mid H_t]$, not $P(\mu_t)$ in general.
The independent enumeration uses this tower rule for $P_1$.
It obtains the same $P_1$ from $\mathbb E[P_2\mid H_1]$.

For separate investors, define $e_H=\mathbb E[e(\mu_T)\mid H,H_t]$.
Define $e_L$ in the same way for class $L$.
Define $D(H_t)=w_He_H-w_Le_L$.
Bayes rule gives $\mathbb E[e(\mu_T)\mu_T\mid H_t]=\mu_te_H$.
It also gives $\mathbb E[e(\mu_T)\mid H_t]=\mu_te_H+(1-\mu_t)e_L$.
Subtraction gives $\operatorname{Cov}(e(\mu_T),\mu_T\mid H_t)=\mu_t(1-\mu_t)(e_H-e_L)$.
Entry $e$ does not fall in belief, so the covariance is at least zero.
Thus $e_H\ge e_L$ at each interior public belief.

It follows that $D(H_t)=\Delta e_H+w_L(e_H-e_L)\ge\rho\Delta$.
It also follows that $D(H_t)\le W$ with $W=w_H-\rho w_L$.
After history $H_t$, the $H$ residual is $(1-\mu_t)D(H_t)$.
The $L$ residual is $-\mu_tD(H_t)$.
Hence an $L$ purchase with no retained share earns at most $-k$.
This step excludes $L$ orders for separate investors.
It also excludes a second $L$ order with zero retained units.

### 3.2 Claim 1: graded beliefs and coexistence

#### Signs and posteriors

Write $a=e^{-1/b}$ with $0<a<1$.
Discrete-Laplace noise has mass $(1-a)(1+a)^{-1}a^{|z|}$.
Call flow $x\ge1$ a plus sign and flow $x\le0$ a minus sign.
Under order one, plus has probability $u=1/(1+a)$.
Under order zero, plus has probability $v=a/(1+a)$.
Thus $u+v=1$ and $u>v$.
The likelihood ratio $f(x-1)/f(x)$ depends only on the sign.
It equals $a^{-1}$ after plus and $a$ after minus.

Suppose each $H$ investor buys and each $L$ investor stops.
Posterior odds start at $\pi/(1-\pi)$.
Each plus multiplies odds by $a^{-1}$.
Each minus multiplies odds by $a$.
At $\pi=1/2$, two rounds give

$$
\mu_2(--)=\frac{a^2}{1+a^2},\quad
\mu_2(+-)=\mu_2(-+)=\frac12,\quad
\mu_2(++)=\frac1{1+a^2}.
$$

At $b=2$, fifty digit values are $0.2689414213\ldots$ and $0.7310585786\ldots$.
These beliefs are graded and stay away from zero and one.
One round already gives graded beliefs $v$ and $u$.
The second round widens the range from $u$ to $1/(1+a^2)$.
That wider top belief creates the new entry and coexistence results.

Exact flow size inside one sign adds no payoff-relevant information here.
Candidate prices in each example depend only on signs.
Future sign laws do not depend on past exact size given the sign.
A size-based second order therefore earns the same as its sign order.
Full sign-plan enumeration covers each payoff-relevant deviation.
Other size-based continuation selections can still add equilibria.
The memo states that limit for its sign-history equations.

#### Gross profits under full orders

Assume only history $++$ recruits costly entry.
Write $M_2=1/(1+a^2)$.
After a minus first sign, final entry stays at $\rho$.
After a plus first sign, final entry is $1$ only after a second plus.
Direct sign enumeration gives second gross profits

$$
C_-=D\left(\frac u2+vM_2\right),\qquad
C_+=\Delta\left[u(1-M_2)+\frac{v\rho}{2}\right].
$$

Continuation spreads after plus and minus are

$$
D_+=D+(1-\rho)(w_Hu-w_Lv),\qquad D_-=D.
$$

First gross profit is therefore

$$
C_1=uv\{2D+(1-\rho)(w_Hu-w_Lv)\}.
$$

The independent enumeration builds posteriors from Bayes rule directly.
It then builds $P_2$, $P_1$, and each purchase mean from those objects.
Differences between enumeration values and the three formulas are zero.
The check ran this comparison at $a=3/5$ with exact fractions.

At $r=3$ and $a=3/5$, exact values are

$$
C_-=\frac5{51},\qquad C_+=\frac{77}{544},\qquad C_1=\frac{1405}{8192}.
$$

At $r=17/10$ and $a=3/5$, exact values are

$$
C_-=\frac{49}{2312},\quad
C_+=\frac{11319}{369920},\quad
C_1=\frac{7167}{139264}.
$$

Both triples match the original memo exactly.
Preparation values at $r=3$ are $B_3(u)=16/3<6<B_3(M_2)$.
Preparation values at $r=17/10$ satisfy the same strict order.
Hence only $++$ recruits costly entry in each full candidate.

#### Interval proof and both designs

No trade keeps each posterior at $1/2$ and entry at $\rho$.
One purchased unit then earns gross profit $\rho\Delta/2$.
At $r=3$, this value is $1/12<9/100$.
At $r=17/10$, this value is $49/2720<1/50$.
A second unit cannot change entry against the fixed no-trade schedule.
Full plan enumeration gives negative best values for each first purchase.
No trade is therefore a strict equilibrium in each design at those costs.

For full orders, each gross value must exceed $k$ on $a\in[3/5,61/100]$.
Bounds $u\ge100/161$, $v\ge3/8$, and $M_2\ge10000/13721$ hold there.
Bound $1-M_2\ge9/34$ also holds there.
Substitution gives exact lower margins at $r=3$, $k=9/100$:

$$
C_--k\ge\frac{4844813}{662724300},\qquad
C_+-k\ge\frac{111361}{2189600}.
$$

Independent bounds reproduce both fractions exactly.
For $C_1$, the memo uses $uv\ge u_{\min}v_{\min}$.
That step gives $C_1-k\ge3291751/41473600>0$.
A tighter bound uses $\min_a a/(1+a)^2$ at $a=3/5$.
It gives a larger margin, so the memo bound is valid but weak.
A fifty part subdivision with exact endpoint bounds also stays positive.

At $r=17/10$, $k=1/50$, exact lower margins include

$$
C_--k\ge\frac{138982}{134122775},\qquad
C_+-k\ge\frac{444569}{42540800}.
$$

Preparation margins are $6-B_{1.7}(u)\ge133/544$ and $B_{1.7}(M_2)-6\ge629647/933028$.
All four fractions match independent exact bounds.
Alternating sums give $29/48<e^{-1/2}<233/384$.
That interval lies inside $[3/5,61/100]$, so $b=2$ belongs to the proof.
Terms $(1/2)^n/n!$ fall to zero, so odd and even sums bracket the limit.

Separate investors need $C_-,C_+,C_1>k$ and $L$ losses.
Enumeration gives negative $L$ gross values after each first sign.
It also gives negative first $L$ gross values in each full candidate.
Full orders therefore form a strict equilibrium for separate investors.

One long-lived investor needs one extra retained-share check.
After a plus sign, a second order raises expected entry.
The entry mean rises by $(u-v)(1-\rho)$ from order zero to order one.
One retained $H$ unit therefore adds $w_H(u-v)(1-\rho)>0$.
After a minus sign, entry stays at $\rho$, so the addition is zero.
Enumeration second increments match this addition exactly at $a=3/5$.
At $r=3$, the addition is $27/128$.
At $r=17/10$, the addition is $291/2720$.

First-order comparison in the retained design must optimize continuations.
Enumeration tries each second sign plan for each first order.
Best $H$ continuation buys after each first sign in each full candidate.
Best $L$ continuation after a first purchase stops after each sign.
The $H$ first-order gain equals $C_1-k+(u-v)(C_+-C_-)$ exactly.
Enumeration minus that formula is zero at $r=3$ and at $r=17/10$.
Both gains are positive on the full $a$ interval.
The $L$ second increment after plus with one unit is negative.
Its exact upper bounds match the memo fractions in each case.
Full orders therefore also form a strict equilibrium with retained shares.

Second orders are optimal after each first sign and each inventory.
For $H$ with zero units, increments equal $C_\pm-k>0$.
For $H$ with one unit, increments add the retained term above.
For $L$ with zero or one unit, each increment is negative.
No public history needs an off-path rule under this noise law.
These discrete-Laplace equilibria satisfy sequential rationality as checked.

#### Why one round fails at the same inputs

One round with $H$ buy probability $\beta$ gives posteriors $\nu_\pm(\beta)$.
The top posterior rises in $\beta$ and reaches at most $u$.
Since $B_r(u)<6$, entry stays at $\rho$ after each one-round sign.
Gross profit then equals $D[u/(1+L_+)+v/(1+L_-)]$.
Here $L_+=1-\beta+\beta/a$ and $L_-=1-\beta+\beta a$.
Algebra gives $2aD/[(2a+\beta(1-a))(2-\beta(1-a))]\le D/2$.
Equality holds only at $\beta=0$.
Since $D/2<k$ in each coexistence example, no mixture can profit.
Exact checks at five $\beta$ values give zero formula differences.
One-round no trade is unique at those inputs, as the memo states.

The timing candidate at $r=3$, $k=11/100$ also checks.
With no second order after minus, second beliefs stay at $v$.
A deviation second purchase after minus earns gross $Du\le5/48<11/100$.
After plus, $C_+-k$ and $C_1-k$ stay positive on the interval.
Retained-design gain equals $C_1-k+(u-v)(C_+-k)$ exactly in enumeration.
Entry stays equal to the full-order entry rate.
Trade timing, cost, and bad-news beliefs differ as the memo states.

All coexistence inequalities are strict inside one entry region.
Gross values and preparation values vary continuously there.
Coexistence therefore holds on an open neighborhood of inputs.
The analytical label fits the derivation with displayed rational bounds.
Readers need exact arithmetic to verify the large fractions.
That need does not create a missing logical step in the proof.

### 3.3 Claim 2: benchmark entry with separate investors

For any horizon $T$, each one-step likelihood ratio lies in $[a,a^{-1}]$.
A flow law given class and history mixes $f(x)$ and $f(x-1)$.
Each mixture weight $(1-\beta)+\beta f(x-1)/f(x)$ lies in one short interval.
The ratio of two such weights therefore lies in $[a,a^{-1}]$.
Multiplication over $T$ rounds bounds total odds by $a^{\pm T}$.
Hidden retained units do not change this marginal flow argument.
Hence $\mu_T\le M_T(\pi)=\pi a^{-T}/(1-\pi+\pi a^{-T})$.
If $B_r(M_T)<c_H$, costly entry cannot occur in any equilibrium.

For separate investors, a last purchase earns at most $\Delta$.
If $\Delta(r_0)<k$, backward induction removes each earlier purchase.
Each earlier gross value is at most $\Delta$ without later information.
At the other end, each $H$ residual is at least $\rho\Delta(1-M_T)$.
At $\pi=1/2$, this lower bound is $\rho m_T\Delta$.
If $k$ lies below it, each $H$ investor buys at each history.
Low-class purchases still lose by the residual sign in Section 3.1.
Trade outcome is then unique without a sign-history restriction.

The benchmark uses $T=2$, $k=1/50$, $c_H=6$, and $c_L=0$.
Alternating sums $S_9$ and $S_{10}$ bracket $e^{-1/2}$.
Exact values are $S_9=112690097/185794560$ and $S_{10}=2253801941/3715891200$.
Both sums lie in $[606530/10^6,606531/10^6]$.
That enclosure gives $M_2\in[0.7310583580\ldots,0.7310590063\ldots]$.
It also gives $m_2\ge3678786409/13678786409$.

Exact margins from that enclosure are:

- $k-\Delta(1.2)=1/300>0$ for unique no trade at $r_0$.
- $\rho m_2\Delta(3)-k=25466650499/1025908980675>0$ for full orders.
- $B_3(M_2)-6\ge7128940591499/32829116495064>0$ for costly entry.
- $6-B_{3.6}(M_2)\ge5289661241/1969745242896>0$ for the ceiling.
- $6-B_{1.2}(1/2)=287/240>0$ for prior entry at floor $\rho$.

Independent exact bounds reproduce each fraction above.
Fifty digit values give $B_{3.6}(M_2)=5.9973110977\ldots<6$.
The ceiling margin is small, near $0.00269$, but enclosure width is far smaller.
Coarse value $a=3/5$ reverses this one inequality at $r=3.6$.
The certificate therefore must use the narrow enclosure, as the memo does.

Under full orders with entry only after $++$, entry and ownership are

$$
\mathsf E_2=\rho+\frac{1-\rho}{2}(u^2+v^2),\qquad
\mathsf O_{H,2}=\frac\rho2+\frac{1-\rho}{2}u^2.
$$

At $b=2$, fifty digit values are $0.4487472158\ldots$ and $0.2702958571\ldots$.
Rounded values $0.448747$ and $0.270296$ in the memo are correct.
At $r_0$, unique no trade gives entry $0.25$ and ownership $0.125$.
At $r_2$, unique full orders give entry $0.25$ and ownership $0.125$.
Trade still occurs at $r_2$, but no belief recruits costly entry.
The computer-assisted label fits this finite rational certificate.

### 3.4 Claim 3: equal noise with separate investors

Let current $H$ buy probability be $\beta$ and $L$ order be zero.
Flow probabilities in one round are

$$
\Pr(x\mid H)=\left(\frac{1-\beta}3,\frac13,\frac13,\frac\beta3\right),\quad
\Pr(x\mid L)=\left(\frac13,\frac13,\frac13,0\right)
$$

for $x=-1,0,1,2$.
Middle flows $0$ and $1$ keep the current belief for each $\beta$.
Upper flow $2$ reveals $H$, with the completion when $\beta=0$.
Lower flow $-1$ reveals $L$ when $\beta=1$.
With mixed $\beta$, lower flow gives belief $\pi(1-\beta)/(1-\pi\beta)$.

In the last round, one purchase reaches flows $0,1,2$ with equal chance.
Its gross profit is $K(\pi)=(2/3)(1-\pi)e(\pi)\Delta$ for each $\beta$.
Flow $2$ contributes zero residual at belief one.
Middle flows each contribute $e(\pi)\Delta(1-\pi)/3$.
Thus last-round orders are pure unless $k=K(\pi)$.

Backward induction extends this threshold to each finite horizon.
A purchase cannot reach lower flow $-1$.
Later play after $-1$ therefore cannot change that purchase value.
Later play after middle flows starts again at belief $\pi$.
If $k>K(\pi)$, later play after middle flows has no trade by induction.
Current gross profit stays at $K(\pi)$, so zero is uniquely optimal.
If $k<K(\pi)$, later play after middle flows stays active by induction.
With $n$ later rounds, no revelation has chance $s^n$ with $s=2/3$.
Continuation spread is $D_n=s^ne(\pi)\Delta+(1-s^n)[e(1)w_H-e(0)w_L]$.
Difference $D_n-e(\pi)\Delta$ is at least zero by entry monotonicity.
Current gross profit $s(1-\pi)D_n$ is then at least $K(\pi)>k$.
Full purchase is uniquely optimal before revelation in that case.

Equilibrium posteriors for $k\ne K(\pi)$ are only $0$, $\pi$, and $1$.
At $k=K(\pi)$, mixed orders can add graded belief after flow $-1$.
The memo proposition excludes that equality from uniqueness.
Its failure paragraph needs the same exclusion in plain words.
Coexistence can occur only on the equality set $k=K(\pi)$.
Spread $\Delta(r)$ rises strictly for $r>\ell$.
Entry $e_r(\pi)$ takes only values $\rho$ and $1$.
Equality in $r$ at fixed $k$ therefore holds only at isolated points.
No open interval of coexistence exists in $k$ or in $r$.

Assume $B_r(\pi)<c_H\le g_H$, so $e(0)=e(\pi)=\rho$ and $e(1)=1$.
Active entry, ownership, and expected purchases given $H$ are

$$
\rho+(1-\rho)\pi(1-s^T),\quad
\pi\rho+(1-\rho)\pi(1-s^T),\quad
3(1-s^T).
$$

At $\pi=1/2$ and $T=2$, values are $11/24$, $1/3$, and $5/3$.
Independent enumeration at $r=3$ reproduces each value exactly.
Price without revelation after one of two rounds is $145/192$.
Final price without revelation is $59/96$.
Belief stays at $1/2$, while lost future entry lowers the price.
Costly entry needs belief one, so it lasts while $g_H(r)\ge c_H$.
Equation $g_H(r)=6$ gives $r^2-8r+1/4=0$ at benchmark inputs.
Relevant root is $4+\sqrt{63/4}=7.9686269665\ldots$.
Rounded memo value $7.96862697$ is correct.

Second-order optimality needs one off-path amendment in words.
Consider active orders and private history $(H,x_1=-1)$ for a new investor.
That history has probability zero given $H$ under active first orders.
Public belief is zero, while the new investor knows class $H$.
One purchase then earns gross $(2/3)\rho\Delta$ before cost.
At $r=3$, that gross value is $1/9$, which exceeds $k=1/50$ and $k=1/10$.
A rule that stops after each public revelation is not optimal there.
Change that zero-probability order to one without changing prices.
Outcome, entry, and first-order values stay the same after the change.
The same point affects retained-design full orders after a first deviation.
Section 4 lists this correction with exact histories.

### 3.5 Claim 4: retained share and exact mixing

With one long-lived investor, second-order gain at inventory $n$ is

$$
\Gamma_j(n,H_1)=n\{\mathbb E_1V_j-\mathbb E_0V_j\}
+\mathbb E_1[V_j-P_2]-k.
$$

The first term values entry change on units already held.
Separate investors have no such term at their single decision.
Market beliefs must track class and hidden first order jointly.
First values must use the best second order after each first flow.
Independent enumeration tries each feasible second plan in that way.

Use $r=3$, $k=3/20$, and first $H$ mix $\beta=26/81$.
Exact inputs are $\Delta=2/3$, $D=1/6$, $K=1/18$, and $J=9/32$.
Here $J=(1-\rho)w_H/3$ is the retained entry gain after middle flows.
After middle flow $0$ or $1$, belief stays at $1/2$.
Inventory mix inside class $H$ also stays at $\beta$ after middle flows.
Lower belief is $\mu_-=(1-\beta)/(2-\beta)=55/136$.
Final beliefs with positive probability are $55/136$, $1/2$, and $1$.
Bad news is therefore graded, while good costly entry still needs belief one.

After a middle first flow, $\Gamma_H(n)=K+nJ-k$.
Values are $269/1440>0$ at $n=1$ and $-17/180<0$ at $n=0$.
Candidate order buys again exactly when one unit is already held.
After lower flow $-1$, an $H$ investor on path holds zero units.
One purchase there earns gross $9/136<3/20$, so stopping is optimal.
After upper flow $2$, belief is one and one more $H$ purchase earns $-k$.
Each $L$ second increment at a feasible history is negative.
At middle flows with one unit, it equals $-451/1440$.
At upper flow with one unit, it equals $-(\Delta+k)=-49/60$.
With zero units, $L$ gross profit is $-\Delta\mathbb E[e\mu_2]\le0$.

First middle price is $P_1^U=t_0+\rho(w_L+\Delta/2)+\beta J/2=95/144$.
First $H$ value with best continuation is

$$
U_{1H}(1)=\frac53(K-k)+\frac23(1-\beta/2)J=0
$$

at $\beta=26/81$ exactly.
First zero order also earns zero with best continuation.
Mixing at the first order is therefore optimal under the tie rule.
First $L$ purchase with best continuation earns $-989/2160<0$.
Enumeration best plans match candidate orders at each feasible history.
Pair $(n=1,x_1=-1)$ cannot occur, since order one cannot give flow $-1$.
Its mechanical second gain has no decision node and needs no order.

Equilibrium outcomes from enumeration are

$$
\mathsf E=\frac{77}{243},\quad
\mathsf O_H=\frac{373}{1944},\quad
\mathbb E[N_2\mid H]=\frac{130}{243},\quad
\Pi_H=0.
$$

Expected trade cost given $H$ is $13/162$.
Each fraction matches the original memo exactly.
No trade fails at the same inputs in the retained design.
Best two-order deviation from no trade earns $13/432>0$.
That deviation buys first, then buys again after middle flows.
A tie rule that forces zero at each investor tie removes this mixture.
The memo states that dependence correctly.

Full first purchase also checks at $k=1/50$ and $k=1/10$ with retained shares.
Second order buys after middle flows and stops after upper revelation.
At $k=1/10$, standalone second net value is $K-k=-2/45$.
Retained gain $J=9/32$ makes the on-path second order optimal.
Exact enumeration gives first gains $2137/21600$ and $23/1440$.
Entry $11/24$, ownership $1/3$, and profits match Section 3.7 below.
Off-path zero-inventory orders after lower flow need the Section 3.4 amendment.

### 3.6 Claim 5: horizon-free ceiling with separate investors

Fix $r$, $k>0$, and $a\in(0,1)$ under discrete-Laplace noise.
Consider separate investors only in this claim.
At current belief $\mu$, next belief is at least $a\mu/(1-\mu+a\mu)$.
That bound uses smallest one-step likelihood ratio $a$.
Current gross profit is $\mathbb E[(1-\mu')D(H')\mid H,\text{buy}]$.
Bound $D(H')\le W$ and the belief bound give

$$
\text{gross}\le W\frac{1-\mu}{1-\mu+a\mu}.
$$

This bound does not use later orders or remaining horizon.
Positive buy probability needs gross value at least $k$.
When $W>k$, purchase therefore needs $\mu\le\bar\mu$.
Here $\bar\mu=(W-k)/(W-k+ka)$.
Class $L$ never buys with separate investors.
If class $H$ also stops, next flow carries no class information.
Belief then stays fixed in that round.
Each belief rise must start at or below $\bar\mu$.

Largest one-step odds factor is $a^{-1}$.
Next belief after such a rise is at most $(W-k)/(W-k+ka^2)$.
Induction from prior $\pi$ gives

$$
\mu_t\le\max\left\{\pi,\frac{W-k}{W-k+ka^2}\right\}<1
$$

in each finite-horizon equilibrium.
If $W\le k$, the gross bound gives no strictly profitable purchase.
At interior beliefs, the bound lies strictly below $k$ in that case.
The analytical label fits this short complete proof.

At $r=3$, exact spread bound is $W=97/96$.
At $b=2$ and $k=0.02$, the ceiling is $0.9926259985\ldots$.
Rounded memo value $0.992626$ is correct.
This ceiling is far above two-round bound $M_2=0.7310585786\ldots$.
It rules out full revelation through separate equilibrium purchases.
It does not by itself rule out costly entry at $r=3$.
Forced full orders would reveal class as $T$ grows.
Positive cost stops new purchases at high beliefs before that limit.
Retained units add an inventory term, so the bound excludes that design.

### 3.7 Agreement with saved original outputs

Saved original output has $46$ records, with $34$ finite candidates.
Receipt hashes match current memo, calculation, and output files.
Independent values agree with saved records in each checked case.
Exact agreement includes:

- Three-point full entry $11/24$, ownership $1/3$, and units $5/3$.
- Three-point profits $661/4320$ at $k=1/50$ and $17/864$ at $k=1/10$.
- Mixed entry $77/243$, ownership $373/1944$, and first gain zero.
- No-trade deviation $13/432$ at $k=3/20$ with retained shares.
- Discrete-Laplace entry $115/256$ at $a=3/5$ under full orders.
- First gains $16693/204800$ and $109543/3481600$ for separate investors.
- Retained first gains $964943/10444800$ and $2001391/59187200$.
- Interval margins in equations (43) and (47b) of the original memo.
- Benchmark margins, including ceiling gap $5289661241/1969745242896$.

Fifty digit table values also agree after rounding:

- Profit $0.038394$ at $r=1.7$, $k=0.02$, from $0.0383938607\ldots$.
- Profit $0.257263$ at $r=3$, $k=0.02$, from $0.2572628518\ldots$.
- Profit $0.174399$ at $r=3.6$, $k=0.02$, from $0.1743992366\ldots$.
- Profit $0.117263$ at $r=3$, $k=0.09$, from $0.1172628518\ldots$.
- Timing cost $0.178471$ and profit $0.081842$ at $k=0.11$.
- Margins $0.08125985$, $0.05306512$, and $0.00787234$ at $k=0.09$.
- Prices $P_1(-)=0.59417344$ and $P_1(+)=1.01090598$ at $r=3$.
- Prices $0.57607357$, $0.61458333$, and $1.36237239$ in round two.

At $a=3/5$ and $r=3.6$, saved records still give costly entry after $++$.
That coarse value does not prove the $b=2$ benchmark ceiling.
Narrow enclosure records give the correct strict ceiling at $b=2$.
Memo text keeps those two calculations apart correctly.
No memo headline number needs a numerical correction.

Original calculation logic matches independent enumeration on checked cases.
It aggregates discrete-Laplace flows by sign with no tail cut.
It uses exact fractions for rational inputs and decimals for $e^{-1/2}$.
It prints best second orders at each private history.
It prints choice margins only when candidate joint probability is positive.
That last filter hides the off-path order issue in Section 3.4 from margins.
Best-order records still reveal the issue on inspection.

## 4. Errors found and corrections

No error changes a headline entry, ownership, or profit number.
Errors below concern scope words, proof completeness, and off-path orders.

1. **Cost scope in opening claims.** Section 1 says original costs without the $c_L$ change.
   Correct scope is $c_H=6$, $k=1/50$ only in the $r=1.7$ corollary, and $c_L=0$.
   Main proposition cost $k=9/100$ is not an original cost.

2. **Equal-noise equality case.** All-or-nothing words need exclusion $k\ne K(\pi)$.
   At equality, mixing can create graded belief after flow $-1$.
   Coexistence then sits on one equality set, not on an open interval.

3. **Off-path second orders with equal noise.** Stop after public revelation fails at $(H,-1)$.
   That history has zero probability under active $H$ first orders.
   Best order there is one at $r=3$ for $k=1/50$ and $k=1/10$.
   Retained full orders need the same fix after first deviation $(H,0,-1)$.
   Price schedules and outcomes do not change after this fix.

4. **Short induction wording for equal noise.** Proof should name the $\pi$ subgame after middle flows.
   It should state that play after $-1$ cannot affect a current purchase.
   It should also state why equality in $r$ gives no open interval.
   Spread strict increase plus two entry values gives that step.

5. **Mixed-equilibrium proof completeness.** Displayed equations omit two short sign steps.
   Add $L$ zero-inventory gross sign $-\Delta\mathbb E[e\mu_2]\le0$.
   Add feasible-history list, with $(n=1,x_1=-1)$ marked impossible.
   Saved margins already contain the missing exact values.

6. **Sequential equilibrium scope.** Memo proves perfect Bayesian equilibrium as stated.
   Equal-noise sequential consistency has no tremble proof in the memo.
   Discrete-Laplace examples pass sequential rationality checks in this memo.
   Text should keep that distinction explicit near the completion rule.

7. **Small text items.** Odds display has a stray comma in exponent $a^{,t-2N_+}$.
   Correct exponent is $t-2N_+$.
   One-round graded beliefs already exist under discrete-Laplace noise.
   Text should credit round two with wider beliefs, entry, and coexistence.

Status labels need no change for claims 2, 4, and 5.
Claim 1 analytical status stands once cost scope is fixed.
Claim 3 analytical status stands once equality and off-path fixes enter.
Section 4 comparison labels were not part of headline verdicts here.

## 5. What the original memo should change

Make only the small changes below.
No headline number, entry rate, or ownership rate should change.

1. State costs in Section 1 and in each original-cost claim.
   Write $c_H=6$, $k=1/50$ where that pair holds, and $c_L=0$ always.
   Mark $k=9/100$ and $k=11/100$ as changed trade costs.

2. Add $k\ne K(\pi)$ to each all-or-nothing summary sentence.
   State that mixing at equality can grade belief after flow $-1$.
   Keep the no-open-interval claim with the spread monotonicity step.

3. Amend equal-noise second orders at zero-probability private histories.
   Set order one at $(H,-1)$ when $(2/3)\rho\Delta>k$ in active cases.
   State that prices and outcomes stay fixed under that amendment.
   Apply the same rule after retained-design deviation $(H,0,-1)$.

4. Expand two proof paragraphs by a few lines each.
   Name the belief-$\pi$ subgame in the equal-noise induction.
   Add the $L$ zero-inventory sign step in the mixed-equilibrium proof.
   List feasible $(n,x_1)$ pairs and mark $(1,-1)$ as impossible.

5. Clarify equilibrium language near the completion rule.
   Keep perfect Bayesian equilibrium as the stated concept.
   Say that equal-noise sequential consistency stays open without trembles.
   Say that discrete-Laplace histories need no public completion.

6. Fix the exponent typo and one contribution sentence.
   Replace $a^{,t-2N_+}$ with $a^{t-2N_+}$.
   Credit round two with wider beliefs, not with first graded beliefs.

## 6. Plain summary

Two discrete-Laplace rounds do restore wide graded beliefs and coexistence.
At $r=1.7$ with $c_H=6$, $k=0.02$, and $c_L=0$, both investor designs check.
Separate investors also give entry $0.25$, $0.448747$, then $0.25$ as stated.
Equal three-point noise stays all-or-nothing away from one knife-edge cost.
Its proof needs that exclusion and one off-path order fix.
The retained-share mixed equilibrium checks exactly at $\beta=26/81$.
Separate investors face the stated horizon-free belief ceiling for fixed $r$.
No headline number changes.


