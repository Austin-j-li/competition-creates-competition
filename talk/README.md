# Seminar talk

The seminar talk is a web page, published at `/talk/` beside the research brief and the paper.
It has 65 pages: a title, 20 main pages and 44 backup pages (B1 to B21) in the plate look.

```sh
python3 talk/build.py
```

The build writes `talk/dist/index.html`, one self-contained file that opens directly in a current
browser without a network connection. It verifies and embeds the site's faces from
`handout/fonts.lock.json` and reads the shared look tokens from `design/tokens.css`.
The build refuses missing pages, unfilled numbers, network references, notes, colours outside
the shared palette and unlocked faces. `--allow-missing` is for an incomplete working copy.
`handout/publish.py` builds and stages the site together; see `handout/README.md`.

Open `talk/dist/index.html` to present. Right, Space, PageDown or Enter advances a step; Left or
PageUp goes back. Home and End go to the ends of the current main or backup sequence.
Type a main page number then Enter to jump; type `b8` then Enter for backup B8. A backup link
remembers the page and step it came from; Backspace returns there from any backup, and so does a backup's Back link. Where a backup names the pages it belongs to instead (B2 shows "◂ 15", "◂ 16", "◂ 17"), a named link returns to the exact step if that is the page it was opened from, and otherwise to that page finished. A backup opened directly, with nothing remembered, returns to the main page that links to it. The control row above the stage shows the position, a Back button on every backup, and buttons for every key below; in full screen it appears only while the pointer moves.
O opens the overview; arrows and Enter choose a page. V toggles the finished reading view,
which also opens with `?view=read` and is the default on a narrow screen. S opens the strength
control on the entry charts; Left and Right move between marked strengths. Escape closes the
control, overview, sheet or blank screen. F (or a clicker's F5) toggles full screen. B or a full stop blanks the screen; a click also returns. G shows the notation (B16), ? lists the keys, R restarts the current page.
`?static=1` turns motion off.

For a PDF fallback, run `talk/export_pdf.sh` after building. It prints every finished page to
`talk/dist/talk.pdf` with local Chrome; its third argument `main` prints only the main sequence.
Inspect the PDF before using it. The Beamer PDF remains the fallback in the room.

The words, numbers and page order come from the Beamer slides, the master of the talk since
18 November 2026 (`overleaf/slot/slides.tex`, one frame per page under a banner such as
`===== PAGE 8 / 20`), copied by hand, page by page, into `talk/src/pages/`, and set in the plate
look, not in the look of the slides. The author changes wording in `slides.tex` first. The text
dumps under `audit/` are working records and are not needed to build. The last sync followed
Overleaf commit b7ee263 (`audit/talk_sync_2026_11_18_beamer/`).
Page files are named by position in the PowerPoint's show order: `pNN` is main page NN (`p00` the
title), `bNN` the backup at show position NN (B1 to B17 are `b22` to `b61`; B18 is only the formal
Proposition 2 page, `b74`; the twelve earlier versions of main pages that the PowerPoint keeps in B18,
show positions 62 to 73, are not built; B19, B20 and B21 are `b75`, `b76` and `b77`, the numerical-example
table, the two-equilibria algebra and the research page, shown finished). `master_dump/slideNN.txt` is
the text dump of the slide at show position NN, from the 20-page PowerPoint master.
Number ids and figure variants keep the names their pages had in earlier decks (for example `p14.*`
and the entry chart's variant `p14` are main page 17; `example.*` is backup B19 and main page 17; the
research chart's variant `p18` and its `p18.*` numbers are backup B21); they are names, not page numbers.
Numbers are bound through `data-num` to `src/data.json` and `src/data_*.json`, written by
`build_data.py` and the `build_data_*.py` scripts from the registry. Rebuild the relevant data file
when its registry inputs change, then rebuild the talk. Figures read those data files and the
paper's closed forms.

Each group of pages keeps its page files, figure modules, page styles (`src/css/`) and data script
together. `src/engine.js`, `src/stage.css` and `src/template.html` hold navigation, the stage and
the shell. `build.py` joins them with the shared tokens (`design/tokens.css`) and the locked
fonts; `src/looks/plate.css` holds the type sizes of the stage and the reveal behaviour.

This folder also holds an earlier LaTeX talk of the paper (`talk.tex`, `script.tex`,
`structure-plan.md`, `paper-sync.md`, `econ-slides-compat.sty`, `figures/`, `notes/`). Those files
are not part of the web talk and its build does not read them.
