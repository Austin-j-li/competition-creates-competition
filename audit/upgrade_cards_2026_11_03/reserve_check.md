# Seller reserves: independent check

The original calibration does not survive reserve optimization. At \(\rho=1/4\), all three strengths favor \(p\to10^-\). Proceeds approach \(1.25\), and entry equals \(1/4\). The seller thus shuts the recruitment channel in this exercise.

This conclusion is **new, not in the paper**. The paper proves its main result at a fixed reserve. It does not claim that its reserve maximizes proceeds.

## Scope and source facts

The calculation uses the sale rule in `overleaf/slot/sections/02_model.tex`, especially equations (classes) and (price). It uses (H1)–(H3) in `sections/04_equilibrium_results.tex`. The reserve kernel and proposition appear in `appendix/A7_welfare.tex:145–190`. The reserve table appears in `sections/07_welfare.tex`.

The primitive inputs come from `numbers.tex`, keys `prim_*` and `beta_B`. Appendix A9 declares the exact slot definitions. Thus

\[
\beta=0.294655,\quad u=e-1,\quad
\lambda=\frac{u\beta}{1+u\beta}=0.3361217689151212,
\quad b=(1-\lambda)\beta=0.1956150401803150.
\]

The displayed `lambda_B` value, \(0.336122\), is rounded. It is not the exact primitive. The calculations use 60 decimal digits and the unrounded definition.

\[
M=\frac e{1+e}=0.7310585786300049,
\quad \kappa=m=1-M=0.2689414213699951,
\]
\[
A=b+\lambda=0.5317368090954362,
\quad Q=b+\lambda/2=0.3636759246378756.
\]

The incumbent value is uniform on \([0,r]\). The rival values are \(h=10\) and \(\ell=1\), with equal class probabilities. The high preparation cost is \(6\). The zero-cost rival prepares even when its acquisition profit is zero. Market makers use conditional expected proceeds as the share price.

All optimization results below are **new, not in the paper**. “Floor” means preparation probability \(\rho\). It does not mean the probability of a sale. The objective is expected proceeds for shareholders who hold through the sale. It does not subtract the informed trader's gains from those proceeds.

## Reproduction of the printed results

The following values reproduce the paper's point-value reserve rows after rounding. Here \(\rho=1/4\) and \(k=1/50\).

| Reserve | Strength | Proceeds | Entry | Sale | Two admissible bidders |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 1.2 | 0.3927083333 | 0.2500000000 | 0.6875000000 | 0.1458333333 |
| 0.5 | 3 | 0.8725311347 | 0.5227569435 | 0.9204594906 | 0.4356307862 |
| 1.01 | 1.2 | 0.4405643443 | 0.5227569435 | 0.4313710970 | 0.0513635397 |
| 1.01 | 3 | 0.9943841901 | 0.5227569435 | 0.7725484388 | 0.2151861979 |
| 1.55 | 1.2 | 0.5028220203 | 0.5227569435 | 0.3244013034 | 0 |
| 1.55 | 3 | 0.8930729167 | 0.2500000000 | 0.5479166667 | 0.0604166667 |

At \(p=1/2,r=3.6\), proceeds equal \(0.6642361111111111\). Entry equals \(1/4\).

## 1. Global reserve choices for point values

Use \(k=0.02\) for \(\rho\in\{1/4,1/5,3/20,1/8\}\). Use \(k=0.017\) for \(\rho=1/10\). The latter change is necessary for (H2).

The paper's bounds decide every reserve in \((0,10)\) for these five pairs. No point-value reserve remains open.

* At \(r=1.2\) and \(0<p\le1\), \(\Delta_T=1/60<k\). The informed trader abstains in both classes.
* At \(r=1.2\) and \(p>1\), \(\Delta_T\ge17/20\). The lower trade bound forces full orders.
* At \(r=3\), \(\Delta_T=2/3\) for \(p\le1\). For \(p>1\), its minimum is \(1\). Full orders hold throughout.
* At \(r=3.6\), \(\Delta_T=169/180\) for \(p\le1\). For \(p>1\), its minimum is \(1.2\). Full orders hold throughout.

