# T2: A liquidity trader in the speculator slot

## 1. Question

Can an uninformed trader of the same order size remove revelation at extreme flows and recover the benchmark results?

**analytical.** Yes for Proposition 2, interior beliefs, a finite entry ceiling, and price-access welfare at the benchmark.
All three variants work on an open parameter strip.
The recommended case is V3 with a two-sided menu and equal liquidity probabilities.
It supports coexistence at all three requested intermediate strengths.
It does not reproduce their strictly upward entry order.

The paper source is `overleaf/paper` commit `01bd5d6`, `main.tex`, Sections 2–4, equations (4), (9)–(11), and Appendix A.6.
The noise comparison also uses `online_appendix.tex`, A.6.
The earlier discrete memos are reference results, not the current paper benchmark.
Their buy-only benchmark sometimes uses $c_H=5$; this memo uses $c_H=6$ throughout.

## 2. Setup

### 2.1 Auction and costs

I use Reading N and the point-mass benchmark.
The primitives are

$$
(h,\ell,p,\rho,c_L,c_H,k,\pi)
=(10,1,1/2,1/4,0,6,1/50,1/2).
$$

The incumbent value is uniform on $[0,r]$, with $1<r<10$.
Equation (4) at the pinned source gives

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&g_H&=h-t_H,\\
g_L&=\ell-t_L,&\Delta&=t_H-t_L=(r-1)^2/(2r).
\end{aligned}
$$

Here $\Delta$ denotes the paper's $\Delta_T$.
Define

$$
B_r(\mu)=g_L+\mu(g_H-g_L),\qquad
\tau(r)=\frac{6-g_L}{g_H-g_L}
=\frac{48r-3}{4(20r-r^2-1)}.
$$

The zero-cost challenger always prepares.
At the benchmark, $g_L=3/(8r)>0$, so this choice is strict.
Also $B_r(1/2)=5-r/4+1/(8r)<6$ for $1<r<10$.
Thus $\tau(r)>1/2$ throughout the stated auction domain.

### 2.2 The slot and the probability convention

A public opportunity permits one slot order.
With probability $\lambda$, an informed investor fills the slot and observes the class.
Otherwise, a liquidity trader fills it.
Its order has an exogenous liquidity motive and uses the same unit size.
The identity draw is independent of the class, costs, incumbent value, and separate noise.

The buy-only menu is $\{0,1\}$, with liquidity purchase probability $\beta$.
For two-sided orders, I first index the triple by the menu $(-1,0,1)$:

$$
\eta(-1)=\beta,\qquad \eta(0)=1-2\beta,\qquad \eta(1)=\beta.
\tag{1}
$$

The task's prose also permits the literal buy, sell, abstain order.
Section 3.9 covers that interpretation exactly.
The recommended example uses $\beta=1/3$, so both interpretations coincide.

The variants are:

| Variant | Informed menu | Separate noise | Reason |
|---|---|---|---|
| V1 | $\{0,1\}$ | Uniform on $\{-1,0,1\}$ | Add the slot device to the prior buy-only case. |
| V2 | $\{-1,0,1\}$ | Uniform on $\{-1,0,1\}$ | Retain the EGJ-style order and noise menus. |
| V3 buy | $\{0,1\}$ | None | Observe one slot order. |
| V3 two | $\{-1,0,1\}$ | None | Observe one slot order with both directions. |

Write $f$ for the separate noise mass; V3 uses $f(0)=1$.
Flow is $X=Q+Z$.
A zero order is an observed abstention at the public opportunity.
V3 is a one-opportunity model, not a continuous arrival model.

### 2.3 Equilibrium, beliefs, and ties

The equilibrium is perfect Bayesian equilibrium of the stated finite order game.
A deviation faces fixed candidate price and entry schedules.
Market makers set the conditional mean of terminal target proceeds.
The challenger observes the price and its cost.
Prepared bidders bid their true values.

Bayes' rule applies at every feasible flow in the parameter domains below.
No equilibrium or deviation requires an off-path flow belief there.
Prices outside the feasible image cannot be reached by an allowed order.

The default investor rule permits any mixture at indifference, denoted IM.
The alternative I0 requires zero at indifference.
The default challenger rule requires preparation at indifference, denoted C1.
The alternative CM permits any mixture at indifference.
Strict benchmark results hold under both pairs of rules.

### 2.4 What the informed payoff means

Let $I=1$ denote an informed slot arrival.
The investor trades only on that branch and pays $k|q|$ on its actual order.
Its conditional payoff is

$$
U_j(q\mid I=1)
=q\sum_z f(z)e(q+z)\Delta[\mathbf1\{j=H\}-\mu(q+z)]-k|q|.
\tag{2}
$$

Its ex ante payoff multiplies class-conditional profit by $\lambda$.
This multiplier does not alter its conditional action threshold.
A fee paid before the identity draw would define a different model.

An always-present investor can instead receive information with probability $\lambda$.
If an exogenous liquidity mandate fixes its uninformed order, equation (2) still governs its informed choice.
Its uninformed profit and order costs add terms independent of that informed choice.
If it freely chooses its uninformed order, the proposed liquidity probabilities need a separate incentive argument.
Section 3.7 gives that argument and documents its failure without a liquidity motive.

## 3. Results

### 3.1 Full support and bounded beliefs — analytical

Let $\sigma_j$ be any informed order distribution, including a mixed or incorrectly signed distribution.
The conditional flow mass is

$$
a_j(x)=C_x+\lambda\sum_q\sigma_j(q)f(x-q),\qquad
C_x=(1-\lambda)\sum_q\eta(q)f(x-q).
\tag{3}
$$

If $C_x>0$, each class gives flow $x$ positive mass under every strategy.
Let $F_x=\max_q f(x-q)$.
Since the strategic term lies between zero and $\lambda F_x$,

$$
\frac1{R_x}\le\frac{a_H(x)}{a_L(x)}\le R_x,
\qquad R_x=1+\frac{\lambda F_x}{C_x}<\infty.
\tag{4}
$$

Bayes' rule then implies

$$
\frac1{1+R_x}\le\mu(x)\le\frac{R_x}{1+R_x}.
\tag{5}
$$

