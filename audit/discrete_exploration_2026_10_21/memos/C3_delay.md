# C3. An option to delay preparation

## 1. Question

The challenger sees a first price $P_1$.
It can prepare at once.
It can also wait for a second price $P_2$.
Waiting gives more information.
Waiting also discounts the acquisition gain.

This memo asks five questions.

- When does the challenger wait?
- How does waiting change trading incentives?
- Does entry rise or fall?
- Does waiting recover graded beliefs, coexistence, or a ceiling?
- How does incumbent strength $r$ change the value of waiting?

The memo studies both discrete base models.
The first base model uses three-point equal noise.
The second base model uses discrete-Laplace noise.
Orders allow purchases only.
The low preparation cost is zero.

The main findings follow.

- The waiting rule has an exact threshold form.
- The sign of the entry effect depends on the base model.
- Three-point delay raises entry in the benchmark region.
- Discrete-Laplace delay lowers entry at $r_1=3$.
- Discrete-Laplace delay creates entry beyond the one-round ceiling.
- Delay creates coexistence in one discrete-Laplace window.
- Delay creates no coexistence under three-point equal noise.

Check scripts sit in `scripts/C3_delay/`.
The file `c3_three_point.py` uses exact fractions.
The file `c3_dlaplace.py` uses 50-digit arithmetic.
The file `c3_welfare.py` prints profits and proceeds.
Each script prints results only.

## 2. Setup

### 2.1 Paper objects and team choices

Paper references use commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
Sections 2 to 4 of the paper supply the auction objects.
The incumbent value is $R\sim U[0,r]$.
The reserve is $p$.
The domain is $0<p<\ell<r<h$.

The team objects are as follows.

$$
\begin{aligned}
t_0&=p(1-p/r), &
t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r), &
g_H&=h-r/2-p^2/(2r),\\
g_L&=(\ell^2-p^2)/(2r), &
\Delta_T&=(r-\ell)^2/(2r).
\end{aligned}
$$

Put $w_L=t_L-t_0$ and $w_H=t_H-t_0$.
Put $S_r=g_H-g_L$.
The split identity gives $S_r=(h-\ell)-\Delta_T$.
At belief $\mu=\Pr(H)$, the expected gain is $B_r(\mu)$.
The formula is $B_r(\mu)=g_L+\mu S_r$.
Both $g_H$ and $g_L$ fall in $r$.
The spread $\Delta_T$ rises in $r$.

Reading N holds in this memo.
Nature draws class $j\in\{H,L\}$.
The benchmark prior is $\pi=1/2$.
The benchmark values are point masses at $\ell$ and $h$.
Formulas in $\mu_1$ allow a general prior.
Section 4 notes the distribution-value extension.

The challenger cost is $c_L=0$ with probability $\rho$.
The cost is $c_H>0$ with probability $1-\rho$.
Cost and class stay independent.
The trading cost is $k>0$ per purchased unit.
The symbol $\lambda$ means investor presence only.
The leading case sets $\lambda=1$ in each round.

Benchmark auction values follow.

- $h=10$, $\ell=1$, and $p=0.5$.
- $\rho=0.25$ and $k=0.02$.
- Three-point calculations use $c_H=6$.
- Discrete-Laplace calculations use $c_H=5$ and $b=2$.
- The paper strengths are $r_0=1.2$, $r_1=3$, and $r_2=3.6$.

The value $c_H=5$ needs a comment.
The brief candidate for discrete-Laplace noise uses $c_H=5$.
Section 3.4 checks that candidate again.
With $c_H=6$, one good price cannot recruit entry at $r_1$.
Delay then needs $\delta>0.965$ at $r_1$.

### 2.2 Timing with two trading rounds

The sale date stays fixed.
The seller commits to the second-price sale first.
Trading then has two rounds.
The auction closes the game.

The sequence is as follows.

1. Nature draws the class and the incumbent value.
2. Round 1 trading occurs.
3. Market makers set price $P_1$ from flow $X_1$.
4. The challenger sees $P_1$ and learns its cost.
5. The low-cost challenger prepares at once.
6. The high-cost challenger chooses now, wait, or exit.
7. Round 2 trading occurs with fresh noise.
8. Market makers set price $P_2$ from flows $X_1,X_2$.
9. A waiting challenger sees $P_2$.
10. It then prepares late or exits.
11. Prepared bidders bid truthfully in the sale.

Early preparation is a commitment.
It does not move the sale date.
Exit also is a commitment.
A challenger that exits cannot return after $P_2$.
Round 2 trading occurs in every branch.
The claim $V_T$ still trades after an early decision.

Each round has a fresh informed investor.
Each investor starts with zero shares.
Each investor sees the class.
The round 2 investor also sees public price $P_1$.
Each investor chooses $q_t\in\{0,1\}$.
Its payoff is $q_t(V_T-P_t)-kq_t$.

Fresh investors isolate the delay option.
One investor with two orders would hold a stake.
That stake adds a separate manipulation motive.
Workstreams C2 and C5 study that motive.
Section 6 lists the stake case as open.

Noise draws $Z_1,Z_2$ stay independent.
Flow in round $t$ is $X_t=q_t+Z_t$.
Market makers see flows, not orders.
The challenger sees prices, not flows.
Beliefs are $\mu_1=\Pr(H\mid X_1)$.
Beliefs after round 2 are $\mu_{12}=\Pr(H\mid X_1,X_2)$.
Prices are $P_1=\mathbb E[V_T\mid X_1]$.
Prices are $P_2=\mathbb E[V_T\mid X_1,X_2]$.

### 2.3 Waiting cost: discounted gain

Waiting discounts the gross acquisition gain.
The factor is $\delta\in(0,1)$.
Early preparation at belief $\mu$ pays $B_r(\mu)-c_H$.
Late preparation at belief $\mu_{12}$ pays $\delta B_r(\mu_{12})-c_H$.
The cost $c_H$ stays in current units.
Diligence capacity must stay open during the wait.
The integration gain arrives later.

Truthful bidding survives this discount.
After late preparation, profit is $\delta(\theta-\text{payment})$.
The positive factor $\delta$ does not change the best bid.
Target proceeds after late entry stay $t_H$ or $t_L$.
Only the preparation threshold changes.

The early threshold belief is $\tau(r)$.
The late threshold belief is $\tau_\delta(r)$.
The formulas follow.

$$
\tau(r)=\frac{c_H-g_L}{S_r},
\qquad
\tau_\delta(r)=\frac{c_H/\delta-g_L}{S_r}.
$$

Late entry needs a strictly higher belief.
The gap grows as $\delta$ falls.
Late entry is impossible when $\delta B_r(1)<c_H$ in finite models.
In discrete-Laplace noise, $B_r(1)$ reads $B_r(M_2)$ after two rounds.

The other waiting cost is preemption risk.
Under preemption, the sale survives with probability $1-s$.
Late payoff then is $(1-s)$ times a familiar option value.
The late threshold stays at $\tau(r)$.
Target proceeds after preemption equal $t_0$ in expectation.
Prices then carry a survival factor on waiting branches.
Entry after two good prices would rise relative to discounting.
Ceilings would use $B_r(M_2)=c_H$, not $\delta B_r(M_2)=c_H$.
Preemption risk can also respond to the price.
That response belongs to incumbent preemption, workstream C7.
Discounting keeps the sale rule fixed.
This memo therefore uses discounting.

A net-discount variant gives $\delta(B_r(\mu_{12})-c_H)$.
Its late threshold also stays at $\tau(r)$.
Its waiting value is $\delta\,\mathbb E[(B_r(\mu_{12})-c_H)_+\mid\mu_1]$.
That variant enlarges every waiting region.
Gross discounting is the conservative choice.
Sign results in Section 3 use $\tau_\delta$ explicitly.

### 2.4 Equilibrium, beliefs, and tie rules

