# X_C9. Independent check of C9: unequal noise, investor and challenger mixing

## 1. Scope

- **Memo under check:** `memos/C9_unequal_mixing.md` (file time 21 October 2026, 18:03 UTC).
  Its scripts are in `scripts/C9_unequal_mixing/`.
- **Paper:** Proposition 3 and Section 4.3 of `main.tex` at commit
  `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`; Appendix A.8 for the benchmark vector.
- **Base model, as C9 uses it:** the three-point model with buy-only orders $q\in\{0,1\}$.
  The noise is $Z\in\{-1,0,1\}$ with $(z_-,z_0,z_+)=(u,v,w)$. C9's example has $(2/5,2/5,1/5)$.
- **Parameters of the example:** $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_H=6$, $c_L=0$, $k=1/50$,
  $\lambda=1$, $\pi=1/2$, and $r\in I=[63/40,317/200]=[1.575,1.585]$.
- **Equilibrium concept, as in C9:** the price is $P(x)=\mathbb E[V_T\mid x]$. The challenger sees the
  price and its cost. Each investor deviation is evaluated against fixed price and entry schedules.
- **Tie rules, as in C9:**
  - the investor may mix when a purchase earns exactly zero;
  - the high-cost challenger may mix when $B_r(\mu)=c_H$.

  The paper instead lets an indifferent challenger prepare. The earlier discrete work let an
  indifferent investor choose zero.
- **Off-path rule, as in C9:** under no trade, the unused flow $X=2$ gets posterior one.
  The market maker and the challenger share this belief.
- **Method:**
  1. I derived each claim again (Section 3).
  2. I wrote `scripts/X_C9_check/check_c9.py` from scratch, before I read the author's code.
     It uses `fractions.Fraction` only and prints its results to `output.txt`.
  3. After that, I reran the author's `certificates.py` into `scripts/X_C9_check/author_rerun/`.
     `compare_author.py` compares its CSV with my values (`compare_output.txt`).
- **Commands** (repository root):
  - `bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C9_check/check_c9.py`
  - `.venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C9_check/compare_author.py`
- **Outside this check:** the items of C9 Section 4 other than Proposition 3 and the Proposition 2(iii)
  ceiling. I did not explore beyond what the verdicts need.

## 2. Verdict table

| # | Claim (label in C9) | Verdict | Evidence |
|---|---|---|---|
| 1 | An equilibrium exists for every admissible parameter vector when both sides may mix, under the stated completion (analytical) | CONFIRMED | Every step of the fixed-point proof holds (§3.1). The completion is essential: under a passive or adverse off-path belief, an equal-noise economy in C9's domain has no equilibrium. An exact random sweep of 1,500 economies finds no empty case. |
| 2 | Every $r\in[1.575,1.585]$ has exactly three outcomes: no trade and two informative equilibria (analytical) | CONFIRMED | My own derivation excludes other supports, other price partitions and challenger mixing at other prices (§3.2). Exact enumeration at 101 strengths finds the same three outcomes. The count holds for every common off-path belief. |
| 3 | Exact entry $0.526900<0.535188<0.543596$ on one informative branch (computer-assisted) | CONFIRMED | Every fraction reproduces exactly: $\beta_A$, $\mathsf E_A$, $U_L(1)$, preparation margins, entry differences and no-trade payoffs (§3.3). |
| 4 | Challenger mixing repairs an explicit existence gap found by the earlier verifier; interior purchase probabilities give an endogenous information intensity (analytical) | CONFIRMED WITH CORRECTION | The gap of Proposition C9.5 and its repair reproduce exactly. But this gap is C9's own construction. The earlier verifier's tie-rule gaps lie in the two-sided and sell-only menus, outside C9's theorem. C9's own text says so (§3.4). |
| 5 | Entry falls on the other informative branch across the same strengths (computer-assisted) | CONFIRMED | Exact entry $0.525157>0.520148>0.515255$. Entry on this branch also falls at all 101 grid strengths (§3.5). |
| 6 | The model does not recover the paper's partial short sale | CONFIRMED | True by construction: the menu has no sale. The analog is a purchase probability at indifference (§3.6). |
| — | The memo's numbers match its scripts' outputs | CONFIRMED | The rerun reproduces `summary.csv` and `flows.csv` byte for byte. The receipt hashes match. All 99 compared fields equal my values (§3.8). |
| — | C9's comparison with Proposition 3 (its Section 4) | CONFIRMED WITH CORRECTION | Correct as far as it goes. It omits four differences (§3.7). |

