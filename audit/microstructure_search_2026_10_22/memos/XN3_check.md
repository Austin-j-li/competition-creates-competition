# XN3: Independent check of N3, Extension B (costly research with a success ceiling)

Status: complete, 23 October 2026.
Memo checked: `memos/N3_size_research.md`.
Scripts and outputs: `scripts/XN3_check/`.

## 1. Scope

This memo checks Extension B of N3 (§2.2) in full.
It also checks the Extension C claims (§2.3) and two Extension A claims (§2.1) that the task names.
It does not check the full Extension A correspondence, its price-access numbers, or literature claims other than Dow–Gorton (L1 record C09).

**Model as checked (N3 §2.2).**

- Benchmark: $(h,\ell,p,\rho,c_L,c_H,k,\pi)=(10,1,1/2,1/4,0,6,1/50,1/2)$; incumbent value $R\sim U[0,r]$; the paper's second-price auction with reserve $p$.
- Unit menu $\{-1,0,1\}$. The liquidity trader sells, waits, and buys with probability $1/3$ each ($\beta=1/3$).
- Research success $\lambda\in[0,\bar\lambda]$ with $\bar\lambda=6/17$. Research cost $C(\lambda)=a\lambda^2/2$ with $a=1/40$.

**Equilibrium concept.** Perfect Bayesian equilibrium.
Market makers know the equilibrium research choice and strategies.
A deviation in research or in trade faces the fixed price and entry schedule.

**Belief rule.** Every order has liquidity mass $(1-\lambda)/3>0$ when $\lambda<1$.
Bayes' rule therefore defines every belief. No result uses an off-path belief.

**Tie rules.**

