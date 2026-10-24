# X_C8. Independent reserve check

## 1. Scope

This memo checks the seven headline claims in `C8_reserve.md`.
The base is discrete-Laplace noise with orders $q\in\{0,1\}$.
It retains class information before preparation, as the team brief requires.
The only extension changes the low preparation cost.

The paper source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
Relevant sources are main Sections 2 and 6.3, main Appendix A.7, and online Appendix A.10.
The check uses no other manuscript version.

The parameters are

$$
(h,\ell,\rho,c_H,b,k,\pi,\lambda)
=(10,1,1/4,5,2,1/50,1/2,1).
$$

The main case has $c_L=0$.
The robustness cases have $0<c_L\le0.1$ and $c_L=1$.
The latter keeps $c_H=5$; it does not restore every paper parameter.

Independent derivations and a new script preceded inspection of the original scripts.
The new script uses 60 decimal digits and exact rational bounds.
It enumerates reserve boundaries and stationary points; it does not use a reserve grid.
Its files are in `scripts/X_C8_check/` relative to the team folder.

## 2. Verdict table

| Claim | Verdict | Evidence and status |
|---|---|---|
| 1. Lemma C8.0: posterior formulas | CONFIRMED WITH CORRECTION | The formulas are analytical. At $\beta=0$, the two formulas give one posterior. |
| 2. Proposition C8.1: cap, candidates, strict price revelation | CONFIRMED | Section 3.3 gives an analytical proof under the stated tie rules. |
| 3. Corollary C8.1a: $p^*=h$ throughout the interval; revenue comparison | CONFIRMED WITH CORRECTION | Exact rational bounds certify the whole interval. The original grid does not supply that certificate. |
| 4. Proposition C8.2 and Corollary C8.2a | CONFIRMED | The return formula and low-state dominance are analytical. Full purchase and proceeds $1.25$ follow from claim 3. |
| 5. Proposition C8.3 and the best committed reserve | CONFIRMED WITH CORRECTION | The fixed-orders inequality is analytical. Claim 3 proves $p^c=10$ globally at both benchmark strengths. Broader equilibrium comparisons need more proof. |
| 6. Proposition C8.4 and its benchmark failure | CONFIRMED WITH CORRECTION | The conditional proof works for the declared primitives. A general version needs the low-posterior condition in part (iii). The benchmark failure is certified. |
| 7a. Unobservable preparation before the reserve gives the same game | REFUTED | A seller deviation holds sunk preparation fixed. Section 3.8 gives a strict deviation at $r=3.6$. |
| 7b. Observable preparation: $p=h$ after entry; proceeds $2.118648$ | CONFIRMED | An analytical bound proves the reserve choice at $r=3$. Independent arithmetic reproduces the number. |

The central robustness result has status **computer-assisted**.
Small positive costs preserve the entry floor outcome.
At $c_L=1$, expensive entry returns at $r=3$, under the original preparation tie rule.

## 3. Derivations and evidence for each claim

### 3.1 Information, timing, and equilibrium

Nature draws the class, the preparation cost, the incumbent value, and noise independently.
The investor sees the class and submits an order.
The market observes total flow.
The seller receives the market posterior through the quote.
The seller then sets the reserve before preparation.
Preparation reveals the challenger value and permits a bid.

An equilibrium specifies conditional orders, Bayesian posteriors, a competitive quote, a sequentially optimal reserve, and optimal preparation.
Truthful bids apply after preparation.
An investor deviation faces the fixed quote and reserve schedules.
A seller deviation holds the posterior fixed and permits a preparation response.
This last response requires preparation to occur after the reserve.

All integer flows have positive probability under every conditional order distribution.
Thus no off-path flow belief is needed.
After a reserve deviation, the challenger retains the posterior from the quote.
The seller has no extra private information, so the reserve supplies no additional signal.
This continuation rule should appear explicitly in the original memo.

The preparation rule admits preparation at equality.
The investor chooses zero at equality.
The seller chooses the smallest optimal reserve.
A bid equal to the reserve is admissible.
These four rules have different roles.
In particular, the investor rule excludes deliberate randomization at equality.

