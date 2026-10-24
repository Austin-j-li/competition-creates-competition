# Paper digest for the 40-minute talk

Source: `paper/main.md` (line numbers below are main.md lines; `main_filled.md` has identical numbering) and `paper/main_filled.md` (display values). Registry: `numerics/quantity_registry.csv`. Status vocabulary preserved: analytical, computer-assisted, numerical diagnostic, open; declarations = input.

## 1. Bottom line and research question

**Bottom line (with its number).** A stronger incumbent bidder can attract a challenger: at the benchmark, moving the incumbent from r0 = 1.2 to r1 = 3 lowers the challenger's gross acquisition profit at the prior (4.804167 to 4.291667) yet raises challenger preparation (entry E) from 0.250000 to 0.522757 (+27.28 percentage points) and high-value-challenger ownership from 0.125000 to 0.324192, because the price becomes informative (target-payoff spread 0.016667 to 0.666667). Holding the price experiment fixed reverses it: entry falls from 0.562178 to 0.522757 (main.md 257, 267). Status: analytical (Proposition 2).

**Research question.** Does stronger competition for a takeover target reduce or raise the entry of a further bidder when that bidder can watch the target's stock price before paying a preparation cost? The paper's answer is that competition can raise entry through the information channel, outweighing the direct deterrence of lower acquisition profit (main.md 13).

## 2. Theory primitives

**Agents (2.1-2.2, main.md 43-85).**
- Seller: publicly commits to a cash second-price auction with reserve p before trading; all target shares are bound by the sale (no tendering or holdout).
- Incumbent bidder: already prepared, no participation cost; value R uniform on [0, r], knows R; r is "strength" (first-order stochastic dominance shift); public distribution, realized R private until it bids. Not an announced bid.
- Challenger (one buyer): value theta in {l, h}, equal priors; does not know theta initially; sees price P, then privately learns preparation cost C (c_L w.p. rho, else c_H; 0 <= c_L < c_H, 0 < rho < 1). Paying C reveals theta and permits bidding; declining = stays out (cannot bid its expected value).
- Informed investor: observes theta, order q in [-1,1], linear cost k|q| (k > 0), no control rights, cannot acquire.
- Market makers: competitive, see aggregate flow X = q + Z only, set P(X) = E[V_T | X], anticipating preparation and auction outcomes.
- Noise demand Z: Laplace, f(z) = (1/2b) e^{-|z|/b}, b > 1 (logistic in extension). All strategic agents risk neutral; incumbent value, challenger value, cost, noise mutually independent.

**Restrictions (eq. 1, main.md 54):** 0 < p < l < r < h. Standalone target value normalized to 0.

**Timing (main.md 85):** seller announces rule; investor learns theta and trades; market makers set price from flow; challenger observes price and own cost, decides to prepare; prepared bidders learn values and bid truthfully; ownership and payoffs realized.

**Information.** Challenger sees P and C, not X, theta or R. Investor sees theta, not R. Market makers see only X. Baseline: perfect investor, uninformed challenger. Extension (5.3): conditionally independent binary signals, investor accuracy a, buyer accuracy d, both in (1/2, 1); buyer signal may be more accurate.

**Choices and constraints.** Investor: max q{V_T - P(X)} - k|q|. Challenger: prepare iff expected gross profit B_r(mu) >= C (entry at indifference, tie rule). Bidders: truthful (weakly dominant). Reserve-equal bids admissible.

**Equilibrium concept (2.3, main.md 89).** Order distributions sigma_H, sigma_L (mixing allowed, any deviation in [-1,1]), measurable price function, Bayesian beliefs, optimal preparation, truthful bidding. Two comparisons kept distinct: unilateral investor deviation (against FIXED price and preparation schedules) versus cross-economy comparison (re-solves schedules). Uniqueness refers to trading and on-path entry under truthful bidding.

**Load-bearing assumptions.**
1. Preparation is a participation cost required for an executable bid (no uninformed bid).
2. Cash second-price auction with reserve; pointwise target-payoff difference (R - l)_+ is a property of this payment rule (Sec 6.2 shows another institution changes it).
3. Bounded likelihood ratio of Laplace noise: posterior confined to [m, M], m = 1/(1+e^{2/b}), M = 1 - m (eq. 7; Prop A.1).
4. Participation floor: c_L < B_r(m), so low-cost type always prepares, entry >= rho > 0 (main.md 235: "part of the mechanism, not a numerical regularizer"; without it no informative trading is consistent).
5. Investor's information need not dominate the buyer's (complementary information).
6. Decision interval (1.1, main.md 33): sale opportunity publicly understood while stock trades and a further bidder can still enter; a wholly confidential process does not qualify. Paper does not settle any specific transaction.

**Closed forms (eq. 4-5, main.md 99-121), uniform incumbent.** t_0 = p(1 - p/r); t_H = r/2 + p^2/(2r); t_L = l - (l^2 - p^2)/(2r); g_H = h - r/2 - p^2/(2r); g_L = (l^2 - p^2)/(2r); Delta_T(r) = (r - l)^2/(2r); B_r(mu) = g_L + mu(g_H - g_L). Derivatives: Delta_T' > 0, g_H' < 0, g_L' < 0.