## 3. Derivations and evidence for each claim

### 3.0 Common reduction (own derivation) and the design of the check program

Let $\alpha=\lambda\beta$, where $\beta$ is the high-quality purchase probability. At flow $x$, write $\mu_x$ for
the posterior and $e_x$ for total entry. With $V_j(x)=t_0+e_x(t_j-t_0)$, the competitive price is
$P_x=\mu_xV_H(x)+(1-\mu_x)V_L(x)$. Hence

$$
V_H(x)-P_x=e_x\Delta(1-\mu_x)\ge0,\qquad V_L(x)-P_x=-e_x\Delta\mu_x\le0 .
$$

A low-quality purchase earns at most $-k<0$ under every belief. So $\beta_L=0$ in every equilibrium.

A purchase moves flow $z$ to $z+1$. Flow 2 has posterior one whenever a purchase reaches it, so its
residual is zero. With $\pi=1/2$ the gross purchase payoff is

$$
K(\alpha;e_0,e_1)=\Delta\left[\frac{uv\,e_0}{2v+\alpha(u-v)}+\frac{vw\,e_1}{2w+\alpha(v-w)}\right].
$$

This is C9's equation (1). My program uses it only to locate roots. Every check recomputes
$U_H(1)=\sum_z n(z)[V_H(1+z)-P_{1+z}]-k$ directly from the prices.

The program `check_c9.py` works as follows:

1. **Auction objects.** It computes $t_0,t_H,t_L,g_H,g_L$ as exact means over $R\sim U[0,r]$ from the
   auction rules. The midpoint rule is exact on each affine piece. At the three strengths, the
   results equal the paper's equation (4).
2. **Enumeration.** It finds the points $\alpha_0,\alpha_1$ where $\mu_0$ or $\mu_1$ equals
   $\tau=(c_H-g_L)/(g_H-g_L)$. On each open interval between them, it solves the quadratic
   $kL_0L_1-aL_1-bL_0=0$ exactly. At each threshold it tests $K^-\le k\le K^+$. At the endpoints it
   tests $K^-(0)\le k$ and $K^+(\lambda)\ge k$.
3. **Candidate checks.** For each candidate it builds the prices, groups equal prices, recomputes the
   pooled Bayes posterior, tests the challenger's choice at that posterior, and computes $U_H(1)$,
   $U_L(1)$, $\mathsf E$ and $\mathsf O_H$.

### 3.1 Claim 1: existence (Proposition C9.1)

**Step-by-step check of the proof.**

1. *Reduction.* The game reduces to $(\beta,e_0,e_1)$. Flows $-1$ and $2$ do not enter $K$: a purchase
   never reaches flow $-1$, and flow 2 has zero residual. Correct.
2. *Values.* $\mathcal X=[0,1]\times[\rho,1]^2$ is compact and convex. The investor's best-response
   correspondence $R$ and the entry correspondences $E_0,E_1$ have nonempty, convex, compact values. Correct.
3. *Closed graph.* With $u,v,w>0$, $D_0=(2-\alpha)v+\alpha u>0$ and $D_1=(2-\alpha)w+\alpha v>0$. So $K$ and
   $\mu_0,\mu_1$ are continuous. $S_r$ is the sign correspondence of the continuous map
   $\mu\mapsto B_r(\mu)-c_H$. Both correspondences have closed graphs. Correct.
4. *Fixed point.* Kakutani's theorem applies. Correct.
5. *Prices.* $S_r$ is monotone, so $\mu_y>\mu_x$ implies $e_y\ge e_x$. With $a_L=t_L-t_0>0$,

   $$
   P_y-P_x=e_y\Delta(\mu_y-\mu_x)+(e_y-e_x)(a_L+\Delta\mu_x)>0 .
   $$

   Equal prices therefore occur only for equal $(\mu,e)$. A flow-by-flow entry rate is thus a valid
   strategy that depends on the price only. Correct. At the three strengths,
   $a_L=53/126,\ 133/316,\ 267/634>0$.
