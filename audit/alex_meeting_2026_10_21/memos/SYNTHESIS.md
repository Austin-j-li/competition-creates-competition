# Synthesis: the supervisor's four points, red-team verdicts, and the revision plan

Memo to the author, 21 October 2026. This memo reviews the fourteen workstream memos and the
numerical verifier memo (`V_discrete_check.md`) in this folder. It re-derives the high-stakes claims,
resolves the disagreements between memos, and states what to change in the paper.

Check scripts (print-only) are in `audit/alex_meeting_2026_10_21/scripts/SYNTHESIS/`:
`check_split_and_props.py`, `check_laplace_class.py`, `check_discrete.py`,
`check_stake_welfare.py`, `check_normalization.py`. Run each from the repository root with
`.venv/bin/python <path>`. Every number quoted below comes from one of these scripts or from the
named memo. Paper references are to `overleaf/paper/main.tex` unless stated.

Status labels follow the paper: **analytical**, **numerical diagnostic**, **conjecture**, **open**.

---

## Part A. Red-team verdicts

### A.1 Verdict table

Verdicts: CONFIRMED, CONFIRMED WITH CORRECTION (the correction is in the note), REFUTED.

| # | Claim | Memo | Verdict | Note (status of my check) |
|---|---|---|---|---|
| 1 | Split identity $t(\theta)+g(\theta)=\theta$ for $\theta\ge p$; $\Delta_T+(g_H-g_L)=h-\ell$ at every $r$ in the binary model | Q1_N_main Claims 1, 3; Q4 Claim 4 | CONFIRMED | Analytical and numerical. The identity is pointwise in $\theta$. It uses only the second-price rule, the reserve, and a continuous $F$ (no ties). It holds for every $r>0$, also for $r<\ell$ (then $\Delta_T=0$) and $r>h$. Checked at $r=0.3,0.8,1.2,3,3.6,9,25$: the sum is $9.000000000000$. |
| 2 | With distribution types, $\Delta_T+(g_H-g_L)=\mathbb E_H\max\{\theta,p\}-\mathbb E_L\max\{\theta,p\}$ under equal admissibility | Q1_N_main Claim 3 (N7) | CONFIRMED WITH CORRECTION | The general form is $\int_p^\infty D+pF(p)D(p^-)$; checked in four cases, including $p=1.1$ where the reserve term is $1.008$. The $F$-free form holds when $D(p^-)=0$ **or** when $F(p)=0$ (the incumbent always clears the reserve; then $t+g=\max\{\theta,p\}$ pointwise). The memo states only the first condition. Small refinement, not an error. |
| 3 | Reserve boundary term $pF(p)[G_L(p^-)-G_H(p^-)]$; Prop. 1 generalizes iff "FOSD above the reserve and equal mass below" | Q1_N_main Claims 2, 4; Q1_N_numerics Sec. 2 | CONFIRMED | Analytical. The kernel argument is right. The "iff" is over every continuous $F$ and every FOSD shift. For the uniform family alone the exact condition is weaker: $\int_p^r uD\ge p^2D(p^-)$. Say both. Section 6.3 at $p=1.1$: $\Delta_T(1.2)=1.012500>\Delta_T(3)=1.005000$, falling on $(p,\sqrt3p)=(1.1,1.905)$. Confirmed. |
| 4 | General prior: $m(\pi),M(\pi)$, $1-M(\pi)=m(1-\pi)$, $\lambda(\pi)=m(\min\{\pi,1-\pi\})$, $x^*=(b/2)[\operatorname{logit}\tau-\operatorname{logit}\pi]$, Prop. 2$'$ | Q1_N_main Claims 6, 8, 10, 11 | CONFIRMED | Analytical. At $b=2$: $(m,M)=(0.136190,0.538102)$ at $\pi=0.3$ and $(0.461898,0.863810)$ at $\pi=0.7$. $\mu_X(x^*)=\tau$ checked. A prior away from $1/2$ narrows the (A3) window by the factor $\lambda(\pi)/m$. |
| 5 | Ownership caveat $\mathsf O_H=\pi e_HW_H$: entry can rise while type-H ownership falls | Q1_N_main Claims 10(ii), 12(a) | CONFIRMED | Numerical diagnostic reproduced: case 2c gives $\mathsf O_H$ $0.422906\to0.416476$ while entry rises; $W_H$ falls $0.890329\to0.850658$ and $\rho/e_H=0.970193$. |
| 6 | Prop. 2 holds for every noise law with $\lvert(\log f)'\rvert\le L<1$, with the largest attained posterior in (A2) | Q2_laplace_technical R16 | CONFIRMED | Analytical (proof steps re-read; each uses only $K_f<\infty$, $m_f$, the floor, $\lvert f'\rvert\le Lf$, $f>0$). For symmetric unimodal members the full-order supremum equals the uniform bound (R1 v). Student $t$ ($\nu=3$, $L=1/2$): $\sup\mu=0.729061>\tau=0.705$; entry $0.374834$. |
| 7 | Laplace is extremal: lightest tails (R8), most informative at every pure profile (R9), largest plateau mass (R11) | Q2_laplace_technical | CONFIRMED | Analytical. R8 re-derived (median-zero argument). R9(i) re-derived (ODE comparison with Grönwall; half-line tests are Neyman–Pearson for Laplace). R9(ii) needs log-concavity for mixed profiles; R9(i) covers pure profiles only. Both scopes are stated in the memo. |
| 8 | $\mathrm{Logistic}(b)=\mathrm{Laplace}(b)+W$, $W$ independent, via Euler's product for $\pi x/\sinh(\pi x)$ | Q2_laplace_technical R10 | CONFIRMED | Analytical and numerical. The paper's (A.21) is the standard logistic with scale $b$, so its characteristic function is $\pi bt/\sinh(\pi bt)$. The convolution of Laplace(2) with $W\sim\tfrac3{8b}\operatorname{sech}^4(z/2b)$ reproduces $f_{\log}$ to 12 digits at $z=0,0.7,2,5$. |
| 9 | The paper's sentence "neither experiment Blackwell dominates the other in general" (lines 1877–1880; OA lines 2631–2632) is wrong at a common scale | Q2_laplace_technical R10 | CONFIRMED | Analytical. At common $b$ the logistic flow is a garbling of the Laplace flow at every order profile, pure or mixed, because $W$ is independent of the order. Both Section 5.1 equilibria are $(1,-1)$ under Prop. A.5, so the ordering holds across those equilibria, and the price experiments inherit it through price sufficiency. Numerical: $G(\tau)=\mathbb E(\mu-\tau)_+$ is larger under Laplace at every $\tau$ at common scale; at matched variance the curves cross ($-0.00085$ at $\tau=0.72$). Entry $0.522757$ vs $0.301509$ stands: entry is not a convex functional of the posterior. |
| 10 | Buy-only menu, equal noise: one cutoff $k=\rho\Delta_T/3$; no coexistence; presence $\lambda$ does not move it | Q2_discrete_buy_only Claims 5, 12; Q2_discrete_sell_only Claim 5; V_discrete_check 3.3 | CONFIRMED | Analytical (exact rationals). H's buy payoff is $\bar e\Delta_T/3-k$ against every schedule, for every $\beta_H$ and every $\lambda$. $r_T=\mathfrak r(3k/\rho)=1.973212111$. Scope: $\bar e=\rho$ fixed (no expensive entry at the prior), equal noise. |
| 11 | Benchmark path $0.25\to1/3\to1/3$ at $(1.2,3,3.6)$; return only for $r>7.968627$, and then to $5/24<\rho$ | Q2_discrete_buy_only Sec. 5; Q2_discrete_literature C6; V_discrete_check | CONFIRMED | Analytical. At $c_L=1$ the floor fails at the $L$-revealing flow ($g_L(3)=0.125$), so entry there is zero. $r_C^D=h-c_H+\sqrt{(h-c_H)^2-p^2}=7.968626967$. |
| 12 | The floor $c_L\le g_L$ is what keeps low-cost entry at an $L$-revealing flow | Q2_discrete_buy_only, Q2_discrete_sell_only, Q2_discrete_literature C5 | CONFIRMED WITH CORRECTION | The floor is **sufficient** for price sufficiency, not necessary: at the benchmark the three prices still identify the posteriors $0,1/2,1$ although entry at posterior $0$ is zero (verifier 3.2). The literature memo's "only with a floor" is too strong. The buy-only memo's Claim 6 has the correct statement. |
| 13 | Presence probability: $\mathsf E=\rho+(1-\rho)\lambda/6$, $\mathsf O_H=\rho/2+(1-\rho)\lambda/6$ under $c_L\le B_{r}(m_\lambda)$, $m_\lambda=(1-\lambda)/(2-\lambda)$ | Q2_discrete_buy_only Claim 12; Q2_discrete_sell_only Claim 10 | CONFIRMED | Analytical. With $c_L=1$ at $r=3$ the floor holds iff $\lambda\le158/179=0.882682$. At $\lambda=0.9$ the formula fails ($0.316667$, not $0.3625$) because the floor fails. |
| 14 | Buy-only is the unique partial-trade equilibrium of the two-sided game for $\lambda\in(0.58,0.857]$ | Q2_discrete_literature C7 | CONFIRMED WITH CORRECTION | True for **pure** profiles on the partial-trade cost interval $[k_T(\lambda),\rho\Delta_T/3)$ with $k_T(\lambda)=(\rho\Delta_T/3)[\tfrac12+\tfrac{1-\lambda}{2-\lambda}]$; the window is closed, $[82/141,6/7]$ (entry at indifference). Three corrections. (a) That interval lies **above** the benchmark cost: $k_T\ge0.0328$ for $\lambda\le0.9$, so at $k=0.02$ the two-sided game has both types trading, not buy-only. (b) Conventional mixtures add equilibria inside the window (verifier 3.4: $\lambda=0.8$, $k=0.05$). (c) At $\lambda\in(0.79,0.883]$ with $c_L=1$, two price schedules support full two-sided trade (verifier 3.5; entry $7/15$ vs $5/12$). |
| 15 | Factor $3/2$ from the off-path belief rule | Q2_discrete_literature C4 | CONFIRMED | Analytical. No-trade cutoff is $\rho\Delta_T/3$ under the Intuitive-Criterion belief at flow 2 and $\rho\Delta_T/2$ under the passive belief. The second equals the continuous model's Prop. A.4 condition. |
| 16 | Conflict: single cutoff (buy-only memos) vs partial-trade interval (literature memo) | Q2 discrete memos | RESOLVED, no conflict | They describe different **menus**: the buy-only menu game has one cutoff; the two-sided menu game at $\lambda=1$ has three regions ($T$ for $k<\rho\Delta_T/6$; buy-not-sell or sell-not-buy on $[\rho\Delta_T/6,\rho\Delta_T/3)$; no trade above). Not about $\lambda$. Verifier 3.3 agrees. |
| 17 | $\Omega_U=2b[(1-1/b)\rho m\Delta_T(r_1)-k]/((1-\rho)(t_H-t_0))=0.011434$ | Q3_stake Result 4 | CONFIRMED | Analytical. Slack $0.002412$; $w_H=1.125$; $\Omega_U=0.011433648$. Also $\Omega_0=0.043097643$ at $r_0$. |
| 18 | No trade at $r_0$ survives every stake | Q3_stake Result 3 | CONFIRMED (existence) | Against the constant schedule entry is $\rho$ at every flow, so the stake term has zero derivative; deviations earn $\lvert q\rvert(\rho\Delta_T(r_0)/2-k)=-0.017917\lvert q\rvert$. Uniqueness at $r_0$ is proved only for $\omega<\Omega_0$; beyond it, **open**. The memo's premise correction is right: $B_{r_0}(1/2)=4.804<6<B_{r_0}(M)=6.880$. |
| 19 | Full-order existence cutoff $\Omega_F\simeq\Omega_{\rm loc}=2.158463$ | Q3_stake Result 5 | CONFIRMED | $J=G_L(-1)=0.140731227283$ (quadrature and closed form (S17) agree to 12 digits); $\Omega_{\rm loc}=2.158462981$. The equality $\Omega_F=\Omega_{\rm loc}$ is a numerical diagnostic. |
| 20 | "About 14 times the (A3) slack" | Q3_story Claim S6 | CONFIRMED, and reconciled | Ratio $13.98$. Three different objects: $\Omega_U$ uses the worst-case stake derivative $(1-\rho)w_H/2b=0.2109$ per unit stake against the worst-case slack; "14 times" uses the actual $L$-state derivative $0.033717$ against the same slack ($\omega\approx0.07$); $\Omega_{\rm loc}$ uses the actual derivative against the actual marginal trading profit $0.072777$ ($\omega=2.158$). No contradiction. |
| 21 | $\Pi^{\rm acc}=0.1407$, $\Pi^{\rm hid}=0.0691$, $\Delta\mathcal R_T=0.257809$, $\lambda^*=1.832$ | Q3_welfare Claims W4, W5 | CONFIRMED | $\Pi^{\rm acc}=0.140731=J$ of the stake memo; $\Delta\mathcal R_T=0.257809$ equals the Section 6.1 dividend; $\lambda^*=1.8319$. Note the welfare memo's $\lambda$ is a trade scale, not the discrete memos' presence probability. |
| 22 | Caveat: an informative price lowers proceeds when the prior already justifies high-cost entry ($\tau<1/2$) | Q3_story Claim S4(b) proves the sign; Q3_welfare Rec. 5 states the region condition | CONFIRMED | Analytical. Example at $r_1$ with $c_H=4$: $\tau=0.465$, proceeds $1.208333$ hidden vs $0.973089$ with access. This is Prop. A.3 deterrence through information. |
| 23 | $c_L$ enters no closed form in eq. (12); entry unchanged for $c_L\in[0,2.26)$ | Q4_normalization Claim 3 | CONFIRMED WITH CORRECTION | $c_L$ is absent from (4), (9)–(12). The window is $[0,B_{r_1}(m))=[0,2.366179)$ for parts (i)–(ii) and $[0,B_{r_2}(m))=[0,2.272133)$ for the three-economy result; $2.26$ is the memo's grid endpoint, not the edge. Q4 also refutes the brief's "only in (A1)": $c_L$ also enters the separate floor at $r_2$, the atomless-cost windows, the pooling example, the reserve events, and the level of $\mathcal W$. |
| 24 | Reading C (the challenger chooses a plan before trading and knows it) removes the price-to-entry channel | Q1_C_choice Claim 10 | CONFIRMED | Analytical, one line: the challenger already knows the only payoff state in the investor's signal. |
| 25 | Price sufficiency with more than two classes needs no collinearity in equilibrium | Q1_N_extensions Claim 7 | CONFIRMED (logic re-read; not re-derived in full) | The monotone-order step ($H$ strictly increasing by the global bound) and the covariance step with the Laplace likelihood ratio are sound as written. Treat as analytical with the memo's own scope: no existence claim for every vector. |
| 26 | The four journal names in the brief were wrong | LIT_extracts | CONFIRMED, brief only | Corrections: Dow–Goldstein–Guembel 2017 is JEEA (not JFQA); Khanna–Sonti 2004 is J. Financial Markets (not JFI); Boleslavsky–Kelly–Taylor 2017 is JET (not JFE); Marmer–Shneyerov–Xu 2013 is J. Econometrics (not JET). The paper's bibliography is right for Dow et al. (JEEA) and Edmans et al. (AER); it does not cite the other three. **No journal-name correction is needed in the paper.** |

