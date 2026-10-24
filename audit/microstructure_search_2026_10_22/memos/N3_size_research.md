# N3: Order size and research in the order slot

## 1. Question

Can order size or costly research restore the features that the unit slot loses?
Three extensions give different answers.

- Size choice restores a rising branch and smaller expected sales, but it loses uniqueness against strong incumbents.
- Research with a success ceiling restores rising entry and preserves the unique return to the floor.
- Research without that ceiling excludes floor entry at 3.6 under the same research cost.

The second extension ranks first.
Its positive branch has strict trade choices and an interior research choice.
It therefore needs no investor indifference between trade and abstention.

### Common setup and evidence

The auction source is `overleaf/paper`, commit `01bd5d6`, `main.tex`, Sections 2–4 and Appendix A.1.
I checked the formulas against equations (4), (9)–(11).
The noise discussion is in `online_appendix.tex`, A.6.
I use Reading N, point masses, and all benchmark auction primitives:

$$
(h,\ell,p,\rho,c_L,c_H,k,\pi)
=(10,1,1/2,1/4,0,6,1/50,1/2).
$$

There is one public slot and no separate noise.
An informed investor fills it with probability $\lambda$.
Otherwise, a separate trader with an exogenous liquidity motive fills it.
The investor has no initial stake.

Write $\Delta=\Delta_T$.
Direct auction integration gives

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&g_H&=h-t_H,&g_L&=\ell-t_L,\\
\Delta&=(r-1)^2/(2r),&
\tau(r)&=\frac{48r-3}{4(20r-r^2-1)}.
\end{aligned}
$$

For example, $t_H=r^{-1}[\int_0^p p\,du+\int_p^r u\,du]$.
For $t_L$, replace the integrand above $\ell$ by $\ell$.
The identities $t_j+g_j=\theta_j$ give both acquisition profits.

Competitive market makers observe the order $q$.
The challenger observes the price and its cost.
For a liquidity law $\eta$ and informed strategies $\sigma_j$, define

$$
\begin{aligned}
f_j(q)&=(1-\lambda)\eta(q)+\lambda\sigma_j(q),\\
\mu_q&=\frac{f_H(q)}{f_H(q)+f_L(q)},\\
e_q&=\rho+(1-\rho)\mathbf1\{\mu_q\ge\tau(r)\},\\
P_q&=t_0+e_q[t_L-t_0+\Delta\mu_q],\\
U_H(q)&=q e_q\Delta(1-\mu_q)-k|q|,\\
U_L(q)&=-q e_q\Delta\mu_q-k|q|.
\end{aligned}
\tag{1}
$$

These are conditional trade payoffs, given an informed slot.
Every allowed order has positive liquidity mass in the examples.
Thus Bayes' rule determines every feasible belief.
No result uses an off-path belief.

The equilibrium concept is perfect Bayesian equilibrium.
Each deviation faces the fixed candidate price and entry schedule.
The default investor rule permits mixtures among maximizing orders.
The alternative rule selects zero when zero ties with trade.
The default challenger rule requires preparation at indifference.
The alternative rule permits a mixture there.

Wrong-signed orders strictly lose because $0<\mu_q<1$ and $e_q\ge\rho>0$.
Equation (1) therefore excludes high-class sales and low-class purchases.
The price reveals the posterior through equation (10) of the pinned paper.
This remains true when several orders share one posterior.

The new program is `scripts/N3_size_research/derive_extensions.py`.
It does not import the earlier exploratory programs.
Its output is `scripts/N3_size_research/derived_results.txt`.
The earlier programs and their output remain unchecked background.

## 2. Extensions developed

### 2.1 Extension A: size choice and a change in the active size — computer-assisted

#### Model change

The informed menu is $\{-2,-1,0,1,2\}$.
The cost remains $k|q|$.
Set

$$
\lambda=\frac15,\qquad
\eta(\pm1)=\frac1{20},\qquad
\eta(\pm2)=\frac5{28},\qquad
\eta(0)=\frac{19}{35}.
\tag{2}
$$

These probabilities sum to one.
The common liquidity masses are

$$
b_1=(1-\lambda)\eta(1)=\frac1{25},\qquad
b_2=(1-\lambda)\eta(2)=\frac17.
$$

