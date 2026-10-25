I applied the author's scope decision and reissued the full findings below. All items about `c_H` are gone: the old 02:91 item, the `c_H`/`c_L` row at A9:19, the `c_H` bullet in pattern 3, the `\bar c` suggestion and the cost row of the notation table. I also propose no general cost law and no restatement of the cost model.

One related item stays, narrowed: inside Proposition A.4 (`prop:atomless`, A6:73), its cost-law symbols `H_C, H^0, H^1` and the bound `L` reuse the class letters H and L. I suggest renaming those symbols only; the proposition and its content stay as they are. Drop that item too if the author wants Proposition A.4's notation left alone. Where my first report wrote "Proposition A.?", I now cite the label (`prop:payment`, `prop:control`).

**Defect outside the brief:** `sections/02_model.tex:1` begins `ty\section{The model}`. The stray "ty" prints in the PDF.

**Negative result:** `b` has one meaning throughout, `(1-λ)β` (its variants `b_0`, `\hat b` and `\bar b` are all liquidity masses). The only Laplace words outside the permitted footnote are at 08:79 and A4:409.

Each item reads: file:line, "quote", [category], fix.

## main.tex
- 92–93 "a challenger from the high-value class acquires" [1/5]. Use "a class-H challenger acquires".
- 93–95 "informative and uninformative equilibria coexist … rises and then stays constant" [3]. `prop:coexistence` assumes the benchmark auction at prior 1/2. Use "In the benchmark auction, …".
- 95–96 "research and entry rise together over a range of strengths" [3]. `prop:research` has the same benchmark restriction. Add the qualifier.
- 54 and 57, the macro comments "(entry is e(x))" and "root of Delta_T(r) = d" [4]. These are the three E's (`\mathbb E`, `\mathsf E`, `e(x)`) and `d` (also the signal accuracy). See patterns 2 and 5.

## sections/01_introduction.tex
- 9, 41 "challenger from the high-value class" [1/5]. Use "class-H challenger".
- 13–14 "Incumbent strength is the public distribution" [5]. Elsewhere strength is the scalar `r` (04:79). Use "the incumbent's value law F; for the uniform family, its strength r".
- 19 "from a high-value or a low-value quality class" [1/5]. Use "from one of two quality classes, H and L, with ranked value distributions".
- 54 "the entry ceiling, the strength r_C" [5]. Pattern 4.
- 61 "Informative and uninformative equilibria coexist on an interval of strengths" [3]. Use "Along the benchmark path, …".
- 70–75 "The unique outcome has no research … at the cap", "for every liquidity probability" [3]. Use "In the benchmark auction at prior 1/2, …".
- 81–82 "the buyer and the investor", "the buyer's signal" [5]. Use "challenger".
- 87–89 "the effect of competition on the target-payoff spread depends on the weight" [3]. `prop:payment` covers point-mass classes with zero reserve only. Add "With point-mass classes, …".
- 89 "A reserve that excludes the low-value class" [1]. Use "A reserve above every low-class value".
- 93–96 "the entry component of the spread between purchase and sale prices … of the spread" [4/5]. Use "purchase–sale price gap" and keep "spread" for Δ_T.
- 108–109 "learns about its own acquisition value from the target's price" [1]. Use "learns about its class, and so about the distribution of its value".

