# T4: One-sided noise and buy-only orders

## 1. Question

Can one-sided noise preserve an interior posterior at the flow that recruits entry?
**analytical:** Yes. D1 and D2 recover all three benchmark outcomes, but lose Proposition 3's upward triple.
They share T2 V3's conditional payoff function after a parameter match, with different signal probabilities and ownership.

Sources: the paper's Sections 2–4 and Online Appendix A.9 at `overleaf/paper` commit `01bd5d6`;
`L2_taxonomy.md`, G1–G8 and short-list item 2; `T2_liquidity_trader.md`, Sections 3.3–3.10;
`audit/discrete_exploration_2026_10_21/memos/B_dlaplace_theory.md`, Results 1–8 (B2);
and `audit/alex_meeting_2026_10_21/memos/LIT_extracts.md`, A6.
The last record verifies Edmans (2009); this memo uses that record, without a new source retrieval.

## 2. Setup

D1 permits $q\in\{0,1\}$ and $X=q+G$, with $\Pr(G=n)=(1-a)a^n$, $n\ge0$, $0<a<1$.
D2 keeps that menu and uses $X=q+u$, with density $\eta e^{-\eta u}$ on $u>0$; set $a=e^{-\eta}$.
D3 permits $q\in\{-1,0\}$ with the same exponential noise. Its discrete counterpart gives the same formulas.
The investor is always present. The optional presence extension is outside this memo.

Use Reading N, the stated point-mass benchmark, and $c_L=0$.
The equilibrium is perfect Bayesian equilibrium with truthful bids and competitive prices.
A deviation faces fixed price and entry schedules.
The default investor rule permits any mixture at indifference (IM).
The default challenger rule requires preparation at indifference (C1).
Alternatives are zero investor orders at indifference (I0), and arbitrary challenger mixtures at indifference (CM).

Write $\Delta=t_H-t_L$, $\tau=(6-g_L)/(g_H-g_L)$, and $w_L=t_L-t_0$.
Equation (4) of the pinned paper confirms every auction formula in TEAM_RULES §3.
At any posterior, its equations (9)–(11) give

$$
e=\rho+(1-\rho)\mathbf1\{\mu\ge\tau\},\quad
P=t_0+e(w_L+\Delta\mu),\quad
V_H-P=e\Delta(1-\mu),\quad V_L-P=-e\Delta\mu.
$$

Since $e\ge\rho>0$, the identity $\mu=(P-t_0-ew_L)/(e\Delta)$ makes the posterior recoverable from price.
Thus the challenger can use the flow posterior without direct access to flow.
Under CM, replace the indicator by the high-cost preparation probability.
All upper-region entry rates below can be conditional averages if indifferent preparation varies within a posterior plateau.

## 3. Results

### 3.1 D1 and D2: every strategy and every flow — analytical

Let $s_j$ be the purchase probability in class $j$, and put $b_j=a+(1-a)s_j$.
For D1,

$$
f_j(0)=(1-a)(1-s_j),\qquad
f_j(n)=(1-a)a^{n-1}b_j\quad(n\ge1).
$$

Bayes' rule therefore gives, for any prior $\pi$,

$$
\mu_0=\frac{\pi(1-s_H)}{\pi(1-s_H)+(1-\pi)(1-s_L)},\qquad
\mu_+=\frac{\pi b_H}{\pi b_H+(1-\pi)b_L}.
\tag{1}
$$

For D2, the densities are $\eta e^{-\eta x}(1-s_j)$ on $0<x\le1$ and
$\eta e^{-\eta x}b_j/a$ on $x>1$.
Their region probabilities are $(1-a)(1-s_j)$ and $b_j$.
Thus (1), the signal experiment, and every order payoff coincide with D1.
Boundary points have zero probability. The integer part of exponential noise also has D1's geometric law.

At $\pi=1/2$, all four pure profiles are:

| $(s_H,s_L)$ | Low-region posterior | Upper-region posterior |
|---|---|---|
| $(0,0)$ | $1/2$ | $1/2$ |
| $(1,0)$ | $0$ | $M=1/(1+a)$ |
| $(0,1)$ | $1$ | $1-M$ |
| $(1,1)$ | unused | $1/2$ |