Large liquidity orders are more common than small liquidity orders.
This supplies distinct concealment at the two sizes.
Easley–O'Hara motivates the size question only.
Its exact menu and probabilities remain unverified in `L1_survey.md`, M03, which has abstract evidence only.

#### Derivation: a rising small-order branch

Let $A_m=\lambda\sigma_H(m)$ and $S_m=\lambda\sigma_L(-m)$ for $m\in\{1,2\}$.
The positive and negative posteriors are

$$
\mu_{+m}=\frac{b_m+A_m}{2b_m+A_m},\qquad
\mu_{-m}=\frac{b_m}{2b_m+S_m}.
\tag{3}
$$

Their trade payoffs are

$$
U_H(m)=m\left[e_{+m}\Delta\frac{b_m}{2b_m+A_m}-k\right],\qquad
U_L(-m)=m\left[\rho\Delta\frac{b_m}{2b_m+S_m}-k\right].
\tag{4}
$$

At each requested middle strength, $\rho\Delta/2-k<0$.
Every sale therefore loses, whatever its size.
Consider $S_1=S_2=A_2=0$, with a mixture between $+1$ and zero.
The unused size-two purchase has posterior $1/2$ and negative payoff.
Zero has a posterior below $1/2$.

Entry after $+1$ equals one on the proposed branch.
Purchase indifference gives

$$
\Delta\frac{b_1}{2b_1+A_1}=k
\quad\Longrightarrow\quad
A_1=b_1\left(\frac\Delta k-2\right),\qquad
\mu_{+1}=1-\frac k\Delta.
\tag{5}
$$

The program prints every order payoff, not just this identity.
The exact values are:

| $r$ | $\sigma_H(1)=A_1/\lambda$ | $\mu_{+1}$ | Aggregate entry $\mathsf E$ |
|---|---:|---:|---:|
| $31/20$ | $357/620$ | $481/605$ | $1603/4960=0.323185484$ |
| $8/5$ | $29/40$ | $37/45$ | $107/320=0.334375000$ |
| $33/20$ | $581/660$ | $713/845$ | $609/1760=0.346022727$ |

All three purchase probabilities lie strictly between zero and one.
Each posterior strictly exceeds its preparation threshold.
Every unused nonzero order has negative payoff for its relevant class.
Thus these are equilibria under investor mixtures and either challenger rule.

Only $+1$ recruits the high-cost challenger.
Its unconditional probability is $b_1+A_1/2$.
Therefore

$$
\mathsf E
=\rho+(1-\rho)(b_1+A_1/2)
=\frac14+\frac34\Delta(r).
\tag{6}
$$

This expression rises strictly with $r$.
The branch exists throughout $[1.55,1.65]$.
To see this, $A_1$ rises with $\Delta$ and stays between its displayed endpoint values.
Also $\mu_{+1}\ge481/605>7620/11711\ge\tau(r)$ on that interval.
The low-class sale and the unused large purchase stay unprofitable since $\rho\Delta/2-k<0$ at 1.65.

No informed trade also remains an equilibrium throughout that interval.
All its posteriors equal $1/2$, and each order earns its size times $\rho\Delta/2-k<0$.
The branch does need investor indifference with zero.
The alternative investor rule removes it.

#### Derivation: large purchases and smaller expected sales at 3

Let the high class buy two for sure.
The maximum posterior in this candidate is

$$
\mu_{+2}=\frac{b_2+\lambda}{2b_2+\lambda}=\frac{12}{17}>\tau(3)=\frac{141}{200}.
$$

Its net purchase payoff is $449/1275=0.352156863$.
A size-one deviation earns $19/300=0.063333333$.
Thus the large purchase is strict.

The low class uses both sale sizes.
Let $x=S_1$ and $S_2=1/5-x$.
The common positive payoff solves

$$
\underbrace{\frac{\rho\Delta b_1}{2b_1+x}-k}_{U_L(-1)}
=
\underbrace{2\left[\frac{\rho\Delta b_2}{2b_2+1/5-x}-k\right]}_{U_L(-2)}.
\tag{7}
$$

The left side falls strictly with $x$.
The right side rises strictly with $x$.
Their difference equals $9/1700>0$ at zero and $-43/350<0$ at $1/5$.
Thus there is exactly one root.

Exact rational bisection encloses that root.
The program retains its full rational endpoints.
It gives

