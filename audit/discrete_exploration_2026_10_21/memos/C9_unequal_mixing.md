# C9. Unequal noise and preparation at indifference

## 1. Question

Can preparation at indifference restore existence in the three-point model with unequal noise?
Can informative equilibria coexist with no trade and show higher entry at greater incumbent strengths?
Does an interior purchase probability replace the paper's endogenous order asymmetry?

The answers are yes, yes, and partly.
Existence holds throughout the admissible parameter domain under the belief rule below.
One explicit interval has exactly three equilibrium outcomes: no trade and two informative outcomes.
Entry rises on one informative branch and falls across the reported points on the other branch.

## 2. Setup

### Base model and sources

The base model has buy-only orders and three-point noise.
This memo changes the noise probabilities and both indifference rules.
The investor starts with no shares.
The low preparation cost is $c_L=0$.
The benchmark prior is $\Pr(H)=\Pr(L)=1/2$.

Write $(u,v,w)=(z_-,z_0,z_+)$, with $u+v+w=1$.
Initially, all three probabilities are positive.
Proposition C9.1 also covers zero probabilities and any interior prior.
The presence probability is $\lambda\in(0,1]$.
Presence, noise, preparation cost, incumbent value, and quality are independent.

The paper source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
The source commands are:

```text
git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:main.tex
git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:online_appendix.tex
```

The relevant passages are main Sections 2–4.3, Appendix A.2–A.4, and online Appendix A.3 and B.
Proposition 3 certifies three strengths, ordered entry, and separate no-trade equilibria.
It does not establish an entire continuous branch.
The present result establishes such a branch for a different, finite order menu.

The prior references are [the buy-only derivation](../../alex_meeting_2026_10_21/memos/Q2_discrete_buy_only.md), Claim 10, and [the independent check](../../alex_meeting_2026_10_21/memos/V_discrete_check.md), Sections 3.6–3.7.
Their equilibrium calculations are distinct from the exact schedules below.
No external literature result enters the proof.

### Auction values

Maintain $0<p<\ell<r<h$, $0<\rho<1$, $c_H>0$, and $k>0$.
The incumbent value is uniform on $[0,r]$.
The pinned paper gives

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&g_H&=h-r/2-p^2/(2r),\\
g_L&=(\ell^2-p^2)/(2r),&\Delta&=\Delta_T=(r-\ell)^2/(2r).
\end{aligned}
$$

These formulas agree with the shared objects.
In particular, $g_L>0$, $g_H-g_L>0$, and $\Delta>0$.
Put $a_L=t_L-t_0>0$.
The profit difference satisfies $g_H-g_L=h-r/2-\ell^2/(2r)>h-r>0$.
Entry also raises target receipts when $R<p$: it creates a sale at the reserve.
At every other incumbent value, entry weakly raises receipts.
Thus $a_L>0$.
The expected preparation gain at posterior $\mu$ is

$$
B_r(\mu)=g_L+\mu(g_H-g_L),
\qquad
\tau(r)=\frac{c_H-g_L}{g_H-g_L}.
$$

### Equilibrium, beliefs, and indifference

The investor observes quality and chooses $q\in\{0,1\}$ when present.
Market makers observe $X=q+Z$ and set a competitive price.
The challenger observes only this price and its cost.
Preparation reveals quality and permits a truthful auction bid.

The high-cost challenger uses the correspondence

$$
S_r(\mu)=
\begin{cases}
\{0\},&B_r(\mu)<c_H,\\
[0,1],&B_r(\mu)=c_H,\\
\{1\},&B_r(\mu)>c_H.
\end{cases}
$$

At a realized price, $\sigma\in S_r(\mu)$ is its preparation probability conditional on high cost.
Total entry is $e=\rho+(1-\rho)\sigma$.
The low-cost challenger always prepares because $g_L>0=c_L$.
The investor may mix between zero and one exactly when both actions give zero net profit.
Neither indifference selects a pure action by rule.

On-path beliefs follow Bayes' rule.
Under no trade, assign posterior one to the unused flow $X=2$.
This directional completion attributes a new purchase to the high-quality investor.
It remains the stated completion when a refinement imposes no restriction.
This memo does not claim that every arbitrary off-path belief supports the same outcomes.

