# C5. An informed investor with a stake, in the discrete model (manipulation by buying)

Workstream C5, 21 October 2026. Scripts: `scripts/C5_stake/`. Their printed outputs are in `scripts/C5_stake/out/`.

## 1. Question

The informed investor owns $\omega\ge0$ units of the target before it learns the class $j\in\{H,L\}$.
Its payoff is

$$
\omega V_T+q\,\{V_T-P(X)\}-kq,\qquad X=q+Z,\quad q\in\{0,1\}.
$$

Entry of the second bidder raises $V_T$ in both states. So the investor may buy in class $L$ to push the price up and to recruit entry.
This is manipulation by buying. A real decision (preparation) responds to the price, and the investor profits from the response.

The brief asks five questions.

1. For which $\omega$ does the Proposition 2 analog survive? Give exact bounds.
2. When does the $L$ investor buy? Does the price pool? Does entry fall or rise?
3. Is there a stake that maximizes informative entry?
4. Does a stake create coexistence (a Proposition 3 analog) or a new type of equilibrium?
5. Who gains: target shareholders, the challenger, the investor?

## 2. Setup

### 2.1 Base models and what changes

- **Three-point model.** $Z\in\{-1,0,1\}$ with probability $1/3$ each. Buy-only orders. This model has an unused flow, so it needs a belief rule.
- **Discrete-Laplace model.** $P(Z=z)=\frac{1-a}{1+a}a^{|z|}$, $a=e^{-1/b}$, $b=2$. Buy-only orders. Every flow has positive probability, so no belief rule is needed.

Both models keep Reading N, $c_L=0$, prior $\pi=1/2$ and presence $\lambda=1$. Section 3.12 treats $\lambda<1$.
The only change is the stake. I use the two models for different reasons. The three-point model gives closed forms and a clean test of the off-path belief.
The discrete-Laplace model has informative flows everywhere, so the posterior moves with the investor's mix.

### 2.2 The stake

The stake $\omega$ is a known, fixed number of order units. It carries no control rights. Its purchase cost is sunk.
The stake pays $V_T$, the terminal proceeds per share. It does not pay the price $P$. An extra term $\omega P$ would count the same share twice (see Q3_stake, Result 9).

### 2.3 Equilibrium, belief rule and tie rules

- **Concept.** Perfect Bayesian equilibrium. Class $j$ buys with probability $\beta_j$. Market makers set $P(x)=\mathbb E[V_T\mid x]$. The challenger sees the price and its cost only.
  On the path, beliefs follow Bayes' rule. Since $c_L=0$, entry is at least $\rho$ at every belief, so the price reveals the market maker's posterior (Proposition A.2 argument).
- **Off-path flows.** Only the three-point model has them: flow $2$ under no trade, flow $-1$ under pooled buying.
  At such a flow the market maker holds a belief $\mu$. The price follows from the same pricing formula, and the challenger holds the same belief.
- **Belief rule (main text).** D1. At the unused top flow, class $L$ is deleted whenever class $H$ gains from every response that gives class $L$ a weak gain (Lemma 2(c) shows that this always holds). So $\mu=1$ whenever a purchase can pay for some belief.
  I also report the Intuitive Criterion (IC), the passive belief $1/2$ and the pessimistic belief ($\mu<\tau$).