Full orders mean a purchase by the high-class informed trader and a sale by the low-class informed trader. These conclusions use bounds for every candidate plan. They do not impose full orders as an assumption.

| \(\rho\) | \(k\) | \(r\) | Best reserve or limit | Proceeds | Entry |
|---:|---:|---:|---:|---:|---:|
| 1/4 | .02 | 1.2 | \(10^-\) | 1.2500000000 | .2500000000 |
| 1/4 | .02 | 3 | \(10^-\) | 1.2500000000 | .2500000000 |
| 1/4 | .02 | 3.6 | \(10^-\) | 1.2500000000 | .2500000000 |
| 1/5 | .02 | 1.2 | \(10^-\) | 1.0000000000 | .2000000000 |
| 1/5 | .02 | 3 | 1.3252698283 | 1.0690594690 | .4909407397 |
| 1/5 | .02 | 3.6 | 1.9058823529 | 1.0376470588 | .2000000000 |
| 3/20 | .02 | 1.2 | \(10^-\) | .7500000000 | .1500000000 |
| 3/20 | .02 | 3 | 1.3252698283 | 1.0567336085 | .4591245359 |
| 3/20 | .02 | 3.6 | 1.8760563380 | 1.0026760563 | .1500000000 |
| 1/8 | .02 | 1.2 | \(10^-\) | .6250000000 | .1250000000 |
| 1/8 | .02 | 3 | 1.3252698283 | 1.0505706782 | .4432164341 |
| 1/8 | .02 | 3.6 | 1.8620689655 | .9853448276 | .1250000000 |
| 1/10 | .017 | 1.2 | 1.7927233530 | .5186018155 | .4273083322 |
| 1/10 | .017 | 3 | 1.3252698283 | 1.0444077479 | .4273083322 |
| 1/10 | .017 | 3.6 | 1.8486486486 | .9681081081 | .1000000000 |

Every optimum in this table has full orders. A \(10^-\) row is a supremum. No reserve inside \((0,10)\) attains that value. At \(p=10\), the paper's zero-cost preparation convention attains it exactly.

The reserve \(1.3252698283\) puts the high-cost rival exactly at its preparation threshold after a purchase. The reserve \(1.7927233530\) does the same at the weak incumbent. The table uses the paper's default rule: the indifferent high-cost rival prepares. A different tie rule can replace these maxima by limits from below.

### Analytical global comparison

The following formulas prove the point-value optimization; the table is not a reserve grid.

Write \(\mathcal R\) for proceeds and \(C=[\rho+(1-\rho)A]/2\). For \(1<p<r\), only a purchase recruits when it can recruit. On that branch,

\[
\mathcal R_C(p)=C\frac r2+(1-C)p-
\left(1-\frac{3C}{2}\right)\frac{p^2}{r}.
\]

The branch ends at the threshold reserve. For \(r\le p\), its proceeds equal \(Cp\). Define

\[
a=10-\frac6M=1.7927233529713461,
\quad p_C(1.2)=a,
\quad p_C(3)=\sqrt{6a-9}=1.3252698283097206.
\]

At \(r=3.6\), recruitment is possible only below the low value. Its largest reserve is

\[
p_C(3.6)=\sqrt{2r\left[M(10-r/2)+\frac{\kappa}{2r}-6\right]}
=0.4802498346543007.
\]

On the floor branch with \(1<p<r\),

\[
\mathcal R_D(p)=\frac{\rho r}{4}+
(1-\rho/2)p-\left(1-\frac{3\rho}{4}\right)\frac{p^2}{r},
\]
\[
p_D=\frac{r(1-\rho/2)}{2-3\rho/2},\qquad
\mathcal R_D(p_D)=r\left[\frac\rho4+
\frac{(1-\rho/2)^2}{4-3\rho}\right].
\]

For \(p\ge r\) above the preparation threshold, proceeds equal \(\rho p/2\). Their supremum is \(5\rho\).