For arbitrary mixtures, (1) is exhaustive.
The low region reveals H only if $s_L=1>s_H$, and reveals L only if $s_H=1>s_L$.
It is unused only if both classes always buy.
Every upper flow has positive likelihood in both classes.
Negative integer flows in D1 and nonpositive flows in D2 are impossible under every allowed order.

A low-class purchase has net payoff $-\Delta E[e\mu]-k<0$.
Hence every equilibrium has $s_L=0$.
Then the low region is always used, $\mu_0=(1-s)/(2-s)$, and

$$
\mu_+(s)=\frac{a+(1-a)s}{2a+(1-a)s},\quad
N_+(s)=a+\frac{1-a}{2}s,\quad
K(s,e)=\Delta e\frac{a}{2a+(1-a)s}.
\tag{2}
$$

Here $s=s_H$ and $K$ is the gross return from a purchase.
A purchase always reaches the upper region, which proves the last expression.
Its net return is $K-k$; abstention pays zero.
The upper likelihood ratio reaches $1/a$, so $\mu_+\le M<1$.
This cap holds after the low-class exclusion, not under every wrong-signed profile in the table.

No equilibrium or profitable deviation needs an off-path belief in D1 or D2.
Under the nonequilibrium profile $(1,1)$, an abstention can reach the unused low region, but earns zero regardless of price.

### 3.2 Complete order conditions and the benchmark strip — analytical

The prior never recruits on $1<r<10$: $B_r(1/2)<B_1(1/2)=39/8<6$.
The low region therefore has entry $\rho$.
Solve $\mu_+(s)=\tau$ and $K(s,e)=k$ to obtain

$$
s^*=\frac{a(2\tau-1)}{(1-a)(1-\tau)},\qquad
s_e=\frac{a(e\Delta/k-2)}{1-a},\qquad
e^*=\frac{k}{\Delta(1-\tau)}.
\tag{3}
$$

The following list is exhaustive because the investor has two actions and $K$ decreases strictly on each fixed-entry piece.

- No trade: $\rho\Delta/2\le k$.
- Full purchase: $\Delta e(M)(1-M)\ge k$.
- Interior mixture: retain $s_e\in(0,1)$ only if $e=\rho$ below $s^*$ or $e=1$ above $s^*$.
- Threshold mixture under CM: retain $s=s^*\in(0,1)$ only if $\rho\le e^*\le1$.
- C1 retains the threshold mixture only when $e^*=1$. I0 excludes interior mixtures and requires strict full-order profit.

If $\tau\ge1$, no upper flow recruits; use only the $e=\rho$ piece.
If $s^*$ lies outside $[0,1]$, omit that threshold and each inconsistent piece.
These rules cover all pure and mixed equilibria in the benchmark strength domain.

At the three strengths,

$$
\tau(6/5)=\frac{195}{308},\quad \tau(3)=\frac{141}{200},\quad
\tau(18/5)=\frac{4245}{5804}.
$$

Recruitment at 3 and no recruitment at 3.6 require $\tau(3)\le M<\tau(3.6)$.
Equivalently,

$$
\boxed{\frac{1559}{4245}<a\le\frac{59}{141}}
= (0.3672555948,\ 0.4184397163].
\tag{4}
$$

The robust range excludes the upper endpoint. C1 permits that endpoint; CM can remove recruitment there.
The lower endpoint fails the return to the floor under C1.
For D2, (4) becomes $\log(141/59)\le\eta<\log(4245/1559)$.

Uniqueness needs payoff bounds as well as posterior bounds.
At $r_0$, $\Delta=1/60<k=1/50$, so every nonzero order loses money under every candidate schedule.
At $r_1$ and $r_2$, (2) gives $K\ge\rho\Delta(1-M)$.
Throughout (4), its margins above $k$ exceed $21563/870600$ and $899467/20894400$, respectively.
Thus full high-class purchases are unique at both strengths, including arbitrary investor mixtures.
The unique outcomes are entry $\rho$, above $\rho$, and $\rho$, respectively.

At full purchases, $\Pr(+\mid H)=1$ and $\Pr(+\mid L)=a$, hence

$$
\mathsf E=\rho+(1-\rho)\frac{1+a}{2},\qquad \mathsf O_H=\frac12.
\tag{5}
$$

