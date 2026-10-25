# W2-ownership: Solver G

Provenance. I continued from `solvers/W2_F.md`. Its scratch folder was empty. I read the study brief,
`W2.md`, `SCAN.md`, `sections/02_model.tex`, `03_competition_information.tex:60-141`,
`04_equilibrium_results.tex:1-120, 180-240`, `05_research.tex`, `appendix/A1_payoffs.tex:60-217`,
`A3_proposition2.tex:1-158`, `A5_research.tex:1-320`, `A6_robustness.tex:1-262, 375-500`, `A8_empirical.tex:166-195`,
`A9_parameters.tex:1-60`, the intro, abstract and conclusion passages on ownership, and the registry values in
`numbers.tex`. Every number below comes from five print-only scripts in `audit/theory_upgrade_2026_10_25/solvers/computations/W2_G/`
(`recompute.py`, `share.py`, `bounds.py`, `check.py` and `mixdigits.py`). They use mpmath at 30
to 40 digits, β = 0.294655 as an exact decimal, u = e − 1 and λ̄ = uβ/(1 + uβ). Tags: **[Solver F]** means the idea is
in the Solver F notes and I re-derived and recomputed it here; **[new]** means it was added in this takeover. Every
Solver F number I keep was recomputed. Some Solver F claims did not survive (see Other findings).

Recomputation status. The counterexample of W2.md reproduces to six places: entry 0.279883 → 0.282574 and O_H
0.157434 → 0.147305. Every branch margin is strict at r = 11 and 12:
- τ − 1/2 = 0.0480 and 0.0985;
- ρΔ − 2k = −0.175 and −0.156;
- φ_a = 1.427 and 0.864;
- λ̄ − λ_R = 0.760 and 0.751.

The failure therefore holds on an open set of parameters. The benchmark registry values reproduce to six places:
- `res_lambda` 0.237901, 0.279037, 0.316683;
- `res_entry` 0.507630, 0.513965, 0.519763;
- `res_own` 0.298422, 0.309302, 0.319260;
- r_R = 1.501023, r̄_R = 1.677633, r_N = 1.747878;
- λ_E(r_R) = 0.193853;
- `own_r1_B` 0.324401.

## Candidate 1: Ownership through information, against a given incumbent

Angle: both. Parts (a) to (c) are reformulations that need no condition. Part (d) is the level claim and its condition.

Intuition: A stronger incumbent changes high-class ownership through two channels: through the price, a wider spread
draws more research and more class-H challengers, and through the auction, the stronger incumbent beats a prepared
class-H challenger more often. The first channel is the paper's mechanism, and it raises the probability of a
high-class takeover against every given incumbent value with no condition. The second is ordinary competition,
the only channel left once information is held fixed. It disappears when class H always outbids the incumbent.

Formal statement. Take the prior 1/2, classes under the class ranking, 0 < β ≤ 1/3, a > 0 and 0 < λ̄ < 1. Let F_1
be a continuous first-order stochastic strengthening of the continuous law F_0, and let the research branch (R) of
Lemma a5-middle be an equilibrium at both. Write e_H(F) = ρ + (1 − ρ)[β + (1 − β)λ_R(F)] for class-H entry. Let
S_H(x) = Pr_H(θ > x) for x ≥ p and S_H(x) = 1 for x < p.

- (a) [new] *Against a given incumbent.* For each incumbent value x, the probability that a class-H challenger
  acquires the target given R = x is ½·e_H(F)·S_H(x). It is weakly higher at F_1 than at F_0. It is strictly
  higher when Δ(F_1) > Δ(F_0) and S_H(x) > 0.
- (b) [Solver F] *Against the same incumbent law without research.* At every branch point the zero-research
  equilibrium (Z) coexists, and its high-class ownership is ½ρW_H(F). The branch multiplies it by
  e_H/ρ = 1 + (1 − ρ)[β + (1 − β)λ_R]/ρ, and this factor rises with strength.
- (c) [new] *Fixed information.* Hold the research intensity and the orders at their F_0 values. The strengthening
  then cannot raise high-class ownership. More generally, in the setting of Proposition A.3 (any signal, any cost
  law, rule C1), a stronger incumbent can only lower high-class ownership, and the decrease is exactly

  O_H^0 − O_H^1 = π·Pr(B_{F_1}(μ(S)) < C ≤ B_{F_0}(μ(S)) | H)·W_H(F_1) + π·Pr(C ≤ B_{F_0}(μ(S)) | H)·[W_H(F_0) − W_H(F_1)] ≥ 0.

