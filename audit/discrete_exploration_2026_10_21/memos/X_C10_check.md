# X_C10 check: C10 target disclosure and a challenger toehold

Checker workstream X_C10, 21 October 2026.
Scripts: `scripts/X_C10_check/check_c10.py`.
Printed output: `scripts/X_C10_check/output_check_c10.txt`.

## 1. Scope

This memo checks Results D1 to D6 and T1 to T3 in `C10_other.md`.
It does not explore new variants.

The base case is fixed throughout the check.

- Discrete-Laplace noise, buy-only orders and $c_L=0$.
- $h=10$, $\ell=1$, $p=1/2$ and $\rho=1/4$.
- $b=2$, $k=0.02$ and $c_H=5$, unless a result states other values.
- Prior $\pi=1/2$, unless a result states a general branch prior $\varphi$.

The checker wrote `check_c10.py` from the model definitions.
The script uses 50-digit arithmetic.
One part uses exact fractions at the surrogate value $a=3/5$.
One part uses interval arithmetic at $a=e^{-1/2}$ and $r=3$.

The checker obtained the numbers in Sections 3.1 to 3.9 first.
The checker then read the C10 scripts and saved outputs.
Section 3.10 reports that comparison.
Two comparison logs sit in `scripts/X_C10_check/`.

The shared auction formulas match the paper at the pinned commit.
In particular, $t_0$, $t_H$, $t_L$, $g_H$, $g_L$ and $\Delta_T$ match.
The paper also gives $g_H'<0$, $g_L'<0$ and $\Delta_T'>0$ for $r>\ell$.

The disclosure timing in C10 is clear.
The target commits first.
All players then see the public signal.
The investor also sees the class and trades.
Market makers condition on the signal and on the flow.
The challenger then sees the signal, the price and its cost.
This timing fits a branch-prior formulation.

## 2. Verdict table

| Claim | Verdict | Short evidence |
|---|---|---|
| D1. Trading stage at any prior | CONFIRMED | Direct sum and closed form for $\bar G_1$ differ by at most $2\times10^{-51}$ at four priors. Profile and pure-equilibrium conditions re-derive cleanly. |
| D2. Piecewise linearity and concavification | CONFIRMED WITH CORRECTION | Linearity is exact. Concavification needs a fixed selection, an existence domain, and care at one-sided cell edges. |
| D3. Optimal test | CONFIRMED WITH CORRECTION | Support-line proof and benchmark numbers confirm. At $r=3$, $\varphi^*=0.699167$, entry $0.786353$, ownership $0.5$. The computer-assisted label and the gap wording need correction. |
| D4. Symmetric signals | CONFIRMED WITH CORRECTION | Exact fractions confirm the valley formulas. The result needs an explicit full-buying selection and branch existence scope. |
| D5. Competition and disclosure | CONFIRMED WITH CORRECTION | The $\varphi_3$ regime, benchmark pairs and ceilings confirm. Global entry monotonicity fails at the switch near $r=1.413$. |
| D6. Trade after disclosure | CONFIRMED | $k_{\max}=0.190337$ at $\varphi^*$ and $0.195836$ at $1/2$ for $r=3$. Table B, Table C and the $k$ ranges reproduce. |
| T1. Public toehold | CONFIRMED WITH CORRECTION | All fixed-bid formulas and numbers reproduce. Fixed truthful bids are a material partial-equilibrium restriction, in particular at large $s$. |
| T2. Fair-price toehold purchase | CONFIRMED WITH CORRECTION | The payoff identity holds with a fixed trading experiment, fixed bids, and a publicly anticipated size. The printed proof does not state those limits. |
| T3. Hidden unit | CONFIRMED WITH CORRECTION | The pure equilibrium and benchmark numbers reproduce, with the class-L investor check added. Scope and one grid extreme need clearer definitions. |

No headline claim receives a full REFUTED verdict.
One subclaim inside D5 does fail.
Entry under the stated $\varphi^*$ rule does not fall at every $r$.

## 3. Derivations and evidence

### 3.1 D1: the trading stage at a branch prior

Fix $\varphi$ and put $\omega=\varphi/(1-\varphi)$.
Write $w_L=t_L-t_0$.
At flow $x$, competitive pricing gives
$P=t_0+e_x(w_L+\Delta_T\mu_x)$.
Entry depends on the price and on cost.
Cost is independent of class.
Hence $\mathbb E[V_T\mid j,x]=t_0+e_x(t_j-t_0)$.
Subtraction gives the two stated residuals.

- Class H: $e_x\Delta_T(1-\mu_x)$.
- Class L: $-e_x\Delta_T\mu_x$.

Each class-L term is at most zero for every deviation flow.
The class-L investor therefore never buys one unit at cost $k>0$.

If class H buys with probability $\beta$, the likelihood ratio is
$(1-\beta)+\beta/a$ for $x\ge1$.
It is $(1-\beta)+\beta a$ for $x\le0$.
At $\beta=1$, posterior odds are $\omega/a$ after good flow.
Posterior odds are $\omega a$ after bad flow.
With $T=\tau/(1-\tau)$, the entry profile follows at once.
Challenger preparation at a tie gives the stated weak inequalities.

