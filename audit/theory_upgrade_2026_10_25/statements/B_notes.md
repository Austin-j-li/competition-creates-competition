# Area B statements: notes

The mathematics writer, statement freeze S4: Appendix A.4 (coexistence), Proposition 3 and Corollary 2.

## Files

- `statements/B.tex` holds the statements of area B, with the general results first and then the example. It starts with `\input{../tex/preamble}` and compiles.
- `statements/O5/` holds Proposition 3(d), existence at the prior 1/2: `O5_proof.tex` (statement and proof) and `O5_notes.md`.
- `statements/O9/` holds Proposition 3(c)(iii), the uniform incumbent: `O9_proof.tex` and `O9_notes.md`.

Line references `A4:n` are to `slot/manuscript/appendix/A4_coexistence.tex`. Line references `04:n` are to `slot/manuscript/sections/04_equilibrium_results.tex`.

The `\extlabel` block at the top of `B.tex` prints the numbers of labels defined outside the file:

| Label | Number |
|---|---|
| `def:equilibrium` | A.1 |
| `lem:prices` | A.2 |
| `lem:trading` | A.3 |
| `app:coexistence` | A.4 |
| `lem:twonumbers` | A.5 |

The block is a reading aid and is not part of the transplant. The same holds for the `\setcounter` and `\renewcommand` lines that set the lemma and corollary numbers.

## Numbering in the finished paper (decision 7, PLAN.md Part 6)

**What the numbering assumes.**

- Area A adds Lemma A.4 (`lem:reduction`) and Lemma A.5 (`lem:twonumbers`) after the trading lemma, and Lemma A.6 (`lem:decisive`) in A.3. This follows `plan/lens_theory.md` section 4.
- The five A.4 lemmas are then A.7 to A.11, in the order of `B.tex`.
- If area A adds a different number of lemmas, the five A.4 lemmas shift by the difference. Nothing else in `B.tex` depends on it.

**Table and equation numbers.**

- No table enters or leaves A.4. Tables A.1 to A.3 keep their numbers.
- The two displays of the full statement of Proposition 3, `eq:region` and `eq:entry-inf`, take appendix equation numbers (A.n). Every later appendix equation number moves up by two.
- The proof of part (d) (`O5/O5_proof.tex`) numbers two more displays, `eq:o5-sale` and `eq:o5-buy`. Later appendix equations move up by two more. The proof of part (c)(iii) numbers none.

**Main-text corollaries.**

- Corollary 2 belongs to the main-text corollary counter (PLAN.md Part 6) and follows Proposition 3.
- Its full statement is named and unnumbered, so Corollaries A.1 to A.3 keep their numbers.

**Labels.** The two named full statements carry no label of their own, as in the manuscript. They are cited as `Proposition~\ref{prop:coexistence} (full statement)` and `Corollary~\ref{cor:example-coexistence} (full statement)`, through the labels of the main-text results. Their displays carry `eq:region` and `eq:entry-inf`.

**The A.4 results, numbered.**

| Result | Label | Number in the manuscript | Number in the statements |
|---|---|---|---|
| The high class | `lem:a4-high` | A.6 | A.7 |
| The low class | `lem:a4-low` | A.7 | A.8 |
| Product structure | `lem:a4-product` | A.8 | A.9 |
| Proposition 3 (full statement) | named; `prop:coexistence` stays on the main-text proposition | named | named |
| The example path | `lem:a4-path` | A.4 | A.10 |
| The order of the marked strengths | `lem:a4-order` | A.5 | A.11 |
| Corollary 2 (full statement) | named; label of the main-text corollary | named, as the example's "Proposition 3 (full statement)" | named |
| Coexistence at every prior | `prop:priors` | Corollary A.2 | Corollary A.2 |
| Main-text Proposition 3 | `prop:coexistence` | 3 | 3 |
| Main-text Corollary 2 | `cor:example-coexistence` (proposed) | none | 2 |

## The statements, in the order of B.tex

### 1. Setting (A.4, general part)

- **Source.**
  - A4:132–157, restated at a fixed continuous law F.
  - `scan/reduction_A3_A5.md` section 1, rows "High-class lemma" and "Low-class lemma": s* needs τ < 1, and the case τ ≥ 1 needs its own sentence.
  - `plan/NOTATION.md` (c), "Paths".
- **Scope.**
  - The class ranking; π ∈ (0, 1); 0 < λ < 1 and 0 < β < 1/2; ρ ∈ (0, 1), c_H > 0, k > 0.
  - A continuous F with Δ_T > 0 and g_H > g_L.
  - The paragraph defines Δ_T^F = k/(1 − M), Δ_T^N = k/(ρ max{π, 1 − π}), the posteriors, a path, an up-set and a down-set.
  - The threshold-reaching rate s* = b(τ − π)/[π(1 − τ)] is defined for π < τ < 1, where it is positive and μ_+(s*) = τ, with μ_+ extended to every s ≥ 0. It is feasible, s* ≤ λ, exactly when τ ≤ M, and s* < λ exactly when τ < M. For τ < π the expression is negative, and for M < τ < 1 it exceeds λ; neither is an investor rate. The case τ ≥ M, including τ ≥ 1, has its own sentence.
  - The path facts cite Lemma A.5.
