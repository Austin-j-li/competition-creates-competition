# Terminology scan: order-slot paper

29 October 2026. Read-only scan of `overleaf/slot` (HEAD `eaf3049`, clean except `build/`). The contract is
`decisions.md` in this folder. Scope: `main.tex`, `sections/*.tex`, `appendix/*.tex`, `comparison.tex`. Line
numbers refer to that HEAD. Apply the edits from the bottom of each file to the top, or re-find each excerpt,
because the line numbers move after a rewrite.

## 1. Verdict on the decisions for this paper

The decisions work for the paper. Five points need care:

1. **"Rival" as a noun adjunct reads as "competing".** "both rival rules", "the rival value", "a rival
   signal", "rival beliefs", "rival quality", "a rival win" read as "competing rules", "competing value", and so
   on. The paper has 55 such sites with "challenger" and 29 with "investor". Do not swap them word for word.
   Use the possessive or an of-phrase (table 2B). "Rival entry" is safe and the decisions approve it. The paper
   uses no "challenger entry" phrase. It uses "the challenger's entry" once (intro:131-132).
2. **One existing "rival" means the incumbent.** intro:5 "a stronger rival lowers what that preparation earns".
   After the swap, the incumbent and the rival would share the word. Change it to "stronger competition" (item 3).
3. **Two "investor"/"informed trader" uses have a different sense. Do not apply the rule to them.**
   - 02:120 "a liquidity purchase from an outside investor": this is the liquidity buyer, not the informed
     actor. Keep "investor".
   - intro:155 "An informed trader can also hold a stake before a control decision": this is the generic
     literature sense. After the rename, it would refer to the model's actor. Rewrite it (item 11).
4. **"Trader" next to the liquidity trader.** The paper never shortens to "the trader" when it means the
   informed actor. "the selected trader" (02:167) is generic on purpose and stays. No other site is at risk if the
   implementer always writes the full "informed trader".
5. **No collisions in other words.** "Entrant": 0 uses. "Specialist": 6 uses, all the informed actor, all
   replaced (items 15, 20, 33, 34, 43). "Buyer": 23 uses; 21 change to "bidder", 2 stay (institutional). Other
   "informed" uses ("informed order", "informed trade", "informed presence", "the informed share",
   `sec:informed`, 02:150 "the informed holder's own sale" about Admati-Pfleiderer) agree with the new name and
   stay. "Entry" in the sense of a table cell occurs at 04:139, 05:142 and A9:60. These are outside the
   decisions. Optional: A9:60 "A negative entry marks" -> "A negative margin marks", because "entry" is a model
   term in a table of margins.

Headings and names:
- Section titles: only 03:70 has an actor word (item 28). No `\section` or `\subsection` contains "investor".
- Theorem, lemma, proposition, definition names: none contains "challenger", "investor" or "buyer".
  "[Strong incumbents]" (A5:561) and "[Informed trading]" (A2:190) stay.
- Run-in labels with an actor word: A1:32, A1:38, A4:482, A4:505, A6:544, 04:284 (items below).
- Macros: no `\newcommand` in `main.tex` or `comparison.tex` prints an actor word. `numbers.tex` has none.
  No index or glossary.
- Captions: no caption contains "challenger" or "investor". The caption of `tab:a4-ties` (A4:961-963)
  contains "investor" and changes mechanically.
- `references.bib`: no actor word in any title. The scanned `.tex` files contain no quotation of another
  author. Citation keys contain no actor word.
- Article changes: "a challenger" -> "a rival" keeps "a". "an investor" -> "an informed trader" keeps "an".
  Only two sites change the article: 02:22 "a specialist investor" -> "an informed trader" (item 15) and 04:233
  "an investor strategy" -> "a strategy of the informed trader" (item 30).
- Figures: see section 6. No disagreement.

## 2. Non-mechanical items

