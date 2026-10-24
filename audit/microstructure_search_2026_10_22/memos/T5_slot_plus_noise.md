# T5: one order slot with symmetric separate noise

## 1. Question

Can the liquidity slot preserve the entry ceiling while separate noise permits strictly ordered entry at the three intermediate strengths?

**computer-assisted.** Yes, for the requested finite menu, at

$$
(\lambda,\beta,\theta)=\left(\frac5{11},\frac12,\frac{71}{200}\right).
\tag{1}
$$

The result holds on an explicit open box around this point.
No trade coexists with the selected informative branch at all three strengths.
The investor mixes at $1.55$ and $1.60$, then buys fully at $1.65$.
Thus the result does not supply three strictly interior purchase rates.

Entry at strength $3$ is $613/1600=0.383125$, below the paper's $0.522757$.
The successful noise has slightly more tail mass than equal EGJ weights.
It reverses the proposed direction of concentration toward zero.
The point favors simple fractions and equal liquidity action probabilities; it is not a global optimum.

## 2. Setup

### 2.1 Auction and information

The source is `overleaf/paper` commit `01bd5d6`.
The formulas below follow `main.tex`, Sections 2–4, equations (4), (9)–(11), and Appendix A.6.
The welfare accounting also follows `online_appendix.tex`, A.9.

Use Reading N with point masses and the paper's benchmark:

$$
(h,\ell,p,\rho,c_L,c_H,k,\pi)
=(10,1,1/2,1/4,0,6,1/50,1/2).
$$

The incumbent value is uniform on $[0,r]$, with $1<r<10$.
The auction objects are

$$
\begin{aligned}
t_0&=\frac12-\frac1{4r},&
t_H&=\frac r2+\frac1{8r},&
t_L&=1-\frac3{8r},\\
g_H&=10-\frac r2-\frac1{8r},&
g_L&=\frac3{8r},&
\Delta&=\frac{(r-1)^2}{2r}.
\end{aligned}
\tag{2}
$$

Here $\Delta$ denotes the paper's $\Delta_T$.
The high-cost preparation threshold is

$$
\tau(r)=\frac{6-g_L}{g_H-g_L}
=\frac{48r-3}{4(20r-r^2-1)}.
\tag{3}
$$

Both $g_H$ and $g_L$ fall strictly in $r$.
Thus $\tau$ rises wherever it lies inside $(0,1)$.
Also $B_r(1/2)=5-r/4+1/(8r)<6$ for $r>1$.

### 2.2 Order slot and separate noise

The order menu is $\{0,1\}$.
One hidden identity occupies a public order opportunity.
An informed investor occupies it with probability $\lambda$.
Otherwise, a liquidity trader buys one unit with probability $\beta$ and abstains otherwise.
The identity, liquidity action, and separate noise are independent of the class and auction primitives.

Separate noise has law

$$
\Pr(Z=-1)=\Pr(Z=1)=\theta,\qquad
\Pr(Z=0)=1-2\theta,
\quad 0<\theta<1/2.
$$

Flow is $X=Q+Z$.
Assume $0<\lambda<1$ and $0<\beta<1$.
The liquidity motive is exogenous, as in the slot construction of T2.
A free uninformed speculator requires a separate incentive model.

Let $\alpha\in[0,1]$ be the class-$H$ purchase probability conditional on an informed identity.
Define

$$
s=\lambda\alpha,\qquad b=(1-\lambda)\beta,
\qquad a=1-2\theta,\qquad d=1-3\theta.
\tag{4}
$$

Thus $s$ is the effective class-$H$ purchase rate.
Full informed purchases mean $s=\lambda$, not $s=1$.
The cost $k$ applies to an actual informed purchase.
An ex ante factor $\lambda$ does not change its conditional action comparison.

### 2.3 Equilibrium, beliefs, and ties

Use perfect Bayesian equilibrium of this finite order game.
An investor deviation faces fixed price and preparation schedules.
Market makers price expected terminal target proceeds.
The challenger sees the price and its cost; prepared bidders bid truthfully.

