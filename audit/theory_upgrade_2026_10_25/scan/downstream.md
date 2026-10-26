# Downstream-consumer report: theory upgrade of Propositions 3, 4, A.2, Corollary A.2 and A.11–A.14

I changed no files and ran nothing. Everything below is from reading files and grep. Paths are relative to `the repository root`. `OL` means `overleaf/slot`, `SM` means `slot/manuscript`, and `AUD` means `audit/slot_manuscript_2026_10_23`.

## 0. Findings that affect planning

- **Counters.**
  - Numbering is automatic from `main.tex:34-43` and `:123-132`. Main text has Proposition 1–4. The appendix prints Proposition A.n, Lemma A.n and Corollary A.n from separate counters.
  - The labels do not match the printed kinds. `prop:priors` is Corollary A.2 (cor:exclusion A.1, prop:priors A.2, cor:purchasesonly A.3). `prop:researchregion` is Proposition A.2. The empirical statements are A.11 `prop:spread`, A.12 `prop:informedshare`, A.13 `prop:winner` and A.14 `prop:announcement`.
  - `comparison.tex`, `slides.tex`, the study guide, the website and the web slides hard-code these numbers in prose. None uses `\ref`.
  - A new reduction lemma in the main text gets its own counter ("Lemma 1") and shifts nothing. A new appendix lemma shifts Lemma A.1–A.3, which `comparison.tex` cites. A new appendix proposition or corollary shifts everything after it.
- **Status labels.** Result-status words (analytical, computer-assisted, numerical diagnostic, open) appear only in `comparison.tex`. The manuscript and `slides.tex` have none. The registry `status` column is per value, so benchmark values keep their statuses.
- **Pipeline paths.** The numerics write to `SM`, not `OL`, even though `OL` is now the master. This affects §6.
  - `AUD/scripts/_coordinator/make_numbers.py:14` writes `SM/numbers.tex`.
  - `number_scan.py:9` scans `SM`.
  - `AUD/scripts/F_figures/make_figures.py:36` writes to `SM/figures`.
  - `make_figures.py:38` hard-codes a Linux Fira path under `/home/uctpiaj/...`, so the figures cannot be regenerated on this Mac without editing it.
- **Condition 1−ρ/2 versus 1−ρ.** The current proof has two different bounds in play.
  - `OL/appendix/A4_coexistence.tex:96` uses M < 1−ρ/2, which orders r_F < r_N.
  - A4:505 uses τ_A < 3/4 = 1−ρ for Corollary A.2 at every prior (the `margin_tauA_3q_B` key).
  - Your τ_A < 1−ρ/2 is the prior-1/2 form, which gives r_A < r_N when ρΔ(r_A)/2 < k.
  - The general Corollary A.2 will need 1−ρ, not 1−ρ/2. Decide which one each statement uses before adding keys.

## 1. `OL/comparison.tex`

**Numbering and status paragraph**

| Line | Current text | Change |
|---|---|---|
| 66-67 | "Propositions 1 to 4 in the main text, Propositions A.1 to A.14 in the appendix" | Update if the reduction lemma or a new corollary or proposition is added. A main-text lemma shifts nothing. |
| 69-70 | "Each result carries one status label…" | No change. Add that a general statement and its benchmark instance can carry different labels. |

**Section 2: the two set-ups**

| Line | Current text | Change |
|---|---|---|
| 84-92 | "The auction objects are t_0, t_j, g_j and Δ_T… Proposition 1 of either manuscript" | Add one sentence on the reduction lemma. The game depends on the auction only through Δ_T(F), τ(F), t_0 and t_L in price levels. Say whether it holds in both set-ups. |
| 133-144 | "Lemma A.1… Lemma A.2… Lemma A.3" | Renumber if the new lemma sits in the appendix lemma counter. |
| 168 | Table row "Added assumptions" | Add for the slot: ranked classes G_H, G_L, a stochastically ordered family F_r, the J condition. |
| 200, 201 | "Lemma A.1…", "Lemma A.2… Lemma A.3" | Same renumbering. |

