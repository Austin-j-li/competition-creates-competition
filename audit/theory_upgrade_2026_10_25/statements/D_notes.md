# Area D: notes on the statements of Appendix A.8 and Section 8

The mathematics writer to the coordinator, 25 October 2026, stage S4. The statements are in `statements/D.tex`, which builds on its own from `../tex/preamble` (nine pages, no overfull box, no undefined reference). The seven example values listed in part 4 print as placeholders until the production assistant adds their keys. No proof obligation of Part 5 belongs to area D.

Sources: referee reports W4 and W5, `plan/PLAN.md` (S4, S5 item 5, Part 6), `plan/DECISIONS.md` (decisions 5 and 7), `plan/NOTATION.md`, `plan/lens_theory.md` (S6 and part 3.2), the S0 label map, and the manuscript copy `slot/manuscript/` (`appendix/A8_empirical.tex`, `sections/08_empirical.tex`, `appendix/A2_beliefs_trading.tex`).

## 0. Numbering

Decision 7 and Part 6: Proposition A.1 and the example part of Proposition 4 become the full Corollaries 1 and 3 of the main text, which have their own counter, and the later appendix propositions move up by one.

| Label | S0 label map | Number in the final build | Title in `D.tex` |
|---|---|---|---|
| `prop:spread` | Proposition A.11 | Proposition A.10 | The price gap and the weighted test |
| `prop:informedshare` | Proposition A.12 | Proposition A.11 | What order counts and prices identify |
| `cor:purchasesonly` | Corollary A.3 | Corollary A.3 | Counts under purchases only |
| `prop:winner` | Proposition A.13 | Proposition A.12 | Orders predict the winner |
| `prop:announcement` | Proposition A.14 | Proposition A.13 | Announcement returns |

- Labels stay as they are. The titles of A.10 and A.11 change with their content (S0 titles: "The spread and its entry component"; "Identification of the informed share"); the other three keep theirs.
- Two labelled displays: `eq:a8-full` (the order law under full two-sided trade) and `eq:a8-balance` (the balance identity). They take the appendix equation counter; the draft prints (1) and (2).
- The example is an unnumbered `named` block, "The example", at the end of A.8. Its eight parts can equally stand as paragraphs.
- No lemma, numbered table or remark is added. The sign table of A.10(iii) sits inside the proposition and has no number.
- The numbers assume that no other area adds an appendix proposition before A.8 or an appendix corollary before Corollary A.3. The S12 comparison of label maps settles this.

Cross-references fixed by stubs at the top of `D.tex`:

- `prop:region` prints "Corollary 1": the full Corollary 1 is taken to keep the label of S0's Proposition A.1.
- `cor:coexistence` stands in for the label of the full Corollary 2 (the example's coexistence set, area C, A4). The current A8 cites `prop:coexistence` (main-text Proposition 3 in S0). The coordinator sets the label once A4's statements fix it.
- `lem:a4-order` prints A.5 (its S0 number). It moves with the lemmas placed after Lemma A.3 (Part 6; the area A statements place Lemmas A.4 to A.6).
- `lem:beliefs`, `lem:prices`, `lem:trading` print A.1, A.2, A.3, as Part 6 keeps them.

## 1. Where the referee decides

The referee reports decide each point below. Where the plan's wording is wider, the statement follows the report.

1. **The weighted test needs full two-sided trade and a prior below the threshold.** Plan, S5 item 5: "the weighted price test at every prior". W5, "Shared candidate 1" and "The purchases-only false positive is an equilibrium": the price identity holds in every equilibrium, but its reading as a recruitment test needs full two-sided trade (so the posterior after no order is the prior) and π < τ. At π = 0.3, r = 2, a purchases-only equilibrium has entry ρ after every order and a positive weighted impact difference (0.008685; W5 gives the same value). A.10(i) is the identity in every equilibrium; A.10(ii) adds full two-sided trade, and its test adds π < τ. "Every prior" therefore reads "every prior below the threshold", as PLAN S4's acceptance list says.
2. **The hidden-price comparison needs full orders in the hidden economy.** W5, "Full-order existence, uniqueness and the hidden-price comparison": at π = 0.6, r = 2.3, hiding the price makes class H mix, and E[P(X)] − P(0) = −0.004489. A.10(iv) states the comparison under the trading margin ρκ(π)Δ_T − k > 0 (W5 eq. (7)), which forces full two-sided trade in both economies under both investor rules, and under π < τ.
3. **The unweighted test needs no exact symmetry.** Plan: "the unweighted test, kept as a part at π ≥ 1/2". W5, "Primitive rescue of the naive impact comparison": π ≥ 1/2 and ρ ≤ 1/2 suffice when an indifferent high-cost challenger prepares; when it may prepare with any probability the comparison can fail (W5: π = 0.6, r = 3, e(1) = 0.251). A.10(v) states the formula under full two-sided trade with π < τ, and the equivalence "I_+ > I_− exactly when π < τ ≤ M" under π ≥ 1/2, ρ ≤ 1/2 and the preparing tie rule.
4. **Unknown prior.** W5, "Shared candidate 2" and its verdict table: count nonidentification at an unknown prior holds only locally and with feasibility restrictions; the universal form is false. Decision 5 leaves the unknown-prior result out. A.11 keeps the known-prior result (a) and the sale-price inversion (c).
5. **The entry-component trend needs a condition beyond first-order dominance.** W5, "Entry-component trend: exact condition and counterexamples", including the counterexample that keeps the example's prior, reserve, slot and costs. A.10(vi)(a) states the exact pairwise condition; (vi)(b) the two sufficient conditions (constant reserve-failure probability; uniform incumbent with p < min{θ_low, r_low}/√3). The example meets the second with ℓ² − 3p² = 1/4.
6. **The winner trend is weak, and strict exactly when W_L falls.** Plan: "the gap widens under outbidding". W4, "High-class outbidding" and the ranking paragraph: with the prior and slot fixed and W_H = 1, the gap is nondecreasing, strictly larger exactly when the low class's win probability falls. A.12(v).
7. **The tie at τ = π.** W5, the tie subsection of "Shared candidate 1": when an indifferent high-cost challenger may prepare with any probability and τ = π, the weighted moment takes any value between the two one-sided signs. A.10(iii) gives the sign table when an indifferent high-cost challenger prepares, restricts it to τ ∉ {m, π, M} when it may prepare with any probability, and states the three tie cases.
8. **Corollary A.3(b) on the whole segment.** W5, "Purchases only and Corollary A.3", proves observational equivalence for presence probabilities near the true one ("local"). Its argument uses only that the class-conditional order laws f_H = (b, 1 − 2b − s_+, b + s_+) and f_L = (b, 1 − 2b, b) depend on (b, s_+) alone, so that posteriors, prices, entry and deviation payoffs do not change. That argument covers every λ' in [s_+, 1 − 3b] when an indifferent investor may mix: λ' ≥ s_+ keeps σ'_H(1) = s_+/λ' ≤ 1, and λ' ≤ 1 − 3b keeps β' = b/(1 − λ') ≤ 1/3. The statement gives the whole segment; the referee reads the step from "local" to the segment at S4. The recruiting-branch formula s_+ = (b/π)[(1 − π)Δ_T/k − 1] is W5 eq. (14), which assumes entry one after a purchase; the statement gives the general form with e(1) and this case.
9. **The informed share.** W5, "Shared candidate 2" (W5:325–332): the informed share is λ/v at every prior, and M − m equals it only at the prior 1/2. The standing paragraph states both.

## 2. The statements

### Standing paragraph (`D.tex`:35–74)

- **Source.** W5, "Shared candidate 1", eq. (1), and its paragraph on a fixed public state (W5:121); W5, "Shared candidate 2", subsection "Full two-sided trade" (W5:210–277, 325–332).
- **Scope.** Any continuous incumbent law, the class ranking (1), any prior π in (0, 1), Δ_T > 0 and γ > 0 as in Lemma A.2. Every statement concerns one target in one public state, with its prior, slot and incumbent law fixed. Entry at a posterior equal to τ is given for both challenger tie rules in plain phrases. The full-trade facts: order law (eq:a8-full), balance identity (eq:a8-balance), ϑ = λ/v = u/(2 + u) at every prior, M − m ≤ ϑ with equality exactly at the prior 1/2, and entry ρ after a sale and after no order when π < τ.
- **Manuscript lines.** `appendix/A8_empirical.tex`:3–12 (the opening; its facts about the example move to the example), 35–37 (the full-trade frequencies), 41–43 (impacts, price gap, no quote stage).
- **Number.** None (running text).

### Proposition A.10, `prop:spread` (`D.tex`:85–174)

- **Source.** W5, "Shared candidate 1", eqs. (1)–(6), the threshold classification table and its tie subsection; "Full-order existence, uniqueness and the hidden-price comparison", eq. (7); "Primitive rescue of the naive impact comparison", eqs. (15)–(16); "Entry-component trend: exact condition and counterexamples", eqs. (17)–(19); "Ceiling jumps".
- **Scope by part.**
  - (i) Every equilibrium, every trading pattern, any prior, both tie rules.
  - (ii) Full two-sided trade, any prior. The test adds π < τ and holds under both challenger tie rules.
  - (iii) Full two-sided trade. The table: an indifferent high-cost challenger prepares. The tie cases τ = M, τ = m, τ = π: an indifferent high-cost challenger may prepare with any probability.
  - (iv) The split of the price gap: full two-sided trade with π < τ. Forcing: ρκ(π)Δ_T − k > 0, both investor rules, visible and hidden price. The hidden-price comparison adds π < τ.
  - (v) The formula: full two-sided trade with π < τ. The equivalence: full two-sided trade, π ≥ 1/2, ρ ≤ 1/2, an indifferent high-cost challenger prepares.
  - (vi) A path along which Δ_T rises strictly, the prior and slot fixed. (a) Every belief. (b) F_r(p) constant on the path, or F_r uniform on [0, r] with r > p and p < min{θ_low, r_low}/√3. (c) An indifferent high-cost challenger prepares; full two-sided trade at every strength of an interval on which π < τ(r) and w_r(M) rises strictly. (d) F_r(y) continuous in r; a crossing strength r_C; full two-sided trade and π < τ(r) on a neighbourhood of r_C; both challenger tie rules at r_C.
- **Manuscript lines.** `appendix/A8_empirical.tex`:45–58 (statement), 60–78 (proof, which S5 writes from the sources above), 79–83 (the example's numbers and the tie remark, which move to the example).
- **Number.** Proposition A.10 (A.11 in S0).

### Proposition A.11, `prop:informedshare` (`D.tex`:182–210)

- **Source.** W5, "Shared candidate 2", eqs. (8), (9), (11), (12), the variance display, and "Sale-price identification with an unknown prior" (the inversion). Part (b) keeps A8:88–96 with W5's feasibility restriction ϑ' ≥ 3 − 2/v (eq. (10), last inequality) and W5:186–189 for the incentive condition (weak under the mixing rule, strict under the abstaining rule). Decision 5: the unknown-prior identified set (W5 eq. (10)) is left out.
- **Scope.** Full two-sided trade throughout. (a) A known prior π ≠ 1/2; independent order opportunities for the variance; the identification of ρΔ_T adds π < τ. (b) The prior 1/2 and τ > 1/2; the entry formula when an indifferent high-cost challenger prepares; the equilibrium condition for each investor tie rule. (c) Entry ρ after a sale and after no order, and ρΔ_T known; (c) identifies the prior as well.
- **Manuscript lines.** `appendix/A8_empirical.tex`:85–102 (statement), 104–130 (proof), 131–142 (the example's numbers move to the example; the reference at 141–142 goes).
- **Number.** Proposition A.11 (A.12 in S0).

### Corollary A.3, `cor:purchasesonly` (`D.tex`:218–233)

- **Source.** W5, "Purchases only and Corollary A.3", eqs. (13)–(14) and the class-conditional laws.
- **Scope.** The purchases-only pattern: class L abstains and class H buys with probability σ_H(1) > 0; any prior; both challenger rules. (a) The counts at every prior; s_+ at a known prior; λ when class H buys surely. (b) An indifferent investor may mix, and 0 < σ_H(1) < 1; the whole segment λ' in [s_+, 1 − 3b] (point 8 of part 1); the indifference formula for s_+ with e(1), and its form when every challenger prepares after a purchase.
- **Manuscript lines.** `appendix/A8_empirical.tex`:144–150 (statement), 152–164 (proof). The example's part (the full purchase on [r_F, r_N], the mixed purchase on (r_A, r_F)) moves to the example, part (e).
- **Number.** Corollary A.3, unchanged.

### Proposition A.12, `prop:winner` (`D.tex`:243–285)

- **Source.** W4, the section on the general identity and its sign (parts (i) and (ii)); the section on the covariance constants, the arbitrary-prior display, with W5's numerical audit (last paragraph) for Cov(X, 1_prep) (part (iii)); the section on the two channels and the winner second difference, including the general-prior display (part (iv)); "High-class outbidding" (part (v)); "Exact uniform-family condition" (part (vi)). Ω, D and Γ as in W4's opening display and `NOTATION.md` (Γ(x) = ∫_p^x D).
- **Scope.** (i) Every equilibrium, any prior, both rules; Ω(F) > 0 exactly when Pr_F{D(R) > 0} > 0. (ii) Full two-sided trade, any prior. (iii) Full two-sided trade with π < τ; the post-ceiling form under B_F(M) < c_H. (iv) Full two-sided trade with π < τ; the two-channel form at the prior 1/2 when an indifferent high-cost challenger prepares. (v) A path, the prior and slot fixed, W_H(F_r) = 1 at every strength, full two-sided trade at the compared strengths. (vi) F_r uniform on [0, r] with r ≥ p; the winner gap at a fixed prior and slot.
- **Manuscript lines.** `appendix/A8_empirical.tex`:166–167 (the events A and W and w_x, written as indicators and W_F), 169–177 (statement), 179–193 (proof). The point-mass formulas (172–175, 183–191) move to the example, part (f).
- **Number.** Proposition A.12 (A.13 in S0).

### Proposition A.13, `prop:announcement` (`D.tex`:292–315)

- **Source.** W5, "Announcement returns and A.14 positivity", eqs. (21)–(22) and the Bayes-plausibility paragraph (part (iii)); "Exact identity with A.14(iv)", eq. (5) (part (iv)). Parts (i) and (ii) are the current ones, at any prior.
- **Scope.** Any equilibrium, any prior, both challenger rules. (iii) The exact condition (some order leaves entry below one) and the sufficient condition B_F(π) < c_H. (iv) The identity in every equilibrium; the posterior after no order equals the prior under full two-sided trade. The value of the weighted impact difference is stated once, in A.10, and A.13(iv) refers to it (`lens_theory.md`, S6 acceptance 4).
- **Manuscript lines.** `appendix/A8_empirical.tex`:195–196 (the event), 198–211 (statement), 213–234 (proof), 235–237 (the example's numbers move to the example, part (g)).
- **Number.** Proposition A.13 (A.14 in S0).

### The example (`D.tex`:316–405)

- **Source.** The example's statements of A8, restated through A.10 to A.13 and Corollary A.3; W5, the margins of the entry-trend section (ℓ² − 3p² = 1/4), the announcement section (the margin c_H − B_r(1/2) on the declared strengths), and the numerical audit; W4, "Numerical reconciliation" (the two covariance terms, the second difference, D − Ω at r_1 and r_2).
- **Scope.** The prior 1/2; the incumbent uniform on [0, r]; point-mass classes at h and ℓ; a slot in the band τ(r_1) < M < τ(r_2) of Corollary 1. Default tie rules: an indifferent investor may mix over its best orders, and an indifferent high-cost challenger prepares; a part that uses another rule names it.
- **Parts.** (a) full two-sided trade on (r_S, h); (b) recruitment and entry; (c) the price gap; (d) identification; (e) purchases only; (f) winners; (g) announcements; (h) two clusters.
- **Manuscript lines.** `appendix/A8_empirical.tex`:3–12 (the example's facts), 14–39 (full two-sided trade on (r_S, h); the rounding remark at 28–30 goes), 79–83, 131–142 (the share of u' = 8/5 stays; the illustrations u' = 1/10 and 0.9 go), 147–149 and 156–163, 172–175 and 183–191, 225–228 and 235–237, 239–249 (two clusters). The closing paragraph on the computations, 251–259, goes.
- **Number.** None.

### Main-text forms (`D.tex`:407–490)

- **Manuscript lines.** `sections/08_empirical.tex`:3–9 (opening), 19–31 (the price gap and its entry component), 33–42 (the informed share), 44–50 (winners), 52–57 (announcements). The paragraphs on entry (11–17), two clusters (59–64) and measurement (66–79) keep their content and take the vocabulary of `NOTATION.md`.
- **Qualifiers carried.** One public state (opening). Full two-sided trade for every test. "While gross profit at the prior falls short of c_H", which is π < τ because B_F rises in the belief with slope γ > 0, for the weighted test, the sale-impact identification of ρΔ_T, the second difference and the discount after no order. The prior and the slot fixed for both strength trends. The prior 1/2 for the second difference. π ≥ 1/2, ρ ≤ 1/2 and the preparing tie rule for the unweighted comparison.
- **For the prose writer.** These are working forms in the order of the current Section 8 paragraphs; every number prints through `\reg`.

## 3. The hypotheses (deliverable 3)

PLAN S4 lists four qualifiers for area D. Each holds in the statements and in the main-text forms.

| Qualifier | Where it is stated |
|---|---|
| Two-sided trade for the tests | A.10(ii)–(vi); A.11 (opening sentence "Let full two-sided trade hold"); A.12(ii)–(v), and (vi) through "the full-trade winner gap"; A.13(iv), second sentence. A.10(i), A.12(i) and A.13(i)–(iii) hold in every equilibrium and say so. Corollary A.3 names the purchases-only pattern. |
| One public state | The standing paragraph ("Every statement concerns one target in one public state, with its prior, slot and incumbent law fixed, and every probability, mean and covariance is taken over the order opportunity of that state"), from W5:121; the main-text opening. |
| A prior below the threshold for the weighted test | A.10(ii) ("If also π < τ"), A.10(iv) and (v) formula; the main-text form ("while gross profit at the prior falls short of c_H"). The same condition is stated for A.11(a)'s ρΔ_T, A.12(iii) and (iv), and the main-text forms of A.12 and A.13. |
| Prior and slot fixed for the winner trend | A.12(v) ("hold the prior and the slot fixed"), A.12(vi) ("at a fixed prior and slot"); the main-text form ("With the prior and the slot fixed"). The same holds for the entry-component trend, A.10(vi) and its main-text sentence. |

The further hypotheses named in W4 and W5, part by part:

| Referee point | Statement |
|---|---|
| W5: a purchases-only equilibrium gives a positive weighted difference without recruitment | A.10(ii) requires full two-sided trade; A.10(i) gives the general formula, whose first term e(0)Δ_T[π − μ(0)] carries that case |
| W5: the hidden economy needs full orders of its own | A.10(iv), the trading margin |
| W5: the tie at τ = π when an indifferent high-cost challenger may prepare with any probability | A.10(iii), last sentence |
| W5: the naive comparison needs the preparing tie rule or the exact inequality | A.10(v) names the preparing rule; the formula gives the exact inequality |
| W5: the sale-impact formula needs entry at its floor after a sale and after no order | A.11(a) adds π < τ; A.11(c) assumes entry ρ after a sale and after no order |
| W5: strict trade incentives are not necessary under the mixing rule | A.11(b), weak inequality under the mixing rule and strict under the abstaining rule |
| W5: ϑ = M − m only at the prior 1/2 | Standing paragraph |
| W5: the entry trend needs a fixed posterior mixture and more than first-order dominance | A.10(vi), prior and slot fixed, (a) and (b) |
| W5: the ceiling jump needs a fixed slot and prior, persistent full orders, continuity, π < τ and an actual crossing | A.10(vi)(d) |
| W5: the announcement mean reveals uncertain preparation, not recruitment | A.13(iii), exact condition |
| W4: strictness of the winner sign needs incumbent mass where the classes differ | A.12(i)–(iii), Pr_F{D(R) > 0} > 0 |
| W4: the second difference needs the prior 1/2, full orders and recruitment by a purchase only | A.12(iv): full two-sided trade, π < τ, the prior 1/2; no claim about its size |
| W4: M − m is constant only with slot and prior fixed | A.12(v) and (vi) |
| W4: the uniform condition is exact, with a right derivative | A.12(vi) |

W4 places the uniform condition in a remark after the proposition. The house rules leave out remark environments, so it is part (vi) of A.12; its content is W4's.

## 4. Keys to add

The example's inputs, all through existing keys: β = 294655/10^6 (`beta_B`), u = e − 1 (`u_B`), so λ = uβ/(1 + uβ), b = β/(1 + uβ), b + λ/2 (`d_slot_B`), M = e/(1 + e) (`M_half_B`); ρ = 1/4, h = 10, ℓ = 1, p = 1/2, c_H = 6, k = 1/50, r_1 = 3, r_2 = 18/5 (the inputs W4's numerical reconciliation lists). At these values w_3(μ) = 11/24 + 2μ/3 and W_{F_3}(μ) = 1/3 + 2μ/3.

| Key | Exact value | Display | Closed form | Printed in |
|---|---|---|---|---|
| `wtest_r1_B` | 0.2579478013681287647781157082705427… | 0.257948 | (1 − ρ)(b + λ/2) w_3(M) = β(11 + 27e)/(64[1 + (e − 1)β]) | example (c) and (g); main-text form of A.13 |
| `margin_reserve_unif_B` | 1/4 | 1/4 | ℓ² − 3p² | example (c) |
| `margin_winsep_r1_B` | 1/3 | 1/3 | D(r_1) − Ω(F_{r_1}) = ℓ/r_1 | example (f) |
| `margin_winsep_r2_B` | 5/18 | 5/18 | D(r_2) − Ω(F_{r_2}) = ℓ/r_2 | example (f) |
| `cov_win_class_r1_B` | 0.0280101474095934331164319624… | 0.028010 | ρλΩ(F_{r_1})/2 = λ/12 = (e − 1)β/(12[1 + (e − 1)β]) | example (f) |
| `cov_win_recruit_r1_B` | 0.2238531834333279308144102718… | 0.223853 | (1 − ρ)(b + λ/2) W_{F_3}(M) = β(1 + 3e)/(8[1 + (e − 1)β]) | example (f) |
| `wsecond_r1_B` | 0.6155292893150024396255796209… | 0.615529 | (1 − ρ) W_{F_3}(M) = 1/4 + M/2 = (1 + 3e)/(4(1 + e)) | example (f) |

How each is computed and compared:

- `wtest_r1_B` is the weighted impact difference E[P(X)] − P(0) at r_1. It equals −`pdrop_neutral_r1_B` (−0.25794780136812876478) exactly as given there, and the value of `p2_access_proceeds_gain` as given there to fifty places; `lens_theory.md` S6 names it as −`pdrop_neutral_r1_B`.
- `cov_win_class_r1_B` + `cov_win_recruit_r1_B` = 0.2518633308429213639308… = `cov_win_r1_B` (0.25186333084292136393). W4's numerical reconciliation gives the two terms as 0.028010147410 and 0.223853183433.
- `wsecond_r1_B` uses A.12(iv) at the prior 1/2: (1 − ρ)χ W(M) with χ = 1 at r_1. W4 gives 0.615529289315.
- `margin_winsep_r1_B` and `margin_winsep_r2_B`: D = 1 on [ℓ, h) and Ω = 1 − ℓ/r; W4 gives D − Ω = 1/3 and 5/18.
- The decimals are the closed forms evaluated to fifty places by a print-only computation; the displays follow the neighbouring keys (six decimals, as `cov_win_r1_B`; fractions typed, as `tau_r1_frac`).

For the S5 proof of example (d), the production assistant adds two keys that the statements do not print:

| Key | Exact value | Display | Closed form |
|---|---|---|---|
| `vol_band_max_frac` | 200/259 | 200/259 | the largest volume at which every ratio u' above `u_lo_frac` = 82/59 meets 3v ≤ 2 + u'(1 − v) |
| `margin_vol_band_B` | 0.0448489229250210762131514601… | 0.044849 | 200/259 − v, with v = β(1 + e)/(1 + (e − 1)β) |

The current proof types 200/259 at A8:120.

## 5. Keys the statements leave unprinted

| Key | Current place | Reason |
|---|---|---|
| `margin_obs_post_over_58_B` | A8:11 | The example states M > τ(r_1) = 141/200 > 5/8, which holds for every slot in the band. |
| `rS_counter_r_B`, `rS_counter_margin_B`, `rS_cert_hi_B` | A8:29–30 | The rounding remark goes (`lens_theory.md` 3.2). |
| `theta09_beta_B`, `theta09_lowsale_r1_B` | A8:116–117 | The share 0.9 illustration goes; part (d) gives the incentive bound through `theta_max_full_eq_r1_B`. |
| `pdrop_neutral_r1_B` | 08:57 | The main-text form prints the positive gap `wtest_r1_B` ("lies ... below"). |
| `u_lo_frac`, `u_hi_frac`, `margin_obs_band_incentive_B` | A8:120–123 | Proof only; they stay with the S5 proof of example (d). |

The statements also print existing keys that the current A8 and Section 8 do not: `cov_win_r1_B`, `cov_win_r2_B`, `d_slot_B`, `margin_res_half_B`, `tau_r1_frac`, `theta_B`, `theta_lo`, `theta_hi`. All are defined in `slot/manuscript/numbers.tex`.

## 6. Notes for the S5 proofs

- **A.13(iii) and (iv) at a general prior.** The current proofs use the prior 1/2: A8:225 bounds some posterior by 1/2, and A8:231 uses m + M = 1. The general proofs use Bayes plausibility, Σ_x f̄(x) B_F(μ(x)) = B_F(π), so some order has B_F(μ(x)) < c_H (W5), and the identity E[P(X)] − P(0) = f̄(1)I_+ − f̄(−1)I_− (W5 eq. (5)).
- **A.10(iii) at τ = π.** An abstaining investor earns zero, so the investors' incentives do not depend on e(0); the high-cost challenger is indifferent at the posterior π = τ. Every e(0) in [ρ, 1] therefore goes with the same full-trade orders. W5's tie subsection gives the instance r = 3, π = 1/2, c_H = B_3(1/2) = 103/24.
- **A.10(iv), forcing.** W5 eq. (7) with the bounds ρκ(π)Δ_T ≤ K_j of Lemma A.3 (A2:189, 222–223); in the hidden economy the same bounds hold with e ≡ ρ.
- **A.10(v), the equivalence.** W5 eqs. (15)–(16): under the preparing rule, ρ ≤ 1/2 gives M − 2ρπ ≥ M − π > 0. In the other rows of the sign table, I_+ ≤ I_− at π ≥ 1/2: with entry (1, 1, 1) or (ρ, ρ, ρ) the difference is a positive multiple of M + m − 2π ≤ 0, and with entry (ρ, 1, 1), I_+ − I_− = Δ_T(M − π) − ρΔ_T(π − m) − (1 − ρ)w_F(π) < 0, because M − π ≤ π − m at π ≥ 1/2 and w_F(π) ≥ Δ_Tπ > Δ_T(π − m).
- **A.10(vi)(b).** W5 eq. (19); it needs only θ ≥ p, which the class ranking gives.
- **A.11(c).** With q = f̄(−1)I_−/(ρΔ_T) = π(1 − π)λ and E[X]² = λ²[1 − 4π(1 − π)], λ is the positive root of λ² − 4qλ − E[X]² = 0.
- **A.12(vi).** Γ(r) = ∫_p^r D is Lipschitz, so Ω(F_r) = Γ(r)/r is absolutely continuous and the almost-everywhere condition on its derivative is exact.
- **Corollary A.3(b).** At λ' = s_+ class H buys surely while indifferent, which the mixing rule allows; at λ' = 1 − 3b, β' = 1/3.
- **Example (d).** The band argument prints 200/259 through `vol_band_max_frac` and keeps `margin_obs_band_incentive_B`.
- **The liquidity probability.** The general results of A.8 use Lemma A.1(a), (b) and (d), Lemma A.2 and Lemma A.3 only, so they hold for every β < 1/2, as A2:232–236 records for Propositions 2 and 3 and Corollary A.2 (S0 numbers). The bound β ≤ 1/3 enters A.11(b) and Corollary A.3(b) only as the definition of a slot. The O2 notes list "Proposition A.11, parts (a) and (c)" (the current parts); in the restated proposition the place is A.11(b), with Corollary A.3(b).
- **Left out.** The uninformative-order extension of the weighted test (W5, recommendation 1); the odds and relative-risk trends (W4, recommendation 4); the marginal-spread identity and the ratio Ω/Δ_T (W4, recommendation 5); the hump of the winner gap, which W4 shows is not general; the unknown-prior identified set (decision 5). The weighted winner difference f̄(1)[y_1 − y_0] − f̄(−1)[y_0 − y_{−1}] = f̄(1)[e(1) − ρ]W_F(M) under full two-sided trade with π < τ is my own observation; no referee report covers it, so it stays out.

## 7. Changes after the referee

The referee's report is `D_referee.md`. All four issues are applied as written or in a close variant; no computation changed, and the seven printed keys keep their values.

- **D1 (blocker), Corollary A.3(b).** The identification sentence now reads: "The counts therefore identify \(b\) and, at a known prior, \(s_+\); even with the prices, they do not identify \(\lambda\)." The whole-segment equivalence is unchanged, and the example's part (e) only states the value of \(s_+\) on its interval.
- **D2 (should fix), opening of the main text.** "at every prior" is gone. The sentence now says that each prediction holds for every continuous incumbent law, names the incumbent, prior, trading-pattern and tie-rule conditions it needs, and concerns one target in one public state.
- **D3 (minor), informed-share paragraph.** "Prices separate the slots that counts leave together" is removed as a categorical opening. The sentence with the entry-floor and known-scale conditions now ends "prices then separate slots that have the same counts", and the example's alternative slot follows as "In the example, a slot with share ...". The purchases-only sentence is unchanged.
- **D4 (should fix), winner paragraph.** "When no order recruits" is replaced by "When gross profit at the top posterior falls short of \(c_H\), entry is \(\rho\) after every order, the covariance of the order with entry is zero, and its covariance with a challenger win is ...". The paragraph's preceding "Under full two-sided trade" and the fixed prior keep the condition \(B_F(M)<c_H\) with \(\pi<\tau\), which \(B_F(M)<c_H\) implies.

Build: `D.tex` rebuilt in two passes into the private build folder; nine pages, no undefined references, no overfull boxes. The language scan reports the one accepted interval expression and the permitted tie-rule phrases.
