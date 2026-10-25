# W3-research-branch-end: Solver D

Scratch scripts: `audit/theory_upgrade_2026_10_25/solvers/computations/W3_D/` (`model.py`, `run_bench.py`, `run_referee.py`, `run_rf.py`, `run_sc.py`, `run_capped.py`). All numbers below are float diagnostics (bisection to 1e-60 in λ, finite differences for slopes), not certificates. Every equilibrium claim was recomputed at the stated tuple: order laws, posteriors, entry, prices, the four nonzero-order payoffs, the research value V and the research best response min{λ̄, V/a}.

Standing hypotheses for every statement below: prior 1/2; Δ > 0, γ > 0, τ > 1/2; 0 < β < 1/2 (β ≤ 1/3 is not needed: μ(0) ≤ 1/2 follows from σ_H(0) = 0 ≤ σ_L(0)); investor rule IM and challenger rule C1 unless said otherwise; a > 0, 0 < λ̄ < 1. Everything depends on the auction only through (Δ, τ), as the reduction lemma requires. Notation: m_λ = (1−λ)β/[2β + λ(1−2β)], M_λ = 1 − m_λ, λ_E(τ) solves M_λ = τ (set λ_E = +∞ when τ ≥ 1), Δ_N = 2k/ρ (the no-trade spread, r_N in the benchmark), J = Δ(1−τ).

## Candidate 1: The recruiting branch does not end when the low class sells

Angle: both (reformulate; the one remaining path condition is restated in the (Δ, τ) plane)

Intuition: The manuscript's branch R is defined with class L abstaining, so it has to stop at the no-trade spread Δ_N = 2k/ρ, where a sale against the uninformative price starts to pay. Nothing economic happens there. Past Δ_N the low class sells with the probability that keeps its own sale exactly break-even, so it adds nothing to the value of research and the research equation is unchanged. Once the low class sells after every success, its strictly positive sale profit also pays for research, and research rises faster with the spread. Research and entry are continuous, strictly increasing functions of the spread alone from the start of the branch to the cap. The branch ends only at the cap, or where the preparation threshold climbs above the top posterior that research can generate.

Formal statement:

Define the sale-switch intensity λ_S = (1−ρ)k/(2aρ) and the research schedule λ*(Δ) on Δ > 2k:
- λ*(Δ) = Λ(Δ), the root of 2aλ = Δ m_λ − k, when Λ(Δ) ≤ λ_S;
- λ*(Δ) = Λ_F(Δ), the root of 2aλ = (1+ρ)Δ m_λ − 2k, when Λ(Δ) ≥ λ_S.

Its inverse is Δ*(λ) = (2aλ + k)/m_λ for λ ≤ λ_S and (2aλ + 2k)/[(1+ρ)m_λ] for λ ≥ λ_S. Write Δ_S = Δ*(λ_S) and Δ_cap = Δ*(λ̄).

(a) Existence and form. At (Δ, τ) there is an equilibrium in which class H buys after every success, a purchase recruits (e(1) = 1), and research is interior, if and only if λ_E(τ) ≤ λ*(Δ) < λ̄. It is unique. Research is λ*(Δ); entry is ρ + (1−ρ)[β + (1/2−β)λ*(Δ)]; e(0) = e(−1) = ρ. Class L abstains if ρΔ ≤ 2k; sells with probability t/λ*, t = (1−λ*)β(ρΔ/k − 2), if ρΔ > 2k and λ* < λ_S (equivalently ρΔ m_{λ*} < k); sells after every success if λ* ≥ λ_S. The capped version (research λ̄, same orders) exists if and only if Δ ≥ Δ_cap and τ ≤ M_λ̄; its entry is ρ + (1−ρ)[β + (1/2−β)λ̄].

(b) Monotonicity. λ* is continuous and strictly increasing, C¹ except at Δ_S, with dλ*/dΔ = m/(2a − Δm′) below Δ_S and (1+ρ)m/(2a − (1+ρ)Δm′) above (m = m_{λ*}, m′ = dm/dλ < 0). The slope jumps up at Δ_S: the ratio of the two slopes is (1+ρ)(2a − Δ_S m′)/(2a − (1+ρ)Δ_S m′) > 1. Entry is strictly increasing in Δ. Neither research nor entry depends on τ, which enters only through the recruitment condition.

