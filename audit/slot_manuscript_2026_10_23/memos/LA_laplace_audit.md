# Audit of the Laplace manuscript against the proof standard

Workstream LA, 23 October 2026. Read-only audit of `overleaf/paper` at commit `01bd5d6`
(`main.tex`, `online_appendix.tex`; below "the manuscript", "A.n" for its Appendix A, "OA A.n",
"OA B", "OA C" for the Online Appendix). Standard: BRIEF §5. Outputs of this workstream:

- this memo;
- `proofs/LA_worked.tex`, compiled to `proofs/build/LA_worked.pdf` (8 pages);
- `scripts/LA/margins.py`, with `margins.csv` (141 rows) and `margins_run.log`.

## 0. Summary

The manuscript meets the core of the standard on its main theorem. Proposition 2 checks each
condition against a fixed candidate. No step assumes its conclusion. Uniqueness rests on bounds
that hold for every profile: the posterior bounds of Proposition A.1, the entry floor $\rho$, the
residual bounds (11), and the derivative bound (A.6). Proposition 3 is an interval-certified
existence result at three strengths. Every strict hypothesis holds at the benchmark. Of the 141
quantities that I recomputed, 40 have a printed counterpart, and all 40 agree with it to every
printed digit. The other 101 are margins and auxiliary objects the manuscript does not print.

The manuscript falls short of the standard in form, not in substance:

1. No result displays its equilibrium as one explicit tuple. The components of Proposition 2
   sit in the statement, (A.8), (9), Proposition A.2 and the phrase "truthful bids".
2. The main text has no margins table. The Online Appendix tabulates four margins at
   $(r_0,r_1)=(1.2,3)$; Table 4 prints $c_H-B_2(M)$ for its four class cases. No part (iii)
   margin is printed at the benchmark. That margin is the thinnest in the paper:
   $c_H-B_{3.6}(M)=0.002689$, or $0.000334$ in posterior units, and $r_2-r_C=0.00734$.
3. The thresholds $\mathfrak r(k)$, $r_N$, $r_U$, $r_C$ are closed forms evaluated in floating
   point. The "lower" and "upper" columns in `numerics/thresholds.csv` are the two float
   neighbours of the value (`numerics/thresholds.py`, `nextafter`); they are not certificates. Interval enclosures are in `scripts/LA/margins.csv`.
4. The open parameter set is asserted ("open in $(r_0,r_1,c_H,k)$"), proved nonempty, but not
   tabulated. Section 4.2 prints three prior windows; their endpoints are closed forms, and I
   name the inequality that binds at each.
5. A repository-state gap: the printed numbers come from a run of 21 October on the branch
   `revision/alex-2026-10-21` (zero low cost). That branch is unmerged and unpushed. The
   numerical layer on `main` and in this working tree still declares `c_L = 1` and prints a
   net surplus of 2.382301 where the manuscript prints 2.632301 (Section 6).

I found no real gap in any proof of a numbered result (Section 2). The one failed hypothesis in
the paper, case D of Table 4, is reported by the manuscript as a failure.

## 1. Table of results (task 1)

Status labels are the manuscript's own. "Every profile" means the bound holds for arbitrary mixed
orders and every unilateral deviation in $[-1,1]$. Margin values are from `scripts/LA/margins.csv`
(exact rationals, or interval enclosures at 50 digits for quantities that involve $e$; the
enclosures below are rounded inward to the digits shown).

### 1a. Claim, label, location, object, verification, uniqueness

