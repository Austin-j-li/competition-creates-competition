# Report visual QA — round 2

Reviewed on 21 October 2026.
URL: http://127.0.0.1:50461/report.html.
Viewport widths: 728 px and 390 px. Height: 950 px.
The review covered all three charts, the memo index, the revised sentence, horizontal overflow and the console in both themes.
The first-round record was read before this review.

Light used the document's default palette.
Dark used native `prefers-color-scheme: dark` emulation, as in round 1.
The dark media query returned true at both widths.
The body background was `rgb(22, 22, 20)`.
The body text was `rgb(233, 231, 225)`.
No root-variable override or document rewrite was necessary.

## Status of the round-1 problems

All three low problems are **fixed** under the stated acceptance criteria.

1. **Fixed — R1-1, fragmented filenames in the memo index.**

   Section: `method`; the last table.
   Widths: 728 px and 390 px; both themes.

   The table has classes `stack sm memo-index`.
   At 390 px, each row forms a separate block with the labels “Topic” and “Checked by”.
   All 27 filename elements stay on one line.
   Their computed `white-space` is `nowrap`.
   At 728 px, the three columns remain readable, and the filenames stay intact.
   No filename clips or spills outside a row.

   Screenshots:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-728-memo-index.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-728-memo-index.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-memo-viewport-1.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-memo-viewport-2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-memo-viewport-3.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-memo-viewport-4.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-memo-viewport-1.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-memo-viewport-2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-memo-viewport-3.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-memo-viewport-4.png

2. **Fixed — R1-2, chart subscripts below the minimum text size.**

   Charts: `ch-post`, `ch-p2`, `ch-p3`.
   Widths: 728 px and 390 px; both themes.

   All 12 subscript spans use `font-size="0.9em"`.
   The table below gives effective sizes after the SVG scale, with the vertical scroll bar visible.
   Each value applies to every subscript in that chart.

   | Chart | 728 px, light | 728 px, dark | 390 px, light | 390 px, dark |
   | --- | ---: | ---: | ---: | ---: |
   | `ch-post` | 10.275 CSS px | 10.275 CSS px | 10.862 CSS px | 10.862 CSS px |
   | `ch-p2` | 10.275 CSS px | 10.275 CSS px | 10.862 CSS px | 10.862 CSS px |
   | `ch-p3` | 10.275 CSS px | 10.275 CSS px | 10.862 CSS px | 10.862 CSS px |

   The computed sizes before the SVG scale are 10.8 px at 728 px and 14.4 px at 390 px.
   Effective sizes use the computed font size multiplied by the screen transform scale.
   When the document's client width was 390 px, the effective size was 11.332 CSS px.
   The smaller, scroll-bar-visible measurement still exceeds 10 CSS px.
   No larger subscript touches a line, dot, bar or another label.
   No chart text clips at an SVG edge.

   Screenshots:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-728-ch-post.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-728-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-728-ch-p3.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-ch-post.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-ch-p3.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-728-ch-post.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-728-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-728-ch-p3.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-ch-post.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-ch-p2.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-ch-p3.png

3. **Fixed — R1-3, the default favicon request caused a console error.**

   Location: document head.
   Widths: 728 px and 390 px; both themes in the same review session.

   The favicon link resolves to `data:,`.
   The report request returned HTTP 200.
   No request for `/favicon.ico` appeared.
   The console contained zero errors and zero warnings after all four configurations.
   The screenshots below give page context; the request and console observations establish this fix.

   Screenshots:

   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-728-top.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-top.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-728-top.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-top.png

## New problems, most severe first

Counts: **high 0; medium 0; low 0**.
No new visual problem appeared within this review's scope.
No corrective change is necessary.

## Layout, theme and resize observations

At 390 px, the final document measurements were `clientWidth = scrollWidth = 375 px` in both themes.
Each of the seven table containers had `clientWidth = scrollWidth = 347 px`.
There was no horizontal overflow.
An earlier measurement without the scroll bar gave equal document widths of 390 px and equal table widths of 362 px.

At 728 px, the final document measurements were `clientWidth = scrollWidth = 713 px` in both themes.
Each table container had equal widths of 685 px.
The charts changed layouts after each width change.
Their wide viewBoxes were 720 × 360, 720 × 430 and 720 × 270.
Their narrow viewBoxes were 460 × 402, 460 × 492 and 460 × 350.

The revised sentence in `fell` fits at both widths in both themes.
The paragraph below the refuted claims remains separate from the table and the next subsection.
It distinguishes the first five claims from the last two general statements.
The review checked its visual presentation, without a new audit of the research claims.

Screenshots:

- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-728-fell-end.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-light-390-fell-end.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-728-fell-end.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/discrete-r2-dark-390-fell-end.png

## Review scope and close

I listed the three existing tabs before I opened a separate review tab.
I used only the review tab and closed it at the end.
The three original tabs retain their original URLs.
I did not log in or save downloads.

The local server ran in the background on port 50461, after a free-port check.
The server process, PID 3513947, no longer exists.
A connection to that port returned connection refused.
A temporary socket could bind and listen with `SO_REUSEADDR`, then closed.
A bind without that option initially met a residual socket state after shutdown.
These observations confirm that the server stopped.

The report's SHA-256 stayed unchanged:
`8d80b23f3fcd2875f44c9b97b9c6b86f8c9e9eeaf9cd5381b90bd0130e41a691`.
Only this review record was added inside the repository.
Screenshots reside outside the repository at the paths above.
No commit was made.
No tests were written or run.

## What looks correct

- The memo index uses readable stacked rows at 390 px.
- Memo and check filenames remain intact at both widths.
- Every chart subscript exceeds the 10 CSS px minimum.
- Chart labels remain clear of other labels, lines, dots and bars.
- All chart text stays inside its SVG bounds.
- The document and all seven table containers have no horizontal overflow at 390 px.
- Text, status labels and chart series remain distinct in both themes.
- The revised paragraph in `fell` wraps cleanly.
- The favicon causes no request error, and the console contains no errors or warnings.