6. *Zero noise probabilities.* A newly reachable purchase flow has $f_L=0$, posterior one and zero
   residual. The conventions $A=0$ when $v=0$ and $C=0$ when $w=0$ follow. Correct.
7. *General prior.* The formula
   $K_r=\Delta(1-\pi)[uve_0/(v+\pi\alpha(u-v))+vwe_1/(w+\pi\alpha(v-w))]$ is correct. Section [G] of the
   output confirms it exactly against first principles at $(\pi,\alpha)=(1/3,2/7)$ and $(4/5,5/6)$.

**The role of the off-path completion.**

- With $u,v,w>0$, only flow 2 can be unused, and only at $\alpha=0$.
- For $\alpha>0$, flow 2 is on path with posterior one. The completion gives the same value at
  $\alpha=0$. So $K$ is continuous at $\beta=0$. This continuity gives $R$ its closed graph at $\beta=0$.
- A common belief $\nu<1$ at flow 2 adds $w\,e(\nu)\Delta(1-\nu)>0$ at $\alpha=0$ only. The purchase
  payoff then drops at $\beta=0^+$, and existence can fail.
- **Example (output section [F]).** Take equal noise $(1/3,1/3,1/3)$, $r=3$, $c_H=6$ and $k=7/100$.
  Then $\tau=141/200$, so entry is $\rho$ at flows 0 and 1 for every $\alpha$. For $\alpha>0$,
  $K=\rho\Delta/3=1/18<k$, so no positive purchase probability is optimal.
  - Under the completion, no trade holds.
  - Under $\nu=1/2$, a deviation earns $\rho\Delta/2-k=1/12-7/100>0$.
  - Under $\nu=0$, it earns $2\rho\Delta/3-k=1/9-7/100>0$.

  Under either of the last two beliefs, this economy has **no** equilibrium, even when both sides may mix.
  Here $k$ lies in $(K,3K/2)$ with $K=\rho\Delta/3$. The ledger's coordinator notes report the same
  passive-belief window from memo A1; this example is an independent instance (A1 not checked here).
- The completion is not arbitrary. It is the limit of the on-path beliefs at flow 2. A low-quality
  purchase is strictly dominated under every belief. So dominance and the Intuitive Criterion put
  posterior one on flow 2 whenever they restrict that belief. The theorem therefore gives an
  equilibrium that passes these refinements.

**Brute force (numerical diagnostic in exact arithmetic).** Output section [H] draws 1,500 economies with
seed 20261021: $r\in(1,10)$, positive noise, $\pi\in\{0.1,\dots,0.9\}$, $\lambda\in\{0.1,\dots,1\}$,
$\tau\in(0,1.2)$ and $k\in(0,\Delta)$. With both mixtures, each economy has at least one equilibrium.

The label "analytical" is deserved.

### 3.2 Claim 2: exactly three outcomes on $I$

**Own derivation.** Fix $r\in I$.

1. *Investor types.* $\beta_L=0$ (Section 3.0).
2. *Price partitions.* $c_L=0<g_L$, so $e\ge\rho>0$ at every price. Equal prices occur only for equal
   $(\mu,e)$, and no zero-entry pool exists.
   - At $\alpha=0$, flows $-1,0,1$ share posterior $1/2$ and entry $\rho$. They form one price.
   - At $\alpha>0$, $\mu_{-1}=\frac{1-\alpha}{2-\alpha}<\frac12=\mu_0<\mu_1=\frac{1+\alpha}{2+\alpha}<1=\mu_2$.
     So there are four prices.

   No other partition exists.
3. *Where the challenger can mix.* On $I$, $B_r(1/2)\le4.685615<6$ and $g_H\ge9.128636>6$, so
   $1/2<\tau<1$. Flows $-1$ and $0$ have $\mu\le1/2<\tau$. Flow 2 has $B=g_H>c_H$. Only flow 1 can sit
   at $\tau$, and only at $\alpha_T=(2\tau-1)/(1-\tau)$.
4. *Investor.*
   - On $[0,\alpha_T)$: $K_F(\alpha)=\Delta[1/20+1/(10(2+\alpha))]\le\Delta/10<k$, because $\Delta<1/5$.
     No purchase probability in this range is optimal.
   - On $(\alpha_T,1]$: $K_A(\alpha)=\Delta[1/20+2/(5(2+\alpha))]$ strictly decreases. It equals $k$ only at
     $\alpha_A$.
   - Full purchases fail: $K_A(1)=11\Delta/60<k$. At $r=317/200$ the margin is only
     $k-K_A(1)=527/2536000\approx2.1\times10^{-4}$, but it is exact.
