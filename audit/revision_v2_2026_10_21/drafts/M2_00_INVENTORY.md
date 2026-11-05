# M2 inventory: every occurrence affected by the zero preparation cost

Source files, read only: `overleaf/paper-revision/main.tex` (2638 lines) and
`overleaf/paper-revision/online_appendix.tex` (3703 lines). Line numbers refer to those files
as read on 21 October 2026.

Search terms: `c_L`, `c_{L}`, `\zeta_L`, low-cost / low cost, `(A1)` and `eq:paper-a1`, floor,
pool (all senses), vanish, Proposition A.10, A.11, C.6b, `p_L`, and the floor formulas
`B_r(m)`, `B_{r_1}(m)`, `B(m)`. One inventory row can cover a consecutive passage; every line
that a search returned appears in exactly one row.

Raw line counts from the searches. A line with two search terms counts in both rows of this
count list, so the counts do not add up to a line total.

- main.tex: `c_L` / low-cost 50 lines; (A1) 6; floor 17; pool 29; vanish 3; A.10 6; A.11 1
  (an equation tag); C.6 1; `p_L` 4.
- online_appendix.tex: `c_L` / low-cost 38 lines; (A1) 6; floor 18; pool 77; vanish 9;
  A.10 5; A.11 9; C.6 25; `p_L` 5.

Actions: **D** delete, **R** rewrite, **K** keep. Owners: **A** drafter A regions
(main.tex Sections 1–4, Section 5.2, Appendix A.1–A.3, the Nonemptiness subsection);
**B** drafter B regions (Section 5.1 noise part, Appendix A.4 logistic part, Online Appendix
C.5 lines 2631–2632); **M2** the regions in the M2 task; **M2-x** Online Appendix passages
outside the M2 list that only restate a `c_L`, floor, or pool item (the M2 task covers any
`c_L` reference elsewhere in that file). M2-x rows that overlap the general-model rewrite are
marked for the integrator to merge, not to apply blindly.

Two homonyms need care in every row below.

- "Pooling" in Proposition A.4, Online Appendix A.5, C.1, and C.2 means the zero-order
  trading outcome. That result survives. It is not price pooling.
- "Bidder pool" in the introduction, the conclusion, and one bibliography title names the set
  of bidders. It survives.

## 1. main.tex, regions owned by drafter A

