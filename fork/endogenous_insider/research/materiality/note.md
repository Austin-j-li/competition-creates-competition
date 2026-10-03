---
title: "Materiality: when is the investor an insider?"
subtitle: "Research track for the endogenous-insider fork"
date: "2026-10-03"
---

This note belongs to `fork/endogenous_insider/`. It uses the notation of `paper/main.md` and of `mechanism.md` in the fork. Equation numbers such as (4), (9), (12) and (A.5) to (A.11) refer to the paper. Results labeled F.1 to F.5 are the fork's. Results labeled M.1 to M.6 are new to this note. Every result carries its status in the paper's vocabulary: analytical, computer-assisted, numerical diagnostic, or open. Files in this folder: `materiality.py` (solver, writes CSV only), `render_tables.py` (reads CSV, writes `tables.md`), four CSV outputs, and `refs.bib`.

## 1. Question

What is the right formal definition of "insider" in the fork? The fork removes the cost floor. The target's value then depends on the investor's signal $\theta$ only where the challenger prepares. Whether the investor holds information about the stock is an equilibrium outcome. This note asks three things. First, what is the correct index of materiality, and how does it relate to the investor's gross value of information? Second, how does that index map to the legal test for material information about mergers, and what does it mean that the "probability" in that test depends on the insider's own trade? Third, where does the fork sit relative to the feedback-effects and insider-trading literatures?

## 2. Headline result

The investor is an insider in an equilibrium of the fork if and only if the entry set has positive measure. That is equivalent to each of: the investor trades, the price is informative, and the equilibrium is not the dead one (Proposition M.1, analytical). Ex ante materiality factors exactly as the legal test says it should: a probability times a magnitude, $\mathfrak M_\theta=\Pr(\text{entry}\mid\theta)\,\Delta_T$ (Proposition M.2, analytical). The magnitude $\Delta_T(r)$ is set by the sale rule and the incumbent's strength. The probability is set in equilibrium, and the investor's own order moves it: a buy raises it and a sell lowers it (Proposition M.4). On the benchmark the index rises from $0.106$ to $0.320$ along the live branch and then drops to zero at the preparation ceiling $r_C$ (Table 1, numerical diagnostic). A by-product is a closed form for the existence statistic $J$ in (F.3), which turns the fork's open item 1 into one line of elementary arithmetic (Lemma M.3, analytical).

## 3. Model changes

None beyond the fork. The model is Section 2 of the paper with one deterministic cost $c>0$ in place of $(c_L,c_H,\rho)$, as in `mechanism.md` Section 2. Throughout I keep the fork's maintained domain
$$
B_r(\tfrac12)<c\le B_r(M),
\tag{M.0}
$$
so that $\tau\in(\tfrac12,M]$ and the dead profile $\mathcal D$ exists. On the benchmark vector $(h,\ell,p,b,k,c)=(10,1,0.5,2,0.02,6)$ the first inequality holds at every $r\in(\ell,h)$, because $\sup_r B_r(\tfrac12)=4.875<6$ (fork thresholds table). The second holds for $r\le r_C=3.5927$.

