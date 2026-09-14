# Deck design contract ("After hours")

The contract between the three deck files: `content.js` (slides), `deck.css` (visual
system) and `deck.js` + `template.html` (engine and widgets). Every name below is binding;
change the contract before changing a name.

## 1. Brief

Research talk, 40 minutes, seminar room projector, theorist audience plus the supervisor
(Alex Gorbenko, M&A auctions and bidder entry). The deck must feel cinematic and
interactive, not Beamer: a blue-black ground, one warm amber accent, Instrument Serif for
the big words, JetBrains Mono for every number, Libre Franklin for running text. A
projector variant (warm off-white ground, same identity) is one key press away.

Invariants that do not move:

- Offline. Fonts, KaTeX, data and PDFs are local. No network at runtime.
- Every number on a slide comes from `window.CCC_DATA` (registry, tables, fig1..fig4) or
  from `window.CCC.explorer.closedForms(P, r)` arithmetic. Nothing is solved in the deck.
- Result vocabulary on slides: `analytical`, `computer-assisted`, `numerical diagnostic`,
  `open`; declarations carry `input`. Rendered as a stamp in the slide footer.
- Hedges ("not an empirical estimate", "not an equilibrium simulation", "not a joint
  calibration"...) live in speaker notes and the source line, never in slide body copy.
- The endogenous-insider fork is excluded. Benchmark paper only.
- Voice: single author, "I". Sentence case. No AI copy cliches. Plain finance English.

## 2. Slide record (content.js exports `window.createSlides(H)`)

```js
H = { m(latex, cls), mi(latex), v(key), pct(key), fmt(key, digits), link() }
S(id, { act, kicker, title, subtitle, body, notes, source, minutes, widget, backup, status })
```

- `id`: `s01`..`s22` main, `b1`..`b7` backup. Zero-padded main ids.
- `act`: one of `question | setting | mechanism | result | scope | next | backup`.
- `kicker`: short mono label above the title (may be empty). Example: `Turn the dial`.
- `title`: sentence, may contain `<i>word</i>` for the amber italic word. Title slide: empty.
- `subtitle`: one line, may be empty.
- `body`: HTML using only the class vocabulary in section 4 plus widget ids in section 5.
- `notes`: full speaker prose. Include every hedge that used to sit on the slide, and end
  with one line `If asked: ...` naming the question a theorist or Gorbenko will raise and the
  answer or backup slide.
- `source`: paper anchors, e.g. `Proposition 2; Online Appendix C.0`.
- `minutes`: number; main slides sum to 40. Backups 0.
- `widget`: `'' | title | puzzle | auction | dial | tape | economies | control | coexist |
  bargaining | certificates | reserve`.
- `status`: `'' | analytical | computer-assisted | numerical diagnostic | open | input`.
- `defines`: array of glossary keys this slide introduces (see section 10). A symbol may
  appear in slide copy only on or after the slide that defines it; `check_deck.mjs` fails
  the build otherwise.

`content.js` also exports `window.createGlossary(H)`: an ordered array of
`{key, latex, meaning, group, pattern}` covering every symbol the talk uses (section 10).

## 3. Markup the engine produces

Chrome (`template.html`):

```html
<a class="skip" href="#stage">Skip to slide</a>
<main id="stage" tabindex="-1" aria-label="Presentation"><div id="deck"></div></main>
<nav class="hud" aria-label="Presentation tools">
  <button id="overview">Slides</button><button id="notes">Notes</button>
  <button id="theme">Projector</button><button id="fullscreen">Fullscreen</button>
  <button id="help" aria-label="Presentation controls">?</button>
</nav>
<footer class="rail">
  <ol id="acts" class="acts"></ol>
  <div class="pager"><button id="return" hidden>Return to talk</button>
    <button id="previous" aria-label="Previous">←</button><span id="counter"></span>
    <button id="next" aria-label="Next">→</button></div>
  <span id="progress-label"></span>
</footer>
<dialog id="panel"><div class="panel-heading"><h2 id="panel-title"></h2>
  <button id="close-panel">Close</button></div><div id="panel-body"></div></dialog>
<div id="announcer" class="sr-only" aria-live="polite"></div>
<div class="grain" aria-hidden="true"></div>
```

Stage geometry: `#deck` is a fixed 1600 x 900 design surface. The engine sets
`--stage-scale` on `#stage` to `min(innerWidth/1600, (innerHeight - 56)/900)` on load and
resize; CSS applies `transform: scale(var(--stage-scale))` with `transform-origin: top
center`. Fonts are therefore absolute pixels at 1600 x 900. Print resets the transform and
lays one slide per 16in x 9in page.

Each slide:

```html
<section class="slide" id="s09" data-act="mechanism" data-widget="auction"
         data-status="analytical" aria-label="9. Who wins, who pays">
  <header class="slide-head"><p class="kicker">…</p><h2>…</h2><p class="sub">…</p></header>
  <div class="slide-body">…</div>
  <footer class="slide-foot">
    <span class="stamp" data-status="analytical">analytical</span>
    <span class="source">…</span>
    <button class="detail" data-goto="b1">Technical detail</button>
  </footer>
</section>
```

`.slide.active` is displayed; others `display:none`. `.reveal[data-step=n]` elements get
`.shown` when the step is reached. Acts rail: `#acts` holds six `<li data-act>` with the
act name; the current one has `data-current`, and `--p` (0..1) gives progress inside it.

## 4. Class vocabulary (content.js uses, deck.css styles)

Layout: `.hero` (title composition: left text, right ambient), `.split` (2 col), `.split.wide`
(1.45fr 1fr), `.split.narrow` (.8fr 1.2fr), `.stack` (column, gap), `.row` (inline row, gap),
`.center` (vertically centred body).

Type: `.display` (large serif statement, `<i>` for amber), `.sub`, `.kicker`, `.small`,
`.muted`, `.accent`, `.num` (mono tabular figure), `.metric` (very large serif number),
`.metric-label`, `.endline` (closing statement), `.byline`.

Components: `.callout` (amber left rule, serif), `.timeline > article` (6 steps, horizontal),
`.cast > article.role` (four roles; `.symbol` + `h3` + `p`), `.conditions > .cond`
(`<b>A1</b>` + `.job` plain-language line + `.formal` LaTeX, formal is a `.reveal`),
`.data-table` (mono numerals, amber `.highlight`), `.comparison > .economy(.strong)`,
`.references`, `.controls` (instrument strip under a diagram: `label`, `input[type=range]`,
`output`, `.segmented > button[data-choice][data-value][aria-pressed]`, `button[data-reset]`),
`.plot-shell` + `.plot-caption`, `.readout` (stack of `.kicker` + `.metric`), `.dots` (puzzle
grid), `.reveal[data-step]`, `.print-only`.

Math: `H.m(latex)` produces `<div class="equation">`; add `eq-small` or `eq-big` as the
second argument. `H.mi(latex)` produces inline math.

## 5. Widgets (engine renders into these ids; content must include them)

| widget | elements content.js must include | behaviour |
|---|---|---|
| `title` | `#title-ambient` | slow ambient drift of a faint value line; no data |
| definition strip | `<div class="defs" data-defs="r,R"></div>` on any slide | engine fills a two-column strip (symbol in KaTeX, meaning) from the glossary for the listed keys; content uses it on the model slides so every symbol is defined where it first appears |
| `preview` | `#preview-vline` | the value line in words, no symbols: ticks labelled `reserve`, `low challenger`, `high challenger`, a support bar labelled `incumbent's range`; reveal 1 stretches the bar (weak to strong), reveal 2 shows two brackets: `what the challenger keeps` (shrinks) and `what shareholders receive, by challenger type` (widens) |
| `glossary` | `#glossary-table` | renders `createGlossary` as a grouped table: symbol (KaTeX), meaning, first slide |
| `auction` | `#auction-vline`, `#auction-r` (range), `#auction-r-value`, `.segmented[data-choice=quality]` H/L, `[data-reset=auction]`, `#auction-readout` | value line 0..h with reserve p, ℓ, h, incumbent support [0,r_strong] and realised R marker; readout: winner, payment, challenger gross profit |
| `dial` | `#dial-vline`, `#dial-r`, `#dial-r-value`, `.segmented[data-choice=dial-preset]` weak/strong, `#dial-profit .metric`, `#dial-spread .metric`, `#dial-curves` | same value line; support stretches with r; two count-animated metrics `B_r(1/2)` and `Delta_T` from closedForms; `#dial-curves` draws both curves from fig1 with the marker at r |
| `tape` | `#tape-plot`, `#tape-x`, `#tape-x-value`, `#tape-demo`, `[data-reset=tape]`, `#tape-readout` | posterior vs order flow under Laplace, plateau shaded; reveal 1 posterior curve, 2 threshold τ line, 3 readout (price, cost-averaged preparation) |
| `economies` | `.segmented[data-choice=benchmark]` weak/strong, `#economies-compare`, `#economies-view` | economy cards from `equilibrium_controls` feedback rows |
| `control` | `.segmented[data-choice=experiment]` feedback/frozen, `#control-plot`, `#control-readout` | two bars animate between feedback and frozen rows; readout "Entry rises / falls" |
| `coexist` | `#coexist-plot` | r axis 1..3.8, preparation axis; reveal 1: three analytical nodes (r_weak, r_strong, r_collapse from `equilibrium_controls`), not joined; reveal 2: three certified nodes from `tables.certificates` as outward-rounded interval bars plus dashed pooling level ρ over the region where pooling exists (`fig2.thresholds`, `fig2.regions`); reveal 3: collapse annotation |
| `bargaining` | `#seller-weight`, `#seller-weight-value`, `.segmented[data-choice=eta]`, `#bargaining-plot`, `#bargaining-readout` | as before, from fig4 |
| `certificates` | `#certificate-table` | as before |
| `reserve` | `#reserve-table` | table from `tables.reserve_comparisons`; numbers to 3 decimals, status leading word |
| `access` | `#access-table` | price-hidden versus price-observed table at the strong incumbent from the registry (`base_hidden_entry_strong`, `base_entry_strong`, `base_revenue_hidden`, `base_revenue_feedback`, `base_net_surplus_gain`) |

SVG classes for deck.css: `.plot` (root), `.axis`, `.grid`, `.tick` (mono), `.label` (sans),
`.curve`, `.curve.secondary`, `.point`, `.node` (analytical), `.cert` (certified interval),
`.shade`, `.marked` (dashed guide), `.bar-fill`, value line: `.vl-axis`, `.vl-support`,
`.vl-marker`, `.vl-reserve`, `.vl-tick`, `.vl-label`.

## 6. Tokens and type

```css
:root{ --g:#0c1117; --g2:#121a24; --g3:#18222e; --t:#ece5d8; --t2:#c9c2b4; --m:#8e98a6;
  --l:#26303d; --a:#e2a13a; --a2:#f0c46b; --a-soft:rgba(226,161,58,.14); --ghost:#5d6b7c;
  --serif:"Instrument Serif",Georgia,serif; --sans:"Atkinson Hyperlegible",Franklin,Arial,sans-serif;
  --spring:cubic-bezier(.32,.72,0,1); --hi:rgba(255,255,255,.08); --edge:rgba(255,255,255,.07); --lo:rgba(0,0,0,.8);
  --mono:"JetBrains Mono",Prime,"Courier Prime",monospace; color-scheme:dark }
:root[data-theme=light]{ --g:#f4efe4; --g2:#ece6d8; --g3:#e3dccb; --t:#1a1710; --t2:#3d382e;
  --m:#6a6459; --l:#d3cbb9; --a:#b4761a; --a2:#8f5c10; --a-soft:rgba(180,118,26,.14);
  --ghost:#a39c8c; --hi:rgba(255,255,255,.75); --edge:rgba(40,30,10,.09); --lo:rgba(60,45,20,.28); color-scheme:light }
```

Font faces (self-hosted, files copied into `dist/`): `"Atkinson Hyperlegible"` 400 and 700,
regular and italic (`uifonts/AtkinsonHyperlegible-*-latin.woff2`; the running-text face,
chosen for width and legibility at distance), `Franklin` (LibreFranklin variable 300–900,
fallback), `Prime` (Courier Prime), `"Instrument Serif"` regular + italic
(`uifonts/InstrumentSerif-Regular-latin.woff2`, `-Italic-latin.woff2`), `"JetBrains Mono"`
variable 400–700 (`uifonts/JetBrainsMono-400-700-latin.woff2` and `-greek.woff2`).

Type scale at 1600 x 900: title h1 138px serif; slide h2 58px serif 400, letter-spacing
-.012em, line-height 1.04; `.display` 54px serif; `.sub` 24px Franklin 300 `--m`; body 24px
Franklin 400 `--t2`; `.small` 18px; `.kicker` 14px mono uppercase tracking .14em `--m`;
`.metric` 104px serif tabular; `.num` mono; `.source` 13px mono `--m`; `.stamp` 12px mono
uppercase. Slide padding 64px 88px 56px. Title `<i>` and `.display i` are amber, not italic
in mono. KaTeX equations 30px (eq-small 24, eq-big 40), left aligned, colour `--t`.

Surfaces: machined, not flat. The economy cards, definition strips, instrument strips
(`.controls`), the tools pill and the rail island are `--g2` shells with a 1px `--edge`
border, an inner top highlight (`inset 0 1px 0 --hi`) and a soft tinted drop (`--lo`);
the economy cards carry a concentric inner outline. Rules (1px `--l`) and one amber rule
carry hierarchy elsewhere. Equations are one object per line inside a column; the layout
audit (`await DECK.audit()`) must return an empty list. Grain: fixed full-screen SVG turbulence overlay at 0.16 opacity, pointer-events none,
hidden in print. Ambient: one radial amber glow bottom-right on the title slide only.

Stamps: `analytical` amber outline; `computer-assisted` amber dashed outline;
`numerical diagnostic` ghost outline; `open` ghost outline with the word only; `input`
renders the word `declaration` in `--m` without an outline.

## 7. Motion

- Every transition uses `--spring` (`cubic-bezier(.32,.72,0,1)`); never linear or ease-in-out.
- Reveal: opacity 0 → 1, translateY 18px → 0, blur 6px → 0, 700 ms.
- Slide change: incoming `.slide-head` and `.slide-body` rise 14px with a 4px blur over 650 ms.
- The two action buttons (`#tape-demo`, `#economies-compare`) carry a nested circular arrow
  that shifts on hover.
- Numbers count with `requestAnimationFrame`, 700 ms, ease-out; sliders update instantly.
- Value-line support and bars transition `transform` 500 ms; never width/height.
- `prefers-reduced-motion` disables everything and shows final states.

## 8. The arc (22 main, 7 backup; minutes sum to 40)

Six blocks. Numbers from the registry appear on main slides only as annotations inside a
result figure, labelled "at the declared benchmark"; never as a headline. Every symbol is
defined on the slide where it first appears (section 10).

| id | act | kicker | title | widget | status | defines | min |
|---|---|---|---|---|---|---|---|
| s01 | question | | (title) Competition creates competition. | title | | | 0.5 |
| s02 | question | The institution | A public sale, a traded stock, and a buyer deciding whether to prepare. | | | | 2.5 |
| s03 | question | The myth | Stronger rivals deter entry. | | | | 2 |
| s04 | question | The question | Can a stronger rival bring a buyer in? | | | | 2 |
| s05 | preview | The mechanism in one picture | Two claims on one surplus. | preview | | | 1.5 |
| s06 | preview | Antecedents | Learning from prices, and what is new here. | | | | 1 |
| s07 | model | Players and values | Two bidders, one target, one reserve. | | input | R, r, theta, ell, h, p | 1.5 |
| s08 | model | Preparation | A cost that must be paid before an executable bid. | | input | C, c_L, c_H, rho, e | 1.5 |
| s09 | model | Trading | An informed investor, noise demand, competitive market makers. | | input | q, Z, b, X, k, P, mu | 2 |
| s10 | model | Timing | Sale rule, order, price, cost, preparation, bids. | | input | | 1.5 |
| s11 | model | The auction | Who wins, who pays, who keeps the surplus. | auction | analytical | g_H, g_L, t, Delta_T, B | 2 |
| s12 | equilibrium | Equilibrium | Prices are Bayesian; deviations hold schedules fixed. | | | sigma, mu_P, e_schedule | 2 |
| s13 | equilibrium | What the price reveals | Bounded posteriors, a threshold, and a residual advantage. | tape | analytical | m, M, tau, x_star, A_H | 3 |
| s14 | results | Proposition 1 | One auction, two claims, opposite responses. | dial | analytical | | 2.5 |
| s15 | results | Proposition 2 | Three conditions, one open set. | | analytical | r_0, r_1 | 2 |
| s16 | results | Proposition 2, seen | Stronger competition raises preparation. | economies | analytical | E, O_H | 2 |
| s17 | results | Control one | Freeze the information and deterrence returns. | control | numerical diagnostic | | 2 |
| s18 | results | Control two | Change the payment rule and the sign flips. | bargaining | analytical | eta, Delta_eta | 2 |
| s19 | results | Proposition 3 | Between the two economies, equilibria coexist. | coexist | computer-assisted | r_2 | 3 |
| s20 | next | Robustness | The mechanism survives changes in primitives. | | analytical | | 1.5 |
| s21 | next | What comes next | Evidence, and the seller's problem. | | open | | 1.5 |
| s22 | next | | Competition creates competition. | | | | 0.5 |
| b1 | backup | Global bounds | The trading outcome is pinned by global bounds. | | analytical | A_L | 0 |
| b2 | backup | Why Laplace | Bounded posteriors and the plateau. | | analytical | | 0 |
| b3 | backup | Certificates | Three computer-assisted equilibria. | certificates | computer-assisted | | 0 |
| b4 | backup | Access to prices | Seeing the price improves acquisition outcomes. | access | analytical | V_T, d | 0 |
| b5 | backup | Reserve comparisons | Fixed-reserve comparisons with supported continuations. | reserve | numerical diagnostic | | 0 |
| b6 | backup | Notation | Every symbol in the talk. | glossary | | | 0 |
| b7 | backup | Sources | Sources and research boundaries. | | | | 0 |

Technical-detail links: s10→b6, s12→b1, s13→b2, s15→b1, s19→b3, s21→b4, s22→b7.
Acts in rail order: question, preview, model, equilibrium, results, next.

Literature placement: the entry and deterrence papers (Fishman 1988; Hirshleifer and Png
1989; Levin and Smith 1994; Gentry and Stroup 2019; Roberts and Sweeting 2013) are the myth
on s03. The feedback papers (Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang
2015; Luo 2005; Persico 2000; Betton et al. 2014) and the increment are s06. b4 also carries
the matched-price diagnostic (the old b5) as its second half.

## 9. Data reference

`window.CCC_DATA`: `inputs` (h, ell, p, rho, c_L, c_H, b, k, r_weak, r_strong, r_collapse as
strings), `registry[key] = {display, value, lower, upper, units, status, ...}`, `fig1` (r[],
Delta_T[], B{'0.5':[]...}), `fig2` (branches, nodes, certificates, thresholds, regions),
`fig3` (Laplace, logistic posterior tails), `fig4` ({'1.2','3'} → eta[], Delta_eta[]),
`tables` (auction_primitives, equilibrium_controls, extensions, moderate_values,
reserve_comparisons, feedback_comparisons, thresholds, certificates).
`window.CCC.explorer.closedForms(P, r)` returns g_H, g_L, Delta_T, B_prior, tau, t_0, t_L,
t_H, x_star, E, O_H, alpha_H, alpha_L and the A1–A3 chips. The current `deck.js` shows how
each existing widget reads these; reuse those readers.

## 10. Glossary and the notation rule

`window.createGlossary(H)` returns entries in introduction order:

```js
{ key:'Delta_T', latex:String.raw`\Delta_T`, meaning:'target-payoff spread: the gap in
  target proceeds between a high- and a low-value challenger, per share', group:'derived',
  pattern:String.raw`\\Delta_T` }
```

- `key`: plain identifier used in `defines` and `data-defs`.
- `latex`: rendered by KaTeX in the definition strip, the glossary panel and b6.
- `meaning`: one clause in plain English, no symbols other than the entry's own.
- `group`: `values | preparation | trading | prices | derived | outcomes | institutions`.
- `pattern`: a regular expression (string) matching the symbol inside LaTeX source. The
  check tokenises every `m()` and `mi()` argument on a slide and flags any pattern match
  whose key is not in the union of `defines` over slides up to and including that one.
  Backups count after all main slides. Plain words in body copy are not checked.

Engine: `G` key and the hud button `Notation` open the glossary panel (grouped table).
`<div class="defs" data-defs="…"></div>` is filled from the glossary at load. Widget
`glossary` renders b6 from the same source. One definition, three surfaces.

Keys the talk needs: R, r, theta, ell, h, p, C, c_L, c_H, rho, e, q, Z, b, X, k, P, mu,
g_H, g_L, t, Delta_T, B, sigma, mu_P, e_schedule, m, M, tau, x_star, A_H, A_L, r_0, r_1,
r_2, E, O_H, eta, Delta_eta, V_T, d.
