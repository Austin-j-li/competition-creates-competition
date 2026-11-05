# Integration record: revised manuscript, 21 October 2026

## 1. Result

- The revised manuscript is on branch `revision-alex-2026-10-21` of `overleaf/paper-revision`.
  Commit `ac4e37e` sits on base `9b9bf3c`. Nothing is pushed.
- The commit changes `main.tex`, `online_appendix.tex`, and six tables. No PDF is committed.
- Both documents compile with `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build`.

| Document | Base pages | New pages | Errors | Warnings | Overfull boxes | Underfull boxes |
|---|---:|---:|---:|---:|---:|---:|
| `main.tex` | 73 | 90 | 0 | 0 | 0 | 0 |
| `online_appendix.tex` | 57 | 59 | 0 | 0 | 0 | 5 |

The five underfull boxes also occur in the base build. They are in unchanged C.2 text, in the
generated table `table_reserve_details.tex`, and in the C.6 data dictionary (long `\texttt` names).
The logs show no undefined reference, undefined citation, or multiply defined label.

## 2. How to rebuild

```sh
cd /home/uctpiaj/work/Projects/competition-creates-competition
.venv/bin/python audit/revision_v2_2026_10_21/scripts/integrate.py          # writes the clone
.venv/bin/python audit/revision_v2_2026_10_21/scripts/integrate.py --check  # checks only
cd overleaf/paper-revision
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build online_appendix.tex
```

The script always starts from `git show 9b9bf3c:<file>`. It applies the stages below and prints
a report (`integration/integrate_report.txt` holds the report of the committed run). It stops
with a message on an overlap, a missing anchor, a boundary line whose text the fragment drops,
an edit whose count differs from its expected count, a placeholder without a value, a duplicate
label or tag, or a reference to an undefined label. It has no assertions.

1. Drafted fragments, by declared range or anchor, bottom-up.
2. Integrator edits X1 to X17 (Section 4), each with an expected count.
3. `\NUM{...}` substitution from `reconciliation.csv`, with the display rule of the numerical
   contract's `paper/quantity_manifest.csv` (`decimal_6` with round-half-even, `exact_input`).
4. Bibliography records from `drafts/F_bibitems.tex`, at their author-date positions.
5. Checks, then the write and the copy of the regenerated tables.

Integrator text that is longer than one edit is in `integration/`:
`I01_oa_c9_exercise.tex` (new C.9), `I02_oa_c0_noise_declaration.tex` (C.0 declaration for C.9),
and `I03_oa_c6c_events.tex` (C.6c from the validated contract).

The script also reads the numerical worktree `/home/uctpiaj/work/Projects/ccc-revision-numerics`
(branch `revision/alex-2026-10-21`; validated commit `9faf2d7`, report commit `d28acdc`):
`paper/quantity_manifest.csv` for the display rules, `numerics/quantity_registry.csv` for the
cross-check of each value, and `tables/*.tex` for the copied tables. A rerun needs that worktree
at the same state.

## 3. Fragments applied

All prose versions were used for A and B. Every header anchor matched the base text, with the
two exceptions in Section 5 (C9, C10). The anchored fragments M1_02, M1_03, M1_04 went to the
anchor comments of A06 and A07; the text between the M1_03 anchors matched base lines 337–340.

### main.tex (36 blocks and 3 anchored fragments; 2638 to 3421 lines)

| Fragment | Operation | Base lines |
|---|---|---|
| A01 | replace | 155–156 |
| A02 | replace | 158–177 |
| M1_01 | insert, new paragraph | after 177 |
| A03 | replace | 192 |
| A04 | replace | 197 |
| A05 | replace | 203 |
| M1_07 | insert, end of paragraph | after 205 |
| A06 (with M1_03 and M1_02 at its anchors) | replace | 264–384 |
| A07 (with M1_04 at its anchor) | replace | 386–564 |
| A08 | replace | 566–686 |
| A09 | replace | 691–693 |
| A10 | replace | 729–740 |
| B01 (2 blocks) | replace | 828–841, 858–860 |
| M2_01 | replace | 862–871 |
| A11 | replace | 873–884 |
| M2_02 | replace | 899–920 |
| M2_03 (2 blocks) | replace | 937–940, 1060–1069 |
| M1_05 | insert, new paragraph | after 956 |
| M1_06 | insert, end of paragraph | after 1081 |
| M2_04 | replace | 1094–1102 |
| A12 | replace | 1254–1397 |
| A13 | replace | 1399–1660 |
| A14 | replace | 1666 |
| B02 | replace | 1815–1880 |
| M2_05 | replace | 1882–1924 |
| A15 | replace | 1925–1948 |
| M2_06 (2 blocks) | replace | 2000–2017, 2043–2047 |
| M2_07 | replace | 2231–2236 |
| M2_08 (4 blocks) | replace | 2336–2465, 2466–2512, 2527–2536, 2564–2583 |
| M2_09 | replace | 2585–2636 |

### online_appendix.tex (50 blocks; 3703 to 3912 lines)

| Fragment | Operation | Base lines |
|---|---|---|
| B05 | insert, new paragraph | after 186 |
| M2_20 (21 blocks) | replace or delete | 206–208, 222–233, 297–299, 379, 490–492, 511–515, 622–627, 663, 683–687, 787–792, 798–803, 813–820, 1827–1832, 2107–2113, 2118–2134, 2294–2295, 2386–2390, 2497–2505, 2583–2596, 2643–2649, 3482 (deleted) |
| B03 | insert, new paragraph | after 707 |
| M2_10 | replace | 749–770 |
| M2_11 (2 blocks) | replace | 851–866, 896–902 |
| M2_12 (3 blocks) | replace | 1111–1117, 1139–1146, 1163–1168 |
| M2_13 (2 blocks) | replace | 1264–1271, 1281–1299 |
| M2_14 | replace | 1357–1609 |
| M1_08 | insert, new paragraph | before 1611 |
| M2_15 (6 blocks) | replace | 1875–1885, 1891–1898, 1904–1912, 1943–1961, 1963–1977, 2058–2066 |
| B04 | replace | 2625–2632 |
| M2_16 (5 blocks) | replace | 2700–2739, 2741–2747, 2749–2754, 2758–2777, 2900–2921 |
| M2_17 | replace | 2956–3036 |
| M2_18 (body from I03) | replace | 3038–3083 |
| M2_19 (3 blocks) | replace | 3187–3198, 3202–3216, 3218–3223 |

### Bibliography

- `main.tex`: 16 records from `F_bibitems.tex` at their author-date positions. The existing
  30 records keep their order. Every `\citeproc` key has a record.
- `online_appendix.tex`: the record `ref-EdmansGoldsteinJiang2015`, after
  `ref-DowGoldsteinGuembel2017`. M1_08 cites it there.
- Records with no citation in `main.tex`: `ref-Edmans2009`, `ref-KotzKozubowskiPodgorski2001`,
  `ref-Krishna2010`, `ref-Vickrey1961`, `ref-Ye2007`. They stay as inserted (review point R1).

## 4. Integrator edits

### Cross-cutting fixes that the brief requested

| Id | Where | Change |
|---|---|---|
| X1a | Abstract | "high-value challenger ownership increase" becomes "Challenger participation rises, and so does the probability that a challenger from the high-value class acquires the target." |
| X1b | Section 2.1 | "The benchmark ... gives the investor perfect information" becomes "The model ... gives the investor exact knowledge of the challenger's quality class, though not of its value". |
| X1c, X1d | Introduction, Section 5.3 | "a low-value challenger" becomes "the low-value class"; "A high-value challenger" becomes "A challenger from the high-value class". The benchmark passages (Sections 4.2, 6.2, 6.3, Appendices A.3 and A.7) keep "high-value". |
| X2 | Both files | Conditions (A2), (A3) are retagged (A1), (A2). Labels `eq:paper-a2`, `eq:paper-a3` stay. Main-text mentions use `\eqref`. Literal mentions in the Online Appendix: (A2) to (A1) twice, (A3) to (A2) twice. No "(A1)" or `eq:paper-a1` remained before the retag. |
| X3a–h | Proposition 3, (13), Appendix A.3, Online Appendix B.4 | Certificate index j becomes i: `v_i`, `r_i`, `E_i`, `v_{i,-}`, `v_{i,+}`, mesh `s_i=i/n`, `\min_i`, `\Delta_T(r_i)`. The index i is used nowhere else in these passages. |
| X4a–c | Appendix A.6, (A.39) | Allocation values `W_0(R)`, `W_theta(R)` become `\mathcal V_0(R)`, `\mathcal V_theta(R)`. `\mathcal V` is unused elsewhere. |
| X5a | Section 3.3 (M1_04) | "Each gain is positive" becomes: each gain is nonnegative; both gains are strictly positive when both class supports lie above the reserve, as in the benchmark. (With supports above p, t_j − t_0 > 0 for every continuous F: either F(p) > 0, or 1 − F(u) > 0 just above p.) |
| X5b | Section 6.1 (M1_05) | The same condition, stated for the benchmark, before "t_H > t_0 and t_L > t_0". |
| X6 | Proof of Proposition A.5 (B02) | Part (iii): "Δ_T(r_2) ≥ Δ_T(r_1) by Proposition 1(b), so the strict order bound of (A2) holds at r_2 with no separate condition." The prose version of B02 had already removed "its stated order condition"; this edit names the source, as A00_NOTES asks. |
| X9m, I01 | Online Appendix C.9 | New subsection "Gross trade profits, stake bounds, and additional noise laws", transcribed from the validated contract. The contract's `\Delta R_T` is written `\Delta\mathcal R_T`, the symbol of (A.41) for the same object. It points to A.12 for the stake bounds. |
| (M2_17) | Online Appendix C.6b | Retired as drafted by M2; number and label kept. |

