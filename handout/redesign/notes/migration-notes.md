# Migration notes

These notes surface the work that a real implementation needs. They do not solve it.
All paths are relative to `/home/uctpiaj/work/Projects/competition-creates-competition/`.

## 1. The linked PDFs and the byte-identity checks

### What the build asserts today

- `handout/build.py` (line 38) copies `paper/main_filled.pdf` and `paper/online_appendix_filled.pdf`
  into the output folder as `main_filled.pdf` and `online_appendix_filled.pdf`.
- `handout/check_display.py` (lines 44–47) asserts the sha256 of those two output files:
  `e912d0db…` and `4567b920…`. These are the `peer_release/` bytes.
- `presentation/build.py` (line 75) copies the same two files into `presentation/dist/` and
  checks them against the handout files.
- `handout/publish.py` (lines 30–41) stages an exact file list: the two PDFs at the root and
  again under `talk/`. The assertion on line 53 fails on any extra or missing file.
- `numerics/manifests/handout.json` records input hashes and the output HTML hash. It does not
  record the PDF hashes or the manuscript version.

### Facts about the candidate files

| File | sha256 (first 8) | Pages | PDF date | Source `.tex` |
|---|---|---|---|---|
| `peer_release/main.pdf` (= `docs/main_filled.pdf`) | e912d0db | 72 | 2026-09-06 | `paper/main_filled.tex` 06a035ed |
| `overleaf/paper/build/main.pdf` | 4003e37c | 72 | 2026-09-30 | `overleaf/paper/main.tex` 06a035ed (identical) |
| `peer_release/online_appendix.pdf` | 4567b920 | 57 | 2026-09-06 | `paper/online_appendix_filled.tex` 5accb7a4 |
| `overleaf/paper/build/online_appendix.pdf` | da907359 | 57 | 2026-09-30 | `overleaf/paper/online_appendix.tex` 5accb7a4 (identical) |

The `.tex` sources are byte-identical. Only the PDF bytes and the PDF metadata differ.
Switching the links today changes no text. The value of the switch is the path for future
Overleaf edits.

### Proposal

1. Add one declaration file, `paper/version.json`, written by a small stdlib script
   `handout/paper_version.py`. The script takes the PDF pair to publish (default
   `overleaf/paper/build/`), and records for each PDF: path, sha256, page count (parse the
   `/Type /Pages` `/Count` entry; no new dependency), the Info `CreationDate`, the sha256 of the
   `.tex` source, and the Overleaf commit id from `git -C overleaf/paper rev-parse HEAD`.
2. `handout/build.py` reads `paper/version.json`, copies the two PDFs, and writes the version
   stamp into the Read-the-paper tab and the colophon from that file. No date is typed by hand.
3. `handout/check_display.py` replaces the two hard-coded hashes with an assertion that the
   output bytes hash to the values in `paper/version.json`, and that the page counts match.
4. `presentation/build.py` reads the same file for the copies under `talk/`.
5. `numerics/manifests/handout.json` gains a `paper` block: source path, both hashes, pages,
   dates, commit id. The manifest then says which manuscript the page carries.
6. Keep the public file names `main_filled.pdf` and `online_appendix_filled.pdf`. External
   links point at them. The stamp inside the tab carries the version. A rename needs a
   `_redirects` file for Workers Static Assets and a change in both `publish.py` lists.
7. `peer_release/README.md` and the colophon should state the relation: same text as the
   peer-circulation revision, PDF rebuilt on the Overleaf date.

Decision for the author: switch now (one path for all future edits) or wait for the next text
revision (no visible change today).

## 2. Recovering the lost handout source

### Evidence

Word-level similarity between `handout/sections/*.html` (stale) and the live sections:

| Section | Stale words | Live words | Similarity |
|---|---|---|---|
| 01-setting | 1006 | 1012 | 0.933 |
| 02-mechanism | 1746 | 1781 | 0.982 |
| 03-evidence | 1066 | 1557 | 0.788 |
| 04-implications | 1611 | 1861 | 0.502 |

The live `<style>` block also differs from `handout/style.css` (193 diff lines: the amber and
blue accents are swapped and an `--accent-fill` token is added). The masthead text in
`handout/template.html` differs from the live masthead (opening question and answer).

### Method: start from the stale source and port the live differences

Do not rebuild the source from the live HTML alone. The reverse map from a displayed value to a
registry key is ambiguous: `0.250000` is the display of `base_entry_weak`, `base_entry_collapse`,
`base_hidden_entry_weak`, `base_hidden_entry_strong` and `moderate_entry_weak`. The stale source
keeps every placeholder, every table slot and the section structure. The live page keeps the
newer prose. Combine them:

1. Split the live HTML into its four `<section class="sec">` blocks (stdlib `re` or
   `html.parser`).
2. For each `span.q`, emit `[[key]]` from `data-q`, or `[[key:percent]]` when the text ends
   with `%`. This map is exact because the spans carry the key.
3. For each `<figure class="table">` whose `<table>` has `data-table="name"`, emit
   `<!-- @@TABLE:name@@ -->`. Names on the live page: `core_comparison`, `certificates`,
   `thresholds`, `auction_primitives`, `equilibrium_controls`, `comparative_statics`, `welfare`,
   `reserve_comparisons`, `extensions`. The model-to-record table (`#table-dictionary`) is
   hand-written HTML; keep it as prose.
4. For every math block, diff the live block against the stale block. Where the stale block has
   `[[key]]` and the live block has a bare value, restore `[[key]]`. List every bare value with no
   stale counterpart for manual mapping. Resolve each one against the registry by key, not by
   value.
