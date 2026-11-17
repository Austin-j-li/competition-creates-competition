# Figure hooks a look can style

Every rule below sits in `figs.css` (common part and the entry chart) or `bars.css` (page 14's
split bars, in its own file). A look overrides any of them under
`body[data-look="…"]`. Colours reach the figures only through the shared tokens
(`design/tokens.css`); the custom properties listed here are the only other hooks.

## Custom properties

| Property | Default | Used for |
|---|---|---|
| `--fig-share-fill`, `--fig-rival-fill`, `--fig-shade-fill`, `--tint-fill` | the flat tokens | filled areas; point one at a screen: `url(#scr-a-entry)` |
| `--scr-ink`, `--scr-w`, `--scr-pitch` | `--fig-ink`, 1.5px, 9 (px) | the line screens' line colour, weight, pitch |
| `--dash-mixed` | `14px 9px` | `.br-mixed`, the dashed stretch from 1.75 to 1.97 |
| `--dash-hidden` | `18px 11px` | `.cmp-hidden`, page 20's "price hidden from the rival" |
| `--dash-drop` | `0.1px 9px` (round caps: dots) | `.br-drop`, `.cmp-drop`, the connectors at 3.59 |
| `--fig-axis-w` | `2px` | axes, ticks, brackets, shade edges, the control's marker (no data) |
| `--fig-line` | the look's token | `.br-none`, `.br-mixed`, `.cmp-hidden`, the connectors, `.inc-tick` |
| `--fig-line-heavy` | the look's token | `.br-up`, `.br-floor`, `.cmp-fixed`; `.br-trace` is three times it |
| `--fig-dot` | the look's token | radius of `.dot-end`, `.dot-open`; incumbents' `.dot` is 2px larger |

## Line screens

Each figure's SVG defines `#scr-a-<fig>` (lines at 45°) and `#scr-b-<fig>` (lines at 135°), whose
line is `.screen-line`. The entry chart's are `#scr-a-entry` and `#scr-b-entry` (one copy per
page, identical; the first in the document is the one `url()` finds, and it draws even when its
page is hidden). Its only filled area is `.shade`.

## The entry chart (pages 19, 20, 22)

Mount `.fig[data-fig="entry"][data-variant="p14|p16|p17"]` (variant names from before the 17 November deck: main pages 19, 20, 22) > `svg.fig-svg` plus HTML `.fig-label`
spans. The figure draws its own motion (lines drawn along x behind a clip, dots arriving when the
line reaches them); the engine's fade is switched off for its SVG steps.

- Axes: `.ax` (both axis lines), `.ax-tick`, `.ax-label` (tick numbers, HTML), `.ax-title`
  ("entry", "incumbent strength r", HTML). `.plot-frame` is an unpainted box (the carry key).
- Branches, all `.br` plus exactly one of:
  `.br-none` (no informed order, solid), `.br-mixed` (dashed, 1.75 to 1.97),
  `.br-up` (informed orders where entry is above ρ: the ramp and the stretch at 0.52; the accent),
  `.br-drop` (dotted connector at 3.59, carries no data), `.br-floor` (the stretch at ρ after
  3.59; not accent), `.br-trace` (page 20's pale trace of the full model),
  `.cmp-fixed` ("orders held fixed"), `.cmp-drop` (its dotted connector at 3.59),
  `.cmp-hidden` ("price hidden from the rival", dashed).
- Marks: `.dot[data-inc="0|1|2"]` (the incumbents), `.dot.dot-end` (filled end of a branch at
  1.39 and 3.59), `.dot.dot-open` (open circle at 1.97), `.inc-tick[data-inc]` (a short tick on
  the strength axis for each incumbent).
- Areas and furniture: `.shade` (fill `--fig-shade-fill`), `.shade-edge`, `.bracket`.
- HTML labels (all `.fig-label`): `.inc-label[data-inc]` with `.inc-word` and `.inc-sym`,
  `.bracket-label`, `.shade-label` ("◂ two equilibria coexist"), `.model-label`
  ("full model"), `.cmp-label[data-cmp="fixed|hidden"]`.
- The strength control (key S): `.ctl-stop` (where it can stop), `.ctl-marker`,
  `.ctl-dot[data-line="model|fixed|hidden"]`, `.ctl-readout[data-role="r|entry"]` (HTML).

The incumbents' labels `.inc-label` carry a ground-coloured background (knocked out of the
shade's screen where they cross it).

Page layout of these pages (in `figs.css`): `.chart-page`, `.chart-body`, `.chart-side`,
`.chart-note`, `.rowtxt` (a paragraph of the text column; the column is set at
`max(26px, 0.9 × --fs-body)`, as the master sets it at 16 pt against an 18 pt body), `.claim.is-tint` (page 20's claim:
a default plain tint). Page 19 has no table.

Carry keys: `frame` (the plot frame), `dot-0|1|2`, `sym-0|1|2` (the incumbent's symbol, at the
same box on pages 19, 20, 22), and on page 19 `inc-0|1|2` (the whole label, which page 17's
column heads travel onto).

## The region figure (`region.js`: backup B3, pages 1 and 2)

Mount `.fig[data-fig="region"][data-variant="b24|b25"]` > `svg.fig-svg` plus HTML `.fig-label` spans
placed by `data-place`. The master's pictures redrawn from the closed forms; backups show whole (no
steps, no motion).

