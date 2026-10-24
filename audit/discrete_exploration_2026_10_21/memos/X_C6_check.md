# X_C6. Independent check of the costly-acquisition memo

Object checked: `memos/C6_info_acquisition.md`. Its SHA-256 starts `d3eeb9d0615259b0`, the same value as in the author's run record.
My script: `scripts/X_C6_check/check.py`. Its output: `scripts/X_C6_check/output.txt`. The run takes 18 seconds.
A helper, `compare_memo_numbers.py`, matches memo numbers to outputs. A copy of the author's run is in `author_run.txt`.

## 1. Scope

This check covers seven headline claims and five side items.

Headline claims:

1. Equal noise: exact research cutoff, no robust coexistence, no entry feedback.
2. Discrete-Laplace noise, $r=3$, $c_H=5$, $\kappa=0.05$: no research and full research are both equilibria.
3. $\kappa=0.02$, $c_H=5$: research is unique at each strength, and entry goes $0.25\to0.625\to0.25$.
4. The paper's $c_H=6$ blocks expensive entry at every permitted strength.
5. Public acquisition removes the benchmark coexistence.
6. Research can cut welfare even when it raises entry.
7. The no-response purchase profit at $r_1$ is $0.058334570734\ldots$, not $0.060$.

Side items: order of events; mixed $\psi$; equilibrium concept, off-path rule, and both tie rules; status labels; memo numbers against script output.

Method:

- I read the memo first. I wrote my script before I opened the author's script and its output file.
- Auction objects and equal noise use exact fractions. Discrete-Laplace work uses 50 digits.
- I re-derived the auction objects by exact integration over $R\sim U[0,r]$. They equal equation (4) of the pinned paper at $r=1.2,\,3,\,3.6,\,4.2$.
- I compute each purchase return two ways. The first is a direct sum over integer flows $|z|\le300$; the omitted noise mass is $5.4\times10^{-66}$. The second is my own two-region closed form. The two differ by at most $2.4\times10^{-51}$.
- After that, I compared with the author's output. I also ran the author's script into my folder. It reproduces the saved `results.txt` byte for byte. The script has no assertion.

Not checked: the $\kappa=0.06$ strength sweep, the Section 4 comparison table, the literature paragraph, and every case with $\pi\ne1/2$. For the sweep I compared the memo with the author's output only.

## 2. Verdict table

| # | Claim (label in memo) | Verdict | Evidence |
|---|---|---|---|
| 1 | Equal noise: exact cutoff, no robust coexistence, no entry feedback (analytical) | CONFIRMED | $D=\tfrac23\rho(1-\pi)\Delta_T$ for every $s$. $\bar V_3=0,\ 4/225,\ 629/21600$ at $r=1.2,\,3,\,3.6$. $r_\kappa=2.571054535759$ at $\kappa=1/100$. $\mathsf E=\rho+(1-\rho)\pi\psi/3$. |
| 2 | Coexistence at $r=3$, $c_H=5$, $\kappa=0.05$ (analytical) | CONFIRMED | $v_0=19/600=0.031667<0.05<v_1=0.087918213417$. Exact chain $19/600<1/20<561/6400$. Holds under small moves of $k$, $r$, $c_H$. |
| 3 | $\kappa=0.02$: unique research, entry $0.25\to0.625\to0.25$ (analytical) | CONFIRMED at $r=1.2,\ 3,\ 4.2$ | $\psi=0,1,1$. Entry $1/4,\ 5/8,\ 1/4$. At the paper's $r_2=3.6$ research is unique but entry stays $5/8$. |
| 4 | $c_H=6$ blocks expensive entry at every strength (analytical) | CONFIRMED for $b=2$ | $B_r(M)<B_1(M)=5.97713<6$. Exact chain $B_1(33/53)=2535/424<6$. The result needs $b>1/\ln(5/3)=1.9576$. |
| 5 | Public acquisition removes the coexistence (analytical) | CONFIRMED | $V^{\rm public}=v_1=0.087918213417$. At $\kappa=0.05$ only $\psi=1$ survives. The claim needs a unique continuation; it holds at $r=3$. |
| 6 | Research can cut welfare while it raises entry (numerical diagnostic) | CONFIRMED | $\kappa=0.094$: entry $0.25\to0.5915$, $\Delta\mathcal W=-0.036442$ ($-0.030091$ if $k$ is a transfer). The sign changes with $\kappa$: at $\kappa=0.09$ it is $+0.017476$. |
| 7 | Purchase profit without entry response is $0.058334570734\ldots$ (no status label) | CONFIRMED | $0.0583345707338648$ by direct sum and by closed form. The brief's $0.060$ is not reproduced by any variant I tried. |

