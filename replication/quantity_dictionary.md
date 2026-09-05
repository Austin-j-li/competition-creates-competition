# Quantity dictionary

Every `[[key]]` placeholder used by the manuscript and the online appendix, generated from `paper/quantity_manifest.csv` (declarations, selectors, display rules) and the resolved registry `numerics/quantity_registry.csv` (a copy is `replication/quantity_registry.csv`). Each key resolves from one validated output row selected by the full parameter declaration and, where the source carries it, the continuation identity; rows with an input value are declarations. Status uses the paper's vocabulary (analytical, computer-assisted, numerical diagnostic, open) plus `input` for declarations. Displays are formatted after validation: outward rounding for interval enclosures, conservative rounding for one-sided bounds, half-even rounding otherwise.

Registry decimal context: precision 60, rounding ROUND_HALF_EVEN (established locally by `numerics/registry.py`, independent of the ambient context). Keys: 128; open: 0.

Units: `probability` (a probability in [0,1]); `percentage` (a probability times 100, shown with a percent sign); `percentage_point` (a difference of two probabilities times 100); `payoff per share`, `surplus per share`, `payoff margin`, `payoff per marginal order` (model value units per target share); `order units` (investor order scale); `model units` (declared primitives); `standard deviations`; `version` (software metadata).