$$
\sigma_L(-1)\approx0.022234398770,\qquad
\sigma_L(-2)\approx0.977765601230,\qquad
U_L\approx0.058945091708>0.
$$

Every remaining low-class order is worse.
Its expected sale size is $1.977765601230<2$.
After division by the maximum size, the expected order pair is approximately $(1,-0.988882800615)$.
This is a mixture over two sizes, not a deterministic fractional sale.
It is a small asymmetry.

A pure size-one sale cannot accompany a size-two purchase here.
An unused size-two sale has posterior $1/2$.
At 3 its payoff is $2(19/300)$.
A size-one sale earns at most $19/300$.
Thus the unused large sale gives a strict profitable deviation.
This exclusion also holds for any positive liquidity weights at these orders.

#### Derivation: a floor equilibrium at 3.6, with a competing equilibrium

At $18/5$, let the classes use $+2$ and $-2$ for sure.
The posteriors are $12/17$, $5/17$, and $1/2$.
All lie below $\tau(18/5)=4245/5804$.
The size-two payoff for either class is $3001/30600$.
The unused size-one payoff is $701/7200$.
Their difference is $29/40800>0$.
Thus this informative floor equilibrium is strict.

The posterior cap of T6 does not bind all candidate sizes here.
A full size-one purchase has posterior $6/7$.
The proposed floor equilibrium leaves that size unused by informed trade.
At the middle strengths, the small order instead carries the information.
The effective signal therefore changes with the active size.

However, this does not restore a unique return to the floor.
At 3.6 another equilibrium uses both purchase sizes.
Let $x=A_1$ and $A_2=1/5-x$.
Set entry to one after $+1$ and to $\rho$ elsewhere.
The purchase equality is

$$
\frac{\Delta b_1}{2b_1+x}-k
=2\left[\frac{\rho\Delta b_2}{2b_2+1/5-x}-k\right].
\tag{8}
$$

Its left side falls and its right side rises.
Opposite rational endpoint signs give one root.
At that root, the program gives

$$
\begin{aligned}
\sigma_H(1)&\approx0.687784472341,&
\sigma_H(2)&\approx0.312215527659,\\
\mu_{+1}&\approx0.816140048801,&
\mu_{+2}&\approx0.589676547306,\\
U_H&\approx0.152624065293,&
\mathsf E&\approx0.331583835426>\rho.
\end{aligned}
$$

The low class strictly sells two.
The posteriors justify the stated entry pattern.
The program prints positive active payoffs and strictly worse unused payoffs.
A second equilibrium also exists at 3, with entry about $0.333877967986$.
No claim here exhausts the size-game correspondence.

T6's unit-menu constraint remains correct.
Size choice escapes it for a selected branch by a change in the active size.
The same change also permits an equilibrium that violates floor entry at 3.6.

#### Price access, prediction, and scorecard

At 3 with the price hidden, both classes use the sale-size mixture from equation (7), with opposite signs.
Their common payoff is positive.
Entry equals $\rho$.
These strategies solve the hidden-price game itself.

With access, the high class instead buys two.
The exact proceeds gain is $379/2240$.
The surplus gain before trade costs is $37/2240$.
If $k$ is a resource cost, subtract $kx/2$ from the latter gain.
The resulting gain is about $0.016473388345>0$.
Liquidity costs are absent from the objective; an unchanged liquidity cost would cancel.

The prediction is conditional on the selected branch.
Small purchases carry more information than large purchases at the middle strengths.
Large purchases carry more information in the selected strong equilibrium.
Thus size and information need not move together across strengths.

| Scorecard item | Verdict |
|---|---|
| 1. Weak incumbent | Unique no informed trade at 1.2, since $\Delta<k$ per unit. |
| 2. Strong incumbent | Trade and entry $121/280$ at 3; another equilibrium also exists. |
| 3. Very strong incumbent | A strict informative floor equilibrium at 3.6; another equilibrium has extra entry. Uniqueness fails. |
| 4. Coexistence | No trade and a rising branch coexist throughout 1.55–1.65. |
| 5. Price access | Positive proceeds and net surplus gains for the stated equilibrium pair. |
| 6. Beliefs | Every order has liquidity support; no off-path rule. |
| 7. Ties | Middle branch needs investor mixtures with zero. Strong sale asymmetry uses a positive-payoff mixture across sizes. No challenger tie. |
| 8. Knobs | Size weights and $\lambda$ in equation (2). No open parameter box is certified. |
| 9. Precedent | Size-dependent inference has abstract evidence. This exact device is unverified. |
| 10. Status | Computer-assisted; exact middle formulas and rational root brackets for the strong cases. |

