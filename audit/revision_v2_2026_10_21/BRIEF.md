# Team 1 brief: revised manuscript after the supervisor meeting (21 October 2026)

Read this file before you start. Your own task prompt names your role and your output files.

Repository root: `/home/uctpiaj/work/Projects/competition-creates-competition` (paths below are
relative to it unless absolute).

## 0. What the author decided

1. **Reading N becomes the main model.** Nature draws the challenger's quality class
   `j ∈ {H, L}` with prior `π = Pr(j = H) ∈ (0, 1)`. Given the class, the challenger's value `θ` is
   drawn from the cdf `G_j`. The investor observes the class, not `θ`. The challenger knows neither
   before preparation; preparation reveals `θ`. Ranking: `G_H` first-order dominates `G_L` above
   the reserve, and both classes are equally likely to fall below the reserve ("equal
   admissibility"; the simplest case is that both supports lie above `p`). This is the
   selective-entry framework of the auction literature, with the stock price as the pre-entry
   signal.
2. **The benchmark stays the point-mass case with equal prior.** `G_L = δ_ℓ`, `G_H = δ_h`,
   `π = 1/2`. The general model is stated and proved in the text; the benchmark is "the point-mass
   case". This keeps the Proposition 3 certificates, Table 2 entry numbers, Section 5.1 and every
   figure valid as a special case. Section 6.3's ±0.05 value classes become the nondegenerate
   running example. (The author may revisit this later; do not change it.)
3. **`c_L = 0`.** The low-cost type's preparation cost is zero ("a ready buyer whose diligence costs
   nothing at the margin"). Keep the symbol `c_H` for the other cost (it is fixed in the numerical
   contract C.0); write one sentence that the other type's cost is zero. Condition (A1) disappears.
   The entry floor `ρ` then holds at every belief, so price sufficiency (Prop. A.2) is unconditional
   and price pooling (Prop. A.10, Online Appendix A.11, exercise C.6b) loses its premise.
4. **Laplace noise stays in the main model**, now justified technically and economically, stated as
   the extreme member of the bounded-score (log-Lipschitz) class, with Prop. A.5 generalized to that
   class and the Blackwell error corrected.
5. **Institutional motivation** for `t_0` and for the informed investor is added (who trades, who
   holds, what `t_0` does, how shareholders gain).
6. **No normalization is needed in the general statements.** The benchmark keeps `ℓ = 1` as its
   money unit and says so.

## 1. Notation sheet (use exactly this)

| Object | Symbol | Note |
|---|---|---|
| Quality class | `j ∈ {H, L}` | Say "class", not "type" (type = investor information) |
| Prior | `π = Pr(j = H)` | Benchmark `π = 1/2` |
| Value cdf of class j | `G_j` | Benchmark: point masses at `ℓ`, `h` |
| Challenger value | `θ` | Revealed by preparation |
| Incumbent value, cdf | `R`, `F` (uniform `[0, r]` leading case) | |
| Preparation cost | `C ∈ {0, c_H}`, `Pr(C = 0) = ρ` | `c_L` no longer appears |
| Class proceeds, profits | `t_0`, `t_j`, `g_j` | Class expectations of the per-value objects |
| Spread | `Δ_T = t_H − t_L` | |
| Posterior bounds | `m(π)`, `M(π)` | `m(1/2) = m`, `M(1/2) = M` of the paper |
| Trading-bound constant | `κ(π) = min{m(π), 1 − M(π)}` | Do **not** use `λ` (overloaded) |
| High-class win probability | `W_H` | For the ownership condition |
| Low-cost probability | `ρ` | |

Do not introduce `λ` for anything. If you need a new symbol, list it in your output header.

## 2. Sources to transcribe (do not re-derive)

All in `audit/alex_meeting_2026_10_21/memos/`. These claims were checked by an adversarial review
(`SYNTHESIS.md`, Part A). Transcribe them into paper prose and LaTeX; check each step as you write,
and report any step you cannot follow. Do not invent new results.