Under no trade, one unit earns $e(\varphi)\Delta_T(1-\varphi)-k$.
The investor tie rule gives existence exactly under $\bar G_0\le k$.

Under full buying, $Z\ge0$ has probability $1/(1+a)$.
Also $Z\le-1$ has probability $a/(1+a)$.
The two posterior complements are

$$
1-\mu_g=\frac{a(1-\varphi)}{a+(1-a)\varphi},
\qquad
1-\mu_b=\frac{1-\varphi}{1-(1-a)\varphi}.
$$

Substitution gives the stated $\bar G_1$ formula.
The investor tie rule gives existence exactly under $\bar G_1>k$.

The derivative signs in item 6 are correct.
For $(e_g,e_b)=(1,1)$, each reciprocal term is convex in $\varphi$.
The ratio $F$ equals 1 at both endpoints.
A convex function lies at or below its endpoint chord.
Hence $\bar G_1(\varphi;1,1)\le\Delta_T(1-\varphi)$.
Smaller entry levels only reduce the left side.

At $r=3$, the checker compared a direct $Z$ sum with the closed form.
The tail bound after $|Z|\le300$ is $5.4\times10^{-66}$.

| $\varphi$ | Profile | Closed form minus direct sum |
|---|---|---|
| 0.2 | $(\rho,\rho)$ | $1.0\times10^{-51}$ |
| 0.5 | $(1,\rho)$ | $1.7\times10^{-51}$ |
| 0.65 | $(1,\rho)$ | $-3.3\times10^{-52}$ |
| 0.8 | $(1,1)$ | $3.3\times10^{-52}$ |

The analytical label is deserved for the stated pure-action items.
D1 does not characterise interior $\beta$ equilibria.
That omission matters in D2 and D3, not in the D1 formulas.

One proof detail needs a text fix.
The steps in C10 shift by one item after Step 1.
The algebra still covers each item.
The price-to-posterior step also uses $w_L>0$ and $e\ge\rho>0$.
Those facts make $P_r(\mu)$ strictly increasing in $\mu$.

### 3.2 D2: linearity, selection, gaps and cell edges

Under full buying, the region probabilities are linear in $\varphi$.
For example,
$\Pr(g)=[\varphi+a(1-\varphi)]/(1+a)$.
Also $\Pr(g,H)=\varphi/(1+a)$.
Hence $E$, $O_H$ and $\Phi=w_LE+\Delta_TO_H$ are linear.
This holds inside one entry profile and one equilibrium label.
Under no trade, $\Phi=e(w_L+\Delta_T\varphi)$ is also linear.
The linearity claim is exact.

Concavification needs more structure than one symbol $\Phi(\varphi)$.
The branch payoff must first attach one continuation value to $\varphi$.
That value already includes trading and entry at public prior $\varphi$.
C10 has the right timing for this object.
The object is still not a single function on all of $[0,1]$.

- At some priors, no trade and full buying both exist.
- At some priors, neither pure equilibrium exists.
- At a root $\bar G_1=k$, full buying fails under the strict tie rule.

The checker used a 2,001-point prior grid for a first map.
Intervals below are grid ranges, not exact endpoints.

| $r$ | $\varphi^*$ | No pure equilibrium | Both pure equilibria |
|---|---|---|---|
| 1.2 | 0.521800 | none found | none found |
| 1.4 | 0.650000 | $[0.5295,0.6495]$ | $[0.4055,0.4190]$ |
| 1.5 | 0.652723 | $[0.0325,0.0400]$, $[0.5825,0.6525]$, $[0.7485,0.7600]$ | $[0.4090,0.5325]$ |
| 1.6 | 0.655910 | $[0.2545,0.2885]$, $[0.8155,0.8220]$ | $[0.4125,0.5360]$ |
| 1.8 | 0.662169 | $[0.8850,0.8875]$ | none found |
| 3.0 | 0.699167 | none found on this grid | none found |

At $r=3$, a root calculation finds the thin gap that the grid misses.
Full buying with $(1,1)$ fails after $\varphi=0.969776$.
No trade with $e=1$ starts at $\varphi_{NT}=0.97$.
The gap width is $0.000224$.
At $r=1.8$, the same calculation gives width $0.002932$.
These values match C10 Section 6 after rounding.

Under the stated tie rule, a gap branch has no pure continuation.
A policy with weight on a gap prior has no stated payoff.
The feasible pure-policy set must therefore exclude gap support.
A mixed-investor extension would need a new tie convention.
It would also need a value for each mixed continuation.

The C10 hull calculation skips gap cells.
It also uses linear values at both sides of each cell edge.
That method computes a closure object at jump points.
A one-sided limit at $\bar G_1=k$ need not be an attained branch value.
The concave envelope statement must name this closure issue.
It must also name the selection rule on coexistence priors.

D3 repairs the main optimum despite this D2 gap.
Its support line bounds every pure branch value.
Its two support points attain the line.
The D2 text alone does not supply that repair.

### 3.3 D3: optimal disclosure

The support-line proof is sound after its hypotheses are made explicit.
The needed domain facts are $0<\tau<1$, $w_L>0$ and $\Delta_T>0$.
The needed length condition is $\pi\le\varphi^*<1$.
Condition (C) must also hold.