- **Takes the place of.**
  - A4:1–8, the opening, which fixes the example as the setting of all of A.4.
  - A4:132–157, the two investor problems.
  - The sentence "On the path τ(r) < 3/4" (A4:149) has no counterpart: the general part defines s* for π < τ < 1 and states the case τ ≥ M.
- **Number.** Unnumbered paragraph.

### 2. Lemma A.7, the high class (`lem:a4-high`)

- **Source.** A4:159–191; reduction section 1.
- **Scope.**
  - Any F as in item 1 with π < τ, including τ ≥ 1.
  - Each pair carries in words the tie rule it needs: (Q), (R) and (T) need an indifferent investor who may mix.
  - (T) under each challenger rule: e* = 1, or ρ ≤ e* ≤ 1.
  - (F) has a weak return condition under the mixing investor and a strict one under the abstaining investor.
- **Manuscript against statement.**

| Manuscript (A4:159–173) | Statement |
|---|---|
| "Fix r and π with π < τ(r)" | "Let π < τ" |
| (Q): 0 < s_+ < min{s*, λ} | (Q): 0 < s_+ < λ with μ_+(s_+) < τ, which covers τ ≥ 1 |
| no sentence on τ ≥ M | last sentence: the case τ ≥ M |

- **Takes the place of.** A4:159–173. The proof, A4:174–191, carries over at a fixed F.
- **Number.** Lemma A.7 (manuscript A.6).

### 3. Lemma A.8, the low class (`lem:a4-low`)

- **Source.** A4:193–222; reduction section 1. No bound τ < 1 is needed.
- **Scope.** Any F with π < τ. It covers both investor rules, including the gap ρΔ_T m ≤ k < ρΔ_T π under the abstaining rule.
- **Takes the place of.** A4:193–209. The proof, A4:210–222, carries over.
- **Number.** Lemma A.8 (A.7).

### 4. Lemma A.9, product structure (`lem:a4-product`)

- **Source.** A4:224–256.
- **Scope.**
  - π < τ and s_+ ≥ s_-, under each pair of tie rules.
  - With s_+ ≥ s_-, two orders share a posterior only if one of them is 0 or −1. Both then have entry ρ, so the qualification of equal posteriors under the alternative challenger rule does not bite here (reduction section 4.1).
- **Takes the place of.** A4:224–233. The proof, A4:235–256, carries over.
- **Number.** Lemma A.9 (A.8).

### 5. Proposition 3 (full statement), named

**Source.**

- `referee/W1.md`:
  - equations (1) and (2), with the proof before them (uniqueness under the default challenger rule, convexity, τ ≤ 1 − ρ max{π, 1 − π}, π < 1/(1 + ρ));
  - equation (3) and the wording points after it (part (b));
  - equation (10), the balance condition, undivided as NOTATION (d) asks;
  - equations (4)–(8), the uniform case;
  - equation (12) and the paragraph after it on the threshold pair (part (c)(iv)).
- `scan/reduction_A3_A5.md` sections 3(b) to 3(d).
- `WORKAROUNDS.md` W1, "Manuscript points", last item.
- Proofs: O9 for (c)(iii) and O5 for (d). Parts (a), (b), (c)(i), (c)(ii) and (c)(iv) follow the referee's proofs, which S5 writes out.

**Scope and form.**

- (a) to (c), except the second sentence of (c)(iv), take the default tie rules: an indifferent investor may mix, and an indifferent high-cost challenger prepares.
- They hold at every prior and every slot.
- (a) holds at a fixed F. (b) and (c) hold along a path.
- (c)(ii) adds a compact I, continuity of Δ_T and τ, and τ > π at the weakest incumbent.
- (c)(iii) is the uniform case.
- (c)(iv), first sentence: if Δ_T(g_H − c_H)² is nondecreasing, then Δ_T(1 − τ)² is nondecreasing. This needs only the path hypotheses.
- (c)(iv), second sentence: when an indifferent investor may mix and an indifferent high-cost challenger may prepare with any probability, the threshold pair is a pair of Lemma A.7 exactly where π < τ < M and ρJ ≤ k ≤ J, and its entry Ent_T is nonincreasing on those strengths. Under the default challenger rule the threshold pair needs J = k, a single strength on a path where J rises strictly, so the comparison is a statement about the alternative rule.
- (c)(iv), third sentence: at τ = M the threshold rate is λ, and a purchase at it is the full purchase (F).
- (d) holds at π = 1/2 with τ > 1/2, including τ ≥ 1, under the mixing investor and either challenger rule.

**Weak against strict.**

- **(a)** Entry rises strictly for Δ_T < Δ_T^F and is constant for Δ_T ≥ Δ_T^F.
- **(c)(i)** J is nondecreasing on {J ≥ k}, and strictly increasing wherever Δ_T rises strictly.
- **(c)(iii)** The product is nondecreasing and J is strictly increasing.
- **(c)(iv)** Both monotonicities are weak.

