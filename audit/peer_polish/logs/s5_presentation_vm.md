# S5 presentation and registry completion

Final canonical rendering used the frozen full C.2 and C.6 outputs after independent verification released its input-stability hold. No exploratory corpus was withheld.

## Checks

- `numerics/registry.py`: 128 quantities, zero open rows, all seven price-pool keys resolved.
- `numerics/check_registry.py`: identical registry output across twelve fresh-process precision/import-order combinations.
- `pytest numerics/tests/test_registry_invariants.py numerics/tests/test_render_boundaries.py`: 17 passed.
- `numerics/render/render_all.py`: passed; four figures, four main tables, five online-table files, source-derived companion CSVs and full quantity dictionary regenerated.
- All standalone table QA compilations use the manuscript fonts and one-inch margins and report zero overfull boxes. Table QA totals eleven pages: four main/signal pages, two matched/margins pages, five reserve pages. These are exhibit checks; final full-manuscript page review remains a separate release gate.

## Retained content and presentation

- P22: main matched-dividend rows moved to the online matched-price panel. The renderer checks mean-price/dividend, unchanged preparation/outcomes, and investor-residual identities. The external dividend is excluded from seller revenue.
- P23: Table 3 displays preparation changes in percentage points computed from the same validated probabilities. Full margins and all 25 signal accuracy rows remain online, including negative comparisons and unmet sufficient conditions.
- P24: main Table 4 contains the eight supported fixed-reserve comparisons with preparation, sale, two-admissible-bidder probability, proceeds and trading outcome. Its rows join complete continuation and parameter identities across final comparison/event files. Exploratory maxima and final-pass attempt counts remain online; earlier refinement attempts are explicitly distinguished and archived. All 40 exact-event rows remain in a multipage landscape table.
- P25: Figure 2 checks complete identities and deduplicated counts, distinguishes analytical shading from found-multiplicity node ticks, preserves gaps and all accepted branch points, names analytical bounds, and retains genuine certificate interval widths. The mixed diagnostic node is a diamond with its identified support triangles. At the high-cost ceiling, the validated equality point is closed and the right-hand limit is open.
- P26: Figure 3 closes the logistic endpoint at zero tail mass and baseline preparation, preserves positive Laplace plateau mass, validates common scale and noise-standardized cutoff 1.4953689214214978.
- P27: Figure 4 excludes eta=1 by numeric comparison and rejects nonpositive/nonfinite profits on the retained domain. Axis limits include every positive retained value.
- P28: full definitions and selectors are in `replication/quantity_dictionary.md` and both registry CSVs. Registry scalar guards reject nonfinite values, reversed enclosures, duplicate/unknown selectors and invalid probabilities. Full source identities are retained in the registry.

## Visual evidence

Final Figure 2 color and grayscale screenshots: `audit/peer_polish/figures_qa/equilibrium_correspondence_final.png` and `equilibrium_correspondence_final_gray.png`. Both panels were inspected after the final root cleanup. No clipping or overlap; region/branch styles remain distinguishable in grayscale. Figures 1, 3 and 4 were also inspected, with the detailed iteration record in `audit/peer_polish/figures_qa/inspection.md`.

Table screenshot evidence is under `audit/peer_polish/tables_qa/`. Final matched-price panel and exploratory summary were rechecked after regeneration; all other layouts retain their inspected geometry. Temporary QA PDFs/TeX/aux files are not release artifacts.

## Final quantities and output hashes

| Pool key | Display | Status |
|---|---|---|
| pool_reserve | 7 | input |
| pool_posterior_cutoff_low | 0.272979 | analytical |
| pool_posterior_cutoff_high | 0.303265 | analytical |
| pool_entry_cutoff_low | 0.151805 | analytical |
| pool_entry_cutoff_high | 0.125000 | analytical |
| pool_revenue_cutoff_low | 0.687364 | analytical |
| pool_revenue_cutoff_high | 0.609643 | analytical |

| Output | SHA-256 |
|---|---|
| `figures/two_returns.pdf` | `c31343e30fd2b1a15fc285013154b6c12ac5007381706300a0aad8a9d0ac4438` |
| `figures/equilibrium_correspondence.pdf` | `d7c918f8ac1eaeb75b013230f5f9f32cc4bc8720e4f015ee2ce77ae239838003` |
| `figures/posterior_tail_entry.pdf` | `312418860527814fd20bfda15d7ca79cd7a5cd393c64edfbb0f1a3bc495dc513` |
| `figures/bargaining_weight.pdf` | `9018f5624f9b1595115a9995f0737a710f528f37f1c540c9687a1b04c4e93457` |
| `tables/table1_auction_primitives.tex` | `e2ae3f48738c89c774311e0e0bca572489e02f9d47bd946777787b2e53ad7e5f` |
| `tables/table2_equilibrium_controls.tex` | `2f175d699144e04b98ba6201fb296d0e68894418fea4fce9c7b5502b7473f016` |
| `tables/table3_extensions.tex` | `2f335907a7414ae9733aca6a80f3ef190e35440bcbe0dcdd9b6af3afdb5b0177` |
| `tables/table4_reserve_comparisons.tex` | `b31b608f68830ae3b613f72b4f9918fe7e801123eaf8baa012a7570071c98063` |
| `tables/table_matched_price.tex` | `bc866f5c1e5e0dcfa1cbeeb0fd943c448df0b0e5cf8747802d42244fb729e6a8` |
| `tables/matched_price.csv` | `38a6e847d8df7e1ab35f9f01ad0521f9fb6a2bc020bd6a4048920690713e1bc1` |
| `tables/table_extensions_margins.tex` | `89ef8fac49cc321ec9d6fba8c4689fa2c221d7ea84872a710c2da41249d39605` |
| `tables/extensions_margins.csv` | `50e7464b2da76e28be7561f32a6b7aa6749cf50c98d714d15347c592d9f49fc1` |
| `tables/table_signal_grid.tex` | `a3e0ed9aceb9ac5d8fadf2091ad113196669f70d9b527cc26614fb83f1593232` |
| `tables/table_reserve_details.tex` | `64f94beec36755f45c35a5f8edaab860689a6938aa99d0cdd7d7e1cb565ca900` |
| `tables/table_reserve_exploratory.tex` | `a5932bf6012cce847e9b0cee0b382b75b7b7518204ddc3a7096e47d771412474` |
| `replication/quantity_dictionary.md` | `88855662e2c2daba0430ab675f714574ed8dab0b70d4ce4d1258b1b2a022c6e3` |
| `replication/quantity_registry.csv` | `ca0cd1d611030ebbb1a0dea650bdf6ba124904a43e31978dd3ca21642d2358b0` |

All input hashes are recorded in `numerics/manifests/render.json`.
