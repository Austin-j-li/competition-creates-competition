# Spec: readability pass on the main deck, locked to the website

Status: READY FOR TAKEOVER AGENT. Rev. 2, 9 November 2026.
Wording owner: Muse Code (this spec's author). The implementer
owns code, builds, and git state. The implementer does not own words.
Normative appendix: `audit/wording_pass_2026_11_09/EXACT_CHANGES.md`.
Background only: `audit/wording_pass_2026_11_09/DISCUSSION.md`.
Handoff note: `/tmp/ccc-wording-handoff-2026-11-09.md` (if present).

## Wording ownership (read first)

- `EXACT_CHANGES.md` is final. Apply each “To” text verbatim.
- Do not paraphrase, shorten, or “smooth” any “To” text.
- Do not coin a new name for any object in the term ledger.
- If a “To” text cannot fit or a build rejects its form,
  stop on that frame. Quote the conflict in your report.
  Propose no silent substitute. The wording owner rules.
- Author ruling, 9 November 2026: “all yes” on CHECK 1–7.
  Every former `[CHECK]` span now has final text in the appendix.
  Include all of them. See the appendix “Resolved” section
  for the ground of CHECK 4 and CHECK 7.

## Takeover state (verified 9 November 2026, after prior agent stopped)

A prior delegated agent started this spec, then stopped on
the author's order so this takeover could occur clean.
Verified state at stop time. Re-verify each line before you edit:

- Branch `slot-revision` at `12a0df3`, in step with `origin/main`.
  The 3 upstream commits are IN (D1 is done). No merge in progress.
- Uncommitted edits exist in exactly four tracked files:
  `slot/manuscript/slides.tex`, `presentation/content.js`,
  `slot/manuscript/slides_script.md`, `presentation/deck.js`
  (one figure label). Nothing is staged. No new commit exists.
- Form of those edits: the appendix applied in large part.
  All new titles S10–S18 are present in `slides.tex`.
  CHECK 1–7 texts are present in draft form (see next bullet).
- Three clauses in the working tree differ from final wording.
  Replace them with the appendix forms, word for word:
  (a) S14 scope sentence — final: “Let only the mass ratio
  $u$, and with it $M(1/2)$, vary.” Drop the interval
  parenthetical the prior agent added.
  (b) S16 `2k` gloss — final: the “Why $2k$” gloss in the appendix.
  (c) S16 hold-fixed sentences — final: the two sentences in
  the appendix starting “The comparison holds $a$…”.
- `presentation/dist/` was rebuilt at 14:32 on 9 November.
  Its hashes matched the working tree at stop time
  (`slides.tex` 981a754b…, `content.js` caa495a6…,
  `slides_script.md` fc0fd914…). Any edit breaks that match.
  You must delete and rebuild `dist/` again (D5).
- `slot/manuscript/slides.pdf` exists from 14:32. Treat it
  as stale the moment you edit. Rebuild it (D5).
- Not yet done at stop time: your three-clause correction,
  full diff audit against the appendix, browser read (D9),
  the lock commit (D7), stage and dry run (D8), live deploy.
- First action: `git diff` audit, file by file, against
  `EXACT_CHANGES.md`. List each appendix item as
  present / differs / absent. Fix “differs” and “absent”.
  Do not restart from clean sources. Do not discard the
  working tree. Its edits are the current draft of record.

## Problem statement

The website deck is correct. A cold reader cannot follow it.

The speaker script repairs each gap in the room.
The website reader reads each slide alone.
Terms arrive before their definitions.
One object carries several names.
Five titles state a strict claim. Their bodies state a weak claim.
Frames 14, 15, and 16 state conditions and stop.
Each lacks its last sentence.

Two system faults compounded the text faults at first draft:

- The local branch sat 3 commits behind `origin/main`.
  Resolved before takeover. See “Takeover state”.
- `presentation/dist/` held a stale 47-frame build.
  The first clean rebuild replaced it with a 57-frame build:
  title, 19 main frames, 37 backup pages.
  Your edits will stale it again. Rebuild clean before the lock.

The author wants one result: raise readability.
Keep full rigour. Make the website carry that one version,
and no other version in reach of the build.

## Solution

Apply the exact wording in the normative appendix
to the 19 main frames, in both copies of the deck.
Then rebuild the website deck from an empty output folder.
Then lock the result by hash and by commit.

The reader gains:

- Each result frame states its conclusion in words.
  The reader no longer supplies the last step.
- Each key term gets its words at first use on its frame.
  A reader who lands mid-deck can still start there.
- Each object keeps one name on every surface in scope.
- Each title keeps its truth condition:
  “weakly”, “can”, “exactly when”, “frequency-weighted”.
- The `/talk/` pages come from one clean build.
  Its provenance record hashes the exact sources in use.

No claim grows stronger in this pass.
No number, symbol set, citation, or result changes.

## Reading of “delete the previous version”

In this spec, “previous version” means the previous
**built** version of the current deck.
The implementer deletes generated output, then rebuilds it.
The implementer deletes no tracked source, no git history,
and no pinned archive.

Delete, before the rebuild:

- All contents of `presentation/dist/`.
- Any staged site tree the implementer creates under `/tmp`
  for this task, once its check is complete.
- Any `presentation.pdf` the implementer creates for a check,
  unless the publish step ships that same file.

Do not delete:

- `slot/manuscript/`, `presentation/` sources, `talk/`,
  `overleaf/`, `handout/`, `docs/` sources.
- The Laplace archive under `/laplace/` and its pinned commit
  in `handout/publish.py`. It is a labelled archive,
  not the current deck.
- Any untracked file the implementer did not create.

If the author meant a tracked source by “previous version”,
the implementer stops and asks. It deletes no source on a guess.

## User stories

1. As a seminar visitor who opens `/talk/` first, I want frame 4
   to gloss “shareholder spread” in words, so that I need
   no speaker to grasp the mechanism.
2. As a cold reader on frame 14, I want the frame to say that
   (H1)–(H3) hold and Proposition 2 applies, so that I know
   why the example sits in the talk.
3. As a cold reader on frame 14, I want decimal thresholds,
   so that I can check `τ(r1) < M(1/2) < τ(r2)` by eye.
4. As a cold reader on frame 15, I want `S` mapped to the news
   in the stock price, so that I know which signal stays fixed.
5. As a cold reader on frame 15, I want flat table rows named
   as flat, so that I do not read the control as a counterexample.
6. As a cold reader on frame 16, I want “research” stated as an
   all-or-nothing success chance, so that I do not read it
   as estimate precision.
7. As a referee who skims titles, I want each title to keep its
   weak or weighted qualifier, so that a skim states no claim
   the paper lacks.
8. As a referee, I want “rival gross profit” with “gross” at
   each use, so that I never read profit net of preparation cost.
9. As a reader who lands on frame 17 from search, I want the
   title to say “strong incumbent (F1)”, “target proceeds”,
   and “net of preparation costs”, so that the title stands alone.
10. As an empiricist on frame 18, I want the empirical moment in
    words, so that I know which average to form and which
    inequality to test.
11. As a listener at the close, I want frame 19 to end on the
    implication, so that the last words answer frame 1.
12. As the author, I want one name per object across slides,
    web copy, and script, so that edits stop drift at the source.
13. As the author, I want the web copy to match the Beamer deck
    word for word outside maths, so that one edit serves both rooms.
14. As the author, I want the old build gone before the new
    build starts, so that no stale page can ship by mistake.
15. As the author, I want a hash record of the shipped sources,
    so that I can prove which text the website shows.
16. As the author, I want the seven CHECK points settled by my
    ruling, with their grounds on record, so that the pass adds
    no false precision.
17. As a future editor, I want the term rules in the deck header,
    so that the next edit keeps the same names.

## Implementation decisions

### D1. Base: upstream already in (verify, do not redo)

- Record `git status` and the current head first.
- Verify `HEAD` contains `12a0df3`. The 3 upstream commits
  are already in: distribution wording; website rebuild;
  S6 incumbent lane plus S11 threshold rule in symbols.
  Merge again only if `origin/main` moved since takeover.
- Never force-push. Never rewrite history.
- Re-read S6 and S11 as built. Apply appendix items
  for S6 and S11 only where upstream leaves them open.
- Every “law” replacement in the appendix is already upstream.
  Skip it. Write “distribution” in any new sentence.

### D2. One master, two copies, one script

Edit order is fixed:

1. `slot/manuscript/slides.tex` — the master deck.
2. `presentation/content.js` — the same words, frame by frame.
3. `presentation` figure labels inside `content.js`,
   plus the matching TikZ labels inside `slides.tex`.
4. `slot/manuscript/slides_script.md` — headings for any
   changed title; the two script-only fixes in the appendix
   (`hidden price`, `sale impact`); word counts if speech changes.
   Speech text does not change unless a heading forces it.

Do not edit `slot/manuscript/numbers.tex`.
It is generated. The appendix uses keys that exist:
`tau_r1`, `tau_r2`, `lambda_B`, `M_half_B`, and the rest.
If a key is absent at build time, stop and report the key.
Do not invent a number. Do not hand-edit the registry display.

### D3. Apply the appendix verbatim, with three exceptions

- Apply each “To” text in `EXACT_CHANGES.md` as written.
  Keep the formal scope of each sentence: weak stays weak,
  “can” stays, “exactly when” stays biconditional.
- Exception 1, layout: if a new sentence overflows its frame,
  first use the frame's own slack (statement size, local spacing
  in use on that frame). Do not shrink a statement past the
  size its neighbours use. If a frame still overflows, stop
  on that frame and report the exact line. Propose a shorter
  form with the same truth conditions. Do not cut a condition
  to fit space.