## sections/02_model.tex
- 30 "Public incumbent strength is a distribution" [5]. Same issue as 01:13.
- 52–53 "F on [0,\bar r]" [4]. Collides with `\bar r_R` (05:119).
- 54–55 "In the main case R is uniform on [0,r]" [3]. Use "In the benchmark, R is uniform on [0,r]".
- 62 "The high class, or high-value class," [1/5]. Delete "or high-value class".
- 69–73 "the spread rises under every strengthening" [4]. Used before its definition at 02:199. Define `t_j` and Δ_T earlier, or forward-reference.
- 123–124 "the ceiling of Section~\ref{sec:inference}" [5]. Use "the posterior bound".
- 162–163 footnote, "\eu … printed upright to separate it from entry e(x)" [2/4]. The footnote itself is permitted. The upright e is needed only because the benchmark sets 1+u=e (pattern 2). The footnote's `s` also collides with the purchase rate `s` in A4.
- 191 "e(q) is entry after the order q" [4]. Entry appears as `e(x)`, `\Ent`, `e_H` and `\Ent_F`, alongside `\E` and `\eu`.
- 203–204 "g_j(F), \DT(F), B_F; … g_j(r), \DT(r), B_r" [4]. The argument switches between a law and a scalar, and `F_r` (A5), `\Ent_F` (A4) and `B_i` (A3) then read as instances.
- 228 "W_H(F)" [4]. Near-collision with `w_H` (A2:23), `w_x` (A8:167) and `\mathcal W` (A7:10).

## sections/03_competition_information.tex
- 80–82 "approaches zero as r approaches ℓ … low-value challenger. As r increases" [1/3]. Use "In the benchmark, … a class-L challenger (value ℓ). As the incumbent strengthens, …".
- 94 "This gives the ceiling of the model" [5]. Use "the posterior bound on preparation".

## sections/04_equilibrium_results.tex
- 52 "The ceiling (H3)" [5]. Use "the exclusion condition (H3)".
- 83, 124 "1+u=\eu" [2/4]. Pattern 2.
- 121, 131 "the admissible region at the benchmark auction" [4/5]. "Admissible" already means a bid that meets the reserve (02:101). Use "hypothesis region".
- 158–160 "a high-class challenger outbids every incumbent on the path … r/2+p^2/(2r)" [1/3]. Use "in the benchmark h exceeds every strength on the path, so a class-H challenger always wins and pays r/2+p^2/(2r)".
- 194 "gross profit at the two strengths" [5]. This is the general `prop:control`. Use "at the two incumbent laws".
- 220, plus A6:50 and 53: "Full orders held fixed", "frozen profile", "fixed-information control" [5]. Pick one name.
- 267 "the sale threshold r_S" [5]. "Threshold" names τ, the strengths r_A to r_C (A4:116) and the pair T. Keep it for τ and say "marked strengths" for the r's.
- 301–302 figure labels N, R, F, Q, T [4]. R, F and T collide with R, F and Δ_T/the signal T, and A5 reuses R and T for different tuples.

## sections/05_research.tex
- 1, 52 Section and proposition title "Competition creates research" [3]. The hypothesis is the benchmark auction at prior 1/2. Title the proposition "… at the benchmark auction".
- 5 "cost (a/2)λ^2, where a>0" [4]. Collides with the accuracy `a_T` (06:61).
- 32, 42 "λ_E(r)", "λ_R(r)" [4]. The subscripts read as `\Ent` and the incumbent value R.
- 119 "[r_R,\bar r_R)" [4]. Collides with `\bar r`. Use `r_R^{cap}`.
- 154 "admissible region of the research parameters" [4/5]. Use "parameter region".
- 158 "With 1+u=\eu" [2]. Pattern 2.

## sections/06_robustness.tex
- 42 "a mean-preserving spread within a class" [4/5]. A third sense of "spread". Use "a mean-preserving increase in risk".
- 61 "accuracy a_T … accuracy d" [4]. `a` is the research cost, T the target subscript, `d` the argument of `\fr`. Use `α_I` and `α_C` (α is unused).
- 79 "a buyer signal" [5]. Use "the challenger's signal".

## sections/07_welfare.tex
- 30 "recruitment region" [5]. A third name for the H1–H3 set, after "admissible region" and "band".
- 32 "with the strong benchmark" (also A7:90) [5]. Use "in the benchmark at r_1".
- 42–45 "The effect of competition on the target-payoff spread depends on the sale payment" [3]. Use "With point-mass classes and zero reserve, …".
- 52–53 "A high-class challenger wins and pays (1−ω)R+ωh" [1]. Use "A class-H challenger, whose value h exceeds the incumbent's support, …".
- 70–71 "A reserve that excludes the low class … adds nothing" [1/3]. Use "A reserve above every low-class value (in the benchmark, p>ℓ)".

