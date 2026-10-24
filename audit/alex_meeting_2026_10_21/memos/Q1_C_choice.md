# Point 1, Reading C: the challenger chooses its value distribution

## 1. Question and reading

This memo covers supervisor point 1 under Reading C.
Reading C has one core idea.
The challenger chooses one value distribution from a menu before preparation.
An integration plan with a given risk profile is one example.
The challenger learns the realized value only after diligence.
Diligence is the preparation step in the paper.

The memo asks four questions.

- What does the cash second-price auction imply for that choice?
- What does the target's traded claim then look like?
- How does incumbent strength change the preferred choice?
- Can "competition creates competition" survive the change in timing?

The short answer has two parts.
The auction stage gives a clean and neat result.
The full trading model does not, under a pure form of Reading C.
Section 3 proves the first part.
Claims 10 to 12 prove the limits in the second part.
Claim 13 compares Reading C with Reading N.

Reading N is the other reading in the shared brief.
Under Reading N, nature draws the distribution.
The investor observes the distribution.
The challenger knows neither the distribution nor the value before preparation.
This memo does not develop Reading N.
It only compares the two readings at the end.

## 2. Formal setup

Notation follows the paper, with one change.
Write $\Gamma$ for a challenger value law (a cdf on $[0,\infty)$).
The brief writes $G_j$ for such a law.
The paper uses $G_\theta(F)$ for a profit in equation (6).
This memo avoids that symbol for a law.

### 2.1 Auction stage

- The seller commits to a cash second-price auction with reserve $p>0$.
- The incumbent has value $R$ with continuous cdf $F$ on $[0,\bar r]$.
- Extend $F$ by $F(u)=1$ for $u>\bar r$, as in Proposition 1.
- Assume $p<\bar r$, so the incumbent can meet the reserve with values above it.
- The incumbent is already prepared and knows $R$ at the bid stage.
- A prepared challenger learns its value $\theta$ and then bids.
- Truthful bids are weakly dominant for both bidders.
- This fact does not depend on beliefs about $\Gamma$.
- A bid at the reserve is admissible, as in the paper.
- All agents are risk neutral. Values are per share.
- The target standalone value is $0$, as in the paper.
- $R$ is independent of $\theta$ and of the preparation cost.

A plan is one law $\Gamma$ in a menu $\mathcal M$.
Each $\Gamma$ has finite mean $m(\Gamma)=\int \theta\,d\Gamma(\theta)$.
Write $S_\Gamma(u)=\Pr_\Gamma(\theta>u)$ for the survival function.
A law may put mass below $p$.
A law may have atoms, for example a two-point law.
Ties between $R$ and $\theta$ then still have probability zero.
The reason is that $F$ is continuous.

At a known value $\theta$, define two functions.

- $g(\theta)$ is the challenger's gross profit from entry.
- The profit is gross of the preparation cost.
- $t(\theta)$ is the target's expected proceeds given entry at $\theta$.
- Both expectations are over $R$ only.

Write $t_0$ for expected proceeds with no entry.
For a plan $\Gamma$, write $\bar g(\Gamma)=\int g(\theta)\,d\Gamma(\theta)$.
Write $\bar t(\Gamma)=\int t(\theta)\,d\Gamma(\theta)$ in the same way.
The dependence on $F$ and $p$ is implicit unless stated.

### 2.2 Preparation and entry

Preparation costs follow the paper.
The cost $C$ equals $c_L$ with probability $\rho$ and $c_H$ otherwise.
Assume $0\le c_L<c_H$ and $0<\rho<1$.
Payment of $C$ reveals $\theta$ and permits a bid.
A challenger with $\theta<p$ after diligence cannot bid.
Preparation and admissibility then differ, as in Section 6.3 of the paper.

The baseline menu has no direct plan cost.
Section 3 notes each place where a plan cost would change a result.
The challenger must commit to $\Gamma$ before diligence.
After diligence it cannot redraw $\theta$ from another law.
This commitment is an assumption, not a result.

### 2.3 Orders over laws

Law $\Gamma_2$ first-order dominates law $\Gamma_1$ if $S_{\Gamma_2}(u)\ge S_{\Gamma_1}(u)$ for all $u$.
Law $\Gamma_r$ is a mean-preserving spread of law $\Gamma_s$ if two facts hold.
First, $m(\Gamma_r)=m(\Gamma_s)$.
Second, $\int\phi\,d\Gamma_r\ge\int\phi\,d\Gamma_s$ for every convex $\phi$.
A two-point spread around a sure value is the leading case.

Incumbent law $F_1$ is stronger than $F_0$ if $F_1(u)\le F_0(u)$ for all $u$.
That is first-order dominance, as in Proposition 1.
For $R\sim U[0,r]$, a larger $r$ is a stronger incumbent.

### 2.4 Timing variants for Section 3, part D

Trading, noise, and pricing follow the paper unless a variant states otherwise.
The investor submits $q\in[-1,1]$ at linear cost $k|q|$.
Noise $Z$ is Laplace with scale $b>1$. Flow is $X=q+Z$.
Competitive market makers set $P(X)=\mathbb E[V_T\mid X]$.
The challenger observes the price and its cost, not the flow.

Three timings receive separate treatment.

- **V1.** The challenger chooses $\Gamma$ before trading.
- **V2.** The challenger chooses risk after it observes the price.
- **V3.** Nature draws a type. The challenger then chooses risk after the price.

Each variant states what the investor observes.
The auction-stage claims 1 to 9 need no timing variant.
They hold at any fixed plan and any fixed entry event.

## 3. Results

### Part A. Profit and proceeds at a known value

**Claim 1 (formulas and shapes; analytical).**
For $\theta\ge p$,

$$
g(\theta)=\int_p^\theta F(u)\,du,
\qquad
t(\theta)=p+\int_p^\theta [1-F(u)]\,du,
\qquad
g(\theta)+t(\theta)=\theta.
$$

For $\theta<p$, $g(\theta)=0$ and $t(\theta)=t_0=p[1-F(p)]$.
The function $g$ is convex and nondecreasing on $[0,\infty)$.
The function $t$ is concave and nondecreasing on $[p,\infty)$.
At $\theta=p$, $g$ is continuous with a kink.
At $\theta=p$, $t$ jumps up by $pF(p)$.
For $\theta\ge\bar r$, $t$ is flat and $g$ has slope $1$.

*Derivation.*
Fix $\theta\ge p$ and $R$.
The challenger's realized gross profit is $(\theta-\max\{p,R\})_+$.
The target's realized proceeds are $\max\{p,\min(R,\theta)\}$.
The sale is sure because the challenger bid meets the reserve.
Two indicator identities hold for each $R$:

$$
(\theta-\max\{p,R\})_+=\int_p^\theta \mathbf 1\{R<u\}\,du,
\qquad
\max\{p,\min(R,\theta)\}=p+\int_p^\theta \mathbf 1\{R>u\}\,du.
$$

Check the first identity by three cases.
If $R\le p$, both sides equal $\theta-p$.
If $p<R<\theta$, both sides equal $\theta-R$.
If $R\ge\theta$, both sides equal $0$.
Check the second identity by the same three cases.
The three values are $p$, then $R$, then $\theta$.
Tonelli's theorem applies because the integrands are nonnegative.
Take expectations over $R$.
Continuity of $F$ gives $\Pr(R<u)=F(u)$ and $\Pr(R>u)=1-F(u)$.
The two integral formulas follow, as in Appendix A.1, equation (A.2).
Add the two formulas.
The integrands sum to $1$, so $g(\theta)+t(\theta)=p+(\theta-p)=\theta$.

Now take $\theta<p$.
The challenger cannot submit an admissible bid.
Realized profit is $0$.
The target receives $p\mathbf 1\{R\ge p\}$, as with no entry.
Hence $t(\theta)=p\Pr(R\ge p)=p[1-F(p)]=t_0$.

