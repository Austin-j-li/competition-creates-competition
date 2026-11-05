# Point 1, Reading N (main line): nature draws the challenger's value distribution

Research memo to the author, 21 October 2026.
Script (print-only): `audit/alex_meeting_2026_10_21/scripts/Q1_N_main/reading_n_main.py`.
Run it from the repository root with `.venv/bin/python <path>`; it takes about one second.

Equation numbers (N1)–(N13) are local to this memo. Numbers without "N" refer to the paper
(`overleaf/paper/main.tex`).

---

## 1. Question and reading

The supervisor finds the binary challenger value with prior 1/2 unconventional. He suggests a model
in which the challenger "ends up" in one of a few value distributions and learns which one only when
it receives information. He asks whether a clear, neat result follows.

This memo uses **Reading N**. Nature draws the challenger's type $j\in\{H,L\}$ with prior
$\pi=\Pr(j=H)\in(0,1)$. Given $j$, the value $\theta$ has cdf $G_j$. Before preparation, the
challenger knows neither $j$ nor $\theta$. The investor observes $j$, not $\theta$. Preparation
reveals $\theta$. The incumbent has a general continuous cdf $F$; the uniform cdf $F_r$ on $[0,r]$
is the leading case. The supports of $G_H$ and $G_L$ can overlap, and they can include values below
the reserve $p$.

Two special cases are already in the paper:

- the benchmark: $G_H=\delta_h$, $G_L=\delta_\ell$, $\pi=1/2$;
- the value classes of Section 6.3 and OA.52: $G_H$ uniform on $[h-\varepsilon_V,h+\varepsilon_V]$,
  $G_L$ uniform on $[\ell-\varepsilon_V,\ell+\varepsilon_V]$, $\pi=1/2$.

So the question is not whether Reading N fits the paper. The questions are: which results hold for
every pair $(G_H,G_L)$ and every prior, and which new effects appear.

---

## 2. Formal setup

All assumptions of Sections 2.2–2.4 of the paper hold, except for the challenger's value.

1. **Incumbent.** Its value $R$ has a continuous cdf $F$ on $[0,\bar r]$, with $F(u)=1$ for
   $u\ge\bar r$. Continuity makes the events $R=\theta$ and $R=p$ null.
2. **Challenger.** Its type is $j\in\{H,L\}$ with $\Pr(j=H)=\pi$. Given $j$, $\theta\sim G_j$, a cdf
   on $[0,\infty)$ with a finite mean. Atoms are allowed. $G_j(u^-)=\Pr_j(\theta<u)$.
3. **Independence.** $(j,\theta)$, $R$, the cost $C$, and the noise $Z$ are independent. The value
   $\theta$ depends on the order flow only through $j$.
4. **Sale.** Cash second-price auction with reserve $p>0$. A bid equal to $p$ is admissible. A
   prepared challenger with $\theta<p$ cannot win at a profit, so it does not bid.
5. **Costs, trading, prices.** As in the paper: $C\in\{c_L,c_H\}$ with $\Pr(C=c_L)=\rho$, learned
   after the price; orders $q\in[-1,1]$ with cost $k\lvert q\rvert$; Laplace noise with scale
   $b>1$; competitive price $P(X)=\mathbb E[V_T\mid X]$. The challenger sees the price and its cost.
   A belief is $\mu=\Pr(j=H\mid\cdot)$.

**Notation.**

- $D(u)=G_L(u)-G_H(u)$ is the gap between the type cdfs.
- $D(p^-)=G_L(p^-)-G_H(p^-)$ is how much more likely the L type is to have a value below the
  reserve. I call a value below $p$ **inadmissible**.
- $\hat\theta=\max\{\theta,p\}$.
- **FOSD above the reserve:** $D(u)\ge0$ for almost every $u>p$.
  **Equal admissibility:** $D(p^-)=0$.

**Auction objects.** For a known challenger value $\theta$, $t(\theta)$ is the expected target
proceeds after the challenger prepares, and $g(\theta)$ is its expected gross profit. Then $t_0$ is
the proceeds without entry, $t_j=\mathbb E_j[t(\theta)]$, $g_j=\mathbb E_j[g(\theta)]$,
$\Delta_T=t_H-t_L$, $B_F(\mu)=g_L+\mu(g_H-g_L)$, and
$W_j=\Pr_j(\text{a prepared challenger wins})=\mathbb E_j[F(\theta)\mathbf 1\{\theta\ge p\}]$.

**Outcome measures.** Entry $\mathsf E$ is the preparation probability, as in the paper.
**Type-H ownership** $\mathsf O_H=\pi e_HW_H$ is the probability that a type-H challenger acquires the
target; in the benchmark $W_H=1$, so $\mathsf O_H=e_H/2$, as in eq. (12). I also report the
probability of an admissible prepared challenger,
$\mathsf A=\pi e_H[1-G_H(p^-)]+(1-\pi)e_L[1-G_L(p^-)]$.

---

## 3. Results

### Claim 1 (proceeds and profit at a known value; analytical)

For $\theta\ge p$,

$$
t(\theta)=p+\int_p^\theta[1-F(u)]\,du,\qquad g(\theta)=\int_p^\theta F(u)\,du.
\qquad\text{(N1)}
$$

For $\theta<p$, $t(\theta)=t_0=p[1-F(p)]$ and $g(\theta)=0$. Therefore:

- (a) $t$ **jumps up by $pF(p)$ at $\theta=p$**; $g$ is continuous there.
- (b) $t(\theta)+g(\theta)=\theta$ for every $\theta\ge p$.
- (c) $t$ and $g$ are nondecreasing, and $t(\theta)\ge t_0$ for every $\theta$.
- (d) For the uniform incumbent with $p\le r$: $t_0=p-p^2/r$, the jump is $p^2/r$, and for
  $\theta\ge p$

$$
t(\theta)=\frac r2+\frac{p^2}{2r}-\frac{(r-\theta)_+^2}{2r}.\qquad\text{(N2)}
$$

*Derivation.* OA.50 gives realized proceeds $\max\{p,\min(R,\theta)\}$ if $\theta\ge p$ and
$p\mathbf 1\{R\ge p\}$ if $\theta<p$. For $\theta\ge p$,
$\max\{p,\min(R,\theta)\}=p+\int_p^\theta\mathbf 1\{R>u\}\,du$, and the challenger's profit is
$(\theta-\max\{p,R\})_+=\int_p^\theta\mathbf 1\{R<u\}\,du$ (eq. A.2). Tonelli's theorem gives (N1).
The two indicators sum to one for almost every $u$, which gives (b). The jump is
$t(p)-t_0=p-p[1-F(p)]=pF(p)$. For (c), $t(\theta)\ge p\ge t_0$ when $\theta\ge p$. For (d),
integrate $1-u/r$: for $p\le\theta\le r$, $t=\theta-(\theta^2-p^2)/(2r)$, which equals (N2); for
$\theta\ge r$, $t=r/2+p^2/(2r)$. $\square$

*Reading.* The jump is an **admissibility premium**. If the incumbent fails the reserve ($R<p$), an
admissible challenger sells the target at $p$, but an inadmissible one leaves it unsold. Identity
(b) says that the second-price rule passes the challenger's whole value to the target and the
challenger together. If the challenger wins, $\theta$ splits into the payment and the rent. If it
loses, the incumbent pays $\theta$.

### Claim 2 (type payoffs, and a correction to the brief's check; analytical)

$$
t_j=t_0+pF(p)[1-G_j(p^-)]+\int_p^\infty[1-G_j(u)][1-F(u)]\,du,\qquad
g_j=\int_p^\infty[1-G_j(u)]\,F(u)\,du,\qquad\text{(N3)}
$$

