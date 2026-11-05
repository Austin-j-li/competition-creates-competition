# Report visual QA — round 3

Reviewed on 21 October 2026.
URL: http://127.0.0.1:8791/report.html.
Viewport widths: 728 px and 390 px. Height: 950 px.
The scroll bar left SVG widths of 713 px and 375 px.
The dark view used the exact document rewrite supplied in the review brief.

## Status of the round-2 problems

1. **Fixed — tiny chart labels at 390 px.**
   All four charts use a 460-unit viewBox and 15-unit text in the narrow layout.
   Main labels now appear at about 12.2 CSS px, instead of about 5.7 px.
   The ledger uses a height of 250 units in the narrow layout.
   The labels are readable at normal size in both themes.

2. **Fixed — poor visited-link contrast in dark mode.**
   The rule `a,a:visited` uses the chart-1 color.
   I clicked contents links and returned to the contents without a reload.
   The visited links stayed light blue in both dark views.
   The computed link color was `rgb(110, 168, 254)`.
   The browser hides visited-state details from scripts; the screenshots provide the visual check.

3. **Fixed — “ρ = 0.25” overlaps “0.252”.**
   The base-rate label now sits above the entry plot.
   It stays clear of the final bar value at both widths and in both themes.

4. **Fixed — “Gaussian” and “logistic” touch their curves.**
   Both labels now have clear gaps from their curves.
   The Laplace label also stays clear of its curve.
   This holds at both widths and in both themes.

## New problems, most severe first

1. **Low — vertical ledger lines pass through the row labels.**
   Chart: `ch-ledger`; width 390 px; both themes.
   The narrow layout places the three row labels inside the plot.
   The vertical grid lines and the zero line continue through those label rows.
   For example, the zero line passes through “from” in “Extra sale proceeds from entry”.
   Suggested fix: draw separate grid segments within the bar rows, below each label.
   Alternatively, place an opaque background behind each label, with a small text margin.
   Screenshots:
   - /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-390-ch-ledger.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-ch-ledger.png

2. **Low — the left ledger tick clips at the SVG edge.**
   Chart: `ch-ledger`; width 390 px; both themes.
   The “−0.2” tick starts at x = −2.23 in the 460-unit viewBox.
   The edge cuts a small part of the minus sign, about 1.8 CSS px.
   Suggested fix: increase the narrow layout's left margin from 14 to at least 20 units.
   An alternative sets the first tick's text anchor to `start`.
   Screenshots:
   - /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-390-ch-ledger.png
   - /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-ch-ledger.png

No other visible overlap, curve contact, or text clipping appeared in the four charts.
The bottom axis titles have little spare space.
Their font boxes extend about 0.68 viewBox units below the narrow SVG bounds.
I saw no clear loss of glyphs there, so this is not a separate visual defect.
An extra two units of bottom clearance would remove that edge risk.

## Console and resize observations

The report console had **zero errors and zero warnings**.
This held after the light views, the dark rewrite, and the resize cycle.
Console capture: /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-console.txt.

The light page completed a 728 → 390 → 728 px cycle without a reload.
I allowed 300 ms after each resize for the 150 ms redraw delay.
The first three viewBoxes changed from 720 × 300 to 460 × 300 and back.
The ledger changed from 720 × 210 to 460 × 250 and back.
The text changed from 12 to 15 units and back.
The wide tick counts returned; the charts had no duplicate labels or missing series.
The return screenshots match the initial wide layouts on visual inspection.
The dark page also returned from the narrow layout to the wide layout without a reload.

One browser command sought a `nav` element, which this page does not contain.
That command timed out; I used the actual `.toc` element for the link screenshots.
This tool timeout was not a page console message.

I listed the existing tabs before I opened a new tab.
I used only that new tab and closed it at the end.
The three original tabs retain their original URLs.
I did not log in or edit the report.
I wrote no tests and ran no test suite.

## Screenshot paths

Light mode, width 728 px:

- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-728-ch-split.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-728-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-728-ch-entry.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-728-ch-ledger.png

Light mode, width 390 px:

- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-390-ch-split.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-390-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-390-ch-entry.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-light-390-ch-ledger.png

Dark mode, width 728 px:

- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-728-ch-split.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-728-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-728-ch-entry.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-728-ch-ledger.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-728-links.png

Dark mode, width 390 px:

- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-ch-split.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-ch-entry.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-ch-ledger.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-dark-390-links.png

Light mode, after the return to 728 px without a reload:

- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-resize-back-728-ch-split.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-resize-back-728-ch-post.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-resize-back-728-ch-entry.png
- /home/uctpiaj/work/vm-browser/evidence/mcp/report-r3-resize-back-728-ch-ledger.png