### Main propositions and every scope condition

**Proposition 1 (analytical; main.md 125).** Competition and the two returns to information. Incumbent value has continuous F on [0, r-bar], 0 < p < l < r-bar < h, F extended by unity above support. FOSD strengthening of F weakly raises the target-proceeds spread Delta_T(F) = E_F[(R - l)_+] = integral_l^{r-bar} [1 - F(u)] du and weakly lowers challenger gross profit at every fixed posterior, G_theta(F) = E_F[(theta - max{p, R})_+] = integral_p^theta F(u) du. Strict when the change in F has positive integral over the range. Scope: cash second-price with reserve. Intuition: if R <= l both types pay max{p, R}; if R > l a high-value challenger pays R while a low-value one loses and the incumbent pays l; difference is (R - l)_+, increasing in R.

**Proposition 2 (competition creates competition; analytical; main.md 216-233).** Fix 0 < p < l < r0 < r1 < h, 0 < rho < 1, b > 1, k > 0 and suppose, EXACTLY:

- (A1) `0 <= c_L < B_{r_1}(m)`
- (A2) `B_{r_0}(1/2) < c_H < B_{r_1}(M)`
- (A3) `Delta_T(r_0) < k < (1 - 1/b) rho m Delta_T(r_1)`

(i) Weak incumbent r0: unique equilibrium trading q_H = q_L = 0, price uninformative, entry = rho. (ii) Strong incumbent r1: unique trading (q_H, q_L) = (1, -1), price informative, entry strictly exceeds rho, probability that the high-value challenger acquires the target strictly higher than at r0; the strong price experiment strictly Blackwell dominates the weak one at the same noise law. (iii) For any r2 in (r1, h) with c_L < B_{r2}(m), B_{r2}(M) < c_H, and k < (1 - 1/b) rho m Delta_T(r2): unique trading again (1, -1) but entry returns to rho. Holds on a nonempty open set of primitives. Uniqueness = trading and on-path entry under truthful bidding; arbitrary mixed orders and every unilateral deviation q in [-1,1] allowed (audit F37). Result is "a rise and a subsequent fall", not a monotone path (main.md 253).
- Role of A1: participation floor (main.md 235). A2: excludes high-cost prep at weak prior, permits it at favorable strong prices. A3: cost above every informational return in the weak economy, below a global bound on marginal trading profit in the strong economy.
- Derived objects (eq. 12, main.md 243-248): tau = (c_H - g_L)/(g_H - g_L); x* = (b/2) log(tau/(1 - tau)); alpha_H = 1 - (1/2)e^{(x*-1)/b}; alpha_L = (1/2)e^{-(x*+1)/b}; E = rho + ((1 - rho)/2)(alpha_H + alpha_L); O_H = (1/2)[rho + (1 - rho) alpha_H]. A2 puts tau in (1/2, M) and x* in (0, 1); alpha_H > alpha_L so extra entry tilts to high-value challengers.
- Nonempty for every h > l (Sec 5.2; A.25): r0, r1 chosen close enough to l; mathematical nonemptiness, not an effect-size claim at every ratio.

**Proof intuition (main.md 237, 535-550).** Weak economy: gross advantage per unit <= Delta_T(r0) < k, so any nonzero order loses; posterior stays at the prior; only low-cost prepares. Strong economy: the residual advantage has lower bound rho m Delta_T (eq. 11); derivative U'(s) >= (1 - 1/b) rho m Delta_T - k > 0 for all s in [0, 1], so full correctly signed order strictly dominates every smaller one against every candidate schedule (global, not first-order). This forces (1, -1); favorable prices then cross the expensive threshold with positive probability. Blackwell dominance: constant kernel maps strong experiment to weak; no state-independent kernel maps the constant experiment to the strong one.

**Residual advantage (eq. 11, main.md 201-203):** A_H = e_r(mu_X) Delta_T (1 - mu_X); A_L = e_r(mu_X) Delta_T mu_X; rho m Delta_T <= A <= Delta_T. Interpretation: entry probability x payoff spread x market's residual uncertainty.

### Fixed-information control (Proposition A.3; analytical; main.md 554)
Fixed signal S and quality Theta distribution, cost C independent with fixed law, posterior Pr(H|S) independent of r. Then entry is weakly decreasing in r; strictly when the profit decline crosses preparation costs on a positive-probability set. Applies only within a region of fixed full orders (conditional flow laws do not depend on r); NOT across order profiles that change with r. Numbers: frozen full orders, entry 0.562178 at r = 1.2 falls to 0.522757 at r = 3 (status: numerical diagnostic; the frozen r = 1.2 profile is not an investor equilibrium, deviation gain 1.619e-2). Price-hidden control: entry 0.250000 at both strengths (analytical). Conclusion: incumbent strength changes the information generated by trading; the entry response can exceed direct deterrence.

