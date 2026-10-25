# W1-coexistence-interval: Solver B

## Notation and three identities

Everything below is along a path F_s ordered by first-order stochastic dominance, with ranked classes, Δ > 0 and
γ > 0 on the path, rules IM and C1. Write m̄ = max{π, 1 − π} and M = M(π).

- Γ = Δ + γ = E_Hθ − E_Lθ, the class mean gap, fixed along the path.
- σ = Δ/Γ ∈ (0, 1), the share of the class gap that the target already captures.
- g_H − c_H, the high class's net margin from high-cost preparation. Since 1 − τ = (g_H − c_H)/γ, J = Δ(g_H − c_H)/γ.
- η = |dg_H|/dΔ ≥ 1, the high-class gross profit lost per unit of spread gained. Because dγ = −dΔ,
  dg_H = dg_L − dΔ, so η − 1 = |dg_L|/dΔ is the low-class profit lost per unit of spread. With point masses
  ℓ < h, η − 1 = (incumbent mass the strengthening pushes within (p, ℓ)) / (mass pushed within [ℓ, h)).
  For R ~ U[0, r], η = (r² − p²)/(r² − ℓ²).
- ε_Δ = dΔ/Δ (growth rate of the spread), ε_m = |dg_H|/(g_H − c_H) (erosion rate of the net margin).
- S(π) = {s : π < τ(s) ≤ M, ρΔ(s)m̄ ≤ k}, the strip. By the pointwise criterion the coexistence set is
  C(π) = S(π) ∩ {J ≥ k}.
- s_π, s_C, s_N, s_F: where τ crosses π, τ reaches M, ρΔm̄ reaches k, Δ reaches k/(1 − M).
  s_A = inf{s ∈ S(π) : J(s) ≥ k}.

(I1) J = Δ(g_H − c_H)/γ.

(I2) For γ > 0: J ≥ k ⟺ Δ·(g_H − c_H + k) ≥ kΓ. (J ≥ k ⟺ Δ(g_H − c_H) ≥ kγ = k(Γ − Δ).)

(I3) For F′ stronger than F (primes at F′):
  γγ′(J′ − J) = Γ(g_H′ − c_H)(Δ′ − Δ) − γ′Δ(g_H − g_H′).
Infinitesimally, γ dJ = Γ(1 − τ) dΔ − Δ|dg_H|, that is
  d ln J = ε_Δ/(1 − σ) − ε_m.

Derivation of (I3). Put m = g_H − c_H, m′ = g_H′ − c_H, dΔ = Δ′ − Δ ≥ 0, dG = g_H − g_H′ ≥ 0. Then γ = γ′ + dΔ
and m = m′ + dG, so
γγ′(J′ − J) = γΔ′m′ − γ′Δm = (γ′ + dΔ)Δ′m′ − γ′Δm′ − γ′Δ dG = γ′m′dΔ + Δ′m′dΔ − γ′Δ dG = Γm′dΔ − γ′Δ dG,
using γ′ + Δ′ = Γ. Dividing by γ² and letting F′ → F gives the infinitesimal form, and
Γ(1 − τ) = Γ(g_H − c_H)/γ gives the elasticity form. Python check at the uniform laws r = 1.3 and r = 2.9: both
sides equal 13.04534. At five benchmark strengths, J′ = (Δ′/γ)[Γ(1 − τ) − ηΔ] matches direct differentiation to
seven digits.

## Candidate 1: coexistence as a race between the threshold and the break-even posterior

Angle: both. This is an unconditional restatement in the (Δ, τ) plane, and the interval holds under one stated
crossing condition.

Intuition. A recruiting purchase that lands at posterior μ earns Δ(1 − μ), so it covers the trading cost exactly
when μ ≤ 1 − k/Δ. Call 1 − k/Δ the break-even posterior; on the mixed-purchase branch it is the posterior after a
purchase. Coexistence needs three things: the preparation threshold lies above the prior and below both the top
posterior and the break-even posterior, and an uninformative unit order does not pay. A stronger incumbent raises
both the threshold and the break-even posterior. The full-purchase part of the coexistence region is a rectangle,
which a path that only moves up and to the right crosses in one stretch. Only the mixed-purchase part can break up.

