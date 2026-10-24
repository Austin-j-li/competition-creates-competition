# C4. Several potential challengers in sequence

Workstream C4, 21 October 2026. Status: complete for phase 1; awaiting the phase-2 check.

## 1. Question

Does entry cascade? Does one entrant's decision inform the next through the price?
The test: apply the paper's title mechanism recursively. Challenger 1's entry makes the field stronger
for challenger 2. Does that widen the target's payoff spread across challenger 2's class, recruit
informed trading, and recruit challenger 2? Or does the first entrant deter the second?

## 2. Setup

### 2.1 Base model and the reason for it

The base is the discrete-Laplace model with buy-only orders (TEAM_RULES §4, model 2). The reasons:

1. Every integer flow is on path under every investor strategy. Two rounds with four investor types would
   need off-path beliefs at several histories in the three-point model.
2. Posteriors stay interior. In each round, the likelihood ratio between any two states lies in $[a,1/a]$.
   The three-point model can reveal the state at its top flow. Then no two-round posterior bound exists.
3. A buy-only flow carries information only through one binary event, $X\ge1$ against $X\le0$
   (Lemma 1 below). Each round is then a binary experiment, so the game stays finite.

I re-derive the three discrete-Laplace facts that I use (Lemma 1). B1 (§3.1) reports the same reduction.
I use no other candidate result from the brief.

### 2.2 Primitives

- Target: standalone value $0$. Second-price auction with reserve $p$. Truthful bids.
- Incumbent: prepared, value $R\sim U[0,r]$.
- Challengers $i=1,2$: class $j_i\in\{H,L\}$, value $v_i=h$ for $H$ and $v_i=\ell$ for $L$
  (the benchmark point masses). Cost $C_i=c_L=0$ with probability $\rho$, else $c_H$.
  The costs are independent of each other and of everything else.
- State $s=(j_1,j_2)\in\{HH,HL,LH,LL\}$ with prior
  $\pi_{HH}=\pi_{LL}=(1+\kappa)/4$ and $\pi_{HL}=\pi_{LH}=(1-\kappa)/4$, $\kappa\in(-1,1)$.
  Each class has marginal prior $1/2$.
  - $\kappa=0$: independent classes.
  - $\kappa>0$: a common target-specific component. With probability $\kappa$ both classes equal one
    common draw; otherwise they are independent.
  - $\kappa<0$: negative correlation (a contrast case: the target fits one buyer or the other).
- Noise: $Z_t=G_{t1}-G_{t2}$ in round $t$, independent across rounds, with
  $\Pr(Z=z)=n(z)=\frac{1-a}{1+a}a^{|z|}$ and $a=e^{-1/b}$.
- Investors: one short-lived informed investor in each round. Investor $t$ sees $s$, chooses
  $q_t\in\{0,1\}$, pays $kq_t$, buys at $P_t$ and holds the share to the end.
  Its payoff is $q_t(V_T-P_t-k)$. A single investor active in both rounds would add manipulation through
  challenger 1's entry; Section 6 lists that case as open.

Benchmark values: $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$, $c_L=0$, $b=2$, $k=0.02$,
$r_0=1.2$, $r_1=3$, $r_2=3.6$. The cost $c_H$ is scanned, because the lone-challenger window
$(4.80,5.31]$ of the brief does not carry over (Result 8). The two marked costs are $c_H=5$ and $c_H=5.8$.

### 2.3 Timing

1. Nature draws $s$, $R$, $C_1$, $C_2$, $Z_1$, $Z_2$. The seller has committed to the auction.
2. Round 1. Investor 1 trades. Flow $X_1=q_1+Z_1$. Market makers set $P_1=\mathbb E[V_T\mid X_1]$.
   Challenger 1 sees $P_1$ and $C_1$ and chooses $d_1\in\{0,1\}$. The decision $d_1$ is public.
   A prepared challenger's value stays private until the auction.
3. Round 2. Investor 2 trades. Flow $X_2=q_2+Z_2$. Market makers set
   $P_2=\mathbb E[V_T\mid X_1,d_1,X_2]$. Challenger 2 sees $P_1$, $d_1$, $P_2$ and $C_2$, and chooses $d_2$.
4. The incumbent and every prepared challenger bid. $V_T$ is the auction payment to the target.

### 2.4 Equilibrium concept, beliefs and tie rules

- **Concept.** Perfect Bayesian equilibrium with competitive prices. Each price equals the expected
  terminal payoff given public information, and it anticipates all later play. An investor deviation
  holds the candidate price and entry schedules fixed. A challenger prepares when its expected gross
  gain is at least its cost.
- **Beliefs.** Bayes' rule applies at every flow, because noise has full support.
  Challenger 1's decision does not change beliefs about $s$. Challenger 1 knows only $(P_1,C_1)$, and
  $C_1$ is independent of $s$. The same rule fixes beliefs after an off-path decision, for example
  $d_1=0$ at a price where both cost types prepare.