$$
\Delta_T=pF(p)\,D(p^-)+\int_p^\infty[1-F(u)]\,D(u)\,du,\qquad\text{(N4)}
$$

$$
g_H-g_L=\int_p^\infty F(u)\,D(u)\,du.\qquad\text{(N5)}
$$

*Derivation.* By Claim 1, for every $\theta$,
$t(\theta)=t_0+pF(p)\mathbf 1\{\theta\ge p\}+\int_p^\infty\mathbf 1\{u\le\theta\}[1-F(u)]\,du$ and
$g(\theta)=\int_p^\infty\mathbf 1\{u\le\theta\}F(u)\,du$. Take $\mathbb E_j$ and apply Tonelli:
$\mathbb E_j\mathbf 1\{\theta\ge p\}=1-G_j(p^-)$, and $\Pr_j(\theta\ge u)=1-G_j(u)$ for almost every
$u$. Subtract the two types. $\square$

*Check against the paper.* With $G_H=\delta_h$, $G_L=\delta_\ell$ and $p<\ell$, $D=\mathbf 1\{\ell\le
u<h\}$ and $D(p^-)=0$. Then (N4) is $\int_\ell^{\bar r}[1-F]$ and (N5) is $\int_\ell^hF$, as in
eq. (6). The script's values match eq. (4) and OA.52.

*Verdict on the brief's "discriminating check".*

- The spread form $\int[1-F(\theta)][G_L(\theta)-G_H(\theta)]\,d\theta$ is right only on
  $[p,\infty)$, and only after the point term $pF(p)D(p^-)$ is added. If neither type has mass below
  $p$, as in the benchmark, the brief's form holds. If the integral starts at $0$ and the types differ
  below $p$, the form is wrong. Example: if both types are always below $p$, then $\Delta_T=0$, but
  the brief's integral is not zero in general.
- The profit-gap form $\int\big(\int_p^\theta F\big)\,d(G_H-G_L)(\theta)$ is right only if the inner
  integral is zero for $\theta<p$, that is, $\int_p^{\max\{\theta,p\}}F$. Without that fix, the inner
  integral is negative below $p$. With the fix, integration by parts gives (N5).

*Uniform closed form.* For $p\le r$, (N2) and (N3) give

$$
\Delta_T(r)=D(p^-)\,\frac{(r-p)^2+2p^2}{2r}
+\frac{\mathbb E_L[(r-\theta)_+^2;\,\theta\ge p]-\mathbb E_H[(r-\theta)_+^2;\,\theta\ge p]}{2r}.
\qquad\text{(N6)}
$$

In the benchmark, (N6) is $(r-\ell)^2/(2r)$. With value classes, it is
$[(r-\ell)^2+\varepsilon_V^2/3]/(2r)$, which is OA.52. If $G_L$ lies in $[p,r]$ and $G_H$ lies above
$r$, then $\Delta_T(r)=[(r-\mathbb E_L\theta)^2+\operatorname{Var}_L\theta]/(2r)$.
(Derivation: $t_j=\Pr_j(\theta\ge p)[r/2+p^2/(2r)]-\mathbb E_j[(r-\theta)_+^2;\theta\ge p]/(2r)
+\Pr_j(\theta<p)(p-p^2/r)$; subtract, and note $r/2+p^2/(2r)-p+p^2/r=[(r-p)^2+2p^2]/(2r)$.)

### Claim 3 (the split of the value gap; analytical)

Add (N4) and (N5):

$$
\Delta_T+(g_H-g_L)=pF(p)\,D(p^-)+\int_p^\infty D(u)\,du.\qquad\text{(N7)}
$$

With equal admissibility, the right side equals $\mathbb E_H[\hat\theta]-\mathbb E_L[\hat\theta]$
and **does not depend on $F$**. In the benchmark it equals $h-\ell$ at every $r$:
$(r-\ell)^2/(2r)+h-r/2-p^2/(2r)-(\ell^2-p^2)/(2r)=h-\ell$. The paper states this only at $r=\ell$
(A.25).

*Kernel form.* For each incumbent value $R$, let $\varphi(R)$ be the difference in proceeds between
an H and an L challenger. Then $\Delta_T=\mathbb E_F[\varphi(R)]$, with

$$
\varphi(R)=
\begin{cases}
p\,D(p^-), & R<p,\\[3pt]
\displaystyle\int_p^R D(u)\,du=\mathbb E_H\big[\min\{\hat\theta,R\}\big]-\mathbb E_L\big[\min\{\hat\theta,R\}\big], & R\ge p.
\end{cases}
\qquad\text{(N8)}
$$

Likewise $g_j=\mathbb E_F[\gamma_j(R)]$ with $\gamma_j(R)=\mathbb E_j[(\theta-\max\{p,R\})_+]$, which
is nonincreasing in $R$ for every $G_j$.

*Derivation.* (N7) is the sum of (N4) and (N5), and
$\mathbb E_j\hat\theta=p+\int_p^\infty[1-G_j(u)]\,du$. For (N8): if $R\ge p$, the proceeds equal
$\min\{R,\hat\theta\}$ for every $\theta$. (If $\theta\ge p$, both $R$ and $\theta$ are at least $p$,
so $\max\{p,\min(R,\theta)\}=\min(R,\theta)$. If $\theta<p$, the incumbent pays $p=\min(R,p)$.)
Also $\mathbb E_j\min\{R,\hat\theta\}=p+\int_p^R[1-G_j(u)]\,du$. If $R<p$, the proceeds are
$p\mathbf 1\{\theta\ge p\}$. $\square$

*Reading.* Cut the value gap between the types into slices $D(u)\,du$, one at each value level
$u>p$. A slice goes to the target when the incumbent's value exceeds $u$ (probability $1-F(u)$),
because the incumbent then pays the challenger's bid. It goes to the challenger when the incumbent's
value is below $u$. **A stronger incumbent does not change the size of the gap. It moves every slice
from the challenger to the target.** The only exception is the admissibility slice $pD(p^-)$. It
reaches the target only when the incumbent fails the reserve, and a stronger incumbent fails it less
often.

### Claim 4 (generalized Proposition 1; analytical)

Let $\tilde F\le F$ pointwise (an FOSD strengthening), with both cdfs continuous.

- (a) **For every $G_H,G_L$**, $g_j(\tilde F)\le g_j(F)$ for $j=H,L$. Hence
  $B_{\tilde F}(\mu)\le B_F(\mu)$ at every belief. No ranking of the types is necessary. For type $j$
  the decrease is strict iff $\int_p^\infty[1-G_j][F-\tilde F]\,du>0$.
- (b) The spread changes by

$$
\Delta_T(\tilde F)-\Delta_T(F)=\int_p^\infty[F(u)-\tilde F(u)]\,D(u)\,du-p\,[F(p)-\tilde F(p)]\,D(p^-).
\qquad\text{(N9)}
$$

- (c) $\Delta_T$ weakly rises under every FOSD strengthening of every continuous $F$ **if and only
  if** $D\ge0$ a.e. on $(p,\infty)$ and $D(p^-)\le0$. If the types are FOSD-ranked ($D\ge0$
  everywhere), this holds iff $D(p^-)=0$. The shape of $G_j$ below $p$ is irrelevant; only the mass
  below $p$ matters.
- (d) Uniform family, $r>p$:

$$
\frac{d\Delta_T}{dr}=\frac1{r^2}\Big[\int_p^r u\,D(u)\,du-p^2D(p^-)\Big],\qquad
\frac{dg_j}{dr}=-\frac1{r^2}\int_p^r u\,[1-G_j(u)]\,du.\qquad\text{(N10)}
$$

  If $D\ge0$ on $(p,\infty)$, the bracket is nondecreasing in $r$, so $\Delta_T$ is quasi-convex in
  $r$. It falls on $(p,r^\ast)$ and rises above $r^\ast$, where $\int_p^{r^\ast}uD=p^2D(p^-)$. With
  $D(p^-)=0$, $\Delta_T$ is nondecreasing on $(p,\infty)$.
