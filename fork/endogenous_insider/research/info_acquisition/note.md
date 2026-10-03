---
title: "Information acquisition in the endogenous-insider fork"
subtitle: "Track: info_acquisition (open item 3 of the fork note)"
date: "2026-10-03"
---

This note extends `fork/endogenous_insider/mechanism.md`. It uses the notation of `paper/main.md` and of the fork note. Equation numbers such as (4), (12), (A.6) refer to the paper. Labels F.1 to F.5 refer to the fork note. New results carry the labels G.1 to G.7. Each result carries its status in the paper's vocabulary: analytical, computer-assisted, numerical diagnostic, or open. Nothing here is part of the manuscript or of its numerical contract.

## 1. Question

In the fork, the investor knows $\theta$ for free. Whether that knowledge is material for the target stock is an equilibrium outcome. This note makes the knowledge itself a choice. The investor must pay $\kappa>0$ to learn $\theta$ before it trades. An investor who does not pay does not know $\theta$. The word "insider" then has two layers. The investor must acquire the signal, and the signal must be material. The note asks four things.

1. What is the equilibrium set of the acquisition game? When does the dead equilibrium exist? When do live equilibria exist? Are there mixed-acquisition equilibria, and are they stable?
2. What is the insider region in the $(r,\kappa)$ plane at the benchmark primitives? Is its upper edge hump-shaped in $r$, as deterrence (Proposition F.4) might suggest?
3. Does the two-sided complementarity of @DowGoldsteinGuembel2017 create new multiplicity, a new selection argument, or a theorem stronger than Proposition F.3?
4. When is the investor an insider? The note separates "knows $\theta$", "$\theta$ is material", and "chooses to learn $\theta$".

## 2. Headline result

Competition is necessary for information production at every cost of information, and it is sufficient for the existence of information production below an explicit cost ceiling. At every strength outside $(\mathfrak r(k),r_C]$ the investor does not learn $\theta$ at any $\kappa>0$, because its knowledge could not be material. [Referee fix: the interval was written $(\mathfrak r(k),r_C)$. At $r=r_C$ itself $\tau=M$, the plateau entry set is admitted by the tie rule, and Proposition G.2(i) gives an acquisition equilibrium for $\kappa\le U^*(r_C)=0.1058$.] Inside, an equilibrium with acquisition exists whenever $\kappa\le U^*(r)$ [Referee fix: the original said "exactly when". Only sufficiency is proved. The exact ceiling over all continuations is open (Section 4.3), and $\bar U(r)$ of Proposition G.2(iv) is the only proved necessary bound.], and on the full-order segment $U^*(r)=J(r)-k$ has a closed form that increases in $r$ up to the ceiling $r_C$ and then drops to zero: the insider region is a ramp with a cliff, not a hump. Acquisition adds a dilution floor $\lambda_{\min}(r)$: the challenger listens to no price unless it believes the investor is informed with probability at least $\lambda_{\min}(r)$, which rises from $0.69$ to $1$ across the full-order range $[2.02,r_C]$ at the benchmark [Referee fix: the original said "across the live range"; the grid live range starts at $r=1.66$, where $\lambda_{\min}=0.63$]. On the minimal-pool full-order branch, mixed-acquisition equilibria exist only for $\kappa$ in a band of width $0.0005$ to $0.004$ just below $U^*(r)$, and they are repellers (numerical diagnostic). [Referee fix: the original sentence had no branch qualifier. Larger pools support mixed-acquisition equilibria at much lower costs, for example $\kappa=0.035$ at $r=3$, $\lambda=0.95$, pool cutoff $x'=2$ (referee check, numerical diagnostic), and the author's own partial-order grid nodes at $r=2.05$ give $\kappa$ down to $0.0191$.] Under a stated forward-induction restriction, observable acquisition selects the live equilibrium, and a higher cost selects a smaller pool [Referee fix: the restriction is stated, not derived from a standard refinement; see open item 5].

## 3. Model changes

The economy is the fork's: values and the sale rule of Section 2 of the paper, one preparation cost $c$, orders $q\in[-1,1]$, trading cost $k$, Laplace noise with scale $b>1$, competitive pricing. The fork's domain assumption $B_r(\tfrac12)<c$ holds throughout unless a result says otherwise. Two things change.

**Acquisition.** Before trading, the investor chooses whether to pay $\kappa>0$ and learn $\theta$. The choice may be mixed. Write $\lambda\in[0,1]$ for the probability that it acquires. The choice is private: market makers and the challenger do not see it. An investor who acquires learns $\theta$ and submits an order from $\sigma_\theta$. In the main game, game A, an investor who does not acquire submits no order. Section 4.5 treats game B, in which a non-acquirer may trade.

**Timing.** The seller announces the sale rule. The investor chooses acquisition. If it acquired, it learns $\theta$ and trades. Market makers see the flow $X=q+Z$ (or $X=Z$ if there was no order) and set $P=\mathbb E[V_T\mid X]$. The challenger sees $P$ and prepares if and only if $B_r(\mu_P)\ge c$. Prepared bidders bid truthfully.

**Beliefs.** With acquisition probability $\lambda$, the conditional flow densities are

$$
a^\lambda_\theta(x)=\lambda\int f(x-q)\,d\sigma_\theta(q)+(1-\lambda)f(x),
\qquad
\mu^\lambda_X(x)=\frac{a^\lambda_H(x)}{a^\lambda_H(x)+a^\lambda_L(x)}.
\tag{G.1}
$$

The second term is the flow of an investor who did not acquire. It is the same in both states, so it dilutes every posterior toward $\tfrac12$.

**Payoffs.** Against a fixed schedule $(P,e)$, an informed type $\theta$ that submits $q$ expects $V_T=t_0+e(x)(t_\theta-t_0)$ at flow $x$, because it knows $\theta$ and knows that the flow is $q+Z$. Its profit is $q\int f(x-q)\,[\,t_0+e(x)(t_\theta-t_0)-P(x)\,]\,dx-k|q|$. Write $U_\theta$ for the supremum over $q$; the zero order is always available, so $U_\theta\ge0$. The value of acquisition is

$$
V=\tfrac12\,(U_H+U_L).
\tag{G.2}
$$

**Equilibrium.** A tuple $(\lambda;\sigma_H,\sigma_L;P;\mu_P;e)$ is an equilibrium if (E1) each $\sigma_\theta$ puts all mass on maximizers of the informed type's problem against $(P,e)$; (E2) $\lambda=1$ if $V>\kappa$, $\lambda=0$ if $V<\kappa$, and $\lambda$ is unrestricted if $V=\kappa$; (E3) $P$ is competitive given $(\lambda,\sigma)$; (E4) $\mu_P$ is Bayesian given $(\lambda,\sigma)$, with the pool average at a price atom, and $e(\pi)=\mathbf 1\{B_r(\mu_P(\pi))\ge c\}$. Unilateral deviations are evaluated against the fixed schedule, as in Section 2.3 of the paper. Write $\mathcal D$ for the profile with $\lambda=0$, no orders, $P\equiv t_0$, belief $\tfrac12$, and no preparation.

**Objects.** $M_\lambda$ is the largest posterior that any strategy can produce at acquisition probability $\lambda$, and $\lambda_{\min}(r)$ is the smallest $\lambda$ at which some posterior can reach $\tau$:

$$
M_\lambda=\frac{\lambda e^{1/b}+1-\lambda}{\lambda\,(e^{1/b}+e^{-1/b})+2(1-\lambda)},
\qquad
\lambda_{\min}(r)=\frac{2\tau-1}{(e^{1/b}-1)-\tau\,(e^{1/b}+e^{-1/b}-2)} .
\tag{G.3}
$$

## 4. Results

### 4.1 Two lemmas

