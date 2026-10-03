---
title: "Selection design in the endogenous-insider fork"
subtitle: "Can the seller or a policy remove the dead equilibrium?"
date: "2026-10-03"
---

This note extends `fork/endogenous_insider/mechanism.md` (the fork). It uses the fork's notation, its equation numbers (F.1) to (F.5), and the equation numbers of `paper/main.md`. Results S.1 to S.9 are new. Each result carries its status in the paper's vocabulary: analytical, computer-assisted, numerical diagnostic, or open. The code is `selection_solve.py`; it writes the CSV files in this folder and nothing else.

## 1. Question

In the fork the dead profile $\mathcal D$ (no trade, constant price $t_0$, no preparation) is an equilibrium at every strength, because $B_r(\tfrac12)<c$ everywhere on the benchmark domain (Proposition F.1(i)). On a middle range of strengths it coexists with live equilibria, in which the investor trades, the price is informative, and the challenger sometimes prepares. The question is whether the seller (the target board) or a policy maker can remove $\mathcal D$ and leave only live equilibria. The main device is a preparation subsidy $s\ge0$, paid to the challenger only when it prepares, such as expense reimbursement or a go-shop term. I also compare a price-contingent backstop, a subsidy lottery, a reserve price, and two forms of disclosure.

## 2. Headline result

A uniform subsidy removes $\mathcal D$ exactly when $s\ge s_D(r)=c-B_r(\tfrac12)$, and then the investor is an insider in every equilibrium. But the seller pays it on the equilibrium path, it does not select the unsubsidized live equilibrium, and for $s\ge c-B_r(m)$ entry becomes certain and the price no longer steers it. At the benchmark $s_D(r)$ exceeds the seller's largest gain per entry, $t_L-t_0+M\Delta_T$, at every $r\in(\ell,h)$, so any subsidy that removes $\mathcal D$ leaves the seller below even $\mathcal D$ (at $r=3$: $0.024$, against $0.417$ in $\mathcal D$ and $0.760$ live). A backstop that pays $\bar s\ge s_D$ only for preparation at the quiet price $t_0$ removes $\mathcal D$ at zero cost, because the quiet price carries the prior in $\mathcal D$ but bad news in a live equilibrium, so nobody ever claims it. [Referee fix: this needs a live equilibrium whose pool posterior lies below $\tau_{\bar s}$; where none exists, for example below $\mathfrak r(k)$ or above $r_C$, the backstop leaves no equilibrium at all (Proposition S.5(vi)).] A reserve cannot remove $\mathcal D$, and disclosure of order flow only shrinks the pool to its minimum.

## 3. Model changes

Everything is as in the fork (Sections 2 and 3 of `mechanism.md`), with one addition.

**Transfer schedule.** Before trading, the seller commits to a measurable schedule $s(\pi)$. The challenger receives $s(\pi)$ if it prepares at price $\pi$. A negative value is a fee. The challenger prepares at price $\pi$ if and only if $B_r(\mu_P(\pi))\ge c-s(\pi)$ (tie rule kept). An equilibrium is the fork's tuple $(\sigma_H,\sigma_L;P;\mu_P;e)$ with this preparation rule.

**Funding.** With $\kappa=1$ the seller pays the transfer, so on preparation at price $\pi$ the target's terminal value is $t_\theta-\kappa s(\pi)$; on no preparation it is $t_0$. With $\kappa=0$ a third party pays. The seller's expected net proceeds are $\mathsf N=\mathcal R_T-\mathbb E[\text{transfer paid}]$, with $\mathcal R_T=t_0+\tfrac12\sum_\theta e_\theta(t_\theta-t_0)$ as in (A.44).

**Three designs.**

1. Uniform subsidy: $s(\pi)\equiv s$.
2. Backstop: $s(\pi)=\bar s$ for $\pi\in I_\varepsilon:=(t_0-\varepsilon,t_0+\varepsilon)$ and $s(\pi)=s_0$ otherwise. The pure backstop has $s_0=0$.
3. Lottery: with probability $\rho$, drawn independently of $(\theta,R,Z)$ and revealed to the challenger after the price, the challenger receives $s_\ell$ on preparation; otherwise it receives nothing.

**Notation.** For a uniform subsidy,

$$
\tau_s=\frac{c-s-g_L}{g_H-g_L},\qquad
s_M=c-B_r(M),\quad s_D=c-B_r(\tfrac12),\quad s_m=c-B_r(m),
\tag{S.1}
$$

so $s_M<s_D<s_m$, $\tau_s$ falls in $s$, and $\tau_{s_M}=M$, $\tau_{s_D}=\tfrac12$, $\tau_{s_m}=m$. Under full orders, $x^*_s=\tfrac b2\log\frac{\tau_s}{1-\tau_s}$ is the flow at which $\mu_X$ reaches $\tau_s$, and $\bar\mu_{x}=F_Z(x-1)/[F_Z(x-1)+F_Z(x+1)]$ is the pool posterior of the pool $\{X<x\}$, as in (F.2). Write $w_L=t_L-t_0$ and $J(x)$ for the statistic (F.3) with lower limit $x$. The separation condition is

$$
\kappa s\notin[\,w_L+m\Delta_T,\;w_L+M\Delta_T\,].
\tag{S}
$$

## 4. Results

### 4.1 Structure under a transfer

**Lemma S.1 (structure under a uniform subsidy; analytical).** *Assume (S). In every equilibrium:*

*(a) $P=t_0$ on $N$ and $P=t_L-\kappa s+\Delta_T\mu_X$ on $A$.*

*(b) No price on $A$ equals $t_0$. The pool $N$ is the preimage of $t_0$, $\mu_P=\mu_X$ on $A$, and $\mu_P(t_0)=\bar\mu_N$.*

*(c) $A\subseteq\{\mu_X\ge\tau_s\}$, and if $\Pr(X\in N)>0$ then $\bar\mu_N<\tau_s$.*

*(d) The residuals are $A_H=\mathbf 1_A\Delta_T(1-\mu_X)$ and $A_L=\mathbf 1_A\Delta_T\mu_X$. They do not depend on $s$ or $\kappa$.*

*Proof.* On $N$ nobody prepares, so $V_T=t_0$ in both states and the competitive price is $t_0$. On $A$, $\mathbb E[V_T\mid x]=t_L-\kappa s+\Delta_T\mu_X(x)$. This equals $t_0$ if and only if $\mu_X(x)=(\kappa s-w_L)/\Delta_T$. Proposition A.1 puts $\mu_X$ in $[m,M]$, and (S) puts $(\kappa s-w_L)/\Delta_T$ outside $[m,M]$, so no flow in $A$ has price $t_0$. The map $\mu\mapsto t_L-\kappa s+\Delta_T\mu$ is injective, so on $A$ the price partition is the $\mu_X$ partition and $\mu_P=\mu_X$ there by the tower property. The preimage of $t_0$ is $N$, so the belief at $t_0$ is $\bar\mu_N$. Part (c) is the preparation rule at cost $c-s$ with the tie rule. For (d), $\mathbb E[V_T\mid\theta,x]=t_0+\mathbf 1_A(x)(t_\theta-\kappa s-t_0)$; subtract the price, and the terms $t_0$, $w_L$ and $\kappa s$ cancel. $\square$

*Remark.* If (S) fails, entry flows with $\mu_X=(\kappa s-w_L)/\Delta_T$ also reach the price $t_0$. This matters only if that level set has positive probability inside $A$. Under pure orders $q_H>q_L$ the level sets of $\mu_X$ are single points except the two plateaus, so a failure needs the knife edge $\kappa s=w_L+M_q\Delta_T$. Condition (S) always holds for $\kappa=0$. At the benchmark it holds for $\kappa=1$ and every $s\ge s_D$ at every $r$, by Proposition S.3(b).

