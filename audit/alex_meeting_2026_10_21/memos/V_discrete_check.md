# Independent numerical check of the discrete models

## 1. Question and reading

This memo checks the three discrete menus in the shared brief. It treats the challenger as an observer of price alone.

The main one-directional results survive. The benchmark entry path is $1/4\to1/3\to1/3$. The later return occurs after $r=7.9686269666$.

The main new finding concerns the two-sided menu. At $r=3$, $\lambda=0.8$, and $k=0.02$, two price schedules support full trade. Entry is $0.466667$ in one schedule and $0.416667$ in the other. Both satisfy the prescribed investor tie rule. Neither has an off-path flow.

Three qualifications matter:

1. A positive entry floor is sufficient for price sufficiency. It is not necessary.
2. The stated investor tie rule excludes every genuine trade–zero mixture in this model.
3. The buy-not-sell window describes pure outcomes. Conventional mixed strategies add outcomes inside that window.

Inputs read:

- [BRIEF.md](../BRIEF.md), especially Sections 0 and 3.2.
- [Q2_discrete_buy_only.md](Q2_discrete_buy_only.md), Claims 1–12.
- [Q2_discrete_literature.md](Q2_discrete_literature.md), especially C1–C7.
- [LIT_extracts.md](LIT_extracts.md), especially A1–A2.
- [Q2_discrete_sell_only.md](Q2_discrete_sell_only.md), Claims 1–14. This file became available before the comparison was complete.
- The local manuscript, Sections 2–3 and Proposition A.2, for the information sets and auction payoffs.

The calculation uses new code. It does not import or run any memo's scripts. The source files and results are under [V_discrete_check](../scripts/V_discrete_check/).

**Status convention.** CONFIRMED means the stated calculation or algebra survives this check within its stated assumptions. REFUTED identifies a counterexample or a false boundary. NOT CHECKED identifies an unverified claim. A numerical diagnostic does not establish a general uniqueness theorem.

## 2. Formal setup

The primitives are those of the brief. The prior on $H$ is $1/2$. The incumbent value is uniform on $[0,r]$. The challenger prepares at cost indifference. The investor has no initial stake.

The menus are

$$
M1=\{0,1\},\qquad M2=\{-1,0\},\qquad M3=\{-1,0,1\}.
$$

Write $\sigma_j(q)$ for each present type's strategy. Let $n(z)$ denote the noise probability, with zero probability outside its support. The conditional flow law is

$$
f_j(x)=(1-\lambda)n(x)+\lambda\sum_{q\in M}\sigma_j(q)n(x-q).
$$

For an on-path flow,

$$
w_x=\frac{f_H(x)+f_L(x)}2,
\qquad
\mu_x=\frac{f_H(x)}{f_H(x)+f_L(x)}.
$$

The code integrates the piecewise auction receipts to obtain $t_0,t_H,t_L,g_H,g_L$. A separate quadrature calculation reproduces those objects. The spread is $\Delta_T=t_H-t_L$.

For a block $S$ of flows with one price, the challenger uses

$$
\nu_S=\frac{\sum_{x\in S}f_H(x)}{\sum_{x\in S}[f_H(x)+f_L(x)]},
\qquad
e_S=\rho\mathbf1\{B_r(\nu_S)\ge c_L\}
 +(1-\rho)\mathbf1\{B_r(\nu_S)\ge c_H\}.
$$

The market maker still conditions on its own flow:

$$
P_x=t_0+e_S[t_L-t_0+\Delta_T\mu_x],\qquad x\in S.
$$

Every price must be equal within its block. Different blocks must have different prices. These conditions enforce price observation without a substitution of flow observation.

For every menu action, the program computes

$$
U_j(q)=\sum_z n(z)q\{t_0+e_{q+z}(t_j-t_0)-P_{q+z}\}-k|q|.
$$

It holds the candidate price and entry schedules fixed during this calculation. It checks wrong-direction actions in M3 as well.

The reported outcomes are

$$
\mathsf E=\sum_x w_xe_x,
\qquad
\mathsf O_H=\frac12\sum_x f_H(x)e_x.
$$

Here $\mathsf O_H$ means ownership by the high-value challenger. It does not mean ownership by whichever bidder has the larger realized value.

The outputs distinguish two investor rules:

- **Prescribed rule:** an investor chooses zero when zero and a trade give the same maximum payoff.
- **Conventional correspondence:** an investor may mix among actions with the same maximum payoff.

The challenger enters at indifference in both calculations. Separate examples that allow challenger mixtures carry an explicit changed-rule label.

## 3. Results

### 3.1 Dominance and the full simplex

**CONFIRMED — analytical.** Wrong-direction orders cannot occur in a zero-stake equilibrium.

For any consistent price schedule,

$$
V_H(x)-P_x=e_x\Delta_T(1-\mu_x)\ge0,
\qquad
V_L(x)-P_x=-e_x\Delta_T\mu_x\le0.
$$

A sale by $H$, or a purchase by $L$, therefore pays at most $-k<0$. Zero pays zero. This argument also applies to every off-path belief in $[0,1]$.

The full simplex mesh has step $1/40$. M3 has 861 strategies per type and 741,321 profile pairs. Each one-directional menu has 1,681 profile pairs.

The program computes flow posteriors across these full simplices for all five presence probabilities and all three main noise laws. This covers 11,170,245 profile pairs. Strict dominance removes profiles with positive probability on a wrong-direction order before the continuation search.