The price must anticipate the reserve strategy.
A precise sequential version sets the transaction quote before the seller chooses its reserve.
Competitive prices then equal expected proceeds under the anticipated strategy.
A seller deviation leaves that quote fixed.
Alternatively, a reference quote can precede a later transaction quote.
The original memo must identify which quote the investor pays; equilibrium invertibility alone does not establish identical games at every history.

All main calculations below concern the posterior-observation formulation in the original memo.
They support the sequential version with an anticipated reserve strategy and the stated continuation beliefs.

### 3.2 Auction payoffs and Lemma C8.0

**Status: analytical.**

For $0\le p\le\ell$, direct integration gives

$$
\begin{aligned}
t_0&=\frac1r\int_p^r p\,dR=p(1-p/r),\\
t_H&=\frac1r\left[\int_0^p p\,dR+\int_p^r R\,dR\right]
=\frac r2+\frac{p^2}{2r},\\
t_L&=\frac1r\left[\int_0^p p\,dR+\int_p^\ell R\,dR+\int_\ell^r\ell\,dR\right]
=\ell-\frac{\ell^2-p^2}{2r},\\
g_H&=h-t_H,\\
g_L&=\frac1r\left[\int_0^p(\ell-p)\,dR+\int_p^\ell(\ell-R)\,dR\right]
=\frac{\ell^2-p^2}{2r}.
\end{aligned}
$$

For $\ell<p\le r$, the low class cannot bid, so $t_L=t_0$ and $g_L=0$.
For $r<p\le h$, only the high class can bid, so $(t_0,t_H,t_L,g_H,g_L)=(0,p,0,h-p,0)$.
These formulas agree with the pinned paper.
At $p=\ell$, the low class remains admissible.
At $p=h$, the high class remains admissible with zero acquisition rent.

Let $f(z)=(1-a)a^{|z|}/(1+a)$, where $a=e^{-1/2}$.
Under $(\beta_H,\beta_L)=(\beta,0)$,

$$
\frac{\Pr(X=x\mid H)}{\Pr(X=x\mid L)}
=1+\beta\left(\frac{f(x-1)}{f(x)}-1\right).
$$

The density ratio equals $a^{-1}$ for $x\ge1$ and $a$ for $x\le0$.
Thus

$$
\mu_G(\beta)=\frac{1+\beta(a^{-1}-1)}{2+\beta(a^{-1}-1)},\qquad
\mu_B(\beta)=\frac{1+\beta(a-1)}{2+\beta(a-1)}.
$$

For $\beta>0$, these are distinct.
At $\beta=0$, both equal $1/2$.
This corrects the claim of exactly two posterior values for every $\beta$.

At $\beta=1$,

$$
m=\frac{a}{1+a}=0.37754066879814543536,\qquad
M=\frac1{1+a}=0.62245933120185456464.
$$

The geometric sums give $\Pr(Z\ge0)=M$ and $\Pr(Z\ge1)=m$.
A high-state purchase reaches $X\ge1$ with probability $M$.
A low-state zero order reaches it with probability $m$.
Its unconditional probability under full purchase is $(M+m)/2=1/2$.

### 3.3 Proposition C8.1: the seller problem

**Status: analytical.**

Write $B(p,\mu)=(1-\mu)g_L+\mu g_H$.
Its derivative across the three reserve regimes is

$$
B_p=
\begin{cases}
-p/r,&0<p<\ell,\\
-\mu p/r,&\ell<p<r,\\
-\mu,&r<p<h.
\end{cases}
$$

The function is continuous at both regime boundaries.
It strictly decreases from $B(0,\mu)$ to zero.
For a cost $c\le B(0,\mu)$, its cap is

$$
p_c(\mu)=
\begin{cases}
\sqrt{2r[B(0,\mu)-c]},&c\ge B(\ell,\mu),\\
\sqrt{2r(h-c/\mu)-r^2},&B(r,\mu)\le c<B(\ell,\mu),\\
h-c/\mu,&0\le c<B(r,\mu).
\end{cases}
$$

