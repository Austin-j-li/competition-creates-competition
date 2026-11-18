---
name: Competition Creates Competition
description: The navy plate. One look for the website of the paper, on its two surfaces, the front page (research brief, paper, talk tabs) and the seminar talk presented from the browser. Black ink for text, navy for the frame, teal for position and links, orange for one meaning.
colors:
  ground: "oklch(0.985 0.002 250)"
  ink: "oklch(0.20 0.01 260)"
  ink-2: "oklch(0.40 0.012 260)"
  frame: "oklch(0.35 0.093 259)"
  mark: "oklch(0.52 0.088 190)"
  accent: "oklch(0.54 0.154 46)"
  reverse: "#ffffff"
  screen-grey: "oklch(0.62 0.008 260)"
  trace-grey: "oklch(0.70 0.008 260)"
  trace-pale: "oklch(0.80 0.006 260)"
typography:
  stage-cover:
    fontFamily: "Jost, Futura, Century Gothic, sans-serif"
    fontSize: "100px"
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: "-0.022em"
  stage-title:
    fontFamily: "Jost, Futura, Century Gothic, sans-serif"
    fontSize: "56px"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.012em"
  stage-sub:
    fontFamily: "STIX Two Text, Times New Roman, serif"
    fontSize: "28px"
    fontWeight: 400
    lineHeight: 1.3
  stage-body:
    fontFamily: "STIX Two Text, Times New Roman, serif"
    fontSize: "30px"
    fontWeight: 400
    lineHeight: 1.32
  stage-statement:
    fontFamily: "STIX Two Text, Times New Roman, serif"
    fontSize: "28px"
    fontWeight: 600
    lineHeight: 1.3
  stage-label:
    fontFamily: "Jost, Futura, Century Gothic, sans-serif"
    fontSize: "24px"
    fontWeight: 500
    lineHeight: 1.28
  stage-small:
    fontFamily: "STIX Two Text, Times New Roman, serif"
    fontSize: "22px"
    fontWeight: 400
    lineHeight: 1.3
  stage-foot:
    fontFamily: "Jost, Futura, Century Gothic, sans-serif"
    fontSize: "21px"
    fontWeight: 500
    lineHeight: 1.3
  page-title:
    fontFamily: "Jost, STIX Two Text, Futura, sans-serif"
    fontSize: "clamp(2.3rem, 5.4vw, 4rem)"
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: "-0.022em"
  page-headline:
    fontFamily: "Jost, STIX Two Text, Futura, sans-serif"
    fontSize: "clamp(1.6rem, 2.4vw, 2rem)"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.012em"
  page-subhead:
    fontFamily: "Jost, STIX Two Text, Futura, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.004em"
  page-body:
    fontFamily: "STIX Two Text, Times New Roman, serif"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1.55
  page-statement:
    fontFamily: "STIX Two Text, Times New Roman, serif"
    fontSize: "1.2rem"
    fontWeight: 600
    lineHeight: 1.45
  page-label:
    fontFamily: "Jost, STIX Two Text, Futura, sans-serif"
    fontSize: "0.92rem"
    fontWeight: 500
    lineHeight: 1.3
rounded:
  none: "0"
spacing:
  keyline-heavy: "3px"
  keyline-thin: "1.5px"
  keyline-inner: "1px"
  stage-margin: "80px"
  stage-top: "40px"
  stage-foot: "66px"
  page-width: "73rem"
  page-column: "53.5rem"
  page-contents: "12rem"
  page-gutter: "3.5rem"
  page-measure: "29.5em"
  page-section: "5rem"
components:
  statement-band:
    backgroundColor: "{colors.frame}"
    textColor: "{colors.reverse}"
    typography: "{typography.stage-statement}"
    rounded: "{rounded.none}"
    padding: "20px 9% 22px 36px"
  entry-cell:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.reverse}"
    rounded: "{rounded.none}"
    padding: "8px 18px 9px"
  strong-column-head:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.accent}"
    typography: "{typography.stage-label}"
  stage-foot:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink-2}"
    typography: "{typography.stage-foot}"
    height: "66px"
  tab:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink-2}"
    typography: "{typography.page-label}"
    padding: "0.7rem 0 0.6rem"
  tab-selected:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.frame}"
  link:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.mark}"
---

# Design System: Competition Creates Competition

## Overview

**Creative North Star: "The Navy Plate"**

The site is set as the diagram plate of an economics textbook on bright white stock. Each ink has one job: black for text, every thin keyline and the line marks of a figure; navy for the frame of the page; teal for where the reader is and where a link leads; orange for one meaning. The navy, teal and orange are the colours of the PowerPoint of the talk; the finish is the site's own. The grammar is printing grammar. Ink is flat. Structure is drawn with keylines. An area that a screen design would tint is filled with a screen of fine parallel lines. Titles and labels are set in Jost, running text in STIX Two Text, mathematics in KaTeX.