- (e) **The failure already occurs in the paper.** In Section 6.3 at $p=1.1>\ell+\varepsilon_V$,
  the low class is never admissible ($D(p^-)=1$), and (N6), or A.42, gives
  $\Delta_T(r)=r/2-p+3p^2/(2r)$ for $p\le r\le h-\varepsilon_V$. This falls on
  $(p,\sqrt3\,p)=(1.1,1.905)$. So $\Delta_T(1.2)=1.012500>\Delta_T(3)=1.005000$: a stronger
  incumbent lowers the spread between $r_0$ and $r_1$. Table 4 shows deterrence at that reserve
  (preparation 0.540309 to 0.511638). Proposition 1 assumes $p<\ell$, so it is correct as stated.
  But Section 6.3 could say why the reversal is absent at the high reserve.

*Proof.* (a) In $g_j(F)=\int_p^\infty[1-G_j]F$ the weight on $F$ is nonnegative. (b) Subtract (N4)
at the two cdfs. (c) Sufficiency: both terms of (N9) are nonnegative because $F-\tilde F\ge0$.
Necessity: by (N8), $\Delta_T(F)=\mathbb E_F\varphi(R)$. Suppose $\varphi(x_1)>\varphi(x_2)$ at
continuity points $x_1<x_2$. Let $F$ be uniform on $[x_1-\eta,x_1+\eta]$ and let $\tilde F$ move
that law to $x_2$. For small $\eta$, $\Delta_T(\tilde F)-\Delta_T(F)\to\varphi(x_2)-\varphi(x_1)<0$.
(If the incumbent's support must be $[0,\bar r]$, mix a small uniform component into both laws; the
sign does not change.) Now $\varphi$ is continuous on $(p,\infty)$ with derivative $D$ a.e., and
$\varphi(p^-)=pD(p^-)$, $\varphi(p)=0$. So $\varphi$ is nondecreasing iff $D\ge0$ a.e. above $p$ and
$pD(p^-)\le0$. (d) $-\partial_rF_r(u)=u/r^2$ on $[0,r)$ and $0$ above; differentiate (N4) and (N3)
under the integral. The bracket has derivative $rD(r)\ge0$. (e) Put $D(p^-)=1$ and no admissible
L mass into (N6); the H term vanishes because $G_H$ lies above $r$. $\square$

*When do supports below $p$ break the sign pattern?* Never for $g_H$, $g_L$ and $B$. For
$\Delta_T$, the pattern survives every strengthening iff the two types are equally likely to be
inadmissible. If the L type is more likely to be inadmissible, a strengthening that moves incumbent
mass from just below $p$ to just above $p$ lowers $\Delta_T$. For uniform incumbents, $\Delta_T$
then falls on $(p,r^\ast)$ and rises above $r^\ast$, so the sign pattern holds for comparisons with
$r^\ast\le r_0<r_1$.

### Claim 5 (the weakest ranking for each sign; analytical)

"Every $F$" means every continuous incumbent cdf.

| Sign wanted | Condition for a given $F$ (or a given shift) | Condition for every $F$ and every shift |
|---|---|---|
| $g_j$ falls with competition | none | none |
| $\Delta_T$ rises with competition | (N9) $\ge0$: integral of $D$ weighted by the shift $F-\tilde F$, minus the reserve term. Uniform: $\int_p^r uD\ge p^2D(p^-)$ | $D\ge0$ a.e. above $p$ and $D(p^-)\le0$ (with FOSD: equal admissibility) |
| $\Delta_T>0$ (level) | (N4) $>0$: integral of $D$ weighted by $1-F$, plus the reserve term | $D(p^-)\ge0$ and $\int_p^xD\ge0$ for all $x\ge p$ |
| $g_H>g_L$ (level) | (N5) $>0$: integral of $D$ weighted by $F$ | $\int_x^\infty D\ge0$ for all $x\ge p$, that is, $\mathbb E_H(\theta-x)_+\ge\mathbb E_L(\theta-x)_+$ |

*Derivation of the last two rows.* $\Delta_T=\mathbb E_F\varphi$, so $\Delta_T\ge0$ for every $F$ iff
$\varphi\ge0$, which is the stated condition by (N8). Also $g_H-g_L=\mathbb E_F[\gamma_H-\gamma_L]$
with $\gamma_H(R)-\gamma_L(R)=\int_{\max\{p,R\}}^\infty D(u)\,du$, which is nonnegative for every $R$
iff the stated condition holds. $\square$

The two level conditions are the increasing concave and the increasing convex orders on
$\hat\theta$ (the first with an admissibility ranking). Both are weaker than FOSD. **The comparative
static is not weaker:** a distribution-free Proposition 1 needs FOSD above the reserve (row 2). The
integral order "weighted by $1-F$" governs the level of $\Delta_T$, not its response to competition.

*A risk ranking reverses the trading direction.* Let $G_H$ be a mean-preserving spread of $G_L$,
with both supports above $p$. Then $\int_x^\infty D\ge0$ but $\int_p^xD\le0$, with equality as
$x\to\infty$. So $g_H\ge g_L$ while $\Delta_T\le0$, and (N7) gives $\Delta_T=-(g_H-g_L)$. Example
(script, section C): $G_H=U[1,3]$, $G_L=\delta_2$, $p=0.5$, $r=2.5$ gives $\Delta_T=-0.0625$ and
$g_H-g_L=0.0625$. An investor whose news favors the challenger now **sells** the target, so a low
price attracts the challenger. Reading C, in which the challenger chooses its risk, is the natural
place for this case.

### Claim 6 (posterior bounds with a general prior; analytical)

For arbitrary mixed state-contingent orders on $[-1,1]$,

$$
\operatorname{logit}\pi-\frac2b\le\operatorname{logit}\mu_X\le\operatorname{logit}\pi+\frac2b,\qquad
m(\pi)=\frac{\pi}{\pi+(1-\pi)e^{2/b}},\quad
M(\pi)=\frac{\pi}{\pi+(1-\pi)e^{-2/b}},\qquad\text{(N11)}
$$

and $1-M(\pi)=m(1-\pi)$. The price posterior obeys the same bounds.

*Derivation.* $\mu_X=\pi a_H/[\pi a_H+(1-\pi)a_L]$, so
$\operatorname{logit}\mu_X=\operatorname{logit}\pi+\log(a_H/a_L)$, and Prop. A.1 gives
$\lvert\log(a_H/a_L)\rvert\le2/b$. Solve for $\mu_X$. The price posterior is
$\mathbb E[\mu_X\mid P]$, which inherits the interval. $\square$

The band is symmetric in log-odds, not in probability: $M(\pi)\ne1-m(\pi)$ unless $\pi=1/2$. At
$b=2$: $(m,M)=(0.268941,0.731059)$ at $\pi=1/2$, $(0.136190,0.538102)$ at $\pi=0.3$, and
$(0.461898,0.863810)$ at $\pi=0.7$.

### Claim 7 (price sufficiency, Prop. A.2; analytical)

Suppose $\Delta_T>0$, $g_H\ge g_L$, and the floor $c_L<B(m(\pi))$ holds. Then Proposition A.2 holds
word for word with the new $t_j$ and $g_j$. In every candidate equilibrium the price reveals
$\mu_X$, entry and the price take the form (9), and the residuals take the form (11).

*Derivation.* Three facts carry the old proof over.