### A.2 Other errors, overclaims, and cross-memo contradictions

1. **Q2_laplace_economic, Sec. 3.5.** "The bounded-score class is exactly the class of laws whose tails are at least exponential." Only one direction holds: a bounded score implies $f(z)\ge f(0)e^{-L\lvert z\rvert}$. A law with exponential tails can have an unbounded score. Write "every member has tails at least exponential".
2. **Q2_discrete_literature C1.** "With $\lambda=1$ and equal noise every flow is fully revealing or equal to the prior." True for the four pure profiles only. A mixture gives interior posteriors (verifier 3.4: $0.4$ and $0.6$).
3. **Q2_discrete_literature C3.** "The Intuitive Criterion fixes that belief in one line." It fixes it when some type can gain under some response. When no type can gain, the criterion is silent and the belief is a completion (verifier 3.6).
4. **Q2_discrete_literature C5.** "Prop. A.2 survives only with a floor." Sufficient, not necessary (row 12).
5. **Q2_discrete_literature, Sec. 7, positioning sentence.** "Buy-only trade is also the unique partial-trade equilibrium of the two-sided game." Do not use it at the benchmark cost (row 14). If the author wants buy-only to be endogenous, the cost must lie in $[k_T(\lambda),\rho\Delta_T/3)$, for example $k=0.04$ at $r_1=3$, $\lambda=0.8$; the weak economy then still has no trade because $\rho\Delta_T(1.2)/3=0.001389<0.04$.
6. **Q2_discrete_sell_only Claim 4(d).** The pooled-entry formula $(1+2\rho)/6$ assumes costly entry at posterior 1; the general form is $(e_1+2\bar e)/6$ (verifier). Claim 6's "strict lower inequality in (S3) is necessary" fails at equality, where the tie rule still selects no trade (verifier). Claim 13's "local complementarity only if $\pi_->\pi_+$" is refuted if read as a sign of the local derivative (verifier). Claim 14's "full selling survives at equality in its stake bound" fails under the prescribed tie rule: at equality the investor ties with zero and must choose zero, so the survival condition is strict (verifier).
7. **Q2_discrete_sell_only and Q2_discrete_buy_only, tie rules.** Both memos state the prescribed investor rule (zero at indifference). The verifier shows that this rule removes every genuine mixture, and that some unequal-noise cases then have no equilibrium. Any equilibrium table in the paper must state both tie rules (investor and challenger).
8. **Notation clash across memos.** $\lambda$ is a presence probability (discrete memos), a trade scale (Q3_welfare), a money scale (Q4 Claim 1), and $\lambda(\pi)=\min\{m(\pi),m(1-\pi)\}$ (Q1_N_main). Pick one symbol per object before any text enters the paper.
9. **Q1_N_main Claim 9 and Q1_literature.** Both say the second-price rule makes the information structure harmless for bidding. Correct, with the memo's two limits (private values; selection of truthful bids). The brief's "Section 3.5" of Edmans, Goldstein and Jiang (2015) is working-paper numbering; the published stake discussion is Section II.E, pp. 3787–3788 (LIT_extracts A1). The paper does not cite these sections, so nothing to fix there.
10. **Q2_laplace_technical, "Gaussian $\sigma^2=b$ dominates Laplace".** Numerical diagnostic only, as the memo says. Do not cite it as a fact.
11. **Q1_literature.** Samuelson (1985), Ye (2007), Fishman (1988), Hirshleifer and Png (1989), Athey, Levin and Seira (2011) are known to that memo only through other papers; Persico (2000) and Daniel and Hirshleifer (2018, not 1998) are unverified. The paper already cites Samuelson (1985, *Economics Letters*), Persico (2000), and Hirshleifer and Png (1989); no memo read those three in full, so verify their records before any new use. Check the exact result numbers before adding any new citation from that memo.
12. **Q3_story Claim S7(b)** (weak-economy no trade with a reserve above $\ell$) is a conjecture, as labelled. Do not promote it.
13. **No contradiction** between Q3_stake and Q3_story on the stake (row 20), between Q3_welfare and the paper's Table 2 (row 21), or between the three discrete memos at $\lambda=1$ (rows 10–16). The buy-only and sell-only menus give identical outcomes at $\lambda=1$ (sell-only Claim 13, verifier 13(a)).