Bayes' rule determines every feasible flow belief, including under no informed trade.
No claim needs a belief at an unused flow.
The investor may mix at indifference, called IM.
The default challenger prepares at indifference, called C1.
The alternative rule CM permits challenger mixtures at indifference.

The selected informative branch needs IM at its first two reported strengths.
It needs no challenger mixture.
The three Proposition 2 outcomes use strict preferences, so neither tie rule affects them.
These are analogs for the stated buy-only menu, not claims about continuous order sizes.

## 3. Results

### Result 1 — analytical. Every flow is on path, and every posterior is interior

Write $f$ for the separate noise law.
Let $A_x$ be the class-$L$ flow mass after low-class purchases are excluded.
The class-$H$ flow mass is $H_x$:

$$
A_x=(1-b)f(x)+bf(x-1),\qquad
H_x=A_x+s[f(x-1)-f(x)].
\tag{5}
$$

A low-class purchase has payoff

$$
-\Delta\sum_z f(z)e_{1+z}\mu_{1+z}-k<0.
$$

Hence the low class abstains in every equilibrium.
Bayes' rule gives the four posteriors:

$$
\begin{array}{c|c|c|c}
x&A_x&H_x&\mu_x=H_x/(A_x+H_x)\\\hline
-1&(1-b)\theta&(1-b-s)\theta&
\dfrac{1-b-s}{2(1-b)-s}\\[4pt]
0&A_0=a-bd&A_0-sd&\dfrac{A_0-sd}{2A_0-sd}\\[4pt]
1&A_1=\theta+bd&A_1+sd&\dfrac{A_1+sd}{2A_1+sd}\\[4pt]
2&b\theta&(b+s)\theta&\dfrac{b+s}{2b+s}
\end{array}
\tag{6}
$$

Both class probabilities are positive in every row.
For example, $1-b-s\ge(1-\lambda)(1-\beta)>0$ and $b\theta>0$.
The middle rows are sums of positive order and noise masses.
Thus every flow has positive unconditional mass and $0<\mu_x<1$.

The conclusion also holds before the low-class action is excluded.
The common liquidity component is

$$
C_x=(1-\lambda)[(1-\beta)f(x)+\beta f(x-1)]>0
$$

at each feasible flow.
Every strategy adds nonnegative informed mass in each class.
Thus no strategic mixture creates an unused or revealing extreme flow.

### Result 2 — analytical. The top posterior controls all three benchmark outcomes

For $s>0$, each flow likelihood ratio is a weighted average of the two slot likelihood ratios.
These ratios are

$$
\frac{1-b-s}{1-b},\qquad \frac{b+s}{b}.
$$

The top flow attains the larger ratio.
Therefore

$$
\mu_x(s)\le\mu_2(s)\le
M:=\frac{b+\lambda}{2b+\lambda}<1.
\tag{7}
$$

At $r=6/5$, $\Delta=1/60<k$.
A purchase earns at most $\Delta-k=-1/300$, under every candidate schedule.
Consequently, the unique outcome is no informed trade and entry $\rho$.

At $r=3$, every high-class purchase earns at least

$$
\rho\Delta(1-M)-k.
\tag{8}
$$

The same bound applies when the challenger cannot see prices.
If $M<\tau(18/5)$, then

$$
\rho\Delta(3)(1-M)-k
>
\frac16\left(1-\frac{4245}{5804}\right)-\frac1{50}
=\frac{21563}{870600}>0.
\tag{9}
$$

Thus every candidate with partial high-class purchases has a profitable purchase.
The unique high-class action is full purchase, including against mixed candidates.
The bound strengthens at $r=18/5$ because $\Delta$ rises.

The strict parameter strip is

$$
\frac{141}{200}<M<\frac{4245}{5804},
\quad\text{or}\quad
\frac{82}{59}<\frac{\lambda}{(1-\lambda)\beta}<\frac{2686}{1559}.
\tag{10}
$$

At $3$, the top flow then recruits with positive probability.
At $18/5$, no flow recruits the high-cost challenger.
Full purchases still give distinct posteriors, so trade and prices remain informative.
This proves all three Proposition 2 analogs on this strip, for every admissible $\theta$.

