# T3: The one-directional (buy-only) EGJ menu with bounded noise

Status labels: **analytical**, **computer-assisted**, **numerical diagnostic**, **conjecture**, **open**.

Scripts and outputs: `scripts/T3_buy_only_bounded/`.
Run from the repository root:

```bash
.venv/bin/python audit/microstructure_search_2026_10_22/scripts/T3_buy_only_bounded/t3_exact.py
.venv/bin/python audit/microstructure_search_2026_10_22/scripts/T3_buy_only_bounded/t3_branches.py
.venv/bin/python audit/microstructure_search_2026_10_22/scripts/T3_buy_only_bounded/t3_scan.py
```
Each run took under one second, so no slot was used.
The scripts only print results.
Every equilibrium inequality at a stated point uses exact rational arithmetic.

## 1. Question

The order menu is one-directional: $q \in \{0,1\}$.
The informed investor is present with probability $\lambda$.
The price is competitive, and the challenger sees the price.
Another workstream studies a liquidity trader with the informed order size.
This memo does not use that device.

The question has three parts.

- Which bounded-noise levers make an interior flow recruit the challenger?
- Which levers give feedback, coexistence, and ordered entry?
- Can any lever return entry to $\rho$ at $r_2 = 3.6$?

The levers are:

- B1: symmetric three-point weights $(\theta, 1-2\theta, \theta)$.
- B2: $N$ independent noise traders.
  Each trader buys, sells, or abstains, or each trader buys or abstains.
- B3: an informed order of two units, fixed or chosen.
- B4: any other natural bounded-noise law in the verified records.

The earlier record already settles two neighbouring cases.
Equal three-point weights with presence $\lambda$ are in the A memos.
Asymmetric weights $(2/5, 2/5, 1/5)$ with mixing are in memo C9.
This memo does not redo those cases.
It uses their formulas and their method where they apply.

The bar for comparable strength is the discrete-Laplace base.
The buy-only version needs $c_H = 5$ and strengths $(1.2, 3, 4.2)$.
It gives entry $0.25 \to 0.625 \to 0.25$ and coexistence on $[1.443, 1.748]$.
The two-sided version keeps $c_H = 6$ and $(1.2, 3, 3.6)$.
It gives entry $0.569293$ at $r_1$ and ceiling $3.592659$.
The paper gives entry $0.522757$ at $r_1$.

The headline result is negative on one point and positive on others.
No bounded-noise lever returns entry to $\rho$ at $3.6$ with informative trade.
Lever B1 with small $\theta$ does give the rest at the paper costs.
It gives interior recruitment, entry $5/8$ at $r_1$, and ordered coexistence.
Exact certificates cover the three strengths $1.55$, $1.60$, and $1.65$.

## 2. Setup (menu, noise law, presence or liquidity device, equilibrium concept, belief rule, tie rules)

### 2.1 Auction objects

The paper benchmark is $h = 10$, $\ell = 1$, $p = 1/2$.
It also sets $\rho = 1/4$, $c_L = 0$, $c_H = 6$, $k = 1/50$, and $\pi = 1/2$.
The strengths are $r_0 = 6/5$, $r_1 = 3$, and $r_2 = 18/5$.
The auction objects are those of TEAM_RULES §3.
The script checks them against the closed forms.
At the three strengths:

| $r$ | $\Delta_T$ | $g_L$ | $g_H$ | $\tau$ | $B_r(1/2)$ |
|---|---|---|---|---|---|
| $6/5$ | $1/60$ | $5/16$ | $2231/240$ | $195/308 \approx 0.633117$ | $1153/240 \approx 4.804167$ |
| $3$ | $2/3$ | $1/8$ | $203/24$ | $141/200 = 0.705$ | $103/24 \approx 4.291667$ |
| $18/5$ | $169/180$ | $5/48$ | $5879/720$ | $4245/5804 \approx 0.731392$ | $2977/720 \approx 4.134722$ |

Here $\tau = (c_H - g_L)/(g_H - g_L)$.
The high-cost challenger prepares exactly when $\mu \ge \tau$ (rule E below).
Two facts hold at every $r > 1$ in this benchmark.
First, $B_r(1/2) < 5 < c_H$, because $g_H + g_L = 10 - r/2 + 1/(4r)$ falls in $r$.
Second, $B_r(\mu)$ falls strictly in $r$ at each fixed $\mu$.
Its derivative is $-[\mu r^2 + (1-\mu)\ell^2 - p^2]/(2r^2)$.
The bracket exceeds $\ell^2 - p^2 > 0$ when $r > \ell$.
Hence $\tau(r)$ rises strictly in $r$ while it lies in $(0,1)$.

Write $w_L = t_L - t_0 = 1/2 - 1/(8r) > 0$ and $w_H = t_H - t_0$.
Entry at belief $\mu$ is $e_r(\mu) = \rho + (1-\rho)\mathbf 1\{\mu \ge \tau\}$.
The price at belief $\mu$ is $P_r(\mu) = t_0 + e_r(\mu)(w_L + \Delta_T \mu)$.
Inverting $\Delta_T(r) = d$ for $r > 1$ gives $\mathfrak r(d) = 1 + d + \sqrt{d^2 + 2d}$.
The root of $B_r(\mu) = c_H$ is $r_C(\mu)$ as in memo A.
In particular $r_C(1) = 4 + \tfrac32\sqrt 7 \approx 7.968627$.

### 2.2 Trading stage

Reading N holds with point masses at $\ell$ and $h$ and prior $\pi = 1/2$.
The investor sees the class $j \in \{H, L\}$.
The investor is present with probability $\lambda \in (0,1]$.
This is the first reading of $\lambda$ in the verified EGJ record.
An absent investor sends order zero.
A present investor orders $q \in \{0,1\}$, except in lever B3.
The trading cost is $k$ per unit.
Noise $Z$ has law $f$ on a finite integer set.
Flow is $X = q + Z$.
Market makers see $X$ and set $P = \mathbb E[V_T \mid X]$.
The challenger sees $P$ and its own cost, as in the paper.

Write $\beta_H$ for the purchase probability of a present class-$H$ investor.
Write $\alpha = \lambda \beta_H$ for the effective purchase probability.
Result 1 shows that class $L$ never buys.
So one number $\alpha \in [0, \lambda]$ describes trade.
Full trade means $\alpha = \lambda$.
No trade means $\alpha = 0$.

The four levers change only $f$ or the order size.

- B1: $f = (\theta, 1-2\theta, \theta)$ on $\{-1, 0, 1\}$, with $0 < \theta < 1/2$.
- B2a: $f$ is the $N$-fold convolution of the B1 law.
- B2b: $f$ is $\mathrm{Bin}(N, \beta)$ on $\{0, \dots, N\}$.
- B3a: the menu is $\{0, 2\}$ against B1 noise.
- B3b: the menu is $\{0, 1, 2\}$ against B1 noise.
- B3$\times$B2: the order is two units against B2a noise.
- B4: a general finite law $f$, with two computed examples.

### 2.3 Equilibrium concept, belief rule, and tie rules

The concept is perfect Bayesian equilibrium.
The investor best-responds to a fixed price and entry schedule.
The price is competitive given the entry that the price induces.
Preparation is optimal given the posterior at the observed price.
Beliefs follow Bayes' rule at each flow with positive probability.

Only flows above the largest noise value $b$ can be unused.
They are unused only under no trade.
At an unused flow this memo uses belief $v = 1$.
This is the directional completion of memo C9.
The verified EGJ record uses the same belief under the Intuitive Criterion.
Result 1(d) gives the dominance reason and the supporting belief set.
Passive beliefs $v = 1/2$ serve as the comparison.

Tie rules follow memo A.

- Investor rule Z: a tied investor chooses zero.
- Investor rule M: a tied investor may mix.
- Challenger rule E: a tied challenger prepares.
  This is the paper rule.
- Challenger rule X: a tied challenger may mix.

Headline existence uses rules M and X where a mixture is named.
Each result states the rules that it needs.
Strict benchmark inequalities usually make the rules irrelevant.
The exceptions are stated in each case.

## 3. Results: each with its status label and its full derivation

### Result 1 (analytical). The general frame for every bounded law

Fix a finite noise law $f$ with largest support point $b$ and $f(b) > 0$.
Keep the buy-only menu and $\pi = 1/2$ unless a formula states $\pi$.

**(a) Class $L$ never buys.**
Let $e(x) \in [0,1]$ be entry at the price of flow $x$.
Let $\mu(x)$ be the belief there, on path or off path.
Then $\mathbb E[V_T \mid j, x] = t_0 + e(x)(t_j - t_0)$.
The competitive price is $t_0 + e(x)(w_L + \Delta_T \mu(x))$.
Subtraction gives the two residuals:

$$
V_H(x) - P(x) = e(x)\Delta_T[1-\mu(x)], \qquad
V_L(x) - P(x) = -e(x)\Delta_T\mu(x).
$$

A class-$L$ purchase of any size earns at most $-k$ per unit.
Zero earns zero.
So $\beta_L = 0$ in every equilibrium, under every belief and tie rule.
The same line excludes class-$L$ purchases of two units in lever B3. $\square$

