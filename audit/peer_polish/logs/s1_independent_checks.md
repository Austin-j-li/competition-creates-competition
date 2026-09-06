# S1-B/S1-C independent checks

Generated 2026-09-05 23:57:31; elapsed 1639 s; Python 3.12.13, numpy 2.5.2, scipy 1.18.1, mpmath 1.4.1.

Controls: quadrature targets 1e-12 abs/rel (C.0 1e-11 tightened by ten), order intervals 800 (C.0 400 doubled), line cut at 60 b beyond the outermost breakpoint with the omitted mass bounded (Laplace e^{-60}, logistic 2/(1+e^{60})), mpmath 40 digits for closed forms, 30 digits for auction integrals.

## Counts per test

| test | pass | fail | info | required failures |
|---|---:|---:|---:|---:|
| T02 | 140 | 0 | 0 | 0 |
| T03 | 206 | 0 | 48 | 0 |
| thresholds | 29 | 0 | 0 | 0 |
| landmark | 10 | 0 | 0 | 0 |
| T04 | 1092 | 0 | 0 | 0 |
| T05 | 216 | 0 | 0 | 0 |
| T07 | 104 | 0 | 0 | 0 |
| T06 | 82 | 0 | 2 | 0 |
| T08 | 24 | 0 | 0 | 0 |
| T09 | 144 | 0 | 0 | 0 |
| T10 | 44 | 0 | 6 | 0 |
| T11 | 22 | 0 | 0 | 0 |
| T12 | 54 | 0 | 12 | 0 |
| T13 | 21 | 0 | 0 | 0 |
| T15 | 153 | 0 | 0 | 0 |
| T14 | 3451 | 0 | 0 | 0 |
| provenance | 10 | 0 | 0 | 0 |

## Landmarks

| landmark | independent | spec value | abs diff | status |
|---|---:|---:|---:|---|
| strong_preparation (base/Laplace/atoms r=3 feedback full E) | 0.5227572972597378580444496 | 0.5227572973 | 4.03e-11 | pass |
| strong_high_value_ownership (base/Laplace/atoms r=3 feedback full O_H) | 0.3241924257758907071252122 | 0.3241924258 | 2.41e-11 | pass |
| strong_target_proceeds (base/Laplace/atoms r=3 feedback full R_T) | 0.8723920450946403230205142 | 0.8723920451 | 5.36e-12 | pass |
| frozen_prep_weak (base/Laplace/atoms r=1.2 frozen full E) | 0.5621780582084275588062021 | 0.5621780582 | 8.43e-12 | pass |
| strong_hidden_proceeds (base/Laplace/atoms r=3 price_hidden R_T) | 0.6145833333333333333333333 | 0.6145833333 | 3.33e-11 | pass |
| logistic_strong_prep (base/logistic/atoms r=3 feedback full E) | 0.3015088516350812798000066 | 0.3015088516 | 3.51e-11 | pass |
| moderate_strong_prep (moderate r=1.5 feedback full E) | 0.5268046621928848548987668 | 0.5268046622 | 7.12e-12 | pass |
| atomless_laplace_strong_prep repo table vs landmark (independent value checked in T04) | 0.5227147163813063 | 0.5227147164 | 1.87e-11 | pass |
| atomless_logistic_strong_prep repo table vs landmark (independent value checked in T04) | 0.30137412771940725 | 0.3013741277 | 1.94e-11 | pass |
| net_surplus_gain repo vs landmark (independent value checked in T10) | 0.080217534836442 | 0.0802175348 | 3.64e-11 | pass |
| logistic strong preparation vs landmark | 0.3015088516350812798000066 | 0.3015088516 | 3.51e-11 | pass |
| moderate E_strong vs landmark | 0.5268046621928848548987668 | 0.5268046622 | 7.12e-12 | pass |
| complementary strong preparation vs landmark | 0.8794375515549989 | 0.8794375516 | 4.50e-11 | pass |

## Failures (0)

None.

## Deviation-scan error budgets (T07, T13, T14: maximum over rows)

364 state-scans; max quadrature error 2.09e-12; max tail-truncation bound 3.29e-26 (cut at 60 b); between-grid coverage bound: first-order Lipschitz 1.92e-03, second-order (OA.63) 9.89e-07.
The between-grid bound is a coverage budget for the finite grid and is not itself a certificate at the 1e-7 deviation tolerance. Benchmark analytical margins are checked separately in T06; signal margins and status distinctions are checked in T14/T15. Rows outside the stated theorem region retain their numerical-diagnostic status.
