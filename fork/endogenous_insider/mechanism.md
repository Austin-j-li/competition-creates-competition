---
title: "Fork: the endogenous insider"
subtitle: "Deterministic preparation cost, no participation floor"
author: "Austin Li"
date: "2026-09-07"
---

This note is a fork of the benchmark model in `paper/main.md`. It is not part of the manuscript. It records a modification suggested at a supervisory meeting on 2026-09-07. One deterministic preparation cost replaces the stochastic one, and equilibrium rather than assumption settles whether the investor's knowledge is information about the target. Everything below uses the notation of the paper. Equation numbers such as (4) and (A.5) refer to `paper/main.md`; results labeled F.1 to F.5 are new to this note. Each result carries its status in the paper's vocabulary.

## 1. What changes and why

In the benchmark the challenger's preparation cost is $c_L$ with probability $\rho$ and $c_H$ otherwise, and condition (A1) makes the low-cost type prepare at every feasible belief. That type does one specific job. It guarantees that the target's terminal value depends on the challenger's quality $\theta$ at every price, which is what makes the investor's knowledge of $\theta$ material for the stock. Section 4.1 of the paper says as much: without the floor, "nobody prepares, proceeds do not depend on challenger quality, and the investor has nothing to trade on." The high-cost type does the other job. It is the margin that responds to the price.

The fork keeps the margin and removes the floor. There is one cost $c>0$, known to everyone. The challenger prepares at a price if and only if its posterior gross profit covers $c$. On flows where it would not prepare, the target is worth $t_0$ in both states, the price is $t_0$, and the investor's knowledge of $\theta$ is not information about the security there. Whether the investor is an insider is then an equilibrium outcome. This is the structure of @DowGoldsteinGuembel2017, in which information about a project is worth producing only if the firm will act on the price. Here the real decision is a rival's participation in a takeover contest.

The fork changes four things and leaves the rest of the paper intact.

1. The dead outcome, with no trade, a constant price, and no entry, is an equilibrium at every incumbent strength on the relevant domain. No parameter choice removes it.
2. Live equilibria, with informed orders, an informative price, and positive entry, exist on a middle range of strengths. They come in a family indexed by how much of the flow pools at the no-entry price.
3. The fork loses uniqueness at the strong incumbent, part (ii) of Proposition 2. The global bound (A.6) needs a residual bounded away from zero, and the residual is now zero on the pool.
4. Price sufficiency, Proposition A.2, holds on the entry region and fails on the pool. The pool is one price atom, and the challenger's belief there is the pool average.

The benchmark is the fork with a vanishing floor. Proposition F.5 makes this precise. As $\rho\to0$ the benchmark's informative equilibrium converges to the fork's minimal-pool live equilibrium, the benchmark's no-trade equilibrium survives at every strength, and the benchmark's uniqueness bound (A3) fails for every fixed $k$. The floor is a selection device.

## 2. Model

Values, the sale rule, trading, noise, and pricing are those of Section 2 of the paper, with $0<p<\ell<r<h$, incumbent value uniform on $[0,r]$, challenger quality $\theta\in\{\ell,h\}$ with equal priors, orders $q\in[-1,1]$, linear trading cost $k>0$, Laplace noise with scale $b>1$, and competitive pricing $P(X)=\mathbb E[V_T\mid X]$. The one change is the preparation cost. It is a constant $c>0$, common knowledge, paid after the challenger observes the price. I keep the tie rule, so an indifferent challenger prepares.

Acquisition payoffs $t_0,t_H,t_L,g_H,g_L$ and the spread $\Delta_T$ come from (4), with $w_L=t_L-t_0>0$. Gross profit at belief $\mu$ is $B_r(\mu)=g_L+\mu(g_H-g_L)$. The preparation threshold belief is

$$
\tau=\frac{c-g_L}{g_H-g_L},
\qquad
\tau>\tfrac12\iff B_r(\tfrac12)<c,
\qquad
\tau\le M\iff c\le B_r(M).
\tag{F.1}
$$

The posterior bounds $m\le\mu_X\le M$ of Proposition A.1 hold for arbitrary mixed orders, because that proposition uses only the noise density.

## 3. Equilibrium

