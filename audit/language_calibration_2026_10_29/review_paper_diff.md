# Review of the paper terminology diff, 29 October 2026

Scope: the uncommitted diff in `overleaf/slot` for `main.tex`, `comparison.tex`, `sections/*.tex` and
`appendix/*.tex` (20 files, 591 insertions, 600 deletions). `slides.tex` and `slides_script.md` are out of
scope. Contract: `decisions.md` and `scan_paper.md` in this folder. This review is read-only. No source
file was changed.

Method:
1. I read the whole diff, hunk by hunk, as a word diff.
2. I compared the old and new text of each file for the items that must not change (see "Verified clean").
3. I searched each file for the old words and for the new compounds.

## Result

| Severity | Count |
|---|---|
| must-fix | 0 |
| should-fix | 5 |
| optional | 10 |

The swap is correct in meaning. No "rival" refers to the incumbent, and no "incumbent" refers to the
rival. No maths, key, macro, citation or comment changed. The should-fix items are names for the
incumbent that the pass did not touch, one stray short form, and two clumsy sentences.

## Findings

| # | file:line | Current text | Problem | Fix | Severity |
|---|---|---|---|---|---|
| 1 | `sections/01_introduction.tex:14` | "Incumbent strength is the public distribution of the prepared bidder's value" | "Prepared bidder" here means the incumbent. `decisions.md` lists "prepared buyer" as an old name of the incumbent, and the paper now also uses "a prepared rival". This sentence defines incumbent strength, so it should use the defined name. | "Incumbent strength is the public distribution of the incumbent's value" | should-fix |
| 2 | `sections/08_empirical.tex:13-15` | "a stronger prepared bidder can raise the probability that the rival prepares ... a stronger prepared bidder can only lower it. Against a strong enough prepared bidder, entry can return to its floor" | The same old name for the incumbent, three times. The paragraph title is "Entry and incumbent strength". | "a stronger incumbent can raise ... a stronger incumbent can only lower it. Against a strong enough incumbent, entry can return ..." | should-fix |
| 3 | `comparison.tex:273-274` | "a stronger prepared bidder can raise the probability of further preparation ... against a strong enough prepared bidder, preparation returns to its floor" | The same as item 2, in the note. | "a stronger incumbent can raise ... against a strong enough incumbent, preparation returns ..." | should-fix |
| 4 | `sections/01_introduction.tex:134` | "in this model, the potential rival learns about its own acquisition value" | A third form, neither the first-use name "potential rival bidder" nor the short name "rival". `decisions.md` uses "rival" after the first use. | "in this model, the rival learns about its own acquisition value" | should-fix |
| 5 | `sections/06_robustness.tex:79-82` | "the conditions cannot hold with a signal of the rival at least as accurate as that of the informed trader: the strong trading bound needs an accurate signal for the informed trader, and the weak bound then fails. The signal example meets the conditions with a more accurate signal for the rival at other costs and strengths." | The pass avoided "rival signal" correctly, but the sentence now has three different forms ("signal of", "that of", "signal for"). A possessive is allowed; only the noun adjunct is barred. | "the conditions cannot hold when the rival's signal is at least as accurate as the informed trader's: the strong trading bound needs an accurate signal for the informed trader, and the weak bound then fails. The signal example meets the conditions with the rival's signal more accurate, at other costs and strengths." | should-fix |
| 6 | `appendix/A8_empirical.tex:650` | "A path of strengths in \((\ell,h)\) has lowest value \(\ell\) of the rival and lowest strength above \(\ell\)" | The swap gives a broken order of words: "has lowest value ℓ of the rival". | "On a path of strengths in \((\ell,h)\), the lowest value of the rival is \(\ell\) and the lowest strength lies above \(\ell\)" | optional (appendix; meaning is clear) |
| 7 | `appendix/A6_robustness.tex:544`, `:514`, `:534`, `:563` | "\paragraph{A slot with a more accurate signal for the rival.}"; "the unfavorable signal of the rival never recruits"; "an uninformative signal for the rival"; "an accurate signal for the informed trader and a weak signal for the rival" | Correct, but "of" and "for" alternate. One form reads better. | Use the possessive: "A slot in which the rival's signal is more accurate."; "the rival's unfavorable signal never recruits"; "With the rival's signal uninformative"; "With an accurate signal for the informed trader and a weak one for the rival" (or keep "for" throughout). | optional |
| 8 | `sections/07_welfare.tex:69` | "the reserve lies below both values of the rival" | "Both values" was clear for "both challenger values" (the two point masses). With "of the rival" it can read as two values held at once. | "the reserve lies below both class values of the rival" | optional |
| 9 | `sections/03_competition_information.tex:5` | "the claim that informed traders trade" | Check 6 of the brief: "traders trade". No exact "the informed trader's trade" exists in the paper. | "the claim on which informed traders trade" or "the claim that informed traders buy and sell" | optional |
| 10 | `sections/04_equilibrium_results.tex:309`; `appendix/A5_research.tex:73` | "the informed trader trades fully at \(r_1\)"; "The informed trader trades only after a success" | The same collocation (also noted in `scan_paper.md`). It is grammatical. | Keep, or "the informed trader places full orders at \(r_1\)"; "The informed trader places an order only after a success". | optional |
| 11 | `sections/02_model.tex:166` | "The informed trader learns the class, the slot draw selects the informed trader with probability \(\lambda\)" | The long name now repeats in one clause pair. | "The informed trader learns the class, the slot draw selects it with probability \(\lambda\)" | optional |
| 12 | `sections/02_model.tex:190`; `appendix/A5_research.tex:614` | "For a known value \(\theta\) of the rival,"; "For any value \(\theta\ge p\) of the rival," | Correct. The math moved inside the phrase but is not changed. | Keep, or "When the rival's value \(\theta\) is known,". | optional |
| 13 | `comparison.tex:69-70` against `sections/02_model.tex:11-14` | "One bidder, the incumbent bidder or the incumbent, is already prepared. A second bidder, the potential rival bidder or the rival, has a class" | The definitions agree with `decisions.md`. The paper puts a comma before "or" ("the incumbent bidder, or the incumbent"); the note does not. Also, the note uses "potential rival bidder" at line 55 before this definition. | Add the comma for consistency. Line 55 can stay; it is in the summary paragraph. | optional |
| 14 | `sections/01_introduction.tex:155` | "The informed trader in this paper is an outsider and earns only the trading residual. In other work, an informed party can also hold a stake" | Correct and good: the examples (an acquirer, large holders, arbitrageurs) are not the model's informed trader, so "informed party" avoids check-1 misuse. "In other work" is a small addition outside the terminology table. | Keep. Note it for the author as a non-terminology edit. | optional |
| 15 | `sections/05_research.tex:75`; `sections/07_welfare.tex:15`; `appendix/A5_research.tex:213`; `sections/08_empirical.tex:57` | "the rivals who prepare"; "which high-cost rivals prepare"; "the class-\(H\) share of prepared rivals"; "prepared rivals" | The plural is over draws of the one rival. It follows the old "challengers" and reads correctly. | Keep. | optional |