### Coexistence and correspondence (Section 4.3, Proposition 3; computer-assisted; main.md 273-304)
- Proposition 3 (computer-assisted): at the benchmark, equilibria (q_H, q_L) = (1, -v_j) at r_j = 1.55, 1.60, 1.65 with certified enclosures for v_j and E_j (eq. 13) whose entry intervals are strictly ordered upward; each economy also admits no trade with entry rho. Proof by outward interval arithmetic on exact decimal inputs: low type globally strictly concave, sign change of Psi(r, .) gives a root; high type covered by a uniform derivative bound over the whole bracket (margins 0.0000761777, 0.0027531948, 0.0054921767). Does NOT prove uniqueness of the informative profile, exclude mixed equilibria, or certify a continuous branch between nodes.
- Analytical thresholds (Prop A.4, benchmark): no trade is an equilibrium iff rho Delta_T(r)/2 <= k, i.e. r <= r_N = 1.747877538; uniquely optimal below sufficient bound r(k) = 1.220997512; unique full orders above r_U = 2.837416964; expensive entry infeasible above r_C = 3.592658519 (indifferent challenger still prepares at r_C). Existence boundary, sufficient uniqueness bound, ceiling answer different questions and need not coincide.
- Numerical continuation (Figure 2): asymmetric family (1, -v) with v rising toward 1 and entry rising; symmetric interior family with entry rho; a mixed candidate at the no-trade boundary labeled numerical diagnostic. Searches are not exhaustive; "multiplicity found; search not exhaustive". Complete intermediate correspondence: **open**.

### Robustness (Section 5)
- Logistic noise (Prop A.5, analytical): |f'| <= f/b is all that is used; unique trading and entry comparison remain. Posterior reaches bounds only as flow to infinity. Entry 0.301509 vs Laplace 0.522757; threshold flow 5.424598398 = 1.495369 noise s.d.; same posterior bounds support different participation (tail mass). Figure 3 is a fixed-profile comparison at common scale b, not common variance; not a Blackwell ranking.
- Atomless costs (Prop A.6, analytical): supports within half-width epsilon_C = 0.1 (eq. A.24 support restrictions); entry 0.522715 (Laplace), 0.301374 (logistic).
- Moderate values (5.2, analytical): h = 2, l = 1; entry 0.250000 to 0.526805; all five strict margins positive.
- Complementary signals (Prop A.7, analytical): a = 70%, d = 75% (declared example, not a joint calibration); entry 0.850000 to 0.879438; does not require a >= d; entry is state dependent (e_H, e_L) but price still reveals the market posterior. Complete accuracy grid online: reversal holds only where the sufficient margins are met (numerical diagnostic elsewhere, incl. negative changes, e.g. d = 0.76 rows show entry falling with preparation already high at weak).

### Welfare (Section 6.1, Proposition A.9; analytical)
At fixed strength r1: access to prices strictly raises expected target proceeds (0.872392 vs 0.614583; gain 0.257809) and acquisition surplus net of preparation costs (W 2.382301 vs 2.302083; gain 0.080218). Trading costs coincide (full orders both). Each added preparation contributes at least p^2/r in conditional expectation. Does not rank incumbent strengths or sale mechanisms. Matched-dividend diagnostic (numerical diagnostic): add external dividend 0.257809 to the claim in the hidden economy; mean price matches feedback economy, entry still differs: information, not price level, matters. Diagnostic only, not a feasible sale mechanism, excluded from surplus.

### Bargaining (Section 6.2, Proposition A.8; analytical; main.md 357-372)
Zero-reserve verifiable-value institution; Nash bargaining seller weight eta; fallback = runner-up value. Transfer T_eta, G_{theta,eta} = (1 - eta) E[(theta - R)_+], Delta_eta = eta(h - l) + (1 - 2 eta) E[(R - l)_+]. Stronger incumbent weakly reduces challenger profit for every eta; effect on spread positive for eta < 1/2, zero at eta = 1/2, negative for eta > 1/2 (0 <= eta < 1). Scope: does NOT establish an entry reversal under bargaining (trading and participation not solved); does not solve first-price or bargaining-and-trading equilibrium.

### Reserve results (Section 6.3, Prop A.10, A.7; main.md 383-396)
- Reserve comparisons at listed nodes: analytical support from global trading bounds (unique trading at reported nodes). Raising reserve 0.5 to 1.1 (atomless value classes, epsilon_V = 0.05): weak proceeds 0.392665 to 0.432173; strong 0.872367 to 1.014500; prep probability at higher reserve 0.540309 (weak), 0.511638 (strong). Binary panel uses p = 1.01. Shows a feasible improvement, not an optimal reserve; no best reserve reported.
- Preparation, sale, and two-admissible-bidders probabilities separate once the reserve excludes bidders (E >= A >= C_2). Positive preparation with excluded incumbent is not more acquisition competition.
- Proposition A.10 (analytical): price-pooling family at fixed full orders (reserve p = 7, r0, cutoff c in [-log 2, 0]); orders the same, prices/beliefs/entry differ; shows continuation must include price rule. Existence only; no uniqueness; does not arise on benchmark support.
- Exploratory reserve summary (online): numerical diagnostic / "continuations found", with unresolved counts. Seller-optimal terms, commitment timing, and whether they preserve the reversal: **open**. Empirical pilot (Sec 7, Online App D) is design only; no sample assembled.

## 3. Mechanism classification

