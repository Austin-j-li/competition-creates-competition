# XP5: independent check of the empirical implications

Date: 23 October 2026. Scope: R11, P5 Propositions 1–9 and all 112 registry rows.

**Verdict: corrected.** All 112 numbers agree at their display precision. Several statements require correction before transfer to the manuscript.

The spread decomposition, its 90.2% entry share, the identification formula, the winner gap, and the announcement values are confirmed.
The exact full-order bound is also confirmed.
The literal interval with the rounded lower endpoint is refuted.
The strict rise of the entry component above the ceiling is refuted.

## 1. Evidence and reproduction

The independent files are:

- `scripts/XP5/recompute.py`: independent reconstruction from the auction cash flows and the slot probabilities.
- `scripts/XP5/run_log.txt`: interval values, fixed-candidate payoffs, corrections, source hashes, and software versions.
- `scripts/XP5/registry_recompute.csv`: one comparison row for each P5 registry row.
- `memos/XP5_check.md`: this check.

Run the program from the repository root:

```bash
.venv/bin/python audit/slot_manuscript_2026_10_23/scripts/XP5/recompute.py > audit/slot_manuscript_2026_10_23/scripts/XP5/run_log.txt
```

The program ran through this CLI with the exact calibration B inputs.
It printed 112 confirmed rows and zero differences at display precision.
It used no assertions and no test suite.
It did not import or execute the P5 script.
It wrote only inside `scripts/XP5/`.

The certificate uses an exact Taylor bound for the exponential constant.
For $N=120$, let

\[
S_N=\sum_{n=0}^{N}\frac1{n!},\qquad
0<e-S_N<\frac{1}{(N+1)!}\frac{1}{1-1/(N+2)}.
\]

The tail bound follows from the upper bound $1/(N+2)$ on successive tail ratios.
The program lifts these rational bounds into 90-digit interval arithmetic.
The decimal input is exactly $\beta=294655/10^6$.
No binary float enters a numerical certificate.
Every display comparison uses both interval endpoints, with a separate percentage scale where required.

The reviewed snapshot has these hashes:

| Source | SHA-256 |
|---|---|
| `proofs/P5_observables.tex` | `00b6f168a35a68e8d37b572f30faf8b902a0a7775d1de953dde8ad7c3f41cb85` |
| `registry/P5_observables.csv` | `d12831139e4dfc49c7a964ace4ed6577672953e592cc96ed347fddc13070cdd7` |
| `scripts/P5_observables/p5_observables.py` | `ed870c1633775241db1ecdeabe8b6433d0505e3341b9316465eb24d44b571e3d` |

The log records the other source hashes.
Each source hash stayed unchanged through the run.
The existing P5 build log records a 15-page PDF.
This check did not rebuild or alter that package.

## 2. Independent foundation

### Auction cash flows: confirmed, analytical

The pinned manuscript's equation (4) and Appendix equation OA.5 agree with the shared objects.
Direct integration gives

\[
\begin{aligned}
t_0&=\frac1r\int_p^r p\,dR=p(1-p/r),\\
t_H&=\frac{p^2}{r}+\frac1r\int_p^r R\,dR
     =\frac r2+\frac{p^2}{2r},\\
t_L&=\frac{p^2}{r}+\frac1r\int_p^\ell R\,dR
       +\frac1r\int_\ell^r\ell\,dR
     =\ell-\frac{\ell^2-p^2}{2r},\\
g_L&=\frac{p(\ell-p)}r+\frac1r\int_p^\ell(\ell-R)\,dR
     =\frac{\ell^2-p^2}{2r},\\
g_H&=h-t_H,\qquad
\Delta=t_H-t_L=\frac{(r-\ell)^2}{2r}.
\end{aligned}
\]

Thus there is no discrepancy with the pinned source.
At the fixed auction primitives,

\[
A_r(\mu)=\frac12-\frac1{8r}+\Delta(r)\mu>0,
\quad \Delta'(r)=\frac12-\frac1{2r^2}>0,
\quad B_r(1/2)=5-\frac r4+\frac1{8r}<6.
\]

Both class rents fall strictly with $r$, so $B_r(\mu)$ falls for every belief $0\le\mu\le1$.
Its slope in the belief is $g_H-g_L=10-r/2-1/(2r)>0$.
The ceiling equation has the stated root when $M>5/8$.