At $\varphi=0$, entry is $\rho$ and $\Phi=\rho w_L$.
At $\varphi^*$, every pure equilibrium has full entry.
The case proof for that point is correct.

- If $\varphi^*=\varphi_3$, full buying gives profile $(1,1)$.
- No trade at the same point gives $e=1$, since $\varphi_3\ge\tau$.
- If $\varphi^*=\varphi_{NT}$, then $\Delta_T(1-\varphi^*)\le k$.
- D1 item 6 then rules out full buying in every profile.
- No trade exists at $\varphi_{NT}$ and gives $e=1$.

Thus selection among pure equilibria does not change $\Phi(\varphi^*)$.
Selection can still change values at other priors.
It can change the no-disclosure baseline in a coexistence range.

For $\varphi\ge\varphi^*$, the bound
$\Phi\le w_L+\Delta_T\varphi\le\ell(\varphi)$ is correct.
It uses $E\le1$, $O_H\le\varphi$ and $w_L>0$.
The same bound covers a future mixed continuation in that range.
That point matters at $r=3$, since the thin gap lies above $\varphi^*$.

For $\varphi<\varphi^*$, the no-trade step is correct.
A no-trade branch with $e=1$ needs
$\varphi\ge\max\{\tau,1-k/\Delta_T\}$.
That lower bound is at least $\varphi^*$.
Hence only $e=\rho$ can occur below $\varphi^*$ under no trade.

The $(1,\rho)$ step is also correct.
If $\varphi_{FB}$ is finite, then $\varphi^*\le\varphi_3$.
Profile $(1,1)$ cannot occur below $\varphi^*$.
If $\varphi_{FB}$ is infinite, monotonicity rules out $(1,1)$ buying.
Condition (C) and linearity then give the bound on $[\varphi_1,\varphi^*)$.

The policy formulas follow from mean $\pi$.
The pass branch has weight $w=\pi/\varphi^*$.
Entry is $\rho+(1-\rho)w$.
High-class ownership is $w\varphi^*=\pi$.
The class-L pass fraction is $\pi(1-\varphi^*)/[\varphi^*(1-\pi)]$.

Benchmark values reproduce closely.

| $r$ | $\varphi^*$ | Pass weight | $E^*$ | Baseline $E$ | $O_H^*$ | $\Phi^*$ |
|---|---|---|---|---|---|---|
| 1.2 | 0.521800 | 0.958222 | 0.968667 | 0.250 | 0.5 | 0.391764 |
| 3.0 | 0.699167 | 0.715137 | 0.786353 | 0.625 | 0.5 | 0.693745 |
| 3.6 | 0.718320 | 0.696069 | 0.772051 | 0.625 | 0.5 | 0.828663 |
| 4.2 | 0.738275 | 0.677254 | 0.757940 | 0.250 | 0.5 | 0.965936 |

At $r=3$, baseline ownership is $0.358422$.
Hence entry $0.625\to0.786$ and ownership $0.358\to0.5$ confirm.

Condition (C) also reproduces on the stated $r$ grid.

- The smallest margin is $0.051774$ at $r=1.4$.
- The margin at $r=3$ is $0.145034$.
- A finer $0.01$ scan finds minimum $0.048074$ at $r=1.41$.

At $a=3/5$ and $r=3$, exact fractions match C10.

- Condition (C) margin: $17427/122560=0.142192$.
- Full-buying slack: $10313/61200=0.168513$.
- Largest $\Phi-\ell$ on 1,001 rational priors: $0$.

That exact case checks algebra for a surrogate noise ratio.
It does not by itself certify $a=e^{-1/2}$.

The checker ran interval arithmetic at the true $a$ and $r=3$.
The interval for the (C) margin is
$[0.1450335540770219,\,0.1450335540770263]$.
This certifies the benchmark inequality at $r=3$.
C10 itself reports 60-digit values and bisection roots.
Under the team label rule, that evidence is not yet computer-assisted.
The conditional theorem is analytical once (C) is given.
The grid application in C10 is a numerical diagnostic.

The gap qualification needs one wording change.
Under the stated investor tie rule, mixed buying at exact indifference is excluded.
The D3 policy is then exact among policies with pure continuations.
It is not merely a lower bound inside that same game.
A different game that permits mixing at ties may give a larger value.
C10 does not solve that different game on $r\in[1.4,1.6]$.

A root scan for a mixed $\beta$ does not settle the extension.
The gain $G(\beta)$ can jump where a posterior crosses $\tau$.
A sign change across a jump need not contain a zero.
The thin $(1,1)$ gap has no such jump in profile.
Continuity gives a zero there.
The lower gaps need a cell-by-cell argument.

### 3.4 D4: symmetric signals

Let $d_1=1-\varphi_1$ and $d_2=\varphi_3$.
The stated order proof is correct.
Indeed $d_1<d_2$ reduces to $a<aT^2$, hence to $T>1$.

The three profile ranges are also correct.

