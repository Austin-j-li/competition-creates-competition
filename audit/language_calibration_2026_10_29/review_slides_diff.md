# Review of the slide terminology diff

29 October 2026. Counts: **0 must-fix, 1 should-fix, 0 optional**. There are no must-fix items.

The terminology change preserves the actor roles and the economic sequence. One script phrase needs a possessive to avoid the adjective sense of “rival”.

| Location | Current text | Problem | Fix | Severity |
|---|---|---|---|---|
| `overleaf/slot/slides_script.md:257`, frame 15 | “Conditional on the case and signal, rival value theta and incumbent value R are independent.” | “Rival value” can mean a competing value. The phrase names the value that belongs to the rival. | Replace “rival value theta” with “the rival's value theta”. Then update frame 15's count from 202 to 203. Update the main total to 3,458 and the total with the title to 3,522. | should-fix |

The review covered only `git diff -- slides.tex slides_script.md` against HEAD `eaf30496c9a54e42eff65b1c5b96ded51f811f18` in `overleaf/slot`. The contract was `decisions.md` and `scan_slides.md`, with the accepted exceptions in the review brief. No paper diff was reviewed. No source file was edited. No test was written or run. No Git command changed state.

The checks found these results:

- No swap assigns the incumbent's role to the rival, or the rival's role to the incumbent.
- “Rival profit” and “rival gross profit” name the accepted profit object. The short labels remain consistent with its class components and prior value.
- No new bare “trader” refers ambiguously to the informed trader. The two generic script uses, at lines 113 and 133, mean whoever fills the slot.
- Frame 5 defines “incumbent bidder” and “potential rival bidder” under the correct label heads. The script defines both names in the title speech.
- Frame 6 now says “Rival, if prepared, learns” its value. Frames 5 and 7 and the script retain the incumbent's earlier knowledge of its own value.
- Articles, agreement, possessives, title capitals and label capitals show no other swap defect. The slides contain no first-person prose.
- All 19 script frame titles match the slide titles exactly. The headline matches the contract on frame 19 and in the closing speech.
- Whole-word searches found zero occurrences of buyer, challenger, investor, specialist or entrant, including their plurals, in either source file. The two slide occurrences of “arrival” remain intact.
- The accepted B8 claim, frame 5 market makers, Bulow–Klemperer bidder, Fishman first bidder and sector-expertise descriptions are present.
- Every current speech count matches the stated whitespace rule: main frames 3,457; title 64; combined 3,521.

Changes outside visible words were also checked:

- Five source comments changed at `slides.tex:8`, `:10`, `:66`, `:67` and `:114`. The scan explicitly requests these terminology updates.
- The frame 5 spacer `\vspace{0.25em}` was removed, as authorized.
- Frame 5 adds one `\textbf{...}` call for “potential rival bidder:”. This follows the definition format in the scan.
- The script's silent count table and totals changed. The scan requires the recount, and the current counts are correct.
- All 394 extracted key uses remain identical. These include frame labels, references, navigation targets and registry calls.
- All 1,073 extracted math spans remain identical. Macro names, signatures and environment sequences remain identical. Macro bodies change only their visible labels. Figure coordinates remain identical. The only removed numeric token in the slide source is the authorized spacer's `0.25`.

The supplied pre-change PDF was absent. The baseline was built from `git show HEAD:slides.tex` in a scratch directory outside the repository. The build used the existing local style, registry and figure files.

Both PDFs have 56 pages. Poppler rendered every page at **80 dpi**. A raster comparison identified 47 changed pages, and each received visual inspection:

`2–31, 33–35, 37, 39–41, 43–45, 48–52, 55–56`.

Frames 5, 6, 10, 16 and 18 fit without visible clipping or collisions. The changed figure overlays on frame 14 and backup B3 remain clear. No changed page has a new bad wrap or overlap.

The current log reports a **0.1453 pt overfull vertical box** at frame 5's end. The baseline has no such warning. The rendered footer remains separate from the page footer, with no clipped text. This is a build observation, not an additional repair request.

Scratch evidence: `/home/uctpiaj/work/tmp/slides-terminology-review-_fk9r7f3/`. The repository's built PDF was not rebuilt or replaced.
