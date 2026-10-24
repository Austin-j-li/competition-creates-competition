# Team rules: the order-slot manuscript (23 October 2026)

Read this file first. Then read `BRIEF.md` in this folder. The brief has priority if the two differ.
The ledger is `LEDGER.md` in this folder. It lists each workstream, its output, and its checker.
All paths are relative to the repository root `/home/uctpiaj/work/Projects/competition-creates-competition`.

## 1. Scope and files

- Team folder: `audit/slot_manuscript_2026_10_23/` (below, "the team folder").
- Write only in the places your task names:
  - proof packages: `proofs/<STEM>.tex` (a standalone LaTeX article that compiles) and a short summary
    `memos/<STEM>.md`;
  - check memos: `memos/X<STEM>_check.md`;
  - scripts and run logs: `scripts/<STEM>/`;
  - registry rows: `registry/<STEM>.csv`;
  - writers only: the files in `overleaf/competition_slot/` that their task names.
- Do not edit or create files anywhere else. Do not commit. Do not push.
- Read the Laplace manuscript only at the pinned commit:
  - `git -C overleaf/paper show 01bd5d6:main.tex`
  - `git -C overleaf/paper show 01bd5d6:online_appendix.tex`
- Do not edit `overleaf/paper/`, `overleaf/talk/` or the earlier study `audit/microstructure_search_2026_10_22/`.
  You may read every file of the earlier study and copy its scripts into your own folder.
- Do not hand any part of your task to others.
- Do not use a web browser, web search or web fetch. For citations, use the verified records in
  `audit/microstructure_search_2026_10_22/memos/L1_survey.md` and the existing `references.bib`.
  Mark every other source "unverified" in your memo, and do not cite it in a document.
- Other members work at the same time. You may read their files. Do not edit them.

## 2. Model decisions

- The model is the order slot of BRIEF §2: unit orders `{−1, 0, 1}`, presence probability `λ`, liquidity
  probabilities `(β, 1 − 2β, β)`, `0 < β ≤ 1/3`, competitive price `P = E[V_T | X]`, the challenger sees the price.
- `c_L = 0`. Classes `j ∈ {H, L}`, prior `π`, values from `G_j`; the benchmark uses point masses at `ℓ` and `h`.
- `λ` is only the presence probability (or, in the research section, the research intensity that sets it).
- The trading cost is `k`. The research cost parameter is `a`; the research cap is `λ̄`.
- Calibration B (BRIEF §3) is the benchmark: `1 + u = e`, `β = 0.294655`, `λ = uβ/(1 + uβ)`.

## 3. Shared objects (Laplace manuscript, Sections 2 to 3; `R ~ U[0, r]`, reserve `p`)

```
t_0 = p(1 − p/r)                 t_H = r/2 + p²/(2r)          t_L = ℓ − (ℓ² − p²)/(2r)
g_H = h − r/2 − p²/(2r)          g_L = (ℓ² − p²)/(2r)         Δ_T = t_H − t_L = (r − ℓ)²/(2r)   (p < ℓ < r < h)
B_r(μ) = g_L + μ(g_H − g_L)      τ(r) = (c_H − g_L)/(g_H − g_L)
e_r(μ) = ρ + (1 − ρ)·1{B_r(μ) ≥ c_H}          (c_L = 0)
P_r(μ) = t_0 + e_r(μ)(t_L − t_0 + Δ_T μ)
```

Check every formula above against the pinned manuscript before you rely on it. Report any difference.

## 4. The proof standard

Every proof follows BRIEF §5. In short:

1. State the equilibrium as an explicit tuple.
2. List the conditions.
3. Check each condition against the fixed tuple. A deviation holds the candidate price function and entry
   rule fixed. Do not assume the conclusion. Do not write "it is easy to show", "by symmetry" or
   "similarly" without the computation.
4. Prove uniqueness with bounds that hold for every profile.
5. Every hypothesis is a strict inequality with its benchmark margin in a margins table.

## 5. Status labels and evidence

- One label on each result: **analytical**, **computer-assisted**, **numerical diagnostic**, **open**;
  declarations carry **input**.
  - analytical: a complete proof in the proof package.
  - computer-assisted: a proof whose finite steps use exact rational or interval arithmetic in a named script
    with a run log.
  - numerical diagnostic: floating-point evidence on stated grids.
- A documented failure is a result. Report it with the same care as a success.
- State both tie rules (investor and challenger) and say which results depend on them.
- Do not name AI models, agents, assistants or tools in any memo, script, comment or document.

## 6. Scripts, CPU and disk

- **No tests of any type.** Scripts print results. Scripts with assertions are not allowed. Do not add test
  files or test frameworks.
- Python: `/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python` (numpy, scipy, mpmath,
  matplotlib, and the standard library with `fractions`). Do not install packages.
- **CPU.** The whole team shares 8 CPU slots. Run every script that can take more than 60 seconds through
  `bash audit/slot_manuscript_2026_10_23/scripts/_slots/run_slot.sh .venv/bin/python <script> ...`.
  One slot covers one process. Use at most 2 slots at the same time.
- **Disk.** The root disk is almost full. Keep outputs under `/home/uctpiaj/work`. Do not write to `/tmp`.
  Set `TMPDIR` to your own scripts folder if a tool needs a temporary directory. Keep each `scripts/<STEM>/`
  folder under 20 MB.
- **LaTeX.** `latexmk` and `pdflatex` are in `/home/uctpiaj/work/.local/bin`. Compile into a `build/`
  folder beside the source: `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build <file>.tex`.
  The slides use `-xelatex`.

## 7. Registry rows

Columns: `key, value, display, status, source_script, run_log, note`. One row per printed number.
Keys use lowercase letters, digits and underscores, for example `entry_r1_B`. Write the `value` with at
least 10 significant digits or as an exact rational. Write `display` exactly as a document prints it.

## 8. Controlled English

- Sentences of 25 words at most (20 in procedures). One topic in each paragraph, 6 sentences at most.
- Active voice where possible. Simple verb forms: commands, infinitives, simple present, past and future.
- Avoid -ing forms except in technical names. Avoid the perfect tense.
- Use the same word for the same thing in the whole document.
- Simple words: "use", not "utilize"; "start", not "commence"; "before", not "prior to".
- Noun clusters of 3 words at most. Do not drop "the", "a" or "this".
- Vertical lists for complex text.
- Mathematics is exempt from the word counts. Proofs may use longer displays.

## 9. Anti-defensive writing

Advance the claim directly. Say what is true, what the model shows and what the proof does.

- Lead each paragraph with its point, not with a caveat.
- State scope positively: "Section 5 studies research with a cap", not "we do not study research without a cap".
- Keep a limitation when it affects validity, interpretation, scope or correct use. Write it once, calmly,
  in the section where it matters. Do not repeat it in the abstract, introduction and conclusion.
- Replace stacked hedges with precision. If uncertainty is real, name its source. Keep the status labels:
  they are precision, not hedges.
- Avoid: "we do not claim", "this is not to say", "it is worth noting", "to be clear", "of course",
  "the goal is not X but Y", reflexive "rather than" contrasts, and self-criticism with no information.
- A weaker result is a trade-off with a stated condition. Do not turn it into a verdict on the model.
- Do not invent facts, mechanisms or advantages to sound stronger.
- Final pass: delete each sentence that exists only to answer a hypothetical objection.

## 10. Final reply

When you finish, reply with at most 250 words:

- the paths you wrote;
- each main result, one line each, with its status label;
- what failed or stays open;
- any claim from the brief or from an earlier memo that you refuted.
