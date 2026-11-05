# Study guide

The guide explains the order-slot manuscript in `../overleaf/slot/` (revision 5bad2bc, 26 October 2026).
It is for a reader who knows basic probability and needs every step of each derivation.
Chapters 1 to 13 use words and symbols, with no numerical examples. Chapter 14 lists the example's values for use with the figures.

- PDF: `../output/pdf/Competition_Creates_Competition_Study_Guide.pdf` (352 pages).
- Short guide (49 pages): `../output/pdf/Competition_Creates_Competition_Study_Guide_Short.pdf`. Text: `short/chapters/`. Build: `./build_short.sh`, or `./build_short.sh 07_main_result` for one chapter. It keeps the paper's main results and the key proof steps, and it cuts the exercises, most analogies and the arithmetic steps.
- Build: `./build.sh` for the whole guide, or `./build.sh 07_main_result` for one chapter. The build needs pdfLaTeX and latexmk.
- Text: `chapters/`. Macros and boxes: `preamble.tex`. Writing rules: `STYLE.md`.
- `source/` holds copies of the manuscript's `numbers.tex` and its three figures. Values print through `\reg{key}`.

Chapters 2 to 7 received a second read against the manuscript. Chapters 1 and 8 to 13 did not.

On 27 October 2026 all earlier guides were removed: the guide of 26 October, the old slot guide, and the `learn/` course on the earlier paper.
An archive of them is at `/mnt/rdss/austin/project-backups/2026-10-27/ccc-old-study-guides.tar.gz`.