A unilateral deviation holds the price and entry schedules fixed.
It changes only the flow distribution that the investor reaches.
All payoffs below use this deviation rule.

### Why price observation causes no extra restriction

At flow $x$, let $\mu_x$ be the market maker's posterior and $e_x$ the entry rate.
Competitive prices satisfy

$$
P_x=t_0+e_x(a_L+\Delta\mu_x),
\qquad e_x\ge\rho>0.
$$

At any common price, the challenger uses one preparation probability.
Therefore,

$$
\mu_x=\frac{P_x-t_0-e(P_x)a_L}{e(P_x)\Delta}.
$$

Thus the price reveals the flow posterior.
Conversely, every collection of optimal entry rates below yields consistent price beliefs.
If $\mu_y>\mu_x$, the preparation correspondence implies $e_y\ge e_x$.
Then

$$
P_y-P_x
=e_y\Delta(\mu_y-\mu_x)+(e_y-e_x)(a_L+\Delta\mu_x)>0.
$$

If two flows share a posterior at indifference, their entry rates may differ.
Their prices then differ by $(e_y-e_x)(a_L+\Delta\mu_x)$.
Equal prices still imply equal posteriors and equal entry rates.
The construction therefore respects price observation even at an indifference.

## 3. Results

### Proposition C9.1 — analytical: reduction and existence

An equilibrium exists for every admissible parameter vector under the stated completion.
This result allows both investor and challenger mixtures.

**Reduction.** Conditional expected terminal value is $t_0+e_x(t_j-t_0)$ in state $j$.
Subtract the competitive price:

$$
V_H(x)-P_x=e_x\Delta(1-\mu_x),
\qquad
V_L(x)-P_x=-e_x\Delta\mu_x.
$$

A low-quality purchase has net payoff at most $-k<0$.
Zero gives zero.
Thus the low-quality investor never buys.
Let $\beta$ be the high-quality investor's purchase probability when present.
Put $\alpha=\lambda\beta$.

The conditional flow laws and posteriors are

$$
\begin{array}{c|c|c|c}
x&f_H(x)&f_L(x)&\mu_x\\ \hline
-1&u(1-\alpha)&u&(1-\alpha)/(2-\alpha)\\
0&v+\alpha(u-v)&v&[v+\alpha(u-v)]/[2v+\alpha(u-v)]\\
1&w+\alpha(v-w)&w&[w+\alpha(v-w)]/[2w+\alpha(v-w)]\\
2&\alpha w&0&1
\end{array}
$$

The last posterior also specifies the completion at $\alpha=0$.
Define

$$
D_0=2v+\alpha(u-v),\qquad D_1=2w+\alpha(v-w),
\qquad A=\frac{uv}{D_0},\qquad C=\frac{vw}{D_1}.
$$

A purchase reaches flows $0,1,2$ with probabilities $u,v,w$.
At flow two its residual is zero.
The high-quality purchase payoff is therefore

$$
U_H(1)=K_r(\alpha;e_0,e_1)-k,
\qquad
K_r(\alpha;e_0,e_1)=\Delta(Ae_0+Ce_1).
\tag{1}
$$

This formula also holds at no trade under the stated completion.
It evaluates a purchase against the fixed candidate schedule.
For later outcome comparisons, put $W_x=[f_H(x)+f_L(x)]/2$.
Aggregate entry and high-quality ownership are

$$
\mathsf E=\sum_x W_xe_x,
\qquad
\mathsf O_H=\frac12\sum_x f_H(x)e_x.
$$

The ownership formula uses $h>r$, so a prepared high-quality challenger always wins.

**Existence proof.** Consider the compact convex set

$$
\mathcal X=[0,1]\times[\rho,1]^2.
$$

For each point $(\beta,e_0,e_1)$, let $R(\beta,e_0,e_1)$ be the high-quality investor's optimal purchase probabilities.
Equation (1) gives