The cap is absent when $c>B(0,\mu)$.
The high-cost cap is $\bar p=p_{c_H}$.
In regime I, $B_\mu=h-r/2-\ell^2/(2r)>h-r>0$.
In regime II, $B_\mu=h-t_H\ge h-r>0$.
In regime III, $B_\mu=h-p\ge0$.
Thus the cap rises weakly with $\mu$.
At zero low cost, entry equals one below this cap and $\rho$ above it.

For a fixed entry probability $e$, write proceeds as $S_e$.
Direct substitution gives

$$
\begin{aligned}
S_e'&=(1-e)+(3e-2)p/r,&&p<\ell,\\
S_e'&=(1-e\mu)+(3e\mu-2)p/r,&&\ell<p<r,\\
S_e'&=e\mu,&&r<p<h.
\end{aligned}
$$

An interior maximum in the first regime can occur at
$p=r(1-e)/(2-3e)$.
An interior maximum in the second can occur at
$p=r(1-e\mu)/(2-3e\mu)$.
Each candidate must lie in its regime and have the stated entry probability.
For $c_L=0$, the first regime needs only $e=\rho$; $e=1$ gives a positive derivative for $p>0$.
The second regime uses $e\in\{\rho,1\}$.

Together with $0,\ell,r,h,\bar p$, these points exhaust the possible maximizers.
There are at most two feasible interior candidates, as the original claim requires.
Indeed, the two second-regime roots increase with $e$ whenever they are interior maxima.
Both cannot satisfy the opposite cap restrictions at once.
The first regime supplies at most one more root.

At $p=\ell$, proceeds can jump down to the right.
At a participation cap, preparation at equality gives the higher entry value at the cap.
The participation jump has size

$$
(1-\rho)\big[(t_L-t_0)+\mu(t_H-t_L)\big]\ge0.
$$

Thus proceeds are upper semicontinuous on $[0,h]$.
They attain a maximum.
This proof uses the preparation rule at equality and admissible bids at the reserve.

At a fixed reserve, between participation jumps,

$$
S_\mu=e\Delta_T(p)>0.
$$

Here $e\ge\rho>0$, and the spreads are

$$
\Delta_T(p)=
\begin{cases}
(r-\ell)^2/(2r),&p\le\ell,\\
r/2-p+3p^2/(2r),&\ell<p\le r,\\
p,&r<p\le h.
\end{cases}
$$

The middle expression has minimum $r/3>0$ over the real line.
Thus every spread is positive.
At a participation jump, proceeds rise.
Hence each fixed-reserve proceeds function strictly rises with $\mu$.
For $\mu'>\mu$, evaluate the higher-posterior problem at a maximizer for $\mu$:

$$
V(\mu')\ge S(p^*(\mu);\mu')>S(p^*(\mu);\mu)=V(\mu).
$$

The price reveals the posterior, not the realized class.
This confirms Proposition C8.1.

### 3.4 Corollary C8.1a: a certificate for the full posterior interval

**Status: computer-assisted.**

The original sample of 25 posteriors does not certify the interval.
The following bounds cover every posterior and every reserve.

Set $C(\mu)=\rho\mu h$ and $\delta_r=(r-1)^2/(2r)$.
Let $m_-$ and $M_+$ be exact rational bounds for $m$ and $M$.
The script constructs them from

$$
E_- =\sum_{n=0}^{20}\frac{(1/2)^n}{n!},\qquad
E_+=E_-+\frac{(1/2)^{21}}{21!}\frac{44}{43}.
$$

The ratio of successive terms after the first omitted term is at most $1/44$.
Therefore $E_-<e^{1/2}<E_+$.
Take $m_-=1/(1+E_+)$ and $M_+=E_+/(1+E_+)$.
Every sign comparison below uses exact fractions.

For floor entry in regime I,

$$
S_\rho\le(1-\rho)r/4+\rho(1+\mu\delta_r).
$$

Consequently,

$$
C-S_\rho\ge\rho m_-(h-\delta_r)-(1-\rho)r/4-\rho.
$$

For floor entry in regime II, put $z=\rho\mu$.
The unrestricted quadratic maximum is

$$
F_r(z)=\frac{r(1-2z^2)}{2(2-3z)}.
$$

For each fixed reserve in this regime, $C-S_\rho$ increases with $\mu$.
Its slope is $\rho(h-\Delta_T(p))>0$, since $\Delta_T(p)\le r<h$.
Thus the uniform gap is at least $\rho m_-h-F_r(\rho m_-)$.

