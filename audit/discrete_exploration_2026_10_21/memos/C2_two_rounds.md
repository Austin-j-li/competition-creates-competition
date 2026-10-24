# C2: two rounds before entry

## 1. Question

Can a second trade round restore graded beliefs, equilibrium coexistence, and the information ceiling?
Does a retained share change the second order and the price path?

Two discrete-Laplace rounds restore all three features, with qualifications about the horizon and the order menu.
At the original preparation cost, two rounds also restore the benchmark rise and fall in entry.
Coexistence holds at the original trade cost when $r=1.7$.
Equal three-point noise needs a different answer: repetition alone preserves its extreme information structure.

## 2. Setup

### 2.1 Designs and scope

The first base has independent noise $Z_t\in\{-1,0,1\}$, with equal probabilities.
The second base has independent discrete-Laplace noise, with parameter $a=e^{-1/b}$.
Each order satisfies $q_t\in\{0,1\}$, and each purchased unit costs $k>0$.
The investor presence probability is $\lambda=1$ throughout.
With $T$ rounds, total feasible purchases equal $T$ units.
Thus horizon comparisons also change total capacity.

Design S has one new investor per round.
Each investor knows the same class, has no initial position, and chooses only its own round's order.
It retains its purchased claim until the sale but cannot trade again.
This design isolates repeated information from the effect of a retained position on later choices.

Design R has one investor for both rounds.
Its final wealth from trade is

$$
(q_1+q_2)V_T-q_1P_1-q_2P_2-k(q_1+q_2).
\tag{1}
$$

Thus its first purchase creates a stake at the second decision.
The investor remembers its first order.
The market does not observe that order separately from noise.

The market and each active investor observe the public flow history.
The challenger observes the price history and its preparation cost.
All noise draws are independent of class, acquisition values, and preparation cost.
Preparation occurs only after the last price.

The analysis uses the point-mass special case of Reading N.
Nature selects $H$ or $L$; the corresponding acquisition values are $h$ and $\ell$.
The prior is $\pi=1/2$, except where a result states a general prior.
The low preparation cost is $c_L=0$.

### 2.2 Auction objects and source