The retained M3 face has $41^2=1,681$ grid points. It includes every pair of purchase and sale probabilities on that mesh. Local roots supplement the mesh. The reduction is analytical; it does not assume pure strategies.

Let $a=\Pr(q_H=1)$ and $b=\Pr(q_L=-1)$. The prescribed rule forces $a,b\in\{0,1\}$ in equilibrium. A genuine mixture requires zero trade profit, which activates the rule to choose zero.

Thus the strict equilibrium calculation is finite and exhaustive after dominance. The conventional mixed calculation remains a numerical diagnostic.

### 3.2 Every consistent price partition

**CONFIRMED — analytical.** A price can hide different flow posteriors only when entry at that price is zero.

If $P_x=P_y=P$ and entry is positive, then

$$
0=P_x-P_y=e(P)\Delta_T(\mu_x-\mu_y).
$$

Since $r>\ell$, this implies $\mu_x=\mu_y$. If entry is zero, every such flow has price $t_0$. All zero-entry flows must therefore belong to one price block.

This gives a finite construction:

1. Enumerate a partition of the feasible flows.
2. Compute the pooled posterior for each block.
3. Compute entry from that posterior.
4. Compute each flow's competitive price.
5. Retain the partition only if its prices satisfy all block equalities and inequalities.

The program enumerates all 15 partitions for a four-flow menu and all 52 partitions for M3. It includes unused flows. At an unused price, the posterior over unused flows is free within their specified beliefs' convex hull.

For the numerical root search, an equivalent construction enumerates every entry vector in $\{0,\rho,1\}^{|X|}$. The zero entries define the one possible zero-price pool. Bayes denominators convert the entry conditions into affine inequalities in $(a,b)$. The code enumerates these regions before it searches for roots. Every reported root then receives a fresh full-partition calculation.

Two labels distinguish the outcomes:

- **Canonical:** each flow receives the entry rate implied by its own posterior.
- **Self-fulfilling pool:** a zero-price block suppresses entry at a flow whose own posterior would induce entry.

A canonical schedule need not reveal every posterior. Several already inactive flows can share $t_0$. For example, at $r=3,\lambda=0.9$, M3 pools two inactive flows with different posteriors. This differs from an additional pool that changes entry.

The strong floor $c_L\le g_L$ excludes every zero-entry block. Under equal noise, the one-directional menus also admit the weaker sufficient condition $c_L\le B_r(1/3)$. This condition excludes every pool that combines the low extreme with an active flow.

**REFUTED:** price sufficiency requires the strong floor. At the original benchmark, M1 has three prices that identify posteriors $0,1/2,1$, although entry at posterior zero is zero. The buy-only and sell-only memos handle this distinction correctly in their detailed claims. The literature memo's “only with a floor” language is too strong.

### 3.3 Exact cutoffs and the role of ties

**CONFIRMED — analytical.** With equal noise and a canonical schedule, each one-directional trade has gross payoff

$$
K=\frac{\bar e\Delta_T}{3},\qquad \bar e=e_r(1/2).
$$

The trade visits two prior-posterior flows and one revealing flow. Each prior flow contributes $\bar e\Delta_T/6$. The revealing flow contributes zero. Presence changes flow frequencies, but it does not change this conditional trade payoff.

Under the prescribed rule, no trade occurs for $k\ge K$, and full trade occurs for $k<K$. Under conventional indifference, every trade probability is possible at $k=K$, subject to the price conditions.

If one interior flow belongs to an inactive price pool, the gross payoff becomes $\bar e\Delta_T/6$. This reproduces the buy-only memo's second cutoff.

For M3 at $\lambda=1$, the pure-profile conditions are

| Profile | Prescribed-rule condition |
|---|---|
| No trade | $k\ge\bar e\Delta_T/3$ |
| Both types trade | $k<\bar e\Delta_T/6$ |
| Buy-not-sell or sell-not-buy | $\bar e\Delta_T/6\le k<\bar e\Delta_T/3$ |

These conditions use the directional off-path completion and the benchmark's canonical prices. In full two-sided trade, only flow zero pays a positive residual. This gives the factor $1/6$.

With a passive posterior $1/2$ at an unused extreme, no trade instead requires $k\ge\bar e\Delta_T/2$. This gives the third requested cutoff.

In the benchmark's one-directional menus,

$$
r_T=1+\frac{3k}{\rho}
 +\sqrt{\left(\frac{3k}{\rho}\right)^2+\frac{6k}{\rho}}
=1.9732121111929344.
$$

The single cutoff applies where $\bar e=\rho$ remains fixed. A cost crossing at the prior can reduce $\bar e$. Unequal noise can also create a coexistence interval. A general single-crossing claim would therefore be false.

### 3.4 The presence window and mixed outcomes

**CONFIRMED — analytical, pure-profile scope.** At $r=3$, the costly entrant's threshold is $\tau_H=141/200$. A sell-not-buy profile produces the upper posterior $1/(2-\lambda)$.

Costly entry starts when

$$
\lambda\ge2-\frac1{\tau_H}=\frac{82}{141}=0.5815602837.
$$

The inequality includes equality because the challenger enters at indifference.

Once that entry occurs, the high type's purchase deviation against sell-not-buy has gross payoff

$$
\frac{\rho\Delta_T}{6}
 +\frac{\Delta_T(1-\lambda)}{3(2-\lambda)}.
