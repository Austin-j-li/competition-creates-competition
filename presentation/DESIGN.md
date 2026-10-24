# Slides design contract ("UCL family")

The contract between the slide files: `content.js` (the frames), `render.mjs` (build-time
rendering and the number guard), `deck.js` and `template.html` (the engine), `deck.css` (the
visual system) and `check_deck.mjs` (the drift check). Change this file before you change a
name in it.

## 1. Brief

The web version of `talk/talk.tex`, the Beamer deck of the 40-minute seminar talk (30.25 planned
minutes and a question reserve). All 47 frames stay in the Beamer order and organisation. The
look copies the Beamer deck (moloch in the UCL palette) and the handout of the same design.

Invariants:

- Offline. Fonts, KaTeX, data and PDFs are local. No network at runtime.
- `talk.tex` is the master. Titles, subtitles, text, tables, hypertargets and link buttons are
  copied from it; `check_deck.mjs` fails on any difference it can see.
- Every number carries its source: a registry key in `numerics/quantity_registry.csv`, or the
  paper table file that `talk.tex` cites. The build stops unless the number rounds from that
  source at the precision shown.
- Status words: analytical, computer-assisted, numerical diagnostic, open; declarations carry
  `input`. Each status line on a slide names one of them.
- Purple is chrome only. `--c-info` (#AA4B00) marks the target-payoff spread and the
  information chain; `--c-cost` (#006F50) marks preparation costs, the floor and the window.
- The deviation phrase follows `talk.tex` ("every unilateral deviation").
- Benchmark paper only.

## 2. The helper contract (content.js)

`window.createDeck(H)` returns `{ frames, glossary, notation }`. `H` comes from the renderer or
the check, never from `content.js`.

| Helper | Meaning |
|---|---|
| `H.m(latex)`, `H.d(latex)` | inline and display mathematics |
| `H.q(key, shown)` | a registry number. `key` is a name, `-name` (negated) or `a+b` (a sum); several keys separated by spaces must all match. `shown` is the string `talk.tex` prints. |
| `H.qm(latex, key, shown)` | the same number inside a formula; the formula must print `shown`. Several numbers: `H.qm(latex, [[key, shown], ...])`. |
| `H.qk(html, keys)` | provenance for a formula that names a quantity but prints no number of it (F7: M = 1 − m) |
| `H.tx(file, row, col, value, text, latex)` | a number printed in `tables/<file>`: the line that starts with `row` (`Panel A:` or `Panel B:` selects a panel; `#count:met`, `#count:unchanged`, `#count:falls` count rows of the signal grid), cell `col` (0 = the label). `text` is a shown magnitude; `latex` shows it as mathematics. |
| `H.go(target, text)` | a link button to a `\hypertarget` name, as `\hyperlink` does |
| `H.back(target)` | the Back button of a backup |
| `H.status(text)` | a status line in the paper's vocabulary |
| `H.endFrame(label)` | optional; called after each frame is built, so the renderer can attribute messages |

The guard accepts a shown string when it equals the registry display, or when it lies within
half a unit of its last digit from the registry value. An integer label (0, 2, 7) must match
exactly. Intervals must equal the registry display, or its negation with the bounds swapped.

## 3. Frame record

```js
{ id, label, num, part, title, titleQ, subtitle, targets, minutes, defines, widget, body,
  backup, origin, noframenumbering }
```

- `id`: `f0` … `f16`, `f10a`, `f10b`, `a1` … `a29`. `label`: the `talk.tex` label.
- `num`: the displayed number; `F10a` and `F10b` both show 10; backups show their label.
- `part`: 1 to 8 for the main frames, `B` for backups (section 7).
- `title`: the `talk.tex` title argument verbatim; `$...$` is mathematics. `titleQ` maps a
  number in the title to its registry key (only F10a and F10b, as in `talk.tex`).
- `subtitle`: HTML built with the helpers; its plain text equals the `\framesubtitle`.
- `targets`: the frame's `\hypertarget` names, in order.
- `minutes`: the timing plan of `talk/structure-plan.md`, section 10; backups 0.
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
<section class="slide" id="f7" data-label="F7" data-num="7" data-part="4" data-title="…"
         data-minutes="3" data-widget="" data-targets="main:bound main:orders main:notation">
  <header class="slide-head"><h2>…</h2><p class="sub">…</p></header>
  <div class="slide-body">…</div>
  <footer class="slide-foot"><span class="foot-title">…</span><span class="foot-num">7</span></footer>
</section>
```

Backups add `data-backup="true"` and `data-origin`. Reveals use `data-step="n"`: an element is
shown from step n on. Number spans are `span.q` (`data-q`, `data-shown`, `data-status`, a
title with value, status and source); formula numbers add `.q-tex`; table numbers add
`.q-table` with `data-row` and `data-col`. Links are `button.goto[data-target]`; Back is
`button.goto.back[data-back]`.

Class vocabulary for the body: `.lead`, `.small`, `.roomy`, `.claims`, `.bench`, `.keyidea`,
`.info`, `.cost`, `.grayline`, `.graycite`, `.status`, `.takeaway`, `.nav`, `.flow > .box`,
`.timeline > .tl`, `.infoset`, `.segmented`, `.two-lines`, `.resultbox > .propitem > .propnum`,
`.split` (`.narrow`, `.wide`), `.figure`, `.slider`, `.readout`, `.bars`, `.notation`, `.refs`,
`.steps`, and the table classes named after their frame (`.t-bench`, `.t-controls`, …).

## 5. Widgets

| `widget` | Frame | Elements | Behaviour |
|---|---|---|---|
| `title` | F0 | `.cover` | static title page |
| `infosets` | F4 | `.tl[data-info]`, `#f4-infoset` | focus, hover or click shows the agent's information set |
| `cases` | F5 | `.segmented [data-case]`, `tr[data-row]` | highlights the row R ≤ ℓ or R > ℓ |
| `x1` | F6 | `#x1` | spread and profit at the prior from `fig1`, markers at r0 and r1 |
| `x2` | F8 | `#x2`, `#x2-r`, `#x2-r-value`, `#x2-readout` | profit at three beliefs from `fig1` with the cost lines; the slider moves a marker and reads the closed forms (a fixed-order calculation) |
| `controls` | F11 | `.segmented [data-row]`, `#f11-bars` | highlights a row and draws its two entry values with its status |
| `footnote` | F13 | `[data-toggle]` | opens the signal-grid line |
| `access` | F14 | `.segmented [data-col]` | highlights a column |
| `rows` | A3 | `.hover-rows` | row highlight on hover |
| `x4` | A9 | `#x4` | Figure 4 builder |
| `notation` | A12 | `#notation-table` | the A12 table from the notation rows |
| `columns` | A18 | `[data-col]` | dims the other force on hover |
| `x3` | A14 | `#x3` | Figure 3 builder |
| `x5a`, `x5b` | A24, A25 | `#x5a`, `#x5b` | one panel each of the Figure 2 builder, with every display rule |

F7 also uses `[data-toggle]` for its arithmetic line. Figures draw with `CCC.charts.draw` from
`handout/charts.js` at a zoom of 1.4, so text reads at a distance. The closed forms come from
`handout/explorer.js`.

## 6. Tokens and type

```css
:root { --ucl-dark:#361A54; --ucl-bright:#993BFF; --ucl-mid:#BA82FF; --bg:#ffffff;
  --surface:#f6f3fa; --ink:#14111a; --muted:#5d5866; --gray-text:#616161; --line:#d9d3e2;
  --c-info:#AA4B00; --c-cost:#006F50;
  --font-sans:"Fira Sans","CCC Symbols",system-ui,Arial,sans-serif;
  --font-mono:"Fira Mono","CCC Symbols",ui-monospace,Menlo,monospace }
```

The dark theme swaps the ground to #17101f and lightens the concept colours. The faces are the
handout's locked files (`handout/fonts.lock.json`): Fira Sans 400 to 700 with italic, Fira Mono
400 to 700, and the "CCC Symbols" fallback for arrows and relations.

Type scale at 1600 x 900: slide title 48 px Fira Sans 500 on the purple band; subtitle 25 px;
body 31 px; small 27 px; grey lines 23 px; status 21 px; tables 27 px (dense backups 20 to
24 px); link buttons 19 px. Slide padding 26 px 56 px. The progress rule under the title band
is 5 px, bright purple, as long as the frame number over 16.

## 7. Parts

| Part | Name | Frames |
|---|---|---|
| 1 | Question | F0, F1, F2, F3 |
| 2 | Model | F4 |
| 3 | Two claims | F5, F6 |
| 4 | Price | F7, F8 |
| 5 | Theorem | F9 |
| 6 | Numbers | F10a, F10b, F11 |
| 7 | Boundaries | F12, F13, F14 |
| 8 | Close | F15, F16 |
| B | Backups | A1 to A29 |

Links and origins (from `talk.tex`): F1 → A1, A2; F3 → A3, A29; F4 → A4, A5, A7; A5 → A6;
F5 → A8, A9; F7 → A10, A11, A12; F8 → A13, A14, A15; F9 → A16, A17, A18; F10b → A19, A20,
A21; F11 → A22, A23; F12 → A24; A24 → A25; F13 → A26; F14 → A27; A27 → A28.

## 8. Notation

`glossary` lists every symbol the slides use, with a pattern that finds it in a slide's
LaTeX. `defines` on a frame introduces symbols. `check_deck.mjs` walks the frames in deck order
(the main frames, then the backups) and fails if a pattern matches before the frame that
defines it. The order follows `talk/structure-plan.md`, section 6.1: R, r, θ, h, ℓ, p, C,
c_L, c_H, ρ on F4; Δ_T, t_θ, g_H, g_L and the general-support F, r̄ on F5; r0, r1 on F6; μ, m,
M, b, k, (q_H, q_L) on F7; B_r and r2 on F8; the dummy q on F9; backup-only symbols on the
first backup that shows them. `notation` holds the A12 rows; the A12 slide and the G panel
render from it.

## 9. Data

`window.CCC_DATA` is the handout's data (`handout/data.py`): `inputs`, `registry`, `fig1` to
`fig4`, `tables`. `window.CCC_DECK` holds the frame list, the parts, the notation rows and the
checkpoint line; `window.CCC_NOTES` holds the speaker notes by label.
