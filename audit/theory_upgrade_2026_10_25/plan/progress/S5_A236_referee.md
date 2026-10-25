# S5 A236: referee report on foundations, ownership and robustness

The referee read the package `slot/manuscript/appendix/A2_beliefs_trading.tex`, `A3_proposition2.tex` and `A6_robustness.tex`, the mathematics writer's report `S5_A236.md`, the frozen statements `statements/A.tex` with `A_notes.md` and `A_referee.md`, the proofs `O2`, `O6` and `O7`, and the plan and notation card. The coordinator committed the package as `09e88cc` while this review was under way. The files reviewed are identical to the committed ones, so every `file:line` below refers to `09e88cc`, and "removed text" means the difference from `a7fb483`.

## Verdict

Every frozen statement is transcribed intact. Every proof is correct under its stated hypotheses, with five one-line gaps (R-04 to R-08). One displayed identity that the package introduces is false: `A6_robustness.tex:42` writes \(\tau(\ell)=c_H/(h-\ell)\), which equals 2/3 in the example, while \(\tau(\ell)=5/8\). The conclusion \(\tau(\ell)>\pi\) survives, but the equation must be fixed before transplant (R-01). Two further items change what a reader computes and should be fixed: the description of the bound 19/795 (R-02), and printed products such as "119/96b" and "m0.713542" (R-03). Everything else is minor. No result, proof or needed fact that the plan keeps was dropped. No process text remains in the three files.

## Per-result table

Fidelity was checked by a whitespace-normalized comparison of each frozen block in `statements/A.tex` (at `09e88cc`, which carries the three single names `cH_DA_floor_B`, `cH_afford_ceiling_B` and `margin_unif_afford_B` that `A_notes.md` prescribes) with the package text.

| File | Result | Fidelity | Proof | Issues |
|---|---|---|---|---|
| A2 | Beliefs, prices and trading (`par:a2-scope`) | intact | no proof needed | |
| A2 | Lemma A.1, order probabilities and beliefs | not frozen; part (c) narrowed to \(\beta\le1/3\), as O2 requires | accept | R-09 |
| A2 | Corollary A.1, high-cost preparation under every profile | not frozen; hypothesis \(0<\beta\le1/3\) added, as O2 requires | accept | |
| A2 | Lemma A.2, entry and prices | unchanged apart from the tie phrases | accept | |
| A2 | Constructed tuples (`par:constructed-tuples`) | intact | accept (the proof of O7) | R-08 |
| A2 | Lemma A.3, informed trading | unchanged apart from the tie phrases | accept | |
| A2 | Lemma A.4, the auction through the spread and the threshold | intact | accept | |
| A2 | Lemma A.5, the two numbers along a path | intact | accept, with a gap in the last sentence | R-06 |
| A2 | The liquidity share (`par:beta-scope`) | intact | no proof needed | |
| A2 | A price reached by a nonzero order | identical to `O2_proof.tex` | accept | |
| A3 | Proposition 2, full statement (`prop:ccc-app`), with (A.7) `eq:a3-share` | intact | accept, with a gap at Step 5 | R-04, R-20 |
| A3 | Lemma A.6, decisive advantage | intact | accept | |
| A3 | Corollary 1, full statement (`prop:region`, `cor:ccc-example`) | intact | accept, with a gap in part (a) | R-05, R-16, R-17 |
| A3 | The example (the counterexample with \(c_H=47/10\)), the tuples, the recruitment region | not frozen | accept | R-18, R-21 |
| A6 | Proposition A.2, fixed information | not frozen; tie phrase | accept | |
| A6 | The control in the slot | not frozen | wrong (false identity; conclusion survives) | R-01, R-17 |
| A6 | Proposition A.3, preparation cost laws | not frozen; symbols \(\Phi,\Phi^0,\Phi^1,\bar c_0\); Steps 1 and 2 are `O2_cost_floor.tex` verbatim | accept | |
| A6 | Value classes and priors (`par:uniform-classes-scope`) | intact | no proof needed | R-19 |
| A6 | Proposition A.4, value classes and priors | unchanged apart from \(\theta_*\) | accept | R-11, R-15 |
| A6 | Proposition A.5, many classes under separation | statement unchanged; proof uses the nonzero-order bounds only | accept | |
| A6 | The four-class economy; a price collision at three classes | not frozen | accept | R-12 |
| A6 | Proposition A.6, complementary private signals, with (A.14) `eq:a6-DP` | intact | accept, with a gap in its last sentence | R-07 |
| A6 | A slot with a more accurate challenger signal; the signal example; the example; the example with the signal example's accuracies | not frozen | accept, except the items listed | R-02, R-03, R-13, R-14 |