5. *At $\alpha_T$.* Investor indifference fixes $e_1=(k/\Delta-1/20)/[(2/5)(1-\tau)]$. This lies in
   $(\rho,1)$ because $K_F(\alpha_T)<k<K_A(\alpha_T)$. The right inequality is $\alpha_T<\alpha_A$.
6. *Order of the roots.* $\alpha_T<\alpha_A$ is equivalent to $\mu_1(\alpha_A)>\tau$. I confirmed the identity
   $B_r(\mu_1(\alpha_A))-6=P(r)/[80r(r-1)^2]$ by exact evaluation at eight strengths; a quartic numerator
   needs five. Also $P(63/40)=32763/102400$, and the bound $P'\ge2511/50$ on $[3/2,8/5]$ holds term by
   term. So $P>0$ on $I$.

Hence the outcomes are exactly: no trade; the threshold mixture $(\alpha_T,\sigma_T)$; and the interior
mixture $\alpha_A$.

**Brute-force evidence** (output section [C.3]). Exact enumeration at $r=63/40+j/10^4$, $j=0,\dots,100$,
gives exactly these three outcomes at every point. Every outcome passes the price-group, Bayes,
challenger-optimality and payoff checks.

**Two additions.**

- *The count does not depend on the completion.* With a common belief $\nu$ at flow 2, a no-trade
  deviation earns at most $\Delta[(u+v)\rho/2+w\max(\rho,1-\tau)]-k$. This is $-0.002110$ at $r=63/40$
  and $-0.001607$ at $r=317/200$. Both $\Delta$ and $\tau$ rise with $r$, so a uniform bound on $I$ is
  $\Delta(317/200)[1/10+(1-\tau(63/40))/5]-k=-0.001599<0$. For $\alpha>0$ no flow is unused.
  The enumeration with $\nu=1/2$ also returns the same three outcomes.
  - No trade could fail only if the market maker and the challenger held different beliefs at
    flow 2 (deviation payoff $+0.0115$ at $r=63/40$, $+0.0124$ at $r=317/200$). Such split beliefs violate the consistency condition of
    sequential equilibrium, because the market maker and the challenger both condition on the event $X=2$.
- *Under the paper's tie rule, the count is two.* If an indifferent challenger must prepare, $K$ jumps at
  $\alpha_T$ from $K_F<k$ to $K_A(\alpha_T)>k$. The threshold branch then disappears. The enumeration
  gives no trade and the interior branch at all 101 strengths.

The author's script evaluates the three closed-form schedules only. It does not search for other
equilibria. The word "exactly" therefore rests on the proof, which this check confirms.

### 3.3 Claim 3: certificates on the upward branch (A)

| $r$ | $\beta_A$ | $\mathsf E_A$ | $U_L(1)$ | $B_r(\mu_1)-c_H$ | no-trade $U_H(1)$ | equal to C9 |
|---|---|---|---|---|---|---|
| $63/40$ | $1258/1487$ | $1567/2974\approx0.526900$ | $-529/7200$ | $10921/1421952$ | $-479/50400$ | all |
| $79/50$ | $2090/2319$ | $4137/7730\approx0.535188$ | $-5887/79000$ | $3479731/53151200$ | $-739/79000$ | all |
| $317/200$ | $35450/37031$ | $201299/370310\approx0.543596$ | $-95823/1268000$ | $187972799/1542902400$ | $-11671/1268000$ | all |

- $U_H(1)=0$ exactly at all three points. The entry vector is $(1/4,1/4,1,1)$.
- $\mathsf O_H=\mathsf E_A-1/5$ holds exactly.
- The entry differences are $47632/5747255$ and $240688/28624963$, as in C9.
- With $\lambda=49/50$ at $r=317/200$: $\beta_A=1772500/1814519$ and $\alpha_A=35450/37031$, as in C9.

The label "computer-assisted" is deserved. In fact the whole branch is analytical, by C9's
equation (6) and the bounds on $I$. The certificates are exact rationals because $u=v$ makes the
investor's equation linear in $\alpha$.

