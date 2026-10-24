# XP3: Independent check of the research result

Status: complete, 23 October 2026.

The research result holds at calibration B.
The equilibrium lists at all six strengths are complete.
Every registry display agrees with an independent calculation.
The package needs corrections to its interval records and three statements of scope or interpretation.

## 1. Verdicts and evidence

| Item | Verdict | Result and status |
|---|---|---|
| 1. Equilibrium and joint deviations | **confirmed** | The private research choice and subsequent orders form a coherent equilibrium. The deviation holds prices and entry fixed. **analytical**. |
| 2. Complete sets at six strengths | **confirmed** | The lists below exhaust pure orders, mixed orders, zero research, cap research, and threshold entry under all four rule pairs. **analytical**, with **computer-assisted** signs. |
| 3. Branch values, interval, and slope | **confirmed** | The three research values, three entry values, and interval agree. Entry rises strictly for every permitted beta, wherever the branch exists. **analytical**, with **computer-assisted** endpoints. |
| 4. Endpoint uniqueness | **corrected** | Uniqueness holds at 6/5, 3, and 18/5. The broader uniqueness sentence omits the CM exception at the entry ceiling. **analytical**, with **computer-assisted** margins. |
| 5. Admissible region | **corrected** | The four bounds are exact for the stated interior-branch claims. The cap margin and posterior margin differ. **analytical**, with **computer-assisted** endpoints. |
| 6. Price access | **confirmed** | Proceeds rise by 0.257948. Net surplus rises by 0.081960. Research and trade costs cancel. **analytical**, with **computer-assisted** values. |
| 7. Registry | **corrected** | All 138 displays agree; all 71 fraction value fields agree exactly. However, 65 written enclosure notes exclude their true value. **computer-assisted**. |

The checked sources are `proofs/P3_research.tex`, `memos/P3_research.md`, `scripts/P3_research/`, and `registry/P3_research.csv`.
The core reference is `proofs/P1_core.tex`.
The earlier references are N3, XN3, T2, EXTENSIONS_SUMMARY, and SYNTHESIS section 5.1.
The payoff source is `overleaf/paper` at commit `01bd5d6`, `main.tex`, equations (4) and (9).
The shared formulas in TEAM_RULES section 3 agree with that pinned source.
No external source enters this check.

The independent calculation is [recompute.py](../scripts/XP3/recompute.py).
Its output is [recompute.log](../scripts/XP3/recompute.log).
It imports no code from the checked package.
It integrates the actual auction payoffs on their affine segments.
It computes the research roots through the quadratic formula, with exact rational bounds for every square root.
The source package instead uses bisection for those roots.

All comparisons use rational endpoints.
For the exponential constant, define

\[
s_{60}=\sum_{n=0}^{60}\frac1{n!},\qquad
s_{60}<e<s_{60}+\frac{62}{61\cdot61!}.
\]

After the first omitted term, every ratio is at most \(1/62\).
The geometric sum therefore proves the upper bound.
The file [exact_enclosures.json](../scripts/XP3/exact_enclosures.json) records exact rational endpoints for all 138 quantities.
The decimal intervals below round outward.

## 2. Equilibrium and the fixed-object deviation

### 2.1 The tuple and information

**Confirmed; analytical.** The equilibrium is

\[
\mathcal E=(\widehat\lambda,\sigma_H,\sigma_L,P,\mu,\zeta,\text{bids}).
\]

The investor chooses research before it knows the class.
Research remains private.
Market makers use the candidate intensity \(\widehat\lambda\).
After success, the investor knows the class and chooses its order.
After failure, the liquidity trader fills the slot.
The failed investor receives no trade payoff.

For each order \(q\), the candidate defines