## Exercise C.0

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `base_h` | Declared $h$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 10` | `input` | 10 |
| `base_ell` | Declared $\ell$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1` | `input` | 1 |
| `base_p` | Declared $p$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.5` | `input` | 0.5 |
| `base_rho` | Declared $\rho$; retain its exact decimal input. | `probability` | `exact_input` | `input manifest` | `declared input 0.25` | `input` | 0.25 |
| `base_c_low` | Declared $c_L$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1` | `input` | 1 |
| `base_c_high` | Declared $c_H$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 6` | `input` | 6 |
| `base_b` | Declared $b$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 2` | `input` | 2 |
| `base_k` | Declared $k$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.02` | `input` | 0.02 |
| `base_r_weak` | Declared $r_0$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1.2` | `input` | 1.2 |
| `base_r_strong` | Declared $r_1$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 3` | `input` | 3 |
| `base_r_collapse` | Declared $r_2$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 3.6` | `input` | 3.6 |
| `moderate_h` | Declared $h$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 2` | `input` | 2 |
| `moderate_ell` | Declared $\ell$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1` | `input` | 1 |
| `moderate_p` | Declared $p$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.5` | `input` | 0.5 |
| `moderate_rho` | Declared $\rho$; retain its exact decimal input. | `probability` | `exact_input` | `input manifest` | `declared input 0.25` | `input` | 0.25 |
| `moderate_c_low` | Declared $c_L$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.3` | `input` | 0.3 |
| `moderate_c_high` | Declared $c_H$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.89` | `input` | 0.89 |
| `moderate_b` | Declared $b$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 2` | `input` | 2 |
| `moderate_k` | Declared $k$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.002` | `input` | 0.002 |
| `moderate_r_weak` | Declared $r_0$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1.05` | `input` | 1.05 |
| `moderate_r_strong` | Declared $r_1$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1.5` | `input` | 1.5 |
| `signal_h` | Declared $h$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 10` | `input` | 10 |
| `signal_ell` | Declared $\ell$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1` | `input` | 1 |
| `signal_p` | Declared $p$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.5` | `input` | 0.5 |
| `signal_rho` | Declared $\rho$; retain its exact decimal input. | `probability` | `exact_input` | `input manifest` | `declared input 0.85` | `input` | 0.85 |
| `signal_c_low` | Declared $c_L$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1` | `input` | 1 |
| `signal_c_high` | Declared $c_H$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 7.14` | `input` | 7.14 |
| `signal_b` | Declared $b$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 2` | `input` | 2 |
| `signal_k` | Declared $k$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 0.015` | `input` | 0.015 |
| `signal_r_weak` | Declared $r_0$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 1.1` | `input` | 1.1 |
| `signal_r_strong` | Declared $r_1$; retain its exact decimal input. | `model units` | `exact_input` | `input manifest` | `declared input 2.3` | `input` | 2.3 |
| `signal_trader_accuracy_value` | Declared $a$; retain its exact decimal input. | `probability` | `exact_input` | `input manifest` | `declared input 0.70` | `input` | 0.70 |
| `signal_buyer_accuracy_value` | Declared $d$; retain its exact decimal input. | `probability` | `exact_input` | `input manifest` | `declared input 0.75` | `input` | 0.75 |

## Exercise C.0/C.6

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `cost_halfwidth` | $\varepsilon_C$, the preparation-cost half-width. | `model units` | `exact_input` | `input manifest` | `declared input 0.1` | `input` | 0.1 |
| `value_band_halfwidth` | $\varepsilon_V$, the within-class value half-width. | `model units` | `exact_input` | `input manifest` | `declared input 0.05` | `input` | 0.05 |
| `value_reserve_high` | The class-economy reserve above the entire low-value band. | `model units` | `exact_input` | `input manifest` | `declared input 1.1` | `input` | 1.1 |
| `pool_reserve` | Declared reserve $p$ of the price-pool regression (fixed full orders; retain its exact decimal input). | `model units` | `exact_input` | `input manifest` | `declared input 7` | `input` | 7 |

## Exercise C.1

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `base_entry_weak` | $\mathsf E=(\bar e_H+\bar e_L)/2$ in the validated Laplace, atomic-cost feedback equilibrium. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=feedback; noise=Laplace; cost_law=atoms; r=r_weak` | `analytical` | 0.250000 |
| `base_entry_strong` | $\mathsf E=(\bar e_H+\bar e_L)/2$ in the validated Laplace, atomic-cost feedback equilibrium. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=feedback; noise=Laplace; cost_law=atoms; r=r_strong` | `analytical` | 0.522757 |
| `base_entry_collapse` | $\mathsf E=(\bar e_H+\bar e_L)/2$ in the validated Laplace, atomic-cost feedback equilibrium. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=feedback; noise=Laplace; cost_law=atoms; r=r_collapse` | `analytical` | 0.250000 |
| `base_frozen_entry_weak` | $\mathsf E$ with fixed full orders and optimal preparation at this strength; not an equilibrium assertion for the investor. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=frozen; noise=Laplace; cost_law=atoms; r=r_weak` | `numerical diagnostic` | 0.562178 |
| `base_hidden_entry_weak` | $\mathsf E$ in the reoptimized price-hidden economy. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=price_hidden; noise=Laplace; cost_law=atoms; r=r_weak` | `analytical` | 0.250000 |
| `base_ownership_weak` | $\mathsf O_H=\bar e_H/2$, unconditional probability of high-quality challenger ownership. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=feedback; noise=Laplace; cost_law=atoms; r=r_weak` | `analytical` | 0.125000 |
| `base_spread_weak` | $\Delta_T=t_H-t_L$ from independently checked auction expectations. | `payoff per share` | `decimal_6` | `tables/auction_primitives.csv` | `r=r_weak` | `analytical` | 0.016667 |
| `base_profit_prior_weak` | $B_r(1/2)=(g_H+g_L)/2$. | `payoff per share` | `decimal_6` | `tables/auction_primitives.csv` | `r=r_weak` | `analytical` | 4.804167 |
| `base_frozen_entry_strong` | $\mathsf E$ with fixed full orders and optimal preparation at this strength; not an equilibrium assertion for the investor. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=frozen; noise=Laplace; cost_law=atoms; r=r_strong` | `numerical diagnostic` | 0.522757 |
| `base_hidden_entry_strong` | $\mathsf E$ in the reoptimized price-hidden economy. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=price_hidden; noise=Laplace; cost_law=atoms; r=r_strong` | `analytical` | 0.250000 |
| `base_ownership_strong` | $\mathsf O_H=\bar e_H/2$, unconditional probability of high-quality challenger ownership. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=feedback; noise=Laplace; cost_law=atoms; r=r_strong` | `analytical` | 0.324192 |
| `base_spread_strong` | $\Delta_T=t_H-t_L$ from independently checked auction expectations. | `payoff per share` | `decimal_6` | `tables/auction_primitives.csv` | `r=r_strong` | `analytical` | 0.666667 |
| `base_profit_prior_strong` | $B_r(1/2)=(g_H+g_L)/2$. | `payoff per share` | `decimal_6` | `tables/auction_primitives.csv` | `r=r_strong` | `analytical` | 4.291667 |
| `base_revenue_feedback` | $\mathcal R_T$ in the strong feedback equilibrium. | `payoff per share` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=feedback; r=r_strong; noise=Laplace; cost_law=atoms` | `analytical` | 0.872392 |
| `base_revenue_hidden` | $\mathcal R_T$ in the strong price-hidden equilibrium. | `payoff per share` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=price_hidden; r=r_strong; noise=Laplace; cost_law=atoms` | `analytical` | 0.614583 |
| `base_matched_dividend` | $D_0=\mathcal R_T^{feedback}-\mathcal R_T^{hidden}$ at the strong strength; verify residual invariance. | `payoff per share` | `decimal_6` | `tables/equilibrium_controls.csv` | `experiment=matched_dividend; r=r_strong; noise=Laplace; cost_law=atoms` | `numerical diagnostic` | 0.257809 |
| `base_margin_low_cost` | $\zeta_L$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `tables/extensions.csv` | `parameter_set=base; noise=Laplace; cost_law=atoms; declared comparison` | `analytical` | 1.366178511e+0 |
| `base_margin_high_prior` | $\zeta_{H0}$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `tables/extensions.csv` | `parameter_set=base; noise=Laplace; cost_law=atoms; declared comparison` | `analytical` | 1.195833333e+0 |
| `base_margin_high_ceiling` | $\zeta_{H1}$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `tables/extensions.csv` | `parameter_set=base; noise=Laplace; cost_law=atoms; declared comparison` | `analytical` | 2.171548219e-1 |
| `base_margin_weak_trade` | $\zeta_0$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `tables/extensions.csv` | `parameter_set=base; noise=Laplace; cost_law=atoms; declared comparison` | `analytical` | 3.333333333e-3 |
| `base_margin_strong_trade` | $\zeta_1$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `tables/extensions.csv` | `parameter_set=base; noise=Laplace; cost_law=atoms; declared comparison` | `analytical` | 2.411785114e-3 |
| `base_net_surplus_gain` | $\Delta\mathcal W$ at strong strength: (OA.47) and the independent difference of (OA.49). | `surplus per share` | `decimal_6` | `numerics/feedback_comparisons.csv` | `r=r_strong; noise=Laplace; cost_law=atoms; column=W_gain` | `analytical` | 0.080218 |
| `base_revenue_gain` | $\Delta\mathcal R_T$ at strong strength, calculated from conditional entry and independently from mean prices. | `payoff per share` | `decimal_6` | `numerics/feedback_comparisons.csv` | `r=r_strong; noise=Laplace; cost_law=atoms; column=R_T_gain` | `analytical` | 0.257809 |
| `base_entry_change_pp` | $\Delta\mathsf E_{\mathrm{pp}}=100(\mathsf E_{\mathrm{strong}}-\mathsf E_{\mathrm{weak}})$ at the benchmark, from the two validated probability rows; percentage points, not a percentage change. | `percentage_point` | `decimal_2` | `numerics/quantity_registry.csv` | `pp_change; strong=base_entry_strong; weak=base_entry_weak` | `analytical` | 27.28 |