For \(p\le1\), class proceeds have the same coefficient on \(p^2\). If class entry rates are \(e_H,e_L\), set \(E=(e_H+e_L)/2\). Then

\[
\mathcal R(p)=K+(1-E)p+
\left(-1+\frac{3E}{2}\right)\frac{p^2}{r},
\]

where \(K\) does not depend on \(p\). At the weak incumbent, \(e_H=e_L=\rho\). At the other strengths, split this quadratic at \(p_C\). Evaluate its endpoints and any interior stationary point. Also compare the two one-sided values at \(p=1\).

At \(p=1\), the low class remains admissible. Just above \(1\), it becomes inadmissible, so proceeds and the order plan can jump. The comparison includes this discontinuity. These piecewise quadratics, their stationary points, and the high-reserve limit exhaust the reserve domain.

## 2. Main conditions at the original reserve

All five chosen pairs satisfy (H1), (H2), and (H3). The cost margins for (H1) and (H3) do not depend on \(\rho,k\):

\[
6-B_{1.2}(1/2)=1.1958333333333333,
\]
\[
B_3(M)-6=0.2171548219167073,
\qquad 6-B_{3.6}(M)=0.0026889022659051.
\]

The exclusion margin is small. The two margins for (H2) are:

| \(\rho\) | \(k\) | \(k-\Delta_0\) | \(\rho\kappa\Delta_1-k\) |
|---:|---:|---:|---:|
| 1/4 | .02 | .003333333333 | .024823570228 |
| 1/5 | .02 | .003333333333 | .015858856183 |
| 3/20 | .02 | .003333333333 | .006894142137 |
| 1/8 | .02 | .003333333333 | .002411785114 |
| 1/10 | .017 | .000333333333 | .000929428091 |

If \(k=.02\) remains fixed at \(\rho=.1\), (H2) fails. Its upper margin becomes \(-.002070571909\).

## 3. Exact crossover values and entry patterns

These crossover results are **new, not in the paper**. They use a common cost within the main theorem's window:

\[
\frac1{60}<k<\frac{2\rho\kappa}{3}.
\]

Such a cost exists exactly when

\[
\rho>\rho_{\min}=\frac1{40\kappa}
=0.0929570457114761.
\]

For each strength, evaluate \(t_0,t_H,t_L\) at its \(p_C\) above. Define

\[
J_r=\frac{A(t_H-t_0)+b(t_L-t_0)}2,
\qquad L_r=\frac{t_H+t_L-2t_0}{2}.
\]

The best reserve that recruits has proceeds

\[
\mathcal R_C^*(\rho)=t_0+J_r+\rho(L_r-J_r).
\]

The exact crossover with the high-reserve supremum is

\[
\boxed{\rho_r^*=\frac{t_0+J_r}{5-L_r+J_r}}.
\]

| Strength | \(\rho_r^*\) |
|---:|---:|
| 1.2 | .1040612951733614 |
| 3 | .2145281832411283 |
| 3.6 | .1874747424489786 |

Above the displayed crossover, \(5\rho\) exceeds the best proceeds with recruitment. Below it, recruitment beats that supremum. At equality, the reserve with recruitment attains the common value, while \(p<10\) cannot attain the high-reserve supremum.

The third crossover does not decide the optimal entry rate. At \(r=3.6\), the best floor reserve beats the best reserve with recruitment throughout \((\rho_{\min},1)\). The floor optimum switches between \(p_D\) and \(10^-\) at \(\rho\approx.2087645370825808\). This comparison follows from the quadratic formulas above.

Under the default tie rule and with the endpoint treated as a limiting choice, the optimal pattern is:

| Range | Entry at \(r=1.2,3,3.6\) |
|---|---|
| \(\rho_{\min}<\rho\le\rho_{1.2}^*\) | above floor, above floor, floor |
| \(\rho_{1.2}^*<\rho\le\rho_3^*\) | floor, above floor, floor |
| \(\rho_3^*<\rho<1\) | floor, floor, floor |

