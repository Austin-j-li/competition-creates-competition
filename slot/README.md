# Order-slot version

This folder holds the order-slot version of the paper. In this version, one public
order slot replaces the Laplace order flow of the version on `main`. The informed
investor fills the slot with probability `λ`. Otherwise, a liquidity trader sells,
abstains or buys with probabilities `β`, `1 − 2β` and `β`.

## Contents

| Path | Content |
| --- | --- |
| `manuscript/main.tex` | Manuscript (pdfLaTeX) |
| `manuscript/slides.tex` | Presentation (XeLaTeX) |
| `manuscript/comparison.tex` | Comparison of the order-slot and Laplace set-ups (pdfLaTeX) |
| `manuscript/sections/`, `manuscript/appendix/` | Text of the manuscript |
| `manuscript/figures/` | Figures of the manuscript and the presentation |
| `manuscript/numbers.tex` | Generated file: one `\reg{key}` entry for each registry row |
| `../audit/slot_manuscript_2026_10_23/` | Proof packages, check memos, number registry and scripts |
| `../audit/microstructure_search_2026_10_22/` | Search that selected the order slot |
| `../audit/discrete_exploration_2026_10_21/` | Earlier study of discrete trading |

Start with `../audit/slot_manuscript_2026_10_23/BRIEF.md` and `LEDGER.md` in the same folder.
They give the model decisions, the workstreams and the checks.

## Build

Run these commands in `slot/manuscript/`:

```bash
latexmk main.tex              # pdfLaTeX, set in latexmkrc
latexmk -xelatex slides.tex   # XeLaTeX
latexmk comparison.tex        # pdfLaTeX
latexmk -c                    # remove the auxiliary files
```

The manuscript and the comparison use the `newtx` fonts and `natbib` with the `aer` style.
Do not commit the PDF files.

## Numbers

The documents print every number through `\reg{key}`. Do not type a number in the text, and do
not edit `numbers.tex`. To change a number, do these steps from the repository root:

1. Edit the row in `audit/slot_manuscript_2026_10_23/registry/<STEM>.csv`.
2. Run `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/make_numbers.py`.
   The script writes `registry/registry.csv` and `slot/manuscript/numbers.tex`.
   It prints each key that two files give with different display values.
3. Run `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py`.
   The script lists the keys in use, the keys missing from the registry and the decimals
   typed directly in the source.

The figures come from the closed forms of the proof packages. To make them again, run
`.venv/bin/python audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py`.
The script needs `numpy`, `mpmath` and `matplotlib` (see `replication/README.md` for the
environment). It writes the PDF files into `slot/manuscript/figures/`.

## Overleaf

The Overleaf project is <https://www.overleaf.com/project/6adbcf95d3bcdaeacca72fcf>.
`slot/manuscript/` is a Git subtree of that project's `main` branch, with the full Overleaf
history. Use your own Overleaf Git token. The token is not in this repository; do not add it.

Get the edits from Overleaf first:

```bash
git subtree pull --prefix=slot/manuscript https://git.overleaf.com/6adbcf95d3bcdaeacca72fcf main
```

Then send the edits from this branch to Overleaf:

```bash
git subtree push --prefix=slot/manuscript https://git.overleaf.com/6adbcf95d3bcdaeacca72fcf main
```

Commit only files that belong in the Overleaf project under `slot/manuscript/`.
Records, scripts and the registry stay under `audit/`.

## Relation to the Laplace version

The Laplace version is on the branch `laplace`, under `laplace/`, after its revision of
21 October 2026. `main` holds the Laplace version before that revision. The auction, entry
and ownership set-up of the Laplace version is the base of this version. `comparison.tex` describes the two set-ups, puts the main results
side by side and gives the trade-offs between them. The proof packages read the
Laplace manuscript at the Overleaf commit `01bd5d6`, which is `laplace/manuscript/` on that branch.
