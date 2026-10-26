# Slides design contract (the ruled document)

The contract between the slide files: `content.js` (the frames), `render.mjs` (build-time
rendering and the registry keys), `figdata.py` (the figure curves), `deck.js` and `template.html`
(the engine), `charts.js` (the SVG renderer), `deck.css` (the visual system), `notes.md` (the speaker notes) and `check_deck.mjs`
(the drift check). Change this file before you change a name in it.

## 1. Brief

The web version of `slot/manuscript/slides.tex`, the Beamer deck of the order-slot seminar talk
(30.25 planned minutes and a question reserve). All 34 frames stay in the Beamer order and
organisation: the title, 21 numbered frames and 12 backups. The look is the ruled document system
of the front page: ink on cool white paper (slate in the dark theme), Archivo for titles and
instruments, STIX Two Text for prose, two rule weights (a 1 px hairline and a 2 px ink rule) and no
fills, cards, pills, shadows, gradients or side stripes. The 2 px rule under each frame title is the
progress rule. The Beamer PDF keeps its own theme.

Invariants:

- Offline. Fonts, KaTeX and data are local. No network at runtime.
- `slides.tex` is the master. Titles, subtitles, hypertargets and link buttons are copied from it;
  `check_deck.mjs` fails on any difference it can see.
- Every number is the `display` of a row in
  `audit/slot_manuscript_2026_10_23/registry/registry.csv`, the string that `\reg{key}` prints in
  `slides.tex`. The build stops on a key the registry does not hold. No decimal is typed into a slide.
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
| `H.m(latex)`, `H.d(latex)` | inline and display mathematics. `{{key}}` or `\reg{key}` inside the formula prints the registry display of `key`; `\reg{key}` keeps a subtitle identical to its `slides.tex` text. |
| `H.q(key)` | a registry number in running text: the display that `\reg{key}` prints |
| `H.v(key)` | the registry value as a number, for layout only (the position of a mark on a scale) |
| `H.go(target, text)` | a link button to a `\hypertarget` name, as `\hyperlink` does |
| `H.back(target)` | the Back button of a backup |
| `H.endFrame(label)` | optional; called after each frame is built, so the renderer can attribute messages |

## 3. Frame record

```js
{ id, label, num, part, title, short, subtitle, targets, minutes, defines, widget, body,
  backup, origin }
```

- `id`: `f0`, `q1` to `q3`, `f1` to `f17`, `a1` to `a12`. `label`: the `slides.tex` label.
- `num`: the displayed number, the Beamer frame number. `Q1` is slide 1, `F17` is slide 20. The
  title is 0; backups show their label.
- `part`: 1 to 7 for the main frames, `B` for backups (section 7).
- `title`: the `slides.tex` title argument verbatim; `$...$` is mathematics. Q1 has none and a
  `short` name for the overview; its slide has no title band.
- `subtitle`: HTML built with the helpers; its plain text equals the `\framesubtitle`.
- `targets`: the frame's `\hypertarget` names, in order.
- `minutes`: the timing plan, section 10 of this file; backups 0.
- `defines`: notation keys introduced on the frame (section 8).
- `widget`: the engine behaviour (section 5); empty for static frames.
- `backup`, `origin`: backups and the frame their Back button names.

## 4. Markup

Chrome (`template.html`): a tools bar `nav.hud` (`#overview`, `#notes`, `#notation`, `#theme`,
`#fullscreen`, `#help`, and a link back to the research brief), the stage `main#stage >
#deck`, the rail `footer.rail-bar` (`#rail`, `#return`, `#previous`, `#counter`, `#next`,
`#progress-label`), a dialog `#panel` and a live region `#announcer`.

The build writes one section per frame:

```html
<section class="slide" id="f7" data-label="F7" data-num="10" data-part="4" data-title="…"
         data-minutes="2.5" data-widget="gain" data-targets="">
  <header class="slide-head"><h2>…</h2><p class="sub">…</p></header>
  <div class="slide-body">…</div>
  <footer class="slide-foot"><span class="foot-title">…</span><span class="foot-num">10</span></footer>
</section>
```

Backups add `data-backup="true"` and `data-origin`. A frame without a title (Q1) carries the class
`nohead` and no header. Reveals use `data-step="n"`: an element is shown from step n on. Number
spans are `span.q` (`data-q` holds the registry key, or several keys for a formula, and the
`title` reads `key = display`); formula numbers add `.q-tex`. Links are `button.goto[data-target]`;
Back is `button.goto.back[data-back]`.

Class vocabulary for the body: `.lead`, `.small`, `.roomy`, `.claims`, `.keyidea`, `.info`,
`.cost`, `.grayline`, `.graycite`, `.takeaway`, `.nav`, `.bigq`, `.flow > .box`, `.slotflow >
.sbox`, `.beliefbar`, `.timeline > .tl`, `.infoset`, `.segmented`, `.two-lines`, `.resultbox >
.propitem > .propnum`, `.split` (`.narrow`, `.wide`), `.figure` (`.wide`, `.nolegend`), `.slider`,
`.readout`, `.bars`, `.notation`, `.refs`, `.steps`, and the table classes named after their frame
(`.t-cases`, `.t-orders`, `.t-inputs`, `.t-trade`, `.t-bench`, `.t-controls`, …).

## 5. Widgets

