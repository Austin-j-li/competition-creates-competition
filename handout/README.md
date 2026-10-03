# Professor handout

Edit `handout/`, then regenerate the HTML. Do not edit `docs/index.html` directly.
The page has three tabs. The research brief is designed for 10–15 minutes of reading.
"Read the paper" shows the two PDFs. "Seminar talk" links the slides under `/talk/`.
The brief has four sections: the takeover setting, the mechanism, the evidence, and
implications. Only their headings appear in the sidebar. The model, the incentive comparison,
the price-inference argument and the theorem conditions are visible; derivations stay in
native `details` controls. Retired public section and table anchors remain as spans near their
replacement content.

The design is the "UCL family" direction: a UCL dark-purple masthead with the tabs, a white
body with cards, pill controls and a dark theme. Purple is chrome only. Two concept colours
hold on the page and on the slides: `--c-info` for the target-payoff spread and the
information chain, `--c-cost` for preparation costs.

## Build and checks

```sh
python3 handout/build.py
python3 handout/check_display.py
```

The build uses only Python's standard library. The display check also uses Node's standard
library. No package installation or bundler is needed. The build writes `docs/index.html`,
`.nojekyll`, the two linked PDFs, `docs/fonts/` and `docs/vendor/`, and refreshes
`numerics/manifests/handout.json`. It exits nonzero without replacing the handout on failure.
`--out DIRECTORY` changes the artifact destination; the manifest still goes in the repository.
`--verify-vendor` also fetches the upstream KaTeX files and compares them with the lock.

`check_display.py` checks the built page and the chart code:

- source manifest binding, continuation deduplication and finite table values;
- the two PDFs are the peer-circulation bytes (sha256 in the script), and the paper tab states
  the page counts and the text date that the build reads from the files;
- every number span equals the registry value under the display rule and carries its key,
  status, precision and exact value; numbers inside formulas carry the same; no decimal is
  typed into the prose;
- status words come from the paper's vocabulary (analytical, computer-assisted, numerical
  diagnostic, open, input), in spans and in the evidence columns of the tables;
- every legacy anchor and every public id of the 2 October 2026 page is present;
- only the locked faces load, and the page makes no network request;
- the chart builders and the SVG renderer keep the display rules below, and neither changes
  the release data.

For the browser check, serve `docs/` with
`python3 -m http.server 8765 --bind 127.0.0.1 --directory docs`. Run `handout/check_browser.js`
with the existing Playwright browser tool's run-code function and the file's absolute path as
`filename`. It checks 1440, 390 and 320 pixels in both themes: the five figures, mathematics,
Fira Sans, the explorer slider, the hover readout, the theme toggle, the three tabs and the
inline viewer, legacy anchors, the timeline, the mobile contents drawer, the skip link and a
malformed fragment. With a second and third argument (the handout and the slides addresses)
it also checks the slides: 47 slides, no overflow, a backup link, Back and End. The tab must be
in front: a hidden tab runs no animation frames. No browser package is added to this
repository.

The research gate is `.venv/bin/python numerics/verify.py --final`. It rebuilds the registry
and filled manuscripts, so use an isolated copy when checking a presentation-only change.
The handout builder does not alter research sources or run numerical searches.

## Publishing

The public handout is https://competition.dealextract.org/ and the interactive talk is
https://competition.dealextract.org/talk/, both hosted by Cloudflare Workers Static Assets.
The source repository is hosted on GitHub. No VM or Worker script is required.

```sh
# Once per machine: sign in to the Cloudflare account that owns dealextract.org.
npx --yes wrangler@4.130.0 login --scopes account:read user:read workers:write workers_scripts:write workers_routes:write zone:read ssl_certs:write
python3 handout/publish.py --dry-run
python3 handout/publish.py
```

Requires Python, Node.js and npm. The publisher rebuilds the handout, runs
`check_display.py`, rebuilds the talk (`presentation/build.py`, which also runs
`presentation/check_deck.mjs`), and stages an explicit file list in a temporary directory: the
handout HTML, both PDFs, the locked fonts and licences (`fonts.lock.json`) and the KaTeX files
(`vendor.lock.json`) at the root; under `talk/` the slides, the same fonts and KaTeX files, the
two PDFs, `provenance.json`, and `presentation.pdf` when it has been exported. Speaker notes in
Markdown and QA output are never staged. A failed check stops publication. Wrangler is
version-pinned; credentials stay in its machine-local login store, never in this repository.
The builder refreshes `numerics/manifests/handout.json` with the local build environment.
Publishing is explicit; pushing research changes to GitHub does not update the website.

Run `handout/check_browser.js` against the deployed address after publishing and compare
the live HTML and PDF hashes with `docs/`. In Cloudflare's Workers dashboard, select
`competition-creates-competition` > Deployments to inspect or roll back a deployment.
The custom domain and disabled alternate URLs are declared in `wrangler.jsonc`.

The migration on 2026-09-10 deployed version `8c42fb77-3ffa-4e21-9fd0-9cc9392282f2`.
The first deployment with the talk under `/talk/`, on 2026-09-14, is version
`94018472-5374-4d16-87bf-73a2dd78d858`. Those records describe the earlier design.
The redesigned handout and talk of 2 October 2026 went live on 2026-10-03 as version
`ca5d847f-6e9f-4221-afc0-605587396ab5`.