## sections/08_empirical.tex
- 19, 22, 28–30, 40 "The price spread" against "target-payoff spread" at 42 [4/5]. Use "price gap".
- 49–50 "A prepared high-class challenger always outbids the incumbent" [1/3]. Use "In the benchmark, where h exceeds every strength, a prepared class-H challenger always wins".
- 79 "such as flow from sector specialists" [2]. Use "orders from sector specialists".

## sections/09_conclusion.tex
- 10–13 the coexistence and entry-path sentence [3]. Use "Along the benchmark path, …".
- 14–15 "research and entry rise together" [3]. Add "in the benchmark auction".
- 19–21 the payment-rule claim and "A reserve that excludes the low class" [3/1]. Add "with point-mass classes" and "above every low-class value".

## appendix/A1_payoffs.tex
- 13 "\mathcal{E}=(σ_H,…)" [4]. A fourth E. Use Σ (unused).
- 22 "\bar P in the image of P" [4]. A8:229 uses `\bar P` for the expected price.
- 27 "f_j(x)=(1-λ)η(x)+λσ_j(x)" [4]. Reads as the density of F. Use `ψ_j(x)`.
- 59 "Y≥0 the highest competing admissible bid" [4]. `Y` is also the signal (A6:385) and an indicator (A8:188).
- 77–78 "the high-value challenger always wins", "The low-value challenger" [1/5]. Use "the class-H challenger (value h)" and "the class-L challenger (value ℓ)".
- 178, and A7:147 "kernel ξ" against "kernel (t_v,g_v,W_v)" [5]. Two objects share the name.
- 213–214 "g_j=∫_p^θ F at θ=h and θ=ℓ" [1]. Write `g_H=∫_p^h F` and `g_L=∫_p^ℓ F`.

## appendix/A2_beliefs_trading.tex
- 23–24 "w_j=t_j−t_0 … w(μ)" [4]. Collides with `W_H`, `w_x` (A8), the weights `w_j` and `w` (A6) and `\mathcal W`. Keep `w` here and rename the others.

## appendix/A3_proposition2.tex
- 4, 157 "the admissible region" [4/5].
- 79 "e_H, e_L" class entry [4/5]. A6 writes `\bar e_H` and `e_H(μ)`. Use `\Ent_j`.
- 124, 134–135, 155, 226, 231 "calibration B" [4/5]. Pattern 1.
- 142 "every quantity that depends on \eu" [2]. Pattern 2.
- 226 "trade bound" against "trading bound" [5].

## appendix/A4_coexistence.tex
- 17 "\fr(d) … root of \DT(r)=d" [4]. Use `\fr(Δ)`.
- 32 "D_τ" [4]. Collides with `D(y)`.
- 107, 116, 120, 399–400, 414 "calibration B", "Value at B" [4/5].
- 135 "s=s_+=λσ_H(1) and t=s_-=λσ_L(−1)" [4]. `t` is proceeds (`t_0` at 231 in the same lemma). Use `s_+` and `s_-` only.
- 204 "s_-^*(r)" against "s^*" (152) [4/5]. The star has two meanings. Use `\hat s_-(r)`.
- 166 "e^*:=k/J(r)" [4]. A5:57 redefines it. Write `e^*_a`.
- 305 "\Ent_R, \Ent_F, \Ent_T" [4]. The subscript F means the law in `B_F`. Use `\Ent^{\rm F}`.
- 409 "from the flow law" [2]. Use "the order law".
- 441 "C(π)" [4]. Collides with the cost variable `C` and the rules C1/CM. Use `\mathcal C(π)`.
- 551, 595 "no admissible (sale) rate" [4/5]. Use "no qualifying rate".

