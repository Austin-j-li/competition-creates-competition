# S9, Sections 5 to 8: report of the prose writer

25 October 2026. Files changed: `slot/manuscript/sections/05_research.tex`, `06_robustness.tex`, `07_welfare.tex`, `08_empirical.tex`. `main.tex` is unchanged. Sources: `statements/wording_targets.md` (T-5.1 to T-5.9, T-8.1 to T-8.8, with "Changes after the referee"), `statements/figure_captions.md`, the frozen statements `C.tex` and `D.tex`, and the appendix as it stands (A5 to A8).

## Section 5, Competition creates research

Order of the section: the opening paragraphs on research (05:3 to 27, with T-5.1 in place of the first sentence); T-5.2, the lead-in with `\label{eq:research}` on the display, which gains the sale's profit; Proposition 4 (T-5.3); its intuition (T-5.4); Corollary 3 (T-5.5); a pointer to the full Corollary 3; Table 4 (rows and note of T-5.6); the reading of Table 4 (T-5.6); the reading of Corollary 3 (T-5.7); Figure 3 with the caption and notes of `figure_captions.md`; the comparison with coexistence (T-5.8); the research parameter region (T-5.9).

What left the section:
- the example-only Proposition 4 (old parts (a) and (b)) and the two paragraphs after it (05:73 to 81); their content goes to Corollary 3 and the intuition;
- the old lead-in paragraph 05:44 to 50 ("At the benchmark strengths...", the research parameters of the example), replaced by T-5.2 and by the declarations inside Corollary 3;
- the paragraph on \([r_R,r_{\lb})\) as the end of the equilibrium and on \(r_U\) (05:119 to 130); \(r_U\) and `res_rUR` do not print in the main text;
- "interval enclosures" in the Table 4 note, "now" (05:3, 05:149), "the research branch" (four places), "the benchmark" (nine lines), and the two references to "Proposition 4(b)" (05:143 in the figure note, 05:156 in the parameter-region paragraph).

The research story ends at the entry ceiling: Corollary 3(ii) gives recruiting research on \([r_R,r_C]\), at the cap from \(r_{\lb}\); T-5.7 and the figure note say the same.

Placed as written: T-5.1, T-5.2, T-5.4, T-5.5, T-5.6, T-5.7, T-5.8, T-5.9 (spliced into the existing parameter-region paragraph, which cites `cor:research-short`).

Departures from the targets, each deliberate:
1. **Proposition 4, the threshold below one.** T-5.3 puts \(1/2<\tau<1\) in the frame. The appendix setting (A5) and the frozen main-text form in `C.tex` put only \(\tau>1/2\) in the frame and \(\tau<1\) inside part (d), up to the strength at which research reaches its cap. The brief asks the main text to match the appendix in hypotheses, so the frame reads \(\tau>1/2\), and part (d) adds "and that the threshold stays below one up to the strength at which research reaches its cap". The recruitment intensity is still defined for \(1/2<\tau<1\) in the lead-in, as T-5.2 has it. The rest of T-5.3 stands as written.
2. **Intuition, two added sentences.** After the ownership paragraph of T-5.4: "A decisive advantage of class \(H\) (Section~\ref{sec:ccc}) supplies this outbidding at every incumbent against which a purchase recruits", from Proposition 4(c) of the full statement. After the path paragraph: two sentences that name the cheap-research condition in words and point to Appendix A.5 for it and for the full statement and proof of Proposition 4. The frozen main-text form carries both facts; T-5.3 and T-5.4 do not.
3. **Corollary 3 cites its full version.** One sentence after the corollary: "Appendix A.5 states Corollary 3 in full, with the low class's orders along each equilibrium and the equilibria at the three intermediate strengths of Table 4, and proves it." The brief asks each main-text corollary to cite its full version; T-5.5 and T-5.7 do not.
4. **Figure 3 note, the cap.** `figure_captions.md` writes \(\lb=\reg{res_cap}\); the note writes \(\lb\approx\reg{res_cap}\), following the coordinator's decision on the cap in the targets (T-5.5, T-5.6).
5. **Wording changes for the scan.** "throughout this section the prior is \(1/2\)" reads "The prior is \(1/2\) throughout"; "each result of this section" reads "each result on research"; "a purchase becomes more likely" reads "more frequent" (T-5.4 and T-5.6). The meaning is unchanged.
6. **Table 4 note, the example's notation.** The note gains "with \(\lambda_E(r)=\lambda_E(\tau(r))\) and \(\lambda_R(r)=\lambda_R(\DT(r))\)", because the lead-in defines \(\lambda_E(\tau)\) and \(\lambda_R(\DT)\) and the table rows print them as functions of \(r\) (`NOTATION.md` part (c): the example keeps \(r\), declared once).
7. **The parameter region.** "\(\beta\in(\reg{res_beta_lo},1/3]\)" reads "\(\beta\in(\beta_{\rm lo},\reg{res_beta_upper}]\), with \(\beta_{\rm lo}\approx\reg{res_beta_lo}\)", as Proposition A.1 states it, because the lower end is a rounded root.

