# X: Independent check of T2, variants V3 buy and V3 two

## 1. Scope

This memo checks seven claims of `memos/T2_liquidity_trader.md` for the variants V3 buy and V3 two.
It does not check V1, V2, the literal order of §3.9, the literature claims, or the PIN calibration.

**Model as checked.**

- One public order slot. With probability $\lambda$ the informed investor fills it and sees the class $j\in\{H,L\}$.
- Otherwise a liquidity trader of the same unit size fills it:
  - buy-only menu $\{0,1\}$: it buys with probability $\beta$;
  - two-sided menu $\{-1,0,1\}$: it sells, abstains, buys with probabilities $(\beta,1-2\beta,\beta)$.
- No separate noise. The flow $x$ equals the slot order.
- Competitive price $P(x)=t_0+e(x)[t_L-t_0+\Delta_T\mu(x)]$. The challenger sees the price.
- The paper's auction; benchmark $h=10,\ \ell=1,\ p=1/2,\ \rho=1/4,\ c_L=0,\ c_H=6,\ k=1/50,\ \pi=1/2$.
- The informed payoff conditions on filling the slot (T2 §2.4, equation (2)).

**Equilibrium concept.** Perfect Bayesian equilibrium of the finite order game.
Bayes' rule applies at every flow of the menu.
Investor tie rules: IM (any mixture at indifference) and I0 (zero at indifference).
Challenger tie rules: C1 (prepare at indifference) and CM (any mixture at indifference).
I checked all four pairs where they matter.

**Method.**

1. I derived each claim by hand, from the primitives.
2. I wrote a new exact-rational program: `scripts/X_check/v3_check.py`. Its output is `scripts/X_check/results.txt`.
3. The program computes the auction objects by direct integration over $R\sim U[0,r]$, not from the closed forms.
   It then compares them with equation (4) of the paper. The differences are zero at all six test strengths.
4. The program builds the flow law, posteriors, prices, entry and payoffs from first principles.
   It verifies every candidate equilibrium by a direct best-response test.
5. Only after step 4, I ran T2's program. Its new output, `scripts/X_check/t2_rerun_output.txt`,
   is byte-identical to T2's saved `exact_results.txt`. I then compared the numbers.

## 2. Verdict table

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | Every flow on path for $0<\beta<1$ (buy), $0<\beta<1/2$ (two), $0<\lambda<1$; every posterior interior; no off-path belief | **CONFIRMED** (on the unit menu) | Each flow has liquidity mass $(1-\lambda)\eta(x)>0$ in both classes. Posterior bounds $[C_x/(2C_x+\lambda),(C_x+\lambda)/(2C_x+\lambda)]$. See §4, item 2, for continuous order sizes. |
| 2 | Strip $82\beta/(59+82\beta)<\lambda<2686\beta/(1559+2686\beta)$; $82/259<\lambda<2686/7363$ at $\beta=1/3$ | **CONFIRMED** | Both ends come from the $c_H$ window: $\tau(3)=141/200<M<\tau(3.6)=4245/5804$. The trading-cost windows are slack. |
| 3 | $M=29/40$; entry $1/4\to37/68\to1/4$; ownership $23/68$; $r_C=(50+\sqrt{2529})/29$; unique orders | **CONFIRMED** | Exact values reproduced. One equilibrium at each strength under all four tie-rule pairs. |
| 4 | Coexistence on about $[1.3939579,1.7478775]$, contains 1.55–1.65; entry flat on the full branch; threshold entry falls | **CONFIRMED WITH CORRECTION** | Interval, flat entry $37/68$, falling threshold entry all reproduced. Full orders exist only from $r_F\approx1.4609847$. Below $r_F$ the informative equilibrium is a partial purchase. |
| 5 | Prop. A.9 at 3: proceeds $+113/408$, net surplus $+5/68$ | **CONFIRMED** | Both regimes solved from primitives; equal flow law and trading cost; both menus. |
| 6 | An uninformed filler with only the trading payoff prefers zero | **CONFIRMED** | Best nonzero uninformed payoff is at most $-k$ in every equilibrium found. |
| 7 | Equal posteriors do not imply equal payoff thresholds (geometric base) | **CONFIRMED** | Same binary experiment. Returns: $11/240$ vs $319/4800$ hidden; $11/60$ vs $319/1920$ with access. The order flips. |

