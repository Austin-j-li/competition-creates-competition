---
title: "Referee report: selection design in the endogenous-insider fork"
date: "2026-10-03"
---

## 1. Scope and method

This report checks `../note.md` and `../selection_solve.py`. I tried to refute every result. For each one I checked the proof steps, the signs, the edge cases (tie rule, $\tau_s=M$, $\tau_s\le\tfrac12$, $\tau_s=m$, price atoms, plateaus, mixed orders, null sets), and whether the stated status is earned.

I re-implemented the key numbers independently in this folder.

- `check.py` re-derives the closed forms and evaluates them in 30-digit arithmetic (mpmath). It also holds an independent grid layer. That layer computes the deviation payoff $F_\theta(s)$ by an exact recursive Laplace convolution on a flow grid of step $0.001$. It does not use the author's kernel matrix.
- `run_closed.py` and `run_closed2.py` check every closed-form claim and Tables 1, 2, 4, 6 and 7. Outputs: `ref_closed.csv`, `ref_table2.csv`, `ref_table4.csv`.
- `run_grid.py` checks cutoff-family members and Table 3 rows with the independent grid layer. Output: `ref_grid_points.csv`.
- `run_gap.py`, `run_gap_fine.py` and `run_gap_mixed.py` probe the gap region of Table 3. Outputs: `ref_gap_scan.csv`, `ref_gap_mixed.csv`.
- `rerun_author.py` re-runs the author's solver with output sent to `rerun/`. All nine CSV files are byte-identical to the author's files.

## 2. Summary verdict

The analytical core survives. I found no wrong sign and no false proof step in Lemma S.1, Lemma S.2, Propositions S.1 to S.3, S.5, S.7 to S.9, or the public-signal remark. Every number in Tables 1 to 7 that I recomputed agrees with the note to the printed digits.

The main problems are of scope, not of truth.

1. Proposition S.4 is false as stated in general. It needs $s_M\le p^2/r$. At the benchmark this fails for $r>3.7736$. It holds at $r=3$.
2. Corollary S.6 is correct as a formal statement, but its reading as "the strong form of the paper's comparison" overreaches. The same backstop leaves no equilibrium at $r_0$. The comparison therefore holds a posting rule that depends on $r$, not one institution.
3. The remark after Lemma S.1 understates how often (S) fails. For $\kappa=1$ it fails on a whole interval of $s$ below $s_D$. The failure is harmless up to a null set, except at one knife edge, where the minimal-pool profile is not an equilibrium.
4. In Proposition S.1(v)(d), "the interval shrinks" is not proved. Both ends fall. The length falls on a grid, so this part is a numerical diagnostic.
5. A few interpretive sentences in Sections 2, 4.2, 6.1 and 6.2 drop an existence caveat or a selection caveat.

I marked thirteen small fixes in `note.md` with "[Referee fix: ...]". Section 5 lists them in eleven groups. I deleted nothing.

## 3. Result-by-result verdicts

### Lemma S.1 (structure under a uniform subsidy; analytical). Verdict: holds, remark needs a fix.

The proof is correct under (S). Part (d) does not even need (S): the residual $e(x)\Delta_T(1-\mu_X(x))$ follows from $P(x)=\mathbb E[V_T\mid X=x]$ with $e$ measurable in $X$. Part (c) holds up to a null set, because $\mu_P$ is defined only almost surely at prices of zero probability. This is the same gloss as in Lemma F.1 of the fork. It changes no result.