## Proof notes

- **Lemma A.4.** The forward direction uses Lemma A.2 for the price posterior, \(B(\mu)-c_H=\gamma(\mu-\tau)\) for the threshold rule including the selected action at equality, and Lemma A.3 for the payoffs, from which \(t_0\) and \(w_L\) cancel. The converse builds the tuple from the constructed-tuples paragraph; under the second challenger rule, orders at \(\tau\) with different entry get different prices, so every reduced solution is realized. The research part is correct: the deviation payoff \(\tilde\lambda\Psi-(a/2)\tilde\lambda^2\) is strictly concave on \([0,\lb]\), and \(\Psi\ge0\) because abstention pays zero.
- **Lemma A.5.** The auction integrals \(g_j(F)=\int_p^\infty F(1-G_j)\), the threshold increment (from \(\tau\gamma=c_H-g_L\) and \(\gamma(r')=\gamma(r)-[\DT(r')-\DT(r)]\)), the product increment and the formula for \(J'\) all check by direct algebra. The translated uniform economy has every incumbent value in \([6.9,7.6]\), strictly between \(\ell\) and \(h\).
- **Proposition 2, Step 4.** The cross-multiplication criterion is exact; the denominators are positive because (H1) gives some \(W_j(F_1)>0\) and dominance gives \(W_j(F_0)\ge W_j(F_1)\). Under outbidding the share is nondecreasing, strictly exactly when \(W_L(F_0)>0\).
- **Lemma A.6.** For \(r>h\), \(g_H(U[0,r])=(h^2-p^2)/(2r)\) has supremum \((h^2-p^2)/(2h)\), not attained, so the weak inequality is exact.
- **Corollary 1(e).** On \([p,h]\), \(g_H(r)=h-r/2-p^2/(2r)\) falls strictly; the roots of \(r^2-2(h-c_H)r+p^2=0\) have product \(p^2\), so the lower root lies below \(p\); for \(r\le p\), \(g_H=h-p>c_H\). The upper root is the unique crossing.
- **Proposition A.3.** Step 1 needs only the price-preimage bound, so the proposition holds for every \(0<\beta<1/2\). At \(F_0\), abstention is forced for any entry in \([0,1]\); at \(F_1\), the floor at the nonzero orders forces full orders, after which every price belief averages \((m,\pi,M)\) and the low component prepares everywhere.
- **Proposition A.6.** The payoffs \(U_+(1)=(2\alpha_I-1)[1-\nu_I(1)]\Delta_P-k\) and \(U_-(-1)=(2\alpha_I-1)\nu_I(-1)\Delta_P-k\) follow from \(\mu=(1-\alpha_I)+(2\alpha_I-1)\nu_I\); the bounds \(\rho\DT\le\Delta_P\le\bar\Delta_P\) follow from \(e_H-e_L=(1-\rho)(2\alpha_C-1)(\zeta_+-\zeta_-)\); the class order laws \(f_H,f_L\) and the one-pair averages are right.

## Issues

### Blocker

**R-01. False identity in the control paragraph.** `A6_robustness.tex:42`. The text reads "\(\tau(\ell)=c_H/(h-\ell)>\pi\)". This ignores \(g_L(\ell)=(\ell^2-p^2)/(2\ell)\). In the example it gives 2/3, while the stated \(\tau(r)\) at \(r=\ell\) gives \(11.25/18=5/8\) (the old text had \(\tau(1)=5/8\)). The conclusion \(\tau(\ell)>\pi\) holds either way. Fix: write \(\tau(\ell)=[2\ell c_H-(\ell^2-p^2)]/[2\ell(h-\ell)]>\pi\). If the value is printed, add a row for 5/8; no existing row holds \(\tau(\ell)\).

### Should fix

**R-02. The bound 19/795 is described wrongly, and "the threshold" remains.** `A6_robustness.tex:587-589`. "The sale earns at least the return at the public belief that makes a challenger with \(S_C=+\) indifferent, 19/795." At that belief the return with \(S_C=+\) preparing is \(2603/25440\approx0.102\); 19/795 is the return there with entry \(\rho\) after the sale, which is the lower bound used, because \(\nu_I(-1)\ge19/53\) and \(\Delta_P\ge\rho\DT(r_1)\) on that range. The same sentence ends "no tie mixture exists at the threshold", which `NOTATION.md` (part (b), A6:540-541) asks to write as the public belief. Fix: "On that range the public belief after a sale is at least \(\reg{a236_sig_public_cutoff}\), and \(\Delta_P\ge\rho\DT(r_1)\), so the sale earns at least the return at that belief with entry \(\rho\), \(\reg{a236_sig_sale_floor}\), …; so no equilibrium has …, and no tie mixture exists at the public belief \(\reg{a236_sig_public_cutoff}\)."

**R-03. Printed products that parse wrongly.** `A6_robustness.tex:581`, `586`, `587`, `589`, `591`, `604`. `\reg{a236_sig_rate0}b` prints "119/96b", which reads as \(119/(96b)\); the same holds for "15/19b" (587, 589) and "4/3b" (591, 604). At 586, `m\reg{a236_sig_DP1}` prints "m0.713542". The old text had \(119b/96\), \(15b/19\) and \(4b/3\). Fix: write `\reg{...}\cdot b` or put \(b\) first, and at 586 write \((2\alpha_I-1)\,m\,\Delta_P-k\), since \(\Delta_P\) is named just before.

### Minor: gaps in proofs

**R-04. Step 5 omits the ownership conclusion.** `A3_proposition2.tex:148-165`, statement at `A3:47`. Part (iii) states "High-class ownership is \(\pi\rho W_H(F_2)\)", but Step 5 stops at the tuple. Fix: add "Entry is \(\rho\) after every order, so, as in Step 4, high-class ownership is \(\pi\rho W_H(F_2)\)."

**R-05. Corollary 1(a): entry and ownership are not derived in part (a).** `A3_proposition2.tex:313-319`, statement at `A3:268-270`. The proof of part (a) establishes the band only; \(W_H=1\) at the three strengths first appears in part (d). Fix: end part (a) with "Proposition 2(i)-(iii) then give the entry values under all four tie rules, and since \(h>r_2\), \(W_H=1\) at the three strengths, which gives the ownership values."

**R-06. Lemma A.5: one step from Proposition 3(c) to "\(J\) rises".** `A2_beliefs_trading.tex:353-354`, `381-382`. The uniform case of Proposition 3(c) gives that \(\DT(g_H-c_H)\) does not fall. \(J\) rises because \(J=\DT(g_H-c_H)/\gamma\), \(\gamma=\bar\Gamma-\DT\) falls strictly where \(\DT\) rises, and \(g_H>c_H\) under affordability. Fix: add this sentence to the proof.

**R-07. Proposition A.6: the appeal to Lemma A.6.** `A6_robustness.tex:517-519`. Lemma A.6 is stated for the base model, where the recruited challenger's belief is a price posterior. Here it is the private belief \(\mu^C_+(M^I)\). Fix: "Recruitment at \(F_1\) gives \(c_H<B_{F_1}(\mu^C_+(M^I))<g_H(F_1)\), because \(\mu^C_+(M^I)<1\) and \(g_H(F_1)>g_L(F_1)\); decisive advantage at \(F_1\) then gives \(W_H(F_1)=1\), as in Lemma A.6."

**R-08. The constructed-tuples proof cites Lemma A.2(d).** `A2_beliefs_trading.tex:184`. Lemma A.2 assumes a candidate, which a constructed profile is not yet. Fix: "Under the first challenger rule, threshold-consistent entry is \(\rho\) below \(\tau\) and one at and above \(\tau\), a function of the posterior."

### Minor: wording, vocabulary, keys and layout

**R-09. Lemma A.1(c) conditions an unconditional fact.** `A2_beliefs_trading.tex:42`. "If \(\beta\le1/3\), then \(b_0\le f_j(0)\le b_0+\lambda\) and \(b_0\ge b\)": only \(b_0\ge b\) needs the bound. Fix: "\(b_0\le f_j(0)\le b_0+\lambda\). If \(\beta\le1/3\), then \(b_0\ge b\), hence \(m(\pi)\le\mu(0)\le M(\pi)\)."

**R-10. Conventions.** `A2_beliefs_trading.tex:16-21`. The third bullet repeats the second, and the old clause that a check of a condition cites no lemma whose premises include that condition was dropped; it is a mathematical rule, not process text. Fix: merge the two deviation bullets, and write "A constructed tuple satisfies each equilibrium condition by direct substitution, and its proof cites no lemma whose premises include the condition at issue."

**R-11. Vocabulary and a typo in A6.** `A6_robustness.tex:262` "trade margins" → "trading margins" (`NOTATION.md`, part (b)); `A6:567` "satisfy the theorem" → "satisfy the proposition"; `A6:197-198` "On this set, The tuples" → "On this set, the tuples". The source comment `A2_beliefs_trading.tex:106` still names "rule-CM"; write "its arbitrary-preparation clause".

**R-12. Keys that print the wrong quantity.** `A6_robustness.tex:361` prints the bound \(\beta>1/4\) (from \(4\beta-1>0\)) through `a236_pool_pi1`, the prior of class 1; `A6:544` prints \(\alpha_C=1/2\) through `prim_pi`, the example's prior. The values agree by coincidence. Fix: "Since \(4\beta>1\)", and "with an uninformative challenger signal (\(\alpha_C=1/2\))", with 1/2 typed as a constant as in \(m(1/2)\) and "prior one half"; or give each its own row.

**R-13. Two keys duplicate existing rows.** `A6_robustness.tex:530`, `532`. `a236_sig_alt_private` (21/400) and `a236_sig_alt_weak` (2/1375) do not depend on the slot and equal `margin_p4_signal_s_private` and `margin_p4_signal_s_weak`, as the production assistant's `S6_numbers.md` records. Fix: cite the existing rows; retire the two duplicates at S8.

**R-14. The signal example is introduced after it is used.** `A6_robustness.tex:522-527`, `539-544`. The signal example's primitives appear only in the alternative-slot paragraph, which precedes "The signal example", and "Then \((\alpha_I,\alpha_C)=\dots\)" presents primitives as consequences of the slot. Fix: begin "The signal example" with its primitives \((h,\ell,p,r_0,r_1,\rho,c_H,k,\alpha_I,\alpha_C)\) and slot; then "A slot with a more accurate challenger signal: keep the signal example's primitives and set \((\lambda,\beta)=\dots\); then \(M=\dots\) and \(m=\dots\)."

**R-15. Margins that depend on \(\eu\).** `A6_robustness.tex:253-254`. "Exact integration gives (H1)-(H2) …": at the slot \(1+u=\eu\), the signs of the margins also need bounds on \(\eu\). Fix: "Exact integration, with rational bounds on \(\eu\), gives …".

**R-16. The equivalences in Corollary 1(a) and (c) lost their middle step.** `A3_proposition2.tex:315`, `337-338`. With the typed fractions removed, "that is \(u>\reg{u_lo_frac}\)" cannot be checked in place. Fix: give the symbolic forms: \(M>\tau\iff u>(2\tau-1)/(1-\tau)\); \(\rho(1-M)\DT(r_1)>k\iff u<\rho\DT(r_1)/k-2\); \(m(\pi)>\kappa_0\iff\pi>\kappa_0\eu/(1-\kappa_0+\kappa_0\eu)\) with \(\kappa_0=k/[\rho\DT(r_1)]\).

**R-17. The range of the closed form of \(\tau(r)\).** `A3_proposition2.tex:309`, `A6_robustness.tex:42`. The formula \([2rc_H-(\ell^2-p^2)]/(2rh-r^2-\ell^2)\) holds for \(\ell\le r\le h\). Fix: state the range once.

**R-18. The point of the counterexample is blurred.** `A3_proposition2.tex:231`. "The inequality \(B_1(\pi)<c_H\) permits certain preparation against the weaker incumbent" does not say what the paragraph shows: that the left side of (H1) must hold at the weaker incumbent. Fix: "Proposition 2 needs \(B_0(\pi)<c_H\) in (H1); with \(B_1(\pi)<c_H\) in its place, both cost types can prepare against the weaker incumbent:".

**R-19. Layout.** `A2_beliefs_trading.tex:187` and `401`: a blank line before `\end{proof}` puts the end mark on its own line (pages 45 and 50). `A6_robustness.tex:154-162`: a subsection heading, a paragraph heading and a proposition title all read "Value classes and priors"; drop the paragraph heading or retitle it "Scope". Pages 54 and 106 end half empty before a paragraph heading; this is for the S12 layout pass.

**R-20. Proposition 2 is printed in full twice after S9, and `eq:a3-share` must exist once.** `A3_proposition2.tex:15-51`, label at `A3:40`. The resolution of A-02 in `A_notes.md` places the full statement in Section 4.1. The A3 restatement carries `\label{eq:a3-share}`; if the Section 4.1 statement also carries it, the label is defined twice. This is the coordinator's decision. Recommendation: one full statement, in Section 4.1, with the label; A3 opens with the proof and cites (A.7) by label. If the A3 copy stays, the main-text statement must not repeat the label.

**R-21. Example sentences in the general part.** `A3_proposition2.tex:225-227`. "Corollary 1 gives its section through the example" and "In the example, \(b+\lambda=\dots\)" stand before the heading "The example". Fix: move them under that heading, as the plan's general-first order asks.

## Removed text

Against `a7fb483`, the package removes, in addition to process text:
- A2: the opening sentence (narrowed to the belief lemma, as S5 asks), the paragraph "Where \(\beta\le1/3\) enters" (its content is in the frozen liquidity paragraph and the price-preimage claim), the convention on script paths, and the old constructed-tuples paragraph, which claimed equal prices at equal posteriors (repaired as the plan asks).
- A3: the explicit inequalities in the proof of the corollary (R-16), "The model adds the structural bound \(\beta\le1/3\)" (consistent with O2), and the sentence on the weaker condition \(B_1(\pi)<c_H\) (R-18). Every result and price of the old Proposition A.1 is in Corollary 1 and its proof.
- A6: the motivating sentence for complementary signals, which stands in `sections/06_robustness.tex:59`; the paragraphs "Beliefs, entry and prices", "Order payoffs" and "One pair that recruits", which stand inside Proposition A.6 and its proof; "No step uses atomlessness or a density", which the remaining text still implies.

None of these drops a result, proof or needed fact that the plan keeps. The equilibrium counterexample at \(\beta>1/3\) in `O2_proof.tex` is not placed; the plan does not require it, and the proof of Lemma A.1(c) shows out of equilibrium that the zero-order bound fails.

## Process text and language

No line of the three files names a file, log, program, key, computation record, or the example's internal label; the retired names of the example, `\nolinkurl` and the tie codes are absent from the printed text. The prescribed language scan of the three files counts zero findings, with eleven allowed tie phrases (A2 seven, A3 two, A6 two). The vocabulary leftovers are R-02, R-11 and R-19. Rule 4: the example and the signal example are named as `NOTATION.md` prescribes.

## What the referee recomputed

All by print-only computations in the referee's private folder at 40 digits. Auction quantities were obtained by numerical quadrature of the second-price auction with reserve over the incumbent's law, not from the closed forms.
- **A2.** Translated uniform economy: \(\DT=6\), \(g_H=3\), \(\tau=2/3\), \(J=2\) at \(r=7\); \(\DT=13/2\), \(g_H=5/2\), \(\tau=4/5\), \(J=13/10\) at \(r=15/2\); \(g_L=0\) at both.
- **A3.** Spreads \(1/60\), \(2/3\), \(169/180\); thresholds \(195/308\), \(141/200\), \(4245/5804\); \(\tau(\ell)=5/8\) (against \(c_H/(h-\ell)=2/3\), R-01); slot band \(82/59<u<2686/1559\), \(u<19/3\); \(k/[\rho\DT(r_1)]=3/25\) and \(\DT(r_0)/[\rho\DT(r_1)]=1/10\); prior endpoints 0.467850029686 and 0.500424307320; windows \((0.270432,0.729568)\) and \((0.231969,0.768031)\); at the example slot \(b+\lambda=0.531737\), entry at \(r_1\) 0.522756943478, ownership 0.324401303411; takeover shares 0.545454545454545, 0.830690945230374, 0.782608695652174 with \(W_L=\ell/r\); cost window \(399/80\), \(32/5\), margins \(81/80\), \(2/5\); the root of \(g_H(U[0,r])=6\) by bisection on the quadrature, 7.96862696659689, equal to \(4+\sqrt{63}/2\); \(g_H\) just above \(r=h\) is 4.98749999950.
- **A6, the price collision.** \(t_0=7/8\), \(t_1=1\), \(t_3=65/16\), \(g_3=95/16<10\); \(t_0=p(1-p/r)\) and \(t_3=r/2+p^2/(2r)\); \(2b+b_0+\lambda=1\); \(\psi=0.940709\) and \(1-\psi=(1-\lambda)(4\beta-1)/2\); \(\bar t(0)=\bar t(1)=0.804384959820\) from both the posterior vectors and the displayed closed forms; posterior vectors, both prices and the three choice margins as printed.
- **A6, the signal economies, in exact rationals.** The alternative slot: \(M=8/11\), \(m=3/11\), \(M^I=13/22\), \(\mu^C_\pm(M^I)=13/16,13/40\), and the five margins \(21/400\), \(1363/36800\), \(2/1375\), \(603/31625\), \(76753/18400\). The example with the signal example's accuracies: \(e_H=13/16\), \(e_L=7/16\), \(\Delta_P=311/1920\) at \(r_0\) and \(137/192\) at \(r_1\), the rate \(119b/96\), the cutoffs \(47/106\) and \(15b/19\), the floor return \(19/795\) (exceeding \(k\) by \(31/7950\)), the rate \(4b/3\) with \(\mu(-1)=21/50\), and entry \(5/8-23b/40\) and ownership \(13/32-63b/160\) at \(r_1\).
- **The 32 pending names of `S5_A236.md`.** Each listed exact value equals the value in the A2, A3 and A6 text at `a7fb483` (all 29 A6 values stand there verbatim or as the same fraction) and equals the referee's recomputation above. The production assistant's rows in `09e88cc` hold the same exact values.

## Build and pages read

The manuscript builds from `slot/manuscript/main.tex` into the referee's private folder: 136 pages, no errors, no unknown numerical names (the rows of `09e88cc` define all 32), no multiply defined labels. The only warnings are four undefined references to `cor:example-coexistence` on pages 128-131 and one overfull box of 3.86 points in A4, both outside this package. The referee read the extracted text and the page images of pages 41-58 (A2 on 42-50, A3 on 50-58) and 94-107 (A6 on 95-107). Equations, statement numbers, the named Proposition 2 and Corollary 1, Table A.4 and every proof end are within the page area. No build product is in the repository.

## Integration notes

These belong to later stages, not to this package.
- Citations of `prop:region` that still print "Proposition 1": `sections/04_equilibrium_results.tex:121,151,185,259,274` (S9) and `appendix/A9_parameters.tex:96,265` (S8).
- "Proposition 3(c)" in Lemma A.5 and Corollary 1(e) resolves to the old Proposition 3 until S9 places the frozen statement.
- `appendix/A7_welfare.tex` (5) and `A9_parameters.tex` (10) still carry script paths whose anchoring convention A2 removed; S8 removes them.
- The production assistant's rows print \(\Delta_P\) at \(r_0\) and \(r_1\), \(e_H\), \(e_L\) and the perturbation as decimals (0.161979, 0.713542, 0.812500, 0.437500, 0.001). The rates \(119/96\) and \(4/3\) follow exactly from 311/1920 and 137/192; fraction displays would let the reader follow the arithmetic.
