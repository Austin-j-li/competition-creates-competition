# Seminar slides (the /talk/ page)

The web version of the Beamer talk in `slot/manuscript/slides.tex`, the seminar talk for the
order-slot version of the paper: 43 frames, the title, 26 numbered slides, then backups B1 to B12
on 16 pages, with the same titles, numbers and backup links as the Beamer deck.

## Open and present

The published slides are https://competition.dealextract.org/talk/ (published together with
the front page by `handout/publish.py`). Locally, open `dist/index.html` in a current desktop
browser. Fonts, equations and data are local; no network is required. For a local preview:

```sh
python3 -m http.server 8766 --bind 127.0.0.1 --directory presentation/dist
```

Open `http://127.0.0.1:8766/`. Press F for fullscreen when presenting.

- Right arrow, Space, PageDown: next reveal, then the next slide. Left arrow, PageUp: back.
- Home: title. End: conclusion. The main sequence stops at the conclusion, as the PDF does.
- A link button jumps to its backup. Back, or Escape, returns to the slide and the step it
  came from. Arrow keys inside the backups move between backups.
- O: overview of all 43 frames by part. N: speaker notes. G: notation. T: dark or light theme.
  F: fullscreen. R: reset the slide. ?: controls. A focused slider or figure keeps its arrows.

The stage is a fixed 1600 x 900 design surface scaled to the window, so layouts are the same
on a laptop and a projector. The light theme is ink on white paper; the dark theme is slate, for a
dim room. The choice persists in the browser under the same key as the front page.

The two decks share words, numbers, frames and links but not their look. By rule, the Beamer deck
in Overleaf uses a classic Beamer theme (Madrid, `slot/manuscript/ccc-classic.sty`); this web deck
keeps the ruled design of the website.

## Content and design

`DESIGN.md` is the contract between the files. In short:

- `content.js` copies `slides.tex` frame by frame and is kept by hand. A number is written with
  `H.q('key')` or `{{key}}` inside a formula and prints the registry display of its key, the string
  that `\reg{key}` prints in `slides.tex`. A rounded number is written with `H.q('key', 3)` or
  `{{key|3}}` and prints what `\regr{key}{3}` prints.
- `render.mjs` renders the slide records at build time: KaTeX for the mathematics, and a stop
  on any registry key the registry does not hold.
- `figdata.py` computes the curves of the five figures from the closed forms of the paper in
  the example. Primitives and boundaries come from registry keys.
- `charts.js` is the SVG renderer of the figures, a trimmed copy of the handout's; it holds no builders.
- `deck.js` is the engine: navigation, reveals, the link graph, panels and the widgets.
- `deck.css` is the visual system, the ruled document of the front page: ink on cool white paper
  (slate in the dark theme), Archivo for titles, tables, figures and controls, STIX Two Text for
  prose, two rule weights, no fills, cards, pills or shadows. Controls are text with an underline.
- `notes.md` holds the speaker notes, one block per frame, headed `## LABEL | timing`.

Exhibits (figures, tables, the timeline, the order-slot flow) span the content column; prose and
captions stop at the text measure.

Interactive parts: on slide 10, a click or Enter highlights a case of the payment table; slide 13
draws the ceiling and the floor of the gain from a correct order against the order cost, with
symbols only; slide 16 draws the threshold belief against strength, and a strength slider moves a
cursor along the curve; on slide 18, a click or Enter selects a row of the entry table (the full
model or one of the two information controls), and bars draw its two entries; slide 19 draws the
coexistence region with the example's path; slide 20 draws entry in each equilibrium; slide 22
draws research and entry in each research equilibrium; backup B2 builds the notation table. No
widget solves an equilibrium. Hover or arrow keys over a figure give its values, except on slide
13, which shows no values.

## Build and checks

```sh
python3 presentation/build.py
node presentation/check_deck.mjs
```

The build reads the slot registry, verifies the fonts against the deck's lock and KaTeX against the handout's lock,
renders the slides, computes the figure curves, reads the notes, writes `dist/index.html`,
`dist/provenance.json` and `dist/speaker-notes.md`, and runs `check_deck.mjs`. Any failure stops
the build.

`check_deck.mjs` keeps the slides in step with `slides.tex`. It compares the frame order and
labels, the titles and subtitles, the `\hypertarget` names, the link graph, and the registry keys:
every `\reg{key}` that `slides.tex` prints on a frame must be a number span with that key on the
web frame, and every `\regr{key}{digits}` must print the same rounded string. It also checks that
every number span names a registry key, that no example number appears before slide 16, that no
number sits in a headline, that every notation symbol is defined on its slide or an earlier one,
that the main slides follow the timing plan (45 minutes with the title), and that every frame has
notes.

In the browser, `DECK.selfCheck()` reports runtime errors, mathematics errors and the number of
number spans, and `DECK.audit()` walks every slide with all reveals shown and lists any body that
overflows the stage; it must return an empty list.

To change the talk: edit `slot/manuscript/slides.tex` in Overleaf first, then the matching frame in
`content.js`, then rebuild. The check names every difference.

## PDF

With the preview server running:

```sh
presentation/export_pdf.sh
```

Headless Chrome prints all 43 frames with every reveal visible to `dist/presentation.pdf` at
16 by 9 inches. The script opens the page with `?print=1`, which draws every figure and table
first. Headless Chrome can hang on some machines; the Beamer PDF of `slides.tex` is the printable
alternative. Inspect the rendered PDF after any edit.

These are presentation checks against existing research output. They do not rerun the
research acceptance gate and establish no new equilibrium or release-readiness claim.
Publication is the explicit action in `handout/README.md`.
