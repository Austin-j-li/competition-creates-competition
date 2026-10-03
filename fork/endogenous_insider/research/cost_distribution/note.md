---
title: "The cost distribution decides who is an insider"
subtitle: "Research track for the endogenous-insider fork"
date: "2026-10-03"
---

This note belongs to `fork/endogenous_insider/`. It uses the notation of `paper/main.md` and of the fork's `mechanism.md`. Equation numbers such as (4), (9), (12) and (A.3) to (A.14) refer to the paper. Results F.1 to F.5 are the fork's. Results CD.1 to CD.15 are new to this note. Each result carries its status in the paper's vocabulary: analytical, computer-assisted, numerical diagnostic, or open.

## 1. Question

The benchmark draws the preparation cost from two points, $c_L$ with probability $\rho$ and $c_H$ otherwise. The fork puts all mass on one point $c$. These are two members of one family: a cost law with CDF $G$. This note asks four things.

1. With a general $G$, when is the investor's knowledge of $\theta$ material for the target stock? When is the investor an insider at every price, in every equilibrium, or only in some equilibria?
2. With a continuous $G$, does the pool at the no-entry price $t_0$ survive?
3. Does a small amount of cost noise around the fork's $c$ change anything? Which cost perturbations select the live equilibrium, and which do not?
4. The model has other random variables: $\theta$, the incumbent value $R$, the noise $Z$, and the investor's signal. What would a fork that kills each one do to "what is information"?

## 2. Headline result

Materiality of $\theta$ at a price $\pi$ is exactly $\Delta_T\,G(B_r(\mu_P(\pi)))$, so insider status depends only on where the lowest cost $c_0$ of $G$ sits relative to three profit levels $B_r(m)<B_r(\tfrac12)<B_r(M)$ (Theorem CD.3, analytical). The investor is an insider at every price in every equilibrium, for every trading cost, if and only if $G(B_r(m))>0$; it is an insider in every equilibrium if and only if $G(B_r(\tfrac12))>0$; insider status is an equilibrium outcome when $G(B_r(\tfrac12))=0<G(B_r(M))$ [Referee fix: this holds for $k\le\bar k_G$; for $k>M\Delta_T g_M$ the dead equilibrium is unique by Theorem CD.3(v), and between the two bounds it is open]; and it is a bystander in every equilibrium when $G(B_r(M))=0$. A continuous $G$ removes the price jump at the edge of the pool, not the pool. Small cost noise around $c$ keeps the dead equilibrium, the live equilibrium, and the cutoff family, and changes only how the live branch ends near the preparation ceiling (Corollary CD.9, Proposition CD.13). No vanishing cost perturbation selects the live equilibrium over the dead one: the location of the lowest added cost selects the pool size, while the mass at or below $B_r(\tfrac12)$ must exceed $2k/\Delta_T$ to remove uninformative prices (Theorem CD.14, analytical). The shape of $G$ plays a third, separate role: entry is a Jensen gap of $G\circ B_r$, so a cost law that is affine on the profit range makes the investor an insider at every price while information never moves total entry (Proposition CD.11, analytical). [Referee fix: "insider at every price" needs a floor, $G(B_r(m))>0$, as in $U[0,12]$. An affine law with $G(B_r(m))=0$, such as $U[B_r(m),12]$, still gives $\mathsf E=g_{1/2}$, but under full orders it has a pool at belief $m$ with zero materiality (Theorem CD.3(iv)).]

## 3. Model changes

Everything is as in Section 2 of the paper, with one change. The preparation cost $C$ has a CDF $G$ on $[0,\infty)$, independent of $\theta$, $R$, $Z$, and the investor's randomization. The challenger observes the price and its cost and prepares if and only if $C\le B_r(\mu_P)$. This is the paper's tie rule: an indifferent challenger prepares. Since $G$ is right-continuous, $G(y)=\Pr(C\le y)$, so entry at a price $\pi$ is

$$
e(\pi)=G\big(B_r(\mu_P(\pi))\big).
\tag{CD.0}
$$

Two members of the family are already in the repository:

- the benchmark, $G_\rho(y)=\rho\,\mathbf 1\{y\ge c_L\}+(1-\rho)\,\mathbf 1\{y\ge c_H\}$, which gives (9);
- the fork, $G(y)=\mathbf 1\{y\ge c\}$, which gives the fork's preparation rule.

**Notation.** Write $c_0=\inf\{y:G(y)>0\}$ for the lowest cost. Then $G(y)=0$ if and only if $y<c_0$, or $y=c_0$ and $G$ has no atom at $c_0$. This is the only place where the tie rule enters. Write

$$
g_m=G(B_r(m)),\qquad g_{1/2}=G(B_r(\tfrac12)),\qquad g_M=G(B_r(M)),\qquad g_m\le g_{1/2}\le g_M .
$$

Write $\mu_0=B_r^{-1}(c_0)=(c_0-g_L)/(g_H-g_L)$ for the participation belief: the belief at which the cheapest challenger breaks even. Write $\varphi(\mu)=G(B_r(\mu))$ for entry as a function of the revealed belief.

**Equilibrium** is the fork's definition with (CD.0) in place of the fork's preparation rule: conditional order laws, a measurable price function of flow, a belief at every realized price including atoms, entry (CD.0), competitive pricing, and investor optimality against the fixed schedule. Write $e(x)=e(P(x))$, $A=\{x:e(x)>0\}$ for the entry set, and $N=\{x:e(x)=0\}$ for the pool. Statements hold almost surely. Laplace noise makes every flow law equivalent to Lebesgue measure under every order distribution, so "almost surely" means the same thing under every unilateral deviation.

**Materiality.** Following the fork's Section 5, the materiality of $\theta$ at a realized price $\pi$ is

$$
\mathfrak m(\pi)=\mathbb E[V_T\mid H,P=\pi]-\mathbb E[V_T\mid L,P=\pi].
$$

The investor is an *insider at $\pi$* if $\mathfrak m(\pi)>0$. It is an *insider in an equilibrium* if $\Pr(\mathfrak m(P)>0)>0$. It is an *insider at every price* if $\mathfrak m(P)>0$ almost surely. It is a *bystander* if $\mathfrak m(P)=0$ almost surely.

**Regimes.** The four regimes below classify $G$ at a fixed strength $r$ and noise scale $b$.

| regime | condition | in terms of the lowest cost $c_0$ |
|---|---|---|
| I, floor | $g_m>0$ | $c_0<B_r(m)$, or $c_0=B_r(m)$ with an atom |
| II, prior entry | $g_m=0<g_{1/2}$ | $c_0$ between $B_r(m)$ and $B_r(\tfrac12)$, ties as above |
| III, price-gated entry | $g_{1/2}=0<g_M$ | $c_0$ between $B_r(\tfrac12)$ and $B_r(M)$, ties as above |
| IV, no entry | $g_M=0$ | $c_0>B_r(M)$, or $c_0=B_r(M)$ without an atom |

The benchmark under (A1) and (A2) is in regime I. The fork is in regime III for $r\le r_C$ and in regime IV above. All three profit levels fall in $r$ by (5), so for a fixed $G$ the regime index can only rise as the incumbent strengthens.

## 4. Results

### 4.1 Materiality and the structure of prices

**Lemma CD.1 (materiality at a price; analytical).** *In every equilibrium, for almost every realized price $\pi$,*

$$
\mathbb E[V_T\mid\theta,P=\pi]=t_0+e(\pi)(t_\theta-t_0),
\qquad
\mathfrak m(\pi)=\Delta_T\,G\big(B_r(\mu_P(\pi))\big).
$$

*For a general incumbent law $F$ as in Proposition 1, the same holds with $\Delta_T$ replaced by $\mathbb E_F[(R-\ell)_+]$ and $B_r$ by the corresponding gross profit.*

*Proof.* Fix $\theta$ and a price $\pi$. The challenger prepares if and only if $C\le B_r(\mu_P(\pi))$. The cost is independent of $\theta$, of the noise, and of the investor's order, so the conditional probability of preparation given $(\theta,P=\pi)$ is $G(B_r(\mu_P(\pi)))=e(\pi)$. The incumbent value is independent of all of these. Given preparation and $\theta$, expected proceeds are $t_\theta$; without preparation they are $t_0$. This gives the first identity. Subtract the two states to get $\mathfrak m(\pi)=e(\pi)(t_H-t_L)=e(\pi)\Delta_T$. For a general $F$, the proof of Proposition 1 shows that the pointwise difference between proceeds with a high-value and a low-value challenger is $(R-\ell)_+$, so $t_H-t_L=\mathbb E_F[(R-\ell)_+]$. $\square$

The formula has two factors and each is a tail condition. The first factor is positive only if some cost lies at or below the challenger's gross profit at the price. The second is positive only if $\Pr(R>\ell)>0$: without an incumbent that can beat a low-value challenger, $\theta$ never moves the proceeds. "Competition creates materiality" holds literally in the second factor.

**Lemma CD.2 (structure of prices, pools, and residuals; analytical).** *In every equilibrium:*

*(a) $P=t_0$ on $N$ and $P>t_0$ on $A$, so $N=P^{-1}(t_0)$.*

*(b) For almost every $x\in A$, $\mu_P(P(x))=\mu_X(x)$, $e(x)=\varphi(\mu_X(x))$, and $P(x)=t_0+\varphi(\mu_X(x))[w_L+\Delta_T\mu_X(x)]$.*

*(c) The forced pool $Z_0=\{x:\varphi(\mu_X(x))=0\}$ lies in $N$ up to a null set. If $\Pr(X\in N)>0$, then $\mu_P(t_0)=\bar\mu_N:=\Pr(H\mid X\in N)$ and $\varphi(\bar\mu_N)=0$.*