(c) The region and the path. In the (Δ, τ) plane the interior recruiting branch lives on 𝓡 = {1/2 < τ ≤ M_{λ*(Δ)}, 2k < Δ < Δ_cap}: below the research-recruitment curve τ = M_{λ*(Δ)}, which rises in Δ, and left of the vertical cap line. Take a path (Δ(s), τ(s)) with both coordinates nondecreasing. If the path crosses the curve once, from above, at s_R, before it reaches the cap line at s_cap, then the interior branch is exactly [s_R, s_cap), the capped branch continues on [s_cap, s_C] where s_C is the first point with τ = M_λ̄, and on [s_R, s_C] research min{λ*(Δ), λ̄} and entry are nondecreasing: strictly increasing wherever Δ rises strictly before s_cap, constant after. The spread Δ_N is not an endpoint of anything. The cap-before-selling condition of the scan (ρ(2aλ̄ + k) ≤ 2k m_λ̄) is not needed.

Proposed wording for the paper: "Wherever a purchase after a success recruits, research is min{λ*(Δ_T), λ̄} and entry is ρ + (1−ρ)[β + (1/2−β)·research]: continuous, nondecreasing functions of the target-payoff spread alone, strictly increasing until research reaches the cap. A stronger incumbent raises research and entry wherever such an equilibrium exists. The low class's selling, which begins at the no-trade spread 2k/ρ, never ends the branch; once the low class sells after every success, each unit of spread raises research by more."

Derivation:

1. Payoffs at a conjectured intensity λ̂ with σ_H = δ_1 and informed sale probability t = λ̂σ_L(−1). Write b̂ = (1−λ̂)β, b̂_0 = (1−λ̂)(1−2β). Then f_H = (b̂, b̂_0, b̂+λ̂) and f_L = (b̂+t, b̂_0+λ̂−t, b̂) on (−1, 0, 1). So μ(1) = M_λ̂, μ(−1) = b̂/(2b̂+t) ≤ 1/2, μ(0) = b̂_0/(2b̂_0+λ̂−t) ≤ 1/2. Since τ > 1/2, e(0) = e(−1) = ρ, and e(1) = 1 exactly when M_λ̂ ≥ τ (C1). By Lemma A.3, U_H(1) = e(1)Δ m_λ̂ − k and U_L(−1) = ρΔ b̂/(2b̂+t) − k. Prices P(x) = t_0 + e(x)w(μ(x)) with entry nondecreasing in the posterior, so distinct posteriors give distinct prices and equal posteriors give equal entry and equal prices (the constructed-tuple paragraph of A2).

