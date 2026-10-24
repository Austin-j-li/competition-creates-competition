# C1. Geometric-count noise with two-sided orders $q\in\{-1,0,1\}$

## 1. Question

The three-point buy-only model loses two paper results.
It loses the endogenous trading asymmetry.
It loses coexistence in Proposition 3 of the paper.
Proposition 3 has full purchases and partial sales.
Those orders coexist with no trade.
Entry rises across the three certified strengths.

This memo asks one question.
Do two-sided orders with discrete-Laplace noise recover those results?
The memo answers four sub-questions from the task.

- Posteriors under full orders and under mixtures.
- A Proposition 2 analog with two-sided orders.
- Asymmetry, coexistence, and entry order across strengths.
- Comparison with the three-point two-sided analysis.

The short answer follows.

- Posteriors take at most three values.
- Full orders give the paper bounds $m$ and $M$.
- A Proposition 2 analog holds with exact bounds.
- No trade and full trade coexist on an interval.
- The interval contains $r=1.55,1.60,1.65$.
- The buyer is the strong side, as in the paper.
- A pure asymmetric buy-only outcome also exists for $c_H=5$.
- A full-buy and partial-sell branch exists only in a narrow window.
- A wider partial branch needs challenger mixing at indifference.
- Entry on the full branch is flat across strengths.
- Entry on the wider mixing branch falls across strengths.
- So the strict upward order in Proposition 3 does not return.

## 2. Setup

### Base model and change

The base model is the discrete-Laplace model in TEAM_RULES §4.2.
Noise is $Z=G_1-G_2$ with geometric counts.
Its law is $P(Z=z)=\frac{1-a}{1+a}a^{|z|}$ for $z\in\mathbb Z$.
Here $a=e^{-1/b}$ and $b=2$.
So $a=e^{-1/2}\approx0.606531$.

The base model has buy-only orders $q\in\{0,1\}$.
This memo changes only the order set.
The new order set is $q\in\{-1,0,1\}$.
Flow is $X=q+Z$.
The change restores the sale in the paper profile $(1,-1)$.

All other objects stay as in TEAM_RULES §3.
The incumbent value is uniform on $[0,r]$.
The reserve is $p$.
The challenger class is $H$ or $L$.
The prior is $\pi=1/2$ in the benchmark.
Values are point masses at $h$ and $\ell$ (Reading N).
Costs satisfy $c_L=0<c_H$.
The low-cost share is $\rho$.
The trading cost is $k$ per unit.
The investor is present for sure ($\lambda=1$).
Section 6 lists $\pi\ne1/2$ and $\lambda<1$ as open items.

Benchmark values are as follows.

- $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$.
- $b=2$, $k=0.02$, $c_L=0$.
- $r_0=1.2$, $r_1=3$, $r_2=3.6$.
- $c_H=5$ is the brief starting point.
- $c_H=6$ is the paper value.
- Result 3 recomputes the full $c_H$ window.

Paper formulas were checked at the pinned commit.
The check used $t_0,t_H,t_L,g_H,g_L,\Delta_T$ in paper eq. (4).
It used $B_r$, $e_r$, $P_r$ in paper eq. (9).
It used residuals in paper eq. (11).
Proposition 3 is in paper §4.3 at the pinned commit.

| Symbol | Meaning |
|---|---|
| $u$ | $\Pr(q_H=1)$, buy probability in state $H$ |
| $v$ | $\Pr(q_L=-1)$, sell probability in state $L$ |
| $\mu_+,\mu_0,\mu_-$ | posteriors at $X\ge1$, $X=0$, $X\le-1$ |
| $e_+,e_0,e_-$ | entry rates at those posteriors |
| $\tau$ | $(c_H-g_L)/(g_H-g_L)$, costly-entry belief |
| $G_H,G_L$ | gross gains from a unit correct trade |
| $\mathsf E,\mathsf O_H$ | entry rate, high-class ownership rate |

### Equilibrium, beliefs, and tie rules

The equilibrium concept is perfect Bayesian equilibrium.
Market makers see $X$ and set $P(X)=\mathbb E[V_T\mid X]$.
The challenger sees $P$ and its cost $C$.
It does not see $X$.
Result 2 proves that $P$ reveals the flow posterior.
So flow beliefs and price beliefs agree on path.

Noise has full support on $\mathbb Z$.
Every integer flow has positive probability under every strategy.
No flow is off path.
No refinement is needed.
This point differs from the three-point model.

Tie rules need care because atoms have positive mass.
The memo uses two nested concepts and labels each result.

- **Baseline ties.** The challenger prepares at indifference.
  So $e_r(\mu)=\rho+(1-\rho)\mathbf 1\{B_r(\mu)\ge c_H\}$.
  The investor may mix at indifference (conventional rule).
  A mixture with $0<u<1$ needs $G_H=k$ at the candidate.
- **Prescribed investor tie.** The investor abstains at indifference.
  Then no genuine investor mixture survives.
  Only corner profiles survive, except at isolated equalities.
  The memo states which results survive this stricter rule.
- **Challenger mixing.** At $\mu=\tau$ the costly type is indifferent.
  A mix gives $e\in[\rho,1]$ at that belief.
  Such equilibria carry an explicit mixing label.
  The baseline tie selects $e=1$ and excludes them.

Status labels follow TEAM_RULES §5.
Each result states its label.
Scripts print results only.
Section 5 lists scripts, precision, and grids.

## 3. Results

### Result 1. Posteriors take at most three values (analytical)

Write $f(z)=P(Z=z)$ and $d=1-a$.
Result 2 shows that wrong orders never occur.
So write a candidate as $(u,v)\in[0,1]^2$.
Flow laws by class are
$a_H(x)=(1-u)f(x)+uf(x-1)$ and $a_L(x)=(1-v)f(x)+vf(x+1)$.
With prior $1/2$, the posterior is $\mu(x)=a_H(x)/(a_H(x)+a_L(x))$.

*Derivation.* Ratios $f(x-1)/f(x)$ and $f(x+1)/f(x)$ have three cases.

