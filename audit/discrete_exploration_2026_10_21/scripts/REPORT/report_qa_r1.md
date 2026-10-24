# Report visual QA — round 1

Reviewed on 21 October 2026.
URL: http://127.0.0.1:8793/report.html.
Viewport widths: 728 px and 390 px. Height: 950 px.
The review covered the full page in light and dark at each width.

Light used the document's default palette.
Dark used native `prefers-color-scheme: dark` emulation.
The dark media query returned true.
The body background was `rgb(22, 22, 20)`.
The body text was `rgb(233, 231, 225)`.
No root-variable override or document rewrite was necessary.

## Problems, most severe first

Counts: **high 0; medium 0; low 3**.

1. **Low — the memo index breaks filenames into short fragments.**

   Section: `method`; the seventh table, which lists the memos.
   Width: 390 px; both themes.
   The same problem appears less severely at 728 px in both themes.

   The narrow index keeps three columns instead of the stacked rows used elsewhere.
   Memo names break across three or four lines.
   Some rows place the final “d” of “.md” on a separate line.
   Check filenames also break in the middle.
   The names remain present, but the fragments make them hard to identify.

   Suggested fix: give this table a dedicated class, such as `memo-index`.
   Set `.memo-index{min-width:720px}`.
   Set `.memo-index code{white-space:nowrap;overflow-wrap:normal}`.
   Keep `.tw{overflow-x:auto}` so this table scrolls inside its container.
   Alternatively, apply the existing stacked row style with explicit cell labels.

   Screenshots:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-page-38.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-page-39.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-page-38.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-page-39.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-page-21.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-page-21.png

2. **Low — chart subscripts fall below the requested text size.**

   Charts: `ch-post`, `ch-p2`, `ch-p3`.
   Widths: 728 px and 390 px; both themes.

   Main chart text is readable.
   Its measured size is about 11.4–11.7 CSS px at 728 px and 12.1 CSS px at 390 px.
   Subscripts use `font-size="0.75em"`, which reduces them to about 8.6–8.8 CSS px and 9.1 CSS px, respectively.
   This affects the “1” in the posterior labels and the letters in the cost and boundary labels.
   Those small letters need more effort to read at normal size.
   I saw no lost glyphs or overlap.

   Suggested fix: change the subscript span size in `txt()` from `0.75em` to `1em`.
   Retain the baseline offset.
   Reserve extra clearance below the labels if the larger spans approach a line or bar.

   Screenshots:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-ch-p2.png

3. **Low — the default favicon request produces one console error.**

   Section: document head; no section id.
   Widths and themes: the same session covered all four configurations.
   The request failed once on the first page load.

   The console reports HTTP 404 for `http://127.0.0.1:8793/favicon.ico`.
   The report body shows no visible failure.
   No other console errors or warnings appeared.

   Suggested fix: add `<link rel="icon" href="data:,">` to the head.
   This keeps the file self-contained and avoids a separate icon request.

   Screenshot, for page context only:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-page-01.png

   Console record:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-console.txt

## Layout, theme and resize observations

At 390 px, `document.documentElement.scrollWidth` equalled `clientWidth`: 375 px in both theme measurements.
The page had no horizontal overflow.
All seven table containers also had equal scroll and client widths.
Their `overflow-x` value was `auto`.
The first six tables changed to stacked rows.
The memo index stayed a three-column table, which caused problem 1.

At 728 px, the light measurement was 713 px for both document widths.
The dark measurement was 728 px for both document widths.
The scroll bar state changed the available content width; neither view overflowed.

All three charts changed layouts after a resize.
The wide viewBoxes were 720 × 360, 720 × 430 and 720 × 270.
The narrow viewBoxes were 460 × 402, 460 × 492 and 460 × 350.
The labels returned after the width changed back.
No duplicate labels or missing series appeared.
All chart text bounds stayed within the SVG bounds.

I clicked contents links and returned to the contents in each theme and at each width.
The visited links stayed blue in light and light blue in dark.
The computed palette colors were `rgb(47, 107, 216)` and `rgb(118, 170, 251)`.
Computed colors alone cannot prove the visited state; the screenshots provide the visual check.

The console contained one error, for the favicon, and zero warnings.
No chart or page-script error appeared during the theme and width changes.

## Screenshot inventory

Each combination has screenshots of all three charts and all seven tables.
The table numbers follow document order:

1. Noise laws, under `laws`.
2. Survival comparison, under `survive`.
3. Failed modifications, under `mods`.
4. Refuted claims, under `fell`.
5. Overclaimed claims, under `fell`.
6. Confirmed claims with corrections, under `fell`.
7. Memo index, under `method`.

The scroll frames show the page from top to bottom, with 100 px overlaps.
Each wide view has frames `page-01.png` through `page-22.png`.
Each narrow view has frames `page-01.png` through `page-39.png`.
Use the same directory and width/theme prefix as the individual screenshots below.
The scroll frames also preserve complete table context when an isolated table image includes adjacent text.

### Light, 728 px

- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-ch-p2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-ch-p3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-1.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-4.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-5.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-6.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-table-7.png

### Light, 390 px

- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-ch-p2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-ch-p3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-1.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-4.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-5.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-6.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-table-7.png

### Dark, 728 px

- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-ch-p2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-ch-p3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-1.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-4.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-5.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-6.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-table-7.png

### Dark, 390 px

- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-ch-p2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-ch-p3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-1.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-2.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-3.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-4.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-5.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-6.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-table-7.png

### Visited links

- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-728-links-visited-viewport.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-light-390-links-visited-viewport.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-728-links-visited.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r1-dark-390-links-visited.png

## Review scope and close

I listed the three existing tabs before I opened a separate review tab.
I used only the review tab and closed it at the end.
The three original tabs retain their original URLs.
I did not log in or save downloads.

The local server used port 8793, after a free-port check.
The server process, PID 3510909, no longer exists.
A connection to that port returned connection refused.
A new bind to port 8793 succeeded, which confirms that the server stopped.

The report's SHA-256 stayed unchanged:
`9232bb58c2067ad383e5a70151437e96bbde25144f365c3e2f59005d919dae40`.
Only this review record was added inside the repository.
No commit was made.
No tests were written or run.
This review concerns visual presentation; it does not establish the research claims.

## What looks correct

- No chart label overlaps another label, line, dot or bar.
- No chart label clips at an SVG edge.
- The page stays within the viewport at 390 px.
- Cards, section headings, stacked rows and captions remain aligned and readable.
- Text, chips, links, chart series and interval bars remain distinct in both themes.
- Visited links retain clear contrast.
- No names of internal products or automated participants appear in the visible report.