**Lemma G.1 (dilution bound; analytical).** *Fix $\lambda\in[0,1]$. For arbitrary mixed orders, $1-M_\lambda\le\mu^\lambda_X\le M_\lambda$, and the price posterior obeys the same bounds. $M_\lambda$ is strictly increasing in $\lambda$, $M_0=\tfrac12$, and $M_1=M$. The upper bound is attained under full orders on $x\ge1$. Consequently a posterior can reach $\tau\in(\tfrac12,M]$ only if $\lambda\ge\lambda_{\min}(r)$, with $\lambda_{\min}$ as in (G.3), $\lambda_{\min}\in(0,1]$, and $\lambda_{\min}(r)=1$ exactly when $\tau=M$.*

*Proof.* For $|q|\le1$ the triangle inequality gives $\big||x-q|-|x|\big|\le1$, so $e^{-1/b}f(x)\le f(x-q)\le e^{1/b}f(x)$. Integrate against $d\sigma_H$ and $d\sigma_L$: $a^\lambda_H\le(\lambda e^{1/b}+1-\lambda)f$ and $a^\lambda_L\ge(\lambda e^{-1/b}+1-\lambda)f$. Hence $a^\lambda_H/a^\lambda_L\le R_\lambda:=(\lambda e^{1/b}+1-\lambda)/(\lambda e^{-1/b}+1-\lambda)$ and $\mu^\lambda_X\le R_\lambda/(1+R_\lambda)=M_\lambda$. The lower bound is symmetric. The price posterior is $\mathbb E[\mu^\lambda_X\mid P]$ by the tower property. Under full orders and $x\ge1$ all three densities are proportional to $e^{-x/b}$ and the bound holds with equality. Write $a=e^{1/b}$, $d=e^{-1/b}$, $u=a+d-2>0$, so $M_\lambda=(1+\lambda(a-1))/(2+\lambda u)$. The derivative has numerator $(a-1)(2+\lambda u)-(1+\lambda(a-1))u=2(a-1)-u=a-d>0$. Solve $M_\lambda=\tau$: $\lambda[(a-1)-\tau u]=2\tau-1$, and $(a-1)-\tau u\ge(a-1)-u=1-d>0$ for $\tau\le1$. At $\tau=M=a/(a+d)$ the ratio equals $1$. $\square$