At each crossover, inclusion changes if \(p=10\) is allowed and the seller can choose between tied optima. Below \(\rho_{\min}\), no \(k\) satisfies (H2). These statements do not classify all equilibria there. A choice of \(k\) and a new equilibrium calculation are necessary.

## 4. A reserve near the standalone value

This result is **new, not in the paper**. Let \(p\to0^+\), with \(\rho=1/4,k=.02\). At \(r=1.2\), the informed trader abstains, and entry equals the floor. At \(r=3\), full orders recruit after a purchase. At \(r=3.6\), full orders also recruit. Thus these exact three strengths do not give a return to the floor near zero reserve.

For \(p\le\ell=1\) and \(1<r<h\),

\[
\Delta_T=\frac{(r-1)^2}{2r}.
\]

The shareholder spread does not depend on the reserve in this range. Both class proceeds rise by \(p^2/(2r)\). Both class acquisition profits fall by the same amount.

The smallest limiting strength that can stop recruitment solves

\[
M(10-r/2)+\frac{\kappa}{2r}=6.
\]

Its exact value is

\[
r_* =\frac{10M-6+\sqrt{(10M-6)^2+M\kappa}}{M}
=3.6852709643830822.
\]

There is no smallest strength with strict exclusion at \(p=0\). Every \(r>r_*\) works, and \(r_*\) is the infimum. At \(r=r_*\), every sufficiently small positive reserve gives strict exclusion. At exactly zero reserve, the default rule admits the indifferent high-cost rival.

A simple strict choice is \(r=3.7\). In the limit, its exclusion margin equals \(0.0055291488451906\). The other margins are

\[
6-B_{1.2}(1/2)=1.0916666666666667,
\quad B_3(M)-6=.2588214885833740,
\]
\[
k-\Delta_{1.2}=.0033333333333333,
\quad \rho\kappa\Delta_3-k=.0248235702283325.
\]

The same lower trade bound holds at \(3.7\), since its spread exceeds the spread at \(3\). At \(3.6\), the top-profit margin is instead positive: \(B(M)-6=.0320333199563171\). A small positive reserve preserves these strict signs.

## 5. Class width and a different high value

All results in this section are **new, not in the paper**. The paper's narrow classes are uniform on \([.95,1.05]\) and \([9.95,10.05]\).

The point-value formulas remain exact when the reserve exceeds the whole low band and lies below the whole high band. In particular, both threshold reserves above \(1.05\) remain unchanged. The floor reserve at \(r=3.6\) also remains unchanged.

The high-reserve optimum changes. For \(p\) above the incumbent support, floor proceeds equal

\[
\frac\rho2p\Pr(\theta_H\ge p).
\]

This expression reaches its maximum at \(p=9.95\). Its value is \(4.975\rho\), which is attained. The high-value band removes the point-value endpoint discontinuity.

If only reserves above \(1.05\) count as alternatives with recruitment, the crossover values become

\[
\frac{t_0+J_r}{4.975-L_r+J_r}.
\]

They equal \(.1046323994536304\) at \(1.2\), and \(.2156624169520614\) at \(3\). The first is **not** the global weak-incumbent crossover. Reserves inside the low band can do better.

### The narrow band changes an optimum

At \(\rho=.1,k=.017,r=1.2,p=.9561\), a valid informative outcome gives proceeds \(.5216735894\). Entry equals \(.4273083322\). The high-class informed trader buys for sure. The low-class informed trader abstains.

This candidate beats the point-value optimum \(.5186018155\) at \(p=1.7927233530\). Thus the exact answer to question 1 does not survive even this narrow band.

The candidate comes from a grid with step \(.00005\) on \([.95,1.05]\). The calculation averages the kernel by exact polynomial integrals. It then evaluates the candidate's prices, preparation choices, and order payoffs. This is numerical evidence for the candidate, not a proof of its global optimality.

The paper's two bounds leave the following weak-incumbent reserve intervals undecided. Endpoints include equality cases. The intervals concern order plans, not the existence of a sale.