$$

Sell-not-buy also requires the low type to prefer a sale: $k<\rho\Delta_T/3$. These conditions leave a nonempty cost interval exactly when

$$
\frac{1-\lambda}{2-\lambda}<\frac\rho2,
\quad\text{or}\quad \lambda>\frac67.
$$

Thus the reported asymmetric window is correct for pure outcomes, with the exact endpoints

$$
\boxed{\lambda\in[82/141,\;6/7].}
$$

**REFUTED as a statement about conventional mixed equilibria.** At $r=3,\lambda=0.8,k=0.05$, both of these outcomes exist:

| Strategy when present | $\mathsf E$ | $\mathsf O_H$ | Prescribed tie rule |
|---|---:|---:|---|
| Buy-not-sell: $(a,b)=(1,0)$ | 0.350000000 | 0.225000000 | Satisfies |
| $(a,b)=(5/12,5/12)$ | 0.277777778 | 0.166666667 | Excluded |

In the mixed outcome, the effective trade probabilities are $\lambda a=\lambda b=1/3$. The flow posteriors are $0,0.4,0.5,0.6,1$. Entry rates are $0,\rho,\rho,\rho,1$.

Both correct trades have gross payoff

$$
\frac{\Delta_T}{3}\left(\frac\rho2+0.4\rho\right)=0.05=k.
$$

Every wrong-direction trade has negative net payoff. The mixture is a conventional equilibrium, but the pinned investor rule selects zero at the tie.

This example also refutes the literature memo's unqualified statement that every flow at $\lambda=1$ is revealing or uninformative. That statement holds for its listed pure profiles. Mixed profiles produce partial posteriors. For example, at $\lambda=1,k=0.05$, $(a,b)=(1/3,1/3)$ gives the same five posteriors.

### 3.5 An additional price equilibrium at the original costs

**CONFIRMED — analytical construction and numerical diagnostic.** Set $r=3,\lambda=4/5,k=1/50$, with the original benchmark costs. Both types trade fully.

| Flow | Probability | Flow posterior | Canonical entry | Entry with the extra pool |
|---:|---:|---:|---:|---:|
| $-2$ | $2/15$ | $0$ | $0$ | $0$ |
| $-1$ | $1/5$ | $1/6$ | $1/4$ | $0$ |
| $0$ | $1/3$ | $1/2$ | $1/4$ | $1/4$ |
| $1$ | $1/5$ | $5/6$ | $1$ | $1$ |
| $2$ | $2/15$ | $1$ | $1$ | $1$ |

The extra schedule sets $P(-2)=P(-1)=t_0=5/12$. The challenger then uses

$$
\nu_{\{-2,-1\}}=\frac{1-\lambda}{2}=\frac1{10},
\qquad
B_3(1/10)=\frac{23}{24}<1.
$$

Zero entry therefore confirms that price. By contrast, the flow posterior at $-1$ gives

$$
B_3(1/6)=\frac{109}{72}>1.
$$

That flow supports low-cost entry in the canonical schedule. The extra pool changes the decision, rather than just the price's label.

All net action payoffs under the extra pool are:

| Type | Sell | Zero | Buy |
|---|---:|---:|---:|
| $H$ | $-0.047777778$ | $0$ | $0.044814815$ |
| $L$ | $0.007777778$ | $0$ | $-0.455185185$ |

Every prescribed trade is strictly optimal. There is no tie and no off-path belief.

The outcomes are

$$
(\mathsf E,\mathsf O_H)_{\rm canonical}=(7/15,7/20),
\qquad
(\mathsf E,\mathsf O_H)_{\rm pool}=(5/12,41/120).
$$

This is an open-region phenomenon. At $r=3$, the extra pool is feasible when $\lambda>0.79$. The canonical low-cost entrant at $-1$ remains active for $\lambda\le158/179$.

Thus both price schedules exist for

$$
0.79<\lambda\le0.8826815642,
\qquad k<\rho\Delta_T/6,
$$

within the costly-entry region used above. At the lower endpoint, the pooled low-cost entrant enters, so zero entry fails.

The literature memo checks pools at $\lambda=1$ and $1/2$. Its negative result on those points is confirmed. It does not cover this intermediate presence window.

### 3.6 Off-path beliefs

**CONFIRMED — analytical.** Directional beliefs minimize a correct-direction deviation's residual at an unused extreme. They assign $H$ to an unused purchase and $L$ to an unused sale.

Dominance excludes the wrong type whenever the refinement has a profitable deviation to consider. If no type can gain under any response, that argument does not determine a unique belief. The solver therefore calls this a **directional completion**, rather than an unconditional uniqueness result for the Intuitive Criterion.

For every reported on-path outcome, the output records whether a consistent continuation supports it under:

- `directional`: the completion above;
- `all_L`: posterior zero at each unused flow;
- `all_H`: posterior one at each unused flow;
- `prior`: posterior $1/2$ at each unused flow;
- `max_deviation`: beliefs that maximize the unused-flow residual of the relevant deviator.

The extreme state beliefs are not always extreme incentives. A high type's off-path gain is $e(v)\Delta_T(1-v)$. Its maximum can occur at an entry threshold, rather than at $v=0$ or $v=1$. The code evaluates both cost thresholds as well as the endpoints.

The low type's gain is $e(v)\Delta_Tv$. It is nondecreasing in $v$, so its maximum occurs at $v=1$.