| `widget` | Frame | Elements | Behaviour |
|---|---|---|---|
| `title` | F0 | `.cover` | static title page |
| `infosets` | F2 | `.tl[data-info]`, `#f2-infoset` | focus, hover or click shows the agent's information set |
| `cases` | F3 | `.segmented [data-case]`, `tr[data-row]` | highlights the row R ≤ ℓ or R > ℓ |
| `orders` | F5 | `.segmented [data-order]`, `#f5-pin`, `#f5-say` | an order moves a pin on the belief scale to m(π), π or M(π) and explains where it comes from |
| `gain` | F7 | `#gain` | the floor ρκΔ_T and the ceiling Δ_T of a correct order in units of k, on a log axis, with the strengths where only a quiet market or only full orders can occur |
| `beliefs` | F8 | `#beliefs`, `#beliefs-r`, `#beliefs-r-value`, `#beliefs-readout` | the threshold belief τ(r) against the band [m, M]; the slider reads the plotted curve and says whether a buy order clears the threshold |
| `controls` | F11 | `.segmented [data-row]`, `#f11-bars` | highlights a row and draws its two entry values |
| `region` | F12 | `#region` | the coexistence region of Proposition 3 in the plane of Δ_T and τ, with the example's path through r_0, r_A, r_F, r_N |
| `coex` | F12b | `#coex` | entry in each equilibrium at the prior, whole path (a) and the marked strengths (b), with the threshold pair T |
| `research` | F13 | `#research` | research (a) and entry (b) along the path in zero, recruiting and floor-entry research (Corollary 3) |
| `access` | F15 | `.segmented [data-col]` | highlights a column |
| `notation` | A2 | `#notation-table` | the A2 table from the notation rows |

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

Type scale at 1600 x 900. Archivo: frame title 44 px at weight 600; the title frame 48 px at 600 and
112% width; frame number 44 px muted; tables 27 px with tabular figures (dense backups 20 to 25 px);
link buttons 19 px; figure text 12 to 20 px drawn at a zoom of 1.4. STIX Two Text: subtitle 28 px
muted; body 33 px at line height 1.32; small 29 px; grey lines 25 px; takeaway 33 px at weight 500
under a 2 px ink rule. Mathematics is KaTeX at 1.02 em; the seam with STIX is accepted. Slide padding
26 px 56 px.

## 7. Parts

| Part | Name | Frames (slide numbers) |
|---|---|---|
| 1 | Question | F0, Q1, Q2, Q3 (0 to 3) |
| 2 | Setting | F1, F2, F3 (4 to 6) |
| 3 | Price | F4, F5, F6 (7 to 9) |
| 4 | Mechanism | F7, F8, F9 (10 to 12) |
| 5 | Result | F10, F11 (13, 14) |
| 6 | Beyond | F12, F13, F14, F15 (15 to 18) |
| 7 | Close | F16, F17 (19, 20) |
| B | Backups | A1 to A12 |

Links and origins (from `slides.tex`): Q2 → A1; F2 → A2; F4 → A3; F5 → A4; F6 → A5; F9 → A6;
F10 → A7; F12 → A8; F13 → A9; F14 → A10, A11; F15 → A12.

## 8. Notation

`glossary` lists every symbol the slides use, with a pattern that finds it in a slide's LaTeX.
`defines` on a frame introduces symbols. `check_deck.mjs` walks the frames in deck order (the main
frames, then the backups) and fails if a pattern matches before the frame that defines it. The
order: R, r, class j and G_j, π, h, ℓ, p, ρ, c_H on F2; Δ_T, t_j, g_j, B_r(μ), μ, r_0, r_1 on F3;
λ, q, k, β, X, P, V_T, b, u on F4; m and M, e_r, t_0 on F5; r_2 on F6; κ and (q_H, q_L) on F7;
τ and r_C on F8; W_H and F_i on F9; the thresholds r_A to r_S on F12; a, λ̄, r_R on F13; ω on F14;
backup-only symbols on the first backup that shows them. `notation` holds the A2 rows; the A2
slide and the G panel render from it. Definition strips (`.infoset` on F2 and F5) say in a
sentence what the selected object is.

## 9. Data

`window.CCC_DATA` holds `registry` (the key, value and display of every key the slides print, and
nothing else) and `fig` (the curves and the example's inputs for the figures). `window.CCC_DECK`
holds the frame list, the parts, the notation rows, the total of numbered slides and the
checkpoint line; `window.CCC_NOTES` holds the speaker notes by label, from `notes.md`.

## 10. Timing plan (30.25 minutes before questions)

| Slides | Minutes |
|---|---|
| 0 (title) | 0.25 |
| 1 to 3 | 1.5, 1.25, 1.0 |
| 4 to 6 | 1.0, 2.0, 2.0 |
| 7 to 9 | 1.75, 1.75, 1.0 |
| 10 to 12 | 2.5, 2.25, 2.0 |
| 13, 14 | 1.5, 1.75 |
| 15 to 18 | 1.5, 1.5, 1.0, 1.0 |
| 19, 20 | 1.0, 0.75 |

Checkpoints: slide 6 by 9 min; slide 8 by 12.5 min, else skip slide 9; slide 12 by 20.25 min, else
skip slides 15 and 17; slide 14 by 23.5 min, else give slide 16 as one sentence and skip slide 18.