| \(\rho,k\) | Interval with no decision from the two bounds |
|---|---|
| .25, .02 | [.9503967356, .9848398179] |
| .20, .02 | [.9503967356, .9933594943] |
| .15, .02 | [.9503967356, 1.0069950293] |
| .125, .02 | [.9503967356, 1.0174424151] |
| .10, .017 | \((0,1.0212627455]\) |

For the last row, the narrow-band spread below \(.95\) already exceeds \(.017\). The abstention bound therefore fails there. The grid resolves some informative candidates inside these intervals. A complete classification of all narrow-band plans remains open in this report.

The qualitative optimal pattern survives at \(\rho=.15,k=.02\). The weak incumbent favors \(9.95\), with proceeds \(.74625\). The strong incumbent favors \(1.3252698283\), with proceeds \(1.0567336085\). The very strong incumbent favors \(1.8760563380\), with proceeds \(1.0026760563\).

For the weak incumbent, a universal upper bound on proceeds in the low band is less than \(.553\) at this \(\rho\). To obtain it, allow every purchase to recruit. Its class purchase probabilities cannot exceed \(A\) in the high class and \(b\) in the low class. The low-class informed trader never buys, since its purchase payoff is negative. Integration of the kernel gives a quadratic bound on each band piece. Both pieces lie below \(.553\). Thus unresolved plans in that band cannot beat \(.74625\).

At the other two strengths, the minimum spread already forces full orders. Their low-band branches remain below the stated optima. Hence the three stated choices are analytical comparisons, although the separate transition search uses a grid.

The exact point-value interval from question 3 does not carry over unchanged. Its weak endpoint depends on the cost and on equilibrium choices inside the low band. This report does not prove a complete replacement interval. It does prove survival at an interior example and failure of literal equality of the optima.

### Wider classes can cause coexistence

Take uniform classes on \([0,2]\) and \([9,11]\). Keep \(\rho=.25,k=.02,p=.5,r=1.2\). The kernel gives

\[
\Delta_T=.1269444444444444,\quad
 g_H=9.2958333333333333,\quad g_L=.4331944444444444,
\quad \tau=.6281205434799643.
\]

Both a market with no informed orders and a market with an informed purchase satisfy the equilibrium conditions. In the informative outcome, the high-class informed trader buys and the low-class informed trader abstains. Entry equals \(.5227569435\). In the uninformative outcome, entry equals \(.25\).

The relevant payoff margins are

\[
\Delta_T(1-M)-k=.0141406193239133>0,
\quad \rho\Delta_T/2-k=-.0041319444444444<0.
\]

Thus a purchase pays when it recruits, while trade does not pay at the uninformative price. The prior is below \(\tau\), and \(M\) exceeds it. With only high-class purchases, the other posteriors do not exceed the prior. These facts verify both outcomes directly.

This case breaks uniqueness at the original weak incumbent. It defeats a general claim that class width preserves the same order plan. This report leaves its global reserve problem open.

### A lower high value removes the middle rise

Set \(h=9\), with point values and all other original inputs unchanged. At \(r=3,p=0\),

\[
B_3(M)-6=-.4722370900466309.
\]

A positive reserve only lowers this profit. Thus a purchase cannot recruit against either \(r=3\) or \(r=3.6\), at any reserve. Against \(r=1.2\), no trade occurs for \(p\le1\). For \(p>1\), \(B(M)<8M<6\). Its entry also remains at the floor.

The reserve optimum is \(p\to9^-\) at all three strengths when \(\rho=.25,k=.02\). Proceeds approach \(1.125\). This follows from the same piecewise quadratic comparison. A separate grid with step \(.001\) gives \(p=8.999\), proceeds \(1.124875\), and entry \(.25\) at each strength. The grid supports the analytical result; it does not prove it.

This change is not a common rescale of all monetary inputs. A common rescale would preserve incentives. A change in \(h\) alone need not preserve them.

## 6. Statement issues and the trade bound

The independent findings in this section are **new, not in the paper**. The source statements quoted below remain facts from the paper.

