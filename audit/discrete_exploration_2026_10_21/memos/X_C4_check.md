# X_C4. Independent check of sequential entry

## 1. Scope

This check concerns `C4_sequential.md` and the eight claims in the review brief.
The base is discrete-Laplace noise, buy-only orders, two challengers, and zero low preparation cost.
Claims 1–5 receive full derivations.
Claims 6–8 receive checks at the six benchmark points and a check of the stated cost window.
The broad scans receive a scope review, rather than a second complete scan.

The paper source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` in `overleaf/paper`.
Equation (4), Proposition 2, Section 6.1, and Appendix A.6 supply the relevant comparisons.
No mutable paper source enters this review.

The equilibrium concept is the memo's perfect Bayesian equilibrium with competitive prices.
The low-cost challenger prepares at every belief.
An indifferent challenger prepares in the main specification.
Investor mixtures are admissible at indifference; the selected pure outcome uses no purchase at a tie.
Equal auction bids pay the tied value; the winner rule does not affect the quantities below.

The belief rule retains the class posterior after the first decision, including an off-path decision.
This completion forms part of the result's scope.
Bayes' rule alone does not select beliefs at a decision with zero probability.

The independent calculation preceded access to the source scripts.
The first output was `scripts/X_C4_check/point_r3.jsonl`.
It already contained the reported benchmark prices, margins, entry, ownership, proceeds, and surplus.
The subsequent source comparison used read-only access and separate output files.

## 2. Verdict table

| Claim | Verdict | Evidence |
|---|---|---|
| 1. Auction objects and spread–rent identity | CONFIRMED | Exact auction integrals, both winner priorities, and the derivation in §3.1. |
| 2. Binary signals and posterior bounds | CONFIRMED | The likelihood factorization in §3.2 covers arbitrary state-dependent mixtures. |
| 3. No cascade under (NC) | CONFIRMED | The gain bound applies to every equilibrium under the stated belief completion; §3.3. |
| 4. Price and gain after entry | CONFIRMED | The stated sufficient conditions imply opposite price and gain orders; §3.4. |
| 5. Round-1 informed trade at every strength | CONFIRMED WITH CORRECTION | The order result holds under the displayed bound. General price sufficiency needs a separate argument; §3.5. |
| 6. Benchmark equilibria and numerical values | CONFIRMED | Independent interval enumeration at all six points; a separate argument covers every mixture and pooled price at $r=6/5$; §3.6. |
| 7. Entry across strengths and the cost window | CONFIRMED | The six entry values and the exact endpoint formulas reproduce; §3.7. |
| 8. Price access, proceeds, and net surplus | CONFIRMED WITH CORRECTION | Access weakly raises both quantities. Equality holds at two stated points; §3.8. |

The tie rule requires a separate correction in the broad scans.
Several mixed outcomes use challenger mixtures, which the main specification forbids.
This issue does not change the six benchmark outcomes.

## 3. Derivations and evidence

### 3.1 Claim 1: auction objects

**Status: analytical, with exact arithmetic for the stated examples.**

Write $\Delta=(r-\ell)^2/(2r)$ and $D=g_H-g_L$.
With two prepared challengers, the second-highest bid determines the payment.
The two challengers meet the reserve, even when the incumbent does not.

For one challenger, direct integration gives

$$
\begin{aligned}
t_0&=p\Pr(R\ge p)=p(1-p/r),\\
t_H&=\frac1r\left(\int_0^p p\,du+\int_p^r u\,du\right)
      =\frac r2+\frac{p^2}{2r},\\
t_L&=\frac1r\left(\int_0^p p\,du+\int_p^\ell u\,du+
                    \int_\ell^r\ell\,du\right)
      =\ell-\frac{\ell^2-p^2}{2r},\\
g_H&=h-t_H,\\
g_L&=\frac1r\left(\int_0^p(\ell-p)\,du+
                      \int_p^\ell(\ell-u)\,du\right)
      =\frac{\ell^2-p^2}{2r}.
\end{aligned}
$$

These formulas match equation (4) of the pinned paper.
For two challengers, the auction gives this table.

| State | Expected payment | Challenger 1 gain | Challenger 2 gain | Incumbent gain |
|---|---:|---:|---:|---:|
| $HH$ | $h$ | $0$ | $0$ | $0$ |
| $HL$ | $\ell+\Delta$ | $D$ | $0$ | $0$ |
| $LH$ | $\ell+\Delta$ | $0$ | $D$ | $0$ |
| $LL$ | $\ell$ | $0$ | $0$ | $\Delta$ |

For $HL$ and $LH$,

$$
\mathbb E\max(\ell,R)
=\ell+\frac1r\int_\ell^r(u-\ell)\,du
=\ell+\Delta.
$$

The high challenger keeps $h-\ell-\Delta$.
The same quantity equals the difference between the single-challenger gains:

$$
\begin{aligned}
g_H-g_L
&=h-\frac r2-\frac{p^2}{2r}-\frac{\ell^2-p^2}{2r}\\
&=h-\ell-\frac{r^2-2r\ell+\ell^2}{2r}
=h-\ell-\Delta=D.
\end{aligned}
$$

Equal challenger values imply zero challenger surplus when both prepare.
The payment remains the tied value under either winner priority.
The expected allocation value also remains the same.
Only the winner's identity can change.

Thus challenger 2 faces spreads $\Delta,\Delta,D$ against no first entrant, a low first entrant, and a high first entrant.
Its gain vectors are $(g_H,g_L)$, $(D,0)$, and $(0,0)$.
The table and the identity are correct.

`supplement.py` integrates each affine auction outcome over rational intervals.
It uses both challenger priorities at $r\in\{6/5,3,18/5\}$.
The exact differences in payment, surplus, and allocation are zero.
For example, at $r=3$, the two-challenger payments are $10,5/3,5/3,1$ and $D=25/3$.

### 3.2 Claim 2: binary signals and likelihood bounds

**Status: analytical.**

For $z\ge0$, the difference of two geometric counts has probability

$$
\sum_{m=0}^{\infty}(1-a)^2a^{z+2m}
=\frac{(1-a)^2a^z}{1-a^2}
=\frac{1-a}{1+a}a^z.
$$

Symmetry supplies negative $z$.
Let $\beta_s$ denote a purchase probability in state $s$.
Then

$$
\Pr(X=x\mid s)=n(x)
\begin{cases}
1+\beta_s(a^{-1}-1),&x\ge1,\\
1-\beta_s(1-a),&x\le0.
\end{cases}
$$

The common factor $n(x)$ cancels from Bayes' rule.
Thus the current flow posterior depends only on $S=\mathbf1\{X\ge1\}$.
The two signal probabilities are

$$
L_g(\beta)=\frac{a+(1-a)\beta}{1+a},\qquad
L_b(\beta)=\frac{1-(1-a)\beta}{1+a}.
$$

Each lies in $[a/(1+a),1/(1+a)]$.
Their ratio across any two states therefore lies in $[a,a^{-1}]$.
At the second date, the same bound applies conditional on each history.
The product bound is $[a^2,a^{-2}]$, even with history-dependent mixed orders.

For a fixed first flow, challenger 1 chooses from its price and an independent cost.
Its decision probability is therefore common across states at that flow.
That factor cancels from the state likelihood ratio.
The same conclusion holds with a price pool.

For any event $E$ with prior probability $\pi_E$, let $L_s$ denote the likelihood of the full record.
Then

$$
\Pr(E\mid\text{record})
\le\frac{\pi_E L_{\max}}
{\pi_E L_{\max}+(1-\pi_E)L_{\min}}
\le\frac{\pi_E}{\pi_E+a^2(1-\pi_E)}=\psi_2(\pi_E).
$$

The one-round formula replaces $a^2$ with $a$.
A posterior conditional on prices averages the flow posteriors.
The same bounds therefore apply to pooled prices.
The binary result concerns beliefs; continuation selection still requires an explicit strategy specification.

### 3.3 Claim 3: no cascade under (NC)

**Status: analytical.**

Fix a posterior $\nu$ over $(HH,HL,LH,LL)$.
Without challenger 1, challenger 2 earns

$$
\Gamma_2^0=g_L+D(\nu_{HH}+\nu_{LH}).
$$

With challenger 1, it earns

$$
\Gamma_2^1=D\nu_{LH}.
$$

The difference is $g_L+D\nu_{HH}>0$.
Thus a fixed experiment gives deterrence at every posterior.
This statement does not yet compare endogenous experiments.

The likelihood bound supplies that comparison under (NC):

$$
\Gamma_2^1
\le D\psi_2(\pi_{LH})<c_H.
$$

The high-cost challenger never prepares after $d_1=1$.
The low-cost challenger prepares because its gain is nonnegative.
Hence the conditional entry rate equals $\rho$, under every mixed order profile and every price partition.
After $d_1=0$, the low-cost challenger still prepares, so entry is at least $\rho$.

Consequently, where both conditional events have positive probability,

$$
\Pr(d_2=1\mid d_1=1)=\rho
\le\Pr(d_2=1\mid d_1=0),\qquad
\mathsf E_{12}=\rho\mathsf E_1.
$$

The same result holds at each first signal.
When $d_1=0$ is off path, use the stated counterfactual continuation rather than an undefined conditional probability.
The result includes challenger mixtures because (NC) is strict.
No investor best-response assumption enters the gain bound.

At $b=2$, $a^2=e^{-1}$.
The independent interval calculation gives these thresholds, rounded here to six decimals.

| $\kappa$ | $r=1.2$ | $r=3$ | $r=3.6$ |
|---|---:|---:|---:|
| $-0.5$ | 5.568875 | 5.165933 | 4.997179 |
| $0$ | 4.270379 | 3.961391 | 3.831985 |
| $0.5$ | 2.512711 | 2.330901 | 2.254758 |

Thus both costs satisfy (NC) at all six independent-class benchmark points.
At $\kappa=-0.5$, cost $5$ fails at the first two strengths and passes at the third.
Cost $5.8$ passes at all three strengths.
Failure of (NC) is failure of a sufficient condition, rather than evidence of a cascade.

For $\kappa\ge0$ and $b\ge2/\log3$, $\pi_{LH}\le1/4$ and $a^2\ge1/3$.
Therefore $\psi_2(\pi_{LH})\le1/(1+3a^2)\le1/2$.
The memo's corollary follows from $c_H>B_r(1/2)=g_L+D/2$.

### 3.4 Claim 4: price and gain orders in round 2

**Status: analytical under the proposition's stated sufficient conditions.**

Under (NC), entry after $d_1=1$ equals $\rho$ at both signals.
Let $v=V_{LL}=t_L+\rho g_L$.
The other values are

$$
V_{HL}=v+\Delta,\qquad
V_{LH}=v+\rho\Delta,\qquad
V_{HH}=v+\Delta+\rho D.
$$

Thus $LL$ never buys.
At every signal,

$$
V_{HH}-P_2\ge(1-\nu_{HH})\rho D
\ge(1-\psi_2(\pi_{HH}))\rho D.
$$

The displayed condition in C4.2 makes the $HH$ purchase strictly profitable.
For $LH$,

$$
V_{LH}-P_2
=-\nu_{HH}[(1-\rho)\Delta+\rho D]
 -\nu_{HL}(1-\rho)\Delta+\nu_{LL}\rho\Delta.
$$

Since $\nu_{HH}/\nu_{LL}\ge a^2\pi_{HH}/\pi_{LL}$, C4.2's third condition makes this residual negative.
Hence $LH$ and $LL$ do not buy; $HH$ buys; $HL$ may buy or mix.

The purchase probability of $LH$ is the smallest possible probability.
Bayes' rule then gives

$$
\Pr(LH\mid g)<\Pr(LH)<\Pr(LH\mid b).
$$

With fixed entry, each purchase margin equals $V_s-K$ for a common $K$.
Purchase probabilities therefore increase weakly with $V_s$.
The covariance between value and purchase probability is strictly positive because $HH$ buys and $LL$ does not.
For $\delta=(1-a)/(1+a)$ and $p_g=\Pr(g)$,

$$
P_2(g)-P_2(b)
=\frac{\delta\operatorname{Cov}(\beta_s,V_s)}{p_g(1-p_g)}>0.
$$

A higher price therefore reduces challenger 2's gain $D\Pr(LH\mid\cdot)$.
It also raises the posterior probability that challenger 1 is high-class.
This conclusion uses the additional sufficient conditions, rather than (NC) alone.

After $d_1=0$, a low-class state has residual
$-e_2\Delta\mu_2\le0$.
A high-class state has residual $e_2\Delta(1-\mu_2)$.
With a positive purchase probability, good news raises $\mu_2$, entry, and price.
If $\Delta<k$, the upper residual bound $\Delta$ instead implies no trade.
These are the price and gain orders in the paper.

For the Blackwell comparison, full high-class purchases give likelihood ratios $a^{-1}$ and $a$ about $j_2$.
Every other buy-only binary experiment has posteriors inside these endpoints.
Both posterior laws have the same mean at a fixed first history.
The full-purchase experiment therefore dominates; the inclusion is strict under C4.2's second and third conditions.

### 3.5 Claim 5: round-1 informed orders

**Status: analytical for the order result.**

Let $W_s^d$ denote the terminal payoff after first decision $d$.
Under (NC), $W_s^1=V_s$ from §3.4.
After $d_1=0$, the low class never buys in round 2.
The same-class selection rule equates the orders of the two high-class states.
Good news then induces weakly more preparation.

Let $\bar e_H\ge\bar e_L\ge\rho$ denote the resulting expected entry rates.
The continuation payoffs satisfy

$$
W_H^0-W_L^0
=\bar e_H(t_H-t_L)+(\bar e_H-\bar e_L)(t_L-t_0)\ge0.
$$

Here $t_L-t_0>0$.
Thus $W^0$ is largest for $j_2=H$ and smallest for $j_2=L$.
At a fixed first signal, write

$$
Y_s=e_1V_s+(1-e_1)W_s^0.
$$

The value $Y_{LL}$ is minimal, so $LL$ never buys.
For every $s\ne HH$,

$$
Y_{HH}-Y_s
\ge e_1(V_{HH}-V_s)
\ge\rho^2D.
$$

Therefore the $HH$ purchase margin has the lower bound

$$
M_{HH}\ge\rho^2(1-\psi_1(\pi_{HH}))D-k.
$$

The memo's sufficient inequality makes $HH$ buy with probability one.
At the three independent-class strengths, the gross bounds are $0.362331$, $0.336114$, and $0.325134$.
Each exceeds $k=0.02$.
This reproduces the loss of the paper's weak-incumbent no-trade outcome.

The benchmark conclusion also covers every $1<r<10$.
On this interval, $D$ decreases from $9$ to $99/20$.
The gross bound is therefore at least $0.1996516775>0.02$.
Also, $D\psi_2(1/4)<9/(1+3e^{-1})<5$, so (NC) holds throughout.

One wording correction remains.
Different orders imply an informative flow; they do not alone prove that the first price reveals that flow signal.
The proof in C4.3 establishes the order result, but omits a general exclusion of pooled first prices.
Retain the order result as analytical.
State price separation separately where it is proved or certified.
At the six benchmark points, the calculation certifies distinct first prices.

### 3.6 Claim 6: benchmark equilibria and full payoff accounting

**Status: computer-assisted for the six pure outcomes and for uniqueness at $r=6/5$.**

The independent calculation uses exact rational primitives and an interval enclosure of $a=e^{-1/2}$.
For each point, it forms all 16 pure first order profiles.
Each profile gives two first posteriors and two first decisions, hence 64 continuation subgames.
Each continuation has 16 order profiles and four high-cost entry patterns.
It also examines the 14 informative order profiles under a common pooled price.

Every one of the 64 subgames has one certified pure continuation at each benchmark point.
Every remaining pure candidate fails a strict inequality.
The separate pooled-price calculation leaves no unresolved continuation.
The backward calculation gives exactly one pure equilibrium with distinct first prices.
This matches the scope of C4.4(i), which excludes pooled first prices at the stronger incumbents.

The payoff calculation includes both later entry decisions.
For a second-round candidate, let $L_2(z\mid s)$ denote its signal probability and $e_2(z)$ its entry rate.
The continuation values are

$$
\begin{aligned}
W_s^1&=\sum_z L_2(z\mid s)
 [t_{j_1}+e_2(z)(T_s-t_{j_1})],\\
W_s^0&=\sum_z L_2(z\mid s)
 [t_0+e_2(z)(t_{j_2}-t_0)],\\
\Gamma_1&=\sum_s\mu_1(s)\sum_zL_2(z\mid s)
 [(1-e_2(z))g_{j_1}+e_2(z)D\mathbf1\{s=HL\}].
\end{aligned}
$$

The first investor therefore uses

$$
M_{1s}
=\frac{Y_s(g)-P_1(g)}{1+a}
 +\frac{a[Y_s(b)-P_1(b)]}{1+a}-k,
\qquad
Y_s(y)=e_1(y)W_s^1(y)+(1-e_1(y))W_s^0(y).
$$

This formula accounts for challenger 2's later entry in investor 1's payoff.
The source scripts use the same terminal payoff.
They also condition the second price on $d_1$.
Neither incentive error in the review brief occurs at the benchmark.

At $r=3$, $c_H=5$, $\kappa=0$, the independent result is:

| Quantity | Value |
|---|---:|
| $\mathsf E_1$ | 0.250000000000 |
| $\mathsf E_2$ | 0.377621862493 |
| $\Pr(d_2=1\mid d_1=0)$ | 0.420162483324 |
| $\mathsf E_{12}$ | 0.062500000000 |
| High-class owner | 0.321908343450 |
| Proceeds | 1.028307249276 |
| Allocation value | 4.258636583438 |
| Preparation cost | 0.638109312465 |
| Net surplus | 3.620527270973 |
| Trade cost | 0.013750000000 |

The first purchase margins, in state order $(HH,HL,LH,LL)$, are

$$
(0.561434975502,\;-0.268998222178,\;-0.084398357831,\;-0.435664888844).
$$

The first prices are $1.251176540329$ and $0.854067647637$.
The second-round objects also reproduce:

| First signal, decision | Second buyers | Second prices, good / bad | Second gain, good / bad |
|---|---|---|---|
| $g,1$ | $HH$ | 2.359240 / 1.802083 | 1.457314 / 2.083333 |
| $g,0$ | $HH,LH$ | 1.332254 / 0.605492 | 5.840671 / 3.837087 |
| $b,1$ | $HH$ | 1.802083 / 1.454073 | 2.083333 / 2.474356 |
| $b,0$ | $HH,LH$ | 0.626212 / 0.585850 | 4.873118 / 2.854981 |

#### A separate uniqueness argument at $r=6/5$

At this strength, $\Delta=1/60<k$.
Thus no second investor trades after $d_1=0$.
After $d_1=1$, the sufficient bounds fix $HH$ purchases and rule out $LH$ and $LL$ purchases.
For $HL$, let $m_2=a^2/(a^2+3)$.
Its purchase margin is at most

$$
(1-m_2)\Delta-m_2\rho D-k<-0.2504702187.
$$

Only $HH$ therefore buys after the first entry.
The first investor's $HH$ type buys and its $LL$ type does not, by §3.5.
Only the first purchase probabilities of $HL$ and $LH$ remain possible mixtures.

Let $m_1=a/(a+3)$, the lower posterior bound for $HH$ after one round.
For either middle state $s\in\{HL,LH\}$, $Y_s-Y_{HH}\le-\rho^2D$.
For every other state $u\ne HH$, $Y_s-Y_u\le\Delta$.
The latter bound follows because both continuation payoff spreads between these states are at most $\Delta$.
It holds for all entry rates in $[\rho,1]$ and includes pooled prices.

Consequently, at either first signal,

$$
Y_s-P_1\le(1-m_1)\Delta-m_1\rho^2D,
\qquad
M_{1s}\le(1-m_1)\Delta-m_1\rho^2D-k
<-0.1005598844.
$$

Thus neither middle state can mix.
Only $HH$ buys in round 1.
If the first price pooled the signals, both entry rates would be constant across those signals.
The resulting terminal values would be constant across signals, with $HH$ strictly maximal.
The posterior tilt toward $HH$ would then imply distinct first prices, a contradiction.

The first prices therefore separate.
The remaining entry decisions are strict at both costs.
This proves uniqueness over all mixtures and pooled prices at $r=6/5$.
The interval bounds in `supplement.jsonl` enclose the stated signs.
This argument does not infer completeness from a finite mesh of mixtures.

The source certificate and weak-incumbent calculation were then rerun through their real command interfaces.
Their outputs agree with their saved outputs and the independently derived outcomes.
The stronger-incumbent claim of uniqueness over all mixtures remains a numerical diagnostic, as the memo states.

### 3.7 Claim 7: strength comparisons and the cost window

**Status: computer-assisted at the six benchmark points; analytical endpoint formulas on the stated branch.**

Only $HH$ buys in round 1 at these points.
For independent classes, the first good posterior is

$$
\mu_g=(1,a,a,a)/(1+3a),\qquad
\Pr(g)=\frac{1+3a}{4(1+a)}.
$$

The second high-class posterior after two good signals and no first entry is

$$
\mu_{gg}(j_2=H)=\frac{1+a}{1+a+2a^2}.
$$

Hence the two cost endpoints are

$$
\begin{aligned}
c_-&=B_{18/5}\!\left(\frac{1+a}{1+a+2a^2}\right)
 =5.633125370886170741\ldots,\\
c_+&=B_3\!\left(\frac{1+a}{1+a+2a^2}\right)
 =5.840670610840286776\ldots.
\end{aligned}
$$

The endpoint signs require $(c_-,c_+]$ under preparation at indifference.
The lower endpoint must be open because the expensive challenger still prepares at $r=3.6$ there.
The upper endpoint remains closed because it prepares at $r=3$ there.
The displayed rounded window is therefore correct.

The independent calculation gives:

| Cost | $\mathsf E_2(1.2)$ | $\mathsf E_2(3)$ | $\mathsf E_2(3.6)$ |
|---|---:|---:|---:|
| $5$ | 0.496808313099 | 0.377621862493 | 0.377621862493 |
| $29/5$ | 0.250000000000 | 0.377621862493 | 0.250000000000 |

At cost $5$, entry at the weak incumbent follows first good news alone.
At $r=3$, it requires two good signals and no first entry.
At cost $5.8$, only the middle strength recruits expensive preparation.
The headline comparisons hold.

The lower-cost rows with challenger mixtures require the separate tie rule discussed in §4.
This check does not certify all mixtures throughout every cost interval.

### 3.8 Claim 8: access to prices and welfare

**Status: analytical on the stated branch, with numerical values at the six points.**

At the six points, the first entry rate equals $\rho$ with or without price access.
Without access, the second entry rate also equals $\rho$.
With access, the only additional preparation occurs after $d_1=0$.
Thus price access does not remove any preparation on this branch.

For either challenger class $j$, let $A_j$ denote allocation value with that challenger alone.
Let $A_0=(r^2-p^2)/(2r)$.
Direct substitution gives

$$
\begin{aligned}
A_H-A_0-g_H
&=h-\frac{r^2-p^2}{2r}-h+\frac r2+\frac{p^2}{2r}
=\frac{p^2}{r},\\
A_L-A_0-g_L
&=\ell+\Delta-\frac{r^2-p^2}{2r}
-\frac{\ell^2-p^2}{2r}
=\frac{p^2}{r}.
\end{aligned}
$$

At any additional preparation event $I$, conditional expected net surplus therefore rises by

$$
B_r(\mu_I)-c_H+\frac{p^2}{r}>0.
$$

The entry condition supplies the weak inequality for the first two terms.
The last term makes the result strict whenever additional preparation has positive probability.
Proceeds also rise because $t_j-t_0>0$ in both classes.

The independent comparison gives these differences, visible prices minus hidden prices:

| Cost | $r$ | Proceeds difference | Net surplus difference |
|---|---:|---:|---:|
| $5$ | 1.2 | 0.100038707269 | 0.157785680909 |
| $5$ | 3 | 0.116848915943 | 0.117923104306 |
| $5$ | 3.6 | 0.141563700149 | 0.089663268364 |
| $29/5$ | 1.2 | 0 exactly | 0 exactly |
| $29/5$ | 3 | 0.116848915943 | 0.015825614312 |
| $29/5$ | 3.6 | 0 exactly | 0 exactly |

Thus the blanket statement of strict gains in every stated case is false.
The correct statement is weak gains throughout, with strict gains when prices recruit expensive preparation.
The positive comparisons at cost $5$ are correct.
Net surplus excludes trade costs, consistent with the memo's definition.
The hidden-price trade game remains unsolved here, so no comparison of surplus inclusive of those costs follows.

### 3.9 Late scan and evidence scope

**Status: numerical diagnostic for the scan; open for unproved existence claims.**

The memo changed during this review.
The final source read and its hash appear in `scripts/X_C4_check/receipt.json`.
The review covers the late addition to Result 9 at negative correlation.

At $\kappa=-1/2$, $r=18/5$, and $c_H\in\{43/10,22/5\}$, the independent calculation finds no equilibrium with pure play in both rounds.
At either cost, six of the 64 continuation subgames have no pure equilibrium.
Therefore this pure enumeration cannot establish nonexistence of a mixed equilibrium.
The broader scan can omit several simultaneous mixtures.
An empty search result must remain a documented failure, with existence open.

The final source read includes a new paragraph about $c_H=4.4$ in Result 9, item 9.
It reports an empty broad search, an incomplete finer run, and open existence.
That label is appropriate.
The paragraph names two omitted classes: two simultaneous investor mixtures, and a challenger-1 tie combined with a cross-round tie.
The source does not report a completed late broad scan at $c_H=4.3$.
No claim about existence or nonexistence at that point follows from the review's empty pure calculation.

### 3.10 Files, arithmetic, and reproduction

All files below lie under `scripts/X_C4_check/`.

| File | Content |
|---|---|
| `review.py` | Independent backward calculation, posterior bounds, and threshold formulas. |
| `supplement.py` | Exact auction integrals, a uniform weak-incumbent bound, cost endpoints, and price-access comparisons. |
| `point_r3.jsonl` | Independent benchmark result before source-code access. |
| `benchmarks_interval.jsonl` | Six point enclosures, all pure candidates, and the separate second-price pool calculation. |
| `bounds_interval.jsonl` | (NC), purchase bounds, and no-purchase bounds. |
| `thresholds.jsonl` | Closed-form gains and cost endpoints. |
| `supplement.jsonl` | Auction values, weak-incumbent signs, and welfare comparisons. |
| `late_43_pure.jsonl`, `late_44_pure.jsonl` | Independent pure calculations at the two late points. |
| `source_certify_output.txt`, `source_unique_r0_output.txt` | Fresh source-script outputs after the independent calculation. |
| `receipt.json` | Source hashes, output hashes, and the final source read. |

The rational inputs remain exact until interval conversion.
The exponential and every arithmetic operation in the certificate use outward intervals.
The interval precision is 45 decimal places.
The accepted and excluded candidates use strict interval signs, rather than rounded display values.
Floating-point summary values only describe the certified results.

Consumer commands from the repository root are:

```bash
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python -B audit/discrete_exploration_2026_10_21/scripts/X_C4_check/review.py benchmarks --interval
bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python -B audit/discrete_exploration_2026_10_21/scripts/X_C4_check/supplement.py
.venv/bin/python -B audit/discrete_exploration_2026_10_21/scripts/X_C4_check/review.py bounds
.venv/bin/python -B audit/discrete_exploration_2026_10_21/scripts/X_C4_check/review.py thresholds
```

The programs received the real economic inputs above.
Their printed outputs supplied the numerical evidence in this memo.
No test suite or assertion script entered the review.

### 3.11 Status labels

| Source item | Label assessment |
|---|---|
| Results 1–4 and Lemma 1 | The analytical labels are justified under the stated setup and belief completion. |
| Result 5 | The analytical label is justified with its additional sufficient conditions. |
| Result 6 | The order theorem is analytical. The general price claim requires the correction in §3.5. |
| Result 7 | The computer-assisted label is justified for the stated pure scope and for all mixtures at $r=1.2$. |
| Result 8 | The two marked costs have certificates. The wider equilibrium windows remain numerical diagnostics. |
| Result 9 | The scan is a numerical diagnostic. C4.5 remains a conjecture. The late existence question remains open. |
| Result 10 | The numerical label and conditional analytical step are justified after the strictness correction. |

## 4. Errors found and corrections

1. **Tie-rule mismatch in the broad scans.** The main specification requires preparation at indifference.
   The numerical correspondence also admits partial preparation at a tie.
   Those outcomes require a changed tie rule.
   They cannot establish equilibrium existence under the stated main rule.

2. **Strict welfare claim.** At $c_H=5.8$, price access changes neither proceeds nor net surplus at $r=1.2$ or $r=3.6$.
   Replace the blanket strict statement with the weak comparison in §3.8.

3. **Trade versus price sufficiency.** C4.3's proof establishes different orders across states.
   It does not supply a general exclusion of pooled first prices.
   Retain the trade result and qualify the additional price conclusion.
   The six benchmark prices do separate.

4. **Off-path conditioning.** An ordinary conditional probability on $d_1=0$ requires positive probability for that event.
   Otherwise, name the prescribed counterfactual continuation.
   The no-cascade proof already works with that completion.

5. **Auction wording.** The incumbent value can fall below $\ell$ and below $p$.
   Result 1 should say that both challengers meet the reserve.
   Also replace “same-class first entrant maximizes the spread” with “high-class first entrant maximizes the spread.”

No error appears in the benchmark terminal payoff, the first decision's class information, or the treatment of auction ties.
The benchmark numbers match the source outputs to their reported precision.

## 5. What the original memo should change

- Keep the auction formulas, likelihood bounds, and no-cascade proposition.
- Retain the sufficient conditions beside each claim about all equilibria.
- State the off-path belief completion beside the no-cascade proposition.
- Restrict C4.3's analytical conclusion to informed orders unless a separate price argument is supplied.
- Keep the pure uniqueness certificate at all six points.
- Keep uniqueness over all mixtures at $r=1.2$; retain the numerical label at stronger incumbents.
- Separate the main challenger tie rule from the correspondence that permits challenger mixtures.
- State weak welfare gains, with strict gains when prices recruit additional preparation.
- Keep the late empty scan as a failure of the declared search, with existence open.

## 6. Plain summary

The main economic results pass the independent check.
The auction gives the stated spread–rent identity.
The likelihood bound covers arbitrary mixed orders and pooled prices.
Under (NC), the expensive second challenger never prepares after the first prepares.
Thus no entry cascade occurs within the stated belief rule.

The price and gain orders reverse after a first entry under the stated sufficient conditions.
Round-1 informed purchases occur at every benchmark strength.
The general price-sufficiency claim needs a separate argument.

All six benchmark outcomes reproduce.
A separate argument also proves uniqueness over all mixtures and pooled prices at the weak incumbent.
The reported entry reversal and the rise-then-fall cost window are correct.

Two corrections matter for interpretation.
The broad scans sometimes change the challenger tie rule.
Price access gives weak welfare gains; two stated cases give equality.
The negative-correlation empty scan leaves existence open.
