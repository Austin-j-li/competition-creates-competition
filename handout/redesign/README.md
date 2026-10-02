# Website redesign: staging folder and build brief

This folder holds the approved design and the inputs for the redesign of
https://competition.dealextract.org/ (the handout) and its `/talk/` deck.
It is a staging folder. Remove it in the last commit of the build, after the
new handout and deck land in `handout/` and `presentation/`.

Status on 2 October 2026: the author chose the design. No build work has started.

## 1. Objective

1. Polish the handout text against the current paper.
2. Give the handout a "Read the paper" tab that shows the current paper PDFs.
3. Rebuild `/talk/` from the Beamer deck. Keep all 47 frames in the same order
   and organisation. Make it an HTML deck with interactive parts.
4. Replace the fonts. The author finds the current fonts "a bit weird".

## 2. Author decisions (2 October 2026)

| Item | Decision |
|---|---|
| Design | Direction C, "UCL family". Beamer purple chrome, white body, cards, pill buttons. See `mockup/`. |
| Fonts | Fira Sans for text, Fira Mono for numbers. Ship only these two families, plus a locked fallback face for the glyphs that the Fira subsets omit (see `notes/migration-notes.md`, section 4). Remove the pairing switcher. |
| Affiliation | "Department of Economics, University College London" on the handout and the talk. `talk/talk.tex` already says this. The paper names no affiliation; do not add one. |
| Number style | Three decimals, as on the slides: 0.250 → 0.523. A percent can appear only as a secondary gloss. Derive the display from the registry value with a display rule in the builder. Never type the number. |
| Reconciliation items 4.4, 4.5, 4.6/4.7/6.2 and 5.2 | Follow the paper in all four. Print "numerical diagnostic", not "control". The core-table caption says that fixed informative orders restore deterrence. Add "weakly" for Proposition A.8. Replace "Off-path pricing rules need not be unique." with the paper's sentence: "Uniqueness refers to trading and on-path entry under truthful bidding and allows arbitrary mixed orders and every continuous deviation." |
| Other "Author decides" rows in `notes/handout-reconciliation.md` | Use the proposed wording in the row. If a row has no proposal, keep the paper's words. |
| Deviation phrase | The handout uses the paper's phrase, "every continuous deviation". The deck copies `talk.tex`, which says "every unilateral deviation". Do not change `talk.tex`; the Overleaf master is out of scope. |
| Paper PDFs | Do not switch. The Overleaf build of 30 September 2026 has the same text as `peer_release/` (16 metadata bytes differ). Keep the `peer_release/` bytes, the public file names and the hashes in `check_display.py`. The "Read the paper" tab states: text revision of 6 September 2026. |
| Checks | Rewrite `presentation/check_deck.mjs`, `handout/check_display.py` and `handout/check_browser.js` for the new deck and charts. Keep every guarantee they give today (see section 6). Do not add new test files. |

## 3. Sources

The Overleaf working copies are not in Git. The repository copies are identical
to them on 2 October 2026:

| Overleaf path in the notes | Repository path |
|---|---|
| `overleaf/paper/main.tex` | `paper/main_filled.tex` |
| `overleaf/paper/online_appendix.tex` | `paper/online_appendix_filled.tex` |
| `overleaf/talk/talk.tex`, `script.tex` | `talk/talk.tex`, `talk/script.tex` |
| `overleaf/paper/build/*.pdf` | `peer_release/*.pdf` (same text) |

Content sources:

- Handout text: `inputs/live_handout_2026-10-02.html`, the page live on
  2 October 2026. It is newer than `handout/sections/` and `docs/index.html`.
  Its source files are lost. `inputs/live_handout_stripped.html`,
  `live_handout_data.json` and `live_handout_style.css` are extracts of it.
- Deck content: `talk/talk.tex` (47 frames: F0 to F16 with F10a and F10b, then
  A1 to A29), `talk/script.tex` (speaker notes) and `talk/structure-plan.md`.
  The current `presentation/content.js` is an earlier, different talk. Do not
  use it as a content source.
- Numbers and status labels: `numerics/quantity_registry.csv` only.

## 4. Folder contents

- `mockup/`: the approved direction as static files. Open `mockup/handout.html`
  and `mockup/slides.html` in a browser; both work from `file://`. The PDFs
  are left out, so the PDF links in the mockup do not resolve.
