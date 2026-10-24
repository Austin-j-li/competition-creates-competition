# Seminar slides (the /talk/ page)

The web version of the Beamer talk in `talk/talk.tex`: all 47 frames in the Beamer order, with
the same titles, numbers and backup links. F0 to F16 (F10a and F10b share number 10), then the
backups A1 to A29. The content covers the benchmark paper only.

## Open and present

The published slides are https://competition.dealextract.org/talk/ (published together with
the handout by `handout/publish.py`). Locally, open `dist/index.html` in a current desktop
browser. Fonts, equations, data and both PDFs are local; no network is required. For a local
preview:

```sh
python3 -m http.server 8766 --bind 127.0.0.1 --directory presentation/dist
```

Open `http://127.0.0.1:8766/`. Press F for fullscreen when presenting.

- Right arrow, Space, PageDown: next reveal, then the next slide. Left arrow, PageUp: back.
- Home: title. End: conclusion. The main sequence stops at the conclusion, as the PDF does.
- A link button jumps to its backup. Back, or Escape, returns to the frame and the step it
  came from. Arrow keys inside the backups move between backups.
- O: overview of all 47 frames by part. N: speaker notes. G: notation. T: dark or light theme.
  F: fullscreen. R: reset the slide. ?: controls. A focused slider or figure keeps its arrows.

The stage is a fixed 1600 x 900 design surface scaled to the window, so layouts are the same
on a laptop and a projector. The light theme matches the Beamer deck; the dark theme suits a
dim room. The choice persists in the browser under the same key as the handout.

## Content and design

`DESIGN.md` is the contract between the files. In short:

- `content.js` copies `talk.tex` frame by frame and is kept by hand. Every number is written
  with a helper that names its registry key or the paper table it comes from.
- `render.mjs` renders the slide records at build time: KaTeX for the mathematics, and a guard
  that stops the build unless each number rounds from its registry value at the precision
  shown, or from the printed cell of the cited table.
- `deck.js` is the engine: navigation, reveals, the link graph, panels and the widgets.
- `deck.css` is the visual system: the moloch chrome of the Beamer deck in the UCL palette,
  Fira Sans for text and Fira Mono for numbers.
- Speaker notes come from `talk/script.tex`, one block per frame, keyed by the frame title.
  A9, A12, A25 and A29 have no block there; their notes come from `talk/structure-plan.md`,
  section 9.

Interactive parts: the F4 timeline shows each agent's information set; F5 highlights a case of
the payment table; F6, F8, A9, A14, A24 and A25 draw the paper's figure data with the handout's
SVG renderer (hover or arrow keys for values); F8 has a strength slider with closed-form
readouts; F11 switches between the equilibrium and the two information controls; F14
highlights a column; F7 and F13 open their footnotes on demand. No widget solves an
equilibrium.

## Build and checks

```sh
python3 presentation/build.py
node presentation/check_deck.mjs
```

The build binds the 16 research CSV sources through `handout/data.py`, verifies the fonts and
KaTeX against the handout's locks, renders the slides, reads the notes, writes
`dist/index.html`, `dist/provenance.json` and `dist/speaker-notes.md`, and runs
`check_deck.mjs`. Any failure stops the build.

`check_deck.mjs` keeps the slides in step with `talk.tex`. It compares the frame order and
labels, the titles and subtitles, the `\hypertarget` names, the link graph, and every number
that `talk.tex` tags with a `% source:` comment. A tagged number must appear on the web slide
in a span with the same registry key that rounds from the registry value; a formula reference
must carry its key; table numbers must appear. It also checks that status words come from the
paper's vocabulary, that every number span names a registry key or a paper table, that no
registry number sits in a headline unless `talk.tex` prints it there (the F10 titles), that every
notation symbol is defined on its slide or an earlier one, that the main frames follow the
timing plan (30.25 minutes before questions), and that every frame has notes.

In the browser, `DECK.selfCheck()` reports runtime errors, mathematics errors and the number
of number spans, and `DECK.audit()` walks every slide with all reveals shown and lists any body
that overflows the stage; it must return an empty list. `handout/check_browser.js` runs both
when given the slides address.

To change the talk: edit `talk/talk.tex` in Overleaf first, then the matching frame in
`content.js`, then rebuild. The check names every difference.

## PDF

With the preview server running:

```sh
presentation/export_pdf.sh
```

Headless Chrome prints all 47 slides with every reveal visible to `dist/presentation.pdf` at
16 by 9 inches. Headless Chrome can hang on some machines; the Beamer PDF of `talk.tex` is the
printable alternative. Inspect the rendered PDF after any edit.

These are presentation checks against existing research output. They do not rerun the
research acceptance gate and establish no new equilibrium or release-readiness claim.
Publication is the explicit action in `handout/README.md`.
