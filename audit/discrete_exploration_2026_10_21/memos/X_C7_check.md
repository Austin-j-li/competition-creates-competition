# Independent check of C7: incumbent bids after the price

## 1. Scope

This memo checks C7.1 and C7.3–C7.10 in [C7_incumbent.md](C7_incumbent.md).
It checks the stated equilibrium selection and the main numerical claims.
It also compares the baseline branches with [B_dlaplace_numeric.md](B_dlaplace_numeric.md).
It does not revise either memo or the paper.

The base uses discrete-Laplace noise, buy-only orders, and $c_L=0$.
Unless stated otherwise, the parameters are

$$
(h,\ell,p,\rho,c_H,b,k,\pi,\lambda)
=(10,1,1/2,1/4,5,2,1/50,1/2,1).
$$

The paper source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
The source reads use `git -C overleaf/paper show <commit>:main.tex` and the corresponding appendix command.
Main equation (4) and appendix equation (OA.5) give the stated auction objects.
Main Section 2 gives the information sets and the preparation tie rule.

Independent calculations appear in [the script folder](../scripts/X_C7_check/).
The first calculations use 70 decimal digits and precede inspection of the original scripts.
A separate calculation uses exact fractions and alternating bounds for $e^{-1/2}$.
Only after these calculations did I inspect the original scripts and rerun their benchmark command.
All runs use the shared slot wrapper.

The equilibrium concept is perfect Bayesian equilibrium with competitive prices.
Investor deviations hold the price and continuation schedules fixed.
Indifferent investors may mix.
The high-cost challenger stays out at the selected bid boundary.
At other ties, the challenger prepares.
The board rejects indifferent private offers.

## 2. Verdict table

| Claim | Verdict | Evidence |
|---|---|---|
| C7.1: no private lockup | CONFIRMED WITH CORRECTION | Analytical. The result holds, but its final null-set argument needs an incentive argument. |
| C7.3: strong types deter; weak types face entry | CONFIRMED WITH CORRECTION | Analytical under IC-P and the stated ties. The claim about silence pooling is false. |
| C7.4: transfer at fixed information | CONFIRMED | Analytical for the selected continuation. A different bid can also raise surplus. |
| C7.5: neutralization and unique trade under N | CONFIRMED | Analytical under the selected continuation. Independent profits match. |
| C7.6: weaker Proposition 2 | CONFIRMED | Analytical conditional on selection. Exact rational bounds reproduce the benchmark values. |
| C7.7: three-point trade stays unchanged | CONFIRMED | Analytical with the usual revealing belief at the off-path top flow. |
| C7.8: new mixed branches | CONFIRMED WITH CORRECTION | Continuity is analytical. The reported locations are numerical diagnostics. The baseline comparison needs narrower wording. |
| C7.9: intermediate-strength entry peak | CONFIRMED WITH CORRECTION | The path reproduces numerically. The floor starts strictly above $r_C$, rather than at equality. |
| C7.10: continuous-Laplace comparison | CONFIRMED | Numerical diagnostic. Entry, ownership, and the surplus increment reproduce. |

The auxiliary claim that silence pooling survives both refinements is **REFUTED**.
The universal claim about every bid through $\ell$ also needs a restriction.
Neither error changes the selected benchmark values.

## 3. Derivations and evidence

### 3.1 Game form and beliefs

The incumbent privately observes $R$ and publicly observes the stock price.
It does not observe challenger quality.
The challenger observes both the price and the public bid before preparation.
The challenger then observes its cost.
Preparation reveals its value.
The board observes the private offer in Model L.

Conditional on a price, a bid conveys information about $R$.
It does not convey extra information about quality.
The public posterior $\mu$ therefore remains the quality posterior after the bid.
The distribution of $R$ can change after the bid.
This distinction is necessary for every deterrence calculation.

A public bid is a payment floor, not an immediate sale.
The seller commits to this institution before trade.
Seller optimality over alternative auction rules is outside this game.
In Model L, board optimality is a separate decision and requires the argument below.