**Section 3: the results table (`tab:results`)**

| Line | Current text | Change |
|---|---|---|
| 205 | Row "Coexistence at the benchmark"; slot cell: "Proposition 3: the complete equilibrium set on [r_0,r_2] at prior 1/2… Computer-assisted (two Sturm counts)." | Rename the row. State the general pointwise characterization and "entry rises along the coexisting branch". State the interval statement under the J condition. Move the thresholds [r_A,r_N] = [rA,rN] and "entry … beside no trade" into a "benchmark worked example" clause. Relabel: the general part is analytical, the benchmark thresholds are computer-assisted. The Laplace cell is unchanged. |
| 206 | Row "Coexistence at other priors"; "Corollary A.2… π_A^lo… π_max… Computer-assisted." | Same treatment. General Corollary A.2 is analytical under its condition. The `piA_lo_B`, `pimax`, `piA_hi` values and the CM remark (`margin_cmend_B`) stay as benchmark instance, computer-assisted. |
| 207 | Row "Research"; "Proposition 4, Proposition A.2: … Slope analytical, lists and values computer-assisted." | Say 4(a) is general (analytical: research and entry rise with Δ_T; ownership needs W_H = 1). 4(b) and A.2 stay at the benchmark. |
| 215 | Row "Empirical implications"; "Propositions A.11 to A.14… orders predict the winner above r_C… Analytical; values computer-assisted." | Say these hold for general F. Say the winner-gap rise needs W_H > W_L. Keep `ba_r1_B`, `ba_share_r1_B` as the benchmark instance. |
| 202 | Proposition 2 row | No change. |

**Section 3 prose**

| Line | Current text | Change |
|---|---|---|
| 219-225 | "the slot replaces three certified points with a complete equilibrium set, and it adds research, coexistence at every prior and derived observables" | Scope "complete equilibrium set" to the benchmark. Add "pointwise characterization for general F". |
| 231-234 | "The whole set is known at every strength on the path (Proposition 3)… a stronger completeness claim along the path" | Rewrite the scope: the complete set is known at the benchmark. For general F the statement is pointwise coexistence plus an interval under the J condition. |
| 253 | "mixes on (r_N,r_S) and sells with probability one from r_S (Proposition 3; computer-assisted)" | Mark as benchmark. |
| 266-270 | "entry rises strictly on [r_A,r_F]… (Proposition 3(b); computer-assisted)… The rise needs rule IM" | Add the general "entry rises along the branch". Keep the benchmark endpoints as an example. Re-check the part letters. |
| 272-279 | "entry rises strictly on [res_rR, res_rcap)… (Proposition 4; slope analytical, values computer-assisted)" | Cite 4(a) for the general slope and 4(b) for the benchmark interval. |
| 291-295 | "No trade and an informative equilibrium coexist exactly on [r_A,r_N]… (Proposition 3; computer-assisted)" | Mark as benchmark. Add the general pointwise condition. |
| 300-305 | Research paragraph | Add that 4(a) is general. The open set on (r_N, r_U^R) stays benchmark-only. |
| 351-358 | "S = ρΔ_Tϑ+(1−ρ)J A(M)… orders predict the winner among prepared challengers above r_C (Proposition A.13)" | Note the general-F form. For A.13, "mu W_H(F)+(1−mu)W_L(F)" replaces "mu+(1−mu)ℓ/r". Note the extra condition for the rise. |
| 360-362 | Observation protocol paragraph | No change. |

**Section 5: where each set-up stands**

| Line | Current text | Change |
|---|---|---|
| 436-446 | Margins section | Add the new hypotheses to the list of strict conditions. |
| 654-667 | "Table A.6 lists every strict hypothesis… Two monotonicity steps on the path rest on exact Sturm counts…" | The J, Δ(1−τ)² and Δτ monotonicity steps (Lemma `lem:a4-path`(b)–(d)) become conditions of the general statement. They are certified only at the benchmark. Reword. |
| 664 | "The strict rise on [r_A,r_F] needs IM" | Still true. Check the general statement says so. |
| 671-702 | `tab:thin` | Optionally add rows for any new thin margin. Keys are in §3. |