### 2.2 Extension B: costly research with a success ceiling — analytical

#### Model change and research incentives

Return to the unit menu $\{-1,0,1\}$.
Liquidity sells, waits, and buys with equal probabilities.
The investor chooses private research effort before it learns the class.
Effort determines the success probability $\lambda\in[0,\bar\lambda]$, where $\bar\lambda=6/17$.
Successful research reveals the class exactly.
The informed investor then fills the slot.
After failure, a separate liquidity trader fills it instead.
The researcher receives no trade payoff on that failure branch.

Thus $\lambda$ remains the probability of an informed investor in the slot.
Its bound describes a technological limit on research success.
It does not bound the fraction of orders that are informed.
Set

$$
C(\lambda)=\frac a2\lambda^2,\qquad a=\frac1{40}.
\tag{9}
$$

The cost is paid before success and does not depend on the class.
The alternative-arrival structure and costly research have verified precedent in `L1_survey.md`, C09, Dow–Gorton.
The quadratic cost and this success ceiling are new assumptions.
There is no strategic uninformed trader on the failure branch.

Let $V_r$ denote the expected optimal trade profit conditional on successful research, before research cost.
Given fixed prices, a private deviation to success probability $z$ earns

$$
zV_r-\frac a2z^2.
$$

This objective is strictly concave.
Its global optimum is

$$
\lambda=\min\{\bar\lambda,V_r/a\}.
\tag{10}
$$

Prices stay fixed under this deviation.
Thus the first-order condition is $a\lambda=V_r$.
The derivative of the re-solved product $\lambda V_r(\lambda)$ is not the research incentive.

#### Derivation: research and entry rise together at intermediate strengths

For $r\in[1.55,1.65]$, the low class cannot profit from a sale.
Its maximum gross return is $\rho\Delta/2<k$.
If research is positive, its conditional value must be positive by equation (10).
The high class must then buy for sure after success.
Otherwise, a mixture with zero would give $V_r=0$ and imply zero effort.

Write $d(\lambda)=(1-\lambda)/(2+\lambda)$.
With a full purchase and no sale,

$$
\mu_+=\frac{1+2\lambda}{2+\lambda}=1-d(\lambda),\qquad
\mu_0=d(\lambda),\qquad \mu_-=\frac12.
$$

When $+1$ recruits, the research value is

$$
V_r(\lambda)=\frac12[\Delta(r)d(\lambda)-k].
$$

Equations (9)–(10) give

$$
F_r(\lambda):=
2a\lambda^2+(4a+k+\Delta)\lambda+2k-\Delta=0.
\tag{11}
$$

The constant is negative, and $F_r$ rises strictly for $\lambda\ge0$.
Hence it has one positive root:

$$
\lambda_R(r)=
\frac{-(4a+k+\Delta)+
\sqrt{(4a+k+\Delta)^2+8a(\Delta-2k)}}{4a}.
\tag{12}
$$

Simple rational brackets establish the relevant location:

| $r$ | Bracket for $\lambda_R$ | $F_r$ at lower endpoint | $F_r$ at upper endpoint |
|---|---|---|---|
| $31/20$ | $(1/4,251/1000)$ | $-3/49600$ | $112931/620000000$ |
| $8/5$ | $(293/1000,294/1000)$ | $-1701/20000000$ | $221/1250000$ |
| $33/20$ | $(332/1000,333/1000)$ | $-3569/20625000$ | $71437/660000000$ |

All roots lie strictly below $6/17$.
The first root exceeds $1/4$, so its purchase posterior exceeds $2/3$.
The largest preparation threshold is $7620/11711<2/3$.
Thus all three roots strictly recruit the high-cost challenger.
The active high-class profit equals $2a\lambda_R>0$.
The low class strictly abstains.
These are strict trade choices under either investor tie rule.

Implicit differentiation of equation (11) gives

