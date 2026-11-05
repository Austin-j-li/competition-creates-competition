# Paper check of main frames 10–20

Date: 28 October 2026.

The displayed formulas match the paper within the stated model. The prose needs the corrections below before final use.
The main risks are missing scope conditions, claims of full revelation, and strict claims where the formulas permit equality.
The slide files stay unchanged. The spoken script uses the corrected scope.

The supplied PDF contains 57 pages. The title and main frames occupy pages 1–21; backups follow.
This check covers printed frames 10–20, which are PDF pages 11–21.
I read the TeX and paper sources, extracted the PDF text, and examined all eleven rendered frames.
Line numbers below refer to `/home/uctpiaj/work/tmp/ccc-beamer30/slides.tex` at the recorded hash.
Paper paths are relative to `overleaf/slot/`.

## Problems, most serious first

“Medium” denotes a substantive scope or interpretation problem. “Low” denotes an imprecise gloss or shorthand.
No displayed formula failed this comparison. A correct box does not remove a false or unrestricted claim elsewhere on its frame.

| Severity | Frame | Line and current text | What the paper says | Corrected line |
|---|---:|---|---|---|
| Medium | 20 | 858: “no price before preparation means strength cannot raise entry” | The fixed-information proposition fixes the joint law of class and signal, class laws, cost law, independence and the tie rule. No price alone does not fix other information. See `appendix/A6_robustness.tex:8–16`. | “With other information, values, reserve and costs fixed under the control's assumptions, no price before preparation means strength cannot raise entry.” |
| Medium | 17 | 695, 739: the title and intuition imply that every wider spread produces more research and entry. | Proposition 4 concerns the equilibrium where good synergy buys after success and only a purchase recruits. Research stays constant at the cap. The equilibrium also requires the threshold condition. See `sections/05_research.tex:49–60`. | “On this equilibrium, a wider spread raises research below the cap. Research and entry stay constant at the cap while this equilibrium persists.” |
| Medium | 14 | 592: “Orders still reveal the case, but profit stays too low.” | Orders reveal a posterior, not the class. Full liquidity support leaves every posterior strictly between zero and one. See `appendix/A2_beliefs_trading.tex:35–45`, and its proof, part (a). | “Orders still convey partial news about the case, but buyer profit stays below the high cost.” |
| Medium | 12 | 503: “a correct order always trades at a favourable price, and a wider spread enlarges that gain.” | This frame allows `Delta_T = 0`. Its gross gains can then equal zero. The gain also depends on entry and the posterior. A wider spread raises it with those objects fixed. See the informed-trading lemma in `appendix/A2_beliefs_trading.tex:190–245`. | “With positive spread, a correct order has a positive gross gain. With entry and beliefs fixed, a wider spread raises that gain.” |
| Medium | 18 | 776: “the extra bidder raises both the sale price and the value created” | The proposition gives strictly positive expected proceeds and expected acquisition surplus net of preparation costs. It does not give strict gains in every realization. See `appendix/A7_welfare.tex:14–23`, and its surplus proof. | “Under these conditions, price access raises expected sale proceeds and expected acquisition surplus net of preparation costs.” |
| Medium | 16 | 681, 686: “Full informed orders held fixed”; the explanatory note omits their status at the weak strength. | The frozen profile is a control, not an equilibrium at the weak strength. Its informed orders lose money there. See `appendix/A6_robustness.tex:35–54`. | “Full informed orders imposed as a control: entry is equal and above the floor at both strengths. At the weak strength, these orders are not optimal.” |
| Low | 19 | 783: “without recruitment the orders still predict the winner” | A strictly positive winner difference also needs full two-sided trade and `W_H > W_L`. The box states this condition; the title omits it. See `appendix/A8_empirical.tex:405–422`. | “With full informed orders and W_H greater than W_L, orders predict the winner even when entry stays at its floor.” |
| Low | 14 | 596: “exactly one equilibrium in each economy” | Proposition 2 states a unique equilibrium outcome. Its proof fixes the realized orders, beliefs, entry, prices and bids. Use the proposition's stated object. See `sections/04_equilibrium_results.tex:11–25`. | “Each bound holds for every candidate, so these conditions give a unique equilibrium outcome in each economy.” |
| Low | 14 | 572, 574: “a purchase brings the second buyer in”; “no order brings the second buyer in” | The zero-cost second buyer always prepares. Only additional, high-cost preparation responds to recruitment. See `sections/04_equilibrium_results.tex:25–44`. | “At F1, a purchase recruits the high-cost second buyer. At F2, no order recruits the high-cost second buyer.” |
| Low | 12 | 480: “every order costs k” | A nonzero order costs k. Abstention earns zero, as the same box states. See the investor payoff in `sections/02_model.tex` and the informed-trading lemma. | “Good synergy never lowers proceeds; each nonzero order costs k.” |
| Low | 11 | 469: “an order moves the belief” | A posterior can equal the prior. With full orders, no order leaves it at the prior; with abstention in both classes, every order does. See `appendix/A2_beliefs_trading.tex:43–45` and Proposition 2. | “Liquidity trade can copy every order, so an order can change the belief but never settles the synergy case.” |
| Low | 10 | 416: “takes part of the second buyer's gain ... and passes it” | Both comparative statics are weak. Either change can equal zero. Strictness needs the positive-integral conditions in Proposition 1. See `sections/03_competition_information.tex:25–41`. | “A stronger first buyer can transfer part of the buyer's profit gap to shareholders. Either change can be zero.” |
| Low | 16 | 661: “Given the case, the two buyers' values are unrelated.” | The displayed condition fixes the joint value law conditional on both case and signal as `G_j` times `F_i`. It also excludes further signal news within a class. See `appendix/A6_robustness.tex:8–11`. | “Given the case and signal, the values are independent and keep laws G_j and F_i. The signal adds no within-class value news.” |
| Low | 11 | 438: “Enough liquidity trade hides every order.” | Positive support hides every order for beta below one half. Beta at most one third also puts the zero order inside the same band. See `appendix/A2_beliefs_trading.tex:39–42, 64–71`. | “At beta at most one third, no order has less liquidity mass than a purchase or sale. The same band then covers no order.” |

