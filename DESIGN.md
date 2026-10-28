---
name: Competition Creates Competition
description: The ruled document. One visual system for the website of the paper, the research brief page and the web slides. The Beamer deck in Overleaf uses a classic Beamer theme instead.
colors:
  paper: "#fbfcfc"
  paper-stage: "#e7eaee"
  ink: "#1e2530"
  muted: "#5b6573"
  hairline: "#c7cdd5"
  grid: "#e4e8ec"
  surface: "#f1f3f5"
  information: "#b54b00"
  cost: "#006459"
  fail: "#b0261c"
  slate: "#1a1f26"
  slate-stage: "#10141a"
  slate-surface: "#232931"
  slate-ink: "#e8ecf1"
  slate-muted: "#a3adb9"
  slate-hairline: "#3d4652"
  slate-grid: "#2a313a"
  slate-information: "#f6a157"
  slate-cost: "#46b3a8"
  slate-fail: "#f29a92"
typography:
  display:
    fontFamily: "Archivo, system-ui, Arial, sans-serif"
    fontSize: "clamp(2.2rem, 4vw, 3rem)"
    fontWeight: 600
    lineHeight: 1.02
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Archivo, system-ui, Arial, sans-serif"
    fontSize: "clamp(1.6rem, 2.2vw, 1.85rem)"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.012em"
  title:
    fontFamily: "Archivo, system-ui, Arial, sans-serif"
    fontSize: "1.12rem"
    fontWeight: 600
    lineHeight: 1.25
  body:
    fontFamily: "STIX Two Text, Georgia, Times New Roman, serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Archivo, system-ui, Arial, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 500
    lineHeight: 1.35
rounded:
  none: "0"
spacing:
  hair: "1px"
  rule: "2px"
  xs: "0.35rem"
  sm: "0.7rem"
  md: "1rem"
  lg: "1.75rem"
  xl: "2.5rem"
  section: "4.5rem"
components:
  title-block:
    textColor: "{colors.ink}"
    typography: "{typography.display}"
    padding: "0 0 1.6rem"
  section-heading:
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    padding: "0.9rem 0 0"
  text-control:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.15rem 0"
  tab-active:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    padding: "0.75rem 0 0.7rem"
  statement:
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: "0.9rem 0 0.15rem"
---

# Design System: Competition Creates Competition

## Overview

**Creative North Star: "The Ruled Document"**

The paper's two web surfaces are set as one document from the paper's own apparatus: a
research brief page and a web slide deck, both read by finance and economics
professors, the author's supervisor and seminar audiences. The page is ink on cool white paper,
slate in the dark theme. Structure comes from two rule weights and from type, never from fills:
a 2 px ink rule sits above the title block and above each section heading of the brief, under
the title of each slide and above the title of the deck; 1 px hairlines carry everything else
(the tabs, the contents, the statement of a proposition, tables, figure frames, the explorer).
The reading column is STIX Two Text at a real measure; titles, headings, tables, figure text and
every control are Archivo. Mathematics is KaTeX on the web and STIX Two Math in the deck.

Colour means something or is absent. The chrome has no colour: links, tabs, buttons, the focus
ring, the slider, the progress rule and the theme control are ink or grey. Two concept colours
appear only inside figures, charts, diagrams and their keys: the information colour for the
target-payoff spread and the information chain, the cost colour for preparation costs, the
floor and the window. The purple "UCL family" palette of an earlier design is rejected on every
surface, and the build checks refuse it.

The page reads as written once, in the register of the paper: a run-in bold word opens a labelled
paragraph ("Answer.", "In short.", the name of a scenario, the title of a proposition); there are
no label capitals, no eyebrow or kicker lines, no numbered section labels and no reading-time
elements. Registry numbers are set in the text face with tabular figures and a faint grey dotted
underline that carries their provenance on hover.

**Key Characteristics:**
- One palette, one type pairing and one rule grammar across the brief page and the web slides. The Beamer deck is outside this system (see the rule below).
- Hierarchy by rule weight and type, never by fill, card, pill, shadow, gradient or side stripe.
- Chrome in ink and grey; the two concept colours live inside exhibits only.
- Exhibits span the content column; prose and captions stop at the measure.
- Every control is text with an underline; the active choice carries a 2 px ink underline.

## Colors

A cool neutral scale from paper to ink, and two concept colours reserved for exhibits.

