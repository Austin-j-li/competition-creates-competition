# B2. The discrete-Laplace model: theory

Workstream B2, 21 October 2026. Base model: the discrete-Laplace model of TEAM_RULES §4.2.
Paired numerical check: B1 (`memos/B_dlaplace_numeric.md`); Section 5.8 compares the two memos.
Scripts and their printed outputs: `scripts/B_dlaplace_theory/` (Section 5.7).

## 1. Question

Brief §0 states a candidate fix for the three-point model. The noise is the difference of two
independent geometric counts of unit noise orders. This memo develops that model analytically. It
answers seven items:

1. the posteriors under every investor strategy;
2. a Proposition 2 analog, with exact cutoffs and the admissible $c_H$ window;
3. a Proposition 3 analog (coexistence), with every mixed equilibrium and the order of entry;
4. welfare and ownership, and the effect of price access (Table 2 and Section 6.1 of the paper);
5. the general prior, the presence probability $\lambda$, and general value classes $G_j$;
6. the fixed-experiment control (Proposition A.3) and the information controls of Section 4.2;
7. a comparison with the Laplace paper and with the three-point model.

Result 13 gives a verdict on every claim of brief §0.

## 2. Setup

### 2.1 Base model, and why

I use the discrete-Laplace model of TEAM_RULES §4.2. It changes the three-point model in one place:
the noise law. The reason is the diagnosis in brief §0. Equal three-point noise makes the middle
flows uninformative and the top flow conclusive. The discrete-Laplace law has full support on the
integers and a bounded one-step likelihood ratio. Result 1 shows that these two features restore an
interior posterior range and remove every off-path flow.

### 2.2 Primitives

- **Auction.** As in the paper (Sections 2.2 and 3.1, eq. (4)): incumbent value $R\sim U[0,r]$,
  reserve $p$, a cash second-price auction, truthful bids. The objects $t_0,t_H,t_L,g_H,g_L$,
  $\Delta_T=t_H-t_L$, $w_L=t_L-t_0>0$ and $B_r(\mu)=g_L+\mu(g_H-g_L)$ are those of TEAM_RULES §3.
  I checked them against the pinned paper, eq. (4), and by quadrature (script `closed_forms.py`,
  block A).
- **Classes (Reading N).** Nature draws the class $j\in\{H,L\}$ with $\Pr(H)=\pi$. In the benchmark the
  values are the point masses $h$ and $\ell$. Result 11 treats general distributions $G_j$.
- **Costs.** $C=c_L=0$ with probability $\rho$, and $C=c_H$ otherwise. The challenger learns $C$ after
  it sees the price.
- **Investor.** It is present with probability $\lambda\in(0,1]$. When present it sees $j$. It buys one
  unit ($q=1$) or nothing ($q=0$). It buys with probability $\beta_j$ in class $j$ and pays $kq$. The
  purchase rate is $s_j=\lambda\beta_j$.
- **Noise.** $Z=G_1-G_2$ with independent geometric counts, so
  $\Pr(Z=z)=f(z)=\frac{1-a}{1+a}a^{|z|}$ with $a=e^{-1/b}$. The flow is $X=q+Z\in\mathbb Z$.
- **Prices.** Market makers see $X$ and set $P(X)=\mathbb E[V_T\mid X]$. The challenger sees $P$ and
  $C$, not $X$.

**Benchmark.** $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_L=0$, $c_H=5$, $b=2$, $k=1/50$, $\pi=1/2$,
$\lambda=1$. Strengths $r_0=1.2$, $r_1=3$, $r_2=4.2$. Section 5.5 also uses $c_H=5.2$ with the
paper's strengths $(1.2,3,3.6)$.

### 2.3 Notation

- $\gamma=\frac1{1+a}=\Pr(Z\ge0)$ and $1-\gamma=\frac a{1+a}=\Pr(Z\ge1)$. Also $\delta=2\gamma-1=\frac{1-a}{1+a}$.
- **Good news** is a flow $x\ge1$. **Bad news** is a flow $x\le0$.
- When $s_L=0$, write $s=s_H\in[0,\lambda]$. The probabilities of good news and bad news are
  $N_+(s)=1-\gamma+\pi\delta s$ and $N_-(s)=\gamma-\pi\delta s$.
- The two posteriors are $\mu_+(s)=\pi(1-\gamma+\delta s)/N_+(s)$ and $\mu_-(s)=\pi(\gamma-\delta s)/N_-(s)$.
- Global bounds: $m_1(\pi)=\frac{\pi a}{\pi a+1-\pi}$ and $M_1(\pi)=\frac{\pi}{\pi+(1-\pi)a}$. At
  $\pi=1/2$ these are $m_1=1-\gamma=1/(1+e^{1/b})$ and $M_1=\gamma$.
- $\kappa=(1-\pi)\gamma(1-\gamma)$, $\varphi(y)=\frac1{1-\gamma+y}+\frac1{\gamma-y}$, and
  $\varphi_1(y)=\frac1{1-\gamma+y}+\frac\rho{\gamma-y}$.
- $\tau=(c_H-g_L)/(g_H-g_L)$. The high-cost type prepares at belief $\mu$ if and only if $\mu\ge\tau$.
- $s^*$ is the purchase rate with $\mu_+(s^*)=\tau$ (Result 2(d)).
- $\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}$ is the root above $\ell$ of $\Delta_T(r)=d$ (paper, (A.10)).
- The letter $\lambda$ is used only for presence (TEAM_RULES §2).

### 2.4 Equilibrium concept, beliefs and tie rules

- **Concept.** Perfect Bayesian equilibrium. The investor best-responds to fixed price and entry
  schedules; a unilateral deviation moves only the flow law (paper, Section 2.4). Market makers
  price competitively. The challenger prepares optimally given its posterior at the observed price.
  Bidders bid truthfully.
- **Beliefs.** Result 1(c) shows that every integer flow has positive probability under every
  strategy profile. Bayes' rule therefore fixes the posterior at every flow. Every price in the image
  of the price function comes from on-path flows. A unilateral deviation reaches only on-path flows.
  So no belief is off path, and no refinement is used.
- **Investor tie rules.**
  - (I0): zero at indifference. This is the prescribed rule of the prior three-point memos.
  - (IM): any mixture at indifference. This is the conventional rule.
- **Challenger tie rules.**
  - (C1): prepare at indifference. This is the paper's rule (Section 2.2).
  - (CM): any mixture at indifference.
- The low-cost type is never indifferent, because $B_r(\mu)\ge g_L>0=c_L$ at every belief.
- **Equilibrium outcome.** I count outcomes $(s,\bar e_+,\bar e_-)$: the purchase rate and the average
  entry after good news and after bad news. Result 1(e) shows that the flow law inside each half-line
  does not depend on the action. So payoffs, entry, ownership and proceeds depend on the entry
  schedule only through $\bar e_\pm$. Under (CM) at a knife edge, several price functions can support
  one outcome. They differ in no payoff-relevant way.

## 3. Results

### Result 1. Half-line sufficiency and the two posteriors (analytical)

**Statement.** For every $(\beta_H,\beta_L)$, every $\lambda\in(0,1]$ and every $\pi\in(0,1)$:

- (a) the likelihood ratio $\Pr(x\mid H)/\Pr(x\mid L)$ is constant on $x\ge1$ and on $x\le0$;
- (b) the two posteriors are
$$
\mu_+=\frac{\pi(1-\gamma+\delta s_H)}{\pi(1-\gamma+\delta s_H)+(1-\pi)(1-\gamma+\delta s_L)},\qquad
\mu_-=\frac{\pi(\gamma-\delta s_H)}{\pi(\gamma-\delta s_H)+(1-\pi)(\gamma-\delta s_L)};
$$
- (c) every flow is on path;
- (d) every posterior lies in $[m_1(\pi),M_1(\pi)]$, and $1-M_1(\pi)=m_1(1-\pi)$;
- (e) given the half-line, the flow law is the same for both actions. So $S=\mathbf 1\{X\ge1\}$ is a
  sufficient statistic, and the flow experiment is a binary channel: $\Pr(S=1\mid q=1)=\gamma$ and
  $\Pr(S=1\mid q=0)=1-\gamma$;
- (f) with $s_L=0$, the experiments are Blackwell ordered by the purchase rate $s$;
- (g) conversely, let the noise law be positive on the integers. If (a) holds under every profile, the
  noise is a difference of two independent geometric counts. The two rates may differ.

**Proof.**

(a) The one-step ratio is $f(x-1)/f(x)=a^{|x-1|-|x|}$. For $x\ge1$ the exponent is $-1$, so the ratio
is $1/a$. For $x\le0$ the exponent is $+1$, so the ratio is $a$. Hence

$$
\Pr(x\mid j)=(1-s_j)f(x)+s_jf(x-1)=
\begin{cases}
f(x)\,u_j,\quad u_j=1+s_j(a^{-1}-1), & x\ge1,\\
f(x)\,d_j,\quad d_j=1-s_j(1-a), & x\le0.
\end{cases}
$$

The factor $f(x)$ cancels from the ratio, which equals $u_H/u_L$ on $x\ge1$ and $d_H/d_L$ on $x\le0$.

(b) Multiply $u_j$ by $1-\gamma=a/(1+a)$: $(1-\gamma)u_j=[a+s_j(1-a)]/(1+a)=1-\gamma+\delta s_j$.
Multiply $d_j$ by $\gamma$: $\gamma d_j=[1-s_j(1-a)]/(1+a)=\gamma-\delta s_j$. Bayes' rule gives (b).

(c) $f(x)>0$, $u_j\ge1$ and $d_j\ge a>0$. So $\Pr(x\mid j)>0$ at every flow, for both classes.

(d) $u_j\in[1,a^{-1}]$ and $d_j\in[a,1]$. So the likelihood ratio lies in $[a,a^{-1}]$ at every flow,
and Bayes' rule maps this interval to $[m_1(\pi),M_1(\pi)]$. The identity follows from
$1-M_1(\pi)=\frac{(1-\pi)a}{\pi+(1-\pi)a}=m_1(1-\pi)$. The upper bound is attained on $x\ge1$ when
$s_H=1$ and $s_L=0$.