80 items in total. Items 9, 21, 26, 32 and 36 are mechanical; the list shows them because they are visible
or sensitive. The other 75 need judgement. 2A is the list of single edits (items 1-48). 2B holds the noun-adjunct sites (items 49-80,
grouped by pattern). Excerpts are verbatim; `→` gives the new text.

### 2A. Single edits

**main.tex (abstract)**

1. main.tex:77-78. `A stronger incumbent bidder can attract a challenger when it makes the target's stock price
   more informative. I study a takeover auction in which a prospective challenger sees the price before it pays
   to prepare a bid.` → `A stronger incumbent bidder can induce rival entry through a more informative stock
   price. I study a takeover auction in which a potential rival bidder sees the target's stock price before it
   pays to prepare a bid.` (This is the headline sentence of the decisions. The rest of the abstract is
   mechanical: 81 "high-class challenger" -> "high-class rival", 84 "indifferent investor" -> "indifferent
   informed trader".)

**sections/01_introduction.tex**

2. 01:3-9. The full paragraph is in section 4 (first use in the introduction).
3. 01:5 is part of item 2: `a stronger rival lowers` → `stronger competition lowers`.
4. 01:11. `One buyer is already prepared, and the challenger` → `The incumbent is already prepared, and the
   rival`. The rest of 01:11-15 is mechanical.
5. 01:27. `An outside specialist investor with no net position in the target knows the challenger's class` →
   `An outside informed trader with no net position in the target knows the rival's class`. (The text
   describes sector expertise once, at 02:22.)
6. 01:31. `Under every investor strategy` → `Under every strategy of the informed trader`.
7. 01:49. `Market makers anticipate` → `Competitive market makers anticipate` (first use of "market makers"
   in the paper; decisions table).
8. 01:106. `what a buyer pays when it wins` → `what a bidder pays when it wins`.
9. 01:122. `the informed investor's presence` → `the informed trader's presence` (rule M1; listed because it is
   the first "informed" + "investor" pair).
10. 01:135. `a prospective challenger learns about its own acquisition value` → `the potential rival learns
    about its own acquisition value`.
11. 01:155. `The investor in this paper is an outside trader and earns only the trading residual. An informed
    trader can also hold a stake before a control decision:` → `The informed trader in this paper is an
    outsider and earns only the trading residual. In other work, an informed party can also hold a stake before
    a control decision:`

**sections/02_model.tex**

12. 02:7-8. `before the buyer set is fixed; only then can a prospective buyer watch the price` → `before the set
    of bidders is fixed; only then can a further bidder watch the price` ("a further bidder" repeats 02:6).
13. 02:11-13. This is the definition paragraph. See section 4.
14. 02:14, 16, 17, 18. `before a buyer can submit` → `before a bidder can submit`; `differ across buyers` →
    `differ across bidders`; `the buyer's size` → `the bidder's size`; `for some buyers and expensive for
    others` → `for some bidders and expensive for others`.
15. 02:21-22. `The investor and the challenger know different things. The challenger knows its own integration
    plans, while a specialist investor can know` → `The informed trader and the rival know different things.
    The rival knows its own integration plans, while an informed trader with sector expertise can know`
    (the article changes; this is the one description of sector expertise).
16. 02:31-32. Keep `a financial buyer` (term of art: strategic and financial buyers, an institutional sense).
    Change `what either buyer would pay` → `what either bidder would pay`.
17. 02:36. Keep `outreach to potential buyers` (it reports the Imprivata proxy; acquirers outside the model).
18. 02:38. `whether prices draw buyers into that preparation stage` → `whether prices draw bidders into that
    preparation stage`.
19. 02:85. `a zero-cost challenger is a ready buyer` → `a zero-cost rival is a ready bidder`.
20. 02:106-107. `An investor observes the challenger's class \(j\). It is an outside sector specialist, such as
    a sector-focused long-short fund.` → `The informed trader observes the rival's class \(j\). It is an
    outside party, such as a sector-focused long-short fund.`
21. 02:112. `the informed investor fills the slot` → `the informed trader fills the slot` (rule M1).
22. 02:120. `a liquidity purchase from an outside investor` → **no change** (different sense; see section 1).
23. 02:139. `under every investor strategy` → `under every strategy of the informed trader`.
24. 02:163-170. This is the content fix. See section 5.
25. 02:190. `For a known challenger value \(\theta\)` → `For a known value \(\theta\) of the rival`.

**sections/03_competition_information.tex**

26. 03:5. `the claim that informed investors trade` → `the claim that informed traders trade` (rule M1).
    Optional, to avoid "traders trade": `the claim that informed traders buy and sell`.
27. 03:22. `the sensitivity of target proceeds to challenger quality` → `the sensitivity of target proceeds to
    the quality of the rival`.
28. 03:70. `\subsection{What the challenger learns from the price}` → `\subsection{What the rival learns from
    the price}` (keep `\label{sec:inference}`).
29. 03:76. `under every investor strategy` → `under every strategy of the informed trader`.

**sections/04_equilibrium_results.tex**

30. 04:233 (figure note). `the posteriors that an investor strategy can produce` → `the posteriors that a
    strategy of the informed trader can produce` (the article changes).
31. 04:284 (table panel head). `\emph{Panel C. The challenger does not see the price}` → `\emph{Panel C. The
    rival does not see the price}`.
32. 04:128-129 (table rows; mechanical, but visible table text). `Proceeds with a high-class challenger` →
    `Proceeds with a high-class rival`; `Proceeds with a low-class challenger` → `Proceeds with a low-class
    rival`.

**sections/05_research.tex**

33. 05:9. `It is the specialist's own work` → `It is the informed trader's own work`.
34. 05:12-13. `because the specialist uses cheap sources first` → `because the informed trader uses cheap
    sources first`.
35. 05:17. `After a failure, the investor knows no more than the market` → `After a failure, the informed
    trader knows no more than the market`. **Judgement:** the role name is kept although the actor holds no
    information after a failure. I recommend that you keep it, because the decisions make the name a fixed
    label. Show this sentence to the author.

**sections/06_robustness.tex**

36. 06:59. `while investors who follow the target` → `while informed traders who follow the target`.
37. 06:71. `With investor accuracy \(\alpha_I=...\) and challenger accuracy \(\alpha_C=...\)` → `With accuracy
    \(\alpha_I=...\) for the informed trader's signal and \(\alpha_C=...\) for the rival's signal`.
38. 06:80-82. `with a challenger signal at least as accurate as the investor's: the strong trading bound needs
    an accurate investor signal, and the weak bound then fails. The signal example meets the conditions with a
    more accurate challenger signal` → `with a signal of the rival at least as accurate as that of the informed
    trader: the strong trading bound needs an accurate signal for the informed trader, and the weak bound then
    fails. The signal example meets the conditions with a more accurate signal for the rival`.

**sections/07_welfare.tex**

39. 07:46. `a sale to the next buyer at its value` → `a sale to the next bidder at its value`.
40. 07:69. `the reserve lies below both challenger values` → `the reserve lies below both values of the rival`.

**sections/08_empirical.tex**

41. 08:30. `the lowest challenger value` → `the lowest value of the rival`.
42. 08:54. `covaries positively with a challenger win` → `covaries positively with a win by the rival`.
43. 08:90-91. `such as orders from sector specialists.` → `such as orders from sector-focused funds.` (In
    Glosten and Milgrom, "specialist" is the market intermediary.)

**sections/09_conclusion.tex**

44. 09:3. `the information that buyers have` → `the information that bidders have`.

**appendix/A7_welfare.tex**

45. A7:96, 116, 117, 124. `the next buyer at its value` → `the next bidder at its value`; `the buyer with the
    largest value` → `the bidder with the largest value`; `the next buyer's value` → `the next bidder's value`;
    `the next buyer accepts` → `the next bidder accepts`.

**comparison.tex**

46. comparison:51-55 and 67-69. These are the first-use definitions of the note. See section 4.
47. comparison:112 (table row head, column `L{3.1cm}`). `Investor's problem` → `Informed trader's problem`
    (can wrap to two lines; this is acceptable). comparison:115: `need no rule for the investor` → `need no
    tie rule for the informed trader`.
48. Optional, comparison:55. The note cites the Laplace manuscript ("Proposition L-2"), which keeps
    "challenger" and "investor". Add one sentence after the definition: `The Laplace manuscript calls the
    rival the challenger and the informed trader the investor.` I recommend it.

### 2B. Noun adjuncts (fixed phrase for each pattern)

"Tie rule" is the paper's own term (02:210-212). Use these forms only:

| # | Pattern | Replacement | Sites (file:line of the actor word) |
|---|---|---|---|
| 49 | `both challenger rules` | `both tie rules for the rival` | A2:101, A2:119, A5:142, A5:583, A6:346, A8:35, A8:73, A8:151, A8:536 |
| 50 | `both challenger tie rules` | `both tie rules for the rival` | A6:124 |
| 51 | `either challenger rule` | `either tie rule for the rival` | A4:210, A4:400, A4:419, A4:430, A4:437, A4:441, A4:909, A6:302, A6:456, A6:608, A8:339, A8:386, A8:500 |
| 52 | `either challenger tie rule` | `either tie rule for the rival` | A5:157, A5:484 |
| 53 | `the first challenger rule` | `the first tie rule for the rival` | A2:183 |
| 54 | `the challenger rule in use` | `the tie rule for the rival in use` | A4:153 |
| 55 | `The challenger rule matters` | `The tie rule for the rival matters` | A4:988 |
| 56 | `the chosen challenger tie rule` | `the chosen tie rule for the rival` | A6:421 |
| 57 | `a challenger tie` | `a tie for the rival` | A5:1092, A5:1096, A5:1155 |
| 58 | `both investor rules` | `both tie rules for the informed trader` | A3:25, A3:50, A5:141, A5:579, A6:485, A8:100, A8:199, A8:637 |
| 59 | `both investor tie rules` | `both tie rules for the informed trader` | A6:112 |
| 60 | `either investor rule` | `either tie rule for the informed trader` | A5:115 |
| 61 | A5:127 `Under either investor tie rule and either challenger tie rule` | `Under either tie rule for the informed trader and either tie rule for the rival` | A5:127 |
| 62 | A8:550-551 `under both investor rules and both challenger rules` | `under both tie rules for the informed trader and both tie rules for the rival` | A8:550 |
| 63 | A3:125 `Every investor comparison in Steps 1, 2 and 5` | `Every comparison of the informed trader in Steps 1, 2 and 5` | A3:125 |
| 64 | A5:1158 `the threshold pair survives investor abstention` | `the threshold pair survives the rule that an indifferent informed trader abstains` | A5:1158 |
| 65 | `Challenger beliefs.` (run-in, `\emph`) | `Beliefs of the rival.` | A1:32 |
| 66 | `Investor optimality.` (run-in, `\emph`) | `Optimality of the informed trader.` | A1:38 |
| 67 | `challenger beliefs:` (list item) | `beliefs of the rival:` | A4:686 |
| 68 | `the challenger belief \(\pi\)` | `the rival's belief \(\pi\)` | A7:27 |
| 69 | `for every challenger value.` | `for every value of the rival.` | A1:173 |
| 70 | `For any challenger value \(\theta\ge p\)` | `For any value \(\theta\ge p\) of the rival` | A5:614 |
| 71 | `the challenger value and the incumbent value` | `the rival's value and the incumbent's value` | A6:392 |
| 72 | `the lowest challenger value` / `has lowest challenger value \(\ell\)` | `the lowest value of the rival` / `has lowest value \(\ell\) of the rival` | A8:128, A8:654 |
| 73 | `Every challenger value is at least` | `Every value of the rival is at least` | A8:245 |
| 74 | `a challenger win` | `a win by the rival` | A8:598 |
| 75 | `either investor signal` / `each investor signal` / `the investor signal` | `either signal of the informed trader` / `each signal of the informed trader` / `the informed trader's signal` | A6:414, A6:471, A6:453 |
| 76 | `The two investor signals` | `The two signals of the informed trader` | A6:448 |
| 77 | `the unfavorable challenger signal` | `the unfavorable signal of the rival` | A6:514 |
| 78 | `an uninformative challenger signal` | `an uninformative signal for the rival` | A6:534 |
| 79 | `\paragraph{A slot with a more accurate challenger signal.}` | `\paragraph{A slot with a more accurate signal for the rival.}` | A6:544 |
| 80 | A6:563 `With an accurate investor signal and a weak challenger signal` and A6:571 `At a higher investor accuracy` | `With an accurate signal for the informed trader and a weak signal for the rival`; `At a higher accuracy of the informed trader's signal` | A6:563, A6:571 |

Table heads in A4:967 (`\multicolumn{2}{l}{Investor may mix}`, `{Investor abstains}`) take rule M4:
`Informed trader may mix`, `Informed trader abstains`. Check the table width after the build.

## 3. Mechanical rules and counts

Order of operations:
1. Apply sections 2A, 2B, 4 and 5 first. They rewrite text around the words.
2. **M1:** `informed investor` -> `informed trader`, `informed investors` -> `informed traders`, `informed
   investor's` -> `informed trader's`. Match across `~` and line breaks (`informed\s+investor`). Apply this
   before M2, or the result is "informed informed trader". 12 sites: 01:122, 02:112, 03:5, 03:74, 08:6, 08:38,
   A1:18, A7:73, A8:357, A8:377, comparison:52, comparison:82.
3. **M2:** `investor's` -> `informed trader's`; `investors` -> `informed traders`; `investor` -> `informed
   trader`. Exception: 02:120. The article does not change ("an investor" -> "an informed trader").
4. **M3:** `Investor` (capital) -> `Informed trader`. The only remaining sites are the A4:967 table heads.
   comparison:112 and A1:38 are in section 2.
5. **M4:** `challenger's` -> `rival's`; `challengers` -> `rivals`; `challenger` -> `rival`. The article
   does not change. No sentence-initial `Challenger` remains after item 65. There are no `challengers'` forms.
6. **Buyer:** no mechanical rule. All 23 sites are in items 1-48. 21 change to "bidder". 2 stay: 02:31
   "financial buyer" and 02:36 "potential buyers".
7. **Incumbent:** no change except the definition (section 4). "Incumbent strength", "uniform incumbent" and
   "incumbent distribution" stay.

Raw counts at HEAD (all forms; the exceptions above are inside these totals):

| File | challenger | challenger's | challengers | Challenger | investor (all lc forms) | of which informed investor | investor's | investors | Investor | buyer |
|---|---|---|---|---|---|---|---|---|---|---|
| main.tex | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 01_introduction | 25 | 9 | 0 | 0 | 16 | 1 | 5 | 0 | 0 | 4 |
| 02_model | 28 | 10 | 0 | 0 | 22 | 1 | 4 | 0 | 0 | 13 |
| 03_competition_information | 19 | 4 | 0 | 0 | 8 | 2 | 4 | 1 | 0 | 0 |
| 04_equilibrium_results | 25 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| 05_research | 8 | 1 | 1 | 0 | 14 | 0 | 3 | 0 | 0 | 0 |
| 06_robustness | 8 | 4 | 0 | 0 | 6 | 0 | 3 | 1 | 0 | 0 |
| 07_welfare | 9 | 1 | 1 | 0 | 3 | 0 | 1 | 0 | 0 | 1 |
| 08_empirical | 10 | 2 | 1 | 0 | 3 | 2 | 3 | 0 | 0 | 0 |
| 09_conclusion | 1 | 4 | 0 | 0 | 4 | 0 | 1 | 0 | 0 | 1 |
| A1_payoffs | 15 | 2 | 0 | 1 | 3 | 1 | 0 | 0 | 1 | 0 |
| A2_beliefs_trading | 11 | 4 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 |
| A3_proposition2 | 16 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| A4_coexistence | 39 | 1 | 0 | 0 | 47 | 0 | 0 | 0 | 2 | 0 |
| A5_research | 30 | 1 | 1 | 0 | 22 | 0 | 0 | 0 | 0 | 0 |
| A6_robustness | 22 | 4 | 0 | 0 | 14 | 0 | 0 | 0 | 0 | 0 |
| A7_welfare | 12 | 6 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 4 |
| A8_empirical | 59 | 3 | 0 | 0 | 25 | 2 | 1 | 0 | 0 | 0 |
| A9_parameters | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| comparison.tex | 13 | 6 | 0 | 0 | 12 | 2 | 2 | 0 | 1 | 0 |
| **Total** | **354** | **62** | **4** | **1** | **217** | **12** | **27** | **2** | **4** | **23** |

"challenger" in all forms: 421. "investor" in all forms: 221. "incumbent": 281 (no change). "investor (all lc
forms)" includes the possessive and plural columns.

