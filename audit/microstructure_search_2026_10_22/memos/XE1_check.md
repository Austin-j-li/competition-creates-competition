# XE1: Independent check of E1 (auction-side extensions under the order slot)

## 1. Scope

This memo checks the six headline claims of `memos/E1_auction_side.md`.
The paper is `overleaf/paper` at commit `01bd5d6` (`main.tex`, `online_appendix.tex`, the class-exhibit and reserve tables).

**Model as checked.** One public order slot, unit menu $\{-1,0,1\}$.
With probability $\lambda$ the informed investor fills the slot; it sees the class, not the value.
Otherwise a liquidity trader sells, waits, or buys with probabilities $(\beta,1-2\beta,\beta)$.
Market makers see the order $Q$ and set $P=\mathbb E[V_T\mid Q]$. The challenger sees $P$.
Write $b=(1-\lambda)\beta$, $b_0=(1-\lambda)(1-2\beta)$, $u=\lambda/b$, $\kappa=\min\{m,1-M\}$.

**Equilibrium concept.** Perfect Bayesian equilibrium of the finite order game.
Every flow has liquidity mass in every class, so Bayes' rule applies everywhere; no off-path belief is used.
Challenger tie rule C1 (prepare at indifference). Investor rules IM and I0.
Every example below has strict investor margins, so both investor rules give the same outcome.

**Method.**

1. I derived each claim by hand from the primitives.
2. I wrote a new program, `scripts/XE1_check/xe1_check.py`. Its output is `scripts/XE1_check/results.txt`.
   - Auction objects come from quadrature of the sale payoffs, not from closed forms.
     Over $R\sim U[0,r]$ the program uses the midpoint rule on each linear piece (exact).
     Over a uniform class band it uses Milne's open rule on each polynomial piece (exact for cubics).
     The quadrature equals the paper's closed forms exactly at six test strengths.
   - Calibration A and all auction objects use exact fractions.
   - Calibration B uses outward interval arithmetic at 40 digits. A sign counts only when the interval excludes zero.
   - Equilibria: the program enumerates all nine pure order profiles at each node and tests best responses.
     The analytical return bounds cover mixed profiles.
3. I derived calibration B from the paper's equation (12), not from E1's (2):
   $\tau(3)=141/200$, $x^*=\log(141/59)$, $\mathsf E_*=0.5227572972597\ldots$, $u=e-1$.
   The slot-B bounds $m,M$ equal the Laplace bounds at priors $1/10,3/10,1/2,7/10$ to 40 digits.
4. Only after step 2, I ran E1's program with its output directed to `scripts/XE1_check/e1_rerun/`.
   Its five output files are byte-identical to E1's saved files. I then compared the numbers.

**Not checked.** Coexistence, X1, X3, X4 and the atomless-cost variant of X5 (all E2).
The run used one slot and took about seven seconds.

