# S11, the slides

Report of the production assistant to the coordinator. Nothing is committed. One file changed: `slot/manuscript/slides.tex`. The builds went to a private folder outside the repository, and no build product is in the repository.

## Changed frames

Main frames, in talk order:

- **Q2, Q3, F1, F2:** "enter", "entrant" and "entered" become "prepare", "challenger" and "prepared". Entry is named once, in F1, as the probability that the challenger prepares. The benchmark sentences read "In the example" and "The example uses point masses".
- **F3:** the subtitle and the closing line read "in the example"; "entrant" becomes "challenger".
- **F5:** "Full orders at the example's prior".
- **F6:** retitled "The example: only incumbent strength changes"; the navigation button reads "Recruitment region"; the note "Inputs are not estimates from data" is removed.
- **F7:** "Bound check" becomes "Trading bound"; "no trade" becomes "quiet market".
- **F8:** "Threshold belief" becomes "Preparation threshold"; "ceiling" becomes "entry ceiling" three times; "top belief" becomes "top posterior".
- **F9 (Proposition 2):** "(H3) Ceiling at \(r_2\)" becomes "(H3) Exclusion condition"; part (i) reads "quiet market"; the ownership note gains the outbidding clause, that ownership rises and class \(H\)'s takeover share does not fall when class \(H\) outbids \(F_1\); "tie-rule pairs" becomes "all four tie rules"; the note on strict inequalities says the parts hold on an open set of inputs.
- **F10:** retitled "In the example, entry rises and then returns", with the subtitle "Corollary 1"; a line states the window of Corollary 1, \(\reg{u_lo_frac}<u<\reg{u_hi_frac}\), equivalently \(\tau(r_1)<M<\tau(r_2)\).
- **F11:** retitled "a stronger incumbent can only lower entry"; the direction column reads "constant"; "up to the entry ceiling".
- **F12, now Proposition 3.** Title "Quiet and informative markets coexist". Left: the region panel of the coexistence figure. Right: the general region (\(\pi<\tau\le M(\pi)\) and \(k/(1-\tau)\le\Delta_T\le k/[\rho\max\{\pi,1-\pi\}]\)), the uniqueness of the informative market, the rise of entry with the spread while class \(H\) mixes, and the meaning of the two bounds.
- **F12b, new, Corollary 2.** Title "In the example, coexistence runs from \(r_A\) to \(r_N\)". It holds the path panels (a) and (c) of the same figure, a legend line in the figure's colours (N, R, F, Q, T in words), and two bullets: coexistence on \([r_A,r_N]\); entry rises strictly on \([r_A,r_F]\), stays at \(\reg{entry_r1_B}\) up to the entry ceiling \(r_C\) and returns to \(\rho\) above it. The target `main:coex` and the navigation button "Marked strengths" moved to this frame, so the backup frame A8 returns to its single origin.
- **F13, Proposition 4 and Corollary 3.** The subtitle states the hypothesis, "at the prior \(1/2\)". The opening line states the general result (research rises with the spread up to the cap, and entry rises with research). The grey line states Corollary 3: zero research on \([r_0,r_N]\); recruiting research on \([r_R,r_C]\), below the cap until \(r_{\bar\lambda}\) and at the cap from there, entry rising from \(\reg{res_entry_rR}\) to \(\reg{res_entry_cap}\) and then constant; floor-entry research on \((r_N,r_Q)\) and on \((r_C,r_2]\). The old "branch runs on \([r_R,\bar r_R)\)" line and "Proposition 4(a)" are gone. The takeaway ends the story at the entry ceiling.
- **F14, F15:** appendix numbers follow the label map; "benchmark band case" becomes "the example's band"; "At \(B\)" becomes "In the example".
- **F16:** the entry bullet reads "with the price hidden, it can only lower them"; the spread bullet becomes the price-gap bullet (weighted impacts, entry component); the full-orders bullet becomes the informed-share bullet (full two-sided trade for \(r>r_S\); the sale impact and the mean order identify presence and prior); the winner bullet says "entry ceiling".
- **F17:** "at the benchmark" becomes "in the example".

Backup frames:

- **A2 (notation):** "benchmark class values" becomes "the example's class values"; "no entrant, \(H\) entrant, \(L\) entrant" becomes "no entry, a class \(H\) challenger, a class \(L\) challenger"; \(\tau(r)\) is the preparation threshold; the row for \(W_H(F)\) is added; "A.9" becomes "A.8".
- **A3:** "under all four tie rules".
- **A4:** "At the example's prior".
- **A5:** retitled "Recruitment and research regions in the example"; columns "Region" and "Example"; "Mass ratio \(u\) (Corollary 1)"; "Research cost \(a\) (Proposition A.1)"; "Top posterior"; the closing line says the regions are cut out by strict inequalities.
- **A6:** "A quiet market is the sole outcome".
- **A7:** retitled "in the example"; "a quiet market gives a flat price".
- **A8:** retitled "Marked strengths of the coexistence region"; columns "Strength" and "Value in the example"; the roles follow Corollary 2 (a quiet market ends at \(r_N\); mixed orders at the entry floor join the full purchase on \((r_N,r_J)\); the full purchase is alone from \(r_J\); \(r_C\) is the entry ceiling).
- **A9:** rewritten to Corollary 3, with the five marked strengths, the three equilibria and their intervals, the two equilibria at the three intermediate strengths, and the unique equilibrium at \(r_0\), \(r_1\), \(r_2\). The closing sentence on set-up choices is removed.
- **A10, A12:** appendix numbers follow the label map; "exclusion reserve" becomes "a reserve that excludes the low class".
- **A11:** the Laplace scale reads \(\xi\), and \(1+u=e^{2/\xi}\).

