# L2: Taxonomy of microstructure methods for the paper's mechanism (22 October 2026)

Workstream L2. No browser. Sources: the verified records named in §1. Scripts: `scripts/L2_taxonomy/` (`devices.py`, `twosided_profiles.py`, and their `.out.txt` files). Status labels: **analytical**, **computer-assisted**, **numerical diagnostic**, **conjecture**, **open**. A fact from my own knowledge is marked "unverified" and listed in §6.

## 1. Scope

Question. Which microstructure methods do models use when trading interacts with a corporate decision? Which of them can give the paper's results with strength comparable to the Laplace model?

Sources.

- `alex_meeting_2026_10_21/memos/LIT_extracts.md` (cited as A1–A7, C13, C14, and so on).
- `alex_meeting_2026_10_21/memos/Q2_discrete_literature.md` (cited as Q2).
- `discrete_exploration_2026_10_21/memos/D_literature.md` (cited as D).
- `discrete_exploration_2026_10_21/memos/A_three_point.md`, `B_dlaplace_theory.md`, `SYNTHESIS.md`.
- The pinned paper (`01bd5d6`): §2.3 (trading), §3.2 (inference), §4.1 (Prop. 2), §4.3 (Prop. 3, ceiling `r_C`).
- `memos/L1_survey.md`: a skeleton when I started. It filled in while I worked. I use its counts and its verified readings of Dow–Gorton (1997), Admati–Pfleiderer, and Faure-Grimaud–Gromb (cited as L1 C09, C11, C13, §5).

Setting. Reading N, `c_L = 0`, `π = 1/2`, benchmark of TEAM_RULES §3. The investor sees the class `j`. The market maker sets `P = E[V_T | X]`. The challenger sees `P`. Notation:

- `P_H(x)`, `P_L(x)`: the flow laws of the two classes under the profile, including presence.
- `μ_x`: the posterior of class `H` at flow `x`.
- `τ(r) = (c_H − g_L(r)) / (g_H(r) − g_L(r))`: the posterior at which the high-cost type is indifferent.
- `M`: the largest attained posterior (essential supremum of `μ_x` over the flows of a trading class).
- `r̄`: the strength at which `g_H(r̄) = c_H`. At `c_H = 6`, `r̄ = 7.9686`.

## 2. Taxonomy table

A method is a triple: the order structure, the noise law, and what the price or the decision maker sees. The table lists the methods found in the records, and four devices found by the earlier study or by this memo. "Rec." means the record where the method appears.

| ID | Method | Order structure and noise | Corporate-finance use in the records | Rec. |
|---|---|---|---|---|
| M1 | Kyle-type, normal noise | One strategic informed trader, order size chosen, additive normal noise | Kyle (1985) is the base cited by the pinned paper; Kyle–Vila (1991) takeover noise (abstract only); Chordia–Subrahmanyam (2004), non-corporate | paper §2.3; A4; C14 |
| M2 | Noisy rational expectations | Continuum of price-taking informed traders, orders in `[−1, 1]` or linear, normal noise or supply | DGG (2017), GOY (2013), Bond–Goldstein (2015), BGP (2010) | A3; D §3.6–3.8 |
| M3 | Discrete three-point | Orders in `{−1, 0, 1}`, additive noise in `{−1, 0, 1}`, presence `λ`, cost per unit | EGJ (2015), GG (2008) | A1; A2; Q2 |
| M4 | Exclusive arrival (one order per arrival) | One order arrives: informed with probability `λ`, else a liquidity order of the same size. With or without a separate additive noise | Dow–Gorton (1997): informed or liquidity order of size `x`, perfectly negatively correlated (L1 C09). BKT (2017): informed or noise trader. Admati–Pfleiderer: a shock forces the same whole-stake sale (L1 C11). Faure-Grimaud–Gromb: same-size orders (L1 C13). Glosten–Milgrom (1985) and PIN: unverified | A7; L1 |
| M5 | One-sided exponential | Additive noise `u > 0` with density `λ e^{−λu}`; informed order chosen | Edmans (2009) | A6 |
| M6 | Uniform noise | Additive bounded noise, continuous | BKT working paper (footnote 6 in Q2); the published BKT allows general densities | Q2; A7 |
| M7 | General full-support densities | Any density, tails at least exponential; bounded score | BKT (2017) general `f_s, f_b`; paper's Prop. A.5 class (logistic, hyperbolic secant, Student) | A7; paper §2.3, A.5 |
| M8 | Laplace | Additive Laplace noise, orders in `[−1, 1]`, cost `k|q|` | This paper. One numerical preprint (Friedrich–Teichmann 2020) | C13 |
| M9 | Discrete Laplace (geometric counts) | Orders `{0, 1}` or `{−1, 0, 1}`, noise `G_1 − G_2` | None in the records; earlier study (B1, B2, C1) | `B_dlaplace_theory` |
| M10 | Count noise with `N` noise traders | Orders `{0, 1}`; noise = number of `N` noise buyers, binomial | None in the records; EGJ and GG are `N = 1` | T3 lever |
| M11 | One-sided geometric noise | Orders `{0, 1}`; noise `Z ≥ 0` with `Pr(Z = z) = (1 − a) a^z` | None in the records; discrete form of M5 | this memo |
| M12 | Coarse observation | Market maker or challenger sees a function of the flow (the sign of the imbalance, or a price grid) | None in the records | this memo |

Overlays. These change a method but are not methods: two trade dates (GG; C2), an initial stake (Edmans 2009; EGJ §II.E; C5), costly information acquisition (DGG; C6), mixed informed orders (BKT; GG; C9), imperfect informed signals (Edmans 2009; DGG).