\[
f_j(q)=(1-\widehat\lambda)\eta(q)+\widehat\lambda\sigma_j(q),\qquad
\mu_q=\frac{f_H(q)}{f_H(q)+f_L(q)},
\]
\[
e_q=\rho+(1-\rho)\zeta(P_q),\qquad
P_q=t_0+e_q[t_L-t_0+\Delta_T\mu_q].
\]

The equilibrium conditions are Bayes consistency, beliefs conditional on the price, optimal entry, competitive prices, optimal orders, truthful bids, and optimal research.
The high-cost challenger uses C1 or CM at equality.
The investor uses IM or I0 at equality.
The zero-cost challenger prepares throughout the calibrated domain.

### 2.2 Joint deviations

The order payoffs against this fixed tuple are

\[
U_H(q)=q e_q\Delta_T(1-\mu_q)-k|q|,\qquad
U_L(q)=-q e_q\Delta_T\mu_q-k|q|.
\]

For any research choice \(z\) and any class-contingent order distributions \(\sigma'_j\), the deviation earns

\[
\Pi(z,\sigma')=
\frac z2\sum_q[\sigma'_H(q)U_H(q)+\sigma'_L(q)U_L(q)]-\frac a2z^2.
\]

The deviation changes the true order masses.
It leaves the candidate prices and entry rule fixed.
In particular, the deviation does not replace \(\mu_q\) with a posterior under \(z\).
The source uses this distinction correctly.

Define

\[
V=\frac12\max_q U_H(q)+\frac12\max_q U_L(q).
\]

The bracket is at most \(V\), with equality at optimal orders.
Thus every joint deviation is bounded by \(zV-az^2/2\).
The unique maximizer is

\[
z^*=\min\{\bar\lambda,V/a\}.
\]

This proves the joint-deviation condition without a change in the price function.
Strict concavity also excludes a nondegenerate mixture over research intensities.
At zero research, sequential order optimality after a hypothetical success supports the same deviation calculation.

### 2.3 Price access and circularity

Every order has positive liquidity mass because \(\bar\lambda<1\) and \(0<\beta\le1/3\).
Every permitted deviation reaches an order with a defined price.
No belief outside the image of the price function enters the argument.

Equal prices imply equal entry probabilities because entry is a function of the price.
Competitive prices then imply equal market posteriors when \(\Delta_T>0\).
This proves price sufficiency within any candidate equilibrium.

Candidate construction also permits a direct check of distinct prices.
For the research and threshold tuples,

\[
\mu_0<\mu_{-1}=\tfrac12<\mu_1,\qquad
e_0=e_{-1}=\rho<e_1.
\]

Since \(t_L-t_0>0\), these inequalities imply \(P_0<P_{-1}<P_1\).
For the full-trade tuples, \(P_{-1}<P_0<P_1\).
For zero research, all three posteriors and prices coincide.
These direct comparisons close the construction without an assumption that the desired entry rule already uses distinct prices.
The log prints every price and every order payoff.
No circular step affects the checked result.

## 3. An exhaustive support reduction

**Confirmed; analytical.** The posterior bound under every order profile is

\[
m_\lambda\le\mu_q\le M_\lambda,\qquad
m_\lambda=\frac{(1-\lambda)\beta}{2\beta+(1-2\beta)\lambda},\quad M_\lambda=1-m_\lambda.
\]

The liquidity mass at zero is at least the mass in either direction because \(\beta\le1/3\).
The informed mass at any order is at most \(\lambda\).
These two bounds prove the posterior interval for arbitrary pure or mixed profiles.

Wrong-signed orders obey

\[
U_H(-1)\le-k<0=U_H(0),\qquad U_L(1)\le-k<0=U_L(0).
\]

Suppose research is positive.
Then \(V>0\).
If the high-class purchase is profitable, it is its unique best order.
If only the low-class sale appears profitable, sequential optimality forces a full sale.
That sale has posterior \(m_\lambda<\tau\), so its entry is \(\rho\).
The high-class purchase then earns at least the same positive payoff, from the posterior bound.

Consequently, every equilibrium with positive research has a strict full purchase by the high class.
The posteriors at zero and at a sale are then at most \(1/2\).
At all six strengths, \(\tau>1/2\), so those two orders induce entry \(\rho\).

Write \(d=\Pr(-1\mid L,\text{success})\) and \(b=(1-\lambda)\beta\).
The complete low-class support conditions are

\[
\begin{array}{ll}
d=0:&\rho\Delta_T/2-k\le0,\\
d=1:&\rho\Delta_T m_\lambda-k\ge0,\\
0<d<1:&d=\dfrac b\lambda\left(\dfrac{\rho\Delta_T}{k}-2\right),\quad U_L(-1)=0.
\end{array}
\]

IM permits the last case.
I0 excludes it because zero is also optimal.
These conditions cover every low-class mixture.
They do not assume that the source list is complete.

At the three middle strengths,

\[
k-\rho\Delta_T/2=
\frac{387}{49600},\quad\frac{19}{3200},\quad\frac{211}{52800}>0.
\]

Thus the low class strictly chooses zero at every positive-research candidate.
At 3 and 18/5, the uniform bounds in section 5 instead force a full sale.
This leaves only the research regimes that the next section lists.

## 4. The complete equilibrium sets at B

**Confirmed; analytical, with computer-assisted values.** The investor rule does not affect any outcome at these six strengths.
Every order choice is strict at every equilibrium in the table.
Only the challenger rule adds an equilibrium.

| Strength | IM/C1 | I0/C1 | IM/CM | I0/CM |
|---|---|---|---|---|
| 6/5 | Z | Z | Z | Z |
| 1.55 | Z, R | Z, R | Z, R, T | Z, R, T |
| 1.60 | Z, R | Z, R | Z, R, T | Z, R, T |
| 1.65 | Z, R | Z, R | Z, R, T | Z, R, T |
| 3 | C | C | C | C |
| 18/5 | C | C | C | C |

All tuples use the price formula in section 2 and truthful bids.
The other components are:

\[
\begin{array}{c|c|c|c|c}
&\widehat\lambda&\sigma_H&\sigma_L&(\zeta_{-1},\zeta_0,\zeta_1)\\ \hline
Z&0&\delta_0&\delta_0&(0,0,0)\\
R&\lambda_R&\delta_1&\delta_0&(0,0,1)\\
T&\lambda_E&\delta_1&\delta_0&(0,0,(e^*-\rho)/(1-\rho))\\
C\text{ at }3&\bar\lambda&\delta_1&\delta_{-1}&(0,0,1)\\
C\text{ at }18/5&\bar\lambda&\delta_1&\delta_{-1}&(0,0,0).
\end{array}
\]

Z has \(\mu_q=1/2\) for every order.
R and T have

\[
(\mu_{-1},\mu_0,\mu_1)=
\left(\tfrac12,\frac{(1-\lambda)(1-2\beta)}{2(1-\lambda)(1-2\beta)+\lambda},M_\lambda\right).
\]

C has \((\mu_{-1},\mu_0,\mu_1)=(m_{\bar\lambda},1/2,M_{\bar\lambda})\).
The exact cap is

\[
\bar\lambda\in[0.3361217689151211973971835499034514993733,
0.3361217689151211973971835499034514993734].
\]

For an interior research choice with low-class abstention,

\[
2a\lambda=e_1\Delta_Tm_\lambda-k.
\]

The branch R uses \(e_1=1\).
A threshold uses

\[
\lambda_E(r)=\frac{\beta(2\tau-1)}{\beta+(1-2\beta)(1-\tau)},\qquad
e^*=\frac{2a\lambda_E+k}{\Delta_T(1-\tau)}.
\]

| Strength | Research on R | Entry on R | Research on T | Entry after a purchase on T | Aggregate entry on T |
|---|---:|---:|---:|---:|---:|
| 1.55 | 0.237901194995391 | 0.507630115664746 | 0.196741122491405 | 0.865702724312279 | 0.456294156723749 |
| 1.60 | 0.279037101522556 | 0.513965405209112 | 0.199697586626788 | 0.758776526022282 | 0.420776895871104 |
| 1.65 | 0.316683177855701 | 0.519763230367584 | 0.202664281613542 | 0.673747528534174 | 0.392494046232212 |

The log evaluates both interior research regimes, the threshold regime, zero research, and the cap at each strength.
The floor-entry roots at the middle strengths are negative.
The cap candidates there have negative research KKT margins.
At 3 and 18/5, both interior roots exceed the cap.
Their threshold candidates violate the feasible entry interval; the threshold intensity at 18/5 also exceeds the cap.
Together with the support reduction, these exclusions prove completeness.

## 5. The branch, its slope, and endpoint uniqueness

### 5.1 General beta

**Confirmed; analytical.** Clear the denominator in the interior condition for R:

\[
F_r(\lambda)=2a(1-2\beta)\lambda^2+
[4a\beta+k(1-2\beta)+\beta\Delta_T(r)]\lambda+
\beta[2k-\Delta_T(r)].
\]

When \(\Delta_T>2k\), this polynomial has one positive root below one.
Its derivative in \(\lambda\) is positive on \([0,1]\).
Its derivative in \(r\) is \(-\beta(1-\lambda)\Delta_T'(r)\).
Thus

\[
\lambda_R'(r)=\frac{\beta(1-\lambda_R)\Delta_T'(r)}{\partial_\lambda F_r(\lambda_R)}>0.
\]

Only a purchase recruits on R, so

\[
\mathsf E_R=\rho+(1-\rho)[\beta+(1/2-\beta)\lambda_R],\qquad
\mathsf E_R'=(1-\rho)(1/2-\beta)\lambda_R'>0.
\]

The last sign holds for every \(0<\beta\le1/3\).
It describes the branch wherever that branch satisfies entry and cap conditions.
It does not require that the branch exist at every strength for every beta.

### 5.2 The branch interval at B

**Confirmed; computer-assisted endpoints, analytical interval proof.** The branch starts where

\[
\varphi_a(r)=\Delta_T(r)(1-\tau(r))-k-2a\lambda_E(r)=0.
\]

The independent exact derivative bound on \([6/5,7/4]\) is

\[
\varphi_{1/40}'(r)>0.033766>0.
\]

The function has opposite signs at the two endpoints.
It therefore has exactly one zero there.
The calculation gives outward bounds

\[
r_R\in[1.501022966262572145582851379980,
1.501022966262572145582851379981],
\]
\[
\bar r_R\in[1.677632834385080818823429063896,
1.677632834385080818823429063897].
\]

The upper endpoint solves \(\Delta_T=(2a\bar\lambda+k)(1+e)\).
The interior branch is exactly \([r_R,\bar r_R)\).
The lower endpoint includes full entry at the challenger tie under both C1 and CM.
The upper endpoint belongs to the cap regime.

Zero research coexists throughout this interval because

\[
\bar r_R<r_N=1.747877538267962743567348177929\ldots,
\qquad \rho\Delta_T(r_N)=2k.
\]

After \(\bar r_R\), entry stays at its cap level until \(r_N\).
No interior equilibrium with a recruiting purchase can return above \(\bar r_R\).
Indeed, its research condition would imply \(F_r(\lambda)\ge0\), hence \(\lambda\ge\lambda_R(r)\ge\bar\lambda\).

### 5.3 The three unique endpoint outcomes

**Confirmed at the three requested points; analytical, with computer-assisted margins.** At 6/5, \(\Delta_T=1/60<k\).
Every nonzero order loses against every consistent candidate schedule.
Thus \(V=0\), research is zero, both classes abstain, and entry is \(1/4\).
The bound has margin \(k-\Delta_T=1/300\).

At 3 and 18/5, every correctly signed order earns at least

\[
\rho\Delta_Tm_{\bar\lambda}-k>a\bar\lambda>0.
\]

This bound holds for every candidate order profile.
Its margins above \(a\bar\lambda\) are 0.01642052600545449 and 0.03472348384869027.
Both classes therefore trade fully, and research equals the cap.
The strict posterior margins are

\[
M_{\bar\lambda}-\tau(3)=0.026058578630004879\ldots,
\]
\[
\tau(18/5)-M_{\bar\lambda}=0.000333564719409317854\ldots.
\]

Entry is 0.522756943478406672 at 3 and exactly 1/4 at 18/5.
These outcomes are unique under all four pairs of tie rules.

### 5.4 Correction: uniqueness at the entry ceiling

**Refuted as an unrestricted equilibrium claim; analytical.** The memo's result table says the equilibrium is unique for every \(r>r_U^R\).
Under CM this fails at

\[
r_C=3.592658518794661833335916059882\ldots>r_U^R.
\]

At that strength, \(M_{\bar\lambda}=\tau(r_C)\).
The same uniform bound forces full trades and research at the cap.
The high-cost challenger is indifferent after a purchase.
Every \(\zeta_1\in[0,1]\) is admissible; \(\zeta_0=\zeta_{-1}=0\).
Each choice gives its own competitive purchase price.

Aggregate entry spans the complete interval

\[
\left[\frac14,\ 0.522756943478406671709643\ldots\right].
\]

Research itself remains unique.
The full equilibrium is unique above \(r_U^R\) under CM only when \(r\ne r_C\).
C1 selects \(\zeta_1=1\) at \(r_C\).
The formal strong-incumbent proposition already includes \(M_{\bar\lambda}\ne\tau(r)\).
The correction belongs in the broader memo summary and any similar manuscript sentence.

### 5.5 Correction: the general weak-incumbent statement

**Corrected; analytical.** The weak-incumbent proposition uses \(B_r(1/2)<c_H\) in its proof but omits this condition from its displayed hypothesis.
The condition holds for all calibrated auction primitives and every beta in this check.
If the proposition permits other auction primitives, add the condition.

For example, change only \(c_H\) from 6 to 1 at \(r=6/5\).
Then \(\Delta_T=1/60<k\), so zero research remains unique.
But \(B_r(1/2)-c_H=913/240>0\), so both cost classes prepare and entry equals one.
The statement that entry equals \(\rho\) fails in that generality.
The zero-research criterion \(\rho\Delta_T\le2k\) also presumes floor entry at the uninformative price.

## 6. The admissible region and its precise scope

**Confirmed for the stated claims; analytical, with computer-assisted endpoints.** Fix beta at B.
Require the interior branch at all three middle strengths and the stated full-trade cap outcomes at 3 and 18/5.
The exact open region is

\[
\lambda_E(3)<\bar\lambda<\lambda_E(18/5),\qquad
\frac{\Delta_T(33/20)m_{\bar\lambda}-k}{2\bar\lambda}<a<
\frac{\Delta_T(31/20)[1-\tau(31/20)]-k}{2\lambda_E(31/20)}.
\]

The endpoints are

| Quantity | Independent value |
|---|---:|
| Lower cap, \(\lambda_E(3)=2416171/8316171\) | 0.29053887901054463647 |
| Upper cap, \(\lambda_E(18/5)=79144333/235044333\) | 0.33672087299377688038 |
| Lower cost at \(\lambda_B\) | 0.02146937956738749777 |
| Upper cost | 0.03676330206514472513 |
| Lower cap at \(a=1/40\) | 0.31668317785570084272 |

Each value in this table is rounded for display.
The log and exact endpoint file supply its enclosure.

The lower cost bound is exactly the condition that research at 1.65 stays below the cap.
The upper cost bound is exactly the strict recruitment condition at 1.55.
The derivative bound makes the latter condition hold at 1.60 and 1.65 as well.
The cap strip gives strict recruitment at 3 and strict exclusion at 18/5.

The strong-incumbent cost limits do not add a constraint within this region.
Their infima over the cap strip are

\[
\inf a_{U3}=0.07355640263170949144\ldots>a_{\rm up},\qquad
\inf a_{U36}=0.12784545441639196993\ldots>a_{\rm up}.
\]

The monotonicity limit also exceeds the upper cost bound.
The cost window is nonempty throughout the strip.
Thus the four stated bounds are exactly the active constraints for the declared claim set.

### 6.1 Strict entry growth alone allows a larger set

The lower cost bound changes if only strict entry growth across the three strengths is required.
Research may reach the cap at 1.65 while entry still exceeds entry at 1.60.
At \(\bar\lambda=\lambda_B\), the relevant lower cost becomes

\[
\frac{\Delta_T(8/5)m_{\lambda_B}-k}{2\lambda_B}
=0.01525624171446377539\ldots.
\]

For costs between this number and 0.02146937956738749777, research reaches the cap at 1.65 only.
The three entry values still rise strictly, subject to the same upper cost bound.
This distinction matches XN3's correction at calibration A.
P3's region is exact for three interior research choices; it is narrower than the region for strict entry growth alone.

### 6.2 General beta at the exponential cap

**Confirmed; computer-assisted endpoints, analytical inequalities.** Put \(\bar\lambda=(e-1)\beta/[1+(e-1)\beta]\).
Then \(m_{\bar\lambda}=1/(1+e)\), independently of beta.
The two endpoint posterior conditions therefore remain fixed.

Let

\[
x=\frac{\Delta_T(33/20)/(1+e)-k}{2a},\qquad
\beta_{\rm lo}=\frac{x}{(1-x)(e-1)}.
\]

For \(a=1/40\), the independent value is

\[
\beta_{\rm lo}\in[0.236156685530381042164523080574,
0.236156685530381042164523080575].
\]

The upper cost condition holds for beta below 0.48974067309178476470, which exceeds 1/3.
The worst uniform research margin over \(0<\beta\le1/3\) occurs at 1/3 and exceeds 0.01571918704961392850.
The derivative bound for \(\varphi\) also stays positive over the required domain.
Thus all declared claims hold exactly for \(\beta\in(\beta_{\rm lo},1/3]\).
Below the lower endpoint, the recruiting branch reaches the cap at 1.65; zero research still coexists.

### 6.3 Correction: two different margins

**Refuted literally; computer-assisted.** The memo says that the upper cap margin equals the posterior margin.
The correct values are

\[
\lambda_E(18/5)-\lambda_B=0.00059910407865568298\ldots,
\]
\[
\tau(18/5)-M_{\lambda_B}=0.00033356471940931785\ldots.
\]

They measure the same boundary in different coordinates.
They have the same sign because \(M_\lambda\) rises strictly.
They are not equal numbers.
Replace “equals” with “corresponds to”.

## 7. Price access at r = 3

**Confirmed; analytical, with computer-assisted values.** With hidden prices, the challenger's belief stays at one half.
Since \(B_3(1/2)<6\), entry is \(\rho\) after every order.
The uniform payoff bound still forces full trades and cap research.
Thus the two economies have the same order law, research cost, and trade cost.

Let \(w_+=(1-\bar\lambda)\beta+\bar\lambda/2\).
Price access adds high-cost entry only after a purchase.
The changes are

\[
\Delta\mathcal R_T=(1-\rho)w_+[t_L-t_0+\Delta_T M_{\bar\lambda}],
\]
\[
\Delta\mathcal W=(1-\rho)w_+[B_3(M_{\bar\lambda})-c_H+p^2/3].
\]

The second identity includes the reserve term.
For each class, entry adds auction surplus \(g_j+p\Pr(R<p)=g_j+p^2/3\).
Subtract the extra preparation cost to obtain the formula.
Both expressions are strictly positive.

| Quantity | Hidden prices | Price access | Change |
|---|---:|---:|---:|
| Expected proceeds | 0.614583333333333 | 0.872531134701462 | +0.257947801368129 |
| Surplus net of preparation costs | 2.552083333333333 | 2.634043564110799 | +0.081960230777466 |

The research cost is 0.001412223044232877 in both economies.
The trade cost is 0.006722435378302424 in both economies.
The surplus difference therefore stays the same after both resource costs.
The independent script obtains the levels from a sum over the actual class and order masses.

## 8. The registry and certificate correction

### 8.1 Every numerical display agrees

**Confirmed; computer-assisted.** The independent calculation covers every one of the 138 registry rows.
No row differs beyond its display precision.
All 71 fraction value fields agree exactly.
The file [registry_comparison.csv](../scripts/XP3/registry_comparison.csv) gives the independent endpoints and both differences for each row.
Its final count is `input=138, recomputed=138, unresolved=[], display differences=[]`.

The six calibration-A rows also agree.
Their research values are 0.250249322293818, 0.293324846156412, and 0.332615237748222.
Their entry values are 0.531281165286727, 0.536665605769552, and 0.541576904718528.

### 8.2 The printed enclosures need repair

**Corrected; computer-assisted.** The source uses exact rational interval arithmetic internally.
Its function `enc`, at script lines 162–165, converts both endpoints to binary floats and then rounds them to nearest decimals.
That procedure does not preserve an enclosure.
The log and registry notes often print a nonzero interval as an equal pair of rounded endpoints.

For example, the first log lines call this an enclosure of the exponential constant:

\[
[2.718281828459045090795598298428,
2.718281828459045090795598298428].
\]

The exact constant exceeds that singleton interval.
The `res_rR` note also gives

\[
[1.501022966262571,1.501022966262572],
\]

while the independent exact value exceeds its upper endpoint:

\[
r_R>1.501022966262572145582851379980.
\]

The problem affects 65 registry enclosure notes.
The file [invalid_enclosures.csv](../scripts/XP3/invalid_enclosures.csv) lists every affected key, its written endpoints, and corrected outward endpoints.
This is a certificate-output defect.
It does not change any displayed registry value or any equilibrium verdict at the six strengths.

Write rational endpoints, or round the lower decimal downward and the upper decimal upward.
Keep the full exact endpoints in a machine-readable file.
The independent output supplies both forms.

## 9. Completion, scope, and files

The script ran through its real command interface with the actual primitives and registry.
It printed all six equilibrium sets, all order deviations, the excluded research regimes, and every registry comparison.
The final run used one shared CPU slot.
The checked files remain unchanged.
No test or test suite ran.

The required seven items are complete.
The equilibrium correspondence on \((r_N,r_U^R)\) stays outside this check.
Section 5.4 separately checks the entry ceiling \(r_C>r_U^R\).
The source package itself marks the intermediate correspondence as outside its proved claims.
No claim of BRIEF R10 or of the calibrated N3 result is refuted.
The broader uniqueness sentence, the omitted hypothesis for a general weak-incumbent proposition, and the literal margin equality need correction.
The written enclosure records need replacement before they serve as standalone certificates.

Files written:

- `memos/XP3_check.md`: this memo.
- `scripts/XP3/recompute.py`: the independent calculation.
- `scripts/XP3/recompute.log`: the final output.
- `scripts/XP3/registry_comparison.csv`: all 138 registry comparisons.
- `scripts/XP3/invalid_enclosures.csv`: all 65 invalid enclosure notes, with corrected bounds.
- `scripts/XP3/exact_enclosures.json`: exact rational endpoints for all quantities.
- `scripts/XP3/receipt.json`: source hashes and method declarations.