### Price sufficiency: confirmed, analytical; add this step to P5

The challenger observes the price, so its posterior first requires a check at each price preimage.
Let $e_x$ denote the entry probability at the price after order $x$.
Independence of the cost and the class gives

\[
E[V_T\mid j,x]=t_0+e_x(t_j-t_0),\qquad
P(x)=t_0+e_x[A_r(\mu_x)].
\]

If $P(x)=P(y)$, the challenger uses the same entry probability after both orders.
Call this probability $e\ge\rho>0$.
Subtract the two price equations:

\[
0=e\Delta(\mu_x-\mu_y).
\]

Hence $\mu_x=\mu_y$.
The posterior at that price equals this common posterior.
The challenger can therefore use $B_r(\mu_x)$ at every price, even when prices pool orders.

P5 directly checks distinct prices in U and F, so its existence proof does not depend on this omitted step.
The step completes its treatment of arbitrary candidates.
The reviewed P1 already states this argument in its price lemma.
P1's later result sections remain marked open in the reviewed snapshot.
No result below requires those unfinished sections.

### Bounds and deviations: confirmed, analytical

Write $c_x=(1-\lambda)\eta_x$.
For each class, $c_x\le a_j(x)\le c_x+\lambda$.
Since $\beta\le1/3$, every $c_x\ge b$.
Thus the class likelihood ratio lies between $1/(1+u)$ and $1+u$.
At prior $1/2$, Bayes' rule gives $m\le\mu_x\le M$ under every strategy pair.

At the fixed candidate price and entry schedule, subtraction gives

\[
\begin{array}{lll}
U_H(1)=e_1\Delta(1-\mu_1)-k,&U_H(0)=0,&
U_H(-1)=-e_{-1}\Delta(1-\mu_{-1})-k,\\
U_L(-1)=e_{-1}\Delta\mu_{-1}-k,&U_L(0)=0,&
U_L(1)=-e_1\Delta\mu_1-k.
\end{array}
\]

Both wrong-sign orders lose strictly.
These formulas hold the price function and the entry rule fixed.
They do not replace the candidate posterior after a deviation.

### Explicit tuples and conditions

The following tuples independently reproduce P5's outcomes.
All vectors use the order $(-1,0,1)$.
Let $J=\mathbf1\{B_r(M)\ge6\}$, $e_+=\rho+(1-\rho)J$, and

\[
z=\frac{1-2b-\lambda}{2-4b-\lambda}.
\]

| Object | N | U | F |
|---|---|---|---|
| $(\sigma_H,\sigma_L)$ | $(\delta_0,\delta_0)$ | $(\delta_1,\delta_0)$ | $(\delta_1,\delta_{-1})$ |
| Beliefs | $(1/2,1/2,1/2)$ | $(1/2,z,M)$ | $(m,1/2,M)$ |
| Entry | $(\rho,\rho,\rho)$ | $(\rho,\rho,e_+)$ | $(\rho,\rho,e_+)$ |
| Prices | $t_0+\rho A_r(1/2)$, all orders | $t_0+(\rho A_r(1/2),\rho A_r(z),e_+A_r(M))$ | $t_0+(\rho A_r(m),\rho A_r(1/2),e_+A_r(M))$ |
| Bids | Incumbent $R$; prepared challenger $\ell$ or $h$ | Same bids | Same bids |

The five economic conditions are Bayes consistency, competitive prices, optimal entry, optimal investor orders, and truthful bids.
The price-preimage check above supplies the challenger's information condition.
The order probabilities below verify Bayes consistency directly.
The class cash flows verify competitive prices directly.
The inequalities below verify entry and investor choices against each fixed tuple.
Truthful bids are weakly dominant under the stated second-price auction.

## 3. Verdict for every proposition

### Proposition 1: confirmed, analytical; numeric bound computer-assisted

If $\Delta<k$, every correct-order payoff is at most $\Delta-k<0$.
The wrong-sign payoffs are negative, and abstention pays zero.
Both classes therefore abstain under every candidate.
The resulting posterior is $1/2$, which gives entry $\rho$.
This proves existence and uniqueness of N without a circular step.