### Reconciliation with the validated numerical contract (C-items in Section 5)

| Id | Where | Change |
|---|---|---|
| X8a–c | (A.24), Appendix A.8 | Low atomless component on [0, 2ε_C], condition 2ε_C < B_{r_1}(m); A.8 states the declared law (uniform on [0, 2ε_C] and on [c_H − ε_C, c_H + ε_C]). |
| X8d–g | Online Appendix A.6, C.1, (OA.77) remark, C.0 | The same law; C.1 inputs and the C.0 benchmark declaration (`low_cost_uniform_support = [0, 0.2]`, `value_band_halfwidth` on its own line) from the contract; the atomless low margin reads B_{r_1}(m) − 2ε_C. |
| X9a | C.0 controls | Tie rule as in the contract: "lower plateau enters at B(m) = c_L" (c_L = 0 in the declarations). |
| X9b, X9c | C.0 controls paragraph | Two contract sentences added: C.6b is retired; a zero-spread constant-price node gets the prior on the full preimage. |
| X9d, I02 | C.0 | New declaration "additional noise laws in C.9". The contract's density sech(z/b)/(πb) is stated up to its constant, and the Student scale is unnamed, because π is the prior and s an order magnitude here. |
| X9e–g | C.6 event grid and data dictionary | The floor endpoint is p_L = h for binary values and p_L = h + ε_V for uniform classes; the endpoint also carries the three offsets above it. |
| X9h | C.6 coverage | Contract sentences on the bounded refinement of interior pure candidates. |
| X9i–l | C.8 | Family table rows for C.9 replace M2_19's "Reserve-event endpoints" row; the phrase on event keys is removed; the C.6b keys are withdrawn, not left unresolved; "C.1 to C.7 and C.9". |
| X9n, X9o | E.1 | `c9_revision.py` joins the run list; one sentence names the release gate of this version (`numerics/release_checks.py`), as in NUMERICS.md. |
| X10 | Appendix A.7 (M2_08) | "Offsets ... run only below h" becomes "Offsets below this event lie inside the domain ...". The event ledger has offsets above the endpoint. |

### Other consistency and clarity edits

| Id | Where | Change |
|---|---|---|
| X7 | Section 2.3 (M1_03) | "the least dispersed law ... the most informative price" becomes "among laws with median zero it has the thinnest tails, and at every pure order profile it gives the most informative flow experiment (Section 5.1)", the conditions of B01 and the Online Appendix lemma. |
| X11a, X11b | Lemma OA.2 and its proof | μ₋, μ₊, ω become m(π), M(π), κ(π) (the M2_20 integrator note). The objects are equal; ω is now the stake of A.12. |
| X12 | Online Appendix A.6 (B03) | The lemma heading is a run-in heading with the same label. As a subsubsection it would put the rest of A.6 under the lemma's heading. |
| X13 | Appendix A.7, A.8 | Tags (A.50)–(A.57) become (A.45)–(A.52), so no gap remains after the removal of (A.45)–(A.49). Labels stay; all references use `\eqref`. No literal reference to these tags exists in either file. |
| X14a–h | Online Appendix A.12 (M1_08) | `G_H(q)`, `G_L(q)` become `\bar A_H(q)`, `\bar A_L(q)` (G_j is the class value cdf); the entry set D becomes `\mathcal X_\tau` (D(u) is G_L − G_H); "w_H > w_L ≥ 0, with w_H > 0 when Δ_T > 0" becomes "w_H ≥ w_L ≥ 0, with w_H > w_L when Δ_T > 0", and "Since w_H > w_L" becomes "Since w_H ≥ w_L ≥ 0". |
| X14i | Online Appendix A.12 | The eight displays carry tags (OA.57)–(OA.64), the numbers that A.11 released. The labels `eq:oa-oa-57` to `eq:oa-oa-64` are reused; no reference to the removed A.11 equations survives in either file. |
| X15 | Section 5.1 (B01) | "its log odds" becomes "the Laplace log odds" (no antecedent after the paragraph break). |
| X16 | Appendix A.7 (M2_08) | "A prepared low-value challenger ... pays max{p, min(R, ℓ)}" becomes "With a prepared low-value challenger ..., the target receives max{p, min(R, ℓ)}". The inequality concerns proceeds. |
| X17 | Section 2.3 (M1_03) | m(π), M(π) get a pointer to Section 3.2, where (7) defines them. |

No edit changes a proposition's mathematics. X5a, X14g, and X14h correct a sign statement to its
weak form with the stated condition for strictness; X16 corrects a wording error. All are recorded above.

## 5. Conflicts and their resolution

| Id | Conflict | Resolution |
|---|---|---|
| C1 | M1_02, M1_03, M1_04 target lines inside A06 and A07. | Placed at the anchor comments; the anchored text matched the base. |
| C2 | M1_01 inserts after line 177, the last line of A02. | Applied as an insert after the A02 range. |
| C3 | M2_18 (C.6c) was drafted before the numerical run and disagrees with the validated contract and the event ledger (class endpoint h + ε_V; offsets above the endpoint; the node 6.280 kept as "an earlier sweep's sampled maximum"). | Superseded by `integration/I03_oa_c6c_events.tex`, from the contract; M2_18 wording kept for the p_H criteria and outputs. |
| C4 | M2 states the low atomless support as [0, ε_C]; the contract and the C.1 manifest use [0, 2ε_C] with ε_C = 0.1. | X8a–g. |
| C5 | M2_16 and M2_08 say that no offset above h is evaluated; the event ledger has `offset:floor_equality_p_L+...` nodes. | X9f, X10. |
| C6 | M2_19 adds a "Reserve-event endpoints" registry family; the registry has no event keys, and it has two new C.9 families. | X9i–k. |
| C7 | M2_15 uses the key `cost_low_support` and one long line; the contract uses `low_cost_uniform_support` and two lines. M2_15 rewrites the tie rule. | X8g, X9a (contract wording). |
| C8 | The contract adds sentences to C.0, C.6, and E.1 that no fragment carries. | X9b, X9c, X9h, X9n, X9o. |
| C9 | M2_20 blocks 4 and 12 end mid-line and drop the rest of base lines 492 ("For a correctly signed order of") and 1832 ("Entry is enclosed by evaluating the exact tail formula"). The script's boundary check found both. | The dropped words are restored in the fragment text before parsing (logged as "repaired"). |
| C10 | M2_20 block 18 quotes "When the intervals are nonempty choose", but "When" ends line 2582. | Documented quote correction; the range and body start at line 2583. |
| C11 | B01 kept one sentence commented out until the C.9 values existed. | Activated, with the qualifier "with full orders held fixed" and a pointer to C.9, because the contract calls these fixed-profile calculations. |
| C12 | `reserve_event_sampled_weak_max` (M2_18): by the M2 definition it would be 10, which is already the endpoint event p_L = h. | Not substituted; C.6c keeps the contract's declared node 6.280 (event id `published_sampled_weak_reserve_6.280`). |
| C13 | `atomless_low_upper` has no reconciliation row. | Not used. The text writes [0, 2ε_C]; the C.0 declaration line copies the contract's literal `[0, 0.2]` (also in `numerics/manifests/c1_baseline.json`, `atomless_cost_supports.low`). |
| C14 | Parameter vectors (A.50)–(A.52): M2_09 drops the c_L slot; the contract and the quantity manifest keep `c_L = 0` as a key. | The manuscript follows M2_09 and the brief's notation sheet (c_L no longer appears; "the preparation cost is 0 with probability ρ and c_H otherwise"). The C.0 declarations keep `c_L = 0` as a schema key. |

## 6. Number substitutions

| Placeholder | Where | Reconciliation name | Stored value | Display | Printed |
|---|---|---|---|---|---:|
| `entry_hypsec_r1` | Section 5.1 (B01) | `sech_entry_strong` | 0.3766056093539899 | decimal_6 | 0.376606 |
| `entry_t3_r1` | Section 5.1 (B01) | `student_t3_entry_strong` | 0.3749945168160299 | decimal_6 | 0.374995 |
| `atomless_entry_strong_laplace` | Section 5.1 (M2_01) | `cost_mix_laplace_entry_strong` | 0.5227147163813063 | decimal_6 | 0.522715 |
| `atomless_entry_strong_logistic` | Section 5.1 (M2_01) | `cost_mix_logistic_entry_strong` | 0.30137412771940725 | decimal_6 | 0.301374 |
| `Pi_acc` | Section 6.1 (M1_05), C.9 | `Pi_acc` | 0.1407312272830394 | decimal_6 | 0.140731 |
| `breakeven_scale` | Section 6.1 (M1_05) | `break_even_trade_scale` | 1.831922571404858 | decimal_6 | 1.831923 |
| `atomless_epsilon_C` | Appendix A.8, C.0 | `cost_halfwidth` | 0.1 | exact_input | 0.1 |
| `Omega_U` | A.12 (M1_08), C.9 | `Omega_U` | 0.011433647948640045 | decimal_6 | 0.011434 |
| `Omega_0` | A.12 (M1_08), C.9 | `Omega_0` | 0.04309764309764388 | decimal_6 | 0.043098 |
| `Pi_hid` | C.9 | `Pi_hid` | 0.06910405796503649 | decimal_6 | 0.069104 |
| `Delta_R_T` | C.9 | `Delta_R_T` | 0.25780871176130704 | decimal_6 | 0.257809 |
| `break_even_trade_scale` | C.9 | `break_even_trade_scale` | 1.831922571404858 | decimal_6 | 1.831923 |
| `sech_entry_strong` | C.9 | `sech_entry_strong` | 0.3766056093539899 | decimal_6 | 0.376606 |
| `student_t3_entry_strong` | C.9 | `student_t3_entry_strong` | 0.3749945168160299 | decimal_6 | 0.374995 |