## 2. Verdict table

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| 1 | The coordinator's general-prior Prop. 2 omits $B_{F_0}(\pi)<c_H$; E1's counterexample gives weak entry one; corrected hypotheses (3), ownership condition (6); the all-strategy posterior bound needs $\beta\le1/3$ | **CONFIRMED** | All counterexample margins reproduced exactly (A) and by intervals (B). Unique pure equilibrium $(0,0)$ at $6/5$ with entry 1; entry then falls to $37/68$ (A) or $\mathsf E_*$ (B). Proof of (3) re-derived. At $\beta=2/5$ the zero-flow posterior reaches $41/52>M=26/37$. The omitted inequality is the left half of the paper's own (A1). One addition: the paper's sufficient ownership condition fails to transfer when $b+\lambda<1/2$ (§3.2). |
| 2 | X2: the two-class reversal holds for any ranked pair and interior prior; every paper two-class example works with the paper's costs and strengths under A and B | **CONFIRMED** | Construction re-derived; it needs only $M>\pi$ and $\kappa>0$. Every strict margin is positive for the moderate values, the bands, the benchmark, and Cases A–C, under A and B. Case D fails $B_1(M)>c_H$ under both. The C.4 sequence admits $n=3$ first. Entry levels differ from the paper's. |
| 3 | X2 with three classes: an exact equilibrium with two posteriors at one price; a restricted two-group result | **CONFIRMED** | The unrestricted statement fails literally. Exact reproduction under A; interval reproduction under B. Severity: a knife-edge. A perturbation of $\pm1/1000$ separates all three prices with the same strict orders. The pooled flows have equal gross profit, so pooling does not change entry. Order observation removes the failure. |
| 4 | X5: access raises proceeds and net surplus in the recruiting region; outside it access can lower both | **CONFIRMED** | Direct summation: A gains $113/408$, $5/68$; B gains $0.2579481359412$, $0.0819603370846$. Outside: A $-77/408$, $-1/68$ at $c_H=49/20$; B $-0.1739175847201$, $-0.0135047169563$ at $c_H=12/5$. Surplus falls exactly when $B_1(m)+pF_1(p)>c_H$. |
| 5 | X6: the payment-rule comparison holds unchanged | **CONFIRMED** | The result concerns the acquisition stage only. Exact formulas at $r=6/5,3$ reproduced; $\Delta_\eta(3)-\Delta_\eta(6/5)=(13/20)(1-2\eta)$. |
| 6 | X7: flat slot entry across strengths at the paper's exclusion reserve; $p=1.55$ restores strict deterrence and higher proceeds but excludes the weak incumbent | **CONFIRMED** | Entry $37/68$ (A) and $\mathsf E_*$ (B) at both strengths, at $p=1.01$ (points) and $p=1.1$ (bands). At $p=31/20$: entry $37/68\to1/4$ (A), $\mathsf E_*\to1/4$ (B), with higher proceeds. Sharpening: the exclusion is forced, not a choice (§3.7). |

## 3. Derivations

### 3.1 Auction objects

For a prepared challenger with value $v\ge p$, the target receives $\max\{p,\min(R,v)\}$.
The challenger earns $(v-\max\{p,R\})_+$. A value $v<p$ is not admissible; the target then receives $p\mathbf 1\{R\ge p\}$.
These payoffs are piecewise linear in $R$, with kinks at $p$ and $v$.
Their expectations over $R$ are piecewise quadratic in $v$, with breaks at $p$ and $r$.
The two quadrature rules are therefore exact.

Checks printed by the program:

- At $r\in\{6/5,3,18/5,8\}$ ($h=10$) and $r\in\{21/20,3/2\}$ ($h=2$), quadrature minus closed form is exactly zero for $t_0,t_H,t_L,g_H,g_L,\Delta$.
- The identity $t_v+g_v=v$ holds exactly.
- The band spread equals $[(r-1)^2+\varepsilon^2/3]/(2r)$ exactly at $r=6/5,3,18/5$.

### 3.2 Claim 1: general-prior Proposition 2

**The paper already has the inequality.** The paper's (A1) is $B_{F_0}(\pi)<c_H<B_{F_1}(M(\pi))$.
The coordinator's list keeps $\pi<\tau_1<M<\tau_2$, which is $B_1(\pi)<c_H<B_1(M)$ and $B_2(M)<c_H$.
It drops the left half of (A1). E1's "correction" restores the paper's own hypothesis.

**Counterexample (calibration A analytical; B computer-assisted).**
Benchmark values, $\pi=1/2$, $\rho=1/4$, $k=1/50$, $c_H=47/10$, strengths $(6/5,3,8)$.

| Margin | A (exact) | B (interval midpoint) |
|---|---:|---:|
| $k-\Delta_0$ | $1/300$ | $0.0033333$ |
| $c_H-B_1(\pi)$ | $49/120$ | $0.4083333$ |
| $B_1(M)-c_H$ | $22/15$ | $1.5171548$ |
| $c_H-B_2(M)$ | $223/640$ | $0.3124647$ |
| $\rho\kappa\Delta_1-k$ | $31/1200$ | $0.0248236$ |
| $\rho\kappa\Delta_2-k$ | $2439/12800$ | $0.1859083$ |
| $c_H-B_0(\pi)$ (omitted) | $-5/48$ | $-0.1041667$ |

At $F_0$ every unit residual is at most $e\Delta_0\le\Delta_0<k$, so zero is the unique order, also against mixtures.
All posteriors then equal $\pi$. Since $B_0(\pi)=1153/240>47/10$, both cost types prepare and entry is one.
At $F_1$ full orders give entry $37/68$ (A) or $\mathsf E_*$ (B). Entry falls. The enumeration finds exactly these outcomes.

