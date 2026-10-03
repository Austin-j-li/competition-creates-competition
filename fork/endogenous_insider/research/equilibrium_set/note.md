---
title: "The equilibrium set of the endogenous-insider fork"
subtitle: "Research track on open items 1 and 2 of the fork"
date: "2026-10-03"
---

This note belongs to `fork/endogenous_insider/`. It uses the notation of `paper/main.md` and of the fork's `mechanism.md`. Equation numbers such as (4), (12) and (A.5) to (A.11) refer to the paper. Results F.1 to F.5 are the fork's. Results ES.1 to ES.6 and equations (ES.1) to (ES.4) are new here. Every result carries its status in the paper's vocabulary: analytical, computer-assisted, numerical diagnostic, or open. The files are listed in `README.md`. Tables T1 to T11 are in `tables.md`, and the figure is `equilibrium_set.pdf`.

## 1. Question

The fork has a dead equilibrium $\mathcal D$ and a family of live ones. The fork leaves four things open.

1. Is the inequality $k<(1-1/b)J(3)$ in Proposition F.3(ii) true, with a certificate rather than a quadrature?
2. Where exactly does the minimal-pool full-order equilibrium exist? The fork's test in F.2(c) is only sufficient. It first holds on the grid at $r=2.05$.
3. Where does the live branch start? The fork's first grid point with a live fixed point is $r=1.66$, with an interior low-type order. What happens at that edge?
4. Are there equilibria outside the cutoff family: entry sets with holes, mixed orders, wrong-signed orders?

## 2. Headline result