- (d) *Level.* O_H(F_1) − O_H(F_0) = ½[e_H(F_1) − e_H(F_0)]W_H(F_1) + ½e_H(F_0)[W_H(F_1) − W_H(F_0)]. The first
  term (information) is ≥ 0, and the second (auction) is ≤ 0. Ownership rises if and only if
  e_H(F_1)/e_H(F_0) > W_H(F_0)/W_H(F_1). In particular it rises whenever W_H(F_1) = W_H(F_0), which Candidate 2
  turns into a condition on primitives.

Suggested text for Proposition 4(a): "On the research branch, research, entry and the entry of class H are
increasing functions of the target-payoff spread, so all three rise with incumbent strength. Against an incumbent of
any given value, a high-class takeover becomes more likely. High-class ownership itself rises when class H outbids
every incumbent against which it would prepare at the high cost."

Derivation.
1. *Factorization* [Solver F; same argument as A3 Step 4, lines 82-86]. By 02_model:96-98, (j, θ), R, the cost and the
   slot draws are mutually independent. The order depends on the class and the slot. Preparation depends on the
   price and the cost. So, given the class, preparation is independent of (θ, R). A prepared class-H challenger
   with θ ≥ p wins exactly when θ > R or R < p. So O_H(F) = π·e_H(F)·W_H(F), with W_H(F) = E_H[F(θ)] under the
   class ranking. The same independence holds after conditioning on R = x, which gives π·e_H(F)·S_H(x). Integrating
   over x ~ F returns O_H, since ∫S_H dF = E_H[F(θ)] by Fubini and the continuity of F.
2. *Class-H entry on the branch.* In (R), class H buys after a success and class L abstains. Only a purchase
   recruits: μ(1) = M_λ ≥ τ, and μ(0), μ(−1) ≤ 1/2 < τ. Class H reaches a purchase with probability
   (1 − λ)β + λ = β + (1 − β)λ, and class L with probability (1 − λ)β. Hence
   e_H = ρ + (1 − ρ)(β + (1 − β)λ_R) and e_L = ρ + (1 − ρ)β(1 − λ_R).
3. *Research is an increasing function of the spread* [Solver F formula, re-derived]. λ_R solves 2aλ = Δ·m_λ − k with
   m_λ = (1 − λ)β/[2β + λ(1 − 2β)]. Write d = 2β + λ(1 − 2β). Then dm/dλ = −β/d², and implicit differentiation
   gives Λ′(Δ) = m_λ/(2a + Δβ/d²) > 0. At the root this equals the paper's β(1 − λ)/∂_λF_r (A5:276), because
   ∂_λF_r = 2a·d + Δβ/d once 2aλ = Δm − k is used. Central finite differences agree with this formula to 10 digits:
   2.881675 at Δ = 0.10 and 2.426506 at Δ = 0.12 (benchmark slot), and 0.0256762 at Δ = 4.5 (counterexample slot).
   On the branch, therefore, e_H depends on the auction only through Δ. In the (Δ, τ) plane it does not depend on τ.
4. *The spread along the path.* Proposition 1(b) gives Δ(F_1) ≥ Δ(F_0) under the class ranking, strictly when
   ∫(F_0 − F_1)D > 0. Steps 1 to 4 give (a).
5. *(b).* Lemma a5-middle, Step 1, shows that (Z) exists whenever 1/2 < τ < 1 and ρΔ < 2k, and the branch requires
   both. In (Z), e_H = ρ. The difference ½(e_H − ρ)W_H(F) still carries W_H, so it need not rise. The Solver F notes
   said only the ratio cancels W_H, and that is correct.
