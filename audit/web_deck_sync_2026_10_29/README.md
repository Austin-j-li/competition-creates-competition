# Web slides brought to the Overleaf deck (29 October 2026)

The web slides (`presentation/` on `main`) now copy `slot/manuscript/slides.tex` frame by frame:
56 frames, the title, 19 main frames and 36 backup pages for B1 to B16, as in the PDF
`overleaf/slot/build/slides.pdf` (56 pages).

## Master used

`slides.tex` and `slides_script.md` of the Overleaf working copy at 76e1acd. That state contains the
author's Overleaf edit of 16:42 (f259a1f): the frame 10 title is "Strength lowers rival profit and
widens the spread". The copy in `slot/manuscript/` at ef225da still had the earlier title; the two
files were brought to 76e1acd. Nothing else differs.

## Files here

- `pdf_contact_sheet.png`: the 56 PDF pages (`pdftoppm -r 40`), from `pdf_pages/`.
- `web_contact_sheet.png`: the 56 web frames at 1440 x 900 in headless Chrome, light theme.
- `web_full/`: full-size web frames (five with a figure or diagram, the densest frame 5, the
  notation page B16, and two in the dark theme).
- `web_audit.json`: `DECK.audit()` (no frame overflows) and `DECK.selfCheck()` (no runtime or
  mathematics errors, 254 number spans) in both themes.
- `web_frame_texts.json`: the visible text of each web frame (MathML copies removed).
- `word_diff.txt`, `word_diff.json`: per frame, the words that only the PDF page has and the words
  that only the web frame has, after NFKC normalisation and lower case (word bags, because
  pdftotext reads table columns and figure labels out of reading order).

## Word differences and their reasons

Every frame: the PDF page text also holds the footline title "Competition Creates Competition"
(the web prints it too; the extraction drops it) and the total "19" (the web prints it with CSS).

| Kind | Frames | Reason |
|---|---|---|
| `p̄`, `μ̄`, `λ̄`, `f̄`, `r̄` split into a letter and a macron | S5, S7, S9, S16, S18, B1, B9, B10, B12, B12b, B12c, B13c, B16, B16b | KaTeX sets the bar accent as a separate glyph; the PDF sets one glyph |
| `W^1`, `W^0`, `r_1`, `δ_0` joined or split | S17, B2b, B4b, B10 | sub- and superscripts in KaTeX against Libertinus Math |
| `define b`, `2k and τ`, `ρκ Δ_T`, `is ρ` joined; `1/3` read as `31` | S11, S16, B3, B11b | `\quad` and `\text{}` spacing inside one formula; KaTeX puts a fraction's denominator first in the page text |
| enumerate numbers `1 2 3` | S4, B11b, B13 | Beamer prints them as text; the web as list markers |
| figure labels in the PDF only (`592659`, `quiet`, `payoff spread`, `research intensity`, duplicate axis titles, legend words) | S14, B3, B3b, B12b | the PDF text layer keeps the labels that `\FigCover` patches hide and the legend that the trim clips; the visible labels match the web figure |

No other word differs. The parity check in `presentation/check_deck.mjs` compares the words of
each frame outside mathematics and diagrams with `slides.tex` in order and reports none.

## Open

- The PDF text layer of frames 14, B3, B3 page 2 and B12 page 2 keeps the old figure labels
  under the cover patches, including "quiet market"; `pdftotext slides.pdf | grep quiet` finds
  them. Regenerating the talk figures with the new labels would remove them.
- The `slides.tex` header comment still says "The website keeps the ruled design of DESIGN.md";
  it is Overleaf-owned and was left unchanged.
- The Overleaf working copy is three commits ahead of its remote (76e1acd); nothing was pushed.