## Coverage of the formal claims

| Frame | Result of the paper comparison |
|---:|---|
| 10 | The weak profit inequalities, ranked-class spread inequality and fixed class-gap identity agree with Proposition 1. The identity uses reserve admissibility. The picture illustrates the split; it does not prove strictness. |
| 11 | The definitions of b, u, m and M agree with the belief lemma. The all-order band needs beta at most one third. Price sufficiency uses positive spread and positive entry floor. The preparation threshold needs a positive buyer-profit gap. Equality induces preparation under the default rule. |
| 12 | K_H, K_L, kappa, the gross-gain bounds and all three comparisons with k agree with the informed-trading lemma. Wrong orders lose at least k. At a tie, the default investor rule permits a mixture. The bounds concern every stated profile, including a nonoptimal profile. |
| 13 | H1–H3, the distribution order, all three table rows, total entry and unique outcomes agree with Proposition 2. The open set fixes the example's class values and reserve. Beta below one half is valid here: the proof forces full orders through bounds at nonzero orders. It does not require the all-profile zero-order bound. |
| 14 | All four displayed proof steps agree with Appendix A.3. At F2, the comparison with B_2(M) concerns the resulting beliefs m, pi and M. The strict order comparisons force full orders before this entry comparison. The prose needs the corrections above. |
| 15 | The equivalence with the strict threshold band agrees with Corollary 1 for the listed fixed auction values, costs, strengths and prior. It is not an equivalence for arbitrary uniform families. All sixteen registry keys agree across both number files and the registry. |
| 16 | The formal joint-law conditions and the weak total-entry inequality agree with the fixed-information proposition. All three table rows agree with the example. The frozen-order row needs its control label at the weak strength. |
| 17 | The research cost, cap, beliefs, unique root, capped choice, existence conditions and three entry formulas agree with Proposition 4 and Appendix A.5. Total and good-synergy entry rise strictly with research; poor-synergy entry falls strictly. This uses beta below one half and interior rho. A unique root does not imply a unique equilibrium overall. |
| 18 | Both gain formulas and strict signs agree exactly with the price-access proposition at F1. The counterfactual hides both price and order. Both economies have full informed orders. Surplus excludes transfers and subtracts preparation costs. |
| 19 | Order frequencies, impact definitions, the weighted equivalence and the equal-frequency specialization agree with Appendix A.8. The winner gap equals rho times the posterior gap times the class win gap when entry stays at rho. Its strict sign needs W_H greater than W_L. |
| 20 | The price-content conclusion and conditional seller claim agree with the paper. The no-price sentence needs the fixed-information scope. The market claim concerns preparation, not a guaranteed second-buyer acquisition. |

