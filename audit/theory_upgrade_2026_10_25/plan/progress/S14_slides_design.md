# S14 slides design — 26 October 2026

The Beamer deck `slot/manuscript/slides.tex` uses the ruled-document design of the web deck.

## Theme

- **Base and colours:** moloch and its purple palette are replaced by plain Beamer with the ruled tokens: paper `#FBFCFC`, ink `#1E2530`, muted grey `#5B6573`, hairline `#C7CDD5`.
- **Concept colours:** `#B54B00` marks the spread and information, and `#006459` marks the costs. Both appear only in figures and their keys.
- **Frame titles:** set in Archivo with a 2 pt ink rule beneath. There is no fill and no progress bar.
- **Footline:** the short title and the frame number, in muted grey.
- **Other elements:** bullets are short ink dashes, tables use hairline rules, and blocks have no fill. The title page has a 2 pt rule above the title and hairlines below it.

## Fonts

- STIX Two Text and STIX Two Math come from TeX Live.
- Archivo (Regular, Medium, SemiBold, Bold, Italic and SemiBold Italic) is in `slot/manuscript/fonts/` with its OFL licence. It is loaded through fontspec's `Path`, so the deck compiles on Overleaf.
- Every font is embedded.

## Figures

- The slide figures (`figures/*_talk.pdf`) set their text in Archivo. Axes and in-figure text are ink, tick labels are muted grey, and the face colour is the slide paper colour, so no box shows on the slide.
- The paper figures are byte-identical to their previous versions.

## Fit

- Six frames ran past the bottom by 2.5 to 9.7 pt: F9, F12, F12b, F13, F16 and A8. Each now uses Beamer's `shrink` option (2 to 8 per cent). No words, numbers or frame order changed.

## Builds

- `latexmk -xelatex slides.tex`: exit 0, 35 pages, 0 overfull boxes.
- `presentation/build.py` and `check_deck.mjs`: the web deck matches `slides.tex` and the deck contract.
