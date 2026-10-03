---
title: "Referee report: the cost distribution decides who is an insider"
subtitle: "Track cost_distribution of the endogenous-insider fork"
date: "2026-10-03"
---

## 1. Verdict

The note is sound. I tried to refute every numbered result and found no false theorem. Every key number reproduces in an independent implementation. The interval certificates reproduce bit for bit.

I found one proof gap that matters for a stated bound (Proposition CD.13(d)), two overclaims in the headline (an affine cost law and the regime III sentence), one certified inequality stated above its certificate (0.02775), one rounding error (0.0297), and several small gaps and status labels. I fixed each one in `note.md` and marked it "[Referee fix: ...]". I deleted no author text.

The status labels are earned, with the exceptions listed in Section 5. The analytical results have complete proofs once the fixes are in. Table T2 earns "computer-assisted".

## 2. What I checked and how

- I read `mechanism.md` in full and the paper's (4), (5), (7)–(12), (A1)–(A3), Propositions A.1–A.4, (A.5)–(A.14), and Lemma OA.2.
- I checked every proof step by hand: signs, tie rule, atoms, $\tau=M$, $\tau\le\tfrac12$, mixed orders, null sets, and measurability.
- `referee/recheck.py` is an independent implementation. It does not import `core.py`, `grid.py`, or `solve.py`. It rebuilds $t_0,t_H,t_L,g_H,g_L$ by integrating the sale rule over $R\sim U[0,r]$. It integrates (A.7) and the state entry probabilities in the flow variable $x$, not in the arcsine variable of Lemma CD.6. It evaluates investor payoffs against fixed schedules by adaptive quadrature in $x$, with a golden-section refinement. It writes `referee/recheck.csv`; the console log is `referee/recheck.log`.
- `referee/recert.py` reruns `certify.certify_law` in memory for all ten laws and compares with `certificates.csv`. All ten rows agree to every printed digit.

Status of my checks: the hand checks of proofs are analytical; the recomputed numbers are numerical diagnostics; the certificate rerun is a rerun of a computer-assisted proof, not a new one.

## 3. Result by result

