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
- J rises strictly, with J′ ≥ AΔ²/γ² > 0 where A = (r² − p²)/(2r²).

`O9_proof.tex` gives the statement and a complete proof. The proof is ready for the appendix and needs no computation.

Decision 4 therefore takes its first branch. Proposition 3(c) leads with the balance condition, and the uniform incumbent is its primitive case. In `statements/B.tex` this reads:

- **(c), hypothesis.** Along a path, Δ_T(r)[g_H(r) − c_H] is nondecreasing.
- **(c)(i).** {J ≥ k} is an up-set on which J is nondecreasing, strictly where Δ_T rises strictly. Coexistence is an interval at every prior and every slot.
- **(c)(ii).** On a compact I with Δ_T and τ continuous and τ > π at the weakest incumbent, the interval is closed. It starts at the weakest strength with J ≥ k and ends at the smaller of the last strength with τ ≤ M and the last strength with Δ_T ≤ Δ^N.
- **(c)(iii).** The uniform incumbent above satisfies the hypothesis of (c), and J rises strictly.
- **(c)(iv).** If in addition Δ_T(g_H − c_H)² is nondecreasing, then Δ_T(1 − τ)² is nondecreasing, and the threshold pair's entry is nonincreasing where ρJ ≤ k ≤ J.

The main-text Proposition 3(c) states the balance condition in words, "the product of the spread and g_H − c_H does not fall", and gives the uniform case as one sentence.

## The argument in words

For a uniform incumbent, a high-class value at or above the strongest incumbent always wins and pays the larger of the reserve and the incumbent's value. A low-class value below the weakest incumbent's top earns (θ² − p²)/(2r). The auction terms are therefore explicit:

- g_H = v_H − r/2 − p²/(2r);
- g_L = (E_L θ² − p²)/(2r);
- Δ_T = E_L(r − θ)²/(2r).

Their sum Δ_T + γ is the class mean gap. As r rises:

- the high class's margin X = g_H − c_H falls at the rate A = (r² − p²)/(2r²);
- the spread rises at the rate Δ_T′ = (r² − E_L θ²)/(2r²) ≥ 0.

The spread wins because of two facts.

1. **Affordability gives X ≥ rA.** The margin is at least r times its own rate of decline: X ≥ rA because v_H − c_H ≥ max I ≥ r.
2. **Separation gives rΔ_T′ ≥ Δ_T.** The spread grows at least in proportion to r: rΔ_T′ − Δ_T = E_L[θ(1 − θ/r)] ≥ 0 because every low-class value lies in [0, r].

Together, (Δ_T X)′ = Δ_T′X − AΔ_T ≥ A(rΔ_T′ − Δ_T) ≥ 0. This is the "two-line derivation" of PLAN.md Part 5, and every step holds.

The rise of J needs one more step. Write J = Δ_T X/γ with γ′ = −Δ_T′. Then J′ = [d X Δ_T′ − AΔ_T γ]/γ². The same two facts bound this below by AΔ_T²/γ². That is the referee's equation (8).

## Relation to the referee's report

The referee (`referee/W1.md`, equations (4) to (8)) proved the strict rise of J directly, without passing through the product. Its equation (10) proved that the balance condition gives a nondecreasing J. The proof here adds two links:

- the uniform hypotheses give the balance condition itself (Step 3);
- they give g_H > g_L, so the standing positive profit gap is a consequence and not an extra hypothesis (Step 2).

## How far apart the two conditions are

**1. The balance condition is strictly more general than the uniform case.**

- Take the example's path with c_H = 33/5 in place of c_H = 6. Affordability fails: E_H θ − (r_2 + c_H) = −1/5.
- The balance condition still holds. On this path X = g_H − c_H decreases and Y = −g_H′Δ_T/Δ_T′ increases (referee, equation (11)), so the minimum of X − Y sits at r_2, where it equals 4699/8280 ≈ 0.5675 > 0.
- An exact print-only computation gives this value.

**2. The uniform case does not give the squared form of (c)(iv).**

- Take point-mass classes at h and ℓ = 1, p = 1/2, I = [3/2, 5], and c_H = h − 5, so that affordability holds with equality.
- At r = max I = 5, X = rA. Then (Δ_T X²)′ = XA(rΔ_T′ − 2Δ_T), and for point masses rΔ_T′ − 2Δ_T = (r − ℓ)(3ℓ − r)/(2r) < 0 whenever max I > 3ℓ. Here (Δ_T X²)′ = −9801/10000 at r = 5.
- For h = 100 and c_H = 95, the exact derivative of Δ_T(1 − τ)² at r = 5 is −4302639/46200521200 < 0. So Δ_T(1 − τ)² falls near max I under the uniform hypotheses.
- For h = 10 and c_H = 5 the same derivative is 107811/20261200 > 0. The fall needs a large h.

So (c)(iv) keeps the squared form as its own hypothesis. In the example, Lemma A.10(c) proves the squared form directly, with margin 937/5520.

**3. The positive start margin g_H > c_H plays no role in the interval claim.**

- On {J ≥ k}, J > 0 forces Δ_T X > 0. The referee's comparison (10) therefore runs from any strength in that set, and the up-set and interval claims of (c)(i) need no start margin.
- The margin matters only for the stronger claim "J is nondecreasing on the whole path", which no statement uses.
- The main-text form drops it.

## What it changes in the plan

Nothing beyond fixing decision 4 on its first branch:

- PLAN.md Part 4, S4 item 3 ("the whole set is one interval under the balance condition, its primitive case the uniform, separated and affordable incumbent, subject to proof O9") holds as planned.
- The alternative of two conditions side by side does not arise.
- The referee's weaker point-mass bound (equation (9), c_H ≤ h − r_2 + ℓ/2 − p²/(2r_2), which is 6.865 in the example) is not stated. This follows the theory lens's recommendation not to print it. The balance condition already covers the example with c_H = 6.6, as shown in point 1.
