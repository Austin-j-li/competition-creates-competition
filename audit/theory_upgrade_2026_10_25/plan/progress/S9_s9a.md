# S9, Sections 2 to 4 of the main text

Report of the prose writer to the coordinator. Nothing is committed. Files changed: `slot/manuscript/sections/02_model.tex`, `03_competition_information.tex` and `04_equilibrium_results.tex`. `main.tex` is unchanged. The build went to a private folder outside the repository, and no build product is in the repository.

## Section 2, the model

- Moved out: the example's declaration (old 02:78–83, the point masses, \(\pi\) and `eq:order`), the example's unit sentence (old 02:87–88) and the uniform main case (old 02:54–55). All three now stand in Section 4.2.
- T-2.1 placed at old 02:54–55: the definition of a path.
- T-2.2: the normalization paragraph keeps only its general sentence.
- T-2.3 placed as the liquidity footnote (old 02:123–125), as written.
- T-2.4 placed at old 02:203–204: notation along a path.
- T-2.5 placed at old 02:216–218, with one added clause that names the other two tie rules ("the other two are that an indifferent investor abstains and that an indifferent high-cost challenger may prepare with any probability"). Without it, the phrase "under all four tie rules" in Proposition 2 refers to rules that the main text never names.
- T-2.6 placed at old 02:226–228: \(W_j(F)\), outbidding, \(e_j\) and the takeover share.
- Vocabulary and symbols: the Laplace scale \(s\) becomes \(\xi\) in the footnote (NOTATION part (d), S9 and S10). Old 02:72, "the spread rises", reads "that difference rises", because the spread is defined only in Section 2.4.
- Language fixes from the scan: "It may be" → "It is" (02:11); "may know" → "can know" (02:22); "need not reveal" → "can stay silent on" (02:32); "Two potential acquirers face the target" → "The target faces two potential acquirers" (count opener); "equally likely to fall below it" → "fall below it with equal probability".

## Section 3, competition and information

- Moved out: the closed forms `eq:payoffs` and `eq:derivatives` (old 03:19–35), the example's clause of the class-gap identity (old 03:76) and the limit as \(r\) approaches \(\ell\) (old 03:80–81). They stand in Section 4.2 as T-4.5.
- T-3.1 placed in place of old 03:19–39, before Proposition 1, which is unchanged. The intuition for Proposition 1 stays the slice argument of old 03:60–70, which comes from the general formula.
- T-3.2 placed at old 03:76–78; T-3.3 at old 03:80–82; T-3.4 at old 03:99–100.
- Old 03:128, "the upper bound is the spread", reads "the spread bounds the return from above" (NOTATION part (d)).
- T-3.5 placed at old 03:140–141.
- T-3.6 placed as Section 3.4, "What the market sees of the auction", `\label{sec:twonumbers}`. The last clause reads "the formal statements and their proofs", because Appendix A.2 holds two lemmas (`lem:reduction`, `lem:twonumbers`).
- Sections 2 and 3 contain no example and no example strength. The symbol \(r\) appears there only as the index of a general path.

## Section 4, equilibrium results

### 4.1

- Proposition 2 is the full statement of `statements/prop2_full_for_main_text.tex`, with labels `prop:ccc` and `eq:a3-share`. Edits to the source, none of substance: the frame cites the class ranking \eqref{eq:classes}; "\(F_1\le F_0\)" is written in words, as "a continuous first-order stochastic strengthening", because the main text defines no order on distributions; the "Write" sentence adds \(t_{0,i}\) and \(t_{L,i}\), which parts (i) and the last sentence use; the last sentence says that \(\mu_i(x)\) and \(e_i(x)\) are the posterior and entry after the order \(x\); "the probability that class \(H\) acquires the target, conditional on acquisition by the challenger" is written "class \(H\)'s takeover share", the term defined in Section 2.4; the part labels keep the words "The weak incumbent \(F_0\)" and so on.
- The hypotheses paragraph stays. T-4.2 ends the paragraph on the window, with "an open set of parameters" for "an open set of primitives", so that 4.1 and 4.2 name the set with one word. T-4.3 (ownership, then decisive advantage) replaces old 04:63–67, with "the ownership condition in part (ii)" for "the condition in part (ii)" and "the takeover-share statement" for "the share statement". T-4.3b is placed in the closing paragraph, which reads "Appendix A.3 gives the proof and the three equilibrium tuples".