Side items:

| Item | Verdict |
|---|---|
| Order of events and what the market sees | Correct. |
| Mixed $\psi$: posteriors and indifference | Correct. |
| Equilibrium concept, off-path rule, tie rules | Correct as stated. Two conventions need a remark (Section 5). |
| Status labels | All deserved. |
| Memo numbers against script output | All match. |

## 3. Derivations and evidence

### 3.1 Common objects (my derivation)

Take $\pi=1/2$. Let $a=e^{-1/b}$, $d=1-a$, $m=a/(1+a)$, $M=1/(1+a)$, $w_L=t_L-t_0$.

**Rents.** At flow $x$ the market has entry rate $e(x)$ and posterior $\mu(x)$. Then

$$E[V_T\mid H,x]=t_0+e(w_L+\Delta_T),\quad E[V_T\mid L,x]=t_0+e\,w_L,\quad P(x)=t_0+e\,(w_L+\Delta_T\mu).$$

So a high-class purchase earns $e\Delta_T(1-\mu)$ at flow $x$. A low-class purchase earns $-e\Delta_T\mu\le0$ before the cost $k$. The low class never buys. One number $s=\psi\beta$ describes the flow law.

**Posteriors.** Let $n(z)=\frac{1-a}{1+a}a^{|z|}$. I checked this law against the difference of two geometric counts, to 25 digits. The flow laws are $f_H(x)=(1-s)n(x)+sn(x-1)$ and $f_L(x)=n(x)$. The ratio $n(x-1)/n(x)$ equals $a$ for $x\le0$ and $1/a$ for $x\ge1$. So the likelihood ratio takes two values, and with $y=\pi ds$:

$$\mu_-=\frac{\pi(1-ds)}{1-y},\qquad \mu_+=\frac{\pi(a+ds)}{a+y}.$$

Flow-level Bayes at $s\in\{0,\,0.1,\,0.4109,\,0.5,\,0.8631,\,1\}$ gives one posterior at $s=0$ and exactly two for $s>0$. Both agree with these formulas. On a 1001-point grid, $m\le\mu_-\le\tfrac12\le\mu_+\le M$. The ends are tight: all three equal $1/2$ at $s=0$, and $\mu_-=m$, $\mu_+=M$ at $s=1$.

**Purchase return.** A purchase reaches $x=1+z$. The weights are $P(z\le-1)=a/(1+a)$ and $P(z\ge0)=1/(1+a)$. With $1-\mu_-=(1-\pi)/(1-y)$ and $1-\mu_+=(1-\pi)a/(a+y)$,

$$D_r(s)=C\Big[\frac{e_-}{1-y}+\frac{e_+}{a+y}\Big],\qquad C=\frac{\Delta_T(1-\pi)\,a}{1+a}.$$

The direct sum agrees with this form to $10^{-51}$ at six test points, on both sides of the entry jump.

**Entry threshold.** Let $\tau=(c_H-g_L)/(g_H-g_L)$. Then $\mu_+(s)\ge\tau$ iff $s\ge s_E=\dfrac{a(\tau-\pi)}{\pi d(1-\tau)}$. Bisection on the flow-level posterior gives the same $s_E$ to $7\times10^{-51}$.

