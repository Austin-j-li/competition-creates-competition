# Professor handout

Edit `handout/`, then regenerate the HTML. Do not edit `docs/index.html` directly.
The default reading path is designed for 10–15 minutes. The model, incentive comparison,
price-inference argument, and theorem conditions are visible; derivations stay in native
`details` controls. The four sections are the takeover setting, the mechanism, the evidence,
and implications. Only their headings appear in the sidebar.
The research-brief layout uses a short opening question, two mechanism paths, and a visible
benchmark comparison. The prose assumes a research reader who is new to this model.
Retired public section and table anchors remain as spans near their replacement content.

## Build and checks

```sh
python3 handout/build.py
python3 handout/check_display.py
```

For browser checks, serve `docs/` with `python -m http.server 8765 --bind 127.0.0.1 --directory docs`.
Run `handout/check_browser.js` using the existing Playwright MCP tool
`browser_run_code_unsafe` with its absolute path as `filename`. It checks desktop/mobile,
both themes, all five plots, mathematics, legacy anchors, the slider, timeline, and keyboard
navigation. No browser package is added to this repository.

The build uses only Python's standard library. The focused display check also uses Node's
standard library. No package installation or bundler is needed. The build writes
`docs/index.html`, `.nojekyll`, the two linked PDFs, `docs/fonts/`, and
`numerics/manifests/handout.json`. It exits nonzero without replacing the handout on failure.
`--out DIRECTORY` changes the artifact destination; the manifest still goes in the repository.
`--verify-vendor` also verifies the pinned CDN files in `vendor.lock.json`.

The research gate is `.venv/bin/python numerics/verify.py --final`. It rebuilds the registry
and filled manuscripts, so use an isolated copy when checking a presentation-only change.
The handout builder does not alter research sources or run numerical searches.

## Publishing

The public handout is https://competition.dealextract.org/ and the interactive talk is
https://competition.dealextract.org/talk/, both hosted by Cloudflare Workers Static Assets. The source repository is hosted on GitLab. No VM or Worker script is required.

```sh
# Once per machine: sign in to the Cloudflare account that owns dealextract.org.
npx --yes wrangler@4.130.0 login --scopes account:read user:read workers:write workers_scripts:write workers_routes:write zone:read ssl_certs:write
python3 handout/publish.py --dry-run
python3 handout/publish.py
```

Requires Python, Node.js and npm. The publisher rebuilds the handout, runs
`check_display.py`, rebuilds the talk (`presentation/build.py`, `presentation/check_deck.mjs`),
and stages an explicit file list in a temporary directory: the handout HTML, both PDFs and
the five locked font files at the root, and under `talk/` the deck, its locked fonts and
KaTeX assets, the two PDFs, `provenance.json`, and `presentation.pdf` when it has been
exported. Speaker notes and QA output are never staged. A failed check stops publication. Wrangler is version-pinned;
credentials stay in its machine-local login store, never in this repository.
The builder refreshes `numerics/manifests/handout.json` with the local build environment.
Publishing is explicit; pushing research changes to GitLab does not update the website.

Run `handout/check_browser.js` against the deployed address after publishing and compare
the live HTML and PDF hashes with `docs/`. In Cloudflare's Workers dashboard, select
`competition-creates-competition` > Deployments to inspect or roll back a deployment.
The custom domain and disabled alternate URLs are declared in `wrangler.jsonc`.

The migration on 2026-09-10 deployed version `8c42fb77-3ffa-4e21-9fd0-9cc9392282f2`.
The first deployment with the talk under `/talk/`, on 2026-09-14, is version
`94018472-5374-4d16-87bf-73a2dd78d858`.
Live HTML, both PDFs and all five fonts matched the local files byte for byte. Browser
checks passed at 1440, 390 and 320 pixels in both themes, including all five plots,
mathematics, keyboard controls and legacy anchors. Unpublished source paths returned 404.
This verified the hosting migration; it did not rerun the research acceptance gate.

The browser check accepts an optional second argument for its base URL. To check production,
load the file's function and invoke it as `check(page, 'https://competition.dealextract.org/')`
through the existing Playwright tool. The default still checks the local server.

