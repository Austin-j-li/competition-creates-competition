# Question A: exact enumeration of the three-point model

## 1. Question

Find every equilibrium with equal three-point noise, buy-only orders, uncertain investor presence, and a zero low preparation cost.
Include investor mixtures, challenger mixtures, and both off-path belief rules.
Report the full correspondence, exact boundaries, entry, high-class ownership, and target proceeds.

**Computer-assisted.** The enumeration covers 13,387,500 grid points under each of four conventions.
It also covers 35,392 additional boundary points per convention.
The calculation uses exact rational arithmetic and symbolic families of equilibria.
It does not approximate interior strategies by a grid.

## 2. Setup

### Base model and source

The base model has $Z\in\{-1,0,1\}$, with probability $1/3$ each, and orders $q\in\{0,1\}$.
The investor is present with probability $\lambda$, independently of quality, costs, and noise.
Conditional on presence, its purchase probabilities are $(\beta_H,\beta_L)$.
An absent investor submits zero.

Reading N gives class $H$ prior probability $\pi$.
This exercise uses point masses at $h$ and $\ell$.
The investor sees the class; preparation reveals the value to the challenger.
The challenger sees only the price and its cost.

All calculations use $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, and $c_L=0$.
The maintained domain has $1<r<10$, $0<\pi<1$, $0<\lambda\le1$, $c_H>0$, and $k>0$.
The parameter $\lambda$ denotes presence only.