**How the content follows.**

- *The informative market in (a).*
  - Its rate s_+ = min{λ, (b/π)[(1 − π)Δ_T/k − 1]} equals s* at J = k, so the threshold pair with entry one is the case J = k, Δ_T < Δ_T^F.
  - At τ = M the region forces Δ_T ≥ Δ_T^F, so that case is a full purchase.
  - Entry = ρ + (1 − ρ)(b + πs_+), which gives `eq:entry-inf`.
- *Part (b).* It uses the referee's wording: the gap lies at spreads below Δ_T^F, and no informative equilibrium exists in the gap.
- *Part (c)(i).* If J(r) ≥ k, then Δ_T(g_H − c_H) > 0. The referee's comparison (10) then runs from r with no start margin.
- *Part (c)(ii).* With τ > π at the weakest incumbent, the up-set {π < τ} is all of I. The remaining three sets are closed under continuity, so the interval is closed, and its endpoints are the stated extreme strengths.
- *Part (c)(iv).*
  - 1 − τ = (g_H − c_H)/γ, so Δ_T(1 − τ)² = Δ_T(g_H − c_H)²/γ². Along a path γ is positive and nonincreasing, so 1/γ² is nondecreasing, and the product of two nonnegative nondecreasing functions is nondecreasing.
  - Lemma A.7(T) under the two named rules needs 0 < s* < λ, that is π < τ < M, and ρ ≤ k/J ≤ 1, that is ρJ ≤ k ≤ J.
  - With entry ρ after a sale and after the zero order, total entry is ρ + (k/J − ρ)(b + πs*), and b + πs* = (1 − π)b/(1 − τ). This gives the displayed Ent_T.
  - On these strengths J ≥ k, so by (c)(i) the numerator k − ρJ is nonnegative and nonincreasing, and the denominator Δ_T(1 − τ)² is positive and nondecreasing. Hence Ent_T is nonincreasing.
  - At τ = M, s* = λ and b + πλ = (1 − π)b/(1 − M), so the formula is the entry of a full purchase with e(1) = k/J.
- *Part (d).* See `O5/O5_notes.md`.

**Takes the place of.** The named "Proposition 3 (full statement)" at A4:287–314. That block is the example's equilibrium set, and its content is item 13.

**Number.**

- Named and unnumbered.
- The label `prop:coexistence` stays on the main-text Proposition 3, so `Proposition~\ref{prop:coexistence} (full statement)` prints "Proposition 3 (full statement)".
- `eq:region` and `eq:entry-inf` take (A.n) numbers.

### 6. Proposition 3 in the main text

- **Source.** Item 5, parts (a) to (c); `plan/lens_maintext.md` target T-P3; decision 4, first branch, since O9 holds.
- **Against T-P3.**

| Point | T-P3 | Statement |
|---|---|---|
| Tie rules | not named | named, because uniqueness needs the preparing challenger and the strict rise needs the mixing investor |
| Part (b) | no gap sentence | the gap sentence, from the referee's wording points |
| Part (c), start margin | "class H's gross profit exceeds c_H at the weakest incumbent of the path" | not a hypothesis: the interval claim holds without it (`O9/O9_notes.md`, point 3) |
| Part (c), uniform case | stated with r_0 and r_2 | stated for "r in a closed interval" |
| Fixed primitives | implicit | ρ, c_H, k and the slot fixed; the laws continuous |

- **Takes the place of.** 04:272–283. The title at 04:272 names the example by the word rule (4) excludes.
- **Number.** Proposition 3, label `prop:coexistence`, title "Quiet and informative markets" (lens_maintext).

### 7. Paragraph "Two intervals of coexistence"

**Source.** `referee/W1.md` equation (20) and the section that proves it, including the affordability margin 10 − 1.81 − 6 = 2.19; `WORKAROUNDS.md` W1, "What remains weak".

**Scope.**

- The example's h, ℓ, p, ρ, c_H and k; the prior 1/2; the strength r ∈ [0, 2]. NOTATION (c), "Paths", names a path index r; W1 equation (20) writes it t.
- The slots: those with 141/200 < M(1/2) < 4245/5804, the example's thresholds at r_1 and r_2. The paragraph prints them through `tau_r1_frac` and `tau_r2_frac`, because τ(r_1) and τ(r_2) would read as values on this path.
- The claims hold at every such slot. Along the path, τ ∈ [0.630661, 0.670628], which lies below 141/200 < M. Also Δ_T ≤ 2/25 < Δ_T^N = 4/25. The condition J ≥ k does not involve the slot.
- At every such slot, Δ_T^F = k/(1 − M) ∈ (0.0678, 0.0745). This lies above the smaller root 0.060452 of the second piece and below 2/25, so the sure-purchase strengths form one nonempty interval inside [r_hi, 2]. At the example's slot it is [1.755028, 2], as the referee found.