*(d) The residuals are $A_H(x)=e(x)\Delta_T[1-\mu_X(x)]$ and $A_L(x)=e(x)\Delta_T\mu_X(x)$, with $0\le A_H,A_L\le g_M M\Delta_T$.*

*(e) Conversely, fix order laws with posterior $\mu_X$ and a measurable set $N\supseteq Z_0$ such that $\Pr(X\in N)=0$ or $\varphi(\bar\mu_N)=0$. Put the price $t_0$ and belief $\bar\mu_N$ on $N$, and the price of (b) and belief $\mu_X$ on $A=N^c$. Then the challenger's and the market maker's conditions hold.*

*(f) The map $\psi(\mu)=t_0+\varphi(\mu)[w_L+\Delta_T\mu]$ is strictly increasing on $\{\mu\in[m,M]:\varphi(\mu)>0\}$.*

*Proof.* (a) Conditional on $X=x$, Lemma CD.1 and $t_H-t_0=w_L+\Delta_T$, $t_L-t_0=w_L$ give $\mathbb E[V_T\mid X=x]=t_0+e(x)[w_L+\Delta_T\mu_X(x)]$. Competitive pricing sets $P(x)$ equal to this. On $N$ it is $t_0$. On $A$ it is at least $t_0+e(x)w_L>t_0$, since $w_L>0$.

(b) For $x\in A$, the identity in (a) gives $\mu_X(x)=[P(x)-t_0-e(P(x))w_L]/[e(P(x))\Delta_T]$. The right side is a Borel function of $P(x)$ on $\{\pi:e(\pi)>0\}$. So on $A$, $\mu_X$ is measurable with respect to the price, and the tower property gives $\mu_P(P(x))=\mathbb E[\mu_X(X)\mid P(X)=P(x)]=\mu_X(x)$ for almost every $x\in A$. Then $e(x)=G(B_r(\mu_P))=\varphi(\mu_X(x))$.

(c) For almost every $x\in A$, $\varphi(\mu_X(x))=e(x)>0$, so $x\notin Z_0$. If $N$ has positive probability, then by (a) the price $t_0$ is an atom whose preimage is $N$. Its belief is $\Pr(H\mid X\in N)$, and $e=0$ there forces $\varphi(\bar\mu_N)=0$.

(d) Subtract the price of (a) from $t_0+e(x)(t_\theta-t_0)$, as in the residual step of Proposition A.2. The bound uses $e\le g_M$ and $1-\mu_X,\mu_X\le M$, from Proposition A.1.

(e) On $N$ the challenger's belief is $\bar\mu_N$ and $\varphi(\bar\mu_N)=0$, so no cost type prepares, $V_T=t_0$, and the price $t_0$ is competitive. On $A$ we have $\varphi(\mu_X)>0$ because $A\cap Z_0=\emptyset$. By (f) the price on $A$ is a strictly increasing function of $\mu_X$, so it reveals $\mu_X$, and it exceeds $t_0$, so it never meets the pool price. The challenger's belief at the price $\psi(\mu)$ is $\mu$, its entry is $\varphi(\mu)$, and the price formula is the competitive price for that entry.

(f) Let $\mu_2>\mu_1$ with $\varphi(\mu_1)>0$. Since $\varphi$ is nondecreasing,

$$
\psi(\mu_2)-\psi(\mu_1)=\varphi(\mu_2)\Delta_T(\mu_2-\mu_1)+[\varphi(\mu_2)-\varphi(\mu_1)](w_L+\Delta_T\mu_1)\ge\varphi(\mu_1)\Delta_T(\mu_2-\mu_1)>0.
$$

This is the argument of (A.3) with $\rho$ replaced by $\varphi(\mu_1)$. $\square$

Lemma CD.2 contains Lemma F.1 ($G$ a point mass) and Proposition A.2 ($G$ with a floor, where $N$ is empty) as special cases.

### 4.2 When is the investor an insider

**Theorem CD.3 (four regimes; analytical).** *Fix $r\in(\ell,h)$, $b>1$, and $G$.*

*(i) Floor. If $g_m>0$, then for every $k>0$ and in every equilibrium the pool is null, the price reveals $\mu_X$, and $\mathfrak m(\pi)\ge\Delta_T g_m$ at almost every realized price. The residuals satisfy $A_H,A_L\ge g_m m\Delta_T$.*

*(ii) Dead equilibrium. The profile $\mathcal D$ (zero orders, constant price $t_0$, belief $\tfrac12$, no preparation) is an equilibrium if and only if $g_{1/2}=0$. Every equilibrium with $\mathfrak m(P)=0$ almost surely is $\mathcal D$.*

*(iii) No entry. If $g_M=0$, then $\mathcal D$ is the unique equilibrium.*

*(iv) No floor. If $g_m=0<g_M$, put $\bar k_G=(1-\tfrac1b)J_G$, with $J_G$ the existence statistic of Lemma CD.6 under full orders and the minimal pool. Then $\bar k_G\ge(1-\tfrac1b)\Delta_T g_M m/2>0$, and for every $k\le\bar k_G$ there is an equilibrium with full orders $(1,-1)$ in which $\Pr(\mathfrak m(P)=0)\ge\Pr(X\le-1)=\tfrac14(1+e^{-2/b})$.*

*(v) Large trading cost. If $k>M\Delta_T g_M$, the unique equilibrium has zero orders, a constant price, entry $g_{1/2}$, and materiality $\Delta_T g_{1/2}$ at its only price.*

*Proof.* (i) By Proposition A.1, which allows arbitrary mixed orders, $\mu_X\in[m,M]$, and by the tower property so is $\mu_P$. Then $e(\pi)=\varphi(\mu_P(\pi))\ge\varphi(m)=g_m>0$ at almost every price, so $N$ is null. Lemma CD.2(b) gives revelation, and Lemma CD.1 gives the materiality bound. The residual bound follows from $e\ge g_m$ and $\mu_X,1-\mu_X\ge m$.

(ii) If $g_{1/2}=0$: under zero orders $X=Z$, $\mu_X\equiv\tfrac12$, the price is one value, its belief is $\tfrac12$, and nobody prepares. Then $V_T\equiv t_0=P$, so an order $q\ne0$ earns $-k|q|<0$, and zero is optimal. Conversely, in $\mathcal D$ the only price has belief $\tfrac12$, so no preparation requires $\varphi(\tfrac12)=g_{1/2}=0$. For the second claim, suppose $\mathfrak m(P)=0$ almost surely. Since $\Delta_T>0$, Lemma CD.1 gives $e(X)=0$ almost surely, hence for Lebesgue-almost every $x$. Then both residuals vanish almost everywhere under every deviation, every nonzero order earns $-k|q|$, and both types play zero. So $\mu_X\equiv\tfrac12$, the price is one value with belief $\tfrac12$, and consistency requires $g_{1/2}=0$. This is $\mathcal D$.

(iii) Every price belief is at most $M$, so $e\le g_M=0$ and $\mathfrak m=0$ almost surely. Part (ii) gives $\mathcal D$, which exists because $g_{1/2}\le g_M=0$.

(iv) Under full orders $\mu_X=m$ on $x\le-1$, so $Z_0\supseteq(-\infty,-1]$. The set $\{\mu:\varphi(\mu)=0\}$ is an interval $[0,\mu_0)$ or $[0,\mu_0]$. Every $\mu_X(x)$ with $x\in Z_0$ lies in it, so their conditional mean $\bar\mu_{Z_0}$ lies in it too; if the interval is open at $\mu_0$, then $\mu_X<\mu_0$ on $Z_0$ and the mean is strictly below $\mu_0$. So $\varphi(\bar\mu_{Z_0})=0$, and Lemma CD.2(e) with $N=Z_0$ gives the challenger's and the market maker's conditions. For the investor, the residuals of Lemma CD.2(d) are nonnegative, bounded, and measurable. The translation identity (A.5) and $|F_\theta'|\le F_\theta/b$ hold, and the ratio bound gives $F_\theta(s)\ge e^{-(1-s)/b}J_G$. Hence $U_\theta'(s)\ge(1-\tfrac1b)J_G-k\ge0$ on $[0,1]$, so the full correctly signed order is a best response; wrong-signed orders earn a nonpositive gross amount and pay the cost. The upper plateau $x\ge1$ has $\mu_X=M$ and $\varphi(M)=g_M>0$, so it lies in $A$ and contributes $\Delta_T g_M m/2$ to $J_G$ by Lemma CD.6. The pool contains $x\le-1$, where $\mathfrak m=0$, and $\Pr(X\le-1)=\tfrac12[F_Z(-2)+F_Z(0)]=\tfrac14(1+e^{-2/b})$.

(v) By Lemma CD.2(d), $F_\theta(s)\le\sup A_\theta\le g_M M\Delta_T<k$ against every candidate schedule. A correctly signed order of size $s>0$ earns $s[F_\theta(s)-k]<0$, and a wrong-signed order earns at most $-ks$ [Referee fix: the text said "less than"; the gross amount can be zero]. So zero is the unique best response of both types, $\mu_X\equiv\tfrac12$, and the profile is the one stated. It is an equilibrium by Proposition CD.4, because $\Delta_T g_{1/2}\le2M\Delta_T g_M<2k$. $\square$

**Corollary (what the regimes say about insider status; analytical).**

| regime | insider at every price, every equilibrium | insider in every equilibrium | $\mathcal D$ exists | pool at $t_0$ |
|---|---|---|---|---|
| I, floor | yes, for every $k$ | yes | no | never |
| II, prior entry | no for $k\le\bar k_G$; yes for $k>M\Delta_T g_M$ | yes | no | optional; forced under full orders |
| III, price-gated entry | no | no: $\mathcal D$ exists for every $k$ | yes | in every equilibrium (CD.10) |
| IV, no entry | bystander | bystander | yes, unique | the whole line |