**Corrected statement (3) (analytical).** My derivation:

1. Under any informed strategy, $a_j(\pm1)\in[b,b+\lambda]$. Hence $\mu_{+1}\le M$ and $\mu_{-1}\ge m$.
2. A class-H purchase earns $e(+1)\Delta(1-\mu_{+1})-k\ge\rho\kappa\Delta-k$. A class-L sale earns at least the same bound.
   A wrong-sign order earns $-e\Delta(\cdot)-k<0$. So $\Delta_i\rho\kappa>k$ forces full orders, uniquely.
3. Full orders give posteriors $(m,\pi,M)$. The zero-flow posterior enters no return, so the proof never uses a bound on it.
4. Redundancy: $g_j(F)=\int_p^\infty[1-G_j]F\,dv$ falls under strengthening, so $B_1(\pi)\le B_0(\pi)$.
   $\Delta_F=\int_p^\infty D(1-F)\,dv$ rises, so $\Delta_2\ge\Delta_1$. Also $g_H-g_L=\int D F\ge0$, so $B_2(\pi)\le B_2(M)$.
5. Entry formula (5) and condition (6) follow from $\Pr(Q=+1\mid H)=b+\lambda$ and $\Pr(Q=+1\mid L)=b$.

**Ownership sufficient condition (analytical; a change to Prop. 2(ii) for some slots).**
The paper's condition $(1+\rho)W_H(F_1)\ge2\rho W_H(F_0)>0$ implies (6) when $e_H>(1+\rho)/2$, that is $b+\lambda>1/2$.
A has $b+\lambda=29/51$; B has $0.5317$. For smaller $b+\lambda$ the paper's sentence fails. My own example:

- Point masses 10 and 1, $p=1/2$, $\rho=1/4$, $\pi=1/10$, $\lambda=2/25$, $\beta=1/125$ ($b+\lambda=0.08736$).
- Strengths $(21/20,40/3,40)$, $c_H=17/10$, $k=1/200$. Every margin of (3) is positive.
- $W_H=1$ at $21/20$ and $3/4$ at $40/3$. The paper's sufficient margin is $7/16>0$.
- The slot margin (6) is $-167/12500<0$. Ownership falls from $1/40$ to $1479/62500$.

E1 says "for other slots, use (6)". That is correct; the example makes the consequence explicit.

**Zero-flow bound (analytical).** The zero-flow mass is $b_0+\lambda\sigma_j(0)$. Its ratio is bounded by $1+u$ only if $b_0\ge b$, that is $\beta\le1/3$.
The program maximizes the zero-flow posterior over pure strategies at $\lambda=6/17$, prior one half:

| $\beta$ | $M$ | Largest zero-flow posterior |
|---|---:|---:|
| $1/4$ | $35/46$ | $23/34$ |
| $1/3$ | $29/40$ | $29/40$ (tight) |
| $2/5$ | $26/37$ | $41/52$ |

**Prior windows.** Solving $M(\pi)=\tau_1$ and $M(\pi)=\tau_2$ gives $(1551/3262,46695/91906)$ under A and $(0.4678500296861,0.5004243073201)$ under B.
The omitted inequality has margins $1.416$ and $1.123$ at the A ends. The ledger's windows stand.

### 3.3 Claim 2: two-class value classes

**Construction (analytical).** E1's (7) is correct.
For $R\sim U[0,r]$, $1-F(v)=r^{-1}\int_v^r dx$, so Tonelli gives $\Delta(r)=r^{-1}\int_p^r\Gamma(x)\,dx$.
Since $\Gamma$ is nondecreasing, $\int_p^r\Gamma\le(r-p)\Gamma(r)$; this gives $\Delta'(r)\ge p\Gamma(r)/r^2$ and $g_H-g_L\ge p\Gamma/r$.
The paper's A.4 argument then goes through with two slot inputs only: $M>\pi$ and $\kappa>0$.
The factor $1-1/b$ disappears. The slot version is weakly easier than the Laplace version.

**Examples (A analytical, B computer-assisted).** Decisive margins:

| Example | $k-\Delta_0$ | $B_1(M)-c_H$ A | $B_1(M)-c_H$ B | $c_H-B_2(M)$ A | $c_H-B_2(M)$ B |
|---|---:|---:|---:|---:|---:|
| Moderate, $h=2$ | $17/21000$ | $59/2400$ | $0.0301370$ | (no third strength) | (no third strength) |
| Benchmark points | $1/300$ | $1/6$ | $0.2171548$ | $371/7200$ | $0.0026889$ |
| Bands, $\varepsilon=1/20$ | $43/14400$ | $48011/288000$ | $0.2171922$ | $17797/345600$ | $0.0026578$ |
| Case A | $3/550$ | $15/328$ | $0.1091794$ | $49/410$ | $0.0581371$ |
| Case B | $3/550$ | $659/7080$ | $0.1234127$ | $3439/21240$ | $0.1325687$ |
| Case C | $1/150$ | $706193/22939200$ | $0.0588908$ | $354251/1038400$ | $0.3145507$ |
| Case D | $1/50$ | $-1951/42480$ | $-0.0181217$ | $24599/51920$ | $0.4477272$ |

All other margins of (3) are positive in every row except D.
Every node has a unique pure equilibrium, with strict margins. Entry at the middle strength:

| Example | A | B | Paper (Laplace) |
|---|---:|---:|---:|
| Moderate, bands, benchmark | $37/68$ | $0.5227573$ | 0.526805, 0.522760, 0.522757 |
| Case A | $167/340$ | $0.4723390$ | 0.464564 |
| Cases B, C | $203/340$ | $0.5731756$ | 0.571808, 0.563404 |
| Case D | $1/4$ | $1/4$ | 0.250000 |

Case C ownership rises from $7/40$ to $96439/220320$ (A) or $0.4198197$ (B). The slot margin (6) is $8269/22032$ (A).
The C versus D distinction holds under both slots.

**Levels.** With full orders and recruitment only at $Q=+1$, entry is $\rho+(1-\rho)(b+\pi\lambda)$.
It does not depend on costs or strengths. One slot calibration cannot reproduce the paper's distinct Laplace levels. E1 states this correctly.

**C.4 sequence (computer-assisted).** E1 tests the paper's own Laplace-recipe costs, which contain $e$, under both slots.
I find the same: the first feasible member is $n=3$ for all five ratios. The B-valued costs at $n=3$ also lie inside A's windows.
With a slot-native recipe (no factor $1/2$ in $k$), the first feasible member is $n=2$ for ratios 1.05, 1.10, 1.25.
The table in E1 reports the B-valued costs; this is not stated there, but it is not an error.

### 3.4 Claim 3: more than two classes

**Reproduction (A analytical, B computer-assisted).** $R\sim U[0,8]$, $p=1$, $\rho=1/4$, $c_H=10$, $k=1/8$.
Quadrature gives $t_0=7/8$, $(t,g)=(1,0)$ at value 1 and $(65/16,95/16)$ at value 10.
No class profit reaches $c_H$, so entry is $1/4$ at every price. Orders $(-1,0,1)$:

| Flow | Posterior | $\bar t_Q$ | $\bar B_Q$ | Price |
|---|---|---:|---:|---:|
| $-1$ | $(29/62,11/31,11/62)$ | $63565/25296$ | $74195/25296$ | $129967/101184$ |
| $0$ | $(11/80,29/40,11/80)$ | $347/102$ | $475/102$ | $2459/1632$ |
| $+1$ | $(11/62,11/31,29/62)$ | $347/102$ | $475/102$ | $2459/1632$ |

The net payoffs equal E1's table. Each prescribed order is the strict best response. Under B the same holds with outward intervals.

**My closed form for the mixture weight.** Equal posterior means at flows 0 and $+1$ give, with $2b+b_0+\lambda=1$,

$$
w=\frac{2b+3b_0+2\lambda}{2(2b+b_0+\lambda)}=\frac{1+2b_0+\lambda}{2}.
$$

It gives $91/102$ under A and $0.9407083097495\ldots$ under B; it agrees with E1's (10a).
It lies in $(0,1)$ exactly when $\beta>1/4$. So this construction needs $\beta>1/4$; other constructions may cover smaller $\beta$.

**How serious is the failure?**

1. *What the price reveals (analytical).* Competitive pricing gives $P=t_0+e(P)(\bar t_Q-t_0)$ with $e\ge\rho$.
   So the price reveals $\bar t_Q$, the posterior mean of class proceeds. Two flows share a price only if their means agree.
