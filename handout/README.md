# Website

Edit `handout/`, then regenerate the HTML. Do not edit `docs/index.html` directly.

The site presents the order-slot version of the paper (`slot/manuscript/`). The front page has three
tabs. The research brief is designed for 10 to 15 minutes of reading. "Read the paper" shows the
manuscript with its appendix and the note that compares the order slot with the Laplace order flow
of the earlier version. "Seminar talk" links the slides under `/talk/`. The earlier version stays
reachable through one link on the paper tab, "Earlier version: Laplace order flow", at `/laplace/`
(its front page and its two PDFs) and `/laplace/talk/` (its slides).

The brief has six sections: the setting, the mechanism, the main result and its controls, the
benchmark path (coexistence and research), robustness with welfare and sale terms, and the
empirical implications. Only their headings appear in the sidebar. The model, the mechanism, the
three propositions of the main text and the tests are visible; formal statements, derivations
and long tables stay in native `details` controls.

The design is the "UCL family" direction: a UCL dark-purple masthead with the tabs, a white body
with cards, pill controls and a dark theme. Purple is chrome only. Two concept colours hold on the
page and on the slides: `--c-info` for the target-payoff spread and the information chain,
`--c-cost` for preparation costs and the preparation threshold.

## Build and checks

```sh
python3 handout/build.py
python3 handout/check_display.py
```

The build uses Python's standard library and latexmk. It writes `docs/index.html`, `.nojekyll`,
`paper.pdf` and `comparison.pdf`, `docs/fonts/` and `docs/vendor/`, and refreshes
`numerics/manifests/handout.json` with the inputs, the output hash and every check. It exits
nonzero without replacing the page on failure. `--out DIRECTORY` changes the artifact destination;
the manifest still goes in the repository. `--verify-vendor` also fetches the upstream KaTeX files
and compares them with the lock.

The two PDFs are built from `slot/manuscript/main.tex` and `slot/manuscript/comparison.tex` with
`latexmk -pdf` and an output directory outside the repository (`--paper-cache`, by default
`ccc-slot-paper-build` in the system temporary directory). Nothing is written inside
`slot/manuscript/`. `SOURCE_DATE_EPOCH` is the date of the last commit that touched
`slot/manuscript/` (or the newest modification time of its changed files), so the PDFs, the
"Text revised" stamp and the paper tab are stable across rebuilds of an unchanged manuscript.

`check_display.py` checks the built page:

- the paper tab states the page counts, hashes and text date read from the two PDFs it ships;
- every number span prints the display of its slot registry row and carries its key and exact
  value; numbers inside formulas carry the same; no decimal is typed into the prose;
- only the locked faces load, and the page makes no network request.

`check_browser.js` is the browser check of the Laplace page of 2 October 2026. It still encodes
that page's expectations (five figures, legacy anchors, 47 slides), which `/laplace/` now serves;
it does not describe the current front page.

## Publishing

The public site is https://competition.dealextract.org/, hosted by Cloudflare Workers Static
Assets. The source repository is hosted on GitHub. No VM or Worker script is required.

```sh
# Once per machine: sign in to the Cloudflare account that owns dealextract.org.
npx --yes wrangler@4.130.0 login --scopes account:read user:read workers:write workers_scripts:write workers_routes:write zone:read ssl_certs:write
python3 handout/publish.py --stage-only /tmp/site-preview   # the staged tree, nothing uploaded
python3 handout/publish.py --dry-run
python3 handout/publish.py
```

Requires Python, latexmk, Node.js and npm. The publisher rebuilds the page, runs
`check_display.py`, rebuilds the talk (`presentation/build.py` and
`presentation/check_deck.mjs`), builds the Laplace archive, and stages an explicit file list:

- at the root: `index.html`, `paper.pdf`, `comparison.pdf`, the locked fonts and licences
  (`fonts.lock.json`) and the KaTeX files (`vendor.lock.json`);
- under `talk/`: the slides, `provenance.json`, the same fonts and KaTeX files, and
  `presentation.pdf` when it has been exported;
- under `laplace/`: the committed handout build of the pinned commit (`LAPLACE_COMMIT` in
  `publish.py`, the last commit of the Laplace website sources, on the main and laplace branches):
  its `index.html` with one added line that names it the earlier version and links the current
  one, `main_filled.pdf`, `online_appendix_filled.pdf`, and its fonts and KaTeX files;
- under `laplace/talk/`: the Laplace slides, built by the pinned commit's own
  `presentation/build.py` in an extracted copy (cached by commit in the system temporary
  directory), with their two PDFs, provenance record, fonts and KaTeX files.

Speaker notes in Markdown and QA output are never staged. A failed check stops publication.
Wrangler is version-pinned; credentials stay in its machine-local login store, never in this
repository. Publishing is explicit; pushing research changes to GitHub does not update the website.

After publishing, compare the live HTML and PDF hashes with the staged tree. In Cloudflare's
Workers dashboard, select `competition-creates-competition` > Deployments to inspect or roll back
a deployment. The custom domain and disabled alternate URLs are declared in `wrangler.jsonc`.