*Proof.* Rows I and IV are Theorem CD.3(i) and (iii). In rows II and III, $\mathcal D$ exists if and only if $g_{1/2}=0$, by (ii), and every equilibrium other than $\mathcal D$ has positive materiality with positive probability. Part (iv) gives the zero-materiality pool for small $k$, and part (v) gives the exception for large $k$ in regime II. The last column is Proposition CD.10. $\square$ [Referee fix: in row II the first column is open for $\bar k_G<k\le M\Delta_T g_M$.]

Two natural conjectures need correction. First, the dead profile $\mathcal D$ exists if and only if $g_{1/2}=0$, which with the tie rule means $B_r(\tfrac12)<c_0$, or $B_r(\tfrac12)=c_0$ and no atom at $c_0$. But a *no-trade* equilibrium is a different object; it exists if and only if $\Delta_T g_{1/2}\le2k$ (Proposition CD.4). In it the investor can be an insider who does not trade. Second, "insider at every price in every equilibrium if and only if $g_m>0$" holds when the statement must hold for every trading cost. At one fixed $k$ the "only if" can fail: in regime II with $k>M\Delta_T g_M$ the unique equilibrium has positive materiality at its only price.

**Proposition CD.4 (uninformative prices; analytical).** *For every $G$ and $k>0$, an equilibrium with an uninformative price exists if and only if*

$$
\Delta_T\,g_{1/2}\le2k .
\tag{CD.1}
$$

*Every such equilibrium has zero orders, the constant price $t_0+g_{1/2}[w_L+\Delta_T/2]$, entry $g_{1/2}$, and materiality $\Delta_T g_{1/2}$ at its only price.*

*Proof.* "Uninformative" means the price law does not depend on $\theta$, so $\mu_P=\tfrac12$ almost surely and $e=g_{1/2}$ at almost every price. Case $g_{1/2}>0$: the pool is null, Lemma CD.2(b) gives $\mu_X=\mu_P=\tfrac12$ almost surely, so $a_H=a_L$. Convolution with the Laplace density is injective, because its Fourier transform $1/(1+b^2t^2)$ never vanishes, so $\sigma_H=\sigma_L$. The residuals are the constant $g_{1/2}\Delta_T/2$. Type $H$ strictly prefers zero to any negative order and type $L$ strictly prefers zero to any positive order, so a common order law must be the point mass at zero. Zero is optimal if and only if $g_{1/2}\Delta_T/2\le k$. Case $g_{1/2}=0$: entry is zero almost surely, Theorem CD.3(ii) gives $\mathcal D$, and (CD.1) holds. Conversely, if (CD.1) holds, the stated profile has competitive prices, consistent entry, and gives every order $q$ the payoff $|q|(g_{1/2}\Delta_T/2-k)\le0$ or less. $\square$

With the benchmark's $G_\rho$ under (A1) and (A2), $g_{1/2}=\rho$ and (CD.1) is the pooling boundary $r\le r_N=\mathfrak r(2k/\rho)$ of Proposition A.4. With the fork's point mass, $g_{1/2}=0$ when $B_r(\tfrac12)<c$, and (CD.1) holds for every $k$, which is Proposition F.1(i).

**Proposition CD.5 (a heavy floor forces full orders; analytical).** *If $k<(1-\tfrac1b)\,m\,\Delta_T\,g_m$, then every equilibrium has orders $(1,-1)$, a fully revealing price, and entry $\varphi(\mu_X)$ with $\mu_X$ from (A.8). This equilibrium exists and is unique in trading and on-path entry.*

*Proof.* Theorem CD.3(i) gives $A_\theta\ge g_m m\Delta_T$ against every candidate, so (A.6) holds with $\rho$ replaced by $g_m$. Full orders are necessary. Lemma CD.2(e) with $N=\emptyset$ constructs prices and entry, and they are pinned by Lemma CD.2(b). $\square$

For $G_\rho$ this is the right inequality of (A3). At $r=3$ the required floor mass is $k/[(1-\tfrac1b)m\Delta_T]=0.2231$, and the benchmark's $\rho=0.25$ exceeds it.

### 4.3 Full orders, pools, and continuous costs

**Lemma CD.6 (arcsine form of the existence statistic; analytical).** *Under full orders and the pool $N=Z_0\cup(-\infty,x')$, the statistic (A.7) is*

$$
J_G(x')=\Delta_T\Big[g_m\,m\big(\tfrac12-F_Z(x'+1)\big)\mathbf 1\{x'<-1\}
+\frac{e^{-1/b}}4\int_{\max(m,\mu_X(x'))}^{M}\frac{\varphi(\mu)\,d\mu}{\sqrt{\mu(1-\mu)}}\,\mathbf 1\{x'<1\}
+g_M\,m\,S_Z\big(\max(x',1)-1\big)\Big].
$$

*With the minimal pool,*

$$
J_G=\Delta_T\Big[(g_m+g_M)\frac m2+\frac{e^{-1/b}}{2}\int_m^M\varphi(\mu)\,d\big(\arcsin\sqrt\mu\big)\Big].
\tag{CD.2}
$$

*For the fork with $\tau\in[\tfrac12,M]$, $J=\Delta_T[\tfrac m2+\tfrac{e^{-1/b}}2(\arcsin\sqrt M-\arcsin\sqrt\tau)]$. For a uniform cost law, $\varphi$ is affine, $\varphi=\alpha+\beta\mu$, on each piece of $[m,M]$, and*

$$
\int_{\mu_1}^{\mu_2}\frac{(\alpha+\beta\mu)\,d\mu}{\sqrt{\mu(1-\mu)}}=\Big[(2\alpha+\beta)\arcsin\sqrt\mu-\beta\sqrt{\mu(1-\mu)}\Big]_{\mu_1}^{\mu_2}.
$$

*Proof.* By (A.7), $J=\Delta_T\int e(x)\kappa(x)\,dx$ with $\kappa=f(x-1)f(x+1)/[f(x-1)+f(x+1)]$. On $x\le-1$, $\mu_X=m$ and $\kappa=m f(x+1)$, whose integral over $[x',-1]$ is $m[\tfrac12-F_Z(x'+1)]$. On $x\ge1$, $\kappa=m f(x-1)$, whose integral over $[\max(x',1),\infty)$ is $m\,S_Z(\max(x',1)-1)$. On $(-1,1)$, $f(x\mp1)=e^{-(1\mp x)/b}/(2b)$, so $\kappa=e^{-1/b}/[4b\cosh(x/b)]$. With $\mu=\mu_X(x)=\operatorname{logistic}(2x/b)$ we have $d\mu=(2/b)\mu(1-\mu)\,dx$ and $\cosh(x/b)=1/[2\sqrt{\mu(1-\mu)}]$, so $\kappa\,dx=\tfrac{e^{-1/b}}4\,d\mu/\sqrt{\mu(1-\mu)}$. On the forced pool $\varphi=0$, so the minimal pool needs no separate term. For the uniform formula put $\mu=\sin^2\phi$, so $d\mu/\sqrt{\mu(1-\mu)}=2\,d\phi$ and $\int(\alpha+\beta\sin^2\phi)\,2\,d\phi=(2\alpha+\beta)\phi-\beta\sin\phi\cos\phi$. $\square$

The fork's closed form gives $J(3)=0.0955029$ at the benchmark, which matches the fork's quadrature. Table T2 encloses it from below by interval arithmetic: $(1-\tfrac1b)J(3)-k\ge0.02774$. [Referee fix: the text said $\ge0.02775$. The certified lower bound in `certificates.csv` is $0.0277493$, which is below $0.02775$; the quadrature value is $0.0277514$.] This closes open item 1 of `mechanism.md`; Proposition F.3(ii) at the benchmark vector is computer-assisted.

**Proposition CD.7 (full orders, pools, and the cutoff family under a general $G$; analytical).** *Suppose $g_M>0$ and orders are $(1,-1)$.*

*(a) The forced pool is a half-line $Z_0=(-\infty,z_0)$ or $(-\infty,z_0]$. It is empty in regime I. Otherwise $z_0=\tfrac b2\operatorname{logit}\mu_0$ when $\mu_0\in(m,M]$, and $z_0=-1$ when $\mu_0=m$.*

*(b) The pool belief $\bar\mu(x')=\Pr(H\mid X<x')=F_Z(x'-1)/[F_Z(x'-1)+F_Z(x'+1)]$ equals $m$ on $x'\le-1$, is continuous and strictly increasing on $(-1,\infty)$, and tends to $\tfrac12$.*

*(c) A half-line pool $(-\infty,x')$ with $x'\ge z_0$ satisfies the challenger's condition if and only if $\varphi(\bar\mu(x'))=0$. The consistent cutoffs therefore form an interval from $z_0$ to $\bar x'$, where $\bar\mu(\bar x')=\mu_0$. The interval is empty in regime I, bounded when $\mu_0<\tfrac12$ (regime II), and equal to $[z_0,\infty)$ in regime III.* [Referee fix: regime II also contains the tie case $\mu_0=\tfrac12$ with an atom at $c_0=B_r(\tfrac12)$. Then $\varphi(\mu)=0$ exactly for $\mu<\tfrac12$, and the interval is $[z_0,\infty)$, as in Table T5, row $c'=4.2917$.]

*(d) The minimal pool $x'=z_0$ is always consistent. Every consistent cutoff with $k\le(1-\tfrac1b)J_G(x')$ gives an equilibrium.*

*Proof.* (a) Under full orders $\mu_X$ is nondecreasing, and $\varphi(\mu_X(x))=0$ if and only if $B_r(\mu_X(x))<c_0$, or equality without an atom. (b) Write $\eta(z)=f(z)/F_Z(z)$ for the reverse hazard. For Laplace noise $\eta(z)=1/b$ on $z\le0$ and $\eta(z)=1/[b(2e^{z/b}-1)]$ on $z>0$, which is strictly decreasing. The derivative of $\log[F_Z(x'-1)/F_Z(x'+1)]$ is $\eta(x'-1)-\eta(x'+1)$. It is zero when $x'\le-1$ and strictly positive when $x'>-1$, since then $x'+1>0$. At $x'=-1$ direct evaluation gives $\bar\mu=e^{-2/b}/(1+e^{-2/b})=m$. As $x'\to\infty$ both CDFs tend to one. (c) Lemma CD.2(c) and (e). In regime III, $B_r(\bar\mu(x'))<B_r(\tfrac12)\le c_0$ for every finite $x'$, so every cutoff is consistent. (d) The convexity argument of Theorem CD.3(iv), and the investor argument there with $J_G(x')$ in place of $J_G$. $\square$