| Lines | Item | Action | Owner |
|---|---|---|---|
| 188 | "low-cost challenger prepares" in the introduction summary | R: say the zero-cost challenger; the comparison itself stands | A |
| 197 | "participation returns to its floor" (Proposition 2(iii) preview) | K: the floor is the entry level `\rho`; it now holds at every belief | A |
| 203 | "bidder pool endogenous" in the entry literature | K: homonym, no price pool | A |
| 301–303 | Cost definition `c_L` with probability `\rho`, `0\le c_L<c_H`, "not a low-cost buyer and a high-cost buyer" | R: cost is `0` with probability `\rho` and `c_H` otherwise; drop the ordering `0\le c_L<c_H` | A |
| 508, 525 | Price sufficiency under the hypothesis `c_L<B_r(m)`; "Under this floor" | R: drop the hypothesis; sufficiency is unconditional on the benchmark support | A |
| 561–562 | Bounds use "entry floor `\rho`" and "posterior floor `m`" | K: both bounds stand; the entry floor needs no condition now | A |
| 573 | "low-cost preparation only" in the Proposition 2 preview | R: zero-cost preparation only | A |
| 584–585 | Condition (A1), `0\le c_L<B_{r_1}(m)`, label `eq:paper-a1` | D: delete the condition and its label; integrator decides whether (A2)–(A3) keep their numbers | A |
| 605 | Proposition 2(iii) needs the separate condition `c_L<B_{r_2}(m)` | R: delete that condition; keep `B_{r_2}(M)<c_H` | A |
| 612–619 | Explanation of (A1) and the three uses of the participation floor | R: state that the zero-cost realization prepares at every price, then give the same three uses | A |
| 622–635, incl. 624, 627, 628, 631–633 | Two weaker-floor cases, `B_r(m)<c_L\le B_r(1/2)` and `c_L>B_r(1/2)`; "flows can pool at one price" at 628 | D: both cases need a positive low cost and no longer occur | A |
| 646 | "only low-cost" preparation without trade | R: zero-cost wording | A |
| 721, 753 | Entry `\rho` in the controls and Table 2 text | K: entry, orders, and proceeds do not change; only net-surplus levels in Table 2 change, through the pipeline | A |
| 873–884 (Section 5.2) | No search term; "costs satisfying the strict inequalities" | K: check the sentence once (A1) is gone; the moderate example stands with cost `0` in place of `0.3` | A |
| 1351, 1358–1359 | Proposition A.2 hypothesis `c_L<B_r(m)` and its "Floor" step | R: drop the hypothesis; the step becomes "the zero-cost type prepares, since gross profit is positive at every feasible posterior on this support" | A |
| 1476, 1494, 1535, 1538 | Proof of Proposition 2 uses (A1), the floor at `r_2`, and "separate from (A1)" | R: replace each use by the unconditional entry floor; part (iii) keeps only the `B_{r_2}(M)<c_H` condition beside (A3) | A |
| 1582, 1623, 1799, 1803 | "Pooling" and "pooling margin" in and around Proposition A.4 | K: zero-order pooling, not price pooling | A |
| 1584 | Domain `\mathcal D=\{r:c_L<B_r(m),\ B_r(1/2)<c_H\}` | R: `\mathcal D=\{r\in(\ell,h):B_r(1/2)<c_H\}` | A |
| 1944–1946 | Nonemptiness chooses `c_L` strictly between zero and `B_{r_1}(m)` and derives `c_L<c_H` | R: no choice is left; the cost `0` lies below `c_H` because `0<B_{r_1}(m)<B_{r_0}(1/2)<c_H` | A |

## 2. main.tex, regions owned by drafter B

| Lines | Item | Action | Owner |
|---|---|---|---|
| 825–861 | Section 5.1 noise text and Figure 3 note; no `c_L`, floor, or pool term except "baseline preparation `\rho`" at 852 | K for this inventory; line 860 is the informativeness sentence that the noise rewrite handles | B |
| 1857–1864, at 1860 | Proposition A.5 holds "under conditions (A1) to (A3)" | R: cite the surviving conditions only; the logistic argument does not use a low cost | B |
| 1877–1880 | Blackwell comparison paragraph after Proposition A.5 | K for this inventory; no `c_L` item. Listed so the integrator does not expect an M2 fragment here | B |

## 3. main.tex, M2 regions