For any prior in $(0,1)$, replace these endpoints by the corresponding posterior odds transforms.
Thus every posterior is interior, with a bound uniform over all informed strategies.

The exact domains and supports are:

| Variant | Domain | Feasible flows | Common positive mass |
|---|---|---|---|
| V1 | $0<\lambda<1$, $0<\beta<1$ | $-1,0,1,2$ | $3C_x/(1-\lambda)=(1-\beta,1,1,\beta)$ |
| V2 | $0<\lambda<1$, $0<\beta\le1/2$ | $-2,-1,0,1,2$ | $3C_x/(1-\lambda)=(\beta,1-\beta,1,1-\beta,\beta)$ |
| V3 buy | $0<\lambda<1$, $0<\beta<1$ | $0,1$ | $(1-\lambda)(1-\beta,\beta)$ |
| V3 two | $0<\lambda<1$, $0<\beta<1/2$ | $-1,0,1$ | $(1-\lambda)(\beta,1-2\beta,\beta)$ |

V2 allows $\beta=1/2$ because separate noise still covers zero flow.
V3 two does not: under full informed orders, zero flow then disappears.
At $\lambda=1$, the common component disappears and these uniform conclusions fail.
At $\beta=0$, the positive extreme can again reveal the high class.

Put $b=(1-\lambda)\beta$.
In V1, after the low-class investor's purchase is excluded, let $s$ be the effective high-class purchase rate.
At the top flow,

$$
a_H(2)=(b+s)/3,\qquad a_L(2)=b/3,\qquad
\mu(2)=\frac{b+s}{2b+s}<1.
\tag{6}
$$

The same posterior applies at flow 2 in V2 and at flow 1 in V3.
The recruiting flow therefore pays a strictly positive high-class residual.
Bounded separate noise alone does not force revelation after this slot device.

### 3.2 Price sufficiency and order direction — analytical

The source's price identity uses only competitive pricing and the entry floor:

$$
P=t_0+e(P)[t_L-t_0+\Delta\mu_X],\qquad
\mu_X=\frac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta}.
\tag{7}
$$

Since $e(P)\ge\rho>0$ and $\Delta>0$, the price reveals the flow posterior.
This proof permits atoms, jumps, and challenger mixtures.
The canonical price uses $e(\mu)=\rho+(1-\rho)\mathbf1\{\mu\ge\tau\}$.
It is strictly increasing in $\mu$.

The class-conditional residuals are

$$
A_H(x)=e(x)\Delta[1-\mu(x)]>0,\qquad
A_L(x)=e(x)\Delta\mu(x)>0.
\tag{8}
$$

A high-class sale and a low-class purchase lose before the positive trade cost.
Neither occurs in equilibrium.
Hence only the effective rates $s=\lambda\Pr(q=1\mid H,I=1)$ and
$t=\lambda\Pr(q=-1\mid L,I=1)$ remain.
The buy-only case has $t=0$.

### 3.3 Flow posteriors and actual informed returns — analytical

For V1 the posterior vector is

$$
\begin{array}{c|cccc}
x&-1&0&1&2\\\hline
\mu_x&\dfrac{1-b-s}{2(1-b)-s}&1/2&1/2&\dfrac{b+s}{2b+s}.
\end{array}
\tag{9}
$$

A high-class purchase reaches flows 0, 1, and 2 with equal probability.
Only flow 2 can recruit the high-cost challenger.
Therefore its gross return, conditional on an informed arrival, is

$$
K_H^{V1}(s)=\frac\Delta3\left[\rho+e_2\frac b{2b+s}\right].
\tag{10}
$$

This return changes with the purchase rate and with recruited entry.
The prior three-point failure, with zero return at the recruiting flow, disappears.

For V2 the posterior vector is

$$
\begin{array}{c|ccccc}
x&-2&-1&0&1&2\\\hline
\mu_x&\dfrac b{2b+t}&\dfrac{1-b-s}{2(1-b)-s}&1/2&
\dfrac{1-b}{2(1-b)-t}&\dfrac{b+s}{2b+s}.
\end{array}
\tag{11}
$$

Direct substitution into equation (2) gives

$$
\begin{aligned}
K_H^{V2}(s,t)&=\frac\Delta3\left[
\frac\rho2+e_1\frac{1-b-t}{2(1-b)-t}+e_2\frac b{2b+s}\right],\\
K_L^{V2}(s,t)&=\frac{\rho\Delta}3\left[
\frac b{2b+t}+\frac{1-b-s}{2(1-b)-s}+\frac12\right].
\end{aligned}
\tag{12}
$$

The negative flows never recruit because their posteriors do not exceed the prior.
The high-class purchase and low-class sale each reach flow zero with probability $1/3$.
Consequently,

$$
K_H^{V2},K_L^{V2}\ge\rho\Delta/6.
\tag{13}
$$

For V3 buy, the two posteriors equal the extreme entries in equation (9).
A purchase reaches only flow 1, rather than both posterior regions.
Thus

$$
K_H^{V3}(s)=\Delta e_+\frac b{2b+s}.
\tag{14}
$$

For V3 two, set $c=1-2b$.
The posteriors are

$$
\mu_- =\frac b{2b+t},\qquad
\mu_0=\frac{c-s}{2c-s-t},\qquad
\mu_+=\frac{b+s}{2b+s}.
\tag{15}
$$

Its informed returns are

$$
K_H^{V3}(s)=\Delta e_+\frac b{2b+s},\qquad
K_L^{V3}(t)=\rho\Delta\frac b{2b+t}.
\tag{16}
$$

The high-class and low-class order conditions therefore separate.
An entry response at zero flow does not affect either nonzero order's return.

### 3.4 Proposition 2 and the exact parameter strip — analytical

Define the full-purchase upper posterior and its ratio parameter by

$$
M=\frac{b+\lambda}{2b+\lambda},\qquad
u=\frac\lambda{(1-\lambda)\beta},\qquad M=\frac{1+u}{2+u}.
\tag{17}
$$

The symbol $\lambda$ retains only its presence meaning.
Exact auction arithmetic gives

$$
\tau(3)=\frac{141}{200},\qquad
\tau(18/5)=\frac{4245}{5804}.
$$