**High: a literal assumption conflict.** Section 02 defines “class ranking” to include both first-order dominance and full admissibility. Appendix A7:162 says both “allow class values below” the reserve and “keep the class ranking.” Those requirements conflict when the reserve excludes the low class.

The reserve proposition should retain first-order dominance and explicitly drop full admissibility. Its reserve kernel already permits that change. The proof needs \(\Delta_T\ge0\), which dominance supplies. It does not need full admissibility.

**The lower trade bound remains valid after exclusion.** Competitive prices imply the exact order payoffs

\[
U_H(1)=e(1)[1-\mu(1)]\Delta_T-k,
\qquad U_L(-1)=e(-1)\mu(-1)\Delta_T-k.
\]

These identities cancel the common terms \(t_0\) and \(t_L-t_0\). They remain valid when \(t_L=t_0\). The liquidity trader gives the posterior bounds, and the zero-cost rival gives \(e\ge\rho\). Therefore \(\rho\kappa\Delta_T>k\) correctly forces full orders even when the reserve excludes the low class.

A wrong-signed order earns at most \(-k\). The strict lower bound therefore makes each correct order uniquely optimal. A claim that exclusion invalidates this bound would be incorrect.

**Positive reserves do not rule out the exercise.** Section 02 requires \(p>0\), so \(p=0\) lies outside the stated domain. Every arbitrarily small positive reserve remains admissible. The limit in question 4 therefore has a valid interpretation. Neither the normalization of standalone value nor the positive-reserve assumption requires a material gap above zero.

**The printed reserve table is correct but incomplete for the seller's objection.** Its reserves show that a seller can raise proceeds and remove the weak-to-strong entry increase. They do not identify the seller's optimum. At the original inputs, the stronger result is complete suppression of recruitment at all three strengths under the optimal limiting reserve.

**Scope of the shareholder objective.** Interim share prices equal expected terminal proceeds. The paper separately discusses transfers from liquidity traders. The current optimization uses the proceeds objective requested here. A seller objective with weights on liquidity losses or sale probability requires another calculation.

## Comparison with the existing scan

The independent numerical results came first. Only then did the comparison use `scripts/reserve_scan.py`.

The scan reproduces the printed baseline and the qualitative optimum table for its four chosen pairs. It omits \(\rho=1/8\). Its reserve grid ends at \(9.995\), so its high-reserve rows fall below the true supremum. Its grid also rounds the threshold reserve downward, which slightly lowers proceeds.

The scan uses the rounded presence probability \(.336122\). This changes \(M\) and other derived quantities slightly. Appendix A9 instead requires the unrounded formula used here.

There is one material difference. The scan's final “best recruiting reserve” loop passes \(k=10^{-6}\) to the payoff function. It does not use the cost shown in its preceding loop. This forces full orders below \(p=1\) at the weak incumbent.

For example, at \(\rho=.25\), that loop reports a reserve \(p=1\) with proceeds about \(.6077\). At the original \(k=.02\), the informed trader abstains there, and a purchase does not recruit. The correct best reserve with recruitment, subject to the main cost window, is \(a=1.7927233530\). Its proceeds equal about \(.5816\) at \(\rho=.25\).

The scan's final loop answers a different cost experiment. It cannot supply the crossover values in question 3 for the original channel. Its \(p=9.9\) comparison also differs from the requested supremum \(p\to10^-\).

## Evidence status

* **Proved by piecewise formulas:** all point-value optimum rows, their order plans, the main margins, and the crossover formulas.
* **Proved with stated scope:** the entry interval above \(\rho_{\min}\), the near-zero reserve result, and validity of the lower trade bound after exclusion.
* **Proved counterexamples:** the wider-class coexistence and the loss of middle recruitment when \(h=9\).
* **Numerical on a grid:** informative narrow-band candidates inside the low band and the separate \(h=9\) grid comparison.
* **Open:** full equilibrium classification inside the narrow low band, its exact global crossover interval, and global reserve choices for the wider classes.

The calculation file is `scripts/reserve_independent_review.py`. It prints the inputs, formulas, margins, and candidate outcomes. It contains no assertions. No source file changed.