- At $d\le d_1$, both branches lie in profile $(1,\rho)$.
- At $d_1<d<d_2$, the low branch has profile $(\rho,\rho)$.
- At the same $d$, the high branch has profile $(1,\rho)$.
- At $d\ge d_2$, the high branch has profile $(1,1)$.
- The low branch then stays in profile $(\rho,\rho)$.

The challenger tie rule gives the stated endpoint cases.
Linearity gives the neutral zone.
The valley and recovery algebra checks symbol by symbol.

At $a=3/5$ and $r=3$, exact values are:

| $d$ | Entry | Ownership difference from $d=1/2$ |
|---|---|---|
| 0.55 | $283/640=0.442188$ | $-27/256$ |
| 0.60 | $143/320=0.446875$ | $-3/32$ |
| 0.65 | $289/640=0.451563$ | $-21/256$ |
| 0.70 | $73/160=0.456250$ | $-9/128$ |
| 0.75 | $5/8=0.625$ | $3/64$ |

At the true $a=e^{-1/2}$ and $r=3$, $d_1=0.539087$.
Also $d_2=0.699167$.
Entry at $d=0.55$ is $0.442092$.
Entry at $d=0.65$ is $0.451277$.
These values match Table D.

The correction concerns equilibrium selection and existence.
D4 assumes full buying in each branch.
Assumption of existence does not select full buying under coexistence.
It also excludes a branch prior in a pure-equilibrium gap.
The result should therefore name the full-buying selection.

At benchmark $r=3$, the checker finds no second pure equilibrium.
This holds at the valley branch priors for $d=0.55$, $0.60$ and $0.65$.
In the recovery range, the two labels can give the same outcomes.
The high branch gives entry 1 under $(1,1)$ buying or no trade.
The low branch gives entry $\rho$ under $(\rho,\rho)$ buying or no trade.
Thus Table D survives at the listed benchmark values.

One endpoint still needs care.
A high branch near $\varphi=0.9698$ at $r=3$ lies in the thin gap.
D4 and D5(ii) should exclude such a signal accuracy.
They should also state the rule for $d$ near 1.
Full buying eventually fails as $1-\varphi\to0$.
No trade then gives the same high-branch entry and ownership.

### 3.5 D5: competition, disclosure and ceilings

The derivative proof for $\tau_r$ is correct on its stated domain.
It needs $g_L<c_H<g_H$ and $g_H>g_L$.
The paper gives $g_L'<0$ and $g_H'<0$ for $r>p$.
The numerator formula in C10 follows without a sign error.
For $r>\ell$, $\Delta_T$ also rises.
Hence $T_r$, $\varphi_3(r)$ and $1-k/\Delta_T(r)$ rise.

Where $\varphi^*=\varphi_3$ at both strengths, the spread claim follows.
The two-point laws have the same mean $\pi$.
The law with the larger $\varphi^*$ is a mean-preserving spread.
Its pass weight $\pi/\varphi^*$ is smaller.
Entry $E^*=\rho+(1-\rho)\pi/\varphi^*$ is therefore smaller.

The global monotonicity claim fails at the regime switch.
The checker finds one fall in $\varphi^*$ on a $0.01$ scan.
The fall sits between $r=1.41$ and $r=1.42$.

| $r$ | $\varphi_{NT}$ | $\varphi_3$ | $\bar G_1(\varphi_3;1,1)-k$ | $\varphi^*$ | $E^*$ |
|---|---|---|---|---|---|
| 1.40 | 0.650000 | 0.649478 | $-0.001070$ | 0.650000 | 0.826923 |
| 1.41 | 0.664485 | 0.649806 | $-0.000271$ | 0.664485 | 0.814346 |
| 1.42 | 0.678005 | 0.650132 | $0.000539$ | 0.650132 | 0.826806 |
| 1.43 | 0.690644 | 0.650458 | $0.001358$ | 0.650458 | 0.826516 |

The switch root solves $\bar G_1(\varphi_3(r);1,1)=k$.
Bisection gives $r=1.413360$.
Just left of the root, $\varphi^*=\varphi_{NT}$.
Just right of the root, $\varphi^*=\varphi_3$.
The pass posterior jumps down at the root.
Entry jumps up at the root.

This point does not overturn the benchmark pair comparison.
Entry under the optimal rule is $0.968667$ at $r_0=1.2$.
Entry is $0.786353$ at $r_1=3$.
The reversal still fails between those two strengths under the rule.
The coarse grid sequence in C10 also reproduces.
It is $0.969$, $0.827$, $0.822$ and $0.816$ at $r=1.2,1.4,1.6,1.8$.
The unqualified sentence that entry falls in $r$ is false.

The gap status near the switch adds a second qualifier.
At $r$ near $1.41$, some priors below $\varphi^*$ have no pure equilibrium.
The switch calculation uses the pure-equilibrium $\varphi^*$ rule in C10.
A mixed-extension optimum could differ in this local range.
The correction still stands against the formula as printed.

The fixed-signal claim D5(ii) holds at the benchmark values.
It uses $\Delta_T(1.2)=0.016667<k$ and $\tau_{1.2}=0.521800$.
It also uses $\varphi_3(3)=0.699167$.
Those benchmark facts should appear as hypotheses.
A signal with a branch in a pure-equilibrium gap needs exclusion.