For full entry in regime I, feasibility requires $B(0,\mu)\ge5$.
Hence

$$
\mu\ge q_r:=\frac{5-1/(2r)}{10-r/2-1/(2r)}.
$$

Since $S_1$ rises with the reserve there, $S_1\le1+\mu\delta_r$.
The resulting gap is at least $q_r(\rho h-\delta_r)-1$.

In regime II, full entry implies $\mu t_H\le\mu h-5$.
Since $t_0\le r/4$,

$$
S_1\le\mu h-5+(1-\mu)r/4,
\qquad
C-S_1\ge5-r/4-[(1-\rho)h-r/4]M_+.
$$

In regime III, full entry implies $p\le h-5/\mu$.
Thus $C-S_1\ge5-(1-\rho)hM_+$.
Floor entry gives $S_\rho=\rho\mu p$, which strictly rises up to $p=h$.
For later cost comparisons, no entry gives $S_0\le r/4$.

The exact calculations give these conservative gaps:

| Competing branch | $r=1.2$ | $r=3$ |
|---|---:|---:|
| Floor, regime I | 0.467278585875 | 0.068428227195 |
| Floor, regime II | 0.600600009539 | 0.085722515854 |
| Full entry, regime I | 0.267006802721 | 0.063333333333 |
| Full entry, regime II | 0.218292815346 | 0.048399514387 |
| Full entry, regime III, if feasible | 0.331555015986 | 0.331555015986 |
| No entry | 0.643851671995 | 0.193851671995 |

Every gap is strictly positive.
The remaining floor branch in regime III strictly rises to $h$.
Therefore $p^*(\mu)=h$ uniquely for every $\mu\in[m,M]$ at both strengths.
This supplies the missing interval certificate.

At $(r,\mu)=(3,M)$, independent evaluation gives

$$
\begin{aligned}
\bar p&=1.67453880475222110987,\\
S(\bar p)&=1.50391503985100811694,\\
S(h)&=1.55614832800463641160,\\
S(h)-S(\bar p)&=0.05223328815362829466.
\end{aligned}
$$

These numbers confirm the headline comparison.
At $(3,m)$, the best floor reserve below $r$ gives $0.85812915614079187451$.
The reserve is $1.58246393364753309404$.
Its gap below $S(h)$ is $0.08572251585457171389$.

### 3.5 Proposition C8.2 and Corollary C8.2a

**Status: analytical, conditional on the certified seller choice.**

At a fixed flow, reserve, and entry probability, the conditional residuals are

$$
\begin{aligned}
E[V_T\mid H,x]-P(x)&=e\Delta_T(1-\mu_x),\\
E[V_T\mid L,x]-P(x)&=-e\Delta_T\mu_x.
\end{aligned}
$$

A low-state purchase has net return at most $-k<0$.
Thus $\beta_L=0$ in every equilibrium.
A high-state purchase reaches good news with probability $M$ and bad news with probability $m$.
Its gross return is

$$
K(\beta)=M e_G\Delta_G(1-\mu_G)+m e_B\Delta_B(1-\mu_B).
$$

The original formula is correct.
Under the stated investor rule, no purchase requires $K(0)\le k$.
Full purchase requires $K(1)>k$.
An interior probability cannot occur under that selection rule.
Under the usual mixed best-response correspondence, equality permits mixtures and permits full purchase.
The two concepts must remain separate.

At both benchmark strengths, the certificate gives $e_s=\rho$ and $\Delta_s=h$.
For every $\beta\in[0,1]$,

$$
K(\beta)\ge\rho h(Mm+m/2)
=1.05943511650166801687>0.02.
$$

Hence full purchase is unique even under the mixed best-response correspondence.
The endpoint values are

$$
K(0)=1.25,\qquad K(1)=2\rho hMm=1.17501856100797244535.
$$

Entry is $\rho$, high-class ownership is $\rho/2$, and proceeds are

$$
E[V(\mu_X)]=\rho hE[\mu_X]=\rho h/2=1.25.
$$

