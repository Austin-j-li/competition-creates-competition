# W2-ownership: Solver A

## Candidate 1: Research raises ownership relative to the same-incumbent no-research equilibrium

Angle: reformulate

Intuition: Research brings class H into the auction more often, even when a stronger incumbent makes winning harder. Compare the research equilibrium with the no-research equilibrium against the **same incumbent**: research always raises high-class ownership, and its proportional ownership advantage increases with the target-payoff spread. This preserves a statement about actual acquisitions while separating information production from the incumbent's direct displacement of challengers.

Formal statement: Maintain the ranked, reserve-admissible classes, independence assumptions and two-point preparation cost, with prior $1/2$. Fix $\rho,k,\beta,a,\bar\lambda$, with $0<\beta\le1/3$, and consider any auction at which the standard interior research branch exists: class H buys after successful research, class L abstains, only a purchase recruits, and $1/2<\tau<1$. Write its research intensity as $\lambda_R$, and its ownership as $O_H^R(F)$. There is also a zero-research equilibrium Z at the same $F$, with ownership $O_H^Z(F)=\rho W_H(F)/2>0$. Then

$$
\boxed{
\frac{O_H^R(F)}{O_H^Z(F)}
=1+\frac{1-\rho}{\rho}
 \left[\beta+(1-\beta)\lambda_R(\Delta(F))\right]>1.
}
$$

This multiplier is a strictly increasing function of $\Delta$. Thus it weakly rises along a first-order stochastic strengthening, and rises strictly between any two points on the branch at which the spread rises strictly. No condition on the path of $W_H$, on the shape of the class distributions, or on connectedness of the branch is needed. The corresponding unnormalised statement is pointwise: **research raises the probability that a class-H challenger acquires the target, holding the incumbent fixed.**

Derivation:

1. On this branch, $b=(1-\lambda_R)\beta$. Conditional purchase probabilities are $b+\lambda_R$ in H and $b$ in L. Consequently, class entry probabilities are

   $$
   e_H(\lambda)=\rho+(1-\rho)[\beta+(1-\beta)\lambda],
   \qquad
   e_L(\lambda)=\rho+(1-\rho)\beta(1-\lambda).
   $$

   Preparation is independent of $(\theta,R)$ conditional on class, so $O_H^R=W_He_H/2$. This independence is the same factorisation used in [A3, ownership proof](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A3_proposition2.tex:75).

2. The sale posterior on this branch is $1/2$, with entry $\rho$. Since class L abstains, its sale payoff must satisfy

   $$
   \rho\Delta/2-k\le0.
   $$

   At zero research all orders are liquidity orders, so all posteriors equal $1/2<\tau$, entry is $\rho$, and prices coincide. At those prices a hypothetical successful investor's correct order earns $\rho\Delta/2-k\le0$, a wrong-signed order earns at most $-k$, and abstention earns zero. Choose abstention after either class: it is allowed under IM and I0, including equality. The successful-research trading value is zero, so the best research choice is uniquely zero. This constructs Z as an equilibrium of the **same research game**. Compare [A5, Z construction](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A5_research.tex:141).