---

## Part B. Synthesis

### B.1 Point 1: the challenger's value distribution

**Answer.** The paper's binary value with prior $1/2$ is a special case of the selective-entry
model of the auction literature: a quality class $j$ with a conditional value distribution $G_j$,
and a cost that reveals the exact value (Q1_literature; Gentry and Li 2014; Roberts and Sweeting
2013). Under Reading N (nature draws the class; the investor sees the class) the whole paper
survives for every pair $(G_H,G_L)$ and every prior $\pi$. The second-price rule is why: every
bidder bids its own value, so $t_j$ and $g_j$ do not depend on beliefs, and the price stays affine
in the posterior. The supervisor is right on this point. The one neat new fact is the split
identity: $\Delta_T+(g_H-g_L)=\mathbb E_H\max\{\theta,p\}-\mathbb E_L\max\{\theta,p\}$ at every
incumbent strength. Competition does not change the value gap between the two types. It moves the
gap from the challenger's rent to the target's proceeds. In the binary model this reads
$\Delta_T+(g_H-g_L)=h-\ell$ at every $r$.

**Strongest result (analytical).** Proposition 1$'$ and 2$'$ of Q1_N_main (Claims 4, 10, 11): a
stronger incumbent lowers $g_j$ for every $G_j$; $\Delta_T$ rises under every FOSD strengthening
of every continuous $F$ if and only if $G_H$ dominates $G_L$ above the reserve and both types are
equally likely to fall below it; under these two conditions the reversal of Proposition 2 holds for
every prior, noise scale and low-cost probability on a nonempty open set. Posterior bounds become
$m(\pi),M(\pi)$; (A3) uses $\lambda(\pi)=m(\min\{\pi,1-\pi\})$; eq. (12) shifts $x^*$ by
$-(b/2)\operatorname{logit}\pi$. With more than two classes, equilibrium orders are monotone in
class proceeds, so the price still reveals the posterior vector without collinearity
(Q1_N_extensions Claim 7, analytical; a two-group many-class Proposition 2 is Claim 8).

