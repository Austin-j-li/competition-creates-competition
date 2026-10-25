# W5-symmetry-tests: Solver B

Scope read: `appendix/A8_empirical.tex` (A.11 to A.14, the full-trade paragraph, the two-cluster paragraph), `sections/08_empirical.tex`, `appendix/A2_beliefs_trading.tex` (Lemmas A.1 to A.3), `appendix/A1_payoffs.tex` (the payoff integrals), `sections/02`–`04`, Corollary A.2 in `appendix/A4_coexistence.tex`, SCAN.md and the Solver A report rows for A8. Every identity below was checked numerically at 30 digits (scripts in `audit/theory_upgrade_2026_10_25/solvers/computations/W5_B/check1.py` to `check8.py`). The benchmark slot is β = 294655/10⁶, 1 + u = e, so λ = 0.336122, b = 0.195615, b₀ = 0.272648, M(1/2) = 0.731059.

Notation used throughout. Under full two-sided trade (σ_H = δ₁, σ_L = δ₋₁) at a prior π, write ν₊ = Pr(X = 1) = b + πλ, ν₋ = Pr(X = −1) = b + (1 − π)λ, v = ν₊ + ν₋ = 2b + λ, and A(μ) = A_F(μ) = w_L + Δμ with w_L = t_L − t₀ (the paper's A_r, the w(μ) of A2). Posteriors are (m, π, M) = (m(π), π, M(π)). With π < τ (gross profit at the prior below c_H), entry is (ρ, ρ, e₊) with e₊ = ρ + (1 − ρ)χ and χ = 1{M ≥ τ} under rule C1.

---

## Candidate 1: "No news is bad news": the count-weighted impact test

Angle: reformulate.

Intuition: Under full two-sided trade both classes reach the zero order only through the liquidity trader, so an opportunity that passes with no order says nothing about the class. If no order recruits, every price is ρ times an affine function of the posterior, and the posterior is a martingale; so the expected price after the opportunity equals the price after no order, and the purchase and sale impacts, each weighted by the frequency of its order, balance exactly at every prior. A recruiting purchase adds entry after the purchase only, so the price after no order falls short of the expected price by the probability of a purchase times the recruitment gain. At the prior 1/2 the two frequencies are equal, which is why the paper's raw comparison I₊ > I₋ works there and only there.

Formal statement (a prior-free replacement for A.11 and A.14(iv)). Take ranked classes, a continuous F with Δ(F) > 0 and g_H > g_L, any prior π ∈ (0, 1) and any slot, and an equilibrium at F with full two-sided trade and π < τ(F). Then:

1. S = P(1) − P(−1) = ρΔ[M − m] + (1 − ρ)χA(M): a class component and an entry component.
2. ν₋·I₋ = ρΔ·π(1 − π)λ and ν₊·I₊ = ρΔ·π(1 − π)λ + (1 − ρ)χ·ν₊A(M). Hence

   E[P(X)] − P(0) = ν₊I₊ − ν₋I₋ = (1 − ρ)χ·ν₊·A(M),

   so the count-weighted purchase impact exceeds the count-weighted sale impact, equivalently an order opportunity that passes with no order lowers the price, if and only if a purchase recruits. The two components are observable from prices and counts: entry component = I₊ − (ν₋/ν₊)·I₋, class component = (v/ν₊)·I₋.
3. If the challenger does not see the price, ν₊I₊ = ν₋I₋ and S equals the class component.
4. (Completion.) If instead m < τ ≤ π, so the prior alone recruits and a sale deters, E[P(X)] − P(0) = −(1 − ρ)ν₋A(m) < 0. If entry does not depend on the order, it is zero.
5. Under rule CM at M = τ, replace (1 − ρ)χ by e(1) − ρ: the difference is positive exactly when e(1) > ρ.

At π = 1/2, ν₊ = ν₋ = b + λ/2, so part 2 is A.11(ii) multiplied by b + λ/2, and the middle expression is A.14(iv). The paper's two tests are one result.

Derivation.
- Bayes plausibility. f_H = (b, b₀, b + λ) and f_L = (b + λ, b₀, b) on (−1, 0, 1). Then M = π(b + λ)/ν₊, so M − π = π[(b + λ) − ν₊]/ν₊ = π(1 − π)λ/ν₊. Likewise m = πb/ν₋ and π − m = π(1 − π)λ/ν₋. Hence

  ν₊(M − π) = ν₋(π − m) = π(1 − π)λ. (★)

  In closed form, M − π = π(1 − π)u/(1 + πu) and π − m = π(1 − π)u/(1 + (1 − π)u), and (M − π) − (π − m) = π(1 − π)u²(1 − 2π)/[(1 + πu)(1 + (1 − π)u)], which is the prior term the brief flags; it has the sign of 1 − 2π.
- Prices (Lemma A.2(b)). With e(−1) = e(0) = ρ: I₋ = ρ[A(π) − A(m)] = ρΔ(π − m), and I₊ = e₊A(M) − ρA(π) = ρΔ(M − π) + (e₊ − ρ)A(M). Multiply by ν₋ and ν₊ and use (★): ν₊I₊ − ν₋I₋ = ν₊(e₊ − ρ)A(M).
- The identity E[P(X)] − P(0) = ν₊[P(1) − P(0)] + ν₋[P(−1) − P(0)] = ν₊I₊ − ν₋I₋ holds for any prices.
- Sign. A(M) = w_L + ΔM > 0, because w_L ≥ 0 (A1: entry never lowers second-price proceeds), Δ > 0 and M > 0. So the difference is positive iff e₊ > ρ.
- Components. By (★), (π − m)/(M − m) = (1/ν₋)/(1/ν₊ + 1/ν₋) = ν₊/v. So I₋ = ρΔ(M − m)·ν₊/v gives the class component; subtracting it from S gives the entry component I₊ − (ν₋/ν₊)I₋.
- Part 4. With e = (ρ, 1, 1): I₋ = Δ(π − m) + (1 − ρ)A(m) and I₊ = Δ(M − π); by (★) ν₊I₊ − ν₋I₋ = −(1 − ρ)ν₋A(m).
- The floated "prior-adjusted benchmark" is the same test. Without recruitment, ρΔ[(M − π) − (π − m)] = I₋[(M − π)/(π − m) − 1] = I₋(ν₋/ν₊ − 1) by (★). So comparing I₊ − I₋ with the brief's ρΔ{[M − π] − [π − m]}, or comparing I₊/(M − π) with I₋/(π − m), is the count-weighted test, and the counts make it computable without ρ, Δ, u or π.

Conditions.
- Full two-sided trade, used through μ(0) = π. The test fails off this pattern: with purchases only (σ_H = δ₁, σ_L = δ₀) and no recruitment, μ(0) < π and E[P(X)] − P(0) = ρΔ[π − μ(0)] > 0 (check5: 0.0993 at π = 1/2, r = 6). The paper's raw test has the same restriction, so nothing is lost here.
- π < τ(F), i.e. B_F(π) < c_H, for part 2 as stated; part 4 covers the other case.
- Unique full trade holds wherever ρκ(π)Δ(F) > k (Lemma A.3(c), the A.11 argument with m(π) and 1 − M(π) in place of m). This domain shrinks as π moves away from 1/2.

Benchmark check.
- π = 1/2, r₁ = 3: ν₊ = ν₋ = 0.363676; entry component 0.709279 (registry `ba_entry_r1_B`); 0.363676 × 0.709279 = 0.257948 = P̄ − P(0) (registry `pbar_r1_B − p_neutral_r1_B` = 0.872531 − 0.614583).
- π = 0.4, r = 3.6, full trade without recruitment (K_L − k = 0.026): raw I₊ − I₋ = +0.00971, 20% of I₋, while ν₊I₊ − ν₋I₋ = 0 to 30 digits.
- π = 0.6, r = 3.6, recruiting: ν₊I₊ − ν₋I₋ = 0.36330 = ν₊(1 − ρ)A(M); the raw difference 0.90473 contains the prior term −0.00971.
- π = 0.75, r = 3 (τ = 0.705 ≤ π): −0.16948 = −(1 − ρ)ν₋A(m).
- Lower end of the unique full-trade interval at the benchmark slot: r_S(π) = 2.124 (π = 1/2), 2.200 (π = 0.4679), 2.395 (π = 0.4 or 0.6), 2.820 (π = 0.3).

What is lost.
- The raw test compares three prices. The corrected test also needs the purchase-to-sale frequency ratio ν₋/ν₊ from the same population of processes, or the price before the opportunity. The model has no market before the slot; reading the pre-opportunity price as E[P(X)], the competitive price before the slot, is the paper's own interpretation in A.14(iv). The measurement design of §8 already records the zero order, so the data are the same.
- Pooling across processes with different priors needs weights cell by cell. The no-order-return form needs none, provided every cell has full trade and π < τ. Under the null of no recruitment, P(0) then equals E[P(X)] in every cell, whatever its prior, so the mean return over no-order processes is zero, and it is negative when some cells recruit. A cell with π ≥ τ > m would contribute a positive return (part 4).
- "The sale impact contains half of the class component" becomes "the sale impact contains the share ν₊/v of it". The rarer order moves the price more.
- Nothing is lost at π = 1/2.

Extension (a test that also drops the full-trade pattern, if winner data are available). The win rate of prepared challengers after order x is w_x = W_L + (W_H − W_L)μ(x) (cost independent of class; A.13(i) generalized). Without recruitment, P(x) = t₀ + ρ(w_L + Δμ(x)) is also affine in μ(x), so the three points (w_x, P(x)) lie on one line. A recruiting purchase lifts (w₁, P(1)) above the line through the other two by exactly (1 − ρ)A(M). This needs W_H > W_L and distinct posteriors at the two lower orders, but neither full two-sided trade nor the prior.

---

## Candidate 2: what counts and prices identify at any prior

Angle: reformulate (this is the better identification result the brief asks about).

Intuition: Counts see the informed investor only through the order imbalance, and the imbalance is the informed presence times the prior's tilt toward the high class, λ(2π − 1). At the symmetric prior the imbalance is zero whatever λ is, which is why the paper finds that counts cannot see the informed share; at any other known prior the imbalance reveals λ directly. Prices add a separate moment: by (★), the count-weighted sale impact equals ρΔ times the informed presence times the class variance π(1 − π). With Δ known, the two moments pin down both λ and π; with π known, they pin down Δ, so the stock price then measures the target-payoff spread.

Formal statement. Full two-sided trade at F with π < τ(F) (so neither a sale nor no order recruits); ρ is read from the preparation rate after a sale, as in A.12(d).

- (a) Counts. ν₊ = b + πλ and ν₋ = b + (1 − π)λ. So the order law depends on (π, λ, β) only through the volume v = 2b + λ and the imbalance E[X] = λ(2π − 1); equivalently E[X]/v = ϑ·(2π − 1), with ϑ = λ/v the informed share of nonzero orders.
  - At a known prior π ≠ 1/2, the counts identify the slot: λ = E[X]/(2π − 1), b = (v − λ)/2, β = b/(1 − λ).
  - At an unknown prior, every pair (π′, λ′) with λ′(2π′ − 1) = E[X], 0 < λ′ < v and b′/(1 − λ′) ≤ 1/3 gives the same counts. These pairs also give the same entry wherever their recruitment status agrees, since entry is ρ + (1 − ρ)χν₊ and ν₊ = (v + E[X])/2 is fixed; that status must be checked member by member.
  - When E[X] = 0, as at the benchmark, this set is {π′ = 1/2} × {every share with volume v}. That is exactly A.12(a). So the paper's nonidentification is the balanced-order-flow case of a general confounding between the informed share and the prior.
- (b) Prices. ν₋·I₋ = ρΔ·π(1 − π)λ.
- (c) Identification. Given Δ, put Q = ν₋I₋/(ρΔ) = π(1 − π)λ. Then λ = 2Q + √(4Q² + E[X]²), π = (1 + E[X]/λ)/2, b = (v − λ)/2 and β = b/(1 − λ). Given instead a known prior π ≠ 1/2, the counts give λ and b, and the sale impact gives the spread: ρΔ = ν₋I₋/[π(1 − π)λ].
- (d) Where a purchase recruits, the entry component of Candidate 1 gives A(M) = [I₊ − (ν₋/ν₊)I₋]/(1 − ρ), and then the low-class entry gain t_L − t₀ = A(M) − ΔM.
- The prior 1/2 is the only prior at which knowing the prior adds nothing to the counts. Near it, identification from counts is weak: dλ/dE[X] = 1/(2π − 1).

Corollary A.3 at a general prior. With σ_H = δ₁ and σ_L = δ₀: ν₋ = b and E[X] = π·s₊, where s₊ = λσ_H(1). So b = Pr(X = −1) at every prior (the printed b = (v − E[X])/2 is the same number). In form F, λ = E[X]/π at a known prior (the printed λ = 2E[X] is the case π = 1/2). On branch R, s₊ = E[X]/π, and λ stays unidentified. At an unknown prior the counts identify b and π·s₊ only.

Derivation.
- (a): subtract and add ν₊ and ν₋.
- (b): (★) multiplied by ρΔ, with I₋ = ρΔ(π − m).
- (c): E[X]² + 4λQ = λ²[(2π − 1)² + 4π(1 − π)] = λ², so λ solves λ² − 4Qλ − E[X]² = 0, and its positive root is the one displayed. The sign of 2π − 1 is the sign of E[X].
- Corollary: f_H(1) = b + s₊, f_L(1) = b and f_j(−1) = b give ν₊ = b + πs₊ and ν₋ = b.

Conditions. Full two-sided trade with m < τ and π < τ, so that I₋ = ρΔ(π − m); λ > 0. Part (c) needs one of Δ or π, the same kind of outside knowledge as A.12(d), which needs both Δ and π = 1/2. The incentive and band parts A.12(b)–(c) carry over once m(π) and M(π) replace (1 − ϑ)/2 and (1 + ϑ)/2: full trade needs ρΔm′(π) ≥ k and e₊Δ[1 − M′(π)] ≥ k, with m′(π) = π(1 − ϑ′)/[1 − (2π − 1)ϑ′].

Benchmark check.
- At π = 1/2: E[X] = 0, Q = λ/4 = 0.084030 and λ = 4Q = 0.336122, which is A.12(d).
- Same-counts family for data generated at π₀ = 0.6, the benchmark slot and r = 3: the pairs (π′, λ′, β′) run from (0.56, 0.560, 0.190) to (0.65, 0.224, 0.324). β′ exceeds 1/3 beyond π′ = 0.6846. Every member has unique full trade at r = 3 and at r = 3.6 (smallest margin K_L − k = 0.0036, at π′ = 0.56 and r = 3) and recruits at both strengths. Their sale impacts I₋ at r = 3 run from 0.0697 to 0.0257, so prices separate members that counts cannot.
- The known-prior inversion and the Δ-known inversion recover (λ, β, ρΔ) and (λ, π, β) to 30 digits at π ∈ {0.3, 0.45, 0.5, 0.62} and r ∈ {3, 3.6, 5}.

What is lost. The clean A.12(a)/(c) message, "counts cannot see the informed share", survives only when E[X] = 0 or the prior is unknown, and then as a statement about (prior, share) pairs. At a known prior other than 1/2 it is false. The slogan "prices separate slots that order counts cannot" then becomes "counts identify the slot, and prices identify the spread". The benchmark numbers in A.12(b)–(c), the interval [0.250299, 0.76], are prior-1/2 numbers.

---

## Candidate 3: primitive conditions that keep the original claims

Angle: primitive condition.

Intuition: The raw comparison I₊ > I₋ goes wrong only because the prior makes one order rarer, and so more informative, than the other. If the prior does not favor the low class, the purchase is the more frequent and less informative order, so absent recruitment the purchase impact is the smaller one, and a recruiting purchase must overcome that. The entry-component trend needs the target's gain from entry to grow with strength, which fails only when a stronger incumbent mainly stops failing the reserve. Positive announcement returns need only that the prior alone does not recruit a high-cost challenger.

Formal statement.

1. Raw test (A.11(ii)). Under full two-sided trade with π < τ and Δ > 0: if π ≥ 1/2 and ρ ≤ 1/2, then I₊ > I₋ if and only if a purchase recruits. Economic reading: the prior does not favor the low class, and a ready buyer is no more likely than a costly one. π ≥ 1/2 is necessary whenever some full-trade incumbent has no recruitment (at the benchmark, (r_C, h)). For π < 1/2, I₊ > I₋ at every full-trade incumbent, with or without recruitment.
2. Trend of the entry component (A.11(iv)). Along a continuous FOSD path F_s, the entry component (1 − ρ)A_{F_s}(M), I₊ and S rise wherever A_{F_s}(M) rises. A sufficient condition with economic meaning: the target's gain from a low-class entrant, t_L − t₀, does not fall along the path. Then A(μ) = w_L + μΔ rises for every μ, strictly where Δ rises strictly. This holds whenever the probability that the incumbent fails the reserve, F_s(p), is the same along the path, in particular when every incumbent on the path meets the reserve. For a location family F_s(y) = F(y − s), the exact local condition is

   p·f_s(p) ≤ Pr(p < R < θ), with R ~ F_s and θ ~ G_M:

   the reserve times the density at the reserve must not exceed the probability that the challenger beats an incumbent who meets the reserve. For the benchmark family (uniform incumbents, point masses), w_L(r) = (ℓ − p) − (ℓ² − 3p²)/(2r) rises iff ℓ ≥ √3·p, and A_r(M) rises iff ℓ² − 3p² + M(r² − ℓ²) > 0.
3. Announcement returns (A.14(iii)). At any prior, if Δ > 0 and B_F(π) < c_H, the mean price change in a sample of preparation reports is positive in every equilibrium. A.14(iv) holds at every prior with b + λ/2 replaced by b + πλ (Candidate 1, part 2). A.14(i)–(ii) need nothing.

Derivation.
1. By Candidate 1, I₊ − I₋ = ρΔ[(M − π) − (π − m)] + (1 − ρ)χA(M), and the first term has the sign of 1 − 2π. Without recruitment the sign is that of 1 − 2π, which gives necessity and the π < 1/2 failure. With recruitment, I₊ − I₋ ≥ −ρΔ(π − m) + (1 − ρ)(w_L + ΔM) > −ρΔM + (1 − ρ)ΔM = (1 − 2ρ)ΔM ≥ 0, using M − π > 0, π − m < M and w_L ≥ 0. The exact requirement is (1 − ρ)A(M) > ρΔ[(π − m) − (M − π)], so ρ ≤ 1/2 is far from necessary. A failure needs ρ well above 1/2 and a negligible w_L: with w_L = 0, π = 0.9, u = 20 and ρ = 0.8, (1 − ρ)M = 0.199 < ρ[(π − m) − (M − π)] = 0.404.
2. A1 gives t_j = t₀ + pF(p) + ∫_p^∞[1 − G_j][1 − F] under the class ranking. So A_F(μ) = E_F[ψ_μ(R)], with ψ_μ(R) = p for R < p and ψ_μ(R) = ∫_p^R[1 − G_μ(y)]dy for R ≥ p, where G_μ = (1 − μ)G_L + μG_H. ψ_μ jumps down by p at the reserve: below it, entry rescues a sale at p; just above it, the incumbent pays p anyway. A strengthening F → F̃ ≤ F changes A by ∫_p^∞[1 − G_μ][F − F̃]dy − p[F(p) − F̃(p)]: a competition gain minus a reserve-rescue loss. With F(p) = F̃(p) the loss is zero. Since 1 − G_μ ≥ 1 − G_L, the low class (μ = 0) is the hardest case, which gives the w_L condition. For a location family, differentiate in s: −p f_s(p) + ∫_p^∞[1 − G_μ(y)] f_s(y)dy, and the integral is Pr(p < R < θ). For the uniform family, ∂_r F_r(y) = −y/r², which gives dA_r(M)/dr = [ℓ² − 3p² + M(r² − ℓ²)]/(2r²).
3. Bayes plausibility gives Σ_x ν_x μ(x) = π, so some order has μ(x) ≤ π < τ. Lemma A.2(d) then gives e(x) = ρ under both challenger rules. That order has ν_x ≥ (1 − λ)η(x) > 0 and A(μ(x)) = w_L + Δμ(x) > 0, so its term in Σ_x Pr(X = x | A)(1 − e(x))A(μ(x)) is positive. The argument is the paper's, with π in place of 1/2. How far from necessary: the mean is zero exactly in equilibria where e ≡ 1, that is, where every posterior is at least τ (rule C1). With π ≥ τ, the no-informed-trade equilibrium (all posteriors π) is such a case exactly when Δ·max{π, 1 − π} ≤ k (Step 2 of the Corollary A.2 proof). So the condition can be weakened to "some on-path posterior lies below τ", but not dropped.

Conditions. Full two-sided trade for parts 1–2; part 3 needs nothing about the order pattern. B_F(π) < c_H is the left half of (H1), and along an FOSD path B_F(π) falls (Proposition 1(a)), so once it holds at the weakest incumbent it holds at every stronger one.

Benchmark check.
- Part 1: π = 1/2 lies exactly on the boundary, so the margin is zero; ρ = 1/4 leaves a margin of 1/4.
- Part 2: ℓ² − 3p² = 1/4 > 0, so w_L′(r) = 1/(8r²) > 0. In the reserve, p = 1/2 against the bound ℓ/√3 = 0.5774, a margin of 0.077. dA_r(M)/dr ≥ 0.31 on the full-trade interval (r_S, h).
- Part 2 counterexample, inside the paper's model: the benchmark h, ℓ, c_H, ρ, slot and prior, with p = 0.95 and k = 1/250. Full two-sided trade is the unique outcome for r > 1.4095 (ρm(1/2)Δ − k = 0.0016 at r = 1.5), and a purchase recruits (π < τ ≈ 0.67 < M). Yet on [1.5, 1.71] the price gap S falls from 0.5197 to 0.5098; I₊ falls until r = 1.76 and A(M) until r = 1.83. The general form of A.11(iv) would say all three rise; A.11 itself is stated at p = 1/2 and claims nothing here. The failure needs both a reserve near the low value and a low trading cost: at k = 1/50 the full-trade interval starts at r_S = 2.12, past the turn at 1.83.
- Part 3: c_H − B_r(1/2) ≥ 1.125 on (1, h), and τ(r) − 1/2 ≥ 0.125 there (τ → 0.625 as r → ℓ).

What is lost. Part 1 keeps the simple test only on half the prior line. Part 2 adds an assumption on the family, not on the prior; the benchmark meets it with margin. Part 3 loses nothing.

---

## Which statements survive at a general prior

Full two-sided trade with π < τ throughout.

| Item | Form at a general prior | Verdict |
|---|---|---|
| A.11(i) price-gap decomposition | S = ρΔ(M − m) + (1 − ρ)χA(M) | survives; replace ϑ by M(π) − m(π) |
| A.11(ii) sale impact | I₋ = ρΔ(π − m) = ρΔπ(1 − π)λ/ν₋ | survives with this correction |
| A.11(ii) raw test I₊ > I₋ ⟺ recruitment | fails at every π < 1/2; holds for π ≥ 1/2 if ρ ≤ 1/2 | needs π ≥ 1/2 (Candidate 3) |
| A.11(ii) count-weighted test ν₊I₊ > ν₋I₋ ⟺ recruitment | exact; = E[P(X)] − P(0) | holds at every prior (Candidate 1) |
| A.11(iii) hidden price | S = ρΔ(M − m) | survives |
| A.11(iv) trends | class component and I₋ rise with Δ; entry component, I₊ and S need A_F(M) to rise | independent of the prior; needs the A_F(M) condition |
| A.11(v) jump at the ceiling | at r_C(π) (τ = M(π)), P(1), I₊ and S fall by (1 − ρ)A(M) | survives |
| A.12(a) counts | depend on (π, λ, β) only through (v, λ(2π − 1)) | the nonidentification needs E[X] = 0 or an unknown prior |
| A.12(b) incentive bound | ρΔm′(π) ≥ k and e₊Δ[1 − M′(π)] ≥ k | survives with m(π), M(π) |
| A.12(c) band of shares with the same counts | the same-counts set is a curve in (π′, ϑ′) | needs π = 1/2 as stated |
| A.12(d) identification from prices | λ = 2Q + √(4Q² + E[X]²) given Δ; ρΔ given a known π ≠ 1/2 | survives and becomes stronger (Candidate 2) |
| Cor A.3 | b = Pr(X = −1); E[X] = π·s₊ | survives at a known prior |
| A.14(i)–(ii) | unchanged | general |
| A.14(iii) | positive under B_F(π) < c_H | survives with this condition |
| A.14(iv) | P(0) − P̄ = −(1 − ρ)χ(b + πλ)A(M) | survives; it is Candidate 1 |

---

## Importance of the weakness

- Nothing in A8 is false as written: A8:3–4 and §8:3–5 confine the results to the prior 1/2. The weakness is that exactness rests on a knife-edge prior, and the empirical claims read as general tests.
- The benchmark's own prior band is the strongest evidence. At the benchmark slot, (H1)–(H3) hold for π ∈ (0.467850, 0.500424) (registry `prior_lo_B`, `prior_hi_B`), and 98.7% of that band lies below 1/2. At every such prior the raw test reports recruitment at the non-recruiting full-trade strengths (r_C(π), h). Under the null this is a size distortion, not a loss of power: a large sample rejects "no recruitment" when it is true.
- Magnitudes point the other way. At the band's lower end, π = 0.4679, the no-recruitment asymmetry is 6.1% of I₋, 3.0% of the class component, and at most 1% of the recruitment term at r₁. At π = 0.3 the figures are 45%, 18% and 3–6%. The economics survive: a recruiting purchase moves the price by an order of magnitude more than the class news does. The exact "if and only if" does not survive.
- Is π = 1/2 reasonable or extreme? It is a natural theory normalization but not an empirical one. A further buyer who has not yet committed to diligence is plausibly more often a poor fit than a good one, and that is the side (π < 1/2) on which the raw test errs toward finding recruitment.
- Identification is the most affected part. At a known asymmetric prior the statement of A.12(a)/(c) inverts, but the general version (Candidate 2) is a cleaner and stronger result.
- A.14 is robust: (i)–(ii) are general, (iii) needs only B_F(π) < c_H, and (iv) is the corrected A.11 test.
- For the paper's economics the weight is low. Propositions 2 to 4 do not use the symmetric prior in this way, and every Section 8 prediction has a prior-free version that is no harder to state. Adopting Candidate 1 makes the price-gap test and the no-order-return test one result, which strengthens the section.
- The trend in A.11(iv) has nothing to do with the prior. It needs a family condition that the benchmark meets with margin; failure needs a reserve close to the low value together with a small trading cost.

## Other findings (errors in the manuscript, anything surprising)

1. A.11(ii) and A.14(iv) are one moment at the prior 1/2. In the registry, `pdrop_neutral_r1_B` = −0.257948 = −(b + λ/2) × `ba_entry_r1_B` = −0.363676 × 0.709279. The paper can state the prior-free result once and cite it in both places.
2. A.13(iii), outside W5, also uses E[X] = 0. At a general prior, Cov(X, 1_A) = (1 − ρ)χ·ν₊·[1 − λ(2π − 1)], and past the ceiling Cov(X, 1_W) = 2ρπ(1 − π)λ(W_H − W_L) (checked numerically). At π = 1/2 the latter is ρλ(1 − ℓ/r)/2, simpler than the printed (b + λ/2)ρϑ(1 − ℓ/r).
3. At any prior, both components of the price gap can be read from prices and counts alone: class component (v/ν₊)I₋, entry component I₊ − (ν₋/ν₊)I₋. At π = 1/2 these are 2I₋ and I₊ − I₋.
4. With E[X] = 0 observed under full trade and λ > 0, the counts reveal that the prior is 1/2. The paper's benchmark data therefore pin the prior while leaving the share free; at any imbalanced data point the reverse confounding holds.
5. The weighted test and the A.11 raw test both fail off the full-order pattern, for example in purchases-only profiles without recruitment. The winner-based collinearity test in Candidate 1 does not.
6. No algebra errors found in A8 at the prior 1/2. I rechecked ϑ = 2M − 1 = M − m, B_r(1/2) = 5 − r/4 + 1/(8r), B_ℓ(M) = 9M + 3/8, the feasibility condition 3v ≤ 2 + u′(1 − v), the R-branch rate s₊ = b(Δ/k − 2), μ₀ = (1 − 2b − λ)/(2 − 4b − λ) and 1/2 − μ₀ = λ/[4(1 − v_U)].
7. Wording: A.14(iv) "although the posterior after no order is 1/2" should read "is the prior" in a general statement. Cor A.3's b = (v − E[X])/2 is simply Pr(X = −1).
