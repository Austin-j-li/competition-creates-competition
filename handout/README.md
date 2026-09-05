# Handout: interactive HTML companion to the paper

`python3 handout/build.py` reads the repo's validated CSVs and the scalar registry, fills the
section fragments, inlines everything, and writes `docs/index.html` (one self-contained file),
`docs/.nojekyll`, and copies of the two built PDFs. GitHub Pages serves `docs/` from this branch.
The build exits nonzero on any failed check. `numerics/verify.py --final` runs it as the `handout`
stage. No number on the page is typed by hand: scalars come through `[[name]]` placeholders
resolved from `numerics/quantity_registry.csv` (column `display`, same rules as
`numerics/substitute.py`), tables are generated from CSV rows, and charts read `window.CCC_DATA`,
which is emitted from the CSVs with every token copied verbatim.

## Files

| File | Owner | Role |
|---|---|---|
| `build.py` | pipeline | orchestration, checks, manifest (`numerics/manifests/handout.json`) |
| `data.py` | pipeline | CSV slices to `window.CCC_DATA` (deterministic emitter) |
| `tables_html.py` | pipeline | CSV rows to `<table>` HTML, mirrors `numerics/render/tables.py` formatting |
| `vendor.lock.json` | pipeline | pinned CDN URLs, versions, sha512 integrity |
| `crosscheck.py` | explorer | Python closed forms vs CSV rows at the benchmark, tolerance 1e-9 |
| `explorer.js` | explorer | closed forms in the browser, slider, chips, explorer chart, `selfTest()` |
| `template.html` | shell | page skeleton with slots |
| `style.css` | shell | tokens, layout, components |
| `app.js` | shell | theme, progress, scrollspy, details, stepper, KaTeX, `CCC.selfCheck()` |
| `charts.js` | figures | Plotly builders for fig1 to fig4, theme rerender, lazy mount |
| `sections/*.html` | content | prose fragments with placeholders and mount points |

Every file is plain ES2019 JavaScript, CSS, HTML, or stdlib Python 3.11+. No bundler, no npm,
no imports from `numerics/` (those pull numpy and scipy; the build must run in a bare Python).

## Vendor (CDN, pinned)

| Asset | URL | sha512 |
|---|---|---|
| Plotly 3.5.1 basic | `https://cdnjs.cloudflare.com/ajax/libs/plotly.js/3.5.1/plotly-basic.min.js` | `sha512-YnU1t4Rre6Tw27Vlb0ThLdBjGJizJLFcBmNIoUtyC8lznPx96xKdc6zGpkwqxlnU7vgGQJHjMT4ra2YUA+lcVA==` |
| KaTeX 0.18.5 css | `https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.18.5/katex.min.css` | `sha512-eLvr2vghJzBvLDxpgIyx3qrDj1chzZfD4SPOE4otnJPa6GsyJ/lBDGFhZO8OsmyYNnqqjqXOSjHAV1cBax33oA==` |
| KaTeX 0.18.5 js | `https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.18.5/katex.min.js` | `sha512-yRrA0fXbfdjHDJXBxj4ABSlaLGZk5HOm5qpvXx6GEjR1t5yCLdenOvN9hzHZhrznHyHVKuIK+QltSR4gc//lQA==` |
| KaTeX auto-render | `https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.18.5/contrib/auto-render.min.js` | `sha512-0HzJcHCD+wBh9kNUUcm3DWH9IbNDfudsYyMD5EHwSuFK6aEsaa/UEPqqk4t0pm4bbmwR6A11yNsD7Q+nz6XF+Q==` |

All tags carry `integrity` and `crossorigin="anonymous"`. Scripts load with `defer`; inline
page scripts run on `DOMContentLoaded`. `build.py --verify-vendor` refetches and checks the hashes.
KaTeX 0.18 prefixes its internal class names; page CSS styles only `.math-block`, never KaTeX
internals.

## Template slots (`template.html`)