$$
\lambda_R'(r)=
\frac{(1-\lambda_R)\Delta'(r)}
{4a\lambda_R+4a+k+\Delta(r)}>0.
\tag{13}
$$

The positive root therefore rises throughout the interval.
Its endpoints stay below capacity and above the largest recruitment threshold.
The whole interval supports this branch.

Only a purchase recruits.
Its unconditional probability is $(1-\lambda)/3+\lambda/2$.
Hence

$$
\boxed{\mathsf E_R(r)=\frac12+\frac{\lambda_R(r)}8},\qquad
\mathsf E_R'(r)=\lambda_R'(r)/8>0.
\tag{14}
$$

Exact rational root brackets give the decimal displays below.
These displays do not replace the brackets in the output.

| $r$ | Research success $\lambda_R$ | Purchase posterior | Entry $\mathsf E_R$ |
|---|---:|---:|---:|
| 1.55 | 0.250249322294 | 0.666814396841 | 0.531281165287 |
| 1.60 | 0.293324846156 | 0.691855623930 | 0.536665605770 |
| 1.65 | 0.332615237748 | 0.713889907152 | 0.541576904719 |

#### Derivation: complementarity and the complete middle correspondence

Zero research is another equilibrium at every strength in this interval.
Then all orders come from liquidity, all posteriors equal $1/2$, and every informed deviation would lose.
Successful research therefore has value zero against that schedule.
The research cost makes zero the unique effort response.

At a positive candidate success probability, purchases recruit exactly when

$$
\lambda\ge\lambda_E(r):=\frac{2\tau(r)-1}{2-\tau(r)}.
$$

At that threshold, entry increases the research value by

$$
\frac{(1-\rho)\Delta(r)[1-\tau(r)]}{2}>0.
\tag{15}
$$

This jump supplies complementarity between discovery and entry.
Within the recruited branch, congestion instead reduces the research return:

$$
\frac{\partial V_r}{\partial\lambda}
=-\frac{3\Delta}{2(2+\lambda)^2}<0.
$$

The complementarity is therefore a discrete entry effect, not a positive slope within that branch.

Under mandatory preparation at indifference, the two middle equilibria are exactly:

- Zero research, no informed trade, and entry $\rho$.
- Research $\lambda_R$, a strict high-class purchase, and entry from equation (14).

For completeness, below $\lambda_E$ a purchase cannot pay because $\rho\Delta d<k$.
Positive effort with a partial purchase also cannot pay the research cost.
Equation (11) has only one positive root.
At capacity, $V_r(\bar\lambda)<a\bar\lambda$, so capacity cannot be optimal here.
These facts exhaust the alternatives.

A challenger mixture adds one threshold equilibrium under the alternative challenger rule.
Set $\lambda=\lambda_E$ and solve the research condition for total entry after a purchase:

$$
e^*(r)=\frac{2a\lambda_E+k}{\Delta(r)[1-\tau(r)]}.
\tag{16}
$$

At the three strengths, $e^*$ is approximately $0.895040$, $0.784642$, and $0.696846$.
Each lies strictly between $\rho$ and one.
Their aggregate entry levels are approximately $0.488338$, $0.447830$, and $0.415581$.
This third branch has falling entry at the three points.
The desired rising branch needs no challenger tie.

The three requested rising points also survive an open range of research costs:

$$
\frac{1241}{57600}<a<\frac{150913279}{4526936200},
\quad\text{approximately }0.0215451<a<0.0333367.
\tag{17}
$$

The lower endpoint makes capacity slack at 1.65.
It follows from $V_{1.65}(\bar\lambda)/\bar\lambda$.
The upper endpoint makes recruitment strict at 1.55.
It follows from $[\Delta(1-\tau)-k]/(2\lambda_E)$ there.
The same comparisons hold at the other two points, as direct rational evaluation shows.
Equation (13) then orders their research and entry.
This range holds the success ceiling fixed.

#### Derivation: unique endpoint outcomes and price access

At 1.2, every unit order has gross residual at most $\Delta=1/60<k$.
Research has value zero against every candidate schedule.
Thus zero research is unique, and entry equals $\rho$.

For $0\le\lambda\le6/17$, every posterior is between $11/40$ and $29/40$.
This bound applies to every informed strategy, because each liquidity order has mass $(1-\lambda)/3$.
At 3 and 3.6, either correctly signed unit trade therefore earns at least

$$
\rho\Delta\frac{11}{40}-k>0.
$$

Both classes must trade after success.
The lower bound on their average profit exceeds the marginal research cost even at capacity:

$$
\begin{aligned}
r=3:&\quad \rho\Delta\frac{11}{40}-k-a\bar\lambda=\frac{347}{20400}>0,\\
r=18/5:&\quad \rho\Delta\frac{11}{40}-k-a\bar\lambda=\frac{17491}{489600}>0.
\end{aligned}
\tag{18}
$$

Thus capacity is the unique research choice at both strengths.
The unique order pair is $(1,-1)$ after success.
At 3, $29/40>141/200$, so entry is $37/68$.
At 3.6, $29/40<4245/5804$, so entry is $1/4$.
The price remains informative.
The ceiling on this capacity region is $(50+\sqrt{2529})/29\approx3.458247$.

With hidden prices at 3, the same bounds still force capacity research and both trades.
The research and trade costs therefore cancel from the access comparison.
Direct auction sums give

$$
\Delta\mathcal R_T=\frac{113}{408}>0,\qquad
\Delta\mathcal W=\frac5{68}>0.
\tag{19}
$$

Research itself need not improve welfare.
At 3.6 it changes no entry decision, so it changes no expected auction allocation.
Relative to a zero-research counterfactual, its resource cost alone lowers surplus by $9/5780$.
If informed trade costs also use resources, the total loss is $249/28900$.
This calculation excludes any liquidity cost or external value of research.

#### Reading, prediction, and scorecard

A stronger incumbent raises research on the positive branch.
More successful research raises the purchase posterior and entry.
This recovers rising entry without an investor mixture over trade and zero.
Low research and high research coexist because entry raises the value of discovery.

The prediction concerns information production as well as informed trade.
Within the positive branch, stronger incumbents raise research success, the frequency of informed purchases, and entry.
The technological ceiling is essential to the stated unique endpoint result.
Research does not recover partial low-class sales at the middle strengths.

| Scorecard item | Verdict |
|---|---|
| 1. Weak incumbent | Unique zero research, zero informed trade, and entry $1/4$. |
| 2. Strong incumbent | Unique capacity research and full trade; entry $37/68$; high-class ownership $23/68$. |
| 3. Very strong incumbent | Unique capacity research and informative trade; entry $1/4$ at 3.6. |
| 4. Coexistence | Zero research and the rising branch coexist throughout 1.55–1.65. |
| 5. Price access | Proceeds rise by $113/408$ and net surplus by $5/68$ at 3. |
| 6. Beliefs | Every allowed order has liquidity support. No off-path rule. |
| 7. Ties | Rising branch has strict trades under both investor rules. Challenger mixtures add a separate threshold branch. |
| 8. Knobs | Success ceiling $6/17$ and cost coefficient $a=1/40$; equation (17) gives an open cost interval. |
| 9. Precedent | Dow–Gorton verifies costly research and alternative arrivals. The exact cost and ceiling are unverified as a published specification. |
| 10. Status | Analytical. Exact rational computations supply the displayed root enclosures and outcomes. |

### 2.3 Extension C: research without the success ceiling — computer-assisted

#### Model change

Keep the research mechanism, cost, and unit menu of Extension B.
Permit $\lambda\in[0,1]$.
The first result changes only the success ceiling.
A second calculation uses $a=1/4$ to display the equilibrium choices that can arise without that ceiling.

#### Derivation: no floor equilibrium at 3.6 under the original research cost

First exclude $\lambda=1$.
Any nonzero correctly signed order on that path reveals the class and loses $k$ per unit.
Thus both classes must abstain in any conditional trade equilibrium there.
Research then has value zero, which cannot justify success probability one at a positive cost.
Hence any equilibrium has $\lambda<1$, and every order has liquidity support.

Suppose every order induces entry $\rho$ at $r=18/5$.
Every posterior must then be at most $\tau=4245/5804$.
This statement also allows challenger mixtures at a threshold.
A high-class purchase earns at least

$$
v_*:=\rho\Delta(1-\tau)-k=\frac{899467}{20894400}>0.
$$

Thus the high class buys for sure after success.
Its purchase posterior is $M(\lambda)=(1+2\lambda)/(2+\lambda)$.
Floor entry therefore requires

$$
\lambda\le\lambda_E=\frac{2686}{7363}<1.
$$

At a sale, the posterior is at least $1-M(\lambda)\ge1-\tau$.
The low class also earns at least $v_*>0$ and therefore sells for sure.
Consequently, the research value is at least $v_*$.
But the marginal research cost satisfies

$$
C'(\lambda)=\frac\lambda{40}\le\frac{1343}{147260}<v_*,\qquad
v_*-\frac{1343}{147260}
=\frac{5219716561}{153845467200}>0.
\tag{20}
$$

Every candidate with floor entry therefore gives a strict incentive to increase research.
The candidate success probability is below one, so this deviation is feasible.
Hence no equilibrium has floor entry at 3.6 under the original cost without the success ceiling.
This proof permits both challenger tie rules.

#### Derivation and exact computation

Consider full trades after success.
Let $e$ be total entry after a purchase.
A sale has entry $\rho$.
The research value is

$$
V_r(\lambda;e)=\frac{e+\rho}{2}\Delta(r)d(\lambda)-k.
$$

The research condition becomes

$$
(a\lambda+k)(2+\lambda)
=\frac{e+\rho}{2}\Delta(r)(1-\lambda).
\tag{21}
$$

For this second calculation, set $a=1/4$, so $C(\lambda)=\lambda^2/8$.
For fixed $e$, the left side rises and the right side falls.
A positive solution is unique on that piece.
The program isolates the roots for $e=\rho$ and $e=1$ with rational endpoints.
It then computes every order payoff and checks the entry pattern directly.

| $r$ | Entry after purchase $e$ | Research $\lambda$ | Purchase posterior | Aggregate entry |
|---|---:|---:|---:|---:|
| 3 | $\rho$ | 0.173505737518 | 0.619741393724 | 0.250000000000 |
| 3 | 1 | 0.366319417529 | 0.732208349483 | 0.545789927191 |
| 3.6 | $\rho$ | 0.239072475620 | 0.660159493422 | 0.250000000000 |
| 3.6 | 1 | 0.448586547489 | 0.774803364383 | 0.556073318436 |

All four rows have strict positive trade profits for both classes.
The smallest is about $0.024631941753$.
Their posteriors lie strictly on their stated entry sides.
Strict concavity of the private effort objective makes each research condition globally sufficient.
Thus all four rows are equilibria under both default tie rules.
These rows illustrate coexistence at strong incumbents under the larger research cost.

A challenger mixture adds a threshold candidate at each strength.
Its entry solves

$$
e^*=\frac{2(a\lambda_E+k)}{\Delta(1-\tau)}-\rho.
$$

At 3 and 3.6 it equals approximately $0.758311$ and $0.631858$.
Both lie strictly between $\rho$ and one.
The default challenger rule excludes these two threshold candidates.
No claim here exhausts other conditional trade patterns on $[0,1]$.

#### Reading, prediction, and scorecard

The high-research branch raises its success probability as the incumbent strengthens.
Its posterior at 3.6 exceeds the old cap of $0.731392$.
Entry therefore stays above the floor.
The low-research branch also exists at both strengths.
A comparison across different branches can reverse the research order, but the model does not select that comparison.

The prediction is branch-dependent research and entry after the same public strength shock.
Endogenous research can move the entry ceiling outward.
It does not impose the fixed information cap that Extension B retains.

| Scorecard item | Verdict |
|---|---|
| 1. Weak incumbent | Unique zero research and floor entry at 1.2, since $\Delta<k$. |
| 2. Strong incumbent | Low-research floor equilibrium and high-research recruiting equilibrium both exist at 3. |
| 3. Very strong incumbent | At $a=1/40$, floor entry is impossible. At $a=1/4$, floor and extra-entry equilibria coexist. |
| 4. Coexistence at middle strengths | Not classified for this cost calibration. |
| 5. Price access | Not compared across all research continuations. |
| 6. Beliefs | All allowed orders have liquidity mass in the constructed equilibria, since $\lambda<1$. |
| 7. Ties | The four reported equilibria use strict trade and entry choices. Challenger mixtures add threshold candidates. |
| 8. Knobs | Unrestricted success; $a=1/40$ for the impossibility result and $a=1/4$ for the equilibrium illustration. |
| 9. Precedent | The same verified alternative-arrival and research precedent as Extension B. Exact specification unverified. |
| 10. Status | Computer-assisted; rational root isolation and direct payoff enclosures. |

## 3. Ideas considered and dropped

- **A pure small sale against a large purchase.** The unused large sale defeats it under linear costs at 3.
- **An unchanged posterior cap for every size.** This would remove the rare small-order signal that supports Extension A's rising branch.
- **A public effort choice.** This changes the information in the effort announcement and requires a separate deviation analysis.
- **A freely strategic uninformed failure type.** It cannot supply the exogenous liquidity law without another motive, as T2 and X show.
- **A separate buy-only research extension.** It removes the low-class trade term but adds no stronger result than Extension B.
- **More dates or strategic incumbent orders.** These overlap with N2 and N4 and are outside this memo.

## 4. Ranking

1. **Extension B: research with a success ceiling.** Strongest result and proof. It restores rising entry with strict trade choices and unique endpoint outcomes.
2. **Extension A: size choice.** A useful mechanism and a clear limit. It restores selected lost features but admits extra entry at 3.6.
3. **Extension C: unrestricted research.** A useful negative control. It proves that the original research cost cannot preserve floor entry without a success ceiling.

The ranking concerns these specifications, not all possible size or research models.

## 5. Open issues

- The success ceiling needs an economic or empirical calibration.
- Equation (17) certifies a cost interval, not a joint open box in every primitive.
- Extension A's complete equilibrium correspondence remains open.
- A stronger sale asymmetry may need nonlinear costs or asymmetric liquidity motives.
- No result here gives a deterministic fractional sale on a continuous order menu.
- A continuous menu would require liquidity densities or off-path beliefs.
- The correspondence for unrestricted research and all strengths remains open.
- Research subsidies, several researchers, and private research costs require separate work.
- These are exploratory extensions. No paper file changes.

### Program use and reproducibility

I used the program through its CLI with the stated benchmark and examined its output.
The run used one slot and finished in less than one second.
It contains no assertions and runs no test suite.

```bash
bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh \
  .venv/bin/python \
  audit/microstructure_search_2026_10_22/scripts/N3_size_research/derive_extensions.py \
  > audit/microstructure_search_2026_10_22/scripts/N3_size_research/derived_results.txt
```

The program forms both class laws, every posterior, each price, and every available order payoff.
It uses exact fractions and rational intervals.
Root existence follows from opposite exact endpoint signs.
The monotonicity proofs in this memo supply root uniqueness.
The brackets enclose all strict comparisons that support the reported candidates.
The output gives software versions, source hashes, the pinned commit, and all benchmark inputs.
Displayed interval endpoints use exact outward decimal conversion.
Their printed widths are exact fractions.
Point estimates use floating-point conversion only after the exact calculation.
`scripts/N3_size_research/run_receipt.json` records the new file hashes and the output hash.
No independent second review is claimed.

## 6. Plain summary

Research gives the strongest extension.
The investor pays for a chance to learn the challenger's class.
A separate liquidity trader fills the slot after research fails.
Research success has a fixed technological ceiling of $6/17$.

At strengths 1.55, 1.60, and 1.65, successful research leads to a strict purchase after good news.
Research success rises from 0.2502 to 0.2933 to 0.3326.
Entry rises from 0.5313 to 0.5367 to 0.5416.
Zero research also remains an equilibrium.
Entry and research support each other because recruitment raises the private value of discovery.
These outcomes require no investor mixture between trade and zero.

At 1.2, zero research is unique.
At 3 and 3.6, research reaches its ceiling uniquely.
Entry equals 0.5441 at 3 and returns to 0.25 at 3.6.
Prices remain informative.
Price access raises proceeds and net surplus at 3.
Research still uses resources at 3.6 without a gain in auction allocation.

Size choice gives a second result.
Small informed purchases support a rising entry branch at the three middle strengths.
Large purchases support another equilibrium against strong incumbents.
At 3, the low class mixes over smaller and larger sales.
Its expected sale is slightly smaller than the high-class purchase.
However, another equilibrium retains extra entry at 3.6.
Size choice therefore restores the selected pattern, not a unique return to the floor.

Without the success ceiling, the same research cost makes floor entry impossible at 3.6.
At a higher research cost, low-research and high-research equilibria coexist there.
The research ceiling is a substantive assumption, not a consequence of endogenous information alone.
