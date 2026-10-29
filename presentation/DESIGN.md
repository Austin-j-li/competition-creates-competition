# Slides design contract (the journal look)

The visual system (tokens, type, rules, components, the one-accent rule and the slop list) is
`DESIGN.md` at the repository root, shared with the research brief page. This
file is the contract between the slide files; where it quotes a value, the root `DESIGN.md` is the
source.

The contract between the slide files: `content.js` (the frames), `render.mjs` (build-time
rendering and the registry keys), `figdata.py` (the figure curves), `deck.js` and `template.html`
(the engine), `charts.js` (the SVG renderer), `deck.css` (the visual system), the speaker script
`slot/manuscript/slides_script.md` (the notes) and `check_deck.mjs` (the drift check). Change this file before you change a name in it.

## 1. Brief

The web version of `slot/manuscript/slides.tex`, the Beamer deck of the order-slot seminar talk in
Overleaf (33.5 planned minutes of speech with the title, in a 45-minute slot). All 56 frames stay in
the Beamer order: the title, 19 numbered frames and 36 backup pages for backups B1 to B16. The look
is the journal look of the Beamer deck (`ccc-journal.sty`, chosen by the author on 29 October 2026),
shared with the research brief page: Libertinus Serif for the body, Libertinus Sans for titles,
tags, labels and the footline, white paper, one oxblood accent (#7A1F1F) and greys; no bars, fills,
cards, pills, shadows or gradients. A frame is a bold sans title over an accent rule, the body,
the takeaway or intuition pinned above the foot zone, grey pointer lines, and a footline with the
short title in small capitals, the link buttons and the frame number. Words, numbers, frames and
links stay identical between the two decks. Section 11 names the class for each Beamer macro. The
Beamer deck has no click builds; the web frames have none either.

Invariants:

- Offline. Fonts, KaTeX and data are local. No network at runtime.
- `slides.tex` is the master. Titles, subtitles, hypertargets, link buttons, inline links and the
  words outside mathematics are copied from it; `check_deck.mjs` fails on any difference it can see.
- Every number is the `display` of a row in
  `audit/slot_manuscript_2026_10_23/registry/registry.csv`, the string that `\reg{key}` prints in
  `slides.tex`. A rounded number is that value rounded as `\regr{key}{digits}` prints it, and both
  decks print the same string. The build stops on a key the registry does not hold. No decimal is
  typed into a slide. No registry number appears before frame 14, as the `slides.tex` header states.
- No status labels. The registry's status column is never read, shown or embedded.
- The accent is the only chrome colour: the rule under a title, the rule above a statement or a
  takeaway, tags, bullets, the active rail entry or control, the link buttons and the focus ring.
  Figures and diagrams draw in ink (`--chart-1`, `--c-cost`), the accent (`--chart-2`, `--c-info`)
  and greys (`--chart-3`), told apart by dash and marker; the orange and teal of the Beamer
  figures map to the accent and ink. Nothing else is coloured, and `check_deck.mjs` fails on a hex
  outside the journal palette.
- Controls share one grammar: sans text with an underline. The active choice is accent at weight
  700 with a 2 px accent underline (the rail, the pager). A link button on a slide is the Beamer
  button: accent text on a light grey rounded ground with a triangle. An inline link is the text
  with a faint underline.
- Registry numbers keep their provenance hover, marked by a faint dotted hairline.
- The curves of the figures are closed forms of the paper in the example, computed at build time
  from registry primitives; no widget solves an equilibrium.

## 2. The helper contract (content.js)

`window.createDeck(H)` returns `{ frames, notation }`. `H` comes from the renderer or the check,
never from `content.js`.

| Helper | Meaning |
|---|---|
| `H.m(latex)`, `H.d(latex)` | inline and display mathematics. `{{key}}` or `\reg{key}` inside the formula prints the registry display of `key`; `{{key\|3}}` prints the value rounded to three decimals, as `\regr{key}{3}` does; `\reg{key}` keeps a subtitle identical to its `slides.tex` text. |
| `H.q(key[, digits])` | a registry number in running text: the display that `\reg{key}` prints, or with `digits` the rounded value that `\regr{key}{digits}` prints |
| `H.v(key)` | the registry value as a number, for layout only, never before frame 14 |
| `H.go(target, text)` | a link button to a `\hypertarget` name, as `\hyperlink{target}{\beamergotobutton{text}}` |
| `H.back(target[, text])` | a return button: `\BackButton{target}` prints "Back", `\beamerreturnbutton{text}` prints its text |
| `H.link(target, text)` | an inline text link, as `\hyperlink{target}{text}` |
| `H.endFrame(label)` | optional; called after each frame is built, so the renderer can attribute messages |

## 3. Frame record

```js
{ id, label, num, part, title, short, subtitle, targets, minutes, widget, body, backup, origin, cls }
```

- `id`: `f0` for the title, `s1` to `s19`, and the lower-case label of a backup page (`b1`, `b2b`,
  `b11s`). `label`: the `slides.tex` label (`S0` to `S19`, `B1` to `B16` with their page labels
  `B2b`, `B3b`, `B3c`, `B4b`, `B6b`, `B6c`, `B8s`, `B8b`, `B11s`, `B11f`, `B11b`, `B11c`, `B11d`,
  `B12b`, `B12c`, `B12d`, `B13b`, `B13c`, `B14b`, `B16b`).
- `num`: the Beamer frame number of a main frame (the title is 0) and the `\BackupId` of a backup
  page (B11s shows B11).
- `part`: 1 to 6 for the main frames, `B` for backups (section 7).
- `title`: the `slides.tex` title argument verbatim; `$...$` is mathematics. `short` names the title
  frame (`Title`).
- `subtitle`: HTML built with the helpers; its plain text equals the `\framesubtitle`.
- `targets`: the frame's `\hypertarget` names, in order.
- `minutes`: the timing line of the frame in `slides_script.md`; backups 0.
- `widget`: the figure on the frame (section 5); empty for the others.
- `backup`, `origin`: backups and the frame of their first Back or return button.
- `cls`: extra classes on the slide: `bigtitle` (frame 1, \LARGE), and the body size of a frame
  that does not use `\Body`: `sz-n` (\normalsize), `sz-f` (\footnotesize), `sz-x` (\scriptsize).

## 4. Markup

Chrome (`template.html`): a tools bar `nav.hud` (`#overview`, `#notes`, `#notation`, `#theme`,
`#fullscreen`, `#help`, and a link back to the research brief), the stage `main#stage >
#deck`, the rail `footer.rail-bar` (`#rail`, `#return`, `#previous`, `#counter`, `#next`,
`#progress-label`), a dialog `#panel` and a live region `#announcer`.

The build writes one section per frame:

```html
<section class="slide" id="s13" data-label="S13" data-num="13" data-part="3" data-title="…"
         data-minutes="1.5" data-widget="gain" data-targets="">
  <header class="slide-head"><h2>…</h2><p class="sub">…</p></header>
  <div class="slide-body">…</div>
  <footer class="slide-foot"><span class="foot-title">…</span><span class="foot-num">13</span></footer>
</section>
```

The title frame adds the class `title-slide` and holds only its body (`.cover`). Backups add the class
`backup`, `data-backup="true"` and `data-origin`. The `cls` of a frame is added to its classes. The
build gives a frame without a title the class `nohead` and no header; no frame uses it now.
The engine still supports reveals (`data-step="n"`: an element is shown from step n on); no frame
uses them, because the Beamer deck has no click builds. Number
spans are `span.q` (`data-q` holds the registry key, or several keys for a formula, and the
`title` reads `key = display`); formula numbers add `.q-tex`; rounded numbers add `data-round`.
Link buttons are `button.goto[data-target]`; inline links are `a.xlink[data-target]`; Back and
return buttons are `button.goto.back[data-back]`.

Class vocabulary for the body: the frame skeleton of section 11; `.jcols > .jcol` (Beamer
columns and minipages, each with its width as a percentage); `.jcenter`; tables `table.tj` with the
size classes `.fs-s`, `.fs-f`, `.fs-x` and the `\arraystretch` classes `.stretch-098` to
`.stretch-135`, `tr.mid` for a `\midrule`; `.vfill` and `.vsp` (`\vfill` and `\vspace`);
`.diagram` around a TikZ picture (`.dg-svg`, `.timeline`, `.pflow > .fbox.pbox`, `.sflow > .fbox`);
`.figure.plain` for a figure; `.refs2`; `.roadline`; `.cover`.

## 5. Widgets

| `widget` | Frame | Elements | Behaviour |
|---|---|---|---|
| `title` | S0 | `.cover` | static title page |
| `beliefs` | S14 | `#beliefs` | the threshold belief τ(r) from r_1 to r_2, the top belief M(1/2), the band from τ(r_1) up to it, and the values τ(r_2), M(1/2), τ(r_1) from the registry: panel (b) of the belief figure of `slides.tex` |
| `region` | B3 | `#region` | panel (b) of the coexistence figure: the region of Proposition 3 at the prior in the plane of Δ_T and τ, with the example's path through r_0, r_A, r_F, r_N |
| `coex` | B3b | `#coex` | panels (a) and (c) of the coexistence figure: entry in each equilibrium against strength, the whole path and the marked strengths r_A, r_F, r_N, r_J, r_S, with the band [r_A, r_N] |
| `research` | B12b | `#research` | research (a) and total entry (b) along the path in zero, recruiting and floor-entry research, with r_R, r_λ̄, r_N, r_Q and r_C and the example strengths marked |

Axis, line and annotation labels are those of the Beamer figures. Figures draw with
`CCC.charts.draw` from `charts.js` (a trimmed copy of the handout's SVG renderer) at a zoom of 1.4,
so text reads at a distance. The curves come from `window.CCC_DATA.fig`, written by `figdata.py`.
`?print=1` in the address draws every figure before printing; `export_pdf.sh` uses it.

## 6. Tokens and type

```css
:root { --bg:#ffffff; --page:#e9e9e9; --ink:#1c1c1c; --muted:#666666; --line:#c9c9c9; --grid:#e6e6e6;
  --rule:#7a1f1f; --accent:#7a1f1f; --c-info:#7a1f1f; --c-cost:#1c1c1c;
  --chart-1:#1c1c1c; --chart-2:#7a1f1f; --chart-3:#666666;
  --font-serif:"Libertinus Serif","Libertinus Math",Georgia,serif;
  --font-sans:"Libertinus Sans","Libertinus Math",system-ui,Arial,sans-serif }
```

The dark theme is slate paper (#171717, ink #ebebeb, muted #a3a3a3, hairline #474747) with the
accent lightened to #d4908f; it has no tint and no glow. The faces are the deck's locked files
(`presentation/fonts.lock.json`, identical to `handout/fonts.lock.json`): Libertinus Serif 400 and
700 with italics, Libertinus Sans 400 and 700 with the regular italic, and Libertinus Math subset
to the symbol blocks as the fallback for arrows, relations and operators. `build.py` writes the
`@font-face` rules and embeds the font data so the staged deck carries its own faces. Mathematics
is KaTeX at 0.95 em, close to the size of Libertinus Math in the Beamer deck; the seam with Libertinus is accepted.

Type scale at 1600 x 900, where 1 pt of the 16:9 Beamer page is 3.5 px. Libertinus Sans: frame
title 50 px at weight 700 (60 px on S1, `.bigtitle`, the \LARGE of the deck); statement tag 30 px
in the accent; link buttons 20 px; the footline 23 px in small capitals; figure
text 12.5 to 20 px drawn at a zoom of 1.4. Libertinus Serif: the title frame 60 px at 700; body
32 px at line height 1.22 (\Body, the 11 pt baseline of 9 pt type); \normalsize 35 px; subtitle 27 px italic muted; statement body and gloss 28 px;
small 28 px, xs 25 px; foot lines 23 px muted; takeaway 32 px at 700 over a 3 px accent rule;
intuition 32 px italic over a hairline; the large line 42 px at 700. Paragraphs are 6 px apart. Tables are set in the text face at the size of their block. Body padding 12 px 40 px (the 0.4 cm text margin of the deck).

## 7. Parts

The parts follow the roadmap line of frame 4.

| Part | Name | Frames |
|---|---|---|
| 1 | Question | S0 to S4 |
| 2 | Model | S5 to S9 |
| 3 | Mechanism and main result | S10 to S14 |
| 4 | Fixed-information control | S15 |
| 5 | Extensions and prediction | S16 to S18 |
| 6 | Conclusion | S19 |
| B | Backups | B1 to B16 on 36 pages |

Links, origins and hypertargets are those of `slides.tex`; `check_deck.mjs` compares them in
source order. Every main frame carries `main:s<n>`; the first page of a backup carries
`app:b<n>`; a continuation page repeats the title and carries a Back button but no hypertarget.
Not every Back target links to its backup (B5, B7, B8, B9, B15 and B16 are reached from the
overview); a Back button always names a main frame.

## 8. Notation

`notation` holds the rows of the two B16 pages (symbol, gloss, first defined). The B16 tables and
the notation panel (G) render from it. The order in which symbols are introduced is that of
`slides.tex`; the word check keeps the web frames in that order.

## 9. Data

`window.CCC_DATA` holds `registry` (the key, value and display of every key the slides print or the
figures place, and nothing else) and `fig` (the curves and the example's inputs for the figures).
`window.CCC_DECK` holds the frame list, the parts, the notation rows, the total of numbered frames,
the planned minutes and the planned-speech line of the script; `window.CCC_NOTES` holds the
speaker notes by label, from `slot/manuscript/slides_script.md`.

## 10. Timing plan

The timing line of each frame in `slot/manuscript/slides_script.md`: the title 0.5; frames 1 to 4:
2.5, 1.5, 1.0, 1.5; frames 5 to 9: 1.5, 2.0, 2.0, 2.0, 1.5; frames 10 to 13: 2.0, 1.5, 1.5, 3.0;
frames 14 and 15: 1.5, 2.0; frames 16 to 19: 1.5, 1.5, 1.5, 1.5. Prepared speech 33.5 minutes;
questions 11.5 minutes within the 45-minute slot. `check_deck.mjs` reads the script, so this list
only restates it.

## 11. The class for each Beamer macro

The macros of `ccc-journal.sty` and the class that prints the same thing on a web frame.
`content.js` uses these; `deck.css` holds the rules.

| Beamer | Web | Prints as |
|---|---|---|
| `\Body` | the default size of `.slide-body` (32 px); `.small` is \footnotesize, `.xs` is \scriptsize | the body of a main frame |
| `\begin{Statement}{tag}` | `<div class="statement"><p class="statement-tag">tag</p> ... </div>` (`.resultbox` with `.resultbox-title`, and `.propblock`, print the same way) | an accent rule, a bold sans tag in the accent, the body one size down, a light rule |
| `\begin{DefList}` and `\DefRow{label}{text}` | `<dl class="deflist"><dt>label</dt><dd>text</dd> ... </dl>` (`.deflist.narrow` for a 220 px label column) | a label column: bold sans labels on the left, text on the right |
| `\ColHead{head}` | `<b class="colhead">head</b>` at the top of a column (`.rcol > b:first-child` and `.rpanel > b` print the same way) | a bold sans head in the accent over an accent rule |
| `\RuledCol{text}` | `<div class="ruledcol">text</div>` | a column that opens with an accent rule |
| `\Intuition{text}` | `<p class="intuition">text</p>` as a late child of `.slide-body` | pinned above the foot zone: a light rule, then the italic sentence |
| `\TakeawayEnd{text}` (and `\Takeaway`) | `<p class="takeaway">text</p>` as a late child of `.slide-body` | pinned above the foot zone: an accent rule, then the bold line |
| `\FootLine{text}`, `\SmallLine{text}` | `<div class="footzone"><p class="footline">text</p></div>` (`p.foot` and `p.smallline` print the same way) | grey pointer lines in small type at the foot of the body |
| `\Gloss{text}`, `\GrayLine{text}` | `<p class="gloss">text</p>` (`.grayline` prints the same way) | a grey sentence one size down |
| `\LargeLine{text}` | `<p class="largeline">text</p>` (`p.bigline` prints the same way) | one large bold statement between an accent rule and a light rule |
| `\NavyRule` | `<hr class="rule-accent">` | a rule in the accent |
| `\LightRule` | `<hr class="rule-light">` | a light hairline |
| `\ModelStrip{3,4}` | `<ul class="model-strip"><li>Players</li>...<li class="current">Information</li>...</ul>` under the head | the six parts of the model; the current ones bold accent, the others grey |
| `\framesubtitle` | `subtitle` of the frame record (`p.sub`) | serif italic in grey between the title and the accent rule |
| `\PlaceNav`, `\beamergotobutton`, `\BackButton` | `H.go(target, text)` and `H.back(target)` inside `.nav` (`.goto`, `.goto.back`) | the Beamer button in the footline: accent text on a light rounded ground with a triangle |
| `\BackupId{B1}` and the frame number | `.foot-num` (the build writes the number or the label; `deck.js` adds `data-total` on a main frame) | `n / N` on a main frame, the label on a backup, nothing on the title frame |
| `\titlepage` | `.cover` with `h1`, `.cover-author`, `.cover-inst` | a short accent rule, the serif title, the author and the department in sans |
| `columns`, `minipage` | `.jcols > .jcol` with the width of the Beamer column | columns side by side; the rest of the width is the gap |
| `tabular` with booktabs | `table.tj` (column widths in px: 1 cm of the page is 100 px) | rules above and below the head and at the end, no row rules, the head in the text face |
| `tikzpicture` | an SVG or HTML diagram inside `.diagram` | the same nodes, labels and arrows in ink, the accent and greys |