Optional style note (no action required): M2 produces "the informed trader trades" at 04:309 and A5:73. This is
acceptable.

Acceptance checks after the edits (run them as a reader of the files, not as a test suite):
- `grep -n -i 'challenger\|specialist' main.tex sections/*.tex appendix/*.tex comparison.tex` returns
  nothing. If item 48 is applied, it returns only that sentence.
- `grep -n -i 'investor' ...` returns only 02:120 (plus item 48 if applied).
- `grep -n -i 'buyer' ...` returns only 02:31 and 02:36.
- `perl -0ne 'print "$ARGV: $&\n" while /\brivals?\s+(rules?|tie|signals?|values?|quality|accuracy|beliefs?|belief|win)\b/g' main.tex sections/*.tex appendix/*.tex comparison.tex` returns nothing.
- `grep -n 'informed informed' ...` returns nothing.
- Build `main.tex` and `comparison.tex` with `latexmk -pdf` and look at Table A.3 (A4:961) and the
  comparison table `tab:setups`.

## 4. First-use definitions

### Introduction, 01:3-9

Current:
> At fixed information, a stronger incumbent reduces a prospective challenger's expected return from entry into a
> takeover contest. The challenger must pay preparation costs before it can submit an executable offer, and a
> stronger rival lowers what that preparation earns \citep{Fishman1988,HirshleiferPng1989}. I study a force in
> the opposite direction. Competition can make the target's stock more informative about the challenger, and when a
> potential buyer observes that price before it commits to acquisition preparation, the information effect can
> outweigh the loss of acquisition profits. A stronger incumbent can then attract another buyer and raise the
> probability that a challenger from the high class acquires the target.