2. Classification, the analogue of Step 5 of lem:a5-middle. Any equilibrium with λ̂ > 0 has σ_H = δ_1 and U_H(1) > 0 (lem:a5-buy, which needs only τ > 1/2 and prior 1/2). The low class's rate is pinned by K_L = ρΔ b̂/(2b̂+t), which falls strictly in t from ρΔ/2 to ρΔ m_λ̂: t = 0 iff ρΔ/2 ≤ k; t interior with K_L = k, that is t = b̂(ρΔ/k − 2), iff 2k < ρΔ < k/m_λ̂ (rule IM); t = λ̂ iff ρΔ m_λ̂ ≥ k. Exactly one case holds at each (Δ, λ̂). The research condition (E7) is λ̂ = min{λ̄, V/a} with V = ½U_H(1) + ½U_L(−1)⁺ (Lemma A.5-joint, general). So an interior intensity solves 2aλ = U_H(1) + U_L(−1)⁺; the brief's conjectured form 2aλ = ½[U_H(1) + U_L(−1)] carries an extra ½ and omits the positive part.

 Recruiting case, e(1) = 1. If t < λ̂ the low class earns zero (it abstains or is indifferent), so V = ½(Δ m_λ̂ − k); if t = λ̂, V = ½[(1+ρ)Δ m_λ̂ − 2k]. In both cases V/a falls strictly in λ̂ while the left side rises, so the interior fixed point is unique: Λ(Δ) or Λ_F(Δ). Consistency of the regimes: on Λ, Δ m_Λ = 2aΛ + k, so t < λ̂ (ρΔ m_Λ < k) is ρ(2aΛ + k) < k, that is Λ < λ_S. On Λ_F, (1+ρ)Δ m_{Λ_F} = 2aΛ_F + 2k, so t = λ̂ (ρΔ m_{Λ_F} ≥ k) is ρ(2aΛ_F + 2k) ≥ (1+ρ)k, that is Λ_F ≥ λ_S. At Δ_S both roots equal λ_S: (1+ρ)Δ_S m_{λ_S} − 2k = (Δ_S m_{λ_S} − k) + (ρΔ_S m_{λ_S} − k) = 2aλ_S + 0. Since Λ and Λ_F both rise in Δ and meet at Δ_S, the regimes are exclusive and exhaustive and λ* is continuous. Recruitment is λ̂ ≥ λ_E(τ); interior research is λ̂ < λ̄. Hence the interior recruiting equilibrium exists iff λ_E(τ) ≤ λ*(Δ) < λ̄. For the capped tuple, V(Δ, λ̄) is continuous and strictly increasing in Δ and equals aλ̄ at Δ = Δ*(λ̄) by the fixed-point identity (the regime at (Δ*(λ̄), λ̄) is the full sale exactly when λ̄ ≥ λ_S, which matches the piece of Δ* used), so research λ̄ is optimal iff Δ ≥ Δ_cap, and recruitment is τ ≤ M_λ̄.

 Non-recruiting case, e(1) = ρ (M_λ̂ < τ). t = 0 needs ρΔ/2 ≤ k, and then U_H(1) = ρΔ m_λ̂ − k < 0 contradicts lem:a5-buy, so the only equilibrium without recruitment there is Z. Interior t gives U_H(1) = ρΔ m_λ̂ − k < ρΔ b̂/(2b̂+t) − k = 0, again a contradiction. So t = λ̂, U_H(1) = U_L(−1) = ρΔ m_λ̂ − k, V = ρΔ m_λ̂ − k, and λ̂ = min{λ̄, λ_Q(Δ)} with aλ_Q = ρΔ m_{λ_Q} − k (unique root, exists iff ρΔ > 2k). It exists iff ρΔ > 2k and τ > M_{min(λ_Q, λ̄)}. The capped version needs ρΔ m_λ̄ − k ≥ aλ̄, which is condition (U) of lem:a5-strong. Always λ_Q(Δ) < λ*(Δ): if λ_Q ≥ λ*, then on the full-sale piece 2aλ_Q ≤ 2ρΔ m_{λ*} − 2k < (1+ρ)Δ m_{λ*} − 2k = 2aλ*, and on the other piece ρΔ m_{λ*} ≤ k forces λ_Q ≤ 0.

3. Monotonicity by implicit differentiation of the two fixed-point equations, with m′ < 0; the slope ratio at Δ_S follows since the numerator exceeds the denominator by 2aρ. Entry: Pr(X = 1) = ½(b̂+λ̂) + ½b̂ = β + (1/2−β)λ̂, independent of t, and only a purchase recruits.

4. Every branch point has J > k, so the branch starts after s_A: on the abstaining and mixed pieces, λ* ≥ λ_E gives m_{λ*} ≤ 1−τ and J ≥ Δ m_{λ*} = 2aλ* + k > k; on the full-sale piece ρJ ≥ ρΔ m_{λ*} ≥ k.

5. Path. {s : λ_E(τ(s)) ≤ λ*(Δ(s)) < λ̄} is [s_R, s_cap) under the single crossing of ψ(s) = λ*(Δ(s)) − λ_E(τ(s)) before the cap; {Δ(s) ≥ Δ_cap, τ(s) ≤ M_λ̄} is [s_cap, s_C] because both coordinates are nondecreasing.

Conditions: the standing hypotheses; rule IM for the mixed-sale piece (Δ_N, Δ_S) and, at the cap, for Δ_N < Δ < k/(ρ m_λ̄); C1 at the ties M_λ̂ = τ. The only path condition is one crossing of the research-recruitment curve before the cap. Along a stochastically ordered path with ranked classes, Δ and τ are nondecreasing, so the path moves right and up in the plane; the start curve and the "interior ceiling" are the same curve, crossed in opposite directions.