All three Proposition 2 outcomes hold, with strict entry decisions, on the strip

$$
\boxed{\frac{141}{200}<M<\frac{4245}{5804}}
\quad\Longleftrightarrow\quad
\boxed{\frac{82}{59}<u<\frac{2686}{1559}}.
\tag{18}
$$

Equivalently, for any admissible $\beta$,

$$
\boxed{
\frac{82\beta}{59+82\beta}<\lambda<
\frac{2686\beta}{1559+2686\beta}.}
\tag{19}
$$

Use the domains in Section 3.1.
For symmetric V2 and V3 two, this strip gives full purchases in class H and full sales in class L.
For buy-only variants, it gives full purchases in class H and zero purchases in class L.
The uniqueness claim covers mixtures over the stated menus, not continuous order sizes.

**Proof, weak incumbent.** At $r=6/5$, $\Delta=1/60<k=1/50$.
Every unit order's gross residual is at most $\Delta$.
Every nonzero informed order therefore loses against every candidate schedule.
Both classes choose zero, every posterior equals $1/2$, and entry equals $\rho$.
Liquidity orders can still occur; “no trade” here means no informed trade.

**Proof, V1 at the strong incumbent.** Equations (9)–(10) give $K_H^{V1}\ge\rho\Delta/3$ at every candidate.
At $r=3$,

$$
\rho\Delta/3-k=\frac8{225}>0.
$$

Thus the high-class investor must purchase fully.
The low-class investor never purchases, so the outcome is unique.
Condition (18) makes flow 2 recruit at $r=3$.

**Proof, V2 at the strong incumbent.** Equation (13) applies to both correctly signed orders under every candidate.
At $r=3$,

$$
\rho\Delta/6-k=\frac7{900}>0.
$$

Both classes must trade fully.
At full orders, put

$$
N=\frac{1-b}{2(1-b)-\lambda}.
\tag{20}
$$

The positive posteriors are $N$ and $M$.
Cross multiplication gives $M\ge N$ because $2b+\lambda\le1$.
Hence condition (18) makes at least flow 2 recruit.

**Proof, V3 at the strong incumbent.** In any candidate, each correctly signed order has residual fraction at least $1-M$.
The entry floor gives $K_j\ge\rho\Delta(1-M)$.
Condition (18) implies

$$
K_j-k>
\frac16\left(1-\frac{4245}{5804}\right)-\frac1{50}
=\frac{21563}{870600}>0.
$$

Thus every available correctly signed order is full.
For the two-sided menu, the zero-flow posterior then equals $1/2$.
Only positive flow recruits.

**Proof, very strong incumbent.** The spread rises from $r=3$ to $r=18/5$.
All preceding strict return bounds continue to apply.
The full-order maximum posterior is $M$ in each variant.
Condition (18) places it strictly below $\tau(18/5)$.
Thus entry returns to $\rho$ while the price stays informative.

Under C1, the lower bound in (18) can be weak.
Under CM, equality permits zero extra entry, so the strict lower bound ensures the result for every tie choice.
The upper bound must stay strict under C1.
No paper primitive needs a change for Proposition 2.

### 3.5 Entry, ownership, and the ceiling — analytical

Set $w=2b+\lambda$.
At $r=3$, V1 gives

$$
\mathsf E_{V1}=\frac14+\frac w8,\qquad
\mathsf O_{H,V1}=\frac18+\frac{b+\lambda}8.
\tag{21}
$$

The unconditional top-flow probability is $w/6$.
Its conditional probability in class H is $(b+\lambda)/3$.
Multiplication by $1-\rho=3/4$ and the class prior gives equation (21).

For symmetric V2, let $J=\mathbf1\{N\ge141/200\}$ under C1.
Its outcomes are

$$
\begin{aligned}
\mathsf E_{V2}&=\frac14+\frac{w+J(2-w)}8,\\
\mathsf O_{H,V2}&=\frac18+
\frac{b+\lambda+J(1-b)}8.
\end{aligned}
\tag{22}
$$

If both positive flows recruit, $\mathsf E_{V2}=1/2$ and $\mathsf O_{H,V2}=1/4+\lambda/8$.
At a middle-flow entry tie, replace $J$ by the challenger's CM preparation probability.
In terms of the two parameters, $J=1$ exactly when

$$
\beta\ge\frac{82}{82+59u}
$$

under C1.
This follows by substitution of $b=\beta/(1+u\beta)$ and cross multiplication in $N\ge141/200$.

Both V3 menus give

$$
\mathsf E_{V3}=\frac14+\frac{3w}8,\qquad
\mathsf O_{H,V3}=\frac18+\frac{3(b+\lambda)}8.
\tag{23}
$$

These ownership probabilities include the prior class probability.
Since $h>r$, every prepared high-class challenger wins.
At the weak incumbent, high-class ownership equals $1/8$.
Each expression above strictly exceeds that level.

The full-order maximum posterior is $M$ in all four cases.
The common equilibrium entry ceiling solves $B_r(M)=6$:

$$
r_C(M)=\frac{10M-6+
\sqrt{(10M-6)^2+M(3/4-M)}}M.
\tag{24}
$$

The relevant root is unique because $B_r(M)$ falls strictly in $r$.
Condition (18) gives $3<r_C<18/5$.
At $r_C$, C1 retains extra entry at the maximum-posterior flow.
Strictly above it, entry equals $\rho$.
This is an equilibrium ceiling in the full-order region, not a bound on arbitrary incorrect-sign strategies.

### 3.6 Coexistence, all tractable mixtures, and the missing entry order — analytical

Under no informed trade, every posterior equals $1/2$.
Each informed deviation has gross return $K_0=\rho\Delta/2$.
Define

$$
\mathfrak r(D)=1+D+\sqrt{D^2+2D},\qquad
r_N=\mathfrak r(2k/\rho)=\mathfrak r(4/25).
\tag{25}
$$

No informed trade is an equilibrium exactly when $r\le r_N$.
At equality, both IM and I0 permit the zero order.

