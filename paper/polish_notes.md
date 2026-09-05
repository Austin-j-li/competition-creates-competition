# Circulation edit — 5 September 2026

The main paper and online appendix have been rewritten, regenerated, and checked. The title, single-author voice, model, three main propositions, and validated numerical exercise outputs are retained. No skill, plugin, or dependency was installed for this edit.

The main PDF has 52 pages: title and abstract on page 1, body on pages 2–29, references on pages 30–33, and the paper appendix on pages 34–52. The compact online appendix has 43 pages. The abstract has 147 words and the introduction approximately 1,040 words, spanning just under four double-spaced pages.

## Editorial changes

The main text now has the eight agreed sections. The introduction explains the institutional setting and the opposing acquisition and trading incentives before stating the results. The payoff and price-learning discussions are combined. Intuition stays beside the propositions; detailed trading bounds, signal formulas, certificate calculations, and the seller's continuation problem are in the appendices. The sale-terms discussion concentrates on the completed bargaining and reserve comparisons.

Editorial references were the [econ-writing guide](https://github.com/Silas1929/econ-writing), Gorbenko and Malenko's [Auctions with Endogenous Initiation](https://drive.google.com/file/d/1xw2SXJxpZcaNf2d_-0V9r6V1GGFemm2S/view), and Gorbenko's [M&A theory chapter](https://drive.google.com/file/d/1OZy9uJKRM7L6gkmPirQqHkykrXTKrlP1/view). The edit uses concrete motivation, explicit incentives, economical exposition, and restrained claims.

## Evidence and claim boundaries

| Main claim | Supporting material and retained scope |
|---|---|
| Competition lowers acquisition profit and raises the information spread | Proposition 1; Online Appendix A.2; C.1 payoff checks. The spread is not described as unbounded on the maintained domain. |
| Entry reverses as the incumbent strengthens | Proposition 2 and its strict inequalities; Online Appendix A.4–A.6; C.1 controls. The comparison concerns the specified economies, without imposing monotonicity between them. |
| Informative equilibria coexist with no trade | Proposition 3; paper Appendix A.4; Online Appendix B and C.2. The three ordered certified intervals establish three comparisons. Other plotted branches remain numerical continuations. |
| Robustness and complementary signals | Propositions A.5–A.7 and C.3–C.5. Main Table 3 summarizes the declared examples; Online Appendix Table 1 retains all 25 accuracy combinations. |
| Gains from access to prices | Proposition A.9, Online Appendix A.9, and C.1. Table 2 separates target proceeds from acquisition surplus net of preparation costs. |
| Effects of sale terms | Proposition A.8 and C.7 establish payment-stage results. C.6 supports the declared reserve comparisons and exploratory ranges, not an optimal reserve. |
| Empirical implications | Online Appendix D specifies a pilot and measurement design; no sample or estimated effect is asserted. |

Two overly broad extension statements were narrowed: Proposition A.6 and Lemma OA.1 now refer to parts (i) and (ii) of Proposition 2, which their stated assumptions support. The three main propositions are preserved. Table 4 now reports entry and revenue ranges separately; their endpoints need not represent the same continuation.

## Presentation and checks

- Repaired alignment and line breaks in the probability, private-signal, and certificate equations. Equation, section, figure, table, and cross-document references were updated.
- Rebuilt all four main tables. Welfare has a separate panel; the complete signal grid uses a multipage table with repeated headers. Registry tables have widths suited to their contents.
- Standardized serif figure typography, panel labels, captions, notes, line styles, and spacing. All four figures remain vector graphics with embedded fonts. Accepted branches, certified intervals, and breaks at unresolved gaps are retained; grayscale versions were inspected.
- Registry arithmetic now uses a local 60-digit decimal context. The regression check passes all 12 combinations of ambient precision and import order, preserves the caller's context, and returns identical output. The registry CSV is unchanged from the validated 60-digit baseline; its manifest was regenerated and is included in final hash verification.
- The final numerical acceptance gate passed, including all exercise, registry, and presentation hashes. Strict substitution filled all 95 required keys with zero unresolved or unknown keys. The original citation occurrences and quantity keys are retained.
- Both PDFs built successfully with zero warnings: no overfull or underfull boxes, oversized floats, missing glyphs, or undefined references. All 95 final pages were visually checked, including unchanged pages verified against their earlier renders. All PDF fonts are embedded; no off-page text or rasterized figures was found.

The authoritative sources remain `paper/main.md` and `paper/online_appendix.md`. The generated PDFs are `paper/main_filled.pdf` and `paper/online_appendix_filled.pdf`. README and Online Appendix E give the rebuild sequence. Existing validated exercise outputs were reused; no expensive equilibrium search was rerun.

The full intermediate equilibrium correspondence, optimal seller terms and commitment timing, alternative-format trading equilibria, and empirical identification remain research extensions. These are stated explicitly in the revised paper.