Sources: `numerics/revision_quantities.csv` (C.9, new rows), `tables/equilibrium_controls.csv`
(atomless entry, unchanged), input manifest (`cost_halfwidth`). Every value agrees with the
validated registry `numerics/quantity_registry.csv` of the numerical worktree. No `\NUM` remains.

`breakeven_scale` maps to the W5 ratio that M1_00_NOTES asks for: ΔR_T/Π_acc = 0.257809/0.140731,
the comparison with an economy without the informed investor (that economy has entry ρ, as the
price-hidden one). It is not the access-alone ratio ΔR_T/(Π_acc − Π_hid).

### Displayed numbers that NUMERICS.md lists as changed

- Low-cost inputs 1, 0.3, 1: the main-text vectors drop the slot (C14); the C.0 declarations
  print `c_L = 0`; the regenerated table notes print 0.
- Low-cost margins 1.366179, 0.196530, 0.773430 (now 2.366179, 0.496530, 1.773430): they appear
  only in generated tables (Table 2 note, the margins table, the reserve-details table), which
  are copied.
- Table 2, Panel C surplus levels (now 2.632301 and 2.552083): generated table, copied.
- Binary floor event 6.281718 (now p_L = h = 10): Appendix A.7 (M2_08), C.6, C.6c, and the
  exploratory table.
- Removed with the price-pool family: 0.272979, 0.303265, 0.151805, 0.125000, 0.687364, 0.609643.
- A text search of both files found no other changed value.

### Tables

The six changed tables were copied from the numerical worktree. Their SHA-256 values match the
reconciliation rows: `table2_equilibrium_controls.tex`, `table_extensions_margins.tex`,
`table_matched_price.tex`, `table_reserve_details.tex`, `table_reserve_exploratory.tex`,
`table_signal_grid.tex`. The other three tables are byte-identical to the worktree copies.

## 7. Labels and tags

| File | Removed | Added | Reused with new content |
|---|---|---|---|
| `main.tex` | `eq:paper-a1`, `eq:paper-a-45` to `eq:paper-a-49`, `price-pooling-at-fixed-orders`, `result-proposition-a-10` | `more-than-two-classes`, `the-price-experiment-at-fixed-orders` | — |
| `online_appendix.tex` | `result-proposition-oa-3` | `oa-a-quality-class-scope`, `oa-a-laplace-extreme`, `result-lemma-oa-laplace-extreme`, `oa-a-stake`, `oa-c-revision` | `eq:oa-oa-57` to `eq:oa-oa-64` (A.12 displays) |

- Tags in `main.tex` run (A.1)–(A.52) without a gap; conditions are (A1), (A2).
- Label and tag now differ in name: `eq:paper-a2` shows (A1), `eq:paper-a3` shows (A2), and
  `eq:paper-a-50` to `eq:paper-a-57` show (A.45) to (A.52).
- Tags in `online_appendix.tex` run (OA.1)–(OA.79) without a gap.
- Subsection numbers do not move: A.11 is a short note, A.12 is new, C.6b is a retirement note,
  C.9 is new.

## 8. Open review points for the next phase

### From A_PROSE_NOTES (no prose file changed them)

- R2 (A15): the many-class price-sufficiency proof compresses the step from a constant
  likelihood ratio to "the posterior is a measurable function of T_X"; the level-set argument
  is absent.
- R3 (A15): the two-group result gives sufficient conditions only; the appendix does not show
  that they hold on a nonempty set.
- R4 (A08): "any low cost below B_F(m(π)) in every economy compared gives the same orders,
  prices, and entry" rests on a sketch (posterior floor and monotone B) with no proof pointer.
- R5 (A13): the general-prior no-trade condition e(π)Δ_T max{π, 1 − π} ≤ k; the drafter checked
  it by script at π = 0.3 and 0.7. The residual computation for π ≠ 1/2 may need to be written out.
- The index clash near Proposition 3 (A_PROSE_NOTES point 5) is resolved (X3).

### From A00_NOTES, Section 5 (steps not fully verified)

- R6: Proposition 1(c) states the iff as "D ≥ 0 above p and D(p⁻) ≤ 0" and equates it with the
  two restrictions only without atoms at p. Check the proof of part (c).
- R7: the F-free split identity needs equal admissibility or F(p) = 0 (SYNTHESIS row 2).
- R8: condition (R) of Claim 10 is folded into Step 1 of the proof of Proposition 2.
- R9: "unconditional" price sufficiency means the entry floor; the inversion still needs Δ_T > 0.
- R10: selective-entry sentences (A05) rest on working-paper versions of Gentry and Li (2014)
  and Marmer et al. (2013), and Samuelson's assumption comes through Levin and Smith (1994,
  footnote 7). The citation check verified the published records, not those passages.
- R11: the slack-low-cost sentence (same as R4) and the general-prior no-trade condition (R5).

### From B_PROSE_NOTES

- Points 1, 2, 3, 4, and 6 were resolved by B00 "Fix round 1" (Euler product without the circle
  constant; median zero stated in B01 and B03; price-construction paragraph in B03; Proposition 2
  part (iii) named in B02; Lebesgue measure and continuity in B02 and B03). The integrated text
  confirms each. X6 and X7 align the neighbouring text.
- R12 (point 5): the joint nonemptiness and ownership construction in B02 is now six explicit
  steps. It needs a proof check, especially the continuity of both conditional entry
  probabilities at the chosen threshold.

### From M1_00_NOTES and M2_00_NOTES

- R13: "trades lawfully" (M1_02) rests on United States law only.
- R14: Kyle and Vila (1991), Maug (1998), Back et al. (2018), Acharya and Johnson (2010), and
  Meulbroek (1992) rest on abstracts; the text keeps each claim at mechanism level.
- R15: the transfer split in Section 6.1 is stated in words only; the screening-region surplus
  clause is omitted; exact stake cutoffs stay open (A.12).
- R16: the fixed-orders argument in Appendix A.7 and C.6 uses the two-point cost law; do not
  widen it to atomless costs at reserves with zero gross profit.
- R17: the schema names `c_L`, `zeta_L`, `low_cost_margin`, `low_cost_floor_*`, and the `pool_*`
  columns keep old names with new definitions (numerical contract decision).

### Found during integration

- R1: five bibliography records have no citation (Section 3). Natural homes: Kotz et al. (2001)
  for the Gaussian-with-exponential-variance representation in Section 2.3, and Edmans (2009)
  in the blockholder sentence of the introduction. Otherwise delete them.
- R18: duplicated content. Section 2.3 (M1_03) and Section 5.1 (B01) both state the clipped log
  odds and the failure of Gaussian noise; M1_03 and M1_02 both state the exponential-difference
  construction of Laplace noise.
- R19: Lemma OA.2 (general prior) is now a special case of Proposition 2, which holds at every
  prior. Consider removal.
- R20: Section 6.3 introduces the value classes again, although Section 5.2 now presents them as
  the running example; a back-reference would shorten it.
- R21: the introduction's class condition ("stochastically higher values in the high class")
  omits that the classes must differ above the reserve (Γ > 0), which Proposition 2's
  nonemptiness clause requires.
- R22: Online Appendix A.6 lemma uses ℓ_b for the Laplace density (ℓ is the low value) and
  e_r, P_r (A07 dropped the r subscript).
- R23: the A.11 note refers to "the reserve example that the earlier construction used", which a
  reader of this version cannot see.

## 9. Not resolved

- U1: generated table notes contradict the revised text. They need a change in the numerical
  renderer, not a hand edit:
  - Table 2 note: "The five strict margins of Proposition 2 ... ζ_L = 2.37 × 10⁰ ...". ζ_L is no
    longer a hypothesis of Proposition 2, which has four strict conditions.
  - Table 3 note (unchanged file): "all five margins strictly positive".
  - `table_extensions_margins.tex`: "five strict sufficient inequalities ... (low cost, ...)",
    and parameter vectors with a c_L slot.
  - `table_signal_grid.tex`: "the smallest of the five conditions in (OA.29)"; (OA.29) now has four.
  - `table_reserve_details.tex`: "Floor margin is B_r(m) − c_L".
  - Table 1 note: "across challenger types" (class wording).
- U2: Section 6.2, (14), Proposition A.8, Online Appendix A.8 and C.7, and the Figure 4 labels
  write challenger profit under bargaining as G_{θ,η} (G_{H,η}, G_{L,η}). This collides with the
  class value cdf G_j. Figure 4 is byte-identical pipeline output, so a rename needs a new render.