| result | verdict | comment |
|---|---|---|
| Lemma CD.1 | holds | Cost independence gives $\Pr(\text{prepare}\mid\theta,P=\pi)=G(B_r(\mu_P(\pi)))$. Correct for general $F$ too. |
| Lemma CD.2 (a)–(f) | holds | (b) inversion is correct; $e$ is a Borel function of the price. (e) at a null pool the belief is unrestricted, which is harmless. (f) matches (A.3). |
| Theorem CD.3 (i)–(iv) | holds | (iv): minimal-pool consistency by the interval argument is correct, including the open-endpoint case. $\Pr(X\le-1)=\tfrac14(1+e^{-2/b})$ checked. |
| Theorem CD.3 (v) | holds, wording fixed | "Earns less than $-ks$" should be "at most". Existence via CD.4 uses $\Delta_Tg_{1/2}\le\Delta_Tg_M<2M\Delta_Tg_M<2k$; correct. |
| Corollary (regimes) | holds with fix | Row II, first column, is open for $\bar k_G<k\le M\Delta_Tg_M$. Fixed. |
| Proposition CD.4 | holds | The mixed case is handled: $\sigma_H=\sigma_L$ by injectivity, then sign restrictions force $\delta_0$. |
| Proposition CD.5 | holds | (A.6) with $\rho\to g_m$. Required floor mass $0.22310$ at $r=3$ reproduced. |
| Lemma CD.6 | holds | Change of variables verified by hand. Arcsine form and $x$-integration agree: $J(3)=0.0955028924$ both ways. Uniform antiderivative verified. |
| Proposition CD.7 | holds with fix | (b): reverse-hazard argument correct. (c): the parenthetical "(regime II)" misses the tie case $\mu_0=\tfrac12$ with an atom, where the interval is unbounded (T5, row $c'=4.2917$). Fixed. |
| Lemma CD.8 | holds | Strict concavity of the low type's payoff on $A\subseteq[0,\infty)$ is correct. Numerically, against the fork's full-order schedule the low type's best short is $0.985$ at $r=2.00$ and $1$ at $r=2.05$, around the root $2.0155$. |
| Corollary CD.9 | holds | The last sentence, about an atom, sits under the hypothesis "atomless"; it is a contrast, not part of the corollary. Consider moving it. |
| Proposition CD.10 | holds with fix | (a) needs injectivity of Laplace convolution to get "$\mu_X$ not a.s. $\tfrac12$" from $\sigma_H\ne\sigma_L$. Fixed by citing CD.4. |
| Proposition CD.11 | holds | Jensen and the $\mathsf O_H$ identity are correct; $h>r$ is used correctly. |
| Text after CD.11 | holds with fix | $\beta\operatorname{Var}(\mu_P)=0.029644$, not $0.0297$. The sentence "the entry reversal needs mass above the prior profit" had no proof; I added a three-line proof. |
| Lemma CD.12 | holds | It can be sharpened. The ratio bound also gives $f(x-s)\le e^{2/b}a_L(x)$, so $\min\{e_H,e_L\}\ge ke^{-2/b}/\Delta_T$ whenever either type trades. |
| Proposition CD.13 (a)–(c) first part | holds | The $\delta^2$ expansion is correct, including the factor $1/24$. At $r=3$ the prediction matches the exact change to a relative error of about $10^{-4}$ for $\varepsilon\le0.05$ and $4\times10^{-4}$ at $\varepsilon=0.1$. |
| Proposition CD.13 (c) second sentence | unclear | "Falls at first order in $\varepsilon$" has no proof and is imprecise. It is first order in $\varepsilon-\varepsilon^*$ with $\varepsilon^*=(M-\tau)(g_H-g_L)$, and a jump at $\tau=M$. Fixed and relabeled as numerical diagnostic. |
| Proposition CD.13 (d) | holds with fix | The statement is true, but the cited Lemma CD.12 bounds only $\max\{e_H,e_L\}$, which gives $\mathsf E\ge ke^{-2/b}/(2\Delta_T)$. The sharpened min bound above closes the gap. Fixed. |
| Theorem CD.14 (i), (ii) | holds | Portmanteau and dominated convergence are applied correctly. |
| Theorem CD.14 (iii) | holds with fix | Two gaps: the limit $x'_\infty=+\infty$ is not excluded in the text (it is excluded by $U_n(1)\ge0$ against a limit payoff of $-k$), and the "only if" needs $k<(1-\tfrac1b)J$ strictly. Fixed. |
| Theorem CD.14 (iv) | holds with caveat | Logically correct, but "every equilibrium" is vacuous if none exists. Existence when (CD.1) fails is proved only for $k\le\bar k_G$. Caveat added. |
| Corollary CD.15 | holds | $c_L\le B_r(m)<B_r(\bar\mu(x^*))=3.1948$ checked. |
| Text after CD.15 | holds with fix | "Mass anywhere below $B_r(\tfrac12)$ cuts the family" is true for the half-line family. The full-order family ends at $2.614$, so it is cut only for $c'<3.945$. Fixed. |
| Headline (Section 2) | holds with fixes | Two overclaims fixed: regime III needs small $k$; "affine cost law makes the investor an insider at every price" needs a floor. A counterexample is $U[B_r(m),12]$, which is affine on $[B_r(m),B_r(M)]$ with $g_m=0$. |
| Section 6.1 | holds with fix | Same regime III qualifier. |
| Section 6.2 | partly unclear | The status line "analytical by direct computation" is too broad. Payoff formulas, the band width, and the state-dependent materiality identity are analytical. The $b\to\infty$ and $b\to0$ limits, item 4, and the ranking are informal. Relabeled as open. |
| T2 and "F.3(ii) is computer-assisted" | holds with fix | The certificate code is a valid lower Riemann sum: $G\circ B_r$ is nondecreasing, the weight is bounded below by its interval extension, and the domain shrink lowers a nonnegative integral. But the certified margin is $0.0277493$, so the text "$\ge0.02775$" overstated it. Fixed to $\ge0.02774$. F.3(iii) at $r_2=3.6$ ($B_{3.6}(M)=5.9973<6$) is not certified by this track; the note does not claim it. |

## 4. Numbers reproduced

`referee/recheck.csv` has 92 rows: 83 agree with the note within the displayed precision, 7 are informational (no note value), and 2 disagree. The two disagreements are one number computed two ways, the $0.0297$ of Section 4.4, now fixed to $0.0296$. Run `python3 recheck.py` from `referee/`; it takes about five minutes. The agreeing values include the following.

- Payoffs from the integrated sale rule equal (4) at $r=3$ to machine precision. $B_3(m)=2.36618$, $B_3(\tfrac12)=4.29167$, $B_3(M)=6.21715$; $x^*=0.871222$; $\tau=0.705$.
- T1, all six laws: pool probability, $J$, $\mathsf E$, $\mathsf O_H$. For example, the fork gives $0.636324$, $0.0955029$, $0.363676$, $0.265590$, and $U[3,9]$ gives $0.401116$, $0.0698685$, $0.254635$, $0.177591$.
- T3: $J$ at $\varepsilon\in\{0.25,0.5,1,1.5\}$, and the full-order cutoff ends $2.4781$, $1.9491$, $1.6207$, $1.4981$ by bisection on the integrated $J$.
- The fork's full-order cutoff end $2.61400$, by the closed form and by bisection.
- T4: $J$ and $\mathsf E$ for $\rho\in\{0.25,0.1,0.01\}$, and the identity $\mathsf E_\rho-\mathsf E_{\rm fork}=\rho\Pr(X<x^*)$.
- T5: the largest consistent cutoffs $-0.3496$, $0.5932$, $1.3203$, $2.9107$, $5.0365$; $B_3(\bar\mu(x^*))=3.19485$.
- T9: full orders start at $r=2.01552$ (fork), $2.01554$ ($\varepsilon=0.1$), $2.01612$ ($\varepsilon=0.5$), and end at $3.70255$ and $4.35066$. $r_C(6)=3.59266$, $r_C(5.9)=3.86572$, $r_C(5.5)=4.95855$.
- Section 6.2: $b\le2/\operatorname{logit}\tau=2.29562$ at $r=3$.
- T8 grid points, checked by quadrature best responses against the fixed schedule: $U[3,9]$ at $r=1.90$, $(1,-0.443)$: the low type's best short is $0.4425$, the high type's best order is $1$, no pool. At $r=1.95$, $(1,-0.530)$: best short $0.5296$, pool probability $0.3686$. At $r=2.10$, $(1,-0.815)$: best short $0.8146$, pool probability $0.3804$. The fork at $r=2.00$, $(1,-0.98)$: best short $0.9804$.
- End of the $\varepsilon=0.1$ branch at $r=3.70$: $\mathsf E=0.10476$, $e_L=0.0564$, against the bound $ke^{-2/b}/\Delta_T=0.0075$.

## 5. Status labels

- Analytical labels on CD.1–CD.15 are earned after the fixes above.
- T2 is earned as computer-assisted. One presentation point: `render.py` rounds certified lower bounds to nearest, so a lower bound $0.0954987$ shows as $0.09550$ and a margin $0.0277493$ shows as $0.02775$. Lower bounds should be rounded down.
- Grid rows are correctly labeled numerical diagnostic. The grid searches only pure orders, the minimal pool, and half-line pools from five starts. The note says so in open items 1–3.
- The note's T9 is assembled by hand, not by `render.py`, although Section 5 says all tables are generated. Fixed by a caption note.

## 6. Code findings

1. `solve.py`, `full_order_boundary_rows`: the column `x_pool_end_nonnegative` is the constant `True`. It is not computed. The property is true analytically for the three regime III laws, so no number changes, but a check should compute what it reports.
2. `family_r3.csv`: the column `pool_belief_formula` uses the full-order formula (F.2) even at partial-order fixed points such as $(1,-0.7585)$. The grid's own consistency test uses the actual orders, so no result changes, but the column is misleading past $x'=2.614$.
3. `core.regime` and `no_trade_exists` decide ties by floating-point equality. This is fine at the declared laws, and `certify.py` decides the $r=3$ labels exactly, but the `regime_map.csv` labels at ties are not certified.
4. `grid.py` and `core.py` are otherwise correct: payoffs use $q(V_T-P)-k|q|$ with the right signs, the pool belief uses the actual flow densities, and the state entry integrals use the right shifts.

## 7. Requests to the author

1. Prove existence of some equilibrium when (CD.1) fails and $k>\bar k_G$, or state it as open next to every "every equilibrium" claim. The $U[3,9]$ branch on $[1.75,2.20]$ is the test case.
2. Adopt the sharpened Lemma CD.12, $\min\{e_H,e_L\}\ge ke^{-2/b}/\Delta_T$. It also tightens the fork's Proposition F.2(b).
3. State the regime III sentence everywhere with its trading-cost range.
4. Use directed rounding for certified bounds in `render.py`.
5. Either prove the limit statements of Section 6.2 or keep them as open remarks.