At $r=1.8,k=0.02$, no trade survives the directional completion in all three menus. Passive beliefs eliminate it. In M1, both extreme state beliefs still permit no trade at the original costs. An interior high-cost threshold belief can eliminate it. Thus checks at posterior zero and one alone do not establish belief robustness.

The output flags report existence of a consistent off-path price continuation under each belief rule. They do not mean that every continuation under that rule works. The detailed point outputs retain the supporting off-path prices.

### 3.7 Unequal noise and existence

**CONFIRMED — numerical diagnostic, with analytical endpoint comparisons.** The buy-only memo's unequal-noise examples reproduce:

| Noise | Other changes | $k$ | Conventional M1 outcomes |
|---|---|---:|---|
| $(0.1,0.2,0.7)$ | $r=2+\sqrt3$, $c_L=0.02$ | 0.045 | $a=0$, $a=0.5160395534$, $a=1$ |
| $(0.7,0.2,0.1)$ | Same $r,c_L$; $c_H=12$ | 0.080 | $a=0.3856157589$ |

In the first row, the two pure outcomes satisfy the prescribed rule. In the second row, the only conventional equilibrium is excluded by that rule.

The sell-only memo's coexistence intervals also reproduce on its $0.005$ strength grid:

| Noise | $c_H$ | No-trade and full-sale coexistence |
|---|---:|---|
| $(0.25,0.5,0.25)$ | 6 | $r\in[1.545,1.900]$ |
| $(0.2,0.6,0.2)$ | 6 | $r\in[1.585,1.860]$ |
| $(0.4,0.4,0.2)$ | 7 | $r\in[1.975,2.040]$ |

The boundaries in this table are grid endpoints, not exact roots.

An entry jump can also remove every conventional investor equilibrium when the challenger must enter at its cost threshold. The sweep has 3,376 such empty numerical cases under noise $(0.1,0.2,0.7)$, all in M3. A second calculation uses quadratic resultants on every empty case. It finds no extra root and no unresolved algebraic degeneracy. This remains numerical evidence, not an interval-arithmetic nonexistence certificate.

The sell memo's example with $(c_L,c_H,r,k)=(2.5,7,3,0.03)$ and noise $(0.2,0.6,0.2)$ also has no equilibrium in the pinned game. If both tie rules change, its proposed outcome reproduces:

$$
s_L=0.7543859649,\quad
\Pr(\text{low-cost entry at the threshold})=0.2713815789,
\quad \mathsf E=0.1672264543.
$$

This outcome requires an investor mixture and a challenger mixture. It is not an equilibrium under the brief's two tie selections.

The claim that challenger mixtures always restore existence needs an additional condition: investors must also be allowed to mix at zero profit. For a counterexample, use M2, noise $(0.1,0.2,0.7)$, $r=2+\sqrt3$, $c_L=0.02$, $c_H=12$, and $k=0.08$. The only conventional strategy has $s_L=0.3856157589$. Neither challenger cost is ever at indifference. Challenger mixtures therefore cannot repair the investor tie rule's exclusion.

### 3.8 Fixed experiments and the later entry fall

**CONFIRMED — analytical.** At every fixed posterior, both $g_H(r)$ and $g_L(r)$ decrease with $r$. Each cost type's entry indicator therefore weakly decreases. An average under a fixed price experiment has the same sign.

A fixed order profile does not always fix the price experiment. The buy memo's example reproduces: with $c_L=3$, a pooled M1 equilibrium at $r=3$ has entry $1/4$. The canonical equilibrium at $r=3.1$ has entry $1/3$. Orders remain unchanged. The price partition changes.

For $\lambda=1$, costly preparation ends strictly above

$$
r_C=4+\sqrt{16-1/4}=7.968626966596886.
$$

To derive the root, solve $g_H(r)=c_H$:

$$
r^2-2(h-c_H)r+p^2=0.
$$

The larger root lies in the model's domain. Entry persists at equality. This confirms the memos' correction to the paper's $r_2=3.6$ comparison.

At uncertain presence, M1 retains posterior one at its high extreme. M2 instead has maximum posterior $1/(2-\lambda)$. Its costly-entry ceilings are:

| $\lambda$ | M2 costly-entry ceiling |
|---:|---:|
| 0.5 | 2.060660172 |
| 0.7 | 4.394310826 |
| 0.8 | 5.582085549 |
| 0.9 | 6.774166564 |
| 1.0 | 7.968626967 |

M3 can lose costly entry at flow $1$ at the earlier ceiling, while it retains costly entry at flow $2$. Its entry path can therefore have more than one fall.

### 3.9 Claim ledger

The ledger separates each memo's scope from stronger interpretations. References to “strict” mean the prescribed investor tie rule.

#### Buy-only memo