Labels: `prop:research` (Proposition 4, the plain label); `eq:research` (equation 6); `cor:research-short` (Corollary 3); `tab:research` (Table 4); `fig:research` (Figure 3). The full statements in A5 keep `prop:research-full` and `cor:research`. No duplicate label in the build.

Corollary mechanism: the section defines `\fixedlabel` with `\providecommand` at its top, as A3 and A5 do, and sets Corollary 3 as
`\renewcommand{\resultname}{Corollary 3}\begin{namedresult}[Research equilibria in the example]\fixedlabel{cor:research-short}{3}`.
This uses the `named` machinery of `main.tex` with the optional title, so it prints "Corollary 3 (Research equilibria in the example)." with the title in roman, as the propositions print. `\begin{named}{Corollary 3 (...)}` would set the title in bold. At the final build Section 4 had no corollary yet and `main.tex` had no main-text corollary counter; the coordinator should give Corollaries 1 and 2 the same form, or switch all three to one counter.

Figure: `figures/research.pdf` (the filled figure of S7), caption "Research and entry along the example's path.", notes from `figure_captions.md`. Read in the PDF: the marks \(r_R\), \(r_{\bar\lambda}\), \(r_N\), \(r_Q\), \(r_C\) and the labels "zero research", "recruiting research", "recruiting research at the cap", "floor-entry research", "entry along the recruiting branch" agree with the note.

Handshakes with Section 4: the intuition cites Section~\ref{sec:ccc} for "a decisive advantage of class \(H\)", and Corollary 3 and its reading rely on the example being declared at the opening of Section 4.2. Both belong to the other prose writer's targets (T-4.3, T-4.4); the coordinator should check them when Section 4 is in place.

Observation outside this brief: the in-figure label of Figure 3 reads "cap \(\bar\lambda=\) 0.336122" with "=", while every note and statement writes \(\lb\approx\reg{res_cap}\). The label comes from the figure code (S7); it can be aligned in S11 or S12.

## Section 6, Robustness

- 06:10 to 12: "The cost now mixes ..." becomes "The proposition lets the cost mix ..."; "may be atomless" becomes "can be atomless".
- "At the benchmark" (06:17), "near the benchmark" (06:52), "of the benchmark" (06:69), "At the benchmark itself" and "At the benchmark" (06:76, 06:78) become "In the example", "near the example", "of the example", "In the example itself", "In the example".
- \(v_*\) becomes \(\theta_*\) (three places).
- 06:28: "differ above the reserve" becomes "class \(H\) has the higher mean value", the hypothesis of Proposition A.4 (\(\E_H[\theta]>\E_L[\theta]\)).
- 06:58: "A challenger may know its integration plans" becomes "A challenger knows its integration plans".
- 06:79: "a buyer signal" becomes "a challenger signal".
- Section 6.3 gains one scope sentence after the first mention of Proposition A.6: "It holds at the prior \(1/2\) for every pair of ranked classes and every weak and strong incumbent with continuous distributions." It follows the hypotheses of A.6 as it stands (ranked finite-mean classes, continuous \(F_1\le F_0\), prior one half). No wording target gives a sentence for Section 6.
- References follow the appendix by `\ref`: preparation-cost laws A.3, value classes A.4, many classes A.5, complementary signals A.6 (the former A.7). Table A.4 still lists six economies.

## Section 7, Welfare and sale terms