[Referee fix: for $\kappa=1$ and $s<s_D$, (S) can fail on a whole interval of $s$, not only at a knife edge. At $r=3$ it fails for $s\in[0.638,0.946]$, which includes the rows $c=5.202$ and $c=5.222$ of Table 4 and the crossing $s\approx0.936$ of Table 2. Under full orders this is harmless off the knife edge. The critical flow is a single point; for $s<0.860$ it already lies in the pool, and for $s\in[0.860,0.946)$ it moves from $A$ to $N$, a null set. The minimal-pool rows stay equilibria up to a null set. At the knife edge $s=w_L+M\Delta_T=0.9457$ the plateau $x\ge1$ has price $t_0$; the belief at $t_0$ is then $0.481<\tau_s=0.592$, so the challenger does not prepare there, and the minimal-pool profile is not an equilibrium at that one value of $s$.]

**Lemma S.2 (closed form for $J$; analytical).** *Under full orders and entry set $[x,\infty)$ with $x\in[-1,1]$,*

$$
J(x)=\Delta_T\Big[\frac m2+\frac{e^{-1/b}}4\big(\operatorname{gd}(1/b)-\operatorname{gd}(x/b)\big)\Big],
\qquad \operatorname{gd}(u)=2\arctan\big(\tanh\tfrac u2\big).
\tag{S.2}
$$

*In particular $J(x)\ge\Delta_T m/2$ for every $x\le1$.*

*Proof.* Let $g(y)=f(y-1)f(y+1)/[f(y-1)+f(y+1)]$. On $y\ge1$, $f(y+1)/f(y-1)=e^{-2/b}$, so $g=m\,f(y-1)$, and $\int_1^\infty f(y-1)\,dy=\tfrac12$. On $|y|<1$, $f(y-1)f(y+1)=e^{-2/b}/(4b^2)$ and $f(y-1)+f(y+1)=e^{-1/b}\cosh(y/b)/b$, so $g(y)=e^{-1/b}/(4b\cosh(y/b))$. The antiderivative of $1/\cosh(y/b)$ is $b\operatorname{gd}(y/b)$. Add the two pieces. $\square$

*Consequence for the fork.* At $r_1=3$, $J(3)\ge\Delta_T(3)\,m/2=m/3>1/12$, because $m=1/(1+e)>1/4$. So $(1-1/b)J(3)>1/24>1/50=k$. The existence test of Proposition F.3(ii) therefore holds by hand, and open item 1 of `mechanism.md` closes: F.3 holds at the benchmark vector as an analytical result. The closed form gives $J(3)=0.095503$, which matches the fork's quadrature. More generally, the test $k<(1-1/b)J(x^*_s)$ holds for every $\tau_s\in(m,M]$ once $k<(1-1/b)m\Delta_T/2$, that is, once $r>\mathfrak r\big(2k/((1-1/b)m)\big)=2.1241$ at the benchmark.

### 4.2 The equilibrium set under a uniform subsidy

**Proposition S.1 (equilibrium set as a function of $s$; analytical).** *Fix $r\in(\ell,h)$ and $s$, and assume (S).*

*(i) $\mathcal D$ is an equilibrium if and only if $s<s_D$.*

*(ii) Every equilibrium without preparation is $\mathcal D$. Hence for $s\ge s_D$ every equilibrium has $\Pr(X\in A)>0$, and $V_T$ depends on $\theta$ on a set of positive probability: the investor is an insider in every equilibrium.*

*(iii) Case $\tau_s>M$ ($s<s_M$): $\mathcal D$ is the unique equilibrium.*

*(iv) Case $\tau_s\in(\tfrac12,M]$ ($s_M\le s<s_D$): Propositions F.1 and F.2 hold with $\tau_s$ in place of $\tau$. $\mathcal D$ coexists with the cutoff family. Full orders with entry set $[x^*_s,\infty)$ form an equilibrium if $k<(1-1/b)J(x^*_s)$.*

*(v) Case $\tau_s\in(m,\tfrac12]$ ($s_D\le s<s_m$):*

*(a) Let $\mathcal C$ be the profile with zero orders, preparation at the single price, and price $t_L-\kappa s+\Delta_T/2$. $\mathcal C$ is an equilibrium if and only if $\Delta_T\le2k$. It is the only equilibrium with $\sigma_H=\sigma_L$. If $\Delta_T<k$, it is the unique equilibrium.*

*(b) If $\Delta_T>2k$, the price is informative in every equilibrium: $\mu_P\ne\tfrac12$ on a set of positive probability.*

*(c) If $k<(1-1/b)m\Delta_T$, every equilibrium has a pool of positive probability, so preparation responds to the price.*