For every candidate, the correct-order payoffs satisfy

\[
U_H(1)\ge\rho\Delta m-k,\qquad
U_L(-1)\ge\rho\Delta m-k.
\]

When this common lower bound is positive, both classes strictly choose their correct full orders.
Bayes' rule then forces the F beliefs and its order probabilities.
Its prices satisfy $P(-1)<P(0)<P(1)$.
The challenger therefore infers the order and uses exactly the stated entry rule.
This proves existence and uniqueness through bounds on every profile.
The same bounds apply when the price is hidden and entry stays at $\rho$.

For U with $r_F<r<r_N$ and $r\le r_C$, the four relevant payoffs are

\[
U_H(1)=\Delta m-k>0,quad U_H(0)=0,
\quad U_L(-1)=\rho\Delta/2-k<0,quad U_L(0)=0.
\]

Wrong-sign deviations lose strictly.
The non-buy posteriors stay below the entry threshold.
The buy posterior is $M$, so the buy recruits under the declared challenger rule.
For N, either correct-order deviation pays $\rho\Delta/2-k$.
Thus N also exists for $r\le r_N$, under the declared investor rule.

**Endpoint correction, analytical and computer-assisted.** The exact bound is

\[
r_S=2.1241481328154506735390194153101386039\ldots.
\]

Use $r\in(r_S,10)$, with $r_S\approx2.124148$, or the sufficient interval $(2.124149,10)$.
The literal claim “unique on $(2.124148,10)$” is false.
At $r=2.1241481$, which lies inside that printed interval,

\[
\rho\Delta(r)m-k
\in[-8.586805804831898\times10^{-10},-8.586805804831897\times10^{-10}].
\]

The low class strictly prefers abstention to the full sale in F there.
The registry value `rS_p5_B` is correctly rounded; the interval wording is the error.

### Proposition 2: confirmed, analytical; values computer-assisted

Let $s=\lambda\Pr(q=1\mid H,I)$ and $t=\lambda\Pr(q=-1\mid L,I)$.
Direct class averaging gives

\[
D_+=b+s/2,\quad D_-=b+t/2,\quad
v=2b+(s+t)/2,\quad E[X]=(s-t)/2.
\]

The actual informed trade probability is $(s+t)/2$.
Its share of nonzero orders is therefore $(s+t)/(4b+s+t)$.
Set $(s,t)$ equal to $(0,0)$, $(\lambda,0)$, and $(\lambda,\lambda)$.
This gives every table entry and every comparison in Proposition 2.
The U share equals $E[X]/v=u/(4+u)$, below the F share $u/(2+u)$.
The F order law and posterior vector contain no $r$.

These signatures distinguish the three stated tuples at fixed slot parameters.
They do not classify an arbitrary mixture of processes with different parameters or equilibria.

### Proposition 3: corrected; identities analytical, values computer-assisted

Subtract the F prices in the explicit tuple:

\[
\begin{aligned}
S&=\rho\Delta(M-m)+(1-\rho)J A_r(M)
   =\rho\Delta\vartheta+(1-\rho)J A_r(M),\\
I_-&=\rho\Delta(1/2-m)=\rho\Delta\vartheta/2,\\
I_+&=\rho\Delta(M-1/2)+(1-\rho)J A_r(M)
    =I_-+(1-\rho)J A_r(M).
\end{aligned}
\]

These identities and parts (i)–(iv) are exact.
At $r_1$, the independent values are

\[
S=0.78629881552500406604\ldots,\qquad
S_{\rm entry}=0.70927928931500243963\ldots,
\]
\[
S_{\rm entry}/S=0.90204801954511855852\ldots.
\]

Thus the displayed **90.2%** is correct.

**Part (v) is refuted as written.** Above $r_C$, $J=0$, so the entry component is identically zero.
Its derivative is zero there.
The class component, both impacts, and the total spread still rise strictly.
Below the ceiling, both spread components rise strictly.
Replace “all increase strictly” with these two separate statements.

For part (vi), a ceiling inside the F interval requires $r_S<r_C<10$.
The benchmark satisfies this condition with margin $r_C-r_S=1.468510385979211\ldots$.
At the ceiling, the declared challenger rule sets $J=1$.
The right limit sets $J=0$.
Their difference is exactly $(1-\rho)A_{r_C}(M)$.
Only the buy price changes discontinuously; its probability is (d).
The mean price change is therefore $-(1-\rho)dA_{r_C}(M)$.
All registered jump values are correct.