- For $x\ge1$: ratios are $a^{-1}$ and $a$.
- For $x\le-1$: ratios are $a$ and $a^{-1}$.
- For $x=0$: both ratios are $a$.

Define four affine terms.

$$
A_+=1+u\frac{d}{a},\quad B_+=1-vd,\quad
A_-=1-ud,\quad B_-=1+v\frac{d}{a}.
$$

Then $a_H(x)/f(x)$ equals $A_+,A_-,A_-$ by region.
Then $a_L(x)/f(x)$ equals $B_+,B_+,B_-$ by region.
The regions are $X\ge1$, $X=0$, $X\le-1$.
Hence the infinite flow space has three likelihood classes.

$$
\mu_+=\frac{A_+}{A_++B_+},\qquad
\mu_0=\frac{A_-}{A_-+B_+},\qquad
\mu_-=\frac{A_-}{A_-+B_-}.
$$

Order holds: $\mu_+\ge\mu_0\ge\mu_-$.
The proof uses $A_+\ge A_-$ and $B_-\ge B_+$.
Equality $\mu_+=\mu_0$ holds exactly when $u=0$.
Equality $\mu_0=\mu_-$ holds exactly when $v=0$.
So the count of distinct posteriors is exact.

- One value if $u=v=0$ (the prior $1/2$).
- Two values if exactly one of $u,v$ is positive.
- Three values if $u>0$ and $v>0$.

Define $m_1=a/(1+a)$ and $M_1=1/(1+a)$.
Define $m=a^2/(1+a^2)$ and $M=1/(1+a^2)$.
At $b=2$: $m_1\approx0.377541$, $M_1\approx0.622459$.
At $b=2$: $m\approx0.268941$, $M\approx0.731059$.
Note $M=1/(1+e^{-2/b})$ and $m=1/(1+e^{2/b})$.
These are the paper Laplace bounds in eq. (7).

| Profile $(u,v)$ | $\mu_+$ ($X\ge1$) | $\mu_0$ ($X=0$) | $\mu_-$ ($X\le-1$) |
|---|---|---|---|
| $(1,1)$ full | $M$ | $1/2$ | $m$ |
| $(1,0)$ buy only | $M_1$ | $m_1$ | $m_1$ |
| $(0,1)$ sell only | $M_1$ | $M_1$ | $m_1$ |
| $(0,0)$ none | $1/2$ | $1/2$ | $1/2$ |

*Derivation for $(1,1)$.* Terms are $A_+=1/a$, $B_+=a$, $A_-=a$, $B_-=1/a$.
So $\mu_+=(1/a)/(1/a+a)=1/(1+a^2)=M$.
So $\mu_-=a/(a+1/a)=a^2/(1+a^2)=m$.
So $\mu_0=a/(a+a)=1/2$. $\square$

Bounds hold for every mixture: $m\le\mu(x)\le M$.
Odds prove the bounds.
Odds at $+$ are $A_+/B_+\in[1,a^{-2}]$.
Odds at $-$ are $A_-/B_-\in[a^2,1]$.
Odds at $0$ are $A_-/B_+\in[a,a^{-1}]$.
The endpoints give $m$ and $M$.
Only full orders attain $m$ and $M$.

For a general prior $\pi$, odds gain a factor $\pi/(1-\pi)$.
The three-class reduction still holds.
Posteriors become $\pi A/(\pi A+(1-\pi)B)$ by region.
Equilibria for $\pi\ne1/2$ stay open (§6).

Script `posteriors.py` checks the formulas by direct convolution.
It uses 50-digit arithmetic on flows $[-6,6]$.
Worst differences are below $3\times10^{-51}$.
The omitted tail $P(|Z|>60)$ is about $7.07\times10^{-14}$.
No truncation enters the proofs, which use exact geometric sums.

### Result 2. Prices, dominance, and trading gains (analytical)

**Price sufficiency.** With $c_L=0$, entry has floor $\rho$.
Proof: $B_r(\mu)\ge g_L>0=c_L$ for every $\mu$.
Here $g_L=(\ell^2-p^2)/(2r)>0$.
Also $g_H>g_L$ for $\ell<r<h$.
Competitive pricing gives paper eq. (10):
$P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X]$.
Since $e(P)\ge\rho>0$, $\mu_X$ is a function of $P$.
The challenger therefore reads $\mu_X$ from the price.
Also $P_r(\mu)=t_0+e_r(\mu)[t_L-t_0+\Delta_T\mu]$ rises strictly in $\mu$.
The bracket is positive because $t_L>t_0$.
The step in $e_r$ jumps up, so strict increase survives.
No self-fulfilling pool can hide a posterior.
A shared price needs $e=0$ or a shared posterior.
The floor excludes $e=0$.

**Dominance.** Residuals follow paper eq. (11).
At any flow, $V_H-P=e\Delta_T(1-\mu)\ge0$.
At any flow, $P-V_L=e\Delta_T\mu\ge0$.
A sale by $H$ earns at most $-k<0$.
A purchase by $L$ earns at most $-k<0$.
Zero earns zero.
So every equilibrium has the form $(u,v)$ in Result 1.
The argument uses no belief restriction.

**Region probabilities.** Geometric sums give exact masses.
For $k\ge0$, $P(Z\ge k)=a^k/(1+a)$ with $a^0=1$.
Define region masses for one unit order.

| Mass | Value | At $b=2$ |
|---|---|---|
| $\alpha=P(Z\ge1)$ | $a/(1+a)$ | $0.377541$ |
| $\beta=P(Z\ge0)$ | $1/(1+a)$ | $0.622459$ |
| $\gamma=P(Z=0)$ | $(1-a)/(1+a)$ | $0.244919$ |
| $\delta=P(Z\ge2)$ | $a^2/(1+a)$ | $0.228990$ |
| $\phi=P(Z=1)$ | $a(1-a)/(1+a)$ | $0.148551$ |

Order $q=0$ gives region masses $(\alpha,\gamma,\alpha)$.
Order $q=1$ gives $(\beta,\phi,\delta)$.
Order $q=-1$ gives $(\delta,\phi,\beta)$.
Region order is $(+,0,-)$ in each triple.