$$
R=
\begin{cases}
\{0\},&K_r(\lambda\beta;e_0,e_1)<k,\\
[0,1],&K_r(\lambda\beta;e_0,e_1)=k,\\
\{1\},&K_r(\lambda\beta;e_0,e_1)>k.
\end{cases}
$$

For $i=0,1$, define $E_i(\beta)=\rho+(1-\rho)S_r(\mu_i(\lambda\beta))$.
Use the correspondence

$$
\Gamma(\beta,e_0,e_1)=R(\beta,e_0,e_1)\times E_0(\beta)\times E_1(\beta).
$$

Every value is nonempty, compact, and convex.
The functions $\mu_i$ and $K_r$ are continuous because $D_i>0$.
Indeed, $D_0=(2-\alpha)v+\alpha u>0$ and $D_1=(2-\alpha)w+\alpha v>0$.

Both optimal action correspondences have closed graphs.
A strict payoff sign persists under a sufficiently small parameter change.
At a zero payoff, the correspondence includes every limit choice.
These facts also show that $\Gamma$ has a closed graph.

A closed graph with compact domain and range gives upper hemicontinuity here.
Kakutani's fixed-point theorem gives a fixed point of $\Gamma$.
At this point, the investor and the two relevant entry rates are mutual best responses.
Choose optimal entry at flows $-1$ and $2$.
Construct prices by the displayed price formula.
The price argument above establishes Bayesian consistency for the challenger.

The low-quality investor strictly prefers zero.
Truthful auction bids remain optimal.
The fixed point therefore gives a complete equilibrium.

**Zero noise probabilities.** The result extends to the boundary of the noise simplex.
If $f_L(x)=0$, assign posterior one to a newly reachable purchase flow.
Its high-quality purchase residual is zero.
Omit this zero term from (1).
Every remaining term has a strictly positive denominator and a continuous posterior.
Flows unreachable under either action do not affect any payoff.

The same fixed-point proof then applies to the remaining terms.
For example, set $A=0$ when $v=0$, and set $C=0$ when $w=0$.
If both coefficients vanish, no trade is an equilibrium for every $k>0$.

**General prior.** The proof also covers $\pi\in(0,1)$.
The flow laws stay the same and Bayes' rule uses prior $\pi$.
Replace (1) by

$$
K_r=\Delta(1-\pi)\left[
\frac{uv e_0}{v+\pi\alpha(u-v)}
+\frac{vw e_1}{w+\pi\alpha(v-w)}\right].
$$

The same continuity, correspondence, and price arguments apply.
The remaining results use $\pi=1/2$. $\square$

### Proposition C9.2 — analytical: complete scalar characterization

Define the smallest and largest optimal entry rates:

$$
e^-(\mu)=\rho+(1-\rho)\mathbf1\{B_r(\mu)>c_H\},
\qquad
e^+(\mu)=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\}.
$$

Substitute them into (1) to obtain $K_r^-(\alpha)$ and $K_r^+(\alpha)$.
Every intermediate gross purchase payoff is feasible.
Indeed, a common convex combination of the extreme entry vectors produces that payoff.
Every component remains an optimal entry choice.
The price construction remains valid.

The complete set of high-quality purchase probabilities is

$$
\begin{aligned}
\beta=0&\quad\Longleftrightarrow\quad K_r^-(0)\le k,\\
0<\beta<1&\quad\Longleftrightarrow\quad
K_r^-(\lambda\beta)\le k\le K_r^+(\lambda\beta),\\
\beta=1&\quad\Longleftrightarrow\quad k\le K_r^+(\lambda).
\end{aligned}
\tag{2}
$$

Each equivalence means that some optimal preparation schedule supports the stated purchase probability.
Necessity follows from the two available investor actions.
Sufficiency follows from the feasible payoff interval and the price construction.

No trade requires

$$
k\ge\frac{\Delta}{2}(u+v)e^-(1/2).
\tag{3}
$$

In particular, if $B_r(1/2)<c_H$, its condition is $k\ge\rho\Delta(u+v)/2$.
If $B_r(1/2)=c_H$, choose no expensive preparation to obtain the same condition.
An alternative preparation choice at that prior can give a different no-trade entry rate.