**(b) Posteriors.**
With $f_L(x) = f(x)$ and $f_H(x) = (1-\alpha) f(x) + \alpha f(x-1)$:

$$
\mu_x(\alpha) = \frac{f_H(x)}{f_H(x) + f_L(x)}, \qquad \alpha > 0 \text{ at used flows}.
$$

Three flow types follow at once.

- The top flow $b+1$ has $f_L = 0$ and $f_H = \alpha f(b)$.
  It has $\mu = 1$ when $\alpha > 0$ and is unused when $\alpha = 0$.
- The bottom flow $a$ has $\mu_a = (1-\alpha)/(2-\alpha) \le 1/2$.
- Each interior posterior moves monotonically in $\alpha$.
  Write $A = f(x)$ and $B = f(x-1)$.
  Then $\mu_x = [A + \alpha(B-A)]/[2A + \alpha(B-A)]$.
  Its derivative in $\alpha$ has the sign of $B - A$ at each $\alpha$.
  At $\alpha = 0$ each used posterior equals $1/2$.

Entry is $\mathsf E = \rho + (1-\rho)\Pr(\mu_X \ge \tau)$ under rule E.
High-class ownership is $\mathsf O_H = \pi e_H$ with $e_H = \sum_x f_H(x) e_x$.
A prepared class-$H$ challenger always wins because $h > r$.
Proceeds are $\mathcal R_T = t_0 + \pi e_H w_H + (1-\pi) e_L w_L$.
Welfare $\mathcal W$ uses the accounting of memo A, Result 7.
The script uses those formulas with exact rationals.

**(c) Price sufficiency at $c_L = 0$.**
The low-cost type strictly prepares at each belief.
Its gross profit obeys $B_r(\mu) \ge g_L = 3/(8r) > 0 = c_L$.
So entry is at least $\rho$ at each price.
If two flows share a price, they share entry $e \ge \rho$.
Then $e(w_L + \Delta_T \mu)$ is common to both flows, so $\mu$ is common.
The price is strictly increasing in the posterior across best responses.
The proof is the displayed difference in memo C9, §2.
Hence the challenger recovers $\mu_x$ from the price.
Seeing the price and seeing the flow posterior partition coincide.
This holds for every finite $f$ and every menu in this memo. $\square$

**(d) The no-trade test and off-path beliefs.**
Assume $B_r(1/2) < c_H$, as at the benchmark.
Under no trade each used posterior is $1/2$ and entry is $\rho$.
A deviating purchase reaches flow $z+1$ with probability $f(z)$.
At belief $v$ on the unused top flow its payoff is:

$$
U^{\mathrm{dev}}(v) = \Delta_T\Big[\tfrac{\rho}{2}(1-f(b)) + f(b)\, e(v)(1-v)\Big] - k .
$$

At $v = 1$ the second term is zero.
No trade then holds exactly when $k \ge K_0 := \rho \Delta_T (1-f(b))/2$.
Write $C_N = K_0/\Delta_T = \rho(1-f(b))/2$ for the no-trade coefficient.
Under passive beliefs $v = 1/2$ the test is $k \ge \rho\Delta_T/2$.
No trade survives every belief exactly when:

$$
k \ge \Delta_T\Big[\tfrac{\rho}{2}(1-f(b)) + f(b)\max\{\rho, 1-\tau\}\Big].
$$

The maximum comes from $e(v)(1-v)$ on $v < \tau$ and on $v \ge \tau$.
Belief $v = 1$ is the completion of this memo.
A class-$L$ purchase loses at each belief by part (a).
It is equilibrium-dominated under no trade.
The Intuitive Criterion therefore puts zero weight on class $L$ there.
This matches the one-line argument in the verified EGJ record.
For a two-unit deviation replace $1-f(b)$ by $1-f(b)-f(b-1)$.
Flows $b+1$ and $b+2$ are then both unused under no trade.

**(e) Existence and jump direction at the benchmark.**
Under rules M and X an equilibrium exists for every finite $f$.
The proof is the fixed-point argument of memo C9, Proposition C9.1.
It uses the compact set of purchase rates and entry rates.
Posteriors and the purchase payoff are continuous in $\alpha$ there.
Best-response correspondences have closed graphs.
Kakutani's theorem gives a fixed point.
Part (c) then gives consistent prices.
At the benchmark $\tau > 1/2$.
By part (b) each posterior starts at $1/2$ and moves one way in $\alpha$.
So entry at a flow can jump only upward, from $\rho$ to $1$, as $\alpha$ rises.
The purchase payoff is continuous between jumps and jumps upward at them.
Rules M and E then also give existence at the benchmark.
Rule Z can fail to give existence when only a mixed root works.
Each lever below states where that case occurs. $\square$

### Result 2 (analytical). Proposition 2(iii) fails for every bounded law

**Claim.**
Take any finite noise law and any buy size of at least one unit.
Take any $\lambda$, any mixing, and $r$ with $g_H(r) > c_H$.
Every equilibrium with $\alpha > 0$ has entry strictly above $\rho$.

*Derivation.*
Flows above $b$ need an informed purchase.
Their posterior is $1$ by Result 1(b).
Their total probability is at least $\pi \alpha f(b) > 0$.
At belief $1$ the challenger gain is $g_H(r) > c_H$.
So entry there is $1$ under rules E and X alike.
Entry is therefore at least $\rho + (1-\rho)\pi\alpha f(b) > \rho$. $\square$

At $r_2 = 18/5$, $g_H = 5879/720 \approx 8.165 > 6$.
So informative trade at $r_2$ always has entry above $\rho$.
Entry $\rho$ at $r_2$ needs $\alpha = 0$.
That outcome is uninformative, so it is not Proposition 2(iii).
It also fails as an equilibrium at $k = 1/50$ for the levers here.
Their top noise mass obeys $f(b) \le 1/2$.
Then $K_0 \ge \rho\Delta_T/4 = 169/2880 \approx 0.0587 > k$ at $r_2$.
A deviating purchase profits even under belief $v = 1$.

**The weaker statement that holds (analytical).**
Fix $\alpha > 0$ and follow the full-trade branch as $r$ rises.
The recruiting set $\{x : \mu_x \ge \tau(r)\}$ shrinks by steps.
Entry is a nonincreasing step function of $r$ on that branch.
Its floor before the ceiling is $\rho + (1-\rho)\pi\alpha f(b)$.
At $r > r_C(1) = 4 + \tfrac32\sqrt 7$ no flow recruits.
Entry then equals $\rho$ exactly, and trade stays informative.
Posteriors still differ from $1/2$ and prices still vary.
The script verifies this row at $r = 17/2$ for five candidates.
Each has $\mathsf E = 1/4$ and $U(\lambda) > 0$ there (computer-assisted).

**Smallest changes that restore (iii) (analytical).**
Only parameters in $g_H$ against $c_H$ can restore (iii).
Changes in $(\theta, \lambda, N, \text{size}, k, \rho, \pi)$ cannot.
They leave $g_H(18/5) > c_H$ and the claim applies.
The reserve $p$ cannot work within $p < \ell = 1$.
Even $p \to 1$ gives $g_H(18/5) = 10 - 9/5 - 5/36 > 6$.
Three moves remain, each with trade kept at $r_1$:

- Raise $c_H$ into $(5879/720,\ 203/24] \approx (8.1653,\ 8.4583]$.
  The smallest rise is $1559/720 \approx 2.1653$.
  The new cost is above $82\%$ of $h = 10$.
  BRIEF §2 counts $c_H$ near $h$ as a documented failure.
  At $c_H = 41/5$ and $\theta = 1/5$ entry is $13/40$ at $r_1$ and $1/4$ at $r_2$.
  Trade at $r_2$ is full with $U = 121/2400 > 0$ (computer-assisted).
  Only the top flow recruits at $r_1$, and the feedback gap is negative.
  Coexistence then fails as well.
- Lower $h$ into $[181/24,\ 5641/720) \approx [7.5417,\ 7.8347)$.
  The smallest fall is again $1559/720$.
- Move $r_2$ above $4 + \tfrac32\sqrt 7 \approx 7.968627$.
  The smallest move is about $+4.3686$.

So bounded noise trades the paper ceiling $r_C \approx 3.59$ for $7.97$.
No lever in B1 to B4 changes that number.
The number depends only on $g_H(r) = c_H$.

### Result 3 (analytical). Proposition 2(i) holds at $r_0$ for every bounded law

At $r_0 = 6/5$, $\Delta_T = 1/60 < k = 1/50$.
A purchase at any $\alpha$ and any entry schedule earns per unit:

$$
\Delta_T \sum_z f(z) e_{z+1} (1-\mu_{z+1}) - k \;\le\; \Delta_T - k \;=\; -\frac{1}{300} < 0 .
$$

The bound uses $e \le 1$ and $1-\mu \le 1$.
So buying loses against every candidate schedule.
The same bound covers a no-trade deviation at every off-path belief.
It also covers two-unit orders, with the sum over $z+2$.
Hence no trade is the unique outcome at $r_0$ for every lever.
Entry is $\rho$ and $\mathsf O_H = \pi\rho = 1/8$.
No belief rule and no tie rule matters at $r_0$. $\square$

