# Q2 (technical): what the proofs need from Laplace noise, the class of laws that supplies it, and why Laplace is the extreme member

Memo to the author, meeting of 21 October 2026, point 2 (technical side).
Scripts: `audit/alex_meeting_2026_10_21/scripts/Q2_laplace_technical/`
(`noise_laws.py`, `model.py`, and the print-only scripts `g1_posterior_entry.py` to `g5_gaussian_kyle.py`).
Run each script from the repository root with `.venv/bin/python <path>`.

## 1. Question and reading

The supervisor asks for "a very very clear justification" of Laplace noise "from a technical
perspective (a clean linear posterior that gives rise to a clean equilibrium)". I read the request
as five technical questions. The economic justification and the discrete model are separate
workstreams. I touch them only where a technical result bears on them.

- (a) Which property of the Laplace law does each proof step use? What is the weakest condition on a
  noise law under which that step still holds?
- (b) What is the natural general class? Which results hold on all of it? Is Laplace special inside it?
- (c) Why not Kyle's Gaussian noise? Which steps fail? In what exact sense is the Laplace posterior "linear"?
- (d) What does the class lose? Does Proposition 2 hold on the class with the same proof?
- (e) Does a one-directional continuous version (orders in $[0,1]$) simplify the proof?
- (f) A draft paragraph and a footnote for Section 2.3 (in Section 7 below).
- (g) A numerical illustration (Section 5).

## 2. Formal setup

The model is that of Sections 2–4 of `overleaf/paper/main.tex`. Only the noise law changes. The
noise $Z$ has a density $f$ on $\mathbb R$ and the flow is $X=q+Z$. Notation:

- Score: $\psi=-(\log f)'=-f'/f$ where it exists.
- Class $\mathcal C_L$ ($L>0$): $f$ is absolutely continuous and positive, and $|f'|\le Lf$ almost
  everywhere. Equivalently, $\log f$ is Lipschitz with constant $L$. Laplace with scale $b$ is in
  $\mathcal C_{1/b}$.
- Likelihood-ratio bound: $K_f=\sup_{|\delta|\le 2}\operatorname{ess\,sup}_y f(y+\delta)/f(y)$,
  with $m_f=1/(1+K_f)$ and $M_f=K_f/(1+K_f)$.
- Full orders $(q_H,q_L)=(1,-1)$: log odds
  $\lambda_f(x)=\log f(x-1)-\log f(x+1)=\int_{x-1}^{x+1}\psi(u)\,du$, posterior
  $\mu_f(x)=1/(1+e^{-\lambda_f(x)})$, and attained supremum $\bar\mu_f=\operatorname{ess\,sup}_x\mu_f(x)$.
- Laplace values: $K=e^{2/b}$, $m=1/(1+e^{2/b})$, $M=1-m$, and
  $\lambda(x)=(2/b)\operatorname{clip}(x,-1,1)$, where $\operatorname{clip}(x,-1,1)=\max\{-1,\min\{x,1\}\}$.
- Entry, general form: $e(\mu)=\rho\,\mathbf 1\{B_r(\mu)\ge c_L\}+(1-\rho)\,\mathbf 1\{B_r(\mu)\ge c_H\}$.
  Under (A1) the first indicator is always one.
- Deviation objects (eq. A.4): for a bounded measurable residual $A\ge0$,
  $F_A(s)=\int f(x-s)A(x)\,dx$, and $U(s)=sF(s)-ks$.
- Experiments: for a pure profile $q_L<q_H$, the flow experiment is the dichotomy
  $(f(\cdot-q_H),f(\cdot-q_L))$. Its Neyman–Pearson (ROC) curve is
  $\beta_f(\alpha)=\sup\{P_H(\varphi):P_L(\varphi)\le\alpha\}$ over tests $\varphi:\mathbb R\to[0,1]$.
- Benchmark: $(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02)$. At $r_1=3$:
  $g_L=0.125$, $g_H=8.458333$, $\Delta_T=0.666667$, high-cost threshold $\tau=0.705$.

## 3. Results

### 3.1 Property-to-proof map (task a)

| Proof step in the paper | Laplace property used | Weakest general condition | Necessary? |
|---|---|---|---|
| Prop. A.1, eq. (8): $m\le\mu\le M$ under every strategy | $\big||x-q|-|x-q'|\big|\le 2$, so the ratio lies in $[e^{-2/b},e^{2/b}]$ | $K_f<\infty$; the bounds become $m_f,M_f$ | Yes, for bounds uniform over strategies (R1) |
| Prop. A.2, price sufficiency; eq. (10) inversion | entry floor $e\ge\rho$ from (A1) at $m$ | $m_f>0$ (that is, $K_f<\infty$) and $c_L<B_r(m_f)$ | A floor is needed for the inversion at every price |
| Eq. (11), residual floor $\rho m\Delta_T$ | $m>0$ | as above, floor $\rho m_f\Delta_T$ | Yes, for a positive uniform floor |
| A.5–A.6, global order bound | $\vert f'\vert\le f/b$, $b>1$ | $f$ absolutely continuous, $\vert f'\vert\le Lf$ a.e., $L<1$ | Necessary and sufficient for $\vert F_A'\vert\le LF_A$ over all residual schedules (R2) |
| A.7, full-order existence test | $f(x-s)/f(x-1)\ge e^{-(1-s)/b}$ | $\log f$ Lipschitz with constant $L$ | Sufficient |
| Eq. (12), closed forms | piecewise-linear log odds (A.8) and an explicit survival function | $\lambda_f$ invertible in closed form, and an explicit survival function | No: the results survive without closed forms (R16, R17) |
| Step 6, $\alpha_H>\alpha_L>0$, entry above $\rho$ | monotone posterior, positive tails | $\tau<\bar\mu_f$ and $f>0$ | Monotone likelihood ratio is not needed (R16) |
| A.14, tie rule and entry jump at $r_C$ | plateau $\mu=M$ on $x\ge1$ with positive mass | the posterior has an atom at $\bar\mu_f$; in $\mathcal C_L$ this needs $\psi=L$ on an interval longer than 2 | Only exact exponential pieces give it (R5) |
| OA A.1, null sets, no off-path flows | $f>0$ everywhere | $f>0$ a.e.; implied by $K_f<\infty$ | Yes (R6) |
| Prop. 3 certificates (OA B.1–B.5) | piecewise-logistic posterior (OA.65), $f''=(f-\delta_0)/b^2$ (OA.71), elementary antiderivatives (OA.74) | Laplace-specific as written | Open for other laws |

**R1 (posterior bounds; analytical).** (i) If $K_f<\infty$, then for arbitrary mixed orders on
$[-1,1]$, $m_f\le\mu_X\le M_f$ almost everywhere, and the price posterior obeys the same bounds.
(ii) If $K_f=\infty$, no pair of bounds strictly inside $(0,1)$ holds for all strategies. (iii)
$K_f<\infty$ implies $f>0$ almost everywhere. (iv) If $f\in\mathcal C_L$, then $K_f\le e^{2L}$.
(v) If $f$ is symmetric and unimodal, then $K_f=\sup_x f(x-1)/f(x+1)$. So the full-order profile
attains the uniform bound and $M_f=\bar\mu_f$.