HTML comments, exact text: `<!-- @@VENDOR_HEAD@@ -->` (KaTeX css link), `<!-- @@THEME_BOOT@@ -->`
(inline script that sets `data-theme` before paint), `<!-- @@STYLE@@ -->` (inlined `style.css`
inside `<style>`), `<!-- @@TOC@@ -->` (generated `<ol>` of links), `<!-- @@SECTIONS@@ -->`
(the fragments in file order), `<!-- @@DATA@@ -->` (`<script>window.CCC_DATA = {...};</script>`),
`<!-- @@APP@@ -->`, `<!-- @@CHARTS@@ -->`, `<!-- @@EXPLORER@@ -->` (each an inlined `<script>`),
`<!-- @@VENDOR_SCRIPTS@@ -->` (the three deferred CDN script tags), `<!-- @@BUILD_META@@ -->`
(a short colophon fragment: registry hash and source hashes, no timestamps).

The template also contains the header (title, "Austin Li, UCL", the status line, links to
`main_filled.pdf` and `online_appendix_filled.pdf` as relative hrefs, the theme toggle button
`<button id="theme-toggle">`), the progress bar `<div class="progress" id="progress">`, the
`<nav class="toc" id="toc">` wrapper, `<main id="main">`, and the footer. Placeholders such as
`[[seed_python_version]]` are allowed in the template; the build resolves them there too.

## Section fragments (`sections/`)

Files in build order, each one `<section class="sec" id="…">` with a single `<h2>`:

| File | id | h2 |
|---|---|---|
| `01-claim.html` | `sec-01-claim` | The claim |
| `02-position.html` | `sec-02-position` | Where the decision sits |
| `03-model.html` | `sec-03-model` | The model |
| `04-two-returns.html` | `sec-04-two-returns` | Two returns to information |
| `05-results.html` | `sec-05-results` | Competition creates competition |
| `06-robustness.html` | `sec-06-robustness` | What survives |
| `07-welfare.html` | `sec-07-welfare` | Welfare and sale terms |
| `08-statics.html` | `sec-08-statics` | Comparative statics at a glance |
| `09-outlook.html` | `sec-09-outlook` | Conclusion and next steps |
| `appendix.html` | `sec-appendix` | Appendix propositions |

Rules inside fragments:

- Headings (`h2`, `h3`) are plain text, no math, no placeholders. Every `h3` needs a unique `id`
  (prefix it with the section id, e.g. `sec-05-results-prop2`). The TOC is generated from
  `h2[id]` and `h3[id]`.
- Math: `\( … \)` inline and `\[ … \]` display. Display math sits in
  `<div class="math-block">\[ … \]</div>`. Never use `$`. Inside math write `\lt`, `\gt`, `\le`,
  `\ge` (a raw `<` followed by a letter opens an HTML tag). Use `&amp;` for the alignment
  ampersand in `aligned` environments. Equation tags: `\tag{4}` etc. to match the paper.
- Placeholders: `[[name]]` with a name from `numerics/quantity_registry.csv`. Outside math the
  build replaces it with
  `<span class="q" data-q="name" data-status="…" title="status · source_file · row">display</span>`.
  Inside math the build inserts the bare display text. Displays containing a backslash
  (`signal_trader_accuracy`, `signal_buyer_accuracy`, `cert_a_v_interval`, `cert_b_v_interval`,
  `cert_c_v_interval`) must be inside math; the build fails otherwise. Margin registry rows
  (`*_margin_*`) display as `1.366178511e+0` and belong in tables, not prose.
- Tables: `<!-- @@TABLE:name@@ -->` on its own line, where `name` is one of
  `auction_primitives`, `equilibrium_controls`, `welfare`, `extensions`, `reserve_comparisons`,
  `comparative_statics`, `thresholds`, `certificates`. The build replaces the comment with a
  `<div class="table-wrap">` containing a `<table>`; the fragment supplies the caption around it
  in a `<figure class="table"> … <figcaption>` wrapper.
- Charts: mount markup exactly
  `<figure class="chart" data-chart="fig2"><div class="chart-mount" id="chart-fig2" role="img" aria-label="…"></div><figcaption>…</figcaption></figure>`
  with ids `fig1`, `fig2`, `fig3`, `fig4`. The explorer mount is
  `<div id="explorer" data-explorer></div>` (explorer.js builds its own controls and its own
  chart mount `chart-explorer` inside it). Never place a chart or the explorer inside `<details>`.
  Each chart id appears exactly once across all fragments.
