# W2: registry keys in slides.tex

Workstream W2 (slides). The deck `overleaf/competition_slot/slides.tex` prints each value with `\reg{<key>}`.
This memo lists each key in the deck, with its object and its main frame or backup frame.
Frame ids M1 to M20 name main frames in talk order. Ids A1 to A12 name backup frames.
Keys with the mark (BRIEF) come from the starter list in BRIEF §6. Other keys follow the same pattern.

## Benchmark inputs (M9, A5)

| Key | Object | Where |
|---|---|---|
| `prim_h` | class $H$ value $h$ at the benchmark | M9 |
| `prim_ell` | class $L$ value $\ell$ at the benchmark | M9 |
| `prim_p` | reserve $p$ | M9 |
| `prim_pi` | prior $\pi$ on class $H$ | M8, M9, A5 |
| `prim_rho` | probability $\rho$ of cost $c_L$ | M9 |
| `prim_cL` | low preparation cost $c_L$ (zero) | M5, M8, M9 |
| `prim_cH` | high preparation cost $c_H$ | M9 |
| `prim_k` | order cost $k$ | M9, M10 |
| `prim_r0`, `prim_r1`, `prim_r2` | strengths $r_0$, $r_1$, $r_2$ | M9, M13 |
| `beta_B` (BRIEF) | liquidity order chance $\beta$ at B | M9, A5 |
| `lambda_B` (BRIEF) | informed presence chance $\lambda$ at B | M9, A5 |
| `u_B` (BRIEF) | informed odds $u=\lambda/b$ at B | M9, A5 |
| `b_B` (BRIEF) | $b=(1-\lambda)\beta$ at B | M9 |

## Beliefs and auction objects (M8, M10, M11)

| Key | Object | Where |
|---|---|---|
| `M_half_B` (BRIEF) | top belief $M(\pi)$ at the benchmark prior | M8, M11, A4, A5 |
| `m_half_B` (BRIEF) | low belief $m(\pi)$ at the benchmark prior | M8, A4 |
| `tau_r0`, `tau_r1`, `tau_r2` (BRIEF) | threshold belief $\tau(r)$ at $r_0$, $r_1$, $r_2$ | M11 |
| `Delta_r0` | spread $\Delta_T(r_0)$ | M10, M13 |
| `Delta_r1` | spread $\Delta_T(r_1)$ at B | M13 |
| `Delta_r2` | spread $\Delta_T(r_2)$ at B | M13 |
| `Bprior_r0` | gross profit $B_{r_0}(\pi)$ at the prior | M13, A7 |
| `Bprior_r1_B` | gross profit $B_{r_1}(\pi)$ at B | M13, A7 |
| `Bprior_r2_B` | gross profit $B_{r_2}(\pi)$ at B | M13, A7 |
| `trade_bound_r1_B` | bound $\rho\min\{m,1-M\}\,\Delta_T(r_1)$ at B | M10 |

## Entry, ownership and thresholds (M3, M13, M15, A7, A8)

| Key | Object | Where |
|---|---|---|
| `entry_r0` (BRIEF) | entry at $r_0$ | M3, M13, M14, M20, A7 |
| `entry_r1_B` (BRIEF) | entry at $r_1$ at B | M3, M13, M14, M20, A7 |
| `entry_r2` (BRIEF) | entry at $r_2$ | M13, M20, A7 |
| `own_r0` (BRIEF) | class $H$ ownership at $r_0$ | M13, A7 |
| `own_r1_B` (BRIEF) | class $H$ ownership at $r_1$ at B | M13, A7 |
| `own_r2_B` (BRIEF) | class $H$ ownership at $r_2$ at B | M13, A7 |
| `entry_branch_B` | flat entry on the informative branch past $r_F$, at B | M15 |
| `rA` (BRIEF) | start $r_A$ of coexistence | M15, A8 |
| `rF_B` (BRIEF) | end $r_F$ of the mix part of the branch, at B | M15, A8 |
| `rN` (BRIEF) | no-trade boundary $r_N$ | M15, A8 |
| `rC_B` (BRIEF) | ceiling strength $r_C$ at B | M13, A8 |

## Controls (M14)

| Key | Object | Where |
|---|---|---|
| `ctrl_fixed_r0` | entry at $r_0$ with full orders set by fiat | M14 |
| `ctrl_fixed_r1_B` | entry at $r_1$ with full orders set by fiat, at B | M14 |
| `ctrl_hidden_r0` | entry at $r_0$ with the price hidden | M14 |
| `ctrl_hidden_r1_B` | entry at $r_1$ with the price hidden, at B | M14 |

## Admissible region (M17, A5)

