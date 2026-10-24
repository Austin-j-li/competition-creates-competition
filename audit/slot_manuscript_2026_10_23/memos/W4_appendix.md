# W4: Appendix A.2 to A.9 of the order-slot manuscript

Workstream W4, 23 October 2026. Files in `overleaf/competition_slot/appendix/`:

| File | Label | Pages in `build/main.pdf` |
|---|---|---|
| `A2_beliefs_trading.tex` | `app:beliefs` | 51–55 |
| `A3_proposition2.tex` | `app:prop2` | 55–59 |
| `A4_coexistence.tex` | `app:coexistence` | 59–71 |
| `A5_research.tex` | `app:research` | 71–79 |
| `A6_robustness.tex` | `app:robustness` | 79–88 |
| `A7_welfare.tex` | `app:welfare` | 88–93 |
| `A8_empirical.tex` | `app:empirical` (new) | 93–97 |
| `A9_parameters.tex` | `app:parameters` (renamed from `A8_parameters.tex`) | 97–101 |

Appendix A runs from page 48 to page 101 (54 pages; A.1 by W1 is pages 48–51). The whole build has 101 pages.

`main.tex`: W1 had already replaced the appendix `\input` lines by `\slotappendix{A8_empirical}` and
`\slotappendix{A9_parameters}` before this workstream reached that step, so this workstream made no edit to
`main.tex`. It renamed the stub `A8_parameters.tex` to `A9_parameters.tex` and created `A8_empirical.tex`.

Build: `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` exits 0. Every reference
resolves, and no registry key is unknown. The appendix files have no overfull box. Overfull boxes remain in W1's
section files: `sections/06_robustness.tex` lines 76–106 (Table `tab:classes`, 130 pt) and line 169 (19 pt), and
`sections/04_equilibrium_results.tex` line 137 (4 pt). One
transient break came from W1's `sections/01_introduction.tex` (a literal `\n` at line 76); W1 fixed it.

## 1. What each file proves

Every proof (24 in all) opens with `\begin{proof}[Proof of Proposition~\ref{...}]` under the main-text label of
LABELS §3 (Lemma, Corollary or Remark where the statement is one), states the tuple, checks (E1)–(E6) of Definition 1 against it, and proves uniqueness from bounds
on every candidate. The conventions paragraph at the start of A.2 fixes "profile", "candidate", "deviation" and
"verification" once for A.2–A.9.

- **A.2** Lemma `lem:beliefs` (a)–(d) and the bound at a pooled price; Corollary `cor:exclusion`; Lemma `lem:prices`
  (a)–(e); a paragraph on constructed tuples (the price algebra with no equilibrium premise); Lemma `lem:trading`
  (a)–(d). Status: analytical.
- **A.3** Proposition `prop:ccc` (Steps 0–6, tuples E_0, E_1, E_2), the use of each hypothesis, the 47/10 example,
  the open set; Proposition `prop:region` (a)–(c). Analytical; decimals computer-assisted.
- **A.4** Lemma A.1 (the path, Sturm certificates), Lemma A.2 (threshold order), Lemmas A.3–A.5 (high class, low
  class, product), Proposition `prop:coexistence` (Steps 1–8), Proposition `prop:priors` (three steps, four cases),
  the CM endpoint, the tie-rule table. Computer-assisted (two Sturm counts).
- **A.5** Lemmas A.6–A.10 (joint deviation, bounds, positive research, the complete set at intermediate strengths,
  strong incumbents); Propositions `prop:research`, `prop:researchbranch`, `prop:researchregion`; the branch at B;
  Remark `rem:researchties`; access with research. Analytical with computer-assisted values.
- **A.6** Proposition `prop:control` and the slot control; `prop:atomless` for any cost law with the stated supports
  (atomlessness only for the ramp); `prop:classes` (construction from v_*); the economies of Table `tab:classes`;
  `prop:manyclasses`; the four-class certificate; the three-class collision; `prop:signals` with the one-pair
  formulas, S(B), the pair (0.94, 0.505) at B, the impossibility of d ≥ a_T at B, and the mixed equilibria at B with
  the accuracies of S(B).