Formal statement. Take ranked classes, π ∈ (0, 1), ρ, k, a slot with 0 < λ < 1 and 0 < β < 1/2, rules IM and C1,
and a path along which Δ and τ are continuous with Δ > 0 and γ > 0.

1. Pointwise, with no condition. No trade and an informative equilibrium coexist at F if and only if
   π < τ(F) ≤ min{M, 1 − k/Δ(F)} and ρΔ(F)m̄ ≤ k.
   The informative equilibrium is unique. It is a full purchase when Δ(1 − M) ≥ k and a mixed recruiting purchase
   otherwise (the threshold pair when J = k). Its entry is ρ + (1 − ρ)·min{(1 − π)bΔ/k, b + πλ}.
2. The region, with no condition. In the (Δ, τ) plane, coexistence is the fixed set 𝒞 = 𝒞_F ∪ 𝒞_R:
   - 𝒞_F = {π < τ ≤ M, k/(1 − M) ≤ Δ ≤ k/(ρm̄)}, where the informative equilibrium is a full purchase; this is a rectangle.
   - 𝒞_R = {π < τ < M, k/(1 − τ) ≤ Δ < k/(1 − M), ρΔm̄ ≤ k}, where it is a mixed purchase; this region lies under
     the rectangle and above the rising curve Δ = k/(1 − τ).

   𝒞 depends on (π, ρ, k, λ, β) and not on the auction. A stronger incumbent moves the economy weakly up (Δ) and
   to the right (τ).
3. Along the path, with no condition.
   - (a) S(π) is an interval running from s_π to min{s_C, s_N}, and C(π) ⊆ S(π). Leaving through the top (an
     uninformative order pays) or through the right (the top posterior cannot recruit) is permanent.
   - (b) C_F = {s : F_s ∈ 𝒞_F} is an interval, and entry on the informative branch is constant on it at
     ρ + (1 − ρ)(b + πλ).
   - (c) Every strength in C_R lies below every strength in C_F. Any hole in C(π) lies in C_R, among strengths
     where the purchase is mixed.
   - (d) Entry on the coexisting informative branch is nondecreasing in strength over all of C(π), whether or not
     C(π) is an interval. It is strictly increasing over C_R wherever Δ rises strictly.
4. Interval, under a stated condition. C(π) = S(π) ∩ [s_A, ∞) if and only if J ≥ k on S(π) ∩ [s_A, s_F): once
   the break-even posterior reaches the threshold, it must stay at or above it until full purchases pay. When
   τ > π at s_A, this set is [s_A, min{s_N, s_C}], which is the form the paper uses. Candidates 2 and 3 give
   sufficient conditions.

Derivation.
- Part 1 is the scan's pointwise criterion, with J ≥ k ⟺ τ ≤ 1 − k/Δ. On branch R, Δ[1 − μ(1)] = k gives
  μ(1) = 1 − k/Δ.
- Part 2, split by Δ(1 − M).
  - If Δ(1 − M) ≥ k, then τ ≤ M gives J = Δ(1 − τ) ≥ Δ(1 − M) ≥ k. The J condition is slack, and what remains
    is the rectangle.
  - If Δ(1 − M) < k, then J ≥ k gives 1 − τ ≥ k/Δ > 1 − M, so τ < M. This is 𝒞_R.
- Part 3(a). {τ > π} = {B_F(π) < c_H} is an up-set and {τ ≤ M} = {B_F(M) ≥ c_H} is a down-set, because B_F(μ)
  falls with strength at every μ (Proposition 1(a)). {ρΔm̄ ≤ k} is a down-set because Δ rises (Proposition 1(b)).
  Under γ > 0 these equivalences need no sign condition on c_H − g_L.
- Part 3(b). On {τ > π}, c_H − g_L > πγ > 0. Since g_L falls, c_H > g_L at every stronger law, so τ is
  nondecreasing there. Take s₁ < s < s₂ with s₁, s₂ ∈ C_F. Then τ(s₁) ≤ τ(s) ≤ τ(s₂) and
  Δ(s₁) ≤ Δ(s) ≤ Δ(s₂), so F_s ∈ 𝒞_F. Entry: Pr(X = 1) = b + πλ and e(1) = 1.
