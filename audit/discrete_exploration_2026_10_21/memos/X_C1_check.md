# X_C1. Independent check of `C1_two_sided.md`

## 1. Scope

This memo checks the headline claims of `memos/C1_two_sided.md`: two-sided orders $q\in\{-1,0,1\}$ with discrete-Laplace noise.

- **Model.** The same as C1. $P(Z=z)=\frac{1-a}{1+a}a^{|z|}$ with $a=e^{-1/b}$, flow $X=q+Z$, prior $\tfrac12$, presence $\lambda=1$, $c_L=0$. Benchmark: $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$, $b=2$, $k=0.02$, $c_H\in\{5,6\}$.
- **Paper.** Read at the pinned commit `9b9bf3c`: main text §§2–4 and Appendix A.1–A.3.
- **Method.** I derived each claim again from the model. I wrote my own scripts before I read the author's scripts or outputs. Then I compared the numbers. Last, I ran the author's four scripts again.
- **Concepts.** I use the three concepts of C1:
  - baseline ties: perfect Bayesian equilibrium; the investor may mix at indifference; an indifferent challenger prepares (the paper's rule);
  - prescribed investor tie: the investor abstains at indifference;
  - challenger mixing: an indifferent high-cost challenger may mix.

  A statement uses baseline ties unless it says otherwise.
- **Notation.** $u=\Pr(q_H=1)$ and $v=\Pr(q_L=-1)$. Profile labels:
  - NT $(0,0)$, T $(1,1)$, BNS $(1,0)$, SNB $(0,1)$;
  - FB-PS: $u=1$, $0<v<1$; PB-FS: $0<u<1$, $v=1$;
  - PB-NS: $0<u<1$, $v=0$; NB-PS: $u=0$, $0<v<1$;
  - SYM: $u=v\in(0,1)$.

  An entry pattern $(e_+,e_0,e_-)$ gives entry at $X\ge1$, $X=0$, $X\le-1$.

Scripts are print-only. They sit in `scripts/X_C1_check/`, with each output beside its script.

| Script | Content | Precision |
|---|---|---|
| `exact.py` | posteriors by direct convolution; constants, window, ceilings, thresholds; corner algebra; nets; branch points; checks of the omitted equilibria | 50 digits |
| `enumerate.py` | all baseline-tie equilibria on $[0,1]^2$ (corners, edges, interior); $r\in[1.40,1.95]$ in steps of $0.0025$, plus 18 other strengths; jump-line scans | double |
| `interior.py` | second interior search (contour trace) and a direct solve on the diagonal | double |
| `branches_extra.py` | end points of the branches that C1 omits | double |
| `rerun/` | outputs of the author's four scripts, run again | as the author's |

Every script ran through the slot wrapper. The longest run took 60 seconds.

## 2. Verdict table

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | At most three posterior values; full orders give $(M,\tfrac12,m)\approx(0.731,0.5,0.269)$ (analytical) | CONFIRMED | §3.1. The result holds for every strategy pair, also with wrong-signed orders and any prior. The spread inside a flow class is at most $3\times10^{-51}$. |
| 2 | Proposition 2 analog under (D1)–(D3) (analytical) | CONFIRMED | §3.2. Uniqueness holds against every mixed strategy and every two-sided deviation. A grid check over $66^2$ strategy pairs agrees. Two wording fixes (E5). |
| 3 | Window $c_H\in(4.804167,6.217155]$; ceilings $3.592659$ ($c_H=6$) and $6.325302$ ($c_H=5$) (analytical) | CONFIRMED | §3.3. Values agree to 50 digits. |
| 4 | NT and T coexist on $[1.515898,1.747878]$, also at 1.55, 1.60, 1.65 (analytical) | CONFIRMED | §3.4. Both end points are closed forms. The nets agree to 6 decimals. |
| 5 | Buyer inframarginal, seller marginal; BNS exists; recruited SNB impossible when $a>\rho$ (analytical) | CONFIRMED WITH CORRECTION | §3.5. The corner algebra is exact. The general statement has no proof, and it fails on a PB-NS branch for $c_H=5$ and at constant entry (E4). |
| 6 | FB-PS branch only on $(1.515898,1.533807)$; wider branches need challenger mixing (numerical diagnostic) | CONFIRMED WITH CORRECTION | §3.6. The recruited window is exact and has a short proof. "Only" is false: for $c_H=6$ an FB-PS branch with entry $\rho$ exists on $(1.819330,1.840115)$ (E1). |
| 7 | Entry order across strengths fails (T entry flat at 0.569293; mixing-branch entry falls) | CONFIRMED WITH CORRECTION | §3.7. This is true at 1.55, 1.60 and 1.65. But a second baseline branch has entry that rises with $r$: PB-NS for $c_H=5$ on $(1.405430,1.443322)$ (E2). |
| 8 | Two-sided entry at $r_1$ is 0.569293, not the buy-only 0.625 | CONFIRMED | §3.8. The value 0.625 applies to $c_H=5$ only. Buy-only entry at $c_H=6$ is 0.25. |
| S | $r_C=3.592659$ and $r_N=1.747878$ equal the paper's values | CONFIRMED, exact | §3.9. The two equalities have different reasons. |

No headline number in C1 is wrong. No claim is refuted. The corrections concern the completeness of Result 5 and one label.

## 3. Derivations and evidence

### 3.1 Claim 1: three posterior values

Take any order laws $\sigma_H,\sigma_L$ on $\{-1,0,1\}$, with wrong-signed orders allowed. With $f(z)\propto a^{|z|}$,

$$
\frac{a_\theta(x)}{f(x)}=\sigma_\theta(0)+\sigma_\theta(1)\frac{f(x-1)}{f(x)}+\sigma_\theta(-1)\frac{f(x+1)}{f(x)}.
$$

The two ratios are $(a^{-1},a)$ on $x\ge1$, $(a,a)$ at $x=0$ and $(a,a^{-1})$ on $x\le-1$. So $a_\theta(x)/f(x)$ depends on $x$ only through its class. The posterior $\mu=\pi a_H/(\pi a_H+(1-\pi)a_L)$ therefore takes at most three values, for every prior $\pi$.

Under full orders the class values are:

- $\mu_+=a^{-1}/(a^{-1}+a)=1/(1+a^2)$;
- $\mu_0=a/(2a)=\tfrac12$;
- $\mu_-=a^2/(1+a^2)$.

Since $a^2=e^{-2/b}$, these are $M$ and $m$ of paper eq. (7).

Evidence (`exact.py`, §A):

- Seven strategy pairs, three of them with wrong-signed orders: the spread inside each class is at most $2.7\times10^{-51}$.
- The full-order posterior equals paper eq. (A.8) at each integer in $[-12,12]$, to $1.3\times10^{-51}$.
- On a $66^2$ grid of strategy pairs, $\mu\in[0.268941,0.731059]$. Only full orders reach the bounds.
- At prior $0.3$ the three values are $(0.538102,0.3,0.136190)$.

C1 proves the three classes only for candidates $(u,v)$. That suffices after the dominance step. The form above needs no dominance step. The label "analytical" is deserved.

### 3.2 Claim 2: Proposition 2 analog

My derivation:

1. **Floor.** $g_L=(\ell^2-p^2)/(2r)>0=c_L$. So the low-cost type prepares at every belief, and entry is at least $\rho$ after every price.
2. **Price sufficiency.** $P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X]$ with $e(P)\ge\rho$ makes $\mu_X$ a function of $P$. This also holds if the challenger mixes at indifference.
3. **Residuals.** $\mathbb E[V_T\mid\theta,x]=t_0+e(x)(t_\theta-t_0)$. So $\mathbb E[V_T\mid H,x]-P(x)=e\Delta_T(1-\mu)$ and $P(x)-\mathbb E[V_T\mid L,x]=e\Delta_T\mu$. The script computes payoffs from $t_0,t_H,t_L$ directly. They agree with these residual forms to $10^{-51}$.
4. **Payoffs.** A unit buy by $H$ earns $G_H-k$, with $G_H=\sum_x f(x-1)\,e\,\Delta_T(1-\mu)$. A unit sale by $H$ earns at most $-k$. The mirror statements hold for $L$.
5. **Bounds.** Since $e\in[\rho,1]$ and $\mu\in[m,M]$: $\rho m\Delta_T\le G_H,G_L\le\Delta_T$.
6. **At $r_0$.** $\Delta_T(r_0)=0.016667<k$. Each nonzero order of each type earns a negative amount against every candidate schedule. A mixture with weight on a nonzero order earns less than zero. So $(0,0)$ is the only outcome. The posterior is $\tfrac12$, and $B_{r_0}(\tfrac12)=4.804167<c_H$ gives entry $\rho$.
7. **At $r_1$.** $\rho m\Delta_T(r_1)=0.044824>k$. Against every candidate, the correct order earns more than zero, and zero earns more than the wrong order. So $(u,v)=(1,1)$ is the only outcome. Entry is $(1,\rho,\rho)$ because $B_{r_1}(\tfrac12)<c_H\le B_{r_1}(M)$.
8. **At $r_2$.** $\Delta_T$ rises in $r$, so step 7 applies again. $B_{r_2}(M)<c_H$ and $\mu\le M$ give entry $\rho$.