- **A.7** `prop:access` (both tuples, coupling, the welfare identity), transfer and break-even scale, access outside
  the recruitment region; `prop:payment` (Nash bargaining continuation, weight ω); `prop:reserves`, the reserve
  kernel, the benchmark nodes, deterrence and why it needs p > r_0, boundary reserves.
- **A.8** Full two-sided trade on (r_S, h) with the exact r_S; `prop:spread`, `prop:informedshare`, `prop:winner`,
  `prop:announcement`; the two clusters under C1 and the third tuple under CM.
- **A.9** Declarations at B (Table `tab:a9-declarations`), the vector S(B), and Table `tab:margins` (one table,
  three floats joined by `\ContinuedFloat` because the preamble has no `longtable`), with a source code for the
  script of every margin and the open parameter sets.

## 2. Checks applied

Every check memo in `memos/` was read and applied. Round-2 package updates that followed a check were also read.

| Check | Applied corrections (where) |
|---|---|
| XP1 | Zero-order mass at F_0 is (1−λ)η(x)+λ1{x=0} (A.3 Step 1). Lemma `lem:trading` premises (E1), (E4), e ∈ [ρ,1], Δ_T ≥ 0 (A.2). Product lemma: direct price algebra before sufficiency; separate necessity and sufficiency (A.2 "Constructed tuples", A.4 Lemma A.5, every verification in A.3–A.8). Tie table row (r_N, r_S] split into (r_N, r_J), r_J, (r_J, r_S] (A.4). CM entry interval at r_C (A.4 Step 7, A.8). Domains of r_π and r_C(π) (A.4). CM endpoint at π_max with its tuple values (A.4). Derived margins with exact forms (A.4, `tab:margins`). Certificates cite the exact rational endpoints of `scripts/XP1/xp1_registry_recompute.csv`; decimal prior endpoints printed with ≈ where W1 does. |
| XP2 | Seller weight written ω, not η (A.7, matching W1). Payment rule: "weakly, strictly when E[(R−ℓ)_+] changes strictly" (A.7). Compressed step for the bands with 21/20 < p ≤ r_0 written out (A.7). Endpoint reserves: zero-cost preparation now follows from Definition 1, so no tie-rule caveat is needed (A.7). The constructive sequence with raw `e-7` displays is not printed. |
| XP3 | Weak-incumbent research statement uses B_r(1/2) < c_H, with the counterexample in words (A.5). Uniqueness above r_U^R: under CM the tuple is not unique at r_C, entry fills [ρ, 0.522757] (A.5 proof of `rem:researchties`). "Corresponds to", not "equals", for the cap and posterior margins (A.5). Exact endpoints from `scripts/XP3/exact_enclosures.json` and P3's round-2 `P3_enclosures.json` (A.5). Strict entry growth alone holds on a wider set (A.5). |
| XP4 | Fixed-information control stated as the step at r_C with both crossing probabilities (A.6). Cost-law result for any component laws on the supports; atomlessness only for the ramp; Δ_0 > 0 not needed (A.6). The pair (0.95, 0.505) is not used; the pair (0.94, 0.505) with its no-signal control shows complementarity at B (A.6, keys from P4 round 2). The separate order problems are stated (A.6). The no-signal control at B needs IM and has no I0 equilibrium (A.6). |
| XP5 | Exact r_S with the counterexample at 2.1241481 (A.8). Entry component zero above r_C; two separate monotonicity statements (A.8). Count range needs ϑ' ≤ 1 − 2k/(ρΔ_T(r)) (0.76 at r_1, 0.829586 at r_2) and the band incentive margin (A.8). Spread as conditional execution prices, no quote stage (A.8). Zero mean of announcements uses both reports; preparation-only sample positive (A.8). Two-cluster statement under C1; the CM third tuple at 1.60 (A.8). Open set with β < 1/3 strict and the vanishing margin at r_S (A.9). |
| XLA | Not applicable to the manuscript appendix (it concerns the Laplace audit for the comparison note). |