The ceiling solves $B_{r_C}(M)=6$, or
$Mr_C^2+(12-20M)r_C+M-3/4=0$; take the positive root.
Both $g_j$ decrease with $r$, so entry returns to $\rho$ strictly above this unique root.
At $a=e^{-1}$, $M=1/(1+e^{-1})$ and $r_C$ exactly equal the paper's values.

### 3.3 Coexistence and entry order — analytical

Put $\mathfrak r(d)=1+d+\sqrt{d^2+2d}$, the inverse of $\Delta(r)$ for $r>1$.
Define

$$
r_N=\mathfrak r(2k/\rho),\qquad r_F=\mathfrak r(k/(1-M)),\qquad
\Delta(r_A)[1-\tau(r_A)]=k.
\tag{6}
$$

No trade and full purchases coexist on $[r_F,r_N]$ under IM, or $(r_F,r_N]$ under I0.
Under IM and C1, the full coexistence interval is $[r_A,r_N]$.
On $[r_A,r_F)$, the informative outcome uses $s_1$ from (3).
At $r_A$, both players are indifferent and C1 supports entry.

To prove that this is one interval, note $r_N<7/4$ and $1/2<\tau<2/3$ there.
On $[6/5,7/4]$, $g_H-g_L>8$ and $0<\tau'<7/64$.
Indeed, $\tau'=\{-(1-\tau)g_L'-\tau g_H'\}/(g_H-g_L)$, with $-g_L'\le3/8$ and $-g_H'<1/2$.
Also $\Delta'/\Delta>2$, while $\tau'/(1-\tau)<21/64$.
Thus $\Delta(1-\tau)$ increases strictly.
Its values at $6/5$ and $5/3$ are $113/18480<k<371/7980$.
This proves the unique root $r_A$.
Since $\tau(r_N)<2/3<M$, the threshold stays feasible throughout coexistence.
The strict decrease of $K$ on each entry piece proves the stated interval and excludes additional branches there.

Across (4), the full-order margin at 1.55 exceeds $223499/35984800>0$.
Thus all of 1.55–1.65 lies in the full-purchase coexistence interval.
The informative entry level in (5) is flat across these strengths.
Under CM, one extra threshold outcome has

$$
\mathsf E^*=\rho+\frac a2\left[
\frac{k}{\Delta(1-\tau)^2}-\frac\rho{1-\tau}\right].
\tag{7}
$$

Its entry lies strictly between no trade and full purchases, since $0<e^*-\rho<1-\rho$ and $N_+(s^*)<N_+(1)$.
**computer-assisted:** At 1.55, 1.60, and 1.65, (7) decreases strictly throughout (4).
The exact successive differences divided by $a$ are positive fractions in `results.txt`.
These are the only informative outcomes there, so no strictly upward triple exists, even through a change of branch.
On the earlier recruited mixed branch, entry equals $\rho+(1-\rho)a\Delta/(2k)$ and rises strictly.
Thus some upward entry order survives, but not at the requested strengths.

### 3.4 D3: the sale direction — analytical, with the numerical limits stated below

D3 retains Edmans's direction: the low class sells and the high class holds; good news comes from the absence of a revealed sale.
Let $s_j$ denote sale probabilities. Bayes' rule gives

$$
\mu_-=\frac{\pi s_H}{\pi s_H+(1-\pi)s_L},\quad -1<x\le0;
\qquad
\mu_+=\frac{\pi[1-(1-a)s_H]}
{\pi[1-(1-a)s_H]+(1-\pi)[1-(1-a)s_L]},\quad x>0.
\tag{8}
$$

For discrete noise, these regions are $x=-1$ and $x\ge0$.
Every mixture uses (8); the four pure sale profiles $(0,0),(0,1),(1,0),(1,1)$ give
$(\text{unused},1/2),(0,M),(1,1-M),(1/2,1/2)$, respectively.
The lower region is unused only when neither class sells; it reveals a class when only that class sells.
Flows below the feasible lower bound are impossible.

A high-class sale earns $-\Delta E[e(1-\mu)]-k<0$, hence $s_H=0$ in equilibrium.
With $s=s_L>0$, a sale reaches the pooled region with probability $a$ and earns zero gross return elsewhere:

$$
\mu_+=\frac1{2-(1-a)s},\quad
K_S(s,e)=\frac{a\Delta e}{2-(1-a)s},\quad
s_S^*=\frac{2-1/\tau}{1-a},\quad
s_{S,e}=\frac{2-ae\Delta/k}{1-a},\quad e_S^*=\frac{k}{a\Delta\tau}.
\tag{9}
$$

