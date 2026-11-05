# M2 notes: placeholders, labels, and integrator checks

Companion to `M2_00_INVENTORY.md`. Fragments are `M2_01` to `M2_20` in this folder.

## 1. Placeholders used in the M2 fragments

`\NUM` is not yet defined in either manuscript. The integrator adds it or substitutes
from `reconciliation.csv` at integration.

| Name | Where used | Definition | Source |
|---|---|---|---|
| `atomless_entry_strong_laplace` | M2_01 | Strong-incumbent entry `\mathsf E` under the declared atomless cost law with Laplace noise, at the benchmark vector of (A.55) | Numerics report; the current text value 0.522715 used a low support near 1 and is not valid for a support at zero |
| `atomless_entry_strong_logistic` | M2_01 | Same entry quantity with logistic noise | Numerics report; current text value 0.301374 is likewise superseded |
| `atomless_epsilon_C` | M2_09, M2_15 | Value of `\varepsilon_C`: the low component's support width from zero and the high component's half-width around `c_H`, as in (A.24) | Numerics report. The old declaration 0.1 was a half-width around cost 1 |
| `atomless_low_upper` | M2_15, M2_20 | Upper end of the low component's support, `[0, atomless_low_upper]`. It equals `atomless_epsilon_C` under a law on `[0,\varepsilon_C]` and twice it under a law on `[0,2\varepsilon_C]` | Numerics report, which fixes the exact low-cost law. If the two values coincide, the integrator may collapse this name into `atomless_epsilon_C` |
| `reserve_event_sampled_weak_max` | M2_18 (twice) | The reserve that the current C.6 sweep reports as the sampled weak-economy revenue maximum, in the online-summary sense of C.6 ("highest revenue among continuations found") | New C.6 ledger. The current text value 6.280 came from the earlier sweep and sat next to the old endpoint `h-1/m` |

Net-surplus levels need no new placeholder name from M2. No level of `\mathcal W` is printed
in an M2 fragment. The levels sit in Table 2 (Section 4, drafter A) and in the C.1 panels,
which the pipeline regenerates at the new declarations.
Check for the pipeline: inside the old cost window, orders, entry, ownership, and proceeds
do not move, and the level of net surplus rises by `\rho` times the old low cost, while
`\Delta\mathcal W` and `\Delta\mathcal R_T` do not move. At the benchmark that shift is
`0.25`. The normalization memo in `audit/alex_meeting_2026_10_21/memos/Q4_normalization.md`
(Sections 3.4 and 3.7) records diagnostic benchmark levels under both costs. The pipeline
values must reproduce that shift; the memo values are a check, not manuscript numbers.

Numbers that M2 deliberately kept, with the reason in each fragment header:

- Section 5.3 example, entry 0.850000 to 0.879438. At the signal vector, gross profit at
  the lowest joint posterior is about 1.773, above the old low cost 1. Preparation,
  orders, and entry are the same at cost zero. An independent arithmetic check of this
  value from (A.27)–(A.29) formulas is recorded in the task reply.
- Section 6.1 proceeds 0.872392 and 0.614583, and dividend 0.257809.
- Section 6.3 class-economy proceeds and preparation at reserves 0.5 and 1.1.
  At both reserves and both strengths, gross profit at the lowest belief exceeds the old
  low cost 1, so the old low-cost realization already prepared at each price.
- All numbers inside generated tables (`tables/table2*`, `table3_extensions.tex`,
  `table4_reserve_comparisons.tex`, reserve detail tables, matched-price panel).
  Those are pipeline outputs. The integrator must regenerate them at the new
  declarations before accepting any kept number above. Table 2 net-surplus levels will move.

## 2. Labels removed, retained, and added

### Removed by M2 fragments, with every reference to them

main.tex:

| Label | Defined at | References | Disposition |
|---|---|---|---|
| `price-pooling-at-fixed-orders` | 2337 | None in either file | Removed with the subsection; replaced by `the-price-experiment-at-fixed-orders` |
| `result-proposition-a-10` | 2375 | main.tex 2625–2626; online_appendix.tex 1362 (text "Proposition A.10"); online_appendix.tex 3035 (feed line) | All three sit inside M2 replacements (M2_09, M2_14, M2_17) and leave with them |
| `eq:paper-a-45` | 2367 | main.tex 2377, inside the removed proposition | Leaves with it |
| `eq:paper-a-46` | 2387 | None outside its own paragraph | Leaves with the subsection |
| `eq:paper-a-47` | 2421 | None outside its own paragraph | Leaves with the subsection |
| `eq:paper-a-48` | 2434 | main.tex 2442, inside the removed subsection | Leaves with it |
| `eq:paper-a-49` | 2455 | None outside its own paragraph | Leaves with the subsection |

