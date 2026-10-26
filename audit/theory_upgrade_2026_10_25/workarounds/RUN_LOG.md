# Workaround research: run log (25 October 2026)

Replaces the interrupted workflow run wf_a6ceccda-4c2. The study runs as T3 delegated tasks from the coordinator thread, across every frontier model enabled in T3 Code (Grok, Cursor, OpenCode, Antigravity and Pi are disabled there).

Briefs: `prompts/BRIEF_common.md` (solvers), `prompts/W1.md` to `prompts/W5.md` (weaknesses), `prompts/CHECK_common.md` (referee).
Outputs: `raw/W<i>_<model>.md`. The cached Opus W4 candidate from the old run is `raw/W4_opus_primitive_condition.json`.

## Stage 1: solve (launched)

| Weakness | Solvers (all at max effort) | Output files |
|---|---|---|
| W1 coexistence interval | GPT-6.1 Sol (priority tier); Opus 5.5 (account claude2); Kimi K3.1 Pro | W1_sol, W1_opus, W1_kimi |
| W2 ownership | GPT-6.1 Sol; Opus 5.5 (account claudeAgent); Muse Wonder Full 1.0 | W2_sol, W2_opus, W2_muse-wonder |
| W3 research branch end | GPT-6.1 Sol; Opus 5.5 (claude2); Fable 5.1 (claudeAgent) | W3_sol, W3_opus, W3_fable |
| W4 winner gap | Kimi K3.1 Pro; Sonnet 5.5 (claude2); cached Opus (old run) | W4_kimi, W4_sonnet, W4_opus_primitive_condition.json |
| W5 symmetric tests | GPT-6.1 Sol; Opus 5.5 (claudeAgent); Muse Wonder Full 1.0 | W5_sol, W5_opus, W5_muse-wonder |

Task client ids: `ccc-wa2-solve-<W>-<model>-v1`. A Muse Spark 1.3 solver on W4 was cancelled minutes after launch at Austin's request (no Muse Wonder 1.0 or Spark; Muse Wonder Full only where needed) and replaced by Sonnet 5.5.

Muse phase-out (Austin, same day: his Muse usage will run out soon). Both Muse Wonder Full solvers (W2, W5) were told to save partial work to their output files and stop. When each one ends, an Opus 5.5 solver continues from its notes under `prompts/TAKEOVER_muse.md`: W2 on claude2, output `raw/W2_opus-takeover.md`; W5 on claudeAgent, output `raw/W5_opus-takeover.md`. Client ids `ccc-wa2-takeover-<W>-opus-v1`.

## Stage 2: referee (per weakness, when its solvers finish)

GPT-6 Astra, reasoning effort max, service tier default (off the fast tier). Brief `prompts/CHECK_common.md`. Output `raw/W<i>_astra_check.md`. Client id `ccc-wa2-check-<W>-v1`.

Status: all solvers finished. Astra referee tasks launched for W1, W3, W5, W4 and W2, in that order, each when its solvers ended.

## Stage 3: memo and second opinion

Opus 5.5 (claude2) reads the five referee reports and the candidates and writes `../WORKAROUNDS.md` (intuition first, formal appendix last) under `prompts/MEMO.md`. Then one Fable 5.1 pass (claude2) as second opinion, written to `raw/WORKAROUNDS_fable_review.md`.

## Scope

No manuscript edit, no commit, no push. The stray `ty` in overleaf/slot/sections/02_model.tex:1 stays until Austin decides.

## Progress

- All five Astra referee reports written (`raw/W<i>_astra_check.md`).
- `../WORKAROUNDS.md` written by Opus 5.5 (claude2), about 7,300 words.
- Fable 5.1 (claude2) second-opinion review launched: fidelity to the Astra reports, judgement, the general-then-special-case structure Austin proposed, and readability. Output `raw/WORKAROUNDS_fable_review.md`. Client id `ccc-wa2-fable-review-v1`.
- Fable review written (`raw/WORKAROUNDS_fable_review.md`): nine material and seven small fidelity issues, all omitted qualifiers; no refuted statement recommended. Key points: the research continuation needs prior 1/2 and the mixing tie rule; the sharper claims need four different conditions, not one; two of them bracket the preparation cost (4.9875 ≤ c_H ≤ 6.4).
- Memo revision launched: Opus 5.5 (claudeAgent), client id `ccc-wa2-memo-revise-opus-v1`, edits `../WORKAROUNDS.md` only.
- Memo revised (Opus, claudeAgent): plain summary on top, sixteen fidelity fixes, "Conditions, one per result", benchmark-story section, revisions list.

## Stage 4: end-to-end update plan (launched)

Brief `prompts/PLAN_brief.md`. Three Opus 5.5 planners at max effort, read-only, each writes one file in `../plan/`:
- theory and proofs, `PLAN_theory.md` (claude2), client id `ccc-plan-theory-opus-v1`;
- main text and story, `PLAN_maintext.md` (claude2), `ccc-plan-maintext-opus-v1`;
- numbers, figures and delivery, `PLAN_delivery.md` (claudeAgent), `ccc-plan-delivery-opus-v1`.
The coordinator merges them into `../plan/PLAN.md` for Austin.
- Scratch from /tmp/ccc_wa2 (solvers and referees) and /tmp/ccc_wa (interrupted run) archived to workarounds/scratch/.
- Three plans written (plan/PLAN_theory.md 14 stages, PLAN_maintext.md 13, PLAN_delivery.md 12); merged by the coordinator into plan/PLAN.md (14 stages S0 to S13, nine open proofs, eight decisions for Austin).

## Stage 5: cloud setup

- Austin moved the update to Claude-only cloud sessions in the existing Claude project "Competition" (account 1), with no routine.
- The setup agent (GPT-6 Astra, at Austin's request; the first run was interrupted, finished at medium effort) pushed branch `theory-upgrade` at 26895f3: 143 study files, scrubbed of model and tool names (zero hits on a word-boundary scan), with solver letters A to H.
- The kickoff and resume prompts are in `plan/KICKOFF_PROMPT_local.md` and the setup report in `plan/SETUP_REPORT_local.md`, both local only.
- No cloud session was started: the CLI cannot target an existing project and branch together.
