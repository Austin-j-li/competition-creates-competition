# S0 smoke check — 25 October 2026

Starting revision: `26895f3b87e76e6a5aa9c97adfd2b405df7fead7` on `theory-upgrade`. No `LOCK` file was present.

Gate state: the smoke check is complete. The rest of S0 (the label map, the line re-anchor of the lens plans and the record of side commit 80804f0) is not done. The S1 decision gate is blocked: all nine answer lines in `plan/DECISIONS.md` are empty.

## 1. Result in brief

- The three documents build with no errors, no undefined references and no overfull boxes.
- The numbers pipeline is consistent: 5221 keys, 0 conflicts, 0 missing keys, 0 typed decimals.
- The figure program runs. Every boundary and value it prints matches the registry (34 of 34 rows).
- The three manuscript figures are pixel-identical to the committed figures.
- The three slide figures fall back from Fira Sans to DejaVu Sans, because the Fira path in the figure program is fixed to one machine. S2 fixes this path.

## 2. Software that was missing and was installed

The base image has TeX Live 2023 (Debian), Python 3.13.17 and NumPy 2.5.3. The items below were missing. They were installed in this work period only; no project setting or environment variable was changed.

| Missing item | Where it showed | Installed |
|---|---|---|
| `newtxtext.sty`, `newtxmath.sty` | `main.tex` line 10 (fatal) | apt `texlive-fonts-extra` 2023.20240207-1 |
| `binhex.tex` | `main.tex`, second build (fatal) | apt `texlive-plain-generic` 2023.20240207-1 |
| `ts1-qtmr.tfm` (TeX Gyre Termes metric for newtx) | `main.tex`, third build (fatal) | apt `tex-gyre` 20180621-6 |
| Fira Sans OTF fonts for the slides | `slides.tex` line 14 | supplied by `texlive-fonts-extra` above |
| moloch keys `frametitle margin left` and `frametitle margin right` | `slides.tex` line 9 (pgfkeys error) | moloch v2.3.1 from CTAN, made from its `.ins` file into the user TeX tree; TeX Live 2023 has moloch v0.1.0 |
| Python `mpmath`, `matplotlib` | `make_figures.py` imports | pip: mpmath 1.4.1, matplotlib 3.11.2 (with fontTools 4.67.0) |

`plan/cloud_setup.sh`, the installer that `S0_setup.md` names, is not in the branch at this revision. A setup step for later work periods needs the three apt packages, a moloch release that knows the frame-title margin keys, and the two Python packages above.

## 3. Commands and outputs

All commands ran with the documents and data as committed.

1. In `slot/manuscript/`: `latexmk main.tex`. Exit 0 after the installs. Output: `main.pdf`, 102 pages. The log has no warnings, no undefined references and no overfull or underfull boxes. All fonts are embedded.
2. In `slot/manuscript/`: `latexmk -xelatex slides.tex`. Exit 0 after the installs. Output: `slides.pdf`, 34 pages, no overfull boxes. The log has two kinds of warning:
   - `TU/lmr/b/it` is not available in sizes 5, 6 and 9 at `slides.tex` line 423; bold slanted is used instead.
   - hyperref removes `\translate` from a PDF bookmark at line 571 (`\AppendixStart`).
3. In `slot/manuscript/`: `latexmk comparison.tex`. Exit 0. Output: `comparison.pdf`, 16 pages, no warnings, no overfull boxes.
4. From the root: `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/make_numbers.py`. Exit 0. Output: `keys: 5221; conflicts: 0`. The rewritten `registry.csv` and `numbers.tex` are byte-identical to the committed files.
5. From the root: `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`. Exit 0. Output: `files scanned: 21; distinct keys used: 676; missing keys: 0` and `literal decimals outside \reg: 0`.
6. From the root: `python3 audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py`. Exit 0. Output:
   - nine boundaries (r_A, r_F, r_N, r_J, r_S, r_C, r_R, the cap strength, r_U) and 25 other values, each printed beside its registry display; all 34 rows match;
   - boundary order r_A < r_F < r_N < r_J < r_S < r_C, that is 1.393958 < 1.467127 < 1.747878 < 1.966097 < 2.124148 < 3.592659;
   - `Fira Sans registered: False`; the slide figures embed DejaVu Sans with Computer Modern math; the manuscript figures embed STIXGeneral.

## 4. Figure comparison

The committed figures were saved before the run and compared with the new output.

- `beliefs.pdf`, `coexistence.pdf`, `research.pdf`: the bytes differ (new font subset tags, matplotlib 3.11.2 against 3.11.1). The extracted text is identical. Rendered at 100 dpi, the maximum pixel difference is 0.
- `beliefs_talk.pdf`, `coexistence_talk.pdf`, `research_talk.pdf`: the text font changes from Fira Sans to DejaVu Sans. These files must not be committed from a run without the Fira path.
- The run log changes only in the font lines, the matplotlib version and the file hashes.

All six figures, the run log and the PNG previews were restored to the committed state. No figure or number moved.

## 5. Pages read

Page 1 of `main.pdf` (title and abstract), slide 2 of `slides.pdf` and page 1 of `comparison.pdf` were rendered and read. They show the expected text, fonts and layout. The text of all three PDFs has no `??` and no "in preparation".

## 6. Language scan

Not applicable. No manuscript text changed.

## 7. Clean-up

The PDFs, auxiliary files, slide navigation files, `.xdv` and figure previews were deleted. The working tree differs from the starting revision only by this report.

## 8. Next eligible work

- S1: Austin answers the nine decisions in `plan/DECISIONS.md`. The update waits for these answers.
- After S1: the rest of S0 (label map from this build, line re-anchor, record of 80804f0), then S2 (the Fira path, the real includes, the language scan).
