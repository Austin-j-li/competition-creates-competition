# Handoff — 25 October 2026, 21:10 UTC

Austin stopped the cloud run during S4 to continue with local agents. This file gives the state of the work and the steps to resume it. `PLAN.md` is still the authority on order, rules and gates. `NOTATION.md` is frozen.

## 1. Done and pushed on `theory-upgrade`

| Commit | Stage | Report |
|---|---|---|
| `d5d29ac` | S0 smoke check | `progress/S0_smoke.md` |
| `6f56952` | S0 baselines and S1 decisions | `progress/S0.md`, `progress/S0_label_map.md`, `plan/DECISIONS.md` |
| `144b039` | S2 tooling | `progress/S2.md` |
| `a1f7b6f` | S3 notation and vocabulary freeze | `progress/S3.md`, `plan/NOTATION.md` |
| this commit | S4, partial | this file, `progress/S4_briefs.md`, `statements/` |

Each stage before S4 passed its gate: build, pages read, language scan judged, number scan clean, report, push. At `a1f7b6f` the paper builds to 103 pages. The language scan gives 975 hits, all in the starting text that S5 to S11 rewrite. The number scan reports 676 keys, 0 missing and 0 typed decimals.

## 2. S4 state

Five jobs ran in parallel: one mathematics writer for each area A to D, then a referee and a fix pass for each area, and the prose writer for the wording targets. I stopped all of them at 21:05 UTC. The writers worked in place in `statements/`, and nothing in that folder is refereed except O1 (see below).

**Warning:** a stopped writer can leave a file in the middle of an edit. Read each file before you build on it.

| Job | State | Files |
|---|---|---|
| A: foundation and ownership (A2, A3, A6; Proposition 2; Corollary 1; O2, O6, O7) | The writer was stopped while it wrote `A.tex`. Its derivations were done (reduction lemma, two numbers, constructed tuples, takeover share, decisive advantage, Corollary 1, Proposition A.7). | `statements/O2/`, `statements/O6/`, `statements/O7/` (proof, notes, print-only computation each). No `A.tex` or `A_notes.md` yet. |
| B: coexistence (A4; Proposition 3; Corollary 2; O5, O9) | The writer was stopped near its end. Both files are complete through section 18 of the notes. | `statements/B.tex` builds (7 pages; 11 keys still print `??`: the `twopath_*` keys, `margin_balance_B_frac`, `margin_balance_sq_B_frac` and `margin_unif_afford_B`), `statements/B_notes.md`, `statements/O5/`, `statements/O9/`. Not refereed. |
| C: research (A5; Proposition 4; Corollary 3; O3, O4, O8; O1 notation) | The writer was stopped early. It finished the O1 notation pass and started O3 and O4. | `statements/O1/` (notation pass done; see section 9 of `O1_notes.md`), `statements/O3/O3_proof.tex` (draft), `statements/O4/o4_margins.py` (computation only). No `C.tex`, `C_notes.md` or O8 yet. |
| D: empirical (A8) | The writer finished ("done with open issues"). The referee had started and was stopped before it wrote a report. | `statements/D.tex` builds (9 pages; 7 keys still print `??`; `D_notes.md` part 4 gives their exact values), `statements/D_notes.md`. Not refereed. |
| Wording targets (prose writer) | Draft finished: 52 targets in paper order, each with its location, the result it must match and its scope list. The file ends with 5 placeholder keys and 15 open points for the referee. | `statements/wording_targets.md`. Not refereed; the referee needs `A.tex` to `D.tex` first. |

**O1.** The proof is done. The referee accepted it with fixes to notation and wording only (`O1/O1_referee.md`). The C writer then applied the frozen notation and referee fixes 3 to 5. It did not change the mathematics. A referee has not yet read this notation pass.