- Collapsibles: `<details class="proof"><summary>Proof sketch</summary> … </details>`. Other
  `details` use `class="fold"` with a descriptive summary.
- Timeline stepper (03-model): `<ol class="stepper" data-stepper>` with six
  `<li data-step><button type="button" class="step-btn">Short label</button><div class="step-note">Who knows what at this point.</div></li>`.
  app.js shows one note at a time, wires ArrowLeft/ArrowRight, and sets `aria-current`.
- Number strip (01-claim): `<div class="strip"><div class="stat"><span class="stat-value">[[base_entry_weak]]</span><span class="stat-label">entry, r = [[base_r_weak]]</span></div>…</div>`.
- Parameter card (03-model): `<dl class="params">` with `<dt>` / `<dd>` pairs using
  `[[base_h]]` etc.
- Proposition blocks: `<div class="prop" id="…"><p class="prop-title">Proposition 2 (competition creates competition).</p><div class="prop-body"> … </div></div>`. Conditions (A1) to (A3) are display math with `\tag{A1}`.
- Citations are plain text in the paper's style, e.g. `(Fishman 1988)`, `Boone and Mulherin (2007)`.
  Only references that appear in `references.bib` may be cited.
- No inline styles, no scripts, no external images. No `<h1>` (the template owns it).

## CSS contract (`style.css`)

Tokens on `:root[data-theme="light"]` and `:root[data-theme="dark"]` (theme boot always sets one):
`--bg --surface --surface-2 --ink --muted --grid --line --accent --accent-soft --c2 --c3
--region-a --region-b --region-c --font-sans --font-mono --measure`. Light accent `#5b3df5`,
dark accent `#a596ff`; `--c2` amber (`#c98a1b` light, `#e3b04b` dark); `--c3` slate
(`#5f6b7a` light, `#a1acbb` dark); regions are low-alpha tints (accent, amber, neutral).
Charts read these through `getComputedStyle(document.documentElement)`.

Layout: two-column grid `260px minmax(0,1fr)` at 1024px and up with a sticky `nav.toc`; below
1024px the TOC becomes a top `<details class="toc-drawer">` and the page is one column. Prose
measure `--measure: 68ch`. Charts and tables may extend to the full content column width.
Components to style: `.progress`, `header.masthead`, `.status-line`, `#theme-toggle`, `nav.toc`
(`a[aria-current="location"]` highlighted), `.sec`, `.math-block` (`overflow-x:auto`), `.q`
(subtle dotted underline, provenance tooltip via `title`), `.strip` and `.stat`, `dl.params`,
`.prop`, `details.proof` and `details.fold`, `.stepper`, `figure.chart` (reserve `min-height:
380px`, `520px` for `[data-chart="fig2"]`), `.chart-mount`, `.table-wrap` (`overflow-x:auto`),
`table` (compact, numerics right-aligned, sticky header), `.chip.pass` / `.chip.fail` / `.chip.na`,
`.live` (mono readouts), `.badge`, `.explorer` and its `input[type=range]`, `.colophon`,
`@media (prefers-reduced-motion: reduce)`. No print stylesheet.

## JS contract

Global namespace built by the three inline scripts, in load order app, charts, explorer:

```
window.CCC = {
  theme:    { get(), set(name), toggle() },                 // app.js; dispatches 'ccc:themechange' on document with detail {theme}
  charts:   { mount(id), mountAll(), rerender(), status() },// charts.js; status() -> {fig1:{mounted,traces},...}
  explorer: { init(), setR(r), reset(), selfTest(), status() }, // explorer.js
  ready:    Promise,                                         // app.js; resolves after math render and initial mounts
  selfCheck(): { charts, katexErrors, unresolvedPlaceholders, explorer, consoleErrors, details }
}
```