**Gains.** Fix a candidate $(u,v)$ and its price schedule.
Let $e_s=e_r(\mu_s)$ for $s\in\{+,0,-\}$.
Gross gains from correct unit trades are

$$
\begin{aligned}
G_H(u,v)&=\Delta_T\big[\beta e_+(1-\mu_+)+\phi e_0(1-\mu_0)+\delta e_-(1-\mu_-)\big],\\
G_L(u,v)&=\Delta_T\big[\delta e_+\mu_++\phi e_0\mu_0+\beta e_-\mu_-\big].
\end{aligned}
$$

Net gains subtract $k$.
Type $H$ buys if $G_H>k$, abstains if $G_H<k$, mixes if equal.
Type $L$ sells by the same rule with $G_L$.
Universal bounds follow from $e_s\in[\rho,1]$ and $\mu_s\in[m,M]$.

$$
\rho m\Delta_T\ \le\ G_H,G_L\ \le\ \Delta_T .
$$

The lower bound uses $1-\mu_s\ge m$ and $\mu_s\ge m$.
The upper bound uses residuals at most one.
Entry thresholds are linear in $(u,v)$.
For example, $\mu_+\ge\tau$ means $A_+(1-\tau)\ge\tau B_+$.
So each entry pattern holds on a polygon in the unit square.
Gains are smooth inside each polygon.
Gains jump up where a posterior crosses $\tau$.
The jump size is $(1-\rho)$ times a positive residual term. $\square$

### Proposition C1.1. Proposition 2 analog (analytical)

Fix $0<p<\ell<r_0<r_1<h$, $\rho\in(0,1)$, $b>1$, $k>0$.
Orders are $q\in\{-1,0,1\}$ with discrete-Laplace noise.
Suppose the three conditions hold.

$$
0\le c_L\le B_{r_1}(m) \tag{D1}
$$

$$
B_{r_0}(1/2)<c_H\le B_{r_1}(M) \tag{D2}
$$

$$
\Delta_T(r_0)<k<\rho m\Delta_T(r_1) \tag{D3}
$$

The team case $c_L=0$ meets (D1) at every strength.
Then three conclusions hold under baseline ties.
They also hold under the prescribed investor tie.

- **(i)** At $r_0$, the unique outcome is $(u,v)=(0,0)$.
  The price is constant and entry is $\rho$.
- **(ii)** At $r_1$, the unique outcome is $(u,v)=(1,1)$.
  Orders are $(q_H,q_L)=(1,-1)$.
  The price takes three values.
  Entry and ownership exceed the $r_0$ values.
- **(iii)** Take $r_2\in(r_1,h)$ with $c_L\le B_{r_2}(m)$ and $B_{r_2}(M)<c_H$.
  The unique outcome is again $(1,1)$.
  Entry returns to $\rho$.

Formulas in part (ii) are exact.
Let $P_+=(1+a^2)/(2(1+a))$ be $\Pr(X\ge1)$ under full orders.
Then entry is $\mathsf E=\rho+(1-\rho)P_+$.
Ownership is $\mathsf O_H=\tfrac12[\rho+(1-\rho)/(1+a)]$.
At $b=2$, $\rho=0.25$: $P_+\approx0.425725$.
So $\mathsf E\approx0.569293$ and $\mathsf O_H\approx0.358422$.
At $r_0$: $\mathsf E=0.25$ and $\mathsf O_H=0.125$.
The labor in §5 verifies each benchmark number.

*Proof.*

*Step 1: floors and prices.* Condition (D1) gives $e\ge\rho$.
Result 2 then gives dominance and price sufficiency.
With $c_L=0$, (D1) holds because $B_r(m)>0$.

*Step 2: weak incumbent.* Result 2 gives $G_H,G_L\le\Delta_T(r_0)$.
Left side of (D3) makes both net gains negative.
The sign holds at every candidate $(u,v)$.
So $u=v=0$ is the only fixed point.
Posteriors equal $1/2$.
Left side of (D2) gives $e_{r_0}(1/2)=\rho$.
Entry is $\rho$ and the price is constant.

*Step 3: strong incumbent.* Result 2 gives $G_H,G_L\ge\rho m\Delta_T(r_1)$.
Right side of (D3) makes both net gains positive.
The sign holds at every candidate $(u,v)$.
So $u=v=1$ is the only fixed point.
Result 1 gives posteriors $(M,\tfrac12,m)$.
Each $B_r(\mu)$ falls in $r$ by paper eq. (5).
So $B_{r_1}(1/2)\le B_{r_0}(1/2)<c_H$.
Hence $e_0=e_-=\rho$.
Right side of (D2) gives $e_+=1$.
Equality uses the challenger tie rule (prepare).

*Step 4: entry sums.* Under $H$, region masses are $(\beta,\phi,\delta)$.
Under $L$, region masses are $(\delta,\phi,\beta)$.
Average mass at $+$ is $(\beta+\delta)/2=P_+$.
Entry is $1$ at $+$ and $\rho$ elsewhere.
So $\mathsf E=\rho+(1-\rho)P_+>\rho$.
A prepared $H$ challenger wins because $h>r_1$.
So $\mathsf O_H=\tfrac12[\beta\cdot1+(1-\beta)\rho]$.
Rewrite with $\beta=1/(1+a)$ for the stated form.
Then $\mathsf O_H>\rho/2$.
Good news is more likely under $H$: $\beta>\delta$.
So added entry tilts to the high class.
The constant $r_0$ experiment is a garbling of the $r_1$ experiment.
Strict Blackwell dominance follows.

*Step 5: ceiling.* At $r_2$, every posterior is at most $M$.
Hypothesis $B_{r_2}(M)<c_H$ gives $\tau>M$.
So $e\equiv\rho$ and entry is $\rho$.
Also $\Delta_T$ rises in $r$.
So $k<\rho m\Delta_T(r_1)\le\rho m\Delta_T(r_2)$.
Step 3 logic gives unique full orders again.

