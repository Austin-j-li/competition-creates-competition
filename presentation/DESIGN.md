# Seminar presentation design contract

A 40-minute academic talk by Austin Li. The main sequence contains 24 slides, with
38 minutes of planned exposition and two minutes of transition/discussion allowance.
Fifteen technical slides follow the conclusion. The deck concerns the benchmark paper.

## Narrative and timing

| Slides | Purpose | Allocation |
|---|---|---|
| 1–7 | Motivation, fixed-information intuition, missing feedback, question, literature, contribution | 8 min |
| 8–12 | Information sets, preparation, trading, auction, equilibrium | 8 min |
| 13–16 | Acquisition profit, target-payoff spread, price inference, opposing incentives | 9 min |
| 17–20 | Sufficient conditions, theorem, benchmark, fixed-information comparison | 8 min |
| 21–22 | Scope/robustness and welfare/payment rules | 5 min, including 1 min allowance |
| 23–24 | Research agenda and conclusion | 2 min, including 1 min allowance |

The title teases the question. The contribution slide previews the answer before the
model. The theorem assumptions and uniqueness qualifications remain visible in the
main sequence. Detailed correspondence, robustness, bargaining and threshold material
is available through technical links and the overview.

## Visual system

- Instrument Serif for headings, display statements and pull lines, with true italics for
  the accented word; Geist for running text and labels; Geist Mono for numerals and
  controls. All are self-hosted files recorded in `vendor/uifonts/lock.json`.
  Mathematics uses the existing locked KaTeX fonts.
- One warm neutral family: cream paper `#f5f1e8`, ink `#1c1a17`, warm greys, hairlines
  `#d8d1c3`, a single ink-blue accent `#27479b`. Focal slides (title, question, theorem,
  conclusion) use warm charcoal `#1d1b18` with cream text and a lighter accent `#a7b8ea`,
  so the automatic theme reads as chapter dividers in the same palette. A fixed
  low-opacity grain overlay sits over both. A user can force light or dark throughout.
- Rules are 1 px hairlines; a 2 px accent rule marks only the strong-economy or accented
  case. Feature surfaces use the sand tone `#ece6d9` with a 2 px accent edge.
- Fixed 1600 × 900 surface. Main headings 76 px serif, typically two lines; title 136 px,
  deliberately two lines. Main body about 22–32 px. Equations use a separate scale.
- Flat compositions: timelines, actor columns, parallel payoff cases, annotated equations,
  a literature map, theorem rows, comparative results and technical tables.
- Controls occupy dedicated 44 px and 56 px screen rails outside the slide. They retain
  visible contrast, keyboard focus and touch targets. They are excluded from print.
- GSAP provides short scale/fade entrances and presenter-controlled reveals. No automatic
  slide advance. Reduced-motion preference disables transitions. Optional reading mode
  uses ScrollTrigger to introduce slide bodies while scrolling.
- No generic section kickers, decorative stock imagery or boxed status badges. Result
  status is plain source information in the slide footer, using the paper's vocabulary.

## Research invariants

The builder binds 16 research CSV sources through `handout/data.py`. Quantities come from
`CCC_DATA` or existing `CCC.explorer.closedForms`; the presentation solves no equilibrium.
Preserve accepted continuation identity, outward interval rounding, missing-node gaps,
endpoint conventions and the distinction between analytical, computer-assisted, numerical
diagnostic and open results. `input` renders as `declaration`.

A fixed-information comparison is a counterfactual when informative orders would not be
chosen in equilibrium. An acquisition-stage slider is not a solved equilibrium path.
Preparation, admissible bidding, sale and ownership remain different objects. Welfare
comparisons hold strength and sale terms fixed. Bargaining analysis concerns acquisition
payoffs, not a solved trading/participation game. Relevant qualifications belong on the
slide; speaker notes add explanation rather than supplying a missing essential condition.

## Source and engine responsibilities

- `content.js`: `createGlossary(H)` and `createSlides(H)`, audience copy, sources, notes,
  per-slide theme, timing, semantic layouts and symbol introductions.
- `deck.css`: layout, typography, themes, controls, print and reduced motion.
- `deck.js`: navigation, presentation/reading modes, glossary, equations, widgets and QA.
- `template.html`: accessible application shell and local dependencies.
- `build.py`: locked assets, bound research inputs, offline output, provenance and notes.

A slide record contains `id`, `act`, `title`, `subtitle`, `body`, `notes`, `source`,
`minutes`, `speakingMinutes`, `widget`, `status`, `defines`, `theme` and `backup`.
Main acts are `puzzle`, `model`, `mechanism`, `results`, `scope`, `next`. Main IDs are
`s01` through `s24`. Backup IDs are stable source identifiers, not display ordinals.
The engine numbers technical slides by their order in the deck.

`H.m` and `H.mi` generate block and inline math. `H.v`, `H.pct` and `H.fmt` retrieve bound
registry quantities. A symbol is introduced on or before its first mathematical use.
The G-key panel and four appendix notation pages share the same 41-entry glossary.

`data-step` defines presenter-controlled reveals. `data-goto` links slides. The
`DETAIL` map provides returnable technical detours. Input controls retain their arrow
keys. Escape closes a modal, leaves reading mode, or returns from a technical detour.

Retained widgets: auction outcomes, strength/payoff dial, posterior threshold, benchmark
comparison, fixed-order comparison, equilibrium correspondence, bargaining, certificates,
reserve table, price-access comparison and glossary. The old title and preview renderers
remain inert when no matching mount exists.

## Validation and delivery

`python3 presentation/build.py` verifies inputs and local libraries; `node
presentation/check_deck.mjs` checks slide records, timing, notation and internal links.
`check_browser.js` exercises all slides in three viewports and all three themes, as well
as keyboard reveals, sliders, technical returns, notes, reading mode and normal motion.
`DECK.selfCheck()` includes the 49 pre-existing formula comparisons. `DECK.audit()` checks
stage overflow. Screenshot review must also inspect equations and graphical labels.

The HTML works from a local file without network access. The PDF shows every slide and
reveal using a deterministic comparison state in the light theme, one 16 × 9 inch page
per slide. A changed HTML build invalidates an old generated PDF. Publishing remains an
explicit, separate action through `handout/publish.py`.