| Result | Claim (one line) | Label | Proof | Equilibrium object | Verification | Uniqueness |
|---|---|---|---|---|---|---|
| Prop. 1(a),(b) | A stronger incumbent lowers $g_H,g_L$ and raises $\Delta_T$ | analytical | A.1; OA A.2 | none (auction stage) | direct: Tonelli on indicator integrals (A.2) | n/a |
| Prop. 1(c) | Weakest class restriction for (b): $D\ge0$ above $p$, $D(p^-)\le0$ | analytical | A.1 | none | direct; converse by a two-point construction | n/a |
| Prop. A.1 | $m(\pi)\le\mu_X,\mu_P\le M(\pi)$ for every profile | analytical | A.1; OA A.1 | none; it is the every-profile lemma | direct: triangle inequality, Bayes, tower | n/a |
| Prop. A.2 | With $\Delta_T>0$ the price reveals $\mu_X$; residuals (11) with bounds | analytical | A.1; OA A.3 | holds for every candidate | direct inversion of (10); increment (A.3) | n/a |
| Prop. 2(i),(ii) | Weak: unique no trade, entry $\rho$. Strong: unique $(1,-1)$, entry $>\rho$, ownership rises | analytical | A.2; OA A.4 | orders in the statement; $\mu$ (A.8); $e,P$ (9); beliefs by A.2; bids. Not one display | direct, non-circular: Steps 3 and 5 check the fixed candidate | every profile: Steps 1 to 4 (posterior bounds, floor, residual bounds, $W^{1,1}$ derivative bound) |
| Prop. 2(iii) | Strongest: unique $(1,-1)$, entry returns to $\rho$ | analytical | A.2 "Part (iii)" (three sentences); OA A.5 | not displayed; see `LA_worked.tex` §1 | via Steps 4, 5 of (ii) | every profile; needs no price inversion (`LA_worked.tex` Step 2) |
| Prop. 3 | Equilibria $(1,-v_i)$ at $r=1.55,1.60,1.65$ with entry strictly ordered upward | computer-assisted | A.3; OA B | $(1,-v)$ with $v$ in an 8-decimal bracket; schedules (A.15). An enclosure, not a point | implicit: IVT on $\Psi(r,\cdot)$ for the low type; concavity (B.2); uniform cover (B.4) for the high type; each against the fixed schedule | none claimed; no trade coexists at each node |
| Prop. A.3 | Fixed experiment: entry falls weakly with strength | analytical | A.2; OA A.5 | none (fixed signal) | direct: indicator difference (A.9) | n/a |
| Prop. A.4 | $r_N$, $\mathfrak r(k)$, $r_U$, $r_C$ and what each bounds | analytical | A.2; OA A.5 | no-trade candidate (explicit) | direct | sufficient bounds hold for every profile ($\Delta_T<k$; derivative bound) |
| Prop. A.5 | Prop. 2 for every bounded-score density | analytical | A.4; OA A.3, A.6 | as Prop. 2 with $\mu_f$ | direct; nonemptiness by a six-step construction | every profile (score bound) |
| Prop. A.6 | Prop. 2(i),(ii) with atomless costs | analytical | A.4; OA A.6 | as Prop. 2 with $e(\mu)=H_C(B(\mu))$ | direct | every profile |
| Prop. A.7 | Complementary signals: unique zero orders, then unique orders by signal, entry rises | analytical | A.5; OA A.7 | orders by $T$; price (A.34); beliefs $\phi_y(\mu_P)$; entry (A.28); bids. Scattered, complete | direct, Steps 1 to 4 | every profile ($\lambda_X\in[m,M]$, $\Delta_P\ge\rho\Delta_T$) |
| Prop. A.8 | Bargaining: sign of the spread effect switches at $\eta=1/2$ | analytical | A.6; OA A.8 | none (payment stage) | direct | n/a; the trading game under bargaining is open |
| Prop. A.9 | Access to prices raises proceeds and net surplus at $F_1$ | analytical | A.6; OA A.9 | coupled full-order equilibria | direct accounting (A.40), (A.41) | inherited from Prop. 2 |
| Lemma OA.1 | Laplace is extreme: tails, Blackwell order, logistic decomposition | analytical | OA A.6 | none | direct: ODE comparison; Euler product | n/a |
| Lemma OA.2 | Quadratic trading cost keeps Prop. 2(i),(ii) | analytical | OA A.6 | as Prop. 2 | direct | every profile |
| OA A.12 | Stake bounds $\Omega_0,\Omega_U$ keep Prop. 2(i),(ii) | analytical, sufficient | OA A.12 | as Prop. 2 | direct | every profile |
| OA A.13 | Many classes: price sufficiency; two groups under a separation $\gamma>0$ | analytical | OA A.13 | as Prop. 2 by group | "repeats Steps 3 to 6" | every profile; classes inside the feasible range: open |

### 1b. Strict hypotheses and margins, computer-assisted steps, open set