**Competing (net effect resolved by equilibrium information), with a complementary chain inside the information channel.**
- Force 1 (deterrence): stronger incumbent lowers g_H, g_L, hence B_r(mu) at every fixed belief; lowers preparation at any FIXED experiment (Prop A.3).
- Force 2 (information): same shift widens the target-proceeds spread Delta_T, raising the residual advantage A = e * Delta_T * (posterior uncertainty) and hence the investor's incentive to trade on challenger quality.
- Chain within force 2: Delta_T up (Prop 1) -> trading pays if Delta_T(r1) rho m (1 - 1/b) > k (A3) -> price informative (posterior spans [m, M]) -> favorable prices cross tau -> high-cost challenger prepares -> entry and O_H up.
- Dependency: force 2 needs the participation floor (A1: low-cost entry gives proceeds sensitivity to quality) and the price observed before preparation; force 1 dominates when information is held fixed or hidden. Net sign is resolved parametrically by A1-A3 (A2 sets the weak-prior exclusion and the strong-price inclusion). Force 2 fades at very strong r (Prop 2 iii): B_r(M) < c_H, so the deterrence force reasserts and entry returns to rho.
- Bargaining shows the opposition itself depends on the payment rule: the sign of the spread effect flips at eta = 1/2.

## 4. Antecedents and the stated increment (main.md 27)

1. Dow, Goldstein and Guembel (2017): investment decision feeds back into incentive to produce information about the stock. Increment: the sale rule divides acquisition surplus between a traded claim and a buyer deciding participation, and the two returns to information move in opposite directions as competition changes; that opposition and the participation reversal is the increment over generic learning from prices.
2. Fishman (1988) / Hirshleifer and Png (1989): preemption and entry costs; stronger rival lowers what preparation earns (direct deterrence, kept). Increment: add a market operating before preparation whose information the challenger uses.
3. Edmans, Goldstein and Jiang (2015): corrective real decisions can discourage trading on bad news under rational pricing; here rival strength changes the information sensitivity of the claim and through it participation.
4. Levin and Smith (1994) / Gentry and Stroup (2019) / Roberts and Sweeting (2013): endogenous bidder pool and selective entry; direct deterrence kept, price-information channel added. (Also contrasted: Edmans-Goldstein-Jiang 2012, Luo 2005, Persico 2000, Betton et al. 2014, Lin-Ma-Yang-Zhu 2025, Cornelli-Li 2002.)

Suggested talk anchor: Dow-Goldstein-Guembel 2017 and the Fishman/Hirshleifer-Png deterrence force.

## 5. Exhibit inventory

Figures: vector PDFs, embedded STIX fonts, 468 pt (6.5 in) wide. `talk/figures/` is currently empty.

| # | File (figures/) | Size | Caption (main.md) | Panels | 16:9 legibility |
|---|---|---|---|---|---|
| 1 (main.md 141-144) | `two_returns.pdf` | 468 x 208.8 pt (2.24:1) | "Competition and the two returns to information." Benchmark h = 10, l = 1, p = 0.5, b = 2; acquisition-stage payoffs before trading and entry. | (a) target-payoff spread Delta_T(r) vs r in [1, 3.6], rising from 0 at r = l; (b) gross profit B_r(mu) at mu = m, 1/2, M falling in r. | Yes. Wide aspect fits a slide; likely the key opening exhibit; fonts small but scalable; may add r0/r1 markers. |
| 2 (main.md 291-294) | `equilibrium_correspondence.pdf` | 468 x 374.4 pt (1.25:1) | "Trading and entry across incumbent strengths." Analytical uniqueness shading, boundaries r_N, r_U, r_C, certified black points (Prop 3), continuations broken at unresolved nodes. | (a) total entry E vs r (labels: no trade, asymmetric orders (1, -v), symmetric interior (u, -u), computer-assisted nodes, full orders no expensive entry); (b) order magnitude vs r (v, u, mixed supports, q = 0, v = 1). | Not as is. Dense annotations, near-square: needs a rebuild or two-step reveal (panel a only, then b); backup slide. |
| 3 (main.md 315-318) | `posterior_tail_entry.pdf` | 468 x 208.8 pt | "Posterior tails and high-cost entry." Full orders at strong strength, b = 2; Laplace vs logistic; fixed-profile, not Blackwell ranking. | (a) Pr(mu_X >= tau) vs M - tau; (b) implied entry vs M - tau; Laplace plateau vs logistic tail. | Legible; robustness/backup slide. |
| 4 (main.md 374-377) | `bargaining_weight.pdf` | 468 x 208.8 pt | "Bargaining and the division of acquisition surplus." Zero-reserve verifiable-value institution, h = 10, l = 1, r = 1.2 or 3. | (a) Delta_eta vs seller weight eta with eta = 1/2 marked; (b) conditional challenger profits G_H,eta and G_L,eta (weak and strong) on log scale. | Legible; panel (b) log scale with four curves is busy; use for a backup or a one-slide payment-rule point. |

Data for figures: `figures_data/two_returns.csv`, `bargaining.csv`, `posterior_tails.csv` (no data file for Figure 2 in figures_data).

Tables (main text; `tables/*.tex` with same-stem CSV where noted):

