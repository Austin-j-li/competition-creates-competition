---
title: "Proposition 2 without the floor: the verdict"
subtitle: "Synthesis, regime II team"
date: "2026-10-04"
---

Read this note first. It states only what survived the two referee reports (`check_theory/review.md`, `check_numerics/review.md`) on the three track notes (`theory/`, `numerics/`, `adversary/`). Every claim carries the paper's status word: analytical, computer-assisted, numerical diagnostic, open. By Online Appendix C.2, a floating-point quadrature check is a numerical diagnostic, even where a track note calls it computer-assisted; no number in this project is an interval enclosure. Notation is that of `theory/note.md`. Benchmark: $h=10$, $\ell=1$, $p=\tfrac12$, $b=2$, $c_H=6$, $r_0=1.2$, $r_1=3$, $k=0.02$, $\rho=0.25$. At $r_1=3$: $B(m)=2.3662$, $B(\tfrac12)=4.2917$, $B(M)=6.2172$, $\Delta_T=\tfrac23$, $\tau_H=0.705$, and the right side of (A3) is $0.02241$.

## 1. Verdict

Proposition 2 survives in part, not in full. Replace (A1) by

$$
B_{r_1}(m)<c_L<B_{r_1}(\tfrac12),
\tag{A1$'$}
$$

with both ends strict: the point $c_L=B_{r_1}(m)$ is regime I under the paper's tie rule, so Proposition 2 itself covers it, and at $c_L=B_{r_1}(\tfrac12)$ the replacement conditions below are empty. Then part (i) survives unchanged (analytical), and at $r_1$, under the right side of the paper's (A3), every equilibrium has correctly signed informed trading and an informative price that strictly Blackwell dominates the $r_0$ price (analytical); but every equilibrium also pools a positive-probability set of bad flows at the no-entry price, so the price does not reveal $\mu_X$ everywhere and on-path entry is not unique. The unique trading outcome $(1,-1)$ and the reversal $\mathsf E>\rho$, $\mathsf O_H>\rho/2$ in every equilibrium do **not** survive under the paper's (A3): at the benchmark $k=0.02$ they fail for $c_L>2.9844$ (numerical diagnostic) and for $c_L>3.4211$ (analytical). They survive under two replacements: (A3') $\Delta_T(r_0)<k\le K(c_L)$, a trading-cost bound that is always less than half of (A3)'s right side, and (A4'), a joint bound on $(c_L,\rho)$ that at $\rho=0.25$ reads $c_L\le3.4607$ (entry) and $c_L\le3.7408$ (ownership) and that is empty for every $c_L$ once $\rho\ge0.5154$. Part (iii) becomes stronger: at every $r_2>r_1$ with $B_{r_2}(M)<c_H$, entry is strictly below $\rho$ and ownership strictly below $\rho/2$ in every equilibrium (analytical).

The weakest replacement for (A1), with (A2) kept and the trading cost forcing full orders ((A3) in regime I, (A3') in regime II), is: the reversal holds in every equilibrium if and only if $c_L\le B_{r_1}(m)$ or [(A1') and (A4')]. Given (A1'), (A2), (A3'), condition (A4') is necessary and sufficient. For $c_L\ge B_{r_1}(\tfrac12)$ it always fails (the dead profile is an equilibrium). With the paper's (A3) at $k=0.02$, $\rho=0.25$, no theorem replaces (A1): the best statement is "fails for $c_L>2.9844$; no failure found for $c_L\le2.9844$" (Section 4).

## 2. Proposition 2'

**Proposition 2' (analytical; benchmark threshold values numerical diagnostic).** *Fix $0<p<\ell<r_0<r_1<h$, $0<\rho<1$, $b>1$, $k>0$. Assume (A1'), (A2), and*