The equilibrium concept is perfect Bayesian equilibrium.
Investor orders can mix.
Market makers price competitively at each history.
The challenger acts sequentially after each price.
Deviations hold price functions fixed.
Cross-economy comparisons resolve prices in each economy.

Canonical schedules price each belief separately.
Section 3.1 proves price sufficiency on those schedules.
The floor $c_L=0$ gives entry at least $\rho$.
Positive entry keeps price denominators positive.
Zero-entry pools cannot occur under this floor.

Three-point noise has one off-path flow.
Flow $2$ is off path when a round has no purchases.
The belief rule attributes flow $2$ to class $H$.
The price and entry then follow belief $1$.
Prior memos call this rule the directional completion.
Full-purchase histories need no off-path rule.

Discrete-Laplace noise has full integer support.
Every flow has positive probability under every strategy.
Bayes rule then fixes every belief.
No refinement is necessary.

Tie rules are as follows.

- An indifferent investor chooses $q_t=0$.
- The memo also notes mixtures at exact indifference.
- An indifferent challenger prepares now when $B_r(\mu_1)=c_H$.
- An indifferent waiting challenger prepares late when $\delta B_r(\mu_{12})=c_H$.
- Waiting requires a strict gain over now and exit.
- Entry $\mathsf E$ means the preparation probability.
- Ownership $\mathsf O_H$ means $\Pr(H,\text{entry})$.

The strict waiting rule matters only at boundaries.
Interior results use strict inequalities.
Boundary entry follows the preparation-at-indifference rule.

### 2.5 The two noise laws

Three-point noise is $Z\in\{-1,0,1\}$.
Each value has probability $1/3$.
Flows lie in $\{-1,0,1,2\}$ under buy-only orders.

Discrete-Laplace noise is $Z=G_1-G_2$.
Counts $G_i$ are independent geometric variables.
The law is $\Pr(Z=z)=(1-a)/(1+a)\cdot a^{|z|}$.
The parameter is $a=e^{-1/b}$ with $b=2$.
One round then gives two posterior values.
Section 3.4 derives those values again.

The memo modifies each base model in turn.
Three-point noise gives exact rational results.
Discrete-Laplace noise gives graded two-round beliefs.
The contrast between them is a main result.

## 3. Results

### 3.1 General pricing and the waiting rule

**Result 1 — analytical: second price, residuals, and waiting.**

Fix $r$ and continuation strategies.
Let $e_2(\mu_1,\mu_{12})$ denote eventual entry.
The average runs over challenger costs.
By branch, the entry rate is as follows.

- Enter now at $\mu_1$: $e_2=1$.
- Exit at $\mu_1$: $e_2=\rho$.
- Wait at $\mu_1$: $e_2=\rho+(1-\rho)\mathbf 1\{\delta B_r(\mu_{12})\ge c_H\}$.

The low-cost challenger always enters.
Its entry explains the floor $\rho$ in each branch.

Conditional on $(X_1,X_2)$, entry depends only on beliefs.
Target value then satisfies two identities.

$$
\begin{aligned}
\mathbb E[V_T\mid\theta,X_1,X_2]
&=t_0+e_2(\mu_1,\mu_{12})(t_\theta-t_0),\\
P_2(\mu_1,\mu_{12})
&=t_0+e_2(\mu_1,\mu_{12})(w_L+\Delta_T\mu_{12}).
\end{aligned}
$$

Subtraction gives round 2 residuals.

$$
\begin{aligned}
\mathbb E[V_T\mid H,X_1,X_2]-P_2
&=e_2\Delta_T(1-\mu_{12})\ge 0,\\
\mathbb E[V_T\mid L,X_1,X_2]-P_2
&=-e_2\Delta_T\mu_{12}\le 0.
\end{aligned}
$$

A purchase by the $L$ investor pays at most $-k$.
Zero pays zero.
Hence the $L$ investor never buys in round 2.
The same argument covers every belief in $[0,1]$.

For fixed $\mu_1$, entry $e_2$ is nondecreasing in $\mu_{12}$.
For $\mu'>\mu$, the price difference is positive.

