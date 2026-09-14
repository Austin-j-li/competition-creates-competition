# Interactive research presentation

A 40-minute seminar talk: 22 main slides in six blocks and seven technical discussion
slides. The content covers the benchmark paper only. The endogenous-insider fork is excluded.

## Open and present

The published talk is https://competition.dealextract.org/talk/ (published together with
the handout by `handout/publish.py`). Locally, open `dist/index.html` in a current desktop
browser. Fonts, equations, data, the working
paper and the Online Appendix are local; no network is required. For a local preview:

```sh
python3 -m http.server 8766 --bind 127.0.0.1 --directory presentation/dist
```

Open `http://127.0.0.1:8766/`. Press F for fullscreen when presenting.

- Right arrow / Space: next reveal, then next slide.
- Left arrow: undo a reveal, then previous slide.
- O: slide overview. N: speaker notes. G: notation. T: projector theme. F: fullscreen.
- R: reset the current slide's interaction and reveals.
- Escape: close a panel or return from a technical slide.
- Home / End: title / close. A focused slider keeps its arrow keys.

The deck is a fixed 1600 x 900 design surface scaled to the window, so layouts are identical
on a laptop and a projector. The default theme ("After hours", blue-black with amber) suits a
dim room or a screen share; the projector theme (warm off-white, same identity) is for a lit
seminar room. The choice persists in the browser. Speaker notes open in a dialog on the
presentation screen; `dist/speaker-notes.md` carries the same notes for a second device.

## Content and design

`DESIGN.md` is the contract between the three deck files: slide record, chrome markup, class
vocabulary, widget ids, tokens, type scale, motion, and the arc with acts, statuses and
minutes. `content.js` owns slide copy, speaker notes, sources and timing. `deck.js` owns
navigation, the stage, and the widgets. `deck.css` owns the visual system and print.

The talk runs in six blocks: the question (institution, myth, research question; 7 min),
one qualitative preview of the mechanism and the antecedents (2.5), the model with
progressive notation (8.5), two equilibrium slides (what an equilibrium is; what the price
reveals; 5), the propositions visualised with two controls (14), and robustness and next
steps (3.5). The literature is placed twice: the entry and deterrence papers as the myth,
the feedback papers after the preview as the increment. Registry numbers appear on main
slides only as annotations inside a result figure or in the robustness table, labelled "at
the declared benchmark"; never as a headline. Seven widgets are live: the preview value
line, the auction value line, the incumbent-strength dial, the order-flow tape, the two
economies, the fixed-information control, and the bargaining weight. Every number comes from
the bound registry or from the benchmark closed forms in `handout/explorer.js`; no widget
solves an equilibrium.

Notation is progressive. `content.js` exports a glossary (41 symbols: LaTeX, meaning, group,
and a pattern that matches the symbol in LaTeX source). Each model slide carries a
definition strip rendered from that glossary for the symbols it introduces; the G key opens
the full grouped table; backup slide B6 prints it. `check_deck.mjs` fails the build if any
symbol appears in slide LaTeX before the slide that defines it.

Result status appears as a stamp in each slide's footer using the paper's vocabulary:
analytical, computer-assisted, numerical diagnostic, open; declarations are stamped
"declaration". The hedges that qualify each result live in the speaker notes and the source
line, not in slide copy. Each note ends with an "If asked" line for the question a theorist or
the supervisor is likely to raise.

Type: Instrument Serif for titles, statements and metrics; JetBrains Mono for numbers, ticks,
kickers and stamps; Atkinson Hyperlegible for running text, chosen for width and legibility
at distance. The faces are self-hosted under `vendor/uifonts/` with their SIL Open Font
License texts and a hash lock.

## Build and checks

```sh
python3 presentation/build.py
node presentation/check_deck.mjs
```

The build verifies KaTeX and every font against their locks, binds 16 research CSV sources
through `handout/data.py`, fills the template, writes `dist/speaker-notes.md` from the slide
records, and records source hashes in `dist/provenance.json`. `check_deck.mjs` confirms the
slide records satisfy `DESIGN.md`: ids, acts, statuses, widget elements, the "If asked"
lines, no hedge in slide copy, no registry number in a headline element, the notation rule,
and 40 minutes over the main slides. In the browser,
`DECK.selfCheck()` reports formula, equation and runtime status, and `await DECK.audit()`
walks every slide with all reveals shown and lists any body that overflows the stage or any
column whose content is wider than the column; it must return an empty list.

## PDF

With the preview server running:

```sh
presentation/export_pdf.sh
```

Headless Chrome prints all 29 slides with every reveal visible, in the projector theme, to
`dist/presentation.pdf` at 16 by 9 inches. The interactive slides print their deterministic
comparison state. Inspect the rendered PDF after any edit.

These are presentation checks against existing research output. They do not rerun the
research acceptance gate and establish no new equilibrium or release-readiness claim. The
paper and handout are unchanged. Publication is the explicit action in `handout/README.md`.