For curvature, write $Y=\max\{p,R\}$.
Then $g(\theta)=\mathbb E[(\theta-Y)_+]$ for all $\theta$.
The map $\theta\mapsto(\theta-Y)_+$ is convex for each $Y$.
It is the maximum of two affine maps, $0$ and $\theta-Y$.
Expectation preserves convexity. So $g$ is globally convex.
For $\theta\ge p$, $t(\theta)=\mathbb E[\min(Y,\theta)]$.
The map $\theta\mapsto\min(Y,\theta)$ is concave for each $Y$.
It is the minimum of a constant and the identity.
Expectation preserves concavity. So $t$ is concave on $[p,\infty)$.
Both functions are nondecreasing by the same representations.

Derivatives make the split of a marginal unit of value clear.
Since $F$ is continuous, for $\theta>p$,

$$
g'(\theta)=F(\theta),\qquad t'(\theta)=1-F(\theta),\qquad g'(\theta)+t'(\theta)=1.
$$

Where a density $f$ exists, $g''(\theta)=f(\theta)\ge0$ and $t''(\theta)=-f(\theta)\le0$.
A small rise in $\theta$ pays the challenger when $R<\theta$.
That event has probability $F(\theta)$.
The rise pays the target when $R>\theta$.
In that event the incumbent wins and pays $\theta$.
That event has probability $1-F(\theta)$.

At $p$, $g(p)=0$ from both sides, so $g$ is continuous.
The left slope is $0$. The right slope is $F(p)$.
Hence the kink, unless $F(p)=0$.
For $t$, the left limit at $p$ is $t_0=p-pF(p)$.
The value at $p$ is $t(p)=p$.
The gap is $pF(p)$.
The economic source is sale failure.
Just below $p$, no sale occurs when $R<p$.
At $p$, the challenger bid removes that event.

For $\theta\ge\bar r$, $F(\theta)=1$.
So $t'(\theta)=0$ and $g'(\theta)=1$.
Also $t(\theta)=\mathbb E[Y]$ for all such $\theta$.
This ends the derivation. $\square$

Two accounting remarks complete part A.
First, $g(\theta)+t(\theta)=\theta$ is not total surplus.
The incumbent keeps rent $i(\theta)=\mathbb E[(R-\max\{p,\theta\})_+]$.
For $\theta\ge p$, $i(\theta)=\int_\theta^{\bar r}[1-F(u)]\,du$.
Total surplus at $\theta\ge p$ is $\mathbb E[\max(R,\theta)]=g(\theta)+t(\theta)+i(\theta)$.
Second, Claim 1 reproduces equation (4) of the paper.
For $R\sim U[0,r]$ and $p\le\theta\le r$, $g(\theta)=(\theta^2-p^2)/(2r)$.
Also $t(\theta)=\theta-(\theta^2-p^2)/(2r)$.
For $\theta>r$, $g(\theta)=\theta-r/2-p^2/(2r)$ and $t(\theta)=r/2+p^2/(2r)$.
Set $\theta=\ell$ and $\theta=h$ to recover $g_L,g_H,t_L,t_H$.
Section 5 prints these values from both forms.

Strictness in Claim 1 is also exact **(analytical)**.
For $p<\theta-d<\theta<\theta+d$,

$$
g(\theta+d)+g(\theta-d)-2g(\theta)
=\int_\theta^{\theta+d}F(u)\,du-\int_{\theta-d}^\theta F(u)\,du\ge0.
$$

The difference is strictly positive iff $F$ is not constant on $[\theta-d,\theta+d]$.
The $t$ second difference is the negative of this quantity.
The reason is that $g+t$ is affine on $[p,\infty)$.

### Part B. Which law each side prefers

**Claim 2 (survival weights and first-order dominance; analytical).**
For any plan $\Gamma$ with finite mean,

$$
\bar g(\Gamma)=\int_p^\infty F(u)S_\Gamma(u)\,du,
$$

$$
\bar t(\Gamma)=t_0+pF(p)\Pr_\Gamma(\theta\ge p)
+\int_p^\infty [1-F(u)]S_\Gamma(u)\,du.
$$

If $\Gamma_2$ first-order dominates $\Gamma_1$, then $\bar g$ and $\bar t$ are both weakly higher at $\Gamma_2$.

*Derivation.*
For each $\theta$, Claim 1 gives $g(\theta)=\int_p^\infty F(u)\mathbf 1\{u<\theta\}\,du$.
Integrate over $\Gamma$ and swap the two integrals by Tonelli's theorem.
The inner probability is $\Pr_\Gamma(\theta>u)=S_\Gamma(u)$.
Finite mean gives $\int_p^\infty S_\Gamma(u)\,du\le m(\Gamma)<\infty$.
So the swap is valid and the first formula follows.

For $t$, write one identity that holds for all $\theta$:

$$
t(\theta)=t_0+pF(p)\mathbf 1\{\theta\ge p\}
+\int_p^\infty [1-F(u)]\mathbf 1\{u<\theta\}\,du.
$$

For $\theta<p$ both extra terms are zero, so the identity gives $t_0$.
For $\theta\ge p$ use $t_0+pF(p)=p$ and Claim 1.
Integrate over $\Gamma$ and swap integrals as before.
The second formula follows.
An atom at $p$ counts in $\Pr_\Gamma(\theta\ge p)$.
Such a bid is admissible, so the count is correct.

Both weights, $F(u)$ and $1-F(u)$, are nonnegative.
First-order dominance raises $S_\Gamma(u)$ at each $u$.
It also weakly raises $\Pr_\Gamma(\theta\ge p)$.
Hence both $\bar g$ and $\bar t$ weakly rise. $\square$

Claim 2 verifies the two integral checks in the brief, with $\Gamma$ in place of $G$ **(analytical)**.
Take two laws $\Gamma_H$ and $\Gamma_L$ with $\Gamma_H$ dominant.
Then $\bar g(\Gamma_H)-\bar g(\Gamma_L)=\int g(\theta)\,d(\Gamma_H-\Gamma_L)(\theta)$ by definition of $\bar g$.
Claim 2 also writes this gap as $\int_p^\infty F(u)[S_H(u)-S_L(u)]\,du$.
If both laws put all mass at or above $p$, the target gap is

$$
\bar t(\Gamma_H)-\bar t(\Gamma_L)
=\int_p^\infty [1-F(u)][\Gamma_L(u)-\Gamma_H(u)]\,du\ge0,
$$

because $S_H(u)-S_L(u)=\Gamma_L(u)-\Gamma_H(u)$.
The integrand shows the opposition of weights.
The challenger weights high $u$ more, since $F$ rises in $u$.
The target weights low $u$ more, since $1-F$ falls in $u$.
First-order shifts raise survival at all $u$, so both sides gain.
Mean-preserving spreads move survival from low $u$ to high $u$.
The two sides then move in opposite ways. Claim 3 states this result.

**Claim 3 (mean-preserving spreads above the reserve; analytical).**
Let $\Gamma_r$ be a mean-preserving spread of $\Gamma_s$.
Let both laws put all mass on $[p,\infty)$.
Then the challenger weakly prefers the risky law and the target weakly prefers the safe law:

$$
\bar g(\Gamma_r)\ge\bar g(\Gamma_s),
\qquad
\bar t(\Gamma_r)\le\bar t(\Gamma_s),
\qquad
\bar g(\Gamma_r)-\bar g(\Gamma_s)=-[\bar t(\Gamma_r)-\bar t(\Gamma_s)].
$$

Total surplus $\bar w(\Gamma)=\int\mathbb E[\max(R,\theta)]\,d\Gamma(\theta)$ weakly rises under the spread.
Expected incumbent rent also weakly rises.
For a two-point spread $\{m-d,m+d\}$ around a sure $m$, all three gaps are strict iff $F$ is not constant on $[m-d,m+d]$.