## 3. Properties matrix with derivations

### 3.0 Common identities (all **analytical**)

Reading N, `c_L = 0`, and the paper's auction give these facts for every method.

**(G1) Residual identity.** The price is `P(x) = t_0 + e(x)[w_L + Δ_T μ_x]`, where `w_L = t_L − t_0` and `e(x)` is the entry rate at the price of flow `x`. The class-`j` value given entry is `V_j(x) = t_0 + e(x)(t_j − t_0)`. Since `t_H − t_0 = w_L + Δ_T` and `t_L − t_0 = w_L`:

`V_H − P = e(x) Δ_T (1 − μ_x)`, `V_L − P = −e(x) Δ_T μ_x`.

A buyer of class `H` earns a positive residual at flow `x` if and only if `μ_x < 1`. A seller of class `L` earns a positive residual if and only if `μ_x > 0`. This is A_three_point Result 2.

**(G2) Price sufficiency.** At `c_L = 0` entry is at least `ρ` at every price. Hence `P` is strictly increasing in `μ`, and the challenger's posterior equals `μ_x` (A_three_point Result 3). Every method enters the model only through its flow experiment `{P_H, P_L}`.

**(G3) Entry.** `e(x) = ρ + (1 − ρ) 1{μ_x ≥ τ(r)}` (the challenger prepares at indifference). Benchmark values (numerical diagnostic, `devices.out.txt`):

| `r` | 1.2 | 1.55 | 1.65 | 3 | 3.5927 | 3.6 |
|---|---|---|---|---|---|---|
| `τ(r)`, `c_H = 6` | 0.6331 | 0.6468 | 0.6507 | 0.7050 | 0.7311 | 0.7314 |

The paper's cap `M(b = 2) = 1/(1 + e^{−1}) = 0.73106`. So `r_C = 3.5927` is the strength with `τ(r_C) = M`, and `r_2 = 3.6` lies just above it. The paper's condition (A1) is the statement "`τ(r_1) ≤ M < τ(r_2)`".

**(G4) Deviation from no trade.** Under no trade (NT) every class has the noise law `N`. A unit purchase by class `H` has flow law `P_B`. Its payoff is `Δ_T Σ_x P_B(x) e(x)(1 − μ_x) − k`. If `P_B` is absolutely continuous with respect to `N`, every flow is on path with `μ = π` and `e = ρ`. Then

`V := ρ(1 − π) Δ_T`, so NT holds if and only if `k ≥ ρ(1 − π) Δ_T`.

This cutoff is the paper's `ρ Δ_T / 2`. It needs no belief, and it does not depend on the noise law or on presence (B_dlaplace Result 12(a)). If a mass `o` of `P_B` falls on flows unused under NT, an off-path belief is needed. With the Intuitive Criterion (`μ = 1`, zero residual), `V = ρ(1 − π)(1 − o) Δ_T`.

**(G5) Coexistence index.** Take the buy-only informative profile (class `H` buys, class `L` idles). Write `U = Δ_T Σ_x P_B(x) e(x)(1 − μ_x)` for the purchase payoff before cost. Define:

- `P_B`: the flow law of the purchase order, given that the investor is present;
- `D = Σ_x P_B(x) μ_x − π`: the expected posterior gain at the flows of a purchase;
- `D_on = Σ_{x on path under NT} P_B(x)(μ_x − π)`: the part of `D` that sits on flows used under NT;
- `G = (1 − ρ) Σ_{x : μ_x ≥ τ} P_B(x)(1 − μ_x)`: the recruitment gain.

Then

`(U − V) / Δ_T = G − ρ D_on`.

*Proof.* By definition, `Σ P_B (1 − μ) = (1 − π) − D`. Split `U` by entry: `U/Δ_T = ρ[(1 − π) − D] + G`. Off-path flows under NT have `μ = 1` in the buy-only profile, so `D = D_on + (1 − π) o`. Subtract `V/Δ_T = ρ(1 − π)(1 − o)`. ∎

For `λ = 1`, `D ≥ 0`: by Cauchy–Schwarz, `Σ P_H² / P_mix ≥ 1`, so `E_H[μ] = π Σ P_H² / P_mix ≥ π`. I do not use the sign of `D` for `λ < 1`.

Trade and no trade coexist when `U − V > 0` (and `k` lies between `V` and `U`). Two things are needed: an interior recruiting flow (`G > 0`) and little information loss on the flows that NT uses.

Checks (numerical diagnostic, `devices.out.txt`):

- Discrete Laplace buy-only, `c_H = 5`, `λ = 1`: `D_on = 0.0300`, `G = 0.1763`, `U − V = 0.1688`. The script gives `0.2938 − 0.1250`.
- Exclusive arrival, `λ`: `G = (1 − ρ)(1 − λ)/2`, `D = λ/2`, so `(U − V)/Δ_T = (1 − ρ − λ)/2`. At `λ = 0.46`, this is `0.145`. The script gives `0.2700 − 0.1250`.
- Three-point buy-only: `G = 0` (the only recruiting flow reveals), `D_on = 0`, and `U = V` exactly (A_three_point Result 4).

**(G6) Ceiling.** Let `M` be the essential supremum of `μ` over the flows of a trading class.

- If `M < 1`, entry equals `ρ` if and only if `τ(r) > M`, that is `r > r_C(M)`, where `B_r(M) = c_H`.
- If `M = 1`, entry exceeds `ρ` for every `r < r̄`. This holds even when `M = 1` is only a supremum: by the definition of the essential supremum, the flows with `μ ≥ τ(r)` have positive mass.

