# S0 baseline presentation rebuild: comparison with the reviewed PDFs

Date: 2026-09-05. Source revision: commit `1cb7475b` on `peer-circulation-fix`, clean tree.

## Setup

- Isolated copy: `rsync -a --exclude .git --exclude .venv --exclude __pycache__ --exclude .DS_Store`
  of the repository to
  `/private/tmp/claude-501/-Users-austinli-Projects-competition-creates-competition/b1216b8b-72db-4131-8936-6f28dcd5c5fc/scratchpad/baseline_build/`,
  with `.venv` symlinked to the original `.venv`. All paths inside `numerics/` resolve through
  `numerics.io.ROOT` (parent of `numerics/`), so the copy built entirely against itself; the
  original repository was not written to.
- Pre-build snapshot of the copy's generated outputs kept in `baseline_build/_orig/`.
- Raw exercises (`numerics/exercises/c1..c7`) were NOT run. Only the OA E.1 presentation chain
  was executed, in this order, with `.venv/bin/python` (3.12.13, NumPy 2.5.2, SciPy 1.18.1,
  mpmath 1.4.1, matplotlib 3.11.1; pandoc 3.9.0.2; latexmk 4.88; pdfTeX 1.40.29, TeX Live 2026).

## Exit codes and runtime

| Step | Command | Exit | Runtime (s) | Log |
|---|---|---|---|---|
| 1 | `numerics/check_registry.py` | 0 | 3.43 | `s0_baseline_check_registry.log` |
| 2 | `numerics/registry.py` | 0 | 0.15 | `s0_baseline_registry.log` (118 rows, 0 open) |
| 3 | `numerics/substitute.py` | 0 | 0.09 | `s0_baseline_substitute.log` (95 filled, 0 unresolved, 0 unknown) |
| 4 | `numerics/render/render_all.py` | 0 | 0.92 | `s0_baseline_render_all.log` |
| 5 | `numerics/render/latex.py` | 0 | 2.85 | `s0_baseline_latex.log` ("LaTeX build ok"; warm `paper/build/`) |
| 6 | `numerics/verify.py --final` | 0 | 1.94 | `s0_baseline_verify_final.log` (416 PASS, 0 FAIL, handout build passed) |

No step failed; `raw_failures/` is empty.

## Output hashes (rebuilt copy)

| File | Reviewed / original SHA-256 | Rebuilt SHA-256 |
|---|---|---|
| `paper/main_filled.pdf` | `6568203e5266ffe076ec094ef9768b763f7a227813064418fa680c4b6bff1427` | `6630bb260728e32f40aebe860f1b0f101e2e2159b591e8f6111a3cabb29d6840` |
| `paper/online_appendix_filled.pdf` | `734a51c2e4ed130e3cb11597c89d2c32d39a01dad64704ee1979a54427e36922` | `11c9900588cece19a46cbe649134b7f09ece089d383b45a45c3f1ee8edb32727` |
| `figures/two_returns.pdf` | `d2b8e6deeccd271f4afbe28e870a106196b9b21af052acd27599a7d359bd846e` | `3bbf3fdbd712eee739da1875d53b8af54afa4fd8f81a5e4f30986ac1903876a9` |
| `figures/equilibrium_correspondence.pdf` | `53d0e5f59874a727f17fb9757775aaf1d3cbb34c6ceff7d672fca55ffda30932` | `81a3d6cfd5ccb3ab8feeec80e28cab79bac1413f70b6b5d7b45973007a34dc29` |
| `figures/posterior_tail_entry.pdf` | `c25a3118bb770ff1dafa8ac8889f8f306179885985f14d99444902c35b0c8e7f` | `befd7344664c31618a1fefa81c0fa3d422e017dfe7252612c811f60beebd9b43` |
| `figures/bargaining_weight.pdf` | `2ecf3684b67646ce7544376b1f0e917e76f34fc97c6b536938348628f93bf114` | `0e9725c88e5d7aa2544be2d6e6e124a2988fb7f2401f6904f7e0339df3091493` |

## Comparison

Byte-identical after the rebuild (cmp):

- `numerics/quantity_registry.csv`
- `paper/main_filled.md`, `paper/online_appendix_filled.md`
- `paper/main_filled.tex`, `paper/online_appendix_filled.tex`
- all 9 files in `tables/` (4 CSV, 5 `.tex`)
- all 3 files in `figures_data/`
- `docs/index.html`
- `numerics/manifests/c1_baseline.json` … `c7_bargaining.json`, `handout.json`

Differing after the rebuild, metadata only:

- `figures/*.pdf` (4): the only differing line in each is `/CreationDate` (matplotlib stamp,
  `D:20260905191722` vs `D:20260905223446`).
- `numerics/manifests/c8_registry.json`: `timestamp_utc` only.
- `numerics/manifests/render.json`: `timestamp_utc` and the four figure-PDF hashes (consequence of
  the figure `/CreationDate`); the five table `.tex` hashes are unchanged.
- `paper/online_appendix_filled.pdf`: `strings` diff shows only `/CreationDate`, `/ModDate`, and
  the trailer `/ID`.
- `paper/main_filled.pdf`: `/CreationDate`, `/ModDate`, `/ID`, plus differing compressed
  streams, which are the embedded figure PDFs carrying the new `/CreationDate`.

Substantive comparison of the manuscript PDFs:

- `pdftotext -layout` extracted text: 0 differing lines for both documents (main 52 pages,
  online appendix 43 pages in both versions).
- Rasterized pages (`pdftoppm -r 50 -gray`): 52/52 main pages and 43/43 appendix pages are
  pixel-identical to the originals.

## Verdict

The local source at commit `1cb7475b` reproduces the reviewed PDFs substantively: every
numerical table, figure input, registry value, filled Markdown, and LaTeX source is
byte-identical, and the rebuilt PDFs differ from the reviewed ones only in pdfTeX/matplotlib
creation timestamps and the PDF `/ID`. No numerical difference was observed. The raw exercises
were not rerun in this stage; their outputs were taken from the committed, hash-locked files and
were confirmed against their manifests by `verify.py --final`.

Note: the isolated copy was taken from the clean tree at commit `1cb7475b` (verified byte-equal
to HEAD for the editable sources). Concurrent edits to `paper/main.md` and `handout/sections/*`
appeared in the original working tree while S0 ran; they are not part of this comparison.