**Best reply.** The value of acquisition against schedule $s$ is $V(s)=\pi[D(s)-k]_+$. The investor acquires iff $V(s)>\kappa$, and mixes iff $V(s)=\kappa$. Positive $\psi$ needs $D>k$ strictly; otherwise $V=0<\kappa$.

**Numbers at $r=3$, $c_H=5$:** $\tau=117/200$, $s_E=0.631455407304$, $v_0=19/600$, $v_E^-=0.029489021784$, $v_E^+=0.094069177396$, $v_1=0.087918213417$.

In each entry regime $V$ falls strictly in $s$. It jumps up by $0.064580$ at $s_E$. I checked both facts on a 2001-point grid.

**Equilibrium sets** (my solver: grid scan, then bisection on each smooth branch; every root is checked by the direct sum):

| $\kappa$ | Equilibria $\psi$ | Entry |
|---|---|---|
| 0.02 | 1 | 0.625 |
| 0.03 | 0.410890232219 and 1 | 0.25 and 0.625 |
| 0.05 | 0 and 1 | 0.25 and 0.625 |
| 0.09 | 0 and 0.863132221274 | 0.25 and 0.612429447516 |
| 0.094 | 0 and 0.635073337122 | 0.25 and 0.591483493695 |
| 0.095 | 0 | 0.25 |

At the three interior roots the indifference residual $\pi(D-k)-\kappa$ is at most $7\times10^{-52}$. The smaller root of the memo's boxed quadratic equals each root. The larger root is $1.589$, $3.536$, $3.671$, which exceeds one.

I also tested each cutoff of the memo's regime table with offsets of $\pm10^{-9}$. The table is right. The endpoint at $v_E^+$ is closed (a root at $s_E$), and so are the corners at $v_0$ and $v_1$. The rows "exactly" at $v_E^-$ and $v_1$ print an extra root. It sits at $s_E$ (for $v_E^-$) or at $1$ (for $v_1$), to within $10^{-30}$. This is an artifact of the offset I use for the left limit. It is not a new root.

### 3.2 Claim 1: equal noise

Flows are $X\in\{-1,0,1,2\}$. Class $H$ buys with probability $s$. Then

$$f_H=\big(\tfrac{1-s}3,\tfrac13,\tfrac13,\tfrac s3\big),\quad f_L=\big(\tfrac13,\tfrac13,\tfrac13,0\big),\quad \mu=\Big(\tfrac{\pi(1-s)}{1-\pi s},\ \pi,\ \pi,\ 1\Big).$$

I confirmed the posteriors, entry, and ownership in exact fractions at $s\in\{0,\tfrac1{10},\tfrac12,1\}$.

Assume $B_r(\pi)<c_H$. Then $e=\rho$ at flows $-1,0,1$, because $\mu\le\pi$ there. A purchase reaches flows $0,1,2$ with probability $1/3$ each. The rents are $\rho\Delta_T(1-\pi)$, $\rho\Delta_T(1-\pi)$, and $0$. Flow $2$ reveals $H$. Hence

$$D=\tfrac23\rho(1-\pi)\Delta_T\ \text{ for every } s,\qquad \bar V_3=\pi\big[\tfrac23\rho(1-\pi)\Delta_T-k\big]_+ .$$

Because $V$ does not depend on $s$:

- $\psi=1$ iff $\kappa<\bar V_3$;
- $\psi=0$ iff $\kappa>\bar V_3$;
- every $\psi\in[0,1]$ works iff $\kappa=\bar V_3>0$.

So coexistence exists only at one knife-edge cost. There is no strategic complementarity.

Exact values: $D=1/720$ at $r=1.2$ (below $k$, so $\bar V_3=0$); $D=1/18$ and $\bar V_3=4/225$ at $r=3$; $\bar V_3=629/21600$ at $r=3.6$. For $\kappa=1/100$: $d_\kappa=12/25$ and $r_\kappa=2.57105453575887$; bisection on $\bar V_3(r)=\kappa$ gives the same value.