| # | File | Main.md | What it shows | 16:9 legibility |
|---|---|---|---|---|
| 1 | `table1_auction_primitives.tex` / `auction_primitives.csv` | 259-260 | Weak (r = 1.2) vs strong (r = 3): t_0, t_H, t_L, g_H, g_L, Delta_T, B_r(1/2); 7 rows x 2 columns | Yes, as is (short); best as a 3-4 row excerpt (Delta_T, B_r(1/2)). |
| 2 | `table2_equilibrium_controls.tex` / `equilibrium_controls.csv` | 262-265 | Panel A equilibrium outcomes (q_H, q_L, E, O_H, R_T, evidence, unique) at r = 1.2, 3, 3.6; Panel B controls (frozen, price hidden); Panel C access to prices (R_T, W gains) | No: 8 columns, 3 panels. Rebuild as separate slim tables (Panel A; frozen/hidden; Panel C). |
| 3 | `table3_extensions.tex` / `extensions.csv`, `extensions_margins.csv` | 338-341 | Robustness: E weak, E strong, Delta E (pp), O_H weak, O_H strong for Laplace/logistic x atoms/mixture, moderate values, complementary signals | Borderline: 8 columns, 6 rows. Drop the Evidence/Unique columns for the slide (state in a footnote line). |
| 4 | `table4_reserve_comparisons.tex` / `reserve_comparisons.csv` | 389-392 | Reserve comparisons: preparation, sale, two admissible bidders, expected target proceeds, trading outcome; Panel A binary (p = 0.5, 1.01), Panel B atomless (p = 0.5, 1.1) | Borderline: 6 columns, 8 rows; use one panel (B) or a backup. |

Online tables (backup only): `table_matched_price.tex` (matched dividend by noise/cost law; 7 columns, 4 blocks; too dense), `table_extensions_margins.tex` (five strict margins and minimum), `table_reserve_details.tex` (orders, margins, evidence; 11 columns), `table_reserve_exploratory.tex` (exploratory reserve search coverage counts; numerical diagnostic), `table_signal_grid.tex` (a in 0.68..0.72+, d in 0.73..0.77 grid; longtable, 10 columns). Not slide-legible; cite in appendix or backup only.

## 6. Number inventory (display value as printed in main_filled.md)

Registry names are in `numerics/quantity_registry.csv`. "—" = value comes from a `tables/*.csv` or table .tex file with no separate registry scalar.

### Benchmark inputs (Appendix A.8 and text)
| Display | Registry name | Status | main.md line |
|---|---|---|---|
| 10 (h) | base_h | input | 144, 377, 1117 |
| 1 (l) | base_ell | input | 144, 377, 1117 |
| 0.5 (p) | base_p | input | 144, 387, 1117 |
| 0.25 (rho) | base_rho | input | 1117 |
| 1 (c_L) | base_c_low | input | 1117 |
| 6 (c_H) | base_c_high | input | 1117 |
| 2 (b) | base_b | input | 144, 318, 1117 |
| 0.02 (k) | base_k | input | 1117 |
| 1.2 (r0) | base_r_weak | input | 257, 377, 1118 |
| 3 (r1) | base_r_strong | input | 257, 377, 1118 |
| 3.6 (r2) | base_r_collapse | input | 257, 1118 |
| 0.1 (epsilon_C) | cost_halfwidth | input | 1146 |
| 0.05 (epsilon_V) | value_band_halfwidth | input | 387, 1146 |
| 1.1 (higher reserve, atomless) | value_reserve_high | input | 387 |
| 7 (price-pool reserve) | pool_reserve | input | 1148 |
| 1.55, 1.60, 1.65 (certified nodes) | cert_a_r, cert_b_r, cert_c_r | input | 280-282 |
| h = 2, l = 1, p = 0.5, rho = 0.25, c_L = 0.3, c_H = 0.89, b = 2, k = 0.002; r = 1.05, 1.5 | moderate_h, moderate_ell, moderate_p, moderate_rho, moderate_c_low, moderate_c_high, moderate_b, moderate_k, moderate_r_weak, moderate_r_strong | input | 326, 1128-1129 |
| h = 10, l = 1, p = 0.5, rho = 0.85, c_L = 1, c_H = 7.14, b = 2, k = 0.015; r = 1.1, 2.3; a = 0.70, d = 0.75 | signal_h, signal_ell, signal_p, signal_rho, signal_c_low, signal_c_high, signal_b, signal_k, signal_r_weak, signal_r_strong, signal_trader_accuracy_value, signal_buyer_accuracy_value | input | 1139-1141 |
| 70\% (a), 75\% (d) | signal_trader_accuracy, signal_buyer_accuracy | input | 336 |