*(d) Under full orders, the entry set $[x',\infty)$ with the price of Lemma S.1 satisfies the challenger and the market maker if and only if $x'\in[x^*_s,\bar x_s)$. Here $x^*_s\in(-1,0]$, and $\bar x_s$ solves $\bar\mu_{\bar x_s}=\tau_s$, with $\bar x_s=\infty$ when $\tau_s=\tfrac12$. The interval shrinks as $s$ rises, and $\bar x_s\to-1$ as $s\to s_m$. [Referee fix: both ends fall as $s$ rises, so the intervals are not nested. The proof shows only that $\bar x_s$ falls. That the length $\bar x_s-x^*_s$ falls is a numerical diagnostic: it holds on a grid of 400 values of $\tau_s$ in $(m,\tfrac12)$ at $b=2$.] The minimal member $x'=x^*_s$ is an equilibrium if $k<(1-1/b)J(x^*_s)$.*

*(vi) Case $\tau_s\le m$ ($s\ge s_m$): the challenger prepares at every price in every equilibrium. The equilibrium set is that of the paper's model with $\rho=1$. Zero orders are the unique outcome if $\Delta_T<k$. Full orders are the unique outcome if $k<(1-1/b)m\Delta_T$. Zero orders form an equilibrium if and only if $\Delta_T\le2k$. The price has no effect on preparation, and $\theta$ is material at every flow.*

*Proof.* (i) Under $\mathcal D$, $V_T\equiv t_0=P$, so an order $q$ earns $-k|q|$ and zero is the unique best response. Then $X=Z$, there is one price, and the belief is $\tfrac12$. No preparation is optimal if and only if $B_r(\tfrac12)<c-s$, that is, $s<s_D$. At equality the tie rule forces preparation.

(ii) Without preparation, $V_T\equiv t_0$, so $P\equiv t_0$, zero orders are uniquely optimal, the only belief is $\tfrac12$, and consistency needs $s<s_D$. This is $\mathcal D$. For $s\ge s_D$ part (i) excludes $\mathcal D$, so $\Pr(X\in A)>0$, and on $A$ the value $t_\theta-\kappa s$ differs across states by $\Delta_T>0$.

(iii) Proposition A.1 gives $\mu_P\le M$ at every price. If $s<s_M$, then $B_r(\mu_P)\le B_r(M)<c-s$, nobody prepares, and (ii) gives $\mathcal D$. $\mathcal D$ exists because $s<s_M<s_D$.

(iv) Lemma S.1 reproduces Lemma F.1 with $\tau_s$. The proofs of F.1 and F.2 use $\tau$ only through Lemma F.1 and through $\tau>\tfrac12$ in the pool test, and here $\tau_s>\tfrac12$.

(v)(a) Suppose $\sigma_H=\sigma_L$. Then $a_H=a_L$ and $\mu_X\equiv\tfrac12$. Every price posterior is $\tfrac12\ge\tau_s$, so the challenger prepares at every price, and Lemma S.1(d) gives $A_H=A_L=\Delta_T/2$ at every flow. A correctly signed order of size $q>0$ earns $q(\Delta_T/2-k)$, and a wrong-signed order earns $-q(\Delta_T/2+k)<0$. If $\Delta_T>2k$, the high type's unique best response is $+1$ and the low type's is $-1$, which contradicts $\sigma_H=\sigma_L$. If $\Delta_T\le2k$, zero is optimal for both types; equal strategies must then have support in $[0,1]\cap[-1,0]=\{0\}$, which is $\mathcal C$. Conversely, under $\mathcal C$ the same computation shows that zero orders are optimal if and only if $\Delta_T\le2k$. The price $t_0+w_L-\kappa s+\Delta_T/2$ is competitive, and preparation is optimal at belief $\tfrac12$. If $\Delta_T<k$, Lemma S.1(d) bounds every residual by $\Delta_T$ against every candidate schedule, so every nonzero order loses as in the proof of F.1(iv). Then $\sigma_H=\sigma_L=\delta_0$ and the outcome is $\mathcal C$.

(v)(b) Suppose $\mu_P=\tfrac12$ almost surely. If $\Pr(X\in N)>0$, then $\bar\mu_N=\tfrac12\ge\tau_s$, which contradicts Lemma S.1(c). So $\Pr(X\in N)=0$, and Lemma S.1(b) gives $\mu_X=\mu_P=\tfrac12$ almost surely. Then $a_H=a_L$ almost everywhere. The Laplace characteristic function $1/(1+b^2t^2)$ never vanishes, so convolution with $f$ is injective on probability measures, and $\sigma_H=\sigma_L$. Part (a) with $\Delta_T>2k$ excludes this.

(v)(c) Suppose $\Pr(X\in N)=0$. Then $A$ has full probability, and Lemma S.1(d) with Proposition A.1 gives $A_\theta\ge m\Delta_T$ almost everywhere. The bound (A.6) with $\rho=1$ gives $U_\theta'(q)\ge(1-1/b)m\Delta_T-k>0$ on $[0,1]$, and wrong-signed orders have negative gross payoff, so both types play full orders. Under full orders $\mu_X=m<\tau_s$ on $x\le-1$, a set of positive probability. The price reveals $\mu_X$ on $A$ by Lemma S.1(b), so at those prices the challenger's belief is $m$ and it does not prepare. Those flows lie in $N$, a contradiction.

(v)(d) On $[x',\infty)$ with $x'\ge x^*_s$, $\mu_X\ge\tau_s$ because $\mu_X$ is nondecreasing, and the price reveals $\mu_X$, so preparation is optimal. If $x'<x^*_s$, flows in $[x',x^*_s)$ have revealed posterior below $\tau_s$, and the challenger would not prepare there. On the pool, (F.2) gives the posterior $\bar\mu_{x'}$. This function equals $m$ for $x'\le-1$, is continuous, is strictly increasing on $(-1,\infty)$ by the monotone likelihood ratio, and tends to $\tfrac12$ as $x'\to\infty$. Pool consistency $\bar\mu_{x'}<\tau_s$ therefore holds exactly on $x'<\bar x_s$. At $x'=x^*_s$, $\mu_X<\tau_s$ at every pooled flow, so $\bar\mu_{x^*_s}<\tau_s$ and $x^*_s<\bar x_s$. Since $\tau_s\in(m,\tfrac12]$ and $\operatorname{logit}(m)=-2/b$, $x^*_s\in(-1,0]$. As $s$ rises, $\tau_s$ falls, so $\bar x_s$ falls, and $\bar x_s\to-1$ as $\tau_s\downarrow m$. Competitive pricing is Lemma S.1(a). Investor optimality at $x'=x^*_s$ is the proof of F.2(c) with $J(x^*_s)$ from Lemma S.2.

(vi) Proposition A.1 bounds every price posterior below by $m$, including the posterior at a price atom, which is a conditional expectation of $\mu_X$. So $B_r(\mu_P)\ge B_r(m)\ge c-s$ at every price, and the challenger prepares everywhere (tie rule at equality). Then $A=\mathbb R$, the price $t_L-\kappa s+\Delta_T\mu_X$ is strictly increasing in $\mu_X$, and the residuals are (11) with $\rho=1$. Step 3 and Step 4 of the proof of Proposition 2, and (A.12), apply with $\rho=1$. $\square$

So the answer to the first question is yes: $\mathcal D$ disappears exactly at $s=s_D$. Three things replace it. At a weak incumbent ($\Delta_T\le2k$) the replacement is $\mathcal C$: the investor is an insider but does not trade, and the price is constant. [Referee fix: $\mathcal C$ is an equilibrium when $\Delta_T\le2k$, but the note proves that it is the unique one only when $\Delta_T<k$.] At a strong incumbent the replacement is a live family with a pool. Pools survive below $\tau_s=\tfrac12$ because the pool belief $\bar\mu_N$ can sit below $\tau_s$; under full orders this happens exactly when $\tau_s>m$. At $s\ge s_m$ the pool vanishes, entry is certain, and the feedback channel closes.

**Proposition S.2 (the minimal-pool selection as $s$ rises; analytical).** *Fix full orders and the minimal pool, and let $s$ rise on $[s_M,s_m)$.*

*(a) $x^*_s$ falls strictly; $e_H=S_Z(x^*_s-1)$ and $e_L=S_Z(x^*_s+1)$ rise strictly; and the price experiment becomes strictly more informative in the Blackwell sense.*

*(b) At $s=s_D$, $\mathsf E=\tfrac12$ exactly. More generally, at $s=s_D$ every pure profile $q_H>q_L$ with its minimal pool has $\mathsf E=\tfrac12$.*

*(c) At $s=s_m$, $\mathsf E$ jumps from $(3-e^{-2/b})/4$ to $1$, and preparation no longer responds to the price.*

*Proof.* (a) $x^*_s=\tfrac b2\operatorname{logit}(\tau_s)$ and $\tau_s$ falls in $s$; the tail probabilities fall in $x^*$. For $s<s'$ the price at $s'$ reveals $\mu_X$ on $[x^*_{s'},\infty)\supset[x^*_s,\infty)$ and pools the rest, so its partition of the flow line refines the partition at $s$. The experiment at $s$ is a garbling of the one at $s'$. The two are not equivalent: on $[x^*_{s'},x^*_s)$ the posterior is strictly increasing and the set has positive probability in both states, so the distribution of posteriors at $s'$ is a strict mean-preserving spread of the one at $s$.

(b) Under pure orders $q_H>q_L$, $\mu_X(x)\ge\tfrac12$ if and only if $|x-q_H|\le|x-q_L|$, that is, $x\ge x_0:=(q_H+q_L)/2$. With $\delta=(q_H-q_L)/2$, $e_H=S_Z(-\delta)$ and $e_L=S_Z(\delta)$, and $S_Z(-\delta)+S_Z(\delta)=1$ by symmetry of the noise.

(c) At $\tau_s=m$ the tie rule admits preparation on the plateau $x\le-1$, so $A=\mathbb R$. Just above $m$, $x^*_s\downarrow-1$ and $\mathsf E\to\tfrac12[S_Z(-2)+S_Z(0)]=(3-e^{-2/b})/4$. $\square$

### 4.3 Who pays for the subsidy

**Proposition S.3 (seller's accounting; analytical).** *Let the seller fund the subsidy ($\kappa=1$).*

*(a) In every equilibrium the seller's expected net proceeds equal the mean price:*

$$
\mathsf N=\mathbb E[P(X)]=t_0+\Pr(X\in A)\,\big[w_L+\Delta_T\Pr(H\mid X\in A)-s\big].
\tag{S.3}
$$

*(b) $\mathsf N<t_0$ in every equilibrium with preparation whenever $s>w_L+M\Delta_T$. At the benchmark $(h,\ell,p,b,c)=(10,1,\tfrac12,2,6)$, $s_D(r)>w_L(r)+M\Delta_T(r)$ at every $r\in(\ell,h)$. So every uniform subsidy that removes $\mathcal D$ gives the seller strictly less than $t_0$ in every equilibrium. This is worse than $\mathcal D$, and worse than every unsubsidized live equilibrium.*

*(c) Under $\mathcal C$ at $s=s_D$, $\mathsf N=(h+\ell)/2-c$ at every $r$. At the benchmark this is $-\tfrac12$.*

*Proof.* (a) Competitive pricing gives $\mathbb E[P]=\mathbb E[V_T]$. With $\kappa=1$, $V_T$ is the seller's net receipt per share: $t_0$ on $N$ and $t_\theta-s$ on $A$. So $\mathbb E[V_T]=t_0+\mathbb E[\mathbf 1_A(t_\theta-t_0-s)]$; condition on $A$ and use $t_H-t_0=w_L+\Delta_T$.

(b) $\Pr(H\mid X\in A)=\mathbb E[\mu_X\mid X\in A]\le M$ by Proposition A.1, so the bracket in (S.3) is at most $w_L+M\Delta_T-s<0$. For $s\ge s_D$, Proposition S.1(ii) gives $\Pr(X\in A)>0$. For the benchmark inequality, (4) gives $s_D=c-\tfrac h2+\tfrac r4-\tfrac{\ell^2-2p^2}{4r}$, $w_L=\ell-p-\tfrac{\ell^2-3p^2}{2r}$, and $\Delta_T=\tfrac r2-\ell+\tfrac{\ell^2}{2r}$. Hence

$$
d(r):=s_D-w_L-M\Delta_T
=c-\frac h2+p-m\ell-\frac{(M-m)\,r}{4}-\frac{(M-m)\ell^2/4+p^2}{r}.
\tag{S.4}
$$

$d$ is strictly concave on $r>0$. At the benchmark, $d(1)=\tfrac34$ exactly, because the terms in $m$ cancel. Also $d(10)=4.05\,m-1.05>0$, because $m=1/(1+e)>1.05/4.05$ is equivalent to $e<2.857$. Concavity gives $d>0$ on $[1,10]$. An unsubsidized live equilibrium gives $t_0+\Pr(X\in A)[w_L+\Delta_T\Pr(H\mid A)]>t_0$, since $w_L>0$.

(c) Under $\mathcal C$, $A=\mathbb R$ and $\Pr(H\mid A)=\tfrac12$, so $\mathsf N=\tfrac12(t_H+t_L)-s_D=\tfrac12(t_H+g_H)+\tfrac12(t_L+g_L)-c$. Pointwise in $R$, the target's receipt plus the challenger's gross profit equals $\theta$: for $\theta=h$ because $R<h$; for $\theta=\ell$ case by case on $R<p$, $p\le R\le\ell$, $R>\ell$. So $t_\theta+g_\theta=\theta$. $\square$

Part (a) reads directly. Under seller funding, the price at an entry flow is the seller's net receipt there. A subsidized entry hurts the seller exactly where the stock trades below $t_0$ after the market prices that entry. Part (c) shows the size of the problem. At $s_D$ the challenger earns zero net at the prior. The seller's net receipt is then the expected challenger value $(h+\ell)/2$ minus the whole cost $c$, which is negative at the benchmark.

The surplus side points the same way.

**Proposition S.4 (surplus-maximizing subsidy; analytical).** *Hold full orders and the minimal pool, and let $\mathcal W(s)=\mathbb E[\mathbf 1_A(B_r(\mu_X)+p^2/r-c)]$ be acquisition surplus net of preparation cost, with transfers excluded as in (A.40). On $[s_M,s_m)$, $\mathcal W$ is maximized at $s=p^2/r$.* [Referee fix: this needs $s_M\le p^2/r$. If $s_M>p^2/r$, the proof shows that $\mathcal W$ falls on the whole window, and the maximum is at $s_M$. At the benchmark this happens for $r>3.7736$; for example at $r=4$, $s_M=0.149>p^2/r=0.0625$. The hypothesis holds at $r=3$.]

*Proof.* By (A.39) and (A.40), a preparation at belief $\mu$ adds $B_r(\mu)-c+p^2/r$ to surplus; the term $p^2/r$ is the sale that the challenger creates when the incumbent misses the reserve, and the challenger does not count it. With $A=\{\mu_X\ge\tau_s\}$ and $G$ the law of $\mu_X$, which has a density on $(m,M)$ under full orders, $d\mathcal W/d\tau_s=-[B_r(\tau_s)+p^2/r-c]\,G'(\tau_s)=-(p^2/r-s)\,G'(\tau_s)$, because $B_r(\tau_s)=c-s$. Since $\tau_s$ falls in $s$, $\mathcal W$ rises for $s<p^2/r$ and falls for $s>p^2/r$. $\square$

At $r=3$ the efficient subsidy is $p^2/r=1/12$, far below $s_D=41/24$. An efficient uniform subsidy does not remove $\mathcal D$.

### 4.4 A backstop at the quiet price

The dead and live equilibria share the price $t_0$ but not the belief at that price. In $\mathcal D$ the quiet price carries the prior, $\tfrac12$. In a live equilibrium it carries the pool posterior $\bar\mu_N<\tfrac12$, which is bad news, because the low-value investor's sales push flow into the pool. A transfer offered only at the quiet price can separate the two.

**Proposition S.5 (backstop; analytical).** *Let $s(\pi)=\bar s$ on $I_\varepsilon$ and $s(\pi)=s_0$ elsewhere, with $s_0<s_D\le\bar s$. Assume $\varepsilon>0$ and*

$$
\varepsilon\le w_L-\kappa s_0+m\Delta_T,
\qquad
\text{and, if }\kappa=1,\quad \bar s\ge w_L+M\Delta_T+\varepsilon .
\tag{B}
$$

*(i) No equilibrium has preparation at a price in $I_\varepsilon$ with positive probability. The backstop is paid with probability zero.*

*(ii) The equilibria are exactly the equilibria of the uniform-$s_0$ economy whose pool satisfies $\bar\mu_N<\tau_{\bar s}$.*

*(iii) $\mathcal D$ is an equilibrium if and only if $\bar s<s_D$.*

*(iv) Let $s_0\ge s_M$, and let $\bar\mu^*$ be the pool posterior of the minimal-pool full-order equilibrium of the uniform-$s_0$ economy. If $\bar s<c-B_r(\bar\mu^*)$ and $k<(1-1/b)J(x^*_{s_0})$, that equilibrium survives. Then the equilibrium set is nonempty, and in every equilibrium the challenger prepares with positive probability, the price is informative, and the investor is an insider.*

*(v) Let $s_0\ge s_M$. In every full-order equilibrium the pool $N$ contains $N^*=\{X<x^*_{s_0}\}$, and*

$$
\Pr(X\in N\setminus N^*)\le\Pr(X\in N^*)\,\frac{\tau_{\bar s}-\bar\mu^*}{\tau_{s_0}-\tau_{\bar s}},
\qquad
\mathsf N\ge\mathsf N^*-\Pr(X\in N\setminus N^*)\,(w_L-\kappa s_0+M\Delta_T),
$$

*where $\mathsf N^*$ is the seller's net proceeds in the minimal-pool equilibrium. As $\bar s\uparrow c-B_r(\bar\mu^*)$, full-order equilibria converge to the minimal pool.*

*(vi) If no equilibrium of the uniform-$s_0$ economy has $\bar\mu_N<\tau_{\bar s}$, no equilibrium exists. In particular, with $s_0=0$ and $\bar s\ge s_D$, no equilibrium exists when $r<\mathfrak r(k)$ or $r>r_C$.*

*Proof.* (i) and (ii). Suppose the challenger prepares at a price $\pi\in I_\varepsilon$ on a set of flows of positive probability. Competitive pricing at those flows gives $\pi=t_0+w_L-\kappa\bar s+\Delta_T\mu_X(x)$. For $\kappa=0$ this is at least $t_0+w_L+m\Delta_T\ge t_0+\varepsilon$. For $\kappa=1$ it is at most $t_0+w_L+M\Delta_T-\bar s\le t_0-\varepsilon$. Either way $\pi\notin I_\varepsilon$, a contradiction. So prices in $I_\varepsilon$ carry no preparation, $V_T=t_0$ there, and the price there is exactly $t_0$. At prices outside $I_\varepsilon$ the transfer is $s_0$, and a preparation price equals $t_0+w_L-\kappa s_0+\Delta_T\mu_X\ge t_0+\varepsilon$ by (B), so such a price indeed lies outside $I_\varepsilon$. So $N$ is the preimage of $t_0$, every preparation price lies outside $I_\varepsilon$, and (S) holds for $s_0$. Every equilibrium condition then coincides with the uniform-$s_0$ economy except one: at the price $t_0$ the challenger's cost is $c-\bar s$, so non-preparation there requires $B_r(\bar\mu_N)<c-\bar s$, that is, $\bar\mu_N<\tau_{\bar s}$. Since $\bar s>s_0$, this is stronger than the pool test of the uniform-$s_0$ economy. Every equilibrium has a pool of positive probability, because $\tau_{s_0}>\tfrac12=\mathbb E[\mu_X]$ rules out $A$ of full probability. Preparation in $I_\varepsilon$ has probability zero, so the backstop is never paid.

(iii) $\mathcal D$ is an equilibrium of the uniform-$s_0$ economy because $s_0<s_D$, and its pool is the whole line with $\bar\mu_N=\tfrac12$. By (ii) it survives if and only if $\tfrac12<\tau_{\bar s}$, that is, $\bar s<s_D$.

(iv) Under full orders $\mu_X<\tau_{s_0}$ on the minimal pool and $\bar\mu^*<\tfrac12$ by (F.2), so $c-B_r(\bar\mu^*)>s_D$ and the window is nonempty. The minimal-pool equilibrium exists by Proposition S.1(iv) and passes the test of (ii). The only equilibrium without preparation is $\mathcal D$ (Proposition S.1(ii)), which (iii) removes. If $\sigma_H=\sigma_L$, then $\mu_X\equiv\tfrac12<\tau_{s_0}$, nobody prepares, and the profile is $\mathcal D$; so orders differ across states. On $A$, which has positive probability, the price reveals $\mu_X\ge\tau_{s_0}>\tfrac12$, while $\mathbb E[\mu_P]=\tfrac12$; so the price is informative. On $A$, $V_T$ depends on $\theta$.

(v) Under full orders Lemma S.1(c) gives $A\subseteq[x^*_{s_0},\infty)$, so $N\supseteq N^*$. On $N\setminus N^*$, $\mu_X\ge\tau_{s_0}$. Hence $\bar\mu_N\ge[\Pr(N^*)\bar\mu^*+\tau_{s_0}\Pr(N\setminus N^*)]/[\Pr(N^*)+\Pr(N\setminus N^*)]$, and $\bar\mu_N<\tau_{\bar s}$ gives the first bound, since $\tau_{s_0}>\tfrac12\ge\tau_{\bar s}$. For proceeds, $\mathsf N=t_0+\mathbb E[\mathbf 1_A(w_L-\kappa s_0+\Delta_T\mu_X)]$, and $A=A^*\setminus(N\setminus N^*)$, where the integrand is at most $w_L-\kappa s_0+M\Delta_T$. As $\tau_{\bar s}\downarrow\bar\mu^*$, the first bound tends to zero.

(vi) This follows from (ii). With $s_0=0$, the fork has only $\mathcal D$ below $\mathfrak r(k)$ and above $r_C$ (Proposition F.1(iii) and (iv)), and (iii) removes it. $\square$

At the benchmark (B) is mild. At $r=3$ with $\kappa=1$ and $s_0=0$, any $\varepsilon\le\min\{w_L+m\Delta_T,\ \bar s-w_L-M\Delta_T\}$ works, and at $\bar s=s_D$ this minimum is $0.638$. The band need not be a knife edge.

**Corollary S.6 (competition creates the insider in every equilibrium; analytical).** *Take the benchmark vector with $(r_0,r_1)=(1.2,3)$. At $r_0$, $\mathcal D$ is the unique equilibrium (Proposition F.1(iv)), and no backstop with $\bar s\ge s_D(r_0)$ leaves an equilibrium.* [Referee fix: "no backstop" means no pure backstop that satisfies (B); the proof uses S.5(vi), which assumes (B).] *At $r_1$, the pure backstop with $\bar s=s_D(r_1)=41/24$ leaves a nonempty equilibrium set, and in every equilibrium the investor is an insider, the price is informative, and the challenger prepares with positive probability.*

*Proof.* At $r_0$: Proposition F.1(iv) and S.5(vi). At $r_1$: Lemma S.2 gives $k<(1-1/b)J(x^*)$; $\bar\mu^*<\tfrac12=\tau_{\bar s}$; (B) holds with any $\varepsilon\le0.638$; apply S.5(iv). $\square$

This restores the strong form of the paper's comparison. Without a device, the fork says that competition *permits* an insider. With the backstop, a stronger incumbent moves the economy from "bystander in every equilibrium" to "insider in every equilibrium". [Referee fix: the paper compares two strengths under one institution. Here the device is not the same at both strengths. At $r_0$ the same backstop leaves no equilibrium, so the comparison holds only for the rule "post the backstop where a live equilibrium exists", which conditions on the public strength $r$. At $r_0$ the statement "bystander in every equilibrium" refers to the economy without the backstop.] The backstop costs nothing on path. It needs commitment, because in $\mathcal D$ the seller would want to withdraw it ex post: at $r=3$ a claimed backstop costs $1.708$ and brings $w_L+\Delta_T/2=0.792$. The construction is a price-contingent rule in the sense of the market-based corrective action literature, and it shares that literature's existence problem: (vi) shows the seller must not post it where the fork has no live equilibrium.

### 4.5 A subsidy lottery recreates the floor

**Proposition S.7 (lottery; analytical).** *Assume $B_r(\tfrac12)<c$.*

*(a) If $s_\ell\ge s_D$, $\mathcal D$ is not an equilibrium. Every equilibrium with an uninformative price is the no-trade profile with preparation probability $\rho$, and that profile is an equilibrium if and only if $\rho\Delta_T\le2k$.*

*(b) If $s_\ell>s_m$, the economy is the paper's model with $c_L=c-s_\ell<B_r(m)$ and $c_H=c$. No pool forms. The no-trade profile is an equilibrium if and only if $r\le r_N(\rho)=\mathfrak r(2k/\rho)$; full orders are the unique trading outcome if $k<(1-1/b)\rho m\Delta_T$. The seller's expected outlay is $\rho s_\ell$.*

*Proof.* (a) Under zero orders the single price has posterior $\tfrac12$, and the subsidized challenger prepares because $B_r(\tfrac12)\ge c-s_\ell$. So preparation has probability $\rho>0$ and $\mathcal D$ fails. Suppose $\mu_P=\tfrac12$ almost surely. Then at every price the subsidized challenger prepares and the other does not, so preparation is $\rho$ at every flow. The price $t_0+\rho(w_L-\kappa s_\ell+\Delta_T\mu_X)$ then reveals $\mu_X$, so $\mu_X=\tfrac12$ almost surely and $\sigma_H=\sigma_L$ by injectivity of the Laplace convolution. The residual is $\rho\Delta_T/2$ at every flow, and the argument of Proposition S.1(v)(a) gives zero orders with $\rho\Delta_T\le2k$. The converse is (A.12). (b) The subsidized type prepares at every price, so Propositions A.2 and A.4 and the proof of Proposition 2 apply verbatim. The subsidized type prepares with probability one, so the outlay is $\rho s_\ell$. $\square$

The lottery acts on the investor, not on the challenger. A uniform subsidy must make the challenger prepare at the prior. The lottery needs only $\rho>2k/\Delta_T$, enough to make an informed order pay against the no-trade schedule. This is the paper's floor (A1) read as a design: Proposition F.5 calls the floor a selection device, and the lottery shows its price. At $r=3$, $\rho_N=2k/\Delta_T=0.06$ and $\rho_U=k/((1-1/b)m\Delta_T)=0.223$.

### 4.6 Reserve price and disclosure

**Proposition S.8 (a reserve cannot remove $\mathcal D$; analytical).** *For every reserve $p'\in[0,h]$ and every belief $\mu$, $B_{p',r}(\mu)\le B_{0,r}(\mu)$, and $B_{0,r}(\tfrac12)=\tfrac12[h-r/2+\ell^2/(2r)]$ is strictly decreasing on $r>\ell$ with limit $h/2$ at $r=\ell$. Hence if $c\ge h/2$, $\mathcal D$ is an equilibrium after every reserve at every $r\in(\ell,h)$. At the benchmark $c=6>5=h/2$.*

*Proof.* By (A.42), $g_v(p',r)=\mathbb E[(v-\max\{p',R\})_+]$, which is nonincreasing in $p'$ pointwise in $R$. $B_{p',r}$ is a convex combination of $g_h$ and $g_\ell$. After any reserve, $\mathcal D$ has $V_T\equiv t_0(p',r)=P$, and the proof of F.1(i) gives existence if and only if $B_{p',r}(\tfrac12)<c$. At $p'=0$, $g_h=h-r/2$ and $g_\ell=\ell^2/(2r)$; the derivative of $B_{0,r}(\tfrac12)$ in $r$ is $-\tfrac14-\ell^2/(4r^2)<0$. $\square$

A reserve moves $\tau$ and $\Delta_T$, so it moves the pool, but it cannot select. A higher reserve lowers $B$ at every belief, so it raises $\tau$ and enlarges the minimal pool; above $p'=1.5$ at $r=3$ it pushes $\tau$ above $M$ and leaves $\mathcal D$ unique (Table 7). [Referee fix: the crossing $\tau=M$ is at $p'=1.3253$, between the rows $1.2$ and $1.5$ of Table 7; "above $1.5$" is true but not sharp.] Proposition A.10 already shows that pools at fixed orders arise in the reserve game itself; in the fork the same continuation correspondence applies at every reserve.

**Proposition S.9 (flow disclosure shrinks the pool but keeps $\mathcal D$; analytical).** *Suppose the order flow $X$ is published before the challenger decides. Then in every equilibrium $A=\{\mu_X\ge\tau\}$ up to a null set, so at each order profile only the minimal pool survives. $\mathcal D$ is an equilibrium if and only if $B_r(\tfrac12)<c$.*

*Proof.* The price is a function of $X$, so the challenger's belief at flow $x$ is $\mu_X(x)$, and its rule is $e(x)=\mathbf 1\{\mu_X(x)\ge\tau\}$. The market maker sets $P=t_0+e(x)(w_L+\Delta_T\mu_X)$. Under zero orders $X=Z$ carries no information, $\mu_X\equiv\tfrac12<\tau$, nobody prepares, and the proof of F.1(i) applies. $\square$

*Remark (public signal).* Suppose the seller held a public signal $Y$ about $\theta$ with accuracy $d$ and released it before trading. After $Y$ the continuation is the fork with prior $d$ or $1-d$. After bad news $\mathcal D$ survives, since $B_r(1-d)<B_r(\tfrac12)<c$. After good news it disappears only if $d\ge\tau$. Full disclosure makes $\theta$ public: the challenger prepares exactly when $\theta=h$, and the seller earns $t_0+\tfrac12(t_H-t_0)=0.979$ at $r=3$. But then nobody holds private information, so nobody is an insider. Disclosure replaces the insider; it does not select the live equilibrium, and in the model the seller has no such signal.

## 5. Numerics

All closed-form rows evaluate the formulas above in double precision; their status is the status of the formula. Grid rows come from best-response iteration on the fork's grid (60,001 flow points on $[-30,30]$, order grid of step $0.01$ refined to $0.0005$, six starts including zero orders); their status is numerical diagnostic, and the search covers pure profiles and interval pools only. Benchmark: $(h,\ell,p,b,k,c)=(10,1,0.5,2,0.02,6)$, seller funding $\kappa=1$. Sources: `key_numbers.csv`, `subsidy_sweep_r3.csv`, `across_strengths.csv`, `cost_sweep_r3.csv`, `breakeven_r3.csv`, `backstop_family_r3.csv`, `backstop_window_r3.csv`, `lottery_r3.csv`, `reserve_r3.csv`.

**Table 1. Thresholds at $r_1=3$.**

| Object | Value | Status |
|---|---|---|
| $s_M=c-B_3(M)$ (negative: a fee) | $-0.2172$ | analytical |
| $s_D=c-B_3(\tfrac12)$ | $41/24=1.7083$ | analytical |
| $s_m=c-B_3(m)$ | $3.6338$ | analytical |
| $w_L+M\Delta_T$, the largest seller gain per entry | $0.9457$ | analytical |
| $d(3)=s_D-w_L-M\Delta_T$ | $0.7626$ | analytical |
| $J(3)$ by (S.2); hand bound $\Delta_T m/2$ | $0.09550$; $0.08965$ | analytical |
| $\bar\mu^*$, minimal-pool posterior | $0.3684$ | analytical |
| backstop window $[s_D,\ c-B_3(\bar\mu^*))$ | $[1.7083,\ 2.8051)$ | analytical |
| efficient subsidy $p^2/r$ | $0.0833$ | analytical |
| lottery: $\rho_N=2k/\Delta_T$, $\rho_U=k/((1-1/b)m\Delta_T)$ | $0.060$, $0.223$ | analytical |
| $\mathfrak r(k)$, $\mathfrak r(2k)$, $r_C$ | $1.2210$, $1.3257$, $3.5927$ | analytical |
| smallest $r$ with $k<(1-1/b)J(x^*)$ at $s=0$; at $s=s_D$ | $2.0155$; $1.8434$ | closed-form $J$, numerical root [Referee fix: in the paper's vocabulary a root found in floating point without an enclosure is a numerical diagnostic; a 30-digit bisection agrees to 10 digits] |

**Table 2. Uniform subsidy at $r=3$, minimal-pool full-order equilibrium.** $\mathcal D$ yields $\mathsf N=t_0=0.417$ and $\mathcal W=0$ wherever it exists.

| $s$ | case | $\mathcal D$ exists | $\mathsf E$ | $e_H$ | $e_L$ | $\mathcal R_T$ | outlay $s\mathsf E$ | net $\mathsf N$ | $\mathcal W$ |
|---|---|---|---|---|---|---|---|---|---|
| $-0.217$ ($s_M$, fee) | $\tau_s=M$ | yes | 0.342 | 0.500 | 0.184 | 0.740 | $-0.074$ | 0.814 | 0.103 |
| $0$ | $(\tfrac12,M]$ | yes | 0.364 | 0.531 | 0.196 | 0.760 | 0 | 0.760 | 0.107 |
| $0.1$ | $(\tfrac12,M]$ | yes | 0.373 | 0.544 | 0.202 | 0.769 | 0.037 | 0.732 | 0.107 |
| $0.5$ | $(\tfrac12,M]$ | yes | 0.408 | 0.591 | 0.225 | 0.801 | 0.204 | 0.597 | 0.100 |
| $1.0$ | $(\tfrac12,M]$ | yes | 0.448 | 0.640 | 0.255 | 0.835 | 0.448 | 0.388 | 0.074 |
| $1.708$ ($s_D$) | $\tau_s=\tfrac12$ | no | 0.500 | 0.697 | 0.303 | 0.878 | 0.854 | 0.024 | 0.007 |
| $2.0$ | $(m,\tfrac12)$ | no | 0.521 | 0.717 | 0.325 | 0.895 | 1.043 | $-0.148$ | $-0.031$ |
| $3.0$ | $(m,\tfrac12)$ | no | 0.599 | 0.780 | 0.418 | 0.951 | 1.797 | $-0.846$ | $-0.219$ |
| $3.634^-$ | $\tau_s\downarrow m$ | no | 0.658 | 0.816 | 0.500 | 0.990 | 2.391 | $-1.401$ | $-0.411$ |
| $3.634$ ($s_m$) | $\tau_s=m$ | no | 1 | 1 | 1 | 1.208 | 3.634 | $-2.426$ | $-1.625$ |

Status: analytical rows (the existence test holds at every listed $s$; at $s\ge s_m$ full orders are unique). The grid search at every $s$ in the sweep returns the same full-order point, within $10^{-4}$ in $\mathsf E$, and returns $\mathcal D$ from the zero start exactly when $s<s_D$ (numerical diagnostic). The seller's net proceeds fall below $t_0$ near $s=0.93$, well before $s_D$.

**Table 3. Minimal subsidy that removes $\mathcal D$, across strengths.** Grid search at $s=s_D(r)$ from six starts.

| $r$ | $s_D$ | $d(r)$ | pure equilibria found at $s_D$ | $\mathsf E$ | net $\mathsf N$ | $t_0$ |
|---|---|---|---|---|---|---|
| 1.2 | 1.196 | 0.788 | $\mathcal C$: $(0,0)$ | 1 | $-0.500$ | 0.292 |
| 1.3 | 1.229 | 0.800 | $\mathcal C$: $(0,0)$ | 1 | $-0.500$ | 0.308 |
| 1.35 to 1.50 | | | none: the map cycles between $(0,0)$ and $(1,-1)$ | | | |
| 1.55 | 1.307 | 0.816 | $(1,-0.227)$ | 0.500 | $-0.074$ | 0.339 |
| 1.70 | 1.351 | 0.820 | $(1,-0.718)$ | 0.500 | $-0.061$ | 0.353 |
| 1.85 | 1.395 | 0.820 | $(1,-1)$ | 0.500 | $-0.048$ | 0.365 |
| 2.5 | 1.575 | 0.796 | $(1,-1)$ | 0.500 | $-0.006$ | 0.400 |
| 3.0 | 1.708 | 0.763 | $(1,-1)$ | 0.500 | 0.024 | 0.417 |
| 3.5 | 1.839 | 0.722 | $(1,-1)$ | 0.500 | 0.052 | 0.429 |
| 4.0 | 1.969 | 0.678 | $(1,-1)$ | 0.500 | 0.079 | 0.438 |
| 6.0 | 2.479 | 0.477 | $(1,-1)$ | 0.500 | 0.184 | 0.458 |
| 9.95 | 3.475 | 0.045 | $(1,-1)$ | 0.500 | 0.383 | 0.475 |

Status: $d(r)>0$ and $\mathsf N<t_0$ in every equilibrium are analytical (Proposition S.3). The $\mathcal C$ rows are analytical ($\Delta_T\le2k$ there). The other rows are numerical diagnostics; $\mathsf E=\tfrac12$ matches Proposition S.2(b). On $r\in[1.35,1.50]$ no pure equilibrium was found, and existence there is open. Above $r_C$ the subsidy creates entry that the fork never has, yet the seller still loses.

**Table 4. When does the minimal subsidy pay? Cost sweep at $r=3$.** Minimal-pool equilibria, closed forms.

| $c$ | $s_D$ | $\mathsf N$ at $s_D$ | live $\mathcal R_T$ at $s=0$ | gain over $\mathcal D$ | gain over live |
|---|---|---|---|---|---|
| 4.302 | 0.010 | 0.873 | 0.877 | $+0.456$ | $-0.004$ |
| 4.782 | 0.490 | 0.633 | 0.849 | $+0.216$ | $-0.216$ |
| 5.202 | 0.910 | 0.423 | 0.822 | $+0.006$ | $-0.399$ |
| 5.222 | 0.930 | 0.413 | 0.820 | $-0.004$ | $-0.407$ |
| 5.502 | 1.210 | 0.273 | 0.801 | $-0.144$ | $-0.528$ |
| 6.000 | 1.708 | 0.024 | 0.760 | $-0.393$ | $-0.737$ |
| 6.217 | 1.925 | $-0.085$ | 0.740 | $-0.501$ | $-0.825$ |

The minimal subsidy beats $\mathcal D$ exactly when $c<B_3(\tfrac12)+w_L+(1-\tfrac12e^{-1/b})\Delta_T=5.2145$ (analytical, from Proposition S.2(b) and (S.3)). It never beats the unsubsidized minimal-pool live equilibrium on the grid of $c$; the gap closes only as $c\downarrow B_3(\tfrac12)$ (numerical diagnostic). The benchmark $c=6$ lies far inside the region where the seller loses.

**Table 5. Backstop at $r=3$ ($s_0=0$).** The searched family is the fork's cutoff family, 48 members with lower ends $x'$ from $0.871$ to $3.221$, found by best-response iteration with the entry floor fixed (numerical diagnostic). A member survives when $\bar\mu_{x'}<\tau_{\bar s}$.

| $\bar s$ | $\tau_{\bar s}$ | members kept | largest kept $x'$ | worst $\mathcal R_T$ | best $\mathcal R_T$ | outlay |
|---|---|---|---|---|---|---|
| no backstop | — | 48, plus $\mathcal D$ | 3.221 | 0.417 ($\mathcal D$) | 0.760 | 0 |
| $1.708$ ($s_D$) | 0.500 | 48 | 3.221 | 0.525 | 0.760 | 0 |
| $1.958$ | 0.470 | 45 | 3.071 | 0.533 | 0.760 | 0 |
| $2.208$ | 0.440 | 23 | 1.971 | 0.616 | 0.760 | 0 |
| $2.458$ | 0.410 | 11 | 1.371 | 0.685 | 0.760 | 0 |
| $2.708$ | 0.380 | 3 | 0.971 | 0.745 | 0.760 | 0 |
| $2.758$ | 0.374 | 2 | 0.921 | 0.753 | 0.760 | 0 |
| $\ge2.805$ | $\le0.368$ | 0 | — | no equilibrium | — | — |

The removal of $\mathcal D$ and the zero outlay are analytical (Proposition S.5). The grid member at the minimal pool has $\bar\mu=0.36841$, slightly above the exact $0.36838$, so it drops out $10^{-4}$ before the analytical top of the window. Partial-order members with $x'>2.6$ are the first to go.

**Table 6. Devices compared at $r=3$.** Net proceeds $\mathsf N$; "range" is over the equilibria found.

| Device | removes $\mathcal D$ | equilibria | $\mathsf N$ | on-path outlay | $\mathcal W$ | status |
|---|---|---|---|---|---|---|
| none | no | $\mathcal D$; live family | 0.417 ($\mathcal D$); 0.525 to 0.760 (live) | 0 | 0; up to 0.107 | analytical ($\mathcal D$, minimal pool); family: numerical diagnostic |
| uniform $s=s_D$ | yes | live with pool | 0.024 (minimal pool); below 0.417 in every equilibrium | 0.854 | 0.007 | analytical |
| uniform $s\ge s_m$ | yes | full orders, certain entry, unique | $-2.426$ | 3.634 | $-1.625$ | analytical |
| lottery $\rho=0.07$, $s_\ell=s_m$ | yes, and no trade too | only full orders found | 0.537 | 0.254 | $-0.014$ | removal analytical; set: numerical diagnostic |
| lottery $\rho=0.25$, $s_\ell=s_m$ | yes | unique full orders | $-0.036$ | 0.908 | $-0.326$ | analytical |
| backstop $\bar s=s_D$ | yes | live family | 0.525 to 0.760 | 0 | 0.011 to 0.107 | removal analytical; family: numerical diagnostic |
| backstop $\bar s=2.758$ | yes | two members near the minimal pool | 0.753 to 0.760 | 0 | about 0.106 | as above |
| fee $0.217$ plus backstop | yes | minimal pool on the plateau | 0.814 | $-0.074$ (fee received) | 0.103 | analytical for the minimal pool; family not searched |
| any reserve | no | $\mathcal D$ survives | — | 0 | — | analytical |
| flow disclosure | no | $\mathcal D$; minimal pool only | 0.417; 0.760 | 0 | 0; 0.107 | analytical [Referee fix: analytical for $\mathcal D$ and the full-order minimal pool; S.9 rules out larger pools at each order profile but does not rule out other live order profiles] |
| full disclosure of $\theta$ (seller information) | no insider | entry iff $\theta=h$ | 0.979 | 0 | — | analytical |

The lottery rows use $s_\ell=s_m$ with the tie rule at $\mu=m$; Proposition S.7(b) states the strict version.

**Table 7. Reserve at $r=3$.**

| $p'$ | $B(\tfrac12)$ | $\tau$ | $\mathcal D$ exists | live possible ($\tau\le M$) |
|---|---|---|---|---|
| 0 | 4.333 | 0.700 | yes | yes |
| 0.5 | 4.292 | 0.705 | yes | yes |
| 1.0 | 4.167 | 0.720 | yes | yes |
| 1.2 | 4.130 | 0.726 | yes | yes |
| 1.5 | 4.063 | 0.738 | yes | no |
| 3.0 | 3.500 | 0.857 | yes | no |
| 7.0 | 1.500 | 2.000 | yes | no |

Status: analytical (closed forms of (A.42)).

## 6. What this means for "when is the investor an insider"

### 6.1 Materiality by design

The fork says the investor is an insider only where the challenger listens to the price. Design changes that answer in three ways.

1. **Materiality for a price.** A uniform subsidy $s\ge s_D$ makes $\theta$ material in every equilibrium, because the challenger now prepares at the prior. But the insider status is bought. At a weak incumbent ($\Delta_T\le2k$) the insider does not trade ($\mathcal C$). At $s\ge s_m$ the insider trades, but its trades no longer steer entry. Only for $s\in[s_D,s_m)$ and $\Delta_T>2k$ does the subsidized economy keep both an insider and feedback. At the benchmark the seller loses money on every such design (Proposition S.3).
2. **A threat against the dead outcome.** The backstop does not create materiality. It only makes the equilibrium without materiality inconsistent. The investor is then an insider in every equilibrium for the fork's own reason: the challenger listens to the price. With the backstop, Proposition F.3 becomes a statement about every equilibrium (Corollary S.6). The flat regions stay flat: below $\mathfrak r(k)$ and above $r_C$ no live equilibrium exists, and the backstop would leave none at all.
3. **The floor, rebuilt.** A lottery with $\rho>2k/\Delta_T$ makes $\theta$ material at every price for the subsidized draw. This is the paper's (A1). It removes all no-trade outcomes, but the seller pays $\rho s_\ell$ on path.

So the answer to "when is the investor an insider" now has a design clause. Without a device: in some equilibria on the coexistence region, and in none outside it. With a backstop: in every equilibrium on the coexistence region. With a uniform subsidy above $s_D$: in every equilibrium at every strength, at a cost. [Referee fix: "every equilibrium" is empty of content where no equilibrium exists. Existence at $s=s_D$ is open for $r$ between $\mathfrak r(2k)$ and about $1.5$ (open item 1).]

### 6.2 Policy and empirical content

The model gives one clean prediction and several cautions.

*Prediction.* Provisions that lower a rival's net preparation cost below the prior-belief threshold remove the outcome without informed trading. Where the incumbent is strong ($\Delta_T>2k$), such provisions imply pre-announcement informed trading in the target and a price that is informative about the rival (Proposition S.1(v)(b)). Along the minimal-pool selection, a more generous provision weakly raises price informativeness and entry (Proposition S.2). But the sensitivity of rival entry to the pre-entry price is hump-shaped in generosity: it is zero in $\mathcal D$, positive on $[s_D,s_m)$, and zero again once entry is certain. The testable content is this hump, not a monotone effect. [Referee fix: the hump assumes that $\mathcal D$ is played below $s_D$. If a live equilibrium is played there, the sensitivity is already positive on $[s_M,s_D)$, and only the fall at $s_m$ remains. Caution 2 below applies to this prediction too.]

*Cautions.*

1. **Selection of provisions.** A value-maximizing board would not adopt a uniform reimbursement large enough to remove $\mathcal D$ at benchmark-like primitives (Proposition S.3, Table 4). At the benchmark $s_D$ exceeds the target's whole expected sale price. Any reimbursement capped at a small fraction of deal value cannot reach $s_D$. Observed provisions should therefore come from economies where the dead gap $c-B_r(\tfrac12)$ is small, or from motives outside the model.
2. **Unobserved selection at $s=0$.** The econometrician does not see whether the economy played $\mathcal D$ or a live equilibrium without the provision. The effect of a provision on informed trading is a jump if $\mathcal D$ was played and a small change if a live equilibrium was played. The sign agrees; the size does not.
3. **Unclaimed provisions can matter most.** The backstop works, yet nobody ever claims it. A study that measures a provision by its take-up would find zero effect for the device that matters most here. Its footprint is in informed trading and in price informativeness before any rival appears, and in the fact that rival entry follows price run-ups rather than quiet prices.
4. **Surplus.** The efficient uniform subsidy is $p^2/r$ (Proposition S.4), far below $s_D$. A mandate large enough to remove $\mathcal D$ induces preparation at beliefs where it destroys surplus (Table 2: $\mathcal W$ turns negative just above $s_D$). The backstop keeps the live surplus ($0.107$ at $r=3$) at no cost. [Referee fix: $0.107$ is the minimal pool. At $\bar s=s_D$ all 48 searched members survive, with surplus from $0.011$ to $0.107$. Only near the top of the window do the survivors have surplus near $0.106$.]

## 7. Open items and the next best step

1. **Gap region under a uniform subsidy.** For $s\ge s_D$ and $r\in(\mathfrak r(2k),\approx1.55)$ the best-response map cycles between zero and full orders, and no pure equilibrium was found (Table 3). Existence of a mixed equilibrium there is open.
2. **Backstop beyond full orders.** Proposition S.5(v) bounds the pool for full-order equilibria only. Partial-order, mixed, and non-interval pools are covered only by the cutoff-family search in Table 5.
3. **Fee plus backstop.** At $r=3$ a fee of $0.217$ with a backstop yields $0.814$ in the minimal pool, above any device without a fee. The cutoff family under the fee was not searched, so the pessimistic value is open. The seller's optimum over $(s_0,\bar s,p')$ is open.
4. **Cheaper lottery.** A lottery prize of $s_D$ instead of $s_m$ removes $\mathcal D$ (Proposition S.7(a)) at lower cost, but pools can return. Its equilibrium set is open.
5. **Robustness of the backstop.** The pool price is an exact atom in the model. With non-informational price noise, the quiet price becomes a region, and the band in (B) must absorb that noise but exclude live entry prices. The analysis of that case is open.
6. **Reserve and backstop together.** Proposition S.8 rules out the reserve as a selector. Whether a reserve above $\ell$ and a backstop together improve on the fee-plus-backstop design is open (open item 4 of `mechanism.md`).

**Next best step.** Add the backstop to `mechanism.md` as a proposition after F.3, with Corollary S.6, and record that Lemma S.2 closes open item 1. Then extend Proposition S.5(v) to the partial-order members of the cutoff family. The numbers in `backstop_family_r3.csv` suggest that the backstop removes them first, so a bound on $\bar\mu_{x'}$ along the partial-order segment would make the selection of near-minimal pools analytical for every searched member.

## Files

- `selection_solve.py`: closed forms and grid search; writes all CSV files. Run with `python3 fork/endogenous_insider/research/selection_design/selection_solve.py` (about three minutes).
- `key_numbers.csv`: every scalar quoted in Tables 1 and 6, with definitions and status.
- `subsidy_sweep_r3.csv`: Table 2, all branches at every $s$ in the sweep.
- `across_strengths.csv`: Table 3 and the backstop window across $r$.
- `cost_sweep_r3.csv`, `breakeven_r3.csv`: Table 4.
- `backstop_family_r3.csv`, `backstop_window_r3.csv`: Table 5.
- `lottery_r3.csv`: lottery rows of Table 6.
- `reserve_r3.csv`: Table 7.