- Part 3(c). If s ∈ C_R and s′ ∈ C_F, then Δ(s) < k/(1 − M) ≤ Δ(s′). Since Δ is nondecreasing, s < s′.
- Part 3(d). Entry is a nondecreasing function of Δ, and Δ is nondecreasing in s.
- Part 4. For s ∈ S(π) with s ≥ s_F, J(s) ≥ Δ(s)(1 − M) ≥ k automatically. So S(π) ∩ [s_A, ∞) ⊆ C(π) exactly when
  J ≥ k on S(π) ∩ [s_A, s_F). The reverse inclusion is the definition of s_A.

The (Δ, τ)-plane idea floated in the brief is right, but the region alone does not give the interval. The
region's lower boundary Δ = k/(1 − τ) rises, so a path moving up and to the right can cross it downward. The
rectangle part does not have this problem.

Conditions. None for parts 1 to 3: they use only the class ranking (through the directions of Δ and B_F),
Δ > 0, γ > 0, and continuity for attained endpoints. Part 4 is an "if and only if".

Benchmark check (prior 1/2, benchmark slot, M = e/(1 + e) = 0.731059).
- 𝒞_F: τ ∈ (1/2, 0.731059] and Δ ∈ [k/(1 − M), 2k/ρ] = [0.074366, 0.16].
- 𝒞_R: τ ∈ (1/2, 0.731059) and Δ ∈ [k/(1 − τ), 0.074366).
- On the path, C_F = [r_F, r_N] = [1.467127, 1.747878] and C_R = [r_A, r_F) = [1.393958, 1.467127).
- Entry rises from 0.454185 to 0.522757 on C_R and stays at 0.522757 on C_F, matching the registry values.
- The condition in part 4 holds (Candidate 2), so there is no hole.

What is lost.
- Without the part-4 condition, the mixed-purchase part may have holes.
- Coexistence can end where the threshold catches the break-even posterior, before s_N and s_C (Importance,
  item 1).
- "Entry rises strictly and continuously on [r_A, r_F]" weakens to "entry rises across C_R".

What is kept: the pointwise criterion, uniqueness, the entry formula, the full-purchase interval, and the
permanence of both exits. The CM claim that entry in the threshold pair falls is a separate issue: it needs
Δ(1 − τ)² to be monotone (see Other findings, item 1).

## Candidate 2: the spread is at least as elastic as the high class's net margin

Angle: primitive condition.

Intuition. J = Δ(g_H − c_H)/γ. A stronger incumbent widens the spread Δ, shrinks the high class's net margin
g_H − c_H, and shrinks γ, and the last effect helps J. J falls only when the net margin is thin: a small loss of
gross profit is then a large proportional loss of margin, and the threshold is close to one. If the spread grows
proportionally at least as fast as the net margin shrinks, J cannot fall. The coexistence set is then exactly the
paper's interval, at every prior.

Formal statement. Suppose g_H > c_H at s_0 and that on the path [s_0, s_2]:

  (E) Δ(F_s)·[g_H(F_s) − c_H] is nondecreasing in s.

Since the product is positive at s_0 and does not fall, g_H > c_H on the whole path. Then J is nondecreasing on
the path. So for every prior, every k and every slot, {J ≥ k} ∩ S(π) is an up-set
within S(π), and C(π) = S(π) ∩ [s_A(π), ∞). At prior 1/2 with τ > 1/2 on the path, C = [s_A, min{s_N, s_C}].
Corollary A.2's set formula holds with r ≥ r_A replaced by J ≥ k, and its four cases follow under the
level-crossing conditions listed in the scan. If the product in (E) is strictly increasing, or if γ is strictly
decreasing, then J is strictly increasing and s_A is the unique root of J = k.

On a differentiable path, (E) reads ε_Δ ≥ ε_m: the growth rate of the spread is at least the erosion rate of the
high class's net margin. Equivalently, g_H − c_H ≥ ηΔ. For one prior, (E) is needed only on the initial segment
{τ ≤ M(π)}, which contains S(π).