| Lines | Item | Action | Fragment |
|---|---|---|---|
| 862–871, at 864, 867, 870 | Atomless-cost paragraph: "every low-cost realization prepares", entry floor, half-width `\varepsilon_C=0.1`, entry 0.522715 and 0.301374 | R: the low component starts at zero; entry numbers become placeholders | M2_01 |
| 886–926, at 903, 910 | Section 5.3: "positive entry floor leaves a strictly positive coefficient" | R at 903 and the sentence before Table 3 only in wording; the example numbers, Table 3, and Proposition A.7 reference stand | M2_02 |
| 930–967, at 940, 944 | Section 6.1: atomless costs in the access result; entry `\rho` when the price is hidden | R at 940 in one phrase; K for the proceeds numbers, the dividend 0.257809, and the argument, which does not use `c_L` | M2_03 |
| 969–1016 | Section 6.2 bargaining; no search term | K: no fragment | — |
| 1017–1059 | Section 6.3 reserve text and Table 4; no search term before 1060 | K: the two-reserve numbers stand, because the old cost `1` already lay below gross profit at the lowest belief at both reserves. The pipeline must confirm this. See the notes file | — |
| 1060–1069 | Price-pooling paragraph; reference to the Online Appendix subsection "Price pooling when preparation can vanish" | R: one short paragraph. The floor holds at every reserve in the domain, so at fixed orders the price reveals beliefs wherever the target-payoff spread is positive | M2_03 |
| 1079 | Section 7: "preparation returns to its floor" | K: Proposition 2(iii) stands; the floor is `\rho` | M2_04 (no-change note) |
| 1085 | "The bidder pool in a takeover" | K: homonym | — |
| 1094–1097 | Conclusion: "the price-pooling rules that can differ at identical orders" | R: continuations can differ through their orders; at fixed orders the price experiment is tied to the orders | M2_04 |
| 1137 | Bibliography title *Bidder Pools in Mergers and Acquisitions* | K: not an M2 region; homonym | — |
| 1882–1924, at 1887–1896, 1905, 1913, 1920 | Atomless costs: support `[c_L-\varepsilon_C,c_L+\varepsilon_C]`, `c_L-\varepsilon_C\ge0`, `c_L+\varepsilon_C<B_{r_1}(m)`, Proposition A.6 and proof | R: support starts at zero, `[0,\varepsilon_C]`; keep Proposition A.6, its label, equation (A.24), and the proof structure | M2_05 |
| 1950–2136, at 2006, 2046 | Appendix A.5: first condition `c_L<B_{r_1}(\phi_-(\mu_-))` in (A.29); proof sentence that uses it | D for the condition at 2006; R at 2043–2047. K for the rest, including (A.28), the entry rates, and entry above `\rho` | M2_06 |
| 2137–2261, at 2235 | Appendix A.6: "Low-cost preparation is unchanged in the matched comparison" | R: zero-cost wording. K for Propositions A.8 and A.9, (A.40), (A.41), and both differences, which never contained `c_L` | M2_07 |
| 2264–2335 | Appendix A.7 payoffs and the continuation object (A.43)–(A.44) | K: a continuation is still the whole object, and the seller problem still needs a selection after every reserve | — |
| 2336–2465, incl. 2339, 2342–2344, 2370, 2393–2395, 2403, 2424, 2447, 2460–2464 | Subsection "Price pooling at fixed orders", price rule (A.45), Proposition A.10, (A.46)–(A.49), endpoint numbers 0.272979, 0.303265, 0.151805, 0.125000, 0.687364, 0.609643 | D for the family, the proposition, and its numbers. R for the subsection: a short argument that fixed orders fix the price experiment wherever the spread is positive. The key step `3\bar\mu_c<1=c_L` at 2393 fails at cost zero, since `3\bar\mu_c>0` | M2_08 |
| 2466–2512, incl. 2475, 2479, 2483–2487, 2492, 2507–2508 | Exact reserve events: `B_p(m)=m(h-p)=c_L`, `p_L=h-c_L/m` (A.50), `B(M)=Mc_L/m`, entry `\rho`, `\mathcal R_T=\rho p_L/2`; strong event (A.51) with floor `mg_H=mc_H/M>c_L` | R: (A.50) becomes `p_L=h`, an endpoint with no rent and no offsets above it in the domain. Keep (A.51) and its derivation; its floor sentence becomes `mg_H=mc_H/M>0`. Keep both equation labels | M2_08 |
| 2531–2534 | Outcome measures at "the weak-incumbent floor event" and the ceiling event | R: name the endpoint `p_L=h`. K for (A.52) and all four probabilities | M2_08 |
| 2566 | "which vanishes locally when orders stay at their bounds" | K: a derivative term, not vanishing preparation | — |
| 2570, 2576–2583 | Local regularity and the reserve sweep; "at a price pool" at 2572; event reserves (A.50)–(A.51) included | R at 2572 only, plus one clause that names the endpoint. K for (A.53)–(A.54) and the open status of seller-optimal terms | M2_08 |
| 2587–2619, at 2591, 2602, 2613 | Parameter vectors (A.55)–(A.57) with `c_L` values `1`, `0.3`, `1` | R: drop the `c_L` entry from each vector; the cost is `0` with probability `\rho` and `c_H` otherwise. Keep every other number | M2_09 |
| 2621–2623 | "The atomless-cost half-width is `\varepsilon_C=0.1`" | R: the low support starts at zero, so `\varepsilon_C` is a width from zero there and a half-width only around `c_H`; its value becomes a placeholder | M2_09 |
| 2625–2636, at 2632 | Price-pool family declaration, cutoff grid, negative controls; exact events `p_L=h-c_L/m` and `p_H` | D for the family declaration, the grid, and the controls. R for the event sentence: `p_L=h` at `r_0`, `p_H` unchanged | M2_09 |