- Theme boot: `localStorage['ccc-theme']` or `?theme=light|dark`, else
  `matchMedia('(prefers-color-scheme: dark)')`; writes `data-theme` on `<html>`. The toggle
  persists the choice; the page follows system changes only when nothing is stored.
- `app.js` installs a `window.onerror` and `unhandledrejection` collector before anything else;
  `selfCheck().consoleErrors` returns the collected messages. Query params: `?eager=1` mounts all
  charts immediately and opens every `<details>`; `?debug=1` shows an error banner.
- `charts.js` registers builders `{fig1, fig2, fig3, fig4}`; `mount(id)` draws into
  `#chart-<id>` with `Plotly.newPlot(el, traces, layout, {displayModeBar:false, responsive:true})`;
  lazy mount through IntersectionObserver unless eager; `rerender()` calls `Plotly.react` with a
  layout rebuilt from the CSS tokens and `uirevision:'ccc'`; a ResizeObserver on each mount
  calls `Plotly.Plots.resize`. Below 640px container width, side-by-side panels stack.
  If `typeof Plotly === 'undefined'`, the mount shows a one-line notice and `status()` reports
  `mounted:false`.
- `explorer.js` owns everything inside `#explorer`, uses `CCC.charts` conventions for its own
  chart (`chart-explorer`, registered as builder `explorer` so `status()` includes it), listens to
  `ccc:themechange`, and logs `[ccc] self-test passed (N comparisons)` or
  `console.error('[ccc] self-test FAILED', diffs)` when `selfTest()` runs on init.
- Math render: `renderMathInElement(document.body, {delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}], throwOnError:false, ignoredTags:['script','noscript','style','textarea','pre','code']})`, then count `.katex-error`.

## `window.CCC_DATA` contract (emitted by `data.py`)

Keys sorted at every level. A CSV token that matches `^-?\d+(\.\d+)?([eE][-+]?\d+)?$` in a numeric
column is written verbatim as a JSON number literal; everything else is a JSON string. Python
never calls `float()` on a value that reaches the page. Certificate endpoints are always strings.

```
meta:      { plotly, katex, registry_hash, sources: {path: sha256} }
inputs:    { h, ell, p, rho, c_L, c_H, b, k, r_weak, r_strong, r_collapse }      // exact strings from registry base_* rows
registry:  { name: {display, value, lower, upper, units, status, exercise, parameter_set, branch, source_file, source_row, definition} }  // all strings
fig1:      { r:[560], Delta_T:[560], d_Delta_T_dr:[560],
             mu:["0.2689414213699951","0.5","0.7310585786300049"],
             mu_label:{"0.2689414213699951":"m","0.5":"1/2","0.7310585786300049":"M"},
             B:{mu:[560]}, dB:{mu:[560]} }
fig2:      { x_range:[1.0,3.8],
             branches:{ pooling|full_orders|asymmetric|symmetric_interior:
                        { r:[], E:[], O_H:[], q_H:[], q_L:[], v:[], tau:[], existence_status:[], uniqueness_status:[], multiplicity_found:[] } },  // accepted=="true", sorted by Decimal(r)
             certificates:[ { r, v_lower, v_upper, E_lower, E_upper, accepted (strings), v_mid, E_mid (numbers for plot position), v_halfwidth, E_halfwidth (strings, Decimal-computed) } x3 ],
             thresholds:{ pooling_unique_sufficient|pooling_existence|full_orders_unique_sufficient|high_cost_ceiling|m|M|laplace_entry_left_limit:
                          { value (number), value_str, lower, upper, interpretation } },
             regions:{ no_trade_unique:[1.0, r_k], full_orders_unique:[r_U, 3.8], multiplicity:[min, max of accepted r with multiplicity_found=="true"] } }
fig3:      { Laplace|logistic: { M_minus_tau:[], posterior_upper_tail_mass:[], E:[], x_star:[] } }   // tau_label=="grid", ascending x; index 0 is the zero-distance row
fig4:      { "1.2"|"3": { eta:[], Delta_eta:[], G_H_eta:[], G_L_eta:[] } }                          // eta != "1", ascending
tables:    { auction_primitives:[rows], equilibrium_controls:[rows], extensions:[rows], moderate_values:[rows],
             reserve_comparisons:[rows], feedback_comparisons:[rows], thresholds:[rows], certificates:[rows] }  // every cell a string
```