Derivation.
- Monotone J. If (E) holds and g_H − c_H > 0, then J = Δ(g_H − c_H)/γ has a nonnegative, nondecreasing numerator
  and a positive, nonincreasing denominator (dγ = −dΔ ≤ 0). So J is nondecreasing. No differentiability is needed.
- Where g_H − c_H > 0. On {τ ≤ M} we have g_H − c_H = γ(1 − τ) ≥ γ(1 − M) > 0. (E) cannot hold all the way to
  the strength where g_H = c_H, because the product is zero there. For the same reason, J cannot be monotone along
  a path that runs that far. A bounded path is part of the statement.
- Up-set. If J is nondecreasing and J(s₁) ≥ k with s₁ < s₂ in S(π), then J(s₂) ≥ k.
- Elasticity form. d ln[Δ(g_H − c_H)] = ε_Δ − ε_m. By (I3), d ln J = ε_Δ/(1 − σ) − ε_m, so the exact condition for
  J to rise is ε_Δ ≥ (1 − σ)ε_m. (E) drops the factor 1 − σ.

Conditions: the class ranking, γ > 0 and Δ > 0 on the path, and (E). In economic terms, competition raises the
target's stake in the class proportionally at least as fast as it erodes the high class's net preparation margin.

Benchmark check, by hand.
- With R ~ U[0, r], g_H − c_H = 4 − r/2 − 1/(8r). Its derivative is −1/2 + 1/(8r²), negative for r > 1/2, so it
  decreases.
- ηΔ = (r − 1)(r² − 1/4)/(2r(r + 1)) increases for r > 1. Its log-derivative is
  [1/(r − 1) − 1/r] + [2r/(r² − 1/4) − 1/(r + 1)], and both brackets are positive.
- So g_H − c_H − ηΔ decreases along the path. At r_2 = 18/5 it equals 2.1653 − 0.9978 = 1.1675 > 0.
- Hence (E) holds strictly on [r_0, r_2], with ε_Δ/ε_m ≥ 2.170. The bound binds at r_2; the ratio is 73.1 at r_0.

This replaces the Sturm count in Lemma A4-path(b) with a two-line argument.

How far from necessary.
- J-monotonicity needs ε_Δ/ε_m ≥ 1 − σ. On the benchmark path σ ≤ Δ(r_2)/9 = 0.1043, so (E) asks at most 12% more.
- J-monotonicity itself holds with ratio Γ(1 − τ)/(ηΔ) = 2.423 at r_2.
- J-monotonicity is more than the interval needs: only the crossings matter (Candidate 3).

Special case: the strengthening leaves the low class's profit unchanged (η = 1). the referee's family is an example:
the incumbent always beats the low class. Then (E) reads g_H − c_H ≥ Δ. Exactly, J rises if and only if τ ≤ γ/Γ,
which is equivalent to τ ≤ √[(c_H − g_L)/Γ]. So J rises on the whole recruitment-feasible set {τ ≤ M} if and only
if c_H − g_L ≥ M²Γ. This is a direct bound on the high cost relative to the class gap. The benchmark's c_H = 6
exceeds M²Γ = 4.81, but the benchmark has η > 1, so it is not in this case.

What is lost: nothing relative to the paper's conclusion. The hypothesis is a condition on the path, though. It
fails on the referee's family and on the mixture path in the Importance section, and it is stronger than the interval
requires.

## Candidate 3: only the break-even point matters (an up-set without a monotone J)

Angle: primitive condition. The hypothesis is weaker than in Candidate 2; the conclusion is the same for one k and
one prior.

Intuition. The coexistence interval needs J to cross k only upward inside the strip. At a crossing, the purchase
lands exactly at the break-even posterior and the spread is pinned at k/(1 − τ). The race then reduces to one
comparison: the trading cost against the class gap times the squared residual doubt. When trading costs are small
relative to the class gap, the threshold cannot overtake the break-even posterior.

Formal statement. Let s ↦ (Δ(F_s), g_H(F_s)) be differentiable (C¹ is enough), and fix π and k.

- (a) At any s* ∈ S(π) with J(s*) = k, J′(s*) has the sign of Γ(1 − τ*)² − kη*. Here η* = |g_H′|/Δ′, with
  η* = ∞ if Δ′ = 0 < |g_H′|.