- `prototype/`: the generator of the mockup (`make.py`), its shared scripts and
  styles, the direction C skin and the font fetcher. It reads absolute paths on
  the author's machine and does not run from a clone. Use it as a reference
  for the registry guard `R()`, the notes extraction and the chart code.
- `notes/inventory.md`: each Beamer frame mapped to a web slide, with the
  proposed interactions and the progress-rail parts.
- `notes/handout-reconciliation.md`: the live handout compared with the paper,
  row by row, with quotations and proposed wording.
- `notes/migration-notes.md`: source recovery, deck synchronisation, deployment
  risks. Paths in it are relative to the repository root, or to the
  Overleaf copies (see the table in section 3).
- `inputs/`: the live handout and the live talk of 2 October 2026, with
  extracts and provenance.

## 5. Work plan

Do the steps in order. Commit at the end of each step with an informative
subject.

1. Recover the handout source. Follow `notes/migration-notes.md`, section 2:
   start from `handout/sections/`, port the live prose, restore every
   `[[registry_name]]` placeholder and table slot, keep every legacy anchor.
   Build to a temporary folder and diff against the live HTML until only the
   build line and asset URLs differ. Put the live HTML sha256 in the commit
   message.
2. Apply the reconciliation edits from section 2 of this file in a separate
   commit.
3. Implement direction C in `handout/`: template, CSS, charts, "Read the paper"
   tab. Lock the Fira files and the fallback face in `handout/fonts.lock.json`
   with sha256. Vendor KaTeX locally. Keep the data hooks: provenance spans,
   registry values, status labels, broken lines at unresolved nodes, interval
   bars on certified points, closed and open endpoints.
4. Build the `/talk/` deck in `presentation/` from `talk.tex`. Use 47 slides in
   the Beamer order, the parts in `notes/inventory.md`, back buttons for the
   backup links, and speaker notes from `script.tex`. Use the sync method in
   `notes/migration-notes.md`, section 3 (hand-kept content plus a drift check
   against `talk.tex`). Every number carries its registry key.
5. Rewrite the three checks (section 6). Update `handout/README.md`,
   `presentation/README.md` and `presentation/DESIGN.md`. Update the staged file
   lists in `handout/publish.py` if the published files change. Do not run it.
6. Run `python3 handout/build.py`, `python3 handout/check_display.py`,
   `python3 presentation/build.py` and `node presentation/check_deck.mjs`.
   Report each result.
7. Remove this folder. Push the branch.

## 6. Guarantees that the rewritten checks keep

- Status words come from the paper's vocabulary: analytical,
  computer-assisted, numerical diagnostic, open, input.
- Each displayed number equals the registry display at the declared
  precision, and carries its registry key.
- No registry number appears in a slide headline.
- Charts break lines at unresolved nodes, mark multiplicity nodes, and show
  interval bars, shading, and closed and open endpoints as today.
- The chart builders do not change the release data.
- The two published PDFs match the `peer_release/` hashes.
- The source manifest binding and the finite-value table checks stay.
- Every legacy anchor id stays on the handout.
- Every notation symbol on a slide is defined on that slide or an earlier one.
- The deck order, titles and link graph match `talk.tex`.

## 7. Rules

- Do not run `handout/publish.py`. Do not run `wrangler`. Do not use any
  Cloudflare service or tunnel. Do not change the live website.
- Push only to this branch. Do not push to `main` or `gh-pages`. Do not open a
  pull request unless the author asks.
- Do not edit `paper/`, `talk/`, `numerics/` or `peer_release/`. Do not change a
  registry value, a tolerance or a status.
- Do not commit generated PDFs, `.venv`, `node_modules` or fetched browser
  packages. Do not add a browser package to the repository.
- Do not write tests. Do not add test files, fixtures or frameworks. The three
  existing checks in section 6 are the only exception: rewrite them, do not
  add to their number.
- Verify by use: build the pages, open them where a browser is available,
  and report what you saw. If no browser is available, say so. The author
  runs the browser pass on their machine before publication.
- Keep tool names, agent names and session details out of every repository
  file and commit message.
- Write in short, plain sentences: one instruction in each sentence, simple
  verbs, active voice, no "-ing" forms where a simple form fits.