**What to change, in priority order.**
1. Add the split identity to Section 3.1 (one display, one sentence). No cost.
2. Add one appendix result, "distribution types", with general prior: Claims 4, 10, 11 of
   Q1_N_main, with the value classes of Section 6.3 as the example. Keep the binary model in the
   main text and say that it is the point-mass case.
3. Add one sentence to Section 6.3 (lines 1040–1050): at $p=1.1$ the low class is inadmissible,
   $\Delta_T$ falls in $r$ on $(p,\sqrt3p)$, both economies trade, and the fall in preparation
   ($0.540309\to0.511638$) is the fixed-experiment deterrence of Proposition A.3. The text is not
   wrong; it is unexplained.
4. Adopt the selective-entry vocabulary in Section 2.2 ("quality class", "pre-entry signal",
   "preparation cost (entry cost)"), with the citations in Q1_literature Sec. 7. Check the
   unverified entries first.
5. Define ownership for distribution types as $\pi e_HW_H$ and state the ownership condition.

**What remains open.** The size of a tolerable admissibility gap (numerical diagnostic on one
family: feasible up to $D(p^-)=0.10$ at $\rho=0.25$, infeasible at $0.20$). Incumbent families
other than the uniform in Claim 11. The widest symmetric class in Q1_N_numerics (N100) finds no
pair in the sufficient windows. Reading N3 (the investor sees $\theta$) with a connected value
continuum: a no-trade region of intermediate values exists and the global order proof does not
cover it (Q1_N_extensions Claims 12–13). Reading C in its pure form removes the mechanism (Q1_C_choice
Claim 10); the hybrid (nature draws the type, the price informs, the challenger then picks risk)
has only a jump condition, not an equilibrium analog.