- Exception 2, maths in titles: `check_deck.mjs` bars a number
  in a headline. Symbols with no decimal (`ρ`, `Δ_T`, `F_1`,
  `λ̄`) follow the present S17 practice. If the check rejects
  the S12 title form, stop and report its exact message.
  Do not weaken the bound to pass the check.
- No held-out text remains. CHECK 1–7 have final forms
  in the appendix (author: “all yes”). See D6.
  Include each one verbatim.

Title outcomes (full table sits in the appendix):
new titles on S10, S11, S12, S13, S14, S15, S16, S17, S18;
new subtitles on S10, S11, S15; new S1 subtitle.
S1–S9 titles and the S19 title do not change.
Each changed title changes `slides.tex`, `content.js`, and the
script heading together, or `check_deck.mjs` will fail the build.

### D4. Order of frames

At takeover, most groups sit in the working tree as a draft.
Audit in this order. Build after each group you touch.
Fix the first failure before the next group starts.

- Group A: S14, S15, S16 (full statement swaps in the appendix).
- Group B: titles and bodies of S10, S11, S12, S17, S18.
- Group C: S1–S4, then S19 as their mirror.
- Group D: S5–S9, S13 bridges.
- Group E: header lock text, global spelling swaps,
  figure-label swaps, script headings.