**Formulas.** The lower law lies in (p, ℓ) and the upper law in (ℓ, h). Hence:

- Δ_T = (upper centre − 1)/10 and g_L = (9/10)(1 − lower centre);
- γ = 9 − Δ_T and τ = (6 − g_L)/(9 − Δ_T);
- J = Δ_T(3 + g_L − Δ_T)/(9 − Δ_T).

**Takes the place of.** Nothing. It is a paragraph after the proof of the full statement of Proposition 3 (PLAN.md Part 4, S4 item 3: "The two-interval economy is a stated fact").

**Number.** Unnumbered paragraph.

**Note.** The range [0, 2] of r, with its break at 1, is the path's own parameter, typed as in the referee's equation (20). Every other number of the paragraph prints through a key.

### 8. Paragraph "Other tie rules" (general F)

**Source.**

- A4:533–543, and the general-prior sentences at A4:555–571, restated at a general F.
- `plan/lens_theory.md`, A4 change list at 533–598 ("add the general statements").
- The proof of W1 equations (1) and (2).
- Reduction section 4.1.

**Content, derived from Lemmas A.7 to A.9 and the proof of part (a).**

- *An indifferent high-cost challenger may prepare with any probability, and the investor may mix.*
  - **The region.** It adds {τ = π, k/(1 − π) < Δ_T ≤ Δ_T^N}. At τ = π, one quiet market has entry ρ after every order, and one informative market is constructed as in part (a), with entry ρ after a sale. Neither is the only one: a quiet market with constant entry e after every order is consistent with abstention whenever ρ ≤ e ≤ min{1, k/[Δ_T max{π, 1 − π}]}, and the informative construction admits entry above ρ after a sale whose posterior is the prior, as long as that sale does not pay. τ < π gives no coexistence under either rule.
  - **The extra threshold pair.** Inside the region, wherever τ < M and J > k, the threshold pair with e(1) = k/J is a further equilibrium. Here Δ_T ≤ Δ_T^N gives ρJ < ρΔ_T(1 − π) ≤ k, so k/J > ρ.
  - **Its entry.** The threshold pair's entry is ρ + (1 − π)b(k − ρJ)/(Δ_T(1 − τ)²). It is strictly below `eq:entry-inf`, since k/J < 1 and s* < s_+.
  - **At τ = M.** A full purchase holds with e(1) ∈ [k/J, 1].
- *An indifferent investor abstains, and the challenger prepares.* Coexistence holds exactly when π < τ ≤ M and Δ_T^F < Δ_T ≤ Δ_T^N, with the full purchase as the informative market. When the challenger may prepare with any probability, add {τ = π, Δ_T^F < Δ_T ≤ Δ_T^N}.

**Takes the place of.** A4:533–543, the opening of the tie paragraph, and the general-prior sentences at A4:555–571. Their example content is item 17. Table A.3 (A4:573–593) stays. The prose writer puts the four plain phrases in place of the abbreviations in its header.

**Number.** Unnumbered paragraph.

### 9. Paragraph "The path and its marked strengths" (example)

- **Source.** A4:4–18 and A4:65–83. fr(d) is written fr(y), following NOTATION (c), and r_* joins the list of marked strengths.
- **Scope.**
  - r_A, r_N, r_J and r_* do not depend on the slot and are defined at every slot. Each of r_A, r_J and r_* is a root in (r_0, r_2), unique by Lemma A.10.
  - r_F, r_S and r_C are defined for a slot with 0 < λ < 1, 0 < β < 1/2 and τ(r_1) < M(1/2) < τ(r_2). The condition places the root r_C of τ(r) = M in (r_1, r_2), and τ rises strictly (Lemma A.10(a)).
  - Outside this band the root can be missing: at λ = 1/100 and β = 1/5, M(1/2) = 104/203 < τ(r_0) = 195/308.
- **Takes the place of.** A4:4–18 and A4:65–83. The definitions are the manuscript's, which A4:4–8 states for the slots of the band.
- **Displays.** The closed form of J (A4:12–16) and the closed form of r_C (A4:77–79) are not statements. They stay as displays in this paragraph.
- **Number.** Unnumbered paragraph.

### 10. Lemma A.10, the example path (`lem:a4-path`)

**Source.** A4:20–29; `referee/W1.md` equations (4)–(8) with the margin 10 − 3.6 − 6 = 0.4, equation (11) and equation (12).

**Manuscript against statement.**

| Part | Manuscript (A4:20–29) | Statement |
|---|---|---|
| (a) | τ(r_2) < 3/4 | 1 − ρ − τ(r_2) = 27/1451 > 0, through the key `margin_tau_r2_3q_B_frac`, whose value is 3/4 − τ(r_2) |
| (b) | J strictly increasing, by a root count | J strictly increasing, from Proposition 3(c)(iii) with h − r_2 − c_H = 2/5, and from the derivative bound (Δ_T(g_H − c_H))′ ≥ (9667/8280)Δ_T′ |
| (c) | on [r_0, 2] | on the whole path [r_0, r_2], with the bound (Δ_T(g_H − c_H)²)′ ≥ (937/5520)(g_H − c_H)Δ_T′ |
| (d) | as stated | as stated |