### Headline results: acquisition stage and entry
| Display | Registry name | Status | main.md line |
|---|---|---|---|
| 4.804167 (B_r(1/2), r0) | base_profit_prior_weak | analytical | 257 |
| 4.291667 (B_r(1/2), r1) | base_profit_prior_strong | analytical | 257 |
| 0.016667 (Delta_T, r0) | base_spread_weak | analytical | 257 |
| 0.666667 (Delta_T, r1) | base_spread_strong | analytical | 257 |
| 0.250000 (E at r0) | base_entry_weak | analytical | 257 |
| 0.522757 (E at r1) | base_entry_strong | analytical | 257, 313 |
| 0.125000 (O_H at r0) | base_ownership_weak | analytical | 257 |
| 0.324192 (O_H at r1) | base_ownership_strong | analytical | 257 |
| 0.250000 (E at r2, entry returns to rho) | base_entry_collapse | analytical | 257 |
| 27.28 (Delta E, percentage points, base) | base_entry_change_pp | analytical | Table 3 (338-341) |
| 0.562178 (frozen orders, E at r0) | base_frozen_entry_weak | numerical diagnostic | 267 |
| 0.522757 (frozen orders, E at r1) | base_frozen_entry_strong | numerical diagnostic | 267 |
| 0.250000, 0.250000 (price hidden, E at r0, r1) | base_hidden_entry_weak, base_hidden_entry_strong | analytical | 269 |
| 0.269 posterior bounds: m = 0.268941421, M = 0.731058579 | base_m, base_M | analytical | (Online App / thresholds.csv; formula eq. 7, main.md 158) |

Table 1 (main.md 259-260), weak / strong: t_0 0.291667 / 0.416667; t_H 0.704167 / 1.541667; t_L 0.687500 / 0.875000; g_H 9.295833 / 8.458333; g_L 0.312500 / 0.125000; Delta_T 0.016667 / 0.666667; B_r(1/2) 4.804167 / 4.291667. Source `tables/auction_primitives.csv`; only Delta_T and B_r(1/2) have registry scalars. r = 3.6 row (csv): Delta_T 0.938889, B_r(1/2) 4.134722 (not printed in main text).

Table 2 (main.md 262-265): Panel A E / O_H / R_T: r = 1.2: 0.250000 / 0.125000 / 0.392708; r = 3: 0.522757 / 0.324192 / 0.872392; r = 3.6: 0.250000 / 0.125000 / 0.664236 (analytical). Panel B: frozen r = 1.2: 0.562178 / 0.350606 / 0.520039 (numerical diagnostic); frozen r = 3: 0.522757 / 0.324192 / 0.872392; hidden r = 1.2: 0.250000 / 0.125000 / 0.392708; hidden r = 3: 0.250000 / 0.125000 / 0.614583. Source `tables/equilibrium_controls.csv` (no separate registry scalars except those listed elsewhere).

### Welfare and access to prices
| Display | Registry name | Status | main.md line |
|---|---|---|---|
| 0.872392 (target proceeds, price observed) | base_revenue_feedback | analytical | 351 |
| 0.614583 (target proceeds, price hidden) | base_revenue_hidden | analytical | 351 |
| 0.257809 (revenue gain; also matched dividend D_0) | base_revenue_gain / base_matched_dividend | analytical (gain); numerical diagnostic (dividend) | 353 |
| 0.080218 (net acquisition surplus gain) | base_net_surplus_gain | analytical | Table 2 Panel C (262-265) |
| 2.382301 vs 2.302083 (W observed vs hidden) | — (equilibrium_controls.csv; matched_price.csv) | analytical | Table 2 Panel C |

### Thresholds and certified equilibria
| Display | Registry name | Status | main.md line |
|---|---|---|---|
| 1.747877538 (r_N) | base_r_no_trade_exact | analytical | 296 |
| 1.220997512 (r(k)) | base_r_pool_unique_sufficient | analytical | 296 |
| 2.837416964 (r_U) | base_r_full_unique_sufficient | analytical | 296 |
| 3.592658519 (r_C) | base_r_high_cost_ceiling | analytical | 296 |
| 0.506477395 (Laplace entry left-limit at r_C, eq. A.14) | base_laplace_entry_ceiling_left_limit | analytical | (registry; formula 608) |
| [0.46031618, 0.46031620] (v at 1.55) | cert_a_v_interval | computer-assisted | 280 |
| [0.5450528898, 0.5450528922] (E at 1.55) | cert_a_entry_interval | computer-assisted | 280 |
| [0.70747537, 0.70747539] (v at 1.60) | cert_b_v_interval | computer-assisted | 281 |
| [0.5487563062, 0.5487563085] (E at 1.60) | cert_b_entry_interval | computer-assisted | 281 |
| [0.90333198, 0.90333201] (v at 1.65) | cert_c_v_interval | computer-assisted | 282 |
| [0.5513607988, 0.5513608020] (E at 1.65) | cert_c_entry_interval | computer-assisted | 282 |
| 0.0000761777, 0.0027531948, 0.0054921767 (high-type derivative margins) | cert_a/b/c_high_derivative_lower | computer-assisted | 679 |
| 0.000000000114 / -0.000000000096; 0.000000000123 / -0.000000000121; 0.000000000172 / -0.000000000242 (Psi sign tests, left lower / right upper, nodes a, b, c) | cert_a/b/c_psi_left_lower, cert_a/b/c_psi_right_upper | computer-assisted | 649-654 |

### Robustness
| Display | Registry name | Status | main.md line |
|---|---|---|---|
| 0.301509 (logistic E at r1) | logistic_entry_strong | analytical | 313 |
| 5.424598398 (logistic flow threshold) | logistic_flow_threshold | analytical | 313 |
| 1.495369 (threshold in noise s.d.) | logistic_threshold_noise_sd | analytical | 313 |
| 0.522715 (Laplace, cost mixture) | cost_mix_laplace_entry_strong | analytical | 322 |
| 0.301374 (logistic, cost mixture) | cost_mix_logistic_entry_strong | analytical | 322 |
| 0.250000 to 0.526805 (moderate values E weak, strong); 27.68 pp | moderate_entry_weak, moderate_entry_strong, moderate_entry_change_pp | analytical | 326; Table 3 |
| 0.850000 to 0.879438 (signals E weak, strong); 2.94 pp | signal_entry_weak, signal_entry_strong, signal_entry_change_pp | analytical | 336; Table 3 |