## Remaining old words (check 4)

`grep -niE 'challenger|investor|buyer|specialist|entrant|prospective'` over the scope gives four hits. All four
stay:

| file:line | Text | Judgement |
|---|---|---|
| `sections/02_model.tex:31` | "the prepared party is a financial buyer" | Keep. Term of art (strategic and financial buyers); `scan_paper.md` item 16. |
| `sections/02_model.tex:36` | "outreach to potential buyers" | Keep. It reports the Imprivata proxy; acquirers outside the model. |
| `sections/02_model.tex:120` | "a liquidity purchase from an outside investor" | Keep. This is the liquidity side, not the informed trader. "Investor" now has only this sense in the paper, so the old ambiguity is gone. |
| `comparison.tex:56` | "The Laplace manuscript calls the rival the challenger and the informed trader the investor." | Keep. Correct: `overleaf/paper` uses "challenger" 155 times and "investor" 52 times. |

"Prepared bidder" sites that correctly stay, because they mean whichever bidder is prepared:
`appendix/A1_payoffs.tex:15`, `appendix/A1_payoffs.tex:43`, `sections/02_model.tex:101`, `comparison.tex:73`.
The sites in items 1 to 3 mean the incumbent and should change.

## Definitions and the content fix (check 5)

- Introduction, lines 3 to 11: "a stronger incumbent bidder reduces a potential rival bidder's expected return",
  then "The rival", then "The incumbent is already prepared". This names the actors and agrees with the rule that
  the introduction can name them.