**Proof for S5, by hand, with no root count.**

- *(a)* As in the manuscript.
- *(b)* Proposition 3(c)(iii) applies: ℓ = 1 ∈ [p, r_0] and r_2 + c_H ≤ h. Directly, (Δ_T(g_H − c_H))′ = Δ_T′[(g_H − c_H) + g_H′Δ_T/Δ_T′]. Here g_H − c_H = 4 − r/2 − 1/(8r) falls for r > 1/2, and −g_H′Δ_T/Δ_T′ = (r − 1)(r² − 1/4)/(2r(r + 1)) rises for r > 1 (W1 after equation (11)). So the bracket is at least its value at r_2, which is 9667/8280. Division by the falling γ gives the strict rise of J.
- *(c)* (Δ_T(g_H − c_H)²)′ = (g_H − c_H)Δ_T′[(g_H − c_H) + 2g_H′Δ_T/Δ_T′] ≥ (937/5520)(g_H − c_H)Δ_T′, and division by the falling γ² gives the result.
- *(d)* As in the manuscript.
- The root-count record (A4:41–62) and the sentence that rests on it have no counterpart in this proof.

**Takes the place of.** A4:20–29. The proof, A4:31–63, is rewritten in S5.

**Number.** Lemma A.10 (A.4). Title "The example path"; the manuscript says "The path". In the general part "path" means any FOSD family, and lens_theory's proposed title uses the word that rule (4) excludes.

### 11. Lemma A.11, the order of the marked strengths (`lem:a4-order`)

- **Source.** A4:85–105.
- **Statement.** The manuscript's, with the band written out.
- **For the S5 proof.** The proof types 3/4 (A4:96, A4:102), 1/50 and 22/25 (A4:101) by hand.
  - With Lemma A.10(a), the step r_F < r_N reads M < τ(r_2) < 1 − ρ < 1 − ρ/2.
  - The step r_S < r_1 follows from 1 − M > 1 − τ(r_2) > ρ and ρ²Δ_T(r_1) = 1/24 > k. The margin ρ²Δ_T(r_1) − k = 13/600 needs its own key only if it prints.
- **Takes the place of.** A4:85–87.
- **Number.** Lemma A.11 (A.5).

### 12. Paragraph "The forms at the prior 1/2"

- **Source.** A4:258–272, with the form names of NOTATION (b).
- **Scope.**
  - The prior 1/2 and a slot with τ(r_1) < M(1/2) < τ(r_2), so that r_S, r_C and the low-class rate ŝ_-(r) on [r_S, r_2] are defined.
  - The low-class rate and the five forms take the default tie rules.
  - F at r_C has e(1) = 1 because an indifferent high-cost challenger prepares. T has e*(r) = k/J(r), which is one only at r_A.
  - The alternative rules, named in the paragraph: when an indifferent high-cost challenger may prepare with any probability, F at r_C admits every e(1) ∈ [ρ, 1], and T qualifies exactly on [r_A, r_J]. R, Q and T need an indifferent investor who may mix.
  - At r_C, every e(1) ∈ [ρ, 1] meets the return condition of (F), because r_C > r_S gives ρΔ_T(r_C)(1 − M) ≥ k. T on [r_A, r_J] has 0 < s* < λ, because r_J < r_C (Lemma A.11).
- **Takes the place of.** A4:258–272. The tuple list at A4:273–285 stays.
- **Number.** Unnumbered paragraph.

### 13. Corollary 2 (full statement), named

**Source.** A4:287–314 and the proof at A4:316–397; PLAN.md S5 item 3 and S9.

**Scope.** The example at the prior 1/2, any slot of the band, and the default tie rules.

**Content.** The set table, the entries and parts (a) to (c) are those of the manuscript. Part (b) states entry along the informative branch on [r_A, r_C] in one formula, which is the same content as the manuscript's two sentences.

**Proof for S5.**

| Manuscript step (A4:316–397) | Proof of the full statement |
|---|---|
| Steps 1 to 6 | Proposition 3(a) at each strength, where J(r) ≥ k exactly when r ≥ r_A by Lemma A.10(b), together with Lemmas A.7 to A.9 for the strengths without coexistence |
| Step 7 | its threshold-pair part is item 17, which uses Lemma A.10(b) and (c) on the whole path; the sentence through r_J < 2 (A4:389–391) and its key have no counterpart |
| Step 8 | Proposition 3(d) at each strength, since τ ≥ τ(r_0) > 1/2 |

**Takes the place of.** A4:287–314.

**Number.** Named and unnumbered, "Corollary 2 (full statement)". It cites the label of the main-text corollary.

### 14. Corollary 2 in the main text