## Exercise C.1/C.3/C.4

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `base_minimum_theorem_margin` | Minimum of the five explicitly defined strict margins, retaining the separate component values in the output. | `payoff margin` | `scientific_10` | `numerics/quantity_registry.csv` | `the five base_margin_* rows` | `analytical` | 2.411785114e-3 |
| `moderate_minimum_theorem_margin` | Minimum of the five explicitly defined strict margins, retaining the separate component values in the output. | `payoff margin` | `scientific_10` | `numerics/quantity_registry.csv` | `the five moderate_margin_* rows` | `analytical` | 8.014731393e-4 |
| `signal_minimum_theorem_margin` | Minimum of the five explicitly defined strict margins, retaining the separate component values in the output. | `payoff margin` | `scientific_10` | `numerics/quantity_registry.csv` | `the five signal_margin_* rows` | `analytical` | 1.454545455e-3 |

## Exercise C.1/C.5

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `logistic_entry_strong` | $\mathsf E$ under logistic noise and atomic costs. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `noise=logistic; cost_law=atoms; r=r_strong` | `analytical` | 0.301509 |
| `logistic_flow_threshold` | $x^*_{\log}$ from the likelihood-ratio inverse, independently checked by a root. | `order units` | `decimal_9` | `tables/equilibrium_controls.csv` | `noise=logistic; cost_law=atoms; r=r_strong` | `analytical` | 5.424598398 |
| `logistic_threshold_noise_sd` | $x^*_{\log}/(b\pi/\sqrt{3})$, using the standard deviation of noise, not aggregate flow. | `standard deviations` | `decimal_6` | `figures_data/posterior_tails.csv` | `noise=logistic; tau=benchmark strong threshold; column=threshold_noise_sd` | `analytical` | 1.495369 |
| `cost_mix_laplace_entry_strong` | $\mathsf E$ under Laplace noise with the complete uniform-mixture cost CDF. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `noise=Laplace; cost_law=uniform_mixture; r=r_strong` | `analytical` | 0.522715 |
| `cost_mix_logistic_entry_strong` | $\mathsf E$ under logistic noise with the complete uniform-mixture cost CDF. | `probability` | `decimal_6` | `tables/equilibrium_controls.csv` | `noise=logistic; cost_law=uniform_mixture; r=r_strong` | `analytical` | 0.301374 |