$$
\Delta_T(r_0)<k\le K(c_L):=\Big(1-\frac1b\Big)\rho\,\Delta_T(r_1)\min\{\tau_L S(\bar x+1),\ m\,S(\bar x)\},
\tag{A3$'$}
$$

$$
\mathsf E_0-V_E\ge\rho,\qquad e_{H,0}-V_H\ge\rho ,
\tag{A4$'$}
$$

*where $\tau_L=B_{r_1}^{-1}(c_L)$, $\bar x$ solves $\bar\mu(\bar x)=\tau_L$ (the largest consistent half-line pool), $\mathsf E_0,e_{H,0}$ are entry and high-state entry under full orders with the minimal pool $(-\infty,z_0)$, and $V_E,V_H$ are the fractional-knapsack values of Proposition R.7. (i) At $r_0$ the unique trading outcome is $q_H=q_L=0$, the price carries no information, entry is $\rho$ and $\mathsf O_H=\rho/2$. (ii) At $r_1$ the unique trading outcome is $(1,-1)$; in every equilibrium the price is informative and strictly Blackwell dominates the $r_0$ price, $\mathsf E>\rho$, and $\mathsf O_H>\rho/2$; every equilibrium has a no-entry pool of positive probability, and on-path entry takes every value in $(\mathsf E_0-V_E,\mathsf E_0]$. (iii) At every $r_2\in(r_1,h)$ with $B_{r_2}(M)<c_H$, an equilibrium exists and every equilibrium has $\mathsf E<\rho$ and $\mathsf O_H<\rho/2$. The conditions hold on a nonempty set (benchmark with $r_0=1.1$, $k=0.008$, $c_L\in(2.3662,2.5866]$), open when the right side of (A3') and (A4') are strict. Given (A1'), (A2), (A3'), condition (A4') is also necessary for the entry and ownership claims.*

Proofs: R.1 (i), R.2 and R.3 (signs, informativeness, pool), R.4 and R.5 (likelihood-ratio pool cap), R.6 (forcing), R.7 (bathtub), R.12 (collapse) in `theory/note.md`; Lemma C.1 (existence at $r_2$ and $K<\tfrac12(1-\tfrac1b)\rho m\Delta_T(r_1)$) in `check_theory/review.md`. The theory referee checked each proof line by line and found no gap. Three facts about the conditions, all analytical:

- (A3') is empty at the paper's triple $(r_0,k,\rho)=(1.2,0.02,0.25)$: $\sup K=0.0112<\Delta_T(1.2)=0.0167$. Proposition 2' needs $r_0\le1.157$ and $k\le0.0107$ at the benchmark $r_1$ and $\rho$ (Section 4 gives other $r_1$).
- (A4') contains a condition on $\rho$ alone (Theorem AD.1, `adversary/note.md`): every full-order equilibrium has $\mathsf E<\rho(1-\pi_0)+(1-\rho)a$ with $\pi_0=\Pr(X\le-1)=0.342$ and $a=S_X(x^*)=0.364$, so the entry half of (A4') is empty once $\rho\ge\rho_E^*=a/(a+\pi_0)=0.5154$, and the ownership half once $\rho>\rho_O^*=0.7428$ ($r_1=3$).
- The strict bound $\mathsf E>\mathsf E_0-V_E$ uses the paper's tie rule (an indifferent challenger prepares). Under the opposite tie rule (A4') must be strict.

**What changes in the proof.** The paper's Step (A.6) bounds the residual by $\rho m\Delta_T$ at every flow because the cheap type enters everywhere. In regime II the cheap type enters only off the pool, so the residual is $\rho\tau_L\Delta_T$ (low type) and $\rho m\Delta_T$ (high type) on the entry set $A$ and zero on the pool $N$. The new step bounds the mass that any deviation puts into the pool: a Neyman-Pearson argument for the Laplace likelihood ratio (Lemma R.4) and the pool-belief constraint $\bar\mu_N<\tau_L$ give $\Pr(N\mid H)<F(\bar x-1)$, $\Pr(s+Z\in N)<F(\bar x)$, $\Pr(Z-s\in N)<F(\bar x+s)$ for every order law and every Borel pool (Lemma R.5). This yields $K(c_L)$. Uniqueness of on-path entry is lost and replaced by a classification: the equilibrium set is exactly full orders times every Borel pool $N\supseteq(-\infty,z_0)$ with belief below $\tau_L$ (R.6), and the infimum of entry over it is a fractional knapsack whose worst pool is the forced half-line plus a mid band, an island just above $x^*$, and a share of the top plateau (R.7). Blackwell dominance follows from Proposition CD.4 (every equilibrium is informative iff $\rho\Delta_T(r_1)>2k$, which (A3') implies). Part (iii) no longer uses the floor: every belief is at most $M$, so the expensive type never enters, and every equilibrium has a pool (R.3(b) or CD.10), so $\mathsf E=\rho\Pr(A)<\rho$.

## 3. Counterexamples

Each row is an equilibrium (or family) that breaks a claim of Proposition 2 under (A1'), (A2) and the paper's (A3) or (A3'), with its status and the assumption that excludes it. Benchmark unless stated.

| # | equilibrium | numbers | breaks | status | excluded by |
|---|---|---|---|---|---|
| 1 | Starved family: orders $(1,-v)$, $v<v_H=0.7424$, half-line pool. The pool removes the short seller's residual; a short below $v_H$ keeps every belief below $\tau_H$, so the expensive type never enters | $c_L=3.0$, $k=0.02$: $(1,-0.7344)$, pool $(-\infty,0.4606)$, $\mathsf E=0.1117$, $\mathsf O_H=0.0773$. Exists for $c_L>2.9844$ at $k=0.02$. Inside the (A3) window with $k$ free: $c_L=2.9$, $k=0.0224$, $(1,-0.73)$, pool $(-\infty,0.1913)$, $\mathsf E=0.1227$; infimum over the window $2.8319$ | unique trading, $\mathsf E>\rho$, $\mathsf O_H>\rho/2$ | numerical diagnostic (three independent quadrature codes; high type checked on grids); **analytical** for members with pool cutoff $x'\ge1$ (Prop. C.2): at $k=0.02$ for every $c_L>3.4211$ ($v=0.5026$, $\mathsf E=0.0920$, $\mathsf O_H=0.0625$) | (A3'): $k\le K$ forces full orders |
| 2 | Island (bathtub) pools under full orders: forced half-line plus mid band, island above $x^*$, plateau share | $c_L=3.5$, $k=0.02$: $\mathsf E=0.2408<\rho$, accepted; $\inf\mathsf E=0.24999$ at $c_L=3.4607$. Branch ends below $c_L=4.0$ at $k=0.02$ (worst pool fails the low type there) | $\mathsf E>\rho$ for $c_L>3.4607$, $\mathsf O_H>\rho/2$ for $c_L>3.7408$ | numerical diagnostic at $k=0.02$; analytical under (A3') (R.6 + R.7) | (A4') |
| 3 | Half-line family: full orders, pool $(-\infty,x')$, $x'\ge x^*$ | at $k=0.02$: $\mathsf E<\rho$ for $c_L>3.6498$, $\mathsf O_H<\rho/2$ for $c_L>3.8945$; investor test ends at $x'=2.614$ | same | analytical (R.9) | (A4') |
| 4 | Cheap-type share: every full-order equilibrium pools at least the plateau $x\le-1$, losing $\rho\pi_0$ of cheap entry against at most $(1-\rho)a$ of expensive entry | paper's $k=0.02$, $r_0=1.2$, $\rho=0.6$, $c_L=2.4$: (A1'), (A2), (A3), (A3') all hold ($K(2.4)=0.0234$); every equilibrium has full orders; minimal pool $\mathsf E=0.5382<0.6$, $e_H=0.701$, $e_L=0.375$, $\mathsf O_H=0.350>0.3$; all other pools lower. $\rho=0.75$: ownership fails too | $\mathsf E>\rho$ at every regime II $c_L$ once $\rho\ge0.5154$; $\mathsf O_H>\rho/2$ once $\rho>0.7428$ | analytical (AD.1 + R.6); values numerical diagnostic | (A4') ($\rho$ part) |
| 5 | Full-order half-line pools at $\rho=\tfrac12$ | $c_L=2.5$, $k=0.02$, cutoffs $-0.6,-0.5,-0.4$: $\mathsf E=0.478,0.470,0.462<0.5$ | kills the candidate $c_L+c_H\le2B_{r_1}(\tfrac12)$ as a general sufficient condition | numerical diagnostic | (A4') |

Mechanism, in one sentence: in regime II bad prices deter the cheap type, good prices recruit the expensive type, and entry rises only when $(1-\rho)\Pr(\text{good news})$ beats $\rho\Pr(\text{pool})$; the pool can also starve the short seller's incentive, and then information recruits nobody.

What was **not** found: at $r_1=3$, $k=0.02$, $\rho=0.25$, no equilibrium with $\mathsf E\le\rho$ exists for $c_L\in(2.3662,2.9844]$ in any class tried by any track: all consistent pure order lattices with every measurable pool (numerics LP), 745 lattice and 960 random mixed schedules (adversary, numerics referee), 1500 random schedules at each of 11 values of $c_L$ (numerics), pools ending below zero, partial buys $q_H\in\{0.8,0.6\}$ (numerics referee: 75 low-type fixed points all fail the high type). Full orders are forced over pure half-line schedules only for $c_L\le2.59$ ($k_{\rm pure}$ crosses $0.02$ between $2.585$ and $2.60$; break point $2B(\tfrac12)-c_H=2.5833$, Lemma R.11, analytical). Status of the window: open as a theorem, numerical diagnostic in support.

## 4. Map: where the reversal holds in every equilibrium, $\rho=0.25$

Two questions, two columns. "At $k=0.02$" asks about the paper's trading cost; its $c^*$ is the numerics region map (`numerics/thresholds.csv`; reversal holds in every *found* equilibrium for $c_L<c^*$, breaks at $c^*$ with a verified member; numerical diagnostic). "Under (A3')" asks about Proposition 2'; its thresholds are the exact (A4') knapsack values (`synthesis/map.csv`, theory closed forms; agree with the numerics columns and both referees to $10^{-4}$; numerical diagnostic). The last two columns show that (A3') cannot be met with the paper's $r_0=1.2$ at any $r_1$ in the map.

| $r_1$ | regime II $(B(m),B(\tfrac12))$ | paper's (A3) at $k=0.02$, $r_0=1.2$ | $c^*$ at $k=0.02$ (family) | (A4') entry | (A4') ownership | $\sup K$ | largest $r_0$ for (A3') |
|---|---|---|---|---|---|---|---|
| $\le1.7$ | | no | empty: no-trade equilibrium | | | | |
| 1.8 | $(2.581,4.619)$ | no | empty at $B(m)$: low-trade family; holds again on $3.542$ to $4.619$ | | | | |
| 1.9 | $(2.561,4.591)$ | no | no break found (isolated point) | | | | |
| 2.0 | $(2.541,4.563)$ | no ($0.0084$) | 3.9307 (island, exact LP; upper bound) | 3.7719 | 4.0504 | 0.0042 | 1.096 |
| 2.3 | $(2.485,4.479)$ | no ($0.0124$) | 2.9758 (starved) | 3.6790 | 3.9576 | 0.0062 | 1.117 |
| 2.5 | $(2.449,4.425)$ | no ($0.0151$) | 2.9456 (starved) | 3.6172 | 3.8960 | 0.0076 | 1.131 |
| 2.7 | $(2.415,4.371)$ | no ($0.0180$) | 2.9743 (starved) | 3.5551 | 3.8342 | 0.0090 | 1.143 |
| 2.9 | $(2.382,4.318)$ | yes ($0.0209$) | 2.9875 (starved) | 3.4924 | 3.7721 | 0.0105 | 1.155 |
| 3.0 | $(2.366,4.292)$ | yes ($0.0224$) | 2.9844 (starved) | 3.4607 | 3.7408 | 0.0112 | 1.161 |
| 3.1 | $(2.350,4.265)$ | yes ($0.0239$) | 2.9743 (starved) | 3.4287 | 3.7093 | 0.0120 | 1.167 |
| 3.3 | $(2.319,4.213)$ | yes ($0.0270$) | 2.9324 (starved) | 3.3639 | 3.6456 | 0.0135 | 1.178 |
| 3.5 | $(2.287,4.161)$ | yes ($0.0300$) | 2.8607 (starved) | 3.2976 | 3.5808 | 0.0150 | 1.189 |
| 3.6 | $(2.272,4.135)$ | yes | empty: ceiling $B(M)=5.997<c_H$ | | | | |

Reading the map. At the paper's $k=0.02$ the reversal holds in every found equilibrium on roughly the lower third of regime II, $c_L\in(B(m),2.86$ to $2.99)$, for $r_1$ from $2.3$ to $3.5$, and the starved family sets the edge; this is a numerical diagnostic, and the paper's (A3) itself holds only for $r_1\ge2.9$. Under (A3') the exact region is (A4'): about $57\%$ of regime II at $r_1=3$ ($c_L\le3.4607$), but with a trading cost below $0.0112$ and a weak incumbent below $r_0=1.161$. The (A4') region in $(c_L,\rho)$ at $r_1=3$ is a curved triangle with top $\rho_E^*=0.5154$ at the floor and corner near $(4.1498,0)$, not at $(B(\tfrac12),0)$ (`check_numerics/rho_curve.csv`; the adversary's row $c_L=4.20$ was corrected). At $\rho=0.5$ the entry half of (A4') allows only $c_L\le2.3726$. At $\rho=0.1$ the numerics found no break at $k=0.02$ for $r_1\in[2.7,3.0]$, with unconverged starts above $c_L=2.6$ (open).

## 5. What this means for the paper

**Is the change worth making?** Not as a replacement of (A1) inside Proposition 2. The cost is high: the proposition would lose unique on-path entry (a continuum of pools), would need a trading-cost bound (A3') that is empty at the paper's own benchmark triple, and would need a new joint restriction (A4') on $(c_L,\rho)$ that excludes every $\rho\ge0.5154$; Table 2 of the paper could no longer report unique outcomes, and the open-set claim would carry two extra strict inequalities. The gain is real but belongs in a remark and an online-appendix proposition: (A1) is sufficient, not necessary; the floor does two jobs, and only the second (keeping cheap entry insensitive to the price) is what the reversal needs; and regime II adds an economically new force, information that deters entry after bad news, which turns "competition creates competition" into "competition sorts competition" when cheap challengers are common ($\mathsf O_H$ rises over a wider range, $\rho<0.743$, than $\mathsf E$ does, $\rho<0.515$). One sentence of the current (A1) discussion needs a fix in any case: "nobody prepares, proceeds do not depend on challenger quality, and the investor has nothing to trade on" is true in regimes III and IV only; in regime II the investor trades in every equilibrium.

**Recommendation.** Keep (A1) and Proposition 2 as they are. Add Proposition 2' to the online appendix with the status labels of Section 2, and replace the (A1) discussion paragraph of Section 4.1 by the draft below. Do not cite the window $c_L\le2.9844$ at $k=0.02$ as a theorem.

**Draft (not for the manuscript until the author approves). Replacement (A1) line for the online-appendix Proposition 2':**

> *(A1') $B_{r_1}(m)<c_L<B_{r_1}(1/2)$; (A3') $\Delta_T(r_0)<k\le K(c_L)$ with $K$ as in Proposition 2'; (A4') $\mathsf E_0-V_E\ge\rho$ and $e_{H,0}-V_H\ge\rho$. At the benchmark primitives with $\rho=0.25$, (A4') is $c_L\le3.4607$, and (A3') requires $r_0\le1.157$ and $k\le0.0107$; it is satisfied, for example, at $r_0=1.1$, $k=0.008$, $c_L\in(2.3662,2.5866]$.*

**Draft discussion paragraph for Section 4.1 (replaces "Condition (A1) ensures ... not a numerical regularizer."):**

> Condition (A1) is a participation floor: low-cost preparation is worthwhile even at the lowest feasible belief. It does two jobs. First, some preparation makes the target's proceeds sensitive to challenger quality before favorable information recruits additional preparation, which supplies a base return to revealing that quality through trading. Second, it makes low-cost preparation insensitive to the price, so that information can only add entry. The first job survives without the floor. If $c_L$ lies between $B_{r_1}(m)$ and $B_{r_1}(1/2)$, the low-cost challenger still prepares at the prior, no uninformative-price equilibrium exists at $r_1$, and every equilibrium has correctly signed informed trading and an informative price. The second job does not survive. Unfavorable prices then deter the low-cost challenger, every equilibrium pools a positive-probability set of unfavorable flows at the no-entry price, on-path entry is no longer unique, and total entry exceeds $\rho$ only if the high-cost entry recruited by favorable prices outweighs the low-cost entry lost in the pool. That balance needs a smaller trading-cost bound than (A3), because the pool also weakens the short seller's incentive, and it fails at every such $c_L$ once the share of low-cost challengers exceeds about one half. Online Appendix [section] states the exact conditions. The floor is therefore part of the mechanism in two senses: it supplies the base return to informed trading, and it keeps information from deterring the entry it is meant to create.

## 6. Open items

1. The window $c_L\in(2.3662,2.9844]$ at $k=0.02$, $\rho=0.25$, $r_1=3$: is the reversal true in every equilibrium? No counterexample in any class tried; forcing over pure half-line schedules is verified only to $c_L\approx2.59$. A route: extend Lemma R.11 to mixtures and bound the island budget against the top plateau. Status: open.
2. A forcing bound sharper than $K$. Random consistent pools are $(1,-1)$ equilibria up to $k=0.04$ near the floor and fail at $0.06$, so the true forcing level is five to seven times $K$. But the admissible set of $k$ at fixed $c_L$ is not an interval (at $c_L=2.6$ the reversal holds at $k=0.02$ and fails at $k=0.03$), so a sharp replacement for (A3) must be a set, not an upper bound. Status: open.
3. Interval enclosure of the high type's best response in the starved family for pool cutoffs $x'<1$, which carry the failure on $c_L\in(2.9844,3.4211]$ at $k=0.02$. Status: numerical diagnostic.
4. Non-uniqueness of on-path entry under the paper's (A3) alone is proved when $k<(1-\tfrac1b)J_G(z_0)$, which covers every $\rho\le\tfrac12$ (benchmark: $\rho<0.699$); open for larger $\rho$ with $\tau_L$ near $\tfrac12$.
5. Monotonicity of $\inf\mathsf E$ in $c_L$, which turns (A4') into a single threshold in $c_L$, is seen on grids only. Status: numerical diagnostic.
6. Selection over the pool continuum: no refinement in the paper picks a point of $(\mathsf E_0-V_E,\mathsf E_0]$. Status: open.
7. Not computed: $\rho_E^*$ and (A4') for the moderate-value specification of Section 5.2 and for other $c_H$; part (iii) numerics at $\rho=0.25$ only; the $\rho=0.1$ map has unconverged starts above $c_L=2.6$; one region point with no equilibrium found ($r_1=1.6$, $\rho=0.5$, $c_L=2.8969$).

## 7. Claims from the track notes that did not survive refereeing (do not cite)

- Numerics `kscan`: "(A3) is sufficient and not sharp for $c_L$ up to $2.9$", $k_S(2.9)=0.0718$, $k_U\approx0.05$. Refuted: a starved equilibrium with $\mathsf E=0.1227$ exists at $(c_L,k)=(2.9,0.0224)$ inside (A3), and at $(2.6,0.03)$, $(2.9,0.03)$, $(2.9,0.035)$ with negative pool cutoffs. The bisection ran on a predicate that is not monotone in $k$.
- Theory: "$c_L+c_H\le2B_{r_1}(\tfrac12)$ is a sufficient condition for the reversal under (A3)". Refuted at $\rho=0.5$ (row 5 above) and for every $\rho\ge0.5154$ (row 4). It is an open candidate at $\rho=0.25$ only, and only for pure orders (Lemma R.11).
- Theory digest: "an informative equilibrium exists iff $\rho\Delta_T>2k$". Refuted ($\rho=0.1$, $c_L=3$, $k=0.04$ has a full-order equilibrium next to no-trade). Correct form: every equilibrium is informative iff $\rho\Delta_T>2k$ (R.3(a), CD.4).
- Adversary Table 1, row $c_L=4.20$ (thresholds $0.0007$, $0.0010$) and "corner of the reversal region at $(B_{r_1}(\tfrac12),0)$". Refuted: $\inf\mathsf E=0.0635\rho$ at $c_L=4.2$ for every $\rho$; the corner is near $(4.1498,0)$.
- Numerics: "the pool LP is a relaxation, so its minimum is a lower bound". Refuted at $c_L=2.4$ ($0.42495$ above the exact infimum $0.42453$); no conclusion changes.
- Numerics: "lowest values just below $c^*$: $\mathsf E=0.3764$, $\mathsf O_H=0.2741$". Those are the half-line member; island pools reach $0.3444$ and $0.2441$ at $c_L=2.975$ and are accepted at $k=0.02$.
- Status words: "computer-assisted" in the numerics and adversary notes and in the theory digest's threshold table means floating-point quadrature; by Online Appendix C.2 these rows are numerical diagnostics. Two upgrades go the other way: the $\rho=0.6$, $c_L=2.4$ example is analytical (AD.1 + R.6 + $K(2.4)=0.0234\ge0.02$), and starved members with $x'\ge1$ are analytical (Prop. C.2).

## 8. Files

See `README.md` in this folder for the file list and the reading order. The map table of Section 4 comes from `synthesis/map.py` (reuses `theory/formulas.py`; writes `synthesis/map.csv`; a few seconds) and from `numerics/thresholds.csv`.
