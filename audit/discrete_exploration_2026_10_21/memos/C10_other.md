# C10. Other modifications: target disclosure and a toehold

Workstream C10, 21 October 2026. Scripts: `scripts/C10_other/`. Paper source: commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` only.

## 1. Question

Item C.10 asks for modifications of the discrete model that can recover or create results. This memo studies two of them.

- **(b) Target disclosure.** The target commits to a public test of challenger fit before trading starts.
  - Does the test crowd out the investor's information and the trading incentive?
  - Does the target want to disclose more against a stronger incumbent?
- **(a) A toehold.** The challenger holds or buys target shares before it prepares.
  - Does a toehold change the price-to-entry channel?
  - Does the challenger's own trade reveal something?

Why these two. Disclosure is the first thing a seller can control, and it needs only a shift of the prior in the trading stage. A toehold is the classic bidder-side force; the paper names it as an abstraction. I did not study the third example ("the challenger observes order flow, not price"). Section 3.8 shows that it changes nothing in the discrete-Laplace model.

Main findings:

- A costless public test beats the market as a source of information. The optimal test pools every high-class challenger with enough low-class ones.
- A small test can lower entry. The market's information and the test's information are substitutes, with a valley between them.
- Against a stronger incumbent the optimal test is more informative, and entry under it falls. The reversal of the paper does not survive.
- A public toehold widens the window of the reversal and moves the information ceiling out. A hidden toehold by a low-cost challenger is profitable, and it leaves entry unchanged.

## 2. Setup

### 2.1 Base model and why

**Base: discrete Laplace.** Noise $Z\in\mathbb Z$ has $n(z)=\frac{1-a}{1+a}a^{|z|}$ with $a=e^{-1/b}$. Orders are $q\in\{0,1\}$, $c_L=0$, and the investor is present with probability one ($\lambda=1$). Auction values are the paper's: $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$.

The reasons for this base:

1. Every flow has positive probability. No off-path belief is needed.
2. At every prior the posterior takes two values only. A public signal then moves the log odds in a clean way.
3. The three-point model has posteriors in $\{0,\varphi,1\}$. A bad top flow always reveals class L there. I expect a different disclosure result. I did not study it.

Parameters used in numbers: $b=2$ ($a=0.606531$), $k=0.02$, $c_H=5$, prior $\pi=1/2$. The value $c_H=5$ follows the team's discrete-Laplace window. The paper's $c_H=6$ lies outside it, and Section 5 shows the market alone cannot recruit there.

### 2.2 The disclosure game

The timing is:

1. The target commits to a public experiment on the class $j$. The experiment is any joint law of a public signal and $j$.
2. The signal is realised and is public. All players see it.
3. The investor sees $j$ and trades. Market makers set $P(X)=\mathbb E[V_T\mid X, \text{signal}]$.
4. The challenger sees the signal, the price and its cost. It decides to prepare.

The test needs a certifier who observes $j$. This is an assumption of the exercise.

Only the posterior $\varphi=\Pr(H\mid\text{signal})$ matters for the later game. So a policy is a distribution of branch priors $\varphi$ with mean $\pi$.

**Equilibrium concept.** Subgame perfect: the target moves first and commits. In each branch, the trading stage is a Bayesian equilibrium with competitive prices and optimal entry.

**Belief rule.** None is needed. All flows are on path.

**Tie rules.**

- The investor buys only if the gain is strictly positive. A tie gives no trade.
- The challenger prepares at indifference.

**Selection in a branch.** Some priors have two equilibria (no trade and full buying). I report both selections. The optimal policy below does not depend on the choice (Lemma in Result D3).

### 2.3 Notation

All auction objects are those of the paper (Section 3 of the team rules): $t_0,t_L,t_H,g_L,g_H,\Delta_T$. Add

$$w_L=t_L-t_0,\qquad \Phi=\Pi-t_0,$$

where $\Pi$ is target proceeds in a branch. With $0<\tau<1$ the entry rule is $e(\mu)=\rho+(1-\rho)\mathbf 1\{\mu\ge\tau\}$, and

$$\tau_r=\frac{c_H-g_L}{g_H-g_L},\qquad T_r=\frac{\tau_r}{1-\tau_r}.$$

Write $\omega=\varphi/(1-\varphi)$ for the prior odds. Three cut-off priors appear:

$$\varphi_1=\frac{aT}{1+aT},\qquad \varphi_2=\tau=\frac{T}{1+T},\qquad \varphi_3=\frac{T}{a+T}.$$

They are the priors with odds $aT$, $T$ and $T/a$. The symbol $\lambda$ is used only for investor presence.

### 2.4 The toehold

A toehold of size $s\in[0,1]$ is a stake in target shares. I use two forms:

- **Public toehold.** The stake is known to all. The challenger's bids stay truthful (partial analysis, see Section 6).
- **Hidden unit.** A challenger who knows its cost buys one unit before the price forms. The unit is small. It moves the flow, and it does not move the challenger's gain from entry.

Bulow, Huang and Klemperer (1999) is the toehold reference in the paper. It is **unverified** for this team.

## 3. Results

### 3.1 Result D1: the trading stage at any public prior (analytical)

Fix a branch prior $\varphi\in(0,1)$ and $0<\tau<1$.

**Statement.**

1. For every price schedule, $V_H-P=e\Delta_T(1-\mu)$ and $V_L-P=-e\Delta_T\mu$. Class L never buys.
2. If H buys with probability $\beta$, flows $x\ge1$ ("good") have likelihood ratio $(1-\beta)+\beta/a$. Flows $x\le0$ ("bad") have ratio $(1-\beta)+\beta a$. At $\beta=1$ the ratios are $1/a$ and $a$.
3. At $\beta=1$ the entry profile $(e_g,e_b)$ is:
   - $(\rho,\rho)$ if $\omega<aT$;
   - $(1,\rho)$ if $aT\le\omega<T/a$;
   - $(1,1)$ if $\omega\ge T/a$.
4. No trade is an equilibrium if and only if $\bar G_0(\varphi)\le k$, where $\bar G_0(\varphi)=e(\varphi)\Delta_T(1-\varphi)$ is the gross gain from one unit.
5. Full buying is an equilibrium if and only if $\bar G_1(\varphi)>k$, where the gross gain from one unit is

$$\bar G_1(\varphi;e_g,e_b)=\frac{\Delta_T\,a(1-\varphi)}{1+a}\left[\frac{e_g}{a+(1-a)\varphi}+\frac{e_b}{1-(1-a)\varphi}\right].$$

6. Inside one entry profile, $\bar G_1$ is strictly decreasing in $\varphi$. Also $\bar G_1(\varphi;e_g,e_b)\le\bar G_1(\varphi;1,1)\le\Delta_T(1-\varphi)$.

**Proof.**

*Step 1.* Competitive pricing gives $P=t_0+e(w_L+\Delta_T\mu)$. Entry depends on the price and on the cost. Both are independent of $j$ given the price. So $\mathbb E[V_T\mid j,x]=t_0+e\,(t_j-t_0)$. With $t_H-t_0=w_L+\Delta_T$ and $t_L-t_0=w_L$, item 1 follows. The entry floor $\rho$ keeps $e>0$, so the price reveals $\mu$.

*Step 2.* The gain of class L from one unit is $-\sum_x(\cdot)e_x\Delta_T\mu_x-k\le-k<0$.

*Step 3.* Under H-buying with probability $\beta$, $\Pr(x\mid H)=(1-\beta)n(x)+\beta n(x-1)$ and $\Pr(x\mid L)=n(x)$. For $x\ge1$, $n(x-1)/n(x)=1/a$. For $x\le0$, it is $a$. This gives item 2. The posterior odds are $\omega$ times the ratio. Entry at $\mu\ge\tau$ is the same as odds $\ge T$. So the good flow recruits when $\omega/a\ge T$, and the bad flow when $\omega a\ge T$. This is item 3.

*Step 4.* Under no trade all flows have posterior $\varphi$. The gain from one unit is $e(\varphi)\Delta_T(1-\varphi)-k$. This is item 4.

*Step 5.* Under $\beta=1$ the gain from one unit is $\Pr(Z\ge0)\,e_g\Delta_T(1-\mu_g)+\Pr(Z\le-1)\,e_b\Delta_T(1-\mu_b)-k$ with $\Pr(Z\ge0)=1/(1+a)$. Also $1-\mu_g=\frac{a(1-\varphi)}{a+(1-a)\varphi}$ and $1-\mu_b=\frac{1-\varphi}{1-(1-a)\varphi}$. Substitution gives item 5.

*Step 6.* Both terms in item 5 fall in $\varphi$:

$$\frac{d}{d\varphi}\frac{1-\varphi}{a+(1-a)\varphi}=\frac{-1}{(a+(1-a)\varphi)^2}<0,\qquad \frac{d}{d\varphi}\frac{1-\varphi}{1-(1-a)\varphi}=\frac{-a}{(1-(1-a)\varphi)^2}<0.$$

For the bound, put $F=\bar G_1/(\Delta_T(1-\varphi))=\frac{a}{1+a}\big[\frac{e_g}{a+(1-a)\varphi}+\frac{e_b}{1-(1-a)\varphi}\big]$. For $e_g=e_b=1$ the bracket is convex in $\varphi$, and $F(0)=F(1)=1$. So $F\le1$ on $[0,1]$. Lower entry levels only lower $F$. $\square$

Remarks:

- Both equilibria can exist together (for example $r=1.5$, $\varphi=1/2$). Neither may exist. The prescribed tie rule then gives no pure equilibrium. See Section 6.
- This is the "general prior" version of the discrete-Laplace stage. Workstream B2 has the same item. I derived it myself; a reader should reconcile the two.
- Exact check: `run_exact_identities.py` (rational $a=3/5$) shows the closed form in item 5 equals the direct sum at four priors.
- Item 6 has a use below: if $\Delta_T(1-\varphi)\le k$, then full buying fails at $\varphi$, whatever the entry profile.

### 3.2 Result D2: outcomes are piecewise linear; disclosure is concavification (analytical)

Inside one entry profile and one equilibrium label, the outcome functions are linear in $\varphi$. Under full buying:

$$\Pr(g)=\tfrac{\varphi+a(1-\varphi)}{1+a},\quad \Pr(g,H)=\tfrac{\varphi}{1+a},\quad \Pr(b,H)=\tfrac{a\varphi}{1+a},\quad \Pr(b)=\tfrac{a\varphi+1-\varphi}{1+a}.$$

Entry, high-class ownership and proceeds are

$$E=\sum_s e_s\Pr(s),\qquad O_H=\sum_s e_s\Pr(s,H),\qquad \Phi=w_LE+\Delta_TO_H.$$

All three are linear in $\varphi$ for fixed $(e_g,e_b)$. Under no trade, $\Phi=e\,(w_L+\Delta_T\varphi)$.

**Consequence.** The target's value from a policy is $\mathbb E[\Phi(\varphi)]$ over branch priors with mean $\pi$. The best value is the concave envelope of $\Phi$ at $\pi$. This is the standard Bayesian persuasion argument (Kamenica and Gentzkow 2011; **unverified**). The envelope has finitely many vertices. They are the cell edges below, so the computation is exact.

Cell edges of $\Phi$ (all computed in `pieces.py`): the three cut-offs $\varphi_1,\varphi_2,\varphi_3$; the root of $\bar G_0=k$ for each entry level; the root of $\bar G_1=k$ for each of the three profiles. Each root is unique by D1, item 6.

### 3.3 Result D3: the optimal disclosure policy (computer-assisted)

Define the lowest prior with full entry after every flow:

$$\varphi^*=\min\{\varphi_{NT},\varphi_{FB}\},\quad \varphi_{NT}=\max\{\tau,\,1-k/\Delta_T\},\quad \varphi_{FB}=\begin{cases}\varphi_3&\text{if }\bar G_1(\varphi_3;1,1)>k,\\ \infty&\text{otherwise.}\end{cases}$$

Let $\gamma=\Delta_T+(1-\rho)w_L/\varphi^*$ and $\ell(\varphi)=\rho w_L+\gamma\varphi$.

**Statement.** Assume $\pi\le\varphi^*<1$, and the chord condition

$$\textbf{(C)}\qquad \Phi_{(1,\rho)}(\varphi_1)\le\ell(\varphi_1),$$

where $\Phi_{(1,\rho)}(\varphi)=\frac{1}{1+a}\big[w_L(\varphi+a(1-\varphi))+\Delta_T\varphi+\rho\,(w_L(a\varphi+1-\varphi)+\Delta_Ta\varphi)\big]$. Then the optimal policy has two branches:

- prior $0$ with probability $1-\pi/\varphi^*$ (the test reveals class L);
- prior $\varphi^*$ with probability $w=\pi/\varphi^*$ (the test passes).

Every H passes. A fraction $\frac{\pi(1-\varphi^*)}{\varphi^*(1-\pi)}$ of L also pass. The outcomes are

$$E^*=\rho+(1-\rho)\frac{\pi}{\varphi^*},\qquad O_H^*=\pi,\qquad \Phi^*=w_LE^*+\Delta_T\pi.$$

**Proof (support line).**

*(a)* $\ell(0)=\rho w_L=\Phi(0)$, because at prior 0 only L exists and entry is $\rho$. Also $\ell(\varphi^*)=w_L+\Delta_T\varphi^*=\Phi(\varphi^*)$, because both entries are 1 at $\varphi^*$ (a tie at the bad-flow posterior is resolved by preparing).

*(b)* For $\varphi\ge\varphi^*$: $E\le1$ and $O_H\le\varphi$, so $\Phi\le w_L+\Delta_T\varphi$. Also $\ell(\varphi)-(w_L+\Delta_T\varphi)=(1-\rho)w_L(\varphi/\varphi^*-1)\ge0$.

*(c)* For $\varphi<\varphi^*$, take each pure equilibrium.

- *No trade.* If $\varphi<\tau$, then $e=\rho$. If $\varphi\ge\tau$, no trade needs $\varphi\ge1-k/\Delta_T$, hence $\varphi\ge\varphi_{NT}\ge\varphi^*$. So $e=\rho$ and $\Phi=\rho(w_L+\Delta_T\varphi)\le\ell(\varphi)$, because $\gamma\ge\Delta_T$.
- *Full buying below $\varphi_1$.* The profile is $(\rho,\rho)$. The same bound holds.
- *Full buying on $[\varphi_1,\varphi^*)$.* The profile is $(1,\rho)$. (Profile $(1,1)$ needs $\varphi\ge\varphi_3$, and full buying fails there if $\varphi_{FB}=\infty$.) $\Phi_{(1,\rho)}$ is linear. At $\varphi^*$ it is at most $\Phi_{(1,1)}(\varphi^*)=\ell(\varphi^*)$, since $e_b\le1$. At $\varphi_1$ it is at most $\ell(\varphi_1)$ by (C). A linear function below $\ell$ at both ends is below $\ell$ between them.

*(d)* So $\Phi\le\ell$ on $[0,1]$ for every pure equilibrium, whatever the selection. The envelope at $\pi$ is at most $\ell(\pi)$. The two-branch policy reaches $\ell(\pi)$ if the selected equilibrium at $\varphi^*$ has value $w_L+\Delta_T\varphi^*$. The lemma below shows that it has. $\square$

**Lemma (selection does not matter at $\varphi^*$).** Every pure equilibrium at $\varphi^*$ has $e_g=e_b=1$.

*Proof.* There are two cases.

- If $\varphi^*=\varphi_3$: full buying has profile $(1,1)$. No trade, if it exists, has $e=1$ since $\varphi_3\ge\tau$. Both give $\Phi=w_L+\Delta_T\varphi^*$.
- If $\varphi^*=\varphi_{NT}<\varphi_{FB}$: then $\Delta_T(1-\varphi^*)\le k$. By D1, item 6, full buying fails at $\varphi^*$ for every profile. No trade is the only equilibrium, and it has $e=1$ since $\varphi^*\ge\tau$. $\square$

So the optimal policy and its value do not depend on the selection. Selection matters only for the no-disclosure baseline.

**What the computer checks.** The proof is analytical once (C) and the existence of $\varphi^*$ hold. Those are finite inequalities:

- (C) holds with margin at all 41 strengths $r\in\{1.2,1.4,\dots,9.2\}$ (smallest margin $0.0518$ at $r=1.4$; $0.145$ at $r=3$), 60 digits, $b=2$.
- Exact rational check at $a=3/5$, $r=3$: the margin is $17427/122560=0.1422$. $\bar G_1(\varphi_3;1,1)-k=10313/61200>0$. On 1001 rational priors the largest $\Phi-\ell$ is $0$, reached only at $\varphi=0$.
- The exact-piece hull equals the closed form $\varphi^*$ at every tested $r$, except one point: at $r=1.4$, full buying fails at $\varphi_3$, and the hull uses $\varphi_{NT}=0.65$ (the rule above covers this).
- Priors with no pure equilibrium exist (Section 6). For $r\ge1.8$ they lie above $\varphi^*$ and cannot change the result, since $\Phi\le w_L+\Delta_T\varphi\le\ell$ there. For $r\in[1.4,1.6]$ they lie below $\varphi^*$. The result is then a lower bound under the prescribed tie rule.

### 3.4 Result D4: symmetric signals, a neutral zone, a valley, a recovery (analytical)

Take $\pi=1/2$ and a symmetric signal of accuracy $d\in(1/2,1]$. The branch priors are $d$ and $1-d$. Assume the window $1<T\le1/a$ (the paper's (A2) in odds form) and full buying in each branch. Put $d_1=1-\varphi_1$ and $d_2=\varphi_3$, and $P_g(\varphi)=\frac{\varphi+a(1-\varphi)}{1+a}$.

**Statement.**

- $d_1<d_2$.
- *Neutral zone.* For $d\le d_1$, entry, ownership and proceeds equal their no-disclosure values.
- *Valley.* For $d_1<d<d_2$:
  - $E(d)=\rho+\tfrac{1-\rho}{2}P_g(d)$, below $E(\tfrac12)=\tfrac{1+\rho}{2}$ by $\tfrac{1-\rho}{2}(1-P_g(d))$;
  - $O_H(d)-O_H(\tfrac12)=-\frac{(1-\rho)(1-d)}{2(1+a)}<0$;
  - proceeds fall.
- *Recovery.* For $d\ge d_2$: $E=\tfrac{1+\rho}{2}$ (as with no disclosure), $O_H=\tfrac12[d+(1-d)\rho]$, and $O_H$ exceeds its no-disclosure value if and only if $d>1/(1+a)$. Proceeds rise.

**Proof.**

*(i) Order.* $d_1=\frac1{1+aT}$ and $d_2=\frac T{a+T}$. Then $d_1<d_2$ iff $a+T<T+aT^2$ iff $T>1$. The window gives $T>1$.

*(ii) Neutral zone.* For $d\le d_1$, the lower branch $1-d\ge\varphi_1$ and the upper branch $d<\varphi_3$ both lie in profile $(1,\rho)$. Outcomes are linear in $\varphi$ within one profile. The two branches have mean prior $1/2$. So the average outcome equals the outcome at $1/2$.

*(iii) Valley.* For $d>d_1$ the lower branch has $1-d<\varphi_1$, so $E=\rho$. The upper branch has profile $(1,\rho)$, so $E=\rho+(1-\rho)P_g(d)$. Averaging gives the stated $E(d)$. Ownership: $O_H=\tfrac12\big[\tfrac{d(1+\rho a)}{1+a}+(1-d)\rho\big]$. Subtracting $\tfrac12\tfrac{1+\rho a}{1+a}$ and using $\tfrac{1+\rho a}{1+a}-\rho=\tfrac{1-\rho}{1+a}$ gives the stated difference.

*(iv) Recovery.* For $d\ge d_2$ the upper branch has $e_g=e_b=1$, so $E=1$ there and $E(d)=\tfrac{1+\rho}2$. The ownership comparison reduces to $d(1-\rho)>\tfrac{1-\rho}{1+a}$. $\square$

Exact check (`run_exact_identities.py`, $a=3/5$, $r=3$): $d_1=0.5418$, $d_2=0.7014$. The predicted $E$ equals the computed $E$ as an exact fraction at all nine tested $d$ (for example $E(0.55)=0.442188$).

### 3.5 Result D5: competition and disclosure (analytical; numbers in Table D)

**(i) The cut-off rises with the incumbent (analytical).** If $g_L<c_H<g_H$, then $\tau_r$ is strictly increasing in $r$.

*Proof.* With $N=c_H-g_L$ and $D=g_H-g_L$: $N'D-ND'=|g_L'|(g_H-c_H)+(c_H-g_L)|g_H'|>0$, because $g_L'<0$ and $g_H'<0$ by the paper's equation (5). $\square$

Hence $T_r$, $\varphi_3(r)$ and $1-k/\Delta_T(r)$ all increase in $r$. Where $\varphi^*=\varphi_3$, the optimal policy at a stronger incumbent is a mean-preserving spread of the policy at a weaker one. It is more informative in the Blackwell sense.

**Answer to the second question: yes.** Against a stronger incumbent the target discloses more. The pass posterior $\varphi^*$ rises and the pass probability $\pi/\varphi^*$ falls. Entry under the optimal policy, $E^*(r)=\rho+(1-\rho)\pi/\varphi^*(r)$, falls in $r$. High-class ownership stays at $\pi$ for all $r$ below the disclosure ceiling.

Status of the monotonicity:

- Analytical where $\varphi^*=\varphi_3$ on both sides of the comparison (the benchmark, $r\ge1.6$).
- A fact on the tested grid ($r=1.2,1.4,\dots,9.2$) across the switch from $\varphi_{NT}$ to $\varphi_3$ (between $r=1.2$ and $r=1.6$). Entry there is $0.969$, $0.827$, $0.822$, $0.816$, and then falls.

**(ii) A fixed public signal removes the reversal.** If $d\ge\max\{\tau_{r_0},\varphi_3(r_1)\}$, then entry is $\tfrac{1+\rho}2$ at both $r_0$ and $r_1$. Ownership is also the same. At $r_0$ the market is dead ($\Delta_T<k$), so the upper branch recruits through the signal alone.

**(iii) Reversal of the reversal in the valley.** At the benchmark with $d\in[0.55,0.65]$, entry is $0.625$ at $r_0$ and $0.442$ to $0.451$ at $r_1$ (Table D). Competition then lowers entry.

**(iv) Value of disclosure is U-shaped in $r$ (numerical diagnostic).** `output_value_of_disclosure.txt`: the gain $\Pi^*-\Pi^{\text{market only}}$ is $0.29$ at $r=1.2$, $0.105$ at $1.75$, $0.168$ at $3$, $0.20$ at $3.6$, and $0.66$ at $4.0$, after the market's ceiling. The target values disclosure least where the market works best.

### 3.6 Result D6: does disclosure kill trading? (numerical diagnostic, with an analytical part)

**Trade survives.** In the pooled branch the investor still trades if $k<k_{\max}(\varphi^*)=\bar G_1(\varphi^*;1,1)$. Table B: $k_{\max}=0.190$ at $r=3$ (no disclosure: $0.196$), $0.251$ at $3.6$, $0.304$ at $4.2$. The cost $k=0.02$ is far below. Disclosure does not kill trading at the benchmark. It kills the **use** of the trade: in the pooled branch both flows give entry 1.

**The investor's information is a cost to the persuader.** Without trading, the target would pool at $\tau$ and pass a larger share. With an active market it must overshoot to $\varphi_3$, because bad flow would otherwise cancel the entry. Table C ($r=3$): pass probability $0.715$ with the market and $0.855$ without; entry $0.786$ against $0.891$.

**When trading dies.** The rule for $\varphi^*$ has three ranges of $k$ at $r=3$:
- $k<0.190$: full buying holds at $\varphi_3$, and $\varphi^*=\varphi_3=0.699$.
- $0.190\le k<0.277$: full buying fails at $\varphi_3$ and $\varphi^*=1-k/\Delta_T$ (for example $0.70$ at $k=0.2$).
- $k\ge\Delta_T(1-\tau)=0.277$: no trade with full entry holds at $\tau$, and $\varphi^*=\tau=0.585$ (the run at $k=0.3$).

A higher trading cost helps the persuader, because it silences the market.

**Sensitivity of the optimal policy at $r=3$** (`run_sensitivity.py`):

| change | $\varphi^*$ | pass prob. $w$ | entry $E^*$ |
|---|---|---|---|
| benchmark | 0.6992 | 0.715 | 0.786 |
| $c_H=4$ / $6$ / $8$ | 0.589 / 0.798 / 0.966 | 0.849 / 0.627 / 0.518 | 0.887 / 0.720 / 0.638 |
| $b=1.5$ / $4$ / $10$ | 0.733 / 0.644 / 0.609 | 0.682 / 0.776 / 0.821 | 0.762 / 0.832 / 0.866 |
| $\rho=0.1$ / $0.5$ | 0.6992 | 0.715 | 0.744 / 0.858 |
| $\pi=0.3$ | 0.6992 | 0.429 | 0.572 (ownership 0.3) |

At $c_H=6$ and at $b\ge4$ the market alone gives entry $\rho$ (no recruitment), but disclosure still recruits. This is the information ceiling: disclosure removes it.

### 3.7 The toehold

**Result T1: a public toehold (analytical; numbers computed).** Keep bids truthful. With a stake $s$, entry adds $s$ shares of the change in target proceeds. The entry gain at posterior $\mu$ is

$$B^s_r(\mu)=B_r(\mu)+s\,(w_L+\Delta_T\mu)=g_L+sw_L+\mu\big[(g_H-g_L)+s\Delta_T\big].$$

*Derivation.* If the challenger prepares, it gets $g_\theta+st_\theta$ in expectation (the stake earns the proceeds $t_\theta$). If it does not, it gets $st_0$. The difference is $g_\theta+s(t_\theta-t_0)$.

*Properties.*

1. **Deterrence survives.** At fixed $\mu$, $\partial_rB^s_r=-(1-s)t_L'-st_0'-(1-s)\mu\Delta_T'<0$ for $s\in[0,1]$. A toehold shrinks deterrence; it never reverses it. (The grid check gives a largest derivative of $-0.0039$.)
2. **The window of the reversal widens.** The $c_H$ window of Proposition 2 becomes $B^s_{r_0}(\tfrac12)<c_H\le B^s_{r_1}(M_1)$. At the benchmark its width is $0.508$ at $s=0$, $0.602$ at $s=0.2$, $0.743$ at $s=0.5$, $0.977$ at $s=1$.
3. **The reversal breaks at a large stake.** The prior alone recruits at $r_0$ when $s\ge s^*=(c_H-B_{r_0}(\tfrac12))/(w_L+\Delta_T/2)=0.4845$. Then $r_0$ has entry $1$ with no trade. This is a very large stake.
4. **The information ceiling moves out.** The market-only ceiling $r_C(s)$ solves $B^s_r(M_1)=c_H$:

| $s$ | 0 | 0.1 | 0.2 | 0.3 | 0.5 | 1 |
|---|---|---|---|---|---|---|
| $r_C(s)$ | 3.986 | 4.395 | 4.903 | 5.551 | 7.608 | none below $h$ |

5. **Entry and ownership.** At $r=4.2$ a stake of $s=0.1$ restores entry $0.625$ (from $0.25$).
6. **Toehold and disclosure are weak substitutes.** With a stake, $\tau^s$ falls. The optimal pass posterior falls, and the pass probability rises. At $r=3$: $\varphi^*=0.699,0.682,0.656,0.614$ for $s=0,0.2,0.5,1$; entry $0.786,0.800,0.822,0.861$.

**Result T2: a purchase at the fair price before the cost is known does not pay (analytical).** Suppose the challenger buys $s$ shares at public price $P_0(s)=\mathbb E[V_T\mid s]$, before it learns $C$.

*Proof.* Let $e^s$ maximise the gain $g_j+s(t_j-t_0)-C$. Market makers anticipate $e^s$. So $\mathbb E[s(V_T-P_0(s))]=0$. The challenger's expected payoff is $U(s)=\mathbb E[e^s(g_j-C)]$. The rule $e^0$ maximises this over all rules that use the price and the cost. So $U(s)\le U(0)$, with strict inequality when $e^s\ne e^0$ matters. $\square$

A challenger that is uninformed at the purchase gets no rent, and the stake only distorts its entry towards too much entry. The toehold of the literature rests on a price that does not anticipate it, or on private information at the purchase. Result T3 studies the second case.

**Result T3: a hidden unit bought after the cost is known (numerical diagnostic).** Setup (`toehold_hidden.py`): the challenger learns $C$ first. It buys one unit with probability $\sigma_C\in\{0,1\}$ at cost $k_C=k$. The unit adds to the flow. Market makers do not see who buys. The challenger sees the price, knows its own unit, and removes it from the flow. The three flow regions $\{x\le0\},\{1\},\{\ge2\}$ are sufficient: the likelihood ratio of every pair of hypotheses is constant on each region. Pure profiles are $(\beta,\sigma_L,\sigma_H)\in\{0,1\}^3$, all 8 enumerated at $r=1.2,3,3.6,4.2$. A grid over $\beta\in\{0,\tfrac14,\dots,1\}$ covers mixed investor play.

Findings:

1. **The low-cost challenger always buys.** Its net gain from one unit (after the cost $0.02$) is positive in every profile tested. The smallest net gain over the grid is $0.071$ ($r=1.2$), $0.109$ ($r=3$), $0.121$ ($r=3.6$), $0.749$ ($r=4.2$). The reason: it enters for sure, and the price assumes entry with a probability below one.
2. **The high-cost challenger never buys.** Its largest net gain over the grid is negative ($-0.051$ at $r=1.2$ to $-0.278$ at $r=4.2$). Its own unit moves the flow across a threshold, so the price rises on its own order.
3. **The pure equilibrium is unique** in the 8 profiles at each strength, and strict: $\beta=1,\sigma_L=1,\sigma_H=0$ at $r=3,3.6,4.2$ and $\beta=0,\sigma_L=1,\sigma_H=0$ at $r=1.2$.
4. **Entry, ownership and proceeds do not change.** At $r=3$: $E=0.625$, $O_H=0.358422$, as in the baseline. The trade reveals the cost type $C$, and the cost type is independent of the class. The high-cost challenger's inference is unchanged, because it removes its own order.
5. **The investor's cut-off moves a little.** The largest $k$ at which the investor still buys is $0.1988$ (baseline $0.1958$) at $r=3$, $0.2800$ (baseline $0.2758$) at $r=3.6$, and $0.1264$ (baseline $0.1432$) at $r=4.2$. In the weak economy the gross gain from buying turns negative: $-0.0146$ at $r=1.2$ (baseline $+0.0021$).

*Answer to the question.* The challenger's own trade reveals its cost, hence its entry. It cannot reveal the class. Under Reading N its order depends on the cost only, and the cost is independent of the class. Hidden trading by the challenger does not change the price-to-entry channel at these parameters. It shifts the investor's cut-off by a small amount.

### 3.8 Remark: flow versus price (analytical, a short note on the third example)

In the discrete-Laplace model with full buying, the price takes two values ($P_g>P_b$), and the likelihood ratio takes two values on the same two regions. A challenger who sees the flow has the same posterior as one who sees the price. Observing the flow adds nothing. In the hidden-toehold equilibrium the price separates all three regions. So the same holds there.

## 4. What it recovers or loses relative to the Laplace paper

| Paper item | Under disclosure | Under a toehold |
|---|---|---|
| Prop. 1 (two returns) | Unchanged. It lives in the auction layer. | Unchanged under truthful bids. With a stake, the low type overbids; $t_L$ rises and $\Delta_T$ falls (not computed). |
| Prop. 2 (i)-(ii), the reversal | Survives only for a weak signal ($d\le d_1$). It fails for $d>\tau_{r_0}$, where entry is $0.625$ at both strengths (Result D5). Under the optimal policy entry falls with $r$. | Survives and widens (T1.2). Breaks only at $s\ge0.48$. |
| Prop. 2 (iii), the ceiling | Removed. The disclosure ceiling solves $g_H(r)=c_H$: $r=9.97$ against $3.99$. | Moves out with $s$ (T1.4). |
| Prop. 3, coexistence | Branch-level coexistence remains. The optimal policy picks a branch with a unique equilibrium. | Not studied. |
| Endogenous asymmetry | Not applicable (buy-only). | Not applicable. |
| Prop. A.3, fixed experiment | The fixed public signal is such an experiment. The valley is its numerical counterpart. | Deterrence at fixed belief remains (T1.1). |
| Size of the effect | At $r=3$: entry $0.625\to0.786$, ownership $0.358\to0.5$, added proceeds $\Phi$ $+32\%$ (proceeds $\Pi$ $+18\%$). | Small at small stakes. |
| Robustness | The policy shape is stable across $c_H$, $b$, $\rho$, $\pi$, and $k\le0.1$ (Section 3.6). | Window widens with $s$. |

**What this says about the paper.** A target that can commit to a costless public test of fit does not need competition to create information. The reversal is a result about information that the target cannot or will not supply. This is a limit on the claim, and it is also a statement of when the mechanism matters: when disclosure is not credible, not verifiable, or costly.

## 5. Numerical example

Benchmark: $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $b=2$, $k=0.02$, $c_H=5$, $\pi=1/2$. Source: `output_memo_tables.txt`. $\Phi=\Pi-t_0$.

**Table A.** Entry $E$, high-class ownership $O_H$, proceeds $\Phi$.

| $r$ | $\Delta_T$ | $\tau$ | no disclosure ($E$, $O_H$, $\Phi$) | full disclosure | $d=0.55$ | optimal: $\varphi^*$, $w$, $E$, $O_H$, $\Phi$ |
|---|---|---|---|---|---|---|
| 1.2 | 0.0167 | 0.5218 | 0.250, 0.125, 0.1010 | 0.625, 0.500, 0.2557 | 0.625, 0.331, 0.2529 | 0.5218, 0.958, 0.969, 0.5, 0.3918 |
| 3.0 | 0.6667 | 0.5850 | 0.625, 0.358, 0.5254 | 0.625, 0.500, 0.6198 | 0.442, 0.253, 0.3716 | 0.6992, 0.715, 0.786, 0.5, 0.6937 |
| 3.6 | 0.9389 | 0.6073 | 0.625, 0.358, 0.6273 | 0.625, 0.500, 0.7602 | 0.442, 0.253, 0.4436 | 0.7183, 0.696, 0.772, 0.5, 0.8287 |
| 4.2 | 1.2190 | 0.6311 | 0.250, 0.125, 0.2699 | 0.625, 0.500, 0.9034 | 0.442, 0.253, 0.5168 | 0.7383, 0.677, 0.758, 0.5, 0.9659 |

Notes. Full disclosure has flat entry in $r$ ($0.625$). The optimal policy has the highest proceeds at each $r$. At $r=1.2$ the market is dead, so $\varphi^*=\tau$. At $r\ge1.8$ it equals $\varphi_3$. Levels of $\Pi$ at $r=3$: $0.942$ (no disclosure), $1.110$ (optimal).

**Table B.** Largest $k$ at which the investor buys: at $\varphi^*$ and at the prior $1/2$ without disclosure.

| $r$ | 3.0 | 3.6 | 4.2 | 5.0 | 7.0 |
|---|---|---|---|---|---|
| at $\varphi^*$ | 0.190 | 0.251 | 0.304 | 0.357 | 0.383 |
| no disclosure | 0.196 | 0.276 | 0.143 | 0.188 | 0.302 |

**Table C.** Pass probability and entry, with and without an active market.

| $r$ | 2.0 | 3.0 | 3.6 | 4.2 |
|---|---|---|---|---|
| $w$ with / without market | 0.748 / 0.909 | 0.715 / 0.855 | 0.696 / 0.823 | 0.677 / 0.792 |
| $E$ with / without market | 0.811 / 0.932 | 0.786 / 0.891 | 0.772 / 0.867 | 0.758 / 0.844 |

**Table D.** Entry under a fixed symmetric signal of accuracy $d$, by strength.

| $d$ | $r=1.2$ | $r=3.0$ | $r=3.6$ | $r=4.2$ |
|---|---|---|---|---|
| 0.50 | 0.250 | 0.625 | 0.625 | 0.250 |
| 0.55 | 0.625 | 0.442 | 0.442 | 0.442 |
| 0.60 | 0.625 | 0.447 | 0.447 | 0.447 |
| 0.65 | 0.625 | 0.451 | 0.451 | 0.451 |
| 0.70 | 0.625 | 0.625 | 0.456 | 0.456 |
| 0.75 | 0.625 | 0.625 | 0.625 | 0.625 |
| 1.00 | 0.625 | 0.625 | 0.625 | 0.625 |

The first row is the paper's reversal ($0.25\to0.625\to0.25$). Every other row removes it.

**Cut-offs at $r=3$.** $T=1.4096$, $\varphi_1=0.4609$, $\varphi_2=\tau=0.585$, $\varphi_3=0.6992$; valley $d_1=0.539$, $d_2=0.699$. With rational $a=3/5$: $d_1=415/766$, $d_2=195/278$.

**Scripts** (all print only):

- `common.py`, `branch.py`, `pieces.py`, `persuasion.py`: the model, the trading stage, the exact cells, the hull.
- `run_branch_table.py`, `run_pieces.py`, `run_symmetric.py`, `run_formula_check.py`: the equilibria, the policy, the valley, the support line.
- `run_exact_identities.py`: exact rational checks (output in `output_exact_identities.txt`).
- `run_sensitivity.py`, `run_memo_tables.py`, `run_value_of_disclosure.py`, `run_gap_mixed_scan.py`, `run_gap_by_r.py`: sensitivity and robustness.
- `run_toehold_public.py`, `toehold_hidden.py`, `run_hidden_dominance.py`: the toehold.

## 6. Open issues

1. **Priors with no pure equilibrium.** Under the prescribed investor tie rule some priors have neither no trade nor full buying. Interior investor mixtures exist there if ties may mix.
   - At $r=1.4$ the gap is $[0.529,0.649]$. At $r=1.6$ it is $[0.254,0.289]$. At $r=1.5$ a scan finds 38 of 401 grid priors without a pure equilibrium.
   - For $r\ge1.8$ the only gap is a thin band just below $\varphi_{NT}$ (width $0.0029$ at $r=1.8$, $0.0002$ at $r=3$). It lies above $\varphi^*$.
   - Result D3 is exact for $r\ge1.8$ and for $r=1.2$. For $r\in[1.4,1.6]$ it is a lower bound. I did not solve the mixed branch games.
2. **The condition (C) is checked on a grid, not proved** for all parameters.
3. **Equilibrium selection** matters for the no-disclosure baseline at $r\approx1.5$ (coexistence). It does not matter for the optimal policy (Lemma in Result D3), but only among pure equilibria.
4. **Disclosure technology.** The test needs a certifier who knows $j$. A cost of disclosure, a limit on test accuracy, or delay are not modelled. With them the optimum would not be the pure screen.
5. **No commitment.** Without commitment, silence may reveal class L (unravelling). Not modelled.
6. **Welfare.** I computed target proceeds only. Challenger payoffs and total surplus net of preparation costs are not computed.
7. **Toehold and bidding.** I held bids truthful. With a stake $s$ and a uniform incumbent, the low type's bid maximises its payoff at $b^*=(\ell+sr)/(1+s)>\ell$. This raises $t_L$ and lowers $\Delta_T$. It changes the trading incentive. Not computed. Bulow, Huang and Klemperer (1999) is unverified.
8. **Hidden toehold.** Only pure challenger strategies and a unit that does not change the entry gain. The unit price impact and the unit size are tied to the noise unit. Legal limits on hidden stakes (disclosure rules) are outside the model and unverified.
9. **The three-point model** under disclosure. I expect that a bad top flow reveals class L at any prior, so overshoot cannot work. The pooled branch would then need a dead market ($\varphi\ge1-O(k/\Delta_T)$). I did not check this.
10. **Interaction with other items.** The incumbent's response to the price (C7), the reserve after the price (C8) and a second round (C2) can change how disclosure and trading interact.

## 7. Plain summary

I studied two modifications in the discrete-Laplace model with buy-only orders: public disclosure by the target, and a toehold for the challenger.

Disclosure first. The target commits to a test of challenger fit. The best test passes every high-class challenger and enough low-class ones to hold the posterior at a set level. That level is high enough that even bad market news keeps entry at one. At the benchmark ($r=3$) entry rises from 0.625 to 0.786, high-class ownership from 0.358 to 0.5, and added proceeds by 32% (total proceeds by 18%). A small test does harm: for accuracy between 0.54 and 0.70, entry falls to about 0.44. Against a stronger incumbent the optimal test is more informative, and entry under it falls. The paper's reversal does not survive costless disclosure. The disclosure ceiling is 9.97, against 3.99 for the market. The investor still trades after disclosure; the trade stops mattering for entry.

Toehold next. A public stake widens the window of the reversal and moves the information ceiling out. It breaks the reversal only at a stake of 0.48 or more. A stake bought at the fair price before the cost is known has no value. A hidden unit bought by the low-cost challenger always pays, and it leaves entry unchanged. The challenger's trade reveals its cost, not its class.

Limits: some priors have no pure equilibrium, bids stay truthful, and welfare is not computed.