- Section 2, lines 11 to 14: "one bidder is already prepared; I call it the incumbent bidder, or the incumbent.
  It is the party that approached the target or a bidder that has completed diligence ... A second bidder, the
  potential rival bidder, or the rival, has not decided whether to prepare." This follows the definition text in
  `decisions.md` nearly word for word. It is natural.
- Section 2, line 106: "The informed trader observes the rival's class j. It is an outside party, such as a
  sector-focused long-short fund." Line 21 gives the sector expertise once in words, as the rule asks.
- Content fix, `sections/02_model.tex:168-169`: "A rival that prepares learns its value. The incumbent and a
  prepared rival then submit their bids". This is correct. It agrees with line 52 (the incumbent "knows its value
  before it bids") and line 165 ("the incumbent knows its own value"). No other sentence in scope says that both
  bidders learn their values (`comparison.tex:73` says only that prepared bidders bid their values).

## Verified clean

- Meaning (check 1): no "rival" refers to the incumbent. The only old use of "rival" (`01_introduction.tex:5`,
  "a stronger rival lowers what that preparation earns", where "rival" meant the incumbent) became "stronger
  competition". This is a correct fix. No "rival + noun" compound reads as "competing": the only compound is the
  approved headline "rival entry" (`main.tex:77`, `01_introduction.tex:8`). Old compounds became possessives or
  "of the rival" ("rival's belief", "Beliefs of the rival", "tie rule for the rival").
- "Trader" alone: two sites, both correct. `02_model.tex:167` "the selected trader" is generic on purpose
  (`scan_paper.md`). `08_empirical.tex:83` "any trader's" is generic. "Informed trader" never means the liquidity
  side or an outside party in general.
- Non-prose content (check 3): a script compared old and new text of each file. These match exactly as
  multisets: inline and display maths, `$...$`, `align`/`equation`/`gather` bodies, `\label`, `\ref`/`\eqref`,
  `\hypertarget`, `\reg{...}` keys, citations, `\fixedlabel` arguments, environment names, macro names, `%`
  comments, and blank-line paragraph breaks. The only changes inside `tabular` bodies are visible words
  ("high-class rival", "The rival does not see the price", "Informed trader may mix").
- Grammar (check 2): no "a informed", "an rival" or "a incumbent"; no doubled words; every sentence-initial
  "A rival", "The rival" and "The informed trader" has a capital. The two article changes in `scan_paper.md`
  ("a specialist investor" -> "an informed trader", 02:21; "an investor strategy" -> "a strategy of the informed
  trader", 04:233) are correct.
- Some symbols keep the old initials: `\alpha_C`, `\alpha_I`, `S_C`, `S_I`, `\mu^C`, `M^I`. These are maths and
  are out of scope. Do not change them in this pass.

## Note for the implementer

The table headers are longer now ("Informed trader may mix", "Informed trader abstains" in
`appendix/A4_coexistence.tex:965`; "Informed trader's problem" in `comparison.tex:115`). Build the PDF once and
look at these two tables for overfull boxes. I did not build, because this review is read-only.