Entry. Only flow $2$ can recruit the cost-$c_H$ type, and $\Pr(X=2)=\pi\psi/3$. So $\mathsf E=\rho+(1-\rho)\pi\psi/3$ and $\mathsf O_H=\pi\rho+(1-\rho)\pi\psi/3$. At $\psi=1$ and $c_H=6$ I get $\mathsf E=3/8$ and $\mathsf O_H=1/4$ at all three strengths. The extra entry occurs where the rent is zero, so it cannot raise the research return. Entry returns to $\rho$ only if $g_H(r)<c_H$, that is $r>4+\sqrt{63}/2=7.968627$.

**Off-path belief.** Flow $2$ is off path only at $\psi=0$. Let $\mu_2$ be the belief there. A deviation to a purchase then earns $D(0;\mu_2)=\tfrac13[2\rho(1-\pi)\Delta_T+e(\mu_2)\Delta_T(1-\mu_2)]\ge\tfrac23\rho(1-\pi)\Delta_T$. So $\psi=0$ holds iff $\kappa\ge V(0;\mu_2)\ge\bar V_3$. The memo's choice $\mu_2=1$ is the most permissive belief. It gives $V(0)=\bar V_3$. Hence the set of $\psi$ that some perfect Bayesian equilibrium supports is exactly the memo's set. The same belief also follows from equilibrium dominance, because only the high class can gain from flow $2$.

The completion is needed for existence. At $r=3$, the passive belief $\mu_2=1/2$ gives $V(0)=19/600>\bar V_3=4/225$. Under that belief no equilibrium exists for $\kappa\in(4/225,\,19/600)$. The belief $\mu_2=0$ widens the gap to $(4/225,\,41/900)$.

### 3.3 Claim 2: coexistence at $\kappa=0.05$

At $r=3$: $v_0=\pi[\rho(1-\pi)\Delta_T-k]=\tfrac12[\tfrac1{12}-\tfrac1{50}]=19/600$. At $s=1$: $\mu_-=m$ and $\mu_+=M$, $1-y=a+y=(1+a)/2$, so $D(1)=\Delta_T(1+\rho)\,a/(1+a)^2$ when $M\ge\tau$. Then $v_1=\tfrac5{12}\,a/(1+a)^2-\tfrac1{100}$.

- No research: the deviator faces flat prices and gains $v_0-\kappa=-0.018333<0$.
- Full research: a switch to no acquisition forgoes $v_1-\kappa=+0.037918>0$.
- The posterior $M=0.62246$ exceeds $\tau=0.585$ strictly. So no tie rule is used.
- At both corners the low class does not buy (its purchase nets $-e\Delta_T\mu-k<0$). The challenger follows the entry rule, and the price equals the conditional mean. So both profiles are equilibria.

Exact chain. $e^{1/2}<33/20<5/3$ gives $a>3/5$. $e^{1/2}>3/2$ gives $a<2/3$. So $M>3/5>117/200=\tau$. The map $a\mapsto a/(1+a)^2$ rises on $(0,1)$ (derivative $(1-a)/(1+a)^3$). Hence $v_1>\tfrac5{12}\cdot\tfrac{15}{64}-\tfrac1{100}=\tfrac{561}{6400}>\tfrac1{20}$. Also $19/600<1/20$. The proof is complete and uses only rational bounds. The label "analytical" is deserved.

Robustness. I moved $k$ to $0.015$ and $0.025$, $r$ to $2.8$ and $3.3$, and $c_H$ to $4.9$ and $5.2$. In every case $v_0<0.05<v_1$.

Mechanism. Without the entry response, full research is worth only $0.029167<v_0$. The entry response lifts the value of full research to $0.087918$.

