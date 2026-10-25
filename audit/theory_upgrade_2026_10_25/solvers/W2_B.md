# W2-ownership: Solver B

Notation. On the research branch (R) the prior is 1/2, as in Section 5. e_j = Pr(the challenger prepares | class j), called class-j entry. Λ(Δ) = λ_R is the root of 2aλ = Δ·m_λ − k, with m_λ = β(1−λ)/[2β + (1−2β)λ]. On (R), e_H = ρ + (1−ρ)[β + (1−β)Λ(Δ)] and e_L = ρ + (1−ρ)β[1 − Λ(Δ)]. ε_e(Δ) = Δ·e_H′(Δ)/e_H is the spread elasticity of class-H entry. Along a stochastically ordered path F_s, η(s) = −(d ln W_H/ds)/(d ln Δ/ds) is the spread elasticity of the high class's win probability, with the sign flipped so that η ≥ 0. q_H(x) is the probability that a prepared class-H challenger beats an incumbent of value x: it is 1 if x < p and Pr_H(θ > x) if x ≥ p. It does not depend on F.

Scripts: `audit/theory_upgrade_2026_10_25/solvers/computations/W2_B/` (`model.py`, `run1` to `run9`). Every number below was printed by them.

## Candidate 1: Two channels. Against an incumbent of any given value, competition gives the target to the high class more often

Angle: reformulate. The exact condition for the level follows as a corollary.

Intuition: High-class ownership is the product of two probabilities: that a class-H challenger prepares (e_H), which only information moves, and that, once prepared, it outbids the incumbent (W_H), which only the stronger incumbent's own bidding moves. On the research branch the first rises with the spread with no condition. The second falls only because the incumbent's value exceeds the challenger's more often, which means the incumbent is then the better owner. The fall in the level is therefore efficient, and the paper's mechanism lives in e_H.

Formal statement.
1. (Any prior, any equilibrium, ranked classes, continuous F.) O_H(F) = π·e_H·W_H(F). For every incumbent value x, Pr(class H acquires | R = x) = π·e_H·q_H(x). The capture rate is Pr(class H acquires | j = H, θ beats R) = e_H. By the reduction lemma, e_H depends on the auction only through (Δ, τ).
2. (Fixed information.) In the fixed-information control of Proposition A.3, with the signal law, the cost law and the classes fixed, a strengthening F_0 → F_1 weakly lowers e_H. So it weakly lowers high-class ownership against every incumbent value and in total.
3. (Research branch, prior 1/2, 0 < β < 1/2, a > 0.) e_H = ε(Δ) := ρ + (1−ρ)[β + (1−β)Λ(Δ)] is a C¹, strictly increasing function of Δ alone on Δ > 2k. Take any stochastically ordered path and two laws at which (R) is an equilibrium. Between them the capture rate e_H rises weakly, and so does ownership against every incumbent value x with q_H(x) > 0; both rise strictly when Δ rises strictly. The no-research equilibrium (Z) exists at every law where (R) does, and O_H^R/O_H^Z = ε(Δ)/ρ rises with Δ.
4. (Level, corollary.) Total ownership rises between two branch laws if and only if ε(Δ_1)/ε(Δ_0) > W_H(F_0)/W_H(F_1). Along a differentiable path it rises locally if and only if ε_e(Δ) > η.