The last equality also holds without a full-purchase posterior law.
It uses the Bayesian identity $E[\mu_X]=1/2$.

### 3.6 Proposition C8.3: commitment

**Status: analytical, conditional on the certified seller choice where stated.**

For a fixed posterior law and any committed reserve $p^c$,

$$
E[V(\mu_X)]-E[S(p^c;\mu_X,r)]\ge0.
$$

This follows pointwise from the maximum that defines $V$.
It does not compare endogenous posterior laws across arbitrary equilibria.

At $r=1.2$ and $r=3$, the interval certificate proves more.
Every possible posterior under the permitted orders lies in $[m,M]$.
For every reserve and every such posterior,

$$
S(p;\mu,r)\le\rho\mu h.
$$

Thus every committed-reserve continuation has proceeds at most $\rho h/2=1.25$.
Reserve $p^c=h$ attains that bound and induces unique full purchase.
This proves global optimality at both strengths, without a committed-reserve grid or an equilibrium selection across other reserves.

The entry comparison under full purchase is also correct at the declared primitives.
A low committed reserve can admit expensive preparation only after good news.
Then expected entry is $(1+\rho)/2=0.625$.
The contingent benchmark gives $\rho=0.25$.
In a general statement, that comparison also requires floor entry at the lower posterior under the contingent rule.

The broad sentence that commitment never helps a seller does not follow from the fixed-orders inequality.
Limit that sentence to the two certified strengths.
The reported $r=9$ comparison is a grid comparison, as its local qualification states.

### 3.7 Proposition C8.4 and its benchmark failure

**Status: analytical for the conditional argument; computer-assisted for the benchmark seller choice.**

At $r_0$, $k>\bar\Delta^*$ implies $K(\beta)<k$ for every $\beta$.
The only order is zero.
The posterior is $1/2$, and the stated prior entry condition gives entry $\rho$.

At $r_1$, the stated lower bound exceeds $k$ for every $\beta$.
The only high-state order is one.
The two entry conditions then give entry probabilities $1$ and $\rho$ at $M$ and $m$.
Expected entry is $0.625$, and high-class ownership is $(M+\rho m)/2>\rho/2$.

Part (iii) also needs no expensive preparation at the lower posterior under its chosen reserve.
That conclusion does not follow merely from exclusion at $M$ for an arbitrary posterior-dependent reserve.
For the declared primitives, it follows from a separate bound:

$$
B(0,m;r)=\frac{1-m}{2r}+m(10-r/2)
<\frac12+9m=3.89786601918330891825<5,
\qquad r>1.
$$

The expression strictly decreases with $r$.
No reserve can induce expensive preparation at $m$ for these primitives.
Thus part (iii) is valid here.
A general version must add $B(p^*(m),m)<c_H$ or prove it from other assumptions.
No global monotonicity of the selected entry probability appears in the original proof.

At the benchmark pair, the seller chooses $h$ throughout the posterior interval.
Therefore $B(h,M)=0<5$ at $r_1$.
Also $\bar\Delta^*(r_0)=10>0.02$.
Both failed conditions in the original memo are correct.
The benchmark gives full purchase and entry $\rho$ at both strengths.

### 3.8 Reserve choice after preparation

**Unobservable preparation: REFUTED; status analytical.**

An unobserved preparation decision is still a sunk decision.
Let $e^{\mathrm{pre}}(\mu)$ denote its equilibrium probability.
At the later reserve node, the seller maximizes

$$
\widetilde S(p;\mu)
=t_0(p)+e^{\mathrm{pre}}(\mu)
\big[t_L(p)-t_0(p)+\mu\Delta_T(p)\big].
$$

A seller deviation cannot replace $e^{\mathrm{pre}}(\mu)$ with the responsive function $e(p,\mu)$.
The original memo does exactly that when it says every outcome carries over.

Its own $r=3.6$ case supplies a counterexample.
At $\mu=M$, the main timing chooses $p=1$ and induces preparation with probability one.
Its proceeds are $1.58442014985063011902$.
After that preparation, a deviation to $p=h$ gives

$$
\widetilde S(h;M)=Mh=6.22459331201854564639.
$$