## appendix/A5_research.tex
- 4, 316 "the admissible cap and cost" [4/5].
- 18 "research value V" [4]. Collides with `V_T`. Use Ψ.
- 40, 61, 255, 286, 317, 339 "calibration B" [4]. 61 and 317 sit next to `B_r`.
- 47–54, 267–276, 346, 364 "F_r(λ)", "F_{1.65}(\lb)" [4]. These read as the uniform law. Use `Λ_r(λ)`.
- 57 "φ_a(r)" [4]. Collides with `φ_±(μ)` (A6:392).
- 127–135 forms (Z), (R), (\bar R), (T) [4]. R and T mean different tuples in A4.
- 373 "λ_B(β)" [4]. Use `λ_\star(β)`.
- 419 "allocation value" against "acquisition surplus" [5].

## appendix/A6_robustness.tex
- 31 "A tie probability q" [4]. `q` is the order. Use `\bar ζ`.
- 73 "H_C=ρH^0+(1−ρ)H^1, supp H^0⊂[0,L]" [4]. The symbols in Proposition A.4 reuse the class letters H and L. Rename the letters only and leave the result unchanged; for example `Φ, Φ^0, Φ^1` and bound `c_0`. The same applies to A9:30 "Cost law L".
- 128 "\bar e_H" [5]. See A3:79.
- 237, 360, 467, 491, 506–507, 521–522 "slot of B", "S(B)", "The benchmark B", "At B" [4/5]. Pattern 1.
- 245 "t_v, g_v, W_v for a point value v" [1]. Use `t(v)`, `g(v)`, `W(v)` (02:196).
- 254, A7:158 and 163 "class order" [5]. Use "class ranking".
- 279 "classes j=1,…,J" [4]. Collides with `J(r)` and `r_J`. Use `n`.
- 285 "\mathcal L low group" [4]. A6:11 uses `\mathcal L_i` for a law.
- 332, 371, 507 "z" as group posterior, conditional means and 2a_T−1 [4]. `z` also has meanings at 07:27, A5:65 and A7:119.
- 352, 362 "weights w_j", "w=(1+2b_0+λ)/2" [4]. Use `υ_j` and `υ`.
- 361–364 "t_0=7/8, (t_1,t_2,t_3)" [4]. Index the classes a, b, c.
- 385–389 "T∈{+,−} with accuracy a_T … Y" [4]. Use `S_I`, `S_C` and `α_I`, `α_C`.
- 391 "μ_-=…, μ_+=…" are numbers here but functions in A4:142 [4].
- 393 "D^+(r)" [4]. Collides with `D(y)`.
- 397 "f_t(x) … given T=t" [4].
- 519 "satisfy the theorem" [5]. Use "the proposition".
- 524 "t=λσ_-(−1)" [4]. Same as A4:135.

## appendix/A7_welfare.tex
- 10–11 superscripts 1/0 for access/hidden [4]. Subscripts 0/1 mean weak/strong elsewhere. Use `^{\rm acc}` and `^{\rm hid}`.
- 47 "\mathcal V_0(R)" [4]. Collides with `V_T` and `V`.
- 69 "G=λΔ_1{…}" [4]. Collides with `G_j`. Use `Π_I`.
- 103 "Let the challenger's values be the point masses ℓ and h" [1]. Use "Let the classes be point masses at h and ℓ".
- 107–108 "T_ω(R,θ)", "g_{θ,ω}" [1/4]. Write `g_{j,ω}`.
- 119–120 "(P−z)^ω(V−P)" [4]. `P` is the stock price. Write `(T−y)^ω(v−T)^{1−ω}`.
- 146–157 "(t_v,g_v,W_v)" [1]. Same fix as A6:245.
- 196 "T=…, C=c_H−B(1/2) and J=B(M)−c_H" [4]. The margin names collide with the signal T, the cost variable C and `J(r)`. Name them in words.
- 222 "p_H" [4, minor].