Every $\beta>0$ gives an informative price experiment.
The conditional flow difference is $\alpha[n(x-1)-n(x)]$, where $n$ is the noise law.
A nonzero finite probability law cannot equal its unit shift.
Thus at least two on-path posteriors differ.
Price sufficiency preserves this difference.

Consequently, coexistence means that (3) and a positive-purchase row of (2) both hold.
This is a necessary and sufficient characterization, including every indifference.

There is also a finite construction.
Interior entry changes can occur only at

$$
\alpha_0=\frac{v(2\tau-1)}{(1-\tau)(u-v)},
\qquad
\alpha_1=\frac{w(2\tau-1)}{(1-\tau)(v-w)}.
$$

Retain only defined values inside $[0,\lambda]$.
On each intervening interval, the entry rates are constant.
An interior investor equilibrium solves

$$
\frac{k}{\Delta}D_0D_1=uv e_0D_1+vw e_1D_0.
\tag{4}
$$

This equation has degree at most two.
At an entry threshold, solve the linear indifference equation for the preparation probability.
Check the two endpoint rows of (2) separately.
Constant posteriors at a cost threshold retain their full entry interval.
An identity in (4) retains its whole feasible interval. $\square$

### Proposition C9.3 — analytical: an upward branch and exactly three outcomes

First consider noise $(u,v,w)=(s,s,w)$, with $w=1-2s$ and $s>w>0$.
Assume $B_r(1/2)<c_H<g_H$.
Suppose expensive preparation occurs at flow one and flow two only.
Then $e_{-1}=e_0=\rho$ and $e_1=e_2=1$.
Equation (1) becomes

$$
K_r(\alpha)=\Delta\left[\frac{\rho s}{2}
+\frac{sw}{2w+\alpha(s-w)}\right].
$$

Its interior zero-profit solution is

$$
\alpha_A(r)=\frac{sw/[k/\Delta-\rho s/2]-2w}{s-w},
\qquad \beta_A=\alpha_A/\lambda.
\tag{5}
$$

The solution is an equilibrium whenever

$$
0<\alpha_A<\lambda,\qquad
\mu_1(\alpha_A)>\tau,\qquad
k/\Delta>\rho s/2.
$$

For coexistence, also require $k\ge\rho s\Delta$.
Equation (3) then supports no trade independently.

On every open interval with these strict inequalities,

