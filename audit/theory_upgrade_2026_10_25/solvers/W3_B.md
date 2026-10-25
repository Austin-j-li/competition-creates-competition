# W3-research-branch-end: Solver B

Conventions. Prior 1/2 throughout, as in Section 5. At conjectured intensity λ̂: b̂ = (1 − λ̂)β, b̂₀ = (1 − λ̂)(1 − 2β); m_λ = (1 − λ)β/[2β + λ(1 − 2β)] = 1/(2 + u_λ) with u_λ = λ/[(1 − λ)β]; M_λ = 1 − m_λ; m′_λ = −β/[2β + λ(1 − 2β)]²; λ_E(τ) solves M_λ = τ, with λ_E′(τ) = β/[β + (1 − 2β)(1 − τ)]². J = Δ(1 − τ). "The purchase recruits" means μ(1) > τ (C1 also accepts μ(1) = τ). s_N is where ρΔ = 2k, s_C is where τ = M_λ̄ (the ceiling at the cap). "IM" and "I0" are the investor tie rules, "C1" and "CM" the challenger rules.

How the numbers were obtained. Scratch scripts are in audit/theory_upgrade_2026_10_25/solvers/computations/W3_B/. `model.py` has the closed forms. `scan.py` rebuilds the equilibrium set at a given strength without them: for each conjectured intensity on a grid of 3,000 to 20,000 points in (0, λ̄], it lists the trading equilibria at that presence from Lemmas A4-high and A4-low, which hold at any presence. It computes the research value V and locates the fixed points of λ̂ = min{λ̄, V/a}, checking the cap and zero separately. `s4_primitive_check.py` and `s10_*.py` recheck selected tuples from the auction primitives: proceeds t₀, t_H, t_L, competitive prices, the challenger's belief and preparation at each price, the investor's payoffs E[V_T | j, q] − P(q), and research optimality. Every number below is a floating-point diagnostic, not a certificate.

## Candidate 1: one research branch through s_N (the low class mixes, and research is unchanged)

Angle: both. The endpoint is reformulated, and the continuation the brief asks for is constructed.

Intuition: Past ρΔ = 2k, a low-class sale at the uninformative sale price pays, so the low class must sell with some probability. Under the paper's default rule IM, it sells just often enough that the posterior after a sale falls to k/(ρΔ), where it is indifferent. An indifferent seller adds nothing to the value of research, and a sale never recruits. So research optimality, the purchase posterior and entry are exactly those of branch R, and the branch carries straight through s_N. Once even a full sale pays (ρΔm_λ ≥ k), the sale adds to the value of research, and research then rises faster.

Formal statement. Fix the prior 1/2, 0 < β < 1/2, a > 0, 0 < λ̄ < 1, rule IM, and either challenger rule. Take any auction with Δ > 0, γ > 0 and τ > 1/2. Let

  Ψ(λ, Δ) = Δm_λ − k + (ρΔm_λ − k)⁺,

let Λ*(Δ) be the unique λ ∈ (0, 1) with 2aλ = Ψ(λ, Δ) (it exists exactly when Δ > 2k), and let λ*(Δ) = min{λ̄, Λ*(Δ)}.

(a) Existence and form. If Δ > 2k and τ < M_{λ*(Δ)}, there is exactly one equilibrium in which research is positive and the purchase recruits. Research is λ*(Δ), and class H buys after a success. Class L abstains if ρΔ ≤ 2k. It sells with probability σ_L(−1) = (1 − λ*)β(ρΔ/k − 2)/λ* if ρΔm_{λ*} < k < ρΔ/2, and it sells for sure if ρΔm_{λ*} ≥ k. Entry is ρ + (1 − ρ)[β + (1/2 − β)λ*(Δ)]. High-class ownership is ½W_H(F)[ρ + (1 − ρ)(β + (1 − β)λ*(Δ))].

(b) Comparative statics. Research and entry on this branch are continuous, nondecreasing functions of Δ alone, and they rise strictly while λ* < λ̄. The slope is dΛ*/dΔ = m/(2a + Δ|m′|) while class L does not sell for sure, and (1 + ρ)m/(2a + (1 + ρ)Δ|m′|) once it does. The slope jumps up there, so research has a convex kink.