| Result | Strict hypotheses and margins at the benchmark | Computer-assisted steps and certificate | Open set |
|---|---|---|---|
| Prop. 1 | FOSD and supports above $p$; strictness by the integral conditions in the statement | none | holds for all continuous $F$ and all class pairs |
| Prop. A.1 | $b>0$ | none | all $b$ |
| Prop. A.2 | $\Delta_T>0$, $\rho>0$ | none | yes |
| Prop. 2(i),(ii) at $(1.2,3)$ | (A1) lower $c_H-B_{r_0}(\pi)=287/240=1.1958$; (A1) upper $B_{r_1}(M)-c_H=0.217155$; (A2) lower $k-\Delta_T(r_0)=1/300$; (A2) upper $(1-1/b)\rho m\Delta_T(r_1)-k=0.0024118$; ownership $(1+\rho)-2\rho=3/4$; $\tau_1-\pi=0.205$; $M-\tau_1=0.026059$; $x^*=0.871222\in(0,1)$ | none in the proof. Printed scalars (entry 0.522757, ownership 0.324192, windows) are closed forms evaluated in floating point; all reproduce by interval | asserted open in $(r_0,r_1,c_H,k)$; nonempty by A.4; prior windows $(0.404610,0.595390)$ for a nonempty (A2) window, $(0.467850,0.538096)$ for (i),(ii), both reproduced with the binding inequality named |
| Prop. 2(iii) at $r_2=3.6$ | $c_H-B_{r_2}(M)=0.0026889$ (not printed); $\tau_2-M=0.00033356$; trading bound $0.011563$; $\Delta_T(r_2)-\Delta_T(r_1)=49/180$; $r_2-r_C=0.0073415$ | none | $r_2\in(r_C,h)$; $c_H\in(5.99731,6.21715)$; $\pi\in(0.467850,0.500424)$; the benchmark sits $0.00734$, $0.00269$ and $0.000424$ from the nearest edge |
| Prop. 3 | pooling margins $k-\rho\Delta_T/2=387/49600,\,19/3200,\,211/52800$; domain $c_H-B_r(1/2)\ge1.3069$; threshold ordering $M_v-\tau\ge0.0280,\,0.0526,\,0.0708$ over the brackets; $b>1/2$ for concavity | yes: outward `mpmath.iv` at 50 digits from exact decimal inputs; exact antiderivatives (A.20); mesh 200; high-type cover uniform over the bracket; $\Psi$ endpoint signs $\ge1.1\times10^{-10}$ and $\le-0.96\times10^{-10}$ (bracket width, not hypothesis margins); $\Gamma_H\ge7.6\times10^{-5},\,2.8\times10^{-3},\,5.5\times10^{-3}$; entry enclosures disjoint; manifest `c2_correspondence.json` (21 Oct), `numerics/certificates.csv` | not stated. Continuity of $\Psi$ and $\Gamma_H$ in the primitives gives some $(1,-v)$ equilibrium near each node; the manuscript does not claim or quantify this |
| Prop. A.3 | FOSD; strictness on a positive-probability crossing set | none; Table 2's control row 0.562178 is labelled numerical diagnostic though it is a closed form | yes |
| Prop. A.4 | at B: $\mathfrak r(k)-r_0=0.020998$; $r_1-r_U=0.162583$; $r_2-r_C=0.0073415$ | none in the proof; printed values are floats with residual checks; `thresholds.csv` bounds are float ulps | n/a |
| Prop. A.5 | logistic at B: same four margins; $x^*_{\log}=5.424598$, entry $0.301509$ reproduced | none | proved open in $(r_0,r_1,r_2,c_H,k)$ |
| Prop. A.6 at $\varepsilon_C=0.1$ | $B_{r_1}(m)-2\varepsilon_C=2.16618$; $(c_H-\varepsilon_C)-B_{r_0}(\pi)=263/240$; $B_{r_1}(M)-(c_H+\varepsilon_C)=0.117155$ | none | yes by continuity; not stated |
| Prop. A.7 at (A.50) | $c_H-B_{r_0}(d)=21/400$; $B_{r_1}(\phi_+(\mu_+))-c_H=0.045265$; $k-(2a-1)\{\cdot\}=2/1375$; $(1-1/b)m(2a-1)\rho\Delta_T(r_1)-k=0.0017971$; floor diagnostic $1.77343$ | none in the proof; the accuracy grid of OA C.3 is numerical | implicit (strict inequalities); not tabulated |
| Prop. A.8 | $\ell<\bar r<h$; $0\le\eta<1$ | none | yes |
| Prop. A.9 | $c_H-B_{r_1}(\pi)=41/24$; gains $0.257809$ and $0.080218$ reproduced | none | inherited |
| Lemma OA.2 | $k+\gamma_q<(1-1/b)\rho\kappa\Delta_T(r_1)$ | none | yes |
| OA A.12 | $\Omega_0=0.043098$, $\Omega_U=0.011434$ reproduced | none | yes |
| OA A.13 | $\gamma>0$; cost windows by group | none | not stated |
| Table 4 cases A, B, D | all six margins reproduced; D fails (A1) upper by $-0.018122$, as printed | none | per-case margins printed (the one margins table in the paper) |