1. *Entry depends on the price only through $\mu$.* Given the price, the challenger's expected gross
   profit is $\mathbb E[g(\theta)\mid P]=\sum_j\Pr(j\mid P)\,g_j=B(\mu_P)$, because $\theta$ depends
   on the flow only through $j$.
2. *Terminal value given the type and the flow.* Entry depends only on $(P,C)$, and $C$ is
   independent. So $\mathbb E[V_T\mid j,x]=t_0+e(P(x))(t_j-t_0)$, and
   $P=t_0+e(P)[w_L+\Delta_T\mu_X]$ with $w_L=t_L-t_0$.
3. *The low-type increment is nonnegative.* $w_L=\mathbb E_L[t(\theta)-t_0]\ge0$ by Claim 1(c). It
   can be zero, as at $p=1.1$ in Section 6.3; OA.52 already allows this.

With $e\ge\rho$ (the floor) and $\Delta_T>0$, eq. (10) inverts the price. Entry is nondecreasing in
$\mu$ and $w_L+\Delta_T\mu\ge0$, so (A.3) still gives a strictly increasing $P(\mu)$. $\square$

With two types, target proceeds and challenger profit load on the same scalar $\mu$. Sufficiency
needs no extra condition on $\{(t_j,g_j)\}$. (More than two types is extension N2, outside this
memo.)

### Claim 8 (residuals, the global bound, and (A3) with a general prior; analytical)

The residuals keep the form of eq. (11), $A_H=e\Delta_T(1-\mu_X)$ and $A_L=e\Delta_T\mu_X$, because
$t_0$ and $e\,w_L$ cancel. The bounds become

$$
\rho\,m(1-\pi)\,\Delta_T\le A_H\le[1-m(\pi)]\,\Delta_T,\qquad
\rho\,m(\pi)\,\Delta_T\le A_L\le M(\pi)\,\Delta_T.
$$

The global order bound (A.6) becomes, for $s\in[0,1]$,

$$
U_H'(s)\ge\Big(1-\frac1b\Big)\rho\,m(1-\pi)\,\Delta_T-k,\qquad
U_L'(s)\ge\Big(1-\frac1b\Big)\rho\,m(\pi)\,\Delta_T-k.\qquad\text{(N12)}
$$

Both bounds are positive iff $k<(1-1/b)\rho\lambda(\pi)\Delta_T$ with
$\lambda(\pi)=\min\{m(\pi),m(1-\pi)\}=m(\min\{\pi,1-\pi\})$. So condition (A3) becomes

$$
\Delta_T(F_0)<k<\Big(1-\frac1b\Big)\rho\,\lambda(\pi)\,\Delta_T(F_1).\qquad\text{(A3}\pi\text{)}
$$

- $\lambda(\pi)\le m(1/2)$, with equality only at $\pi=1/2$. **Any prior away from 1/2 narrows the
  (A3) window.** At $b=2$, $\lambda(0.3)=\lambda(0.7)=0.136190$, about half of
  $m(1/2)=0.268941$. The binding type is the one that the prior favors. At $\pi>1/2$ it is the buyer
  in state H, because the price already leans toward H.
- *A sharper weak-economy test.* Every nonzero order loses if
  $k>\bar e\,\Delta_T\max\{1-m(\pi),M(\pi)\}$, where $\bar e=\rho$ if $B(M(\pi))<c_H$ and $\bar e=1$
  otherwise. At $\pi=1/2$ this improves the paper's test $k>\Delta_T(r)$ to $k>M\Delta_T(r)$. In
  the benchmark, the sufficient bound for unique no trade in Prop. A.4 then rises from
  $\mathfrak r(k)=1.220998$ to $\mathfrak r(k/M)=1.262865$ (there $B_r(M)=6.856>c_H$, so $\bar e=1$).
- *No-trade existence (Prop. A.4 analog).* No trade is an equilibrium iff
  $e(\pi)\,\Delta_T\max\{\pi,1-\pi\}\le k$, where $e(\pi)=\rho+(1-\rho)\mathbf 1\{B(\pi)\ge c_H\}$.
- *Full-order existence test (A.7 analog).* Under full orders, $J_H=(1-\pi)K$ and $J_L=\pi K$, with
  $K=\Delta_T\int e(x)\,\frac{f(x-1)f(x+1)}{\pi f(x-1)+(1-\pi)f(x+1)}\,dx$. So $\pi J_H=(1-\pi)J_L$.
  Full orders are an equilibrium against their own schedule if $k<(1-1/b)\min\{J_H,J_L\}$.

*Derivation.* The cancellation is the one in the proof of Prop. A.2. The bounds follow from
$\rho\le e\le1$, Claim 6, and $1-M(\pi)=m(1-\pi)$. The paper's chain
$U_\theta'(s)\ge(1-s/b)F_\theta(s)-k$ uses only $\lvert f'\rvert\le f/b$ and
$F_\theta(s)\ge\inf A_\theta$, which gives (N12). Sharper test: a correctly signed order of size $s$
earns at most $s[\sup A_\theta-k]$, with $\sup A_H\le\bar e\Delta_T(1-m)$ and
$\sup A_L\le\bar e\Delta_TM$; a wrong-signed order earns less than zero. No-trade existence: against
a constant schedule at $\mu=\pi$, an order of size $s$ earns $s[e(\pi)\Delta_T(1-\pi)-k]$ in state H
and $s[e(\pi)\Delta_T\pi-k]$ in state L. For $J$: substitute
$1-\mu_X=(1-\pi)f(x+1)/[\pi f(x-1)+(1-\pi)f(x+1)]$ and the analog for $\mu_X$ into (A.7). Then the
paper's ratio bound $F_\theta(s)\ge e^{-(1-s)/b}J_\theta$ gives the test. $\mathfrak r(d)$ is (A.10).
$\square$

### Claim 9 (truthful bidding; analytical, a standard result)

At the bidding stage each bidder knows its own value, and the values are private: the incumbent's
payoff depends only on $R$, and the challenger's only on $\theta$. In a second-price auction with a
reserve, it is weakly dominant to bid one's value, and not to bid if the value is below the reserve
(Vickrey 1961, *Journal of Finance* 16(1): 8–37; Krishna 2010, *Auction Theory*, 2nd ed., Section
2.2). The argument holds for each value $y$ of the highest competing admissible bid. A winner pays
$\max\{y,p\}$, so a bid equal to the value wins exactly when a win is profitable. Because the
argument holds for every $y$, it holds for every belief about $y$.

So the information structure never enters the bids. It does not matter who knows $j$, what the price
reveals, or whether the incumbent sees the price or the challenger's entry. This is why $t_j$ and
$g_j$ do not depend on the public belief $\mu$. It is also why the price is affine in $\mu$ at a
given entry rate. **The supervisor's remark is correct.** Two limits apply:

1. The argument needs private values. The model keeps $R$ independent of $(j,\theta)$. If the
   investor's information also moved the incumbent's value, truthful bids would no longer be
   dominant.
2. Weak dominance does not exclude other equilibria. The paper already selects truthful bids.

If preparation revealed only part of $\theta$, a risk-neutral challenger would bid its conditional
expected value. That bid would still be weakly dominant, because the rival's bid carries no
information about $\theta$.

*Why a first-price auction is different.* In a first-price auction, the incumbent's best bid
depends on its belief about the challenger's value. That belief is the mixture
$(1-\mu)G_L+\mu G_H$, conditional on entry. So the bids, $t_j$ and $g_j$ all become functions of
$\mu$, and possibly of whether the incumbent observes entry. Then:

1. the price $t_0+e(\mu)[t_L(\mu)-t_0+\mu\Delta_T(\mu)]$ is not affine in $\mu$, and its monotonicity
   needs a new proof;