### Proposition 4: corrected scope; identification analytical, values computer-assisted

On F, the order law is $(v/2,1-v,v/2)$.
For given (v) and $u'>0$, solve $v=\lambda'+2b'$ and $u'=\lambda'/b'$:

\[
b'=\frac{v}{u'+2},\qquad
\lambda'=\frac{vu'}{u'+2},\qquad
\beta'=\frac{v}{2+u'(1-v)}.
\]

The liquidity condition is $3v\le2+u'(1-v)$.
This proves the algebraic range in part (a).
It is a range of full-order **laws**, before investor optimality.

**Correct the unrestricted equilibrium interpretation at lines 507–515.**
The asserted range $[0.250299\ldots,1)$ includes pairs for which F is not an equilibrium at $r_1$.
For any full-order pair, the low-class sale payoff at $r_1$ is

\[
\rho\Delta(r_1)\frac{1-\vartheta'}2-k.
\]

It is nonnegative only when $\vartheta'\le0.76$.
For strict incentives, require $\vartheta'<0.76$.
At $\vartheta'=0.9$, the same counts give $\beta'=0.105296314876202\ldots<1/3$.
Yet the low-class sale payoff is exactly $-7/600$.
Thus this pair cannot produce those counts through an F equilibrium.
At $r_2$, the corresponding upper bound is $701/845=0.829585798816568\ldots$.
Non-identification remains true after these restrictions.

For part (c), strict recruitment and non-recruitment imply

\[
\tau(r_1)<M'<\tau(r_2)
\quad\Longleftrightarrow\quad
0.41<\vartheta'<\frac{1343}{2902}.
\]

The upper bound is $0.462784286698828\ldots$.
The condition $v\le200/259$ ensures $\beta'\le1/3$ throughout this band.
Every pair in this band also satisfies strict full-order incentives at both benchmark strengths.
For example, the weakest bound at $r_1$ exceeds

\[
\rho\Delta(r_1)[1-\tau(r_2)]-k>0.0247.
\]

This fills the omitted equilibrium check for the alternative pairs.
The registered example $u'=8/5$ is admissible and has the claimed prices and entry.

The core identification in part (d) is confirmed:

\[
\rho=\Pr(A\mid X\ne1),\quad
\vartheta=\frac{2I_-}{\rho\Delta(r)},\quad
\lambda=v\vartheta,\quad
\beta=\frac{v(1-\vartheta)}{2(1-v\vartheta)},\quad
u=\frac{2\vartheta}{1-\vartheta}.
\]

Both the sale and neutral order have entry $\rho$, which establishes the first two equalities.
The remaining equalities follow from $v=\lambda+2b$ and $b=(1-\lambda)\beta$.
The independent reconstruction errors lie inside $3\times10^{-89}$.
The inputs include $\rho$, or its non-buy entry estimate, and the auction object $\Delta$.
“Sell impact and volume identify” must retain these maintained inputs.

For U, $E[X]=\lambda/2$ and $v=2b+\lambda/2$.
Hence $\lambda=2E[X]$, $b=(v-E[X])/2$, and its informed share is $E[X]/v$.
The formula $\beta=b/(1-\lambda)$ completes slot identification there.

### Proposition 5: confirmed, analytical; values computer-assisted

In U and F, only a buy can recruit the high-cost challenger.
The buy frequency in either tuple is $d=b+\lambda/2$.
Thus

\[
\Pr(A)=\rho+(1-\rho)Jd,\qquad
\Pr(A\mid X=1)-\Pr(A\mid X\ne1)=(1-\rho)J.
\]

If H buys fully, let L sell with total informed mass $t\in[0,\lambda]$.
Then $\mu_{-1}=b/(2b+t)\le1/2$, $\mu_0\le1/2$, and $\mu_1=M$.
Only the buy recruits whenever $J=1$, regardless of $t$.
This verifies part (iv) without a conclusion about the low-class mixture.

With a hidden price, the challenger's posterior stays at the prior.
Since $B_r(1/2)<6$, entry equals $\rho$ at every strength and every order profile.
This is stronger than the stated restriction to N and F.
The derivatives $\partial d/\partial\lambda=1/2-\beta>0$ and $\partial d/\partial\beta=1-\lambda>0$ verify part (vi).
These derivatives hold within a region where the recruitment indicator stays fixed.

At B, the plateau is $0.52275694347840667171\ldots$, and the floor is $1/4$.
For the U plateau, retain the existence condition $r\le r_C$ from Proposition 1.
It is automatic on the stated coexistence interval within the strict benchmark parameter band.

### Proposition 6: confirmed, analytical; values computer-assisted

The four stated hypotheses imply N at $r_0$ and F at both $r_1$ and $r_2$.
The F incentive bound at $r_2$ follows from $\Delta(r_2)>\Delta(r_1)$.
The entry indicators are respectively irrelevant in N, one at $r_1$, and zero at $r_2$.
Thus the entry rise is $(1-\rho)d>0$, and entry returns to $\rho$ at $r_2$.
The hidden-price comparison has entry $\rho$ throughout.
The F posteriors and order law stay unchanged between the latter strengths.

The winner prediction follows from the independent derivation for Proposition 7 below.
The sell impact at $r_2$ stays positive because $\rho\Delta\vartheta/2>0$.
All hypotheses have positive benchmark margins in Section 4.

### Proposition 7: confirmed, analytical; values computer-assisted

Conditional on the order, preparation depends only on the independent cost.
It therefore leaves the class posterior unchanged.
A prepared H challenger wins with probability one.
A prepared L challenger wins with probability $\ell/r$.
Consequently,

\[
w_x=\Pr(W\mid X=x,A)=\mu_x+(1-\mu_x)\ell/r,
\quad\Pr(W\mid X=x)=e_xw_x.
\]

The first expression increases strictly with $\mu_x$, since $r>\ell$.
U and F prices have the same strict order as their posteriors.
This proves the conditional price prediction.

In F, subtract the buy and sale expressions:

\[
w_1-w_{-1}=(M-m)(1-\ell/r)=\vartheta(1-\ell/r),
\qquad \frac{d}{dr}(w_1-w_{-1})=\frac{\vartheta\ell}{r^2}>0.
\]

The two adjacent gaps are each half this gap.
Since $E[X]=0$, any indicator with conditional means $y_x$ satisfies $\operatorname{Cov}(X,Y)=d(y_1-y_{-1})$.
Apply this equation first to entry, then to a challenger win:

\[
\operatorname{Cov}(X,\mathbf1_A)=d(1-\rho)J,
\quad
\operatorname{Cov}(X,\mathbf1_W)=d[e_+w_1-\rho w_{-1}].
\]

Above the ceiling, the second covariance becomes $d\rho\vartheta(1-\ell/r)>0$.
The hidden-price case has exactly that formula at every F strength.
The winner gaps are $0.3080781048400065\ldots$ and $0.3337512802433404\ldots$.
The gap concerns prepared challengers; the unconditional win gap also contains entry.

### Proposition 8: corrected event domain; formulas analytical, values computer-assisted

An announcement of preparation leaves the class posterior at $\mu_x$.
The revised price is $t_L+\Delta\mu_x=t_0+A_r(\mu_x)$.
A positive-probability announcement of no preparation gives price $t_0$.
Subtract the execution-stage price:

\[
\Delta_x^1=(1-e_x)A_r(\mu_x),\qquad
\Delta_x^0=-e_xA_r(\mu_x),\quad e_x<1\text{ for the second observed event}.
\]

Their probability-weighted mean is exactly

\[
e_x\Delta_x^1+(1-e_x)\Delta_x^0=0.
\]

Division by the fixed positive price $P(x)$ preserves the zero conditional mean.
Since $A_r(\mu_x)>0$, the preparation surprise vanishes exactly when $e_x=1$.
Write the probability statement in part (iii) as $\Pr(A^c\mid X=x)=0\iff e_x=1$.
At $e_x=1$, a posterior after $A^c$ is undefined.
The no-preparation formula there can only be an algebraic extension, not an observed return.
P5 correctly omits that value from its benchmark table.

For F, the posterior mean is $1/2$, and only a buy adds entry.
Therefore

\[
\bar P=t_0+\rho A_r(1/2)+(1-\rho)JdA_r(M),
\quad P(0)-\bar P=-(1-\rho)JdA_r(M).
\]

The neutral posterior stays at $1/2$.
Thus the negative price change reflects the lost expected entry increment.
All registered announcement values and ratios are confirmed.

**Observation correction.** The zero mean uses both announcements, including no preparation, with their model probabilities.
It is not the mean return in a sample of preparation announcements alone.
At $r_1$, that latter sample has mean dollar change $0.160591936090535\ldots>0$.
Its mean ratio return is $0.270348938702210\ldots>0$.
At $r_2$, the corresponding means are $0.701041666666667\ldots$ and $1.045917750972411\ldots$.
A public event must reveal only preparation for these formulas to apply.

### Proposition 9: corrected proof sentence and tie scope; formulas analytical, values computer-assisted

The N and U tuples exist under the stated strict investor incentives.
Their order laws give the claimed volume and mean order.
In U,

\[
\frac12-z
=\frac{\lambda}{2(2-4b-\lambda)}
=\frac{\lambda}{4(1-v_U)}>0.
\]

Both the sale and neutral order have entry $\rho$.
Hence $P(-1)-P(0)=\rho\Delta\lambda/[4(1-v_U)]>0$.
The buy has posterior $M>1/2$ and entry one, so $P(1)>P(-1)>P(0)$.
The registered gap at 1.60 is $0.005362622499240276\ldots$.

**Correct the proof of part (iv).** The sentence “In N both are zero” uses an incorrect entry level.
In N, the buy impact is zero and entry after a buy is $\rho$.
The entry **increment** above $\rho$ is zero.
The stated association between N and U follows with that corrected sentence.

Under the declared challenger rule, the two-cluster interpretation can also be proved for the strict coexistence interval.
Every equilibrium has $t=0$, since a sale earns at most $\rho\Delta/2-k<0$.
If a buy fails to recruit, its payoff is at most that same negative bound.
If it recruits, its payoff is at least $\Delta m-k>0$.
Thus H either abstains fully or buys fully.
These are exactly N and U under that rule.

**The exhaustive interpretation depends on the challenger rule.** A permitted mixture at challenger indifference adds another equilibrium under the declared investor rule.
Set

\[
s_\tau=b\frac{2\tau-1}{1-\tau},\quad t=0,\quad
\sigma_H(1)=s_\tau/\lambda,\quad
e_1=\frac{k}{\Delta(1-\tau)}.
\]

Then $\mu_1=\tau$, H is indifferent between a buy and abstention, and L strictly abstains.
At $r=1.60$, $\sigma_H(1)=0.492845139150601\ldots$ and $e_1=0.506106106106106\ldots$.
Both probabilities are interior.
The low-class sale payoff is $-0.0059375$.
All non-buy entry rates remain $\rho$, and the price reveals the relevant posterior.
This verifies the additional tuple under the alternative rule.
The tie table must restrict its “none” statement to the existence and formulas of N and U.
It cannot extend that statement to the exhaustive two-cluster interpretation.

## 4. Strict margins and the open parameter set

The existing benchmark margins are correct.
The following table lists their numerical values, with the additional margins needed for the ceiling scope.
The values below are short displays of the independent intervals in the log.

| Strict condition | Benchmark margin | Result |
|---|---:|---|
| $\beta<1/3$ | $0.0386783333333$ | Interior posterior-bound condition |
| $\Delta(r_0)<k$ | $0.00333333333333$ | N uniqueness |
| $\rho\Delta(r_1)m>k$ | $0.0248235702283$ | F uniqueness |
| $\rho\Delta(r_2)m>k$ | $0.0431265280716$ | F uniqueness |
| $M>\tau(r_1)$ | $0.0260585786300$ | Buy recruits |
| $M<\tau(r_2)$ | $0.000333564719409$ | Return to the floor |
| $r_C<r_2$ | $0.00734148120534$ | Ceiling location |
| $B_{r_1}(1/2)<6$ | $1.70833333333$ | Neutral order does not recruit |
| $u<2686/1559$ | $0.00461746596045$ | Upper information bound |
| $u>82/59$ | $0.328451319984$ | Lower information bound |
| $M>5/8$ | $0.106058578630$ | Ceiling exists |
| $r_S<r_C$ | $1.46851038598$ | Ceiling lies on F |
| $r_N<r_C$ | $1.84478098053$ | Recruitment on the coexistence interval |
| $r_S<10$ | $7.87585186718$ | Nonempty F interval |
| $\Delta(1.55)m>k$ | $0.00624347740788$ | H buys in U |
| $B_{1.65}(M)>6$ | $0.713202283588$ | Buy recruits in U |
| $\rho\Delta(1.65)/2<k$ | $0.00399621212121$ | L abstains in U |
| $1.55>r_F$ | $0.0828729587069$ | Coexistence location |
| $1.65<r_N$ | $0.0978775382680$ | Coexistence location |

The primitive margins also stay positive: $\lambda=0.336121768915\ldots$, $1-\lambda=0.663878231085\ldots$, $\beta=0.294655$, $\rho=1/4$, and $1-\rho=3/4$.
The fixed cost satisfies $k=1/50>0$.
The reserve and value gaps satisfy $p=\ell-p=1/2>0$.
At the three benchmark strengths, the smallest $r-\ell$ is $1/5$, and the smallest $h-r$ is $32/5$.

**Correct the open-set statement.** P5's displayed set uses $\beta\le1/3$, so it is not open in the parameter plane.
It is relatively open within the admitted liquidity domain.
For a strict open set in the two free slot parameters, use this table:

| Free parameter | Strict restriction |
|---|---|
| $\beta$ | $0<\beta<1/3$ |
| $\lambda$ | $\dfrac{(82/59)\beta}{1+(82/59)\beta}<\lambda<\dfrac{(2686/1559)\beta}{1+(2686/1559)\beta}$ |
| Equivalent posterior | $141/200<M<4245/5804$ |
| F strength | $r_S(M)<r<10$ |
| U coexistence strength | $r_F(M)<r<r_N$ |

This set contains B.
It implies $M>5/8$, $r_S<3<r_C<3.6$, and all strict benchmark incentive conditions.
The coexistence interval lies below $r_C$ on this set.
Treat $\beta=1/3$, $r=r_C$, and $r=r_N$ as separate boundary cases under the declared tie rules.
The existing text's claim that every hypothesis is strict requires this separation.
The uniqueness margin tends to zero as $r\downarrow r_S$; no uniform positive margin exists on that entire open interval.

## 5. Verdict for every registry row group

Row numbers below count data rows, with the CSV header excluded.
The companion CSV provides the individual verdict, interval, stored-value difference, and display comparison for every row.
**Every row is confirmed numerically. No row differs beyond its display precision.**

| Rows | Keys, inclusive | Count | Verdict and status |
|---|---|---:|---|
| 1–12 | `u_p5_B` through `theta_pct_B` | 12 | confirmed; computer-assisted, with exact beta input |
| 13–32 | `margin_obs_beta_B` through `theta_hi` | 20 | confirmed; computer-assisted or exact analytical values |
| 33–37 | `own_p5_r1_B` through `entry_r2_obs_B` | 5 | confirmed; computer-assisted, with input floor |
| 38–47 | `ba_class_r1_B` through `impact_sell_r2_B` | 10 | confirmed; computer-assisted |
| 48–55 | `pbar_r1_B` through `pbar_jump_rC_B` | 8 | confirmed; computer-assisted, with exact zero neutral change above the ceiling |
| 56–61 | `alt_lambda_B` through `theta_min_counts_B` | 6 | confirmed; computer-assisted; count-law scope for the final key |
| 62–71 | `imb_buy_B` through `ba_U_r165_B` | 10 | confirmed; computer-assisted, with exact sale posterior $1/2$ |
| 72–85 | `wgap_r1_B` through `win_prob_r2_B` | 14 | confirmed; computer-assisted, with exact zero entry covariance at $r_2$ |
| 86–106 | `evA_r1_sale_B` through `evNr_r2_buy_B` | 21 | confirmed; computer-assisted; observed events only |
| 107–112 | `price_r1_sale_B` through `price_r2_buy_B` | 6 | confirmed; computer-assisted |

No numeric replacement is required in the P5 registry.
The note for `rF_check_B` is stale: the current brief states the correct B value.
The registry labels the boundary $r_S$ accurately; it does not certify a downward-rounded interval endpoint.
The key `theta_min_counts_B` remains correct as a lower count-law bound.
It does not remove the upper equilibrium restriction derived above.

## 6. Model objects and their empirical counterparts

| Model object | Correct counterpart and condition | Verdict |
|---|---|---|
| $P(x)=E[V_T\mid X=x]$ | Competitive conditional target value, also the execution price for a nonzero unit order | confirmed, analytical |
| $P(1)-P(-1)$ | Difference between conditional unit execution prices | corrected terminology |
| $X=0$ | A public opportunity with no trade | confirmed; preserve the opportunity denominator |
| $v=\Pr(X\ne0)$ | Nonzero unit trades per public opportunity | confirmed; it is not volume per unit of calendar time |
| $P(0)$ | Conditional value after an observed inactive opportunity | confirmed; it is not automatically the pre-slot price |
| $I_-=P(0)-P(-1)$ | Sale price difference relative to the neutral conditional value | confirmed; identification needs this reference |
| $\bar P=E[P(X)]$ | Price before the slot under the selected equilibrium | confirmed under the passive observation protocol |
| $A$ | Preparation before the auction | confirmed; an observed final bid is a different selection event |
| $w_x$ | Challenger win probability conditional on preparation and the order | confirmed; keep it separate from $e_xw_x$ |
| $\Delta_x^a$ | Announcement price change when the event reveals only preparation | confirmed on positive-probability events |
| $\Delta_x^a/P(x)$ | Simple return with zero additional standalone value | confirmed; a positive constant value enlarges the denominator |
| $\vartheta$ | Share of actual nonzero orders from the informed identity on F | confirmed; it differs from presence $\lambda$ |

**Correct “quoted spread” at P5 lines 399–401.** The model sets a price after the market makers observe the order.
It contains no separate public quote stage or continuous limit order book.
The conditional execution spread is exact.
A precommitted bid and ask require an added institutional interpretation.
Zero conditional dealer profit establishes the price formula; it does not itself establish observed pre-trade quotes.
The earlier N1 memo correctly uses the conditional execution interpretation.

**Correct the first-order measurement instruction.** Use the first prespecified public opportunity, including a recorded zero when no trade occurs.
A sample of the first executed trade omits $X=0$.
That sample cannot identify (v), the neutral-price effect, or the stated informed share from these formulas.

The separate friction $k$ enters the investor's choice but does not enter the execution spread as a dealer charge.
The known class values and public incumbent strength supply $\Delta(r)$ only within the maintained auction model.
The sell-impact formula is not an estimator without those maintained inputs.

## 7. Earlier claims, failures, and open items

The exact calibration A values in N1 agree with the independent rational reconstruction.
This includes the spread $25/32$, entry share $113/125$, winner gaps $3/10$ and $13/40$, and announcement changes.
The structural decomposition, identification formula, winner restriction, and passive announcement formulas survive at B.
The N1 comparison pair with $\beta'=23/68$ exceeds the new bound $1/3$.
P5's admissible example $u'=8/5$ correctly replaces it.

**Refuted earlier claim.** N1 §2.1 says each component rises strictly while $J$ stays fixed.
The entry component is zero throughout the regime $J=0$.
P5 Proposition 3(v) repeats this error.
Thus P5's statement that no structural claim fails requires correction.

**Current brief: no refuted numerical claim.** BRIEF §3 already states $r_F=1.467127$ at B and assigns $1.460985$ to A.
P5's “Refuted brief value” paragraph describes an earlier version, not the reviewed brief.
Replace that paragraph and the related registry note with the current agreement.

The following items stay open or require a manuscript decision:

- Selection between N and U remains open under the baseline tie rules.
- The low-class mixture on $(r_N,r_S)$ lies outside this check's complete equilibrium classification.
- A quote protocol and a reliable opportunity denominator require empirical specification.
- Announcement formulas require events that reveal only preparation.
- The extra equilibrium under challenger mixtures changes the exhaustive two-cluster claim.

The checked files remain unchanged.
The manuscript can use the confirmed identities and values after the stated corrections to scope, boundaries, and observables.
