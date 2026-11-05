# Brief: the end-to-end plan to update the order-slot paper

Three planners work in parallel, each from a different lens. Each reads everything below, then writes a complete end-to-end plan, going deepest on its own lens. The coordinator merges the three plans into one for Austin, the single author, so cover every stage at least briefly and flag anything you think another lens might miss.

READ-ONLY on the whole repository except your one output file. Do not edit, create or delete anything else, and run no git command that changes state. Do not write or run tests.

## Read (all paths absolute)

Repository root: `/Users/austinli/Projects/competition-creates-competition`

1. The decisions so far, in `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/`:
   - `WORKAROUNDS.md` (revised after the second opinion): what each result can claim, its conditions, the formal statements.
   - `SCAN.md`: the generality table (Part 1), the reduction lemma (Part 2), the vocabulary and notation list (Part 3), the proposed structure (Part 4), downstream consumers (Part 5), the earlier change list (Part 6).
   - `workarounds/raw/W1_astra_check.md` to `W5_astra_check.md`: the referee reports, the authority on what is true, with full proofs.
   - `workarounds/raw/WORKAROUNDS_fable_review.md`: the second opinion.
2. The manuscript master: the Overleaf working copy `/Users/austinli/Projects/competition-creates-competition/overleaf/slot/` (`main.tex`, `sections/`, `appendix/`, `numbers.tex`, `figures/`, `comparison.tex`, `slides.tex`). Its mirror: `/Users/austinli/Projects/competition-creates-competition/slot/manuscript/`, and `slot/README.md` for the build and the numbers workflow.
3. The numbers and figures pipeline: `/Users/austinli/Projects/competition-creates-competition/audit/slot_manuscript_2026_10_23/` (`BRIEF.md`, `LEDGER.md`, `LABELS.md`, `TEAM_RULES.md`, `registry/*.csv`, `scripts/`, especially `scripts/_coordinator/make_numbers.py`, `number_scan.py`, `scripts/F_figures/make_figures.py`, and the exercise folders P1 to P5, XP1 to XP5).
4. House rules: the repository `CLAUDE.md` and `AGENTS.md`; the manuscript style guide `/Users/austinli/Projects/competition-creates-competition/audit/slot_revision_2026_10_24/STYLE_GUIDE.md`.

## What Austin has decided or leans toward