Three objects from the fork are used repeatedly. The entry set $A=\{x:e(x)=1\}$ and its complement, the pool $N$. The residuals of Lemma F.1(d), $A_H=\mathbf 1_A\Delta_T(1-\mu_X)$ and $A_L=\mathbf 1_A\Delta_T\mu_X$. And the full-order cutoff family of Proposition F.2(a), $A=[x',\infty)$ with $x'\ge x^*=\tfrac b2\log\frac{\tau}{1-\tau}$.

**Definitions.** Fix an equilibrium. Write $F_Z$ and $S_Z=1-F_Z$ for the Laplace noise distribution and survival functions.

- *Local materiality* at flow $x$: $\mathfrak m(x):=\mathbb E[V_T\mid H,x]-\mathbb E[V_T\mid L,x]$.
- *State-conditional ex ante materiality*: $\mathfrak M_\theta:=\mathbb E[\mathfrak m(X)\mid\theta]$.
- *Ex ante materiality index*: $\mathfrak M:=\mathbb E[\mathfrak m(X)]=\tfrac12(\mathfrak M_H+\mathfrak M_L)$.
- *Insider*: the investor is an insider in the equilibrium if $\mathfrak M>0$.

In the fork $\mathbb E[V_T\mid\theta,x]=t_0+e(x)(t_\theta-t_0)$, so $\mathfrak m(x)=e(x)\Delta_T=\mathbf 1_A(x)\Delta_T$. Materiality is a two-point object. On $A$ the signal moves expected value by the full spread $\Delta_T$. On $N$ it moves nothing.

## 4. Results

### Lemma M.1 (materiality identity; analytical)

*In every equilibrium and at every flow $x$,*
$$
A_H(x)+A_L(x)=\mathfrak m(x)=\mathbf 1_A(x)\,\Delta_T,
\qquad
P(x)=\mathbb E[V_T\mid L,x]+\mu_X(x)\,\mathfrak m(x).
$$
*The two residual advantages split local materiality by the market's posterior: the buyer in state $H$ gets the share $1-\mu_X$, the seller in state $L$ gets the share $\mu_X$.*

*Proof.* Lemma F.1(d) gives $A_H=\mathbf 1_A\Delta_T(1-\mu_X)$ and $A_L=\mathbf 1_A\Delta_T\mu_X$. Add them. For the second identity, on $N$ both sides equal $t_0$. On $A$, $P=t_L+\Delta_T\mu_X$ by Lemma F.1(a), and $\mathbb E[V_T\mid L,x]=t_L$. $\square$

### Proposition M.1 (the investor is an insider if and only if he trades; analytical)

*Assume (M.0). In every equilibrium of the fork, pure or mixed, the following are equivalent.*

*(i) $\mathfrak M>0$ (the investor is an insider).*
*(ii) $\mathfrak M_H>0$. (iii) $\mathfrak M_L>0$.*
*(iv) $A$ has positive Lebesgue measure.*
*(v) $\Pr(X\in A)>0$ under the equilibrium flow law.*
*(vi) Some investor type places a nonzero order with positive probability.*
*(vii) The price experiment is not constant, and it strictly Blackwell dominates the constant experiment.*
*(viii) The equilibrium is not $\mathcal D$.*

*Proof.* Under any conditional order distributions, the flow density in state $\theta$ is $a_\theta(x)=\int f(x-q)\,d\sigma_\theta(q)$, and $a_\theta>0$ everywhere because $f>0$. Hence $e_\theta=\int_A a_\theta\,dx>0$ if and only if $\operatorname{Leb}(A)>0$, for each $\theta$. Since $\mathfrak M_\theta=e_\theta\Delta_T$ and $\Delta_T>0$ on $r>\ell$, (i) to (v) are equivalent.

(iv) implies (vi). Suppose both types place all mass on zero. Then $a_H=a_L=f$, $\mu_X\equiv\tfrac12$, and Lemma F.1(c) gives $A\subseteq\{\mu_X\ge\tau\}=\emptyset$ because $\tau>\tfrac12$ under (M.0). So $A$ is empty, which contradicts (iv).

(vi) implies (iv). Suppose $A$ is null. Then $P=t_0$ almost everywhere by Lemma F.1(a), and $\mathbb E[V_T\mid\theta,x]=t_0$ almost everywhere. Every nonzero order $q$ earns $-k|q|<0$ against this schedule, and zero earns exactly zero. So zero is the unique best response of both types, which contradicts (vi).

(iv) implies (vii). On $A$, $P=t_L+\Delta_T\mu_X$ is injective in $\mu_X$ and exceeds $t_0$, so the map $g(P)=\mu_X\mathbf 1\{P\ne t_0\}$ is a measurable function of the price. Its conditional means differ across states:
$$
\mathbb E[g(P)\mid H]-\mathbb E[g(P)\mid L]
=\int_A\mu_X\,(a_H-a_L)\,dx
=\int_A\mu_X\,(a_H+a_L)\,(2\mu_X-1)\,dx>0,
$$
because $\mu_X\ge\tau>\tfrac12$ on $A$ and $\operatorname{Leb}(A)>0$. So the law of $P$ depends on $\theta$. A constant experiment is a garbling of every experiment by a constant kernel, and no state-independent kernel maps a constant into a state-dependent law. This is Step 6 of the proof of Proposition 2 in the paper.

(vii) implies (iv). If $A$ is null, $P=t_0$ almost surely, which is the constant experiment.

(iv) is equivalent to (viii). $\mathcal D$ has $A=\emptyset$. Conversely, if $A$ is null the equilibrium has no entry and is $\mathcal D$ by Proposition F.1(ii). $\square$

Two remarks. First, the proof allows mixed orders; the fork's open item 2 does not affect this statement. Second, the benchmark has no such equivalence. There $\mathfrak m(x)\ge\rho\Delta_T>0$ at every flow, so the investor is an insider at every strength, including in the no-trade equilibrium below $r_N$ of Proposition A.4. The benchmark has passive insiders. The fork has none.

**Corollary M.1 (a perfectly enforced trading ban; analytical).** *Under (M.0), suppose a prohibition removes every informed order, so both types play zero. Then the unique continuation is $\mathcal D$: no entry, proceeds $t_0$, and $\mathfrak M=0$.* Proof: the step "(iv) implies (vi)" above. $\square$ In the fork a ban on trading on $\theta$ does not only transfer rents from noise traders to the investor's counterparties. It removes the challenger.

### Proposition M.2 (probability times magnitude; analytical)

*(a) In every equilibrium, $\mathfrak M_\theta=\Pr(X\in A\mid\theta)\cdot\Delta_T$ and $\mathfrak M=\mathsf E\cdot\Delta_T$, with $\mathsf E$ the preparation probability of (12) at $\rho=0$. The magnitude $\Delta_T(r)=(r-\ell)^2/(2r)$ depends only on the sale rule and the incumbent's strength. The probability depends on the order profile and the entry set, both equilibrium objects.*

*(b) Gross value bound. Against any fixed equilibrium schedule, a correctly signed order of size $s\in[0,1]$ earns gross profit at most the order size times the materiality index evaluated at that order:*
$$
sF_H(s)\le s\,\Delta_T\,\Pr(s+Z\in A),\qquad sF_L(s)\le s\,\Delta_T\,\Pr(-s+Z\in A).
$$

*(c) Under full orders and $A=[x',\infty)$, the existence statistic $J$ of (F.3) factors as*
$$
J=F_H(1)=\mathfrak M_H\cdot\mathbb E[1-\mu_X\mid H,\,X\in A]
=F_L(1)=\mathfrak M_L\cdot\mathbb E[\mu_X\mid L,\,X\in A].
$$
*Gross value of information equals probability, times magnitude, times the market's residual uncertainty on the entry set.*

*(d) The residual factor is bounded: $m\le\mathbb E[1-\mu_X\mid H,X\in A]\le1-\tau$, so $m\,\mathfrak M_H\le J\le(1-\tau)\,\mathfrak M_H$.*

*Proof.* (a) is $\mathfrak m=\mathbf 1_A\Delta_T$ integrated against the conditional flow law. (b) $F_H(s)=\int f(x-s)A_H(x)\,dx\le\Delta_T\int_A f(x-s)\,dx=\Delta_T\Pr(s+Z\in A)$ because $0\le A_H\le\mathbf 1_A\Delta_T$; the same for $F_L$ with $f(x+s)$. (c) Under full orders $F_H(1)=\Delta_T\int_A f(x-1)(1-\mu_X)\,dx=\Delta_T e_H\int_A\frac{f(x-1)}{e_H}(1-\mu_X)\,dx$, and $f(x-1)/e_H$ on $A$ is the conditional density of $X$ given $H$ and $X\in A$. The $L$ form is symmetric. The equality $F_H(1)=F_L(1)$ is (A.7). (d) On $A$, $\tau\le\mu_X\le M$, so $1-M=m\le1-\mu_X\le1-\tau$. $\square$

On the benchmark the residual factor is nearly constant, between $0.269$ and $0.277$ across the whole branch (Table 1, column $J/\mathfrak M_H$). It sits just above $m=0.2689$ because the entry set is mostly the plateau $x\ge1$ where $\mu_X=M$. So in this model gross value of information is close to $m$ times the state-$H$ materiality index.

### Lemma M.3 (closed form for the existence statistic; analytical)

*Under full orders and entry set $A=[x',\infty)$ with $x'\in[-1,1]$, with $\operatorname{gd}(u)=\arctan(\sinh u)$,*
$$
J(x')=\frac{\Delta_T\,e^{-1/b}}{4}\Big[\operatorname{gd}(1/b)-\operatorname{gd}(x'/b)+\operatorname{sech}(1/b)\Big],
\qquad
J(x')=\frac{\Delta_T\,e^{-x'/b}}{4\cosh(1/b)}\ \text{ for } x'\ge1 .
$$
*$J$ is continuous and strictly decreasing in $x'$. The sufficient test $k<(1-1/b)J(x')$ of Proposition F.2(c) therefore holds exactly on an interval $[x^*,\bar x)$, and for $\bar x\ge1$,*
$$
\bar x=b\log\frac{(1-1/b)\,\Delta_T}{4k\cosh(1/b)} .
$$

