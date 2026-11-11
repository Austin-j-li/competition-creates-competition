---
name: Competition Creates Competition
description: The journal look in the colours of UCL. One visual system for the website of the paper (the research brief page and the web slides), matched to the Beamer deck of the talk (ccc-journal.sty).
colors:
  paper: "#ffffff"
  ink: "#1c1c1c"
  muted: "#666666"
  hairline: "#c9c9c9"
  grid: "#e6e6e6"
  surface: "#f2f2f2"
  accent: "#361a54"
  rule: "#993bff"
  dark-paper: "#361a54"
  dark-ink: "#fafafa"
  dark-muted: "#ba82ff"
  dark-accent: "#30d6ff"
  dark-rule: "#ba82ff"
  dark-hairline: "#6a4e8a"
  dark-grid: "#4a2d6c"
  dark-surface: "#422464"
typography:
  title:
    fontFamily: "Libertinus Serif, Georgia, serif"
    fontSize: "clamp(1.9rem, 3.4vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.12
  headline:
    fontFamily: "DM Sans, system-ui, Arial, sans-serif"
    fontSize: "clamp(1.55rem, 2.2vw, 1.8rem)"
    fontWeight: 700
    lineHeight: 1.15
  tag:
    fontFamily: "DM Sans, system-ui, Arial, sans-serif"
    fontSize: "0.98rem"
    fontWeight: 700
    lineHeight: 1.3
  body:
    fontFamily: "Libertinus Serif, Georgia, serif"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "DM Sans, system-ui, Arial, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.35
rounded:
  none: "0"
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

# Competition Creates Competition: the journal look in the colours of UCL

## Overview

The website is set like the Beamer deck of the talk (`overleaf` working copy, `ccc-journal.sty`).
The layout is the journal look that the author chose on 29 October 2026. The colours and the sans
face are the ones he chose on 11 November 2026 from four demos (`audit/look_ucl200_2026_11_11/`):
the purples of UCL in its bicentenary year, on a flat, ruled, typographic page. Libertinus Serif
sets the reading text; DM Sans sets titles, tags, labels and controls; Libertinus Math is the symbol
fallback. The paper is white. There are no bars, boxes, fills, cards, pills, shadows or gradients.
Hierarchy comes from the type and from two rules: a bright purple rule (1 to 1.5 px on the page,
3 px on the 1600 by 900 slide stage) and a light hairline.

This is the research site of a PhD student in the colours of the university. It carries no UCL logo
and does not copy the layout of a UCL page.

**Key Characteristics:**
- One palette, one type family pair and one rule grammar across the brief page, the web slides and the Beamer deck.
- Two purples, each in one role. Dark purple is coloured text: titles, tags, the active control, links. Bright purple is every rule, bullet and mark.
- A title is bold sans in dark purple over a rule; a statement is a rule, a bold sans tag in dark purple, the body, a light rule; a takeaway is bold text over a rule; an intuition is italic text over a light rule.
- The title frame of the deck is white paper with a wide margin, as the title block of the brief page. A short bright purple rule, the title in bold serif and the subtitle in regular serif, in dark purple, sit at the head. A grey hairline, the name in bold sans and the department in grey sit at the foot. The author chose purple type on white over white type on a purple ground (11 November 2026).
- Figures draw in ink, the information colour and greys; series differ by dash and marker, never by a third colour.
- Prose and captions stop at the measure; exhibits span the content column.

## Colors

The purples, the blue and the off-white are the official values of the UCL brand pages (Colour and
Bicentenary colours, read 11 November 2026). UCL fixes the ground of each one, and the tokens follow
that: bright purple on white only; heritage blue and mid purple on dark purple only.