IC-P is explicit: retain types that can strictly gain at the proposed bid, then use prior proportions.
This is a possible completion of beliefs under the Intuitive Criterion.
It is an additional assumption, rather than a consequence of that criterion.
It need not satisfy D1's stricter comparison between types.
The scripts apply the selected formulas consistently.
They do not derive that belief rule from a perturbation of the game.
For bids above $r$, the fallback restriction $R\ge J$ is empty.
Cap bids at $r$, or complete the beliefs for those unprofitable deviations.

### 3.2 C7.1: the lockup result

**Status: analytical.**

Fix the continuation after no accepted offer.
Let its entry probability be $e\ge\rho$.
The challenger does not observe the private offer.
Its continuation strategy therefore does not depend on the offer price.

For $R\ge p$, the target and incumbent jointly receive $R$ in every auction outcome.
If the challenger wins, the target receives $R$.
If the incumbent wins at payment $T_A$, the sum is $T_A+(R-T_A)=R$.
This identity does not hold for $R<p$.
Such a type cannot benefit from an accepted offer $T\ge p$.

For $R\ge p$, let the target's continuation proceeds be

$$
W(R)=e\{\mu R+(1-\mu)\min(R,\ell)\}+(1-e)p.
$$

An offer accepted with probability $s(T)>0$ changes the incumbent's payoff by

$$
s(T)[W(R)-T].
$$

Thus every type that uses an accepted offer needs $W(R)\ge T$.
The board accepts only if $T\ge\mathbb E[W(R)\mid T]$.
Both inequalities imply equality for almost every type behind an accepted offer.
The stated board tie rule then excludes acceptance.

The memo's stronger claim for $\mu>0$ also holds.
Its stated proof does not establish that claim.
A singleton preimage for each price does not exclude a continuum of distinct offers.
The missing argument uses imitation.

If an accepted offer satisfies $T<W(r)$, a stronger type can copy that offer and gain strictly.
Every type's equilibrium gain from an accepted offer equals zero by the preceding argument.
The deviation is therefore profitable.
Only types at the maximum of $W$ can remain.
For $\mu>0$, $W$ is strictly increasing, so that type has probability zero.
This completes the proof under other tie rules.

### 3.3 C7.3: selected bids and the refinement errors

**Status: analytical.**

For a bid $J\le R$, define the incumbent's gain from deterrence as $G(R;J)$.
After silence with full entry, its payoff is

$$
U_S=(1-\mu)(R-\ell)_+.
$$

After deterrence, its payoff is

$$
U_J=(1-\rho)(R-J)+\rho(1-\mu)(R-\max(J,\ell))_+.
$$

For $J\le\ell$, subtraction gives

$$
G(R;J)=
\begin{cases}
(1-\rho)(R-J),&J\le R\le\ell,\\
(1-\rho)[\mu R+(1-\mu)\ell-J],&R>\ell.
\end{cases}
$$

For $J>\ell$, subtraction gives

$$
G(R;J)=(R-J)(1-\rho\mu)-(1-\mu)(R-\ell).
$$

These expressions give the cutoff

$$
c(J)=
\begin{cases}
J,&J\le\ell,\\
\ell+\dfrac{(J-\ell)(1-\rho\mu)}{\mu(1-\rho)},&J>\ell.
\end{cases}
$$

The challenger faces $R\sim U[c,r]$ after the common deterring bid.
For $c\ge p$, its gross profit is

$$
D_\mu(c)=\mu\left(h-\frac{c+r}{2}\right)
+(1-\mu)\frac{(\ell-c)_+^2}{2(r-c)}.
$$

This expression decreases in $c$.
Its limit is $\mu(h-r)$.
Thus deterrence is impossible when this limit reaches $c_H$.
Otherwise, the selected cutoff is $c^*=\max(p,a^*)$, where $D_\mu(a^*)=c_H$.
The inverse of $c(J)$ gives the selected bid.

For a smaller bid, IC-P retains types above its smaller cutoff.
Their average challenger profit exceeds $c_H$ when $c^*>p$.
The smaller bid therefore fails to deter.
For a larger bid, the incumbent pays more without further entry reduction.
This establishes the selected financial outcome.

After silence, the selected belief is $U[0,c^*)$.
It gives a weakly higher gross profit than $U[0,r]$.
The high-cost challenger therefore enters after silence in Case C.
Costless, non-deterring bids by weak types can replace silence at indifference.
The literal claim that every weak type stays silent needs this normalization.