*Derivation.*
By Claim 1, $g$ is convex and $t$ is concave on $[p,\infty)$.
The definition of a mean-preserving spread in Section 2.3 now applies with $\phi=g$ and $\phi=-t$.
The first two inequalities follow at once.
Pointwise $g(\theta)+t(\theta)=\theta$ on $[p,\infty)$ by Claim 1.
Integrate over each law.
Both sums equal the common mean. The zero-sum equality follows.
For total surplus, $\theta\mapsto\max(R,\theta)$ is convex for each $R$.
Expectation over $R$ keeps convexity in $\theta$.
Apply the spread definition once more.
Expected incumbent rent is $\bar w(\Gamma)-m(\Gamma)$ on this support, because $\bar g+\bar t=m(\Gamma)$.
The mean is fixed, so rent moves with $\bar w$.
Strictness for the two-point case is the strictness remark after Claim 1. $\square$

The economic reading is direct.
The second-price rent is an option on the challenger's own value.
The option pays only in the win event, and its strike is $\max\{p,R\}$.
Options gain from spread. The target holds the concave side of the split.
At a fixed mean and a fixed entry event, the gain of one side is the loss of the other.
Total surplus still rises with spread.
The extra surplus goes to the two bidders, not to the target.

This opposition is specific to the payment rule **(analytical)**.
Section 6.2 of the paper has a zero-reserve bargaining rule with seller weight $\eta$.
Expected target receipts at value $\theta$ are $t_\eta(\theta)=\mathbb E[(1-\eta)\min(R,\theta)+\eta\max(R,\theta)]$.
Differentiation under the expectation gives $t_\eta'(\theta)=(1-\eta)[1-F(\theta)]+\eta F(\theta)$.
This slope rises in $\theta$ iff $\eta>1/2$ and falls iff $\eta<1/2$.
So $t_\eta$ is convex for $\eta>1/2$ and concave for $\eta<1/2$.
The challenger profit there is $(1-\eta)\int_0^\theta F(u)\,du$, which is convex for all $\eta<1$.
Hence target risk aversion over challenger laws holds only for $\eta<1/2$.
The cash second-price auction with zero reserve is the case $\eta=0$.
The reserve in the benchmark adds the jump of Claim 1, but not a sign change above $p$.

**Claim 4 (the reserve breaks global target risk aversion; analytical).**
The challenger prefers a mean-preserving spread even if the spread crosses $p$.
The target has no global risk attitude over laws that cross $p$.
If a safe law sits below $p$, a spread with mass above $p$ can strictly raise $\bar t$.

*Derivation.*
Claim 1 proves that $g$ is convex on all of $[0,\infty)$.
The kink at $p$ has left slope $0$ and right slope $F(p)\ge0$.
So the spread result for $\bar g$ needs no support restriction.
For the target, take a sure value $a<p$ and a spread $\{a-d,a+d\}$ with equal weights and $a+d>p$.
Claim 2 gives $\bar t$ for the sure law as $t_0$.
For the spread law, $\bar t-t_0=\tfrac12\big[pF(p)+\int_p^{a+d}[1-F(u)]\,du\big]$.
This term is strictly positive if $F(p)>0$, or if $F(u)<1$ on a subset of $[p,a+d]$ with positive length.
So the target strictly prefers the risky law in this case.
Claim 3 gives the opposite ranking for laws above $p$.
No single global ranking can cover both cases. $\square$

Section 5, item 5, prints one such case at the benchmark reserve **(numerical diagnostic)**.
A sure value of $0.4$ gives $\bar t=t_0=0.416667$ at $r=3$.
The equal spread $\{0,0.8\}$ gives $\bar t=0.575833$.
The challenger also gains, from $0$ to $0.032500$.
Risk that creates an admissible bid helps both sides.
Risk after admissibility splits the two sides.
Any reserve design result must keep the two margins apart.

**Claim 5 (the mean alone does not rank plans; analytical).**
Neither $\bar g$ nor $\bar t$ is a function of the plan mean.
A plan with a lower mean can beat a plan with a higher mean for either side.

*Derivation.*
Start with a strict two-point spread on $[p,\infty)$ with challenger premium $\Pi>0$.
Such a spread exists by the strictness part of Claim 3, at any $m$ where $F$ is not locally constant.
Shift each point of the risky law down by $\delta$, with $0<\delta<\Pi$ and support still at or above $p$.
The mean falls by $\delta$.
Both $g$ and $t$ have slopes in $[0,1]$ on $[p,\infty)$, by Claim 1.
So $\bar g$ falls by at most $\delta$ under the shift.
The shifted risky law still beats the safe law for the challenger, now at a lower mean.
For the target, shift the safe law down by $\delta$ in the same way.
Its $\bar t$ falls by at most $\delta<\Pi$, so it still beats the risky law at a lower mean. $\square$

**Claim 6 (an unrestricted menu gives a corner choice; analytical).**
Let the menu contain all laws on $[0,\bar\theta]$ with a fixed mean $m$.
The challenger then chooses the two-point law on $\{0,\bar\theta\}$ with $\Pr(\theta=\bar\theta)=m/\bar\theta$.
If support must lie in $[p,\bar\theta]$, the choice is the two-point law on $\{p,\bar\theta\}$ with the mean matched.
If $\bar\theta$ is unbounded and $m>0$, $\bar g$ has supremum $m$ and no maximizer.

*Derivation.*
A convex function lies below the chord between two support endpoints.
On $[0,\bar\theta]$, $g(\theta)\le (\theta/\bar\theta)g(\bar\theta)$ because $g(0)=0$.
Take expectations at mean $m$.
Then $\bar g\le (m/\bar\theta)g(\bar\theta)$, with equality for the stated two-point law.
The $[p,\bar\theta]$ case uses the chord between $p$ and $\bar\theta$ in the same way.
For the unbounded case, take $\{0,H\}$ with $\Pr(\theta=H)=m/H$ and $H\ge\bar r$.
Then $g(H)=H-\mathbb E[\max\{p,R\}]$ by Claim 1.
So $\bar g=m\big(1-\mathbb E[\max\{p,R\}]/H\big)$, which tends to $m$ as $H\to\infty$.
No law can exceed $m$ on $[p,\infty)$ mass, since $g(\theta)\le\theta$ there and $g=0$ below $p$.
Hence the supremum claim. $\square$

Claim 6 is neat but degenerate.
A useful menu needs a trade-off.
Three trade-offs are natural: a lower mean for a risky plan, a direct plan cost, or a support cap.
Without one of them, Reading C predicts a maximal gamble and no interior choice.
Section 5, item 6, uses the first trade-off.

**Claim 7 (entry does not change the challenger ranking; analytical).**
Fix the information that the challenger has at the entry decision.
If that information gives gross value $\bar g(\Gamma)$ for plan $\Gamma$, then the challenger ranks plans by $\bar g$.
This ranking holds if the cost is known, and it holds in expectation if the cost is not yet known.
The target ranking need not agree once entry responds to the plan.

*Derivation.*
With known cost $C$, plan $\Gamma$ yields $\max\{0,\bar g(\Gamma)-C\}$.
This payoff is nondecreasing in $\bar g(\Gamma)$.
With the two-point cost of the paper, the ex ante payoff is $\rho(\bar g-c_L)_++(1-\rho)(\bar g-c_H)_+$.
Each term is nondecreasing in $\bar g$.
So the sum is nondecreasing in $\bar g$.
A direct plan cost $\kappa(\Gamma)$ would change the objective to a function of $\bar g(\Gamma)-\kappa(\Gamma)$.
The baseline menu has $\kappa=0$.

For the target, define $e(\Gamma)$ as the entry probability at plan $\Gamma$.
Expected proceeds are $T(\Gamma)=t_0+e(\Gamma)[\bar t(\Gamma)-t_0]$.
Entry weakly raises realized proceeds at each $(R,\theta)$.
With no entry the payment is $p\mathbf 1\{R\ge p\}$.
With entry and $\theta\ge p$ the payment is at least $p$.
With entry and $\theta<p$ the payment is unchanged.
Hence $\bar t(\Gamma)\ge t_0$ and the bracket is nonnegative.
A risky plan lowers $\bar t$ by Claim 3 but can raise $e(\Gamma)$ by a jump.
Under the cost floor $c_L<\bar g(\Gamma)$, $e(\Gamma)=\rho+(1-\rho)\mathbf 1\{\bar g(\Gamma)\ge c_H\}$.
If the safe plan has $e=\rho$ and the risky plan has $e=1$, the target prefers the risky plan iff