Numbers (`exact.py`, §G, direct sums over flows):

- $\mathsf E(r_1)=0.5692934958$ and $\mathsf O_H(r_1)=0.3584222492$ for both $c_H$.
- $\mathsf E(3.6)=0.25$ for $c_H=6$, and $0.569293$ for $c_H=5$.
- Prices at $r_1$: $1.362372$, $0.614583$, $0.576074$.

Brute-force check over $66^2$ strategy pairs, with wrong-signed orders, for both $c_H$:

- at $r_0$ the best nonzero order earns at most $-0.010993$;
- at $r_1$ the correct order beats every other order by at least $0.048300$.

The proof in C1 is complete. Two wording points (E5):

- Step 6 calls the region open, but (D1) and (D2) are weak inequalities. The strict versions define an open, nonempty set. The benchmark meets them strictly.
- At $c_H=B_{r_1}(M)$, entry is unique only under the prepare tie. Under challenger mixing, $e_+$ can take any value in $[\rho,1]$.

### 3.3 Claim 3: window and ceilings

- $B_{r_0}(\tfrac12)=4.804166667$ and $B_{r_1}(M)=6.217154822$. The right end is closed: $\mu=M$ has positive probability, and the indifferent challenger prepares.
- The buy-only top is $B_{r_1}(M_1)=5.312161$. The two-sided window is wider by $0.904994$.
- $B_r(M)=Mh-\tfrac{Mr}{2}+\tfrac{(1-M)\ell^2-p^2}{2r}$ falls strictly in $r$. Its crossing with $c_H$ is paper eq. (A.11).
- $c_H=6$: $r_C=3.592658518795$. $c_H=5$: $r_C=6.325301769278$. The residual $B_{r_C}(M)-c_H$ is zero to 50 digits.
- Buy-only ceilings: $3.986097$ for $c_H=5$. For $c_H=6$ none exists above $r=1$, because $B_1(M_1)=5.977134<6$.