6. *(c).* In Proposition A.3 the joint law of (j, S) and the cost law are fixed, and L(θ, R | j, S) = G_j ⊗ F_i.
   So, given the class, (S, C) is independent of (θ, R), and O_H^i = π·p_i·W_H(F_i) with
   p_i = Pr(C ≤ B_{F_i}(μ(S)) | H). Proposition 1(a) gives B_{F_1} ≤ B_{F_0} at every belief, so p_1 ≤ p_0. Also
   W_H(F_1) ≤ W_H(F_0), since F_1 ≤ F_0. The displayed identity is p_0W_0 − p_1W_1 =
   (p_0 − p_1)W_1 + p_0(W_0 − W_1). On the research branch take S = X with the law of (R) at λ_R(F_0). Then the
   frozen class-H entry at F_1 is e_H(F_0) if M_{λ_R(F_0)} ≥ τ(F_1), and ρ otherwise. Either way it is at most
   e_H(F_0). So the equilibrium change splits into an information effect
   ½[e_H(F_1) − ē_H]W_H(F_1) ≥ ½[e_H(F_1) − e_H(F_0)]W_H(F_1) ≥ 0 and a fixed-information effect ≤ 0.
7. *(d).* The identity is the product rule for p·W. The iff condition follows by dividing by ½e_H(F_0)W_H(F_1) > 0.

Conditions: only the branch hypotheses (1/2 < τ < 1, ρΔ < 2k, φ_a ≥ 0, λ_R < λ̄, λ_E ≠ λ̄) at both laws. W_H(F_1) > 0
is needed only for the strict form of (d). No condition on W_H is needed for (a) to (c).
Strictness: weak along any FOSD path, and strict where Δ rises strictly.

Benchmark check.
- At the benchmark W_H = 1 on the whole branch, so (a), (b) and (d) all reduce to e_H rising: 0.573541 at r_R,
  0.596843, 0.618604 and 0.638519 at r = 1.55, 1.60 and 1.65, and 0.648803 at r̄_R (+13.12% across the branch).
- The multiplier of (b) is e_H/ρ = 2.387372, 2.474417 and 2.554078. This equals the Solver F "8·O_H" values, now
  verified.
- Part (c) matches Table 3 (`tab:outcomes`), Panel B: ownership with full orders frozen is 0.324401 at both r_0 and r_1. Here the
  equality is exact, because W_H = 1 and the frozen top posterior recruits at both strengths.
- In the counterexample, (a) holds: e_H goes 0.346355 → 0.353531, and the multiplier of (b) goes 6.927 → 7.071,
  while the difference falls (0.134707 → 0.126471).
- In (c), frozen O_H(12) = 0.144314 < O_H(11) = 0.157434. The frozen purchase still recruits, since
  M = 0.644577 ≥ τ(12) = 0.598485.
- In (d), the information effect is +0.002990 and the auction effect −0.013119. Their sum, −0.010129, is the
  observed change.

What is lost: the unconditional level. Parts (a) and (b) say nothing about whether more targets end up owned by
class H, since a stronger incumbent's values are higher on average. The factorization also shows that every
ownership statement free of a W_H condition must be a statement about e_H. So (a) and (b) are class-H entry
rewritten as takeover probabilities. Their value is that they keep the ownership event and isolate exactly the
channel the paper is about. Part (a) also fits the model's own reading of strength: "Public incumbent strength is a
distribution, not a bid" (02_model:30).

## Candidate 2: Decisive advantage of class H (primitive condition), with the exact frontier

Angle: primitive condition.

Intuition: Ownership rises with strength exactly when the proportional gain in class-H entry beats the proportional
loss in its win probability. The loss vanishes if class H never loses to the incumbent wherever it would pay the high
cost. High-cost preparation needs a large expected rent. The condition therefore says that the high cost is too
large to be worth paying against any incumbent that can beat class H.

Formal statement.
- **Decisive advantage (DA)** [new]. For every F_s on the path, g_H(F_s) > c_H implies W_H(F_s) = 1. Equivalently,
  τ(F_s) < 1 implies F_s(θ) = 1 for G_H-almost every θ: wherever a challenger sure of being class H would prepare
  at the high cost, it outbids every incumbent value.
- **Never outbid (NO)** [Solver F, as "Never Outbid"] is the simplest sufficient form: inf supp G_H ≥ sup_s sup supp F_s.
  NO implies DA.
- *Claim* [new]. Under DA, every equilibrium in which some order recruits a high-cost challenger has W_H = 1, so
  high-class ownership equals π·e_H. Hence:
  - (i) the level claim of Proposition 4(a) holds along every FOSD path, weakly, and strictly where Δ rises
    strictly;
  - (ii) the ownership condition of Proposition 2 reduces to e_H > ρ and holds automatically, and the same is true of
    Proposition A.4 with c_− in place of c_H;
  - (iii) the line in A.7 "ownership is e_H/2" needs no assumption r_1 < h.
