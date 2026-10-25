# W5-symmetry-tests: Solver G

Takeover note. I re-derived every claim I kept from the Solver F partial notes (`solvers/W5_F.md`), and each
candidate ends with a provenance line. The Solver F author ran no code. Every number below comes from my scripts
`audit/theory_upgrade_2026_10_25/solvers/computations/W5_G/s01_calibrate.py` to `s07_classification.py` (mpmath, 50 digits, printed values, no
assertions). `s01` reproduces the registry values `lambda_B, b_B, b0_B, M_half_B, m_half_B, rS_B, rC_B, ba_class_r1_B,
ba_entry_r1_B, ba_rC_left_B, ba_rC_right_B, pdrop_neutral_r1_B, cov_entry_r1_B, evprep_mean_r1_B, evprep_mean_r2_B,
theta_max_full_eq_r1_B` to six places, so my price, entry and threshold code matches the manuscript. One Solver F claim
is wrong (the naive test does not need π = 1/2 exactly); Candidate 3(a) corrects it.

Notation at a general prior π. u = λ/b; M = M(π), m = m(π); p_x = Pr(X = x); v = p_1 + p_{−1}; e_x is entry after the
order x; A_F(μ) = w_L + Δμ with w_L = t_L − t_0 ≥ 0 (the paper's A_r, w); I₊ = P(1) − P(0), I₋ = P(0) − P(−1),
S = P(1) − P(−1); P̄ = Σ_x p_x P(x), the expected price before the order opportunity (A.14(iv)). Under full two-sided
trade (σ_H = δ_1, σ_L = δ_{−1}), Lemma A.1(d) gives the posteriors (m, π, M) after the orders (−1, 0, 1), and

    p_1 = b + πλ = b(1 + uπ),   p_{−1} = b + (1 − π)λ = b(1 + u(1 − π)),   p_0 = b_0,
    M − π = π(1 − π)u/(1 + uπ),   π − m = π(1 − π)u/(1 + u(1 − π)).

## Candidate 1: The quiet-opportunity test (frequency-weighted impacts) at every prior
Angle: reformulate

Intuition: Under full two-sided trade the price after no order sits at the prior posterior, and the posterior is a
martingale. If no order changes entry, the price is affine in the posterior, so the average price equals the price after
no order: the purchase and sale impacts, each weighted by the frequency of its order, are equal at every prior. A
purchase that recruits breaks the equality by exactly its expected recruitment value. So "the price after a quiet
opportunity lies below the average price" detects recruitment at every prior with no auction object, no slot parameter
and no knowledge of the prior; at prior 1/2 the two weights are equal and the test is A.11(ii) as written.

Formal statement. Take ranked classes, a continuous F with Δ > 0 and γ > 0, any prior π ∈ (0, 1), any slot with
0 < β < 1/2, and rule C1. Fix an equilibrium with full two-sided trade.

(i) Identity. T := p_1 I₊ − p_{−1} I₋ = P̄ − P(0) = p_1 (e_1 − e_0) A_F(M) − p_{−1} (e_0 − e_{−1}) A_F(m).
In data, T = E[P] − E[P | X = 0]: the mean price minus the mean price after a quiet opportunity.

(ii) Classification. T > 0 if and only if π < τ ≤ M (a purchase recruits: entry (ρ, ρ, 1)). T < 0 if and only if
m < τ ≤ π (a sale deters: entry (ρ, 1, 1)). T = 0 if and only if τ > M or τ ≤ m (no order moves entry). Under rule CM the
same holds when τ ∉ {m, π, M}; at τ = M, T ≥ 0 with equality iff e_1 = ρ; at τ = m, T ≤ 0; at τ = π, T can take either
sign.

(iii) Decomposition when no order is at the ceiling (π < τ, that is B_F(π) < c_H):
S = ρΔ(M − m) + (e_1 − ρ)A_F(M), I₋ = ρΔ(π − m), and both components are read off prices and frequencies:

    entry component  (e_1 − ρ)A_F(M) = T/p_1 = I₊ − (p_{−1}/p_1) I₋,
    class component  ρΔ(M − m) = (v/p_1) I₋.

The whole entry component sits in the purchase impact; the sale impact carries the share p_1/v of the class component
(1/2 only at π = 1/2). When m < τ ≤ π the mirror holds: S = Δ(M − m) + (1 − ρ)A_F(m), the entry component sits in the
sale impact, and it equals −T/p_{−1}.

(iv) Hidden price. Entry does not depend on the order, so T = 0, and S = ρΔ(M − m) when B_F(π) < c_H.

(v) Ceiling. Along an FOSD path with full trade and π < τ(s), on which Δ, w_L are continuous and τ is nondecreasing
(true when c_H ≥ g_L and γ > 0), a purchase recruits on the down-set {s : τ(s) ≤ M}. At its upper end, under C1, P(1),
I₊ and S fall by (1 − ρ)A_F(M) and T by p_1(1 − ρ)A_F(M); P(0), P(−1) and I₋ are continuous.

(vi) Uninformative-order form. In any equilibrium in which some order x° leaves the posterior at the prior,
μ(x°) = π, P̄ − P(x°) = Σ_x p_x (e_x − e_{x°}) A_F(μ(x)). If π < τ this is ≥ 0, with equality iff no order raises entry
above the floor. Under full trade x° = 0; when the low class abstains (form F, branch R, threshold pair T of A4) x° = −1.

(vii) Part (i) and A.14(iv) are one statement: P(0) − P̄ = −T. At π = 1/2, p_1 = p_{−1} = b + λ/2, and (i)–(iii) are
A.11(i)–(ii) and A.14(iv).

Derivation.
1. Bayes plausibility. Σ_x p_x μ(x) = π and μ(0) = π give p_1(M − π) = p_{−1}(π − m). Directly:
p_1(M − π) = b(1 + uπ) · π(1 − π)u/(1 + uπ) = π(1 − π)λ, and the same for p_{−1}(π − m).
2. Identity. Σ_x p_x [P(x) − P(0)] equals p_1 I₊ − p_{−1} I₋ (the x = 0 term is zero) and equals P̄ − P(0). With
P(x) = t_0 + e_x A_F(μ(x)) (Lemma A.2(b)) and A_F affine with slope Δ,
P(x) − P(0) = e_0 Δ[μ(x) − π] + (e_x − e_0) A_F(μ(x)). Weighting by p_x, the first terms sum to e_0 Δ[Σ p_x μ(x) − π] = 0,
which leaves T = Σ_x p_x (e_x − e_0) A_F(μ(x)).
3. Classification. Lemma A.2(d) under C1: e = ρ below τ and 1 at or above τ. With m < π < M the four positions of τ
give entry (1,1,1), (ρ,1,1), (ρ,ρ,1), (ρ,ρ,ρ) on (−1, 0, 1), hence T = 0, −p_{−1}(1 − ρ)A_F(m), p_1(1 − ρ)A_F(M), 0.
A_F(μ) ≥ Δμ > 0 because w_L ≥ 0, Δ > 0 and posteriors are interior.
4. Decomposition. With e_{−1} = e_0 = ρ: S = e_1A(M) − ρA(m) = ρΔ(M − m) + (e_1 − ρ)A(M), I₋ = ρΔ(π − m), and
ρΔ(M − m) = ρΔ(π − m)[1 + (M − π)/(π − m)] = I₋(1 + p_{−1}/p_1) = I₋ v/p_1.
5. (vi) repeats step 2 with x° in place of 0: e_{x°}Δ[Σ p_x μ(x) − π] = 0.
6. (v): only e_1 changes at the upper end of the down-set (1 under C1, ρ beyond it).

The floated alternatives in the brief collapse to this statistic. The prior-adjusted benchmark,
I₊ − I₋ − ρΔ[(M − π) − (π − m)] = (e_1 − ρ)A_F(M), is valid but needs ρΔ, π and u. The impact ratio scaled by posterior
moves, (I₊/I₋)·(π − m)/(M − π), needs π and u, but by step 1 (π − m)/(M − π) = p_1/p_{−1}, so it equals
p_1I₊/(p_{−1}I₋): the frequency-weighted test, which needs neither.

Conditions: full two-sided trade (or, for (vi), an order that leaves the posterior at the prior); Δ > 0, γ > 0; the
class ranking (through w_L ≥ 0). At prior π, full trade is the unique equilibrium order profile, under both investor
rules, when ρΔκ(π) > k with κ(π) = min{m(π), 1 − M(π)}, by the bounds (eq. a2-bounds) of Lemma A.3. κ is largest at
π = 1/2, so the unique-trade region shrinks away from 1/2. Full trade exists more widely, when K_L = e_{−1}Δm > k and
K_H = e_1Δ(1 − M) > k.

Benchmark check (benchmark auction and slot; the full-trade tuples at π ≠ 1/2 were checked condition by condition,
(E1)–(E6), in `s03`):

| π | r | τ(r) | entry after (−1,0,1) | I₊ | I₋ | I₊ − I₋ | T | T/p_1 |
|---|---|---|---|---|---|---|---|---|
| 1/2 | 3 | 0.705 | ρ, ρ, 1 | 0.74779 | 0.03851 | 0.7093 | 0.257948 | 0.709279 |
| 0.3 | 3 | 0.705 | ρ, ρ, ρ | 0.03968 | 0.02730 | 0.01238 | 0 | 0 |
| 0.4 | 3 | 0.705 | ρ, ρ, ρ | 0.04073 | 0.03384 | 0.00689 | 0 | 0 |
| 0.6 | 3 | 0.705 | ρ, ρ, 1 | 0.77912 | 0.04073 | 0.7384 | 0.29609 | 0.74527 |
| 0.7 | 2.0 | 0.664 | ρ, 1, 1 | 0.04095 | 0.47426 | −0.4333 | −0.12295 | — |
| 0.7 | 2.5 | 0.684 | ρ, 1, 1 | 0.07371 | 0.60054 | −0.5268 | −0.14627 | — |

At π = 1/2, r_1: T = 0.257948 = −`pdrop_neutral_r1_B` and T/p_1 = 0.709279 = `ba_entry_r1_B`. At π = 0.6, r = 3:
(v/p_1)I₋ = 0.074576 = ρΔ(M − m). At π = 0.7, r = 2: K_H − k = 0.0140, K_L − k = 0.0089, and
T = −p_{−1}(1 − ρ)A(m) = −0.122948 exactly. Unique-trade thresholds r_S(π), the root of ρΔ(r)κ(π) = k: 2.820 (π = 0.3),
2.395 (0.4), 2.246 (0.45), 2.124 (0.5), 2.246 (0.55), 2.395 (0.6), 2.820 (0.7); all lie below r_1 = 3. Part (vi) on branch
R at π = 0.55, r = 1.45 (equilibrium checked in `s07`): P̄ − P(−1) = 0.106865 = Σ p_x(e_x − ρ)A(μ_x).

What is lost: the bare comparison of two impacts. The test needs the frequencies of purchases and sales, or
equivalently the mean price across processes; §08:70–75 already records zero orders and counts, so nothing new is
measured, but the opening-auction design gives no pre-slot price, so the operational form is E[P] − E[P | X = 0] or the
frequency weighting, not a deal-level price change. The test needs an order that leaves the posterior at the prior, and
the econometrician must know which one. Outside full trade the zero order can be informative: in the purchases-only
equilibrium at π = 0.3, r = 2 (checked in `s03`), μ(0) = 0.161 < π, no order recruits, yet P̄ − P(0) = 0.00869 > 0;
there the right comparison is P̄ − P(−1) = 0. Under two-sided mixing with unequal rates (form Q at π ≠ 1/2) no order is
uninformative, and no prior-free comparison of this kind exists. "The whole entry component sits in the purchase impact"
becomes a statement about the regime π < τ.

Provenance: the weighted statistic p_1I₊ − p_{−1}I₋ and the four-regime classification are from the Solver F notes
(Candidate 1(ii)–(iii)). New here: T = P̄ − P(0) = E[P] − E[P | X = 0] and its identity with A.14(iv), the
uninformative-order form (vi), the CM boundary cases, the domain counterexample, the "sale deters" regime checked as an
equilibrium, the reduction of both floated alternatives to this statistic, and every number.

## Candidate 2: Identification at every prior: counts are silent about the informed share exactly when the prior is 1/2 or unknown
Angle: reformulate

Intuition: Under full two-sided trade the volume of nonzero orders, 2b + λ, does not depend on the prior, but the order
imbalance is λ(2π − 1). When the econometrician knows a prior other than 1/2, the imbalance reveals λ, the counts reveal
the slot, and the sale impact then reveals ρΔ, an auction object that A.12(d) had to assume. At prior 1/2 the imbalance
is zero, and A.12 is the knife-edge case. When the prior is unknown, the imbalance confounds λ with π at every prior,
so counts never identify the informed share, and the sale impact, given ρΔ, separates the observationally equivalent
(prior, slot) pairs. A.12's message, that prices separate slots that counts cannot, then holds at every prior.

Formal statement. Full two-sided trade at prior π, with π < τ (or no recruitment), any ranked classes and continuous F.

(a) Counts. The order law on (−1, 0, 1) is (b + (1 − π)λ, b_0, b + πλ). The volume is v = 2b + λ, and the informed
share of nonzero orders is ϑ = λ/v = u/(2 + u) at every prior. The imbalance is E[X] = λ(2π − 1).

(b) Known prior π ≠ 1/2. The counts identify the slot: λ = E[X]/(2π − 1), b = (v − λ)/2, β = b/(1 − λ). The sale impact
then identifies ρΔ = I₋/(π − m(π)), and Candidate 1 gives the entry component T/p_1. (In the regime m < τ ≤ π, use
I₊ = Δ(M − π) to identify Δ instead.)

(c) Known prior 1/2. A.12(a), (b) and (d) stand as written: the counts depend on (λ, β) only through v.

(d) Unknown prior. The counts identify (v, E[X]) only. The (prior, slot) pairs with the same counts are
λ′ = E[X]/(2π′ − 1), b′ = (v − λ′)/2, with π′ on the side of 1/2 given by the sign of E[X] and
|2π′ − 1| ∈ (|E[X]|/v, ū]: ū = |E[X]|/(3v − 2) when 3v − 2 > |E[X]| (the bound β′ ≤ 1/3), and otherwise ū = 1 (excluded).
This is a nondegenerate interval for every E[X], and λ′/v ranges over it, so the counts do not identify the informed
share at any prior. (At E[X] = 0 the set is A.12(a)'s family at π′ = 1/2.) Given ρΔ, the sale impact separates the
pairs: p_{−1}I₋/(ρΔ) = π(1 − π)λ, so t = 2π − 1 is the unique root in (−1, 1) of t² + 4φt − 1 = 0 with
φ = p_{−1}I₋/(ρΔ E[X]), and λ = E[X]/t; E[X] = 0 gives π = 1/2 and then A.12(d).

(e) Purchases only (Corollary A.3), known prior. Pr(X = −1) = b and E[X] = π s₊. In form F, λ = E[X]/π and
b = (v − E[X])/2. On branch R, s₊ = b[(1 − π)Δ/k − 1]/π, so E[X] = b[(1 − π)Δ/k − 1] depends on the slot only through
b: the counts identify b and πs₊ and never λ, at every prior. With the prior unknown, form-F counts identify only b
and πλ.

(f) Prices at a known prior (A.12(d) at every π). s := I₋/(ρΔ) = π − m(π, u) rises strictly in u, with inverse
u = s/[(1 − π)(π − s)]; then b = v/(2 + u) and λ = uv/(2 + u).

Derivation. (a) p_x = πf_H(x) + (1 − π)f_L(x) with f_H = (b, b_0, b + λ), f_L = (b + λ, b_0, b). (b) Solve (a); then
I₋ = ρΔ(π − m(π, u)) with u now known. (d) b′ > 0 ⇔ λ′ < v; β′ = (v − λ′)/[2(1 − λ′)] ≤ 1/3 ⇔ λ′ ≥ 3v − 2; λ′ < 1 is
implied by λ′ < v. Separation: p_{−1} = (v − E[X])/2 is fixed by the counts and
I₋ = ρΔ·π′(1 − π′)λ′/p_{−1} = ρΔ·E[X](1 − t²)/(4t p_{−1}), strictly monotone in t on each side of 0. The quadratic
follows from π(1 − π) = (1 − t²)/4; the product of its roots is −1, so exactly one lies in (−1, 1), with the sign of φ.
(e) A4's high-class lemma, form R: K_H = Δ[1 − μ₊(s)] = k with 1 − μ₊(s) = (1 − π)b/(b + πs) (A4, the formula for
μ₊), so b + πs = (1 − π)bΔ/k. Lowering λ with b fixed lowers β′ = b/(1 − λ′) and keeps s_R and the strict inequalities
J > k, s_R < λ′ and Δ(1 − M′) < k for small changes, as in the proof of Corollary A.3. (f) Solve
π(1 − π)u/(1 + u(1 − π)) = s for u.

Conditions: full two-sided trade (form F or branch R for (e)); a known prior for (b), (e), (f); ρΔ known for (d) and
(f); the regime read from the sign of T (Candidate 1) so that the right impact is used.

Benchmark check (`s05`). Known prior: at π = 0.6, r = 3 the counts are v = 0.727352, E[X] = 0.067224, giving
λ = 0.336122 and β = 0.294655 (the benchmark slot), then ρΔ = I₋/(π − m) = 0.166667 = ρΔ(3), and T/p_1 = 0.745275, the
true entry component; π = 0.4 and π = 0.55 (r = 2.5) recover the same slot and ρΔ = 0.166667 and 0.1125. Unknown prior:
the benchmark counts at true π = 0.6 are matched by every π′ ∈ (0.5462, 0.6846], with λ′ from 0.727 down to 0.182, so the
informed share λ′/v runs from about 1 down to 0.250; at true π = 0.7 the interval is (0.5924, 0.8693]. The round trip
from (v, E[X], I₋, ρΔ) recovers (π, λ, b) to ten digits at π ∈ {0.3, 0.4, 0.6, 0.7}. Branch R: at π = 1/2, r = 1.45,
s_R = 0.291736 = b[Δ/k − 2], A4's formula; at π = 0.55, s_R = 0.203127 and E[X] = 0.111720 = b[(1 − π)Δ/k − 1]; lowering
λ by 0.01 (β′ = 0.2903) keeps an R equilibrium with the same counts at both priors. Price inverse (f) returns u = e − 1
to twelve digits at π ∈ {0.3, 0.5, 0.7}. Precision: the variance of λ̂ = (p̂_1 − p̂_{−1})/(2π − 1) carries the factor
1/(2π − 1)², which is 100 at π = 0.55 and 25 at π = 0.6.

What is lost: "counts cannot identify the informed share" is false at a known prior other than 1/2; it holds at prior 1/2
and at every unknown prior. A.12(c)'s band statement is moot at a known π ≠ 1/2, where the slot is unique. Near 1/2 the
count identification is weak. The unknown-prior result still needs ρΔ.

Provenance: the general-π count formulas (also in the scan), the known-prior dichotomy, the quadratic in t, the price
inverse u(s), Corollary A.3's λ = E[X]/π and the branch-R formula (which the Solver F notes marked unchecked) are from the
Solver F notes; I verified each. New here: identification of ρΔ at a known prior other than 1/2; nonidentification at every
unknown prior with the exact feasibility interval and the price separation; the branch-R check against A4 and the
perturbation at π ≠ 1/2.

## Candidate 3: Keep the original statements under named conditions
Angle: primitive condition

Intuition: The prior enters the impact comparison only through which order is rarer: the rarer order is more
informative and moves the price more. When purchases are at least as frequent as sales, information alone cannot make the
purchase impact the larger one, so a larger purchase impact proves recruitment, and the converse needs only that
recruitment is not swamped (a zero-cost share of at most one half is ample). Separately, the entry component's trend is
not a prior question at all. Entry adds most to the target's proceeds when the incumbent alone would leave it unsold, so
a strengthening that turns walk-aways into sales at the reserve can lower the entry premium even at prior 1/2; one
condition on the strengthening restores the trend.

Formal statement.
(a) Naive impact comparison. Under full two-sided trade with π < τ, that is B_F(π) < c_H (the regime of A.11, where the
paper's "a purchase recruits", χ = 1, means e_1 > e_0):
  - If Pr(X = 1) ≥ Pr(X = −1), equivalently π ≥ 1/2, then I₊ > I₋ implies that a purchase recruits.
  - If π ≤ 1/2, or ρ < M(π)/[2π − m(π)] (true whenever ρ ≤ 1/2), then a purchase that recruits gives I₊ > I₋.
    The exact condition is (1 − ρ)(w_L + ΔM) > ρΔ(2π − m − M).
  - Hence "purchases at least as frequent as sales, and a zero-cost share of at most one half" gives A.11(ii) verbatim:
    I₊ > I₋ if and only if a purchase recruits.
  - The condition π ≥ 1/2 cannot be dropped: at every π < 1/2 every non-recruiting full-trade equilibrium has
    I₊ − I₋ = ρΔ[(M − π) − (π − m)] > 0, of relative size (I₊ − I₋)/I₋ = u(1 − 2π)/(1 + uπ).
  - Outside this regime (τ ≤ π) entry after no order is already one, so no purchase raises entry relative to no order,
    although χ = 1 when τ ≤ M; with π ≥ 1/2, I₊ < I₋ there. So under the same two conditions "I₊ > I₋ if and only if a
    purchase raises entry relative to no order" holds in every regime, but "if and only if χ = 1" holds only for π < τ.
(b) Entry-component trend. A_F(μ) = E_F[α_μ(R)], where α_μ(R) = p for R < p and α_μ(R) = ∫_p^R [1 − G_μ(y)] dy for
R ≥ p, with G_μ = (1 − μ)G_L + μG_H. For a strengthening F̃ ≤ F with δ = F − F̃ ≥ 0,

    A_F̃(μ) − A_F(μ) = ∫_p^∞ [1 − G_μ(y)] δ(y) dy − p δ(p).

A.11(iv) holds along a path with full trade and recruitment exactly when this is positive at μ = M (with Δ rising
strictly). Sufficient conditions, each in the language of primitives:
  - (S1) the strengthening leaves the incumbent's reserve-failure probability F(p) unchanged, for example the
    incumbent always meets the reserve;
  - (S2) ∫_p^{ℓ₀} δ ≥ p δ(p), where ℓ₀ is the lowest challenger value: the strengthening raises the incumbent's value,
    clipped to [p, ℓ₀], by at least p times the fall in its reserve-failure probability;
  - (S3) the uniform family U[0, r], when r and ℓ₀ both exceed √3·p.
(c) Announcements. A.14(i)–(ii) hold at every prior. A.14(iii) holds in every equilibrium when B_F(π) < c_H (that is,
π < τ). A.14(iv) holds under full trade and π < τ with b + λ/2 replaced by b + πλ = Pr(X = 1). If B_F(π) ≥ c_H, the
no-trade equilibrium, whenever it exists (Δπ ≤ k and Δ(1 − π) ≤ k), has entry one after every order and a zero mean of
preparation reports, so the condition cannot be dropped from "positive in every equilibrium".

Derivation.
(a) I₊ − I₋ = ρΔ[(M − π) − (π − m)] + (e_1 − ρ)A_F(M) when π < τ, and
(M − π) − (π − m) = π(1 − π)u²(1 − 2π)/[(1 + uπ)(1 + u(1 − π))], which has the sign of 1 − 2π. If π ≥ 1/2 the bracket is
≤ 0, so I₊ > I₋ forces e_1 > ρ. (The other regimes give I₊ ≤ I₋ when π ≥ 1/2: with τ ≤ π, I₊ − I₋ =
Δ[(M − π) − (π − m)] − (1 − ρ)A(m) < 0; with τ > M, the bracket alone.) With recruitment, I₊ > I₋ ⇔
(1 − ρ)A_F(M) > ρΔ(2π − m − M); since A_F(M) ≥ ΔM, it suffices that (1 − ρ)M > ρ(2π − m − M), that is
ρ < M/(2π − m). Also M/(2π − m) > 1/2 because 2(M − π) + m > 0, so ρ ≤ 1/2 suffices. Finally
p_1 − p_{−1} = λ(2π − 1).
(b) With G_j(p⁻) = 0, A1 gives w_j = pF(p) + ∫_p^∞ (1 − G_j)(1 − F), hence A_F(μ) = pF(p) + ∫_p^∞ (1 − G_μ)(1 − F);
subtract at F̃ and F. Tonelli and the continuity of F give A_F(μ) = E_F[α_μ(R)]. (S1) removes the last term. (S2): on
[p, ℓ₀) both classes put no mass, so 1 − G_μ = 1 there. (S3): for U[0, r] → U[0, r̃], δ(y) = y(1/r − 1/r̃) on [0, r], so
∫_p^{min(r, ℓ₀)} δ ≥ pδ(p) ⇔ min(r, ℓ₀)² ≥ 3p². Smooth form for U[0, r]:
dA_r(μ)/dr = r^{−2}[∫_p^r (1 − G_μ(y)) y dy − p²], which at the benchmark is μ/2 + (1 − 4μ)/(8r²).
(c) By (E1), Σ_x p_x μ(x) = π, so some order has μ(x) ≤ π < τ, hence e(x) = ρ under both challenger rules
(Lemma A.2(d)), and its term p_x ρ(1 − ρ)A_F(μ(x))/Pr(A) is positive because A_F(μ) ≥ Δμ > 0. For A.14(iv), Candidate
1(vii). Sharpness: in no trade all posteriors equal π ≥ τ, so e ≡ 1 under C1; no trade is an equilibrium iff
K_H = Δ(1 − π) ≤ k and K_L = Δπ ≤ k.

Conditions: as stated in each part; (a) and (c) need nothing about the auction beyond the class ranking.

Benchmark check.
(a) The benchmark (π = 1/2, ρ = 1/4) meets both parts; at π = 1/2, M/(2π − m) = 1. Over π ∈ (1/2, 1) at the benchmark
slot, min M/(2π − m) = 0.9114 (at π = 0.79), so ρ ≤ 1/2 is far from necessary (the threshold is 0.80 at u = 5 and 0.66
at u = 20). Necessity of π ≥ 1/2, on the benchmark auction: at π = 0.3 full trade is unique on (2.820, 3.6] and no
strength on the path recruits (M(0.3) = 0.538 < τ(6/5) = 0.633); the false gap is 45.4% of I₋. At π = 0.4 (unique on
(2.395, 3.6], ceiling r_C(0.4) = 1.488): 20.4%. At π = 0.45 (unique on (2.246, 3.6], ceiling 2.638): 9.7% beyond the
ceiling. A false negative needs extreme values: ρ = 0.8, u = 20, π = 0.9, U[0, 9], c_H = 5.214, k = 0.01 gives full trade
(K_H − k = 0.0087, K_L − k = 0.843) and recruitment (τ = 0.95 ≤ M = 0.995), yet I₊ − I₋ = −0.633.
(b) The benchmark fails (S1), since F_r(p) = 1/(2r) falls from 0.235 at r_S to 0.139 at r_C, but meets (S3) with
ℓ/(√3p) = 1.155, and its exact derivative is at least 0.3122 on [r_S, r_C] (minimum at r_S = 2.1241). Two
counterexamples to a trend under FOSD alone (`s04`), both at the benchmark classes, reserve, costs, slot and prior 1/2,
with unique full trade and recruitment:
  - Extreme (Solver F's): F = 0.9 U[0, 1/2] + 0.1 U[9, 10] → F̃ = 0.9 U[1/2, 1] + 0.1 U[9, 10] leaves Δ = 0.85 and lowers
    A(M) from 1.1214 to 0.8964 (τ = 0.681 and 0.709 < M = 0.731); moving the top component to U[9.02, 10.02] makes
    Δ = 0.85198 > 0.85 with A(M) = 0.8978. F(p) = 0.9 is extreme.
  - Mild (new): the incumbent is a financial buyer, value U[x − 0.3, x + 0.3], or a strategic buyer, value
    U[1.5 + e, 2.5 + e], each with probability 1/2; on the path x = 0.4 + 0.2s, e = 0.02s, s ∈ [0, 1], F(p) falls from
    0.333 to 0.167 (inside the benchmark's range 0.139 to 0.417), Δ rises strictly from 0.500 to 0.510, and A(M) falls
    strictly at every step from 0.7989 to 0.7728. Throughout, ρΔκ − k ≥ 0.0136 and τ ≤ 0.685 < M. The entry component
    falls from 0.5991 to 0.5796, so I₊ and S fall, while the class component rises from 0.05776 to 0.05892. The kernel
    formula E_F[α_M] equals w_L + ΔM to ten digits on both end points.
(c) On the path τ(r) ∈ [0.633, 0.731], so A.14(iii) holds in every equilibrium on the whole path for every π < 0.633. At
π = 0.7, r = 1.2 (τ = 0.633), no trade is an equilibrium (U_H(1) = −0.015, U_L(−1) = −0.0083), every price coincides,
entry is one, and the mean of preparation reports is 0. At π = 0.7, r = 2 the full-trade equilibrium (a sale deters) has
mean 0.0395 > 0, so once π ≥ τ positivity depends on the equilibrium.

What is lost: (a) π ≥ 1/2 is a restriction on the economy, not a normalization; nothing rescues the naive comparison for
π < 1/2, the case in which a good fit is a priori the less likely class. (b) "Any stronger incumbent" becomes "a stronger
incumbent that does not mainly push values across the reserve", via (S1)–(S3) or the exact kernel inequality.
(c) one named condition, B_F(π) < c_H.

Provenance: the kernel difference formula, (S1), the 90/10 counterexample (its arithmetic now checked) and the benchmark
derivative are from the Solver F notes. The Solver F notes claimed that the naive test and count nonidentification each hold
"iff π = 1/2"; that is right for counts at a known prior and wrong for the naive test, so part (a) is new, as are (S2),
(S3), the mild financial-strategic counterexample, the false-negative example and the sharpness of B_F(π) < c_H.

## Importance of the weakness

Every A8 result is stated at prior 1/2 (A8:3–4, §08:4), so no stated result is false; the weakness is reach. Corollary
A.2 shows that the paper treats other priors as live, and §08:21–22 sells the impact test as needing "no knowledge of the
auction objects", which is true only because the prior is fixed.

Statement by statement at a general prior:

| Statement | Survives at every prior? | Correction |
|---|---|---|
| A.11(i) decomposition | yes | class component ρΔ(M − m), not ρΔ·(informed share) |
| A.11(ii) impact test | with weights | p_1I₊ vs p_{−1}I₋, or E[P] vs E[P \| X = 0]; for π < τ the naive form holds when π ≥ 1/2 and ρ < M/(2π − m), and fails at every π < 1/2 that admits non-recruiting full trade |
| A.11(iii) hidden price | yes | S = ρΔ(M − m) |
| A.11(iv) trends | class part yes; entry part needs (S1)–(S3) at every prior, including 1/2 | — |
| A.11(v) jump at the ceiling | yes | given a single crossing of τ(s) through M(π) |
| A.12(a) count nonidentification | only at π = 1/2 or an unknown prior | at a known π ≠ 1/2 counts identify the slot, and prices identify ρΔ |
| A.12(b) incentive bound | yes | m(π; u′) in place of (1 − ϑ′)/2 |
| A.12(d) price identification | yes | u = s/[(1 − π)(π − s)] |
| Corollary A.3 | yes, known prior | λ = E[X]/π; branch R: E[X] = πs₊ |
| A.14(i)–(ii) | yes | — |
| A.14(iii) | yes under B_F(π) < c_H | replace 1/2 by π in the proof |
| A.14(iv) | yes | b + πλ in place of b + λ/2 |

Size. The naive test's false positive at π < 1/2 is 9.7% of the sale impact at π = 0.45, 20.4% at 0.4 and 45.4% at 0.3
(formula u(1 − 2π)/(1 + uπ), any auction). Against the entry component that recruitment would add at the same point, the
false gap is at most 3.2% on the benchmark path's unique-trade domain (π = 0.21, r = 3.6). The auction-free bound
ρ[(M − π) − (π − m)]/[(1 − ρ)M] at the benchmark slot and ρ = 1/4 approaches 13.3% only as π → 0, where full trade needs
Δ > k/(ρm(π)) → ∞ and w_L → 0. So the naive test is formally invalid off 1/2 but its bias is small next to a real
recruitment signal; a sign test in a large sample would still reject falsely. Frequency weighting removes the bias at no cost in data.

Counts. Nonidentification at a known prior is a knife-edge at 1/2, but the realistic case, a prior unknown to the
econometrician, keeps the message at every prior, so the paper loses little by restating it.

Trend. This part matters more than the prior, because it fails at prior 1/2 under a mild path: a financial-or-strategic
incumbent with reserve-failure probabilities inside the benchmark's own range. The benchmark statement A.11(iv) is
correct, with margin 0.31 in dA_r(M)/dr. Any general claim that the spread rises with incumbent strength while a purchase
recruits needs the entry-premium condition.

Announcements. Essentially unaffected: replace B_r(1/2) < c_H by B_F(π) < c_H.

## Other findings (errors in the manuscript, anything surprising)

1. A8:8 sets ϑ = u/(2 + u) = 2M − 1 = M − m. At a general prior the informed share of nonzero orders is still
λ/v = u/(2 + u), but M − m = ϑ·π(1 − π)(2 + u)²/[1 + u + u²π(1 − π)] < ϑ unless π = 1/2 (0.4019 against 0.4621 at
π = 0.3 or 0.7), and 2M − 1 has no role. So §08:23–24 ("ρΔ times the informed share") and §08:25 ("the sale impact
contains only half of the class component") are prior-1/2 identities: the sale impact carries the share Pr(X = 1)/v of
the class component, 0.408 at π = 0.3 and 0.592 at π = 0.7.
2. A.11(ii) and A.14(iv) are the same identity, T = P̄ − P(0). The proof of A.14(iv) uses m + M = 1; the martingale
argument of Candidate 1 is shorter and prior-free. The proof of A.14(iii) cites B_r(1/2) < c_H and the mean posterior
1/2; replace both by π.
3. Off prior 1/2 a regime appears that the paper never meets: when B_F(m) < c_H ≤ B_F(π), a sale deters entry, the
entry component sits in the sale impact, and a quiet opportunity is good news, P(0) > P̄. In the benchmark at π = 0.7,
full trade is an equilibrium in this regime for r ∈ (1.787, 2.882]: the lower end is ρΔ(r)m(0.7) = k, the upper end
r_π = 2.882 solves τ(r) = 0.7, and T jumps from −0.165 to +0.320 between r = 2.88 and 2.89.
4. A.13(iii) uses E[X] = 0. At prior π, Cov(X, 1_A) = (e₊ − ρ)Pr(X = 1)(1 − E[X]), still zero exactly when no purchase
recruits, and above the ceiling Cov(X, 1_W) = 2ρπ(1 − π)λ(W_H − W_L), because Cov(X, μ(X)) = 2π(1 − π)λ (checked in
`s07`). The W4 study owns A.13.
5. Refinement of SCAN Part 1 (A.11 row): the scan says the impact test "needs prior 1/2". More precisely, in the regime
π < τ the naive comparison survives for every π ≥ 1/2 when ρ < M(π)/(2π − m(π)) (at least 0.911 at the benchmark slot),
fails at every π < 1/2, and the frequency-weighted form of Candidate 1 holds at every prior.
6. The Solver F notes' arithmetic flagged "unverified" checks out: κ(0.3) = 0.1362 and r_S(0.3) = 2.820; λ = 0.336122,
b = 0.195615; M(1/2) = 0.731059; τ(3) = 0.705; the 45% bias at π = 0.3; the 90/10 drop of 0.225 in A(M); the general-π
branch-R formula; the quadratic for the unknown prior. The claim that the naive test holds iff π = 1/2 is wrong
(Candidate 3(a)).