$$
\bar t(\Gamma_r)-t_0>\rho\,[\bar t(\Gamma_s)-t_0].
$$

The left side is positive, so the entry jump can dominate the concave loss. $\square$

Claim 7 splits two target objects that the paper keeps apart as well.
Conditional on entry, target shareholders dislike challenger risk above $p$.
Without the condition, they may like the same risk because it recruits entry.
Any statement of the form "the target prefers plan X" must name the object.

### Part C. Incumbent strength and the preferred choice

**Claim 8 (levels at a fixed plan; analytical).**
Let $F_1$ be stronger than $F_0$, so $F_1(u)\le F_0(u)$ for all $u$.
At each fixed plan $\Gamma$, $\bar g$ weakly falls and $\bar t$ weakly rises.
At each fixed pair $p\le\theta_L<\theta_H$, the spread $t(\theta_H)-t(\theta_L)$ weakly rises.
At each fixed pair of laws with $\Gamma_H$ dominant over $\Gamma_L$ and mass on $[p,\infty)$, the spread $\bar t(\Gamma_H)-\bar t(\Gamma_L)$ weakly rises.
Strictness holds when the fall in $F$ has positive integral on the relevant range, with the survival weight of Claim 2 in place for law comparisons.

*Derivation.*
Claim 2 writes $\bar g(\Gamma)=\int_p^\infty F(u)S_\Gamma(u)\,du$.
A pointwise fall in $F$ lowers the integral because $S_\Gamma\ge0$.
Pointwise in $\theta\ge p$, $t(\theta)=p+\int_p^\theta[1-F(u)]\,du$ rises as $F$ falls.
Also $t_0=p[1-F(p)]$ rises.
Hence $\bar t(\Gamma)$ rises for each fixed $\Gamma$.
For a fixed pair, $t(\theta_H)-t(\theta_L)=\int_{\theta_L}^{\theta_H}[1-F(u)]\,du$ by Claim 1.
The integral rises as $F$ falls.
For a fixed pair of laws, the gap formula after Claim 2 has weight $1-F$ and a nonnegative survival gap.
The same step applies.
This claim is Proposition 1 of the paper at a general fixed plan. $\square$

Claim 8 concerns levels at a fixed plan.
Choice concerns a difference between plans.
The two objects need not move in the same way.
Claim 9 shows that they do not in general.

**Claim 9 (the risk premium has no signed response to incumbent strength; analytical).**
Take a safe law $\delta_m$ and a risky law $\{m-d,m+d\}$ with equal weights, with $p<m-d$.
The challenger risk premium is

$$
\Pi_g(F)=\frac12\left[\int_m^{m+d}F(u)\,du-\int_{m-d}^{m}F(u)\,du\right]\ge0.
$$

Under a stronger law $F_1\le F_0$, write $D(u)=F_0(u)-F_1(u)\ge0$ for the drop.
Then

$$
\Pi_g(F_1)-\Pi_g(F_0)
=\frac12\left[\int_{m-d}^{m}D(u)\,du-\int_m^{m+d}D(u)\,du\right].
$$

First-order dominance alone signs neither term against the other.
Both signs occur in the uniform model of the paper.

*Derivation.*
The premium is $\tfrac12[g(m+d)+g(m-d)]-g(m)$.
Write each $g$ term with Claim 1 and cancel the common part on $[p,m-d]$.
The first formula follows.
Nonnegativity follows because $F$ is nondecreasing, so the upper integral weakly exceeds the lower one.
Replace $F$ by $F_1-F_0=-D$ in the same formula.
The second formula follows.

Now take $R\sim U[0,r]$, so $F_r(u)=\min(u/r,1)$.
*Interior case.* Let $m+d<r_0<r_1$.
Then $g(\theta)=(\theta^2-p^2)/(2r)$ at all three points.
Direct algebra gives $\Pi_g=d^2/(2r)$.
The premium falls as $r$ rises.
In drop terms, $D(u)=u(1/r_0-1/r_1)$ rises in $u$.
The drop above $m$ exceeds the drop below $m$.

*Straddle case.* Let $\ell<r<m<h$ with $m=(\ell+h)/2$, and take the pair $\delta_m$ and $\{\ell,h\}$ with equal weights.
Use the uniform forms after Claim 1: $g(\ell)=(\ell^2-p^2)/(2r)$, $g(h)=h-r/2-p^2/(2r)$, $g(m)=m-r/2-p^2/(2r)$.
Then

$$
\frac{g(\ell)+g(h)}2-g(m)=\frac{(r-\ell)^2}{4r}=\frac{\Delta_T(r)}2,
$$

where $\Delta_T(r)=(r-\ell)^2/(2r)$ is the spread in equation (4) of the paper.
The premium rises in $r$ on this range, since $\Delta_T'(r)=\tfrac12-\ell^2/(2r^2)>0$ for $r>\ell$.
In drop terms, $F_r(u)=1$ for $u\ge r$.
A rise in $r$ creates no drop far above the support.
The drop below $m$ then dominates the drop above $m$.
Both cases use the same first-order strengthening, a rise in $r$. $\square$

Three corollaries follow **(analytical)**.

- *No flip without a trade-off.* If $\Gamma_r$ is a mean-preserving spread of $\Gamma_s$, then $\bar g(\Gamma_r)\ge\bar g(\Gamma_s)$ at every $F$, by Claims 3 and 4.
- Incumbent strength changes the size of the premium, not its sign.
- So strength alone never flips the choice between two convex-ordered plans.
- *Flips need non-comparable plans.* Let a risky plan carry a mean penalty.
- The choice flips when $\Pi_g(F)$ crosses the gross value of that penalty.
- Section 5, item 6, gives a uniform case with a flip toward risk as $r$ rises.
- The interior case gives the opposite force, since $\Pi_g$ falls in $r$ there.
- *Entry selection is distinct from preference.* Claim 8 lowers $\bar g$ at each fixed plan.
- A safe plan can fall below $c_H$ while a risky plan stays above $c_H$.
- Observed entrants then hold riskier plans after a rise in strength.
- This pattern can hold even while $\Pi_g$ falls.
- It is a selection effect at the cost threshold, not a rise in the value of risk.

The small-spread form of the premium helps intuition **(analytical, under smoothness)**.
Let $F$ have a continuous density $f$ near an interior point $m>p$.
Taylor expansion of the second difference gives $\Pi_g=\tfrac12 f(m)d^2+o(d^2)$ as $d\to0$.
Local risk has value where incumbent density is high.
The reason is that $g''=f$ where the density exists.
A stronger incumbent raises local risk value at $m$ iff it raises density near $m$, to this order.
First-order dominance does not order densities pointwise.
Hence local analysis gives the same ambiguity as Claim 9.

What happens to the spread that an informed investor trades on depends on the state definition **(analytical at fixed objects; open in equilibrium)**.

- If the state is a pair of realized values, the spread rises with strength, by Claim 8.
- If the state is a pair of dominant laws, the spread also rises, by Claim 8.
- If the state is plan identity at a fixed mean, the spread is $\bar t(\Gamma_s)-\bar t(\Gamma_r)$.
- By Claim 3 this spread equals $\Pi_g$.
- By Claim 9 its response to strength has no general sign.
- If the challenger switches plans as strength rises, observed $\bar t$ jumps at the switch point.
- A switch to a riskier plan jumps $\bar t$ down, by Claim 3.
- That jump can offset the rise in Claim 8 at a fixed plan.

The residual advantage in equation (11) of the paper has the form $e\,\Delta_T$ times a posterior term.
At a fixed plan, strength raises $\Delta_T$ and lowers entry pressure through $\bar g$.
With an endogenous plan, strength also moves $\Pi_g$ and can move $e$ by a plan switch.
No version of the bound $\rho m\Delta_T$ survives without a new definition of $\Delta_T$ for the chosen state.
Part D makes the state definition explicit for each timing.