### 3.4 Claim 3: $\kappa=0.02$ at $r=1.2,\ 3,\ 4.2$

**Uniform bound.** Every rent is at least $\rho m\Delta_T$, because $e\ge\rho$ and $1-\mu\ge1-M=m$ at every $s$. So $V(s)\ge\pi(\rho m\Delta_T-k)$. If this exceeds $\kappa$, a purchase is strict ($D>k$) and acquisition strictly beats no acquisition against every schedule. Then $\psi=1$ is the only equilibrium.

- **$r=1.2$.** $\Delta_T=1/60<k=1/50$. A rent never exceeds $\Delta_T$. So $V\equiv0<\kappa$, and $\psi=0$ is the only equilibrium. Also $B_{1.2}(1/2)=1153/240<5$, so entry is $\rho=1/4$ and $\mathsf O_H=1/8$.
- **$r=3$.** With $m>3/8$: $\tfrac12[\tfrac14\cdot\tfrac38\cdot\tfrac23-\tfrac1{50}]=\tfrac{17}{800}>\tfrac1{50}$. So $\psi=1$ is unique. Its upper-flow probability is $\tfrac12\cdot\tfrac1{1+a}+\tfrac12\cdot\tfrac a{1+a}=\tfrac12$ exactly (direct sum: $0.5$). Since $B_3(M)>B_3(3/5)=41/8>5$, entry is $\rho+(1-\rho)/2=5/8$. High-class ownership is $\tfrac\rho2+\tfrac{1-\rho}{2(1+a)}=0.358422249201$.
- **$r=4.2$.** The bound is $0.0475$ with the exact $m$, and at least $0.0471$ with $m>3/8$. Both exceed $0.02$, so $\psi=1$ is unique. Since $B_{4.2}(M)<B_{4.2}(5/8)=104/21<5$, entry is $\rho=1/4$ and $\mathsf O_H=1/8$.

The ceiling solves $B_r(M)=5$ at $r_C=3.986096571638$. At the paper's $r_2=3.6$ research is also unique ($\psi=1$) but entry is $5/8$. So the sequence $0.25\to0.625\to0.25$ needs a third strength above $r_C$. The memo chooses $4.2$.

My grid scan of $\pi(D-k)$ over $s\in[0,1]$ gives minima $0.029492$ ($r=3$), $0.045243$ ($r=3.6$), $0.061620$ ($r=4.2$). All exceed $\kappa=0.02$.

### 3.5 Claim 4: $c_H=6$

With $\pi=1/2$ and buy-only orders, the likelihood ratio of any strategy profile lies in $[a,1/a]$. So every posterior is at most $M$. I checked this on a grid of all profiles $(s_H,s_L)\in\{0,0.1,\dots,1\}^2$. The largest posterior is $M$. Two profiles reach it: only the high class buys (flows $x\ge1$), or only the low class buys (flows $x\le0$). So the bound does not use equilibrium.

Both $g_H$ and $g_L$ fall in $r$ (their derivatives are negative because $p<\ell<r$). So $B_r(\mu)\le B_1(\mu)=\tfrac38+9\mu$ for $r>1$. Then

$$B_1(M)=5.9771339808<6\quad(\text{gap }0.02287).$$

A grid over $r\in(1,10)$ gives a maximum of $B_r(M)$ equal to $5.97339$.

Exact chain: $e^{1/2}\le1+\tfrac12+\tfrac{1/8}{1-1/6}=\tfrac{33}{20}<\tfrac53$. So $a\ge\tfrac{20}{33}>\tfrac35$ and $M\le\tfrac{33}{53}<\tfrac58$. Then $B_1(5/8)=\tfrac38+\tfrac{45}8=6$ exactly, and $B_1(33/53)=2535/424=5.9788<6$.

The margin is thin. $B_1(M)<6$ iff $M<5/8$ iff $b>1/\ln(5/3)=1.957615$. At $b=1.9$ the value is $6.0326$, and expensive entry becomes possible as $r\to\ell$. The memo fixes $b=2$, so the proposition is correct. The summary should state the $b$ condition.

