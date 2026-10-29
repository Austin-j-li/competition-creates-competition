---
name: Competition Creates Competition
description: The journal look. One visual system for the website of the paper (the research brief page and the web slides), matched to the Beamer deck of the talk (ccc-journal.sty).
colors:
  paper: "#ffffff"
  ink: "#1c1c1c"
  muted: "#666666"
  hairline: "#c9c9c9"
  grid: "#e6e6e6"
  surface: "#f2f2f2"
  accent: "#7a1f1f"
  slate: "#171717"
  slate-surface: "#242424"
  slate-ink: "#ebebeb"
  slate-muted: "#a3a3a3"
  slate-hairline: "#474747"
  slate-grid: "#2e2e2e"
  slate-accent: "#d4908f"
typography:
  title:
    fontFamily: "Libertinus Serif, Georgia, serif"
    fontSize: "clamp(1.9rem, 3.4vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.12
  headline:
    fontFamily: "Libertinus Sans, system-ui, Arial, sans-serif"
    fontSize: "clamp(1.55rem, 2.2vw, 1.8rem)"
    fontWeight: 700
    lineHeight: 1.15
  tag:
    fontFamily: "Libertinus Sans, system-ui, Arial, sans-serif"
    fontSize: "0.98rem"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: "Libertinus Serif, Georgia, serif"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Libertinus Sans, system-ui, Arial, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.35
rounded:
  none: "0"
  button: "6px"
spacing:
  hair: "1px"
  rule: "1.5px"
  xs: "0.35rem"
  sm: "0.7rem"
  md: "1rem"
  lg: "1.75rem"
  xl: "2.5rem"
  section: "4.25rem"
---

# Competition Creates Competition: the journal look

## Overview

The website is set like the Beamer deck of the talk (`overleaf` working copy, `ccc-journal.sty`),
which the author chose on 29 October 2026: Libertinus Serif for the reading text, Libertinus Sans
for titles, tags, labels and controls, Libertinus Math as the symbol fallback, white paper, one
oxblood accent, and greys. There are no bars, boxes, fills, cards, pills, shadows or gradients.
Hierarchy comes from the type and from two rules: an accent rule (1 to 1.5 px on the page, 3 px on
the 1600 by 900 slide stage) and a light hairline.

**Key Characteristics:**
- One palette, one type family and one rule grammar across the brief page, the web slides and the Beamer deck.
- A title is bold sans in ink over an accent rule; a statement is an accent rule, a bold sans tag in the accent, the body, a light rule; a takeaway is bold text over an accent rule; an intuition is italic text over a light rule.
- The accent is the only chrome colour: rules, tags, the active tab or control, bullets, link buttons and the focus ring. Everything else is ink or grey.
- Figures draw in ink, the accent and greys; series differ by dash and marker, never by a third colour.
- Prose and captions stop at the measure; exhibits span the content column.

## Colors