**Why the two-sided low class abstains throughout coexistence.**
In V2, every posterior reached by a sale is at most $1/2$.
At least one becomes strictly smaller whenever either informed class trades.
Thus equation (12) gives $K_L<\rho\Delta/2\le k$ in any informative candidate with $r\le r_N$.
In V3, equation (16) gives $K_L(t)<\rho\Delta/2$ whenever $t>0$.
So no informative coexistence outcome has a positive low-class sale rate.

The high-class problem therefore has one form in all variants:

$$
K(s,e)=\Delta g\left[d+e\frac b{2b+s}\right],\qquad
(g,d)=
\begin{cases}
(1/3,\rho),&V1,V2,\\
(1,0),&V3\text{, either menu}.
\end{cases}
\tag{26}
$$

Here $e$ is entry at the upper flow.
This formula also describes V1 outside the coexistence region.
For V3 two, the independent low-class problem remains equation (16).

The recruitment rate and the payoff pieces are

$$
s^*=b\frac{2\tau-1}{1-\tau},\qquad
e=\rho\text{ below }s^*,\qquad e=1\text{ above }s^*.
\tag{27}
$$

On each piece,

$$
\frac{\partial K}{\partial s}
=-\frac{\Delta g e b}{(2b+s)^2}<0.
\tag{28}
$$

Every interior informed mixture on a fixed entry piece therefore has the exact rate

$$
s_e=b\left[\frac e{k/(\Delta g)-d}-2\right].
\tag{29}
$$

Retain this rate only when $0<s_e<\lambda$ and its entry piece is consistent.
At $s=s^*$, CM permits the unique entry rate

$$
e^*=\frac{k/(\Delta g)-d}{1-\tau},\qquad
\zeta^*=\frac{e^*-\rho}{1-\rho},
\tag{30}
$$

provided $\rho\le e^*\le1$.
Here $\zeta^*$ is the high-cost challenger's preparation probability.
C1 permits this threshold outcome only when $e^*=1$.
I0 excludes all interior informed mixtures.
Full purchase requires $K(\lambda,e(M))\ge k$ under IM and a strict inequality under I0.
Equations (27)–(30), the no-trade inequality, and the full-purchase inequality list every high-class outcome.

For V3 two, the exact low-class rate under IM is

$$
t=
\begin{cases}
0,&\rho\Delta/2\le k,\\
\lambda,&\rho\Delta b/(2b+\lambda)\ge k,\\
b(\rho\Delta/k-2),&\text{otherwise}.
\end{cases}
\tag{31}
$$

The first case includes its boundary; coincident boundary cases have the same rate.
Combine each admissible high-class rate with equation (31), then calculate the zero-flow posterior from equation (15).
This gives the V3 two correspondence even when zero flow induces extra entry.
The broader coupled V2 correspondence above $r_N$ remains open.

**The coexistence intervals.**
Define $r_A$ by

$$
\Delta(r_A)g[d+1-\tau(r_A)]=k,
\tag{32}
$$

and define

$$
r_F=\mathfrak r\left(\frac{k}{g[d+1-M]}\right).
\tag{33}
$$

On the working strip, $s^*<\lambda$ throughout $r\le r_N$.
Indeed, $\tau$ rises in $r$, and $\tau(r_N)<\tau(3)<M$.
The jump payoff at $s^*$ is the left side of equation (32).
It must reach $k$ before any informative outcome exists.

For completeness, that jump payoff rises strictly on $6/5\le r\le r_N<7/4$.
Put $y=r-1$, so $0<y<3/4$.
After positive denominators are removed, its derivative has the sign of

$$
\begin{cases}
y(1620+3888y+2664y^2+219y^3-170y^4+5y^5),&V1,V2,\\
y(972+2268y+1440y^2+3y^3-136y^4+4y^5),&V3.
\end{cases}
$$

Each polynomial is positive because its constant term exceeds the absolute negative term on $0<y<3/4$.
Specifically, $170(3/4)^4<1620$ and $136(3/4)^4<972$.
Equation (32) therefore has at most one root in that interval.
Its existence follows from these exact jump returns at $r=6/5$ and $r=5/3$:

$$
\frac{19}{5544}<\frac1{50}<\frac{637}{23940}\quad(V1,V2),
\qquad
\frac{113}{18480}<\frac1{50}<\frac{371}{7980}\quad(V3).
$$

Also $\Delta(5/3)=2/15<4/25$, so $5/3<r_N$.
Because $\tau(r_A)<M$, the jump return exceeds the full-purchase return at $r_A$.
Hence $r_A<r_F$.
On the strip, $g[d+1-M]>\rho/2$, so the full-purchase return exceeds $k$ at $r_N$.
Hence $r_F<r_N$.

Under IM and C1, no trade and informative trade coexist on $[r_A,r_N]$.
For $r_A<r<r_F$, informative trade uses the rate in equation (29) with $e=1$.
For $r_F\le r\le r_N$, full high-class purchases give an informative equilibrium.
At $r_A$, the investor and challenger are both indifferent at the recruitment threshold.
CM adds the threshold mixture from equation (30) in the interior of this coexistence interval.
Under I0, coexistence instead requires $r_F<r\le r_N$.

On the recruited interior branch,

$$
\mathsf E=\rho+
\frac{(1-\rho)g b\Delta}{2(k/g-d\Delta)}.
\tag{34}
$$

This expression rises strictly with $\Delta$, and hence with $r$.
Once the high-class purchase becomes full, entry stays constant until a preparation threshold changes.
At each strength with $r_A<r<r_N$, CM gives the strict order

$$
\mathsf E_{\rm no\ trade}<\mathsf E_{\rm threshold\ mixture}
<\mathsf E_{\rm recruited\ mixture\ or\ full}.
\tag{35}
$$

The first inequality follows from $e^*>\rho$.
The second follows from $e^*<1$ and $s^*<s_1\le\lambda$.
This within-strength order differs from Proposition 3's order across strengths.

**Failure at $r=31/20$ for V1 and V2.**
Even the largest recruiting return at that strength falls below the trade cost:

$$
\frac{\Delta(31/20)}3[\rho+1-\tau(31/20)]-k
=-\frac{44551}{117328800}<0.
\tag{36}
$$

Thus neither variant has any informative equilibrium at $1.55$ on the working strip.
This conclusion permits both investor and challenger mixtures.
The smallest reduction of $k$ that permits one is