The label "analytical" is deserved.

### 3.4 Claim 4: coexistence of NT and T

- **NT.** Under NT, $\mu=\tfrac12$ at every flow. A unit deviation earns $\rho\Delta_T/2-k$. So NT exists exactly when $r\le r_N=\mathfrak r(2k/\rho)=1.747877538$.
- **T.** Under T, $G_H=G_L=\Delta_T[J(e_++e_-)+\phi e_0/2]$, where $J=\beta m=\delta M=a^2/((1+a)(1+a^2))=0.167405$. With entry $(1,\rho,\rho)$ the coefficient is $c_T=J(1+\rho)+\phi\rho/2=0.227825206$. So T exists exactly when $r\ge\mathfrak r(k/c_T)=1.515898365$.
- **Pattern.** On the whole interval, $B_r(M)\ge6.677>6$ and $B_r(\tfrac12)\le4.704<5$. So entry under T is $(1,\rho,\rho)$ for both $c_H$.
- **Nets.** Closed forms and direct sums agree:

| $r$ | NT deviation net | T net |
|---|---|---|
| 1.55 | $-0.007802$ | $+0.002231$ |
| 1.60 | $-0.005938$ | $+0.005630$ |
| 1.65 | $-0.003996$ | $+0.009169$ |

The feedback numbers of C1 also hold. At $r_1$, full trade nets $+0.131883$ with recruitment and $+0.048181$ without. Buy-only trade nets $+0.175836$ and $+0.058335$. The label "analytical" is deserved.

### 3.5 Claim 5: which side is marginal

What I confirm:

- **Symmetric points.** At $u=v=s$: $\beta B_+-\delta A_+=[(1-sd)-a^2(1+sd/a)]/(1+a)=d(1-s)$. So $G_H-G_L=\Delta_T(e_+-e_-)\,d(1-s)/S_+$, as C1 states.
- **BNS with recruitment.** The buy coefficient is $\alpha\beta(1+\rho)=0.293755$. The sale-deviation coefficient is $\delta M_1+\rho m_1(\phi+\beta)=0.215309$. The gap $(1-a)\alpha(\beta-\rho\alpha)=0.078446$ is positive. The window is $r\in[1.443322,1.533807]$ where $B_r(M_1)\ge c_H$, so for $c_H=5$.
- **SNB with recruitment.** At $(0,1)$, $\mu_+=\mu_0=M_1$, so recruitment at $+$ implies recruitment at $0$. The buy-deviation coefficient $0.326722$ exceeds the sale coefficient $0.293755$. The gap is $(1-a)\alpha(\alpha-\rho\beta)=(1-a)\alpha(a-\rho)/(1+a)$. It is positive exactly when $a>\rho$. The case list is complete.
- **Constant entry.** The game is then a mirror image: $G_H(u,v)=G_L(v,u)$. For $c_H=6$, BNS and SNB both exist on $[1.777986,1.819330]$.
- **Jump lines.** At $r=1.55,1.60,1.65$ and on the line $\mu_+=\tau$, $e_L^*-e_H^*$ stays in $[0.042,0.399]$. On the line $\mu_0=\tau$ ($c_H=5$) the buyer is strict. So no point with both types indifferent exists, as C1 states.

What does not hold:

- The general claim "the buyer is inframarginal and the seller is marginal" has no complete proof. The step "a jump-curve equilibrium must put $H$ at a corner" rests on the numerical branch solves of Result 5. The label "analytical" covers only the identity and the corner algebra.
- The claim fails on a branch that C1 does not report. For $c_H=5$ and $r\in(1.405430,1.443322)$, $H$ mixes and $L$ abstains strictly, with entry $(1,\rho,\rho)$ (§3.7). There the buyer is the marginal type. The $c_H=5$ challenger-mixing branch of C1 also has a marginal buyer.
- At constant entry both directions occur. At $r=1.825$ and $c_H=6$, both $(1,0.081665)$ and $(0.081665,1)$ are equilibria.

What survives:

- In every equilibrium found with entry above $\rho$, $u\ge v$.
- Recruited SNB is impossible when $a>\rho$ (analytical).

### 3.6 Claim 6: the full-buy / partial-sell branch

On the edge $u=1$, $\mu_0\le\tfrac12<\tau$. So the pattern is $(1,\rho,\rho)$ where $\mu_+\ge\tau$, and $(\rho,\rho,\rho)$ elsewhere.

**Recruited part: the window is exact.** Write $w=vd$. Then $\mu_+=1/(1+a(1-w))$, $\mu_0=a/(1+a-w)$ and $\mu_-=a^2/(a^2+a+w)$. Two slope results follow.

- For $L$:
  $$
  \tfrac{1+a}{a}\,\partial_w\frac{G_L}{\Delta_T}=\frac{a^2}{(1+a-aw)^2}+\frac{\rho ad}{(1+a-w)^2}-\frac{\rho a}{(a^2+a+w)^2}.
  $$
  The first two terms grow in $w$, and the third term shrinks. So the minimum is at $w=0$, where the expression equals $(a^2+\rho ad-\rho/a)/(1+a)^2$. At the benchmark, $a^2+\rho ad-\rho/a=0.015362>0$. So $G_L(1,v)$ rises strictly in $v$.
- For $H$:
  $$
  \tfrac{1+a}{a}\,\partial_w\frac{G_H}{\Delta_T}=-\frac{1}{(1+a-aw)^2}-\frac{\rho ad}{(1+a-w)^2}+\frac{\rho a^3}{(a^2+a+w)^2}\le\frac{-1+\rho a^2}{(1+a)^2}<0.
  $$
  So $G_H(1,v)$ falls strictly in $v$, for all parameters.

So the indifference root of $L$ is unique. It exists exactly when $G_L(1,0)<k<c_T\Delta_T$. At the root $G_H(1,v)>G_H(1,1)=c_T\Delta_T>k$, so $H$ buys strictly. This gives:

- $c_H=5$: $r\in(1.515898,1.533807)$;
- $c_H=6$: $r\in(1.515898,1.532313)$. The upper end is where the root meets $\mu_+=\tau$ (a one-dimensional root, found numerically).

