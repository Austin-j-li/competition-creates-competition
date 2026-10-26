# S15 unified design: report of the design lead

26 October 2026. One visual system, the ruled document, across the research brief page, the web slides and the Beamer deck, written down in `DESIGN.md` at the repository root and guarded so that the purple "UCL family" look cannot return. Content, words, numbers, frame order and section order are unchanged on all three surfaces; the paper figures are byte-identical to their committed versions.

## Design decisions

- **One system, three implementations.** The brief page, the web deck and the Beamer deck share the tokens of `DESIGN.md`: paper #fbfcfc and ink #1e2530 (slate #1a1f26 and #e8ecf1 in the dark theme), muted #5b6573, hairline #c7cdd5, grid #e4e8ec; STIX Two Text for reading text, Archivo for titles, headings, tables, figure text and controls, Fira Mono for file hashes only; a 2 px ink rule above the title block and each section heading of the brief, under each slide title and above the deck title; 1 px hairlines elsewhere; no fills, cards, pills, gradients, glows, shadows, side stripes or rounded corners.
- **The chrome has no colour.** Links, tabs, buttons, the focus ring, the slider, the progress rule, the pager and the theme control are ink or grey on every surface. Text selection is ink at low opacity on both pages (the web deck used the information colour for selection; it follows the brief page).
- **Two concept colours inside exhibits only.** #b54b00 for the target-payoff spread, the information chain, the branches a purchase recruits along and the posterior band; #006459 for preparation costs, the threshold, the floor and the window; #f6a157 and #46b3a8 on slate. The slide figures (`figures/*_talk.pdf`) take the same roles: the quiet branch and region boundaries in ink, the recruiting branches and the belief band in the information colour, the preparation threshold in the cost colour, the floor branches in muted grey, the bands as the information tint and the neutral tint on the slide paper. This matches the keys the slides print under the figures and the web charts of the brief and the deck.
- **Run-in words instead of labels.** The brief's labelled paragraphs begin with a bold Archivo run-in word and a period: the answer, the takeaway, the scenario, the two paths of the mechanism map and the two propositions ("Proposition 2 · Competition creates competition."). The section fragments were not edited; the run-ins are produced by the stylesheet from the existing label elements. The numbered reading-time line under each section heading is not displayed; the fragments still carry it, and the coordinator can remove those six lines when the sections are next edited.
- **Registry numbers** are set in the text face with tabular figures and a faint dotted hairline underline that carries the key on hover; no monospace.
- **The motivation slides** (the title and the three question frames) carry no number; unchanged.

## Changes per file

Research brief page (`handout/`):
- `style.css`: rewritten to the ruled document from the author's port, merged by hand where the port assumed a different fragment markup. Added: the run-in rules for the scenario label, the path labels of the mechanism map and the proposition titles; the hidden section-time line; the page-width token renamed so that it does not collide with the deck's stage-colour token of the same name.
- `template.html`: the progress bar, the decorative masthead figure, the status line with the reading time and the "Interactive slides" kicker are gone; the record line under the byline names the paper's kind and the text date; the colophon names the three faces.
- `charts.js`: the fallback tokens of the SVG renderer are the ruled palette and faces (they carried the purple).
- `build.py`: the face check names Archivo, STIX Two Text, Fira Mono and the symbol fallback; the generated font faces carry `font-stretch` for the variable Archivo; the preloads are the body and the display face; the paper tab has no kicker.
- `fonts/` and `fonts.lock.json`: the Fira Sans files are removed; the Archivo and STIX Two Text files (fontsource subsets, SIL OFL, with their licences) are locked by sha256; the shared file names carry the same hashes as the deck's lock.
- `check_display.py`: the face assertion is the contract of the four locked faces; a palette guard fails on any UCL hex or `--ucl-*` token in the built page or the handout sources. Every other check stays.
- `publish.py`: the archive line of the Laplace page is set in the ruled design; a palette guard scans every staged HTML, CSS and JS file of the current site; publishing requires the checkout to contain `origin/main`.
- `README.md`: the design paragraph, the typeface bullet and the publishing notes describe the ruled document and the guards.