**Section 6: decision points**

| Line | Current text | Change |
|---|---|---|
| 708-711 | Decision point 1 | The slot now also offers general-F statements. |
| 712-714 | Decision point 2 | Qualify "[r_A,r_F], rule IM". |
| 726-728 | Decision point 7 | "Open items" stay. Add that the equilibrium set off the benchmark is characterized pointwise only. |

Optional: a decision point on "benchmark versus general scope of each statement".

**Language.** `comparison.tex` uses "high class" and "low class" at lines 90, 116, 150, 247, 331, 382, 641, 642. Lines 247, 331, 641 and 642 describe the Laplace manuscript and can stay. Lines 90, 116, 150 and 382 are generic or slot text and should use "class H" and "class L".

## 2. `OL/slides.tex`

| Frame / line | Current text | Change |
|---|---|---|
| F12, 456 | `\framesubtitle{Proposition 3 at fixed $\lambda$: no trade and informative trade side by side}` | State that the result is general and the thresholds are the benchmark example. |
| F12, 464-466 | "On [rA,rN], no informed trade (N) and an informative equilibrium coexist… the high class mixes… stays flat at entry_r1_B until r_C" | Mark as "At the benchmark". Add a bullet for the general pointwise condition. Replace "high class" with "class H". |
| F12, 468 | `\TakeawayWithNav… {Coexistence spans $[r_A,r_N]$.}` | Mark as benchmark. |
| F12, 459 | `coexistence_talk.pdf` | Stays valid as the worked example. |
| F13, 476 | `\framesubtitle{Proposition 4: costly research sets presence…}` | Mention that part (a) is general. |
| F13, 484 | `…entry rises from res_entry_rR to res_entry_cap (Proposition 4(a))` | This is benchmark content. Re-point to 4(b). Put the general rise in Δ_T under 4(a). |
| F13, 481 | `research_talk.pdf` | Stays valid. |
| F16, 545 | `Propositions A.11--A.14` | Update if the numbering changes. |
| F16, 548-550 | "Spread… Full orders: the unique outcome for r>r_S… Winners: orders predict the winner even above r_C" | Winners now hold when W_H > W_L. Say the other bullets hold at the benchmark. |
| A2 notation, 602-640 | Notation table | Add J = Δ_T(1−τ), W_H, W_L, F if used. Line 614 "h,ℓ; π benchmark class values" already marks the benchmark. |
| A8, 747 | "Value at the benchmark" | Keep. Add a line that thresholds are defined through Δ_T(F) and τ(F). |
| A8, 760-763 | "Before r_A, a buy order cannot pay at any mix rate…" | Mark "under the J condition". |
| A9, 773 | `(Proposition 4)` | Fine. |
| A9, 776 | `(Proposition 4(a))` | Re-point to 4(b). |
| A5, 678-700 | Admissible-region table | Add rows only if new conditions get a frame. |
| A10, 786-804 | Extensions table | No change. |

- **Language.** Slides use "class $H$" in most places. "High class" and "low class" remain at 465, 753 and 829.
- **Reduction lemma.** A backup frame fits after F3 (217-245) or in the appendix. The 20 main plus backup budget allows it, and the new frame needs `\hypertarget` and `\BackButton` links.
- **Key list.** `AUD/memos/W2_keys.md` (160 lines) lists keys by frame, so new keys go there.

## 3. Registry and numbers pipeline

**Rows that feed the affected statements**