The browser check accepts its base URL as the second argument. To check production, load the
file's function and invoke it as `check(page, 'https://competition.dealextract.org/',
'https://competition.dealextract.org/talk/')` through the existing Playwright tool.

The retired publishing procedure is preserved in
[`audit/peer_polish/retired_pages_deployment.md`](../audit/peer_polish/retired_pages_deployment.md)
as a historical record only.

## Content and data boundaries

- Each `sections/*.html` fragment has one `section.sec`, one `h2`, and unique IDs on `h3`.
  The template owns the masthead, the tabs, the opening question, the theme control, the
  paper and talk tabs, and the colophon.
- Scalars use `[[registry_name]]`. Do not type research values into prose. The builder derives
  each display from the registry value: a declaration (status `input`) keeps its declared
  display; a result shows three decimals, or three significant digits when a nonzero magnitude
  is below 0.01 (`tables_html.three_decimals`). Percent forms are not used for results. Each
  span carries `data-q`, `data-status`, `data-precision` and `data-value`; its tooltip keeps the
  registry display, status and source.
- Inside math a placeholder becomes the bare display, and the builder wraps the whole math
  segment in `span.q-math` with the keys, displays and statuses, so provenance survives KaTeX.
- Math uses `\( ... \)` and `\[ ... \]`, with display math in `.math-block`. Use `\lt` and
  `\gt` instead of raw angle brackets. No dollar delimiters or inline styles or scripts.
- Table slots are `<!-- @@TABLE:name@@ -->`. `tables_html.py` selects validated CSV rows,
  uses Decimal for formatting, and keeps raw values and row locations in cell attributes.
  The core comparison shows three decimals and an Evidence column. The controls table prints
  the evidence class; "(control)" is a role and sits in the row label.
- `data.py` binds every input CSV to a passed numerical manifest before emitting
  `window.CCC_DATA`. Numeric tokens are emitted verbatim, with Decimal used for sorting.
  Source hashes are available in the footer disclosure.
- PDF links point to `main_filled.pdf` and `online_appendix_filled.pdf` beside the HTML.
  These are byte-identical to the returned peer-circulation PDFs (`peer_release/`). The build
  reads their page counts, sizes, sha256 and creation date with the standard library and writes
  the paper tab and the "Text revised" stamp from them. No date or count is typed by hand.
- Typefaces are Fira Sans and Fira Mono (SIL OFL, fontsource subsets) and a symbol fallback,
  "CCC Symbols", a byte copy of KaTeX_Main-Regular for the arrows and relations that the Fira
  subsets omit. All are pinned by sha256 in `fonts.lock.json` with their licences. The build
  generates the font-face rules from the lock and fails if a file is missing, altered or
  unlocked, or if `style.css` declares a font itself.
- KaTeX 0.18.5 is a local copy under `handout/vendor/`, pinned by sha256 and by the upstream
  sha512 integrity in `vendor.lock.json`. The slides use the same copy.

## Figures and interaction

`charts.js` has two layers. The builders (`fig1` to `fig4`) read `CCC_DATA` and the CSS tokens
and return a plain spec: traces with null at every break, marker symbols, interval bars, shapes
and annotations. The renderer turns a spec into SVG with a legend of toggle buttons, a hover
readout and a keyboard cursor (left and right arrow keys on a focused figure). `svgMarkup` is
the pure part that the display check calls. The slides draw their figures with the same code.

Each figure has exactly one `#chart-figN.chart-mount`, with an accessible description and a
caption. The explorer has one `#explorer[data-explorer]` mount and draws its own chart. Charts
inside closed disclosures wait until opened; a capturing `toggle` listener mounts them. Theme
changes and resizes redraw. Panels stack below 640 pixels of chart width. The six-stage timeline
supports arrow keys; disclosures, tabs (arrow keys), the theme toggle and the explorer controls
support the keyboard. Hash navigation selects the brief tab and opens enclosing disclosures;
`#tab-paper` and `#tab-talk` select those tabs.

Scientific display rules:

- Accepted correspondence rows keep evidence status and complete continuation identity.
  The mixed diagnostic and its support weights are displayed; unresolved searches do not
  mean nonexistence. Multiplicity ticks mark individual searched nodes. Only analytical
  uniqueness regions receive shading. Missing nodes and ambiguous roots break connecting
  lines; certificate intervals keep their outward endpoints.
- At the high-cost ceiling, equality includes the posterior plateau. The lower marker is
  an open right-hand limit. The logistic upper bound is unattained, but the tail probability
  at that bound is defined as zero, so its marker is closed.
- Bargaining at seller weight one stays on the linear spread panel; zero profits are
  excluded only from the logarithmic panel.
- The reserve table joins complete continuation identifiers to validated sale-event rows.
  Preparation, sale, and two admissible bidders are distinct outcomes.

`crosscheck.py` and `explorer.js` share the same closed forms. The explorer is a fixed-order
calculation, not an equilibrium solver. Its runtime self-test compares 49 values to the CSVs.

For browser QA, `CCC.ready` resolves after initial rendering and `CCC.selfCheck()` reports
chart status, math errors, unresolved placeholders, explorer comparisons, the tab, the loaded
faces and script errors. Closed charts report `reason: 'collapsed'` until expanded. `?eager=1`
opens all disclosures for inspection; `?lazy=1` mounts charts as they near the viewport.