The branch values agree: $v=0.863389,0.670587,0.418994$ and $\mathsf E=0.576904,0.587644,0.601659$ at $r=1.520,1.525,1.530$. C1 calls the two monotonicity facts diagnostic. At the benchmark they are analytical.

**"Only" is false.** At constant entry, $G_L(1,v)/(\rho\Delta_T)$ is U-shaped. It falls from $0.433625$ at $v=0$ to about $0.40884$ near $v=0.9$, then rises to $0.409086$ at $v=1$. For $c_H=6$, the constant pattern needs $v<v_\tau(r)\approx0.36$. A root lies there for $r\in(1.819330,1.840115)$. $H$ buys strictly, with net about $+0.0017$. Entry is $\rho$.

A 50-digit check at $r=1.825$, $c_H=6$ (`exact.py`, §L):

- $v=0.081665$; posteriors $(0.630103,0.385246,0.365488)$, all below $\tau=0.657458$;
- $H$: buy $+0.001764$, sale $-0.046618$;
- $L$: sale $0$, buy $-0.044854$.

So a second FB-PS branch exists under baseline ties. It has no feedback. For $c_H=5$ no constant-entry FB-PS exists, because $\mu_+\ge M_1>\tau$ on the edge.

**"Wider branches need challenger mixing": confirmed.** On $(1.533807,1.747878]$ my enumeration finds only NT and T, for both $c_H$. The mixing points agree to six decimals:

| $r$ | $c_H=6$: $v^*$ | $e_L^*$ | $\mathsf E$ | $c_H=5$: $u_p$ | $e_H^*$ | $\mathsf E$ |
|---|---|---|---|---|---|---|
| 1.55 | 0.253308 | 0.923037 | 0.573855 | 0.228270 | 0.536787 | 0.366291 |
| 1.60 | 0.272646 | 0.739324 | 0.484753 | 0.240749 | 0.444215 | 0.329050 |
| 1.65 | 0.291865 | 0.594346 | 0.414708 | 0.253260 | 0.370460 | 0.299215 |

The mirror point $(u^*,1)$ for $c_H=6$ fails. $L$'s net at $e_H^*$ is $-0.0022$, $-0.0015$ and $-0.0008$.

### 3.7 Claim 7: entry across strengths

- Under T with pattern $(1,\rho,\rho)$, $\mathsf E=\rho+(1-\rho)\frac{1+a^2}{2(1+a)}=0.569293$. This value does not depend on $r$. It holds up to $r_C$.
- At $r=1.55,1.60,1.65$ the baseline-tie equilibria are NT and T only, for both $c_H$. Entry takes only the values $0.25$ and $0.569293$. So no strictly upward triple exists at the paper strengths.
- Both challenger-mixing branches have entry that falls in $r$ (table in §3.6).

Correction. C1 says that only the narrow FB-PS branch has entry that rises in $r$. A second baseline branch has this property. For $c_H=5$ on $(1.405430,1.443322)$:

- $H$ mixes with $u\in(0.192244,1)$, and $L$ abstains strictly. Entry is $(1,\rho,\rho)$.
- Entry rises from $0.550812$ to $0.625$. At $r=1.41,1.42,1.43$ it is $0.558559$, $0.576414$, $0.595797$.
- NT coexists, because $r<r_N$.
- A 50-digit check at $r=1.42$ gives $u=0.470999$. $H$: buy net $0$, sale $-0.032767$. $L$: sale $-0.006571$, buy $-0.044525$.

The branch ends at BNS ($u=1$, $r=1.443322$). At its lower end it meets the $c_H=5$ challenger-mixing branch of C1, with $e_H^*=1$.

So for $c_H=5$, three informative equilibria with upward entry coexist with NT, for example at 1.41, 1.42 and 1.43. Their form differs from Proposition 3: partial buys and no sales, not full buys and partial sales. The narrow FB-PS branch is the only one in the paper's form. Its sale probability falls in $r$, unlike the paper's $v_j$.

### 3.8 Claim 8: entry at $r_1$