Replacement:
> At fixed information, a stronger incumbent bidder reduces a potential rival bidder's expected return from entry
> into a takeover contest. The rival must pay preparation costs before it can submit an executable offer, and
> stronger competition lowers what that preparation earns \citep{Fishman1988,HirshleiferPng1989}. I study a force
> in the opposite direction. Competition can make the target's stock more informative about the rival, and when the
> rival observes that price before it commits to acquisition preparation, the information effect can outweigh the
> loss of acquisition profits. A stronger incumbent can then induce rival entry and raise the probability that a
> rival from the high class acquires the target.

### Section 2, 02:11-13

Current:
> Within the interval, one buyer is already prepared. It is the party that approached the target or a
> bidder that has completed diligence, and its strength is what the public can infer about its acquisition
> value from the disclosed record. Another buyer, the challenger, has not decided whether to prepare. Preparation is required
> for an executable proposal: before a buyer can submit a binding offer, ...

Replacement:
> Within the interval, one bidder is already prepared; I call it the incumbent bidder, or the incumbent. It is the
> party that approached the target or a bidder that has completed diligence, and its strength is what the public
> can infer about its acquisition value from the disclosed record. A second bidder, the potential rival bidder, or
> the rival, has not decided whether to prepare. Preparation is required for an executable proposal: before a
> bidder can submit a binding offer, ...