(e) The tail sums are $\Pr(Z\ge0)=\frac{1-a}{1+a}\cdot\frac1{1-a}=\gamma$ and $\Pr(Z\ge1)=a\gamma=1-\gamma$.
Given $x\ge1$ and $q=0$, the flow law is $f(x)/(1-\gamma)$. Given $x\ge1$ and $q=1$, it is
$f(x-1)/\gamma=a^{-1}f(x)/\gamma$. Since $\gamma=(1-\gamma)/a$, the two laws agree. The same argument
holds on $x\le0$. Given $S$, the flow carries no information about $q$, and therefore none about $j$.

(f) Take $0\le s<s'\le1$. Define the kernel $Q(1\mid1)=q_0+s/s'$ and $Q(1\mid0)=q_0$, with
$q_0=(1-\gamma)(1-s/s')$. Both entries lie in $[0,1]$. Applied to the $s'$ channel it gives, for class
$L$, $(1-\gamma)(q_0+s/s')+\gamma q_0=q_0+(1-\gamma)s/s'=1-\gamma$. For class $H$ it gives
$(1-\gamma+\delta s')(q_0+s/s')+(\gamma-\delta s')q_0=q_0+(1-\gamma+\delta s')s/s'=1-\gamma+\delta s$.
These are the good-news probabilities of the $s$ channel. So the $s$ experiment is a garbling of the
$s'$ experiment. The order is strict. A garbling cannot raise the gap
$\Pr(S=1\mid H)-\Pr(S=1\mid L)$, and this gap is $\delta s'$ for the $s'$ channel but $\delta s<\delta s'$
for the $s$ channel.

(g) Suppose the posterior is constant on $x\ge1$ for some profile with $s_H\ne s_L$. With
$R(x)=f(x-1)/f(x)$, the likelihood ratio is $(1-s_H+s_HR)/(1-s_L+s_LR)$, which is strictly monotone
in $R$. So $R$ is constant on $x\ge1$, say $R_+$, and $f(x)=f(0)R_+^{-x}$ for $x\ge0$. Likewise $R=R_-$
on $x\le0$ gives $f(-n)=f(0)R_-^{\,n}$ for $n\ge0$. Summability needs $R_+>1>R_-$. This is the law of
$G_1-G_2$ with geometric rates $a_+=1/R_+$ for $G_1$ and $a_-=R_-$ for $G_2$. $\square$

**Remarks.**

- At $\pi=1/2$ under full purchases, $(\mu_+,\mu_-)=(\gamma,1-\gamma)=(M_1,m_1)=(0.622459,0.377541)$
  at $b=2$. This confirms brief §0.
- The bounds are the paper's (7)–(8) with $2/b$ replaced by $1/b$. Buy-only orders span one unit, not
  two.
- With rates $a_+\ne a_-$ the structure survives. Then $\gamma$ becomes $\Pr(Z\ge0)=(1-a_-)/(1-a_+a_-)$,
  and $1-\gamma$ becomes $\Pr(Z\ge1)=a_+\Pr(Z\ge0)$. I do not develop that case.
- Check (computer-assisted): direct Bayes over $|x|\le320$ reproduces (b) to $10^{-50}$ for six
  profiles, including mixed and wrong-signed ones (`closed_forms.py`, block C).

### Result 2. Price sufficiency, no purchases by class L, and the purchase payoff (analytical)

**(a) Price sufficiency.** Since $c_L=0<g_L\le B_r(\mu)$, the low-cost type prepares at every price, so
$e(P)\ge\rho$. Competitive pricing gives $P(x)=t_0+e(P(x))[w_L+\Delta_T\mu_x]$. Hence
$\mu_x=[P-t_0-e(P)w_L]/[e(P)\Delta_T]$, which is a function of the price. The challenger's posterior
at a price therefore equals the flow posterior. This is the argument of the paper's Proposition A.2.
It uses no property of the noise law.

*Construction.* $P_r(\mu)=t_0+e_r(\mu)(w_L+\Delta_T\mu)$ is strictly increasing in $\mu$ (paper, (A.3)).
Under (C1) the price takes two values, $P_r(\mu_+)$ and $P_r(\mu_-)$, or one value when $s_H=s_L$.

**(b) Class L never buys.** Given $j$ and $x$, the terminal value has mean $t_0+e(x)(t_j-t_0)$.
Subtract the price:

$$
\mathbb E[V_T\mid H,x]-P(x)=e(x)\Delta_T(1-\mu_x),\qquad
\mathbb E[V_T\mid L,x]-P(x)=-e(x)\Delta_T\mu_x<0.
$$

A purchase in class $L$ earns less than $-k<0$. So $\beta_L=0$ in every equilibrium, under every tie
rule.

**(c) The purchase payoff.** Let $s_L=0$ and $s=s_H$. A purchase moves the flow to $1+Z$. It reaches
good news with probability $\gamma$ and bad news with probability $1-\gamma$. By Result 1(e), the
average entry that it meets on each half-line is the $f$-weighted average $\bar e_\pm$. So the gross
payoff of a purchase in class $H$ is
$K=\Delta_T[\gamma\bar e_+(1-\mu_+)+(1-\gamma)\bar e_-(1-\mu_-)]$. Bayes' rule gives
$1-\mu_+=(1-\pi)(1-\gamma)/N_+(s)$ and $1-\mu_-=(1-\pi)\gamma/N_-(s)$. Therefore

$$
\boxed{K(s;\bar e_+,\bar e_-)=\Delta_T\,\kappa\left[\frac{\bar e_+}{N_+(s)}+\frac{\bar e_-}{N_-(s)}\right],
\qquad \kappa=(1-\pi)\gamma(1-\gamma).}
$$

The investor in class $H$ compares $K-k$ with zero. These are its only two actions, so no derivative
bound is needed.

**(d) Entry.** Write $\bar e_\pm=\rho+(1-\rho)\zeta_\pm$, where $\zeta_\pm$ is the high-cost entry rate.
Then $\zeta=1$ if $\mu>\tau$ and $\zeta=0$ if $\mu<\tau$. At $\mu=\tau$, $\zeta=1$ under (C1) and
$\zeta\in[0,1]$ under (CM). Three facts fix the pattern:

- $\mu_+(s)-\pi=\pi(1-\pi)\delta s/N_+(s)\ge0$ and $\pi-\mu_-(s)=\pi(1-\pi)\delta s/N_-(s)\ge0$;
- $\mu_+'(s)=\pi(1-\pi)\delta(1-\gamma)/N_+(s)^2>0$;
- so if $B_r(\pi)<c_H$, that is $\tau>\pi$, then $\zeta_-=0$ at every $s$, and $\zeta_+$ switches once,
  at

$$
s^*=\frac{(1-\gamma)(\tau-\pi)}{\pi\delta(1-\tau)}.
$$

Full purchases can recruit the high-cost type if and only if $s^*\le\lambda$, that is,
$\mu_+(\lambda)\ge\tau$.

*Check (computer-assisted).* Direct flow sums reproduce the boxed $K$ to $10^{-50}$ for four rates and
three schedules. They also reproduce it for a schedule that varies inside the good-news half-line,
once $\bar e_+$ is the $f$-weighted average (`closed_forms.py`, block D).

### Result 3. Bounds on the purchase payoff, and its shape (analytical)

Put $y=\pi\delta s\in[0,\pi\delta\lambda]$, so $N_+=1-\gamma+y$ and $N_-=\gamma-y$. The map
$y\mapsto\delta-y$ swaps $1-\gamma+y$ and $\gamma-y$. So $\varphi$ is symmetric about $\delta/2$. It is
also convex.

**(a) Upper bound.** For every $s$ and every schedule, $K\le(1-\pi)\Delta_T$.

*Proof.* $\bar e_\pm\le1$ gives $K\le\Delta_T\kappa\varphi(y)$. On $[0,\pi\delta]\subset[0,\delta]$ the
convex symmetric $\varphi$ is largest at $y=0$, where $\varphi(0)=1/[\gamma(1-\gamma)]$. So
$K\le\Delta_T\kappa/[\gamma(1-\gamma)]=(1-\pi)\Delta_T$. Equality needs $s=0$ and entry one. $\square$

**(b) Lower bound.** For every $s$ and every schedule, $K\ge\rho\Lambda\Delta_T$, where

$$
\Lambda(\pi,\lambda)=\kappa\,\varphi\big(\min\{\pi\delta\lambda,\ \delta/2\}\big).
$$

*Proof.* $\bar e_\pm\ge\rho$ gives $K\ge\rho\Delta_T\kappa\varphi(y)$. On $[0,\pi\delta\lambda]$ the minimum
of $\varphi$ is at the point nearest to $\delta/2$. $\square$

At $\pi=1/2$ and $\lambda=1$, $\varphi(\delta/2)=4$, so $\Lambda=2\gamma(1-\gamma)$. Since
$\gamma(1-\gamma)=a/(1+a)^2=1/(a^{-1/2}+a^{1/2})^2$, this is $\Lambda=\tfrac12\operatorname{sech}^2(\tfrac1{2b})$.
At $b=2$, $\Lambda=0.470007$. The pointwise residual bound of the paper's eq. (11) has the analog
$e\Delta_T(1-\mu)\ge\rho m_1\Delta_T$. The averaged bound is sharper, because $2\gamma>1$.

**(c) Shape on each entry piece.** Write $K_\rho(s)=K(s;\rho,\rho)$ and $K_1(s)=K(s;1,\rho)$.

- $K_\rho=\rho\Delta_T\kappa\varphi(y)$ falls strictly for $y<\delta/2$ and rises for $y>\delta/2$. It is
  U-shaped in $s$ only when $\pi>1/2$ and $\lambda>1/(2\pi)$.
- $K_1=\Delta_T\kappa\varphi_1(y)$ has derivative $\Delta_T\kappa[-(1-\gamma+y)^{-2}+\rho(\gamma-y)^{-2}]$.
  This is negative for $y<y_1=[\gamma-\sqrt\rho(1-\gamma)]/(1+\sqrt\rho)$. A short computation gives
  $y_1-\delta/2=(1-\sqrt\rho)/[2(1+\sqrt\rho)]>0$. So $K_1$ falls strictly on $[0,\lambda]$ whenever
  $\pi\delta\lambda\le y_1$, and in particular whenever $\pi\le1/2$.
- At $s^*$ the payoff moves from $K_\rho(s^*)$ to $K_1(s^*)$ as $\zeta_+$ goes from 0 to 1. The move is
  linear in $\zeta_+$, with slope $\Delta_T\kappa(1-\rho)/N_+(s^*)$.

**(d) The no-trade payoff.** If $B_r(\pi)<c_H$, then $K_0:=K(0;\rho,\rho)=\rho(1-\pi)\Delta_T$. At
$\pi=1/2$ this is $\rho\Delta_T/2$, the paper's no-trade test (A.12).

**(e) Two more facts used below.** $\varphi(y)<\varphi(0)$ for $y\in(0,\delta)$, so $K_\rho(s)<K_0$ for
every $s\in(0,\lambda]$ and every $\pi$. And $K_F:=K_1(\lambda)$ is the payoff against the full-purchase
schedule that recruits after good news.

### Result 4. Proposition 2 analog (analytical)

**Statement.** Fix $0<p<\ell<r_0<r_1<h$, $\rho\in(0,1)$, $b>0$, $\pi\in(0,1)$, $\lambda\in(0,1]$,
$k>0$ and $c_L=0$. Suppose

$$
\text{(A2-DL)}\qquad B_{r_0}(\pi)<c_H<B_{r_1}\big(\mu_+(\lambda)\big),
$$

$$
\text{(A3-DL)}\qquad (1-\pi)\,\Delta_T(r_0)<k<\rho\,\Lambda(\pi,\lambda)\,\Delta_T(r_1).
$$

Condition (A1) of the paper is automatic: $c_L=0$ gives the floor at every belief. Then, under every
pair of tie rules:

- (i) at $r_0$ the unique equilibrium outcome is no trade. The price is constant, entry is $\rho$, and
  high-class ownership is $\mathsf O_H=\pi\rho$;
- (ii) at $r_1$ the unique outcome is $\beta_H=1$, $\beta_L=0$. The price takes two values. Entry and
  ownership are
$$
\mathsf E_1=\rho+(1-\rho)(1-\gamma+\pi\delta\lambda),\qquad
\mathsf O_{H,1}=\pi\big[\rho+(1-\rho)(1-\gamma+\delta\lambda)\big].
$$
  At $\lambda=1$ these are $\mathsf E_1=\rho+(1-\rho)\frac{\pi+(1-\pi)a}{1+a}$ and
  $\mathsf O_{H,1}=\pi[\rho+\frac{1-\rho}{1+a}]$. At $\pi=1/2$, $\mathsf E_1=(1+\rho)/2$ for every $b$.
  Both exceed their values at $r_0$, and the $r_1$ price strictly Blackwell dominates the $r_0$ price;
- (iii) take $r_2\in(r_1,h)$ with $B_{r_2}(\mu_+(\lambda))<c_H$. Since $\Delta_T$ rises in $r$, the
  unique outcome is again $\beta_H=1$, $\beta_L=0$. The price is informative, but entry returns to
  $\rho$ and ownership to $\pi\rho$.

The conditions are strict inequalities in continuous functions of the primitives. So they hold on an
open set, and the benchmark is an interior point of it (Section 5.1).

**Proof.**

*Step 1 (beliefs and the floor).* Result 1 gives the posteriors and the bounds. Result 2(a) gives
price sufficiency in every candidate equilibrium, at every strength.

*Step 2 (the weak economy).* By Result 3(a), $K\le(1-\pi)\Delta_T(r_0)<k$ for every $s$ and every
schedule. So a purchase is strictly worse than no purchase in class $H$, and class $L$ never buys
(Result 2(b)). No tie arises, so the tie rules do not matter. Thus $s=0$, every posterior is $\pi$, and
$B_{r_0}(\pi)<c_H$ gives entry $\rho$. The constant price $t_0+\rho(w_L+\pi\Delta_T)$ is competitive.

*Step 3 (the strong economy).* By Result 3(b), $K\ge\rho\Lambda\Delta_T(r_1)>k$ for every $s$ and every
schedule. So class $H$ strictly prefers to buy, and $s=\lambda$. The posteriors are $\mu_\pm(\lambda)$.
After bad news, $\mu_-<\pi$ and $B_{r_1}(\mu_-)<B_{r_1}(\pi)<B_{r_0}(\pi)<c_H$, so entry is $\rho$. After
good news, $B_{r_1}(\mu_+(\lambda))>c_H$, so entry is one. No tie arises. For existence, define the
price by $P_r(\mu)$ at the two posteriors. The challenger then prepares optimally, the price is
competitive, and $K>k$ confirms the investor's choice.

*Step 4 (outcomes).* Entry is $\rho+(1-\rho)\Pr(\text{good news})=\rho+(1-\rho)N_+(\lambda)$. Since $h>r$, a
prepared class-$H$ challenger always wins. So
$\mathsf O_H=\pi[\rho+(1-\rho)\Pr(\text{good news}\mid H)]=\pi[\rho+(1-\rho)(1-\gamma+\delta\lambda)]$.
At $\lambda=1$, $N_+(1)=\pi\gamma+(1-\pi)(1-\gamma)=\frac{\pi+(1-\pi)a}{1+a}$. Result 1(f) gives the
Blackwell comparison.

*Step 5 (the very strong economy).* $\Delta_T(r_2)>\Delta_T(r_1)$, so Step 3's bound applies and
$s=\lambda$. In every equilibrium $\beta_L=0$ and $s\le\lambda$, so every posterior is at most
$\mu_+(\lambda)$. Then $B_{r_2}(\mu)\le B_{r_2}(\mu_+(\lambda))<c_H$ at every flow, and entry is $\rho$.
$\square$

**Exact cutoffs and windows.**

- In $r$ (for fixed $k$): (A3-DL) holds if and only if $r_0<\mathfrak r(k/(1-\pi))$ and
  $r_1>\mathfrak r(k/(\rho\Lambda))$.
- The ceiling $r_C(\lambda)$ solves $B_r(\mu_+(\lambda))=c_H$. Since
  $B_r(\mu)=\mu h-\mu r/2+[(1-\mu)\ell^2-p^2]/(2r)$ falls strictly in $r$, the root is unique:
$$
r_C=\frac{\mu h-c_H+\sqrt{(\mu h-c_H)^2+\mu[(1-\mu)\ell^2-p^2]}}{\mu},\qquad \mu=\mu_+(\lambda).
$$
  This is the paper's (A.11) with $M$ replaced by $\mu_+(\lambda)$. At $\lambda=1$, $\mu_+(1)=M_1(\pi)$.
- The admissible $c_H$ window, as a function of $b$ and $\pi$ (at $\lambda=1$):
$$
B_{r_0}(\pi)<c_H<B_{r_1}\!\left(\frac{\pi}{\pi+(1-\pi)e^{-1/b}}\right),
$$
  plus $c_H>B_{r_2}(M_1(\pi))$ for part (iii). Under (C1) the right inequality may be weak; under (CM)
  it must be strict, or entry after good news is not determined.
- The $k$ window: $(1-\pi)\Delta_T(r_0)<k<\rho\Lambda(\pi,\lambda)\Delta_T(r_1)$, with
  $\Lambda=\frac12\operatorname{sech}^2(\frac1{2b})$ at $\pi=1/2$, $\lambda=1$.
- The bounds in (A3-DL) do not depend on the schedule. Each is attained by some rate and some schedule,
  so no schedule-free bound is sharper. The exact uniqueness boundaries depend on the schedule that $s$
  induces (Result 5).

**Exact region at fixed strengths (analytical, from Result 5).** Suppose good news can recruit at both
$r_0$ and $r_1$, as in the benchmark. Under (IM, CM), part (i) holds if and only if $k\ge K_0(r_0)$ and
$k>K_1(s^*(r_0))$. Part (ii) holds if and only if $k<K_\rho(s^*(r_1))$ and $k\le K_F(r_1)$. Under (I0),
the conditions are $k\ge\max\{K_0,K_F\}(r_0)$ and $k<\min\{K_0,K_F\}(r_1)$. At the benchmark:

- (IM, CM): $0.005770<k<0.078978$;
- (I0): $0.004896\le k<0.083333$;
- the schedule-free window (A3-DL): $0.008333<k<0.078335$, which lies inside both.

Under (IM, C1) the conditions differ only at one end point: part (ii) also holds at
$k=K_\rho(s^*(r_1))$. Part (iii) at $r_2=4.2$ holds for $k<K_\rho(\lambda)(4.2)=0.143240$ under every
rule. B1 reports the same (IM, CM) region.

### Result 5. The equilibrium set at a fixed strength (analytical)

**Statement.** Fix $r$ with $B_r(\pi)<c_H$. Assume that $K_\rho$ and $K_1$ fall on $[0,\lambda]$; by
Result 3(c) this holds whenever $\pi\le1/2$. Write $K_\rho^*=K_\rho(s^*)$ and $K_1^*=K_1(s^*)$.

*Case N (no recruitment), $\mu_+(\lambda)<\tau$.* Then $K=K_\rho(s)$ falls strictly from $K_0$ to
$K_\rho(\lambda)$, and:

- $k\ge K_0$: no trade only;
- $K_\rho(\lambda)<k<K_0$: under (IM), one mixed outcome $\tilde s\in(0,\lambda)$ with entry $\rho$;
  under (I0), **no equilibrium**;
- $k<K_\rho(\lambda)$: full purchases only, with entry $\rho$. At $k=K_\rho(\lambda)$ this holds under (IM).

*Case R (recruitment), $\mu_+(\lambda)>\tau$, so $0<s^*<\lambda$.* Then $K_\rho^*<K_0$ and $K_1^*>K_F$. The
equilibrium outcomes under (IM, CM) are exactly the following:

| Outcome | Exists if and only if | Entry $\mathsf E$ |
|---|---|---|
| no trade, $s=0$ | $k\ge K_0$ | $\rho$ |
| full purchases, $s=\lambda$ | $k\le K_F$ | $\rho+(1-\rho)N_+(\lambda)$ |
| mixed $\tilde s\in(0,s^*)$, no recruitment | $K_\rho^*<k<K_0$ | $\rho$ |
| mixed at $s^*$, challenger mixes with $\zeta^*$ | $K_\rho^*\le k\le K_1^*$ | $\rho+(1-\rho)\zeta^*N_+(s^*)$ |
| mixed $\hat s\in(s^*,\lambda)$, recruitment | $K_F<k<K_1^*$ | $\rho+(1-\rho)N_+(\hat s)$ |

Here $\tilde s$ and $\hat s$ solve $K_\rho(\tilde s)=k$ and $K_1(\hat s)=k$, and

$$
\zeta^*=\frac{N_+(s^*)\big[k/(\Delta_T\kappa)-\rho/N_-(s^*)\big]-\rho}{1-\rho}.
$$

- Under (IM, C1), drop the $s^*$ row, except at $k=K_1^*$, where $\zeta^*=1$.
- Under (I0), only the no-trade row and the full-purchase row remain, with $k<K_F$ in the second.

**Proof.** Class $L$ never buys (Result 2(b)), so an outcome is fixed by $s$ and $\zeta_+$. The investor
conditions are $K(0)\le k$ for $s=0$, $K(\lambda)\ge k$ for $s=\lambda$, and $K(s)=k$ for interior $s$.
On $[0,s^*)$ entry is $\rho$ and $K=K_\rho$. On $(s^*,\lambda]$ entry after good news is one and
$K=K_1$. Each piece falls strictly, so each has at most one root, and the root exists exactly on the
stated $k$ range. At $s^*$, $K$ is linear and increasing in $\zeta_+$. So $K=k$ has the unique solution
$\zeta^*\in[0,1]$ exactly when $K_\rho^*\le k\le K_1^*$. Solving the linear equation gives $\zeta^*$.
Result 3(e) gives $K_\rho^*<K_0$. Monotone $K_1$ gives $K_1^*>K_F$. $\square$

**Corollaries.**

- *Existence.* Under (IM, CM) an equilibrium exists for every $k$. The table covers every $k$: low $k$
  gives full purchases or $\hat s$, high $k$ gives no trade, and the $s^*$ row bridges the jump.
- *Failure under (I0).* Under (I0) existence fails exactly when $K_F\le k<K_0$ (Case R) or
  $K_\rho(\lambda)\le k<K_0$ (Case N). In Case R this needs $K_F\le K_0$, that is, no feedback.
  The script finds such a region at $\rho=0.95$, $k=0.3$, $r\in[2.92,2.97]$ (Section 5.7).
- *Counting.* In Case R with feedback ($K_0<K_F$), there is one outcome when $k<K_\rho^*$ or $k>K_1^*$,
  and three outcomes when $K_\rho^*<k<K_1^*$.
- *Prior above one half.* If $K_\rho$ is U-shaped, the piece $[0,s^*)$ can hold two roots. Each piece
  equation $K=k$ is the quadratic
  $q y^2-(q\delta-\rho+e)y+e\gamma+\rho(1-\gamma)-q\gamma(1-\gamma)=0$, with $q=k/(\Delta_T\kappa)$,
  $y=\pi\delta s$ and $e\in\{\rho,1\}$. This gives every root. At $\pi=0.7$, $r=3.5$ and $k=0.0632$
  there are two mixed outcomes ($s=0.5299$ and $0.8987$) and full purchases. Brute force confirms
  this (Section 5.7).

### Result 6. Proposition 3 analog: coexistence (analytical)

**Statement.** Fix $r$ with $B_r(\pi)<c_H<B_r(\mu_+(\lambda))$. Suppose

$$
K_0=\rho(1-\pi)\Delta_T\ \le\ k\ <\ K_F=\Delta_T\kappa\left[\frac1{N_+(\lambda)}+\frac\rho{N_-(\lambda)}\right].
$$

Under (IM) the value $k=K_F$ is also allowed. This range is nonempty if and only if the **feedback condition**
$\gamma(1-\gamma)[1/N_+(\lambda)+\rho/N_-(\lambda)]>\rho$ holds. At $\pi=1/2$ and $\lambda=1$ the condition
reads $\Lambda(1+\rho)>\rho$, that is, $\rho<\Lambda/(1-\Lambda)$; at $b=2$ this is $\rho<0.886819$. Then:

- (a) no trade (entry $\rho$) and full purchases (entry $\rho+(1-\rho)N_+(\lambda)$) are both
  equilibria, under every pair of tie rules;
- (b) under (IM, CM) there is exactly one more outcome: purchase rate $s^*$, with the high-cost type
  mixing at $\zeta^*\in(0,1)$ after good news. This holds whenever $K_1$ falls on $[s^*,\lambda]$, so
  for every $\pi\le1/2$. Under (C1) or under (I0) there is no third outcome;
- (c) entry and ownership are strictly ordered across the coexisting outcomes:
  $\rho<\mathsf E(s^*)<\mathsf E(\lambda)$, and $\pi\rho<\mathsf O_H(s^*)<\mathsf O_H(\lambda)$. The price
  experiments are Blackwell ordered in the same direction;
- (d) the middle outcome is unstable under a myopic adjustment of $s$: $K<k$ just below $s^*$ and $K>k$
  just above it.

**Proof.**

(a) No trade: against the no-trade schedule every posterior is $\pi$, entry is $\rho$, and a
purchase earns $K_0-k\le0$. Under (I0) the investor chooses zero at $K_0=k$; under (IM) zero is also
allowed. Full purchases: against the full-purchase schedule, entry is one after good news, because
$\mu_+(\lambda)>\tau$ strictly. So a purchase earns $K_F-k>0$. Both schedules are consistent by
Result 2(a).

(b) On $(0,s^*)$, $K=K_\rho(s)<K_0\le k$ by Result 3(e). So the investor strictly prefers zero, and no
interior $s$ there is optimal. On $(s^*,\lambda)$, $K=K_1(s)>K_1(\lambda)=K_F>k$. So the investor
strictly prefers to buy. At $s^*$, $K(s^*;\zeta)$ rises linearly from $K_\rho^*<k$ to $K_1^*>k$, so a
unique $\zeta^*\in(0,1)$ gives $K=k$. Under (C1), $\zeta=1$ and $K=K_1^*>k$, which breaks the
investor's indifference. Under (I0), interior $s$ is excluded.

(c) Entry is $\rho+(1-\rho)\zeta_+N_+(s)$, with $\zeta_+=0$ under no trade. Since $0<\zeta^*<1$ and
$N_+(s^*)<N_+(\lambda)$, the order is strict. Ownership is $\pi[\rho+(1-\rho)\zeta_+(1-\gamma+\delta s)]$,
with the same order. Result 1(f) orders the experiments by $s$.

(d) Immediate from (b). $\square$

**The strengths with coexistence.** Both $K_0$ and $K_F$ are proportional to $\Delta_T(r)$, and
$\Delta_T$ rises strictly. So, for fixed $k$, coexistence holds exactly for

$$
r_F\le r\le r_N,\qquad r_F=\mathfrak r\big(k/\hat K_F\big),\quad r_N=\mathfrak r\big(k/(\rho(1-\pi))\big),\quad \hat K_F=K_F/\Delta_T,
$$

under (IM), and for $r_F<r\le r_N$ under (I0). Both sets are intersected with the strengths where $B_r(\pi)<c_H<B_r(\mu_+(\lambda))$. At the benchmark this set is
$[1.443322,1.747878]$, and $r_C=3.986$ lies far above it (interval check, Section 5.7). It contains the
paper's three certified strengths $1.55$, $1.60$ and $1.65$. The upper end $r_N=1.747877538$ equals the
paper's no-trade boundary, because the no-trade payoff is the paper's $\rho\Delta_T/2$.

**Entry on the full and $\hat s$ branches (analytical).** On the full branch entry is $0.625$ for every
$r\in[r_F,r_C]$. On the branch $\hat s$ entry rises strictly with $r$. There
$\Delta_T(r)\,\kappa\varphi_1(\pi\delta\hat s)=k$, and $\kappa\varphi_1$ does not depend on $r$. Since
$\varphi_1$ falls and $\Delta_T$ rises, $\hat s(r)$ rises, and so does $\mathsf E=\rho+(1-\rho)N_+(\hat s)$.
Entry is $0.558559$, $0.576414$, $0.595797$ and $0.617257$ at $r=1.41,1.42,1.43,1.44$. Each of these
strengths also admits no trade. B1 found this branch numerically first.

The branch exists on an interval just below $r_F$. At $r_F$, $K_F=k$ and $K_1(s^*)>K_F$, because $K_1$
falls and $s^*<\lambda$. By continuity, $K_F<k<K_1(s^*)$ holds just below $r_F$, which is the existence
condition of Result 5. So the sequence of the paper's Figure 2 holds analytically in local form:

1. a partial informative family with rising entry coexists with no trade just below $r_F$;
2. full orders coexist with no trade on $[r_F,r_N]$;
3. no trade ends at $r_N$.

Only the left end $r_I$ of the partial family is numerical (Result 6A).

**The path under (I0) (analytical).** Under (I0) the whole path uses only the closed forms $r_F$, $r_N$,
$r_C$ and $\mathfrak r(k/(\rho\Lambda))=1.777986<r_C$. No trade holds for $r\le r_N$. Full purchases hold
for $r>r_F$. Both hold on $(r_F,r_N]$.

This result overlaps with workstream C9, which studies challenger mixing at indifference under
unequal three-point noise.

### Result 6A. The correspondence across strengths at the benchmark (numerical diagnostic)

The fixed-$r$ classification of Result 5 is analytical.
The ordering of the regions in $r$ uses two implicit crossings, $r_I$ ($K_1(s^*(r))=k$) and $r_U$
($K_\rho(s^*(r))=k$). I did not prove that each crosses once; the grid check found one crossing each.
So the region boundaries $r_I$ and $r_U$ are a **numerical diagnostic**. The resulting picture:

| Strengths | (IM, CM) outcomes | (IM, C1) | (I0) |
|---|---|---|---|
| $(1,\ r_I)$, $r_I=1.405430$ | no trade | no trade | no trade |
| $[r_I,\ r_F)$, $r_F=1.443322$ | no trade; $s^*$; $\hat s$ | no trade; $\hat s$ | no trade |
| $[r_F,\ r_N]$, $r_N=1.747878$ | no trade; $s^*$; full | no trade; full | no trade; full (from $r>r_F$) |
| $(r_N,\ r_U)$, $r_U=1.762507$ | $\tilde s$; $s^*$; full | $\tilde s$; full | full |
| $[r_U,\ r_C]$, $r_C=3.986097$ | full, $\mathsf E=0.625$ | same | same |
| $(r_C,\ \infty)$ | full, $\mathsf E=\rho$ | same | same |

In $s$ the correspondence is a fold. The no-trade branch continues as $\tilde s$ from $r_N$ to $r_U$.
It turns back along $s^*(r)$ from $r_U$ to $r_I$. It then rises as $\hat s$ to full purchases at $r_F$.

**Entry along the branches.** Entry is flat at $0.625$ on the full branch and rises on $\hat s$
(Result 6). On the $s^*$ branch it falls with $r$: $0.524$ at $r=1.42$, $0.366$ at $1.55$, $0.329$ at
$1.60$, $0.299$ at $1.65$, and $0.255$ at $1.75$. On $\tilde s$ it stays at $\rho$.

On the grid, the partial family $\hat s$ of Result 6 occupies the whole interval $[r_I,r_F)$. The
location of the paper's sequence differs. Here the paper's three certified
strengths lie in $[r_F,r_N]$. There entry is flat on the full branch and falls on the $s^*$ branch. The rising family $\hat s$ needs the conventional investor rule (IM); it is compatible with (C1).

### Result 7. The fixed-experiment control and the information controls (analytical)

**Proposition A.3 analog.** Fix any profile $(s_H,s_L)$ and vary $r$. Under $c_L=0$ the price reveals
$\mu_\pm$, which do not depend on $r$ (Results 1 and 2(a)). Under (C1), entry is

$$
\mathsf E(r)=\rho+(1-\rho)\big[N_+\mathbf 1\{B_r(\mu_+)\ge c_H\}+N_-\mathbf 1\{B_r(\mu_-)\ge c_H\}\big],
$$

where $N_\pm$ are the probabilities of good and bad news. Both $g_H$ and $g_L$ fall in $r$ (paper,
eq. (5)), so each indicator can only switch off. So $\mathsf E(r)$ weakly falls. It is a step function:
it is constant between the two crossings $r_C(\mu_+)$ and $r_C(\mu_-)$, and it jumps down at them.
Deterrence at a fixed experiment is therefore a jump, not a smooth decline.

**Frozen full orders at the benchmark.** $B_{1.2}(M_1)=5.904$ and $B_3(M_1)=5.312$ both exceed $c_H=5$,
and $B_{1.2}(m_1)=3.704<5$. So frozen full orders give entry $0.625$ at both $r_0$ and $r_1$. Entry
falls to $\rho$ only above $r_C=3.986$. Between $r_0$ and $r_1$ the control shows **no** direct
deterrence at all. The whole rise from $0.25$ to $0.625$ comes from the change in the experiment.

**Price hidden.** The challenger keeps the prior, so entry is $\rho$ at every flow. Result 3 still
applies with entry $\rho$. At $r_0$, $K\le(1-\pi)\Delta_T<k$ gives no trade. At $r_1$,
$K\ge\rho\Lambda\Delta_T>k$ gives full purchases. So the hidden economy has the same orders as the
feedback economy at both strengths, and entry is $\rho$ at both.

### Result 8. Welfare, ownership and price access (analytical)

**Outcome formulas.** Let $\bar e_-=\rho$ and $\bar e_+=\rho+(1-\rho)\zeta_+$. Then the entry
probabilities by class are

$$
e_H=\rho+(1-\rho)\zeta_+(1-\gamma+\delta s),\qquad e_L=\rho+(1-\rho)\zeta_+(1-\gamma).
$$

- Entry: $\mathsf E=\pi e_H+(1-\pi)e_L$.
- Ownership: $\mathsf O_H=\pi e_HW_H$, with $W_H=1$ in the benchmark ($h>r$).
- Target proceeds: $\mathcal R_T=t_0+\pi e_H(t_H-t_0)+(1-\pi)e_L(t_L-t_0)$.
- Net acquisition surplus (paper, (A.39)–(A.40)):
  $\mathcal W=\frac{r^2-p^2}{2r}+\sum_j\pi_je_j\big(g_j+\frac{p^2}r\big)-c_H(\mathsf E-\rho)-c_L\rho$.
- Investor profit: gross $\Pi=\pi sK(s)$, net $\pi s[K(s)-k]$. Market makers break even. So the
  liquidity traders lose the gross profit $\Pi$ (the zero-sum trading ledger of the prior welfare
  memo, Claim W3).

**Proposition A.9 analog.** Hold $r=r_1$ under (A2-DL)–(A3-DL). Compare the feedback economy with the
economy in which the challenger cannot see the price. Then:

- orders are full in both economies (Results 4 and 7), so the flow experiment and the trading costs
  coincide;
- access raises net acquisition surplus by
  $\Delta\mathcal W=(1-\rho)N_+(\lambda)\big[B_{r_1}(\mu_+(\lambda))-c_H+p^2/r_1\big]>0$;
- access raises target proceeds by
  $\Delta\mathcal R_T=(1-\rho)\big[\pi(1-\gamma+\delta\lambda)(t_H-t_0)+(1-\pi)(1-\gamma)(t_L-t_0)\big]>0$;
- access raises the investor's gross profit by
  $\Delta\Pi=\pi\lambda\Delta_T\kappa(1-\rho)/N_+(\lambda)>0$. The recruited entry raises the residual
  after good news. This is the feedback that the three-point model lacks.

*Proof.* Only high-cost preparation after good news differs between the two economies. Each such
preparation has the posterior $\mu_+(\lambda)$ and the cost $c_H$. By (A.40) of the paper it adds
$B_{r_1}(\mu_+)-c_H+p^2/r_1\ge p^2/r_1>0$ in expectation. Its probability is $(1-\rho)N_+(\lambda)$. For
proceeds, each extra entry in class $j$ adds $t_j-t_0>0$, and the extra entry rates by class are
$(1-\rho)(1-\gamma+\delta\lambda)$ and $(1-\rho)(1-\gamma)$. For the investor, the two schedules differ
only in $\bar e_+$, by $1-\rho$, which enters $K$ with weight $\Delta_T\kappa/N_+(\lambda)$. $\square$

At the benchmark: $\Delta\mathcal R_T=0.327490$, $\Delta\mathcal W=0.148310$, and the investor's gross
profit is $0.097918$ with access against $0.039167$ without (Section 5.2).

**Matched dividend (Section 6.1).** In each economy the mean price equals $\mathcal R_T$. So the
dividend that matches the hidden economy's mean price to the feedback economy's is
$\Delta\mathcal R_T=0.327490$. It leaves $V_T-P$, trading and entry unchanged, exactly as in the paper.

**Caveat: access can deter (analytical).** Suppose instead that the prior already recruits,
$B_r(\pi)\ge c_H$, so $\tau\le\pi$. Without access every cost type prepares. With access and informed
purchases, bad news has $\mu_-(s)<\tau$ once $s>s_-=\gamma(\pi-\tau)/(\pi\delta(1-\tau))$. Then bad
news deters the high-cost type. Example at $c_H=4$, $r=3$: $\tau=0.465$ and $s_-=0.3325$. Full
purchases are the unique outcome in both economies. Access lowers proceeds from $1.208333$ to
$0.942073$ (by $0.266260$). It raises $\mathcal W$ from $2.833333$ to $3.075394$, because it stops
high-cost entry at bad news, where $B_r(\mu_-)+p^2/r=3.35<c_H$. This matches the sign found for the
Laplace model in the prior memo `Q3_story.md` (Claim S4(b)).

### Result 9. The general prior (analytical)

Results 1–8 hold for every $\pi\in(0,1)$ with the stated formulas. The prior enters in five places.

1. *Bounds.* $[m_1(\pi),M_1(\pi)]$, with $1-M_1(\pi)=m_1(1-\pi)$.
2. *No-trade payoff.* $K_0=\rho(1-\pi)\Delta_T$. A higher prior leaves less residual to class $H$.
3. *Windows.* The $c_H$ window is $(B_{r_0}(\pi),B_{r_1}(M_1(\pi)))$, and the $k$ window is
   $((1-\pi)\Delta_T(r_0),\rho\Lambda(\pi,1)\Delta_T(r_1))$.
4. *Outcomes.* $\mathsf E_1=\rho+(1-\rho)\frac{\pi+(1-\pi)a}{1+a}$ and $\mathsf O_{H,1}=\pi[\rho+\frac{1-\rho}{1+a}]$.
5. *Shape.* For $\pi>1/2$ and $\lambda>1/(2\pi)$, $K_\rho$ is U-shaped. Then $\Lambda=4\kappa$, attained at
   $s=1/(2\pi)$, and one entry piece can hold two mixed roots (Result 5).

Proposition 3's coexistence (Result 6(a), (c)) holds for every $\pi$. Its exact count in (b) holds
for every $\pi\le1/2$, and for $\pi>1/2$ when $\pi\delta\lambda\le y_1$. At $\pi=0.7$ and $b=2$,
$\pi\delta=0.171<y_1=0.289$, so the count holds there too.

Numbers at $b=2$, with $c_H$ at the window midpoint (Section 5.6): at $\pi=0.3$ coexistence holds on
$[1.350533,1.605847]$; at $\pi=0.7$ it holds on $[1.622456,2.044127]$.

### Result 10. Presence probability (analytical)

All results hold with $s\in[0,\lambda]$. Presence enters only as a cap on the purchase rate.

- It shrinks the attainable range: $\mu_+(\lambda)<M_1(\pi)$ for $\lambda<1$.
- Recruitment under full purchases at $r$ needs $\lambda\ge s^*(r)$. At $r_1=3$ in the benchmark this
  is $\lambda\ge0.631455$. At $\lambda=0.5$ entry at $r_1$ stays at $\rho$, and the ceiling falls to
  $r_C=2.572$.
- The no-trade boundary $r_N$ does not depend on $\lambda$. Nor do $r_I$ and $r_U$, while $s^*<\lambda$.
  The boundaries $r_F$ and $r_C$ do depend on $\lambda$.

This differs from the three-point model. There the top flow reveals class $H$ for every $\lambda>0$, so
presence never blocks recruitment (prior memo `Q2_discrete_buy_only.md`, Claim 12).

### Result 11. General value classes $G_j$ (analytical corollary)

Under Reading N with class distributions $G_j$, the auction objects become class averages $t_j$ and
$g_j$. The prior memo `Q1_N_main.md` gives them (Claim 2), and the prior synthesis confirmed them
(rows 1–3). The
trading stage uses the auction only through $\Delta_T$, $w_L$, $g_L\ge0$ and $g_H-g_L$. So Results 1–10
hold verbatim if $\Delta_T>0$ and $g_H>g_L$. Three points need care.

1. *Cross-economy steps.* (A3-DL) is stated in $\Delta_T(r_0)$ and $\Delta_T(r_1)$ directly, so parts
   (i)–(ii) need no monotonicity. Part (iii) needs $\Delta_T(r_2)\ge\Delta_T(r_1)$, or a direct check.
   That holds under FOSD above the reserve with equal admissibility (`Q1_N_main.md`, Claim 4). The fall of
   $B_r$ in $r$ holds for every $G_j$ (same claim, part (a)).
2. *Ownership.* $\mathsf O_H=\pi e_HW_H(r)$, with $W_H(r)=\mathbb E_H[F_r(\theta)\mathbf 1\{\theta\ge p\}]$.
   Higher ownership at $r_1$ needs the ownership condition $e_H(r_1)W_H(r_1)>\rho W_H(r_0)$. It is not
   automatic, because $W_H$ can fall with $r$.
3. *The split identity.* With equal admissibility, $\Delta_T+(g_H-g_L)=\mathbb E_H\max\{\theta,p\}-\mathbb
   E_L\max\{\theta,p\}$ at every $r$ (`Q1_N_main.md`, Claim 3). Here the trading payoff is proportional
   to $\Delta_T$, and the recruitment threshold $\tau$ depends on $g_H-g_L$. A stronger incumbent moves
   value from the second to the first. So it raises trading and makes recruitment harder through the
   same moved value.

### Result 12. Robustness to the noise law (analytical)

**(a) Every positive noise law on the integers.** Every flow is on path. Under no trade
both classes have the same flow law, so every posterior equals the prior. A deviation reaches only
on-path flows. So $K_0=\rho(1-\pi)\Delta_T$, and $r_N=\mathfrak r(k/(\rho(1-\pi)))$, for every such law.
Also, class $L$ never buys and prices are sufficient (Result 2(a)–(b) use no noise property).

**(b) Laws with a bounded one-step ratio.** Suppose $f(x-1)/f(x)\in[\bar R^{-1},\bar R]$ at
every flow. Then every posterior lies in $[\frac{\pi}{\pi+(1-\pi)\bar R},\frac{\pi\bar R}{\pi\bar R+1-\pi}]$.
The upper end $\bar\mu$ gives $K\ge\rho(1-\bar\mu)\Delta_T$, and $K\le\Delta_T$ always. So the
Proposition 2 pattern holds with the paper-type window $\Delta_T(r_0)<k<\rho(1-\bar\mu)\Delta_T(r_1)$. Recruitment at
$r_1$ needs a positive-probability set of flows with posterior above $\tau$. The ceiling sits at the
largest attained posterior.

**(c) What needs exactly geometric tails.** By Result 1(g), the two-value posteriors need
the two-sided geometric law. So do the closed forms for $K$, $s^*$, $\zeta^*$, $r_F$, $r_C$ and the
outcome count in Result 6(b).

**(d) Coexistence survives small perturbations.** Let $\tilde f$ satisfy
$\sup_x|\log\tilde R(x)-\log R(x)|\le\varepsilon$ for the one-step ratios. Under full purchases the
posterior at $x$ has logit $\operatorname{logit}\pi+\log\tilde R(x)$, so it moves by at most $\varepsilon$
in logit. If $B_r(\mu_\pm)\ne c_H$, small $\varepsilon$ leaves entry unchanged at every flow. Also
$\tilde f(x)/f(x)\le e^{\varepsilon|x|}$ up to normalization, so $\tilde f\to f$ in $\ell^1$ for
$\varepsilon<1/(2b)$ by dominated convergence. Hence $\tilde K_F\to K_F$, while $K_0$ is unchanged by
(a). So $K_0\le k<K_F$ persists for small $\varepsilon$, and both no trade and full purchases remain
equilibria. $\square$

### Result 12A. Other noise laws at the benchmark (numerical diagnostic)

Script `extras.py` (Section 5.7) tests three other laws at the benchmark:
$a^{|z|}(1+0.1\cos z)$, $a^{|z|}(1+0.3\cos z)$, and a discretized Gaussian law with the same variance
$2a/(1-a)^2=7.835$.

- In all three, $K_0=\rho\Delta_T/2$ exactly, and no trade and full purchases coexist at $r=1.6$.
- The perturbed laws spread the posteriors inside each half-line. Then the good-news flows switch at
  different rates, and extra mixed outcomes appear.
- The ceiling moves out. With the 10% perturbation, entry under full purchases is still $0.553$ at
  $r=4.2$.
- Under the Gaussian law the one-step ratio is unbounded and posteriors approach 0 and 1. The ceiling
  then moves to $g_H(r)=c_H$: entry is still $0.255>\rho$ at $r=6$.

### Result 13. Verdicts on the claims of brief §0

| Claim in brief §0 | Verdict | Evidence |
|---|---|---|
| Posteriors take two values in $[0.378,0.622]$, $m_1=1/(1+e^{1/b})$ | confirmed | Result 1(b), (d) |
| Every flow on path; no refinement needed | confirmed | Result 1(c); Section 2.4 |
| Unique no trade at $r_0=1.2$ because $k>\Delta_T(r_0)$ | confirmed, with a sharper bound | the schedule-free bound is $k>\Delta_T(r_0)/2=0.008333$ (Result 3(a)) |
| Unique full buying at $r_1=3$ because $k<\rho m_1\Delta_T(r_1)=0.063$ | confirmed, not sharp | $0.062923$ is valid; the sharp schedule-free bound is $2\rho\gamma(1-\gamma)\Delta_T=0.078335$ (Result 3(b)) |
| Entry $0.25\to0.625\to0.25$ at $1.2,3,4.2$ | confirmed | Result 4; $r_C=3.986097$ |
| High-class ownership $0.125\to0.358$ | confirmed | $0.358422=\frac12[\rho+(1-\rho)/(1+a)]$ |
| Admissible $c_H$ window $(4.80,5.31]$ | confirmed for parts (i)–(ii), refined | part (iii) at $r_2=4.2$ also needs $c_H>4.932612$, so the window for all three parts is $(4.932612,5.312161]$; the right end needs (C1) |
| Entry returns near $r\approx4$; information ceiling restored | confirmed | $r_C=3.986097$ |
| Feedback at $r_1$: $+0.176$ with entry after good news | confirmed | $0.175836$ |
| Feedback at $r_1$: $+0.060$ without entry after good news | **refuted** (rounding) | the exact value is $2\rho\gamma(1-\gamma)\Delta_T-k=0.058335$, as the coordinator found |
| A Proposition 3 analog may exist, possibly analytic | confirmed, and extended | Result 6: analytical coexistence on $[r_F,r_N]$ (open at $r_F$ under (I0)), plus a third outcome with challenger mixing |
| The coordinator's rough argument for coexistence near $r=1.6$ | confirmed | Result 6(a); $K_0=0.014063\le0.02<K_F=0.033047$ at $r=1.6$ |

Also useful: $c_H\in(5.121880,5.312161]$, for example $c_H=5.2$, reproduces the paper's own strengths
$(1.2,3,3.6)$ (Section 5.5).

## 4. What it recovers or loses

Comparison with the Laplace paper (pinned commit) and the three-point model (brief §0; prior memos
`Q2_discrete_buy_only.md` and `SYNTHESIS.md`, Part B.2). Numbers use each model's benchmark. The three-point
numbers use $c_H=6$ unless stated.

| Object | Laplace paper | Three-point model | Discrete-Laplace (this memo) | Verdict |
|---|---|---|---|---|
| Prop. 1, eq. (4), auction stage | — | unchanged | unchanged | survives |
| Posterior bounds (7)–(8), Prop. A.1 | $[m,M]$, $m=1/(1+e^{2/b})$ | none; posteriors reach 0 and 1 | $[m_1(\pi),M_1(\pi)]$, $m_1=1/(1+e^{1/b})$ | **recovered** |
| Off-path flows and beliefs | none | one (flow 2 under no trade); Intuitive-Criterion completion | none | **recovered** |
| Price sufficiency, Prop. A.2 | under the floor | under $c_L<g_L$ | under $c_L=0$ | survives |
| Residual bounds, eq. (11) | pointwise $\rho m\Delta_T\le A\le\Delta_T$ | lower bound fails at revealing flows | pointwise $\rho m_1\Delta_T$; sharp averages $\rho\Lambda\Delta_T\le K\le(1-\pi)\Delta_T$ | recovered, sharper |
| Global order bound (A.6) | derivative bound, factor $1-1/b$ | one comparison $K-k$ | one comparison $K-k$, closed form | simpler |
| Prop. 2 (i)–(ii) | analytical | analytical, cutoff $\rho\Delta_T/3$ | analytical, (A2-DL)–(A3-DL) | survives |
| Prop. 2 (iii), ceiling | $B_r(M)<c_H$; $r_C=3.593$ | $g_H(r)<c_H$; $r=7.97$ ($c_H=6$), $9.97$ ($c_H=5$) | $B_r(M_1)<c_H$; $r_C=3.986$ | **recovered** |
| Entry and ownership at $r_1$ | $0.522757$, $0.324192$ | $0.375$, $0.25$ ($c_L=0.02$ variant) | $0.625$, $0.358422$ | larger effect |
| Closed forms, eq. (12) | Laplace tails | finite sums | $\mathsf E_1=(1+\rho)/2$ at $\pi=1/2$ | simpler |
| No-trade existence boundary | $r_N=\mathfrak r(2k/\rho)=1.747878$ | $\mathfrak r(3k/\rho)=1.973212$ | $\mathfrak r(2k/\rho)=1.747878$ | **recovered exactly** |
| Sufficient bounds of Prop. A.4 | $\mathfrak r(k)=1.221$, $r_U=2.837$ | one cutoff | $\mathfrak r(2k)=1.326$, $\mathfrak r(k/\rho\Lambda)=1.778$ | survives, tighter |
| Prop. 3, coexistence with no trade | computer-assisted at three strengths | none at equal noise | analytical on $[1.4433,1.7479]$, which contains $1.55,1.60,1.65$ | **recovered, stronger status** |
| Feedback from entry to trading | yes | none at equal noise | $K_F/K_0=2.35$ at $r_1$ | **recovered** |
| Mixed equilibria | numerical diagnostic (a mixed candidate) | a continuum at the cutoff only | closed form: $\tilde s$, $s^*$ with $\zeta^*$, $\hat s$ | new, analytical |
| Entry order across coexisting outcomes | no trade below the informative outcome | — | strict: no trade $<s^*<$ full | sharper |
| Entry order across strengths, on informative branches that coexist with no trade | strictly upward on a partial-sale family (certified) | — | strictly upward on the partial-purchase branch $\hat s$ just below $r_F$ (its left end $r_I$ is numerical); flat on the full branch; falls on $s^*$ | partly recovered |
| Trading asymmetry $(1,-v)$ | yes | not applicable (buy-only) | not applicable (buy-only); see C1 | not applicable |
| Prop. A.3, fixed experiment | strict fall $0.562\to0.523$ | weak, survives | weak; one jump at $r_C$; flat $0.625$ at $r_0$ and $r_1$ | **weakened** |
| Price-hidden control | entry $\rho$ | entry $\rho$ | entry $\rho$ | survives |
| Prop. A.9, access to prices | $\Delta\mathcal R_T=0.257809$ | not computed | $\Delta\mathcal R_T=0.327490$, $\Delta\mathcal W=0.148310$ | survives |
| Investor profit, with and without access | $0.1407$ vs $0.0691$ (prior memo `Q3_welfare.md`, two-sided) | zero residual at the recruiting flow | $0.097918$ vs $0.039167$ | survives |
| Smooth comparative statics in $r$ | yes | no | no; the entry path is a step function | lost |
| Existence under the zero-at-indifference rule | not used | can fail (unequal noise) | can fail, exactly when $K_F\le k<K_0$; not at the benchmark | caveat |
| General prior | prior memo `Q1_N_main.md`, Claim 10 | cutoff $\frac23\rho(1-\pi)\Delta_T$ | all closed forms in $\pi$; U-shape for $\pi>1/2$ | survives |
| Presence $\lambda$ | not in the paper | does not move the cutoff | does not move $r_N$; small $\lambda$ blocks recruitment | changes |
| Value classes $G_j$ | prior memo `Q1_N_main.md` | — | corollary, with the ownership condition | survives |
| Robustness to the noise law | class $\lvert(\log f)'\rvert\le L<1$ | equal noise is a knife edge | closed forms need geometric tails; coexistence and $r_N$ are robust | partly robust |
| Prop. A.5, Section 5.1: other noise laws | logistic; class $\lvert(\log f)'\rvert\le1/b$ | — | class analog: a bounded one-step ratio $\bar R$ (Result 12(b)); exact forms need geometric tails | survives in class form |
| Prop. A.10: zero-entry price pools | pools where the floor fails | pools without the floor | cannot arise: $c_L=0$ gives entry at least $\rho$ at every price | not applicable |
| Props. A.6–A.7; Sections 5.3, 6.3 | — | — | not studied | open |
| Prop. A.8 (bargaining) | — | — | auction stage only, so unchanged | survives |

**In words.** The discrete-Laplace model recovers five things that the three-point model lost:

- interior posteriors;
- no off-path beliefs;
- the early information ceiling;
- the paper's exact no-trade boundary;
- feedback from entry to trading.

It even upgrades Proposition 3 from computer-assisted to analytical. It also keeps the sequence of the
paper's Figure 2 (Result 6, analytical in local form). A partial informative family with rising entry
comes first. Full orders that coexist with no trade come next. No trade ends at $r_N$. The model loses
smoothness.
Posteriors take two values, so entry moves in steps. Fixed-experiment deterrence becomes a single jump.
Rising entry across strengths survives only on a short mixed branch, not at the paper's three
strengths. Buy-only orders also rule out the paper's trading asymmetry.

## 5. Numerical example

### 5.1 Benchmark constants (computer-assisted)

At $b=2$: $a=0.606531$, $\gamma=M_1=0.622459$, $1-\gamma=m_1=0.377541$, $\delta=0.244919$,
$\gamma(1-\gamma)=0.235004$ and $\Lambda=0.470007$.

Interval enclosures (`certify.py`, width below $10^{-49}$) give these strict margins:

- (A2-DL): $c_H-B_{1.2}(1/2)=0.195833$ and $B_3(M_1)-c_H=0.312161$;
- part (iii): $c_H-B_{4.2}(M_1)=0.067388$;
- (A3-DL): $k-\Delta_T(1.2)/2=0.011667$ and $\rho\Lambda\Delta_T(3)-k=0.058335$.

Thresholds: $\mathfrak r(2k)=1.325657$, $r_F=1.443322$, $r_N=1.747878$, $\mathfrak r(k/\rho\Lambda)=1.777986$ and
$r_C=3.986097$ (analytical). $r_I=1.405430$ and $r_U=1.762507$ (numerical diagnostic).

### 5.2 Table 2 analog

Benchmark of this memo against the paper's Table 2 (the paper uses two-sided orders, $c_L=1$ and
$c_H=6$).

| Row | Orders | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | Paper: $\mathsf E$, $\mathsf O_H$, $\mathcal R_T$ |
|---|---|---|---|---|---|
| A. weak, $r=1.2$ | $(0,0)$ | 0.250000 | 0.125000 | 0.392708 | 0.250000, 0.125000, 0.392708 |
| A. strong, $r=3$ | $(1,0)$ | 0.625000 | 0.358422 | 0.942073 | 0.522757, 0.324192, 0.872392 |
| A. very strong, $r=4.2$ (paper: 3.6) | $(1,0)$ | 0.250000 | 0.125000 | 0.710417 | 0.250000, 0.125000, 0.664236 |
| B. frozen full orders, $r=1.2$ | $(1,0)$ | 0.625000 | 0.358422 | 0.545036 | 0.562178, 0.350606, 0.520039 |
| B. frozen full orders, $r=3$ | $(1,0)$ | 0.625000 | 0.358422 | 0.942073 | 0.522757, 0.324192, 0.872392 |
| B. price hidden, $r=1.2$ | $(0,0)$ | 0.250000 | 0.125000 | 0.392708 | 0.250000, 0.125000, 0.392708 |
| B. price hidden, $r=3$ | $(1,0)$ | 0.250000 | 0.125000 | 0.614583 | 0.250000, 0.125000, 0.614583 |

Panel C, access to prices at $r=3$:

| Quantity | Price observed | Price hidden | Gain | Paper's gain |
|---|---|---|---|---|
| Target proceeds $\mathcal R_T$ | 0.942073 | 0.614583 | 0.327490 | 0.257809 |
| Net acquisition surplus $\mathcal W$ ($c_L=0$, $c_H=5$) | 2.700394 | 2.552083 | 0.148310 | 0.080218 |
| Investor gross profit | 0.097918 | 0.039167 | 0.058751 | — |
| Investor net profit | 0.087918 | 0.029167 | 0.058751 | — |

The $\mathcal W$ levels and gains are not comparable with the paper's, because $c_L$ and $c_H$ differ.
The rows with entry $\rho$ have the paper's proceeds exactly, because $c_L$ does not enter proceeds.

### 5.3 The three coexisting outcomes at the paper's Proposition 3 strengths

| $r$ | Outcome | $s$ | $\zeta^*$ | $\mathsf E$ | $\mathsf O_H$ | $\mathcal R_T$ | Paper's certified $\mathsf E$ |
|---|---|---|---|---|---|---|---|
| 1.55 | no trade | 0 | — | 0.250000 | 0.125000 | 0.455746 | |
| 1.55 | mixed at $s^*$ | 0.228270 | 0.382383 | 0.366291 | 0.187154 | 0.510578 | 0.545053 |
| 1.55 | full purchases | 1 | — | 0.625000 | 0.358422 | 0.635782 | |
| 1.60 | no trade | 0 | — | 0.250000 | 0.125000 | 0.463281 | |
| 1.60 | mixed at $s^*$ | 0.240749 | 0.258954 | 0.329050 | 0.167388 | 0.501399 | 0.548756 |
| 1.60 | full purchases | 1 | — | 0.625000 | 0.358422 | 0.647744 | |
| 1.65 | no trade | 0 | — | 0.250000 | 0.125000 | 0.470549 | |
| 1.65 | mixed at $s^*$ | 0.253260 | 0.160614 | 0.299215 | 0.151475 | 0.494818 | 0.551361 |
| 1.65 | full purchases | 1 | — | 0.625000 | 0.358422 | 0.659525 | |

The paper's informative outcomes are partial sales $(1,-v_j)$. They have no exact counterpart under
buy-only orders. Two more points show the other regions: at $r=1.42$, $\hat s=0.471$ with entry $0.576$;
at $r=1.75$, $\tilde s=0.0356$ with entry $\rho$.

### 5.4 Margins at $r=1.6$ (computer-assisted)

$k-K_0=0.005938$, $K_F-k=0.013047$, $B_{1.6}(M_1)-c_H=0.766482$ and $c_H-B_{1.6}(1/2)=0.321875$. All four
are certified positive by interval arithmetic. The same holds at $1.55$ and $1.65$.

### 5.5 Variant $c_H=5.2$ with the paper's strengths $(1.2,3,3.6)$

The window for all three parts is $(5.121880,5.312161]$. At $c_H=5.2$: $r_C=3.353187$, so entry is
$0.25\to0.625\to0.25$ at $(1.2,3,3.6)$. Proceeds are $0.392708$, $0.942073$ and $0.664236$; the last
equals the paper's $r_2$ value. Coexistence holds on $[1.443322,1.747878]$, as before.
$\Delta\mathcal W=0.073310$ at $r=3$.

### 5.6 Prior, presence and noise scale

| Case | $c_H$ | $c_H$ window | $k$ window | $[r_F,r_N]$ | $r_C$ | $\mathsf E_1$ | $\mathsf O_{H,1}$ |
|---|---|---|---|---|---|---|---|
| $\pi=0.3$ | 3.291408 | $(3.0075,3.575315)$ | $(0.011667,0.110731)$ | $[1.350533,1.605847]$ | 4.290074 | 0.588262 | 0.215053 |
| $\pi=0.5$ | 5 | $(4.804167,5.312161)$ | $(0.008333,0.078335)$ | $[1.443322,1.747878]$ | 3.986097 | 0.625000 | 0.358422 |
| $\pi=0.7$ | 6.669948 | $(6.600833,6.739063)$ | $(0.005000,0.047001)$ | $[1.622456,2.044127]$ | 3.175173 | 0.661738 | 0.501791 |
| $\lambda=0.8$ | 5 | $(4.804167,5.150112)$ | — | $[1.435192,1.747878]$ | 3.486535 | 0.606631 | 0.340053 |

In the $\lambda=0.8$ row the upper end of the $c_H$ window is $B_3(\mu_+(0.8))$ with $\mu_+(0.8)=0.603013$.

Noise scale at $\pi=1/2$, $r_0=1.2$, $r_1=3$: the upper end of the $c_H$ window, $B_3(M_1)$, is
$6.217$, $5.631$, $5.312$, $4.980$ and $4.810$ at $b=1,1.5,2,3,4$. The window closes at $b=4.0445$. The
upper end of the $k$ window, $\rho\Lambda\Delta_T(3)$, is $0.0655$, $0.0747$, $0.0783$, $0.0811$ and
$0.0820$. So less noise widens the $c_H$ window but narrows the $k$ window.

### 5.7 Scripts and checks

All scripts print only; none asserts. Run from the repository root. Outputs are saved as `.out` files.

| Script | What it does | Status of its evidence |
|---|---|---|
| `closed_forms.py` | auction objects by quadrature; noise law by convolution; posteriors and $K$ by direct flow sums vs closed forms (50 digits) | computer-assisted check |
| `benchmark.py` | thresholds, the equilibrium set at each strength, the Table 2 analog, the general prior, presence, $c_H=5.2$, the deterrence case (50 digits) | evaluation of analytical formulas |
| `certify.py` | interval enclosures of every benchmark margin | computer-assisted |
| `correspondence.py` | brute force: direct flow sums over $\lvert x\rvert\le90$, 2001 rates, bisection at sign changes and entry switches; compared with the analytic classification at 2000 strengths, for six parameter sets | numerical diagnostic |
| `extras.py` | the two-root example at $\pi=0.7$; other noise laws | numerical diagnostic |

*Truncation.* The theory has no truncation, because the half-line sums are exact (Result 1(e)). The
brute force truncates at $\lvert x\rvert\le90$; the omitted noise mass is $2a^{91}/(1+a)=2.1\times10^{-20}$,
below double precision. The 50-digit checks use $\lvert x\rvert\le320$, with omitted mass
$2.5\times10^{-70}$.

Results of `correspondence.py` (run through the slot wrapper; about eight minutes):

- **zero mismatches** between brute force and the analytic list, at all 2000 strengths. The six sets
  are the benchmark, $c_H=5.2$, $\pi=0.3$, $\pi=0.7$, $\lambda=0.8$, and a no-feedback case
  ($\rho=0.95$, $k=0.3$);
- the largest difference in $s$ is $1.2\times10^{-14}$;
- the entry-switch points of all good-news flows coincide to $3.8\times10^{-15}$. This confirms
  Result 1 without using it;
- the first grid points of the regions are $1.4075$, $1.4450$, $1.7500$ and $1.7650$. These match $r_I$,
  $r_F$, $r_N$ and $r_U$;
- in the no-feedback case, rule (I0) leaves no equilibrium on $[2.9225,2.9750)$, as Result 5 predicts.

### 5.8 Comparison with the numerical memo B1

I read B1 (`memos/B_dlaplace_numeric.md`) after this memo was complete. B1 derives the model by its own
route: class masses for asymmetric geometric counts, a quadratic for every interior root, and 60-digit
arithmetic. B1 could compare only my skeleton. The table compares the two final memos.

| Item | B1 | This memo | Verdict |
|---|---|---|---|
| Half-line reduction; posteriors; every flow on path | analytical, also for $a_+\ne a_-$ | Result 1; asymmetric rates as a remark | agree |
| $\beta_L=0$; price sufficiency; purchase payoff | its eqs. (1) and (8) | Result 2 | agree; same formula with $d=s$ |
| Unique no trade at $r_0$ | bound $\Delta_T(r_0)<k$ | sharper bound $(1-\pi)\Delta_T(r_0)<k$ | agree; mine is sharper |
| Unique full buying at $r_1$ | bound $\rho(1-M_1)\Delta_T(3)=0.062923>k$ | sharper bound $\rho\Lambda\Delta_T(3)=0.078335>k$ | agree; mine is sharper |
| Exact $k$ region for the three outcomes, (IM, CM) | $(0.005770,0.078978)$ | the same (Result 4) | agree |
| $c_H$ windows | $(4.804167,5.312161]$; $(4.932612,5.312161]$ with the return at $4.2$ | the same | agree |
| $r_C$, entry and ownership | $3.986097$, $0.625$, $0.358422$ | the same | agree |
| Feedback figures | $0.175836$ and $0.058335$; the brief's $0.060$ is wrong | the same | agree |
| Coexistence set | $[r_F,r_N]$ under ordinary indifference; $(r_F,r_N]$ under (I0) | the same, after I fixed the endpoint | agree |
| Branch boundaries | $r_S,r_F,r_N,r_Q=1.405430,1.443322,1.747878,1.762507$ | $r_I,r_F,r_N,r_U$: the same values | agree; both memos label $r_S=r_I$ and $r_Q=r_U$ as numerical |
| Branch outcomes at $r=1.42,1.60,1.75$ | for example $T$ at $1.60$: $\beta_H=0.240749$, $\mathsf E=0.329050$ | the same to every printed digit | agree |
| Rising entry on the recruiting mixed branch | numerical: $0.558559,0.576414,0.595797$ | the same numbers; now proved (Result 6) | agree; B1 found it, and I had wrongly called the order lost |
| Net surplus $\mathcal W$ at $r=3$ | subtracts the trading cost $\pi\lambda k$: $2.690394$ vs $2.542083$ | the paper's convention, preparation costs only: $2.700394$ vs $2.552083$ | levels differ by $0.01$ by convention; gains agree ($0.148310$) |
| Proposition A.3 analog | weak fall at every fixed experiment | the same, plus the step form | agree |
| Atomless costs (A.6) | local persistence for narrow cost supports | open | B1 goes further |
| Asymmetric noise | an explicit region $0.5845<a_+<0.7094$, any $a_-$ | a remark only | B1 goes further |
| General prior | the $c_H$ window is nonempty for $0.0428<\pi<0.7525$ | windows at $\pi=0.3$ and $0.7$ | consistent |
| Non-geometric noise | not studied | Result 12 | this memo goes further |
| Access can deter when the prior recruits | not studied | Result 8 | this memo goes further |

No substantive disagreement remains. The comparison corrected one claim of mine: the upward order of
entry across strengths survives on the recruiting mixed branch (Result 6).

## 6. Open issues

1. **Single crossing of $r_I$ and $r_U$ (open).** The fixed-$r$ classification is analytical. The
   claim that each region in $r$ is an interval rests on a grid (numerical diagnostic).
2. **Two-sided orders (open here).** Buy-only orders exclude the paper's asymmetry $(1,-v)$.
   Workstream C1 studies geometric-count noise with orders $\{-1,0,1\}$.
3. **Atomless preparation costs (Prop. A.6 analog; open).** With a continuous cost law, entry would be
   continuous in $\mu$. The jump at $s^*$ and the challenger-mixing outcome would then become an
   ordinary interior root. I expect coexistence to survive (conjecture).
4. **Complementary private information, bargaining with trading, reserve comparisons (open).** I did
   not study Sections 5.3 and 6.3 or Props. A.6–A.7. Nor did I study the trading continuation of
   Section 6.2. Result 12(b) covers the class part of Prop. A.5. The pools of Prop. A.10 cannot arise
   here.
5. **Selection among the three outcomes (open).** Result 6(d) shows that the middle outcome is
   unstable under myopic adjustment. A formal selection argument is not given.
6. **Exact count for other noise laws (conjecture).** Result 12(d) proves that coexistence survives
   small perturbations. The diagnostic in Result 12A shows extra mixed outcomes. I conjecture that
   their number grows with the spread of posteriors inside each half-line.
7. **Prior above one half (partly open).** Result 5 gives every root through quadratics, but I did not
   tabulate the full correspondence for $\pi>1/2$.

## 7. Plain summary

In this model the noise is the difference of two independent geometric counts. Then every order flow
is possible, and the market only learns whether the flow is positive. So the price takes two values,
and beliefs stay between $0.378$ and $0.622$ at the benchmark. No belief is ever off path, so no
refinement is needed.

The paper's main result holds with a short proof. A weak incumbent gives no trade and entry $0.25$. A
strong incumbent gives informed buying after good news. The high price after good news then recruits
the expensive challenger, and entry rises to $0.625$. A very strong incumbent keeps the buying, but even
good news cannot justify expensive preparation, so entry returns to $0.25$ above $r=3.986$. Each step
uses one comparison: the purchase payoff against the trading cost. Its sharp bounds are $(1/2)\Delta_T$
and $0.47\rho\Delta_T$ at the benchmark.

The coexistence result also holds, and now with a full proof. Recruited entry raises the investor's
profit from buying by a factor of $2.35$. So for strengths between $1.443$ and $1.748$, no trade and
full buying are both equilibria. This interval contains the paper's three certified points.
When indifferent players may mix, a third outcome lies between them, with the expensive challenger
mixing. Entry rises strictly from no trade to the mixed outcome to full buying.

Price access raises proceeds by $0.327$ and net surplus by $0.148$ at $r=3$. It also raises the
investor's profit, which liquidity traders pay.

The costs: entry moves in steps, not smoothly. A fixed experiment deters only by one jump. Entry rises
with strength only on a short mixed branch just before the coexistence interval. Buy-only orders give no
trading asymmetry. The exact formulas need exactly geometric noise, but coexistence and the no-trade boundary
survive small changes in the noise law.