*Step 6: open set.* Benchmark §5 meets each inequality strictly.
Values include $c_H=5$ and $c_H=6$ (Result 3).
Each bound is continuous in the primitives.
So the region is open and nonempty. $\square$

Three contrasts with paper conditions (A1)–(A3) matter.

- (D1) allows equality, because $m$ occurs with positive mass.
  Paper (A1) is strict.
- (D2) allows $c_H=B_{r_1}(M)$ for the same reason.
  The tie rule then decides recruitment at $M$.
- (D3) has no factor $(1-1/b)$.
  The paper needs that factor for marginal continuous orders.
  A unit discrete order needs only the residual bounds.
  The discrete uniqueness region is therefore larger.

Exact uniqueness thresholds lie inside the sufficient bounds.
No trade is unique if $\Delta_T(r)<k$ (sufficient).
Full trade is unique if $\rho m\Delta_T(r)>k$ (sufficient).
At $k=0.02$, $\rho=0.25$, $b=2$, thresholds in $r$ follow.
Write $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$ for $\Delta_T(r)=d$.

- Sufficient no-trade uniqueness: $r<\mathfrak r(k)\approx1.220998$.
- Sufficient full uniqueness: $r>\mathfrak r(k/(\rho m))\approx2.124148$.
- Paper sufficient full bound is $r_U\approx2.837417$.
- The gap $[1.220998,2.124148]$ needs the branch analysis below.

### Result 3. Exact existence, $c_H$ window, and coexistence (analytical)

Existence of the two corner outcomes has exact thresholds.
Let $\bar e=e_r(1/2)\in\{\rho,1\}$.

**No trade.** At $(0,0)$ each posterior equals $1/2$.
So $G_H(0,0)=G_L(0,0)=\bar e\Delta_T/2$.
No trade is an equilibrium exactly when $k\ge\bar e\Delta_T/2$.
The factor $1/2$ matches paper Proposition A.4.
The three-point factor is $1/3$ instead (§4).

**Full trade.** At $(1,1)$ both gains coincide.
Proof uses $J:=\beta m=\delta M=a^2/((1+a)(1+a^2))$.
Then $G_H(1,1)=G_L(1,1)=\Delta_T[J(e_++e_-)+\phi e_0/2]$.
Entry rates use posteriors $(M,\tfrac12,m)$.
Full trade is an equilibrium exactly when $k$ is at most that value.

In the benchmark regime $B_r(1/2)<c_H\le B_r(M)$:
entry is $(e_+,e_0,e_-)=(1,\rho,\rho)$ and $\bar e=\rho$.
Define $c_T=J(1+\rho)+\phi\rho/2$.
At $b=2$, $\rho=0.25$: $c_T\approx0.227825$.
The no-trade coefficient is $\rho/2=0.125$.
Since $c_T>\rho/2$, existence intervals overlap.
Both outcomes exist exactly when $\Delta_T\in[k/c_T,\,2k/\rho]$.
Endpoints use conventional mixing at zero net gain.
Under the prescribed investor tie, read the left end as open.
Full trade at the left end has zero net gain there.

At $k=0.02$ the overlap in strengths is explicit.

- Full trade appears at $r\approx1.515898$.
- No trade ends at $r_N=\mathfrak r(2k/\rho)\approx1.747878$.
- The paper value is $r_N=1.747877538$ (§4.3).
- Strengths $1.55,1.60,1.65$ lie strictly inside.
- At each one, no trade and full trade coexist.
- Nets are strict there, so the prescribed tie keeps both.

Without recruitment, coexistence of the corners is impossible.
At constant entry $\rho$, full gain coefficient is
$\rho[\beta m+\phi/2+\delta M]\approx0.102271$.
That value is below $\rho/2=0.125$.
So corner existence intervals are disjoint without feedback.
Recruitment at $+$ adds $(1-\rho)J\approx0.125554$ to the coefficient.
Feedback therefore creates the overlap.
At $r_1=3$, full net gain is $+0.131883$ with recruitment.
It is $+0.048181$ if entry stays at $\rho$ everywhere.
The buy-only edge gives a check of brief §0 feedback numbers.
Buy-only net gain at $r_1$ is $+0.175836$ with recruitment.
It is $+0.058335$ without recruitment.
Brief §0 states $+0.176$ and $+0.060$ (rounded nets).
This memo confirms those buy-only numbers as the edge $v=0$.

**Admissible $c_H$ window.** Condition (D2) at $(1.2,3)$ gives
$(B_{r_0}(1/2),\,B_{r_1}(M)]$.
Values are $(4.804167,\,6.217155]$ (50-digit script).
Buy-only orders give $(4.804167,\,5.312161]$ instead.
Two-sided orders widen the top by about $0.905$.
Both $c_H=5$ and paper $c_H=6$ lie inside.
The split at $B_{r_1}(M_1)=5.312161$ matters for branches.

- If $c_H\le B_r(M_1)$, one-sided trade alone can recruit.
- If $c_H>B_r(M_1)$, recruitment needs both sides active.
- At $c_H=6$, buy-only recruitment never occurs for $r>1$.
  Proof: $B_r(M_1)$ falls in $r$ and $B_{1}(M_1)\approx5.977<6$.
  The script verifies $B_{1+10^{-6}}(M_1)\approx5.977134$.

**Ceilings.** Solve $B_r(M)=c_H$ for the return in part (iii).
For $c_H=6$: $r_C\approx3.592659$, the paper value.
So $r_2=3.6$ returns entry to $\rho$, as in the paper.
For $c_H=5$: $r_C\approx6.325302$.
So $r_2=3.6$ still recruits and entry stays $0.569293$.
Buy-only ceilings solve $B_r(M_1)=c_H$.
For $c_H=5$: $r_C\approx3.986097$ (brief says near $4$).
Two-sided orders restore the paper ceiling function $B_r(M)$.