The valley reversal D5(iii) reproduces.
At $d=0.55$, entry is $0.625$ at $r=1.2$ and $0.442092$ at $r=3$.
At $d=0.65$, entry is $0.625$ and $0.451277$ at those strengths.

The value-of-disclosure numbers D5(iv) reproduce.

- Gain $0.290722$ at $r=1.2$.
- Gain $0.105319$ at $r=1.75$.
- Gain $0.168338$ at $r=3$.
- Gain $0.201346$ at $r=3.6$.
- Gain $0.662170$ at $r=4.0$.

The baseline at these points uses full buying when it exists.
At $r=1.5$, the saved C10 output gives two baseline values.
Selection therefore matters for a fuller U-shape claim near that range.
The listed points remain correct as a numerical diagnostic.

Both ceilings reproduce.

- Market ceiling: $B_r(M_1)=5$ at $r=3.986097$.
- Disclosure ceiling: $g_H(r)=5$ at $r=9.974937$.
- Closed form: $(10+\sqrt{99})/2=9.974937$.

Full disclosure alone proves recruitment up to the second ceiling.
At branch prior 1, full entry needs exactly $g_H\ge c_H$.
This part does not need the full D3 optimality proof.
Section 4 should say the ceiling moves out, not that it is removed.

### 3.6 D6: trade after disclosure

At $r=3$, the pooled branch has $\varphi^*=0.699167$.
No trade gives gross gain $\Delta_T(1-\varphi^*)=0.200556$.
Hence no trade fails for each $k<0.190337$.
Full buying is then the unique pure equilibrium in that range.
The investor still trades, and both flows give entry 1.
The interpretation in C10 is correct at the benchmark.

Gross gains reproduce in Table B order.

| $r$ | At $\varphi^*$ | At prior $1/2$ |
|---|---|---|
| 3.0 | 0.190337 | 0.195836 |
| 3.6 | 0.251478 | 0.275803 |
| 4.2 | 0.304058 | 0.143240 |
| 5.0 | 0.357429 | 0.188003 |
| 7.0 | 0.382747 | 0.302148 |

At $r=3$, a no-market pool at $\tau$ gives pass weight $0.854701$.
Entry under that counterfactual is $0.891026$.
With the market, pass weight is $0.715137$ and entry is $0.786353$.
A short support-line proof also works in the no-market case.
It uses the chord from $(0,\rho w_L)$ to $(\tau,w_L+\Delta_T\tau)$.
C10 should add that proof or cite the same argument as D3.

The three $k$ ranges at $r=3$ reproduce.
Thresholds are $0.190337$ and $\Delta_T(1-\tau)=0.276667$.
At $k=0.2$, $\varphi^*=0.7$.
At $k=0.3$, $\varphi^*=\tau=0.585$.
The checker also finds positive (C) margins at $k=0.2$, $0.25$ and $0.3$.
The margins are $0.144764$, $0.171925$ and $0.189258$.

Sensitivity values reproduce to the printed digits.
Examples are $E^*=0.720174$ at $c_H=6$ and $0.832181$ at $b=4$.
At those values, the market-only branch gives entry $\rho$.
The numerical diagnostic label is deserved.

### 3.7 T1: public toehold with bids held fixed

The $B^s_r(\mu)$ derivation is correct under its fixed-schedule premise.
With entry, the challenger receives the bidder gain plus $s t_j$.
Without entry, the stake receives $s t_0$.
Expectation over $j$ at belief $\mu$ gives
$s(w_L+\Delta_T\mu)$.
Hence $B^s_r(\mu)=B_r(\mu)+s(w_L+\Delta_T\mu)$.

The deterrence derivative formula also checks.
Use $g_L'=-t_L'$, $g_H'=-t_H'$ and $t_H'=t_L'+\Delta_T'$.
Then
$\partial_rB^s_r=-(1-s)t_L'-st_0'-(1-s)\mu\Delta_T'$.
All three derivatives $t_L'$, $t_0'$ and $\Delta_T'$ are positive.
They are positive on the benchmark range $r>\ell$.
The sign result is therefore analytical, not only a grid fact.

Window widths reproduce.

| $s$ | Width | Ceiling $r_C(s)$ |
|---|---|---|
| 0 | 0.507994 | 3.986097 |
| 0.1 | 0.554908 | 4.395090 |
| 0.2 | 0.601822 | 4.902752 |
| 0.3 | 0.648736 | 5.551285 |
| 0.5 | 0.742564 | 7.608424 |
| 1 | 0.977134 | none below $h$ |

The stated break point also reproduces:
$s^*=0.484536$.
At $r=4.2$, $B^{0.1}(M_1)=5.055517$ and entry returns to $0.625$.

Two side conditions complete the benchmark window claim.
First, the bad posterior must not recruit at $r_1$.
At $r=3$, $\tau^s$ is $0.585$ at $s=0$ and $0.490741$ at $s=1$.
Both values exceed $m_1=0.377541$.
Second, the investor conditions must retain no trade and full buying.
At $r_0$, $\Delta_T<k$ gives no trade for every entry profile.
At $r_1$, profile $(1,\rho)$ leaves the baseline investor gain unchanged.
C10 should state these checks beside the two window inequalities.