The upper restriction is also necessary for a strict Proposition 2(iii) outcome.
Suppose an equilibrium has entry exactly $\rho$ at $18/5$.
Every posterior then lies below $\tau(18/5)$ under C1.
Its purchase return exceeds $\rho\Delta(18/5)[1-\tau(18/5)]>k$.
Hence purchases must be full, so their top posterior is $M<\tau(18/5)$.
The lower restriction then follows from entry above $\rho$ at $3$.
Equality cases depend on the challenger tie rule.

### Result 3 — analytical. Exact scalar equilibrium conditions

Competitive pricing and the entry floor give

$$
P_x=t_0+e_x(t_L-t_0+\Delta\mu_x),\qquad
\mu_x=\frac{P_x-t_0-e(P_x)(t_L-t_0)}{e(P_x)\Delta}.
\tag{11}
$$

Since $e(P_x)\ge\rho>0$, prices reveal the flow posterior.
This argument permits atoms, entry jumps, and challenger mixtures.

A high-class purchase reaches flows $0,1,2$ with probabilities $\theta,a,\theta$.
Its net payoff is $U(s)=\Delta S(s)-k$, where

$$
S(s;e_0,e_1,e_2)=
\frac{\theta e_0A_0}{2A_0-sd}
+\frac{ae_1A_1}{2A_1+sd}
+\frac{\theta e_2b}{2b+s}.
\tag{12}
$$

All feasible order comparisons reduce to this payoff and zero.
Specifically:

- $s=0$ is an equilibrium exactly when $U(0)\le0$.
- $0<s<\lambda$ requires $U(s)=0$ and IM.
- $s=\lambda$ requires $U(\lambda)\ge0$ under IM.
- At a preparation tie, CM also permits a suitable $e_x\in[\rho,1]$.

Under no trade, every posterior equals $1/2$.
Thus $S(0)=\rho/2$ and no trade holds exactly when

$$
\frac{\rho\Delta(r)}2\le k,
\qquad
r\le r_N=\frac{29+6\sqrt6}{25}\approx1.747877538268.
\tag{13}
$$

This condition needs no extreme-flow belief.

When $\theta>1/3$, flow $0$ carries good news and flow $1$ carries bad news.
The top flow reaches the preparation threshold first.
Define $q(r)=(2\tau(r)-1)/(1-\tau(r))$.
The two possible recruitment rates are

$$
s_2^*=bq(r),\qquad
s_0^*=\frac{A_0q(r)}{-d}>s_2^*.
\tag{14}
$$

For $\theta<1/3$, replace the second threshold by $s_1^*=A_1q(r)/d>s_2^*$.
These thresholds and equation (12) permit a direct search over all preparation segments.

### Result 4 — computer-assisted. The selected point gives one ordered branch

At (1),

$$
b=\frac3{11},\quad M=\frac8{11},\quad
(a,d,A_0,A_1)=\left(\frac{29}{100},-\frac{13}{200},\frac{677}{2200},\frac{371}{1100}\right).
\tag{15}
$$

The middle posteriors never recruit over the stated coexistence interval.
Indeed, $\mu_0(\lambda)=742/1419<\tau(3/2)$ and $\mu_1\le1/2$.
Write $S_\rho(s)=S(s;\rho,\rho,\rho)$ and $S_+(s)=S(s;\rho,\rho,1)$.

On either preparation segment,

$$
S''(s)=
\frac{2\theta\rho A_0d^2}{(2A_0-sd)^3}
+\frac{2a\rho A_1d^2}{(2A_1+sd)^3}
+\frac{2\theta e_2b}{(2b+s)^3}>0.
\tag{16}
$$

The exact endpoint derivatives are

$$
S_\rho'(\lambda)=-\frac{53}{2150}<0,\qquad
S_+'(\lambda)=-\frac{7361}{75680}<0.
\tag{17}
$$

Since each derivative increases, each coefficient falls strictly on $[0,\lambda]$.
The purchase payoff therefore falls, jumps upward at $s_2^*$, then falls again.
No roots or mixtures are omitted by this description on the interval under study.

