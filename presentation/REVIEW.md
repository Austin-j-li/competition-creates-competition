# Seminar redesign review

Local review build, 28 September 2026. Based on GitLab `origin/main` at `674ffbd`.
Branch: `codex/seminar-redesign`. No publication has been performed.

## What changed

The talk now follows the agreed 24-slide sequence and 40-minute allocation: 38 minutes
of planned exposition plus two minutes for transitions and brief questions. Fifteen
technical slides carry proofs, diagnostics, extended comparisons and four notation pages.

The visual system uses Geist and Geist Mono, light technical slides, dark focal slides,
a cobalt accent, larger equations and flat diagrams. The opening establishes the public
preparation window, fixed-information deterrence, endogenous information, research
question, literature and contribution. The theorem's conditions and scope are visible
in the main sequence. Existing registry quantities and calculation functions are retained.

Navigation supports progressive reveals, keyboard controls, technical detours with return,
notes, a glossary, three theme modes, fullscreen and a scrolling reading mode. All runtime
libraries and fonts are local. PDF export shows deterministic comparison states and all
reveals. The build invalidates stale PDFs after an HTML change.

## Visual upgrade, 29 September 2026

The slide material is unchanged: `content.js`, `deck.js`, the bound data and the glossary
are byte-identical to the 28 September build. Only `deck.css`, `DESIGN.md` and `README.md`
changed.

- Instrument Serif (already locked in `vendor/uifonts`) now carries headings, display
  statements, pull lines and node claims, with true italics for the accented word; Geist
  remains for running text, Geist Mono for numerals. Title 136 px, main headings 76 px.
- One warm neutral family replaces the warm-paper/cool-grey mix: cream `#f5f1e8`, ink
  `#1c1a17`, hairlines `#d8d1c3`, sand surfaces `#ece6d9`. The accent is a desaturated
  ink-blue `#27479b` (previously an 85 %-saturated cobalt). Focal slides use warm charcoal
  `#1d1b18` with a lighter accent, so the automatic theme reads as chapter dividers rather
  than an unrelated dark deck.
- A pre-rasterised 160 px paper-grain tile is painted on the slide surface in both themes
  (no live SVG filter, no blend mode, no extra compositing layer); the print palette removes it.
- Full-width accent bars became 1 px hairlines; a 2 px accent rule survives only where it
  carries meaning (strong economy, accented payoff case, strong theorem column). The cast
  slide uses column rules instead of three boxed columns; the hero's rising bar motif
  became a value-line tick mark; the radial glow is confined to the dark surface.
- Segmented controls, custom range sliders, hover/active/focus states and 200 ms transitions;
  overview, notes and notation dialogs restyled; the notation panel's meaning column no
  longer inherits the numeric monospace rule.

Rechecked after the change: build (16 sources, locked assets), structural check, browser
layout audit on all 39 slides at 1600 × 1000, 1366 × 768 and 390 × 844 in automatic,
light and dark themes (no overflow), the full interaction sequence, the 49 formula
comparisons, screenshot review of every slide plus dialogs, reading mode and forced themes,
and a regenerated 39-page 16 × 9 inch PDF with rendered inspection of the title, theorem,
benchmark and bargaining pages.

## Verification

- Build passed with 16 manifest-bound research sources and locked local assets.
- Structural check passed: 24 main + 15 backup slides, 40-minute allocation,
  38-minute exposition, 41 glossary entries, and valid symbol introductions and slide links.
- Browser layout checks passed on all slides at 1600 × 1000, 1366 × 768 and 390 × 844,
  in automatic, light and dark themes.
- Browser interactions passed: reveals in both directions, auction winner, focused-slider
  keys, strength preset, benchmark/ownership quantities, fixed-information comparison,
  return from appendix, glossary, speaker notes, reading view and normal-motion reveal.
- All 49 existing formula comparisons passed; no math errors, runtime errors or unresolved
  placeholders. Reading mode showed no horizontal overflow on desktop or phone.
- Local-file loading with network disabled passed, including all formula checks.
- All 39 slides received screenshot review. PDF export has 39 pages at 16 × 9 inches;
  representative title, theorem, benchmark and glossary pages received rendered inspection.
- Changed HTML removed the prior generated PDF as intended. The final export was regenerated.
- `git diff --check` passed. Changes are confined to `presentation/`.

These checks verify presentation behaviour and binding to existing research output.
They are not a new independent audit of the paper's proofs or research acceptance gate.

## Review artifacts

- `dist/index.html`: interactive deck; preview at http://127.0.0.1:8776/ while the server runs.
- `dist/presentation.pdf`: static light-theme export.
- `dist/speaker-notes.md`: timed notes and anticipated questions.
- `dist/provenance.json`: bound source and library hashes.
- `seminar-redesign.zip`: portable offline package; unzip and open `index.html`.
- `qa/browser-check.json` and `qa/`: browser results and screenshots (local, ignored).

Visual and academic presentation review remains with the author. Publishing the reviewed
site is a separate Cloudflare action. The main handout has not been redesigned in this build.