### B.2 Point 2: the microstructure

**Answer, Laplace.** The proofs need two things from the noise: no order flow is conclusive
(bounded likelihood ratio, Prop. A.1), and a marginal change in the order changes the flow density
by at most the fraction $1/b$ of its level (score bound, (A.6)). Both follow from one condition,
$\lvert(\log f)'\rvert\le L<1$. Proposition 2 holds on that whole class with the same proof
(Q2_laplace_technical R16, analytical), with the largest attained posterior in the upper part of
(A2). Inside the class, Laplace with $b=1/L$ is the extreme member: least dispersed, most
informative at every pure order profile, and a Blackwell parent of every log-concave member. The
logistic law is Laplace plus independent noise. Gaussian noise fails both properties: a large flow
is near-proof of information, the residual floor is zero, and full orders can fail (R13, R15). The
"clean linear posterior" is exact: between the two orders the Laplace log odds equal those of a
Gaussian with variance $b$, and outside they are clipped (R12). Three standard stories give a
Laplace law (exponential buy and sell volumes; Gaussian with exponential variance; Brownian noise
at an exponential time), and the time-change story fits a sale process best (Q2_laplace_economic).

**Answer, discrete.** A buy-only menu with three-point noise reproduces the main result with a
one-line proof: one exact cutoff $k=\rho\Delta_T/3$ separates no trade from purchases, with no
coexistence, for every presence probability $\lambda$ (rows 10–13). The costs: beliefs reach 0 and
1, so the floor and the ceiling move ($c_L\le g_L$ at an $L$-revealing flow; $c_H\le g_H(r)$ for
recruitment); the return to $\rho$ needs $r_2>7.97$ at the benchmark, and otherwise entry falls
below $\rho$; no feedback from entry to trading at equal noise, hence no Proposition 3; an off-path
flow remains in the no-trade case and needs a belief rule, which moves the no-trade cutoff by the
factor $3/2$. The two-sided menu is less clean: a separate partial-trade cost interval, mixed
equilibria inside it, and, at intermediate presence with the benchmark $c_L=1$, two price
schedules for the same trades (verifier 3.5).

**Strongest results.** Analytical: R16 (class proposition), R8–R10 (extremality and the logistic
decomposition), and the discrete Proposition 2d (buy-only menu, equal noise, presence $\lambda$)
with exact cutoffs. Numerical diagnostic: the entry table across laws (Laplace $0.5228$, logistic
$0.3015$, hyperbolic secant $0.3766$, Student $t$ $0.3750$, Laplace+Gaussian $0.4204$), and the
verifier's sweep of $495{,}450$ discrete cases.

**What to change, in priority order.**
1. Correct the Blackwell sentences (Section B.4, items 1–2). This is an error.
2. Replace the one-line justification in Section 2.3 (lines 337–340) by the draft paragraph of
   Q2_laplace_technical Sec. 7, merged with the economic stories of Q2_laplace_economic Sec. 3.6.
   Check every citation in that paragraph against the full text first.
