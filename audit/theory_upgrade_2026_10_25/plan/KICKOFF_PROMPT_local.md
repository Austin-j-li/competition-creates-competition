# Kickoff and resume prompts for the cloud sessions (local only; never committed)

Use these in the Claude project "competition" (account 1), in a session on branch `theory-upgrade`, with Claude Opus 5.5.

## Kickoff prompt (first session)

```
You coordinate the update of the order-slot paper in this repository. Work on branch theory-upgrade (git fetch origin; git checkout theory-upgrade). Read, in full, audit/theory_upgrade_2026_10_25/plan/PLAN.md, then plan/DECISIONS.md and every file in plan/progress/. PLAN.md is the authority on order, rules and gates.

First, the smoke check (stage S0 preflight). In slot/manuscript/ run: latexmk main.tex; latexmk -xelatex slides.tex; latexmk comparison.tex. From the repository root run: python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/make_numbers.py, then number_scan.py in the same folder, then audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py. If TeX Live or a Python package is missing, install it inside this session if you can (apt-get or pip), and record exactly what was missing. Do not change the project's settings or environment variables, and never print a credential. Write the results to audit/theory_upgrade_2026_10_25/plan/progress/S0_smoke.md. Delete the build products, commit only that report with a plain message, and push theory-upgrade.

Then check plan/DECISIONS.md. If Austin has not answered, stop: tell him in plain words that the update waits for his answers, and list the decisions with their recommendations.

If the decisions are answered, carry out the stages of PLAN.md in order, one at a time, starting with what remains of S0 and then S2. End every stage at the plan's gate: build, read every changed page, run the language scan and judge each hit, run the numbers scripts if a number moved, write plan/progress/S<n>.md, commit with a plain message, push theory-upgrade. Then continue to the next stage while you have room. When a stage is too large for the rest of this session, stop at a clean gate, so the next session can resume from the report.

Staffing (you are the coordinator). The mathematics writer is a helper on Claude Opus 5.5 at maximum effort. The independent referee is a fresh-context helper that did not write the text under review: Claude Opus 5.5, or Claude Fable 5.1 for proof O1 and for the A5 research package. The prose writer and integrator is Claude Opus 5.5. The production assistant (figures, numbers code, labels, slides, comparison note) is Claude Sonnet 5.5. The second reader in S13 is Claude Fable 5.1. Spawn at most six helpers at a time, and helpers do not spawn helpers. A referee never reviews its own text.

Every helper brief states these rules in full:
(1) No status labels anywhere: no "analytical", "computer-assisted", "numerical diagnostic", "certified", or "open" as a status. A proof may name its method as mathematics.
(2) No defensive writing: scope sits inside the claim, a condition is a hypothesis stated once, and there are no caveats, hedges, reassurance or paragraphs that end on a limitation.
(3) No development-log writing: the paper reads as written once, with no narration of its own changes and no process words (registry, script, exercise, checker, certificate, run, verified, file names, keys, "calibration B"). Comparative statics across strengths are fine.
(4) The example is neutral: never "the benchmark"; its results are corollaries, at most three in the main text.
Also: "I", numbers only through \reg, the style guide in audit/slot_revision_2026_10_24/STYLE_GUIDE.md except its status rules, the two-point preparation cost unchanged, and no tool, agent, model or account names in any committed file or commit message.

Never push to Overleaf. Never merge into main, and open no pull request. Before the Overleaf step of S13, stop and ask Austin. Write no tests; verify by building, running and reading. At the end of each turn, tell Austin in a few plain sentences what was done, what was checked, and what comes next.
```

## Resume prompt (any later session)

```
Resume the update of the order-slot paper on branch theory-upgrade. Read audit/theory_upgrade_2026_10_25/plan/PLAN.md in full, plan/DECISIONS.md, and the latest report in plan/progress/. Then continue with the next pending stage, under the same rules, staffing and gates as before: Opus 5.5 writes; a fresh Opus 5.5 helper referees, or Fable 5.1 for proof O1 and the A5 package; Sonnet 5.5 does production; Fable 5.1 gives the final read. The four language rules of PLAN.md Part 2 go in full into every helper brief. End every stage at the gate (build, read, scan, numbers, report, commit, push). Never push to Overleaf, never merge into main, and stop before S13's Overleaf step. Finish each turn with a few plain sentences for Austin.
```
