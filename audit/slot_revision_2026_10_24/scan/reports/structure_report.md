# Structure pass report: formal apparatus moved to Appendix A

Branch `slot-revision`, manuscript `slot/manuscript/`. I worked in place. I did not commit and did not write tests. The plan is `audit/slot_revision_2026_10_24/scan/reports/prose_apparatus.md`, Sections 2.2, 2.3, 2.4, 4 and 6. Each seam in `sections/` and `appendix/` has one comment line `% STRUCTURE: <what left> -> <destination>` (or `<- <source>` on the appendix side).

## 1. Result

- The main text now has four environments, all propositions:
  1. Proposition 1, "Competition and the two returns to information; analytical" (unchanged).
  2. Proposition 2, "Competition creates competition; analytical".
  3. Proposition 3, "Coexistence on the benchmark path; computer-assisted" (short statement).
  4. Proposition 4, "Competition creates research; part (a) analytical, part (b) computer-assisted" (merge of the former Proposition 4 and Corollary 3).
- No assumption, definition, lemma, corollary or remark stays in `sections/*.tex`.
- Main text: the references now start on PDF page 35. Before the pass they started on page 39. The main text is pages 2 to 34 (33 pages after the title page), against 37 pages before. The PDF has 103 pages in total, against 102 before.

## 2. What moved where (one line per environment)

| Environment (old number, old label) | Main text now | Appendix destination, new number |
|---|---|---|
| E-a Assumption 1 `ass:classes` | prose with the numbered display `eq:classes` (printed (1)), named "the class ranking", §2.2 | none; label retired |
| E-b Definition 1 `def:equilibrium`, with (E1)–(E6), f_j, e(x), the tuple 𝓔, and the paragraph on off-path beliefs | one prose paragraph with the U_j display, §2.4; pointer to Definition A.1 | Definition A.1, unnumbered opening of Appendix A (before A.1), with η and one sentence on the tie rules |
| E-c Proposition 1 `prop:returns` | kept; "Assumption 1" became "the class ranking (1)" | — |
| E-d Lemma 1 `lem:beliefs` | prose paragraph in §3.2 | Lemma A.1 in A.2, before its proof; with δ_q, b_0 and `eq:odds` (now (A.3)) |
| E-e Corollary 1 `cor:exclusion` | prose ("This is the ceiling of the model"), §3.2 | Corollary A.1 in A.2, before its proof |
| E-f Lemma 2 `lem:prices` | prose paragraph in §3.2 (τ inline, sufficiency argument kept) | Lemma A.2 in A.2, with the rule-CM sentence on part (d) |
| E-g Lemma 3 `lem:trading` | the K_H, K_L display with the bounds, §3.3 | Lemma A.3 in A.2, before its proof |
| E-h Proposition 2 `prop:ccc` | kept; δ-notation and the shorthand B_i, Δ_i, M, m, κ, Ent_1, e_H written out; (H1)–(H3) tags kept | — |
| E-i Proposition 3 `prop:coexistence` | short statement: existence, (a) coexistence on [r_A,r_N], (b) entry on the branch; five-strengths sentence replaces the definitions table; the forms table, J, 𝔯, s_± and the shorthand M, m left | unnumbered `named` environment "Proposition 3 (full statement; computer-assisted)" in A.4, before the proof: threshold order, set table (a `tabular`, not a float), entry of each form, parts (a)–(c) verbatim |
| E-j Remark 1 `rem:ties` | removed | prose in A.4, paragraph "Other tie rules" (no environment); label retired |
| E-k Corollary 2 `prop:priors` | two sentences with `piA_lo_B`, `piA_hi`, `pimax` and a pointer | Corollary A.2 in A.4, new unnumbered heading "Coexistence at other priors", with its definitions paragraph, before the proof |
| E-l Proposition 4 `prop:research` | merged statement; old (i)–(iii) nested under part (b) | proofs: "Proof of Proposition 4(b)" with "Part (b)(i)" to "(b)(iii)" |
| E-m Corollary 3 `prop:researchbranch` | merged as Proposition 4(a) | "Proof of Corollary 3" became "Proof of Proposition 4(a)"; label retired |
| E-n Remark 2 `rem:researchties` | removed ("research never has a tie" stays in §5) | Remark A.1 in A.5, before its proof; "Proposition 4" became "Proposition 4(b)"; the Table 4 pointer became the three `res_th_entry_*` values |
| E-o Remark 3 `rem:sizes` and §6.4 `sec:sizes` | footnote in §2.3 after the slot references | none; both labels retired |
| (E1)–(E6) | gone from the main text; (E5), (E1), (E4) in the §2.4 paragraph after the definition became words | Definition A.1 |
| (E7) and the research tuple | prose in §5 | A.5 opening, new paragraph "Equilibrium with research", then "Standing assumptions" |
| u_λ and the closed form of λ_E | §5 keeps M_λ, m_λ=1−M_λ and λ_E in words | A.5, paragraph "Derived functions" |
| Closed form of r_U | §5 keeps r_U ≈ `res_rUR` | already in the proof of Proposition 4(b)(iii) |
| Tie-rule alternatives I0 and CM (list) | one sentence names IM and C1 and glosses I0 and CM with a pointer to A.4 and Table A.3 | A.4, paragraph "Other tie rules", with the list and the sentence on where they change a conclusion |
| Table 4, row "Entry in the threshold equilibrium (rule CM)" and its note | removed (with its `\midrule`) | values in Remark A.1 |