At $s=0.5$, $B^s_{r_0}(1/2)=5.00625$.
Thus benchmark $c_H=5$ is outside the admissible window at that stake.
The reported width then concerns other hypothetical values of $c_H$.
That point is consistent with the break at $s\ge s^*$.

The disclosure interaction also reproduces under the same fixed schedules.
At $r=3$, $\varphi^*$ is $0.699167$, $0.681640$, $0.655766$ and $0.613716$.
The values correspond to $s=0$, $0.2$, $0.5$ and $1$.
The checker finds positive $C_s$ margins at those four stakes.
The margins are $0.145034$, $0.138499$, $0.129304$ and $0.115409$.
This supports the numerical entries in T1 item 6.
It does not supply a general proof across $s$ or $r$.

Truthful bids are a defensible partial step.
They isolate the stake payoff from the auction response.
They are not defensible as a full equilibrium at large $s$.

The low type has a direct gain from a higher losing price.
It receives $s$ times that price when the incumbent wins.
For a bid $b\in[p,r]$, expected proceeds are
$t(b)=b-b^2/(2r)+p^2/(2r)$.
The stated interior bid is $b^*=(\ell+sr)/(1+s)$.
That bid raises $t_L$ and lowers $\Delta_T=t_H-t_L$.
It also raises the low type entry gain relative to the fixed-bid formula.

At $r=3$, the magnitudes are material.

| $s$ | $b^*$ | $\Delta_T$ with $b^*$ | Fixed-bid $\Delta_T$ | Extra low-type gain |
|---|---|---|---|---|
| 0.1 | 1.181818 | 0.550964 | 0.666667 | 0.006061 |
| 0.5 | 1.666667 | 0.296296 | 0.666667 | 0.111111 |
| 1 | 2.000000 | 0.166667 | 0.666667 | 0.333333 |

The investor gain scales with the target payoff spread.
A smaller spread can therefore weaken or remove informed buying.
The slope of the entry gain in $\mu$ also changes.
Ceilings, window widths and $s^*$ can all move after bid adjustment.
The direction of the net entry effect needs a new auction calculation.
It does not follow from the fixed-bid table.

The simplification is least harmful near $s=0$.
Bid adjustment has only a second-order effect on bidder payoff at $s=0$.
The spread effect on the investor is still first order in $s$.
At $s=0.1$ and $r=3$, the spread already falls by about $17\%$.
T1 should therefore carry the fixed-schedule qualifier in its statement.
Its large-stake numbers should read as partial-equilibrium values.

### 3.8 T2: purchase at a fair public price

The central identity is correct inside a fixed continuation.
Let $V_T$ denote realised target proceeds.
Total expected payoff from stake $s$ can split into two parts.
One part is expected entry surplus.
The other part is $s(V_T-P_0(s))$.
A fair conditional price makes the second part zero in expectation.
The remaining part is $\mathbb E[e^s(B_r(\mu)-C)]$ before preparation.
The pointwise entry rule without a stake maximises that part.
This proof uses conditional expected gains at the price.
C10 writes realised $g_j$ and $t_j$ at that step.
The notation should switch to the conditional objects.

Three scope conditions are missing from the printed proof.

1. The trading experiment stays fixed as $s$ changes.
2. Auction gains $g_j$ and proceeds $t_j$ stay fixed as $s$ changes.
3. The purchase size $s$ is public or otherwise priced in $P_0(s)$.

The first condition matters in the full model.
Entry under $s$ enters the investor gain.
The investor response can change posterior informativeness.
A rule from the $s=0$ experiment need not dominate rules under a new experiment.
The phrase "over all rules that use the price" hides that change.

The second condition excludes the bid response in Section 3.7.
The third condition excludes a private size choice at an average price.
Purchase trading costs would only reduce the stake value further.

At the benchmark full-buying experiment, the identity gives the stated result.
The entry profile stays $(1,\rho)$ for the stated small stakes at $r=3$.
The correct label is analytical under the three scope conditions.

### 3.9 T3: hidden unit

The checker used three total-flow regions:
$\{x\le0\}$, $\{x=1\}$ and $\{x\ge2\}$.
For total shifts 0, 1 and 2, likelihood ratios are constant on each region.
Region probabilities use closed geometric tails.
No flow truncation enters the calculation.

The checker priced each region from latent class and cost states.
Entry uses the cleaned flow $Z+q_I$.
The high-cost challenger removes its own unit from that flow.
The low-cost challenger always enters after its trade decision.
Deviation gains hold the candidate price schedule fixed.

The checker also computed the class-L investor deviation.
C10 writes only one investor variable $\beta$.
Its script does compute a class-L gain.
The memo text should state that class-L no-buying is checked, not assumed.

Pure equilibria in the eight profiles reproduce exactly.