The look covers two surfaces. The front page is a reading page: a title face, three tabs (research brief, the paper, the seminar talk), a contents rail and one reading column. The seminar talk is a fixed stage of 1600 by 900 px with 65 pages (a title, 20 main pages, 44 backup pages), scaled to the window and driven by the keys a clicker sends. Both surfaces take their colours, families, keyline weights and figure tokens from `design/tokens.css`. Sizes are set per surface: pixels on the stage, rem on the reading page.

The site has one light theme. It has no dark theme and no theme switch.

**Key Characteristics:**
- One colour, one job. Black carries text, every thin keyline and the line marks of a figure. Navy carries the frame: titles, labels, the band, solid figure areas and closing statements. Teal carries position and passage: the heavy keyline, the current marks and links. Orange carries one meaning.
- Figures read in greyscale: a distinction is a stroke pattern, a marker shape, a weight or a line screen.
- Keylines in fixed weights, one weight per role, running the full measure without a break. Thin keylines are black; the heavy keyline is teal.
- A solid navy band for the main statement of a talk page. Other statements are bold navy text between thin keylines, or bold navy text alone.
- Navy registration crosses on the two title faces. No other ornament.
- On the stage, a click is a stored state and ink is laid down along its own direction.

## Colors

White stock and black ink, three colours each with one job, and light greys that draw only line screens and one comparison trace. Navy, teal and orange are the PowerPoint's (1B3A6B, 0B7A75 and B54B00 in hex), written in the token file in the `oklch()` form.

