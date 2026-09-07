# Professor handout

Edit `handout/`, then regenerate the HTML. Do not edit `docs/index.html` directly.
The default reading path is designed for 10–15 minutes; technical material stays in native
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

GitHub Pages serves the root of `gh-pages`. Build and check the source branch first, then
copy only `index.html`, `.nojekyll`, `main_filled.pdf`, `online_appendix_filled.pdf`, and the
`fonts/` directory from `docs/` into an isolated checkout of the current remote `gh-pages` commit.
Commit the generated files there and push normally, without force. Do not switch the source
checkout to the deployment branch or publish other files from `docs/`.

The deployment before this research-brief revision is
`07380e7fc95d9c385afdef69d932472d624d93b9`. To roll back, restore those four files from that
commit in a fresh deployment checkout and publish a new commit. This preserves history.
After publishing, check Pages build status and compare the live HTML and both PDF hashes
with the reviewed local artifacts.

The revision was checked at desktop and mobile sizes in both themes. The main reading path
is approximately 2,060 words, excluding expanded details. Prose, the benchmark table and
PDF links also remain available with JavaScript disabled or the CDN blocked.

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