5. Restore the masthead prose into `template.html` and the live `<style>` block into
   `style.css` (or let the redesign replace both).
6. Run `python3 handout/build.py --out /tmp/recovered` and diff the output against the live
   HTML. Iterate until the only differences are the build-meta line and asset URLs.
7. Commit the recovered sources with the live HTML hash in the commit message. Then apply the
   reconciliation items in a separate commit.

Known hook limitation to fix in the same pass: placeholders inside `\( \)` lose their tooltip.
Proposal: emit `[[key]]` inside math as the bare display value (as now) and add a
`<span class="q-math" data-q="key">` wrapper around the enclosing `.math-block`, so the
provenance survives as a block-level attribute.

## 3. Keeping the HTML slides in step with `talk.tex`

Two options.

**A. A generator that reads `talk.tex`.** Parse frames by `\begin{frame}`, titles, subtitles,
`\hypertarget` markers, `\hyperlink` buttons, `\BackButton`, itemize, tabular, display math,
`\includegraphics`, and every number followed by `% source:`. Emit `content.js`.
Pros: one source; titles, order, links and numbers cannot drift; every `% source:` key becomes
a `data-q` attribute. Cons: the deck has two TikZ diagrams (F1, F4), a `ResultBox`, column
layouts and macro-styled fragments (`\Info`, `\Cost`, `\Status`, `\GrayLine`, `\KeyIdea`,
`\PropItem`); a LaTeX-to-HTML converter for these is brittle, and the author edits `talk.tex`
live in Overleaf.

**B. A hand-kept `content.js` with a drift check.** A Node script (stdlib only) extracts from
`talk.tex`: the ordered frame labels, titles, subtitles, `hypertarget` names, the link graph
(`\hyperlink` targets and `\BackButton` origins), and every (number, `% source:` key) pair. It
extracts the same from `content.js` and fails on any difference in order, title, link graph, or
number-key pairs. It also checks that every number on a web slide carries a `data-q` key that
exists in the registry, and that the displayed string equals the registry display at the
deck's precision.

**Recommendation: B, with one generated layer.** Keep `content.js` by hand, because the
diagrams and the macro layout need web-specific markup. Generate two small files at build time:
`talk_numbers.json` (frame, string, key) from the `% source:` comments, and `talk_notes.json`
from `script.tex` (one block per `\scriptframe`, keyed by the exact title; the four backups
without a block, A9, A12, A25 and A29, fall back to the structure-plan text and are listed by
the check). `content.js` reads both at build time, and the drift check compares the deck
against `talk.tex` on every build. Promote to a full generator only if the author stops editing
the TikZ frames by hand.

## 4. Deployment risks

- **Fonts.** New families must enter `handout/fonts.lock.json` with their sha256; the build
  fails otherwise, and `style.css` must reference exactly the locked files. Fontsource "latin"
  subsets omit U+2113 ℓ, U+2192 →, U+2191 ↑, U+2193 ↓, U+2264 ≤, U+2265 ≥, U+2248 ≈, U+2208 ∈
  and U+221E ∞. The live tables use ℓ, →, ↑, ↓ and × as text. Without a `unicode-range`
  fallback face that holds those glyphs, the browser substitutes a system face. That is the
  "weird font" effect. The mockups declare a fallback face per pairing; the real build must lock
  it too.
- **Vendored libraries.** The handout loads KaTeX and Plotly from cdnjs with SRI; the talk bundles
  KaTeX locally. Offline-first for both means copying KaTeX into the handout output (as
  `presentation/build.py` already does) and either replacing Plotly with hand-built SVG (as the
  mockups do) or vendoring it. Replacing Plotly rewrites `handout/charts.js`; the display rules
  in `handout/README.md` (broken lines, interval bars, multiplicity ticks, shading, closed and
  open endpoints) must be re-verified in `check_display.py` against the new chart code.
- **Browser check contract.** `handout/check_browser.js` expects the ids `#chart-fig1` to
  `#chart-fig4`, `#explorer`, the stepper, the theme toggle and the legacy anchors. A redesign
  must keep those ids or update the check in the same change.
- **Legacy anchors.** The `span.legacy-anchor` elements carry ids that external links use.
  Keep every one.
- **Provenance lists.** `presentation/dist/provenance.json` hashes `presentation/content.js`,
  `deck.js`, `deck.css` and `template.html`. New files (a shared engine, data files, fonts) must
  join that list, and `publish.py` must add them to its exact staged lists. Its assertion
  fails on any extra file.
- **Two copies of the PDFs.** The root and `talk/` each carry the two PDFs. One version file
  must drive both, or the two copies can diverge.
- **Theme storage keys.** The handout uses `ccc-theme`; the talk uses `ccc-deck-theme`. A unified
  key is fine, but the code must accept the old values once.
- **PDF export of the talk.** `presentation/export_pdf.sh` uses headless Chrome, which hangs on
  this machine. Run the export on another machine or keep the Beamer PDF as the printable copy
  and link it from the web deck.
- **Charts inside closed folds.** The live page mounts charts on `toggle`. Hand-built SVG removes
  that need, but the lazy-mount query flags (`?eager=1`, `?lazy=1`) are used by the browser check.
- **Status vocabulary in tables.** `handout/tables_html.py` prints "control" for the frozen rows.
  The paper prints "numerical diagnostic". Fix `status_word` and the table note together
  (reconciliation item 4.7).
- **Naming hygiene.** No agent or tool names may appear in any file that lands in the
  repository: mockup text, HTML comments, file names, metadata, commit messages. The mockups
  under `proposals/` follow this rule; a copy into the repository must keep it.
