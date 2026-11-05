# Brief: condense study-guide chapters to a page budget

The full study guide (`study_guide/chapters/*.tex`, 352 pages) must become a short guide of no more than 50 pages.
You condense the chapters assigned to you. Write each one to `study_guide/short/chapters/<same file name>.tex`.

## What to keep
- The chapter title and its `\label`. Keep the same `\section` labels for sections you keep.
- A `chapterplan` box of two or three lines.
- Every `paperresult` box (the exact statement of each result of the paper), with a short proof:
  the key steps in a compact `align*`, with `\why{...}` only where a step is not routine. Merge trivial steps.
- The intuition for each result, in one short paragraph or one `intuition`/`keyidea` box.
- The one or two `watchout` points that matter most for the chapter.
- A `chaptersummary` box of three to five sentences.
- Figures and tables that the chapter needs (the three figures `beliefs`, `coexistence`, `research` stay).

## What to cut
- All `checkyourself` boxes and the `\answersection` with all answers.
- Most analogies (keep at most one per chapter, two sentences).
- Repeated reminders of definitions, extreme-case tests beyond one per result, long motivation, repetition.
- Derivation steps that are pure arithmetic; show the step that carries the idea.

## Rules
- Do not add a claim that the long chapter does not make. Do not change any result, formula, hypothesis or `\reg{...}` key.
  Copy formulas from the long chapter; do not rederive them in new notation.
- Cross-chapter `\ref`: refer to chapters by `Chapter~\ref{ch:...}` (chapter labels stay). Avoid `\ref` to section or equation
  labels in other chapters, because those may not exist in the short guide. Say "Chapter 2" style references instead.
- Writing: short sentences, active voice, simple words, no "clearly"/"obviously". Keep the existing macros and boxes from `preamble.tex`.
- Do not write or run tests. Do not edit any file outside your assigned `short/chapters/` files.

## Page budget and check
Build one chapter: `cd study_guide && ./build_short.sh <chapter file name without .tex>`.
The PDF is `build/short_<name>/only.pdf`. It has 2 front pages (title and contents) plus the chapter.
So the chapter's page count = `pdfinfo build/short_<name>/only.pdf | grep Pages` minus 2.
The chapter must build without errors and must not exceed its budget. Aim to end well inside the last page.
Report: file written, final page count, and what you cut.