- U3: Appendices A.6–A.7 and Online Appendix A.1–A.7, B, and C still index class objects by θ
  (t_θ, e_θ, μ_θ, F_θ, U_θ). A00_NOTES recommends j. The change touches many lines outside the
  drafted regions and was not part of the task list.
- U4: `talk.tex` and `script.tex` in the clone still use c_L and the old tags (A1)–(A3). They
  were not edited.

## 10. Verification

- The script run in `integration/integrate_report.txt` shows every anchor match, every edit
  count, every substitution with its source, the bibliography order, and the checks.
- Both documents were built from a clean `build/`. The PDFs were read in full text for the
  introduction, Sections 2 to 8, the appendix boundaries, and the changed Online Appendix
  sections (scope note, A.6, A.11, A.12, C.0, C.1, C.6, C.6b, C.6c, C.8, C.9, E.1).
- The base commit was built separately for the page counts and the underfull comparison.
- No test was written or run.

---

# Round 2: fixes from the four reviews (21 October 2026)

## R2.1 Result

- Commit `14736739078ce8c005edea7daab9755923a713c8` on branch `revision-alex-2026-10-21` of
  `overleaf/paper-revision`, on top of `ac4e37e`. Nothing is pushed. `overleaf/paper/` is not
  touched. No PDF is committed.
- The commit changes `main.tex`, `online_appendix.tex`, seven tables, and Figure 4
  (`figures/bargaining_weight.pdf`).
- Both documents compile from a clean `build/` with
  `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build <file>`.

| Document | Round 1 pages | Round 2 pages | Errors | LaTeX warnings | Undefined refs or citations | Overfull boxes | Underfull boxes |
|---|---:|---:|---:|---:|---:|---:|---:|
| `main.tex` | 90 | 92 | 0 | 0 | 0 | 0 | 0 |
| `online_appendix.tex` | 59 | 61 | 0 | 0 | 0 | 0 | 5 |

The five underfull boxes are the same five as in the base and round-1 builds (C.2 file name,
three in the generated `table_reserve_details.tex` note, C.6 data dictionary). No log has a
multiply defined label or a rerun request.

Page positions in `main.pdf`: body pages 2-44 (round 1: 2-42), references 45-51, Appendix A
pages 52-92 (round 1: 50-90). The body grew because of the requested additions (maintained
restriction, Proposition 1(c) pointer, floor, worst-case reading, entry range, shareholder
paragraph). The two moves offset the new proofs in Appendix A, which keeps its length. Line
spacing is unchanged.

## R2.2 How to rebuild

```sh
cd /home/uctpiaj/work/Projects/competition-creates-competition
.venv/bin/python audit/revision_v2_2026_10_21/scripts/round2.py --check  # checks only
.venv/bin/python audit/revision_v2_2026_10_21/scripts/round2.py          # writes the clone
```

`round2.py` starts from `git show ac4e37e:<file>`. It applies the edits in
`round2_edits_main.py` and `round2_edits_oa.py` (each an exact replacement with an expected
count, a block between two unique anchors, or replacements scoped to a region), then the two
moves, then the retag and the label renames, then the checks (labels, references, tag
sequences, citations against records, leftover notation), and then it copies the tables and
the figures after a hash check against `round2_artifacts.csv`. It stops on any mismatch and
writes nothing before every step passes. It has no assertions. The report of the committed
run is `integration/round2_report.txt`. Each edit note names the review items it serves.

## R2.3 Artifacts

| File | SHA-256 (first 16) | Action |
|---|---|---|
| `tables/table1_auction_primitives.tex` | `ebeade4fb8bd1168` | copied; matches round2_artifacts.csv |
| `tables/table2_equilibrium_controls.tex` | `533ef7e15f77f4f7` | copied; matches |
| `tables/table3_extensions.tex` | `323bfed91e995a32` | copied; matches |
| `tables/table4_reserve_comparisons.tex` | `c5128fb2f6d2bd80` | copied; matches |
| `tables/table_extensions_margins.tex` | `cb53d3547cbce8dc` | copied; matches |
| `tables/table_reserve_details.tex` | `fcee1a14685b35eb` | copied; matches |
| `tables/table_signal_grid.tex` | `a183760be4469567` | copied; matches |
| `tables/table_matched_price.tex`, `tables/table_reserve_exploratory.tex` | unchanged | byte-identical to the worktree |
| `figures/bargaining_weight.pdf` | `e981d3f27d785890` | copied; matches; labels `g_{θ,η}`, `g_{H,η}`, `g_{L,η}` |
| `figures/equilibrium_correspondence.pdf`, `posterior_tail_entry.pdf`, `two_returns.pdf` | unchanged | byte-identical to the worktree |

The worktree also holds a new `tables/table_class_exhibit.tex`. It is the class exhibit of a
later round. It was not copied, and no text refers to it.

## R2.4 Choices between reviews

| Problem | Reviews | Choice and reason |
|---|---|---|
| Independence sentence (Section 2.2) | M2, P-S2 | M2: the pair (j, theta) as one joint object, as in the Online Appendix price construction. P-S2's "depends on the class only through G_j" is less exact. |
| Atomless-cost windows | M1, C3b | Same correction. Written for general F0, F1 (r0, r1 for uniform incumbents), as Proposition 2 and the corrected Proposition A.5 are. The proof does not use uniformity. |
| Welfare proceeds gain | M3, C3a | M3: it also corrects the allocation increment and the reserve term, and adds the strictness step. |
| Retired pooling example (A.11, C.6b) | M12, C4, P-S12 | M12: "prescribes zero preparation at a pooled price violates the zero-cost buyer's optimality condition and the tie rule" also covers zero gross profit. C4's "with positive gross profit" omits that case. |
| Duplicated noise argument | M9, C12, P-S3, F9 | P-S3, as the round's decision 6 asks. Kept "mean b" so the scale of (2) stays pinned; added the median-zero qualifier (F15); made the exponential variance the stated condition in the Kotz et al. sentence; kept the economic Gaussian sentence once, in Section 5.1. |
| Lemma OA.2 | M10, C14, P-M15 | C14: delete the lemma and renumber, so the extremality lemma used by Section 5.1 is Lemma OA.1 and the quadratic-cost lemma is Lemma OA.2. Labels unchanged. M10's replacement sentences are not used (C39 calls such sentences meta text). |
| Value classes in 5.2 and 6.3 | C13, P-S10, F-report minor 7 | P-S10 for Section 5.2; C13 and P-S10 merged for Section 6.3. |
| Bargaining-profit symbol | C1 (g_eta(theta)), M11, D3 | D3: g_{theta,eta}, g_{H,eta}, g_{L,eta}, the regenerated Figure 4 labels. |
| Price-sufficiency topic sentence | C42, F13 | F13: keeps "in every candidate equilibrium" and adds Delta_T > 0. |
| Dividend sentence | C44, P-S13 | C44: splits the sentence and keeps all three facts. |
| Table-note texts | C2, M7 | The numerics member regenerated the notes in round 2; their wording is authoritative. In C.1 the text keeps the atomless low margin strict (M7), which C2's "zeta_L needs no strict sign" would miss. |
| Introduction class condition | M8, C11, P-S5, F14, D5 | One sentence in words: classes that differ above the reserve, stochastically higher values in the high class, both supports above the reserve (the new maintained restriction). |
| Uncited records | C18, F18, P-S7, D8 | Edmans (2009) and Kotz et al. (2001) cited where C18 proposes. Vickrey (1961) and Krishna (2010, Section 2.2) cited at the truthful-bidding sentence (P-S7): Vickrey was checked for content and the Krishna section title was checked (Q1_N_main.md). Ye (2007) removed: only its abstract was verified (LIT_extracts.md, B9). |

## R2.5 R_math.md (1 blocking, 7 should fix, 4 minor)

| Item | Action | Edits | Note |
|---|---|---|---|
| 1 (blocking) Proposition A.6 at a general prior | applied | m78, m79, o35 | (A.24) and (OA.26) use m(pi), pi, M(pi). The statement retains the class assumptions and (A2), states the exact ownership condition e_H W_H(F1) > rho W_H(F0), and says it holds when W_H = 1. The proof is written in full: zero-cost floor from the first line, e(pi) = rho from both lines, e = 1 near M(pi), ownership from conditional independence, e_H > rho. The sufficient condition (1+rho)W_H(F1) >= 2 rho W_H(F0) is not carried over: it rests on the Laplace entry set for cost atoms. |
| 2 Independence | applied | m13 | |
| 3 Welfare proof | applied | m95, o42a, o56 | (A.39) for every value; (A.40) with pF1(p)[1 - G_L(p-)]; (A.41) with prior weights; strictness step; A.5 and A.6 cases; Online Appendix A.9 labeled as the benchmark computation; C.9 says "(A.41) at pi = 1/2". |
| 4 Benchmark scope statements | applied | m43, m82, m87, m91, m96 | Section 5.3, Appendix A.5, Proposition A.7, Appendix A.6 (bargaining), Appendix A.7. |
| 5 Online Appendix auction proof | applied | o13, o43b, o05, o12 | R_math's text for lines 444-464, with tag (OA.6) on the new display. Kernel bound: "at most max{p, R}, bounded on the incumbent's support" (the Online Appendix uses R ~ U[0, r]). |
| 6 Level-set step (many classes) | applied | v04 | Written in full in Online Appendix A.13; states that it uses the Laplace law and b > 1. |
| 7 Table notes | applied | renderer (numerics round 2), o48 | Tables copied. C.1 text: four strict margins for cost atoms, five for the atomless mixture. |
| 8 Introduction class gap | applied | m04b | See R2.4. |
| 9 Noise repetition | applied differently | m15, m36, m17b | P-S3 merge (decision 6). |
| 10 Lemma OA.2 | applied differently | o39, o37a, o37b, o31 | Removed as C14 proposes. |
| 11 G collision | applied | m48, m93, o41, o55, o55b | g_{theta,eta}; C.7 states that the schema columns G_H_eta, G_L_eta hold g_{H,eta}, g_{L,eta}. |
| 12 Retired example | applied | o44, o53 | |

