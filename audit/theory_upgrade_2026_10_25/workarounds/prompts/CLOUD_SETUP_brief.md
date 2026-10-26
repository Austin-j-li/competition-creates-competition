# Brief: set up the cloud run of the paper update

You set up infrastructure. You do not do the paper update itself and you do not edit the manuscript.

## Goal

Austin wants the update of his paper, planned in `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/plan/PLAN.md`, to run as Claude-only cloud work. It runs in Claude Code's cloud (Claude Code on the web, reachable from the Claude desktop app) on his Claude account 1, a Max x20 subscription. That account is already logged in, both in the desktop app (`/Applications/Claude.app`) and in the local `claude` CLI under its default configuration (`~/.claude`; do not set `CLAUDE_CONFIG_DIR`). The work must keep running while his Mac is closed. The project's virtual machine is unreachable, so the cloud work rests only on GitHub (`Austin-j-li/competition-creates-competition`), Overleaf and Claude's cloud.

Read first:
- `PLAN.md`, in particular Part 3, "Where the work runs".
- `STAFFING_local.md` beside it.
- The repository's `CLAUDE.md`, `AGENTS.md` and `README.md`.
- `slot/README.md`, for the build and the numbers pipeline.

## Hard limits

- Do not touch Austin's working tree at `/Users/austinli/Projects/competition-creates-competition`. It sits on branch `slot-revision` with many uncommitted changes that are his. Do all Git work in a separate worktree, for example `/Users/austinli/Projects/ccc-theory-upgrade-worktree`. You may only read the main tree, plus the folder `audit/theory_upgrade_2026_10_25/`, which you copy from.
- Push exactly one new branch, `theory-upgrade`, to `origin`. Do not push any other branch. Do not touch `main`. No merge, no pull request, no force-push. Never push to Overleaf (`overleaf/slot` is a separate Git working copy with an Overleaf remote; leave it alone).
- Do not handle secrets. If a step needs a credential (for example an Overleaf Git token), stop that step and list it for Austin, with the exact place he enters it.
- Do not log out of, log in to, or switch any Claude account.
- No tool, agent, model, session or account names in any committed file or commit message. Write commit messages as plain descriptions of the content.
- No tests. Verify by running things and reading their output.
- Do not start any stage of the paper update beyond the smoke test in Step 4.

## Step 1. The work branch

1. Create the worktree on a new branch `theory-upgrade` from local `slot-revision` HEAD (487619f). Those committed commits are not on GitHub yet, and pushing them with the work branch is intended. Do not include the side-branch commit 80804f0 (branch `t3/remove-result-status-vocabulary`); PLAN.md S0 records it.
2. Copy the study folder into the worktree at `audit/theory_upgrade_2026_10_25/`, in this layout. Remove every model, agent, tool, session and account name from file names and contents.

| Committed path | Source in the main tree (under `audit/theory_upgrade_2026_10_25/`) |
|---|---|
| `SCAN.md` | `SCAN.md`; the "How the scan was done" table and every mention name roles ("scan referee 1", "scan referee 2", "reviewer") |
| `scan/` | `raw/astra_A3_A5_reduction.md`, `raw/sol_generality_A1_A2_A6_A8.md`, `raw/opus_conflation.md`, `raw/sonnet_downstream.md`, renamed `reduction_A3_A5.md`, `generality_A1_A2_A6_A8.md`, `conflation.md`, `downstream.md`; leave out the prompt files |
| `WORKAROUNDS.md` | `WORKAROUNDS.md` |
| `referee/W1.md` … `W5.md` | `workarounds/raw/W1_astra_check.md` … `W5_astra_check.md` |
| `referee/second_opinion.md` | `workarounds/raw/WORKAROUNDS_fable_review.md` |
| `referee/computations/W1/` … `W5/` | `workarounds/scratch/ccc_wa2/W*/astra/` |
| `solvers/W<i>_<letter>.md` | `workarounds/raw/W<i>_<model>.md`, using the letter map below |
| `solvers/computations/W<i>_<letter>/` | the matching solver scratch folders under `workarounds/scratch/ccc_wa2/` |
| `plan/PLAN.md` | `plan/PLAN.md`; already role-based, so check it |
| `plan/lens_theory.md`, `lens_maintext.md`, `lens_delivery.md` | `plan/PLAN_theory.md`, `PLAN_maintext.md`, `PLAN_delivery.md`; turn their staffing passages into the role names of PLAN.md |
| `plan/progress/README.md` | new: how each stage writes `S<n>.md` (what was done, what was checked, open items, next stage) |
| `plan/DECISIONS.md` | new: PLAN.md Part 8 as a form, with each decision, its recommendation and an empty answer line. The S1 gate reads it |
| `plan/progress/S0_setup.md` | new: what this setup did, and that `slot/manuscript/` equals the Overleaf working copy at 69c25f4 except line 1 of `sections/02_model.tex` (check with `diff -r`, and record any other difference) |

Leave out `prompts/`, `RUN_LOG.md`, `STAFFING_local.md` and anything else not listed.