### Part D. Information and timing

One fact holds in all variants **(analytical)**.
Knowledge of $\Gamma$ does not change bids in the cash second-price auction.
Truthful bids are weakly dominant for each bidder at each realized value.
So private knowledge of the plan creates no bid-shading problem.
The supervisor remark on the second-price auction is exact at the bid stage.
All hard effects sit in entry, in trading, and in price inversion.
They do not sit in bid functions.

**Claim 10 (choice before trading breaks the price-to-entry channel; analytical).**
In variant V1, let the challenger choose $\Gamma$ before trading and know its choice.
Let the investor observe $\Gamma$ and no further fact about $\theta$.
Let market makers observe flow only.
Then the entry rule does not depend on the price.
Price informativeness has no effect on entry in this variant.

*Derivation.*
At the entry decision the challenger knows $\Gamma$ and $C$.
Its payoff from entry is $\bar g(\Gamma)-C$.
The price is a function of flow.
Flow depends on orders that depend on $\Gamma$ and on noise.
Conditional on $(\Gamma,C)$, the price adds no fact about $\theta$, about $R$, or about $C$.
The challenger already knows the only payoff state in the investor signal.
Hence entry is $\mathbf 1\{\bar g(\Gamma)\ge C\}$, with no price argument.
A change in price informativeness at a fixed choice rule leaves this rule unchanged. $\square$

Three consequences follow.

- *A public pure choice gives the investor no private fact* **(analytical)**.
- If the optimal $\Gamma$ is a pure function of public primitives, market makers can compute it.
- The investor signal then has no residual content.
- With $k>0$, the zero order is strictly optimal.
- Trade needs a hidden driver of choice, such as a private cost or a private signal.
- The investor must observe that driver, or the realized mixed choice, while the market does not.
- The true latent state is then that driver, not a free choice.
- *Correlation is not feedback* **(analytical)**.
- If a hidden driver moves both $\Gamma$ and the price, entry and price correlate across states.
- Entry still does not respond to the price within a state, by Claim 10.
- A test in the style of Section 7 of the paper must separate the two patterns.
- *Sign reversal at a fixed mean* **(analytical)**.
- If the state is safe versus risky at one mean, the safe plan has the higher $\bar t$, by Claim 3.
- Good news for target shareholders is then a safe plan.
- The challenger prefers the risky plan, by the same claim.
- In the paper, good news is a high value, and both $\bar t$ and entry pressure rise with that news.
- Under V1 at a fixed mean, target news and challenger rent move in opposite ways.

A stronger incumbent can still raise entry in V1, but through choice, not through price learning **(conjecture as an equilibrium statement; analytical as a threshold statement)**.
Suppose a rise in strength flips the choice from a safe plan to a risky plan with $\bar g$ above $c_H$.
Entry then jumps from $\rho$ to $1$ at the flip point, under the cost floor of Claim 7.
Claim 9 shows that such a flip needs a mean trade-off and a premium that rises in strength.
The mechanism is "competition creates gambles, and gambles create entry."
It is not the mechanism of the paper.
No result in this memo signs the flip in general.

Variant V1 changes if the investor also observes the realized $\theta$.
Call this case V1b.
The price can then teach the challenger about $\theta$ given $\Gamma$.
Entry takes the form $\mathbf 1\{\mathbb E[g(\theta)\mid P,\Gamma]\ge C\}$.
The feedback channel returns.
But price sufficiency in the sense of Proposition A.2 fails in general with a continuous $\theta$ **(analytical)**.
The price is one number.
Market makers price a posterior mean of $t(\theta)$ plus an entry term.
Entry needs a posterior mean of $g(\theta)$.
On $[p,\infty)$, $g(\theta)=\theta-t(\theta)$ pointwise.
So $\mathbb E[g(\theta)\mid P]=\mathbb E[\theta\mid P]-\mathbb E[t(\theta)\mid P]$.
One price cannot in general pin down both posterior means.
A three-point case shows the gap.
Take $\theta_1<\theta_2<\theta_3$ in a range where $t$ is strictly concave.
A law on $\{\theta_1,\theta_3\}$ and a sure law at $\theta_2$ can share one value of $\mathbb E[t(\theta)]$ and still differ in $\mathbb E[\theta]$.
To see this point, vary the weight on $\theta_3$ until the law gives $t(\theta_2)$ in expectation.
Strict concavity puts the mean of that law above $\theta_2$.
They then differ in $\mathbb E[g(\theta)]$ at one price and one entry value.
Binary $\theta$ is the special case where one posterior pins down all means.
That special case is the model of the paper with a plan-dependent pair $(g_j,t_j)$.
The general continuous case needs a restriction that makes the two means one object.
No such restriction is in Reading C as stated.
The value of a dispersed $\Gamma$ under price learning is plausibly higher than $\bar g$ alone suggests **(conjecture)**.
The challenger holds an entry option on the posterior mean of $g(\theta)$.
More dispersion of that posterior mean raises an option value.
A proof needs an order on experiments and a monotone order rule.
This memo does not supply that proof. The claim stays open.

**Claim 11 (choice after the price, with a base value state; analytical in a stated subcase, conjecture beyond it).**
In variant V2, let the investor observe a base value $\theta\in\{\ell,h\}$ as in the paper.
After the price, the challenger chooses a spread $\varepsilon\in\{-d,+d\}$ with equal weights, or no spread.
Diligence then reveals $\theta+\varepsilon$ in the spread case.
Let $\Pi(\theta)=\tfrac12[g(\theta-d)+g(\theta+d)]-g(\theta)$ be the spread premium at base $\theta$.
At posterior $\mu=\Pr(h\mid P)$, the expected premium is $(1-\mu)\Pi(\ell)+\mu\Pi(h)$.
With no cost for the spread, the challenger weakly chooses the spread at each $\mu$.
The choice margin is then inoperative.
With a fixed cost for the spread, in profit units, the challenger chooses the spread on one side of a threshold $\mu^*$.
For small $d$ and a smooth density, $\Pi(\theta)=\tfrac12 f(\theta)d^2+o(d^2)$.
In the uniform benchmark with $h-d\ge r>\ell+d$ and $\ell-d>p$, $\Pi(h)=0$ and $\Pi(\ell)=d^2/(2r)>0$.
The challenger then gambles after low beliefs and not after high beliefs.

*Derivation.*
Conditional on base $\theta$, the spread changes gross profit by $\Pi(\theta)$.
The challenger does not know $\theta$ when it chooses.
It knows only $\mu$ from the price, if the price reveals $\mu$.
Linearity in $\mu$ gives the expected premium formula.
Claim 1 gives $\Pi(\theta)\ge0$ because $g$ is convex.
With no cost the spread weakly dominates at each $\mu$.
With a fixed gross cost $K>0$ for the spread, in profit units, the rule is to spread iff $(1-\mu)\Pi(\ell)+\mu\Pi(h)\ge K$.
A mean penalty for the spread gives a state-dependent cost in place of $K$.
The threshold form then needs that cost written out. This memo keeps $K$ fixed for exactness.
The left side is affine in $\mu$, so the rule is a threshold rule unless $\Pi(\ell)=\Pi(h)$.
The small-$d$ form is the Taylor step at the end of Claim 9.
In the uniform case, $g$ is affine with slope $1$ on $[r,\infty)$ by Claim 1.
A spread with both points in that region has premium $0$.
A spread with both points in $(p,r)$ has premium $d^2/(2r)$. Claim 9 proves that value.
If $\Pi(\ell)>\Pi(h)$, the expected premium falls in $\mu$.
The spread region is then $\mu\le\mu^*$ for an interior threshold. $\square$