### 3.6 Claim 5: public acquisition

After an observed acquisition, the market knows informed trade is available. The high class buys with probability $\beta$, so the schedule is the one for $s=\beta$ (not $\psi\beta$). At $r=3$ the minimum over $\beta\in[0,1]$ of $D(\beta)-k$ is $0.058980>0$. Every continuation therefore has $\beta=1$ strictly, and the continuation is unique. Then the value of acquisition is fixed:

$$V^{\rm public}=\pi[D(1)-k]=0.087918213417\ \text{(direct flow sum)}=v_1 .$$

The investor acquires with probability one if $\kappa<v_1$, zero if $\kappa>v_1$, and any probability at equality. At $\kappa=0.05$ a deviation from $\psi=0$ pays $v_1-\kappa=0.037918>0$. So $\psi=0$ fails and only $\psi=1$ survives. Hidden acquisition allows both. At $\kappa=0.09$ hidden acquisition allows $\{0,0.8631\}$, and public acquisition allows $\{0\}$ only.

Equal noise has the same return under both regimes, because $D$ does not depend on $s$.

### 3.7 Claim 6: welfare

**Welfare from primitives.** Let $W_0=E[R\mathbf 1\{R\ge p\}]=(r^2-p^2)/(2r)$, $W_h=E\max(R,h)=h$, and $W_\ell=E\max(R,\ell)=(r^2+\ell^2)/(2r)$. Then $W_\theta-W_0=g_\theta+p^2/r$ for $\theta=h,\ell$. I checked both identities in exact fractions at $r=1.2,\,3,\,3.6,\,4.2$.

Welfare is allocation value, less preparation cost, less $\psi\kappa$, less $\xi\pi\psi k$ (with $\xi=1$ if $k$ is a resource cost). I summed it over all flows, class by class, with no use of the memo's identity. The result equals the memo's closed form to 14 digits in all five cases:

| Case | $\psi$ | Entry | $\Delta\mathcal W$, $k$ a resource | $\Delta\mathcal W$, $k$ a transfer |
|---|---|---|---|---|
| $r=3$, $\kappa=0.02$ | 1 | $0.25\to0.625$ | $+0.118310$ | $+0.128310$ |
| $r=3$, $\kappa=0.09$ | 0.863132 | $0.25\to0.612429$ | $+0.017476$ | $+0.026108$ |
| $r=3$, $\kappa=0.094$ | 0.635073 | $0.25\to0.591483$ | $-0.036442$ | $-0.030091$ |
| $r=3$, $\kappa=0.03$ | 0.410890 | $0.25\to0.25$ | $-0.016436$ | $-0.012327$ |
| $r=4.2$, $\kappa=0.02$ | 1 | $0.25\to0.25$ | $-0.030000$ | $-0.020000$ |

The case $\kappa=0.094$ supports the claim: entry rises by $0.341$ and welfare falls. The marginal entrants near $s_E$ add only about $p^2/r$ each, while research costs $\psi\kappa$.

Two comparisons apply. First, the comparison is between two equilibria at the same parameters ($\psi=0$ and $\psi>0$). Second, the sign depends on $\kappa$: at $\kappa=0.09$ research raises welfare. The memo does not claim a general sign. The label "numerical diagnostic" is right, and it is even conservative.

### 3.8 Claim 7: the no-response profit

With entry held at $\rho$ after good news and $s=1$, $D=2\rho\Delta_T\,a/(1+a)^2$. At $r=3$ this is $0.078334570734$. After $k$: $0.0583345707338648$. The direct sum gives the same value. With the entry response: $\Delta_T(1+\rho)a/(1+a)^2-k=0.175836426834662$. Times $\pi$: $0.029167$ and $0.087918$.

