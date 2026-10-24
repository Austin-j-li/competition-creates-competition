# Synthesis: what discrete trade keeps, what the modifications add, and what to put in the paper

Memo to the author, 21 October 2026. It rests on the 25 workstream memos in this folder and on the red-team pass `memos/RED_TEAM.md` (check scripts in `scripts/RED_TEAM/`). Every number below comes from those files. Paper references are to the pinned commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba` of `overleaf/paper/main.tex`.

Status labels: **analytical**, **computer-assisted**, **numerical diagnostic**, **conjecture**, **open**. Tie rules: the investor chooses zero at indifference (I0) or may mix (IM); the challenger prepares at indifference (C1, the paper's rule) or may mix (CM).

The two discrete bases are the three-point model (noise $\{-1,0,1\}$ with equal weights, unit purchases only) and the discrete-Laplace model (noise is the difference of two geometric counts, $\Pr(Z=z)\propto a^{|z|}$ with $a=e^{-1/b}$). Both use Reading N with point masses, $c_L=0$, and the paper's auction. The buy-only discrete-Laplace benchmark uses $c_H=5$ and strengths $(1.2,3,4.2)$; the two-sided one keeps the paper's $c_H=6$ and $(1.2,3,3.6)$.

## 1. Verdicts on the key claims

| # | Claim | Source | Status after the red team | Verdict |
|---|---|---|---|---|
| 1 | Discrete-Laplace, buy-only: Prop. 2 analog; entry $0.25\to0.625\to0.25$ at $(1.2,3,4.2)$; ownership $0.125\to0.358422\to0.125$ | B1, B2 | analytical | CONFIRMED |
| 2 | Its $c_H$ window is $(4.804167,5.312161]$ and its ceiling $r_C=3.986097$; the paper's $c_H=6$ recruits nobody at any $r>1$ | B1, B2, C6 | analytical | CONFIRMED; $c_H\in(5.121880,5.312161]$ keeps the paper's strengths |
| 3 | Feedback: a purchase at $r_1$ nets $+0.175836$ with entry after good news and $+0.058335$ without | B1, B2 | analytical | CONFIRMED; the brief's $+0.060$ is REFUTED |
| 4 | Prop. 3 analog: no trade and full purchases coexist on $[1.443322,1.747878]$; a third outcome under (CM); entry strictly ordered within each strength | B2 | analytical | CONFIRMED |
| 5 | Entry rises with strength on an informative branch that coexists with no trade | B1, B2, X_C1 | analytical (local) | CONFIRMED WITH CORRECTION: only on $(1.405430,1.443322)$, not at $1.55$ to $1.65$ |
| 6 | Two-sided unit orders: Prop. 2 at the paper's own $c_H=6$ and strengths; entry $0.569293$; $r_C=3.592658519$ and $r_N=1.747877538$ exact | C1, X_C1 | analytical | CONFIRMED |
| 7 | Two-sided: no trade and full trade coexist on $[1.515898,1.747878]$; the buyer is the strong side | C1, X_C1 | analytical (corners); numerical diagnostic (branches) | CONFIRMED; "buyer inframarginal" in general is OVERCLAIMED |
| 8 | Three-point model: one cutoff $\tfrac23\rho(1-\pi)\Delta_T$; needs the directional completion; equal noise is a knife-edge; return only above $7.969$ | A1, A2 | analytical, computer-assisted | CONFIRMED |
| 9 | Two rounds: coexistence at the paper's $c_H=6$, $k=0.02$ at $r=1.7$; benchmark path $0.25\to0.448747\to0.25$ at $(1.2,3,3.6)$ | C2, X_C2 | analytical; computer-assisted | CONFIRMED WITH CORRECTION: two units of capacity; the margin at $3.6$ is $0.0027$ |
| 10 | Costly information: no research and full research coexist for $\kappa\in[0.031667,0.087918]$ at $r=3$ | C6, X_C6 | analytical | CONFIRMED; (CM) adds a third equilibrium |
| 11 | Delay: discrete-Laplace entry falls to $0.448747$ at $r=3$ for $\delta>0.899$; the ceiling moves to $5.606$; three-point entry rises to $11/24$ | C3, X_C3 | analytical | CONFIRMED WITH CORRECTION: private decisions; the $\delta=0.8$ ceiling is $2.910$, not $8$ |
| 12 | Stake: Prop. 2 analog iff $\omega<0.1805$ (three-point) or $0.1878$ (discrete Laplace); class L buys from $2.027$; no equilibrium above $2.599$ under the paper's rules | C5, X_C5 | analytical | CONFIRMED; "rent transfer" REFUTED (shareholders get $11/141$ of the lost rent) |
| 13 | Incumbent jump bid: entry $0.625\to0.366988$; a pure transfer to the incumbent; the investor earns the no-feedback value | C7, X_C7 | analytical under rule IC-P and a selection | CONFIRMED; "Prop. 2 survives" OVERCLAIMED (a weak-economy equilibrium with entry $0.5625$ exists at $c_H=5$); "silence pooling" REFUTED |
| 14 | Reserve after the price: the seller sets $p=h$, entry stays $\rho$, trade is full at both strengths | C8, X_C8 | computer-assisted | CONFIRMED at $c_L\le0.1$; at $c_L=1$ entry rises $0.25\to0.625$ but trade is full at both strengths; "unobservable equivalence" REFUTED |
| 15 | Unequal three-point noise with mixtures: existence; exactly three outcomes on $[1.575,1.585]$; an upward entry branch | C9, X_C9 | analytical | CONFIRMED; "ordered equilibria recovered" OVERCLAIMED (one branch, width $0.0144$, a mixture at indifference) |
| 16 | Target disclosure: the optimal test raises entry to $0.786$ and ownership to $0.5$; the reversal does not survive | C10, X_C10 | analytical conditional on (C); numerical diagnostic on the grid | CONFIRMED WITH CORRECTION: entry is not monotone in $r$ (a jump at $1.413$) |
| 17 | A public toehold widens the window and moves the ceiling out | C10, X_C10 | numerical diagnostic in a fixed-bid partial model | OVERCLAIMED: the low type's optimal bid cuts $\Delta_T$ by $17\%$ at $s=0.1$ |
| 18 | Sequential challengers: no entry cascade under (NC); round-1 trade is informative at every strength, so Prop. 2(i) is lost; the benchmark equilibrium is certified | C4, X_C4 | analytical; computer-assisted | CONFIRMED WITH CORRECTION: weak welfare gains; the scans change the tie rule; the no-cascade bound uses the point-mass tie |
| 19 | Prop. A.10 is not applicable at $c_L=0$ under every noise law | A1 | analytical | CONFIRMED WITH CORRECTION ("dies" should read "not applicable"; at $c_L=1$ bounded noise does create pools) |
| 20 | No verified source supplies a theorem for these games | D | — | CONFIRMED; every transfer is open |

No shared number disagrees across memos. The welfare level $\mathcal W$ carries two conventions ($2.700394$ with preparation costs only, $2.690394$ with the trading cost too); the gains agree.

## 2. What discreteness alone does

The table compares the paper's results in the two discrete bases. The three-point column uses $c_H=6$; the buy-only discrete-Laplace column uses $c_H=5$; the two-sided column uses $c_H=6$. "Survives" means the statement holds with the discrete objects in place of the continuous ones.

| Paper result | Three-point, equal noise, buy-only | Discrete Laplace, buy-only | Discrete Laplace, two-sided | Status |
|---|---|---|---|---|
| Prop. 1 (two returns) | survives | survives | survives | analytical |
| Prop. 2(i), weak incumbent | survives; needs the directional completion; passive beliefs fail on $k\in(K,\tfrac32K)$ | survives, belief-free: $K\le(1-\pi)\Delta_T(r_0)<k$ | survives, belief-free: $\Delta_T(r_0)<k$ | analytical |
| Prop. 2(ii), strong incumbent | survives, weaker: entry $0.375$ (paper $0.523$) | survives: entry $0.625$; dies at the paper's $c_H=6$ | survives at $c_H=6$: entry $0.569293$ | analytical |
| Prop. 2(iii), return to $\rho$ | changes: only above $r_C(1)=7.969$ (fails at $3.6$) | survives: $r_C=3.986$ ($r_2=4.2$) | survives exactly: $r_C=3.592659$ | analytical |
| Prop. 3, coexistence | dies (only at the knife-edge $\tau=\pi$ under (CM)) | survives on $[1.443,1.748]$, with a third outcome under (CM) | survives on $[1.516,1.748]$ | analytical |
| Prop. 3, upward entry across strengths | dies | only on $\hat s$ below $r_F$ | only on two short branches; flat T entry at $1.55$ to $1.65$ | analytical (local) |
| Section 4.3, $(1,-v)$ asymmetry | not applicable | not applicable | direction survives (buyer strong); full buys with partial sells only on $(1.516,1.534)$ | analytical; numerical diagnostic |
| Prop. A.1, posterior bounds $[m,M]$ | dies: $0$ and $1$ are attained | recovered with $[m_1,M_1]=[0.378,0.622]$ | recovered exactly | analytical |
| Prop. A.2, price sufficiency | survives, unconditional at $c_L=0$ | survives | survives | analytical |
| Prop. A.3, fixed experiment | survives weakly: a step function, flat at the benchmark | survives weakly: one jump at $r_C$ | survives weakly: flat | analytical |
| Prop. A.4, thresholds | one cutoff $1.973$; passive $1.748$; $r_C(1)=7.969$ | $r_N=1.747878$ exact; $\mathfrak r(2k)=1.326$; $\mathfrak r(k/\rho\Lambda)=1.778$; $r_C=3.986$ | $r_N$, $\mathfrak r(k)$, $r_C$ exact; $r_U$ becomes $2.124$ | analytical |
| Prop. A.5, noise class | not applicable; any unequal law breaks the single cutoff | class form with a bounded one-step ratio; closed forms need geometric tails | not studied | analytical; open |
| Prop. A.6, atomless costs | survives; gradual return | local persistence only | not studied | analytical; open |
| Prop. A.7, private signals | survives: entry $0.85\to0.865$ | open | not studied | analytical; open |
| Prop. A.8, payment rule | survives; the trading game is solvable | survives | survives | analytical |
| Prop. A.9, access to prices | survives: $\Delta\mathcal R_T=9/64$, $\Delta\mathcal W=61/192$ | survives: $0.327490$, $0.148310$ | not computed | analytical; open |
| Prop. A.10, price pools | not applicable at $c_L=0$ (pools return at $c_L=1$) | not applicable | not applicable | analytical |
| Section 5.1, other noise laws | not applicable | perturbations keep coexistence and $r_N$ | not studied | analytical; numerical diagnostic |
| Section 5.2, value gap | survives, easier | survives | not studied | analytical |
| Section 5.3 | survives (A1) | open | not studied | analytical; open |
| Section 6.1, welfare | survives, smaller effects | survives | open | analytical; open |
| Section 6.2, bargaining | survives | survives | not studied | analytical |
| Section 6.3, reserve | changes: proceeds fall at $r_0$ ($0.3927\to0.3448$) | a contingent reserve kills the entry response (C8) | not studied | analytical; computer-assisted |

**In words.** Bounded noise support is the loss, not discreteness. With three-point noise the top flow reveals the class, so the flow that recruits pays the investor nothing. The consequences are no feedback, no coexistence, a ceiling at $g_H(r)=c_H$, and an off-path flow that needs a belief rule. Geometric-count noise has full support and a bounded one-step likelihood ratio. Every flow is on path, posteriors stay inside $(0,1)$, and the recruiting flow keeps a positive residual. Then Prop. 2 and Prop. 3 return with shorter proofs than the paper's, because the investor's choice is one comparison, $K-k$, with closed-form bounds. The buy-only version pays a price: the paper's $c_H=6$ recruits nobody, so the benchmark must move to $c_H=5$ and $r_2=4.2$. Two-sided unit orders remove that price. They reproduce the paper's bounds $m,M$, its ceiling and its no-trade boundary exactly, because the discrete law is the Laplace density at the integers and the no-trade payoff is noise-free. What no discrete version reproduces is the paper's order pattern $(1,-v_j)$ and the upward entry order at $1.55,1.60,1.65$; entry moves in steps, and the fixed-experiment control is flat.

## 3. Ranked list of the modifications

Each modification is judged against the discrete-Laplace base. The four criteria are:

- (a) which paper results it recovers, or which new result it creates;
- (b) the status label after the checks;
- (c) robustness to tie rules, off-path beliefs, $c_L$ and parameters;
- (d) simplicity.

| Rank | Modification | Mechanism (one line) | Key number | (a) Recovers or creates | (b) Status | (c) Robustness | (d) Simplicity | Main caveat |
|---|---|---|---|---|---|---|---|---|
| 1 | Two-sided unit orders with geometric-count noise (C1) | The sale after bad news restores the paper's two-unit likelihood span, so the posterior bounds are the paper's $m,M$ | entry $0.569293$; $r_C=3.592659$; $r_N=1.747878$ | Prop. 2(i) to (iii) at the paper's own $c_H=6$ and strengths; coexistence on $[1.516,1.748]$; the buyer-strong direction | analytical (corners); numerical diagnostic (branches) | corner results hold under both tie rules; no off-path flow; the floor holds at $c_L=1$ ($B_3(m)=2.37$) | one change: the order menu | no $(1,-v)$ at $1.55$ to $1.65$; T entry is flat; the full mixed correspondence is open |
| 2 | Two trading rounds before entry, fresh investors (C2) | A second binary signal widens the belief range to $[m_2,M_2]=[0.269,0.731]$ | coexistence at $(1.7,0.02)$, $c_H=6$; entry $0.448747$ at $r=3$ | Prop. 2 at the paper's $c_H=6$ and $(1.2,3,3.6)$; coexistence at the original costs; a price path that falls without news | analytical; computer-assisted at the benchmark | no belief rule; both designs; $c_L=1$ coincides on path | simple | two units of capacity do part of the work ($M_2$ equals the paper's $M$); the ceiling margin at $3.6$ is $0.0027$ |
| 3 | Costly information acquisition (C6) | Recruited entry raises the private value of information, so research and entry are complements | coexistence for $\kappa\in[0.0317,0.0879]$ at $r=3$; entry $0.25\to0.625\to0.25$ at $\kappa=0.02$ | creates coexistence at the strong benchmark; "competition creates research" (local) | analytical | (CM) adds a third equilibrium; the $c_H=6$ barrier needs $b>1.9576$; no belief rule | simple | the feedback is the base model's in another coordinate; research can lower welfare |
| 4 | Unequal three-point noise with mixtures at indifference (C9) | A non-uniform law makes a camouflage flow informative, so the purchase payoff moves with the purchase rate | exactly three outcomes on $[1.575,1.585]$; entry $0.5269<0.5352<0.5436$ | coexistence and an upward entry branch in the three-point base; existence for every parameter vector | analytical | needs the directional completion; branch T needs (CM); window width $0.0144$ | moderate | a mixture at zero profit, not an optimal order size; the top flow still reveals $H$ |
| 5 | An option to delay preparation (C3) | A second price screens entry; with discrete-Laplace noise two good prices are needed | discrete Laplace: entry $0.625\to0.449$, ceiling $3.986\to5.606$ at $\delta=0.95$; three-point: entry $3/8\to11/24$ | creates coexistence in a cost window; a non-monotone timing result; moves the ceiling out | analytical after the checks | needs private preparation decisions; needs $\delta>0.899$; closed endpoints wrong | moderate | the sign of the entry effect flips across bases; the coexistence example is off the benchmark $k$ |
| 6 | An informed investor with a stake (C5) | A holder gains from entry in both states, so class L may buy to recruit | Prop. 2 survives for $\omega<0.1805$; manipulation from $2.027$; no equilibrium above $2.599$ under the paper's rules | exact robustness bounds for Prop. 2; new mixed branches; coexistence in the three-point base | analytical; computer-assisted | the weak-economy bound depends on the directional belief; (CM) repairs the nonexistence | moderate | manipulation destroys $96.7\%$ of the information surplus; "rent transfer" is wrong |
| 7 | The incumbent bids after the price (C7) | After good news strong types bid just enough to deter the high-cost challenger | entry $0.625\to0.367$; transfer $0.172$ to the incumbent | the mechanism survives weakened; a pure-transfer result; new mixed branches | analytical under rule IC-P and a selection; numerical diagnostic for the branches | two selections; the boundary tie differs from the paper's; at $c_H=5$ a second weak-economy equilibrium reverses the rise | complex | belief completion is an extra assumption; silence pooling claim was wrong |
| 8 | A public toehold for the challenger (C10) | The stake adds $s(w_L+\Delta_T\mu)$ to the entry gain | window width $0.508\to0.602$ at $s=0.2$; $r_C(0.1)=4.395$ | widens the Prop. 2 window; moves the ceiling out | numerical diagnostic, fixed bids | bids held truthful; $\Delta_T$ falls $17\%$ at $s=0.1$ under optimal bids | simple | partial equilibrium only |

**Modifications that failed to recover results, with the reason.**

| Modification | What happened | Reason | Status |
|---|---|---|---|
| Reserve set after the price (C8) | At the benchmark the seller sets $p=h$; entry stays $\rho$; trade is full at both strengths; Prop. 2 fails | hold-up: exclusion is worth $\rho\mu h$, more than accommodation; rests on $c_L\le0.1$ and the prepare-at-indifference rule; at $c_L=1$ the entry rise returns but not Prop. 2(i) | computer-assisted |
| Target disclosure (C10) | The optimal test gives entry $0.969$ at $r_0$ and $0.786$ at $r_1$; the reversal dies | a costless certifier beats the market; the result is a scope limit on the paper's claim | analytical conditional on (C); numerical diagnostic |
| Sequential challengers (C4) | No cascade; Prop. 2(i) is lost; challenger 2's entry falls with strength at $c_H=5$ | a second potential challenger makes state $HH$ worth $h$, so trade pays at every strength; the auction tie at $h$ zeroes the second entrant's rent | analytical; computer-assisted |
| Delay in the three-point base (C3) | Entry rises to $11/24$; no coexistence | round 2 is the bottleneck; the recruiting flow still pays zero | analytical |
| Repetition with equal noise (C2, Design S) | No graded beliefs; no open coexistence interval | each round reveals or stays at the prior | analytical |
| Private lockup (C7, Model L) | Never accepted | the second-price rule already pays the target the incumbent's value | analytical |

The change of base itself, from three-point to discrete-Laplace noise, is the largest single gain in this study. The prior synthesis (`audit/alex_meeting_2026_10_21/memos/SYNTHESIS.md`, B.8 rank 5) recommended a three-point companion. That companion is now dominated: it needs an off-path completion, returns only above $7.97$, and carries no coexistence.

## 4. Recommendation

The Laplace case stays the benchmark. Nothing here changes the paper's main text. Three additions are worth the author's time, and the rest should stay out.

**Put in the paper.**

1. **One remark after Proposition 2 or in Section 5.1, five to eight lines.** State that a discrete companion exists: unit orders in $\{-1,0,1\}$, noise equal to the difference of two independent geometric counts of unit orders, scale $a=e^{-1/b}$. Under the paper's own benchmark ($c_H=6$, $(1.2,3,3.6)$) it gives the same posterior bounds $m,M$, the same ceiling $r_C=3.592659$ and the same no-trade boundary $r_N=1.747878$, with entry $0.569293$ at $r_1$. The proof needs no derivative bound: the investor's choice is one comparison. Say what does not transfer: the uniqueness bound $r_U$, the entry levels, and the $(1,-v)$ pattern. Place the geometric-count story for the noise beside the noise justification of Section 2.3.
2. **An online-appendix section, two to three pages.** Proposition C1.1 with conditions (D1) to (D3) and its proof; Result 3 of C1 (coexistence on $[1.515898,1.747878]$) with the closed-form endpoints; the exact-match statement with its two reasons; both tie rules; the fact that no flow is off path. Add the buy-only variant as one paragraph: its window $(4.804167,5.312161]$, its ceiling $3.986097$, and its analytical Proposition 3 analog with the third outcome under challenger mixtures. State that the two-sided mixed branches are numerical diagnostics (X_C1's map) and that the paper's upward entry order at $1.55$ to $1.65$ is not reproduced.
3. **One footnote at Proposition 3.** The coexistence of no trade with full orders has a closed-form proof in the discrete companion, which supports the computer-assisted certificates. Feedback raises the full-order payoff coefficient $c_T=0.227825$ above the no-trade coefficient $\rho/2=0.125$, so both outcomes exist exactly for $\Delta_T(r)\in[k/c_T,2k/\rho]$. In the buy-only variant the condition reads $(1+\rho)a/(1+a)^2>\rho/2$.

**Keep out.** The reserve-after-price result (a hold-up result that rests on $c_L\le0.1$ and a tie rule; not the paper's question). The disclosure result (a different question; at most one sentence in the conclusion: the mechanism matters when the target cannot certify fit). The stake, incumbent-response and sequential-entry extensions: each rests on a belief completion or a selection, and each changes the question. The three-point model: dominated as a companion.

**Two extensions that merit further work.**

- **Costly information acquisition (C6).** The result is analytical and clean: no research and full research coexist on a cost interval at the strong benchmark, and a stronger incumbent raises the private return to research within an entry regime. It connects the paper to the verified record of Dow, Goldstein and Guembel (2017). The open parts are the welfare sign and the tie rule.
- **Two trading rounds (C2).** It recovers Prop. 2 and coexistence at the paper's own costs and adds a testable price-path implication. Before any use, repeat the exercise with a fixed cumulative purchase limit, so that the capacity confound is removed.

**A caution on parameters.** Any buy-only discrete statement needs $c_H\in(4.804167,5.312161]$; the paper's $c_H=6$ recruits nobody for $b>1.9576$. Any two-sided discrete statement keeps $c_H=6$.

## 5. What remains open

1. The full mixed correspondence of the two-sided discrete model, and its exact uniqueness thresholds inside $(1.220998,2.124148)$ (C1; X_C1's map is numerical). **open**
2. The order of the branch regions in $r$ for the buy-only base: $r_I$ and $r_U$ cross once on a 5,701-point grid, but no proof exists. **numerical diagnostic**
3. Atomless preparation costs in the discrete-Laplace model: the $s^*$ outcome should become an interior root and coexistence should survive. **conjecture**
4. Two rounds with a fixed cumulative purchase limit; the infinite-horizon game with a retained position. **open**
5. Sequential challengers: existence at $\kappa=-1/2$, $r=3.6$, $c_H=4.4$; uniqueness over mixtures at $r=3,3.6$; the within-class value spread in condition (NC); a long-lived investor. **open**
6. The incumbent's response: a derivation of rule IC-P from a perturbed game; a bid before the price; non-degenerate value classes. **open**
7. The reserve after the price with $c_L>0$ in general, an open set for Proposition C8.4, and seller objectives beyond proceeds. **open**
8. The Laplace large-stake plateau: whether challenger mixtures remove the nonexistence found in the earlier study. **conjecture**
9. Disclosure with mixed investor ties in the gaps; the toehold with optimal bids; costly or limited tests. **open**
10. A region map for unequal noise beyond the one certified interval. **open**
11. Props. A.5 to A.7 analogs in the discrete-Laplace model (private signals, atomless costs, a logistic comparison). **open**
12. Full texts of the abstract-only sources before any new citation (Fishman 1988; Bulow, Huang and Klemperer 1999; Daniel and Hirshleifer 2018). **open**

## 6. Plain summary

What survives when trade is discrete depends on the noise, not on discreteness as such. With three-point noise the top flow reveals the class and pays the investor nothing. The main result survives in a weak form; coexistence, feedback and the early ceiling die; an unused flow needs a belief rule. With noise that is the difference of two geometric counts, every flow is on path, beliefs stay inside the unit interval, and the recruiting flow still pays the investor. Then the main result and the coexistence result hold with short proofs. The buy-only version needs a lower preparation cost than the paper's. The two-sided version keeps the paper's cost and reproduces the paper's posterior bounds, its ceiling and its no-trade boundary exactly. No discrete version reproduces the paper's partial sales or the upward order of entry at its three certified strengths.

Among the modifications, two-sided orders rank first. Two trading rounds and costly information come next; both create coexistence at the paper's own strengths, with one caveat each. Unequal noise with mixtures restores an upward entry branch on a narrow window. Delay, a stake, an incumbent that bids back, and a toehold change magnitudes and add branches; each needs a belief completion, a selection, or fixed bids. A seller who sets the reserve after the price kills the entry response unless the low cost is near the paper's value. Costless disclosure removes the reversal. A second potential challenger makes the weak market trade, so the no-trade premise fails.

Five earlier claims were refuted (one number in the brief and four claims in the memos), two further general statements fell, and six claims were overclaimed; no shared number was wrong. Keep the Laplace model, add a short remark and an appendix section on the two-sided companion, and pursue costly information and two rounds next.