$$
k\le\frac{92081}{4693152},
\qquad \frac1{50}-\frac{92081}{4693152}
=\frac{44551}{117328800}.
\tag{37}
$$

Equality requires IM and the challenger entry tie.
This change permits the missing first point; it does not establish the full upward triple.

**V3 at the requested strengths — computer-assisted.**
V3 supports no trade and full high-class purchases at $31/20,8/5,33/20$.
The full informative branch has the same entry at all three strengths.
Under CM, the additional threshold branch has strictly decreasing entry at those points; Section 5 gives exact fractions.
There are no other informative outcomes there by equations (27)–(31).
Therefore V3 also fails the strictly upward triple of Proposition 3 at the benchmark.
This failure holds throughout the working strip.
The full-purchase return at $31/20$ exceeds $\Delta(31/20)(1-4245/5804)$ throughout that strip.
This bound exceeds $k$ by $223499/35984800>0$.
For the threshold branch, equation (30) gives

$$
\mathsf E^*(r)=\rho+\frac b2
\left[\frac{k}{\Delta(r)[1-\tau(r)]^2}-\frac\rho{1-\tau(r)}\right].
$$

Its differences across the three strengths have signs independent of $b>0$.
Thus the exact decreasing order in Section 5 applies to every parameter pair in the strip.

### 3.7 A liquidity trader is not a free uninformed speculator — analytical

An uninformed investor with no initial stake knows only the prior.
If it freely selects $q$, its conditional return against the candidate schedules is

$$
U_U(q)=q\Delta\sum_z f(z)e(q+z)[1/2-\mu(q+z)]-k|q|.
\tag{38}
$$

In each full benchmark outcome, a purchase reaches only posterior values at least $1/2$.
A sale reaches only posterior values at most $1/2$.
Thus either nonzero uninformed order earns strictly negative profit after $k$.
Its preferred order is zero.
The same argument applies to the informative outcomes in the coexistence interval.

Consequently, the device requires an exogenous liquidity motive or a binding order mandate.
It is not an equilibrium model of a freely strategic uninformed speculator with the paper's one-date payoff.
An always-present but sometimes informed investor can implement it only if its uninformed branch has that extra motive.
Without it, the proposed $\beta>0$ cannot be sustained by these candidate schedules.
GG's verified two-date inventory mechanism does not supply this missing one-date incentive automatically.

### 3.8 Information and payoffs versus the buy-only geometric base — analytical

The earlier base has the exact sufficient signal $S=\mathbf1\{X\ge1\}$.
Its two posterior regions follow from the constant one-step noise ratio.
This is Lemma 1 in `C4_sequential.md` and Result 1 in `B_dlaplace_theory.md`.
An informed purchase reaches both regions.
By contrast, a V3 informed purchase reaches only its positive order flow.

For the geometric base, write $\gamma=1/(1+a)$, $\delta=2\gamma-1$, and let $v$ denote its effective high-class purchase rate.
At prior $1/2$ and no low-class purchase,

$$
N_+(v)=1-\gamma+\delta v/2,\quad N_-(v)=\gamma-\delta v/2,
$$
$$
K_{\rm base}(v)=\frac{\Delta\gamma(1-\gamma)}2
\left[\frac{e_+}{N_+(v)}+\frac{e_-}{N_-(v)}\right].
\tag{39}
$$

Result 3 of that memo gives the exact bounds, with a fully present informed investor,

$$
2\rho\gamma(1-\gamma)\Delta\le K_{\rm base}(v)\le\Delta/2.
\tag{40}
$$

The lower bound is an average over flows.
A pointwise bound on a posterior does not replace it.
Equations (10), (12), and (14) give the different actual order returns for the slot models.
An ex ante presence factor does not turn their conditional flow laws into the base's flow law.

At full high-class purchases, V3 buy with $\beta=1/2$ and $\lambda=(1-a)/(1+a)$ has the base's binary experiment.
Then $M=\gamma$, but $K_{\rm slot}=\Delta e_+(1-M)$ and $K_{\rm base}=\Delta M(1-M)(e_++e_-)$.
At $M=29/40$ and $r=3$, their hidden-price returns are $11/240$ and $319/4800$.
With recruited entry, they are $11/60$ and $319/1920$.
Thus identical posteriors and state-conditional signal probabilities do not imply identical trade thresholds.

### 3.9 The literal buy, sell, abstain interpretation — analytical

This subsection assigns the task's triple in its literal word order:

$$
\eta(1)=\beta,\qquad\eta(-1)=1-2\beta,\qquad\eta(0)=\beta,
\quad 0<\beta<1/2.
\tag{42}
$$

Put $b_+=(1-\lambda)\beta$ and $b_-=(1-\lambda)(1-2\beta)$.
All support and likelihood proofs remain valid because every liquidity menu probability is positive.
The upper-flow posterior remains $(b_++s)/(2b_++s)$.
The same open strip (18)–(19) applies with $b=b_+$.

For V2, replace the posterior at flow 1 by

$$
\mu_1=\frac{1-b_-}{2(1-b_-)-t}.
\tag{43}
$$

Replace $b$ by $b_-$ at flow $-2$.
Keep the formulas at flows $-1$, 0, and 2, with $b=b_+$.
The central-flow return bound still forces full correctly signed informed orders at $r=3$ and $18/5$.
At full orders,

$$
\mu_1=\frac{2+u}{4+u}<\frac{141}{200}
\quad\text{for}\quad \frac{82}{59}<u<\frac{2686}{1559}.
\tag{44}
$$

The inequality follows by cross multiplication; it suffices that $u<164/59$, which the strip implies.
Thus only the top flow recruits at $r=3$.
Literal V2 has exactly the entry and ownership in equation (21).
Its coexistence outcomes and the failure at $1.55$ remain those of Section 3.6.

For V3 two, the returns separate with $b_+$ in the high-class formula and $b_-$ in the low-class formula.
The high class purchases fully throughout the strong benchmark region.
The low-class rate under IM is

$$
t_3=\min\{\lambda,19b_-/3\},\qquad
t_{18/5}=\min\{\lambda,701b_-/72\}.
\tag{45}
$$