**Lemma CD.8 (the existence test is exact when entry starts at a nonnegative flow; analytical).** *Under full orders, let the entry set be $A\subseteq[0,\infty)$. Then the profile is an equilibrium if and only if $k\le(1-\tfrac1b)J_G(x')$. In regime III every full-order half-line equilibrium has $A\subseteq[0,\infty)$.*

*Proof.* For the low type and $s\in[0,1]$, every $x\in A$ has $x+s\ge0$, so $f(x+s)=e^{-s/b}f(x)$ and $F_L(s)=e^{(1-s)/b}J_G$. The payoff of a short of size $s$ is $g(s)=s\,e^{(1-s)/b}J_G-ks$. Its derivative $e^{(1-s)/b}(1-s/b)J_G-k$ is strictly decreasing, so $g$ is strictly concave on $[0,1]$ and $s=1$ is optimal if and only if $g'(1)=(1-\tfrac1b)J_G-k\ge0$. Buying earns a nonpositive gross amount. When the test holds, the high type's full purchase is optimal by the bound in Theorem CD.3(iv). In regime III, $\mu_0\ge\tfrac12$, so $z_0\ge0$ and every consistent cutoff is at least $z_0$. $\square$

So the fork's test $k<(1-\tfrac1b)J(r)$ in Proposition F.2(c) is necessary as well as sufficient. Two consequences at the benchmark. The full-order region of the fork starts at $r=2.0155$ (root of the closed form; numerical diagnostic), between the fork's grid points $2.00$ and $2.05$. At $r=3$ the full-order cutoff family ends exactly at

$$
x'=1+b\log\frac{(1-\tfrac1b)m\Delta_T}{2k}=2.614,
$$

because $J(x')=\Delta_T m\,e^{-(x'-1)/b}/2$ for $x'\ge1$. Beyond it the grid family continues with partial shorts and collapses to $\mathcal D$ at $x'\approx3.27$ (Table T6).