### 3.4 Claim 4: the repaired gap and the information intensity

**(a) The gap of Proposition C9.5** (output section [E]). The example reproduces exactly:
$\Delta=2/3$, $\tau=2/5$, and $B_3(1/2)=103/24>c_H=83/24$.

- If an indifferent challenger must prepare, the gross payoff rises from $2/15$ at $\alpha=0$ to $11/75$ at
  $\alpha=1/2$. Just above $1/2$ it drops to $13/150$ and rises to $11/120$ at $\alpha=1$. The cost
  $k=1/10$ lies in the jump.
- Under "must prepare" and under "must not prepare", no equilibrium exists. No trade fails under every
  off-path belief: the completion already gives the smallest flow-2 residual (zero), and $K(0)=2/15>k$.
- When both sides may mix, exactly one equilibrium exists: $\beta=1/2$, posteriors $(1/3,1/2,2/5,1)$,
  entry $(1/4,1,5/12,1)$, $\sigma_1=2/9$, $U_H(1)=0$, $U_L(1)=-53/90$, $\mathsf E=143/240$ and
  $\mathsf O_H=83/240$. This matches C9.

**(b) C9's "analytical qualification."** If $B_r(1/2)<c_H$, investor mixing alone suffices. The argument is
correct. The posteriors at flows 0 and 1 start at $1/2<\tau$ and move monotonically, so each
preparation jump raises $K$. Under either pure tie rule, $K-k$ has only upward jumps. A sign change from
positive to negative then has a zero at $s=\sup\{\alpha:K(\alpha)\ge k\}$. The sweep agrees:

- 869 draws with $B_r(\pi)<c_H$, challenger must prepare at indifference: no empty case;
- 631 draws with $B_r(\pi)\ge c_H$: 6 empty cases. With both mixtures, all 6 have an equilibrium.

**(c) Attribution.** The earlier verifier (`audit/alex_meeting_2026_10_21/memos/V_discrete_check.md`,
Section 3.7) reports these existence gaps:

- 3,376 numerical empty cases under noise $(0.1,0.2,0.7)$, all in the two-sided menu, with a challenger
  that must prepare at indifference;
- a sell-only example with $(c_L,c_H,r,k)=(2.5,7,3,0.03)$ and noise $(0.2,0.6,0.2)$, where the low-cost
  challenger mixes. The earlier verifier already showed that both changed tie rules restore an
  equilibrium there;
- buy-only and sell-only gaps caused by the investor rule "choose zero at indifference". Investor
  mixing alone repairs these.

C9's theorem covers only the buy-only menu with $c_L=0$. It repairs none of the challenger-tie gaps
above. Its Proposition C9.5 is a new buy-only gap at $c_H=83/24$; the earlier sweep found no buy-only
challenger-tie gap. C9 states this correctly ("Analytical qualification", end of its Section 3). The
claim as worded in the check request needs this correction.

**(d) Information intensity.** Both informative branches have an interior purchase probability.

- Branch A: $\beta_A$ solves the investor's zero-profit condition. It depends on $k$ and $\Delta$.
  Preparation is pure at every on-path price.
- Branch T: $\alpha_T$ solves $\mu_1(\alpha_T)=\tau$. It depends only on the noise law and $\tau$, not on $k$.
  The cost $k$ then fixes $\sigma_T$.

In both cases, the intensity is a mixing frequency at indifference. It is not a strictly optimal order size.

### 3.5 Claim 5: entry on the threshold branch (T)

| $r$ | $\beta_T$ | $\sigma_T$ | $\mathsf E_T$ |
|---|---|---|---|
| $63/40$ | $13249/15791$ | $16652273/16706878$ | $1108369107487/2110546483984\approx0.525157$ |
| $79/50$ | $20791/24734$ | $121328033/124807764$ | $21409248607791/41159936463680\approx0.520148$ |
| $317/200$ | $5303/6297$ | $490344541/517197798$ | $22374377953091/43423927120080\approx0.515255$ |

- Every value equals C9's summary file. At each point, $U_H(1)=0$, the flow-1 preparation margin is
  exactly zero, and $U_L(1)<0$.