The decisive rational payoff signs are

$$
\begin{aligned}
U_+(s_2^*;31/20)
&=\frac{78642628125838933}{976763725491465440000}>0,\\
U_+(\lambda;8/5)&=-\frac{2407}{30272000}<0,\\
U_+(\lambda;33/20)&=\frac{4001579}{1498464000}>0.
\end{aligned}
\tag{18}
$$

The jump payoff rises strictly on $[3/2,7/4]$.
For $G(r)=\Delta(r)S_+(bq(r))-k$, differentiate to obtain

$$
G'(r)=\Delta'(r)S_+(bq(r))
+\Delta(r)S_+'(bq(r))\frac{b\tau'(r)}{[1-\tau(r)]^2}.
\tag{19}
$$

Exact interval arithmetic gives a positive lower bound throughout this interval; the complete fractions are in `exact_results.txt`.
Thus the positive jump at $1.55$ persists through $r_N$.
The full-purchase payoff rises strictly with $r$ while only the top flow recruits.

There is a unique recruited root $s_A(r)$ until it reaches $\lambda$.
Implicit differentiation gives

$$
\frac{ds_A}{dr}=-\frac{\Delta'(r)S_+(s_A)}{\Delta(r)S_+'(s_A)}>0.
$$

Entry on this branch is

$$
\mathsf E_A(r)=\rho+(1-\rho)\theta\left(b+\frac{s_A(r)}2\right).
\tag{20}
$$

It rises strictly before the full-purchase cutoff and stays constant afterward.
The selected branch has the following exact root enclosures.
Decimal endpoints in this table are rationals, not rounded root estimates.

| $r$ | Effective rate $s_A$ | Exact payoff signs at endpoints | Conditional rate $\alpha_A$ | Entry enclosure or exact value |
|---|---|---|---|---|
| $31/20$ | $[0.231790368476,\ 0.231790368477]$ | $+,-$ | $[0.5099388106472,\ 0.5099388106494]$ | $[0.353470729167,\ 0.353470729168]$ |
| $8/5$ | $[0.447331543809,\ 0.447331543810]$ | $+,-$ | $[0.9841293963798,\ 0.9841293963820]$ | $[0.382164648133,\ 0.382164648134]$ |
| $33/20$ | $5/11$ | Strictly positive full payoff | $1$ | $613/1600=0.383125$ |

The output records the full rational payoff at every endpoint.
Continuity gives existence; equation (17) gives uniqueness on the recruited segment.
The entry intervals are disjoint, which proves the strict order.
The paper's three values are $0.545053<0.548756<0.551361$.
The present values are substantially lower.

The no-trade deviation payoffs at these strengths are

$$
-\frac{387}{49600},\qquad -\frac{19}{3200},\qquad -\frac{211}{52800}.
$$

Thus every reported informative outcome coexists with no trade.
The coexistence interval includes $[r_A,r_N]$, with rational endpoint brackets:

| Threshold | Definition | Rational bracket |
|---|---|---|
| $r_A$ | $\Delta S_+(bq)=k$ | $[1.548628009784,\ 1.548628009785]$ |
| $r_F$ | $\Delta S_+(\lambda)=k$ | $[1.601472912427,\ 1.601472912428]$ |
| $r_N$ | $\rho\Delta/2=k$ | $[1.747877538267,\ 1.747877538268]$ |
| $r_C$ | $B_r(8/11)=6$ | $[3.508905909933,\ 3.508905909934]$ |

Each first three payoff functions has exact signs $-,+$ at its endpoints.
The ceiling function has exact signs $+,-$.
The derivative proof and the closed forms give uniqueness of the relevant roots.
In particular,

$$
r_C=\frac{14+3\sqrt{22}}8.
$$

Under CM, each intermediate strength also has a threshold equilibrium at $s_T=bq(r)$.
Let $e_T$ denote total entry at the top flow.
The investor's indifference condition gives

$$
e_T=\rho+
\frac{k/\Delta-S_\rho(s_T)}{\theta b/(2b+s_T)},\qquad
\zeta_T=\frac{e_T-\rho}{1-\rho}.
\tag{21}
$$