The brief's $0.060$ does not reproduce. Other nearby quantities are $\rho(1-\pi)\Delta_T-k=19/300=0.063333$ (flat prices) and $\rho m\Delta_T-k=0.042923$. I also tried a noise law cut to $|z|\le K$ and renormalised. For $K=2,\,3,\,4,\,5,\,6,\,8,\,12$ it gives $0.0486,\ 0.0532,\ 0.0554,\ 0.0567,\ 0.0573,\ 0.0580,\ 0.0583$. None reaches $0.060$. I could not find the source of the brief's figure.

### 3.9 Side items

**Order of events.** The order is: nature draws the class; the investor pays $\kappa$ or not, before it sees the class; an acquirer sees the class and chooses $q\in\{0,1\}$; the market sees only $X=q+Z$ and sets the competitive price; the challenger sees the price and its cost. A low-class acquirer pays $\kappa$ and sends pure noise. So $f_H$ is a mixture with weight $\psi$ on a purchase, and $\psi$ acts as a presence probability. This is what the memo says.

**Mixed $\psi$.** Posteriors at $\psi<1$ have two values (Section 3.1). The indifference condition holds to $10^{-52}$ at all three interior roots. High-class purchase is strict there: $D-k=0.06,\ 0.18,\ 0.188$. A low-class purchase nets $-0.107,\ -0.298,\ -0.290$. A positive $\psi$ with $\beta<1$ is impossible, because it needs $D\le k$ and then $V=0<\kappa$.

**Uninformed purchase (side result).** The memo bars trade without acquisition. For $\pi=1/2$ and $s\in[0,1]$ the gross payoff of an uninformed purchase is $\Delta_Ty(1-\pi)\big[\tfrac{a\,e_-}{(1+a)(1-y)}-\tfrac{e_+}{(1+a)(a+y)}\big]\le0$. This holds because $1-y\ge a+y$ and $e_+\ge\rho$. The analytic form equals the direct sum to 15 digits at $s=0.3,\,0.7,\,1$. This check used $c_H=5$. Equal noise with $c_H=6$ gives $-1/9$ at $r=3$. So the bar does not bind in these cases. I did not check $\pi\ne1/2$.

**Equilibrium concept and conventions.**

| Convention | Where the memo uses it | Effect of a change |
|---|---|---|
| Investor chooses zero at a trade tie | $\beta=1$ whenever $\psi>0$ | None. At $D=k$, $V=0<\kappa$, so acquisition fails anyway. |
| Challenger prepares at a tie | Endpoint $s_E$; ceiling $r_C$; regime table | Matters. See below. |
| Investor may mix at an acquisition tie | Interior $\psi$ and the corners | Needed for existence. |
| $\Pr(H\mid X=2)=1$ at $\psi=0$ (equal noise) | Claim 1 | See Section 3.2. |

If the indifferent challenger could mix at $\tau$, a third equilibrium appears at $\psi=s_E$ for every $\kappa\in[v_E^-,v_E^+]$. The needed entry rate $e_+$ is $0.2501,\ 0.2559,\ 0.4882,\ 0.9527,\ 0.9992$ at $\kappa=0.0295,\ 0.03,\ 0.05,\ 0.09,\ 0.094$. Each lies in $[\rho,1]$. At $\kappa=0.02$ it is $0.140<\rho$, so no such equilibrium exists. Claims 2, 3, and 5 hold under either rule. The statement "at most two acquisition equilibria" and the regime table hold only under the tie rule that the memo states.

**Off-path rule in the discrete-Laplace model.** Every integer flow has positive probability under every profile, so Bayes' rule fixes every posterior. No off-path belief is needed.

**Status labels.**

- C6.1 to C6.6 are proofs. The proofs of C6.3 to C6.5 end in rational bounds. "Analytical" is deserved.
- C6.7: the identity is analytical. The example values are numerical. I reproduce them from primitives.
- Claim 6 is a numerical diagnostic. That label is right.
- Claim 7 is a closed form with a 15-digit evaluation. The memo gives it no label; "analytical closed form" would fit.