2. the residual becomes $e(\mu)\Delta_T(\mu)(1-\mu)$, so the trading bounds need bounds on
   $\Delta_T(\mu)$ over $[m,M]$;
3. $B(\mu)$ is no longer linear in $\mu$;
4. asymmetric first-price auctions rarely have closed forms, and they are not revenue equivalent to
   the open or second-price auction (Maskin and Riley 2000, *Review of Economic Studies* 67:
   413–438; specific result number unverified).

### Claim 10 (Proposition 2 with distribution types and a general prior; analytical)

Let $F_1$ be an FOSD strengthening of $F_0$ (for uniform incumbents, $r_0<r_1$). Assume:

- (R) $\Delta_T(F_i)>0$ and $g_H(F_i)>g_L(F_i)$ for $i=0,1$;
- (A1$\pi$) $0\le c_L<B_{F_1}(m(\pi))$;
- (A2$\pi$) $B_{F_0}(\pi)<c_H<B_{F_1}(M(\pi))$;
- (A3$\pi$) as in Claim 8.

Then:

- **(i)** At $F_0$, the unique trading outcome is $q_H=q_L=0$, the price is uninformative, and entry
  is $\rho$.
- **(ii)** At $F_1$, the unique trading outcome is $(q_H,q_L)=(1,-1)$, the price is informative, and
  entry is $\mathsf E>\rho$, with the closed forms (N13). Type-H ownership moves from
  $\pi\rho W_H(F_0)$ to $\pi e_HW_H(F_1)$. It rises iff
  $W_H(F_1)/W_H(F_0)>\rho/e_H(F_1)$. A sufficient condition is
  $W_H(F_1)/W_H(F_0)\ge2\rho/(1+\rho)$. The condition holds automatically if $G_H$ puts all its
  mass above both incumbents' supports ($W_H\equiv1$, the paper's case $h>\bar r$).
- **(iii)** Suppose $F_2$ satisfies $c_L<B_{F_2}(m(\pi))$, $B_{F_2}(M(\pi))<c_H$, (R), and
  $k<(1-1/b)\rho\lambda(\pi)\Delta_T(F_2)$. Then the unique trading outcome is $(1,-1)$ and entry is
  $\rho$. If the types are FOSD-ranked above $p$ with equal admissibility and $F_2$ strengthens
  $F_1$, the last inequality follows from (A3$\pi$) by Claim 4. Otherwise it must be checked,
  because $\Delta_T$ need not rise.

Closed forms under full orders (the analog of eq. 12):

$$
\tau=\frac{c_H-g_L}{g_H-g_L},\qquad x^\ast=\frac b2\big[\operatorname{logit}\tau-\operatorname{logit}\pi\big],\qquad
\alpha_H=1-\tfrac12e^{(x^\ast-1)/b},\qquad \alpha_L=\tfrac12e^{-(x^\ast+1)/b},
$$

$$
e_H=\rho+(1-\rho)\alpha_H,\quad e_L=\rho+(1-\rho)\alpha_L,\quad
\mathsf E=\pi e_H+(1-\pi)e_L,\quad \mathsf O_H=\pi e_HW_H,\quad
\mathsf A=\pi e_H[1-G_H(p^-)]+(1-\pi)e_L[1-G_L(p^-)].\qquad\text{(N13)}
$$

Condition (A2$\pi$) places $\tau$ in $(\pi,M(\pi))$ and $x^\ast$ in $(0,1)$.

*Proof.*

- *Step 1 (beliefs and the floor).* Claim 6 bounds every posterior in $[m(\pi),M(\pi)]$. By (R),
  $B$ increases in $\mu$. By Claim 4(a), $B$ falls under the strengthening for every $G_j$. So
  (A1$\pi$) gives $c_L<B_{F_1}(m)\le B_{F_0}(m)$: the floor holds in both economies, and Claim 7
  applies to both.
- *Step 2 (the buyer).* Claim 7 gives $\Pr(H\mid P)=\mu_X$, entry
  $e(\mu)=\rho+(1-\rho)\mathbf 1\{B(\mu)\ge c_H\}$, and the residuals of Claim 8.
- *Step 3 (the weak economy).* Every residual is at most $\Delta_T(F_0)<k$. A correctly signed order
  of size $s>0$ earns at most $s[\Delta_T(F_0)-k]<0$. A wrong-signed order has a negative gross
  payoff and still pays its cost. So zero is the unique best response to every candidate schedule.
  Then $\mu=\pi$, and $B_{F_0}(m)\le B_{F_0}(\pi)<c_H$ gives entry $\rho$, with the low-cost type in.
  The constant price is $t_0+\rho[\pi t_H+(1-\pi)t_L-t_0]$.
- *Step 4 (the strong economy).* (N12) and (A3$\pi$) make $U_\theta'(s)>0$ on $[0,1]$ against every
  candidate schedule. Full correctly signed orders are the unique best responses, and a mixture with
  any other order is strictly worse.
- *Step 5 (existence).* Under full orders,
  $\operatorname{logit}\mu_X(x)=\operatorname{logit}\pi+(\lvert x+1\rvert-\lvert x-1\rvert)/b$. It is
  constant at $\operatorname{logit}\pi\mp2/b$ outside $(-1,1)$ and linear with slope $2/b$ inside.
  Define entry and the price by (9). Claim 7 gives a measurable inverse, Step 4 gives investor
  optimality, and the price is competitive by construction.
- *Step 6 (closed forms).* $B_{F_1}(\pi)\le B_{F_0}(\pi)<c_H<B_{F_1}(M(\pi))$, so
  $\tau\in(\pi,M(\pi))$, $\operatorname{logit}\tau-\operatorname{logit}\pi\in(0,2/b)$, and
  $x^\ast\in(0,1)$. High-cost entry occurs iff $x\ge x^\ast$. Under H, $X=1+Z$, so
  $\alpha_H=\Pr(Z\ge x^\ast-1)$; under L, $\alpha_L=\Pr(Z\ge x^\ast+1)$. Both are positive, so
  $\mathsf E>\rho$. Given $j$ and entry, the challenger wins with probability $W_j(F)$, independent
  of the price, so $\mathsf O_H=\pi e_HW_H$. Because $x^\ast\in(0,1)$,
  $\alpha_H\in(\tfrac12,1-\tfrac12e^{-1/b})$, so $e_H>(1+\rho)/2$. This gives the sufficient
  ownership condition.
- *Part (iii).* As in the paper, with the trading condition at $F_2$ stated directly.
  $B_{F_2}(M)<c_H$ excludes expensive entry at every feasible belief. The Blackwell comparison is
  unchanged. $\square$

### Claim 11 (the reversal holds for every ranked pair; analytical)

Assume $D\ge0$ a.e. on $(p,\infty)$, $D(p^-)=0$, and $\Gamma:=\int_p^\infty D>0$ (the types differ
above the reserve). Let $u_0=\inf\{x\ge p:\int_p^xD>0\}$. Then, for every $\pi\in(0,1)$, $b>1$ and
$\rho\in(0,1)$, a nonempty open set of uniform strengths $r_0<r_1<r_2$ and costs $(c_L,c_H,k)$
satisfies all hypotheses of Claim 10 and the ownership condition.

*Proof (the analog of A.25, with $u_0$ in place of $\ell$).* Write $\Psi(x)=\int_p^xD$. By (N8),
$\Delta_T(r)=\frac1r\int_p^r\Psi$ for $r\ge p$. So $\Delta_T(r)=0$ for $r\le u_0$, and $\Delta_T$
is continuous and, by (N10), increasing for $r>u_0$. Since $\Psi\le\Gamma$,
$\Delta_T(r)\le(1-p/r)\Gamma$, and (N7) gives $g_H-g_L=\Gamma-\Delta_T(r)\ge\Gamma p/r>0$. The
functions $r\mapsto B_r(\mu)$ and $r\mapsto W_H(r)$ are continuous. Also $W_H(u_0)>0$, because
$\Gamma>0$ forces $G_H$ to put mass above $u_0$.

