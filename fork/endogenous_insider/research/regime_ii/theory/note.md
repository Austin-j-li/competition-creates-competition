---
title: "Proposition 2 without the floor: the regime II test"
subtitle: "Theory track, regime II team"
date: "2026-10-03"
---

This note belongs to `fork/endogenous_insider/research/regime_ii/`. It uses the notation of `paper/main.md` and of `research/cost_distribution/note.md` (the CD note). Equation numbers (4) to (12) and (A.1) to (A.14) refer to the paper. Results CD.1 to CD.15 are the CD note's. Results R.1 to R.12 and Proposition 2' are new. Each result carries its status: analytical, computer-assisted, numerical diagnostic, or open. Numbers come from the CSV files in this folder (Section 6).

## 1. Question and short answer

Proposition 2 assumes the floor (A1): $0\le c_L<B_{r_1}(m)$. The cheap type then prepares at every belief. We replace (A1) by the regime II condition at $r_1$,

$$
B_{r_1}(m)<c_L<B_{r_1}(\tfrac12),
\tag{A1$'$}
$$

with a strict lower end. At $c_L=B_{r_1}(m)$ the tie rule makes the cheap type prepare at belief $m$, so that case is regime I and the paper's proof applies. The upper end may be weak for the structural lemmas; Proposition 2' needs it strict.

Under (A1') the cheap type exits after bad prices. Entry at $r_1$ is $\rho\Pr(\mu_P\ge\tau_L)+(1-\rho)\Pr(\mu_P\ge\tau_H)$, and the first term can fall below $\rho$.

**Short answer.**

1. Part (i) survives unchanged (Lemma R.1, analytical).
2. Part (ii) survives only in part. Under the right side of (A3), every equilibrium at $r_1$ has correctly signed informed trading and an informative price that strictly Blackwell dominates the $r_0$ price (analytical). But every equilibrium also has a pool at the no-entry price, so the investor is never an insider at every price, and on-path entry is never unique (Lemma R.3, Proposition R.7, analytical). [Referee fix: the last clause needs two equilibria with different entry. Proposition R.7 supplies them only under $k\le K(c_L)$. Under the right side of (A3) alone, Proposition CD.7(d) supplies full-order half-line equilibria with cutoffs in $[z_0,z_0+\varepsilon)$ whenever $k<(1-\frac1b)J_G(z_0)$, and $J_G(z_0)\ge\Delta_Tm/2$ makes this hold for every $\rho\le\frac12$. At the benchmark $b$, $c_H$, $r_1$ it holds for every $\tau_L$ when $\rho<0.699$. For larger $\rho$, $\tau_L$ near $\frac12$ and $k$ near the (A3) bound, $J_G(z_0)<\rho m\Delta_T$ (for example $\rho=0.9$, $\tau_L=0.49$: $J_G(z_0)/\Delta_T=0.2036<\rho m=0.2420$), and non-uniqueness of entry is open there.]
3. The entry and ownership claims need two new conditions. A smaller trading cost, $k\le K(c_L)$, forces full orders in every equilibrium (Proposition R.6). Then entry exceeds $\rho$ in every equilibrium if and only if $c_L$ lies below an exact "bathtub" threshold (Proposition R.7). At the benchmark, $\rho=0.25$, the thresholds are $c_L\le3.4607$ for entry and $c_L\le3.7408$ for ownership. This is Proposition 2' (analytical; threshold values are double-precision evaluations of closed forms).
4. The paper's (A3) is not enough. At the benchmark trading cost $k=0.02$, which satisfies (A3), equilibria with entry at most $0.112$ exist for every $c_L>2.9844$ (the starved family, Proposition R.10; numerical diagnostic, because the high type's check is a grid check). A fully analytical half-line family gives entry below $\rho$ for $c_L>3.6498$ and ownership below $\rho/2$ for $c_L>3.8945$ (Proposition R.9). [Referee fix: starved members with cutoff $x'\ge1$ are analytical (see the note after Proposition R.10), so at $k=0.02$ entry and ownership both fail analytically for $c_L>3.4211$.]
5. Part (iii), as stated, is vacuous under (A1'), because it assumes $c_L<B_{r_2}(m)<B_{r_1}(m)$. Its replacement is stronger: at every $r_2>r_1$ with $B_{r_2}(M)<c_H$, entry is strictly below $\rho$ in every equilibrium (Proposition R.12, analytical).

The mechanism behind the failures is new. In regime II, bad prices push the cheap type out. A pool at the no-entry price removes the short seller's residual on low flows. The low type then shorts less. A short below $v_H=b\operatorname{logit}\tau_H-1$ keeps every belief below $\tau_H$, so information never recruits the expensive type and only destroys cheap entry. In these equilibria a stronger incumbent creates less competition, not more.

## 2. Setting and notation

All objects are at $r=r_1$ unless a subscript says otherwise. Entry at a revealed belief $\mu$ is

$$
\varphi(\mu)=\rho\,\mathbf 1\{\mu\ge\tau_L\}+(1-\rho)\,\mathbf 1\{\mu\ge\tau_H\},\qquad
\tau_L=B_{r_1}^{-1}(c_L),\quad \tau_H=B_{r_1}^{-1}(c_H).
$$

(A1') means $m<\tau_L<\tfrac12$. (A2) gives $\tfrac12<\tau_H<M$, because $B_{r_1}(\tfrac12)<B_{r_0}(\tfrac12)<c_H$ by (5).

Write $F,S,f$ for the CDF, survival function, and density of the Laplace noise $Z$. We use these objects.

| symbol | definition | benchmark ($r_1=3$) |
|---|---|---|
| $z_0$ | $\tfrac b2\operatorname{logit}\tau_L\in(-1,0)$: the forced pool under full orders is $(-\infty,z_0)$ | $-0.641$ at $c_L=3$ |
| $x^*$ | $\tfrac b2\operatorname{logit}\tau_H\in(0,1)$: expensive entry under full orders on $[x^*,\infty)$ | $0.8712$ |
| $\bar\mu(x')$ | $F(x'-1)/[F(x'-1)+F(x'+1)]$: belief of the pool $(-\infty,x')$ under full orders (CD.7(b)) | |
| $\bar x$ | the root of $\bar\mu(\bar x)=\tau_L$; it exists and exceeds $-1$ because $m<\tau_L<\tfrac12$ | $0.593$ at $c_L=3$ |
| $\bar\pi$ | $\tfrac12[F(\bar x-1)+F(\bar x+1)]$: the pool cap | $0.591$ at $c_L=3$ |
| $S_X(z)$ | $\Pr(X\ge z)$ under full orders $=\tfrac12[S(z-1)+S(z+1)]$ | |
| $\beta_d(u)$ | $F(F^{-1}(u)+d)$ for $u\in(0,1)$, $\beta_d(0)=0$, $\beta_d(1)=1$ | |
| $v_H$ | $b\operatorname{logit}\tau_H-1=2x^*-1$: the largest short that keeps beliefs below $\tau_H$ when $q_H=1$ | $0.7424$ |
| $K(c_L)$ | $(1-\tfrac1b)\rho\,\Delta_T\min\{\tau_L S(\bar x+1),\,m\,S(\bar x)\}$ | $0.00648$ at $c_L=3$ |

Benchmark: $(h,\ell,p,b,k,\rho,c_H)=(10,1,0.5,2,0.02,0.25,6)$, $r_0=1.2$, $r_1=3$. At $r_1$: $\Delta_T=2/3$, $m=0.26894$, $B(m)=2.36618$, $B(\tfrac12)=4.29167$, $B(M)=6.21715$, $\tau_H=0.705$. The right side of (A3) is $(1-\tfrac1b)\rho m\Delta_T=0.022412$. At $r_0$: $\Delta_T=0.016667<k$, $B_{r_0}(\tfrac12)=4.80417$.

Equilibrium is the paper's definition. Lemma CD.2 applies with $G$ the two-point law: $P=t_0$ on the pool $N$, $P>t_0$ on $A=N^c$; on $A$ the price reveals $\mu_X$ and $e=\varphi(\mu_X)$; $N$ contains $Z_0=\{\varphi(\mu_X)=0\}=\{\mu_X<\tau_L\}$; if $\Pr(N)>0$ the pool belief $\bar\mu_N=\Pr(H\mid X\in N)$ is below $\tau_L$; and $A_H=e\Delta_T(1-\mu_X)$, $A_L=e\Delta_T\mu_X$. Entry and ownership are

$$
\mathsf E=\rho\Pr(A)+(1-\rho)\Pr(A\cap\{\mu_X\ge\tau_H\}),\qquad
\mathsf O_H=\tfrac12e_H,\quad e_H=\rho\Pr(A\mid H)+(1-\rho)\Pr(A\cap\{\mu_X\ge\tau_H\}\mid H).
\tag{R.0}
$$

So $\mathsf E-\rho=(1-\rho)\Pr(A\cap\{\mu_X\ge\tau_H\})-\rho\Pr(N)$: information gains expensive entry after good news and loses cheap entry after bad news.

## 3. What survives in every equilibrium

**Lemma R.1 (the weak incumbent; analytical).** *Suppose $c_L\le B_{r_0}(\tfrac12)<c_H$ and $\Delta_T(r_0)<k$. Then at $r_0$ the unique trading outcome is $q_H=q_L=0$, the price is constant, entry is $\rho$, and $\mathsf O_H=\rho/2$. Under (A1') and (A2), $c_L<B_{r_1}(\tfrac12)<B_{r_0}(\tfrac12)$, so part (i) of Proposition 2 holds for every $c_L$ in regime II at $r_1$.*

*Proof.* By Lemma CD.2(d), $0\le A_\theta\le\Delta_T(r_0)\max\{\mu_X,1-\mu_X\}\le\Delta_T(r_0)$ against every candidate schedule. A correctly signed order of size $s>0$ earns at most $s[\Delta_T(r_0)-k]<0$, and a wrong-signed order earns at most $-ks<0$. So zero is the unique best response of both types. Then $X=Z$, $\mu_X\equiv\tfrac12$, and $\varphi(\tfrac12)=\rho>0$, so $Z_0$ is empty. A pool would need belief $\tfrac12$ with $\varphi(\tfrac12)=0$, which fails, so $N$ is null. The price is $t_0+\rho[w_L+\Delta_T/2]$ and entry is $\rho$ in both states. $B_r(\tfrac12)$ falls in $r$ by (5). $\square$

**Lemma R.2 (signs and monotone posteriors; analytical).** *At any strength and in every equilibrium, $\sigma_H$ puts no mass on $[-1,0)$ and $\sigma_L$ puts no mass on $(0,1]$. Then $\mu_X$ is nondecreasing in $x$. Hence $Z_0=\{\mu_X<\tau_L\}$ is a lower half-line and $\{\mu_X\ge\tau_H\}$ is an upper half-line.*

*Proof.* The high type's payoff from an order $q$ is $q\int f(x-q)A_H(x)\,dx-k|q|$. For $q<0$ this is at most $-k|q|<0$, since $A_H\ge0$; the order $0$ earns $0$. So no $q<0$ is a best response. The low type is symmetric. For monotonicity take $x>y$. Then

$$
a_H(x)a_L(y)-a_H(y)a_L(x)=\iint\big[f(x-q)f(y-q')-f(y-q)f(x-q')\big]\,\sigma_H(dq)\,\sigma_L(dq').
$$

Every pair in the supports has $q\ge0\ge q'$. The Laplace density is log-concave, so $f(x-q)$ is totally positive of order two in $(x,q)$, and the bracket is nonnegative when $x>y$ and $q\ge q'$. Hence $a_H/a_L$ and $\mu_X$ are nondecreasing. $\square$

**Lemma R.3 (informed trading and unavoidable pools; analytical).** *(a) Every equilibrium at $r_1$ has an informative price if and only if $\rho\Delta_T(r_1)>2k$. Then $\sigma_H\ne\sigma_L$, some type trades with positive probability, and the price strictly Blackwell dominates the constant price at $r_0$. (b) If $k<(1-\tfrac1b)\rho m\Delta_T(r_1)$, the right side of (A3), then every equilibrium at $r_1$ has a pool of positive probability. On it $\theta$ is immaterial, so the investor is not an insider at every price.*

*Proof.* (a) Under (A1') and (A2), $\varphi(\tfrac12)=\rho$. Proposition CD.4 says an uninformative equilibrium exists if and only if $\Delta_T\varphi(\tfrac12)\le2k$, and that every such equilibrium has zero orders. Conversely, if $\sigma_H=\sigma_L$ then $\mu_X\equiv\tfrac12$ and the price is uninformative. An informative price law depends on $\theta$; no kernel applied to a constant experiment produces it, while a constant kernel applied to it reproduces the $r_0$ experiment. (b) Suppose $N$ is null. Then $Z_0$ is null, so $\mu_X\ge\tau_L$ and $e=\varphi(\mu_X)\ge\rho$ for almost every $x$. Lemma CD.2(d) gives $A_H\ge\rho\Delta_T(1-\mu_X)\ge\rho m\Delta_T$ and $A_L\ge\rho\Delta_T\mu_X\ge\rho\tau_L\Delta_T>\rho m\Delta_T$ almost everywhere, hence under every deviation. The argument of (A.6) gives $U_\theta'(s)>0$ on $[0,1]$, so both types play full orders. Under full orders $\mu_X=m<\tau_L$ on $(-\infty,-1]$, which has probability $\tfrac14(1+e^{-2/b})>0$. So $Z_0$ is not null, a contradiction. On $N$, $e=0$, and Lemma CD.1 gives zero materiality. $\square$

Part (b) is the first qualitative loss. In regime I the price reveals $\mu_X$ everywhere. In regime II every equilibrium has a no-entry price, and the right side of (A3) is exactly what makes the pool unavoidable.

### 3.1 The pool cap

**Lemma R.4 (a likelihood-ratio bound; analytical).** *(a) $\beta_d$ is continuous, strictly increasing, and concave on $[0,1]$, and nondecreasing in $d$. (b) If $|q-q'|\le d$, then $\Pr(q'+Z\in N)\le\beta_d(\Pr(q+Z\in N))$ for every Borel set $N$. (c) If $\sigma,\sigma'$ are order laws with $|q-q'|\le d$ for all $q\in\operatorname{supp}\sigma$, $q'\in\operatorname{supp}\sigma'$, then $\int\Pr(q'+Z\in N)\,\sigma'(dq')\le\beta_d\big(\int\Pr(q+Z\in N)\,\sigma(dq)\big)$.*

*Proof.* (a) With $y=F^{-1}(u)$, $\beta_d'(u)=f(y+d)/f(y)=\exp\{(|y|-|y+d|)/b\}$. This is positive and nonincreasing in $y$, hence in $u$. Monotonicity in $d$ holds because $F$ is increasing. (b) If $q'=q$ there is nothing to prove. If $q'<q$, put $\delta=q-q'\le d$ and $N'=N-q$. Then $\Pr(q+Z\in N)=\Pr(Z\in N')=:u$ and $\Pr(q'+Z\in N)=\int_{N'}f(x+\delta)\,dx$. The ratio $\lambda(x)=f(x+\delta)/f(x)$ is nonincreasing. Let $t=F^{-1}(u)$. On $N'\setminus(-\infty,t)$, $\lambda\le\lambda(t)$; on $(-\infty,t)\setminus N'$, $\lambda\ge\lambda(t)$. So
$\int_{N'}f(x+\delta)dx-F(t+\delta)=\int(\mathbf 1_{N'}-\mathbf 1_{(-\infty,t)})\lambda f\,dx\le\lambda(t)[u-F(t)]=0$, and $F(t+\delta)=\beta_\delta(u)\le\beta_d(u)$. If $q'>q$, apply this to $-N$ and the orders $-q'<-q$; $Z$ is symmetric. (c) Apply (b) to each pair, integrate over $\sigma'(dq')\sigma(dq)$, and use Jensen's inequality for the concave $\beta_d$. $\square$

**Lemma R.5 (pool cap; analytical).** *In every equilibrium at $r_1$ with $\Pr(X\in N)>0$, and for every $s\in[0,1]$,*

$$
\Pr(N\mid H)<F(\bar x-1),\quad \Pr(N\mid L)<F(\bar x+1),\quad \Pr(N)<\bar\pi,\quad
\Pr(s+Z\in N)<F(\bar x),\quad \Pr(Z-s\in N)<F(\bar x+s).
$$

*Proof.* By Lemma R.2, $\operatorname{supp}\sigma_H\subseteq[0,1]$ and $\operatorname{supp}\sigma_L\subseteq[-1,0]$. Write $u_H=\Pr(N\mid H)$ and $u_L=\Pr(N\mid L)$. Every pair of orders is at most $2$ apart, so Lemma R.4(c) gives $u_L\le\beta_2(u_H)$. The pool belief is below $\tau_L$, so $u_H<\lambda u_L$ with $\lambda=\tau_L/(1-\tau_L)$. Noise has full support, so $u_H>0$. Put $y=F^{-1}(u_H)$. Then $\psi(y):=F(y)/F(y+2)=u_H/\beta_2(u_H)<\lambda$. The function $\psi$ equals $e^{-2/b}$ on $y\le-2$ and is continuous and strictly increasing on $[-2,\infty)$ with limit $1$ (the reverse-hazard argument of CD.7(b)). Since $e^{-2/b}=m/(1-m)<\lambda<1$, there is a unique $y^*>-2$ with $\psi(y^*)=\lambda$, and $\psi(y)<\lambda$ forces $y<y^*$. With $\bar x=y^*+1$, $\bar\mu(\bar x)=\psi(y^*)/(1+\psi(y^*))=\tau_L$. So $u_H<F(\bar x-1)$. Then $u_L\le\beta_2(u_H)<\beta_2(F(\bar x-1))=F(\bar x+1)$, and $\Pr(N)=\tfrac12(u_H+u_L)<\bar\pi$. A deviation $s\in[0,1]$ is at most $1$ from every $q\in[0,1]$, so Lemma R.4(c) with $\sigma=\sigma_H$ gives $\Pr(s+Z\in N)\le\beta_1(u_H)<\beta_1(F(\bar x-1))=F(\bar x)$. A deviation $-s$ is at most $1+s$ from every $q\in[0,1]$, so $\Pr(Z-s\in N)\le\beta_{1+s}(u_H)<F(\bar x+s)$. $\square$

The bound is tight: full orders and the half-line pool $(-\infty,\bar x)$ attain it in the limit. It holds for every order law and every pool shape, including islands and mixtures. A random test of 4,000 mixed-order laws and pool sets finds no violation (`checks_roc.csv`, largest value of each left side minus its bound: $-2.8\times10^{-5}$).

### 3.2 Forcing full orders

**Proposition R.6 (a regime II replacement for the residual bound in (A3); analytical).** *Assume (A1') and (A2). If $k\le K(c_L)$, then every equilibrium at $r_1$ has orders $(1,-1)$. The equilibrium set is then exactly the set of profiles with full orders and a Borel pool $N\supseteq(-\infty,z_0)$ with $\bar\mu_N<\tau_L$, with prices and entry given by Lemma CD.2(e).*

*Proof.* Fix a candidate equilibrium. On $A$, $e=\varphi(\mu_X)\ge\rho$ and $\mu_X\ge\tau_L$ almost everywhere (Lemma CD.2(b),(c)), and $\mu_X\le M$. So $A_L\ge\rho\tau_L\Delta_T\mathbf 1_A$ and $A_H\ge\rho m\Delta_T\mathbf 1_A$. By Lemma R.5, for every $s\in[0,1]$,

$$
F_L(s)=\int f(x+s)A_L(x)\,dx\ge\rho\tau_L\Delta_T[1-\Pr(Z-s\in N)]>\rho\tau_L\Delta_T S(\bar x+1),
$$

$$
F_H(s)=\int f(x-s)A_H(x)\,dx\ge\rho m\Delta_T[1-\Pr(s+Z\in N)]>\rho m\Delta_T S(\bar x).
$$

If $N$ is null the same bounds hold with $\Pr(\cdot\in N)=0$. By (A.5) and $|F_\theta'|\le F_\theta/b$, $U_\theta'(s)\ge(1-\tfrac sb)F_\theta(s)-k>(1-\tfrac1b)\rho\Delta_T\min\{\tau_LS(\bar x+1),mS(\bar x)\}-k\ge0$ for almost every $s$. So $s=1$ is the unique best correctly signed size, and wrong signs lose (Lemma R.2). Hence $\sigma_H=\delta_1$ and $\sigma_L=\delta_{-1}$. Under full orders $Z_0=(-\infty,z_0)$ has positive probability, so $N\supseteq Z_0$ and $\bar\mu_N<\tau_L$. Conversely, take full orders and any such $N$. Lemma CD.2(e) gives the challenger's and the market maker's conditions. The bounds above hold against this schedule too, so full orders are the investor's unique best response. $\square$

Three remarks.

1. As $c_L\downarrow B_{r_1}(m)$, $\bar x\to-1$ and $K\to\tfrac12(1-\tfrac1b)\rho m\Delta_T$: half of (A3)'s bound ($0.011206$ against $0.022412$ at the benchmark). The equilibrium set jumps at $c_L=B(m)$: just above it, the plateau $x\le-1$ becomes a no-entry pool of probability $0.342$, and the low type's residual there drops from $\rho m\Delta_T$ to zero.
2. $K$ is sufficient, not sharp. On pure orders and half-line pools, the forcing level is $0.054$ to $0.060$ for $c_L\le2.55$, but it drops to $0.019$ at $c_L=2.65$ and to $0.014$ at $c_L=3.05$ (`checks_forcing_map.csv`, numerical diagnostic). In the continuum the drop sits at $c_L=2B(\tfrac12)-c_H=2.5833$ (Lemma R.11): above it, a pure profile with separation just below $2x^*$ pools the whole lower plateau at once. On the order grid of the check (step $0.05$) the drop shows just above $c_L=2.6202$, where separation $1.70$ first pools. A finer check with $q_H=1$ and shorts in $[0.70,v_H)$ confirms the continuum break (`checks_break.csv`): no such profile pools at $c_L=2.58$; the forcing level is $0.0205$ at $c_L=2.59$, $0.0199$ at $2.60$, and $0.0193$ at $2.62$. So at $k=0.02$ full orders stop being forced, among pure half-line schedules, between $c_L=2.59$ and $2.60$.
3. At $k=0.008$ and $c_L\in\{2.4,2.5\}$, all 281 consistent pure half-line schedules on the check grid give full best responses, with smallest marginal payoff $0.048$ (`checks_forcing.csv`).

### 3.3 Entry and ownership over the equilibrium set

Under full orders, define for a flow set $I$

$$
\Gamma(I)=\int_I(\mu_X-\tau_L)\,dP,\qquad
B_0=-\Gamma(Z_0)=\tfrac12\big[\tau_LF(z_0+1)-(1-\tau_L)F(z_0-1)\big]>0,
$$

$$
\mathsf E_0=\rho S_X(z_0)+(1-\rho)S_X(x^*),\qquad
e_{H,0}=\rho S(z_0-1)+(1-\rho)S(x^*-1)=\rho S(z_0-1)+(1-\rho)\alpha_H .
$$

$\mathsf E_0$ and $e_{H,0}$ are the outcomes with the minimal pool. A pool $N\supseteq Z_0$ is consistent if and only if $\Gamma(N\setminus Z_0)<B_0$: the budget $B_0$ is the belief slack that the forced pool provides.

**Proposition R.7 (the bathtub bound; analytical).** *Under full orders, every consistent pool $N$ satisfies*

$$
\mathsf E(N)>\mathsf E_0-V_E,\qquad e_H(N)>e_{H,0}-V_H,
$$

*where $V_E=\sup\{W_E(I):I\subseteq[z_0,\infty),\ \Gamma(I)<B_0\}$ with $W_E(I)=\int_I\varphi(\mu_X)\,dP$, and $V_H$ is the same with $W_H(I)=\int_I\varphi(\mu_X)f(x-1)\,dx$. The supremum is not attained. It equals $W(I^*)$ for the bathtub set*

$$
I^*=[z_0,y_1)\cup[x^*,y_2)\cup P,
$$

*where, for entry, $\mu_X(y_1)=\min\{\tau_L+\rho\theta^*,\tau_H\}$, $\mu_X(y_2)=\min\{\tau_L+\theta^*,M\}$ ($y_2=x^*$ if $\tau_L+\theta^*<\tau_H$), $P\subseteq[1,\infty)$ is a share of the plateau used only when $\theta^*=M-\tau_L$, and $\theta^*$ solves $\Gamma(I^*)=B_0$. For ownership replace $\tau_L+\rho\theta$ by $\tau_L/(1-\rho\theta)$, $\tau_L+\theta$ by $\tau_L/(1-\theta)$, and $M-\tau_L$ by $1-\tau_L/M$. If $k\le K(c_L)$, every value in $(\mathsf E_0-V_E,\mathsf E_0]$ and in $(e_{H,0}-V_H,e_{H,0}]$ is attained by some equilibrium.*

*Proof.* Under full orders, $\mathsf E(N)=\mathsf E_0-W_E(N\setminus Z_0)$ and $e_H(N)=e_{H,0}-W_H(N\setminus Z_0)$ by (R.0), and $\Gamma(N)<0$ is $\Gamma(N\setminus Z_0)<B_0$. On $[z_0,\infty)$ the cost density $c=\mu_X-\tau_L$ is positive except at $z_0$, and the value density $w$ is $\rho$ on $[z_0,x^*)$ and $1$ on $[x^*,\infty)$ (times $2\mu_X$ for ownership). The ratio $c/w$ is nondecreasing in $x$ on each of the two pieces, because $\mu_X$ is. So the sublevel sets $\{c<\theta w\}$ are the sets $I^*$ above, and $\Gamma$ of them rises continuously in $\theta$ from $0$, except on the plateau, where the ratio is constant and any share can be taken. Since $\Gamma([z_0,\infty))=\tfrac12-\tau_L+B_0>B_0$, a unique $\theta^*\in(0,\infty)$ and plateau share give $\Gamma(I^*)=B_0$. For any $I$ with $\Gamma(I)<B_0$: on $I^*\setminus I$, $w\ge c/\theta^*$; on $I\setminus I^*$, $w\le c/\theta^*$. Hence

$$
W(I^*)-W(I)\ge\frac1{\theta^*}\big[\Gamma(I^*)-\Gamma(I)\big]=\frac{B_0-\Gamma(I)}{\theta^*}>0 .
$$

Truncations $I^*\cap(-\infty,t)$ are consistent for every $t$ below the top of $I^*$, and their value rises continuously to $W(I^*)$, so the supremum is $W(I^*)$ and every value below it is reached. Under $k\le K(c_L)$ each such pool is an equilibrium by Proposition R.6. $\square$

The worst pool is not a half-line. It adds a mid band where cheap entry is cheap to remove, an island just above $x^*$ where both types would enter, and a share of the top plateau. Per unit of belief cost, removing a flow above $x^*$ removes $1/\rho$ times more entry than removing a flow of the same belief below $x^*$. At $c_L=3$ the worst pool is $(-\infty,-0.235)\cup[0.871,1)\cup P$ with $P$ equal to $13\%$ of the plateau.

At $k=0.02$, which is above $K$, the worst pools still pass the investor test, with the plateau share placed as a far tail (`checks_island.csv`, numerical diagnostic): at $c_L=3.5$ the island equilibrium has $\mathsf E=0.2408<\rho$, and the smallest marginal payoffs are $0.0256$ (high type) and $0.0126$ (low type).

### 3.4 Proposition 2'

**Proposition 2' (competition creates competition without a floor; analytical).** *Fix $0<p<\ell<r_0<r_1<h$, $0<\rho<1$, $b>1$, $k>0$. Assume (A1'), (A2), and*

$$
\Delta_T(r_0)<k\le K(c_L)=\Big(1-\frac1b\Big)\rho\,\Delta_T(r_1)\min\{\tau_L\,S(\bar x+1),\ m\,S(\bar x)\},
\tag{A3$'$}
$$

$$
\mathsf E_0-V_E\ge\rho,\qquad e_{H,0}-V_H\ge\rho .
\tag{A4$'$}
$$

*(i) At $r_0$ the unique trading outcome is $q_H=q_L=0$, the price carries no information, and entry is $\rho$.*

*(ii) At $r_1$ the unique trading outcome is $(1,-1)$. In every equilibrium the price is informative and strictly Blackwell dominates the $r_0$ price, entry strictly exceeds $\rho$, and high-value ownership strictly exceeds its $r_0$ value $\rho/2$. Every equilibrium has a no-entry pool of positive probability. On-path entry is not unique: it takes every value in $(\mathsf E_0-V_E,\mathsf E_0]$.*

*(iii) At every $r_2\in(r_1,h)$ with $B_{r_2}(M)<c_H$, every equilibrium has entry strictly below $\rho$ and ownership strictly below $\rho/2$.*

*Conditions (A1') to (A4') hold on a nonempty set that is open when (A4') is taken strict [Referee fix: and when the right inequality of (A3') is taken strict]. Given (A1'), (A2), and (A3'), condition (A4') is also necessary for the entry and ownership claims in (ii).*

*Proof.* (i) is Lemma R.1. (ii): Proposition R.6 gives unique full orders and the equilibrium set. Lemma R.3(a) gives informativeness and Blackwell dominance, since $K<(1-\frac1b)\rho m\Delta_T<\rho\Delta_T/2$. Lemma R.3(b) gives the pool. Proposition R.7 gives $\mathsf E>\mathsf E_0-V_E\ge\rho$ and $e_H>e_{H,0}-V_H\ge\rho$, and the range of entry. In the benchmark a prepared high-value challenger always wins, so $\mathsf O_H=e_H/2$. Necessity: if $\mathsf E_0-V_E<\rho$, Proposition R.7 gives a consistent pool with $\mathsf E<\rho$, and by Proposition R.6 it is an equilibrium; the same holds for ownership. (iii) is Proposition R.12. Nonemptiness: the benchmark with $r_0=1.1$ and $k=0.008$ satisfies (A3') for $c_L\in(2.3662,2.5867]$ [Referee fix: the right end is $2.58668$; $K(2.5867)=0.0079999<0.008$, so the closed interval should end at $2.5866$] ($\Delta_T(1.1)=0.004545$, $B_{1.1}(\tfrac12)=4.839<6$), and (A4') holds there with room ($\inf\mathsf E=0.4107$, $\inf e_H=0.5790$ at $c_L=2.5$; `example_r1.csv`). All conditions are continuous in the primitives. $\square$

At the benchmark $\rho=0.25$, (A4') is $c_L\le3.4607$ (entry) and $c_L\le3.7408$ (ownership); the entry condition binds. Table 2 gives other $\rho$. With $\rho=0.5$ the entry condition allows only $c_L\le2.3726$, a sliver above $B(m)=2.3662$: when cheap entry is common, losing it after bad news costs more than expensive entry gains after good news. [Referee fix: (A4') contains a condition on $\rho$ alone. Every pool contains $Z_0$, and $z_0>-1$, so $\mathsf E_0<\rho(1-\pi_0)+(1-\rho)a$ with $\pi_0=\Pr(X\le-1)=\frac14(1+e^{-2/b})$ and $a=S_X(x^*)$ (Theorem AD.1, adversary note). So the entry half of (A4') fails at every $c_L$ in regime II once $\rho\ge\rho_E^*=a/(a+\pi_0)=0.5154$, and the ownership half fails once $\rho>\rho_O^*=\alpha_H/(\alpha_H+F(-2))=0.7428$. Also, at the paper's triple $(r_0,k,\rho)=(1.2,0.02,0.25)$ condition (A3') is empty: $K\le0.0112<\Delta_T(1.2)=0.0167$. The thresholds $3.4607$ and $3.7408$ hold at the benchmark $r_1$ and $\rho$ with a weaker $r_0$ and a smaller $k$, as in the example of the proof.]

A closed-form sufficient condition for the entry half of (A4'): by Lemma R.5 and the budget, $\Pr(N\setminus Z_0)<\bar\pi-\Pr(Z_0)$ and the part of $N$ above $x^*$ has probability at most $B_0/(\tau_H-\tau_L)$, so

$$
\mathsf E_0-\rho\big[\bar\pi-\Pr(Z_0)\big]-(1-\rho)\min\Big\{S_X(x^*),\frac{B_0}{\tau_H-\tau_L}\Big\}\ge\rho
\tag{A4$''$}
$$

implies it. At the benchmark (A4'') is $c_L\le3.3357$.

## 4. Why (A3) is not enough: three families

The families below are exact equilibria at the stated parameters. They show where Proposition 2 fails when only the paper's (A3) holds.

**Proposition R.8 (universal bounds; analytical).** *For every $k$ and every equilibrium at $r_1$: $\mathsf E>\rho(1-\bar\pi)$ and $e_H>\rho\,S(\bar x-1)$.*

*Proof.* By (R.0), $\mathsf E\ge\rho\Pr(A)$ and $e_H\ge\rho\Pr(A\mid H)$. Apply Lemma R.5. $\square$

At the benchmark these bounds are $\mathsf E>0.102$ at $c_L=3$ and $\mathsf E>0.073$ at $c_L=3.5$. The starved family below comes close to them.

**Proposition R.9 (half-line family; analytical).** *Assume (A1') and (A2). For $x'\ge x^*$, full orders with the pool $(-\infty,x')$ form an equilibrium if and only if $\bar\mu(x')<\tau_L$ and $k\le(1-\tfrac1b)J^+(x')$, where $J^+(x')=\Delta_T[\tfrac{e^{-1/b}}2(\arcsin\sqrt M-\arcsin\sqrt{\mu_X(x')})+\tfrac m2]$ for $x'\in[x^*,1]$ and $J^+(x')=\tfrac12\Delta_Tm\,e^{-(x'-1)/b}$ for $x'\ge1$. Its outcomes are $\mathsf E=S_X(x')$ and $e_H=S(x'-1)$. If $k<(1-\frac1b)\rho m\Delta_T$ and $\rho\le\frac12$, the members with $\mathsf E$ or $e_H$ at or just below $\rho$ pass the investor test.*

*Proof.* On $[x',\infty)$, $\mu_X\ge\mu_X(x^*)=\tau_H$, so $e=1$; on the pool, belief below $\tau_L<\tau_H$ means no type enters, which is consistent exactly when $\bar\mu(x')<\tau_L$. Since $x^*>0$, $A\subseteq[0,\infty)$ and Lemma CD.8 makes $k\le(1-\frac1b)J$ necessary and sufficient for the low type; the high type's full purchase follows from $F_H(s)\ge e^{-(1-s)/b}J$, as in Theorem CD.3(iv). $J^+$ is Lemma CD.6 with $\varphi=1$ on $[\mu_X(x'),M]$. For the last claim: $(1-\frac1b)J^+(1)=\frac12(1-\frac1b)m\Delta_T\ge(1-\frac1b)\rho m\Delta_T>k$, so the investor test ends at some $x_k>1$, where $e_H(x_k)=\tfrac12e^{-(x_k-1)/b}=k/[(1-\frac1b)m\Delta_T]<\rho$. Since $S_X(x')<S(x'-1)$, entry falls to $\rho$ before ownership does. $\square$

So under (A3) the result fails whenever $\tau_L$ exceeds the pool belief of the member where $\mathsf E$ or $e_H$ reaches $\rho$. At the benchmark these members are $x_E=1.6265$ and $x_O=2.3863$ (the test ends at $x_k=2.6140$), and the thresholds are $c_L>B(\bar\mu(x_E))=3.6498$ for entry and $c_L>B(\bar\mu(x_O))=3.8945$ for ownership.

**Proposition R.10 (the starved family).** *Assume (A1') and (A2). Take pure orders $(1,-v)$ with $0<v<v_H$ and a pool $(-\infty,x')$ with $x'\ge0$ that contains $Z_0$. Put*

$$
C_L(v,x')=\rho\Delta_T\int_{x'}^\infty\frac{e^{-x/b}}{2b}\,\mu_X(x)\,dx,\qquad \mu_X(x)=\frac{f(x-1)}{f(x-1)+f(x+v)} .
$$

*(a) (Analytical.) The challenger and market maker conditions hold if and only if $\bar\mu_N=F(x'-1)/[F(x'-1)+F(x'+v)]<\tau_L$; then entry is $\rho$ on $[x',\infty)$ and zero on the pool. The low type's best response is $v$ if and only if $C_L(v,x')\,e^{-v/b}(1-v/b)=k$. The outcomes are $\mathsf E=\tfrac\rho2[S(x'-1)+S(x'+v)]<\rho$ and $e_H=\rho\,S(x'-1)<\rho$. At such a profile $F_H(1)=k/(1-v/b)$, so full purchase earns $kv/(b-v)>0$.*

*(b) (Numerical diagnostic.) Along the family at the benchmark, full purchase is the high type's best response on a 401-point order grid with adaptive quadrature (`starved_checks.csv`, 45 members, $k\in[0.005,0.03]$).*

*Proof of (a).* Under $(1,-v)$ the largest belief is $\mu_X=1/(1+e^{-(1+v)/b})<\tau_H$ on $[1,\infty)$, because $1+v<b\operatorname{logit}\tau_H$; so the expensive type never enters, and $e=\rho$ on $A$ by Lemma CD.2. Lemma CD.2(c),(e) gives the pool condition. Since $x'\ge0$, $x+s\ge0$ on $A$ for $s\ge0$, so $f(x+s)=e^{-s/b}f(x)$ there and $F_L(s)=e^{-s/b}C_L$. The low type's payoff $s\,e^{-s/b}C_L-ks$ has second derivative $C_Le^{-s/b}(s/b-2)/b<0$ on $[0,1]$, so it is strictly concave and the first-order condition characterizes the maximizer. Wrong signs lose (Lemma R.2). Entry follows from (R.0). For the identity, $\int f(x-1)(1-\mu_X)e\,dx=\int f(x+v)\mu_Xe\,dx$ under these orders, so $F_H(1)=F_L(v)=e^{-v/b}C_L=k/(1-v/b)$. $\square$

The corner $v=0$ belongs to the family: the low type abstains if and only if $C_L(0,x')\le k$, and the identity $F_H(1)=F_L(0)=C_L$ then forces $C_L(0,x')=k$ for the high type to buy, with $U_H(1)=0$. The high type is indifferent between $0$ and $1$ there. The numerics track finds this member for $c_L\ge3.95$ (pool end $1.906$, $\mathsf E=0.0638$), the lower end of the entry range below.

[Referee fix: part (b) is analytical for every member with $x'\ge1$, and this covers the corner. For $x\ge x'\ge1\ge s$, $f(x-s)=e^{-(1-s)/b}f(x-1)$, so $F_H(s)=e^{-(1-s)/b}F_H(1)$ and $U_H(s)=s\,e^{-(1-s)/b}F_H(1)-ks$ is strictly convex on $[0,1]$. Its maximum is at an end point, and $U_H(1)=kv/(b-v)\ge0=U_H(0)$, so $q_H=1$ is a best response. On $[1,\infty)$ the posterior is the constant $M_v=(1+e^{-(1+v)/b})^{-1}$, so $C_L=\frac{\rho\Delta_T}2M_ve^{-x'/b}$ and the whole member is closed form. At $k=0.02$ the member with $x'=1$ has $v=0.50255$ and pool belief $0.39553$. So Proposition 2(ii) fails analytically for $c_L>3.4211$ ($\mathsf E=0.0920$, $\mathsf O_H=0.0625$), not only for $c_L>3.6498$. Over the (A3) window at $r_0=1.2$ this analytical threshold runs from $3.3714$ ($k=0.0167$) to $3.4581$ ($k=0.0224$). For $k\le0.01546$ the limit member $v\uparrow v_H$ has $x'\ge1$, so the entries of Table 3 with $k\le0.015$ are analytical. The corner exists exactly for $c_L>3.9418$ (`check_theory/starved_closed.csv`).]

At $k=0.02$ the family exists exactly for $c_L>2.9844$ (the infimum of the pool belief is $0.34312$, approached as $v\uparrow v_H$ with $x'=0.4388$). Its entry is between $0.064$ and $0.112$, and $\mathsf O_H\le0.078$. The numerics track found a member of this family independently at $c_L=3.5$ ($x'=0.5$, $v=0.7196$, $\mathsf E=0.1103$). The threshold rises as $k$ falls (Table 3). On the $k$ grid of Table 3, its smallest value inside the (A3) window is $2.8326$, at $k=0.0224$. [Referee check: Table 3 is reproduced by independent quadrature, and the infimum over the whole (A3) window, $k\uparrow0.022412$, is $2.8319$. A member inside the window is confirmed with both best responses: $c_L=2.9$, $k=0.0224$, orders $(1,-0.73)$, pool $(-\infty,0.1913)$, pool belief $0.3277<\tau_L=0.333$, $\mathsf E=0.1227$, $\mathsf O_H=0.0833$ (`check_theory/starved_a3.csv`; numerical diagnostic). So under the paper's (A3), with $k$ free in its window, unique trading and the reversal both need $c_L\le2.8319$ at $\rho=0.25$.]

**Lemma R.11 (when starving is impossible for pure orders; analytical).** *Suppose $c_L+c_H\le2B_{r_1}(\tfrac12)$, that is, $\tau_L\le1-\tau_H$. Then every equilibrium with pure orders and a pool of positive probability has expensive entry with positive probability.*

*Proof.* Pure orders $(q_H,q_L)$ give beliefs symmetric about $\tfrac12$: the reflection $x\mapsto q_H+q_L-x$ swaps the two flow laws and maps $\mu_X$ to $1-\mu_X$. A pool needs $\mu_X<\tau_L$ somewhere, so the smallest belief is below $\tau_L\le1-\tau_H$, and the largest belief exceeds $\tau_H$. Let $T=\{\mu_X\ge\tau_H\}$; it contains $T'=\{\mu_X>1-\tau_L\}$. By the reflection, $B_0=\int_{\{\mu<\tau_L\}}(\tau_L-\mu)\,dP=\int_{T'}(\mu-(1-\tau_L))\,dP$. If the pool contained $T$, then $\Gamma(N)\ge-B_0+\int_{T'}(\mu-\tau_L)\,dP>-B_0+\int_{T'}(\mu-(1-\tau_L))\,dP=0$, because $\tau_L<\tfrac12$ and $\Pr(T')>0$. That contradicts $\bar\mu_N<\tau_L$. So $T\setminus N$ has positive probability. $\square$

The condition $c_L+c_H\le2B(\tfrac12)$ says that the cheap cost lies at least as far below the prior profit as the expensive cost lies above it. At the benchmark it is $c_L\le2.5833$, exactly where the forcing map breaks (Section 3.2). Mixed low-type orders can lower the smallest belief without raising the largest one, so the lemma does not cover mixtures.

## 5. The collapse

**Proposition R.12 (entry falls below its start; analytical).** *Assume (A1') and let $r_2\in(r_1,h)$ with $B_{r_2}(M)<c_H$. Suppose $k<(1-\frac1b)\rho m\Delta_T(r_2)$, which (A3) or (A3') implies. Then every equilibrium at $r_2$ has $\mathsf E<\rho$ and $\mathsf O_H<\rho/2$.*

*Proof.* Every belief is at most $M$, so the expensive type never prepares, and $\mathsf E=\rho\Pr(A)$, $e_H=\rho\Pr(A\mid H)$. Since $B_r(m)$ falls in $r$, $c_L>B_{r_1}(m)>B_{r_2}(m)$, so $\tau_L(r_2)>m$. Three cases. If $c_L>B_{r_2}(M)$, nobody ever prepares and $\mathcal D$ is the unique equilibrium (Theorem CD.3(iii)), with $\mathsf E=0$. If $B_{r_2}(\tfrac12)<c_L\le B_{r_2}(M)$, the cost law at $r_2$ is in regime III, and Proposition CD.10(a) gives a pool of positive probability in every equilibrium. If $c_L\le B_{r_2}(\tfrac12)$, it is in regime II, and the argument of Lemma R.3(b) at $r_2$ gives a pool in every equilibrium. In all cases $\Pr(N)>0$ and $\Pr(N\mid H)>0$ by full support of the noise, so $\mathsf E<\rho$ and $e_H<\rho$. Since $\Delta_T$ rises in $r$, $(1-\frac1b)\rho m\Delta_T(r_1)<(1-\frac1b)\rho m\Delta_T(r_2)$. $\square$

So the paper's "rise and fall" becomes "rise and fall below the start". The original part (iii) needs $c_L<B_{r_2}(m)$, which (A1') rules out. The new part (iii) drops the uniqueness of full orders at $r_2$. When $c_L\le B_{r_2}(\tfrac12)$, uniqueness holds again if $k\le K_{r_2}(c_L)$, by the proof of Proposition R.6, which does not use the expensive type. At the benchmark, $B_{r}(M)=c_H=6$ at $r_C=3.5927$; at $r_2=4$, $c_L\le3.46$ is in regime II ($B_4(m)=2.212$, $B_4(\tfrac12)=4.031$).

## 6. Benchmark numbers

All rows come from `thresholds.py` (closed forms in double precision, root finding, adaptive quadrature) and `checks.py` (grids). Status: numerical diagnostic for every number; the classifications they feed are the analytical results above.

**Table 1. The equilibrium set under full orders at $r_1=3$, $\rho=0.25$** (`knapsack_r1.csv`). $\bar\pi$ is the pool cap; $\mathsf E_0$, $e_{H,0}$ use the minimal pool; $\inf$ is over all consistent pools (Proposition R.7). Under $k\le K$ these are the exact ranges over the equilibrium set.

| $c_L$ | $\tau_L$ | $\bar x$ | $\bar\pi$ | $K(c_L)$ | $\mathsf E_0$ | $\inf\mathsf E$ | $e_{H,0}$ | $\inf e_H$ |
|---|---|---|---|---|---|---|---|---|
| 2.37 | 0.2694 | $-0.901$ | 0.359 | 0.01068 | 0.4371 | 0.4330 | 0.6023 | 0.6000 |
| 2.50 | 0.2850 | $-0.350$ | 0.447 | 0.00858 | 0.4339 | 0.4107 | 0.6005 | 0.5790 |
| 2.80 | 0.3210 | 0.274 | 0.542 | 0.00708 | 0.4268 | 0.3711 | 0.5962 | 0.5253 |
| 3.00 | 0.3450 | 0.593 | 0.591 | 0.00648 | 0.4225 | 0.3403 | 0.5934 | 0.4824 |
| 3.20 | 0.3690 | 0.878 | 0.637 | 0.00601 | 0.4183 | 0.3048 | 0.5904 | 0.4325 |
| 3.40 | 0.3930 | 1.155 | 0.683 | 0.00558 | 0.4143 | 0.2637 | 0.5873 | 0.3742 |
| 3.60 | 0.4170 | 1.515 | 0.736 | 0.00494 | 0.4105 | 0.2157 | 0.5842 | 0.3057 |
| 3.80 | 0.4410 | 2.039 | 0.797 | 0.00402 | 0.4067 | 0.1591 | 0.5810 | 0.2244 |
| 4.00 | 0.4650 | 2.911 | 0.868 | 0.00261 | 0.4030 | 0.0916 | 0.5777 | 0.1269 |
| 4.20 | 0.4890 | 5.037 | 0.955 | 0.00090 | 0.3994 | 0.0158 | 0.5742 | 0.0210 |

**Table 2. Largest $c_L$ at which each claim holds in every equilibrium** (`thresholds_r1.csv`). Columns 2 and 3 are the exact thresholds of (A4') under (A3'). Columns 5 and 6 are the half-line counterexample thresholds, valid for every $k$ in the (A3) window (a dash means the member is beyond the investor test). Regime II is $c_L\in(2.3662,4.2917)$. [Referee fix: the earlier table had dashes at $\rho=0.1$ (both columns) and $\rho=0.2$ (ownership). Those dashes came from the investor test at $k=0.02$, which lies outside the (A3) window when $\rho<0.2231$. Inside the window the last proof step of Proposition R.9 applies: the test ends at $x_k$ with $e_H(x_k)=k/[(1-\frac1b)m\Delta_T]<\rho$, so both members pass. The values now shown are $B(\bar\mu(x_E))$ and $B(\bar\mu(x_O))$ with $x_E=3.4591$, $x_O=4.2189$ at $\rho=0.1$ and $x_O=2.8326$ at $\rho=0.2$ (`check_theory/thresholds_check.csv`). At $k=0.02$ itself these two members fail the investor test, and the dashes are correct for that $k$. At $\rho=0.1$ the (A3) window is empty when $r_0=1.2$, since its right side is $0.0090<\Delta_T(1.2)$.]

| $\rho$ | (A4') entry | (A4') ownership | (A4'') entry | half-line entry | half-line ownership |
|---|---|---|---|---|---|
| 0.10 | 3.9201 | 4.0036 | 3.8276 | 4.0777 | 4.1503 |
| 0.20 | 3.6330 | 3.8350 | 3.5245 | 3.8103 | 3.9865 |
| 0.25 | 3.4607 | 3.7408 | 3.3357 | 3.6498 | 3.8945 |
| 0.30 | 3.2638 | 3.6388 | 3.1177 | 3.4665 | 3.7946 |
| 0.35 | 3.0366 | 3.5280 | 2.8820 | 3.2553 | 3.6857 |
| 0.50 | 2.3726 | 3.1300 | 2.3722 | 3.1948 | 3.2910 |

**Table 3. Starved family at $\rho=0.25$: lowest $c_L$ at which it exists** (`starved_r1.csv`). The limiting member has $v\uparrow v_H=0.7424$ for $k\le0.0224$.

| $k$ | 0.0224 | 0.021 | 0.020 | 0.019 | 0.018 | 0.016 | 0.015 | 0.0125 | 0.010 | 0.0075 | 0.005 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $c_L>$ | 2.8326 | 2.9177 | 2.9844 | 3.0561 | 3.1329 | 3.3029 | 3.3954 | 3.6048 | 3.7831 | 3.9367 | 4.0703 |
| $\mathsf E$ at limit | 0.124 | 0.117 | 0.112 | 0.107 | 0.102 | 0.092 | 0.086 | 0.072 | 0.057 | 0.043 | 0.029 |

For each $k$ the starved threshold lies above $K^{-1}(k)$, as Proposition R.6 requires: at $k=0.0075$ it is $3.937$, and $K(3.937)=0.0030<0.0075$.

**The benchmark ($k=0.02$, $\rho=0.25$) in one line.** Regime II is $c_L\in(2.3662,4.2917)$. Proposition 2(ii) fails for $c_L>2.9844$ through the starved family (numerical diagnostic), for $c_L>3.4607$ also through island pools (numerical diagnostic), and for $c_L>3.6498$ through the half-line family (analytical). For $c_L\le2.59$ the forcing checks show full orders forced over pure half-line schedules (margin about $0.03$ up to $2.58$, and $0.0005$ at $2.59$), and then Proposition R.7 gives $\mathsf E>\rho$; this is a numerical diagnostic, not a proof, because $k=0.02$ exceeds $K$. For $c_L\in(2.59,2.9844]$ forcing fails for some schedules, but neither track has found an equilibrium with $\mathsf E\le\rho$ there (the numerics track's sweep finds only full orders up to $c_L=2.975$). The status is open.

## 7. What survives: a ledger

| claim of Proposition 2 | under (A1') with the paper's (A3) | under (A1'), (A3'), (A4') |
|---|---|---|
| (i) at $r_0$: no trade, constant price, entry $\rho$ | survives (R.1) | survives |
| (ii) informed trading, correct signs | survives (R.2, R.3a) | survives |
| (ii) informative price, Blackwell dominance | survives (R.3a) | survives |
| (ii) unique trading outcome $(1,-1)$ | fails for $c_L>2.9844$ at the benchmark (R.10, numerical diagnostic); open below [Referee fix: analytical for $c_L>3.4211$; and $c_L>2.8319$ fails for some $k$ in the window] | survives (R.6) |
| (ii) unique on-path entry | fails always: pools form a continuum (R.3b, R.7) [Referee fix: proved when $k<(1-\frac1b)J_G(z_0)$, which covers $\rho\le\frac12$; open for large $\rho$, see Section 1] | fails: entry fills $(\mathsf E_0-V_E,\mathsf E_0]$ |
| (ii) price reveals $\mu_X$; insider at every price | fails always (R.3b) | fails always |
| (ii) $\mathsf E>\rho$ in every equilibrium | fails for $c_L>3.6498$ (analytical) [Referee fix: for $c_L>3.4211$ (analytical, starved members with $x'\ge1$)] and for $c_L>2.9844$ (numerical diagnostic) at the benchmark; open below | survives iff (A4'), i.e. $c_L\le3.4607$ at $\rho=0.25$ [Referee fix: (A4') also needs $\rho<0.5154$] |
| (ii) $\mathsf O_H>\rho/2$ in every equilibrium | fails for $c_L>3.8945$ (analytical) [Referee fix: for $c_L>3.4211$ (analytical, starved members with $x'\ge1$)] and for $c_L>2.9844$ (numerical diagnostic) at the benchmark; open below | survives iff (A4'), i.e. $c_L\le3.7408$ |
| (iii) collapse to entry $\rho$ | vacuous; replaced by $\mathsf E<\rho$ (R.12) | $\mathsf E<\rho$ (R.12) |

**The weakest replacement for (A1).** Part (i) needs only $c_L\le B_{r_0}(\tfrac12)$. Part (ii) needs more, and the answer depends on $k$:

- With the trading cost in (A3'), the exact condition is (A4'). At the benchmark it is $c_L\le3.4607$: about $57\%$ of regime II beyond the floor.
- With the paper's trading cost window (A3), the half-line family makes $c_L\le3.6498$ necessary for entry and $c_L\le3.8945$ necessary for ownership at every $k$ in the window (analytical). The starved family makes $c_L\le2.9844$ necessary at $k=0.02$, and $c_L\le2.8326$ necessary at $k=0.0224$ (numerical diagnostic). The natural sufficient candidate is $c_L+c_H\le2B_{r_1}(\tfrac12)$ (Lemma R.11; $2.5833$ at the benchmark). The forcing map and the bathtub bound support it, but it is open as a theorem. [Referee fix: the candidate can hold only together with a bound on $\rho$. It is false for $\rho\ge\rho_E^*=a/(a+\pi_0)=0.5154$: by Theorem AD.1 of the adversary note every full-order equilibrium then has $\mathsf E<\rho$, and by Proposition R.6 every equilibrium has full orders when $k\le K(c_L)$. At $\rho=0.6$, $c_L=2.4\le2.5833$, $r_0=1.2$, $k=0.02$, conditions (A1'), (A2), (A3) and (A3') all hold ($K(2.4)=0.0234$), and $\mathsf E<\rho$ in every equilibrium (analytical, with closed-form evaluation). At $\rho=0.5$, $c_L=2.5$, $k=0.02$, the full-order half-line equilibria with cutoffs $-0.6$, $-0.5$, $-0.4$ have $\mathsf E=0.478$, $0.470$, $0.462<\rho$ (both best responses checked by independent quadrature; `check_theory/candidate_counter.csv`). So the open candidate is "$c_L+c_H\le2B_{r_1}(\frac12)$ at $\rho=0.25$", not a general sufficient condition.]

**The replacement for (A3).** The residual bound of (A3) uses entry $\rho$ at every flow. In regime II the bound must use the cheap type's entry only off the pool, and Lemma R.5 caps the pool under any deviation. This gives (A3'), $k\le K(c_L)$. Near the floor it is half of (A3); it falls as $c_L$ rises ($K(3)=0.0065$, $K(3.5)=0.0053$).

## 8. Economic reading

The floor does two jobs in the paper. It makes $\theta$ material at every price, and it keeps cheap entry insensitive to information. Regime II keeps the first job at the prior but drops the second. Information now moves cheap entry in the wrong direction. Bad news deters the cheap type, good news recruits the expensive type, and entry rises only if the second effect wins. Two forces decide this. The pool, the set of bad-news flows that the market pools at $t_0$, can be large, because many beliefs below $\tau_L$ are consistent with one pooled belief below $\tau_L$; its size grows as $c_L$ approaches the prior profit. And the pool feeds back on trading: it removes the short seller's residual on low flows, so the low type shorts less. A short just below $v_H$ keeps every belief below $\tau_H$. Then the stronger incumbent's informative price recruits nobody and only deters. In these starved equilibria, competition reduces competition.

## 9. Open items

1. **Sufficiency at the paper's trading cost.** Prove that every equilibrium has $\mathsf E>\rho$ at $k=0.02$ for $c_L\le2.5833$, including mixtures and island pools with partial orders. [Referee fix: this is a question at $\rho=0.25$ only. The statement is false at $\rho=0.5$ and for every $\rho\ge0.5154$; see Section 7.] A route: extend Lemma R.11 to mixtures (the largest belief falls by at most the factor $2/(1+\cosh(1/b))$ in the likelihood ratio), then bound the island budget against the top plateau. Status: open.
2. **The window $c_L\in(2.59,2.9844]$ at $k=0.02$.** No starved fixed point exists there among pure orders and half-line pools with $x'\ge0$, but forcing fails for some schedules. Mixed starved profiles, pools with $x'<0$, and partial buys are not checked. Status: open; numerics track to search.
3. **A sharper forcing bound.** $K$ is about one sixth of the pure-schedule forcing level near the floor. A bound that uses expensive entry on the top of $A$ would close part of the gap. Status: open.
4. **The high type in the starved family.** Part (b) of Proposition R.10 is a grid check. An interval enclosure of $U_H(1)-\max_sU_H(s)$ along the family would make it computer-assisted. Status: numerical diagnostic.
5. **Selection.** On-path entry is never unique in regime II. The minimal pool gives the most entry. Whether a refinement selects it is open.

## 10. Files

- `formulas.py`: pure functions (payoffs, thresholds, pool cap, forcing bound, bathtub, half-line and starved families).
- `thresholds.py`: writes `constants_r1.csv`, `knapsack_r1.csv`, `thresholds_r1.csv`, `starved_r1.csv`, `starved_checks.csv`, `example_r1.csv`. Run `python3 thresholds.py` in this folder (a few seconds).
- `checks.py`: writes `checks_roc.csv`, `checks_forcing.csv`, `checks_forcing_map.csv`, `checks_island.csv`, `checks_break.csv`. Run `python3 checks.py` (about fifteen minutes; the forcing map dominates).