- "In the benchmark" (07:20, 07:56), "with the strong benchmark" (07:32, which reads "in the example at \(r_1\)"), "In the benchmark of Section 4.2" (07:67), the Table 5 caption, its note, and "in the benchmark" (07:98) all name the example.
- 07:27 to 28: the order unit \(z\) is written in words, as `NOTATION.md` gives it.
- 07:106 to 107: "strict deterrence after the low class is excluded requires this second exclusion" becomes "strict deterrence with a reserve that excludes the low class requires the reserve to exclude the weak incumbent as well".
- 07:50: "\(\omega\ne1/2\)" and "at \(\omega=1/2\)" become "\(1-2\omega\ne0\)" and "when \(1-2\omega=0\)", which matches the sign of \(1-2\omega\) in the same sentence and removes a typed fraction after "=".
- "A reserve that excludes the low class" (07:70) stays: `NOTATION.md` keeps that phrase in full and overrides the lens plan's "a reserve above every low-class value". "A high-class challenger" (07:52) stays, as `NOTATION.md` allows. "The next buyer" (07:46) stays.
- References: access A.7, payment rule A.8, reserves A.9, by `\ref`. The statements in A7 were checked against the text; no hypothesis changed.

## Section 8, Empirical implications

Placed as written: T-8.1 (opening), T-8.2 (entry and incumbent strength), T-8.3 and T-8.4 (the price gap and its entry component, with the example's numbers), T-8.5 (the informed share), T-8.6 (winners), T-8.7 (announcements), T-8.8 (two clusters, with the rest of the old paragraph kept). These are the four general predictions in prose: price impacts and the price gap, the informed investor's presence, the winner, announcement returns. The example's numbers appear only as illustrations after each general statement.

Qualifiers kept: two-sided trade for every test (T-8.3, T-8.5, T-8.6, T-8.7); a prior below the preparation threshold for the weighted test and the no-order drop (T-8.3, T-8.7); the prior and the slot fixed for the winner trend and for the entry-component trend (T-8.3, T-8.6); \(3p^2<\min\{\underline\theta,\underline r\}^2\) for the entry-component trend; entry at its floor after a sale and after no order, and a known \(\rho\DT\), for the sale-price identification.

Departures, each deliberate:
1. One sentence added to T-8.1: "The predictions concern price impacts, the informed investor's presence, the winner and announcement returns." It names the four predictions, as PLAN.md S9 asks, without opening a paragraph with a count.
2. T-8.3 says "the expected price after the order opportunity" and T-8.7 "the expected price before the opportunity". Both read "before", as Proposition A.13(iv) does.
3. For the scan: in T-8.6, "where a high-class value is more likely than a low-class value to beat it" reads "where a high-class value beats it with a higher probability than a low-class value", and "even where they no longer predict entry" reads "even where they do not predict entry", the wording of the frozen main-text form in `D.tex`.
4. Measurement paragraph (no target): "an opportunity with no trade" becomes "with no order"; "the buyer's decision" and "the further buyer's fit" become "the challenger's decision" and "the challenger's fit"; "flow from sector specialists" becomes "orders from sector specialists".

References: Proposition A.2 (fixed information), A.10 to A.13 (price gap, identification, winner, announcements), by `\ref`. The label `sec:benchmark` of Section 4.2 is cited twice (07:67, 08:17) and does not print.

## Build and scan

- Build: from `slot/manuscript`, `latexmk -pdf -interaction=nonstopmode -outdir=/Users/austinli/Projects/ccc-tu-scratch/s9b/build main.tex`, exit 0. No multiply defined label and no error. No unknown number key in the four files; the last build lists four unknown keys (`margin_res_cap_lamQ_B`, `margin_res_phi_r0_B`, `margin_res_rQ_rN_B`, `margin_res_rU_rQ_B`), all in `appendix/A9_parameters.tex`, which another writer is editing. Every `\ref` and `\eqref` in the four files resolves. The undefined references in the log (`eq:a3-share`, `eq:derivatives`, `eq:order`, `eq:payoffs`) come from files outside this brief, which other writers are editing at the same time.
- Pages read in the PDF: 22 to 34 (Sections 5 to 8, Table 4, Figure 3, Table 5). No "??" on these pages. Every number prints through `\reg`.
- Language scan on the four files: 2 counted hits, 3 allowed tie-rule phrases. The two hits are "interval of strengths" in Proposition 4(d) and in its intuition; each sentence carries its condition (the hypotheses of part (d), and "When the exact recruitment margin rises up to the strength at which research reaches its cap"), so both stand. Before the fixes listed above the scan counted 10.
- A search of the four files for "benchmark", "research branch", \(r_U\), `res_rUR`, "buyer" (other than "the next buyer"), "now", hard-coded appendix numbers, "calibration", "main case", "no trade", "without informed trade", "threshold belief", "price spread" and "interval enclosure" finds nothing else.
