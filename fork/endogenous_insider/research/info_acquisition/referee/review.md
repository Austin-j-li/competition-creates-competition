---
title: "Referee report: information acquisition in the endogenous-insider fork"
date: "2026-10-03"
---

## 1. Scope and method

I read `note.md`, `acquisition.py`, `render.py`, the CSV outputs, the fork note `mechanism.md`, and the paper's equations (4), (7) to (12), (A.3) to (A.13) and Propositions A.1 to A.4. I tried to refute every result. I checked each proof step by hand. I re-ran the author's solver in a separate copy. I wrote an independent re-implementation, `check.py`, which does not import the author's code. It finds every threshold by root-finding and every integral by adaptive quadrature or `mpmath`, and it checks investor optimality by a global scan over order sizes, not only by the sufficient test. Its output is `check_results.csv`. The scratch file `entry_check.py` computes the preparation probability at $\lambda<1$.

All referee numbers are floating-point quadrature without interval enclosure. Their status is numerical diagnostic.

## 2. Summary

The algebra is sound. Every proof that the note labels analytical survives a line-by-line check, and every closed form matches an independent quadrature: $J$ to $10^{-10}$, the others to the printed precision. The solver reproduces byte for byte. The problems are in the claims that summarize the results. Four summary claims were stronger than the proofs:

1. The headline said an acquisition equilibrium exists "exactly when" $\kappa\le U^*(r)$. Only sufficiency is proved. The note's own Section 4.3 says the exact ceiling is open.
2. The headline said mixed-acquisition equilibria exist "only" in a narrow band just below $U^*(r)$. This is false outside the minimal-pool branch. Larger pools give mixed-acquisition equilibria at much lower costs. At $r=3$ I find full-order mixed equilibria that pass the sufficient test for $\kappa$ down to about $0.023$, against a stated band floor of $0.0724$ (numerical diagnostic).
3. The headline and Section 6 placed the insider range at $(\mathfrak r(k),r_C)$. The right end $r_C$ belongs to it under the tie rule.
4. Proposition G.5(iv) claims as analytical that mixed equilibria disappear as $\kappa\downarrow0$. The proof rests on a branch-only floor whose monotonicity part is a numerical diagnostic. The clause is open.

There are also two smaller logical gaps. The jump dynamic in the proof of Proposition G.3(iii) does not support the attractor claim in Remark G.1. The forward-induction step in Proposition G.6 needs a strict inequality. I fixed all of these in `note.md` and marked each fix "[Referee fix: ...]". Section 5 lists them.

## 3. Result-by-result verdicts

**Lemma G.1 (dilution bound; analytical). Holds.** The ratio bound $e^{-1/b}f(x)\le f(x-q)\le e^{1/b}f(x)$ is correct for $|q|\le1$. The derivative numerator $a-d>0$ is correct. The solution for $\lambda_{\min}$ and the identity $\lambda_{\min}=1$ at $\tau=M$ check: $(a-1)-Mu=(a-d)/(a+d)=2M-1$. Independent check: the plateau posterior under full orders matches (G.3) to $3\times10^{-16}$. A random search over 400 mixed order profiles at $\lambda=0.9$ never exceeds $M_{0.9}$. Root-finding reproduces every $\lambda_{\min}$ in Table 2.

**Lemma G.2 (structure at fixed $\lambda$; analytical). Holds.** The exponents $|x|-|x-q_H|$ and $|x|-|x-q_L|$ have the stated monotonicity, so the likelihood ratio is nondecreasing. The pool inequality is correct. The sign restriction $q_H\ge0\ge q_L$ is needed and is stated. Without it, the mixture with $f(x)$ can break monotonicity at $\lambda<1$.