No check memo was missing at the end of this workstream: XP1, XP2, XP3, XP4 and XP5 all exist. P1, P3, P4 and P5
round-2 updates were read; P2 had no round 2 at the time of writing.

## 3. Findings for W1 and the coordinator

1. **Meaning of u.** XP1 and P1 round 2: u = λ/b is the informed presence mass relative to the liquidity mass in
   one direction; under full orders the odds that a purchase is informed are πu. Section 2.3 says that u "compares
   the probability of an informed order in a given direction with the probability of a liquidity order in that
   direction". That phrase reads as πλ/b under full orders. A wording change in Section 2.3 is advised.
2. **Zero-cost preparation.** Definition 1 now fixes zero-cost preparation after every price. The appendix relies
   on this for the entry floor. If a later edit applies the challenger's tie rule at zero gross profit instead,
   Proposition `prop:ccc`(iii) under CM needs g_H(F_2) > 0 (true in the benchmark).
3. **Table numbers.** Appendix tables use the global table counter (Tables 7–11), while equations, propositions and
   lemmas carry the prefix A. A `\renewcommand{\thetable}{A.\arabic{table}}` in `main.tex` would align them; this
   workstream does not edit the preamble.
4. **Main-text duplicates.** A.3 refers to W1's `tab:region` and `tab:outcomes` instead of repeating them; the
   two extra prior windows (κ > 3/25, κ > 1/10) are stated in the text of A.3.

## 4. Numbers printed without a registry key

All calibrated values use `\reg{}`. The proofs print these exact constants that follow by one line of arithmetic
from keyed primitives, or that define an example; the number check can confirm them against the named scripts:

- algebra in the slot band: 200(1+u) > 141(2+u), 5804(1+u) < 4245(2+u), 3/25, 22/25, 1/10, Δ_T(r_0) = 1/60,
  Δ_T(r_1) = 2/3, Δ_T(r_2) = 169/180, 9M + 3/8, 5/8, 1/2 and 3/4 as comparison values;
- the path: the polynomial coefficients of Q_J and of the degree-10 polynomial, 12r² − 3r/2 + 3, the interval
  [r_0, 7/4], 241 strengths in the diagnostic;
- the mixed signal equilibria at B: 13/16, 7/16, 311/1920, 2/5, 119/96, 137/192, 47/106, 15/19, 19/795, 1/15, 4/3,
  21/50, 5/8 − 23b/40, 13/32 − 63b/160;
- the three-class collision primitives: R ~ U[0, 8], p = 1, ρ = 1/4, c_H = 10, k = 1/8, priors (1/4, 1/2, 1/4),
  t_0 = 7/8, 49/16, 65/16, 95/16, and the perturbation 1/1000;
- reserves: 17/20 and the polynomial identities (p − 1)(5p + 1)/4, (p − 1)²/2;
- the empirical section: the example share 0.9, u' = 8/5 and v ≤ 200/259; digit counts (50, 60, 90, 110, 120).

Requested keys, if the coordinator wants every one keyed: the collision primitives (`p2_input_many_*`), the share
0.9 (`theta09`), 7/4 (`res_bound_r_hi`), 200/259 (`v_band_max`).

## 5. Open items (stated once, in the section where they matter)

- The equilibrium set with research on (r_N, r_U^R) (A.5 text of W1; proofs cover the six strengths and the branch).
- Selection between no trade and purchases-only on (r_F, r_N) (A.8).
- The full trading and preparation game under the bargaining rule (A.7).
- A selection at every reserve and the seller's optimal reserve (A.7).
- Full posterior recovery with more than two classes under mixed profiles (A.6 collision is a knife-edge example).
- Remark `rem:sizes` has no appendix proof, as LABELS §3 states.

## 6. Claims refuted or corrected

No new refutation. This workstream carries into the manuscript the refutations of the checks: the entry component
does not rise above r_C (XP5); the rounded interval (2.124148, 10) is not the uniqueness set (XP5); the pair
(0.95, 0.505) does not show complementary information (XP4); uniqueness above r_U^R fails at r_C under CM (XP3); the
summary row on (r_N, r_S] was wrong (XP1); the CM endpoint at π_max was missing (XP1).