*Derivation.* (i) For $q,q'\in[-1,1]$, put $y=x-q'$ and $\delta=q'-q\in[-2,2]$. Then
$f(x-q)/f(x-q')=f(y+\delta)/f(y)\le K_f$ for almost every $x$. The lower bound $1/K_f$ follows from
the shift $-\delta$ at the point $y+\delta$. Tonelli's theorem over $\sigma_H(dq)\sigma_L(dq')$ gives
$a_L/K_f\le a_H\le K_fa_L$ almost everywhere, hence $\mu_X\in[m_f,M_f]$. The tower property
$\mu_P=\mathbb E[\mu_X\mid P]$ carries the bounds to the price posterior. This is the paper's proof
with $e^{2/b}$ replaced by $K_f$.
(ii) If $K_f=\infty$, then for each $n$ there is a $\delta\in[-2,2]$ with $f(y+\delta)>nf(y)$ on a
set $E_n$ of positive measure. Take the pure orders $q_H=-\delta/2$ and $q_L=\delta/2$. Then
$\mu_X>n/(n+1)$ on $E_n+q_L$. This set has positive probability, because $f(x-q_H)>0$ there.
(iii) Suppose $f=0$ on a set $E$ of positive measure. For every $|\delta|\le2$,
$f(y+\delta)\le K_ff(y)=0$ for almost every $y\in E$. Integrate over $\delta\in[-2,2]$:
$\int_E[F(y+2)-F(y-2)]\,dy=0$. So for almost every $y\in E$, $f=0$ almost everywhere on
$(y-2,y+2)$. Repeat the argument from $E+(-2,2)$: $f=0$ almost everywhere on $\mathbb R$, a contradiction.
(iv) $|\log f(y+\delta)-\log f(y)|\le L|\delta|\le 2L$.
(v) For symmetric unimodal $f$, $\psi\le0$ on $(-\infty,0)$ and $\psi\ge0$ on $(0,\infty)$. For
$0<\delta\le2$, $\log f(y)-\log f(y+\delta)=\int_y^{y+\delta}\psi\le\int_{[y,y+\delta]\cap(0,\infty)}\psi$.
A window of length $\delta$ inside $(0,\infty)$ extends to a window of length 2 inside $(0,\infty)$
without a decrease of the integral. So the supremum over all shifts equals
$\sup_x\int_{x-1}^{x+1}\psi=\sup_x\lambda_f(x)$. Symmetry covers negative shifts. $\square$

**R2 (global order bound; analytical).** Let $f\in W^{1,1}$ be positive. The inequality
$|F_A'(s)|\le LF_A(s)$ holds for every $s$ and every bounded measurable $A\ge0$ if and only if
$|f'|\le Lf$ almost everywhere. With a floor $F\ge a>0$ and $L<1$,
$U'(s)\ge(1-sL)F(s)-k\ge(1-L)a-k$ on $[0,1]$.

*Derivation.* Online Appendix A.3 already proves that $F_A$ is absolutely continuous with
$F_A'(s)=-\int f'(x-s)A(x)\,dx$, for any positive $f\in W^{1,1}$ with $|f'|\le Lf$. Sufficiency is
immediate. For necessity, suppose $f'>Lf$ on a set $S$ of positive measure. Take
$A=\mathbf 1_{S\cap[-R,R]}$ and $s=0$. Then $-F_A'(0)=\int_{S\cap[-R,R]}f'>L\int_{S\cap[-R,R]}f=LF_A(0)$.
The case $f'<-Lf$ is the same. The buyer needs only $f'\le Lf$, and the seller needs only $f'\ge-Lf$.
The condition $L<1$ (that is, $b>1$) is substantive: the noise must be large relative to the order
bound. Without a score bound below one, full orders can lose to smaller orders. R15 shows such a
loss under Gaussian noise, whose score is unbounded.

*Remark (another route; analytical).* If $A$ takes values in $[a,\bar A]$, then
$F(s_2)-F(s_1)=\int[f(x-s_2)-f(x-s_1)](A-\tfrac{a+\bar A}2)\,dx$. So
$|F(s_2)-F(s_1)|\le\tfrac12(\bar A-a)\,\mathrm{TV}(f)\,|s_2-s_1|$ for any $f$ of bounded variation,
and $U'\ge a-\tfrac12(\bar A-a)\mathrm{TV}(f)-k$. This route allows densities with jumps, but at the
benchmark it fails: $0.0448-\tfrac12(0.6219)(0.5)<0$. The score bound is the condition that works.

**R3 (one condition gives all the regularity; analytical).** If $\log f$ is Lipschitz with constant
$L$, then $f$ is continuous and positive, $f\le L/2$ (with equality only for Laplace with $b=1/L$),
$\int|f'|\le L$ (so $f\in W^{1,1}$), $K_f\le e^{2L}$, and the flow law under any strategy is
equivalent to Lebesgue measure.

*Derivation.* $f(y)\ge f(z)e^{-L|y-z|}$; the integral over $y$ gives $1\ge 2f(z)/L$. Equality forces
$f(y)=f(z)e^{-L|y-z|}$ for all $y$, which is the Laplace density centred at $z$. The rest follows
from $|f'|\le Lf$ and R1. Every regularity statement in Online Appendix A.1 and A.3 (positivity,
boundedness, continuity, $W^{1,1}$, null-set invariance) therefore follows from the one score bound. $\square$

**R4 (the "clean linear posterior" and the closed forms; analytical).** For Laplace noise and pure
orders $q_L<q_H$,
$$\lambda(x)=\frac{|x-q_L|-|x-q_H|}{b}=\frac1b\operatorname{clip}\big(2x-q_H-q_L,\,-(q_H-q_L),\,q_H-q_L\big).$$
The log odds are linear in flow, with slope $2/b$, between the two orders. They are constant
outside. Under full orders this is (A.8): $\lambda(x)=(2/b)\operatorname{clip}(x,-1,1)$. Then
$x^*=(b/2)\operatorname{logit}\tau$, and $\alpha_H,\alpha_L$ in (12) are Laplace survival
probabilities. *Characterization:* a symmetric $f\in\mathcal C_L$ has
$\lambda_f(x)=2L\operatorname{clip}(x,-1,1)$ for all $x$ if and only if $f$ is Laplace with $b=1/L$.

*Derivation.* For $x>1$, $\lambda_f(x)=\int_{x-1}^{x+1}\psi=2L$ with $\psi\le L$ forces $\psi=L$
almost everywhere on $[x-1,x+1]$. The union over $x>1$ is $(0,\infty)$, and symmetry gives
$\psi=-L$ on $(-\infty,0)$. So $f(z)\propto e^{-L|z|}$. For the closed forms in general, the weakest
condition is an explicit inverse of $\lambda_f$ on $(m_f,M_f)$ and an explicit survival function.
Two other members have both:
- Logistic: (A.23) in the paper.
- Hyperbolic secant, $f(z)=\operatorname{sech}(z/b)/(\pi b)$:
  $x^*=b\operatorname{artanh}\{\tanh(\operatorname{logit}(\tau)/2)/\tanh(1/b)\}$ and
  $\alpha_{H,L}=(2/\pi)\arctan e^{-(x^*\mp1)/b}$. At the benchmark this gives $x^*=2.8174$ and
  $\alpha_H=0.24391$, which agrees with direct computation (`g1`, Table 4). $\square$

**R5 (plateaus and the tie rule; analytical).** For $f\in\mathcal C_L$, $\lambda_f(x)\le 2L$, with
equality if and only if $\psi=L$ almost everywhere on $[x-1,x+1]$. So the full-order posterior equals
the class bound $M_L=e^{2L}/(1+e^{2L})$ on a set of positive measure if and only if $\psi=L$ on an
interval longer than 2. The tie rule matters at a threshold $\tau$ if and only if
$\Pr(\mu_X=\tau)>0$. Under Laplace noise the posterior law has atoms only at $m$ and $M$, each with
mass $(1+e^{-2/b})/4=0.3420$ at $b=2$. So the tie matters only at $\tau=M$, that is, at $r_C$. For
the logistic law, the hyperbolic secant law, and Laplace plus Gaussian noise, $\psi<L$ everywhere.
For these laws there is no plateau, indifference is a null event, and entry tends continuously to
$\rho$ as $r\uparrow r_C$. The discontinuity in (A.14) and Figure 2 is a Laplace feature, not a
feature of the mechanism. $\square$ (`g2`, Part D: the near-plateau mass shrinks to zero as the
tolerance shrinks, except for Laplace, where it stays at $0.5$.)