The effect on the traded spread is exact in one subcase **(analytical)**.
Suppose the price perfectly reveals the base state, so $\mu\in\{0,1\}$.
Suppose the uniform conditions of Claim 11 hold, with a fixed cost $K$ between $0$ and $\Pi(\ell)$.
The challenger spreads in state $L$ and does not spread in state $H$.
Expected proceeds in state $H$ stay at $t(h)$.
In state $L$ they fall from $t(\ell)$ to $t(\ell)-\Pi(\ell)$, by the zero-sum part of Claim 3.
Hence the state spread rises from $t(h)-t(\ell)$ to $t(h)-t(\ell)+\Pi(\ell)$.
Endogenous gambling widens the claim that the investor trades on.
Intuition is "gambling for resurrection" by a low-value challenger.
The gamble has value inside the incumbent support and no value above it.

With Laplace noise the price does not perfectly reveal the state.
The spread choice then depends on the price, not on the state.
Under full orders, low prices are more likely in state $L$ than in state $H$.
Expected proceeds in state $L$ should then fall by more than in state $H$.
The state spread should still widen **(conjecture)**.
A proof must integrate the choice rule over the two flow laws.
It must also solve the price fixed point with the choice rule inside $P$.
Neither step is in this memo.
Existence and uniqueness of that fixed point are **open**.
One hazard is already visible.
At $\mu^*$ the target bracket in the price jumps down as the spread switches on when $\mu$ falls.
Equivalently, the bracket jumps up as $\mu$ rises through $\mu^*$ and the spread switches off.
That jump helps price monotonicity in this direction of switch.
Claim 12 treats the general jump condition, where the sign can go the other way.

**Claim 12 (nature draws the type, the challenger chooses risk; analytical jump condition, open equilibrium analog).**
In variant V3, nature draws type $j\in\{L,H\}$.
The investor observes $j$. The challenger observes neither $j$ nor $\theta$ before the price.
After the price the challenger picks an action $a\in\{s,r\}$, safe or risky.
Action $a$ gives type laws $\Gamma_L^a,\Gamma_H^a$ on $[p,\infty)$.
Assume $\Gamma_H^a$ first-order dominates $\Gamma_L^a$ for each action $a$.
Claim 2 then gives $\bar g_H^a\ge\bar g_L^a$ and $\bar t_H^a\ge\bar t_L^a$ for each $a$.
Write $\bar g_j^a$ and $\bar t_j^a$ for the four means.
Let $B_a(\mu)=(1-\mu)\bar g_L^a+\mu\bar g_H^a$ and $T_a(\mu)=(1-\mu)\bar t_L^a+\mu\bar t_H^a$.
Let $B^*(\mu)=\max\{B_s(\mu),B_r(\mu)\}$ and let $a^*(\mu)$ attain the maximum.
Assume the cost floor $c_L<B^*(m)$ with $m$ from the paper, so $e(\mu)=\rho+(1-\rho)\mathbf 1\{B^*(\mu)\ge c_H\}$.
A candidate price is $P(\mu)=t_0+e(\mu)[T_{a^*(\mu)}(\mu)-t_0]$.
Within one action regime, $P$ is strictly increasing in $\mu$ if $\bar t_H^a>\bar t_L^a$ and $T_a(\mu)>t_0$.
At an action switch $\mu^*$, price sufficiency holds only if the jump condition below holds.

*Derivation.*
The function $B^*$ is the maximum of two affine functions.
It is convex and piecewise affine, with at most one switch point $\mu^*$.
Each $B_a$ is nondecreasing by the dominance assumption in the claim statement.
So $B^*$ is nondecreasing, and the floor at $m$ covers all feasible posteriors in $[m,M]$.
Entry follows from $B^*$ as in equation (9) of the paper, under the stated floor.
Within a regime, $a^*(\mu)$ is constant.
The proof of statement (A.3) in the paper then applies word for word with $t_L,t_H$ replaced by $\bar t_L^a,\bar t_H^a$.
The price gap across $\mu_2>\mu_1$ in one regime is at least $\rho(\bar t_H^a-\bar t_L^a)(\mu_2-\mu_1)>0$.

At $\mu^*$, write $e_-,e_+$ for entry just below and just above the switch.
Write $a_-,a_+$ for the two actions.
The price jump as $\mu$ rises through $\mu^*$ is

$$
\Delta P=e_+[T_{a_+}(\mu^*)-t_0]-e_-[T_{a_-}(\mu^*)-t_0].
$$

If entry does not change at the switch, $e_+=e_-=e$.
If the switch is safe below to risky above, Claim 3 gives $T_r(\mu^*)<T_s(\mu^*)$ when the risky laws are spreads of the safe laws.
Then $\Delta P=-e[T_s(\mu^*)-T_r(\mu^*)]<0$.
A higher posterior then has a lower price near $\mu^*$.
The price is not strictly increasing in $\mu$ across the switch.
When the two regime price ranges overlap near $\mu^*$, one price fits two posteriors with distinct $B^*$ values in general.
Proposition A.2 inversion fails at such prices.
The challenger must then use a pooled belief at those prices.
Entry and the action choice must be solved at that pooled belief.
This memo does not solve that fixed point.

If the switch has the V2 direction, risky below to safe above, then $\Delta P>0$ at fixed entry.
The jump then helps monotonicity, as at the end of Claim 11.
If entry also jumps at $\mu^*$, sufficiency needs $\Delta P\ge0$ in the formula above.
For a safe-to-risky switch with $e_-=\rho$ and $e_+=1$, the condition is

$$
T_r(\mu^*)-t_0\ge\rho\,[T_s(\mu^*)-T_r(\mu^*)].
$$

The left side is the entry gain at full entry.
The right side is the floor share of the concave loss from risk.
Under $\Delta P\ge0$ plus within-regime monotonicity, $P$ is strictly increasing across regimes.
The price then reveals $\mu$ almost surely, by the inversion step of Proposition A.2.
A price in a jump gap is generated by no flow, as in the paper. $\square$

Under the jump condition, the architecture of Proposition 2 can be rebuilt in form **(open as a theorem)**.
Condition (A1) becomes $c_L<B^*(m)$.
Condition (A2) must use $B^*$ at the two incumbent laws.
Condition (A3) must use a regime-dependent spread.
Residual advantages take the form $e(\mu)\Delta_{a^*(\mu)}$ times a posterior term, with $\Delta_a=\bar t_H^a-\bar t_L^a$.
The global order bound needs an infimum of that product over flows.
A switch inside the flow range changes the infimum.
No claim in this memo proves existence, uniqueness, or the three-part comparison for V3.
The direction of the risk effect on $\Delta_a$ is also not general **(analytical)**.
A common spread of both type laws changes $S_H-S_L$ without a fixed sign.
In the uniform case with the $H$ law above $\bar r$ and the $L$ law inside support, the spread lowers $\bar t_L$ and leaves $\bar t_H$ fixed.
Then $\Delta_r>\Delta_s$, and risk choice strengthens the trading motive.
Claim 11 is that case with degenerate base laws.

The table sums up Part D. "Survives" means the price-to-entry channel of the paper stays intact in form.

| Variant | Investor knows | Price reveals | Entry responds to price | Channel status |
|---|---|---|---|---|
| V1a: choice first | Plan $\Gamma$ only | Posterior over $\Gamma$ | No (Claim 10) | Fails |
| V1b: choice first | Plan and $\theta$ | Posterior over $\theta$ given $\Gamma$ | Yes | Survives only in binary case |
| V2: risk after price | Base value $\theta$ | Posterior $\mu$ if inversion holds | Yes, plus risk choice | Can strengthen (Claim 11) |
| V3: type, then risk | Type $j$ | Posterior $\mu$ iff jump condition holds | Yes, plus risk choice | Fragile (Claim 12) |

### Part E. Verdict

**Claim 13 (comparison of the two readings; conjecture as interpretation, analytical in its cited parts).**
Reading C yields one clear and neat result at the auction stage.
It does not yield a clear and neat result for the full model in its pure V1 form.
Reading N fits the paper story and the second clause of the supervisor remark better than pure Reading C.