The paper source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`.
The auction objects match main-text equation (4).
The price identity matches equations (9)–(10).
Online Appendix A.2 confirms the truthful auction implementation.
The source commands were:

```bash
git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:main.tex
git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:online_appendix.tex
```

### Equilibrium and tie rules

An equilibrium consists of investor strategies, a deterministic price for each possible flow, price beliefs, preparation probabilities, and truthful bids.
Prices are competitive conditional expectations.
Investor deviations face the fixed candidate price and preparation schedules.
The enumeration describes schedules on the four flows that some feasible order can reach.
Arbitrary descriptions at other prices do not count as different outcomes.

The low-cost challenger prepares strictly because $g_L>0=c_L$.
At a high-cost preparation tie, it may choose any probability $\sigma(P)\in[0,1]$.
Different prices may use different probabilities, even if their posteriors coincide.
A common price must use one common probability.
The usual enter-at-indifference convention is the subset with $\sigma(P)=1$ at each tie.

The investor follows one of two conventions:

- **Zero:** it chooses zero when a purchase gives zero profit.
- **Any:** it may choose any mixture when a purchase gives zero profit.

The only unused flow after the dominance reduction is $x=2$ under no trade.
Its posterior is one under the **Intuitive-Criterion completion**, abbreviated IC.
Its posterior is $\pi$ under the **passive belief**.
Passive belief fixes the posterior, not an additional preparation choice at a tie.

IC here names the explicit completion $\mu_2=1$.
It does not assert that the criterion alone selects that belief when every type loses from a deviation.

## 3. Results

### 3.1 Auction objects — analytical

Without entry, the incumbent pays $p$ if $R\ge p$:

$$
t_0=\frac1r\int_p^r p\,dR=p(1-p/r).
$$

A high challenger always wins and pays $\max(p,R)$:

$$
t_H=\frac1r\left(\int_0^p p\,dR+\int_p^r R\,dR\right)
=\frac r2+\frac{p^2}{2r},\qquad g_H=h-t_H.
$$

A low challenger induces payment $\max(p,\min(R,\ell))$:

$$
\begin{aligned}
t_L&=\frac1r\left(\int_0^p p\,dR+\int_p^\ell R\,dR+\int_\ell^r\ell\,dR\right)
=\ell-\frac{\ell^2-p^2}{2r},\\
g_L&=\frac1r\left(\int_0^p(\ell-p)\,dR+\int_p^\ell(\ell-R)\,dR\right)
=\frac{\ell^2-p^2}{2r},\\
\Delta_T&=t_H-t_L=\frac{(r-\ell)^2}{2r},\qquad w_L=t_L-t_0>0.
\end{aligned}
$$

Write $B(\mu)=g_L+\mu(g_H-g_L)$ and $\tau=(c_H-g_L)/(g_H-g_L)$.
The entry correspondence is

$$
I(\mu)=
\begin{cases}
\{\rho\},&B(\mu)<c_H,\\
[\rho,1],&B(\mu)=c_H,\\
\{1\},&B(\mu)>c_H.
\end{cases}
\qquad e=\rho+(1-\rho)\sigma.
\tag{1}
$$

### 3.2 Elimination of all low-class purchases — analytical

Let $e_x=e(P(x))$ and let $\mu_x$ denote the flow posterior.
Competitive prices and the independent cost draw imply

$$
P(x)=t_0+e_x(w_L+\Delta_T\mu_x).
$$

The conditional payoff residuals are

$$
V_H(x)-P(x)=e_x\Delta_T(1-\mu_x),\qquad
V_L(x)-P(x)=-e_x\Delta_T\mu_x.
\tag{2}
$$

The second expression is nonpositive at every on-path and completed off-path flow.
A purchase therefore gives class $L$ at most $-k<0$.
Zero gives zero.
Thus every equilibrium has $\beta_L=0$.
This eliminates all pure and interior supports with a positive low-class purchase probability.

### 3.3 Posteriors, price sufficiency, and price partitions — analytical

Before the reduction, conditional flow probabilities are

$$
\Pr(X=x\mid j)=\frac13
\begin{cases}
1-\lambda\beta_j,&x=-1,\\
1,&x=0,1,\\
\lambda\beta_j,&x=2.
\end{cases}
$$

Set $\beta=\beta_H$ after the reduction.
For $\beta>0$,

$$
\begin{aligned}
(\mu_{-1},\mu_0,\mu_1,\mu_2)
&=\left(\frac{\pi(1-\lambda\beta)}{1-\pi\lambda\beta},\pi,\pi,1\right),\\
(\Pr(-1),\Pr(0),\Pr(1),\Pr(2))
&=\frac13(1-\pi\lambda\beta,1,1,\pi\lambda\beta).
\end{aligned}
\tag{3}
$$

Under no trade, the three on-path posteriors equal $\pi$.
The specified completion supplies the fourth posterior.

The entry floor permits inversion:

$$
\mu_x=\frac{P(x)-t_0-e(P(x))w_L}{e(P(x))\Delta_T}.
\tag{4}
$$

Thus one price cannot combine distinct posteriors.
At two distinct posteriors $u<v$, optimal preparation gives $e_u\le e_v$.
Consequently,

$$
P_v-P_u=e_v\Delta_T(v-u)+(e_v-e_u)(w_L+\Delta_Tu)>0.
\tag{5}
$$

At one posterior, different entry probabilities give different prices because $w_L+\Delta_Tu>0$.
Therefore equal posteriors need not imply equal prices at a preparation tie.
This distinction matters for completeness.

For positive trade, the two middle flows share one price unless $B(\pi)=c_H$.
At that equality, they may share a price or use two prices.
Under no trade and a prior tie, the three on-path flows admit up to five price partitions.
Passive completion can add a fourth equal-posterior flow, with up to fifteen partitions.
The investor inequalities can exclude some of these partitions at boundary costs.

### 3.4 Complete equilibrium correspondence as exact families — analytical

For each proposed $\beta$, set $\mu$ by equation (3) and the specified completion.
Choose one rate $e_x\in I(\mu_x)$ for each flow.
Set its price through the competitive price identity.
Equation (5) prevents a price collision between distinct posteriors.
Within one posterior, identical rates give identical prices and one common preparation probability.

For $\beta>0$, a purchase reaches $0,1,2$ with probability $1/3$ each.
Its gross profit is

$$
G=\frac{\Delta_T(1-\pi)}3(e_0+e_1).
\tag{6}
$$

The term at flow two vanishes because $\mu_2=1$.
Neither $\beta$ nor $\lambda$ appears in equation (6).

The complete positive-trade conditions are:

| Investor support | Zero convention | Any convention |
|---|---|---|
| $\beta=1$ | $G>k$ | $G\ge k$ |
| $0<\beta<1$ | excluded | $G=k$ |

For no trade, let $v=1$ under IC and $v=\pi$ under passive belief.
The gross deviation profit is

$$
G_N=\frac{\Delta_T}3\left[(1-\pi)(e_0+e_1)+(1-v)e_2\right].
\tag{7}
$$

No trade is an equilibrium under either investor convention exactly when $G_N\le k$.
Its rate at flow minus one does not affect a purchase deviation.

Equations (1), (3), and (6)–(7) are a complete set description, including all challenger mixtures.
Necessity follows from dominance, Bayes' rule, optimal preparation, and the investor's two actions.
For sufficiency, construct prices from the chosen rates.
Equation (5) and equal-posterior rate consistency give valid price beliefs.
Equation (1) makes preparation optimal.
Equations (6)–(7) make the investor's prescribed support optimal.
Truthful bids implement the auction payoffs.
No further equilibrium conditions remain.

### 3.5 Generic prior: exact trade and nonexistence intervals — analytical

Suppose $B(\pi)\ne c_H$ and let $\bar e$ be its unique entry rate.
Define

$$
K=\frac23\bar e(1-\pi)\Delta_T,
\qquad N=\bar e(1-\pi)\Delta_T=\frac32K.
\tag{8}
$$

Then $e_0=e_1=\bar e$.
The complete investor correspondence is:

| Belief | Investor tie | $k<K$ | $k=K$ | $K<k<N$ | $k\ge N$ |
|---|---|---|---|---|---|
| IC | zero | $\{1\}$ | $\{0\}$ | $\{0\}$ | $\{0\}$ |
| IC | any | $\{1\}$ | $[0,1]$ | $\{0\}$ | $\{0\}$ |
| passive | zero | $\{1\}$ | empty | empty | $\{0\}$ |
| passive | any | $\{1\}$ | $(0,1]$ | empty | $\{0\}$ |

Each entry lists $\beta_H$; $\beta_L=0$ throughout.
Rates at a lower-flow or top-flow preparation tie remain free under equation (1).
Thus a singleton investor strategy need not imply a unique preparation schedule.

Under IC, an equilibrium exists for every maintained parameter vector.
At a generic prior, passive beliefs produce a genuine gap.
Challenger mixtures cannot repair this gap because the middle-flow rates are fixed.

In the intended region $B(\pi)<c_H$, equation (8) reduces to

$$
\boxed{K=\frac23\rho(1-\pi)\Delta_T.}
\tag{9}
$$

Outside that region, replace $\rho$ by one if $B(\pi)>c_H$.
A formula with $\rho$ alone is not a global characterization over the requested cost grid.

### 3.6 Prior ties and all challenger mixtures — analytical

Suppose $B(\pi)=c_H$.
Define

$$
A=\frac23(1-\pi)\Delta_T,\qquad K_{\min}=\rho A,\qquad K_{\max}=A.
$$

For every $\beta>0$, $\mu_{-1}<\pi<1$.
Therefore $e_{-1}=\rho$, $e_2=1$, and $e_0,e_1\in[\rho,1]$.
An interior investor mixture requires

$$
e_0+e_1=\frac{3k}{\Delta_T(1-\pi)},\qquad
\sigma_0+\sigma_1=
\frac{3k/[\Delta_T(1-\pi)]-2\rho}{1-\rho}.
\tag{10}
$$

This equation has a solution exactly when $K_{\min}\le k\le K_{\max}$.
Every $\beta\in(0,1)$ then qualifies under the any convention.
Equation (10), with each $\sigma_i\in[0,1]$, retains every possible split between the two prices.

Full purchases exist if $k<K_{\max}$ under zero, or $k\le K_{\max}$ under any.
Their rates must also satisfy equation (6) with the appropriate strict or weak inequality.

Under IC, no trade exists if $k\ge K_{\min}$.
Under passive belief, no trade exists if $k\ge3K_{\min}/2$.
These conditions follow from the minimum of the rate box in equation (7).
No-trade rates remain subject to equation (7), rather than a common-rate restriction.

With $\rho=1/4$, passive no trade starts below $K_{\max}$.
Thus both belief rules admit coexistence at a prior tie.
Under zero, IC permits both pure investor strategies for $k\in[K_{\min},K_{\max})$.
Under any, the upper endpoint also qualifies.
For passive belief, replace the lower coexistence endpoint by $3K_{\min}/2$.

This coexistence occurs on the equality surface $B(\pi)=c_H$.
It is not an open set of all primitives and does not reproduce the paper's Proposition 3.
It does refute an unrestricted statement that the three-point model never has coexistence.

For the lower flow, the only additional interior boundary is

$$
\boxed{\beta_*=
\frac{\pi-\tau}{\pi\lambda(1-\tau)}}.
\tag{11}
$$

To derive it, multiply $\mu_{-1}=\tau$ by $1-\pi\lambda\beta$:

$$
\pi-\pi\lambda\beta=\tau-\tau\pi\lambda\beta,
\qquad \pi-\tau=\pi\lambda\beta(1-\tau).
$$

If $0<\tau<\pi$, the lower rate is one below $\beta_*$ and $\rho$ above it.
At a feasible $\beta_*$, every $\sigma_{-1}\in[0,1]$ is available.
The solver retains this point even when its investor strategy is interior.
If $g_H=c_H$, every $\sigma_2\in[0,1]$ is available at the top flow.
Neither lower-flow nor top-flow mixtures affect equation (6).

### 3.7 Boundaries in incumbent strength — analytical

Within a region with fixed prior entry $\bar e$, solve $\Delta_T=d$:

$$
r^2-2(\ell+d)r+\ell^2=0,
\qquad \mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}.
$$

The IC trade boundary and passive no-trade boundary are

$$
r_T=\mathfrak r\!\left(\frac{3k}{2\bar e(1-\pi)}\right),
\qquad
r_N=\mathfrak r\!\left(\frac{k}{\bar e(1-\pi)}\right).
\tag{12}
$$

These are local formulas until a prior-entry boundary changes $\bar e$.
For a fixed posterior $u>0$, the equation $B_r(u)=c_H$ is

$$
u r^2-2(uh-c_H)r-[(1-u)\ell^2-p^2]=0.
$$

Its relevant root is

$$
r_C(u)=
\frac{uh-c_H+\sqrt{(uh-c_H)^2+u[(1-u)\ell^2-p^2]}}u.
\tag{13}
$$

Set $u=\pi$ for a prior boundary.
Set $u=1$ for the ceiling after full revelation.
For full purchases, use $u=\pi(1-\lambda)/(1-\pi\lambda)$ for the lower-flow boundary.
If $u=0$, use $g_L=c_H$ directly.
All reported roots must also lie in $1<r<10$.

For $k=1/50$, $\pi=1/2$, and $\bar e=1/4$,

$$
r_T=\frac{31+4\sqrt{21}}{25}=1.973212111193\ldots,
\qquad
r_N=\frac{29+6\sqrt6}{25}=1.747877538268\ldots.
$$

The revealed-quality ceiling is $r_C(1)=10-c_H+\sqrt{(10-c_H)^2-1/4}$:

| $c_H$ | Exact boundary | Decimal | Within $1<r<10$? |
|---:|---|---:|---|
| 4 | $6+\sqrt{143}/2$ | 11.979130372 | no |
| 5 | $5+3\sqrt{11}/2$ | 9.974937186 | yes; above the grid |
| 6 | $4+3\sqrt7/2$ | 7.968626967 | yes |
| 7 | $3+\sqrt{35}/2$ | 5.958039892 | yes |
| 8 | $2+\sqrt{15}/2$ | 3.936491673 | yes |

The prior boundaries inside the maintained domain are:

| $\pi$ | $c_H$ | Exact boundary | Decimal |
|---:|---:|---|---:|
| $1/2$ | 4 | $2+3\sqrt2/2$ | 4.121320344 |
| $2/3$ | 4 | $4+\sqrt{258}/4$ | 8.015594601 |
| $2/3$ | 5 | $5/2+\sqrt{102}/4$ | 5.024876235 |
| $2/3$ | 6 | $1+3\sqrt2/4$ | 2.060660172 |

The other requested prior–cost pairs have no prior boundary in this domain.
These roots are irrational, so the rational strength grid does not land on a prior tie.
Section 5 includes a separate rational tie case.

### 3.8 Entry, ownership, and proceeds for every family — analytical

Let $s=e_0+e_1$.
Conditional preparation probabilities are

$$
\bar e_H=\frac{(1-\lambda\beta)e_{-1}+s+\lambda\beta e_2}{3},
\qquad
\bar e_L=\frac{e_{-1}+s}{3}.
$$

It follows that

$$
\boxed{\begin{aligned}
\mathsf E&=\frac{(1-\pi\lambda\beta)e_{-1}+s+\pi\lambda\beta e_2}{3},\\
\mathsf O_H&=\frac\pi3[(1-\lambda\beta)e_{-1}+s+\lambda\beta e_2],\\
\mathcal R_T&=t_0+\mathsf O_H(t_H-t_0)
 +(\mathsf E-\mathsf O_H)(t_L-t_0).
\end{aligned}}
\tag{14}
$$

The high challenger always wins after preparation because $h>r$.
Thus $\mathsf O_H$ counts high-class challenger ownership, not incumbent ownership.
Equation (14) also holds at $\beta=0$, where the top rate has zero probability mass.

In the main recruitment region $B(\pi)<c_H<g_H$,

$$
\begin{aligned}
\mathsf E&=\rho+\frac{\pi\lambda\beta}{3}(1-\rho),\\
\mathsf O_H&=\pi\rho+\frac{\pi\lambda\beta}{3}(1-\rho),\\
\mathcal R_T&=t_0+\rho[w_L+\pi\Delta_T]
 +\frac{\pi\lambda\beta}{3}(1-\rho)(t_H-t_0).
\end{aligned}
\tag{15}
$$

Presence scales the outcome increment but does not move the trade cutoff.
At $c_H=g_H$, multiply each increment in equation (15) by $\sigma_2$.
Above that cost, every increment is zero.

### 3.9 Exhaustiveness and exact computation — computer-assisted

The support argument starts from nine combinations: zero, interior, or one for each class.
The dominance proof removes six combinations and leaves three high-class supports.
It then divides the positive interval at every feasible root in equation (11).
Each remaining interval or point has constant preparation-rate bounds.
The no-trade point is separate because its off-path belief changes equation (7).

For each support cell, the solver intersects a rational rate box with one linear investor condition.
It solves an interior indifference equation exactly through equation (10), or its fixed-rate special case.
It never substitutes a strategy grid for an indifference equation.

The solver also enumerates all fifteen partitions of four flows.
A partition with distinct posteriors in one block fails equation (4).
A surviving block must use one entry rate.
The solver adds the investor coefficients within each block and solves the reduced rate box.

For a box intersected with one half-space or hyperplane, each vertex is a box vertex or a hyperplane intersection with an edge.
The implementation constructs these vertices with rational arithmetic.
Two equal-posterior blocks must not be forced to use the same rate at every vertex.
Otherwise they are one price block, not two.
If no pair is forced equal, finitely many equality hyperplanes cannot cover the feasible relative interior.
A feasible schedule with all required distinct prices therefore exists.
Strict investor conditions use the open half-space and require its maximum to exceed $k$.

This argument supplies an exhaustive finite procedure for every rational input in the maintained domain.
Equations (1)–(14) also cover irrational parameter boundaries symbolically.
The finite grid supports the classification; the completeness claim does not rest on the grid.

The grid is:

- $\lambda\in\{1,19/20,9/10,4/5,3/5,2/5,1/5\}$.
- $\pi\in\{1/2,1/3,2/3\}$.
- $c_H\in\{4,5,6,7,8\}$.
- $r=n/20$, $n=21,\ldots,190$: 170 strengths from 1.05 through 9.5.
- $k=n/1000$, $n=1,\ldots,500$; and $k=n/100$, $n=51,\ldots,300$: 750 costs.
- Extra costs at every distinct $K_{\min},K_{\max},3K_{\min}/2,3K_{\max}/2$.

The solver evaluates exact parameter cells and counts their grid intersections.
It retains each continuum as a family.
It does not save millions of repeated rows.

| Convention | Base cases | No equilibrium | Multiple equilibria | Unique equilibrium |
|---|---:|---:|---:|---:|
| IC, zero | 13,387,500 | 0 | 0 | 13,387,500 |
| IC, any | 13,387,500 | 0 | 196 | 13,387,304 |
| passive, zero | 13,387,500 | 1,332,674 | 0 | 12,054,826 |
| passive, any | 13,387,500 | 1,332,478 | 196 | 12,054,826 |

Each convention adds 35,392 boundary cases absent from the base grid.
Their results are:

| Convention | Additional cases | No equilibrium | Multiple equilibria | Unique equilibrium |
|---|---:|---:|---:|---:|
| IC, zero | 35,392 | 0 | 0 | 35,392 |
| IC, any | 35,392 | 0 | 17,654 | 17,738 |
| passive, zero | 35,392 | 17,654 | 0 | 17,738 |
| passive, any | 35,392 | 0 | 17,654 | 17,738 |

The combined coverage is 53,691,568 parameter–convention cases.
These are distinct after the extra cost points are deduplicated within each parameter vector.
There are 88,760 nonempty cost cells before the four conventions.

Every multiple case in these grids contains an investor continuum at $k=K$.
Of these, 59 base cases and 1,731 added cases also contain a lower-flow challenger continuum.
Those counts apply to each any convention and overlap the investor-continuum count.
The rational grid contains no prior or top preparation equality.
The separate examples cover both missing equality types.

Files under `scripts/A_bruteforce/` provide the complete compact result:

| File | Content |
|---|---|
| `solver.py` | Exact correspondence for any supplied rational input; price partitions and outcome ranges |
| `scan.py` | Exact support-cell sweep and grid counts |
| `cutoffs.csv` | 2,550 strength–prior–cost records; exact cutoffs and lower-flow threshold products |
| `summary.csv` | Counts by presence, prior, cost, belief, investor tie, and grid |
| `aggregate.csv` | The two count tables above |
| `outcome_catalog.py` | Exact pure-profile outcome calculation |
| `outcomes.csv` | 35,700 no-trade or full-purchase profile records across every strength and requested parameter triple |
| `benchmark.csv` | The benchmark at all seven presence probabilities and four conventions |
| `boundary_examples.json` | Full symbolic families for selected cutoff and preparation-tie cases |
| `selected_outcomes.json` | Explicit rational interior schedules and their actual prices |
| `manifest.json`, `outcome_manifest.json` | Inputs, method, file sizes, and output hashes |

Use the cutoffs to select which pure-profile rows are equilibria.
The outcome catalog does not label every pure profile as an equilibrium.
For interior profiles, equation (14) and the exact family constraints give the entire outcome set.
The command output reports closure ranges; an open strategy endpoint need not attain its range endpoint.

## 4. What it recovers or loses relative to the Laplace paper

The table concerns the pinned paper and this exercise's specified domain.
A source comparison does not constitute an independent proof of an extension outside that domain.

| Paper result | Verdict | Reason and scope |
|---|---|---|
| Proposition 1 | survives | **Analytical.** $\Delta_T'=1/2-\ell^2/(2r^2)>0$; $g_H',g_L'<0$. The auction opposition is unchanged. |
| Proposition 2(i) | changes | **Analytical.** The exact no-trade cutoff is equation (8), with a required off-path completion. |
| Proposition 2(ii) | survives in adapted form | **Analytical.** Full purchases replace two-sided full orders. Equations (9) and (15) give the entry and ownership rise. |
| Proposition 2(iii) | changes | **Analytical.** The relevant ceiling is $g_H<c_H$, since a purchase reveals $H$ at the top flow. |
| Proposition 3 | dies as an open-region mechanism | **Analytical.** Generic purchase profit is independent of $\beta$. Boundary continua and prior-tie coexistence remain. |
| Proposition A.3 | survives | **Analytical.** At fixed posterior, both gross profits decrease with $r$. A positive-cost threshold can only remove preparation. |
| Proposition A.4 | changes | **Analytical.** Equations (8), (12), and (13) replace the three continuous-noise thresholds. |
| Proposition A.5 | not applicable | The logistic-noise theorem concerns a different noise law and order menu. |
| Proposition A.6 | changes | The same residual calculation extends to a cost distribution if its entry floor remains positive. Its continuous-order proof is unnecessary here. |
| Proposition A.7 | not applicable | Complementary private signals are absent from this exercise. |
| Proposition A.8 | survives at the auction stage | Its payment-rule comparison does not use noise. This solver retains the second-price institution only. |
| Proposition A.9 | survives in the recruitment region | **Analytical.** The matched-profile gain appears below. |
| Proposition A.10 | excluded in this domain | **Analytical.** The positive entry floor rules out a shared price for distinct flow posteriors. |
| Section 5.1 | changes | The finite noise law has zero-probability flows and exact revelation. Smooth density bounds do not apply. |
| Section 5.2 | not evaluated beyond point masses | The auction formulas retain $h,\ell$ symbolically, but the requested grid fixes their values. |
| Section 5.3 | not applicable | No additional private signal enters the specified model. |
| Section 6.1 | survives with smaller effects | Equation (15) gives proceeds. The gain in net acquisition surplus is below. |
| Section 6.2 | outside the fixed institution | The payment rule remains a cash second-price auction. |
| Section 6.3 | outside the fixed reserve | The enumeration keeps $p=1/2<\ell$ and does not establish reserve-choice results. |

For A.3, preparation ties require a consistent selection when the gross profit stays unchanged.
Here both gross profits decrease strictly with $r$ on the maintained domain, so the fixed-belief comparison is strict before threshold selection.

For A.9, suppose $B(\pi)<c_H<g_H$ and $k<K$.
Hidden prices give entry $\rho$ and the same full-purchase investor strategy.
Price access adds preparation only at $x=2$, which has probability $\pi\lambda/3$.
Hence

$$
\Delta\mathcal R_T=\frac{(1-\rho)\pi\lambda}{3}(t_H-t_0)>0,
\qquad
\Delta\mathcal W=\frac{(1-\rho)\pi\lambda}{3}
\left(g_H-c_H+\frac{p^2}{r}\right)>0.
\tag{16}
$$

The welfare increment equals expected allocation value less the extra preparation cost.
The term $p^2/r$ accounts for the no-sale event without an admissible incumbent.
The investor uses the same order in both economies, so its resource cost cancels.

The imposed buy-only menu cannot establish endogenous buy–sell asymmetry.
It removes the sale decision from the game.
The middle flows remain at the prior, but the lower flow can have a partially informative posterior.
Thus “all-or-nothing information” needs a pure-profile and presence qualification.

## 5. Numerical example

### 5.1 Benchmark and presence — computer-assisted

At $c_H=6$, $k=1/50$, $\pi=1/2$, and $\lambda=1$, all four conventions give:

| $r$ | $\beta_H$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ |
|---:|---:|---:|---:|---:|
| $6/5$ | 0 | $1/4$ | $1/8$ | $377/960$ |
| 3 | 1 | $3/8$ | $1/4$ | $145/192$ |
| $18/5$ | 1 | $3/8$ | $1/4$ | $4837/5760$ |

The ceiling occurs at $4+3\sqrt7/2$, not at $18/5$.
At that ceiling, top-flow challenger mixtures span the return from $3/8$ to $1/4$.
Above it, entry equals $1/4$.

At $r=3$, the exact presence table is:

| $\lambda$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ |
|---:|---:|---:|---:|
| 1 | $3/8$ | $1/4$ | $145/192$ |
| $19/20$ | $59/160$ | $39/160$ | $2873/3840$ |
| $9/10$ | $29/80$ | $19/80$ | $1423/1920$ |
| $4/5$ | $7/20$ | $9/40$ | $349/480$ |
| $3/5$ | $13/40$ | $1/5$ | $671/960$ |
| $2/5$ | $3/10$ | $7/40$ | $161/240$ |
| $1/5$ | $11/40$ | $3/20$ | $617/960$ |

Every row has the same cutoff $K=1/18$.
Presence affects outcomes through the top-flow probability.

### 5.2 Passive nonexistence and an investor continuum — computer-assisted

At $r=9/5$, $c_H=6$, $\pi=1/2$, and $k=1/50$,

$$
K=\frac{2}{135}<\frac1{50}<\frac1{45}=N.
$$

IC admits no trade.
Passive belief admits no equilibrium under either investor convention.
This holds for every requested presence probability.

At $r=3$, $c_H=6$, and $k=1/18$, IC with any permits $\beta\in[0,1]$.
Passive with any permits $\beta\in(0,1]$.
For $\lambda=1$ and $\pi=1/2$,

$$
\mathsf E=\frac14+\frac\beta8,\quad
\mathsf O_H=\frac18+\frac\beta8,\quad
\mathcal R_T=\frac{59}{96}+\frac{9\beta}{64}.
$$

For example, $\beta=1/2$ gives $(\mathsf E,\mathsf O_H,\mathcal R_T)=(5/16,3/16,263/384)$.

### 5.3 Exact interior strategy with challenger indifference — computer-assisted

Use requested grid values $r=3$, $c_H=4$, $\pi=2/3$, and $\lambda=3/5$.
Use the added boundary cost $k=4/27$.
Then

$$
\tau=\frac{93}{200},\qquad
\lambda\beta_*=\frac{121}{214},\qquad
\beta_*=\frac{605}{642}.
$$

The high investor is indifferent because $K=4/27$.
The high-cost challenger is indifferent at the lower price.
For $\sigma_{-1}=1/2$, the exact schedule gives

$$
(e_{-1},e_0,e_1,e_2)=(5/8,1,1,1),
$$

$$
(P_{-1},P_0,P_1,P_2)=(287/320,95/72,95/72,37/24),
$$

$$
(\mathsf E,\mathsf O_H,\mathcal R_T)
=\left(\frac{296}{321},\frac{1619}{2568},\frac{1213}{963}\right).
$$

The solver retains every $\sigma_{-1}\in[0,1]$, not only this displayed choice.
It also retains all other positive investor mixtures at this cost.
The zero convention excludes these interior investor mixtures.

### 5.4 Prior indifference: coexistence and distinct middle prices — computer-assisted

This supplemental case sets $c_H=103/24$, outside the five-cost grid, to hit the prior equality exactly.
Keep $r=3$, $\pi=1/2$, $\lambda=1$, and $k=1/10$.
Then

$$
B(\pi)=\frac{103}{24}=c_H,\quad
K_{\min}=\frac1{18},\quad K_{\max}=\frac29,\quad
\frac32K_{\min}=\frac1{12}.
$$

Both no trade and full purchases exist under either belief rule, even with the zero convention.
For no trade, choose every prior-posterior rate as $1/4$.
Under IC the off-path top rate is one; under passive belief choose its rate as $1/4$.
The deviation gross profits are $1/18$ and $1/12$, both below $1/10$.

For full purchases, choose $e_{-1}=1/4$ and $e_0=e_1=e_2=1$.
The purchase gross profit is $2/9>1/10$.
The two pure outcomes are

$$
\begin{array}{c|ccc}
&\mathsf E&\mathsf O_H&\mathcal R_T\\\hline
\text{no trade}&1/4&1/8&59/96\\
\text{full purchases}&7/8&1/2&221/192
\end{array}
$$

Under any, choose $\beta=1/2$ and rates $(1/4,1/4,13/20,1)$.
Equation (10) holds because $1/4+13/20=9/10$.
The two middle posteriors equal $1/2$, but their prices are

$$
P_0=\frac{59}{96},\qquad P_1=\frac{149}{160}.
$$

The full price partition consists of four singleton flows.
The resulting outcomes are

$$
(\mathsf E,\mathsf O_H,\mathcal R_T)=(107/240,61/240,4553/5760).
$$

This explicit case rules out an enumeration that forces equal prices at equal posteriors.

### 5.5 Top indifference and a global cutoff qualification — computer-assisted

A second supplemental cost, $c_H=203/24=g_H(3)$, makes the top challenger indifferent.
At the benchmark trading cost, full purchases remain strict.
With $\sigma_2=1/2$, outcomes equal $(5/16,3/16,263/384)$.
Every $\sigma_2\in[0,1]$ is an equilibrium choice.

Within the requested cost grid, take $c_H=4$, $\pi=1/2$, and $k=1/5$ under IC.
At $r=3$, the prior supports full entry and $K=2/9>k$, so purchases are full.
At $r=5$, prior entry is $1/4$ and $K=2/15<k$, so there is no trade.
At $r=7$, $K=3/14>k$, so purchases are full again.
The prior-entry change therefore prevents a single global monotone trade cutoff.

### 5.6 Commands and observed output

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_bruteforce/scan.py
PYTHONDONTWRITEBYTECODE=1 bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_bruteforce/outcome_catalog.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_bruteforce/solver.py --r 3 --k 1/18 --belief passive --investor-tie any
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_bruteforce/solver.py --r 3 --k 1/10 --c-H 103/24 --belief IC --investor-tie zero
```

