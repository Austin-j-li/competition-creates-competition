# Information derivation

Run from the repository root:

```bash
TMPDIR="$PWD/audit/slot_manuscript_2026_10_23/scripts/P4_information" \
bash audit/slot_manuscript_2026_10_23/scripts/_slots/run_slot.sh \
.venv/bin/python audit/slot_manuscript_2026_10_23/scripts/P4_information/derive.py \
> audit/slot_manuscript_2026_10_23/scripts/P4_information/run.log
```

The program prints the declared outcomes through its CLI.
It writes the registry, local number macros, exact interval endpoints, and a receipt.
It contains no assertions.

The arithmetic uses rational endpoints for every operation.
The exponential constant lies between its Taylor sum through index 60 and that sum plus `1/(60*60!)`.
Decimal inputs enter as exact fractions.
The log rounds interval endpoints outwards.
Every strict sign follows from a rational endpoint.
The interval width is not a statistical confidence interval.

The current B declaration fixes `beta = 0.294655` and `u = e - 1`.
It derives the presence probability without rounding.
The earlier study used a slightly different B convention.
The label S(B) keeps the current slot parameters and uses the source's separate signal vector.

Round 2 selects `(a_T, d) = (47/50, 101/200)` at unchanged B.
The selected tuples use `p4_comp_b_*`; both controls have their own tuples and strict margins.
The earlier `(19/20, 101/200)` pair keeps every original key and value.
Its new no-signal control shows why that pair does not establish complementarity.
The derivation imports no checker code.

The frozen-order ceiling uses rational bisection of `B_r(M) - 6` on `[3, 18/5]`.
Its two endpoint gaps certify the root bracket; monotonicity proves uniqueness.
The registry contains 1,332 rows, including all 1,038 original keys.
The four shared floor rows use exact fractions and analytical status, as P1 does.

The program records every order posterior, price, class entry rate, and unilateral order payoff.
The exact mixed B rates follow from the algebra in the proof.
Their payoff intervals contain zero because the same irrational input appears more than once.
The proof establishes the zero payoffs by exact algebraic cancellation.

Compile from `audit/slot_manuscript_2026_10_23/proofs/`:

```bash
TMPDIR="$PWD/../scripts/P4_information" \
/home/uctpiaj/work/.local/bin/latexmk -pdf -interaction=nonstopmode \
-halt-on-error -outdir=build P4_information.tex
```

The source record is `overleaf/paper` at commit `01bd5d6`.
The proof uses main Sections 4.2, 5.1, 5.3, A.4, and A.5.
It also uses Online Appendix A.6, A.7, C.0, and C.3, plus the control table.
The current brief supplies the exact slot declaration.

Files:

- `derive.py`: executable derivation.
- `run.log`: complete outcome and margin record.
- `endpoints.json`: exact rational bounds for every registry row.
- `numbers.tex`: local macros generated from the same rows.
- `receipt.json`: inputs, method, and hashes.
- `compile.log`: article build record.
- `page-*.png`: rendered article pages for visual inspection.
- `round1_registry.csv`: the original rows, retained for the key comparison.
- `proof_text.txt`: text extracted from the current article PDF.
- `inspection.md`: the Round 2 output inspection record.
- `delivery_hashes.json`: hashes of the delivered files.