- **Paper** (#ffffff): the page and the slide. **Stage** (#e9e9e9): the ground behind a slide in the web deck.
- **Ink** (#1c1c1c): reading text, headings, booktabs rules, the slider track.
- **Accent** (#7a1f1f, the `cAccent` of the deck): the rule under a title, the rule above a statement or a takeaway, the tag of a statement, column heads, the active tab, contents entry or control, bullets, link buttons, the focus ring; in figures the information series (`--c-info`, `--chart-2`).
- **Muted** (#666666): glosses, subtitles, foot lines, tick labels, inactive controls; in figures the grey series (`--chart-3`).
- **Hairline** (#c9c9c9): light rules, the dotted underline of a registry number, the border of a tooltip. **Grid** (#e6e6e6): chart gridlines and the hairlines inside a table.
- **Surface** (#f2f2f2): the ground of a tooltip; **button ground** (#ebebeb): the ground of a link button on a slide. Never a card.
- **Dark theme**: slate paper (#171717), ink #ebebeb, muted #a3a3a3, hairline #474747, grid #2e2e2e, surface #242424, and the accent lightened to #d4908f so that it keeps its contrast.

### Named Rules
**The One Accent Rule.** The oxblood is the only chrome colour. A coloured control, rule or tag in any other colour is a defect; `handout/check_display.py` and `presentation/check_deck.mjs` fail on a hex outside the palette above.
**The Figure Palette Rule.** A figure uses ink, the accent and greys (`--chart-1`, `--chart-2`, `--chart-3`, `--c-info`, `--c-cost`), and two series on one panel never share both colour and dash. Bands are the accent, ink or grey at low opacity.
**The Rejected Palette Rule.** No purple of the earlier "UCL family" design (#361A54, #993BFF, #BA82FF or the `--ucl-*` tokens) appears anywhere; the checks and the publisher fail on it.

## Typography

**Reading face:** Libertinus Serif (regular, italic, bold, bold italic). **Apparatus face:** Libertinus Sans (regular, italic, bold) for titles, tags, labels, tables' heads, legends, controls and the footline. **Symbols:** Libertinus Math, subset to the symbol blocks, as the fallback for arrows, relations and operators in text. **Mathematics:** KaTeX on the web, Libertinus Math in the deck; the seam is accepted. Hashes use the system monospace.

### Hierarchy
- **Title** (serif 700): the two lines of the brief's title; the title frame of the deck at 60 px.
- **Headline** (sans 700): a section heading of the brief; a frame title at 50 px (60 px on the question frame). Both sit over the accent rule; a subtitle is serif italic in grey under the title, above the rule.
- **Tag** (sans 700, accent): the name of a statement ("Proposition 2 · ..."), a column head, the contents heading; 30 px on a slide.
- **Body** (serif 400): 1.15rem at a 66ch measure on the brief; 32 px at 1.3 on a slide (\Body), 28 px inside a statement, 25 px for the small sizes.
- **Label** (sans 400): tabs, the contents, buttons, legends, table heads, the record line; 20 to 26 px on a slide.
- **Gloss and foot line** (serif, muted): 0.95rem on the brief; 28 px and 23 px on a slide.

### Named Rules
**The Run-In Rule.** A labelled paragraph opens with a bold sans run-in word and a period ("Answer.", "In short.", a scenario's name). A statement's name is a tag on its own line, not a run-in.
**The Measure Rule.** Prose, lists and captions stop at the measure; exhibits span the content column.
**The Registry Number Rule.** A registry number is set in the text face with tabular figures and a dotted hairline underline that carries its key on hover. No status word accompanies it.

## Layout

The brief page: at 1024 px and above, a 12.5rem contents rail on the left and a 54rem reading column inside a 72rem page. The title block opens with a short accent rule (7.5rem), the serif title on two lines, the sans byline and record line, then the tab row between hairlines. The opening question is the large line of the deck: an accent rule above, bold serif, a light rule below. Each section opens with its sans heading over the accent rule. Sections are 4.25rem apart. Below 1024 px the rail stacks above the column; at 600 px the body is 1.0625rem.

The web deck is a fixed 1600 by 900 stage with a 44 px tools bar above and a 52 px rail below. A frame has 40 px side padding; the head holds the title, the optional subtitle and the 3 px accent rule; the body starts under the rule; the takeaway or the intuition is pinned above the foot zone; the footline carries the short title in sans small capitals on the left and the link buttons and the frame number (`n / N`, or the backup label) on the right. The title frame has no footline.

## Elevation & Depth

Flat. No shadows, glows, gradients or layered surfaces. A tooltip and a dialog are paper with a hairline or ink border; a dialog backdrop is ink at 45 per cent.

## Shapes

Rectilinear, except the link buttons of a slide, which copy Beamer's `\beamergotobutton`: accent text on a light grey ground with a 6 px radius and a small triangle. Everything else is square: inputs, the tooltip, the slider thumb (a 4 px accent bar on a 1 px ink track), legend swatches.

## Components

- **Title block (brief):** short accent rule, serif title, sans byline, muted record line, tab row; the active tab is accent at weight 700 with a 2 px accent underline. **Title frame (deck):** a 240 px accent rule, the serif title at 60 px, the author and the department in sans.
- **Section heading:** sans 700 over a 1 px accent rule; the frame title is the same over a 3 px rule.
- **Statement:** accent rule, tag, body one size down, light rule (`.prop` on the brief; `.statement`, `.resultbox`, `.propblock` on a slide).
- **Takeaway and intuition:** bold over an accent rule; italic over a light rule; both pinned at the foot of a slide (`.takeaway`, `.intuition`).
- **Column head and label column:** a sans bold head in the accent over an accent rule (`.colhead`, the mechanism map's path labels, `.rcol`, `.rpanel`); bold sans labels on the left and text on the right (`.deflist`).
- **Lists:** a small accent square bullet; numbered items with a bold number.
- **Tables:** booktabs in the text face with a bold sans head: an ink rule above and below, a hairline under the head, grid hairlines between rows, no vertical rules, no zebra.
- **Figures:** the SVG renderer draws ink, accent and grey series over grid-coloured dotted gridlines; sans tick labels; a hairline above the legend and below the plot; the caption opens with a bold sans run-in.
- **Controls:** text in sans with a hairline underline; the active choice in the accent with a 2 px accent underline; the focus ring is 2 px accent. The link buttons of a slide are the Beamer button.
- **Model strip:** the six parts of the model in sans under the title of the model frames; the current ones bold accent, the others grey, light bullets between (`.model-strip`).
- **Footline:** sans small capitals, 23 px, grey.

## Do's and Don'ts

### Do:
- **Do** set every rule in the accent or as a hairline, and put the accent rule under a title and above a statement, a takeaway or a large line only.
- **Do** keep the accent as the only chrome colour and let it mean structure.
- **Do** draw figures in ink, the accent and greys, told apart by dash and marker.
- **Do** keep prose at the measure and exhibits across the column.
- **Do** compose the dark theme on slate with the lightened accent.

### Don't:
- **Don't** use a fill, card, pill, chip, badge, gradient, glow, shadow or side stripe; the only rounded shape is the link button of a slide.
- **Don't** add a second accent, a third figure colour, a decorative illustration or an icon set.
- **Don't** use any purple of the rejected palette.
- **Don't** set an eyebrow or kicker above a heading, a label in capitals, a numbered section label, a reading time or a progress bar on the page.
- **Don't** put a number on the motivation frames.

## Where each surface implements the system

- **Research brief page** (`handout/`): `style.css` (tokens, type, layout, components), `template.html`, `charts.js` (the SVG renderer; its fallback tokens repeat the palette), `figures.js` and `explorer.js` (figures through the renderer's tokens), `fonts/` with `fonts.lock.json` (Libertinus Serif, Sans and Math, SIL OFL, subset to woff2 from the 7.051 release, pinned by sha256), `build.py` (font faces and preload from the lock), `check_display.py` (the locked faces, the registry numbers, the journal palette, the rejected palette), `publish.py`.
- **Web slides** (`presentation/`): `deck.css` (the same `:root` tokens; `check_deck.mjs` fails when a shared token differs from `handout/style.css`), `charts.js`, `deck.js`, `template.html`, `fonts/` with `fonts.lock.json` (identical to the brief's), `build.py`, `check_deck.mjs` (the drift check against the Beamer deck, the palette guards and the token check), `DESIGN.md` (the contract between the slide files and the class for each Beamer macro).
- **Beamer deck** (`ccc-journal.sty` and `slides.tex` in the Overleaf working copy): the same look in XeLaTeX; the website follows it, never the other way round.