- The differences are about $-0.005010$ and $-0.004893$.
- $\mathsf E_T$ also falls strictly at all 101 grid strengths. At the spot checks $r=1.6,1.7,1.86$ it
  continues to fall: $0.5012$, $0.4278$, $0.3552$.

The label "computer-assisted" is deserved for the three points.

### 3.6 Claim 6: no partial short sale

The claim holds by construction. The menu $\{0,1\}$ contains no sale, and a low-quality purchase is
dominated. In the paper, the low type stops at an interior short $-v_j$. That size is the unique root of a
strictly concave profit, and the high type buys fully. In C9, the high type mixes over $\{0,1\}$ at zero
profit, and the low type abstains. C9 also keeps full revelation at flow 2, which the Laplace bound
$M<1$ excludes.

### 3.7 Comparison with Proposition 3

| Part of Proposition 3 | Paper (pinned commit) | C9 | Reproduced? |
|---|---|---|---|
| Coexistence with no trade | Each of $r=1.55,1.60,1.65$ admits no trade with entry $\rho$ | Every $r\in I$ admits no trade with entry $1/4$; analytical; for every common off-path belief | Yes, on a whole interval |
| Several informative equilibria | One certified equilibrium per strength; other families appear only as numerical continuations | Two informative outcomes at every $r\in I$, and no others | Yes, and the set is complete on $I$ |
| Entry ordered upward across strengths | Disjoint enclosures $0.545053<0.548756<0.551361$ over a span of $0.10$ | Branch A only: strictly upward on $I$ (analytical); $0.526900<0.535188<0.543596$ over a span of $0.01$. Branch T falls. | Partly |
| Certificate method | Interval enclosures of roots, endpoint signs, a derivative bound | Exact rational schedules at three points, and an analytical proof for all of $I$ | Yes, in exact form |
| Order pattern | $(q_H,q_L)=(1,-v_j)$ | $(\beta_A,0)$ with $\beta_A\in(0,1)$ | No |
| Type of optimality | Strict: the low type's interior size is the unique optimum; full purchase dominates | Indifference: the investor mixes at zero profit | No |
| Challenger tie rule | An indifferent challenger prepares | Branch A survives this rule; branch T needs challenger mixing | Partly |
| Primitives | Laplace noise, $b=2$; orders in $[-1,1]$; $c_L=1$ | Noise $(2/5,2/5,1/5)$; $q\in\{0,1\}$; $c_L=0$ | A different economy |

**Width of the upward window** (exact values; outside $I$, the structure rests on the formulas of §3.2
and exact spot checks in output section [D]):

- Branch A exists for $r\in(r_{lo},r_{up}]$.
  - $r_{lo}\approx1.574344841$ is the root of $P$ in $(3/2,63/40)$. There, branches A and T merge.
  - $r_{up}=(122+\sqrt{2784})/110\approx1.588760$ is where $\alpha_A=1$, that is, $\Delta=6/55$.
- For $r\in[r_{up},2.06)$, full purchases form an equilibrium, because $K_A(1)=11\Delta/60\ge k$ and
  $\mu_1(1)=2/3>\tau$. Their entry is $11/20=0.55$ at every such $r$.
- No trade coexists with full purchases up to $r=(12+\sqrt{44})/10\approx1.863325$, where $\Delta=1/5$.
- At the spot checks $r=1.570$ and $1.574$, the enumeration finds only no trade.

So upward ordered entry holds on a window of width about $0.0144$. The qualitative pattern resembles the
paper's Figure 2: an informative branch with upward entry appears before no trade ends, and full orders
then coexist with no trade. But Figure 2 is a numerical continuation. Proposition 3 itself certifies
only three points.

### 3.8 Parameters, rules, labels, and numbers against scripts

- **Noise vector.** C9 uses $(z_-,z_0,z_+)=(u,v,w)=(2/5,2/5,1/5)$ in the memo, the CSV and the code
  (`Parameters.noise`, used as $n(-1),n(0),n(1)$). The order is the same everywhere. The noise has mean
  $-1/5$. Because $u=v$, flow 0 carries no information ($\mu_0\equiv1/2$).
- **Other parameters.** They match Section 1 and the paper's benchmark, except $c_L=0$ (team decision)
  and the noise law.
- **Concept and rules.** C9's Section 2 states the equilibrium concept, the off-path rule and both tie
  rules. The paper also lets the investor mix ("The investor can mix", Section 2.4).
