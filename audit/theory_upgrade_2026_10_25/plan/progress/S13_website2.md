# S13: the website ready to publish

Work of the production assistant (front end) on branch `theory-upgrade`, 26 October 2026, for the coordinator. The web slides match `slot/manuscript/slides.tex` under the deck contract. The retired words are gone from everything the site prints. Figure 4 draws Corollary 3 as the paper's research figure does. Every build and check passes, and the full site is staged in `../ccc-tu-scratch/site-stage2` without upload. Nothing is committed.

## Changes per file

**presentation/content.js (web slides).** The deck has 34 frames: 22 main and 12 backups, the same as `slides.tex`.
- **New frame F12b.** "In the example, coexistence runs from \(r_A\) to \(r_N\)", subtitle "Corollary 2: entry along the path of strengths". It is slide 16, carries target `main:coex` and the button "Marked strengths", and holds the entry chart with the N/R/F/Q/T key.
- **F12.** Now "Quiet and informative markets coexist". It has no target or link, and it draws the coexistence region in the plane of the spread and the threshold, with the example's path, beside the displayed conditions of Proposition 3.
- **F13.** It carries Proposition 4 at the prior \(\reg{prim_pi}\) and the Corollary 3 line with `res_rR`, `res_rC`, `res_rcap`, `res_entry_rR` and `res_entry_cap`.
- **Numbering and timing.** F13 to F17 are renumbered 17 to 21. F12 and F12b take 0.75 minutes each, so the main frames still sum to 30.25 minutes. A8's origin is F12b.

The other frames follow the TeX text:
- Q1 to Q3, F1 and F2 say "prepare" where they said "enter", and Q3 reads "In the example, entry rises".
- F3 and F5 say "in the example" and "the example's prior".
- F4 adds the default tie rules.
- F6 is titled "The example: …", has the inputs line, and its button reads "Recruitment region".
- F7 has the "Trading bound" column and "quiet market".
- F8 says "Preparation threshold", "top posterior" and "entry ceiling".
- F9 has the quiet market, "(H3) Exclusion condition", the takeover-share clause and the open-set line.
- F10 has the Corollary 1 title and subtitle and the band line (`u_lo_frac`, `u_hi_frac`, `u_B`).
- F11 has the new title, Proposition A.2, the "constant" directions and the fixed-information bullet.
- F14 to F16 use the appendix letters A.3 to A.13. F16 has the four rewritten predictions.
- F17 reads "in the example".
- A3 to A12 are aligned with the TeX: A5 "Recruitment and research regions in the example", A8 "Marked strengths of the coexistence region", A9 with Corollary 3 and `res_rN`, `res_rQ`, `res_rC`, A10 and A12 with the current letters, and A11 with \(\xi\).
- The notation table adds \(W_H(F)\) and the TeX meanings.

**Deck engine files outside the brief's named three, edited because the frames needed them:**
- `presentation/render.mjs` and `presentation/check_deck.mjs`. `\reg{key}` inside a formula is read like `{{key}}`. This is the only way the F13 subtitle can read as in `slides.tex` (`$\reg{prim_pi}$`) and still carry the key. In the check, only the stub's key regex changed (two lines). Every comparison is unchanged, and an unknown key still fails.
- `presentation/deck.js`.
  - New region chart `specRegion` and widget `region` for F12. It draws \(\tau\) from 0.45 to 0.765, as the paper's panel does. The region's closed edges are solid, and the open edge \(\tau=\pi\) is the dotted prior line.
  - The coexistence chart (F12b) adds the threshold pair T and reads "N: quiet market", "R: mixed purchase that recruits", "Q: mixed orders at the entry floor" and "quiet and informative coexist".
  - The research chart (F13) draws Corollary 3 over \([r_0,r_2]\): zero, recruiting and floor-entry research, open and filled markers as in the paper, and marks \(r_R, r_{\bar\lambda}, r_N, r_Q, r_C\).
  - The notes footer reads "in the example".
  - The F12b chart is 240 high, so that F12b does not overflow.