- `Q1_N_main.md`: Claims 4 (generalized Prop. 1 with the reserve term `pF(p)D(p⁻)`), 6 (posterior
  bounds with prior π), 7 (price sufficiency), 8–11 (trading bounds, Prop. 2 with general π,
  ownership condition, nonemptiness for every ranked pair), the split identity
  `Δ_T + (g_H − g_L) = E_H max{θ,p} − E_L max{θ,p}` (binary: `= h − ℓ` at every `r`), and §7.
- `Q1_N_extensions.md`: Claims 7–8 (more than two classes) — appendix remark only.
- `Q1_literature.md` §7: the selective-entry positioning sentences.
- `Q2_laplace_technical.md`: R8–R10 (Laplace is extremal; logistic = Laplace + independent noise),
  R12–R13 (clipped-Gaussian log odds; why Gaussian fails), R16 (Prop. 2 for every density with
  `|(log f)'| ≤ L < 1`, with the largest attained posterior in (A2)), §7 draft paragraph.
- `Q2_laplace_economic.md` §3.6: economic paragraph (three microfoundations). Use only verified
  citations (see `LIT_extracts.md` and §5 below).
- `Q3_story.md` §7.1–7.2: roles paragraph and shareholder paragraph. `Q3_welfare.md`: ledger
  identities W1–W5. `Q3_stake.md`: payoff split (S4)–(S5), bounds `Ω_U`, `Ω_0` (formulas).
- `Q4_normalization.md` §7: rewrites of eq. (4), (12), (A2)–(A3) (drop `ℓ = 1` from the general
  statement; keep it as the benchmark unit), and the identity `t_θ + g_θ = θ`.
- `SYNTHESIS.md` B.6: the exact replacement text for the Blackwell sentences.

## 3. Workspaces and ownership

- **Manuscript clone** (the only place where the manuscript changes):
  `overleaf/paper-revision/` on branch `revision-alex-2026-10-21`. Only the **integrator** edits
  `main.tex` and `online_appendix.tex` there. Everyone else reads it.
  Never edit `overleaf/paper/` (the live working copy). Never push anything.
- **Drafts**: `audit/revision_v2_2026_10_21/drafts/`. Each drafter writes LaTeX fragments there.
  Each fragment starts with a header block:
  `% REPLACES: main.tex lines X–Y ("first words …" to "… last words")` or `% INSERT AFTER: …`, so
  the integrator can apply it mechanically. Use the paper's existing macros and conventions:
  `\hyperref[...]{...}`, labels `result-proposition-…`, `eq:paper-…`, `\citeproc{ref-Key}{Author
  Year}`. The bibliography is embedded citeproc output: a new reference needs a new
  `\bibitem[\citeproctext]{ref-Key}` in the existing format (request it in your fragment header;
  the citation workstream supplies verified records).
- **Numerics worktree**: `/home/uctpiaj/work/Projects/ccc-revision-numerics` on branch
  `revision/alex-2026-10-21` (from `main`). Only the **numerics workstream** edits there. Python:
  `/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python`.
- **Numbers**: every number that changes or is new comes from
  `audit/revision_v2_2026_10_21/reconciliation.csv`, which the numerics workstream writes from validated
  pipeline outputs. Drafters write `\NUM{name}` placeholders for numbers they need and list them in
  their header; the integrator substitutes from the CSV. Do not type a new number by hand.

## 4. Rules (all members)

1. Do not write tests of any type. Print-only scripts are allowed; scripts with assertions are not.
2. Do not push, and do not commit, except the numerics workstream on its branch.
3. Do not name AI models, agents, or tools in any file.
4. Do not save downloaded files. Browser and paper-fetch work goes only to the citation workstream.
5. Keep proofs complete. Status vocabulary of the paper: analytical, computer-assisted, numerical
   diagnostic, open.
6. Style: match the manuscript's voice — plain, short declarative sentences, no new jargon, no
   rhetorical flourish. Prefer "uses" to "utilizes", avoid "-ing" forms where a simple verb works.
7. Do not hand any part of your task to others.

## 5. Citations already verified (safe to cite)