**R6 (full support removes off-path flows; analytical).** Suppose $f>0$ almost everywhere (implied
by $K_f<\infty$). Then the flow law under any strategy and any unilateral deviation has density
$\tfrac12(a_H+a_L)>0$ almost everywhere, so it is equivalent to Lebesgue measure. Three
consequences follow:
1. Bayes' rule fixes $\mu_X$ almost everywhere under every deviation. No flow is off-path, and no
   belief refinement is needed.
2. Two versions of the price function that agree almost everywhere give the same payoffs under every
   deviation (Online Appendix A.1).
3. A deviation changes the law of the flow, not the price function. So price values outside the
   image of $P$ are never observed.

Part (i) of Proposition 2 uses only $A_\theta\le\Delta_T$ and this property. The bound
$A_H=e(P)\Delta_T(1-\mu_X)\le\Delta_T$ holds without any floor, because $e(P(x))$ is a function of
$x$. So part (i) holds for every full-support noise law, Gaussian included. $\square$

### 3.2 The general class and the extreme position of Laplace (task b)

**R7 (closure and membership; analytical, checked numerically).** (i) $\mathcal C_L$ is convex and
closed under convolution with any probability measure $\kappa$:
$|(f*\kappa)'|=|f'*\kappa|\le|f'|*\kappa\le L\,f*\kappa$. A change of scale by $\sigma$ maps $\mathcal C_L$ to
$\mathcal C_{L/\sigma}$. (ii) Membership:

| Law (score bound $L=1/2$ where defined) | score $\psi(z)$ | in class? | log-concave | $K_f$ | $\bar\mu_f$ |
|---|---|---|---|---|---|
| Laplace, $b=2$ | $\operatorname{sgn}(z)/b$ | yes; bound attained everywhere | yes | $e=2.7183$ | $M=0.7311$, attained on $x\ge1$ |
| Logistic, $s=2$ | $\tanh(z/2s)/s$ | yes; bound approached as $\vert z\vert\to\infty$ | yes | $2.7183$ | $M$, not attained |
| Hyperbolic secant, $\operatorname{sech}(z/b)/(\pi b)$ | $\tanh(z/b)/b$ | yes; approached | yes | $2.7183$ | $M$, not attained |
| Student $t$, $\nu=3$, $\sigma=2.309$ | $(\nu+1)z/(\nu\sigma^2+z^2)$ | yes; $L=(\nu+1)/(2\sigma\sqrt\nu)$, attained at $\vert z\vert=\sigma\sqrt\nu$ | no | $2.6909$ | $0.7291<M$, at $x=4.12$; $\mu\to\tfrac12$ as $\vert x\vert\to\infty$ |
| Cauchy, $\sigma=2$ | as Student $t$ with $\nu=1$ | yes | no | $2.6180$ | $0.7236<M$ |
| Laplace$(2)$ + $N(0,1)$ | $\tfrac1b\tanh\{(\log T_1-\log T_2)/2\}$ | yes | yes | $2.7183$ | $M$, not attained |
| Gaussian | $z/\sigma^2$ | no: unbounded | yes | $\infty$ | 1 |
| Finite Gaussian mixture | $\psi(z)/z\to1/\sigma_{\max}^2$ | no | in general no | $\infty$ | 1 |
| Uniform on $[-c,c]$ | 0 inside, $\log f=-\infty$ outside | no: no full support | n/a | $\infty$ | 1 at flows near the support's edge |

Here $T_1=e^{-z/b}\Phi(z/s-s/b)$ and $T_2=e^{z/b}\Phi(-z/s-s/b)$ for Laplace$(b)$+$N(0,s^2)$.
(iii) Kyle-type Gaussian noise traders plus an independent Laplace$(b)$ component is in
$\mathcal C_{1/b}$ by (i). Its tail is exponential,
$f(z)\sim(2b)^{-1}e^{s^2/2b^2}e^{-|z|/b}$, so $\bar\mu_f=M$. The paper's exact conditions (A1)–(A3)
then apply (R16). More generally, the same holds for $Z_{\rm Lap}+W$ whenever
$\mathbb Ee^{|W|/b}<\infty$, by dominated convergence of $e^{|z|/b}f(z)$.
(`g2`, Part A; `g1`, Table 3.) $\square$

**R8 (Laplace is the most concentrated member; analytical, checked numerically).** Let
$f\in\mathcal C_L$ have median 0 (for example, $f$ symmetric). Then for every $t\ge0$,
$$\Pr_f(|Z|>t)\ \ge\ e^{-Lt}=\Pr_{\rm Laplace(1/L)}(|Z|>t),$$
with equality at some $t>0$ only if $f$ is Laplace with $b=1/L$. So $|Z|$ under any member
first-order dominates $|Z|$ under Laplace. The expectation of every nondecreasing function of $|Z|$ (second
moment, mean absolute value, any tail probability) is smallest under Laplace. In particular
$\mathbb E_fZ^2\ge 2/L^2$, which is the variance bound when $f$ is symmetric. Laplace is the lightest-tailed member, in this strong sense.

*Derivation.* Put $S(t)=\int_t^\infty f$. For $z\ge t\ge0$, $f(z)\ge f(t)e^{-L(z-t)}$, so
$S(t)\ge f(t)/L$. For $0\le z\le t$, $f(z)\le f(t)e^{L(t-z)}$, so $\int_0^tf\le f(t)(e^{Lt}-1)/L$.
Since the median is 0, $\tfrac12=\int_0^tf+S(t)\le S(t)(e^{Lt}-1)+S(t)=S(t)e^{Lt}$. So
$S(t)\ge\tfrac12e^{-Lt}$, and the left tail is the same. Equality needs both inequalities tight,
that is, $f(z)=f(0)e^{-Lz}$ on $[0,\infty)$. Without a zero median, the same holds for $|Z-\mathrm{med}|$.
(`g2`, Part B: Laplace has the smallest tail at every $t$; the variances are 8 for Laplace, 9.87 for
the hyperbolic secant, 13.16 for the logistic, and 16 for Student $t$ with $\nu=3$.) $\square$