| Key | Object | Where |
|---|---|---|
| `u_lo`, `u_hi` (BRIEF) | low and high ends of the admitted band for $u$ | A5 |
| `M_lo`, `M_hi` (BRIEF) | low and high ends of the admitted band for $M$ at the benchmark prior | A5 |
| `prior_lo_B`, `prior_hi_B` (BRIEF) | prior range for Proposition 2 at B | M17, A5 |

## Research (M16, A9)

| Key | Object | Where |
|---|---|---|
| `res_a` (BRIEF) | research cost parameter $a$ | A5, A9 |
| `res_cap` (BRIEF) | research cap $\bar\lambda$ | A5, A9 |
| `res_a_lo`, `res_a_hi` | admitted range for $a$ | A5 |
| `res_cap_lo`, `res_cap_hi` | admitted range for the cap | A5 |
| `r155_val`, `r160_val`, `r165_val` | the three intermediate strengths in the research table | M16, A9 |
| `res_lambda_r155`, `res_lambda_r160`, `res_lambda_r165` (BRIEF pattern) | research $\lambda$ on the research branch at those strengths | M16, A9 |
| `res_entry_r155`, `res_entry_r160`, `res_entry_r165` (BRIEF pattern) | entry on that branch at those strengths | M16, A9 |

## Robustness, welfare and sale terms (M17, M18, A10, A12)

| Key | Object | Where |
|---|---|---|
| `atomless_entry_r1_B` | entry at $r_1$ with atomless costs, at B | M17 |
| `sig_entry_weak` | entry at the weak strength in the signal example | M17 |
| `sig_entry_strong` | entry at the strong strength in the signal example | M17 |
| `access_scale_B` | break-even trade scale in the price-access comparison, at B | A10 |
| `proc_seen_B` | expected proceeds at $r_1$ with the price seen | M18 |
| `proc_hidden_B` | expected proceeds at $r_1$ with the price hidden | M18 |
| `proc_gain_B` | proceeds gain from price access at $r_1$ | M18, A12 |
| `surp_seen_B` | net surplus at $r_1$ with the price seen | M18 |
| `surp_hidden_B` | net surplus at $r_1$ with the price hidden | M18 |
| `surp_gain_B` | net surplus gain from price access at $r_1$ | M18, A12 |
| `reserve_excl_B` | exclusion reserve at B | A12 |
| `reserve_strict_B` | reserve level with strict reserve deterrence, at B | M18, A12 |

## Notes for the merge step

- The deck has no other `\reg` key. A text search for `\\reg{` in `slides.tex` gives this set.
- Formula constants stay in the source as symbols: the order set $\{-1,0,1\}$, the bound $1/3$ on $\beta$, and $1+u=e$.
- Years in citations and proposition numbers stay in the source as text.
- Where a manuscript key for the same object exists under another name, one rename in `slides.tex` per key aligns the deck.
- Candidate matches in team rows at draft time, for the merge step to confirm: `atomless_entry_r1_B` with
  `p4_atomless_r1_entry`; `ctrl_fixed_r0`, `ctrl_fixed_r1_B` with `p4_frozen_r0_entry`, `p4_frozen_r1_entry`;
  `ctrl_hidden_r0`, `ctrl_hidden_r1_B` with `p4_hidden_r0_entry`, `p4_hidden_r1_entry`;
  `proc_gain_B`, `surp_gain_B` with `p2_access_proceeds_gain`, `p2_access_surplus_gain`;
  `access_scale_B` with `p2_access_break_even`. Signal-example rows exist under several `p4_*_signal_*_entry`
  names; the merge step picks the manuscript example for `sig_entry_weak` and `sig_entry_strong`.
- The spread keys use the P1 and manuscript names `Delta_r0`, `Delta_r1`, `Delta_r2`. No `spread_*` key remains.
- For `entry_branch_B`, P1 rows `entry_th_r155_B` to `entry_th_r165_B` are candidates; the merge step confirms.

## Round 2 changes (23 October 2026)

The deck now follows the finished manuscript (`overleaf/competition_slot/main.tex`, Sections 1–9 and the abstract).
Frames: title, 20 main frames (M1–M20), an appendix divider, and 12 backup frames (A1–A12); 34 pages in total.
Build: `latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build slides.tex` from
`overleaf/competition_slot/` exits 0 with no overfull box and no unknown `\reg` key.
Renders: `scripts/W2/png/slide-01.png` to `slide-34.png` (110 dpi); each frame was read and the three figure
frames and backup A8 were re-set after the first build.
Number scan: `.venv/bin/python audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py` reports
0 missing keys and 0 literal decimals. The deck prints 85 distinct registry keys.

### Key remap (round-1 key to manuscript key)