## R2.6 R_consistency.md (4 blocking, 14 should fix, 26 minor)

| Item | Action | Edits | Note |
|---|---|---|---|
| 1 (blocking) Letter G | applied differently | m48, m93, o41, o43a, o55, o55b | g_{theta,eta} (D3) instead of g_eta(theta); g(R,v,p) in (OA.50); Figure 4 re-rendered by numerics; CSV column names kept. |
| 2 (blocking) Table notes | applied | renderer (numerics), o48 | |
| 3 (blocking) Equal-prior displays | applied | m95 (a), m78/o35 (b), o34a-d (c), m82 (d) | |
| 4 (blocking) Unseen example in A.11, C.6b | applied differently | o44, o53 | M12 wording (R2.4). |
| 5 Class index theta | applied | m42b-e, m84, m86, m88-m90, m95, m98, m99, m101a-c, o02b, o04, o06-o08, o10, o11, o16, o18, o20b, o23, o25, o40a-c, o40m-n, o42a, o42g-i, o43d-f, o43h-k, o47e-f, o51a-b | Class variable J, class index j. Per-value objects t(theta), g(theta), V_theta keep theta. A.1 draws J with Pr(J=H) = pi, not "equal probabilities", because C10 asks for the general prior there. The dominating function J(z) in (OA.54) is renamed Lambda(z). The C.2 mixed-candidate support index is n. |
| 6 F_j collides with F | applied | m60-m62, m65, m71, m72, m75a-b, o17, o20a, o28, o45d, o46 | bar A_j everywhere, including A.3 and Part B; J_H, J_L removed. A.12 states that its argument is the signed order, while Appendix A.2 of the paper uses the magnitude (bar A_L(s) there equals bar A_L(-s) in A.12). |
| 7 Letter D | applied | m84-m86, m90, o40d-j, o50a | Delta_P in A.5 and Online Appendix A.7; Gamma in C.4. |
| 8 Entry set E_f | applied | m74, m75g-h | X_f. |
| 9 ell_b, e_r, P_r | applied | o30a-b, o33 | f^Lap_b; schedules named as equation (9) of the paper. |
| 10 Scope note | applied | o01-o24, o27, o36a, o38a, o42a, o43l | Items 1-3 deleted. A.1-A.4 and A.6 print the general prior (including (OA.1), (OA.2), the bounds, (OA.16), the weak price, entry, ownership, the logistic formulas, (OA.26), Lemma OA.2 with kappa(pi)). A.5, A.7, A.9, A.10, A.14 state the benchmark prior. |
| 11 Introduction class gap | applied | m04b | |
| 12 Duplicated noise claims | applied differently | m15, m36, m17b | P-S3 (decision 6). |
| 13 Value classes twice | applied | m40, m51 | |
| 14 Lemma OA.2 and lemma numbers | applied | o31, o37a-b, o39 | |
| 15 Tie rule with c_L | applied | o47b | Manuscript listing only; the contract source is listed for numerics (R2.11). |
| 16 Word "type" | applied | m13, m34, m50, v16, o42b, o49, o52b | Investor "type" kept where it means investor information. |
| 17 Proposition A.5 for general F | applied | m74, m75b-d, m75f | Uniform strengths kept in the nonemptiness clause and its proof. |
| 18 Uncited records | applied differently | m09, m14, m15, m55f | See R2.4. |
| 19 Label names | applied | stage 3 | eq:paper-cond-1/2; eq:paper-a-45 to eq:paper-a-50 match tags (A.45)-(A.50). |
| 20 Class C_L | applied | m36, m73, m74, m76, o29 | N_L. |
| 21 Student nu | applied | o47a | Scale 2b/sqrt3. |
| 22 W and Y_n | applied | o32a-c | Z_n and the remainder sum. |
| 23 g(P), g(x) | applied | o14a-b, o42c-d | iota(P), bar f(x). |
| 24 Scalar bar A | applied | m90, o40k-l, o47c-d | A^+. |
| 25 a(q) | applied | o45, o45b-c | alpha(q); (OA.62) set on two lines to avoid a 0.56pt overfull box. |
| 26 C.4 index j | applied | o50a-b | n; CSV column j kept. |
| 27 H_L, H_H | applied | o35, o42e-f | H_C^0, H_C^1. |
| 28 Dummy eta | applied | m59b | delta. |
| 29 T_X, truncation T | applied | v03, o47c-d | bar t_X, bar x. |
| 30 R_max | applied | m47, m92 | bar r. |
| 31 B_p(m) | applied | v12 | Now in Online Appendix A.14. |
| 32 lambda_X | not applied | | Optional in the review. The symbol has one meaning in the paper; a rename touches A.5 and Online Appendix A.7 with no gain in correctness. |
| 33 Four pointers | applied | m09, m45, m103, o57 | |
| 34 epsilon_V typeset | applied | m104 | |
| 35 Two writings of the spread | applied | o43c | |
| 36 Locked conventions | not applied | | The review proposes no change. |
| 37 Nonemptiness disclaimers | applied | m81, o36b | |
| 38 Proof paragraph of A.5 | applied | m75e | |
| 39 Meta sentences | applied | o01, o39 | |
| 40 Bargaining disclaimer | applied | m94 | Kept in the Online Appendix. |
| 41 Two local denials | applied | o38b, o43g | |
| 42 Topic sentences | applied | m15, m23 | The first through P-S3; the second with F13 wording. |
| 43 Section 5.3 sentences | applied | m43 | |
| 44 Three long sentences | applied | m16, m35, m46 | |

## R2.7 R_prose_latex.md (14 should fix, 16 minor, plus Parts 1 and 4)

| Item | Action | Edits | Note |
|---|---|---|---|
| S1 Abstract | applied | m01 | One sentence added: the investor knows the buyer's quality class (the review's own problem 2). "more accurate private signal" kept from the original wording. |
| S2 Independence | applied differently | m13 | M2 wording (R2.4). |
| S3 Sections 2.3 and 5.1 | applied | m15, m36, m17b | See R2.4. |
| S4 Words | applied | m04a, m13, m22, m25, m27, m29, m32, m38, m42a, m42d, m56, m57, m63, m64, m66-m70, m82, m83, m90, m95, m97, m100, o40o | zero-cost and challenger at the listed loci. Not at Section 7 (line 1376): that section uses "further buyer" for the empirical counterpart throughout. The Figure 2 note follows C16. |
| S5 Introduction sentence | applied | m04b | |
| S6 Entry cost | applied | m06 | |
| S7 Uncited records | applied | m09, m14, m15, m55f | Krishna cited as "Section 2.2", the verified section title, not "Chapter 2". |
| S8 Sequence sentence | applied | m18 | |
| S9 Section 6.1 sentence | applied | m44, m45 | |
| S10 Value classes | applied | m40, m51 | |
| S11 Introduction | applied | m02, m03a-b, m05 | The bounded-score sentence moves to the robustness paragraph (F9). |
| S12 A.11 | applied differently | o44 | M12 wording (R2.4). |
| S13 Defensive framing | applied | m08, m13, m15, m38, m46, m49, m77, m81, o26 | Line 215: sentence split, "abstracts from" kept as a statement of scope. Line 1130: "holds without point masses, at any prior, and for any class gap above the reserve, however small". Line 1269: C44 (R2.4). OA 696: the negative clause removed. |
| S14 Long sentences | applied | m07a-b, m09, m30, m37, m53 | Lines 311-314 superseded by the new restriction paragraph (m12). |
| M1 Journal name | applied | m55a-b | |
| M2 Book place | applied | m55c | Place dropped for Kotz et al., as for Krishna. |
| M3 Working papers | applied | m55d-e | |
| M4 Label names | applied | stage 3 | Same as C19. |
| M5 Blank lines | applied | m02 | |
| M6 One sentence per source line | not applied | | Optional; no effect on the PDF. The rewritten 2.3 and 5.1 are paragraph source. |
| M7 "in the main" | applied | m17c | |
| M8 Conclusion repeat | applied | m54 | |
| M9 Incumbent sentence | applied | m11 | |
| M10 Class names | applied | m12 | "The high class, or high-value class"; benchmark passages keep "high-value". |
| M11 "class-level" | not applied | | Optional in the review. |
| M12 "the" to "a" | applied | m31 | |
| M13 "online" panel | applied | m46 | |
| M14 Scope note | superseded | | C10 applied instead (should fix). |
| M15 Lemma OA.2 | applied | o39 | |
| M16 Table notes | applied | renderer (numerics) | |
| Part 1: underscore preamble fix | not applied | | Optional; the five underfull boxes predate the revision and are not gated. The table note needs a renderer change (R2.11). |
| Part 4: L1, L2 | applied | moves | Decision 6. |
| Part 4: L3, L6-L9, spacing | not applied | | Not requested this round; line spacing unchanged as decided. L4, L5 are S3. |