**R9 (Laplace is the most informative member; analytical, checked numerically).**
(i) Let $f\in\mathcal C_L$, and fix a pure profile $q_L<q_H$ with $\Delta=q_H-q_L$. Then the ROC
curve of the $f$-experiment lies below the ROC curve of Laplace with $b=1/L$:
$$\beta_f(\alpha)\le\beta_{\rm Lap}(\alpha)=\begin{cases}\alpha e^{L\Delta},&\alpha\le\tfrac12e^{-L\Delta},\\ 1-e^{-L\Delta}/(4\alpha),&\tfrac12e^{-L\Delta}\le\alpha\le\tfrac12,\\ 1-(1-\alpha)e^{-L\Delta},&\alpha\ge\tfrac12.\end{cases}$$
For a binary state, pointwise ROC dominance gives the convex order of posteriors (derivation
below), which is Blackwell dominance (Blackwell's theorem, which the paper cites as Blackwell 1953).
Every Bayesian decision maker (the challenger among them) values the Laplace price weakly more at the
same orders.
(ii) If $f\in\mathcal C_L$ is also log-concave, then $\kappa=f-L^{-2}f''$ is a probability measure
and $f=\ell_{1/L}*\kappa$, where $\ell_b$ is the Laplace density. So $Z_f=Z_{\rm Lap}+W$ with
$W\sim\kappa$ independent. The Laplace experiment is then Blackwell-superior at every order profile,
mixed profiles included, by additive garbling.
(iii) As a by-product, the Fisher information $I(f)=\mathbb E\psi^2\le L^2$, with equality among
symmetric unimodal members only for Laplace.

*Derivation of (i).* Fix a test $\varphi$ and put $h(s)=\int\varphi(x)f(x-s)\,dx$. By Online
Appendix A.3, $h$ is absolutely continuous with $h'(s)=\int\varphi(x)\psi(x-s)f(x-s)\,dx$, so
$|h'|\le Lh$. Since $\int\psi(x-s)f(x-s)\,dx=-\int f'=0$, also
$h'(s)=-\int(1-\varphi)\psi f$, so $|h'|\le L(1-h)$. Thus $h'\le\Phi(h)$ with
$\Phi(h)=L\min\{h,1-h\}$, which is Lipschitz. Let $g$ solve $g'=\Phi(g)$ with $g(q_L)=h(q_L)=\alpha$.
Put $w=h-g$. Then $w'\le L|w|$ and $w(q_L)=0$, so Grönwall's inequality gives $w\le0$ and
$P_H(\varphi)=h(q_H)\le g(q_H)$. For Laplace, the half-line test $\mathbf 1[t,\infty)$ has
$h_t(s)=\Pr(Z\ge t-s)$, and $h_t'=\Phi(h_t)$ holds exactly: $h_t'=Lh_t$ while $h_t\le\frac12$, and
$h_t'=L(1-h_t)$ after that. By uniqueness of the ODE solution, $g=h_t$ when $h_t(q_L)=\alpha$.
Half-line tests are Neyman–Pearson tests for Laplace (monotone likelihood ratio), so
$g(q_H)=\beta_{\rm Lap}(\alpha)$. The solution of the ODE gives the display. For the challenger, the entry
value $\mathbb E\max\{B_r(\mu)-C,0\}$ is convex in $\mu$. ROC dominance gives
$\mathbb E[(\mu-t)_+]$ larger for every $t$, because
$\mathbb E[(\mu-t)_+]=\tfrac12\sup_\alpha[(1-t)\beta(\alpha)-t\alpha]$ at prior $\tfrac12$. So it
gives the convex order of posteriors and a weakly higher value.

*Derivation of (ii).* $f'=-\psi f$, $\psi$ is nondecreasing and bounded, and $f$ is Lipschitz. So
the distributional derivative is $f''=-f\,d\psi+\psi^2f\,dx$, and
$\kappa=f(1-b^2\psi^2)\,dx+b^2f\,d\psi\ge0$ with $b=1/L$. Its total mass is
$1-b^2[f']_{-\infty}^{\infty}=1$. Because $(1-b^2D^2)\ell_b=\delta_0$ (this is identity OA.71 in the
paper), $\ell_b*\kappa=f$; in Fourier terms, $\hat\kappa(t)=(1+b^2t^2)\hat f(t)$. For Laplace itself,
$\kappa=\delta_0$. The condition for $f=\ell_b*\kappa$ with $\kappa\ge0$ is $d\psi\ge(\psi^2-1/b^2)\,dx$ as measures.
Log-concavity and $|\psi|\le1/b$ are sufficient. Student $t$ fails it just beyond $|z|=\sigma\sqrt\nu$.

*Numerical checks.*
- `g2`, Part F: the function $D(\tau)=G_{\rm Lap}(\tau)-G_f(\tau)$, with
  $G(\tau)=\mathbb E(\mu-\tau)_+$ at prior $\tfrac12$, is $\ge0$ for every $\tau$ against the
  logistic, the hyperbolic secant, Laplace + $N(0,1)$, Student $t$ ($\nu=3$), and Cauchy, all at
  $L=\tfrac12$.
- `g2`, Part G: the ROC gap $\beta_f-\beta_{\rm Lap}$ is at most $3\times10^{-12}$ (grid error is
  $10^{-7}$) for two bimodal members, a member with a periodic score term, an asymmetric member, and
  Student $t$.
- `g2`, Part E: for the logistic and the hyperbolic secant, $\kappa\ge0$ integrates to 1, and the
  convolution $\ell_b*\kappa$ reproduces $f$ to 10 digits. For Student $t$ ($\min\kappa=-1.2\times10^{-3}$)
  and Cauchy ($-7.7\times10^{-3}$), $\kappa$ is negative somewhere. $\square$

**R10 (correction: at a common scale, logistic noise is Laplace noise plus independent noise;
analytical, checked numerically).** For every $b>0$,
$$\text{Logistic}(b)\overset d=\text{Laplace}(b)+W,\qquad W\sim\tfrac{3}{8b}\operatorname{sech}^4\!\big(\tfrac{z}{2b}\big)\overset d=\textstyle\sum_{n\ge2}\text{Laplace}(b/n),$$
with all terms independent. In the same way, the hyperbolic secant law
$\operatorname{sech}(z/b)/(\pi b)$ equals Laplace$(b)$ plus an independent $W$ with density
$\tfrac{2}{\pi b}\operatorname{sech}^3(z/b)$, which is $\sum_{n\ge2}$Laplace$(b/(2n-1))$.

*Two derivations.*
1. Characteristic functions. The logistic law has characteristic function $\pi bt/\sinh(\pi bt)$.
   By Euler's product, $\sinh(\pi x)/(\pi x)=\prod_{n\ge1}(1+x^2/n^2)$, so the characteristic
   function is $\prod_{n\ge1}(1+b^2t^2/n^2)^{-1}$. This is a product of Laplace$(b/n)$
   characteristic functions, and the $n=1$ factor is Laplace$(b)$. The hyperbolic secant uses
   $\cosh(\pi x/2)=\prod_{n\ge1}(1+x^2/(2n-1)^2)$.
2. R9(ii): for the logistic, $\psi'=\operatorname{sech}^2(z/2b)/(2b^2)\ge0$, and $\kappa$ is the
   stated density.

*Consequence.* At a common scale $b$ and the same orders, the Laplace price experiment
Blackwell-dominates the logistic one, at every order profile. This includes the full-order
equilibrium of the strong economy, where both laws give $(1,-1)$ under (A3).

*What this corrects.* `main.tex` lines 1877–1880 say "neither experiment Blackwell dominates the
other in general". That is false at the common scale that the paper uses. At a common variance
(logistic scale $\sqrt6\,b/\pi$) the $G$-curves do cross (`g2`, Part F, numerical diagnostic). This
is the correct scope of "neither dominates". Blackwell dominance does not order entry, because
entry $\Pr(\mu\ge\tau)$ is not convex in the posterior. So the entry comparison (0.522757 against
0.301509) remains a statement about where posterior mass sits. Online Appendix C.5 (lines 2631–2632)
instructs "do not claim ... a Blackwell ordering between the laws". That instruction should change
too. (`g3`, item 4: the characteristic functions agree to 18 digits.) $\square$

**R11 (plateau mass is maximal under Laplace; analytical).** Among symmetric unimodal
$f\in\mathcal C_L$, the full-order posterior satisfies $\Pr(\mu_X=M_L\mid H)\le\tfrac12$ and
$\Pr(\mu_X=M_L\mid L)\le\tfrac12e^{-2L}$. Laplace with $b=1/L$ attains both bounds, and it is the
only member that attains either one.

*Derivation.* By R5, $\mu_X=M_L$ needs $\psi=L$ on $[x-1,x+1]$. Unimodality gives $\psi\le0<L$ on
$(-\infty,0)$, so the plateau lies in $\{x\ge1\}$. Then
$\Pr(\mu=M_L\mid H)\le\Pr(1+Z\ge1)=\tfrac12$. On the plateau $f(x+1)=e^{-2L}f(x-1)$, so the second
bound is $e^{-2L}$ times the first. Equality needs the plateau to be all of $[1,\infty)$, so $\psi=L$
on $(0,\infty)$, which is Laplace. Attainment alone does not single out Laplace: the bimodal member
$\propto\exp(-L||z|-c|)$ also reaches the bounds on tails. Maximal attainment within symmetric
unimodal members does single it out. $\square$

**Answer to task (b).** Laplace is an extreme member of $\mathcal C_L$ in four precise senses:
- it is the least dispersed member (R8);
- it is the most informative member at every pure order profile, and a Blackwell parent of every
  log-concave member (R9, R10);
- it is the member whose posterior sits at the bounds with the largest probability (R11);
- it is the member with the largest Fisher information (R9 iii).

The proofs need $|(\log f)'|\le L<1$. Among all laws that satisfy this need with a given constant,
Laplace with $b=1/L$ adds the least noise. It is the boundary case of the class, not an arbitrary choice.

### 3.3 Gaussian noise and Kyle (task c)

**R12 (Laplace is the Gaussian with its log odds clipped; analytical).** Let $\sigma^2=b$. Under full
orders, the Gaussian log odds are $\lambda_G(x)=2x/\sigma^2=2x/b$ for all $x$. The Laplace log odds
are
$$\lambda_{\rm Lap}(x)=\operatorname{clip}\big(\lambda_G(x),-2/b,\,2/b\big).$$
For a general pure profile with gap $\Delta$, the same identity holds with $\sigma^2=b\Delta/2$ and
clip bounds $\pm\Delta/b$.
Between the two orders, the Laplace market maker updates exactly like a Kyle market maker who faces
Gaussian noise of variance $b$. The posterior there is logistic in flow,
$\mu(x)=1/(1+e^{-2x/b})$. Outside the order range the update stops. This is the precise content of
"a clean linear posterior": linear log odds where the two order distributions overlap most, with a
cap that keeps the market uncertain. (`g1`, Table 2: Gaussian with $\sigma^2=2$ gives log odds
$x$, and Laplace gives $\operatorname{clip}(x,-1,1)$.)

*Interpretation (the mode computation is analytical; the reading is heuristic).* Laplace$(b)$ is a Gaussian with an independent exponential variance
of mean $2b^2$ (R20). Given a large flow $z$, the conditional density of that variance,
$\propto v^{-1/2}\exp\{-z^2/2v-v/2b^2\}$, peaks at $v=b|z|$. At that variance, the Gaussian log odds
$2x/v$ are close to $2/b$. A very large flow is most likely a high-noise episode, so it carries no
extra information. The clip is this inference. $\square$

**R13 (what fails under Gaussian noise, and what survives; analytical).**
Fails:
1. Prop. A.1. Under any pure profile with $q_H\ne q_L$, $\lambda_G$ is affine with nonzero slope, so
   $\mu_X$ ranges over $(0,1)$: $m=0$, $M=1$, $K_f=\infty$.
2. The residual floor. $\inf_xA_H=\inf_xA_L=0$, because $\mu_X\to1$ or $0$ at extreme flows. The
   floor $\rho m\Delta_T$ is 0. At the benchmark with $\sigma=2$: $A_H(10)=0.0045$ and
   $A_H(20)=0.00003$, against a Laplace floor of $0.0448$ (`g5`, item 1).
3. The global bound. $\psi$ is unbounded, so $|F_A'|\le LF_A$ fails for every finite $L$. For the
   half-line $A=\mathbf 1[x_0,\infty)$, $F'/F$ is the Gaussian hazard, which is
   $0.76,1.41,2.59,5.05$ at $x_0=2,5,10,20$; for Laplace it is $0.5$ (`g5`, item 2). The right-hand
   side of (A3) has no positive value, no $k>0$ satisfies it, and Step 4 (uniqueness of full orders) cannot be
   proved this way.
4. Part (iii). With $M=1$, $B_r(M)=g_H(r)$. Expensive entry stays feasible until $g_H(r)=c_H$, at
   $r=7.9686$ at the benchmark, against $r_C=3.5927$ under Laplace (`g5`, item 5).
5. The low-cost floor at the benchmark. With $m=0$, (A1) becomes $c_L<g_L(r_1)=0.125$. The benchmark
   $c_L=1$ violates it. The low-cost challenger stays out when $\mu<0.105$, prices pool at $t_0$
   there, and the residual there is 0 (`g5`, item 3).

Survives:
- Part (i) of Proposition 2 (R6).
- Proposition A.3 (any fixed experiment).
- The no-trade test $\rho\Delta_T/2\le k$, so $r_N$ is unchanged.
- Price sufficiency, if $c_L<g_L(r)$.
- Proposition 1 and the auction layer.

**R14 (no affine price exists; analytical).** Take any noise law with full support (Gaussian
included) and any equilibrium with informative trading. Then the price is not affine in flow. With
an entry response, it is also discontinuous.

*Derivation.* $P(x)=t_0+e(P(x))[w_L+\Delta_T\mu_X(x)]\in[t_0,t_H]$ for almost every $x$, since
$0\le e,\mu\le1$ and $w_L+\Delta_T=t_H-t_0$. The flow has full support, so an affine $P=a+\lambda x$
with $\lambda\ne0$ leaves $[t_0,t_H]$ with positive probability. So $\lambda=0$, and the price is a
constant $\bar P$ with entry $e=e(\bar P)$. If $e>0$, (10) makes $\mu_X$ constant. If $e=0$, both
residuals are zero and no order covers its cost $k>0$. Either way trading is not informative.
Where expensive entry switches on, the price jumps by $(1-\rho)(w_L+\Delta_T\tau)$, which is $0.696$
at the benchmark (`g5`, item 6).

Kyle's linear equilibrium therefore fails here for reasons that have nothing to do with the noise
law:
- the value is binary, so its conditional mean is bounded;
- entry makes the terminal value a step function of the price;
- the investor's type is binary, so "linear strategies" are just two numbers.

What survives of Kyle's linearity is linear log odds. Laplace keeps it on the central region (R12).
Kyle (1985, Econometrica 53(6), Section 2) assumes normal value and normal noise in the single
auction. The paper already cites it; I did not re-check the theorem number. For Kyle-type models
without normality, Rochet and Vila (1994, Review of Economic Studies 61(1), 131–152; abstract
checked) prove existence and uniqueness for general distributions, in a variant where the insider
also observes noise demand. $\square$

**R15 (full orders are not an equilibrium under Gaussian noise with $\sigma^2=b$; numerical
diagnostic).** At the strong benchmark, against the schedules of the full-order profile (a
fixed-profile check):
- $\sigma=b=2$ and $\sigma=\sqrt8$ (matched variance): $(1,-1)$ is a best response for both types.
  Existence holds numerically, but uniqueness is not covered by any proof.
- $\sigma^2=b=2$ (the clipped-Gaussian match of R12): the low type's best sale is $s=0.930$
  ($c_L=1$) or $s=0.962$ ($c_L=0$), so $(1,-1)$ is not an equilibrium.

With $c_L=0$ the low-cost floor returns but full sales do not. So the cause is the absent
posterior floor and the unbounded score, not the low-cost floor. A larger sale pushes the flow to
where the market is nearly certain of low quality, and the residual vanishes there. The high type
still buys fully, because its extra flow crosses the entry threshold. This is the Section 4.3
asymmetry, here forced at $r_1$. Under Laplace noise the clip caps the posterior at $m$, and the
global bound rules this out. (`g1`, Table 5; `g5`, item 4.)

### 3.4 Proposition 2 on the class, and what is lost (task d)

**R16 (Proposition 2 for log-Lipschitz noise; analytical).** Let $f\in\mathcal C_L$ with $L<1$.
Fix $0<p<\ell<r_0<r_1<h$, $\rho\in(0,1)$, $k>0$, and suppose
$$\text{(A1$_f$)}\ \ 0\le c_L<B_{r_1}(m_f),\qquad \text{(A2$_f$)}\ \ B_{r_0}(1/2)<c_H<B_{r_1}(\bar\mu_f),\qquad \text{(A3$_f$)}\ \ \Delta_T(r_0)<k<(1-L)\rho\, m_f\Delta_T(r_1).$$
Then:
- (i) At $r_0$ the unique trading outcome is no trade, and entry is $\rho$.
- (ii) At $r_1$ the unique trading outcome is $(1,-1)$, and the price is informative. Entry is
  $\mathsf E_f=\rho+\tfrac{1-\rho}2(\alpha_H+\alpha_L)>\rho$, with
  $\alpha_\theta=\Pr(\mu_f(q_\theta+Z)\ge\tau)$ and $\alpha_H\ge\frac{\tau}{1-\tau}\alpha_L>\alpha_L$.
  High-value ownership is $\tfrac12[\rho+(1-\rho)\alpha_H]>\rho/2$.
- (iii) For $r_2\in(r_1,h)$ with $c_L<B_{r_2}(m_f)$ and $B_{r_2}(1-m_f)<c_H$, the unique trading
  outcome is $(1,-1)$ and entry is $\rho$.

The comparisons hold on a nonempty open set of primitives. Because $m\le m_f$, the paper's (A1) and
(A3) with $m=1/(1+e^{2L})$ imply (A1$_f$) and (A3$_f$). The paper's (A2) implies (A2$_f$) whenever
$\bar\mu_f=M$. This holds for Laplace, the logistic, the hyperbolic secant, and Laplace plus any
independent noise with $\mathbb Ee^{|W|/b}<\infty$ (R7 iii). It fails for Student $t$
($\bar\mu_f=0.7291<M=0.7311$ at $L=\tfrac12$).

*Derivation.* The proof of Proposition 2 runs unchanged, step by step:
- Step 1 uses R1 with $K_f$.
- Step 2 is Prop. A.2, which needs only $e\ge\rho$.
- Step 3 uses only $A\le\Delta_T$ (R6).
- Step 4 is R2 with floor $\rho m_f\Delta_T(r_1)$.
- Step 5 builds $P$ from (9) with $\mu_f$. Strict monotonicity in $\mu$ (A.3) gives the inversion.
  The price need not be monotone in flow (Student $t$), and that is harmless.
- Step 6: (A2$_f$) gives $\tfrac12<\tau<\bar\mu_f$. By the definition of the essential supremum,
  $\{\mu_f>\tau\}$ has positive Lebesgue measure, so it has positive probability because $f>0$. On
  $\{\mu_f\ge\tau\}$, $f(x-1)\ge\frac\tau{1-\tau}f(x+1)$; the integral gives the ratio bound on
  $\alpha_H/\alpha_L$.
- Blackwell ordering across economies: $f(x-1)/f(x+1)$ is not constant. Otherwise $f$ would be
  2-periodic, which no density is.
- Part (iii): every posterior is at most $1-m_f$.
- Nonemptiness: (A.25) with $\bar\mu_f>\tfrac12$.

Monotone likelihood ratio is never used. At the benchmark, Student $t$ ($\nu=3$, $L=\tfrac12$)
satisfies (A1$_f$)–(A3$_f$): the margin of (A3$_f$) is $0.00258$, and $\tau=0.705<0.7291$. Its
favourable flow set is the bounded interval $[2.4843,6.843]$, because extreme flows are
uninformative. Entry is $0.3750$ (`g1`, Table 4). $\square$

The other results of Section 4 and Appendix A carry over as follows:
- Prop. A.1: holds with $K_f$.
- Prop. A.2, Prop. A.3, Prop. A.6 (atomless costs) and Lemma OA.1: hold unchanged.
- Lemma OA.2 (general prior): holds with $\log K_f$ in place of $2/b$.
- Prop. A.4: holds with $r_U=\mathfrak r(k/[(1-L)\rho m_f])$, and $r_C$ solves
  $B_r(\bar\mu_f)=c_H$. The tie rule matters there only with a plateau (R5).
- Prop. A.5: is the logistic case.

**R17 (what the class loses; analytical, except where marked).**
1. *Closed forms.* Eq. (12) becomes $\alpha_\theta=\Pr_\theta(\mu\ge\tau)$. Explicit forms exist
   only for special members (R4).
2. *The plateau atoms and the tie rule.* These are generically absent (R5). Entry is continuous at
   $r_C$, the jump in (A.14) disappears, and the price atoms at the plateaus disappear. This is a
   simplification: the tie convention is no longer needed.
3. *The exact (A2).* Its upper bound must use $\bar\mu_f$.
4. *Monotone flows.* For members that are not log-concave (Student $t$), the price is not monotone
   in flow. Very large flows look like noise.
5. *Proposition 3.* Its certificates use three Laplace-specific tools:
   - the piecewise-logistic posterior (OA.65);
   - the identity $f''=(f-\delta_0)/b^2$ for the high-type cover bound (OA.71–OA.72);
   - elementary antiderivatives (OA.74).

   The low-type concavity argument (OA.67–OA.69) needs monotone $A_L$ and $|f'|\le f/b$, so it
   extends to log-concave members. The cover bound needs a finite-measure $f''$. New interval
   quadrature would be needed. Recertification for other laws: **open**.
6. *Benchmark numbers.* Entry at $r_1$ is $0.5228$ (Laplace), $0.3015$ (logistic), $0.3766$
   (hyperbolic secant), $0.3750$ (Student $t$), $0.4204$ (Laplace + $N(0,1)$).
7. *Sections 5.3, 6.2, 6.3 and Appendix A.5–A.7.* I did not examine these for the class: **open**.

### 3.5 One-directional trading (task e)

**R18 (buy-only and sell-only Laplace models; analytical, with numerical values).** Let orders lie
in $[0,1]$ (buy-only) or $[-1,0]$ (sell-only). Any two feasible orders differ by at most 1, so
$K=e^{1/b}$, $m_1=1/(1+e^{1/b})$, and $M_1=1-m_1$. At $b=2$, $m_1=0.3775$ and $M_1=0.6225$. Under
(A1$_1$) $c_L<B_{r_1}(m_1)$, (A2$_1$) $B_{r_0}(1/2)<c_H<B_{r_1}(M_1)$, and (A3$_1$)
$\Delta_T(r_0)<k<(1-1/b)\rho m_1\Delta_T(r_1)$, Proposition 2 holds with the same proof:
- In the buy-only model, a low type's buy is wrong-signed, so $q_L=0$ uniquely. The high type buys 1
  by R2.
- Under $(1,0)$, $\lambda(x)=(1/b)\operatorname{clip}(2x-1,-1,1)$,
  $x^*=\tfrac12(1+b\operatorname{logit}\tau)\in(\tfrac12,1)$,
  $\alpha_H=1-\tfrac12e^{(x^*-1)/b}$, and $\alpha_L=\tfrac12e^{-x^*/b}$.
- The sell-only model gives the same experiment shifted by $-1$, so its outcomes are identical
  (`g4`).

At the benchmark, $c_H=6$ lies outside the one-directional range $(4.8042,5.3122)$, against
$(4.8042,6.2172)$ for two-sided trading. Indeed $B_r(M_1)<6$ for every $r>\ell$ (the formal ceiling
is $0.94<\ell$). So entry stays at $\rho$ at $r_1=3$. With $c_H=5$:

| | $x^*$ | $\alpha_H$ | $\alpha_L$ | entry $\mathsf E$ | $\mathsf O_H$ |
|---|---|---|---|---|---|
| two-sided $(1,-1)$ | 0.3433 | 0.6399 | 0.2554 | 0.5858 | 0.3650 |
| buy-only $(1,0)$ | 0.8433 | 0.5377 | 0.3280 | 0.5746 | 0.3266 |

The larger floor lowers the full-order uniqueness bound $r_U$ from $2.837$ to $2.437$, and the
right-hand side of (A3) rises from $0.0224$ to $0.0315$. The fixed-profile check confirms a full buy
($U_H(1)=0.1608$) and no profitable low-type buy (`g4`).

*Does it simplify the proof?* Only a little. The low type's problem becomes trivial, and candidate
profiles become one-dimensional. The global step (A.6), the price construction, and the
measure-theoretic parts are unchanged. The cost is half the order range, so less information and a
narrower range for $c_H$. $\square$

**R19 (full support already removes the off-path problem; analytical).** By R6, with any
full-support noise every flow is on-path under every strategy and every deviation. The motivation for
one-directional menus in discrete models, which is to limit off-path flows and the refinements they
need, does not arise in the continuous model. There is one more link to the discrete model. With
bounded discrete noise, extreme flows reveal the state, and the residual there is 0. The Laplace
plateaus are the continuous counterpart, but they reveal only up to $m$ or $M$, so the residual stays
at least $\rho m\Delta_T$. This floor is what the global bound needs. $\square$

### 3.6 Textbook facts in the brief

**R20 (analytical; checked to 15–18 digits).** Let Laplace$(b)$ have characteristic function
$1/(1+b^2t^2)$. Then:
1. $E_1-E_2$, with $E_i$ independent exponential of mean $b$, has characteristic function
   $\frac1{1-ibt}\cdot\frac1{1+ibt}=\frac1{1+b^2t^2}$, so it is Laplace$(b)$. The convolution gives
   $\frac1{2b}e^{-|z|/b}$ directly.
2. $\sqrt V\,N$, with $N$ standard normal and $V$ exponential, satisfies
   $\mathbb Ee^{-t^2V/2}=1/(1+t^2\,\mathbb EV/2)$. This is Laplace$(b)$ if and only if $\mathbb EV=2b^2$.
3. Brownian motion at an independent exponential time $T$ is the same mixture, with $\mathbb ET=2b^2$.
4. The logistic and hyperbolic secant decompositions of R10 hold.

(`g3`.) Item 3 has an economic interpretation: Gaussian noise flow over a trading window of random,
memoryless length is Laplace. I leave its economic use to the companion memo.

## 4. What changes relative to the current paper

*Survives on the class $\mathcal C_L$, $L<1$, with the same proof:*
- Prop. A.1, with $K_f$;
- Prop. A.2 and Prop. A.3;
- Prop. A.4, with $m_f$, $\bar\mu_f$, and $L$;
- Prop. A.6, Lemma OA.1, and Lemma OA.2;
- Proposition 2, with $\bar\mu_f$ in the upper part of (A2) (R16).

The derivative bound for the class is already in Online Appendix A.3, which is stated for any
positive $f\in W^{1,1}$ with $|f'|\le Lf$. So the general result is a short addition.

*Laplace-specific:*
- eq. (12) and the threshold formula;
- the plateau atoms, the tie at $r_C$, and the jump (A.14), together with the filled and hollow
  circles at $r_C$ in Figure 2;
- the certificates of Proposition 3 (OA.65, OA.71, OA.74);
- the benchmark numbers.

*Corrections:*
1. `main.tex` lines 1877–1880 (Appendix A.4) say that neither experiment Blackwell dominates the
   other in general. At a common scale, the Laplace experiment Blackwell-dominates the logistic one
   at every order profile (R10). The two are not ordered at a common variance.
2. Online Appendix C.5 (lines 2631–2632) needs the same change.
3. `main.tex` line 860 (Section 5.1) can stay, but it can now say that the more informative law
   (Laplace) also gives higher entry at the benchmark, and that entry is not ordered by information
   in general.
4. The proof of Prop. A.5 says that the score bound "is all that" the posterior bounds and the
   derivative bound use. That is correct for the logistic law. For the class, (A2) also needs
   $\bar\mu_f=M$.

*Gaps in the current text:*
- Section 2.3 (lines 337–340) states the bounded likelihood ratio, but it does not state the score
  bound, the clipped-linear log odds, or why the choice is not arbitrary. Section 7 has a draft.

## 5. Numerical example

All values are at the benchmark, strong economy $r_1=3$, full orders, fixed profile. The scripts
reproduce the paper's values: Laplace entry $0.522757$ and ownership $0.324192$; logistic entry
$0.301509$, $x^*_{\log}=5.424598398$, and $1.495369$ noise standard deviations.

*Posterior $\mu(x)$ under full orders* (`g1`, Table 1):

| law (variance) | $x=-4$ | $-1$ | $0$ | $0.5$ | $1$ | $2$ | $4$ | $16$ |
|---|---|---|---|---|---|---|---|---|
| Laplace $b=2$ (8) | 0.2689 | 0.2689 | 0.5 | 0.6225 | 0.7311 | 0.7311 | 0.7311 | 0.7311 |
| Logistic $s=2$, matched scale (13.16) | 0.3197 | 0.4402 | 0.5 | 0.5304 | 0.5598 | 0.6117 | 0.6803 | 0.7309 |
| Logistic $s=1.559$, matched variance (8) | 0.2517 | 0.4047 | 0.5 | 0.5492 | 0.5953 | 0.6702 | 0.7483 | 0.7829 |
| Gaussian $\sigma=b=2$, matched scale (4) | 0.1192 | 0.3775 | 0.5 | 0.5622 | 0.6225 | 0.7311 | 0.8808 | 0.9997 |
| Gaussian $\sigma=\sqrt8$, matched variance (8) | 0.2689 | 0.4378 | 0.5 | 0.5312 | 0.5622 | 0.6225 | 0.7311 | 0.9820 |
| Gaussian $\sigma^2=b$, matched central slope (2) | 0.0180 | 0.2689 | 0.5 | 0.6225 | 0.7311 | 0.8808 | 0.9820 | 1.0000 |
| Hyperbolic secant, $L=\frac12$ (9.87) | 0.2773 | 0.3932 | 0.5 | 0.5566 | 0.6068 | 0.6760 | 0.7227 | 0.7311 |
| Student $t$ $\nu=3$, $L=\frac12$ (16) | 0.2710 | 0.3902 | 0.5 | 0.5578 | 0.6098 | 0.6838 | 0.7290 | 0.6156 |
| Laplace$(2)$ + $N(0,1)$ (9) | 0.2692 | 0.3686 | 0.5 | 0.5710 | 0.6314 | 0.7039 | 0.7308 | 0.7311 |

*Entry at $r_1$, and full-order best-response check* (`g1`, Tables 4–5; `g5`). "Margin" is
$(1-L)\rho m_f\Delta_T-k$:

| law | favourable flows | $\alpha_H$ | $\alpha_L$ | $\mathsf E$ | $\mathsf O_H$ | margin | $(1,-1)$ best response? |
|---|---|---|---|---|---|---|---|
| Laplace $b=2$ | $[0.8712,\infty)$ | 0.5312 | 0.1962 | 0.5228 | 0.3242 | 0.0024 | yes (proved) |
| Logistic $s=2$ | $[5.4246,\infty)$ | 0.0987 | 0.0387 | 0.3015 | 0.1620 | 0.0024 | yes (proved) |
| Logistic, matched variance | $[2.6536,\infty)$ | 0.2572 | 0.0876 | 0.3793 | 0.2215 | $-0.0070$ | yes (numerical only) |
| Gaussian $\sigma=2$ | $[1.7424,\infty)$; low cost only for $x\ge-4.29$ | 0.3552 | 0.0852 | 0.4084 | 0.2577 | n/a | yes (numerical only) |
| Gaussian $\sigma=\sqrt8$ | $[3.4849,\infty)$; low cost for $x\ge-8.57$ | 0.1898 | 0.0564 | 0.3418 | 0.1961 | n/a | yes (numerical only) |
| Gaussian $\sigma^2=b$ | $[0.8712,\infty)$; low cost for $x\ge-2.14$ | 0.5363 | 0.0929 | 0.4581 | 0.3245 | n/a | **no**: low type sells 0.930 |
| Hyperbolic secant | $[2.8174,\infty)$ | 0.2439 | 0.0937 | 0.3766 | 0.2165 | 0.0024 | yes (proved) |
| Student $t$ $\nu=3$ | $[2.4843,6.843]$ | 0.2404 | 0.0930 | 0.3750 | 0.2151 | 0.0026 | yes (proved) |
| Laplace + $N(0,1)$ | $[2.0271,\infty)$ | 0.3298 | 0.1247 | 0.4204 | 0.2487 | 0.0024 | yes (proved) |

*Blackwell comparison at full orders* (`g2`, Part F; $D=G_{\rm Lap(2)}-G_f$):
- Laplace dominates ($\min D=0$): the logistic, the hyperbolic secant, Laplace + $N(0,1)$, Student
  $t$, and Cauchy, all at $L=\tfrac12$.
- The curves cross: the matched-variance logistic ($D$ from $-0.0032$ to $0.021$), Gaussian
  $\sigma=2$, and Gaussian $\sigma=\sqrt8$.
- Gaussian $\sigma^2=b$ dominates Laplace ($\max D\approx-9\times10^{-7}$). This last result is a
  numerical diagnostic only.

*One-directional model:* see the table in R18 (`g4`).

## 6. Open issues and risks

1. **Mixed profiles for members that are not log-concave.** R9(i) covers pure profiles. Mixed
   profiles are covered for log-concave members by R9(ii). For other members, dominance at mixed
   profiles is a **conjecture**. Equilibrium profiles in Propositions 2 and 3 are pure, so the
   paper does not need it.
2. **Proposition 3 for other laws** is **open**. It needs new interval quadrature (R17, item 5).
3. **Gaussian noise.** Existence and uniqueness of informative equilibria under pure Gaussian noise
   are **open**. The numerical evidence (R15) shows that the full-order profile can fail.
4. **Sections 5.3, 6.2, 6.3 and Appendix A.5–A.7** were not examined for the class: **open**.
5. **Blackwell dominance is not more entry.** Entry $\Pr(\mu\ge\tau)$ is not convex in the
   posterior. The paper should not say that Laplace gives higher entry because it is more
   informative. At the benchmark it does, but only as a numerical fact.
6. **Hypotheses in the extremal results.** R8 needs a zero median. R11 and the uniqueness part of
   R9(iii) need symmetry and unimodality. R9(i) needs none of these.
7. **Literature.** Kyle (1985): cited by the paper; I did not re-check the theorem number here.
   Rochet and Vila (1994): abstract checked. For differential privacy, see Section 7.
8. **Presentation risk.** A class result may invite a request to switch the benchmark to the
   logistic law. I advise against it. Laplace gives the closed forms, the certificates, and (R9)
   the most informative price for the same proof constant.

## 7. Recommendation

In priority order:

1. **Add the justification paragraph to Section 2.3**, or the footnote version, both below.
2. **Replace or extend Prop. A.5 by R16**, a proposition for log-Lipschitz noise, with
   $\bar\mu_f$ in the upper part of (A2). List its members: logistic, hyperbolic secant, Student
   $t$, and Kyle Gaussian noise plus an independent Laplace component. The proof is a paragraph,
   since Online Appendix A.3 already holds at this generality.
3. **Correct the Blackwell sentences**: `main.tex` lines 1877–1880, Online Appendix C.5 lines
   2631–2632, and optionally line 860 (R10).
4. **State the extremal result** (R8–R11) as a lemma in the Online Appendix. The ODE proof of R9(i)
   takes six lines. It is the most direct answer to "why Laplace": among all laws that the global
   argument admits with constant $1/b$, Laplace with scale $b$ is the least noisy and gives the most
   informative price.
5. **Add one sentence on Gaussian noise**, with the clipped-Gaussian identity (R12) and the reason
   for failure (R13). Optionally cite R15 as a numerical diagnostic.
6. **Do not adopt one-directional trading in the continuous model** for tractability (R18–R19). At
   most add a remark: buy-only and sell-only are equivalent, the constants are $m_1,M_1$, and the
   $c_H$ range is narrower.
7. *Optional:* hyperbolic secant closed forms (R4). The Student $t$ example shows that monotone
   likelihood ratio is not needed.

*Related literature (for a footnote, if wanted).* Eq. (8) is the property that defines the Laplace
mechanism in differential privacy, with privacy parameter $\varepsilon=2/b$ and sensitivity 2:
- Dwork, McSherry, Nissim and Smith (2006), *Theory of Cryptography Conference*, LNCS 3876,
  265–284. Bibliographic data and the attribution of the Laplace mechanism were checked; I could
  not open the primary text, so the result number is **unverified**.
- Under the bounded-ratio condition alone, the noise that minimizes cost is a staircase law, not
  Laplace (Geng and Viswanath 2016, IEEE Transactions on Information Theory 62, 925–951; abstract
  checked).
- Under the stronger Lipschitz condition that the proof needs, Laplace minimizes mean-squared error
  (Koufogiannis, Han and Pappas 2015, arXiv:1504.00065; abstract checked). For symmetric noise, R8 is a stronger,
  one-dimensional form of that statement.

**Draft paragraph for Section 2.3 (231 words).**

> The Laplace density is a technical choice with a precise role. Up to a constant, its logarithm is
> $-|z|/b$, with slope $\pm1/b$. This one property has three consequences. First, for any two
> feasible orders the likelihood ratio of a flow lies in $[e^{-2/b},e^{2/b}]$. No trading strategy
> can then move the market's posterior outside $[m,M]$, so the investor always keeps a residual
> advantage. Second, a change in the order changes the flow density by at most the fraction $1/b$
> of its level. With $b>1$, this gives a lower bound on marginal trading profit over the whole order
> interval. The bound covers mixed strategies and every deviation, and it gives uniqueness in
> Proposition 2. Third, under full orders the posterior log odds equal $(2/b)\max\{-1,\min\{x,1\}\}$.
> Between the two orders they are linear in flow, exactly as under Gaussian noise with variance $b$.
> Outside the orders they are flat. The linear part gives the closed forms in (12). The flat part
> keeps the market uncertain after extreme flows. Gaussian noise has the linear log odds but not
> the bounds: extreme flows reveal quality, the residual advantage vanishes there, and the global
> argument fails. A version of Proposition 2 holds for every density whose logarithm is Lipschitz
> with a constant below one. Within that class, Laplace noise is the least dispersed law, and at the same
> orders it gives the most informative price (Appendix A.4).

**Footnote version (87 words).**

> The log Laplace density has slope $\pm1/b$. Hence the likelihood ratio of any two feasible orders
> lies in $[e^{-2/b},e^{2/b}]$, which keeps every posterior in $[m,M]$. The score bound
> $|f'|\le f/b$, with $b>1$, bounds marginal trading profit below over the whole order interval.
> Under full orders the log odds are $(2/b)\max\{-1,\min\{x,1\}\}$: linear in flow, as under
> Gaussian noise with variance $b$, and flat outside. A version of Proposition 2 holds for any density
> with $|(\log f)'|\le L<1$, and at the same orders Laplace with $b=1/L$ is the most informative such law.

## 8. Plain summary

The paper adds random "noise" orders to the investor's order. Prices then carry some information,
but not all. The supervisor asks why this noise follows a Laplace law and not the usual normal
law. This memo answers the technical side.

The proofs need two things from the noise. First, no order can make the market almost sure about the
challenger's quality. With Laplace noise, any order flow changes the odds by at most a fixed factor,
so the market's belief stays between two bounds. Second, a small change in the investor's order
changes its expected profit only in proportion to that profit. Together, they give a lower bound on
the gain from one more unit of trade, for every strategy. That bound makes the trading
outcome unique.

Any noise law whose log-density has slope at most a constant below one has both properties. Examples
are the logistic law, Student's t law, and normal noise plus an independent Laplace part. The main
result holds for all of them with the same proof. What is lost: the closed-form entry formulas, and
a tie at one strength where entry jumps.

Laplace is the extreme member of this class. It has the least noise, and it gives the most
informative price. The logistic law is exactly Laplace plus extra noise. This corrects an appendix
sentence that says the two cannot be ranked.

Normal noise fails both properties. Very large flows reveal quality, and the investor's advantage
disappears there. In one numerical case, full trading is then not optimal. Laplace keeps the
normal law's straight-line update near the centre and caps it outside. This is the precise sense of
a "clean linear posterior".

Buy-only trading does not simplify the continuous model. With full-support noise, no order flow is off the
equilibrium path.
