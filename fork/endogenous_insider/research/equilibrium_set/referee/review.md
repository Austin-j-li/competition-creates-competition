---
title: "Referee report on the equilibrium-set track"
subtitle: "fork/endogenous_insider/research/equilibrium_set/note.md"
date: "2026-10-03"
---

## 1. Scope and method

I read `note.md`, `core.py`, `certify.py`, the three solvers, `render.py`, the CSV outputs and `tables.md`. I read the fork's `mechanism.md` in full and the paper's (4), (7) to (12), (A.3) to (A.13), Propositions A.1 to A.4 and conditions (A1) to (A3).

For each result I tried to refute it. I checked each proof step, the signs, the edge cases (tie rule, $\tau=M$, $\tau\le\tfrac12$, atoms, mixed strategies, measurability) and whether the stated status is earned. I then recomputed the key numbers with code that shares nothing with the author's quadrature layer. The scratch files are in this folder:

- `recheck.py` and `recheck.csv`: adaptive quadrature (scipy) of (F.3), (ES.2) and (A.4) from the definitions, brute-force best responses, roots, slopes, the edge and plateau equilibria, the hole and band numbers.
- `recheck2.py` and `recheck2.csv`: (ES.2) against quadrature; Lemma ES.2 and Proposition ES.2(a) on 2,000 random mixed profiles; least and largest entry as functions of $z$.
- `certify_rerun.py`, `certify_rerun.log`, `certificates_rerun.csv`: a rerun of the author's interval certificates, plus a box-by-box audit of the cover below $r_e$.
- `adversary.py`, `adversary.csv`, `adversary_mixed.csv`: a search for live equilibria with an interior or mixed high-type order against entry sets bounded above and two-piece sets, which the author's scans did not use.
- `below_edge_general.py`, `below_edge_general.csv`: below $r_e$, the low type's necessary condition for every pure high-type order on a grid and for random high-type mixtures.

Every number in these files is a numerical diagnostic, except the 40-digit roots, which only confirm the author's interval enclosures.

## 2. Summary verdict

The track is sound. Every analytical proof I checked is correct, up to four small statement errors that I fixed in place. All certificates reproduce exactly. All key numbers reproduce to $10^{-13}$ or better. The stated status of each result is earned, with one exception of interpretation: Section 6.1 said that $r_1$ in Proposition F.3 can be any strength in $[r_e,r_C]$. That is false for F.3 as stated, because F.3(ii) asserts full orders, and full orders fail below $r_J$. I fixed the sentence.

The strongest results hold. These are the closed form (ES.1), the analytical proof of F.3 at the benchmark, the exactness of the F.2(c) test with $r_J$, the edge $r_e$ for $\sigma_H=\delta_1$, and the plateau equilibria. The adversarial search found no live equilibrium with an interior or mixed high-type order. Below $r_e$ it found no high-type strategy at all that meets the low type's necessary condition. This supports the note's "numerical diagnostic" label for the general "only if" claim.

I applied thirteen marked fixes in `note.md` (search for "Referee fix"). None changes a number or a status. Section 5 below lists them.

## 3. Result-by-result verdicts

**Lemma ES.1 (closed form; analytical). Holds.** I checked $g=e^{-1/b}/[4b\cosh(x/b)]$ on $|x|\le1$, the antiderivative $2b\arctan e^{x/b}$, the tail $g=f(x+1)/(1+e^{-2/b})$ on $x\ge1$ and its integral $m/2$. Quadrature of (F.3) gives $J(3)=0.09550289242400385$, inside the enclosure.

**Proposition ES.1 (F.3 at the benchmark; analytical). Holds.** I redid each rational: $\Delta_T(1.2)=1/60$, $B_{1.2}(\tfrac12)=1153/240$, $B_3(\tfrac12)=103/24$, $\tau(3)=141/200$, $\tau(3.6)=4245/5804$, and the two bounds on $e$. The bound $J(3)\ge\Delta_T(3)m/2$ needs only $x^*(3)\le1$, which holds. So $(1-1/b)J(3)\ge m/6>1/24>1/50$. The proof relies on the fork's Propositions F.1(iv), F.2(c) and F.3, which I also checked; they are correct.

**Lemma ES.2 (signs and monotone posterior; analytical). Holds.** The wrong-sign step uses $A_H\ge0$. The log-concavity step is correct: with $q\ge0\ge q'$ and $x_1<x_2$ the four points satisfy $u\le v,w\le y$ and $u+y=v+w$. On 2,000 random mixed profiles the largest decrease of $\mu_X$ was $5\times10^{-16}$ (rounding), and $\mu_X\le\tfrac12$ on $x\le-1$. The half-line conclusion needs $\tau>\tfrac12$, which the note assumes throughout.