- **Source.** Item 13; PLAN.md S9 ("Corollary 2: in the example, coexistence on [r_A, r_N], and entry that rises, flattens and returns to the floor above r_C"); decision 6.
- **Scope.** The example at the prior 1/2, the band, and the default tie rules, all named.
- **Takes the place of.** The example content of 04:272–283. Proposition 3 keeps that place and number.
- **Number.** Corollary 2 on the main-text counter, after Proposition 3. Proposed label `cor:example-coexistence`, title "Coexistence in the example".

### 15. Paragraph "Coexistence at other priors"

- **Source.** A4:431–438, with π_A^lo written in closed form as in the proof (A4:467–468).
- **Scope.** Every slot. r_N(π), r_C(π), r_π, τ_A, π_A^lo, π_A^hi and π_max are defined without the band; r_C(π) and r_π only when the stated strengths exist.
- **Takes the place of.** A4:434–438 and the repeated definitions at A4:460–470.
- **Number.** Unnumbered paragraph.

### 16. Corollary A.2, coexistence at every prior (`prop:priors`)

**Source.** A4:440–457; reduction section 3(e).

**Content against the manuscript.**

- The set 𝒞(π) is identified as the set of Proposition 3(a) on the path.
- The tie rules are named.
- The four cases and the entry sentence are the manuscript's.
- The scope is every slot with 0 < λ < 1 and 0 < β < 1/2.

**Proof for S5.**

| Manuscript step | Proof of the statement |
|---|---|
| Steps 1 and 2 (A4:477–500) | one citation of Proposition 3(a), with J(r) ≥ k exactly when r ≥ r_A |
| Step 3 (A4:501–528) | its four cases; "τ_A < 3/4 = 1 − ρ" (A4:505–506) reads τ_A < τ(r_2) < 1 − ρ, from Lemma A.10(a) |
| the program reference at A4:529–530 | no counterpart |

- The window of case (c) is nonempty because ρτ_A < 1 − τ_A, that is r_A < r_*. In the example 1 − (1 + ρ)τ_A ≈ 0.199076. The existing key `margin_pimax_tauA_B` (π_max − τ_A) records the same fact.

**Takes the place of.** A4:440–457. The proof at A4:459–531 is shortened in S5.

**Number.** Corollary A.2, as in the manuscript.

### 17. Paragraph "Other tie rules in the example"

**Source.**

- A4:544–571.
- `referee/W1.md`: the paragraph on the threshold pair after equation (12), on the strict fall of its entry, and the paragraph after the referee's table of example values, on the threshold pair at r_A under the default rules.
- Reduction section 4.2.

**Content and scope.**

- *The prior 1/2.* The first paragraph takes a slot with τ(r_1) < M(1/2) < τ(r_2).
  - The threshold pair holds at r_A under the default rules. When an indifferent investor may mix and the challenger may prepare with any probability, it holds on (r_A, r_J], with entry falling strictly from Ent_R(r_A) to ρ. The strict fall uses Lemma A.10(b) and (c) on the whole path and Proposition 3(c)(iv), whose strength set π < τ < M, ρJ ≤ k ≤ J is [r_A, r_J] here, because r_J < r_C.
  - At r_C, a full purchase admits every entry after a purchase in [ρ, 1] under that rule.
  - When an indifferent investor abstains, the equilibrium set is as stated, under either challenger rule: the threshold pair, R and Q need the mixing investor, and the only posterior at τ is M at r_C, where the full purchase holds under both challenger rules.