**Open issues the writers reported:**
- D, medium: Corollary A.3(b) states observational equivalence on the whole segment \(\lambda'\in[s_+,1-3b]\). The referee report W5 proves it only near the true value. The D referee must decide.
- D, low: label stubs (`cor:coexistence`, `prop:region`, `lem:a4-order`) wait for the final labels of areas B and A.
- Wording targets, medium:
  - Proposition 3(c) depends on O9.
  - The liquidity footnote depends on O2.
  - Proposition 4(d) depends on O3 and O4.
  - The two takeover-share decimals are the writer's own arithmetic, so recompute them.

## 3. What remains

1. **Finish S4.**
   - Area A: write `A.tex` and `A_notes.md` from the O2, O6 and O7 folders and the area A brief.
   - Area C: write `C.tex` and `C_notes.md`, and finish O3, O4 and O8.
   - Referee each area with a reader that did not write it. Austin's staffing note keeps the strongest reader for two places: the referee of the A5 research package in S5, and the second reader in S13.
   - Apply the fixes.
   - Referee the wording targets against `A.tex` to `D.tex` and apply those fixes.
   - Run the gate, then write `progress/S4.md`, commit and push.
2. **S5 to S13**, as `PLAN.md` Part 4 orders them:
   - S5: appendix packages, A2 first, then A3 and A6, A4, A5 and A8 in parallel.
   - S6: numbers, with an independent recomputation of every new row.
   - S7: figures.
   - S8: appendix integration and removal of the process text.
   - S9 and S10: the main text.
   - S11: the slides and the comparison note. The note is recast (decision 8).
   - S12: verification.
   - S13: second reader, then ask Austin before anything goes to Overleaf.

## 4. How to resume locally

1. `git fetch origin && git checkout theory-upgrade && git pull origin theory-upgrade`.
2. Read `PLAN.md`, `DECISIONS.md`, `NOTATION.md`, this file and `progress/S4_briefs.md`. The briefs file holds the exact S4 instructions: the shared rules, each area's sources and results, the referee task and the wording-target tasks. Give the shared brief to every helper in full, because `PLAN.md` Part 2 requires it.
3. **Builds.**
   - Paper and comparison note: from `slot/manuscript/`, `latexmk -pdf main.tex` and `latexmk -pdf comparison.tex`.
   - Slides: `latexmk -xelatex slides.tex`. They need moloch 2.x; TeX Live 2023's moloch 0.1.0 fails on `frametitle margin left`.
   - Statement files: from `audit/theory_upgrade_2026_10_25/statements/`, `latexmk -pdf -outdir=<scratch> B.tex`. They start with `\input{../tex/preamble}`, which loads the manuscript's packages, macros and numbers.
   - Build into a scratch folder, so that no build product lands in the repository.
4. **Tools,** all print-only:
   - `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/language_scan.py [--doc DIR] [--extra PATH ...] [--pdf FILE ...] [--no-figcode] [--no-doc]` checks rules 1 to 4, the house rules and names;
   - `label_map.py AUX [--before FILE]` maps the labels;
   - `number_scan.py` and `make_numbers.py` check and build the numbers;
   - `scripts/F_figures/make_figures.py [--out DIR]` draws the figures; it needs `mpmath` and `matplotlib`, and finds Fira Sans with `kpsewhich`.
5. **Gate at the end of every stage:** build, read every changed page, run the language scan and judge each hit, and run the numbers scripts if a number moved. Then write `progress/S<n>.md`, commit by explicit paths with a plain message, and push `theory-upgrade`.
6. **Fixed rules.**
   - No tool, agent, model or account names in any committed file or commit message (rule 7). The commits on this branch carry Austin's identity and no co-author lines.
   - No tests: verify by building, running and reading.
   - Never push to Overleaf, never merge into main, and open no pull request.
   - At S13, compare Overleaf with its commit `031d79d` and merge any later edits before a push. The push itself needs Austin's approval.

No job ran on any remote machine, so nothing needs to be cancelled elsewhere.
