# Competition Creates Competition

Stock Prices and the Discovery of Takeover Bidders

Austin Li. Working-paper revision, 2026-10-04. Built from the Overleaf manuscript master at
commit 0fa51c0 ("Apply theory, citation and copy-edit corrections to the edited text").

main.pdf contains the theory working paper and its paper appendix (73 pages).
online_appendix.pdf supplies the detailed proofs, numerical methods and additional results
(57 pages). The website serves these files as `main_filled.pdf` and
`online_appendix_filled.pdf` so that existing links keep working.

## Build

`latexmk -pdf main.tex` and `latexmk -pdf online_appendix.tex` in a clean copy of the Overleaf
project (pdfTeX, TeX Live 2023, with newtx and kastrup from CTAN).

| File | sha256 |
|---|---|
| main.pdf | d67ae249d7a971383031ecad3e16377e3727b58739f1442bdd53075606cbbfde |
| online_appendix.pdf | 70f739fdf9dcc676da79d70c8fac1e1ed6bbf249f3fdb16cdf69d921dd3cfcbd |

## Number reconciliation

Every decimal number in the Overleaf `main.tex` and `online_appendix.tex` at 0fa51c0 also
appears in `paper/main_filled.tex` and `paper/online_appendix_filled.tex`, the validated
filled manuscripts from which the Overleaf project was imported on 2026-09-30 (their sha256
values match the Overleaf `source-provenance.json`), so the revisions since then introduced no
new number. The Overleaf `tables/*.tex` files are byte-identical to `tables/` in this
repository. The four figure PDFs are the 6 September 2026 renders.