The retired publishing procedure is preserved in
[`audit/peer_polish/retired_pages_deployment.md`](../audit/peer_polish/retired_pages_deployment.md)
as a historical record only.

## Content and data boundaries

- Each `sections/*.html` fragment has one `section.sec`, one `h2`, and unique IDs on `h3`.
  The template owns the large title, theme control, PDF links, navigation, and colophon.
- Scalars use `[[registry_name]]`. Outside math, `[[registry_name:percent]]` displays a
  probability as a percentage rounded to one decimal; its tooltip retains the exact source
  value. Other scalars use the release registry's display field. Do not type research values
  into prose.
- Math uses `\( ... \)` and `\[ ... \]`, with display math in `.math-block`. Use `\lt` and
  `\gt` instead of raw angle brackets. No dollar delimiters or inline styles/scripts.
- Table slots are `<!-- @@TABLE:name@@ -->`. `tables_html.py` selects validated CSV rows,
  uses Decimal for formatting, and retains raw values and row locations in cell attributes.
  The core comparison uses `core_comparison`; larger exhibits remain expandable.
- `data.py` binds every input CSV to a passed numerical manifest before emitting
  `window.CCC_DATA`. Numeric tokens are emitted verbatim, with Decimal used for sorting.
  Source hashes and library provenance are available in the footer disclosure.
- PDF links point to `main_filled.pdf` and `online_appendix_filled.pdf` beside the HTML.
  These are byte-identical to the returned peer-circulation PDFs. Keep the three files
  together for review. The existing pinned Plotly and KaTeX assets load from their CDN.
- Typefaces are self-hosted latin subsets (Literata, Libre Franklin, Courier Prime; all SIL OFL)
  under `handout/fonts/`, pinned by sha256 in `fonts.lock.json` and copied to `docs/fonts/`.
  The build fails if a file is missing, altered, unlocked, or not referenced by `style.css`.

## Figures and interaction

`charts.js` builds Figures 1–4 from `CCC_DATA`. Each figure has exactly one
`#chart-figN.chart-mount`, with an accessible description and a caption. The explorer has
one `#explorer[data-explorer]` mount and creates its own chart and controls.

Charts inside closed disclosures wait until opened; a capturing `toggle` listener mounts
and resizes them. Theme changes rebuild visible plots from CSS colors. Panels stack below
640px chart width. The six-stage timeline supports arrow keys; disclosures, theme toggle,
and explorer controls support the keyboard. Hash navigation opens enclosing disclosures.

Scientific display rules:

- Accepted correspondence rows retain evidence status and complete continuation identity.
  The mixed diagnostic and its support weights are displayed; unresolved searches do not
  mean nonexistence. Multiplicity ticks mark individual searched nodes. Only analytical
  uniqueness regions receive continuous shading. Missing nodes and ambiguous roots break
  connecting lines; certificate intervals retain their outward endpoints.
- At the high-cost ceiling, equality includes the posterior plateau. The lower marker is
  an open right-hand limit. The logistic upper bound is unattained, but the tail probability
  at that bound is defined as zero, so its marker is closed.
- Bargaining at seller weight one remains on the linear spread panel; zero profits are
  excluded only from the logarithmic panel.
- The reserve table joins complete continuation identifiers to validated sale-event rows.
  Preparation, sale, and two admissible bidders are distinct outcomes.

`crosscheck.py` and `explorer.js` share the same closed forms. The explorer is a fixed-order
calculation, not an equilibrium solver. Its runtime self-test compares 49 values to the CSVs.
`check_display.py` protects source binding, continuation deduplication, finite table values,
chart gaps, multiplicity ticks, endpoint conventions, preparation ties, and PDF bytes.

For browser QA, `CCC.ready` resolves after initial rendering and `CCC.selfCheck()` reports
chart status, math errors, unresolved placeholders, explorer comparisons and script errors.
Closed charts should report `reason: 'collapsed'` until expanded. Inspect desktop and mobile
in both themes, open all figure disclosures, exercise keyboard controls, and follow both PDF
links. `?eager=1` opens all disclosures for inspection; `?lazy=1` enables viewport lazy mounting.