- **Challenger tie rule.** An indifferent challenger prepares (the paper's rule).
- **Investor tie rule.** The main correspondence allows any mixture at investor indifference.
  The selected rule for the reported pure equilibria is no trade at indifference.
- **Auction tie rule.** Equal highest bids: the winner is drawn at random. The paper excludes this case
  ("acquisition-value ties have probability zero"), but here two same-class challengers tie.
  The payment equals the tied value, and the winner's surplus is zero. Proceeds, surpluses and allocation
  value therefore do not depend on this rule. Only the identity of the winner does.
- **Selection inside a class.** Two investor types with identical continuation payoffs use the same
  mixture. This matters only at indifference.

### 2.5 Notation

- Shared objects $t_0,t_H,t_L,g_H,g_L,\Delta_T,B_r$ as in TEAM_RULES §3. I checked each against
  equation (4) of the pinned paper.
- $D_r=g_H-g_L=h-\ell-\Delta_T(r)$: the rent of a high-class challenger against a low-class rival
  (Result 1). The second equality is the split identity $\Delta_T+(g_H-g_L)=h-\ell$.
- $\mathsf E_i$: preparation probability of challenger $i$. $\mathsf E_{12}$: both prepare.
- An **entry cascade** means $\Pr(d_2=1\mid d_1=1)>\Pr(d_2=1\mid d_1=0)$. The history-by-history version
  compares the two decisions at the same round-1 signal $S_1$; it removes the selection of $d_1$ on $S_1$ and
  stays defined when $d_1=0$ is off path. This is not an informational cascade in the sense of Bikhchandani, Hirshleifer and Welch (1992;
  verified abstract only, D1 §3.14). There, a decision ignores private information. Here, no challenger
  has private information about values when it decides.


## 3. Results

Scripts are in `scripts/C4_sequential/` (Section 5 lists them). Every number below comes from one of them.

### Result 1 (analytical, with a numerical check): auction objects with three bidders

When both challengers prepare, every bidder value is at least $\ell>p$, so the reserve never binds.
The payment is the second-highest of $\{R,v_1,v_2\}$:

| State $s$ | Bidder values | Payment $T_s$ | Surplus: ch. 1, ch. 2, incumbent |
|---|---|---|---|
| $HH$ | $h,h,R$ | $h$ (tie at $h$) | $0,\ 0,\ 0$ |
| $HL$ | $h,\ell,R$ | $\mathbb E\max\{\ell,R\}=\ell+\Delta_T$ | $D_r,\ 0,\ 0$ |
| $LH$ | $\ell,h,R$ | $\ell+\Delta_T$ | $0,\ D_r,\ 0$ |
| $LL$ | $\ell,\ell,R$ | $\ell$ | $0,\ 0,\ \Delta_T$ |

Derivations:

- $\mathbb E\max\{\ell,R\}=\ell+\mathbb E(R-\ell)_+=\ell+\int_\ell^r(u-\ell)\,du/r=\ell+(r-\ell)^2/(2r)$.
- In state $HL$ the high-class challenger pays $\max\{\ell,R\}$, so its surplus is
  $h-\ell-\Delta_T=D_r$. Also $g_H-g_L=h-r/2-\ell^2/(2r)=h-\ell-\Delta_T$.
- In state $LL$: if $R<\ell$, the two challengers tie at $\ell$ and pay $\ell$; if $R>\ell$, the
  incumbent wins and pays $\ell$. The incumbent's expected surplus is $\mathbb E(R-\ell)_+=\Delta_T$.
- Each row satisfies payment plus surpluses equal to the expected highest value ($h$, $h$, $h$,
  $\ell+\Delta_T$).

With one prepared challenger of class $j$, the payment is $t_j$ and its gain is $g_j$ (paper, eq. (4)).
With none, the payment is $t_0$. The allocation value is $(r^2-p^2)/(2r)$ with no challenger,
$\ell+\Delta_T$ when the best prepared challenger is low-class, and $h$ when it is high-class.
Note $D_r'(r)=-\Delta_T'(r)<0$.

**Check.** `c4_auction.py` integrates the auction outcome over $R$ with `quad` at
$r\in\{1.2,2,3,3.6,4.2,6\}$. The largest difference from the closed forms is $1.8\times10^{-15}$.

### Result 2 (analytical): the spread–rent table

The table gives the payment spread across challenger 2's class and challenger 2's gross gain by class.

| Field when challenger 2 decides | Spread across challenger 2's class | Gain if $j_2=H$ | Gain if $j_2=L$ |
|---|---|---|---|
| Incumbent only | $t_H-t_L=\Delta_T$ | $g_H$ | $g_L$ |
| Incumbent and a low-class challenger 1 | $T_{LH}-T_{LL}=\Delta_T$ | $D_r=g_H-g_L$ | $0$ |
| Incumbent and a high-class challenger 1 | $T_{HH}-T_{HL}=D_r$ | $0$ | $0$ |

At $r=3$: $\Delta_T=0.666667$ and $D_r=8.333333$. So a high-class first entrant multiplies the spread by
12.5, and it removes all of challenger 2's gain.

Consequences:

1. Challenger 1's entry raises the spread across challenger 2's class only in the state $j_1=H$.
   In that state challenger 2 gains nothing, whatever its class.
2. In the state $j_1=L$ the spread does not change, and both of challenger 2's gains fall by $g_L$.
3. The reason is the split identity. A high-class rival in the field takes the payment to $h$ when
   challenger 2 is also high-class. The extra payment comes from challenger 1's rent, not from
   challenger 2's. Challenger 2 can only compete that rent away; it cannot keep any of it.

### Result 3 (analytical): deterrence at a fixed information experiment

Fix any information $I$ about $s$ (any signal with a fixed joint law). Challenger 2's expected gross gain is

$$
\text{without challenger 1: } g_L+D_r\Pr(j_2=H\mid I)=B_r(\Pr(j_2=H\mid I)),\qquad
\text{with challenger 1: } D_r\Pr(s=LH\mid I).
$$

The difference is $g_L+D_r\Pr(s=HH\mid I)>0$ at every realization of $I$.
The cost is independent of $I$. So at a fixed experiment, entry by challenger 1 weakly lowers
challenger 2's preparation probability, at every realization. This is the analog of Proposition A.3,
with the first entrant in the role of the stronger incumbent. Any cascade must therefore come from a
change in information.

### Lemma 1 (analytical): one binary event per round, and two-round posterior bounds

I re-derive the discrete-Laplace facts that I use.

(a) *Noise law.* For $z\ge0$,
$\Pr(G_1-G_2=z)=\sum_{j\ge0}(1-a)a^{z+j}(1-a)a^j=(1-a)^2a^z/(1-a^2)=\frac{1-a}{1+a}a^z$.
The case $z<0$ is symmetric. So $n(z)=\frac{1-a}{1+a}a^{|z|}$.

(b) *Binary reduction.* A type that buys with probability $\beta$ produces flow $x$ with probability
$\beta n(x-1)+(1-\beta)n(x)$. For $x\ge1$, $n(x-1)=n(x)/a$; for $x\le0$, $n(x-1)=a\,n(x)$. Hence

$$
\Pr(X=x\mid\beta)=\begin{cases}n(x)\,[1+\beta(1/a-1)],&x\ge1,\\ n(x)\,[1-\beta(1-a)],&x\le0.\end{cases}
$$

The factor $n(x)$ is the same in every state. So every posterior depends on $x$ only through
$S=\mathbf 1\{x\ge1\}$ ("good news" $g$ or "bad news" $b$). Summing,
$\Pr(S=g\mid\beta)=\frac{a+\beta(1-a)}{1+a}$, and a purchase reaches $g$ with probability $1/(1+a)$.
This holds for arbitrary mixtures, separately for each state.

(c) *One-round bound.* $\Pr(S\mid\beta)\in[\frac{a}{1+a},\frac1{1+a}]$ for both signals and every
$\beta\in[0,1]$. So the likelihood ratio of a signal between any two states lies in $[a,1/a]$.

(d) *Two-round bound.* Round-2 strategies may depend on the public history. Given the history, the
round-2 factor still lies in $[a,1/a]$. Challenger 1's decision is independent of $s$ given $P_1$, so it
adds a common factor. Hence the likelihood of the public record lies in $[a^2,a^{-2}]$ across states.
For any event $E$ with prior $\pi_E$,

$$
\Pr(E\mid\text{public record})\le\psi_2(\pi_E):=\frac{\pi_E}{\pi_E+a^2(1-\pi_E)},\qquad
\text{after one round: }\psi_1(\pi_E):=\frac{\pi_E}{\pi_E+a(1-\pi_E)}.
$$

Proof: $\Pr(E\mid\cdot)=\sum_{s\in E}\pi_sL_s/\sum_s\pi_sL_s\le\pi_EL_{\max}/(\pi_EL_{\max}+(1-\pi_E)L_{\min})$
and $L_{\max}/L_{\min}\le a^{-2}$.

(e) *Prices.* A challenger sees prices, not flows. Its posterior is a conditional expectation of the
flow posterior (tower property), so the same bounds hold.

**Check.** `c4_flowcheck.py` recomputes seven solved equilibria by summing over integer flows
$x\in[-80,81]$, with entry decided from flow posteriors. Posteriors, gains, margins and outcomes agree with the
reduced solver to $3\times10^{-15}$, with no entry mismatch.

### Result 4 (analytical): no entry cascade

**Proposition C4.1 (no entry cascade; analytical).** Take any $b>1$, $\kappa\in(-1,1)$ and $r\in(\ell,h)$,
with $c_L=0$ and point-mass classes. Suppose

$$
c_H>\psi_2(\pi_{LH})\,D_r .\tag{NC}
$$

Then challenger 2's high-cost type never prepares after challenger 1 prepares, at every history, in every
equilibrium. This allows arbitrary mixed orders in both rounds, either investor tie rule, and challenger
mixing at indifference. Hence

$$
\Pr(d_2=1\mid S_1,d_1=1)=\rho\le\Pr(d_2=1\mid S_1,d_1=0)\ \text{ at each }S_1,\qquad
\Pr(d_2=1\mid d_1=1)=\rho\le\Pr(d_2=1\mid d_1=0),\qquad \mathsf E_{12}=\rho\,\mathsf E_1 .
$$

There is no entry cascade, in either version. The gap $\Pr(d_2=1\mid d_1=0)-\rho$ equals $(1-\rho)$ times the probability that
challenger 2's high-cost type prepares after $d_1=0$.

*Proof.* After $d_1=1$, challenger 2's gain is $D_r\Pr(LH\mid P_1,d_1,P_2)$ (Result 3). By Lemma 1(d,e)
it is at most $D_r\psi_2(\pi_{LH})<c_H$. The low-cost type has gain $\ge0=c_L$ and prepares (tie rule; in
fact the gain is positive because posteriors are interior). After $d_1=0$ the gain is $B_r(\cdot)\ge g_L>0$,
so the low-cost type prepares there too. $\square$

**Corollary.** If $\kappa\ge0$ and $b\ge2/\ln3\approx1.820$, then $\psi_2(\pi_{LH})\le\psi_2(1/4)=1/(1+3a^2)\le1/2$.
Then $c_H>B_r(1/2)=g_L+D_r/2$ implies (NC). In words: if challenger 2's high-cost type does not prepare
alone at the prior (the lower half of the paper's (A2)), it never prepares after a first entry.

At the benchmark $b=2$, $\kappa=0$, the threshold $\psi_2(1/4)D_r$ is 4.270 at $r=1.2$, 3.961 at $r=3$ and
3.832 at $r=3.6$ (`c4_bounds.py`). For $\kappa=0.5$ it is 2.513, 2.331 and 2.255. For $\kappa=-0.5$ it is 5.569, 5.166 and
4.997, above $B_r(1/2)$: (NC) can fail with negative correlation.

### Result 5 (analytical): information after entry, and its sign

Assume (NC), so challenger 2's entry after $d_1=1$ is $\rho$ at both signals. The terminal values are then
$V_s=t_{j_1}+\rho(T_s-t_{j_1})$:

$$
V_{HH}=t_H+\rho g_H,\quad V_{HL}=t_H+\rho g_L,\quad V_{LH}=t_L+\rho(\Delta_T+g_L),\quad V_{LL}=t_L+\rho g_L .
$$

**Proposition C4.2 (information after entry; analytical).** Assume (NC). After $d_1=1$, at every history,
in every round-2 equilibrium:

1. Type $LL$ never buys.
2. Type $HH$ buys with probability one if $(1-\psi_2(\pi_{HH}))\rho D_r>k$.
3. Type $LH$ never buys if $a^2(\pi_{HH}/\pi_{LL})[(1-\rho)\Delta_T+\rho D_r]>\rho\Delta_T$.

Under 1–3 the round-2 price after entry is informative about $s$, and a higher price lowers challenger 2's
posterior on $LH$, the only state in which it profits. After $d_1=0$, if $\Delta_T(r)<k$, no type buys and the
round-2 price carries no information. So at a weak incumbent, challenger 1's entry turns an uninformative
round-2 price into an informative one.

*Proof.*

1. $V_{HL}-V_{LL}=\Delta_T$, $V_{LH}-V_{LL}=\rho\Delta_T$, $V_{HH}-V_{LL}=\Delta_T+\rho D_r$. So $V_{LL}$ is the
   smallest value. The price is an average of the $V_s$, so a purchase by $LL$ earns at most $-k$.
2. $V_{HH}-V_{HL}=\rho D_r$, $V_{HH}-V_{LH}=(1-\rho)\Delta_T+\rho D_r$, $V_{HH}-V_{LL}=\Delta_T+\rho D_r$.
   So $V_{HH}-P_2\ge(1-\nu'(HH))\rho D_r\ge(1-\psi_2(\pi_{HH}))\rho D_r$ at each signal, where $\nu'$ is the
   market posterior.
3. $V_{LH}-P_2=-\nu'(HH)[(1-\rho)\Delta_T+\rho D_r]-\nu'(HL)(1-\rho)\Delta_T+\nu'(LL)\rho\Delta_T$.
   Lemma 1(d) gives $\nu'(HH)/\nu'(LL)\ge a^2\pi_{HH}/\pi_{LL}$. Under the condition, $V_{LH}<P_2$ at both
   signals.
4. Sign. $LH$ has the smallest probability of good news, $a/(1+a)$, and $HH$ has $1/(1+a)$. By Bayes' rule,
   $\Pr(LH\mid g)<\Pr(LH)<\Pr(LH\mid b)$. With entry fixed across signals, the buyers are the types with the
   highest $V_s$, so good news raises the price: $P_2(g)>P_2(b)$.
5. After $d_1=0$: $V_s-P_2=e_2(t_{j_2}-\textstyle\sum\nu'(s')t_{j_2'})$, which is at most $\Delta_T$ in absolute
   value. If $\Delta_T<k$, every purchase loses. $\square$

The three conditions hold with wide margins at every $b\in\{1.2,1.5,2,3\}$, $\kappa\in\{-0.5,0,0.5\}$ and
$r\in\{1.2,2,3,3.6,4.2\}$ (`c4_bounds.py`). At $b=2$ the bound in item 2 is at least $0.739$ (against $k=0.02$), and the
slack in item 3 is at least $0.747$. Over all four scales the smallest values are $0.466$ and $0.235$.

What the information is about depends on type $HL$. If only $HH$ buys, the signal moves the posterior on
$j_2$ as well. If $HH$ and $HL$ both buy, the signal is about $j_1$ alone; with independent classes it then
says nothing about challenger 2's own class, yet it still moves $\Pr(LH)$.

**Proposition C4.2, continued (strong incumbent; analytical).** Suppose that after $d_1=0$ the round-2
equilibrium has full purchases by the $j_2=H$ types and none by the $j_2=L$ types. Then, as an experiment
about $j_2$, the round-2 price after $d_1=0$ Blackwell-dominates the round-2 price after $d_1=1$ at the
same history, and strictly so under items 2–3 above.

*Proof.* Take binary signals, a binary state and a common prior. Then one experiment dominates another if
and only if the second one's posteriors lie between the first one's posteriors. The reason: two-point
posterior laws with a common mean are ordered by mean-preserving spread exactly when their supports nest. Full purchases
by $j_2=H$ types give likelihood ratios $1/a$ and $a$ about $j_2$, the extremes allowed by Lemma 1(c).
Every buy-only experiment has likelihood ratios inside $[a,1/a]$, so its posteriors lie inside. After
$d_1=1$, $HH$ buys and $LH$ does not, so the ratio is interior and the inclusion is strict. $\square$

So entry by challenger 1 raises the informativeness of the round-2 price about challenger 2's class only
at weak incumbents. At strong incumbents it lowers it.

### Result 6 (analytical): informed trading in round 1 at every incumbent strength

**Proposition C4.3 (informative first round at every strength; analytical).** Assume (NC) and the selection
rule of §2.4. In every equilibrium, investor 1's type $LL$ never buys, and type $HH$ buys with probability one if

$$
\rho^2\,(1-\psi_1(\pi_{HH}))\,D_r>k .
$$

So the round-1 price is informative at every incumbent strength. At $b=2$, $\kappa=0$, the left side is
0.362 at $r=1.2$, 0.336 at $r=3$ and 0.325 at $r=3.6$, against $k=0.02$.

*Proof.* Write $Y_s(S_1)=e_1W_s(S_1,1)+(1-e_1)W_s(S_1,0)$ for type $s$'s expected terminal value after
signal $S_1$.

1. By (NC), $W_s(S_1,1)=V_s$ of Result 5.
2. After $d_1=0$, round 2 is the single-challenger game about $j_2$. There $V_L\le P_2$, so $j_2=L$ types
   never buy. If $j_2=H$ types buy with positive probability, the posterior on $j_2=H$ is higher after good
   news. So challenger 2's gain is higher there, and its entry is weakly higher (at most one signal can be at
   a tie). Hence $\bar e_2(j_2=H)\ge\bar e_2(j_2=L)$. Also $t_H\ge t_L>t_0$. The second inequality holds
   pointwise: with a prepared challenger the payment is at least $p$, and without one it is
   $p\,\mathbf 1\{R\ge p\}$, so $t_L-t_0\ge p\Pr(R<p)=p^2/r$. So $W_s(S_1,0)=t_0+\bar e_2(s)(t_{j_2}-t_0)$ is
   largest for $j_2=H$ and smallest for $j_2=L$. The selection rule gives equal values within each $j_2$ class.
3. $LL$ has the smallest $V_s$ and the smallest $W_s(S_1,0)$, so $Y_{LL}\le P_1$ and a purchase earns at
   most $-k$.
4. $Y_{HH}-Y_s\ge e_1(V_{HH}-V_s)\ge\rho\cdot\rho D_r$ for $s\ne HH$. So
   $Y_{HH}-P_1\ge(1-\mu_1(HH))\rho^2D_r\ge(1-\psi_1(\pi_{HH}))\rho^2D_r$ at each signal. $\square$

The economics: the round-1 investor trades on the joint state. In state $HH$ the target receives $h$
whenever both challengers prepare, which the low-cost types alone produce with probability $\rho^2$. The
spread that drives trading is of order $\rho D_r\approx\rho(h-\ell)$, not $\Delta_T(r)$. Incumbent strength no
longer decides whether the price is informative.


### Result 7 (computer-assisted): the benchmark equilibrium

**Proposition C4.4 (benchmark equilibrium; computer-assisted).** Take $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$,
$k=1/50$, $b=2$, $\kappa=0$, $c_L=0$, and $c_H\in\{5,\ 29/5\}$. At each $r\in\{6/5,\ 3,\ 18/5\}$:

1. The game has exactly one equilibrium in which every player uses a pure strategy and the round-1 price
   reveals the round-1 signal.
2. At $r=6/5$ this equilibrium is the unique equilibrium, mixed strategies and pooled prices included.
3. Its form:
   - Round 1: only type $HH$ buys. Challenger 1's high-cost type never prepares.
   - After $d_1=1$: type $HH$ buys (with $HL$ also after bad news at $r=18/5$). Challenger 2's high-cost
     type never prepares.
   - After $d_1=0$: no trade at $r=6/5$; the $j_2=H$ types buy at $r\in\{3,18/5\}$.
   - Challenger 2's high-cost type prepares only after $d_1=0$, at these histories:

| $c_H$ | $r=1.2$ | $r=3$ | $r=3.6$ |
|---|---|---|---|
| 5 | after round-1 good news | after good news in both rounds | after good news in both rounds |
| 5.8 | never | after good news in both rounds | never |

*Method.* `c4_certify.py` encloses every equilibrium inequality in interval arithmetic, with $a=e^{-1/2}$
enclosed and exact rational parameters. It works backward over all 64 round-2 subgames that follow a pure
round-1 profile, and it tests each of their 64 pure candidates. Each subgame has exactly one certified pure
equilibrium; every other candidate is refuted; no candidate is undecided. The same holds for the 64
round-1 candidates. The smallest certified margin is $0.0128$. The run also covers $r=3$, $\kappa=1/2$,
$c_H=5$, with the same form.

Price sufficiency is part of the certificate. A certified candidate must have two certainly different prices
in each informative round, so the challenger reads the signal from the price; the certified round-1 gaps are
$0.106$ to $0.464$. Pooled round-2 prices are also covered. For every informative pure round-2 investor
profile, either the two prices certainly differ for every common entry probability, or the pooled candidate
(entry set at the pooled belief) fails an investor inequality. Pooled round-1 prices are not tested, hence
the scope of item 1.

*Mixed strategies at $r=6/5$.* `c4_unique_r0.py` checks the analytical steps of Results 4–6 as certain
interval inequalities. Those steps fix every choice except investor 1's purchase probabilities of $HL$ and
$LH$. An interval enclosure over the whole square $[0,1]^2$ then shows that both purchase margins are
negative for every admissible entry response; the largest upper bounds are $-0.144$ and $-0.146$. The
entry hull also covers challenger mixing and pooled prices. So no equilibrium has a purchase by $HL$ or
$LH$, and the rest of the equilibrium is pinned with strict margins.

At $r=3$ and $r=3.6$, uniqueness among mixed strategies is a **numerical diagnostic**: the search in
`c4_core.py` (investor mixtures in both rounds, challenger mixtures at ties, and cross-round ties) finds
no other equilibrium.

**Closed forms on this branch** (`c4_closed_form.py`). With only $HH$ buying in round 1:

- $\mu_1(\cdot\mid g)=(1,a,a,a)/(1+3a)$ and $\mu_1(\cdot\mid b)=(a,1,1,1)/(a+3)$ over $(HH,HL,LH,LL)$.
  Round-1 good news has probability $(1+3a)/(4(1+a))=0.438770$.
- Challenger 1's gain: $\Gamma_1(g)=(1-\rho)g_L+D_r\frac{1-\rho+a}{1+3a}$ and
  $\Gamma_1(b)=(1-\rho)g_L+D_r\frac{1+a-\rho a}{a+3}$. Values: $4.5563$ and $3.8583$ at $r=1.2$; $4.1030$ and
  $3.4555$ at $r=3$; $3.9564$ and $3.3300$ at $r=3.6$.
- Challenger 2's posterior on $j_2=H$ after $d_1=0$: $(1+a)/(1+3a)=0.569774$ after round-1 good news. After
  good news in both rounds (with full purchases by the $j_2=H$ types in round 2) it is
  $(1+a)/(1+a+2a^2)=0.685880$.
- Hence challenger 2's gain after $(g,d_1=0)$ is $B_{1.2}(0.569774)=5.4310$ at $r=1.2$. After good news in
  both rounds it is $5.8407$ at $r=3$ and $5.6331$ at $r=3.6$.
- Entry of challenger 2: $\mathsf E_2=\rho^2+(1-\rho)[\Pr(g)+\Pr(b)\rho]=0.496808$ when it prepares after
  every $(g,d_1=0)$; $\mathsf E_2=0.377622$ when it needs good news in both rounds.

### Result 8 (numerical diagnostic; computer-assisted at $c_H\in\{5,5.8\}$): where each force wins across incumbent strengths

The no-cascade result is about challengers at one strength. The paper's title result is a comparison
across strengths. On the benchmark branch the two challengers behave differently.

1. **Challenger 1: deterrence wins (numerical diagnostic on the grid).** Its round-1 information is the same at every strength (only $HH$
   trades). Its gain falls with $r$ at every belief. So its entry is weakly decreasing in $r$, as in
   Proposition A.3. For $c_H>4.5563$ it is $\rho$ at all three strengths.
2. **Challenger 2: the outcome depends on its cost.** After $d_1=0$, challenger 2 faces the paper's
   one-challenger round 2, with the round-1 price as extra information. At $r_0$ that round has no trade
   ($\Delta_T<k$); at $r_1$ it is informative. The extra round-2 signal pushes entry up; the lower gain
   pushes it down. With independent classes:

| Cost window | $\mathsf E_2$ at $r=1.2,\ 3,\ 3.6$ | From $r_0$ to $r_1$ |
|---|---|---|
| $(4.5563,\ 4.6972]$ | $0.4968,\ 0.5313$; at $r=3.6$ only mixed equilibria, $\approx0.474$ | information (small rise) |
| $(4.6972,\ 4.8731]$ | $0.4968,\ 0.5313,\ 0.3776$ | information (small rise) |
| $(4.8731,\ 5.4310]$ (contains $c_H=5$) | $0.4968,\ 0.3776,\ 0.3776$ | deterrence |
| $(5.4310,\ 5.6331]$ | $0.25,\ 0.3776,\ 0.3776$ | information |
| $(5.6331,\ 5.8407]$ (contains $c_H=5.8$) | $0.25,\ 0.3776,\ 0.25$ | information, then the ceiling |
| above $5.8407$ | $0.25,\ 0.25,\ 0.25$ | neither |

Each endpoint is one of challenger 2's gains in the closed forms:

- $4.5563=\Gamma_1(g)$ at $r=1.2$; below it challenger 1 is recruited instead.
- $4.6972$ and $4.8731$: the gain after (bad news, $d_1=0$, good news) at $r=3.6$ and $r=3$.
- $5.4310$: the gain after (good news, $d_1=0$) at $r=1.2$, where round 2 has no trade.
- $5.6331$ and $5.8407$: the gain after good news in both rounds at $r=3.6$ and $r=3$.

`c4_windows.py` confirms every window on a grid of step $0.02$ in $c_H$. It lists all equilibria with pure
round-1 strategies; at $\kappa\in\{0,0.5\}$ every one it finds is pure in both rounds. Challenger 1's entry
is $\rho$ throughout these windows, and $\Pr(d_2=1\mid d_1=1)=\rho$ in every equilibrium on the grid
$c_H\in[3.6,6.2]$ at $\kappa\in\{0,0.5\}$. Proposition C4.4 certifies the two marked points.

3. **A lone challenger with the same cost.** With one challenger, entry is $0.25,\ 0.625,\ 0.625$ at
   $c_H=5$ and $0.25$ at all three strengths at $c_H=5.8$ (the lone-challenger window is
   $(4.8042,\ 5.3122]$). So two potential challengers reverse the paper's comparison at $c_H=5$. At
   $c_H=5.8$ they create a rise and fall where a lone challenger has none: the round-1 price, informative
   because of the $HH$ trades, adds a second signal about $j_2$.

### Result 9 (numerical diagnostic): scans over costs and correlation

`c4_scan.py` searches at $r\in\{1.2,3,3.6\}$ and $c_H\in\{3.6,3.8,\dots,6.0\}$ (16 values) for $\kappa\in\{0,0.5\}$,
and at $c_H\in\{4.4,4.6,\dots,5.6\}$ for $\kappa=-0.5$. The search covers:

- pure profiles;
- one mixing investor class in each round;
- challenger mixing at ties;
- cross-round ties: investor 1 mixes so that challenger 2 is exactly indifferent, and challenger 2 mixes so
  that investor 1 is indifferent.

It keeps every combination of round-2 equilibria. `c4_windows.py` adds a grid of step $0.02$ with pure round-1 strategies for every $\kappa$.

Findings for $\kappa\in\{0,0.5\}$:

1. **No cascade anywhere.** Every equilibrium found has $\Pr(d_2=1\mid d_1=1)=\rho=0.25$. This includes
   the points where (NC) fails ($\kappa=0$, $c_H<4.27$ at $r=1.2$; $c_H<3.96$ at $r=3$).
2. **Round-1 trading is informative in every equilibrium found** (type $HH$ always buys).
3. **Correlated classes** ($\kappa=0.5$) give the same windows, shifted up: deterrence from $r_0$ to $r_1$ for
   $c_H\in(4.6,5.7]$ ($\mathsf E_2$: $0.514\to0.388$), information for $(5.7,5.8]$ ($0.25\to0.388$), and a rise
   and fall for $(5.8,6.0]$ ($0.25\to0.388\to0.25$). Round-1 good news now says more about $j_2$, because
   $j_1$ and $j_2$ move together. Proposition C4.4 certifies $r=3$, $c_H=5$, $\kappa=1/2$.
4. **Coexistence: which challenger the price recruits.** At $\kappa=0$, $r=3$, $c_H\in\{3.8,4.0,4.2\}$ three
   equilibria coexist. In one, only $HH$ buys in round 1 and good news recruits challenger 1
   ($\mathsf E_1=0.579$, $\mathsf E_2=0.404$ at $c_H=4$). In another, $HH$ and $LH$ buy, so the round-1 price is
   about $j_2$; it recruits challenger 2 after $d_1=0$ ($\mathsf E_1=0.25$, $\mathsf E_2=0.663$). The third mixes
   between them. The same pattern appears at $r=3.6$, $c_H=3.8$, and at $\kappa=0.5$.
5. **Cross-round ties.** At $\kappa=0$, $r=3.6$, $c_H\in[4.14,4.68]$ no equilibrium with pure round-1 strategies
   exists. The search
   finds equilibria in which investor 1's type $LH$ mixes ($0.90$, $0.57$, $0.20$ at $c_H=4.2,4.4,4.6$) and
   challenger 2 mixes after (bad news, $d_1=0$, good news). This is the structure of Proposition 3, spread
   over two rounds. Entry there is $\mathsf E_1=0.25$, $\mathsf E_2\approx0.474$.
6. **Round-2 trading after entry can have several equilibria** (for example $HL$ buys or not at $r=3.6$).
   Under (NC) they change the information in the round-2 price but not entry, proceeds or any earlier
   incentive.

Findings for $\kappa=-0.5$:

Condition (NC) fails at most of these points. `c4_negcorr.py` lists every equilibrium with pure round-1
strategies at $c_H\in\{3.6,\dots,4.1,4.4,4.5,5.2,5.6\}$; `c4_windows.py -0.5` covers the grid of step $0.02$.

7. **Challenger 2 is sometimes recruited after a first entry.** Examples: $\Pr(d_2=1\mid d_1=1)=0.518$ at
   $r=1.2$, $c_H=3.6$; $0.326$ at $r=3$, $c_H=3.6$; $0.331$ at $r=3.6$, $c_H=3.6$. With negative correlation the state
   $LH$ has prior $0.375$. Bad news in both rounds moves weight from the buying states ($HH$ in round 1; $HH$
   and $HL$ in round 2) to $LH$ and $LL$. At $r=3$ this lifts $\Pr(LH)$ to $0.485$, and the gain $8.333\times0.485=4.04$
   exceeds $c_H=3.6$.
8. **Still no entry cascade.** In every equilibrium found, challenger 2 prepares less often after a first
   entry. On path: for example $0.282$ against $0.620$ at $r=3$, $c_H=3.9$, and $0.266$ against $0.449$ at $r=3.6$,
   $c_H=4.5$. History by history, where challenger 1 always prepares: $0.518$ against $1$ at $r=1.2$, $c_H=3.6$,
   and $0.326$ against $0.625$ at $r=3$, $c_H=3.6$ (the comparison uses the off-path continuation of §2.4).
9. **Gaps without pure round-1 strategies.** At $r=3$, $c_H\in\{4.04\}\cup[4.18,5.10]$, and at $r=3.6$,
   $c_H\in[4.04,4.40]$, no equilibrium with pure round-1 strategies exists. The full search (`c4_scan.py -0.5`)
   finds exactly one equilibrium at each of $r=3$, $c_H\in\{4.4,4.6,4.8,5.0\}$, and each one mixes:
   - at $c_H=4.4$, investor 1's type $LH$ buys with probability $0.780$ and challenger 1 mixes at a tie after
     bad news ($\mathsf E_1=0.343$);
   - at $c_H\in\{4.6,4.8,5.0\}$, type $LH$ buys with probability $0.672$, $0.429$, $0.158$, and challenger 2 mixes
     after (bad news, $d_1=0$, good news); at $c_H=5$ its entry there is $0.392$.

   In all four, $\Pr(d_2=1\mid d_1=1)=0.25$, against $\Pr(d_2=1\mid d_1=0)=0.628$, $0.477$, $0.466$ and $0.453$.
   At $r=3$, $c_H\in\{5.2,5.4,5.6\}$ the equilibrium is pure, with $0.25$ against $0.406$. At $r=3.6$,
   $c_H\in\{4.6,\dots,5.6\}$, types $HH$ and $LH$ buy in round 1 in a pure equilibrium, with $0.25$ against
   $0.449$. At $r=3.6$, $c_H=5.6$ two more equilibria coexist (conditional entries $0.25$ against $0.25$, and $0.25$
   against $0.391$).
   At $r=3.6$, $c_H=4.4$ the search finds no equilibrium at all. This is a documented failure of the search,
   not a proof of nonexistence. The searched class omits two mixing investor types in one round, and a
   challenger-1 tie combined with a cross-round tie. A finer grid ($n=120$) was started at this point and
   not completed. Existence at this point is open.
10. **The grid.** On the grid of step $0.02$ (`c4_windows.py -0.5`), every equilibrium with pure round-1
    strategies and $\mathsf E_1<1$ has $\Pr(d_2=1\mid d_1=1)\le\Pr(d_2=1\mid d_1=0)$. The grid output has 108
    distinct equilibrium entries; the comparison applies to those with $\mathsf E_1<1$. Where $\mathsf E_1=1$, `c4_negcorr.py` gives the history-by-history comparison above.

**Conjecture C4.5.** At the benchmark values, for every $\kappa\in[-1/2,1/2]$, every equilibrium has
$\Pr(d_2=1\mid d_1=1)\le\Pr(d_2=1\mid d_1=0)$, and the same inequality averaged over round-1 signals when
$d_1=0$ is off path. Proposition C4.1 proves the signal-by-signal version wherever (NC) holds. The scans
support the conjecture elsewhere; they test the aggregate and averaged versions only.

### Result 10 (numerical diagnostic, with an analytical step): target proceeds and welfare

Welfare is the allocation value minus preparation costs, as in Section 6.1 of the paper. Trading costs are
reported separately. Four economies (`c4_summary.py`):

- SEQ: two challengers in sequence, prices observed.
- SEQ-H: two challengers, prices hidden from both challengers.
- ONE: one challenger, price observed (the discrete-Laplace game of workstream B).
- ONE-H: one challenger, price hidden.

Independent classes, $c_H=5$:

| $r$ | Economy | $\mathsf E_1$ | $\mathsf E_2$ | Both | High-class owner | Proceeds | Net surplus | Trading cost |
|---|---|---|---|---|---|---|---|---|
| 1.2 | SEQ | 0.2500 | 0.4968 | 0.0625 | 0.3750 | 0.7287 | 2.9870 | 0.0063 |
| 1.2 | SEQ-H | 0.2500 | 0.2500 | 0.0625 | 0.2344 | 0.6286 | 2.8292 | – |
| 1.2 | ONE | 0.2500 | – | – | 0.1250 | 0.3927 | 1.7490 | 0 |
| 3 | SEQ | 0.2500 | 0.3776 | 0.0625 | 0.3219 | 1.0283 | 3.6205 | 0.0138 |
| 3 | SEQ-H | 0.2500 | 0.2500 | 0.0625 | 0.2344 | 0.9115 | 3.5026 | – |
| 3 | ONE | 0.6250 | – | – | 0.3584 | 0.9421 | 2.7004 | 0.0100 |
| 3.6 | SEQ | 0.2500 | 0.3776 | 0.0625 | 0.3219 | 1.1282 | 3.8202 | 0.0145 |
| 3.6 | SEQ-H | 0.2500 | 0.2500 | 0.0625 | 0.2344 | 0.9866 | 3.7306 | – |
| 3.6 | ONE | 0.6250 | – | – | 0.3584 | 1.0579 | 2.8881 | 0.0100 |

ONE-H has entry $\rho$, proceeds $0.3927,\ 0.6146,\ 0.6642$ and net surplus $1.7490,\ 2.5521,\ 2.8163$ at the three
strengths. At $c_H=5.8$, SEQ differs from SEQ-H only at $r=3$: proceeds $1.0283$ against $0.9115$, net surplus
$3.5184$ against $3.5026$.

Findings:

1. **Access to prices (analog of Proposition A.9).** In every case above, SEQ has higher proceeds and higher
   net surplus than SEQ-H. The analytical step: on this branch challenger 1's entry is $\rho$ with and without
   prices, so price access changes only challenger 2's high-cost preparation after $d_1=0$. Each added
   preparation has expected gross gain at least $c_H$. Against the incumbent alone, its allocation increment
   exceeds its gross gain by exactly $p^2/r$ for either class: for the low class,
   $\ell+\Delta_T-\frac{r^2-p^2}{2r}-\frac{\ell^2-p^2}{2r}=\frac{p^2}{r}$, and the high class gives the same value.
   It also raises proceeds by $t_{j_2}-t_0>0$. Trading costs are not compared: the SEQ-H trading game is not
   solved here.
2. **Two potential challengers against one.** Proceeds and net surplus are higher with two potential
   challengers at every strength. This holds even at $r=3$, where the lone challenger is recruited more often
   (0.625, against 0.25 and 0.3776). The second challenger's low-cost type alone adds a contest, and a two-high contest
   pays the target $h$.
3. **Ownership.** With two challengers the high-class owner probability falls from $r=1.2$ to $r=3$
   ($0.3750\to0.3219$), the reverse of the lone-challenger comparison ($0.1250\to0.3584$).
4. **Across strengths.** In SEQ, proceeds and net surplus rise with $r$ at $c_H=5$ even though entry falls.
   The incumbent's higher values raise every payment.



## 4. What it recovers or loses relative to the Laplace paper

| Paper result | In the sequential discrete model | Status here |
|---|---|---|
| Prop. 1 (two returns to information) | Extends as the spread–rent table. A same-class first entrant maximizes the spread across challenger 2's class and removes all of challenger 2's gain. The opposition becomes extreme. | analytical (Results 1–2) |
| Prop. A.1 (posterior bounds) | Per round $[a,1/a]$; two rounds $[a^2,a^{-2}]$, for arbitrary mixtures. | analytical (Lemma 1) |
| Prop. A.2 (price sufficiency) | Not automatic: four states and one price per round. Each price reveals its round's binary signal when the two prices differ. True in every equilibrium of Results 7, 8 and 10: the smallest round-1 gap is $0.106$ and the smallest on-path round-2 gap is $0.040$. | computer-assisted at the points of Prop. C4.4; numerical diagnostic elsewhere |
| Prop. 2(i) (weak incumbent: no trade, entry $\rho$) | Lost. Round-1 trading is informative at every strength, because state $HH$ is worth $h$ to the target when both challengers prepare. | analytical (Prop. C4.3) |
| Prop. 2(ii) (stronger incumbent raises entry) | Lost for challenger 1 (its information does not depend on $r$). For challenger 2 it holds in some cost windows and reverses in others; at $c_H=5$ it reverses. | computer-assisted at points; numerical windows (Result 8) |
| Prop. 2(iii) (return to $\rho$) | Holds for challenger 2 in the window $(5.6331,5.8407]$. | computer-assisted at $c_H=5.8$ |
| Prop. 3 (coexistence) | Multiplicity appears: two pure equilibria recruit different challengers (for example $r=3$, $c_H=4$). Mixed equilibria in which investor 1 keeps challenger 2 exactly indifferent have the structure of Prop. 3. | numerical diagnostic (Result 9) |
| Prop. A.3 (fixed experiment) | Holds across challengers (Result 3) and across strengths for each challenger. | analytical |
| Prop. A.4 (thresholds) | The no-trade region $r\le r_N$ disappears whenever $\rho^2(1-\psi_1(\pi_{HH}))D_r>k$. | analytical |
| Props. A.5–A.8, A.10; Sections 5.2–5.3, 6.2–6.3 | Not studied. | – |
| Prop. A.9 (access to prices) | Holds at the benchmark points: price access raises proceeds and net surplus. | numerical diagnostic, with an analytical step |
| Section 7 (empirical predictions) | New predictions: (a) a further buyer prepares less often after a first preparation; (b) after a first preparation its preparation does not respond to the target price, and a higher price then signals a strong first entrant. | analytical within the model |


## 5. Numerical example

### 5.1 The benchmark equilibrium at $r=3$, $c_H=5$, independent classes

Inputs: $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$, $c_L=0$, $c_H=5$, $b=2$, $k=0.02$, $\kappa=0$.
Auction objects: $\Delta_T=0.666667$, $g_L=0.125$, $D_r=8.333333$, $B_3(1/2)=4.291667$.

Round 1. Only type $HH$ buys. Purchase margins: $HH$ $+0.5614$, $HL$ $-0.2690$, $LH$ $-0.0844$, $LL$ $-0.4357$.

| Signal | Posterior $(HH,HL,LH,LL)$ | Price $P_1$ | Challenger 1's gain | Challenger 1's entry |
|---|---|---|---|---|
| good | $(0.3547,0.2151,0.2151,0.2151)$ | 1.251177 | 4.1030 | $\rho$ |
| bad | $(0.1682,0.2773,0.2773,0.2773)$ | 0.854068 | 3.4555 | $\rho$ |

Round 2 (round-2 buyers; challenger 2's gain after good and bad round-2 news; prices):

| History | Buyers | Gain after $g$ / $b$ | Entry after $g$ / $b$ | $P_2(g)$ / $P_2(b)$ |
|---|---|---|---|---|
| $g$, $d_1=1$ | $HH$ | 1.4573 / 2.0833 | $\rho$ / $\rho$ | 2.35924 / 1.80208 |
| $g$, $d_1=0$ | $HH$, $LH$ | 5.8407 / 3.8371 | 1 / $\rho$ | 1.33225 / 0.60549 |
| $b$, $d_1=1$ | $HH$ | 2.0833 / 2.4744 | $\rho$ / $\rho$ | 1.80208 / 1.45407 |
| $b$, $d_1=0$ | $HH$, $LH$ | 4.8731 / 2.8550 | $\rho$ / $\rho$ | 0.62621 / 0.58585 |

Read the rows with $d_1=1$: the higher round-2 price comes with the lower gain for challenger 2
(Proposition C4.2, item 4). In the rows with $d_1=0$ the order is the paper's: a higher price raises the gain.

Outcomes: $\mathsf E_1=0.25$, $\mathsf E_2=0.377622$, both $0.0625$,
$\Pr(d_2=1\mid d_1=1)=0.25$, $\Pr(d_2=1\mid d_1=0)=0.420162$, high-class owner $0.321908$,
proceeds $1.028307$, allocation value $4.258637$, preparation costs $0.638109$, net surplus $3.620527$,
trading costs $0.013750$.

The same parameters with one challenger give entry 0.625 (the brief's candidate value, confirmed).

### 5.2 Scripts and outputs

All scripts are print-only and run from the repository root with `.venv/bin/python`. Runs longer than
60 seconds used `scripts/_slots/run_slot.sh`. Output files sit next to each script.

| Script | What it does | Output |
|---|---|---|
| `c4_auction.py` | three-bidder auction objects; closed forms against `quad` | `c4_auction_output.txt` |
| `c4_bounds.py` | the sufficient conditions of Results 4–6 over $b$, $\kappa$, $r$ | `c4_bounds_output.txt` |
| `c4_core.py` | the model and the equilibrium search (module) | – |
| `c4_flowcheck.py` | recomputes solved equilibria over integer flows | `c4_flowcheck_output.txt` |
| `c4_certify.py` | interval certificate of the pure equilibria (Prop. C4.4) | `c4_certify_output.txt` |
| `c4_unique_r0.py` | interval proof of uniqueness over mixtures at $r=1.2$ | `c4_unique_r0_output.txt` |
| `c4_closed_form.py` | closed forms and cost thresholds on the benchmark branch | `c4_closed_form_output.txt` |
| `c4_windows.py KAPPA` | fine $c_H$ grid, equilibria with pure round-1 strategies, merged into windows | `c4_windows_k0.txt`, `c4_windows_k05.txt`, `c4_windows_km05.txt` |
| `c4_negcorr.py` | conditional entry of challenger 2 at $\kappa=-0.5$, on and off path | `c4_negcorr_output.txt` |
| `c4_scan.py KAPPA` | coarse $(r,c_H)$ table with mixed equilibria and information comparisons | `c4_scan_k0.txt`, `c4_scan_k05.txt`, `c4_scan_km05.txt`, `c4_scan_km05_r36b.txt` |
| `c4_summary.py` | proceeds and welfare in the four economies (Result 10) | `c4_summary_output.txt` |


## 6. Open issues

1. **A long-lived investor.** With one investor in both rounds, a round-1 purchase moves challenger 1's
   entry and so the round-2 trading profit. That is manipulation through a real decision. Not solved.
2. **Spread within a class (Reading N with non-degenerate $G_j$).** Two high-class challengers then do not
   tie, and the second keeps $\mathbb E(v_2-v_1)_+$ against a high-class first entrant. Condition (NC) must
   add this rent. With the paper's half-width $\varepsilon_V=0.05$ the rent is about $\varepsilon_V/3$, far below
   $c_H$. A wide class spread could reopen a cascade. Open.
3. **More than two challengers.** Conjecture: after any earlier entry, the next challenger's gain is $D_r$
   times the probability that every prepared rival is low-class and it is high-class. A no-cascade bound of
   the same form would follow. Not proved.
4. **Asymmetric challengers.** If challenger 1's high value is below $h$, a high-class challenger 2 keeps a rent
   against it, and the spread–rent opposition weakens. Open.
5. **Uniqueness over mixtures at $r=3$ and $r=3.6$.** Numerical diagnostic only. At $r=1.2$ it is
   computer-assisted.
6. **Lower costs.** For $c_H$ below about 4.3 (with $\kappa=0$), (NC) fails at $r=1.2$. No cascade appears in the
   scans there, but no proof covers that region. At $r=3.6$, $\kappa=0$, no pure equilibrium exists for
   $c_H\in[4.14,4.68]$ (Result 9). At $\kappa=-0.5$, $r=3.6$, $c_H=4.4$ the search finds no equilibrium;
   existence there is open.
7. **Price sufficiency.** It is certified at the points of Proposition C4.4, where round-1 pooling is covered
   only at $r=1.2$. Elsewhere it is checked in each reported equilibrium, not proved in general.
8. **Private information of challenger 1.** Here a decision reveals nothing about classes, so an
   informational cascade in the sense of Bikhchandani, Hirshleifer and Welch (1992) cannot arise. A
   challenger with a private signal would change this (D1 §3.14 makes the same point).
9. **Other bases.** Two-sided orders and the three-point base are not studied. In the three-point base a
   revealing top flow would remove the posterior bound behind Proposition C4.1.


## 7. Plain summary

Two potential challengers arrive in sequence. Before each decision, an investor who knows both classes may
buy the target's stock. Does the first entry trigger the second?

No. The first entrant deters the second, because of the auction. If the first entrant is high-class, the
target's payment becomes very sensitive to the second challenger's class: a second high-class bidder pushes
it up to $h$. But that extra payment comes out of the first entrant's rent, and the second challenger keeps
none of it. With independent or positively correlated classes, if the second challenger would not prepare
alone at the prior, its high-cost type never prepares after a first entry (analytical). With negative
correlation it sometimes does, but less often than without one (numerical).

The first decision reveals nothing about the classes, but it changes what the next price is about. Against a
weak incumbent, entry makes the second-round price informative. But a high price then signals a strong first
entrant, which tells the second challenger to stay out. Against a strong incumbent the price becomes less
informative about the second challenger's class.

The second challenger matters before it acts. Both challengers high-class is worth $h$ to the target, so
informed trading pays at every incumbent strength. The paper's no-trade result for a weak incumbent is lost
(analytical).

Across incumbent strengths, the first challenger's entry falls. For the second challenger the answer depends
on its cost. At the brief's cost $c_H=5$, a stronger incumbent lowers its entry from $0.497$ to $0.378$. At
$c_H=5.8$ its entry rises and then falls ($0.25$, $0.378$, $0.25$), which a lone challenger never shows at that
cost. Interval arithmetic certifies these equilibria. Access to prices raises proceeds and net surplus.

Open: a long-lived investor, value spread within a class, and more than two challengers.