The fork's existence statistic has a closed form, and Proposition F.3 holds at the benchmark by plain arithmetic: $(1-1/b)J(3)\ge m/6>1/24>k$ (Proposition ES.1, analytical). The fork's sufficient test is also necessary. The minimal-pool full-order equilibrium exists exactly on $[r_J,r_C]$ with $r_J=2.01552$ (Proposition ES.3, computer-assisted). Live equilibria with $q_H=1$ exist exactly on $[r_e,r_C]$ with $r_e=1.65859$, the root of a closed-form edge equation. At $r_e$ the entry set shrinks to the top price atom and entry jumps from $0.384$ to $0$; this is a boundary collision, not a fold (Propositions ES.4 and ES.5, computer-assisted). Above $r_e$ the live set is large: every measurable entry set with enough "information mass" works, wrong-signed orders never occur, the low type never mixes, and we find no mixed or interior high-type order (Propositions ES.2 and ES.6, analytical; the high-type part is a numerical diagnostic). [Referee fix: "every measurable entry set with enough information mass works" is proved only for full orders, which needs $r\ge r_J$ (Proposition ES.6). For $r\in[r_e,r_J)$ no full-order equilibrium exists. For an interior short $z<1$ the entry set must meet the equality $\Delta_T\int_Af\mu_X=C^*(z)$, and the high type's global optimality against such sets is a numerical diagnostic (open item 3).]

## 3. Model changes

None. The model is the fork: one cost $c$, the tie rule (an indifferent challenger prepares), and the benchmark $(h,\ell,p,b,k,c)=(10,1,0.5,2,0.02,6)$. Throughout, $B_r(\tfrac12)<c\le B_r(M)$, so $\tau\in(\tfrac12,M]$. On the benchmark the first inequality holds at every $r\in(\ell,h)$ and the second holds for $r\le r_C=3.59266$.

Notation added here.

- $g(x)=f(x-1)f(x+1)/[f(x-1)+f(x+1)]$, the integrand of (F.3). For an entry set $A$, $J_A=\Delta_T\int_A g$, so $J=J_{[x^*,\infty)}$.
- $\hat\mu=(1+e^{-1/b})^{-1}$. On the benchmark $\hat\mu=0.62246$.
- For orders $(1,-z)$ with $z\in[0,1]$: the posterior plateau is $M_z=(1+e^{-(1+z)/b})^{-1}$, and $\mathcal U(z)=\{x:\mu_X(x)\ge\tau\}=[x^*(z),\infty)$ with $x^*(z)=\tfrac{1-z}2+\tfrac b2\operatorname{logit}\tau$.
- $n(r)=b\operatorname{logit}\tau(r)-1$. This is the smallest $z$ with $M_z\ge\tau$, so the smallest low-type order that makes any entry possible when $q_H=1$.
- $F_\theta$ and $U_\theta$ as in (A.4), against a fixed schedule. Write $F_L(s)$ for the low type's gross per unit at the order $-s$.

## 4. Results

### 4.1 The closed form of $J$ and Proposition F.3 at the benchmark

**Lemma ES.1 (closed form; analytical).** *For $0\le x_0\le x_1\le1$,*
$$\int_{x_0}^{x_1}g=\frac{e^{-1/b}}2\big[\arctan e^{x_1/b}-\arctan e^{x_0/b}\big],$$
*and for $1\le x_0\le x_1\le\infty$, $\int_{x_0}^{x_1}g=\tfrac12\big(e^{-(x_0+1)/b}-e^{-(x_1+1)/b}\big)/(1+e^{-2/b})$. Hence, for $\tau\in(\tfrac12,M]$,*
$$J(r)=\Delta_T(r)\Big[\frac m2+\frac{e^{-1/b}}2\Big(\arctan e^{1/b}-\arctan\sqrt{\tfrac{\tau}{1-\tau}}\Big)\Big].\tag{ES.1}$$

*Proof.* For $|x|\le1$, $f(x-1)f(x+1)=e^{-2/b}/(4b^2)$ and $f(x-1)+f(x+1)=e^{-1/b}\cosh(x/b)/b$. So $g(x)=e^{-1/b}/[4b\cosh(x/b)]$. The derivative of $2b\arctan e^{x/b}$ is $1/\cosh(x/b)$, which gives the first formula. For $x\ge1$, $f(x+1)/f(x-1)=e^{-2/b}$, so $g=f(x+1)/(1+e^{-2/b})$, and $\int_{x_0}^{x_1}f(x+1)\,dx=\tfrac12(e^{-(x_0+1)/b}-e^{-(x_1+1)/b})$. On $[1,\infty)$ the integral is $\tfrac12e^{-2/b}/(1+e^{-2/b})=m/2$. Finally $e^{x^*/b}=\sqrt{\tau/(1-\tau)}$ and $x^*\in(0,1]$. $\square$

**Proposition ES.1 (Proposition F.3 at the benchmark; analytical).** *The benchmark vector with $(r_0,r_1,r_2)=(1.2,3,3.6)$ satisfies (F.4), (F.5) and the ceiling condition of F.3(iii). In particular $(1-1/b)J(3)-k\ge m/6-1/50>0$. So Proposition F.3 holds at the benchmark as an analytical statement.*

*Proof.* Each step uses exact rationals and the bounds $2.718<e<2.7183$.

- $\Delta_T(1.2)=0.04/2.4=1/60<1/50=k$.
- $B_r(\tfrac12)=\tfrac12[h-\tfrac r2+(\ell^2-2p^2)/(2r)]$. So $B_{1.2}(\tfrac12)=1153/240=4.8042<6$ and $B_3(\tfrac12)=103/24=4.2917<6$.
- $B_3(M)>6$ is equivalent to $M>\tau(3)=141/200$, that is $e>141/59=2.390$. True.
- $B_{3.6}(M)<6$ is equivalent to $M<\tau(3.6)$. Here $g_L=5/48$ and $g_H-g_L=1451/180$, so $\tau(3.6)=4245/5804$. The inequality is $1559e<4245$, that is $e<2.7229$. True.
- $J(3)\ge\Delta_T(3)\,m/2$ by (ES.1), because $x^*(3)\le1$ makes the arctan bracket nonnegative. With $\Delta_T(3)=2/3$ and $b=2$, $(1-1/b)J(3)\ge m/6$. Since $e<3$, $m=1/(1+e)>1/4$, so $m/6>1/24>1/50$.

The other hypotheses of F.3 ($0<p<\ell<r_0<r_1<r_2<h$, $b>1$) hold by inspection. $\square$

The interval certificates in Table T1 confirm each number. $J(3)\in[0.0955028924240038,\,0.0955028924240039]$ from (ES.1) in outward interval arithmetic. An independent enclosure by monotone Riemann sums of (F.3) gives $[0.09550285,\,0.09550293]$ (the integrand decreases on $[x^*,1]$, and the tail on $[1,\infty)$ is exact). The margin is $(1-1/b)J(3)-k\in[0.0277514462120019,\,0.0277514462120020]$. Status of the enclosures: computer-assisted. The fork's open item 1 is closed, and in a stronger form than asked.

### 4.2 Structure of every equilibrium

**Lemma ES.2 (signs and monotone posterior; analytical).** *In every equilibrium, $\sigma_H$ puts no mass on $[-1,0)$ and $\sigma_L$ puts no mass on $(0,1]$. Then $\mu_X$ is continuous and nondecreasing, $\mu_X\le\tfrac12$ on $x\le-1$, and $\{\mu_X\ge\tau\}$ is empty or a closed half-line $[x^*,\infty)$.*

*Proof.* By Lemma F.1(d), the high type's payoff from $q<0$ is $q\Delta_T\int_Af(x-q)(1-\mu_X)\,dx-k|q|\le-k|q|<0$, while $q=0$ earns zero. So $q<0$ is never a best response. The low type is symmetric. Each $a_\theta$ is continuous by dominated convergence, so $\mu_X$ is continuous. For $x_1<x_2$,
$$a_H(x_2)a_L(x_1)-a_H(x_1)a_L(x_2)=\iint\big[f(x_2-q)f(x_1-q')-f(x_1-q)f(x_2-q')\big]\,d\sigma_H(q)\,d\sigma_L(q').$$
Every pair has $q\ge0\ge q'$. Put $u=x_1-q$, $v=x_2-q$, $w=x_1-q'$, $y=x_2-q'$. Then $u\le v,w\le y$ and $u+y=v+w$. Since $\log f$ is concave, $\log f(v)+\log f(w)\ge\log f(u)+\log f(y)$. So each bracket is nonnegative and $\mu_X$ is nondecreasing. For $x\le-1$, $a_H/a_L=\int e^{-q/b}d\sigma_H/\int e^{-q'/b}d\sigma_L\le1$. A closed, upward-closed set that misses $(-\infty,-1]$ is empty or $[x^*,\infty)$. $\square$

So wrong-signed profiles are never equilibria. This settles item 4(iii).

**Lemma ES.3 (the pool is always consistent; analytical).** *Fix any order strategies and any measurable $A\subseteq\{\mu_X\ge\tau\}$ with $\tau>\tfrac12$. Then the pool posterior satisfies $\bar\mu_N\le\tfrac12<\tau$. With the price and beliefs of Lemma F.1, the challenger's and the market maker's conditions hold.*

*Proof.* By the tower property, $\tfrac12=\Pr(X\in A)\,\Pr(H\mid X\in A)+\Pr(X\in N)\,\bar\mu_N$. If $\Pr(X\in A)>0$, then $\Pr(H\mid X\in A)=\mathbb E[\mu_X\mid X\in A]\ge\tau>\tfrac12$, so $\bar\mu_N<\tfrac12$. If $\Pr(X\in A)=0$, then $\bar\mu_N=\tfrac12$. On $A$ the price $t_L+\Delta_T\mu_X$ reveals $\mu_X\ge\tau$, so preparation is optimal. At $t_0$ the belief $\bar\mu_N<\tau$ makes non-preparation strictly optimal. Pricing is competitive on each region by Lemma F.1(a). $\square$

This generalizes (F.2), which used the cutoff structure. Only the investor's optimality restricts the entry set. Any measurable subset of $\{\mu_X\ge\tau\}$ is a candidate.

**Lemma ES.4 (shape of the two payoffs; analytical).** *Let $\underline a=\operatorname{ess\,inf}A$.*

*(a) If $\underline a\ge0$, then $F_L(s)=e^{-s/b}F_L(0)$ on $[0,1]$. If $F_L(0)>0$, the low type's payoff $U_L(s)=s\big(F_L(0)e^{-s/b}-k\big)$ is strictly concave on $[0,1]$. Its unique maximizer is $0$ if $F_L(0)\le k$; it is $1$ if $(1-1/b)e^{-1/b}F_L(0)\ge k$; otherwise it is the unique root of $F_L(0)e^{-s/b}(1-s/b)=k$.*

*(b) On $[0,\min\{\underline a,1\}]$, $F_H(s)=e^{s/b}F_H(0)$. If $F_H(0)>0$, $U_H(s)=s\big(F_H(0)e^{s/b}-k\big)$ is strictly convex there.*

*Proof.* (a) On $A$, $x+s\ge0$, so $f(x+s)=e^{-s/b}f(x)$. Then $U_L''=F_L(0)e^{-s/b}(s/b-2)/b<0$ for $s<2b$, and $b>1$. The marginal profit $F_L(0)e^{-s/b}(1-s/b)-k$ is strictly decreasing, which gives the three cases. (b) On $A$, $x\ge s$, so $f(x-s)=e^{s/b}f(x)$, and $U_H''=F_H(0)e^{s/b}(2+s/b)/b>0$. $\square$

**Lemma ES.5 (the two types see the same total residual; analytical).** *Against any schedule with entry set $A$,*
$$\mathbb E_{\sigma_H}\big[F_H(S)\big]=\mathbb E_{\sigma_L}\big[F_L(S')\big]=\Delta_T\int_A\frac{a_H(x)\,a_L(x)}{a_H(x)+a_L(x)}\,dx,$$
*where $S$ and $S'$ are the magnitudes of the two types' orders.*

*Proof.* Integrate $F_H$ against $\sigma_H$: $\Delta_T\int_Aa_H(1-\mu_X)=\Delta_T\int_Aa_Ha_L/(a_H+a_L)$. Integrate $F_L$ against $\sigma_L$: $\Delta_T\int_Aa_L\mu_X$, the same integral. $\square$

Under pure full orders this is $F_H(1)=F_L(1)=J_A$, which is (A.7). Table T10 checks it on mixed profiles to $10^{-17}$.

**Proposition ES.2 (structure of all equilibria; analytical).** *Suppose $\tau(r)>\hat\mu$. On the benchmark this holds at every $r\in(\ell,h)$, since $\tau(\ell)=0.625>0.62246$ and $\tau$ increases in $r$. Then in every equilibrium:*

*(a) $\mu_X\le\hat\mu<\tau$ on $x\le0$, so $A\subseteq[x^*,\infty)$ with $x^*>0$.*

*(b) The low type plays one pure order $-z$, $z\in[0,1]$.*

*(c) If the equilibrium is live, then $z>0$, $U_L(z)>0$, $\max U_H>0$, and $\sigma_H$ puts no mass on $[0,\underline a]$. If $\underline a\ge1$, then $\sigma_H=\delta_1$.* [Referee fix: the clause "no mass on $[0,\underline a]$" holds only when $\underline a<1$, which is the case the proof treats. When $\underline a\ge1$ the set $[0,\underline a]$ contains $1$, and $\sigma_H=\delta_1$ puts all its mass there, as in the plateau equilibria of Proposition ES.5. Read: if $\underline a<1$, $\sigma_H$ puts no mass on $[0,\underline a]$; if $\underline a\ge1$, $\sigma_H=\delta_1$.]

*(d) If the equilibrium is live and $z<1$, then $U_L=kz^2/(b-z)$ and $\mathbb E_{\sigma_H}[F_H]=kb/(b-z)$. If moreover $\sigma_H=\delta_1$, then $U_H=kz/(b-z)$.*

*Proof.* (a) Take $x\le0$, $q\in[0,1]$, $q'\in[-1,0]$. Then $|x-q|=q-x\ge|x|$, so $|x-q'|-|x-q|\le|x-q'|-|x|\le|q'|\le1$. Hence $f(x-q)\le e^{1/b}f(x-q')$, and integration gives $a_H\le e^{1/b}a_L$, so $\mu_X(x)\le\hat\mu$. Continuity and monotonicity (Lemma ES.2) give $\{\mu_X\ge\tau\}=[x^*,\infty)$ with $x^*>0$. Lemma F.1(c) gives $A\subseteq[x^*,\infty)$.

(b) By (a), Lemma ES.4(a) applies. If $F_L(0)>0$ the low type has a unique best response. If $F_L(0)=0$ then $A$ is null and zero is the unique best response. In equilibrium $\sigma_L$ is supported on the best responses.

(c) If $z=0$, then $a_H/a_L=\int f(x-q)\,d\sigma_H/f(x)\le e^{1/b}$ everywhere, so $\mu_X\le\hat\mu<\tau$ and $A$ is null. So $z>0$. Strict concavity, $U_L(0)=0$ and an interior or corner maximizer at $z>0$ give $U_L(z)>0$, so $F_L(z)>k$. Suppose $\max U_H=0$. Then $F_H(s)\le k$ for every $s\in(0,1]$, and by continuity also at $s=0$. So $\mathbb E_{\sigma_H}[F_H]\le k<F_L(z)$, which contradicts Lemma ES.5. Hence $\max U_H>0=U_H(0)$, and $0$ is not a best response. By Lemma ES.4(b), no point of $(0,\underline a)$ is a maximizer. Now let $\underline a<1$ and suppose $\underline a$ is a maximizer. $U_H$ is $C^1$, since $F_H'(s)=\tfrac1b\Delta_T\int_A\operatorname{sign}(x-s)f(x-s)(1-\mu_X)\,dx$ is continuous by dominated convergence. So $U_H'(\underline a)=0$. Strict convexity on $[0,\underline a]$ then gives $U_H'<0$ on $(0,\underline a)$ and $U_H(0)>U_H(\underline a)$, a contradiction. If $\underline a\ge1$, $U_H$ is strictly convex on $[0,1]$ and the maximum is at $1$.

(d) For interior $z$, Lemma ES.4(a) gives $F_L(z)=F_L(0)e^{-z/b}=k/(1-z/b)$. Then $U_L=z(F_L(z)-k)=kz^2/(b-z)$, and Lemma ES.5 gives the expectation. With $\sigma_H=\delta_1$, $U_H=F_H(1)-k=kz/(b-z)$. $\square$

Part (d) says something sharp. In every live equilibrium with an interior low-type order, the investor's profits depend only on $k$, $b$ and $z$. [Referee fix: for the high type this holds when $\sigma_H=\delta_1$. Without that, (d) pins only $\mathbb E_{\sigma_H}[F_H]$, not $U_H$.] They do not depend on $\Delta_T$ or on the entry set. The fork's table confirms it: at $r=2$, $z=0.98$ gives $U_H=0.0192$ and $U_L=0.0189$, and the formulas give $0.01922$ and $0.01883$.

### 4.3 The exact region of the minimal-pool full-order equilibrium

**Proposition ES.3 (the sufficient test is exact; analytical, root computer-assisted).** *Suppose $B_r(\tfrac12)<c\le B_r(M)$. Orders $(1,-1)$ with the minimal pool $A=[x^*,\infty)$ form an equilibrium if and only if $(1-1/b)J(r)\ge k$. On the benchmark the set of such $r$ is exactly $[r_J,r_C]$ with*
$$r_J\in[2.0155164410601003,\;2.0155164410601075].$$

*Proof.* Here $x^*>0$ because $\tau>\tfrac12$, so Lemma ES.4(a) applies with $F_L(0)=e^{1/b}F_L(1)=e^{1/b}J$. The low type's best response is $1$ if and only if $(1-1/b)J\ge k$. This is necessity. For sufficiency, take the high type. The pointwise ratio $f(x-s)/f(x-1)\ge e^{-(1-s)/b}$ gives $F_H(s)\ge e^{-(1-s)/b}J$, and $|F_H'|\le F_H/b$ gives $U_H'(s)\ge(1-s/b)F_H(s)-k$. The function $h(s)=(1-s/b)e^{-(1-s)/b}$ has $h'(s)=-(s/b^2)e^{-(1-s)/b}$, so it strictly decreases on $(0,1]$. So $U_H'(s)>(1-1/b)J-k\ge0$ on $[0,1)$, and $1$ is the unique best response. Wrong signs are dominated (Lemma ES.2). The challenger and the market maker are covered by Lemma ES.3.

Benchmark root. $\Delta_T$ increases on $r>\ell$. The threshold $\tau$ increases on $r>\ell$, because $c-g_L$ rises and $g_H-g_L=h-r/2-\ell^2/(2r)$ falls. The bracket in (ES.1) decreases in $\tau$. So on a box $[r_a,r_b]$, $J\in[\Delta_T(r_a)K(\tau(r_b)),\,\Delta_T(r_b)K(\tau(r_a))]$, with $K$ the bracket. An adaptive cover of $(\ell,r_C]$ by such boxes, an interval bisection, and an interval enclosure of $J'(r)>0$ on a window of width $10^{-6}$ around the root prove the sign pattern: negative below $r_J$, positive above (Table T1). $\square$

So the fork's "sufficient" test in F.2(c) is necessary as well. The value $2.05$ in the fork's threshold table is the first point of a grid with step $0.05$ above $r_J=2.01552$. Table T3 confirms the result with the quadrature layer and a 2001-point order grid. Both types' best responses are $(1,-1)$ for $r\ge r_J$. Below $r_J$ the low type's best response is interior, for example $-0.9854$ at $r=2$. The high type's best response is $1$ at every tested $r$ (numerical diagnostic). The value $1.66$ belongs to a different equilibrium, with an interior low-type order (Section 4.4).

### 4.4 The live branch and its lower edge

Fix $q_H=1$. By Proposition ES.2(b) the low type plays some $-z$. For $z\ge n(r)$ define

$$C(z,r)=\Delta_T\int_{x^*(z)}^\infty f(x)\mu_X(x)\,dx=\Delta_T\Big[\frac{\arctan e^{(1+z)/(2b)}-\arctan\sqrt{\tfrac\tau{1-\tau}}}{2e^{(1-z)/(2b)}}+\frac{M_z e^{-1/b}}2\Big],\tag{ES.2}$$

$$\Psi(z,r)=C(z,r)\,e^{-z/b}(1-z/b)-k,\tag{ES.3}$$

$$G(r)=\Psi(n(r),r)=\Delta_T(r)\,\frac{1-\tau(r)}2\Big(1+\frac1b-\operatorname{logit}\tau(r)\Big)-k.\tag{ES.4}$$

$C(z,r)$ is $F_L(0)$ against the minimal pool $\mathcal U(z)$, and $\Psi$ is the low type's marginal profit at its own order. The closed form of (ES.2) follows as in Lemma ES.1. With $u=e^{x/b}$ and $\kappa=e^{(1-z)/b}$, $f(x)\mu_X(x)\,dx=\tfrac12\,du/(u^2+\kappa)$ on $[x^*(z),1]$, and $\mu_X=M_z$ on $[1,\infty)$. At $z=n(r)$, $x^*=1$, $M_z=\tau$ and $e^{-(1+n)/b}=(1-\tau)/\tau$, which gives (ES.4).

**Proposition ES.4 (live equilibria with $q_H=1$; benchmark).**

*(a) (analytical) Orders $(1,-z)$ admit an entry set that satisfies the challenger, the market maker and the low type if and only if $z\in[n(r),1]$ and $\Psi(z,r)\ge0$. For $z<1$ the admissible sets are exactly the measurable $A\subseteq\mathcal U(z)$ with $\Delta_T\int_Af\mu_X=C^*(z):=ke^{z/b}/(1-z/b)$. For $z=1$ they are the measurable $A\subseteq\mathcal U(1)$ with $(1-1/b)J_A\ge k$. In every such profile $U_H(1)=kz/(b-z)>U_H(0)$. The high type's global optimality is not implied.* [Referee fix: (i) read "admit an entry set of positive probability". The profile $(1,0)$ with $A$ null satisfies the challenger, the market maker and the low type, and $z=0\notin[n(r),1]$. (ii) For $z=1$ the profit is $U_H(1)=J_A-k\ge k/(b-1)=kz/(b-z)$, with equality only when $(1-1/b)J_A=k$. The equality $U_H(1)=kz/(b-z)$ holds for $z<1$.]

*(b) (computer-assisted) For every $r\in(\ell,r_e)$ there is no live equilibrium with $\sigma_H=\delta_1$, for any entry set. Here $r_e\in[1.6585908245511404,\,1.6585908245511462]$ is the unique zero of $G$ on $(\ell,r_C]$.*

*(c) (computer-assisted) For every $r\in[r_e,r_C]$ the set in (a) is the interval $[n(r),z_U(r)]$. Here $z_U(r)$ is the unique root of $\Psi(\cdot,r)$ for $r<r_J$, and $z_U=1$ for $r\ge r_J$. The map $r\mapsto z_U(r)$ is continuous. It has no fold.*

*Proof.* (a) If $z<n(r)$, then $M_z<\tau$, $\mathcal U(z)$ is empty, and the profile is dead. For $z\ge n(r)$, Lemma ES.3 covers the challenger and the market maker for every $A\subseteq\mathcal U(z)$, and Lemma ES.4(a) applies with $F_L(0)=C_A:=\Delta_T\int_Af\mu_X$. For interior $z$ the low type's condition is $C_Ae^{-z/b}(1-z/b)=k$, that is $C_A=C^*(z)$. As $A$ runs over measurable subsets of $\mathcal U(z)$, $C_A$ takes every value in $[0,C(z,r)]$: the map $t\mapsto C_{[x^*(z),t]}$ is continuous. So an admissible $A$ exists if and only if $C^*(z)\le C(z,r)$, that is $\Psi(z,r)\ge0$. The case $z=1$ is the corner case of Lemma ES.4(a), with $e^{-1/b}C_A=F_L(1)=J_A$ by Lemma ES.5, and $J_A\le J$ gives $\Psi(1,r)\ge0$. The profit formula is Proposition ES.2(d).

(b) By (a), a live equilibrium needs $z\in[n(r),1]$ with $\Psi(z,r)\ge0$. Table T1 gives two interval covers in the variables $(r,t)$ with $z=n(r)+t(1-n(r))$, $t\in[0,1]$. First, $\Psi<0$ on all of $\{(z,r):n(r)\le z\le1,\ \ell<r\le r_e-10^{-5}\}$ (78 boxes, none unresolved). Second, $\partial\Psi/\partial z<0$ on $\{n(r)\le z\le1,\ 1.3\le r\le r_C\}$ (30 boxes, none unresolved). So for $r\in[1.3,r_e)$, $\Psi(z,r)\le\Psi(n(r),r)=G(r)$. A third cover shows $G<0$ on $(\ell,r_e)$ and $G>0$ on $(r_e,r_C]$, with $G'>0$ on a window of width $10^{-6}$ around the root (39 boxes). Together the covers exclude every $z$ for every $r\in(\ell,r_e)$.

(c) Since $\partial\Psi/\partial z<0$ and $G(r)=\Psi(n(r),r)\ge0$ on $[r_e,r_C]$, the set $\{z\ge n(r):\Psi\ge0\}$ is an interval that starts at $n(r)$. It ends at the unique root of $\Psi(\cdot,r)$, or at $1$ when $\Psi(1,r)=(1-1/b)J(r)-k\ge0$, which is $r\ge r_J$. Since $\partial_z\Psi\ne0$, the implicit function theorem makes $z_U$ continuous and rules out a fold, where two roots of $\Psi(\cdot,r)$ would merge with $\partial_z\Psi=0$. $\square$

**Proposition ES.5 (plateau equilibria and the edge; analytical given the sign of $G$).** *Suppose $\tau(r)\in(\hat\mu,M]$, so $n(r)\in(0,1]$, and $G(r)\ge0$. Put $\pi(r)=k/(G(r)+k)\in(0,1]$. Then orders $(1,-n(r))$ with any measurable $A\subseteq[1,\infty)$ with $\int_Af=\pi(r)\int_1^\infty f$, for example $A=[1+b\log(1/\pi),\infty)$, form an equilibrium. Its outcomes are*
$$\mathsf E=\frac{\pi}{4\tau},\qquad \mathsf O_H=\frac\pi4,\qquad U_H=\frac{kn}{b-n},\qquad U_L=\frac{kn^2}{b-n}.$$
*On the benchmark, $G\ge0$ holds exactly on $[r_e,r_C]$ (computer-assisted), so a live equilibrium exists at every $r\in[r_e,r_C]$. At $r=r_e$, $\pi=1$, the entry set is the whole plateau $[1,\infty)$, and $\mathsf E=1/(4\tau(r_e))\in[0.384022801668302,\,0.3840228016683023]$.*

*Proof.* At $z=n$, $M_n=\tau$, so $\mathcal U(n)=[1,\infty)$ and the posterior there equals $\tau$. The tie rule makes preparation optimal on $A$. Lemma ES.3 covers the pool, which includes the rest of the plateau. On the plateau $f\mu_X=\tau f$, so $C_A=\pi C(n,r)$. From (ES.3) and (ES.4), $C(n,r)e^{-n/b}(1-n/b)=G+k$. So $C_Ae^{-n/b}(1-n/b)=k$, and Lemma ES.4(a) makes $n$ the low type's unique best response. Since $\underline a\ge1$, Lemma ES.4(b) makes $U_H$ strictly convex on $[0,1]$, so the best response is $0$ or $1$. By Lemma ES.5, $F_H(1)=F_L(n)=k/(1-n/b)$, so $U_H(1)=kn/(b-n)>0$. Entry: $e_H=\int_Af(x-1)=\pi/2$ and $e_L=\int_Af(x+n)=\tfrac\pi2e^{-(1+n)/b}=\tfrac\pi2\cdot\tfrac{1-\tau}\tau$. So $\mathsf E=\tfrac\pi4(1+\tfrac{1-\tau}\tau)=\pi/(4\tau)$ and $\mathsf O_H=\pi/4$. $\square$

What happens at the edge. The minimal-pool branch $z_U(r)$ and the entry boundary $n(r)$ meet at $r_e$ and cross transversally: their slopes there are about $3.6$ and $0.34$ (Table T2). As $r$ falls to $r_e$, the low type's short shrinks to $n(r_e)=0.24690$. The entry set shrinks to the plateau atom $\{X\ge q_H\}$, where the challenger is exactly indifferent. Below $r_e$ no admissible low-type order exists, and only $\mathcal D$ remains with $\sigma_H=\delta_1$. [Referee fix: $\mathcal D$ has $\sigma_H=\delta_0$. Read: below $r_e$ no live equilibrium with $\sigma_H=\delta_1$ exists, so among such profiles only $\mathcal D$ remains.] Entry along the live set jumps from $0.38402$ to $0$. This is a boundary collision of a fixed point with the edge of the region where entry is possible. It is not a fold: $\partial_z\Psi<0$ everywhere (certified), so two branches never merge. It is also not a vanishing of the investor's incentive: at the edge $U_H=0.0028167>0$. The binding margin is the low type's. At the smallest order that makes the top flows credible, its marginal profit just covers $k$; this is $G(r_e)=0$. The fork's grid found the edge between $1.65$ and $1.66$, and the first grid fixed point at $1.66$ had $q_L=-0.25$. This agrees with $r_e=1.65859$ and $z_U(1.66)=0.2520$.

The live branch, refined (Table T2, numerical diagnostic). On $[r_e,r_J]$ the minimal-pool member has $z_U$ rising from $0.2469$ to $1$. Entry rises from $0.38402$ at $r_e$ to its peak $0.39406$ at $r_J$, then falls to $0.34197$ at $r_C$. The fall on $[r_J,r_C]$ is Proposition F.4, because the experiment is fixed there. The rise on $[r_e,r_J]$ is numerical. At every row the low type's quadrature best response equals $-z_U$ to $3\times10^{-8}$, and the high type's global best response is $1$ with zero gap.

### 4.5 Outside the cutoff family

**Proposition ES.6 (entry sets with holes at full orders; analytical).** *Suppose $B_r(\tfrac12)<c\le B_r(M)$ and let $G_0(r)=k/[(1-1/b)\Delta_T(r)]$.*

*(a) Orders $(1,-1)$ with entry set $A$ form an equilibrium if and only if $A$ is a measurable subset of $[x^*,\infty)$ with $\int_Ag\ge G_0$.*

*(b) Entry over this family is largest at $A=[x^*,\infty)$. It is smallest at $A=[x^*,y]$ with $\int_{x^*}^yg=G_0$ (and at any $[x^*,1)\cup P$ with $P\subseteq[1,\infty)$ of the same $g$-mass). Every value in between is attained.* [Referee fix: the parenthetical alternative applies only when $y\ge1$, that is $\int_{x^*}^1g\le G_0$. If $y<1$ the least-entry set is $[x^*,y]$ up to null sets, because the ratio $\mu_X(1-\mu_X)$ is strictly decreasing on $[x^*,1)$. At $r=3$, $y=1.9589$, so the alternative applies there.]

*(c) When $A$ is bounded above, the price is not monotone in the flow: the highest flows pool with the lowest flows at $t_0$.*

*Proof.* (a) Necessity: Lemma F.1(c) gives $A\subseteq[x^*,\infty)$, and the low type's condition at $1$ is $(1-1/b)J_A\ge k$ by Lemma ES.4(a). Sufficiency: Lemma ES.3 covers the challenger and the market maker. Lemma ES.5 gives $F_H(1)=F_L(1)=J_A$. The ratio bound $F_H(s)\ge e^{-(1-s)/b}J_A$ holds pointwise for every $A$, and $|F_H'|\le F_H/b$ holds for every nonnegative bounded residual. So the argument of Proposition ES.3 gives $U_H'>0$ on $[0,1)$. (b) Entry is $\tfrac12\int_A(a_H+a_L)$, and $g=(a_H+a_L)\mu_X(1-\mu_X)$. On $\mu_X\ge\tau>\tfrac12$ the ratio $\mu_X(1-\mu_X)$ decreases in $\mu_X$, so it is nonincreasing in $x$. The bathtub principle then says: to reach $g$-mass $G_0$ with least entry, take the flows with the largest ratio first, which is $[x^*,y]$. On the plateau the ratio is constant at $Mm$, so any plateau subset with the right $g$-mass ties. The map $y\mapsto\tfrac12\int_{x^*}^y(a_H+a_L)$ is continuous and increasing, which gives every intermediate value. (c) The price is $t_L+\Delta_T\mu_X>t_0$ on $A$ and $t_0$ above $y$. $\square$

At $r=3$, $G_0=0.06$, while $\int_{x^*}^\infty g=0.1433$ and $\int_1^\infty g=m/2=0.1345$. So every measurable $A$ with $[1,\infty)\subseteq A\subseteq[x^*,\infty)$ works, including the plateau alone. Entry over the full-order family ranges over $[0.15195,\,0.36368]$. The least-entry set is $[x^*,1.9589]$. The cutoff family alone covers $[0.15258,\,0.36368]$. Holes extend the range by only $0.0006$ at $r=3$ (Tables T5 and T6). Holes matter more for the form of the price than for the outcome.

The whole family with $q_H=1$. Proposition ES.4(a) gives, for each supported $z$, a continuum of entry sets. The same bathtub argument applies, now with the ratio $f\mu_X/(a_H+a_L)=e^{z/b}\mu_X(1-\mu_X)$ on $x\ge0$. So the least-entry set for each $z$ is again an interval $[x^*(z),y]$ (Table T8). The least entry over all members we construct is the plateau equilibrium of Proposition ES.5: $0.1147$ at $r=3$, against $0.3637$ for the minimal pool. The two curves bound the shaded band in panel (a) of the figure. The members we construct fill the band; we found none above the minimal-pool curve (numerical diagnostic). Table T7 shows that the cutoff family alone already supports every $z\in[n(r),z_U(r)]$, with both best responses verified by quadrature. At $r=3$ that is $z\in[0.7424,1]$.

Mixed orders. Proposition ES.2 settles most of item 4(ii) analytically. The low type never mixes. The high type puts no mass on $[0,\underline a]$, and $\sigma_H=\delta_1$ whenever $\underline a\ge1$. [Referee fix: "no mass on $[0,\underline a]$" when $\underline a<1$; see the fix to Proposition ES.2(c).] A mixed equilibrium would need the high type's payoff to have two global maximizers in $(\underline a,1]$. We scanned the high type's payoff curve against 3,315 pure-order schedules and 2,840 schedules with mixed profiles and holed entry sets (Table T9). We found no interior local maximum in any of them. The high type's best response was always $0$ or $1$. [Referee fix: the pure-order scan (`pure_scan.csv`) tests where the global best response lies, not interior local maxima. The 2,840 "mixed" schedules include pure high-type profiles (weight one on $q_H=1$). The mixed scan starts at $r=1.66$, so it gives no evidence below $r_e$.] Status: numerical diagnostic. So every live equilibrium we find is pure with $q_H=1$. Whether a mixed high-type equilibrium exists is open.

**Remark ES.1 (preparation mixed at the indifferent atom; analytical).** The fork's tie rule makes the indifferent challenger prepare. Suppose instead it may prepare with any probability $\pi$ at a price where it is indifferent. Then at $z=n(r)$ the plateau price atom with probability $\pi(r)=k/(G+k)$ gives a further branch on $[r_e,r_C]$. Its outcomes coincide with those of Proposition ES.5: on the plateau, $f$, $a_H$ and $a_L$ are proportional, so mixing over the whole atom and preparing on a fixed share of it give the same entry, ownership and profits (Table T11). The relaxation adds no new outcome.

## 5. Numerics

All numerics use the quadrature layer `core.py`. It applies composite Gauss–Legendre integration on each smooth piece between breakpoints, and it integrates the tails exactly, where the posterior is constant. Every closed form above agrees with it to $10^{-15}$. Certificates use outward interval arithmetic (mpmath.iv, 40 digits) on exact decimal inputs. The full tables are in `tables.md`; the key rows follow.

Thresholds on the benchmark.

| object | value | status |
|---|---|---|
| $\mathfrak r(k)$: below it, $\mathcal D$ is unique (F.1(iv)) | $1.2209975$ | computer-assisted enclosure |
| $r_e$: lower edge of live equilibria with $q_H=1$ | $[1.6585908245511404,\,1.6585908245511462]$ | computer-assisted |
| $n(r_e)$: low-type order at the edge | $0.2469019$ | computer-assisted |
| $r_J$: lower edge of the minimal-pool full-order equilibrium | $[2.0155164410601003,\,2.0155164410601075]$ | computer-assisted |
| $r_C$: above it, $\mathcal D$ is unique (F.1(iii)) | $3.5926585$ | computer-assisted enclosure |
| fork's first grid point with a live fixed point | $1.66$ | grid value consistent with $r_e$ |
| fork's first grid point passing the F.2(c) test | $2.05$ | grid value consistent with $r_J$ |

The minimal-pool live branch (Table T2; numerical diagnostic, except where marked).

| $r$ | $q_L$ | $x^*$ | $\mathsf E$ | $\mathsf O_H$ | $U_H$ | $U_L$ |
|---|---|---|---|---|---|---|
| $r_e=1.65859$ | $-0.2469$ | $1.0000$ | $0.38402$ | $0.2500$ | $0.00282$ | $0.00070$ |
| 1.70 | $-0.3856$ | $0.9377$ | $0.38666$ | $0.2577$ | $0.00478$ | $0.00184$ |
| 1.80 | $-0.6459$ | $0.8247$ | $0.39081$ | $0.2710$ | $0.00954$ | $0.00616$ |
| 1.90 | $-0.8358$ | $0.7471$ | $0.39300$ | $0.2797$ | $0.01436$ | $0.01200$ |
| 2.00 | $-0.9806$ | $0.6922$ | $0.39399$ | $0.2857$ | $0.01924$ | $0.01887$ |
| $r_J=2.01552$ | $-1$ | $0.6852$ | $0.39406$ | $0.2864$ | $0.02000$ | $0.02000$ |
| 2.50 | $-1$ | $0.7732$ | $0.37982$ | $0.2768$ | $0.04754$ | $0.04754$ |
| 3.00 | $-1$ | $0.8712$ | $0.36368$ | $0.2656$ | $0.07550$ | $0.07550$ |
| 3.59 | $-1$ | $0.9994$ | $0.34207$ | $0.2501$ | $0.10567$ | $0.10567$ |

The first row is the analytical edge equilibrium of Proposition ES.5. At $r_J$, $U_H=U_L=J-k=k/(b-1)=0.02$ exactly, because $(1-1/b)J=k$ there.

The range of live outcomes across strengths (`entry_band.csv`, numerical diagnostic). Least entry is $\pi/(4\tau)$ from Proposition ES.5.

| $r$ | supported $z$ | least $\mathsf E$ | minimal-pool $\mathsf E$ |
|---|---|---|---|
| 1.70 | $[0.261,\,0.386]$ | 0.352 | 0.387 |
| 2.00 | $[0.365,\,0.981]$ | 0.219 | 0.394 |
| 2.50 | $[0.546,\,1]$ | 0.142 | 0.380 |
| 3.00 | $[0.742,\,1]$ | 0.115 | 0.364 |
| 3.50 | $[0.958,\,1]$ | 0.108 | 0.346 |

The figure `equilibrium_set.pdf` has two panels. Panel (a) shows entry against $r$: the minimal-pool member (solid), the least-entry member $\pi/(4\tau)$ (dashed), the band between them, and $\mathcal D$ at zero. The shaded strip on the left is $r<\mathfrak r(k)$. Dotted lines mark $r_e$, $r_J$ and $r_C$. Panel (b) shows the supported low-type orders $[n(r),z_U(r)]$.

Below the edge (Table T4). On $[1.30,r_e)$ the maximum of $\Psi(\cdot,r)$ over $z\in[n(r),1]$ is attained at $z=n(r)$ and equals $G(r)<0$. At $r_e-10^{-7}$ it is $-4.3\times10^{-9}$. This agrees with the certified covers.

## 6. What this means for "when is the investor an insider"

1. **The threshold is $r_e$, and it has a closed-form equation.** On the benchmark an equilibrium in which the investor is an insider exists at $r$ if and only if $r\in[r_e,r_C]=[1.6586,\,3.5927]$. The "only if" part is computer-assisted for every equilibrium with $\sigma_H=\delta_1$ (Proposition ES.4(b)). For any other high-type strategy, an interior pure order or a mixture, it is a numerical diagnostic. Above $r_C$ it is analytical (Proposition F.1(iii)). The "if" part is analytical given the sign of $G$ (Proposition ES.5). So in Proposition F.3, $r_1$ can be any strength in $[r_e,r_C]$, not only one near $3$. [Referee fix: Proposition F.3(ii) asserts full orders $(1,-1)$, and (F.5) has strict inequalities. As stated, it needs $r_1\in(r_J,r_C)$, since no full-order equilibrium exists below $r_J$ (Propositions ES.3 and ES.6). The claim for all of $[r_e,r_C]$ holds for a modified F.3(ii) that asserts informed orders $(1,-z)$ with $z\in[n(r_1),1]$, entry at least $\pi/(4\tau)>0$, and a nonconstant, state-dependent price.] The insider condition is $G(r)\ge0$:
$$\Delta_T(r)\,\frac{1-\tau(r)}2\,\Big(1+\frac1b-\operatorname{logit}\tau(r)\Big)\ge k.$$
It reads as follows. The informed short must be just large enough, $z=n(r)$, that the highest flows lift the market's posterior to the challenger's threshold $\tau$. At that order the short's marginal profit must cover $k$. Competition raises $\Delta_T$ and so relaxes this; it also raises $\tau$, which requires a larger short. The first effect wins until $r_C$.

2. **The binding insider is the seller, not the buyer.** At the edge the high type earns $0.0028$, well above zero, while the low type's marginal profit is exactly zero. [Referee fix: this compares a level with a marginal. The low type's level profit at the edge is also positive, $kn^2/(b-n)=0.0007$, and its marginal profit is zero at every interior optimum. The binding fact is that below $r_e$ the low type's marginal profit at the smallest entry-enabling short $n(r)$ is negative, $G(r)<0$, so it would short less than $n(r)$, and a smaller short kills entry.] The buy side is profitable whenever any entry exists. The short side is what makes high flows credible, and it is the margin that fails first.

3. **Materiality appears with a jump.** Entry in live equilibria jumps from $0$ to $0.384$ at $r_e$. Entry falls continuously to zero nowhere in the live set. This sharpens F.2(b): the live set does not reach $\mathcal D$ continuously in $r$ either.

4. **Rents are pinned by the short.** In every live equilibrium with an interior short $z$, $U_H=kz/(b-z)$ and $U_L=kz^2/(b-z)$, whatever the entry set (Proposition ES.2(d)). [Referee fix: the formula for $U_H$ needs $\sigma_H=\delta_1$; the formula for $U_L$ holds in general.] Across the live set at a given $r$, the investor's rent ranges with $z$ over $[n(r),z_U(r)]$. The least informed live equilibrium gives the insider the least rent.

5. **The insider's information can be material on odd sets.** Any measurable subset of $\{\mu_X\ge\tau\}$ with enough $g$-mass supports full informed trading (Proposition ES.6). The price can fall back to $t_0$ at the strongest buy flows. Materiality is a property of the price partition, not of the flow ordering. Outcomes move little across holes, though. At $r=3$ entry in full-order equilibria spans $[0.152,0.364]$ with or without holes. [Referee fix: with holes the span is $[0.15195,0.36368]$; without holes (the cutoff family) it is $[0.15258,0.36368]$, which rounds to $[0.153,0.364]$.] Across all live equilibria with $q_H=1$ it spans at least $[0.115,0.364]$.

6. **Wrong-signed and mixed insiders do not appear.** [Referee fix: the heading overstates. Analytically, wrong-signed orders never occur and the short never mixes. A high-type mixture over two points of $(\underline a,1]$ is not excluded; it is open (Section 7, item 1).] Wrong-signed orders never occur. The low type never mixes. The high type never puts mass near zero, so it never mixes between trading and abstaining (Proposition ES.2). So an insider, when it exists, always trades on its information in the right direction, and the short is deterministic.

## 7. Open items and the next best step

1. **High-type orders other than $1$ (open; numerical diagnostic says none).** Proposition ES.2 leaves one case: a global maximizer of $U_H$ inside $(\underline a,1)$, which an interior pure order or a mixture would need. At a critical point, $U_H''=2(k-F_H)/s+s(F_H-\Delta_T(1-\mu_X(s))\mathbf 1_A(s))/b^2$. The first term is negative, because $F_H>k$ at any profitable order. A sign argument for this expression would make "every live equilibrium is pure with $q_H=1$" analytical. Then Section 6.1 becomes an exact, computer-assisted characterization of when the investor is an insider. This is the next best step.
2. **Largest entry at a fixed strength (open).** We show that the minimal-pool member is the largest-entry member we construct. A bathtub argument in the other direction, over $z$ and $A$ jointly, should settle it.
3. **The high type's optimality for arbitrary admissible $A$ with interior $z$ (numerical diagnostic).** It holds at every sampled set: cutoff representatives, least-entry intervals, holed sets.
4. **Robustness of the plateau equilibria (open).** In Proposition ES.5 the challenger is exactly indifferent on the whole entry set. A refinement, for example a small random cost around $c$, might select against them. With $\rho>0$, Proposition F.5 already selects the minimal pool.
5. **Beyond the benchmark (open).** The condition $\tau>\hat\mu$ drives Proposition ES.2. It holds on the whole benchmark domain, with little slack ($0.625$ against $0.6225$ at $r=\ell$). When it fails, entry can reach flows with $x<0$, and the low type's payoff can lose concavity. A version without this condition is open.