The informed trader takes its Section 2 description at 02:21-22 (item 15) and 02:106-107 (item 20). "Competitive
market makers" is already the first use in Section 2 (02:124).

### comparison.tex, 51-55 and 67-69

Current (51-55):
> In the order slot, the trading stage of the paper, an informed investor and a liquidity trader are alternative
> arrivals in one public order opportunity. In the Laplace set-up, the investor chooses a continuous order and
> Laplace noise hides it; ... The auction, the preparation cost and the challenger's decision are the same in both.

Replacement:
> In the order slot, the trading stage of the paper, an informed trader and a liquidity trader are alternative
> arrivals in one public order opportunity. In the Laplace set-up, the informed trader chooses a continuous order
> and Laplace noise hides it; ... The auction, the preparation cost and the decision of the potential rival bidder
> are the same in both.

Current (67-69):
> \paragraph{Shared primitives.} A challenger of class \(j\in\{H,L\}\), with prior \(\pi=\Pr(j=H)\), has a value
> \(\theta\sim G_j\). ... The incumbent's value is \(R\sim F\). The challenger's preparation cost is ...

Replacement:
> \paragraph{Shared primitives.} One bidder, the incumbent bidder or the incumbent, is already prepared. A second
> bidder, the potential rival bidder or the rival, has a class \(j\in\{H,L\}\), with prior \(\pi=\Pr(j=H)\), and a
> value \(\theta\sim G_j\). ... The incumbent's value is \(R\sim F\). The rival's preparation cost is ...