Case C uses class-band integrals that I did not redo.

## 2. Skipped computations (task 2)

The manuscript avoids the phrases "it is easy to see", "similarly" and "by symmetry". The
compressed steps are the ones below. Each carries a verdict.

1. **A.2, part (iii): "exactly as in Steps 4 and 5."** No gap. `LA_worked.tex` expands it.
   One fact the manuscript does not state: uniqueness in part (iii) needs no price inversion,
   because (H5) pins entry at $\rho$ for every profile through the posterior bound alone.
2. **A.2, Proposition A.4: "$B_r(M)$ is strictly decreasing on $r>\ell>p$."** No derivative is
   shown. The derivative is $-M/2-[(1-M)\ell^2-p^2]/(2r^2)$. If the bracket is nonnegative both
   terms are negative. If it is negative, $Mr^2>M\ell^2>p^2-(1-M)\ell^2$ because $\ell>p$. At B
   the bracket is $+0.018941$ and the derivative at $3.6$ is $-0.36626$. No gap.
3. **A.2, (A.11): "the larger root."** The product of the two roots is $-[(1-M)\ell^2-p^2]/M<0$
   at B, so the other root is negative. No gap.
4. **A.4, Proposition A.5: "the price inversion and the residual calculation in OA A.3 apply
   without change."** OA A.3 needs $f\in W^{1,1}$, $f>0$ and $|f'|\le Lf$. The first paragraph
   of the proof shows all three. No gap.
5. **A.4, Proposition A.5: "the null-set arguments in OA A.1 apply."** They need a positive
   density, which the score bound gives. No gap.
6. **A.6, Proposition A.9: "the same argument" for A.6 and A.5.** The accounting identity
   (A.40) holds realization by realization, so it carries over. The positive probability of the
   additional-entry event is supplied in each case. No gap.
7. **OA A.6, Lemma OA.1(i): "apply the same argument to $f(-z)$."** Reflection preserves the
   score bound. No gap.
8. **OA A.13: "the proof repeats Steps 3 to 6."** The one new computation is the group residual:
   $\mathbb E[V_T\mid j,x]-P(x)=e(P(x))[t_j-\bar t_X(x)]$, with $\bar t_X$ in the feasible range
   of posterior means and $t_j$ at distance at least $\gamma$ from it. Hence the sign is the
   group's and the magnitude is at least $\rho\gamma$. One line. No gap.
9. **Section 3.2: "integrating over the conditional order distributions preserves these
   inequalities."** A ratio of two integrals of the same measure is bounded by the pointwise
   ratio bounds. No gap.
10. **A.1, Proposition 1(c): the mixing step.** $\Delta_T(F)=\mathbb E_F[\xi]$ is linear in $F$,
    so mixing a common component scales the difference by $1-\varepsilon$. No gap.
11. **OA B.3: continuity of $\Psi$ "except for individual density kink points."** Kinks have
    Lebesgue measure zero under a bounded integrand. No gap.
12. **Grids and figures in place of bounds.** Figure 2's branches between the certified nodes,
    the symmetric interior family, the mixed candidate at $r_N$, the hyperbolic-secant and
    Student $t_3$ entries of OA C.9, and Figure 3 are numerical diagnostics. The manuscript
    labels each one. Two sentences of Section 4.3 prose rest on the grid, not on Proposition 3:
    "the short magnitude increases toward one as the incumbent strengthens" and "entry rises
    along the accepted continuation". The comparison note must cite them as diagnostics.
13. **Proposition 3: "the entry intervals are strictly ordered upward."** The enclosures
    $[0.5450528898,0.5450528922]$, $[0.5487563062,0.5487563085]$, $[0.5513607988,0.5513608020]$
    are disjoint. Verified from `certificates.csv` and reproduced over the brackets in
    `margins.csv`.