**Proposition G.1 (no acquisition; analytical). Holds.** In (iii), "the entry set is null" is a Lebesgue statement, so it is null under every deviation's flow law, because all flow densities are positive. The proof uses this implicitly; it is correct. In (iv), the wrong-signed orders have nonpositive gross payoff, as claimed. The remark after the proof, that the three layers "coincide inside every equilibrium", holds only at the level of the equilibrium. In a mixed equilibrium a non-acquirer's flow lands in the entry set with positive probability, so $\theta$ is then material while nobody knows it. Verdict on the remark: holds with fix.

**Proposition G.2(i) (pure acquisition; analytical). Holds.** It is Proposition F.2(c) plus (E2). Strictness in orders follows from $U_\theta'>0$ on $[0,1]$ and the strict loss of wrong-signed orders.

**Proposition G.2(ii), closed form (G.4); analytical. Holds.** I re-derived $f(x-1)(1-\mu_X)=e^{-1/b}/(4b\cosh(x/b))$ on $(-1,1)$ and the plateau term $m/2$. The low type's plateau term is $\tfrac12e^{-2/b}M=m/2$, so $F_L(1)=F_H(1)$. Direct `mpmath` quadrature of (F.3) agrees with (G.4) to $10^{-10}$ at seven strengths.

**Proposition G.2(iii), monotonicity of $U^*$; analytical. Holds.** Each step checks: $\Delta_T'/\Delta_T=(r+\ell)/(r(r-\ell))$ is decreasing; $\cosh(x^*/b)=1/(2\sqrt{\tau(1-\tau)})$; $G'(\tau)=-(e^{-1/b}/4)/\sqrt{\tau(1-\tau)}$; $\tau'=N'/D+\tau|D'|/D$ with the stated bounds; and $\tau(1-\tau)\ge Mm=1/(4\cosh^2(1/b))$ on $[\tfrac12,M]$. Formula (G.5) matches a numerical derivative to $10^{-6}$ at $r\in\{2.02,3,3.5\}$. The benchmark margin is $0.06630-0.01940=0.0469$. Combined with the test at $2.02$ (margin $1.25\times10^{-4}$), monotonicity of $J$ extends the full-order existence test from the grid point to the whole interval $[2.02,r_C]$. The exact crossing is $r=2.0155$. One inconsistency: Table 1 calls the benchmark arithmetic analytical, while open item 4 says an interval evaluation would lift it to computer-assisted. The fork uses the first reading for closed-form arithmetic. The note should pick one reading.

**Proposition G.2(iv), universal bound $\bar U$; analytical. Holds.** The proof cites "Lemma G.2(c)", which has no part labels; it means the inclusion $A\subseteq\{\mu^\lambda_X\ge\tau\}$. All eight $\bar U$ values in Table 2 reproduce.

**Headline: acquisition equilibrium "exactly when" $\kappa\le U^*(r)$. Refuted as stated; fixed.** Proposition G.2 proves sufficiency only. Other continuations, with other pools, partial or mixed orders, or $\lambda<1$, are not excluded from giving $V>U^*$. The only proved necessary bound is $\bar U(r)$, which is four times $U^*$ at $r=3$. On $(\mathfrak r(k),1.66)$ no live equilibrium was found and none is excluded.

**Headline and Section 6: no insider outside $(\mathfrak r(k),r_C)$. Refuted at the endpoint $r_C$; fixed.** At $r=r_C$, $\tau=M$, the entry set is the plateau, the tie rule admits preparation, and the full-order test holds ($(1-1/b)J(r_C)=0.0629>k$). My global scan confirms full orders are the best response. So an acquisition equilibrium exists at $r_C$ for $\kappa\le0.1058$. The correct range is $(\mathfrak r(k),r_C]$. At the left end, $\Delta_T=k$ still kills every order, because $F_\theta(s)<\Delta_T$ strictly. Propositions G.1(iv) and G.5(i), (ii) are stated with strict inequalities and are correct.

