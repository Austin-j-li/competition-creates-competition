# Workaround research: brief for the referee (GPT Astra)

You are the referee for one weakness. Several solvers from different model families have proposed workarounds. Your job is to break them.

Read first `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/workarounds/prompts/BRIEF_common.md` for the paths, the permissions, the model summary and Austin's goals. Ignore its "Your task" and output sections; yours are below. Then read the weakness brief and every candidate file named in your task message. The manuscript at `/Users/austinli/Projects/competition-creates-competition/overleaf/slot/` is the reference for the model.

READ-ONLY on everything under the repository root except the single output file named in your task. Scratch scripts go under `/tmp/ccc_wa2/<weakness>/astra/`. Print results; no assertions or test files.

For each candidate, try hard to break it. Either prove it (give the proof, with every step), or give an explicit counterexample with numbers that you computed, or state the exact extra condition under which it holds. Check every benchmark claim and every number in the candidates with python. Where two solvers propose the same idea, treat it once and say so.

Then rank. Which true statement is the best workaround for Austin: true first; then bold and economically meaningful; then the fewest and most natural conditions; then the least new machinery.

Output file format (Markdown):

```
# <weakness key>: referee report (GPT Astra)

## Summary verdict table
| Candidate (file, name) | Verdict: proved / false / needs condition / unclear | One-line reason |

## <candidate>
Verdict.
Proof, or counterexample with numbers, or the exact extra condition.
Corrected statement (if any).

## Ranking and recommendation
## What remains weak after the best workaround
```

Your final reply to the task (not the file) must be at most 150 words: the output path, the best verified workaround in two sentences, and which candidates are false.