The exact rational $\zeta_T$ values lie in $(0,1)$.
Their decimal displays are $0.991226120$, $0.707936702$, and $0.481888643$.
Their total entry values decrease: $0.351891376>0.323172303>0.300084043$.
They form a separate branch and do not support the upward comparison.
Under C1, only no trade and the selected informative outcome remain at these strengths.

### Result 5 — computer-assisted. An explicit open region preserves the scorecard

Every point in the following box satisfies the same qualitative results:

$$
\boxed{
\left|\lambda-\frac5{11}\right|<\frac1{1000},\qquad
\left|\beta-\frac12\right|<\frac1{1000},\qquad
\left|\theta-\frac{71}{200}\right|<\frac1{2000}.}
\tag{22}
$$

The certificate covers the closed box, which is stronger than the stated open-box claim.
It divides each axis into eight closed cells.
Natural interval arithmetic uses exact rational endpoints on all 512 cells.
The denominators stay positive throughout these cells.

The output retains the complete rational enclosures.
The following conservative rational lower bounds describe the decisive margins:

| Quantity | Positive lower bound throughout the box |
|---|---|
| $M-\tau(3)$ | $21/1000$ |
| $\tau(18/5)-M$ | $29/10000$ |
| $\tau(3/2)-\mu_0(\lambda)$ | $11/100$ |
| $\lambda-s_2^*(33/20)$ | $21/100$ |
| $-S_\rho'(\lambda)$ | $24/1000$ |
| $-S_+'(\lambda)$ | $96/1000$ |
| $U_+(s_2^*;31/20)$ | $47/1000000$ |
| $-U_+(\lambda;8/5)$ | $23/1000000$ |
| $U_+(\lambda;33/20)$ | $26/10000$ |
| $G'(r)$ on $[3/2,7/4]$ | $14/10000$ |

Equations (16)–(20) then prove the same branch order throughout the box.
The branch remains mixed at the first two strengths and full at the third.
The Proposition 2 strip and the welfare argument remain strict there.
Thus no tie in the knobs supports the result.
The small box is a sufficient region, not the maximal feasible region.

### Result 6 — analytical. Price access raises proceeds and net surplus at strength 3

At strength $3$, the prior gives $B_3(1/2)=103/24<6$.
Hidden prices therefore imply entry $\rho$.
Equation (9) forces full purchases in both price regimes, including all mixed candidates.
The liquidity law and every realized order cost therefore coincide across regimes.

Let $w_x=(A_x+H_x)/2$ and let $D$ contain flows with additional preparation.
The paper's welfare identities become finite sums:

$$
\begin{aligned}
\Delta\mathcal R_T
&=(1-\rho)\sum_{x\in D}w_x[t_L-t_0+\Delta\mu_x]>0,\\
\Delta\mathcal W
&=(1-\rho)\sum_{x\in D}w_x[B_3(\mu_x)-6+1/12]>0.
\end{aligned}
\tag{23}
$$

Every additional preparation decision raises target proceeds.
Its conditional allocation gain exceeds its preparation cost by at least $1/12$.
The top flow gives additional preparation with positive probability.
This proves the Proposition A.9 analog throughout the strip, including box (22).

**computer-assisted.** At point (1), the exact gains are

$$
\Delta\mathcal R_T=\frac{17679}{140800}\approx0.125561080,
\qquad
\Delta\mathcal W=\frac{5041}{140800}\approx0.035802557.
$$

### Result 7 — numerical diagnostic. The proposed concentration direction did not succeed on the grid

The search used $u=\lambda/b$ on $1.40:0.02:1.72$.
It used $b=j/[100(1+u)]$, for $j=1,\ldots,99$.
It used $\theta=0.005:0.005:0.495$.
This gives 166,617 parameter points within the strict Proposition 2 strip.

The search enumerates each preparation segment.
Each payoff is strictly convex on a fixed segment.
Its derivative increases, so each segment has at most one minimum and two payoff roots.

