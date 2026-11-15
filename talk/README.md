# Seminar talk

The seminar talk is a web page, published at `/talk/` beside the research brief and the paper.
It has a title, 19 main pages and 39 backup pages in the plate look.

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
remembers the page and step it came from; Backspace returns there from any backup, and so does a backup's Back link. Where a backup names the pages it belongs to instead (B2 shows "◂ 11", "◂ 12", "◂ 15"), a named link returns to the exact step if that is the page it was opened from, and otherwise to that page finished. The two lead pages of B4 and B13 carry no return link of their own: Backspace returns from them.
O opens the overview; arrows and Enter choose a page. V toggles the finished reading view,
which also opens with `?view=read` and is the default on a narrow screen. S opens the strength
control on the entry charts; Left and Right move between marked strengths. Escape closes the
control, overview or blank screen. F toggles full screen. B or a full stop blanks the screen.
`?static=1` turns motion off.

For a PDF fallback, run `talk/export_pdf.sh` after building. It prints every finished page to
`talk/dist/talk.pdf` with local Chrome; its third argument `main` prints only the main sequence.
Inspect the PDF before using it. The author's PowerPoint remains the fallback in the room.

The words, numbers and page order come from the root PowerPoint, copied by hand, page by page,
into `talk/src/pages/`. The author changes wording in the PowerPoint first. The text dumps under
`audit/` are working records and are not needed to build. Never write to the PowerPoint.
Numbers are bound through `data-num` to `src/data.json` and `src/data_*.json`, written by
`build_data.py` and the `build_data_*.py` scripts from the registry. Rebuild the relevant data file
when its registry inputs change, then rebuild the talk. Figures read those data files and the
paper's closed forms.

Page owners keep their pages, figure modules, page styles and data scripts together. The engine
owns navigation, stage layout and the shell. The build, shared tokens, font lock and publisher
join those files; the look styles presentation-specific type sizes and reveal behaviour.