Table 3 (main.md 338-341), E weak / E strong / Delta E (pp) / O_H weak / O_H strong: Laplace atoms 0.250000 / 0.522757 / 27.28 / 0.125000 / 0.324192; Laplace mixture 0.250000 / 0.522715 / 27.27 / 0.125000 / 0.324148; logistic atoms 0.250000 / 0.301509 / 5.15 / 0.125000 / 0.161994; logistic mixture 0.250000 / 0.301374 / 5.14 / 0.125000 / 0.161854; moderate 0.250000 / 0.526805 / 27.68 / 0.125000 / 0.327032; signals a = 0.70, d = 0.75: 0.850000 / 0.879438 / 2.94 / 0.425000 / 0.448942. Source `tables/extensions.csv`, `extensions_margins.csv`. Five strict margins (base; Table 2 note): zeta_L 1.37e0, zeta_H0 1.20e0, zeta_H1 2.17e-1, zeta_0 3.33e-3, zeta_1 2.41e-3 (registry base_margin_*; minimum base_minimum_theorem_margin 2.411785114e-3; moderate 8.014731393e-4; signal 1.454545455e-3), analytical.

### Reserve comparisons (Section 6.3; main.md 387)
| Display | Registry name | Status | main.md line |
|---|---|---|---|
| 0.392665 (weak proceeds, p = 0.5, atomless) | value_revenue_weak_low_p | analytical | 387 |
| 0.432173 (weak proceeds, p = 1.1) | value_revenue_weak_high_p | analytical | 387 |
| 0.872367 (strong proceeds, p = 0.5) | value_revenue_strong_low_p | analytical | 387 |
| 1.014500 (strong proceeds, p = 1.1) | value_revenue_strong_high_p | analytical | 387 |
| 0.540309 (preparation, weak, p = 1.1) | value_entry_weak_high_p | analytical | 387 |
| 0.511638 (preparation, strong, p = 1.1) | value_entry_strong_high_p | analytical | 387 |

Table 4 (main.md 389-392), Preparation / Sale / Two admissible / Proceeds / Trading: A weak p = 0.5: 0.250000 / 0.687500 / 0.145833 / 0.392708 / no trade; A weak p = 1.01: 0.543573 / 0.443232 / 0.053595 / 0.452756 / full orders; A strong p = 0.5: 0.522757 / 0.920460 / 0.435631 / 0.872392 / full orders; A strong p = 1.01: 0.513373 / 0.770226 / 0.210611 / 0.987487 / full orders. B weak p = 0.5: 0.250000 / 0.687500 / 0.145833 / 0.392665 / no trade; B weak p = 1.1: 0.540309 / 0.391610 / 0.028025 / 0.432173 / full orders; B strong p = 0.5: 0.522760 / 0.920460 / 0.435634 / 0.872367 / full orders; B strong p = 1.1: 0.511638 / 0.749292 / 0.200293 / 1.014500 / full orders. Source `tables/reserve_comparisons.csv`; only the atomless rows have registry scalars (above).

### Price-pool regression (Appendix, Prop A.10; main.md 1047)
Pooled posterior 0.272979 (c = -log 2) and 0.303265 (c = 0): pool_posterior_cutoff_low/high; preparation 0.151805 and 0.125000: pool_entry_cutoff_low/high; revenue 0.687364 and 0.609643: pool_revenue_cutoff_low/high. All analytical. Backup only.

## 7. Symbol table

"Locked by C0" = the symbol is one of the CSV column names fixed in Online Appendix C.0 (h, ell, p, rho, c_L, c_H, b, k, r, Delta_T, B_prior, q_H, q_L, e_H, e_L, E, O_H, R_T, tau, x_star).