## Numbers from the label map

The map was built from `main.tex` and compared with the baseline `S0_label_map.md`. 23 labels changed, 15 appeared, one disappeared (`lem:a5-middle`). The slides use these:

| Slide text, before | After | Object |
|---|---|---|
| Proposition 4(a), Proposition 4(b) | Corollary 3 | research equilibria in the example |
| Mass ratio \(u\) (A.1) | Corollary 1 | recruitment and ownership in the example |
| Research cost (A.2) | Proposition A.1 | research parameter region |
| Proposition A.3 | Proposition A.2 | fixed information |
| (A.4) | (A.3) | preparation cost laws |
| (A.5), (A.6) | (A.4), (A.5) | value classes; many classes |
| (A.7) | (A.6) | complementary signals |
| Proposition A.8 | Proposition A.7 | access to prices |
| (A.9) | (A.8) | payment rule |
| (A.10) | (A.9) | reserves |
| Propositions A.11 to A.14 | Propositions A.10 to A.13 | empirical results |
| Lemma A.3 | Lemma A.3 | unchanged (trading bound) |

Propositions 1 to 4 keep their numbers. Corollaries 1, 2 and 3 are cited by their printed numbers. Every other hard-coded number is a structural constant (the slot bound \(\beta\le1/3\), the cost \(\tfrac a2\lambda^2\), the exponent \(2/\xi\)); every value of the example prints through `\reg`.

Keys added to the slides, all present in `numbers.tex`: `res_rC`, `res_rN`, `res_rQ`, `u_lo_frac`, `u_hi_frac`. The slide key list under `audit/slot_manuscript_2026_10_23/memos/` needs these five rows.

## Build

From `slot/manuscript`: `latexmk -xelatex -interaction=nonstopmode -outdir=<private folder>/sbuild slides.tex`. The result has 35 pages (the title, 21 main frames, the appendix divider and 12 backup frames), no overfull box, no unknown key and no undefined reference. Each frame with a changed figure was resized until the box warnings were gone.

The coexistence figure's slide version has three panels in one row, 10.2 by 3.3 inches, which scaled to the text width would print at about half size. The slides crop its panels from the one PDF: panel (b) alone on F12, panels (a) and (c) on F12b, and the legend as a text line in the figure's colours. A white patch covers the left edge of the neighbouring panel's label on F12. The main frames number 21 (the plan counted 20); the extra frame is F12b. The panel trims are fixed coordinates in points, set against the present layout of `coexistence_talk.pdf`, and the white patch sits at a fixed offset; a regenerated figure with another panel arrangement needs the trims reset. The legend colours on F12b are hex values sampled from the rendered figure (navy 1F3A6E, brick B4472E, grey 6C6C6C), not named colours from the figure code; they can be aligned with its palette.

## PNG review

I rendered the whole deck at 110 dpi and read every changed frame (including Q2, F13 after its subtitle change and A12), the new F12b and the backup frames, and read F12, F12b and F13 again at 130 and 140 dpi. Results:

- No text runs outside a frame, and no text sits on a figure.
- F12 and F12b show their panels at the size the other figure frames (F8) use, with tick labels and panel letters readable.
- F13's three lines under the figure fit; the figure height is reduced to make room.
- A9 holds seven bullets and the grey line without overflow.
- In panel (a) of the coexistence figure, the label "N" touches the dashed line of the threshold pair. That is figure code, which this stage does not change.

## Scan

`language_scan.py --no-doc --no-figcode --extra slot/manuscript/slides.tex` lists 17 lines. Each is judged:

- 1 "check" (Q1, "check the books"): ordinary meaning, kept.
- 15 bold defined terms and legend letters: the deck's own definitions (F1, F4) and the bold roman form letters N, R, F, Q, T of F12b; kept.
- 1 "no longer" (F16, "above the entry ceiling … orders no longer predict entry"): a comparative static across strengths, allowed by rule 3.
- 1 tie-rule phrase "may mix" (A3): an allowed tie-rule phrase.

The scan lists no "benchmark", status label, "no trade", "entrant", "admissible", "threshold" for a marked strength, or defensive hit. The whole file was read for the rule card: no status label, no "benchmark", no process word, no tool or model name.

## Left for later

- The key list memo (five rows, above).
- The slides' navigation, the notation frame and the appendix frames follow the statements of sections 2 to 8. The introduction and abstract, rewritten in parallel, are not cited by the slides.