The altered challenger tie rule matters.
With continuous bids and preparation at equality, an interior cheapest deterring bid does not exist.
Every strictly deterring bid admits a slightly smaller strictly deterring bid under IC-P.
The memo's boundary convention defines an equilibrium of the altered game.
Its bid-grid construction gives the same limit under the original tie rule.
These two statements should remain distinct.

**The silence-pooling claim is false.**
At $r=3$, $\mu=3/5$, and $c_H=5$, suppose every type stays silent and entry equals one.
A public bid $J=2$ bounds challenger profit by

$$
\mu(h-J)=\frac{24}{5}<5.
$$

This bound holds under every belief about $R$ because the bid itself is binding.
The bid therefore deters regardless of off-path beliefs.
Type $R=3$ gains

$$
(3-2)(1-\rho\mu)-(1-\mu)(3-1)
=\frac1{20}>0.
$$

A positive interval of nearby types also gains.
Silence pooling fails even without a refinement at this posterior.
At the actual benchmark posterior $M_1$, the same bid deters and type $3$ gains $0.089303830$.

The claimed whole continuum through $\ell$ is also too broad.
Take $r=6/5$, $\mu=11/20$, and $c_H=5$.
These values lie in Case C, with the selected cutoff below $\ell$.
Consider the proposed larger bid $J'=\ell=1$.
A smaller bid $J=99/100$ bounds challenger profit by

$$
\mu h+(1-\mu)\ell-J=\frac{124}{25}=4.96<5.
$$