- **Proposition 3 and Corollary A.2.** All in `AUD/registry/P1_core.csv`. Source is `scripts/P1_core/p1_numbers.py` (writes `P1_core.csv`) and `p1_certificates.py` (log only).
  - Thresholds and entries: `rA, rF_B, rN, rJ, rS_B, rC_B, rstar, entry_rA_B, entry_mb_r140_B, entry_mb_r145_B, entry_r1_B, entry_th_r155_B, entry_th_r160_B, entry_th_r165_B, entry_cmend_B, str_r140, str_r145`.
  - Auction values on the path: `tau_r0_frac, tau_r2_frac, J_r0, QJ_r0, rhoJ_r1, rhoJ_r2, Delta_rA`.
  - Prior cut points and margins: `piA_lo_B, piA_hi, pimax, M_pimax_B, mu0_pimax_B, margin_cmend_B, margin_piA_lo_B, margin_piA_hi, margin_pimax_tauA_B, margin_tauA_3q_B`.
  - Other margins: `margin_J_r0_B_frac, margin_rhoJ_r1_B_frac, margin_rhoJ_r2_B_frac, margin_rhoJ_2_B_frac, margin_Delta_pos_B_frac, margin_gHgL_B_frac, margin_tau_r0_half, margin_tau_r2_3q_B_frac, margin_tau_rN_half_B, margin_u_kstrong_B, gap_*_B`.
- **Proposition 4 and Proposition A.2.** All in `P3_research.csv`. Source is `scripts/P3_research/P3_research.py`.
  - Branch ends and parameters: `res_rR, res_rcap, res_rN, res_rUR, res_rC, res_rA, res_a, res_cap, res_a_lo, res_a_up, res_cap_lo, res_cap_hi, res_cap_lo_a, res_beta_lo, res_beta_hi`.
  - Branch values at the three strengths: `res_lambda_*, res_entry_*, res_own_*, res_lamE_*, res_tau_*, res_Delta_*, res_muplus_*, res_th_*`.
  - Monotonicity of the recruitment margin φ_a: `res_phi_r155, res_phip_lb, res_dphi_lead, res_amono, res_amono_third, res_bound_dDelta, res_bound_tau74, res_bound_Delta74, res_bound_taup, margin_res_amono_B`. These already certify φ_a strictly increasing on [6/5, 7/4] at a = 1/40 and for a below `res_amono`.
  - Other margins: `margin_res_*`.
  - Proposition 4(a) itself prints no registry number. Its "W_H = 1 because h > r" is a text literal.
- **A.11–A.14.** All in `P5_observables.csv`. Source is `scripts/P5_observables/p5_observables.py`.
  - Spread: `ba_r1_B, ba_r2_B, ba_share_r1_B, ba_class_r1_B, ba_entry_r1_B, ba_rC_left_B, ba_rC_right_B, ba_jump_rC_B`.
  - Informed share: `theta_*, theta_min_counts_B, theta_max_full_eq_r1_B, theta_max_full_eq_r2_B`.
  - Winner (A.13): `wgap_r1_B, wgap_r2_B, cov_win_r1_B, cov_win_r2_B, win_prob_r1_B, win_prob_r2_B`. The `wgap` note reads "theta(1-l/r)" (`p5_observables.py:609-610`).
  - Announcement and clusters: `evprep_mean_r1_B, evprep_mean_r2_B, pdrop_neutral_r1_B, imb_buy_B, U_gap_r160_B, mix_*`.
  - Margins: `margin_obs_*`.
- **Ownership.** `own_r0, own_r1_B, own_r2_B` (P1_core, note "W_H = 1") and `margin_p4_ownership_rise_B` (`P4_information.csv`, source `scripts/P4_information/derive.py`).

**Existing keys that already certify the conditions you named**

| Condition | Existing key or evidence |
|---|---|
| J strictly increasing on the path | The Sturm count (no real root of Q_J on (6/5, 18/5]) is in `P1_core/p1_certificates.log` item 3 only. The registry holds just `QJ_r0` (the sign at r_0). |
| J(r_0) < k | `margin_J_r0_B(_frac)`. |
| ρJ(r_1) > k and ρJ(r_2) > k | `margin_rhoJ_r1_B(_frac)`, `margin_rhoJ_r2_B(_frac)`. |
| ρJ(2) > k | `margin_rhoJ_2_B(_frac)`. |
| τ_A < 1−ρ (the form Corollary A.2 uses) | `margin_tauA_3q_B`. |
| φ_a single crossing | See the list above. It covers [6/5, 7/4] only. |

