# Slides design contract (the journal look)

The visual system (tokens, type, rules, components, the one-accent rule and the slop list) is
`DESIGN.md` at the repository root, shared with the research brief page. This
file is the contract between the slide files; where it quotes a value, the root `DESIGN.md` is the
source.

The contract between the slide files: `content.js` (the frames), `render.mjs` (build-time
rendering and the registry keys), `figdata.py` (the figure curves), `deck.js` and `template.html`
(the engine), `charts.js` (the SVG renderer), `deck.css` (the visual system), `notes.md` (the speaker notes) and `check_deck.mjs`
(the drift check). Change this file before you change a name in it.

## 1. Brief

The web version of `slot/manuscript/slides.tex`, the Beamer deck of the order-slot seminar talk
(45 planned minutes, the title included). All 43 frames stay in the Beamer order and
organisation: the title, 26 numbered slides and 16 backup pages for backups B1 to B12. The look is
the journal look of the Beamer deck (`ccc-journal.sty`, chosen by the author on 29 October 2026),
shared with the research brief page: Libertinus Serif for the body, Libertinus Sans for titles,
tags, labels and the footline, white paper, one oxblood accent (#7A1F1F) and greys; no bars, fills,
cards, pills, shadows or gradients. A frame is a bold sans title over a 3 px accent rule, the body,
the takeaway or intuition pinned above the foot zone, grey pointer lines, and a footline with the
short title in small capitals, the link buttons and the frame number. Words, numbers, frames and
links stay identical between the two decks. Section 11 names the class for each Beamer macro.

Invariants:

- Offline. Fonts, KaTeX and data are local. No network at runtime.
- `slides.tex` is the master. Titles, subtitles, hypertargets and link buttons are copied from it;
  `check_deck.mjs` fails on any difference it can see.
- Every number is the `display` of a row in
  `audit/slot_manuscript_2026_10_23/registry/registry.csv`, the string that `\reg{key}` prints in
  `slides.tex`. A rounded number is that value rounded as `\regr{key}{digits}` prints it, and both
  decks print the same string. The build stops on a key the registry does not hold. No decimal is
  typed into a slide.
- No status labels. The registry's status column is never read, shown or embedded.
- The accent is the only chrome colour: the rule under a title, the rule above a statement or a
  takeaway, tags, bullets, the active rail entry or control, the link buttons and the focus ring.
  Figures draw in ink (`--chart-1`, `--c-cost`), the accent (`--chart-2`, `--c-info`) and greys
  (`--chart-3`), told apart by dash and marker. Nothing else is coloured, no UCL colour appears, and
  `check_deck.mjs` fails on a hex outside the journal palette.
- Controls share one grammar: sans text with an underline. The active choice is accent at weight
  700 with a 2 px accent underline (the rail, the choice buttons, the pager). A link button on a
  slide is the Beamer button: accent text on a light grey rounded ground with a triangle. A
  switched-off legend entry is struck through.
- Exhibits (figures, tables, the timeline, the order-slot flow) span the content column; prose and
  captions stop at the text measure. Registry numbers keep their provenance hover, marked by a
  faint dotted hairline; numbers in prose are Libertinus Serif with tabular figures.
- The curves of the figures are closed forms of the paper in the example, computed at build time
  from registry primitives; no widget solves an equilibrium.

## 2. The helper contract (content.js)

`window.createDeck(H)` returns `{ frames, glossary, notation }`. `H` comes from the renderer or
the check, never from `content.js`.

| Helper | Meaning |
|---|---|
| `H.m(latex)`, `H.d(latex)` | inline and display mathematics. `{{key}}` or `\reg{key}` inside the formula prints the registry display of `key`; `{{key\|3}}` prints the value rounded to three decimals, as `\regr{key}{3}` does; `\reg{key}` keeps a subtitle identical to its `slides.tex` text. |
| `H.q(key[, digits])` | a registry number in running text: the display that `\reg{key}` prints, or with `digits` the rounded value that `\regr{key}{digits}` prints |
| `H.v(key)` | the registry value as a number, for layout only (the position of a mark on a scale), never before slide 16 |
| `H.go(target, text)` | a link button to a `\hypertarget` name, as `\hyperlink` does |
| `H.back(target)` | the Back button of a backup |
| `H.endFrame(label)` | optional; called after each frame is built, so the renderer can attribute messages |

## 3. Frame record

```js
{ id, label, num, part, title, short, subtitle, targets, minutes, defines, widget, body,
  backup, origin, cls }
```

- `id`: `f0`, `s1` to `s26`, `b1` to `b12`, with the continuation pages `b6b`, `b6c`, `b8b` and
  `b9b`. `label`: the `slides.tex` label (`S0` to `S26`, `B1` to `B12`, `B6b`, `B6c`, `B8b`, `B9b`).
- `num`: the displayed number, the Beamer frame number. `S1` is slide 1, `S26` is slide 26. The
  title is 0; backups show their label.
- `part`: 1 to 6 for the main frames, `B` for backups (section 7).
- `title`: the `slides.tex` title argument verbatim; `$...$` is mathematics. Every frame has a
  title. `short` names a frame without a title; only the title frame carries one (`Title`).
- `subtitle`: HTML built with the helpers; its plain text equals the `\framesubtitle`.
- `targets`: the frame's `\hypertarget` names, in order.
- `minutes`: the timing plan, section 10 of this file; backups 0.
- `defines`: notation keys introduced on the frame (section 8).
- `widget`: the engine behaviour (section 5); empty for static frames.
- `backup`, `origin`: backups and the frame their Back button names.
- `cls`: an extra class on the slide. S1 has `cls: 'bigtitle'`, a larger title.

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

The title frame adds the class `title-slide` and holds only its body. Backups add the class
`backup`, `data-backup="true"` and `data-origin`. The `cls` of a frame is added to its classes. The
build gives a frame without a title the class `nohead` and no header; no frame uses it now.
Reveals use `data-step="n"`: an element is shown from step n on. Number
spans are `span.q` (`data-q` holds the registry key, or several keys for a formula, and the
`title` reads `key = display`); formula numbers add `.q-tex`; rounded numbers add `data-round`.
Links are `button.goto[data-target]`; Back is `button.goto.back[data-back]`.

Class vocabulary for the body: `.bigtitle` (on the slide), `.cover`, `.lead`, `.bigline`,
`.formal`, `.roadmap`, `.small`, `.mid`, `.xs`, `.roomy`, `.smallline`, `.grayline`,
`.ruled-line`, `.caption`, `.definition`, `.setup`, `.takeaway`, `.intuition`, `.statement > .statement-tag`,
`.deflist`, `.colhead`, `.ruledcol`, `.footline`, `.gloss`, `.largeline`, `.rule-accent`, `.rule-light`,
`.model-strip > .current` (section 11), `.footzone > .foot`, `.nav`,
`.chain`, `.lastline`, `.info`, `.muted`, `.nw`, `.cols3 > .rcol`, `.flow > .box` (`.flow-3`,
`.box-cost`, `.arrow`), `.slotflow > .slotsrc`, `.sbox` (`.slotbox`, `.makerbox`, `.sbox-cost`),
`.beliefbar > .track > .band`, `.tick`, `.scale`, `.propblock` (`.theorem`), `.result-lines`,
`.proofmap > .pbox > .ptag`, `.impact` (`.brace`, `.lvl > .lvl-line`), `.split > .col`
(`.wide`, `.gainsplit`, `.beliefsplit`, `.regionsplit`, `.accesssplit`, `.testsplit`, `.text`),
`.figure` (`.wide`), `.slider`, `.bars`, `.twocol`, `.twotables`, `.panels4 > .rpanel`,
`.notation`, `.refs`, `.steps`, the list classes `.props`, `.conds`, `.defs`, `.conclusion` and
`.predictions`, the table row classes `.panel`, `.subhead` and `.last-a`, and the table classes
named after their content (`.t-lit3`, `.t-inv`, `.t-cases`, `.t-prop2`, `.t-out`, `.t-controls`,
`.t-access2`, `.t-region`, `.t-payoffs`, `.t-panels`, `.t-thresh`, `.t-econ`).

## 5. Widgets

| `widget` | Frame | Elements | Behaviour |
|---|---|---|---|
| `title` | S0 | `.cover` | static title page |
| `cases` | S10 | `tr[data-row]` | a click or Enter on a row of the payment cases (R low or R high) highlights it; the same action on the highlighted row clears it |
| `gain` | S13 | `#gain` | the ceiling Δ_T and the floor ρκ(π)Δ_T of the gain of a correct order against strength, in units of k on a log axis, with the cost line k; one band shades the strengths below Δ_T = k, one the strengths from r_S on. Symbols only: no ticks, no hover values, no example strengths |
| `beliefs` | S16 | `#beliefs`, `#beliefs-r`, `#beliefs-r-value` | the threshold belief τ(r) against strength, with the band [m(π), M(π)], the prior, r_0, r_1, r_2 and r_C; the slider moves a cursor along the plotted curve and prints r to two decimals |
| `controls` | S18 | `tr[data-row]`, `#f11-bars` | a click or Enter selects a row of the entry table (full model, full orders held fixed, price hidden); the bars draw its entries at r_0 and r_1. The full-model row is selected first |
| `region` | S19 | `#region` | the coexistence region of Proposition 3 at the prior in the plane of Δ_T and τ, with the example's path through r_0, r_A, r_F, r_N |
| `coex` | S20 | `#coex` | entry in each equilibrium of the example against strength, whole path (a) and the marked strengths r_A, r_F, r_N, r_J, r_S (b), with the threshold pair T and the coexistence band [r_A, r_N] |
| `research` | S22 | `#research` | research (a) and entry (b) along the path in zero, recruiting and floor-entry research, with r_R, r_λ̄, r_N, r_Q and r_C marked |
| `notation` | B2 | `#notation-table` | the B2 table from the notation rows |

Figures draw with `CCC.charts.draw` from `charts.js` (a trimmed copy of the handout's SVG renderer: tokens, geometry, drawing, legend and hover) at a zoom of 1.4, so text reads at a
distance. The curves come from `window.CCC_DATA.fig`, written by `figdata.py`. A figure that
labels its lines directly carries `.nolegend`. `?print=1` in the address draws every figure
before printing; `export_pdf.sh` uses it.

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
is KaTeX at 1.04 em; the seam with Libertinus is accepted.

Type scale at 1600 x 900, where 1 pt of the 16:9 Beamer page is 3.5 px. Libertinus Sans: frame
title 50 px at weight 700 (60 px on S1, `.bigtitle`, the \LARGE of the deck); statement tag 30 px
in the accent; table heads 27 px; link buttons 20 px; the footline 23 px in small capitals; figure
text 12.5 to 20 px drawn at a zoom of 1.4. Libertinus Serif: the title frame 60 px at 700; body
32 px at line height 1.3 (\Body); subtitle 27 px italic muted; statement body and gloss 28 px;
small 28 px, xs 25 px; foot lines 23 px muted; takeaway 32 px at 700 over a 3 px accent rule;
intuition 32 px italic over a hairline; the large line 42 px at 700. Slide padding 22 px 40 px.

## 7. Parts

| Part | Name | Frames (slide numbers) |
|---|---|---|
| 1 | Why the question matters | S0 to S4 (0 to 4) |
| 2 | Model | S5 to S9 (5 to 9) |
| 3 | Mechanism | S10 to S13 (10 to 13) |
| 4 | Main result | S14 to S18 (14 to 18) |
| 5 | Path and research | S19 to S22 (19 to 22) |
| 6 | Scope, money, tests | S23 to S26 (23 to 26) |
| B | Backups | B1 to B12 on 16 pages: B1 to B5, B6, B6b, B6c, B7, B8, B8b, B9, B9b, B10, B11, B12 |

Links (the `\hyperlink` buttons of `slides.tex`): S2 → B1; S3 → B1; S6 → B2; S7 → B11; S9 → B3;
S11 → B5; S14 → B6; S15 → B6; S16 → B4; S17 → B4, B6; S18 → B6; S19 → B7; S20 → B7; S21 → B8;
S22 → B8; S23 → B9, B11; S24 → B10; S25 → B12.

Origins (the `\BackButton` targets): B1 → S2; B2 → S6; B3 → S9; B4 → S16; B5 → S11; B6, B6b,
B6c → S14; B7 → S19; B8, B8b → S21; B9, B9b → S23; B10 → S24; B11 → S7; B12 → S25. The
hypertargets are `main:s2`, `main:s6`, `main:s7`, `main:s9`, `main:s11`, `main:s14`, `main:s16`,
`main:s19`, `main:s21`, `main:s23`, `main:s24`, `main:s25` and `app:b1` to `app:b12`. The
continuation pages B6b, B6c, B8b and B9b repeat the title, carry a Back button and have no
hypertarget.

## 8. Notation

`glossary` lists every symbol the slides use, with a pattern that finds it in a slide's LaTeX.
`defines` on a frame introduces symbols. `check_deck.mjs` walks the frames in deck order (the main
frames, then the backups) and fails if a pattern matches before the frame that defines it. The
order: p on S5; R, F, r, class j and G_j, π, θ, C, ρ, c_H, y, D on S6; λ, q, k, β, X, P, V_T, b,
u on S7; t_0, t_j, g_j, Δ_T, μ, B(μ), W_j on S8; x, e(x), U_j and the sans-serif E and O on S9;
m and M, τ on S12; K_j and κ on S13; F_0 to F_2, Δ_0 to Δ_2, e_H and e_L on S14; h, ℓ, r_0, r_1, r_2, r_C on S16;
the strengths r_A, r_F, r_N, r_J, r_S on S20; a, λ̄, m_λ and M_λ, λ_E, λ_R on S21; r_R on S22;
ω on S24; the backup-only symbols e_r and (q_H, q_L) on B2 and ξ on B11. `notation` holds the B2
rows; the B2 slide and the G panel render from it.

## 9. Data

`window.CCC_DATA` holds `registry` (the key, value and display of every key the slides print, and
nothing else) and `fig` (the curves and the example's inputs for the figures). `window.CCC_DECK`
holds the frame list, the parts, the notation rows, the total of numbered slides, the planned
minutes and the checkpoint line; `window.CCC_NOTES` holds the speaker notes by label, from `notes.md`.

## 10. Timing plan (45 minutes with the title)

| Slides | Minutes |
|---|---|
| 0 (title) | 0.5 |
| 1 to 4 | 2, 2, 2, 2 (8) |
| 5 to 9 | 1.5, 2, 2, 2, 1.5 (9) |
| 10 to 13 | 1.5, 2, 2, 1.5 (7) |
| 14 to 18 | 2, 1.5, 1.5, 1.5, 2 (8.5) |
| 19 to 22 | 1.5, 1.5, 2, 1.5 (6.5) |
| 23 to 26 | 1.5, 1.5, 2, 0.5 (5.5) |

Checkpoints: minute 9 ends slide 4; minute 18 ends slide 9; minute 25 ends slide 13; minute 34 ends
slide 18; minute 45 ends slide 26. Cuts in order: slide 20 to one spoken sentence; slide 22 to one
spoken sentence; slide 23 to its takeaway line. Never cut slides 4, 9, 11, 14, 18 or 25.

## 11. The class for each Beamer macro

The macros of `ccc-journal.sty` and the class that prints the same thing on a web frame. A later
port of the Overleaf deck frame by frame uses these in `content.js`; `deck.css` holds the rules.

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