The rest of the memo therefore scores parts (ii) and 3 by lever.
Part (i) is common ground.
At $r_1$ and $r_2$ no trade fails for each computed lever.
Their $U^{\mathrm{dev}}(1)$ values are positive in the output tables.
Trade at those strengths is therefore full or mixed, never zero alone.

### Result 4 (analytical). B1 posteriors: when flow $x=1$ is good news

Let $f = (\theta, 1-2\theta, \theta)$ on $\{-1,0,1\}$ and $d = 1-3\theta$.
Flows are $\{-1, 0, 1, 2\}$.
Bayes' rule with $\pi = 1/2$ gives, for $\alpha > 0$:

$$
\mu_{-1} = \frac{1-\alpha}{2-\alpha}, \qquad
\mu_0 = \frac{(1-2\theta) - \alpha d}{2(1-2\theta) - \alpha d}, \qquad
\mu_1 = \frac{\theta + \alpha d}{2\theta + \alpha d}, \qquad
\mu_2 = 1 .
$$

Flow $-1$ is always bad news and never recruits ($\mu_{-1} \le 1/2 < \tau$).
Flow $2$ always reveals class $H$ and always recruits before the ceiling.
The two middle flows split by the sign of $d$:

- $\mu_1 > 1/2$ exactly when $\theta < 1/3$. Flow $1$ is then good news.
- $\mu_0 > 1/2$ exactly when $\theta > 1/3$. Flow $0$ is then good news.
- At $\theta = 1/3$ both middle posteriors equal $1/2$ at each $\alpha$.
  That is the equal-weight knife-edge of memo A.

The reason is one line of algebra.
$\mu_1 > 1/2$ holds exactly when $f_H(1) > f_L(1) = \theta$.
But $f_H(1) - \theta = \alpha(1-3\theta)$.
The flow-$0$ comparison gives the opposite sign.
Economically, $\theta < 1/3$ means noise usually abstains.
Flow $1$ then points to a purchase with $Z = 0$.
For $\theta > 1/3$ noise usually trades.
Flow $0$ then points to a purchase offset by a noise sale.

**Recruitment bounds (analytical).**
Flow $1$ recruits at full trade $\alpha = \lambda$ exactly when:

$$
\theta \;\le\; \frac{\lambda(1-\tau)}{(2\tau-1) + 3\lambda(1-\tau)} \qquad (\theta < 1/3).
$$

Flow $0$ recruits at full trade exactly when:

$$
\theta \;\ge\; \frac{(2\tau-1) + \lambda(1-\tau)}{2(2\tau-1) + 3\lambda(1-\tau)} \qquad (\theta > 1/3).
$$

Each line solves $\mu \ge \tau$ for $\theta$ from the displayed posteriors.
At $\lambda = 1$ they read $\theta \le (1-\tau)/(2-\tau)$ and $\theta \ge \tau/(1+\tau)$.
The exact benchmark bounds are:

| $r$ | $\tau$ | flow $1$ recruits ($\lambda=1$) | flow $0$ recruits ($\lambda=1$) |
|---|---|---|---|
| $6/5$ | $195/308$ | $\theta \le 791/2947 \approx 0.2684$ | $\theta \ge 1365/3521 \approx 0.3877$ |
| $3$ | $141/200$ | $\theta \le 59/259 \approx 0.2278$ | $\theta \ge 141/341 \approx 0.4135$ |
| $18/5$ | $4245/5804$ | $\theta \le 1559/7363 \approx 0.2117$ | $\theta \ge 4245/10049 \approx 0.4224$ |

At $\lambda = 1$ the full-trade posteriors have simple forms.
They are $\mu_1(1) = (1-2\theta)/(1-\theta)$ and $\mu_0(1) = \theta/(1-\theta)$.
Also $\mu_{-1}(1) = 0$.
Lower $\lambda$ tightens each bound through the formulas above.
At $r_1$ the flow-$1$ bound is $0.2061$ at $\lambda = 3/4$.
It is $0.1730$ at $\lambda = 1/2$ (numerical evaluation of the formula).
An interior recruiting flow exists for an open set of $(\theta, \lambda)$.
That answers the first BRIEF §3 question in the positive for B1.
The recruiting flow is interior: its posterior lies strictly inside $(0,1)$.
A purchase there keeps residual $e \Delta_T (1-\mu) > 0$.
Feedback can therefore live, unlike at equal weights.

### Result 5 (analytical). B1 payoff shape and complete fixed-$r$ classification

A purchase reaches flows $0, 1, 2$ with probabilities $\theta, 1-2\theta, \theta$.
Flow $2$ pays zero residual.
With $D_0 = 2(1-2\theta) - \alpha d$ and $D_1 = 2\theta + \alpha d$:

$$
1-\mu_0 = \frac{1-2\theta}{D_0}, \qquad 1-\mu_1 = \frac{\theta}{D_1}, \qquad
S(\alpha; e_0, e_1) := \theta(1-2\theta)\Big[\frac{e_0}{D_0} + \frac{e_1}{D_1}\Big].
$$

The purchase payoff is $U(\alpha) = \Delta_T S(\alpha) - k$.
At $\alpha = 0$ under the completion, $S(0) = C_N = \rho(1-\theta)/2$.
Differentiating at fixed entry rates gives:

$$
S'(\alpha) = \theta(1-2\theta)(3\theta-1)\Big[\frac{e_1}{D_1^2} - \frac{e_0}{D_0^2}\Big].
$$

Also $D_0 - D_1 = 2(1-3\theta)(1-\alpha)$.
Four cases now give $S'(\alpha) < 0$ for $\alpha \in [0,1)$ and $\theta \ne 1/3$:

- $\theta < 1/3$, $e_0 = e_1 = \rho$: $D_0 \ge D_1$, so the bracket is nonnegative.
- $\theta < 1/3$, $e_0 = \rho$, $e_1 = 1$: $D_0 - D_1/2 > 0$, so the bracket is positive.
- $\theta > 1/3$, $e_0 = e_1 = \rho$: $D_0 \le D_1$, so the bracket is nonpositive.
- $\theta > 1/3$, $e_0 = 1$, $e_1 = \rho$: $D_0/2 - D_1 < 0$, so the bracket is negative.

In each case the factor $(3\theta-1)$ makes the product negative.
So $S$ falls strictly on each fixed-entry segment.
At most one middle posterior can cross $\tau > 1/2$ upward.
Write $\alpha^*$ for that crossing when it lies in $[0,\lambda]$:

$$
\alpha^* = \frac{\theta(2\tau-1)}{(1-3\theta)(1-\tau)}\ (\theta<1/3), \qquad
\alpha^* = \frac{(1-2\theta)(2\tau-1)}{(3\theta-1)(1-\tau)}\ (\theta>1/3).
$$

At $\alpha^*$ entry at the recruiting flow jumps from $\rho$ to $1$.
The payoff jumps upward by $\Delta_T \theta(1-2\theta)(1-\rho)/D_{\mathrm{rec}}(\alpha^*) > 0$.
Hence $U$ falls, jumps up once, then falls again.
At $\theta = 1/3$ it is constant, which is memo A's single cutoff.
Symmetric weights never give memo A's increasing case.
That case needs monotone weights $a \le d \le c$ with $a \ne c$.
Symmetry forces $a = c$, so only the jump can create feedback here.

Write $K(\alpha) = \Delta_T S(\alpha)$ with rule-E entry.
Write $K(\alpha^{*-})$ and $K(\alpha^{*+})$ for its two limits at the jump.
Under the completion the outcomes at fixed $r$ are exactly:

| Outcome | Holds exactly when | Rules |
|---|---|---|
| no trade $\alpha = 0$ | $K(0) \le k$ | Z or M |
| full trade $\alpha = \lambda$ | $K(\lambda) \ge k$ (strict under Z) | Z or M |
| mixed root in $(0, \alpha^*)$ | $K(0) > k > K(\alpha^{*-})$ | M |
| threshold outcome $\alpha^*$ | $K(\alpha^{*-}) \le k \le K(\alpha^{*+})$ | M and X |
| mixed root in $(\alpha^*, \lambda)$ | $K(\alpha^{*+}) > k > K(\lambda)$ | M |

If $\alpha^* > \lambda$ only the first, second, and one-root rows can occur.
Existence holds under (M, E) and under (M, X) at the benchmark.
The case split in Result 1(e) proves it from the shape.
Under (Z, E) existence fails exactly when $K(\lambda) \le k < K(0)$ up to ties.
Only a mixed root or the threshold outcome can work there.
The threshold outcome needs challenger mixing at one posterior.
Its mixing rate $\sigma_T$ solves $U(\alpha^*) = 0$ linearly.
This classification mirrors memo C9, Proposition C9.2, on symmetric weights.
The new content is the sign proof, which C9 does not need.
C9's weights $(2/5,2/5,1/5)$ make flow $0$ exactly neutral.
Here both middle flows move, in opposite directions.

### Result 6 (analytical and computer-assisted). B1 feedback, windows, and ordered entry

**Feedback gap.**
Define $C_T = S(\lambda)$ at rule-E entry and $C_\rho = S(\lambda)$ at forced entry $\rho$.
The gap $C_T - C_N$ splits into two signed parts:

$$
C_T - C_N = \underbrace{(C_T - C_\rho)}_{\text{entry effect} \ge 0} + \underbrace{(C_\rho - C_N)}_{\text{information decay} < 0}.
$$

The decay is negative by Result 5: more trade reveals more at camouflage flows.
The entry effect is positive only when an interior flow recruits.
Coexistence of no trade and full trade needs a positive total gap.
It then holds for $\Delta_T \in [k/C_T, k/C_N]$ with the recruiting pattern intact.
In strengths the window is $[r_F, \min(r_N, r_C(\mu_{\mathrm{rec}}))]$.
Here $r_N = \mathfrak r(k/C_N)$ and $r_F = \mathfrak r(k/C_T)$.
The cap $r_C(\mu_{\mathrm{rec}})$ keeps $\tau(r) \le \mu_{\mathrm{rec}}(\lambda)$.

At $\lambda = 1$, $D_0(1) = D_1(1) = 1-\theta$.
So $C_T = \theta(1-2\theta)(e_0+e_1)/(1-\theta)$.
With exactly one recruiting flow, $C_T = (1+\rho)\theta(1-2\theta)/(1-\theta)$.
The gap is positive exactly when $21\theta^2 - 12\theta + 1 < 0$ at $\rho = 1/4$.
That is $\theta \in ((6-\sqrt{15})/21, (6+\sqrt{15})/21) \approx (0.1013, 0.4701)$.
Entry at full trade is then $5/8$ on either side of $1/3$.
The recruiting mass obeys $w_{\mathrm{rec}} + w_2 = (1-\theta)/2 + \theta/2 = 1/2$.
Hence $\mathsf E = \rho + (1-\rho)/2 = 5/8$.
The value $5/8 = 0.625$ equals the buy-only discrete-Laplace bar.
It exceeds the paper value $0.522757$.
Without interior recruitment entry is $\rho + (1-\rho)\theta/2$ at $\lambda = 1$.
That value is $11/32$ at $\theta = 1/4$ and $3/8$ at $\theta = 1/3$.

**Computed benchmark rows (computer-assisted, $\lambda = 1$).**

| $\theta$ | $\mu_0, \mu_1$ | recruit at $r_1$ | $C_N$ | $C_T$ | gap | $\mathsf E(r_1)$ | $\mathsf E(r_2)$ |
|---|---|---|---|---|---|---|---|
| $1/10$ | $1/9, 8/9$ | $1,2$ | $9/80$ | $1/9$ | $-1/720$ | $5/8$ | $5/8$ |
| $3/20$ | $3/17, 14/17$ | $1,2$ | $17/160$ | $21/136$ | $131/2720$ | $5/8$ | $5/8$ |
| $1/5$ | $1/4, 3/4$ | $1,2$ | $1/10$ | $3/16$ | $7/80$ | $5/8$ | $5/8$ |
| $11/50$ | $11/39, 28/39$ | $1,2$ | $39/400$ | $77/390$ | $1559/15600$ | $5/8$ | $133/400$ |
| $1/4$ | $1/3, 2/3$ | $2$ | $3/32$ | $1/12$ | $-1/96$ | $11/32$ | $11/32$ |
| $2/5$ | $2/3, 1/3$ | $2$ | $3/40$ | $1/15$ | $-1/120$ | $2/5$ | $2/5$ |
| $9/20$ | $9/11, 2/11$ | $0,2$ | $11/160$ | $9/88$ | $59/1760$ | $5/8$ | $5/8$ |

The row $\theta = 1/10$ shows the gap boundary at work.
Its interior flow recruits, yet decay beats the entry effect by $1/720$.
The row $\theta = 11/50$ shows the partial return pattern.
Flow $1$ recruits at $r_1$ but not at $r_2$, since $28/39 \approx 0.718 < \tau(r_2)$.
Entry falls from $5/8$ to $133/400 = 0.3325$, but not to $\rho$.
At $\lambda < 1$ entry falls with $\lambda$ at fixed $\theta$.
For $\theta = 3/20$ it is $179/320$ at $\lambda = 3/4$ and $79/160$ at $\lambda = 1/2$.
For $\theta = 1/5$ at $\lambda = 1/2$ flow $1$ stops recruiting at $r_1$.
Entry there is then only $23/80$.

**Windows and branches.**
The mixed root $\alpha_A$ in $(\alpha^*, \lambda)$ solves $\Delta_T S_2(\alpha) = k$.
Here $S_2$ is the post-jump segment, which falls in $\alpha$ and ignores $r$.
Implicit differentiation gives $d\alpha_A/dr > 0$ wherever the root exists.
Entry on this branch rises strictly in $r$ (analytical).
For $\theta < 1/3$ it is $\rho + (1-\rho)[\theta + \alpha_A(1-2\theta)/2]$.
For $\theta > 1/3$ replace the bracket by $(1-2\theta) + \alpha_A(4\theta-1)/2$.
This is the symmetric counterpart of memo C9's upward branch.
Entry on the full branch is flat in $r$ while its recruiting set is fixed.
Entry on the threshold branch $\alpha_T = \alpha^*(r)$ falls at computed points.
At fixed $r$ the order is $\rho < \mathsf E_T < \mathsf E_A \le \mathsf E_{\mathrm{full}}$.
The certificates below verify the order at three strengths.

Window endpoints from the formulas ($\lambda = 1$; decimals numerical):

| $\theta$ | $r_F$ | $r_N$ | $r_C(\mu_{\mathrm{rec}})$ | window |
|---|---|---|---|---|
| $3/20$ | $1.6547$ | $1.8300$ | $5.4121$ | $[1.6547, 1.8300]$ |
| $1/5$ | $1.5807$ | $(6+\sqrt{11})/5 \approx 1.8633$ | $4$ exact | $[1.5807, 1.8633]$ |
| $1/4$ | $1.5446$ | $1.9005$ | $1 + 3\sqrt2/4 \approx 2.0607$ | $[1.5446, 1.9005]$ |
| $9/20$ | $1.8508$ | $2.1073$ | $5.3177$ | $[1.8508, 2.1073]$ |

The branch $\alpha_A$ starts below $r_F$ at a birth strength $r_I$.
Grid search gives $r_I \approx 1.466$ at $\theta = 3/20$ (numerical diagnostic).
It gives $r_I \approx 1.461$ at $\theta = 7/50$ and $1.498$ at $\theta = 1/5$.
No trade and informative trade therefore coexist from about $1.466$ to $1.830$.
The full-trade part of that interval starts only at $1.6547$.
None of these windows is a knife-edge: each has positive width in $r$.
Each also persists for nearby $\theta$ by continuity of the strict inequalities.

**A trade-off triangle (analytical at $\lambda = 1$).**
Three wishes compete at $\lambda = 1$:

- (a) interior recruitment at $r_1$;
- (b) a no-trade plus full-trade window covering $[1.55, 1.65]$;
- (c) the rising branch $\alpha_A$ alive at $1.55, 1.60, 1.65$ with no trade.

Wish (b) needs $r_F \le 1.55$, hence $C_T \ge k/\Delta_T(31/20) = 124/605$.
On the low side wish (a) needs $\theta \le 59/259$.
There $C_T(\theta)$ rises in $\theta$, since its derivative has sign $1-4\theta+2\theta^2 > 0$.
Its maximum under (a) is $8319/41440 \approx 0.2007 < 124/605 \approx 0.2050$.
On the high side wish (a) needs $\theta \ge 141/341$.
There $C_T$ falls in $\theta$ and its maximum under (a) is $8319/54560 \approx 0.1525$.
So (a) and (b) cannot hold together at $\lambda = 1$.
Wishes (a) and (c) do hold together for small $\theta$.
The certificates prove them at $\theta = 3/20$ and $\theta = 7/50$.
At $\lambda < 1$ wishes (a) and (b) can hold together in a small corner.
Grid search finds such points only at small $(\theta, \lambda)$ (numerical diagnostic).
An example is $\theta = 1/20$, $\lambda = 1/10$ with $C_T \approx 0.2498$.
Entry at $r_1$ there is only $257/800 \approx 0.3213$.
Small presence buys window placement at the cost of entry level.

**Exact certificates (computer-assisted).**
Take $\theta = 3/20$ and $\lambda = 1$ at $r = 31/20, 8/5, 33/20$.
The values $\alpha_T$ and $\sigma_T$ below are exact rationals.
The values $\alpha_A$ are bracketed by exact payoff signs to width below $10^{-21}$.
At each strength $U^{\mathrm{dev}}(1) < 0$, so no trade is an equilibrium.
At each strength $U(\alpha^{*+}) > 0 > U(1)$, so $\alpha_A$ is an equilibrium under (M, E).
The threshold outcome is a third equilibrium under (M, X).