**Lemma ES.3 (the pool is consistent; analytical). Holds.** One step is implicit. The proof divides by $\Pr(X\in N)$. That probability is positive, because $\Pr(X\in N)=0$ would force $\Pr(H\mid X\in A)=\tfrac12<\tau$. The lemma does not depend on the sign of the orders.

**Lemma ES.4 (shapes of $U_L$ and $U_H$; analytical). Holds.** I checked $U_L''=F_L(0)e^{-s/b}(s/b-2)/b$ and $U_H''=F_H(0)e^{s/b}(2+s/b)/b$, and the three cases for the low type's maximizer.

**Lemma ES.5 (equal total residual; analytical). Holds.** It is Fubini on $a_\theta$. It needs correctly signed supports, which Lemma ES.2 supplies in equilibrium.

**Proposition ES.2 (structure; analytical). Holds with a fix.** Part (a): the bound $|x-q'|-|x-q|\le|q'|$ for $x\le0$, $q\ge0$ is correct; random mixtures stay at least $0.016$ below $\hat\mu$ on $x\le0$. Parts (b) and (d) are correct. Part (c) is correct as proved, but its statement said $\sigma_H$ puts no mass on $[0,\underline a]$ without the condition $\underline a<1$. When $\underline a\ge1$ that set contains $1$, where $\sigma_H=\delta_1$ puts all its mass; the plateau equilibria of ES.5 are examples. I fixed the statement. The $C^1$ property of $U_H$ is right: the kink of $f$ sits at one point and dominated convergence applies. The paragraph after the proof said that both profits depend only on $(k,b,z)$. For $U_H$ this needs $\sigma_H=\delta_1$; fixed.

**Proposition ES.3 (the sufficient test is exact; analytical, root computer-assisted). Holds.** Necessity is the corner case of Lemma ES.4(a) with $F_L(0)=e^{1/b}J$, valid because $x^*>0$. Sufficiency is the paper's (A.7) argument; I checked $h'(s)=-(s/b^2)e^{-(1-s)/b}$. At equality the low type's corner is still optimal and the high type's $U_H'$ stays strictly positive on $[0,1)$, so the region is closed. The monotone box bounds in `phi_J` are valid ($\Delta_T$ and $\tau$ increase, $K$ decreases in $\tau$). A 40-digit root of (ES.1) gives $r_J=2.01551644106010729$, inside the enclosure. A quadrature root gives $2.015516441060108$.

**Proposition ES.4(a) (admissible sets for $(1,-z)$; analytical). Holds with two fixes.** (i) As written, the "if and only if" fails at $z=0$ with a null entry set. That profile satisfies the challenger, the market maker and the low type, and $0\notin[n(r),1]$. Read "an entry set of positive probability". (ii) For $z=1$, $U_H(1)=J_A-k\ge k/(b-1)$, with equality only when $(1-1/b)J_A=k$. The equality $U_H(1)=kz/(b-z)$ holds for $z<1$. Both are fixed in place. The closed form (ES.2) matches quadrature to $5\times10^{-14}$ at 45 points. $G=\Psi(n(r),r)$ matches to $1.5\times10^{-14}$.

**Proposition ES.4(b) (no live equilibrium with $\sigma_H=\delta_1$ below $r_e$; computer-assisted). Holds.** The rerun of `certify.py` gives identical certificates. I audited the cover below $r_e$ box by box. Its 78 boxes have total area equal to the area of the domain $[1,r_e-10^{-5}]\times[0,1]$, so it leaves no gap. Each box has a strictly negative upper bound; the closest to zero is $-3.2\times10^{-8}$. I checked three implementation details. The endpoint accessors return point intervals, so all arithmetic stays outward. Box splitting through an interval midpoint leaves no gap, because the constructor takes the hull. Clipping $z$ to $[\underline n,1]$ and the arctan difference to $[0,\infty)$ only intersects valid enclosures with true constraints. I rederived $\partial_z\Psi$ in `psi_z_box`, including the $z$-dependence of $x^*(z)$, which cancels inside the arctan. Independent quadrature agrees: $\max_z\Psi<0$ at $r=1.25$, $1.40$, $1.55$, $1.62$, $1.65$ and $r_e-10^{-4}$, attained at $z=n(r)$. A 40-digit root of (ES.4) gives $r_e=1.65859082455114216$, inside the enclosure. The quadrature root, $1.6585908245509768$, lies $1.6\times10^{-13}$ below it, which is within the quadrature error.