| Claim | Verdict | Evidence or limit |
|---|---|---|
| 1: flow likelihoods, prior interiors, revealing extremes | CONFIRMED | Direct convolution over both full simplices; Section 3.1. |
| 2: low type never buys | CONFIRMED | Strict dominance proof in Section 3.1. |
| 3: price sufficiency under the floor | CONFIRMED | Partition identity in Section 3.2. |
| 4: directional completion and no-trade belief dependence | CONFIRMED | Every unused-flow continuation is enumerated; Section 3.6. |
| 5: $\bar e\Delta_T/3$, the threshold continuum, and one crossing when $\bar e=\rho$ | CONFIRMED | Section 3.3 and the exact-boundary runs. The continuum uses the conventional rule. |
| 5: a prior-cost crossing can produce trade, no trade, then trade | CONFIRMED | $\bar e$ falls while $\Delta_T$ rises. The two spread thresholds in that claim follow directly. |
| 6: additional one-interior-flow pools and $\bar e\Delta_T/6$ | CONFIRMED | Exhaustive partitions; at $c_L=3,r=3$, both extra M1 pools occur. |
| 7: entry and ownership sums, including pooled schedules | CONFIRMED | Independent sums of conditional flow masses and entry rates. |
| 8: the stated sufficient three-strength proposition | CONFIRMED | The $c_L=0.02$ example gives $0.25\to0.375\to0.25$ at $r=1.2,3,8.5$. |
| 9: fixed-experiment deterrence; fixed orders alone are insufficient | CONFIRMED | Section 3.8, including the $c_L=3$ counterexample. |
| 10: unequal-noise likelihoods, payoff formula, and finite pool construction | CONFIRMED | Convolution and all entry regions reproduce these formulas. Within a region, the one-variable equation is quadratic. |
| 10: zero-noise support corners | CONFIRMED | Analytically, disjoint supports at noise $\{-1,1\}$ leave no profitable M1 trade under revealing deviation beliefs. The main grid uses positive probabilities. |
| 11: unequal-noise coexistence and a tie-rule existence failure | CONFIRMED | Both mixed roots and both endpoint payoffs reproduce; Section 3.7. |
| 12: presence-independent equal-noise cutoff and conditional floor formula | CONFIRMED | All five presence values, both low costs, and the full strength grid. |

#### Literature memo

| Claim | Verdict | Evidence or limit |
|---|---|---|
| C1: the listed pure-profile posterior table | CONFIRMED | Direct likelihood calculation. |
| C1: every flow at $\lambda=1$ is revealing or at the prior, without a pure-profile restriction | REFUTED | The M3 mixture in Section 3.4 gives interior posteriors $0.4$ and $0.6$. |
| C2: unused flows for NT, T, BNS, and SNB | CONFIRMED | Exhaustive support calculation. |
| C3: dominance supplies the directional completion | CONFIRMED | Section 3.1. |
| C3: the Intuitive Criterion always fixes a unique belief | REFUTED | At a sufficiently large $k$, neither type can gain under any response. The criterion is then silent. |
| C4: $1/3$ versus $1/2$ no-trade cutoffs | CONFIRMED | Section 3.3; passive beliefs remove the benchmark no-trade outcome at $r=1.8$. |
| C5: $c_L\le g_L$ is required for low-cost entry at a revealing-low flow | CONFIRMED | At $r=3$, $g_L=0.125<1$. Entry is zero at that flow. |
| C5: price sufficiency survives only with that floor | REFUTED | Canonical M1 and M2 at $r=3,c_L=1$ reveal all on-path posteriors despite zero entry at the low extreme. |
| C5: no extra pools at its checked pure profiles, $\lambda\in\{1,1/2\}$, $r\in\{1.2,3,3.6\}$ | CONFIRMED | The negative result holds on those points. Section 3.5 supplies an extra pool at $\lambda=0.8$. |
| C6: pure M3 cutoffs, benchmark entry, and the late ceiling | CONFIRMED | Section 3.3 and the outcome tables below. |
| C7: BNS-only partial-trade window among pure outcomes | CONFIRMED | Exact window $[82/141,6/7]$. |
| C7: an open lower endpoint under entry at indifference | REFUTED | Recruitment also occurs at $\lambda=82/141$. |
| Recommendation 3 if read as uniqueness over all mixtures | REFUTED | BNS and a conventional mixture coexist at $\lambda=0.8,k=0.05$. |
| EGJ baseline menu, noise, presence, investor tie, flow observation, and pure-profile scope | CONFIRMED | Published Sections I.B–I.C and II.C, independently read online. |
| GG's two-date equilibrium and manipulation results | NOT CHECKED | The supplied extract was read. This one-date solver does not reproduce that model; the independent full-text route failed. |
| Claims about DGG, BKT, BGP, GOY, and the unread papers | NOT CHECKED | Outside this numerical model. The supplied version and access warnings remain in force. |
| Initial-stake results attributed to EGJ Appendix B.2 | NOT CHECKED | The supplied extract also marks that appendix unverified. |