**Existence on $[r_0,h)$.** Under (D1)–(D3), a corner always exists.
No trade covers $\Delta_T\le2k/\rho$.
Full trade with recruitment covers $\Delta_T\ge k/c_T$.
The two ranges overlap because $c_T>\rho/2$.
After the ceiling, full gain uses coefficient $0.102271$ at benchmark.
But $\Delta_T$ there already exceeds $k/0.102271$.
Formally, (D3) plus $0.409086>m$ keeps full trade valid past $r_C$.
Here $0.409086=\beta m+\phi/2+\delta M$.
No existence gap occurs on $[r_0,h)$ in this regime. $\square$

### Result 4. The buyer is the strong side (analytical)

Entry rises only at high beliefs.
So feedback helps the two types by different amounts.
Three exact comparisons locate the asymmetry.

**Symmetric points.** Take $u=v=s\in(0,1)$.
Then $\mu_0=1/2$ and $\mu_-=1-\mu_+$.
Write $S_+=A_++B_+$.
Direct algebra gives
$\beta(1-\mu_+)-\delta\mu_+=d(1-s)/S_+\ge0$.
Hence, for any entry rates with $e_0$ common,

$$
G_H-G_L=\Delta_T(e_+-e_-)\,\frac{d(1-s)}{S_+}.
$$

At constant entry, the gap is zero.
With recruitment only at $+$ ($(e_+,e_-)=(1,\rho)$), the gap is positive.
It is zero only at $s=1$.
So no symmetric interior point is an equilibrium under recruitment.
Both types cannot be indifferent there.
Type $H$ is strict, type $L$ is marginal.
This matches the paper direction: full buys, partial sells.
Script values confirm the sign on the diagonal (§5).

**Slope at the entry jump.** Fix a point with $\mu_+=\tau$.
Vary the common rate $e_+$ at that belief.
Slopes are $\partial G_H/\partial e_+=\Delta_T\beta(1-\tau)$.
Slopes are $\partial G_L/\partial e_+=\Delta_T\delta\tau$.
Their ratio is $(1-\tau)/(a^2\tau)$ because $\beta/\delta=a^{-2}$.
The buyer slope is larger exactly when $\tau<M$.
Recruitment needs $\tau\le M$.
So extra entry helps the buyer more, except at $\tau=M$.
The buyer reaches indifference at a lower entry rate.
Branch solves in Result 5 show $e_H^*<e_L^*$ on the jump curve.
A jump-curve equilibrium must therefore put $H$ at a corner.
Interior points with both types indifferent need $e_H^*=e_L^*$.
Scans find no such point in the coexistence region (§5).

**Pure one-sided corners.** Write gains as $\Delta_T$ times a coefficient.
Assume first that $M_1\ge\tau$, so one-sided trade recruits.
At BNS $(1,0)$, entry is $(1,\rho,\rho)$.
Coefficients are $c_H=\alpha\beta(1+\rho)\approx0.293755$.
Coefficients are $c_L=\delta M_1+\rho m_1(\phi+\beta)\approx0.215309$.
Their gap is $(1-a)\alpha(\beta-\rho\alpha)>0$ always.
So the BNS cost window $k/\Delta_T\in[c_L,c_H]$ is nonempty.
At SNB $(0,1)$, entry is $(1,1,\rho)$.
Coefficients are $c_L=\alpha\beta(1+\rho)$.
Coefficients are $c_H=(\beta+\phi)m_1+\delta\rho\beta\approx0.326722$.
Their gap $c_H-c_L$ equals $(1-a)\alpha(\alpha-\rho\beta)$.
It is positive exactly when $a>\rho$.
Benchmark $a\approx0.607>0.25$ holds.
So SNB needs $k/\Delta_T\ge c_H$ and $k/\Delta_T\le c_L$ at once.
That is impossible.
Sell-only trade cannot survive when it recruits at $+$ and $0$.
The buyer deviates in and captures the recruited regions.
At constant entry $\rho$ ($M_1<\tau$), BNS and SNB are mirrors.
Trader coefficient is $2\rho\alpha\beta\approx0.117502$.
Deviation coefficient is about $0.108406$.
Both corners exist on the same narrow cost window then.
Recruitment breaks the mirror in favor of buys. $\square$

### Result 5. Branches between the corners (numerical diagnostic)

Scripts `equilibria.py`, `branches.py`, and `sweep.py` map branches.
Methods: edge scans split at exact linear jumps (400 points each).
Interior search: Newton steps from 81 starts in each entry cell.
Jump mixing: exact affine solve for $e^*$ at each jump point.
Sweeps: corner flags on $r$ grid with step $0.01$.
All claims in this result are numerical diagnostics, except corner algebra.
No interior cell root was found at any sampled point.
Sampled points are $r\in\{1.4,1.525,1.55,1.65,1.9\}$ for $c_H\in\{5,6\}$.
Edge scans also cover $r\in\{1.2,1.55,1.6,1.65,3,3.6\}$.
A proof needs monotonicity inside cells (§6, open).

**Corner map over $r$ (sweep step $0.01$).**

| Case | $r$ range (grid) | Corner equilibria |
|---|---|---|
| $c_H=5$ | $1.05$–$1.44$ | NT |
| $c_H=5$ | $1.45$–$1.51$ | NT, BNS |
| $c_H=5$ | $1.52$–$1.53$ | NT, T, BNS |
| $c_H=5$ | $1.54$–$1.74$ | NT, T |
| $c_H=5$ | $1.75$–$8.00$ | T |
| $c_H=6$ | $1.05$–$1.51$ | NT |
| $c_H=6$ | $1.52$–$1.74$ | NT, T |
| $c_H=6$ | $1.75$–$1.77$ | T |
| $c_H=6$ | $1.78$–$1.81$ | T, BNS, SNB |
| $c_H=6$ | $1.82$–$8.00$ | T |

Analytic corner windows match the grid thresholds.
BNS with recruitment needs $r\in[1.443322,1.533807]$ (Result 4).
It needs also $M_1\ge\tau(r)$, which holds there for $c_H=5$.
BNS/SNB at constant $\rho$ need $r\in[1.777986,1.819330]$.
That window applies for $c_H=6$, where $M_1<\tau$.
SNB with recruitment never appears, as Result 4 proves.
At $r=1.9$ all sampled nets push to full trade.
Diagnostics suggest unique full trade already at $r=1.9$.
The sufficient proof needs $r>2.124148$ (Proposition C1.1).
Exact uniqueness thresholds inside the gap stay open.