These expressions follow from $K_L(t)=k$ and the endpoint bounds in equation (31).
The zero-flow posterior cannot exceed $1/2$ because $s=\lambda\ge t$.
Thus entry, ownership, and the ceiling remain equations (23)–(24).
Full two-sided orders at both strengths require

$$
\frac\lambda{b_-}<\frac{19}3
\quad\Longleftrightarrow\quad
\beta<\frac{19}{38+3u}.
\tag{46}
$$

Equality also permits full orders under IM; the strict form covers I0.
If (46) fails, the low class mixes at $r=3$ under IM.
I0 then has no equilibrium there: zero gives a profitable sale, while a full sale loses.
The recommendation $\beta=1/3$, $\lambda=6/17$ satisfies (46) strictly.
It therefore gives the same scorecard under both probability conventions and both investor tie rules.

### 3.10 Access to prices — analytical

At $r=3$, hiding the price fixes entry at $\rho$, because $B_3(1/2)<6$.
The strict benchmark return bounds still force the same informed orders in both price regimes.
For literal V3 with a partial low-class sale, equation (45) is also the same in both regimes.
The liquidity law stays fixed.
Thus any resource cost of trade cancels from the welfare comparison.

Let $D_x=[a_H(x)+a_L(x)]/2$ and let $A$ denote flows that recruit the high-cost challenger.
An extra preparation decision raises proceeds by $t_j-t_0>0$.
Its expected allocation gain, net of its preparation cost, is

$$
B_r(\mu_x)-6+p^2/r.
$$

The $p^2/r$ term is the reserve gain when the incumbent fails its reserve.
Optimal extra entry gives $B_r(\mu_x)\ge6$.
At the benchmark, $p^2/r=1/12>0$.
Hence

$$
\begin{aligned}
\Delta\mathcal R_T
&=(1-\rho)\sum_{x\in A}D_x[t_L-t_0+\Delta\mu_x]>0,\\
\Delta\mathcal W
&=(1-\rho)\sum_{x\in A}D_x[B_r(\mu_x)-6+1/12]>0.
\end{aligned}
\tag{47}
$$

The strict strip makes $A$ have positive probability.
This proves the Proposition A.9 analog at $r=3$, with both regimes solved for their own equilibrium.
The claim does not cover every equilibrium at intermediate strengths.

### 3.11 Economic meaning and verified precedent — open

Here $\lambda$ is the probability that the slot contains an informed investor.
It is not generally the fraction of executed orders that are informed.
The parameter $\beta$ controls the liquidity trader's activity and direction probabilities.
Separate noise in V1 and V2 adds another source of noninformational orders.

For full two-sided orders in symmetric V3, define $\operatorname{PIN}_{\rm slot}$ as the informed fraction of nonzero slot orders.
It is

$$
\operatorname{PIN}_{\rm slot}
=\frac\lambda{\lambda+2(1-\lambda)\beta}=2M-1.
\tag{48}
$$

For V3 buy, the same formula follows because only half of informed identities submit a nonzero order.
Equation (18) requires

$$
\frac{41}{100}<\operatorname{PIN}_{\rm slot}<\frac{1343}{2902}.
\tag{49}
$$

Thus the model permits a direct calibration to an informed-order fraction and an inactivity rate.
It does not establish that an empirical PIN estimator identifies these objects.
No verified PIN estimate appears in the permitted records.
Every proposed empirical number here is **unverified**.
The example below is an illustrative input, not an empirical estimate.

The permitted source records support these narrower claims:

- `Q2_discrete_literature.md`, R1–R2: EGJ describes presence, a liquidity shock, and information with probability $\lambda$.
  Its third interpretation is not a solved version of the present exogenous liquidity rule.
- `LIT_extracts.md`, A2: Goldstein–Guembel has a freely strategic uninformed speculator and two trade dates.
  That model verifies a distinct inventory mechanism, not this fixed liquidity distribution.
- `LIT_extracts.md`, A7: Boleslavsky–Kelly–Taylor has one informed identity or one noise identity, without separate additive noise.
  This is the closest verified identity device for V3.
  Its orders and noise densities are continuous, so the exact finite menu remains a new specification here.
- `Q2_discrete_literature.md`, Table 2.1: Glosten–Milgrom is expressly unverified in that record.
  I therefore do not claim verified precedent from that paper or from a PIN estimate.

The exact proposed finite device's publication precedent stays open.
The linked source records verify adjacent devices, not every specification in this memo.

## 4. Scorecard

Each table uses the example $\beta=1/3$, $\lambda=6/17$.
It lies strictly inside (18), and both probability conventions agree there.
All decimals below are displays of exact quantities or rational root brackets.

### V1: buy-only, separate three-point noise

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique no informed trade at $6/5$; entry $1/4$. | analytical |
| 2. Prop. 2(ii) | Unique full high-class purchase at 3; entry $71/204$; high-class ownership $10/51$. | analytical |
| 3. Prop. 2(iii) | Full high-class purchase at $18/5$; entry $1/4$; $r_C=(50+\sqrt{2529})/29$. | analytical |
| 4. Prop. 3 | IM coexistence $[r_A,r_N]$, about $[1.5565944,1.7478775]$; excludes 1.55. Entry rises on $(r_A,r_F)$, then stays flat. | analytical |
| 5. Prop. A.9 | At 3, proceeds rise by $113/1224$ and net surplus by $5/204$. | analytical |
| 6. Off-path beliefs | None on the stated domain; top flow is interior under every strategy. | analytical |
| 7. Ties and mixtures | Equations (27)–(30) give all rates; I0 coexistence needs $r_F<r\le r_N$. | analytical |
| 8. Knob and range | $0<\beta<1$ and (19); $\lambda$ governs identity, $\beta$ liquidity activity. | analytical |
| 9. Exact literature device | EGJ interpretations and alternative trader identities are verified; this precise finite device is not. | open |
| 10. Evidence | Proofs above; exact rational example and root brackets in the saved output. | computer-assisted |

