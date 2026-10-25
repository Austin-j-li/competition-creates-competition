# O9. The uniform incumbent and the balance condition

The mathematics writer, statement freeze S4, area B.

## The question

Does the uniform, separated and affordable incumbent imply the balance condition, that is, Δ_T(r)[g_H(r) − c_H] nondecreasing along the path? The hypotheses are:

- F_r = U[0, r] for r in a compact interval I, with p < min I;
- every low-class value lies in [p, min I];
- every high-class value is at least max I;
- E_H θ ≥ max I + c_H.

## Result

Yes. Under these hypotheses:

- g_H > g_L, since γ ≥ c_H > 0;
- the product Δ_T(g_H − c_H) is nondecreasing;
- J′ ≥ (r² − p²)Δ_T²/(2r²γ²) ≥ 0 on all of I, with strict inequality wherever Δ_T > 0, which includes every r > min I. Hence J rises strictly on I. At r = min I the bound can be zero: if the low class is a point mass at min I, then Δ_T and Δ_T′ vanish there, and so does J′.

`O9_proof.tex` gives the statement and a complete proof. The proof is ready for the appendix and needs no computation.

Decision 4 therefore takes its first branch. Proposition 3(c) leads with the balance condition, and the uniform incumbent is its primitive case. In `statements/B.tex` this reads:

- **(c), hypothesis.** Along a path, Δ_T(r)[g_H(r) − c_H] is nondecreasing.
- **(c)(i).** {J ≥ k} is an up-set on which J is nondecreasing, strictly where Δ_T rises strictly. Coexistence is an interval at every prior and every slot.
- **(c)(ii).** On a compact I with Δ_T and τ continuous and τ > π at the weakest incumbent, the interval is closed. It starts at the weakest strength with J ≥ k and ends at the smaller of the last strength with τ ≤ M and the last strength with Δ_T ≤ Δ_T^N.
- **(c)(iii).** The uniform incumbent above satisfies the hypothesis of (c), and J rises strictly.
- **(c)(iv).** If in addition Δ_T(g_H − c_H)² is nondecreasing, then Δ_T(1 − τ)² is nondecreasing. When an indifferent investor may mix and an indifferent high-cost challenger may prepare with any probability, the threshold pair qualifies exactly where π < τ < M and ρJ ≤ k ≤ J, and its entry is nonincreasing there.

The main-text Proposition 3(c) states the balance condition in words, "the product of the spread and g_H − c_H does not fall", and gives the uniform case as one sentence.

## The argument in words

Write Γ̄ = E_H θ − E_L θ for the class mean gap. For a uniform incumbent, a high-class value at or above the strongest incumbent always wins and pays the larger of the reserve and the incumbent's value. A low-class value below the weakest incumbent's top earns (θ² − p²)/(2r). The auction terms are therefore explicit:

- g_H = E_H θ − r/2 − p²/(2r);
- g_L = (E_L θ² − p²)/(2r);
- Δ_T = E_L(r − θ)²/(2r).

Their sum Δ_T + γ is the class mean gap Γ̄. As r rises:

- the high class's margin g_H − c_H falls at the rate (r² − p²)/(2r²);
- the spread rises at the rate Δ_T′ = (r² − E_L θ²)/(2r²) ≥ 0.

The spread wins because of two facts.

1. **Affordability gives g_H − c_H ≥ r(r² − p²)/(2r²).** The margin is at least r times its own rate of decline, because E_H θ − c_H ≥ max I ≥ r.
2. **Separation gives rΔ_T′ ≥ Δ_T.** The spread grows at least in proportion to r: rΔ_T′ − Δ_T = E_L[θ(1 − θ/r)] ≥ 0 because every low-class value lies in [0, r].

Together, (Δ_T(g_H − c_H))′ = Δ_T′(g_H − c_H) − [(r² − p²)/(2r²)]Δ_T ≥ [(r² − p²)/(2r²)](rΔ_T′ − Δ_T) ≥ 0. This is the "two-line derivation" of PLAN.md Part 5, and every step holds.