Retain each interior root only on its consistent entry piece; retain the threshold root under CM only if $\rho\le e_S^*\le1$.
Full sale requires $K_S(1,e(M))\ge k$, and I0 makes this strict.
Under no trade, impose posterior zero at unused nonpositive flows; this is the informed-sale convention, not a proved refinement theorem.
Then no trade requires $a\rho\Delta/2\le k$.
With other off-path beliefs, its deviation payoff becomes $\Delta[a\rho/2+(1-a)E_-[e\mu]]$ and can be larger.
This proves the complete D3 order conditions and identifies the belief dependence.

At full sale the experiment is D1's full experiment translated by minus one, and $K_S(1,e)=\Delta e(1-M)$.
Thus (4), (5), the ceiling, and A.9 survive; full sale is unique at 3 and 3.6 because $a\rho\Delta/2>k$.
Under the stated belief rule, coexistence is $[r_F,\mathfrak r(2k/(a\rho))]$; there is no informative outcome below $r_F$ because $K_S$ increases in $s$.
An earlier mixed branch has rising entry until $a\Delta\tau=k$, but it ends below 1.55 throughout (4).
At the requested strengths, only the flat full branch and a decreasing CM branch remain; exact differences appear in `results.txt`.

For completeness, the upper mass is $N_S=1-(1-a)s/2$, so the threshold branch has
$\mathsf E_S^*=\rho+[k/(a\Delta\tau)-\rho]/(2\tau)$.
On the recruited interior branch, substitute $s_{S,1}$ to obtain $\mathsf E_S=\rho+(1-\rho)a\Delta/(2k)$, which rises with $r$.
At the requested strengths, $K_S(s_S^*,1)>k$ and $K_S(1,\rho)<k$ exclude both ordinary interior roots.
Exact endpoint margins also place CM entry below full entry throughout (4).

Economically, D3 preserves recruitment through good news. The informed trade is a sale on bad news.
No trade requires an off-path convention, while full-sale outcomes need none.

### 3.5 A.9 and comparisons — analytical

At 3, hidden prices imply entry $\rho$.
The payoff bounds above force the same full orders with prices hidden or visible, in each candidate.
Only extra high-cost preparation differs. Write $N=(1+a)/2$.
The pinned appendix's allocation identity gives

$$
\Delta\mathcal R_T=\frac{1-\rho}{2}[(t_H-t_0)+a(t_L-t_0)]>0,
\qquad
\Delta\mathcal W=(1-\rho)N[B_3(M)-6+1/12]>0.
\tag{10}
$$

The first inequality uses positive proceeds increments. The second uses optimal preparation and the reserve gain $p^2/r=1/12$.
Trade costs cancel because orders coincide across the two price regimes.
This proves the A.9 analog at 3, not a welfare order across every intermediate equilibrium.

For T2 V3 buy, write $b=(1-\lambda)\beta$ and $v$ for the purchase probability conditional on informed presence.
Its return is $\Delta e b/(2b+\lambda v)$.
Set $a=b/(b+\lambda)$ and $s=v$; this becomes exactly (2), for every mixture and entry rate.
Therefore the order thresholds, $r_A$, $r_F$, $r_N$, and $r_C$ coincide after this match.
But its upper signal mass is $b+\lambda s/2=(b+\lambda)N_+(s)$.
Entry above the floor, extra ownership, and both access gains in (10) are larger in D1 by $1/(b+\lambda)$.
D1's always-present investor and T2's intermittent investor also have different ex ante trade costs and profits.

B2's original $a=e^{-1/2}$ has $M=0.622459<\tau(3)$ and cannot recruit at $c_H=6$.
The comparison below holds $a$ fixed across the devices; no benchmark cost change is needed on (4).
At a common $a$, B2's full-purchase experiment has posteriors $(1-M,M)$ and upper mass $1/2$.
A purchase reaches that upper region with probability $M$, rather than one.
Its gross return is $\Delta M(1-M)(e_++\rho)$.
Thus, in units of $\Delta$,