### Primary
- **Ink** (#1e2530): all reading text, headings, rules, the active underline, the focus ring, the slider track and thumb, the progress rule. On the slate theme ink is #e8ecf1.

### Secondary
- **Information** (#b54b00; #f6a157 on slate): the target-payoff spread, the information chain, the branches along which a purchase recruits, the posterior band. Inside figures, charts, diagrams and their keys only.
- **Cost** (#006459; #46b3a8 on slate): preparation costs, the preparation threshold, the floor, the window, the cost line of a diagram. Inside figures, charts, diagrams and their keys only.

### Neutral
- **Paper** (#fbfcfc): the page and the slide; **Stage** (#e7eaee): the ground behind a slide in the web deck.
- **Slate** (#1a1f26) and **Slate stage** (#10141a): the dark theme's page and ground.
- **Muted** (#5b6573; #a3adb9 on slate): secondary text, the subtitle of a slide, tick labels, captions' secondary runs, inactive tabs and controls, the frame number.
- **Hairline** (#c7cdd5; #3d4652 on slate): 1 px rules, the dotted underline of a registry number, the border of a tooltip.
- **Grid** (#e4e8ec; #2a313a on slate): chart gridlines, the hairlines inside a ledger or a contents list.
- **Surface** (#f1f3f5; #232931 on slate): the only tint, used by a tooltip's ground or a hover; never a card.
- **Fail** (#b0261c; #f29a92 on slate): the debug banner and an explorer warning only.
- **Selection**: ink at 14 per cent on paper, slate ink at 22 per cent on slate; never a concept colour.

### Named Rules
**The Chrome Has No Colour Rule.** Links, tabs, buttons, the focus ring, the progress rule, the slider, the theme control and the pager are ink or grey. A coloured control is a defect.

**The Two Concept Colours Rule.** Information orange and cost green appear only inside a figure, a chart, a diagram or its key, and each always means the same thing. The information path of the mechanism map and the cost box of a slide diagram are keys in this sense. No third colour is introduced, and no purple of the rejected palette (#361A54, #993BFF, #BA82FF) appears anywhere.

**The Dark Theme Is Composed Rule.** Slate is a second paper, not an inversion: ink lightens to #e8ecf1, the hairline to #3d4652, and the two concept colours are lightened to #f6a157 and #46b3a8 so that they keep their contrast on slate.

## Typography

**Display Font:** Archivo (variable weight and width; with system-ui, Arial)
**Body Font:** STIX Two Text (with Georgia, Times New Roman)
**Label/Mono Font:** Archivo for labels, controls, tables and figure text; Fira Mono only for file hashes; "CCC Symbols" (a KaTeX Main subset) as the fallback for arrows and relations.

**Character:** a scholarly text face carries the reading and a sober grotesque carries the apparatus, so that the page reads as the paper's own document with its instruments set apart by family rather than by colour. Numbers are tabular everywhere.

### Hierarchy
- **Display** (600, clamp(2.2rem, 4vw, 3rem), 1.02, width 112%): the title of the brief page; the title of the deck at 48 px and width 112% on the 1600 by 900 stage.
- **Headline** (600, clamp(1.6rem, 2.2vw, 1.85rem), 1.15): a section heading of the brief, under its 2 px rule; a slide title at 44 px on the stage.
- **Title** (600, 1.12rem, 1.25): a subsection heading of the brief; the name of a result box on a slide (26 px).
- **Body** (400, 1.125rem, 1.6): the reading column at a 64ch measure on the brief; 33 px at 1.32 on a slide. The subtitle of the brief is the body face in italic; a slide subtitle is the body face in muted grey (28 px).
- **Label** (500 or 600, 0.85 to 0.98rem, 1.35, sentence case): tabs, the contents, buttons, legend entries, table heads, captions' opening words, the record line under the byline; 19 to 23 px on the stage.
- **Mathematics**: KaTeX at 1.02 em on the web. The seam between KaTeX and STIX Two Text is accepted.

### Named Rules
**The Run-In Rule.** A labelled paragraph opens with a bold Archivo run-in word at 0.93 em followed by a period ("Answer.", "In short.", "An illustrative sale process.", "Proposition 2 · Competition creates competition."). No label sits above a heading or a paragraph in capitals, small capitals or letterspacing.

**The Measure Rule.** Prose, lists and captions stop at the measure (64ch on the brief; a text column on a slide). Exhibits (figures, tables, the stepper, the mechanism map, the explorer, the ledger) span the content column.

**The Registry Number Rule.** A registry number is set in the text face with tabular figures, never monospace, with a 1 px dotted hairline underline that darkens on hover and carries the key as a title. No status word accompanies it.

## Layout

The brief page is a document with a narrow apparatus column: at 1024 px and above, a 12.5rem contents rail on the left, sticky, and a 54rem reading column, inside a 72rem page with 2rem side padding and a 3.5rem gutter. Below 1024 px the rail stacks above the column. Vertical rhythm comes from a 0.35 / 0.7 / 1 / 1.75 / 2.5rem scale with 4.5rem between sections (3rem under 1024 px). The title block opens with the 2 px rule, then the title, the italic subtitle, the byline and the record line, then the tab row between two hairlines. The opening question and its answer sit at the top of the column without a rule of their own; each section opens with its 2 px rule and heading. A proposition is a statement between two hairlines; a fold is a summary between hairlines with a "+" that becomes a minus; a nested fold has a 1 px left hairline. Tables are booktabs: a 1 px ink rule above and below, a hairline under the head, no vertical rules, no zebra. Figures carry a hairline above the legend and below the plot. The number ledger is a two-column list between ink rules; the parameter ledger is a wrapped row between hairlines.

The web deck is a fixed 1600 by 900 design surface scaled to the window, with a 44 px tools bar above and a 52 px rail below, both on paper with a hairline. A slide has 26 px top and 56 px side padding; the head holds the title and the frame number on one line, the subtitle under it and the progress rule at the bottom (done fraction in 2 px ink over a full-width hairline; a backup carries the full 2 px rule). The body is a column; a takeaway sits at the bottom above a 2 px rule; link buttons sit on the right of the foot. Columns inside a slide use 30 to 40 px gaps.


At 760 px and below the mechanism map and the PDF list fall to one column, the stepper to three tabs; at 600 px and below the body is 1.0625rem, the explorer's slider takes a row of its own and the readouts fall to two columns; at 480 px the tabs tighten and the stepper falls to two tabs. The web deck hides the secondary tools under 760 px and shows only the current part in the rail.

## Elevation & Depth

Flat. There are no shadows, no glows, no gradients and no layered surfaces. Depth is carried by the two rule weights alone: a 2 px ink rule marks a title or a section, a 1 px hairline marks everything inside it. A tooltip and a dialog are paper with a 1 px ink or hairline border; a dialog backdrop is ink at 45 per cent.

### Named Rules
**The Two Rule Weights Rule.** A rule is 2 px ink or 1 px hairline, nothing else. A coloured rule exists only as the key of a path or a box inside an exhibit (the information path of the mechanism map, the cost box and cost step of a slide diagram).

## Shapes

Rectilinear. Every corner is square (radius 0): buttons, inputs, the tooltip, the dialog, the slider thumb (a 4 px by 22 px ink bar on a 1 px track), legend swatches and the skip link. There are no pills, chips, badges, cards or side stripes. Markers inside charts are circles and lines because they are data, not chrome.

## Components

### Title block
- **Brief page:** the 2 px rule, then the title (Display), the subtitle in italic body type, the byline in Archivo at 1rem, the record line in muted Archivo at 0.88rem ("Theory working paper · Text revised …"), then the tab row. The theme control sits at the top right as a text control.
- **Web deck:** the cover is a ruled block on paper: the title between a 2 px rule and a hairline, the author in Archivo 32 px, the institute in muted body type with a hairline under it, a one-line hint in muted Archivo 18 px.

### Section heading
- A 2 px ink rule with 0.9rem below it, then the heading (Headline), 1.4rem to the first paragraph. Subsection headings (Title) carry no rule.

### Tabs, contents and controls (the one control grammar)
- **Tabs:** text in Archivo between two hairlines; the active tab is ink at weight 600 with a 2 px ink underline; others are muted and turn ink on hover.
- **Contents:** a numbered list in Archivo at 0.9rem under a hairline, each entry on a grid hairline; the current section is ink at weight 600.
- **Buttons and links styled as actions:** Archivo text with a 1 px hairline underline that darkens on hover; the primary action carries a 2 px ink underline. A link in prose is ink with a hairline underline.
- **Choice rows** (the stepper, the explorer presets, the equilibrium picker, the viewer bar, the segmented choices of a slide): text with a transparent 2 px underline that becomes ink on the chosen item.
- **Legend entries:** a swatch and Archivo text; a switched-off entry is struck through and muted.
- **Slider:** a 1 px ink track and a 4 px ink thumb; the readout in body type with tabular figures.
- **Focus:** a 2 px ink outline at 2 px offset, everywhere.

### Statement box (propositions)
- **Brief page:** between two hairlines with 0.9rem above; the title runs in ("Proposition 2 · Competition creates competition."), the statement follows in body type, a fold with a left hairline holds the full statement.
- **Web deck:** a result box is ruled 2 px above and below with a hairline under its Archivo title; numbered items hang at 64 px.

### Tables
- Booktabs: 1 px ink rules above and below, a hairline under the Archivo head, numbers right-aligned and tabular, row heads at weight 400. On a slide, 27 px (20 to 25 px for dense backups) with a 2 px rule above the head and under the last row, a highlighted row ruled above and below in 2 px ink.

### Figures and charts
- The SVG renderer draws ink curves, the two concept colours and muted grey; gridlines are grid-coloured dotted; axes titles and ticks are Archivo 12 to 13.5 px. A hairline sits above the legend and below the plot; the caption opens with a bold Archivo run-in ("Figure 1.") and stays at the measure. Hover readouts are paper with a hairline border. On a slide the renderer draws at a zoom of 1.4.
- The `_talk` figure PDFs, which the Beamer deck includes, use this palette: in-figure text and axes in ink, tick labels muted, the quiet branch and region boundaries in ink, the branches a purchase recruits along and the posterior band in the information colour, the preparation threshold in the cost colour, the floor branches in muted grey, the bands as the information tint (#f5ece5) and the neutral tint (#ebedee) on the slide paper colour. The manuscript figures keep their own navy and brick palette.

### Diagrams
- The mechanism map: two columns under a 1 px ink rule each, the information path's rule and its run-in in the information colour, the end of each path over a hairline in Archivo.
- Slide process steps and timeline boxes: a 1 px ink rule above each box, a 2 px cost-coloured rule on the cost step, arrows in muted grey.

### Navigation of the web deck
- The tools bar: the way back to the brief, the deck title in muted grey, text controls with hairline underlines. The rail: the parts as text, the current part underlined in 2 px ink; the pager with ink arrows, the counter and the step label in tabular figures.

### Colophon (brief)
- The colophon under a hairline in muted Archivo at 0.85rem, with the build line in Fira Mono.

## Do's and Don'ts

The slop list these surfaces are checked against, by the design detector and by eye.

### Do:
- **Do** set every rule at 2 px ink or 1 px hairline, and use the 2 px rule only above the title block, above a section heading, under a slide title and above the deck title.
- **Do** begin a labelled paragraph with a bold Archivo run-in word and a period.
- **Do** keep prose at the measure and let exhibits span the content column.
- **Do** keep the two concept colours inside exhibits and their keys, each with its one meaning.
- **Do** set numbers in the text face with tabular figures and the dotted provenance underline.
- **Do** make every control text with an underline, the active one in 2 px ink, and give every control a visible ink focus ring.
- **Do** compose the dark theme on slate with its own ink, hairline and lightened concept colours.

### Don't:
- **Don't** use a fill, card, pill, chip, badge, gradient, glow, shadow, side stripe or rounded corner.
- **Don't** colour the chrome: no coloured link, tab, button, focus ring, slider, progress bar or theme control.
- **Don't** use any purple of the rejected palette (#361A54, #993BFF, #BA82FF or the --ucl-* tokens); the brief check, the deck check and the publisher fail on it.
- **Don't** set an eyebrow or kicker above a heading, a label in capitals or small capitals, a numbered section label, a reading time, a section time or a progress bar on the page.
- **Don't** set numbers or labels in monospace; Fira Mono is for file hashes only.
- **Don't** add a third colour, a decorative illustration, a background figure or an icon set; an arrow is the one drawn glyph.
- **Don't** put a number on the motivation slides (the title and the three question frames).

## The Beamer deck uses a classic theme

Rule from 28 October 2026. The slide deck in Overleaf (`slot/manuscript/slides.tex`) uses a stock
classic Beamer theme, now Madrid, loaded by `ccc-classic.sty`. The website keeps the ruled
document: the research brief page and the web slides under `/talk/` follow this file. Every later
change to the Overleaf slides keeps a classic Beamer theme and never brings the ruled look into
Beamer; every later change to the website keeps the ruled look. The words, numbers, frame order,
titles, subtitles and links stay identical between the two decks (`presentation/check_deck.mjs`);
only the look differs.

## Where each surface implements the system

- **Research brief page** (`handout/`): `style.css` (tokens in its `:root` blocks, type, layout, components), `template.html` (the title block, tabs, contents, opening question, paper and talk tabs, colophon), `charts.js` (the SVG renderer; its fallback tokens repeat the palette), `figures.js` and `explorer.js` (the figures and the explorer through the renderer's tokens), `fonts/` with `fonts.lock.json` (STIX Two Text, Archivo, Fira Mono, the symbol fallback), `build.py` (generates the font faces and the preload from the lock, assembles the page), `check_display.py` (the locked faces, the registry numbers, the palette guard), `publish.py` (the palette guard on the staged site and the main-branch gate), `README.md`.
- **Web slides** (`presentation/`): `deck.css` (the same `:root` tokens; `check_deck.mjs` fails when a shared token differs from `handout/style.css`), `charts.js`, `deck.js`, `template.html`, `fonts/` with `fonts.lock.json`, `build.py`, `check_deck.mjs` (the drift check against the Beamer deck, the palette guard and the token check), `DESIGN.md` (the contract between the slide files), `README.md`.
- **Beamer deck** (`slot/manuscript/`), outside the ruled document: `ccc-classic.sty` (the stock Madrid theme and the layout macros the frames use), `slides.tex` (the frames only; loads the style file), `figures/*_talk.pdf` (from `audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py`, slide palette), `latexmkrc` (XeLaTeX for the deck, pdfLaTeX for the manuscript and the comparison note), `START_HERE.txt`.