### The frame
- **Navy** (`frame`; `--frame`, `--band-bg`, `--fig-share`): the frame of every page. On the talk: the page title and the cover title, the name on the cover, the tag of the sub line, run-in labels, column heads, side heads and lead-ins, the stop heads of main page 7, table heads and row labels (the backups' number tables among them, and the panel heads), the statement band, the solid areas of the payoff figure (main page 8) and the split bars (main page 13) with their outlines and their line screens, closing statements set plain or between keylines without a label, the label of a labelled closing row, and the four registration crosses. On the backups also the formal run-in labels, the proof numbers of B2 and the counted numbers of B13. On the front page: the title, section headings and subheadings, the author's name, the opening question and its "Answer.", run-ins, scenario names, the proposition tag, table heads, legend titles, the "Figure 1." run-in of a caption, disclosure summaries, the "Contents" label, the labels of the mechanism, the stage numbers of the stepper and the numbers of an ordered list, the explorer's title and the letters of its picker, the viewer label, the text of a selected tab, stage, preset, choice or viewer button, the takeaway ("In short.") and the two registration crosses.

### Position and passage
- **Teal** (`mark`; `--mark`, `--link`, `--rule-strong`): the heavy keyline (under a title or heading, on the cover, round the current thumbnail of the overview, the top edge of the explorer); the current part of the roadmap and the current stage of the stage strip; the line under a selected tab, stage, preset, choice, viewer button and the pressed Strength button of the control row; the 2 px marker under the current contents entry; the strength marker on the entry chart; and every link on both surfaces, with its underline.

### The one meaning
- **Orange** (`accent`; `--accent`, `--fig-accent`): the price brings the costly rival in. On the talk it marks the Strong column head and its Entry cell (main pages 9 and 16, backups B11 and B19), the line screen of the strong column, the branch of the entry chart where entry is above its floor together with the ends of that branch and the dot, tick and label of the strong incumbent, the label "purchases in class H expected" on that branch (main page 19), the costly rival's preparation and its arrow on main page 14, the strong row of the outcome table on backup B18, the branch with informed orders, its ends and its arrowhead on the research chart (backup B21 and the second page of B12), the branches of the chart on B3, and the entry part of the price-impact figure (B13) and its label. On the front page it marks the figure branches and points where a purchase brings in the high-cost rival, that mark on the belief line, and the matching cells and totals of the explorer.

### Neutral
- **White stock** (`ground`; `--ground`): the page, the stage, the ground of tooltips, the overview and the blank screen. It has no warmth.
- **Black ink** (`ink`; `--ink`, `--rule`, `--fig-ink`, `--focus-ring`): text, every thin and inner keyline, axes, ticks, branches other than the orange one, dots other than the strong incumbent's, brackets, leader lines, every label inside a figure, the factor underlines of main page 11, the page number of the talk, the site name of the control row, the overview's headings, the focus outline and the selection ground. On the front page the STIX row labels of a table and the bullet squares are black. Bold text-face words inside running text (for example "Reserve." on B4 or the strands of B14's first page) are emphasis, not labels, and stay black, as does the text of a labelled closing row.
- **Secondary ink** (`ink-2`; `--ink-2`): subtitles, glosses, notes, the foot and the roadmap's other parts, the other stages of the stage strip, axis titles, unselected tabs and contents entries. Apart from text it draws only guide lines that carry no data, such as the dotted underline of a registry number.
- **Reverse white** (`reverse`; `--band-ink`, `--accent-ink`): type set on the navy band or on the solid orange cell.
- **Screen grey** (`screen-grey`; `--scr-page`, and `--scr-ink` on the entry chart): the lines of a screen that lies behind other marks in a chart. It never fills an area flat and never sets text.
- **Trace greys** (`trace-grey`, `trace-pale`): the trace of the full model on main page 18 of the talk. The token `--trace-grey` is declared in `design/tokens.css`; the shipped trace is the paler value, drawn as a broad stroke.

### Contrast
WCAG ratios measured for the three colours on the paper and for white type on them:

| Colour | On the paper | White type on it |
|---|---|---|
| Navy | 10.8 | 11.3 |
| Teal | 5.0 | 5.2 |
| Orange | 5.1 | 5.3 |

Black ink is 17.0 on the paper and secondary ink 8.8. Navy against black ink is 1.6, so the two differ in hue, not in darkness: on a washed-out projector navy reads as black.

### Named Rules
**The One Meaning Rule.** Orange means only that the price brings the costly rival in. It is never used for a link, a focus outline, a tab, a selected control, a current mark, a heading, a bullet or decoration. Main pages 1 to 6 of the talk carry no orange: the sale process, the question, the received answer, the preview, the related literature and the players.

**The Frame Rule.** Navy carries no meaning. It sets titles, labels, the band, solid figure areas and closing statements, and it is never the only thing that tells two items apart: navy against black is 1.6:1. Running text is black, never navy.

**The Mark Rule.** Teal marks position and passage only: where the reader is, and where a link leads. It never marks data, never fills an area and never sets running text. Every current mark carries a second code beside its colour: the current part and the current stage are set at 600 against 500; a selected tab, stage, preset, choice, viewer button or contents entry has a line under it, and all of them but the presets are also set at 600; a link is underlined. Under red-green colour blindness teal turns to a grey-blue close to the secondary ink, and the weight, line or underline still carries the mark.

**The Greyscale Rule.** Every distinction in a figure other than the one orange carries a second code: solid against dashed against dotted, a filled dot against an open ring, a heavy line (6 px on the stage) against a normal one (3 px), a solid fill against a line screen. In grey, navy prints as a dark grey just lighter than black, and orange and teal print as one mid grey; no distinction rests on them. A figure printed in grey loses nothing.

**The Screen Rule.** An area is never tinted. It is a line screen: an SVG pattern in a figure, drawn in the ink of the solid area it pairs with (navy on main pages 8 and 13, screen grey elsewhere), or the one CSS repeating-line screen (`--tint-fill`, orange toward the paper) behind the strong column of a table. A figure's areas are one ink: a solid navy area, its navy screen and their navy outlines. Type that sits on a screen carries a hard halo of paper so the lines give way to the letters.

## Typography

**Title and label face:** Jost, weights 500 and 600 (fallbacks Futura, Century Gothic). It has no Greek, so on the front page its stack falls back to STIX Two Text for Δ, τ, λ and μ.
**Text face:** STIX Two Text, weights 400 and 600, upright and italic (fallback Times New Roman).
**Mathematics:** KaTeX, at 1.1em on the stage and 1.02em on the front page.
**Monospace:** the system monospace, for file hashes and the build line of the front page only.

**Character:** a geometric sans in the tradition of mid-century textbook plates over a scientific text face that sits beside the mathematics. Bold is 600 in both faces. No other weights are shipped: a request for 700 renders at 600.

### Hierarchy

On the stage (pixels at 1600 by 900):
- **Cover title** (Jost 600, 100 px, line height 1.04, tracking -0.022em, navy): the title page. The subtitle is STIX 400 at 40 px, the name Jost 600 at 30 px in navy, the affiliation STIX at 26 px in secondary ink.
- **Page title** (Jost 600, 56 px, 1.1, -0.012em, navy): one per page, over the heavy keyline. The formal backup pages set it at 52 px.
- **Sub line** (STIX 400, 28 px, 1.3, secondary ink): one line under the title. Its opening tag ("Result 2", "Discussion") is Jost 600 in navy.
- **Body** (STIX 400, 30 px, 1.32). Dense pages step down to 26 px, and to 22 px on the fullest backup pages. Rows of run-in and matrix tables on the main pages are set in two tiers: 27 px (main pages 9, 10, 11) and 24 px (main page 16, backups B14 and B18). The side columns of main pages 18 and 19, the fullest sides, are set at 24 px. Where an opening page has little text the body steps up one tier, to 34 px (1.3): the columns of main pages 2 and 4 (with page 4's lead line) and the rows of main pages 3 and 12.
- **Statement** (STIX 600): 28 px (1.3) in the band, in white; 30 px (1.3), in navy, for the closing statement of a main page set plain or between keylines.
- **Label** (Jost 500, 24 px): table heads and row labels in navy, figure labels in ink, run-in labels (600) in navy. Row numbers are Jost 600.
- **Small** (22 px): notes in STIX italic, figure labels in Jost 500.
- **Foot** (Jost 500, 21 px, secondary ink): roadmap and links; the current part and the links are 600 in teal, the page number 600 in ink.

On the front page (root 20 px text, 17 px at 600 px wide and below):
- **Title** (Jost 600, clamp 2.3rem to 4rem, 1.04, -0.022em, at most 18ch, navy): the paper's title. The subtitle is STIX 400 at 1.25rem to 1.65rem.
- **Section heading** (Jost 600, clamp 1.6rem to 2rem, 1.15, navy): over the heavy keyline.
- **Subheading** (Jost 600, 1.2rem, 1.25, navy).
- **Body** (STIX 400, 1.25rem, 1.55) at a measure of 29.5em.
- **Statement** (STIX 600, 1.2rem, 1.45, navy): the takeaway. The opening question is Jost 600 at 1.4rem to 1.75rem, in navy.
- **Label** (Jost 500, 0.88rem to 1rem): tabs, contents, legends, table heads (600), controls, the record line and the colophon.
- **Caption and note** (STIX 400, 0.98rem, secondary ink).

### Named Rules
**The Twenty Pixel Rule.** No text on a page of the stage is smaller than 20 px. The room is lit and the screen is a projector.

**The Run-In Rule.** A labelled paragraph opens with a Jost 600 run-in in navy: "Answer.", "In short.", a scenario's name, "Result 2", "Proposition A.2". The formal backup pages B2 and B8 set their run-in labels ("Lemma A.1", "Proposition 1") in STIX 600, also navy. A bold word in the text face inside running text is emphasis, not a run-in, and stays black. No label is set in capitals and no small label sits above a heading.

**The Tabular Rule.** Numbers in tables, axis ticks, readouts and the page number use lining tabular figures.

## Layout

**The stage.** 1600 by 900 px, scaled to fit the window and centred. A page is a grid of three rows: head, body, foot. Side margins are 80 px and the top margin is 40 px. The head holds the title, an optional one-line sub line or stage strip of fixed height, and the heavy keyline, so the body starts at the same height on every page. The body starts 26 px below the keyline. The foot is 66 px high under a thin keyline. The title page has no foot: the title block starts at 300 px from the top over a heavy keyline, and the name and affiliation sit on a thin keyline at 770 px.

**Column lines of the stage.** The body of a main page is x 80 to 1520, y 193 to 810. Every main page takes its vertical lines from one set:
- **Thirds:** 80, 576, 1072 (columns of 448 px, gutters of 48).
- **Halves:** 80, 824 (columns of 696 px, gutter of 48).
- **Label column:** the label in 80 to 286, text from x = 314. Columns after a label column start at 314 and set their own widths: thirds of 370 px (main page 2), halves of 579 px (main page 20), and the unequal columns of main pages 6 and 11, where one column holds more text or a longer head.
- **Figure and side:** the figure mount in 80 to 930, the side column from 947 to 1520. On main pages 17, 18 and 19 the plot frame of the entry chart is x 197 to 905, y 285 to 677 and does not move between them; the blocks of their side columns are separated by thin keylines.

**Arrangements of the main pages.** Six arrangements cover the 20 pages; backups B19 to B21 keep the arrangement they had as main pages.
- **Columns** (2, 4, 5, 11, 20 and backup B20): two or three headed columns from a thin keyline at y = 241 (y = 278 on page 4, which sets a lead line above them), over one conclusion row whose keyline is at y = 590 on every such page, so the answer appears on the same line from page to page. Page 2 and page 20 name their columns in the label column; page 20 sets its statement row first; page 11 sets its columns under the equation.
- **Rows** (1, 3, 6, 12): run-in rows on the label column, a thin keyline under each. Page 6 has two tiers of heads on a keyline. Page 3 closes with a labelled row ("This paper") whose keyline is at y = 590, the line of the Columns conclusion.
- **Axis** (7): one thin rule at y = 270 with a solid dot at each stop, heads above the rule and text hanging under it. The rule arrives whole with the first stop. The four stage heads of page 7 travel into the stage strip of page 8.
- **Figure and side** (8, 13, 17, 18, 19 and backup B21; mirrored on 10): the element the first click reveals sits on the left. A claim closes the side between thin keylines.
- **Figure over text** (14, 15): a figure strip over the full measure, ruled rows under it (page 14 unlabelled, page 15 on the label column).
- **Table** (9, 16 and backup B19): a matrix table over the full measure, then the statement, then the note. The column heads of page 16 travel to their labels on the chart of page 17.

**Holes and cramming.**
- Content is anchored to the top of the body, a closing statement or note to the bottom. Free space lies between them and never above the content.
- A page that leaves much of the body free steps its text up one tier or opens its rows before anything else moves; a page that overflows steps down one tier. No page invents a size.
- A closing statement set plain sits on the last line of the body (main pages 8 to 11, 14, 15).
- Every page is complete in its own markup when finished. A figure held between pages is mounted on each of them, because the reading view, the overview, the PDF, a jump and a backward move all cut.

**The front page.** A page of 73rem holds, from 1024 px up, a sticky contents rail of 12rem, a gutter of 3.5rem and a column of 53.5rem. Prose, lists and captions stop at the measure of 29.5em; figures, tables, statements and the explorer span the column. Sections are 5rem apart. Below 1024 px the contents become a drawer above the column. At 760 px the two-column blocks stack and the stepper wraps to three columns; at 600 px the body text is 1.0625rem; at 480 px the stepper wraps to two columns.

**The reading view of the talk** stacks the finished pages in one scrolling column, each at 1600 by 900 scaled to the window width, 56 px apart with a thin keyline between. It opens by itself when the window is narrower than 700 px.

## Elevation & Depth

Flat. There is no shadow, glow, blur or layered surface, and nothing floats over a tinted backdrop. A tooltip is paper inside a thin keyline. The overview and the blank screen are plain paper over the stage.

Two devices use shadow or gradient syntax in the code and are part of the look because they draw hard edges in one solid colour: the paper halo behind type on a screen (a ring of hard `text-shadow` offsets in the ground colour on the stage, a `paint-order` stroke on the front page), and the line screen and registration crosses, which are stripes of one solid ink.

## Shapes

Rectilinear. Every box has square corners (radius 0): the band, table cells, tooltips, key caps, the slider thumb (a 5 by 24 px bar on a 2 px track), overview thumbnails. Bullets on the front page are small solid squares of ink. The only round forms are data marks: solid dots, open rings and the round caps of a dotted connector.

**Keylines.** A keyline is solid and continuous. It starts and ends on the margins of its block and keeps one weight per role. Thin and inner keylines are black; the heavy keyline is teal.
- **Heavy (3 px, teal):** under a page title, a section heading, the front page's subtitle and the contents label, and on the cover of the talk; the top edge of the explorer; under the selected tab, stepper stage, preset, picker choice or viewer button, and under the pressed Strength button of the control row; round the current thumbnail of the overview. The current contents entry has a teal marker of 2 px in place of its inner keyline.
- **Thin (1.5 px, black):** tables, the foot, statements between keylines, run-in rows, disclosures, legends, tooltips, thumbnails, the divider between pages in the reading view.
- **Inner (1 px, black), front page only:** divisions inside a block that already has thin keylines: under a table head, between contents entries, between ledger rows, inside a nested disclosure, inside the explorer.
- In figures: axes and ticks 2 px, brackets and the control marker 2.5 px, bar and area outlines 3 px, leader lines 1.5 px. Axes, ticks, brackets and leader lines are black; the outlines of the navy areas are navy; the control marker is teal. Lines that carry data are at least 3 px on the stage.

**Line screens.** Parallel lines at 45 degrees, with a second screen at 135 degrees when two areas meet.
- Stage, payoff figure of main page 8 and bars of main page 13: navy lines, 1.5 px at a pitch of 9 px, for what the rival keeps, beside solid navy for what shareholders are paid.
- Stage, coexistence region of the entry chart: screen grey, 1 px at a pitch of 8, ruled round in ink, so branches and text read over it.
- Strong column of a table: an orange line of 1 px every 12 px, the orange mixed at 30 per cent with the ground, so that it reads as a light tone and text sits over it cleanly. The column head sits on paper; the screen starts under its keyline.
- Front page figures and the belief line: screen grey, 1.1 px at a pitch of 7 px.

**Registration crosses.** The title page of the talk carries four navy crosses, 34 px long and 1.5 px thick, one in each corner, 40 px from the edges. The title face of the front page carries two navy crosses of 1.5rem at its top corners, hidden below 760 px and in print. No other page carries them.

## Components

### Statements
- **Band:** solid navy, reverse white STIX 600 at 28 px, full measure, square, padding 20 px 9% 22 px 36 px. It holds the main statement of a talk page and is used on main page 16, the main result, and on the literature page (backup B14). The front page has no band.
- **Keyline statement:** bold navy text between two thin keylines. On the talk it is the unlabelled conclusion row of a Columns page (main pages 2 and 4), the statement under the table of backup B19, and the claim that closes a side column (main pages 13 and 18, backup B21). On the front page it is the takeaway ("In short."), all navy, and the opening question, in navy Jost 600.
- **Labelled closing row:** a row between thin keylines with its label in the label column, in navy Jost 600, and its text in ink. It closes main pages 1, 3, 5 and 20 and backup B20.
- **Proposition (front page):** between thin keylines, a navy Jost 600 tag line, then the statement in ink.
- **Plain statement:** bold navy text with no rule.
- **Formal statement (talk backups):** a navy run-in label ("Proposition 1") and its text in ink.

### Run-in rows
A row with a navy Jost 600 label column (206 px on the main pages) and text beside it, with a thin keyline above or below. On the main pages the label is 24 px in a column of 206 px with a 28 px gutter, so the text starts at x = 314 on every page with run-in rows.

### Matrix tables
Continuous horizontal thin keylines under every row and under the head, no vertical rules, no zebra. Heads and row labels in navy Jost 500, cells in STIX, numbers right-aligned in tabular figures. Every table of the talk with labelled rows sets them in navy, the number tables of the backups and the text-face labels of B6 among them; panel heads are navy too. The column a table singles out takes the orange line screen: the strong incumbent on main page 16 and on the backup tables (B11 and B19 among them), the costly rival on main page 9. The Strong head is orange Jost 600 on paper, and its Entry cell is solid orange with reverse white type. On the front page a table sits between two thin keylines with an inner keyline under a navy Jost 600 head; its row labels are STIX text in ink.

### Stage strip
On main pages 8 to 12, the stages of the model sit in the place of the sub line: Jost 500 at 21 px in secondary ink with dot separators, the current stage in Jost 600 teal. The current stage is never orange.

### Foot of a talk page
A thin keyline over the full measure. On the left the roadmap of five parts (Question, Model setup, Main results, Discussion, Conclusion) with the current part in Jost 600 teal. On the right the links to backup pages in Jost 600 teal, and the page number as "12 / 20" in Jost 600 ink. A backup page carries its label ("B4"), set as the page number in Jost 600 ink, and a return link in Jost 600 teal; the label and the link sit 26 px apart on every backup.

A link on the stage is teal with a quiet underline: 1 px, in teal mixed 40 per cent toward the paper, at an offset of 0.18em. On hover the underline turns full teal over 120 ms, with no transition under reduced motion. A visited link looks the same. A link's triangle carries no underline: the underline runs under the label only. The few links inside the text of a backup page ("page 17" on B1, "B13" in a note) take the same finish. Links are the stage's only pointer response.

### Figures
- **Branches of the entry chart:** no informed order, solid black 3 px; its mixed stretch, dashed 14 9; informed orders above the floor, solid orange 6 px; the floor after the drop, solid black 6 px; the drop, dotted 2 9 with round caps; "fixed informative trading", solid black 6 px; "rival cannot see price", dashed 16 10, one click after it; the full model's trace on main page 18, a broad pale grey stroke of 18 px behind the comparison lines.
- **Points:** solid dots (radius 8 px on the stage, the three incumbents 10 px); an open ring where a branch excludes its end; the strong incumbent's dot, tick and label in orange.
- **Labels:** Jost 500 at 22 to 24 px in ink, set beside their marks, with short black leader lines or brackets where needed; a label inside a screened region is knocked out on paper. No figure numbers, no in-figure titles, no legend box on the stage.
- **Factor underline (main page 11):** a black rule of 2.5 px, the bracket weight, under each of the three factors of the profit equation. Each is laid down on the click that brings the column explaining that factor.
- **Payoff figure (main page 8):** solid navy for what shareholders are paid, with its label in paper white; a navy line screen for what the rival keeps, with its label on a patch of paper; both areas ruled round in navy at 3 px. The line at R = θ is a dashed paper keyline over the solid area. Axes, brackets and labels are black. In the reading view the swatches of the probe are ruled in navy.
- **Split bars (main page 13):** solid navy for shareholders, navy line screen for the rival, outlined in navy at 3 px, with a black bracket for the shareholder spread. The row labels inside the figure are black.
- **Front page charts:** every series in ink, told apart by solid, dashed, dotted and dash-dotted strokes and by filled or open markers; the one orange series is also the heaviest. A legend of Jost labels under a navy title sits between thin keylines above the plot; a caption opens with a navy Jost 600 run-in. The areas are grey line screens; the front page has no solid figure area. A legend entry switched off is struck through.

### Strength control
A vertical teal marker of 2.5 px on the entry chart (main pages 17, 18, 19), called and hidden with `S`. It marks where the control stands. It snaps to the strengths the paper marks and never rests between them. At each stop a ring in ink marks each equilibrium, with a Jost readout in ink on paper beside it. It is hidden until called. While it is open, the "Strength" button of the control row is ink over a teal line of 3 px.

### Overview and reading view
- **Overview (`O`):** the finished pages as thumbnails on paper, grouped under Jost 500 headings at 24 px, in a grid with columns of at least 280 px and gaps of 20 px. Each thumbnail has a thin keyline; the current one has the heavy teal keyline, with the black focus outline outside it when it has focus. The headings are in ink. No surface sits behind a thumbnail.
- **Reading view (`V`, or `?view=read`):** described under Layout. Every click step is shown finished. Each group of backup pages opens with its label ("B8") in Jost 500 ink at the size of a page title, under a thin keyline.
- **Control row:** outside full screen, a row 44 px high on paper above the stage, closed by a thin keyline; the stage fits below it. Left: the site name, a link to the front page. Right, in Jost 500 at 15 px in secondary ink: the position ("Page 17 of 20 · click 3 of 4", or the backup label), "◂ Back to 17" on a backup, "Strength" on the entry-chart pages, previous and next arrows, then Overview, Notation, Reading view, Full screen and Keys, each with its key in a key cap (a thin keyline box). In full screen the stage is clean: the row floats in a thin keyline box at the top right only while the pointer moves or rests on it, and the cursor hides. On a phone the row keeps Overview, Notation and Keys.
- **Notation (`G`) and Keys (`?`):** a sheet of paper over the stage with a sticky head (title, "Close Esc") on a thin keyline. Notation shows the two B16 pages finished; Keys lists every key in a two-column ruled list. Escape or a forward press closes a sheet on the same click.
- **Blank (`B` or `.`):** plain paper; a click, Escape or any forward or back press returns to the same click.

### Front page controls
- **Tabs:** Jost 500 in secondary ink on a thin keyline; the selected tab is Jost 600 navy over a heavy teal keyline.
- **Contents:** a navy "Contents" label over the heavy teal keyline, then Jost 500 entries separated by inner keylines; the current entry is Jost 600 navy with a teal marker of 2 px in place of its keyline. In the phone drawer the last entry, which has no keyline, takes the marker when it is current.
- **Links:** teal with a quiet underline: 1 px, in teal mixed 40 per cent toward the paper, at an offset of 0.18em. On hover the underline turns full teal over 120 ms, with no transition under reduced motion; the weight does not change. A visited link looks the same. An action link is Jost 500 in teal with the same underline; the primary one is Jost 600 with a 3 px underline in full teal, the weight of the heavy keyline. The first line of the colophon shows its links with no underline until hover. The skip link is ink. Never a box.
- **Disclosures:** a navy Jost 600 summary between thin keylines.
- **Stepper, presets, picker, viewer bar:** text controls; the current choice is navy over a heavy teal keyline, and, except for the presets, set at 600. The stage numbers of the stepper and the letters of the picker are navy.
- **Explorer:** a heavy teal keyline above and a thin black one below; a navy title; a square slider in ink; readouts in STIX with tabular figures.
- **Registry number:** tabular figures with a dotted underline; its key shows on hover.
- **Focus:** a black outline of 2 px, offset 3 px, on the front page; 3 px, offset 4 px, on the talk's links and control strip.

### Motion of the talk
As built:
- **A click is a stored state.** The screen is a function of page and step, held in the address (`#p18.3`). Reload, back and a jump land on that state. A key pressed during motion finishes that motion and does nothing else. Going back cuts.
- **Reveal.** New ink is wiped in behind a hard edge along the mark's own long direction: text in 240 ms, lines, areas, table cells and the band in 380 ms, easing `cubic-bezier(.16,1,.3,1)`. When one click brings orange and other ink, the orange follows 120 ms after the rest; navy and teal go down with the black. Areas never fade in. The entry chart draws its branches from left to right in 300 to 450 ms, with a drop of 200 ms.
- **Shift.** On main page 13 the bars are copied, the copy travels down and its boundaries slide while the bracket widens, in 550 ms. Both pictures remain.
- **Carry.** Going forward between adjacent pages, an element both pages mark travels from its old box to its new one in 450 ms (`cubic-bezier(.33,1,.68,1)`), while the rest of the page fades in over 200 ms. A jump and a backward move cut.
- **Limits.** The rule is that nothing runs longer than about half a second, and no single movement does: the longest is the shift at 550 ms. One click of the entry chart chains a drop of 200 ms, a draw of up to 450 ms and dots of 160 ms, and can last about 0.8 s. Nothing dims or disappears within a page, except the full model's curve on main page 18, which becomes the pale trace. Nothing idles, pulses or loops. Nothing reacts to hover except links.
- **Reduced motion.** With the operating system's setting, `?motion=0` or `?static=1`, every state appears whole with no movement.

The front page has no animation of its own apart from the 120 ms change of a link's underline colour on hover. That change and its smooth scrolling are switched off under reduced motion.

## Do's and Don'ts

### Do:
- **Do** take every colour, family and keyline weight from `design/tokens.css`. Colour enters through `var(--frame)`, `var(--mark)`, `var(--link)` and `var(--accent)`; a lighter shade is made only by `color-mix(in oklch, var(--x) N%, var(--ground))`. A literal colour must be one of the ten palette values.
- **Do** give each colour its one job: black for text and thin keylines, navy for the frame, teal for position and passage, orange for the one meaning.
- **Do** keep orange for the one meaning, and give every other distinction a pattern, a marker shape, a weight or a screen.
- **Do** give every current mark a second code beside its teal: a weight of 600, a line under it, or an underline.
- **Do** show the same element in the same colour on every page of its kind.
- **Do** fill an area with a line screen, and knock type out of it on paper. A figure's areas, outlines and screens are one ink.
- **Do** run each keyline continuous across its block, in the weight and ink of its role: 3 px teal under a title, 1.5 px black for tables and the foot.
- **Do** set titles and labels in Jost 500 or 600 and text in STIX Two Text 400 or 600.
- **Do** keep stage text at 20 px or more and data lines on the stage at 3 px or more.
- **Do** keep a finished talk page equal to the author's page: every build ends on his words and numbers.
- **Do** use the solid navy band only for the main statement of a talk page.

### Don't:
- **Don't** use orange for a link, focus, a tab, a selected control, a current mark, a heading, a bullet or decoration.
- **Don't** give navy a meaning, or let navy alone tell two items apart.
- **Don't** use teal for data, an area, running text or decoration.
- **Don't** add a colour outside the palette, or give a colour a second job.
- **Don't** set running text in a colour, or draw a thin keyline in navy or teal.
- **Don't** change the colour of a visited link, or make the focus outline anything but black.
- **Don't** set a pale tinted callout box with a heavy accent bar on its side or top.
- **Don't** use a blended gradient, a glow, a soft shadow, a rounded box, a pill, a tinted area, or cards as page structure.
- **Don't** set a small label above a heading, a numbered section label, a label in capitals or a reading-time badge.
- **Don't** add a dark theme or a theme switch.
- **Don't** break a keyline, or use two weights for one role.
- **Don't** carry a distinction by colour alone, or data by a hairline.
- **Don't** let anything on the stage dim, loop, pulse or bounce, or react to hover apart from its links.
- **Don't** add figure numbers, captions or lettered points that the author's page does not have.
- **Don't** bring back a retired look: the purple look of 11 November 2026, the oxblood accent of 29 October 2026, or the template of 3 October 2026. The orange of the one meaning is not the oxblood: it is a lighter, yellower burnt orange taken from the PowerPoint, and the guards still reject the oxblood.
- **Don't** take anything from the look of the Beamer deck. From the PowerPoint the site takes only its three colours and their jobs; its flat pale teal box behind the Strong column stays out (the strong column is an orange line screen), and the finish is the site's own.

## Where the look is implemented and enforced

**Sources.**
- `design/tokens.css`: the shared tokens (ground, inks, the navy frame, the teal mark and link, the orange accent, keyline weights, families, figure marks, dash patterns, screens, focus). Its comments name the PowerPoint's hex values without a leading `#`, because the guard reads comments too.
- `handout/fonts.lock.json` and `handout/fonts/`: Jost 500 and 600 and STIX Two Text 400 and 600, upright and italic, as woff2 subsets pinned by sha256 and byte count, with their licence texts (SIL Open Font License 1.1).
- Front page (`handout/`): `style.css` (reading sizes, layout, components), `template.html`, `charts.js` (the SVG renderer, whose fallback literals repeat the palette; it reads `--fig-accent` first and falls back to the orange's literal), `figures.js`, `explorer.js`, `app.js`; `build.py` inlines the tokens and writes the font faces from the lock. Built page: `docs/index.html`.
- Talk (`talk/`): `src/stage.css` (structure of the stage, overview, reading view, print), `src/looks/plate.css` (stage sizes and the look's rules), `src/looks/plate.js` (the wipe), `src/css/*.css` and `src/figs/*.css` (layout of each group of pages and figures), `src/figs/*.js`, `src/engine.js`. Built page: `talk/dist/index.html`, from `python3 talk/build.py`.

**Guards.**
- `handout/check_display.py` (run after `handout/build.py`) fails when:
  - the built front page declares a face other than Jost and STIX Two Text, or makes a network request;
  - a colour literal in `design/tokens.css`, `handout/style.css`, `handout/template.html`, `handout/charts.js`, `handout/figures.js`, `handout/explorer.js` or the page's styles is outside its `PALETTE`;
  - `--ground`, `--ink`, `--ink-2`, `--frame`, `--mark`, `--accent` or `--fig-accent` in the tokens differs from the palette value;
  - a rule of `handout/style.css` spends the orange in a selector that does not name the recruit meaning, or `figures.js` or `explorer.js` names the orange directly (as a token, as its `oklch()` value or as its hex);
  - the focus ring is not ink, or a theme hook is present;
  - the built page, the tokens or a file of `handout/` carries a retired hex, a `--ucl-*` token, a gradient other than the one `--tint-fill` screen of the tokens, a `box-shadow`, or a radius above 2 px.
- `talk/build.py` stops the build when:
  - a locked font file fails verification, or the faces in the page differ from the lock;
  - a colour literal anywhere in the built talk is outside the same `PALETTE`, which it reads from `handout/check_display.py`;
  - the page refers to an external resource, a number is unfilled, a page is missing or duplicated, or speaker-note material is present.
- `handout/publish.py` refuses to publish when a file of the staged site, other than the archived earlier version it keeps under its own look, carries a retired hex or a `--ucl-*` token.
- The talk has no automatic check of the orange's meaning, of the jobs of navy and teal, or of gradients, shadows and radii. There those rules hold by this document.

**Changing the palette or a face.** A colour changes in three places together: `design/tokens.css`, the `PALETTE` set and the token assertions of `handout/check_display.py`, and the literals that repeat it (`handout/charts.js`, and the screen and trace greys in `talk/src/looks/plate.css`). A face changes in four: the files and `handout/fonts.lock.json`, the family assertion of `handout/check_display.py`, the stacks in `design/tokens.css`, and the stacks that `handout/style.css` overrides. Both pages are then rebuilt and both guards rerun.

**Token defaults that the pages override.**
- `--scr-ink`, `--scr-w` and `--scr-pitch` are black, 1.5 px and 9 px; the payoff figure (main page 8) and the split bars (main page 13) set navy, the entry chart of the talk sets screen grey, 1 px and 8, and the front page's renderer draws 1.1 px at 7 px.
- `--trace-grey` is replaced on the talk by the paler literal and a broad stroke.
- `--focus-w` is 3 px; the front page sets 2 px.
- `--tint` equals the ground and paints nothing.