3. Extend Prop. A.5 to the class $\mathcal C_L$, $L<1$ (R16), with $\bar\mu_f$ in (A2), and list
   the members (logistic, hyperbolic secant, Student $t$, Kyle-type Gaussian plus an independent
   Laplace component). Add the extremal lemma (R8, R9). The proof is short because Online Appendix
   A.3 already holds at this generality.
4. Add a discrete companion, buy-only, equal noise, presence $\lambda\in(0,1)$: Proposition 2d
   with (B1) $c_L\le B_{r_1}(m_\lambda)$, (S2) $B_{r_0}(1/2)<c_H\le g_H(r_1)$, (S3)
   $\rho\Delta_T(r_0)/3<k<\rho\Delta_T(r_1)/3$, and for the return $g_H(r_2)<c_H$ with the floor at
   $r_2$; the exact cutoff $\mathfrak r(3k/\rho)$; $\mathsf E=\rho+(1-\rho)\lambda/6$. State: the Intuitive-Criterion completion at the one
   off-path flow; both tie rules; "pure profiles"; the floor is sufficient, not necessary; and
   that the benchmark $c_L=1$ needs $\lambda\le0.8827$. Do not claim that buy-only is endogenous at
   the benchmark cost.
5. Report one more law in Section 5.1 beside the logistic number, and say that Laplace sets the
   upper envelope at the benchmark as a numerical fact, not as a consequence of Blackwell dominance.

**What remains open.** Proposition 3 for other noise laws (its certificates OA.65, OA.71, OA.74 are
Laplace-specific). Existence and uniqueness under pure Gaussian noise. Blackwell dominance at mixed
profiles for members that are not log-concave (conjecture). A single-cutoff theorem for general
three-point noise: refuted in general (unequal noise restores coexistence and can remove every
equilibrium under the prescribed tie rule). A theory of the two-sided price-pool multiplicity at
intermediate presence.

### B.3 Point 3: who the investors are, and $t_0$

**Answer.** The level $t_0$ is harmless: it cancels from every trading incentive, and the dividend
diagnostic of Section 6.1 is the same cancellation (Q3_story S1). The real content of the question
is the increment $t_\theta-t_0>0$ for both types: every holder of $V_T$ wants entry, with either
challenger. The paper's investor is an outsider with no stake, so it trades only on the residual
$V_T-P$. Target shareholders gain from the mechanism through entry, not through the price: a holder
who keeps the shares receives $V_T$; a higher interim price is a transfer. At $r_1$ price access
raises proceeds by $0.257809$ per share, and the informed investor's profit $0.1407$ is paid by the
traders who provide liquidity. Initial shareholders as a group gain iff the trade scale is below
$\lambda^*=1.832$ (Q3_welfare W5). The gain needs the recruiting region $\tau>1/2$; where the prior
already justifies expensive entry, an informative price deters and lowers proceeds (Q3_story S4b).
A shareholder-investor with a stake $\omega$ wants entry for its own sake and buys in both states
at the margin (S6). Small stakes keep Proposition 2 ($\omega<0.0114$ order units, analytical);
the full-order equilibrium itself survives to about $2.16$ (numerical); beyond that, pooled
purchases are never an equilibrium and the correspondence is open (Q3_stake).

**Strongest results.** Analytical: the ledger identities (Q3_welfare W1–W5), the sign of S4, the
stake split (S4)–(S5) of Q3_stake, and the sufficient bounds $\Omega_U$, $\Omega_0$. Numerical
diagnostic: $\Omega_F\simeq2.158463$, the partial-sale branch to $2.498855$, and the welfare
table.

**What to change, in priority order.**
1. Add the roles paragraph to Section 2.3 (Q3_story Sec. 7.1): an outside specialist with no net
   stake and short-sale access; noise as net liquidity demand $Z=Z_+-Z_-$ (which also gives the
   Laplace law with exponential volumes); competitive market makers; every share held at the sale
   receives $V_T$.
2. State the role of $t_0$ once in Section 3.3: it cancels from the residual; only a net stake
   gives a reason to care about entry for its own sake, and such a holder gains from entry with
   either type.
3. Add $\Pi$ and $\lambda^*$ beside the proceeds gain in Section 6.1, and the within-class split
   (holders who must trade can lose). Do not let Table 2 Panel C read as a pure shareholder gain
   of $0.257809$. Add the S4(b) caveat.
4. Add the stake extension as an appendix remark: payoff split, $\Omega_U$ with its scale in
   order units, the existence cutoff as a numerical diagnostic, and the contrast with Edmans,
   Goldstein and Jiang (2015, Section II.E): there the stake cancels because the action is
   corrective; here it does not because selling on bad news deters entry.
5. Cite Kyle and Vila (1991) and Edmans et al. (2015) for informed blockholders in the "abstracts
   from" sentence of the literature review. Kyle and Vila's full text was not accessible to any
   memo; cite the mechanism only.

**What remains open.** The equilibrium correspondence for stakes above $\Omega_F$ (mixed orders,
nonmonotone entry, plateau atoms). Exact uniqueness limits at $r_0$ and $r_1$. Proposition 3 with
a stake. Whether the board maximizes proceeds to holders at the sale or the ex-ante value of
initial holders (Q3_welfare W7, conjecture).

### B.4 Point 4: normalization