**Proposition ES.4(c) (supported orders form $[n,z_U]$; no fold; computer-assisted). Holds.** On a 25 by 41 grid of $(r,z)$ over $[1.3,r_C]$, the quadrature $\Psi$ is strictly decreasing in $z$. The slopes at $r_e$ are $3.636$ for $z_U$ and $0.341$ for $n$, as stated. The note cites Table T2 for the slopes, but T2 does not list them. They follow from the first rows of `live_branch.csv`.

**Proposition ES.5 (plateau equilibria and the edge; analytical given the sign of $G$). Holds.** I checked $\mathcal U(n)=[1,\infty)$, $C_A=\pi C(n,r)$, $e_H=\pi/2$, $e_L=\tfrac\pi2(1-\tau)/\tau$, $\mathsf E=\pi/(4\tau)$, and the corner case $n=1$ at $r_C$. Brute-force best responses on a 401-point grid with refinement give $q_H=1$ and $q_L=-n$ to $10^{-8}$ at $r_e$, $r=2$ and $r=3$. The pool belief is below $\tau$ in each case. Entry is $0.3840228$ at $r_e$, $0.2193926$ at $r=2$ and $0.1147052$ at $r=3$, each equal to $\pi/(4\tau)$.

**Proposition ES.6 (holes at full orders; analytical). Holds with a fix.** Parts (a) and (c) are correct. In (b), the alternative least-entry sets $[x^*,1)\cup P$ exist only when $y\ge1$. If $y<1$ the least-entry set is $[x^*,y]$ up to null sets. Fixed. At $r=3$ I get $y=1.958892335$ with entry $0.1519539$, and a cutoff-family end $x'=2.614003697$ with entry $0.1525848$, matching the note.

**Remark ES.1 (preparation mixed at the indifferent atom; analytical). Holds** within the $q_H=1$ family. The only positive-probability set where the challenger is indifferent is the plateau at $z=n$, and the residuals there scale by $\pi$. Below $r_e$ the relaxation adds nothing, because $\pi C(n,r)\le C(n,r)$.

**Numerics of Section 5 (numerical diagnostic). Hold.** Every row of the live-branch table and the entry-band table matches my independent values to the printed digits. Entry along the minimal-pool branch rises up to $r_J$ and falls after it on the 196-point grid.