**New keys likely needed.** Use the BRIEF pattern `margin_<condition>_B`.

| Condition | Proposed key | Value / note | Write it in |
|---|---|---|---|
| τ_A < 1−ρ/2 (prior-1/2 form; implies r_A < r_N) | `margin_tauA_half_B` | 7/8 − τ_A ≈ 0.2343, from the `tA_hi` bracket | `p1_numbers.py`, near line 432 |
| M < 1−ρ/2, giving r_F < r_N | `margin_M_78_B` | Currently only in the log (`p1_certificates.py:141`, "M_hi − 7/8"). Optional. | `p1_numbers.py` |
| J single crossing on the path | `sturm_QJ_B` (count 0), or a rational lower bound on J′ | Now log-only. | See the file note below. |
| Δ(1−τ)² and Δτ increasing | Same pattern | Log-only items 4 and 5. | See the file note below. |
| W_H = 1 | `margin_WH_B` | h − r_2 = 32/5 | `p1_numbers.py` or `P4_information/derive.py` |
| W_L(F_r) at the benchmark, for A.13 | `WL_r1_B` (1/3), `WL_r2_B` (5/18) | Optional; or fold into the `wgap` notes. | `p5_observables.py` |
| Slope of W_H − W_L | Optional, e.g. ℓ/r² | | `p5_observables.py` |
| Stochastic-order condition | None | Analytic at the benchmark. | |

- **Where to write J, Δ(1−τ)² and Δτ.** `p1_certificates.py` has no registry writer. Either add rows in `p1_numbers.py` (the QJ block is at lines 348-354) or let `p1_certificates.py` write a new `AUD/registry/P1_cert.csv`. `make_numbers.py` globs every `registry/*.csv` except `HEADER.csv` and `registry.csv`, so a new CSV file merges with no code change.
- **Checker rows.** Each new row needs an independent checker row per the ledger discipline. Targets are `XP1/xp1_numbers.py` with `xp1_registry_recompute.csv`, `XP1b/xp1b_recompute.py` and `xp1b_intervals.csv` for the P1 additions, `XP3/recompute.py` for P3, and `XP5/recompute.py` for P5 changes.

**Possible orphans.** The scan used 677 keys against 5,221 registry rows, with 0 missing.
- `margin_tauA_3q_B` (A4:506, A9:135) stays used if Corollary A.2 keeps τ_A < 1−ρ. It is orphaned only if the proof switches entirely to 1−ρ/2.
- `margin_tau_r2_3q_B(_frac)` is used only at A9:121. A4:23 and A4:102 print "3/4" as a literal. It is orphaned if the "M < 3/4" step is dropped.
- `QJ_r0` and `J_r0` (A4:24) stay used.
- No benchmark statement is deleted, so the other keys stay. The `3/4` and `7/8` literals pass `number_scan.py`, which flags only decimals with two or more places.

## 4. Figures

| Figure | Script | Labels and captions | Change |
|---|---|---|---|
| `coexistence.pdf`, `coexistence_talk.pdf` | `AUD/scripts/F_figures/make_figures.py`, function `fig_coexistence` (line 443). `draw_branches` (line 412) is the drawing helper. | No in-figure title. Axes are "incumbent strength, r" and "total entry, E". Branch labels N, R, F, Q, T. "Benchmark" appears only in a docstring. | Figure files unchanged. The caption is `OL/sections/04_equilibrium_results.tex:295` "Equilibrium entry along the benchmark path". Its notes (:298-307) say "The benchmark at the prior 1/2". Both stay if the figure is the worked example. |
| `research.pdf`, `research_talk.pdf` | `fig_research` (line 538) | Same style. | Caption `OL/sections/05_research.tex:~134`, notes at :138 "The benchmark with a=… and λ̄=…". Stays. |
| `beliefs.pdf`, `beliefs_talk.pdf` | `fig_beliefs` (line 336) | Same style. | Caption `04_equilibrium_results.tex:170` "Beliefs and the entry ceiling in the benchmark". Stays. |

