# Team rules: exploratory study of discrete trading (21 October 2026)

Read this file first. Then read `BRIEF.md` in this folder. The brief has priority if the two differ.
The task ledger is `LEDGER.md` in this folder. It lists each workstream, its output, and its checker.

## 1. Scope

- This study is **exploratory**. The paper keeps Laplace noise as its benchmark. Nothing here edits the paper.
- Team folder: `audit/discrete_exploration_2026_10_21/` (below, "the team folder").
- Write only in the team folder:
  - memos in `memos/<STEM>.md`;
  - scripts and their outputs in `scripts/<STEM>/`.
- Do not edit or create files anywhere else. Do not commit. Do not push.
- Read the paper only at the pinned commit:
  - `git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:main.tex`
  - `git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:online_appendix.tex`
- Do not read or edit `overleaf/paper-revision/`. Do not edit `overleaf/paper/`.
- Do not hand any part of your task to others.
- Do not use a web browser, web search, or web fetch, unless your workstream is D1 or a report check.
  Only those workstreams fetch papers. For citations, use the verified records in
  `audit/alex_meeting_2026_10_21/memos/LIT_extracts.md` and, when it exists, `memos/D_literature.md`.
  Mark every other source "unverified".
- Other members work at the same time. You may read their memos in `memos/`. Do not edit their files.

## 2. Model decisions that apply to every workstream

- **Reading N.** Nature draws the challenger's quality class `j ∈ {H, L}` with prior `π`. The value comes
  from `G_j`. The investor sees the class. Preparation reveals the value. The benchmark is the special case
  of point masses at `ℓ` and `h` with `π = 1/2`.
- **`c_L = 0`.** The low-cost type prepares at zero cost. Then the entry floor `ρ` holds at every belief.
- **Buy-only orders** (`q ∈ {0, 1}`) are the starting point. Item C.1 studies two-sided orders.
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

Paper benchmark: `h = 10, ℓ = 1, p = 0.5, ρ = 0.25, c_H = 6, b = 2, k = 0.02, r_0 = 1.2, r_1 = 3, r_2 = 3.6`.
The paper uses `c_L = 1`. This team uses `c_L = 0` (Section 2). Check every formula above against the
pinned paper before you rely on it.

## 4. The two discrete base models

1. **Three-point model.** Noise `Z ∈ {−1, 0, 1}`, each with probability 1/3 ("equal noise"). Order flow
   `X = q + Z`. The prior work is in `audit/alex_meeting_2026_10_21/` (see the brief, Section 0).
2. **Discrete-Laplace model.** `Z = G_1 − G_2`, with `G_1, G_2` independent geometric counts of unit noise
   orders, `P(G = n) = (1 − a)aⁿ`. Then `P(Z = z) = (1 − a)/(1 + a) · a^{|z|}`, `a = e^{−1/b}`.
   The candidate results in the brief, Section 0, are **not verified** until workstream B reports.
   If your work uses one of them, check it yourself and say so.

In each memo, state which base model you modify and why.

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
    `bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh .venv/bin/python <script> ...`
  - One slot covers one process. Do not use `multiprocessing`, thread pools, or `&` background jobs
    inside a slot. For parallel work, start more wrapped processes. Each one waits for a free slot.
  - Use at most 3 slots at the same time.
- **Disk.** The root disk is almost full. Keep outputs under `/home/uctpiaj/work`. Do not write to `/tmp`.
  Keep each `scripts/<STEM>/` folder under 20 MB. Save summaries, not raw rows.
- You may reuse the prior solver in `audit/alex_meeting_2026_10_21/scripts/V_discrete_check/`.
  Copy what you need into your own scripts folder. Do not edit the original.

## 7. Memo format (brief, Section 4.1)

Each memo has these sections, in this order:

1. Question.
2. Setup (base model, what changes, equilibrium concept, belief rule, tie rules).
3. Results: each with its status label and its full derivation.
4. What it recovers or loses relative to the Laplace paper (Props. 1–3, A.3–A.10, Sections 5–6).
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