## 4. online_appendix.tex, region owned by drafter B

| Lines | Item | Action | Owner |
|---|---|---|---|
| 2630–2632 | C.5: "do not claim equal variance or a Blackwell ordering between the laws" | K for this inventory; no `c_L` item. The noise rewrite owns these lines | B |

Line 2646 in the same subsection, "recheck the low-cost floor", is not in the B lines. It
appears below as an M2-x row.

## 5. online_appendix.tex, M2 regions

| Lines | Item | Action | Fragment |
|---|---|---|---|
| 749–770, at 751–756, 762, 764, 766 | A.6 atomless costs: supports on `[c_L-\varepsilon_C,c_L+\varepsilon_C]`, conditions `c_L-\varepsilon_C\ge0`, `c_L+\varepsilon_C<B_{r_1}(m)`, (OA.26), `e\ge\rho` | R: low support `[0,\varepsilon_C]` with `\varepsilon_C<B_{r_1}(m)`. Keep (OA.26), the entry rule, and the atomless-not-density point | M2_10 |
| 833–1053, at 855, 900–902 | A.7 signals: first line of (OA.29), `c_L<B_{r_1}(\phi_-(\mu_-))`; "low-cost restriction … make low-cost preparation optimal" | D for the first line of (OA.29); R at 900–902. K for (OA.28), (OA.30)–(OA.41), and the entry formulas | M2_11 |
| 1108–1196, at 1116, 1144–1145, 1163 | A.9 welfare: "all low-cost realizations enter in both environments"; realized gain can fall short of "the cost paid"; strict-support conditions | R: zero-cost wording. K for (OA.45)–(OA.49). The paid-cost term in (OA.49) is zero for the zero-cost realization, so the level `\mathcal W` changes while (OA.47)–(OA.48) do not | M2_12 |
| 1197–1356, at 1264–1271, 1283–1299, 1346 | A.10 sale design: "a positive entry floor holds"; "If entry vanishes on a set of flows … those flows share the no-entry price"; the C.6 construction "pools exactly the zero-entry preimage"; reference to A.11's family at 1291–1293; atomic-threshold sentence | R: entry is at least `\rho` at every reserve in the domain; a price atom can still collect flows with one posterior, and the buyer then conditions on the whole preimage. Retire the A.11 family reference. K for (OA.50)–(OA.56) and the regularity conditions | M2_13 |
| 1357–1609, incl. 1375, 1392, 1419–1420, 1457, 1461–1467, 1474–1479, 1509, 1564–1566, 1586–1609 | A.11 price pooling subsection: declared `c_L = 1`, price family (OA.58), pooled posterior (OA.60), `3\bar\mu_c<1=c_L`, Proposition OA.3, outputs (OA.64), cutoff grid, negative controls | D for the family, Proposition OA.3, (OA.57)–(OA.64) as a group, the grid, and the controls. R for the subsection: keep the heading number A.11 and label `oa-a-pools` with a short note on price atoms. No other subsection then moves | M2_14 |
| 1852–2103 (C.0), at 1878, 1894, 1907 | Three input declarations with `c_L = 1`, `c_L = 0.3`, `c_L = 1` | R: `c_L = 0` in all three declarations. The key stays until the numerics contract renames it; the integrator and the numerics team decide that together. See the notes file | M2_15 |
| 1941–1961, at 1945–1948, 1957 | Continuation controls: `pool_reserve`, cutoff grid, negative controls; tie rule "lower plateau enters at `B(m) = c_L`" | D for the three pool controls. R for the tie rule: the lower plateau binds only at `B(m)=0`, the endpoint `p=h` in the reserve domain | M2_15 |
| 1963–1977, at 1964, 1966 | "the two regression exercises C.6b and C.6c"; "the four checks of A.11" for a price atom | R: the event exercise C.6c remains, and the same four atom checks stay for plateau atoms. Retire the C.6b name here | M2_15 |
| 2060–2063, at 2061 | Parameter columns `h, ell, p, rho, c_L, c_H, b, k, r` | R: keep the column, record that every declared value is now `0`. Flagged with the declaration rows above | M2_15 |
| 2676–2955 (C.6), at 2703–2709, 2719–2739 | Complete continuations: "every positive-mass price pool", zero-entry flows pool at `t_0`, (OA.79), the A.11 family as a warning at 2730–2732 | R: keep the whole-object rule and (OA.79) for any price atom; entry cannot vanish on the part of the domain with a positive spread, so the construction prices each flow by inversion there | M2_16 |
| 2741–2747 | Degenerate reserves: `e_0=H_C(B(1/2))`, "When `e_0=0`, no trade and no entry" | K as a conditional guard, with one added clause: under the declared atomic law `e_0\ge\rho`, so that branch needs a cost law with no atom at zero | M2_16 |
| 2749–2754, at 2751 | "the actual floor `e(m)=H_C(B_r(m))`" | K for the formula; R for one clause that states `e(m)\ge\rho` under the declared laws | M2_16 |
| 2758–2777, at 2763, 2772–2773 | Event grid: "`p_L=h-c_L/m`", tie rule "at `p_L` … under `B(m)=c_L`" | R: `p_L=h` and `B(m)=0`. Offsets above `h` stay outside the domain under the existing grid rule | M2_16 |
| 2784 | Solver "checks pooling, full orders, asymmetric roots" | K: zero-order pooling | — |
| 2806, 2861, 2866, 2868, 2873–2874 | Continuation schema columns: `low_cost_floor_margin`, `no_entry_price_mass`, `posterior_in_no_entry_pool`, `low_cost_floor_relation`, `pool_id` and the other `pool_*` columns | K for the column names as a schema, R for their definitions below: a zero-entry atom can arise only at a degenerate reserve under the declared laws. The numerics team owns any column rename | M2_16 |
| 2900–2921, at 2900, 2912, 2915–2921 | Data dictionary for `low_cost_floor_relation`, `price_rule_id` with "its pool sets", and the `pool_*` columns, ending "not written as a no-entry pool" | R: the relation compares `B_r(m)` with zero; the `pool_*` columns describe a constant-price atom when one exists | M2_16 |
| 2933 | "pooled-belief" diagnostic in `belief_error` | K: the diagnostic still applies at a plateau atom | — |
| 2956–3037, incl. 2958–2967, 2969–3008, 3014–3036 | C.6b exercise: regression for A.11, cutoff family, exact targets `t_H=7, g_H=3`, acceptance bounds `7/32` and `143/1600`, output file `price_pool_regression.csv`, feed line with registry keys `pool_*` | D for the exercise content and its outputs. R for the subsection: keep the number C.6b and label `oa-c-price-pools` as a retired-exercise note that states the reason | M2_17 |
| 3038–3084, at 3048, 3053–3062, 3058 | C.6c events: "`p_L` at every strength", floor classification at `p_L`, offsets above the event classify the floor as strictly negative, `\mathcal R_T=\rho p_L/2`; at `p_H`, "a strictly positive floor" | R: `p_L=h` is an endpoint; offsets run below it only; `\mathcal R_T=\rho h/2`. At `p_H` the floor value is `mc_H/M>0`, computed, not assumed. K for the `p_H` acceptance items and the outcome identities | M2_18 |
| 3067–3070 | Sampled reserve `6.280` with `\mathsf E=\rho`, sale `\rho/2`, `\mathcal R_T=\rho\,(6.280)/2` | R: the value sat next to the old `p_L`. Its revenue formulas hold at any reserve in `(r,h)` with the high cost excluded, but its status as a sampled maximum must come from the new sweep. Use a placeholder | M2_18 |
| 3121–3228 (C.8), at 3198 | Quantity-family row "Price-pool endpoints — C.6b" | D: no exercise produces these quantities now | M2_19 |
| 3202–3216, at 3206, 3212–3213 | Shared definitions; "the price-pool keys select on the symbolic cutoff" | D for the price-pool clause. K for `\mathsf E`, `\mathsf O_H`, `\mathcal R_T`, and the margin references (OA.77) and (OA.29) | M2_19 |
| 3218–3224, at 3223 | Production order: "the price-pool regression, and the event exercise follow" | R: the event exercise follows the reserve sweep; no regression step | M2_19 |

