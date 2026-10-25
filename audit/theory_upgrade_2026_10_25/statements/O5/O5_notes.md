# O5. Existence at the prior 1/2

The mathematics writer, statement freeze S4, area B.

## The claim

Proposition 3(d), in the full statement in `statements/B.tex`. Take the class ranking and a continuous incumbent law F with Δ_T > 0 and g_H > g_L. Let π = 1/2 and τ > 1/2, with τ ≥ 1 allowed. Let an indifferent investor mix over its best orders. Then an equilibrium exists against F under either challenger rule, for every slot with 0 < λ < 1 and 0 < β < 1/2. The equilibrium is explicit:

- **ρΔ ≤ 2k.** The quiet market.
- **ρΔ > 2k and μ_+(t) < τ.** Here t = min{λ, b(ρΔ/k − 2)}. Both classes trade at the rate t, and entry is ρ after every order. This is Q when t < λ, and full orders at the floor when t = λ.
- **ρΔ > 2k and μ_+(t) ≥ τ.** The low class sells at the rate t. Class H buys at the rate min{λ, b(Δ/k − 2)}, which is at least t. A purchase recruits, and entry is ρ after a sale and after the zero order. This is R when Δ(1 − M) < k, and F otherwise.

## Result

The claim holds. `O5_proof.tex` gives the statement and a complete proof. The proof is ready for the appendix and needs no computation.

## The argument in words

1. **The frame.** At π = 1/2 the prior is below τ. So Lemmas A.7 to A.9 apply against F, and an equilibrium is a high-class pair times a low-class rate, provided s_+ ≥ s_-.
2. **The symmetry.** At the prior 1/2, a purchase at rate s and a sale at rate s leave the same distance to the truth: 1 − μ_+(s) = μ_-(s) = b/(2b + s). At equal entry, the two orders therefore earn the same gross return.
3. **Small spread.** If ρΔ ≤ 2k, an order at the uninformative price does not pay, and the quiet market is an equilibrium.
4. **The low class's rate.** If ρΔ > 2k, the low class has exactly one rate under the mixing rule, and it is t. When t < λ, the sale breaks even at entry ρ. When t = λ, the sale earns at least k.
5. **No recruitment at t.** Suppose a purchase at the same rate t does not reach τ. By the symmetry, it also breaks even at entry ρ, or earns at least k at the full rate. Both classes trading at the rate t is then an equilibrium, with entry ρ everywhere. This is always the case when τ ≥ 1, because every posterior is below M < 1.
6. **Recruitment at t.** Suppose instead the purchase at t reaches τ. It then recruits, and its gross return is Δμ_-(t) ≥ k/ρ, strictly above k.
   - The recruiting return Δb/(2b + s) falls continuously and strictly in s.
   - If it is still at least k at s = λ, the full purchase F is an equilibrium.
   - Otherwise the return equals k at exactly one rate s_+ = b(Δ/k − 2) in (t, λ). That rate is the mixed purchase R, and its posterior lies strictly above τ.
   - In both cases s_+ ≥ s_-.
7. **Ties.** The only posterior that can equal τ is M, at the full rate. There e(1) = 1 is admitted under both challenger rules. Every other posterior is strictly on one side of τ, so the construction never needs a tie rule beyond the mixing rule for the investor.

## A second full reading of scan/reduction_A3_A5.md section 3(d)

The sketch is correct. Each of its sentences is a step of the proof:

- **"N exists because τ > 1/2."** Step 2. The quiet market needs π < τ for entry ρ, and ρΔ/2 ≤ k for both deviations.
- **"The low class has the unique positive rate t."** Step 3. This is the identity ρΔm ≥ k ⇔ b(ρΔ/k − 2) ≥ λ, which turns the three-case rate of Lemma A.8 into t.
- **"1 − μ_+(t) = μ_-(t)."** Step 1.
- **"If buying at rate t does not recruit, choosing s = t gives the floor-entry Q/full-order equilibrium."** Step 4. The return condition of (Q) or (F) is the low-class condition at the same rate, by the symmetry.
- **"If it recruits, its return at t is at least the low-class return, and the recruiting purchase return decreases continuously thereafter."** Step 5, with one precision:
  - The return at t is Δμ_-(t) ≥ k/ρ, which is strictly above k.
  - This strict margin forces t < λ whenever Δ(1 − M) < k.
  - It also places the mixed rate strictly above t, with a posterior strictly above τ.
  - The rate has the closed form min{λ, b(Δ/k − 2)}.
- **"In each case s ≥ t, so the product lemma applies."** Steps 1 and 5.
- **"For τ ≥ 1 ... e ≡ ρ."** Step 4. When τ ≥ 1 the recruiting case is empty, since μ_+(t) ≤ M < 1 ≤ τ. Lemma A.7 in `B.tex` writes (Q) as 0 < s_+ < λ with μ_+(s_+) < τ, without s*, so it covers τ ≥ 1.

Nothing in the sketch fails. The referee's verdict "proved, including τ ≥ 1" stands.

## Sharpness: the hypothesis τ > 1/2 is needed

**Fact.** At π = 1/2, suppose m(1/2) < τ ≤ 1/2 and ρΔτ < k < Δτ. If an indifferent high-cost challenger prepares, no tuple satisfies (E1) to (E6), under either investor rule.

**Proof.**

- Class H never sells (Lemma A.3(a)). So the posterior after a sale is μ_-(s_-) = b/(2b + s_-). This posterior falls strictly in s_- from 1/2 to m.
- Let s_τ = b(1/τ − 2). The hypotheses give 0 ≤ s_τ < λ.
- By Lemma A.2(d) under the default challenger rule, e(−1) = 1 for s_- ≤ s_τ, and e(−1) = ρ for s_- > s_τ.
- If s_- ≤ s_τ, the sale earns Δμ_-(s_-) ≥ Δτ > k. Lemma A.3(b) then forces s_- = λ > s_τ.
- If s_- > s_τ, the sale earns ρΔμ_-(s_-) < ρΔτ < k. Lemma A.3(b) then forces s_- = 0 ≤ s_τ.
- No rate is consistent with itself, so no equilibrium exists.

**An instance.** Take the example's classes, reserve and ρ (h = 10, ℓ = 1, p = 1/2, ρ = 1/4). Take the uniform incumbent at r = 6/5, the cost c_H = 4 and k = 1/200. Then:

- Δ = 1/60 and τ = 885/2156 ≈ 0.4105.
- ρΔτ ≈ 0.00171 < k < Δτ ≈ 0.00684.
- Every slot in the band has m(1/2) < 0.295 < τ.

An exact print-only computation confirms these values.

**Under the alternative challenger rule** the argument breaks at s_τ. There, entry k/(Δτ) after a sale makes the low class indifferent. So the fact is stated for the default challenger rule only.

**The investor rule.** The mixing rule is also needed. When an indifferent investor abstains, the example has no equilibrium on (r_N, r_S]: the low class has no qualifying sale rate there (Corollary 2's full statement and the tie paragraph).

## What it changes in the plan

- **PLAN.md Part 5, O5.** It reads "for every incumbent distribution". The proof gives existence for every continuous F with Δ_T > 0 and g_H > g_L whose threshold exceeds 1/2. By the fact above, existence can fail when τ ≤ 1/2. The scope τ > 1/2 therefore sits in the claim, as in the brief and in `B.tex`. The referee's sketch already carries it, so this is a precision, not a conflict.
- **No other change.** Corollary 2(c), existence at every strength of the example, follows from part (d), because τ ≥ τ(r_0) > 1/2 on the example path (Lemma A.10(a)).
- **Possible addition.** The coordinator can add the sharpness fact to the appendix as one sentence after the proof. It is not in `B.tex`.