| Round-1 key | Manuscript key (or removal) |
|---|---|
| `prim_cL` | removed; the low cost prints as the exact `0`, as in Section 2.2 |
| `trade_bound_r1_B` | no registry row holds the bound itself; M10 and M12 now state (H2) with `margin_kstrong_B` (the excess of the bound over `k`) |
| `Bprior_r2_B` | `Bprior_r2` |
| `ctrl_fixed_r0`, `ctrl_fixed_r1_B` | `p4_frozen_r0_entry`, `p4_frozen_r1_entry` |
| `ctrl_hidden_r0`, `ctrl_hidden_r1_B` | `p4_hidden_r0_entry`, `p4_hidden_r1_entry` |
| `entry_branch_B` | `entry_r1_B` (Section 4.3: entry stays at this level from `r_F` to `r_C`) |
| `r155_val`, `r160_val`, `r165_val` | `str_r155`, `str_r160`, `str_r165` |
| `atomless_entry_r1_B` | `p4_atomless_r1_entry` |
| `sig_entry_weak`, `sig_entry_strong` | `p4_comp_b_r0_entry`, `p4_comp_b_r1_entry` (the pair at `B`, accuracies `sig_comp_aT`, `sig_comp_d`) |
| `proc_seen_B`, `proc_hidden_B`, `proc_gain_B` | `p2_base_r1_proceeds`, `p2_base_hidden_proceeds`, `p2_access_proceeds_gain` |
| `surp_seen_B`, `surp_hidden_B`, `surp_gain_B` | `p2_base_r1_surplus`, `p2_base_hidden_surplus`, `p2_access_surplus_gain` |
| `reserve_strict_B`, `reserve_excl_B` | `rsv_deter`, `rsv_points_excl` |
| `res_a_hi` | `res_a_up` |
| `access_scale_B` | `p2_access_break_even` |

New keys in round 2: `margin_kstrong_B`, `rJ`, `rS_B`, `res_rR`, `res_rcap`, `res_lambda_rR`, `res_entry_rR`,
`res_entry_cap`, `sig_comp_aT`, `sig_comp_d`, `p4_comp_b_no_y_r1_entry`, `ba_r1_B`, `ba_share_r1_B`.

### Statement and numbering changes

- Proposition numbers follow `memos/W1_keys.md` (Round 3): Propositions 1–4 in the main text, Corollary 3 on
  the research branch (M16, A9), Proposition A.1 for the region (A5), A.2 for the research region (A5), A.3 for
  the control (M14), A.4–A.7 for robustness (M17, A10), A.8–A.10 for sale terms (M18, A12), A.11–A.14 for the
  empirical results (M19). M15 stays Proposition 3 and M16 stays Proposition 4.
- `u` reads "the informed presence mass relative to the liquidity mass in one direction" (M7); `1+u` is the
  largest likelihood ratio of an order. The seller share is `ω` (M17, A2, A10, A12), with the spread response
  "weakly has the sign of `1−2ω`; strictly when `E[(R−ℓ)_+]` changes strictly".
- The fixed-information control "does not rise" (M3, M14, M19); frozen full orders keep entry flat up to `r_C`,
  then give `ρ`.
- The signal frame uses the pair at `B` with accuracies from `sig_comp_aT` and `sig_comp_d` (the earlier pair
  of the draft does not appear).
- Full orders are unique for `r > r_S` (M19, A8); the spread entry component is zero above `r_C` (M19).
- The research branch runs on `[r_R, r̄_R)` with endpoints from `res_rR` and `res_rcap`; entry rises from
  `res_entry_rR` to `res_entry_cap`; at the three intermediate strengths the equilibrium count is exactly two;
  research at the cap is unique at `r_1` and `r_2` (M16, A9).
- Proposition 1 (M6) states the two signs with their exact scope; Proposition 2 (M12) states (H1)–(H3) with
  `κ` and uniqueness under all four tie-rule pairs; the payment row of M17 no longer claims a reversal under
  the bargaining rule, whose trading equilibrium the manuscript leaves open.
- Backup A11 states Remark 3 on continuous order sizes; it is the only frame that names Laplace noise. The
  partial-sale growth claim of the draft does not appear, because the manuscript does not state it.
- No frame uses the first person or a status label.

### Figures

- M11 includes `figures/beliefs_talk.pdf`, M15 includes `figures/coexistence_talk.pdf`, and M16 includes
  `figures/research_talk.pdf`, each at `width=\linewidth` with a height cap and `keepaspectratio`. The round-1
  `\FigBox` placeholders and the macro itself are gone. M16 carries the three intermediate rates in its opening
  line instead of a separate table, so the figure keeps legible size; backup A9 keeps the same rates.

### Claims refuted or corrected against round 1

- The round-1 text called `u` "the odds that an order in a direction is informed". That reading is false and
  no frame uses it.
- The round-1 backup A12 used the seller share `η`, which the manuscript reserves for the liquidity law.
- The round-1 backup A11 claimed a partial sale that grows with strength under continuous sizes. The final
  manuscript states no such result, so the claim is out.