**Corollary CD.9 (continuous costs keep the pool; analytical).** *Let $G$ be atomless with $g_m=0<g_M$. Under full orders and the minimal pool, the price is continuous in $x$. It equals $t_0$ on $(-\infty,z_0]$, rises strictly on $(z_0,1)$, and is constant on $[1,\infty)$. The price law has an atom at $t_0$ of mass $\tfrac12[F_Z(z_0-1)+F_Z(z_0+1)]\ge\tfrac14(1+e^{-2/b})$. A voluntary pool with cutoff $x'\in(z_0,1)$ creates a price jump of size $\varphi(\mu_X(x'))[w_L+\Delta_T\mu_X(x')]>0$ at $x'$. An atom of $G$ at $c_0\in(B_r(m),B_r(M))$ creates a jump of size $G(\{c_0\})[w_L+\Delta_T\mu_0]$ at $z_0$ even with the minimal pool.*

*Proof.* On $(z_0,1)$, $\mu_X$ is continuous and strictly increasing, $\varphi$ is continuous, and $\varphi(\mu_X(x))>0$, so Lemma CD.2(f) gives a continuous, strictly increasing price. At $z_0$, $\varphi(\mu_0)=G(c_0)=0$ because $G$ is atomless, so the price tends to $t_0$. The atom is $\Pr(X\le z_0)$, and $z_0\ge-1$. The jump sizes are the price of Lemma CD.2(b) evaluated at the cutoff. $\square$

So the answer to question 2 is no. A continuous $G$ makes the price continuous at the edge of the pool. It does not remove the pool, because the pool is the event of zero entry, and that event has positive probability whenever the lowest posterior lies below $\mu_0$. The next result says when that happens.

**Proposition CD.10 (where pools are forced; analytical).** *(a) In regime III every equilibrium has a pool of positive probability, and $\mathfrak m=0$ on it. (b) In regime II, pure orders $q_H>q_L$ admit a pool-free continuation if and only if $\varphi(1-M_q)>0$, where $M_q=(1+e^{-(q_H-q_L)/b})^{-1}$ is the largest posterior they produce. Full orders never do.*

*Proof.* (a) If $\sigma_H=\sigma_L$, then $\mu_X\equiv\tfrac12$, $e=g_{1/2}=0$, and the equilibrium is $\mathcal D$, whose pool is everything. Otherwise $\mu_X$ is not almost surely $\tfrac12$ [Referee fix: because Laplace convolution is injective, as in the proof of Proposition CD.4, $\sigma_H\ne\sigma_L$ gives $a_H\ne a_L$ on an open set], and $\mathbb E[\mu_X(X)]=\Pr(H)=\tfrac12$, so $\Pr(\mu_X<\tfrac12)>0$. On that event $\varphi(\mu_X)\le g_{1/2}=0$, so $Z_0$ has positive probability, and $N\supseteq Z_0$ by Lemma CD.2(c). (b) Pure orders give $\mu_X\in[1-M_q,M_q]$ with positive-probability plateaus at both ends. So $Z_0$ is null if and only if $\varphi(1-M_q)>0$, and then $N=\emptyset$ is consistent by Lemma CD.2(e). Full orders give $1-M_q=m$ and $\varphi(m)=g_m=0$. $\square$

The regime II example $G=U[3,9]$ shows both cases on the grid (Table T8, numerical diagnostic). For $r\in[1.75,1.90]$ the live fixed point has orders $(1,-v)$ with $v\le0.443$ and no pool, so the investor is an insider at every price. At $r=1.95$ the short reaches $v=0.53$, the lowest posterior falls below $\mu_0$, and a pool with probability $0.368$ appears. A stronger incumbent here creates a pool: on $37\%$ of flows the investor stops being an insider.

### 4.4 The shape of $G$ and the entry response

**Proposition CD.11 (entry is a Jensen gap; analytical).** *In every equilibrium, $\mathsf E=\mathbb E[\varphi(\mu_P)]$ and $\mathsf O_H=\mathbb E[\mu_P\,\varphi(\mu_P)]$, with $\mathbb E[\mu_P]=\tfrac12$. Hence, relative to an uninformative price, which gives $\mathsf E=g_{1/2}$ and $\mathsf O_H=g_{1/2}/2$:*

*(a) if $\varphi$ is convex on $[m,M]$, every equilibrium has $\mathsf E\ge g_{1/2}$; if concave, $\mathsf E\le g_{1/2}$; if affine, $\mathsf E=g_{1/2}$;*

*(b) if $\varphi=\alpha+\beta\mu$ on $[m,M]$, then $\mathsf O_H=g_{1/2}/2+\beta\operatorname{Var}(\mu_P)$;*

*(c) if $G$ is uniform on $[0,\bar c]$ with $\bar c\ge B_r(M)$ for all $r$ in an interval, then in every equilibrium at every such $r$, $\mathsf E(r)=B_r(\tfrac12)/\bar c$, which is strictly decreasing in $r$, although the investor is an insider at every price.*

*Proof.* Preparation has probability $\mathbb E[\Pr(\text{prepare}\mid P)]=\mathbb E[\varphi(\mu_P)]$. A prepared high-value challenger always wins in the benchmark, since $h>r$, and $C$ is independent of $\theta$ given the price, so $\mathsf O_H=\mathbb E[e(P)\mathbf 1\{\theta=h\}]=\mathbb E[e(P)\mu_P]$. The tower property gives $\mathbb E[\mu_P]=\tfrac12$, and Jensen's inequality gives (a). For (b), $\mathbb E[\mu_P(\alpha+\beta\mu_P)]=\alpha/2+\beta(\tfrac14+\operatorname{Var}\mu_P)$ and $\alpha+\beta/2=g_{1/2}$. For (c), $\varphi(\mu)=B_r(\mu)/\bar c$ is affine on $[m,M]$ because $0<B_r(m)$ and $B_r(M)\le\bar c$; regime I holds; $B_r(\tfrac12)$ falls in $r$ by (5). $\square$

This separates two questions that the benchmark answers with one assumption. The lower end of the support of $G$ decides whether the investor is an insider. The curvature of $G$ on $[B_r(m),B_r(M)]$ decides whether the information the insider reveals raises entry. The two-point benchmark has both: a floor, and a jump above $B_r(\tfrac12)$. The cost law $U[0,12]$, with the same mean as the fork, has the floor but no curvature. Its investor trades fully and is an insider at every price, but entry equals $B_r(\tfrac12)/12$ at every strength (Table T7: $0.3576$ at $r=3$, falling from $0.390$ at $r=1.6$ to $0.315$ at $r=5$; numerical diagnostic, matching (c)). Information then changes who enters, not how many: $\mathsf O_H$ exceeds the uninformative value by $\beta\operatorname{Var}(\mu_P)=0.0296$ at $r=3$. [Referee fix: the text said $0.0297$, the difference of the rounded entries $0.2085-0.1788$; the unrounded value is $0.029644$.] The entry reversal of Proposition 2 needs the price-sensitive cost mass to sit above the prior profit. [Referee fix: the note gives no proof; here is one. If $G$ puts no mass in $(B_{r_1}(\tfrac12),B_{r_1}(M)]$, then $\varphi\le\varphi(\tfrac12)$ on $[m,M]$ at $r_1$, so $\mathsf E(r_1)\le g_{1/2}(r_1)\le g_{1/2}(r_0)$ by (5). The right side is entry in an uninformative weak economy, so no reversal against it can occur. Analytical.]

### 4.5 Small cost noise and the selection question

**Lemma CD.12 (entry bound with informed trading; analytical).** *In every equilibrium in which some type trades with positive probability, $\Delta_T\,e^{2/b}\max\{e_H,e_L\}\ge k$, where $e_\theta=\Pr(\text{prepare}\mid\theta)$.*

*Proof.* This is the proof of Proposition F.2(b), with $A_H\le e(x)\Delta_T$ from Lemma CD.2(d). A correctly signed deviation of size $s$ by the high type earns at most $s[\Delta_T e^{2/b}e_H-k]$, by the ratio bound (8) integrated against the candidate order law. If both $e_\theta$ violate the bound, zero is each type's unique best response. $\square$

**Proposition CD.13 (uniform cost noise; analytical).** *Let $G_\varepsilon$ be uniform on $[c-\varepsilon,c+\varepsilon]$ with $c-\varepsilon>B_r(\tfrac12)$, and put $\tau_\pm=B_r^{-1}(c\pm\varepsilon)$ and $\delta=\varepsilon/(g_H-g_L)$.*

*(a) The economy is in regime III when $B_r(M)>c-\varepsilon$ and in regime IV otherwise. $\mathcal D$ exists for every $k$.*

*(b) Under full orders the minimal pool is $(-\infty,x_-]$ with $x_-=\tfrac b2\operatorname{logit}\tau_-$, entry rises linearly in the revealed belief from $0$ at $\tau_-$ to $1$ at $\tau_+$, and the price is continuous at $x_-$. Every half-line cutoff $x'\ge x_-$ satisfies the challenger's condition, so the whole cutoff family of Proposition CD.7 survives, cut only by the investor's test of Lemma CD.8.*

*(c) If $m<\tau_-$ and $\tau_+<M$, then*

$$
J_\varepsilon=J-\frac{\Delta_T e^{-1/b}}{24}\,w'(\tau)\,\delta^2+O(\delta^4),\qquad w(\mu)=\frac1{\sqrt{\mu(1-\mu)}},\quad w'(\tau)=\frac{2\tau-1}{2[\tau(1-\tau)]^{3/2}}>0 .
$$

*If $\tau_+>M$, the plateau term $g_M m/2$ of (CD.2) has $g_M<1$, and $J_\varepsilon$ falls at first order in $\varepsilon$.* [Referee fix: the loss is first order in $\varepsilon-\varepsilon^*$, where $\varepsilon^*=(M-\tau)(g_H-g_L)$ is the noise at which $\tau_+$ reaches $M$ ($\varepsilon^*=0.217$ at $r=3$). At $\tau=M$ the change is a jump: $g_M$ falls from one to one half for every $\varepsilon>0$. This sentence has no proof in the note; it is a numerical diagnostic (Table T3).]

*(d) As $r$ rises from $r_C(c+\varepsilon)$ to $r_C(c-\varepsilon)$, $g_M=G_\varepsilon(B_r(M))$ falls continuously from one to zero. Informed trading is impossible once $\Delta_T e^{2/b}g_M<k$, so every live branch ends strictly before $r_C(c-\varepsilon)$, with entry bounded below by $k e^{-2/b}/\Delta_T$ just before its end.*

*Proof.* (a) $g_{1/2}=0$ because $B_r(\tfrac12)<c-\varepsilon$, and $g_M>0$ if and only if $B_r(M)>c-\varepsilon$, since $G_\varepsilon$ is atomless. Theorem CD.3(ii). (b) Proposition CD.7 with $\mu_0=\tau_->\tfrac12$, Corollary CD.9, and Lemma CD.8. (c) The difference $d(\mu)=\varphi_\varepsilon(\mu)-\mathbf 1\{\mu\ge\tau\}$ satisfies $d(\tau-u)=(\delta-u)/(2\delta)=-d(\tau+u)$ on $u\in[0,\delta]$. By (CD.2), $J_\varepsilon-J=\Delta_T\tfrac{e^{-1/b}}4\int_0^\delta\tfrac{\delta-u}{2\delta}[w(\tau-u)-w(\tau+u)]\,du$. Expand $w(\tau-u)-w(\tau+u)=-2uw'(\tau)+O(u^3)$ and integrate: $\int_0^\delta(\delta-u)u\,du=\delta^3/6$. (d) Every price belief is at most $M$, so $e_\theta\le g_M$; apply Lemma CD.12. $\square$

[Referee fix: Lemma CD.12 bounds only $\max\{e_H,e_L\}$, and $\mathsf E=(e_H+e_L)/2$ is only at least half of that. The stated bound on entry still holds. The ratio bound (8) also gives $f(x-s)\le e^{2/b}a_L(x)$, because it holds against every order in the support of $\sigma_L$. So a high-type order of size $s$ earns at most $s[\Delta_T e^{2/b}e_L-k]$, and a low-type short earns at most $s[\Delta_T e^{2/b}e_H-k]$. If either type trades, then $\min\{e_H,e_L\}\ge ke^{-2/b}/\Delta_T$, and $\mathsf E\ge\min\{e_H,e_L\}$.]

So small noise changes nothing qualitative away from the ceiling (Table T3, numerical diagnostic): at $r=3$ and $\varepsilon=0.1$, $J$ moves by $-5.2\times10^{-6}$, as (c) predicts, and entry by $-6\times10^{-5}$. The dead equilibrium, the live equilibrium, and the whole cutoff family remain. Near the ceiling the picture changes. In the fork the live branch runs to $r_C=3.5927$ and then jumps to $\mathcal D$ from entry $(1+e^{-2/b})/4=0.342$, by (A.14) with $\rho=0$. With $\varepsilon=0.1$ entry falls steeply but continuously after $r_C(6.1)$, the investor's test fails at $r=3.7026$, and the branch jumps to $\mathcal D$ from entry $0.105$, well before $r_C(5.9)=3.866$ (Tables T7 and T9, Figure panel (b); numerical diagnostic). With $\varepsilon=0.5$ the end is at $r=4.3507$, from entry $0.079$. Cost noise turns an end set by the challenger into an end set by the investor.

**Theorem CD.14 (what a cost perturbation selects; analytical).** *Fix $r$ with $B_r(\tfrac12)<c<B_r(M)$, so that the fork is in regime III, and fix $k>0$. Let $G_n\to\delta_c$ weakly.*

*(i) The dead equilibrium survives. For all large $n$ the economy with $G_n$ has an uninformative-price equilibrium. Its entry $G_n(B_r(\tfrac12))$ tends to zero and its price tends to $t_0$, so it converges to $\mathcal D$.*

*(ii) The live equilibrium survives. If $k<(1-\tfrac1b)J$, with $J$ the fork's statistic, then for all large $n$ the economy with $G_n$ has the full-order minimal-pool equilibrium of Proposition CD.7. Its statistic, entry, and price converge to the fork's minimal-pool values, the price at every $x\ne x^*$.*

*(iii) The pool is selected by the location of the lowest cost. Let $\mu_0^n=B_r^{-1}(c_0^n)$ for the lowest cost $c_0^n$ of $G_n$, and $\mu^*=\limsup_n\mu_0^n$. Every pointwise limit of full-order half-line-pool equilibria of $G_n$ is the fork's minimal-pool equilibrium or a fork cutoff member with pool belief $\bar\mu(x')\le\mu^*$. For the two-point law $G_\eta=\eta\,\delta_{c'}+(1-\eta)\delta_c$ with $c'<c$, every equilibrium of the fork's cutoff family with $x'\ge x^*$ and $\bar\mu(x')<B_r^{-1}(c')$ is an exact equilibrium of every $G_\eta$. Hence the limit set as $\eta\to0$ is the fork family cut at pool belief $B_r^{-1}(c')$, and it is the minimal pool alone if and only if $c'\le B_r(\bar\mu(x^*))$.*

*(iv) Mass relative to the trading cost selects trade. For any $G$, every equilibrium has an informative price if and only if $G(B_r(\tfrac12))>2k/\Delta_T$; every equilibrium has full orders if $G(B_r(m))>k/[(1-\tfrac1b)m\Delta_T]$. No sequence with $G_n\to\delta_c$ satisfies the first condition for large $n$ at a fixed $k$. Along a sequence $(G_n,k_n)$, uninformative prices disappear exactly when $G_n(B_r(\tfrac12))>2k_n/\Delta_T$.*

*Proof.* (i) $(-\infty,y]$ is closed, so weak convergence gives $\limsup_n G_n(y)\le\delta_c((-\infty,y])=0$ for $y<c$. Hence $G_n(B_r(\tfrac12))\to0$, and (CD.1) holds for large $n$. The price $t_0+G_n(B_r(\tfrac12))[w_L+\Delta_T/2]$ tends to $t_0$.

(ii) For $\mu\ne\tau$, $B_r(\mu)\ne c$ is a continuity point of the limit CDF, so $G_n(B_r(\mu))\to\mathbf 1\{\mu\ge\tau\}$. In particular $G_n(B_r(m))\to0$ and $G_n(B_r(M))\to1$, since $B_r(m)<c<B_r(M)$. The integrand of (CD.2) is bounded by the integrable $w$, so dominated convergence gives $J_{G_n}\to J>k/(1-\tfrac1b)$. Proposition CD.7(d) applies for large $n$. Entry and prices converge pointwise off $\mu_X=\tau$, that is, off $x=x^*$, and entry converges by dominated convergence.

(iii) A $G_n$ member with cutoff $x_n'$ needs $\varphi_n(\bar\mu(x_n'))=0$, so $B_r(\bar\mu(x_n'))\le c_0^n$ and $\bar\mu(x_n')\le\mu_0^n$. Take a subsequence with $x_n'\to x'_\infty\in[-\infty,\infty]$. For $x\notin\{x'_\infty,x^*\}$, entry $\mathbf 1\{x\ge x_n'\}G_n(B_r(\mu_X(x)))$ tends to $\mathbf 1\{x\ge x'_\infty\}\mathbf 1\{\mu_X(x)\ge\tau\}$. If $x'_\infty\le x^*$ this is the minimal-pool entry. Otherwise it is the fork member $x'_\infty$, and continuity of $\bar\mu$ gives $\bar\mu(x'_\infty)\le\mu^*$. In both cases the limit pool belief is below $\tfrac12<\tau$, so the fork's challenger condition holds. The investor's payoff from each order converges by dominated convergence, so the full order stays a best response, and the limit profile is an equilibrium of the fork. For the two-point law and $x'\ge x^*$: on $[x',\infty)$, $\mu_X\ge\tau$, so $B_r(\mu_X)\ge c>c'$ and $G_\eta=1$, as in the fork; on the pool, $B_r(\bar\mu(x'))<c'$, so $G_\eta=0$. The two schedules coincide, so the investor problems coincide. Since $\bar\mu$ is increasing and the atom at $c'$ needs $\bar\mu(x')<B_r^{-1}(c')$, no member with $x'\ge x^*$ exists when $B_r^{-1}(c')\le\bar\mu(x^*)$. The minimal pool of $G_\eta$ always exists for $k<(1-\tfrac1b)J$, because its entry dominates the fork's pointwise, so its statistic is at least $J$.