Verdict: no skipped step hides a real gap. The proofs of the numbered results are complete.

## 3. For the comparison note: main results and dynamics (task 3)

Each item carries the manuscript's label and source. Numbers are the benchmark of A.8.

**The reversal.** Entry rises from $\rho=0.25$ at $r_0=1.2$ to $0.522757$ at $r_1=3$ and returns
to $0.25$ at $r_2=3.6$; the trading outcome is unique in each economy (Proposition 2, analytical;
A.2, OA A.4). High-class ownership rises from $0.125$ to $0.324192$. The strong price
Blackwell-dominates the weak one.

**No off-path beliefs.** Every order gives flow a positive density on $\mathbb R$, so every price
in the image is on path and no unilateral deviation reaches a price outside it (OA A.1,
analytical). The uniqueness claims cover arbitrary mixed orders and continuous deviations.

**The fixed-information control falls strictly.** With full orders imposed at both strengths,
entry falls from $0.562178$ to $0.522757$ (Proposition A.3, analytical; the numbers are closed
forms, labelled numerical diagnostic in Table 2). With the price hidden, entry is $\rho$ at both
strengths (analytical).

**The plateau and the ceiling.** Full Laplace orders put the posterior at $M=e/(1+e)$ on the tail
$x\ge1$, which has probability $1/2$ in class $H$ and $e^{-1}/2$ in class $L$. High-cost entry
is impossible above $r_C=3.592659$ (Proposition A.4, analytical). At $r_C$ the tie rule admits
entry on the plateau, so entry equals the left limit $0.506477$ there and drops to $\rho$ just
above (A.14, OA A.5). Entry is discontinuous in strength at the ceiling.

**Coexistence.** No trade is an equilibrium exactly up to $r_N=1.747878$ and is unique below
$\mathfrak r(k)=1.220998$; full orders are unique above $r_U=2.837417$ (Proposition A.4,
analytical formulas). Between $r_N$ and $r_U$ the manuscript proves no uniqueness.

**The partial sale and strictly rising entry.** At $r=1.55,1.60,1.65$ there are equilibria
$(1,-v)$ with $v=0.4603,0.7075,0.9033$ and entry $0.54505<0.54876<0.55136$ (Proposition 3,
computer-assisted, three nodes). Each coexists with no trade. The continuous branch between the
nodes is a numerical diagnostic; the first informative equilibrium is open (Section 4.3).

**Welfare.** At $r_1$ access to prices raises expected proceeds by $0.257809$ and net surplus by
$0.080218$ (Proposition A.9, analytical). The sign reverses when $B(m)<c_H\le B(\pi)$.

**Robustness.** Bounded-score noise (A.5); logistic entry $0.301509$; atomless costs (A.6),
entry $0.522715$; complementary signals (A.7), entry $0.85\to0.879438$; classes and priors
(Table 4; case D fails (A1) at the strong strength, as printed); two groups of many classes
under a separation condition (OA A.13); stakes below $0.011434$ order units (OA A.12);
quadratic trading cost (Lemma OA.2). All analytical.

**Sale terms.** Reserve comparisons at two reserves with analytical uniqueness at the listed
nodes (Table 5); the seller-optimal reserve is open (A.7).

**Dynamics that the continuous order size produces.** The interior sale $-v$ exists because the
low-class investor's marginal profit is strictly decreasing in its order (OA B.2), so a root of
the first-order condition is a global optimum. The certified sale magnitudes rise across the three
nodes, $0.4603<0.7075<0.9033$; the branch between them is a numerical diagnostic. The posterior
plateau carries positive mass at the upper bound, which makes $r_C$ a tie-rule event with a jump
in entry. The fixed-information control gives a strict fall. These are the facts against which the
slot set-up is compared.

## 4. The worked proof (task 4)

`proofs/LA_worked.tex` proves Proposition 2(iii) in the manuscript's general class form under six
named hypotheses, then gives the margins at $r_2=3.6$:

1. the tuple: $\sigma_H^*=\delta_{+1}$, $\sigma_L^*=\delta_{-1}$, the posterior (A.8), the
   price $P^*(x)=t_0+\rho[w_L+\Delta_T\mu^*(x)]$ on all of $\mathbb R$ with its two atoms and
   their probabilities, the belief $\beta^*(P)$ as the inverse on the image, the entry rule
   $e^*\equiv\rho$ with the reason for each cost type, truthful bids;
