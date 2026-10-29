# Seminar slides (the /talk/ page)

The web version of the Beamer talk in `slot/manuscript/slides.tex` (the Overleaf deck), the seminar
talk for the order-slot version of the paper: 56 frames, the title, 19 numbered frames, then
backups B1 to B16 on 36 pages, with the same words, numbers, titles and links as the Beamer deck.
The planned speech is 33.5 minutes with the title, in a 45-minute slot.

## Open and present

The published slides are https://competition.dealextract.org/talk/ (published together with
the front page by `handout/publish.py`). Locally, open `dist/index.html` in a current desktop
browser. Fonts, equations and data are local; no network is required. For a local preview:

```sh
python3 -m http.server 8766 --bind 127.0.0.1 --directory presentation/dist
```

Open `http://127.0.0.1:8766/`. Press F for fullscreen when presenting.

- Right arrow, Space, PageDown: the next frame. Left arrow, PageUp: back.
- Home: title. End: conclusion. The main sequence stops at the conclusion, as the PDF does.
- A link button, or an inline link such as "B2" in a foot line, jumps to its backup. Back, or
  Escape, returns to the frame it came from. B2 has one return button for each of frames 11, 12
  and 13. Arrow keys inside the backups move between backup pages.
- O: overview of all 56 frames by part. N: speaker notes. G: notation. T: dark or light theme.
  F: fullscreen. R: reset the slide. ?: controls. A focused figure keeps its arrows.

The stage is a fixed 1600 x 900 design surface scaled to the window, so layouts are the same
on a laptop and a projector. The light theme is ink on white paper; the dark theme is slate, for a
dim room. The choice persists in the browser under the same key as the front page.

The two decks share words, numbers, frames, links and the journal look (`ccc-journal.sty` in
Beamer, `DESIGN.md` on the web). The Beamer deck has no click builds, and neither does this one.

## Content and design

`DESIGN.md` is the contract between the files. In short:

- `content.js` copies `slides.tex` frame by frame and is kept by hand, with the class for each
  Beamer macro (`DESIGN.md` section 11). A number is written with `H.q('key')` or `{{key}}`
  inside a formula and prints the registry display of its key, the string that `\reg{key}` prints
  in `slides.tex`. A rounded number is written with `H.q('key', 3)` or `{{key|3}}` and prints what
  `\regr{key}{3}` prints. The TikZ pictures (the timeline, the number lines, the proof steps, the
  order slot, the price levels) are SVG and HTML diagrams.
- `render.mjs` renders the slide records at build time: KaTeX for the mathematics, and a stop
  on any registry key the registry does not hold.
- `figdata.py` computes the curves of the four figures from the closed forms of the paper in
  the example. Primitives and boundaries come from registry keys.
- `charts.js` is the SVG renderer of the figures, a trimmed copy of the handout's; it holds no builders.
- `deck.js` is the engine: navigation, the link graph, panels and the figures.
- `deck.css` is the journal look of `DESIGN.md`: Libertinus Serif for text, Libertinus Sans for
  titles, tags and controls, white paper (slate in the dark theme), one oxblood accent and greys.
- The speaker notes are the spoken script, `slot/manuscript/slides_script.md`: one block for each
  main frame; a prepared answer goes to the first page of the backup it names.

Figures: frame 14 draws the threshold belief between the strong and the very strong incumbent
with the top belief; B3 draws the coexistence region with the example's path; B3, page 2 draws
entry in each equilibrium along the path; B12, page 2 draws research and total entry. They are
the figures of the Beamer deck, drawn from the same closed forms, with the same labels. Hover or
arrow keys over a figure give its values. No figure solves an equilibrium.

## Build and checks

```sh
python3 presentation/build.py
node presentation/check_deck.mjs
```

The build reads the slot registry, verifies the fonts against the deck's lock and KaTeX against the handout's lock,
renders the slides, computes the figure curves, reads the notes from the script, writes `dist/index.html`,
`dist/provenance.json` and `dist/speaker-notes.md`, and runs `check_deck.mjs`. Any failure stops
the build.

`check_deck.mjs` keeps the slides in step with `slides.tex` and its script. It compares the frame
order, labels and numbers (a backup page shows its `\BackupId`), the titles and subtitles, the
`\hypertarget` names, the link graph in source order with the button texts (link buttons, inline
links, return and Back buttons), the registry keys (each `\reg{key}` as often as `slides.tex`
prints it on the frame), the rounded numbers (`\regr{key}{digits}` must print the same string),
and the words outside mathematics and diagrams, in order, after NFKC normalisation. It also checks
that every number span names a registry key, that no example number appears before frame 14 (the
first frame the `slides.tex` header allows), that no number sits in a headline, that every backup
page has a Back or return button to a main frame, that the timing of each main frame and the
33.5-minute total are those of `slides_script.md`, and that every main frame has notes.

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

Headless Chrome prints all 56 frames to `dist/presentation.pdf` at
16 by 9 inches. The script opens the page with `?print=1`, which draws every figure and table
first. Headless Chrome can hang on some machines; the Beamer PDF of `slides.tex` is the printable
alternative. Inspect the rendered PDF after any edit.

These are presentation checks against existing research output. They do not rerun the
research acceptance gate and establish no new equilibrium or release-readiness claim.
Publication is the explicit action in `handout/README.md`.