## appendix/A8_empirical.tex
- 5 "A_r(μ) … is the function w(μ)" [4/5]. One object has two names, and `A` is also the event at 166. Use `w_r(μ)`.
- 8 "\vartheta=u/(2+u)", "v=Pr(X≠0)", "\bar f" [4]. Use `ι` for the informed share.
- 15 "D_S=k/(ρm)" [4].
- 21 "The tuple \mathcal F" [4]. Collides with the law F and the form F. Use `\Sigma_{\rm full}`.
- 41, 45, 80, 82 "The spread S=P(1)−P(−1)" and the proposition title "The spread and its entry component" [4/5]. Section 8 says "price spread", and `S` is the signal. Use "price gap".
- 98 "and the spread \DT(r)" [4/5]. The second sense of "spread" in the same subsection. Use "target-payoff spread".
- 42 "I_+, I_-" [4, minor]. Collides with `I_y` (A6) and the rules IM/I0.
- 166–167 "w_x=Pr(W|X=x,A)" [4]. `w_1` against `w_1(μ)` in A3:61. Use `ϖ_x`.
- 229 "\bar P=∑_x …" [4]. Collides with A1:22.
- 243 "v_U=2b+λ/2" [5]. A second name for `v`.

## appendix/A9_parameters.tex
- 4, 10, 94, 96, 169 "calibration B", "Value at B" [4/5].
- 23 "u=\eu−1" [2]. Pattern 2.
- 30 "Cost law L; ε" [4]. The letter only; see A6:73.
- 32 "Four-class values θ_1,…,θ_4" [1]. Use `v_1..v_4`.
- 49–58, 192–199 "The vector S(B)" and the "S(B): …; B: …" cells beside `B_{r_0}(d)` [4]. Call it "the signal example".
- 201, 231, 244 "T, C, J", "C_0, C_1, T_0, T_H, T_L, C_2, O" [4]. Use word-labelled columns.

## Systematic patterns
1. **"Calibration B", "B", "S(B)", "λ_B" against gross profit B(μ)** (about 35 items in A3–A6 and A9). Use "the benchmark" and "the signal example". The registry keys don't print and stay as they are.
2. **1+u=e is the Laplace s=2 inheritance.** It is the only reason the main text needs Euler's e set apart from `e(x)`. The author decides whether to say so once in the benchmark declaration or to choose a rational u.
3. **Class letters H and L on non-class objects.** These are the Proposition A.4 cost-law symbols `H_C, H^0, H^1, L`, the margins `T_H`/`T_L`, and `p_H`. This is a symbol rename only.
4. **One word, several meanings.** "Spread" should mean Δ_T only; the others become "price gap" and "increase in risk". "Admissible" should mean a bid that meets the reserve only; the others become "parameter region" and "qualifying rate". "Ceiling" should mean `r_C` only; the others become "posterior bound" and "exclusion condition". "High-value class" becomes "class H".
5. **Letter collisions across sections.** `t`/`s` as rates, `F_r(λ)`, `w`/`W`/`w_x`/`\mathcal W`, `V` against `V_T`, T/C/J as margins, `A_r=w`, `G`, `\bar P`, `\mathcal E`/`\mathcal F`, R/T/F form labels, `e^*` and `μ_±` each defined twice, and `z`, `v`, `d`, `a`, `Y`, `D_*`. Unused letters available: ψ, Ψ, ι, Φ, Λ, Σ, α, υ, ϖ, `\mathcal C`.
6. **Benchmark-only results stated generally.** `prop:coexistence`, `prop:region`, `prop:research`, `prop:researchregion`, `prop:payment`, `prop:priors`, all of A8 and the reserves table carry benchmark or point-mass hypotheses. The general results are returns, ccc, control, atomless, classes, manyclasses, access and reserves. The abstract, intro, conclusion, 02:54, 03:80, 07:42/70, 08:49 and the Section 5 title need qualifiers.
7. **Value used as a class index.** `t_v`, `g_v`, `W_v`, `g_{θ,ω}`, `θ_1..θ_4`, and `g_j` "at θ=h". Use `t(v)` and the subscript j.
8. **Synonyms for one object.** Entry given class (`e_H`, `\bar e_H`, `e_H(μ)`); `w` against `A_r`; held-fixed, frozen and control; "class order" against "class ranking"; "strength" for both F and r; "buyer" against "challenger".