## Exercise C.2

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `cert_a_r` | Declared incumbent strength of the corresponding certified node. | `model units` | `exact_input` | `input manifest` | `declared input 1.55` | `input` | 1.55 |
| `cert_b_r` | Declared incumbent strength of the corresponding certified node. | `model units` | `exact_input` | `input manifest` | `declared input 1.60` | `input` | 1.60 |
| `cert_c_r` | Declared incumbent strength of the corresponding certified node. | `model units` | `exact_input` | `input manifest` | `declared input 1.65` | `input` | 1.65 |
| `cert_a_v_interval` | Certified bracket for the exact equilibrium root $v^*$; require both endpoint signs, threshold ordering, low-type concavity, and positive global high-type derivative cover. | `order units` | `outward_interval_8` | `numerics/certificates.csv` | `r=1.55; all certificate predicates=true` | `computer-assisted` | [0.46031618,\,0.46031620] (enclosure [0.46031618, 0.46031620]) |
| `cert_a_entry_interval` | Outward enclosure of $\mathsf E(r,v)$ for every $v$ in the certified root bracket. | `probability` | `outward_interval_10` | `numerics/certificates.csv` | `r=1.55; all certificate predicates=true` | `computer-assisted` | [0.5450528898,\,0.5450528922] (enclosure [0.545052889808945713520237620328749119481683845800618298332444, 0.545052892132246689741896675903819707329977318624990770537445]) |
| `cert_a_high_derivative_lower` | The nonnegative lower enclosure $\Gamma_H$ after subtracting the between-grid Lipschitz correction, uniform over the full root bracket. | `payoff per marginal order` | `lower_bound_10` | `numerics/certificates.csv` | `r=1.55; all certificate predicates=true` | `computer-assisted` | 0.0000761777 |
| `cert_b_v_interval` | Certified bracket for the exact equilibrium root $v^*$; require both endpoint signs, threshold ordering, low-type concavity, and positive global high-type derivative cover. | `order units` | `outward_interval_8` | `numerics/certificates.csv` | `r=1.60; all certificate predicates=true` | `computer-assisted` | [0.70747537,\,0.70747539] (enclosure [0.70747537, 0.70747539]) |
| `cert_b_entry_interval` | Outward enclosure of $\mathsf E(r,v)$ for every $v$ in the certified root bracket. | `probability` | `outward_interval_10` | `numerics/certificates.csv` | `r=1.60; all certificate predicates=true` | `computer-assisted` | [0.5487563062,\,0.5487563085] (enclosure [0.548756306279402553094473342650650704987833563703042353794586, 0.548756308461269927283787391337035286049034141128488454660113]) |
| `cert_b_high_derivative_lower` | The nonnegative lower enclosure $\Gamma_H$ after subtracting the between-grid Lipschitz correction, uniform over the full root bracket. | `payoff per marginal order` | `lower_bound_10` | `numerics/certificates.csv` | `r=1.60; all certificate predicates=true` | `computer-assisted` | 0.0027531948 |
| `cert_c_v_interval` | Certified bracket for the exact equilibrium root $v^*$; require both endpoint signs, threshold ordering, low-type concavity, and positive global high-type derivative cover. | `order units` | `outward_interval_8` | `numerics/certificates.csv` | `r=1.65; all certificate predicates=true` | `computer-assisted` | [0.90333198,\,0.90333201] (enclosure [0.90333198, 0.90333201]) |
| `cert_c_entry_interval` | Outward enclosure of $\mathsf E(r,v)$ for every $v$ in the certified root bracket. | `probability` | `outward_interval_10` | `numerics/certificates.csv` | `r=1.65; all certificate predicates=true` | `computer-assisted` | [0.5513607988,\,0.5513608020] (enclosure [0.551360798856776788533769270145071166432320955743300255818651, 0.551360801970062274597481435420114471003452102733480241341781]) |
| `cert_c_high_derivative_lower` | The nonnegative lower enclosure $\Gamma_H$ after subtracting the between-grid Lipschitz correction, uniform over the full root bracket. | `payoff per marginal order` | `lower_bound_10` | `numerics/certificates.csv` | `r=1.65; all certificate predicates=true` | `computer-assisted` | 0.0054921767 |
| `base_m` | $m=(1+e^{2/b})^{-1}$. | `probability` | `decimal_9` | `numerics/thresholds.csv` | `boundary=m; benchmark inputs` | `analytical` | 0.268941421 |
| `base_M` | $M=1-m$. | `probability` | `decimal_9` | `numerics/thresholds.csv` | `boundary=M; benchmark inputs` | `analytical` | 0.731058579 |
| `base_r_pool_unique_sufficient` | $\mathfrak r(k)$, the sufficient pooling-uniqueness boundary. | `model units` | `decimal_9` | `numerics/thresholds.csv` | `boundary=pooling_unique_sufficient; benchmark inputs` | `analytical` | 1.220997512 |
| `base_r_no_trade_exact` | $r_N=\mathfrak r(2k/\rho)$, checked within the stated prior/floor domain. | `model units` | `decimal_9` | `numerics/thresholds.csv` | `boundary=pooling_existence; benchmark inputs` | `analytical` | 1.747877538 |
| `base_r_full_unique_sufficient` | $r_U=\mathfrak r(k/[(1-1/b)\rho m])$. | `model units` | `decimal_9` | `numerics/thresholds.csv` | `boundary=full_orders_unique_sufficient; benchmark inputs` | `analytical` | 2.837416964 |
| `base_r_high_cost_ceiling` | $r_C$ from (OA.20), independently checked against $B_r(M)=c_H$ and its admissible domain. | `model units` | `decimal_9` | `numerics/thresholds.csv` | `boundary=high_cost_ceiling; benchmark inputs` | `analytical` | 3.592658519 |
| `base_laplace_entry_ceiling_left_limit` | $\rho+(1-\rho)(1+e^{-2/b})/4$; the one-sided limit, not automatically the boundary equilibrium. | `probability` | `decimal_9` | `numerics/thresholds.csv` | `boundary=laplace_entry_left_limit; benchmark inputs` | `analytical` | 0.506477395 |
| `cert_a_psi_left_lower` | Outward lower enclosure of $\Psi(r,v_-)$ at the certified left endpoint; must be strictly positive. | `payoff per marginal order` | `lower_bound_12` | `numerics/certificates.csv` | `r=1.55; column=Psi_left_lower; all predicates accepted` | `computer-assisted` | 0.000000000114 |
| `cert_a_psi_right_upper` | Outward upper enclosure of $\Psi(r,v_+)$ at the certified right endpoint; must be strictly negative. | `payoff per marginal order` | `upper_bound_12` | `numerics/certificates.csv` | `r=1.55; column=Psi_right_upper; all predicates accepted` | `computer-assisted` | -0.000000000096 |
| `cert_b_psi_left_lower` | Outward lower enclosure of $\Psi(r,v_-)$ at the certified left endpoint; must be strictly positive. | `payoff per marginal order` | `lower_bound_12` | `numerics/certificates.csv` | `r=1.60; column=Psi_left_lower; all predicates accepted` | `computer-assisted` | 0.000000000123 |
| `cert_b_psi_right_upper` | Outward upper enclosure of $\Psi(r,v_+)$ at the certified right endpoint; must be strictly negative. | `payoff per marginal order` | `upper_bound_12` | `numerics/certificates.csv` | `r=1.60; column=Psi_right_upper; all predicates accepted` | `computer-assisted` | -0.000000000121 |
| `cert_c_psi_left_lower` | Outward lower enclosure of $\Psi(r,v_-)$ at the certified left endpoint; must be strictly positive. | `payoff per marginal order` | `lower_bound_12` | `numerics/certificates.csv` | `r=1.65; column=Psi_left_lower; all predicates accepted` | `computer-assisted` | 0.000000000172 |
| `cert_c_psi_right_upper` | Outward upper enclosure of $\Psi(r,v_+)$ at the certified right endpoint; must be strictly negative. | `payoff per marginal order` | `upper_bound_12` | `numerics/certificates.csv` | `r=1.65; column=Psi_right_upper; all predicates accepted` | `computer-assisted` | -0.000000000242 |