## 6. online_appendix.tex, other passages that restate the same items (M2-x)

These rows sit in subsections that restate the model, Proposition 2, or the baseline exercises.
The fragments in M2_20 give one-line replacements. Where the general-model rewrite also
rewrites the passage, the integrator should take the substance and drop the M2 line.

| Lines | Item | Action | Fragment |
|---|---|---|---|
| 207–208 | A.1 cost definition, `c_L` with probability `\rho`, `0\le c_L<c_H` | R: cost `0` with probability `\rho`, `c_H` otherwise | M2_20 |
| 224–232, at 228 | A.1 restates (A1)–(A3) as (OA.1), first line `0\le c_L<B_{r_1}(m)` | D for the first line; the sentence then names the surviving conditions. Integrator merges with the main-text numbering decision | M2_20 |
| 298 | A.2: "When `c_L<B_r(m)`, the cost-averaged rule is bounded below by `\rho`" | R: the bound holds at every belief, since the zero-cost realization always prepares | M2_20 |
| 379 | A.3: "For any candidate equilibrium with the low-cost entry floor" | R: drop the qualification; `e(P)\ge\rho` in every candidate equilibrium | M2_20 |
| 490, 512 | A.4 proof: "(A1) give the entry floor"; "(A1) admits low-cost preparation" | R: Proposition A.1 plus the zero cost give the floor; (A2) alone excludes the high cost at the prior | M2_20 |
| 625 | A.5 domain `\mathcal D` with `c_L<B_r(m)` | R: drop that member, as in main.tex line 1584 | M2_20 |
| 629–641 | A.5 pooling outcome, pooling-existence and pooling-uniqueness boundaries | K: zero-order pooling | — |
| 663 | "the support and floor conditions" in the root check | R: support conditions, plus `B_r(m)>0` where the check needs it | M2_20 |
| 683–685 | Proposition 2(iii) restatement with "(A1) to (A3)" and "the low-cost floor at `r_2`" | R: surviving conditions at `r_0,r_1`, and `B_{r_2}(M)<c_H` at `r_2` | M2_20 |
| 772–792, at 787–789 | A.6 nonemptiness chooses `c_L` between zero and `B_{r_1}(m)` | R: as at main.tex 1944–1946. Integrator checks against drafter A's nonemptiness fragment | M2_20 |
| 798–803, at 800 | Lemma OA.1 holds "Under (A1) and (A2)" | R: under (A2) and the two stated cost bounds | M2_20 |
| 813–820, at 817–818 | Lemma OA.2 replaces (A1)–(A3) by `c_L<B_{r_1}(\mu_-)` and two further conditions | R: drop the first condition; at a general prior the zero-cost realization prepares because gross profit is positive at `\mu_-` on this support. Integrator merges with the general-prior rewrite | M2_20 |
| 1828–1831 | B.6 certificate requires "low-cost participation and high-cost prior exclusion" and "a positive pooling-existence margin" | R for the first phrase: zero-cost participation, which the bracket check reads as `B_r(m)>0`. K for the pooling-existence margin (zero-order pooling) | M2_20 |
| 2107–2113, at 2111–2112 | C.1 inputs: uniform components on `[c_L-\varepsilon_C,c_L+\varepsilon_C]` and `[c_H-\varepsilon_C,c_H+\varepsilon_C]` | R: low component on `[0,\varepsilon_C]` under the declared law; exact law and endpoint come from the numerics report | M2_20 |
| 2118–2133, at 2122, 2132 | C.1 margins (OA.77): `\zeta_L=B_{r_1}(m)-c_L`; collapse node needs `B_{r_2}(m)-c_L>0` | R: `\zeta_L=B_{r_1}(m)`, the gross profit at the lowest belief, and `B_{r_2}(m)>0`. The margin name stays; its values change and come from the pipeline | M2_20 |
| 2136, 2157 | C.1 "Pooling has `q_H=q_L=0`"; price-hidden control has "pooling at weak strength" | K: zero-order pooling | — |
| 2295 | C.2: "membership in the maintained floor/prior domain" | R: the maintained domain `\mathcal D` of A.5, which no longer contains a floor member | M2_20 |
| 2329, 2417–2418, 2441, 2465 | C.2 pooling-existence flag and columns `pooling_exists`, `pooling_unique_bound`, `pooling_margin_lower`, `pooling_existence` | K: zero-order pooling; schema names stay | — |
| 2386–2387 | C.2: "the low-cost floor `c_L<B_r(m)` holds at every node, entry is positive at every flow, and no price pool combines distinct raw posteriors" | R: gross profit at the lowest belief is positive at every node, so the same two conclusions hold without a condition | M2_20 |
| 2445 | C.2 schema column `low_cost_floor_valid` | K as a schema name; under the new declarations it records `B_r(m)>0`. Numerics owns any rename | M2_20 (note only) |
| 2500–2501 | C.3: "the five strict margins from (OA.29): the low-cost floor, …" | R: four condition margins remain in (OA.29); the gross profit at the lowest joint posterior stays as a recorded quantity, not a condition | M2_20 |
| 2549–2554 | C.3 scalar-margin names, "low cost to `low_cost_margin`" | K for the column name; its definition follows the row above | M2_20 (note only) |
| 2583–2596, at 2589, 2595 | C.4 construction (OA.78) sets `c_L=B_{r_1}(m)/2`; "Check `c_L<c_H`" | D for the `c_L` choice in (OA.78); R for the check: `0<c_H` and the surviving inequalities. Keep the `k` and `c_H` midpoints | M2_20 |
| 2608–2614 | C.4 output columns `c_L`, `\zeta_L` in two files | K as schema names, with `c_L` recorded as `0` and `\zeta_L` as at (OA.77). Numerics owns any rename | M2_20 (note only) |
| 2643–2649, at 2646 | C.5 threshold rows: "recheck the low-cost floor, cost ordering, and global full-order bound" | R: recheck `B_r(m)>0`, the ordering `0<c_H(\tau)`, and the full-order bound | M2_20 |
| 3482 | E.1 run list includes `numerics/exercises/c6b_price_pools.py` | D: the retired exercise leaves the run list. The numerics team confirms the file disposition | M2_20 |
| 3651 | E.3: "the event candidates are reported online under the heading fixed in C.6" | K: the event exercise remains | — |

## 7. Items with no occurrence to change

- main.tex Section 6.2 (969–1016) and the bargaining proof in Appendix A.6 (2139–2186)
  contain no search term. Proposition A.8 stands as written.
- The closed forms (4), (9)–(12), entry, ownership, and target proceeds never contained
  `c_L`. Their numbers stand at the declared vectors. Net surplus `\mathcal W` is the one
  level that moves, by the zero-cost share of the old cost. Its new levels come from the
  pipeline, not from these fragments.
- Propositions 1, 2, 3, A.1–A.9, and OA.1–OA.2 survive. Proposition A.10 and
  Proposition OA.3 are the only numbered results that fall.