An equilibrium is a tuple $(\sigma_H,\sigma_L;P;\mu_P;e)$: conditional order distributions, a measurable price function of flow, a belief $\mu_P(\pi)=\Pr(H\mid P(X)=\pi)$ at every realized price including atoms, and a preparation rule $e(\pi)=\mathbf 1\{B_r(\mu_P(\pi))\ge c\}$, such that the price is competitive given $e$ and each investor type's order is optimal against the fixed schedule $(P,e)$. Write $e(x)$ for $e(P(x))$, $A=\{x:e(x)=1\}$ for the entry set, and $N$ for its complement, the pool. I evaluate unilateral deviations against the fixed schedule, as in Section 2.3 of the paper.

**Lemma F.1 (structure of prices and entry; analytical).** *In every equilibrium:*

*(a) $P(x)=t_0$ on $N$ and $P(x)=t_L+\Delta_T\,\mu_X(x)$ on $A$.*

*(b) Every price on $A$ exceeds $t_0$. The pool $N$ is the preimage of the single price $t_0$, and on $A$ the price reveals $\mu_X$. Hence $\mu_P=\mu_X$ on $A$ and $\mu_P(t_0)=\bar\mu_N:=\Pr(H\mid X\in N)$.*

*(c) $A\subseteq\{x:\mu_X(x)\ge\tau\}$, and if $\Pr(X\in N)>0$ then $\bar\mu_N<\tau$.*

*(d) The residual advantages are $A_H(x)=\mathbf 1_A(x)\,\Delta_T[1-\mu_X(x)]$ and $A_L(x)=\mathbf 1_A(x)\,\Delta_T\,\mu_X(x)$. Both lie in $[0,\Delta_T]$ and vanish on $N$.*

*Proof.* On $N$ nobody prepares, so $V_T=t_0$ in both states and the competitive price is $t_0$. On $A$ the challenger prepares, $V_T=t_\theta$, and $P=t_0+w_L+\Delta_T\mu_X$. Since $t_L+\Delta_T\mu_X\ge t_L+\Delta_T m>t_L>t_0$, no price on $A$ equals $t_0$, and since $\mu\mapsto t_L+\Delta_T\mu$ is injective, two flows in $A$ share a price if and only if they share a posterior. The price partition on $A$ is the $\mu_X$ partition, so $\mu_P=\mathbb E[\mu_X\mid P]=\mu_X$ there by the tower property, exactly as in the inversion step of Proposition A.2. At $t_0$ the belief is the pool average. Part (c) is the preparation rule at each price under the tie rule. Part (d) subtracts the price from $\mathbb E[V_T\mid\theta,x]=t_0+e(x)(t_\theta-t_0)$ as in the residual step of Proposition A.2, with $e\in\{0,1\}$. $\square$

The one place the fork departs from the paper is (b). Proposition A.2 inverts the price on the whole flow line because $e\ge\rho>0$ everywhere. Here the inversion is available only on $A$. The pool is an information set of its own.

## 4. Results

### 4.1 The dead equilibrium and the flat regions

Let $\mathcal D$ denote the profile with zero orders, constant price $t_0$, belief $\tfrac12$ at that price, and no preparation.

**Proposition F.1 (dead equilibrium; flat regions; analytical).**

*(i) $\mathcal D$ is an equilibrium if and only if $B_r(\tfrac12)<c$.*

*(ii) Every equilibrium without entry is $\mathcal D$.*

*(iii) If $B_r(M)<c$, then $\mathcal D$ is the unique equilibrium.*

*(iv) If $\Delta_T(r)<k$ and $B_r(\tfrac12)<c$, then $\mathcal D$ is the unique equilibrium. The first inequality holds exactly when $r<\mathfrak r(k)$, with $\mathfrak r$ as in (A.10).*

*In cases (iii) and (iv) the investor knows $\theta$, does not trade, the price is constant, and $\theta$ is not information about $V_T$.*

*Proof.* (i) Under $\mathcal D$, $V_T\equiv t_0=P$, so an order $q$ earns $-k|q|$, and zero is the unique best response. Zero orders give $X=Z$, one price, and belief $\tfrac12$. No preparation is optimal at that belief if and only if $B_r(\tfrac12)<c$; at equality the tie rule forces preparation.

(ii) Without entry, $V_T\equiv t_0$, so $P\equiv t_0$ by competitive pricing, zero orders are uniquely optimal, the belief at the only price is $\tfrac12$, and consistency of non-preparation requires $B_r(\tfrac12)<c$. This is $\mathcal D$.