The search separates both sides of that minimum before a root calculation.
It retains downward roots and their continuation into full purchases.
Each retained triple uses the same set of flows with extra entry.
This filter excludes threshold outcomes with challenger mixtures.

The grid found 1,345 qualifying branch triples.
None used $\theta<1/3$ or three strictly interior purchase rates.
This is a diagnostic, not a nonexistence proof for either restriction.
The largest entry at $3$ among these triples was about $0.448557$.
That point used approximately $(\lambda,\beta,\theta)=(0.550147,0.711017,0.445)$.
It also gave a smaller final entry gap than point (1).

No exact certificate is claimed for that point.

The limitation is economic as well as quantitative.
At point (1), noise abstains with probability $0.29$ and trades with probability $0.71$.
EGJ's equal weights give abstention $1/3$ and trade $2/3$.
Thus the successful perturbation increases noise activity.
Also $\mu_0>\mu_1$, so the competitive price need not increase with total flow.
Prices still reveal the posterior by equation (11).
The claim in BRIEF §3 about bounded support requires qualification: a same-size liquidity slot removes its revealing-top-flow premise.

## 4. Scorecard

Candidate: buy-only slot, separate noise $(71/200,29/100,71/200)$, with $\lambda=5/11$ and $\beta=1/2$.

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no informed trade at $6/5$; entry $1/4$. | analytical |
| 2. Prop. 2(ii) | Unique full high-class purchases at $3$; entry $613/1600$; high-class ownership $61/275$. | analytical; exact levels computer-assisted |
| 3. Prop. 2(iii) | Unique full high-class purchases at $18/5$; informative prices; entry $1/4$; ceiling $r_C\approx3.508906$. | analytical; exact ceiling bracket computer-assisted |
| 4. Prop. 3 | Coexistence includes $[1.548628010,1.747877538]$; $0.353471<0.382165<0.383125$. First two rates mix; third is full. | computer-assisted |
| 5. Prop. A.9 | Strict gains $17679/140800$ in proceeds and $5041/140800$ in net surplus at $3$. | analytical; exact gains computer-assisted |
| 6. Off-path beliefs | None; all four flows remain on path under every strategy. | analytical |
| 7. Ties and mixtures | IM is essential at $1.55$ and $1.60$; C1 suffices. CM adds the decreasing threshold branch. | analytical; exact fractions computer-assisted |
| 8. Knobs and range | Identity probability, liquidity activity, and separate noise activity; explicit open box (22). | computer-assisted |
| 9. Precedent | EGJ supplies additive three-point noise; Dow–Gorton supplies alternative same-size identities. The exact combination remains unverified. | open for exact publication precedent |
| 10. Evidence | Full derivations, exact root signs, a rational interval cover, and a separate floating-point search. | as stated above |

## 5. Numerical example

At point (1), full purchases give the following flow values at $r=3$:

| Flow | Posterior | Unconditional mass | Entry | Competitive price |
|---|---|---|---|---|
| $-1$ | $3/11$ | $71/400$ | $1/4$ | $203/352$ |
| $0$ | $742/1419$ | $129/400$ | $1/4$ | $84241/136224$ |
| $1$ | $677/1419$ | $129/400$ | $1/4$ | $83201/136224$ |
| $2$ | $8/11$ | $71/400$ | $1$ | $359/264$ |

Only the top flow recruits the high-cost challenger.
Its probability is $71/400$.
Hence entry is $1/4+(3/4)(71/400)=613/1600$.
This is $0.139632$ below the paper's $0.522757$.
High-class ownership is $61/275\approx0.221818$, against the paper's $0.324192$.

The selected strength path is

$$
\frac14\quad\longrightarrow\quad\frac{613}{1600}
\quad\longrightarrow\quad\frac14
\qquad\text{at}\qquad \frac65,\ 3,\ \frac{18}5.
$$

At $3$, the informed purchase earns $33391/340560>0$ net of $k$.
With hidden prices, its net return is $1921/38700>0$.
Target proceeds rise from $59/96$ to $312637/422400$.
Net surplus rises from $245/96$ to $1093123/422400$.

The parameter meanings are separate:

- $\lambda$ is the chance of an informed identity at the opportunity.
- $\beta$ is the liquidity identity's chance of a unit purchase.
- $2\theta$ is the probability of a nonzero separate noise order.

At the selected point, the informed share of executed slot purchases is $5/11$.
Indeed, this share is $(\lambda/2)/(b+\lambda/2)$, and $2b+\lambda=1$ here.
It differs from the informed share of total flow once separate noise is included.
No empirical calibration is claimed.

The literature comparison uses the verified records in [L1, C01 and C09](L1_survey.md).
EGJ uses unit orders and independent equal-weight three-point noise.
The present setup keeps those supports and the competitive price mechanism.
It changes the menu, the noise weights, and the identity structure.

Dow–Gorton (1997), published pages 1095 and 1124–1125, uses mutually exclusive informed and liquidity arrivals with the same size.
Its liquidity trader buys or sells with equal probabilities.
Its informed trader researches and reverses the position at the next date.
Here liquidity buys or abstains, the information probability is fixed, and the trade stage has one opportunity.
Separate additive noise is another departure from that arrival model.
The precise combination in this memo has no verified publication precedent.

### Program use and saved evidence

All files are under `scripts/T5_slot_plus_noise/` in the team folder.
`source_slot.py` copies T2's `exact_analysis.py`.
`source_bounded.py` copies T3's `t3_exact.py`.
The new calculation reuses their auction formulas, rational bisection, and noise constructor.
It forms the combined flow law directly.

Run from the repository root:

```bash
bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh \
  .venv/bin/python \
  audit/microstructure_search_2026_10_22/scripts/T5_slot_plus_noise/exact_analysis.py \
  > audit/microstructure_search_2026_10_22/scripts/T5_slot_plus_noise/exact_results.txt

bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh \
  .venv/bin/python \
  audit/microstructure_search_2026_10_22/scripts/T5_slot_plus_noise/search.py \
  > audit/microstructure_search_2026_10_22/scripts/T5_slot_plus_noise/search.out.txt
```

I ran both interfaces and examined their printed results.
The exact calculation prints flows, prices, payoffs, welfare, root signs, and every region enclosure.
All region margins have positive lower endpoints.
The search output keeps its grid definition, counts, and selected rows.
`run_receipt.json` records the benchmark, pinned source, versions, and hashes of sources and outputs.
At most two calculation slots ran at once.

## 6. Open issues

- **open.** No proof rules out three strictly interior purchase rates at the requested strengths throughout the full parameter domain.
- **open.** The maximal open region and the best achievable entry level remain unknown.
- **numerical diagnostic.** The stated grid found no qualifying branch with concentration toward zero, $\theta<1/3$.
- **open.** The exact mixture of an alternative slot identity and unequal additive noise lacks a verified publication precedent.
- **open.** An endogenous liquidity motive, general priors, dispersed classes, and continuous order sizes require separate analysis.

## 7. Plain summary

A same-size liquidity purchase prevents the top flow from revealing the class.
This permits the three benchmark outcomes with unique informed actions.
Entry is at its floor at strength $1.2$, above its floor at $3$, and back at its floor at $3.6$.
The last outcome retains informative trade.

The point $(5/11,1/2,71/200)$ also supports an informative branch beside no trade at all three intermediate strengths.
Entry rises from $0.353471$ to $0.382165$ to $0.383125$.
The investor mixes at the first two strengths and buys fully at the third.
Exact rational root signs certify the mixed outcomes.
A rational interval calculation certifies an open box around the point.
Price access raises both target proceeds and net surplus at strength $3$.

The gain has limits.
Entry at strength $3$ is $0.383125$, below the paper's $0.522757$.
The successful noise puts slightly more mass on trade than EGJ's equal weights.
It does not concentrate noise toward zero.
Prices also need not increase with total flow.

The grid found no qualifying example with three strictly interior purchase rates.
That stronger requirement remains open.

The setup combines two verified neighboring devices: EGJ's additive three-point noise and Dow–Gorton's alternative same-size arrivals.
Its exact combination remains a new, unverified specification in the permitted literature records.