## 3. Derivations and evidence

### 3.1 Auction objects

Direct integration gives, at $r=3$: $t_0=5/12$, $t_H=37/24$, $t_L=7/8$, $g_H=203/24$, $g_L=1/8$, $\Delta_T=2/3$.
At $r=18/5$: $\Delta_T=169/180$ and $\tau=4245/5804$. At $r=6/5$: $\Delta_T=1/60$.
The identity $t+g=\theta$ holds exactly for both classes.
I write $\tau(r)=(c_H-g_L)/(g_H-g_L)$, so $B_r(\mu)\ge c_H$ exactly when $\mu\ge\tau(r)$.

### 3.2 Claim 1: support and interior beliefs

Let $\eta(x)$ be the liquidity law and $\sigma_j$ any informed mixed strategy. Then

$$a_j(x)=(1-\lambda)\eta(x)+\lambda\sigma_j(x)\ \ge\ C_x:=(1-\lambda)\eta(x).$$

- Buy-only: $\eta=(1-\beta,\beta)$ on $\{0,1\}$. Both are positive exactly when $0<\beta<1$.
- Two-sided: $\eta=(\beta,1-2\beta,\beta)$ on $\{-1,0,1\}$. All are positive exactly when $0<\beta<1/2$.

So every menu flow has positive mass in each class, under every strategy, when $0<\lambda<1$.
The posterior $\mu(x)=a_H/(a_H+a_L)$ rises in $a_H$ and falls in $a_L$.
Each mass lies in $[C_x,C_x+\lambda]$. Hence

$$\frac{C_x}{2C_x+\lambda}\le\mu(x)\le\frac{C_x+\lambda}{2C_x+\lambda},$$

which is strictly inside $(0,1)$. The program enumerates all pure profiles, the extreme points.
At the example, flow 1 has range $[11/40,29/40]$ and buy-only flow 0 has $[11/31,20/31]$.
At the excluded edges the program shows the lost support: two-sided $\beta=1/2$ gives zero liquidity mass at flow 0.

This is **analytical** and holds for the unit menus that T2 states.

### 3.3 Claim 2: the strip and each inequality

At full informed orders, put $b=(1-\lambda)\beta$ and $u=\lambda/b$. The top posterior is

$$M=\frac{b+\lambda}{2b+\lambda}=\frac{1+u}{2+u}.$$

The conditions of Proposition 2, adapted to V3, are:

| Condition | Exact form | Status on the strip |
|---|---|---|
| (a) $c_H$ window at $r_1=3$: $B_3(M)>c_H$ | $M>141/200\iff u>82/59$ | **binding** (lower end) |
| (b) $c_H$ window at $r_2=3.6$: $B_{3.6}(M)<c_H$ | $M<4245/5804\iff u<2686/1559$ | **binding** (upper end) |
| (c) trading cost at $r_0=1.2$: $\Delta_T(1.2)<k$ | $1/60<1/50$ | slack; free of $\lambda,\beta$ |
| (d) trading cost at 3: $\rho\Delta_T(3)(1-M)>k$ | $M<22/25$ | slack |
| (d') same at 3.6 | $M<773/845$ | slack |
| (e) no recruitment at the prior | $B_{1.2}(1/2)-6=-287/240$, $B_3(1/2)-6=-41/24$ | slack |
| (f) ownership | $h>r_2$, so $W_H=1$; ownership rises iff $e_H>\rho$ | holds |

The paper's factor $(1-1/b)$ in (A2) has no analog here.
In V3 the correctly signed residual is at least $\rho\Delta_T(1-M)$ under every candidate.

Solve (a) and (b) for $\lambda$:

$$\frac{82\beta}{59+82\beta}<\lambda<\frac{2686\beta}{1559+2686\beta}.$$

The program checks this at $\beta\in\{1/10,1/3,2/5,9/10\}$. At each end, $M$ equals $\tau(3)$ or $\tau(3.6)$ exactly.
At $\beta=1/3$ the strip is $82/259<\lambda<2686/7363$, about $(0.316602,0.364797)$.

The threshold $\tau(r)$ rises in $r$. Its derivative has numerator $4(48r^2-6r+12)$, which has no real root.
Under C1, the lower end may be weak. Under CM it must be strict. This matches T2 §3.4.

### 3.4 Claim 3: the example $\beta=1/3$, $\lambda=6/17$

Here $b=11/51$ and $M=29/40$.

| Strength | Informed orders | Posteriors | Entry $\mathsf E$ | High-class ownership |
|---|---|---|---|---|
| $6/5$ | $(0,0)$ | all $1/2$ | $1/4$ | $1/8$ |
| $3$ | buy: $(1,0)$; two: $(1,-1)$ | $\mu(1)=29/40$; $\mu(-1)=11/40$ | $37/68$ | $23/68$ |
| $18/5$ | buy: $(1,0)$; two: $(1,-1)$ | same | $1/4$ | $1/8$ |

Derivation of entry at 3: $\Pr(x=1)=b+\lambda/2=20/51$. So $\mathsf E=1/4+(3/4)(20/51)=37/68$.
Class-H entry is $1/4+(3/4)(29/51)=23/34$, so ownership is $23/68$.

**Uniqueness, with mixtures.** The bounds hold under every candidate schedule, including CM ties:

- at $6/5$: every unit residual is at most $\Delta_T=1/60<k$. Every nonzero order nets at most $-1/300$.
- at 3: every correctly signed order nets at least $\rho\Delta_T(1-M)-k=31/1200>0$.
- at $18/5$: the same bound is $1283/28800>0$.
- wrong-signed orders net $-e\Delta_T(1-\mu)-k<0$ or $-e\Delta_T\mu-k<0$.

The program finds exactly one equilibrium at each strength, in both menus, under C1/IM, CM/IM, C1/I0 and CM/I0.
The bounds are the proof. The count is a cross-check.

**Ceiling.** The program evaluates $8r[B_r(M)-6]$ by integration at $r=2,3,4$ and fits a quadratic.
The fit is $-(29r^2-100r-1)/10$. A fourth point, $r=7/2$, agrees exactly.
The positive root is $r_C=(50+\sqrt{2529})/29\in[3.45824702905933,3.45824702905934]$.
Also $dB_r(M)/dr=-M/2-(3-4M)/(8r^2)<0$, since $3-4M=1/10>0$. So the root is unique.
Full orders stay unique on $[3,3.6]$ because $\Delta_T$ rises in $r$.
Thus entry is $37/68$ on $[3,r_C]$ and $1/4$ on $(r_C,3.6]$.

### 3.5 Claim 4: coexistence

**The class-H problem.** Let $s=\lambda\Pr(q=1\mid H)$. A purchase lands at flow 1 with certainty. Its gross return is

$$K_H(s)=e_+\,\Delta_T\,\frac{b}{2b+s},\qquad \mu_+(s)=\frac{b+s}{2b+s}.$$

Flow 1 recruits when $s\ge s^*=b(2\tau-1)/(1-\tau)$. On each entry piece $K_H$ falls strictly in $s$.
So the equilibrium candidates are: $s=0$; $s=\lambda$; one interior root per piece; and $s=s^*$ with a challenger mixture.

**No trade.** All posteriors equal $1/2$ and entry is $\rho$. A deviation earns $\rho\Delta_T/2$.
No trade is an equilibrium exactly when $\Delta_T\le 2k/\rho=4/25$, that is $r\le r_N=(29+6\sqrt6)/25\approx1.7478775$.

**Two-sided low class.** Its sale return is $\rho\Delta_T b/(2b+t)\le\rho\Delta_T/2\le k$ for $r\le r_N$.
So it abstains in every coexistence outcome. Zero-flow entry does not enter either return.

**Informative outcomes for $r\le r_N$.** Put $J(r)=\Delta_T(r)[1-\tau(r)]$. Then

$$J(r)=\frac{(r-1)^2(32r-4r^2-1)}{8r(20r-r^2-1)}.$$

- Recruited partial purchase, $s=b(\Delta_T/k-2)$: exists when $J>k$ and $\Delta_T(1-M)<k$.
- Full purchase: exists when $\Delta_T(1-M)\ge k$ (IM), that is $r\ge r_F$, with $\Delta_T(r_F)=4/55$.
- Threshold mixture at $s^*$, CM only: challenger entry $e^*=k/J$, valid when $\rho\le e^*\le1$.
- These need $s^*<\lambda$, that is $\tau(r)<M$. This holds: $\tau(r_N)\approx0.654<0.725$.

So an informative equilibrium coexists with no trade exactly when $J(r)\ge k$ and $r\le r_N$.
The numerator of $J-k$ is $-1+\tfrac{854}{25}r-\tfrac{361}{5}r^2+\tfrac{1004}{25}r^3-4r^4$.
A Sturm count finds exactly one root in $(1,r_N]$ and in $(1,18/5]$. Also $J(1)=0<k$.
So the set is the interval $[r_A,r_N]$ with:

| Threshold | Definition | Rational bracket |
|---|---|---|
| $r_A$ | $J(r_A)=k$ | $1.393957920279\ldots$ (signs checked) |
| $r_F$ | $\Delta_T=4/55$ | $1.460984663710\ldots$ |
| $r_N$ | $\Delta_T=4/25$ | $1.747877538268\ldots$ |

My derivative of $J$ in $y=r-1$ is exactly 8 times T2's polynomial $y(972+2268y+1440y^2+3y^3-136y^4+4y^5)$.

**Branch structure (V3 buy, C1/IM).**

| $r$ | Informative equilibrium | Entry |
|---|---|---|
| 1.40 | recruited partial purchase | 0.481092 |
| 1.45 | recruited partial purchase | 0.532391 |
| 1.50 to 1.70 | full purchase | $37/68\approx0.544118$ |

Under I0 the partial purchase is excluded, so coexistence is $(r_F,r_N]$, as T2 states.

**The three strengths.** At 1.55, 1.60 and 1.65 the full branch has entry $37/68$ in both menus.
Under CM, the threshold mixture adds:

| $r$ | $\mathsf E^*$ | Challenger entry at flow 1 |
|---|---|---|
| $31/20$ | $2442588329/6961987560\approx0.3508464$ | 0.580287 |
| $8/5$ | $2186473/6653340\approx0.3286279$ | 0.506106 |
| $33/20$ | $1793732190563/5770000237560\approx0.3108721$ | 0.447179 |

The program tests all eight selections from $\{\mathsf E^*(r),37/68\}$. No selection rises strictly across the three strengths.
So the upward order of Proposition 3 fails, as T2 states.

### 3.6 Claim 5: access to prices at $r=3$

With the price hidden, the challenger keeps the prior. Since $B_3(1/2)<6$, entry is $\rho$ at every flow.
The return bound $\rho\Delta_T(1-M)-k=31/1200>0$ still forces full orders. So the flow law is the same.

The program sums over class and flow, with the low-cost type always prepared:

- proceeds: $t_0+e(x)(t_j-t_0)$;
- net surplus: $S_0+e(x)(S_j-S_0)-(1-\rho)\,\zeta(x)\,c_H$.

Here $S_j$ is the expected value of $\max(\theta_j,R)$, $S_0$ is the expected value of $R\mathbf 1\{R\ge p\}$, and $\zeta(x)$ is high-cost preparation.

| Regime | Proceeds | Net surplus | Informed trading cost (buy / two) |
|---|---|---|---|
| access | $485/544$ | $4285/1632$ | $3/850$ / $3/425$ |
| hidden | $59/96$ | $245/96$ | $3/850$ / $3/425$ |
| difference | $113/408\approx0.27696$ | $5/68\approx0.07353$ | $0$ |

The hidden proceeds $59/96=0.614583$ equal the paper's price-hidden value, as they must.
By hand: $\Delta\mathcal R_T=(3/4)(20/51)(t_L-t_0+\Delta_T M)=(3/4)(20/51)(113/120)=113/408$.
Also $\Delta\mathcal W=(3/4)(20/51)[B_3(29/40)-6+p^2/r]=(5/17)(1/6+1/12)=5/68$.

### 3.7 Claim 6: an uninformed filler

Given that the uninformed trader fills the slot, the class is independent of its order. Its expected value at flow $x$ is

$$t_0+e(x)[t_L-t_0+\Delta_T\pi].$$

A buy nets $e(x)\Delta_T[\pi-\mu(x)]-k$. A sale nets $e(x)\Delta_T[\mu(x)-\pi]-k$.
In every equilibrium found, $\mu(1)\ge1/2\ge\mu(-1)$. So each nonzero order nets at most $-k$.
The program prints the best nonzero payoff in every equilibrium at $r\in\{1.2,1.4,1.55,1.6,1.65,3,3.6\}$:

- it equals $-1/50$ where the reached posterior is exactly $1/2$;
- it is lower elsewhere, for example $-17/100$ for a purchase at $r=3$.

So a free uninformed trader chooses zero. Then $\beta=0$, and flow 1 again reveals class H.
The liquidity motive is essential. **Analytical.**

### 3.8 Claim 7: comparison with the buy-only geometric base

The base noise is $f(z)=\frac{1-a}{1+a}a^{|z|}$. The investor is always present. Class H buys one unit; class L abstains.
Take $a=11/29$, so $\gamma=1/(1+a)=29/40$.

- The program gives posterior $11/40$ at flows $-3,\ldots,0$ and $29/40$ at flows $1,\ldots,4$.
- $\Pr(X\ge1\mid H)=29/40$ and $\Pr(X\ge1\mid L)=11/40$ (closed form and a truncated sum agree).
- V3 buy with $\beta=1/2$ and $\lambda=9/20$ gives $\Pr(x=1\mid H)=29/40$, $\Pr(x=1\mid L)=11/40$.

The two binary experiments are identical. The informed returns at $r=3$ are not:

| Price regime | Base: $\gamma(1-\gamma)\Delta_T(e_++e_-)$ | Slot: $e_+\Delta_T(1-M)$ |
|---|---|---|
| hidden ($e_\pm=1/4$) | $319/4800\approx0.0665$ | $11/240\approx0.0458$ |
| access ($e_+=1$, $e_-=1/4$) | $319/1920\approx0.1661$ | $11/60\approx0.1833$ |

The reason: a base purchase reaches the bad-news region with probability $1-\gamma$, where the residual is large.
A slot purchase always reaches flow 1. The trade threshold therefore depends on the flow law given the investor's own order.
The ranking flips between the two regimes. **Analytical.**

### 3.9 Why the strip is narrow

The strip in $M$ is exactly $(\tau(r_1),\tau(r_2))=(0.705000,0.731392)$, of width $7659/290200\approx0.0264$.

- $\tau$ moves slowly with strength. At $r=3$, $\tau'(3)=213/5000\approx0.043$.
- The reason: $\partial B/\partial r=-131/360\approx-0.36$ at $M=29/40$, but $\partial B/\partial\mu=g_H-g_L=25/3$.
- So a move from $r_1=3$ to $r_2=3.6$ shifts the recruiting posterior by only about 0.026.

The paper's Laplace top posterior is $e/(1+e)\approx0.731059$. Its ceiling is $r_C\approx3.592658519$, as in the paper.
This value lies $0.000334$ below $\tau(3.6)$ and $0.026$ above $\tau(3)$.

So the suggested reason is partly right:

- $r_2=3.6$ lies just above the Laplace ceiling. This puts the top of the band just above the paper's own $M$.
- The width comes from the gap $r_2-r_1$ and the flat $\tau$. The Laplace ceiling does not set the width.
- Any noise law must put its top posterior in the same band to match the benchmark. The paper's Laplace calibration sits at its top edge.

In $\lambda$, the band maps to $82/59<u<2686/1559$. At $\beta=1/3$ this is $0.3166<\lambda<0.3648$.

### 3.10 Status labels and memo numbers

**Labels.**

- Proposition 2 parts, ceiling, A.9, §3.7, §3.8, off-path beliefs: "analytical" is deserved. The proofs use uniform bounds or closed forms.
- Prop. 3 row of the V3 scorecards: labelled "analytical". §3.6 labels the three-strength result "computer-assisted".
  The decimal endpoints are rational brackets, and the triple order uses exact fractions. "Computer-assisted" fits better.
  The containment of 1.55–1.65 alone can be shown by hand.
- Item 9 "open" and item 10 "computer-assisted" are correct.

**Numbers.** Every V3 fraction in T2's memo that I tested appears in T2's output, and my program reproduces it.
The test list: $29/40$, $37/68$, $23/68$, $113/408$, $5/68$, $82/259$, $2686/7363$, $141/200$, $4245/5804$,
$11/60$, $11/240$, $319/1920$, $319/4800$, $21563/870600$, $223499/35984800$, and the three threshold entries.
Two memo values are not printed by T2's program: $113/18480$ and $371/7980$.
My program gives $J(6/5)=113/18480$ and $J(5/3)=53/1140$, which equals $371/7980$.

## 4. Errors and corrections

No numerical error was found in T2's V3 results. The points below are a wording correction and three scope or label notes.

1. **Coexistence wording (correction to the ledger and the task summary, not to T2).**
   "No trade and full informative orders coexist on about $[1.394,1.748]$" is not exact.
   - Full orders exist only on $[r_F,r_N]\approx[1.4609847,1.7478775]$.
   - On $[r_A,r_F)$ the informative equilibrium is a recruited partial purchase (IM).
   - Under I0, coexistence is $(r_F,r_N]$.
   T2 §3.6 states this correctly. The three strengths 1.55–1.65 lie on the full branch.

2. **Scope of "no off-path belief" (omission).** The claim needs the unit menu.
   The paper's Proposition 2 lets the investor deviate to any order in $[-1,1]$.
   In V3 a fractional order reaches a flow that the liquidity trader never uses. That flow needs an off-path belief.
   The program prices a class-H deviation to $q=99/100$:
   - at $r=3.6$, with the prior belief there: $0.0964$, against $0.0446$ for the unit purchase. The full-order outcome fails.
   - with belief "informed, class H" (EGJ's convention): $-0.0198$. The outcome survives.
   - at $r=3$, the prior belief gives $0.0627<0.1633$. The outcome survives.
   So, with continuous order sizes, Proposition 2(iii) in V3 rests on EGJ's off-path convention.
   T2 states the menu restriction (§2.3, §3.4) but not this consequence.

3. **Label (minor).** The V3 scorecard item 4 says "analytical"; §3.6 says "computer-assisted". Use "computer-assisted".

4. **Fraction (trivial).** $371/7980$ in §3.6 is not in lowest terms; it equals $53/1140$.

## 5. Plain summary

I checked the one-slot liquidity model of T2 with my own derivation and a new exact-rational program.
All seven claims hold.

- Every flow of the unit menu has liquidity mass in both classes. Every posterior is interior.
- Proposition 2 holds on $82\beta/(59+82\beta)<\lambda<2686\beta/(1559+2686\beta)$.
  Only the $c_H$ window at 3 and 3.6 binds. The trading-cost conditions are slack.
- At $\beta=1/3$, $\lambda=6/17$: $M=29/40$, entry $1/4,\ 37/68,\ 1/4$, ownership $23/68$, $r_C\approx3.458247$.
  Orders are unique under all tie rules.
- Coexistence holds on about $[1.394,1.748]$. Full orders start only at about 1.461.
  Entry is flat on the full branch. The threshold mixture gives falling entry.
- Price access raises proceeds by $113/408$ and net surplus by $5/68$.
- A free uninformed trader would not trade. The liquidity motive is essential.
- Equal posteriors give unequal returns against the geometric base.

The strip is narrow because the recruiting posterior $\tau(r)$ rises only about 0.026 from $r=3$ to $3.6$.
The Laplace ceiling explains why the paper's own $M$ sits at the top of that band.

With continuous order sizes, as the paper allows, V3 needs an off-path belief at $r=3.6$.