| $r$ | Equilibrium $(\beta,\sigma_L,\sigma_H)$ | Investor H net | Investor L net | Low-cost trade net | High-cost trade net |
|---|---|---|---|---|---|
| 1.2 | $(0,1,0)$ | $-0.034561$ | $-0.038727$ | 0.269280 | $-0.134887$ |
| 3.0 | $(1,1,0)$ | 0.178787 | $-0.299110$ | 0.135022 | $-0.219992$ |
| 3.6 | $(1,1,0)$ | 0.259958 | $-0.413079$ | 0.152863 | $-0.257011$ |
| 4.2 | $(1,1,0)$ | 0.106428 | $-0.198334$ | 0.748594 | $-0.331168$ |

Each listed equilibrium is strict for the trading actions.
No other pure profile passes all four deviation checks.
This is a statement inside the restricted profile set.
It is not a uniqueness theorem over mixed strategies.

Entry and ownership at $r=3$ are $0.625$ and $0.358422$.
They equal the baseline values.
Investor gross gains at the stated profiles also reproduce.

- $r=1.2$: $-0.014561$ in the hidden profile.
- $r=3$: $0.198787$, against $0.195836$ in the baseline.
- $r=3.6$: $0.279958$, against $0.275803$.
- $r=4.2$: $0.126428$, against $0.143240$.

At $r=1.2$, the baseline $+0.002083$ is a deviation gain at no trade.
It is $\bar G_0(1/2)$, not the hypothetical full-buying gain $\bar G_1$.
C10 should label that baseline object in T3 item 5.

The mechanism statement needs one word change.
The hidden order does not perfectly reveal cost to market makers.
Noise and the investor order overlap with the challenger unit.
The flow is informative about cost.
It is not an exact cost signal.
Entry stays unchanged because the focal challenger cleans its own order.
Cost independence from class keeps the cleaned class posterior unchanged.

One dominance extreme depends on an unstated price-pooling step.
The checker's flow-region calculation gives high-cost maximum $-0.070266$.
That value is at $r=1.2$ over $\beta$ grid points and four price schedules.
A later run of the C10 dominance script gives $-0.051291$.
The C10 script pools regions with equal prices before entry beliefs form.
The C10 memo does not describe that fixed-point pooling step.
The sign and all equilibrium results agree under both readings.
The smallest low-cost gains also agree:
$0.070660$, $0.109372$, $0.121211$ and $0.748594$.

The words "always" and "never" need the finite scope beside them.
Evidence covers $\beta\in\{0,1/4,1/2,3/4,1\}$ and four $\sigma$ schedules.
It does not cover every mixed $\beta$ or mixed challenger schedule.
The result heading already says numerical diagnostic.
That label is correct.

The challenger-as-trader tie rule is absent from the memo setup.
The C10 script uses no trade at a trading tie.
All equilibrium gains in the table are strict.
The missing tie statement has no benchmark effect.

### 3.10 Comparison with C10 scripts and saved outputs

The checker read the C10 code after the independent run.
Saved outputs match the memo after rounding.

- `output_memo_tables.txt` matches Tables A to E.
- `output_exact_identities.txt` matches the exact rational values.
- `output_value_of_disclosure.txt` matches D5(iv).
- Sensitivity values match a later print run.
- Public toehold values match a later print run.
- Hidden dominance values match a later print run, with Section 3.9 noted.

The C10 scripts use 60-digit arithmetic in high-precision mode.
They use fraction bisection or direct fractions in the surrogate mode.
They do not use interval enclosures for the true-$a$ grid.
That fact drives the D3 label correction.

The piece code has the same closure feature as the memo argument.
It skips cells with label GAP.
It adds both one-sided linear values at cell edges.
Those choices are visible in `pieces.py` and `persuasion.py`.
The memo should state them next to D2.

One exact-output wording is harmless but imprecise.
The support value 0 occurs on the 1,001-point grid at $\varphi=0$.
It also occurs at $\varphi^*$, which is not a grid point.
C10 should not read as if $\varphi=0$ were the only support point.

The formula-check script confirms the coarse $r$ grid.
Its naive formula column differs from the hull only at $r=1.4$.
The memo's corrected $\varphi_{FB}$ rule gives the hull value there.
The finer switch in Section 3.5 does not appear on that coarse grid.

## 4. Errors found and corrections

Severity order runs from high to low.
No error overturns the central $r=3$ disclosure numbers.

