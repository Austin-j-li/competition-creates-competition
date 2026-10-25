# S6. The example's numbers

Report of the production assistant to the coordinator. Nothing is committed. The generator is `audit/slot_manuscript_2026_10_23/scripts/TU/tu_numbers.py`, with its printed computations in `scripts/TU/run.log`. It writes `registry/TU.csv`; `make_numbers.py` merged that file into `registry/registry.csv` and `slot/manuscript/numbers.tex`.

## Result

- 100 new rows in `registry/TU.csv`: 68 for the keys of the statements and the delivery lens, and 32 for the `a236_*` keys that the appendix edit of A.2, A.3 and A.6 left pending (`S5_A236.md` assigns them to the production assistant).
- The merged table has 5321 keys (5221 before). `make_numbers.py`: 0 conflicts. The diff of `registry.csv` and `numbers.tex` adds 100 lines to each and removes none, so no existing row changed.
- `number_scan.py`: 21 files, 736 distinct keys used, 0 missing keys, 0 literal decimals outside `\reg`.
- Every `\reg` key in `statements/A.tex`, `B.tex`, `C.tex`, `D.tex`, in `statements/O*/*.tex` and in `wording_targets.md` exists in the table. The one placeholder left in `wording_targets.md` is the convention example `NEW:short_name` on line 14.
- Builds, all into the private folder `ccc-tu-scratch/s6_prod/build` (the brief's step 4 names `s6/build`; the working rules name the private folder, which is `s6_prod`): `A.tex`, `B.tex`, `C.tex`, `D.tex` exit 0 with 6, 8, 8 and 9 pages, no "??" in the text and no unknown-key warning. The full manuscript (`slot/manuscript/main.tex`, built into `ccc-tu-scratch/s6_prod/full`) exits 0 with 124 pages, no "??" and no unknown-key warning. No build product is in the repository.
- The independent recomputation by a second helper (PLAN S6, "Checking") is not part of this report.

## Method

Rational quantities are `fractions.Fraction`. Quantities with e or a square root are `mpmath.iv` intervals at 80 digits, and the program refuses a row whose six-decimal display differs between the two ends. Every root is bracketed by a decided sign change of an exact rational function and halved with exact signs to 10^-60; the note column of the row states the monotonicity that makes the root unique. The program prints each value beside the existing row it must reproduce and asserts nothing.

Agreements printed in `run.log`:

- The class-H and class-L entries reproduce `res_lambda_*`, `res_entry_*` and `res_own_*` at r = 1.55, 1.60, 1.65, r_R and the cap. `wtest_r1_B` equals `p2_access_proceeds_gain` and `res_dR_r1`. `cov_win_class_r1_B` plus `cov_win_recruit_r1_B` equals `cov_win_r1_B`. `res_rcap`, `res_rR` and `margin_res_half_B` match their rows.
- The exact values of `res_phi_r0_frac`, `res_J74_frac`, the three `res_I0CM_*` rows, the pooling rows, `res_rQ`, `res_lambda_floor_rQ`, and the smallest of the 24 piece bounds, 5993292043494701003/510152171246294601024 (at least 1/100), equal the values in the area notes. The closed form of `share_H_r1_B` agrees with e_H/(e_H + e_L/3) to 40 digits. The balance margins are the minima on a grid of 2401 strengths, attained at r_2.
- The two-interval path rows come from a direct computation of that path's spread (the spread is h − ell minus the profit gap), profit gap, threshold and J, not from the notes' intermediate numbers: J(3137/6498) = k exactly, and on [1, 2] J − k = −(D² − (1519/500)D + 9/50)/(9 − D).
- The 32 `a236_*` rows are recomputed from the definitions in the appendix text (the market quantities M, m, M^I, m^I, the five margins of the more accurate challenger signal, the class entries, the price gaps, the zero-profit rates, the cutoffs). Each equals the value listed in `S5_A236.md`. `a236_sig_alt_private` and `a236_sig_alt_weak` equal the existing rows `margin_p4_signal_s_private` and `margin_p4_signal_s_weak`; the other three margins depend on the slot (λ = 1/3, β = 3/10 here) and differ from the existing rows by design.

## New rows

| Key | Exact value | Display | Status word (internal) | Method |
|---|---|---|---|---|
| `cH_DA_floor_B` | 399/80 | 399/80 | analytical | exact rational |
| `cH_afford_ceiling_B` | 32/5 | 32/5 | analytical | exact rational |
| `margin_decisive_B_frac` | 81/80 | 81/80 | analytical | exact rational |
| `margin_unif_afford_B` | 2/5 | 2/5 | analytical | exact rational |
| `decisive_rmax_B` | 7.9686269665968858857524 | 7.968627 | computer-assisted | interval, closed form in e |
| `margin_decisive_rmax_B` | 2.0313730334031141142475 | 2.031373 | computer-assisted | interval, closed form in e |
| `margin_balance_B_frac` | 9667/8280 | 9667/8280 | analytical | exact rational |
| `margin_balance_B` | 9667/8280 | 1.167512 | analytical | exact rational |
| `margin_balance_sq_B_frac` | 937/5520 | 937/5520 | analytical | exact rational |
| `margin_balance_sq_B` | 937/5520 | 0.169746 | analytical | exact rational |
| `twonum_h` | 10 | 10 | input | declared input |
| `twonum_ell` | 1 | 1 | input | declared input |
| `twonum_p` | 1/2 | 1/2 | input | declared input |
| `twonum_cH` | 2 | 2 | input | declared input |
| `twonum_halfwidth` | 1/10 | 1/10 | input | declared input |
| `twonum_rlo` | 7 | 7 | input | declared input |
| `twonum_rhi` | 15/2 | 15/2 | input | declared input |
| `twonum_Jlo` | 2 | 2 | analytical | exact rational |
| `twonum_Jhi` | 13/10 | 13/10 | analytical | exact rational |
| `twopath_weight_lower` | 9/10 | 0.9 | input | declared input |
| `twopath_halfwidth` | 1/100 | 0.01 | input | declared input |
| `twopath_lower_start` | 3/5 | 0.6 | input | declared input |
| `twopath_lower_end` | 49/50 | 0.98 | input | declared input |
| `twopath_upper_start` | 157/100 | 1.57 | input | declared input |
| `twopath_upper_end` | 9/5 | 1.8 | input | declared input |
| `twopath_lo` | 3137/6498 | 0.482764 | analytical | exact rational |
| `twopath_hi` | 1.1501058601369759572073 | 1.150106 | computer-assisted | root by exact-sign bisection to 10^-60 |
| `share_H_r0` | 6/11 | 0.545455 | analytical | exact rational |
| `share_H_r1_B` | 0.8306909452303742144408 | 0.830691 | computer-assisted | interval, closed form in e |
| `share_H_r2_B` | 18/23 | 0.782609 | analytical | exact rational |
| `wtest_r1_B` | 0.2579478013681287647781 | 0.257948 | computer-assisted | interval, closed form in e |
| `cov_win_class_r1_B` | 0.0280101474095934331164 | 0.028010 | computer-assisted | interval, closed form in e |
| `cov_win_recruit_r1_B` | 0.2238531834333279308144 | 0.223853 | computer-assisted | interval, closed form in e |
| `wsecond_r1_B` | 0.6155292893150024396255 | 0.615529 | computer-assisted | interval, closed form in e |
| `margin_reserve_unif_B` | 1/4 | 1/4 | analytical | exact rational |
| `margin_winsep_r1_B` | 1/3 | 1/3 | analytical | exact rational |
| `margin_winsep_r2_B` | 5/18 | 5/18 | analytical | exact rational |
| `vol_band_max_frac` | 200/259 | 200/259 | analytical | exact rational |
| `margin_vol_band_B` | 0.0448489229250210762131 | 0.044849 | computer-assisted | interval, closed form in e |
| `res_phi_r0_frac` | -1369550353/60351152400 | -1369550353/60351152400 | analytical | exact rational |
| `res_phi_r0` | -1369550353/60351152400 | -0.022693 | analytical | exact rational |
| `res_J74_frac` | 171/3080 | 171/3080 | analytical | exact rational |
| `res_bound_strength` | 7/4 | 7/4 | input | declared input |
| `res_beta_upper` | 1/3 | 1/3 | input | declared input |
| `str_r200` | 2 | 2 | input | declared input |
| `res_phi_rcap` | 0.0174457484568150571463 | 0.017446 | computer-assisted | interval from a root bracket (monotone) |
| `res_eH_r155` | 0.5968430637880178617288 | 0.596843 | computer-assisted | interval, closed-form quadratic root |
| `res_eL_r155` | 0.4184171675414748767656 | 0.418417 | computer-assisted | interval, closed-form quadratic root |
| `res_eH_r160` | 0.6186043182800706572559 | 0.618604 | computer-assisted | interval, closed-form quadratic root |
| `res_eL_r160` | 0.4093264921381533582661 | 0.409326 | computer-assisted | interval, closed-form quadratic root |
| `res_eH_r165` | 0.6385194220634719831796 | 0.638519 | computer-assisted | interval, closed-form quadratic root |
| `res_eL_r165` | 0.4010070386716963511419 | 0.401007 | computer-assisted | interval, closed-form quadratic root |
| `res_eH_rR` | 0.5735413852478305449765 | 0.573541 | computer-assisted | interval from a root bracket (monotone) |
| `res_eL_rR` | 0.4281513488148359891541 | 0.428151 | computer-assisted | interval from a root bracket (monotone) |
| `res_eH_cap` | 0.6488026068215771207335 | 0.648803 | computer-assisted | interval, closed form in e |
| `res_eL_cap` | 0.3967112801352362226856 | 0.396711 | computer-assisted | interval, closed form in e |
| `res_I0CM_lambda_r200` | 1355413/6055413 | 0.223835 | analytical | exact rational |
| `res_I0CM_e1_r200` | 292690607/813155460 | 0.359944 | analytical | exact rational |
| `res_I0CM_entry_r200` | 40439906511409/140685489814428 | 0.287449 | analytical | exact rational |
| `res_floor_step` | 1/10 | 1/10 | input | declared input |
| `res_floor_dphi_lb` | 1/100 | 1/100 | analytical | exact rational |
| `margin_res_floor_slope_B` | 5993292043494701003/510152171246294601024 | 0.011748 | analytical | exact rational |
| `res_rQ` | 2.1669951582192858822824 | 2.166995 | computer-assisted | root by exact-sign bisection to 10^-60 |
| `res_lambda_floor_rQ` | 0.2342572560656338486369 | 0.234257 | computer-assisted | interval from a root bracket (monotone) |
| `res_tau_rQ` | 0.6708617128560904675394 | 0.670862 | computer-assisted | interval from a root bracket (monotone) |
| `r_pool_B` | 1.9117746293707232487883 | 1.911775 | computer-assisted | interval, closed form in e |
| `pool_mu_B` | 0.3679439526455767409814 | 0.367944 | computer-assisted | interval, closed form in e |
| `pool_price_B` | 0.4978853790195051334338 | 0.497885 | computer-assisted | interval, closed form in e |
| `a236_Delta_r1_frac` | 2/3 | 2/3 | analytical | exact rational |
| `a236_Delta_r2_frac` | 169/180 | 169/180 | analytical | exact rational |
| `a236_kappa_floor_frac` | 3/25 | 3/25 | analytical | exact rational |
| `a236_pool_cH` | 10 | 10 | input | declared input |
| `a236_pool_h` | 10 | 10 | input | declared input |
| `a236_pool_k` | 1/8 | 1/8 | input | declared input |
| `a236_pool_p` | 1 | 1 | input | declared input |
| `a236_pool_perturb` | 1/1000 | 0.001 | input | declared input |
| `a236_pool_pi1` | 1/4 | 1/4 | input | declared input |
| `a236_pool_pi2` | 1/2 | 1/2 | input | declared input |
| `a236_pool_pi3` | 1/4 | 1/4 | input | declared input |
| `a236_pool_r` | 8 | 8 | input | declared input |
| `a236_pool_rho` | 1/4 | 1/4 | input | declared input |
| `a236_sig_alt_private` | 21/400 | 0.052500 | analytical | exact rational |
| `a236_sig_alt_joint` | 1363/36800 | 0.037038 | analytical | exact rational |
| `a236_sig_alt_weak` | 2/1375 | 0.001455 | analytical | exact rational |
| `a236_sig_alt_strong` | 603/31625 | 0.019067 | analytical | exact rational |
| `a236_sig_alt_other` | 76753/18400 | 4.171359 | analytical | exact rational |
| `a236_sig_lambda` | 1/3 | 1/3 | input | declared input |
| `a236_sig_beta` | 3/10 | 3/10 | input | declared input |
| `a236_sig_M` | 8/11 | 8/11 | analytical | exact rational |
| `a236_sig_m` | 3/11 | 3/11 | analytical | exact rational |
| `a236_sig_eH` | 13/16 | 0.812500 | analytical | exact rational |
| `a236_sig_eL` | 7/16 | 0.437500 | analytical | exact rational |
| `a236_sig_DP0` | 311/1920 | 0.161979 | analytical | exact rational |
| `a236_sig_DP1` | 137/192 | 0.713542 | analytical | exact rational |
| `a236_sig_rate0` | 119/96 | 119/96 | analytical | exact rational |
| `a236_sig_rate1` | 4/3 | 4/3 | analytical | exact rational |
| `a236_sig_sale_mu` | 21/50 | 21/50 | analytical | exact rational |
| `a236_sig_public_cutoff` | 47/106 | 47/106 | analytical | exact rational |
| `a236_sig_sale_cutoff` | 15/19 | 15/19 | analytical | exact rational |
| `a236_sig_sale_floor` | 19/795 | 19/795 | analytical | exact rational |

Long decimal values are cut here; `registry/TU.csv` has 30 decimals and the outward enclosure in the note column. The notes give the definition, the monotonicity or the bracket, and no tool, agent or model name.

Displays: fractions print as typed `a/b` where the text prints fractions (`cH_DA_floor_B`, `cH_afford_ceiling_B`, `margin_unif_afford_B`, `margin_decisive_B_frac`, `margin_balance_*_frac`, `twonum_*`, `res_phi_r0_frac`, `res_J74_frac`, `margin_winsep_*`, `margin_reserve_unif_B`, the `a236_*` spreads, priors, M, m, rates and cutoffs); the two-interval parameters print as decimals (0.9, 0.01, 0.6, 0.98, 1.57, 1.8); margins, entries, gaps and every irrational value print with six decimals. Each exact value is in the value column, so any display can change without recomputation.

## One name per quantity: alias replacements

Kept: `margin_unif_afford_B` (2/5), `cH_afford_ceiling_B` (32/5), `cH_DA_floor_B` (399/80), `share_H_r0`, `share_H_r1_B`, `share_H_r2_B`. Replaced by exact find-and-replace of the key name only:

| File | Old name | New name | Occurrences |
|---|---|---|---|
| `statements/A.tex` | `margin_afford_uniform_B_frac` | `margin_unif_afford_B` | 1 |
| `statements/A.tex` | `afford_cost_hi_frac` | `cH_afford_ceiling_B` | 1 |
| `statements/A.tex` | `decisive_cost_lo_frac` | `cH_DA_floor_B` | 1 |
| `statements/wording_targets.md` | `NEW:own_share_r0` | `share_H_r0` | 3 |
| `statements/wording_targets.md` | `NEW:own_share_r1_B` | `share_H_r1_B` | 3 |
| `statements/wording_targets.md` | `NEW:cH_DA_floor_B` | `cH_DA_floor_B` | 3 |
| `statements/wording_targets.md` | `NEW:cH_afford_ceiling_B` | `cH_afford_ceiling_B` | 2 |
| `statements/wording_targets.md` | `NEW:res_rQ` | `res_rQ` | 2 |

The three occurrences of each `NEW:` name in `wording_targets.md` include the closing table "Quantities marked NEW", whose first column now holds the table names; the rest of its text is unchanged. The area notes (`A_notes.md`, `B_notes.md`, `O6_notes.md` and the referee files) still show the old names, because they describe the packages as delivered. `cH_unif_cap_B` and `r_decisive_B` (the delivery lens) are used by no statement and are not in the table.

## Existing keys reused (no duplicate)

`margin_res_half_B` (1.195833, the announcement margin), `rS_B` (2.124148), `margin_res_amono_B` and `res_amono` (the cheap-research margin), `margin_res_rN_B` (the cap-before-selling margin, in strength units), `res_rR`, `res_rcap`, `res_rC`, `res_rN`, `res_entry_cap`, `margin_res_bound_r1_B`, `entry_r0`, `entry_r2`. Class entry at r_0 and r_2 is rho in both classes (zero research; floor-entry research at the cap), so the rows `res_eH_*` and `res_eL_*` start at the intermediate strengths, r_R and the cap (the value at r_1 = 3).

## Rows beyond the statements' keys

Added from PLAN S6 and the delivery lens: `res_phi_r0` (decimal of the exact margin), `res_tau_rQ`, `margin_res_floor_slope_B` (the smallest piece bound), `margin_decisive_rmax_B` (h − `decisive_rmax_B`), the class-entry rows `res_eH_*` and `res_eL_*` at five strengths, `margin_balance_B`, `margin_balance_sq_B`, `vol_band_max_frac` and `margin_vol_band_B` (the proof of example (d)). No statement prints these.

## Language scan

The print-only scan ran on `registry/TU.csv`, `scripts/TU/tu_numbers.py` and this report. Hits and judgments:

- Status words (in the script and in the CSV's status column, the words "analytical" and "computer-assisted"): the registry's internal status column. They print nowhere in the paper, as the brief says.
- Process words in the CSV (file name, script and run hits): the registry's own `source_script` and `run_log` columns and their header, the same columns every existing row has.
- "Method words" (one per row with an interval): the word "enclosure" in the note column and the word "bisection" in some notes; both name the mathematics (an outward interval around the value, a halving of a sign-change bracket). The one key/file hit is the CSV header "key".
- The script's docstring and comments use "run" and "program" for the generator itself; the generator is a project file, not manuscript text.
- No hit in defensive, history, example naming, names, house, interval claim or placeholder for the CSV and the script.
- This report: the status words are the column values listed above; the history hits are the words "new name", "replaced" and "now" in the alias table (a record of find-and-replace); the process hits are file names, registry columns and the build record; the two "??" hits are the build check. The names category has no hit. The report is a project document, not manuscript text, and carries no tool, agent, model or account name.

## Points for the coordinator

1. Names of the rows: `margin_unif_afford_B` displays 2/5 as the brief fixes (the mathematics writer's note proposed 0.4).
2. The `a236_*` displays are my choices (see Displays); the value column is exact.
3. `wording_targets.md` line 14 and the heading "Quantities marked NEW" still describe the placeholder convention; their text is untouched.