Benchmark check:
- Benchmark (h = 10, ℓ = 1, p = 1/2, ρ = 1/4, c_H = 6, k = 1/50, β = 0.294655, λ̄ = 0.336122, a = 1/40). r_R = 1.501023 and λ*(r_R) = 0.193853 reproduce the registry values. λ_S = 1.2 > λ̄, and Δ_cap = 0.136856 < Δ_N = 0.16, so the interior branch sits entirely on the abstaining piece: the manuscript's [r_R, r̄_R) = [1.501023, 1.677633) is right. The capped recruiting equilibrium continues past r_N = 1.747878: the low class abstains on [r̄_R, r_N], mixes on (r_N, 2.124148) with σ_L(−1) = 0.129 at r = 1.8, 0.387 at 1.9, 0.655 at 2.0, and sells after every success from r_S^cap = 2.124148 (where ρΔ m_λ̄ = k) to the ceiling r_C = 3.592659. V ≥ aλ̄ = 0.008403 throughout (0.0115 at r_N, 0.0236 at 2.0, 0.137 at 3.59). Entry is 0.522757 on all of [r̄_R, r_C]. All conditions recomputed at r = 1.745, 1.76, 1.9, 2.0, 2.12, 2.13, 2.3.
- the referee's economy (h = 10, ℓ = 1, p = 1/2, c_H = 4.5, k = 1/2, ρ = 1/2, β = 0.2, a = 0.01, λ̄ = 0.4). λ_S = 25, so the full-sale piece is never reached. r_R = 4.033383 (ψ crosses zero once), r_N = 5.828427, r_cap = 7.281329. The branch is R on [4.03, 5.83] and RQ on (5.83, 7.28): research 0.190390 (r = 5), 0.281144 (r_N), 0.341339 (6.5), 0.399909 (7.28); entry 0.628559, 0.642172, 0.651201, 0.659986; σ_L(−1) = 0, 0, 0.126, 0.213. At r = 6.5: μ = (0.430, 0.363, 0.782), U_H(1) = 2aλ* = 0.006827, U_L(−1) = 0, V/a = λ*. All conditions hold at r = 5.0, 5.5, 5.8284, 5.9, 6.2, 6.5, 6.8, 7.0, 7.2, 7.28. ψ stays positive to r = 9; the capped branch continues to the ceiling r_C = 8.914 < h. So "research rises with strength" holds on the connected set [4.03, 7.28), through r_N, exactly as the brief asked.
- A three-regime economy (benchmark auction with c_H = 5, ρ = 1/2, k = 1/50, benchmark slot, a = 1/10): λ_S = 0.1 < λ̄. r_R = 1.401294, r_N = 1.487922, r_S = 1.541411 (Δ_S = 0.095084; Λ(Δ_S) = Λ_F(Δ_S) = 0.1000 to 1e-15), r_cap = 2.041831 (Δ_cap = 0.265794). Research 0.058043 (1.45, abstain), 0.076578 (1.49, mixed), 0.094847 (1.53, mixed, σ_L(−1) = 0.83), 0.105113 (1.55, full sale), 0.236761 (1.8), 0.335456 (2.04); entry 0.6533 to 0.6818. The slope dλ*/dΔ is 1.555 on the mixed side of Δ_S and 2.064 on the full-sale side (analytic; the finite-difference slopes 1.58 and 2.03 bracket the kink). All conditions hold at 13 points on the interior branch, at the capped tuple with full sale at r = 2.05, 2.1, 3.0, 4.0, 6.3, and recruitment stops at r_C = 6.325 (at r = 6.4 the capped tuple is the non-recruiting one, entry 0.5).

What is lost:
- "Class L abstains on the branch" and "the low class is out of the market": the order pattern changes twice along the branch (at Δ_N and at Δ_S).
- "Zero research is an equilibrium along the whole branch" holds only up to Δ_N (in the benchmark it does hold, since r̄_R < r_N). Past Δ_N zero research turns into a non-recruiting research equilibrium (Candidate 3).
- Rule IM on the mixed piece. Under I0 the recruiting equilibrium is absent on (Δ_N, Δ_S) and, at the cap, on (Δ_N, k/(ρm_λ̄)); what exists there is the non-recruiting branch, when τ > M_{λ_Q}. Checked: in the referee's economy under I0 the only equilibrium past r_N is non-recruiting, with research 0.0068 at r = 5.9 and 0.123 at 7.28 (research collapses at r_N). In the benchmark, r_X = 2.167 (where the non-recruiting branch dies) exceeds r_S^cap = 2.124, so under I0 some equilibrium exists at every strength, but the recruiting one is absent on (r_N, 2.124).
- λ* is C¹ only piecewise (one kink at λ_S); the manuscript's smoothness claim holds on each piece.
- Nothing is claimed about ownership: it is ½W_H[ρ + (1−ρ)(β + (1−β)·research)] in every regime and carries W_H, as the scan notes.

