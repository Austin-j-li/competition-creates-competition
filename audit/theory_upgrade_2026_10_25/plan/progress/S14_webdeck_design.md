# S14 web deck design

The production assistant restyled the web talk as a ruled document. The 34 frames, their titles, text, numbers, order, widgets and figure data stay unchanged. The deck uses ink on cool white, slate in the dark theme, Archivo for titles and instruments, STIX Two Text for prose, a 2 px title rule and 1 px hairlines. Colour is confined to the two concept roles in figures.

## Files

- `presentation/deck.css`: the complete ruled-document visual system, including neutral chrome, underlined text controls, ruled statements and tables, figure treatment, responsive layout and print layout. The F12/F12b additions and the dense F5 layout remain. Backup titles have a full-width 2 px rule.
- `presentation/deck.js`: neutral concept tokens in the F7 cost line; F12b and F13 chart heights are 220 and 242 design pixels so the ruled typography fits.
- `presentation/charts.js`: ink, grey and the two concept colours; Archivo figure text.
- `presentation/build.py`: variable-width font faces, the deck's own font lock, embedded local font data and the shared font files expected by the publisher.
- `presentation/fonts.lock.json` and `presentation/fonts/`: locked Archivo, STIX Two Text, Fira Mono and symbol faces with their licences.
- `presentation/DESIGN.md`: the design contract, typography, palette, controls and font delivery.
- `presentation/README.md`: the ruled-document description and font provenance.

## Commands

From the worktree root:

- `python3 presentation/build.py`: PASS. Compared 34 frames with the talk; 158 printed quantity references, 39 notation symbols and 30.25 planned minutes; built 34 frames with 90 quantities and 165 printed numbers.
- `node presentation/check_deck.mjs`: PASS. Frame order, titles, subtitles, targets, links and the deck contract match.
- `python3 handout/build.py`: PASS. Both PDFs built outside the repository; all six fragments, local assets, numerical displays and the page structure passed.
- `python3 handout/check_display.py`: PASS. Both page counts and hashes, 180 number spans, 53 formula numbers, the brief's locked local faces and offline delivery passed.
- `python3 handout/publish.py --stage-only …/site-stage3`: PASS. Staged 216 files: 54 at the root, 53 under `/talk/`, 54 under `/laplace/` and 55 under `/laplace/talk/`.

The first staging attempt stopped because the publisher expects the brief's full font list under `/talk/fonts/`. The build supplies those shared files as well as the deck's own faces; the final staging attempt passed without changing the publisher or any brief check.

## Browser inspection

At 1600 by 900, the staged talk has no runtime errors, no mathematics errors and no body overflow on any of the 34 frames with every reveal shown, in either theme. Computed title rules are 2 px on main frames and backups. Archivo and STIX Two Text load locally in the staged page.

The production assistant inspected all 14 images below. They show no clipping, purple, pills, cards, gradients, shadows or side stripes. Figures use only ink, greys and the concept colours.

- `…/kdeck/shots/cover-light.png`
- `…/kdeck/shots/cover-dark.png`
- `…/kdeck/shots/F12-light.png`
- `…/kdeck/shots/F12-dark.png`
- `…/kdeck/shots/F12b-light.png`
- `…/kdeck/shots/F12b-dark.png`
- `…/kdeck/shots/F13-light.png`
- `…/kdeck/shots/F13-dark.png`
- `…/kdeck/shots/F16-light.png`
- `…/kdeck/shots/F16-dark.png`
- `…/kdeck/shots/A8-light.png`
- `…/kdeck/shots/A8-dark.png`
- `…/kdeck/shots/A9-light.png`
- `…/kdeck/shots/A9-dark.png`

## Language review

The scan covered the six source and documentation files. Its hits are technical identifiers, file references in the design documentation, browser actions, code operations and the mathematical statement that an edge is open. None is a status claim, defensive prose, version narration or a name for the example. No visible slide text changed.