## Exercise C.3

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `signal_entry_weak` | $\mathsf E=(\bar e_H+\bar e_L)/2$, using true-state-conditioned private-signal probabilities. | `probability` | `decimal_6` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_weak` | `analytical` | 0.850000 |
| `signal_entry_strong` | $\mathsf E=(\bar e_H+\bar e_L)/2$, using true-state-conditioned private-signal probabilities. | `probability` | `decimal_6` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_strong` | `analytical` | 0.879438 |
| `signal_trader_accuracy` | The input $a$ displayed as a percentage; no new calculation beyond the change of units. | `percentage` | `percent_integer` | `input manifest` | `a` | `input` | 70\% |
| `signal_buyer_accuracy` | The input $d$ displayed as a percentage; no new calculation beyond the change of units. | `percentage` | `percent_integer` | `input manifest` | `d` | `input` | 75\% |
| `signal_margin_low_cost` | $\zeta_L$ as defined by the corresponding low-cost, high-cost, or trading inequality in (OA.29); use the signal-specific bounds, not the benchmark bound. | `payoff margin` | `scientific_10` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_strong; column=low_cost_margin` | `analytical` | 7.734304988e-1 |
| `signal_margin_high_prior` | $\zeta_{H0}$ as defined by the corresponding low-cost, high-cost, or trading inequality in (OA.29); use the signal-specific bounds, not the benchmark bound. | `payoff margin` | `scientific_10` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_strong; column=private_only_exclusion_margin` | `analytical` | 5.250000000e-2 |
| `signal_margin_high_ceiling` | $\zeta_{H1}$ as defined by the corresponding low-cost, high-cost, or trading inequality in (OA.29); use the signal-specific bounds, not the benchmark bound. | `payoff margin` | `scientific_10` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_strong; column=joint_entry_margin` | `analytical` | 4.526515342e-2 |
| `signal_margin_weak_trade` | $\zeta_0$ as defined by the corresponding low-cost, high-cost, or trading inequality in (OA.29); use the signal-specific bounds, not the benchmark bound. | `payoff margin` | `scientific_10` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_strong; column=weak_order_margin` | `analytical` | 1.454545455e-3 |
| `signal_margin_strong_trade` | $\zeta_1$ as defined by the corresponding low-cost, high-cost, or trading inequality in (OA.29); use the signal-specific bounds, not the benchmark bound. | `payoff margin` | `scientific_10` | `numerics/two_signals.csv` | `a=0.70; d=0.75; r=r_strong; column=strong_order_margin` | `analytical` | 1.797145730e-3 |
| `signal_entry_change_pp` | $\Delta\mathsf E_{\mathrm{pp}}=100(\mathsf E_{\mathrm{strong}}-\mathsf E_{\mathrm{weak}})$ in the declared complementary-signal example, from the two validated probability rows; percentage points, not a percentage change. | `percentage_point` | `decimal_2` | `numerics/quantity_registry.csv` | `pp_change; strong=signal_entry_strong; weak=signal_entry_weak` | `analytical` | 2.94 |