It therefore deters under every belief.
A type already above the proposed cutoff saves $(1-\rho)(J'-J)=3/400>0$.
Thus $J'=\ell$ cannot survive.

A continuum does survive at the benchmark posterior.
There $\mu(h-\ell)>c_H$.
For $J^*<J'\le\ell$, a lower bid can receive beliefs on weak types that induce entry.
For a weak type $J<R<J'$, every costly-entry probability $s<1$ makes the deviation profitable.
For a strong type $R>\ell$, the deviation is profitable only if

$$
s<\frac{J'-J}{\mu R+(1-\mu)\ell-J}<1.
$$

D1 can therefore retain the weak types alone.
The memo incorrectly writes $R-J$ in this denominator for $R>\ell$.
IC-P instead retains prior proportions over all profitable types.
That extra restriction selects the smaller bid.

### 3.4 C7.4: transfers and surplus

**Status: analytical.**

Only the costly challenger's entry changes for types above $c^*\ge p$.
For these types, the joint target and incumbent payoff remains $R$.
Consequently,

$$
\Delta T=-\Delta U_I
=-\frac1r\int_{c^*}^rG(R;J^*)\,dR.
$$

For $R\ge p$, the allocation gain from entry equals $(\theta-R)_+$.
This is also the challenger's gross auction profit.
Removal of costly entry therefore changes challenger payoff and surplus by the same amount:

$$
\Delta C=\Delta W
=(1-\rho)\left(1-\frac{c^*}{r}\right)[c_H-D_\mu(c^*)].
$$

At an interior selected cutoff, the last bracket is zero.
At the reserve corner, the bracket is nonnegative.
This proves all three statements under the selected continuation.

The pure-transfer result needs the selected cutoff.
At the benchmark, the alternative equilibrium bid $J'=\ell$ gives $c'=\ell$.
Its ex ante surplus gain is

$$
\frac12(1-\rho)\left(1-\frac\ell r\right)[5-8M_1]
=0.005081338>0.
$$

The target-incumbent transfer identity still holds under that alternative.
Zero surplus gain does not.

### 3.5 C7.5: spread, profit, and uniqueness

**Status: analytical.**

Let $S$ be the target payoff in class H minus its payoff in class L.
Competitive prices give residuals $(1-\mu)S$ and $-\mu S$.
Since $S\ge0$ and $k>0$, the low class never buys.

For a fixed price, the selected continuation fixes $V_L(P)$ and $S(P)$.
The positive spread bound in Section 3.6 gives

$$
P=V_L(P)+\mu_X S(P),\qquad
\mu_X=\frac{P-V_L(P)}{S(P)}.
$$

Thus the price reveals the flow posterior.
The challenger needs no separate observation of flow.
At the benchmark, $P_G=0.946180002001$ and $P_B=0.594173444800$.

For a silent incumbent, the class gap is $e(R-\ell)_+$.
For a deterring incumbent, it is $\rho(R-\max(J,\ell))_+$.
Thus, in Case C,

$$
S=\frac1r\left[
\int_0^{c^*}(R-\ell)_+\,dR
+\rho\int_{c^*}^r(R-\max(J^*,\ell))_+\,dR\right].
$$

If $c^*\le\ell$, then $J^*=c^*\le\ell$ and $S=\rho\Delta_T$.
Condition N guarantees this relation at every feasible posterior.
It also excludes Case B.
Hence the purchase profit equals the profit under entry fixed at $\rho$.

Write $a=e^{-1/b}$, $m=a/(1+a)$, and $M=1/(1+a)$.
At purchase probability $\beta$, define

$$
\mu_B=\frac{1-\beta(1-a)}{2-\beta(1-a)},\qquad
\mu_G=\frac{1+\beta(1/a-1)}{2+\beta(1/a-1)}.
$$

A purchase reaches these two regions with probabilities $m$ and $M$.
Under Condition N,

$$
\Pi(\beta)=\rho\Delta_T
\left[\frac{m}{2-\beta(1-a)}+
\frac{M}{2+\beta(1/a-1)}\right]-k.
$$

The derivative is negative for $\beta<1$.
After cancellation of positive factors, this is equivalent to

$$
a[2+\beta(1/a-1)]<2-\beta(1-a),
$$

which holds exactly when $\beta<1$.
Therefore the investor outcome is unique.
The endpoint gross profits are $\rho\Delta_T/2$ and $2\rho mM\Delta_T$.
They give the memo's three cost regions.

At $r=3$, the independent net profits are $0.175836426835$ without preemption and $0.058334570734$ with preemption.
The latter equals the fixed-entry profit.
These values match the original output.

At the benchmark, larger equilibrium bids through $\ell$ also leave $S=\rho\Delta_T$.
Thus profit neutralization survives that particular continuum.
It does not follow under unrestricted continuation beliefs or bids above $\ell$.

### 3.6 C7.6: weaker Proposition 2 and benchmark arithmetic

**Status: computer-assisted for the benchmark values.**

The general argument is analytical under the stated selection.
At weak strength, $S\le\Delta_T<k$, so every purchase loses money.
At strong strength, let $x=c^*-\ell$ and $y=r-c^*$ when $c^*>\ell$.
The spread satisfies

$$
S\ge\frac{x^2+\rho y^2}{2r}
\ge\frac{\rho}{1+\rho}\frac{(x+y)^2}{2r}
=\frac{\rho\Delta_T}{1+\rho}.
$$

The second inequality follows from $(x-\rho y)^2\ge0$.
The posterior bound gives a purchase residual of at least $m\rho\Delta_T/(1+\rho)$.
The stated strict cost bound therefore forces full purchases.

Good news has probability $1/2$ under full purchases.
Conditional on class H, it has probability $M$.
Thus

$$
\mathsf E=\rho+\frac{1-\rho}{2}\frac{c^*}{r},\qquad
\mathsf O_H=\frac\rho2+\frac{1-\rho}{2}M\frac{c^*}{r}.
$$

The exact rational calculation brackets the cutoff within

$$
0.93590073908012834872292351338292634245041815586720
<c^*<
0.93590073908012834872292351338292634245041815586721.
$$

The lower endpoint gives $D-c_H>0$.
The upper endpoint gives $D-c_H<0$.
The exponential bounds come from consecutive odd and even partial sums of its alternating series.
All subsequent interval endpoints use exact fractions.

| Quantity at $r=3$ | Base | Selected preemption |
|---|---:|---:|
| Entry | 0.625000000000 | 0.366987592385 |
| High-class ownership | 0.358422249201 | 0.197820018515 |
| Target proceeds | 0.942073166134 | 0.770176723400 |
| Incumbent payoff | 0.568343500533 | 0.740239943266 |
| Challenger payoff | 1.189977076672 | 1.189977076672 |
| Surplus | 2.700393743339 | 2.700393743339 |

The proceeds loss is $0.171896442734$.
The preemption probability is $0.344016543487$.
Independent surplus uses allocation values and preparation costs directly.
The largest printed discrepancy from the payoff sum is below $10^{-69}$.

The selection qualification is economically material.
At the weak strength, the alternative reserve-bid equilibrium gives

$$
\mathsf E(r_0)=\rho+(1-\rho)\frac{p}{r_0}=0.5625.
$$

There, silence reveals $R<p$ and costly preparation earns exactly its cost.
The prescribed preparation tie supports entry after silence.
Trade stays absent because the spread stays $\rho\Delta_T$.
Comparing this weak equilibrium with the selected strong equilibrium reverses the reported entry increase.
The statement of C7.6 acknowledges this selection; the plain summary should do so too.

### 3.7 C7.7: three-point noise

**Status: analytical.**

With equal three-point noise, the two middle flows retain posterior $1/2$.
The top flow reveals H whenever H buys with positive probability.
At no trade, use the usual off-path completion $\mu(2)=1$.
Without that completion, the numerical cutoff needs a separate belief statement.

At the top flow, the investor's residual is $(1-1)S=0$.
At the two middle flows, selected entry remains $\rho$.
A purchase reaches each middle flow with probability $1/3$.
Its gross profit is therefore

$$
\frac23\frac12\rho\Delta_T=\frac{\rho\Delta_T}{3}.
$$

Preemption at the top cannot change this profit.
At $r=3$, the gross profit is $1/18$ and the net profit is $0.035555556$.
At posterior one, every challenger profit is at least $h-r=7$.
This exceeds both costs five and six.
No credible bid deters at the benchmark.

### 3.8 C7.8 and comparison with the baseline memo

**Status: numerical diagnostic for the reported regions.**

The continuity argument is analytical.
At the entry threshold, the reserve corner has spread $\rho\Delta_T$.
Inside Case C, its cutoff and bid are continuous.
At the deterrence limit, the cutoff approaches $r$ and the spread approaches $\Delta_T$.
Thus $\Pi(\beta)$ is continuous under the selected continuation.
Opposite profit signs imply an interior investor mixture.

Exact rational bounds also establish a mixed equilibrium at $r=8/5$.
Parameterize the Case C cutoff above $\ell$ by $c$.
Set

$$
\mu(c)=\frac{c_H}{h-(c+r)/2},\qquad
\beta(c)=\frac{a[2\mu(c)-1]}{(1-a)[1-\mu(c)]}.
$$

At $c=13/10$, the profit is strictly negative.
At $c=7/5$, the profit is strictly positive.
The exact bounds give $-0.003086726$ and $0.001265262$, respectively.
Both points are inside Case C.
Continuity therefore gives a mixture with partial preemption between them.
This local existence certificate does not certify every reported strength interval.

The independent numerical solution is

$$
\begin{aligned}
\beta^*&=0.652591541220,&\mu_G&=0.587348094878,\\
c^*&=1.374321212234,&J^*&=1.193272144646,\\
\mathsf E&=0.544699515028,&\mathsf O_H&=0.298091198713.
\end{aligned}
$$

The preemption probability is $0.064523905780$.
The memo's $0.064520$ expands a coarser printed figure and is inaccurate at six decimals.
Use $0.064524$ at that precision.

| Strength | Baseline interior purchases, pure challenger | Selected preemption interior purchases |
|---|---|---|
| 1.41 | 0.276593586 | None found |
| 1.43 | 0.682037546 | 0.616394501; 0.682037546 |
| 1.44 | 0.915696442 | 0.618914663; 0.915696442 |
| 1.60 | None | 0.652591541 |
| 1.75 | 0.035613612 | 0.035613612; 0.659482157 |
| 1.765 | None | 0.341749806; 0.655814474 |
| 1.79 | None | 0.617245940; 0.637773527 |
| 1.795 | None | None found |

The baseline findings agree with B1.
Its high-entry interior branch starts at $r_S=1.405429758473$.
It ends when full purchases first exist at $r_F=1.443321951458$.
No trade and full purchases coexist on $[r_F,r_N]$, where $r_N=1.747877538268$.
These intervals describe different branches.

The baseline also admits a threshold branch when the challenger may mix.
It lies at $\mu_G=\tau_r$ and is distinct from the high-entry interior branch.
C7's script marks discontinuity crossings and excludes them under its pure challenger rule.
B1 includes them with the required challenger mixture.
There is no numerical contradiction.

C7.8 should say that a root at the entry discontinuity needs challenger mixing.
Its broader suggestion that every baseline interior root needs such mixing is false.
The memo's own table supplies counterexamples at $r=1.43$ and $1.44$.

### 3.9 C7.9: strength path and the endpoint

**Status: numerical diagnostic for the path.**

The threshold equations are analytical.
At a fixed posterior, a larger $r$ lowers $D_\mu(c)$.
The selected interior cutoff therefore falls with $r$.
Its ratio to $r$ also falls.
The reserve corner gives the same monotonicity through $p/r$.

At full purchases, the thresholds reproduce as follows:

$$
\begin{aligned}
r_D&=1.967346701437,\\
r_N^{\mathrm{N}}&=2.934693402874,\\
r_{\mathrm{corner}}&=3.485483390653,\\
r_C&=3.986096571638.
\end{aligned}
$$

Here $r_N^{\mathrm{N}}$ denotes Condition N's threshold.
It differs from B1's no-trade threshold $r_N$.

Selected entry equals $0.594760988$, $0.477248990$, and $0.392722816$ at strengths $2.05$, $2.45$, and $2.85$.
It equals $0.359204951$, $0.307661949$, and $0.298701299$ at strengths $3.05$, $3.45$, and $3.85$.
These values match the original sweep.
At strength $4.05$, selected entry equals $0.25$.
The entry gain is largest at intermediate strength along this selected path.

At the exact ceiling, however, $B_{r_C}(M)=c_H$.
The memo's Case C applies because preparation at a silence tie is required.
The selected good-news cutoff remains $p$.
Therefore

$$
\mathsf E(r_C)=\rho+\frac{1-\rho}{2}\frac{p}{r_C}
=0.297038499101>\rho.
$$

The floor starts strictly above $r_C$ under minimal preemption.
The phrase “at $r_C$ it drops” needs this endpoint correction.
Alternative reserve-bid equilibria can preserve extra entry above the ceiling.

### 3.10 C7.10: continuous Laplace noise

**Status: numerical diagnostic.**

Use the paper's $c_H=6$, $b=2$, $r=3$, and full orders $(1,-1)$.
The posterior is $\mu(x)=[1+\exp(-x)]^{-1}$ on $[-1,1]$.
Outside that interval, it stays at the endpoint posterior.
The upper endpoint is $M=0.731058578630$.

Condition N holds because $8M<6$.
Every feasible posterior and credible bid gives low-cost gross profit of at least

$$
m(h-r)=1.882589949590>1.
$$

Thus either low cost zero or low cost one gives the same continuation here.
This statement concerns feasible posteriors, rather than every posterior in $[0,1]$.
The paper's full-order bound equals $0.022411785114>k$.
The constant spread therefore preserves unique full orders.

Let $f_H(x)=f(x-1)$ and $f_L(x)=f(x+1)$.
I integrate entry against $(f_H+f_L)/2$.
I integrate ownership against $f_H/2$.
The calculation splits at $-1$, the entry threshold, the corner threshold, and $1$.
It integrates both infinite tails without truncation.

The threshold flows are $0.871222446472$ and $0.972461003341$.
The independent results are

$$
\begin{aligned}
\mathsf E_{\rm base}&=0.522757297260,&
\mathsf E_{\rm jump}&=0.304839864013,\\
\mathsf O_{H,\rm base}&=0.324192425776,&
\mathsf O_{H,\rm jump}&=0.165056181179,\\
\Delta W&=0.000888683585.
\end{aligned}
$$

All values agree with the original output at its printed precision.
The surplus increment comes from the reserve corner.
This evidence remains numerical rather than an interval certificate.

### 3.11 Script comparison and status labels

The independent script uses direct polynomial integrals over incumbent values.
Its cutoff calculation uses bisection of expected challenger profit.
The original code instead uses a quadratic cutoff and integrals over linear pieces.
The two methods give the same benchmark outcomes.

After the independent calculations, I reran `c7_benchmark.py` through its command interface.
The fresh output matches the saved benchmark output.
The comparison appears in `original_benchmark_comparison.txt`.
I also inspected the original interval certificate, region output, and Laplace output.

The analytical labels for C7.4, C7.5, and C7.7 are deserved within their stated scope.
C7.1 needs the imitation argument to complete its stronger statement.
C7.3 needs the refinement corrections above.
C7.6 deserves its computer-assisted benchmark label.
Its original certificate prints sixteen strict margins.
The independent rational enclosures reproduce its main results.

C7.8's continuity result is analytical.
The whole regional correspondence remains a numerical diagnostic.
Endpoint sign changes alone do not establish its two-root regions when both endpoint signs agree.
The table needs numerical interior signs or a separate certificate there.
C7.9 and C7.10 correctly retain numerical diagnostic labels for their paths and integrals.

## 4. Errors found and corrections

1. **Refuted claim:** both refinements support silence pooling throughout Case C.
   A binding bid can deter under every belief and give a strict gain.
2. **Refuted claim:** every larger bid through $\ell$ survives.
   The exact example in Section 3.3 gives a profitable lower bid under every belief.
3. **Proof gap:** null probability at each private offer does not establish zero total trade.
   Add the imitation argument in Section 3.2.
4. **D1 algebra:** for $R>\ell$, replace $R-J$ by $\mu R+(1-\mu)\ell-J$ in the deviation threshold.
5. **Action normalization:** non-deterring bids can cost weak types nothing.
   Select silence at such indifference, or state uniqueness in financial outcomes.
6. **Tie scope:** distinguish the altered continuous game from the limit of games with bid ticks.
7. **Endpoint:** at $r_C$, selected entry is $0.297038499$, rather than $0.25$.
   The floor starts strictly above the ceiling.
8. **Baseline wording:** some interior investor mixtures require no challenger mixture.
   Only the root at the entry jump requires a challenger mixture.
9. **Minor decimal error:** at $r=1.6$, use preemption $0.064524$ to six decimals.
10. **Belief completion:** the IC-P fallback is undefined for $J>r$.
    Complete those beliefs or remove bids above the largest incumbent value.

## 5. What the original memo should change

Keep the selected benchmark results and the surplus derivation.
Describe IC-P as an extra belief completion.
Do not present it as a uniquely compelled refinement.
State the altered boundary tie next to each equilibrium claim.

Remove the claim that both refinements support silence pooling throughout Case C.
Restrict the claimed continuum of larger bids.
The benchmark does support a continuum through $\ell$.
Its alternative bid $J'=\ell$ gives entry $0.375$ and ownership $0.202807416$.
It also gives a strictly positive surplus gain.

Make selection dependence explicit in the plain summary.
At $c_H=5$, weak entry can equal $0.5625$ under another equilibrium.
The entry reversal therefore does not hold across all equilibrium selections.
At the information ceiling, the reserve-bid equilibrium also prevents a selection-free floor conclusion.

Retain analytical status for the conditional formulas.
Retain numerical diagnostic status for the regional search and the continuous-Laplace integral.
Do not promote grid coverage to an exhaustive equilibrium result.
Use the exact rational local certificate if a proved example of the new mixed branch is needed.

## 6. Plain summary

The selected model reproduces the main benchmark numbers.
Entry falls from 0.625 to 0.366988.
High-class ownership falls from 0.358422 to 0.197820.
Target proceeds fall by 0.171896, which the incumbent receives.
Selected surplus and challenger profit stay unchanged at the benchmark.

The proof for private lockups needs one extra incentive argument.
The claims about silence pooling and the full range of larger bids are too broad.
A binding bid can deter regardless of beliefs and defeat either claim.

The belief completion and equilibrium selection are substantive assumptions.
At the weak benchmark, another equilibrium gives entry 0.5625.
The reported increase from weak to strong competition therefore depends on selection.

The new mixed branches reproduce.
The two baseline memos agree once their distinct branches and challenger tie rules are explicit.
At the exact information ceiling, selected entry remains 0.297038499.
The floor starts strictly above that point.

The continuous-Laplace comparison also reproduces: entry falls from 0.522757 to 0.304840.