- `presentation/figdata.py`. Adds the region data, the T entry, floor-entry research \(\lambda_Q\) on \((r_N,r_Q)\), the cap segment to \(r_C\) and the floor cap on \((r_C,r_2]\). The bounds now include `res_rN`, `res_rQ` and `res_rC`, and `res_rUR` is dropped. At \(r_Q\) the curve ends at 0.234257, which is `res_lambda_floor_rQ`.
- `presentation/charts.js`. A trace with `fill: 'toself'` is drawn as a filled closed outline (one line). The region chart uses it.
- `presentation/deck.css`. Rules for the F12 layout, the F12b key line and a `ul.mid` list size for F16, which overflowed at the larger size.
- `presentation/build.py`. Adds the chart keys `res_rN`, `res_rQ`, `res_rC` and `res_lambda_floor_rQ` to the page data and drops `res_rUR`. The checkpoints read "else skip slides 15, 16 and 18; … else give slide 17 as one sentence and skip slide 19". The cumulative minutes at slides 12 and 14 are unchanged (20.25 and 23.5).
- `presentation/notes.md`. Adds a block for F12b and rewrites F12, F13, A5, A8 and A9 without typed numbers. It renumbers F14 to F17 and replaces "benchmark", "no trade" and "entrant". F9, F10, F11, F14, F16, A3, A6, A10, A11 and A12 follow the TeX. Three untouched blocks still type registry displays as decimals, each equal to its registry row: Q3 (0.522757), F3 (0.016667, 0.666667, 4.804167, 4.291667) and F10 (0.522757, 4.804167, 4.134722).
- `presentation/README.md`. Gives 21 numbered slides and 34 frames, says "in the example", and describes the F12, F12b and F13 charts.
- `presentation/DESIGN.md`. Gives 34 frames and 21 numbered frames, says "in the example" and "quiet market", lists the widgets `region` (F12), `coex` (F12b) and `research` (F13, Corollary 3), and documents `\reg{key}` inside a formula.

**Handout:**
- `handout/explorer.js`. The button "Quiet market" and "Mixed orders at the entry floor". The legend "N: quiet market", "Q: mixed orders at the entry floor" and "T: threshold pair (if an indifferent challenger may mix)". The title "Explore the example's path" and the matching aria-label. The Figure 3 caption reads "Entry along the example's path …", "N is the quiet market", "the thin dashed threshold pair T" and "belong to a curve". The header comments also say "example".
- `handout/figures.js`.
  - Figure 4 is rebuilt to Corollary 3 and `research.pdf`, panels (a) research and (b) entry over \([r_0,r_2]\):
    - zero research on \([r_0,r_N]\), with the filled marker at \(r_N\);
    - recruiting research, dashed \(\lambda_R\) on \([r_R,r_{\bar\lambda})\), then at the cap on \([r_{\bar\lambda},r_C]\), filled at \(r_C\);
    - floor-entry research \(\lambda_Q\) on \((r_N,r_Q)\), rising toward the open marker at `res_lambda_floor_rQ`, and at the cap on \((r_C,r_2]\);
    - the entry panel likewise: \(\rho\), the recruiting entry from `res_entry_rR` to `res_entry_cap`, and \(\rho\) for floor-entry research, with open markers at \(r_Q\) and \(r_C\);
    - black markers at \(r_0\), the three intermediate strengths (on both equilibria) and \(r_1, r_2\).
  - The marks \(r_R, r_{\bar\lambda}, r_N, r_Q, r_C\) and the cap label come from the registry keys `res_rR`, `res_rcap`, `rN`, `res_rQ`, `rC_B` and `res_cap`.
  - Adds `CCC.slot.lambdaQ`.
  - The hover names "spread in the example" and "thresholds in the example".
  - The header comment describes both research forms.
- `handout/slot_data.py`. The page data carries `rQ` (`res_rQ`), `lambda_floor_rQ` (`res_lambda_floor_rQ`) and `entry_cap` (`res_entry_cap`). Its comments say "example".
- `handout/sections/04-path.html`. The Figure 4 caption follows the paper's figure notes, with every value as a `[[key]]` row: `res_a`, `res_cap`, `res_rR`, `res_rcap`, `res_rC`, `res_entry_rR`, `res_entry_cap`, `res_rQ` and `res_lambda_floor_rQ`. The aria-label names the three equilibria.
- `handout/template.html`. The colophon reads "the closed forms of the paper at the example's primitives".
- `handout/README.md`. The brief's fourth section is "the path between the three economies (coexistence and research)", with "the four propositions and three corollaries of the main text (the corollaries state the example)". `figures.js` is described with the example's path, recruiting and floor-entry research, and Figure 4 per Corollary 3. Figure 3 is "entry along the example's path".

