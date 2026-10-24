# XP1b: short independent check of round 2

Date: 23 October 2026. Scope: the four new rows, Remark 1, the eleven repairs, and the prior cutoff.

**The four rows and Remark 1 pass. All eleven repairs pass their spot-checks. One prose cutoff still needs its exact symbol.**

The calculations use calibration B through a separate CLI script. The script imports no checked module.
The checked files stay unchanged. No tests or outside sources enter this check.

## 1. Four new rows: PASS — computer-assisted

The independent script is `scripts/XP1b/xp1b_recompute.py`. Its output is `scripts/XP1b/xp1b_recompute.log`.
The file `scripts/XP1b/xp1b_intervals.csv` records the full rational endpoints.

Every registry enclosure contains the complete independent interval. Both independent endpoints give the stated display.

| Key | Independent outward interval | Display | Verdict |
|---|---|---|---|
| `entry_cmend_B` | [0.560585556360065228431303, 0.560585556360065228431304] | 0.560586 | PASS |
| `margin_tau_rN_half_B` | [0.154463130865439596022370, 0.154463130865439596022371] | 0.154463 | PASS |
| `margin_pimax_tauA_B` | [0.009320084909702358395434, 0.009320084909702358395435] | 0.009320 | PASS |
| `margin_u_kstrong_B` | [4.615051504874288097973045, 4.615051504874288097973046] | 4.615052 | PASS |

The formulas are

\[
\begin{aligned}
\mathsf E_*&=\rho+(1-\rho)(b+\pi_{\max}\lambda),\\
\texttt{margin\_tau\_rN\_half\_B}&=\tau(r_N)-\tfrac12,\\
\texttt{margin\_pimax\_tauA\_B}&=\tau(r_*)-\tau(r_A),\\
\texttt{margin\_u\_kstrong\_B}&=\tfrac{19}{3}-(e-1).
\end{aligned}
\]

The last expression is the slack in the equivalent condition \(u<19/3\).
It is not the payoff slack \(\rho\kappa\Delta_1-k\).

The script derives the auction objects from their piecewise integrals.
The shared auction formulas agree with equation (4) of the pinned `main.tex` at commit `01bd5d6`.
It brackets the three roots independently:

\[
\Delta(r_A)[1-\tau(r_A)]=k,\qquad
\rho\Delta(r_*)\tau(r_*)=k,\qquad
\rho\Delta(r_N)/2=k.
\]

Exact rational bisection gives widths below \(10^{-80}\), with opposite residual signs at the endpoints.
Natural interval arithmetic propagates these brackets through every formula.
The exponential certificate uses

\[
S_{100}=\sum_{n=0}^{100}\frac1{n!},\qquad
S_{100}<e<S_{100}+\frac{102}{101\cdot101!}.
\]

The geometric bound on the exponential tail gives the upper endpoint.
Every decimal lower endpoint rounds down; every upper endpoint rounds up.

## 2. Remark 1 at the CM endpoint: PASS — analytical, with computer-assisted values

The statement is right at the exact prior \(\pi_{\max}=\tau(r_*)\).
The independent brackets give

\[
r_*=1.634217965673085473652886\ldots,\qquad
\pi_{\max}=0.650059160618111936396861\ldots.
\]

Under CM, the two equilibria use these components, with orders listed as \((-1,0,1)\):

| Component | No trade | Informative trade |
|---|---|---|
| Investor orders | \((\sigma_H,\sigma_L)=(\delta_0,\delta_0)\) | \((\delta_1,\delta_0)\) |
| Posteriors | \((\pi,\pi,\pi)\) | \((\pi,\mu_0,M(\pi))\) |
| Entry | \((\rho,\rho,\rho)\) | \((\rho,\rho,1)\) |
| Prices | \(t_0+\rho[t_L-t_0+\Delta\pi]\) at every order | \(t_0+e(x)[t_L-t_0+\Delta\mu(x)]\) |
| High-cost preparation | Zero at the common price | Zero after sale and zero order; one after purchase |
| Bids | Truthful | Truthful |

The informative posterior values are

\[
\mu_0\in[0.454139509157646915271487,\ 0.454139509157646915271488],
\]
\[
M(\pi_{\max})\in[0.834698467246826669046413,\ 0.834698467246826669046414].
\]

Bayes' rule gives these posteriors from the stated orders.
The informative prices satisfy \(P(0)<P(-1)<P(1)\), so each price reveals its order posterior.
The price formula then gives competitive prices directly.
Preparation follows the threshold rule at each price.

At every posterior equal to \(\pi=\tau\), CM permits high-cost abstention.
The zero-order posterior lies below the threshold; the purchase posterior lies above it.
Thus the stated preparation rules are optimal.

The script prints all six investor payoffs against each fixed price and entry function.
The decisive payoffs are

\[
\begin{aligned}
U_H^N(1)&\in[-0.009233569478533458317307,\,-0.009233569478533458317306],\\
U_H^F(1)&\in[0.000342952490169732737184,\,0.000342952490169732737185],\\
U_L^N(-1)&=U_L^F(-1)=\rho\Delta(r_*)\pi_{\max}-k=0.
\end{aligned}
\]

Every wrong-sign payoff is negative. Abstention earns zero.
The low class can abstain at its exact tie under both IM and I0.
The high class strictly abstains in N and strictly buys in F.
Thus coexistence holds under both (IM, CM) and (I0, CM).

Under C1, the no-trade tuple requires entry one at every order.
Its low-class sale then earns