## Notation table
| Symbol | Meaning | First defined | Uses to retire |
|---|---|---|---|
| j∈{H,L} | challenger class | 02:57 | "high-value class"; H/L letters in the Proposition A.4 cost law and the A9 margins |
| π | prior Pr(j=H) | 02:57 | — |
| G_j | value law of class j | 02:58 | G as investor profit (A7:69) |
| θ | value drawn from G_j | 02:58 | θ_1..θ_4 (A9:32), g_{θ,ω} (A7:108) |
| D(y) | G_L−G_H | 02:60 | D_τ, D^+, D_S |
| p | reserve | 02:59 | P as a bargaining payment (A7:120), p_H |
| F, \bar r | incumbent law, support bound | 02:52 | F_r(λ), \mathcal F, form F, \bar r_R |
| r | uniform benchmark strength | 02:55 | "strength" = F (01:13, 02:30) |
| R | incumbent value | 02:52 | form label R (A4/A5) |
| h, ℓ | benchmark point masses | 02:78 | "high/low-value challenger" |
| C, ρ, c_H | preparation cost (kept as is) | 02:91 | C(π) (A4:441) and margin C (A7:196) only; c_H itself unchanged |
| λ, β | presence, liquidity probability | 02:119 | λ_B |
| b, b_0, u | liquidity masses, λ/b | 02:142, A2:32 | — (single meaning) |
| M(π), m(π) | top and bottom posterior | 02:146 | μ_± as numbers (A6:391) |
| q, x, X | own order, generic order, observed order | 02:120, 130 | q as tie probability (A6:31) |
| k, κ(π) | trading cost, trading-bound fraction | 02:120, 03:121 | — |
| μ, P, \bar μ | posterior, price, belief at a price | 02:181 | \bar P as expected price |
| e(x), \Ent, \Ent_j | entry by order, total entry, entry by class | 02:191, 225, A3:79 | \bar e_H, e_H(μ), e_r, \Ent_F |
| \eu | Euler's number | 02:163 | tied to 1+u=e |
| t(θ), g(θ), t_0 | proceeds and profit at a value; no entry | 02:196, 107 | t_v/g_v/W_v; t as a rate or signal |
| t_j, g_j | class expectations | 02:199 | (t_1,t_2,t_3) next to t_0 |
| Δ_T | target-payoff spread | 02:199 | "price spread", "the spread S" |
| w_j, w(μ) | entry gain | A2:23 | A_r, w_x, weights w |
| B(μ), B_F, B_r | gross profit | 02:202 | "calibration B", S(B), λ_B |
| τ | preparation threshold | 03:99 | "threshold" for r_A..r_S |
| K_j | gross return of a correct order | 03:119 | — |
| W_H(F) | class-H win probability | 02:228 | \mathcal W, w_x |
| \Own_H | high-class ownership | 02:225 | margin O |
| r_A…r_C | marked benchmark strengths | 04:262 | "ceiling" other than r_C |
| a, \bar λ | research cost, cap | 05:4 | a_T → α_I |
| λ_E, λ_R | recruitment intensity, research choice | 05:32, 42 | F_r → Λ_r, V → Ψ |
| Σ (now \mathcal E) | equilibrium tuple | A1:13 | collides with \E, \Ent |
| ψ_j (now f_j) | order probability by class | A1:27 | reads as the density of F |