## Candidate 2: Keep the abstaining branch; the condition is auction-free

Angle: primitive condition

Intuition: With class L required to abstain, the branch ends at the cap rather than at the first low-class sale exactly when research reaches its cap at a spread below the no-trade spread. Both spreads are fixed by the slot and the research technology, not by the auction. So whether the manuscript's branch ends at the cap is a property of the trading environment; the incumbent family only decides whether the path reaches those spreads.

Formal statement: The abstaining branch (R of lem:a5-middle) ends at the cap and not at the low class's first sale, for every path whose spread reaches Δ_cap while recruiting, if and only if

 ρ(2aλ̄ + k) ≤ 2k m_λ̄,  equivalently  Δ_N m_λ̄ − k ≥ 2aλ̄,

in words: at the no-trade spread 2k/ρ a capped recruiting purchase already pays the marginal research cost at the cap. Equivalent forms: a ≤ a_N = k(2m_λ̄ − ρ)/(2ρλ̄), which needs 2m_λ̄ > ρ; or ρ ≤ ρ_N = 2k m_λ̄/(2aλ̄ + k). The condition involves only (ρ, k, a, λ̄, β). When λ̄ ≥ λ_S the condition fails automatically (ρΔ_cap m_λ̄ ≥ k > 2k m_λ̄ since m_λ̄ < 1/2), so it also implies λ̄ < λ_S.

With it, the manuscript's statement holds in general: along a path on which φ_a = J − k − 2aλ_E(τ) crosses zero once from below, the abstaining branch is [s_R, s_cap), it ends where research reaches the cap, and research and entry rise strictly on it wherever Δ rises strictly.

Derivation: On the abstaining branch ρΔ ≤ 2k, and the cap is reached at Δ_cap = (2aλ̄ + k)/m_λ̄ (fixed point at λ̄). The branch reaches the cap before the first sale iff Δ_cap ≤ Δ_N = 2k/ρ; multiply out. Necessity: if Δ_cap > Δ_N and the path's spread passes Δ_N while recruiting, the abstaining tuple fails (E5) for class L there, so the abstaining branch ends at s_N (the referee's counterexample). Sufficiency given single crossing: for s_R ≤ s < s_cap, Δ < Δ_cap ≤ Δ_N keeps the low class out, and lem:a5-middle applies.

Single crossing of φ_a. Along a path with τ′ > 0, φ_a′ > 0 is J′ > 2a λ_E′(τ) τ′ with λ_E′(τ) = β/[β + (1−2β)(1−τ)]² ∈ (4β, 1/β). So single crossing holds whenever a < a_mono := inf over the path of J′[β + (1−2β)(1−τ)]²/(2βτ′), and a cruder sufficient bound is a ≤ (β/2) inf dJ/dτ. In elasticity form: the spread's elasticity to the threshold along the path must exceed τ/(1−τ) + 2aτλ_E′(τ)/(k + 2aλ_E(τ)); at a = 0 this is "J increasing", the condition the paper already certifies for Proposition 3. J increasing alone does not give single crossing for a > 0: the needed inequality J′ > 2aλ_E′τ′ is strictly stronger than J′ > 0. First-order construction at the benchmark r = 1.6: moving incumbent mass ε = 0.1 from below the reserve to y₀ = 0.75 (read as a narrow continuous bump at y₀, so F stays continuous; the first-order effect is the same) leaves Δ and γ unchanged, lowers g_L and raises τ by 0.0281ε (so J falls by Δ·0.0281ε); adding dr = 0.004 of uniform strengthening gives dJ = +0.000094 while dφ_a = −0.000133. This is a first-order calculation, not an exact two-parameter path.

Conditions: as stated; (C-cap) is necessary and sufficient for Δ_cap ≤ Δ_N, and together with single crossing of φ_a necessary and sufficient for the manuscript's interval claim on a path that reaches Δ_cap while recruiting. The a_mono bound is sufficient and far from necessary (the benchmark φ_a is single-crossing for every a ≤ 0.3 on the grid; for a ≥ 0.5 the branch is empty).