**Lemma G.2 (structure at fixed $\lambda$; analytical).** *Lemma F.1 holds at every $\lambda$ with $\mu_X$ replaced by $\mu^\lambda_X$: the price is $t_0$ on the pool $N$ and $t_L+\Delta_T\mu^\lambda_X$ on the entry set $A$, the price reveals $\mu^\lambda_X$ on $A$, $A\subseteq\{\mu^\lambda_X\ge\tau\}$, and the informed residuals are $A_H=\mathbf 1_A\Delta_T(1-\mu^\lambda_X)$ and $A_L=\mathbf 1_A\Delta_T\mu^\lambda_X$. If the informed orders are pure with $q_H\ge0\ge q_L$ and $q_H>q_L$, then $\mu^\lambda_X$ is nondecreasing in $x$, so $\{\mu^\lambda_X\ge\tau\}$ is a half-line $[x^*_\lambda,\infty)$ when it is nonempty, and the pool posterior of every pool $(-\infty,x')$ is at most $\tfrac12<\tau$.*

*Proof.* The proof of Lemma F.1 uses competitive pricing, the form of $V_T$, and Bayes' rule at prices. None of these depends on $\lambda$; only the posterior formula changes. For monotonicity write $g_\theta(x)=f(x-q_\theta)/f(x)=\exp\{(|x|-|x-q_\theta|)/b\}$. For $q_H\ge0$ the exponent $|x|-|x-q_H|$ is nondecreasing in $x$; for $q_L\le0$ the exponent $|x|-|x-q_L|$ is nonincreasing. Then $a^\lambda_H/a^\lambda_L=(\lambda g_H+1-\lambda)/(\lambda g_L+1-\lambda)$ is nondecreasing. For the pool, $\int_{-\infty}^{x'}a^\lambda_H=\lambda F_Z(x'-q_H)+(1-\lambda)F_Z(x')\le\lambda F_Z(x'-q_L)+(1-\lambda)F_Z(x')=\int_{-\infty}^{x'}a^\lambda_L$ because $q_H>q_L$. $\square$

### 4.2 The dead equilibrium and the necessity of a live continuation

**Proposition G.1 (no acquisition; analytical).** *Assume $B_r(\tfrac12)<c$ and $\kappa>0$.*

*(i) $\mathcal D$ is an equilibrium, and it is strict: a deviation to acquisition earns $-\kappa$.*

*(ii) Every equilibrium with $\lambda=0$ is $\mathcal D$.*

*(iii) In every equilibrium with $\lambda>0$, the entry set has positive probability, $V\ge\kappa$ with equality when $\lambda<1$, and $\lambda\ge\lambda_{\min}(r)$. There is no equilibrium in which the investor learns $\theta$ and $\theta$ is immaterial.*

*(iv) If $B_r(M)<c$, or if $\Delta_T(r)<k$, then $\mathcal D$ is the unique equilibrium, for every $\kappa>0$.*

*Proof.* (i) Under $\lambda=0$ the flow is $Z$ in both states, so $\mu^0_X\equiv\tfrac12$, the price is one atom, the belief there is $\tfrac12$, and $B_r(\tfrac12)<c$ gives no preparation. Then $V_T\equiv t_0=P$. An investor who acquires faces this fixed schedule, so every order earns $-k|q|\le0$, $U_H=U_L=0$, and acquisition earns $-\kappa<0$. (ii) With $\lambda=0$ the schedule is the one in (i) whatever $\sigma$ is; (E1) then forces zero orders, which is $\mathcal D$. (iii) Suppose $\lambda>0$ and the entry set is null. Then $V_T=t_0=P$ almost surely, every order loses its cost, $V=0<\kappa$, and (E2) forces $\lambda=0$, a contradiction. So $A$ has positive probability. By Lemma G.2, $A\subseteq\{\mu^\lambda_X\ge\tau\}$, so $\sup\mu^\lambda_X\ge\tau$, and Lemma G.1 gives $M_\lambda\ge\tau$, which is $\lambda\ge\lambda_{\min}(r)$. The conditions on $V$ are (E2). (iv) If $B_r(M)<c$ then by Lemma G.1 $B_r(\mu_P)\le B_r(M)<c$ at every price under every $\lambda$, so no entry occurs, and (iii) forces $\lambda=0$; then (ii) applies. If $\Delta_T<k$, then by Lemma G.2 every informed residual lies in $[0,\Delta_T]$, so a correctly signed order of size $s$ earns at most $s(\Delta_T-k)<0$ and a wrong-signed order has nonpositive gross payoff; $U_H=U_L=0$, $V=0<\kappa$, $\lambda=0$, and (ii) applies. $\square$

The two flat regions of the fork survive, and they survive at every cost. Below $\mathfrak r(k)$ the trading cost blocks the use of the signal. Above $r_C$ the challenger would not listen to any price. In both cases the investor does not buy a signal it could not use. Part (iii) says more. In game A the three layers of the insider question coincide inside every equilibrium: the investor knows $\theta$ if and only if it trades on $\theta$, if and only if $\theta$ is material. The layers separate only across equilibria. [Referee fix: this holds at the level of the equilibrium ($\lambda>0$ if and only if the entry set has positive probability). It does not hold realization by realization. In a mixed equilibrium a non-acquirer's flow $Z$ lands in the entry set with positive probability, so $\theta$ is then material although nobody knows it.]

### 4.3 Pure acquisition and the shape of the insider region

Let $J(r)$ be the fork's statistic (F.3), the gross profit per unit of a full correctly signed order against the minimal-pool schedule at $\lambda=1$.

**Proposition G.2 (pure acquisition; analytical).** *Assume $B_r(\tfrac12)<c\le B_r(M)$ and $k<(1-1/b)J(r)$.*

*(i) For every $\kappa\le U^*(r):=J(r)-k$, the profile with $\lambda=1$ and the fork's live continuation of Proposition F.2(c) is an equilibrium. For $\kappa<U^*(r)$ it is strict in acquisition and in orders.*

*(ii) $J$ has the closed form*

$$
J(r)=\Delta_T(r)\left[\frac m2+\frac{e^{-1/b}}4\Big(\operatorname{gd}\tfrac1b-\operatorname{gd}\tfrac{x^*}{b}\Big)\right],
\qquad
\operatorname{gd}u=\arctan\sinh u,
\qquad
\sinh\frac{x^*}b=\frac{2\tau-1}{2\sqrt{\tau(1-\tau)}} .
\tag{G.4}
$$

*(iii) $J(r)\ge m\Delta_T(r)/2$ wherever $\tau\le M$. $J$ is differentiable in $r$ with*

$$
\frac{dJ}{dr}=\Delta_T(r)\left[\frac{r+\ell}{r(r-\ell)}\,G(\tau)-\frac{e^{-1/b}}{4\sqrt{\tau(1-\tau)}}\,\tau'(r)\right],
\qquad G(\tau):=\frac{J}{\Delta_T},
\tag{G.5}
$$

*and on an interval $[r_a,r_C]$ the derivative is positive whenever*

$$
\frac{r_C+\ell}{r_C(r_C-\ell)}\,\frac m2
\;>\;
\frac{e^{-1/b}}{4}\,2\cosh\tfrac1b\;
\frac{(\ell^2-p^2)/(2r_a^2)+M/2}{h-r_C/2-\ell^2/(2r_C)} .
\tag{G.6}
$$

*At the benchmark with $r_a=2.02$, the left side is $0.0663$ and the right side is $0.0194$. So $U^*(r)$ is strictly increasing on $[2.02,r_C)$ and equals zero above $r_C$. The upper edge of the insider region is a ramp with a cliff.*

*(iv) In every equilibrium with $\lambda>0$, $\kappa\le V\le\bar U(r):=\tfrac12\big[(\Delta_T(1-\tau)-k)_++(\Delta_TM-k)_+\big]$, whatever the orders and the pool.*

*Proof.* (i) At $\lambda=1$ the continuation is the fork's, and Proposition F.2(c) shows that full orders are optimal with $U_H(1)=U_L(1)=J-k$ and $U_\theta'>0$ on the order interval. Then $V=J-k\ge\kappa$, so $\lambda=1$ satisfies (E2), strictly when the inequality is strict.

(ii) Under full orders $\mu_X=(1+e^{-2x/b})^{-1}$ on $(-1,1)$, so $f(x-1)(1-\mu_X)=\tfrac1{2b}e^{-(1-x)/b}/(1+e^{2x/b})=e^{-1/b}/(4b\cosh(x/b))$. With $u=x/b$, $\int_{x^*}^1f(x-1)(1-\mu_X)\,dx=\tfrac{e^{-1/b}}4\int_{x^*/b}^{1/b}\operatorname{sech}u\,du=\tfrac{e^{-1/b}}4[\operatorname{gd}(1/b)-\operatorname{gd}(x^*/b)]$. On $x\ge1$, $1-\mu_X=m$ and $\int_1^\infty f(x-1)\,dx=\tfrac12$. Since $e^{x^*/b}=\sqrt{\tau/(1-\tau)}$, $\sinh(x^*/b)=\tfrac12[\sqrt{\tau/(1-\tau)}-\sqrt{(1-\tau)/\tau}]$, which is the stated form.

(iii) The lower bound is the plateau term alone. For the derivative, $\cosh(x^*/b)=1/(2\sqrt{\tau(1-\tau)})$ and $d(x^*/b)/d\tau=1/(2\tau(1-\tau))$, so $d\operatorname{gd}(x^*/b)/d\tau=\operatorname{sech}(x^*/b)\,d(x^*/b)/d\tau=1/\sqrt{\tau(1-\tau)}$, and $G'(\tau)=-(e^{-1/b}/4)/\sqrt{\tau(1-\tau)}$. From (4), $\Delta_T'/\Delta_T=(r+\ell)/(r(r-\ell))$, which decreases in $r$. Write $\tau=N/D$ with $N=c-g_L$ and $D=g_H-g_L=h-r/2-\ell^2/(2r)$; then $N'=(\ell^2-p^2)/(2r^2)>0$ decreases in $r$, $D'=-\tfrac12+\ell^2/(2r^2)\in(-\tfrac12,0)$, and $\tau'=N'/D+\tau|D'|/D\le[N'(r_a)+M/2]/D(r_C)$ on $[r_a,r_C]$ because $D$ decreases and $\tau\le M$. On $\tau\in[\tfrac12,M]$, $\tau(1-\tau)\ge Mm=1/(4\cosh^2(1/b))$. Insert these bounds in (G.5): the first term is at least $\Delta_T$ times the left side of (G.6), the second at most $\Delta_T$ times the right side. The benchmark values are closed-form arithmetic: $N'(2.02)=0.0919$, $M/2=0.3655$, $D(r_C)=8.0645$, so $\tau'\le0.0567$; $2\cosh\tfrac12=2.2553$; the right side is $0.0194$; the left side is $4.5927/(3.5927\times2.5927)\times0.1345=0.0663$. Above $r_C$ no live equilibrium exists by Proposition G.1(iv).

(iv) Against any schedule, $U_H=\sup_s s[F_H(s)-k]$ with $F_H(s)=\int f(x-s)A_H(x)\,dx$. On $A$, $1-\mu^\lambda_X\le1-\tau$ by Lemma G.2(c), and $\int_Af(x-s)\,dx\le1$, so $F_H\le\Delta_T(1-\tau)$ and $U_H\le(\Delta_T(1-\tau)-k)_+$. Likewise $A_L\le\Delta_TM_\lambda\le\Delta_TM$. Average. $\square$

The hump of entry in the fork (Proposition F.4) does not carry over to the investor's profit. Deterrence shrinks the entry set as $r$ rises, but $\Delta_T$ grows faster, and the plateau $x\ge1$ is never deterred before $r_C$. On the plateau the investor's residual is $m\Delta_T$, and that term alone gives the lower envelope $m\Delta_T/2-k$, which increases in $r$. At the ceiling the entry set is exactly the plateau, $U^*(r_C^-)=m\Delta_T(r_C)/2-k=0.1058$, and one step further nothing is material.

The bound $\bar U(r)$ is loose ($0.32$ at $r=3$ against $U^*=0.0755$). It matters only for necessity: no equilibrium with acquisition exists above it. The exact ceiling over all continuations is open; the cutoff family of the fork lowers $V$ as the pool grows, so on that family the minimal pool is the ceiling.

### 4.4 Mixed acquisition

Define the full-order candidate at $(r,\lambda)$: orders $(1,-1)$, entry on $[x^*_\lambda,\infty)$ with $x^*_\lambda$ the flow at which $\mu^\lambda_X$ reaches $\tau$, price as in Lemma G.2. Write $V(\lambda,r)$ for the investor's value in it, and set $V(\lambda,r)=0$ for $\lambda<\lambda_{\min}(r)$, where no live continuation exists.

**Proposition G.3 (mixed acquisition; (i) and (ii) analytical, (iii) numerical diagnostic).** *Assume $B_r(\tfrac12)<c\le B_r(M)$.*

*(i) If an equilibrium has $\lambda\in(0,1)$, then $\lambda\ge\lambda_{\min}(r)$ and $\kappa=V$ at its continuation.*

*(ii) At $\lambda=\lambda_{\min}(r)$ the full-order candidate has entry on the plateau $\{x\ge1\}$ only, where the belief is exactly $\tau$. It is a continuation equilibrium when*

$$
\frac{\Delta_T(1-\tau)e^{-1/b}}2>k
\qquad\text{and}\qquad
\frac{\Delta_T\,\tau\,e^{-2/b}}2\Big(1-\frac1b\Big)>k,
\tag{G.7}
$$

*and then*

$$
V(\lambda_{\min},r)=\frac{\Delta_T}{4}\Big[(1-\tau)+\tau e^{-2/b}\Big]-k>0 .
\tag{G.8}
$$

*The value of acquisition therefore jumps at $\lambda_{\min}(r)$, from $0$ to (G.8). At the benchmark (G.7) holds for $r\ge2.2$ on the grid.*

*(iii) At the benchmark and $r\in\{2.5,3,3.5\}$, $V(\lambda,r)$ is strictly increasing in $\lambda$ on $[\lambda_{\min},1]$, and the full-order sufficient test $k<(1-1/b)\min_\theta F_\theta(1)$ holds on the whole interval. The rise from $\lambda_{\min}$ to $1$ is $7.8\%$, $4.1\%$, and $0.7\%$ of $U^*(r)$. Hence on this branch a mixed-acquisition equilibrium exists if and only if $\kappa\in[V(\lambda_{\min},r),U^*(r))$, and every such equilibrium is a repeller of the acquisition best-response dynamic. For $\kappa<V(\lambda_{\min},r)$ there is no mixed equilibrium on the branch; the dynamic has a tipping point at $\lambda_{\min}(r)$, which is not an equilibrium. At $r=2.05$ the test holds only for $\lambda\ge0.932$; below that, the grid finds live fixed points with a partial short from $\lambda=0.74$, and the nodes in $[\lambda_{\min},0.73]$ are unresolved.*

*Proof.* (i) is Proposition G.1(iii) with (E2). (ii) At $\lambda_{\min}$, $M_\lambda=\tau$, and under full orders $\mu^\lambda_X$ is strictly increasing on $(-1,1)$ and equal to $M_\lambda$ on $[1,\infty)$ (Lemma G.2 with the explicit exponents $g_H=e^{(2x-1)/b}$ on $(0,1)$ and $g_L=e^{-(2x+1)/b}$ on $(-1,0)$). So $\{\mu^\lambda_X\ge\tau\}=[1,\infty)$, the belief there is $\tau$, and the tie rule admits preparation. The pool $(-\infty,1)$ has posterior below $\tfrac12$ by Lemma G.2. Against this schedule the high type's residual is $\Delta_T(1-\tau)$ on $[1,\infty)$, so a buy of size $s$ earns $U_H(s)=s[\Delta_T(1-\tau)S_Z(1-s)-k]$ with $S_Z(1-s)=\tfrac12e^{-(1-s)/b}$. Its derivative $\Delta_T(1-\tau)\tfrac12e^{-(1-s)/b}(1+s/b)-k$ is smallest at $s=0$, where it equals the first margin in (G.7). A wrong-signed order has nonpositive gross payoff. The low type's short of size $s$ earns $s[\Delta_T\tau S_Z(1+s)-k]$ with $S_Z(1+s)=\tfrac12e^{-(1+s)/b}$; the derivative $\Delta_T\tau\tfrac12e^{-(1+s)/b}(1-s/b)-k$ is smallest at $s=1$, where it equals the second margin. So full orders are globally optimal, and $U_H(1)=\Delta_T(1-\tau)/2-k$, $U_L(1)=\Delta_T\tau e^{-2/b}/2-k$; average to (G.8). For $\lambda<\lambda_{\min}$ no price reaches $\tau$ (Lemma G.1), so no live continuation exists and $V=0$. (iii) The dynamic moves $\lambda$ up by a small step when $V(\lambda_t,r)>\kappa$ and down by a small step when $V(\lambda_t,r)<\kappa$. [Referee fix: the original dynamic jumped to $\lambda_{t+1}\in\{0,1\}$. Under that jump dynamic the interior equilibrium of Remark G.1 is not an attractor; it starts a two-cycle between $0$ and $1$. The gradual dynamic gives both the repeller claim here and the attractor claim in Remark G.1.] At a mixed equilibrium $V=\kappa$; if $V$ increases through $\kappa$, a small upward perturbation sends $\lambda$ to $1$ and a downward one sends it below $\lambda_{\min}$, where $V=0$, and then to $0$. The monotonicity, the test, and the band are read from `acquisition_profile_quad.csv` and `mixed_band.csv`, where $V$ is computed by adaptive quadrature with the threshold $x^*_\lambda$ found by root-finding, and cross-checked against grid fixed points in `acquisition_profile.csv`. $\square$

Two forces move $V$ with $\lambda$, and they pull in opposite directions. Pointwise on a fixed entry set, the informed profit falls in $\lambda$: the market maker trusts the flow more, and the residual shrinks. [Referee fix: this holds for the average $V$. The pointwise derivative of $f(x-1)(1-\mu^\lambda_X)+f(x+1)\mu^\lambda_X$ in $\lambda$ is $-f_0(f_1-f_{-1})^2/D_\lambda^2\le0$. The low type's own residual $\mu^\lambda_X$ rises in $\lambda$ on $x>0$, because $\partial_\lambda\mu^\lambda_X$ has the sign of $g_H-g_L$.] This is the Kyle effect, and it is the only effect when materiality is exogenous (Remark G.1). Against it, the entry set grows in $\lambda$: $x^*_\lambda$ falls from $1$ at $\lambda_{\min}$ to $x^*$ at $\lambda=1$. At the benchmark the second force wins on average, but barely, and the two types split: at $r=3$, $U_H$ falls from $0.0784$ to $0.0755$ and $U_L$ rises from $0.0665$ to $0.0755$ as $\lambda$ rises from $\lambda_{\min}$ to $1$. The large effect of $\lambda$ is not the slope. It is the jump at $\lambda_{\min}$. That jump is the two-sided complementarity of @DowGoldsteinGuembel2017 in this model: the challenger acts on the price only if it believes the price was made by an insider.

### 4.5 Game B: the non-acquirer who may trade

Suppose a non-acquirer may submit an order. It does not know $\theta$, but it knows something the market maker does not: that the flow it generates is $s+Z$ and carries no information about $\theta$.

**Proposition G.4 (the non-acquirer's short; analytical given the schedule).** *Fix the fork's minimal-pool full-order schedule at strength $r$, with entry on $[x^*,\infty)$ and $x^*>0$. A non-acquirer who submits order $s$ has residual $e(x)\Delta_T(\tfrac12-\mu_X(x))$, which is strictly negative on the entry set and zero on the pool. No buy order is profitable. A short of size $s\in[0,1]$ earns*

$$
U_U(s)=s\big[e^{-s/b}\,\Phi(r)-k\big],
\qquad
\Phi(r)=\Delta_T\int_{x^*}^\infty f(x)\,[\mu_X(x)-\tfrac12]\,dx\;\ge\;\frac{\Delta_T\,(M-\tfrac12)\,e^{-1/b}}2 .
\tag{G.9}
$$

*A profitable short exists if and only if $\Phi(r)>k$. The best short is $s_U=\min\{1,s^\circ\}$, with $s^\circ$ the unique root of $(1-s/b)e^{-s/b}\Phi=k$, and its profit $U_U(r)=U_U(s_U)>0$. In game B the pure-acquisition profile of Proposition G.2 is an equilibrium if and only if $\kappa\le U^*(r)-U_U(r)$; $\mathcal D$ is unchanged.*

*Proof.* From the non-acquirer's view $\theta$ is independent of $(s,Z)$, so its expectation of $V_T$ at flow $x$ is $t_0+e(x)[w_L+\Delta_T/2]$, while the price is $t_0+e(x)[w_L+\Delta_T\mu_X(x)]$. The difference is the stated residual; on $A$, $\mu_X\ge\tau>\tfrac12$. A buy of size $s$ earns $s\int f(x-s)\,e\,\Delta_T(\tfrac12-\mu_X)\,dx-ks<0$. A short of size $s$ earns $s\int f(x+s)\,e\,\Delta_T(\mu_X-\tfrac12)\,dx-ks$. On $A\subseteq[x^*,\infty)$ with $x^*>0$ and $s\ge0$ we have $x+s>0$, so $f(x+s)=e^{-s/b}f(x)$, which gives (G.9). On $x\ge1$, $\mu_X-\tfrac12=M-\tfrac12$ and $\int_1^\infty f=\tfrac12e^{-1/b}$, which gives the lower bound. $U_U'(s)=\Phi e^{-s/b}(1-s/b)-k$, and $(1-s/b)e^{-s/b}$ is strictly decreasing on $[0,1]$ with derivative $-(2-s/b)e^{-s/b}/b$, so $U_U'$ crosses zero at most once, from above. If $\Phi\le k$ the zero order is optimal; otherwise the maximizer is $s_U$. In game B the investor compares $V-\kappa$ with $U_U(r)$, so (E2) becomes $\lambda=1$ if $V-\kappa>U_U$. In $\mathcal D$ the schedule is $P\equiv t_0=V_T$ and every order loses its cost, so the non-acquirer's best order is still zero. $\square$

At the benchmark the lower bound in (G.9) exceeds $k$ for $r>2.09$, and quadrature gives $\Phi(2.05)=0.0215>k$, so the short is profitable on the whole full-order segment. The best short grows from $0.07$ at $r=2.05$ to $0.996$ at $r_C$ [Referee fix: was "$1.0$"; at $r_C$, $(1-1/b)e^{-1/b}\Phi(r_C)=0.0199<k$, so the root $s^\circ$ lies just below $1$], and its profit from $0.00006$ to $0.0198$. [Referee note: on the full-order schedule $\Phi(r)=k$ at $r=1.997$, so the short is already profitable at the first full-order strength $2.0155$; the entry $2.05$ in Table 1 reflects the spacing of the fork's branch grid.] The game-B ceiling $U^*-U_U$ lies $0.3\%$ to $19\%$ below the game-A ceiling (Table 2; dotted line in the figure). On the partial-order segment $r\le2.0$ the short is not profitable ($\Phi(2.0)=0.0199<k$).

Why the short pays. On the entry set the price contains a premium for the market maker's belief that the flow came from an informed buyer. A non-acquirer knows that belief is wrong about its own flow and sells the premium. The short also pushes the flow toward the pool, where the premium is zero, which is why the best short is interior at moderate strengths. This is not the manipulation of @GoldsteinGuembel2008, in which an uninformed short profits because it cancels the real decision. Here the short profits on the flows that keep the real decision and loses nothing on the flows that cancel it. The feature is general: wherever acquisition is uncertain and the price responds to flow asymmetrically, the non-acquirer has private information about the information content of the flow.

### 4.6 Competition creates insiders, at any cost

**Proposition G.5 (competition creates insiders; analytical).** *Fix $0<p<\ell<h$, $b>1$, $k>0$, and $c$ with $\sup_{r\in(\ell,h)}B_r(\tfrac12)<c$, so that $\mathcal D$ exists at every strength. Fix any $\kappa>0$.*

*(i) For every $r<\mathfrak r(k)$ the unique equilibrium is $\mathcal D$: the investor does not learn $\theta$.*

*(ii) For every $r>r_C$ the unique equilibrium is $\mathcal D$.*

*(iii) For every $r$ with $c\le B_r(M)$, $k<(1-1/b)J(r)$, and $\kappa<U^*(r)$, there is a strict equilibrium in which the investor learns $\theta$ with probability one, trades $(1,-1)$, the price is informative, and preparation is $(\alpha_H+\alpha_L)/2>0$. $\mathcal D$ coexists with it.*

*(iv) Parts (i) and (ii) hold uniformly in $\kappa$. In the limit $\kappa\downarrow0$ the equilibrium sets in (i) and (ii) do not change, and in (iii) the mixed equilibria disappear while $\mathcal D$ remains.* [Referee fix: the clause "the mixed equilibria disappear" is not analytical. The proof uses $V(\lambda_{\min},r)$ as a floor, but that floor holds only on the minimal-pool full-order branch, only where (G.7) holds, and its monotonicity part is a numerical diagnostic (Proposition G.3(iii)). Larger pools and partial orders give mixed equilibria with lower $V$. Whether the infimum of $V$ over all live continuations is positive at a fixed $r$ is open. Status of that clause: open; the rest of (iv) is analytical.]

*(v) In every equilibrium with acquisition at strength $r$, $\lambda\ge\lambda_{\min}(r)$, and $\lambda_{\min}(r)\uparrow1$ as $r\uparrow r_C$.*

*The benchmark vector with $c=6$ satisfies the hypothesis, with $\mathfrak r(k)=1.2210$, $r_C=3.5927$, and (iii) on $[2.02,r_C)$ with $U^*$ from $0.0202$ to $0.1058$.*

*Proof.* (i) and (ii) are Proposition G.1(iv); (iii) is Proposition G.2(i); (iv) restates that (i) and (ii) carry no condition on $\kappa$, and that mixed equilibria need $\kappa\ge V(\lambda_{\min},r)>0$ by Proposition G.3; (v) is Proposition G.1(iii) and Lemma G.1. $\square$

What is stronger than Proposition F.3. The fork says that at a weak incumbent nobody trades on $\theta$, which the investor knows for free. This note says that nobody learns $\theta$, however cheap learning is. The standard account of information production, from @GrossmanStiglitz1980 onward, makes production a matter of cost. Here, outside $(\mathfrak r(k),r_C]$ [Referee fix: was $(\mathfrak r(k),r_C)$; an acquisition equilibrium exists at $r=r_C$ under the tie rule], it is a matter of materiality: no cost of learning, however small, produces an insider, because the signal could not move the stock. Inside the range, competition is sufficient for the existence of an insider up to the explicit ceiling $U^*(r)$, and the ceiling rises with competition until the challenger stops listening. [Referee fix: "inside the range" holds analytically on the full-order segment $[2.0155,r_C]$ and as a numerical diagnostic on $[1.66,2.0]$. On $(\mathfrak r(k),1.66)$ no live equilibrium was found and none is excluded, so existence there is open.]

What is not stronger. Competition is never sufficient for uniqueness. $\mathcal D$ exists on the whole domain $B_r(\tfrac12)<c$ at every $\kappa>0$, and Proposition G.1(i) shows it is strict. A theorem of the form "competition is necessary and sufficient for information production" holds for existence and fails for uniqueness, and no change in $\kappa$ repairs this. The dead equilibrium is robust to free information.

The reason the complementarity does not deliver uniqueness here is the one that separates this model from the strategic-substitutes benchmark.

**Remark G.1 (exogenous materiality: strategic substitutes; analytical).** *Suppose instead $c\le B_r(m)$ and $k<(1-1/b)\,m\,\Delta_T(r)$, so the challenger prepares at every price for every $\lambda$ and full orders are the unique informed continuation at every $\lambda$ by the bound (A.6) with $\rho=1$. Then $V(\lambda)=\tfrac{\Delta_T}2\int\frac{2\lambda f_1f_{-1}+(1-\lambda)f_0(f_1+f_{-1})}{\lambda(f_1+f_{-1})+2(1-\lambda)f_0}\,dx-k$, with $f_j(x)=f(x-j)$, is strictly decreasing in $\lambda$, from $V(0)=\Delta_T/2-k$ to $V(1)=\Delta_T[m+\tfrac{e^{-1/b}}2\operatorname{gd}\tfrac1b]-k$. The acquisition equilibrium is unique: $\lambda=1$ if $\kappa\le V(1)$, the unique root of $V(\lambda)=\kappa$ if $V(1)<\kappa<V(0)$, and $\lambda=0$ if $\kappa\ge V(0)$; the interior equilibrium is an attractor of the dynamic.*

*Proof.* With $e\equiv1$ the two gross profits sum pointwise to $N_\lambda/D_\lambda$ with $N_\lambda=2\lambda f_1f_{-1}+(1-\lambda)f_0S$, $D_\lambda=\lambda S+2(1-\lambda)f_0$, $S=f_1+f_{-1}$. The derivative in $\lambda$ of $N_\lambda/D_\lambda$ has the sign of $f_0(4f_1f_{-1}-S^2)/S=-f_0(f_1-f_{-1})^2/S\le0$, strictly for $x\ne0$. Symmetry of $f_0$ and of $D_\lambda$ gives $F_H(1)=F_L(1)$ at every $\lambda$, so the sufficient test at $\lambda=1$ covers every $\lambda$. The value at $\lambda=1$ is (G.4) with $x^*=-1$, using $\operatorname{gd}(-u)=-\operatorname{gd}(u)$ and the lower tail $\tfrac M2e^{-2/b}=\tfrac m2$. The rest is (E2). $\square$

With exogenous materiality the acquisition decision is a Grossman–Stiglitz problem: more insiders make each insider's trade less profitable, and the market settles at an interior, stable fraction. With endogenous materiality the same Kyle force is present, but a threshold force sits on top of it: below $\lambda_{\min}$ the signal is worth nothing because the challenger ignores every price. That threshold is what creates the coordination problem, the multiplicity, and the robustness of $\mathcal D$. At the benchmark $r=3$ with $c\le B_3(m)=2.37$ the substitutes picture holds and $V$ falls from $0.313$ to $0.256$ as $\lambda$ rises from $0$ to $1$ (Table 6). With $c=6$ the complements picture holds: $V$ is zero up to $\lambda_{\min}=0.875$ and about $0.073$ above it.

### 4.7 A new selection argument: observable acquisition

Private acquisition gives forward induction nothing to work with. In $\mathcal D$ a unilateral acquisition changes no schedule, because nobody sees it. Suppose instead that acquisition is observed by market makers and the challenger before trading. Then the continuation after "no acquisition" is $\mathcal D$'s schedule (Proposition G.1(ii)), and the continuation after "acquisition" is an equilibrium of the fork's game at $\lambda=1$, whose set contains $\mathcal D$ and, under the hypotheses of Proposition F.2, the live cutoff family.

Call a continuation after observed acquisition *consistent with acquisition* if the investor's value in it is at least $\kappa$. The forward-induction restriction is that the challenger and the market makers believe that an investor who paid $\kappa$ expects to recover it. This is the argument of @vanDamme1989 and @BenPorathDekel1992 for a costly observable action before a coordination game.

**Proposition G.6 (observable acquisition selects the live equilibrium; analytical under the stated restriction).** *Assume the hypotheses of Proposition G.2 and observable acquisition.*

*(i) If $\kappa>\sup V$ over the continuation set at $\lambda=1$, no continuation is consistent with acquisition, acquisition is strictly dominated, and the outcome is $\mathcal D$.*

*(ii) If $\kappa<U^*(r)$, the minimal-pool live continuation is consistent with acquisition and $\mathcal D$ is not. Under the restriction, the continuation after acquisition is live with $V\ge\kappa$, and the investor acquires. Within the full-order cutoff family, $V(x')=\Delta_T\int_{x'}^\infty f(x-1)(1-\mu_X)\,dx-k$ is strictly decreasing in the pool cutoff $x'$, so the consistent members form an interval $[x^*,x'(\kappa)]$ that shrinks to the minimal pool as $\kappa\uparrow U^*(r)$. A higher acquisition cost selects a more informative price.*

*Proof.* (i) Non-acquisition yields $0$ and acquisition yields $V-\kappa<0$ in every continuation. (ii) In $\mathcal D$ the investor's value is $0<\kappa$; in the minimal-pool continuation it is $U^*(r)\ge\kappa$ by Proposition G.2. Along the family, the integrand $f(x-1)(1-\mu_X)$ is positive, so $V(x')$ falls strictly in $x'$ while orders stay full, and $V(x^*)=U^*(r)$. $\square$

[Referee fix: two gaps. First, with the weak inequality $V\ge\kappa$ the member $x'(\kappa)$ gives the deviator exactly $V-\kappa=0$, its payoff in $\mathcal D$, so $\mathcal D$ is not strictly broken. The selection step needs the strict form of the restriction, $V>\kappa$, under which the consistent set is $[x^*,x'(\kappa))$ and every consistent continuation makes acquisition strictly profitable. Second, the claim "a more informative price" had no proof. A proof: take $x^*\le x_1'<x_2'$ on the full-order segment of the family and write $P_1,P_2$ for the prices. If $x_2'\le1$, then $P_2$ is a function of $P_1$. If $x_2'>1$, the only cell of $P_1$ that $P_2$ splits is the plateau cell $\{X\ge y\}$ of $P_1$, with $y=\max\{x_1',1\}$. On that cell both conditional flow densities are proportional to $e^{-x/b}$, so $\Pr(X<x_2'\mid X\ge y,\theta)=1-e^{-(x_2'-y)/b}$ does not depend on $\theta$, and the split is a state-independent kernel. Hence $P_2$ is a garbling of $P_1$. The dominance is strict because $P_1$ separates the flows in $[x_1',x_2')$, whose posteriors are at least $\tau$, from the pool $(-\infty,x_1')$, whose posterior is at most $\tfrac12$, and $P_2$ pools them. The comparison does not cover members with partial orders, whose flow laws differ.]

At $r=3$ the family's value falls from $0.0754$ at $x'=0.872$ to $0.0508$ at $x'=1.472$ and $0.0219$ at $x'=2.522$ (fork, `cutoff_family.csv`). A cost $\kappa=0.05$ therefore leaves only pools with $x'\le1.49$, and a cost $\kappa=0.07$ only pools with $x'\le0.99$. [Referee fix: was $1.47$ and $0.97$, the last grid nodes of the fork's CSV; quadrature gives $x'(0.05)=1.495$ and $x'(0.07)=0.992$.] The fork's selection discussion (Section 6 of the fork note) had payoff dominance and the vanishing floor. Observable costly acquisition adds a third argument, and it is the only one of the three that selects live over dead by a forward-induction restriction rather than by a payoff comparison [Referee fix: was "by a standard refinement"; which standard refinement delivers the restriction is open item 5]. Its price is observability. For an activist that must file, or a specialist fund whose research is known, the assumption is mild. For a secret trader it fails, and $\mathcal D$ stands.

## 5. Numerics

All numbers use the benchmark vector $(h,\ell,p,b,k,c)=(10,1,0.5,2,0.02,6)$. Closed forms are evaluated with `mpmath` at 30 digits and are labeled analytical. Grid fixed points use the fork's flow grid of $60{,}001$ points on $[-30,30]$ and its order grid, with best-response iteration from the starts $(1,-1)$, $(1,-\tfrac12)$, $(1,-\tfrac14)$, $(\tfrac12,-\tfrac12)$, and are labeled numerical diagnostic. The quadrature profile uses adaptive quadrature on $[x^*_\lambda,1]$ with the exact threshold and the closed-form tail. The solver is `acquisition.py`; it writes `insider_region.csv`, `uninformed_short.csv`, `acquisition_profile.csv`, `acquisition_profile_quad.csv`, `mixed_band.csv`, `monotonicity.csv`, and `thresholds.csv`. The renderer `render.py` draws `insider_region.pdf` from those files and the fork's `branches.csv`.

**Table 1. Thresholds.**

| Object | Value | Status |
|---|---|---|
| $\mathfrak r(k)$: below it $\mathcal D$ is unique at every $\kappa$ | 1.2210 | analytical, (A.10) |
| $r_C$: above it $\mathcal D$ is unique at every $\kappa$ | 3.5927 | analytical, (A.11) with $c_H\to c$ |
| first grid strength with $k<(1-1/b)J(r)$, $J$ closed form | 2.02 | analytical test on a grid |
| $\sup_r U^*(r)$, attained at $r=r_C$ under the tie rule [Referee fix: was "as $r\uparrow r_C$"] | 0.1058 | analytical, (G.4) |
| monotonicity margin of (G.6) on $[2.02,r_C]$ | $0.0663-0.0194=0.0469>0$ | analytical, closed-form bounds |
| first grid strength with full orders optimal at $\lambda_{\min}$, (G.7) | 2.20 | analytical test on a grid |
| first grid strength with a profitable non-acquirer short | 2.05 | numerical diagnostic |

**Table 2. The insider region at selected strengths.** $U^*$ is the game-A ceiling for pure acquisition. $V(\lambda_{\min})$ is the floor of the mixed band. $U_U$ is the non-acquirer's best short profit, and $U^*-U_U$ the game-B ceiling. $\bar U$ is the universal bound of Proposition G.2(iv).

| $r$ | $\tau$ | $\lambda_{\min}$ | $U^*(r)$ | $V(\lambda_{\min},r)$ | band width | $s_U$ | $U_U(r)$ | $U^*-U_U$ | $\bar U(r)$ | status of $U^*$ |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.66 | 0.651 | 0.626 | 0.0018 | | | 0 | 0 | 0.0018 | 0.051 | numerical diagnostic, orders $(1,-0.25)$ |
| 1.80 | 0.656 | 0.650 | 0.0079 | | | 0 | 0 | 0.0079 | 0.076 | numerical diagnostic, orders $(1,-0.65)$ |
| 2.00 | 0.664 | 0.686 | 0.0191 | | | 0 | 0 | 0.0191 | 0.113 | numerical diagnostic, orders $(1,-0.98)$ |
| 2.05 | 0.666 | 0.695 | 0.0219 | 0.0189 (G.7 fails) | 0.0005 on $[0.932,1]$ | $-0.07$ | 0.00006 | 0.0219 | 0.123 | analytical |
| 2.50 | 0.684 | 0.777 | 0.0475 | 0.0438 | 0.0037 | $-0.52$ | 0.0036 | 0.0439 | 0.216 | analytical |
| 3.00 | 0.705 | 0.875 | 0.0755 | 0.0724 | 0.0031 | $-0.80$ | 0.0106 | 0.0649 | 0.322 | analytical |
| 3.50 | 0.727 | 0.980 | 0.1013 | 0.1007 | 0.0007 | $-0.97$ | 0.0184 | 0.0830 | 0.428 | analytical |
| 3.5926 | 0.7311 | 0.99999 | 0.1058 | 0.1058 | 0.0000 | $-1.00$ | 0.0198 | 0.0861 | 0.448 | analytical |
| 3.5927 | 0.7311 | n/a | 0 | 0 | | | | 0 | 0 | analytical, above $r_C$ |

The closed-form $U^*$ agrees with the fork's grid branch to $3\times10^{-5}$ at every full-order node.

**Table 3. The acquisition profile at $r=3$.** Full-order candidate by quadrature; grid fixed point beside it.

[Referee fix: the third column is entry conditional on acquisition, $\tfrac12(e_H+e_L)$, not the preparation probability $\mathsf E$. At $\lambda<1$ the preparation probability is $\lambda\cdot\tfrac12(e_H+e_L)+(1-\lambda)\Pr(Z\ge x^*_\lambda)$, which is $0.337$, $0.340$, $0.349$, $0.358$, $0.364$ on the five live rows. The same holds for the column `E` of `acquisition_profile.csv` and `acquisition_profile_quad.csv`.]

| $\lambda$ | $x^*_\lambda$ | entry given acquisition | $U_H$ | $U_L$ | $V$ (quadrature) | $V$ (grid) | test |
|---|---|---|---|---|---|---|---|
| 0.8546 | none | 0 | 0 | 0 | 0 | 0 | no live continuation (analytical) |
| 0.8746 $=\lambda_{\min}$ | 1.000 | 0.342 | 0.0784 | 0.0665 | 0.0724 | 0.0724 | holds |
| 0.8897 | 0.984 | 0.345 | 0.0781 | 0.0676 | 0.0728 | 0.0728 | holds |
| 0.9298 | 0.941 | 0.352 | 0.0773 | 0.0705 | 0.0739 | 0.0739 | holds |
| 0.9699 | 0.901 | 0.359 | 0.0763 | 0.0734 | 0.0748 | 0.0748 | holds |
| 1.0000 | 0.871 | 0.364 | 0.0755 | 0.0755 | 0.0755 | 0.0755 | holds |

**Table 4. The mixed-acquisition band.** The band is the range of $V(\cdot,r)$ on $[\lambda_{\min},1]$ where the sufficient test holds.

| $r$ | $\lambda_{\min}$ | band $[V(\lambda_{\min}),U^*)$ | width | rise as share of $U^*$ | shape of $V$ in $\lambda$ | stability of mixed equilibria |
|---|---|---|---|---|---|---|
| 2.05 | 0.695 | $[0.0215,0.0219)$ on $\lambda\ge0.932$ | 0.0005 | 2.1% | increasing | repeller |
| 2.50 | 0.777 | $[0.0438,0.0475)$ | 0.0037 | 7.8% | increasing | repeller |
| 3.00 | 0.875 | $[0.0724,0.0755)$ | 0.0031 | 4.1% | increasing | repeller |
| 3.50 | 0.980 | $[0.1007,0.1013)$ | 0.0007 | 0.7% | increasing | repeller |

Status: numerical diagnostic. At $r=2.05$ and $\lambda\in[0.695,0.731]$ the search found no live fixed point from any start; those nodes are unresolved. [Referee fix: at $r=2.05$ the band shown is only the part where the full-order test holds. The grid fixed points with a partial short on $\lambda\in[0.74,0.93]$ in `acquisition_profile.csv` are also points of the minimal-pool branch, with $V$ from $0.0191$ to $0.0214$, so the branch band at $r=2.05$ is at least $[0.0191,0.0219)$, width $0.0028$. All rows are for the minimal pool; larger pools give lower $V$ (open item 2).]

**Table 5. The cutoff family at $r=3$ and the consistent set under observable acquisition** (values from the fork's `cutoff_family.csv`).

| pool cutoff $x'$ | orders | $\mathsf E$ | $V$ | consistent with $\kappa=0.05$ | with $\kappa=0.07$ |
|---|---|---|---|---|---|
| 0.872 (minimal) | $(1,-1)$ | 0.363 | 0.0754 | yes | yes |
| 1.472 | $(1,-1)$ | 0.270 | 0.0508 | yes | no |
| 1.522 | $(1,-1)$ | 0.263 | 0.0491 | no | no |
| 2.522 | $(1,-1)$ | 0.160 | 0.0219 | no | no |
| 3.222 | $(1,-0.76)$ | 0.117 | 0.0107 | no | no |
| 3.272 | collapses to $\mathcal D$ | 0 | 0 | no | no |

**Table 6. Exogenous materiality at $r=3$** (Remark G.1, challenger prepares at every price; needs $c\le B_3(m)=2.37$).

| $\lambda$ | 0 | 0.25 | 0.5 | 0.75 | 1 |
|---|---|---|---|---|---|
| $V(\lambda)$ | 0.3133 | 0.2981 | 0.2835 | 0.2697 | 0.2564 |

Status: analytical form, quadrature values; the endpoints match the closed forms $\Delta_T/2-k$ and $\Delta_T[m+\tfrac{e^{-1/b}}2\operatorname{gd}\tfrac1b]-k$.

**Figure.** `insider_region.pdf` has two panels. Panel (a) plots the $(r,\kappa)$ plane. The shaded region below the solid line $\kappa=U^*(r)$ is where an equilibrium with acquisition exists; the dead equilibrium exists everywhere. The solid line is the closed form (G.4) on $[2.02,r_C)$, and the dashed-and-dotted rust segment on $[1.66,2.0]$ is the fork's partial-order branch (numerical diagnostic). The navy dashed line is $V(\lambda_{\min},r)$, the floor of the mixed band, drawn where (G.7) holds. [Referee fix: it is the floor of the band on the minimal-pool branch only.] The gray dotted line is the game-B ceiling $U^*-U_U$. The two flat regions are shaded, and the cliff at $r_C$ is drawn. Panel (b) plots $V(\lambda,r)$ against $\lambda$ at $r\in\{2.05,2.5,3,3.5\}$: zero below $\lambda_{\min}(r)$, a jump at $\lambda_{\min}(r)$, and a slow rise to $U^*(r)$. Solid segments pass the sufficient test; the dotted segment at $r=2.05$ is a candidate that fails it; circles are grid fixed points; the gap at $r=2.05$ near $\lambda_{\min}$ marks unresolved nodes. [Referee fix: in the rendered figure the gap is only in the circles. The dotted candidate line runs from $\lambda_{\min}$, and the filled "jump" point at $r=2.05$ is a candidate that is not an equilibrium, because (G.7) fails there.]

## 6. What this means for "when is the investor an insider"

Three statements can be made about the investor, and the acquisition game separates them.

**The investor knows $\theta$.** This is the acquisition decision, $\lambda$. In the paper it is an assumption. In the fork it is an assumption. Here it is a choice, and Proposition G.5 says the choice is governed by competition before it is governed by cost. Outside $(\mathfrak r(k),r_C]$ the investor does not learn at any price. Inside, it learns in some equilibrium if $\kappa\le U^*(r)$, and the ceiling rises with $r$ up to the cliff. [Referee fix: the original said $(\mathfrak r(k),r_C)$ and "if and only if". The right end $r_C$ belongs to the insider range under the tie rule, and the converse "only if" is open; $\bar U(r)$ is the proved necessary bound.]

**$\theta$ is material.** This is the fork's object: the entry set has positive probability. In game A, Proposition G.1(iii) ties it to the first statement inside every equilibrium. There is no equilibrium in which the investor knows $\theta$ and $\theta$ is immaterial, because it would not have paid to know. There is no equilibrium in which $\theta$ is material and nobody knows it, because the investor is the price's only source. So in game A, "insider" has one meaning inside an equilibrium, and the only separation is across equilibria: the same investor at the same $(r,\kappa)$ is an insider in the live equilibrium and nothing in $\mathcal D$.

**The investor chooses to learn $\theta$.** This is where the second layer bites, through the dilution floor. The challenger listens to the price only if it believes the investor is an insider with probability at least $\lambda_{\min}(r)$, which is $0.69$ at $r=2.02$, $0.87$ at $r=3$, and $1$ at $r_C$. A market that doubts whether the investor is informed cannot be moved by its trades. The jump in $V$ at $\lambda_{\min}$ is the two-sided complementarity in one number: the value of being an insider is zero until the market expects an insider. The slope of $V$ above the floor is small and even has the Kyle sign for the high type, so the complementarity is a threshold phenomenon, not a gradual one. Mixed-acquisition equilibria sit in a narrow band of costs just below the ceiling and are repellers; for lower costs the game is a pure coordination problem with a tipping point at $\lambda_{\min}$. [Referee fix: this holds on the minimal-pool full-order branch, as a numerical diagnostic. Larger pools support mixed-acquisition equilibria at lower costs, so the band is not the whole set.]

**Game B adds a fourth statement.** A non-acquirer who may trade does trade: it shorts, by $0.8$ units at $r=3$, and earns $0.011$ against the informed $0.0755$. It does not know $\theta$. $\theta$ is material on the flows it profits from. It has material private information, but about the order flow, not about the target: it knows the flow is noise, and it sells the premium that the price pays for the belief that the flow is informed. Under a definition of insider as "holder of material nonpublic information about the issuer", it is not one. Under a definition as "trader with a private informational advantage over the market maker", it is. The acquisition game thus produces an agent that profits from the market's belief in insiders without being one, and that agent lowers the return to becoming one by up to a fifth at the benchmark.

**Selection and observability.** Whether the live equilibrium or $\mathcal D$ is played decides whether there is an insider at all. The fork offered payoff dominance and the vanishing floor. The acquisition game offers forward induction when acquisition is observable: an investor who visibly pays for research is believed to expect to profit from it, and that belief makes the challenger listen and the market price accordingly. A higher visible cost then selects a smaller pool and a more informative price. So the practical answer to "when is the investor an insider" has an observability clause. A visible researcher is an insider when competition is in the live range and its cost is below $U^*(r)$. A secret researcher may be one or not, and the model does not decide which.

## 7. Open items and the next best step

1. **Game B at $\lambda<1$.** When non-acquirers short with positive probability, the market maker's densities become $a_\theta=\lambda f(x-q_\theta)+(1-\lambda)f(x-s_U)$ with $s_U<0$. This raises the plateau posterior, lowers $\lambda_{\min}$, and adds adverse selection on low flows. The fixed point in $(\lambda,s_U,q_H,q_L,x')$ is not computed. Status: open.
2. **Mixed acquisition across the cutoff family.** Each pair $(\lambda,x')$ with $V(\lambda,x')=\kappa$ is a mixed equilibrium. The set is a curve in $(\lambda,x')$ for each $\kappa$, and larger pools give lower $V$, so larger pools pair with lower costs. Not computed. Status: open.
3. **Unresolved nodes near the floor at low strength.** At $r=2.05$ and $\lambda\in[0.695,0.731]$ the full short is not optimal and no live fixed point was found from four starts. A search over partial orders, and a dilution floor for partial orders, would resolve them. Status: open.
4. **Certification.** $U^*(r)$ and the margin in (G.6) are closed forms. One outward interval evaluation would lift the benchmark parts of Propositions G.2(iii) and G.5 to computer-assisted and would close the fork's open item 1 as a by-product. Status: open, cheap.
5. **The formal refinement behind Proposition G.6.** The note states the forward-induction restriction directly. Which standard concept delivers it in this infinite game is not verified. Status: open.
6. **The paper's own benchmark with acquisition.** With a floor $\rho>0$, $V(\lambda)$ is a sum of a floor part that falls in $\lambda$ (Remark G.1) and an expensive-entry part that jumps at $\lambda_{\min}$ computed from $c_H$. Where the mixture sits decides whether the paper's model is a substitutes game or a complements game at the acquisition stage. Not computed. Status: open.
7. **Several investors.** With $n$ investors who each pay $\kappa$, competition among insiders erodes $V$ while the dilution floor applies to the aggregate. A large-$n$ limit may pin the number of insiders. Status: open.
8. **The meaning of $\kappa$ against $c$.** The challenger learns $\theta$ by paying $c$; the investor by paying $\kappa$. If $\kappa<c$ and the signal were transferable, the challenger could buy it and the price channel would be redundant. The paper reads $c$ as verification and transaction preparation as well as learning. The fork and this note inherit that reading. Status: interpretation, open.

**Next best step.** Item 1. It decides whether the non-acquirer's short is a correction to the ceiling, as it is at $\lambda=1$, or a mechanism that changes the equilibrium set, as it may be at $\lambda<1$ when the market maker prices it in. Item 4 is a cheap preliminary that should be done first.

## Files

- `acquisition.py`: solver; pure functions with type hints; writes the seven CSV files listed in Section 5.
- `render.py`: renderer; reads CSV only; writes `insider_region.pdf`.
- `insider_region.csv`: closed-form objects on a strength grid of step $0.01$ (analytical rows).
- `uninformed_short.csv`: the non-acquirer's best short along the fork's $\lambda=1$ branch (numerical diagnostic).
- `acquisition_profile.csv`, `acquisition_profile_quad.csv`: $V(\lambda,r)$ by grid fixed points and by quadrature.
- `mixed_band.csv`, `monotonicity.csv`, `thresholds.csv`: summaries.

Run `python3 fork/endogenous_insider/research/info_acquisition/acquisition.py` (about half a minute) and then `python3 fork/endogenous_insider/research/info_acquisition/render.py` from the repository root.

## References

The citation keys are those of `refs.bib` in this folder; `DowGoldsteinGuembel2017` and `GoldsteinGuembel2008` are also keys of the paper.

- Ben-Porath, E., and E. Dekel (1992). Signaling future actions and the potential for sacrifice. *Journal of Economic Theory* 57(1), 36–51.
- Dow, J., I. Goldstein, and A. Guembel (2017). Incentives for information production in markets where prices affect real investment. *Journal of the European Economic Association* 15(4), 877–909.
- Goldstein, I., and A. Guembel (2008). Manipulation and the allocational role of prices. *Review of Economic Studies* 75(1), 133–164.
- Grossman, S. J., and J. E. Stiglitz (1980). On the impossibility of informationally efficient markets. *American Economic Review* 70(3), 393–408.
- van Damme, E. (1989). Stable equilibria and forward induction. *Journal of Economic Theory* 48(2), 476–496.