- **Paper** (#ffffff): the page and the slide. **Stage** (#e9e9e9): the ground behind a slide in the web deck.
- **Ink** (#1c1c1c): reading text, booktabs rules, the slider track.
- **Dark purple** (#361a54, `--accent`, `--heading`; `cAccent` in the deck): coloured text. Titles and section headings, the tag of a statement, column heads, the active tab, contents entry or control, the current part of the roadmap and of the model strip, links. Also the ground of the dark theme.
- **Bright purple** (#993bff, `--rule`; `cRule` in the deck): the rule under a title, the rule above a statement, a takeaway or a large line, bullets, the underline of the active control, the slider thumb, the focus ring; in figures the information series (`--c-info`, `--chart-2`). On white only.
- **Heritage blue** (#30d6ff): in the dark theme the coloured text, the information series and the short rule of the title block and of the title frame. On dark purple only.
- **Mid purple** (#ba82ff): in the dark theme the rules, bullets, muted text and the grey series. On dark purple only.
- **Off-white** (#fafafa, UCL's screen white): text on dark purple.
- **Muted** (#666666): glosses, subtitles, foot lines, tick labels, inactive controls; in figures the grey series (`--chart-3`).
- **Hairline** (#c9c9c9): light rules, the dotted underline of a registry number, the border of a tooltip. **Grid** (#e6e6e6): chart gridlines and the hairlines inside a table.
- **Surface** (#f2f2f2): the ground of a tooltip. Never a card.
- **Dark theme**: dark purple paper (#361a54), off-white ink, mid purple for muted text and rules, heritage blue for coloured text and the information series. Three tones are derived from dark purple and are not UCL colours: hairline #6a4e8a, grid #4a2d6c, surface #422464; the stage behind a slide is #231137.

### Named Rules
**The Two Roles Rule.** `--accent` is coloured text and `--rule` is every rule, bullet and mark. A border, bullet, underline or figure mark in `--accent`, or body-size text in `--rule`, is a defect. In a diagram a coloured mark or label takes `--c-info`, because dark purple beside ink does not tell two things apart.
**The Ground Rule.** Bright purple never sits on dark purple; heritage blue and mid purple never sit on white. `handout/check_display.py` and `presentation/check_deck.mjs` read the token blocks and fail on a breach, and they fail on a hex outside the palette above.
**The Figure Palette Rule.** A figure uses ink, the information colour and greys (`--chart-1`, `--chart-2`, `--chart-3`, `--c-info`, `--c-cost`), and two series on one panel never share both colour and dash. Bands are the same colours at low opacity. The figures of the Beamer deck are PDF files in orange and teal; the diagram colours of the deck (`cInfo`, `cCost`) match them.
**The Retired Looks Rule.** Two earlier looks must not come back: the oxblood accent of 29 October 2026 (#7A1F1F, #D4908F), and the template of 3 October 2026 that the author rejected as boxed. That template used the same UCL hexes, so its marks identify it: the `--ucl-*` tokens, a gradient, a shadow, a rounded box or pill. The checks and the publisher fail on them.

## Typography

**Reading face:** Libertinus Serif (regular, italic, bold, bold italic). **Apparatus face:** DM Sans (regular, italic, and the semibold as the bold) for titles, tags, labels, tables' heads, legends, controls and the footline. UCL's own face, UCL Sans, is a cut of DM Sans; UCL does not intend it for academic text, so it sets the apparatus only. It is scaled to 90 per cent to sit beside Libertinus Serif (`Scale=0.9` in the deck, `size-adjust` on the web). DM Sans has no small capitals and no Greek. **Symbols:** Libertinus Math, subset to the symbol blocks, as the fallback for Greek letters, relations and operators in text. **Mathematics:** KaTeX on the web, Libertinus Math in the deck; the seam is accepted. Hashes use the system monospace.

### Hierarchy
- **Title** (serif 700): the two lines of the brief's title in dark purple; on the title frame of the deck, the title at 81 px (25 pt in Beamer) and the subtitle at 58 px and weight 400 (16.5 pt), in dark purple.
- **Headline** (sans 700, dark purple): a section heading of the brief; a frame title at 50 px (60 px on the question frame). Both sit over the rule; a subtitle is serif italic in grey under the title, above the rule.
- **Tag** (sans 700, dark purple): the name of a statement ("Proposition 2 · ..."), a column head, the contents heading; 30 px on a slide.
- **Body** (serif 400): 1.15rem at a 66ch measure on the brief; 32 px at 1.3 on a slide (\Body), 28 px inside a statement, 25 px for the small sizes.
- **Label** (sans 400): tabs, the contents, buttons, legends, table heads, the record line; 20 to 26 px on a slide.
- **Gloss and foot line** (serif, muted): 0.95rem on the brief; 28 px and 23 px on a slide.

### Named Rules
**The Run-In Rule.** A labelled paragraph opens with a bold sans run-in word and a period ("Answer.", "In short.", a scenario's name). A statement's name is a tag on its own line, not a run-in.
**The Measure Rule.** Prose, lists and captions stop at the measure; exhibits span the content column.
**The Registry Number Rule.** A registry number is set in the text face with tabular figures and a dotted hairline underline that carries its key on hover. No status word accompanies it.

## Layout

The brief page: at 1024 px and above, a 12.5rem contents rail on the left and a 54rem reading column inside a 72rem page. The title block sits on the paper: a short rule (7.5rem), the serif title on two lines, the sans byline and record line, then the tab row between hairlines. It is not a cover and has no band. The opening question is the large line of the deck: a rule above, bold serif, a light rule below. Each section opens with its sans heading over the rule. Sections are 4.25rem apart. Below 1024 px the rail stacks above the column; at 600 px the body is 1.0625rem.

The web deck is a fixed 1600 by 900 stage with a 44 px tools bar above and a 52 px rail below. A frame has 40 px side padding; the head holds the title, the optional subtitle and the 3 px rule; the body starts under the rule; the takeaway or the intuition is pinned above the foot zone; the footline of a main frame carries the roadmap of the talk in sans on the left, with the current part in bold dark purple, and the text links and the frame number (`n / N`) on the right; a backup page carries the short title and its backup label. The title frame has no footline.

## Elevation & Depth

Flat. No shadows, glows, gradients or layered surfaces. No frame has a painted ground; the title frame is paper as every other frame. A tooltip and a dialog are paper with a hairline or ink border; a dialog backdrop is ink at 45 per cent.

## Shapes

Rectilinear, with no exception. A link in the footline of a slide is sans text in dark purple after a small triangle; it has no box, fill or radius. A step of a flow diagram is text under a rule, not a box. Inputs, the tooltip, the slider thumb (a 4 px bright purple bar on a 1 px ink track) and legend swatches are square.

## Components

- **Title block (brief):** short rule, serif title in dark purple, sans byline, muted record line, tab row; the active tab is dark purple at weight 700 with a 2 px bright purple underline. In the dark theme the short rule is heritage blue. **Title frame (deck):** paper with a 130 px margin; at the head a 220 px bright purple rule, the serif title and the lighter subtitle in dark purple; at the foot a hairline, the name in bold sans in ink and the department in grey. In the dark theme it takes the theme's colours and a heritage blue rule.
- **Section heading:** sans 700 in dark purple over a 1 px rule; the frame title is the same over a 3 px rule.
- **Statement:** rule, tag, body one size down, light rule (`.prop` on the brief; `.statement`, `.resultbox`, `.propblock` on a slide).
- **Takeaway and intuition:** bold over a rule; italic over a light rule; both pinned at the foot of a slide (`.takeaway`, `.intuition`).
- **Column head and label column:** a sans bold head in dark purple over a rule (`.colhead`, the mechanism map's path labels, `.rcol`, `.rpanel`); bold sans labels on the left and text on the right (`.deflist`).
- **Lists:** a small bright purple square bullet; numbered items with a bold number.
- **Tables:** booktabs in the text face with a bold sans head: an ink rule above and below, a hairline under the head, grid hairlines between rows, no vertical rules, no zebra.
- **Figures:** the SVG renderer draws ink, information and grey series over grid-coloured dotted gridlines; sans tick labels; a hairline above the legend and below the plot; the caption opens with a bold sans run-in.
- **Controls:** text in sans with a hairline underline; the active choice in dark purple with a 2 px bright purple underline; the focus ring is 2 px bright purple.
- **Links of a slide:** sans text in dark purple after a small triangle (`.goto`); a bright purple underline on hover.
- **Flow step:** text under a 5 px rule, bright purple or ink (`.fbox`; `flowbox` and `flowcost` in the deck); arrows in grey between the steps.
- **Model strip:** the six parts of the model in sans under the title of the model frames; the current ones bold dark purple, the others grey, light bullets between (`.model-strip`).
- **Footline:** sans, 23 px, grey; in the Beamer deck and on the web a main frame shows the roadmap of the talk there, with the current part in bold dark purple.

## Do's and Don'ts

### Do:
- **Do** set every rule in bright purple or as a hairline, and put the bright purple rule under a title and above a statement, a takeaway or a large line only.
- **Do** keep dark purple for coloured text and bright purple for rules and marks, and let the two mean structure.
- **Do** draw figures in ink, the information colour and greys, told apart by dash and marker.
- **Do** keep prose at the measure and exhibits across the column.
- **Do** compose the dark theme on dark purple with heritage blue and mid purple.

### Don't:
- **Don't** use a fill, card, pill, chip, badge, gradient, glow, shadow, side stripe or rounded box. Nothing is rounded.
- **Don't** add a colour outside the palette, a third figure colour, a decorative illustration or an icon set.
- **Don't** put bright purple on dark purple, or heritage blue or mid purple on white.
- **Don't** use the UCL logo, or lay a page out like an official UCL page.
- **Don't** give the brief page a dark title block or a band: the template of 3 October 2026 had one.
- **Don't** set an eyebrow or kicker above a heading, a label in capitals, a numbered section label, a reading time or a progress bar on the page.
- **Don't** put a number on the motivation frames.

## Where each surface implements the system

- **Research brief page** (`handout/`): `style.css` (tokens, type, layout, components), `template.html`, `charts.js` (the SVG renderer; its fallback tokens repeat the palette), `figures.js` and `explorer.js` (figures through the renderer's tokens), `fonts/` with `fonts.lock.json` (Libertinus Serif and Math from the 7.051 release and DM Sans from the google/fonts repository, all SIL OFL, subset to woff2, pinned by sha256), `build.py` (font faces and preload from the lock), `check_display.py` (the locked faces, the registry numbers, the palette and its grounds, the retired looks), `publish.py` (the retired looks in the staged site).
- **Web slides** (`presentation/`): `deck.css` (the same `:root` tokens; `check_deck.mjs` fails when a shared token differs from `handout/style.css`), `charts.js`, `deck.js`, `template.html`, `fonts/` with `fonts.lock.json` (identical to the brief's), `build.py`, `check_deck.mjs` (the drift check against the Beamer deck, the palette and its grounds, the retired looks and the token check), `DESIGN.md` (the contract between the slide files and the class for each Beamer macro).
- **Beamer deck** (`ccc-journal.sty`, `fonts/dmsans/` and `slides.tex` in the Overleaf working copy): the same look in XeLaTeX; the website follows it, never the other way round.