**Narrow baseline branch $(1,v(r))$.** Inside pattern $(1,\rho,\rho)$:
gains do not depend on $c_H$ or $\tau$.
Along $u=1$, $G_L$ rises in $v$ and $G_H$ falls in $v$ (diagnostic).
Both meet at $v=1$ with coefficient $c_T$.
So $G_L(1,v)=k$ has at most one root $v\in(0,1)$ there.
The root has $G_H>k$, so $H$ buys fully.
It exists only where the root stays inside the pattern cell.

- Common lower end: $r\approx1.515898$, $v=1$ (full trade).
- For $c_H=5$: upper end $r\approx1.533807$, $v=0$ (BNS).
- For $c_H=6$: upper end $r\approx1.532313$, $v=v^*(r)$ (jump).

Values on the branch (same $v(r)$ for both $c_H$ values):

| $r$ | $v(r)$ | $\mathsf E$ | $\mathsf O_H$ |
|---|---|---|---|
| $1.520$ | $0.863389$ | $0.576904$ | $0.358422$ |
| $1.525$ | $0.670587$ | $0.587644$ | $0.358422$ |
| $1.530$ | $0.418994$ | $0.601659$ | $0.358422$ |

Entry rises in $r$ on this short branch.
Sell probability falls in $r$ on this branch.
Formulas explain the entry rise.
Entry is $\rho+(1-\rho)P_+(1,v)$ on the branch.
Mass $P_+(1,v)=\alpha+(\gamma-v\phi)/2$ falls in $v$.
So falling $v$ raises $P_+$ and entry.
Ownership is flat because $\Pr(+\mid H)=\beta$ at $u=1$.
The branch needs investor mixing ($0<v<1$).
The prescribed investor tie excludes it.
It lies below the paper strengths $1.55$–$1.65$.

**Wider branches need challenger mixing.** Past the upper end:
$G_L$ jumps over $k$ at $\mu_+=\tau$ with no baseline root nearby.
A mix $e^*\in(\rho,1)$ at $\tau$ restores indifference.
Two such branches appear, one per $c_H$ regime.

For $c_H=6$, the branch is $(1,v^*(r))$ on $\mu_+(1,v^*)=\tau(r)$.
Type $L$ is indifferent at $e_L^*$.
Type $H$ is strict there ($e_H^*<e_L^*$).

| $r$ | $v^*$ | $e_L^*$ | $\mathsf E$ | NT coexists? |
|---|---|---|---|---|
| $1.55$ | $0.253308$ | $0.923037$ | $0.573855$ | yes |
| $1.60$ | $0.272646$ | $0.739324$ | $0.484753$ | yes |
| $1.65$ | $0.291865$ | $0.594346$ | $0.414708$ | yes |

Sell probability rises in $r$, as in the paper direction.
Entry falls in $r$, against the paper order.
Two forces lower entry: $e_L^*$ falls and $P_+$ falls in $v^*$.
The mirror point $(u^*,1)$ fails at each sampled $r$.
Zeroing $G_H$ there leaves $G_L<k$, so full sales fail.

For $c_H=5$, the jump curve does not meet the edge $u=1$.
Recruitment already holds at $(1,0)$ because $M_1>\tau$.
The mixing branch sits at $(u_p(r),0)$ on $\mu_+(u_p,0)=\tau(r)$.
Type $H$ mixes (partial buys), type $L$ abstains strictly.

| $r$ | $u_p$ | $e_H^*$ | $\mathsf E$ | NT coexists? |
|---|---|---|---|---|
| $1.55$ | $0.228270$ | $0.536787$ | $0.366291$ | yes |
| $1.60$ | $0.240749$ | $0.444215$ | $0.329050$ | yes |
| $1.65$ | $0.253260$ | $0.370460$ | $0.299215$ | yes |

Entry again falls in $r$.
Form differs from the paper (partial buys, no sales).
Both mixing branches need investor mixing and challenger mixing.
Baseline ties exclude both branches.
Pure coexistence (NT with T, plus BNS where listed) needs neither mix.

**Verdict on Proposition 3 features.**

- Coexistence with no trade: **recovered**, in pure form (NT with T).
- Endogenous asymmetry: **recovered in direction**.
  The buyer is inframarginal, the seller is marginal (Result 4).
  Pure BNS exists for $c_H=5$; pure SNB with recruitment does not.
- Full buys with partial sells: **recovered only in the narrow window**.
  The window is $r\in(1.515898,1.533807)$ at benchmark $k$.
  A wider version needs challenger mixing.
- Upward entry order across strengths: **not recovered** in general.
  Full-branch entry is constant at $0.569293$.
  Mixing-branch entry falls across $1.55,1.60,1.65$.
  Only the narrow baseline branch has rising entry.
  Its sell probability falls, unlike paper short magnitudes.

## 4. What it recovers or loses relative to the Laplace paper

| Paper item | Two-sided discrete-Laplace with $c_L=0$ |
|---|---|
| Prop. 1, eqs. (4)–(6) | Survives. Auction stage is unchanged. |
| Eq. (7)–(8), Prop. A.1 | Survives with same $m,M$. Ratio bound is $a^{-2}=e^{2/b}$. |
| Eq. (9)–(10), Prop. A.2 | Survives. Floor $\rho$ gives price sufficiency. |
| Eq. (11) residuals | Survive pointwise. Bounds are $\rho m\Delta_T\le A\le\Delta_T$. |
| Global order bound (App. A.2) | Not needed. Finite orders need only unit gains. |
| Prop. 2 (i)–(iii) | Analog holds (Prop. C1.1). No $(1-1/b)$ factor. |
| Eq. (12) $x^*,\alpha_H,\alpha_L$ | Replaced by regions. $P_+,\beta,\delta$ replace $\alpha$ terms. |
| Prop. 3 coexistence | Partial analog (Result 5). Pure NT+T; order fails. |
| Prop. A.3 fixed experiment | Survives. Proof uses only a fixed signal law. |
| Prop. A.4 thresholds | $r_N$ same formula. $\mathfrak r(k)$ same sufficient bound. |
| $r_U$, $r_C$ | $r_U$ improves to $2.124148$. $r_C$ same function $B_r(M)$. |
| App. A.3 certificates | Replaced by Result 5 diagnostics. No interval proof here. |
| App. A.4 noise, costs | Logistic case not studied. Atomless costs not studied. |
| §5.1–§5.2 robustness | Not studied, except $c_H$ window and ceilings. |
| §5.3 signals, App. A.5 | Not studied. |
| §6 welfare, App. A.6–A.7 | Not studied. Entry and ownership only. |
| Hidden-price control (§4.2) | Survives. Entry stays $\rho$ without price access. |