## R2.8 R_referee.md (ranked fix list 1-25)

| Rank | Action | Edits | Note |
|---|---|---|---|
| 1 Class exhibit | not applied | | Decision: a later round adds it. The one-sentence pointer for many classes is added with the move (m39). |
| 2 Maintained restriction | applied | m12, m19, m20, m21, m24, m26, m30, m41, m52, m58, m59a-d, m80, o01 | Section 2.2 and Proposition 2 state FOSD and G_H(p-) = G_L(p-) = 0. Proposition 1(c) is stated and proved in Appendix A.1 (label result-proposition-1c), with a paragraph that every result also holds under equal admissibility. Section 6.3 sentence added. |
| 3 Worst case and the region between strengths | applied | m28, m33 | Without the referee's numbers (R2.11). |
| 4 Entry range, diagnostics | applied | m04b, m36 | Introduction: 0.522757 (Laplace) and 0.301509 (logistic) against the floor 0.250000. Section 5.1: hyperbolic secant and Student t3 labeled fixed-profile numerical diagnostics; both lie between the two values. |
| 5 Shareholder paragraph; condition of A.9 | applied | m45, m95 | "The gain is real, not a transfer." Expected interim price rises by the same amount. The recruiting condition is stated in Proposition A.9, with a proof that access strictly lowers proceeds when B_F1(m(pi)) < c_H <= B_F1(pi). The referee's "1.83" and "at every admissible order size" are not used: the first is not a registry value, the second rests on a reading of the order unit that the model does not state. |
| 6 Cuts and moves | applied in part | moves | (b) "More than two classes" moved; "Exact reserve events" moved from (a). The rest is a restructure, not requested. |
| 7 Three institutional sentences | applied | m10, m14, m27 | (b) reworded: the board collects its announced walk-away price from a lone prepared bidder whose value meets it. |
| 8 Continuous order interval | not applied | | Its first sentence is false in general: a discrete menu with Gaussian noise has unbounded likelihood ratios. |
| 9 Merge noise text | applied | m02, m04b, m15, m36 | Introduction: the reversal holds for every noise law whose score bound is below one (Proposition A.5); at a given bound, Laplace noise gives the most informative flow experiment at every pure order profile. |
| 10 Condition in A.9 | applied | m95 | |
| 11 Rename bargaining profit | applied | see C1 | |
| 12 Table notes | applied | renderer (numerics) | |
| 13 Two wording fixes | applied | m23, m27 | |
| 14 Introduction class condition | applied | m04b | |
| 15 Median-zero qualifier | applied | m15 | |
| 16 Ownership sentence | not applied | | Needs the numerical verification the referee asks for (R2.11). |
| 17 Abstract ownership clause | not applied | | The rewritten abstract (S1) states the result for a set of parameters on which Proposition 2's ownership condition holds; the sentence is exact as written. |
| 18 Bibliography | applied | m09, m14, m15, m55f | Vickrey cited, Krishna cited, Ye removed. |
| 19 Online Appendix notation | applied | o30a-b, o44, theta renames | |
| 20 Style of 5.1 and the A.5 proof | applied in part | m36, m75e | 5.1 rewritten in paragraphs; one proof paragraph of A.5 rewritten (C38). |
| 21 Proposition A.5 for general F | applied | m74, m75 | |
| 22 Stand-alone Blackwell paragraph | not applied | | One sentence; it is the only main-text statement of the comparison. |
| 23 Legal sentence | applied | m17a | "not from information that either bidder or the target supplies". |
| 24 "Type" for a cost | applied | m13 | |
| 25 Figure 1 note; Proposition A.7 scope | applied in part | m87 | Figure 1 note keeps the explicit prior. |

Report minor comments 1-14 (Part 1 of R_referee.md): 1, 2 (stated in 2.3 with a pointer, in
5.1, and once in the introduction), 3, 7, 11, 12, 14 applied through the items above; 5, 8, 9
already hold in the text; 4, 6, 10, 13 not applied (restructure, registry displays, or
optional).

## R2.9 Renames

| Old | New | Where |
|---|---|---|
| G_{theta,eta}, G_{H,eta}, G_{L,eta} | g_{theta,eta}, g_{H,eta}, g_{L,eta} | (14), A.6, (OA.44), C.7; Figure 4 labels |
| G(R,v,p) | g(R,v,p) | (OA.50) |
| Theta (class variable) | J | (A.30), A.5, A.6 (coupling), Online Appendix A.1, A.4, A.5, A.7, A.9 |
| class subscript theta | j | A.5-A.7 of the paper; Online Appendix A.1, A.3, A.4, A.7, A.9, A.10, C.0, C.2 |
| F_j(s), F_H, F_L, F_theta, F_epsilon | bar A_j(s), bar A_H, bar A_L, bar A_epsilon | A.2, A.3, A.4 of the paper; Online Appendix A.3, A.4, A.5, Part B |
| J_H, J_L, J | bar A_H(1), bar A_L(1) | (A.7), (OA.22) |
| signals D | Delta_P | A.5, Online Appendix A.7 |
| C.4 D, delta_j, j | Gamma, delta_n, n | C.4 |
| E_f | X_f | Proposition A.5 |
| C_L, C_{1/b} | N_L, N_{1/b} | Section 5.1, A.4, Online Appendix A.6 |
| ell_b | f^Lap_b | Online Appendix A.6 |
| e_r, P_r | e, P | Online Appendix A.6 |
| W, Y_n | remainder sum, Z_n | Lemma OA.1 |
| g(P), g(x) | iota(P), bar f(x) | Online Appendix A.3, A.9 |
| bar A (scalar), T (truncation) | A^+, bar x | (A.36), (OA.38), C.0 |
| a(q) | alpha(q) | Online Appendix A.12 |
| H_L, H_H | H_C^0, H_C^1 | Online Appendix A.6, A.9 |
| eta (proof dummy) | delta | proof of Proposition 1(c) |
| T_X | bar t_X | Online Appendix A.13 |
| R_max | bar r | Section 6.2, Proposition A.8 |
| B_p(m) | B_{p,r}(m) | Online Appendix A.14 |
| J(z) (dominating function) | Lambda(z) | (OA.54) |
| q_{theta j}, omega_{theta j} | q_{jn}, omega_{jn} | C.2 |
| eq:paper-a2, eq:paper-a3 | eq:paper-cond-1, eq:paper-cond-2 | labels of (A1), (A2) |
| eq:paper-a-52 to eq:paper-a-57 | eq:paper-a-45 to eq:paper-a-50 | labels match tags |
| Lemma (unnumbered), Lemma OA.1 | Lemma OA.1, Lemma OA.2 | labels unchanged |

## R2.10 Moves, labels, and tags

| Block | From | To | References updated |
|---|---|---|---|
| More than two classes | Appendix A.4 of the paper | Online Appendix A.13 (`oa-a-classes`) | Section 5.2 pointer added; links to Section 2.4, Proposition 2, (A1), (A2) written as references to the paper |
| Exact reserve events | Appendix A.7 of the paper | Online Appendix A.14 (`oa-a-reserve-events`) | A.7 keeps a summary under the same heading and label, with p_L and p_H; the reference to (A.45), (A.46) in A.7 now names p_L and p_H; C.6 and C.6c point to A.14 |

- `main.tex`: removed labels `eq:paper-a2`, `eq:paper-a3`, `eq:paper-a-51` to `eq:paper-a-57`
  (renamed), `more-than-two-classes` (moved); added `eq:paper-cond-1`, `eq:paper-cond-2`,
  `eq:paper-a-45` to `eq:paper-a-49`, `result-proposition-1c`. Tags run (1)-(14), (A1), (A2),
  (A.1)-(A.50) with no gap.
- `online_appendix.tex`: removed `result-lemma-oa-2`; added `oa-a-classes`,
  `oa-a-reserve-events`. Tags run (OA.1)-(OA.79) with no gap. The moved displays are untagged.
- Online Appendix subsections A.1-A.12 keep their numbers; A.13 and A.14 follow A.12, so no
  literal "Online Appendix A.n" reference moves.
- Bibliography: `main.tex` has 45 records and 45 cited keys; the Online Appendix has 2 and 2.

## R2.11 Numbers and items for the numerics member

No number was added that is not already printed in the round-1 text from reconciliation.csv;
a script compared every decimal in the new sources with the round-1 sources and found none new.

1. Referee rank 1: the class exhibit (in progress). `tables/table_class_exhibit.tex` was not
   copied.
2. Referee rank 3 and M1: registry quantities for the benchmark windows, if the text should
   print them: the ratio Delta_T(r0)/Delta_T(r1); the bound (1-1/b) rho kappa(1/2); the upper end
   of the (A2) window (1-1/b) rho kappa(1/2) Delta_T(r1); the (A1) endpoints B_r0(1/2) (already
   registered as 4.804167) and B_r1(M); the range of priors for which the benchmark windows are
   nonempty; windows at priors 0.3 and 0.7.