- The scripts read the registry only to print a match log, and they use closed forms. No regeneration is needed unless the branch labels or thresholds are renamed.
- All six PDFs in `OL/figures` and `SM/figures` have identical sizes. `make_figures.py` writes to `SM/figures` only (see §0).

## 5. Other consumers (name only)

All of these restate the benchmark-path scope. Names marked "digit" cite benchmark digits.

**Inside the manuscript (cross-refs to re-point)**
- `OL/sections/01_introduction.tex:139` (full form of Proposition 3).
- `OL/sections/02_model.tex:124` (Propositions `prop:ccc` and `prop:coexistence` hold for…).
- `OL/sections/04_equilibrium_results.tex:300`, `:332` (Corollary `prop:priors`).
- `OL/sections/05_research.tex:113`, `:143`, `:154`, `:156` (4(a), 4(b), `prop:researchregion`).
- `OL/sections/08_empirical.tex:25, 35, 49, 54`.
- `OL/appendix/A3_proposition2.tex:131`.
- `OL/appendix/A8_empirical.tex:3`, `:147` (cites Proposition 3 for "exactly on [r_F,r_N] (form F)", a benchmark fact), `:156`, `:240`, `:246` (CM threshold pair).
- `OL/appendix/A9_parameters.tex:115` (Proposition 3 and Corollary A.2, "benchmark path", margins table).
- `OL/appendix/A9_parameters.tex:139` (Propositions 4 and A.2).
- `OL/appendix/A2_beliefs_trading.tex:235`.

**Slot study guide** (`slot/study_guide/`; digit unless noted)
- Chapters `08_coexistence.tex` (:57, :207, :233, :317), `09_research.tex` (:201 and its Proposition 4 box), `C_equation_map.tex` (:40, :94), `03_auction.tex:233`, `07_controls.tex:154,159`, `benchmark.tex:27`, `12_empirical.tex:141-151`.
- `verify/08_coexistence.py:183` (references `QJ_r0`).
- Built `index.html` and `web/assets/*.js`.
- Probably out of scope.

**Website** (`handout/`)
- `sections/03-result.html:35` and `sections/04-path.html:5, 10, 39, 47, 50, 53`.
- `slot_data.py:13, 35`, `explorer.js`, `charts.js`, `figures.js`, `README.md:14, 170-175`.
- Built `docs/index.html`.
- Probably out of scope.

**Web slides** (`presentation/`)
- `content.js:282, 292, 296, 437, 440` mirror slide frames F12, F13, A9.
- `notes.md:47`.
- `figdata.py:8, 80, 86`.
- Update with `slides.tex`.

**Discussion notes** (`discussion/2026-10-26/`, excluded from git by `.git/info/exclude`)
- `updates.html:338`, `ji-hee.html:403, 559`, `alex.html:604`, `alex_src/body.html`.
- State Proposition 3 and 4 at the benchmark.

**Audit records (frozen)**
- `AUD/LABELS.md:50-54`. It lists `prop:researchbranch`, which no longer exists.
- `AUD/memos/W1_keys.md`, `W2_keys.md`, `W3_comparison.md`.
- `AUD/proofs/P1_core.tex`, `P3_research.tex`, `P5_observables.tex`, and the matching `memos/P1_core.md`, `P3_research.md`, `P5_observables.md`.
- Leave them as records and add a general-F memo.

**Not slot-related:** `paper/`, `laplace/`, `talk/` and `learn/` concern the Laplace version.

## 6. Sync between `overleaf/slot` and `slot/manuscript`