- *Uniform incumbents.* W_H(r) < 1 exactly when r > θ_min = inf supp G_H, and g_H falls in r. So, for a path that reaches strengths
  above θ_min, DA holds if and only if c_H ≥ g_H(U[0, θ_min]). For point masses this reads c_H ≥ (h² − p²)/(2h).
- *Exact frontier* [Solver F, with SCAN]. For branch points F_0 ≤ F_1, ownership rises if and only if
  log[e_H(Δ_1)/e_H(Δ_0)] > log[W_H(F_0)/W_H(F_1)]. Locally the condition is
  −W_H′/W_H < (1 − ρ)(1 − β)Λ′(Δ)Δ′/e_H.
  - [new] Uniform family, any classes: −d log W_H/d log r = 1 − Pr_H(θ ≥ r)/W_H(r), the share of class-H wins that
    come from values inside the incumbent's support (call it the at-risk share). Also
    d log Δ/d log r = rΓ(r)/∫_p^r Γ − 1. Ownership rises if and only if ε_e·(d log Δ/d log r) exceeds the at-risk
    share, where ε_e = d log e_H/d log Δ.
  - [new] Point masses beyond h: ownership rises if and only if ε_e > Δ/γ = 2r/(h + ℓ) − 1 ≥ (h − ℓ)/(h + ℓ).
- *Ceiling on the research response* [new]. ε_e < ψ(λ_R) = (1 − β)(1 − λ_R)(2β + (1 − 2β)λ_R)/(β + (1 − β)λ_R) <
  2(1 − β). So with uniform incumbents and point masses, branch ownership falls at every strength
  r ≥ (h + ℓ)(3/2 − β).
- *Point-mass bound* [new]. With point masses and any incumbent law, 1 − W_H(F) ≤ Δ(F)/(h − ℓ). The branch requires
  ρΔ < 2k, so 1 − W_H < 2k/(ρ(h − ℓ)) on every research branch. Two branch points are therefore correctly ordered in
  ownership whenever e_H(F_1)/e_H(F_0) ≥ (h − ℓ)/(h − ℓ − Δ(F_1)).

Derivation.
- *Claim.* Recruitment after an order x needs B_F(μ(x)) ≥ c_H. Every posterior is below 1 because of the full
  liquidity support, and γ > 0, so B_F(μ(x)) < B_F(1) = g_H(F). Hence g_H(F) > c_H, and DA gives W_H(F) = 1. Every
  branch point recruits after a purchase, so W_H(F_0) = W_H(F_1) = 1 and Candidate 1(d) gives the rise. In
  Proposition 2, F_1 recruits, so W_H(F_1) = 1 and also W_H(F_0) = 1, because W_H falls along FOSD and is at most 1.
  In A.4, recruitment of the high component needs B_1(M) > c_+ > c_−.
- *Uniform form.* For uniform incumbents, W_H(r) = E_H[min(θ/r, 1)], which is below 1 exactly when r > θ_min.
  Proposition 1(a) makes g_H(r) nonincreasing, and continuity gives sup_{r > θ_min} g_H(r) = g_H(θ_min). For point
  masses with r ≥ h, g_H = (h² − p²)/(2r).
- *At-risk share.* dW_H/dr = −E_H[θ/r²; θ < r], and E_H[θ/r; θ < r] = W_H − Pr_H(θ ≥ r). The formula agrees with
  finite differences to 8 digits for G_H = U[1, 19] at r = 4.5, 9 and 15, with at-risk shares 0.1285, 0.3077 and
  0.6512.
- *Beyond h.* Δ = (h − ℓ) − (h² − ℓ²)/(2r) and γ = (h² − ℓ²)/(2r), so d log Δ/d log r = γ/Δ, while
  d log W_H/d log r = −1. Hence d log O_H/d log r = ε_e·γ/Δ − 1.
- *Ceiling.* Λ′ < m·d²/(Δβ) = (1 − λ)d/Δ and e_H > (1 − ρ)(β + (1 − β)λ) give ε_e < ψ(λ). Write ψ = (1 − β)N/Q
  with N = (1 − λ)(2β + (1 − 2β)λ) and Q = β + (1 − β)λ. Then
  N′Q − NQ′ = −β(1 + 2β) − 2β(1 − 2β)λ − (1 − 2β)(1 − β)λ² < 0, so ψ falls, from ψ(0) = 2(1 − β). Over 3,000
  random (β, ρ, a, k, Δ), the largest ratio ε_e/ψ(λ_R) was 0.9726.