This is a strict profitable deviation.
No observation of the preparation action is needed for that deviation.
At $r=1.2$ and $r=3$, the zero-cost outcomes can coincide because $h$ also maximizes the objective with preparation fixed at $\rho$.
That local coincidence does not establish the general claim.

**Observable preparation at $r=3$: CONFIRMED; status analytical.**

Preparation depends on the posterior and cost, but not on the unknown class.
Conditional on that posterior, the action therefore gives no further class information.
After entry, the seller maximizes $S_1(p;\mu)$.

For $p\le1$, $S_1\le1+(2/3)\mu<10\mu$ throughout $[m,M]$.
For $1<p\le3$, $S_1\le3\mu+(1-\mu)3/4<10\mu$ throughout that interval.
For $3<p\le10$, $S_1=\mu p$, with its unique maximum at $10$.
Thus the optimal reserve after entry is $h$.

After no entry, the seller maximizes $p(1-p/r)$ at $p=r/2$.
Its proceeds are $r/4$.
At $c_L=0$, preparation remains $\rho$ by the preparation rule at equality.
Consequently,

$$
\rho\mu h+(1-\rho)r/4
\bigg|_{r=3,\,\mu=M}
=2.11864832800463641160.
$$

The original numerical diagnostic is correct and admits this analytical reserve proof.
The state-independent no-entry payoff leaves the investor spread equal to $\rho h$.
Full purchase remains optimal at this benchmark.

## 4. The robustness result for positive low cost

### 4.1 Small positive costs preserve suppression of expensive entry

**Status: computer-assisted.**

For general $c_L=c>0$, entry is

$$
e_c(p,\mu)=\rho\mathbf1\{B(p,\mu)\ge c\}
+(1-\rho)\mathbf1\{B(p,\mu)\ge5\}.
$$

At $p=h$, $B=0<c$, so entry and proceeds are zero.
Thus the exact reserve $h$ cannot remain optimal.
If $p>r$, the highest reserve that preserves low-cost preparation is

$$
p_L(\mu)=h-\frac c\mu,\qquad
S(p_L;\mu)=\rho(\mu h-c).
$$

The low-cost challenger has zero net preparation gain at this reserve.
It prepares under the original tie rule.
The expensive challenger stays out because $c<5$.

For $0<c\le0.1$, $p_L>9.7>r$ at both benchmark strengths.
The candidate value differs from $C(\mu)$ by at most $\rho c\le0.025$.
Every competing branch in the certificate has a gap strictly above $0.025$.
The table includes the no-entry branch, which can now occur.
The floor branch in regime III strictly rises to $p_L$ and gives zero proceeds above that cap.
Therefore $p_L$ is uniquely optimal throughout the posterior interval.

The price becomes $\rho(\mu h-c)$ and remains strictly informative about $\mu$.
The spread is at least $h-c/m>9.7$.
Thus, for every candidate purchase probability,

$$
K_c(\beta)\ge\rho(h-c/m)(Mm+m/2)>1.02>k.
$$

Full purchase is unique at both strengths.
Entry stays at $\rho$ and expected proceeds are $1.25-c/4$.
For example, $c=10^{-6}$ gives proceeds $1.24999975$.
The reserve changes, but suppression of expensive entry survives these small positive costs.

### 4.2 At cost one, expensive entry returns at the stronger incumbent

**Status: computer-assisted.**

Keep $c_H=5$ and set $c_L=1$.
At $r=1.2$, the reserve $p_L=10-1/\mu$ remains uniquely optimal throughout $[m,M]$.
The previous floor-branch gaps remain positive after subtraction of $1/4$.
The regime-I full-entry gap also remains positive: its lower bound becomes $0.017006802721$.

The full-entry regime-II bound needs a refinement.
If the expensive cap lies below $r$, then $\mu\le5/(10-r)=25/44$.
Use that bound in the regime-II certificate in place of $M_+$.
After subtraction of $1/4$, the resulting gap is positive.
If the cap exceeds $r$, full-entry proceeds rise through regime II because $\mu>1/2$.
Their maximum there is $\mu r$, with gap at least $0.488636363636$ below the extraction value.

The regime-III full-entry gap is at least $0.081555015986$.
These bounds certify the claim over the whole interval.
Full purchase follows from the same positive return bound, with $h-1/m>7.35$.
Expected entry is $0.25$, and proceeds are $1$.