[Referee fix: two small gaps in (iii). First, the limit $x'_\infty=+\infty$ must be excluded. It is: each $G_n$ member has $U_n(1)\ge U_n(0)=0$, while the limit schedule has no entry and gives the full order $-k<0$, which contradicts the convergence of payoffs. Second, the "only if" in the last sentence needs $k<(1-\tfrac1b)J$ strictly, so that fork members just above $x^*$ pass the investor test; at $k=(1-\tfrac1b)J$ only the minimal pool survives for every $c'$.]

(iv) The first claim is Proposition CD.4: an informative price in every equilibrium is the failure of (CD.1). The second is Proposition CD.5. The third is part (i). $\square$

[Referee fix: the "every equilibrium" claims in (iv) are vacuous if no equilibrium exists. When (CD.1) fails, this note proves existence only for $k\le\bar k_G$ (Theorem CD.3(iv), Proposition CD.7(d)). For $\bar k_G<k<\Delta_T g_{1/2}/2$, existence is shown only by grid fixed points (for example $U[3,9]$ at $r=1.75$, Table T8), so it is a numerical diagnostic there. "Selects informative prices" should be read as "removes every uninformative equilibrium".]

**Corollary CD.15 (the benchmark floor as a perturbation; analytical).** *For $G_\rho=\rho\,\delta_{c_L}+(1-\rho)\delta_c$ with $c_L\le B_r(m)$ and $\rho\to0$: the economy is in regime I for every $\rho>0$, so no pool exists; the no-trade equilibrium exists if and only if $\rho\le2k/\Delta_T$, that is, $r\le r_N(\rho)$; and the full-order equilibrium converges to the fork's minimal-pool member, since $c_L\le B_r(m)<B_r(\bar\mu(x^*))$.*