| $r$ | $U^{\mathrm{dev}}(1)$ | $\alpha_T$ | $\sigma_T$ | $\mathsf E_T$ | $\alpha_A$ | $\mathsf E_A$ |
|---|---|---|---|---|---|---|
| $31/20$ | $-1911/198400$ | $1389/6127 \approx 0.226701$ | $0.660974$ | $0.368017$ | $0.506062$ | $0.495341$ |
| $8/5$ | $-103/12800$ | $94/407 \approx 0.230958$ | $1708969/3293703 \approx 0.518859$ | $0.346079$ | $0.712708$ | $0.549586$ |
| $33/20$ | $-1351/211200$ | $10587/45001 \approx 0.235261$ | $0.405789$ | $0.328575$ | $0.970878$ | $0.617356$ |

Entry on the $\alpha_A$ branch is strictly ordered: $0.495341 < 0.549586 < 0.617356$.
Entry on the threshold branch falls: $0.368017 > 0.346079 > 0.328575$.
The same pattern holds at $\theta = 7/50$ with more margin at the top.
There $\alpha_A$ is $0.464710, 0.644750, 0.859890$ at the three strengths.
Its entry is $0.480472 < 0.529083 < 0.587170$.
Full fractions for $\sigma_T$ and $\mathsf E_T$ are in the branch output file.
At $\theta = 3/20$ the top margin is thin: $U(1) = -69/299200$ at $r = 33/20$.
Just above $r_F \approx 1.6547$ the branch merges into full trade at entry $5/8$.
Ordered entry across the three paper strengths therefore holds.
It holds on the mixed branch, not on the flat full branch.
This matches the discrete-Laplace pattern for its partial branch.
It differs from the paper, where full purchases carry the ordering.

**Working range.**
Float scans on a $0.005$ grid give these ranges at $\lambda = 1$ (numerical diagnostic):

- interior recruitment at $r_1$: $\theta \in [0.02, 0.225] \cup [0.415, 0.49]$;
- positive gap with recruitment: $\theta \in [0.105, 0.47]$;
- nonempty no-trade plus full-trade window: $[0.105, 0.26] \cup [0.395, 0.47]$;
- that window covering $[1.55,1.65]$: $[0.24, 0.255]$ only, without wish (a);
- $\alpha_A$ with no trade at the three strengths: $\theta \in [0.02, 0.15]$.

The analytical gap interval is $(0.1013, 0.4701)$.
The recommended point is $\theta = 7/50$ or $3/20$ with $\lambda$ near $1$.
At $\theta = 3/20$ recruitment at $r_1$ needs $\lambda \ge \alpha^*(3) \approx 0.3790$.
Ordered entry at the three strengths also survives at $\lambda = 0.9$ and $0.75$.
There the $1.65$ point uses full trade instead of $\alpha_A$ (numerical diagnostic).
Presence $\lambda = 1$ is the boundary of EGJ's assumption $\lambda < 1$.
Values just below $1$ keep every strict benchmark inequality here.
They lower entry a little: $179/320 \approx 0.5594$ at $\lambda = 3/4$.

### Result 7 (analytical and computer-assisted). B2a: $N$ trinomial noise traders

Let each of $N$ traders draw from $(\theta, 1-2\theta, \theta)$ with $\theta \le 1/3$.
Noise $Z$ is their sum, with support $\{-N, \dots, N\}$.
Write $r_x = f(x-1)/f(x)$ for the one-step ratio.
Result 1(b) gives $\mu_x = [(1-\alpha) + \alpha r_x]/[(2-\alpha) + \alpha r_x]$.
So $\mu_x$ rises in $r_x$, and $\mu_x \ge \tau$ exactly when:

$$
r_x \;\ge\; R^* := 1 + \frac{2\tau-1}{\alpha(1-\tau)} .
$$

At $\alpha = 1$ this is $R^* = \tau/(1-\tau)$, about $2.39$ at $r_1$.
For the computed laws the posteriors rise in $x$ (computer-assisted tables).
The recruiting set is then an upper tail $\{x \ge \hat x\}$ plus the top flow.
The top flow $N+1$ still reveals class $H$ by Result 2.
Flows just below it are interior and can recruit.
Their residual $1-\mu_x$ is positive but small when $r_x$ is large.

**Computed rows at $r_1$ (computer-assisted, $\lambda = 1$).**

| $N, \theta$ | recruiting flows | $C_N$ | $C_T$ | gap | entry effect | $\mathsf E$ |
|---|---|---|---|---|---|---|
| $1, 1/3$ | $2$ | $1/12$ | $1/12$ | $0$ | $0$ | $3/8 = 0.3750$ |
| $2, 1/3$ | $3$ | $1/9$ | $14/135$ | $-1/135$ | $0$ | $7/24 \approx 0.2917$ |
| $3, 1/3$ | $3,4$ | $13/108$ | $739/5616$ | $7/624$ | $1/48$ | $23/72 \approx 0.3194$ |
| $4, 1/3$ | $3,4,5$ | $10/81$ | $5456/36855$ | $302/12285$ | $32/945$ | $37/108 \approx 0.3426$ |
| $5, 1/3$ | $4,5,6$ | $121/972$ | $6083/46656$ | $275/46656$ | $55/3888$ | $7/24 \approx 0.2917$ |
| $8, 1/3$ | $6,7,8,9$ | $820/6561$ | $0.123358$ | $-0.001623$ | $0.003964$ | $572/2187 \approx 0.2615$ |
| $3, 1/5$ | $2,3,4$ | $31/250$ | $1953/13000$ | $341/13000$ | $3051/65000$ | $2/5 = 0.4000$ |
| $3, 1/4$ | $2,3,4$ | $63/512$ | $75/448$ | $159/3584$ | $27/448$ | $215/512 \approx 0.4199$ |

Three lessons follow from the table.

- At $N = 2$ and $\theta = 1/3$, flow $2$ has $\mu = 2/3 < \tau(r_1)$.
  Only the revealing flow recruits at $r_1$, so the gap is negative.
  Flow $2$ does recruit at lower strengths where $\tau(r) < 2/3$.
  A coexistence window can therefore exist away from $r_1$.
- Smaller per-trader $\theta$ steepens the tail ratios.
  At $N = 3$ entry rises from $0.3194$ to $0.4199$ as $\theta$ falls to $1/4$.
  This combines lever B1 with lever B2.
- Entry never reaches the B1 value $5/8$ in these rows.
  The best trinomial row gives $0.4199$, below the paper value $0.5228$.

**Windows (numerical diagnostic).**
Float scans give first full-trade crossings $r_F$ between $1.58$ and $1.67$.
They give $r_N$ between $1.75$ and $1.81$ for the rows above.
So no-trade plus full-trade windows exist but start above $1.55$.
Mixed roots appear at some of the three strengths on the $\alpha$ grid.
Their entries rise in the clearest case, $N=3$, $\theta = 1/5$ excluded below.
I do not certify B2 mixed branches exactly; they stay diagnostics.
At $N = 3$, $\theta = 1/3$ the scan finds no root at $1.55$.
At $1.60$ and $1.65$ it finds one root near $\alpha = 0.85$.
Full trade already exists there, with flat entry $23/72$ at $\lambda = 1$.
Ordered entry at the three strengths is therefore not shown for B2a.