### 4.2, "The example and the fixed-information control" (`sec:benchmark` kept)

- T-4.4 opens the subsection. One sentence is added in front: "The numbers and figures of the paper come from an example." `eq:order` stands here.
- Corollary 1 (T-4.4a), `\label{cor:ccc-example-short}`, title "Recruitment and ownership in the example". Two changes to the target: "When \(1+u=\eu\), as in the example's slot," for "In the example's slot, with \(1+u=\eu\)," because the prior band depends on the slot only through \(1+u\); and the entry clause adds "at \(r_1\) and returns to \(\rho\) at \(r_2\)", which Corollary 1(a) in Appendix A.3 states.
- Table 1 caption: "Acquisition payoffs in the example."
- T-4.4b (entry, ownership, takeover share, decisive advantage) replaces old 04:113–119.
- T-4.5, the two numbers in closed form, with `eq:payoffs`, `eq:derivatives` and \(\tau(r)\), opens "In the example, integration over \(R\) gives". The closed form of \(\tau(r)\) was checked by hand from \(\tau=(c_H-g_L)/(g_H-g_L)\) and the closed forms of \(g_H\) and \(g_L\).
- T-4.6 replaces old 04:121–127. Table 2: caption T-4.6a; column "Benchmark" → "Example"; note "The example's auction and costs"; "Proposition~\ref{prop:region} gives the exact endpoints" → "Corollary~\ref{prop:region} in Appendix~\ref{app:prop2} gives the exact endpoints"; row label "Presence \(\lambda\) at \(\beta=1/3\)" → "Presence \(\lambda\) at the largest \(\beta\)" (scan: typed fraction; the last row of the table prints the range \((0,1/3]\)).
- T-4.7 replaces old 04:155–165.
- Figure 1: caption and notes as in `figure_captions.md` ("in the example"; "the preparation threshold \(\tau(r)\)"; "the example's value lies"). The paragraph after the figure cites Corollary~\ref{cor:ccc-example-short}.
- The fixed-information control stays. In its general sentence, "gross profit at the two strengths" reads "gross profit against the two incumbent distributions" (old 04:194). Table 3 caption "in the example", note "The example."

### 4.3, "Coexistence" (`sec:coexistence` kept)

- T-4.8 lead-in, then Proposition 3 (T-4.9), `\label{prop:coexistence}`, title "Quiet and informative markets". Two additions, both in the full statement in A4 and in the frozen main-text form in `B.tex`: part (b) ends "Every gap in coexistence lies at spreads too narrow for a sure purchase to pay"; part (c) reads "with \(r\) in a closed interval above the reserve", because A4 (c)(iii) takes \(p<\min I\), and "every low-class value lies between the reserve and the lowest strength" gives only \(p\le\min I\).
- T-4.10, the intuition, as written.
- A lead-in to Corollary 2 is built from T-4.12: its first sentence (the example meets Proposition 3(c)) and the definitions of \(r_A\), \(r_N\) and \(r_F\) in words. Corollary 2 uses those strengths, so they are defined before it; \(r_C\) is defined in Section 4.2.
- Corollary 2 (T-4.11), `\label{cor:example-coexistence-short}`, title "Coexistence in the example". It adds "An equilibrium exists at every strength of the path from \(r_0\) to \(r_2\)", from part (c) of the full Corollary 2 and the frozen main-text form. The band now cites Corollary~\ref{cor:ccc-example-short}.
- Figure 2 follows Corollary 2, with the caption and notes of `figure_captions.md` and panel letters (a) path, (b) region, (c) enlargement, which match the figure file. One change: "The dotted lower edge \(\tau=1/2\)" reads "The dotted lower edge, where \(\tau\) equals the prior," (scan: typed fraction). The notes cite `cor:example-coexistence`, the full Corollary 2, because they refer to each equilibrium, which only the full statement lists. Moving the figure to this position keeps it on the page after Corollary 2 instead of inside Section 5.
- The reading after Corollary 2 is T-4.12 without the definitions moved to the lead-in, with the values of \(r_A\), \(r_N\), \(r_F\), and one sentence from old 04:316–321 as the intuition of the corollary: between \(r_A\) and \(r_F\), class \(H\) buys at the rate \(b[\DT(r)/k-2]\), which rises with the spread until it reaches \(\lambda\) at \(r_F\). This rate is \(s_+\) of A4 at the prior \(1/2\).
- T-4.13 (the high cost between the two bounds) and T-4.14 (other priors) follow, as written.
- Stale references: no `Proposition~\ref{prop:region}` is left. The two remaining `\ref{prop:region}` point to the full Corollary 1 in Appendix A.3 on purpose (the full statement, and the exact endpoints of Table 2). Old 04:259 and 04:274 left with the old Proposition 3.