**Proposition G.3(i), (ii) (mixed acquisition; analytical). Holds.** At $\lambda_{\min}$ the posterior is strictly increasing on $(-1,1)$ and equals $\tau$ on the plateau. The two marginal conditions in (G.7) are the minima of the two types' marginal profits, and both derivative expressions are correct. My quadrature reproduces (G.8) at $r\in\{2.5,3,3.5\}$, and a global scan confirms full orders at $\lambda_{\min}$. The first grid strength with (G.7) is $2.20$; at $2.19$ the low type's condition fails.

**Proposition G.3(iii) (numerical diagnostic). Holds with fix.** I confirm that $V(\lambda,r)$ is increasing on $[\lambda_{\min},1]$ on 41 nodes at each strength. I confirm the rises $7.8\%$, $4.1\%$, $0.7\%$ and the first test node $0.931$ at $r=2.05$. At $r=2.05$ and $\lambda=0.70$ the low type's best response to the full-order schedule is a short of $0.869$. At those orders the largest posterior is $0.6587<\tau=0.6662$, so no pure profile of this kind supports entry. The "unresolved" label is the right treatment. The fix: the proof defined a jump dynamic $\lambda_{t+1}\in\{0,1\}$. Under that dynamic the interior equilibrium of Remark G.1 is not an attractor; it starts a two-cycle. A gradual adjustment dynamic gives both the repeller claim here and the attractor claim there. I changed the definition.

**Headline: mixed equilibria "only" in a narrow band. Refuted; fixed.** Fix $r=3$, $\lambda=0.95$, and the pool cutoff $x'=2$. Under full orders the entry set $[2,\infty)$ has posterior above $\tau$. The pool posterior is $0.443<\tau$. The sufficient test holds, and a global scan gives full orders as each type's best response. $V=0.0350$. So for $\kappa=0.0350$ this profile is a mixed-acquisition equilibrium of game A, far below the band floor $0.0724$. Along the larger-pool family where full orders pass the sufficient test at $r=3$, $V$ reaches about $0.023$ at every $\lambda\in[\lambda_{\min},0.95]$. The author's own grid at $r=2.05$ also contains partial-order fixed points on the minimal-pool branch with $V$ from $0.0191$ to $0.0214$, below the band $[0.0215,0.0219)$ of Table 4. The narrow band is a property of the minimal-pool full-order branch only. Open item 2 already says that larger pools pair with lower costs, so the headline contradicted the note's own open list.

**Remark G.1 (exogenous materiality; analytical). Holds with fix.** I re-derived the derivative numerator $N'D-ND'=-f_0(f_1-f_{-1})^2$, the symmetry $F_H(1)=F_L(1)$, and the endpoint values. Quadrature reproduces Table 6 ($0.3133$, $0.2981$, $0.2835$, $0.2697$, $0.2564$; the second is $0.29805$). The attractor claim needed the gradual dynamic; see above.