**Answer.** $c_L=1$ is a legal unit choice when $c_L>0$, but it simplifies nothing: $c_L$ appears in
no closed form, only in participation floors and in the level of $\mathcal W$ (Q4 Claims 3–5). Any
$c_L\in[0,B_{r_1}(m))=[0,2.366)$ gives the same orders, prices, beliefs, entry and proceeds at the
benchmark. The useful unit is $\ell=1$, which every parameter vector already uses and which
shortens eq. (4). Treat $c_L$ as a slack parameter and compute with $c_L=0$. Two cautions. First,
$c_L=1$ is not harmless in a discrete model with an $L$-revealing flow, because $g_L(r)<1/2$ when
$\ell=1$; there the floor needs $c_L\le g_L$ or the buy-only menu with $\lambda\le0.88$. Second, do
not take $p\to0$: it removes $t_0$ but not the increment $t_L-t_0$, and the reserve acts like an
extra preparation cost $p^2/(2r)$ that shrinks with strength.

**Strongest result (analytical).** Q4 Claims 1 and 3: money-scale invariance, and slackness of
$c_L$ on its window, with the identities of Claim 4 ($t_\theta+g_\theta=\theta$;
$g_H-g_L=(h-\ell)-\Delta_T$; $\Delta_T=\ell[\cosh\ln(r/\ell)-1]$).

**What to change, in priority order.**
1. Say in Section 2.2: "Money is measured in units of the low acquisition value, $\ell=1$."
2. Add a remark under Proposition 2: the outcome does not depend on $c_L$ in $[0,B_{r_1}(m))$;
   calculations use $c_L=0$. If the benchmark vector itself changes to $c_L=0$, the level of
   $\mathcal W$ in Table 2 Panel C rises by $\rho\cdot1=0.25$; the differences do not change.
3. State the ratio form of (A3) and the belief form of (A2) (Q4 Sec. 7).
4. Do not normalize $c_L$ to 1 and do not set $p\to0$.

**What remains open.** Nothing technical. The content choice between a small positive $c_L$ and a
"ready buyer" at $c_L=0$ is the author's.

### B.5 Recommended revised baseline

The evidence supports **keeping the current main model** (binary values, prior $1/2$, Laplace
noise, two-sided continuous orders, an outsider investor with no stake) and adding the
generalizations around it. Reason: every generalization reduces to the current model as a special
case, and none of them changes the mechanism. Keeping the main text fixed means that the
Proposition 3 certificates, the Section 5.1 numbers, Table 2, and eq. (12) need no recomputation.

| Change | Where | Proof cost | Numerics cost | Existing results touched |
|---|---|---|---|---|
| Selective-entry vocabulary; split identity | Sec. 2.2, 3.1 | none | none | none |
| Distribution types with general prior (Prop. 1$'$, 2$'$) | new appendix section | medium (Claims 4, 10, 11 are written; ownership condition; reserve caveat) | small (value-class table; one script) | Section 6.3 gets one sentence; OA.52 becomes a case |
| Log-Lipschitz noise class; Laplace as extreme member | Sec. 2.3 paragraph; Prop. A.5$'$ replaces A.5; extremal lemma in OA | medium (R16 is a paragraph given OA A.3; R8–R9 are one page) | small (entry table across laws exists) | A.5 subsumed; Blackwell sentences corrected; Prop. 3 untouched |
| Discrete buy-only companion with presence $\lambda$ | new subsection after Prop. 2 or OA section | medium (Prop. 2d; off-path completion; price sufficiency; both tie rules) | small (exact rationals; verifier tables) | none; state that it does not carry Prop. 3 |
| Named outsider investor; liquidity-trader noise; welfare transfer | Sec. 2.3, 3.3, 6.1; Table 2 note | none | small ($\Pi$, $\lambda^*$ rows) | Table 2 Panel C reading |
| Stake remark with $\Omega_U$, $\Omega_0$ | OA remark | small (bounds exist) | small | none |
| $\ell=1$ unit; $c_L$ slack | Sec. 2.2; remark under Prop. 2 | none | none (or $+0.25$ on $\mathcal W$ if $c_L=0$ is adopted) | Table 2 Panel C level only |

If the author instead moves any of these into the main model (a general prior, distribution types,
a different noise law, a stake, or a discrete trading stage), then the following must be redone:
the Proposition 3 certificates (OA.65, OA.71, OA.74 are Laplace-specific and assume no stake), all
Section 5.1 numbers, Table 2, Section 6.3, and the benchmark vector itself (the discrete model
needs $r_2>7.97$ and a floor-compatible $c_L$). That is a large task with no new mechanism in
return.

### B.6 Corrections needed regardless of the revision

1. **`overleaf/paper/main.tex`, lines 1877–1880** (Appendix A.4, after Prop. A.5). Replace
   "They do not have a common variance, and neither experiment Blackwell dominates the other in
   general; the comparison concerns where posterior mass sits relative to the common bounds
   $m,M$." by: "They do not have a common variance. At a common scale $b$ the logistic law equals
   the Laplace law plus independent noise, so the Laplace price experiment Blackwell-dominates the
   logistic one at every order profile, including the full-order equilibria compared here. At a
   common variance neither dominates. Dominance does not order entry: $\Pr(\mu_X\ge\tau)$ is not
   convex in the posterior, so the entry comparison concerns where posterior mass sits relative to
   the bounds $m,M$." (Analytical: R10; the crossing at common variance is a numerical
   diagnostic.)