- (b) Suppose kη(s) < Γ(1 − τ(s))² at every s ∈ S(π) with J(s) = k and Δ(s) < k/(1 − M). Then
  C(π) = S(π) ∩ [s_A, ∞).
- (c) At such points, 1 − τ = k/Δ > max{1 − M(π), ρm̄}. So (b) holds under the small-trading-cost condition

    (K) k·η̄ ≤ Γ·max{1 − M(π), ρ·max{π, 1 − π}}²,

  where η̄ is the largest η over strengths with k/(1 − π) < Δ < k/(1 − M). The prior-free version
  (K₀) k·η̄ ≤ Γρ²/4 covers all priors at once. For (K₀), η̄ is the largest η over strengths with
  k < Δ ≤ 2k/ρ, because a crossing inside any S(π) has Δ = k/(1 − τ) > k and Δ ≤ k/(ρm̄) ≤ 2k/ρ.
- (d) The crossing condition, with ≥, is necessary for the paper's endpoint formula. If Γ(1 − τ*)² < kη* at a
  crossing in the interior of S(π), then J < k just above s*, and C(π) ≠ S(π) ∩ [s_A, ∞). It is not necessary for
  C(π) to be an interval, because a hole also needs a later upward crossing.
- Derivative-free variant: by (I2), {J ≥ k} = {Δ(g_H − c_H + k) ≥ kΓ}. So the condition
  (E_k) "Δ·(g_H − c_H + k) nondecreasing on S(π)" also gives the up-set. (E_k) is implied by (E), since kΔ rises.

Derivation.
- (a) By (I3), γJ′ = Γ(1 − τ)Δ′ − Δ|g_H′|. At J = k we have Δ = k/(1 − τ), so
  γJ′ = (Δ′/(1 − τ))[Γ(1 − τ)² − kη].
- (b) Suppose s₁ < s₂ lie in S(π) with J(s₁) ≥ k > J(s₂). Let s* be the last point in [s₁, s₂] with J ≥ k, so
  J(s*) = k and J < k on (s*, s₂].
  - If τ(s*) = M, then Δ(s*) = k/(1 − M). On (s*, s₂], Δ ≥ k/(1 − M) and τ ≤ M, so J ≥ k, which is a
    contradiction.
  - Hence τ(s*) < M and Δ(s*) < k/(1 − M). Then (a) and the hypothesis give J′(s*) > 0, which is again a
    contradiction.
- (c) J = k together with ρΔm̄ ≤ k gives 1 − τ = k/Δ ≥ ρm̄, and τ < M gives 1 − τ > 1 − M. (K₀) uses m̄ ≥ 1/2.

Conditions. A differentiable path, the class ranking, and Δ > 0, γ > 0. Every term in (K) is a primitive except
η̄, which describes where the strengthening moves the incumbent relative to the class distributions:
- For point masses, η − 1 is the ratio of mass pushed within (p, ℓ) to mass pushed within [ℓ, h).
- For a location family F(y − s), η = 1 + Pr(p < R < ℓ)/Pr(ℓ ≤ R < h).
- Spreading the classes raises η, because D < 1 − G_H wherever G_L < 1. Point masses are the favourable case, not
  the unfavourable one.

No hazard-rate condition enters.

Benchmark check.
- J = k only at r_A = 1.393958, where τ_A = 0.640739 and η = 1.7952. There Γ(1 − τ_A)² = 1.1616 against
  kη = 0.0359, a factor of 32.4.
- Uniform (K) at prior 1/2: Γ(1 − M)² = 0.65097. The crossing band is Δ ∈ (0.04, 0.074366), that is
  r ∈ (1.3257, 1.4671). There η ≤ 1.9903, so kη̄ = 0.0398, a factor of 16.4. With η(r_0) = 2.7045 instead, the
  factor is 12.0.
- Prior-free (K₀): the band k < Δ ≤ 2k/ρ is r ∈ (1.221, 1.748], where η ≤ 2.53 ≤ η(r_0). Γρ²/4 = 0.1406
  against kη(r_0) = 0.0541, a factor of 2.6.