- *Point-mass bound.* D = 1{ℓ ≤ y < h}, so Δ = ∫_ℓ^h(1 − F) ≥ (h − ℓ)(1 − F(h)) and W_H = F(h). Then use
  W_H(F_0) ≤ 1 and W_H(F_1) ≥ 1 − Δ_1/(h − ℓ).

Conditions: DA is a joint condition on c_H, G_H and the incumbent family. It does not involve the slot, k, ρ, the
prior or the research technology.

Benchmark check.
- *DA.* The margin is c_H − (h² − p²)/(2h) = 6 − 4.9875 = 1.0125. In strengths, τ(r) = 1 at r = 4 + √63/2 = 7.9686,
  the root of 4r² − 32r + 1. No economy of the benchmark auction recruits at r ≥ 7.97, and h − 7.97 = 2.03. So in the
  benchmark auction W_H = 1 at every recruiting economy, for every slot, trading cost, ρ, prior, research cost and
  cap.
- *NO on the paper's paths.* The margins are h − r_2 = 6.4 (h/r_2 = 2.78) and h − r̄_R = 8.3224.
- *Point-mass bound at benchmark costs.* 2k/(ρ(h − ℓ)) = 0.017778. On any incumbent path, a class-H entry gain of
  1.81% between two branch points guarantees higher ownership. The uniform branch delivers 13.12%.