Counter changes in `main.tex`: definition and remark get the prefix A and a reset, beside the existing proposition, lemma and corollary lines.

## 3. Labels

- New: `eq:classes`.
- Retired: `ass:classes` (15 sites now read "the class ranking~\eqref{eq:classes}"; the paragraph title in A.1 is "Scope of the class ranking."), `rem:ties` (§8 now cites Appendix A.4), `prop:researchbranch` (A.5 cites Proposition 4(a)), `rem:sizes`, `sec:sizes` (no citing site).
- Kept, new printed number: `def:equilibrium` A.1; `lem:beliefs` A.1; `lem:prices` A.2; `lem:trading` A.3; `cor:exclusion` A.1; `prop:priors` A.2; `rem:researchties` A.1; `eq:odds` (A.3).
- Shifted by the moves (all cited by `\ref`): `lem:a4-*` A.4–A.8 (were A.1–A.5); `lem:a5-*` A.9–A.13 (were A.6–A.10); `cor:purchasesonly` A.3 (was A.1); main-text equations +1 from `eq:order` on; appendix equations +1 from `eq:a2-terminal` on.
- Unchanged: Propositions A.1–A.14, Tables A.1–A.6, all section, figure and table labels. The aux diff against the baseline shows no other change.

Main-text references that pointed at moved lemmas became prose or section pointers: §4.1 "the trading bound of Section 3.3" and "the ceiling of Section 3.2"; §4.2 "Lemma A.2(c) in Appendix A.2"; §6.1 and §7.1 "the trading bound(s) of Section 3.3"; §3.3 last sentence now cites Appendix A.4 for the full list.

## 4. References changed outside `sections/` and `appendix/`

`slides.tex`:
- frame subtitle, "Lemma 3" → "Lemma A.3";
- research frame, "(Corollary 3)" → "(Proposition 4(a))", twice.

`comparison.tex`:
- "Propositions 1 to 4 and Corollaries 2 and 3 in the main text" → "Propositions 1 to 4 in the main text";
- "Lemma 1/2/3" → "Lemma A.1/A.2/A.3" (prose at the slot set-up, results table rows, and "Uniqueness starts from the bounds of Lemma A.1");
- "Corollary 2:" → "Corollary A.2:"; in the same cell "(Section 4.3)" → "(Appendix A.4)", because the rule-CM point at π_max left §4.3;
- "Proposition 4, Corollary 3, Proposition A.2:" → "Proposition 4, Proposition A.2:"; "(Proposition 4 and Corollary 3;" → "(Proposition 4;";
- "(Remark 1)" → "(Appendix A.4)", twice;
- "Definition 1" → "Definition A.1", twice;
- "Section 4.3 displays the five forms" → "Appendix A.4 displays the five forms"; "in Section 4.3 and A.4" → "in A.4";
- "Section 5 adds (E7)" → "Appendix A.5 adds (E7)";
- tie-rules row: "I0 and CM stated where they change a result" → "I0 and CM defined in Appendix A.4 and stated where they change a result".

I changed nothing else in either file. The hard-typed "(A.4)", "(A.5)", "(A.6)", "(A.9)" in the slides are Proposition A.x numbers, which did not change. "Table A.3" and "Table A.6" in `comparison.tex` stay correct.