The remark says that a failure of (S) "needs the knife edge $\kappa s=w_L+M_q\Delta_T$". That is true for a failure that matters, but it hides how common (S) failure is. At $r=3$ and $\kappa=1$, (S) fails for every $s\in[0.638,0.946]$. That interval contains Table 4 rows $c=5.202$ and $c=5.222$ (their $s_D$ is $0.910$ and $0.930$), the breakeven cost $5.2145$, and the crossing $s=0.936$ where $\mathsf N=t_0$ in Table 2. I checked the consequence under full orders. The critical flow $\hat x$ with $\mu_X(\hat x)=(\kappa s-w_L)/\Delta_T$ is one point. For $s<0.8596$ it lies in the pool already. For $s\in[0.8596,0.9457)$ it lies in the candidate entry set, but its price is $t_0$, so the challenger does not prepare there, and $A$ loses one point. The profile stays an equilibrium up to a null set. At the knife edge $s=0.9457$ the whole plateau $x\ge1$ has price $t_0$. The belief at $t_0$ is then $0.4814$, below $\tau_s=0.5915$. The challenger does not prepare at $t_0$, so the minimal-pool profile fails at that single $s$. No table row sits exactly there. I added this to the remark.

### Lemma S.2 (closed form for $J$; analytical). Verdict: holds.

I re-derived both pieces. On $y\ge1$, $g=m\,f(y-1)$. On $|y|<1$, $g=e^{-1/b}/(4b\cosh(y/b))$, and $b\operatorname{gd}(y/b)$ is an antiderivative of $\operatorname{sech}(y/b)$. The closed form agrees with adaptive quadrature to $10^{-31}$ at $x\in\{-1,-0.5,0,0.5,1,x^*\}$.

The consequence also holds. $m>1/4$ is $e<3$. So $J(3)\ge m/3>1/12$ and $(1-1/b)J(3)>1/24>k$. I also checked the rest of F.3 at the benchmark by hand. The tightest inequality is $B_{3.6}(M)=5.99731<6$. It needs $M<0.731395$, that is $e<2.72294$, so elementary bounds on $e$ suffice. Open item 1 of `mechanism.md` does close, and F.3 at the benchmark is analytical.

The extension "for every $\tau_s\in(m,M]$ once $r>2.1241$" is correct: $\mathfrak r\big(2k/((1-1/b)m)\big)=2.124148$.

### Proposition S.1 (equilibrium set as a function of $s$; analytical). Verdict: holds, with two fixes.