3. For $\lambda\in[0,1)$, let

   $$
   m_\lambda=\frac{\beta(1-\lambda)}{2\beta+(1-2\beta)\lambda},
   \qquad
   m_\lambda'=-\frac{\beta}{[2\beta+(1-2\beta)\lambda]^2}<0.
   $$

   Interior research satisfies $2a\lambda_R=\Delta m_{\lambda_R}-k$. The left side increases and the right side decreases in $\lambda_R$; for $\Delta>2k$ there is one root in $(0,1)$. Differentiating gives

   $$
   \frac{d\lambda_R}{d\Delta}
   =\frac{m_{\lambda_R}}{2a-\Delta m_{\lambda_R}'}>0.
   $$

   Dividing $W_He_H/2$ by $\rho W_H/2$ proves the multiplier formula, and

   $$
   \frac{d}{d\Delta}\left(\frac{O_H^R}{O_H^Z}\right)
   =\frac{(1-\rho)(1-\beta)}{\rho}
      \frac{m_{\lambda_R}}{2a-\Delta m_{\lambda_R}'}>0.
   $$

   Positivity of the denominator $O_H^Z$ is not an extra assumption: $\gamma=g_H-g_L>0$ implies $g_H>0$, which requires a positive chance that a prepared H challenger wins.

Conditions: Only the maintained model and the specified branch. In particular, $c_H$ remains the nonzero point of the two-point preparation-cost law. This compares equilibrium outcomes; it does not assert that the research equilibrium is selected uniquely. At a capped, purchase-only-recruitment equilibrium the same multiplier identity holds with $\bar\lambda$, but further widening of the spread leaves the multiplier constant until the order pattern changes.

Benchmark check: With the exact declaration $\beta=0.294655$, $a=1/40$, and $\bar\lambda=(\mathrm e-1)\beta/[1+(\mathrm e-1)\beta]\approx0.336121768915$, direct calculations give:

| Strength $r$ | Research $\lambda_R$ | $O_H^R$ | Same-incumbent $O_H^Z$ | Ownership multiplier |
|---:|---:|---:|---:|---:|
| 1.55 | 0.237901195 | 0.298421532 | 0.125000000 | 2.387372255 |
| 1.60 | 0.279037102 | 0.309302159 | 0.125000000 | 2.474417273 |
| 1.65 | 0.316683178 | 0.319259711 | 0.125000000 | 2.554077688 |

The supplied counterexample also satisfies the new claim: the multiplier increases from $6.927092489$ at $r=11$ to $7.070625861$ at $r=12$, although high-class ownership falls.

What is lost: This does not claim that actual high-class ownership rises across different incumbents. Crucially, **subtracting** the same-incumbent counterfactual does not remove the problem:

$$
O_H^R-O_H^Z
=\tfrac12(1-\rho)W_H(F)[\beta+(1-\beta)\lambda_R].
$$

The additive gain still contains $W_H(F)$. It falls from $0.134706647$ to $0.126471372$ in the known counterexample. The universally monotone object is the proportional advantage, not the absolute treatment effect.

## Candidate 2: Preserve the ownership level claim when strengthening does not displace class H

Angle: primitive condition

Intuition: Competition can raise the price paid by class H without changing which incumbent draws it beats. Under that separation, the information effect translates directly into more high-class acquisitions. The clearest sufficient restriction is that every class-H value exceeds every incumbent value on the path; the actual requirement is weaker, because class H's win probability need only stay constant and positive.

Formal statement: Suppose the incumbent strengthens along a path $F_s$, with fixed ranked classes and fixed preparation, trading and research primitives. Assume

$$
\boxed{
\operatorname*{ess\,inf}(\theta\mid H)
\ \ge\ \sup_s\operatorname*{ess\,sup}(R_s).
}
$$

Assume also that strengthening moves incumbent probability where the classes differ, in the precise sense that, for the compared strengths $s<t$,

$$
\int_p^\infty [F_s(y)-F_t(y)]D(y)\,dy>0.
$$

Then actual high-class ownership rises strictly between those strengths whenever both lie on the standard research branch. The support condition makes $W_H=1$; continuity of $F_s$ removes acquisition ties. The positive integral makes $\Delta_t>\Delta_s$, which makes $\lambda_{R,t}>\lambda_{R,s}$ and $e_{H,t}>e_{H,s}$.

More generally, replace the boxed condition by the following primitive restriction: **the incumbent CDF changes only at values to which $G_H$ assigns zero probability**, so

$$
F_t(\theta)=F_s(\theta)\quad G_H\text{-almost surely},
\qquad W_H(F_s)>0.
$$

This leaves $W_H$ constant, possibly far below one, and gives the same result.

Derivation: The exact comparison, without any smoothness, is

$$
\frac{O_H(F_t)}{O_H(F_s)}
=\underbrace{\frac{W_H(F_t)}{W_H(F_s)}}_{\text{direct displacement}}
 \underbrace{\frac{e_H(\lambda_{R,t})}{e_H(\lambda_{R,s})}}_{\text{information and entry}}.
$$

Therefore the exact necessary and sufficient condition for a strict level rise is

$$
\frac{W_H(F_t)}{W_H(F_s)}
>
\frac{e_H(\lambda_{R,s})}{e_H(\lambda_{R,t})}.
$$

On a differentiable path, the equivalent condition for a **positive local slope** is

$$
\boxed{
-\frac{W_H'(s)}{W_H(s)}
<\frac{(1-\rho)(1-\beta)}{e_H(s)}
  \frac{m_{\lambda_R}}{2a-\Delta m_{\lambda_R}'}\,\Delta'(s).
}
$$

The left side is the proportional loss of H's acquisition opportunities; the right side is the proportional expansion of H's entry. This is the natural economic trade-off if the author wants a broader condition than support separation.

To express the trade-off directly in the primitives, suppose differentiation under the integrals is valid and set $q_s(y)=-\partial_sF_s(y)\ge0$. Then

$$
-W_H'(s)=\int q_s(y)\,dG_H(y),
\qquad
\Delta'(s)=\int_p^\infty q_s(y)D(y)\,dy.
$$

Thus the displacement integral uses the probability mass of class-H values at the affected incumbent values, whereas the information integral uses the class-CDF gap. Class ranking does not bound the former by the latter. Support separation makes the displacement integral zero and leaves room for a strictly positive information integral. This explains why it is a substantive primitive condition rather than a consequence of stochastic dominance.

Conditions: The support restriction is sufficient, not necessary. Constant $W_H>0$ is itself sufficient and not necessary; even a declining $W_H$ is compatible with rising ownership when the exact trade-off holds. Strictness also requires a genuine spread increase: stochastic dominance by itself allows shifts in regions irrelevant to both classes. The two-point preparation law remains unchanged.

Benchmark check: The full benchmark path has $h=10$ and $r\le18/5$, so the support-separation margin is

$$
h-\max r=10-18/5=32/5=6.4.
$$

On the research branch the upper strength is approximately $1.677632834385$, so its support margin exceeds $8.322367$. Moreover,

$$
\Delta'(r)=\tfrac12(1-1/r^2)\ge11/72\approx0.152777778
\quad\text{for }r\in[6/5,18/5].
$$

The benchmark consequently has no displacement loss and a strictly positive information effect, with wide support slack. At $r=1.55,1.60,1.65$, the respective proportional ownership slopes are approximately $0.762376, 0.672661, 0.596877$ per unit of $r$.

How far from necessary: Two explicit calculations illustrate the distance.

- Keep point classes $h=10,\ell=1$, reserve $1/2$, and uniform incumbents. Set $c_H=2.4,\rho=0.05,k=2,\beta=0.2,a=0.025,\bar\lambda=0.9$. At $r=11$ and $11.1$, the research branch is strict: purchase-posterior margins are $0.0292742$ and $0.0283587$, with ample sale and cap slack. Although $W_H$ falls from $0.9090909$ to $0.9009009$, ownership rises from $0.125375072$ to $0.125486697$. Hence even a falling win probability need not overturn the entry effect.
- Constant $W_H$ need not be near one. Let $G_L=\delta_1$, $G_H=\tfrac12\delta_1+\tfrac12\delta_{10}$, $p=1/2$, and $R_s\sim U[s-0.1,s+0.1]$, comparing $s=2.9$ with $s=3$. Set $c_H=2,\rho=1/4,k=0.2,\beta=0.2,a=1,\bar\lambda=0.9$. Here half of class H always loses and half always wins: $W_H=1/2$. Since $\Delta=(s-1)/2$, $\gamma=(10-s)/2$, and $g_L=0$, research increases from $0.090286502$ to $0.097051151$, and ownership from $0.113542975$ to $0.114557673$. Recruitment margins are $0.0360166$ and $0.0344691$; the sale margins are $0.08125$ and $0.075$. This is an example of strengthening entirely inside a gap in the high-class value distribution.

What is lost: The original level claim is preserved on economically named paths, but it is not a theorem for arbitrary ranked classes and arbitrary incumbent strengthenings. If the theorem uses the simplest support condition, it excludes meaningful cases in which class H can lose; the exact finite comparison or local trade-off can be supplied as a broader extension.

## Candidate 3: Stronger incumbents improve the distribution of challengers who prepare

Angle: reformulate

Intuition: Research raises class H's entry probability and lowers class L's entry probability, because it replaces liquidity purchases in L with informed abstention. Thus stronger incumbents attract a better pool of prepared challengers even when the final number of high-class acquisitions falls. This is a statement about selection into competition, with no restriction on who eventually beats the incumbent.

Formal statement: With the same maintained assumptions and branch as Candidate 1, an increase in $\Delta$ strictly raises

$$
S_H:=\Pr(H\mid\text{challenger prepares})
=\frac{e_H(\lambda_R)}{e_H(\lambda_R)+e_L(\lambda_R)}.
$$

Consequently, the value distribution conditional on preparation shifts weakly upward in first-order stochastic dominance:

$$
G_{\mathrm{prepared}}(y)
=S_HG_H(y)+(1-S_H)G_L(y).
$$

Its mean increases strictly when the classes have a positive mean gap, as they do on the branch. Along an incumbent strengthening, low-class ownership $O_L=\tfrac12 e_LW_L$ weakly falls, and falls strictly if the spread rises strictly and $W_L$ at the stronger incumbent is positive.

Derivation: From the entry formulas,

$$
\frac{de_H}{d\lambda}=(1-\rho)(1-\beta)>0,
\qquad
\frac{de_L}{d\lambda}=-(1-\rho)\beta<0.
$$

The quotient rule gives

$$
\frac{dS_H}{d\lambda}
=\frac{(1-\rho)[\rho+(1-\rho)\beta]}{(e_H+e_L)^2}>0.
$$

Since $d\lambda_R/d\Delta>0$, the class-H share increases. For any two branch points with $S_{H,2}>S_{H,1}$,

$$
G_{\mathrm{prepared},2}(y)-G_{\mathrm{prepared},1}(y)
=-(S_{H,2}-S_{H,1})D(y)\le0.
$$

There is no within-class selection on $\theta$, because preparation occurs before its revelation and is independent of it conditional on class. This justifies the mixture formula. Finally, $e_L$ falls with the spread and $W_L=\mathbb E_LF_s(\theta)$ weakly falls with incumbent strength, so their product weakly falls.

Conditions: No additional restrictions beyond the original class ranking, independence, fixed primitives and the specified branch. All comparisons are on the set where that branch exists; no interval claim is required. Strict value-distribution improvement occurs where $D>0$, and strict mean improvement follows from the positive class-mean gap.

Benchmark check: At $r=1.55,1.60,1.65$, the H shares among prepared challengers are $0.587872001, 0.601795677, 0.614240663$. With point values $10$ and $1$, the corresponding mean prepared-challenger values are $6.290848010, 6.416161096, 6.528165964$. The known ownership counterexample also improves selection: its H share among entrants rises from $0.618748984$ to $0.625554720$.

What is lost: This replaces the ownership level by the composition and value distribution of the entering pool. The distinction is substantive: acquisition outcomes additionally select on the incumbent's value. In particular, the H share among **successful challengers** need not rise with strength, as the explicit example below shows.

## Importance of the weakness

The supplied counterexample is valid, with strict branch slack throughout the comparison. For point classes and $r>h=10$, direct integration gives

$$
g_L=\frac{\ell^2-p^2}{2r}=\frac{0.375}{r},\qquad
\gamma=\frac{h^2-\ell^2}{2r}=\frac{49.5}{r},\qquad
\Delta=9-\frac{49.5}{r},\qquad W_H=\frac{10}{r}.
$$

Using exactly $c_H=2.5,\rho=0.05,k=0.2,\beta=0.2,a=5,\bar\lambda=0.9$ yields:

| $r$ | $\Delta$ | $\tau$ | $\lambda_R$ | Total entry | $e_H$ | $W_H$ | $O_H$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 4.500000 | 0.547979798 | 0.139940295 | 0.279882984 | 0.346354624 | 0.909090909 | 0.157433920 |
| 12 | 4.875000 | 0.598484848 | 0.149383280 | 0.282574235 | 0.353531293 | 0.833333333 | 0.147304705 |

The purchase posteriors exceed the preparation thresholds by $0.096597324$ and $0.054062269$. Low-class abstention has payoff margins $k-\rho\Delta/2=0.0875$ and $0.078125$; cap slack exceeds $0.75$. On the entire interval, the purchase posterior is at least its $r=11$ value and the threshold is at most its $r=12$ value, leaving the conservative recruitment margin $0.046092273>0$. Thus this is not an endpoint or tie-rule artefact.

Ownership actually falls throughout the interval, not only between the displayed endpoints. For $11\le r\le12$, use $m\le1/2$, $2a-\Delta m'>2a=10$, $\Delta'=49.5/r^2$, and $e_H\ge0.24$. These give

$$
\frac{e_H'}{e_H}
\le \frac{0.76(1/2)(49.5/11^2)}{10(0.24)}
=\frac{57}{880}
<\frac1{12}
\le-\frac{W_H'}{W_H}.
$$

Numerically, research rises by $6.75\%$, total entry by $0.96\%$, and H entry by $2.07\%$, while H's conditional win probability falls by $8.33\%$. Ownership consequently falls by $6.43\%$, approximately one percentage point in levels.

The primitives are simple and economically intelligible, although they are not the benchmark calibration. The class values and reserve are unchanged. The incumbent support exceeds the high point value by only $10\%$ to $20\%$; that is a meaningful change in competitive overlap, not an exotic distribution. The low zero-cost probability $0.05$ and research coefficient $5$ differ substantially from the benchmark, and the trading cost is $2\%$ of the high value, compared with $0.2\%$ in the benchmark. However, realised research expenditure is only $0.048958$ to $0.055788$, about $0.49\%$ to $0.56\%$ of the high acquisition value. The cap is inactive with wide slack. There is no empirical calibration here that would establish which parameter vector is typical; the example demonstrates a structurally ordinary displacement effect on an open set of primitives.

For the economics, the weakness matters to a claim about **who acquires**, not to the information-production or entry mechanism. Research, total entry and selection toward H all improve in the counterexample. At each strength, the research equilibrium also produces much more high-class ownership than the same-incumbent no-research equilibrium. What fails is the inference from increased H participation to increased H acquisitions across different incumbents. Candidate 1 preserves an acquisition statement without restricting auction overlap; Candidate 2 retains the original ownership-level claim where the price and allocation effects are separated. Candidate 3 makes the quality-selection implication explicit.

## Other findings (errors in the manuscript, anything surprising)

1. **The current benchmark proposition is correct; the obstacle is its unrestricted generalisation.** [Proposition 4(a)](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/sections/05_research.tex:52) explicitly assumes the benchmark auction, and [its proof](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A5_research.tex:266) explicitly invokes $h>r$ and $W_H=1$. A general theorem should retain $W_H$ or use Candidate 1. This is not a counterexample within the proposition's currently stated benchmark domain.

2. **The related robustness results already distinguish the relevant cases.** [Proposition 2](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/sections/04_equilibrium_results.tex:35) and [A.4](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A6_robustness.tex:92) state the exact ownership inequality. [A.5's construction](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A6_robustness.tex:180) obtains it by continuity of $W_H$, so its ownership claim survives. The ownership formula following [A.7](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A6_robustness.tex:481) uses $h>r_1$; a general extension must write $\tfrac12 e_HW_H(F_1)$, rather than $e_H/2$. The same-incumbent normalisation also cancels $W_H$ there whenever the baseline class-H entry is $\rho$. None of these observations calls for changing the baseline two-point cost law.

3. **A conditional acquisition share is not an unconditional repair.** The share of H among successful challenger acquisitions is

   $$
   \Pr(H\mid\text{challenger wins})
   =\frac{e_HW_H}{e_HW_H+e_LW_L}.
   $$

   Its odds equal $ (e_H/e_L)(W_H/W_L)$ at prior $1/2$. The first factor rises on the branch; stochastic ordering places no corresponding lower bound on the second factor.

   Here is a fully specified counterexample. Keep $h=10,\ell=1,p=1/2$, prior $1/2$, $\rho=0.05,k=0.2,\beta=0.2,a=5,\bar\lambda=0.9$, and set $c_H=2.7$. Let the continuous incumbent distribution be

   $$
   R_z\sim\tfrac12 U[0,1]+\tfrac12 U[z-0.1,z+0.1],
   \qquad z\in\{9.8,10.2\}.
   $$

   Raising $z$ is an incumbent first-order stochastic strengthening. The spread increases from $4.4$ to $4.5$, while $g_L=0.1875$ throughout and $\gamma$ falls from $4.6$ to $4.5$. Thus $\tau$ rises from $0.546195652$ to $0.558333333$, and research rises from $0.137359005$ to $0.139940295$. The purchase-posterior margins are $0.096170246$ and $0.086243788$, and the low-sale margins are $0.09$ and $0.0875$, so both are strict interior research-branch equilibria. Yet $W_L=1/2$ throughout and $W_H$ falls from $1$ to $1/2$. The H share among successful challengers falls from $0.763038931$ to $0.618748984$, even as its share among prepared challengers rises from $0.616865761$ to $0.618748984$.

   This also defeats a claim about the H share among **all completed sales**, including incumbent wins: $F_z(p)=1/4$ is constant, so the total-sale probability $1-F_z(p)(1-\mathrm{Entry})$ rises with entry, while H ownership falls from $0.172196422$ to $0.086588656$. At a fixed incumbent, by contrast, research does raise the H share among successful challengers relative to Z when both classes can win, because the ownership odds are multiplied by $e_H/e_L>1$. The distinction between within-incumbent and cross-incumbent comparisons remains essential.

4. **Calculation record and scope.** I read the common and W2 briefs, the scan's headline findings, generality table and reduction lemma, both named scan mathematics reports, and the relevant live manuscript passages in Sections 2, 4, 5 and Appendices A1, A3, A5, A6 and A9. I independently evaluated the displayed formulas with Python's Decimal arithmetic at 60-digit working precision, using an increasing scalar research equation and bisection. The consumer calculation is `audit/theory_upgrade_2026_10_25/solvers/computations/W2_A/calculations.py`; its printed results are `audit/theory_upgrade_2026_10_25/solvers/computations/W2_A/calculations_output.txt`. The benchmark numbers reproduce the displayed research and ownership values in `overleaf/slot/numbers.tex`. These numerical calculations support the analytical derivations; they are not interval certificates. No assertions, test files, test framework or test suite were used. No manuscript file was edited, and no other solver's workaround output was read.