At $r=3$, the optimal reserves differ across the full-purchase posteriors:

| Posterior | Optimal reserve | Proceeds | Preparation probability |
|---|---:|---:|---:|
| $m$ | 1.58246393364753309404 | 0.85812915614079187451 | 0.25 |
| $M$ | 1.67453880475222110987 | 1.50391503985100811694 | 1 |

At $m$, expensive preparation is impossible even at reserve zero.
The displayed reserve is the unconstrained floor maximum in regime II.
Its low-cost gross gain is $3.05152329133056419428>1$.
It beats floor proceeds in regime I, the extraction value $0.693851671995$, and the no-entry bound $0.75$.

At $M$, the seller chooses the expensive cap $\bar p$.
It induces expensive preparation at equality.
Its proceeds exceed the low-cost extraction value $1.306148328005$ by $0.197766711846$.
They also exceed all floor maxima and the regime-I full-entry maximum.
Full-entry proceeds rise through the feasible part of regime II because $M>1/2$.
Hence the cap is the full-entry optimum.

The script encloses both posteriors with exact rational intervals of width $10^{-14}$.
It bounds the square root at the cap through integer square-root bounds.
Exact fraction comparisons certify each strict candidate comparison above.
The printed decimals provide readable values; the sign certificate uses fractions.

Full purchase is unique at $r=3$, including against all mixtures.
At reserve $p=3/2$, low-cost preparation is strictly profitable for every $\mu\in[m,M]$.
That reserve gives proceeds strictly above $3/4$.
Every reserve with zero entry gives proceeds at most $3/4$.
Therefore every optimal reserve has entry at least $\rho$.
Also every reserve has $\Delta_T\ge2/3$ at $r=3$.

The purchase return therefore satisfies

$$
K_1(\beta)\ge\rho\frac23(Mm+m/2)
=0.07062900776677786779>0.02.
$$

The endpoint calculation gives $K_1(1)=0.35718433447978373835$.
The equilibrium outcomes are

$$
\begin{aligned}
E[\text{preparation}]&=0.625,\\
O_H&=0.35842224920069546174,\\
E[\text{proceeds}]&=1.18102209799589999573.
\end{aligned}
$$

Thus entry rises from $0.25$ at $r=1.2$ to $0.625$ at $r=3$.
This restores the entry comparison at cost one.
It does not restore the original no-trade result at the weak incumbent: purchase is full at both strengths.

The conclusion concerns $c_H=5$.
At the paper value $c_H=6$, $B(0,M;3)=5.35382776001545470532<6$.
Then expensive preparation is impossible at $r=3$ under these buy-only posterior bounds, whatever reserve the seller chooses.

### 4.3 Attainment and the preparation rule at equality

**Status: analytical, with the strict gaps from Section 3.4.**

Under the original rules, the main seller problem is well posed at $p=h$ when $c_L=0$.
The preparation and admissible-bid rules give positive proceeds at that endpoint.
The maximum is attained.
There is no open-set problem under those rules.

Change the preparation rule so an indifferent challenger stays out.
At $c_L=0$, the reserve $h$ then gives zero proceeds.
For every $p<h$ near $h$, low-cost preparation is strictly profitable.
The proceeds approach $\rho\mu h$ as $p\uparrow h$.
The strict certificate gaps place every other branch below that limit.
Thus the seller has that supremum and no maximizing reserve.

For $0<c\le0.1$, the same problem moves to $p_L=h-c/\mu$.
With preparation only at a strict gain, floor preparation requires $p<p_L$.
Proceeds approach $\rho(\mu h-c)$ as $p\uparrow p_L$ but do not attain it.
The other branches remain strictly below that limit.
Thus merely replacing $h$ with a slightly lower reserve does not supply a seller best response under that alternative rule.

The cost-one result retains the original preparation rule for both cost types.
At its good-news reserve, the expensive type is indifferent and prepares.
The low-cost type is strictly willing to prepare there.
This distinction must remain explicit.
The strict seller comparisons at cost one persist for costs in a neighborhood of one.
The restored entry comparison therefore does not depend on the precise low cost being exactly one.