Benchmark check: ρ(2aλ̄ + k) = 0.009202 ≤ 2k m_λ̄ = 0.010758, margin 0.001556. a_N = 0.034259 against a = 0.025 (a/a_N = 0.73). ρ_N = 0.292279 against ρ = 0.25 (margin 0.042). In strength, r̄_R = 1.677633 < r_N = 1.747878, margin 0.070245 (the registry's margin_res_rN_B). a_mono ≈ 0.469 on the whole path [r_0, r_2] (grid step 0.005, finite differences), against the manuscript's 0.161713 on [r_0, 7/4], which used uniform bounds on the four factors; a = 0.025 is 19 times below the exact bound. φ_a changes sign exactly once on [1.2, 3.6] for a ∈ {0.025, 0.1, 0.16, 0.2, 0.3} and never for a ∈ {0.5, 1}.

What is lost: nothing relative to the manuscript, but the statement stays conditional on a slot inequality with a thin ρ margin, and it says nothing about the economy past Δ_N, where the research branch in fact continues.

## Candidate 3: The research map in the (Δ, τ) plane, and the benchmark's gray band

Angle: reformulate

Intuition: Past the no-trade spread, zero research does not disappear; it becomes a low-research equilibrium in which both classes trade after a success at the entry floor and no purchase recruits. This non-recruiting branch and the recruiting branch coexist on a band, exactly as the forms F and Q coexist in Proposition 3 at a fixed presence. The band (r_N, r_U) that the research figure leaves blank is fully described.

Formal statement: At (Δ, τ) with τ > 1/2, under IM and C1, the equilibrium set is exactly:
- Z (no research, no trade) iff ρΔ ≤ 2k;
- the recruiting research equilibrium, interior λ*(Δ) if λ*(Δ) < λ̄ and capped otherwise, iff τ ≤ M_{min(λ*(Δ), λ̄)};
- the non-recruiting research equilibrium (class H buys, class L sells after every success, entry ρ), interior λ_Q(Δ) if λ_Q(Δ) < λ̄ and capped otherwise, iff ρΔ > 2k and τ > M_{min(λ_Q(Δ), λ̄)}.
Under CM, threshold tuples are added at M_λ̂ = τ only. Since λ_Q < λ*, the two research equilibria coexist exactly on M_{min(λ_Q,λ̄)} < τ ≤ M_{min(λ*,λ̄)}. Along a path with Δ and τ nondecreasing: zero research continues past s_N as the non-recruiting branch with research λ_Q(Δ) rising from zero (dλ_Q/dΔ = ρm/(a − ρΔm′) > 0); if τ − M_{min(λ_Q,λ̄)} crosses zero once from above, at s_X, the non-recruiting branch dies there, and on (s_X, s_C] the recruiting equilibrium, interior before s_cap and capped after, is the unique equilibrium, so uniqueness holds from s_X and not only from s_U (condition U is the point where non-recruiting research would reach the cap, and matters only if s_U < s_X).

Derivation: Step 2 of Candidate 1 is the full classification; λ_Q < λ* is shown there. The non-recruiting fixed point aλ = ρΔ m_λ − k has a left side rising and a right side falling in λ, so it is unique; implicit differentiation gives the slope. The uniqueness on (s_X, s_C] lists the candidates: Z needs ρΔ ≤ 2k; interior recruiting needs Δ < Δ_cap; non-recruiting needs τ > M_{min(λ_Q,λ̄)}; CM ties need M = τ.

Conditions: standing hypotheses; IM where the capped recruiting tuple has a mixed low class; the single crossing of τ − M_{min(λ_Q,λ̄)} for the "dies once" statement.

Benchmark check: r_X = 2.166995. On (r_N, r_X) two research equilibria coexist: at r = 2.0 the recruiting one has research λ̄ and entry 0.522757, the non-recruiting one has research λ_Q = 0.154369, posteriors (0.382, 0.5, 0.618), entry 0.25; both pass every condition. At r = 1.75, λ_Q = 0.0015 (the continuation of Z). At r = 2.3, M_{λ_Q} = 0.704 > τ = 0.676: the non-recruiting tuple no longer exists (the recomputation at r = 2.3 fails (E7) because its purchase recruits, which confirms the death, not a verification failure). r_U = 2.434046 recomputed; r_X < r_U, so in the benchmark the capped recruiting equilibrium is unique on (2.167, 3.593) under IM and C1, and research is at the cap in the recruiting equilibrium on all of [r̄_R, r_C] = [1.678, 3.593]. The research figure's gray band (r_N, r_U) with the broken axis can be drawn: cap on the recruiting branch throughout, plus the non-recruiting branch rising from 0 at r_N to 0.24 at r_X with entry ρ. In the referee's economy the non-recruiting branch exists at every r in [5.9, 9] (λ_Q = 0.0068 to 0.235), coexisting with the recruiting branch.

What is lost: the simple two-equilibrium story (zero research against the branch) becomes a three-regime map; the statement "the equilibrium is unique above r_U" is kept but is no longer sharp.

## Importance of the weakness

The parameters in the referee's counterexample are not extreme individually, but their combination is far from the benchmark in two ways. First, research is nearly free there: the marginal research cost at the cap relative to the trading cost is 2aλ̄/k = 0.016, against 0.84 in the benchmark. Second, and decisive, ρ = 0.5 exceeds 2m_λ̄ = 0.375, so the condition fails even at a = 0: the informed presence at the cap is strong (u_λ̄ = 3.3 against e − 1 = 1.72 in the benchmark) and half the challengers are zero-cost, so a floor-entry sale against the no-trade price pays before a capped recruiting purchase can. In the benchmark slot the condition holds for ρ ≤ 0.292 at a = 1/40 and for ρ ≤ 0.538 as a → 0; the benchmark's ρ-margin of 0.042 is thin. So if the abstaining-branch statement is kept as a general proposition, the condition is not a formality.

For the paper's economics the weakness is small. The content of Proposition 4(a) is that research and entry rise with strength along the branch until the cap; Candidate 1 shows this holds with no condition beyond the start, and the low class's selling strengthens the mechanism (steeper research past Δ_S). What the counterexample breaks is a description of the low class's order pattern, not the comovement. The benchmark statements are all correct as written. The general statement in A5 needs the branch redefined (recruiting purchase, free low-class order) or the auction-free condition added.

## Other findings (errors in the manuscript, anything surprising)

1. The research figure's gray band (r_N, r_U), with the horizontal axis broken, can be filled: under IM and C1 the capped recruiting equilibrium exists on all of [r̄_R, r_C] with entry 0.522757, the low class mixing on (r_N, 2.124148) and selling fully after; a non-recruiting research equilibrium exists on (r_N, r_X = 2.166995) with research rising from 0 to 0.24 and entry ρ; uniqueness holds from r_X, before r_U = 2.434046. The sentence "research stays at the cap from r̄_R to r_N and above r_U" (sections/05:141) is true but understates: in the recruiting equilibrium research is at the cap on all of [r̄_R, r_C].

2. Step 4 of "The branch at calibration B" (A5:303–307) is correct and general: no interior recruiting research exists past Δ_cap under any low-class behaviour, because V ≥ ½(Δ m_λ̂ − k) always.

3. The hypothesis ρΔ < 2k in lem:a5-middle is used only to make the low class's abstention strict. At ρΔ = 2k the tuple R survives and no other sale rate is consistent (any t > 0 makes the sale strictly unprofitable), so the lemma's set is unchanged there apart from the tie.

4. Condition (U) of lem:a5-strong is exactly "non-recruiting research sits at the cap" (Candidate 3). It is sufficient for uniqueness, not necessary: in the benchmark uniqueness starts at r_X = 2.167.

5. The manuscript's bound a_mono = 0.161713 is conservative by a factor of about 2.9 (exact infimum ≈ 0.469 on the whole path). Not an error.

6. Candidate registry keys if the general statement is adopted: λ_S = (1−ρ)k/(2aρ) (benchmark 1.2), Δ_S or r_S^R (absent in the benchmark since λ_S > λ̄), r_S^cap = 2.124148, r_X = 2.166995, ρ_N = 0.292279, a_N = 0.034259, the exact a_mono. Each needs a checker row. The status of everything here: analytical derivations with float diagnostics; no certificate was produced.

7. Sections/05:122 says the branch "ends where research reaches the cap"; sections/05:119 writes the interval with the symbol r̄_R, which collides with the support bound r̄ (already in the scan). If Candidate 1 is adopted, the interval statement needs only the single-crossing condition, and the end is "where research reaches the cap or where the threshold rises above the top posterior research can generate", whichever comes first.