## Exercise C.4

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `moderate_entry_weak` | $\mathsf E$ in the moderate-value feedback equilibrium after every strict theorem margin is verified. | `probability` | `decimal_6` | `numerics/moderate_values.csv` | `declared moderate comparison; column=E_weak` | `analytical` | 0.250000 |
| `moderate_entry_strong` | $\mathsf E$ in the moderate-value feedback equilibrium after every strict theorem margin is verified. | `probability` | `decimal_6` | `numerics/moderate_values.csv` | `declared moderate comparison; column=E_strong` | `analytical` | 0.526805 |
| `moderate_margin_low_cost` | $\zeta_L$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `numerics/moderate_values.csv` | `declared moderate comparison` | `analytical` | 1.965296363e-1 |
| `moderate_margin_high_prior` | $\zeta_{H0}$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `numerics/moderate_values.csv` | `declared moderate comparison` | `analytical` | 3.345238095e-2 |
| `moderate_margin_high_ceiling` | $\zeta_{H1}$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `numerics/moderate_values.csv` | `declared moderate comparison` | `analytical` | 3.013703041e-2 |
| `moderate_margin_weak_trade` | $\zeta_0$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `numerics/moderate_values.csv` | `declared moderate comparison` | `analytical` | 8.095238095e-4 |
| `moderate_margin_strong_trade` | $\zeta_1$ from (OA.68); a strict inequality requires a strictly positive verified value. | `payoff margin` | `scientific_10` | `numerics/moderate_values.csv` | `declared moderate comparison` | `analytical` | 8.014731393e-4 |
| `moderate_entry_change_pp` | $\Delta\mathsf E_{\mathrm{pp}}=100(\mathsf E_{\mathrm{strong}}-\mathsf E_{\mathrm{weak}})$ in the moderate-value example, from the two validated probability rows; percentage points, not a percentage change. | `percentage_point` | `decimal_2` | `numerics/quantity_registry.csv` | `pp_change; strong=moderate_entry_strong; weak=moderate_entry_weak` | `analytical` | 27.68 |

