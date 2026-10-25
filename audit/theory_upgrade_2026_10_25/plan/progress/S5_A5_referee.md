# S5: referee report on the A.5 research package

Report of the referee to the coordinator, 25 October 2026. Under review: `slot/manuscript/appendix/A5_research.tex` (1166 lines, uncommitted) and the mathematics writer's report `plan/progress/S5_A5.md`. The referee wrote neither. Sources read in full: `plan/PLAN.md` (Parts 2, 4 (S4, S5), 5, 6), `plan/NOTATION.md`, `statements/C.tex` with `C_notes.md` and `C_referee.md`, `statements/O1/`, `O3/`, `O4/`, `O8/`, `referee/W3.md`, the ownership sections of `referee/W2.md`, the version of A.5 at `HEAD` (439 lines), and the external lemmas A.5 cites in the current A.2, A.3 and A.4. The package was not edited. The build, the renders and the referee's computation ran in a private folder outside the repository.

## 1. Verdict

**Accept with listed fixes.** Every frozen statement is transcribed intact from `C.tex`, down to the hypotheses, qualifiers and equation labels. Every proof is complete and correct under exactly its stated hypotheses; none is marked "gap" or "wrong". Every number a proof uses reproduces in the referee's independent computation (Section 5). Nothing the plan keeps was dropped. No line names a file, log, program, key, run, status or the example's retired label; the language scan counts zero hits. The fixes are an undefined symbol with an underived identity in the example proofs, a duplicated paragraph, and wording. There is no blocker.

## 2. Per-result table

Columns: (1) statement fidelity against `C.tex`; (2) proof; (3) removed text, against the version at `HEAD`; (4) process text; (5) language rules 1 to 4 and the vocabulary of `NOTATION.md`. "Intact" in column (1) is the output of a normalised text comparison of each statement body with its frozen source, confirmed by reading.