Web slides (`presentation/`):
- `deck.css`: selection colour in ink; the dark region tint equal to the brief's; a header note pointing to `DESIGN.md`.
- `check_deck.mjs`: fails on any UCL hex or token in the deck sources or the built page, and on any `:root` token (light or dark) that the deck declares with a value different from `handout/style.css`. Forty-one shared tokens agree.
- `DESIGN.md`: points to the root `DESIGN.md` as the source of the system.

Beamer deck (`slot/manuscript/`):
- `ccc-ruled.sty`: the theme moved out of `slides.tex`: fonts (fontspec, STIX Two Text, Archivo from `fonts/`), colours, Beamer colour and font settings, the frame head with the progress rule, the footline, the title page, the mathematics setup, booktabs widths, the tabular face and the layout macros (grey lines, takeaways, model boxes, navigation placement, the Back button).
- `slides.tex`: loads the style file; keeps the frames, the figure path, the numbers file and the two coexistence-panel macros; a comment block at the top says where the look comes from. The built deck is pixel-identical to the deck built before the move (35 pages compared at 40 dpi).
- `figures/beliefs_talk.pdf`, `coexistence_talk.pdf`, `research_talk.pdf`: regenerated in the slide palette. `beliefs.pdf`, `coexistence.pdf` and `research.pdf` are byte-identical to the committed files (sha256 65c1d7db…, 479ed66d…, 97c78d73…).
- `latexmkrc`: pdfLaTeX by default; when the file name given to latexmk is `slides.tex` (read from the arguments latexmk exposes to the file), the mode is XeLaTeX and the pdflatex command itself is xelatex, so a `-pdf` option on the command line still builds the deck with xelatex. Tested in a scratch copy: `latexmk -r latexmkrc slides.tex` and `latexmk -pdf -r latexmkrc slides.tex` both apply xelatex (35 pages, 0 overfull boxes, fonts embedded); `latexmk -r latexmkrc main.tex`, `latexmk -pdf -r latexmkrc main.tex` and `comparison.tex` apply pdflatex (150 and 7 pages). The author should confirm once on Overleaf, which this stage cannot reach.
- `START_HERE.txt`: a paragraph says that the look comes from the style file and the fonts folder, which must stay, and what the latexmkrc selects.

Figure program (`audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py`): a slide palette bound when a slide figure is drawn (the manuscript palette otherwise), with the beliefs figure mapping the band to the information colour and the threshold to the cost colour. In-figure words are unchanged.

Root: `DESIGN.md` (frontmatter tokens; overview; colours; typography; layout; elevation; shapes; components; do's and don'ts, which is the slop list; where each surface implements the system).

## Guards

- `handout/check_display.py`: fails on #361A54, #993BFF, #BA82FF (any case) or `--ucl-dark`, `--ucl-bright`, `--ucl-mid` in the built page, the template, the stylesheet, the scripts and the section fragments.
- `presentation/check_deck.mjs`: the same palette check on `deck.css`, `charts.js`, `deck.js`, `template.html`, `content.js` and the built deck; and the token-drift check against the brief's stylesheet.
- `handout/publish.py`: the palette check on every staged `.html`, `.css`, `.js` and `.mjs` file at the root and under `talk/`. The archive under `laplace/` is the committed page of the pinned Laplace commit, which carries fourteen purple occurrences by design, so it is outside the scan; this is the one departure from "any staged file". Publishing (not `--stage-only` or `--dry-run`) fetches `origin/main` and refuses with a message that tells the author to bring the checkout to main when the fetch fails or when `git merge-base --is-ancestor origin/main HEAD` fails.
- `slot/manuscript/slides.tex` and `START_HERE.txt` say that the style file and the fonts folder must stay.

## Detector

`impeccable detect` on the staged brief page and the staged deck: 39 findings, all judged, none a defect of the system.
- `tight-leading` (line height 1.15 on headings): the heading rule; body text is at 1.6, slide text at 1.32. Display leading is intended.
- `cramped-padding` on the stepper list and five table wrappers of the brief: the wrappers carry the booktabs rules; the inset is the cell padding (0.45 to 0.6 rem) and the stepper buttons' padding, which the detector does not count. Intended.
- `cramped-padding` on the slide sections and on the formula number spans of the deck: the slide head carries 26 px of padding inside the section, and the spans carry the dotted provenance hairline as a bottom border under a formula (a text underline would cut through the fraction parts of the mathematics). Intended.