*Proof.* Write $f(z)=e^{-|z|/b}/(2b)$. For $x\ge1$, $f(x-1)f(x+1)/(f(x-1)+f(x+1))=\frac{1}{2b}\,\frac{e^{-x/b}}{e^{1/b}+e^{-1/b}}$, whose integral over $[x',\infty)$ is $\frac{e^{-x'/b}}{4\cosh(1/b)}$. For $-1\le x\le1$, $f(x-1)=e^{-(1-x)/b}/(2b)$ and $f(x+1)=e^{-(1+x)/b}/(2b)$, so the integrand equals $\frac{1}{2b}\,\frac{e^{-2/b}}{e^{-(1-x)/b}+e^{-(1+x)/b}}=\frac{e^{-1/b}}{4b\cosh(x/b)}$. Since $\int\operatorname{sech}(x/b)\,dx=b\,\operatorname{gd}(x/b)$, the integral over $[x',1]$ is $\frac{e^{-1/b}}{4}[\operatorname{gd}(1/b)-\operatorname{gd}(x'/b)]$. Add the two pieces and multiply by $\Delta_T$. Monotonicity: the integrand is positive. The interval claim: $J(x^*)>J(x')$ for $x'>x^*$, and $(1-1/b)J(x')=k$ has one root. Solve the $x'\ge1$ form for $\bar x$. $\square$

The solver checks the closed form against adaptive quadrature at every row; the largest discrepancy is $3\times10^{-42}$ in 40-digit arithmetic. At the benchmark, $J(3)=0.09549$, which matches the fork's $0.0955$ by quadrature, and $(1-1/b)J(3)-k=0.0278>0$. The sufficient-existence boundary on the minimal-pool branch is $r_J=2.0155$, the root of $(1-1/b)J(r)=k$; the fork's grid found $2.05$ as the first grid point. At $r=3$ the family bound is $\bar x=2.614$: every $x'\in[x^*,2.614)$ supports a full-order equilibrium by Proposition F.2(a) and the sufficient test. The fork's grid found full orders up to $x'=2.522$ and interior orders at $3.022$, which is consistent. The status of the formula is analytical. The status of the decimal values is numerical diagnostic until an interval enclosure is run; see open item 1.

### Proposition M.4 (materiality under a unilateral deviation; analytical where stated)

*Fix an equilibrium in the cutoff family, $A=[x',\infty)$ with $x'\ge x^*>0$.*

*(a) The local materiality function $\mathfrak m(\cdot)=\mathbf 1_{[x',\infty)}\Delta_T$ is a function of the equilibrium schedule. A unilateral deviation does not change it.*

*(b) The realized materiality $\mathfrak m(X)$ with $X=q+Z$ satisfies $\Pr(\mathfrak m(X)=\Delta_T\mid q)=S_Z(x'-q)$, strictly increasing in $q$. A buy raises the probability that the information becomes material; a sell lowers it.*

*(c) For correctly signed orders, $\Pr(A\mid H,s)=S_Z(x'-s)$ rises in $s$ and $\Pr(A\mid L,-s)=S_Z(x'+s)$ falls in $s$.*

*(d) The low type's gross per-unit advantage $F_L(s)=\Delta_T\int_{x'}^\infty f(x+s)\mu_X(x)\,dx$ is strictly decreasing in $s$ on $[0,1]$. (Analytical.) The high type's $F_H(s)$ is increasing in $s$ on the benchmark rows (Table 3). (Numerical diagnostic.)*

*Proof.* (a) The schedule $(P,e)$ is fixed in a unilateral deviation by Section 2.3 of the paper. (b) $\Pr(q+Z\ge x')=S_Z(x'-q)$, and $S_Z$ is strictly decreasing. (c) is (b) at $q=s$ and $q=-s$. (d) For $x\ge x'>0$ and $s\ge0$, $x+s>0$, so $f(x+s)=e^{-(x+s)/b}/(2b)$ is strictly decreasing in $s$ pointwise; $\mu_X>0$; integrate. $\square$

Part (d) is the fork's version of the asymmetry in @EdmansGoldsteinJiang2015. The seller's own trade erodes the materiality of the seller's own information, because selling pushes the flow toward the pool where nothing is at stake. The buyer's trade creates materiality. At full orders the two gross values coincide, $F_H(1)=F_L(1)=J$, by the symmetry of the Laplace density, so the asymmetry is in the shape of the profit curve rather than in its endpoint. On the fork's lower live branch the low type's short is interior, $(1,-0.25)$ at $r=1.66$ rising to $(1,-0.98)$ at $r=2$ (fork `branches.csv`), which is where this asymmetry shows. Table 3 also shows that the short side is the lucrative side per unit at small orders: $F_L(0)=0.158$ against $F_H(0)=0.058$ at $r=3$, because on the entry set the market already believes $H$ is likely, so the price overstates value by $\Delta_T\mu_X\ge\Delta_T\tau$ in state $L$ and understates it by only $\Delta_T(1-\mu_X)\le\Delta_T(1-\tau)$ in state $H$.

### Proposition M.5 (the index across strengths)

*(a) (Analytical.) $\Delta_T$ is strictly increasing in $r$. On the full-order minimal-pool branch, $\tau$ is strictly increasing in $r$, hence $x^*$ is strictly increasing and $e_H$, $e_L$, $\mathsf E$ are strictly decreasing in $r$. The probability leg of the index falls and the magnitude leg rises.*

*(b) (Analytical.) At the ceiling, the left limit of the index is $\mathfrak M(r_C^-)=\frac{1+e^{-2/b}}{4}\,\Delta_T(r_C)$, and $\mathfrak M=0$ for $r>r_C$. On the benchmark the limit is $0.3199$.*

*(c) (Numerical diagnostic.) On the 51 grid strengths below $r_C$, $\mathfrak M(r)=\mathsf E(r)\Delta_T(r)$ on the minimal-pool full-order profile is strictly increasing in $r$; on the part where the sufficient test holds it rises from $0.1057$ at $r=2.05$ to $0.3199$ at $r=3.5926$, while $\mathsf E$ falls from $0.393$ to $0.342$. The same holds on the fork's own interior-order branch from $r=1.66$ (index $0.0504$) to $r=2.0$ (index $0.0985$), Table 3b.*

*Proof of (a) and (b).* $\Delta_T'(r)>0$ is (5). Write $\tau=(c-g_L)/(g_H-g_L)$ with $g_H-g_L=h-r/2-\ell^2/(2r)$. The numerator rises in $r$ because $g_L'<0$ by (5), and it is positive because (M.0) gives $c>B_r(\tfrac12)>g_L$. The denominator is positive and falls in $r$, since its derivative is $-\tfrac12+\ell^2/(2r^2)<0$ for $r>\ell$. So $\tau$ rises, $x^*=\tfrac b2\log\frac{\tau}{1-\tau}$ rises, and $e_H=S_Z(x^*-1)$, $e_L=S_Z(x^*+1)$ fall. (b) As $r\uparrow r_C$, $\tau\uparrow M$ and $x^*\uparrow1$, so $(\alpha_H,\alpha_L)\to(\tfrac12,\tfrac12e^{-2/b})$ by (A.14) with $\rho=0$; above $r_C$ Proposition F.1(iii) gives $\mathcal D$. $\square$

Part (c) is the sentence the fork wants about materiality. More competition makes the information more material along the live branch even though it makes entry less likely, because the magnitude leg wins. The index then collapses to zero at the ceiling. The most material information in the model sits just below the strength at which the challenger stops listening.

### Remark M.6 (the disclosure counterfactual; analytical, remark)

The legal test asks what a disclosure would do to a reasonable investor's valuation. If $\theta$ were public before preparation, the challenger would prepare if and only if $g_\theta\ge c$, and the spread between states would be $\mathfrak m^{\rm disc}=t_H\mathbf 1\{g_H\ge c\}+t_0\mathbf 1\{g_H<c\}-t_L\mathbf 1\{g_L\ge c\}-t_0\mathbf 1\{g_L<c\}$. On the benchmark at $r=3$, $g_H=8.46\ge6>0.125=g_L$, so $\mathfrak m^{\rm disc}=t_H-t_0=1.125$, against $\Delta_T=0.667$ (column `disclosure_spread`). Disclosure changes the probability leg to one in state $H$ and to zero in state $L$, so its magnitude differs from $\Delta_T$. The index $\mathfrak M$ is the materiality of $\theta$ as *traded on*, not as *disclosed*. The two coincide only if disclosure left entry unchanged, which it does not.

## 5. Numerics

All values below use the benchmark vector $(h,\ell,p,b,k,c)=(10,1,0.5,2,0.02,6)$ and $\rho=0$. The solver evaluates the closed forms of Lemma M.3 and Proposition M.2 in 40-digit arithmetic and checks $J$ against adaptive quadrature at every row. Status of every numerical entry: numerical diagnostic. Full tables are in `tables.md`; the CSV files carry twelve significant digits and a status column per row.

**Table 1. Materiality index on the minimal-pool full-order branch** (`materiality_branch.csv`). "benchmark index" is $[\rho+(1-\rho)\mathsf E]\Delta_T$ with the paper's $\rho=0.25$, $c_L=1$, at the same $r$.

| $r$ | $\Delta_T$ | $\mathsf E$ | $\mathfrak M=\mathsf E\Delta_T$ | $\mathfrak M_H$ | $\mathfrak M_L$ | $J$ | $J/\mathfrak M_H$ | $(1-1/b)J-k$ | benchmark index | region |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.2000 | 0.0167 | 0.4162 | 0.0069 | 0.0100 | 0.0038 | 0.0028 | 0.277 | -0.0186 | 0.0094 | $\mathcal D$ unique (F.1 iv) |
| 1.6600 | 0.1312 | 0.4039 | 0.0530 | 0.0769 | 0.0291 | 0.0211 | 0.274 | -0.0095 | 0.0725 | sufficient test fails |
| 2.0000 | 0.2500 | 0.3945 | 0.0986 | 0.1434 | 0.0539 | 0.0391 | 0.273 | -0.0004 | 0.1365 | sufficient test fails |
| 2.0500 | 0.2689 | 0.3931 | 0.1057 | 0.1537 | 0.0577 | 0.0419 | 0.273 | 0.0010 | 0.1465 | sufficient test holds |
| 2.5000 | 0.4500 | 0.3798 | 0.1709 | 0.2491 | 0.0927 | 0.0675 | 0.271 | 0.0138 | 0.2407 | sufficient test holds |
| 3.0000 | 0.6667 | 0.3637 | 0.2425 | 0.3541 | 0.1308 | 0.0955 | 0.270 | 0.0278 | 0.3485 | sufficient test holds |
| 3.5000 | 0.8929 | 0.3456 | 0.3086 | 0.4511 | 0.1660 | 0.1213 | 0.269 | 0.0407 | 0.4546 | sufficient test holds |
| 3.5926 | 0.9355 | 0.3420 | 0.3199 | 0.4677 | 0.1721 | 0.1258 | 0.269 | 0.0429 | 0.4738 | sufficient test holds |
| 3.5927 | 0.9355 | 0 | 0 | 0 | 0 | 0 | — | -0.0200 | 0.2339 | above ceiling, $\mathcal D$ unique |

Rows with "sufficient test fails" are hypothetical full-order profiles; the fork's solver finds live fixed points there with interior low-type orders, Table 3b. The row at $r=1.2$ is below $\mathfrak r(k)=1.221$, where no live equilibrium exists (Proposition F.1 iv); the entries show what the index *would* be if the schedule were in place. The benchmark index is positive at every $r$, including above the ceiling, where it equals the floor $\rho\Delta_T$.

**Table 2. The cutoff family at $r=3$** (`materiality_family.csv`): the index and the own-order entry probabilities. The sufficient test certifies full orders for $x'<\bar x=2.614$.

| $x'$ | $e_H$ | $e_L$ | $\mathfrak M$ | $\Pr(A\mid H,s=0)$ | $\Pr(A\mid H,s=1)$ | $\Pr(A\mid L,s=0)$ | $\Pr(A\mid L,s=1)$ | $(1-1/b)J-k$ |
|---|---|---|---|---|---|---|---|---|
| 0.871 | 0.5312 | 0.1962 | 0.2425 | 0.3234 | 0.5312 | 0.3234 | 0.1962 | 0.0278 |
| 1.500 | 0.3894 | 0.1433 | 0.1776 | 0.2362 | 0.3894 | 0.2362 | 0.1433 | 0.0149 |
| 2.000 | 0.3033 | 0.1116 | 0.1383 | 0.1839 | 0.3033 | 0.1839 | 0.1116 | 0.0072 |
| 2.500 | 0.2362 | 0.0869 | 0.1077 | 0.1433 | 0.2362 | 0.1433 | 0.0869 | 0.0012 |
| 2.600 | 0.2247 | 0.0826 | 0.1024 | 0.1363 | 0.2247 | 0.1363 | 0.0826 | 0.0001 |
| 2.700 | 0.2137 | 0.0786 | 0.0974 | 0.1296 | 0.2137 | 0.1296 | 0.0786 | -0.0008 |
| 3.000 | 0.1839 | 0.0677 | 0.0839 | 0.1116 | 0.1839 | 0.1116 | 0.0677 | -0.0035 |
| 3.500 | 0.1433 | 0.0527 | 0.0653 | 0.0869 | 0.1433 | 0.0869 | 0.0527 | -0.0072 |

Every member of the family is the same economy at the same orders. The index falls by more than half across the certified range, from $0.2425$ to $0.102$. The same investor with the same signal is "less of an insider" in the larger-pool members.

**Table 3. Gross value of trading against the fixed schedule, by own order size** (`materiality_deviation.csv`), minimal pool. $F_\theta(s)$ by quadrature; the bound is Proposition M.2(b).

| $r$ | $s$ | $\Pr(A\mid H,s)$ | $F_H(s)$ | $\Delta_T\Pr(A\mid H,s)$ | $\Pr(A\mid L,-s)$ | $F_L(s)$ | $\Delta_T\Pr(A\mid L,-s)$ | $U_H(s)$ | $U_L(s)$ |
|---|---|---|---|---|---|---|---|---|---|
| 3.00 | 0.00 | 0.3234 | 0.0582 | 0.2156 | 0.3234 | 0.1575 | 0.2156 | 0 | 0 |
| 3.00 | 0.25 | 0.3665 | 0.0659 | 0.2443 | 0.2854 | 0.1390 | 0.1903 | 0.0115 | 0.0297 |
| 3.00 | 0.50 | 0.4153 | 0.0747 | 0.2769 | 0.2519 | 0.1226 | 0.1679 | 0.0273 | 0.0513 |
| 3.00 | 0.75 | 0.4706 | 0.0846 | 0.3137 | 0.2223 | 0.1082 | 0.1482 | 0.0485 | 0.0662 |
| 3.00 | 1.00 | 0.5312 | 0.0955 | 0.3541 | 0.1962 | 0.0955 | 0.1308 | 0.0755 | 0.0755 |
| 2.05 | 0.00 | 0.3539 | 0.0260 | 0.0952 | 0.3539 | 0.0691 | 0.0952 | 0 | 0 |
| 2.05 | 0.50 | 0.4544 | 0.0334 | 0.1222 | 0.2756 | 0.0538 | 0.0741 | 0.0067 | 0.0169 |
| 2.05 | 1.00 | 0.5715 | 0.0419 | 0.1537 | 0.2146 | 0.0419 | 0.0577 | 0.0219 | 0.0219 |

$U_H(1)=U_L(1)=0.0755$ at $r=3$ and $0.0219$ at $r=2.05$ reproduce the fork's branch table.

**Table 3b. The index on the fork's own live branch** (`branches.csv` of the fork; interior orders; numerical diagnostic).

| $r$ | $q_H$ | $q_L$ | $\mathsf E$ | $\Delta_T$ | $\mathfrak M$ | $\mathfrak M_H$ | $\mathfrak M_L$ | $U_H$ | $U_L$ |
|---|---|---|---|---|---|---|---|---|---|
| 1.66 | 1.00 | -0.25 | 0.3842 | 0.1312 | 0.0504 | 0.0657 | 0.0351 | 0.0029 | 0.0007 |
| 1.80 | 1.00 | -0.65 | 0.3908 | 0.1778 | 0.0695 | 0.0964 | 0.0426 | 0.0095 | 0.0062 |
| 2.00 | 1.00 | -0.98 | 0.3941 | 0.2500 | 0.0985 | 0.1429 | 0.0542 | 0.0192 | 0.0189 |
| 2.05 | 1.00 | -1.00 | 0.3930 | 0.2689 | 0.1057 | 0.1537 | 0.0577 | 0.0219 | 0.0219 |
| 3.00 | 1.00 | -1.00 | 0.3636 | 0.6667 | 0.2424 | 0.3541 | 0.1308 | 0.0755 | 0.0755 |

**Table 4. Boundaries** (`materiality_thresholds.csv`).

| object | value | definition | status |
|---|---|---|---|
| $\mathfrak r(k)$ | 1.2210 | $\Delta_T(r)=k$; below it $\mathcal D$ is unique (F.1 iv) | analytical, closed form |
| $r_J$ | 2.0155 | $(1-1/b)J(r)=k$ on the minimal-pool branch; above it F.2(c) certifies a live equilibrium | closed-form $J$, bisection root |
| $r_C$ | 3.5927 | $B_r(M)=c$; above it $\mathcal D$ is unique (F.1 iii) | analytical, closed form (A.11) |
| $\mathfrak M(r_C^-)$ | 0.3199 | left limit of the index at the ceiling | analytical, (A.14) with $\rho=0$ |
| $\bar x(3)$ | 2.6140 | at $r=3$, full orders with $A=[x',\infty)$ pass the sufficient test iff $x'<\bar x$ | analytical, closed form |
| $m$, $M$ | 0.2689, 0.7311 | posterior bounds | analytical |

## 6. What this means for "when is the investor an insider"

**The formal answer.** The investor is an insider exactly in the live equilibria, and there he is an insider because he trades (Proposition M.1). Materiality is a fixed-point property of the strategy profile. It is not a property of the signal, and it is not a property of the realized trade. Three layers separate cleanly.

1. *Equilibrium layer.* The local materiality function $\mathfrak m(\cdot)=\mathbf 1_A\Delta_T$ is fixed by the schedule that market makers and the challenger play. It is common knowledge. In a live equilibrium $\theta$ is material even on realizations where the investor's order happens to be small, because noise can carry the flow into $A$. In $\mathcal D$ the same $\theta$ is immaterial even if the investor deviates and trades, because the schedule does not respond to one deviation. So "he is an insider only because he trades" is true in the aggregate sense: no informed trading, no entry set, no materiality.
2. *Realization layer.* The investor's own order shifts the probability that his information turns out to be material (Proposition M.4). The buyer in state $H$ raises it; the seller in state $L$ lowers it and thereby erodes his own per-unit advantage (M.4(d)).
3. *Comparative-static layer.* Competition sets the magnitude leg, $\Delta_T(r)$. The probability leg is positive only on $[\,\mathfrak r(k),r_C\,]$ and only in the live equilibria. Along the live branch the index rises with $r$ and then collapses at $r_C$ (M.5). The information is most material where the challenger is about to stop listening.

**The legal mapping.** The U.S. test for the materiality of merger information is the one the index already has. *Basic Inc. v. Levinson*, 485 U.S. 224 (1988), adopted the *TSC Industries v. Northway*, 426 U.S. 438, 449 (1976), standard for Rule 10b-5 (substantial likelihood that a reasonable investor would view the fact as significantly altering the total mix) and, for contingent events such as mergers, held that materiality "will depend at any given time upon a balancing of both the indicated probability that the event will occur and the anticipated magnitude of the event in light of the totality of the company activity," quoting *SEC v. Texas Gulf Sulphur Co.*, 401 F.2d 833, 849 (2d Cir. 1968) (en banc) [@BasicLevinson1988, at 238; @TexasGulfSulphur1968]. In the fork the contingent event is the challenger's preparation, the probability is $e_\theta$, and the magnitude is $\Delta_T$ (Proposition M.2(a)). The index is the legal test written as an equation.

The mismatch is in how the two assess the probability. *Basic* says a factfinder assesses probability through "indicia of interest in the transaction at the highest corporate levels," such as board resolutions, instructions to investment bankers, and actual negotiations [@BasicLevinson1988, at 239]. Those are past actions of the merging parties. In the fork, at the time of the trade, the challenger has done nothing. It has not decided to prepare, and under the fork's timing it cannot decide before it sees the price. Every indicium a court could point to comes into existence after, and because of, the price the trade produces. The equilibrium probability $e_\theta$ is a forecast of the challenger's response, not a record of its conduct. A court that looked only at conduct at the time of the trade would find the probability near zero; the model says it is $e_\theta>0$ in a live equilibrium and exactly zero in $\mathcal D$. The law has no doctrine for self-fulfilling materiality. But the *TSC* standard is ultimately about the reasonable investor's valuation, and that valuation is an equilibrium object. Applied with the equilibrium in view, the legal test agrees with Proposition M.1: in $\mathcal D$ a reasonable investor would, correctly, consider $\theta$ unimportant.

Two further doctrinal points sharpen the picture.

- *Rule 14e-3* [@Rule14e3] applies once any person "has taken a substantial step or steps to commence, or has commenced, a tender offer," and reaches any other person who holds material nonpublic information relating to that offer which was acquired directly or indirectly from the offering person, the issuer, or persons acting for them; it needs no fiduciary duty, as *United States v. O'Hagan*, 521 U.S. 642, 673 (1997), confirmed. The SEC's adopting release lists as substantial steps a board vote on a resolution relating to the offer, the formulation of a plan or proposal to make the offer, arranging financing, preparing offer materials, and authorizing negotiations with a dealer-manager [@SECRelease17120]. In the fork, preparation *is* the substantial step, and it comes after the trade. The trigger of Rule 14e-3 is itself endogenous to the trade that the rule would govern. Moreover the rule's source condition is not met if $\theta$ is the investor's own knowledge of the target's customers or technology, as Section 1.1 of the paper frames it, rather than information taken from the challenger. And the rule covers tender offers only; the model's sale is a seller-run auction in which a tender offer is one possible form of bid.
- *Chiarella v. United States*, 445 U.S. 222 (1980), is the fork's investor under the classical theory: a financial printer who deduced targets from bidders' documents and bought target shares. The Court held that "a duty to disclose under § 10(b) does not arise from the mere possession of nonpublic market information" (at 235) and that liability requires "a relationship of trust and confidence between parties to a transaction" (at 230). The fork's investor holds information about the acquirer, not from the target, and owes the target's shareholders nothing under the classical theory. *Dirks v. SEC*, 463 U.S. 646, 662 (1983), makes tippee liability derivative of an insider's breach for personal benefit. Under the misappropriation theory of *O'Hagan*, a person commits fraud "when he misappropriates confidential information for securities trading purposes, in breach of a duty owed to the source of the information" (at 652), and full disclosure to the source forecloses liability (at 655). O'Hagan knew his client's *plan*. The fork's investor knows the challenger's *value* $\theta$; the plan does not yet exist, and the investor's trade is what calls it into existence. Whether the investor is liable therefore turns on the source of $\theta$ and on any duty to that source, which the model does not specify. Materiality, which the model does specify, is necessary for liability under every theory and is settled by Proposition M.1. Under Rule 10b5-1(b) [@Rule10b51] a trade is "on the basis of" the information if the trader was aware of it when he traded; in the fork the same awareness is material in one equilibrium and immaterial in another.

**One sentence.** In the fork an insider is a person whose private signal the market expects a third party to act on, and the expectation is self-fulfilling: the probability leg of the legal test is the equilibrium itself.

## 7. Position in the literature

Each entry gives the closest paper's result and then what the fork adds. All records are in `refs.bib` with a verification note per entry. Every legal source and every economics record was checked against a court-report mirror, the publisher, or RePEc. Six entries are marked `partly`: one field in each could not be confirmed from a loaded page (the DOI for Dow and Gorton 1997, Khanna, Slezak and Bradley 1994, Fishman and Hagerty 1992, and Kyle and Vila 1991; the end page for Ayres and Bankman 2001; the volume, issue and pages for Bris 2005, whose title, journal, year and DOI are confirmed).

**Feedback effects.**

- @DowGoldsteinGuembel2017 show that traders' private value of information about a project rises with the ex ante likelihood that the project is undertaken, which creates strategic complementarity in information production and a breakdown equilibrium. The fork keeps that structure with the project replaced by a rival's participation in a contest. New: (i) the real decision maker is a third party, not the issuer, and its action changes the traded claim's sensitivity through an auction payment rule; (ii) because of that rule, the probability leg and the magnitude leg of materiality move in opposite directions with the comparative-static variable $r$ (Proposition M.5(a)); (iii) information is exogenous, so the complementarity is between the trade and the participation decision, not between two production decisions; (iv) the equivalence "insider iff trades" and the index $\mathfrak M$ are explicit; (v) the pool family has closed-form bounds (Lemma M.3).
- @BondEdmansGoldstein2012 review feedback and propose that price efficiency be judged by usefulness for real decisions. The fork proposes the parallel for materiality: the relevance of a signal for a security is defined by the real decision that responds to the price, and it can be zero in equilibrium.
- @BondGoldsteinPrescott2010 show that when agents use prices for corrective actions, prices become less revealing. In the fork the action is entry, not correction, and the pool is the region where the price stops revealing; Lemma F.1(b) and the family of Table 2 are the analog.
- @EdmansGoldsteinJiang2015 derive an asymmetry: feedback discourages selling on bad news because the firm corrects. Proposition M.4(d) is the fork's version: selling on bad news lowers the chance of the event that gives the bad news its value, so the seller's per-unit advantage falls in its own order size. The difference is the channel. There the firm removes the bad outcome; here the rival's non-entry removes the stock's sensitivity to the signal altogether.
- @GoldsteinGuembel2008 study manipulation by an uninformed trader who sells to cancel investment. The fork has no uninformed strategic trader. Proposition M.4(b) shows that a sell order lowers the entry probability, so the ingredient is present; whether an uninformed seller could profit is open item 7.

**Insider trading, outside search, takeovers.**

- @KhannaSlezakBradley1994: insider trading crowds out outside search for information. In the fork, preparation is the challenger's information acquisition about $\theta$ ("paying $C$ reveals $\theta$"), and the insider's trade crowds it *in* (Proposition M.1: no trade, no preparation). The sign is reversed because the outsider here learns from the price rather than competes with the insider.
- @FishmanHagerty1992: insider trading can reduce price efficiency by deterring other traders. In the fork the insider's trade creates price informativeness and its own materiality at once (Proposition M.1 (vi) and (vii)).
- @KyleVila1991: noise trading lets a raider hide its accumulation, which makes takeovers profitable. In the fork the trader is not the raider, its signal concerns a bidder who has not decided, and noise bounds the posterior to $[m,M]$ and thereby bounds entry at $r_C$; noise limits takeovers here rather than enabling them.
- @Leland1992: insider trading raises price informativeness and real investment. In the fork the "investment" is a rival's entry, and whether there is an insider at all is the equilibrium object. Corollary M.1 adds a cost of prohibition that has no analog in a model with a fixed insider: a perfect ban yields $\mathcal D$ and removes the challenger.
- @Meulbroek1992 finds that about half of the pre-announcement run-up in acquisitions occurs on insider trading days; @KeownPinkerton1981 and @JarrellPoulsen1989 document run-ups and ask whether they reflect insider trading or market anticipation. The fork says the dichotomy is false in its setting: the anticipation *is* the trade, and the trade induces the bid. @Bris2005 studies enforcement and takeover-related insider trading across countries; the fork predicts that enforcement that removes informed trading on prospective bidders removes the bidders too.
- @Hirshleifer1971 (foreknowledge has private value without social value when nothing is produced) and @DowGorton1997 (prospective information is valuable only if it influences a decision) are the roots of the "valuable only if acted upon" idea. In the fork the acting party is a stranger to both the trader and the issuer, and the act is participation in a contest for the issuer. @FoxGlostenRauterberg2018 classify "announcement information" as information that would reach the price soon anyway, so trading on it has little social value. The fork's $\theta$ is the opposite case: without the trade there is no announcement.
- @AyresBankman2001 analyze trading in the securities of other firms on inside information. The fork's investor trades the target on information about the bidder, which is a cross-firm case, and under *Chiarella* the classical duty is absent.

**What is new in the fork, in brief.**

- Materiality is an equilibrium outcome, and "insider iff trades" is an equivalence, not an assumption (M.1).
- The legal probability-magnitude test holds as an identity, with the probability leg endogenous to the trade and the magnitude leg set by competition (M.2, M.4).
- The two legs move in opposite directions with incumbent strength, and the magnitude wins on the live branch until a collapse at the ceiling (M.5).
- The seller's trade erodes the materiality of the seller's own signal; the buyer's trade creates it (M.4(d)).
- A trading ban removes the rival bidder, not only the insider's rent (Corollary M.1).
- The existence statistic has a closed form, so the fork's benchmark existence claim can be certified by one interval evaluation (M.3).

## 8. Open items and the next best step

1. *Enclose $J$ by interval arithmetic.* Lemma M.3 reduces the fork's open item 1 to the evaluation of $\operatorname{gd}$, $\operatorname{sech}$, $\exp$ and $\log$ at exact decimals. An outward-rounded evaluation in `mpmath.iv` with the paper's tolerance declaration would make Proposition F.3(ii) computer-assisted at the benchmark. This is the next best step; it costs one afternoon and raises the status of a headline result.
2. *Monotonicity of $\mathfrak M(r)$.* Proposition M.5(c) is a numerical diagnostic. The analytical question is the sign of $\frac{d}{dr}\log\mathfrak M=\frac{r+\ell}{r(r-\ell)}+\frac{\mathsf E'(r)}{\mathsf E(r)}$. The first term is large near $\ell$ and falls like $1/r$; the second is negative and bounded. A proof on the live region is open.
3. *Monotonicity of $F_H(s)$ in $s$.* Analytical for $F_L$ (M.4(d)); numerical diagnostic for $F_H$.
4. *Partial-order branch.* Tables 3b values come from the fork's grid solver and inherit its status. A certificate for one interior-order node would make the asymmetry in M.4(d) computer-assisted.
5. *Mixed equilibria.* Proposition M.1 covers them. Whether they exist is the fork's open item 2 and is unchanged.
6. *Legality is outside the model.* The model fixes materiality. Liability needs a source and a duty (classical, tipper-tippee, misappropriation) or the Rule 14e-3 trigger, none of which the model specifies. A version of the model with the source of $\theta$ made explicit (the challenger's adviser versus an independent specialist) would let the legal analysis bite.
7. *Manipulation.* Can an uninformed trader profit by selling into the pool? Proposition M.4(b) supplies the lever. The price in the pool is $t_0$, which equals value there, so the gain must come from the entry region; this needs a re-solved equilibrium with an uninformed strategic trader.
8. *Disclosure counterfactual.* Remark M.6 shows the magnitude under disclosure differs from $\Delta_T$. A legal materiality test based on disclosure and one based on trading give different magnitudes in this model; which one a court should use for an insider-trading case is a question for the legal literature, not for this note.
