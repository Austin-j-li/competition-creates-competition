# Team rules: search for an EGJ-like microstructure (22 October 2026)

Read this file first. Then read `BRIEF.md` in this folder. The brief has priority if the two differ.
The task ledger is `LEDGER.md` in this folder. It lists each workstream, its output, and its checker.

## 1. Scope

- This study is **exploratory**. Nothing here edits the paper.
- Team folder: `audit/microstructure_search_2026_10_22/` (below, "the team folder").
- Write only in the team folder:
  - memos in `memos/<STEM>.md`;
  - scripts and their outputs in `scripts/<STEM>/`.
- Do not edit or create files anywhere else. Do not commit. Do not push.
- Read the paper only at the pinned commit (the revised paper):
  - `git -C overleaf/paper show 01bd5d6:main.tex`
  - `git -C overleaf/paper show 01bd5d6:online_appendix.tex`
- Do not edit `overleaf/paper/` or `overleaf/paper-revision/`.
- You may read every file of the earlier studies in `audit/discrete_exploration_2026_10_21/` and
  `audit/alex_meeting_2026_10_21/`. Do not edit them. You may copy their scripts into your own folder.
- Do not hand any part of your task to others.
- Do not use a web browser, web search, or web fetch, unless your workstream is L1. Only L1 fetches papers.
  For citations, use the verified records in `audit/alex_meeting_2026_10_21/memos/LIT_extracts.md`,
  `audit/alex_meeting_2026_10_21/memos/Q2_discrete_literature.md`,
  `audit/discrete_exploration_2026_10_21/memos/D_literature.md` and, when it exists, `memos/L1_survey.md`
  in the team folder. Mark every other source "unverified".
- Other members work at the same time. You may read their memos in `memos/`. Do not edit their files.

## 2. Model decisions that apply to every workstream

- **Reading N.** Nature draws the challenger's quality class `j ∈ {H, L}` with prior `π`. The value comes
  from `G_j`. The investor sees the class. Preparation reveals the value. The benchmark is the special case
  of point masses at `ℓ` and `h` with `π = 1/2`.
- **`c_L = 0`.** The low-cost type prepares at zero cost. Then the entry floor `ρ` holds at every belief.
- **Order menus.** Each theory workstream states its menu: buy-only `{0, 1}` or two-sided `{−1, 0, 1}`.
- **Notation.** `λ` is the probability that the informed investor is present. Do not use `λ` for any other
  object. The trading cost is `k`.

## 3. Shared objects (paper, Sections 2 to 4; incumbent value `R ~ U[0, r]`, reserve `p`)

```
t_0 = p(1 − p/r)                 t_H = r/2 + p²/(2r)          t_L = ℓ − (ℓ² − p²)/(2r)
g_H = h − r/2 − p²/(2r)          g_L = (ℓ² − p²)/(2r)         Δ_T = t_H − t_L = (r − ℓ)²/(2r)   (p < ℓ < r < h)
B_r(μ) = g_L + μ(g_H − g_L)      (challenger's expected gain at posterior μ)
e_r(μ) = ρ·1{B_r(μ) ≥ c_L} + (1 − ρ)·1{B_r(μ) ≥ c_H}   (= ρ + (1 − ρ)·1{B_r(μ) ≥ c_H} when c_L = 0)
P_r(μ) = t_0 + e_r(μ)(t_L − t_0 + Δ_T μ)               (competitive price at posterior μ)
```

Paper benchmark: `h = 10, ℓ = 1, p = 0.5, ρ = 0.25, c_L = 0, c_H = 6, k = 0.02, π = 1/2, r_0 = 1.2,
r_1 = 3, r_2 = 3.6` (the Laplace scale `b = 2` does not apply to discrete noise). Check every formula above
against the pinned paper before you rely on it.

## 4. Base model for the theory workstreams

The EGJ-style three-point model: noise `Z ∈ {−1, 0, 1}`, each with probability 1/3 unless your workstream
changes the weights; order flow `X = q + Z`; the informed investor is present with probability `λ`;
competitive price `P = E[V_T | X]`; the challenger sees the price (the paper's assumption; EGJ's decision
maker sees the flow, and in these models the two carry the same information when the price is strictly
monotone in the posterior). The earlier results for this base are in
`audit/discrete_exploration_2026_10_21/memos/A_three_point.md` and `A_bruteforce.md`. Start from them.

In each memo, state your menu, your noise law, your presence or liquidity device, and why.

## 5. Status labels and evidence

- Use one label on each result: **analytical**, **computer-assisted**, **numerical diagnostic**,
  **conjecture**, **open**.
  - analytical: a complete proof in the memo.
  - computer-assisted: a proof whose finite steps use exact (rational or interval) computation.
  - numerical diagnostic: floating-point evidence on stated grids.
- Show every derivation. Do not write "it is easy to show".
- A documented failure is a result. Report it with the same care as a success.
- State the equilibrium concept, the off-path belief rule, and both tie rules (investor and challenger).
- Cite only sources that you verified. Mark all other sources "unverified".
- Do not name AI models, agents, assistants, or tools in memos, scripts, or comments.

## 6. Scripts, CPU, and disk

- No tests of any type. Scripts print results. Scripts with assertions are not allowed.
- Python: `/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python` (numpy, scipy, mpmath,
  and the standard library with `fractions`). Do not install packages.
- **CPU.** Another team runs heavy numerics on this machine. The whole team shares 8 CPU slots.
  - Run every script that can take more than 60 seconds through the slot wrapper:
    `bash audit/microstructure_search_2026_10_22/scripts/_slots/run_slot.sh .venv/bin/python <script> ...`
  - One slot covers one process. Do not use `multiprocessing`, thread pools, or `&` background jobs
    inside a slot. For parallel work, start more wrapped processes. Each one waits for a free slot.
  - Use at most 3 slots at the same time.
- **Disk.** The root disk is almost full. Keep outputs under `/home/uctpiaj/work`. Do not write to `/tmp`.
  Keep each `scripts/<STEM>/` folder under 20 MB. Save summaries, not raw rows.
- You may reuse the earlier solvers (for example `audit/discrete_exploration_2026_10_21/scripts/A_bruteforce/`).
  Copy what you need into your own scripts folder. Do not edit the originals.

## 7. Memo format

Theory memos have these sections, in this order (literature memos use the format in their task):

1. Question.
2. Setup (menu, noise law, presence or liquidity device, equilibrium concept, belief rule, tie rules).
3. Results: each with its status label and its full derivation.
4. The scorecard of BRIEF §2, one table per candidate setup.
5. Numerical example (benchmark values where possible).
6. Open issues.
7. Plain summary, 300 words at most.

Write a skeleton of the memo early and fill it in as you work, so that partial work survives.

## 8. Writing style

Write in simple, controlled English:

- Sentences of 25 words at most. One topic in each paragraph.
- Active voice where possible. Simple verb forms. Simple words ("use", not "utilize").
- Use the same word for the same thing in the whole memo.
- Use vertical lists for complex text.
- Use LaTeX-style math (`$...$`) in memos.

## 9. Final reply

When you finish, reply with at most 250 words:

- the memo path and the script folder;
- each main result, one line each, with its status label;
- what failed or stays open;
- any claim from the brief that you refuted.