2. *Knife-edge (analytical for pure order profiles).* For a fixed pure profile, a shared price is one polynomial equation in the primitives.
   It is not an identity when the posteriors differ: change the proceeds of a class whose weight differs across the two flows.
   So pooling occurs only on a lower-dimensional set of primitives.
   The program confirms it: at $w=91/102\pm1/1000$ the three prices differ, and the orders $(-1,0,1)$ stay strict.
   For mixed profiles, each mixing class adds one unknown and one indifference equation; pooling adds one more equation.
   I state the mixed case as a **conjecture**.
3. *Payoff relevance (analytical).* In E1's example, class 2 is a mixture of classes 1 and 3.
   Both $t_j$ and $g_j$ are affine in the mixture weight, so equal $\bar t$ forces equal $\bar B$ ($475/102$ at both flows).
   The pooled challenger acts exactly as it would after seeing the order.
   More generally: if two pooled flows would give the same entry decision, pooling changes nothing.
   If they would give different decisions, their separated prices differ, so the separated outcome is also a price-observation equilibrium.
4. *Cause (analytical).* Paper A.13 uses a monotone likelihood ratio in the order. The slot law has none.
   Under A, $f(+1\mid q)/f(0\mid q)=1,\ 11/29,\ 29/11$ for $q=-1,0,+1$. Under B: $0.717,\ 0.321,\ 1.950$.
   The paper itself says its many-class argument "uses the Laplace law".
5. *Order observation (analytical).* In the slot the order is the flow. A challenger who sees the order knows the flow posterior.
   The failure disappears. In every two-class economy, price and order observation coincide, because the price is strictly increasing in the posterior.

**Restricted two-group result (analytical; holds with change).** I re-derived E1's version.
Under forced group orders, flows reveal only the group, and within-group proportions stay at the prior.
One detail: the residuals use only the posteriors at $Q=\pm1$, so the bound $1+u$ suffices for every $\beta$. E1's $u_*$ for $\beta>1/3$ is conservative, not wrong.

### 3.5 Claim 4: access to prices

**General result (analytical).** Under (3), the hidden-price challenger stays at $\pi$, so entry is $\rho$.
The return bound still forces full orders, so the order law and the trading cost are the same in both regimes.
Access adds high-cost entry at $Q=+1$ only. This gives E1's (11).
The surplus term per added preparation is $B_1(M)-c_H+pF_1(p)>0$, by the paper's (A.39).

**Outside the region (analytical).** If $B_1(m)<c_H\le B_1(\pi)$, hidden entry is one at every flow.
Access removes high-cost entry at $Q=-1$. Proceeds fall by E1's (12).
Net surplus changes by $-(1-\rho)\Pr(Q=-1)[B_1(m)+pF_1(p)-c_H]$. It falls exactly when $B_1(m)+pF_1(p)>c_H$.
The paper's A.9 claims only the fall in proceeds. E1's surplus statement adds to it and is correct in its examples.

| Case | Proceeds gain | Net surplus gain | $B_1(m)+pF_1(p)-c_H$ |
|---|---:|---:|---:|
| A, $c_H=6$ | $113/408$ | $5/68$ | $-7/2$ |
| B, $c_H=6$ | $0.2579481359412$ | $0.0819603370846$ | $-3.5504882$ |
| A, $c_H=49/20$ | $-77/408$ | $-1/68$ | $1/20$ |
| B, $c_H=12/5$ | $-0.1739175847201$ | $-0.0135047169563$ | $0.0495118$ |

Both regimes have unique full orders in every case. The access levels are $485/544$ and $4285/1632$ under A.

**Not reported by E1: the Section 6.1 transfer (computer-assisted).** The informed investor's unconditional gross trading profit is $11/272$ (A) and $0.0376655$ (B).
Conditional on the investor filling the slot, it is $187/1632\approx0.1146$ (A) and $0.1121$ (B); the paper's investor is always present.
The transfer from liquidity traders is the unconditional figure. The proceeds gain exceeds this transfer at every trade scale below $226/33\approx6.85$ (A) and $6.8484$ (B). The paper's Laplace values are 0.140731 and 1.831923.
The qualitative sentence holds; its two numbers change.