$$
P_2(\mu')-P_2(\mu)
=e_2(\mu')\Delta_T(\mu'-\mu)
+[e_2(\mu')-e_2(\mu)](w_L+\Delta_T\mu)>0.
$$

The inequality uses $e_2\ge\rho>0$ and $\Delta_T>0$.
Thus $P_2$ reveals $\mu_{12}$ given $\mu_1$.
This step is the two-round price-sufficiency step.

Round 1 pricing must average future entry.
Define $a_\theta(\mu_1)=\mathbb E[e_2\mid\theta,\mu_1]$.
The expectation runs over round 2 flow.
Then $\mathbb E[V_T\mid\theta,X_1]=t_0+a_\theta(\mu_1)(t_\theta-t_0)$.
Also $P_1=\mu_1\mathbb E[V_T\mid H,X_1]+(1-\mu_1)\mathbb E[V_T\mid L,X_1]$.
Subtraction gives round 1 residuals.

$$
\boxed{
\begin{aligned}
R^1_H(\mu_1)
&=(1-\mu_1)\big[\Delta_T a_H(\mu_1)
+w_L\big(a_H(\mu_1)-a_L(\mu_1)\big)\big],\\
R^1_L(\mu_1)
&=-\mu_1\big[\Delta_T a_H(\mu_1)
+w_L\big(a_H(\mu_1)-a_L(\mu_1)\big)\big].
\end{aligned}}
$$

Entry $e_2$ is nondecreasing in second flow.
Couple both classes to the same noise draw.
Class $H$ buys weakly more, so its flow is weakly higher.
Class $H$ then gives weakly higher expected entry.
Hence $a_H(\mu_1)\ge a_L(\mu_1)\ge\rho$.
The bracket stays strictly positive.
Hence the $L$ investor never buys in round 1 either.
Write $\beta_1$ for the $H$ purchase probability in round 1.
Write $\beta_2(\mu_1)$ for the $H$ purchase probability in round 2.
All $L$ purchase probabilities equal zero.

The $w_L$ term is new in round 1.
Without delay, entry given $X_1$ does not depend on $\theta$.
Then $a_H=a_L=e_r(\mu_1)$ and $w_L$ cancels.
With delay, future entry correlates with the class.
The $H$ investor captures part of that correlation.

Comparison with immediate entry gives a sign decomposition.
Let $e_r(\mu_1)$ denote one-round entry at $\mu_1$.
Then one line of algebra gives the difference.

$$
R^1_H(\mu_1)-e_r(\mu_1)\Delta_T(1-\mu_1)
=(1-\mu_1)\big[\Delta_T(a_H-e_r)+w_L(a_H-a_L)\big].
$$

The second term is always nonnegative.
The first term has the sign of $a_H-e_r$.
Delay raises round 1 profit when it creates entry in state $H$.
Delay can lower round 1 profit when it replaces sure entry.
Sections 3.3 and 3.5 give one case each.

Price $P_1$ equals $\mathbb E[P_2\mid X_1]$ by iterated expectations.
Higher $\mu_1$ shifts $\mu_{12}$ up for a fixed round 2 rule.
Branch order across $\mu_1$ needs the explicit formulas below.
Finite belief sets in Sections 3.2 and 3.4 verify $P_1$ order directly.
Canonical $P_1$ values stay distinct in every reported equilibrium.
The challenger therefore recovers $\mu_1$ from $P_1$ in those equilibria.

**Result 2 — analytical: only the high-cost challenger waits.**

At belief $\mu_1$, define three high-cost values.

$$
N(\mu_1)=B_r(\mu_1)-c_H,\qquad
W(\mu_1)=\mathbb E\big[(\delta B_r(\mu_{12})-c_H)_+\mid\mu_1\big].
$$

Exit pays zero.
Waiting is optimal exactly when $W(\mu_1)>\max\{N(\mu_1),0\}$.
Enter now is optimal when $N(\mu_1)\ge W(\mu_1)$ and $N(\mu_1)\ge0$.
Exit covers the remaining case.

Beliefs form a martingale: $\mathbb E[\mu_{12}\mid\mu_1]=\mu_1$.
The gain $B_r$ is affine in belief.
Hence $\mathbb E[B_r(\mu_{12})\mid\mu_1]=B_r(\mu_1)$.
The low-cost value of waiting is $\delta B_r(\mu_1)$.
Immediate entry pays $B_r(\mu_1)>0$.
Since $B_r(\mu)\ge g_L>0$, immediate entry strictly wins.
Only the high-cost challenger has a real option.

If round 2 has no informed trade, then $\mu_{12}=\mu_1$.
Waiting then pays $(\delta B_r(\mu_1)-c_H)_+$.
That value never exceeds $\max\{N(\mu_1),0\}$.
Waiting therefore needs an informative second round.
For a fixed second-round experiment, $W$ is convex in $\mu_1$.
Convexity follows because $W$ is a Bayesian option value.
The difference $W-N$ is then convex because $N$ is affine.
Sections below verify interval form from explicit formulas.

### 3.2 Three-point noise: beliefs and the exact waiting region

**Result 3 — analytical: three-point two-round beliefs.**

Fix round purchase probabilities $\beta_1,\beta_2(\mu_1)$ for class $H$.
Class $L$ never buys by Result 1.
One round gives flows $-1,0,1,2$.
Interior flows $0,1$ have probability $1/3$ in each class.
They never move beliefs.
Flow $2$ reveals $H$ when the purchase probability is positive.
Flow $-1$ moves beliefs down by odds factor $1-\beta$.

Given $\mu_1$ and $b_2=\beta_2(\mu_1)>0$, round 2 gives three beliefs.

- Flow $2$: belief $1$, with probability $\mu_1 b_2/3$.
- Flows $0,1$: belief $\mu_1$, with probability $2/3$.
- Flow $-1$: belief $\mu^-$, with probability $(1-\mu_1 b_2)/3$.

The low belief is $\mu^-=\mu_1(1-b_2)/(1-\mu_1 b_2)$.
Bayes rule gives each line directly.
Odds multiply by $1-b_2$, $1$, or infinity.
Full purchases $b_2=1$ give $\mu^-=0$.

With full purchases in both rounds, final beliefs stay coarse.
Round 1 beliefs are $0$, $1/2$, and $1$.
Beliefs $0$ and $1$ absorb further news.
From $1/2$, round 2 again gives $0$, $1/2$, and $1$.
Final beliefs therefore never leave $\{0,1/2,1\}$.
Only revelation probabilities rise.

Under class $H$, one-round revelation has probability $1/3$.
Two-round revelation has probability $1/3+(2/3)(1/3)=5/9$.
Under class $L$, low revelation also rises to $5/9$.
Middle probability falls from $2/3$ to $4/9$.
No new interior belief appears.
Mixed purchases grade only bad news through $\mu^-$.
Good news still jumps straight to belief $1$.

**Result 4 — analytical: exact three-point waiting region.**

Fix $r$, $\delta$, and $b_2>0$.
Assume $0\le\tau(r)\le1$, so $c_H\ge g_L$.
The waiting value at general $\mu_1$ is a three-term sum.

$$
\begin{aligned}
W(\mu_1)
={}&\frac{\mu_1 b_2}{3}(\delta g_H-c_H)_+
+\frac23(\delta B_r(\mu_1)-c_H)_+\\
&+\frac{1-\mu_1 b_2}{3}(\delta B_r(\mu^-)-c_H)_+.
\end{aligned}
$$

Each term matches one belief line in Result 3.
Late entry needs belief at least $\tau_\delta(r)$.
Three cases exhaust the belief line.

Case 1: $\delta g_H\le c_H$.
Then $\tau_\delta(r)\ge1$ and late entry never pays.
Hence $W(\mu_1)=0$ for every $\mu_1<1$.
The challenger never waits.
It enters now exactly when $\mu_1\ge\tau(r)$.

Case 2: $\delta g_H>c_H$ and $0<\mu_1<\tau_\delta(r)$.
Middle and low late terms vanish.
Hence $W(\mu_1)=(\mu_1 b_2/3)(\delta g_H-c_H)>0$.
For $\mu_1<\tau(r)$, waiting beats exit and now.
For $\tau(r)\le\mu_1<\tau_\delta(r)$, compare $W$ with $N$.
Equality $W=N$ gives one candidate cutoff.

$$
\bar\mu_{\text{low}}
=\frac{c_H-g_L}{S_r-b_2(\delta g_H-c_H)/3}.
$$

The denominator stays positive under $c_H\ge g_L$.
Indeed $\delta g_H-c_H\le S_r$ then holds.
Waiting wins below this cutoff in Case 2.
Enter now wins above this cutoff in Case 2.

Case 3: $\mu_1\ge\tau_\delta(r)$.
Middle late entry now pays.
With $b_2=1$, the low belief is $0$ and pays zero.
Equality $W=N$ is then one linear equation.

$$
\frac{\mu_1}{3}(\delta g_H-c_H)
+\frac23\big(\delta B_r(\mu_1)-c_H\big)
=B_r(\mu_1)-c_H.
$$

At $\mu_1=1$, waiting pays $\delta g_H-c_H$.
Enter now pays $g_H-c_H$, which is larger.
Convexity from Result 2 gives one crossing overall.
Collect the three cases into one statement.

$$
\boxed{\text{Wait }\Longleftrightarrow\;
b_2>0,\ \delta>c_H/g_H(r),\ 0<\mu_1<\bar\mu(\delta,r,b_2).}
$$

Here $\bar\mu$ is the unique root of $W(\mu_1)=N(\mu_1)$ in $(\tau(r),1)$.
If $W(\tau_\delta)\le N(\tau_\delta)$, then $\bar\mu=\bar\mu_{\text{low}}$.
Else $\bar\mu$ solves the Case 3 linear equation, with low term added if $b_2<1$.
The test at $\tau_\delta$ is $(\tau_\delta b_2/3)(\delta g_H-c_H)$ against $c_H(1-\delta)/\delta$.
Enter now holds for $\mu_1>\bar\mu$.
Exit holds only at $\mu_1=0$ when $\delta g_H>c_H$.
Any positive belief keeps a revelation chance $\mu_1 b_2/3$.

On the benchmark path, only $\mu_1=1/2$ can wait.
Beliefs $0$ and $1$ absorb news, so waiting pays discount only.
At $\mu_1=1/2$ and $b_2=1$, the value reduces to one term.

$$
W(1/2)=\frac16(\delta g_H(r)-c_H)_+,
\qquad
N(1/2)=B_r(1/2)-c_H.
$$

In the benchmark region $B_r(1/2)<c_H$, waiting beats exit exactly when $\delta>c_H/g_H(r)$.
At $r=3$ and $c_H=6$, the threshold is $144/203\approx0.709$.
Script `c3_three_point.py` prints this fraction exactly.
Values $W(1/2)$ are $0.128$, $0.269$, and $0.339$ at $\delta=0.8,0.9,0.95$.

Upper cutoffs illustrate Case 2 and Case 3.
At $r=3$, $\tau=0.705$ in both cases below.

- $\delta=0.9$: $\tau_\delta=0.785$ and $\bar\mu=0.754$.
- $\delta=0.95$: $\tau_\delta=0.743$ and $\bar\mu=0.822$.

The first cutoff lies in Case 2.
The second cutoff lies in Case 3.
On-path belief $1/2$ lies below both cutoffs.

### 3.3 Three-point noise: equilibrium, entry, and no coexistence

Maintain the benchmark region in this section.

- $B_r(1/2)<c_H$, so entry at the prior is $\rho$.
- $g_L<c_H$, so entry at belief $0$ is $\rho$ under $c_L=0$.
- Prices use canonical schedules.

**Result 5 — analytical: round 2 is the bottleneck.**

Fix $\mu_1$ and $b_2>0$ on a waiting branch.
A round 2 purchase by class $H$ reaches flows $0,1,2$.
Each flow has probability $1/3$ given the purchase.
Beliefs after purchase are $\mu_1,\mu_1,1$.
Gross purchase profit therefore has one formula.

$$
K_2(\mu_1)=\frac23\,e_2(\mu_1,\mu_1)\Delta_T(1-\mu_1).
$$

The top flow contributes zero residual.
Profit does not depend on $b_2$ magnitude.
At $\mu_1=1/2$ in the benchmark region, $e_2=\rho$.
Hence $K_2(1/2)=\rho\Delta_T/3$.
Round 2 full purchases hold exactly when $k<\rho\Delta_T/3$.
No purchases hold exactly when $k\ge\rho\Delta_T/3$.
Mixtures at equality need the conventional tie rule.

Exit and enter-now branches give similar formulas.
Exit gives $e_2=\rho$ at every second belief.
Enter now gives $e_2=1$ at every second belief.
Enter now therefore raises round 2 profit at fixed $\mu_1$.
Waiting gives profit between those two branch values.
In every branch, the floor $\rho$ keeps profit positive.
Round 2 trade never needs the waiting branch itself.
This one-way dependence blocks self-fulfilling pessimism.

**Proposition C3.1 — analytical: three-point delay equilibrium.**

Assume $B_r(1/2)<c_H$ and canonical pricing.
Use the tie rules in Section 2.4.
Then equilibrium trading has three cases.

First, suppose $k\ge\rho\Delta_T(r)/3$.
At $\mu_1=1/2$, enter now pays $N(1/2)<0$.
The branch therefore is wait or exit.
Late entry at belief $1/2$ also fails since $\delta B_r(1/2)<c_H$.
Hence $e_2(1/2,1/2)=\rho$ and $K_2(1/2)=\rho\Delta_T/3\le k$.
On-path round 2 trading at $1/2$ is therefore zero.
Waiting then adds no information at $1/2$.
Round 1 gross collapses to $\rho\Delta_T/3\le k$.
Unique on-path trading is $\beta_1=0$ and $\beta_2(1/2)=0$.
Round 2 actions at absorbing beliefs do not change entry.
Entry equals $\rho$ and ownership equals $\rho/2$.
In the benchmark weak economy, $\Delta_T(r_0)<k$ also holds.

Second, suppose $k<\rho\Delta_T(r)/3$ and $\delta g_H(r)>c_H$.
Then the delay equilibrium has $\beta_1=1$ and $\beta_2(1/2)=1$.
The high-cost challenger waits at $\mu_1=1/2$.
It enters now at $\mu_1=1$ and exits at $\mu_1=0$.
Late entry occurs exactly after $\mu_{12}=1$.
Entry and ownership are as follows.

$$
\boxed{
\mathsf E=\rho+(1-\rho)\frac{5}{18},
\qquad
\mathsf O_H=\frac\rho2+(1-\rho)\frac{5}{18}.}
$$

Third, suppose $k<\rho\Delta_T(r)/3$ and $\delta g_H(r)\le c_H$.
Waiting never pays by Result 4.
Trading stays full in round 1.
Entry equals the one-round value $\rho+(1-\rho)\mathbf 1\{g_H\ge c_H\}/6$.
Ownership equals $\rho/2$ plus the same increment.

Proof of the delay case follows.
Round 2 trades by Result 5 since $k<\rho\Delta_T/3$.
Waiting at $1/2$ pays $(\delta g_H-c_H)/6>0$.
Enter now at $1/2$ pays $B_r(1/2)-c_H<0$.
Hence waiting is optimal at $1/2$.
At $\mu_1=1$, now pays $g_H-c_H$.
Waiting pays $\delta g_H-c_H$, which is smaller.
At $\mu_1=0$, both values stay at most zero.

Round 1 profit needs $a_H$ and $a_L$ at $\mu_1=1/2$.
Late entry rates are $\rho,\rho,1$ at beliefs $0,1/2,1$.
Under $H$, second beliefs are $1/2,1/2,1$ after a purchase path.
Averaging gives $a_H=(1+2\rho)/3$.
Under $L$, second beliefs are $0,1/2,1/2$.
Averaging gives $a_L=\rho$.
Result 1 then gives $R^1_H(1/2)$ directly.

$$
R^1_H(1/2)=\frac{\Delta_T(1+2\rho)+w_L(1-\rho)}{6}.
$$

A round 1 purchase reaches beliefs $1/2,1/2,1$.
Gross round 1 profit is $(2/3)R^1_H(1/2)$.

$$
\boxed{
K_1^{\text{delay}}
=\frac{\Delta_T(1+2\rho)+w_L(1-\rho)}{9}
=\frac{\rho\Delta_T}{3}+\frac{(1-\rho)w_H}{9}.}
$$

The equality uses $w_H=w_L+\Delta_T$.
Delay raises round 1 gross profit by $(1-\rho)w_H/9>0$.
Round 2 gross profit stays $\rho\Delta_T/3$ at $\mu_1=1/2$.
Hence $k<\rho\Delta_T/3$ implies $k<K_1^{\text{delay}}$.
Full round 1 purchases follow.
Profit does not depend on $\beta_1$ magnitude when $\beta_1>0$.
The directional completion gives the same deviation profit at $\beta_1=0$.
No-trade therefore fails in this case.

Entry accounting is direct.
High-cost entry needs $\mu_1=1$ or $(\mu_1=1/2,\mu_{12}=1)$.
Probabilities are $1/6$ and $1/9$.
Their sum is $5/18$.
Low-cost entry always occurs.
All extra entry sits in state $H$.
Entry gain therefore equals ownership gain.

Prices confirm sufficiency at $r=3$.
Second prices are $17/32$, $59/96$, and $37/24$.
They match beliefs $0$, $1/2$, and $1$.
First price at $\mu_1=1/2$ is $145/192\approx0.755$.
One-round middle price is $59/96\approx0.615$.
Delay raises the middle first price.
The rise capitalizes expected future entry.
First prices at $0$ and $1$ stay distinct from $0.755$.

**Corollary — analytical: trade region, steps, and no coexistence.**

Delay does not expand the trade region in $r$.
Round 2 needs $k<\rho\Delta_T(r)/3$.
That condition is $r>r_T$ with $r_T=\mathfrak r(3k/\rho)$.
The root is $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$.
At benchmark values, $r_T\approx1.973$.
Round 1 alone would trade up to $K_1^{\text{delay}}$.
Without round 2 trade, waiting collapses and $K_1^{\text{delay}}$ is irrelevant.
Costs between $\rho\Delta_T/3$ and $K_1^{\text{delay}}$ give unique no trade.

No open coexistence interval exists in this region.
Gross profits do not depend on purchase magnitudes.
Each round has one strict purchase comparison.
The floor $\rho$ fixes round 2 trade without feedback from waiting.
At $k=\rho\Delta_T/3$, conventional mixtures can occur.
That threshold set has empty interior in $k$ or $r$.

Define $r_C(\delta)$ by $g_H(r)=c_H/\delta$.
Define $r_C^D$ by $g_H(r)=c_H$.
Each root is $h-c+\sqrt{(h-c)^2-p^2}$ at the matching $c$.
For $\delta<1$, order is $r_T<r_C(\delta)<r_C^D$ in benchmark cases.
Entry along $r$ then has four plateaus.

- $r\le r_T$: entry $\rho$.
- $r_T<r\le r_C(\delta)$: entry $\rho+(1-\rho)5/18$.
- $r_C(\delta)<r\le r_C^D$: entry $\rho+(1-\rho)/6$.
- $r>r_C^D$: entry $\rho$.

At $c_H=6$ and $\delta=0.95$, roots are $7.334$ and $7.969$.
Delay adds one intermediate step down.
Final return still needs $g_H(r)<c_H$.
The Laplace ceiling $B_r(M)<c_H$ stays unrecovered.
At $r_2=3.6$, delay entry still exceeds $\rho$.

A Proposition 2 analog follows at once.
Take $r_0\le r_T<r_1\le r_C(\delta)<r_C^D<r_2$.
Add $B_{r_0}(1/2)<c_H$ and $k$ between the two $\rho\Delta_T/3$ values.
Entry moves $\rho\to\rho+(1-\rho)5/18\to\rho$.
Ownership moves $\rho/2\to\rho/2+(1-\rho)5/18\to\rho/2$.
The rise exceeds the one-round rise $(1-\rho)/6$.
Conditions hold on an open parameter set by continuity.

Outside the benchmark region, entry can fall with delay.
Take $r=3$, $c_H=4$, and $\delta=0.9$.
Then $B_3(1/2)=103/24$ and $N(1/2)=7/24\approx0.292$.
Waiting pays $289/480\approx0.602$, so waiting wins at $1/2$.
Late entry then needs $\mu_{12}=1$ only.
Eventual entry at $\mu_1=1/2$ falls from $1$ to $1/6$ for high cost.
Total entry falls from $7/8$ without delay to $11/24$ with delay.
Script `c3_three_point.py` prints the two values $N$ and $W$.
Delay screens entry when immediate entry already pays.

### 3.4 Discrete-Laplace noise: one-round check and two-round beliefs

**Result 6 — analytical: two posterior values per round.**

Let $a=e^{-1/b}$ and $b=2$.
Noise satisfies $\Pr(Z=z)\propto a^{|z|}$.
For $x\ge1$, ratio $\Pr(Z=x-1)/\Pr(Z=x)$ equals $1/a$.
For $x\le0$, the ratio equals $a$.
Call $x\ge1$ good news and $x\le0$ bad news.

With $H$ purchase probability $\beta$ and prior $1/2$, likelihood ratios follow.

$$
L^+(\beta)=1-\beta+\beta/a,\qquad
L^-(\beta)=1-\beta+\beta a.
$$

Posteriors are $\mu^+(\beta)=L^+/(1+L^+)$ and $\mu^-(\beta)=L^-/(1+L^-)$.
Full purchases give $M_1=1/(1+a)$ and $m_1=a/(1+a)$.
Numerically $m_1\approx0.378$ and $M_1\approx0.622$.
Good news has probability $M_1$ under $H$ full purchases.
Good news has probability $m_1$ under $L$ with no purchases.
Unconditional good-news probability equals $1/2$ exactly.

One-round gross purchase profit at strategy $\beta$ is as follows.

$$
K(\beta)=\Delta_T\left[
\frac{M_1 e_r(\mu^+(\beta))}{1+L^+(\beta)}
+\frac{m_1 e_r(\mu^-(\beta))}{1+L^-(\beta)}
\right].
$$

A purchase reaches good news with probability $M_1$.
A purchase reaches bad news with probability $m_1$.
Residuals use $1-\mu^+=1/(1+L^+)$ and $1-\mu^-=1/(1+L^-)$.
At $\beta=0$, profit is $\bar e\Delta_T/2$ with $\bar e=e_r(1/2)$.
At $\beta=1$, profit is $\Delta_T m_1M_1[e_r(M_1)+e_r(m_1)]$.

Define $H(\beta)=M_1/(1+L^+)+m_1/(1+L^-)$.
Differentiation gives $H'(\beta)\le0$ on $[0,1]$.
The sign step reduces to one identity.

$$
a\big(1+L^+(\beta)\big)-\big(1+L^-(\beta)\big)
=2(1-a)(\beta-1)\le0.
$$

Hence $H$ falls from $1/2$ to $2m_1M_1$.
Since entry rates lie at or above $\rho$, one bound follows.

$$
K(\beta)\ge \rho\Delta_T H(\beta)\ge 2\rho\Delta_T m_1M_1.
$$

Full purchases are unique when $k<2\rho\Delta_T m_1M_1$.
Every candidate $\beta<1$ then fails the purchase comparison.
The candidate bound $\rho m_1\Delta_T$ is weaker and also suffices.
No trade is unique when $\Delta_T<k$ by the two-step argument below.

Self-check at $c_H=5$ confirms the brief candidate arithmetic.
Script `c3_dlaplace.py` prints $m_1=0.377541$ and $M_1=0.622459$.
It prints $B_{1.2}(1/2)=4.804167$ and $B_3(M_1)=5.312161$.
It prints $\rho m_1\Delta_T(3)=0.062923$.
Full-purchase net profit at $r_1$ is $0.175836$ with recruited entry.
Net profit with entry fixed at $\rho$ is $0.058335$.
The brief value $+0.060$ therefore reads $+0.058$ after rounding.
Entry $0.625$ and ownership $0.358422$ at $r_1$ also reproduce.
Uniqueness at $k=0.02$ follows from bounds in Section 3.5.
Workstream B still owns the full one-round correspondence.

Two full rounds multiply odds twice.
Each round multiplies odds by $1/a$ or $a$.
Products are $1/a^2$, $1$, and $a^2$.
Final beliefs are $M_2$, $1/2$, and $m_2$.

$$
M_2=\frac{1}{1+a^2}\approx0.731,\qquad
m_2=\frac{a^2}{1+a^2}\approx0.269.
$$

Histories $GG$, mixed, and $BB$ give those beliefs.
Probabilities are $\Pr(GG)=(M_1^2+m_1^2)/2\approx0.265$.
Mixed histories have probability $2m_1M_1\approx0.470$.
Belief bounds widen from $[0.378,0.622]$ to $[0.269,0.731]$.
One extra round therefore grades beliefs by one step.
Mixed $\beta$ gives intermediate two-value posteriors each round.
Four history beliefs can then be distinct before odds collapse cases.

**Result 7 — analytical: discrete-Laplace waiting values.**

Fix prior belief $\mu_1$ for round 2 and full round 2 purchases.
Good second news has probability $q^+(\mu_1)=\mu_1M_1+(1-\mu_1)m_1$.
Posteriors $\mu^+(\mu_1)$ and $\mu^-(\mu_1)$ come from odds $/a$ and $\times a$.
Waiting pays a two-term sum.

$$
W(\mu_1)=q^+(\mu_1)(\delta B_r(\mu^+)-c_H)_+
+(1-q^+(\mu_1))(\delta B_r(\mu^-)-c_H)_+.
$$

Waiting holds exactly when $W(\mu_1)>\max\{N(\mu_1),0\}$.
This formula is the exact waiting region in $(\mu_1,\delta,r)$.
On the full-purchase path, $\mu_1$ takes only $m_1$ and $M_1$.
Values at those beliefs follow.

$$
\begin{aligned}
W(M_1)&=P_G(\delta B_r(M_2)-c_H)_+
+(1-P_G)(\delta B_r(1/2)-c_H)_+,\\
W(m_1)&=2m_1M_1(\delta B_r(1/2)-c_H)_+
+(1-2m_1M_1)(\delta B_r(m_2)-c_H)_+,
\end{aligned}
$$

Here $P_G=M_1^2+m_1^2\approx0.530$ is $\Pr(\text{good}_2\mid M_1)$.
In the candidate region, $\delta B_r(1/2)<c_H$ at $r_1$.
Hence $W(m_1)=0$ and $W(M_1)=P_G(\delta B_r(M_2)-c_H)_+$.
Waiting after bad first news never pays there.
One good second price only restores belief $1/2$.

At $M_1$ with $N(M_1)\ge0$, equality $W=N$ gives a discount threshold.

$$
\boxed{
\delta^*(r)=
\frac{c_H+\big(B_r(M_1)-c_H\big)/P_G}{B_r(M_2)}.}
$$

Waiting at $M_1$ holds exactly when $\delta>\delta^*(r)$.
At $r=3$ and $c_H=5$, threshold $\delta^*$ is $0.898963$.
Script `c3_dlaplace.py` prints $W(M_1)=0.316$ at $\delta=0.9$.
Immediate entry pays $N(M_1)=0.312$ there.
The margin at $\delta=0.9$ is only $0.003$.
At $\delta=0.95$, waiting pays $0.480$ and wins clearly.
This memo uses $\delta=0.95$ as the main delay example.

At $M_1$ with $N(M_1)<0$, waiting compares with exit.
The threshold then is $\delta_0(r)=c_H/B_r(M_2)$.
Waiting holds exactly when $\delta>\delta_0(r)$.
Thresholds $\delta^*$ and $\delta_0$ meet when $B_r(M_1)=c_H$.
Section 3.7 traces both thresholds in $r$.

### 3.5 Discrete-Laplace noise: delay equilibrium and entry

**Proposition C3.2 — numerical diagnostic at benchmark values, analytical given full purchases: discrete-Laplace delay.**

Use $c_H=5$, $b=2$, $k=0.02$, and $\delta=0.95$.
Formulas below are analytical given full purchases.
Benchmark inequalities come from script `c3_dlaplace.py` at 50 digits.

Part (i): weak incumbent $r_0=1.2$.
Here $\Delta_T(r_0)=1/60<k$.
Round 2 gross profit never exceeds $\Delta_T$.
Hence round 2 never trades in any branch.
Waiting then adds no information.
Round 1 gross profit also never exceeds $\Delta_T$ after that step.
Unique on-path trading is no purchases in both rounds.
Entry is $\rho$ because $B_{r_0}(1/2)=4.804<5$.

Part (ii): strong incumbent $r_1=3$.
Full purchases in both rounds form an equilibrium.
The high-cost challenger waits after good first news.
It exits after bad first news.
Late entry occurs exactly after history $GG$.
Entry and ownership follow.

$$
\boxed{
\mathsf E=\rho+(1-\rho)\Pr(GG)\approx0.449,
\qquad
\mathsf O_H=\frac\rho2+(1-\rho)\Pr(H,GG)\approx0.270.}
$$

Without delay, entry is $0.625$ and ownership is $0.358$.
Delay therefore lowers entry at $r_1$ in this base model.
Screening improves because $\Pr(H\mid GG)=M_2\approx0.731$.
One good price alone gives $\Pr(H\mid G)=M_1\approx0.622$.

Part (iii): stronger incumbent $r_2=6$.
Here $\delta B_{r_2}(M_2)<c_H$ and $B_{r_2}(M_1)<c_H$.
High-cost entry never pays now or late.
Trading stays full by the same bounds scaled by $\Delta_T(6)$.
Those bounds exceed the $r_1$ bounds below.
Entry returns to $\rho$ and ownership returns to $\rho/2$.
The three economies give a Proposition 2 analog.
The rise is smaller than without delay.
The return is later than without delay.

Proof details at $r_1$ follow.
Waiting after $G$ pays $W(M_1)\approx0.480$.
Enter now after $G$ pays $N(M_1)\approx0.312$.
Waiting wins by Result 7 since $0.95>0.899$.
After $B$, waiting pays $0$ and now pays $-1.729$.
Exit wins after $B$.
Late entry rates are $1$ after $GG$ and $\rho$ after $GB$ or $BB$ histories.
Entry accounting uses $\Pr(GG)\approx0.265$.
High-cost entry falls from $0.500$ to $0.265$.

Round 2 gross profits at full purchases are as follows.

- At $M_1$ on wait branch: $0.143$.
- At $M_1$ on enter-now branch: $0.237$.
- At $m_1$ on exit branch: $0.098$.

Each value exceeds $k=0.02$ by a wide margin.
Waiting lowers round 2 profit relative to locked entry.
Bad second news then drops entry from $1$ to $\rho$.
Waiting still leaves feedback after good second news.
Good second news raises entry from $\rho$ to $1$ on wait branches.

Round 1 values use $a_H(M_1)$ and $a_L(M_1)$.
Under $H$, expected entry after $G$ is $a_H\approx0.717$.
Under $L$, expected entry after $G$ is $a_L\approx0.533$.
Immediate entry after $G$ would give entry rate $1$.
Result 1 decomposition therefore has a negative first term.
Residual after $G$ falls from $0.252$ to $0.212$.
Gross round 1 profit falls from $0.196$ to $0.171$.
Delay lowers round 1 profit in this base model.
Profit stays far above $k$, so full purchases survive.

Prices verify sufficiency in this equilibrium.
Second prices are $1.362$, $0.615$, and $0.576$.
They match beliefs $M_2$, $1/2$, and $m_2$.
First prices are $P_1(M_1)\approx1.011$ and $P_1(m_1)\approx0.594$.
One-round good price is $1.290$.
Delay lowers the good first price.
Future entry after $G$ is no longer certain.
Bad first price equals its one-round value by affinity.

Uniqueness at $k=0.02$ has grid support.
One-round $K(\beta)$ has grid minimum $0.079$ at $r_1$.
Round 1 delay profit has lower bound $2\rho\Delta_Tm_1M_1\approx0.078$.
Round 2 lower bounds $\rho\Delta_T\min_\beta\mathbb E_{\text{buy}}[1-\mu_{12}]$ follow.

- Prior $m_1$: bound $0.098$.
- Prior $1/2$: bound $0.078$.
- Prior $M_1$: bound $0.059$.

Each bound exceeds $k$ by factor at least $2.9$.
Residual bounds fall in prior belief at fixed $\beta_2$.
The $M_1$ bound therefore covers every on-path prior at most $M_1$.
Grids use $2001$ points for $K$ and $1001$ points for round 2 bounds.
This memo labels full uniqueness a numerical diagnostic.
Existence needs only the $\beta=1$ inequalities above.

If $\delta<\delta^*(r_1)$, delay stays unused at $r_1$.
The challenger enters now after $G$ and exits after $B$.
Entry and round 1 profit match one-round values.
Round 2 trading still occurs but cannot change entry.
At $\delta=\delta^*(r_1)$, the tie rule selects enter now.

Delay creates entry beyond the one-round ceiling.
One-round ceiling $r_{C1}$ solves $B_r(M_1)=5$.
Bisection gives $r_{C1}\approx3.986$.
Delay ceiling $r_{C2}(\delta)$ solves $\delta B_r(M_2)=5$.
Bisection gives $4.807$ at $\delta=0.9$ and $5.606$ at $\delta=0.95$.
At $r=4.2$, one-round high-cost entry is zero.
Delay entry there is $0.449$ in total at $\delta=0.95$.
The finite ceiling logic survives with $M_2$ in place of $M_1$.
One delay shifts the ceiling outward.
Many delays would move bounds toward $0$ and $1$.

The entry-creation window at fixed $r=3$ is exact in form.
Delay creates high-cost entry when $B_r(M_1)<c_H\le\delta B_r(M_2)$.
The window is nonempty exactly when $\delta>B_r(M_1)/B_r(M_2)$.
At $r=3$, that ratio is $0.854$.
At $\delta=0.95$, the window is $(5.312,5.906]$.
Candidate $c_H=5$ lies below this window.
Example $c_H=5.5$ in Section 3.6 lies inside it.

### 3.6 Coexistence: a documented contrast

**Result 8 — analytical: no feedback without recruited entry.**

Suppose $B_r(M_1)<c_H$ in the one-round discrete-Laplace model.
Then $e_r(\mu^+(\beta))=e_r(\mu^-(\beta))=\rho$ for every $\beta$.
Gross profit is $K(\beta)=\rho\Delta_T H(\beta)$.
Result 6 shows $H$ falls in $\beta$.
Hence $K(\beta)\le K(0)=\rho\Delta_T/2$ for every $\beta$.
If $k>\rho\Delta_T/2$, no-trade is the unique one-round outcome.
Mixed outcomes also fail because $K(\beta)<k$ everywhere.

**Result 9 — numerical diagnostic: delay creates coexistence.**

Take $r=3$, $c_H=5.5$, $\delta=0.95$, and $k=0.09$.
One-round values are $B_3(M_1)=5.312<5.5$.
Also $\rho\Delta_T/2=1/12\approx0.083<0.09$.
Result 8 gives unique one-round no trade.
Script `c3_dlaplace.py` prints $K(0)=0.083$ and $K(1)=0.078$.

With delay, no trade remains an equilibrium.
Set $\beta_1=0$ and $\beta_2=0$.
Belief stays $1/2$ and $B_3(1/2)=4.292<5.5$.
Each round deviation earns gross $\rho\Delta_T/2<k$.
The challenger exits and entry is $\rho$.

With delay, full trade also forms an equilibrium.
Set $\beta_1=1$ and $\beta_2=1$ after each first price.
After $G$, now pays $N(M_1)\approx-0.188$.
Waiting pays $W(M_1)\approx0.215$.
After $B$, waiting pays $0$, so exit holds.
Gross profits are $0.143$, $0.098$, and $0.171$ in round 2 and round 1 checks.
Each gross profit exceeds $k=0.09$.
First prices $1.011$ and $0.594$ stay distinct.
Entry is $0.449$, strictly above $\rho$.

Two equilibria therefore coexist at the same parameters.
One equilibrium has no trade and entry $\rho$.
One equilibrium has full trade, waiting, and entry $0.449$.
Delay creates the informative equilibrium in this window.
It also creates coexistence where one round has uniqueness.
Feedback now runs through two prices, not one.
Late entry after $GG$ raises both round profits enough.

Three-point noise gives the opposite verdict.
Proposition C3.1 gives no open coexistence interval there.
The recruiting flow earns zero residual under three-point noise.
Feedback through entry therefore cannot raise purchase profit there.
Discrete-Laplace recruiting histories keep positive residual $1-M_2>0$.
That residual carries feedback and coexistence.

At benchmark $k=0.02$, this coexistence window does not apply.
Lower bounds in Section 3.5 exceed $k$ everywhere.
Coexistence needs intermediate $k$ or intermediate $r$.
That scope matches Proposition 3 in the Laplace paper.

### 3.7 Incumbent strength and the timing of entry

**Result 10 — analytical: waiting value moves two ways in $r$.**

Fix belief $\mu_1$ and an informative second round.
The derivative of gain in $r$ is $B_r'(\mu)=g_L'(r)-\mu\Delta_T'(r)$.
Both terms are negative.
Higher beliefs lose gain faster as $r$ rises.
Waiting value against exit therefore falls in $r$ on each branch.
Three-point $W(1/2)=(\delta g_H(r)-c_H)/6$ falls since $g_H'<0$.
Discrete-Laplace $W(M_1)$ falls since $B_r(M_2)$ falls.

Waiting against enter now can rise in $r$.
Immediate surplus $N$ also falls in $r$.
In discrete-Laplace noise at $M_1$, the derivative follows.

$$
\frac{d}{dr}\big(W(M_1)-N(M_1)\big)
=P_G\,\delta B_r'(M_2)-B_r'(M_1).
$$

At $r=3$, derivatives are $B'(M_1)\approx-0.318$ and $B'(M_2)\approx-0.367$.
The display gives $+0.143$ at $\delta=0.9$.
Script `c3_welfare.py` prints both derivative values.
Stronger competition thins immediate surplus faster than option value.
Screening bad second news then matters more.

Three-point upper cutoff $\bar\mu$ also rises in benchmark cases.
Its low-case formula has numerator $c_H-g_L(r)$.
That numerator rises as $g_L$ falls.
Its denominator falls in benchmark calculations.
The waiting interval in belief space therefore expands upward.
Exit still shrinks waiting from below through $\delta g_H(r)>c_H$.

Equilibrium waiting is an intermediate-$r$ event.
At low $r$, round 2 does not trade, so waiting has no value.
Just above trade activation, immediate entry can still beat waiting.
At intermediate $r$, waiting wins after middle or good news.
At high $r$, even best late beliefs fail entry thresholds.
Waiting then returns to zero.

Discrete-Laplace thresholds make the pattern exact at $M_1$.
Threshold $\delta^*(r)$ governs wait against now while $B_r(M_1)\ge c_H$.
Threshold $\delta_0(r)=c_H/B_r(M_2)$ governs wait against exit after that point.
They meet at $r_{C1}\approx3.986$ for $c_H=5$.
The required $\delta$ is V-shaped with minimum near that meeting point.
At $\delta=0.9$, script scan gives now at $r=2.5$, wait at $r=3$, exit at $r=5$.
At $\delta=0.95$, waiting already holds at $r=2$ in the scan.

Timing predictions follow from branch probabilities.
Three-point high-cost waiting probability is $2/3$ on delay plateaus.
It is zero outside delay plateaus.
Discrete-Laplace high-cost waiting probability is $1/2$ when waiting after $G$ holds.
It is zero when now or exit holds after $G$.
Competition therefore first delays entry, then stops delay.
Average time to preparation is nonmonotone in $r$.

## 4. What it recovers or loses relative to the Laplace paper

The auction stage stays unchanged in this memo.
Delay changes only trading rounds and preparation timing.
Table 1 maps each paper result to delay status.
Status words are survives, changes, dies, and not applicable.

| Paper object | Three-point delay | Discrete-Laplace delay |
|---|---|---|
| Proposition 1, equation (4) | survives | survives |
| Proposition A.1 bounds $[m,M]$ | dies: bounds stay $[0,1]$ | changes: bounds widen to $[m_2,M_2]$ |
| Proposition A.2 price sufficiency | survives on canonical schedules | survives on canonical schedules |
| Residuals, equation (11) | changes in round 1: $w_L$ term | changes in round 1: $w_L$ term |
| Proposition A.3 fixed experiment | survives: entry falls at fixed histories | survives: entry falls at fixed histories |
| Proposition A.4 thresholds | changes: $r_T$, $r_C(\delta)$, $r_C^D$ | changes: trade bounds, $r_{C1}$, $r_{C2}(\delta)$ |
| Proposition 2(i)–(ii) | survives with larger rise | survives with smaller rise at high $\delta$ |
| Proposition 2(iii) ceiling | dies at $r_2=3.6$: return needs $r>7.97$ | changes: return shifts from $3.99$ to $5.61$ at $\delta=0.95$ |
| Proposition 3 coexistence | dies: no open interval | survives and expands: Section 3.6 window |
| Endogenous trading asymmetry | dies: buy-only by menu | dies: buy-only by menu |
| Proposition A.5 noise class | not applicable | not applicable as stated |
| Proposition A.6 cost distributions | changes: threshold $\tau_\delta$ shifts entry | changes: threshold $\tau_\delta$ shifts entry |
| Proposition A.7 private signals | not applicable here | not applicable here |
| Proposition A.8 payment rule | survives under second price | survives under second price |
| Proposition A.9 price access | changes: target gains at $r_1$ | changes: target loses at $r_1$ |
| Proposition A.10 seller continuation | not applicable: reserve fixed | not applicable: reserve fixed |
| Section 5.1 noise robustness | changes: grading stays absent | changes: grading improves by one step |
| Section 5.2 value distributions | survives in $B_r,\Delta_T,w_L$ form | survives in $B_r,\Delta_T,w_L$ form |
| Section 5.3 private information | open with delay | open with delay |
| Section 6 welfare | changes: challenger and target gain | changes: challenger gains, target loses |

Graded information needs a precise verdict.
Three-point delay does not recover grading.
Final beliefs stay in $\{0,1/2,1\}$ under full purchases.
Discrete-Laplace delay recovers one grading step.
Final beliefs move from two values to three values.
The extra round creates that grading.
The option selects $GG$ histories for late entry.
Mandatory two rounds without early entry would grade equally.
Workstream C2 owns that mandatory-round comparison.

Coexistence also needs a precise verdict.
Three-point delay does not recover Proposition 3.
Purchase profit stays independent of purchase magnitude there.
Discrete-Laplace delay preserves feedback after recruiting histories.
Section 3.6 creates coexistence where one round has uniqueness.
That result is the strongest recovery in this memo.

The information ceiling splits by base model.
Three-point delay keeps ceiling belief $1$.
Late entry fails earlier at $r_C(\delta)$.
Immediate entry still survives until $r_C^D$.
Discrete-Laplace delay keeps a finite ceiling belief $M_2<1$.
The ceiling moves outward, so Proposition 2(iii) weakens in timing.
Repeated waiting would erode the ceiling toward belief $1$.

Fixed-experiment deterrence survives in both base models.
Hold flow laws and beliefs $(\mu_1,\mu_{12})$ fixed.
Raise $r$ to $r'>r$.
Then $B_{r'}(\mu)<B_r(\mu)$ at every belief.
Now entry, late entry, $N$, and $W$ all fall weakly.
Branches move only from now to wait or exit, or wait to exit.
Eventual entry at each history therefore falls weakly.
Averaging over histories preserves the sign.
Equilibrium entry can still rise because trading strategies change.

Welfare signs follow entry and ownership at $r_1$.
Expected proceeds are $t_0+w_L\mathsf E+\Delta_T\mathsf O_H$.
Three-point proceeds rise from $0.755$ to $0.849$ at $\delta=0.95$.
Discrete-Laplace proceeds fall from $0.942$ to $0.803$ at $\delta=0.95$.
High-cost challenger profit rises in both base models at fixed full trade.
Values rise from $0.410$ to $0.636$ under three-point noise.
Values rise from $0.156$ to $0.240$ under discrete-Laplace noise.
Script `c3_welfare.py` prints each value.
Delay helps the challenger by option logic at fixed strategies.
Target gains only when delay creates net entry.

## 5. Numerical example

### 5.1 Three-point benchmark path

Use $c_H=6$, $k=0.02$, $\rho=0.25$, and $\delta=0.95$.
Exact fractions come from script `c3_three_point.py`.
Thresholds are $r_T\approx1.973$, $r_C(\delta)\approx7.334$, and $r_C^D\approx7.969$.

| Strength $r$ | Trading | High-cost branch at middle or good news | $\mathsf E$ | $\mathsf O_H$ |
|---:|---|---|---:|---:|
| $1.2$ | none | exit at prior | $0.250$ | $0.125$ |
| $3$ | full, full | wait at $1/2$ | $11/24\approx0.458$ | $1/3\approx0.333$ |
| $3.6$ | full, full | wait at $1/2$ | $0.458$ | $0.333$ |
| $7.5$ | full, full | exit at $1/2$, now at $1$ | $0.375$ | $0.250$ |
| $8.5$ | full, full | exit except low cost | $0.250$ | $0.125$ |

At $r=3$, one-round entry is $3/8=0.375$.
Delay entry is $11/24\approx0.458$.
Gross round 1 profit rises from $1/18\approx0.056$ to $43/288\approx0.149$.
Gross round 2 profit at $1/2$ stays $1/18$.
Waiting value $W(1/2)$ is $977/2880\approx0.339$.
First middle price rises from $0.615$ to $0.755$.

### 5.2 Discrete-Laplace benchmark path

Use $c_H=5$, $b=2$, $k=0.02$, and $\delta=0.95$.
Values come from script `c3_dlaplace.py` at 50 digits.
Ceilings are $r_{C1}\approx3.986$ and $r_{C2}\approx5.606$.

| Strength $r$ | Trading | Branch after $G$ | $\mathsf E$ with delay | $\mathsf E$ without delay |
|---:|---|---|---:|---:|
| $1.2$ | none | exit at prior | $0.250$ | $0.250$ |
| $3$ | full, full | wait | $0.449$ | $0.625$ |
| $3.6$ | full, full | wait | $0.449$ | $0.625$ |
| $4.2$ | full, full | wait | $0.449$ | $0.250$ |
| $6$ | full, full | exit | $0.250$ | $0.250$ |

At $r=3$, ownership falls from $0.358$ to $0.270$ with delay.
Gross round 1 profit falls from $0.196$ to $0.171$.
Gross round 2 profit after $G$ is $0.143$ on wait branch.
Locked entry would give round 2 profit $0.237$ after $G$.
First good price falls from $1.290$ to $1.011$.
At $\delta=0.8$, delay stays unused at $r=3$ and entry stays $0.625$.

The coexistence example uses different cost values.
At $r=3$, $c_H=5.5$, $\delta=0.95$, and $k=0.09$, entry is $0.250$ or $0.449$.
One-round entry at those values is uniquely $0.250$.
Section 3.6 gives every inequality for that example.

## 6. Open issues

- **Open:** one investor with two orders and a retained stake.
  Round 1 purchases then gain from later entry directly.
  Manipulation by buying can change both waiting and pricing.
- **Open:** full mixed correspondence under discrete-Laplace noise with delay.
  Grids support uniqueness at $k=0.02$.
  Interval bounds over $\beta_1,\beta_2(\cdot)$ would upgrade that status.
- **Open:** presence probability $\lambda<1$ in each round.
  Three-point waiting value scales with effective round 2 presence.
  Discrete-Laplace bounds shrink toward $1/2$ as presence falls.
- **Open:** many waiting periods.
  Belief bounds then approach $0$ and $1$ under discrete-Laplace noise.
  Optimal stopping and trading incentives need a joint limit.
- **Open:** endogenous delay cost.
  Seller deadlines, financing decay, or incumbent preemption can set $\delta$ or survival risk.
  Price-dependent preemption links this memo to workstreams C7 and C8.
- **Open:** challenger private signals with delay.
  Private signals change $W$ by signal value and can sort waiting by type.
  Proposition A.7 logic needs a two-round version.
- **Open:** atomless preparation costs with delay.
  Waiting then holds on a cost interval at each belief.
  Entry can move smoothly in $r$ inside that interval.
- **Open:** seller choice of deadline or reserve after $P_1$.
  A seller can tax waiting through reserve or closing rules.
  Optimal sale design with delay remains unsolved.
- **Conjecture:** preemption risk preserves entry signs in Sections 3.3 and 3.5.
  Threshold $\tau$ replaces $\tau_\delta$ under preemption.
  Ceilings move outward relative to gross discounting.

## 7. Plain summary

A challenger can wait for a second price before it pays for preparation.
Waiting helps only the high-cost challenger.
The low-cost challenger always enters at once.

With three-point noise, waiting turns flat middle news into a second chance.
Entry rises at the benchmark strong incumbent.
The first investor also earns more.
No new belief grades appear.
No coexistence appears.

With discrete-Laplace noise, waiting asks for two good prices in a row.
Entry falls at the benchmark strong incumbent.
Entry quality rises.
Beyond the one-round ceiling, waiting creates entry again.
In one cost window, waiting creates two equilibria where one round has one.

Stronger competition first makes waiting possible by starting trade.
Later, stronger competition makes even the best late news too weak.
Delay therefore lives at intermediate incumbent strength.
The option changes magnitudes and timing in both models.
It recovers coexistence only where recruiting news still pays the investor.