The neat auction result is Claims 1 to 3 as one sentence.
*In a cash second-price auction, challenger rent is convex in challenger value. Target proceeds are concave above the reserve. So at a fixed mean and a fixed entry event, the challenger loves value risk and the target hates it, in equal amounts.*
Claim 4 adds the reserve qualification.
Claim 8 adds that a stronger incumbent still lowers rent at a fixed plan and raises the fixed-pair spread.
That block is complete and needs no trading model.

The full-model result fails in pure form for three proved reasons.
First, a chooser knows its choice, so the price teaches it nothing in V1a (Claim 10).
Second, an unrestricted menu gives a corner gamble (Claim 6).
Third, incumbent strength has no signed effect on the value of risk (Claim 9).
A neat "stronger incumbent, riskier plan, more entry" claim is false at this level of generality.
Both premium signs occur in the uniform model of the paper itself.

On fit with the supervisor words, the evidence splits.
The word "choosing" points to Reading C in a literal sense.
The clause "only when they receive information can they actually know what distributions they end up at" points away from a deliberate and known choice.
A deliberate chooser knows the chosen distribution at the choice date.
Under Reading N, the challenger learns its distribution class only through information.
That clause then reads in a direct way.
Under Reading C as set for this memo, "know" must mean "learn the realized value."
That reading is coherent, but it uses "distributions" to mean "draws."
On fit with the paper story, the split is sharper.
The paper needs an uninformed challenger and an informed investor.
The price then moves a real decision.
Reading N keeps that structure, and Section 6.3 value classes already have that shape.
Pure Reading C reverses it: the challenger holds the private fact and the market learns it.
The hybrid V3 keeps the paper structure and adds a choice margin.
V3 is the only form of Reading C that preserves the title mechanism in form.
Its Proposition 2 analog is open, and its price inversion holds only under the jump condition of Claim 12.

## 4. What changes relative to the current paper

This section goes object by object.
"Survives" means the statement and proof step hold with the new definition in place.

- **Support restriction (1), $0<p<\ell<r<h$: fails as a general assumption.**
- Plans can put mass below $p$ and above $\bar r$ at the same time.
- Preparation, admissibility, and sale then differ.
- Section 6.3 of the paper already separates the three events.
- Claim 1 adds the exact jump size $pF(p)$ at the reserve.
- Any draft with plans must report preparation and admissibility apart.
- **Auction formulas (4): survive as special values.**
- The numbers $t_0,t_H,t_L,g_H,g_L$ become values of functions $t(\theta),g(\theta)$ at $\ell,h$.
- Claim 1 gives the functions for a general continuous $F$.
- The uniform closed forms after Claim 1 match equation (4) exactly.
- **Proposition 1: survives and extends at a fixed plan.**
- Claim 8 is the same opposition with $\bar g(\Gamma)$ and fixed-law spreads.
- The proof step is the same pointwise payment logic plus Claim 2 weights.
- The extension fails for observed proceeds once the plan switches with $F$.
- The switch jump of Claim 3 can reverse the observed direction at one strength.
- **Gross profit at a belief, $B_r(\mu)$: changes by variant.**
- In V1 the object is $\bar g(\Gamma)$ with no belief argument.
- In V1b the object is $\mathbb E[g(\theta)\mid P,\Gamma]$.
- In V3 the object is the envelope $B^*(\mu)$ of Claim 12.
- Linearity in $\mu$ survives only within one action regime in V3.
- **Posterior bounds (7)–(8) and Proposition A.1: survive only with a binary exogenous state.**
- V2 and V3 keep a binary state, so the Laplace bound step is unchanged.
- V1a has an endogenous prior over plans.
- The bounds $m,M$ then describe a posterior over a choice, not over a payoff type.
- With a pure public choice the posterior is degenerate and trade has no basis.
- **Entry and price forms (9)–(10) and Proposition A.2: fragile.**
- In V1a entry has no price argument, by Claim 10.
- In V1b with continuous $\theta$, one price cannot recover the entry statistic.
- In V3 inversion holds within regimes and across a switch only under Claim 12.
- A safe-to-risky switch at fixed entry gives a downward price jump.
- That jump has no analog in the paper, where the entry jump is upward.
- **Residual advantages (11): survive in form for binary states, with a new spread.**
- Replace $\Delta_T$ by the state spread of the variant.
- In V3 the spread is regime-dependent, $\Delta_{a^*(\mu)}$.
- The lower bound $\rho m\Delta_T$ needs an infimum over regimes.
- **Global order bound (A.6): proof step survives, bound value changes.**
- The step $|f'|\le f/b$ does not use the auction.
- The residual infimum that enters the bound does use the auction and the choice rule.
- A switch inside the flow range can lower the infimum and break condition (A3) as written.
- **Proposition 2: fails in V1a; open in V2 and V3.**
- Part (ii) needs entry above $\rho$ from an informative price.
- Claim 10 removes that channel in V1a.
- Claims 11 and 12 keep the channel in form for V2 and V3.
- No three-part analog is proved in this memo.
- **Closed forms (12): survive only in a binary, one-regime range.**
- The threshold $\tau$ must solve $B^*(\tau)=c_H$ in V3.
- With a switch below $\tau$, $\tau$ is piecewise in form.
- The flow $x^*$ and the terms $\alpha_H,\alpha_L$ keep their Laplace forms given $\tau$.
- **Proposition A.3, deterrence at a fixed experiment: survives at a fixed plan.**
- Claim 8 lowers $\bar g$ at each fixed $\Gamma$ as $F$ strengthens.
- With an endogenous plan, the control must also fix the plan.
- A plan switch is a new channel that can offset deterrence in observed entry.
- It is a choice effect, not an information effect.
- **Proposition A.4, no-trade condition: changes with the spread definition.**
- The condition $\rho\Delta_T/2\le k$ needs the variant spread in place of $\Delta_T$.
- In V1a with a public pure choice, the spread is zero and no trade is the unique outcome.
- **Payment rule, Section 6.2: the target side of Claim 3 flips at $\eta=1/2$.**
- The derivation after Claim 3 shows $t_\eta$ convex iff $\eta>1/2$.
- Challenger risk love holds for all $\eta<1$ in that institution.
- So the neat opposition needs the second-price side of that section.
- **Value classes, Section 6.3: closest current text to this memo, with Reading N shape.**
- Classes there are drawn, not chosen.
- The investor observes the class. Preparation reveals the exact value.
- Reading C would need a new paragraph with a menu, a trade-off, and a timing rule.

## 5. Numerical example

The script is `audit/alex_meeting_2026_10_21/scripts/Q1_C_choice/Q1_C_choice_numbers.py`.
Run it with `.venv/bin/python` and the script path.
The script prints values only.
All numbers in this section are **numerical diagnostics** from that run.
Parameters are the benchmark vector of the brief.
That is $(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02)$.
Strengths are $(r_0,r_1,r_2)=(1.2,3,3.6)$ with $R\sim U[0,r]$.

Item 1 of the script prints $g$ and $t$ at $r=3$ in closed and integral forms.
The two forms agree to six decimals at each printed $\theta$.
The sum $g(\theta)+t(\theta)$ equals $\theta$ at each $\theta\ge p$.
At $\theta=0.4<p$, $t=0.416667=t_0$.
At $\theta=0.5=p$, $t=0.500000$.
The printed jump size is $pF(p)=0.083333$, as in Claim 1.
Item 2 prints second differences on a grid with step $0.5$ in $[0.5,3]$.
Each $g$ value is $+0.083333$. Each $t$ value is $-0.083333$.
Item 7 prints the paper values from equation (4).
At $r_0$, $\Delta_T=0.016667$ and $B(1/2)=4.804167$.
At $r_1$, $\Delta_T=0.666667$ and $B(1/2)=4.291667$.
These match Section 4.2 of the paper.

Item 3 is Menu A, the benchmark straddle menu.
The safe plan gives value $5.5$ for sure.
The risky plan gives values $1$ and $10$ with equal weights.
Both means are $5.5$.
The risky plan is the binary law of the paper.