- **Structure rule.** Prove each result at the most general level its proof supports. Sharpen it with a named economic condition where a stronger claim needs one. Present the worked example (point-mass classes h = 10 and ℓ = 1, uniform incumbent) as a special case that checks the conditions, gives the numbers and figures, and supplies insights only it can show. Stronger results with few assumptions where possible; the example for visualization and extra insight.
- **One named condition per result, not one shared condition.** Outbidding (strong-type ownership level, widening winner gap); uniform incumbent with separated classes and affordability, or the balance condition (coexistence on one stretch); cheap research (research persisting along a path); the reserve condition (rising entry component of the price gap). Two conditions bracket the preparation cost (about 4.99 to 6.4), with the example's 6 inside.
- **Main-text lineup** (four propositions, Gorbenko style: descriptive titles, intuition after each, proofs in the appendix, no lemma, definition or corollary environments in the main text):
  - Section 2: the general model once; the worked example once.
  - Section 3: Proposition 1 (unchanged); the two-numbers idea in prose (the market sees the auction through the spread and the preparation threshold; a stronger incumbent raises both).
  - Section 4: Proposition 2 (general; add the strong type's share of takeovers under outbidding); the worked example with the fixed-information comparison; Proposition 3, quiet and informative markets (general region, the full-purchase stretch with no condition, the whole stretch under its condition), with the worked example, its figure and optionally a new panel of the region in the spread-threshold plane.
  - Section 5: Proposition 4 at prior 1/2 and under the tie rule that lets an indifferent investor mix (research and entry rise with the spread until the cap, not interrupted when weak-type investors sell; strong-type entry rises; ownership level under outbidding; the limit along a path). The worked example's list of equilibria moves out of the proposition into the text and figure note. The research figure is filled in: the recruiting outcome with research at the cap now runs to the entry ceiling.
  - Sections 6 and 7: little change (complementary signals extended to general classes; payment rule stays two-value).
  - Section 8: prose, with appendix statements: the weighted price test at any prior; orders predict the winner (sign general, widening under outbidding); counts and prices identify informed trading; announcement returns.
- **Language rules (override STYLE_GUIDE.md where they conflict).** No result-status labels anywhere in the manuscript, main text or appendix ("analytical", "computer-assisted", "numerical diagnostic", "certified", "open" as a status), in titles, sentences, table notes or captions; STYLE_GUIDE.md sections 2.4 and 2.7 on status are superseded. Proof methods may appear inside appendix proofs as the method, never as a label. No defensive writing: each result stated positively with its scope inside the claim; conditions are hypotheses stated once, not apologies; no caveat or reassurance paragraphs, no hedges, no pre-emptive referee answers, no paragraph ending on a limitation. GPT-written prose follows the same rule. Every stage gets a language-compliance check, and the delivery ends with a sweep of the main text, appendix, captions, comparison.tex and slides.tex. No development-log writing: the paper reads as written once, with no trace of its revision history or production. No narration of changes to the paper ("now", "no longer", "new", "updated", "revised", "corrected", "replaces", "in this version", "previously"), no announced upgrades, no process or pipeline words (registry, script, exercise, checker, certificate, run, verified, file names, keys, "calibration B", weakness codes), no bookkeeping about what was checked. Comparative statics across strengths stay; proof methods inside appendix proofs are stated as mathematics. (All three rules added mid-run by steering messages.)
- **Fixed.** The preparation cost stays two-point (zero with probability ρ, c_H otherwise); no general cost law, no c_H rename. Single author, "I". The manuscript carries no result-status labels (analytical, computer-assisted, and so on). Numbers print only through `\reg{key}`.
- **Model team.** GPT (Sol, Astra) writes and reviews rigorous mathematics. Opus and Sonnet do volume, integration and prose; Muse is not available, so Claude composes manuscript prose under the style guide. Fable gives one second opinion at the end. Claude work is balanced across two accounts.
- **Version control.** Pull the author's latest Overleaf edits first. Work on a new local branch in `overleaf/slot` and in the parent repository. Never push to Overleaf or GitHub without Austin's approval. Do not stage Austin's own uncommitted changes in the parent repository (handout/, docs/, presentation/, slot/study_guide/).
- **Verification.** No tests. Build the PDF and read every changed page; run the registry scripts (make_numbers, number_scan: zero missing keys, no typed decimals); rerun the affected numerical exercises and their checkers; the `verify-ccc` skill exists for this.

Still open, to be marked as decision points in your plan with a recommendation: deleting the stray `ty` at `overleaf/slot/sections/02_model.tex:1`; the region panel; filling the research figure; scope trims (Corollary A.2 at other priors; identification in Section 8); A.7 extended, A.9 skipped, A.5 left on the uniform family; keeping 1 + u = e; consumers limited to comparison.tex and slides.tex; whether the numbers and figure scripts should write to the Overleaf master or to the mirror.

## Your plan file

Write a Markdown plan with these parts:

1. **Summary** (at most 300 words, plain language).
2. **Stages in dependency order.** For each stage: goal; files and labels touched; the source for every new or changed statement (which Astra report section or memo item); who writes it and who checks it (model family); how it is verified; acceptance criteria; rough size (lines or pages).
3. **File-by-file change list** for your lens, down to the proposition, lemma, figure or registry key, with line references in the current master.
4. **Label and numbering map**: every label that is added, removed or renumbered, and every consumer that cites it.
5. **Risks and traps**: things likely to go wrong, with mitigations.
6. **Decision points for Austin**, each with your recommendation.
7. **What you think the other two lenses might miss.**

Your final reply must be at most 150 words: the output path, the number of stages, and the three points you most want the coordinator to weigh.