The migration on 2026-09-10 deployed version `8c42fb77-3ffa-4e21-9fd0-9cc9392282f2`. The first
deployment with the talk under `/talk/`, on 2026-09-14, is version
`94018472-5374-4d16-87bf-73a2dd78d858`. The redesigned handout and talk of 2 October 2026 went
live on 2026-10-03 as version `ca5d847f-6e9f-4221-afc0-605587396ab5`; the ruled layout of the same
day is version `9c52f0de-7531-44d1-a5b2-747292f63875`. The version live before the order-slot
switch, of 21 October 2026, is `1f99d35e-2061-4e33-a38b-8cf9e8902c09`; its page used a different
type design (Archivo and STIX Two Text) that no committed source records, with the same text as
the committed Laplace page to within small edits.

The retired publishing procedure is preserved in
[`audit/peer_polish/retired_pages_deployment.md`](../audit/peer_polish/retired_pages_deployment.md)
as a historical record only.

## Content and data boundaries

- Each `sections/*.html` fragment has one `section.sec`, one `h2`, and unique IDs on `h3`. The
  template owns the masthead, the tabs, the opening question, the theme control, the paper and
  talk tabs, and the colophon.
- Numbers use `[[key]]`, where `key` is a row of the slot registry
  `audit/slot_manuscript_2026_10_23/registry/registry.csv` (columns key, value, display, status,
  source_script, run_log, note). The manuscript prints the same rows through `\reg{key}`. The page
  prints the row's `display` exactly; outside mathematics `\%` becomes `%`. Do not type a research
  value into prose. Each span carries `data-q` and `data-value`, and its tooltip gives the display,
  the key and the source script. No result-status word is printed.
- Inside math a placeholder becomes the bare display, and the builder wraps the whole math
  segment in `span.q-math` with the keys and displays, so the binding survives KaTeX.
- Math uses `\( ... \)` and `\[ ... \]`, with display math in `.math-block`. Use `\lt` and `\gt`
  instead of raw angle brackets. No dollar delimiters or inline styles or scripts. KaTeX rejects
  `array{c@{\qquad}c}`; use `{ccc}` with `\qquad` in cells. Keep display formulas narrow enough
  for a phone (split them with `gathered`).
- `slot_data.py` reads the registry and emits `window.CCC_DATA`: the declared primitives, the slot
  (`lambda_B`, `b_B`, `b0_B`, `M_half_B`, `m_half_B`), the marked strengths (`rA`, `rF_B`, `rN`,
  `rJ`, `rS_B`, `rC_B`, `res_rR`, `res_rcap`, `res_rUR`), the points that the figures label, and
  the registry hash.
- Typefaces are Fira Sans and Fira Mono (SIL OFL, fontsource subsets) and a symbol fallback,
  "CCC Symbols", a byte copy of KaTeX_Main-Regular for the arrows and relations that the Fira
  subsets omit. All are pinned by sha256 in `fonts.lock.json` with their licences. The build
  generates the font-face rules from the lock and fails if a file is missing, altered or unlocked,
  or if `style.css` declares a font itself.
- KaTeX 0.18.5 is a local copy under `handout/vendor/`, pinned by sha256 and by the upstream
  sha512 integrity in `vendor.lock.json`. The slides use the same copy.

## Figures and interaction

`charts.js` is the SVG renderer shared with the slides: a spec of traces and layout becomes SVG
with a legend of toggle buttons, a hover readout and a keyboard cursor. The slides call
`CCC.charts.tokens()` and `CCC.charts.draw()`. It still carries the builders of the Laplace
figures, which the deck used; `figures.js` removes them from this page's registry of figures.

`figures.js` holds `CCC.slot`, the closed forms of the manuscript at the registry declarations:
the benchmark auction payoffs, the order laws, posteriors, entry and prices of each equilibrium
form on the benchmark path (Appendix A4), and the research branch (Section 5). It draws
Figure 1 (the two returns), Figure 2 (beliefs and the entry ceiling) and Figure 4 (research).
`explorer.js` is the explorer of Section 4: a slider on incumbent strength, the equilibria that
Appendix A4 lists at that strength, the posterior after each order against the threshold, the
order table, and Figure 3 (entry along the benchmark path, every form). Marked strengths and
labelled points are registry rows; the curves and the readouts evaluate the closed forms. Nothing
on the page searches for an equilibrium.

Each figure has exactly one `#chart-<id>.chart-mount` with an accessible description and a
caption; the explorer has one `#explorer[data-explorer]` mount and draws Figure 3 itself. Charts
inside closed disclosures wait until opened. Theme changes and resizes redraw. Panels stack below
640 pixels of chart width. The six-stage timeline supports arrow keys; disclosures, tabs (arrow
keys), the theme toggle and the explorer controls support the keyboard. Hash navigation selects
the brief tab and opens enclosing disclosures; `#tab-paper` and `#tab-talk` select those tabs.

For browser QA, `CCC.ready` resolves after initial rendering and `CCC.selfCheck()` reports chart
status, math errors, unresolved placeholders, the explorer state, the tab, the loaded faces and
script errors. `?eager=1` opens all disclosures; `?lazy=1` mounts charts as they near the
viewport. The page sets `scroll-behavior: smooth`, so automation scrolls with
`behavior: 'instant'`; a hidden browser tab runs no animation frames.