$$
\alpha_A'(r)=
\frac{swk\Delta'(r)}{(s-w)\Delta(r)^2[k/\Delta(r)-\rho s/2]^2}>0.
$$

The unconditional probabilities of flows one and two sum to $w+s\alpha_A/2$.
Hence

$$
\mathsf E_A(r)=\rho+(1-\rho)(w+s\alpha_A/2),
\qquad
\mathsf E_A'(r)=\frac{(1-\rho)s}{2}\alpha_A'(r)>0.
\tag{6}
$$

This proves an analytic upward entry comparison across strengths.

**Benchmark construction.** Set

$$
(h,\ell,p,\rho,c_H,k,\lambda)
=(10,1,1/2,1/4,6,1/50,1),
\qquad (u,v,w)=(2/5,2/5,1/5).
$$

For every

$$
r\in I=[63/40,317/200],
\tag{7}
$$

the model has exactly three equilibrium outcomes under the stated completion.
They are no trade, an informative outcome with both indifferences, and the informative outcome in (5).
Entry on the last branch rises strictly throughout $I$.

Here are explicit interval checks.
Formula (5) reduces to

$$
\alpha_A=\frac{10\Delta-40k}{20k-\Delta},
\qquad
K_A=\Delta\left[\frac1{20}+\frac{2}{5(2+\alpha)}\right],
\qquad
\mathsf E_A=\frac25+\frac{3\alpha_A}{20}.
\tag{8}
$$

The spread rises with $r$.
Its endpoint values are $529/5040$ and $13689/126800$.
Thus $20k-\Delta>0$, and $\alpha_A$ rises from $1258/1487$ to $35450/37031$.
Both values lie strictly between zero and one.
Also, $\Delta<1/5$, so $k-\rho s\Delta=1/50-\Delta/10>0$.

At every $r>1$, $B_r(1/2)<5<6$.
For $r\in I\subset[3/2,8/5]$, $g_H>10-4/5-1/12>6$.
Thus $1/2<\tau<1$.
The remaining entry condition reduces to one polynomial:

$$
B_r(\mu_1(\alpha_A))-6
=\frac{P(r)}{80r(r-1)^2},
\qquad
P(r)=-45r^4+514r^3-980r^2+454r-15.
$$

At the lower endpoint, $P(63/40)=32763/102400>0$.
For $r\in[3/2,8/5]$,

$$
\begin{aligned}
P'(r)&=-180r^3+1542r^2-1960r+454\\
&\ge-180(8/5)^3+1542(3/2)^2-1960(8/5)+454\\
&=2511/50>0.
\end{aligned}
$$

Therefore $P(r)>0$ throughout $I$.
This proves every inequality for the upward branch and no trade.

**The third outcome.** The posterior at flow zero is always $1/2$.
The posterior at flow one rises strictly with $\alpha$.
It crosses $\tau$ at

$$
\alpha_T(r)=\frac{2\tau-1}{1-\tau}.
\tag{9}
$$

Since $\mu_1(\alpha_A)>\tau$, we have $0<\alpha_T<\alpha_A<1$.
Before this crossing, both relevant entry rates equal $\rho$.
Gross purchase profit is then

$$
K_F(\alpha)=\Delta\left[\frac1{20}+\frac1{10(2+\alpha)}\right]
\le\Delta/10<k.
$$

At the crossing, the maximal gross profit is $K_A(\alpha_T)>K_A(\alpha_A)=k$.
The inequality follows because $K_A$ strictly decreases with $\alpha$.
Thus one interior preparation probability fills the gap.
Its total entry rate and conditional high-cost probability are

$$
e_{1,T}=\frac{k/\Delta-1/20}{(2/5)(1-\tau)},
\qquad
\sigma_T=\frac{e_{1,T}-1/4}{3/4}\in(0,1).
\tag{10}
$$

The investor uses $\beta_T=\alpha_T$.
It earns zero on a purchase.
The high-cost challenger earns zero at flow one.
The low-quality investor strictly prefers zero.
The challenger strictly prefers its stated action away from the threshold.

There is no other positive-purchase outcome.
Before $\alpha_T$, $K_F<k$ excludes an interior investor choice.
At $\alpha_T$, equation (10) gives the unique feasible entry rate with investor indifference.
After $\alpha_T$, $K_A$ strictly decreases and crosses $k$ once, at $\alpha_A$.
At full purchases, $K_A(1)<k$ excludes $\beta=1$.
This proves the exact count of three outcomes. $\square$

**Analytical robustness.** The equality $u=v$ permits the rational formula in (8).
The coexistence result does not require this equality.
With entry vector $(\rho,\rho,1,1)$, general noise gives

$$
\frac{\partial K_r}{\partial\alpha}
=-\Delta\left[\frac{\rho uv(u-v)}{D_0^2}
+\frac{vw(v-w)}{D_1^2}\right].
$$

This derivative is strictly negative at the construction, uniformly on the compact interval $I$.
Every entry inequality, investor endpoint margin, and interior probability bound is also strict throughout $I$.
Continuity and the implicit function theorem preserve the upward branch under sufficiently small noise changes.
They also preserve no trade and the simultaneous-mixture branch.
The strict margins have positive minima on $I$, so one neighborhood works for the whole interval.

For the nearby upward branch, $K_r=\Delta L(\alpha)$ with $L$ independent of $r$.
Its derivative condition gives

$$
\alpha'(r)=-\frac{\Delta'(r)L(\alpha)}{\Delta(r)L'(\alpha)}>0,
\qquad
\mathsf E=\rho+(1-\rho)(w+v\alpha/2).
$$

Thus its entry also rises strictly.
In particular, the neighborhood includes noise laws with three pairwise different probabilities, such as small changes with $u>v>w$.

### Proposition C9.4 — analytical: what each mixture does

The simultaneous mixtures in (9)–(10) give an interior trade intensity.
Their roles differ.
The preparation condition pins $\alpha_T$ through $\mu_1(\alpha_T)=\tau$.
The investor's condition then pins $\sigma_T$ through zero purchase profit.
Thus the noise law and the preparation threshold determine the purchase frequency on this branch.

However, challenger indifference does not cause the upward entry comparison in Proposition C9.3.
On that upward branch, expensive preparation is pure at every on-path price.
The investor alone uses an interior probability.
Allowing challenger mixtures adds the other informative equilibrium and ensures general existence.

Feedback remains essential for the upward branch in this example.
If expensive preparation is suppressed, $K_F(\alpha)\le\Delta/10<k$ for every $\alpha$.
Every purchase then loses money.
The informative equilibria therefore require the entry response, even though one branch uses pure preparation.

The expected high-quality order is $\beta$; the expected low-quality order is zero.
This gives an endogenous measure of information intensity.
It does not recover the paper's order pattern $(1,-v)$.
The discrete order size remains either zero or one.
The buy-only constraint fixes low-quality abstention before equilibrium is solved. $\square$

### Proposition C9.5 — analytical: an actual existence gap under pure preparation

The previous existence theorem needs challenger mixtures over the full parameter domain.
Here is a case where investor mixtures alone cannot repair existence.
Keep the auction benchmark and $c_L=0$, but set

$$
r=3,\quad \lambda=1,\quad c_H=83/24,\quad k=1/10,
\quad (u,v,w)=(1/5,1/5,3/5).
$$

Then $\Delta=2/3$ and $\tau=2/5$.
The posterior at flow zero stays at $1/2$.
The posterior at flow one falls through $2/5$ at $\alpha=1/2$.
Thus $e_0=1$ throughout, while $e_1$ drops from one to $1/4$.

If an indifferent challenger must prepare, gross purchase profit is

$$
K(\alpha)=
\begin{cases}
\displaystyle\frac23\left[\frac1{10}+\frac3{10(3-\alpha)}\right],&0\le\alpha\le1/2,\\[6pt]
\displaystyle\frac23\left[\frac1{10}+\frac3{40(3-\alpha)}\right],&1/2<\alpha\le1.
\end{cases}
$$

On the first interval, $K\ge2/15>1/10=k$.
On the second, $K\le11/120<1/10=k$.
No trade fails, full purchases fail, and no interior zero-profit choice exists.
This proves nonexistence under that pure preparation rule.

Allow preparation at indifference instead.
Choose

$$
\beta=\alpha=1/2,\qquad
(\mu_{-1},\mu_0,\mu_1,\mu_2)=(1/3,1/2,2/5,1),
$$

$$
(e_{-1},e_0,e_1,e_2)=(1/4,1,5/12,1),
\qquad \sigma_1=2/9.
$$

Equation (1) gives $K=(2/3)[1/10+(5/12)(3/25)]=1/10=k$.
Each challenger choice is optimal at its posterior.
The low-quality purchase payoff is $-53/90<0$.
The entry probability is $143/240$.
This is an exact equilibrium with both mixtures. $\square$

### Analytical qualification: the benchmark does not need this existence repair

If $B_r(1/2)<c_H$, investor mixtures alone already ensure existence under the directional completion.
Each relevant posterior starts at $1/2$ and moves monotonically with $\alpha$.
A decreasing posterior never reaches the higher threshold $\tau$.
An increasing posterior crosses it only upward.
Thus every preparation jump in purchase profit is upward.

If no trade fails, purchase profit starts above zero.
If full purchases also fail, it ends below zero.
An upward jump cannot cause this downward sign change.
Continuity between the finitely many upward jumps therefore gives an interior zero.
This proves the qualification.

At $c_H=6$, the benchmark has $B_r(1/2)<6$ for every $r>1$.
The prior check's many gaps concern broader menus or other cost restrictions.
Those gaps do not establish nonexistence for the present buy-only benchmark with $c_L=0$.
Proposition C9.5 uses a lower $c_H$ to establish the repair within this memo's maintained domain.

## 4. What it recovers or loses relative to the Laplace paper

- **Proposition 1:** the auction comparison survives unchanged.
  A larger $r$ raises $\Delta$ and lowers both gross acquisition profits.
- **Proposition 2(i)–(ii):** information can still raise entry.
  Unequal noise introduces additional entry thresholds and multiple equilibria.
  The equal-noise single cutoff no longer describes the correspondence.
- **Proposition 2(iii):** the Laplace information ceiling is lost.
  Every positive purchase probability with $w>0$ creates posterior one at flow two.
  With benchmark costs, expensive preparation can persist until $r=4+\sqrt{63}/2\simeq7.968627$.
  Preparation at equality can be either pure or mixed under the present convention.
- **Proposition 3 and Section 4.3:** ordered informative equilibria and no-trade coexistence are recovered.
  Equations (5)–(8) give a continuous upward branch, with exact certificates at three rational strengths.
  A second informative branch exists in each economy.
  Its reported entry values move downward across the same strengths.
- **Proposition A.3:** fixed-experiment deterrence survives.
  Both $g_H$ and $g_L$ decrease with $r$ at every fixed belief.
  The upward branch changes the purchase probability and therefore changes the experiment.
- **Proposition A.4:** the three cutoff concepts remain distinct.
  Equation (3) replaces the Laplace no-trade condition.
  Equation (2) describes full purchases and interior mixtures.
  The expensive-entry ceiling uses $g_H$, rather than a posterior upper bound below one.
- **Propositions A.5–A.6 and Section 5.1:** this memo changes the noise law and the indifference convention.
  It does not establish the paper's logistic or atomless-cost results for this discrete model.
- **Proposition A.7 and Section 5.3:** complementary private signals remain outside the present setup.
- **Proposition A.8 and Section 6.2:** the result uses the benchmark auction receipts.
  It does not solve the alternative payment rule.
- **Proposition A.9 and Section 6.1:** entry and ownership follow from exact flow sums.
  A welfare comparison requires preparation costs and allocation gains, beyond entry alone.
  The paper's welfare numbers do not carry over directly.
- **Proposition A.10 and Section 6.3:** the fixed reserve keeps the positive entry floor.
  Price pools cannot conceal different posteriors here.
  Reserve choice outside this domain remains a separate problem.

## 5. Numerical example

### Exact rational certificates — computer-assisted

The program uses `fractions.Fraction` for every parameter, posterior, price, payoff, and entry probability.
It computes all feasible investor action payoffs against each fixed schedule.
It also recomputes the challenger posterior from the groups of equal prices.
The resulting belief differences and price-equation differences are exactly zero.
Every parameter and every flow appears in the saved CSV files.

The command is:

```text
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C9_unequal_mixing/certificates.py
```

For the upward branch, the exact output is

$$
\begin{array}{c|c|c|c}
r&\beta_A&\mathsf E_A&U_L(1)\\ \hline
63/40&1258/1487&1567/2974&-529/7200\\
79/50&2090/2319&4137/7730&-5887/79000\\
317/200&35450/37031&201299/370310&-95823/1268000
\end{array}
$$

Every high-quality purchase payoff is exactly zero.
Each low-quality investor strictly prefers zero.
The entry vector is $(1/4,1/4,1,1)$ at all three points.
The high-cost preparation margins at flow one are, respectively,

$$
\frac{10921}{1421952},\qquad
\frac{3479731}{53151200},\qquad
\frac{187972799}{1542902400}.
$$

All three margins are strictly positive.
The entry differences are exactly

$$
\mathsf E_{A,2}-\mathsf E_{A,1}=\frac{47632}{5747255}>0,
\qquad
\mathsf E_{A,3}-\mathsf E_{A,2}=\frac{240688}{28624963}>0.
$$

The approximate entry values are $0.526900$, $0.535188$, and $0.543596$.
High-quality ownership is $\mathsf O_H=1/5+3\alpha_A/20=\mathsf E_A-1/5$.

The independent no-trade purchase payoffs are

$$
-\frac{479}{50400},\qquad
-\frac{739}{79000},\qquad
-\frac{11671}{1268000}.
$$

Thus each economy separately supports no trade, with entry $1/4$ and high-quality ownership $1/8$.

The simultaneous-mixture certificates are

$$
\begin{array}{c|c|c}
r&\beta_T&\sigma_T\\ \hline
63/40&13249/15791&16652273/16706878\\
79/50&20791/24734&121328033/124807764\\
317/200&5303/6297&490344541/517197798
\end{array}
$$

All six probabilities lie strictly between zero and one.
The preparation margin at flow one is exactly zero.
The high-quality purchase payoff is exactly zero.
The low-quality purchase payoff is strictly negative at every point.
The corresponding entry values are approximately $0.525157$, $0.520148$, and $0.515255$.
Their exact fractions appear in `summary.csv`.

Presence below one does not invalidate the construction.
For example, at $r=317/200$ and $\lambda=49/50$, the upward branch has

$$
\beta_A=1772500/1814519<1,
\qquad \alpha_A=35450/37031.
$$

Its flow experiment and entry probability remain the same.
More generally, equation (5) applies whenever $\lambda>\alpha_A(r)$.

The program also reproduces the exact gap example in Proposition C9.5.
The source file and outputs are:

- [certificates.py](../scripts/C9_unequal_mixing/certificates.py): the equilibrium evaluator and explicit schedules.
- [summary.csv](../scripts/C9_unequal_mixing/summary.csv): exact parameters and equilibrium outcomes.
- [flows.csv](../scripts/C9_unequal_mixing/flows.csv): exact posteriors, prices, entry rates, and preparation margins.
- [run.txt](../scripts/C9_unequal_mixing/run.txt): the printed schedules and exact entry differences.
- [receipt.json](../scripts/C9_unequal_mixing/receipt.json): source commit, run date, output sizes, and hashes.

## 6. Open issues

- Global existence is proved for this buy-only game and the stated completion.
  The result does not cover a fixed arbitrary off-path belief rule.
- Equation (2) characterizes every equilibrium purchase probability.
  A global classification of all parameter regions remains unwritten.
- The explicit interval gives exactly three outcomes under its maintained parameters.
  Other noise laws can give a different number of outcomes or continua.
- A universal upward entry claim is false for the informative outcomes considered here.
  The simultaneous-mixture branch gives the opposite comparison at the certified points.
- The model recovers an interior expected order, but not the paper's endogenous short magnitude.
  It also retains full revelation at an extreme flow.
- Welfare, private signals, an initial stake, and endogenous reserves remain outside this memo.
- The finite schedules have exact arithmetic certificates.
  A separate independent review remains a later task under the team ledger.

No equal-noise claim in the brief is refuted.
Its loss of coexistence concerns the equal-noise base model.
This memo modifies that noise law and its indifference convention.
The general nonexistence warning needs its original menu and cost qualifications.

## 7. Plain summary

Unequal noise can restore the paper's coexistence pattern in a buy-only model.
The low-quality investor never buys.
The high-quality investor chooses a purchase probability.

If both sides may randomize at indifference, an equilibrium exists for every admissible parameter vector.
This result uses a stated belief after an unused purchase flow.
Preparation at indifference fills a gap in the investor's profit schedule.
An exact example shows that the gap can otherwise remove every equilibrium.

With benchmark auction values and noise probabilities $(2/5,2/5,1/5)$, one interval has exactly three outcomes.
They are no trade and two informative equilibria.
On one informative branch, stronger incumbents raise the purchase probability and entry.
Exact entry probabilities rise from about $0.526900$ to $0.535188$ to $0.543596$ at three rational strengths.
Every economy also supports no trade with entry $0.25$.

The other informative branch has both investor and challenger mixtures.
Its entry falls across those same strengths.
Thus coexistence does not imply that every informative branch has higher entry under stronger competition.

The interior purchase probability supplies an endogenous information intensity.
It does not reproduce the paper's partial short sale.
The buy-only constraint fixes low-quality abstention, while the extreme flow still reveals high quality fully.
Challenger mixtures ensure general existence, but pure preparation suffices on the upward branch.