| Symbol | Meaning | First definition (main.md line) | Locked by C0 |
|---|---|---|---|
| R | incumbent's acquisition value, uniform on [0, r] | 49 | no |
| r | incumbent strength (support upper bound); r0, r1, r2 weak, strong, very strong | 49 | yes (r; r_weak, r_strong, r_collapse inputs) |
| theta in {l, h} | challenger acquisition value (equal priors) | 51 | no |
| l (\ell) | low challenger value | 51 | yes (ell) |
| h | high challenger value | 51 | yes |
| p | reserve price | 51 | yes |
| C | challenger preparation cost | 58 | no |
| c_L, c_H | low and high cost levels | 58 | yes |
| rho | probability the realized cost is c_L (entry floor) | 58 | yes |
| q | investor order in [-1, 1] | 64 | no (q_H, q_L are locked) |
| k | linear trading cost coefficient | 64 | yes |
| X, Z | aggregate order flow X = q + Z; Laplace noise demand | 68, 74 | no |
| b | noise scale (Laplace/logistic) | 69 | yes |
| V_T | terminal payoff of a target share | 74 | no |
| P(X) | competitive price E[V_T given X] | 79 | no |
| sigma_H, sigma_L | conditional order distributions | 89 | no |
| t_0 | target proceeds without entry | 91 | no |
| t_H, t_L | proceeds with entry and quality H or L | 91 | no |
| g_H, g_L | challenger gross acquisition profit, quality H, L | 91 | no |
| Delta_T (Delta_T(r), Delta_T(F)) | target-payoff spread t_H - t_L | 91 (closed form 106) | yes |
| mu | belief Pr(theta = h) | 91 | no |
| B_r(mu) | challenger expected gross profit g_L + mu(g_H - g_L) | 91 | no (B_prior = B_r(1/2) is locked) |
| B_prior | B_r(1/2), gross profit at prior (CSV column; text writes B_r(1/2)) | 116 (as B_r(1/2); Table 1 260) | yes |
| G_theta(F) | expected profit against F | 125 | no |
| F, r-bar | general incumbent distribution and its support bound | 125 | no |
| a_H(x), a_L(x), mu_X(x) | flow densities and order-flow posterior | 154-156 | no |
| m, M | posterior bounds 1/(1 + e^{2/b}) and 1 - m | 158 | no |
| e_r(mu) | cost-averaged entry rule | 175 | no (e_H, e_L are locked as state-conditioned entry, A.28 at 800) |
| e_H, e_L | state-conditioned entry rates (complementary signals; CSV entry by state) | 800 (main.md 548 uses e_H) | yes |
| A_H(x), A_L(x) | investor's residual advantage in H, L | 201 | no |
| tau | threshold belief (c_H - g_L)/(g_H - g_L) | 243 | yes (tau) |
| x* | flow at the threshold, (b/2) log(tau/(1 - tau)) | 244 | yes (x_star) |
| alpha_H, alpha_L | conditional probability of crossing the threshold | 245-246 | no |
| E (\mathsf E) | entry: probability that the challenger pays preparation cost | 247 | yes |
| O_H (\mathsf O_H) | probability a high-value challenger owns the target | 248 | yes |
| q_H, q_L | investor's orders in state H, L; (1, -1) full orders | 233 (statement), 275 | yes |
| v_j, v | short magnitude (q_L = -v) at certified strength r_j; r_j = 1.55, 1.60, 1.65 | 275 | no |
| R_T (\mathcal R_T) | expected target (seller) proceeds/revenue, defined via t_theta and e_theta | 351 (text); 935 defined (Delta R_T); 977 (A.44) | yes |
| W (\mathcal W) | allocation value net of paid preparation costs | Table 2 note (265); 934 | no |
| eta | seller Nash bargaining weight | 357 | no |
| T_eta, G_{theta,eta}, Delta_eta | bargaining transfer, challenger profit, target spread | 363-365 | no |
| epsilon_C, epsilon_V | cost half-width, value-class half-width | 741, 387 | no (inputs cost_halfwidth, value_band_halfwidth) |
| a, d | investor signal accuracy, buyer signal accuracy | 330 (A.26 at 777) | no (inputs signal_trader_accuracy_value, signal_buyer_accuracy_value) |
| T, Y | investor and buyer binary signals | 330 | no |
| lambda_X, mu_-, mu_+, phi_+, phi_-, D | signal-extension objects | 784-802 | no |
| r_N, r_U, r_C, r(k) | no-trade existence, full-order uniqueness, high-cost ceiling, pooling-uniqueness thresholds | 296 (Prop A.4 at 568-575) | no (values are registry scalars) |
| zeta_L, zeta_H0, zeta_H1, zeta_0, zeta_1 | five strict margins of Proposition 2 | Table 2 note (265); online | no |
| D_0 | matched external dividend | 353 (text); online table | no |
| A, C_2, S (\mathsf A, \mathsf C_2, \mathsf S) | admissible-challenger, two-admissible-bidder, sale probabilities | 1077-1079 | no |
| c, P_c, mu-bar_c | price-pool cutoff, price rule, pooled posterior | 992-1009 | no |

Notation collisions to avoid on slides: R (incumbent value) vs R_T (target proceeds) vs \mathcal R_T; a (investor accuracy) vs a_H(x) (flow density) vs \mathsf A; d (buyer accuracy) vs d in r(d); e (entry, e_r, e_H) vs \mathsf E (entry probability) vs exponential e; T (investor signal) vs subscript T (target) in V_T, t_H, Delta_T, R_T; H, L are used both for states and for cost labels (c_H, c_L cost; theta = h, l value; state labels H, L); h (high value) vs h_C (density) and H_C (cost CDF); t_0 vs the constant 0.

## Additional notes for the talk builder
- Values in main_filled.md are shown at 6 decimals (thresholds 9 decimals; certificate enclosures 8 to 10 decimals). Percentage-point changes use registry percentage_point (27.28, 27.68, 2.94).
- The benchmark headline compares three strengths (1.2, 3, 3.6); the "rise and fall" is across the three economies; no monotone path is claimed.
- Do not present Figure 2's numerical continuations as equilibria "proved"; only the three black points are computer-assisted; the correspondence between them is open.
- Do not present the bargaining or empirical-pilot sections as reversal or evidence results.
