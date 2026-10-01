# Interactive seminar talk

A redesigned 40-minute talk: **24 main slides and 15 technical slides**. The schedule
allocates 38 minutes to exposition and two minutes to discussion/transitions. The opening
moves from institutional motivation and the conventional deterrence intuition to the
information feedback, research question, literature and contribution before the model.

## Open and present

The existing public talk is at https://competition.dealextract.org/talk/.
Local changes do not update it. Preview the new build with:

```sh
python3 presentation/build.py
node presentation/check_deck.mjs
python3 -m http.server 8776 --bind 127.0.0.1 --directory presentation/dist
```

Open `http://127.0.0.1:8776/`, or open `presentation/dist/index.html` directly.
The HTML, fonts, math, animation libraries, data and linked papers work offline.

- Right arrow / Space: next reveal, then next slide.
- Left arrow: undo a reveal, then previous slide.
- O: slide overview. N: notes. G: notation. F: fullscreen.
- T: cycle automatic, light and dark themes. R: reset the current interaction.
- Escape: close a panel, exit reading mode or return from a technical slide.
- Home / End: title / conclusion. Focused sliders retain their arrow keys.
- Read: see all slides in a scrolling view. Present returns to the selected slide.

Automatic theme uses cream paper for technical material and warm charcoal at the opening,
question, main theorem and conclusion. Light mode supports bright projectors. Instrument
Serif carries headings and display lines, Geist the running text and Geist Mono the
numerals. Motion follows the presenter; there is no automatic advance. Reduced-motion
preferences are respected.

The stage is a scaled 1600 × 900 surface. It fits smaller screens without layout changes;
landscape is preferable on a phone. The notes dialog appears on the presentation screen.
For private notes, use `dist/speaker-notes.md` on a separate device.

## Sources and checks

`content.js` owns the slide copy, speaker notes, sources, timing and glossary. `deck.css`
owns the visual system. `deck.js` owns navigation and interactive figures. `DESIGN.md`
documents the academic and implementation requirements.

The builder binds 16 research CSVs to their passed manifests and verifies local KaTeX,
font and GSAP hashes. The browser's `DECK.selfCheck()` checks 49 existing formula values,
math rendering and runtime errors. `await DECK.audit()` walks the whole deck for overflow.

Run `check_browser.js` through the Playwright `browser_run_code_unsafe` tool against the
preview server. It checks all 39 slides at 1600 × 1000, 1366 × 768 and 390 × 844 in automatic,
light and dark themes, then exercises the presentation controls. If the tool cannot read
an isolated checkout path, pass the file's contents as its `code` argument.

Screenshot and PDF inspection supplement automated checks. The tests verify presentation
behaviour against existing research outputs; they do not rerun numerical searches or
establish research acceptance.

## Export and publication

With the preview server running, `presentation/export_pdf.sh` exports the PDF when a local
Chrome executable is available (set `CHROME` for another installation). Alternatively,
use Playwright's `page.pdf({printBackground:true, preferCSSPageSize:true})` after awaiting
`DECK.ready`. Output is 39 pages, each 16 × 9 inches, with all reveals visible. The builder
removes a stale PDF when the generated HTML changes, so regenerate it after editing.

The build also creates `dist/speaker-notes.md` and `dist/provenance.json`. Keep `dist/`
together when transferring the offline deck. Fonts retain their license texts. GSAP's
bundled source headers identify its version and license URL.

Publication uses `handout/publish.py` and includes the handout and talk. It remains separate
from a GitLab push. Follow `handout/README.md` for the explicit publishing procedure.