| Severity | Location | Error or gap | Correction |
|---|---|---|---|
| High | D5(i), summary | Entry under $\varphi^*$ does not fall at every $r$. It jumps up at $r\approx1.413$. | Limit monotonicity to the $\varphi_3$ regime. State the switch jump. Keep the $r_0$ to $r_1$ pair claim. |
| High | D2 and D3 | $\Phi(\varphi)$ is treated as one function despite coexistence and gaps. Hull edges can be one-sided limits. | Define a selection and a pure-existence domain. State closure at jump edges. Exclude gap support under the tie rule. |
| High | D3 label | True-$a$ grid evidence uses high-precision floats and bisection, not interval bounds. Exact fractions use $a=3/5$. | Label the grid application numerical diagnostic. Keep the conditional support theorem analytical. Add interval certificates for a computer-assisted label. |
| High | T1 | Truthful bids hold $t_L$ and $\Delta_T$ fixed while the low type wants to overbid. Effects are large at $s\ge0.5$. | Put fixed auction schedules in the result statement. Mark ceilings, widths and $s^*$ as partial-equilibrium values. |
| High | T2 | The proof compares entry rules as if the price experiment and auction gains stay fixed in $s$. | Add fixed-experiment, fixed-bid and publicly priced size conditions. Use conditional expected gains in the algebra. |
| Mid | D3 gap text | "Lower bound under the tie rule" mixes two games. Mixed roots in lower gaps are not proved by sign scans. | Say exact in the pure-continuation game. Say open in a mixed-tie extension. Prove roots cell by cell or remove the existence claim. |
| Mid | D4 and D5(ii) | Full-buying existence is stated, but selection and gap exclusions are not. | Name the full-buying selection. Add branch existence conditions and the thin-gap exception. |
| Mid | D5 heading | The heading says analytical for a mixed set of claims. | Label parts separately. Cross-switch, fixed-signal benchmark and U-shape parts are numerical. |
| Mid | T1 window | Two inequalities alone do not state the full trading-stage conditions. | Add bad-flow non-recruitment and investor existence checks. Note $c_H=5$ leaves the window after $s^*$. |
| Mid | T3 | Dominance and uniqueness language exceeds the finite pure and grid scope. Price pooling is not in the memo setup. | State the profile set, the $\beta$ grid, the class-L check, and the pooling rule. Replace perfect cost revelation with cost information. |
| Low | D1 proof | Step labels shift, and price inversion relies on unstated $w_L>0$. | Renumber steps. Add the strict price monotonicity line. |
| Low | D6 | The no-market pool at $\tau$ has no short proof in the memo. | Add the two-line support-line proof for the step payoff. |
| Low | T3 item 5 | Baseline $+0.0021$ at $r=1.2$ does not name its object. | Call it the no-trade deviation gain $\bar G_0(1/2)$. |
| Low | Section 3.8 and Section 4 | Price separation fails at the $r=1.2$ hidden equilibrium. The disclosure ceiling "removed" wording conflicts with value 9.97. | Limit separation to the stated buying cases. Say the ceiling moves from 3.99 to 9.97. |

Status labels after correction should read as follows.

- D1: analytical.
- D2: analytical for linearity; conditional for concavification.
- D3: analytical conditional on (C); numerical diagnostic on the true-$a$ grid.
- D4: analytical under full-buying selection and branch existence.
- D5: analytical in the $\varphi_3$ regime; numerical diagnostic elsewhere.
- D6: numerical diagnostic, with exact threshold formulas.
- T1: analytical inside the fixed-bid partial model; numerical roots.
- T2: analytical under the three scope conditions in Section 3.8.
- T3: numerical diagnostic.

## 5. What the original memo should change

1. Add a short domain paragraph after the D2 consequence.
   The paragraph must define the selection, the gap domain, and edge closure.
2. Restate D3 with $0<\tau<1$, $w_L>0$ and $\Delta_T>0$.
   The statement should separate the conditional theorem from grid evidence.
3. Replace the D3 computer-assisted label for the true-$a$ grid.
   Use numerical diagnostic, or add interval certificates for condition (C).
4. Replace "lower bound under the tie rule" in D3 and Section 6.
   Use exactness in the pure-continuation game and openness under mixed ties.
5. Add full-buying selection and branch existence to D4.
   Add the same exception to D5(ii) for a branch in a gap.
6. Correct D5 monotonicity.
   State the fall in $\varphi^*$ and the entry jump at $r\approx1.413$.
7. Split the D5 status label by part.
   Keep the benchmark reversal failure between $r=1.2$ and $r=3$.
8. Put fixed truthful auction schedules in the T1 result statement.
   Add the spread and low-type gain magnitudes from the bid response.
9. Add the two T1 side conditions for the benchmark window.
   State that $c_H=5$ is inadmissible after the break stake.
10. Rewrite the T2 proof with conditional expected entry gain.
    Add fixed experiment, fixed bids, and publicly priced size.
11. State the T3 class-L investor check and challenger trading tie rule.
    Add the equal-price pooling rule used in the dominance calculation.
12. Replace perfect cost revelation in T3 with cost information in flow.
    Limit "always", "never" and "unique" to the stated finite sets.
13. Fix local wording in D1, D6, Section 3.8 and Section 4.
    The required text changes sit in the table in Section 4.

## 6. Plain summary

The main C10 numbers reproduce from an independent calculation. At $r=3$, the optimal public test pass prior is $0.699$, entry rises from $0.625$ to $0.786$, and high-class ownership rises from $0.358$ to $0.5$. Valley formulas, ceilings, sensitivity values, public-toehold numbers under fixed bids, and hidden-unit equilibria also reproduce.

Four corrections matter. Concavification needs an explicit selection. It must also handle priors with no pure equilibrium. Condition (C) evidence at the true noise ratio is high-precision numerical work. It is not an interval proof in C10. Entry under optimal disclosure does not fall at every incumbent strength. It jumps up at the switch near $r=1.413$. It still falls from $r=1.2$ to $r=3$. Public-toehold results hold only with auction schedules fixed. Optimal low-type overbidding sharply reduces the payoff spread at large stakes. The fair-price toehold proof also needs a fixed trading experiment. Hidden-unit results survive as a finite numerical diagnostic.