- **Difference.** `diff -rq` outside `.git` shows one file differing. `OL/sections/02_model.tex` line 1 reads `ty\section{The model}\label{sec:model}`. `SM` reads `\section{The model}\label{sec:model}`.
  - The cause is the Overleaf commit `69c25f4` "Update on Overleaf." by Austin Li (24 Oct, 16:25). It changed that one line.
  - It looks like a stray "ty" typed in the editor. It prints "ty" before the section heading.
  - `OL` is clean and equals `origin/main` as of the last fetch. A dry-run fetch printed nothing, so I could not confirm the remote is current.
- **Identical copies.** `numbers.tex` and the six figure PDFs are identical in both trees. Their modification times differ only because `OL` was recloned.
- **Sync step.**
  1. Remove the stray "ty" at the Overleaf master (edit in Overleaf, or commit and push from `OL`).
  2. Bring `SM` up to date. `slot/README.md` says `SM` is a `git subtree` of the same remote, so run `git subtree pull --prefix=slot/manuscript https://git.overleaf.com/6adbcf95d3bcdaeacca72fcf main`. The parent tree has many unstaged changes (`docs/`, `handout/`, `slot/README.md`), so stash them first or copy the one file.
  3. Do all text edits in `OL`, because it is the master.
  4. Generated outputs land in `SM`, so after each run copy `SM/numbers.tex` and `SM/figures/*.pdf` into `OL`. Alternatively repoint `make_numbers.py:14`, `number_scan.py:9` and `make_figures.py:36` to `OL`.
  5. Re-run the diff before pushing `OL` to Overleaf.

## 7. Dependency-ordered downstream edits

1. **Fix the sync.** Remove "ty" at `OL/sections/02_model.tex:1`, pull `SM` current, and decide the pipeline direction (§6). Also decide the lemma placement (main text, or the appendix lemma counter), since it fixes all hard-coded numbers.
2. **Fix the condition set.** Decide 1−ρ versus 1−ρ/2 per statement, and the J, W_H and φ_a conditions. These fix the new-key list.
3. **Write the proofs and manuscript statements.** This is the planned theory edit. Change the main text (Sections 2.4, 3, 4.3, 5, 8, introduction), the appendix A2–A5 and A8, and the A9 margins table. Update labels and cross-refs (§5). Record the new labels in `AUD/LABELS.md`.
4. **Add the registry rows.** Edit `p1_numbers.py` (or add `p1_certificates.py` output as `P1_cert.csv`), `P3_research.py` (optional), `p5_observables.py` and, if used, `P4_information/derive.py`. Add the independent checker rows in XP1, XP1b, XP3 and XP5.
5. **Regenerate the numbers.** Run `make_numbers.py` and `number_scan.py` (a later step, not now). Copy `numbers.tex` into `OL`. Confirm 0 missing keys, no new typed decimals, and note any orphaned keys.
6. **Figures.** Regenerate only if branch labels or thresholds are renamed. This needs the Fira path fixed in `make_figures.py:38`. Otherwise keep the PDFs and update the captions (`04…:295`, `05…:~134`, `04…:170`).
7. **`comparison.tex`.** Update §1 of this report: numbers (66-67, 133-144, 200-201), rows 205, 206, 207, 215, the prose at 219-234, 253, 266-279, 291-305, 351-358, §5 at 436-446 and 654-675, and decision points 1, 2 and 7. Do this after the manuscript labels settle.
8. **`slides.tex`.** Update frames F12, F13, F16, A2, A8 and A9, add any reduction backup frame, and update `AUD/memos/W2_keys.md`.
9. **Downstream copies.** Update `presentation/content.js` and `notes.md`, the website sections `03-result` and `04-path`, the study guide chapters, and the discussion notes. The study guide and website are probably out of scope.
10. **Rebuild and check.** Rebuild `main.tex`, `comparison.tex` and `slides.tex`, and confirm there is no unknown key or undefined reference. Then sync `OL` and `SM` again (§6).