`M < 1` if and only if the density ratio `P_H / P_L` is bounded above on the support of `P_H`. This is the "bounded likelihood ratio". Only the bound in the direction of the recruiting class matters (see G7).

**(G7) Edge lemma.** Let noise be additive with support `[z_lo, z_hi]`, and let the two classes use orders `q_B > q_S`. Then:

- Flows in `(q_S + z_hi, q_B + z_hi]` are reached by class `B` only. If `z_hi` is finite, they have positive `P_B` mass and `μ = 1`. This holds for every presence `λ > 0`, because an absent investor adds only noise flows `≤ z_hi`.
- If `z_hi = +∞`, no flow reveals class `H`. Flows in `[q_S + z_lo, q_B + z_lo)` reveal class `L` (`μ = 0`). A buyer never meets them.

The lemma needs one premise: the order of class `S` is deterministic, or at least bounded by `q_S`. Suppose instead that class `S` can also place the order `q_B`. A liquidity trader in the order slot does this, because it buys one unit with positive probability under both classes. Then class `S` reaches `q_B + z_hi` too, and no flow is reached by class `B` only. This is why M4 escapes the lemma even with a bounded additive noise on top (§3.1, M4; lever T2, V1 and V2).

So the bounded edge matters on the side towards which the order pushes. Noise bounded below only, with a buy-only profile, does not stop the recruiting flow from being interior (M5, M11). A noise bounded above always does, when the other class cannot place the same order (M3, M10, M6). *Proof:* direct from the supports. ∎

**(G8) Reach of the low class.** In the two-sided profile `(+1, −1)`, class `L` earns `Δ_T Σ_x P_S(x) e(x) μ_x`, the residual of a seller. It profits from recruitment only if it reaches flows with `μ_x ≥ τ`. With bounded-above noise `z_hi` and `q_S = −1`, class `L` reaches flows `≤ z_hi − 1`. In the three-point model that is `x ≤ 0`, below every recruiting flow. So class `L` gains nothing from recruitment, and its payoff stays below its NT deviation payoff (numerical diagnostic, §3.3).

### 3.1 Properties matrix

Columns follow the task: (a) interior recruiting flow; (b) revealing flows and unused flows needing a belief; (c) likelihood-ratio bound and `M`; (d) order size; (e) tractability for a binary state, binary entry and the auction payoff; (f) typical results. All posteriors at `π = 1/2`, unit orders.

