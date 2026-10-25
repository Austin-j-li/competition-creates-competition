# Plan for the theory upgrade: main text and story

Read PLAN.md first. Its stage order, staffing roles, cloud-only execution, decision gate and delivery restrictions override the earlier alternatives in this lens. All study-relative source paths below are relative to `audit/theory_upgrade_2026_10_25/`.

25 October 2026. Lens: the main text (Sections 1 to 9, abstract, title), its figures and captions, and its vocabulary. The plan still covers every stage, more briefly outside this lens. All of it is a proposal; nothing in the repository was changed.

Inputs: `WORKAROUNDS.md` (revised memo, cited as "memo"); `SCAN.md`; the five referee reports `referee/W1.md` to `W5.md` (cited as "W1 ref" to "W5 ref", with section titles); `referee/second_opinion.md` (cited as "review"); the master `overleaf/slot/` at 69c25f4 (cited as `file:line`); the numbers and figures pipeline under `audit/slot_manuscript_2026_10_23/`; `audit/slot_revision_2026_10_24/STYLE_GUIDE.md` as overridden by the coordinator's language rules. Benchmark values quoted here were recomputed from the closed forms and agree with the referee reports (r_A 1.394, r_F 1.467, r_N 1.748, r_S 2.124, r_C 3.593; research starts at 1.501, reaches the cap at 1.678, floor-entry research ends at 2.167 with research 0.234; challenger-takeover share of class H 6/11 at r_0 and 0.831 at r_1).

Assignments use the roles in PLAN.md.

---

## 1. Summary

The upgrade turns the middle of the paper from statements about one example into general results, and keeps the example for numbers, figures and the insights only it shows. The main text keeps four propositions with descriptive titles, intuition after each, and proofs in the appendix.

Proposition 1 does not change. Section 3 gains a short subsection: the investor, market makers and the challenger see the auction only through the target-payoff spread and the preparation threshold, and a stronger incumbent raises both. Proposition 2 gains one sentence: when class H outbids the incumbent, ownership rises and class H wins a larger share of challenger takeovers. Proposition 3, retitled "Quiet and informative markets", states coexistence as a region in the two numbers, the stretch with a sure purchase as one interval along any path, and the whole stretch as one interval when the spread outpaces the erosion of class H's margin over the high cost (a uniform incumbent with separated classes meets this). Proposition 4 becomes general at an even prior with the default tie rules: research and entry rise with the spread until the cap, the weak class's selling does not interrupt them, ownership rises when class H outbids, and cheap research keeps the equilibrium on one interval along a path. The benchmark's list of equilibria moves to the text and to a filled research figure, where recruiting research at the cap runs to the entry ceiling. Section 8 becomes four general predictions in prose.

Thirteen stages run in dependency order: decisions, a statement freeze refereed before any prose, vocabulary, appendix, numbers, figures, main-text results, introduction and abstract last, build and language sweep, consumers, one second opinion, sync. The main risks are wording that drifts from the appendix statements, scope qualifiers lost in compressed sentences, and the coordinator's language rules, which make `comparison.tex` a redesign rather than a sweep.

---

## 2. Stages in dependency order

### 2.0 Language rules: acceptance criteria for every stage

These override `STYLE_GUIDE.md` where they conflict (its 2.4 status-in-title and 2.7 status-per-cluster rules are void). They apply to the main text, appendix, captions, table notes, `comparison.tex` and `slides.tex`, and to every wording target in this plan.

- **R1 No status labels.** No "analytical", "computer-assisted", "numerical diagnostic", "certified" or "open" as a status, anywhere. Proof methods appear inside appendix proofs as mathematics ("an exact rational computation shows"), never as a label.
- **R2 No defensive writing.** Each result is stated positively with its scope inside the claim. Named conditions are hypotheses, stated once. No caveat or reassurance paragraphs, no hedges ("may" as hedge, "arguably", "it should be noted", "only in the benchmark" as a disclaimer), no pre-emptive answers to referees, no paragraph that ends on a limitation. the mathematics writer-written prose follows the same rule.
- **R3 No development log.** No narration of change when it refers to the paper ("now", "no longer", "new", "updated", "revised", "corrected", "replaces", "in this version", "unlike the earlier draft", "previously"); no upgrade announcements ("this generalizes", "the benchmark restriction is removed"); no process or pipeline words (registry, script, exercise, checker, certificate, run, verified, recomputed, Sturm-count certificates as objects, file names, keys, "calibration B", workstream or weakness codes); no bookkeeping sentences about what was checked. Comparative statics stay ("above the ceiling, orders no longer predict entry").
- **R4 Unchanged.** "I"; numbers only through `\reg{}`; no bold sentences in running text; no tool, reviewers or model names.
- **R5 Structure.** No paragraph opens with a count ("Two numbers summarize..."); no "This section" outside the roadmap; no em dash as connector; four propositions only, and no lemma, definition, corollary or remark environment in the main text.

Sweep, run from `overleaf/slot/` on the files a stage touches, and on all six file groups in Stage 9:

```bash
F="main.tex sections/*.tex appendix/*.tex comparison.tex slides.tex"
grep -n -i -E 'analytical|computer[- ]assisted|numerical diagnostic|certif|\bopen\b' $F                       # R1
grep -n -i -E '\bnow\b|no longer|\bnew\b|updated|revised|corrected|\breplac|in this version|earlier (draft|version|result)|previously|generali[sz]|is removed|upgrade' $F   # R3 history
grep -n -i -E 'registry|script|exercise|checker|certificate|\brun\b|run log|verified|recomput|sturm|calibration b|value at b|\bat b\b|S\(B\)|nolinkurl|\.py|\.log|\.csv|\.json|enclosure|workstream|\bW[1-5]\b|\bX?P[1-5]' $F   # R3 process
grep -n -i -E '\bmay\b|\bmight\b|arguably|should be noted|note that|only in the benchmark|is not needed|does not rise|cannot be weakened|caveat|limitation|admittedly|not only|\bwe\b|\bour\b' $F   # R2
grep -n -E '\\textbf|---' sections/*.tex                                                                    # R4, R5
Review names and voice manually under PLAN.md Part 2; use the first-person singular.
```

Whitelist after reading each hit: "open set", "open interval", "open contest", "open markers"; comparative statics such as "orders no longer predict entry"; the tie-rule phrases "may mix over its best orders" and "may prepare with any probability", which state the rule, not a hedge. Every other hit is fixed. A manual pass then reads the last sentence of every changed paragraph (no limitation endings) and the first (no count openers). Finally a the prose writer pass runs the a plain-language review and `plain-language review` skills over all new prose, formulas untouched.

Baseline at 69c25f4: the main text has no status label; four expository "now" (`04:257`, `05:3`, `05:149`, `06:10`) and one process phrase (`05:103`, "interval enclosures"); two "no longer" that are comparative statics and stay (`01:96`, `08:44`). The appendix has about 100 process hits (A3 13, A4 24, A5 14, A6 16, A7 6, A8 8, A9 22: "calibration B", script and log names, "certificate", "Value at B") and 9 status hits. `comparison.tex` has 56 status hits and 45 process hits, and its framing is version history by design. `slides.tex` has 4 process hits.

### Stage 0. Decisions and setup