- *Distance from necessity.*
  - Proposition 2's exact condition tolerates a 61.47% fall in W_H at the benchmark: e_H/ρ = 2.595 [Solver F's ≈61%,
    verified].
  - Across the branch, the end-to-end comparison tolerates 11.60% [Solver F's ≈12%, verified].
  - Locally, the tolerated loss elasticity d log e_H/d log r is 1.182, 1.076 and 0.985 at r = 1.55, 1.60 and 1.65
    [Solver F's conjecture, verified].
  - Locally the frontier can fail even at the benchmark's own classes, costs, slot, a and λ̄ [new]. With
    F_c = 0.996·U[0, 1.5] + 0.004·U[c − 0.01, c + 0.01], moving c from 9.99 to 10.01 is an FOSD strengthening:
    - Δ rises by 4·10⁻⁵ and τ by 2.9·10⁻⁶;
    - research rises (0.2952730 → 0.2953709) and entry rises (0.5164659 → 0.5164809);
    - W_H falls from 1 to 0.996, and O_H falls from 0.3135966 to 0.3123680 (−0.39%).
    The branch holds throughout: τ = 0.64756, ρΔ − 2k = −0.01025, φ_a = 0.0120. As the cluster width shrinks, the
    changes in Δ and τ go to zero while the 0.4% fall in W_H stays. So no condition on the path of (Δ, τ) alone can
    sign every local comparison.

What is lost: DA excludes economies in which a high-cost challenger enters against an incumbent that sometimes beats
class H. That case is realistic when high-class synergies are dispersed. There the frontier is the honest statement.
How far DA is from necessary depends on the classes:
- With dispersed high-class values the at-risk share can be small (0.13 for U[1, 19] at r = 4.5). This is the
  wide-classes row of `tab:classes` (A6), where Proposition 2 ownership rises from 0.175 to 0.4198 with W_H = 0.9244.
- With point masses and uniform incumbents beyond h, the frontier almost never holds, and DA is close to necessary
  (see Importance).

## Candidate 3: The high class's share of entrants and of challenger takeovers

Angle: reformulate.

Intuition: Even when stronger incumbents reduce high-class takeovers, the challengers that enter, and those that win,
can be increasingly high-class. Research raises class-H entry and lowers class-L entry, so the entrant pool improves
with no condition. Among completed challenger takeovers, the high class's share rises when the strengthening cuts the
low class's win chance proportionally at least as much as the high class's.

Formal statement. On the research branch, at prior 1/2:
- (i) [new] *Entrants.* The entrant share Pr(H | the challenger prepares) = e_H/(e_H + e_L) is a strictly increasing
  function of Δ. It lies inside the reduced outcome and rises along every FOSD path, strictly where Δ rises strictly.
- (ii) [Solver F formula; new condition] *Takeovers.* Let S_H = O_H/(O_H + O_L) = Pr(H | the challenger acquires). Its
  odds are (e_H/e_L)·(W_H/W_L). So S_H(F_1) ≥ S_H(F_0) whenever W_L/W_H does not rise along the path. A sufficient
  condition on primitives: G_H dominates G_L in the likelihood-ratio order, and the strengthening is in the
  reverse-hazard-rate order (F_{s′}/F_s nondecreasing in y for s′ > s). In words, the stronger incumbent is
  proportionally rarest at low values. Point masses and uniform classes with ordered endpoints are
  likelihood-ratio ordered. The uniform scale family is reverse-hazard ordered at every r, including r > h.
- (iii) [new] *No class order alone suffices.* Solver F's conjecture, that the hazard-rate order of the classes makes
  W_L/W_H fall under every FOSD strengthening, is false.

Derivation.
- *(i).* e_H rises and e_L = ρ + (1 − ρ)β(1 − λ) falls in λ, and λ_R = Λ(Δ) is increasing.
- *(ii).* On {F_0 > 0}, write φ = F_1/F_0. It is nondecreasing, and F_1 = 0 wherever F_0 = 0. Define ν_j ∝ F_0·dG_j.
  Then W_j(F_1)/W_j(F_0) = E_{ν_j}[φ]. A common tilt preserves the likelihood-ratio order, so ν_H dominates ν_L in
  that order, hence also by FOSD, so E_{ν_H}[φ] ≥ E_{ν_L}[φ]. That is W_L/W_H(F_1) ≤ W_L/W_H(F_0). For the uniform
  family, F_{r′}/F_r is r/r′ on (0, r], y/r′ on [r, r′] and 1 above r′; this was also checked on a grid.
- *(iii).* Two point masses ℓ < h satisfy every class order (likelihood ratio, hazard rate, reverse hazard rate). Take
  ℓ = 1, h = 3, F_0 = U[0, 2] and F_1 = ½U[0, 1] + ½U[3, 4]. Then F_1 ≤ F_0 everywhere, and
  W_L/W_H = F(1)/F(3) goes from 0.5 to 1. The pair the Solver F notes used to motivate the conjecture
  (G_L = {2, 10}, G_H = {2.5, 10}) is not hazard-rate ordered: the survival ratio rises from 0.5 to 0.98 at 2.5. So
  it could not test the conjecture.

Conditions: (i) needs nothing beyond the branch. (ii) is sufficient, not necessary, since the rise in e_H/e_L can
offset a moderate rise in W_L/W_H. (The Solver F notes wrote "iff".)

Benchmark check.
- *Benchmark.* Entrant share 0.587872, 0.601796 and 0.614241 at r = 1.55, 1.60 and 1.65. S_H 0.688567, 0.707434
  and 0.724311, since W_L/W_H = ℓ/r falls.
- *Counterexample.* S_H rises (0.941960 → 0.943523) while O_H falls 6.43%, because W_L/W_H = ℓ/h = 0.1 is constant
  beyond h. The entrant share goes 0.618749 → 0.625555.
- *The non-uniform path of Candidate 2.* S_H falls (0.6995212 → 0.6987067), so (ii) needs its family condition.

What is lost: S_H is a composition among completed challenger takeovers. It can rise while high-class ownership, and
challenger takeovers overall, fall. The takeover share needs a condition on the incumbent family. The entrant share
needs no condition, but it is a statement about entry, not ownership.

## Importance of the weakness

1. *The printed result is correct.* Proposition 4(a) is stated for the benchmark auction, which imposes r < h
   (02_model eq. order). DA shows more: in the benchmark auction no recruiting economy exists at r ≥ 7.97, so W_H = 1
   on every research branch for every slot, trading cost, ρ, research cost and cap. The weakness concerns the
   general statement planned in SCAN Part 4 and the general prose at 05:44-46. It is not an error in a theorem.
2. *At benchmark costs it is small.* With point-mass classes, and along any incumbent path, the branch's own
   condition ρΔ < 2k caps the high class's losing chance at 2k/(ρ(h − ℓ)) = 1.78%. A local fall is possible
   (−0.39% on the mixture path), and the bound caps it at 1.78%. Against it, class-H entry rises 13.1% across the uniform branch.
3. *The counterexample's parameters are moderate in scale-free terms.*
   - The trading cost relative to the spread is lower than in the benchmark (k/Δ = 0.044 against 0.18).
   - ρΔ/2k is similar (0.56 against 0.70), and so is τ (0.55 to 0.60 against 0.65).
   - c_H/g_H is 0.55 against 0.66.
   - ρ = 0.05 is low but plausible.
   - The research cost a = 5 does not drive the sign. At r = 11.5, ownership falls for every
     a ∈ {0.01, …, 5}, with d log O_H/d log r between −0.86 and −0.71.

   The essential departures are two. First, c_H = 2.5 < (h² − p²)/(2h) = 4.99, so DA fails. Second, r > h, so a
   prepared class-H challenger loses with probability 9% to 17%.
4. *Beyond h the failure is the rule.*
   - In the uniform point-mass family I sampled ρ ∈ [0.003, 0.5], β ∈ [0.02, 1/3], k ∈ [0.01, 2], a ∈ [0.001, 32],
     λ̄ ∈ [0.3, 0.99], c_H ∈ [0.3, 5] and r ∈ (h, 3h). Ownership falls at 1,967 of 1,978 branch points (99.4%).
   - The exceptions need extreme values, such as ρ = 0.004, k = 1.86, a = 0.004 and λ_R = 0.02.
   - The reason is structural. Beyond h, each 1% rise in r costs class H 1% of its wins, but raises the spread by only
     (γ/Δ)% ≤ 1.22%. Meanwhile the spread elasticity of class-H entry is below ψ < 2(1 − β), and is typically
     0.15 to 0.31.
5. *For the paper's economics.* The core chain is untouched: competition widens the spread, which raises research,
   entry and class-H entry. What fails is only the last step, from class-H entry to completed high-class takeovers,
   once the incumbent can beat class H at strengths where class H would still pay the high cost. Propositions 2 and
   A.4 already carry the exact condition, A.5 constructs it, and A.7 assumes r_1 < h. Severity: a statement-scope
   problem, low to moderate. My recommendation for SCAN decision #3: state the ownership rise under DA, with "class H
   outbids every incumbent on the path" as its plain special case. Add Candidate 1(a) or (b) as the claim that needs
   no condition. Put the frontier in a remark.

## Other findings (errors in the manuscript, anything surprising)

- **Prose scope.** 05:44-46 says that "research, entry and high-class ownership then rise together with incumbent
  strength". It sits before Proposition 4, without the benchmark qualifier. It needs "when class H outbids the
  incumbent" or "in the benchmark". No other ownership statement I read is wrong:
  - Proposition 2 (04:35-39), and its sufficient condition at 04:65-67, checked;
  - A3:84-86 and A3:154-155 (b + λ = 0.531737 > 1/2);
  - A.4 (A6:92-93) and A.5's construction (A6:183-189);
  - A.7 (A6:489, under r_1 < h);
  - the abstract and introduction, which carry the open-set or benchmark qualifier.
- **Proposition A.3 extends to ownership** (Candidate 1(c)) in one line. The extension says: with information fixed,
  a stronger incumbent can only lower high-class ownership. It matches Table 3 (`tab:outcomes`), Panel B. The abstract's sentence on
  fixed information could then cover ownership as well as entry.
- **Corrections to the Solver F notes.**
  - The hazard-order conjecture is false (Candidate 3(iii)).
  - The failure does not need "sluggish research": the spread elasticity of class-H entry is about 0.25 in both the
    benchmark (0.255, 0.248, 0.242) and the counterexample (0.254, 0.259). What differs is
    d log Δ/d log r: 4.1 to 4.6 just above ℓ, where the spread is born, against 0.85 to 1.0 beyond h.
  - "Never Outbid is far from necessary" holds for end-to-end comparisons at the benchmark, but not locally in the
    uniform point-mass family beyond h.
  - The S_H condition is sufficient, not "iff".
- **SCAN Part 1 checks.** The ownership trade-off in the Proposition 4 row,
  W_H′/W_H > −(1 − ρ)(1 − β)λ_R′/[ρ + (1 − ρ)(β + (1 − β)λ_R)], is correct as written. It is the local frontier
  above.
- **Something surprising.** The benchmark's local break-even elasticity is close to 1 (1.18 to 0.98). So even a
  hypothetical W_H ∝ 1/r would roughly break even near r = 1.6. The benchmark is therefore not "barely" safe because
  of W_H = 1. It is safe because the spread grows fast there.