2. the five conditions;
3. the check of each against the fixed tuple, with the $W^{1,1}$ translation lemma and the
   derivative bound written out;
4. uniqueness by bounds on every profile in five steps; Step 2 shows that entry is $\rho$ in
   every candidate equilibrium before any price inversion;
5. a margins table of eleven rows and the open set in each coordinate.

Verdict: the manuscript's argument is sound and non-circular. It restates in the five-part form
with two additions, the explicit tuple and the margins table, and one observation, that part
(iii) needs no price sufficiency for uniqueness.

## 5. Tie rules

- **Investor.** Best responses are strict in Propositions 2, A.5, A.6, A.7 and at the
  Proposition 3 roots (strict concavity for the low type, strict cover for the high type). The
  only indifference is at $r=r_N$ exactly against the no-trade schedule (A.4). The manuscript
  notes it and uses no investor tie rule elsewhere.
- **Challenger.** An indifferent challenger prepares. At every declared vector
  $g_L(r)=(\ell^2-p^2)/(2r)>0$, so the zero-cost decision is strict and the rule never binds in
  Propositions 2, 3, A.5 to A.7 and A.9 at those vectors. In the general class model a low class
  with an atom at $p$ gives $g_L=0$, and the rule then decides the zero-cost entry; the proofs
  cover that case. It binds at three exact events: $r=r_C$
  (A.4, A.14), the reserve $p_H$ (OA A.14), and the endpoint $p_L=h$ (OA A.14). Proposition
  2(iii) at $r_2=3.6$ does not depend on it: the margin is $0.0026889$.

## 6. Provenance of the printed numbers

- The pinned manuscript (22 October) prints numbers from the run of 21 October on the branch
  `revision/alex-2026-10-21` (manifests `c1_baseline`, `c2_correspondence`, `c3_signals`,
  `c4_moderate`, `c5_noise`, `c6_reserve`, `c6c_reserve_events`, `c7_bargaining`,
  `c8_registry`, `c9_revision`, `c10_classes`; timestamps 17:49 to 19:48 UTC; `c_L = 0`; every
  `passed = true`). The certificate enclosures on that branch
  ($\Psi$ signs, $\Gamma_H$, entry, pooling margin) are identical to the September file.
  Only the floor-diagnostic column differs, by exactly 1, because the low cost enters the
  certificate there alone.
- `main` and this working tree hold the numerical layer of 5 to 6 September with
  `c_L = 1` (benchmark), `0.3` (moderate values), `1` (signals). Entry, ownership, prices and
  certificates are the same under both low costs at every benchmark strength and at the two
  reserves of Table 5, as Section 4.1 of the manuscript argues. I checked that the floor margin
  $B_r(m)-c_L$ is positive at both values at each of those nodes. The net surplus, the
  expected paid cost and $\zeta_L$ differ by $\rho c_L=0.25$ at the benchmark:
  `tables/equilibrium_controls.csv` on `main` prints 2.382301 at $r_1$; the manuscript prints
  2.632301. The reserve sweep of OA C.6 differs between the two branches, because a high
  reserve lowers $B_r(m)$ below 1; the pinned reserve tables come from the October run.
- OA E.1 describes the distributed numerical layer. The branch that reproduces the manuscript is
  unmerged and unpushed. This is a repository-state gap, not a proof gap.

## 7. Formula check against TEAM_RULES §3

The formulas of §3 ($t_0,t_H,t_L,g_H,g_L,\Delta_T,B_r,\tau,e_r,P_r$) agree with the
manuscript's (4), (9) and (12). No difference.

## 8. Sources

- `git -C overleaf/paper show 01bd5d6:main.tex` and `:online_appendix.tex` (copies in
  `scripts/LA/pinned/`); the table files at the same commit.
- `numerics/certificates.py`, `numerics/certificates.csv`, `numerics/thresholds.csv`,
  `numerics/manifests/*.json` on `main` and on `revision/alex-2026-10-21`.
- `scripts/LA/margins.py`, `margins.csv`, `margins_run.log` (this workstream).
- Earlier study: `audit/microstructure_search_2026_10_22/memos/SYNTHESIS.md` §0, §3 (the
  Laplace reference row).