online_appendix.tex:

| Label | Defined at | References | Disposition |
|---|---|---|---|
| `result-proposition-oa-3` | 1546 | None in either file | Removed with Proposition OA.3 |
| `eq:oa-oa-57` | 1403 | None outside A.11 | Leaves with A.11 |
| `eq:oa-oa-58` | 1416 | 1548; 2970 in C.6b | Both passages are replaced (M2_14, M2_17) |
| `eq:oa-oa-59` | 1439 | 1568; 2972 in C.6b | Same |
| `eq:oa-oa-60` | 1451 | 1551; 2975 in C.6b | Same |
| `eq:oa-oa-61` | 1490 | 1496; 2979 in C.6b | Same |
| `eq:oa-oa-62` | 1506 | 2981 in C.6b | Same |
| `eq:oa-oa-63` | 1532 | 1535; 2987 in C.6b | Same |
| `eq:oa-oa-64` | 1578 | 1587, 1597; 2993 in C.6b | Same |

After the M2 fragments are applied, no reference in either file points at a label in these
two tables. The integrator should still run a label sweep after applying all drafters'
fragments, because other fragments touch adjacent lines.

### Retained with new content, so that references keep working

- `eq:paper-a-24`, `result-proposition-a-6` (atomless costs, M2_05).
- `result-proposition-a-7`, `eq:paper-a-29` (signals, M2_06); (A.29) loses its first line.
- `exact-reserve-events`, `eq:paper-a-50`, `eq:paper-a-51` (M2_08).
  References at main.tex 2579 and the event sentence in Appendix A.8 stay valid.
- `eq:paper-a-55`, `eq:paper-a-56`, `eq:paper-a-57` (parameter vectors, M2_09).
- `oa-a-pools` (A.11, M2_14). References at online_appendix.tex 1291 (M2_13) and 2730
  (M2_16) now point at the short note.
- `oa-c-price-pools` (C.6b, M2_17). No reference points at it; it stays only so the
  subsection number does not move.
- `eq:oa-oa-26`, `eq:oa-oa-29`, `eq:oa-oa-77`, `eq:oa-oa-78`, `eq:oa-oa-79`.
  (OA.29) loses its first line, (OA.78) loses its `c_L` choice, (OA.79) now serves
  plateau atoms.

### Added

- `the-price-experiment-at-fixed-orders` in Appendix A.7 (M2_08). No other text
  references it yet. Section 6.3 refers to Appendix A.7 through the existing
  `pa-design` label, unchanged.

### Removed outside M2, which the integrator must settle with this set

- `eq:paper-a1` (main.tex 585) belongs to drafter A. Its references sit at main.tex
  612, 1476, 1494, 1538 (drafter A) and 1860 (drafter B; fragment B02 in this folder
  replaces lines 1815–1880 and keeps the surviving condition labels
  `eq:paper-a2`, `eq:paper-a3`). No M2 fragment references `eq:paper-a1` or the text
  "(A1)". M2 fragments keep (A2) and (A3) under those numbers, matching B02.
  If the integrator renumbers the surviving conditions, rename them in M2_05, M2_10,
  and M2_20 in the same pass.
- Registry and control names retired with C.6b: `pool_reserve`,
  `price_pool_cutoff_grid`, `price_pool_negative_controls`, the registry keys
  `pool_posterior_cutoff_*`, `pool_entry_cutoff_*`, `pool_revenue_cutoff_*`, the output
  `numerics/price_pool_regression.csv`, and the run-list entry
  `numerics/exercises/c6b_price_pools.py`. Their mentions sat at online_appendix.tex
  1370, 1589–1590, 1945–1948, 3014, 3035, 3198, 3212–3213, 3223, and 3482. Each is inside
  an M2 replacement or the M2_20 deletion line.

### Schema names kept on purpose

`c_L` as an input key and CSV column (value 0), `\zeta_L`, `low_cost_margin`,
`low_cost_floor_margin`, `low_cost_floor_relation`, `low_cost_floor_valid`, and the
C.6 `pool_*` continuation columns stay as names with new definitions. Renaming them is a
numerics-contract change, not a manuscript change. The integrator and the numerics team
either keep them or rename them in the contract, the code, and these fragments together.