**Proposition G.4 (non-acquirer's short; analytical given the schedule). Holds.** The residual $e\,\Delta_T(\tfrac12-\mu_X)$ is correct. The shift identity $f(x+s)=e^{-s/b}f(x)$ holds on $x>0$. The single-crossing argument is correct. I checked $\Phi$, $s_U$, $U_U$ by the closed form and by direct maximization without the shift identity; the two agree to six digits at nine strengths. Two small corrections. The best short at $r_C$ is $0.996$, not $1.0$, because $(1-1/b)e^{-1/b}\Phi(r_C)=0.0199<k$. On the full-order schedule $\Phi(r)=k$ at $r=1.997$, so the short is profitable from the first full-order strength $2.0155$. The value $2.05$ in Table 1 reflects the fork's grid spacing. $\Phi$ is increasing along the full-order range.

**Proposition G.5 (competition creates insiders). (i), (ii), (iii), (v) hold. (iv) is unclear; fixed.** Parts (i) to (iii) and (v) are direct consequences of G.1, G.2 and Lemma G.1, and $\tau'>0$ gives $\lambda_{\min}\uparrow1$. In (iv), the clause "in (iii) the mixed equilibria disappear" needs a positive lower bound on $V$ over all live continuations at a fixed $r$. The proof cites $V(\lambda_{\min},r)$, which is a floor only on the minimal-pool full-order branch, only where (G.7) holds (not on $[2.02,2.2)$), and whose monotonicity is a numerical diagnostic. Larger pools and partial orders give lower $V$. Whether some positive bound survives is plausible but open. I relabeled that clause as open.

**Proposition G.6 (observable acquisition; analytical under the stated restriction). Holds with fix.** Two gaps. First, with the weak restriction $V\ge\kappa$, the cutoff $x'(\kappa)$ gives the deviator exactly $0$, its payoff in $\mathcal D$, so $\mathcal D$ is not strictly broken. The strict form $V>\kappa$ is needed. Second, "a higher acquisition cost selects a more informative price" had no proof. I added a garbling proof. A larger pool splits only the plateau cell, and on the plateau the split is a state-independent exponential kernel. The proof covers full-order members only. The numbers in Section 4.7 used the last grid node; quadrature gives $x'(0.05)=1.495$ and $x'(0.07)=0.992$. The sentence "by a standard refinement" overstated open item 5. The status "analytical under the stated restriction" is honest.

**Section 4.4 discussion of two forces. Holds with fix.** "The informed profit falls in $\lambda$ on a fixed entry set" holds for the average. The low type's residual $\mu^\lambda_X$ rises in $\lambda$ on $x>0$, because $\partial_\lambda\mu^\lambda_X$ has the sign of $g_H-g_L$.

**Table 3. Holds with fix.** The column labeled $\mathsf E$ is entry conditional on acquisition. The preparation probability at $\lambda<1$ adds the non-acquirer's flow: $0.337$ at $\lambda_{\min}$ against the printed $0.342$. The CSV columns `E` in the two profile files carry the same meaning.

**Numerics, Tables 1 to 6. Hold.** Every entry I recomputed agrees to the printed precision, except the items fixed above.

## 4. Independent numerics

| Object | Note | Referee | Agreement |
|---|---|---|---|
| $\mathfrak r(k)$ | 1.2210 | 1.220998 | yes |
| $r_C$ | 3.5927 | 3.592658519 | yes |
| $J(3)$, (G.4) against direct quadrature | 0.0955029 | 0.0955029 | $<10^{-10}$ |
| first grid $r$ with $k<(1-1/b)J$ | 2.02 | 2.02; exact 2.01552 | yes |
| (G.6) left / right | 0.0663 / 0.0194 | 0.06630 / 0.01940 | yes |
| $dJ/dr$ at $3$, (G.5) against numerical | | 0.054226 / 0.054226 | yes |
| first grid $r$ with (G.7) | 2.20 | 2.20 | yes |
| $V(\lambda_{\min},3)$, (G.8) against quadrature | 0.0724 | 0.07239 / 0.07239 | yes |
| $\lambda_{\min}(3)$ | 0.875 | 0.87463 | yes |
| rise of $V$ on $[\lambda_{\min},1]$ at $2.5,3,3.5$ | 7.8, 4.1, 0.7% | 7.79, 4.12, 0.68% | yes |
| $\Phi(2.05)$, $s_U(3)$, $U_U(3)$ | 0.0215, 0.80, 0.0106 | 0.02154, 0.7988, 0.010623 | yes |
| $s_U(r_C)$ | 1.0 | 0.9960 | fixed |
| strength where (G.9) lower bound equals $k$ | 2.09 | 2.0931 | yes |
| Remark G.1 $V(0)$, $V(1)$ at $r=3$ | 0.3133, 0.2564 | 0.313333, 0.256416 | yes |
| $\bar U(3)$ | 0.322 | 0.3220 | yes |
| $x'(0.05)$, $x'(0.07)$ at $r=3$ | $\le1.47$, $\le0.97$ | 1.4948, 0.9921 | fixed |
| mixed equilibrium, $r=3$, $\lambda=0.95$, $x'=2$ | none claimed below 0.0724 | $V=0.0350$, test holds | refutes "only" |
| live equilibrium at $r=r_C$ | none claimed | $V=0.1058$, test holds | refutes open interval |
| preparation probability at $\lambda_{\min}$, $r=3$ | 0.342 | 0.3371 | fixed label |

Reproducibility: a fresh run of `acquisition.py` in a separate copy reproduces all seven CSV files byte for byte in about eleven seconds.

## 5. Fixes applied to `note.md`

Each fix is marked "[Referee fix: ...]" in place. The author's text is kept, except where a word or a number was replaced; each such fix quotes the original.

1. Headline: "exactly when" to "whenever"; $(\mathfrak r(k),r_C)$ to $(\mathfrak r(k),r_C]$; "live range" to "full-order range"; branch qualifier and counterexample for the mixed band; forward-induction qualifier.
2. Section 4.2: the "layers coincide" remark holds at the level of the equilibrium only.
3. Proposition G.3(iii) proof: gradual dynamic replaces the jump dynamic.
4. Section 4.4: the "profit falls" force concerns the average.
5. Section 4.5: $s_U(r_C)=0.996$; the short is profitable from $2.0155$.
6. Proposition G.5(iv): the "mixed equilibria disappear" clause is open.
7. Section 4.6: $(\mathfrak r(k),r_C]$; "inside the range" is proved on $[2.0155,r_C]$ only.
8. Proposition G.6: strict restriction needed; garbling proof for the informativeness claim.
9. Section 4.7: $x'(\kappa)$ values; "standard refinement" softened.
10. Table 1: $\sup U^*$ is attained at $r_C$.
11. Table 3: column relabeled; true preparation probabilities given.
12. Table 4 status: the branch band at $r=2.05$ includes the partial-order nodes.
13. Section 6: $(\mathfrak r(k),r_C]$; "if and only if" to "if"; branch qualifier for the mixed band.
14. Figure description: the dashed line is a branch floor; the filled point at $r=2.05$ is not an equilibrium.

## 6. Recommendations not applied (outside `note.md`)

1. `acquisition.py`: rename the `E` columns of the two profile files to entry given acquisition, or add the true preparation probability.
2. `acquisition.py`: the definitions in `thresholds.csv` cite "Prop. 1 iv" and "Prop. 1 iii"; they mean Proposition G.1(iv). The definition of `U_star_sup` says "attained just below $r_C$"; it is attained at $r_C$.
3. `render.py`, panel (a): label the dashed line as the floor on the minimal-pool branch. Panel (b): do not draw the filled jump point where (G.7) fails, or draw it hollow.
4. Add one panel or table for the larger-pool mixed equilibria (open item 2). The referee check shows they are the bulk of the mixed set at $r=3$.
5. Decide the status of closed-form benchmark arithmetic once, and align Table 1 with open item 4.
6. Notation: the fork and the note use $\mathcal D$ for the dead profile, while Proposition A.4 of the paper uses $\mathcal D$ for the maintained domain.

## 7. What survives

The core contribution survives intact. Outside $(\mathfrak r(k),r_C]$ nobody learns $\theta$ at any $\kappa>0$, and this is analytical. The closed form $U^*(r)=J(r)-k$ and its monotonicity on $[2.0155,r_C]$ are analytical, so the sufficient ceiling is a ramp with a cliff just after $r_C$. The dilution floor $\lambda_{\min}(r)$ is analytical and gives a clean threshold form of the two-sided complementarity. The contrast with exogenous materiality in Remark G.1 is analytical and sharp. What does not survive is the claim that the mixed-acquisition set is a thin band: it is thin only on the minimal-pool branch.