- **Goal.** Austin settles the decision points of Part 6; the work starts from his latest Overleaf state on local branches.
- **Files.** `overleaf/slot/` (pull, branch); parent repository (branch).
- **Source.** Brief; memo decisions 1 to 6 and the four new decisions; Part 6 here.
- **Who.** the prose writer and integrator writes a one-page decision sheet in plain economic words (no codes, per Austin's standing preference); Austin decides.
- **Verification.** `git -C overleaf/slot pull`; `git -C overleaf/slot status` clean; `diff -r overleaf/slot slot/manuscript -x .git` lists only the stray `ty` and any edit Austin made since. In the parent repository, stage by explicit path only; `handout/`, `docs/`, `presentation/`, `slot/study_guide/` stay unstaged.
- **Acceptance.** Decisions recorded by the coordinator; work branches exist in both repositories; build directory outside the working copy (`overleaf/slot` has no `.gitignore`, so a `build/` folder there could be committed and pushed): `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/ccc_build main.tex`.
- **Language.** The decision sheet itself follows R2 and R3 in spirit.
- **Size.** One page.

### Stage 1. Statement freeze

- **Goal.** Every changed result has a final formal statement before any prose, and every main-text sentence that states a result maps to one (the crosswalk of Part 3.2).
- **Files.** A statements file in the plan folder (coordinator's choice of name); later copied into A1 to A8.
- **Sources.** Main text: W1 ref "Shared Candidate 1" (eq. 1 and 2), "Solver B 1" (eq. 3 and the wording corrections), "Solver A 2 and Solver C 3" (eq. 4 to 8), "Solver B 2" (balance); W2 ref "Shared Candidate 1" (factorization, entry, fixed incumbent value), "Shared Candidate 2" (level condition, decisive advantage, benchmark verification), "Shared Candidate 3" (takeover composition), "Do the same workarounds cover Proposition 2..."; W3 ref "Shared Candidate 1" sections 1 to 6, "Solver B/Solver D Candidate 3" (IM with C1; CM; I0), "The benchmark", "Ranking and recommendation"; W4 ref "Solver C 1, Solver B 3, and Solver E 1(a)-(b)", "All three solvers: the covariance constants agree", "High-class outbidding"; W5 ref "Shared candidate 1", "Shared candidate 2", "Entry-component trend", "Announcement returns". Memo appendix items W1.1 to W5.5 and "Conditions, one per result".
- **Who.** the mathematics writer drafts the formal statements; the independent referee referees them against its own reports. the prose writer and integrator writes the main-text wording targets (Part 3.1 is the draft); the independent referee reads each target for mathematical fidelity.
- **Open items to settle here.** (i) Whether the uniform-incumbent condition implies the balance condition (my two-line derivation: with X = g_H − c_H ≥ rA and rΔ′ ≥ Δ, (ΔX)′ = Δ′X − AΔ ≥ A(rΔ′ − Δ) ≥ 0; not refereed). If it fails, Proposition 3(c) lists the two conditions as alternatives. (ii) The strictness condition for class H's takeover share: the referee states a positive low-class win probability at the stronger incumbent; the exact condition appears to be a positive low-class win probability at the weaker one, which also covers saturation. (iii) Whether Proposition 4 holds for every β < 1/2 (W3 ref fixes 0 < β < 1/2 for the continuation; the zero-research tuple uses β ≤ 1/3), which decides the footnote at `02:123`. (iv) The exact form of the recruitment margin in Proposition 4(c), which adds the sale profit (ρJ − k)⁺ to the old margin.
- **Verification.** Read-only fidelity pass; each crosswalk row is marked "match", "missing qualifier" or "overclaim".
- **Acceptance.** No overclaim; every qualifier present where the source has it: prior 1/2 and the mixing investor for research; two-sided trade and one target at one strength for the tests; prior below the threshold for the weighted test; prior and slot fixed for the winner trend; τ > π at the path start and attained crossings for benchmark endpoints.
- **Language.** R1 to R3 on the statements (no "generalizes", no status words).
- **Size.** Six to eight pages of statements; the crosswalk.

### Stage 2. Vocabulary and notation freeze

- **Goal.** One word and one symbol per object across main text and appendix (Part 3.6).
- **Sources.** SCAN Part 3 (items and the eight systematic patterns); style guide 2.3 and 2.10; memo W3 (the `\bar r_R` collision).
- **Who.** the prose writer and integrator drafts the glossary; the mathematics writer checks symbol collisions in the appendix proofs; Austin approves the names in decision points 10, 11 and 15.
- **Verification.** Counts of each retired term before and after (grep).
- **Acceptance.** No symbol with two meanings; no object with two names; "the benchmark" for the worked example; "calibration B" gone.
- **Language.** R3 (the glossary drives the removal of "calibration B", "Value at B", "S(B)").
- **Size.** One to two pages.

### Stage 3. Appendix mathematics

- **Goal.** Proofs of every Stage 1 statement, general parts first, benchmark parts after. Other lenses carry the depth; the main text depends on these items:
  - A1: two numbers along a path (spread rises; threshold rises when c_H ≥ g_L; the race in J).
  - A2: the formal two-numbers statement, placed after `lem:trading`; the fix of the equal-posterior paragraph at A2:165 to 170; the opening sentence at A2:7 to 8.
  - A3: the takeover-share sentence of Proposition 2(ii); decisive advantage.
  - A4: Proposition 3's proof (region, sure-purchase interval, condition (c)); the benchmark as a `named` statement "Proposition 3 in the benchmark" with the current table; hand proofs in place of the two root counts (margins 9667/8280 and 937/5520); Corollary A.2 kept as a benchmark statement; the threshold-pair exception at r_A.
  - A5: Proposition 4's proof (continuation, kink, existence, ownership, path); the three-outcome map; the benchmark as a `named` statement "Proposition 4 in the benchmark"; `prop:researchregion` and `rem:researchties` re-anchored off "Proposition 4(b)"; the tie remark gains the abstaining-investor gap (1.748, 2.124] and the partial-preparation tuple; `eq:a5-F` re-derived from the new `eq:research`.
  - A6: one scope sentence for A.5; A.7 for ranked classes with ownership ½·e_H·W_H(F_1).
  - A8: A.11 with the frequency-weighted test, its identity with A.14(iv), and the entry-component split; A.12 with identification at a known prior; A.13 with the sign, the covariance above the ceiling and the trend under outbidding; A.14 with the exact condition; the identity ϑ = M − m at `A8:8` confined to prior 1/2.
  - A9: new rows of `tab:margins`.
- **Who.** the mathematics writer writes proofs; the independent referee referees; the prose writer and integrator integrates the LaTeX and removes process language; the production assistant runs the sweeps.
- **Verification.** Build; a referee read per file; sweep.
- **Acceptance.** Every Stage 1 statement proved; numbering policy of Part 4 kept; R1 and R3 zero hits in the appendix after whitelisting (this alone removes about 100 process phrases).
- **Size.** Fifteen to twenty-five appendix pages touched.

### Stage 4. Numbers

- **Goal.** Every number the new prose prints exists as a registry row with a checker row; `numbers.tex` regenerated in the master.
- **Files.** `audit/slot_manuscript_2026_10_23/registry/*.csv`; exercises P1, P2, P3, P4, P5 and checkers XP1 to XP5; `scripts/_coordinator/make_numbers.py` (writes to `slot/manuscript/numbers.tex` at line 14) and `number_scan.py` (scans `slot/manuscript` at line 9), both repointed per decision 8. Keys in Part 3.5.
- **Sources.** Memo decision 6 list; W1 ref "Consolidated benchmark numerical check"; W2 ref "Benchmark verification"; W3 ref "The benchmark" and "Primitive margins"; my recomputation (front matter).
- **Who.** the production assistant writes exercise code in the existing exact style; a second, independent reader writes the checker rows; the independent referee spot-checks the formulas.
- **Verification.** Run each exercise and checker through its command line; `make_numbers.py` (no display conflicts); `number_scan.py` (zero missing keys, no typed decimals); values printed beside the referee's (read, not asserted); the numerical verification procedure on P1, P2, P3, P4, P5; run manifests as the project rules require.
- **Acceptance.** Zero missing keys; every new key has value, display, source and checker; registry notes updated where meaning changed (`res_rcap` is where research reaches the cap, not where the equilibrium ends).
- **Language.** The registry is internal; the manuscript never names a key or a script (R3).
- **Size.** About 12 new keys; 200 to 400 lines of exercise code.

### Stage 5. Figures

- **Goal.** Research figure filled with three equilibria on a continuous axis; coexistence figure with the region panel (decision 2) and the corrected note; talk versions regenerated; beliefs figure unchanged.
- **Files.** `scripts/F_figures/make_figures.py`: `research_curves` and `fig_research` (lines 526 to 648), a floor-entry research root Q(Δ) solving aQ = ρΔm_Q − k, the positive-part research equation, `fig_coexistence` (line 443) with a region panel; `OUT` (line 35) and the font path `FIRA` (line 39, a Linux path) per decision 8. Output `figures/{coexistence,research}{,_talk}.pdf`.
- **Sources.** Memo "What changes in the benchmark story"; W3 ref "The benchmark" (the IM/C1 outcome list) and "Solver B/Solver D Candidate 3"; W1 ref eq. 1 and eq. 3.
- **Who.** the prose writer and integrator designs and codes; the production assistant reviews rendered PNGs independently; Austin looks before the main text is final.
- **Verification.** Run the script; read its log (each boundary beside its registry display: r_R, the cap strength, r_N, r_Q, r_S, r_C, r_A, r_F); PNG previews; grayscale check; `pdffonts` shows embedded fonts.
- **Acceptance.** Every curve from closed forms; no "equilibrium set not characterized" or "beyond r_N" label (both are status-like statements, R1 and R2); no broken axis; no label touching data; vector PDF, embedded fonts, no in-figure titles, (a)/(b) labels; overlapping lines (zero research and floor-entry research at entry ρ; recruiting and floor-entry research at the cap) distinguished by color and line style.
- **Size.** About 200 lines of plotting code.

### Stage 6. Main text, Sections 2 to 5

- **Goal.** Sections 2 to 5 rewritten to the targets of Part 3.1 and the crosswalk of Part 3.2.
- **Who.** the prose writer and integrator composes under the style guide and R1 to R5; the independent referee reads every sentence that states a result against the frozen statements; a the prose writer pass runs a plain-language review and anti-defensive writing; the prose writer and integrator integrates.
- **Verification.** Build; read every changed page in the PDF; `number_scan.py`; the log has no undefined reference or citation.
- **Acceptance.** Crosswalk rows all "match"; four propositions with descriptive titles, lead-in of two to four sentences, intuition first after each, proofs pointed to once; numbers only through `\reg{}`; sweep clean.
- **Size.** About 250 lines changed; the main text grows by about one page.

### Stage 7. Main text, Sections 6 to 8

- **Goal.** Section 8 in four general predictions; light edits in 6 and 7.
- **Who, verification, acceptance.** As Stage 6; Section 8 depends on the A8 statements of Stage 3.
- **Size.** About 60 lines.

### Stage 8. Introduction, abstract, conclusion

- **Goal.** The tour states the general results first and the benchmark numbers second; the abstract stays near its current length (about 190 words; target at most about 210).
- **Who, verification, acceptance.** As Stage 6, plus a qualifier check of every compressed claim (Part 5, risk 2).
- **Size.** About 70 lines.

### Stage 9. Build, read, verify, and the final language sweep

- **Goal.** One consistent PDF and the release gate.
- **Verification.** `latexmk` in the master; read every changed page; the numerical verification procedure (affected exercises, or the full gate if Austin wants a readiness claim); `make_numbers.py` and `number_scan.py`; all six sweeps of 2.0 over main text, appendix, captions, `comparison.tex`, `slides.tex`; the manual first-and-last-sentence read; the plain-language review and anti-defensive pass on any prose added since Stage 8.
- **Who.** the production assistant runs the build, scripts and sweeps; the prose writer and integrator reads every changed page; the numerical verification procedure runs the numerical gate.
- **Acceptance.** Zero undefined references; zero missing keys; zero non-whitelisted sweep hits; page count noted.
- **Size.** Checks only; the main text and appendix are read in full once (about 70 pages).

### Stage 10. Consumers: `comparison.tex` and `slides.tex`

- **Goal.** Both consumers match the manuscript and the language rules.
- **Files and anchors.** `comparison.tex`: its status column and the sentence at lines 69 to 70 ("Each result carries one status label") go; rows 205 (coexistence), 206 (priors), 207 (research), 215 (empirics) and prose at 219 to 234, 253, 266 to 305, 351 to 358; the version-history framing ("the slot replaces three certified points", line 222) becomes a side-by-side description of two set-ups; references to "Proposition 3(b)" and "Proposition 4" re-anchored; appendix table numbers rechecked. `slides.tex`: F12 (456 to 468), F13 (476 to 484, where "Proposition 4(a)" and "[r_R, r̄_R)" describe the old endpoint), F16 (545 to 550, winners and tests), notation A2 (602 to 640), A8 (747 to 763), A9 (773 to 776); "High class" wording at 465, 753, 829.
- **Who.** the production assistant edits; the prose writer and integrator reviews; the independent referee reads the result rows of `comparison.tex`.
- **Verification.** `latexmk comparison.tex`; `latexmk -xelatex slides.tex`; read each changed page and frame; sweep.
- **Acceptance.** No status labels; no version narration; numbers through `\reg{}`; every cited number of a result exists in the manuscript.
- **Size.** `comparison.tex`: a redesign of its results table and about 150 lines of prose. `slides.tex`: about 60 lines.

### Stage 11. Second opinion

- **Goal.** One the second reader read of the whole manuscript, main text first, against the memo and the crosswalk: fidelity, story, R1 to R5.
- **Who.** the second reader reviews; the prose writer and integrator applies fixes; the independent referee rechecks any changed statement.
- **Verification.** Rebuild and reread every page a fix touches; sweep the changed files.
- **Acceptance.** Every finding fixed or answered in writing.
- **Size.** One review; fixes usually under a page.

### Stage 12. Sync and commit

- **Goal.** Local commits on the work branches with informative subjects; no push.
- **Steps.** Commit `overleaf/slot` by stage (main text, appendix, figures, numbers file, consumers). Commit `audit/` changes (registry, scripts, plan records) in the parent repository by explicit path. The mirror `slot/manuscript/` is a subtree of the Overleaf project: leave it until Austin approves the Overleaf push, then push the master and `git subtree pull` into the mirror, so the two histories stay one.
- **Who.** the prose writer and integrator commits and writes the report; Austin approves any push.
- **Acceptance.** No push without Austin's approval; Austin's uncommitted parent files untouched; report to Austin in plain words.
- **Size.** Five to eight local commits.

Parallel work: Stages 1 and 2 together; after them Stages 3 (the mathematics writer), 4 (the production assistant) and 5 (the prose writer and integrator) together; Stage 6 drafting may start from the frozen statements, but its acceptance waits for Stage 3.

---

## 3. File-by-file change list (main-text lens)

### 3.1 Wording targets

Each target obeys R1 to R5. Notation follows the glossary of 3.6. `\reg{}` keys marked * are new (3.5).

**T-ABS. Abstract** (`main.tex:84–98`). First paragraph unchanged. Second paragraph, about 130 words (abstract about 210 words):

> On an open set of parameters, a stronger incumbent turns an uninformative price into an informative one, with unique trading and preparation outcomes; entry rises, and so does the probability that a challenger from the high class acquires the target. With the information in the price held fixed, a stronger incumbent can only lower entry. A quiet market and an informative one coexist exactly on a region of two numbers, the sensitivity of proceeds to quality and the belief that preparation requires, and incumbent strength moves the economy through that region; in the informative market, entry rises with the sensitivity and then stays constant. When the investor pays for research and the prior is even, research and entry rise together until research reaches its cap. In the strong-incumbent economy, access to prices raises expected target proceeds and acquisition surplus net of preparation costs.

Optional sentence (decision 14), before the last: "When the investor trades in both directions, frequency-weighted price impacts reveal whether prices recruit challengers." Title unchanged.

**T-2.4. Outbidding** (append to `02:225–228`):

> The probability that a prepared challenger of class \(j\) wins against the incumbent distribution \(F\) is \(W_j(F)=\E_j[F(\theta)\1\{\theta\ge p\}]\). Class \(H\) outbids the incumbent when \(W_H(F)=1\): a prepared class-\(H\) challenger then beats the incumbent for sure. Entry in class \(j\) is the probability that the challenger prepares given class \(j\).

Also at `02:54`: "A path is a family of incumbent distributions, each a first-order stochastic strengthening of the one before, with everything else fixed."

**T-2.5. The benchmark** (new `\subsection{The benchmark}\label{sec:example}` at the end of Section 2; merges `02:78–88`, `02:203–204` and `04:77–87`):

> The numbers and figures of the paper come from one benchmark. Its classes are point masses: \(G_H\) puts all its mass on \(h\) and \(G_L\) on \(\ell\), so the class and the value coincide. The incumbent is uniform on \([0,r]\), and an increase in \(r\) strengthens it; for this family I write \(g_j(r)\), \(\DT(r)\), \(B_r\) and \(\tau(r)\). Values, the reserve and strength satisfy [eq:order]. The benchmark sets \(h=\reg{prim_h}\), \(\ell=\reg{prim_ell}\), \(\pi=\reg{prim_pi}\), \(p=\reg{prim_p}\), \(\rho=\reg{prim_rho}\), \(c_H=\reg{prim_cH}\) and \(k=\reg{prim_k}\), and it compares the strengths \(r_0=\reg{prim_r0}\), \(r_1=\reg{prim_r1}\) and \(r_2=\reg{prim_r2}\); money is measured in units of the low value. In the benchmark slot the largest likelihood ratio of an order is \(1+u=\eu\), and the liquidity probability is \(\beta=\reg{beta_B}\), so the presence probability is \(\lambda=u\beta/(1+u\beta)=\reg{lambda_B}\), with \(b=\reg{b_B}\), and the posterior bounds at the prior are \(M(1/2)=\eu/(1+\eu)=\reg{M_half_B}\) and \(m(1/2)=\reg{m_half_B}\). Appendix~\ref{app:parameters} lists these declarations and the arithmetic behind each value.

**T-3.4. What the market sees of the auction** (new `\subsection{What the market sees of the auction}\label{sec:twonumbers}` after `03:141`):

> When the spread is positive and class \(H\) earns more than class \(L\), the investor's orders, the market makers' posteriors and the challenger's preparation depend on the auction only through the target-payoff spread \(\DT\) and the preparation threshold \(\tau\). The spread sets what an informed order earns at each posterior and level of entry, and the threshold sets which posteriors recruit a high-cost challenger. Two auctions with the same spread and the same threshold, and everything else equal, therefore have the same equilibrium orders, posteriors and entry, and with research the same research intensity. Prices add the levels \(t_0\) and \(t_L\), and ownership adds which bidder wins, so ownership results carry class \(H\)'s chance of beating the incumbent.
>
> A stronger incumbent raises both numbers whenever preparation at the high cost does not pay for a challenger known to be in class \(L\). It widens the spread (Proposition~\ref{prop:returns}), and it lowers the low class's profit while it narrows the profit gap between the classes, so a challenger needs a more favorable belief before preparation at the high cost pays. Coexistence in Section~\ref{sec:coexistence} and research in Section~\ref{sec:research} are statements about these two numbers. Appendices~\ref{app:payoffs} and~\ref{app:beliefs} give the formal statements and proofs.

Opens with a condition and actors, not a count (style guide 2.1). The qualifier on the threshold is required: W1 ref "Solver B 1" shows the threshold can fall when it is negative.

**T-P2. Proposition 2** (`04:11–44`). Statement unchanged except one sentence after the display in part (ii):

```latex
If class \(H\) outbids the incumbent \(F_1\), ownership rises, and class \(H\) wins a larger share of the takeovers
that go to the challenger whenever class \(L\) wins against \(F_1\) with positive probability.
```

Source: W2 ref "Shared Candidate 3" (odds (e_H/e_L)(W_H/W_L); strictness qualifier) and "Do the same workarounds cover Proposition 2" (outbidding at F_1 forces it at F_0). Stage 1 may replace "against F_1" by "against F_0", the exact condition including saturation.

**T-P2-OWN. After Proposition 2** (replaces `04:63–67`):

> The additional entry favors the high class, which places a purchase with probability \(b+\lambda\), while the low class places one with probability \(b\). Ownership multiplies entry in class \(H\) by class \(H\)'s chance of beating the incumbent, and a stronger incumbent lowers that chance when class \(H\) can lose. The condition in part~(ii) holds whenever the stronger incumbent leaves the high class a good chance to win, \((1+\rho)W_H(F_1)\ge2\rho W_H(F_0)>0\), and the high class places a purchase more often than not, \(b+\lambda>1/2\). When class \(H\) outbids the incumbent, its chance to win is one at both strengths, so ownership rises with entry in class \(H\); the stronger incumbent then takes wins only from the low class, and the takeovers that go to the challenger shift toward class \(H\). Values and costs alone give outbidding wherever a price recruits when class \(H\) has a decisive advantage: preparation at the high cost pays for a challenger known to be in class \(H\) only against incumbents that it outbids. A price recruits only where class \(H\)'s profit exceeds the high cost, so under a decisive advantage class \(H\) outbids every incumbent against which a price recruits. With point-mass classes and uniform incumbents, class \(H\) has a decisive advantage exactly when \(c_H\ge(h^2-p^2)/(2h)\).

Source: W2 ref "Decisive advantage" (equivalence on the full uniform family).

**T-4.2-OWN. Benchmark check** (replaces the ownership clause of `04:115–117`):

> The benchmark satisfies (H1)--(H3), so Proposition~\ref{prop:ccc} applies, and entry rises from \(\reg{entry_r0}\) to \(\reg{entry_r1_B}\). Class \(H\) outbids every incumbent on the path, because \(h\) exceeds \(r_2\), so high-class ownership rises from \(\reg{own_r0}\) to \(\reg{own_r1_B}\), and class \(H\)'s share of the takeovers that go to the challenger rises from \(\reg{own_share_r0}\)* to \(\reg{own_share_r1_B}\)*. Its high cost also gives class \(H\) a decisive advantage, since \(c_H\) exceeds \((h^2-p^2)/(2h)=\reg{cH_DA_floor_B}\)*: in the whole uniform family, a price recruits only against incumbents that class \(H\) outbids.

This is the benchmark insight that it cannot show an ownership fall (memo, "What changes in the benchmark story", fourth item), stated positively.

**T-P3-LEAD. Lead-in to Proposition 3** (replaces `04:256–270`):

> Between the weak and the strong incumbent of Proposition~\ref{prop:ccc}, two equilibria can hold at the same incumbent. In a quiet market the investor does not trade, the price carries no information, and entry stays at its floor; in an informative market a purchase recruits a high-cost challenger. The two numbers of Section~\ref{sec:twonumbers} decide where both exist: the threshold must lie above the prior and within reach of a purchase, and the spread must be wide enough that a purchase that just reaches the threshold covers the trading cost, yet narrow enough that an order against an uninformative price does not.

**T-P3. Proposition 3** (replaces `04:272–283`):

```latex
\begin{proposition}[Quiet and informative markets]\label{prop:coexistence}
Let the classes satisfy the class ranking~\eqref{eq:classes}, and let \(0<\pi<1\), \(0<\rho<1\), \(k>0\) and a slot
\((\lambda,\beta)\) be given. Take incumbent distributions with a positive spread \(\DT\) and \(g_H>g_L\), and write
\(\tau\) for the preparation threshold.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
\item A quiet market and an informative market coexist if and only if
\[
\pi<\tau\le M(\pi),\qquad \frac{k}{1-\tau}\le\DT\le\frac{k}{\rho\max\{\pi,1-\pi\}}.
\]
The informative equilibrium is then unique: the low class abstains, only a purchase recruits a high-cost
challenger, and entry is
\[
\rho+(1-\rho)\min\Bigl\{\frac{(1-\pi)\,b\,\DT}{k},\;b+\pi\lambda\Bigr\},
\]
which rises with the spread while class \(H\) mixes between a purchase and abstention and is constant once
class \(H\) buys for sure.
\item Along a path of such distributions, the strengths at which a quiet market coexists with an informative
market in which class \(H\) buys for sure form an interval, and every other strength with coexistence lies below it.
\item Suppose that class \(H\)'s gross profit exceeds \(c_H\) at the weakest incumbent of the path and that the
product of the spread and \(g_H-c_H\) rises weakly along the path. Then the strengths with coexistence form an
interval. A uniform incumbent on \([0,r]\), \(r\in[r_0,r_2]\), satisfies this condition
when every low-class value lies in \([p,r_0]\), every high-class value is at least \(r_2\), and class \(H\)'s mean
value exceeds \(r_2\) by at least \(c_H\).
\end{enumerate}
\end{proposition}
```

Sources: (a) W1 ref "Shared Candidate 1", eq. 1 and 2, uniqueness under the default challenger rule; (b) W1 ref "Solver B 1", eq. 3 and its corrected gap wording (gaps lie at spreads below the sure-purchase cutoff); (c) W1 ref "Solver B 2" (balance condition) and "Solver A 2 and Solver C 3" (uniform condition, J′ ≥ AΔ²/γ²). The last sentence of (c) is the unrefereed chain of Stage 1, item (i); fallback: "(c) ... if either of the following holds: [uniform]; [balance]".

**T-P3-INT. Intuition** (replaces `04:311–321`):

> Coexistence comes from the entry response itself. In a quiet market entry stays at its floor after every order, so an informed order earns at most \(\rho\max\{\pi,1-\pi\}\) times the spread, and the upper bound on the spread keeps that below the trading cost. An informative market changes the entry response to a purchase, and with it the return to trade: a purchase that reaches the threshold recruits, and the lower bound on the spread lets it cover the trading cost.
>
> Entry rises with the spread while class \(H\) mixes, because the purchase rate adjusts. While class \(H\) mixes, a recruiting purchase earns exactly the trading cost, so a wider spread needs a more informative purchase; the purchase rate rises, and entry rises with it until class \(H\) buys for sure. Entry depends on the incumbent only through the spread, so between any two incumbents at which the markets coexist, entry in the informative market is at least as high at the one with the wider spread.
>
> A stronger incumbent raises both numbers, and they pull in opposite directions: a wider spread raises what a recruiting purchase earns, and a higher threshold makes recruitment harder. As the incumbent strengthens, the economy can enter the region, leave it, and enter it again. The stretch with a sure purchase is never split, because there a recruiting purchase pays even at the top posterior and the remaining conditions move in one direction with strength. The whole set stays in one piece when the spread grows, in proportion, at least as fast as class \(H\)'s margin over the high cost shrinks, which is the condition of part~(c).

Source: memo W1 main-text sentence and review section B (W1); the entry ranking across gaps is W1 ref "Shared Candidate 1" after eq. 2.

**T-P3-BENCH. The benchmark** (replaces `04:285–290` and `04:323–324`):

> The benchmark satisfies the condition of part~(c): its incumbent is uniform, \(\ell\) lies below \(r_0\), and \(h\) exceeds \(r_2\) by more than \(c_H\), so coexistence holds on one interval of strengths at every prior. At the prior \(1/2\) and the benchmark slot it starts at \(r_A\approx\reg{rA}\), where a purchase that just reaches the threshold and recruits earns the trading cost; full purchases start at \(r_F\approx\reg{rF_B}\), where a full purchase that recruits earns the trading cost; and the quiet market ends at \(r_N\approx\reg{rN}\), where a unit order against an uninformative price earns the trading cost. Entry in the informative market is \(\reg{entry_rA_B}\) at \(r_A\), \(\reg{entry_mb_r140_B}\) at \(\reg{str_r140}\) and \(\reg{entry_mb_r145_B}\) at \(\reg{str_r145}\), and from \(r_F\) it stays at \(\reg{entry_r1_B}\) up to the entry ceiling \(r_C\approx\reg{rC_B}\). Above \(r_N\) the informative market with a full purchase remains, and on \((r_N,r_J)\), with \(r_J\approx\reg{rJ}\), a market in which the investor mixes in both directions without recruitment joins it. The low class abstains up to \(r_N\), mixes on \((r_N,r_S)\) and sells for sure from \(r_S\approx\reg{rS_B}\), the strength at which a full sale earns the trading cost. Figure~\ref{fig:coexistence} draws the path through the region and the entry it produces, and Appendix~\ref{app:coexistence} lists the complete equilibrium set along the path.

The endpoints r_A and r_N come from the benchmark statement in A4, which keeps its own crossing and order conditions (W1 ref "What remains weak": the general theorem does not supply them).

**T-P3-WINDOW. The high cost of the benchmark** (new paragraph after T-P3-BENCH):

> The benchmark's high cost lies in the window in which both conditions on it hold. It is at most \(h-r_2=\reg{cH_afford_ceiling_B}\)*, so class \(H\)'s value covers the high cost against the strongest incumbent and part~(c) applies, and it is at least \((h^2-p^2)/(2h)=\reg{cH_DA_floor_B}\)*, so class \(H\) has the decisive advantage of Section~\ref{sec:ccc}.

Source: memo "Conditions, one per result" (the bracket 4.9875 to 6.4); review C2.

**T-P3-PRIORS** (`04:326–332`): keep the content; move the pointer to the end so the paragraph ends on it:

> Coexistence also holds away from the even prior. At the benchmark slot it starts at the same strength \(r_A\) for every prior between \(\approx\reg{piA_lo_B}\) and \(\approx\reg{piA_hi}\), and it starts later, where the prior reaches the threshold, for priors up to \(\approx\reg{pimax}\). Below \(\approx\reg{piA_lo_B}\) even the top posterior cannot reach the threshold once a purchase can pay for itself, and from \(\approx\reg{pimax}\) on the quiet market ends before the prior falls below the threshold. Appendix~\ref{app:coexistence} gives the coexistence set at every prior (Corollary~\ref{prop:priors}).

**T-5-OPEN** (`05:3`): "With research, the investor chooses the presence probability \(\lambda\) of Section~\ref{sec:slot} and pays for it." The rest of `05:3–27` stays.

**T-P4-LEAD. Lead-in to Proposition 4** (replaces `05:29–51`):

> Research raises the top posterior that a purchase can reach. At intensity \(\lambda\), I write \(M_\lambda\) for that top posterior and \(m_\lambda=1-M_\lambda\) for the bottom posterior, the posterior bounds of Section~\ref{sec:inference} at the prior \(1/2\) when the presence probability is \(\lambda\). When \(1/2<\tau<1\), the recruitment intensity \(\lambda_E\) is the research level at which a full purchase just reaches the threshold, \(M_\lambda=\tau\), so a full purchase recruits exactly when research is at least \(\lambda_E\).
>
> Consider the equilibrium in which class \(H\) buys after a success and the purchase recruits a high-cost challenger. The low class abstains while a sale at the entry floor cannot pay its cost, \(\rho\DT\le2k\). Beyond that point it sells just often enough that its sale breaks even, a mixture the default tie rule allows, and once even a sure sale pays, it sells for sure. A sale never recruits, and a sale that breaks even adds nothing to the value of research, so research optimality at an interior intensity reads
> \[ 2a\lambda=\DT\,m_\lambda-k+\bigl(\rho\DT\,m_\lambda-k\bigr)^+ \]
> (the display keeps `\label{eq:research}`).
> The left side rises with \(\lambda\), and the right side falls, because more research removes camouflage. When \(\DT>2k\), the two sides meet at one intensity in \((0,1)\), and research is that intensity or the cap \(\lb\), whichever is smaller. At the recruitment intensity, the trading profit after a success minus the marginal cost of research is the recruitment margin.

Source: W3 ref "Shared Candidate 1", sections 2 to 5 and eq. 7 to 10; memo W3.1 and W3.2.

**T-P4. Proposition 4** (replaces `05:52–71`):

```latex
\begin{proposition}[Competition creates research]\label{prop:research}
Let the classes satisfy the class ranking~\eqref{eq:classes} and the prior be \(1/2\), and let an indifferent investor
mix over its best orders and an indifferent high-cost challenger prepare. Take incumbent distributions with
\(1/2<\tau<1\), and the equilibrium in which class \(H\) buys after a success and a purchase recruits a high-cost
challenger.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
\item At a distribution with \(\DT>2k\), the equilibrium exists if and only if the posterior after a purchase, at the
investor's research choice, reaches the threshold. Research rises strictly with the spread until it
reaches the cap and then stays at the cap. Entry, \(\rho+(1-\rho)[\beta+(1/2-\beta)\lambda]\), and entry in class
\(H\) rise with research, and entry in class \(L\) falls.
\item If class \(H\) outbids the incumbent, high-class ownership equals half the entry in class \(H\), so it rises
with the spread.
\item Along a path of such distributions, suppose that the recruitment margin rises, is negative at the weakest
incumbent, and is positive where research reaches its cap. Then the equilibrium exists exactly on an interval of
strengths. On it, research rises from the recruitment intensity to the cap and then stays at the cap, until the
threshold passes the top posterior at the cap.
\end{enumerate}
\end{proposition}
```

Sources: (a) W3 ref "Shared Candidate 1" (existence condition 5, entry 10) and W2 ref "Shared Candidate 1" (entry by class); (b) memo decision 3 and W2 ref "Ranking and recommendation" item 2; (c) memo W3.7 and W3 ref section 6 ("one upward sign crossing before the cap, no subsequent downward exit, attainment of the cap spread"). The frame drops "0 < β ≤ 1/3" (standing assumption; footnote at `02:123` per Stage 1 item iii).

**T-P4-INT. Intuition** (replaces `05:44–46` and folds `05:108–117`):

> A wider spread raises the return to a purchase, so the investor chooses more research, and a purchase becomes more likely; the posterior after a purchase then rises further above the threshold. Research adds informed purchases in class \(H\) and removes liquidity orders in both classes, and the first effect dominates, so entry rises with slope \((1-\rho)(1/2-\beta)\) in research. Entry in class \(H\) rises and entry in class \(L\) falls, so the challengers who prepare are stronger on average.
>
> The low class's selling leaves this mechanism in place. A sale never recruits, and while the low class mixes, its sale breaks even, so a successful draw is worth what the purchase earns, as when the low class abstains. Once a sure sale pays, the sale's profit is a second return to research, and the research schedule kinks upward at that point.
>
> High-class ownership multiplies entry in class \(H\) by class \(H\)'s chance of beating the incumbent. Against a given realized incumbent value at which class \(H\) can win, research makes a class-\(H\) acquisition more likely, because only entry moves; across incumbents, ownership rises with entry when class \(H\) outbids the incumbent, as part~(b) states. Appendix~\ref{app:research} gives the exact comparison across incumbents.
>
> Along a path the spread and the threshold race as in Section~\ref{sec:coexistence}: a stronger incumbent raises what a recruiting purchase earns and the belief it must reach. Cheap research tips the race toward recruitment, because the extra research needed to reach a higher threshold costs little, and part~(c) then keeps the equilibrium on one interval of strengths.

Source: W2 ref "Shared Candidate 1" (fixed incumbent value, almost everywhere, where class H can win) and "Shared Candidate 3" (entrant composition); W3 ref section 5 (kink at the switch only).

**T-P4-BENCH. The benchmark** (replaces `05:46–51`, `05:73–81`, `05:119–130`; Table 4 and `05:148–152` stay):

> The benchmark research parameters are \(a=\reg{res_a}\) and the cap \(\lb=\reg{res_cap}\), the presence probability of the benchmark slot, so research at the cap reproduces that slot, and at \(r_1\) and \(r_2\) the equilibrium with research at the cap is the equilibrium of Proposition~\ref{prop:ccc} with \(\lambda=\lb\). The benchmark meets the condition of part~(c): research is cheap enough that the recruitment margin rises along the path, and the margin is negative at \(r_0\) and positive where research reaches its cap.
>
> Along the benchmark path a researched purchase first recruits at \(r_R\approx\reg{res_rR}\), where research is \(\reg{res_lambda_rR}\) and entry \(\reg{res_entry_rR}\). Research reaches its cap at about \(\reg{res_rcap}\), where entry reaches \(\reg{res_entry_cap}\), and stays at the cap, with that entry, up to the entry ceiling \(r_C\approx\reg{res_rC}\). The low class starts to sell at \(r_N\approx\reg{res_rN}\) and sells for sure from \(r_S\approx\reg{rS_B}\); research has reached its cap before either strength, so in the benchmark the sale's profit leaves research unchanged.
>
> Zero research and research at the entry floor complete the set of equilibria. Zero research, with entry \(\rho\), is an equilibrium up to \(r_N\), where an informed order at the entry floor starts to pay. Research at the entry floor, in which both classes trade after a successful draw, no order recruits and entry stays at \(\rho\), is an equilibrium from \(r_N\) to about \(\reg{res_rQ}\) and again above \(r_C\). The recruiting equilibrium therefore coexists with zero research from \(r_R\) to \(r_N\) and with research at the entry floor from \(r_N\) to about \(\reg{res_rQ}\)*; it is the only equilibrium from there to \(r_C\), and above \(r_C\) research at the cap with entry at the floor is the only equilibrium. Against the weak incumbent every nonzero order after a success loses, so research is zero there, and every trade choice at the benchmark strengths is strict, so these outcomes do not depend on how an indifferent investor breaks a tie. Figure~\ref{fig:research} draws the three equilibria along the path.

Source: memo "What changes in the benchmark story", first and second items; W3 ref "The benchmark" (the IM/C1 list, r_X = 2.166995). The figure note carries the visual reading; the tie dependence under an abstaining investor lives in the appendix tie remark only.

**T-8. Empirical implications** (Section 8; paragraph heads kept):

- Opening (`08:3–9`): "The model gives predictions for publicly visible sale processes in which one bidder is prepared and a further buyer has not yet committed to diligence. Each prediction concerns one target at one incumbent strength, under the trading pattern it names, and Appendix~\ref{app:empirical} states each in full and proves it. In the benchmark at the prior \(1/2\), full two-sided trade is the unique outcome at every strength between \(r_S\), the exact strength at which a full sale earns the trading cost, and \(h\); this interval contains \(r_1\), the entry ceiling \(r_C\) and \(r_2\). Under full two-sided trade the informed share of nonzero orders is \(u/(2+u)\) at every prior."
- Price impacts and the price gap (`08:19–31`): "Weighted by how often its order occurs, the purchase impact \(P(1)-P(0)\) exceeds the sale impact \(P(0)-P(-1)\) exactly when a purchase recruits the challenger, when the investor trades in both directions and the prior lies below the preparation threshold (Proposition~\ref{prop:spread}). The weighted difference equals the average price after the order opportunity minus the price after no order, so the test needs prices and order frequencies and no auction object; at the prior \(1/2\) the two frequencies are equal, and the test compares the impacts directly. The price gap \(P(1)-P(-1)\) has a class component, \(\rho\DT\,[M(\pi)-m(\pi)]\), and an entry component, which is positive exactly when a purchase recruits. As the incumbent strengthens, entry adds more to the price through competition and less by rescuing a sale that the incumbent alone would not complete; with a uniform incumbent and a reserve below a fraction \(1/\sqrt3\) of the lowest challenger value and of the weakest incumbent's top value, the entry component rises with strength, and the benchmark reserve is that low." Then the existing benchmark numbers (`08:28–31`) with "price spread" read as "price gap".
- Informed trading (`08:33–42`): "Under full two-sided trade the mean order is \(\lambda(2\pi-1)\), so order counts identify the informed investor's presence when the prior is known and differs from one half, with a large variance near one half (Proposition~\ref{prop:informedshare}). At one half, and when the prior is unknown, the sale impact identifies presence, given that the payoff scale \(\rho\DT\) is known and that entry after a sale and after no order sits at its floor." Then the existing benchmark interval and the alternative slot (`08:35–41`).
- Winners (`08:44–50`): "Under full two-sided trade, a prepared challenger wins more often after a purchase than after a sale exactly when the incumbent's value sometimes falls where the two classes differ in their chance of beating it; the gap is \(M(\pi)-m(\pi)\) times the average class difference in that chance (Proposition~\ref{prop:winner}). The prediction holds above the entry ceiling, where orders no longer predict entry: there the order still covaries positively with a challenger win and not with entry. With the prior and slot fixed, when class \(H\) outbids every incumbent, the gap widens as a stronger incumbent takes wins from the low class. In the benchmark class \(H\) outbids every incumbent, and the gap is \(\reg{wgap_r1_B}\) at \(r_1\) and \(\reg{wgap_r2_B}\) at \(r_2\); the covariance of the order with entry is \(\reg{cov_entry_r1_B}\) at \(r_1\) and zero at \(r_2\). Among prepared challengers, the share of the high class at each price is the price-implied posterior, which rises with the price."
- Announcements (`08:52–57`): "If a public event after the price reveals only whether the challenger prepared, the mean price change over preparation reports is positive exactly when preparation was still uncertain after some order, at every prior and in every equilibrium; in the benchmark it is \(\reg{evprep_mean_r1_B}\) at \(r_1\) (Proposition~\ref{prop:announcement}). The mean change over both reports, with their model probabilities, is zero. An opportunity that passes with no order is bad news about entry: at \(r_1\) the price after no order minus the expected price before the opportunity is \(\reg{pdrop_neutral_r1_B}\), and the size of this drop is the weighted difference of the price-impact test."
- Two clusters (`08:59–64`): "In one cluster the market is quiet: the mean order is zero and the three prices coincide." Rest unchanged.
- Measurement (`08:79`): "such as flow from sector specialists" becomes "such as orders from sector specialists".

Sources: W5 ref "Shared candidate 1" (weighted identity, sign table, identity with A.14(iv)), "Shared candidate 2" ("Full two-sided trade"; "Sale-price identification with an unknown prior"), "Entry-component trend" (reserve condition, ℓ² − 3p² = 1/4), "Announcement returns"; W4 ref "general identity and its sign", "covariance constants", "High-class outbidding". The class component ρΔ(M − m) replaces "ρΔ times the informed share", a prior-1/2 identity (memo W5, `A8:8`).

**T-INTRO.** Introduction (`01_introduction.tex`):

- Main result (`01:38–41`): "...so entry rises even though acquisition profit falls at every fixed belief. When the high class outbids the incumbent, the probability that a challenger from the high class acquires the target rises with entry, and the high class wins a larger share of the takeovers that go to a challenger."
- Coexistence (`01:61–67`): "The investor's orders, the posteriors and the challenger's preparation depend on the auction only through two numbers, the target-payoff spread and the belief that a high-cost challenger needs before it prepares, and a stronger incumbent raises both whenever a known low-class challenger would not prepare at the high cost (Section~\ref{sec:twonumbers}). A quiet market, in which the investor does not trade, and an informative market coexist exactly on a region of these two numbers (Section~\ref{sec:coexistence}). In the informative market entry depends on the spread alone: it rises while the investor mixes between a purchase and abstention and stays constant once the investor buys for sure. Along any path of strengthening incumbents, the strengths at which coexistence comes with a sure purchase form one interval, and the whole set is one interval when the spread grows, in proportion, at least as fast as the high class's margin over the preparation cost shrinks. In the benchmark that interval runs from \(r_A\approx\reg{rA}\) to \(r_N\approx\reg{rN}\), and the same start of coexistence holds for a window of priors around the benchmark."
- Research (`01:69–75`): "When the investor pays for research that can make it informed and the prior is even, research and entry rise together with the spread until research reaches its cap (Section~\ref{sec:research}). This holds wherever the equilibrium exists, for every pair of ranked classes, and the low class's selling on bad news does not interrupt it: the low class first sells only as often as keeps its sale at break-even, which adds nothing to the value of research, and once a sure sale pays, its profit adds a second return to research. When the high class outbids the incumbent, high-class ownership rises with research. In the benchmark, research rises from \(\reg{res_lambda_r155}\) at the strength \(\reg{str_r155}\) through \(\reg{res_lambda_r160}\) to \(\reg{res_lambda_r165}\) at \(\reg{str_r165}\), and entry from \(\reg{res_entry_r155}\) through \(\reg{res_entry_r160}\) to \(\reg{res_entry_r165}\); research reaches its cap at about \(\reg{res_rcap}\) and stays there up to the entry ceiling. The unique outcome has no research with the weak incumbent and research at the cap with the strong incumbent."
- Robustness (`01:80–83`): "the buyer and the investor" becomes "the challenger and the investor"; "the buyer's signal" becomes "the challenger's signal"; optional clause "for any ranked classes" (A.7 extended).
- Welfare (`01:87–91`): "In a bargaining institution with two class values, the effect of competition on the target-payoff spread depends on the weight..."; "A reserve that excludes the low-value class" becomes "A reserve above every low-class value".
- Empirics (`01:93–98`): "When the investor trades in both directions and the prior lies below the preparation threshold, a purchase raises the price by more than a sale lowers it, once each impact is weighted by how often its order occurs, exactly when the purchase recruits the challenger; the test needs only prices and order frequencies (Section~\ref{sec:empirical}). In the benchmark, the entry component is \(\reg{ba_share_r1_B}\) of the price gap between a purchase and a sale. A prepared challenger wins more often after a purchase than after a sale whenever the incumbent's value sometimes falls where the two classes differ in their chance of beating it, and above the entry ceiling, where orders no longer predict entry, orders still predict the winner. Order counts identify the informed investor's presence when the prior is known and differs from one half, and at one half the sale price identifies it, given the payoff scale."
- Roadmap (`01:136–140`): "Section~\ref{sec:model} sets out the model and the benchmark, and Section~\ref{sec:payoffs} derives the returns to information and the two numbers through which trading sees the auction. Section~\ref{sec:results} states the main results. Sections~\ref{sec:research} to~\ref{sec:empirical} cover research, robustness, welfare and sale terms, and empirical implications, and Section~\ref{sec:conclusion} concludes. Appendix~\ref{app:proofs} states the results of Sections~\ref{sec:research} to~\ref{sec:empirical} in full, lists the complete equilibrium set along the benchmark path, and proves every result."

**T-CONC. Conclusion** (`09_conclusion.tex`):

- `09:9–15`: "The comparison of the weak, strong and very strong incumbent holds with unique outcomes on an open set of parameters. A quiet market and an informative one coexist on a region of the target-payoff spread and the preparation threshold, and a stronger incumbent moves the economy through that region by raising both; in the informative market, entry rises with the spread while the high class mixes between a purchase and abstention and stays constant once it buys for sure. When information is costly, competition creates research: at an even prior, research and entry rise together with the spread until research reaches its cap, and the low class's selling does not interrupt them."
- `09:19–21`: "with two class values, the weight that the payment rule places on the runner-up's value decides how competition moves the target-payoff spread"; "A reserve above every low-class value".
- `09:24–26`: "...and whether a purchase raises the price by more than a sale lowers it, weighted by order frequencies, where the price should recruit."

### 3.2 Crosswalk by file and line

Each row: current passage; target or edit; the appendix statement it must match; source.

**`main.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 23, 77 | Title unchanged | — | brief |
| 54–57 | Macro comment for `\fr`: argument d to Δ (non-printing; with A4) | — | SCAN P3 |
| 84–98 | T-ABS | Prop 2 with A.5 (open set with ownership); A.3; Prop 3(a); Section 3.4 (A2); Prop 4(a); A.8 | memo decisions; W1, W3 ref rankings |

**`sections/01_introduction.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 9, 41 | "a challenger from the high-value class" to "a challenger from the high class" | — | SCAN P3 |
| 19 | "a high-value or a low-value quality class" to "one of two quality classes, high and low, whose value distributions are ranked" | eq:classes | SCAN P3 |
| 38–41 | T-INTRO main result | Prop 2(ii) and T-P2 | W2 ref SC3; "Do the same workarounds cover Proposition 2" |
| 61–67 | T-INTRO coexistence | Section 3.4; Prop 3; A4 benchmark statement | W1 ref SC1, Solver B 1, Solver B 2, Solver A 2 |
| 69–75 | T-INTRO research | Prop 4(a), (b); A5 benchmark statement | W3 ref SC1 §5; W2 ref SC1; memo benchmark story |
| 80–83 | "buyer" to "challenger" (twice) | A.7 | SCAN P3 |
| 87–91 | two-value scope of the payment rule; "a reserve above every low-class value" | A.9, A.10 | SCAN P3 |
| 93–98 | T-INTRO empirics | A.11 weighted; A.13 sign and covariance; A.12 identification | W5 ref SC1, SC2; W4 ref ranking |
| 108–109 | "learns about its class, and through it about the distribution of its value" | — | SCAN P3 |
| 136–140 | T-INTRO roadmap | — | — |

**`sections/02_model.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 1 | Delete `ty` (decision 1) | — | SCAN headline 9 |
| 52–55 | Delete "In the main case..."; add the path sentence of T-2.4 | A1 path lemma | memo appendix notation |
| 62 | "The high class, or high-value class," to "The high class" | — | SCAN P3 |
| 69–74 | "the spread rises" to "the class difference in target proceeds rises" (spread is defined at 199); "a reserve that excludes the low class" to "a reserve above every low-class value" | Prop 1(c) | SCAN P3 |
| 78–88 | Move the benchmark declaration to T-2.5; keep the general normalization sentence (85–87) | — | brief (worked example once) |
| 123–125 | Footnote: "Propositions 2 to 4 hold for every β < 1/2" if Stage 1 item (iii) confirms | A2, A5 | W3 ref SC1 |
| 159–165 | Footnote on Euler's number kept (decision 6) | — | memo decision 5 |
| 203–204 | Uniform-family notation moves to T-2.5 | — | — |
| 216–218 | Tie rules kept as their one home | tab:a4-ties; rem:researchties | style guide 2.6 |
| 225–228 | T-2.4 (W_j, outbidding, entry by class) | A3, A5, A8 usages | memo "Conditions, one per result" item 1 |
| after 228 | T-2.5, `\label{sec:example}` | A9 declarations | — |

**`sections/03_competition_information.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 5–82 | Recommended order: general split (5–17); two-to-three-sentence lead-in from the slice argument; Proposition 1 unchanged (41–58); slice intuition (60–70); class-gap identity (72–78); then "In the benchmark" closed forms (19–35) and the limit near ℓ (80–82, "a class-L challenger"); end on "whether entry rises depends on how this change in payoffs affects the information in the price" | Prop 1 unchanged; eq:payoffs, eq:derivatives labels kept (cited from A1 and A3) | structure rule |
| 94 | Keep "the ceiling" (decision 15) | cor:exclusion | style guide 2.5 |
| after 141 | T-3.4, `\label{sec:twonumbers}` | A2 two-numbers statement; A1 threshold rise | SCAN Part 2; memo decision 2; W1 ref Solver B 1 |

**`sections/04_equilibrium_results.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 11–44 | T-P2 (one sentence in (ii)) | A3 share and outbidding | W2 ref SC3 |
| 52 | "The ceiling (H3)" kept | — | style guide 2.5 |
| 63–67 | T-P2-OWN | A3 decisive advantage | W2 ref "Decisive advantage" |
| 69–73 | "describes the strengths between the three economies" to "describes where quiet and informative markets coexist between them" | — | — |
| 75 | Title optional: "The benchmark economies and the fixed-information control" | — | — |
| 77–87 | Declarations move to T-2.5; 4.2 opens on Table 1 | — | brief |
| 113–119 | T-4.2-OWN | A3; registry | W2 ref benchmark verification |
| 121, 131 | "admissible region" to "recruitment region" (text and Table 2 caption) | prop:region title | SCAN P3, pattern 4 |
| 155–160 | "a high-class challenger outbids every incumbent on the path" to "class H outbids every incumbent on the path" | — | SCAN P3 |
| 194 | "gross profit at the two strengths" to "at the two incumbent distributions" | A.3 | SCAN P3 |
| 256–270 | T-P3-LEAD | — | memo W1 |
| 272–283 | T-P3 | A4 general proof | W1 ref |
| 285–290, 323–324 | T-P3-BENCH ("the sale threshold r_S" becomes "the strength r_S at which a full sale earns the trading cost") | A4 "Proposition 3 in the benchmark" | W1 ref consolidated check |
| 292–309 | T-FIG2 (3.4 below) | A4 table; A4:297 | W1 ref (figure-note exception) |
| 311–321 | T-P3-INT | Prop 3(a)–(c) | memo W1; review B |
| new | T-P3-WINDOW | A9 margins | memo "Conditions, one per result" |
| 326–332 | T-P3-PRIORS | Corollary A.2 unchanged | — |

**`sections/05_research.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 1 | Title kept ("Competition creates research") | — | — |
| 3 | T-5-OPEN (removes "now") | — | R3 |
| 29–51 | T-P4-LEAD; `eq:research` gains the positive part | A5 research condition; eq:a5-F re-derived | W3 ref SC1 §3–5 |
| 52–71 | T-P4 | A5 general proofs; Prop 4(b) content moves to A5 "Proposition 4 in the benchmark" | W3 ref; W2 ref |
| 73–81 | Folded into T-P4-BENCH | A5 benchmark statement | — |
| 83–106 | Table 4 kept; note: "The benchmark with \(a=\reg{res_a}\) and \(\lb=\reg{res_cap}\). The spread, the threshold and \(\lambda_E\) are rational numbers; the other entries are rounded to six places." | — | R3 (removes "interval enclosures") |
| 108–117 | Keep the three-strength reading; "Part (a) ... shows that this comovement is general along the branch" becomes "Proposition 4(a) states the same comovement wherever the equilibrium exists" | Prop 4(a) | — |
| 119–130 | T-P4-BENCH (the cap no longer ends the equilibrium; r_U leaves the main text) | A5 benchmark map | memo benchmark story; W3 ref "The benchmark" |
| 132–146 | T-FIG3 | A5 map | W3 ref |
| 149 | "must now pay" to "must pay" | — | R3 |
| 154–160 | "admissible region of the research parameters" to "region of research parameters"; "patterns of Proposition 4(b)" to "the benchmark pattern of this section" | prop:researchregion re-anchored | — |
| new | T-P4-INT | A5 ownership statements | W2 ref SC1, SC3; W3 ref §5 |

**`sections/06_robustness.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 10–12 | "Proposition~\ref{prop:atomless} lets the cost mix a low component with weight \(\rho\) and a high component in place of the two-point law of Section~\ref{sec:values}; either component can be atomless or have atoms." | A.4 | R3 |
| 42 | "mean-preserving spread" to "mean-preserving increase in risk" | — | SCAN P3 |
| 58–66 | Investor and challenger accuracies \(\alpha_I,\alpha_C\) in place of \(a_T, d\) (decision 15); clause "for any ranked classes and any continuous pair of incumbent distributions" | A.7 extended | W2 ref "Proposition A.7"; SCAN P1 |
| 79 | "a buyer signal" to "a challenger signal" | — | SCAN P3 |

**`sections/07_welfare.tex`**

| Lines | Edit | Must match | Source |
|---|---|---|---|
| 30–32 | "with the strong benchmark and \(c_H=\ldots\)" to "in the benchmark at \(r_1\) with \(c_H=\ldots\)" | A.8 | SCAN P3 |
| 52 | "A high-class challenger wins" to "A class-H challenger wins" | A.9 | SCAN P3 |
| 67 | Section reference to `sec:example` | — | — |
| 70 | "A reserve that excludes the low class" to "A reserve above every low-class value" | A.10 | SCAN P3 |

**`sections/08_empirical.tex`**: T-8 throughout; the "price spread" becomes "the price gap" (`08:19, 22, 28–30, 40`); "A prepared high-class challenger always outbids the incumbent" (`08:49`) becomes the outbidding check in Winners.

**`sections/09_conclusion.tex`**: T-CONC.

### 3.3 Worked-example passages and what each shows

| Passage | What it shows | Kind |
|---|---|---|
| 2.5 declaration | All numbers in one place | numbers |
| 3.1 closed forms (eq:payoffs) | The opposition in closed form; the spread vanishes as r approaches ℓ | illustration of Prop 1 |
| 4.2 Table 1 and T-4.2-OWN | Two forces at three strengths; (H1)–(H3) hold; entry and ownership rise; outbidding holds, and the takeover share rises from 6/11 to 0.83; decisive advantage means the uniform family never shows an ownership fall | check of conditions; insight only the example gives |
| 4.2 Table 2, Figure 1 | The slot band and the prior window; the threshold rises slowly, which sets the band's width | numbers |
| 4.2 Table 3 | The control: entry flat to r_C then lower at fixed information; hidden price | numbers for A.3 |
| 4.3 T-P3-BENCH, Figure 2 | Condition (c) holds; coexistence from r_A to r_N; entry rises then stays; the path through the region | check; figure |
| 4.3 T-P3-WINDOW | The high cost sits between the two conditions that bound it | insight only the example gives |
| 4.3 T-P3-PRIORS | Start of coexistence across priors | numbers (Corollary A.2) |
| 5 T-P4-BENCH, Table 4, Figure 3 | Cheap-research condition holds; research path from r_R to the cap and on to r_C; the cap comes before any selling, so the second return does not move research here; the three equilibria and uniqueness from about 2.167 | check; insight; figure |
| 5, cap and cost (`05:154–160`) | The region of research parameters for the benchmark pattern | numbers (A.2) |
| 6, 7 | Unchanged examples | numbers |
| 8 | Price gap and entry share; identification interval; winner gaps; announcement mean; two clusters at one strength | numbers; the clusters are an example-only insight about selection |

### 3.4 Figures and captions

**Figure 1** (`fig:beliefs`, `04:167–180`): unchanged.

**Figure 2** (`fig:coexistence`, `04:292–309`), recommended layout (decision 2): panel (a) the region of Proposition 3(a) at the prior 1/2 and the benchmark slot, spread on a logarithmic horizontal axis (about 0.01 to 1) so the whole path fits, threshold on the vertical axis (about 0.48 to 0.76); the region bounded by τ = 1/2, τ = M(1/2), the curve Δ_T = k/(1 − τ) and the line Δ_T = 2k/ρ; the sure-purchase part (Δ_T ≥ k/(1 − M)) darker; the benchmark path (Δ_T(r), τ(r)) from r_0 to r_2 with ticks at r_A, r_F, r_N and r_C, and an arrow in the direction of strength. Panel (b) is the current panel (a), with the current panel (b) as an inset. The path in panel (a) is nearly flat (τ moves from 0.633 to 0.731 over the path, 0.641 to 0.654 inside the region): the panel shows that coexistence here is a spread story, which matches the "threshold rises slowly" reading of `04:155–160`. No second, non-uniform path in the main text.

Caption: "Coexistence along the benchmark path." Notes:

> \textit{Notes.} The benchmark at the prior \(1/2\) and the benchmark slot. Panel (a) draws the region of Proposition~\ref{prop:coexistence}(a) in the plane of the target-payoff spread, on a logarithmic scale, and the preparation threshold; the darker part has a sure purchase. The curve is the benchmark path from \(r_0\) to \(r_2\): it enters the region at \(r_A\), reaches the part with a sure purchase at \(r_F\), leaves the region at \(r_N\), and meets the top posterior \(M(1/2)\) at the entry ceiling \(r_C\). Panel (b) shows entry against incumbent strength \(r\) in each equilibrium pattern, when an indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares. It labels a quiet market by N, a mixed purchase that recruits by R, a full purchase by F, mixed orders without recruitment by Q and the threshold pair by T. The thin dashed line is the threshold pair: it is an equilibrium at \(r_A\), where entry after a purchase is one, and on the rest of \((r_A,r_J]\) when an indifferent high-cost challenger may prepare with any probability. The blue band marks coexistence from \(r_A\) to \(r_N\), and the inset enlarges it. With a full purchase the low class abstains up to \(r_N\), mixes from \(r_N\) to \(r_S\) and sells for sure from \(r_S\). Filled markers belong to a branch and open markers do not; above \(r_C\), entry with a full purchase equals \(\rho\).

Source for the threshold-pair sentence: W1 ref (the figure note at `04:302` needs the exception at r_A; `A4:297`); memo W1 first bullet.

**Figure 3** (`fig:research`, `05:132–146`), filled: one continuous axis r ∈ [1.2, 3.6], no gray band, no break. Panel (a) research: zero research at λ = 0 on [r_0, r_N]; recruiting research from λ_E(r_R) = 0.194 at r_R rising to the cap at 1.678, then flat at the cap to r_C; research at the entry floor from 0 at r_N rising to 0.234 at r_Q = 2.167 (open end), and at the cap above r_C. Panel (b) entry: zero research at ρ on [r_0, r_N]; recruiting research from 0.501 to 0.523, flat to r_C; research at the entry floor at ρ on (r_N, r_Q) and above r_C; inset enlarging the rise. A light band over [r_R, r_Q) marks the strengths with two equilibria. Ticks: r_R, the cap strength, r_N, r_Q, r_C (staggered: 1.68 and 1.75 are close). Distinct colors and line styles for the three equilibria where they share a height.

Caption: "Research and entry along the benchmark path." Notes:

> \textit{Notes.} The benchmark with \(a=\reg{res_a}\) and \(\lb=\reg{res_cap}\), when an indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares. Panel (a) shows research \(\lambda\), and panel (b) shows entry; the inset enlarges entry where research rises. The figure draws three equilibria. Zero research holds from \(r_0\) to \(r_N\). Recruiting research starts at \(r_R\), reaches the cap at \(r_{\lb}\) and stays there up to the entry ceiling \(r_C\), with entry \(\reg{res_entry_cap}\) at the cap. Research at the entry floor, in which both classes trade after a successful draw and no order recruits, holds from \(r_N\) to \(r_Q\) and above \(r_C\), with entry \(\rho\). The light band marks the strengths with two equilibria, from \(r_R\) to \(r_Q\). Black dots mark \(r_0\), the three strengths of Table~\ref{tab:research}, \(r_1\) and \(r_2\).

**Tables.** Table 2 caption "The recruitment region at the benchmark auction." Table 4 note as in 3.2. Table 3 Panel B title kept. No new main-text table.

### 3.5 Registry keys

New keys the main text prints (names are proposals; exercise and checker in brackets):

| Key | Value | Used in | Exercise / checker |
|---|---|---|---|
| `own_share_r0` | 6/11 ≈ 0.545455 | T-4.2-OWN | P4_information / XP4 |
| `own_share_r1_B` | ≈ 0.830691 | T-4.2-OWN | P4_information / XP4 |
| `cH_DA_floor_B` | (h² − p²)/(2h) = 399/80 = 4.9875 | T-4.2-OWN, T-P3-WINDOW | P2_auction / XP2 |
| `cH_afford_ceiling_B` | h − r_2 = 32/5 = 6.4 | T-P3-WINDOW | P1_core / XP1 |
| `res_rQ` | ≈ 2.166995 (floor-entry research ends) | T-P4-BENCH, Figure 3 log | P3_research / XP3 |

For the parameter table A9 (appendix lens), with the same checker rule: `margin_afford_B` 0.4; `margin_DA_B` 1.0125; `margin_balance_B` 9667/8280; `margin_balance_sq_B` 937/5520; `margin_reserve_low_B` ℓ² − 3p² = 1/4; `res_phi_start_B` ≈ −0.022693 and `res_phi_cap_B` ≈ 0.017446 (the recruitment margin at r_0 and at the cap); `res_lambda_floor_rQ` ≈ 0.234257 if the appendix prints it; the cap-before-selling margin ≈ 0.001556 only if that corollary stays.

Reused, not duplicated: `margin_res_half_B` = 1.195833 is the announcement condition's minimum margin (c_H − B_r(1/2) is smallest at r_0); `margin_res_amono_B` = 0.136713 is the cheap-research margin; `rS_B` serves as the strength of the first sure sale on the capped research path (the cap equals the slot's presence, so m_λ̄ = m(1/2)).

Notes to change: `res_rcap` (where research reaches the cap; the equilibrium continues), `res_entry_cap` (entry on the capped recruiting equilibrium up to r_C). `res_rUR` leaves the main text and stays in A5.

### 3.6 Vocabulary and notation in the main text

| Object | One word or symbol | Retire | Where it changes |
|---|---|---|---|
| Equilibrium without informed trade | a quiet market (N in figures and appendix tables) | "equilibrium without informed trade", "uninformative equilibrium", "no trade" as a noun | abstract, 01, 04, 08, 09 (decision 10) |
| W_H(F) = 1 | class H outbids the incumbent | "high-class challenger outbids", "always outbids" | 02, 04, 05, 08 |
| Values and costs giving outbidding wherever a price recruits | a decisive advantage | — | 04 (two uses) |
| (H1)–(H3) set | the recruitment region | "admissible region" (main text and the titles of A.1, A.2) | 04:121, 131; 05:154; 07:30 |
| Δ_T | the target-payoff spread, "the spread" | "price spread", "the spread S" | 08 |
| P(1) − P(−1) | the price gap | "price spread", "spread between purchase and sale prices" | 01:95, 08 |
| Mean-preserving change | increase in risk | "mean-preserving spread" | 06:42 |
| r_C and (H3) | the entry ceiling, the ceiling | keep both: the same point beyond which no price recruits | — |
| τ | the preparation threshold, "threshold" | "sale threshold r_S"; "threshold" for marked strengths | 04:267 |
| Classes | class H, the high class; "a challenger from the high class" in the abstract | "high-value class", "high-value challenger" | 01, 02, 03, 07 |
| Entrant | the challenger | "the buyer" for the entrant (keep "buyer" in the setting) | 01:81–82, 06:79 |
| Worked example | the benchmark (declared in 2.5) | "main case", "calibration B", "strong benchmark" | 02:54, 07:32 |
| Research reaches the cap | r_{λ̄} in figure and appendix; words in the text | r̄_R (collides with the support bound r̄, `02:53`, `03:42`) | 05, Figure 3 |
| Floor-entry research ends (≈ 2.167) | r_Q (Q is the floor-entry form) | r_X (X is the order) | Figure 3, A5 |
| Signal accuracies | α_I (investor), α_C (challenger) | a_T (a is the research cost), d (argument of 𝔯) | 06:61–76 |
| Recruitment margin | words in the text; φ with its exact form in A5 | φ_a (collides with φ_± in A6) | 05 |

### 3.7 Style-guide compliance checklist

Laplace register with joined conditional chains; "I"; one argument per paragraph; lead-in of two to four sentences before each proposition with notation at its end; one "Let ... and suppose that" frame per statement; outcomes in words; intuition first after each proposition, then scope that carries economics, then at most two sentences of pointers; hypotheses with economic names ("the high-cost window", "the trading-cost window", "the ceiling", "outbids", "decisive advantage", "cheap research", "a low reserve"); every symbol introduced in words; displays only for reused equations (the region and entry display in Proposition 3, eq:research); no lemma, corollary, definition or remark environment in the main text; tie conventions once in 2.4, alternatives only in figure notes that draw them; margins in A9, positive facts in the text; status sections 2.4 and 2.7 of the style guide void (R1).

---

## 4. Label and numbering map

**Main-text labels**

| Label | Object | Change | Number | Citing it | Action |
|---|---|---|---|---|---|
| `prop:ccc` | Proposition 2 | one sentence in (ii) | 2 (unchanged; parts unchanged) | 02:124; 04:116, 126, 164, 207, 256; 05:67; 06:9, 12, 19, 30; 07:6, 7, 30; 08:15; comparison (12, and "2(iii)"); slides (7) | none |
| `prop:coexistence` | Proposition 3 | title and statement general; parts (a)–(c) change meaning | 3 | 01:139 ("full form"); 02:124; 04:300; A4:288 (named "full statement") and the proof header; comparison "Proposition 3" (8) and "Proposition 3(b)" (1); slides 456 | old (a), (b) references go to "Proposition 3 in the benchmark" (A4) or to the new (a); 01:139 by T-INTRO roadmap |
| `prop:research` | Proposition 4 | general; old part (b) leaves the statement | 4 | 05:113, 143, 156; A5 proof headers; `prop:researchregion` (statement and proof cite "Proposition 4(b)"); `rem:researchties` ("Proposition 4(b) needs no investor tie rule"); comparison row 207 and prose; slides 476, 484, 773, 776 | every "Proposition 4(b)" re-anchored to "Proposition 4 in the benchmark" (A5) or to the text; slides 484 and 776 also lose "[r_R, r̄_R)" |
| `eq:research` | research condition | positive part added | unchanged | A5:46 (`eq:a5-F` clears its denominator) | A5 re-derives |
| `fig:coexistence` | Figure 2 | region panel; note | 2 | 04:267, 311 | none (slides use the file `coexistence_talk.pdf`) |
| `fig:research` | Figure 3 | filled | 3 | 05:148 | none (slides use `research_talk.pdf`) |
| `tab:region` | Table 2 | caption wording | 2 | 04:126, 185 | none |
| `tab:research` | Table 4 | note wording | 4 | 05:108 | none |
| `sec:benchmark` | Section 4.2 | declarations move out | 4.2 | 01:48, 50, 59; 04:60, 259, 266; 05:50; 07:67; 08:5, 16 | 05:50 and 07:67 move to `sec:example`; the rest stay |
| `sec:example` (added) | Section 2.5 | — | 2.5 | 03 closed forms; 05 research parameters; 07:67; 08 opening | — |
| `sec:twonumbers` (added) | Section 3.4 | — | 3.4 | 01 coexistence; 04 lead-in; 05 lead-in | — |

Adding 2.5 and 3.4 at the ends of their sections renumbers no other subsection. Main-text tables stay 1 to 5 and figures 1 to 3 if the region is a panel of Figure 2; a separate region figure would make the research figure Figure 4 (cited only by `\ref` and by file name, so harmless).

**Appendix numbering policy** (for the appendix lens; consumers hard-code numbers). `comparison.tex` cites Lemma A.1–A.3, Corollary A.2, Definition A.1, Proposition A.1–A.13, Table A.3, A.4, A.6; `slides.tex` cites Lemma A.3, Proposition A.3, A.8, A.11–A.14. Hence: no new numbered proposition or corollary anywhere in the appendix (Proposition A.1–A.14 and Corollary A.1–A.3 keep their numbers); benchmark statements use the existing `named` environment ("Proposition 3 in the benchmark", "Proposition 4 in the benchmark"), as A1 already does for Proposition 1(c); new lemmas only after `lem:trading`, so Lemma A.1–A.3 keep their numbers (Lemma A.4 onward may shift; no consumer cites them); no new appendix table before `tab:classes` (Table A.4), or `comparison.tex` updates its table numbers; `rem:researchties` stays Remark A.1.

---

## 5. Risks and traps

1. **Drift between main text and appendix.** The scan found exactly this (benchmark results worded as general). Mitigation: Stage 1 crosswalk; the mathematics writer fidelity read of every result sentence in Stages 6 to 8 and 10; consumers last.
2. **Lost qualifiers in compressed sentences.** At risk: "at an even prior" and the mixing investor (research), "when the investor trades in both directions" and "below the threshold" (weighted test), "one target at one strength" (tests), "with the prior and slot fixed" (winner trend), "class L sometimes wins" (takeover share), "whenever a known low-class challenger would not prepare" (threshold rise). Mitigation: each crosswalk row lists its qualifiers; the abstract, introduction, conclusion and slides get a qualifier-only read.
3. **The old research story survives somewhere.** "The branch ends at the cap" appears at `01:69–75`, `05:119–130`, the figure note `05:138–145`, A5 "The branch at calibration B", slides 484 and 776, comparison row 207. Mitigation: grep `res_rcap`, `\\bar r_R`, `r_U`, `res_rUR`, "branch runs", "not characterized", "beyond".
4. **Language rules on the mathematics writer prose and on the appendix.** the mathematics writer drafts tend to carry hedges and bookkeeping ("we note", "verified by"); the appendix carries about 100 process phrases. Mitigation: R-sweeps per stage; plain-language review and anti-defensive pass on every mathematical paragraph before integration.
5. **`comparison.tex` is built on status labels and version history.** Its results table has a status column (56 hits) and sentences such as "the slot replaces three certified points". Mitigation: treat it as a redesign in Stage 10 (decision 7), not a sweep.
6. **Unrefereed links in my targets.** Uniform condition implies the balance condition; the strictness condition for the takeover share; Proposition 4 for β < 1/2; uniqueness from r_Q holds under the default tie rules only. Mitigation: Stage 1 items (i) to (iv), with the fallbacks stated in 3.1.
7. **Figure traps.** Close ticks (1.68 and 1.75); lines that share a height (entry ρ; the cap); the Linux font path at `make_figures.py:39` falls back to another font on the MacBook; `OUT` writes to the mirror. Mitigation: staggered ticks, distinct styles, grayscale check, `pdffonts`, decision 8.
8. **Registry conflicts and stale meanings.** Duplicate keys with different displays across CSVs (for example a `res_rS` beside `rS_B`); `res_rcap` read as an endpoint. Mitigation: reuse `rS_B`; update notes; `make_numbers.py` prints conflicts.
9. **Scripts point at the mirror.** `make_numbers.py:14` writes `slot/manuscript/numbers.tex`, and `number_scan.py:9` scans `slot/manuscript`; a clean scan of the mirror says nothing about the master. Mitigation: decision 8.
10. **Overleaf edits during the work.** Mitigation: pull at Stage 0 and again before Stage 12; commits by file group; no push without approval.
11. **Subtree divergence.** Copying files into `slot/manuscript/` before the Overleaf push creates history Overleaf lacks. Mitigation: Stage 12 order (push after approval, then subtree pull).
12. **Length creep.** Mitigation: Propositions 3 and 4 at most about 20 lines each; margins stay in A9; the main text grows by about one page.
13. **Partial vocabulary.** "Quiet market" beside "equilibrium without informed trade" would give one object two names. Mitigation: grep both terms after Stage 6.
14. **The research display changes.** `eq:research` gains the sale's profit; A5's polynomial `eq:a5-F` and the benchmark proof rest on the old display. Mitigation: listed in Stage 3 (A5).
15. **The tie dependence disappears.** With the abstaining-investor gap moved off the main text, the appendix must record it, or the paper silently depends on the mixing rule. Mitigation: Remark A.1 and the tie table gain the research rows (gap (1.748, 2.124]; the partial-preparation tuple at r = 2 when the challenger may mix).
16. **Build outputs inside the Overleaf copy.** Mitigation: `-outdir` outside `overleaf/slot`.

---

## 6. Decision points for Austin

1. **The stray `ty` before the model section heading** (`02_model.tex:1`, from the last Overleaf edit; it prints). Recommendation: delete.
2. **Region panel.** Recommendation: yes, as panel (a) of Figure 2, with the benchmark path crossing the region on a logarithmic spread axis and entry along the path as panel (b); no renumbering. Alternative: a separate figure (the research figure becomes Figure 4). No non-uniform path in the main text.
3. **Fill the research figure.** Recommendation: yes: three equilibria on one continuous axis, a band where two coexist, no uncharacterized region.
4. **Scope trims.** Recommendation: keep Corollary A.2 as a benchmark statement, without generalizing its four cases; keep identification in Section 8 as one paragraph, because it states a positive result where the paper had a nonidentification result, at little cost.
5. **Optional extensions.** Recommendation: A.7 extended to ranked classes (one clause in Section 6.3); A.9 kept with two class values; A.5 kept on the uniform family.
6. **1 + u = e.** Recommendation: keep.
7. **Consumers.** Recommendation: only `comparison.tex` and `slides.tex`, but budget `comparison.tex` as a redesign: no status column, two set-ups side by side instead of a version history.
8. **Where scripts write.** Recommendation: the master `overleaf/slot/`, through one output-root setting shared by `make_numbers.py`, `number_scan.py` and `make_figures.py`, with the font path fixed; the mirror follows by subtree pull after the approved push.
9. **"The strong type's share of takeovers."** Recommendation: class H's share of the takeovers that go to the challenger, stated in Proposition 2(ii) under outbidding, with the strictness condition; benchmark 6/11 to 0.83.
10. **"Quiet market."** Recommendation: adopt it as the one name for the equilibrium without informed trade throughout the main text (it is the title of Proposition 3); N stays as the figure and table label.
11. **The worked example.** Recommendation: keep the name "the benchmark" (about 60 uses, consumers, registry); declare it once in a new Section 2.5. Recommended without a decision: reorder Section 3.1 so that Proposition 1 precedes the benchmark closed forms.
12. **Form of Proposition 3(c).** Recommendation: the balance condition as hypothesis, with the uniform separated-and-affordable incumbent as its primitive case, if Stage 1 confirms the implication; otherwise the two as alternatives.
13. **Decisive advantage in the main text.** Recommendation: yes: one sentence in 4.1, the benchmark check in 4.2 and the cost window in 4.3; it explains why the benchmark's ownership rise is no accident of the path.
14. **Empirical sentence in the abstract.** Recommendation: leave the empirics to the introduction; with the sentence the abstract reaches about 225 words. Add it only if Austin prefers a longer abstract.
15. **Notation.** Recommendation: r_{λ̄} for the cap strength (or words), r_Q for the end of floor-entry research, α_I and α_C for the signal accuracies, and "ceiling" kept for both r_C and (H3), since both name the point beyond which no price recruits (this declines the scan's "exclusion condition").

---

## 7. What the other two lenses might miss

1. **The language rules reach well beyond the main text.** About 100 process phrases in A3 to A9 ("calibration B", script and run-log names, "certificate", "Value at B", "S(B)"); certificates paragraphs in A4 and A5 must become statements of method. `comparison.tex` is a redesign (point 5 of Part 5).
2. **Every "Proposition 4(b)" anchor.** `05:143`, `05:156`, the statement and proof of `prop:researchregion`, `rem:researchties`, slides 484 and 776, comparison row 207. Missing one leaves a reference to a part that no longer exists.
3. **The research display and its polynomial.** `eq:research` gains the sale's profit; `eq:a5-F` and step 4 of A5's benchmark proof rest on the old form, and the A5 paragraph "The branch at calibration B" ends the equilibrium at the cap.
4. **The tie remark needs the research rows.** The abstaining-investor gap on (1.748, 2.124] and the partial-preparation tuple must live in Remark A.1 or the tie table, since the main text names the mixing rule only as a hypothesis.
5. **Numbering stability for consumers** (Part 4 policy). A new numbered corollary for the uniform interval, or a new research table in A5, silently breaks `comparison.tex` (Corollary A.2, Table A.4, Table A.6).
6. **Pipeline paths.** `make_numbers.py` and `number_scan.py` target the mirror; `make_figures.py` targets the mirror with a Linux font path; a clean scan proves nothing about the master until they are repointed.
7. **The roadmap claim at `01:139`** that the appendix "states the full form of Proposition 3" becomes false once Proposition 3 is general.
8. **The prior-1/2 identity in A8.** `A8:8` sets ϑ = u/(2+u) = 2M − 1 = M − m; only the first equality holds at every prior. Section 8's class component must read ρΔ(M − m).
9. **Figure labels are prose too.** "equilibrium set not characterized" and "beyond r_N" in `make_figures.py` are status-like statements; the R-sweep of `.tex` files does not see them.
10. **New example-only numbers need checker rows** (takeover shares, the cost window, r_Q); without them `number_scan.py` passes while the release gate does not.
11. **Corollary A.2's proof** cites the root-count part (b) of the path lemma; when that part becomes a hand proof, the corollary's citations change with it.