Notation remains consistent with frames 5–9: R is first buyer value; theta is second buyer value; j is the synergy case.
The prior is pi; mu is an order posterior; rho is the zero-cost entry floor; k is the nonzero-order cost.
Entry e(x) is conditional on the order. Class entry e_j and total entry are averages over orders and costs.
Price sufficiency makes the price posterior equal to mu under its stated conditions. It does not reveal j.
Frame 17 makes the former presence probability lambda a research choice. All other notation keeps its earlier meaning.

## Numbers and strict comparisons

The registry is `audit/slot_manuscript_2026_10_23/registry/registry.csv`.
I compared each display below with both `overleaf/slot/numbers.tex` and the deck's `numbers.tex`.
There are no display discrepancies for these sixteen keys.

| Registry key | Display | Registry key | Display |
|---|---:|---|---:|
| prim_h | 10 | prim_ell | 1 |
| prim_p | 1/2 | prim_pi | 1/2 |
| prim_rho | 1/4 | prim_cH | 6 |
| prim_k | 1/50 | prim_r0 | 6/5 |
| prim_r1 | 3 | prim_r2 | 18/5 |
| tau_r1_frac | 141/200 | tau_r2_frac | 4245/5804 |
| tau_r1 | 0.705000 | tau_r2 | 0.731392 |
| M_half_B | 0.731059 | beta_B | 0.294655 |

Beta equals 294655/1000000 exactly. The footnote's 0.295 is its three-decimal rounding.
The exact top belief is Euler's number divided by one plus Euler's number.
It exceeds 141/200 and falls below 4245/5804. The strict comparison survives the six-decimal display.
The tick labels on the example's strength axis agree with the stated uniform family.

## Script update and verification

The script now follows the twenty main frames. Frames 1–9 retain their speech after cue removal.
Frame 7 adds the required outside-specialist sentence. Frames 10–20 use the new faces and the scope corrections above.
The prepared answers remain and include answers on research uniqueness, conditional price-access gains and the zero order.
Each displayed formula receives an oral reading, sometimes through a shared factor or previously defined object.

The retained first block ends at 16:00, including the title. The requested later times total 18 minutes.
The complete schedule therefore ends at 34:00 and leaves 11 minutes in a 45-minute slot.
The script contains 3,616 main-frame words, plus 50 title words: 3,666 prepared words in total.
The script's count table reports whitespace-delimited speech words. Headings, times, comments and prepared answers are excluded.
No tests or test suites were written or run. No slide or manuscript file was edited.

## Input record

- Deck source: `/home/uctpiaj/work/tmp/ccc-beamer30/slides.tex`.
- Source SHA-256: `31b27fbaa23ff79309bb5db0788f421af5825bce09042de992950e3c1765fbfa`.
- Deck PDF: `/home/uctpiaj/work/tmp/ccc-beamer30/slides.pdf`.
- PDF SHA-256: `25f38e7cd2ac3a5eec9b08bffd4752e8dd588bd33d40f5f560df53101ecf5518`.
- Registry SHA-256: `462de2dc3e7c964ced7d86a0aa45b7432fc66a2105b18f712b5cce881b2cf713`.
- Script: `/home/uctpiaj/work/tmp/ccc-main-slidepack/presentation/SLIDEPACK_30_SCRIPT.md`.