1. At $r=u_0$, $B(M(\pi))-B(\pi)=(M(\pi)-\pi)\Gamma>0$ (if $u_0=p$, then $F_p(p)=1$ and
   $\Delta_T(p)=0$ directly). Choose
   $r_1>u_0$ close to $u_0$, with $B_{r_1}(M(\pi))>B_{u_0}(\pi)$ and
   $W_H(r_1)/W_H(u_0)>2\rho/(1+\rho)$.
2. For every $r_0\in(u_0,r_1)$: $B_{r_0}(\pi)<B_{u_0}(\pi)<B_{r_1}(M)$, and
   $W_H(r_1)/W_H(r_0)\ge W_H(r_1)/W_H(u_0)$. Choose $r_0$ close to $u_0$, so that
   $\Delta_T(r_0)<(1-1/b)\rho\lambda(\pi)\Delta_T(r_1)$.
3. Choose $k$ strictly inside the (A3$\pi$) window and $c_H$ strictly inside the (A2$\pi$) window.
   Since $g_j(r)\to0$ as $r\to\infty$ (dominated convergence, finite means), some $r_2>r_1$ has
   $B_{r_2}(M)<c_H$. Choose $c_L\in[0,B_{r_2}(m))$, which is not empty because $g_H-g_L>0$. Then
   $\Delta_T(r_2)\ge\Delta_T(r_1)$ gives the trading condition of part (iii).

All inequalities are strict and continuous in the primitives, so the set is open. $\square$

*With an admissibility gap.* If $D(p^-)>0$, the reserve term sets a floor
$\Delta_T(F_0)\ge pF_0(p)D(p^-)$ under FOSD above $p$. So (A3$\pi$) needs
$pF_0(p)D(p^-)<(1-1/b)\rho\lambda(\pi)\Delta_T(F_1)$; for uniform incumbents,
$p^2D(p^-)/r_0<(1-1/b)\rho\lambda(\pi)\Delta_T(r_1)$. A small gap does not destroy a configuration
with strict inequalities, because all objects are continuous in the mixture weight below $p$. A
large gap can destroy it (Section 5.5).

### Claim 12 (effects that the binary case hides)

- (a) **A high type can lose** (analytical; example is a numerical diagnostic). $W_H<1$ whenever
  $G_H$ overlaps the incumbent's support, and $W_H$ falls with competition. So entry can rise while
  type-H ownership falls. In case 2c below, all hypotheses of Claim 10 hold with $\rho=0.95$; entry
  rises from 0.950000 to 0.970117, but $\mathsf O_H$ falls from 0.422906 to 0.416476. When $\rho$ is
  high, the information channel adds little entry, while the stronger incumbent beats the H type
  more often.
- (b) **Preparation need not create an admissible bidder** (analytical). With mass below $p$,
  $\mathsf A<\mathsf E$. The benchmark property that every prepared challenger is admissible
  (Section 4.1) does not extend to types with mass below $p$. The paper already anticipates this in
  Sections 4.1 and 6.3 and in the "actual allocation event" remark of A.7.
- (c) **Dispersion of the low type raises the spread** (analytical, from N6). If $G_L$ lies in
  $[p,r]$ and $G_H$ lies above $r$, $\Delta_T=[(r-\mathbb E_L\theta)^2+\operatorname{Var}_L\theta]/(2r)$.
- (d) **A risk ranking reverses the trading direction** (analytical, Claim 5).
- (e) **An admissibility gap works against the reversal** (analytical, Claims 4(e) and 11).

### Claim 13 (is there a clear, neat result? an assessment)

Yes. A clean statement exists, but it is a generalization, not a new mechanism.

> **Proposition 1′.** For any type distributions, a stronger incumbent lowers the challenger's gross
> profit at every belief. The value gap between the types splits as
> $\Delta_T+(g_H-g_L)=\mathbb E_H\hat\theta-\mathbb E_L\hat\theta+pF(p)D(p^-)$, and a stronger
> incumbent moves every slice of the gap above the reserve from the challenger to the target. So the
> target-payoff spread rises with competition for every incumbent distribution if and only if $G_H$
> dominates $G_L$ in FOSD above the reserve and both types are equally likely to fall below it.
>
> **Proposition 2′.** Under these two conditions, for every prior, noise scale and low-cost
> probability, the reversal of Proposition 2 holds on a nonempty open set of primitives.

What is new:

1. the split identity, which also gives the binary model a one-line intuition:
   $\Delta_T+g_H-g_L=h-\ell$ at every $r$;
2. the exact role of the reserve: an admissibility gap is the only force that can break the
   distribution-free sign pattern, and the paper's own Section 6.3 at $p=1.1$ shows it;
3. the ownership condition.

What it does not give: a different or sharper mechanism. When both type supports lie above the
reserve, the binary model loses nothing qualitative.

---

## 4. What changes relative to the current paper

| Paper object | Status under Reading N |
|---|---|
| Eq. (1), $0<p<\ell<r<h$ | Replaced by: types FOSD-ranked above $p$, with equal admissibility. "H always wins" is not needed. |
| Eq. (4) | Replaced by (N3)–(N5); uniform closed form (N6). |
| Eq. (5) | Replaced by (N10). $g_j$ still falls; $\Delta_T$ rises iff the bracket is positive. |
| Prop. 1, eq. (6) | Survives as Claim 4. The profit part holds for every $G_j$. The spread part holds iff FOSD above $p$ and equal admissibility. The pointwise $(R-\ell)_+$ becomes $\varphi(R)$ in (N8). |
| Eqs. (7)–(8), Prop. A.1 | Survive with $m(\pi)$ and $M(\pi)$ from (N11). |
| Eqs. (9)–(10), Prop. A.2 | Survive word for word; the floor is $c_L<B(m(\pi))$. |
| Eq. (11) | The form survives; the lower bounds are $\rho m(1-\pi)\Delta_T$ and $\rho m(\pi)\Delta_T$. |
| (A.6) | The factor $m$ becomes $\lambda(\pi)=m(\min\{\pi,1-\pi\})$. |
| (A.7) | $J_H=(1-\pi)K$ and $J_L=\pi K$. |
| Prop. 2 | Survives as Claim 10 with (R) and (A1$\pi$)–(A3$\pi$). Two changes: an explicit ownership condition, and a direct trading condition at $r_2$ unless Claim 4(c) applies. |
| Eq. (12) | $x^\ast$ shifts by $-(b/2)\operatorname{logit}\pi$; $\mathsf E$ and $\mathsf O_H$ use the weights $\pi$; $\mathsf O_H$ includes $W_H$. |
| Prop. A.3 | Survives unchanged: $B$ falls under competition for every $G_j$. |
| Prop. A.4 | No trade is an equilibrium iff $e(\pi)\Delta_T\max\{\pi,1-\pi\}\le k$. The closed forms (A.10)–(A.11) do not carry over; the thresholds solve the same equations with (N6). |
| A.25 (nonemptiness) | Becomes Claim 11, with $u_0$ in place of $\ell$. |
| Section 6.3 and OA.52 | A special case. The $p=1.1$ row is an instance of Claim 4(e). |
| Sections 5.3, 6.1, 6.2 | Not checked in this memo. |

---

## 5. Numerical example

Script: `audit/alex_meeting_2026_10_21/scripts/Q1_N_main/reading_n_main.py`. It prints all numbers
below. It does not import the project's `numerics/` package. All results in this section are
**numerical diagnostics**, except where a row reproduces an analytical closed form.