(c) The cap. Research reaches the cap at Δ*_cap = (2aλ̄ + k)/m_λ̄ if ρ(2aλ̄ + k) ≤ k, and at Δ*_cap = 2(aλ̄ + k)/[(1 + ρ)m_λ̄] otherwise. The cap therefore comes:
- before the low class starts to sell, if ρ(2aλ̄ + k) ≤ 2km_λ̄ (this is the paper's condition);
- while it mixes, if 2km_λ̄ < ρ(2aλ̄ + k) ≤ k;
- after it sells for sure, otherwise.

(d) Along a path. Take a stochastically ordered path on which Δ is continuous and strictly increasing and τ is nondecreasing. The branch exists exactly on {s : 1/2 < τ(s) < M_{λ*(Δ(s))}}, together with its boundary under C1. At any two branch strengths s < s′, research and entry are at least as high at s′, and strictly higher if research at s is below the cap. This holds even when the two strengths lie in different pieces of the set. Single crossing (SC*) asks that the recruitment margin φ*_a = J − k + (ρJ − k)⁺ − 2aλ_E(τ) cross zero only once, from below, before research reaches the cap; let s_R be that crossing. If (SC*) holds, τ crosses M_λ̄ only once, and the path gets far enough to reach the cap spread Δ*_cap and the ceiling, the branch is the interval [s_R, s_C]. If the path stops sooner, the branch runs from s_R to the end of the path. Research rises strictly from λ_E(τ(s_R)) to λ̄, reaches the cap at some s_cap* < s_C, and stays there up to s_C. The strength s_N lies inside the branch and changes only the low class's order. The branch ends at the ceiling, where the threshold catches up with the purchase posterior, not at s_N.

Derivation.

1. Positive research forces a full purchase. Lemma `lem:a5-buy` needs only τ > 1/2 and the nonzero-order posterior bounds, which hold for every β < 1/2. So in any equilibrium with λ̂ > 0, σ_H = δ₁ and μ(1) = M_λ̂. Then f_H(0) = b̂₀ ≤ f_L(0), so μ(0) ≤ 1/2, and μ(−1) ≤ 1/2. Hence e(0) = e(−1) = ρ.

2. The low class's rate is pinned by λ̂. Let t = λ̂σ_L(−1). Then μ(−1) = b̂/(2b̂ + t), so the gross sale return K_L(t) = ρΔb̂/(2b̂ + t) falls strictly from ρΔ/2 at t = 0 to ρΔm_λ̂ at t = λ̂. Under IM exactly one rate satisfies (E5), as in Lemma `lem:a4-low` at presence λ̂:
   - t = 0 if ρΔ ≤ 2k;
   - t = b̂(ρΔ/k − 2), which lies in (0, λ̂), if ρΔm_λ̂ < k < ρΔ/2;
   - t = λ̂ if ρΔm_λ̂ ≥ k.

   In each case max_q U_L(q) = (ρΔm_λ̂ − k)⁺. In the first case ρΔm_λ̂ < ρΔ/2 ≤ k, in the second the indifferent class earns zero, and in the third the sale earns ρΔm_λ̂ − k ≥ 0.

3. Research optimality on the recruiting branch. If M_λ̂ > τ, then e(1) = 1 and max_q U_H(q) = Δm_λ̂ − k. So V = ½Ψ(λ̂, Δ), and (E7), via Lemma `lem:a5-joint`, reads λ̂ = min{λ̄, Ψ(λ̂, Δ)/(2a)}. Write G(λ) = Ψ(λ, Δ) − 2aλ. G is continuous and strictly decreasing on [0, 1), because m is strictly decreasing and Δ > 0. G(0) = Δ/2 − k + (ρΔ/2 − k)⁺ is positive exactly when Δ > 2k, and G(1⁻) = −k − 2a < 0. So Λ*(Δ) is unique, and (E7) holds exactly at λ̂ = λ*(Δ). Steps 1 to 3 give the uniqueness claim in (a).

4. Verification of the mixed-sale tuple, the new piece. Take λ̂ = λ*(Δ), σ_H = δ₁, σ_L(−1) = t/λ̂ with t = b̂(ρΔ/k − 2), and σ_L(0) = 1 − t/λ̂.
   - (E1): f_H = (b̂, b̂₀, b̂ + λ̂) and f_L = (b̂ + t, b̂₀ + λ̂ − t, b̂) on the orders (−1, 0, 1). They give μ(1) = M_λ̂, μ(−1) = k/(ρΔ) ∈ (m_λ̂, 1/2), and μ(0) = b̂₀/(2b̂₀ + λ̂ − t) < 1/2.
   - (E2)–(E3): μ(1) > τ gives e(1) = 1 under both C1 and CM, and μ(0), μ(−1) < 1/2 < τ give e = ρ. Entry is nondecreasing in the posterior. Two orders can share a posterior only if they are 0 and −1, and those two also share entry ρ. The constructed-tuples paragraph (A2:165–170, in the form corrected by the scan: equal posteriors and equal entry) then gives distinct prices at distinct posteriors, and P(0) = P(−1) with a consistent pooled belief otherwise.
   - (E4): P(x) = t₀ + e(x)w(μ(x)).
   - (E5): U_H(1) = Δm_λ̂ − k ≥ 2aλ̂ > 0, so the purchase is strict. U_L(−1) = ρΔμ(−1) − k = 0, so class L is indifferent and rule IM allows the mixture. Wrong-signed orders earn at most −k.
   - (E6): truthful bids.
   - (E7): V = ½(Δm_λ̂ − k), which is aΛ* in the interior and at least aλ̄ at the cap.

   The full-sale tuple has t = λ̂ and posteriors (m_λ̂, 1/2, M_λ̂), and the same check goes through with U_L(−1) = ρΔm_λ̂ − k ≥ 0. Nothing uses β ≤ 1/3.

5. Comparative statics. Ψ strictly increases in Δ, because m_λ > 0, so Λ* strictly increases. On each smooth piece the implicit function theorem gives Λ*′ = −G_Δ/G_λ. While class L does not sell for sure, G = Δm − k − 2aλ, so Λ*′ = m/(2a + Δ|m′|). Once it does, G = (1 + ρ)Δm − 2k − 2aλ, so Λ*′ = (1 + ρ)m/(2a + (1 + ρ)Δ|m′|). The second is larger, because (1 + ρ)(2a + Δ|m′|) > 2a + (1 + ρ)Δ|m′|. Entry: a purchase has probability ½(b̂ + λ̂) + ½b̂ = β + (1/2 − β)λ̂, which does not involve σ_L. So entry = ρ + (1 − ρ)[β + (1/2 − β)λ*], with slope (1 − ρ)(1/2 − β)λ*′ > 0 for β < 1/2. Class H's purchase probability b̂ + λ̂ also does not involve σ_L, which gives the ownership formula.

6. Where the regimes switch. The low class starts to mix at Δ_N = 2k/ρ. The interior switch to a full sale is at ρΔm_Λ = k. There Δm = k/ρ, and so 2aΛ = k/ρ − k, which gives Λ_sw = k(1 − ρ)/(2aρ). It lies below the cap exactly when ρ(2aλ̄ + k) > k. Solving Ψ(λ̄, Δ) = 2aλ̄ on the relevant piece gives the two formulas in (c). Also Λ* → 1 as Δ → ∞, so the cap is reached at a finite spread. Along a given path it is reached only if the path's spread gets that far.

7. Recruitment along a path. Since Δm_{λ_E(τ)} = J, G(λ_E(τ)) = φ*_a. Because G is decreasing, Λ* ≥ λ_E exactly when φ*_a ≥ 0. With research at the cap, recruitment is λ̄ ≥ λ_E, that is τ ≤ M_λ̄. So the branch is {τ ≤ M_λ̄} ∩ {φ*_a ≥ 0}, and past the cap point the second set is implied by the first. Below s_N, ρJ < ρΔ/2 ≤ k, so φ*_a coincides with the paper's φ_a. If φ*_a(s_cap*) > 0, then λ_E(τ(s_cap*)) < λ̄, so s_cap* < s_C. Every branch point has J > k: where class L does not sell for sure, J ≥ Δm_{λ*} ≥ k + 2aλ* > k, and where it does, J ≥ Δm_{λ*} ≥ k/ρ.

Conditions: rule IM on the mixed-sale segment; τ > 1/2; Δ > 2k; strict recruitment τ < M_{λ*}, with the boundary admitted under C1; β < 1/2. For the interval form, (SC*) and a single crossing of τ = M_λ̄. Under CM the threshold tuple also extends: research λ_E(τ), with e(1) = [2aλ_E + k − (ρJ − k)⁺]/J whenever that value lies in [ρ, 1] and λ_E < λ̄.

Benchmark check.
- Benchmark, a = 1/40. The paper's condition holds, so nothing changes on [r_R, r̄_R) = [1.501023, 1.677633): research rises from 0.193853 to λ̄ = 0.336122, and entry rises from 0.500846 to 0.522757. The capped branch then continues past r_N = 1.747878. Class L mixes its sale on (r_N, 2.124148), where 2.124148 is the strength at which ρΔm_λ̄ = k, and sells for sure from 2.124148 up to r_C = 3.592659. Entry stays at 0.522757.
  - The scanner finds exactly this tuple at r = 1.75, 1.76, 1.8, 1.9, 2.0, 2.1 and 2.12 (cap, mixed sale) and at 2.13 to 3.59 (cap, full orders). At 3.595 > r_C entry is ρ.
  - From primitives at r = 1.9: σ_L(−1) = 0.386708, μ(−1, 0, 1) = (0.375309, 0.362836, 0.731059), e = (0.25, 0.25, 1), U_H(1) = 0.037327, U_L(−1) = 0.000000, and V/a = 0.746540 ≥ λ̄. Preparation is consistent at all three prices.
- Benchmark, other research costs. A numerical sweep holds the other benchmark primitives fixed. For every a < a_max = [J(r_C) − k + (ρJ(r_C) − k)⁺]/(2λ̄) = 0.40833, the recruiting branch is exactly [r_R(a), r_C] and research reaches the cap inside it. For a ≥ 0.40833 there is no recruiting branch.
  - For a ∈ (0.0343, 0.0893) the cap is reached while class L mixes, and for a ∈ (0.0893, 0.4083) after it sells for sure; Λ_sw = 0.03/a.
  - The R-only statement, with class L abstaining, holds only for a ≤ 0.034259.
  - At a = 0.2 the scanner finds interior research with full orders on the branch, matching Λ*: 0.24792 at r = 2.25 and 0.33570 at 2.66. The cap comes near 2.67.
- the referee's counterexample, re-solved (h = 10, ℓ = 1, p = 0.5, c_H = 4.5, k = 0.5, ρ = 0.5, β = 0.2, a = 0.01, λ̄ = 0.4). Here ρ(2aλ̄ + k)/k = 0.508 ≤ 1, so the cap comes while class L mixes:

| r | regime | research | entry | σ_L(−1) |
|---|---|---|---|---|
| r_R = 4.0334 | L abstains | 0.05243 = λ_E | 0.60786 | 0 |
| 5.0 | L abstains | 0.19039 | 0.62856 | 0 |
| r_N = 5.8284 | boundary | 0.28115 | 0.64217 | 0 |
| 6.0 | L mixes | 0.29752 | 0.64463 | 0.0394 |
| 6.5 | L mixes | 0.34134 | 0.65120 | 0.1262 |
| 7.0 | L mixes | 0.38010 | 0.65702 | 0.1864 |
| r_cap* = 7.2813 | L mixes, cap | 0.40000 | 0.66000 | 0.2128 |
| 8.0 | L mixes, cap | 0.40000 | 0.66000 | 0.3187 |
| r_C = 8.9144 | L mixes, cap | 0.40000 | 0.66000 | 0.4540 |

  The scanner reproduces each row. From primitives at r = 6.5: μ(−1, 0, 1) = (0.429752, 0.363010, 0.782190), τ = 0.665706, U_H(1) = 0.006827, U_L(−1) = 0.000000, and V/a = 0.341339 = λ̂. So "research rises with strength" holds on the connected set from r_R up to the cap and beyond it, from 4.03 to 8.91, in the very example that broke the original endpoint.

What is lost.
- Rule IM is now used on the mixed-sale segment (s_N, s_S*], where Δ_S* = k/(ρ m_{min{λ̄, Λ_sw}}). Under I0 the recruiting branch is missing there: on the benchmark path it is (1.747878, 2.124148], and on the referee's path it is everything past r_N, since Δ_S* = 5.333 maps to r = 12.59 > h. On both computed paths the equilibrium set under I0 stays nonempty, because research at floor entry (Q* of Candidate 3, a strict equilibrium) exists throughout the gap. On the benchmark path Q* lasts until 2.166995, past the gap's end at 2.124148. In general Q* covers the gap only while λ_Q(Δ) < λ_E(τ), and beyond that the set under I0 can be empty. This is the research counterpart of the empty set on (r_N, r_S] under I0 in Proposition 3. The paper already uses IM for forms R and Q of Proposition 3.
- Strictness. Proposition 4(b) stresses that every trade choice is strict; on the mixed segment class L is indifferent.
- Zero research coexists with the branch only up to s_N. Past s_N it is not an equilibrium. The coexisting low equilibrium becomes research at floor entry (Candidate 3), where that exists.
- Smoothness. Research is piecewise C¹, with an upward kink where class L starts to sell for sure, so "continuously differentiable" needs "piecewise".
- The interval claim still needs a single-crossing condition (Candidate 2, part SC), and the end is the ceiling s_C, not the cap.

## Candidate 2: keep the original endpoint, under a named condition on primitives

Angle: primitive condition.

Intuition: Branch R, with class L abstaining, reaches the cap before s_N exactly when research hits its cap at a spread at which a sale at the uninformative price still does not pay. That is a bound on how often preparation is free, relative to the costs of trading and of marginal research. The interval claim also needs the recruitment margin, once positive, to stay positive. That holds when research is cheap enough that the threshold cannot outrun the purchase posterior.

Formal statement. Take a stochastically ordered path on which Δ is continuous and strictly increasing and reaches both Δ_N = 2k/ρ and Δ_cap = (2aλ̄ + k)/m_λ̄. Let s̄_R denote the strength with Δ = Δ_cap.
- (SC) Suppose φ_a = J − k − 2aλ_E(τ) has a single zero s_R on the path before min{s_N, s̄_R}, and is positive after it up to min{s_N, s̄_R}.
- (CS) Cheap preparation is rare: ρ(k + 2aλ̄) ≤ 2k·m_λ̄. Equivalently, ρ(1 + 2aλ̄/k)(1 + u_λ̄/2) ≤ 1.

Under (SC), branch R is [s_R, s̄_R) and ends where research reaches the cap if and only if (CS) holds. If (CS) fails, R is [s_R, s_N] and ends, closed at that end, where the low class starts to sell, with research Λ(2k/ρ) < λ̄. (SC) holds whenever

  a < a_mono := inf over s ∈ [s_A, s̄_R] of J′(s)/[2λ_E′(τ(s))τ′(s)],

which is positive when J is strictly increasing there with J′ bounded away from zero.

Derivation.
- F_r(λ̄) = 0 is Δm_λ̄ − k = 2aλ̄, which gives Δ_cap. And s̄_R ≤ s_N ⟺ Δ_cap ≤ Δ_N ⟺ ρ(2aλ̄ + k) ≤ 2km_λ̄. Substituting m_λ̄ = 1/(2 + u_λ̄) gives the normalized form.
- Reading: at Δ_cap a sale at the uninformative price earns ρΔ_cap/2 = ρ(k + 2aλ̄)/(2m_λ̄) gross, and (CS) says this is at most k. As a → 0 it reads ρ ≤ 2m_λ̄.
- Single crossing. Along the path, dφ_a/dΔ = (1 − τ) − τ_Δ[Δ + 2aλ_E′(τ)], where τ_Δ is the derivative of τ in Δ along the path. So at any zero, transversality is dτ/dΔ < (1 − τ)/(Δ + 2aλ_E′(τ)). In elasticity form: −d ln(1 − τ)/d ln Δ < Δ/(Δ + 2aλ_E′(τ)). "J increasing" is the weaker statement −d ln(1 − τ)/d ln Δ < 1, the limit as a → 0. In words, at the strength where research first recruits, a stronger incumbent must raise the return J of a purchase that just reaches the threshold faster than it raises the marginal research cost 2aλ_E(τ) of reaching that higher threshold. The global form of this is the bound a < a_mono.
- J increasing alone is not enough. Example: h = 10, ℓ = 1, p = 1/2, c_H = 4.75, k = 1/50, ρ = 1/4, β = 0.3, a = 2, λ̄ = 0.9. J rises on all of [1.2, 5]. But the recruiting set is [1.366025, 1.464099] ∪ [1.896793, 4.911424]; τ = 1/2 at 1.366025, and φ* vanishes at the other three points. The scanner finds a recruiting equilibrium at r = 1.40, 1.45, 2.5 and 4.0, and none at 1.55, 1.70, 1.85 and 4.95. Research here is very expensive (2aλ̄/k = 180), and the first piece sits just above τ = 1/2, where λ_E is close to 0. A random search over the point-mass and uniform family found 30 draws in which the branch exits before the cap while J is still rising, all with large a.

Conditions: (SC) and (CS) as stated; a strictly increasing spread with both crossings attained; 1/2 < τ < 1 on the stretch.

Benchmark check.
- (CS): ρ(2aλ̄ + k) = 0.00920152 ≤ 2km_λ̄ = 0.0107577. The margin is 0.00155613, the scan's candidate registry key, and the normalized value is 0.855346.
- One primitive at a time, the condition breaks at:
  - a* = 0.034259 (benchmark 0.025, +37%);
  - ρ* = 0.292279 (benchmark 0.25, +17%);
  - k* = 0.014595 (benchmark 0.02; it fails for smaller k, −27%);
  - λ̄* = 0.381595 (benchmark 0.336122, +13.5%, with β fixed).
- Along the paper's β family (λ̄ = λ_B(β), with m_λ̄ = 1/(1 + e) fixed), (CS) needs λ_B(β) ≤ 0.46062. It holds for every β ≤ 1/3, since λ_B(1/3) = 0.36417.
- (SC): numerically, inf J′/(2λ_E′τ′) over [r₀, r₂] is 0.4689, attained at r₀ = 1.2. So φ_a is strictly increasing on the whole benchmark path for every a < 0.4689, about 19 times the benchmark a. The certified bound in A5:296–297 is a_mono = 0.161713 on [r₀, 7/4].

Necessity. Given (SC) and both crossings, (CS) is both necessary and sufficient. The bound on a is sufficient but far from necessary: on the benchmark path the recruiting set is an interval for every a at which it exists (a < 0.40833), while the bound on a ends at 0.4689 only because the branch has already disappeared.

What is lost: nothing relative to the original claim. But (CS) is restrictive. With the benchmark slot (2m_λ̄ = 2/(1 + e) = 0.538) it fails for every ρ > 0.538 at any research cost, and for ρ > 0.29 at the benchmark research cost.

## Candidate 3: the research phase diagram in the (Δ, τ) plane, with research a function of the spread alone

Angle: reformulate.

Intuition: On the recruiting branch, research and entry depend on the incumbent only through the spread. The threshold decides only whether the purchase recruits. The whole equilibrium set with research at prior 1/2 is a phase diagram in (Δ, τ) drawn with curves that depend only on (a, λ̄, k, ρ, β). A stronger incumbent moves the economy northeast. Research rises with the spread at every point where the branch exists, with no path condition.

Formal statement (lemma). Prior 1/2, 0 < β < 1/2, a > 0, 0 < λ̄ < 1, rules IM and C1, and any auction with Δ > 0, γ > 0 and τ > 1/2, including τ ≥ 1. The equilibria with research are exactly the following:
- (Z) No research, no trade, entry ρ. It exists if and only if ρΔ ≤ 2k.
- (R*) Research λ*(Δ), with the purchase recruiting, the class-L rule of Candidate 1(a), and entry ρ + (1 − ρ)[β + (1/2 − β)λ*(Δ)]. It exists if and only if Δ > 2k and τ ≤ M_{λ*(Δ)}.
- (Q*) Research at floor entry. Research is λ_Q(Δ) ∈ (0, λ̄), the unique root of aλ = ρΔm_λ − k; both classes trade fully after a success, the purchase does not recruit, and entry is ρ. It exists if and only if ρΔ > 2k, τ > M_{λ_Q(Δ)} and λ_Q(Δ) < λ̄.
- (F̄) Research at the cap with full orders, no recruitment, and entry ρ. It exists if and only if τ > M_λ̄ and ρΔm_λ̄ − k ≥ aλ̄. This is the paper's equilibrium against a very strong incumbent.

Under CM, add the threshold tuple of Candidate 1. Under I0, delete R* wherever ρΔm_{λ*} ≤ k < ρΔ/2.

Corollary. On R*, research and entry are nondecreasing functions of Δ, strictly increasing below the cap. The region where R* exists is a down-set in τ and an up-set in Δ. So for incumbents F ≤ F′ at which R* exists, research and entry are at least as high at F′, and strictly higher if Δ(F′) > Δ(F) and research at F is below the cap. Two equilibria coexist exactly in the band M_{λ_Q(Δ)} < τ ≤ M_{λ*(Δ)}, together with Z against R* when ρΔ ≤ 2k. The band is never empty because λ_Q < Λ*.

Derivation. R* and Z come from Candidate 1, steps 1 to 3, and the zero-research case of Lemma `lem:a5-middle`, step 1, which needs ρΔ ≤ 2k.
- Non-recruiting case, M_λ̂ < τ. Then e(1) = ρ. Lemma `lem:a5-buy` forces U_H(1) = ρΔm_λ̂ − k > 0. Hence K_L ≥ ρΔm_λ̂ > k, and class L sells for sure. So V = ρΔm_λ̂ − k, and (E7) gives either the interior root λ_Q or the cap; the cap case is F̄. The two classes earn the same, because 1 − M_λ = m_λ.
- λ_Q < Λ*. Since ρΔm − k = aλ_Q > 0 at λ_Q, G(λ_Q) = Δm − k + aλ_Q − 2aλ_Q = (1 − ρ)Δm > 0.
- The boundary λ̂ = λ_E with e(1) = 1 lies in R* at its closure, and with e(1) ∈ (ρ, 1) it is CM's threshold tuple.
- Uniqueness of the order rates and of the research fixed point in each case follows from steps 1 to 3 of Candidate 1.

Benchmark check.
- Benchmark set. The scanner reproduces the lemma at 26 strengths on the benchmark path and 12 on the referee's path, with no extra roots.
  - (r_N, 2.166995): R* at the cap and Q* coexist. At r = 1.9, Q* has λ_Q = 0.098729 < λ_E = 0.217702 and entry 0.25, and from primitives U_H(1) = U_L(−1) = 0.002468 = aλ_Q.
  - 2.166995 is where λ_Q reaches λ_E. From there to r_C, R* is the only equilibrium, at the cap with full orders.
  - Above r_C, F̄ is the only equilibrium.
- the referee's path: Q* exists on all of (5.83, 9.9), and R* on [4.03, 8.91].

What is lost: no interval or endpoint statement. The claim compares strengths only where the branch exists, so along a path its strict form needs Δ to rise strictly. Ownership carries W_H(F), which lies outside (Δ, τ).

## Importance of the weakness

The counterexample's parameters are not extreme. In normalized terms the failure needs only ρ(1 + 2aλ̄/k)(1 + u_λ̄/2) > 1. the referee's example gives 1.355. Its ingredients are ordinary:
- half of the challengers can prepare for free;
- research is cheap relative to trading (2aλ̄/k = 0.016);
- the slot at the cap has λ̄ = 0.4 and β = 0.2, so u_λ̄ = 3.33.

Its k = 0.5 is large next to the benchmark's 1/50, but the condition involves k only through 2aλ̄/k, and a cheaper k makes the failure easier, not harder. The benchmark itself clears the condition by a moderate margin. Raising a by 37%, ρ by 17% or λ̄ by 13.5%, or lowering k by 27%, breaks it, and so does 16% of the paper's own cost window in Proposition A.2.

For the economics it matters little. Under the paper's default rule IM, the failure only relabels the low class's order. Past s_N the low class mixes its sale at indifference, which adds nothing to the value of research. Sales never recruit, so entry is unchanged. Research, the purchase posterior and entry follow the same functions of Δ straight through s_N. "Competition creates research" therefore holds on one connected branch from s_R to the ceiling s_C, in the referee's example as well, wherever the recruitment margin does not cross back below zero before the cap.

Four things do change:
- Zero research stops coexisting at s_N, and research at floor entry replaces it.
- Strictness of trade choices is lost on the mixed segment.
- Under I0 the branch has a gap (s_N, s_S*].
- The correct endpoint is the ceiling, not the cap.

The general statement should therefore be Candidate 1, with Candidate 3 as its backbone lemma. Section 5's text at a = 1/40 stays true as printed.

## Other findings (errors in the manuscript, anything surprising)

1. The gray band in the figure can be filled. The note at sections/05:141–144 says research is at the cap "from r̄_R to r_N and above r_U", and it breaks the axis on (r_N, r_U). Under IM and C1, research on the recruiting branch is at the cap on all of [r̄_R, r_C], with entry 0.522757 throughout. Class L mixes on (r_N, 2.124148) and sells for sure from 2.124148.
   - The set on (r_N, 2.166995) is {R* at the cap, Q*}. On [2.166995, r₂] it is a single equilibrium, so uniqueness starts at 2.167, well below r_U = 2.434046, where the sufficient condition U begins.
   - Under I0 the set on (r_N, 2.124148] is {Q*} only.
   - Nothing printed is false. But "the two cap ranges" are one range, and the axis break hides an equilibrium the paper can characterize.
2. Research at floor entry (Q*) is new. Once a sale at the uninformative price pays, the investor researches even when its purchase cannot recruit, and trades on the floor entry ρ. Both trades are strict and earn aλ_Q. It is the research counterpart of form Q in Proposition 3. It replaces zero research as the low equilibrium past r_N, so the multiplicity of Section 5 persists past r_N in a new form.
3. Proposition A.2's cost window contains costs that move the endpoint. At the benchmark cap the window is (0.021469, 0.036763). For a ∈ (0.034259, 0.036763), 16% of the window, branch R ends at r_N with research below the cap. At a = 0.035, research at r_N is 0.332996 < 0.336122, and the extended branch reaches the cap at r = 1.753373 while class L mixes. No printed claim is wrong, since Section 5 states the endpoint at a = 1/40, but the endpoint is not a property of the admissible region.
4. The certified bound a_mono = 0.161713 at A5:296–297 is conservative. Numerically, inf J′/(2λ_E′τ′) is 0.4689 on all of [r₀, r₂], attained at r₀.
5. The brief has a factor of 2 wrong. With both classes trading, research optimality is aλ = ½[U_H(1) + U_L(−1)], that is 2aλ = U_H(1) + U_L(−1) = (1 + ρ)Δm_λ − 2k, not 2aλ = ½[…].
6. The lemma of Candidate 3 needs only β < 1/2. Once the purchase is full, μ(0) ≤ 1/2 without the zero-order bound. A5's standing assumption β ≤ 1/3 is used only for the zero-order part of `lem:a5-bounds`(a).
7. On the referee's path J peaks near r = 7.28: J(7.28) = 0.7934 and J(7.30) = 0.7932. This is irrelevant to the branch there, because research is already at the cap and recruitment then depends only on τ ≤ M_λ̄.