What is lost relative to Candidate 2. (K) covers one k and one prior at a time; (K₀) covers all priors. It needs a
derivative at the crossing. It says nothing about J away from crossings, so it does not give the CM threshold-pair
claim.

## Importance of the weakness

1. the referee's counterexample does not break the interval; it moves the end.
   - Setup: h = 10, ℓ = 1, p = 1/2, c_H = 2, R ~ U[z − 0.1, z + 0.1]. The high class always wins and the low class
     never does, so g_L = 0, η = 1, Δ = z − 1, g_H = γ = 10 − z, and J = (z − 1)(8 − z)/(10 − z). The numbers
     J(7) = 2 and J(7.5) = 1.3 are reproduced.
   - This J is log-concave in z: the second derivative of ln J is −1/(z − 1)² − 1/(8 − z)² + 1/(10 − z)² < 0. It
     peaks at z = 10 − √(Γc_H) = 5.757, so {J ≥ k} is always an interval.
   - J falls because the high class's net margin is thin. At z = 7, g_H − c_H = 1 and it erodes one for one, so
     ε_m = 1 against ε_Δ = 1/6.
   - Coexistence along this family, at ρ = 1/4 and π = 1/2:
     - With the benchmark slot and k = 2, C = (6, 7]. It ends where J returns to k, before the ceiling z_C = 7.264.
     - With M = 0.8 and k = 3/2, C = (6, 7.386], against z_C = 7.5 and s_N = 13.
     - The informative branch is the mixed purchase throughout; full purchases would need z ≥ 8.5. An independent
       enumeration of equilibria at 501 strengths agrees with the criterion everywhere.
   - How extreme the parameters are. In this family, τ > 1/2 needs z > 6, where the target already holds
     σ ≥ 5/9 of the class gap. Coexistence then needs k ≥ ρΔ/2 ≥ 0.625, which is 31 times the benchmark trading
     cost and 62% of the low class's value. The high cost is 2 instead of 6. With c_H = 6 the same family has J
     rising wherever a purchase can recruit, since c_H ≥ M²Γ = 4.81.
   - Verdict: extreme parameters, mild consequence (an endpoint moves).

2. A real hole at every benchmark primitive.
   - Keep h, ℓ, p, ρ, c_H = 6, k = 1/50, π = 1/2 and the benchmark slot, and change only the incumbent family.
     Let R be the mixture 0.85·U[a ± 0.02] + 0.15·U[b ± 0.02], with a ∈ (p, ℓ) and b ∈ (ℓ, h). Then
     Δ = 0.15(b − 1), g_L = 0.85(1 − a) and g_H = 0.85(10 − a) + 0.15(10 − b).
   - The path has three phases, each a first-order strengthening:
     1. b: 1.10 → 1.38, with a = 0.55.
     2. a: 0.55 → 0.95, with b = 1.38.
     3. b: 1.38 → 1.58, with a = 0.95.
   - Result: coexistence holds on s ∈ [0.93, 1.55] ∪ [2.10, 3.00], with only no trade in between. This comes from
     numerical integration of the laws plus an independent enumeration of the equilibrium set at 301 points, with
     no mismatch against the criterion.
   - In the middle phase the incumbent strengthens only where it loses to both classes. Δ stays at 0.0570, g_L falls
     from 0.3825 to 0.0425, τ rises from 0.6281 to 0.6662, and J falls from 0.02120 to 0.01903 < k. In the third
     phase J returns to 0.02297 at τ = 0.6671 < M.
   - The hole survives a full-support perturbation. Mixing weight 10⁻⁴ of U[0, 10] into every law gives
     J = 0.02134, 0.01916, 0.02310 at the three phase ends.
   - The model allows supports that do not start at zero (F on [0, r̄]). The cause is η = ∞ in the middle phase,
     not extreme numbers.

3. The benchmark auction family is safe at the benchmark slot and trading cost, but not at every slot and trading
   cost.
   - J peaks at r = 5.149, where τ = 0.809.
   - With k = J(5.7) = 0.3095 (15 times the benchmark) and M = 0.87 (outside the band of Proposition A.1),
     coexistence is [4.573, 5.700]. It ends where J returns to k, before r_C = 6.185 and r_N = 6.805.
   - For slots in the band (M < τ(r_2) = 0.7314) and k = 1/50, nothing changes.