### 3.6 Claim 5: the payment rule

Quadrature of $T_\eta=(1-\eta)\min\{R,\theta\}+\eta\max\{R,\theta\}$ gives:

| $r$ | $\Delta_\eta$ | $g_{H,\eta}$ | $g_{L,\eta}$ |
|---|---|---|---|
| $6/5$ | $1/60+(269/30)\eta$ | $(47/5)(1-\eta)$ | $(5/12)(1-\eta)$ |
| $3$ | $2/3+(23/3)\eta$ | $(17/2)(1-\eta)$ | $(1/6)(1-\eta)$ |

Both rows equal the paper's (14). The difference is $(13/20)(1-2\eta)$, zero at $\eta=1/2$.
The slot does not enter these objects. **Analytical.**

### 3.7 Claim 6: reserve comparisons

**The paper's reserves (A analytical, B computer-assisted).** Prior one half, $c_H=6$, $k=1/50$.

| Values | $r$ | $p$ | Orders | Entry A | Entry B | Proceeds A | Proceeds B |
|---|---:|---:|---|---:|---:|---:|---:|
| Points | 1.2 | 0.5 | $(0,0)$ | $1/4$ | $1/4$ | $377/960$ | 0.3927083 |
| Points | 1.2 | 1.01 | $(1,-1)$ | $37/68$ | 0.5227573 | 0.4525325 | 0.4405646 |
| Points | 3 | 0.5 | $(1,-1)$ | $37/68$ | 0.5227573 | $485/544$ | 0.8725315 |
| Points | 3 | 1.01 | $(1,-1)$ | $37/68$ | 0.5227573 | 1.0082189 | 0.9943844 |
| Bands | 1.2 | 1.1 | $(1,-1)$ | $37/68$ | 0.5227573 | $1417/3264$ | 0.4201232 |
| Bands | 3 | 1.1 | $(1,-1)$ | $37/68$ | 0.5227573 | $42293/40800$ | 1.0226902 |

Sale and two-bidder probabilities match E1's table to all printed digits.
The narrowest recruiting node is bands, $p=1.1$, $r=3$: $B_1(M)-c_H=391/24000$ (A), $0.0665678$ (B).
Entry is flat because both strengths recruit at $Q=+1$ only. Proceeds rise in both economies, as in the paper.

**Alternative reserve $p=31/20$.** Entry $37/68\to1/4$ (A) and $\mathsf E_*\to1/4$ (B).
Proceeds $713/1360\to17147/19200$ (A); $0.5028224\to0.8930729$ (B). All exceed the $p=1/2$ levels.

**The exclusion is forced (A analytical, B computer-assisted).**

- At $r=3$ with the low class excluded and no high-cost entry, proceeds are $R_s(p)=\tfrac78(p-p^2/3)+\tfrac18(3/2+p^2/6)$.
  $R_s$ rises on $(1,21/13)$, so $R_s(p)\le R_s(6/5)=339/400$ for $p\le6/5$.
- Under A, strict deterrence needs $p>p_H=\sqrt{39/29}=1.1597$. On $(p_H,6/5)$ deterrence holds with the weak incumbent admissible.
  But strong proceeds are at most $339/400<485/544$, the $p=1/2$ level. So deterrence plus higher proceeds needs $p>6/5$.
- Under B, strict deterrence needs $p>p_H=1.3252698>6/5$. The weak incumbent is excluded at every deterrence reserve.
- Grid scan (numerical diagnostic, exact rationals): $M$ over the benchmark band $0.706$–$0.731$, every $b$ with $\beta\le1/2$, $p\in(1,6/5)$ in steps of $1/200$.
  Of 56472 triples, 38883 give deterrence and 6773 give higher proceeds in both economies. None gives all three.
- The scan uses point masses. The bands give the same objects for $p\ge1.05$: the low band is fully excluded, and the high band lies above both strengths.
  I did not scan bands for $p\in(1,1.05)$.

So no slot calibration in the benchmark band reproduces the paper's full X7 pattern with the weak incumbent admissible (on this grid).
E1's choice $p=1.55$ is therefore close to the only kind of repair.

**Exact events.** $p_H^2=39/29$ (A) and $1.7563401$ (B), as E1 states.
At $p=h=10$, $r=3$: unique full orders, entry $1/4$, sale $1/8$, two bidders 0, proceeds $5/4$, under both slots.