The design critique and the audit ran in this one context, with no helper, as the brief requires.

## Verification

From the worktree root:
- `python3 handout/build.py`: HANDOUT BUILD PASSED (both PDFs built outside the repository, 36 font files copied, 180 number spans).
- `python3 handout/check_display.py`: PASS the paper tab states 150 and 7 pages; PASS 180 number spans and 53 numbers in formulas; PASS only Archivo, STIX Two Text, Fira Mono and the symbol fallback, no network request; PASS no UCL purple hex or token in the page or in 13 handout source files.
- `python3 presentation/build.py` and `node presentation/check_deck.mjs`: 34 frames compared with the talk; 156 printed registry keys on the web frames; 39 notation symbols; 30.25 planned minutes; 41 design tokens shared with the brief agree; no purple palette in 6 deck files; the deck matches the talk and the deck contract.
- `python3 handout/publish.py --stage-only …/site-unified`: staged 232 files (62 at the root, 61 under `talk/`, 54 under `laplace/`, 55 under `laplace/talk/`); no purple palette in the 6 HTML, CSS and JS files of the current site.
- Beamer, from `slot/manuscript` with the output outside the repository: `latexmk -xelatex slides.tex` exit 0, 35 pages, 0 overfull boxes, 15 fonts all embedded (Archivo, STIX Two Text, STIX Two Math and the figure fonts).
- `latexmk -pdf main.tex` and `comparison.tex` into a scratch copy: 150 and 7 pages, unchanged.
- Language scan on `DESIGN.md`, the style file, `START_HERE.txt`, `handout/README.md`, `presentation/DESIGN.md` and this report: the hits are file names and the words key, registry, check and run, which these documents must name, plus "Times New Roman", "An illustrative sale process" and "Text revised" quoted from the page; no status label, no hedge, no narration of the paper's changes.
- No build product is left in the repository: the built page and its fonts under `docs/` are the committed site outputs that the build refreshes; the slide and paper builds and the figure previews went to the scratch folder.

## Screenshots

A headless browser at 1600 by 900 and at 390 by 844, of the staged site, in the unified scratch folder under `shots/`:
- brief page: `brief-top-light`, `brief-top-dark`, `brief-prop-light`, `brief-prop-dark`, `brief-mechanism-light`, `brief-mechanism-dark`, `brief-figure-light`, `brief-figure-dark`, `brief-table-light`, `brief-table-dark`, `brief-explorer-light`, `brief-explorer-dark`; mobile `brief-top-mobile`, `brief-top-mobile-dark`, `brief-prop-mobile`, `brief-figure-mobile`, `brief-table-mobile`, `brief-explorer-mobile`;
- web deck: `deck-cover-light`, `deck-cover-dark`, `deck-F12-light`, `deck-F12-dark`, `deck-F13-light`, `deck-F13-dark`, `deck-A8-light`, `deck-A8-dark`, `deck-F12-mobile`;
- Beamer frames at 80 dpi: `beamer-p1-01` (title), `beamer-p8-08` (the order slot), `beamer-p16-16` (coexistence region), `beamer-p17-17` (coexistence in the example), `beamer-p29-29` (backup A6);
- the three slide figures: `fig-beliefs_talk-1`, `fig-coexistence_talk-1`, `fig-research_talk-1`.

Read critically: no purple, no fill, no pill, no card, no shadow; the two concept colours appear only in the figures, the mechanism map's information path and the slide diagrams' cost boxes; the run-ins read as theorem heads; the dark theme is slate with lightened concept colours; at 390 px the title block, tabs, contents drawer, proposition and explorer hold, and the wide tables scroll inside their rules. One observation for a later pass: the two path names of the mechanism map sit on their own line above the first sentence rather than running into it, because the path columns are flex columns; a true run-in there needs the fragment's markup, which this stage did not touch.