2. **`overleaf/paper/online_appendix.tex`, lines 2631–2632** (C.5 inputs). Replace "do not claim
   equal variance or a Blackwell ordering between the laws" by "do not claim equal variance; at a
   common scale the Laplace experiment Blackwell-dominates the logistic one, but do not claim an
   ordering of entry".
3. **`main.tex`, line 860** (Section 5.1). Optional sharpening: "The comparison concerns the
   location of posterior mass at a common scale; the Laplace experiment is the more informative
   one, but informativeness does not order entry."
4. **`main.tex`, lines 1040–1050** (Section 6.3). Clarification, not an error: add the sentence in
   B.1 item 3.
5. **`main.tex`, Prop. A.5 proof, line 1866** ("The bound $\lvert f'\rvert\le f/b$ is all that ...
   use"). Correct for the logistic law. If the proposition is generalized to the class, add that
   (A2) uses the largest attained posterior $\bar\mu_f$.
6. **Journal names.** None to fix in the paper (row 26). The corrections apply to the brief.
7. **Vocabulary.** If any memo text enters the paper, resolve the $\lambda$ clash (A.2 item 8) and
   use one word for the class ("class", not "type", because "type" names the investor's
   information).

### B.7 Questions for the supervisor

1. "Choosing from a few different distributions": does he mean that nature draws the distribution
   and the challenger learns it only through information (Reading N), or that the challenger
   itself picks a plan before trading (Reading C)? Reading C in its pure form removes the price
   channel; Reading N keeps everything.
2. Is he content with the binary model in the main text and the distribution-type result in an
   appendix, or does he want the general model to lead?
3. For the discrete companion: is a presence probability $\lambda<1$ (the Edmans, Goldstein and
   Jiang device) and the Intuitive-Criterion completion at the one off-path flow acceptable? Is an
   exogenous short-sale constraint (buy-only) acceptable, given that it is not the endogenous
   outcome at the benchmark cost?
4. For the investor: is "an outside specialist with no net stake" the intended baseline, with the
   blockholder as an extension? A blockholder baseline changes Proposition 2 and needs the
   large-stake equilibrium, which is open.
5. Normalization: $\ell=1$ with $c_L$ treated as slack (computed at $c_L=0$), rather than
   $c_L=1$. Agreed?

### B.8 Next research tasks, ranked

| Rank | Task | Effort | Status now |
|---|---|---|---|
| 1 | Correct the two Blackwell sentences; optional Section 5.1 sharpening | small | analytical, ready |
| 2 | Section 2.3 noise paragraph; Prop. A.5$'$ for the class; extremal lemma; one more law in Section 5.1 | medium | analytical, written in memos |
| 3 | Appendix "distribution types": Prop. 1$'$, 2$'$, general prior, ownership condition, reserve caveat; Section 6.3 sentence | medium | analytical, written in memos |
| 4 | Roles paragraph; $t_0$ sentence; $\Pi$, $\lambda^*$, S4(b) caveat in Section 6.1 and Table 2 note | small | analytical |
| 5 | Discrete buy-only companion with presence $\lambda$; state both tie rules and the off-path completion; cite the verifier's two-sided price-pool example as the reason for buy-only | medium | analytical plus numerical diagnostic |
| 6 | $\ell=1$ statement; $c_L$ slack remark; ratio form of (A3) | small | analytical |
| 7 | Stake remark with $\Omega_U$, $\Omega_0$; contrast with Edmans et al. Section II.E | small | analytical |
| 8 | Large-stake equilibrium correspondence (mixed orders, nonmonotone entry) | large | open |
| 9 | Proposition 3 certificates for other noise laws (new interval quadrature) | large | open |
| 10 | N3: investor sees $\theta$ on a connected continuum; the no-trade region | large | open |
| 11 | Reading C hybrid (type by nature, risk chosen after the price): equilibrium analog | large | open; jump condition only |
| 12 | Tolerable admissibility gap $D(p^-)$: a sharp threshold | medium | numerical diagnostic on one family |
| 13 | Two-sided discrete menu: theory of price-pool multiplicity at intermediate presence | medium | numerical diagnostic |

---

## Plain summary

The four points lead to additions, not to a new model. Point 1: the paper's two-value challenger
is the point-mass case of a standard entry model with a quality class and a value distribution.
Everything survives for any distributions and any prior, because the second-price sale makes
beliefs irrelevant to bids. One identity makes the mechanism plain: competition moves a fixed value
gap from the challenger to the target. The one new force is the reserve, which can reverse the
sign when the low class fails it more often. Point 2: the proofs need only that no order flow is
conclusive and that the log-density has a slope below one. Laplace is the extreme member of that
class, and the logistic law is Laplace plus noise. This corrects one sentence in the paper. A
buy-only discrete model gives the main result with an exact cutoff, but it needs a presence
probability below one at the paper's costs, it returns to the floor much later, and it cannot
carry the coexistence result. Point 3: the price level never matters; the increment from entry
does. Shareholders gain through entry, pay the informed trader's profit, and net a gain of about
$0.12$ per share at the benchmark. A shareholder-investor with a large stake would buy on bad news,
which breaks the result; keep the outsider as the baseline. Point 4: measure money in units of the
low value, and treat the low cost as slack; do not set it to one.

The verifier's numerical check of the discrete models is complete and agrees with the memos at
the benchmark. It adds two cautions: the entry floor is sufficient, not necessary, for the price to
reveal beliefs; and the two-sided menu can have two price schedules at intermediate presence.
