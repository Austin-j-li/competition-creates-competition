# Slides design contract (the ruled document)

The visual system (tokens, type, rules, components, the concept-colour rule and the slop list) is
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
the ruled document system of the front page: ink on cool white paper (slate in the dark theme), Archivo for titles and
instruments, STIX Two Text for prose, two rule weights (a 1 px hairline and a 2 px ink rule) and no
fills, cards, pills, shadows, gradients or side stripes. The 2 px rule under each frame title is the
progress rule. The Beamer deck in Overleaf uses a classic Beamer theme (Madrid, `ccc-classic.sty`)
by rule; the web slides keep the ruled look. Words, numbers, frames and links stay identical.

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
- The chrome has no colour: links, buttons, the rail, the focus ring and the slider thumb are ink.
  `--c-info` (#b54b00, #f6a157 in the dark theme) marks the target-payoff spread and the
  information chain; `--c-cost` (#006459, #46b3a8) marks preparation costs and the cost line.
  Nothing else is coloured, and no UCL colour appears.
- Controls share one grammar: text, with an underline. The active choice has a 2 px ink underline
  (the rail, the choice buttons, the pager); a link button has a 1 px underline that becomes 2 px on
  hover. A switched-off legend entry is struck through.
- Exhibits (figures, tables, the timeline, the order-slot flow) span the content column; prose and
  captions stop at the text measure. Registry numbers keep their provenance hover, marked by a
  faint dotted hairline; numbers in prose are STIX with tabular figures.
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
`.ruled-line`, `.caption`, `.definition`, `.setup`, `.takeaway`, `.footzone > .foot`, `.nav`,
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
:root { --bg:#fbfcfc; --page:#e7eaee; --ink:#1e2530; --muted:#5b6573; --line:#c7cdd5; --grid:#e4e8ec;
  --rule:#1e2530; --c-info:#b54b00; --c-cost:#006459;
  --font-serif:"STIX Two Text","CCC Symbols",Georgia,serif;
  --font-sans:"Archivo","CCC Symbols",system-ui,Arial,sans-serif;
  --font-mono:"Fira Mono","CCC Symbols",ui-monospace,Menlo,monospace }
```

The dark theme is slate paper (#1a1f26, ink #e8ecf1, muted #a3adb9, hairline #3d4652) with the two
concept colours lightened; it has no tint and no glow. The faces are the deck's locked files
(`presentation/fonts.lock.json`): Archivo (variable weight and width, normal and italic), STIX Two Text
400 to 600 with italic, Fira Mono, and the "CCC Symbols" fallback for arrows and relations.
`build.py` writes the `@font-face` rules, with `font-stretch` for the variable Archivo, and embeds
the local font data so the staged deck carries its own faces.

Type scale at 1600 x 900. Archivo: frame title 44 px at weight 600 (56 px on S1, `.bigtitle`); the
title frame 48 px at 600 and 112% width; frame number 44 px muted; tables 27 px with tabular figures
(dense backups 20 to 25 px); link buttons 19 px; figure text 12 to 20 px drawn at a zoom of 1.4.
STIX Two Text: subtitle 28 px muted; body 33 px at line height 1.32; small 29 px; grey lines 25 px;
takeaway 32 px at weight 500 under a 2 px ink rule. Mathematics is KaTeX at 1.02 em; the seam with STIX is accepted. Slide padding
26 px 56 px.

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