**Large $N$ (analytical, using Cramér's large-deviation theorem).**
As $N$ grows, $f(N) = \theta^N \to 0$.
So $C_N \to \rho/2$ and $r_N \to \mathfrak r(4/25) = (29+6\sqrt6)/25 \approx 1.747878$.
That limit equals the paper no-trade boundary $r_N$.
The reason matches memo A: the revealing mass $\theta^N$ vanishes.
Recruitment needs ratio $r_x \ge R^*$ at a fixed threshold.
By exponential tilting, the smallest such $x$ obeys $\hat x/N \to c^* > 0$.
Here $c^*$ is the mean under the tilt with parameter $\log R^*$.
The tail probability $\Pr(Z \ge \hat x)$ then falls like $e^{-N I(c^*)}$.
The same bound holds under the purchase law $Z + 1$.
Hence the entry effect and the entry excess over $\rho$ tend to zero.
The feedback gap tends to zero from the computed pattern.
Many noise traders therefore dilute the unit signal away.
The useful range of $N$ is small: $N \in \{2, 3, 4, 5\}$ on the grid.

### Result 8 (analytical and computer-assisted). B2b: binomial noise and the parity failure

Let each of $N$ traders buy with probability $\beta$ or else abstain.
Noise is $Z \sim \mathrm{Bin}(N, \beta)$ on $\{0, \dots, N\}$.
The ratio is $r_x = x(1-\beta)/[(N-x+1)\beta]$, strictly rising in $x$.
Posteriors therefore rise in $x$ by the formula in Result 7 (analytical).
The top flow $N+1$ reveals class $H$.
The bottom flow $0$ has $\mu_0 = (1-\alpha)/(2-\alpha)$ as before.
Large $N$ again kills the entry effect by the same tilting argument.
The ratio crosses $R^*$ only at $x/N$ above $\beta$ by a fixed margin.

**Computed rows at $r_1$ (computer-assisted, $\lambda = 1$).**

| $N, \beta$ | posteriors | recruit | $C_N$ | gap | $\mathsf E$ |
|---|---|---|---|---|---|
| $1, 1/2$ | $0, 1/2, 1$ | $2$ | $1/16$ | $0$ | $7/16 = 0.4375$ |
| $2, 1/2$ | $0, 1/3, 2/3, 1$ | $3$ | $3/32$ | $-1/96$ | $11/32 \approx 0.3438$ |
| $3, 1/2$ | $0, 1/4, 1/2, 3/4, 1$ | $3,4$ | $7/64$ | $7/128$ | $31/64 \approx 0.4844$ |
| $4, 1/2$ | $0, 1/5, 2/5, 3/5, 4/5, 1$ | $4,5$ | $15/128$ | $13/640$ | $25/64 \approx 0.3906$ |
| $3, 1/4$ | $0, 1/2, 3/4, 9/10, 1$ | $2,3,4$ | $63/512$ | $63/1280$ | $269/512 \approx 0.5254$ |
| $5, 1/4$ | $0, 3/8, 3/5, 3/4, 6/7, 15/16, 1$ | $3,4,5,6$ | $1023/8192$ | $7143/229376$ | $1747/4096 \approx 0.4265$ |

The strongest binomial row is $N = 3$, $\beta = 1/4$.
Its entry $0.5254$ sits just above the paper value $0.5228$.
Its float window is $r_F \approx 1.612$ to $r_N \approx 1.755$ (numerical diagnostic).
The $\alpha$ grid finds mixed roots at $1.55, 1.60, 1.65$ there.
Their grid entries are about $0.462$, $0.512$, and full-trade $0.525$.
That pattern suggests ordered entry, but it has no exact certificate here.
The economics are also further from EGJ than B1 or B2a.
Noise never sells in B2b, so mean flow is positive by construction.
The market maker still prices by posterior, so the model is coherent.
But one-sided noise has no precedent in the verified EGJ or GG records.

**Parity failure (analytical).**
Suppose instead each trader buys or sells, with no abstention.
Noise support then lies in one parity class $a + 2\mathbb Z$.
A unit purchase flips the parity of every flow it reaches.
Class $L$ and an absent investor cannot reach those flows.
So each flow a buyer can reach has posterior $1$ when $\alpha > 0$.
The purchase payoff is $-k$ against every such schedule.
Under the completion $v = 1$, no trade is the unique outcome at each $r$.
Under passive beliefs no equilibrium exists at $r_1$.
There the deviation earns $\rho\Delta_T/2 - k > 0$ against no trade.
But each $\alpha > 0$ candidate earns $-k$ on path.
The script verifies $U = -1/50$ exactly for $N = 2, 3$ (computer-assisted).
The two-point law $\{-1, 1\}$ fails by the same argument.
Contiguous integer support is therefore necessary for camouflage.
Abstention by noise traders is not a detail in this menu.
It is what lets noise and a purchase reach the same flow.

### Result 9 (analytical and computer-assisted). B3: two-unit informed orders

**Fixed size two (analytical).**
Take menu $\{0,2\}$ against B1 noise $(\theta, 1-2\theta, \theta)$.
Class-$L$ flows are $\{-1, 0, 1\}$ and purchase flows are $\{1, 2, 3\}$.
Posteriors are $\mu_{-1} = \mu_0 = (1-\alpha)/(2-\alpha)$, $\mu_1 = 1/2$, $\mu_2 = \mu_3 = 1$.
The overlap flow $1$ is exactly neutral at every $\alpha$:
$f_H(1) = (1-\alpha)\theta + \alpha\theta = \theta = f_L(1)$.
A purchase reaches flow $1$ only when $Z = -1$, with probability $\theta$.
Its per-unit payoff is therefore constant in $\alpha$:

$$
U_{\text{per unit}} = \frac{\theta \rho \Delta_T}{2} - k, \qquad C = \frac{\theta\rho}{2}.
$$

Feedback is zero: recruiting flows $2$ and $3$ pay zero residual.
The hidden-price payoff is identical.
There is one cutoff and no coexistence except the tie $k = \theta\rho\Delta_T/2$.
Trade at $r_1$ holds exactly when $\theta > 2k/(\rho\Delta_T) = 6/25$.
Entry under trade is $\rho + (1-\rho)\pi\lambda(1-\theta)$ before the ceiling.
At $\theta = 1/3$, $\lambda = 1$ entry is $1/2$ and per-unit $U = 7/900 > 0$.
At $\theta = 1/5$ trade fails at $r_1$ with $U = -1/300$ per unit.
Smaller $\theta$ raises entry if trade occurs but makes trade harder.
The supremum entry with trade at $r_1$ is $107/200$ as $\theta \downarrow 6/25$.
The single strength cutoff at $\theta = 1/3$ is $r = \mathfrak r(12/25) \approx 2.5711$.
Below it the outcome is no trade, above it full two-unit trade.

**Size choice $\{0,1,2\}$ (analytical in part, computer-assisted on grid).**
A buy-two conjecture always fails at $\alpha = 1$.
Against its schedule a one-unit deviation reaches flows $0, 1, 2$.
Flow $0$ then has $\mu_0 = 0$, so the deviation hides at entry $\rho$.
The deviation beats the two-unit order by $k + \rho\Delta_T(1-\theta)/2 > 0$.
For $\theta \le 1/3$ the same ranking holds at every $\lambda$ (analytical).
The margin is $k + \rho\Delta_T[(1-2\theta)/2 - \theta(1-\lambda)/(2-\lambda)] \ge k$.
A buy-one conjecture faces a two-unit deviation to flows $1, 2, 3$.
Flow $3$ is off path there and takes belief $1$ under the completion.
Buy one beats that deviation by $k + \Delta_T[\theta(1-2\theta)e_0/D_0 + \theta(1-4\theta)e_1/D_1]$.
For $\theta \le 1/4$ both bracket terms are nonnegative (analytical).
Buy one is then the size-choice outcome whenever B1 trade occurs.
Exact evaluation at $r_1$ on $\theta \in \{3/20, 1/5, 1/4, 1/3, 2/5, 9/20\}$ gives:

- buy one stable and buy two unstable for $\theta \le 1/3$, each $\lambda \in \{1, 3/4, 1/2\}$;
- both pure sizes unstable for $\theta = 2/5$ at each listed $\lambda$;
- both unstable for $\theta = 9/20$ at $\lambda = 1, 3/4$; buy one stable at $\lambda = 1/2$.

So the menu $\{0,1,2\}$ collapses to B1 on the recommended range.
For $\theta > 1/3$ it can destroy pure-size equilibrium at $r_1$.
A mixed-size equilibrium may exist under rules M and X.
This memo does not solve that correspondence; it stays **open**.
Under passive belief at flow $3$ buy one also fails at $\theta = 1/3$.
Size choice therefore adds off-path dependence beyond the B1 menu.
Any size mixture still has revealing top flows.
Result 2 still blocks Proposition 2(iii) for every size rule.

**Two units against wider noise (computer-assisted).**
Fixed size two against trinomial noise restores a gap in one row.
At $N = 2$, $\theta = 1/3$ posteriors are $(0,0,1/4,1/2,3/4,1,1)$.
Flows $2,3,4$ recruit at $r_1$ and entry is $13/24 \approx 0.5417$.
The per-unit gap is $7/144 > 0$.
At $N = 3$ the gap is $-1/7560$ for $\theta = 1/3$ and $-1/3100$ for $\theta = 1/5$.
Wider noise gives the two-unit order more camouflage flows.
It also reveals at two top flows instead of one.
The float full-trade crossing for the $N=2$ row is $r_F \approx 1.724$.
Its no-trade boundary uses $C_N = \rho(1-f(b)-f(b-1))/2 = 1/12$.
That boundary is $r \approx 1.973$, so a window exists on the diagnostic.
No mixed branch is certified for this combined lever.

### Result 10 (analytical and computer-assisted). B4: other bounded laws

Result 7 gives the general test for any finite law.
Interior recruitment at flow $x$ needs ratio $r_x \ge R^*$.
Feedback needs in addition that $f(x-1)(1-\mu_x)$ carry real mass.
Contiguous support is necessary by the parity argument in Result 8.
Three further cases from the records and their neighbours follow.

**Uniform noise (analytical).**
Let $f$ be uniform on $\{-M, \dots, M\}$.
Then $r_x = 1$ at each interior flow, so $\mu_x = 1/2$ there.
Only the top flow recruits, and the payoff is constant in $\alpha$:
$U = \rho\Delta_T(1 - 1/(2M+1))/2 - k$.
There is one cutoff, no feedback, and no coexistence off the tie.
Entry at $r_1$ is $13/40$ for $M = 2$ and $17/56$ for $M = 3$ (computer-assisted).
Flat noise kills graded information just as equal three-point noise does.

**Truncated geometric five-point noise (computer-assisted).**
Let $f = (1,2,4,2,1)/10$ on $\{-2, \dots, 2\}$.
Ratios on the upper half are constant at $2$, as in a truncated Laplace law.
Posteriors at $\lambda = 1$ are $(0, 1/3, 1/3, 2/3, 2/3, 1)$.
Flows $1$ and $2$ recruit only while $\tau(r) \le 2/3$, that is $r \le 1 + 3\sqrt2/4$.
At $r_1$ they do not recruit and entry is only $23/80$.
With recruitment, $C_T = 1/4$ against $C_N = 9/80$.
Float search gives a window from about $1.488$ to $1.800$ (numerical diagnostic).
It covers $[1.55, 1.65]$ with full trade at entry $5/8$ there.
This law is a bounded relative of the discrete-Laplace bar.
It is less EGJ-like than B1, since EGJ noise has three points.
It still reveals at the top flow, so Result 2 applies unchanged.

**Pointers without redo.**
Memo C9 studies general three-point weights with mixing.
Its existence theorem and scalar test cover the asymmetric family.
Two trading rounds and delay leave the one-shot class of this memo.
The synthesis of the earlier study reports their benchmark effects.
No other bounded-noise device appears in the verified records provided.
In particular, the verified EGJ and GG records use equal three-point weights.
Unequal weights, $N$ traders, and two-unit orders are marked unverified below.

### Result 11 (analytical and computer-assisted). Access to prices (Proposition A.9)

Hold $r_1$ fixed and hide the price from the challenger.
Entry is then $e_{r_1}(1/2) = \rho$ at each flow, since $B_{r_1}(1/2) < c_H$.
Suppose full trade is the equilibrium in both economies.
The flow experiment then coincides, as in the paper proof.
Let $\alpha_j = \Pr(\mu_X \ge \tau \mid j)$ under full trade.
The paper identities (A.41) give, with the discrete $\alpha_j$:

$$
\Delta \mathcal R_T = (1-\rho)\big[\pi \alpha_H w_H + (1-\pi)\alpha_L w_L\big] > 0,
$$
$$
\Delta \mathcal W = (1-\rho)\, \mathbb E\big[\{B_{r_1}(\mu_X) - c_H + p^2/r_1\}\, \mathbf 1\{\mu_X \ge \tau\}\big] > 0 .
$$

Each term in the welfare sum is at least $p^2/r_1 > 0$ on the recruiting set.
That set has positive probability because the top flow belongs to it.
The result is analytical given the coincident-orders premise.
For B1 the premise is checkable in closed form.
The hidden payoff falls in $\alpha$ by Result 5 with $e \equiv \rho$.
So $U_{\mathrm{hidden}}(\lambda) > 0$ implies unique full trade when hidden.
Access-side uniqueness at $r_1$ also needs $U(\alpha^{*-}) > 0$.
Exact values are $245519/8436000 > 0$ at $\theta = 3/20$ ($\alpha^* = 246/649$).
They are $2121/68000 > 0$ at $\theta = 1/5$ ($\alpha^* = 41/59$).
Since $U$ falls on each segment, its minimum on $[0,\lambda]$ is then positive.
Full trade is therefore the unique outcome at $r_1$ for S1 and S2.
For B2 and B3 rows the hidden payoff minimum on the $\alpha$ grid is positive.
Those rows therefore carry the label numerical diagnostic for uniqueness.
The level differences themselves are exact (computer-assisted):

| candidate at $r_1$ | $U_{\mathrm{hidden}}(\lambda)$ | $\Delta\mathcal R_T$ | $\Delta\mathcal W$ |
|---|---|---|---|
| B1 $\theta=3/20$ | $9/425$ | $123/320 \approx 0.3844$ | $31/64 \approx 0.4844$ |
| B1 $\theta=1/5$ | $3/100$ | $119/320 \approx 0.3719$ | $21/64 \approx 0.3281$ |
| B1 $\theta=9/20$ | $2/275$ | $127/320 \approx 0.3969$ | $41/64 \approx 0.6406$ |
| B1 $\theta=1/3$ (memo A) | $8/225$ | $9/64 \approx 0.1406$ | $61/192 \approx 0.3177$ |
| B2a $N=3, \theta=1/3$ | $5669/105300$ | $119/1728 \approx 0.0689$ | $35/576 \approx 0.0608$ |
| B2b $N=3, \beta=1/4$ | $449/12800$ | $1109/4096 \approx 0.2708$ | $867/4096 \approx 0.2117$ |
| B3a $\theta=1/3$, size 2 | $7/900$ per unit | $9/32 \approx 0.2813$ | $61/96 \approx 0.6354$ |

The paper proceeds gain at $r_1$ is $0.257809$.
B1 gains exceed it because entry $5/8$ exceeds paper entry.
B2a gains fall short because its recruiting mass is small.
Rows without trade in both economies are excluded from this claim.
The parity laws have no trade in either economy, so their gain is zero.

## 4. The scorecard of BRIEF §2, one table per candidate setup

Each table uses the benchmark $c_H = 6$, $k = 0.02$, strengths $1.2, 3, 3.6$.
Item numbers follow BRIEF §2.
Item 1 holds for every candidate by Result 3 and is not repeated in prose.
Item 3 fails for every candidate by Result 2; tables give the weaker path.

### S1. B1 with $\theta = 3/20$, $\lambda = 1$ (headline)

| Item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade, entry $1/4$, belief-free | analytical |
| 2. Prop. 2(ii) | Full trade; flows $1,2$ recruit; entry $5/8$; $\mathsf O_H = 71/160$ | computer-assisted |
| 3. Prop. 2(iii) | Fails: entry $5/8$ at $3.6$; steps to $49/160$ near $5.412$, to $1/4$ at $7.9686$ | analytical |
| 4. Prop. 3 | NT + full on $[1.6547, 1.8300]$; NT + $\alpha_A$ from $\approx 1.466$; ordered $\mathsf E_A$ at $1.55,1.60,1.65$ | computer-assisted |
| 5. Prop. A.9 | Holds: $\Delta\mathcal R_T = 123/320$, $\Delta\mathcal W = 31/64$ | analytical + exact levels |
| 6. Off-path | NT needs belief near $1$ only near its boundary; benchmark $r_0$ belief-free | analytical |
| 7. Ties, mixing | Full classification in Result 5; $\alpha_T$ needs (M, X); $\alpha_A$ needs M only | analytical |
| 8. Knob | $\theta$: noise tail weight, $\Pr(\text{noise trades}) = 2\theta = 0.30$; range in Result 6 | analytical + diagnostic |
| 9. Precedent | Support, menu, $\lambda$ from verified EGJ record; unequal weights unverified | unverified |
| 10. Labels | Shape and windows analytical; three strengths computer-assisted | as listed |

### S2. B1 with $\theta = 1/5$, $\lambda = 1$

| Item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade, entry $1/4$, belief-free | analytical |
| 2. Prop. 2(ii) | Full trade; $\mu_1 = 3/4$ recruits; entry $5/8$; $\mathsf O_H = 17/40$ | computer-assisted |
| 3. Prop. 2(iii) | Fails: entry $5/8$ at $3.6$; interior step at $r_C(3/4) = 4$ exact | analytical |
| 4. Prop. 3 | NT + full on $[1.5807, 1.8633]$; $\alpha_A$ at $1.55$ only; entry then flat $5/8$ | analytical + diagnostic |
| 5. Prop. A.9 | Holds: $\Delta\mathcal R_T = 119/320$, $\Delta\mathcal W = 21/64$ | analytical + exact levels |
| 6. Off-path | As S1 | analytical |
| 7. Ties, mixing | As S1; strict ordering at three strengths fails ($5/8$ twice) | analytical |
| 8. Knob | $\theta = 0.20$; stronger gap $7/80$, earlier full trade than S1 | analytical |
| 9. Precedent | As S1 | unverified |
| 10. Labels | Windows analytical; levels computer-assisted | as listed |

### S3. B1 with $\theta = 9/20$, $\lambda = 1$ (high side)

| Item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade, entry $1/4$, belief-free | analytical |
| 2. Prop. 2(ii) | Full trade; flow $0$ recruits ($\mu_0 = 9/11$); entry $5/8$ | computer-assisted |
| 3. Prop. 2(iii) | Fails: entry $5/8$ at $3.6$; ceiling $7.9686$ | analytical |
| 4. Prop. 3 | NT + full on $[1.8508, 2.1073]$; misses $[1.55,1.65]$; $\alpha_A$ at $1.65$ only | diagnostic |
| 5. Prop. A.9 | Holds: $\Delta\mathcal R_T = 127/320$, $\Delta\mathcal W = 41/64$ | analytical + exact levels |
| 6. Off-path | As S1 | analytical |
| 7. Ties, mixing | As S1 | analytical |
| 8. Knob | $\theta = 0.45$: noise trades with probability $0.90$; flow $0$ camouflages | analytical |
| 9. Precedent | As S1 | unverified |
| 10. Labels | Levels computer-assisted; branch points diagnostic | as listed |

### S4. B2a with $N = 3$, per-trader $\theta = 1/3$, $\lambda = 1$

| Item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade, entry $1/4$, belief-free | analytical |
| 2. Prop. 2(ii) | Full trade; flows $3,4$ recruit; entry $23/72 \approx 0.319$ | computer-assisted |
| 3. Prop. 2(iii) | Fails: entry $23/72$ at $3.6$; ceiling $7.9686$ | analytical |
| 4. Prop. 3 | Window $\approx [1.582, 1.766]$; no mixed root found at $1.55$; ordering not shown | numerical diagnostic |
| 5. Prop. A.9 | Full-vs-full gains positive and small: $0.0689$, $0.0608$ | analytical levels; diagnostic uniqueness |
| 6. Off-path | One unused top flow under NT; completion $v=1$ | analytical |
| 7. Ties, mixing | Existence under (M, X); roots on grid only | analytical + diagnostic |
| 8. Knob | $N$: number of noise traders; useful $N \in \{2,\dots,5\}$; gap $\to 0$ in $N$ | analytical limit |
| 9. Precedent | Per-trader law is EGJ's; $N$-fold sum in one shot unverified | unverified |
| 10. Labels | Benchmark rows computer-assisted; windows diagnostic | as listed |

### S5. B2b with $N = 3$, $\beta = 1/4$, $\lambda = 1$

| Item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade, entry $1/4$, belief-free | analytical |
| 2. Prop. 2(ii) | Full trade; flows $2,3,4$ recruit; entry $269/512 \approx 0.525$ | computer-assisted |
| 3. Prop. 2(iii) | Fails: same entry at $3.6$; ceiling $7.9686$ | analytical |
| 4. Prop. 3 | Window $\approx [1.612, 1.755]$; grid roots suggest ordered entry | numerical diagnostic |
| 5. Prop. A.9 | Gains $1109/4096$ and $867/4096$ on full branch | analytical levels; diagnostic uniqueness |
| 6. Off-path | One unused top flow under NT; completion $v=1$ | analytical |
| 7. Ties, mixing | Existence under (M, X); branch order uncertified | analytical + diagnostic |
| 8. Knob | $(N, \beta)$: count and buy rate of one-sided noise; small $N$ only | analytical limit |
| 9. Precedent | No one-sided noise in verified EGJ or GG records | unverified |
| 10. Labels | Benchmark rows computer-assisted; branches diagnostic | as listed |

### S6. B3a with fixed size two, $\theta = 1/3$, $\lambda = 1$

| Item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | No trade at $r_0$, entry $1/4$ | analytical |
| 2. Prop. 2(ii) | Full two-unit trade; entry $1/2$; $\mathsf O_H = 3/8$ | computer-assisted |
| 3. Prop. 2(iii) | Fails: entry $1/2$ at $3.6$; ceiling $7.9686$ | analytical |
| 4. Prop. 3 | Fails: single cutoff at $r \approx 2.5711$; coexistence only at the tie | analytical |
| 5. Prop. A.9 | Holds with same orders: $\Delta\mathcal R_T = 9/32$, $\Delta\mathcal W = 61/96$ | analytical |
| 6. Off-path | Two unused top flows under NT; beliefs $1$ by dominance | analytical |
| 7. Ties, mixing | Payoff constant in $\alpha$; tie gives a continuum under M | analytical |
| 8. Knob | Order size $2$; trade at $r_1$ needs $\theta > 6/25$ in B1 noise | analytical |
| 9. Precedent | EGJ orders are unit size; size mismatch unverified | unverified |
| 10. Labels | Analytical throughout; levels computer-assisted | as listed |

Two reference points help read the tables.
Equal weights $\theta = 1/3$ give entry $3/8$ at $r_1$ and no feedback (memo A).
The paper gives entry $0.5228$ at $r_1$ and return at $3.6$.
S1 beats the paper entry level but not its return or its ordering location.
The discrete-Laplace bar beats S1 on the ceiling and on window placement.
S1 matches its buy-only entry $0.625$ without moving $c_H$ from $6$.

## 5. Numerical example (benchmark values where possible)

Take S1: B1 with $\theta = 3/20$, $\lambda = 1$, at $r_1 = 3$.
Noise is $(3/20, 7/10, 3/20)$, so noise abstains with probability $0.70$.
Full trade is the unique outcome (Result 11 checks).
Flow-by-flow values under full trade are exact (computer-assisted):

| flow $x$ | $\mu_x$ | entry $e_x$ | price $P_x$ | mass $w_x$ |
|---|---|---|---|---|
| $-1$ | $0$ | $1/4$ | $17/32 = 0.531250$ | $3/40$ |
| $0$ | $3/17$ | $1/4$ | $305/544 \approx 0.560662$ | $17/40$ |
| $1$ | $14/17$ | $1$ | $581/408 \approx 1.424020$ | $17/40$ |
| $2$ | $1$ | $1$ | $37/24 \approx 1.541667$ | $3/40$ |

Masses use $w_x = (f_H(x) + f_L(x))/2$ at $\alpha = 1$.
The recruiting mass is $w_1 + w_2 = 17/40 + 3/40 = 1/2$.
Entry is $\mathsf E = 1/4 + (3/4)(1/2) = 5/8$.
Ownership is $\mathsf O_H = 71/160 = 0.443750$.
Proceeds are $\mathcal R_T = 959/960 \approx 0.998958$.
Welfare is $\mathcal W = 583/192 \approx 3.036458$ before trading costs.
The purchase payoffs are $U_H = 141/1700 \approx 0.082941$.
They are $U_L = -5189/10200 \approx -0.508725$ from the residual formula.
Price access gains are $\Delta\mathcal R_T = 123/320$ and $\Delta\mathcal W = 31/64$.

The strength path on the selected branches is:

- $r \le 1.466$ about: no trade only, entry $1/4$ (diagnostic lower edge).
- $1.55, 1.60, 1.65$: no trade plus $\alpha_A$ plus threshold outcome.
  Branch entry is $0.4953 < 0.5496 < 0.6174$ (computer-assisted).
- $[1.6547, 1.8300]$: no trade plus full trade at entry $5/8$.
- $r = 3$ and $r = 3.6$: full trade at entry $5/8$ in the computed rows.
- Near $r = 5.412$: flow $1$ stops recruiting; entry steps to $49/160$.
- Above $r = 7.9686$: entry $1/4$ with informative full trade.

Commands and run times are at the head of this memo.
Output files are `t3_exact.out.txt`, `t3_branches.out.txt`, `t3_scan.out.txt`.
The equal-weight row in the exact output reproduces memo A exactly.
It gives $\mathsf E = 3/8$, $\mathcal R_T = 145/192$, $\mathcal W = 551/192$ at $r_1$.
That match checks the engine against an independent earlier solver.

## 6. Open issues

1. **Full correspondence in $r$ for B1.**
   Fixed-$r$ outcomes are classified in Result 5.
   The birth and death strengths of each branch are only bracketed numerically.
   In particular $r_I$ and the end of the threshold branch lack closed forms.
   Status: **open** beyond the stated diagnostics.

2. **Mixed branches for B2 and combined levers.**
   Grid roots suggest ordered entry for B2b with $N=3$, $\beta=1/4$.
   No exact bracket or slope proof is given for multi-flow laws.
   Status: **open**; current evidence is a numerical diagnostic.

3. **Mixed order sizes in menu $\{0,1,2\}$.**
   Pure sizes both fail at $r_1$ for $\theta = 2/5$ on the exact grid.
   Existence and outcomes under size mixing are not solved here.
   Status: **conjecture** that (M, X) restores existence; otherwise open.

4. **General prior and general value classes.**
   Benchmark results use $\pi = 1/2$ and point masses.
   Memos A and C9 give general-$\pi$ formulas for three-point noise.
   The B1 window formulas at $\pi \ne 1/2$ are not recomputed here.
   Status: **open** for the symmetric window claim.

5. **Why symmetric unequal weights?**
   The knob $\theta$ has a clear meaning as noise trading intensity.
   No verified source in the records uses unequal three-point weights.
   A micro-foundation or calibration story would need separate work.
   Status: **open**, and the precedent stays unverified.

6. **Presence below one with certificates.**
   Exact certificates use $\lambda = 1$.
   Float tables keep ordered entry at $\lambda = 0.9$ and $0.75$ for S1.
   Exact brackets at $\lambda < 1$ are mechanical but not produced here.
   Status: **open** as certificates; diagnostic as economics.

7. **Uniqueness at $r_1$ for B2 candidates.**
   The A.9 comparison uses full trade in both economies.
   Grid minima support it, but no shape theorem is proved for B2 payoffs.
   Status: **open** as a uniqueness claim.

## 7. Plain summary, 300 words at most

This memo keeps buy-only trade and changes only bounded noise.
The low class never buys, and prices reveal market beliefs.
At the weak strength no trade is the only outcome for every law.

One loss is universal.
The largest flow needs a purchase, so it reveals the high class.
It recruits the challenger at strength $3.6$.
Entry therefore stays above the floor while trade is informative.
Entry returns to the floor only above strength $7.97$.
No change in weights, trader count, order size, or presence can avoid this.
Only a much higher preparation cost, a lower high value, or a later strength can.

Symmetric unequal weights repair the other losses.
With tail weight near $0.15$, the middle flow recruits but still pays the buyer.
Entry at strength $3$ is $0.625$, above the paper value.
No trade and informative trade coexist over a wide interval.
Exact checks give rising entry at strengths $1.55$, $1.60$, and $1.65$.
Many noise traders dilute the signal and give lower entry.
Two fixed units give entry $0.5$ but no feedback and no coexistence.
Noise without abstention destroys trade by parity.

The best lever is symmetric weights $(3/20, 7/10, 3/20)$.
Its cost is a step away from equal EGJ weights, with no verified precedent.