From `audit/alex_meeting_2026_10_21/memos/LIT_extracts.md` (read from full texts): Goldstein and
Guembel (2008, RES); Dow, Goldstein and Guembel (2017, JEEA); Edmans (2009, JF); Boleslavsky, Kelly
and Taylor (2017, JET); Levin and Smith (1994, AER); Marmer, Shneyerov and Xu (2013, Journal of
Econometrics); Gentry and Li (2014, Econometrica); Roberts and Sweeting (2013, AER); Chordia and
Subrahmanyam (2004, JFE); Augustin, Brenner and Subrahmanyam (2019, Management Science); Edmans,
Goldstein and Jiang (2015, AER; stake discussion in Section II.E).

Already in the paper's bibliography (keys `ref-…`): BettonEtAl2014, Blackwell1953,
BondEdmansGoldstein2012, BooneMulherin2007, BulowHuangKlemperer1999, BulowKlemperer1996,
CarlinEtAl2026, CornelliLi2002, DowGoldsteinGuembel2017, EdmansGoldsteinJiang2012,
EdmansGoldsteinJiang2015, Fishman1988, FoucaultFresard2014, GentryStroup2019, GoldsteinGuembel2008,
GorbenkoMalenko2014, GrossmanHart1980, HirshleiferPng1989, Imprivata2016, Kyle1985, LevinSmith1994,
LinMaYangZhu2025, LiuBernhardt2022, Luo2005, McAfeeMcMillan1987, PernoudGleyze2026, Persico2000,
RobertsSweeting2013, Samuelson1985, Schwert1996. Any reference not in this list must go through the
citation workstream, which returns a verified `\bibitem`.

## 6. Phases

1. Drafting (parallel): main-text rewrite (Reading N, Sections 1–4, Appendix A.1–A.4); noise
   justification and class result; institutional motivation; `c_L = 0` consequences (Sections 5–8,
   Appendix A.5–A.8, Online Appendix); numerics; citations.
2. Integration into the clone, compile both documents.
3. Review: proofs, consistency, referee read, prose and LaTeX.
4. Fixes, final compile, delivery.

## 7. New citation keys (the citation workstream verifies these; use only these keys)

Use `\citeproc{ref-KEY}{Author Year}` with these keys. The citation workstream writes verified
`\bibitem` records to `drafts/F_bibitems.tex`; the integrator drops any key it could not verify
(and the sentence that needs it, or rewrites the sentence).

| Key | Reference |
|---|---|
| MarmerShneyerovXu2013 | Marmer, Shneyerov and Xu (2013), Journal of Econometrics, selective entry |
| GentryLi2014 | Gentry and Li (2014), Econometrica, affiliated-signal entry model |
| Ye2007 | Ye (2007), Games and Economic Behavior, indicative bidding |
| KyleVila1991 | Kyle and Vila (1991), RAND Journal of Economics, noise trading and takeovers |
| Meulbroek1992 | Meulbroek (1992), Journal of Finance, insider trading before takeovers |
| AugustinBrennerSubrahmanyam2019 | Augustin, Brenner and Subrahmanyam (2019), Management Science |
| AcharyaJohnson2010 | Acharya and Johnson (2010), Journal of Financial Economics |
| Edmans2009 | Edmans (2009), Journal of Finance, blockholder trading |
| Maug1998 | Maug (1998), Journal of Finance, large shareholders as monitors |
| BackEtAl2018 | Back, Collin-Dufresne, Fos, Li and Ljungqvist (2018), Econometrica |
| SmithSorensen2000 | Smith and Sørensen (2000), Econometrica, bounded private beliefs |
| KotzKozubowskiPodgorski2001 | Kotz, Kozubowski and Podgórski (2001), The Laplace Distribution and Generalizations |
| Clark1973 | Clark (1973), Econometrica, subordinated process |
| Cont2001 | Cont (2001), Quantitative Finance, stylized facts of returns |
| Vickrey1961 | Vickrey (1961), Journal of Finance |
| Krishna2010 | Krishna (2010), Auction Theory, 2nd ed. |