- **Tie rules.** I state three systems.
  - **T0** (the prescribed rules of the discrete memos). An indifferent investor chooses zero. An indifferent challenger prepares. All investor orders are pure.
  - **T1** (the paper's own rules). The investor can mix, as in Section 2.4 of the paper. An indifferent challenger prepares.
  - **T2.** The investor and the challenger may both mix at indifference.

### 2.4 Notation

From the paper, at incumbent strength $r$: $t_0,t_H,t_L,g_H,g_L$, $\Delta_T=t_H-t_L$, $B_r(\mu)=g_L+\mu(g_H-g_L)$.
New symbols:

- $w_L=t_L-t_0$, $w_H=t_H-t_0=w_L+\Delta_T$.
- $\tau=(c_H-g_L)/(g_H-g_L)$: the belief at which the high-cost challenger is indifferent.
- $e(x)=\rho+(1-\rho)\phi(x)$: average entry after flow $x$. $\phi(x)\in[0,1]$ is the preparation probability of the high-cost challenger. It is $1$ if $\mu>\tau$, $0$ if $\mu<\tau$ and free if $\mu=\tau$.
- $R_H(x)=e(x)\Delta_T\{1-\mu(x)\}$, $R_L(x)=-e(x)\Delta_T\mu(x)$: the residuals $\mathbb E[V_T\mid j,x]-P(x)$.
- Regime (R): $\tfrac12<\tau\le1$, that is $B_r(1/2)<c_H\le g_H(r)$. In the three-point model, this is where a posterior of $1$ recruits the high-cost challenger and the prior does not.
- $\beta_{\max}=1/\tau-1$ (three-point model).
- Mixed branches. **S** $=(\beta_H,\beta_L)=(1,0)$. **NT** $=(0,0)$. **M** $=(1,\beta^*)$ with $0<\beta^*<\beta_{\max}$. **M′** $=(1,\beta_{\max})$ with a mixing challenger.

Benchmark: $(h,\ell,p,\rho,c_L,c_H,k)=(10,1,\tfrac12,\tfrac14,0,6,\tfrac1{50})$, $r_0=\tfrac65$, $r_1=3$. For the discrete-Laplace model, $c_H=5$ and $b=2$ (the brief's window).

| | $r_0=6/5$ | $r_1=3$ |
|---|---|---|
| $\Delta_T$ | $1/60$ | $2/3$ |
| $w_L,\ w_H$ | $19/48,\ 33/80$ | $11/24,\ 9/8$ |
| $\tau$ ($c_H=6$) | $195/308=0.6331$ | $141/200=0.7050$ |
| $\beta_{\max}$ | $113/195=0.5795$ | $59/141=0.4184$ |

## 3. Results

### 3.0 Results in brief

| Question | Three-point model | Discrete-Laplace model | Status |
|---|---|---|---|
| Q1: Prop. 2 analog | Holds iff $\omega<\omega_H(r_0)=268/1485=0.1805$. Strong economy unique to $152/75=2.027$ (T1, T2) or $2144/825=2.599$ (T0). Part (iii) holds for all $\omega$. | Holds iff $\omega<0.1878$ (T1, T2) or $\omega\le0.1993$ (T0). Strong economy unique to $3.4225$ or $3.5878$. Part (iii) holds for all $\omega$. | analytical; benchmark values computer-assisted |
| Q2: $L$ buys | Iff $\omega\ge 152/75$ (T1, T2), by mixing. Never in pure orders. Price never pools fully. Entry rises up to $0.4273$, then falls to $\rho$ as $\omega\to\infty$. | Same structure. $L$ buys iff $\omega\ge3.4225$. | analytical |
| Q3: best stake | Informative entry $\mathsf O_H-\rho/2$ is flat at its maximum on $[\omega_H,\Omega_1]$. Total entry peaks at $\omega=\Omega_2$. | Same. | analytical |
| Q4: coexistence | None at zero stake. Stake creates S–M–M′ coexistence. New types: M, M′. | Coexistence exists at zero stake for $1.443\le r\le1.748$. Stake extends it to $r_0$. Five equilibria at $\omega=9/25$. | analytical; computer-assisted |
| Q5: who gains | Shareholders gain from price access. Manipulation moves rent from the challenger to shareholders. Large stakes remove the gain. | Same signs. | computer-assisted (three-point); numerical diagnostic (discrete Laplace) |

### 3.1 Lemma 1: the stake term (analytical)

**Lemma 1.** In the three-point model, for any price and entry schedule, the net gain of class $j$ from order $1$ over order $0$ is

$$
G_j=\underbrace{\omega\,w_j\,\frac{e(2)-e(-1)}{3}}_{\text{stake term}}
+\underbrace{\frac13\sum_{x=0}^{2}R_j(x)}_{\text{trading term}}-k .
$$

*Proof.* Entry depends on the flow only through the price, and the cost is independent of the class.
So $\mathbb E[V_T\mid j,x]=t_0+e(x)w_j$. The competitive price is $P(x)=t_0+e(x)\{w_L+\Delta_T\mu(x)\}$.
Subtract: $\mathbb E[V_T\mid j,x]-P(x)=R_j(x)$. The payoff of class $j$ from order $q$ is

$$
U_j(q)=\omega\sum_z\tfrac13\{t_0+e(q+z)w_j\}+q\sum_z\tfrac13R_j(q+z)-kq .
$$

Order $1$ moves the flow support from $\{-1,0,1\}$ to $\{0,1,2\}$. The flows $0$ and $1$ stay. The stake term is $\omega w_j\{\bar e(1)-\bar e(0)\}$ with $\bar e(1)-\bar e(0)=\tfrac13\{e(2)-e(-1)\}$. The level $t_0$ cancels. $\square$

**Remarks.**
(a) The stake term does not contain $\Delta_T$. At $r_0$, $\Delta_T=1/60$ but $w_H=33/80$. So a small stake matters in the weak economy.
(b) The two classes differ in the stake term only through $w_H-w_L=\Delta_T$.

### 3.2 Lemma 2: structure of every equilibrium (analytical)

**Lemma 2.** Assume regime (R), $c_L=0$ and equal three-point noise. Every equilibrium, for every $\omega\ge0$, every tie system and every belief at an unused flow, satisfies:

- (a) $\beta_L\le\beta_H$.
- (b) $e(-1)=\rho$ and $e(2)\ge\rho$. Write $\epsilon=e(2)-\rho\ge0$.
- (c) $G_H-G_L=\dfrac{\Delta_T}{3}\{\omega\epsilon+2\rho+e(2)\}>0$.
- (d) If $\beta_L>0$ then $\beta_H=1$ and $G_L\ge0$.
- (e) Pooled buying $(\beta_H,\beta_L)=(1,1)$ is not an equilibrium for any $\omega$.

*Proof.* Flows $0$ and $1$ have equal probability in both classes, so $\mu(0)=\mu(1)=\tfrac12<\tau$ and $e(0)=e(1)=\rho$.
The floor $c_L=0<g_L$ gives $e\ge\rho$ at every belief.

(a) Suppose $\beta_L>\beta_H$. Flow $2$ is on the path with $\mu(2)=\beta_H/(\beta_H+\beta_L)<\tfrac12<\tau$. So $e(2)=\rho\le e(-1)$.
Then the stake term of class $L$ is at most zero. The trading term is negative. So $G_L<0$ and $\beta_L=0$. This contradicts $\beta_L>\beta_H\ge0$.

(b) By (a), $\mu(-1)=(1-\beta_H)/(2-\beta_H-\beta_L)\le\tfrac12<\tau$ when flow $-1$ is on the path. So $e(-1)=\rho$.

(c) Subtract the two expressions in Lemma 1. Use $w_H-w_L=\Delta_T$ and $R_H(x)-R_L(x)=e(x)\Delta_T$.

(d) $\beta_L>0$ needs $G_L\ge0$. By (c), $G_H>G_L\ge0$. So $\beta_H=1$.

(e) At $(1,1)$ the flows $0,1,2$ have posterior $\tfrac12$ and entry $\rho$. Flow $-1$ is unused, with $e(-1)\ge\rho$. So the stake term of class $L$ is at most zero. The trading term is $-\rho\Delta_T/2$. Then $G_L\le-\rho\Delta_T/2-k<0$, and class $L$ does not buy. $\square$

Lemma 2(e) is the discrete form of Q3_stake, Result 7 (pooled purchases fail for every stake).

### 3.3 Proposition 1: the equilibrium correspondence (analytical; benchmark values computer-assisted)

Define

$$
\omega_H=\frac{3k-\rho\Delta_T}{(1-\rho)w_H},\quad
\Omega_1=\frac{(1+\rho)\Delta_T+3k}{(1-\rho)w_L},\quad
\Omega_2=\frac{(\rho+\tau)\Delta_T+3k}{(1-\rho)w_L}.
$$

Since $\tau<1$ and $w_H>w_L$: $\omega_H<\Omega_2<\Omega_1$.

**Proposition 1.** Assume regime (R), $c_L=0$, equal three-point noise, buy-only orders, $\lambda=1$. Use T2 and D1. The equilibria are exactly these.

| Label | Profile | Exists iff |
|---|---|---|
| NT | $(0,0)$ | $\omega\le\omega_H$ |
| S | $(1,0)$ | $\max\{0,\omega_H\}\le\omega\le\Omega_1$ |
| Hm | $(\beta_H,0)$, $0<\beta_H<1$ | $\omega=\omega_H\ge0$ |
| M | $(1,\beta^*)$, $\beta^*=\dfrac{\Delta_T}{\omega w_L(1-\rho)-\rho\Delta_T-3k}-1$ | $\Omega_2\le\omega\le\Omega_1$ |
| M′ | $(1,\beta_{\max})$ with $e(2)=\dfrac{3k+\rho\Delta_T+\rho\omega w_L}{\omega w_L-\tau\Delta_T}$ | $\omega\ge\Omega_2$ |

Under T1, delete M′ except at $\omega=\Omega_2$ (there $e(2)=1$).
Under T0, keep NT for $\omega\le\omega_H$ and S for $\omega_H<\omega\le\Omega_1$. If $\omega_H<0$, S holds for $0\le\omega\le\Omega_1$ and NT never holds.
Under a passive belief ($\mu=\tfrac12<\tau$) at the unused flow, NT also holds for every $\omega$ whenever $\rho\Delta_T/2\le k$.

*Proof.* By Lemma 2, three cases cover all profiles.

*Case 1: $\beta_L=0$ and $\beta_H>0$.* Flow $2$ reveals $H$: $\mu(2)=1$, $e(2)=1$ because $g_H\ge c_H$. Then

$$
G_H=\tfrac13\{\omega w_H(1-\rho)+\rho\Delta_T\}-k,\qquad
G_L=\tfrac13\{\omega w_L(1-\rho)-(1+\rho)\Delta_T\}-k .
$$

Neither depends on $\beta_H$. $G_L\le0\iff\omega\le\Omega_1$. $G_H\ge0\iff\omega\ge\omega_H$. Full buying ($\beta_H=1$) needs $G_H\ge0$ (T0: $>0$). An interior $\beta_H$ needs $G_H=0$, that is $\omega=\omega_H$. This gives S and Hm.

*Case 2: no trade.* Flow $2$ is unused. For a response $(\mu,\phi)$ at flow $2$:
$G_H=\tfrac13\{\omega w_H(e(2)-\rho)+\rho\Delta_T+e(2)\Delta_T(1-\mu)\}-k$ and $G_L=\tfrac13\{\omega w_L(e(2)-\rho)-\rho\Delta_T-e(2)\Delta_T\mu\}-k$.
By Lemma 2(c), $G_H>G_L$ for every response. So every response that gives $L$ a weak gain gives $H$ a strict gain. D1 deletes class $L$ and sets $\mu=1$.
At $\mu=1$, $G_H$ equals the expression in Case 1. NT holds iff $\omega\le\omega_H$.

*Case 3: $\beta_L>0$.* Lemma 2(d): $\beta_H=1$. Then $\mu(2)=1/(1+\beta_L)$.
If $\beta_L>\beta_{\max}$, then $\mu(2)<\tau$, $e(2)=\rho$ and $G_L<0$. So $\beta_L\le\beta_{\max}$.
If $\beta_L<\beta_{\max}$, then $e(2)=1$ and

$$
G_L(\beta)=\tfrac13\Big\{\omega w_L(1-\rho)-\rho\Delta_T-\frac{\Delta_T}{1+\beta}\Big\}-k .
$$

$G_L$ strictly increases in $\beta$. Also $G_L(0)=0$ iff $\omega=\Omega_1$ and $G_L(\beta_{\max})=0$ iff $\omega=\Omega_2$ (use $1/(1+\beta_{\max})=\tau$).
So $G_L=0$ has a root $\beta^*\in(0,\beta_{\max})$ iff $\Omega_2<\omega<\Omega_1$. Solve $G_L=0$ for $\beta^*$.
If $\beta_L=\beta_{\max}$, then $\mu(2)=\tau$ and the high-cost challenger may mix. With $e(2)=\rho+(1-\rho)\phi$, the condition $G_L=0$ is $e(2)(\omega w_L-\tau\Delta_T)=3k+\rho\Delta_T+\rho\omega w_L$.
The solution lies in $[\rho,1]$ iff $\omega\ge\Omega_2$.
In all of Case 3, $G_H>G_L=0$, so $\beta_H=1$ is optimal. $\square$

**Check (computer-assisted).** `tp_enumerate.py` scans a rational grid of $(\beta_H,\beta_L)$ and recomputes every payoff from primitives. It finds exactly the equilibria of Proposition 1 at each stake it tests, at $r_0,\tfrac32,2,r_1,9$. It finds no reversed profile and no pooled profile.

### 3.4 Proposition 2: the Proposition 2 analog and its exact bounds (analytical; benchmark values computer-assisted) — Q1

**Proposition 2.** Let $r_0<r_1<r_2$ and suppose $\rho\Delta_T(r_0)/3<k<\rho\Delta_T(r_1)/3$, regime (R) at $r_0$ and $r_1$, and $g_H(r_2)<c_H$. Then:

- **(i) Weak economy.** For $0\le\omega<\omega_H(r_0)$, no trade is the unique equilibrium outcome, with entry $\rho$. At $\omega=\omega_H(r_0)$ it is unique under T0. For $\omega>\omega_H(r_0)$ the separating equilibrium S replaces it under D1, if $\omega\le\Omega_1(r_0)$. Uniqueness of no trade fails under every belief rule, because S exists.
- **(ii) Strong economy.** S is the unique equilibrium for $0\le\omega<\Omega_2(r_1)$ under T1 and T2. Under T0 it is the unique equilibrium for $0\le\omega\le\Omega_1(r_1)$. Entry is $\rho+(1-\rho)/6>\rho$.
- **(iii) Return.** At $r_2$ no belief recruits the high-cost challenger. Then S is the unique equilibrium for every $\omega$, with entry $\rho$.

So the three parts hold together iff $\omega<\omega_H(r_0)$ (iff $\omega\le\omega_H(r_0)$ under T0), when $\omega_H(r_0)<\Omega_2(r_1)$.

*Proof.* (i) and (ii) follow from Proposition 1 with the zero-stake cost conditions. For (ii), $\omega_H(r_1)<0$ because $\rho\Delta_T(r_1)/3>k$.
(iii) Entry is $\rho$ at every belief, so the stake term is zero for every deviation. Lemma 2(a),(c),(e) hold with $\epsilon=0$. Then $G_L<0$, so $\beta_L=0$.
With $\beta_L=0$ and $\beta_H>0$: $G_H=\rho\Delta_T/3-k>0$ since $\Delta_T$ rises in $r$. At no trade, any belief gives $G_H\ge\rho\Delta_T/3-k>0$, so no trade fails. $\square$

**Benchmark values (exact fractions).**

| Bound | Meaning | Value |
|---|---|---|
| $\omega_H(r_0)$ | first stake with a second outcome at $r_0$ | $268/1485=0.180471$ |
| $\Omega_2(r_0),\ \Omega_1(r_0)$ | $L$ buys in equilibrium; $L$ mimics S at $r_0$ | $27616/109725=0.251684$; $388/1425=0.272281$ |
| $\Omega_2(r_1)$ | uniqueness of S at $r_1$ (T1, T2) | $152/75=2.026667$ |
| $\Omega_1(r_1)$ | existence of S at $r_1$; uniqueness under T0 | $2144/825=2.598788$ |

The binding bound is $\omega_H(r_0)=0.1805$, in the weak economy. The Laplace memo found only sufficient bounds, $0.0114$ (strong economy) and $0.0431$ (weak economy). The discrete bounds are exact, because the payoffs are exact.

**Discrete-Laplace values** (Section 3.10): (i) $\omega<\omega^\star(r_0)=0.18780$ (T1, T2) or $\omega\le\omega_H(r_0)=0.19934$ (T0); (ii) $\omega<3.42247$ (T1, T2) or $\omega\le3.58780$ (T0); (iii) all $\omega$.

**Belief dependence at $r_0$ (three-point model).** The table lists the stakes at which no trade is an equilibrium (checked by `tp_enumerate.py`).

| Belief rule at flow $2$ | No trade is an equilibrium iff |
|---|---|
| D1 or directional ($\mu=1$) | $\omega\le0.1805$ |
| IC | $\omega\le0.1805$ or $\omega\ge\Omega_2(r_0)=0.2517$ (IC is silent when $L$ is not dominated) |
| passive $\tfrac12$ or pessimistic ($\mu<\tau$) | every $\omega$ |

The stake makes the unused flow valuable. A cheap purchase can recruit entry. A belief of $1$ at the unused flow then makes class $H$ deviate. This is a new role for the off-path belief. The Laplace memo has no such flow, and its no-trade claim for every stake (Q3_stake, Result 3) holds there. It holds in the discrete-Laplace model too.

### 3.5 Proposition 3: manipulation by buying (analytical) — Q2

**Proposition 3.** Under the assumptions of Proposition 1, with T1 or T2:

- **(a) When $L$ buys.** Class $L$ buys with positive probability in equilibrium iff $\omega\ge\Omega_2$. The probability is $\beta^*(\omega)$ in branch M. It falls from $\beta_{\max}$ at $\Omega_2$ to $0$ at $\Omega_1$. In branch M′ it is $\beta_{\max}$. Pure purchases by class $L$ never occur.
- **(b) The price.** The top-flow posterior is $1/(1+\beta)\in[\tau,1)$. The price never pools fully. The price experiment of M and M′ is a mean-preserving contraction of the experiment of S, so S Blackwell-dominates both.
- **(c) Entry.** Total entry and ownership are

$$
\mathsf E=\rho+\frac{(1+\beta)\{e(2)-\rho\}}{6},\qquad
\mathsf O_H=\frac{\rho}{2}+\frac{e(2)-\rho}{6}.
$$

 For S: $\mathsf E=\rho+\frac{1-\rho}{6}=\tfrac38$, $\mathsf O_H=\tfrac14$. For M: $\mathsf E=\rho+\frac{(1-\rho)(1+\beta^*)}{6}$ and $\mathsf O_H$ is as in S. The maximum over M is $\rho+\frac{1-\rho}{6\tau}=\tfrac{241}{564}=0.4273$, at $\omega=\Omega_2$. For M′: $\mathsf E-\rho=\dfrac{3k+\rho(1+\tau)\Delta_T}{6\tau(\omega w_L-\tau\Delta_T)}$.
- **(d) Payoffs.** In S, M and M′, class $L$ earns $\omega(t_0+\rho w_L)$. This is its payoff from not buying. Manipulation brings class $L$ no gain in equilibrium. Class $H$ gains from the camouflage.

*Proof.* (a) is Proposition 1, Case 3, and Lemma 2(e).
(b) In S the posteriors are $0,\tfrac12,1$ with probabilities $\tfrac16,\tfrac23,\tfrac16$. In M they are $0,\tfrac12,\tfrac1{1+\beta}$ with probabilities $\tfrac{1-\beta}6,\tfrac23,\tfrac{1+\beta}6$. Both have mean $\tfrac12$.
Move the mass $\beta/6$ from posterior $0$ and the mass $1/6$ from posterior $1$ to the posterior $1/(1+\beta)$. The mean of the moved mass is $\frac16$ on both sides. So M is a mean-preserving contraction of S.
(c) Class $H$ buys: flows $0,1,2$ with probability $\tfrac13$ and entry $\rho,\rho,e(2)$. So $\bar e_H=\rho+\{e(2)-\rho\}/3$. Class $L$: flows $-1,0,1$ w.p. $(1-\beta)/3,\tfrac13,\tfrac13$ and flow $2$ w.p. $\beta/3$. So $\bar e_L=\rho+\beta\{e(2)-\rho\}/3$. Average. Insert $e(2)$ from Proposition 1.
(d) $L$ is indifferent between buying and not buying. Not buying gives flows $-1,0,1$ with entry $\rho$. $\square$

**Reading.** The mimic's loss at the top flow falls as more class $L$ mimics, because the top-flow posterior falls. So $G_L$ rises with $\beta$. This complementarity makes M unstable under best-response dynamics (an informal remark, not proved). It also makes S and M coexist.
All the extra entry in M is entry in state $L$. It is fooled entry. The extra entrant is the high-cost challenger, who pays $c_H=6$ in a state where the gross profit is $g_L=0.125$.

### 3.6 Proposition 4: large stakes (analytical) — Q2, Q4

**Proposition 4.** Let $\omega>\Omega_1$ in regime (R) with $\omega_H\le0$ (the strong economy).

- **(a)** Under the paper's own rules (T1) no equilibrium exists. A fortiori none exists under T0.
- **(b)** Under T2 the unique equilibrium is M′. Its entry at the top flow satisfies $e(2)-\rho=\dfrac{3k+\rho(1+\tau)\Delta_T}{\omega w_L-\tau\Delta_T}\to0$ as $\omega\to\infty$, so $\mathsf E\to\rho$ and $\mathsf O_H\to\rho/2$.

*Proof.* For $\omega>\Omega_1$, $G_L(\beta)>G_L(0)>0$ on $[0,\beta_{\max})$. So S fails and M does not exist.
At $\beta=\beta_{\max}$ with $e(2)=1$, $G_L>0$ (because $\omega>\Omega_2$), so class $L$ wants a larger $\beta$. Above $\beta_{\max}$, $G_L<0$.
So the only candidate is M′ with $e(2)<1$, which needs a mixing challenger. Part (b) is the formula in Proposition 1. $\square$

This nonexistence is a documented failure of the paper's own tie rules. It has the same cause as in Q2_discrete_sell_only, Claim 11(e). An entry jump at a posterior that equals $\tau$ cannot be crossed without mixing.

In the weak economy, for $\omega>\Omega_1(r_0)$, the same holds under D1. Under a passive belief, no trade survives.

### 3.7 Proposition 5: strength and stake (analytical; shape numerical diagnostic)

The set where S exists in the $(r,\omega)$ plane is $\omega_H(r)\le\omega\le\Omega_1(r)$.

- $\omega_H(r)$ falls in $r$. The numerator $3k-\rho\Delta_T$ falls and $w_H=r/2-p+3p^2/(2r)$ rises for $r>\sqrt3p$. It is zero at $r_T=\mathfrak r(3k/\rho)=1.9732$, the zero-stake cutoff.
- As $r\to\ell$, $\Delta_T\to0$ and $w_H(\ell)=w_L(\ell)$. All three thresholds tend to $3k/\{(1-\rho)w(\ell)\}=16/75=0.2133$.
- $\Omega_1(r)$ rises on the grid (numerical diagnostic, `tp_phase.py`).

So the stake lets trading start at any strength above $\ell$, but only inside a wedge that is narrow near $\ell$. The onset $r^*(\omega)$ is V-shaped.

| $\omega$ | 0 | 0.10 | 0.18 | 0.21 | 0.22 | 0.50 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|
| lowest $r$ with S | 1.973 | 1.518 | 1.202 | 1.036 | 1.076 | 1.475 | 1.898 | 2.605 |

For $\omega>16/75$ and $r$ below the onset, class $L$ mimics S. Only M′ exists, so T0 and T1 give no equilibrium. Above the onset, S exists up to $r_C$.
This changes the paper's comparison. At fixed $\omega$, the weak-to-strong contrast needs $r_0$ below the onset and $r_1$ above it.

### 3.8 Proposition 6: informative entry (analytical) — Q3

Define informative entry $\mathsf I=\mathsf O_H-\rho/2=\tfrac12(\bar e_H-\rho)$, extra preparation in state $H$. Define fooled entry $\mathsf F=\tfrac12(\bar e_L-\rho)$. Then $\mathsf E-\rho=\mathsf I+\mathsf F$.
Class $H$ reaches flow $2$ with probability $\beta_H/3$. So $\mathsf I=\beta_H\{e(2)-\rho\}/6$. This equals $\{e(2)-\rho\}/6$ when $\beta_H=1$.

**Proposition 6.** In regime (R):

- No equilibrium has $\mathsf I>(1-\rho)/6$. Equality holds iff $e(2)=1$: in S and in M.
- At fixed $r$, the largest $\mathsf I$ over all equilibria is flat on $[\max\{0,\omega_H\},\Omega_1]$ and falls for $\omega>\Omega_1$. In the strong economy the plateau starts at $\omega=0$, so no stake adds informative entry. In the weak economy, $\mathsf I=0$ for $\omega<\omega_H(r_0)$ and $\mathsf I=0.125$ on $(\omega_H(r_0),\Omega_1(r_0)]$. The stake doubles $\mathsf O_H$ from $0.125$ to $0.25$.
- Total entry $\mathsf E$ is maximal at $\omega=\Omega_2(r)$ in M, at $\rho+\frac{1-\rho}{6\tau}$. At $r_1$ this is $0.4273$ against $0.375$. At $r_0$ it is $0.4474$.

*Proof.* $\mathsf I=\beta_H\{e(2)-\rho\}/6\le(1-\rho)/6$, with equality iff $\beta_H=1$ and $e(2)=1$. The rest follows from the formulas in Propositions 1 and 3. $\square$

So there is no interior optimum for informative entry. The plateau is the answer. For total entry, the optimum is a kink at $\Omega_2$. It depends on selecting M among the coexisting equilibria, and it consists of fooled entry.

### 3.9 Coexistence and new equilibrium types (analytical; computer-assisted) — Q4

- **Three-point model, zero stake.** There is one equilibrium at each $r$, except at the knife edge $\rho\Delta_T/3=k$ (Q2_discrete_sell_only, Claim 5). The stake creates two kinds of coexistence.
  - **Strong economy.** For $\omega\in[\Omega_2,\Omega_1]$: S, M and M′. At $r_1$: $[2.027,2.599]$.
  - **Weak economy.** For $\omega\in(\omega_H,\Omega_1(r_0)]$: S coexists with no trade under any belief below $\tau$. Under D1, no trade fails.
- **New equilibrium types.** M (partial manipulation) and M′ (manipulation with a mixing challenger). Neither exists at zero stake.
- **Discrete-Laplace model, zero stake.** Coexistence already exists. No trade and S coexist iff $\Delta_T(r)\in[k/\{g_0g_1(1+\rho)\},\,2k/\rho]$, that is $r\in[1.4433,\,1.7479]$ (analytical endpoints, from $G_H^S=0$ and $\rho\Delta_T/2=k$; the upper end is the paper's $r_N=1.747878$, `dl_misc.py`). A third equilibrium with a mixing challenger exists there (numerical diagnostic, step $0.05$ in $r$, `dl_zero_stake_scan.py`). The memo B_dlaplace_numeric reports the same window, $[1.443322,\,1.747878]$, and the same entry $0.625$ and ownership $0.358422$ for S at $r_1$.
- **Discrete-Laplace model, with a stake.** The stake extends coexistence to the weak economy $r_0=1.2$. At $\omega=9/25$ five equilibria exist: NT, S, M, M′ and a high-type mixing equilibrium Hth. Interval arithmetic certifies each one. In all, `dl_certify.py` runs 32 sign tests at five stakes, all certified, and one bound that holds for every stake above $\omega^\star$ (Section 3.10).

The mechanism differs from Proposition 3. Proposition 3 comes from the feedback of entry on the investor's own information profit. Here the stake term and the mimic's falling loss create the multiplicity.

### 3.10 The discrete-Laplace model

**Lemma DL1: reduction (analytical).** With buy-only orders, $f_j(x)=\beta_jn(x-1)+(1-\beta_j)n(x)$. For $x\ge1$, $f_j(x)=\frac{1-a}{1+a}a^{x-1}\{\beta_j+(1-\beta_j)a\}$. For $x\le0$, $f_j(x)=\frac{1-a}{1+a}a^{-x}\{\beta_ja+1-\beta_j\}$.
So all flows $x\ge1$ ("good news") share one posterior $M$, and all flows $x\le0$ share one posterior $m$, for every $(\beta_H,\beta_L)$. With $g_0=\frac a{1+a}$, $g_1=\frac1{1+a}$, $\delta=\frac{1-a}{1+a}=g_1-g_0$:

$$
\Pr(X\ge1\mid j)=g_j:=g_0+\delta\beta_j,\qquad
M=\frac{g_H}{g_H+g_L},\qquad m=\frac{1-g_H}{2-g_H-g_L}.
$$

A buyer reaches good news with probability $g_1$, a non-buyer with probability $g_0$. A script check by direct summation over $241$ flows confirms the two-value posterior to $10^{-60}$ (`dl_thresholds.py`).

**Lemma DL2: gains.** Let $e_G,e_B$ be entry at good and bad news. Then

$$
G_j=\omega w_j\delta(e_G-e_B)+\text{(trading term)}-k,
$$

$$
G_H^{\rm trade}=\Delta_T\{g_1e_G(1-M)+g_0e_B(1-m)\},\qquad
G_L^{\rm trade}=-\Delta_T\{g_1e_GM+g_0e_Bm\}.
$$

**Lemma DL3: structure (analytical).** The proof of Lemma 2 carries over. Every equilibrium has $\beta_L\le\beta_H$ and $e_B=\rho$. $G_H-G_L=\Delta_T\{\delta\omega\epsilon+g_1e_G+g_0\rho\}>0$. If $\beta_L>0$ then $\beta_H=1$. Pooled buying fails. A script scan on a $41\times41$ grid shows no violation.

**Proposition 7 (analytical).**

(a) *No trade.* It is an equilibrium for every $\omega$ iff $\rho\Delta_T/2\le k$. Against it the entry schedule is constant, so the stake term is zero, and $G_H=\rho\Delta_T/2-k$, $G_L=-\rho\Delta_T/2-k$. No flow is unused. There is no belief rule.

(b) *Line $\beta_H=1$ (class $L$ mixes).* With $e_G=1$:
$M=\frac{g_1}{1+\delta\beta}$, $m=\frac{g_0}{1-\delta\beta}$ and

$$
G_L(\beta)=\omega w_L\delta(1-\rho)-\Delta_T\Big\{\frac{g_1^2}{1+\delta\beta}+\frac{\rho g_0^2}{1-\delta\beta}\Big\}-k .
$$

The braces fall in $\beta$. Their derivative has the sign of $\sqrt\rho\,g_0(1+\delta\beta)-g_1(1-\delta\beta)$. This difference rises in $\beta$. At $\beta=1$ it equals $2g_0g_1(\sqrt\rho-1)<0$. So it is negative on $[0,1]$, and $G_L$ rises in $\beta$. Define $\beta_{\max}=(g_1/\tau-1)/\delta$ and the thresholds

$$
\Omega_1=\frac{\Delta_T(g_1^2+\rho g_0^2)+k}{(1-\rho)\delta w_L},\qquad
\Omega_2=\frac{\Delta_T\{g_1\tau+\rho g_0m_{\max}\}+k}{(1-\rho)\delta w_L},\quad m_{\max}=\frac{g_0}{2-g_1/\tau}.
$$

The branches M and M′ exist iff $\Omega_2\le\omega\le\Omega_1$ and $\omega\ge\Omega_2$, as in Proposition 1.

(c) *Line $\beta_L=0$ (class $H$ mixes).* Let $u=\delta\beta_H$. Then

$$
G_H(\beta_H)=\omega w_H\delta(e_G-\rho)+\Delta_Tg_0g_1\Big\{\frac{e_G}{2g_0+u}+\frac{\rho}{2g_1-u}\Big\}-k .
$$

Inside each entry regime, $G_H$ is non-increasing in $\beta_H$, because $2g_1-u\ge1\ge2g_0+u$ and $e_G\ge\rho$. At $\beta^\star$, where $M=\tau$ (that is $u^\star=g_0(2\tau-1)/(1-\tau)$), $G_H$ jumps up. So the equilibria on this line are: NT; S; an interior mix in regime II (T1, T2); and a threshold mix Hth at $\beta^\star$ with a mixing challenger (T2).
For Hth, $G_H(\beta^\star)=0$ gives

$$
\phi=\frac{k-K_I}{(1-\rho)\{\omega w_H\delta+\Delta_Tg_0g_1/(2g_0+u^\star)\}},\qquad
K_I=\Delta_Tg_0g_1\rho\Big\{\frac1{2g_0+u^\star}+\frac1{2g_1-u^\star}\Big\}.
$$

Hth needs three conditions.

- $K_I<k$, so that $\phi>0$.
- $\phi\le1$, which means $\omega\ge\omega^\star$.
- Class $L$ does not gain at the profile.

For the third condition, write the gain of class $L$ as $\omega w_L\delta(1-\rho)\phi-\Delta_T\{g_1(\rho+(1-\rho)\phi)\tau+g_0\rho m^\star\}-k$. The first term equals $\omega w_L\delta(k-K_I)/\{\omega w_H\delta+\Delta_Tg_0g_1/(2g_0+u^\star)\}$. It rises in $\omega$ and tends to $(w_L/w_H)(k-K_I)$. The $\phi$ part of the trading term is at most zero. So the gain of class $L$ is at most $U=(w_L/w_H)(k-K_I)-\Delta_T\rho(g_1\tau+g_0m^\star)-k$ for every $\omega$. At the weak benchmark, interval arithmetic gives $k-K_I=0.01795>0$ and $U=-0.00489<0$. So Hth exists for every $\omega\ge\omega^\star$ at $r_0$. At $r_1$, $K_I>k$, so Hth does not exist.

Also $\omega_H=\{k-g_0g_1(1+\rho)\Delta_T\}/\{(1-\rho)\delta w_H\}$.

**Proposition 8: benchmark classification (computer-assisted; interval-certified at the stated stakes).**

| | $r_0=6/5$ | $r_1=3$ |
|---|---|---|
| $\tau$ ($c_H=5$) | $1125/2156=0.5218$ | $117/200=0.585$ |
| $M_1=g_1$ | $0.62246$ | $0.62246$ |
| $\beta_{\max}$ | $0.78764$ | $0.26145$ |
| $\omega^\star$ | $0.187802$ | $<0$ |
| $\omega_H$ | $0.199337$ | $<0$ |
| $\Omega_2$ | $0.359635$ | $3.422471$ |
| $\Omega_1$ | $0.372045$ | $3.587802$ |
| no trade for every $\omega$ | yes ($\rho\Delta_T/2=\tfrac1{480}<k$) | no |

Equilibria under T2:

- At $r_0$: $[0,\omega^\star)$: NT. $(\omega^\star,\omega_H)$: NT, Hm, Hth. $[\omega_H,\Omega_2)$: NT, S, Hth. $[\Omega_2,\Omega_1]$: NT, S, Hth, M, M′. $(\Omega_1,\infty)$: NT, Hth, M′.
- At $r_1$: $[0,\Omega_2)$: S. $[\Omega_2,\Omega_1]$: S, M, M′. $(\Omega_1,\infty)$: M′.
- At $r=4$ ($B_r(M_1)=4.996<c_H$): S alone, entry $\rho$, for every $\omega$.

Entry at $r_1$: S has $\mathsf E=0.625$, $\mathsf O_H=0.3584$. M at $\omega=3.5$: $\mathsf E=0.6373$. M′ at $\omega=\Omega_2$: $\mathsf E=\rho+\frac{(1-\rho)g_1}{2\tau}=0.6490$. M′ at $\omega=5,20,100$: $\mathsf E=0.427,\ 0.278,\ 0.255$.

### 3.11 Who gains (computer-assisted for the three-point model; numerical diagnostic for the discrete-Laplace rows) — Q5

The ledger uses one rule. Market makers earn zero. The investor's gross trading profit is the noise traders' loss. The cost $k$ is a resource cost. The total surplus is the winner's value less preparation costs less $k$. A cross-check from auction primitives agrees to $10^{-16}$ in every row (`welfare.py`).

Three-point model at $r_1=3$, per share:

| Equilibrium | $\mathsf E$ | $\mathsf O_H$ | Target proceeds $T$ | Challenger net profit | Incumbent profit | Noise-trader loss | Total surplus |
|---|---|---|---|---|---|---|---|
| hidden price (entry $\rho$) | 0.2500 | 0.1250 | 0.6146 | 1.0729 | 0.8646 | 0.0278 | 2.5421 |
| S | 0.3750 | 0.2500 | 0.7552 | 1.3802 | 0.7344 | 0.0278 | 2.8598 |
| M at $\Omega_2$ | 0.4273 | 0.2500 | 0.7792 | 1.0729 | 0.7148 | 0.0162 | 2.5527 |
| M′, $\omega=3$ | 0.3399 | 0.1884 | 0.6980 | 1.0729 | 0.7886 | 0.0162 | 2.5454 |
| M′, $\omega=10$ | 0.2698 | 0.1389 | 0.6329 | 1.0729 | 0.8479 | 0.0162 | 2.5395 |

- **Target shareholders.** Price access raises proceeds from $0.6146$ to $0.7552$ in S. Manipulation adds $0.024$ at $\Omega_2$. For $\omega>\Omega_1$ the gain shrinks toward zero.
- **Challenger.** It gains $0.3073$ from price access in S. In M and M′ it gains nothing, because the high-cost type is indifferent at the top flow (posterior $\tau$). Manipulation moves the whole rent from the challenger to shareholders.
- **Incumbent.** It loses from every entry.
- **Investor.** Class $L$ earns $\omega(t_0+\rho w_L)$ in S, M and M′. Class $H$ nets $0.0356$ in S and $0.1011$ in M at $\Omega_2$, a camouflage gain. The ex-ante trading profit of the investor falls from $0.0178$ in S to $0.0020$ in M. The stake gain from the price channel is $\omega(T-T_{\rm hidden})$: $0.1406\,\omega$ in S, $0.1646\,\omega$ in M at $\Omega_2$.
- **Noise traders.** They lose less in M, because class $L$'s trading loss is a transfer to them.
- **Total surplus.** Manipulation destroys most of the social value of price information: $2.8598\to2.5527$. Fooled entry in state $L$ costs $c_H=6$ for an allocation gain of about $0.21$.

Discrete-Laplace model at $r_1$: hidden price $T=0.6146$. S has $T=0.9421$, challenger profit $1.1900$, surplus $2.6904$. M at $\omega=3.5$ has $T=0.9477$, challenger profit $1.1301$, surplus $2.6302$. M′ has challenger profit $1.0729$ (the hidden-price level) and surplus $2.5708$ at $\omega=3.5$, falling to $2.5399$ at $\omega=100$.

### 3.12 Presence probability (analytical; computer-assisted check)

With presence $\lambda<1$, a present investor faces the same conditional flow probabilities of the flows that its order reaches. The posteriors at flows $0,1,2$ are unchanged. The bottom flow has posterior $(1-\lambda)/(2-\lambda)<\tau$ under S, so $e(-1)=\rho$. So $G_H$ and $G_L$ do not depend on $\lambda$, and all thresholds are unchanged. Entry scales: $\mathsf E=\rho+\lambda(1+\beta)\{e(2)-\rho\}/6$. `tp_presence.py` confirms this to ten digits at $\lambda=1,\tfrac45,\tfrac12,\tfrac1{10}$.

## 4. What it recovers or loses relative to the Laplace paper

| Paper item | Under a stake in the discrete models |
|---|---|
| Prop. 1, eqs. (4)–(6) | Unchanged. |
| Eqs. (7)–(8), Prop. A.1 | Not applicable. Posteriors are $0,\tfrac12,1$ (three-point) or $m(\beta),M(\beta)$ (discrete Laplace). |
| Prop. A.2, price sufficiency | Survives. $c_L=0$ gives the floor. |
| Eq. (11), residual advantage | Unchanged as a trading residual. The stake adds a separate term (Lemma 1). |
| Prop. 2 (i)–(iii) | The analog holds iff $\omega<\omega_H(r_0)$: $0.1805$ (three-point), $0.1878$ (discrete Laplace). Part (iii) survives every stake. The bounds are exact. |
| Eq. (12), entry and ownership | Unchanged in S. Changed in M and M′ (Proposition 3). |
| Prop. 3, coexistence | Three-point model: created by the stake. Discrete Laplace: present at zero stake and extended by the stake. |
| Prop. A.3, fixed experiment | Unchanged. It concerns the challenger only. |
| Prop. A.4, thresholds | The no-trade cutoff becomes the V-shaped onset $r^*(\omega)$. The ceiling $r_C$ is unchanged. |
| Section 6.1, price access | Price access raises proceeds in S. Manipulation moves the challenger's rent to shareholders. Large stakes remove the gain. |
| Sections 5.1–5.3, 6.2, 6.3 | Not studied. |

**Comparison with the Laplace stake memo (Q3_stake).**

| Q3_stake (Laplace) | This memo (discrete) |
|---|---|
| Unique full orders for $\omega<\Omega_U=0.0114$ (sufficient) | Exact: $\omega<152/75$ in the strong economy. The weak economy binds at $268/1485$. |
| No trade at $r_0$ for every $\omega$ (existence) | Holds in discrete Laplace. In the three-point model it needs a belief below $\tau$ at the unused flow. |
| Full orders exist to $\Omega_F=2.158$; pure partial-sale branch to $2.499$ | S to $\Omega_1=2.599$. A partial-buy branch M on $[2.027,2.599]$. |
| Pooled purchases fail | Same (Lemma 2(e), DL3). |
| Large stakes: open. (S23) excludes nondecreasing entry | Solved in the discrete model: M′ exists for all $\omega$ if the challenger mixes at the plateau. The Laplace statement (S23) may depend on the tie rule. This is a conjecture for the Laplace model. |
| Stake term bounded by worst-case derivative | Exact: $\omega w_j\{e(2)-e(-1)\}/3$, free of $\Delta_T$. |

**Comparison with Q2_discrete_sell_only, Claim 14, and SYNTHESIS, Part A.2, item 6.**

- The numbers $1.9491$ ($c_L=1$) and $2.5988$ ($c_L=0$) are the fixed-schedule threshold $\Omega_1$. I reproduce $2.5988=2144/825$. With $c_L=1$, $e(-1)=0$, so the factor $(1-\rho)$ in $\Omega_1$ becomes $1$, which gives $1.9491$.
- The claim "a low-value holder buys only if $\omega>\Omega_1$" is incomplete. Class $L$ buys in equilibrium from $\Omega_2=2.027$, by mixing. The first buyers appear before the separating profile fails.
- The claim "Claim 2 survives" is true for sales by class $H$. The mirror claim for purchases by class $L$ fails with a stake.
- The memo omits two effects. The stake also makes class $H$ buy in the weak economy (at $\omega_H$), and no equilibrium exists beyond $\Omega_1$ under the paper's tie rules.
- SYNTHESIS A.2 item 6 says that full selling does not survive at equality of its stake bound, because the tying trader must choose zero. For buy-only orders the tying type is class $L$, whose prescribed action is zero. So S survives at $\omega=\Omega_1$ under T0. `tp_enumerate.py` shows `strict=True` at $2144/825$.
- Sell-only orders are far less robust to a stake than buy-only orders (threshold $0.31$ against $2.60$ at $c_L=0$). For class $H$, the stake and the trade point the same way when it buys.

## 5. Numerical example

All values use the benchmark of Section 2.4. The three-point model uses exact fractions. The discrete-Laplace model uses 60-digit arithmetic, and interval arithmetic for the sign tests.

**Three-point model, equilibria and outcomes** (T2, D1).

| $r$ | $\omega$ | equilibria | $\mathsf E$ | $\mathsf O_H$ |
|---|---|---|---|---|
| $6/5$ | $0.10$ | NT | 0.2500 | 0.1250 |
| $6/5$ | $0.1815$ | S | 0.3750 | 0.2500 |
| $6/5$ | $0.2517=\Omega_2$ | S; M, M′ (coincide) | 0.3750; 0.4474 | 0.2500 |
| $6/5$ | $1$ | M′ only | 0.2956 | 0.1539 |
| $3$ | $0$ and $1$ | S | 0.3750 | 0.2500 |
| $3$ | $2.0267=\Omega_2$ | S; M=M′ | 0.3750; 0.4273 | 0.2500 |
| $3$ | $2.3$ | S; M ($\beta^*=0.1821$); M′ ($e(2)=0.839$) | 0.3750; 0.3978; 0.3893 | 0.2500; 0.2500; 0.2232 |
| $3$ | $2.5988=\Omega_1$ | S; M′ | 0.3750; 0.3628 | 0.2500; 0.2045 |
| $3$ | $3$ | M′ | 0.3399 | 0.1884 |
| $3$ | $5,\ 10,\ 100$ | M′ | 0.2947; 0.2698; 0.2518 | 0.1565; 0.1389; 0.1263 |
| $9$ | $0,\ 1,\ 1000$ | S | 0.2500 | 0.1250 |

Interior roots of branch M at $r_1$: $\beta^*(\omega)=0.346,\ 0.259,\ 0.182,\ 0.114,\ 0.054$ at $\omega=2.1,\ 2.2,\ 2.3,\ 2.4,\ 2.5$.

**Thresholds by strength (three-point model).**

| $r$ | 1.01 | 1.2 | 1.5 | 1.75 | 2 | 3 | 4 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|
| $\omega_H$ | 0.2126 | 0.1805 | 0.1044 | 0.0449 | $\le0$ | $\le0$ | $\le0$ | $\le0$ | $\le0$ |
| $\Omega_2$ | 0.2128 | 0.2517 | 0.4306 | 0.6389 | 0.8795 | 2.0267 | 3.3707 | 6.5927 | 8.5215 |
| $\Omega_1$ | 0.2129 | 0.2723 | 0.5253 | 0.8117 | 1.1352 | 2.5988 | 4.1707 | 7.4133 | 9.0548 |

**Commands** (repository root; each runs in seconds unless noted).

- `.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/tp_thresholds.py`: exact thresholds.
- `.../tp_enumerate.py`: brute-force enumeration with exact fractions (about nine seconds; run through the slot wrapper).
- `.../tp_phase.py`, `.../tp_presence.py`: strength map and presence check.
- `.../dl_thresholds.py`, `.../dl_enumerate.py`, `.../dl_five.py`, `.../dl_zero_stake_scan.py`: discrete-Laplace thresholds, equilibria and scans.
- `.../dl_certify.py`: 32 interval-arithmetic sign tests at five stakes, all certified, and one bound for all stakes above $\omega^\star$.
- `.../welfare.py`: ledger of Section 3.11.

I ran all of them through the command line on 21 October 2026 and read the printed output. No script contains an assertion. No test file, fixture or test suite exists.

## 6. Open issues

1. **Private stakes.** With a private stake drawn from a distribution, class $L$ would use a pure threshold rule. The map from the mass of buyers to the hurdle has the same discontinuity at $\beta_{\max}$, so mixing by the challenger may still be needed. Not studied. **Open.**
2. **Mixing challenger.** M′ rests on a challenger who mixes at one plateau value. An atomless cost distribution would smooth this. **Conjecture:** the equilibrium is then unique and continuous in $\omega$.
3. **Laplace plateau.** The same device may remove the Laplace nonexistence for large stakes. **Conjecture.**
4. **Belief rule.** I apply D1 to a composite receiver (market maker and challenger) with a common belief. Another completion could change the three-point results at $r_0$. The discrete-Laplace results do not depend on it.
5. **Selection.** The model gives no reason to select among S, M and M′. I expect M to be unstable under best-response dynamics, but I did not prove it.
6. **Other noise.** Unequal three-point noise (C9) and general priors are not studied here. The thresholds would change.
7. **Two-sided orders and dynamics.** A stake with two-sided orders (C1), two rounds (C2) or delay (C3) may raise manipulation incentives. Not studied.
8. **Endogenous stake.** The investor could buy the stake before learning the class. Not studied.
9. **Discrete-Laplace coverage.** The enumerator lists equilibria for the stakes it tests. The monotonicity proofs cover the whole range, but the interval certificates cover specific rational stakes only. The zero-stake third equilibrium is a numerical diagnostic on a grid of $0.05$.
10. **Scale.** Large $\omega$ is large in order units. It is not a share of outstanding equity.

## 7. Plain summary

An investor who owns shares gains when a second bidder enters. This is a new motive to trade. It does not depend on how strong the incumbent is.

In the three-point model I solved every equilibrium. A small stake ends the paper's weak-economy result first. Above $0.18$ order units, the informed investor buys even when trading costs more than the information pays. The stake substitutes for incumbent strength. The strong-economy result survives up to $2.03$ units, so the weak economy is the binding limit.

In the strong economy, an investor with bad news buys from $2.03$ units, but only with some probability. The price then keeps part of its information but never pools fully. Total entry rises by up to a seventh, all of it in the wrong state. Informative entry does not rise at all. The extra entry moves the challenger's rent to the target's shareholders and destroys most of the social value of price information.

In the strong economy, above $2.6$ units, no equilibrium exists under the paper's tie rules. One exists if the challenger may mix at one posterior. Entry then falls to the floor as the stake grows.

Both types buying the same amount is never an equilibrium.

The stake creates coexistence in the three-point model. In the discrete-Laplace model, coexistence already exists at zero stake. The stake extends it to the weak economy. At $\omega=0.36$ it gives five equilibria.

The earlier claim that an investor with bad news buys only above $2.6$ units is incomplete. The first buyers appear at $2.03$.