(iii) By Lemma F.1(c), $A\subseteq\{\mu_X\ge\tau\}$. If $B_r(M)<c$ then $\tau>M\ge\mu_X$ under every strategy, so $A$ is null and (ii) applies. Since $B_r(M)<c$ implies $B_r(\tfrac12)<c$, $\mathcal D$ exists.

(iv) By Lemma F.1(d), a correctly signed order of magnitude $s$ earns at most $s(\Delta_T-k)<0$ against every candidate schedule, and a wrong-signed order has nonpositive gross payoff and pays its cost. Zero orders are therefore the unique best response for both types, $\mu_X\equiv\tfrac12$, and $A\subseteq\{\tfrac12\ge\tau\}$ is empty because $\tau>\tfrac12$. Apply (ii). Solving $\Delta_T(r)=k$ gives $\mathfrak r(k)$ as in the proof of Proposition A.4. $\square$

These are the two flat regions. Below $\mathfrak r(k)$ the trading cost is what keeps $\theta$ immaterial. Trading on it could not pay even if the challenger were listening, so nobody trades, nobody listens, and nobody comes. Above $r_C$, where $B_r(M)=c$ as in (A.11) with $c_H$ replaced by $c$, the acquisition profit is what keeps it immaterial. No price the market can produce would bring the challenger in, so the investor's knowledge is about nothing the stock pays. Both regions are flat at zero entry with no informed trading, which differs from part (iii) of Proposition 2, where entry is flat at $\rho$ and the investor still trades to its limit.

### 4.2 Live equilibria

**Proposition F.2 (live equilibria; analytical).** *Suppose $B_r(\tfrac12)<c\le B_r(M)$, so $\tau\in(\tfrac12,M]$.*

*(a) Cutoff family. Fix pure orders $q_H>q_L$ and write $M_q=(1+e^{-(q_H-q_L)/b})^{-1}$ for the largest posterior they can produce, so $M_q=M$ at full orders. Then $\mu_X$ is nondecreasing in $x$, and when $\tau\le M_q$ the set $\{\mu_X\ge\tau\}$ is a half-line $[x^*,\infty)$ with $x^*=x^*(q_H,q_L)$ finite. For every $x'\ge x^*$ the entry set $A=[x',\infty)$ with the price of Lemma F.1 satisfies the challenger's and the market maker's conditions. The pool posterior is*

