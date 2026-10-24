# C7. The incumbent responds to the price: preemption and jump bids

Workstream C7, brief item C.7. Scripts and outputs: `scripts/C7_incumbent/`.
Paper source: commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` of `overleaf/paper` (`main.tex`).

## 1. Question

The paper's incumbent is passive. It bids its value in the auction and does nothing else. Item C.7 lets the incumbent act after it sees the target price. The brief asks four questions:

1. Does an informative price trigger preemption after good news, when the high-class challenger is likely? Does that cut the entry gain from information?
2. Does the investor anticipate preemption and change its trading?
3. Does the mechanism survive, die, or reverse? Is there a new result?
4. What happens to target proceeds and welfare?

**Short answers.**

1. Yes. In the discrete-Laplace model, good news makes strong incumbents submit a binding early bid. That bid deters the high-cost challenger. Under the selection of §2.5, preemption never follows bad news or an uninformative price. At the benchmark, entry at $r_1=3$ falls from $0.625$ to $0.366988$.
2. Yes. The investor's expected purchase profit at $r_1$ falls from $0.175836$ to $0.058335$ (net of $k$). Under a stated condition, the investor earns exactly what it would earn if entry never responded to the price. At the benchmark $k$ it still buys, and the trading outcome is unchanged.
3. The mechanism survives but is weaker. It cannot be undone: incumbents too weak to bid stay silent, and silence invites entry. There are three new results:
   - at fixed information, preemption is a pure transfer from target shareholders to the incumbent;
   - it cuts the feedback from entry to trading profit;
   - it creates new mixed trading equilibria at weak incumbents.
4. Target proceeds fall by exactly the incumbent's gain ($0.171896$ at $r_1$). Acquisition surplus net of preparation costs does not change at $r_1$. It rises slightly when the smallest possible bid already over-deters.

## 2. Setup

### 2.1 Base model and why

I modify the **discrete-Laplace model** (TEAM_RULES §4.2): noise $Z=G_1-G_2$, $\Pr(Z=z)=\frac{1-a}{1+a}a^{|z|}$, $a=e^{-1/b}$, buy-only orders $q\in\{0,1\}$, $c_L=0$, Reading N with point masses $\ell,h$ and prior $\pi=1/2$. Reasons:

- **Bounded posteriors.** Under full buying the posteriors are $m_1=a/(1+a)=0.377541$ and $M_1=1/(1+a)=0.622459$. An incumbent can deter only if the challenger is uncertain about its own class. The three-point model reveals the class at the top flow ($\mu=1$). There no jump can deter at the benchmark, because the challenger's profit against the strongest incumbent, $h-r_1=7$, exceeds $c_H$ (Proposition C7.7).
- **Every flow is on path.** Off-path beliefs then enter only at the incumbent's bid, not at the price stage.
- **Comparability.** Workstream B1 reports the base discrete-Laplace equilibria. I reproduce the numbers I use (§5).

Benchmark: $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$, $c_L=0$, $c_H=5$, $b=2$, $k=0.02$, $\pi=1/2$, $\lambda=1$, $r_0=1.2$, $r_1=3$, $r_2=3.6$. I also report $c_H=5.05$ because $c_H=5$ hits a knife-edge (§2.5).

### 2.2 What changes: the incumbent's options

I study the three options of the brief in two models.

**Model L (lockup; brief options (a) first half and (b)).** After the price, the incumbent may privately offer the board an immediate sale at a price $T$. If the board accepts, the contest ends and the challenger cannot enter. If the board rejects, the game continues as without the offer. The challenger does not see the offer. The seller's reserve commitment binds negotiated sales, so $T\ge p$.

**Model J (jump bid; brief options (a) second half and (c)).** This is the main model. After the price, the incumbent chooses either **silence** or a **binding public opening bid** $J\ge p$. A bid $J$ commits the incumbent to pay at least $J$ if it wins. The challenger sees the price and the incumbent's action, then learns its cost and decides whether to prepare. Then the second-price auction runs with reserve $p$ and the incumbent's floor $J$.

Timing in Model J:

1. The seller commits to the auction with reserve $p$.
2. The investor learns the class $\theta$ and trades. Market makers see the flow $X=q+Z$ and set $P(X)=\mathbb E[V_T\mid X]$. They anticipate steps 3–5.
3. The incumbent sees the price and its value $R\sim U[0,r]$. It stays silent or bids $J$.
4. The challenger sees the price and the incumbent's action. It learns its cost $C\in\{0,c_H\}$, with $\Pr(C=0)=\rho$. It prepares or not.
5. Prepared bidders learn values and bid truthfully. Payoffs follow.

The incumbent does not see $\theta$. It knows only the public posterior $\mu$ that the price reveals. So a bid carries information about $R$, never about $\theta$.

### 2.3 Auction payoffs after a bid

Let $R\ge J\ge p$. In an ascending auction with the incumbent's standing bid $J$, the incumbent bids up to $R$. Hence:

- if the challenger enters with $\theta>R$, it wins and pays $R$;
- if the challenger enters with $\theta<R$, the incumbent wins and pays $\max\{J,\theta\}$;
- if the challenger stays out, the incumbent wins and pays $J$.

Truthful bidding stays weakly dominant. A type $R<J$ that bids $J$ pays more than its value when it wins at $J$. Silence gives the paper's auction with reserve $p$.

### 2.4 Shared objects

From TEAM_RULES §3 (checked against equation (4) of the pinned paper): $t_0,t_H,t_L,g_H,g_L$, $\Delta_T=(r-\ell)^2/(2r)$, and $B_r(\mu)=g_L+\mu(g_H-g_L)$. New objects:

- $D_\mu(a,c)$: the challenger's expected gross profit at posterior $\mu$ when it believes $R\sim U[a,c]$. Write $D_\mu(a)=D_\mu(a,r)$. Then $D_\mu(0)=B_r(\mu)$. For $p\le a\le\ell$ and $\ell\le a<r$,

$$
D_\mu(a)=\mu\Big(h-\frac{a+r}{2}\Big)+(1-\mu)\frac{(\ell-a)^2}{2(r-a)},
\qquad
D_\mu(a)=\mu\Big(h-\frac{a+r}{2}\Big).
$$

The second term is $\mathbb E[(\ell-R)_+\mid R\ge a]$. A winning challenger pays $R$ because $R\ge a\ge p$.

- $S(\mu)=\mathbb E[V_T\mid H,\mu]-\mathbb E[V_T\mid L,\mu]$: the **target-payoff spread at posterior $\mu$**, under the continuation that the model selects at $\mu$. In the paper, $S(\mu)=e_r(\mu)\Delta_T$.

### 2.5 Equilibrium concept, beliefs, ties, and selection

**Concept.** Perfect Bayesian equilibrium with competitive prices. The investor evaluates a deviation against fixed price and continuation schedules (paper §2.4). The continuation after each posterior is itself a signaling game between the incumbent and the challenger.

**Off-path belief rule at the incumbent's bid (rule IC-P).** After an off-path bid $J$, the challenger's belief about $R$ is the prior restricted to some types. These are the types for which $J$ is *not* equilibrium-dominated. A type is equilibrium-dominated at $J$ if $J$ cannot beat its equilibrium payoff even when the high-cost challenger stays out. If no type qualifies, the belief is the prior restricted to $R\ge J$.

Why a rule is needed. The Intuitive Criterion and D1 leave a continuum of jump levels (derivation in Proposition C7.3, part (e)). Rule IC-P is the Intuitive Criterion plus prior-proportional beliefs on the surviving types. It selects the least-cost deterring bid.

**Tie rules.**

- Investor: indifferent investors may mix. I report the pure outcome when it is unique.
- Challenger: an indifferent challenger prepares (paper §2.2), with one exception. After a bid at the deterrence boundary, an indifferent high-cost challenger stays out. Proposition C7.3(d) shows that this exception reports the limit of exact equilibria on a bid grid under the paper's rule.
- Board (Model L): the board rejects when indifferent. The incumbent does not offer when indifferent.

**Selection at posteriors that need no deterrence ("minimal preemption").** When $B_r(\mu)<c_H$, silence by all types is an equilibrium with entry $\rho$. I select it. A second equilibrium exists when $\mu h+(1-\mu)\ell-p\ge c_H$: every type $R\ge p$ bids $p$, and silence reveals $R<p$. It changes entry only for types $R<p$ and never changes the spread $S$. At $\mu=1/2$ with $c_H=5$ the inequality holds with equality: $5.5-0.5=5$. This is a knife-edge of the benchmark. It disappears for $c_H\in(5,5.312]$.

## 3. Results

### Proposition C7.1 (no seller-approved lockup; analytical)

*In Model L, at every posterior $\mu$, the probability that the board accepts a lockup is zero. This holds under the stated tie rules. If $\mu>0$, it holds under any tie rules. Prices, trading, and entry are therefore the same as without the lockup option.*

*Proof.* Fix $\mu$ and the continuation without a lockup. Entry $e\in[\rho,1]$ depends on $\mu$ only, because the challenger sees neither $R$ nor the offer.

Step 1: the joint payoff of the target and the incumbent is $R$ for every $R\ge p$ and every continuation outcome.

- Challenger enters with $\theta>R$: the target receives $\max\{p,R\}=R$; the incumbent gets $0$. Sum: $R$.
- Challenger enters with $\theta<R$: the incumbent pays $\max\{p,\theta\}$ and gets $R-\max\{p,\theta\}$. Sum: $R$.
- No entry: the incumbent pays $p$. Sum: $R$.

Step 2. Let $W(R)$ be the board's expected continuation proceeds given $R$ and $\mu$. Let $U_I(R)$ be the incumbent's continuation payoff. Step 1 gives $U_I(R)=R-W(R)$ for $R\ge p$. A lockup at $T$ gives the incumbent $R-T$. So type $R\ge p$ offers $T$ only if $W(R)\ge T$. Types $R<p$ never offer, because $R-T<0\le U_I(R)$.

Step 3. Let $O_T$ be the set of types that offer $T$. If it rejects, the board expects $\mathbb E[W(R)\mid R\in O_T]\ge T$. Acceptance with positive probability needs equality, so $W(R)=T$ for almost every offering type. Both parties are then indifferent, and the tie rules exclude the offer.

Step 4. For $R\ge p$, $W(R)=e[\mu\max\{p,R\}+(1-\mu)\max\{p,\min\{R,\ell\}\}]+(1-e)p$. On $[p,\ell]$ its slope is $e\ge\rho>0$. On $(\ell,r]$ its slope is $e\mu$. If $\mu>0$, $W$ is strictly increasing, so each level set is one point and has probability zero. $\square$

*Interpretation.* The second-price rule already pays the target the incumbent's value whenever the challenger wins. Excluding the challenger therefore creates no joint gain for the target and the incumbent. A lockup is a zero-sum bet against an informed incumbent, and the no-trade logic applies. Preemption can matter only by changing the **challenger's** beliefs. Model J studies that channel.

*Scope.* The proof covers a sale that ends the contest. It does not cover contracts that change the auction, such as stock-option lockups (a toehold), break fees, or matching rights. The paper abstracts from toeholds (Introduction).

### Lemma C7.2 (indifference map; analytical)

Fix $\mu$. Suppose silence leads to entry $1$ and a bid $J$ deters the high-cost challenger. Type $R$'s payoffs are

$$
U_S(R)=(1-\mu)(R-\ell)_+,\qquad
U_J(R)=(1-\rho)(R-J)+\rho(1-\mu)(R-\max\{J,\ell\})_+\quad(R\ge J).
$$

*Derivation.* After silence both cost types enter. The incumbent loses to $h$ (because $R<h$). It beats $\ell$ only if $R>\ell$, paying $\ell$. After the bid, the low-cost challenger enters with probability $\rho$. Otherwise the incumbent pays $J$.

Let $G(R;J)=U_J(R)-U_S(R)$.

- If $J\le\ell$: $G=(1-\rho)(R-J)$ on $[J,\ell]$, and $G=(1-\rho)[\mu R+(1-\mu)\ell-J]$ on $(\ell,r]$.
- If $J>\ell$ and $R\ge J$: $G=(R-J)(1-\rho\mu)-(1-\mu)(R-\ell)$, with slope $\mu(1-\rho)>0$.
- If $R<J$: $G<0$, since the bid can only cost type $R$ money.

So $G$ crosses zero once, from below, at

$$
\hat R(J)=J\ \ (J\le\ell),\qquad
\hat R(J)=\ell+(J-\ell)\frac{1-\rho\mu}{\mu(1-\rho)}\ \ (J>\ell).
$$

$\hat R$ is continuous and strictly increasing. Its inverse is $J(\hat R)=\hat R$ for $\hat R\le\ell$ and $J(\hat R)=\ell+(\hat R-\ell)\mu(1-\rho)/(1-\rho\mu)$ for $\hat R>\ell$. When $J\le\ell$, the marginal type's value equals its bid. It earns zero after silence, because it loses to every entrant. It also earns zero after the bid when no one enters.

### Proposition C7.3 (the incumbent's response at a posterior; analytical)

*Fix $r$ and a posterior $\mu$. Under rule IC-P and the selection of §2.5, the continuation outcome is as follows.*

- *Case A, $B_r(\mu)<c_H$: all types stay silent. Entry is $\rho$.*
- *Case B, $B_r(\mu)\ge c_H$ and $\mu(h-r)\ge c_H$: deterrence is infeasible. All types stay silent. Entry is $1$.*
- *Case C, $B_r(\mu)\ge c_H>\mu(h-r)$: let $a^*\in[0,r)$ solve $D_\mu(a^*)=c_H$ and set $\hat R^*=\max\{p,a^*\}$. Types $R>\hat R^*$ bid $J^*=J(\hat R^*)$. Types $R<\hat R^*$ stay silent. The high-cost challenger stays out after the bid and enters after silence. Entry is $\rho+(1-\rho)\hat R^*/r$.*

*Within Cases B and C this outcome is the unique equilibrium outcome under rule IC-P.*

*Proof.* (a) *Monotonicity.* $D_\mu(a)$ is continuous and strictly decreasing in $a$ on $[0,r)$. For $a\ge p$ this follows from the formula. For $a<p$, raising $a$ removes types that pay only $p$, the lowest payment. Its limit at $a\to r$ is $\mu(h-r)$, since $r>\ell$.

(b) *Case A.* Entry after any action is at least $\rho$, because $c_L=0$. Silence pooling gives entry $\rho$, the floor. A bid can only add a payment above $p$. So no type gains from any bid under any belief.

(c) *Case B.* After any bid, every belief has support in $[0,r]$. So the challenger's profit is at least $\mu(h-r)\ge c_H$, and it enters. A bid then only raises payments, and silence is optimal for all types.

(d) *Case C, existence.* By (a), $a^*$ exists and is unique, because $D_\mu(0)\ge c_H>\lim_{a\to r}D_\mu(a)$. Check the candidate:

- After the bid, the belief is $U[\hat R^*,r]$. Then $D_\mu(\hat R^*)\le c_H$, with equality when $a^*\ge p$. The high-cost challenger stays out (by the boundary convention when there is equality).
- After silence, the belief is $U[0,\hat R^*)$. $D_\mu(0,c)$ falls in $c$, so $D_\mu(0,\hat R^*)\ge D_\mu(0)\ge c_H$. The challenger enters.
- Lemma C7.2 makes types above $\hat R^*$ prefer $J^*$ and types below prefer silence.
- A lower bid $J<J^*$ yields the belief $U[\hat R(J),r]$ under IC-P. Since $\hat R(J)<\hat R^*$, this does not deter. A higher bid costs more.

*Bid grid.* Suppose bids lie on a grid with tick $\delta$, and the paper's tie rule holds everywhere. The smallest grid bid above $J^*$ deters strictly, and every lower grid bid fails to deter. The construction above is then an exact equilibrium, and its bid converges to $J^*$ as $\delta\to0$. The boundary convention reports this limit.

(e) *Case C, uniqueness under IC-P.* Take any equilibrium.

- A non-deterring bid gives entry $1$ and a higher payment than silence, so no type uses it.
- Two deterring bids cannot both be used, because every type prefers the lower one.
- Silence cannot deter. Otherwise no type would bid, the silent set would be all of $[0,r]$, and $D_\mu(0)\ge c_H$ would induce entry.

Hence the equilibrium uses one bid $J'$, with jumpers $[\hat R(J'),r]$ and $J'\ge J^*$. Suppose $J'>J^*$. Take $J\in(J^*,J')$. Its non-dominated types are $(\hat R(J),r]$, so IC-P gives the belief $U[\hat R(J),r]$. This belief deters, because $\hat R(J)>\hat R^*$. Then types above $\hat R(J)$ gain by deviating. So $J'=J^*$.

*Why IC and D1 alone do not suffice.* Take a candidate bid $J'>J^*$ and an off-path $J\in(J^*,J')$. Types in $(J,\min\{\ell,\hat R(J')\})$ earn zero in the candidate. They gain from $J$ under every high-cost entry probability $s<1$. Types above $\hat R(J')$ gain only for $s<(J'-J)/(R-J)$, a strictly smaller set. So D1 puts the belief on the low types $(J,\hat R(J'))$, which invites entry. The Intuitive Criterion allows a belief concentrated at $R=J$, which also invites entry. Both therefore support every $J'\in(J^*,\ell]$. They also support silence pooling in Case C. $\square$

*Closed form for $\hat R^*$.* If $D_\mu(p)>c_H\ge D_\mu(\ell)$, multiply $D_\mu(a)=c_H$ by $2(r-a)$. With $E_\mu=\mu h+(1-\mu)\ell$,

$$
a^2-2(E_\mu-c_H)a+\kappa=0,\qquad \kappa=\mu(2h-r)r+(1-\mu)\ell^2-2c_Hr,
$$

$$
\hat R^*=a^*=(E_\mu-c_H)-\sqrt{(E_\mu-c_H)^2-\kappa}.
$$

The quadratic opens upward. It is positive at $p$ and nonpositive at $\ell$, so the root in $[p,\ell]$ is the smaller one. If $D_\mu(\ell)>c_H$, then $\hat R^*=2(h-c_H/\mu)-r\in(\ell,r)$. If $D_\mu(p)\le c_H$, the threshold sits at the corner $\hat R^*=p$.

### Proposition C7.4 (preemption at fixed information: a transfer; analytical)

*Fix $\mu$ in Case C. Compare Model J with the paper's continuation, in which the incumbent cannot bid. Then:*

1. *the challenger's expected payoff rises by $\Delta_C=(1-\rho)(1-\hat R^*/r)[c_H-D_\mu(\hat R^*)]\ge0$;*
2. *acquisition surplus net of preparation costs rises by the same $\Delta_C$;*
3. *the target loses exactly what the incumbent gains: $\Delta T_{\text{target}}=-\Delta U_I=-\frac1r\int_{\hat R^*}^rG(R;J^*)\,dR<0$.*

*If $a^*\ge p$ (interior threshold), then $\Delta_C=0$: preemption is a pure transfer from target shareholders to the incumbent.*

*Proof.* Silent types face entry $1$ in both continuations, so nothing changes for them. For a jumper ($R\ge\hat R^*\ge p$), only the high-cost challenger's decision changes, from entering to staying out.

- *Challenger.* The low-cost challenger pays $R$ in both continuations, since $\max\{p,R\}=R$. The high-cost challenger loses $\mathbb E_\theta(\theta-R)_+-c_H$ on average over jumpers, which is $D_\mu(\hat R^*)-c_H\le0$. This gives part 1.
- *Surplus.* Paper equation (A.39) gives the surplus from entry, $(\theta-\max\{p,R\})_++p\mathbf 1\{R<p\}-C$. For $R\ge p$ this equals the challenger's net profit. This gives part 2.
- *Target and incumbent.* Step 1 of Proposition C7.1 also holds with a floor $J\le R$: in each case the pair receives $R$. So the pair's joint payoff is unchanged, and part 3 follows. $G>0$ above $\hat R^*$ by Lemma C7.2. $\square$

*Reason.* A second-price auction pays each entrant its marginal contribution to surplus when $R\ge p$. Better information for the challenger therefore weakly raises surplus. The bid reveals just enough to make the deterred challenger indifferent, so this information is worth zero at an interior threshold. At the corner, the cheapest bid ($J=p$) over-deters, and the challenger avoids entry that has negative expected value.

### Proposition C7.5 (anticipated preemption and informed trading; analytical)

Under the selected continuation, for any investor strategy and any flow $x$,

$$
\mathbb E[V_T\mid H,x]-P(x)=(1-\mu_x)S(\mu_x),\qquad \mathbb E[V_T\mid L,x]-P(x)=-\mu_xS(\mu_x)\le0.
$$

The proof of the paper's equation (11) carries over. $V_T$ depends on $\theta$ only through the auction, and the continuation at $x$ depends on $\mu_x$ only. So the low class never buys ($\beta_L=0$).

*(a) Spread.* Each type contributes its entry probability times its class gap in proceeds:

- silent type with entry $e$: gap $e(R-\ell)_+$;
- jumper: gap $\rho(R-\max\{J^*,\ell\})_+$.

Hence $S=\rho\Delta_T$ in Case A and $S=\Delta_T$ in Case B. In Case C,

$$
S(\mu)=\frac1r\Big[\int_0^{\hat R^*}(R-\ell)_+\,dR+\rho\int_{\hat R^*}^r(R-\max\{J^*,\ell\})_+\,dR\Big].
$$

*(b) Feedback neutralization.* If $\hat R^*\le\ell$, then $S(\mu)=\rho\Delta_T$. Silent types have $R<\ell$ and contribute nothing. Jumpers contribute $\rho(R-\ell)_+$. So the extra entry that good news recruits comes only from incumbents with $R<\ell$, where the class does not change proceeds. The investor's residual equals its value when entry is fixed at $\rho$.

*(c) Condition N.* If $B_r(1/2)<c_H$ and $M_1(h-(\ell+r)/2)\le c_H$, then every posterior in $[m_1,M_1]$ is in Case A or in Case C with $\hat R^*\le\ell$. Hence $S\equiv\rho\Delta_T$ at every posterior. The reason: $D_\mu(\ell)=\mu(h-(\ell+r)/2)$ rises in $\mu$, and $\hat R^*\le\ell$ if and only if $D_\mu(\ell)\le c_H$. At the benchmark ($c_H=5$, $b=2$), Condition N holds if and only if $r\ge r_N=2(h-c_H/M_1)-\ell=2.934693$. It holds at $r_1=3$: $M_1\cdot8\le5$ if and only if $e^{-1/2}\ge3/5$, that is $e\le25/9$.

*(d) Unique trading under Condition N.* With $\pi=1/2$, put $u=1/a-1$ and $v=1-a$. Then

$$
\Pi(\beta)=\rho\Delta_T\Big[\frac{M_1}{2+\beta u}+\frac{m_1}{2-\beta v}\Big]-k.
$$

*Derivation.* A purchase lands on a good flow ($x\ge1$) with probability $\Pr(Z\ge0)=M_1$ and on a bad flow ($x\le0$) with probability $m_1$. At strategy $\beta$ the good-flow likelihood ratio is $1+\beta u$ and the bad-flow ratio is $1-\beta v$. So $1-\mu_G=1/(2+\beta u)$ and $1-\mu_B=1/(2-\beta v)$.

$\Pi$ is strictly decreasing on $[0,1)$. Its derivative has the sign of $-a^{-2}(2+\beta u)^{-2}+(2-\beta v)^{-2}$, because $M_1u=a^{-2}m_1v$. Also $a(2+\beta u)=2a+\beta v\le2-\beta v$ if and only if $\beta\le1$. Hence the trading outcome is unique:

- full buying if $k\le2\rho m_1M_1\Delta_T$;
- no trade if $k\ge\rho\Delta_T/2$;
- the unique interior root otherwise.

This is the trading outcome of the economy where entry never responds to the price.

*(e) Global bound without Condition N.* In Case C with $\hat R^*>\ell$, $(r-J^*)^2-(\hat R^*-J^*)^2\ge(r-\hat R^*)^2$. Minimizing $x^2+\rho y^2$ subject to $x+y=r-\ell$ gives $S\ge\rho\Delta_T/(1+\rho)$. So $k<m_1\rho\Delta_T/(1+\rho)$ makes full buying the unique trading outcome at every $r$. The spread *can* fall below $\rho\Delta_T$: at $r=2.5$ the minimum ratio over a 401-point posterior grid is $0.928$, at $\mu=0.613$. A bid above $\ell$ raises what the incumbent pays to beat a low-class entrant.

*(f) Price reveals the posterior.* Suppose $B_r(1/2)<c_H$ and $\beta>0$. Then $P(\mu_G)>P(\mu_B)$. The bad-news posterior lies in Case A, where $P=t_0+\rho(t_L-t_0+\Delta_T\mu)$ rises strictly in $\mu$. In Cases B and C, each type's expected proceeds weakly exceed its Case A value. More entry raises proceeds, and so does a floor $J\ge p$. So the challenger and the incumbent both infer $\mu$ from the price.

### Proposition C7.6 (Proposition 2 survives, weakened; analytical, with benchmark values computer-assisted)

*General statement (analytical).* Assume the following:

- (i) $\Delta_T(r_0)<k$ and $B_{r_0}(1/2)<c_H$;
- (ii) $B_{r_1}(1/2)<c_H\le B_{r_1}(M_1)$, $M_1(h-r_1)<c_H$, and $k<m_1\rho\Delta_T(r_1)/(1+\rho)$;
- (iii) $B_{r_2}(M_1)<c_H$.

Then, in Model J:

1. at $r_0$, no trade is the unique trading outcome, and entry is $\rho$;
2. at $r_1$, full buying is the unique trading outcome, and good news triggers preemption by types above $\hat R^*(M_1)$;
3. at $r_1$, entry is $\rho+\frac{1-\rho}2\hat R^*/r_1>\rho$ and high-class ownership is $\frac12[\rho+(1-\rho)M_1\hat R^*/r_1]>\rho/2$;
4. at $r_2$, entry is $\rho$.

The outcomes in items 1 and 4 use the minimal-preemption selection. That selection binds at $r_0$ only if $c_H\le E_{1/2}\theta-p$, and at $r_2$ only if $c_H\le E_{M_1}\theta-p$.

*Proof.* Item 1: every residual is at most $\Delta_T(r_0)<k$, so the investor does not trade, and $\mu=1/2$ lies in Case A. Item 2: Proposition C7.5(e) gives a residual of at least $m_1\rho\Delta_T/(1+\rho)>k$ at every flow. The good-news posterior $M_1$ lies in Case C, and the bad-news posterior $m_1<1/2$ lies in Case A. Item 3 follows from Proposition C7.3, with $\Pr(\text{good})=1/2$ and $\Pr(\text{good}\mid H)=M_1$. Its inequalities hold because $\hat R^*\ge p>0$. Item 4: Case A at both posteriors. $\square$

*The mechanism cannot be fully undone.* Incumbents with $R<\hat R^*$, and in particular all with $R<p$, cannot credibly bid. Their silence invites the high-cost challenger.

*Benchmark ($c_H=5$; interval certificate in `c7_certify_output.txt`; 16 margins certified).*

- $c_H-M_1(h-(\ell+r_1)/2)=0.020325>0$, so Condition N holds.
- $D_{M_1}(p)-c_H=0.154167>0$, so the threshold is interior.
- $m_1\rho\Delta_T(r_1)-k=0.042923>0$.
- $\hat R^*=J^*=0.9359007391$.
- Entry: $0.366988$ (base model $0.625$). High-class ownership: $0.197820$ (base $0.358422$).
- Preemption probability: $0.344017$.
- $P_G-P_B=0.352007>0$.

With $c_H=5.05$ the knife-edge at $\mu=1/2$ disappears. Then $\hat R^*=0.786527$, and entry at $r_1$ is $0.348316$. At $r_2=3.6$ the threshold is at the corner ($\hat R^*=p$), and entry is $0.302083$.

### Proposition C7.7 (three-point model: preemption cannot affect trading; analytical)

*In the three-point model (equal noise, buy-only, $c_L=0$, $B_r(1/2)<c_H$), only the top flow can recruit the high-cost challenger. There $\mu=1$, and the investor's residual is $(1-1)S=0$. So Model J leaves the investor's payoff ($K_2-k=\rho\Delta_T/3-k$) and the trading outcome unchanged. At $\mu=1$, deterrence is feasible if and only if $h-r<c_H$. At the benchmark, $h-r_1=7>c_H\in\{5,6\}$, so no bid deters, and the jump option changes nothing.*

*Proof.* The top flow reveals $H$ under any $\beta>0$. Interior flows keep $\mu=1/2$, which is Case A. The bottom flow has $\mu\le1/2$. At $\mu=1$, $D_1(a)=h-(a+r)/2>h-r$ for all $a<r$. $\square$

When $c_H\in(h-r,\,g_H(r)]$, preemption at the top flow cuts entry there to $\rho+(1-\rho)\max\{p,2(h-c_H)-r\}/r$. It still leaves trading unchanged.

### Result C7.8 (preemption creates mixed equilibria at weak incumbents; analytical existence, numerical diagnostic location)

*Analytical part.* In Model J, $S(\mu)$ is continuous on $[m_1,M_1]$. The pieces fit as follows:

- Case A and the Case C corner both give $S=\rho\Delta_T$. Silent types with $R<p$ add no spread.
- $\hat R^*(\mu)$ and $J^*(\mu)$ are continuous within Case C.
- As $\mu\uparrow c_H/(h-r)$, $\hat R^*\to r$ and $S\to\Delta_T$, the Case B value.

So $\Pi(\beta)$ is continuous. Whenever $\Pi(0)<0<\Pi(1)$, there is an interior root $\beta^*$. Every such root has $\mu_G(\beta^*)$ in Case B or C, because in Case A, $\Pi(\beta)\le\Pi(0)<0$ by C7.5(d). In the paper's model (and the base discrete-Laplace model), entry jumps at $\tau$. Its $\Pi$ jumps there too, and an interior root at the jump needs challenger mixing (item C.9).

*Numerical part* (`c7_region_output.txt`, $r$ step $0.005$, $\beta$ grid $121$ points plus bisection). Rows marked `jump-through-zero` in the script outputs are sign changes across a discontinuity of $\Pi$. They are not equilibria under the pure challenger tie rule, and the table omits them.

| $r$ range | base model equilibria | Model J equilibria |
|---|---|---|
| $[1.430,1.440]$ | no trade; interior $\beta$ in Case B | no trade; interior $\beta\approx0.62$ in Case C; interior $\beta$ in Case B |
| $[1.445,1.745]$ | no trade; full buying | no trade; full buying; **interior $\beta\in[0.620,0.663]$, Case C, $\hat R^*>\ell$** |
| $[1.750,1.760]$ | interior (Case A); full buying | interior (Case A); interior (Case C); full buying |
| $[1.765,1.790]$ | full buying | two interior (Case C); full buying |
| $[1.795,4.61]$ | full buying unique | full buying unique |

Example at $r=1.6$: $\beta^*=0.652592$, $\mu_G=0.587348$, $\mu_B=0.426351$, $\hat R^*=1.374321$, $J^*=1.193272$, entry $0.544700$, ownership $0.298091$. Here good news triggers preemption with probability $0.064520$. Entry in the new equilibrium lies strictly between the no-trade ($0.25$) and the full-buying ($0.625$) values. It falls from $0.589$ to $0.495$ as $r$ rises over $[1.43,1.75]$.

### Result C7.9 (entry path in incumbent strength; analytical thresholds, numerical diagnostic path)

At the benchmark ($c_H=5$), three thresholds organize the full-buying branch:

- $r_D=h-c_H/M_1=1.967347$: below it, no bid can deter at $M_1$ (Case B). Model J and the base model coincide on the full-buying branch.
- $r_N=2.934693$: above it, Condition N holds.
- $r_C=3.986097$: here $B_r(M_1)=c_H$, which reproduces B1's information ceiling.

The good-news entry probability $\rho+(1-\rho)\hat R^*/r$ equals $1$ at $r_D$ and falls continuously in $r$. It reaches the corner value $\rho+(1-\rho)p/r$ at $r=3.485483$, where $D_{M_1}(p)=c_H$. At $r_C$ it drops to $\rho$.

*Analytical support.* $D_\mu(a)$ falls in $r$ (a first-order shift of $U[a,r]$) and falls in $a$. So $a^*$ falls in $r$, and so does $\hat R^*/r$. At a fixed posterior, entry is therefore non-increasing in $r$. This is the analog of Proposition A.3.

Selected values (full buying, sweep `c7_sweep.csv`):

| $r$ | 2.05 | 2.45 | 2.85 | 3.05 | 3.45 | 3.85 | 4.05 |
|---|---|---|---|---|---|---|---|
| entry, base | 0.625 | 0.625 | 0.625 | 0.625 | 0.625 | 0.625 | 0.25 |
| entry, Model J | 0.594761 | 0.477249 | 0.392723 | 0.359205 | 0.307662 | 0.298701 | 0.25 |
| preemption prob. | 0.0403 | 0.1970 | 0.3097 | 0.3544 | 0.4231 | 0.4351 | 0 |

The entry gain from information is thus largest at intermediate strength. There, the incumbent is strong enough to make the price informative but too weak to deter. A stronger incumbent raises the information in the price, and it also raises the power of its own response. The second force wins gradually above $r_D$.

### Result C7.10 (cross-check in the paper's Laplace model; numerical diagnostic)

The continuation of Proposition C7.3 applies posterior by posterior, so it also applies to the paper's model. I use the paper's benchmark at $r_1=3$ ($c_H=6$, $b=2$, full orders $(1,-1)$). Every belief gives a gross profit above $1$ there, so $c_L\in\{0,1\}$ makes no difference.

- Condition N holds: $M(h-(\ell+r)/2)=5.848<6$, with $M=0.731059$. So $S=\rho\Delta_T$ at every flow. The paper's bound (A3), $0.022412>k$, then keeps full orders unique.
- Entry falls from $0.522757$ (reproducing the paper's value) to $0.304840$.
- High-class ownership falls from $0.324192$ to $0.165056$.
- Near the threshold ($x\in[0.871,0.972)$) the bid sits at the corner $J^*=p$. That region adds surplus $0.000889$.

The weakening is therefore not an artifact of the discrete base.

## 4. What it recovers or loses relative to the Laplace paper

| Paper result | In Model J (discrete-Laplace base) |
|---|---|
| Prop. 1 (two returns) | Unchanged: auction primitives. The spread the investor trades on becomes $S(\mu)$, which equals $\rho\Delta_T$ under Condition N. |
| Prop. 2(i) | Survives (C7.6). The selection binds only at the knife-edge $c_H=5$. |
| Prop. 2(ii) | Survives, weaker: entry $0.25\to0.366988$ (base $0.625$); ownership $0.125\to0.197820$. Never fully undone. |
| Prop. 2(iii) | Survives above $r_C$ under the selection. The decline starts earlier and is gradual from $r_D$. |
| Blackwell remark | Survives: an informative versus an uninformative price. |
| Prop. 3 (coexistence) | The base model's no-trade/full-buying coexistence on $[1.443,1.748]$ survives. Model J adds an interior mixed equilibrium with partial preemption (C7.8). Coexistence is impossible under Condition N. |
| A.1 posterior bounds | Unchanged. |
| A.2 price sufficiency | Survives (C7.5(f)). |
| A.3 fixed-experiment deterrence | Survives: entry at a fixed posterior is non-increasing in $r$ (C7.9). |
| A.4 thresholds | No-trade boundary unchanged. Uniqueness bound becomes $k<m_1\rho\Delta_T/(1+\rho)$ (or $k<m_1\rho\Delta_T$ under N). The ceiling $r_C$ is unchanged, but entry falls before it. |
| A.5–A.7, A.8 | Not studied. |
| A.9 access to prices | Survives at $r_1$: the surplus gain is unchanged ($0.148310$); the proceeds gain halves ($0.327490\to0.155593$). |
| A.10 pooling | Not applicable ($c_L=0$ floor). |
| Endogenous trading asymmetry, feedback | Lost under Condition N: trading profit does not depend on the entry response (C7.5(b)). |
| §5, §6.2, §6.3 | Not studied. §6.1 as A.9. |

## 5. Numerical example

Benchmark $c_H=5$. Ex ante values. "Surplus" is acquisition surplus net of preparation costs. "Incumbent" and "challenger" are expected payoffs. Source: `c7_benchmark_output.txt`. The sum check (proceeds + incumbent + challenger = surplus) holds to $10^{-50}$.

| Economy | trading | entry | $\mathsf O_H$ | preempt | proceeds | incumbent | challenger | surplus |
|---|---|---|---|---|---|---|---|---|
| $r_0=1.2$, both models | none | 0.250000 | 0.125000 | 0 | 0.392708 | 0.155208 | 1.201042 | 1.748958 |
| $r_1=3$, base | full | 0.625000 | 0.358422 | 0 | 0.942073 | 0.568344 | 1.189977 | 2.700394 |
| $r_1=3$, Model J | full | 0.366988 | 0.197820 | 0.344017 | 0.770177 | 0.740240 | 1.189977 | 2.700394 |
| $r_1=3$, price hidden | full | 0.250000 | 0.125000 | 0 | 0.614583 | 0.864583 | 1.072917 | 2.552083 |
| $r_2=3.6$, base | full | 0.625000 | 0.358422 | 0 | 1.057873 | 0.750808 | 1.079386 | 2.888066 |
| $r_2=3.6$, Model J (corner) | full | 0.302083 | 0.157420 | 0.430556 | 0.690278 | 1.118403 | 1.091083 | 2.899764 |

At $r_1$, the move from the base model to Model J changes entry by $-0.258012$ and proceeds by $-0.171896$. The incumbent gains $0.171896$. The challenger and surplus change by $0$. At $r_2$, the corner adds $0.011698$ to both the challenger and surplus.

Trading at $r_1$: the purchase payoff net of $k$ is $0.175836$ in the base model and $0.058335$ in Model J, which equals $2\rho m_1M_1\Delta_T-k$. Prices under full buying: $P_G=0.946180$ (base $1.289973$) and $P_B=0.594173$.

Effect of the trading cost at $r_1$:

- If $k\in[0.083333,0.195836]$, the base model admits full buying, and no trade is also an equilibrium.
- In Model J, no trade is the unique outcome for $k\ge0.083333$, because $\rho\Delta_T/2=0.083333$. So anticipated preemption removes the informative equilibrium there.
- For $k\in(0.078335,0.083333)$, Model J has a unique interior $\beta$.

Reproduced B1 numbers: $r_C=3.986096572$. The coexistence interval bounds are $\mathfrak r(k/((1+\rho)m_1M_1))=1.443322$ and $\mathfrak r(2k/\rho)=1.747878$. The feedback values are $0.175836$ and $0.058335$.

## 6. Open issues

1. **Selection at Case A posteriors.** The reserve-bid equilibrium (every $R\ge p$ bids $p$; silence reveals $R<p$) exists when $E_\mu\theta-p\ge c_H$. It leaves trading unchanged and raises entry by $(1-\rho)p/r$ at those posteriors. At $c_H=5$ it exists at $\mu=1/2$ with equality, so the $r_0$ comparison relies on the selection there. At $c_H\in(5,5.312]$ it does not exist at $\mu=1/2$, but it does exist above $r_C$ at $M_1$.
2. **Belief rule.** The results use rule IC-P. Under D1 or the Intuitive Criterion alone, larger bids, and even silence pooling, survive. Such equilibria give more entry after good news. The lower entry reported here is the outcome of the least-cost bid.
3. **Bid before the price (brief option (c) timing).** A bid before trading cannot condition on news. It reveals $R$ to the market and so changes the spread. Not solved.
4. **Contracts that change the auction.** Toehold-like lockup options, break fees, and matching rights fall outside Proposition C7.1.
5. **Reading N with non-degenerate $G_j$.** Exact neutralization (C7.5(b)) uses the point mass at $\ell$. With a spread-out low class, silent types below $\ell$ would carry some class gap.
6. **Interactions.** Not studied: presence $\lambda<1$, two-sided orders (C.1), challenger mixing (C.9), and a public rejected offer in Model L.
7. **Status of C7.8 and C7.9.** The equilibrium sets and locations are numerical diagnostics on grids. They are not certified.
8. **Literature.** The paper cites Fishman (1988) only for the deterrence force at fixed information (Introduction, paragraph 1, with Hirshleifer and Png 1989). Its title, "A Theory of Preemptive Takeover Bidding", suggests a related signaling game. I did not read it. Any match between Model J and Fishman's model is **unverified**. Roberts and Sweeting (2013, *AER* 103(5)) is verified in `LIT_extracts.md` (B12). In their sequential mechanism, a jump bid reveals incumbent value through an inverse schedule and affects later entry. They use a D1-consistent restriction. That model has no stock market.

## 7. Plain summary

In the paper, the incumbent bidder does nothing when the target's price moves. This memo lets it answer the price with a binding early bid. I use the discrete-Laplace model because its beliefs stay away from certainty. A bid can deter a challenger only if the challenger is still unsure of its own value.

A private offer to buy the target at once never succeeds. The auction already pays the target the incumbent's value whenever the challenger wins. So the incumbent and the target gain nothing jointly by excluding the challenger. A rational board rejects every such offer.

A public early bid works differently. After good news, strong incumbents bid just enough to convince the high-cost challenger that the contest is not worth its cost. Weak incumbents cannot afford the bid. Their silence invites entry. At the benchmark, entry at the strong incumbent falls from 0.625 to 0.367, and high-value ownership falls from 0.358 to 0.198. Entry still rises from 0.25 at the weak incumbent, so the main result survives in a weaker form. The paper's own Laplace model shows the same pattern: entry falls from 0.523 to 0.305.

The early bid moves money from target shareholders to the incumbent. It leaves the challenger's payoff and total surplus unchanged, because the bid reveals just enough to make the deterred challenger indifferent. The investor sees this coming. Its profit from buying falls to what it would earn if entry never responded to the price. At the benchmark trading cost it still buys.

Two new patterns appear. First, the gain in entry from information is largest at intermediate incumbent strength and fades gradually as the incumbent becomes strong enough to deter. Second, at weak incumbents, preemption creates a new equilibrium with partial trading and partial preemption.