| $r$ | $\bar g$ safe | $\bar g$ risky | Premium | $\bar t$ safe | $\bar t$ risky |
|---:|---:|---:|---:|---:|---:|
| 1.2 | 4.795833 | 4.804167 | 0.008333 | 0.704167 | 0.695833 |
| 3.0 | 3.958333 | 4.291667 | 0.333333 | 1.541667 | 1.208333 |
| 3.6 | 3.665278 | 4.134722 | 0.469444 | 1.834722 | 1.365278 |

The premium equals $\Delta_T(r)/2$ at each row, as Claim 9 proves for this menu.
The target loss equals the premium at each row, as Claim 3 requires.
The challenger chooses the risky plan at each strength.
Target shareholders prefer the safe plan conditional on entry.
Both $\bar g$ values lie between $c_L=1$ and $c_H=6$ at each strength.
So choice alone recruits no high-cost entry in Menu A without price information.
The risky plan sits closer to $c_H$ than the safe plan at each strength.
The gap to $c_H$ at $r_1$ is $1.708333$ for the risky plan.

Item 4 is Menu B, an interior menu.
The safe plan gives $0.9$ for sure.
The risky plan gives $0.6$ and $1.2$ with equal weights.
Both means are $0.9$. The half-spread is $d=0.3$.

| $r$ | $\bar g$ safe | $\bar g$ risky | Premium | $d^2/(2r)$ | $\bar t$ safe | $\bar t$ risky |
|---:|---:|---:|---:|---:|---:|---:|
| 1.2 | 0.233333 | 0.270833 | 0.037500 | 0.037500 | 0.666667 | 0.629167 |
| 3.0 | 0.093333 | 0.108333 | 0.015000 | 0.015000 | 0.806667 | 0.791667 |
| 3.6 | 0.077778 | 0.090278 | 0.012500 | 0.012500 | 0.822222 | 0.809722 |

The premium falls as $r$ rises.
Menu A and Menu B give opposite premium responses to the same rise in $r$.
That pair is the numerical content of Claim 9.
Both $\bar g$ values in Menu B lie below $c_L=1$.
So Menu B gives no entry at the benchmark costs.
Menu B serves as a curvature check only. Its scale is too small for the entry stage.

Item 5 is the reserve straddle at $r=3$ from Claim 4.
The safe plan gives $0.4$ for sure, below $p=0.5$.
The risky plan gives $0$ and $0.8$ with equal weights.
Both means are $0.4$.
The safe plan gives $\bar g=0$ and $\bar t=0.416667$.
The risky plan gives $\bar g=0.032500$ and $\bar t=0.575833$.
Both sides prefer the risky plan here.

Item 6 adds a mean trade-off.
The safe plan gives $5.5$ for sure, with mean $5.5$.
The risky plan gives $1$ and $9$ with equal weights, with mean $5.0$.
For $1<r<5.5$, algebra from Claim 1 gives $\bar g(\text{risky})-\bar g(\text{safe})=r/4-1+0.25/r$ **(analytical)**.
The zero solves $r^2-4r+1=0$, so $r=2+\sqrt3\approx3.732051$.
The script prints $-0.491667$ at $r=1.2$ and $-0.166667$ at $r=3$.
It prints $+0.180556$ at $r=4.5$ and $+0.300000$ at $r=5$.
The challenger flips from the safe plan to the lower-mean risky plan as $r$ rises through $3.732051$.
The flip point lies just above $r_2=3.6$ and below $h=10$.
This menu shows a choice-based rise in risk with strength.
Menu B shows the opposite premium force.
No single comparative static covers both menus.

## 6. Open issues and risks

- **Equilibrium in V2 and V3 is open.**
- Existence, uniqueness, and order optimality are not proved with a choice rule inside the price.
- The pooled-belief case after a downward price jump has no solution in this memo.
- Mixed choice at a switch point may be part of any solution.
- **The menu needs a foundation.**
- Claim 6 gives a corner gamble with no trade-off.
- A draft must state why a risky plan costs mean, money, or support.
- The source of that cost will drive each flip result.
- **Commitment to a plan is strong.**
- Diligence reveals $\theta$ in this memo.
- In a deal, a buyer can revise an integration plan after diligence facts arrive.
- Revision without commitment turns $\Gamma$ into a post-information choice.
- That game is V2 with full state knowledge at the choice date, a distinct case.
- **Observability of the plan is unsettled.**
- Rivals, the target board, and investors may see parts of an integration plan.
- Bids do not change with that knowledge, by dominance.
- Reserve choice and outreach choice by the seller can change.
- Seller design with a known plan menu is outside this memo.
- **Risk neutrality drives risk love in part.**
- Claim 3 uses risk neutrality plus convex rent.
- Risk aversion, financing limits, or loss limits can offset the premium.
- The paper assumes risk neutrality, so Claim 3 is the right internal check.
- An external reading should not export risk love without that caveat.
- **One challenger is a restriction.**
- With two challengers, rent depends on the maximum rival value.
- Convexity in own value survives that change in form, since the strike stays exogenous to own $\theta$.
- Plan choice then has a strategic part through rival entry thresholds.
- No claim here covers that part.
- **Welfare language needs care.**
- Claim 3 raises total surplus and incumbent rent under a spread.
- Target proceeds fall at a fixed entry event.
- A seller who can set $p$ or restrict plans faces a transfer problem, not only a surplus problem.
- **Empirical content is thin in pure Reading C.**
- Plan risk is hard to measure from disclosure records.
- The selection pattern after Claim 9 can look like a preference pattern.
- A test must measure the menu or the cost threshold to split the two.

## 7. Recommendation

In priority order:

1. **Keep the binary benchmark as the main model.**
   Do not replace it with a pure pre-trading plan choice.
   Claim 10 removes the title mechanism in that form.
   Reading N is the safer main line for supervisor point 1.
2. **Add Claims 1 to 3 as a short auction lemma or remark.**
   State convex rent, concave proceeds, and the zero-sum split at a fixed mean.
   Add the reserve jump of Claim 1 and the qualification of Claim 4.
   This block answers the "second-price auction" part of the remark at low cost.
   It also gives a clean reason why value classes in Section 6.3 behave as they do.
3. **If Reading C enters the draft, use the V3 hybrid form only.**
   Nature draws the type. The price informs the challenger.
   The challenger then picks safe or risky laws by type.
   Give the risky action an explicit mean cost.
   Restrict parameters to the jump condition of Claim 12.
   State the Proposition 2 analog as a target result, not as a proved result, until the fixed point is solved.
4. **Use the uniform gamble result as a remark, with its limits.**
   In the benchmark support pattern, a low-value challenger gains from a spread and a high-value challenger does not.
   That pattern can widen the traded spread, by Claim 11.
   Pair the remark with Menu B or the interior case of Claim 9.
   The pair stops a reader from taking one sign as general.
5. **Ask the supervisor one timing question at the next meeting.**
   Does "choosing" mean a known choice by the challenger, or a draw that information later reveals?
   The answer selects between V1 and Reading N.
   No technical work can settle that word choice from inside the model.

## 8. Plain summary

A challenger in a second-price sale keeps the gap between its value and the price it must beat. That gap is like an option. It pays in good draws and pays zero in bad draws. So a riskier plan with the same average value raises the challenger profit from entry. The target sits on the other side of the same split. At a fixed average value, each extra unit of challenger profit is one less unit of target proceeds, once the challenger can bid at all. Below the reserve price the story flips. A risky plan can create a valid bid where a safe plan creates none, and then both sides gain. A stronger rival still cuts challenger profit for any fixed plan. But it can raise or cut the extra value of risk. The benchmark numbers show both cases. So strength alone does not push the challenger to riskier plans in general. Timing matters most. If the challenger picks its plan first and knows the pick, the stock price teaches it nothing new. Entry then stops responding to the price, and the main result of the paper fails. The idea works best as a hybrid. Nature sets the type, the price informs the challenger, and the challenger then picks how much risk to take.