The first two commands produced the saved catalogs and count tables.
The script folder occupies about 2.5 MB, below the 20 MB limit.
The third returned the open interior family and the full-purchase endpoint, with no no-trade family.
The fourth returned both strict pure investor outcomes and their admissible preparation-rate sets.
The scripts print economic outputs and contain no assertions.

## 6. Open issues

**Open.** The paired memo `A_three_point.md` did not exist at the comparison check.
The final file check occurred on 21 October 2026 at 18:05 UTC.
The exact comparison targets below permit a later line-by-line reconciliation.

The classification assumes deterministic price schedules, as in the specified price-function equilibrium.
It does not add random price lotteries conditional on a fixed flow.
The finite correspondence excludes irrelevant descriptions at unreachable prices.

The rational strength grid misses irrational preparation boundaries.
Equations (10)–(13) cover them analytically.
The extra rational examples exercise the same equality conditions with an adjusted cost or presence probability.
They are clearly separate from the requested parameter grid.

**Open.** This exercise does not determine equilibria under unequal noise, two-sided orders, private buyer signals, or reserve choice.
It establishes no literature claim beyond the local sources and pinned paper cited above.

### Comparison targets

| Claim to compare | Exact target and concrete case |
|---|---|
| Low-class strategy | $\beta_L=0$ for every maintained parameter vector |
| General-prior cutoff | $K=(2/3)\bar e(1-\pi)\Delta_T$; at $r=3,c_H=6,\pi=1/2$, $K=1/18$ |
| Presence effect on cutoff | None; all seven requested presence values give $K=1/18$ in that case |
| Passive no-trade boundary | $N=3K/2$; at $r=3$, $N=1/12$ |
| Passive failure | At $r=9/5,k=1/50,c_H=6$, no equilibrium under either investor tie |
| Investor mixtures | IC: $[0,1]$ at $k=K$; passive: $(0,1]$ |
| Benchmark levels | At $r=3$: $(3/8,1/4,145/192)$ for entry, ownership, proceeds |
| Benchmark return | $r=4+3\sqrt7/2=7.9686269666\ldots$; entry remains $3/8$ at $r=18/5$ |
| Lower-flow challenger mixture | $r=3,c_H=4,\pi=2/3,\lambda=3/5,k=4/27$: $\beta_*=605/642$ |
| Price versus posterior | At $c_H=103/24,r=3,k=1/10$, equal middle posteriors admit $P_0=59/96\ne149/160=P_1$ |
| Coexistence qualification | At that prior tie, strict no trade and strict full purchases coexist |
| Single-cutoff qualification | $c_H=4,k=1/5$: full at $r=3$, zero at $r=5$, full at $r=7$ |
| Base-grid counts | 13,387,500 points per convention; passive failures 1,332,674 under zero and 1,332,478 under any |

## 7. Plain summary

Equal three-point noise permits a complete exact solution.
The low-class investor never buys.
Positive purchases reveal the high class at the top flow.
The middle flows retain the prior.
The investor earns its gross profit at those middle flows only.

Away from a prior preparation tie, one cutoff determines positive trade.
That cutoff does not depend on investor presence.
Presence instead changes the probability of the revealing flow and the size of the entry effect.

The off-path belief matters for existence.
The Intuitive-Criterion completion always supports an equilibrium.
Passive belief creates a cost interval with no equilibrium.
Investor mixtures fill the trade-cutoff point under the any convention, but they do not fill the open gap.

Challenger ties require separate care.
They permit continuous preparation choices at the lower or top flow.
A prior tie also permits distinct prices at the same posterior.
At that equality, no trade and full purchases can coexist even when investor ties select zero.
This does not restore the paper's coexistence on an open set of primitives.

The exact sweep represents over 53 million parameter–convention cases through compact families.
The saved output includes all requested priors, presence probabilities, costs, and strengths.
The benchmark entry rise is $1/4$ to $3/8$.
Its return to $1/4$ occurs near $r=7.97$, rather than at $r=3.6$.