Remark (incumbent's loss, also unconditional). At prior 1/2, Pr(the incumbent loses | R = x) = ½[e_H·q_H(x) + e_L·q_L(x)]. Its derivative in λ_R is ½(1−ρ)[(1−β)q_H − βq_L] ≥ ½(1−ρ)(1−2β)q_H > 0, because the class ranking gives q_H ≥ q_L. On (R), an incumbent of any given value therefore loses the target more often when it is publicly stronger.

Derivation.
- Factorization. Preparation depends on the price and on the cost C. The price is a function of the order, and the order depends on the class and the slot draws. Given j, all of these are independent of (θ, R). So Pr(H acquires) = π·Pr(prepare | H)·Pr(θ beats R | H) = π·e_H·W_H, with W_H = ∫q_H dF = E_H[F(θ)] (F continuous). Conditioning on R = x replaces W_H by q_H(x). Conditioning on {j = H, θ beats R} leaves Pr(prepare | H) = e_H.
- Fixed information. Under rule C1, e_H^fix(F) = E[1{C ≤ B_F(μ(S))} | j = H]. The joint law of (S, C) given j is fixed, and Proposition 1(a) gives B_{F_1}(μ) ≤ B_{F_0}(μ) at every μ, so the indicator weakly falls pointwise. W_H weakly falls under first-order dominance, so π·e_H^fix·W_H weakly falls. The same holds with a fixed tie probability, by the argument in the A.3 proof.
- Branch formula. On (R), class H buys after a success. A purchase has probability (1−λ)β + λ = β + (1−β)λ in class H and β(1−λ) in class L, and only a purchase recruits (Lemma A5-middle). This gives e_H and e_L. Implicit differentiation of 2aλ = Δm_λ − k gives Λ′(Δ) = m/(2a − Δm′) = m/(2a + Δ|m′|) > 0, since m′ = −β/[2β + (1−2β)λ]² < 0. Hence ε′(Δ) = (1−ρ)(1−β)Λ′ > 0. Under the class ranking, Δ weakly rises along the path (Proposition 1(b)), and strictly when ∫(F_0 − F_1)D > 0.
- (Z) coexists. (R) requires 1/2 < τ < 1 and ρΔ ≤ 2k (the branch set in SCAN Part 1). At the same law, zero research with abstention is an equilibrium. After a hypothetical success U_H(1) = U_L(−1) = ρΔ/2 − k ≤ 0, and B(1/2) < c_H gives entry ρ (Lemma A5-middle, Step 1; at ρΔ = 2k, use a tie rule that lets an indifferent investor abstain). So O^Z = πρW_H, and the ratio is ε(Δ)/ρ.
- Level. ln O_H = ln π + ln ε(Δ) + ln W_H, so d ln O_H/ds = (ε_e − η)·d ln Δ/ds.

Conditions: the class ranking, a continuous F, and the research branch as defined in A5 at prior 1/2. Nothing about W_H.

Benchmark check. In the benchmark W_H = 1, so e_H = 2·O_H. e_H is 0.5735 at r_R = 1.5010; 0.5968, 0.6186 and 0.6385 at r = 1.55, 1.60 and 1.65 (twice `res_own_*`); and 0.6486 at r̄_R. In the counterexample (h = 10, ℓ = 1, p = 1/2, c_H = 2.5, ρ = 0.05, k = 0.2, β = 0.2, a = 5, λ̄ = 0.9), from r = 11 to r = 12:

| Quantity | r = 11 | r = 12 | Change |
|---|---|---|---|
| Capture rate e_H | 0.346355 | 0.353531 | +2.07% |
| Ownership against an incumbent of value x < 10 | 0.173177 | 0.176766 | rises |
| O^R/O^Z | 6.927 | 7.071 | rises |
| W_H | 10/11 | 10/12 | −8.33% |
| Total ownership | 0.157434 | 0.147305 | falls (reproduces the counterexample) |

ε_e is about 0.25 at both strengths.

What is lost: the level, that is, how often the high class ends up owning the target. That is the quantity an econometrician observes; the capture rate needs the incumbent's value or a counterfactual. Every unconditional reformulation is the same object e_H in a different form: ownership at a given incumbent value, the capture rate, the ratio to the no-research equilibrium, and growth relative to fixed information. The capture rate is the most useful form because it is an efficiency statement. It answers: when the high-class challenger is the better owner, how likely is the target to reach it? The level also records how often the incumbent is the better owner, which is the standard effect of a stronger rival. That makes the reformulation at least as interesting as the original. The original adds only that standard effect, which competes with the mechanism. Suggested wording for 4(a): "… research and entry rise strictly with the spread. Against an incumbent of any given value, the high class also acquires more often. High-class ownership itself, ½·e_H·W_H(F), rises when the high class outbids every incumbent on the branch, as in the benchmark."

## Candidate 2: The high class outbids every incumbent that recruitment can reach; in the benchmark this condition is exact

Angle: primitive condition

Intuition: If the high class outbids every incumbent where the branch lives, W_H = 1 and ownership is class-H entry, which rises. A cost bound delivers this without restricting the path: if a challenger known to be high class cannot cover c_H against any incumbent that can beat it, then recruitment, and with it the research branch, lives only among incumbents that the high class always beats. The condition is also close to necessary, because the information channel is weak in a precise sense: its spread elasticity is capped by a function of ρ alone, 2/3 at ρ = 1/4. With point masses, W_H's elasticity jumps above that cap the moment the incumbent can win.

Formal statement.
1. (P1) Suppose the high class outbids every incumbent on the branch: F_s(θ) = 1 for G_H-almost every θ, that is, sup supp F_s ≤ inf supp G_H. Then W_H = 1 there, and O_H = ε(Δ)/2 rises strictly with Δ.
2. (P2, no restriction on the path.) Suppose a challenger known to be high class cannot cover the high cost against any incumbent able to beat it: c_H ≥ g_H(F) for every F in the family with W_H(F) < 1. Then every law with g_H > g_L at which some order can recruit has W_H = 1. So (P1) holds on every research branch, and the ownership conditions of Proposition 2, A.4 (with c_− in place of c_H), A.5 and A.7 all reduce to e_H > ρ. For point-mass classes and uniform incumbents, (P2) reads c_H ≥ (h² − p²)/(2h).
3. (Necessary condition, independent of the auction.) For every a > 0, k > 0, β ∈ (0, 1/2) and Δ > 2k: ε_e(Δ) < Ē(ρ) := 2(1 − √ρ)/(1 + √ρ), and Ē(1/4) = 2/3. This is proved below for ρ ≤ 0.42, which covers the benchmark, and confirmed on a grid at ρ = 0.5. Ownership on the research branch therefore falls wherever η ≥ Ē(ρ).
4. (Exactness for point masses.) With point-mass classes h > ℓ ≥ p and uniform incumbents, η = 0 for r < h and η = (2r − h − ℓ)/(h + ℓ) > (h − ℓ)/(h + ℓ) for r > h. Hence, if h/ℓ ≥ (3 − √ρ)/(3√ρ − 1) (this requires ρ > 1/9, and the bound equals 5 at ρ = 1/4), ownership on the research branch rises at r if and only if r < h. This holds for every β, a, k, λ̄ and c_H.

Derivation.
- (P2). With g_H > g_L, recruitment needs a posterior μ ≤ M < 1 with c_H ≤ B(μ) < g_H, so g_H > c_H. The contrapositive of (P2) then gives W_H = 1. For Proposition 2: B_1(M) > c_H gives g_H(F_1) > c_H, so W_H(F_1) = 1, and W_H(F_0) = 1 because F_0 is weaker. With point masses and r ≥ h, g_H(r) = (h² − p²)/(2r), whose supremum over r > h is (h² − p²)/(2h).
- The bound in item 3. ε_e = (1−ρ)(1−β)Δm/{e_H[2a + Δ|m′|]} < (1−ρ)(1−β)·m/(e_H|m′|) = (1−ρ)(1−β)·N(λ)/D(λ). Here N = (1−λ)[2β + (1−2β)λ], because m/|m′| = (1−λ)[2β + (1−2β)λ], and D = e_H = ρ + (1−ρ)[β + (1−β)λ]. Let s = √ρ and y = (1+s)β − s, and write g(λ) = Ē·D − (1−ρ)(1−β)N = c_0 + c_1λ + c_2λ², where
  - c_0 = [2(1−s)/(1+s)]·y² ≥ 0, which is zero only at β = s/(1+s);
  - c_1 = (1−s²)(1−β)(1 + s + 4y)/(1+s);
  - c_2 = (1−s²)(1−β)(1−2β) > 0.

  If c_1 ≥ 0, then g ≥ c_0 ≥ 0 on λ ≥ 0. c_1 < 0 needs y < −(1+s)/4, which is possible only if s > 1/3. In that case g ≥ 0 if and only if c_1² ≤ 4c_0c_2, that is, (1−β)(1+s+4y)² ≤ 8y²(1−2β). On that region |1+s+4y| ≤ 3s−1, |y| ≥ (1+s)/4 and β < 1/4, so it suffices that 3(3s−1)² ≤ (1+s)², that is, s ≤ (1+√3)/(3√3−1) ≈ 0.651 (ρ ≤ 0.424, which covers the benchmark ρ = 1/4). A 4000 × 4000 grid confirms the same supremum at ρ = 0.5. The supremum sits at λ = 0 and β = √ρ/(1+√ρ). On any branch λ_R > 0 and a > 0, so the inequality is strict. Values of Ē(ρ):

  | ρ | 0.01 | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.50 |
  |---|---|---|---|---|---|---|---|---|
  | Ē(ρ) | 1.64 | 1.27 | 1.04 | 0.88 | 0.76 | 0.67 | 0.58 | 0.34 |
- Item 4. For r ≥ h, W_H = h/r and Δ = (h − ℓ)[1 − (h+ℓ)/(2r)], so η = (1/r)/(d ln Δ/dr) = 2rΔ/(h² − ℓ²) = (2r − h − ℓ)/(h + ℓ); p cancels. Also (h−ℓ)/(h+ℓ) ≥ Ē if and only if h/ℓ ≥ (1+Ē)/(1−Ē) = (3 − s)/(3s − 1).
- General η. Along a stochastically ordered path with ψ = −∂_sF_s ≥ 0, η = [∫ψ dG_H / W_H] / [∫ψD dy / Δ]. For the uniform family ψ(y) = y/r² on [0, r), so η(r) = Δ·E_H[θ1{θ<r}] / (W_H·∫_p^r yD(y)dy).

Conditions. (P1) restricts the path. (P2) uses only (G_H, p, the family, c_H). The bound in item 3 uses only ρ.

Benchmark check.
- (P1): the branch [1.501, 1.678) and the path [1.2, 3.6] lie below h = 10, with h/r̄_R = 5.96 and h/r_2 = 2.78.
- (P2): (h² − p²)/(2h) = 4.9875 < c_H = 6, a margin of 1.0125, so c_H is 20% above the bound. Equivalently, τ < 1 only for r < 7.969 < h. The check uses only (h, p, c_H) and the uniform family, so W_H = 1 at every strength where any equilibrium can recruit, whatever ρ, k, β, a and λ̄ are.
- Item 4: ρ = 1/4 and h/ℓ = 10 ≥ 5, so at the benchmark classes and ρ, the condition r < h is necessary and sufficient. A brute-force check (h/ℓ = 10, ρ = 1/4; wide grids over c_H, k, β and a, including a = 10⁻⁶) found 3247 branch points with r > h. Ownership falls at every one of them, and the largest ε_e − η is −0.284. At h/ℓ = 5 there are 1611 such points, and ownership falls at all of them.

How far from necessary.
- Point masses at ρ = 1/4 and h ≥ 5ℓ: (P1) is necessary and sufficient.
- Small ρ: (P1) is not necessary, but the exceptions sit in a corner. With ρ = 0.01, a = 0.001, k = 1.7, c_H = 2.734 and β = 0.2, ownership rises at r = 10.5 to 11.2 > h (at r = 10.5, ε_e = 1.16 against η = 0.91). Research there is nearly free, and the trading cost absorbs 99.99% of the purchase's gross return. With the same parameters but ρ = 0.25, ε_e = 0.54 and ownership falls.
- Continuous classes: (P1) is not necessary. Take G_H = U[8, 12], G_L = δ_1, p = 1/2, R ~ U[0, r], c_H = 3, ρ = 0.05, k = 0.6, β = 0.2, a = 0.01 and λ̄ = 0.95. The branch covers r ∈ [8.07, 12]. Ownership rises from 0.2653 to a peak of 0.28679 at r = 10.07, where W_H = 0.947 and ε_e = η = 0.443, then falls to 0.2713 at r = 12. Ownership is hump-shaped in strength: when the high class's values are spread out, the overlap with the incumbent's values grows gradually, so η starts at zero.
- (P2) is vacuous when the high-class support reaches down to the incumbents against which recruitment happens. It suits point masses and narrow class supports.

What is lost: (P1) restricts the path, and (P2) restricts c_H relative to the high class's profit. Neither covers incumbents that can beat the high class. Under the bound in item 3, those are exactly the cases where the claim generally fails.

## Candidate 3: Selection. Better entrants, and better winners among challengers

Angle: both. Part (i) is a reformulation as a conditional probability; part (ii) adds a primitive condition.

Intuition: Research adds informed purchases in class H and crowds out liquidity purchases in both classes. A stronger incumbent therefore draws in more high-class challengers and fewer low-class ones. The pool of entrants improves with no condition. Among acquisitions by the challenger, the high class's share also rises, provided a stronger incumbent does not cut the high class's win odds by more, in proportion, than the low class's.

Formal statement.
1. On (R), e_H rises and e_L = ρ + (1−ρ)β[1 − Λ(Δ)] falls, both strictly in Δ. So the high-class share of prepared challengers, π·e_H/(π·e_H + (1−π)·e_L), rises strictly with Δ. Total entry still rises, because 1 − β > β.
2. Suppose W_H/W_L is nondecreasing along the path. A sufficient condition is that G_H dominates G_L in the likelihood-ratio order and that F_{s′}/F_s is nondecreasing in y for s′ > s (the reverse-hazard order, which the uniform scale family satisfies). Then Pr(H | the challenger acquires) rises on (R).

Derivation. Part 1 is direct from the branch formulas. For part 2, the odds are [π/(1−π)]·(e_H/e_L)·(W_H/W_L). Let φ = F_{s′}/F_s, which is nondecreasing. Then W_j(s′)/W_j(s) = E^{(j)}[φ] under the measure proportional to F_s dG_j. The likelihood-ratio order survives the common reweighting by F_s and implies first-order dominance, so E^{(H)}[φ] ≥ E^{(L)}[φ].

Benchmark check. Point masses satisfy the likelihood-ratio order. The uniform family satisfies the reverse-hazard order: F_{r′}/F_r equals r/r′ below r, y/r′ on [r, r′) and 1 above, which is nondecreasing. For ℓ ≤ r ≤ h, W_H/W_L = r/ℓ. On the benchmark branch, from r_R to r̄_R, e_L falls from 0.4282 to 0.3968 and e_H rises from 0.5735 to 0.6486. In the counterexample, from r = 11 to r = 12, the high-class share of entrants rises from 0.6187 to 0.6256, and its share of challenger acquisitions rises from 0.94196 to 0.94352 (W_H/W_L = 10 is constant for r > h).

What is lost: the level, and incumbent wins drop out of the comparison. Part 2 needs more than the class ranking. With classes ranked only by first-order dominance, W_H/W_L can fall along the uniform path. Example: G_H = ½δ_1.5 + ½δ_3 and G_L = ½δ_1 + ½δ_3 give W_H/W_L = (0.75 + 0.5r)/(0.5 + 0.5r), which falls on (1.5, 3). I did not build an equilibrium in which the acquisition share actually falls.

## Importance of the weakness

1. In the benchmark the claim is safe, and it is in fact the class-H entry claim. W_H = 1 at every strength where recruitment is possible (τ < 1 only for r < 7.969 < h = 10), whatever the slot and research parameters, so O_H = e_H/2.
2. The counterexample's parameters are not extreme. Against the benchmark:

   | Parameter | Counterexample | Benchmark |
   |---|---|---|
   | c_H/h | 0.25 | 0.6 |
   | ρ | 0.05 | 0.25 |
   | β | 0.2 | 0.295 |
   | k/Δ | ≈ 0.044 | ≈ 0.18 at r = 1.6 |
   | a/Δ | ≈ 1.1 | ≈ 0.22 |
   | λ̄ | 0.9 (not binding) | 0.336 |

   Research responds to the spread with the same elasticity as in the benchmark: ε_e ≈ 0.25 against 0.24 to 0.26. What drives the counterexample is that its whole branch, r ∈ (10.05, 13.22), lies above h. The incumbent beats a prepared high-class challenger with probability 1 − 10/r, which is 9% to 17% at r = 11 to 12. The high cost is low enough (c_H < g_H(r) ≤ h/2) that a challenger known to be high class still prepares against such incumbents. Neither feature is unusual: initial bidders often win real contests, and a preparation cost below half the high value is common. Ownership falls along the entire branch.
3. The failure is generic once W_H < 1; it is not a tuned corner. With point masses, η ≥ (h−ℓ)/(h+ℓ) = 9/11 as soon as r > h, while at ρ = 1/4 the bound caps ε_e below 2/3 for any research technology. With point masses and ρ = 1/4, the claim therefore fails at every strength where the incumbent can win. With continuous classes, ownership is hump-shaped in strength. Ownership rises past r = h only at small ρ with nearly free research.
4. Comparison with Proposition 2. There information switches on (e_H/ρ = 2.595 in the benchmark), so ownership rises unless W_H falls by more than 61%. On the research branch information moves smoothly, with a spread elasticity of about 1/4, so any material fall in W_H dominates. The ownership claim on the research branch is fragile in a way Proposition 2's is not.
5. For the paper's economics the importance is low. Entry and research respond to the spread with no condition, and that response is the paper's mechanism. The weakness touches only the allocation reading, and there the fall in the level is efficient: the incumbent wins only when its value is higher. Candidate 1's capture rate states the mechanism's consequence for allocation without any condition.

## Other findings (errors in the manuscript, anything surprising)

1. Proposition 4(a) as currently stated is correct. "The benchmark auction" carries eq. (order) r < h (02_model:81–83). Independently, the benchmark c_H = 6 confines every recruiting equilibrium to r < 7.969, so the proof's "W_H = 1 because h > r" (A5:281) holds either way. The weakness enters with the scan's proposed generalization (λ_R = Λ(Δ) for ranked classes along a stochastically ordered path). It also enters through the prose at 05_research:44–46 ("research, entry and high-class ownership then rise together with incumbent strength"), which reads as general.
2. New: on the research branch, class-L entry falls: e_L = ρ + (1−ρ)β(1 − λ_R). The paper notes that research removes liquidity orders in both classes (05:115–117) but does not state the consequence: the entrant pool improves on both margins (Candidate 3, part 1).
3. New: the cap ε_e < 2(1−√ρ)/(1+√ρ), which does not depend on the auction, limits how strongly research-driven class-H entry can respond to the spread. It bounds any comparison that weighs entry against a direct auction effect, not only ownership.
4. (P2) is a single cost inequality that makes W_H = 1 wherever recruitment can occur, so it covers Propositions 2, A.4, A.5, A.7 and 4(a) together. A candidate registry key is c_H − (h² − p²)/(2h) = 1.0125, or equivalently the strength 7.969 at which τ = 1. It certifies more than SCAN's proposed `margin_WH_B` = h − r_2, which covers only the path.
5. A.7's ownership "e_H/2, since h > r_1" (A6:489) is correct under its point-mass hypothesis. Under the scan's extension to ranked classes it becomes π·e_H·W_H(F_1), and any claim that ownership rises then needs Proposition 2's condition.
6. The sufficient condition for Proposition 2's ownership claim stated in Section 4 (04:65–67: (1+ρ)W_H(F_1) ≥ 2ρW_H(F_0) > 0 and b + λ > 1/2) is correct, because b + λ > 1/2 gives e_H > (1+ρ)/2. In the benchmark, b + λ = 0.5317.