- Investor: IM (any mixture at indifference) and I0 (zero at indifference).
- Challenger: C1 (prepare at indifference, the paper's rule) and CM (any mixture at indifference).
- I checked all four pairs where they matter.

**Method.**

1. I derived each claim by hand from the primitives (§3).
2. I wrote three new programs. They import nothing from other members.
   - `xn3_research.py`: exact rational enumeration of every equilibrium of the research game at given $(r,\bar\lambda,a)$ and tie rule. Auction objects come from direct integration. Output: `xn3_research.out.txt`.
   - `xn3_float_scan.py`: a floating-point scan over $(\lambda,\alpha,\sigma)$ with every deviation, wrong-signed orders included. It does not use the classification of §3.2. Output: `xn3_float_scan.out.txt`. Status: numerical diagnostic.
   - `xn3_size.py`: exact check of the named Extension A claims. Output: `xn3_size.out.txt`.
3. After my numbers were complete, I ran N3's program `derive_extensions.py` in one slot.
   The new output `n3_rerun_output.txt` is byte-identical to N3's `derived_results.txt` (SHA-256 `b0811482b579…`).
   I then compared the numbers.

All programs print results only. The longest run (the float scan) took about eight minutes in one slot.

## 2. Verdict table

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | The model (timing, who sees the research outcome, payoff) is coherent | **CONFIRMED WITH CORRECTION** | Coherent hidden-action equilibrium (§3.1). Two wording corrections: the ceiling does cap the informed share of slot orders; research also removes liquidity mass (§4, items 1–2). |
| 2 | At 1.2, zero research is the unique outcome; entry $1/4$ | **CONFIRMED** | $\Delta(6/5)=1/60<k$, so every order loses against every schedule (§3.3). One equilibrium under C1 and CM. |
| 3a | At 1.55, 1.60, 1.65: research 0.2502, 0.2933, 0.3326; entry 0.5313, 0.5367, 0.5416, strictly rising | **CONFIRMED** | Exact roots of N3 eq. (11); disjoint brackets; $\mathsf E_R=1/2+\lambda_R/8$ (§3.4). |
| 3b | Strict purchase after good news; no investor mixing between trade and zero | **CONFIRMED** | $U_H(+1)=0.012512,\,0.014666,\,0.016631>0$. Best low-class sale $-0.007802,\,-0.005938,\,-0.003996<0$. Holds under IM and I0. |
| 3c | Zero research is also an equilibrium (coexistence) | **CONFIRMED** | $\rho\Delta/2<k$ at all three strengths. |
| 3d | The list of equilibria is complete | **CONFIRMED** | Under C1: exactly two equilibria at each strength. Under CM: a third, threshold equilibrium with falling entry 0.488338, 0.447830, 0.415581, as N3 states. The float scan finds no other (§3.4). |
| 4 | At 3 and 3.6: research at the ceiling is unique; entry $37/68=0.5441$ and $1/4$; prices informative | **CONFIRMED** | Uniform bounds of N3 eq. (18). One equilibrium at each strength under C1 and CM. The outcome equals T2 V3 calibration A exactly (§3.5). |
| 5 | Price access raises proceeds and net surplus at 3 | **CONFIRMED** | Proceeds $+113/408$; net surplus $+5/68$. Research and trade costs are equal in both regimes (§3.6). |
| 6a | Without the ceiling, floor entry at 3.6 is impossible at $a=1/40$ | **CONFIRMED** | Complete list: one equilibrium, $\lambda\approx0.8174$, entry $0.6022$ at 3.6 (and $0.5950$ at 3) (§3.7). |
| 6b | Without the ceiling, $a=1/4$ gives coexistence at 3 and 3.6 | **CONFIRMED** | All four rows and both threshold candidates reproduced. The list is complete (§3.7). |
| 7a | Extension A: a rising branch at 1.55–1.65 | **CONFIRMED** | Exact: $\mathsf E=1/4+3\Delta/4$. It needs high-class mixing with zero, as N3 states (§3.8). |
| 7b | Extension A: a second equilibrium keeps extra entry at 3.6 | **CONFIRMED** | Entry $0.331583835426>1/4$. Every unused order is worse (§3.8). |
| 7c | Extension A: a second equilibrium at 3 with entry $0.333877967986$ | **CONFIRMED WITH CORRECTION** | The value is right. The memo omits that the low class must mix sale sizes as in eq. (7). With a pure size-two sale the profile fails (§3.8, §4 item 3). |
| 8 | Status label "analytical" for Extension B | **CONFIRMED WITH CORRECTION** | The proofs are analytical. The root table and several comparisons rest on exact machine evaluation. "Analytical, with computer-assisted root enclosures" fits better (§4 item 6). |

An additional result, not claimed by N3, is in §3.7(c) and §5.1.
Without a ceiling below $2686/7363$, no research cost gives both unique recruitment at 3 and floor entry at 3.6.

## 3. Derivations

### 3.1 The model and its coherence (claim 1)

**Timing.**

1. Nature draws the class $j\in\{H,L\}$ (prior $1/2$), $R\sim U[0,r]$, and the challenger's cost ($0$ with probability $\rho$, else $c_H$). The draws are independent.
2. The investor chooses $\lambda\in[0,\bar\lambda]$ in private and pays $a\lambda^2/2$. It does not know $j$.
3. Research succeeds with probability $\lambda$, independent of $j$. Only the investor sees the outcome. Success reveals $j$ exactly.
4. After success, the investor fills the slot with $q\in\{-1,0,1\}$ at cost $k|q|$.
   After failure, a liquidity trader fills the slot. The failed investor has no order.
5. Market makers see $q$ only. They set $P_q=\mathbb E[V_T\mid q]$ with the equilibrium $\lambda^*$.
6. The challenger sees $P_q$ and its cost, then decides whether to prepare. The auction follows.

**Payoff.** Let $e_q$ be total entry after order $q$ and $\mu_q$ the posterior. Then

$$
\mathbb E[V_T\mid j,q]=t_0+e_q(t_j-t_0),\qquad P_q=t_0+e_q(t_L-t_0+\Delta\mu_q).
$$

The trade payoffs are therefore

$$
U_H(q)=q\,e_q\Delta(1-\mu_q)-k|q|,\qquad U_L(q)=-q\,e_q\Delta\mu_q-k|q|.
$$

The research value is $V_r=\tfrac12[\max_qU_H(q)+\max_qU_L(q)]$.
A private choice $z$ earns $\Pi(z)=zV_r-az^2/2$ against the fixed schedule.

**Coherence.**

- $\Pi$ is strictly concave, so $\lambda=\min\{\bar\lambda,V_r/a\}$ is the unique best response (N3 eq. (10)). No research tie can occur.
- A deviation $z\neq\lambda^*$ changes the true order law but not the prices. N3 correctly uses $V_r$ at the fixed schedule.
- Every order has liquidity mass $(1-\lambda)/3>0$ for $\lambda<1$. No off-path belief enters.
- Research and liquidity arrival are perfectly negatively correlated. Each order has liquidity mass $(1-\lambda)/3$, so more research removes camouflage.
  This is Dow–Gorton's stated simplification (L1 record C09, verified).
  It also causes N3's congestion term $\partial V_r/\partial\lambda=-3\Delta/[2(2+\lambda)^2]<0$, which I reproduce.
- The failed investor has no order by assumption. If it had one, it would abstain in every equilibrium below.
  The reason is X_check §3.7: an uninformed purchase nets $e\Delta(1/2-\mu_+)-k<0$ when $\mu_+\ge1/2\ge\mu_-$.
- $\lambda$ is the probability that the slot order is informed. The ceiling therefore caps the informed share of slot orders (§4 item 1).

### 3.2 Classification of all equilibria

**Notation.** $\alpha=\Pr(+1\mid H,\text{success})$, $\sigma=\Pr(-1\mid L,\text{success})$, $b=(1-\lambda)/3$.

$$
\mu_+=\frac{b+\lambda\alpha}{2b+\lambda\alpha},\qquad
\mu_-=\frac{b}{2b+\lambda\sigma},\qquad
\mu_0=\frac{b+\lambda(1-\alpha)}{2b+\lambda(2-\alpha-\sigma)}.
$$

Write $d(\lambda)=(1-\lambda)/(2+\lambda)$. It is $1-\mu_+$ when $\alpha=1$, and $\mu_-$ when $\sigma=1$.
Write $\lambda_E(r)=(2\tau-1)/(2-\tau)$, the solution of $1-d(\lambda)=\tau(r)$.

**Fact F0 (wrong-signed orders lose).** For $\lambda<1$, $0<\mu_q<1$ and $e_q\ge\rho>0$.
So $U_H(-1)=-e_-\Delta(1-\mu_-)-k<0$ and $U_L(+1)=-e_+\Delta\mu_+-k<0$.

**Fact F1 (the classes decouple).** $U_H(+1)$ depends on $\alpha$ only. $U_L(-1)$ depends on $\sigma$ only.
The zero order earns zero, so $\mu_0$ affects aggregate entry only.

**Fact F2 (sales never recruit).** $\mu_-\le1/2<\tau(r)$ on $1<r<10$, because $B_r(1/2)<c_H$ (T2 §2.1). So $e_-=\rho$.

**Fact F3 (a mixing class earns zero).** Thus $V_r=\tfrac12[U_H(+1)^++U_L(-1)^+]$ at the equilibrium strategies.

**Lemma.** In every equilibrium with $\lambda>0$, the high class buys for sure with strict profit.

*Proof.* $\lambda>0$ needs $V_r>0$, so some class trades with strict profit.
If the low class sells strictly, then $\rho\Delta d(\lambda)>k$.
A purchase then earns at least $\rho\Delta(1-\mu_+)-k\ge\rho\Delta d(\lambda)-k>0$ for every $\alpha$, since $\mu_+\le1-d(\lambda)$.
So $\alpha=1$ strictly in both cases. $\square$

**The candidate types for $\lambda>0$.** The high class buys ($\alpha=1$). Then:

- Low class: L0 ($\sigma=0$) iff $\rho\Delta/2\le k$. Otherwise L1 ($\sigma=1$) iff $\rho\Delta d(\lambda)\ge k$, else Lint ($0<\sigma<1$ with $\rho\Delta\mu_-=k$).
- Entry after a purchase: "hi" ($e_+=1$) iff $\lambda\ge\lambda_E$ under C1; "lo" ($e_+=\rho$) iff $\lambda<\lambda_E$; "th" (CM only) at $\lambda=\lambda_E$ with $e^*\in(\rho,1)$.
- Research value: $V_r=(E\Delta d(\lambda)-K)/2$, with $(E,K)=(e_+,k)$ for L0 and Lint, and $(e_++\rho,2k)$ for L1.

**The research equation.** For $\lambda<\bar\lambda$, $a\lambda=V_r$. Multiply by $2(2+\lambda)$:

$$
F(\lambda)=2a\lambda^2+(4a+K+E\Delta)\lambda+2K-E\Delta=0.
$$

$F$ rises strictly on $\lambda\ge0$, and $F(0)<0$ iff $E\Delta>2K$.
So each type has at most one interior root.
The ceiling is an equilibrium of a type iff $F(\bar\lambda)\le0$ and $\bar\lambda$ lies in that type's region.
The root lies above a rational point $x$ iff $F(x)<0$. Thus every comparison is an exact sign evaluation.
With L0 and hi, $F$ is N3's eq. (11). My program uses $F/3$, so its signs equal N3's printed values divided by 3.

**Zero research** is an equilibrium iff $\rho\Delta/2\le k$, i.e. $r\le r_N\approx1.747878$.
All posteriors equal $1/2<\tau$, so $V_r=(\rho\Delta/2-k)^+$.

**Threshold (CM).** At $\lambda=\lambda_E<\bar\lambda$, the research condition gives
$e^*=(2a\lambda_E+k-g)/[\Delta(1-\tau)]$, with $g=\rho\Delta(1-\tau)-k$ for L1 and $g=0$ otherwise.
It is an equilibrium iff $\rho<e^*<1$.

`xn3_research.py` enumerates exactly these types. `xn3_float_scan.py` checks the result without F1–F3.

### 3.3 Strength 1.2 (claim 2)

$\Delta(6/5)=1/60<k=1/50$. Every unit order earns at most $\Delta-k=-1/300$ against every schedule.
So $V_r=0$, and $\lambda=0$ is the unique effort. All posteriors equal $1/2<\tau(6/5)=195/308$. Entry is $1/4$.
The program finds one equilibrium under C1 and CM.

### 3.4 Strengths 1.55, 1.60, 1.65 (claim 3)

| $r$ | $\Delta$ | $\tau$ | $\lambda_E$ | $\rho\Delta/2-k$ |
|---|---|---|---|---|
| $31/20$ | $121/1240$ | $1020/1577$ | $463/2134=0.216963$ | $-0.007802$ |
| $8/5$ | $9/80$ | $205/316$ | $94/427=0.220141$ | $-0.005938$ |
| $33/20$ | $169/1320$ | $7620/11711$ | $3529/15802=0.223326$ | $-0.003996$ |

**Reduction.** Since $\rho\Delta/2<k$, the low class never sells (L0), and zero research is an equilibrium.
The "lo" type needs $\rho\Delta d(\lambda)\ge k$. This fails because $d<1/2$. So only "hi" and "th" remain.

**The hi root.** Exact bisection of $F$ to width $10^{-18}$ gives:

| $r$ | $\lambda_R$ | $\mu_+$ | $U_H(+1)=2a\lambda_R$ | $\mathsf E_R=1/2+\lambda_R/8$ |
|---|---:|---:|---:|---:|
| 1.55 | 0.250249322294 | 0.666814396841 | 0.012512466115 | 0.531281165287 |
| 1.60 | 0.293324846156 | 0.691855623930 | 0.014666242308 | 0.536665605770 |
| 1.65 | 0.332615237748 | 0.713889907152 | 0.016630761887 | 0.541576904719 |

- Each root exceeds $\lambda_E$, so each purchase recruits.
- Each root is below $6/17$: capacity is slack iff $a>0.009682,\ 0.015495,\ 0.021545$, and $a=0.025$.
- Entry: only $+1$ recruits; $\Pr(+1)=(1-\lambda)/3+\lambda/2=(2+\lambda)/6$; so $\mathsf E=\rho+(1-\rho)(2+\lambda)/6=1/2+\lambda/8$.
- The three entry brackets are disjoint and ordered. Entry rises strictly. N3's eq. (13) gives the same order.

**Strictness.** The high class earns $2a\lambda_R>0$ from a purchase. The low class's best sale earns $\rho\Delta/2-k<0$.
Wrong-signed orders lose (F0). So both trade choices are strict under IM and I0.

**Completeness.**

- Under C1: exactly two equilibria at each strength, zero research and $\lambda_R$.
- Under CM: one more, at $\lambda=\lambda_E$, with $e^*=0.895040,\ 0.784642,\ 0.696846$.
  Its aggregate entry $\rho+(e^*-\rho)(2+\lambda_E)/6$ is $0.488338,\ 0.447830,\ 0.415581$. It falls with strength.
- The float scan (C1) finds only $\lambda=0$ and one cluster at $\lambda\approx0.25026,\ 0.29335,\ 0.33265$ (grid step $10^{-4}$).

This matches N3's list of §2.2 exactly.

### 3.5 Strengths 3 and 3.6 (claim 4)

**Uniform bound.** For $\lambda\le6/17$, each order has liquidity mass at least $11/51$ and informed mass at most $\lambda$.
So every posterior lies in $[11/40,29/40]$ for every strategy.
A correctly signed order earns at least $\rho\Delta\cdot11/40-k$: $31/1200$ at 3 and $1283/28800$ at 3.6.

**Consequences.**

- Both classes trade for sure, with strict profit.
- $V_r$ exceeds $a\bar\lambda=3/340$, so research sits at the ceiling. The margins are $347/20400$ and $17491/489600$, as in N3 eq. (18).
- At $\bar\lambda$, $M=29/40$. Also $\tau(3)=141/200<29/40<\tau(3.6)=4245/5804$.
- Entry at 3: $1/4+(3/4)(20/51)=37/68$. Entry at 3.6: $1/4$.
- Prices at 3.6 after $+1,0,-1$: $20651/28800$, $1913/2880$, $17609/28800$. They differ, so the price is informative.

The program finds one equilibrium at each strength under C1 and CM.
Under CM the threshold candidate at 3 would need $e^*<\rho$, so it does not exist.

**Identity with T2.** $\lambda=6/17$ and $\beta=1/3$ is T2 V3 calibration A.
So the outcome at 3 and 3.6 is exactly T2's outcome. Research changes only the cost, $9/5780$.

### 3.6 Price access at 3 (claim 5)

With the price hidden, entry is $\rho$ after every order, since $B_3(1/2)-c_H=-41/24$.
The bound of §3.5 still forces both trades. The research value $31/1200$ exceeds $a\bar\lambda$, so research again sits at the ceiling.
The order law, the research cost, and the trade cost are the same in both regimes.

| Regime | Proceeds | Net surplus (after preparation costs) |
|---|---|---|
| access | $485/544$ | $4285/1632$ |
| hidden | $59/96$ | $245/96$ |
| difference | $113/408\approx0.276961$ | $5/68\approx0.073529$ |

By hand: $\Delta\mathcal R_T=(1-\rho)\Pr(+1)[t_L-t_0+\Delta M]=(3/4)(20/51)(113/120)=113/408$.
At 3.6 the research cost is $9/5780$; with trade costs, $249/28900$. Both agree with N3.

### 3.7 Extension C: no ceiling (claim 6)

**(a) $a=1/40$, $\lambda\in[0,1]$.** The enumerator gives one equilibrium at each strength, under C1 and CM:

| $r$ | $\lambda$ | Low-class sale probability | $\mu_+$ | Entry |
|---|---:|---:|---:|---:|
| 3 | 0.759907263798 | 0.667006 | 0.913007 | 0.594988 |
| 3.6 | 0.817352634024 | 0.725217 | 0.935171 | 0.602169 |

So N3's impossibility result holds.
In fact the unique outcome has higher entry at 3.6 than at 3.
The low class mixes between a sale and zero, so investor indifference returns.
N3's proof numbers also agree: $v_*=899467/20894400$, $C'(\lambda_E)=1343/147260$, margin $5219716561/153845467200$.
The float scan (finer grid, tolerance $10^{-5}$) finds near-equilibria only near these two points.

**(b) $a=1/4$.** I reproduce all four rows of N3's table:

- at 3: $\lambda=0.173506$ (entry $1/4$) and $\lambda=0.366319$ (entry $0.545790$);
- at 3.6: $\lambda=0.239072$ (entry $1/4$) and $\lambda=0.448587$ (entry $0.556073$);
- CM thresholds: $e^*=0.758311$ at 3 and $0.631858$ at 3.6.

The list is complete: two equilibria under C1, three under CM. N3 left completeness open. It now holds at these two points.

**(c) Proposition (analytical; rules C1 or CM; $\beta=1/3$).**
Let $\bar\lambda\ge\lambda_E(3.6)=2686/7363$.
If an equilibrium at 3.6 has entry $\rho$, then an equilibrium at 3 also has entry $\rho$.

*Proof.*

1. Entry $\rho$ at 3.6 needs every posterior at most $\tau(3.6)$. Then $e_+=\rho$ and $1-\mu_+\ge1-\tau$.
   A purchase earns at least $v_*(3.6)=\rho\Delta(1-\tau)-k=899467/20894400>0$. So the high class buys for sure ($\alpha=1$).
2. With $\alpha=1$, $\mu_+=1-d(\lambda)\le\tau(3.6)$. So $\lambda\le\lambda_E(3.6)\le\bar\lambda$.
   Also $\mu_-\ge d(\lambda)\ge1-\tau$, so a sale also earns at least $v_*(3.6)$, and the low class sells for sure.
3. The research condition gives $a\lambda\ge V_r\ge v_*(3.6)$. Hence $a\ge a_{3.6}:=v_*(3.6)/\lambda_E(3.6)\approx0.118006$.
4. At 3, let $G(\lambda)=\rho\Delta d(\lambda)-k-a\lambda$. It falls strictly. $G(0)=\rho\Delta/2-k>0$.
   Also $G(\lambda_E(3))=v_*(3)-a\lambda_E(3)<0$, because $a>a_3:=v_*(3)/\lambda_E(3)=1813/19680\approx0.092124$.
5. So $G$ has a root $\lambda_{lo}\in(0,\lambda_E(3))$. There $\mu_+<\tau(3)$, entry is $\rho$ after every order, and both trades earn $a\lambda_{lo}>0$.
   Research is interior because $\lambda_{lo}<\lambda_E(3)<\bar\lambda$. This is an equilibrium with entry $\rho$. $\square$

**Consequence.** Without a ceiling below $2686/7363$, no research cost gives both unique recruitment at 3 and floor entry at 3.6.
A recruiting equilibrium without a ceiling exists at 3 iff $a<63973/196800\approx0.3251$, and at 3.6 iff $a<0.377253$.
So for $a\in(0.0921,0.3251)$ the strength 3 has two pure equilibria, as at $a=1/4$.

### 3.8 Extension A, briefly (claim 7)

Menu $\{-2,\dots,2\}$, $\lambda=1/5$, $b_1=1/25$, $b_2=1/7$, rule C1. `xn3_size.py` prints every order payoff.

**Rising branch.** $A_1=b_1(\Delta/k-2)$ gives $\sigma_H(1)=357/620,\ 29/40,\ 581/660$.
Then $\mu_{+1}=481/605,\ 37/45,\ 713/845$, all above $\tau$.
Entry is $1603/4960,\ 107/320,\ 609/1760$. It equals $1/4+3\Delta/4$ because $b_1=2k$.
Every unused order has negative payoff. The high class is indifferent between $+1$ and $0$.
So the branch needs rule IM and fails under I0, as N3 states. No informed trade is also an equilibrium.

**Floor at 3.6.** Both classes use size two. The active payoff is $3001/30600$; the unused size one earns $701/7200$. The choice is strict.

**Second equilibrium at 3.6.** The high class mixes $+1$ (recruits) and $+2$ (does not); the low class sells two.

- The root of eq. (8) is $x\approx0.137556894468$, so $\sigma_H(1)\approx0.687784$.
- $\mu_{+1}\approx0.816140>\tau$ and $\mu_{+2}\approx0.589677<\tau$.
- Both purchase sizes earn $0.152624065$; the low-class size-two sale earns $0.098072>0.097361$.
- Entry is $0.331583835426>1/4$. This confirms N3.

**Second equilibrium at 3.** The same purchase mixture gives $x\approx0.143674581296$ and entry $0.333877967986$.

- With a pure size-two sale, the low class gains $0.005294$ by a size-one sale. That profile fails.
- With the low-class mixture of eq. (7) ($\sigma_L(-1)\approx0.022234$), every condition holds.
- N3's program uses this mixture (its output, line 218). The memo text does not state it.

**Main equilibrium at 3.** The high class strictly buys two ($449/1275$ against $19/300$). The low class uses the eq. (7) mixture. Entry is $121/280$.

## 4. Errors and corrections

No numerical error was found. Every N3 number that I tested agrees with my program to the printed digits.
The items below are wording, omission, scope, and label points.

1. **Wording (§2.2).** "It does not bound the fraction of orders that are informed" is incorrect.
   $\lambda$ is the probability that the slot order is informed, so $\bar\lambda$ caps that share at $6/17$.
   At 3 and 3.6 the cap binds, and the market there is T2's calibration A.
   Suggested text: "The bound is technological. Against strong incumbents it acts exactly as T2's fixed informed probability."
2. **Omission (§2.2).** Research also removes liquidity mass: each order has liquidity mass $(1-\lambda)/3$.
   This is Dow–Gorton's simplification. It drives the falling research value within the branch. The timing paragraph should state it.
3. **Omission (§2.1).** The second equilibrium at 3 needs the low-class size mixture of eq. (7). The memo should state the low-class strategy.
4. **Scope (§2.2, eq. (17)).** The lower endpoint $1241/57600$ is sufficient, not necessary, for strictly rising entry.
   - Strict rise holds for $119/7680<a<150913279/4526936200$, i.e. about $0.01549<a<0.03334$.
   - For $a$ between $119/7680$ and $1241/57600$, the ceiling binds at 1.65 only. Entry there is $37/68$, still above the 1.60 value.
   - The endpoint results need $a\le1813/19680$. N3's interval lies inside this bound.
5. **Open item closed (§2.3).** "No claim here exhausts other conditional trade patterns on [0,1]."
   At $a=1/40$ and $a=1/4$, at 3 and 3.6, the lists are now complete (§3.7).
6. **Label (§2.2).** "Analytical" fits the proofs. The root table and several comparisons rest on exact machine evaluation.
   "Analytical, with computer-assisted root enclosures" matches the team's labels. X_check made the same point for T2.

## 5. Robustness and the ceiling assumption

### 5.1 The endpoint results come from the ceiling alone

**Statement (analytical, rule C1).** Unique recruitment at 3 and floor entry at 3.6 hold together iff

$$
\frac{82}{259}\le\bar\lambda<\frac{2686}{7363}\quad\text{and}\quad a\le\frac{1813}{19680}\approx0.0921.
$$

*Proof.*

- If $\bar\lambda<\lambda_E(3)=82/259$, every posterior at 3 is below $\tau(3)$, so entry at 3 is $\rho$.
- If $\bar\lambda\ge\lambda_E(3.6)$, Proposition §3.7(c) applies.
- Inside the strip, every posterior at 3.6 is at most $1-d(\bar\lambda)<\tau(3.6)$. So entry at 3.6 is $\rho$ for every research choice, and the "lo" outcome is unique there.
- At 3, the recruiting candidate exists iff $F_{hi}(\lambda_E(3))\le0$, i.e. $a\le63973/196800$. The floor candidate exists iff $a>a_3$. Since $a_3<63973/196800$, recruitment is unique iff $a\le a_3$. $\square$

This is T2's strip at $\beta=1/3$: $82/259<\lambda<2686/7363$ (X_check claim 2). Its width is about $0.048$.
For other liquidity weights, the corresponding band is $82\beta/(59+82\beta)\le\bar\lambda<2686\beta/(1559+2686\beta)$ (X_check §3.3).
Inside it, recruitment at 3 is possible and floor entry at 3.6 holds for every effort.
The failure above the band also needs $a_3<a_{3.6}$. I checked that inequality only at $\beta=1/3$.
So the ceiling needs the same narrow calibration as T2's fixed $\lambda$. Research does not widen the strip.

### 5.2 The middle-strength results and the cost

- Coexistence at 1.55 needs $a<a_{up}=150913279/4526936200\approx0.03334$, independent of $\bar\lambda$.
- Strict rise needs $\lambda_R(1.60)<\bar\lambda$, i.e. $a>a_{lo}(\bar\lambda)=[\Delta(1.6)d(\bar\lambda)-k]/(2\bar\lambda)$.

| $\bar\lambda$ | $a_{lo}$ | $a_{up}/a_{lo}$ |
|---|---:|---:|
| $82/259=0.3166$ | 0.020827 | 1.60 |
| $1/3$ | 0.018214 | 1.83 |
| $6/17=0.3529$ | 0.015495 | 2.15 |
| $9/25$ | 0.014595 | 2.28 |
| $2686/7363=0.3648$ | 0.014006 | 2.38 |

- If $a\ge a_{up}$, the positive branch fails at 1.55 first, then at 1.60 and 1.65.
- If $a\le a_{lo}$, research hits the ceiling at 1.60 and 1.65. Entry is then flat at $1/2+\bar\lambda/8$, which is T2's failure again.
- The rise is small: about $0.010$ in entry from 1.55 to 1.65.

### 5.3 The grid (`xn3_research.out.txt`, Section G)

Status: computer-assisted at the grid points (exact enumeration); the price-access column is a numerical diagnostic.

I used 11 ceilings from $0.30$ to $1$ and 13 costs from $1/200$ to $1/2$, at all six strengths, under rule C1.

- Strength 1.2 always gives the unique zero-research outcome.
- All Extension B properties hold at 15 of the 143 points. All 15 lie in the region of §5.1–5.2.
- Price access raises proceeds and net surplus (after research and trade costs) at every point with unique recruitment at 3.
  This includes $a=1/12$, where research under hidden prices lies below the ceiling (floating-point diagnostic).
- Under CM at $\bar\lambda=6/17$, uniqueness at 3 and 3.6 holds for $a\le1/12$; three equilibria exist at 3 for $a\in\{1/10,1/8,1/4\}$.

### 5.4 Is the ceiling natural?

- **Dow–Gorton (L1 C09, verified).** Research is costly and succeeds with an exogenous probability below one. It is a single costly step, not a continuous effort.
  So a success probability below one is natural in their technology.
- **N3's technology differs in two ways.** Effort below the ceiling is continuous with a convex cost. The ceiling is a hard kink. Neither feature is in the verified record.
- **Dow–Gorton's own technology gives a weaker result** (analytical; derivation only, no computation). Take one research decision with fixed cost $c$ and success $\bar\lambda$.
  - Pure research gives $\lambda=\bar\lambda$ and entry $1/2+\bar\lambda/8$ at every middle strength. Entry is flat.
  - Mixed research solves $\bar\lambda V_r(\lambda)=c$, so $d(\lambda)=(2c/\bar\lambda+k)/\Delta$ and $\lambda$ rises with $r$.
  - The rising branch therefore returns, but with investor indifference over research.
  - The convex cost removes that indifference. It acts like many researchers with different costs. This is N3's addition and is unverified.
- **The value of the ceiling is not free.** It must lie in T2's strip. A ceiling at $1/2$, or no ceiling, loses the floor at 3.6 at every cost.

**Judgment.**

- The ceiling is a plausible technological assumption in the spirit of Dow–Gorton.
- It carries the whole endpoint result, with the same narrow tolerance as T2's $\lambda$.
- The new content of Extension B is the middle-strength branch: endogenous research restores strictly rising entry with strict trades.
- That part holds over a cost window of about a factor of two. It also holds for every ceiling in the strip.
- A smooth cost that rises steeply near a ceiling in the strip may give the same results. This is a conjecture; I did not check it.

## 6. Plain summary

I checked N3's research extension with my own derivation and three new programs. N3's program reproduces its saved output exactly. Every tested number agrees.

The model is coherent. The investor pays for a private chance to learn the class. Market makers know the equilibrium effort. A liquidity trader fills the slot when research fails.

Confirmed:

- At 1.2, zero research is unique.
- At 1.55, 1.60, 1.65, research is 0.2502, 0.2933, 0.3326 and entry 0.5313, 0.5367, 0.5416. Trades are strict. Zero research coexists. The list is complete.
- At 3 and 3.6, research at the ceiling is unique. Entry is 37/68, then 1/4.
- Price access raises proceeds by 113/408 and net surplus by 5/68.
- Without the ceiling, floor entry at 3.6 fails at the same cost.

Corrections: the ceiling does cap the informed share. The second size equilibrium at 3 needs a low-class size mixture.

Robustness: the endpoint results hold only for ceilings in T2's narrow strip, from 0.3166 to 0.3648. No higher ceiling works at any cost. The rising branch needs a cost window of about a factor of two. The ceiling resembles Dow–Gorton's technology, but it carries the whole endpoint result.