## Exercise C.6

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `value_entry_weak_high_p` | Class-economy $\mathsf E$ at the high reserve, with class-only investor information. | `probability` | `decimal_6` | `tables/reserve_comparisons.csv` | `value_law=uniform_classes; epsilon_V=0.05; r=r_weak; p=1.1` | `analytical` | 0.540309 |
| `value_revenue_weak_low_p` | Class-economy $\mathcal R_T$ using integrated within-class auction payoffs and the validated continuation. | `payoff per share` | `decimal_6` | `tables/reserve_comparisons.csv` | `value_law=uniform_classes; epsilon_V=0.05; r=r_weak; p=0.5` | `analytical` | 0.392665 |
| `value_revenue_weak_high_p` | Class-economy $\mathcal R_T$ using integrated within-class auction payoffs and the validated continuation. | `payoff per share` | `decimal_6` | `tables/reserve_comparisons.csv` | `value_law=uniform_classes; epsilon_V=0.05; r=r_weak; p=1.1` | `analytical` | 0.432173 |
| `value_entry_strong_high_p` | Class-economy $\mathsf E$ at the high reserve, with class-only investor information. | `probability` | `decimal_6` | `tables/reserve_comparisons.csv` | `value_law=uniform_classes; epsilon_V=0.05; r=r_strong; p=1.1` | `analytical` | 0.511638 |
| `value_revenue_strong_low_p` | Class-economy $\mathcal R_T$ using integrated within-class auction payoffs and the validated continuation. | `payoff per share` | `decimal_6` | `tables/reserve_comparisons.csv` | `value_law=uniform_classes; epsilon_V=0.05; r=r_strong; p=0.5` | `analytical` | 0.872367 |
| `value_revenue_strong_high_p` | Class-economy $\mathcal R_T$ using integrated within-class auction payoffs and the validated continuation. | `payoff per share` | `decimal_6` | `tables/reserve_comparisons.csv` | `value_law=uniform_classes; epsilon_V=0.05; r=r_strong; p=1.1` | `analytical` | 1.014500 |
| `pool_posterior_cutoff_low` | Pooled posterior $\Pr(H\mid P=0)$ of the accepted lower-cutoff pool at the endpoint cutoff $c=-\log 2$; joined on the full parameter vector, the exact cutoff label, and the candidate identity. | `probability` | `decimal_6` | `numerics/price_pool_regression.csv` | `h=10; ell=1; p=7; rho=0.25; c_L=1; c_H=6; b=2; k=0.02; r=1.2; noise=Laplace; cost=atoms; prior_H=0.5; q_H=1.0; q_L=-1.0; cutoff_exact=-log2*(1-0/16); candidate_id=c6b:closed_form_construction:c=-log2*(1-0/16); column=pool_posterior` | `analytical` | 0.272979 |
| `pool_posterior_cutoff_high` | Pooled posterior $\Pr(H\mid P=0)$ of the accepted lower-cutoff pool at the endpoint cutoff $c=0$; joined on the full parameter vector, the exact cutoff label, and the candidate identity. | `probability` | `decimal_6` | `numerics/price_pool_regression.csv` | `h=10; ell=1; p=7; rho=0.25; c_L=1; c_H=6; b=2; k=0.02; r=1.2; noise=Laplace; cost=atoms; prior_H=0.5; q_H=1.0; q_L=-1.0; cutoff_exact=-log2*(1-16/16); candidate_id=c6b:closed_form_construction:c=-log2*(1-16/16); column=pool_posterior` | `analytical` | 0.303265 |
| `pool_entry_cutoff_low` | Preparation probability $\mathsf E$ under the accepted lower-cutoff pool at $c=-\log 2$ (the buyer prepares only at a positive price that justifies it). | `probability` | `decimal_6` | `numerics/price_pool_regression.csv` | `h=10; ell=1; p=7; rho=0.25; c_L=1; c_H=6; b=2; k=0.02; r=1.2; noise=Laplace; cost=atoms; prior_H=0.5; q_H=1.0; q_L=-1.0; cutoff_exact=-log2*(1-0/16); candidate_id=c6b:closed_form_construction:c=-log2*(1-0/16); column=preparation_probability` | `analytical` | 0.151805 |
| `pool_entry_cutoff_high` | Preparation probability $\mathsf E$ under the accepted lower-cutoff pool at $c=0$ (the buyer prepares only at a positive price that justifies it). | `probability` | `decimal_6` | `numerics/price_pool_regression.csv` | `h=10; ell=1; p=7; rho=0.25; c_L=1; c_H=6; b=2; k=0.02; r=1.2; noise=Laplace; cost=atoms; prior_H=0.5; q_H=1.0; q_L=-1.0; cutoff_exact=-log2*(1-16/16); candidate_id=c6b:closed_form_construction:c=-log2*(1-16/16); column=preparation_probability` | `analytical` | 0.125000 |
| `pool_revenue_cutoff_low` | Expected seller revenue $\mathcal R_T$ under the accepted lower-cutoff pool at $c=-\log 2$, from the closed form checked against direct integration. | `payoff per share` | `decimal_6` | `numerics/price_pool_regression.csv` | `h=10; ell=1; p=7; rho=0.25; c_L=1; c_H=6; b=2; k=0.02; r=1.2; noise=Laplace; cost=atoms; prior_H=0.5; q_H=1.0; q_L=-1.0; cutoff_exact=-log2*(1-0/16); candidate_id=c6b:closed_form_construction:c=-log2*(1-0/16); column=seller_revenue` | `analytical` | 0.687364 |
| `pool_revenue_cutoff_high` | Expected seller revenue $\mathcal R_T$ under the accepted lower-cutoff pool at $c=0$, from the closed form checked against direct integration. | `payoff per share` | `decimal_6` | `numerics/price_pool_regression.csv` | `h=10; ell=1; p=7; rho=0.25; c_L=1; c_H=6; b=2; k=0.02; r=1.2; noise=Laplace; cost=atoms; prior_H=0.5; q_H=1.0; q_L=-1.0; cutoff_exact=-log2*(1-16/16); candidate_id=c6b:closed_form_construction:c=-log2*(1-16/16); column=seller_revenue` | `analytical` | 0.609643 |

## Exercise E

| Key | Definition | Units | Display rule | Source file | Selector | Status | Value |
|---|---|---|---|---|---|---|---|
| `seed_python_version` | Documented software version for the distributed verification results; a new run records its actual version separately. | `version` | `literal_string` | `software metadata` | `declared input 3.13.5` | `input` | 3.13.5 |
| `seed_numpy_version` | Documented software version for the distributed verification results; a new run records its actual version separately. | `version` | `literal_string` | `software metadata` | `declared input 2.3.5` | `input` | 2.3.5 |
| `seed_scipy_version` | Documented software version for the distributed verification results; a new run records its actual version separately. | `version` | `literal_string` | `software metadata` | `declared input 1.17.0` | `input` | 1.17.0 |
| `seed_mpmath_version` | Documented software version for the distributed verification results; a new run records its actual version separately. | `version` | `literal_string` | `software metadata` | `declared input 1.3.0` | `input` | 1.3.0 |