- (i), (ii), (iii): correct. (i) and (ii) do not need (S).
- (iv): correct under (S).
- (v)(a): correct. At $\Delta_T=2k$ exactly, the types are indifferent on $[0,1]$ and $[-1,0]$, and equal strategies force $\delta_0$; the proof covers this. Uniqueness for $\Delta_T<k$ is correct.
- (v)(b): correct. The step "$\mu_P=\tfrac12$ a.s. and $\Pr(N)>0$ give $\bar\mu_N=\tfrac12\ge\tau_s$" is right, because $t_0$ is a price atom. Injectivity of the Laplace convolution is right (characteristic function $1/(1+b^2t^2)$).
- (v)(c): correct. The threshold $r=1.71405$ in `key_numbers.csv` is right.
- (v)(d): the challenger and market-maker conditions are correct. I checked that $\bar\mu_{x'}$ equals $m$ for $x'\le-1$ and rises strictly on $(-1,\infty)$: the Laplace reverse hazard $f/F_Z$ is constant on $z\le0$ and falls on $z>0$. The sentence "the interval shrinks as $s$ rises" is not proved, because $x^*_s$ also falls. I computed the length on 400 values of $\tau_s\in(m,\tfrac12)$. It falls strictly, from $10.84$ near $\tau_s=\tfrac12$ to $0.108$ near $m$. I marked this part as a numerical diagnostic in the note.
- (vi): correct.

The text after S.1 says that at $\Delta_T\le2k$ "the replacement is $\mathcal C$". The note proves uniqueness of $\mathcal C$ only for $\Delta_T<k$. I added that qualifier.

### Proposition S.2 (minimal-pool selection as $s$ rises; analytical). Verdict: holds.

(a) The refinement argument is right, including the plateau cell. (b) $e_H+e_L=S_Z(-\delta)+S_Z(\delta)=1$ is right for any pure $q_H>q_L$; the grid rows at $r=1.55$ and $r=1.70$ confirm it. (c) The limit $(3-e^{-2/b})/4=0.65803$ is right.

### Proposition S.3 (seller's accounting; analytical). Verdict: holds.

(a) is competitive pricing plus the per-share reading of $V_T$. (b): I re-derived (S.4) term by term. It agrees with direct evaluation to $10^{-30}$ on $[1,10]$. $d$ is concave, $d(1)=\tfrac34$ exactly, and $d(10)=4.05m-1.05=0.03921>0$. The minimum on $[1,10]$ is at $r=10$. (c): $t_\theta+g_\theta=\theta$ holds case by case, so $\mathsf N=(h+\ell)/2-c=-\tfrac12$.

### Proposition S.4 (surplus-maximizing subsidy; analytical). Verdict: holds only with an added hypothesis.

The derivative formula is right on $(m,M)$, where $G$ has a density. But the statement claims a maximum at $p^2/r$ with no condition. If $s_M>p^2/r$, then $\mathcal W$ falls on the whole window and the maximum is at $s_M$. At the benchmark $s_M(r)=p^2/r$ at $r=3.7736$. Grid check: at $r=4$, $s_M=0.149>0.0625=p^2/r$ and the argmax is $s_M$; at $r=5$ the argmax is $s_M=0.515$. At $r=3$ the argmax on a 4000-point grid is $0.0832$, next to $p^2/r=0.0833$. I added the hypothesis in the note.

### Proposition S.5 (backstop; analytical). Verdict: holds.

I tried to break (i) and (ii) with off-path prices in $I_\varepsilon$, with preparation on null sets, with a tie at $\bar\mu_N=\tau_{\bar s}$, and with a fee $s_0<0$. None breaks it. The key step is right: any preparation price in $I_\varepsilon$ would equal $t_0+w_L-\kappa\bar s+\Delta_T\mu_X$, which (B) puts outside $I_\varepsilon$. The claim that every equilibrium has a pool is right ($\tau_{s_0}>\tfrac12=\mathbb E\mu_X$). (iii) to (v) follow. Part (v) is correctly restricted to full-order equilibria. Part (vi) is a genuine nonexistence result. I checked it at $r>r_C$ by hand: zero orders, no preparation and price $t_0$ make the challenger prepare at $t_0$; preparation then moves the price below $t_0-\varepsilon$, where the backstop is not paid and the challenger does not prepare. With deterministic preparation there is no fixed point.

Benchmark numbers: the bound on $\varepsilon$ at $\bar s=s_D$ is $\min\{0.63763,0.76263\}=0.638$. The window top $c-B_3(\bar\mu^*)=2.805151$ with $\bar\mu^*=0.3683819$. Both agree.

### Corollary S.6 (analytical). Verdict: holds with a fix to its reading.

The formal statement is right once "no backstop" reads "no pure backstop that satisfies (B)". At $r_0=1.2$, (B) is easy to meet ($w_L+M\Delta_T=0.408<s_D=1.196$).

The paragraph after it says the backstop "restores the strong form of the paper's comparison". In the paper the institution is the same at $r_0$ and $r_1$. Here, at $r_0$ the same backstop leaves no equilibrium (S.5(vi)). So "bystander in every equilibrium" at $r_0$ refers to the economy without the backstop, and "insider in every equilibrium" at $r_1$ refers to the economy with it. The comparison is valid for a posting rule that conditions on the public $r$. That is a weaker and different claim. I added a fix that says so.

### Proposition S.7 (lottery; analytical). Verdict: holds.

With $\kappa=1$ the price gains a constant $-\rho\kappa s_\ell$ term. The monotonicity (A.3) and the inversion (10) survive the constant, so "verbatim" is fair. Table 6 lottery rows agree: $\rho=0.07$ gives $\mathsf N=0.5374$, outlay $0.2544$, $\mathcal W=-0.0143$; $\rho=0.25$ gives $-0.0361$, $0.9085$, $-0.326$. The note uses $s_\ell=s_m$ with the tie rule and says so.

### Proposition S.8 (reserve; analytical). Verdict: holds.

$g_v(p',r)$ is nonincreasing in $p'$ pointwise, and $B_{0,r}(\tfrac12)<h/2\le c$ on $r>\ell$. I also checked that $\tau$ rises with $p'$: for $p'\le\ell$ both $g_H$ and $g_L$ fall at rate $p'/r$, so the denominator of $\tau$ stays fixed. Table 7 agrees. The text says $\tau$ exceeds $M$ "above $p'=1.5$". The exact crossing is $p'=1.3253$. I added that.

### Proposition S.9 (flow disclosure; analytical). Verdict: holds.

The statement is right. Table 6 calls the whole row "minimal pool only; analytical". S.9 shows that at each order profile only the minimal pool survives. It does not show that full orders are the only live profile under disclosure. I narrowed the status in the table.

### Remark (public signal). Verdict: holds.

$t_0+\tfrac12(t_H-t_0)=0.979167$ at $r=3$, and $g_H(3)=8.458>c>g_L$.

### Headline (Section 2). Verdict: holds with a fix.

Every number agrees. The backstop sentence omits the existence condition of S.5(iv) and the nonexistence of S.5(vi). I added it.

## 4. Numerical re-implementation

### Closed forms (30 digits)

All Table 1 entries agree: $s_M=-0.2171548$, $s_D=41/24$, $s_m=3.6338215$, $w_L+M\Delta_T=0.9457057$, $d(3)=0.7626276$, $J(3)=0.0955029$, $\Delta_Tm/2=0.0896471$, $\bar\mu^*=0.3683819$, window top $2.8051508$, $\rho_N=0.06$, $\rho_U=0.2230969$, $\mathfrak r(k)=1.2209975$, $\mathfrak r(2k)=1.3256571$, $r_C=3.5926585$. The two roots are $2.0155164$ and $1.8434221$ by 30-digit bisection.

Table 2: all ten rows agree in every column to the printed digits. The crossing $\mathsf N=t_0$ is at $s=0.93574$ ("near $0.93$"). $\mathcal W$ turns negative at $s=1.76833$, just above $s_D$.

Table 3: $s_D$, $d(r)$, $t_0$ and $\mathsf N$ agree at all listed $r$. Under $\mathcal C$, $\mathsf N=-\tfrac12$ exactly.

Table 4: all rows agree. The breakeven against $\mathcal D$ is $c=5.2144898$. On a 2000-point grid of $c\in(B_3(\tfrac12),B_3(M)]$, the gain over the live minimal pool is at most $-0.00043$. Near $c=B_3(\tfrac12)$ it behaves like $-0.442\,(c-B_3(\tfrac12))$. "Never beats the live equilibrium" therefore stands as a numerical diagnostic; a proof looks within reach.

### Grid layer

The independent convolution gives $F_H(1)=0.095490$ against the closed form $0.095503$ (relative error $1.3\times10^{-4}$, from the entry jump between grid nodes).

Cutoff family at $r=3$, $s=0$: members $x'=0.872$, $2.572$, $2.622$ and $3.222$ are fixed points of the independent best-response map within one order-grid step ($0.001$). Their pool posteriors agree with `backstop_family_r3.csv` to $10^{-5}$. At $x'=3.272$ the best response is $(0,0)$, which matches the fork's reported collapse. Since $\bar\mu_{x'}$ rises with $x'$ along the whole searched family, the member counts in Table 5 follow from the posteriors in the CSV. I reproduced them.

Table 3 rows at $s=s_D$: $(1,-0.227)$ at $r=1.55$, $(1,-0.718)$ at $r=1.70$ and $(1,-1)$ at $r=1.85$ are fixed points of the independent map; $\mathsf E=\tfrac12$ in each.

### The gap region of Table 3 (open item 1)

I confirm that no pure, correctly signed fixed point exists on a grid of step $0.02$ at $r\in\{1.35,1.40,1.45,1.50\}$, nor on a finer grid of step $0.004$ near $(1,0)$ at $r\in\{1.45,1.50\}$. The best-response map sends $(0,0)$ to $(1,-1)$ and $(1,-1)$ to $(0,0)$, as the note says. The pure branch starts between $r=1.50$ and $r=1.51$: at $r=1.51$ there is a fixed point near $(1,-0.034)$, and at $r=1.52$ near $(1,-0.086)$. These two strengths are off the note's grid, so the note's "$\approx1.55$" is consistent but loose.

The high type's best response in the gap is a corner, $0$ or $1$. That suggests a mixed candidate. I tested two.

- Candidate (a): the high type buys $1$ with probability $\lambda$ and otherwise abstains; the low type abstains. Then $A=[\tfrac12,\infty)$ for every $\lambda>0$. At $r=1.45$ and $r=1.50$ there is $\lambda^*$ ($0.226$ and $0.943$) at which the high type is indifferent between $0$ and $1$, every other order is strictly worse, the low type's best response is $0$, and the pool posterior is below $\tfrac12$. On the grid this is a mixed equilibrium (numerical diagnostic).
- Candidate (b), symmetric mixing over $\{0,\pm1\}$, fails at both strengths: the low type gains from a small short.
- At $r=1.35$ and $r=1.40$ both candidates fail. Even as $\lambda\to0$ the high type's full order loses: $\Delta_T\,S_Z(-\tfrac12)/2<k$ there.

So existence at $s=s_D$ is still open on roughly $(\mathfrak r(2k),1.45)$. The author may want to state candidate (a) as the next step for open item 1, or to try for a nonexistence proof near $\mathfrak r(2k)$.

## 5. Fixes made in `note.md`

Each fix is marked "[Referee fix: ...]".

1. Section 2: the backstop removes $\mathcal D$ only where a live equilibrium with $\bar\mu_N<\tau_{\bar s}$ exists; elsewhere it leaves no equilibrium.
2. Remark after Lemma S.1: (S) fails on $s\in[0.638,0.946]$ at $r=3$; harmless up to a null set; the knife edge $s=w_L+M\Delta_T$ breaks the minimal-pool profile.
3. S.1(v)(d): the intervals are not nested; the length claim is a numerical diagnostic.
4. Text after S.1: $\mathcal C$ is proved unique only for $\Delta_T<k$.
5. S.4: needs $s_M\le p^2/r$; fails for $r>3.7736$ at the benchmark.
6. Corollary S.6 statement: the claim at $r_0$ assumes (B).
7. Paragraph after S.6: the comparison holds a posting rule that conditions on $r$, not one institution.
8. Reserve paragraph: the crossing $\tau=M$ is at $p'=1.3253$.
9. Table 1: floating-point roots are numerical diagnostics in the paper's vocabulary.
10. Table 6, flow disclosure: the status covers $\mathcal D$ and the full-order minimal pool only.
11. Section 6: existence caveat for "every equilibrium at every strength"; the hump prediction assumes $\mathcal D$ below $s_D$; the backstop's surplus is $0.107$ only for the minimal pool (searched range $0.011$ to $0.107$ at $\bar s=s_D$).

## 6. Code

The code follows the rules: pure functions with type hints, frozen records, CSV output only. A re-run reproduces every CSV byte for byte. Grid rows carry "numerical diagnostic"; closed-form rows carry "analytical" only where the note proves the formula and the test.

Two small issues. Neither changes any reported number.

1. `J_closed` adds $m/2$ whenever `x_cut <= -1`. That is the value at $x_{\rm cut}=-\infty$, not at a finite cut in $(-\infty,-1]$. At $x_{\rm cut}=-1$ exactly it double counts. The function is never called with such a cut, because `x_star_full` returns $-\infty$ at $\tau_s\le m$. A guard or the exact tail term $m[\tfrac12-F_Z(x_{\rm cut}+1)]$ would remove the trap.
2. The sweep labels rows with $s\in[0.638,0.946]$ "analytical" although (S) fails there. Fix 2 above explains why the label still holds up to a null set.

## 7. What I could not confirm

- Proposition S.5(v) and the Table 5 family cover full-order and interval-pool members only. I did not search non-interval pools or mixed profiles under the backstop. The pessimistic value of the backstop stays a numerical diagnostic, as the note says.
- "The minimal subsidy never beats the live minimal pool" holds on my grid of $c$ but has no proof.
- I did not check the fork's own Propositions F.4 and F.5, which the note does not use.