$$
\bar\mu_{x'}=\Pr(H\mid X<x')=\frac{F_Z(x'-q_H)}{F_Z(x'-q_H)+F_Z(x'-q_L)}\le\tfrac12<\tau .
\tag{F.2}
$$

*The lower end $x'$ of the entry region is a free equilibrium object. The investor's optimality is the only condition that restricts it.*

*(b) Entry is bounded away from zero on the live family. In every equilibrium with entry, $\Delta_T\,e^{2/b}\max\{e_H,e_L\}\ge k$, where $e_\theta=\Pr(X\in A\mid\theta)$. The live family therefore does not reach $\mathcal D$ continuously.*

*(c) Existence with full orders and the minimal pool. Let $x^*=\tfrac b2\log\frac{\tau}{1-\tau}\in(0,1]$ and*

$$
J(r)=\Delta_T\int_{x^*}^{\infty}\frac{f(x-1)f(x+1)}{f(x-1)+f(x+1)}\,dx .
\tag{F.3}
$$

*If $k<(1-1/b)\,J(r)$, then orders $(q_H,q_L)=(1,-1)$, entry set $A=[x^*,\infty)$, price $t_0$ on $x<x^*$ and $t_L+\Delta_T\mu_X(x)$ on $x\ge x^*$, with $\mu_X$ as in (A.8), form an equilibrium. Entry and ownership are $e_H=\alpha_H$, $e_L=\alpha_L$, $\mathsf E=(\alpha_H+\alpha_L)/2>0$, and $\mathsf O_H=\alpha_H/2$, with $\alpha_H,\alpha_L$ as in (12).*

*(d) Under the hypotheses of (c), $\mathcal D$ is also an equilibrium.*

*Proof.* (a) For $q_H>q_L$ the likelihood ratio $f(x-q_H)/f(x-q_L)$ is nondecreasing in $x$, so $\mu_X$ is nondecreasing, equal to $1-M_q$ on $x\le q_L$ and to $M_q$ on $x\ge q_H$. The set $\{\mu_X\ge\tau\}$ is therefore a half-line, nonempty exactly when $\tau\le M_q$. When it is empty no flow can support preparation at those orders, and the only consistent profile is one without entry, which is $\mathcal D$ by Proposition F.1(ii). On $A=[x',\infty)$ with $x'\ge x^*$, every flow has $\mu_X\ge\tau$ and the price reveals it, so preparation is optimal. On the pool, $x'-q_H<x'-q_L$ gives $F_Z(x'-q_H)\le F_Z(x'-q_L)$ and hence (F.2); the pooled belief is below $\tfrac12<\tau$, so non-preparation is strictly optimal. Competitive pricing on each region is Lemma F.1(a).

(b) Against any candidate with entry set $A$, a correctly signed deviation of magnitude $s$ by the high type earns gross $F_H(s)=\int f(x-s)A_H(x)\,dx\le\Delta_T\int_A f(x-s)\,dx$. The ratio bound $f(x-s)/f(x-q)\le e^{|s-q|/b}\le e^{2/b}$ holds for every pair of feasible orders, so integrating it against the candidate's conditional order distribution gives $f(x-s)\le e^{2/b}a_H(x)$ and $\int_A f(x-s)\,dx\le e^{2/b}e_H$, where $e_H=\int_A a_H(x)\,dx$; mixed orders are covered. So if $\Delta_T e^{2/b}e_H<k$, every nonzero order of the high type loses and its unique best response is zero; likewise for the low type with $e_L$. If both best responses are zero, then $\mu_X\equiv\tfrac12<\tau$ and $A$ is null, contradicting entry.

(c) Challenger and market maker: part (a) with $x'=x^*$. For the investor, the residuals of Lemma F.1(d) are nonnegative, bounded, and measurable. The translation identity (A.5) and the bound $|F_\theta'|\le F_\theta/b$ use only boundedness and nonnegativity of the residual and the Laplace density, so they hold here. Under full orders and $A=[x^*,\infty)$,

$$
F_H(1)=\Delta_T\int_{x^*}^\infty f(x-1)[1-\mu_X]\,dx
=\Delta_T\int_{x^*}^\infty\frac{f(x-1)f(x+1)}{f(x-1)+f(x+1)}\,dx=J,
$$

and $F_L(1)=\Delta_T\int_{x^*}^\infty f(x+1)\mu_X\,dx=J$ as well. The ratio bound $f(x-s)/f(x-1)\ge e^{-(1-s)/b}$ for $s\in[0,1]$ gives $F_\theta(s)\ge e^{-(1-s)/b}J$, so

$$
U_\theta'(s)=F_\theta(s)+sF_\theta'(s)-k\ge\Big(1-\frac sb\Big)e^{-(1-s)/b}J-k\ge\Big(1-\frac1b\Big)J-k>0
$$

on $[0,1]$, because $(1-s/b)e^{-(1-s)/b}$ decreases on $[0,1]$ when $b>1$. The full correctly signed order dominates every smaller magnitude; wrong-signed orders have nonpositive gross payoff and pay their cost; mixtures average. This is the existence test (A.7) of the paper applied to a residual that vanishes on the pool. Under full orders $\mu_X=\operatorname{logistic}(2x/b)$ on $(-1,1)$, so $\mu_X=\tau$ at $x^*=\tfrac b2\log\frac{\tau}{1-\tau}$, which lies in $(0,1]$ because $\tau\in(\tfrac12,M]$; at $\tau=M$ the entry set is the plateau $x\ge1$, an atom on which the tie rule admits preparation. The tail probabilities are those of (12).

(d) is Proposition F.1(i). $\square$

Two remarks. First, there is no analog of the global bound (A.6). That bound integrates a residual lower bound $\rho m\Delta_T$ over the whole order interval, and the residual is now zero on a set of positive probability. The fork therefore has no uniqueness argument for full orders at the strong incumbent, and (d) shows the claim itself is false. Second, (b) explains the shape of the cutoff family in the numerical section. As the pool grows, entry and the investor's profit fall together until the investor's incentive breaks, and the family then jumps to $\mathcal D$ rather than sliding into it.

### 4.3 Competition creates the insider

**Proposition F.3 (competition creates the insider; analytical).** *Fix $0<p<\ell<h$, $b>1$, $k>0$, $c>0$, and strengths $\ell<r_0<r_1<h$ with*

$$
\Delta_T(r_0)<k,\qquad B_{r_0}(\tfrac12)<c,
\tag{F.4}
$$

$$
B_{r_1}(\tfrac12)<c<B_{r_1}(M),\qquad k<\Big(1-\frac1b\Big)J(r_1).
\tag{F.5}
$$

*(i) With the weak incumbent $r_0$, the unique equilibrium is $\mathcal D$: no informed trading, a constant price, no preparation, and $\theta$ is not information about the target's value.*

*(ii) With the strong incumbent $r_1$, there is an equilibrium with full informed orders $(1,-1)$, a price experiment that strictly Blackwell dominates the constant experiment, preparation probability $(\alpha_H+\alpha_L)/2>0$, and high-value ownership $\alpha_H/2>0$. The dead equilibrium $\mathcal D$ coexists with it.*

*(iii) For any $r_2\in(r_1,h)$ with $B_{r_2}(M)<c$, the unique equilibrium is again $\mathcal D$.*

*The set of primitives satisfying (F.4) and (F.5) is nonempty and open.*

The benchmark vector $(h,\ell,p,b,k)=(10,1,0.5,2,0.02)$ with $c=6$ and $(r_0,r_1,r_2)=(1.2,3,3.6)$ satisfies (F.4), the belief inequalities in (F.5), and the ceiling condition of (iii) by closed-form arithmetic. The remaining inequality $k<(1-1/b)J(3)$ holds by quadrature of $J$. That part of the benchmark verification is a numerical diagnostic until $J(3)$ is enclosed by interval arithmetic, which is open item 1.

*Proof.* (i) is Proposition F.1(iv). (ii) is Proposition F.2(c) and (d); the Blackwell comparison is the argument of Step 6 in the proof of Proposition 2, since the live price is a nonconstant function of flow whose law depends on $\theta$ and the constant price is its garbling by a constant kernel, while no state-independent kernel turns a constant into a state-dependent law. (iii) is Proposition F.1(iii).

Nonemptiness. Since $B_r(\tfrac12)$ and $B_r(M)$ both decrease in $r$ and (A.25) gives $B_\ell(M)>B_\ell(\tfrac12)$, choose $r_1$ close enough to $\ell$ that $B_{r_1}(M)>B_\ell(\tfrac12)$, and choose $c\in(B_\ell(\tfrac12),B_{r_1}(M))$. Then $B_{r_0}(\tfrac12)<B_\ell(\tfrac12)<c<B_{r_1}(M)$ for every $r_0\in(\ell,r_1)$, and $B_{r_1}(\tfrac12)<B_\ell(\tfrac12)<c$. The entry set at $r_1$ has positive Lebesgue measure and $\Delta_T(r_1)>0$, so $J(r_1)>0$; choose $k\in(0,(1-1/b)J(r_1))$. Finally $\Delta_T(r)\to0$ as $r\to\ell$, so $r_0$ close enough to $\ell$ satisfies $\Delta_T(r_0)<k$. All inequalities are strict and continuous in the primitives, so the set is open. For the benchmark vector: $\Delta_T(1.2)=0.0167<0.02$; $B_{1.2}(\tfrac12)=4.80<6$; $B_3(\tfrac12)=4.29<6<6.217=B_3(M)$; $J(3)=0.0955$ by quadrature, so $(1-1/b)J(3)=0.048>0.02$; and $B_{3.6}(M)=5.997<6$. $\square$

The proposition says something different from Proposition 2. In the paper, competition switches the unique outcome from an uninformative price to an informative one. In the fork, competition creates the possibility of information. At $r_0$ no equilibrium contains an insider. At $r_1$ one does, and it coexists with one that does not. Whether "competition creates competition" or only "competition permits competition" is the right headline depends on what selects between them, which is the subject of Section 6.

### 4.4 Deterrence at a fixed experiment

**Proposition F.4 (deterrence at a fixed experiment; analytical).** *Hold a signal experiment $(S,\Theta)$ fixed as $r$ changes and let the cost be $c$. Entry is weakly decreasing in $r$, and strictly decreasing when $B_{r_1}(\mu(S))<c\le B_{r_0}(\mu(S))$ on a set of positive probability.*

*Proof.* The indicator identity (A.9) with $C\equiv c$. $\square$

This is Proposition A.3 with one cost, and it does more work in the fork than in the paper. Once orders reach their bounds, the experiment is fixed, and F.4 says entry falls in $r$ along the live branch. The numerical section shows exactly that. On the full-order segment entry declines from the point where orders reach $(1,-1)$ to the ceiling $r_C$. The rise happens only on the segment where the low type's short is still growing and the experiment is improving. Competition creates the insider; once the insider exists, more competition deters, as the fixed-information benchmark says it should.

### 4.5 The benchmark is the fork with a vanishing floor

**Proposition F.5 (vanishing floor; analytical).** *Take the benchmark model with $c_H=c$, a low cost $c_L<B_r(m)$, and floor $\rho\in(0,1)$. Fix $r$ with $B_r(\tfrac12)<c<B_r(M)$.*

*(a) If the fork's existence test $k<(1-1/b)J(r)$ holds, then the benchmark's full-order existence test (A.7) holds for every $\rho$, because its statistic is $J_\rho=J+\rho\Delta_T\int_{-\infty}^{x^*}\frac{f(x-1)f(x+1)}{f(x-1)+f(x+1)}dx\ge J$. The benchmark's full-order price is*

$$
P_\rho(x)=
\begin{cases}
t_0+\rho\,[w_L+\Delta_T\mu_X(x)],&x<x^*,\\
t_L+\Delta_T\mu_X(x),&x\ge x^*,
\end{cases}
$$

*which is strictly increasing in the posterior, so no two flows with distinct posteriors share a price. As $\rho\to0$ it converges pointwise to the fork's minimal-pool price, and benchmark entry $\rho+(1-\rho)(\alpha_H+\alpha_L)/2$ converges to $(\alpha_H+\alpha_L)/2$. The floor's separating price below $x^*$ pins the pool's lower end at $x^*$, so the benchmark selects the minimal-pool member of the fork's cutoff family.*

*(b) The benchmark's no-trade equilibrium exists exactly when $r\le r_N(\rho)=\mathfrak r(2k/\rho)$ by Proposition A.4, and $r_N(\rho)\to\infty$ as $\rho\to0$. The fork's dead equilibrium is its limit. The floor removes it only for $r>r_N(\rho)$.*

*(c) The benchmark's sufficient uniqueness condition for full orders, $k<(1-1/b)\rho m\Delta_T(r)$ in (A3), fails for every fixed $k>0$ once $\rho<k/[(1-1/b)m\Delta_T(r)]$. The uniqueness region of Proposition 2(ii) is empty in the limit.*

*Proof.* (a) With $e_\rho(x)=\rho+(1-\rho)\mathbf 1\{x\ge x^*\}$ the paper's statistic (A.7) is $\Delta_T\int e_\rho\,f(x-1)f(x+1)/(f(x-1)+f(x+1))\,dx$, which splits into $J$ and the stated $\rho$ term. The price is (9) with that entry rule, and its monotonicity is (A.3). Pointwise convergence is immediate. (b) and (c) read off Proposition A.4 and (A3). $\square$

The interpretation matters for how the paper reads. The benchmark's uniqueness at the strong incumbent is a property of the floor. The low-cost type is a small exogenous reason for the stock to depend on $\theta$ at every price, and that small reason removes both the pooling multiplicity and, above $r_N(\rho)$, the dead equilibrium. The paper already calls the floor "part of the mechanism, not a numerical regularizer." The fork sharpens that sentence. The floor is the assumption that the investor is an insider. The fork asks what happens without that assumption.

## 5. What is information in this setup

Three objects get called information, and the fork separates them.

The first is the investor's signal, $\theta$. It is exogenous in the paper and in the fork. The investor knows the challenger's acquisition value.

The second is materiality, whether $V_T$ depends on $\theta$. A person with material nonpublic information about a security is an insider. In the paper, the floor guarantees materiality at every price. In the fork, $V_T$ depends on $\theta$ only on the entry set, and the entry set is chosen by a challenger who reads the price that the investor's own trading produces. Materiality is an equilibrium outcome. The same investor with the same signal is an insider in a live equilibrium and a bystander in the dead one. In the two flat regions, the investor is a bystander in every equilibrium.

The third is the informativeness of the price about $\theta$, the Blackwell object the paper studies. In the fork it is zero in $\mathcal D$, positive in every live equilibrium, and declining along the cutoff family as more of the flow pools.

The paper fixes the second object and studies the third. The fork makes the second endogenous, and then materiality, price informativeness, and participation are one fixed point. Competition enters through the second object. A stronger incumbent raises $\Delta_T$, the amount by which $V_T$ would depend on $\theta$ if the challenger came, and so raises the return to being an insider conditional on the challenger listening. Below $\mathfrak r(k)$ that return cannot cover the cost of trading, so nobody becomes an insider. Above $r_C$ the challenger will not listen at any price, so there is nothing to be an insider about.

## 6. Selection

Both $\mathcal D$ and the full-order live equilibrium are strict. In $\mathcal D$ every deviation loses $k|q|$, and in the live equilibrium $U_\theta'>0$ on the whole order interval. This is a coordination problem between two strict equilibria, and a best-response dynamic does not select one. Numerically, best-response iteration reaches the live profile only from starts near full orders. At $r=3$, of the five correctly signed starts in the solver, only $(1,-1)$ reaches it and the other four converge to $\mathcal D$; at $r=2$ and $r=1.66$, two of the five do. The basin of $\mathcal D$ is large. That describes basins rather than stability, and it is not evidence for the live equilibrium.

Payoffs rank them. The investor strictly prefers the live equilibrium, where it earns $U_\theta(1)>0$ against zero. The seller strictly prefers it, with expected proceeds $t_0+\tfrac12\sum_\theta e_\theta(t_\theta-t_0)>t_0$. The challenger strictly prefers it ex ante, earning $\mathbb E[(B_r(\mu_X)-c)_+]>0$ because $\mu_X>\tau$ with positive probability when $\tau<M$. At $\tau=M$ the entry set is the plateau, its profit there is exactly $c$, and it is indifferent. Market makers break even in both. Noise traders lose in the live equilibrium what the investor gains. Among the strategic players, the live equilibrium dominates.

The vanishing floor of Proposition F.5 is a perturbation argument. Any small exogenous reason for $V_T$ to depend on $\theta$ at every price selects the minimal-pool member of the cutoff family, because it makes the price separate flows inside what would otherwise be the pool. It does not remove $\mathcal D$ in the limit. The strongest selection statement the perturbation supports is the minimal pool among live equilibria. The choice between live and dead needs a different argument, or it stands as the content of the result. My own view is the latter. "A stronger incumbent makes an equilibrium with an insider possible where none existed" is a true and bold statement, and it is the fork's theorem.

The reserve appendix of the paper already contains the same multiplicity in the reserve game, Proposition A.10. It already treats orders, pools, beliefs, and preparation as a joint object, and it cites @DowGoldsteinGuembel2017 for continuations distinguished by pooling regions. The fork moves that structure from an appendix example into the benchmark.

## 7. Numerical illustration

The solver `solve.py` uses the benchmark primitives with $\rho=0$ and $c=6$, a flow grid of 60,001 points on $[-30,30]$, an order grid of step $0.01$ refined to $0.0005$, and best-response iteration from five correctly signed starts. I check the dead profile from Proposition F.1(i). Every live row is a pure-strategy fixed point of the best-response map on the grid, and the solver verifies the pool consistency of Lemma F.1(c) at each one. Status: numerical diagnostic. I did not search mixed or wrong-signed profiles. The outputs are `branches.csv`, `cutoff_family.csv`, and `thresholds.csv`, and `render.py` draws the figure `entry_fork.pdf` from those files.

Thresholds on the benchmark vector:

| Object | Value | Source |
|---|---|---|
| $\mathfrak r(k)$, below which $\mathcal D$ is unique | 1.2210 | Proposition F.1(iv), closed form |
| $r_C$, above which $\mathcal D$ is unique | 3.5927 | Proposition F.1(iii), closed form (A.11) with $c_H\to c$ |
| $\sup_r B_r(\tfrac12)$ on $(\ell,h)$ | 4.875 | below $c=6$, so $\mathcal D$ exists at every $r$ |
| first grid strength with a live fixed point | 1.66 | numerical diagnostic |
| first grid strength where $k<(1-1/b)J(r)$ | 2.05 | Proposition F.2(c) test by quadrature of $J$; numerical diagnostic |

The live branch:

| $r$ | orders $(q_H,q_L)$ | $\mathsf E$ | $\mathsf O_H$ | investor profit $U_H$, $U_L$ | status |
|---|---|---|---|---|---|
| 1.65 | none found | 0 | 0 | | only $\mathcal D$ found |
| 1.66 | $(1,-0.25)$ | 0.384 | 0.250 | 0.0029, 0.0007 | numerical diagnostic |
| 1.80 | $(1,-0.65)$ | 0.391 | | | numerical diagnostic |
| 2.00 | $(1,-0.98)$ | 0.394 | 0.286 | 0.0192, 0.0189 | numerical diagnostic |
| 2.05 | $(1,-1)$ | 0.393 | 0.286 | 0.0219, 0.0219 | sufficient test holds |
| 3.00 | $(1,-1)$ | 0.364 | 0.266 | 0.0755, 0.0755 | sufficient test holds, margin $0.0477$ vs $k=0.02$ |
| 3.5926 | $(1,-1)$ | 0.342 | 0.250 | 0.1058, 0.1058 | sufficient test holds |
| 3.5927 | none | 0 | 0 | | above $r_C$, $\mathcal D$ unique |

For comparison, the paper's benchmark has entry $0.250$ at $r_0=1.2$ and $0.523$ at $r_1=3$. The fork's live entry at $r_1$ is $0.364=(0.523-0.25)/0.75$, the benchmark's expensive-type entry conditional on being the expensive type, as Proposition F.5(a) says it must be.

The cutoff family at $r=3$ under full orders:

| pool lower end $x'$ | orders | $\mathsf E$ | $U_H$, $U_L$ |
|---|---|---|---|
| 0.872 (minimal pool; exact $x^*=0.8712$) | $(1,-1)$ | 0.363 | 0.0754, 0.0754 |
| 1.522 | $(1,-1)$ | 0.263 | 0.049, 0.049 |
| 2.522 | $(1,-1)$ | 0.160 | 0.022, 0.022 |
| 3.022 | $(1,-0.84)$ | 0.127 | 0.015, 0.012 |
| 3.222 | $(1,-0.76)$ | 0.117 | 0.012, 0.009 |
| 3.272 and above | collapses to $\mathcal D$ | 0 | 0, 0 |

Entry falls by two thirds across the family before the investor's incentive breaks, and the family ends with a jump to zero, as Proposition F.2(b) says it must. The bound itself is loose. At $r=3$ it only forces $\max\{e_H,e_L\}\ge0.011$, and the observed collapse happens from entry $0.117$. Every member is an equilibrium of the same economy at the same orders on most of the range. This is the multiplicity the paper's Section 6.3 describes for the reserve game, now in the benchmark.

The figure has two panels. Panel (a) shows entry across strengths, with the fork's dead branch at zero, its live branch, the paper's validated benchmark branches overlaid for comparison, and the two flat regions shaded. Panel (b) shows the cutoff family at $r=3$.

## 8. What the fork gives up, and what it gains

Given up. Uniqueness at the strong incumbent, and with it the sentence "the unique equilibrium trading outcome is $(1,-1)$." Price sufficiency on the whole flow line. The certified asymmetric equilibria of Proposition 3, which I would have to recompute without the floor; the numerical branch on $[1.66,2.0]$ suggests they survive, but I have no certificate. The welfare comparison of Proposition A.9 changes character. Hiding the price now yields $\mathcal D$, and the comparison is between the unique equilibrium of one game and a selected equilibrium of the other.

Gained. Two fewer parameters, $\rho$ and $c_L$. A theorem about the existence of an insider rather than about the level of entry. A non-monotonicity with a clean account. The live branch appears with positive entry, entry rises while the low type's short is still growing, falls once orders are at their bounds by Proposition F.4, and dies at $r_C$ by Proposition F.1(iii). And an answer to the question of what information is in this model, which the paper's floor currently answers by assumption.

## 9. Open items

1. A certified enclosure of $J(r_1)$, which is one interval integral, would make Proposition F.3(ii) computer-assisted rather than dependent on quadrature at the benchmark.
2. I did not search whether mixed or wrong-signed profiles support additional live equilibria.
3. Endogenous information acquisition by the investor, paying to learn $\theta$, would make the complementarity two-sided as in @DowGoldsteinGuembel2017 and might change the selection discussion.
4. The seller's reserve choice in the fork. With the pool in the benchmark, the continuation correspondence of Appendix A.7 is the object at every reserve, not only above $\ell$.
5. If I adopt the fork into the paper, the paragraphs to rewrite are the abstract's uniqueness sentence, the introduction's fourth and fifth paragraphs, the (A1) discussion in Section 4.1, Proposition 2(ii), Section 4.2's controls, and Section 6.1.