## 4. Errors and corrections

No numerical error was found. Every E1 number I tested matches my program to all printed digits.
E1's program reruns byte-identically. The points below are clarifications, sharpenings, and one omission.

1. **Wording (claim 1).** The omitted inequality is part of the paper's (A1). The correction restores the paper's hypothesis; it is not new.
2. **Sharpening (claim 1).** The paper's sufficient ownership sentence fails for slots with $b+\lambda<1/2$.
   §3.2 gives an exact example in which ownership falls. For A and B the sentence holds. A slot main text should state (6).
3. **Clarification (claim 2).** E1's C.4 table shows the paper's Laplace-recipe costs. A slot-native recipe admits $n=2$ for small ratios.
4. **Scope (claim 3).** E1's construction needs $\beta>1/4$. The two-group bound needs only $u$ for every $\beta$.
   E1's label "fails" is literally correct; §3.4 shows the failure is a knife-edge without effect on entry in the example.
5. **Omission (claim 4).** E1 does not recompute the Section 6.1 transfer. The break-even trade scale becomes about 6.85, not 1.83.
6. **Sharpening (claim 6).** The weak-incumbent exclusion at $p=1.55$ is forced, not only E1's choice (§3.7).

## 5. Judgment on the rule "every extension holds"

**Literal answer: the slot does not pass.** Two statements in E1's scope fail as written:

- the many-class sentence "the price still reveals the whole posterior over classes" (Section 5.2 and Online Appendix A.13);
- the X7 preparation comparison at the paper's reserve: entry is flat, not falling, so Section 5.2's "reports deterrence at such a reserve" fails.

A third change is smaller: the ownership sufficient condition needs $b+\lambda>1/2$. A and B satisfy it.

**Substance: neither failure is material for the paper.**

- *Many classes.* The failure is a knife-edge of codimension one. In E1's example it does not change entry.
  It disappears if the challenger sees the order. The extension that matters, the two-group reversal, holds.
  The paper already ties the many-class step to the Laplace law. A text change suffices:
  "the price reveals the posterior mean of class proceeds, and the whole posterior except at non-generic ties."
  I would keep price observation, because the paper's question is what prices reveal.
- *Reserves.* Section 6.3 is an illustration; the seller-optimal reserve is open in the paper.
  The two headline facts hold: exclusion supports informative trading against a weak incumbent, and proceeds rise in both economies.
  Only the strict fall in entry is lost. A text change suffices: "entry does not rise" in place of "deterrence".

**The pattern behind both changes.** With fixed full orders, slot entry takes at most four values.
The challenger recruits after no flow, after $+1$, after $\{0,+1\}$, or after every flow.
So any paper statement that entry moves strictly with strength or reserve at fixed orders becomes flat.
This produced the X7 change here and the failed upward triple of Proposition 3 in `memos/X_check.md`.
The same feature may affect E2's X1 and X3; I have not checked them. This feature is a real cost of the slot.
It is a larger cost than the many-class knife-edge.

**Recommendation.** If the author applies the rule literally, Laplace stays in the main text.
If the author applies it to substance, E1's scope does not block the slot. Two sentences need rewording, and the ownership condition needs the slot form (6).
The decision should also weigh E2's results and the flat-entry pattern above.

## 6. Plain summary

I rechecked E1 with my own derivations and a new exact program. E1's program reruns identically, and every number I tested agrees.

- The coordinator's general-prior proposition dropped a condition that the paper itself states. E1's counterexample and corrected statement are right.
- The two-class reversal holds for any class pair and prior. All paper examples work with the paper's costs and strengths.
- The three-class example is a valid equilibrium. Two different posteriors share one price. This is a knife-edge: a small change separates the prices. The pooling does not change entry, and order observation removes it.
- Access to prices raises proceeds and surplus in the recruiting region. Outside it, both can fall.
- The payment-rule result does not depend on the trading stage.
- At the paper's exclusion reserve, slot entry is flat across strengths. A reserve of 1.55 restores the fall in entry, but it excludes the weak incumbent. That exclusion is forced.

Literally, the slot fails the rule "every extension holds". In substance, the failures are minor and need only text changes. The larger cost is that slot entry moves in steps, so strict entry comparisons become flat.