- **Labels.** All are deserved. One small exception: the paragraph "Analytical robustness" (small changes
  of the noise law) is a proof sketch through the implicit function theorem and compactness. The strict
  margins it needs do hold on $I$. "Analytical (sketch)" is the more exact label.
- **Numbers against scripts.**
  - The rerun into `author_rerun/` reproduces `summary.csv` and `flows.csv` byte for byte. Its `run.txt`
    differs only in the line that names the output path.
  - `receipt.json` lists SHA-256 values `63755ca4…` (`summary.csv`), `70d9d661…` (`flows.csv`) and
    `9a8beda9…` (`certificates.py`). They equal the current files.
  - Every number in C9 equals the corresponding CSV entry. My values equal all 99 compared fields
    (11 rows, 9 fields each).
  - The author's script prints the preparation margins but does not test the challenger's choice, and it
    does not enumerate equilibria. C9's labels are consistent with this.

## 4. Errors found and corrections

I found no arithmetic error and no invalid step in a proof. Three corrections apply.

1. **Claim 4, attribution (as worded in the check request).** The repaired gap (Proposition C9.5) is C9's
   own construction. It is not a gap that the earlier verifier found. The earlier verifier's
   challenger-tie gaps stay outside C9's theorem: the two-sided menu (3,376 numerical cases) and the
   sell-only example with $c_L=2.5$. C9's own text is correct on this point.
2. **The comparison with Proposition 3 (C9 Section 4).** "Ordered informative equilibria … are recovered"
   needs four qualifications:
   - the order holds on one branch only;
   - it holds on a window of width about $0.0144$; above it, full purchases give flat entry $0.55$;
   - the interior object is a mixture at indifference, not a strictly optimal order size;
   - branch T needs the changed challenger tie rule.
3. **Existence depends on the completion.** C9 says that its theorem does not cover arbitrary off-path
   rules. It should add that this dependence is real. Under a passive or adverse belief, some economies
   in its domain have no equilibrium (§3.1). So the brief's warning for equal noise stays true: C9 does
   not remove the need for the directional belief.

## 5. What the original memo should change

1. **Section 4, Proposition 3 item.** Add:
   - the window $(1.574345,1.588760]$ of branch A;
   - the flat entry $11/20$ on full purchases above it;
   - the loss of the $(1,-v)$ pattern and of strict optimality;
   - the dependence of branch T on the challenger tie rule.
2. **Proposition C9.1 or Section 6.** Add the equal-noise example ($r=3$, $k=7/100$) that has no
   equilibrium under a passive or adverse belief. Say that the completion is the belief that dominance
   and the Intuitive Criterion select.
3. **Proposition C9.3.** Add two facts:
   - on $I$, the count of three holds for every common off-path belief (margin at least $0.0016$);
   - under the paper's tie rule, the count is two.
4. **Section 1 or the plain summary.** Add one sentence: C9.5 is a new gap, and the earlier verifier's
   gaps in the two-sided and sell-only menus stay outside this theorem.
5. **Labels.** Mark the noise-perturbation paragraph "analytical (sketch)", or write out its uniform margins.
6. **Section 5.** Say that `certificates.py` evaluates given schedules and does not enumerate. Cite an
   enumeration, such as this check's, for the count.

## 6. Plain summary

I checked memo C9 with my own derivations and my own exact-fraction program. I wrote the program before
I read the author's code. Every number in C9 reproduces exactly. The author's script reproduces its saved
files byte for byte.

The existence proof is correct. It needs the stated belief after an unused purchase flow. With a passive
belief, an equal-noise economy has no equilibrium. Standard refinements select the stated belief.

The count of exactly three outcomes for $r$ from 1.575 to 1.585 is correct. Other supports, price
partitions and mixing points are excluded. The count holds for every common off-path belief. If an
indifferent challenger must prepare, as in the paper, only two outcomes remain.

Entry rises on one informative branch and falls on the other, as C9 states. The upward branch exists
only on a window about 0.014 wide.

One claim needs a correction. The gap that challenger mixing repairs is C9's own example, not a gap from
the earlier check. C9 itself says this.

The model gives no partial short sale. It reproduces coexistence, several informative equilibria and
exact certificates. It does not reproduce the paper's order pattern or its strict optimality.