| Threshold | D1/D2 and matched V3 | B2 |
|---|---|---|
| No-trade deviation | $\rho/2$ | $\rho/2$ |
| Full order, hidden prices | $\rho(1-M)$ | $2\rho M(1-M)$ |
| Full order, recruitment | $1-M$ | $(1+\rho)M(1-M)$ |

On (4), $2M>1$ but $(1+\rho)M<1$.
D1 therefore has a lower hidden-price payoff and a higher recruited payoff than B2.
Its recruitment multiplier is $1/\rho=4$, versus B2's $(1+\rho)/(2\rho)=2.5$.
Equal upper posteriors do not imply equal payoffs.
At $a=e^{-1}$, full-order coexistence starts at $1.467127$ in D1 and $1.492936$ in B2.

Edmans (2009), verified record A6, supplies the exact exponential noise law and a two-price calculation.
D2 reverses his informed direction and omits his initial stake, endogenous effort, endogenous sale size, and managerial timing.
D3 retains his direction, but perfect class information, fixed unit sales, trade costs, and subsequent challenger entry remain changes.
D1 is the discrete counterpart; exact geometric-noise corporate precedent remains **open** in the verified records.
Relative to EGJ, D1 retains unit orders, aggregate flow, competitive prices, and a corporate response.
It replaces bounded noise with an unbounded count of liquidity purchases and excludes informed sales.
Its knob controls noise volume: $E[G]=a/(1-a)$ ranges from $0.580417$ to $0.719512$ on (4).
D2's mean is $1/\eta$, not the geometric mean.
Neither setup retains the paper's endogenous order size or its partial-sale asymmetry.

## 4. Scorecard

Numbers below use $a=e^{-1}$, or $\eta=1$; displayed decimals are **numerical diagnostic** evaluations of analytical formulas.

### D1

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade at 1.2; entry $0.25$. | analytical |
| 2. Prop. 2(ii) | Unique full purchase at 3; entry $0.762955$, ownership $0.5$. | analytical |
| 3. Prop. 2(iii) | Informative full purchase at 3.6; entry $0.25$; $r_C=3.592659$. | analytical |
| 4. Prop. 3 | IM coexistence $[1.393958,1.747878]$; full purchases from $1.467127$. Contains 1.55–1.65; upward triple fails. | analytical; computer-assisted order comparison |
| 5. A.9 | Proceeds gain $0.485104$; net surplus gain $0.154137$. | analytical |
| 6. Off path | None in equilibria or their deviations. | analytical |
| 7. Ties | Equations (2)–(3) cover all mixtures; C1/CM and IM/I0 matter at specified boundaries. | analytical |
| 8. Knob | Equation (4); mean liquidity purchases $a/(1-a)$. | analytical |
| 9. Precedent | Discrete counterpart of A6; exact discrete device unverified. | open |
| 10. Evidence | Complete finite-menu derivation; exact rational arithmetic and 40-digit evaluations. | analytical; computer-assisted; numerical diagnostic |

### D2

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Same as D1: unique no trade and entry $0.25$. | analytical |
| 2. Prop. 2(ii) | Same as D1: entry $0.762955$, ownership $0.5$. | analytical |
| 3. Prop. 2(iii) | Same as D1: entry $0.25$, informative orders, $r_C=3.592659$. | analytical |
| 4. Prop. 3 | Same coexistence interval; requested upward triple fails. | analytical; computer-assisted |
| 5. A.9 | Same gains as D1. | analytical |
| 6. Off path | No deviation reaches an unused region with positive probability. | analytical |
| 7. Ties | Same conditions as D1; density endpoints have zero mass. | analytical |
| 8. Knob | $0.8712224465\le\eta<1.0016972297$; robust lower endpoint is strict. | analytical |
| 9. Precedent | A6 verifies the exact noise law, with opposite informed direction and different corporate timing. | analytical, source comparison |
| 10. Evidence | Exact reduction to (1)–(3). | analytical; numerical diagnostic decimals |