How much it matters: little for the economics, more for the wording.

These hold with no condition:
- the mechanism (Proposition 2);
- the pointwise criterion;
- uniqueness of the informative equilibrium;
- the entry formula;
- the rise of entry with the spread;
- the permanence of both exits: no trade fails at s_N, and recruitment fails at s_C.

What needs a condition is the claim that the mixed-purchase part is one unbroken stretch starting at s_A. It fails
in two ways:
- a strengthening that raises the threshold without widening the spread, by pushing incumbent values up where the
  incumbent loses to both classes; or
- a thin high-class net margin combined with a trading cost that is large relative to the class gap.

Neither is the paper's story of a stronger incumbent. The sentences to qualify are "coexist on an interval of
strengths" at sections/01_introduction.tex:61 and sections/09_conclusion.tex:11. Possible qualifiers are "when the
spread grows proportionally at least as fast as the high class's net margin falls" or "in the benchmark". The
abstract (main.tex:94) makes no interval claim and can stay.

## Other findings

1. Lemma A4-path (b) and (c) have short analytical proofs, so two computer-assisted Sturm certificates can be
   relabelled analytical.
   - (b): by (I3), J′ = (Δ′/γ)[Γ(1 − τ) − ηΔ]. Γ(1 − τ) falls by part (a), and ηΔ = (r − 1)(r² − 1/4)/(2r(r + 1))
     rises. At r_2 they equal 2.4175 and 0.9978.
   - (c): [Δ(1 − τ)²]′ > 0 if and only if Γ(1 − τ) > Δ(1 + τ) + 2Δ(η − 1). Here Δ(1 + τ) rises to 1.6256 at r_2,
     and 2Δ(η − 1) = 0.75(r − 1)/(r(r + 1)) ≤ 0.1287, with the maximum at r = 1 + √2. So the right side is at most
     1.7543 < 2.4175 everywhere on the path.
   - Part (c) therefore holds on all of [r_0, r_2], not only on [r_0, 2]; the numerical minimum of the margin is
     0.674.
   - A single route gives both: Δ(g_H − c_H)² nondecreasing, which is the same as g_H − c_H ≥ 2ηΔ. At r_2 this is
     2.1653 against 1.9955, and it then holds on the whole path, because the left side falls and the right side
     rises. Since Δ(1 − τ)² = Δ(g_H − c_H)²/γ², this condition is also a general sufficient condition for the CM
     claim that entry in the threshold pair falls.
   - Consequence for the bookkeeping: the status labels in comparison.tex and the certificate keys (QJ_r0 and the
     p1_certificates log) can move from computer-assisted to analytical, or stay as cross-checks.
2. J cannot be monotone along a path that runs until g_H reaches c_H, because J = Δ(g_H − c_H)/γ → 0 there. In the
   benchmark, J peaks at r = 5.149 and g_H = c_H at r = 7.969. "J increasing" is therefore always a statement about
   a bounded part of the path. Every coexistence point at every prior has τ ≤ 1 − ρm̄ ≤ 1 − ρ/2, which gives the
   natural bound.
3. At prior 1/2, coexistence can start at s_π rather than at s_A. In the referee's family, τ < 1/2 for z < 6 while
   J > k. The general Proposition 3 needs τ(s_0) > π as a hypothesis, as the benchmark has, or else a left end of
   max{s_A, s_π}.
4. The research branch faces the same race, since φ_a = J − k − 2aλ_E(τ). By (I3),
   γφ_a′ = Γ(1 − τ)Δ′ − Δ|g_H′| − 2aγλ_E′(τ)τ′. A single-crossing condition for φ_a can therefore be built from (E)
   plus a bound on 2aλ_E′τ′.
5. The independent enumerator (scratch file audit/theory_upgrade_2026_10_25/solvers/computations/W1_B/engine.py) built the high-class pairs N, Q, R, T, F
   and the low-class rates directly. At 802 path points across the two counterexample families it agreed with the
   pointwise criterion everywhere, under rules IM and C1. This supports the scan's claim that the criterion holds in
   general.