3. Referee rank 16: the low-cost probability above which entry rises while high-class
   ownership falls on the region of Proposition 2(ii), from point-mass classes and uniform
   incumbents.
4. Referee rank 4 (option): equilibrium status of the hyperbolic-secant and Student t3 rows
   (global bound and (A1) with the attained supremum). The text now labels them fixed-profile
   numerical diagnostics.
5. C15: the contract source of the C.0 continuation controls still reads "lower plateau enters
   at B(m) = c_L"; the manuscript listing now reads "B(m) >= 0".
6. P Part 1: the renderer of `table_reserve_details.tex` can allow line breaks after ";" and
   "=" in the parameter-identity note, which would remove three of the five underfull boxes.
7. The C.7 CSV columns `G_H_eta`, `G_L_eta` keep their schema names; the text maps them to
   g_{H,eta}, g_{L,eta}.

## R2.12 Round-1 open points

- Resolved this round: R1 (uncited records), R2 (level-set step), R4 and R11 (reason for the
  slack low cost), R13 (legal claim), R18 (duplicated noise text), R19 (Lemma OA.2), R20
  (value classes once), R21 (class gap in the introduction), R22 (Online Appendix symbols),
  R23 (unseen example), U1 (table notes, by the numerics member), U2 (bargaining profit), U3
  (class index j).
- Checked by the mathematical review without a change: R3, R5, R6, R7, R8, R9, R12, R16.
- Still open: R10 and R14 (claims from working-paper versions or abstracts stay at mechanism
  level), R15 (exact stake cutoffs), R17 (legacy schema names), U4 (`talk.tex` and `script.tex`
  in the clone still use c_L and the old tags; they were not edited).

## R2.13 Verification

- The script run in `integration/round2_report.txt` shows each edit with its count, both moves,
  the retag, the label renames, the checks, and the artifact hashes.
- Both documents were built from a clean `build/`. The text of the PDFs was read for the
  abstract, Sections 1-8, Propositions 1, 1(c), 2, A.5, A.6, A.9, the A.7 summary, and the
  changed Online Appendix passages (scope note, A.1-A.6, A.9-A.14, C.0, C.1, C.4, C.6b, C.7,
  C.9). The pages with (A.41) and (OA.62) were also checked as images.
- Every remaining "1/2" in both sources was listed with its section; each lies in a passage
  that states the point-mass benchmark, a declared exercise, or a constant that is not a prior.
- No test was written or run.

---

# Round 3: class exhibit and benchmark windows (21 October 2026)

## R3.1 Result

- Commit `f94b10de76f50ca724029e6800623769588ca18b` on branch `revision-alex-2026-10-21` of
  `overleaf/paper-revision`, on top of `1473673`. Nothing is pushed. `overleaf/paper/` is not
  touched. No PDF is committed.
- The commit changes `main.tex` and `online_appendix.tex` and adds
  `tables/table_class_exhibit.tex`. No other table or figure changes.
- Both documents compile from a clean `build/` with
  `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build <file>`.

| Document | Round 2 pages | Round 3 pages | Errors | LaTeX warnings | Undefined refs or citations | Overfull boxes | Underfull boxes |
|---|---:|---:|---:|---:|---:|---:|---:|
| `main.tex` | 92 | 94 | 0 | 0 | 0 | 0 | 0 |
| `online_appendix.tex` | 61 | 63 | 0 | 0 | 0 | 0 | 5 |

The five underfull boxes are the same five as in the earlier builds (C.2 file name, three in
the generated `table_reserve_details.tex` note, C.6 data dictionary). No log has a multiply
defined label or a rerun request. A first build had two overfull lines (47.5pt and 26.8pt)
from the run of output file names in C.10; the file list is now a code block, as in C.3 to C.5.

Page positions in `main.pdf`: body pages 2-46 (round 2: 2-44), references 47-53, Appendix A
pages 54-94. Table 4 (the exhibit) prints on page 36; Tables 3, 4, and 5 print in order on
pages 33, 36, and 43. In `online_appendix.pdf`, C.10 is on pages 54-55.

## R3.2 How to rebuild

```sh
cd /home/uctpiaj/work/Projects/competition-creates-competition
.venv/bin/python audit/revision_v2_2026_10_21/scripts/round3.py --check  # checks only
.venv/bin/python audit/revision_v2_2026_10_21/scripts/round3.py          # writes the clone
```

`round3.py` starts from `git show 1473673:<file>`. It applies each edit as an exact
replacement with an expected count, moves the Table 3 float, fills the number placeholders,
checks labels (including the label inside the class table), references, tags, table counters,
and citations, and then copies `tables/table_class_exhibit.tex` after a check of its SHA-256
against the reconciliation record. It copies no other artifact. It stops on any mismatch and
writes nothing before every step passes. It has no assertions. The report of the committed
run is `integration/round3_report.txt`. The C.10 text is `integration/I04_oa_c10_classes.tex`.

## R3.3 Additions to main.tex

| Id | Where | Change |
|---|---|---|
| m01 | Introduction, robustness paragraph | One sentence announces the exhibit: dispersion within a class raises the option value of preparation; in Section 5.2 dispersed classes give the reversal and point-mass classes with the same means, costs, prior, and strengths do not. The next sentence starts "The reversal also holds", so its pronoun keeps its antecedent. |
| m02 | Section 4.2, new paragraph after the benchmark numbers | Spread ratio against the bound, the trading-cost window and k = 0.02, and the three prior intervals, each with its scope (window nonempty at the benchmark strengths; parts (i)-(ii) with the other benchmark inputs fixed; all three parts). Points to Section 5.2 for the priors 0.3 and 0.7. |
| m03, m04 | Section 5.1 | The Table 3 float moves from the end of Section 5.3 to the end of Section 5.1. Section 5.1 cites it first: "(Table 3, Panel A)" after the logistic and Laplace entry values, which are Panel A's rows. |
| m05 | Section 5.2, new last paragraph and the table | The exhibit paragraph (quoted in R3.4) and `\input{tables/table_class_exhibit.tex}` after `\setcounter{table}{3}`. The table file is a complete float with its own caption, "Quality classes and general priors.", which already has the manuscript's caption form; the file is not edited, so its label `tab:oa-class-exhibit` is the reference target. |
| m06 | Section 6.3 | The reserve comparisons become Table 5: counter 4, label `tab:4` renamed `tab:5`, three references updated. |
| m07 | Section 7, second prediction | Referee minor 10 (R3.7). |
| m08 | Figure 1 note | Referee minor 13 (R3.7). |
| m09 | Appendix A.8 | "The prior is π = 1/2 in each vector below", and one sentence that the four exhibit vectors, with priors 0.3 and 0.7, are declared in the notes to Table 4 and in Online Appendix C.10 (referee rank 1 asks for the vectors there). |

## R3.4 The exhibit paragraph (Section 5.2, as printed)

> Table 4 reports four economies outside the benchmark. Cases A, B, and C satisfy every
> hypothesis of Proposition 2, including that of part (iii), and its sufficient ownership
> condition. Cases A and B keep the point masses and set the prior at 0.3 and 0.7, where the
> benchmark vector violates these hypotheses and no trading cost satisfies (A2) at the
> benchmark strengths (Section 4.2). Each of the two cases therefore has its own high cost,
> trading cost, and weak strength, and entry rises from 0.250000 to 0.464564 in A and to
> 0.571808 in B. Case C sets the prior at 0.7 and draws values uniformly from [0.6, 1.4] and
> [1, 19], wide classes above the reserve with means ℓ and h. Its high class can lose to the
> strong incumbent, so the ownership condition has content: at r₁, W_H falls to 0.924383, and
> high-class ownership still rises from 0.175000 to 0.411984. Case D puts point masses at the
> same means and keeps the costs, prior, and strengths of C. C raises strong-economy entry to
> 0.563404, and D stays at 0.250000. Dispersion within a class raises the challenger's option
> value of preparation. Preparation reveals the value, and the challenger profits only when it
> wins, so its gross profit is convex in the value; a spread around the same mean raises gross
> profit at every belief. In C a favorable price lifts that profit above the high cost, and in
> D even the largest feasible posterior does not. The class model thus produces a reversal that
> the point-mass model with the same means, costs, prior, and strengths cannot produce. D fails
> the upper bound in (A1) at the strong strength, so its outcome is not a counterexample to
> Proposition 2.

Checks behind the wording:

- The "cannot" is scoped to the same means, costs, prior, and strengths. Proposition 2's
  nonemptiness clause still gives point-mass reversals at other vectors.
- Mechanism: g(θ) = E[(θ − max{p, R})₊] is convex in θ, so a mean-preserving spread raises g_H
  and g_L and so B(μ) at every belief. U[1, 19] puts mass inside the incumbent's support at
  r₁ = 4.5, where g is strictly convex, so the rise is strict. In the registry, D's threshold
  belief 0.866182 (`class_matched_point_07_r_1_tau`) exceeds M(0.7) = 0.863810
  (`class_matched_point_07_M`); C's threshold flow is 0.936639 (`class_wide_07_r_1_x_star`).
- Ownership in C is stated at r₁ only. At r₂ it is 0.157102 (`class_wide_07_r_2_O_H`), below
  the weak value, because W_H falls to 0.897727 (`class_wide_07_r_2_W_H`); the paragraph
  makes no claim there.