## Labels and numbering

- Main-text corollaries use the existing `corollary` environment of `main.tex`. The main text has no other corollary, and the appendix resets the counter and prints A.\(n\), so Corollaries 1 and 2 print as 1 and 2 and no hyperref anchor collides. The Section 5 writer uses `namedresult` with `\fixedlabel{cor:research-short}{3}`, which prints 3; the two mechanisms coexist.
- Labels in the build (`main.aux`): `prop:ccc` 2, `eq:a3-share` (6), `cor:ccc-example-short` 1, `prop:coexistence` 3, `cor:example-coexistence-short` 2, `prop:region` 1 (A3), `cor:example-coexistence` 2 (A4), `cor:research-short` 3, `cor:research` 3. No label is defined twice.

## Build and scan

- Build: `latexmk -pdf -interaction=nonstopmode` from `slot/manuscript` into the private folder; exit 0; 149 pages. Sections 2 to 4 are pages 5 to 23; I read every page of them in the PDF text and the layout of pages 16, 22 and 23 as images.
- Log: no multiply defined label, no undefined reference or citation. Two groups of messages come from files outside my sections:
  - four unknown number keys in `appendix/A9_parameters.tex` (lines 138 and 149 to 151): `margin_res_phi_r0_B`, `margin_res_rQ_rN_B`, `margin_res_rU_rQ_B`, `margin_res_cap_lamQ_B`;
  - eight pdfTeX warnings "destination with the same identifier (equation.A.16)" at `appendix/A5_research.tex:567`, the display with `\tag{U}\label{eq:a5-U}`.
- Every number in my sections prints through `\reg`; every key exists in `numbers.tex`.
- Language scan on the three files: 0 counted hits; 4 allowed (the tie phrases "may mix" and "may prepare with any probability"). The first run had 7 hits, all fixed as listed above.
- `grep -i benchmark` on the three files finds only the non-printing label `sec:benchmark`.

## Targets placed with changes, and why

- T-4.4a: label `cor:ccc-example-short` instead of `prop:region` and `cor:ccc-example`, which the full Corollary 1 in A3 owns; the two wording changes above.
- T-4.9: the two additions above, each from the full statement.
- T-4.11: label `cor:example-coexistence-short`; the existence sentence; the band cites Corollary 1 by its main-text label.
- T-4.12: split into a lead-in before Corollary 2 (definitions) and a reading after it (values), so that the corollary uses no undefined strength.
- T-2.5: one clause naming the two other tie rules.
- Figure 2 notes: "where \(\tau\) equals the prior" for "\(\tau=1/2\)".
- T-4.2: "parameters" for "primitives".

## Outside my sections

- No main-text or appendix file cites `prop:region` or a corollary label with the word "Proposition", "Lemma" or "Remark".
- The four unknown keys in A9 and the duplicate destination at A5:567 are listed under "Build and scan".
- I read pages 14, 15, 17 and 18 as images as well: the display of (H1) to (H3) in Proposition 2 and Tables 1 and 2 fit the text width.