- **b24** (420 x 450): the coexistence region in the plane (Δ_T, τ) at π = 1/2. `.region-fill` (the
  look's shade screen, redrawn in the figure's own pattern `#scr-a|b-region-<page>`), `.bound` (the
  lower bound k/(1 − τ), the upper bound k/(ρ max{π, 1 − π}), the top at M(1/2)), `.bound-split`
  (dashed, k/(1 − M(1/2)): mixing to its left, buying for sure to its right), `.guide` (the dotted
  levels M(1/2) and π). The example's path: `.path.path-ink` from r0 to r_A, `.path.path-up` (green)
  from r_A to the arrowhead `.path-head` at the plot's edge, where the informative market exists
  (the build checks τ ≤ M(1/2) up to the edge and stops otherwise). Points: `.dot` (r0), `.dot.dot-end`
  (r_A, r_F, r_N). Places: `panel`, `ytitle`, `xtitle`, `M`, `pi`, `coex`, `r0`, `rA`, `rF`, `rN`.
- **b25** (980 x 396): panels (a) and (c), entry against strength. Branches: `.br-none` (N),
  `.br-q` (Q, dash-dot), `.br-mix` (R, heavy dashed green), `.br-up` (F above the floor),
  `.br-floor` (F at the floor after r_C), `.br-thresh` (T, thin dashed green). The band [r_A, r_N]
  (this page's text) is a `.region-fill`; `.guide` keylines at r_A, r_N, r_C in (a) and r_A, r_F,
  r_N, r_J, r_S in (c); `.zoom` and `.zoom-head` (the double arrow over the stretch (c) enlarges).
  Places: `panel:a|c`, `ytitle:a`, `xtitle:a|c`, `guide:<at>:a|c`, `zoom:a`, `N:a`, `F:a`,
  `Ffloor:a`, `N:c`, `Q:c`, `R:c`, `T:c`, `F:c`, `coex:c`.

Data: `TALK.data.extra.charts.region.b24|b25` (`build_data_charts.py`); tick labels are `kind: "axis"`
rows of the numbers table (`b24.ax.*`, `b25.ax.*`).

## The research chart (`research.js`: page 23 and backup B12's second page)

Mount `.fig[data-fig="research"][data-variant="p18|b47"]` > `svg.fig-svg` plus HTML `.fig-label`
spans placed by `data-place`. It uses the entry chart's classes: `.ax`, `.ax-tick`, `.ax-label`,
`.ax-title`, `.br-none` ("no research" / zero research), `.br-up` (research where a purchase
attracts the costly rival: the rise and the stretch at the cap; the accent), `.br-q` (b47:
floor-entry research on (r_N, r_Q) and past r_C, dash-dot), `.dot[data-inc]`, `.dot-end` (accent ends), `.dot-open` (b47: r_Q, and entry at r_C), `.dot-stop` (the plain end
of "no research" at r_N), `.shade` (page 23: the strengths with more than one equilibrium),
`.shade-edge`, `.bracket`, `.bracket-label`, `.guide`; and its own `.arrow` (the arrowhead where
the stretch at the cap leaves the plot). Label modifiers: `.is-bold`, `.is-quiet` (secondary
ink), `.is-knock` (a ground-coloured knockout for a label set inside the shaded region).

Its screens are `#scr-a-research` and `#scr-b-research`. The module reads the look's
`--fig-shade-fill` and points it at its own screen, and copies `--scr-ink`, `--scr-w`,
`--scr-pitch` from the entry chart's mount (where the plate look sets them); a look that wants to
style the research chart directly can set those on `.fig[data-fig="research"]`.

Curves: `TALK.data.extra.charts.research` (written by `build_data_charts.py` from the closed forms
of `handout/figures.js`, `lambdaR` and `entryResearch`, with every boundary strength a registry
row).

## Motion shared by both charts

A forward click draws its lines left to right behind a clip that grows along x; each dot arrives
when the line reaches it; a dotted drop sits in its own layer (`.layer-drops`) and is drawn
downward by a second clip that grows along y (on page 19, click 3, the drop first and then the
floor from its foot; on page 20, when the comparison line reaches it). The look's own wipe
(`plate.js`) is cancelled on these figures' SVG step groups, so the figure's drawing is not
replaced; the look's wipe of HTML labels stays.
