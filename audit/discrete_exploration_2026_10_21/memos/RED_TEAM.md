# Red team: verdicts on the headline claims

Phase 3, 21 October 2026. Scripts: `scripts/RED_TEAM/` (print only; each output sits beside its script as `*.out.txt`).
Paper source: commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` of `overleaf/paper` (`main.tex`), read through `git show`.

## 1. Scope

This memo attacks the headline claims of the 25 memos in `memos/`. For each memo it names the weakest step of each headline result. It re-derives the key steps and spot-checks the numbers that carry the conclusions. It does not explore new models.

The five check scripts are:

| Script | What it recomputes |
|---|---|
| `rt_dlaplace_base.py` | the base buy-only discrete-Laplace model at $c_H=5$: constants, window, ceiling, feedback, branch boundaries $r_I,r_F,r_N,r_U$, the equilibrium set on $[1.40,1.77]$ under each pair of tie rules, a single-crossing check, welfare |
| `rt_two_sided.py` | the C1 constants against the paper: $M$, $r_C$ at $c_H=6$, $r_N$, $\mathfrak r(k)$, $r_U$, entry, and the paper's own entry from eq. (12) |
| `rt_reserve_cL.py` | the C8 seller problem by a finite candidate list and a grid, for $c_L\in\{0,0.1,1\}$ |
| `rt_refuted.py` | the five refuted claims: the feedback number, the C5 ledger, the C7 bid, the C8 sunk-preparation deviation, the C3 ceiling at $\delta=0.8$ |
| `rt_three_point.py` | the three-point cutoffs and the floor argument behind the A.10 verdict |

All five run in under two seconds. Exact fractions are used where the inputs are rational; otherwise 30 to 40 decimal digits. Every number quoted below comes from these outputs or from the named memo.

Verdict vocabulary: CONFIRMED, CONFIRMED WITH CORRECTION, OVERCLAIMED (the result holds, but its label or its scope is stronger than the evidence), REFUTED, OPEN. Status vocabulary: analytical, computer-assisted, numerical diagnostic, conjecture, open.

Tie rules are named as in B2: investor (I0) chooses zero at indifference, (IM) may mix; challenger (C1) prepares at indifference, the paper's rule, (CM) may mix. The directional completion puts posterior one on an unused top flow.

The C4 rows use the verdicts of `X_C4_check.md`, which was complete when this memo reached C4 (Section 3.12).

## 2. Verdict table

| # | Memo | Claim | Author status | Verdict | Evidence (one line) |
|---|---|---|---|---|---|
| 1 | A1, A2 | Complete three-point correspondence; one cutoff $K=\tfrac23\rho(1-\pi)\Delta_T$; presence $\lambda$ does not move it | analytical, computer-assisted | CONFIRMED | A1 and A2 agree on every target; $K=1/18$ at $r=3$; cutoff $\mathfrak r(6/25)=1.973212$ (`rt_three_point`) |
| 2 | A1, A2 | Passive beliefs leave no equilibrium on $[K,\tfrac32K)$ under rule Z | analytical | CONFIRMED | 1,332,674 empty grid points recomputed by A1 from closed forms; the gap is the unused top flow |
| 3 | A1 | Equal noise is a knife-edge (Result 10 lemma) | analytical | CONFIRMED | $K$ constant in $s$ iff $a=d=c$; the coefficient argument is sound |
| 4 | A1 | Prop. 2-D with exact iff conditions; $1/4\to3/8\to1/4$; return at $7.968627$ | analytical | CONFIRMED | $r_C(1)=4+\tfrac32\sqrt7=7.968627$; $145/192$ proceeds at $r=3$ |
| 5 | A1 | Prop. A.10 dies because of $c_L=0$, also under Laplace | analytical | CONFIRMED WITH CORRECTION | "Not applicable" is the right label: its hypothesis fails at $c_L=0$. At $c_L=1$ discreteness does matter (Section 4.5) |
| 6 | A1 | Reserve $p=1.1$ lowers weak-economy proceeds, $0.392665\to0.344792$ | analytical | CONFIRMED | Hand check: $t_0=0.091667$, $w_H=1.0125$, $e_H=1/2$, so $\mathcal R_T=0.344792$ |
| 7 | B1, B2 | Prop. 2 analog on an open set; entry $0.25\to0.625\to0.25$ at $(1.2,3,4.2)$; ownership $0.358422$; window $(4.804167,5.312161]$; $r_C=3.986097$ | analytical | CONFIRMED | All reproduced to 30 digits (`rt_dlaplace_base`) |
| 8 | B1, B2 | Feedback $+0.175836$ with entry after good news, $+0.058335$ without | analytical | CONFIRMED | $2\rho a\Delta_T/(1+a)^2-k=0.0583346$; the brief's $+0.060$ is wrong at three decimals |
| 9 | B2 | Prop. 3 analog: no trade and full purchases coexist on $[r_F,r_N]=[1.443322,1.747878]$; third outcome under (CM); entry strictly ordered within a strength | analytical | CONFIRMED | $r_F=\mathfrak r(k(1+a)^2/((1+\rho)a))$, $r_N=\mathfrak r(2k/\rho)$; feedback condition $(1+\rho)a/(1+a)^2=0.2938>\rho/2$ |
| 10 | B2 | Entry rises on the $\hat s$ branch just below $r_F$; region order in $r$ rests on a grid | analytical (local); open | CONFIRMED; the open item is now a numerical diagnostic | One sign change each for $K_1(s^*(r))-k$ and $K_\rho(s^*(r))-k$ on 5,701 grid points in $[1.05,3.9]$ |
| 11 | B2 | Access to prices: $\Delta\mathcal R_T=0.327490$, $\Delta\mathcal W=0.148310$ | analytical | CONFIRMED | Reproduced; $\mathcal W$ levels differ by convention between B1 and B2 (Section 4.6) |
| 12 | B1, B2 | Exact $k$ region $(0.005770,0.078978)$ under (IM, CM) | analytical | CONFIRMED | Lower end $K_1(s^*(1.2))=0.005770$ re-derived by hand; B1 and B2 agree |
| 13 | B2 | Coexistence and $r_N$ survive small changes of the noise law (Result 12) | analytical | CONFIRMED | $K_0$ is noise-free; $K_F$ is continuous in $\ell^1$ with entry fixed off a tie |
| 14 | C1 | Three posterior values; full orders give the paper's $(M,\tfrac12,m)$ | analytical | CONFIRMED | $M=1/(1+a^2)=0.731059$ (`rt_two_sided`) |
| 15 | C1 | Prop. C1.1: Prop. 2 at the paper's $c_H=6$ and strengths $(1.2,3,3.6)$; entry $0.569293$ | analytical | CONFIRMED | Openness needs strict (D1), (D2); the right end of the window needs (C1) |
| 16 | C1, X_C1 | $r_C=3.592658519$ and $r_N=1.747877538$ equal the paper's values exactly | analytical | CONFIRMED | Both reproduced to 30 digits; reasons in Section 4.2 |
| 17 | C1 | NT and T coexist on $[1.515898,1.747878]$, which contains $1.55,1.60,1.65$ | analytical | CONFIRMED | $c_T=0.227825>\rho/2$; $\mathfrak r(k/c_T)=1.515898$ |
| 18 | C1 | The buyer is inframarginal and the seller marginal (Result 4, general) | analytical | OVERCLAIMED | Holds for the corner algebra and the FB-PS branches; fails on the PB-NS branch at $c_H=5$ and at constant entry (X_C1 E4) |
| 19 | C1 | An FB-PS branch exists only on $(1.515898,1.533807)$; only it has rising entry | numerical diagnostic | CONFIRMED WITH CORRECTION | A second FB-PS branch with entry $\rho$ on $(1.819330,1.840115)$ at $c_H=6$; a PB-NS branch with rising entry on $(1.405430,1.443322)$ at $c_H=5$ (X_C1 E1, E2) |
| 20 | C1 | The upward entry order at $1.55$ to $1.65$ is not recovered | numerical diagnostic | CONFIRMED | Only NT and T exist there under baseline ties; T entry is flat |
| 21 | C1 | "This memo confirms" the brief's $+0.176$ and $+0.060$ | — | CONFIRMED WITH CORRECTION | C1's own number is $+0.058335$; $0.060$ is wrong at three decimals |
| 22 | C2 | Two discrete-Laplace rounds: coexistence at $(r,k)=(1.7,0.02)$, $c_H=6$, both designs | analytical | CONFIRMED | Rational bounds hold; $C_-=5/51$ at $a=3/5$, $r=3$ re-derived; caveat: two units of capacity (Section 3.5) |
| 23 | C2 | Design S: entry $0.25\to0.448747\to0.25$ at $(1.2,3,3.6)$, $c_H=6$ | computer-assisted | CONFIRMED | Rational enclosure of $e^{-1/2}$ needed; the ceiling margin at $3.6$ is $0.00269$ |
| 24 | C2 | Equal noise: no graded beliefs, no open coexistence interval | analytical | CONFIRMED WITH CORRECTION | Needs $k\ne K(\pi)$; an off-path second order at $(H,-1)$ must be amended (X_C2) |
| 25 | C2 | Retained share: exact mixed equilibrium $\beta=26/81$ | analytical | CONFIRMED | $\mu_-=55/136$; first-order gain exactly zero |
| 26 | C2 | Horizon-free posterior bound (C2.5) | analytical | CONFIRMED | The bound is $0.992626$ at $r=3$: valid, weak |
| 27 | C3 | Three-point delay: entry $11/24$ at $r=3$; round 2 is the bottleneck; no coexistence | analytical | CONFIRMED WITH CORRECTION | Needs private preparation decisions; closed plateau endpoints are wrong; round-1 feedback is $(1-\rho)w_H/9>0$ (X_C3) |
| 28 | C3 | Discrete-Laplace delay: entry $0.625\to0.448747$ at $r=3$, $\delta=0.95$; ceiling $3.986\to5.606$ | numerical diagnostic | CONFIRMED | Analytical after X_C3's bounds; needs $\delta>\delta^*(3)=0.898963$ |
| 29 | C3 | Delay creates coexistence at $(r,c_H,\delta,k)=(3,5.5,0.95,0.09)$ | numerical diagnostic | CONFIRMED | Analytical after X_C3's rational bounds; not at the benchmark $k$ |
| 30 | C3 | Late ceiling at $\delta=0.8$ equals $8$ | numerical | REFUTED | The root is $2.910409$; at $r=8$ the residual is $-1.489972$ (`rt_refuted`) |
| 31 | X_C3 | Public observation of the first preparation decision kills the three-point delay construction | analytical | CONFIRMED | After an observed wait the high-cost type is identified; the round-2 residual is zero |
| 32 | C5 | Exact stake bounds $268/1485$, $152/75$, $2144/825$; Prop. 2 analog iff $\omega<\omega_H(r_0)$ | analytical | CONFIRMED WITH CORRECTION | Endpoints shared across branches; the regime needs $\tau<1$ (X_C5) |
| 33 | C5 | Class L buys from $\Omega_2$ by a mixture, never purely; S Blackwell-dominates M | analytical | CONFIRMED WITH CORRECTION | Under T1 only on $[\Omega_2,\Omega_1)$ |
| 34 | C5 | No equilibrium above $\Omega_1$ under the paper's rules; M$'$ under (CM) | analytical | CONFIRMED | $G_L$ rises in $\beta$; the jump at $\beta_{\max}$ cannot be crossed without a mixture |
| 35 | C5 | Five equilibria at $\omega=9/25$ in the discrete-Laplace model | computer-assisted | CONFIRMED | Rational enclosures in X_C5; needs T2 |
| 36 | C5 | Manipulation moves the challenger's rent to shareholders | computer-assisted | REFUTED | $\Delta T=649/27072=+0.023973$, $\Delta C=-59/192=-0.307292$, ratio $11/141$; surplus loss $96.67\%$ confirmed (`rt_refuted`) |
| 37 | C5 | The weak-economy result holds for $\omega\le0.1805$ | analytical | CONFIRMED WITH CORRECTION | Only under the directional belief; a passive belief supports no trade at every stake |
| 38 | C6 | Equal noise: exact research cutoff, no feedback | analytical | CONFIRMED | $D$ does not depend on $s$ |
| 39 | C6 | Discrete Laplace: no research and full research coexist for $\kappa\in[19/600,0.087918]$ at $r=3$ | analytical | CONFIRMED | Exact chain $19/600<1/20<561/6400$; (CM) adds a third equilibrium |
| 40 | C6 | $c_H=6$ blocks expensive entry at every strength | analytical | CONFIRMED WITH CORRECTION | Needs $b>1/\ln(5/3)=1.957615$; $B_1(M_1)=5.977134$, margin $0.0229$ |
| 41 | C6 | $\kappa=0.02$: unique research; entry $0.25\to0.625\to0.25$ at $(1.2,3,4.2)$ | analytical | CONFIRMED | Not at $3.6$, where entry stays $0.625$ |
| 42 | C6 | Public acquisition removes the coexistence | analytical | CONFIRMED | Needs a unique acquired continuation; holds at $r=3$ |
| 43 | C6 | Research can cut welfare while it raises entry | numerical diagnostic | CONFIRMED | Sign depends on $\kappa$: $+0.017$ at $0.09$, $-0.036$ at $0.094$ |
| 44 | C7 | No private lockup is ever accepted (C7.1) | analytical | CONFIRMED WITH CORRECTION | The $\mu>0$ case needs the imitation argument (X_C7) |
| 45 | C7 | Jump bid after good news: entry $0.625\to0.366988$; a pure transfer of $0.171896$ to the incumbent | analytical; computer-assisted | CONFIRMED | $c^*=0.935901$ re-derived (`rt_refuted`); conditional on rule IC-P and the boundary tie |
| 46 | C7 | Under Condition N the investor earns the no-feedback value $0.058335$; unique trading | analytical | CONFIRMED | $S=\rho\Delta_T$ when $c^*\le\ell$ |
| 47 | C7 | Prop. 2 survives, weakened (C7.6) | analytical | OVERCLAIMED | At $c_H=5$ a reserve-bid equilibrium at $r_0$ gives entry $0.5625$, which reverses the comparison; the result is selection-dependent |
| 48 | C7 | Silence pooling survives IC and D1 throughout Case C | analytical | REFUTED | At $(r,\mu)=(3,3/5)$ the bid $J=2$ bounds profit by $24/5<5$ under every belief; type $R=3$ gains $1/20$ |
| 49 | C7 | Every larger bid through $\ell$ survives | analytical | REFUTED in general | Counterexample at $(r,\mu)=(6/5,11/20)$ (X_C7); a continuum does survive at the benchmark posterior |
| 50 | C7 | Entry drops to $\rho$ at $r_C$ | analytical | CONFIRMED WITH CORRECTION | Selected entry at $r_C$ is $0.297038$; the floor starts strictly above $r_C$ |
| 51 | C7 | New mixed branches with partial preemption (C7.8) | numerical diagnostic | CONFIRMED | Local rational certificate at $r=1.6$ (X_C7); regions remain numerical |
| 52 | C7 | Laplace cross-check: entry $0.522757\to0.304840$ | numerical diagnostic | CONFIRMED | Independent integrals agree (X_C7) |
| 53 | C8 | $p^*=h$ on $[m_1,M_1]$ at $r\in\{1.2,3\}$; entry $\rho$; full purchases; proceeds $1.25$ | computer-assisted | CONFIRMED; label OVERCLAIMED in C8 | C8's 25-point sample is not a certificate; X_C8 supplies one; my candidate list and grid agree (`rt_reserve_cL`) |
| 54 | C8 | Prop. 2 analog fails at the benchmark pair | computer-assisted | CONFIRMED | $B(h,M_1)=0<5$; $\bar\Delta^*(r_0)=10>k$ |
| 55 | C8 | Unobservable preparation before the reserve gives the same game | analytical | REFUTED | With preparation sunk at one, the deviation to $p=h$ at $(3.6,M_1)$ earns $6.224593>1.584420$ |
| 56 | C8 | Observable preparation: $p=h$ after entry; proceeds $2.118648$ | numerical diagnostic | CONFIRMED | Analytical reserve proof in X_C8 |
| 57 | X_C8 | $0<c_L\le0.1$: $p^*=h-c_L/\mu$, entry $\rho$; $c_L=1$: entry $0.625$ at $r=3$, proceeds $1.181022$, full purchases at both strengths | computer-assisted | CONFIRMED | All reproduced (`rt_reserve_cL`): $p^*(m_1)=1.582464$, $p^*(M_1)=1.674539$ |
| 58 | C9 | Existence under both mixtures and the directional completion | analytical | CONFIRMED | The completion is essential: a passive belief leaves no equilibrium at $(r,k)=(3,7/100)$ (X_C9) |
| 59 | C9 | Exactly three outcomes on $[63/40,317/200]$ | analytical | CONFIRMED | Two under the paper's tie rule (C1) |
| 60 | C9 | Upward branch: entry $0.526900<0.535188<0.543596$ | computer-assisted | CONFIRMED | Analytical on the window; the window is $(1.574345,1.588760]$, width $0.0144$ |
| 61 | C9 | Ordered informative equilibria are recovered (Section 4) | analytical | OVERCLAIMED | One branch, a narrow window, a mixture at indifference, no $(1,-v)$; branch T falls |
| 62 | C9 | Challenger mixtures repair an existence gap found earlier | analytical | CONFIRMED WITH CORRECTION | The gap (C9.5) is C9's own construction (X_C9) |
| 63 | C10 | D1: the trading stage at any public prior | analytical | CONFIRMED | Direct sum and closed form agree to $10^{-51}$ |
| 64 | C10 | D3: optimal test $\varphi^*=0.699167$; entry $0.625\to0.786353$; ownership $\to0.5$ at $r=3$ | computer-assisted | OVERCLAIMED label; result CONFIRMED | Float grid plus bisection; X_C10's interval at $r=3$ certifies the benchmark; concavification needs a selection and an existence domain |
| 65 | C10 | D4: a small test lowers entry (valley $d\in(0.539,0.699)$) | analytical | CONFIRMED WITH CORRECTION | Needs the full-purchase selection and branch existence |
| 66 | C10 | D5: entry under the optimal test falls in $r$; the reversal dies | analytical | REFUTED as a global statement; CONFIRMED for the pair | Entry jumps up at $r=1.413360$; it still falls from $0.968667$ at $1.2$ to $0.786353$ at $3$ |
| 67 | C10 | D6: trade survives the test | numerical diagnostic | CONFIRMED | $k_{\max}=0.190337$ at $\varphi^*$, $r=3$ |
| 68 | C10 | T1: a public toehold widens the window and moves the ceiling out | analytical | OVERCLAIMED | Fixed truthful bids; the low type wants $b^*=(\ell+sr)/(1+s)$, and $\Delta_T$ falls by $17\%$ at $s=0.1$ (X_C10) |
| 69 | C10 | T2: a purchase at the fair price before the cost is known does not pay | analytical | CONFIRMED WITH CORRECTION | Needs a fixed experiment, fixed bids, and a publicly priced size |
| 70 | C10 | T3: the low-cost challenger buys a hidden unit; entry unchanged | numerical diagnostic | CONFIRMED | Finite profile set and grid only |
| 71 | D | Literature: verified records only | — | CONFIRMED | Fishman (1988) and Bulow, Huang and Klemperer (1999) are abstract-only; every transfer is marked open |
| 72 | C4 | Prop. C4.1: no entry cascade under (NC) | analytical | CONFIRMED | $\psi_2(1/4)D_r=3.961<5$ at $r=3$; X_C4 extends it to pooled prices and mixed orders; weakest step in Section 3.12 |
| 73 | C4 | Prop. C4.3: round-1 trade is informative at every strength; Prop. 2(i) is lost | analytical | CONFIRMED WITH CORRECTION | Proves informed orders, not a general separation of round-1 prices (X_C4) |
| 74 | C4 | Prop. C4.4: the benchmark equilibrium, certified | computer-assisted | CONFIRMED | 64-subgame interval certificate; uniqueness over mixtures only at $r=1.2$ |
| 75 | C4 | Result 8: at $c_H=5$ challenger 2's entry falls with strength; at $5.8$ it rises then falls | numerical diagnostic | CONFIRMED WITH CORRECTION | Six entry values reproduce (X_C4); the broad scans admit challenger mixtures that the main tie rule excludes; existence at $\kappa=-1/2$, $r=3.6$, $c_H=4.4$ stays open |
| 76 | C4 | Result 10: access to prices raises proceeds and surplus | numerical diagnostic | CONFIRMED WITH CORRECTION | Weak inequalities at $c_H=5.8$, $r\in\{1.2,3.6\}$ (X_C4) |

## 3. Findings with derivations

### 3.1 A1 and A2: the three-point model

**Weakest step.** The whole correspondence needs one belief at the unused top flow, shared by market makers and the challenger. A1 states this as a choice (Section 2.3). Both memos adopt the directional completion. X_C9 adds the right argument for it: both receivers condition on the same event $X=2$, so a split belief violates consistency.

**Re-derivation of the cutoff.** A purchase reaches flows $0,1,2$ with probability $1/3$ each. The middle flows keep the prior. The top flow reveals $H$ and pays zero. So the gross gain is $\tfrac13(e_0+e_1)(1-\pi)\Delta_T$ for every $s>0$, and $K=\tfrac23\bar e(1-\pi)\Delta_T$. At $r=3$ with $\bar e=\rho$, $K=1/18$ (`rt_three_point`). The passive-belief deviation adds $\tfrac13\bar e(1-\pi)\Delta_T$, hence the factor $3/2$. This is the paper's (A.12) condition $\rho\Delta_T/2\le k$ at $\pi=1/2$.

**Row 6, by hand.** At $p=1.1>\ell$ and $r_0=1.2$, the low class cannot bid: $w_L=0$, $t_0=1.1(1-1.1/1.2)=0.091667$, $t_H=0.6+1.21/2.4=1.104167$. Full purchases recruit only at the top flow, so $e_H=\rho+(1-\rho)/3=1/2$. Proceeds are $t_0+\pi e_Hw_H=0.091667+0.25\times1.0125=0.344792$. A1's number is right. The paper's "raises proceeds in both economies" fails here.

**Row 5.** See Section 4.5.

### 3.2 B1 and B2: the discrete-Laplace base

**Weakest step.** The fixed-$r$ classification (B2 Result 5) is analytical. The picture across $r$ needs two crossings, $r_I$ and $r_U$, to be single. B2 marks this open. My grid check finds exactly one sign change for each of $K_1(s^*(r))-k$ and $K_\rho(s^*(r))-k$ on 5,701 points in $[1.05,3.9]$, at $1.4050$ to $1.4055$ and at $1.7625$ to $1.7630$ (`rt_dlaplace_base`). The crossings are $r_I=1.405430$ and $r_U=1.762507$. The label is now numerical diagnostic, not open.

**Re-derivation of the coexistence endpoints.** At $\pi=1/2$, $N_\pm(1)=1/2$. So $K_F/\Delta_T=\kappa(2+2\rho)=\gamma(1-\gamma)(1+\rho)=a(1+\rho)/(1+a)^2=0.293755$. Then $r_F=\mathfrak r(k/0.293755)=1.443322$. No trade needs $\rho\Delta_T/2\le k$, so $r_N=\mathfrak r(2k/\rho)=1.747878$. Coexistence needs $K_F>K_0$, that is $(1+\rho)a/(1+a)^2>\rho/2$. With $a>3/5$ the left side exceeds $0.2929$ and the right side is $0.125$. The margin is large.

**Re-derivation of the feedback numbers.** With entry fixed at $\rho$, $K=2\rho a\Delta_T/(1+a)^2=0.078335$ and the net gain is $0.058335$. With entry one after good news, $K=(1+\rho)a\Delta_T/(1+a)^2=0.195836$ and the net gain is $0.175836$. No nearby object gives $0.060$: $\rho\Delta_T/2-k=0.063333$ and $\rho m_1\Delta_T-k=0.042923$.

**Uniqueness against mixtures.** B2's bounds are schedule-free. At $r_0$, $K\le(1-\pi)\Delta_T(r_0)=0.008333<k$ for every $s$ and every schedule. At $r_1$, $K\ge\rho\Lambda\Delta_T(r_1)=0.078335>k$. Every flow is on path, so no belief rule enters. This closes the ledger's "not yet checked" items on mixed purchases and on the no-trade argument over all beliefs. The half-line sums are exact, so the solver has no truncation error; the brute force omits mass $2a^{91}/(1+a)=2.1\times10^{-20}$.

**Labels.** "Analytical" for the Prop. 2 and Prop. 3 analogs is deserved. The decimal endpoints are evaluations of closed forms.

### 3.3 C1 and X_C1: two-sided orders

**Weakest step.** Result 5 maps corners only. X_C1 finds the omitted mixed branches and two false "only" statements. The general claim of Result 4 has no proof beyond the corner algebra. The corner results and Prop. C1.1 are sound.

**A consistency gain.** X_C1's PB-NS branch for $c_H=5$ on $(1.405430,1.443322)$ has entry $0.558559$, $0.576414$, $0.595797$ at $r=1.41,1.42,1.43$. These are B1's $I_G$ numbers and B2's $\hat s$ branch. The buy-only branch survives in the two-sided game because the low class strictly prefers zero there. The three memos agree without any coordination.

**Row 21.** C1 writes that it "confirms" the brief's $+0.060$. Its own edge value is $+0.058335$. The sentence should say that $0.060$ is a two-decimal rounding.

### 3.4 The exact matches with the paper (rows 14 to 16)

See Section 4.2.

### 3.5 C2 and X_C2: two rounds

**Weakest step.** Two rounds carry two units of informed orders. The two-round bound $M_2=1/(1+a^2)$ equals the paper's one-round two-sided bound $M$. C2 says so itself: "this ceiling comparison does not identify a benefit unique to dynamics." The coexistence at $(1.7,0.02)$ and the benchmark path at $c_H=6$ are therefore partly a capacity result. A fixed cumulative purchase limit would separate the two effects; C2 lists it as open.

**Spot check.** At $a=3/5$ and $r=3$: $u=5/8$, $v=3/8$, $M_2=25/34$, $D=1/6$. Then $C_-=D(u/2+vM_2)=(1/6)(5/16+75/272)=(1/6)(160/272)=5/51$, as C2 states.

**The thin margin.** At $r=3.6$, $6-B_{3.6}(M_2)=0.00269$. The coarse value $a=3/5$ reverses the sign. C2's certificate uses the alternating series, which is the right method. The result is fragile in $b$, not wrong.

### 3.6 C3 and X_C3: the option to delay

**Weakest step.** The first preparation decision must stay private until round 2. If the market sees a wait, the high-cost type is identified. In the three-point model the round-2 residual after an observed wait is then zero and the construction fails. C3 does not state the privacy assumption; X_C3 adds it. The discrete-Laplace results change their numbers under public observation but keep their form.

**The $\delta=0.8$ error.** The late ceiling solves $0.8B_r(M_2)=5$. The closed-form root is $2.910409$; the residual at the reported value $8$ is $-1.489972$ (`rt_refuted`). The bisection bracket $[3,8]$ contained no root. The $\delta=0.9$ and $0.95$ roots are right ($4.807$ and $5.605891$).

**Delay needs a high discount factor.** At $r=3$, waiting beats immediate entry after good news only for $\delta>\delta^*=0.898963$. At $\delta=0.9$ the margin is $0.003$. The entry fall $0.625\to0.448747$ therefore holds only for discount factors near one.

### 3.7 C5 and X_C5: a stake

**Weakest step.** The welfare reading. The ledger at $r=3$, $c_H=6$ (exact fractions, `rt_refuted`):

| Profile | $\mathsf E$ | Proceeds $T$ | Challenger $C$ | Surplus $W$ |
|---|---|---|---|---|
| hidden price | $1/4$ | $59/96=0.614583$ | $103/96=1.072917$ | $2.542083$ |
| S | $3/8$ | $145/192=0.755208$ | $265/192=1.380208$ | $2.859792$ |
| M at $\Omega_2$ | $241/564$ | $10547/13536=0.779181$ | $103/96=1.072917$ | $2.552674$ |

From S to M the challenger loses $59/192=0.307292$ and shareholders gain $649/27072=0.023973$. The ratio is $11/141=7.8\%$. The rest is preparation cost paid in the wrong state. "Rent transfer" is the wrong word; "rent destruction" is right. The surplus loss of $96.67\%$ of the information surplus is confirmed.

**Belief dependence.** The weak-economy bound $\omega_H(r_0)=0.1805$ uses the directional belief at the unused top flow. Under a passive belief the stake term is zero and no trade survives every stake. C5 reports this; its plain summary does not.

### 3.8 C6 and X_C6: costly information

**Weakest step.** The coexistence in $\kappa$ is the B-model feedback in another coordinate. The acquisition probability $\psi$ enters the flow law exactly like a presence probability. So the jump in the research value at $s_E$ is the jump in $K$ at $s^*$ of B2. The result is right and the proof is complete; it is not a new mechanism. The other weak point is the thin margin behind "$c_H=6$ blocks recruitment": $0.0229$ at $b=2$. The result fails for $b<1.9576$.

### 3.9 C7 and X_C7: the incumbent's response

**Weakest step.** Two layers of selection. First, rule IC-P is an extra completion that picks the least-cost bid that deters. Under D1 or the Intuitive Criterion alone, a continuum of larger bids survives at the benchmark posterior, each with more entry. Second, the selection of silence at Case A posteriors. At $c_H=5$ exactly, $E_{1/2}\theta-p=5=c_H$, so a reserve-bid equilibrium exists at $r_0$ with entry $\rho+(1-\rho)p/r_0=0.5625$. That equilibrium reverses the reported rise from $0.25$ to $0.366988$. C7.6 states the selection; the plain summary and Section 4 of C7 present the rise as a result. Hence OVERCLAIMED.

**The silence-pooling refutation, re-derived.** At $(r,\mu)=(3,3/5)$ suppose every type is silent and entry is one. A binding bid $J=2>\ell$ caps the challenger's gross profit by $\mu(h-J)+(1-\mu)(\ell-J)_+=24/5<5$ under every belief about $R$. The bid deters. Type $R=3$ earns $(1-\rho)(R-J)+\rho(1-\mu)(R-J)=0.85$ after the bid and $(1-\mu)(R-\ell)=0.8$ after silence. The gain is $1/20$. Silence pooling is not an equilibrium, whatever the refinement.

**Confirmed numbers.** The cutoff at $(3,M_1)$ solves $D_\mu(c)=5$ at $c^*=0.935901$, and entry is $\rho+\tfrac{1-\rho}2c^*/3=0.366988$ (`rt_refuted`).

### 3.10 C8 and X_C8: the reserve after the price

**Weakest step.** The exclusion reserve $p=h$ exists only because $c_L=0$ and the challenger prepares at indifference. At $p=h$ the low-cost type's gain is exactly zero. Under "stays out at indifference" the seller has a supremum and no maximizer (X_C8 §4.3). Any $c_L>0$ moves the reserve to $h-c_L/\mu$.

**Reproduction.** My candidate list gives $p^*=h$ at both $r\in\{1.2,3\}$ and both posteriors for $c_L=0$, proceeds $1.25$, and $K(1)=1.175019$. For $c_L=0.1$: $p^*=9.735128$ at $m_1$ and $9.839347$ at $M_1$, entry $\rho$, proceeds $1.225$. For $c_L=1$ at $r=3$: $p^*(m_1)=1.582464$, $p^*(M_1)=1.674539$ with entry one at $M_1$, expected entry $0.625$, proceeds $1.181022$. At $r=1.2$ with $c_L=1$: entry $\rho$, proceeds $1$, full purchases ($K(1)=0.925019$). At $r=3.6$ the exact optimum at $M_1$ is $p=1$ with proceeds $1.584420$; C8's grid value $0.995$ misses the kink.

**The sunk-preparation refutation.** At $(3.6,M_1)$ the main timing sets $p=1$ and induces preparation with probability one. If that decision is sunk and unobserved, the seller's objective at the reserve node holds entry at one. A deviation to $p=h$ then earns $\mu h=6.224593>1.584420$. So the two timings are different games. C8's "every outcome carries over" is false.

### 3.11 C9, C10 and X checks

**C9.** The upward branch A is analytical on $I$, and the count of three is proved. The weak step is scope: the window of branch A is $(1.574345,1.588760]$, width $0.0144$; above it full purchases give flat entry $11/20$. The branch is a mixture at zero profit, not a strictly optimal order size. The top flow still reveals $H$, so no ceiling returns. "Recovered" in C9 Section 4 is too strong.

**D.** The weakest step is access: eleven of its sources are abstract-only, so no transfer to C.1 to C.10 is more than open. The memo says so.

**C10.** The optimal-test numbers hold. Three steps are weak. First, the concavification runs over a value function that is not single-valued (coexistence) and not everywhere defined (gaps); the support-line proof repairs this only at $\varphi^*$. Second, the global monotonicity of entry in $r$ fails at the switch $r=1.413360$. Third, the toehold results hold bids truthful, which is a partial-equilibrium device; the low type's optimal bid $b^*=(\ell+sr)/(1+s)$ cuts $\Delta_T$ by $17\%$ at $s=0.1$. The headline "the reversal does not survive costless disclosure" stands for the benchmark pair.

### 3.12 C4 and X_C4: sequential challengers

`X_C4_check.md` was complete, with its plain summary, when this memo reached C4. Its verdicts are used in rows 72 to 76. The red team adds the following.

**Weakest step.** Proposition C4.1 rests on the auction tie at $h$. With point masses, two high-class challengers tie, the payment is $h$, and the second entrant's rent is exactly zero. Condition (NC) then bounds challenger 2's gain by $D_r\Pr(LH\mid\cdot)\le\psi_2(\pi_{LH})D_r$. At $r=3$: $\psi_2(1/4)=1/(1+3a^2)=0.475367$ and $D_r=8.333333$, so the bound is $3.961<5$, as C4 states. Under Reading N with a value spread inside the high class, the second entrant keeps $\mathbb E(v_2-v_1)_+$, about $\varepsilon_V/3$ at the paper's half-width. C4 lists this as open. The no-cascade result is therefore a property of the degenerate class distribution; the brief's general reading needs the spread term.

**Loss of Prop. 2(i).** Type $HH$ is worth $h$ to the target whenever both challengers prepare, which the low-cost types alone produce with probability $\rho^2$. So the round-1 purchase gain is of order $\rho^2D_r$, not $\Delta_T(r_0)$. At $r=1.2$ it is $0.362>k$. The weak economy trades. This is the right reading: the mechanism of the paper needs a dead market at the weak incumbent, and a second potential challenger revives it.

**Editorial.** An earlier version of C4 left an unfilled placeholder in Result 9. The final version replaces it with a paragraph on the empty search at $\kappa=-1/2$, $r=3.6$, $c_H=4.4$, with existence marked open. X_C4 confirms that label. The ledger also records that one diagnostic ran outside the slot wrapper.

## 4. Reconciliation points 1 to 6

### 4.1 C7's interior equilibria at $r\in[1.41,1.44]$ against B1 and B2

**Confirmed: no contradiction.** C7's "interior $\beta$ in Case B" on $[1.43,1.44]$ is the branch that B1 calls $I_G$ and B2 calls $\hat s$. It lives on $(r_I,r_F)=(1.405430,1.443322)$, has entry $(\rho,1)$ by news, and coexists with no trade, because $r<r_N$. It does not coexist with full purchases, which first exist at $r_F$. X_C7's table agrees point by point: at $r=1.41$ the purchase rate is $0.276594$, which gives entry $0.558559$. The coordinator's reading "just below B1's coexistence interval" is right; the two intervals describe different branches.

**The complete equilibrium set of the base buy-only discrete-Laplace model** at $c_H=5$, $b=2$, $k=0.02$ (`rt_dlaplace_base`; boundaries $r_I=1.405430$, $r_F=1.443322$, $r_N=1.747878$, $r_U=1.762507$, $r_C=3.986097$):

| Strengths | (IM, C1): investor may mix, challenger prepares | (IM, CM): both may mix | (I0, C1) or (I0, CM): investor chooses zero |
|---|---|---|---|
| $(1,r_I)$ | N | N | N |
| $[r_I,r_F)$ | N; $\hat s$ (entry from $0.5508$ up to $0.625$) | N; $\hat s$; $s^*$ (entry falls from $0.548$ to $0.487$) | N |
| $[r_F,r_N]$ | N; F ($0.625$) | N; F; $s^*$ (entry from $0.487$ down to $0.256$) | N; F (F only for $r>r_F$) |
| $(r_N,r_U)$ | $\tilde s$ (entry $\rho$); F | $\tilde s$; $s^*$; F | F |
| $[r_U,r_C]$ | F ($0.625$) | F | F |
| $(r_C,h)$ | F ($\rho$) | F | F |

At $r_C$ itself, (C1) keeps entry $0.625$ and (CM) admits every value in $[0.25,0.625]$. The $\hat s$ branch needs (IM) only; it survives the paper's challenger rule because $\mu_+(\hat s)>\tau$ strictly. The $s^*$ branch needs (CM). The paper's three strengths $1.55,1.60,1.65$ lie in $[r_F,r_N]$: two outcomes under (C1), three under (CM).

### 4.2 C1 and X_C1: the exact matches with the paper

**Confirmed, exact, for the stated reason.** The discrete law is $f(z)\propto e^{-|z|/b}$ on the integers. For integer orders $q,q'$, Bayes' rule uses only $f(x-q)/f(x-q')=e^{(|x-q'|-|x-q|)/b}$, which equals the Laplace density ratio at the same points. Under full orders $(1,-1)$ the ratio is $e^{2/b}$ on $x\ge1$ and $e^{-2/b}$ on $x\le-1$. So the top posterior is the paper's $M=1/(1+e^{-2/b})=0.731059$, attained with positive probability. The ceiling solves the paper's own (A.11), $B_r(M)=c_H$, hence $r_C=3.592658519$ at $c_H=6$ (`rt_two_sided`). The no-trade boundary does not depend on the noise law: under no trade every flow is on path with posterior $1/2$, and a unit deviation earns $\rho\Delta_T/2-k$, the paper's (A.12). Hence $r_N=\mathfrak r(2k/\rho)=1.747877538$. The bound $\mathfrak r(k)=1.220997512$ matches for the same reason.

**Recovered exactly:** the bounds $m,M$ and the full-order posterior at integers; the window ends $4.804167$ and $6.217155$ (closed on the right here); $r_N$, $r_C$, $\mathfrak r(k)$; the residual bounds of eq. (11); entry $0.25$ and ownership $0.125$ at $r_0$; the return to $0.25$ at $r_2=3.6$ for $c_H=6$; the hidden-price control.

**Not recovered:**

- $r_U$: $2.124148$ against $2.837417$; unit orders need no factor $1-1/b$;
- the (A3) upper bound: $0.044824$ against $0.022412$;
- eq. (12)'s $x^*,\alpha_H,\alpha_L$: three flow classes replace the continuum;
- entry and ownership at $r_1$: $0.569293$ and $0.358422$ against $0.522757$ and $0.324192$, because the mass with $\mu\ge\tau$ is one atom, $\Pr(X\ge1)=0.425725$;
- the limit (A.14) as $r\uparrow r_C$: $0.569293$, flat, against $0.506477$;
- the fixed-experiment control: flat $0.569293$ against $0.562178\to0.522757$;
- the Prop. 3 values $(1,-v_j)$ and $\mathsf E_j$: only NT and T exist at $1.55$ to $1.65$, and T entry is flat.

My script reproduces the paper's $0.522757$ and $0.324192$ from eq. (12), so the comparison uses the same auction objects.

### 4.3 C8: "the seller sets $p=h$ and kills entry"

**Honest conclusion, in three parts.**

1. At $c_L=0$ the claim is right and certified (X_C8). It rests on two things: the low-cost type's gain at $p=h$ is exactly zero, and an indifferent challenger prepares. Under the other tie rule the seller has no best response.
2. Hold-up survives small positive costs. For $0<c_L\le0.1$ the seller sets $p=h-c_L/\mu$, entry stays $\rho$, and proceeds are $1.25-c_L/4$ (`rt_reserve_cL`). So the entry response to the price dies for small $c_L$, not only at zero.
3. At the paper's $c_L=1$ with $c_H=5$, the seller accommodates after good news at $r=3$: $p^*(M_1)=\bar p=1.674539$, entry $0.625$, proceeds $1.181022$. Entry rises from $0.25$ at $r=1.2$ to $0.625$ at $r=3$. But purchases are full at both strengths, so Prop. 2(i) still fails. The restored entry comparison is not the paper's mechanism. At the paper's $c_H=6$ no reserve can recruit at $r=3$ under buy-only posteriors.

The separate claim that an unobservable preparation decision before the reserve gives the same game is refuted (row 55).

### 4.4 The refuted claims

| Claim | Source | Verdict | Evidence |
|---|---|---|---|
| Feedback $+0.060$ without entry after good news | brief §0 | REFUTED at three decimals | $2\rho a\Delta_T(3)/(1+a)^2-k=0.058335$; no nearby object gives $0.060$ |
| Manipulation moves the challenger's rent to shareholders | C5 §3.11 | REFUTED | $\Delta T=+0.023973$, $\Delta C=-0.307292$, ratio $11/141$; surplus loss $96.67\%$ stands |
| Silence pooling survives IC and D1 throughout Case C | C7 (C7.3e) | REFUTED | binding bid $J=2$ at $(3,3/5)$ deters under every belief; type $3$ gains $1/20$ |
| Unobservable preparation before the reserve gives the same game | C8 §3.6 | REFUTED | sunk preparation; deviation to $p=h$ earns $6.224593>1.584420$ at $(3.6,M_1)$ |
| C3 corrections: public decisions; late ceiling at $\delta=0.8$ | C3 | REFUTED (the $8$); scope correction (privacy) | root $2.910409$; residual at $8$ is $-1.49$; observed waits identify the high-cost type |

All five refutations stand. Two further general statements are refuted in the verdict table: C7's claim that every larger bid through $\ell$ survives (row 49) and C10's claim that entry under the optimal test falls at every strength (row 66). The C3 privacy point is a scope correction. C3 is right in its own game, which prices on flows alone and therefore assumes private decisions.

### 4.5 A.10 and $c_L=0$

**Confirmed, with one refinement.** Proposition A.10 concerns price pools "when preparation can vanish", that is, when $c_L>B_r(\mu)$ at some attained posterior. With $c_L=0$ and $p<\ell$, $B_r(\mu)\ge g_L>0$ at every posterior and every noise law (`rt_three_point`: $g_L=5/16,1/8,5/48$ at $r=6/5,3,18/5$). Entry is at least $\rho$ everywhere, the price is strictly increasing in the posterior, and no pool of distinct posteriors exists. This is $c_L$, not discreteness. The right label is "not applicable", because the hypothesis of A.10 fails.

The refinement: at the paper's own $c_L=1$ discreteness does matter. Pools need an attained posterior with $B_r(\mu)<1$, that is $\mu<0.105$ at $r=3$. The three-point model attains posterior $0$ at flow $-1$ under full purchases, so it has pools at $c_L=1$ (the prior work's family). The Laplace model keeps $\mu\ge m=0.269$, and the discrete-Laplace model keeps $\mu\ge m_1=0.378$, so neither has a pool within the paper's (A1). Discreteness with bounded support enlarges the pooling region; $c_L=0$ removes it.

### 4.6 Cross-memo consistency

The shared numbers agree in every memo that states them: entry $0.625$ (17 memos), ownership $0.358422$ (14), ceiling $3.986097$ (6), the window ends $4.804167$ and $5.312161$ (4 and 6), $r_N=1.747878$ (13 across both spellings), $r_F=1.443322$ (6), the feedback pair $0.175836$ and $0.058335$ (9 and 11). No numeric contradiction was found. These non-numeric points need one correction each:

1. **Welfare convention.** B1 subtracts the trading cost ($\mathcal W=2.690394$ at $r=3$ with access); B2 and C7 follow the paper and subtract preparation costs only ($2.700394$). C5 and X_C5 use B1's convention. The gains agree ($0.148310$). State the convention beside every level.
2. **Symbol clash.** B1, B2, C1, C5 and A1 use $r_N=1.747878$ for the no-trade boundary; C7 uses $r_N=2.934693$ for its Condition N threshold. Rename the latter.
3. **C1** "confirms" $+0.060$ while its own value is $+0.058335$.
4. **C7** says entry drops to $\rho$ at $r_C$; the selected value is $0.297038$.
5. **C3** reports closed plateau endpoints and the ceiling $8$ at $\delta=0.8$; both are wrong.
6. **C8** reports grid proceeds $1.306395$ at $r=3.6$; the exact optimum is $1.307088$.
7. **C4** still carries the header "awaiting the phase-2 check"; the check is done.
8. **Entry $11/24$** appears in C2 (equal noise, two rounds) and in C3 (three-point delay). This is not a clash: both count a revealing top flow in either of two rounds, so the event is the same.

## 5. Plain summary

The 25 memos hold up. No headline number is wrong. Every shared constant agrees across memos. The base discrete-Laplace model does what the brief claims: entry $0.25\to0.625\to0.25$, a ceiling at $3.986$, and coexistence on $[1.443,1.748]$. C7's interior equilibria near $1.41$ to $1.44$ are B1's and B2's branch; they coexist with no trade, not with full purchases.

The five claims named for review fall (one number in the brief, four claims in the memos). The feedback number is $0.058$, not $0.060$. A stake does not move rent to shareholders; it destroys it. Silence by every incumbent is not an equilibrium when a bid can deter. A seller who moves after sunk preparation plays a different game. The late ceiling at discount $0.8$ is $2.91$, not $8$. Two further general statements fall: C7's bid continuum and C10's monotone entry.

Six claims are overclaimed. C7's weakened Prop. 2 depends on a selection at a knife-edge. C9's "recovered order" holds on one branch, $0.014$ wide. C10's label for the optimal test and its toehold results rest on floats and on fixed bids. C1's "buyer inframarginal" has no general proof. C8's interval claim had no certificate until its check.

Two-sided discrete-Laplace orders reproduce the paper's $r_C$ and $r_N$ exactly, because the discrete law is the Laplace density on the integers and the no-trade payoff is noise-free. They do not reproduce $r_U$, the entry levels, or the Proposition 3 values. The reserve result kills entry only with a zero or small low cost. Proposition A.10 is not applicable at $c_L=0$ under any noise law.