## 7. Registry keys used

436 distinct keys, all present in `registry/registry.csv` after `scripts/_coordinator/make_numbers.py` (last run:
5,216 keys, no conflicts). A.2 prints no number. By file:
- `A3_proposition2.tex` (49): `nec_cH`, `nec_r2`, `nec_margin_kweak`, `nec_margin_prior_r1`, `nec_margin_recruit_B`, `nec_margin_kstrong_B`, `nec_margin_return_B`, `nec_margin_weakcost`, `B_r0_half`, `nec_entry_r0`, `entry_r1_B`, `str_r155`, `Delta_r155_frac`, `prim_pi`, `m_half_B`, `M_half_B`, `price_r1_m1_B`, `price_r1_0_B`, `price_r1_p1_B`, `price_r2_m1_B`, `price_r2_0_B`, `price_r2_p1_B`, `price_r0`, `b_plus_lambda_B`, `prim_h`, `prim_ell`, `prim_p`, `prim_rho`, `prim_cH`, `prim_k`, `prim_r0`, `prim_r1`, `prim_r2`, `tau_r0_frac`, `tau_r1_frac`, `tau_r2_frac`, `margin_weakcost_B`, `margin_kweak_B`, `u_lo_frac`, `u_hi_frac`, `u_kstrong_frac`, `margin_u_kstrong_B`, `prior_kappa_lo_B`, `prior_kappa_hi_B`, `prior_lo_B`, `prior_hi_B`, `prior_ii_hi`, `p2_prior_trade_lo`, `p2_prior_trade_hi`
- `A4_coexistence.tex` (37): `tau_r0_frac`, `tau_r2_frac`, `J_r0`, `rhoJ_r2`, `QJ_r0`, `rhoJ_r1`, `margin_tau_rN_half_B`, `rA`, `rF_B`, `rN`, `rJ`, `rS_B`, `rC_B`, `margin_rhoJ_2_B_frac`, `entry_mb_r140_B`, `str_r140`, `entry_mb_r145_B`, `str_r145`, `str_r155`, `str_r160`, `str_r165`, `entry_th_r155_B`, `entry_th_r160_B`, `entry_th_r165_B`, `entry_r0`, `entry_rA_B`, `entry_r1_B`, `entry_r2`, `margin_tauA_3q_B`, `piA_lo_B`, `piA_hi`, `pimax`, `rstar`, `M_pimax_B`, `mu0_pimax_B`, `margin_cmend_B`, `entry_cmend_B`
- `A5_research.tex` (61): `res_a`, `res_cap`, `res_Delta_r0`, `margin_res_weak_B`, `margin_res_half_B`, `str_r155`, `str_r160`, `str_r165`, `res_ULgap_r155`, `res_ULgap_r160`, `res_ULgap_r165`, `res_lamgap_r155`, `res_lamgap_r160`, `res_lamgap_r165`, `res_capgap_r155`, `res_capgap_r160`, `res_capgap_r165`, `margin_res_tau_r1_B`, `margin_res_tau_r2_B`, `res_rUR`, `margin_res_bound_r1_B`, `margin_res_bound_r2_B`, `res_entry_r1`, `res_entry_r2`, `res_rR`, `res_rcap`, `res_bound_dDelta`, `res_bound_tau74`, `res_bound_Delta74`, `res_bound_taup`, `res_dphi_lead`, `res_phip_lb`, `res_amono`, `res_rN`, `margin_res_rN_B`, `res_lambda_rR`, `res_entry_rR`, `res_entry_cap`, `res_lamE_r175`, `beta_B`, `res_region_aU3_6`, `res_region_a36_6`, `res_a_up`, `res_region_alo_0`, `res_cap_lo`, `res_cap_hi`, `margin_res_caplo_B`, `margin_res_caphi_B`, `margin_res_alo_B`, `margin_res_aup_B`, `res_beta_lo`, `res_beta_hi`, `res_amono_third`, `res_th_entry_r155`, `res_th_entry_r160`, `res_th_entry_r165`, `res_th_estar_r155`, `res_th_estar_r160`, `res_th_estar_r165`, `res_dR_r1`, `res_dW_r1`
- `A6_robustness.tex` (102): `p4_frozen_entry_below_ceiling`, `p4_frozen_entry_above_ceiling`, `rC_B`, `p4_control_crossing_r0_r1`, `p4_control_crossing_r1_r2`, `p4_hidden_r0_entry`, `atom_L`, `atom_eps`, `margin_p4_atomless_floor_B`, `margin_p4_atomless_weak_B`, `margin_p4_atomless_strong_B`, `p4_atomless_r1_entry`, `p4_atomless_r1_own`, `margin_p4_atomless_return_B`, `margin_p4_atomless_top_lower_r2_B`, `margin_p4_atomless_top_upper_r2_B`, `p4_atomless_r2_entry`, `p4_atomless_r2_own`, `p4_atomless_max_width_floor_r2`, `atom_eps_small`, `margin_p4_atomless_small_width_return`, `margin_p2_ex_d_strong_top_B`, `p2_input_ex_a_pi`, `p2_fixed_prior_three_tenths_r1_entry`, `p2_fixed_prior_three_tenths_r1_cost_sign_plus`, `p2_input_ex_b_pi`, `p2_fixed_prior_seven_tenths_r0_entry`, `p2_fixed_prior_seven_tenths_r0_cost_sign_plus`, `p2_fixed_prior_seven_tenths_r1_entry`, `p2_groups_gamma`, `p2_groups_trade`, `p2_groups_weak_range`, `p2_groups_weak_cost`, `p2_groups_profit_gap`, `p2_groups_top`, `p2_many_weight`, `p2_many_q1_mu0`, `p2_many_q1_mu1`, `p2_many_q1_mu2`, `p2_many_q2_mu0`, `p2_many_q2_mu1`, `p2_many_q2_mu2`, `p2_many_q2_price`, `p2_many_q0_price`, `p2_many_choice0`, `p2_many_choice1`, `p2_many_choice2`, `sig_aT`, `sig_d`, `margin_p4_signal_s_private`, `margin_p4_signal_s_joint`, `margin_p4_signal_s_weak`, `margin_p4_signal_s_strong`, `margin_p4_signal_s_other_pair`, `p4_s_signal_r0_entry`, `p4_s_signal_r1_entry`, `p4_s_signal_r0_own`, `p4_s_signal_r1_own`, `margin_p4_s_no_y_top_r0`, `margin_p4_s_no_y_top_r1`, `margin_p4_s_no_y_weak`, `margin_p4_s_no_y_strong`, `p4_s_no_y_r0_entry`, `margin_p4_s_class_weak`, `margin_p4_s_class_strong`, `margin_p4_s_class_prior_r0`, `margin_p4_s_class_top_r1`, `p4_s_class_r0_entry`, `margin_p4_grid_72_75_weak`, `p4_b_signal_z_min`, `margin_p4_b_d_ge_a_impossible`, `sig_comp_aT`, `sig_comp_d`, `margin_p4_signal_comp_b_private`, `margin_p4_signal_comp_b_joint`, `margin_p4_signal_comp_b_weak`, `margin_p4_signal_comp_b_strong`, `margin_p4_signal_comp_b_other_pair`, `p4_comp_b_r0_entry`, `p4_comp_b_r1_entry`, `margin_p4_comp_b_no_y_top_r1`, `margin_p4_comp_b_no_y_weak`, `margin_p4_comp_b_no_y_strong`, `p4_comp_b_no_y_r1_entry`, `margin_p4_b_weak_all_yplus`, `margin_p4_b_weak_no_yminus`, `margin_p4_b_weak_zero_return`, `margin_p4_b_weak_full_loss`, `margin_p4_b_weak_rate_room`, `p4_b_signal_r0_entry`, `p4_b_signal_r0_own`, `margin_p4_b_strong_no_yminus`, `margin_p4_b_strong_prior_yplus`, `margin_p4_b_strong_buy`, `margin_p4_b_strong_threshold_floor_return`, `margin_p4_b_strong_rate_room`, `margin_p4_b_strong_sale_public_gap`, `margin_p4_b_strong_zero_yplus`, `p4_b_signal_r1_entry`, `p4_b_signal_r1_own`, `p4_b_no_y_r1_zero_gross`, `p4_b_no_y_r1_full_gross`
- `A7_welfare.tex` (56): `p2_base_r1_proceeds`, `p2_base_hidden_proceeds`, `p2_access_proceeds_gain`, `p2_base_r1_surplus`, `p2_base_hidden_surplus`, `p2_access_surplus_gain`, `p2_access_gross_transfer`, `p2_access_break_even`, `access_out_cH`, `p2_outside_seen_cost_sign_minus`, `p2_outside_seen_cost_sign_zero`, `p2_outside_proceeds_gain`, `p2_outside_surplus_gain`, `pay_gap_coef`, `rsv_points_excl`, `p2_reserve_points_exclude_r0_global`, `p2_reserve_points_exclude_r0_prior_cost_margin`, `p2_reserve_points_exclude_r0_cost_sign_plus`, `p2_reserve_points_exclude_r1_global`, `p2_reserve_points_exclude_r1_prior_cost_margin`, `p2_reserve_points_exclude_r1_cost_sign_plus`, `p2_reserve_points_exclude_r0_entry`, `prim_p`, `margin_p2_reserve_points_exclude_gain0_B`, `margin_p2_reserve_points_exclude_gain1_B`, `rsv_bands_excl`, `p2_reserve_bands_exclude_r0_global`, `p2_reserve_bands_exclude_r0_prior_cost_margin`, `p2_reserve_bands_exclude_r0_cost_sign_plus`, `p2_reserve_bands_exclude_r1_global`, `p2_reserve_bands_exclude_r1_prior_cost_margin`, `p2_reserve_bands_exclude_r1_cost_sign_plus`, `margin_p2_reserve_bands_exclude_gain0_B`, `margin_p2_reserve_bands_exclude_gain1_B`, `rsv_deter`, `p2_reserve_points_deter_r0_global`, `p2_reserve_points_deter_r0_prior_cost_margin`, `p2_reserve_points_deter_r0_cost_sign_plus`, `p2_reserve_points_deter_r1_global`, `p2_reserve_points_deter_r1_prior_cost_margin`, `p2_reserve_points_deter_r1_cost_sign_plus`, `p2_reserve_points_deter_r0_entry`, `p2_reserve_points_deter_r1_entry`, `margin_p2_reserve_points_rev0_B`, `margin_p2_reserve_points_rev1_B`, `p2_reserve_ph`, `p2_reserve_weak_top`, `margin_p2_deter_lower_B`, `margin_p2_deter_upper_B`, `margin_p2_ph_weak_B`, `margin_p2_reserve_uniform_weak_B`, `margin_p2_reserve_uniform_strong_B`, `margin_p2_reserve_admissible_top_B`, `margin_p2_ph_trade_B`, `p2_endpoint_r1_entry`, `p2_endpoint_r1_proceeds`
- `A8_empirical.tex` (36): `margin_obs_post_over_58_B`, `delta_rS_B`, `margin_obs_rS_rC_B`, `rS_B`, `rS_counter_r_B`, `rS_counter_margin_B`, `rS_cert_hi_B`, `entry_jump_B`, `ba_class_r1_B`, `ba_entry_r1_B`, `ba_r1_B`, `ba_rC_left_B`, `ba_rC_right_B`, `theta_max_full_eq_r1_B`, `theta_max_full_eq_r2_B`, `theta09_beta_B`, `theta09_lowsale_r1_B`, `vol_full_B`, `u_lo_frac`, `u_hi_frac`, `margin_obs_band_incentive_B`, `alt_theta_B`, `alt_ba_r1_B`, `theta_min_counts_B`, `pbar_r1_B`, `p_neutral_r1_B`, `evprep_mean_r1_B`, `evprep_mean_r2_B`, `imb_buy_B`, `str_r160`, `U_gap_r160_B`, `mix_sigma_r160_B`, `mix_e1_r160_B`, `mix_mean_order_r160_B`, `mix_lowsale_r160_B`, `mix_entry_r160_B`
- `A9_parameters.tex` (209): `prim_h`, `prim_ell`, `prim_p`, `prim_rho`, `prim_cH`, `prim_k`, `prim_pi`, `prim_r0`, `prim_r1`, `prim_r2`, `u_B`, `beta_B`, `lambda_B`, `b_B`, `b0_B`, `m_half_B`, `M_half_B`, `res_a`, `res_cap`, `atom_L`, `atom_eps`, `atom_eps_small`, `sig_comp_aT`, `sig_comp_d`, `access_out_cH`, `rsv_points_excl`, `rsv_bands_excl`, `rsv_deter`, `sig_rho`, `sig_cH`, `sig_k`, `sig_r0`, `sig_r1`, `sig_aT`, `sig_d`, `margin_weakcost_B`, `margin_recruit_B`, `margin_recruit_post_B`, `margin_kweak_B`, `margin_kstrong_B`, `margin_return_B`, `margin_return_post_B`, `margin_implied_prior_r1`, `margin_kstrong2_B`, `margin_implied_prior_r2`, `u_lo_frac`, `margin_u_lo_B`, `u_hi_frac`, `margin_u_hi_B`, `margin_lambda_lo_B`, `margin_lambda_hi_B`, `margin_prior_lo_B`, `margin_prior_hi_B`, `margin_beta_B`, `margin_p4_ownership_rise_B`, `margin_p2_bplus_B`, `margin_Delta_pos_B_frac`, `margin_gHgL_B_frac`, `margin_tau_r0_half`, `margin_J_r0_B_frac`, `margin_rhoJ_r1_B_frac`, `margin_rhoJ_r2_B`, `margin_rhoJ_2_B_frac`, `margin_tau_r2_3q_B_frac`, `margin_tau_rN_half_B`, `QJ_r0`, `u_kstrong_frac`, `margin_u_kstrong_B`, `gap_rA_r0_B`, `gap_rF_rA_B`, `gap_rN_rF_B`, `gap_rJ_rN_B`, `gap_rS_rJ_B`, `gap_r1_rS_B`, `gap_rC_r1_B`, `gap_r2_rC_B`, `margin_piA_lo_B`, `margin_piA_hi`, `margin_tauA_3q_B`, `margin_pimax_tauA_B`, `margin_cmend_B`, `margin_res_half_B`, `margin_res_weak_B`, `str_r165`, `margin_res_nosale_B`, `str_r155`, `res_phi_r155`, `margin_res_aup_B`, `margin_res_lamcap_B`, `margin_res_alo_B`, `margin_res_amono_B`, `margin_res_caplo_B`, `margin_res_tau_r1_B`, `margin_res_caphi_B`, `margin_res_tau_r2_B`, `margin_res_bound_r1_B`, `margin_res_bound_r2_B`, `margin_res_rR_B`, `margin_res_rcap_B`, `margin_res_rN_B`, `margin_p4_weak_top_B`, `margin_p4_atomless_floor_B`, `margin_p4_atomless_weak_B`, `margin_p4_atomless_strong_B`, `margin_p4_atomless_floor_r2_B`, `margin_p4_atomless_return_B`, `margin_p4_atomless_small_width_return`, `p2_groups_trade`, `p2_groups_weak_range`, `p2_groups_weak_cost`, `p2_groups_profit_gap`, `p2_groups_top`, `margin_p2_many_beta_B`, `margin_p2_many_w_lower_B`, `margin_p2_many_w_upper_B`, `p2_many_choice0`, `p2_many_choice1`, `p2_many_choice2`, `margin_p4_signal_s_private`, `margin_p4_signal_comp_b_private`, `margin_p4_signal_s_joint`, `margin_p4_signal_comp_b_joint`, `margin_p4_signal_s_weak`, `margin_p4_signal_comp_b_weak`, `margin_p4_signal_s_strong`, `margin_p4_signal_comp_b_strong`, `margin_p4_signal_s_other_pair`, `margin_p4_signal_comp_b_other_pair`, `margin_p4_comp_b_no_y_top_r1`, `margin_p4_b_d_ge_a_impossible`, `p2_reserve_points_exclude_r0_global`, `p2_reserve_points_exclude_r0_prior_cost_margin`, `p2_reserve_points_exclude_r0_cost_sign_plus`, `p2_reserve_points_exclude_r1_global`, `p2_reserve_points_exclude_r1_prior_cost_margin`, `p2_reserve_points_exclude_r1_cost_sign_plus`, `p2_reserve_bands_exclude_r0_global`, `p2_reserve_bands_exclude_r0_prior_cost_margin`, `p2_reserve_bands_exclude_r0_cost_sign_plus`, `p2_reserve_bands_exclude_r1_global`, `p2_reserve_bands_exclude_r1_prior_cost_margin`, `p2_reserve_bands_exclude_r1_cost_sign_plus`, `p2_reserve_points_deter_r0_global`, `p2_reserve_points_deter_r0_prior_cost_margin`, `p2_reserve_points_deter_r0_cost_sign_plus`, `p2_reserve_points_deter_r1_global`, `p2_reserve_points_deter_r1_prior_cost_margin`, `p2_reserve_points_deter_r1_cost_sign_plus`, `margin_p2_deter_lower_B`, `margin_p2_deter_upper_B`, `margin_p2_ph_weak_B`, `margin_obs_rS_rC_B`, `margin_obs_rS_h_B`, `margin_obs_post_over_58_B`, `margin_obs_band_incentive_B`, `margin_obs_rF_B`, `margin_obs_rN_B`, `margin_obs_buy_r155_B`, `margin_obs_lowsell_r165_B`, `margin_obs_buy_recruit_r165_B`, `margin_p2_base_weak_cost_B`, `margin_p2_base_strong_top_B`, `margin_p2_base_weak_trade_B`, `margin_p2_base_high_floor_B`, `margin_p2_base_low_floor_B`, `margin_p2_base_collapse_B`, `margin_p2_base_ownership_B`, `margin_p2_moderate_weak_cost_B`, `margin_p2_moderate_strong_top_B`, `margin_p2_moderate_weak_trade_B`, `margin_p2_moderate_high_floor_B`, `margin_p2_moderate_low_floor_B`, `margin_p2_moderate_ownership_B`, `margin_p2_bands_weak_cost_B`, `margin_p2_bands_strong_top_B`, `margin_p2_bands_weak_trade_B`, `margin_p2_bands_high_floor_B`, `margin_p2_bands_low_floor_B`, `margin_p2_bands_collapse_B`, `margin_p2_bands_ownership_B`, `margin_p2_ex_a_weak_cost_B`, `margin_p2_ex_a_strong_top_B`, `margin_p2_ex_a_weak_trade_B`, `margin_p2_ex_a_high_floor_B`, `margin_p2_ex_a_low_floor_B`, `margin_p2_ex_a_collapse_B`, `margin_p2_ex_a_ownership_B`, `margin_p2_ex_b_weak_cost_B`, `margin_p2_ex_b_strong_top_B`, `margin_p2_ex_b_weak_trade_B`, `margin_p2_ex_b_high_floor_B`, `margin_p2_ex_b_low_floor_B`, `margin_p2_ex_b_collapse_B`, `margin_p2_ex_b_ownership_B`, `margin_p2_ex_c_weak_cost_B`, `margin_p2_ex_c_strong_top_B`, `margin_p2_ex_c_weak_trade_B`, `margin_p2_ex_c_high_floor_B`, `margin_p2_ex_c_low_floor_B`, `margin_p2_ex_c_collapse_B`, `margin_p2_ex_c_ownership_B`, `margin_p2_ex_d_weak_cost_B`, `margin_p2_ex_d_strong_top_B`, `margin_p2_ex_d_weak_trade_B`, `margin_p2_ex_d_high_floor_B`, `margin_p2_ex_d_low_floor_B`, `margin_p2_ex_d_collapse_B`, `margin_p2_ex_d_ownership_B`, `p4_atomless_max_width_floor_r2`