Fixed-experiment note: freeze full orders across $r_0\to r_1$.
Entry then equals $\rho+(1-\rho)P_+$ at both strengths in the window.
So the discrete control is flat at the benchmark, not strictly falling.
Strict deterrence needs a threshold cross inside the interval.
That matches the three-point finding in prior memos.

### Comparison with three-point two-sided analysis

Sources are the three prior memos named in the task.
They study $Z\in\{-1,0,1\}$ with equal weights unless stated.
Labels NT, T, BNS, SNB follow those memos.

| Feature | Three-point, $\lambda=1$ | Discrete-Laplace here |
|---|---|---|
| Full posteriors | $0,0,\tfrac12,1,1$ | $m,\tfrac12,M$ |
| Revealing flows | Yes, residual zero | No, residual $\ge\rho m\Delta_T$ |
| Off-path flows | NT, BNS, SNB each one | None (full support) |
| NT threshold | $\bar e\Delta_T/3$ | $\bar e\Delta_T/2$ |
| Full threshold | $\bar e\Delta_T/6$ | $c_T\Delta_T$, $c_T\approx0.227825$ |
| NT+T overlap | None (ordered intervals) | Yes, $r\in[1.515898,1.747878]$ |
| Partial zone | BNS+SNB, same interval | BNS only with recruitment |
| Ceiling $B$ at best flow | $g_H(r)=B_r(1)$ | $B_r(M)$, as in paper |
| Full entry, $c_L=0$ | $0.500000$ | $0.569293$ |
| Price pools, $c_L=0$ | None (floor holds) | None (floor holds) |

Three agreements deserve emphasis.

- Dominance kills wrong orders in both models.
  The proof is the accounting identity in each case.
- Price sufficiency needs a positive entry floor in both models.
  With $c_L=0$ the floor holds and pools vanish.
  The extra pool in the check memo §3.5 uses $c_L=1$.
  It has no counterpart here.
- Recruitment breaks BNS–SNB symmetry in both models.
  Literature claim C7 uses $\lambda<1$ and flow $X=1$ entry.
  It finds BNS alone for $\lambda\in[82/141,6/7]$ (pure scope).
  The check memo confirms that window for pure outcomes.
  Here $\lambda=1$ already breaks symmetry (Result 4).
  Overlapping geometric tails replace the presence device.
  Interior flows stay informative without $\lambda<1$.

Three differences drive the new results.

- No flow reveals the class here.
  So the recruiting region still pays the trader.
  Feedback can raise full gain above the NT deviation gain.
  In the three-point case the recruiting flow pays zero.
  Sell-only Claim 7 and Claim 8(a) prove feedback neutrality there.
- No flow is off path here.
  Three-point NT needs the Intuitive-Criterion belief at $X=\pm2$.
  Literature claims C2–C4 show the cutoff moves by factor $3/2$.
  Here Bayes rule prices every integer flow.
- Mixed profiles create partial posteriors in both models.
  The check memo §3.4 gives a three-point mixed counterexample.
  It refutes pure-only readings of claim C1 and window C7.
  Result 5 applies the same caution here.
  Corner windows alone do not describe all mixtures.

Sell-only Claim 13 (shift identity) has a partial echo here.
Full buy-only and full sell-only experiments coincide up to a shift.
Their trader gains coincide at full one-sided trade.
Two-sided full trade is a different experiment.
It cuts false good news from $\alpha$ to $\delta$ under $L$.
Entry falls from $0.625$ (buy-only) to $0.569293$ (two-sided).
Ownership stays $0.358422$ in both cases.
Sorting improves because $\Pr(+\mid L)$ falls.

One brief candidate needs a qualification after menu enlargement.
Brief §0 claims unique full buying at $r_1$ in the buy-only menu.
That claim is correct inside the buy-only menu (edge $v=0$ here).
In the two-sided menu, $(1,0)$ fails at $r_1$.
Type $L$ deviates to sell: net gain is $+0.123539$ for $c_H=5$.
The unique outcome becomes full two-sided trade instead.
Entry, ceiling, and $c_H$ window all change with the menu.

## 5. Numerical example

Benchmark: $h=10,\ell=1,p=0.5,\rho=0.25,b=2,k=0.02,c_L=0$.
Auction values at key strengths (script `posteriors.py`, 50 digits):

| $r$ | $\Delta_T$ | $B_r(1/2)$ | $B_r(M_1)$ | $B_r(M)$ | $\tau$ ($c_H{=}5$) | $\tau$ ($c_H{=}6$) |
|---|---|---|---|---|---|---|
| $1.2$ | $0.016667$ | $4.804167$ | $5.904260$ | $6.879843$ | $0.521800$ | $0.633117$ |
| $1.55$ | $0.097581$ | $4.693145$ | $5.783329$ | $6.750126$ | $0.534469$ | $0.646798$ |
| $3.0$ | $0.666667$ | $4.291667$ | $5.312161$ | $6.217155$ | $0.585000$ | $0.705000$ |
| $3.6$ | $0.938889$ | $4.134722$ | $5.121880$ | $5.997311$ | $0.607340$ | $0.731392$ |

Checks for Proposition C1.1 at $(r_0,r_1)=(1.2,3)$:

- $\Delta_T(r_0)=0.016667<0.02=k$.
- $\rho m\Delta_T(r_1)\approx0.044824>k$.
- Paper bound $(1-1/b)\rho m\Delta_T(r_1)\approx0.022412>k$ also holds.
- $c_H$ window is $(4.804167,6.217155]$.
- Prices under full trade at $r_1$ are distinct.
  $P_+\approx1.362372$, $P_0=0.614583$, $P_-\approx0.576074$.
  Values $t_0=0.416667<t_L=0.875<t_H=1.541667$ bracket them.

Equilibrium outcomes at benchmark strengths (baseline ties):

| Case | $r_0=1.2$ | $r_1=3$ | $r_2=3.6$ |
|---|---|---|---|
| $c_H=5$ orders | $(0,0)$ unique | $(1,-1)$ unique | $(1,-1)$ unique |
| $c_H=5$ $\mathsf E$ | $0.250000$ | $0.569293$ | $0.569293$ |
| $c_H=6$ orders | $(0,0)$ unique | $(1,-1)$ unique | $(1,-1)$ unique |
| $c_H=6$ $\mathsf E$ | $0.250000$ | $0.569293$ | $0.250000$ |
| Paper $\mathsf E$ | $0.250000$ | $0.522757$ | $0.250000$ |
| Buy-only $\mathsf E$ ($c_H{=}5$) | $0.250000$ | $0.625000$ | $0.625000$ |

Ownership $\mathsf O_H$ is $0.125$ at $r_0$ in each row.
It is $0.358422$ at $r_1$ for two-sided and buy-only trade.
Paper ownership at $r_1$ is $0.324192$ for comparison.
Return to $\rho$ at $3.6$ holds for $c_H=6$, not for $c_H=5$.
Ceilings are $3.592659$ ($c_H=6$) and $6.325302$ ($c_H=5$).

Coexistence at paper strengths (net gains, both $c_H$ values):

| $r$ | NT net (each type) | T net (each type) | $\mathsf E$ NT / T |
|---|---|---|---|
| $1.55$ | $-0.007802$ | $+0.002231$ | $0.250$ / $0.569$ |
| $1.60$ | $-0.005938$ | $+0.005630$ | $0.250$ / $0.569$ |
| $1.65$ | $-0.003996$ | $+0.009169$ | $0.250$ / $0.569$ |

Nets coincide across $c_H\in\{5,6\}$ at these corners.
Entry patterns coincide there: $(1,\rho,\rho)$ under T, $\rho$ under NT.
Paper entries on its branch are $0.545053,0.548756,0.551361$.
Discrete full entry is higher and flat.
Branch tables in Result 5 give mixing-branch entries.

Scripts (print only, run from repository root):

- `scripts/C1_two_sided/posteriors.py` — 50-digit posteriors,
  windows, ceilings, endpoint gains. Seconds.
- `scripts/C1_two_sided/equilibria.py` — corners, edge scans
  (400 points per segment), $81\times81$ grids. Under a minute.
- `scripts/C1_two_sided/branches.py` — Newton interior search
  (81 starts), jump solves, branch values. Under a minute.
- `scripts/C1_two_sided/sweep.py` — $r$ sweep step $0.01$,
  corner windows, baseline root bisections. Seconds.

Outputs sit beside each script as `*_out.txt` files.
Double precision in search scripts is a diagnostic only.
Headline constants come from the 50-digit script.
No script took over 60 seconds, so no slot wrapper was needed.

## 6. Open issues

- **Full correspondence proof (open).** Interior and edge claims rest
  on grids and Newton starts. A proof needs sign results for
  $\partial G_H/\partial u$, $\partial G_H/\partial v$ and mirrors
  inside each entry polygon. Grid coefficients suggest clean signs.
  At constant entry $\rho$, grid max is $0.125$ at $(0,0)$.
  Grid min is about $0.102210$ near $(0.9,1)$ and $(1,0.9)$.
  Analytic proofs of those extrema would close the gap.
- **Exact uniqueness thresholds (open).** Sufficient bounds are
  $1.220998$ and $2.124148$. Diagnostics suggest full uniqueness
  by $r=1.9$. Exact thresholds need cell-wise extrema with $\tau(r)$.
- **Tie rules (open as modelling choice).** Challenger mixing
  branches fail under baseline ties. Investor mixtures fail under
  the prescribed tie. The paper tie (prepare) plus pure Laplace
  orders avoid atoms. A discrete paper draft must choose and state
  both rules, as prior memos also warn.
- **General prior and presence (open).** Posteriors for $\pi\ne1/2$
  are in Result 1. Equilibria, $\lambda<1$, and Reading N with
  nondegenerate $G_H,G_L$ are not solved here.
- **Welfare and sale terms (open).** Ownership sorting improves
  versus buy-only trade ($\delta<\alpha$ false positives).
  Total surplus, seller proceeds, and reserve choice are not computed.
- **Order size (open).** Orders are unit only. Larger grids
  $\{-1,-\tfrac12,0,\tfrac12,1\}$ may smooth the entry jump.
  They may also restore interior magnitudes as in the paper.
  That extension may change the entry-order verdict.

## 7. Plain summary

Noise traders send many small buy and sell orders.
The net noise follows a discrete Laplace law.
The informed investor can buy one unit, sell one unit, or wait.
Only three beliefs can occur: bad, neutral, and good.
Strong buying and selling give beliefs $0.269$ and $0.731$.
No order flow proves the true class.

With a weak incumbent, trade does not pay.
Only the cheap challenger prepares.
With a strong incumbent, good-news buying and bad-news selling both pay.
The expensive challenger then prepares after good news.
Entry rises from $0.25$ to $0.569$.
With a still stronger incumbent, even good news is too weak.
Entry falls back to $0.25$ while trade stays active.

At middle strengths, silence and active trade are both self-confirming.
If nobody trades, one trade alone does not pay.
If both sides trade, good news recruits entry and trade pays well.
Buying benefits more from recruited entry than selling does.
So buy-only trade can stand alone, but sell-only trade cannot.
Full buys with mixed sells occur only near one threshold.
Wider mixed cases need the challenger to mix when indifferent.
Entry does not rise steadily on those wider cases.