### D5. Clean rebuild: delete the previous build

Run from the repo root:

```sh
rm -rf presentation/dist
mkdir -p presentation/dist
python3 presentation/build.py
```

What the reader gets, in plain words: the build script
renders `content.js` into the offline `/talk/` pages,
draws the figure curves, attaches the speaker notes,
writes `presentation/dist/index.html`,
`presentation/dist/provenance.json`, and
`presentation/dist/speaker-notes.md`, then runs the
sync check itself. A clean exit from `build.py` means
the web deck matches the Beamer deck. Any drift stops it.

Also rebuild the Beamer deck from `slot/manuscript/`:

```sh
latexmk slides.tex
```

Its `latexmkrc` selects XeLaTeX for `slides.tex`.
The result is `slot/manuscript/build/slides.pdf`
(or the path the build log names). Read the log.
An undefined control sequence, a missing figure, or a
missing registry key fails this gate.

Manual `node presentation/check_deck.mjs` after a green
build adds no information, since the build runs it.
Run it once only to quote its exit code in the report.

### D6. Resolved economics: CHECK 1–7 (author “all yes”)

All seven items have final text in the appendix.
Include each one verbatim. Do not re-derive them.

- CHECK 1 (S14): only $u$, and with it $M(1/2)$, varies.
- CHECK 2 (S14): include the $r_0$ sentence.
- CHECK 3 (S15): A.2 tag and exact-fall formula.
- CHECK 4 (S16): the “Why $2k$” gloss. Ground in the appendix.
- CHECK 5 (S16): λ-observability sentence.
- CHECK 6 (S16): class-$L$ success abstains.
- CHECK 7 (S16): hold $a, k, \rho, \beta$ fixed; prior $1/2$.
  Ground: the B12 first-order condition. In the appendix.