## 5. Errors found and corrections

### 5.1 The original output reproduces, but one claim contradicts it

After the independent calculations, the original script ran through its real command interface.
The rerun output is `scripts/X_C8_check/original_rerun.txt`.
Its SHA-256 equals the original saved output:

`57514dfb9671f041d2214b1b8bd1aeac3d4372d7a9d57a236e2075816a8f069b`.

Both outputs print `False` for the claim that every sampled posterior has grid reserve exactly equal to $h$.
The memo says each point has its maximizer at the top point $h$.
The discrepancy comes from repeated decimal addition.
The grid reaches $9.999\ldots9572$ rather than exact $10$.
This is a numerical endpoint defect, not an economic counterexample.

### 5.2 The reserve grid misses the exact low-class boundary

At $r=3.6$ and $M$, the grid reports $p=0.995$ and proceeds $1.5830347$.
The exact candidate $p=1$ gives $1.58442014985063011902$.
Repeated addition crosses just above $1$, where the low class ceases to qualify.
The candidate calculation includes exact $1$ and gives the correct optimum.

The original equilibrium table uses the grid result and reports total proceeds $1.306395$.
The exact candidate value gives $1.30708756860979018422$.
The original text acknowledges this approximation, but the equilibrium table should use the optimum.

### 5.3 The status of the interval claim lacks its required proof

High decimal precision is not an interval certificate.
A reserve derivative bound controls interpolation in the reserve only between included kinks.
It does not control the gap between sampled posteriors.
Exact fractions at one fixed reserve do not fill that gap.
The computer-assisted label needs a certificate such as Section 3.4.

### 5.4 Some reported returns use grid reserves

At $r=5$, exact candidates give $K(0)=0.24778106508875739645$ and $K(1)=0.70203756775616465555$.
The memo reports $0.247604$ and $0.702125$ from its reserve grid.
The qualitative comparison remains correct.
The memo should identify these as grid approximations or replace them with candidate values.

### 5.5 Substantive corrections

- Replace “exactly two” posteriors with “at most two”; retain two for $\beta>0$.
- Replace the general equivalence claim for unobservable prior preparation with the correct sunk-decision objective.
- State the continuation posterior after every reserve deviation.
- Identify the transaction quote and its position in the timeline.
- Restrict the unconditional commitment conclusion to the certified benchmark pair.
- For a general Proposition C8.4, add the lower-posterior exclusion condition in part (iii).
- State that suppression of expensive entry survives small positive costs but fails at $c_L=1$, when $c_H=5$.

## 6. What the original memo should change

1. Retain the zero-cost main result and its headline revenue numbers.
2. Replace the posterior-grid argument with a certificate for the full interval.
3. Use exact reserve endpoints and the finite candidates for all equilibrium tables.
4. Keep the investor selection rule separate from the usual mixed best-response correspondence.
5. Correct the timing claim when preparation is unobservable and precedes the reserve.
6. State that the exact reserve $h$ depends on zero cost and the preparation rule at equality.
7. Add the positive-cost result from Section 4, with its computer-assisted label.
8. State that a strict preparation rule can destroy attainment at the extraction boundary.
9. Keep the restored entry comparison separate from the full Proposition 2 mechanism.

No author file changes form part of this check.
The deliverables are this memo, the independent script, its output, a receipt, and the original-script rerun output.

## 7. Plain summary

The main zero-cost calculations are correct.
At both benchmark strengths, the seller sets reserve ten and entry stays at one quarter.
Purchase is full, and expected proceeds are 1.25.
The original posterior grid does not prove the full interval claim.
An independent exact certificate supplies that proof.

Small positive preparation costs change the reserve but preserve this outcome for entry.
For costs up to 0.1, the seller chooses the highest reserve that preserves low-cost preparation.
At cost one, the result changes.
With expensive cost five, entry rises to 0.625 at strength three.
Purchase remains full at both strengths.

The original preparation rule gives an attained seller maximum.
If an indifferent challenger stays out, the extraction branch can have only a supremum.
Finally, unobservable preparation before the reserve changes the seller's deviation problem.
It is not generally equivalent to preparation after the reserve.
