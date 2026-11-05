# Role brief, phase 0: the profile dossier (Opus A)

Read `CORE_BRIEF.md` in this folder first. It gives the goal, the settled decisions and the asset paths.

## Your task

Write a factual dossier about Austin's research assets. Several agents read it as their starting map. Two of them, Muse and GPT Pro in the web chat, cannot open the repositories and depend on it completely.

**Do not propose research ideas.** The dossier must be neutral, so that it does not anchor the brainstorm. Describe what exists, what state it is in, and what it makes possible as data or as tools. Do not say what Austin should do.

## Output

`/home/uctpiaj/work/Projects/competition-creates-competition/audit/jmp_search_2026_10_30/phase0/DOSSIER.md`. Keep it to at most 10 pages and 4,000 words of Markdown. Two agents wait for it. Cite a path for each fact that comes from a file.

## Sections

1. **Person and timeline.** PhD 2024 to 2029, market in fall 2029, business schools worldwide, solo job-market paper. Fields on the CV. Earlier research and work experience, in brief.
2. **Supervisors.** Alex Gorbenko (primary) and Brian Healy (secondary). Use web search to list their main papers. For each paper, give the title, the journal and year, and one sentence on its question and method. Mark any entry you cannot verify as "unverified". Brian Healy appears on the CV as the supervisor of quantitative industry work, so his academic publication list may be short or empty. A short list is an acceptable answer. Never fill it with guesses. From Alex's collection instructions and voice notes in `/home/uctpiaj/work/Projects/sec-auction/ref/`, summarize what questions Alex wants the sale-process data to answer. Read the `.docx` with `python-docx` or `pandoc`, and the PDF with `pdftotext`.
3. **CCC, the theory paper.** The model, the main results, the empirical predictions and the open items. Read `overleaf/slot/sections/` in the project. Write 1 to 2 pages in economic words.
4. **Informal bids, the joint structural paper.** The model, the estimator, the state of the code and the study, and the planned data. Read `HMC_sim/Informal_bids/README.md`, `SPEC.md`, the newest report in `reports/`, `HMC_sim/talk_reading_group/structure-plan.md` and `HMC_sim/Informal_bids_a1/README.md`.
5. **The sale-process ledgers.** What one ledger records (sheets and fields), the deals done, the state of the pipeline, its scale-up plan and its cost. Read `sec-auction/README.md`, the extraction instruction, `_dev/STATUS.md` and `_dev/ALEX_ALIGNMENT.md`. Say which fields can measure bidder entry, the timing of contacts and NDAs, informal and formal bids, and process type.
6. **Other data and tools.** WRDS tables with verified access (see the core brief), the ThetaData options archive (read `/mnt/rdss/austin/data/README.md`), the 8 case files in `empirical/private/`, and the options and futures research on the CV.
7. **Other collaborations.** The Borda nonresponse project with Stefan Feuerriegel (`/home/uctpiaj/work/Projects/borda-nonresponse-bounds/README.md`) and the HMC metric study with Sam Livingstone. One paragraph each.
8. **The literature tracker.** The private GitHub repository `Austin-j-li/research-feed` may show what Austin reads. Inspect it with `gh api repos/Austin-j-li/research-feed/readme` and `gh api repos/Austin-j-li/research-feed/contents/`. Do not clone it. Summarize what it covers.
9. **Constraints.** Solo job-market paper, the joint papers with Alex, the time to fall 2029, and the storage rules for data.

## Rules

- Read-only. Write only the dossier file.
- Use web search only for the supervisors' publications. Do not use the shared `vm_browser`.
- Do not spawn subagents. Do not commit. Do not contact anyone.
- Plain language. Short sentences. No ideas and no recommendations.