Three of these sit in the working tree in longer draft form.
“Takeover state” names them. Replace those three forms
with the appendix forms. Report CHECK 1–7 as included.
Quote the CHECK 4 gloss and CHECK 7 sentences in your report.

### D7. The lock

“Locked in” means all five items hold at once:

1. Clean build: `python3 presentation/build.py` exits 0
   from an empty `presentation/dist/`.
2. Beamer build: `latexmk slides.tex` exits 0 in
   `slot/manuscript/`.
3. Hash match: each SHA-256 in
   `presentation/dist/provenance.json` for
   `slot/manuscript/slides.tex` (as the build records it),
   `presentation/content.js`, and
   `slot/manuscript/slides_script.md` equals a fresh
   `sha256sum` of the same file in the working tree.
   If the build records a source under a different path key,
   quote that key. A source with no hash entry fails the lock.
4. One commit: a single new commit on the working branch,
   after the upstream merge. It names only the files this
   pass changed. Suggested subject:
   “Raise main-deck readability and lock the web deck to it”.
   The body lists: frames changed, titles changed,
   CHECK 1–7 as included (author “all yes”), build results.
   Stage files by name. Never `git add -A`.
   The repo holds many untracked audit folders. None enters
   this commit except the three files in
   `audit/wording_pass_2026_11_09/`.
5. Staged site check (D8). Live deploy only under D8 rules.

Record the lock in the final report:
commit hash, the three source hashes, frame count (57),
and the build commands with exit codes.

Do not push unless the publish step in D8 needs it
and succeeds. Report push state either way.

### D8. The website carries the new version

The publish path serves `presentation/dist/` under `/talk/`
and the brief at the root. Use stage mode first:

```sh
python3 handout/publish.py --stage-only /tmp/ccc-stage-wording
python3 handout/publish.py --dry-run
```

Check the staged tree by eye and by search:

- `talk/index.html` exists. Its title lines carry the new
  S14, S15, S16 titles. Search the staged HTML for the old
  S14 title text. Zero hits outside `/laplace/`.
- `talk/provenance.json` matches the lock hashes in D7.
- The palette scan inside `publish.py` passes.
  It runs as part of staging. A purple hit fails the run.

Deploy rule: run the full `python3 handout/publish.py`
(with no flags) only if all of these hold:

- The working tree is clean after the D7 commit.
- `origin/main` is an ancestor of `HEAD`.
  `publish.py` enforces this itself. Obey its refusal.
- The dry run exits 0.

If any item fails, do not force a deploy.
Report: “staged and checked at PATH; live site unchanged;
blocker: …”. Never state that the live site carries the new
deck without a successful deploy command in the log.
After a successful deploy, fetch
`https://competition.dealextract.org/talk/` and confirm
the S14 title text in the response. Quote that line.
Delete `/tmp/ccc-stage-wording` after the checks.

### D9. Use the deck as a reader (no new tests)

The seam for this pass is the rendered deck itself.
Do not add test files, fixtures, or frameworks.
Do not edit `check_deck.mjs` or `build.py` to pass.

After the clean build:

```sh
setsid -f python3 -m http.server 8766 --bind 127.0.0.1 --directory presentation/dist </dev/null >>/tmp/ccc-talk.log 2>&1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8766/
```

Then, in a real browser at `http://127.0.0.1:8766/`:

- Step through S1, S4, S10, S12, S14, S15, S16, S17, S18, S19.
- Read each new title. Note any title that wraps to two lines.
- Read S14, S15, S16 cold. State each frame's point in one
  sentence in the report. That sentence is the acceptance test.