### V2: two-sided, separate three-point noise

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique zero informed orders at $6/5$; entry $1/4$. | analytical |
| 2. Prop. 2(ii) | Unique full purchases and sales at 3; entry $71/204$; ownership $10/51$. Equation (22) gives larger symmetric cases. | analytical |
| 3. Prop. 2(iii) | Full informed purchases and sales at $18/5$; entry $1/4$; same $r_C$. | analytical |
| 4. Prop. 3 | Low class abstains on every coexistence outcome; interval and entry order equal V1; 1.55 fails. | analytical |
| 5. Prop. A.9 | At 3, proceeds rise by $113/1224$ and net surplus by $5/204$. | analytical |
| 6. Off-path beliefs | None; all five flows are interior, including both extremes. | analytical |
| 7. Ties and mixtures | Exact scalar correspondence for $r\le r_N$; coupled mixtures above $r_N$ remain unresolved. | open |
| 8. Knob and range | Symmetric: $0<\beta\le1/2$ and (19). Literal: $0<\beta<1/2$ and (19). | analytical |
| 9. Exact literature device | EGJ menus and GG's uninformed type are verified separately; their combination here has no verified exact precedent. | open |
| 10. Evidence | Proofs above; all stated benchmark inequalities use fractions. | computer-assisted |

### V3 buy: one opportunity, no separate noise

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique zero informed orders at $6/5$; entry $1/4$. | analytical |
| 2. Prop. 2(ii) | Unique full high-class purchase at 3; entry $37/68$; ownership $23/68$. | analytical |
| 3. Prop. 2(iii) | Full high-class purchase at $18/5$; entry $1/4$; same $r_C$. | analytical |
| 4. Prop. 3 | IM coexistence about $[1.3939579,1.7478775]$ contains 1.55–1.65. The requested upward triple fails. | analytical |
| 5. Prop. A.9 | At 3, proceeds rise by $113/408$ and net surplus by $5/68$. | analytical |
| 6. Off-path beliefs | None for $0<\beta<1$ and $0<\lambda<1$. | analytical |
| 7. Ties and mixtures | Equations (27)–(30) give every outcome; CM adds an interior threshold outcome. | analytical |
| 8. Knob and range | $0<\beta<1$ and (19); at $\beta=1/3$, $82/259<\lambda<2686/7363$. | analytical |
| 9. Exact literature device | BKT verifies alternative informed and noise identities without separate noise; the exact discrete menu remains unverified. | open |
| 10. Evidence | Analytical classification; exact examples and brackets below. | computer-assisted |

### V3 two: one opportunity, no separate noise

| Brief item | Result | Status |
|---|---|---|
| 1. Prop. 2(i) | Unique zero informed orders at $6/5$; entry $1/4$. | analytical |
| 2. Prop. 2(ii) | At the example, unique full informed purchases and sales at 3; entry $37/68$; ownership $23/68$. | analytical |
| 3. Prop. 2(iii) | At the example, full informed orders at $18/5$; entry $1/4$; same $r_C$. | analytical |
| 4. Prop. 3 | Low class abstains in coexistence; interval equals V3 buy and contains 1.55–1.65. Upward triple fails. | analytical |
| 5. Prop. A.9 | At 3, proceeds rise by $113/408$ and net surplus by $5/68$. | analytical |
| 6. Off-path beliefs | None for $0<\beta<1/2$, $0<\lambda<1$; exclude $\beta=1/2$ if every menu flow must remain on path. | analytical |
| 7. Ties and mixtures | Equations (27)–(31) give all rates; literal order also uses (45). I0 fails when literal low-class mixing is necessary. | analytical |
| 8. Knob and range | Symmetric: $0<\beta<1/2$ and (19). Literal full-order result also requires (46). | analytical |
| 9. Exact literature device | BKT verifies the alternative-identity architecture; GM and PIN source claims remain unverified here. | open |
| 10. Evidence | Complete finite-menu proof on the strip; exact arithmetic below. | computer-assisted |

## 5. Numerical example

### 5.1 A simple calibration and all three benchmark strengths — computer-assisted

Choose the illustrative inputs

$$
\beta=1/3,\qquad\lambda=6/17,\qquad b=11/51,
\qquad M=29/40,\qquad N=20/31.
$$

Their empirical calibration is **unverified**.
Equal probabilities apply to all three liquidity actions in the two-sided cases.
The admissible presence range at this $\beta$ is exactly

$$
\frac{82}{259}<\lambda<\frac{2686}{7363}.
$$

This is a nonzero interval near $0.32$–$0.36$, far from presence one.
The chosen informed-order fraction is $9/20$ in V3, not $6/17$.

| Variant | Informed orders at 1.2 | Entry at 1.2 | Informed orders at 3 | Entry at 3 | High-class ownership at 3 | Informed orders at 3.6 | Entry at 3.6 |
|---|---|---|---|---|---|---|---|
| V1 | $(0,0)$ | $1/4$ | $(1,0)$ | $71/204$ | $10/51$ | $(1,0)$ | $1/4$ |
| V2 | $(0,0)$ | $1/4$ | $(1,-1)$ | $71/204$ | $10/51$ | $(1,-1)$ | $1/4$ |
| V3 buy | $(0,0)$ | $1/4$ | $(1,0)$ | $37/68$ | $23/68$ | $(1,0)$ | $1/4$ |
| V3 two | $(0,0)$ | $1/4$ | $(1,-1)$ | $37/68$ | $23/68$ | $(1,-1)$ | $1/4$ |

At $r=3$, the top posterior $29/40$ exceeds $141/200$ strictly.
The extra entry at that posterior earns conditional gross profit $B_3(29/40)=37/6>6$.
The same posterior falls below $4245/5804$ at $r=3.6$.
No posterior is conclusive.

Conditional gross informed returns at $r=3$ are:

| Variant | High class, price access | Low class, price access | High class, hidden price | Low class, hidden price |
|---|---|---|---|---|
| V1 | $7/60$ | Does not buy | $17/240$ | Does not buy |
| V2 | $101/930$ | $467/7440$ | $467/7440$ | $467/7440$ |
| V3 buy | $11/60$ | Does not buy | $11/240$ | Does not buy |
| V3 two | $11/60$ | $11/240$ | $11/240$ | $11/240$ |

Each active return exceeds $k=1/50$.
These are conditional returns; multiplying by $\lambda$ before the trade comparison would be incorrect.

### 5.2 Rational brackets for the thresholds — computer-assisted