The rise of J needs one more step. Write J = Δ_T(g_H − c_H)/γ with γ′ = −Δ_T′. Then J′ = [Γ̄(g_H − c_H)Δ_T′ − ((r² − p²)/(2r²))Δ_Tγ]/γ². The same two facts bound this below by (r² − p²)Δ_T²/(2r²γ²). That is the referee's equation (8).

## Sources and what each step proves

| Step of `O9_proof.tex` | Content | Source |
|---|---|---|
| Step 1 | the auction terms of the uniform incumbent | `referee/W1.md`, equations (4) and (5) |
| Step 2 | the three inequalities | the first two are `referee/W1.md` equations (6) and (7); the third, γ ≥ c_H, gives g_H > g_L from the hypotheses, where W1 assumes γ > 0 |
| Step 3 | the balance condition itself | PLAN.md Part 5, O9 |
| Step 4 | the strict rise of J | `referee/W1.md`, equation (8) |

`referee/W1.md` equation (10) proves that the balance condition gives a nondecreasing J on {J ≥ k}; Proposition 3(c)(i) states it.

## How far apart the two conditions are

**1. The balance condition is strictly more general than the uniform case.**

- Take the example's path with c_H = 33/5 in place of c_H = 6. Affordability fails: E_H θ − (r_2 + c_H) = −1/5.
- The balance condition still holds. On this path (Δ_T(g_H − c_H))′ = Δ_T′[(g_H − c_H) + g_H′Δ_T/Δ_T′]. The margin g_H − c_H decreases and −g_H′Δ_T/Δ_T′ increases (referee, equation (11)), so the minimum of the bracket on [r_0, r_2] sits at r_2, where it equals 4699/8280 ≈ 0.5675 > 0.
- An exact print-only computation gives this value.

**2. The uniform case does not give the squared form of (c)(iv).**

- Take point-mass classes at h and ℓ = 1, p = 1/2, I = [3/2, 5], and c_H = h − 5, so that affordability holds with equality.
- At r = max I = 5, g_H − c_H = r(r² − p²)/(2r²). Then (Δ_T(g_H − c_H)²)′ = (g_H − c_H)[(r² − p²)/(2r²)](rΔ_T′ − 2Δ_T), and for point masses rΔ_T′ − 2Δ_T = (r − ℓ)(3ℓ − r)/(2r) < 0 whenever max I > 3ℓ. Here (Δ_T(g_H − c_H)²)′ = −9801/10000 at r = 5.
- For h = 100 and c_H = 95, the exact derivative of Δ_T(1 − τ)² at r = 5 is −4302639/46200521200 < 0. So Δ_T(1 − τ)² falls near max I under the uniform hypotheses.
- For h = 10 and c_H = 5 the same derivative is 107811/20261200 > 0. The fall needs a large h.

So (c)(iv) keeps the squared form as its own hypothesis. In the example, Lemma A.10(c) proves the squared form directly, with margin 937/5520.

**3. The positive start margin g_H > c_H plays no role in the interval claim.**

- On {J ≥ k}, J > 0 forces Δ_T(g_H − c_H) > 0. The referee's comparison (10) therefore runs from any strength in that set, and the up-set and interval claims of (c)(i) need no start margin.
- The margin matters only for the stronger claim "J is nondecreasing on the whole path", which no statement uses.
- The main-text form has no start margin.

## Scope against the plan

- PLAN.md Part 4, S4 item 3 ("the whole set is one interval under the balance condition, its primitive case the uniform, separated and affordable incumbent, subject to proof O9") holds as planned, on decision 4's first branch.
- The referee's weaker point-mass bound (equation (9), c_H ≤ h − r_2 + ℓ/2 − p²/(2r_2), which is 6.865 in the example) is not stated, following the theory lens's recommendation. The balance condition covers the example with c_H = 33/5, as point 1 shows.
