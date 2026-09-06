# Exhibit inspection

Figures 1, 3, and 4 were rendered from the fresh C.1/C.5/C.7 outputs to this audit directory, without replacing the canonical registry or thresholds during the independent run.

Figure 3: both panels visually inspected in color and grayscale. Logistic endpoints are filled at zero tail mass and preparation 0.25; Laplace endpoints retain their positive plateau mass and equality preparation. Direct labels, panels, and units are readable; no clipping. Renderer validates the logistic benchmark cutoff against b*pi/sqrt(3), giving 1.4953689214214978 noise standard deviations from the fresh CSV.

Figure 4: both panels visually inspected in color and grayscale. Crossing at eta=0.5 visible. Numeric eta<1 filtering excludes zero-profit eta=1 even when stored as 1.0. Initial lower axis limit clipped the last strictly positive strong low-type profits; changed to 80% of the minimum retained profit. Final rerender pending after this limit change. No in-figure title or payment-stage interpretation change.

Figure 2 and table PDF inspection await fresh C.2/C.6 outputs.

Nonreserve table QA used the manuscript's fonts and one-inch margins in `audit/peer_polish/tables_qa/`:
- Main Tables 1 and 3 already fit. Table 2 overflowed by 49pt due to the fixed-profile qualification repeated in every Unique cell. The cells now read n/a, with the explanation retained in the notes; the first column was adjusted by 0.015 linewidth and price-hidden labels shortened. The resulting main tables compile with zero overfull boxes.
- The complete signal grid overflowed by about 100pt in portrait. It now occupies one landscape page at readable footnote size, preserving all 25 rows, negative comparisons, margins, and notes. No overfull boxes.
- The full margins table is a readable landscape page with all individual margins and distinct parameter vectors. Matched-price panel remains portrait; a long repeated control label was shortened and the first column adjusted by 0.005 linewidth after a 0.5pt overflow. Source-derived values and both matched-dividend identities are unchanged.

Figure 4 final grayscale rerender inspected after the axis-limit fix. Every retained positive profit is now above the lower axis boundary. Figure 1 also inspected in grayscale: all three posterior-profit curves have distinct dash patterns and readable direct labels; axes and panel letters are clear.

Fresh fixed-reserve tables passed their complete parameter/continuation/institution/information identity joins. Main Table 4 initially exceeded the portrait width by31.6pt. Shorter row labels retain weak/strong,r,p and permit a narrower first column; all8rows now fit on one readable portrait page. The online details preserve both information structures, including state versus class-only investor information and price-only buyer information, with break opportunities in long IDs. Main and online reserve detail PDFs have zero overfull boxes.

Exploratory layout QA is provisional until the final C.6 duplicate audit finishes. Current full-run ranges pass ledger identities. The summary displays singleton found ranges once, with an explicit note;40exact events occupy two landscape longtable pages with repeated headings. All5reserve QA pages were visually inspected, with no clipping or overlap. Final exploratory values/counts will be regenerated after C.6 signoff.

Final C.2/C.6 outputs are frozen. Canonical registry, dictionary, tables, and four figures regenerated; render manifest passes. Final Figure 2 color/grayscale, matched-price page and exploratory summary inspected after regeneration. All three table QA compilations report zero overfull boxes. Full evidence and hashes: `audit/peer_polish/logs/s5_presentation_vm.md`.
