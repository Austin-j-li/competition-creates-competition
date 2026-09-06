# Final label map for the peer-circulation revision

Baseline is commit `16fa9f8`, as recorded in `label_map_baseline.md`. Display numbers below refer to authoritative current sources. Persistent equation labels and result/section anchors now support local links; a later display-number change need not alter the target. Cross-document source links are rendered as named references in the standalone PDFs.

## Paper appendix sections

| Baseline | Current location | Stable anchor |
|---|---|---|
| A.1 Supporting results | A.1 payoffs/inference; A.2 fixed information/thresholds; A.4 extensions; A.5 signals; A.6 bargaining/welfare | result anchors below |
| A.2 Trading bounds and extension formulas | A.2, A.4, A.5, A.6 | pa-proofs; pa-calculations; pa-signals; pa-welfare |
| A.3 Proofs of Propositions 1–3 | A.1, A.2, A.3 | pa-results; pa-proofs; pa-certificate |
| A.4 Certified equilibria | A.3 | pa-certificate |
| A.5 Seller continuation | A.7 | pa-design |
| A.6 Numerical parameters | A.8 | pa-parameters |

## Formal results

Propositions 1–3 and A.1–A.9 retain their identities. Proposition A.10 and online Proposition OA.3 establish the price-pool family. Online Lemmas OA.1–OA.2 retain their identities.

| Document | Result | Stable anchor | Line |
|---|---|---|---|
| main | Proposition 1 | result-proposition-1 | 125 |
| main | Proposition 2 | result-proposition-2 | 216 |
| main | Proposition 3 | result-proposition-3 | 275 |
| main | Proposition A.1 | result-proposition-a-1 | 458 |
| main | Proposition A.2 | result-proposition-a-2 | 464 |
| main | Proposition A.3 | result-proposition-a-3 | 554 |
| main | Proposition A.4 | result-proposition-a-4 | 568 |
| main | Proposition A.5 | result-proposition-a-5 | 733 |
| main | Proposition A.6 | result-proposition-a-6 | 753 |
| main | Proposition A.7 | result-proposition-a-7 | 809 |
| main | Proposition A.8 | result-proposition-a-8 | 897 |
| main | Proposition A.9 | result-proposition-a-9 | 918 |
| main | Proposition A.10 | result-proposition-a-10 | 1004 |
| online_appendix | Lemma OA.1 | result-lemma-oa-1 | 326 |
| online_appendix | Lemma OA.2 | result-lemma-oa-2 | 330 |
| online_appendix | Proposition OA.3 | result-proposition-oa-3 | 759 |

## Paper equation relocation

Main equations 1–14 and conditions A1–A3 retain their numbers. Their labels are `eq:paper-1` through `eq:paper-14` and `eq:paper-a1` through `eq:paper-a3`.

| Old appendix equation | Current equation |
|---|---|
| A.1 | A.10 |
| A.2 | A.11 |
| A.3 | A.29 |
| A.4 | A.4 |
| A.5 | A.6 |
| A.6 | A.21 |
| A.7 | A.23 |
| A.8 | A.22 |
| A.9 | A.24 |
| A.10 | A.25 |
| A.11 | A.26 |
| A.12 | A.27 |
| A.13 | A.28 and A.33 |
| A.14 | A.34 |
| A.15 | A.35 |
| A.16 | A.32 and A.33 |
| A.17 | A.36 |
| A.18 | A.37 |
| A.19 | A.39 |
| A.20 | A.41 |
| A.21 | A.1 |
| A.22 | A.5 |
| A.23 | A.8 |
| A.24 | A.14 |
| A.25 | A.12 |
| A.26 | A.13 |
| A.27 | A.15 |
| A.28 | A.16 |
| A.29 | A.17 |
| A.30 | A.18 |
| A.31 | A.19 |
| A.32 | A.20 |
| A.33 | A.44 |
| A.34 | A.44 |
| A.35 | A.42 |
| A.36 | A.53 |
| A.37 | A.54 |
| A.38 | A.55 |
| A.39 | A.56 |
| A.40 | A.57 |

Current appendix labels are `eq:paper-a-1` through `eq:paper-a-57`. New displays separate the payoff opposition, price construction, fixed-experiment difference, signal conditional-independence and posterior identities, bargaining objective, conditional surplus, complete continuation, price-pool proof, reserve events, and admissible-bid outcomes.

## Online equations and sections

Existing section anchors survive. Added `oa-a-pools` for A.11, `oa-c-price-pools` for C.6b, and `oa-c-reserve-events` for C.6c.

| Old online equation | Current equation |
|---|---|
| OA.1–OA.52 | unchanged |
| OA.53–OA.55 | OA.54–OA.56 |
| OA.56–OA.70 | OA.65–OA.79 |

OA.53 is the new complete continuation object; OA.57–OA.64 give the price-pool family. Labels are `eq:oa-oa-1` through `eq:oa-oa-79`.

## Exhibits

Main Figures 1–4 and Tables 1–4 retain their numbers and `fig:N` / `tab:N` labels. The signal-grid reference now names Online Appendix C.3 rather than assuming it is the first table. New online table inputs use existing labels `tab:oa-matched-price`, `tab:oa-margins`, and `tab:oa-reserve-details`; the signal table uses `tab:oa-signals`. The retained exploratory reserve summary uses `tab:oa-reserve-exploratory`.

## Checks

`manuscript_source_audit.json` records citation resolution, equation targets, anchor links, placeholder definitions, author voice, and abstract length. Pandoc citation parsing succeeded for both sources without warnings. Final PDF numbering and visual checks belong to the build gate.