- Two-sided menu: T is unique (§3.2), so $\mathsf E=0.5692934958$.
- Buy-only menu, $c_H=5$: $P(X\ge1)=(\alpha+\beta)/2=\tfrac12$, so $\mathsf E=0.625$.
- Buy-only menu, $c_H=6$: $B_{r_1}(M_1)=5.312<6$, so entry is $0.25$. The comparison with 0.625 applies to $c_H=5$ only.
- In the two-sided menu, $(1,0)$ fails at $r_1$. $L$'s sale earns $+0.123539$ for $c_H=5$ and $+0.052271$ for $c_H=6$.
- $\mathsf O_H=0.358422$ in both menus.

### 3.9 Special point: $r_C$ and $r_N$

Both equalities are exact. Their reasons differ.

**$r_C$.** The discrete law is $p(z)=\frac{1-a}{1+a}e^{-|z|/b}$. This is the Laplace density restricted to $\mathbb Z$, up to a constant. Orders are integers, so flows are integers. Bayes' rule uses only the ratios $p(x-q)/p(x-q')=e^{(|x-q'|-|x-q|)/b}$. These equal the Laplace ratios at the same points. So the full-order posterior is paper eq. (A.8) restricted to $\mathbb Z$: $M$ on $x\ge1$, $\tfrac12$ at $0$, $m$ on $x\le-1$. In both models $M$ is the largest posterior, and it has positive probability. So $r_C$ solves the same equation $B_r(M)=c_H$ with the same $M$. The 50-digit value $3.5926585187947$ rounds to the paper's $3.592658519$.

**$r_N$.** Under no trade, $\mu=\tfrac12$ at every flow, for any noise law with full support. A unit deviation earns $\rho\Delta_T/2-k$. In the paper a deviation of size $s$ earns $s(\rho\Delta_T/2-k)$ (eq. A.12). The boundary $\rho\Delta_T(r)/2=k$ does not involve the noise law. So $r_N=\mathfrak r(2k/\rho)=1.7478775383$ in both models. In the three-point model, flows $\pm2$ are off path, and the factor changes to $1/3$.

**Paper objects that the discrete model reproduces exactly:**

- the posterior bounds $m,M$ (eq. 7), and the full-order posterior on the integers (eq. A.8);
- $\mathfrak r(k)=1.220997512$, the sufficient bound for unique no trade (it does not depend on the noise law either);
- the end points of the $c_H$ window (A2): $4.804167$ and $6.217155$ (the right end is closed here);
- $r_N$, $r_C$, and the residual bounds of eq. (11);
- entry $0.25$ and ownership $0.125$ at $r_0$; the return to $0.25$ at $r_2=3.6$ for $c_H=6$; the hidden-price control.

**Paper objects that it does not reproduce:**

| Object | Paper | Discrete | Reason |
|---|---|---|---|
| $r_U$ | 2.837417 | 2.124148 | unit orders need no factor $1-1/b$ |
| upper bound on $k$ in (A3) | 0.022412 | 0.044824 | the same |
| $x^*,\alpha_H,\alpha_L$ (eq. 12) | continuous threshold | three classes, masses $\beta,\delta$ | coarse flow classes |
| $\mathsf E(r_1)$, $\mathsf O_H(r_1)$ | 0.522757, 0.324192 | 0.569293, 0.358422 | the mass with $\mu\ge\tau$ differs |
| entry as $r\uparrow r_C$ (A.14) | 0.506477 | 0.569293, flat | discrete entry does not move with $\tau$ below $M$ |
| fixed-experiment control | 0.562178 to 0.522757 | 0.569293 at both | the same; deterrence is only weak |
| Prop. 3 values $v_j$, $\mathsf E_j$ | both rise in $r$ | only NT and T at 1.55–1.65 | §3.7 |
| full-order existence test (A.7) | $k<(1-1/b)J$ | $k\le c_T\Delta_T$, $r\ge1.515898$ | no printed paper value |

### 3.10 Concept, belief rule, tie rules, labels

- C1 states the equilibrium concept (perfect Bayesian). Every integer flow has positive probability under every strategy and every deviation. So no off-path flow and no off-path price occur. C1 is right that no refinement is needed.
- C1 states the tie rules and uses them consistently. Prop. C1.1 and the corner results use baseline ties. The end points of the coexistence interval apply the prescribed investor tie correctly. Challenger mixing appears only in labelled branches.
- Minor: §2 of C1 says "two nested concepts" but lists three. They nest as: prescribed investor tie ⊂ baseline ties ⊂ challenger mixing.
- Labels:
  - Results 1–3 and Prop. C1.1 deserve "analytical".
  - Result 4 deserves it only in part (§3.5).
  - Result 5 is correctly labelled "numerical diagnostic", but part of it has a proof (§3.6).

### 3.11 Numbers against scripts

- I checked each number in the tables of C1 and in Results 1–5 against my own computation. All agree to the printed digits. Examples: $c_T=0.227825$, $J=0.167405$, $P_+=0.425725$, the BNS and SNB coefficients, the branch and mixing tables, and the §5 table of $B_r$ and $\tau$.
- I ran the author's four scripts again through the slot wrapper. Each output is byte-identical to its saved `*_out.txt` (see `scripts/X_C1_check/rerun/`).
- The interior and edge searches in C1 use $r\in\{1.2,1.4,1.525,1.55,1.6,1.65,1.9,3,3.6\}$. None of these lies in $(1.405,1.443)$ or $(1.748,1.840)$. This explains the omissions in §4.
- At $r=1.9$, $c_H=6$, the C1 output shows a sign change of $e_H^*-e_L^*$ on the jump line. There the common value is about $0.166<\rho$, so it is not an equilibrium. C1 is right to omit it.

### 3.12 Baseline-tie equilibrium map (numerical diagnostic)

The three double-precision scripts give the map below. End points come from closed forms or one-dimensional roots. Each omitted branch was checked at one point with 50-digit direct sums (`exact.py`, §L).

$c_H=5$:

| $r$ | Equilibria | Entry |
|---|---|---|
| $[1.2,1.405430]$ | NT | 0.25 |
| $(1.405430,1.443322)$ | NT; PB-NS with $(1,\rho,\rho)$ | 0.25; 0.5508 to 0.625 |
| $[1.443322,1.515898)$ | NT; BNS | 0.25; 0.625 |
| $[1.515898,1.533807]$ | NT; BNS; FB-PS; T | 0.25; 0.625; 0.5693 to 0.625; 0.569293 |
| $(1.533807,1.747878]$ | NT; T | 0.25; 0.569293 |
| $(1.747878,1.764025)$ | SYM; T | 0.25; 0.569293 |
| $[1.764025,6.325302]$ | T | 0.569293 |
| above $6.325302$ | T | 0.25 |

$c_H=6$:

| $r$ | Equilibria | Entry |
|---|---|---|
| $[1.2,1.515898)$ | NT | 0.25 |
| $(1.515898,1.532313)$ | NT; FB-PS with $(1,\rho,\rho)$; T | 0.25; 0.5693 to 0.6113; 0.569293 |
| $[1.532313,1.747878]$ | NT; T | 0.25; 0.569293 |
| $(1.747878,1.766966)$ | SYM; T | 0.25; 0.569293 |
| $[1.766966,1.767007]$ | SYM; PB-NS; NB-PS; a mirror pair of asymmetric interior points; T | 0.25; 0.569293 |
| $(1.767007,1.777986)$ | SYM; PB-NS; NB-PS; T | 0.25; 0.569293 |
| $[1.777986,1.813782)$ | SYM; BNS; SNB; T | 0.25; 0.569293 |
| $[1.813782,1.819330]$ | BNS; SNB; T | 0.25; 0.569293 |
| $(1.819330,1.835142)$ | FB-PS; PB-FS; T | 0.25; 0.569293 |
| $[1.835142,1.840115)$ | FB-PS; T | 0.25; 0.569293 |
| $[1.840115,3.592659]$ | T | 0.569293 |
| above $3.592659$ | T | 0.25 |

Notes:

- Every omitted branch above $r_N$ has entry $\rho$. These branches are the discrete analog of the paper's "symmetric interior family" with entry $\rho$ (§4.3).
- At constant entry, $G_H-G_L$ is $\rho\Delta_T(r)$ times a function of $(u,v)$ alone. Its zero set off the diagonal is one fixed curve from $(0,0.393469)$ to $(0.393469,0)$. Along it, $G_H/(\rho\Delta_T)$ stays in $[0.480573,0.480613]$. So asymmetric interior equilibria exist only for $r\in[1.766966,1.767007]$. The pair starts on the edges at $1.766966$, where PB-NS and NB-PS begin. It merges into SYM at $1.767007$.
- For $c_H=5$, the SYM family leaves the constant pattern at $1.764025$, before that curve. So no asymmetric interior equilibrium occurs for $c_H=5$.
- No equilibrium with pattern $(1,1,\rho)$ was found.
- The PB-FS branch leaves the constant pattern at $1.835142$, with $v=0.256171$ (`branches_extra.py`, §5).

## 4. Errors found and corrections

1. **E1 (claim 6).** "A full-buy and partial-sell branch exists only in a narrow window" is false as written. For $c_H=6$, a second FB-PS branch exists on $(1.819330,1.840115)$, with entry $\rho$. Its mirror PB-FS exists on $(1.819330,1.835142)$. Correction: "With entry above $\rho$, an FB-PS branch exists only on $(1.515898,1.533807)$ for $c_H=5$ and on $(1.515898,1.532313)$ for $c_H=6$."
2. **E2 (claim 7).** "Only the narrow baseline branch has rising entry" is false. For $c_H=5$, a PB-NS branch with recruitment on $(1.405430,1.443322)$ has entry from $0.550812$ to $0.625$, and NT coexists with it.
3. **E3 (Result 5).** The map lists corners only, and the text implies that no mixed baseline equilibrium exists outside the narrow window. §3.12 lists the omitted branches. Under baseline ties and on the grid, the equilibrium set is T alone only from $1.764025$ ($c_H=5$) and from $1.840115$ ($c_H=6$).
4. **E4 (Result 4, label).** "Analytical" covers the symmetric identity and the corner algebra only. The jump-curve step is numerical. "Buyer inframarginal, seller marginal" fails on the PB-NS branch of E2 and at constant entry.
5. **E5 (Prop. C1.1, wording).** Openness needs strict (D1) and (D2). At $c_H=B_{r_1}(M)$, unique entry needs the prepare tie.
6. **E6 (§2, wording).** "Two nested concepts" should read "three nested concepts".
7. **E7 (an upgrade, not an error).** The two slope results of §3.6 make the narrow window analytical at the benchmark. Only the $c_H=6$ end point $1.532313$ stays numerical.

## 5. What the original memo should change

1. §1, short answer: add "with entry above $\rho$" to the bullet on the full-buy, partial-sell branch. Add a bullet on the PB-NS branch for $c_H=5$.
2. Result 5: add the map of §3.12, or state that the corner map omits mixed equilibria. Name the strengths where they occur.
3. Result 5, "Verdict on Proposition 3 features":
   - remove "Only the narrow baseline branch has rising entry";
   - state that for $c_H=5$ the PB-NS branch also has upward entry and coexists with NT.
4. Result 5, narrow branch: replace "(diagnostic)" with the two slope results of §3.6. Label the window analytical.
5. Result 4: split the label. Restrict "buyer inframarginal" to the FB-PS branches. State the mirror symmetry at constant entry.
6. Prop. C1.1, Step 6: use strict (D1) and (D2) for the open set. Name the tie rule that makes entry unique at $c_H=B_{r_1}(M)$.
7. §2: change "two nested concepts" to "three nested concepts".
8. §4: give the two reasons for the exact match of $r_C$ and $r_N$ (§3.9). Add the table of paper objects that do not match.
9. Plain summary: qualify "Full buys with mixed sells occur only near one threshold" with "when entry rises above $\rho$".
10. Searches: add sample strengths in $(1.40,1.45)$ and $(1.74,1.85)$.

## 6. Plain summary

I checked the memo on two-sided orders with my own derivations and scripts. Every number in it is correct. Its scripts reproduce their saved outputs exactly.

The core results hold. Beliefs take three values, and full trade gives the paper's bounds 0.269 and 0.731. A weak incumbent gives no trade. A strong incumbent gives full two-sided trade. Uniqueness holds against every mixed strategy and every deviation. Entry rises from 0.25 to 0.569. No trade and full trade coexist between 1.516 and 1.748.

The paper's ceiling 3.592659 and no-trade boundary 1.747878 match exactly. The ceiling matches because the discrete law is the Laplace density on the integers. The boundary matches because it never depends on the noise law. The uniqueness bound, the entry levels and the Proposition 3 values do not match.

The memo misses some equilibria. For $c_H=6$, a second full-buy, partial-sell branch with entry 0.25 exists near 1.82–1.84. For $c_H=5$, a partial-buy branch near 1.41–1.44 has entry that rises with strength, and no trade coexists with it. So two "only" statements need correction. The claim that the buyer is always inframarginal is too strong.