**"No member above the minimal-pool curve" (numerical diagnostic). Holds, and part of it is analytical.** For fixed $z<1$ the admissible sets must meet an equality on $\int_Af\mu_X$. The ratio $e^{z/b}\mu_X(1-\mu_X)$ is nonincreasing in $x$, so the reverse bathtub argument makes the cutoff set $[x'(z),\infty)$ the largest-entry admissible set. This step is analytical. The open part is only the monotonicity in $z$ of that cutoff entry. On five strengths my values of both least and largest entry increase strictly in $z$ (`recheck2.csv`).

**High-type mixtures and interior orders (numerical diagnostic; open in general). Hold as stated.** The author's scans use half-line entry sets and fixed holes. My search used sets bounded above and two-piece sets. It covered 1,399 pure schedules $(q,-z)$ with $q<1$ on which the low type's condition holds, and 5,022 schedules with two-point high-type mixtures. The high type's best response was always $0$ or $1$, never $q$, so none is an equilibrium. The necessary conditions I used are derived in Section 4.

**Section 6.1 "only if" for other high-type strategies (numerical diagnostic). Holds, but the note's own evidence below $r_e$ was thin.** The note's mixed scan starts at $r=1.66>r_e$. My check fills the gap. At five strengths in $[1.40,1.658]$ the low type's necessary statistic is negative for every pure high-type order on a 51 by 51 grid of $(q,z)$, and for 1,500 random high-type mixtures per strength. Its maximum always sits at $q=1$ (`below_edge_general.csv`).

**Section 6.1 "$r_1$ in F.3 can be any strength in $[r_e,r_C]$". Refuted as stated; fixed.** F.3(ii) asserts full orders, and (F.5) has strict inequalities. As stated it needs $r_1\in(r_J,r_C)$. The claim holds for a modified F.3(ii) with informed orders $(1,-z)$.

**Headline sentence "every measurable entry set with enough information mass works". Overstated; fixed.** It holds at full orders, which needs $r\ge r_J$. For $z<1$ the condition is an equality, and the high type's optimality against arbitrary sets is a numerical diagnostic.

**Section 6.2, 6.4, 6.5, 6.6 (interpretation). Hold with fixes.** Item 2 compared the high type's level profit with the low type's marginal profit. I rewrote the evidence; the conclusion stands. Item 4's $U_H$ formula needs $\sigma_H=\delta_1$. Item 5's cutoff-family span rounds to $[0.153,0.364]$. Item 6's heading claimed that mixed insiders never appear, but a high-type mixture inside $(\underline a,1]$ is open.

## 4. A derivation used by the adversarial search

Take a pure live profile $(q,-z)$ with $q\in(0,1)$ and $z\in(0,1)$. Lemma ES.5 gives $F_H(q)=F_L(z)$, and the low type's first-order condition gives $F_L(z)=kb/(b-z)$. The high type's first-order condition is $F_H(q)+qF_H'(q)=k$, so $qF_H'(q)=-kz/(b-z)$. The bound $|F_H'|\le F_H/b$ then gives $kz/(b-z)\le qk/(b-z)$, that is $z\le q$. Entry needs $q+z\ge1+n(r)$. So an interior pure equilibrium needs $q\ge(1+n(r))/2$. The search grid covers this region. Status: analytical for the necessary condition; the search itself is a numerical diagnostic.

## 5. Fixes applied to `note.md`

Each fix is marked "[Referee fix: ...]" next to the original text, which I kept.

1. Section 2, headline: qualified "every measurable entry set with enough information mass works".
2. Proposition ES.2(c): "no mass on $[0,\underline a]$" holds when $\underline a<1$.
3. Remark after ES.2: the $U_H$ formula needs $\sigma_H=\delta_1$.
4. Proposition ES.4(a): "an entry set of positive probability"; for $z=1$, $U_H(1)\ge kz/(b-z)$.
5. Section 4.4: "only $\mathcal D$ remains with $\sigma_H=\delta_1$" reworded, since $\mathcal D$ has $\sigma_H=\delta_0$.
6. Proposition ES.6(b): the alternative least-entry sets need $y\ge1$.
7. Section 4.5, mixed orders: the same restriction as fix 2.
8. Section 4.5, mixed orders: what the two scans test, and that the mixed scan starts above $r_e$.
9. Section 6.1: the claim about $r_1$ in Proposition F.3.
10. Section 6.2: the level-versus-marginal comparison.
11. Section 6.4: the $U_H$ formula needs $\sigma_H=\delta_1$.
12. Section 6.5: the rounded span without holes.
13. Section 6.6: the overstated heading.

## 6. Issues not fixed

1. **Tie-rule dependence (substantive, not an error).** Two features depend on the tie rule. These are the closedness of the live set $[r_e,r_C]$ and the existence of the plateau equilibria, which give the least entry $\pi/(4\tau)$. Under the opposite rule, where an indifferent challenger stays out, the live set with $q_H=1$ is $(r_e,r_C)$. The least entry is then an infimum that no equilibrium attains. The jump at $r_e$ survives as a limit. One sentence in Section 4.4 or Section 7, item 4, would make this explicit.
2. **Status of Section 6.1.** The "if and only if" for all high-type strategies rests on the numerical diagnostic for strategies other than $\delta_1$. The note says this correctly. It should cite the new evidence below $r_e$ if the author adopts it.
3. **Code conventions (minor).** Several functions in `certify.py` and `core._golden` lack type hints. The docstring of `certify.py` says it writes "two cover CSVs", but it writes only `certificates.csv`. The track writes no run manifest (inputs, method, tolerances, versions, output hashes, pass/fail), which the repository convention asks for.
4. **Table citation (minor).** Section 4.4 cites Table T2 for the slopes $3.6$ and $0.34$; T2 does not show them.

## 7. Suggested next step

The note's open item 1 aims to prove that $q_H=1$ in every live equilibrium through the sign of $U_H''$. There is a shorter route to the main use of that result, the "only if" in Section 6.1. Below $r_e$ the low type's necessary condition already fails for every high-type strategy I tried, and its maximum over strategies sits at $\sigma_H=\delta_1$. Consider the statistic $\sup_{A\subseteq\{\mu_X\ge\tau\}}\Delta_T\int_Af\mu_X$ as a function of $\sigma_H$ on $[0,1]$. A proof that $\delta_1$ maximizes it, for each $z$, would combine with the certificates of Proposition ES.4(b). The "only if" part of Section 6.1 would then become computer-assisted for every equilibrium, with no claim about the high type's optimality. The posterior under $\sigma_H$ is not pointwise below the posterior under $\delta_1$, so the proof needs an integral argument, not a pointwise one. Status of the conjecture: open, supported by a numerical diagnostic.