Benchmark vector: $(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02)$ and
$(r_0,r_1,r_2)=(1.2,3,3.6)$, with uniform incumbents. Cases:

- **0**: binary benchmark, $G_H=\delta_{10}$, $G_L=\delta_1$.
- **1**: value classes, $G_H=U[9.95,10.05]$, $G_L=U[0.95,1.05]$ (Section 6.3, $\varepsilon_V=0.05$).
  **1h**: the same at $p=1.1$.
- **2a**: wide overlap, equal mass below $p$:
  $G_H=0.1\,U[0,0.5]+0.9\,U[0.5,19.5]$, $G_L=0.1\,U[0,0.5]+0.9\,U[0.5,2.5]$.
- **2b**: wide overlap, unequal mass below $p$: $G_H=U[0.2,19.8]$, $G_L=U[0.2,2.8]$, so
  $D(p^-)=0.100078$.
- **2c**: case 2a with $\rho=0.95$.
- **3a, 3b**: case 1 with $\pi=0.3$ and $\pi=0.7$.

### 5.1 Validation

- For every case and every $r\in\{r_0,r_1,r_2\}$, the formulas (N3) agree with a direct double
  integration of OA.50 to within $1.8\times10^{-15}$. The split identity (N7) and the kernel (N8)
  hold to the same accuracy.
- (N10) and the profit derivative match central differences to six decimals; (N6) matches (N3) to
  $10^{-16}$.
- The closed forms (N13) match a direct root of $\mu_X(x)=\tau$ and a direct quadrature of the
  Laplace flow law to within $10^{-15}$.
- $\pi J_H-(1-\pi)J_L$ is below $10^{-16}$ in every full-order case, at $\pi\in\{0.3,0.5,0.7\}$.

### 5.2 Cases at the benchmark vector

"NT" = unique no trade; "FO" = unique full orders; "unres." = not settled by the sufficient bounds.

| Case | (A1) | (A2) | (A3) | (iii) | Entry $r_0$ / $r_1$ / $r_2$ | $\mathsf O_H$ $r_0$ / $r_1$ / $r_2$ | Note |
|---|---|---|---|---|---|---|---|
| 0 | yes | yes | yes | yes | 0.250000 / 0.522757 / 0.250000 (NT/FO/FO) | 0.125000 / 0.324192 / 0.125000 | Reproduces A.8 |
| 1 | yes | yes | yes | yes | 0.250000 / 0.522760 / 0.250000 (NT/FO/FO) | 0.125000 / 0.324195 / 0.125000 | Proceeds 0.392665 and 0.872367 = Table 4 |
| 1h | yes | yes | **no** | yes | 0.540309 / 0.511638 / 0.250000 (FO/FO/FO) | 0.336302 / 0.316252 / 0.125000 | $\Delta_T$ falls 1.0125 to 1.005; deterrence; proceeds 0.432173 and 1.014500 = Table 4 |
| 2a | yes | **no** | **no** | no | 0.250000 (NT) / unres. / unres. | 0.111291 / – / – | (A3) window empty; $B_{r_1}(M)=5.689<c_H$ |
| 2b | yes | yes | **no** | no | unres. / unres. / unres. | – | $\Delta_T(r_0)=0.057>k$; see below |
| 2c | yes | **no** | yes | yes | 0.950000 / 0.950000 / 0.950000 (NT/FO/FO) | 0.422906 / 0.404062 / 0.397469 | No expensive entry at $r_1$ |
| 3a | yes | **no** | **no** | no | 0.250000 (NT) / unres. / unres. | 0.075000 / – / – | $B_{r_1}(M(0.3))=4.609<c_H$ |
| 3b | yes | **no** | **no** | no | 1.000000 (NT) / unres. / unres. | 0.700000 / – / – | Entry 1 at $r_0$ because $B_{r_0}(0.7)=6.601>c_H$: expensive entry at the prior |

Details for the unresolved cells:

- 2a, $r_1$: no trade is not an equilibrium, and full orders fail the existence test (A.7 analog). The
  outcome is open.
- 2b: at $r_0$, no trade is an equilibrium (entry 0.25, $\mathsf O_H=0.121785$), but uniqueness is not
  certified. At $r_1$ and $r_2$, no trade is not an equilibrium, and full orders are an equilibrium,
  with entry 0.532450 and 0.517198. So the comparison "no trade at $r_0$, informative trade at $r_1$"
  exists, but it is not certified as unique.
- 3a: full orders are an equilibrium at $r_1$, but the high-cost type never enters, so entry stays
  0.25.
- 3b: full orders are an equilibrium at $r_1$ with entry 0.681296 < 1. With this vector, competition
  **lowers** entry, because the high-cost type already enters at the weak-incumbent prior.

### 5.3 Repaired vectors (stated variants)

The script picks $c_H$ at the midpoint of the joint (A2$\pi$)/(iii) window, $k$ at the geometric
midpoint of the (A3$\pi$) window, and the first $r_2$ on a 0.05 grid with $B_{r_2}(M)<c_H$.

| Case | Changes | All conditions | Entry $r_0$ / $r_1$ / $r_2$ | $\mathsf O_H$ $r_0$ / $r_1$ / $r_2$ | $\mathsf A$ at $r_1$ |
|---|---|---|---|---|---|
| 2a | $r_0=1.0$, $c_H=5.153527$, $k=0.01$, $r_2=4.75$ | yes | 0.250000 / 0.549409 / 0.250000 | 0.111760 / 0.291234 / 0.101242 | 0.494468 |
| 2b | $\rho=0.85$, $r_0=1.0$, $c_H=5.746138$, $k=0.045208$, $r_2=4.8$ | yes | 0.850000 / 0.909947 / 0.850000 | 0.415784 / 0.436445 / 0.376731 | 0.851842 |
| 2c | $\rho=0.95$, $c_H=5.121235$, $k=0.029133$, $r_2=4.9$ | yes | 0.950000 / 0.970117 / 0.950000 | 0.422906 / **0.416476** / 0.383051 | 0.873105 |
| 3a | $\pi=0.3$, $r_0=1.1$, $c_H=3.824527$, $k=0.007476$, $r_2=5.9$ | yes | 0.250000 / 0.498523 / 0.250000 | 0.075000 / 0.206870 / 0.075000 | – |
| 3b | $\pi=0.7$, $r_0=1.1$, $c_H=6.980636$, $k=0.007476$, $r_2=3.85$ | yes | 0.250000 / 0.598889 / 0.250000 | 0.175000 / 0.475498 / 0.175000 | – |

In case 2c, entry rises but type-H ownership falls, because $W_H$ falls from 0.890329 to 0.850658
and $\rho/e_H(r_1)=0.970193>0.955442=W_H(r_1)/W_H(r_0)$. In cases 3a and 3b, $J_H\ne J_L$ at $r_1$
(0.236745 and 0.101462 at $\pi=0.3$; 0.082280 and 0.191987 at $\pi=0.7$), as Claim 8 predicts.

### 5.4 The spread against incumbent strength

| $r$ | 0.6 | 0.8 | 1.0 | 1.2 | 1.5 | 1.9 | 2.5 | 3.0 | 3.6 |
|---|---|---|---|---|---|---|---|---|---|
| Case 1h ($D(p^-)=1$) | – | – | – | 1.012500 | 0.860000 | 0.805263 | 0.876000 | 1.005000 | 1.204167 |
| Case 2b ($D(p^-)=0.10$) | 0.042626 | 0.038780 | 0.044479 | 0.057174 | 0.087105 | 0.145085 | 0.267988 | 0.401996 | 0.591509 |
| Case 2a ($D(p^-)=0$) | 0.000112 | 0.002265 | 0.008388 | 0.019181 | 0.044737 | 0.096914 | 0.214737 | 0.346382 | 0.527586 |