## Closed forms used by `explorer.js` and `crosscheck.py`

With `(h, ell, p, rho, c_L, c_H, b, k)` fixed at the benchmark strings parsed once to float64
and `r` from the slider:

```
t_0 = p (1 - p/r);  t_H = r/2 + p^2/(2r);  t_L = ell - (ell^2 - p^2)/(2r)
g_H = h - r/2 - p^2/(2r);  g_L = (ell^2 - p^2)/(2r);  Delta_T = (r - ell)^2/(2r)
m = 1/(1 + exp(2/b));  M = 1 - m;  B(mu) = g_L + mu (g_H - g_L)
tau = (c_H - g_L)/(g_H - g_L)
  if tau >= M:  E = rho, O_H = rho/2, x* = +inf, alpha_H = alpha_L = 0     (high-cost entry infeasible)
  if tau <= 1/2: entry at the prior; x* = -inf, alpha_H = alpha_L = 1        (outside (A2))
  else: x* = (b/2) log(tau/(1-tau)); alpha_H = 1 - exp((x*-1)/b)/2; alpha_L = exp(-(x*+1)/b)/2
        E = rho + (1-rho)/2 (alpha_H + alpha_L);  O_H = (rho + (1-rho) alpha_H)/2
Chips: (A1) c_L < B(m); (A2a) B(1/2) < c_H; (A2b) c_H < B(M);
       (A3 no trade) Delta_T < k;  (A3 full orders) (1 - 1/b) rho m Delta_T > k
Boundaries: rr(d) = ell + d + sqrt(d^2 + 2 ell d); r_k = rr(k); r_N = rr(2k/rho); r_U = rr(k/((1-1/b) rho m));
            r_C = (M h - c_H + sqrt((M h - c_H)^2 + M ((1-M) ell^2 - p^2))) / M
Domain guard: p < ell < r < h, else blank the readouts and say "outside the maintained ordering (1)".
```

Cross-check rows (tolerance 1e-9 absolute): `tables/auction_primitives.csv` parameter_set=base at
r = 1.2, 3, 3.6 (t_0, t_H, t_L, g_H, g_L, Delta_T, B_m, B_prior, B_M); `tables/equilibrium_controls.csv`
noise=Laplace, cost_law=atoms, experiment=feedback at r=3 and r=3.6 (E, O_H, tau, x_star with
`inf` meaning +Infinity) and experiment=frozen at r=1.2 (E, O_H, x_star); `tables/extensions.csv`
base/Laplace/atoms zeta_L = B_{r1}(m) - c_L, zeta_H0 = c_H - B_{r0}(1/2), zeta_H1 = B_{r1}(M) - c_H,
zeta_0 = k - Delta_T(r0), zeta_1 = (1-1/b) rho m Delta_T(r1) - k; `numerics/thresholds.csv`
the four boundaries plus m and M.

## Build checks (each prints `PASS`/`FAIL` like `numerics/verify.py`)

placeholders known, none open or unresolved, none left in output, TeX displays inside math;
every slot consumed, every table slot has a generator, chart ids each exactly once and each
figure slice nonempty; accepted correspondence rows partition into the four plotted branches;
certificates all accepted; thresholds present; fig3 one zero-distance row per noise; fig4 no
`eta == "1"`; two_returns `r`, `Delta_T`, `d_Delta_T_dr` identical across mu groups; data script
contains no `NaN`, `Infinity`, `</script`, `<!--`; details/section/figure/table tags balanced per
fragment; math delimiters balanced; ids unique; vendor tags carry integrity and crossorigin;
crosscheck passed; PDFs copied. Output has no timestamps, so rebuilds are byte-identical.

## Verify in a browser

```
python3 -m http.server 8765 --directory docs
open "http://localhost:8765/?eager=1&theme=light"
```
Then in the console: `await CCC.ready; JSON.stringify(CCC.selfCheck())`.