**Memo numbers against script output.** A helper script (`compare_memo_numbers.py`) lists every decimal with eight or more digits in the memo. There are 29, and one of them is the tail bound $6.9664\times10^{-88}$. Each one appears in the author's output, to the digits the memo prints. Twenty-five also appear in mine. The other four are two values that I print to fewer digits ($B_{1.2}(1/2)=1153/240$ exactly, and $B_{4.2}(M)=4.93261212945$) and the two sweep values at $\kappa=0.06$, which I did not recompute. The author's script reproduces the saved output exactly. The file hashes in the run record match the files.

## 4. Errors found and corrections

I found no error in a claim, a proof step, or a number. I found four points where the text needs a qualifier:

1. **Claim 4 depends on $b$.** The proof is correct at $b=2$. The result fails for $b<1.9576$. The margin at $b=2$ is only $0.0229$. The Answer and the Plain summary do not state this.
2. **Claim 3 needs its strengths.** The sequence $0.25\to0.625\to0.25$ holds at $r=1.2,\,3,\,4.2$. It does not hold at the paper's $3.6$, where entry stays $5/8$. The memo prints $r_C=3.986$ and chooses $4.2$, but it could say explicitly why $3.6$ fails.
3. **Tie-rule dependence is not flagged.** C6.3 says "at most two acquisition equilibria". This holds only if the indifferent challenger prepares. If the challenger mixes at $\tau$, a third equilibrium exists for $\kappa\in[v_E^-,v_E^+]$.
4. **The welfare sign is not general.** The text can read as if research always lowers welfare. At $\kappa=0.09$ it raises welfare.

## 5. What the original memo should change

1. In the Answer and the Plain summary, state that the $c_H=6$ result needs $b>1/\ln(5/3)\approx1.9576$. Give the margin $0.0229$ at $b=2$.
2. In C6.5 and Section 5, add one sentence: at $r=3.6$ research is unique but entry is still $5/8$, because the ceiling is $r_C=3.986$.
3. In C6.3, add: "If the challenger mixes at $\tau$, there is a third equilibrium at $\psi=s_E$ for $\kappa\in[v_E^-,v_E^+]$. The claims at $\kappa=0.02$, $0.05$ and the public game do not change."
4. In C6.2, add the existence remark: the completion $\Pr(H\mid X=2)=1$ is the most permissive belief. A passive belief leaves no equilibrium for $\kappa\in(4/225,19/600)$ at $r=3$.
5. In C6.7, add the $\kappa=0.09$ row ($+0.017476$), to show that the sign depends on $\kappa$.
6. In Section 6, replace the line that says no independent derivation exists by a pointer to this check. Add the uninformed-purchase result for $\pi=1/2$ as a remark.
7. Give claim 7 a label.
8. Optional: the brief's $0.060$ remains unexplained. The memo can say "source not found" rather than imply a cause.

## 6. Plain summary

I rebuilt the memo's results from scratch with exact fractions and 50-digit arithmetic. I did not use the author's code. All seven claims hold.

Equal noise gives an exact research cutoff. The return to research does not depend on how many others research, so coexistence exists only at one cost.

Discrete-Laplace noise gives coexistence over a range of costs. At strength 3, with preparation cost 5 and research cost 0.05, both no research and full research are equilibria. At research cost 0.02, research is unique at strengths 1.2, 3 and 4.2, and entry goes 0.25, 0.625, 0.25.

The paper's preparation cost of 6 blocks expensive entry, but only for noise scale above 1.9576. The margin at the paper's value of 2 is small.

Public acquisition removes the coexistence. Research can lower welfare while it raises entry, but the sign depends on the research cost. The profit without entry response is 0.058335.

I found no error. Four statements need a qualifier. Two conventions matter: the belief at the off-path flow, and the tie rule for the challenger.