EGJ means Edmans, Goldstein, and Jiang (2015), *American Economic Review* 105(12), 3766–3797. The [published article](https://alexedmans.com/wp-content/uploads/2024/06/LTA.pdf), Sections I.B–I.C and II.C, confirms the specified trading block and its pure-profile scope. Its flow-observation assumption does not supply a price-sufficiency theorem for this model.

#### Sell-only memo

| Claim | Verdict | Evidence or limit |
|---|---|---|
| 1: all-profile posteriors and revealing-flow table | CONFIRMED | Direct convolution on the full simplex. |
| 2: high type never sells with zero initial stake | CONFIRMED | Section 3.1. The unrestricted stake extension is a separate claim. |
| 3(a)–(c): unused flow, directional completion, and supportive-belief cutoff | CONFIRMED | Section 3.6. The memo itself states when the refinements are silent. |
| 3(d)–(e): passive/adverse gaps and benchmark robustness at $r_0$ | CONFIRMED | Cutoffs $1.7478775383$, $1.3615346871$, and $1.9732121112$ reproduce. |
| 4(a)–(b): zero-entry pool restriction and sufficient condition S1 | CONFIRMED | The smallest relevant pooled posterior is $1/(2+\lambda s_L)\ge1/3$. |
| 4(c): the two prior-posterior flows always share a price | REFUTED outside S1 | At $c_L=3,r=3$, the pool $\{-2,-1\}$ gives $P(-1)=t_0\ne P(0)$. Claim 4(d) itself describes this exception. |
| 4(d): the extra pooled equilibrium | CONFIRMED | Both possible one-interior-flow pools reproduce at the stated benchmark variant. |
| 4(d): pooled entry $(1+2\rho)/6$ without a costly-entry assumption | REFUTED | Set $c_H=12,c_L=3,r=3$. Pooled entry is $0.125$, not $0.25$. The general formula is $(e_1+2\bar e)/6$. |
| 4(e): S1 holds on the benchmark domain $(1,10)$ | CONFIRMED | The minimum of $B_r(1/3)$ on its closure is $1.6875>1$. The quoted root above $h$ is outside the auction domain. |
| 5: one cutoff, outcomes, and conventional threshold continuum | CONFIRMED | All one-directional grid outputs and the exact-boundary run. The continuum is excluded by the prescribed tie rule. |
| 6: sufficiency of S1–S3 and the stated entry comparison | CONFIRMED | Entry need not exceed $\rho$ without the floor when $\rho\ge1/2$. At $\rho=0.6$, entry is $0.566667<0.6$. |
| 6: the strict weak-economy inequality in S3 is necessary | REFUTED at equality | At $r_0=r_T$, the prescribed rule still selects unique no trade. The lower condition can be weak. |
| 7: information from the absence of sales; recruitment does not pay the seller | CONFIRMED | The recruiting extreme is outside the seller's conditional flow support. |
| 8(a): neutrality of feedback under the canonical equal-noise schedule | CONFIRMED | Both profitable trade terms retain the prior, for every presence probability. Extra zero-entry pools require a separate qualification. |
| 8(b)–(c): entry scales residuals; a positive floor prevents an absolute reduction relative to fixed entry $\rho$ | CONFIRMED | Multiply each nonnegative residual by $e/\rho\ge1$. The comparison holds at a fixed experiment. |
| 8(d): the two stated numerical feedback examples | CONFIRMED | The first gives positive full-sale profit; the second loses every pinned equilibrium after the entry jump. |
| 9: fixed-experiment deterrence and its three cost examples | CONFIRMED | At $c_L=1,0,0.2$, frozen full-sale entry is respectively $1/3\to1/3$, $3/8\to3/8$, and $3/8\to1/3$. |
| 10: uncertain-presence formulas and the $\lambda=3/4$ example | CONFIRMED | At $r=3$, M1 gives $(0.34375,0.21875)$ and M2 gives $(0.375,0.25)$. |
| 11(a)–(b): unequal-noise posteriors and the symmetric constant-entry derivative | CONFIRMED | The derivative is negative on the stated interval. An interior solution uses conventional investor indifference. |
| 11(c): necessary endpoint condition for coexistence at constant entry | CONFIRMED | The harmonic-mean inequality gives the stated bound. The example has $s_L=2/3$ in the conventional correspondence. |
| 11(d): the displayed pure coexistence ranges | CONFIRMED | All three ranges reproduce on the stated $0.005$ grid. |
| 11(d): a third equilibrium at $s_L=0.7015$ in the pinned model | REFUTED under the pinned rules | It requires both investor and challenger mixtures. With both changes, the calculated values are $s_L=0.7015267176$ and costly-entry probability $0.6340424659$. |
| 11(e): the entry-jump nonexistence example and its changed-rule mixture | CONFIRMED | Section 3.7. The low-cost entrant's mixture is $0.2713815789$. |
| 11(e): challenger mixtures alone always restore existence | REFUTED with the prescribed investor rule | The constant-entry M2 counterexample in Section 3.7 has no indifferent challenger and needs an investor mixture. |
| 11(f): sufficient upper/lower profit bounds and outcome accounting | CONFIRMED | Each residual is bounded by its entry-free value and, under the stated floor, by $\rho$ times that value. Direct sums reproduce the accounting identities. |
| 12: the independent buy-only formulas under S1 | CONFIRMED | They match the independent M1 calculation. |
| 13(a)–(c): full-trade shift identity at $\lambda=1$ and the menus' differences | CONFIRMED | A unit shift preserves the joint flow law. The identity $f_L\mu=f_H(1-\mu)$ gives equal full-trade profits. |
| 13: local complementarity is possible only if $\pi_->\pi_+$ in M2 | REFUTED if “complementarity” means a positive local derivative | With noise $(0.1,0.7,0.2)$, $c_L=0.02,c_H=12,r=3$, the sale payoff rises near $s_L=1$. The endpoint coexistence condition remains valid. |
| 14: the four local stake thresholds | CONFIRMED | $0.2327272727$, $0.3103030303$, $1.9490909091$, and $2.5987878788$ reproduce. |
| 14: full selling survives at equality in its stake bound | REFUTED at equality | The investor then ties with zero and must choose zero. The survival condition is strict. |
| 14: the complete equilibrium set with a positive stake | NOT CHECKED | Only the stated local deviations were computed. The full solver concerns zero initial stake. |

The “more than one equilibrium” ranges that include challenger mixtures in sell Claim 11(d) were not reproduced as a full changed-rule correspondence. Their pure coexistence ranges were checked. Their mixed-rule interval endpoints remain **NOT CHECKED**.

## 4. What changes relative to the current paper

The auction formulas survive. The continuous-support posterior bounds do not survive. A revealing flow can make a correct-direction residual exactly zero.

Price sufficiency survives under a positive entry floor. It can also survive without that floor in a particular finite experiment. A zero-entry price can instead hide several beliefs and change entry, as Section 3.5 shows.

The one-directional benchmark has a clean trade cutoff. It preserves the information mechanism: greater incumbent strength activates trade and can recruit a costly challenger. Equal noise makes the recruitment event irrelevant to the informed trader's own profit.

The two-sided menu has a separate partial-trade interval. At uncertain presence, it can also have multiple price schedules for the same strict trading profile. A pure-profile classification therefore does not establish unique prices or unique entry.

The late return in Proposition 2 requires new values of $r_2$ and, for return exactly to $\rho$, a valid low-cost floor. The original costs give a return below $\rho$ at certain presence.

Proposition A.3 survives for a fixed information experiment. A fixed order profile alone is insufficient when the price partition can change.

## 5. Numerical example and reproducible output

**Status: numerical diagnostic.** All main rows use $(h,\ell,p,\rho,c_H)=(10,1,0.5,0.25,6)$.

The cost variants are $c_L=1$ and $c_L=0.02$. The second gives a floor throughout $1<r<10$, since $g_L(r)>0.0375>0.02$.

### Benchmark path at $k=0.02$, $\lambda=1$

Each cell reports $(\mathsf E,\mathsf O_H)$ under the prescribed rule.

| $c_L$ | Menu | $r=1.2$ | $r=3$ | $r=3.6$ | $r=8.5$ |
|---:|---|---|---|---|---|
| 1 | M1 or M2 | $(0.25,0.125)$ | $(1/3,0.25)$ | $(1/3,0.25)$ | $(5/24,0.125)$ |
| 1 | M3 | $(0.25,0.125)$ | $(5/12,0.375)$ | $(5/12,0.375)$ | $(1/6,0.125)$ |
| 0.02 | M1 or M2 | $(0.25,0.125)$ | $(0.375,0.25)$ | $(0.375,0.25)$ | $(0.25,0.125)$ |
| 0.02 | M3 | $(0.25,0.125)$ | $(0.5,0.375)$ | $(0.5,0.375)$ | $(0.25,0.125)$ |

### Presence comparison at $r=3$, $k=0.02$

Each cell reports $(\mathsf E,\mathsf O_H)$. Every row uses a strict trading equilibrium. A semicolon separates distinct price equilibria.

| $c_L$ | $\lambda$ | M1 | M2 | M3 |
|---:|---:|---|---|---|
| 1 | 1.0 | $(0.333333,0.250000)$ | $(0.333333,0.250000)$ | $(0.416667,0.375000)$ |
| 1 | 0.5 | $(0.312500,0.187500)$ | $(0.229167,0.125000)$ | $(0.291667,0.187500)$ |
| 1 | 0.7 | $(0.337500,0.212500)$ | $(0.383333,0.250000)$ | $(0.470833,0.337500)$ |
| 1 | 0.8 | $(0.350000,0.225000)$ | $(0.366667,0.250000)$ | $(0.466667,0.350000)$; $(0.416667,0.341667)$ |
| 1 | 0.9 | $(0.316667,0.233333)$ | $(0.350000,0.250000)$ | $(0.416667,0.358333)$ |
| 0.02 | 1.0 | $(0.375000,0.250000)$ | $(0.375000,0.250000)$ | $(0.500000,0.375000)$ |
| 0.02 | 0.5 | $(0.312500,0.187500)$ | $(0.250000,0.125000)$ | $(0.312500,0.187500)$ |
| 0.02 | 0.7 | $(0.337500,0.212500)$ | $(0.412500,0.250000)$ | $(0.500000,0.337500)$ |
| 0.02 | 0.8 | $(0.350000,0.225000)$ | $(0.400000,0.250000)$ | $(0.500000,0.350000)$ |
| 0.02 | 0.9 | $(0.362500,0.237500)$ | $(0.387500,0.250000)$ | $(0.500000,0.362500)$ |

### Grid declaration and observed computation

- Equal noise: 179 strengths, $r=1.05,1.10,\ldots,9.95$.
- Unequal noise: $(0.1,0.2,0.7)$ and $(0.7,0.2,0.1)$; 94 strengths each. The grid has step $0.1$, plus $1.2,3,3.6,8.5$.
- Every grid uses $\lambda\in\{1,0.5,0.7,0.8,0.9\}$ and both low costs.
- Every grid uses all three menus and 45 costs: $0.0025,0.005,\ldots,0.1$, then $0.125,0.15,0.2,0.25,0.5$.
- Separate runs cover exact cost boundaries, exact presence boundaries, and the memos' additional noise examples.

This gives 495,450 menu–parameter–cost cases. The output retains each strict outcome and each conventional root found. It reports entry, ownership, entry rates, price-pool status, and all five belief flags.

| Noise | Cases | Cases with no strict equilibrium | Cases with no conventional root found |
|---|---:|---:|---:|
| Equal | 241,650 | 0 | 0 |
| $(0.1,0.2,0.7)$ | 126,900 | 13,884 | 3,376 |
| $(0.7,0.2,0.1)$ | 126,900 | 2,948 | 0 |

The maximum recorded support regret is $1.07\times10^{-13}$. The numerical acceptance tolerance is $2\times10^{-9}$. Entry equality uses an absolute roundoff allowance of $2\times10^{-13}$. These are diagnostics, not proof certificates.

The ordinary CLI ran with the stated economic inputs. Its output was examined as data. No test file, assertion, fixture, or test suite was used.

### Files and commands

All paths below lie under [scripts/V_discrete_check](../scripts/V_discrete_check/).

| File | Purpose |
|---|---|
| `solver.py` | Flow convolution, every price partition, action payoffs, entry regions, simplex and root search. |
| `compute.py` | Print-only CLI for a point, the full simplex, special boundaries, or a grid. |
| `algebraic.py` | Independent quadratic elimination on empty M3 cases. |
| `memo_cases.py` | The exact memo examples, auction quadrature, and explicitly changed-rule examples. |
| `summarize.py` | Print compact outcomes and strength intervals from the grid files. |
| `equal_sweep.jsonl` | Full equal-noise output. |
| `up_sweep.jsonl`, `down_sweep.jsonl` | Full unequal-noise output. |
| `full_simplex.jsonl` | Counts and posterior calculations across both full strategy simplices. |
| `special.jsonl`, `memo_cases.jsonl` | Exact boundaries, extra pools, belief examples, and memo-specific calculations. |
| `up_empty_resultants.jsonl` | Second calculation for all 3,376 empty conventional cases. |
| `summary.jsonl` | Compact totals, benchmark outcomes, and consecutive strength-grid intervals. |
| `equilibria.html` | Interactive equal-noise viewer at $k=0.02$, with presence and low-cost controls. |
| `receipt.json` | Final source and output hashes, file sizes, and completion records. |

Example consumer commands, from the repository root:

```bash
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py point --r 3 --lam .8 --k .02 .05
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py simplex
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py sweep --noise equal --jobs 6
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py sweep --noise up --rstep .1 --jobs 3
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py sweep --noise down --rstep .1 --jobs 3
.venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/memo_cases.py
```

Each main run prints its grid, tolerances, software versions, and source hashes. Detailed point rows include the price partition, both posterior notions, all prices, and every action payoff. Grid rows group off-path variants by their on-path outcome. Exact-threshold continua have sample rows plus their defining equations above; a finite sample is not the whole continuum.

The viewer was opened through its web interface. Both low-cost settings displayed the computed values at $r=3,\lambda=0.8$. The original-cost view showed both M3 outcomes. The low-cost view showed one M3 outcome, with entry $0.5$.

## 6. Open issues and risks

1. The strict calculation is exhaustive over strategies after dominance and over all price partitions. The general conventional mixed calculation is numerical.
2. The root search uses a fine mesh, every entry region, quadratic edge roots, and local interior roots. It is not an algebraic completeness certificate on every nonempty grid case.
3. The independent resultant calculation covers all empty conventional cases. Finite precision still limits any universal nonexistence claim.
4. The grid does not cover every positive noise law or every value of the primitives. Several general claims therefore rest on the displayed algebra, not the grid.
5. An Intuitive-Criterion completion must be distinguished from a uniquely forced belief. No separate formal D1 proof for the whole price-feedback game is claimed.
6. Both tie rules must accompany any equilibrium table. Investor mixtures and challenger mixtures are different changes to the model.
7. A local stake deviation is not a complete equilibrium calculation with a stake. That larger model remains outside this verifier's scope.
8. The quoted mixed-rule interval endpoints in sell Claim 11(d), and the other papers' equilibrium theorems, remain NOT CHECKED.

## 7. Recommendation

1. Keep the one-directional cutoff and benchmark calculations. State their price and tie assumptions beside the result.
2. Add the strict M3 price-pool example in Section 3.5 before any claim of unique entry with uncertain presence.
3. Replace “the floor is necessary for price sufficiency” with a sufficient-condition statement.
4. Label the presence window as a pure-profile result. Use its exact lower endpoint under entry at indifference.
5. Keep conventional investor mixtures and challenger mixtures in separate tables.
6. State the later costly-entry ceiling. State separately whether the low-cost floor survives there.
7. Treat the broad mixed-strategy output as numerical evidence. Obtain a full algebraic or interval certificate before a global uniqueness claim.

## 8. Plain summary

The simple buy-only and sell-only models pass the main numerical check. They share one trade cutoff under equal noise. At the original benchmark, entry is 0.25, then one third, then one third. It does not return at the paper's third strength. The costly challenger stops only after incumbent strength exceeds about 7.97. Entry then falls below 0.25 because cheap preparation also fails after clearly bad news.

A lower cheap cost restores the entry floor. It does not restore the earlier costly-entry ceiling.

The two-sided model needs more care. With an investor present 80% of the time, two price schedules support the same full trades at the benchmark. One schedule hides two low flows behind the same zero-entry price. Entry is 0.4167 there, compared with 0.4667 in the other schedule. Every trade is strictly optimal, so this difference does not depend on a tie or an off-path belief.

Mixed strategies add further outcomes if indifferent investors may trade. The prescribed rule forbids those mixtures. Some unequal-noise examples then have no equilibrium. A separate challenger tie rule can also affect existence.

The author can retain the main one-directional result. The author should narrow the uniqueness language, state both tie rules, and add the price-pool example.