The pinned source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` in the paper checkout.
Equation (4), Section 3.1, gives every auction object below.
Equations (9)–(11) give the static entry, price, and residual formulas.
Sections 4–6 and Propositions A.3–A.10 supply the comparisons in Section 4 of this memo.

For $0<p<\ell<r<h$, those objects are

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&g_H&=h-r/2-p^2/(2r),\\
g_L&=(\ell^2-p^2)/(2r),&\Delta_T&=t_H-t_L=(r-\ell)^2/(2r).
\end{aligned}
\tag{2}
$$

Define $w_j=t_j-t_0>0$, and write $\Delta=\Delta_T$ within derivations.
Then

$$
B_r(\mu)=g_L+\mu(g_H-g_L),\qquad
e(\mu)=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},
$$

$$
P(\mu)=t_0+e(\mu)(w_L+\Delta\mu).
\tag{3}
$$

The benchmark is $(h,\ell,p,\rho,c_H,k,b)=(10,1,1/2,1/4,6,1/50,2)$.
One coexistence example retains $k=1/50$ and uses $r=17/10$.
Other examples change $k$ to $9/100$ or $11/100$ at $r=3$.
They retain $c_H=6$; they do not use the brief's proposed change to $c_H=5$.

### 2.3 Equilibrium and tie rules

The solution concept is perfect Bayesian equilibrium with competitive prices and truthful auction bids.
Prices equal expected terminal target value, conditional on the full flow history.
Investors maximize expected profit against the fixed candidate prices and preparation rule.
In Design R, this comparison includes every first order and the best subsequent order after each possible flow.

An indifferent challenger prepares.
An indifferent investor may mix among optimal orders.
This investor rule permits the mixed example in Proposition C2.2.
The strict examples do not depend on an investor tie rule.

For three-point noise, Bayes' rule applies at every positive-probability history.
At an unused upper flow $2$, the completion assigns class $H$.
At any other unused next flow, the completion retains the preceding public posterior.
An unused first upper flow also receives posterior one.
The completion applies after a public posterior of zero as well.
It is a specified belief rule, not a claim that a refinement uniquely requires it.

Private histories outside the equilibrium path use the best continuation against these fixed public schedules.
Discrete-Laplace noise gives every finite integer flow history positive probability.
It therefore needs no public off-path completion.

## 3. Results

### 3.1 Prices must anticipate the last entry decision

**Lemma C2.0 — analytical.** The final price reveals the final flow posterior under either design.
An interim price generally differs from $P(\mu_t)$ in (3).

Let $H_t$ denote the public flow history and $\mu_t=\Pr(H\mid H_t)$.
Let $\mathcal P_T$ denote the price history.
Competitive final prices satisfy

$$
P_T=t_0+e(\mathcal P_T)(w_L+\Delta\mu_T),
\qquad
\mu_T=\frac{P_T-t_0-e(\mathcal P_T)w_L}{e(\mathcal P_T)\Delta}.
\tag{4}
$$

The denominator is positive because $e\ge\rho>0$.
Thus the price history reveals $\mu_T$.
The challenger's posterior equals $\mu_T$, so its entry rule is (3).
The function $P(\mu)$ is strictly increasing: its slope between jumps is positive, and every jump is upward.
Consequently, the final price alone also reveals $\mu_T$.

At an earlier date, the correct price is

$$
P_t=\mathbb E[t_0+e(\mu_T)w_j\mid H_t].
\tag{5}
$$

It includes the entry response to later information.
The challenger does not lose final information when it observes only prices.
The path still matters for the timing of orders and interim returns.

For Design S, define

$$
D(H_t)=w_H\mathbb E[e(\mu_T)\mid H,H_t]
       -w_L\mathbb E[e(\mu_T)\mid L,H_t].
\tag{6}
$$

Conditional on $H_t$, Bayes' rule gives

$$
\mathbb E[e\mid H,H_t]-\mathbb E[e\mid L,H_t]
=\frac{\operatorname{Cov}(e(\mu_T),\mu_T\mid H_t)}{\mu_t(1-\mu_t)}\ge0.
\tag{7}
$$

The covariance is nonnegative because $e$ is nondecreasing.
For independent copies $Y,Y'$ of $\mu_T$, twice that covariance equals

$$
\mathbb E[(e(Y)-e(Y'))(Y-Y')\mid H_t]\ge0.
$$

It follows that

$$
\rho\Delta\le D(H_t)\le W,
\qquad W=w_H-\rho w_L.
\tag{8}
$$

The upper bound uses $e_H\le1$ and $e_L\ge\rho$.
The lower bound follows from $D=\Delta e_H+w_L(e_H-e_L)$.
At posterior endpoints, the corresponding statements follow directly from the known class.

The current purchase residual is $(1-\mu_t)D(H_t)$ for $H$ and $-\mu_tD(H_t)$ for $L$.
Thus an $L$ investor never buys in Design S.
This conclusion concerns the permitted purchase menu; it does not establish an endogenous ban on sales.

### 3.2 Equal three-point noise: repetition alone does not give graded beliefs

**Proposition C2.1 — analytical.** Consider Design S with any finite horizon $T$ and prior $\pi\in(0,1)$.
Put

$$
s=\frac23,\qquad K(\pi)=s(1-\pi)e(\pi)\Delta.
\tag{9}
$$

If $k<K(\pi)$, every $H$ investor buys until the class becomes public.
If $k>K(\pi)$, there is no informed trade.
These are unique equilibrium outcomes under the stated completion.
The active outcome has only the posteriors $0,\pi,1$.
Conventional mixtures can add outcomes at $k=K(\pi)$; the uniqueness statement excludes that equality.

**Proof.** Suppose the current $H$ purchase probability is $\beta$, while $L$ chooses zero.
The next-flow probabilities are

$$
\begin{array}{c|cccc}
x&-1&0&1&2\\ \hline
\Pr(x\mid H)&(1-\beta)/3&1/3&1/3&\beta/3\\
\Pr(x\mid L)&1/3&1/3&1/3&0.
\end{array}
\tag{10}
$$

Both middle flows retain the current prior, for every $\beta$.
The upper flow reveals $H$, including under the completion when $\beta=0$.
In the last round, a purchase reaches the two middle flows and the upper flow with equal probabilities.
Its gross profit is therefore exactly $K(\pi)$.

Now use backward induction on the number of rounds.
If $k>K(\pi)$, the induction hypothesis gives no subsequent trade after either middle flow.
The current gross purchase profit remains $K(\pi)$, so zero is the unique current choice.
The lower-flow continuation cannot improve that purchase: a purchase cannot produce flow $-1$.

If $k<K(\pi)$, the induction hypothesis gives active trade after both middle flows.
With $n$ later rounds, define

$$
D_n=s^ne(\pi)\Delta+(1-s^n)\{e(1)w_H-e(0)w_L\}.
\tag{11}
$$

Each active round reveals the class with probability $1/3$, conditional on either class.
Equation (11) therefore follows from the probability $s^n$ of no revelation.
Also,

$$
D_n-e(\pi)\Delta
=(1-s^n)\{[e(1)-e(\pi)]w_H+[e(\pi)-e(0)]w_L\}\ge0.
$$

The current gross profit is $s(1-\pi)D_n\ge K(\pi)>k$.
Thus $H$ buys with probability one.
Lemma C2.0 excludes an $L$ purchase at every date.
After revelation, a new investor has no informational profit and stops.
These arguments also exclude a positive mixed purchase probability away from the threshold. $\square$

Suppose now that $B_r(\pi)<c_H\le g_H$, so $e(0)=e(\pi)=\rho$ and $e(1)=1$.
The active outcome gives

$$
\begin{aligned}
\mathsf E_T&=\rho+(1-\rho)\pi(1-s^T),\\
\mathsf O_{H,T}&=\pi\rho+(1-\rho)\pi(1-s^T),\\
\mathbb E[N_T\mid H]&=\sum_{t=1}^Ts^{t-1}=3(1-s^T).
\end{aligned}
\tag{12}
$$

Here $N_T$ counts purchases by all informed investors.
Conditional on $H$, their combined cost is $3k(1-s^T)$.
Their combined net profit is

$$
\Pi_{H,T}=\sum_{t=1}^Ts^{t-1}
\left[s(1-\pi)\{\rho\Delta+(1-\rho)w_H(1-s^{T-t})\}-k\right].
\tag{13}
$$

This is a sum across investors in Design S.
It is not a long-lived investor's deviation payoff.
As $T\to\infty$, the active posterior reveals the true class almost surely.
Indeed, the probability of no revelation after $T$ rounds is $s^T\to0$.

The limits of cost and net profit, conditional on $H$, are

$$
3k,\qquad 2(1-\pi)\{\rho\Delta+(1-\rho)w_H\}-3k.
\tag{14}
$$

If $k>K(\pi)$, the posterior instead remains at the prior for every horizon.

**A new price-path implication.** After $t$ rounds without revelation,

$$
P_t^U=t_0+\rho(w_L+\pi\Delta)
       +\pi(1-\rho)w_H(1-s^{T-t}).
\tag{15}
$$

This price falls as the deadline approaches without revelation.
The class posterior remains constant; the lost prospect of future entry causes the fall.
An $H$ revelation instead produces $P_t=t_H$ and ends informed trade.
The unconditional public price process remains a martingale, because upward revelations offset the conditional decline.

**Documented failure.** Repetition creates no graded on-path beliefs and no open interval of coexistence in Design S with equal noise.
Every active horizon still has posterior one with positive probability.
Thus expensive entry disappears only when $g_H(r)<c_H$.
At the benchmark, its boundary is

$$
r_C=4+\sqrt{16-1/4}=7.96862697\ldots.
\tag{16}
$$

Entry persists at equality because the challenger prepares at a tie.

### 3.3 A retained share creates a different three-point equilibrium

**Analytical characterization.** For Design R, the second-order increment at inventory $n$ is

$$
\Gamma_j(n,H_1)
=n\{\mathbb E_1V_j-\mathbb E_0V_j\}
  +\mathbb E_1[V_j-P_2]-k.
\tag{17}
$$

Each expectation fixes the candidate schedules and varies only the current order.
The first term is absent from Design S.
It measures the effect of the second order on the retained claim.

For a complete finite characterization, let $\sigma_j(n)$ denote the first-order probabilities.
The market retains the joint posterior over class and first order:

$$
\Pr(j,n\mid x_1)
=\frac{\pi_j\sigma_j(n)f(x_1-n)}
       {\sum_{i,m}\pi_i\sigma_i(m)f(x_1-m)}.
\tag{18}
$$

Combine (18) with the second-order policies to obtain $\mu_2$, $P_2$, and then $P_1$ from (5).
Define

$$
V_{2j}(n,x_1)=\max_{q\in\{0,1\}}
\mathbb E[(n+q)V_j-q(P_2+k)\mid j,n,x_1;q],
$$

$$
U_{1j}(n)=\mathbb E[V_{2j}(n,X_1)-n(P_1+k)\mid j;q_1=n].
\tag{19}
$$

Second-order policies must attain the maximum in (19).
First-order support must maximize $U_{1j}$.
Together with Bayes' rule, prices, and entry, these conditions are necessary and sufficient for this two-round game.
They include hidden inventory and every two-order deviation.

**Proposition C2.2 — analytical.** Use equal noise, $r=3$, and the benchmark except $k=3/20$.
Design R has an equilibrium with

$$
\Pr(q_1=1\mid H)=\beta=\frac{26}{81},\qquad q_1(L)=0.
\tag{20}
$$

After a middle first flow, $H$ buys again exactly when it already owns one unit.
After every other on-path first history, it stops.
The low class makes no purchase.
The on-path final posteriors are $55/136,1/2,1$.

**Proof.** The relevant exact values are

$$
\Delta=\frac23,\quad w_H=\frac98,\quad w_L=\frac{11}{24},\quad
D=\rho\Delta=\frac16,\quad K=\frac D3=\frac1{18},\quad
J=\frac{(1-\rho)w_H}{3}=\frac9{32}.
\tag{21}
$$

After either middle first flow, the posterior is $1/2$.
Within class $H$, the conditional probability of one retained unit remains $\beta$.
The aggregate second purchase probability in class $H$ is therefore also $\beta$.
The lower first flow, and the lower second flow after a middle first flow, give

$$
\mu_- =\frac{1-\beta}{2-\beta}=\frac{55}{136}.
\tag{22}
$$

Every posterior at or below $1/2$ induces only low-cost entry.
An upper flow induces full entry.
At a middle first history, (17) becomes

$$
\Gamma_H(n)=K+nJ-k.
\tag{23}
$$

For $n=1$, this equals $269/1440>0$.
For $n=0$, it equals $-17/180<0$.
After the lower first flow, an $H$ investor has inventory zero.
Its possible purchase earns gross profit

$$
\frac23D(1-\mu_-)=\frac9{136}<\frac3{20}=k.
$$

An $H$ investor also stops after its class becomes public.
Thus every proposed on-path second order is optimal.

The middle first price anticipates the hidden inventory distribution:

$$
P_1^U=t_0+\rho(w_L+\Delta/2)+\frac{\beta J}{2}.
\tag{24}
$$

A first purchase, followed by the best second order, earns

$$
U_{1H}(1)=\frac53(K-k)+\frac23(1-\beta/2)J.
\tag{25}
$$

The first term includes both purchase costs and the residual on a second purchase.
The second term includes the retained share's entry gain, less its anticipation in $P_1^U$.
Substitution gives $U_{1H}(1)=0$ exactly at $\beta=26/81$.
A zero first order also earns zero, because all its possible second purchases lose money.
Thus the proposed first mixture is optimal.

A low-class investor that deviates to a first purchase might also buy again.
At either middle history, its second increment is

$$
\Gamma_L(1)=\frac{(1-\rho)w_L}{3}-\frac{(1+\rho)\Delta}{3}-k
=\frac{11}{96}-\frac5{18}-\frac3{20}<0.
\tag{26}
$$

At the upper first history, a further purchase loses $\Delta+k$.
Thus its best continuation after a first purchase is zero.
Its complete first deviation payoff is

$$
U_{1L}(1)
=\frac23\left[-\frac D2-\frac{\beta J}{2}\right]-\frac\Delta3-k
=-\frac{989}{2160}<0.
\tag{27}
$$

Its zero first order earns zero.
Equations (22)–(27) verify all first actions and their best subsequent actions. $\square$

This equilibrium gives

$$
\mathsf E=\frac{77}{243},\qquad
\mathsf O_H=\frac{373}{1944},\qquad
\mathbb E[N_2\mid H]=\frac{130}{243},\qquad
\mathbb E[kN_2\mid H]=\frac{13}{162},\qquad
\Pi_H=0.
\tag{28}
$$

It creates graded bad news, but favorable entry still requires a revealing upper flow.
It does not establish coexistence with no trade.
At these same parameters, a two-order deviation from no trade earns $13/432>0$.
Thus no trade fails.
If an investor must choose zero at every tie, the mixed equilibrium in (20) is excluded.

**Computer-assisted result.** At $k=1/50$ or $1/10$, the full first purchase by $H$ also forms an equilibrium.
The second order is one after either middle flow and zero after revelation.
The calculation in Section 5 enumerates both first actions and all best second actions with exact rational values.
At $k=1/10$, the second purchase's standalone net profit is $K-k=-2/45$.
The retained share adds $J=9/32$, so the investor still purchases.

### 3.4 Discrete-Laplace noise: finite belief states and equilibrium equations

**Analytical derivation.** For $z\ge0$, the geometric-count construction gives

$$
\Pr(Z=z)=\sum_{n=0}^{\infty}(1-a)^2a^{n+z}a^n
=\frac{1-a}{1+a}a^z.
\tag{29}
$$

Symmetry gives the stated probability for negative $z$.
For an integer flow,

$$
\frac{f(x-1)}{f(x)}=
\begin{cases}a,&x\le0,\\a^{-1},&x\ge1.\end{cases}
\tag{30}
$$

Call these observations $-$ and $+$, respectively.
Under a purchase, the probability of $+$ is $u=1/(1+a)$.
Under zero, that probability is $v=a/(1+a)$.
Thus $u+v=1$ and $u>v$.

If every $H$ investor buys and every $L$ investor chooses zero, the posterior odds satisfy

$$
\frac{\mu_t}{1-\mu_t}
=\frac{\pi}{1-\pi}a^{,t-2N_+(t)}.
\tag{31}
$$

At $\pi=1/2$, two rounds produce

$$
\mu_2(--)=\frac{a^2}{1+a^2},\qquad
\mu_2(+-)=\mu_2(-+)=\frac12,\qquad
\mu_2(++)=\frac1{1+a^2}.
\tag{32}
$$

At $b=2$, these values are approximately $0.268941,0.5,0.731059$.
These are graded beliefs, with no finite-history revelation.

For completeness, the two-round Design S equilibrium reduces to three purchase probabilities when strategies use only sign histories.
Let $\beta_1$ be the first probability and $\beta_+,\beta_-$ the second probabilities.
For a current posterior $\nu$ and candidate purchase probability $\beta$, define

$$
L_+(\beta)=1-\beta+\beta/a,\qquad L_-(\beta)=1-\beta+\beta a,
$$

$$
\nu_\pm(\beta)=\frac{\nu L_\pm(\beta)}{1-\nu+\nu L_\pm(\beta)}.
\tag{33}
$$

The last investor's net purchase payoff is

$$
F(\nu,\beta)
=\Delta\{u e(\nu_+)(1-\nu_+)+v e(\nu_-)(1-\nu_-)\}-k.
\tag{34}
$$

The support conditions are $F\le0$ at $\beta=0$, $F=0$ for $0<\beta<1$, and $F\ge0$ at $\beta=1$.
At each first sign, compute

$$
\begin{aligned}
e_H&=[v+\beta(u-v)]e(\nu_+)+[u-\beta(u-v)]e(\nu_-),\\
e_L&=v e(\nu_+)+u e(\nu_-),\qquad D_s=w_He_H-w_Le_L.
\end{aligned}
\tag{35}
$$

Use $\nu=\nu_s(\beta_1)$ and $\beta=\beta_s$ in this expression.
The first net purchase payoff is

$$
F_1=u[1-\nu_+(\beta_1)]D_+
    +v[1-\nu_-(\beta_1)]D_--k.
\tag{36}
$$

Apply the same support conditions to $F_1$ and $\beta_1$.
Equations (33)–(36) are necessary and sufficient within this sign-history class.
Lemma C2.0 excludes purchases by $L$.
They retain all investor mixtures and the specified challenger tie rule.
They do not exclude equilibria that use otherwise irrelevant flow magnitudes to select different continuations.

### 3.5 Two rounds restore coexistence at the original preparation cost

**Proposition C2.3 — analytical.** Let $r=3$, $c_H=6$, $k=9/100$, and $a\in[3/5,61/100]$.
All other auction values equal the benchmark.
Both Design S and Design R admit these strict equilibria:

1. No informed trade, with entry $\rho$.
2. An $H$ purchase in both rounds, with extra entry exactly after $++$.

The interval for $a$ contains $e^{-1/2}$, so the result includes $b=2$.
The one-round model has unique no trade at these same primitives.

**Proof for no trade.** Every flow history then has posterior $1/2$.
All histories have positive probability, so a deviation does not alter those candidate beliefs.
Entry remains $\rho$ and each purchased unit earns gross profit

$$
\rho\Delta/2=1/12<9/100.
\tag{37}
$$

For Design R, a second purchase also cannot alter entry against this fixed schedule.
Thus every nonzero deviation loses money in both designs.

**Proof for informative trade.** Write $D=\rho\Delta=1/6$ and $M_2=1/(1+a^2)$.
The preparation inequalities are

$$
B_3(1/2)<B_3(u)<6<B_3(M_2).
\tag{38}
$$

Only $++$ recruits expensive entry.
Under full purchases, the second gross profits after bad and good first signs are

$$
C_-=D\left(\frac u2+vM_2\right),\qquad
C_+=\Delta\left[u(1-M_2)+\frac{v\rho}{2}\right].
\tag{39}
$$

After a bad first sign, terminal entry always equals $\rho$.
After a good first sign, the high and low classes generate a second positive sign with probabilities $u$ and $v$.
Their continuation value difference is therefore

$$
D_+=D+(1-\rho)(w_Hu-w_Lv),\qquad D_-=D.
\tag{40}
$$

Since the first posteriors are $u$ and $v$, the first gross profit is

$$
C_1=uv\{2D+(1-\rho)(w_Hu-w_Lv)\}.
\tag{41}
$$

At the exact rational value $a=3/5$,

$$
C_-=\frac5{51},\qquad C_+=\frac{77}{544},\qquad
C_1=\frac{1405}{8192}.
\tag{42}
$$

All three exceed $9/100$.
For the full interval, use

$$
u\ge\frac{100}{161},\quad v\ge\frac38,\quad v\le\frac{61}{161},\quad
M_2\ge\frac{10000}{13721},\quad 1-M_2\ge\frac9{34}.
$$

Substitution in (39)–(41) gives the exact positive margins

$$
\begin{aligned}
C_--\frac9{100}&\ge\frac{4844813}{662724300}>0,\\
C_+-\frac9{100}&\ge\frac{111361}{2189600}>0,\\
C_1-\frac9{100}&\ge\frac{3291751}{41473600}>0.
\end{aligned}
\tag{43}
$$

Also $6-B_3(u)\ge2/3$ and $B_3(M_2)-6\ge65339/329304>0$.
Thus Design S satisfies every purchase comparison.
Low-class purchases lose money by Lemma C2.0.

For Design R, a retained share adds

$$
w_H(u-v)(1-\rho)>0
\tag{44}
$$

to the second incentive after a good first sign.
It adds zero after a bad sign.
Thus its proposed second orders remain optimal.

If $H$ skips its first purchase, it still chooses a second purchase after either sign, by (43).
Its first purchase advantage, with both continuation plans optimized, is

$$
C_1-k+(u-v)(C_+-C_-)>0.
\tag{45}
$$

To verify the last inequality throughout the interval, (43) gives $C_+>0.1408$.
The bound $C_-\le\frac16\{5/16+(61/161)(25/34)\}<0.099$ gives $C_+>C_-$.

A low-class investor with one retained unit has this second increment after good news:

$$
w_L(u-v)(1-\rho)
-\Delta\left[uM_2+\frac{v\rho}{2}\right]-k.
\tag{46}
$$

An upper bound drops the last negative term inside the brackets and uses the interval endpoints.
It equals $-6486154159/21207177600<0$.
After bad news, entry is fixed, so a second purchase also loses money.
The best low-class continuation after a first purchase is therefore zero.
Its first residual is negative at both first signs, as in Lemma C2.0.
This excludes every low-class two-order deviation.

Finally, the alternating exponential series gives

$$
\frac{29}{48}<e^{-1/2}<\frac{233}{384},
\qquad
[29/48,233/384]\subset[3/5,61/100].
$$

Thus the entire proof includes $b=2$.
All displayed incentive and preparation margins are strict. $\square$

**Why one round fails.** With one round, the best posterior is at most $u$ after low-class purchase dominance.
Equation (38) therefore excludes every expensive entrant.
At an $H$ purchase probability $\beta$, the gross purchase return is

$$
\frac{2aD}{(2a+\beta(1-a))(2-\beta(1-a))}
=\frac{2aD}{4a+(1-a)^2\beta(2-\beta)}\le\frac D2<k.
\tag{47}
$$

Thus one-round no trade is unique, including against mixtures.
The second round creates the informative equilibrium; it does not merely repeat a pre-existing informative equilibrium.

**Benchmark-cost corollary — analytical.** Both equilibria also coexist at $r=17/10$, $k=1/50$, and every $a\in[3/5,61/100]$.
All other auction values remain at the benchmark, including $c_H=6$.
One round still has unique no trade.

Here

$$
\Delta=\frac{49}{340},\qquad D=\frac{49}{1360},\qquad
w_H=\frac{97}{170},\qquad w_L=\frac{29}{68}.
\tag{47a}
$$

Use these values in (39)–(46), with the same endpoint bounds that produce (43).
Every required inequality retains its strict sign:

$$
\begin{aligned}
k-D/2&=\frac{27}{13600}>0,\\
C_--k&\ge\frac{138982}{134122775}>0,\\
C_+-k&\ge\frac{444569}{42540800}>0,\\
C_1-k&\ge\frac{10740613}{352525600}>0,\\
C_+-C_-&\ge\frac{38941}{4254080}>0,\\
6-B_{1.7}(u)&\ge\frac{133}{544}>0,\\
B_{1.7}(M_2)-6&\ge\frac{629647}{933028}>0.
\end{aligned}
\tag{47b}
$$

The upper bound on the low-class retained-share deviation in (46) is $-45284127/8583857600<0$.
Thus the no-trade payoff formula, (45), and (47) give the same conclusions for both designs and the one-round comparison.
At $a=3/5$, the exact full-schedule gross profits are

$$
C_-=\frac{49}{2312},\qquad C_+=\frac{11319}{369920},\qquad
C_1=\frac{7167}{139264}.
\tag{47c}
$$

All inequalities are strict and continuous within this preparation region.
Coexistence therefore holds on an open neighborhood of these primitives.
This is a Proposition 3 analog at the original trade and preparation costs.

**Timing corollary — analytical.** Use $r=3$ and $k=11/100$.
Both designs admit an informative equilibrium with an initial $H$ purchase and a second purchase only after good first news.
No trade also remains an equilibrium.

After bad news, the zero-purchase continuation gives gross deviation profit $Du\le5/48<11/100$.
After good news, $C_+>0.1408>11/100$.
The first gross profit remains $C_1>0.1693>11/100$.
Its forecast of terminal entry is unchanged after either first sign.
For Design R, the first purchase advantage is now

$$
C_1-k+(u-v)(C_+-k)>0.
\tag{48}
$$

The low-class inequalities remain strict.
The final posterior after a bad first sign stays at $v$, rather than split between $a^2/(1+a^2)$ and $1/2$.
The two informative equilibria at the two costs have identical entry rates.
They differ in trade timing, cost, and information after bad news.

### 3.6 A Proposition 2 analog and a finite-horizon information ceiling

**Proposition C2.4 — analytical.** Under discrete-Laplace noise, any feasible strategy in either design satisfies

$$
m_T(\pi)\le\mu_T\le M_T(\pi),\qquad
M_T(\pi)=\frac{\pi a^{-T}}{1-\pi+\pi a^{-T}},\quad
m_T(\pi)=\frac{\pi a^T}{1-\pi+\pi a^T}.
\tag{49}
$$

Hence $B_r(M_T(\pi))<c_H$ forces entry to equal $\rho$ in every equilibrium.
For Design S with $\pi=1/2$, the following additional claims hold:

- If $\Delta(r_0)<k$, the unique outcome has no informed trade at any finite horizon.
- If $k<\rho m_T(1/2)\Delta(r_1)$, the unique outcome has an $H$ purchase at every date and history.
- If $r_2>r_1$ and $B_{r_2}(M_T(1/2))<c_H$, the same unique trade outcome has entry $\rho$ at $r_2$.

For an entry increase at $r_1$, also require $B_{r_0}(1/2)<c_H<B_{r_1}(M_T(1/2))$.
These strict conditions give a dynamic analog of Proposition 2.

**Proof.** At each history, a class-conditional flow distribution is a mixture of $f(x)$ and $f(x-1)$.
Equation (30) bounds the ratio between any two such mixtures by $a$ and $a^{-1}$.
Multiply these conditional likelihood bounds over the $T$ dates and apply Bayes' rule.
This gives (49), including hidden inventory in Design R.
Lemma C2.0 transfers the bound to the challenger's posterior.
The ceiling implication then follows from monotonicity of $B_r$ in its belief argument.

For Design S, a last-round purchase earns at most $\Delta$.
If $k>\Delta$, nobody purchases at the last date after any history.
Without future informative orders, the preceding purchase also earns at most $\Delta$.
Backward induction excludes all purchases and constructs the unique outcome.

For the full-purchase condition, Lemma C2.0 excludes every low-class purchase.
An $H$ purchase at any date has residual at least $\rho\Delta(1-M_T)=\rho\Delta m_T$.
The bound applies to every candidate strategy and every history.
Thus it strictly exceeds cost, and every $H$ investor purchases.
The implied posterior process, prices, and preparation rule construct that outcome.
This proves uniqueness without a restriction to sign-based equilibrium choices.

At $r_1$, the all-positive history has positive probability and posterior $M_T$.
It recruits expensive entry by the stated strict inequality.
High-class ownership rises because this history also has positive probability conditional on $H$.
The strong final price strictly Blackwell-dominates the constant weak price.
Its nonconstant posterior carries information, and a constant transformation reproduces the weak experiment.
At $r_2$, $\Delta$ is larger, so the full-purchase bound remains valid.
The ceiling excludes expensive entry there. $\square$

For full purchases at a general horizon, $N_+(T)$ is binomial with parameter $u$ in $H$ and $v$ in $L$.
Equation (31) converts the preparation threshold into a cutoff for that count.
If its tail probabilities are $A_H$ and $A_L$, then

$$
\mathsf E_T=\rho+(1-\rho)\{\pi A_H+(1-\pi)A_L\},\qquad
\mathsf O_{H,T}=\pi\{\rho+(1-\rho)A_H\}.
\tag{50}
$$

For $T=2$ and entry only after $++$,

$$
\mathsf E_2=\rho+\frac{1-\rho}{2}(u^2+v^2),\qquad
\mathsf O_{H,2}=\frac\rho2+\frac{1-\rho}{2}u^2.
\tag{51}
$$

**Computer-assisted benchmark corollary.** At $b=2$, $k=1/50$, and $c_H=6$, Design S satisfies Proposition C2.4 with

$$
(r_0,r_1,r_2)=(1.2,3,3.6).
\tag{52}
$$

The exact calculation encloses $e^{-1/2}$ between its degree-nine and degree-ten alternating series sums.
Those sums lie inside $[606530/10^6,606531/10^6]$.
Substitution gives positive rational margins for every inequality in Proposition C2.4.
In particular, the upper bound on $B_{3.6}(M_2)$ is strictly below $6$.
The output records those fractions; it does not infer the result from rounded decimal values.

The resulting entry path is approximately $0.25\to0.448747\to0.25$.
The ownership path is approximately $0.125\to0.270296\to0.125$.
This result uses the paper's original $c_H=6$ and all three original incumbent strengths.
It changes the low preparation cost to zero, as the team brief requires.
For two rounds, $M_2=1/(1+e^{-2/b})$ equals the paper's one-round bound under its two-sided order menu.
The two constructions share the same maximum cumulative log likelihood ratio.
This ceiling comparison does not identify a benefit unique to dynamics.

### 3.7 More rounds: distinguish repeated signals from equilibrium information

**Analytical experiment result.** Under forced full purchases, $M_T\to1$ as $T\to\infty$.
Conditional on $H$, the mean increment of log posterior odds is

$$
(u-v)(-\log a)>0.
\tag{53}
$$

Conditional on $L$, that mean has the opposite sign.
Independent noise and the law of large numbers therefore give posterior convergence to the true class.
Thus a fixed exogenous horizon ceiling does not remain bounded away from one as the horizon grows.

Forced full purchases are not generally equilibrium choices at positive cost.
The next result gives a separate bound for endogenous orders.

**Proposition C2.5 — analytical.** Consider Design S, discrete-Laplace noise, and fixed $r$ and $k>0$.
Let $W=w_H-\rho w_L$ as in (8).
If $W>k$, every finite-horizon equilibrium satisfies

$$
\mu_t\le\max\left\{\pi,\frac{W-k}{W-k+ka^2}\right\}<1.
\tag{54}
$$

If $W\le k$, no short-lived investor has a profitable purchase.
Thus positive trade cost gives a horizon-independent upper bound, although it can be close to one.

**Proof.** At current prior $\mu$, (30) implies that the next posterior is at least

$$
\frac{a\mu}{1-\mu+a\mu}.
$$

Equation (8) therefore bounds every current gross purchase payoff by

$$
W\frac{1-\mu}{1-\mu+a\mu}.
\tag{55}
$$

This bound is independent of all later equilibrium choices and the remaining horizon.
When $W>k$, a positive purchase probability requires

$$
\mu\le\bar\mu=\frac{W-k}{W-k+ka}.
\tag{56}
$$

The low class never purchases.
If the high class also stops, the next flow is independent of class and the posterior stays fixed.
Every posterior increase must therefore start at or below $\bar\mu$.
The largest possible one-step likelihood ratio is $a^{-1}$, so the next posterior is at most

$$
\frac{\bar\mu}{\bar\mu+a(1-\bar\mu)}
=\frac{W-k}{W-k+ka^2}.
$$

Induction, including the initial prior, gives (54).
For $W\le k$, (55) is strictly below $k$ at every interior prior, or the known class has zero residual.
Thus zero is optimal throughout. $\square$

At $r=3$, $b=2$, and $k=0.02$, the bound in (54) is approximately $0.992626$.
It is much weaker than the two-round bound $0.731059$.
It still excludes convergence to posterior one through equilibrium purchases by successive short-lived investors.
For entry, replace $M_T$ by the smaller of $M_T$ and the bound in (54).

A sequence of equilibria with different horizons need not define one common posterior process.
Coexistence makes its selection material.
If an infinite consistent process is specified, its bounded posterior martingale converges, but (54) prevents full high-class revelation.
The infinite game still needs a terminal entry rule and a well-defined payoff.
The result does not supply that missing game definition.

For Design R, the retained inventory grows with the number of purchases.
Equation (17) then adds an inventory term absent from (55).
The bound in (54) does not apply to that design.
Its endogenous infinite-horizon correspondence remains open.

## 4. What it recovers or loses relative to the Laplace paper

The comparisons below concern the pinned paper and the stated dynamic designs.
They do not establish a replacement for the paper's full correspondence.

| Paper object | Status | Dynamic finding and limit |
|---|---|---|
| Proposition 1 | analytical | The auction objects and their opposing derivatives remain unchanged. |
| Proposition 2(i)–(iii) | computer-assisted | Design S with two discrete-Laplace rounds satisfies the benchmark comparison in (52). Equal noise still has the late ceiling in (16). |
| Proposition 3 | analytical | Both designs have strict coexistence at $(r,k)=(1.7,0.02)$ and $(3,0.09)$. The one-round version has unique no trade there. The paper's partial-sale branch is not reproduced. |
| Endogenous directional asymmetry | open | Sales are excluded by the order menu. The timing corollary instead gives an endogenous difference across first histories. |
| Proposition A.3 | analytical | Fixed-experiment deterrence survives. Hold the terminal posterior law fixed; both $g_H$ and $g_L$ fall with $r$, so entry cannot rise. |
| Proposition A.4 | analytical | The static thresholds change. Equations (9), (34)–(36), (49), and (54) give dynamic counterparts with explicit scopes. |
| Proposition A.5 | open | The logistic extension is not evaluated here. The posterior argument uses bounded adjacent likelihood ratios. |
| Proposition A.6 | analytical | The price and covariance arguments extend to nondecreasing entry with a positive floor. Specific cost distributions and equilibrium numbers need a new calculation. |
| Proposition A.7 | open | Separate private signals are not studied. Every informed investor here knows the same class, and the challenger has no extra quality signal. |
| Proposition A.8 | open | The auction stage is unchanged. No alternative negotiation rule is solved. |
| Proposition A.9 | analytical | The entry channel raises target proceeds at the informative equilibria relative to hidden prices. The acquisition-surplus comparison below excludes trade costs. |
| Proposition A.10 | analytical | Its zero-entry price pool cannot occur under $c_L=0$ and $\rho>0$. Interim anticipation in (5) is a separate issue. |
| Section 5 | analytical | Noise support and repeated observation matter. The binary order menu does not reproduce the paper's continuous order magnitudes. |
| Section 6 | open | The reserve stays fixed. Retained shares matter through (17). Seller choice and a full welfare comparison with trade costs remain separate tasks. |

The acquisition-surplus statement uses the benchmark auction directly.
With $R\ge p$, entry raises realized acquisition value by $(\theta-R)_+$, equal to the challenger's auction profit.
With $R<p$, entry creates value $\theta$, while that profit is $\theta-p$.
Since both classes exceed $p$, the conditional social increment before preparation cost is

$$
B_r(\mu)+p\Pr(R<p)=B_r(\mu)+\frac{p^2}{r}.
\tag{57}
$$

Every additional costly entrant satisfies $B_r(\mu)\ge c_H$.
Its expected acquisition-surplus increment net of preparation cost is therefore positive.
Target proceeds also rise because $w_H,w_L>0$.
Extra trade costs are separate resource costs if the model treats $k$ as a real expense.

## 5. Numerical example

### 5.1 Outcomes and costs

**Status: numerical diagnostic**, except for the rational rows and the benchmark certificate stated above.
Costs and profits below are conditional on class $H$.
For Design S, profit is the sum across its two investors.
Every other primitive follows Section 2.

| Noise and design | $r$ | $k$ | Entry | High-class ownership | Total cost in $H$ | Net profit in $H$ |
|---|---:|---:|---:|---:|---:|---:|
| Equal noise, either design, active | 3 | 0.02 | $11/24$ | $1/3$ | $1/30$ | $661/4320$ |
| Equal noise, retained share, active | 3 | 0.10 | $11/24$ | $1/3$ | $1/6$ | $17/864$ |
| Equal noise, retained share, mixed | 3 | 0.15 | $77/243$ | $373/1944$ | $13/162$ | $0$ |
| Discrete Laplace, Design S, no trade | 1.2 | 0.02 | 0.250000 | 0.125000 | 0 | 0 |
| Discrete Laplace, either design, full | 1.7 | 0.02 | 0.448747 | 0.270296 | 0.040000 | 0.038394 |
| Discrete Laplace, Design S, full | 3 | 0.02 | 0.448747 | 0.270296 | 0.040000 | 0.257263 |
| Discrete Laplace, Design S, full | 3.6 | 0.02 | 0.250000 | 0.125000 | 0.040000 | 0.174399 |
| Discrete Laplace, either design, full | 3 | 0.09 | 0.448747 | 0.270296 | 0.180000 | 0.117263 |
| Discrete Laplace, either design, good-news continuation | 3 | 0.11 | 0.448747 | 0.270296 | 0.178471 | 0.081842 |

At $(r,k)=(1.7,0.02),(3,0.09),(3,0.11)$, a separate no-trade equilibrium gives entry $0.25$ and ownership $0.125$.
Its trade costs and profits are zero.
At $k=0.09$, the full equilibrium has

$$
C_1-k=0.08125985,\quad C_+-k=0.05306512,\quad C_--k=0.00787234.
$$

For full trade in both rounds, total net profit in class $H$ is

$$
\Pi_H=C_1+uC_++vC_--2k.
\tag{58}
$$

For continuation only after good first news, total cost and profit are

$$
k(1+u),\qquad \Pi_H=C_1-k+u(C_+-k).
\tag{59}
$$

These formulas apply to either design when their equilibrium orders coincide.
Their deviation incentives still differ.

### 5.2 The price path before entry

At $r=3$ and $b=2$, the informative discrete-Laplace equilibria have

$$
P_1(-)=0.59417344,\qquad P_1(+)=1.01090598.
$$

With full second purchases, the terminal prices are

$$
P_2(--)=0.57607357,\quad
P_2(+-)=P_2(-+)=0.61458333,\quad
P_2(++)=1.36237239.
\tag{60}
$$

A favorable first price can precede a sharp fall if the second signal is unfavorable.
An expensive challenger prepares only after the two favorable observations.
At $k=0.11$, a negative first observation ends informed trade and the price stays at $P_1(-)$.

For equal noise, the unresolved first price at the active two-round equilibrium is $145/192$.
If the second flow is also unresolved, the final price is $59/96$.
This fall occurs without a change in the class posterior, as (15) predicts.

### 5.3 Reproducible calculations

The calculation entry point is [calculate.py](../scripts/C2_two_rounds/calculate.py).
Its options select the equal-noise cases, the discrete-Laplace cases, or all cases.
The saved output is [results.jsonl](../scripts/C2_two_rounds/results.jsonl).
The receipt records inputs, scope, and file hashes.

The calculation uses exact rational arithmetic for all rational inputs.
It collapses the discrete-Laplace tails exactly through (30), so there is no tail truncation.
The $b=2$ decimal rows use the exponential value directly.
Separate rational bounds certify the benchmark inequalities and the coexistence interval.

For each finite candidate, it constructs prices from all terminal histories.
It then prints both first-action values and the best second action at every private history.
It also prints on-path second-choice margins, entry, ownership, total cost, and net profit.
The actual calculation ran through the shared slot wrapper and completed in less than one second.
The retained-share mixture returned an exact zero first-action difference and strictly positive on-path second-choice margins.
The no-trade candidate at equal-noise cost $0.15$ returned a profitable first deviation, as reported above.

## 6. Open issues

- The complete Design R correspondence over all parameters is open. Equations (18)–(19) give the required conditions, not a global solution.
- The discrete-Laplace mixed correspondence can have additional equilibria. Equations (33)–(36) characterize the sign-history restriction.
- Uncertain presence, $\lambda<1$, is not included. Persistent absence also creates a hidden state across dates.
- The infinite Design R game needs an entry date, a total-position rule, and a payoff definition.
- The infinite Design S limit needs an equilibrium selection and a common probability space across horizons.
- The order menu does not establish endogenous asymmetry between purchases and sales.
- A fixed cumulative purchase limit could change the horizon results. That alternative is not solved here.
- A rule that forbids every indifferent investor mixture removes Proposition C2.2. The strict coexistence result remains.
- The equal-noise results depend on the stated off-path completion. The discrete-Laplace results do not need that completion.
- The benchmark return at $r=3.6$ is close to its ceiling. The exact rational enclosure matters; coarse changes in $a$ can reverse that inequality.
- The calculations do not prove uniqueness of the retained-share benchmark outcomes or exhaust every two-round equilibrium.

No baseline claim in the brief is refuted.
The statement that equal noise loses coexistence remains correct for the one-round base and for Design S away from its tie boundary.
The new counterexample concerns an extrapolation: repetition alone does not guarantee graded beliefs or recover the early ceiling.

## 7. Plain summary

Two rounds help, but the noise law and the investor's position matter.

With equal three-point noise and separate investors, each active round either reveals the class or leaves the prior unchanged.
More rounds raise the chance of revelation.
They do not create graded beliefs or an open interval of coexistence.
The expensive challenger still enters after perfect good news until incumbent strength exceeds about 7.97.

A retained share changes the second decision.
The investor can buy again to raise entry and the value of its first share.
An exact mixed equilibrium creates graded bad news.
That example does not coexist with no trade.

Discrete-Laplace noise gives a stronger result.
Two rounds create three terminal beliefs.
With separate investors and the original benchmark strengths and preparation cost, entry becomes 0.25, then 0.448747, then 0.25.
At incumbent strength 1.7, no trade and informative trade coexist at the original trade cost under either design.
One round has unique no trade at those same primitives.

Trade timing also responds to the first price.
At another cost, the investor makes its second purchase only after favorable first news.
Entry stays the same, but fewer trades occur.

More forced signals eventually reveal the class under discrete-Laplace noise.
Positive costs change the equilibrium conclusion: sufficiently optimistic beliefs stop new investors from buying.
A separate bound limits beliefs at every finite horizon.
The corresponding limit with one investor and a growing retained position remains open.
