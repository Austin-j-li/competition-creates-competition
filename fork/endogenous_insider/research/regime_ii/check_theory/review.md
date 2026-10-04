---
title: "Referee report on the theory track: regime II test of Proposition 2"
subtitle: "Theory referee, regime II team"
date: "2026-10-04"
---

This report checks every analytical claim of `theory/note.md` (results R.1 to R.12 and Proposition 2'), and then checks each claim against the numerics note, the adversary note, and new independent computations. Status words are the paper's: analytical, computer-assisted, numerical diagnostic, open. All numbers come from the CSV files in this folder (Section 9). The code in this folder imports nothing from the other tracks.

## 1. Verdict in short

1. **The core theory is right.** I checked the proofs of R.1, R.2, R.3, R.4, R.5, R.6, R.7, R.8, R.9, R.10(a), R.11, R.12 and Proposition 2' line by line. I tried tie rules, mixed orders, island pools, and the quantifier "in every equilibrium". I found no gap in a proof. Independent code reproduces Table 1, Table 2, Table 3, the (A4'') thresholds and the bathtub plateau share.
2. **Small errors, now fixed in the theory note** (each marked "[Referee fix: ...]"): Table 2 dashes; the right end of the nonempty example; the open-set claim; non-uniqueness of entry under (A3) alone; the unqualified sufficient candidate $c_L+c_H\le2B_{r_1}(\tfrac12)$; the missing $\rho$ condition after Proposition 2'.
3. **One upgrade.** The starved family's high-type check is analytical whenever the pool cutoff is at least $1$. So at the paper's $k=0.02$ and $\rho=0.25$, Proposition 2(ii) fails analytically for every $c_L>3.4211$, not only for $c_L>3.6498$ (Referee Proposition C.2).
4. **One refutation in the theory digest** (not in the note): "an informative equilibrium exists iff $\rho\Delta_T>2k$" is false. The note's version, "every equilibrium is informative iff $\rho\Delta_T>2k$", is right.
5. **Main cross-track conflict: the numerics k-scan is wrong.** The numerics track wrote that (A3) is sufficient for the reversal up to $c_L=2.9$. A starved equilibrium with $\mathsf E=0.1227<\rho$ exists at $c_L=2.9$, $k=0.0224$, inside (A3). The theory's Table 3 is right, and the numerics k-scan is not. The cause is a bisection on a predicate that is not monotone in $k$.

## 2. The question and the referee's answer

The team question: replace (A1) by (A1'), $B_{r_1}(m)\le c_L<B_{r_1}(\tfrac12)$, and decide what survives of Proposition 2. The theory track takes both ends strict. That is right: at $c_L=B_{r_1}(m)$ the tie rule makes the cheap type prepare at belief $m$, so that point is regime I and the paper's proof applies. At $c_L=B_{r_1}(\tfrac12)$ the pool cap is $1$ and $K=0$, so Proposition 2' needs the upper end strict.

| part of Proposition 2 | with (A1'), (A2) and the paper's (A3) | with (A1'), (A2), (A3'), (A4') |
|---|---|---|
| (i) weak incumbent | survives (R.1, analytical) | survives |
| (ii) informed trading, correct signs | survives (R.2, R.3a, analytical) | survives |
| (ii) informative price, Blackwell dominance | survives (R.3a, analytical) | survives |
| (ii) every equilibrium has a no-entry pool | yes (R.3b, analytical) | yes |
| (ii) unique on-path entry | fails when $k<(1-\frac1b)J_G(z_0)$, which covers all $\rho\le\frac12$ (analytical); open for large $\rho$ | fails (R.7, analytical) |
| (ii) unique trading outcome | fails at $k=0.02$ for $c_L>2.9844$ (numerical diagnostic) and for $c_L>3.4211$ (analytical); with $k$ free in the window, fails for $c_L>2.8319$ (numerical diagnostic) | survives (R.6, analytical) |
| (ii) $\mathsf E>\rho$, $\mathsf O_H>\rho/2$ in every equilibrium | same failures; also fails at every regime II $c_L$ once $\rho\ge0.5154$ whenever a full-order equilibrium exists | holds iff (A4'); (A4') needs $\rho<\rho_E^*=0.5154$ |
| (iii) collapse | original (iii) is vacuous; new form $\mathsf E<\rho$, $\mathsf O_H<\rho/2$ (R.12, analytical) | same; existence at $r_2$ now proved (Lemma C.1) |

**Replacement for (A3).** (A3') $\Delta_T(r_0)<k\le K(c_L)$ is a correct sufficient replacement. It is not necessary for uniqueness. Lemma C.1 below shows $K(c_L)<\frac12(1-\frac1b)\rho m\Delta_T(r_1)$, so (A3') is always less than half of (A3)'s right side. At the paper's triple $(r_0,k,\rho)=(1.2,0.02,0.25)$ it is empty.

**Weakest replacement for (A1).** Keep (A2), and let the trading cost force full orders: the paper's (A3) when $c_L\le B_{r_1}(m)$, and (A3') when $c_L$ is in regime II. Then the reversal holds in every equilibrium if and only if $c_L\le B_{r_1}(m)$ (the paper's floor, with the tie) or [(A1') and (A4')]. For $c_L\ge B_{r_1}(\frac12)$ it always fails, because the dead profile is an equilibrium (CD.3(ii)). (A4') is a joint condition on $(c_L,\rho)$, not on $c_L$ alone. At $\rho=0.25$ it reads $c_L\le3.4607$ (entry) and $c_L\le3.7408$ (ownership). For $\rho\ge0.5154$ the entry half is empty. With the paper's (A3) at $k=0.02$ and $\rho=0.25$, no theorem gives a replacement. The best known statement is "fails above $2.9844$; no failure found below it".

## 3. Line-by-line review of the theory note

### R.1 (weak incumbent). Holds.

The residual bound $A_\theta\le\Delta_T(r_0)$ holds against every schedule, so zero is the unique best response. Under zero orders $\mu_X\equiv\frac12$ and $\varphi(\frac12)=\rho$, because $c_L<B_{r_1}(\frac12)<B_{r_0}(\frac12)<c_H$. A pool would need belief $\frac12$ and no entry, which fails. The tie rule plays no role. I also confirmed the strict inequality $c_L<B_{r_0}(\frac12)$ from (5).

### R.2 (signs and monotone posteriors). Holds.

A wrong-signed order earns at most $-k|q|<0$, also when the residual is zero almost everywhere. The total-positivity step is correct: the Laplace density is log-concave, so $f(x-q)$ is TP2 in $(x,q)$, and every pair of support points has $q\ge0\ge q'$. Atoms at zero for both types are allowed.

### R.3 (informed trading and pools). Holds, with one fix to a consequence.

(a) is Proposition CD.4 with $g_{1/2}=\rho$. The note states it correctly: "every equilibrium is informative iff $\rho\Delta_T>2k$". The digest states "an informative equilibrium exists iff $\rho\Delta_T>2k$". That is false. Counterexample (`candidate_counter.csv`, last row): $\rho=0.1$, $c_L=3$, $k=0.04>\rho\Delta_T/2=0.0333$. Full orders with the minimal pool form an equilibrium (both regrets $0$ on a 401-point grid with refinement), next to the no-trade equilibrium. The reason is that expensive entry raises the residual far above $\rho\Delta_T/2$ on good flows.

(b) is correct: a pool-free equilibrium has entry at least $\rho$ almost everywhere, so (A.6) forces full orders, and full orders put belief $m<\tau_L$ on the plateau. Two remarks.

- The note's consequence "on-path entry is never unique" needs two equilibria with different entry. Proposition R.7 gives them only under $k\le K$. Under (A3) alone, Proposition CD.7(d) gives full-order half-line equilibria with cutoffs just above $z_0$ whenever $k<(1-\frac1b)J_G(z_0)$. Since $J_G(z_0)\ge\Delta_Tm/2$, this covers every $\rho\le\frac12$. At the benchmark $b$, $c_H$, $r_1$ it covers every $\tau_L$ when $\rho<0.699$. For $\rho=0.9$ and $\tau_L=0.49$, $J_G(z_0)/\Delta_T=0.2036<\rho m=0.2420$ (`jgap.csv`), and the claim is open there. Fixed in the note.
- The note says the right side of (A3) is "exactly what makes the pool unavoidable". It is a sufficient condition. Pool-free (low-trade) equilibria appear only from $k_{LT}\approx0.75\,\rho\Delta_T/2$, far above $(1-\frac1b)\rho m\Delta_T$.

R.3(b) also settles a numerics question analytically: the pool-free low-trade family ($\mathsf E=\rho$ exactly) cannot exist under (A3), because it has no pool. The numerics note rests this on 13 rows. The pooled low-trade members that the numerics referee found near $k=0.026$ are a different family and R.3(b) does not cover them.

### R.4 (likelihood-ratio lemma). Holds.

$\beta_d'(u)=\exp\{(|y|-|y+d|)/b\}$ with $y=F^{-1}(u)$ is nonincreasing, so $\beta_d$ is concave. The Neyman–Pearson step and the reflection for $q'>q$ are correct. Jensen gives the mixed case.

### R.5 (pool cap). Holds.

All five bounds follow. The function $\psi(y)=F(y)/F(y+2)$ is constant $e^{-2/b}$ on $y\le-2$ and strictly increasing after; $\lambda>e^{-2/b}$ because $\tau_L>m$. The bound uses only the signs of R.2 and the strict pool belief. Random test (`random_forcing.csv`): 856 consistent draws of mixed orders (one to three atoms per type) and pools with islands and tails, at six values of $c_L$. No bound is violated. The largest excess is $-2.8\times10^{-4}$, at $c_L=2.6$, which shows the bound is nearly tight.

### R.6 (forcing). Holds.

On $A$, $A_L\ge\rho\tau_L\Delta_T$ and $A_H\ge\rho m\Delta_T$. R.5 bounds the deviation mass in the pool. The strict inequalities of R.5 make $U_\theta'>0$ even at $k=K$. The converse also holds, because R.5 applies to full orders and any consistent pool. Random test: at $k=K(c_L)$ every one of the 856 consistent schedules gives strictly increasing payoffs for both types (smallest step $5.3\times10^{-5}$).

The digest says "unique full orders need a smaller cost $k\le K$". That is too strong. $K$ is sufficient. At $k=0.02>K$ all tracks find only $(1,-1)$ for $c_L\le2.975$.

### R.7 (bathtub). Holds.

The identity $\mathsf E(N)=\mathsf E_0-W_E(N\setminus Z_0)$, the budget $B_0$, and the ratio argument are correct. The supremum is not attained, so the bound is strict. Truncations fill the range. My cell knapsack (400,000 cells) reproduces Table 1 to $10^{-4}$ (`table1_check.csv`) and the plateau share $13.07\%$ at $c_L=3$.

**Tie rule.** The strict bound $\mathsf E>\mathsf E_0-V_E$ uses the paper's tie rule (an indifferent challenger prepares), so a pool needs belief strictly below $\tau_L$. With the opposite tie rule the supremum is attained, and (A4') must be strict to get $\mathsf E>\rho$.

### Proposition 2'. Holds, with four fixes.

1. The nonempty example ends at $c_L=2.58668$: $K(2.5867)=0.0079999<0.008$. Fixed.
2. The set is open only if the right inequality of (A3') is strict too. Fixed.
3. (A4') contains a pure $\rho$ condition: $\mathsf E_0<\rho(1-\pi_0)+(1-\rho)a$ for every pool (adversary Theorem AD.1, which I checked). So (A4') fails at every regime II $c_L$ once $\rho\ge0.5154$. Also, (A3') is empty at the paper's $(r_0,k,\rho)$. Added after the proposition.
4. Part (iii) states "every equilibrium" but does not show that one exists at $r_2$. Lemma C.1 below closes this.

The benchmark thresholds $3.4607$ and $3.7408$ are reproduced to $10^{-5}$ by four independent codes. Their status is numerical diagnostic (double-precision root of a closed form), not computer-assisted as the digest says.

### R.8 (universal bounds). Holds.

### R.9 (half-line family). Holds; Table 2 fixed.

The proof is right, including the last step: under (A3) and $\rho\le\frac12$ the investor test ends at $x_k$ with $e_H(x_k)<\rho$. But Table 2 had dashes at $\rho=0.1$ (both columns) and $\rho=0.2$ (ownership), under the caption "valid for every $k$ in the (A3) window". The dashes came from the test at $k=0.02$, which lies outside (A3) when $\rho<0.2231$. Inside the window the values are $4.0777$, $4.1503$ ($\rho=0.1$) and $3.9865$ ($\rho=0.2$ ownership) (`thresholds_check.csv`). Fixed. The $\rho=0.5$ entry value $3.1948$ correctly clamps the member at $x^*$, where $\mathsf E=a<\rho$.

### R.10 (starved family). Holds; part (b) upgraded.

Part (a) is correct. The identity $U_H(1)=kv/(b-v)$ holds to $10^{-15}$ in every member I built. Part (b) is analytical when $x'\ge1$ (Proposition C.2). Members with $x'<1$, which include every member at $c_L\le3.4211$ when $k=0.02$, remain numerical diagnostics. The adversary's floating-point certificate does not change this: the paper's online appendix, Section C.2, says "an unenclosed high-type derivative mesh is a diagnostic".

The corner $v=0$ is fully analytical. Its cutoff solves $C_L(0,x')=k$, so $x'=1.9061$. For $x'\ge1$, $F_H(s)=e^{-(1-s)/b}k$, so $U_H(s)<0$ on $(0,1)$ and $U_H(0)=U_H(1)=0$. It exists exactly for $c_L>3.9418$. The note's "$c_L\ge3.95$" is a grid value.

### R.11 (no pure starved pool when $\tau_L\le1-\tau_H$). Holds.

The reflection argument is right. It covers pure orders only, as the note says.

### R.12 (collapse). Holds.

The three cases are complete. $\Pr(N\mid H)>0$ follows from full support. Lemma C.1 adds existence.

### Section 6 and 7 claims.

- "The natural sufficient candidate is $c_L+c_H\le2B_{r_1}(\frac12)$." As a general statement this is false. At $\rho=0.5$, $c_L=2.5\le2.5833$, $k=0.02$ (inside (A3)), full-order half-line equilibria with cutoffs $-0.6,-0.5,-0.4$ have $\mathsf E=0.478,0.470,0.462<\rho$; both best responses are verified (`candidate_counter.csv`). At $\rho=0.6$, $c_L=2.4$, every equilibrium has $\mathsf E<\rho$: AD.1 bounds every full-order equilibrium, R.6 forces full orders since $K(2.4)=0.0234\ge0.02$, and R.6's converse gives existence. That last claim is analytical; the floating-point checks only confirm it. The candidate stands as an open question at $\rho=0.25$ only. Fixed in the note.
- "The starved family makes $c_L\le2.8326$ necessary at $k=0.0224$." Confirmed. Member at $c_L=2.9$, $k=0.0224$: orders $(1,-0.73)$, pool $(-\infty,0.1913)$, pool belief $0.3277<\tau_L=0.333$, regrets $0$ for both types, $\mathsf E=0.1227$, $\mathsf O_H=0.0833$ (`starved_a3.csv`). Over the whole (A3) window the infimum is $2.8319$, at $k\uparrow0.022412$.
- "Island pools at $k=0.02$ fail the reversal for $c_L>3.4607$." Confirmed at $c_L=3.5$ by the theory and numerics tracks. The numerics referee reports that the worst island pool fails the investor test at $c_L=4.0$. So this branch covers only part of $(3.4607,4)$; the starved and half-line branches cover the rest. The conclusion "fails above $2.9844$" is unaffected.

## 4. New referee results

**Lemma C.1 ($K$ is below half of (A3); analytical).** *For every $\tau_L\in(m,\frac12)$, $\tau_LS(\bar x+1)<m/2$. Hence $K(c_L)<\frac12(1-\frac1b)\rho m\Delta_T(r_1)$.*

*Proof.* Write $u=F(\bar x-1)$ and $w=F(\bar x+1)$, so $\tau_L=u/(u+w)$ and $\bar x>-1$. If $\bar x\le1$, then $u=\frac12e^{(\bar x-1)/b}$ and $1-w=\frac12e^{-(\bar x+1)/b}$, so $u(1-w)=\frac14e^{-2/b}$ is constant and $\tau_LS(\bar x+1)=\frac14e^{-2/b}/(u+w)$. The denominator is strictly increasing in $\bar x$ and equals $\frac12(1+e^{-2/b})$ at $\bar x=-1$, where the value is $\frac12e^{-2/b}/(1+e^{-2/b})=m/2$. So the value is below $m/2$ for $\bar x\in(-1,1]$. If $\bar x>1$, then $u\le w$, so $\tau_L\le\frac12$ and $\tau_LS(\bar x+1)\le\frac14e^{-(\bar x+1)/b}<\frac14e^{-2/b}<m/2$, because $1+e^{-2/b}<2$. Finally $K\le(1-\frac1b)\rho\Delta_T\tau_LS(\bar x+1)$. $\square$

*Consequences.* (a) (A3') is always less than half of (A3)'s right side. At the benchmark $\sup K=0.011206<\Delta_T(1.2)=0.016667$, so (A3') is empty at the paper's $(r_0,k,\rho)$. (b) Existence in part (iii) of Proposition 2'. If $c_L\le B_{r_2}(\frac12)$, Theorem CD.3(iv) at $r_2$ gives a full-order equilibrium when $k\le(1-\frac1b)\Delta_T(r_2)\rho m/2$, since $g_M=\rho$ there. Under (A3'), $k\le K<\frac12(1-\frac1b)\rho m\Delta_T(r_1)<\frac12(1-\frac1b)\rho m\Delta_T(r_2)$. If $c_L>B_{r_2}(\frac12)$, the dead profile exists (CD.3(ii)). So part (iii) is never vacuous.

**Proposition C.2 (closed-form starved members; analytical).** *Assume (A1') and (A2). Let $0\le v<v_H$, put $M_v=(1+e^{-(1+v)/b})^{-1}$, and let $x'\ge1$ solve*

$$
\tfrac12\rho\Delta_T(r_1)\,M_v\Big(1-\frac vb\Big)e^{-(x'+v)/b}=k .
$$

*If $F(x'-1)/[F(x'-1)+F(x'+v)]<\tau_L$, then orders $(1,-v)$ with the pool $(-\infty,x')$ form an equilibrium at $r_1$ with $\mathsf E=\frac\rho2[S(x'-1)+S(x'+v)]<\rho$ and $e_H=\rho S(x'-1)<\rho$.*

*Proof.* On $[1,\infty)$ the posterior is the constant $M_v$, and $\frac12<M_v<\tau_H$ because $v<v_H$. So on $A=[x',\infty)$ the cheap type enters (as $M_v>\frac12>\tau_L$) and the expensive type does not. $Z_0$ lies in $(-\infty,1)$, hence in the pool. The pool belief is below $\tau_L$ by assumption, so Lemma CD.2(e) gives the challenger's and the market maker's conditions. Low type: $C_L(v,x')=\rho\Delta_TM_v\int_{x'}^\infty e^{-x/b}/(2b)\,dx=\frac12\rho\Delta_TM_ve^{-x'/b}$, and the displayed equation is the first-order condition of R.10(a). The payoff is strictly concave, so $v$ is the best short; for $v=0$ the condition gives $U_L'(0)=0$ and concavity again gives the maximum. High type: for $x\ge x'\ge1\ge s$, $f(x-s)=e^{-(1-s)/b}f(x-1)$, so $F_H(s)=e^{-(1-s)/b}F_H(1)$ and

$$
U_H(s)=s\,e^{-(1-s)/b}F_H(1)-ks,\qquad U_H''(s)=F_H(1)e^{-(1-s)/b}\Big(\frac2b+\frac s{b^2}\Big)>0 .
$$

So $U_H$ is strictly convex on $[0,1]$ and its maximum is at an end point. By the identity of R.10(a), $U_H(1)=kv/(b-v)\ge0=U_H(0)$. Wrong signs lose (R.2). Entry follows from (R.0). $\square$

*At the benchmark* ($\rho=0.25$, $r_1=3$; `starved_closed.csv`). At $k=0.02$ the member with $x'=1$ has $v=0.50255$ (the unique root of a strictly decreasing function) and pool belief $0.39553$. So Proposition 2(ii) fails analytically for every $c_L>3.4211$: unique trading, $\mathsf E>\rho$ ($\mathsf E=0.0920$) and $\mathsf O_H>\rho/2$ ($\mathsf O_H=0.0625$) all fail. This improves the theory's analytical thresholds $3.6498$ (entry) and $3.8945$ (ownership). Over the (A3) window at $r_0=1.2$ the analytical threshold runs from $3.3714$ ($k\downarrow0.0167$) to $3.4581$ ($k=0.0224$). For $k\le0.01546$ the limit member $v\uparrow v_H$ already has $x'\ge1$, so the Table 3 entries for $k\le0.015$ are analytical. An independent quadrature check of the $x'=1$ member at $c_L=3.43$ gives both regrets below $2\times10^{-18}$ (`starved_closed_confirm.csv`).

## 5. Conflicts between tracks and their resolution

| # | conflict | which side is right | how settled |
|---|---|---|---|
| 1 | Numerics `kscan.csv`: $k_S(2.9)=0.0718$, $k_U(2.9)=0.0503$, and "(A3) is sufficient and not sharp for $c_L$ up to $2.9$" vs theory Table 3 ($2.8326$ at $k=0.0224$) | theory | Member at $(2.9,0.0224)$ verified by my code and found by numerics' own window solver. `k_starved` bisects on a predicate that is not monotone in $k$: at $c_L=2.9$ the numerics window solver reports starved candidates for $k$ from $0.0215$ to $0.045$, none from $0.05$ to $0.07$, and candidates again from $0.075$ (candidates only; the solver does not check the high type). $k_U$ also fails: starved equilibria at $(2.6,0.03)$, $(2.9,0.03)$, $(2.9,0.035)$ with $\mathsf E=0.161,0.146,0.155$ (`partial_outside_a3.csv`; the numerics referee confirms them with negative cutoffs). The reversal is not monotone in $k$: at $c_L=2.6$ it holds at $k=0.02$ and fails at $k=0.03$. The numerics referee wrote a fix into the numerics note. |
| 2 | Theory digest "an informative equilibrium exists iff $\rho\Delta_T>2k$" vs CD.4 | note, not digest | Counterexample at $\rho=0.1$, $k=0.04$ (Section 3). |
| 3 | Theory Table 2 dashes vs R.9's own proof | the proof | Values inside (A3) computed and written in. |
| 4 | Theory "sufficient candidate $c_L+c_H\le2B(\frac12)$" vs adversary AD.1 and the numerics $\rho=0.5$ map | adversary and numerics | Verified counterexamples at $\rho=0.5$ and $\rho=0.6$; note fixed. |
| 5 | Adversary Table 1, row $c_L=4.20$, and the triangle corner $(B(\frac12),0)$ vs numerics referee | numerics referee | My knapsack gives $\inf\mathsf E/\rho=0.061$ to $0.063$ at $c_L=4.2$ for all $\rho$, and the $\rho\to0$ threshold $4.1477$ ($\rho=10^{-3}$), $4.1496$ ($10^{-4}$). The corner is near $(4.1498,0)$. |
| 6 | Numerics: pool LP "is a relaxation, so its minimum is a lower bound" vs numerics sweep at $c_L=2.4$ | neither bound | LP minimum $0.42495$ exceeds the exact infimum $0.42453$, which is attained in the limit by half-line pools that the sweep found ($0.4245$). The LP cells of width $0.01$ restrict the pool, so the LP is not a lower bound. No conclusion changes: all values exceed $\rho$. |
| 7 | Numerics: "informative price survives for $c_L\in(B(m),c^*)$" vs theory R.3(a) | theory | R.3(a) proves it on all of regime II whenever $\rho\Delta_T>2k$; the numerics statement is too weak, not wrong. |
| 8 | Status labels: numerics and adversary call floating-point quadrature "computer-assisted"; the theory digest calls the (A4') thresholds "computer-assisted" | the paper's rule | Online appendix, Section C.2: "acceptance without an analytical argument or interval cover remains a numerical diagnostic". These rows are numerical diagnostics. Two adversary results are analytical instead: the $\rho=0.6$ claim (AD.1 + R.6) and the high-type check for members with $x'\ge1$ (Proposition C.2). |
| 9 | Forcing level at $c_L=2.62$: theory $0.0193$, numerics referee $0.01908$ | both are grid values | The difference is grid resolution in a diagnostic; both are below $0.02$, so the conclusion is the same. |

No conflict was found between a proved statement and a verified number. Every disagreement traces to a numerical procedure (bisection, cell LP, grid) or to a table or digest sentence that did not match its own proof.

## 6. Attacks that failed

- **Mixed orders.** R.2, R.4, R.5 and R.6 allow arbitrary order laws. The random test in Section 3 used one to three atoms per type. No counterexample.
- **Island pools.** R.5 and R.7 hold for every Borel pool. The knapsack is the exact worst case under full orders.
- **Tie rules.** At the pool, a belief of exactly $\tau_L$ makes the cheap type prepare, and a price with positive entry cannot pool flows with different beliefs (CD.2(b)). So the only pool is the no-entry price $t_0$, and its belief is strictly below $\tau_L$. The endpoint $c_L=B_{r_1}(m)$ is regime I. The limit member $v=v_H$ of the starved family hits $\tau_H$ on the plateau and leaves the family, so the starved threshold is strict. The corner $v=0$ has an indifferent high type, but $q_H=1$ is still a best response.
- **"In every equilibrium" under (A3').** R.6 covers every mixed profile and every continuous deviation. R.7 covers every consistent pool. Proposition 2'(ii) is a complete classification.
- **Pools that end below zero at $k=0.02$, $\rho=0.25$.** No starved candidate for $c_L\le2.98$ (numerics referee #4). This agrees with the theory's threshold $2.9844$.

## 7. Fixes written into `theory/note.md`

Each fix is marked "[Referee fix: ...]".

1. Section 1, item 2: non-uniqueness of entry under (A3) alone holds when $k<(1-\frac1b)J_G(z_0)$; open for large $\rho$.
2. After Proposition 2': the $\rho$ condition hidden in (A4'), and the emptiness of (A3') at the paper's triple.
3. Proposition 2': open set needs (A3') strict; the example ends at $c_L=2.58668$.
4. After R.10: the high-type check is analytical for $x'\ge1$; the analytical failure threshold at $k=0.02$ is $3.4211$; the corner exists exactly for $c_L>3.9418$.
5. After Table 3's paragraph: confirmation of the member at $(2.9,0.0224)$ and the window infimum $2.8319$.
6. Table 2: values in place of dashes for $\rho=0.1$ and $\rho=0.2$, with the reason.
7. Section 1, item 4, and the ledger rows on unique trading, unique entry, $\mathsf E$ and $\mathsf O_H$: the analytical threshold $3.4211$, the window infimum $2.8319$, the $\rho$ condition, and the range of the non-uniqueness proof.
8. Section 7 on the candidate $c_L+c_H\le2B(\frac12)$, and open item 1, both restricted to $\rho=0.25$.

## 8. Open items (referee view)

1. With the paper's (A3) at $k=0.02$ and $\rho=0.25$: is the reversal true in every equilibrium for $c_L\in(2.3662,2.9844]$? All searches (pure lattices, all-pool LP, mixtures, islands, negative cutoffs) find no counterexample. Status: open; numerical diagnostic support.
2. Unique on-path entry under (A3) alone for $\rho\ge0.699$ with $\tau_L$ near $\frac12$. Status: open.
3. The failure in $c_L\in(2.9844,3.4211]$ at $k=0.02$ rests on members with $x'<1$, whose high-type check is a floating-point grid or mesh. An interval enclosure would make it computer-assisted. Status: numerical diagnostic.
4. Monotonicity of $\inf\mathsf E$ in $c_L$, which turns (A4') into "$c_L\le3.4607$", is seen on grids only. Status: numerical diagnostic.
5. A sharp replacement for (A3). The admissible set of $k$ is not an interval at fixed $c_L$ (Section 5, row 1), so any sharp replacement must be a set, not a single upper bound. Status: open.

## 9. Files

- `referee.py`: pure functions. Closed-form payoffs; full-order posterior and pool belief; forcing bound $K$; a cell knapsack; half-line thresholds; general investor payoffs by adaptive quadrature for orders $(q_H,q_L)$ and a half-line cutoff; global best responses (grid plus bounded refinement); the starved family by quadrature and in closed form; a random test of R.5 and R.6.
- `run_checks.py`: writes all CSVs. Run `python3 run_checks.py` in this folder (under a minute).
- CSVs: `table1_check.csv`, `thresholds_check.csv`, `starved_a3.csv`, `starved_closed.csv`, `starved_closed_confirm.csv`, `candidate_counter.csv`, `partial_outside_a3.csv`, `jgap.csv`, `random_forcing.csv`. Every row is a numerical diagnostic in double precision. The analytical statements they support are Lemma C.1 and Proposition C.2, whose proofs are above.