The script uses rational bisection and prints each exact endpoint value.
The following decimal strings represent rational endpoints, not floating-point certificates.

| Threshold | Exact definition | Rational decimal bracket |
|---|---|---|
| $r_N$ | $\mathfrak r(4/25)$ | $[1.747877538267,1.747877538269]$ |
| $r_C$ | $(50+\sqrt{2529})/29$ | $[3.458247029058,3.458247029060]$ |
| V1/V2 $r_A$ | Equation (32), $g=1/3,d=1/4$ | $[1.556594422881,1.556594422883]$ |
| V1/V2 $r_F$ | $\mathfrak r(4/35)$ | $[1.605847158116,1.605847158118]$ |
| V3 $r_A$ | Equation (32), $g=1,d=0$ | $[1.393957920278,1.393957920280]$ |
| V3 $r_F$ | $\mathfrak r(4/55)$ | $[1.460984663709,1.460984663711]$ |

The output records opposite rational endpoint signs for each bracket.
The derivative proof above supplies uniqueness for the $r_A$ brackets.

### 5.3 The requested intermediate strengths — computer-assisted

Under IM and C1, V1 and V2 have no informative outcome at $31/20$.
At $8/5$, their recruited investor mixture has

$$
s=286/867<\lambda,\qquad\mathsf E=399/1156.
$$

Its informed conditional purchase return equals $k$ exactly.
At $33/20$, the high-class purchase is full, with entry $71/204$.
Thus the local entry rise survives after the missing first point.

For both V3 menus, the full informative outcome has entry $37/68$ at every requested strength.
Under CM, the threshold outcomes have the exact order

$$
\frac{2442588329}{6961987560}
>
\frac{2186473}{6653340}
>
\frac{1793732190563}{5770000237560},
$$

at $31/20$, $8/5$, and $33/20$, respectively.
The decimal displays are about $0.3508464$, $0.3286279$, and $0.3108721$.
Each is strictly above $1/4$ and below $37/68$.
Neither informative branch supplies Proposition 3's upward triple.

### 5.4 A second probability example — computer-assisted

Set $\beta=12/25$ and $\lambda=216/491$.
Then $M=29/40$ still holds.
Under the symmetric convention, V2 has $N=359/502>141/200$.
Both positive flows recruit, so entry is $1/2$ and ownership is $599/1964$.

Under the literal convention, V2 instead has $N=20/31$.
Only its top flow recruits, so entry is $731/1964$ and ownership is $839/3928$.
Literal V3 requires low-class informed mixtures:

$$
t_3=209/1473,\qquad t_{18/5}=7711/35352.
$$

The low-class gross sale return equals $1/50$ at both rates.
The informed conditional sale probabilities are $t_r/\lambda$.
These literal outcomes require IM; they do not exist under I0.
This example shows why the probability order and the investor tie rule must be explicit.

### 5.5 Program use and saved evidence

The calculation program is `scripts/T2_liquidity_trader/exact_analysis.py` under the team folder.
Its output is `scripts/T2_liquidity_trader/exact_results.txt`.
Run it from the repository root:

```bash
bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh \
  .venv/bin/python \
  audit/microstructure_search_2026_10_22/scripts/T2_liquidity_trader/exact_analysis.py \
  --output audit/microstructure_search_2026_10_22/scripts/T2_liquidity_trader/exact_results.txt
```

The program directly forms class-conditional flow masses and Bayesian prices through the entry rule.
It prints informed payoffs, entry, ownership, target proceeds, and the allocation surplus increment.
It also prints exact signs at rational root endpoints.
Every equilibrium comparison uses `fractions.Fraction`.
Decimal conversion occurs only for display.

I used this interface and examined its printed results.
All listed active strong-economy orders earn strictly more than $1/50$, except the explicit literal mixtures.
Those mixtures earn exactly $1/50$.
The output labels threshold formulas even when their rates are infeasible; only the stated admissible rows are equilibrium claims.
One slot suffices; the calculation finishes well below one second.

## 6. Open issues

- **open.** The coupled V2 mixed correspondence above $r_N$ is not classified.
- **open.** No empirical record here calibrates $\lambda$, $\beta$, or a PIN estimator to this takeover interval.
- **open.** The exact finite device's published precedent remains unverified.
- **open.** Dispersion within quality classes, continuous order sizes, and richer liquidity preferences need separate analysis.
- **analytical.** Without a liquidity motive, the uninformed branch chooses zero at the constructed outcomes.
  A freely strategic uninformed speculator cannot replace the exogenous liquidity branch without a new mechanism.
- **analytical.** No candidate here reproduces every requested Proposition 3 feature at the benchmark.
  V1 and V2 lack the first requested informative outcome.
  V3 gives coexistence but fails the upward cross-strength order.

## 7. Plain summary

The liquidity slot removes the extreme-flow problem.
A liquidity purchase can occur in either class.
The top flow therefore has an interior posterior and pays the informed purchaser a positive residual.
Every feasible flow stays on path under every informed strategy in the stated parameter domains.

All variants recover the three benchmark outcomes of Proposition 2 on an open parameter strip.
At $\beta=1/3$, that strip is $82/259<\lambda<2686/7363$.
It does not require presence near one.
The example $\lambda=6/17$ gives the maximum equilibrium posterior $29/40$ and entry ceiling about $3.45825$.

The best case is V3 with the two-sided menu and no separate noise.
Its equal liquidity probabilities avoid any probability-order ambiguity.
At strength 3, entry is $37/68$ and high-class ownership is $23/68$.
Both exceed the weak-economy values, and price access raises proceeds and net surplus.
Its alternative informed and noise identities have a close verified precedent in BKT.
The exact discrete specification remains unverified as a published device.

The loss is clear.
V3 supports coexistence at 1.55, 1.60, and 1.65, but entry is flat on its full informative branch.
Its threshold mixture gives decreasing entry at those three points.
V1 and V2 preserve a short rising branch, but no informative equilibrium exists at 1.55.

The liquidity motive is essential.
An uninformed investor with only the paper's trading payoff prefers zero in these outcomes.
Also, equal posteriors do not imply equal informed returns across microstructures.
Conditional order flows must determine the payoff threshold.