| Result (printed number; pages) | (1) Fidelity | (2) Proof | (3) Removed text | (4) Process text | (5) Language |
|---|---|---|---|---|---|
| Opening paragraph and Setting (71–72) | Setting intact | not a result; the (E7) paragraph is the former text with the research value renamed | the "standing assumptions" (the example, β ≤ 1/3) and "derived functions" paragraphs are replaced by the general setting; the definition of \(u_\lambda\) left with them, see A5-01 | none | pass |
| Lemma A.12, joint deviations (72) | intact | accept: concave quadratic at fixed prices and preparation; strict concavity excludes mixtures | none | none | pass |
| Lemma A.13, bounds under every profile (72–73) | intact | accept: (a) nonzero-order likelihoods in \([\hat b,\hat b+\hat\lambda]\) give \([m,M]\); the zero-order bound needs \(\hat b_0\ge\hat b\), that is β ≤ 1/3; (b) equal prices give equal preparation probability, hence equal entry, hence equal posteriors since \(e\ge\rho>0\), \(\DT>0\); (c), (d) direct | the former proof cited the belief lemma; the new proof is self-contained | none | pass |
| Lemma A.14, strict full purchase (73) | intact | accept: a profitable sale forces \(U_H(1)\ge\rho\DT m-k>0\); strict, so no investor rule; entry ρ after nonpurchase orders from the price lemma at τ > 1/2 | none | none | pass |
| Lemma A.15, the low class's sale (74) | intact | accept: likelihoods, posteriors, the strictly decreasing sale payoff, both boundary choices and the positive-part payoff are all derived in the proof; the citation of the A.4 low-class lemma is a convenience, see remark R1 | new lemma | none | pass |
| Proposition 4, full statement (74–80) | intact (the appendix carries the anchor `prop:research-full` with fixed value 4; the main text owns `prop:research`) | accept. (a) root existence and uniqueness, the strict purchase at the cap, the price ordering with \(t_L\ge t_0\), pooled nonpurchase prices; (b) the share derivative \((1-\rho)[\rho+(1-\rho)\beta]/(e_H+e_L)^2\) recomputed; slopes, the kink at \((1-\rho)k/(2a\rho)\) and the slope jump \(2a\rho m/[\cdots]\) recomputed; cap spread; (c) \(g_H>c_H>0\) gives \(W_H>0\); (d) the O3 and O4 proofs as accepted, with fixes C-02, C-04 and C-05 applied | the former Proposition 4(a) (implicit-function proof of \(\lambda_R'>0\)) is contained in (b); the former "branch at calibration B" steps 1 to 4 are contained in (d) and in the Corollary 3 proof | none | pass |
| The research margin, paragraph (80) | not frozen | accept (C-04 wording in place) | new | none | pass |
| Ownership at the same incumbent (80) | intact | accept; the cited fact (zero-research ownership \(\rho W_H/2\)) is in the proof of Lemma A.16(a), not its statement, see A5-06 | new | none | pass |
| Lemma A.16, the three research outcomes (80–82) | intact | accept: the O8 proof, plus the floor-root existence paragraph (gap falls from \(\rho\DT/2-k\ge0\) to \(-k-a\)); the residual \((1-\rho)\DT m_{\lambda_Q}\) at the floor root, the clipped ordering, the empty band when both roots reach the cap, and existence including τ ≥ 1 all check | replaces the former middle-strength lemma, as the plan directs; its abstaining-branch item (cap before selling) is dropped, as the plan directs | none | pass |
| Lemma A.17, strong incumbents (83) | intact | accept: the former proof read with nonzero-order bounds only, so β < 1/2 suffices; the tie at the cap posterior is removed by \(M_{\lb}\ne\tau\) | none | none | pass |
| Access to prices with research (83–84) | intact | accept: the allocation identity \(\max\{\theta,R\}-R\1\{R\ge p\}=(\theta-\max\{p,R\})_++p\1\{R<p\}\) checks case by case; both gains positive from \(M_{\lb}>\tau\), γ > 0, \(t_L\ge t_0\) | the example's two values move to the Corollary 3 proof | none | pass |
| Remark A.1, tie rules with research (84–85) | intact | accept: interior entry \(e^*\) from the research equality; the cap family from the research inequality intersected with \([\rho,1]\); the abstention survival condition, including exclusion of full selling at zero sale profit | the former remark's content is contained here and in the example continuation | none | pass |
| Primitives and strengths (85–86) | intact | not a result; the polynomial paragraph that follows is the former text, with the sale-term remark justified by \((1-\rho)k/(2a\rho)>1\) | none | none | pass |
| Corollary 3, full statement (86–88) | intact (fixed value 3 through `cor:research`, see A5-07) | accept: the cap segment from Proposition 4(d) with \(\tau'>0\); the margin bounds on \([r_0,7/4]\) (recomputed, Section 5); the tail \(\varphi_a\ge J(7/4)-k-2a\lambda_E(r_2)>0\) completes uniqueness of \(r_R\) on the whole path (C-06); parts (a) and (b) assemble Lemmas A.16, A.17, A.18 correctly; the weak-incumbent and intermediate-strength arguments are the former ones with the closed-form root | the former (b)(i) aside about a smaller \(c_H\) is dropped; it was a comment outside the hypotheses, not a result | none | pass |
| Floor-entry research, definitions (88–89) | not frozen | accept; lines 863–870 repeat lines 516–523 verbatim, see A5-02 | new | none | pass |
| Lemma A.18, floor-entry research along the path (89–92) | intact | accept: the O1 proof as accepted, with fixes 1 to 5 of its referee applied; Steps 0 to 6 reread; the 24-piece bound and the zero recomputed (Section 5) | new | none | pass; \(\tau(r_2)=\reg{tau_r2}\) prints an equality with a rounded value, see A5-04 |
| Proposition A.1, the research cap and cost (92–94) | intact | accept: the former proof under the three-outcome classification; necessity bullets right; the β endpoint 1/3 and \(\beta_{\rm lo}\) recomputed; \(\partial\lambda_E/\partial\beta\) recomputed; \(a_{\rm mono}(\beta)\) falls on \((0,1/3]\) because \(\lambda_E'(\tau;\beta)\) rises in β exactly for β < 19/17. Two wording points, A5-01 (the symbol \(u_{\lb}\)) and A5-05 | the closing aside "strict growth of entry alone holds on a wider set" is dropped; it was an aside, not a result | none | pass |
| Remark A.1, the example (94–95) | intact | accept: \(e^*\) and the three entries recomputed; the whole cap family at \(r_C\) from condition (U); the abstention gap \((r_N,r_S]\subset(r_N,r_Q)\) with \(r_S<r_Q\) checked; the pair at \(r=2\) has both trades strict | the former remark proof's content is contained here | none | pass |

Removed text that the plan directs: the certificates paragraph with its program, log and enclosure names (former lines 423–439); the status and method sentences; "calibration B" and "the benchmark" throughout; the abstaining-branch result. Removed text that the plan keeps: none found. Every fact the former proofs used is either restated as mathematics or replaced by a general lemma.

## 3. Issues

Severity: "blocker" (the package cannot be transplanted), "should fix" (the mathematics writer changes the text before S8), "minor" (wording or integration, fixable at S8).

| Id | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| A5-01 | should fix | `A5_research.tex:1114`; also 766–767, 927 | "Then \(u_{\lb}=u\) for every β" uses \(u_\lambda\), which the former "derived functions" paragraph defined and nothing in the manuscript now defines (the main text defines only \(u\)). The identity \(m_{\lb}=1/(1+\eu)\), used at 766–767 ("hence the cap spread is \((2a\lb+k)(1+\eu)\)"), 927 and 1114, is asserted but never derived. | Add one sentence in the Corollary 3 proof before line 766: "Substituting \(\lb=u\beta/(1+u\beta)\) in \(m_\lambda\) gives \(m_{\lb}=1/(2+u)=1/(1+\eu)\) and \(M_{\lb}=\eu/(1+\eu)\)." At 1114 write "Then \(m_{\lb}=1/(2+u)=1/(1+\eu)\) for every β, so …". |
| A5-02 | should fix | `A5_research.tex:863–870` against 516–523 | The floor-root existence paragraph appears twice, word for word: inside the proof of Lemma A.16 and again at the head of the example's floor-entry definitions. | Delete lines 863–870 and open the paragraph at 872 with "For \(\rho\DT(r)>2k\), with \(\lambda_Q\) the root of \eqref{eq:a5-floor}, floor-entry research is the tuple …". |
| A5-03 | minor | `A5_research.tex:879` | The capped sale rate \(\hat s_-(r)\) is attributed to the A.4 low-class lemma, while Lemma A.15 is the appendix's own general source for the same rate (issue C-09 asked for one source). | "where \(\hat s_-(r)\) is the sale rate of Lemma~\ref{lem:a5-sale} at the presence \(\lb\)". |
| A5-04 | minor | `A5_research.tex:922, 763–764, 828, 855, 925–926, 1009` | Equalities with rounded displays: \(\tau(r_2)=\reg{tau_r2}\) (922; the exact key `tau_r2_frac` exists), \(M_{\lb}-\tau(r_1)=\reg{margin_res_tau_r1_B}\) (763–764, 925–926), \(c_H-B_{r_0}(1/2)=\reg{margin_res_half_B}\) (828; exact 287/240), entry "\(=\reg{res_entry_cap}\)" (1009), and "\(\rho=\reg{res_entry_r2}\)" (855), which prints "ρ = 0.250000". | Use the fraction keys where they exist (`tau_r2_frac`), "≈" or "with margin …" elsewhere, and drop the display after ρ at 855. |
| A5-05 | minor | `A5_research.tex:1083` | "the hypotheses \(1/2<\tau<1\) and \(\rho\DT<2k\) of Lemma A.16" are not hypotheses of that lemma; they are the conditions under which it yields exactly zero research and recruiting research. | "At the intermediate strengths, \(1/2<\tau<1\) and \(\rho\DT<2k\) do not involve \((\lb,a)\) and hold at the three strengths, so Lemma A.16 leaves zero research and recruiting research." |
| A5-06 | minor | `A5_research.tex:451` | "Lemma A.16(a) gives \(\Own_H^{\rm Z}=\rho W_H(F)/2\)" cites a fact that is in the lemma's proof, not its statement. | "Entry ρ after every order in Lemma A.16(a) gives \(\Own_H^{\rm Z}=\rho W_H(F)/2\)." |
| A5-07 | minor | `A5_research.tex:191, 728` | Label ownership is asymmetric: the full Proposition 4 carries `prop:research-full` because the main text owns `prop:research`, but the full Corollary 3 fixes the label `cor:research` in the appendix and hard-codes "Corollary 3" in its heading. `C.tex` assigns the plain labels to the full statements and `-short` to the main-text forms. S9 will collide or drift unless one convention is chosen. | The coordinator fixes the convention for S8 and S9: either the main text takes `cor:research` and the appendix `cor:research-full`, as for the proposition, or both full statements take the plain labels and the main text the `-short` ones, as `C.tex` has it. |
| A5-08 | minor | `A5_research.tex:1115–1117` | In "General β", condition (U) is verified at \(r_1\) only; Lemma A.17 is also applied at \(r_2\). It holds there because \(\DT(r_2)>\DT(r_1)\) with \(m_{\lb}\) and \(\lb(\beta)\) unchanged, but the proof does not say so. | Add "and at \(r_2\), since \(\DT(r_2)>\DT(r_1)\)". |

## 4. Remarks for the coordinator (no change to the package)

- R1. Lemma A.15 and line 879 cite the A.4 low-class lemma (`lem:a4-low`) for a general claim. The frozen `B.tex` version of that lemma is general ("Let π < τ"), but the A.4 file in this checkout still states it on the example path, and it prints as Lemma A.10 rather than the frozen A.8; `lem:a4-path` prints as A.7 rather than A.10. Both resolve when the A.4 package is transplanted; S8 should confirm the general form is in place.
- R2. The Corollary 3 proof refers to Table 4 for the intermediate-strength entry values; S9 keeps or renumbers that table.
- R3. The main text at `sections/04_equilibrium_results.tex` still cites Proposition A.1 as "the research parameter region"; S9 aligns the words with the new title.
- R4. The package's numbers all resolve in this checkout because the S6 rows are already in `numbers.tex`; the build shows no unknown key.

## 5. What the referee recomputed

A print-only computation in a private folder, written independently of `o1_bounds.py` and `o4_margins.py`: exact fractions for every rational quantity (τ built from \(g_H\) and \(g_L\), not from a closed form), 40-digit arithmetic for the quantities that involve Euler's number, and root finding for \(r_R\), \(r_Q\), \(r_C\), \(\beta_{\rm lo}\) and \(\beta_{\rm hi}\).

| Quantity | Package | Referee | Agreement |
|---|---|---|---|
| \(\tau(r_0)\), \(\tau(r_2)\) | 195/308, 4245/5804 | same | yes |
| \(\DT(r_0)\), \(J(r_0)\), \(J(7/4)\) | 1/60, 113/18480, 171/3080 | same | yes |
| \(\varphi_a(r_0)\) | −1369550353/60351152400 | same, ≈ −0.0226930 | yes |
| \(c_H-B_{r_0}(1/2)\) | 287/240 | same | yes |
| bounds on \([6/5,7/4]\): \(\DT'\ge\), \(1-\tau\ge\), \(\DT\le\), \(\tau'\le\) | 11/72, 19/55, 9/56, 16875/211288 | same; the proof's route gives \(\tau'\le11309/207900\approx0.0544<0.0799\); the exact \(\tau'(7/4)=32/825\) | yes |
| \(J'\) bound, \(\varphi_a'\) bound at \(a=1/40\), \(a_{\rm mono}\) | 0.039942, 0.033767, 0.161713 | 21266929/532445760, 46061709624985094449/1364098973371103914560, 54484791118735094449/336923259750000000000 | yes, exact |
| tail bound \(J(7/4)-k-2a\lambda_E(r_2)\) | > 0 | 0.0186834 | yes |
| cap, \(m_{\lb}(1+\eu)\) | 0.336122 | 0.33612176891512119740, exactly 1 | yes |
| \(r_R\), \(\lambda_E(r_R)\), entry at \(r_R\) | 1.501023, 0.193853, 0.500846 | 1.5010229662625721456, 0.1938533819106594078, 0.5008463670313333 | yes |
| \(r_{\lb}\), \(r_N\), \(r_S\), \(r_U\), \(r_C\) | 1.677633, 1.747878, 2.124148, 2.434046, 3.592659 | 1.6776328343850808188, 1.7478775382679627436, 2.1241481328154506735, 2.4340455267120011353, 3.5926585187946618333 | yes |
| \(\varphi_a^*(r_{\lb})\) | 0.017446 | 0.0174457484568150571464 | yes |
| \(r_Q\), \(\lambda_E(r_Q)\) | 2.166995, 0.234257 | 2.16699515821928588228248724493, 0.23425725606563384863691342306 | yes |
| \(\varphi_\rho(r_N)\), \(\varphi_\rho(r_U)\) | < 0, > 0 | −0.0113912, 0.0073464 | yes |
| 24 pieces of width 1/10, smallest bound | ≥ 1/100 | 5993292043494701003/510152171246294601024 ≈ 0.0117480 on [6/5, 13/10]; all 24 exceed 1/100; last right end 18/5 | yes |
| kink intensity \((1-\rho)k/(2a\rho)\) | > 1 | exactly 6/5 | yes |
| at 1.55, 1.60, 1.65: \(k-\rho\DT/2\) | 387/49600, 19/3200, 211/52800 | same | yes |
| \(\lambda_R-\lambda_E\) | 0.041160, 0.079340, 0.114019 | 0.0411600725, 0.0793395149, 0.1140188962 | yes |
| \(\lb-\lambda_R\) | 0.098221, 0.057085, 0.019439 | 0.0982205739, 0.0570846674, 0.0194385911 | yes |
| \(e^*\) | 0.865703, 0.758777, 0.673748 | 3678038964014/4248616598655, 52567609936/69279436215, 113810500777358/168921585545505 | yes, exact |
| threshold-pair entry | 0.456294, 0.420777, 0.392494 | 2150859750351442475417/4713756945289187229720, 404319867721870544/960888945399049755, 77755017762538905788471/198104961104394761762280 | yes, exact |
| cap strip \(\lambda_E(r_1)\), \(\lambda_E(r_2)\) | 2416171/8316171, 79144333/235044333 | same | yes |
| \(a_{\rm lo}(\lb)\), \(a_{\rm up}\), \(a_{\rm lo}(\lambda_E(r_1))\) | 0.021469, 0.036763, 0.030579 | 0.0214693796, 19615197841161/533553754404400, 13003719387/425246096000 | yes |
| \(a_U(r_1;\lambda_E(r_2))\), \(a_U(r_2;\lambda_E(r_2))\) | 0.073556, 0.127845 | 1689420317493/22967685436600, 23490513452279/183741483492800 | yes, exact |
| cap-strip and cost-window margins | 0.045583, 0.000599, 0.003531, 0.011763 | 0.0455828899, 0.0005991041, 0.0035306204, 6276353981051/533553754404400 | yes |
| (U) margin at \(r_1\), β = 1/3 | > 0 | 0.0157192 | yes |
| \(\beta_{\rm lo}\), \(\beta_{\rm hi}\), \(a_{\rm mono}(1/3)\) | 0.236157, 0.4897, 0.150885 | 0.2361566855, 0.4897406731, 0.1508854175 | yes |
| \(\lambda_E'(\tau(7/4);\beta)\) rises in β exactly for | (used on (0, 1/3]) | β < 19/17 | consistent |
| \(r=2\): \(\tau\), \(\lambda_E\), \(\rho J-k\), \(e^*\), entry | 93/140, 1355413/6055413, > 0, 0.359944, 0.287449 | same; \(\rho J-k=11/11200\), \(e^*=292690607/813155460\), entry 40439906511409/140685489814428, \(U_H(1)=98917391/9688660800>0\) | yes, exact |
| access gains at \(r_1\) | 0.257948, 0.081960 | 0.2579478014, 0.0819602308 | yes |
| margins at \(r_1\), \(r_2\): \(M_{\lb}-\tau(r_1)\), \(\tau(r_2)-M_{\lb}\), (U) at \(r_1\), (U) at \(r_2\), \(r_N-r_{\lb}\) | 0.026059, 0.000334, 0.016421, 0.034723, 0.070245 | 0.0260585786, 0.0003335647, 0.0164205260, 0.0347234838, 0.0702447039 | yes |
| order \(r_0<r_R<r_{\lb}<r_N<r_S<r_Q<r_U<r_1<r_C<r_2\); \(r_N<7/4\); \(r_S<r_Q\) | stated | holds | yes |

Algebra rechecked by hand: the share derivative in Proposition 4(b); the slope difference \(2a\rho m_{\lambda_R}/[(2a-\DT m')(2a-(1+\rho)\DT m')]\); the factorisation of \(\Lambda_r\) and \(\Lambda_r(\lambda_E)=-[2\beta+\lambda_E(1-2\beta)]\varphi_a\); the closed form of \(\lambda_R\); \(\tau'=(-g_L'+\tau\DT')/\gamma\) from \(\gamma'=-\DT'\); the identity \(\varphi_\rho=[\rho\DT m_{\lb}-k-a\lb]+\rho\DT[M_{\lb}-\tau]+a[\lb-\lambda_E]\); \(\partial\lambda_E/\partial\beta=(2\tau-1)(1-\tau)/D^2\); the allocation identity in the access proof; \(g_L=(\ell^2-p^2)/(2r)\) and \(g_H=h-r/2-p^2/(2r)\) by direct integration.

## 6. Build, pages and language

- Full manuscript build from `slot/manuscript/` into the private folder: exit 0, 124 pages, all 23 fonts embedded. The log has no error, no undefined or multiply defined reference, no overfull or underfull box, and no unknown number key; the S6 rows are present in this checkout, so the thirteen names the writer's report lists as pending now print.
- A.5 occupies pages 71 (lower half) to 95 (upper third). Every page was read as extracted text, and pages 76, 77, 85 and 90 were also read as rendered images: the case braces, the (CR) tag, the primitives display and the piece-bound display of Lemma A.18 are legible and unclipped. The printed numbers are Lemmas A.12 to A.18, Proposition 4, Corollary 3, Proposition A.1 and Remark A.1; cross-references to A.4 print A.7 and A.10 for the path and low-class lemmas (remark R1).
- Language scan on the package: zero counted hits in every category; 13 allowed tie-rule phrases, each stating an indifference convention inside a statement or proof. A read of the whole file finds no status word, hedge, narration of changes, process word, retired name of the example, tie code, tool or personal name, and no comment line. Every number prints through `\reg`, fractions included. The preparation cost is untouched. Vocabulary follows `NOTATION.md`: floor-entry research, recruiting research at the cap, the threshold pair, the entry ceiling, the floor margin, \(\lambda_Q\), \(r_Q\), \(\hat s_-\), \(r_\pm\) for path ends and \(r',r''\) for pieces.
- The statement comparison (Section 2, column 1) and the referee's computation are in the private folder; only this report was added to the repository.