- "Violates these hypotheses" and "no trading cost satisfies (A2)" rest on the Section 4.2
  intervals: 0.3 and 0.7 lie outside (0.467850, 0.538096) and outside (0.404610, 0.595390).

## R3.5 Additions to online_appendix.tex

| Id | Where | Change |
|---|---|---|
| o01 | New C.10 (`oa-c-classes`), after C.9 | Transcribed from the worktree contract (`paper/online_appendix.md`, commit `9e7ab4d`): Inputs (cases, posterior bounds, W_H, τ, x*, entry, ownership, unattainable threshold), Conditions and status (all margins, ownership margins, Case D, analytical status from the global bounds), Benchmark intervals, Validation and outputs (fifty-digit inputs, independent checks, deviation grids, C.0 tolerances unchanged, outputs and manifest). The contract's `\input` of the table becomes a pointer to Table 4 of the paper; "the table below" becomes "the notes to Table 4 of the paper". The output files are a code block. It ends with "Feed: Table 4 and Sections 4.2 and 5.2 of the paper." |
| o02 | C.8 | "C.1 to C.7 and C.9" becomes "C.1 to C.7, C.9, and C.10". |
| o03b | C.8, Units and rounding | One sentence: the C.10 rows, margins included, use `decimal_6`, except the trade-cost bounds (`decimal_4`) and the spread ratio and its bound (`decimal_3`). The paragraph otherwise says margins and bounds use `scientific_10`, which the C.10 rows do not. |
| o03 | C.8, quantity families | Two rows: "Class exhibits: outcomes and margins" and "Benchmark prior and trade-cost windows; four-law entry range", both C.10, with the registry units. |
| o04 | E.1 run list | `$PY numerics/exercises/c10_classes.py` after the C.9 producer. |
| o05 | C.6 | "Feed: Table 4" becomes "Feed: Table 5". |

The worktree contract has no o02, o03, o03b, or o04 change; R3.9 lists them for the mirror.

## R3.6 Numbers and their registry names

Each `\NUM{name}` takes the registry display after two checks: the reconciliation row marked
"new, round 3" holds the same stored value, and the manifest display rule (round-half-even)
reproduces the registry display. Inputs come from `numerics/manifests/c10_classes.json`
(`passed: true`). The script printed 43 substitutions and left no placeholder.

| Printed | Registry name | Rule | Status | Where |
|---|---|---|---|---|
| 0.025 | `base_spread_ratio` | decimal_3 | analytical | Section 4.2, C.10 |
| 0.034 | `base_spread_ratio_bound` | decimal_3 | analytical | Section 4.2, C.10 |
| 0.0167 | `base_trade_cost_lower` | decimal_4 | analytical | Section 4.2, C.10 |
| 0.0224 | `base_trade_cost_upper` | decimal_4 | analytical | Section 4.2, C.10 |
| 0.404610 | `base_prior_window_lower` | decimal_6 | analytical | Section 4.2, C.10 |
| 0.595390 | `base_prior_window_upper` | decimal_6 | analytical | Section 4.2, C.10 |
| 0.467850 | `base_prior_prop2_lower` | decimal_6 | analytical | Section 4.2, C.10 |
| 0.538096 | `base_prior_prop2_upper` | decimal_6 | analytical | Section 4.2, C.10 |
| 0.467850 | `base_prior_prop2_all_lower` | decimal_6 | analytical | Section 4.2, C.10 |
| 0.500424 | `base_prior_prop2_all_upper` | decimal_6 | analytical | Section 4.2, C.10 |
| 0.301509 | `four_noise_entry_min` | decimal_6 | numerical diagnostic | C.10 |
| 0.522757 | `four_noise_entry_max` | decimal_6 | numerical diagnostic | C.10 |
| 0.250000 | `class_prior_03_r_0_E` | decimal_6 | analytical | Section 5.2 |
| 0.464564 | `class_prior_03_r_1_E` | decimal_6 | analytical | Section 5.2 |
| 0.571808 | `class_prior_07_r_1_E` | decimal_6 | analytical | Section 5.2 |
| 0.924383 | `class_wide_07_r_1_W_H` | decimal_6 | analytical | Section 5.2 |
| 0.175000 | `class_wide_07_r_0_O_H` | decimal_6 | analytical | Section 5.2 |
| 0.411984 | `class_wide_07_r_1_O_H` | decimal_6 | analytical | Section 5.2 |
| 0.563404 | `class_wide_07_r_1_E` | decimal_6 | analytical | Section 5.2 |
| 0.250000 | `class_matched_point_07_r_1_E` | decimal_6 | analytical | Section 5.2 |

Declared inputs printed from the run manifest: k = 0.02 (`benchmark.k`; Section 4.2, C.10);
priors 0.3 and 0.7 (`prior_03`, `prior_07`, `wide_07`; Sections 4.2 and 5.2, A.8); the C supports
[0.6, 1.4] and [1, 19] (`wide_07.a_L`, `b_L`, `a_H`, `b_H`; Section 5.2). The table file was
copied unchanged: SHA-256 `565f8c758f6f764fce2b9a12587b1c4cf91e508fec0365f6d89431223016516f`, the
value of the reconciliation row `file.tables.table_class_exhibit.tex` ("new, round 3").

The closed forms in C.10, (1/60, 1/[12(1+e)]), are the contract's formulas. No number in either
file was computed or typed for this round.

## R3.7 Referee minor items 10-14

| Item | Round 2 | Round 3 |
|---|---|---|
| 10 Section 7, "in the benchmark" | not applied | Applied (m07). The sentence already began "In the benchmark", but the qualifier attached to "the preparation cost is independent of value", which Section 2.2 assumes in general. Now "In the benchmark" opens the claim that a high-value buyer always outbids the incumbent and a low-value buyer loses above ℓ, and independence is the reason for the posterior-share claim. |
| 11 Proof of Proposition 1(c), continuity after mixing | applied | Present: "both mixtures are continuous, and the mixing scales the difference by a positive factor and keeps its sign". No change. |
| 12 Proposition A.5, zero cost with the hypotheses | applied | Present: "with preparation costs C ∈ {0, c_H}" stands with the hypotheses; the closing "with the zero preparation cost fixed" belongs to the nonemptiness clause. No change. |
| 13 Figure 1 note | not applied (kept on purpose) | Applied (m08): the trailing ", with prior 1/2" is removed. The panel (b) clause keeps "the prior 1/2", so the prior stays explicit once. |
| 14 Status of the Section 5.1 diagnostics | applied | Present: "These two values are fixed-profile numerical diagnostics: Online Appendix C.9 computes them without an equilibrium search under these laws." No change. |

## R3.8 Table numbering

The class table is a complete float, and `placeins` with the `section` option prints every
Section 5 float before Section 6. So any numbered table in Section 5.2 comes before the
reserve comparisons, and those become Table 5 under sequential numbering. Three generated
Online Appendix tables print main-text table numbers: `table_extensions_margins.tex` ("behind
Table 3"), `table_matched_price.tex` ("Table 3, Panel A"), and `table_reserve_details.tex`
("behind Table 4"). The exhibit is Table 4, and Table 3 keeps its number, because its float now
precedes the exhibit in the source. This choice leaves one stale generated caption (R3.9,
item 1) and one Online Appendix text edit (o05). With the exhibit as Table 3, three generated
references and five Online Appendix sentences would change.

## R3.9 Open items for the numerics member

1. `tables/table_reserve_details.tex`: the caption "Reserve comparisons: orders, margins,
   evidence, and identity behind Table 4." must read "Table 5". It is generated, so it needs a
   renderer change. Until then the Online Appendix shows the old number in that caption.
2. Contract mirror in `paper/online_appendix.md`: o02 (C.8 exercise list), o03b (display rules
   of the C.10 rows; the paragraph also omits the existing `decimal_2`), o03 (two families),
   o04 (E.1 run list), o05 (C.6 feeds Table 5), and the C.10 pointer to Table 4 of the paper in
   place of the `\input` of the table.
3. Optional: the class table carries the label `tab:oa-class-exhibit` although it is now a
   main-text table. The label is invisible in the PDF.
4. Round 4 of the numerics (commit `8eb6c2e`, report `f222ba3`: the C.0 tie-rule wording and the
   layout of `table_reserve_details.tex`) is not integrated in this round. The clone's C.0
   listing already reads "B(m) >= 0" since round 2. The new reserve-details layout would remove
   three of the five underfull boxes.

## R3.10 Verification

- The script run in `integration/round3_report.txt` shows each edit with its count, the float
  move and the source order of the three tables, every substitution with its registry row, the
  label, reference, tag, counter, and citation checks, and the table hash.
- Both documents were built from a clean `build/`. The logs were searched for errors, LaTeX
  warnings, "undefined", "multiply defined", rerun requests, and overfull and underfull boxes.
- The PDF text was read for the introduction (page 4), Section 4.2 (page 25), Section 5.1
  (page 31), Section 5.2 (pages 33-35), Section 7 (page 44), the Figure 1 note (page 18),
  Appendix A.8 (page 93), and Online Appendix C.6, C.8, C.10, and E.1. Page images were checked
  for main pages 25 and 33-36 (Tables 3 and 4) and Online Appendix pages 52, 54, and 55.
- No test was written or run.