## 3. Equation and proposition numbering

- Removing (A.45)–(A.49) in main.tex and (OA.57)–(OA.64) in the Online Appendix leaves
  gaps if later tags keep their numbers. The fragments keep (A.50) onward and (OA.65)
  onward unchanged. Closing the gaps instead means retagging about eight displays in
  main.tex and about fifteen in the Online Appendix and checking each `\eqref`.
  Either choice is mechanical; make it once, after all fragments land.
- Proposition A.10 is the last appendix proposition in main.tex and Proposition OA.3
  the last in the Online Appendix, so their removal renumbers no other proposition.
- Subsection numbers do not move: Appendix A.7 keeps four subsubsections in the same
  order after M2_08, A.11 keeps its number and position (M2_14), and C.6b keeps its
  number as a retired-exercise note (M2_17). Deleting the C.6b stub later is safe but
  then C.6c keeps its printed number only if the stub stays or the number is set by hand.

## 4. Decisions the integrator must confirm

1. **Cost entry in the parameter vectors.** M2_09 drops the old low-cost entry from
   (A.55)–(A.57) and states the cost law in words, following the brief's notation
   sheet. If the integrator keeps a cost slot in each tuple, its value is 0 in all
   three vectors. Either form is correct; the declarations in C.0 (M2_15) keep the
   key `c_L = 0` until the numerics contract decides.
2. **Condition numbering after (A1).** See Section 2 above. M2 assumes (A2) and (A3)
   keep their numbers.
3. **Atomless law.** `audit/revision_v2_2026_10_21/NUMERICS.md` did not exist when
   these fragments were drafted. All M2 support statements use only
   `[0,\varepsilon_C]` and `[c_H-\varepsilon_C,c_H+\varepsilon_C]`, so they hold for any
   component laws on those supports. The declared law in C.0 and C.1 must name the
   components (uniform or otherwise) once the numerics report lands, and
   `\NUM{atomless_low_upper}` must match it.
4. **Overlap with fragments already in this folder.**
   - B01 replaces the noise text around the atomless paragraph and states that it
     preserves lines 862–871. M2_01 replaces those lines. Apply both; they do not overlap.
   - B03 inserts at the head of Online Appendix A.6. M2_10 replaces the atomless
     passage at lines 749–770. No overlap.
   - M1_05 inserts after main.tex line 956, inside Section 6.1. M2_03 replaces
     lines 937–940 only. Apply both.
   - M1_08 inserts before `\section{B}` at online_appendix.tex line 1611, that is, at
     the end of A.11. Apply M2_14 first, then place that insert after the short A.11 note.
5. **The reserve argument's cost law.** The fixed-orders argument in M2_08 and M2_16
   uses the two-point cost law, where the atom at zero gives entry at least `\rho`
   even at zero gross profit. An atomless law that starts at zero without an atom
   gives entry zero where gross profit is exactly zero. The fragments state the
   two-point law where the argument needs it. Do not widen that claim to atomless
   costs at reserves with zero gross profit.
6. **Style.** Prose follows the house style in
   `audit/revision_v2_2026_10_21/BRIEF.md`: direct claims with their conditions
   intact. Status words stay where the results need them: analytical for the
   propositions that keep proofs, open for seller-optimal terms.

## 5. Verification the integrator and the numerics team still owe

These fragments change manuscript text and the numerical contract in C.0, C.1, C.3,
C.4, C.6, C.6c, and C.8. They do not change code, and no fragment has been compiled,
because the manuscripts change only at integration. After integration, run the
project gate for the affected exercises from the repository root, as the project verification
gate prescribes:

- `.venv/bin/python numerics/verify.py --stage c1 c3 c4 c6 c6c` after the numerics
  declarations and exercises carry the zero cost, with `--rerun` for the cheap stages.
- Regenerate tables and figures, then build both PDFs. The long C.6 stage runs in the
  background under the same gate.

A scoped static check is the right gate for this drafting step alone. It was run as a
print-only arithmetic pass over the affected margins (Section 1 above): gross profit at
the lowest belief at the three benchmark strengths, the endpoint `p_L=h` against the old
`h-1/m`, the pooled-profit value that defeats the old pooling family at cost zero, and
gross profit at the lowest joint posterior for the signal vector. No pipeline stage was
run or marked passed for these fragments.
