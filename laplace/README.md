# Laplace version

This folder holds the Laplace version of the paper, after the revision of 21 October 2026.
The revision uses two quality classes, a zero low preparation cost and a justified Laplace
noise law. The numerical layer of the revision is in `numerics/`, `tables/` and `figures/`
at the repository root.

## Contents

| Path | Content |
| --- | --- |
| `manuscript/main.tex` | Manuscript (pdfLaTeX) |
| `manuscript/online_appendix.tex` | Online appendix (pdfLaTeX) |
| `manuscript/figures/`, `manuscript/tables/` | Figures and tables of the manuscript |
| `talk/talk.tex` | Conference talk (XeLaTeX) |
| `talk/script.tex` | Speaker script (pdfLaTeX) |
| `../audit/revision_v2_2026_10_21/` | Brief, drafts, integration, reviews and numerical reconciliation of the revision |
| `../audit/alex_meeting_2026_10_21/` | Memos and scripts that prepared the meeting of 21 October |
| `../audit/talk_v2_2026_10_22/` | Briefs and text for the new opening of the talk |

`manuscript/` also holds copies of `talk.tex` and `script.tex` from 5 October 2026.
These copies are older than `talk/`. Use `talk/` for the talk.

## Build

```bash
cd laplace/manuscript
latexmk main.tex               # pdfLaTeX, set in latexmkrc
latexmk online_appendix.tex
cd ../talk
latexmk talk.tex               # XeLaTeX, set in latexmkrc
latexmk -pdf script.tex
```

The bibliography text in the LaTeX files is already rendered. A change to `references.bib`
alone does not change that text. Do not commit the PDF files.

## Numbers

The numbers in the manuscript come from the validated numerical pipeline. The root
`README.md` gives the exercise commands and the release gate (`numerics/verify.py --final`
and `numerics/release_checks.py`). `../audit/revision_v2_2026_10_21/reconciliation.csv` lists
each quantity with its old value, its new value, its source file and its row. Do not type a new number by hand.

## Overleaf

| Folder | Overleaf project |
| --- | --- |
| `manuscript/` | <https://www.overleaf.com/project/6abd31b3b1fcb8e38afbb670> |
| `talk/` | <https://www.overleaf.com/project/6abd18d03a1e83999c33b27f> |

Each folder is a Git subtree of the `main` branch of its project, with the full Overleaf
history. Use your own Overleaf Git token. The token is not in this repository; do not add it.

Get the edits from Overleaf first:

```bash
git subtree pull --prefix=laplace/manuscript https://git.overleaf.com/6abd31b3b1fcb8e38afbb670 main
git subtree pull --prefix=laplace/talk https://git.overleaf.com/6abd18d03a1e83999c33b27f main
```

Then send the edits from this branch to Overleaf:

```bash
git subtree push --prefix=laplace/manuscript https://git.overleaf.com/6abd31b3b1fcb8e38afbb670 main
git subtree push --prefix=laplace/talk https://git.overleaf.com/6abd18d03a1e83999c33b27f main
```

On the VM and on other machines, `overleaf/paper/` and `overleaf/talk/` can be separate Git
working copies of the same two projects. The parent repository ignores them. The subtrees
are under `laplace/` so that the two do not collide.

## Relation to the order-slot version

The order-slot version is on the branch `slot`, under `slot/`. It keeps the auction, entry
and ownership set-up of this version and replaces the Laplace order flow with one public
order slot. `slot/manuscript/comparison.tex` describes the two set-ups and puts the main
results side by side. The proof packages of the order-slot version read this manuscript at
the Overleaf commit `01bd5d6`.