\[
\Delta(r_*)\pi_{\max}-k=k(1/\rho-1)=3/50>0.
\]

Thus no trade fails under C1. Both C1 coexistence sets are empty at this endpoint.
The printed margin 0.000343 and informative entry 0.560586 are correct.

## 3. Eleven repairs: PASS — analytical or computer-assisted, as listed

Locations below refer to `proofs/P1_core.tex`, unless another file is named.
Each row addresses the same numbered item in `XP1_check.md` §10.

| Item | Verdict and evidence |
|---|---|
| 1 | **PASS; analytical.** Lines 131–136 and BRIEF §2 define the mass ratio and give the correct conditional odds. |
| 2 | **PASS; analytical.** Lines 280–290 state Bayes consistency, competitive prices, the entry floor, and the spread restriction. |
| 3 | **PASS; analytical.** Lines 394–396 add the informed abstention mass \(\lambda\mathbf1\{x=0\}\) in both classes. |
| 4 | **PASS; analytical.** Lemma 2(f), lines 232–275, supplies direct price algebra; the product proof uses it before E2–E4. |
| 5 | **PASS; analytical.** Lines 1113–1115 split the interval at \(r_J\) and give the correct sets under all four rule pairs. |
| 6 | **PASS; analytical.** Lines 799–803 give the full CM entry interval at \(r_C\); statement (b) repeats the qualification. |
| 7 | **PASS; analytical.** Lines 915–932 restrict both root domains; Proposition 5 treats priors above \(\tau(r_2)\) directly. |
| 8 | **PASS; computer-assisted.** Remark 1 distinguishes both investor rules and both challenger rules; Section 2 above independently verifies the endpoint. |
| 9 | **PASS; computer-assisted.** `p1_common.py:207–268` prints outward endpoints; `p1_numbers.py:254–260` subtracts full brackets; all 70 shared enclosures contain XP1's exact intervals. |
| 10 | **PASS; analytical.** Lines 1332–1334 attribute 1.460985 to calibration A and state the brief's correct B value, 1.467127. |
| 11 | **PASS; computer-assisted.** Tables 4–5 use exact cutoff symbols and add the derived margins; lines 1270–1289 separate domains, weak restrictions, and ties. |

The saved PDF includes Remark 1, the endpoint table, and the revised margins tables.
This check read its text without a rebuild.

## 4. Prior cutoff and the account of round 1: scope confirmed; prose needs correction

**Analytical.** The precise exclusion under C1 is \(\pi\ge\pi_{\max}\).
At calibration B, CM permits coexistence at equality under both investor rules.
For \(\pi>\pi_{\max}\), no strength permits coexistence under any of the four rule pairs.
Thus the rule qualification changes the exact endpoint, not the strict upper range.

**Computer-assisted.** The literal claim “from 0.650059” is false even under C1.
That decimal lies strictly below the exact cutoff.
The real inputs

\[
\pi=0.650059,\qquad r=1.634217
\]

give coexistence under (IM, C1), and also under (I0, C1).
The independent script prints positive margins for every required condition:

\[
\begin{aligned}
\tau(r)-\pi&=0.000000123224474571957372\ldots>0,\\
k-\rho\Delta(r)\pi&=0.000000054028256938108586\ldots>0,\\
J(r)-k&=0.023065620990186459910678\ldots>0,\\
M(\pi)-\tau(r)&=0.184639246601133482967623\ldots>0,\\
\Delta(r)[1-M(\pi)]-k&=0.000342914551010856253040\ldots>0.
\end{aligned}
\]

The no-trade tuple has entry \(\rho\); the informative tuple has a strict full purchase and low-class abstention.
These margins verify both tuples, including the stricter I0 purchase condition.

Replace the prose cutoff with \(\pi_{\max}\), then state its decimal as an approximation.
This affects `P1_core.tex:1337–1338` and point 2 under “Refuted or corrected” in `memos/P1_core.md`.
The exact Proposition 5 and Remark 1 already use the correct boundary.

**Analytical.** The current enumeration code retains the missing CM candidate correctly.
At `p1_enumerate.py:116–119`, a prior tie uses entry \(\rho\) under CM and keeps abstention when its return permits it.
This is the required correction: CM can support no trade at \(B(\pi)=c_H\).

**Open: historical attribution.** The retained round-1 folder contains its memo, proof, registry, and logs, but no original enumeration source.
Its log scans other priors only under IM and C1.
Thus the exact historical code defect cannot be verified from that snapshot.
The stated defect explains the omitted candidate and agrees with the current repair.
The independent payoff calculation establishes the corrected result without that historical attribution.

## 5. Files and verification

The new files are:

- `memos/XP1b_check.md`;
- `scripts/XP1b/xp1b_recompute.py`;
- `scripts/XP1b/xp1b_recompute.log`;
- `scripts/XP1b/xp1b_intervals.csv`;
- `scripts/XP1b/checked_sources.sha256`.

The real CLI run used:

```bash
bash audit/slot_manuscript_2026_10_23/scripts/_slots/run_slot.sh .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/XP1b/xp1b_recompute.py
```

It completed normally and printed the intervals, both fixed tuples, their payoffs, and the registry comparisons.
All ten fresh interval comparisons agree; all 70 shared enclosures contain the prior independent intervals.
The recorded hashes show no change to the checked source files or PDF.
The mathematical items in the requested scope pass. The exact historical source attribution stays open.