- *A general prior.* The second paragraph takes every slot.
  - The set 𝒞̃(π) and the point r_π = r_* at π_max hold at every slot: at r_π, J > k exactly when π > τ_A, and ρΔ_T π ≤ k exactly when r_π ≤ r_*, that is π ≤ π_max.
  - The four evaluations at π_max (M(π_max), the posterior after the zero order, the full purchase's net return, entry) are at the example's slot, λ = `lambda_B`, β = `beta_B`. At that slot the purchase rate is λ, so the informative market there is a full purchase.
  - At the slot λ = 2/5, β = 1/5 the endpoint has M(π_max) ≈ 0.889499, a mixed purchase at the rate ≈ 0.212895 < λ, full-purchase net return ≈ −0.006401 and entry ≈ 0.443796. A full purchase is not an equilibrium there.
  - The sets when an indifferent investor abstains hold at every slot. The condition r_π ≤ r_N(π) is written out. The manuscript (A4:570–571) states only Δ_T(r_π)[1 − M(π)] > k, which leaves the quiet-market condition implicit.
- *The three threshold-pair entries at 1.55, 1.60 and 1.65 (A4:546–548).* They are not repeated here. They print in the paragraph at A4:399–404, which the prose writer keeps.

**Takes the place of.** A4:544–571, with the manuscript's subscripted set written 𝒞̃ (NOTATION (c)). Table A.3 (A4:573–593) and the closing lines (A4:595–598) stay.

**Number.** Unnumbered paragraph.

### 18. Figure 2 note, the sentence on the threshold pair

- **Source.** `plan/lens_theory.md` target T5; `referee/W1.md`, the paragraph after the referee's table of example values; `WORKAROUNDS.md` W1, "Manuscript points", first item; NOTATION (b).
- **Takes the place of.** 04:302–303, "The thin dashed line is the threshold branch, an equilibrium only when an indifferent high-cost challenger may prepare with any probability."
- **Also on line 302.** "the threshold branch by T" takes NOTATION (b)'s name "the threshold pair". That edit belongs to the prose writer.

## Keys

### Keys to add to the numbers files

None of these is in `slot/manuscript/numbers.tex`. Each prints as ??key in the build of `B.tex`.

| Key | Exact value | Display | Definition and computation | Printed in |
|---|---|---|---|---|
| `margin_unif_afford_B` | 2/5 | 0.4 | h − r_2 − c_H = 10 − 18/5 − 6 (lens_delivery 3.1 row) | Lemma A.10(b) |
| `margin_balance_B_frac` | 9667/8280 | exact only | Minimum over [r_0, r_2] of (g_H − c_H) + g_H′Δ_T/Δ_T′, with g_H − c_H = 4 − r/2 − 1/(8r) and −g_H′Δ_T/Δ_T′ = (r − 1)(r² − 1/4)/(2r(r + 1)). The first falls for r > 1/2 and the second rises for r > 1, so the minimum is at r_2 = 18/5: g_H − c_H = 1559/720, −g_H′Δ_T/Δ_T′ = 16523/16560, difference 19334/16560 = 9667/8280. | Lemma A.10(b) |
| `margin_balance_B` | 9667/8280 | 1.167512 | display of the same value (lens_delivery 3.1) | A9 table, if listed |
| `margin_balance_sq_B_frac` | 937/5520 | exact only | Minimum of (g_H − c_H) + 2g_H′Δ_T/Δ_T′, also at r_2: 1559/720 − 2 · 16523/16560 = 2811/16560 = 937/5520 | Lemma A.10(c) |
| `margin_balance_sq_B` | 937/5520 | 0.169746 | display of the same value | A9 table, if listed |
| `twopath_weight_lower` | 9/10 | 0.9 | weight of the lower uniform law | item 7 |
| `twopath_halfwidth` | 1/100 | 0.01 | half-width of both uniform laws | item 7 |
| `twopath_lower_start` | 3/5 | 0.6 | centre of the lower law at r = 0 | item 7 |
| `twopath_lower_end` | 49/50 | 0.98 | centre of the lower law on [1, 2] | item 7 |
| `twopath_upper_start` | 157/100 | 1.57 | centre of the upper law on [0, 1] | item 7 |
| `twopath_upper_end` | 9/5 | 1.8 | centre of the upper law at r = 2 | item 7 |
| `twopath_lo` | 3137/6498 | 0.482764 | End of the first piece. On [0, 1], Δ_T = 57/1000 is fixed and J ≥ k exactly when g_L ≥ 3703/19000, that is lower centre ≤ 13397/17100, that is r ≤ 3137/6498. | item 7 |
| `twopath_hi` | (1485 − √2127361)/23 | 1.150106 | Start of the second piece. On [1, 2], Δ_T = 57/1000 + (23/1000)(r − 1) and g_L = 9/500, and J ≥ k exactly when Δ_T² − (1519/500)Δ_T + 9/50 ≤ 0. The smaller root is (1519 − √2127361)/1000 ≈ 0.060452; the larger root lies above 2/25. So the piece starts at r = 1 + (1000 · root − 57)/23 = (1485 − √2127361)/23. | item 7 |

The displays `twopath_lo` and `twopath_hi` are the six-decimal values that print. If the numbers files keep exact companions, they are `twopath_lo_frac` = 3137/6498 and, for `twopath_hi`, the closed form above.

An exact print-only computation, kept outside the repository, reproduces every value in this table and the referee's table for the two-interval path. At r = 0, 1, 2 it gives J = 0.021052331, 0.018872526, 0.026349776 and τ = 0.630660852, 0.668903053, 0.670627803. At the example's slot the sure-purchase strengths of this path start at r = 1.755028.

### Keys reused

These keys already exist in `slot/manuscript/numbers.tex`:

| Key | Value |
|---|---|
| `prim_h`, `prim_ell`, `prim_p`, `prim_rho`, `prim_cH`, `prim_k`, `prim_r0`, `prim_r1`, `prim_r2` | the example's primitives |
| `tau_r0_frac` | 195/308 |
| `tau_r1_frac` | 141/200 |
| `tau_r2_frac` | 4245/5804 |
| `margin_tau_r2_3q_B_frac` | 27/1451, which is 3/4 − τ(r_2) = 1 − ρ − τ(r_2) at ρ = 1/4 |
| `J_r0` | 113/18480 |
| `rhoJ_r2` | 263471/4178880 |
| `rstar` | 1.634218 |
| `lambda_B` | 0.336122 |
| `beta_B` | 0.294655 |
| `M_pimax_B` | 0.834698 |
| `mu0_pimax_B` | 0.454140 |
| `margin_cmend_B` | 0.000343 |
| `entry_cmend_B` | 0.560586 |

### Keys the A.4 statements do not use

The rows can stay in the numbers files.

- `QJ_r0` (A4:48), the root-count record of the manuscript's Lemma A.4(b). It also appears at A9:123.
- `margin_rhoJ_2_B_frac` (A4:390), the step through r_J < 2.

`margin_tau_r2_3q_B_frac` is in use, through Lemma A.10(a).

### A key for the prose

`cH_unif_cap_B` = 32/5, which is h − r_2, the cost ceiling of the uniform condition. It serves the main-text sentence on the cost window. lens_delivery 3.1 uses this name; lens_maintext calls it `cH_afford_ceiling_B`. `B.tex` does not use it.

## Scope points

1. **τ > π at the start of the path.** It is a hypothesis of Proposition 3(c)(ii) only.
   - {π < τ} = {B(π) < c_H} is an up-set, so the coexistence set is an interval with or without the condition. See W1, the wording points after equation (3), "On and above a coexistence point, τ > π > 0", and reduction section 3(c).
   - The condition fixes the closed form of the interval. Without it, coexistence can start at an open end where τ crosses π (WORKAROUNDS W1, "Manuscript points", last item).
   - Parts (b) and (c)(i) hold without it. The example meets it through τ(r_0) > 1/2 (Lemma A.10(a)).
2. **The scope of O5.** PLAN.md Part 5 says "for every incumbent distribution". Existence at the prior 1/2 holds for every continuous F with τ > 1/2 and can fail without that hypothesis (`O5/O5_notes.md`). The brief and the referee's sketch both carry τ > 1/2.
3. **The start margin in T-P3(c).** It is not a hypothesis (`O9/O9_notes.md`, point 3).
4. **Decision 4.** O9 holds, so Proposition 3(c) leads with the balance condition and gives the uniform incumbent as its primitive case.

## Changes after the referee

The referee's report is `statements/B_referee.md`; its issues are in the body, B-01 to B-08. Each line gives the issue and where the statements meet it.

- **B-01, threshold-pair scope.** Proposition 3(c)(iv) has three sentences. The first, Δ_T(1 − τ)² nondecreasing, needs only the path hypotheses. The second takes the mixing investor and the challenger who may prepare with any probability, says the threshold pair qualifies exactly where π < τ < M and ρJ ≤ k ≤ J, and gives the entry comparison on those strengths. The third treats τ = M as the full purchase. The frame sentence of the full statement exempts the second sentence from the default rules. Item 5 above gives the derivation.
- **B-02, the band.** The marked-strengths paragraph splits the strengths that do not depend on the slot (r_A, r_N, r_J, r_*) from those defined for a slot with τ(r_1) < M(1/2) < τ(r_2) (r_F, r_S, r_C, with r_C in (r_1, r_2)). The forms paragraph and the prior-1/2 part of "Other tie rules in the example" state the same band. The forms paragraph names the default rules, says F at r_C takes e(1) = 1 because the challenger prepares and T needs J = k, and names the alternative challenger rule at both points. Corollary A.2 and the general-prior sets keep every slot.
- **B-03, slot-dependent endpoint values.** The singleton {r_*} at π_max is stated at every slot. The four evaluations start "At the example's slot", with λ and β printed through `lambda_B` and `beta_B`, and the sentence says the informative market there is a full purchase. Item 17 records the slot λ = 2/5, β = 1/5, where it is a mixed purchase.
- **B-04, entry at τ = π.** The general tie paragraph reads "one quiet market has entry ρ after every order, and one informative market is constructed as in part (a), with entry ρ after a sale". Item 8 gives the set of quiet-market entries.
- **B-05, the threshold rate.** The setting defines s* for π < τ < 1 as the positive rate at which a purchase reaches the threshold, feasible exactly when τ ≤ M.
- **B-06, notation.** O9 writes the class mean gap as Γ̄ and writes g_H − c_H, (r² − p²)/(2r²), E_Hθ, E_Lθ and E_Lθ² out; the card reserves v for the volume and m for the bottom posterior, so v_j and m_2 are written out as well. Proposition 3(d) and O5 write the sale rate as ŝ_-, the rate of Lemma A.8. The two-interval path is indexed by r, and its slot condition prints through `tau_r1_frac` and `tau_r2_frac`. The notes write Δ_T, Δ_T^F and Δ_T^N throughout, and the Lemma A.10 comment and key definitions write W1's X and Y out.
- **B-07, the derivative at min I.** `O9/O9_notes.md` states J′ ≥ (r² − p²)Δ_T²/(2r²γ²) ≥ 0 on I, strictly where Δ_T > 0, and the case of a low class concentrated at min I, where J′ = 0. The proof's last sentence states the same.
- **B-08, narration in the notes.** The notes give source, placement, numbering and exact values as reference data, as manuscript-against-statement tables where a mapping is needed, and state each scope directly. `O5/O5_notes.md` and `O9/O9_notes.md` follow the same form.

The rebuilt `B.tex` and the print-only computations for B-02, B-03 and the two-interval path reproduce the referee's values.