- Run `DECK.selfCheck()` and `DECK.audit()` in the console.
  `audit()` must return an empty list. Quote both outputs.
- Press `?`, `O`, `N`, `G` once each. Each panel must open.
  Follow one backup link (S13 to B2) and its Back control.

Also render the Beamer PDF pages for the ten frames above
to images and read them. Note overflow, a rule merged into
a title, or a label collision. Compilation success alone
does not clear a frame.

Stop the server that this task started. Leave no other
process running.

### D10. Failure conduct

- A check failure names the drift. Fix the copy at fault.
  `slides.tex` wins on words. Never edit the check.
- A missing registry key stops the frame. Report the key.
- A type or build error in a touched file goes to zero
  before the task ends. Claim “pre-existing” only with the
  same error shown on the pre-merge tree.
- Keep a plain log of: command, exit code, first error line.
  The final report quotes that log. No log, no claim.

## Testing decisions

- Good check here = outside behaviour: the rendered page,
  the browser view, the staged tree, the hash record.
  Source diffs alone prove nothing about readability.
- Existing seams, in order: `presentation/build.py`
  (renders and runs the sync check), `latexmk slides.tex`,
  the browser console seams `DECK.selfCheck()` and
  `DECK.audit()`, `handout/publish.py --stage-only/--dry-run`.
  One seam per claim. Add no new seam.
- Prior art: the build has run the sync check on each build
  since `check_deck.mjs` entered the repo. Frame order,
  titles, links, registry keys, rounded numbers, words,
  timings, and notes all compare there.
- The author's standing rule bars new tests of any kind.
  This spec adds none. It uses the program as a consumer:
  build it, open it, read it cold, stage it.

## Acceptance checklist

The task is done only when each line is true:

- [ ] `HEAD` contains `12a0df3`; no force action.
- [ ] Diff audit done; all appendix “To” texts in place verbatim,
      including CHECK 1–7; the three takeover clauses corrected.
- [ ] `slides.tex`, `content.js`, script headings agree
      on every changed title.
- [ ] Clean `build.py` exit 0; `latexmk` exit 0.
- [ ] Ten frames read as images and in the browser;
      wraps and overflows listed, or “none” stated.
- [ ] `DECK.audit()` returns an empty list (quoted).
- [ ] Previous `presentation/dist/` deleted before rebuild;
      fresh `provenance.json` hashes match the tree.
- [ ] One commit, files named, hash reported.
- [ ] Stage and dry run pass; old S14 title absent
      from the staged `/talk/` tree.
- [ ] Live state stated true: deployed with proof,
      or unchanged with the exact blocker.
- [ ] Final report: frames changed, titles changed,
      CHECK 1–7 included (CHECK 4 and 7 quoted),
      commands and exit codes, server stopped, stage folder deleted.

## Out of scope

- Backup frames B1–B17, except a main-frame link label.
- The research brief (`handout/sections/*`), its figure axes,
  and the built front page. Its five renames wait for a
  later pass. See `DISCUSSION.md`, brief section.
- The paper (`slot/manuscript/main.tex`, sections, appendix).
- All numbers, the registry, `numbers.tex`, figure curves,
  figure geometry, layout, fonts, and the theme.
- New results, new citations, new frames, frame reordering.
- The Laplace archive, its pinned commit, `/laplace/` routes.
- README minute and frame counts, except a one-line note
  in the report if the build log contradicts them.

## Further notes

- Write in the deck's present voice: specific subjects,
  concrete verbs, scope beside each claim.
  Sound sentences stay. The appendix marks them “Keep verbatim”.
- The S17 title is the one long title. Judge it on the render.
  A two-line title there beats a short title with a false scope.
- Speech timing: title edits do not change speech lengths.
  If a heading change alters a timing line, the check fails.
  That failure means a copy error. Find it.
- The three spec files in `audit/wording_pass_2026_11_09/`
  (`DISCUSSION.md`, `EXACT_CHANGES.md`, this file) travel
  with the lock commit. They are the record of the pass.
- Hand back with the acceptance checklist filled in.
  List any line left unchecked as unfinished work.
  Do not mark the pass done with a red line open.