Cases 1h and 2b show the quasi-convex path of Claim 4(d): $d\Delta_T/dr<0$ at $r=1.2$ in case 1h
($-0.760417$) and at $r=0.6$ in case 2b ($-0.051584$). Case 2a, with equal admissibility, rises
throughout.

### 5.5 How large an admissibility gap the sufficient conditions tolerate

Family: $G_H=U[0.5,19.5]$ and $G_L=\delta\,U[0,0.5]+(1-\delta)\,U[0.5,2.5]$, so $D(p^-)=\delta$;
$p=0.5$, $\pi=1/2$, $b=2$. A pair $r_0<r_1$ (grid 0.55 to 8.0, step 0.05, $r_0\le3$) is feasible if
the (A2$\pi$) and (A3$\pi$) windows are both nonempty ($c_L=0$ allowed). The table reports the best
ratio $(1-1/b)\rho\lambda\Delta_T(r_1)/\Delta_T(r_0)$ over pairs with a nonempty (A2$\pi$) window;
"feasible" means a ratio above 1.

| $\delta=D(p^-)$ | $\min_r\Delta_T$ | $\rho=0.25$ | $\rho=0.5$ | $\rho=0.85$ |
|---|---|---|---|---|
| 0 | $1.7\times10^{-5}$ | 3100, feasible | 6210, feasible | 10600, feasible |
| 0.01 | 0.004373 | 12.2, feasible | 24.5, feasible | 41.6, feasible |
| 0.02 | 0.008417 | 6.47, feasible | 12.9, feasible | 22.0, feasible |
| 0.05 | 0.020090 | 2.80, feasible | 5.59, feasible | 9.51, feasible |
| 0.10 | 0.038880 | 1.52, feasible | 3.05, feasible | 5.18, feasible |
| 0.20 | 0.075704 | 0.848, **infeasible** | 1.70, feasible | 2.88, feasible |

The best pairs use a very strong $r_1$ (6.25 to 6.75). With the benchmark $r_1=3$ and $\rho=0.25$,
case 2b admits no $r_0$ on the grid: the grid minimum $\Delta_T\approx0.039$ exceeds the (A3$\pi$)
cap 0.0135. A
larger admissibility gap shrinks the region, and at $\delta=0.2$, $\rho=0.25$ the grid has no
feasible pair.

### 5.6 A risk ranking

$G_H=U[1,3]$, $G_L=\delta_2$, $p=0.5$: $\Delta_T=-0.006944,-0.041667,-0.062500,-0.055556,-0.041667$
at $r=1.5,2,2.5,3,4$, and $g_H-g_L=-\Delta_T$ in each case. The magnitude $\lvert\Delta_T\rvert$ is
hump-shaped in $r$.

---

## 6. Open issues and risks

1. **The ownership measure (choice).** Under Reading N, "high-value ownership" has three natural
   versions: type-H ownership $\pi e_HW_H$, challenger ownership, or the expected value of the
   winner. They can move in different directions. Case 2c shows that type-H ownership can fall while
   entry rises.
2. **Families other than the uniform (open).** Claim 11 uses uniform incumbents near $u_0$. For
   another family, the construction needs $\Delta_T(F)\to0$ along the family, which holds if the
   incumbent's support can lie below $u_0$. I did not check other families.
3. **The size of a tolerable admissibility gap (open; numerical diagnostic on one family).**
   Continuity shows that small gaps are harmless. Section 5.5 shows that large gaps can destroy the
   sufficient region. I have no sharp threshold.
4. **Intermediate strengths (open).** As in the paper, the equilibrium correspondence between $r_0$
   and $r_1$ is open. Case 2b at the benchmark vector shows coexistence questions at $r_0$ itself.
5. **Risk rankings (conjecture).** If $\Delta_T<0<g_H-g_L$, a mirrored version of Claim 10 should
   hold with orders $(-1,+1)$ and $\lvert\Delta_T\rvert$ in place of $\Delta_T$. But
   $\lvert\Delta_T\rvert$ is hump-shaped in $r$ (Section 5.6), so "competition creates competition"
   can only hold on the rising part. I did not prove this.
6. **A first-price sale (open).** Claim 9 explains why the analysis would change. I did not solve
   it.
7. **More than two types, and an investor who sees $\theta$ (extensions N2 and N3).** Outside this
   memo. With two types, price sufficiency is automatic (Claim 7).
8. **Literature.** Vickrey (1961) was checked for bibliographic data and main content. For Maskin
   and Riley (2000) I checked the bibliographic record and the topic, not a specific result number. For Krishna (2010) I checked the section title ("Second-Price Auctions",
   Section 2.2), not the exact proposition number. The order characterizations in Claim 5 are
   proved here and need no citation.

---

## 7. Recommendation

In order of priority:

1. **Add the split identity to Section 3.1** (one sentence and one display):
   $\Delta_T+(g_H-g_L)=h-\ell$ at every $r$, so competition moves the value gap from the challenger
   to the target. This gives the existing model the "neat" intuition at no cost.
2. **Add one appendix result, "Distribution types"**, that states Claims 4, 10 and 11 (Propositions
   1′ and 2′) with a general prior $\pi$. Use the value classes of Section 6.3 as its example. Keep
   the binary model in the main text.
3. **Add one sentence to Section 6.3.** At $p=1.1$ the low class is inadmissible, $\Delta_T$ falls in
   $r$ on $(p,\sqrt3\,p)$, and the reversal is therefore not expected; Table 4 shows deterrence.
4. **Generalize the prior in Appendix A.** Replace $m$, $M$, $1/2$ and $\rho m$ by $m(\pi)$,
   $M(\pi)$, $\pi$ and $\rho\lambda(\pi)$. State that a prior away from 1/2 narrows the (A3) window.
5. **Define ownership for distribution types** ($\mathsf O_H=\pi e_HW_H$), and state the ownership
   condition of Claim 10(ii).
6. **In the reply to the supervisor**, say: (a) the second-price rule makes the information
   structure harmless for bidding (Claim 9); (b) the neat result is the split identity plus the
   characterization "FOSD above the reserve and equal admissibility"; (c) the reserve is the one
   place where distributions add a genuinely new force.
7. *Optional.* The sharper weak-economy test of Claim 8 ($k>M\Delta_T$) widens the unique no-trade
   region of Prop. A.4 from $r<1.220998$ to $r<1.262865$ in the benchmark.

---

## 8. Plain summary

The paper gives the challenger one of two known values, each with probability one half. The
supervisor asked for a richer model. In it, the challenger draws its value from a good or a bad
distribution and learns its value only when it prepares a bid. This memo works out that model. An
informed investor knows which distribution applies.

Most of the paper survives. The sale is a second-price auction, so each bidder still bids its own
value, whatever anyone else knows. The stock price still tells the challenger everything that the
market knows. The main result also survives: a stronger incumbent can make the price more
informative, and that can draw in more challengers. This works for every pair of distributions in
which the good type has higher values, and for every prior, if both types are equally likely to
fall below the reserve price.

One simple fact drives the result. The value difference between a good and a bad challenger is a
fixed amount. Competition only changes who receives it. A weak incumbent leaves most of it with the
challenger. A strong incumbent pushes it to the target's shareholders. Then the target's price
depends on the challenger's quality, and informed investors trade on that.

Two new effects appear. First, the reserve price matters. If a bad challenger is more likely to fall
below the reserve, competition can make the price less informative, and the main result can fail.
The paper's own high-reserve example shows this. Second, a good challenger can now lose to the
incumbent, so more entry does not always mean that good challengers win more often.

The verdict: the extension gives a clean, general statement and one new insight about the reserve,
but no new mechanism. The binary model is a faithful special case.