`handout/build.py` rewrote `docs/index.html`, `docs/paper.pdf`, `docs/comparison.pdf` and `numerics/manifests/handout.json`, and deleted `docs/main_filled.pdf` and `docs/online_appendix_filled.pdf` as before (see S13_website.md).

## Commands and output

- `python3 presentation/build.py`: exit 0. "Compared 34 frames (22 main, 12 backup) with slides.tex: order, titles, subtitles, targets and links; 158 printed registry keys found on the web frames; 39 notation symbols; 30.25 planned minutes before questions." "Deck matches slides.tex and the deck contract." "34 frames; 90 registry keys, 165 numbers printed."
- `node presentation/check_deck.mjs`: exit 0, the same two lines. It was run once more as the last command, after every edit and after staging, against `slides.tex` as it stood then.
- `python3 handout/build.py`: exit 0, 226 PASS, 0 FAIL, "registry keys used: 183", "HANDOUT BUILD PASSED".
- `python3 handout/check_display.py`: exit 0, with three PASS lines:
  - "the paper tab states 150 and 7 pages, both hashes and the text date 26 October 2026";
  - "180 number spans and 53 numbers in formulas print their slot registry display; no decimal is typed into the prose";
  - "only Fira Sans, Fira Mono and the symbol fallback; no network request".
- `python3 handout/publish.py --stage-only ../ccc-tu-scratch/site-stage2`: exit 0, 229 PASS, 0 FAIL, and "Staged 216 files: 54 at the root, 53 under /talk/, 54 under /laplace/ and 55 under /laplace/talk/". The staged `index.html` is byte-identical to `docs/index.html`. Nothing was uploaded.
- Search of the staged `index.html`, `talk/index.html` and `talk/provenance.json` (the `/laplace/` archive excluded):
  - "research branch", "no informed trade", "threshold branch" and "r̄": 0 hits each.
  - "benchmark": 3 hits, the element IDs `sec-setting-benchmark`, `sec-result-benchmark` and `benchmark-detail` in fragments outside this task. They are navigation hooks and do not print.
- Headless browser:
  - The handout self-report on the staged `index.html`, served locally, has four charts mounted (Figure 4 with 27 traces), 0 KaTeX errors, every placeholder filled, 0 console or page errors, and all 10 disclosures open.
  - The talk self-report on the staged `talk/index.html` has 34 slides, 0 errors and 0 mathematics errors. `DECK.audit()` returns `[]` there and on `presentation/dist/index.html`. Before the F12b and F16 sizes were fixed it listed F12b (70 px) and F16 (46 px).
- The `handout/check_browser.js` routine was not run. It expects the paper tab's earlier links (`main_filled.pdf`) and is written for an interactive browser session. The pages were inspected through screenshots instead.
- Print-only language scan (`--no-doc --no-figcode --extra`) on content.js, notes.md, 04-path.html, explorer.js, figures.js, both READMEs and template.html. The hits are code identifiers (key, registry, file names, `circle-open`, `update`, `new Error`), the allowed tie-rule phrases, and "no longer" as a comparison across strengths ("even above the entry ceiling, where they no longer predict entry"; "M no longer covers the high cost"). In the notes they are also "Now the challenger's side" (a talk transition) and "not only on the candidate" (A4, as in the TeX takeaway). In 04-path.html line 66, "interval of strengths" is the existing restatement of Proposition 4(d). No hit needed a change.

## Screenshots (in ../ccc-tu-scratch/web2/shots/)

The handout shots and the F12 shots are of the staged site. The other deck shots are of `presentation/dist/index.html` from the same build; the staged `talk/` differs from it only by the F12 chart edges and legend, which changed afterwards.

- `fig4.png`, `fig4_dark.png`, `fig4_narrow.png`: Figure 4 and its caption, in light, dark and 390 px.
- `explorer.png`: the explorer and Figure 3 with the quiet-market and threshold-pair legend.
- `deck_f12_light.png` / `_dark`: the coexistence region with the example's path through \(r_0, r_A, r_F, r_N\).
- `deck_f12b_light.png` / `_dark`: entry along the path, key line and Corollary 2 bullets.
- `deck_f13_light.png` / `_dark`: research and entry per Corollary 3, with the Corollary 3 line.
- `deck_f16_light.png` / `_dark`: empirical implications.
- `deck_a9_light.png` / `_dark`: research in detail.