Letter map for solvers, used everywhere, including inside the referee reports, `WORKAROUNDS.md` and the second opinion:

| Source name | Letter |
|---|---|
| sol | A |
| opus | B |
| kimi | C |
| fable | D |
| sonnet | E |
| muse-wonder | F |
| opus-takeover | G |
| `W4_opus_primitive_condition.json` | H |

Rewrite references such as "Sol 2", "Opus C1", "the Opus takeover" and "Kimi 3" as "Solver A 2", "Solver B C1", "Solver G" and "Solver C 3". "Astra" as the referee becomes "the referee"; "Fable" as the second opinion becomes "the second reader".

3. Then grep the committed tree with word boundaries, case-insensitive, for the following names, and fix or justify every hit: GPT, Astra, Sol, Opus, Sonnet, Fable, Haiku, Kimi, Muse, Claude, Codex, OpenAI, Anthropic, agent, subagent, T3, account, session. "Sol" can occur inside "solution", and "agent" can be an economic agent: judge each hit.
4. Save the full mapping and the grep output in a local, uncommitted report at `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/plan/SETUP_REPORT_local.md`.
5. Commit with a plain message (for example "Add the theory-upgrade study, plan and referee reports") and push `theory-upgrade` to `origin`.

## Step 2. The cloud environment

Find the current way to define a Claude Code cloud environment for this repository on account 1. Check the Claude Code documentation, `claude --help`, and the desktop app's Claude Code settings. The environment needs:
- **Network:** the default trusted package hosts plus GitHub. Add `git.overleaf.com` only if Austin later supplies a token.
- **A setup script.** It must install what the build and the pipeline need: TeX Live with latexmk, pdfLaTeX and XeLaTeX, `newtx`, `natbib`, the packages that `main.tex`, `slides.tex` and `comparison.tex` load, and Python 3 with every package that `audit/slot_manuscript_2026_10_23/scripts/` and `figures` import. Read the imports to get the list. Fonts for `make_figures.py` and `slides.tex`: see `lens_delivery.md` on the hard-coded font path.
- **Environment variables:** none required. An optional `OVERLEAF_GIT_TOKEN` is for Austin to enter himself, later, if he wants the cloud to pull from or push to Overleaf.

If you can create the environment yourself (CLI, or desktop app automation that you can drive reliably), do it. Otherwise write click-by-click instructions for Austin with every value to paste. Put the setup script in the work branch at `plan/cloud_setup.sh` and give it a neutral header comment.

## Step 3. The routine

Create a scheduled cloud routine on account 1 that advances the update without the Mac. Use the Claude Code scheduling feature for cloud agents; if headless creation works, `claude -p` with the default configuration can drive it. The routine:
- runs every two hours on branch `theory-upgrade` in the environment of Step 2;
- uses Claude Opus 5.5 (`claude-opus-5-5`) as the session model.

Its prompt says, in substance:
1. Read `audit/theory_upgrade_2026_10_25/plan/PLAN.md`, `plan/DECISIONS.md` and every file in `plan/progress/`.
2. If `DECISIONS.md` has no answers, write nothing and stop.
3. If `plan/progress/LOCK` exists and is less than three hours old, stop. Otherwise write `LOCK` with the time and the stage name.
4. Run the next pending stage, or one pending S5 package, following PLAN.md's rules and gate. Staffing:
   - the mathematics writer and prose writer are Opus 5.5 at maximum effort;
   - the referee is a fresh-context Opus 5.5 helper that did not write the text;
   - the referee for proof O1 and for the A5 package is Fable 5.1 (`claude-fable-5-1`);
   - the production assistant is Sonnet 5.5 (`claude-sonnet-5-5`);
   - the second reader in S13 is Fable 5.1.
5. Every brief to a helper states the four language rules of PLAN.md Part 2 in full.
6. End by writing `plan/progress/S<n>.md`, deleting `LOCK`, committing with a plain message and pushing `theory-upgrade`.
7. Never push to Overleaf. Never merge into `main`. Stop before the Overleaf step of S13 and write a note asking Austin for approval.

Save the exact routine prompt in the local, uncommitted file `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/plan/ROUTINE_PROMPT_local.md`. Do not put it in the repository.

If the routine cannot be created headlessly, give Austin exact steps in the desktop app.

## Step 4. Smoke test

Start one cloud session on account 1, in the environment, on branch `theory-upgrade`. Use the CLI's remote-session option if it exists, or a one-time run of the routine with a smoke-test prompt. The session must:
1. build `slot/manuscript/main.tex`, `slides.tex` and `comparison.tex` with their documented commands;
2. run `make_numbers.py` and `number_scan.py` as `slot/README.md` describes;
3. run `make_figures.py` if its font fix is not needed yet, or report the font failure;
4. write the results to `plan/progress/S0_smoke.md`, commit and push.

It must change nothing else.

## Report

Append to `SETUP_REPORT_local.md`:
- what exists now: the branch URL, the environment name, the routine name and schedule, and the smoke-test session link or id with its result;
- what Austin must do himself, in order;
- anything that failed.

Your final reply must be at most 250 words: the same points in short form.