| ID | (a) Interior recruiting flow? | (b) Revealing flows; unused flows | (c) LR bound; `M` | (d) Order size | (e) Tractability | (f) Typical results |
|---|---|---|---|---|---|---|
| M1 Kyle, normal | Yes: `μ(x) = logistic(2qx/σ²)` at every finite flow | None; no unused flow | Unbounded; `M = 1`, not attained (soft ceiling) | Chosen and interior: price impact grows with `|q|` (score `−z/σ²` unbounded) | Logistic posterior; `Φ`-integrals; no clean global order bound | Unique linear equilibrium (Kyle; unverified); with feedback, self-fulfilling prices (A3; D §3.6) |
| M2 Noisy REE | Yes (normal) | None | Unbounded; `M = 1` unattained | Price taker; corner `±1` set by the bound (A3, D §3.8) | Very tractable; no strategic investor or cost `k` | DGG: unique if the risky project is optimal at the prior, else multiple (A3 #9); BGP: multiple or none (Q2) |
| M3 Three-point | Two-sided, `λ < 1`: flow `±1`, `μ_1 = 1/(2 − λ)`. Buy-only: no informative interior flow | Flows `±2` reveal (G7); under NT the flow 2 is unused: needs the Intuitive Criterion (Q2 C3) | LR `∞` at `±2`; `M = 1`, attained | Fixed unit by the menu; cost per unit | Finite sums; fully solvable (A_three_point) | Pure profiles NT, T, BNS, SNB; BNS and SNB coexist; asymmetric (EGJ) |
| M4 Exclusive arrival | Yes: buy flow has `μ = (1 + λ)/2` | None if the liquidity order can match the informed order. The abstention flow reveals the abstainer; it is irrelevant to incentives. Under NT every deviation flow is on path. With a separate three-point noise on top, the top flow is still interior in both classes (T2 §3.1) | Bounded: LR `= (1 + λ)/(1 − λ)`; `M = (1 + λ)/2` without noise. With noise: `μ(2) = (b + s)/(2b + s)`, `b = (1 − λ)β` (T2 eq. 6) | Fixed unit equal to the liquidity unit; another size would reveal the informed (unverified: Easley–O'Hara) | Three flows; closed forms | Dow–Gorton: informative and no-information equilibria (L1 C09); here BNS and NT coexist for `λ < 1 − ρ` (G5) |
| M5 One-sided exponential | Yes: for `d > q`, `μ = M` | Flows in `(0, q]` reveal "no purchase" (harmless, G7). No unused deviation flow | LR `e^{λ_e q}`; `M = 1/(1 + e^{−λ_e q})` | Chosen; closed form `β = min{1/λ_e, α}` (A6 #6) | Price constant on the pooled region (A6 #5): two prices | Nash equilibrium within the assumed structure (A6 #6); no D1 refinement stated |
| M6 Uniform noise | Only in the overlap of the two flow supports | For orders `±1` and support `[−1, 1]` every flow except 0 reveals (`U = 0`, §3.3) | `∞`; `M = 1` | BKT: unbounded order, mixed (A7 #3) | Tractable when the informed randomizes | BKT: unique positive-profit equilibrium if `c > χ̂` (A7 #9) |
| M7 Full-support, bounded score | Yes | None | `|(log f)'| ≤ 1/b` gives LR in `[e^{−2/b}, e^{2/b}]` for orders in `[−1, 1]` | Corner `±1` when `b > 1`, by the score bound (paper §2.3) | Analytical (paper A.5) | Prop. 2 for the whole class |
| M8 Laplace | Yes | None | `M = 1/(1 + e^{−2/b})` | Full order; class `L` sells partially (paper Prop. 3) | Closed forms; Prop. 3 computer-assisted | The paper's results |
| M9 Discrete Laplace | Yes | None | Buy-only: `M_1 = 1/(1 + a)`; two-sided: `M = 1/(1 + a²)` | Fixed unit | Half-line sufficiency; closed forms (B_dlaplace R1) | Prop. 2 and 3 analogs; two-sided matches the paper's `m, M, r_C` exactly (SYNTHESIS #6) |
| M10 `N` noise traders | Yes, near the top: `μ_x = x/(N + 1)` for `x = 1, …, N + 1` | Top flow `N + 1` reveals (mass `2^{−N}`); under NT it is unused | `∞` at the top; `M = 1`, attained | Fixed unit | Finite sums; no closed form in `N` | Not studied; §3.3 gives a fixed-profile diagnostic |
| M11 One-sided geometric | Yes: for `x ≥ 1`, `μ = 1/(1 + a)` | Flow 0 reveals "no purchase" (harmless) | `1/a`; `M = 1/(1 + a)` | Fixed unit | Two posteriors; trivial | Not studied; fixed-profile diagnostic in §3.3 |
| M12 Coarse observation | Yes, if the pooled set contains a flow that class `L` can reach | Pools the revealing flow with interior flows | Three-point buy-only, sign of the flow: LR 2, `M = 2/3` | Fixed unit | Trivial | Not studied. Two-sided three-point stays revealing: class `L` cannot reach `{1, 2}` |

Derivation notes for the cells.

- **M1.** Orders `±q`, noise `N(0, σ²)`: the density ratio is `φ(x − q)/φ(x + q) = exp(2qx/σ²)`. It is unbounded in `x`. The posterior is `logistic(2qx/σ²)`. It lies in `(0, 1)` at every finite `x` and tends to 1.
- **M3.** Flow laws are in A_three_point Result 1 (buy-only) and in Q2 C1 (two-sided). Two-sided profile `T`: `μ_1 = 1/(2 − λ)`, `μ_{−1} = (1 − λ)/(2 − λ)`, `μ_2 = 1`.
- **M4.** Under `T` (class `H` buys, class `L` sells): `P_H(+1) = λ + (1 − λ)/2`, `P_L(+1) = (1 − λ)/2`. So `μ_{+1} = (1 + λ)/2` at `π = 1/2`. With a liquidity no-order probability `ν`, `μ_{+1} = [λ + (1 − λ)(1 − ν)/2] / [λ + (1 − λ)(1 − ν)]`, which rises with `ν`.
- **M5.** Buy-only, class `H` buys one unit, noise `u > 0` with rate `λ_e`. For `d > 1`: `P_H(d)/P_L(d) = f(d − 1)/f(d) = e^{λ_e}`, constant. For `d ∈ (0, 1]`: `P_H = 0`. All of class `H`'s mass lies on `d > 1`.
- **M9, M11.** The geometric count has `f(x − 1)/f(x) = 1/a` for `x ≥ 1` (B_dlaplace Result 1(a)). One-sided geometric: for `x ≥ 1`, `P_H(x)/P_L(x) = (1 − a)a^{x−1} / ((1 − a)a^x) = 1/a`; at `x = 0`, `P_H = 0`.
- **M10.** Noise `B ~ Bin(N, 1/2)` buyers. A purchase shifts the flow by one, so `P_H(x)/P_L(x) = f(x − 1)/f(x) = x/(N + 1 − x)`, which tends to `∞` at `x = N + 1`.

### 3.2 Which result needs which device property (**analytical**, from G1–G8)

| Paper result | Needs | Source of the need |
|---|---|---|
| Prop. 2(i): NT at `r_0` | `P_B ≪ N`, or an off-path rule; `k ≥ ρ(1 − π)Δ_T` | G4 |
| Prop. 2(ii): trade with entry above `ρ` at `r_1` | `M ≥ τ(r_1)` and `G > 0`: a recruiting flow with `μ < 1` and positive mass | G1, G3 |
| Prop. 2(iii): entry back at `ρ` at `r_2`, trade informative | `M < τ(r_2)`, so `M < 1` | G6 |
| Prop. 3: NT and trade coexist | `G > ρ D_on`; both trading classes reach recruiting flows (two-sided) | G5, G8 |
| Prop. 3: strict upward entry order | Partial sales (continuous order size) or mixing; not available with unit orders | paper §4.3; SYNTHESIS row 5 |
| Prop. A.9: access to prices | Some recruiting flow with positive mass; it need not be interior (A_three_point Result 9) | G3 |
| Belief-free statements | Every flow reached by a deviation is on path | G4, G7 |

### 3.3 Scorecard (g): fixed-profile diagnostics at the benchmark (**numerical diagnostic**)

Script `devices.py`, output `devices.out.txt`. Each row fixes the informative profile (buy-only: class `H` buys, class `L` idle; two-sided: `H` buys, `L` sells). Entry is `ρ + (1 − ρ) × mass of flows with μ ≥ τ(r)`. It is the equilibrium entry only where that profile is an equilibrium. `c_H = 6` unless stated. `U` and `V` are in units of `Δ_T`.

| Method and parameters | `M` | Mass of `μ = 1` | Entry at `r = 3`, `3.6` | `r_C` | `U` | `V` | Reading |
|---|---|---|---|---|---|---|---|
| M8 Laplace `b = 2`, two-sided (paper) | 0.7311 | 0 | 0.523, 0.250 | 3.593 | 0.2111 | 0.1250 | all of Prop. 2 |
| M9 discrete Laplace, two-sided | 0.7311 | 0 | 0.569, 0.250 | 3.593 | 0.2278 | 0.1250 | all of Prop. 2 |
| M9 discrete Laplace, buy-only, `c_H = 6` | 0.6225 | 0 | 0.250, 0.250 | none | 0.1175 | 0.1250 | cap below `τ(3) = 0.705`: bounded, interior, recruits nobody |
| M9 discrete Laplace, buy-only, `c_H = 5` | 0.6225 | 0 | 0.625, 0.625 | 3.986 | 0.2938 | 0.1250 | Prop. 2 with `r_2 = 4.2` |
| M1 normal, variance 8, two-sided | 0.995 | 0 | 0.342, 0.318 | 7.9 (soft) | 0.1432 | 0.1250 | interior, no ceiling |
| M7 logistic, variance 8, two-sided | 0.7829 | 0 | 0.379, 0.340 | 4.663 | 0.1584 | 0.1250 | bounded, but the cap lies above `τ(3.6)` |
| M3 three-point, buy-only, `λ = 1` | 1 | 0.333 | 0.375, 0.375 | 7.969 | 0.0833 | 0.0833 | `U = V`: no feedback, no ceiling |
| M3 three-point, two-sided, `λ = 0.6` | 1 | 0.200 | 0.500, 0.325 | 7.969 | 0.1369 | 0.0833 | interior recruiting flow `x = 1`; `U_L = 0.0655` |
| M3 unequal weights `(.25, .5, .25)`, buy-only | 1 | 0.250 | 0.344, 0.344 | 7.969 | 0.0833 | 0.0938 | interior flow `μ = 2/3 < τ(3)` |
| M10 binomial `N = 8` noise buyers, buy-only | 1 | 0.004 | 0.317, 0.317 | 7.969 | 0.1319 | 0.1245 | feedback weak, no return |
| M10 binomial `N = 20` | 1 | ~0 | 0.279, 0.260 | 7.969 | 0.1304 | 0.1250 | soft decay, like the normal |
| M4 exclusive arrival, two-sided, `λ = 0.46` | 0.7300 | 0 | 0.625, 0.250 | 3.569 | 0.2700 | 0.1250 | all of Prop. 2; `U_L = 0.0675` |
| M4 exclusive arrival, `λ = 0.46`, `ν = 0.5` | 0.8151 | 0 | 0.524, 0.524 | 5.262 | 0.1849 | 0.1250 | no liquidity-order masking: cap too high |
| M11 one-sided geometric, `a = e^{−1}`, buy-only | 0.7311 | 0 | 0.763, 0.250 | 3.593 | 0.2689 | 0.1250 | the paper's cap and `r_C` exactly |
| M5 one-sided exponential, rate 1, buy-only | 0.7311 | 0 | 0.763, 0.250 | 3.593 | 0.2689 | 0.1250 | same as M11 |
| M6 uniform `[−1, 1]`, two-sided | 1 | 1 | 0.625, 0.625 | 7.969 | 0.0000 | 0.0625 | every informative flow reveals |
| M12 three-point buy-only, sign observed, `c_H = 5` | 0.6667 | 0 | 0.625, 0.625 | 5.025 | 0.2778 | 0.1250 | same cap as buy-only discrete Laplace |
| M4 slot + separate three-point noise, buy-only, `β = 1/3`, `λ = 6/17` | 0.7250 | 0 | 0.348, 0.250 | 3.458 | 0.1750 | 0.1250 | the top flow stays interior; matches T2 (`M = 29/40`, entry `71/204`, `r_C = 3.458`) |
| M4 slot, no noise, two-sided, `β = 1/3`, `λ = 6/17` | 0.7250 | 0 | 0.544, 0.250 | 3.458 | 0.2750 | 0.1250 | matches T2 V3 (entry `37/68`) |

Two-sided profile scan, M3 (`twosided_profiles.py`, pure profiles, `c_L = 0`, `c_H = 6`, `k/Δ_T` grid of 0.001). Equilibrium concept: Nash equilibrium of the investor's order game with Bayes-consistent beliefs and the Intuitive Criterion at flows that nobody reaches (`x > 0` gives `μ = 1`, `x < 0` gives `μ = 0`). Tie rules: the challenger prepares at indifference; the investor trades only if the payoff is strictly above zero:

- NT holds for `k/Δ_T ≥ 0.084` at every `λ ∈ {0.5, …, 1}` and both `r = 3` and `r = 3.6`. This is `ρ/3` (G4 with `o = 1/3`).
- Informative profiles hold only for `k/Δ_T ≤ 0.083`. At `λ = 0.6`, `r = 3`: `T` holds for `k/Δ_T ≤ 0.065`, BNS for `0.066 ≤ k/Δ_T ≤ 0.083`.
- **No pure informative profile coexists with NT** on this grid. BNS pays exactly `V` (Result 4), and `T` is limited by the low class (`U_L = 0.0655 < V_L = 0.0833`, G8). The sets touch only at the knife-edge `k/Δ_T = ρ/3`.

### 3.4 Test of the principle

The earlier study's principle: what matters is (i) an interior posterior at the recruiting flow and (ii) a bounded likelihood ratio. I tested each part separately.

**(i) Survives, in a sharper form (analytical, G1 and G5).** Feedback exists if and only if some recruiting flow has `μ < 1` and positive mass: `G > 0`. Evidence: `U = V` exactly for three-point buy-only (`G = 0`); `U = 0` for uniform noise; `U − V = G − ρ D_on` in every row of §3.3. Interior recruitment alone does not give `U > V`: normal buy-only has `U = 0.1235 < V = 0.1250` (see Refinement 3).

**(ii) Survives for exact return; interior alone does not give it (analytical, G6; numerical diagnostic).** The normal case has (i) without (ii). Every flow is interior, yet entry at `r = 3.6` is 0.318, not 0.250, and the ceiling is soft (`r_C ≈ r̄`). Binomial `N = 20` shows the same soft decay. This agrees with B_dlaplace Result 12A (discretized normal: entry 0.255 at `r = 6`).

**Refinement 1: boundedness is not enough; the cap must fall in a window (analytical, G3).** Prop. 2(ii) and 2(iii) together need `τ(r_1) ≤ M < τ(r_2)`. At the benchmark this is `[0.7050, 0.7314)`, a width of 0.026. Three bounded devices miss it:

- buy-only discrete Laplace at `c_H = 6`: `M = 0.6225`, below the window, so the high-cost type never prepares;
- logistic at variance 8: `M = 0.7829`, above it, so `r_C = 4.66 > 3.6`;
- exclusive arrival with `λ = 0.46` and liquidity no-order probability `ν = 0.5`: `M = 0.8151`, so `r_C = 5.26`.

The paper's benchmark sits at the upper edge of the window by construction: `b = 2` gives `M = 0.7311` and `r_2 = 3.6` is just above `r_C`. For any other device the smallest move is to retune the knob that sets `M`, or to move `r_2` above its `r_C` (as the earlier study did with `r_2 = 4.2`).

Cross-check with lever T2 (analytical). With a liquidity buy probability `β` per direction and no separate noise, `μ_{+1} = [λ + (1 − λ)β] / [λ + 2(1 − λ)β]`. At `β = 1/3` this is `(2λ + 1)/(λ + 2)`. The window `τ(3) = 141/200 ≤ (2λ + 1)/(λ + 2) < τ(3.6)` gives `λ ∈ (82/259, 2686/7363)`, which is T2's strip (T2 §4, V3 buy). The knob `λ` moves `M` through the window exactly as the principle says.

**Refinement 2: one-sided boundedness suffices (analytical, G7).** Only `sup P_H / P_L` on the buyer's flows must be bounded. A revealing flow for class `L` is harmless. Noise with a hard edge on the side opposite the order (M5, M11) gives exactly the paper's `M` and `r_C` (table above). So the brief's statement "any noise of bounded support has a revealing top flow" is true for noise bounded in the direction of the order. It is false for noise bounded only on the other side. It is also false for M4, where class `L` can place the same order as class `H` (premise of G7). Adding three-point noise on top of M4 keeps `M < 1`.

**Refinement 3: coexistence needs more than (i) and (ii).** Analytical (G5, G8): coexistence needs `G > ρ D_on`, and in the two-sided menu both classes must reach the recruiting flows. Numerical diagnostic (`twosided_profiles.py`): three-point two-sided with `λ ∈ [0.58, 0.86]` has an interior recruiting flow (feedback exists), yet the pure scan finds no coexistence. In M4 the two-sided profile `T` has the same problem for class `L` (`U_L = 0.0675 < V_L`), but the buy-only informative profile (BNS) coexists with NT because the liquidity buyers, not class `L`, supply the mass at the recruiting flow (§5).

**Refinement 4: the right object is non-revelation of the investor's information (analytical).** Under Reading N the investor's posterior is 0 or 1, so "interior" and "does not reveal the investor's information" coincide. If the investor held only a signal of precision `φ < 1` (Edmans 2009; DGG), a flow that reveals the signal has an interior state posterior `φ`. The residual there is still zero, because the market maker then knows what the investor knows. Interiority of the state posterior would then be necessary but not sufficient. This does not affect the paper (Reading N), but it blocks one tempting repair: imperfect signals do not cure a revealing top flow.

**Refinement 5: an inherited stake bypasses (i) (analytical from C5; SYNTHESIS §1 claim 12).** A holder gains from entry through the stake, not through the trading residual. The paper gives the investor no stake, so this does not apply.

**What would refute the principle.** Any of these would:

- a device with a revealing flow of positive mass that still gives exact return at some `r_2 < r̄` with trade informative;
- a device with `G = 0` that still gives `U > V`;
- an additive device whose noise support is bounded in the direction of the order, with `M < 1`.

I found none. The edge lemma (G7) shows the last cannot occur.

## 4. Conventionality
Counts come from `L1_survey.md` §3: 15 corporate-decision models (C01–C15) with inspected model passages. I map its classes onto my methods. The sample is purposive. It is not a frequency estimate, and L1 says so.

| Method | Count | Papers (L1 id) | Standing |
|---|---:|---|---|
| M1 Kyle-type, normal | 3 | Holmström–Tirole 1993 (C10); Edmans–Manso 2011 (C12); Back et al. 2018 (C14) | Common. Kyle (1985) is the base the pinned paper cites |
| M2 Noisy REE, normal shock | 3 | Bond–Goldstein 2015 (C07); GOY 2013 (C08); Ozdenoren–Yuan 2008 (C15) | Common. L1 counts normal shocks in 7 of 15 models, through different mechanisms (C03 DGG also uses normal noise) |
| M3 Three-point, additive | 2 | EGJ 2015 (C01); Goldstein–Guembel 2008 (C02) | Closest to the author's "EGJ-like" request. Both ask which direction of trade survives or whether sales manipulate. Neither needs a ceiling |
| M4 Exclusive arrival, same size | 1 as a class; 4 with relatives | Dow–Gorton 1997 (C09): informed and liquidity arrivals of size `x` are perfectly negatively correlated. Relatives: BKT (C05, identities), Admati–Pfleiderer (C11, shock forces the same sale), Faure-Grimaud–Gromb (C13, same-size orders) | As common as M3 in this sample. L1 §5.4 verifies why size matches: other trade sizes can reveal the informed (Admati–Pfleiderer fn. 10). Glosten–Milgrom and PIN stay abstract-level (L1 M02, M04) |
| M5 One-sided exponential | 1 | Edmans 2009 (C04), with a stated tractability reason (A6 #8) | One use |
| M6 Uniform | 0 | BKT working paper only (Q2); the 2017 version has general densities | None in selected versions |
| M7 General full-support | 1 | BKT 2017 (C05) | One use; no named law |
| M8 Laplace | 0 | Friedrich–Teichmann 2020: numerical, not corporate (C13 in LIT_extracts) | Unconventional, as the author says |
| M9–M12 | 0 | none | New |

Three readings follow.

- Normal noise is the default family. Discrete finite-noise models are rare (EGJ, GG).
- The device that lets an informed order take the place of a same-size liquidity order is at least as established as the three-point additive model: four models (C05, C09, C11, C13) use some form of it. Only one of the four (C09) is a pure exclusive-arrival model.
- L1 §5.6 finds no verified source that recovers this paper's pattern with "wider bounded noise" or random order size. The edge lemma (G7) explains why bounded additive noise cannot.

## 5. Short-list and predictions for T1–T3

### 5.1 Short-list

The design target is a device that (1) lands `M` in `[τ(r_1), τ(r_2))`, (2) keeps an interior recruiting flow, and (3) keeps `G > ρ D_on`. Ranked by that target and by standing:

1. **Exclusive arrival with a liquidity order of the informed size (M4; lever T2).** It gives `M = (1 + λ)/2`, a bounded ratio, and a knob that sets `M` alone. Reasons:
   - The deviation flow from NT is on path. So Prop. 2(i) needs no belief, the cutoff is the paper's `k ≥ ρ(1 − π)Δ_T`, and `r_N = 1.7479` as in the paper (G4).
   - The buy-only informative profile (class `H` buys, class `L` idles) coexists with NT for `ρΔ_T/2 ≤ k < (1 − M)Δ_T` (G5, numerical check in §3.3). It needs `λ < 1 − ρ = 0.75` and `λ ≥ 2τ(r_1) − 1 = 0.410`. At `k = 0.02` and `λ = 0.46` this covers `r ∈ (1.47, 1.75]`, which contains 1.55–1.65.
   - Prop. 2(ii) and 2(iii) together at the benchmark strengths need `0.410 ≤ λ < 2τ(3.6) − 1 = 0.463`. This window is narrow, as G3 says. At `λ = 0.4621`, `M = 0.7311` and `r_C = 3.593`, the paper's value.
   - It survives EGJ's own noise on top (T2 variants V1 and V2: three-point noise and a slot trader). The top flow is then interior in both classes, because a liquidity buy plus a noise buy gives flow 2 in class `L` too (G7 premise). My independent computation reproduces T2's numbers at `β = 1/3`, `λ = 6/17`: `M = 29/40`, `r_C = 3.458`, entry 0.348 at `r = 3` and 0.250 at `r = 3.6` (§3.3). This keeps EGJ's menu and noise and adds only the slot device. It strengthens the EGJ-like standing of the device. The cost is a lower entry level (0.348, against 0.523 in the paper) and, in T2's results, a coexistence interval that starts at 1.5566 and so excludes 1.55.
   - Standing: four models in the records use a form of it, one of them (Dow–Gorton) as a pure exclusive arrival with a corporate decision. `λ` plays the role of Dow–Gorton's research success probability, and relates to PIN (unverified).
   - Costs: unit orders only, so no partial sales and no strict upward entry order; flat entry across informative equilibria; the informed order size must equal the liquidity size; the informed payoff coefficient is `1 − M`, so thresholds differ from the discrete Laplace base even when posteriors coincide.
2. **Buy-only with noise unbounded in the direction of the order (M5; discrete form M11).** It gives the paper's `M` and `r_C` exactly at `a = e^{−1}` (rate 1), with `U = 1 − M` and two prices. Reason: the edge lemma. It has a verified corporate-finance precedent with a tractability argument (Edmans 2009, A6 #8). Costs: noise that only buys is a restrictive assumption (Edmans allows a downward shift of the law); sells need a mirror device; M11 has no precedent. T3 does not cover this lever. I flag it to the coordinator.
3. **Coarse observation of the flow (M12), buy-only.** It keeps EGJ's own noise and menu and changes only what the market and the challenger see. It gives `M = 2/3`, which needs `c_H` near 5. It does not help the two-sided menu, because class `L` cannot reach the pooled flows. It has no precedent in the records. It is the weakest on standing.

The discrete Laplace companion (M9) is the bar, not a short-list item. T1's two-sided EGJ menu is not on the short-list: it delivers feedback but not the ceiling.

### 5.2 Predictions for T1–T3 if the principle is right (**conjecture**, grounded in G1–G8 and §3.3)

I drew up the first version of these predictions before I read T1 and T2. T1 was a skeleton. T2's memo then refuted one prediction: I had written that three-point noise added on top of the slot device brings back a revealing top flow. That was a wrong application of the edge lemma (the premise in G7 fails when class `L` can place the same order). I corrected G7 and the T2 row. The principle itself held: it predicted the pattern T2 found, once the lemma was applied correctly.

| Lever | Interior recruiting flow (i) | Bounded ratio (ii) | What it should find | What would refute me |
|---|---|---|---|---|
| **T1** two-sided `{−1, 0, 1}`, three-point noise, `λ < 1` (equal or symmetric non-uniform weights) | Yes: flow 1 has `μ_1 = 1/(2 − λ)` and recruits if `λ ≥ 2 − 1/τ(r)`, about 0.58 at `r = 3` | No: flows `±2` reveal for every `λ > 0` and every symmetric weighting | Prop. 2(i): NT iff `k ≥ ρΔ_T/3`. Prop. 2(ii): informative trade with entry 0.325 (BNS, `λ = 0.6`) to 0.500 (T), against 0.523 in the paper. Prop. 2(iii) fails at 3.6: for `λ` below 0.63 the interior flow stops recruiting and entry is `ρ + 0.125 λ` (0.325 at `λ = 0.6`); for larger `λ` it stays at 0.50. Return only above `r̄ = 7.97`. Prop. 3: no coexistence in pure profiles, only a knife-edge at `ρ/3`; at most a mixed branch. Class `L` cannot reach the recruiting flow (G8) | Exact return at `r_2 = 3.6`, or strict coexistence in pure profiles |
| **T2** liquidity or uninformed trader of the informed size | Yes: `μ_{+1} = (1 + λ)/2` | Yes, with or without separate three-point noise: class `L` can place the slot's liquidity order, so the top flow is interior. Without noise `M = (1 + λ)/2`; with noise `μ(2) = (b + s)/(2b + s)` | All of Prop. 2(i)–(iii) on a narrow `λ` strip (above), with or without separate noise. NT cutoff `ρΔ_T/2`. Coexistence with NT in the buy-only profile, flat entry. Separate noise lowers entry at 3 (0.348 against 0.544) and shifts the coexistence interval up | A revealing top flow, or no return at `r_2 = 3.6`, with the slot device |
| **T3** buy-only, bounded-noise variants | Possible: strongly unimodal weights give flow 1 a posterior above `τ`; `N` noise traders give interior flows near the top | No: the top flow (`x = 2`, or `N + 1`) reveals | Feedback and, with unimodal weights and `c_H` near 5, narrow coexistence (C9 found a window of width 0.014). No exact return: entry at 3.6 is 0.375 (three-point), 0.344–0.400 (unequal weights), 0.317 (binomial `N = 8`). Large `N` turns the failure into a soft decay (0.260 at `N = 20`) with weak feedback (`U − V = 0.005`). Two-unit orders are worse: they widen the revealing region. Presence `λ` changes nothing: the top flow reveals for every `λ > 0` | Exact return with a revealing flow of positive mass |

If T1 or T3 finds exact return, the edge lemma G7 or the return condition G6 is wrong, and I should recheck both. (T2's result with separate noise did not refute G7 once its premise is checked.)

## 6. Verification requests

Each line gives the paper, the claim I used, and where to look. All are **unverified**. I used none as evidence for a result; they support only the standing statements in §2–§5.

1. Glosten and Milgrom (1985, *Journal of Financial Economics*): unit-size orders, fixed liquidity buy and sell probabilities, quotes equal to conditional expectations. Look at the model section. L1 holds an abstract only (M02).
2. Easley, Kiefer, O'Hara and Paperman (1996): the PIN formula, and whether `λ` in M4 maps onto it. Look at the model section. L1 holds an abstract only (M04).
3. Kyle (1985, *Econometrica*): the linear equilibrium with normal noise and a chosen order size (row M1, column (f)). The pinned paper cites it. L1 holds an abstract only (M01).
4. Kyle and Vila (1991): the noise law and order menu. The records hold an abstract only (A4).
5. Khanna and Sonti (2004): sequential traders with inventory. The records hold an abstract only (A5).
6. Diamond and Verrecchia (1987): informed traders barred from short sales. Listed as unverified in Q2.
7. Smith and Sørensen (2000): bounded private beliefs. The pinned paper cites it for "no flow is conclusive"; I used only the citation.
8. BKT working paper: uniform `[−1, 1]` noise (Q2 table, footnote 6). The published version (A7) has general densities. Confirm which version Q2 read.

Count: 8 requests.

## 7. Plain summary

The records show four trading set-ups in models with a corporate decision. Most use normal noise, either with a strategic trader or with price takers. EGJ and Goldstein–Guembel use three-point noise. Dow–Gorton and Boleslavsky–Kelly–Taylor let an order be informed or a liquidity order of the same size. Edmans uses one-sided exponential noise. The Laplace law has no corporate precedent.

Four facts decide which set-up gives the paper's results. The recruiting flow must leave the investor a positive residual. No flow with positive mass may reveal the class, or entry never returns to its floor below strength 7.97. The highest posterior must lie in a narrow window set by the auction: 0.705 to 0.731 at the benchmark. For coexistence, the recruiting gain must exceed the information loss on the flows that no trade uses.

Bounded noise on the side of the order always breaks the second fact, so the three-point model fails. Noise bounded only on the opposite side does not. One-sided exponential or geometric noise reproduces the paper's cap and ceiling exactly. An order slot that a same-size liquidity trader can fill also does, with or without EGJ's noise on top. Its knob is the probability that the slot is informed.

The earlier principle holds, with four refinements: a window for the cap, a one-sided bound, a coexistence condition, and non-revelation as the right object.

Short-list: exclusive arrival, one-sided noise, coarse observation. T1 should find feedback but no return. T3 should find no return. T2 finds the full pattern, with or without separate noise.