## 5. Content fix: when the bidders learn their values

The scanned files state this sequence in **one** place only: 02:169. Other statements agree with the
decisions and need no change:
- 02:19, 02:77 and 02:86 say that payment reveals the rival's value.
- 02:51-52 says that the incumbent knows its value before it bids.
- 02:165 says that the incumbent knows its own value.
- comparison:70 says that prepared bidders bid their values. It makes no claim about learning.
- A7:94 says that values are verifiable after diligence. It makes no claim about learning.

Current, 02:163-170 (with the renames applied in the first part):
> ... Market makers set the price from the order, and the challenger observes the price and its cost and decides
> whether to prepare. Prepared bidders then learn their values and submit their bids, and ownership and financial
> payoffs are realized. Section~\ref{sec:research} adds a research stage before the investor learns the class.

Replacement, full passage 02:163-170:
> Market makers observe the order \(X\) and nothing else. The rival observes the price \(P\) and its own
> cost \(C\), but not \(X\), its class, its value, or the incumbent's value; the informed trader observes the class
> \(j\) but not the value \(\theta\), and the incumbent knows its own value. The sequence is as follows. The
> seller announces the sale rule. The informed trader learns the class, the slot draw selects the informed trader
> with probability \(\lambda\) and a liquidity trader otherwise, and the selected trader places its order. Market
> makers set the price from the order, and the rival observes the price and its cost and decides whether to
> prepare. A rival that prepares learns its value. The incumbent and a prepared rival then submit their bids, and
> ownership and financial payoffs are realized. Section~\ref{sec:research} adds a research stage before the
> informed trader learns the class.

Outside this scan: `slides.tex:172` ("The second buyer pays to learn its value before it can bid") is correct on
the timing. It still uses "buyer".

## 6. Words in figures

`figures/beliefs.pdf`, `coexistence.pdf`, `research.pdf` and their `_talk` versions (pdftotext): the only actor
word is "incumbent strength, r". The other labels are "preparation threshold", "entry", "top posterior",
"recruiting research" and similar. The figure script
`audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py` has no "challenger", "investor" or "buyer"
label. No figure disagrees with the new words, and no figure needs a rebuild. (The Laplace-era renderer
`numerics/render/figures.py:254, 361` has "challenger gross profit" and "challenger profit". These labels do not
appear in any `overleaf/slot` figure. Leave them.)