## 5. Status tags (report Section 4)

- Titles: as listed in Section 1.
- Method sentences after the computer-assisted propositions: "Two monotonicity steps of the proof rest on exact Sturm counts; every other step is analytical (Appendix A.4)." and "The equilibrium lists of part (b) follow from analytical arguments, and exact rational and interval arithmetic settles the strict signs at the benchmark."
- Inline "(computer-assisted)" removed at six places, each after I confirmed that the appendix paragraph carries the tag: §5 branch on [r_R, r̄_R) (A.5 "The branch at calibration B (computer-assisted)"); §6.2 Table A.4 economies (A.6 paragraph); §6.2 three-class collision (A.6 paragraph); §6.3 S(B) example (A.6 "The vector S(B)"); §6.3 benchmark with (a_T,d) (A.6 "The benchmark B"); §7.3 reserves (A.7 "The benchmark reserves").
- §6 opening now says "states each result in full, with its status, and proves it"; "and the order menu" left with §6.4.
- Exception: the tag at §8 (spread entry share, `ba_share_r1_B`) stays. Appendix A.8 has no status tag for that number, so removing it would lose the label.
- "Open" statements and the Table 5 note are unchanged.

## 6. Facts and seams to check in the later pass

- Every fact of each moved or replaced block survives in the main text or in Appendix A. I found no fact I could not place. Three appendix passages now repeat a main-text sentence or an existing appendix sentence: the off-path paragraph after Definition A.1, the Remark 1 prose and the closing paragraph of A.4 "Other tie rules", and the (E7) prose against Lemma A.9.
- The tie-rule names stay defined in the main text: §2.4 names IM and C1 and glosses I0 and CM. The coexistence figure prints "rule CM", and §4.2, §6.3 and §8 still use the names.
- The form letters N, R, F, Q, T stay in §4.3 and in the Figure 2 notes. The figure legend defines them, and one added sentence points to the legend and to A.4.
- Not done, because they are style or sit outside the sections the brief assigned: the reordering of the Proposition 2 intuition paragraphs; the shortened tie-rule sentence after Proposition 2; the reworded Figure 2 notes; the notation items of report Section 3 (for example the z/λ collision and the sentence on Euler's number); moving the tie-rule clauses of §8 to A.8.
- Main-text equation numbers shift by one, because the class ranking is now display (1). No file hard-types a slot equation number.
- The §2.3 footnote (former Remark 3) uses e before §4.2 says that it is Euler's number. The old remark sat in §6, after that sentence.
- §5, the paragraph after Proposition 4, says "the research value is zero". The symbol V and the term "research value" moved to A.5 with (E7), so the main text no longer defines the term.
- Remark A.1 has no status tag, and the former Remark 2 had none either. The opening of Appendix A says that each statement carries its status, so this gap is now visible in the appendix.
- §3.2 says "when g_H ≥ g_L, gross profit does not fall with the belief". This keeps the weak hypothesis of Corollary A.1.

## 7. Checks (all run from outside the repository; build outputs in `/tmp/ccc_slot_scan/`)

1. `latexmk -pdf ... -outdir=/tmp/ccc_slot_scan/build_struct main.tex`: exit 0, first from a clean directory and again after the last two edits. `grep -E "undefined|multiply|Reference .* on page" main.log` gives no output.
2. `comparison.tex` (pdfLaTeX, `build_struct_cmp`): exit 0. `slides.tex` (XeLaTeX, `build_struct_slides`): exit 0.
3. `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`: 21 files, 676 keys, missing keys: 0, literal decimals outside `\reg`: 0.
4. Environments in `sections/*.tex`: 4, all `proposition` (03: 1, 04: 2, 05: 1).
5. Printed headings checked in the PDF text: Propositions 1–4, Definition A.1, Lemmas A.1–A.13, Corollaries A.1–A.3 (A.3 is `cor:purchasesonly` in A.8), "Proposition 3 (full statement; computer-assisted)", Remark A.1. I looked at pages 24 (Proposition 4) and 59 (the full statement of Proposition 3) as images. The nested parts and the set table render correctly.
6. Page count: references start on PDF page 35 (baseline 39).
7. `git status`: only the 16 manuscript files changed (`main.tex`, 7 section files, 6 appendix files, `slides.tex`, `comparison.tex`). Two untracked files under `audit/slot_revision_2026_10_24/scan/reports/` are not from this pass.