This is Proposition F.5, read through Theorem CD.14. It also sharpens F.5(a). The floor need not sit below $B_r(m)$ to select the minimal pool. Any vanishing mass at a cost no higher than $B_r(\bar\mu(x^*))=3.195$ does the same at $r=3$ (Table T5). Mass anywhere below $B_r(\tfrac12)=4.292$ cuts the family. [Referee fix: it cuts the half-line family at pool belief $B_r^{-1}(c')$. The full-order family already ends at $x'=2.614$, so mass at $c'$ cuts it only when $c'<B_r(\bar\mu(2.614))=3.945$; see Table T5, row $c'=4$.] Cost noise above $B_r(\tfrac12)$ cuts nothing.

The sharp answer to question 3 is therefore: **location selects the pool; mass relative to $k$ selects trade.** No vanishing cost perturbation selects the live equilibrium over the dead one at a fixed trading cost. A cost law selects informative prices if and only if more than $2k/\Delta_T(r)$ of its mass lies at or below the prior profit $B_r(\tfrac12)$. At $r=3$ that is $6\%$.

## 5. Numerics

All tables below are generated by `render.py` from CSV files in this folder; `tables.md` holds the full versions. Benchmark primitives $(h,\ell,p,b,k)=(10,1,0.5,2,0.02)$. The declared cost laws are in `laws.csv`: the fork $\delta_6$; uniform noise $U[5.9,6.1]$ and $U[5.5,6.5]$; $U[3,9]$; $U[0,12]$; and the benchmark two-point law $(c_L,c_H,\rho)=(1,6,0.25)$. The first five have mean cost $6$.

**Methods.** `core.py` evaluates the closed forms of Lemma CD.6 and the state entry probabilities by adaptive quadrature. `grid.py` generalizes the fork's best-response solver to any $G$: a flow grid of 60,001 points on $[-30,30]$, an order grid of step $0.01$ with local refinement, and iteration from five correctly signed starts. `certify.py` encloses the $r=3$ quantities with `mpmath` interval arithmetic and exact rational arithmetic. `solve.py` writes the CSV files and `render.py` reads them. Status: grid rows and quadrature values are numerical diagnostics; rows marked computer-assisted carry interval certificates; regime labels at $r=3$ and the no-trade test are exact.

**T1. Cost laws at $r=3$.** Full orders, minimal pool. $B_3(m)=2.366$, $B_3(\tfrac12)=4.292$, $B_3(M)=6.217$. Numerical diagnostic, except the regime and existence columns, which T2 certifies.

| law | regime | $g_{1/2}$ | $\mathcal D$ | no trade | $\Pr$(pool) | $J$ | $\mathsf E$ | $\mathsf E-g_{1/2}$ | $\mathsf O_H$ | min $\mathfrak m$ | grid starts to live |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fork $\delta_6$ | III | 0 | yes | yes | 0.636 | 0.0955 | 0.3637 | 0.3637 | 0.2656 | 0 | 1/5 |
| $U[5.9,6.1]$ | III | 0 | yes | yes | 0.627 | 0.0955 | 0.3636 | 0.3636 | 0.2655 | 0 | 1/5 |
| $U[5.5,6.5]$ | III | 0 | yes | yes | 0.592 | 0.0711 | 0.2699 | 0.2699 | 0.1966 | 0 | 2/5 |
| $U[3,9]$ | II | 0.215 | no | no | 0.401 | 0.0699 | 0.2546 | 0.0394 | 0.1776 | 0 | 5/5 |
| $U[0,12]$ | I | 0.358 | no | no | 0 | 0.0989 | 0.3576 | 0.0000 | 0.2085 | 0.131 | 5/5 |
| benchmark | I | 0.250 | no | no | 0 | 0.1407 | 0.5228 | 0.2728 | 0.3242 | 0.167 | 5/5 |

Two facts stand out. In regimes I and II at $r=3$ no uninformative equilibrium exists (Proposition CD.4), and every grid start reaches the full-order profile. In regime III most starts fall into $\mathcal D$. And $U[0,12]$ has $\mathsf E=g_{1/2}$ exactly, as Proposition CD.11(c) says.

**T2. Interval certificates at $r=3$ (computer-assisted).** A lower Riemann sum of (CD.2) on 20,000 cells with interval arithmetic gives a rigorous lower bound $J_{\rm low}$. A positive margin $(1-\tfrac1b)J_{\rm low}-k$ certifies the full-order minimal-pool equilibrium by Proposition CD.7(d).

| law | regime | $g_{1/2}$ exact | no trade exists | $J_{\rm low}$ | margin | full-order equilibrium | unique full orders |
|---|---|---|---|---|---|---|---|
| fork $\delta_6$ | III | 0 | yes | 0.09550 | 0.02775 | certified | no |
| $U[5.9,6.1]$ | III | 0 | yes | 0.09549 | 0.02775 | certified | no |
| $U[5.5,6.5]$ | III | 0 | yes | 0.07112 | 0.01556 | certified | no |
| $U[5,7]$ | III | 0 | yes | 0.06424 | 0.01212 | certified | no |
| $U[4.5,7.5]$ | III | 0 | yes | 0.06400 | 0.01200 | certified | no |
| $U[3,9]$ | II | 31/144 | no | 0.06987 | 0.01493 | certified | no |
| $U[0,12]$ | I | 103/288 | no | 0.09886 | 0.02943 | certified | no |
| benchmark | I | 1/4 | no | 0.14073 | 0.05036 | certified | certified |
| $\rho=0.01$ floor | I | 1/100 | yes | 0.09731 | 0.02865 | certified | no |
| $0.05\,\delta_{3.5}+0.95\,\delta_6$ | II | 1/20 | yes | 0.09860 | 0.02930 | certified | no |

**T3. Uniform cost noise $U[6-\varepsilon,6+\varepsilon]$ at $r=3$ (numerical diagnostic).**

| $\varepsilon$ | $\mathcal D$ | pool end $x_-$ | $\Pr$(pool) | $J$ | $\mathsf E$ | full-order cutoff end | $r_C(6-\varepsilon)$ |
|---|---|---|---|---|---|---|---|
| 0 | yes | 0.8712 | 0.6363 | 0.095503 | 0.3637 | 2.614 | 3.593 |
| 0.01 | yes | 0.8655 | 0.6354 | 0.095503 | 0.3637 | 2.614 | 3.620 |
| 0.1 | yes | 0.8142 | 0.6269 | 0.095498 | 0.3636 | 2.614 | 3.866 |
| 0.25 | yes | 0.7309 | 0.6133 | 0.089611 | 0.3410 | 2.478 | 4.275 |
| 0.5 | yes | 0.5971 | 0.5919 | 0.071124 | 0.2699 | 1.949 | 4.959 |
| 1.0 | yes | 0.3433 | 0.5523 | 0.064245 | 0.2420 | 1.621 | 6.325 |
| 1.5 | yes | 0.1001 | 0.5152 | 0.064007 | 0.2390 | 1.498 | 7.692 |

Up to $\varepsilon=0.1$ the change is second order, as Proposition CD.13(c) predicts. From $\varepsilon=0.25$, $\tau_+>M$ and the change is first order. The closed form of Lemma CD.6 reproduces the $\varepsilon=0.1$ value of $J$ to ten digits.

**T4. The benchmark floor $\rho\to0$ at $r=3$, with $c_L=1$ and $c_H=6$.** $r_N$ and $r_U$ are closed forms (analytical); $J$ and $\mathsf E$ are quadrature values (numerical diagnostic).

| $\rho$ | no trade at $r=3$ | $r_N(\rho)$ | $r_U(\rho)$ | $J$ | $\mathsf E$ | $\mathsf E-\mathsf E_{\rm fork}$ | sup price gap |
|---|---|---|---|---|---|---|---|
| 0.25 | no | 1.748 | 2.837 | 0.14073 | 0.5228 | 0.1591 | 0.2321 |
| 0.10 | no | 2.380 | 4.765 | 0.11359 | 0.4273 | 0.0636 | 0.0928 |
| 0.06 | yes (equality) | 3.000 | 6.811 | 0.10636 | 0.4019 | 0.0382 | 0.0557 |
| 0.01 | yes | 9.899 | 31.715 | 0.09731 | 0.3700 | 0.0064 | 0.0093 |
| 0.001 | yes | 81.988 | 299.459 | 0.09568 | 0.3643 | 0.0006 | 0.0009 |
| 0 (fork) | yes | $\infty$ | $\infty$ | 0.09550 | 0.3637 | 0 | 0 |

The entry gap is exactly $\rho\Pr(X<x^*)$, since the floor adds entry $\rho$ only on the fork's pool. The price gap is $\rho(w_L+\Delta_T\tau)$.

**T5. The lowest added cost selects the pool, $r=3$, $\eta=0.05$.** The two-point law $\eta\,\delta_{c'}+(1-\eta)\delta_6$. The limit set is the set of fork cutoffs that survive as $\eta\to0$ (Theorem CD.14(iii)); its right end is cut further by the full-order test at $2.614$. Analytical classification; cutoffs by root finding (numerical diagnostic).

| $c'$ | $B_r^{-1}(c')$ | regime | largest consistent cutoff | limit set | no trade exists |
|---|---|---|---|---|---|
| 1.000 | 0.105 | I | no pool | minimal pool | yes |
| 2.366 $=B_r(m)$ | 0.269 | I (atom, tie rule) | no pool | minimal pool | yes |
| 3.000 | 0.345 | II | 0.593 | minimal pool | yes |
| 3.195 $=B_r(\bar\mu(x^*))$ | 0.368 | II | 0.871 $=x^*$ | minimal pool | yes |
| 3.500 | 0.405 | II | 1.320 | cutoffs $[0.871,1.320]$ | yes |
| 4.000 | 0.465 | II | 2.911 | cutoffs $[0.871,2.614]$ | yes |
| 4.500 | 0.525 | III | $\infty$ | whole family | yes |

The last column is the point of Theorem CD.14(iv): every row keeps the no-trade equilibrium, because $\eta\Delta_T=0.033\le2k=0.04$.

**T6. Grid cutoff families at $r=3$ (numerical diagnostic).**

| law | first cutoff | last live cutoff | $\mathsf E$ first | $\mathsf E$ last live | first inconsistent cutoff | collapse to $\mathcal D$ |
|---|---|---|---|---|---|---|
| fork $\delta_6$ | 0.871 | 3.221 | 0.3636 | 0.1165 | none | 3.271 |
| $U[5.5,6.5]$ | 0.597 | 1.947 | 0.2699 | 0.1527 | none | 1.997 |
| $0.05\,\delta_{3.5}+0.95\,\delta_6$ | $-0.385$ | 1.315 | 0.3734 | 0.2921 | 1.365 | none |

The grid reproduces the analytical cut at $1.320$ for the two-point law.

**T7. Live branches across strengths (numerical diagnostic).** The no-trade column is analytical (Proposition CD.4).

| law | no trade exists on | live found on | max live $\mathsf E$ | live $\mathsf E$ at $r=3$ | live $\mathsf E$ at last $r$ |
|---|---|---|---|---|---|
| fork $\delta_6$ | $[1.20,5.00]$ (as $\mathcal D$) | $[1.70,3.59]$ | 0.394 at 2.00 | 0.3636 | 0.342 |
| $U[5.9,6.1]$ | $[1.20,5.00]$ (as $\mathcal D$) | $[1.70,3.70]$ | 0.394 at 2.00 | 0.3636 | 0.105 |
| $U[5.5,6.5]$ | $[1.20,5.00]$ (as $\mathcal D$) | $[1.95,4.35]$ | 0.393 at 2.00 | 0.2699 | 0.079 |
| $U[3,9]$ | $[1.20,1.70]$ | $[1.75,5.00]$ | 0.280 at 2.25 | 0.2546 | 0.190 |
| $U[0,12]$ | $[1.20,1.55]$ | $[1.60,5.00]$ | 0.390 at 1.60 | 0.3576 | 0.315 |

For the two laws in regimes I and II, the live branch begins at the first grid point after the no-trade equilibrium ends; no grid point has both or neither. This is a finding on this grid, not a theorem: in the benchmark, which is in regime I, Proposition 3 certifies informative equilibria that coexist with no trade. In regime III the dead and live equilibria coexist on the whole live range.

**T8. Regime II, $G=U[3,9]$: pool-free and pooled live equilibria (numerical diagnostic).**

| $r$ | $(q_H,q_L)$ | $\Pr$(pool) | $\mathsf E$ | $g_{1/2}$ | $\mathsf O_H$ |
|---|---|---|---|---|---|
| 1.75 | $(1,-0.073)$ | 0 | 0.2723 | 0.2723 | 0.1580 |
| 1.90 | $(1,-0.443)$ | 0 | 0.2651 | 0.2651 | 0.1690 |
| 1.95 | $(1,-0.530)$ | 0.368 | 0.2642 | 0.2628 | 0.1721 |
| 2.10 | $(1,-0.815)$ | 0.380 | 0.2751 | 0.2558 | 0.1865 |
| 2.25 | $(1,-1)$ | 0.389 | 0.2797 | 0.2488 | 0.1943 |

Without a pool, $\varphi$ is affine on the range of $\mu_X$ and $\mathsf E=g_{1/2}$ exactly (Proposition CD.11(a)). The pool adds a convex kink, and entry rises above $g_{1/2}$.

**T9. Where the full-order branch ends (`full_order_boundaries.csv`; root finding on the closed form, numerical diagnostic).** [Referee fix: `render.py` does not write this table; it is assembled from `full_order_boundaries.csv` and `branches.csv`, and the T9 in `tables.md` has other columns. The opening sentence of this section overstates the provenance for T9.]

| law | full orders start | full orders end | reason | last grid live $r$ | $\mathsf E$ there |
|---|---|---|---|---|---|
| fork $\delta_6$ | 2.0155 | 3.5927 | preparation ceiling | 3.5926 | 0.342 |
| $U[5.9,6.1]$ | 2.0155 | 3.7026 | investor test fails | 3.70 | 0.105 |
| $U[5.5,6.5]$ | 2.0161 | 4.3507 | investor test fails | 4.35 | 0.079 |

**Figure.** `cost_regimes.pdf`. Panel (a): the three profit levels $B_r(m)$, $B_r(\tfrac12)$, $B_r(M)$ against $r$, with the regimes of the lowest cost $c_0$ shaded, and the lowest costs of the declared laws marked on the right axis. Panel (b): entry on the live branch against $r$ for the fork, $U[5.9,6.1]$, $U[5.5,6.5]$, and $U[0,12]$; filled points mark the last live grid strength; the dead branch at zero belongs to the three regime III laws.

**Files.** `core.py` (closed forms, regimes, quadrature), `grid.py` (best-response checks), `solve.py` (writes `laws.csv`, `regime_map.csv`, `laws_r3.csv`, `eps_r3.csv`, `floor_rho.csv`, `lowest_cost_r3.csv`, `family_r3.csv`, `full_order_boundaries.csv`, `branches.csv`), `certify.py` (writes `certificates.csv`), `render.py` (writes `tables.md` and `cost_regimes.pdf`). Run `python3 solve.py`, `python3 certify.py`, then `python3 render.py` from this folder. The solver takes about six minutes and the certificates about half a minute.

## 6. What this means for "when is the investor an insider"

### 6.1 The answer in one line

The investor is an insider when some challenger would prepare at the price it faces. With a cost law $G$, that is one number, the lowest cost $c_0$, compared with three profit levels. If even the most pessimistic market belief covers the cheapest cost, the investor is an insider at every price (regime I). If the prior covers it but the worst belief does not, the investor is an insider in every equilibrium, though some prices can carry no information about the stock (regime II). If only a favorable price covers it, insider status is an equilibrium outcome (regime III) [Referee fix: for small trading cost; for $k>M\Delta_T g_M$ the investor is a bystander in the unique equilibrium]. If no price covers it, the investor is a bystander (regime IV).

Three properties of $G$ do three different jobs.

1. **The lower end of the support decides insider status** (Theorem CD.3). Only $c_0$ and the presence of an atom at $c_0$ matter.
2. **The mass at or below the prior profit, relative to $k/\Delta_T$, decides whether informed trading is forced** (Proposition CD.4, Theorem CD.14(iv)). Mass above $2k/\Delta_T$ removes every uninformative equilibrium; mass at or below $B_r(m)$ above $k/[(1-\tfrac1b)m\Delta_T]$ forces full orders.
3. **The curvature of $G$ on $[B_r(m),B_r(M)]$ decides whether information raises entry** (Proposition CD.11). Insider status does not imply the entry reversal.

The benchmark's (A1) is the assumption of regime I, and (A3)'s right inequality is the mass condition of Proposition CD.5. The paper's sentence in Section 4.1, "without the floor, nobody prepares, proceeds do not depend on challenger quality, and the investor has nothing to trade on," is true in regimes III and IV only. Regime II has no floor and no dead equilibrium. There the investor is an insider in every equilibrium, and informed trading is forced once $g_{1/2}>2k/\Delta_T$, but prices can pool.

Competition acts on insider status through two channels with opposite signs. It lowers all three profit levels, so for a fixed $G$ the regime index can only rise with $r$: a stronger incumbent moves the economy away from guaranteed insider status. And it raises $\Delta_T$, the stake that makes trading on $\theta$ worth $k$. In the fork the regime is III on all of $(\ell,r_C)$, so "competition creates the insider" (Proposition F.3) is entirely the second channel. The first channel is what ends the insider at $r_C$. The $U[3,9]$ example shows the first channel inside regime II: a stronger incumbent turns a pool-free equilibrium into one with a pool on $37\%$ of flows.

Lemma CD.1 also names a second gate. Materiality needs $\mathbb E[(R-\ell)_+]>0$, so an incumbent that can beat a low-value challenger with positive probability. Insider status is the product of a lower tail of costs and an upper tail of incumbent values.

### 6.2 The other random variables

The fork kills the randomness of the cost. The model has four other sources of randomness. For each one, the question is whether killing it makes insider status endogenous, and whether it makes a good fork. All statements below are analytical by direct computation unless marked. [Referee fix: this label is too broad. The payoff formulas in items 1 and 2, the band width $\tanh(1/b)(g_H-g_L)$ and the bound $b\le2/\operatorname{logit}\tau$ in item 3, and the identity for $\mathfrak m$ with state-dependent entry in the fifth source are analytical. The limits $b\to\infty$ and $b\to0$ in item 3, the claims in item 4, and the ranking table are informal; their status is open.]

1. **Challenger quality $\theta$ (degenerate prior).** If the prior puts mass one on $h$ or $\ell$, everyone knows $\theta$, the residuals $e\Delta_T(1-\mu)$ and $e\Delta_T\mu$ vanish, and the investor never trades. The knowledge stays material through $\Delta_T$ but it is no longer nonpublic, so the investor is never an insider. This kills the question rather than answering it. Not a promising fork. A non-degenerate asymmetric prior $\pi$ is a useful lever instead: by Lemma OA.2 the three profit levels become $B_r(\mu_-)$, $B_r(\pi)$, $B_r(\mu_+)$, and $\mathcal D$ exists if and only if $G(B_r(\pi))=0$.

2. **Incumbent value $R$ (deterministic incumbent $R\equiv\bar r\in(\ell,h)$).** Then $t_0=p$, $t_H=\bar r$, $t_L=\ell$, $g_H=h-\bar r$, $g_L=0$, and $\Delta_T=\bar r-\ell$. Materiality is still $\Delta_T G(B(\mu_P))$, so the entry gate is unchanged and insider status is exactly as endogenous as in the fork. What changes is tractability: $B(\mu)=\mu(h-\bar r)$ and $\tau=c/(h-\bar r)$ are linear, and the second gate becomes $\bar r>\ell$. A good teaching special case, not a new mechanism.

3. **Noise $Z$ (the limits $b\to\infty$ and $b\to0$).** The width of the band of lowest costs in which insider status at a price is an equilibrium outcome, regimes II and III together, is $B_r(M)-B_r(m)=\tanh(1/b)(g_H-g_L)$. As $b\to\infty$ the band closes, $\mu_P\to\tfrac12$, and insider status becomes exogenous again: the investor is an insider if and only if $g_{1/2}>0$. In the fork the live region needs $\tau\le M(b)$, that is $b\le2/\operatorname{logit}\tau$, which is $b\le2.296$ at $r=3$. As $b\to0$, outside the declared domain $b>1$, the band widens to $[g_L,g_H]$, but the price reveals the orders, the residuals vanish on the entry set, and no informed trade can pay $k$: the Grossman–Stiglitz problem. Killing the noise kills trading, not materiality. As a comparative static in $b$ it is cheap and informative; as a fork it is degenerate.

4. **The investor's signal precision.** The investor already knows $\theta$ exactly, so this randomness is already killed. Adding noise, a signal with accuracy $a\in(\tfrac12,1)$, scales materiality by the posterior gap $\Pr(H\mid T=+,\pi)-\Pr(H\mid T=-,\pi)$ but keeps the gate $G(B_r(\mu_P))>0$; insider status is unchanged. Making precision a choice, with a cost of learning $\theta$, adds a second gate on the investor's side: in $\mathcal D$ information has no value, so nobody acquires it. This makes the first object of the fork's Section 5, the signal itself, endogenous, as in @DowGoldsteinGuembel2017. It is the fork's open item 3 and the most promising of the four.

A fifth source deserves a line: the challenger's own signal of Section 5.3. A favorable private signal can play the role of the floor. If $G(B_r(\phi_+(m)))>0$, where $\phi_+$ is the posterior after a favorable signal, then entry is positive at every price, and with state-dependent entry Lemma CD.1 becomes $\mathfrak m(\pi)=e_H(\pi)\Delta_T+[e_H(\pi)-e_L(\pi)]w_L\ge e_H(\pi)\Delta_T$. Insider status then depends on the lower tail of the challenger's net cost, $C$ minus the profit its own signal adds. The cost law in this note stands in for any randomness in participation that the price does not drive.

**Ranking, most promising first.**

| rank | variable | does insider status become endogenous | why |
|---|---|---|---|
| 1 | investor's precision, made a choice | yes, from a second side | two-sided fixed point; may change selection between live and dead |
| 2 | noise scale $b$, as a comparative static | it sets the width of the endogenous band | one closed-form threshold, $b\le2/\operatorname{logit}\tau$; killing noise is degenerate |
| 3 | incumbent value, made deterministic | no change to the gate | linear closed forms; exposes the second gate $\bar r>\ell$ |
| 4 | challenger quality, made known | no: the question disappears | asymmetric priors are a useful lever instead |

## 7. Open items and the next best step

1. **The full equilibrium set in regime II.** This note shows pool-free equilibria with interior shorts (numerical diagnostic) and pooled equilibria with full orders (computer-assisted at $r=3$). Mixed profiles and the transition at $r\approx1.95$ for $U[3,9]$ are open.
2. **Pools that are not half-lines.** Lemma CD.2(e) allows any measurable $N\supseteq Z_0$ with $\varphi(\bar\mu_N)=0$. Under full orders a pool can include islands of high flow. The cutoff family is therefore not the whole equilibrium set, in the fork or here. Open.
3. **Partial-order continuations past the investor's test.** On the grid the noisy branches jump to $\mathcal D$ where the full-order test fails (T9). Whether interior-order equilibria continue them is open; five grid starts found none.
4. **Certificates beyond $r=3$.** The branch ends in T9 and the regime II transition are root findings and grid fixed points. Interval enclosures of the closed form of Lemma CD.6 along $r$ would make the full-order intervals computer-assisted.
5. **Live versus dead in regime III.** Cost perturbations do not select (Theorem CD.14). The candidate devices left are on the investor's side: paid information acquisition (Section 6.2), or a selection argument that uses the payoff ranking in the fork's Section 6.

**Next best step.** Test whether Proposition 2 survives in regime II in a weaker form, with (A1) replaced by "$g_m=0<g_{1/2}$" and with $g_{1/2}(r_1)>2k/\Delta_T(r_1)$. Proposition CD.4 then gives an informative price in every equilibrium at $r_1$, and Theorem CD.3(v) can give a unique uninformative equilibrium at $r_0$. The open step is the comparison: Proposition CD.11 shows that the entry ranking needs curvature of $G$ above the prior profit, and the cutoff family of Proposition CD.7 gives a continuum of entry levels at $r_1$. The sharp target is a lower bound on entry over the whole regime II equilibrium set at $r_1$, as a function of the shape of $G$. If it exceeds $g_{1/2}(r_0)$, the paper can drop the floor assumption and keep "competition creates competition" as a statement about every equilibrium.