### D3

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no trade at 1.2; entry $0.25$. | analytical |
| 2. Prop. 2(ii) | Unique full low-class sale at 3; entry $0.762955$, ownership $0.5$. | analytical |
| 3. Prop. 2(iii) | Informative full sale at 3.6; entry $0.25$; same ceiling. | analytical |
| 4. Prop. 3 | Coexistence $[1.467127,2.464007]$ with posterior zero at unused flows. Contains requested interval; upward triple fails. | analytical; computer-assisted order comparison |
| 5. A.9 | Same gains as D1. | analytical |
| 6. Off path | No-trade boundary and coexistence require the stated informed-sale convention. Weak benchmark exclusion does not. | analytical |
| 7. Ties | Equation (9), NT inequality, and full-sale inequality give all outcomes. | analytical |
| 8. Knob | Same strip (4), or D2's rate range. | analytical |
| 9. Precedent | A6 verifies the sale direction and exponential law; remaining economic structure differs. | analytical, source comparison |
| 10. Evidence | Closed-form order conditions; displayed endpoints use 40 digits. | analytical; numerical diagnostic |

## 5. Numerical example

The rational match $a=11/29$ corresponds to T2 V3's $\beta=1/3$, $\lambda=6/17$, $M=29/40$.

| Quantity at 3 | D1/D2 | T2 V3 buy | B2 at the same $a$ |
|---|---|---|---|
| Entry | $89/116$ | $37/68$ | $5/8$ |
| High ownership | $1/2$ | $23/68$ | $127/320$ |
| Gross purchase return, recruited | $11/60$ | $11/60$ | $319/1920$ |
| Gross purchase return, hidden | $11/240$ | $11/240$ | $319/4800$ |
| Proceeds gain from access | $113/232$ | $113/408$ | — |
| Net surplus gain from access | $15/116$ | $5/68$ | — |

**computer-assisted:** The rational example uses exact fractions, including root brackets and every strict benchmark margin.
The calibration $e^{-1}$ also lies strictly inside (4).
For an exact enclosure, put $L=\sum_{n=0}^{12}1/n!$ and $U=L+14/(13\cdot13!)$.
The exponential series gives $L<e<U$, because successive omitted terms have ratio at most $1/14$.
The script prints positive exact margins $1/U-1559/4245$ and $59/141-1/L$.

At $a=11/29$, $r_F=1.460985$, $r_N=1.747878$, and $r_C=3.458247$.
At $a=e^{-1}$, the CM entry levels at 1.55, 1.60, and 1.65 are $0.422006$, $0.384110$, and $0.353825$.
Their full-purchase counterparts all equal $0.762955$.

Program use: run `.venv/bin/python audit/microstructure_search_2026_10_22/scripts/T4_one_sided_noise/derive.py` from the repository root.
The print-only run took less than one second; output is `scripts/T4_one_sided_noise/results.txt`.
Rational inputs use `fractions`. Irrational evaluations use `mpmath` at 40 decimal digits, with root tolerance $10^{-32}$.
The printed root residuals are below $10^{-38}$; these are not interval certificates for irrational inputs.
Threshold expressions outside their admissible ranges are printed as algebraic values, not equilibrium claims.
No flow truncation or parameter grid is used.

## 6. Open issues

- **open:** Exact corporate precedent for D1's geometric buy count remains unverified.
- **open:** A refinement proof for D3's unused-flow convention is absent.
- **open:** Continuous informed order sizes, optional presence, and endogenous liquidity demand are outside this comparison.
- **analytical:** The paper's smooth entry path and partial-sale mechanism do not survive the binary buy menu.
- **computer-assisted:** The requested upward triple fails throughout the working strip, even with both forms of indifference.

## 7. Plain summary

A one-sided count of noise purchases removes the revealing upper edge.
Low flow can reveal that the investor did not buy, but a purchase always meets residual uncertainty.
The discrete and exponential versions have exactly the same two-region experiment and purchase incentives.
Both recover the benchmark entry reversal, the early ceiling, coexistence, and the access gains.

The viable noise range is an interval, not a knife-edge.
At $a=e^{-1}$, the ceiling equals the paper's ceiling exactly.
Entry and ownership exceed T2 V3's levels, although matched investors face the same conditional purchase thresholds.
This larger response reflects more frequent favorable signals, not a larger conditional profit from the same posterior.

The main failure is the requested upward entry order at 1.55–1.65.
Full purchases give flat entry there; the extra threshold branch under challenger indifference gives decreasing entry.
An earlier mixed branch does have increasing entry.

Edmans's sale direction also recovers the benchmark outcomes.
It makes the no-trade comparison depend on beliefs at a newly feasible sale flow.
T2 V3 retains the stronger precedent for alternative same-size arrivals; D2 has direct precedent for its exponential noise law.
