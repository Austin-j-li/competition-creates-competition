# Terminology scan of the order-slot slide deck

29 October 2026. Read-only scan. No source file was changed.

Files: `overleaf/slot/slides.tex` (1565 lines, at commit `eaf3049`), `overleaf/slot/slides_script.md` (359 lines),
`overleaf/slot/ccc-journal.sty` (183 lines). Rendered check: `overleaf/slot/build/slides.pdf` (56 pages).
Contract: `decisions.md` in this folder.

Scan facts:
- `ccc-journal.sty` has no visible actor words. The model strip prints "Players, Timing, Information,
  Actions, Payoffs, Equilibrium". The style file needs no change.
- "challenger" and "incumbent" have zero occurrences in `slides.tex` and in the script.
- "rival" matches lines 1020 and 1378 only as part of "arrival" ("Alternative arrival: Dow and Gorton").
  Do not run a blind `rival` substitution or a blind `rival` count.
- The rendered PDF and the source give the same term counts, apart from words that pdftotext splits at a
  line end. No macro prints an actor word that the source does not show.
- The figure files under the `\FigCover` patches already print "incumbent strength, r". The slide overlays
  print "first buyer's strength, $r$" over them.
- The last build log (`build/slides.log`) has no overfull box.

## 1. Verdict on the decisions

**Incumbent / rival.** The decisions work in this deck. No existing word collides with them. The only
existing "rival" is in backup B14 (lines 1457, 1459), and it already has the new sense. "Incumbent
strength" is already the axis name inside the three figure files. The locked strength words read
naturally with the new noun: "the weak / strong / very strong incumbent". One rule for the implementer:
use "the rival" for the single actor. Use "a rival" only where the text describes a case ("a rival with
$C=0$", "a prepared rival", "an indifferent rival"). Frames 1 to 4 use the names before frame 5 defines them.
Keep the formal definition on frame 5. The frame 1 title and the "Rival" column head ("Preparation costs
money before a bid is possible") explain the words well enough for an opening frame.

**Bidder.** No collision. The deck title already says "Takeover Bidders". Line 898 ("two admissible
bidders") and line 1459 ("bidders learn from prices after a bid") already use the model sense. The change
removes a present ambiguity: "buyer" names an acquirer, but "buys" and "purchase" name a stock order of the
informed trader. After the change, "buy" means a stock order only. The frame 1 footer (line 163) cites Bulow
and Klemperer. Their own word is "bidder", so change it to "bidder" there too. No sentence in the deck
needs "buyer" in the outside-model sense.

**Informed trader.** The new name is safe. A liquidity trader is in the same passage on frame 5 (line 236),
frame 6, frame 7, and backup B7. Never shorten to "trader" there. The deck never uses "trader" alone. The
script uses "trader" alone twice (lines 113, 133), in the generic sense "whoever filled the slot". Keep
those. The removal of "specialist" (line 907) also removes a clash with the Glosten and Milgrom citation in
the B7 footer (line 1020), where "specialist" is the intermediary. Where the deck uses "investor" as an
adjective, use the existing adjectival terms "informed trade" (line 775) and "informed presence" (line 1425).
Do not write "informed-trader trade".

**Rival gross profit (judgement).** The deck locks the object name "second-buyer gross profit $B(\mu)$"
(header line 10). Under the compound rule ("challenger entry -> rival entry"), it becomes **rival gross
profit**. Use that name everywhere, about 20 times. The short table and title form "Buyer profit" becomes
**Rival profit** (lines 331, 1054, 1147, 1257 to 1259). Use the possessive only for things that the rival
holds: "the rival's value", "the rival's belief", "the rival's signal".

**Entry and entrant.** "Entry" keeps its present meaning (the preparation probability). Do not change it.
"Entrant" appears once, at line 1041, as "the entrant claim". Change it to "the rival's claim".

**Market makers.** The first visible use is on frame 5 (line 236), not frame 6. Put "competitive market
makers" there. Line 266 already says "Competitive market makers"; keep it.

## 2. Replacement tables

Mapping: first buyer -> incumbent; second buyer -> rival; second-buyer X -> rival X; first-buyer
strength -> incumbent strength; (informed) investor -> informed trader; buyer (model) -> bidder.
"keep" rows contain a listed word that needs no change.

### 2a. `slides.tex`, visible text

| Line | Frame | Current (excerpt) | Proposed |
|---:|---|---|---|
| 56 | S8 (macro `\SplitLine`) | `{second buyer's value $\theta$}` | `{rival's value $\theta$}` |
| 78 | S10 (macro `\GapLine`) | `{first buyer's value moves right}` | `{incumbent's value moves right}` |
| 82 | S10 (macro `\GapLine`) | `{second buyer's part}` | `{rival's part}` |
| 106 | S14 figure overlay | `first buyer's strength, $r$` | `incumbent strength, $r$` |
| 124 | S14 figure overlay | `first buyer's strength, $r$` | `incumbent strength, $r$` |
| 130 | B3b figure overlay | `first buyer's strength, $r$` | `incumbent strength, $r$` |
| 132 | B3b figure overlay | `first buyer's strength, $r$` | `incumbent strength, $r$` |
| 150 | S1 title | `Does a stronger first buyer always keep the second buyer out?` | `Does a stronger incumbent always keep the rival out?` |
| 156 | S1 | `must find a second buyer. A stronger first buyer can help find one` | `must find a rival bidder. A stronger incumbent can help find one` |
| 158 | S1 column head | `\ColHead{Second buyer}` | `\ColHead{Rival}` |
| 163 | S1 footer | `One extra buyer can change sale proceeds` | `One extra bidder can change sale proceeds` |
| 168 | S2 subtitle | `When what the second buyer can learn stays fixed` | `When what the rival can learn stays fixed` |
| 172 | S2 | `The second buyer pays to learn its value` | `The rival pays to learn its value` |
| 173 | S2 | `A stronger first buyer weakly cuts its expected auction profit` | `A stronger incumbent weakly cuts the rival's expected auction profit` (see 4: "its" now points at the incumbent) |
| 191 | S3 table | `The decision is second-buyer preparation` | `The decision is rival preparation` |
| 192 | S3 table | `Price news can rise with first-buyer strength` | `Price news can rise with incumbent strength` |
| 193 | S3 table | `Outside investor, no initial position, no target control` | `Outside informed trader, no initial position, no target control` |
| 196 | S3 takeaway | `An outside investor can put ... First-buyer strength can raise` | `An outside informed trader can put ... Incumbent strength can raise` |
| 201 | S4 title | `a stronger first buyer can recruit the second` | `a stronger incumbent can recruit the rival` |
| 204 | S4 large line | `A stronger first buyer weakly cuts the second buyer's profit ... recruit the second buyer.` | `A stronger incumbent weakly cuts the rival's profit ... recruit the rival.` |
| 207 | S4 | `from the weak to the strong first buyer` | `from the weak to the strong incumbent` |
| 208 | S4 | `strength weakly cuts second-buyer profit` | `strength weakly cuts rival profit` |
| 209 | S4 | `a stronger first buyer cannot raise entry` | `a stronger incumbent cannot raise entry` |
| 212 | S4 | `Extensions: costly investor research;` | `Extensions: costly research by the informed trader;` |
| 228 | S5 | `\DefRow{First buyer}{\textbf{already prepared:} ... faces no preparation choice.` | see 3 |
| 229 | S5 | `\DefRow{Second buyer}{\textbf{synergy class:} ...` | see 3 |
| 230 | S5 | `The sale and the second buyer's identity are public` | `The sale and the rival's identity are public` |
| 231 | S5 | `a second buyer who does not pay cannot bid` | `a rival who does not pay cannot bid` |
| 236 | S5 footer | `Neither buyer trades ... informed investor, liquidity trader, market makers.` | `Neither bidder trades ... informed trader, liquidity trader, competitive market makers.` |
| 255 | S6 timeline | `Market makers set $P(X)$` | keep |
| 256 | S6 timeline | `Second buyer sees $P$, learns $C$, prepares or stays out` | `Rival sees $P$, learns $C$, prepares or stays out` |
| 257 | S6 timeline | `Prepared buyer learns $\theta$; bids; payoffs` | `Rival, if prepared, learns $\theta$; bids; payoffs` (content fix, see 5) |
| 264 | S6 | `the slot goes to an outside informed investor` | `the slot goes to an outside informed trader` |
| 266 | S6 | `Competitive market makers ... holds the second buyer's entry response` | `Competitive market makers` keep; `holds the rival's entry response` |
| 281 | S7 table | `First buyer & its value $R$` | `Incumbent & its value $R$` |
| 282 | S7 table | `Informed investor (slot with prob.\ $\lambda$)` | `Informed trader (slot with prob.\ $\lambda$)` |
| 284 | S7 table | `Market makers & outcome $X$` | keep |
| 285 | S7 table | `Second buyer & price $P$ ...` | `Rival & price $P$ ...` |
| 293 | S7 | `the second buyer's belief` | `the rival's belief` |
| 302 | S8 | `\SplitLine{6.2}{first buyer's value $R$}` | `\SplitLine{6.2}{incumbent's value $R$}` |
| 305 | S8 | `Fix a prepared second buyer ... the second buyer's gross profit is` | `Fix a prepared rival ... the rival's gross profit is` |
| 306 | S8 | `With no second-buyer entry, the first buyer alone pays $p$` | `With no rival entry, the incumbent alone pays $p$` |
| 307 | S8 | `if the second buyer prepares. \textbf{Second-buyer gross profit}` | `if the rival prepares. \textbf{Rival gross profit}` |
| 308 | S8 | `The informed investor with order $q$` | `The informed trader with order $q$` |
| 318 | S9 | `competitive market makers` | keep |
| 321 | S9 | `that the second buyer prepares ... An investor who sees class $j$ ... the investor puts` | `that the rival prepares ... An informed trader who sees class $j$ ... the informed trader puts` |
| 323 | S9 | `The second buyer's price belief` | `The rival's price belief` |
| 324 | S9 | `a second buyer with $C=0$ ... A prepared second buyer bids $\theta$; the first buyer bids $R$` | `a rival with $C=0$ ... A prepared rival bids $\theta$; the incumbent bids $R$` |
| 331 | S10 title | `Strength never raises buyer profit and never narrows the spread` | `Strength never raises rival profit and never narrows the spread` |
| 336 | S10 | `continuous first-buyer distributions` | `continuous incumbent value distributions` |
| 338 | S10 gloss | `The new first buyer draws high values more often.` | `The new incumbent draws high values more often.` |
| 365 | S10 intuition | `A stronger first buyer can move part of the second buyer's gain` | `A stronger incumbent can move part of the rival's gain` |
| 401 | S11 gloss | `second-buyer gross profit equals the high cost` | `rival gross profit equals the high cost` |
| 403 | S11 gloss | `A second buyer at the threshold prepares.` | `A rival at the threshold prepares.` |
| 440 | S12 | `The investor who sees class $H$ buys` | `The informed trader who sees class $H$ buys` |
| 441 | S12 | `The investor who sees class $L$ sells` | `The informed trader who sees class $L$ sells` |
| 501 | S13 intuition | `pays the informed investor to trade` | `pays the informed trader to trade` |
| 519 | S14 | `The first buyer has $R\sim...$; a larger $r$ means a stronger first buyer.` | `The incumbent has $R\sim...$; a larger $r$ means a stronger incumbent.` |
| 530 | S14 intuition | `Against the strong first buyer, a purchase lifts` | `Against the strong incumbent, a purchase lifts` |
| 545 | S15 | `the signal $S$ that the second buyer observes` | `the signal $S$ that the rival observes` |
| 550 | S15 gloss | `What the second buyer can learn does not change.` | `What the rival can learn does not change.` |
| 553 | S15 | `Let an indifferent second buyer prepare.` | `Let an indifferent rival prepare.` |
| 574 | S15 | `the second buyer still reads the stock price` | `the rival still reads the stock price` |
| 576 | S15 intuition | `a stronger first buyer only lowers the profit` | `a stronger incumbent only lowers the profit` |
| 586 | S16 | `The investor now chooses presence` | `The informed trader now chooses presence` |
| 592 | S16 | `An indifferent investor may mix; an indifferent high-cost second buyer prepares.` | `An indifferent informed trader may mix; an indifferent high-cost rival prepares.` |
| 597 | S16 | `the investor who learns class $H$ buys after success` | `the informed trader who learns class $H$ buys after success` |
| 620 | S17 | `Hold the first buyer at $F_1$ (strong)` | `Hold the incumbent at $F_1$ (strong)` |
| 621 | S17 | `an economy where the second buyer sees neither` | `an economy where the rival sees neither` |
| 634 | S17 intuition | `The high-cost second buyer then prepares` | `The high-cost rival then prepares` |
| 664 | S18 | `(the investor who sees class $H$ buys; the investor who sees class $L$ sells)` | `(the informed trader who sees class $H$ buys; the informed trader who sees class $L$ sells)` |
| 665 | S18 gloss | `second-buyer gross profit falls short of $c_H$` | `rival gross profit falls short of $c_H$` |
| 688 | S19 large line | `A stronger first buyer can bring in the second buyer through the stock price.` | `A stronger incumbent can induce rival entry through a more informative stock price.` (headline sentence) |
| 691 | S19 | `Entry rises against the strong first buyer` | `Entry rises against the strong incumbent` |
| 692 | S19 | `cuts second-buyer gross profit ... Freeze what the second buyer can learn` | `cuts rival gross profit ... Freeze what the rival can learn` |
| 693 | S19 | `At the strong first buyer, a visible price` | `At the strong incumbent, a visible price` |
| 709 | B1 | `The first buyer's value law $F$` | `The incumbent's value law $F$` |
| 710 | B1 | `With $B_i$ second-buyer gross profit` | `With $B_i$ rival gross profit` |
| 712 | B1 | `a prepared second buyer in case $j$ ... share of second-buyer wins` | `a prepared rival in case $j$ ... share of rival wins` |
| 725 | B2 | `second-buyer gross profit rises ... an indifferent high-cost second buyer may prepare` | `rival gross profit rises ... an indifferent high-cost rival may prepare` |
| 738 | B2b | `second-buyer gross profit there ... second-buyer gross profit at $M(\pi)$` | `rival gross profit there ... rival gross profit at $M(\pi)$` |
| 775 | B3 | `Uninformative market: no informed-investor trade` | `Uninformative market: no informed trade` |
| 777 | B3 | `while the informed investor mixes ... once the informed investor buys` | `while the informed trader mixes ... once the informed trader buys` |
| 801 | B3b | `where the informed investor buys for sure` | `where the informed trader buys for sure` |
| 824 | B3c table | `the informed investor sells for certain` | `the informed trader sells for certain` |
| 849 | B4 | `At the strong first buyer $F_1$` | `At the strong incumbent $F_1$` |
| 851 | B4 | `informed investor orders stay full` | `informed trader orders stay full` |
| 883 | B4b | `excludes poor synergy and the weak first buyer` | `excludes poor synergy and the weak incumbent` |
| 898 | B4b | `two admissible bidders` | keep |
| 903 | B5 title | `Who the informed investor is` | `Who the informed trader is` |
| 907 | B5 | `The informed investor is an outside sector specialist.` | `The informed trader is an outsider with sector expertise.` |
| 908 | B5 | `the second buyer's synergy class` | `the rival's synergy class` |
| 909 | B5 | `the second buyer's value` | `the rival's value` |
| 910 | B5 | `Neither buyer trades target shares. The informed investor stands outside` | `Neither bidder trades target shares. The informed trader stands outside` |
| 927 | B6 table | `For uniform first buyers, an open set` | `For uniform incumbent values, an open set` |
| 929 | B6 table | `Second buyer has its own signal & ... the second buyer's accuracy ... the informed investor's accuracy` | `Rival has its own signal & ... the rival's accuracy ... the informed trader's accuracy` |
| 949 | B6b | `at suitable uniform first buyers and costs` | `at suitable uniform incumbent values and costs` |
| 951 | B6b | `without the second buyer's signal` | `without the rival's signal` |
| 1005 | B7 box | `\textbf{\sffamily Informed investor}` | `\textbf{\sffamily Informed trader}` |
| 1008 | B7 box | `\textbf{\sffamily Market makers}` | keep |
| 1009 | B7 box | `\textbf{\sffamily Second buyer}` | `\textbf{\sffamily Rival}` |
| 1020 | B7 footer | `Alternative arrival` | keep (substring of "arrival") |
| 1029 | B8 | `Take a prepared second buyer ... The first buyer pays $\theta$ when it wins.` | `Take a prepared rival ... The incumbent pays $\theta$ when it wins.` |
| 1034 | B8 | `averages over the first buyer's value $R\sim F$` | `averages over the incumbent's value $R\sim F$` |
| 1038 | B8 | `expected second-buyer gross profit is` | `expected rival gross profit is` |
| 1039 | B8 | `A good-synergy second buyer outbids $F$` | `A good-synergy rival outbids $F$` |
| 1041 | B8 takeaway | `The traded claim and the entrant claim sum` | `The traded claim and the rival's claim sum` |
| 1054 | B8s | `Buyer profit $B(\mu)$ weakly falls` | `Rival profit $B(\mu)$ weakly falls` |
| 1056 | B8s | `with second buyer's value $\theta$` | `with the rival's value $\theta$` |
| 1060 | B8s | `target proceeds and second-buyer gross profit` | `target proceeds and rival gross profit` |
| 1087 | B9 | `when second-buyer gross profit $B(...)>c_H$` | `when rival gross profit $B(...)>c_H$` |
| 1089 | B9 | `maximizes the class-$j$ investor payoff $U_j(q)=...$` | `maximizes the informed trader's class-$j$ payoff $U_j(q)=...$` |
| 1090 | B9 | `each prepared buyer with value at or above reserve $p$` | `each prepared bidder with value at or above reserve $p$` |
| 1091 | B9 | `an indifferent informed investor may mix ... an indifferent second buyer at cost $c_H$ ... informed investor abstains, or an indifferent second buyer` | `an indifferent informed trader may mix ... an indifferent rival at cost $c_H$ ... informed trader abstains, or an indifferent rival` |
| 1147 | B11 table | `Buyer profit at the prior, $B_r(...)$` | `Rival profit at the prior, $B_r(...)$` |
| 1149 | B11 table | `Informed investor orders (good synergy, poor synergy)` | `Informed trader orders (good synergy, poor synergy)` |
| 1155 | B11 takeaway | `second-buyer gross profit falls ... against the strong first buyer` | `rival gross profit falls ... against the strong incumbent` |
| 1166 | B11s | `A stronger first buyer cannot raise entry.` | `A stronger incumbent cannot raise entry.` |
| 1168 | B11s | `between second-buyer gross profit at the two strengths` | `between rival gross profit at the two strengths` |
| 1178 | B11s table | `Second buyer cannot see the price` | `Rival cannot see the price` |
| 1195 | B11f | `with second-buyer gross profit $B_i$ at $F_i$` | `with rival gross profit $B_i$ at $F_i$` |
| 1199 | B11f | `The second buyer still reads the stock price` | `The rival still reads the stock price` |
| 1227 | B11c | `a good-synergy second buyer faces ... a poor-synergy second buyer with chance $b$` | `a good-synergy rival faces ... a poor-synergy rival with chance $b$` |
| 1254 | B11c table | `Proceeds with a good-synergy second buyer, $t_H$` | `Proceeds with a good-synergy rival, $t_H$` |
| 1255 | B11c table | `Proceeds with a poor-synergy second buyer, $t_L$` | `Proceeds with a poor-synergy rival, $t_L$` |
| 1257 | B11c table | `Buyer profit, good synergy, $g_H$` | `Rival profit, good synergy, $g_H$` |
| 1258 | B11c table | `Buyer profit, poor synergy, $g_L$` | `Rival profit, poor synergy, $g_L$` |
| 1259 | B11c table | `Buyer profit at the prior, $B_r(...)$` | `Rival profit at the prior, $B_r(...)$` |
| 1293 | B11d table | `Panel C. The second buyer does not see the price` | `Panel C. The rival does not see the price` |
| 1308 | B12 | `the informed investor picks research` | `the informed trader picks research` |
| 1310 | B12 | `More research adds informed investor orders` | `More research adds informed trader orders` |
| 1321 | B12 takeaway | `More research brings more good-synergy buyers in.` | `More research brings in a good-synergy rival more often.` (judgement: one rival, so no plural) |
| 1374 | B12d | `in which the informed investor trades in both` | `in which the informed trader trades in both` |
| 1375 | B12d | `(the informed investor buys on good synergy` | `(the informed trader buys on good synergy` |
| 1378 | B12d | `with an alternative arrival` | keep (substring of "arrival") |
| 1389 | B13 | `a purchase recruits the second buyer` | `a purchase recruits the rival` |
| 1398 | B13 | `Entry can rise with first-buyer strength` | `Entry can rise with incumbent strength` |
| 1414 | B13 | `Informed-investor share and announcement detail` | `Informed-trader share and announcement detail` |
| 1425 | B13b | `Counts name informed investor presence` | `Counts name informed presence` (the deck's name for $\lambda$, line 264) |
| 1427 | B13b | `For a prepared second buyer, the winner gap` | `For a prepared rival, the winner gap` |
| 1430 | B13b | `Date first-buyer strength from public records` | `Date incumbent strength from public records` |
| 1443 | B13c | `for a prepared second buyer of class $j$ ... For a prepared second buyer,` | `for a prepared rival of class $j$ ... For a prepared rival,` |
| 1457 | B14 table | `The decision is a rival's entry ... between shareholders and that rival` | keep |
| 1459 | B14 table | `An outside investor with no stake informs a rival bidder` | `An outside informed trader with no stake informs a rival bidder` ("bidders learn from prices": keep) |
| 1524 | B16 table | `first buyer's value $R$` | `incumbent's value $R$` |
| 1525 | B16 table | `second buyer's value $\theta$` | `rival's value $\theta$` |
| 1528 | B16 table | `the informed investor's chosen order $q$` | `the informed trader's chosen order $q$` |
| 1533 | B16 table | `second-buyer gross profit $B(\mu)=...$` | `rival gross profit $B(\mu)=...$` |
| 1534 | B16 table | `the probability that the second buyer prepares` | `the probability that the rival prepares` |
| 1549 | B16b table | `payoff from order $q$; investor sees class $j$` | `payoff from order $q$; informed trader sees class $j$` |
| 1557 | B16b table | `a prepared class-$j$ second buyer` | `a prepared class-$j$ rival` |

### 2b. `slides.tex`, source comments (not printed)

These comments are the editor's contract for the deck, so update them. They are not code identifiers.

| Line | Current (excerpt) | Proposed |
|---:|---|---|
| 8 | `% Locked words: first buyer / second buyer;` | `% Locked words: incumbent / rival (frame 5 defines incumbent bidder, potential rival bidder); informed trader;` |
| 10 | `second-buyer gross profit $B(\mu)$;` | `rival gross profit $B(\mu)$;` |
| 66 | `split at the first buyer's value` | `split at the incumbent's value` |
| 67 | `below the first buyer's value ... to the second buyer.` | `below the incumbent's value ... to the rival.` |
| 114 | `between the strong and the very strong first buyer` | `between the strong and the very strong incumbent` |

### 2c. `ccc-journal.sty`

No visible actor words. No change.

## 3. First-use definitions

**Slides, frame 5 (`label=S5`, "Players and the sale rule"), lines 228 and 229.** Change the label heads
and the opening of each row. Keep the rest of each row as it is.

Line 228:
```
\DefRow{Incumbent}{\textbf{incumbent bidder, already prepared:} it knows its value $R$ and faces no further preparation cost. $R\sim F$; ...
```
Line 229:
```
\DefRow{Rival}{\textbf{potential rival bidder:} it sees the stock price, then decides whether to prepare. \textbf{Synergy class:} $j=H$ (good synergy) or ...
```
Line 231 already says "Pay $C$ to learn $\theta$ and to bid". That sentence completes the meaning of
"prepare", as `recommendation.md` asks. Line 236 then names the three market actors ("informed trader,
liquidity trader, competitive market makers"). Frame 6 (lines 264 to 266) defines them.

**Script, title speech, line 33.** This is the first use in the script. Proposed text:
> This talk concerns a public sale before the bidder set closes. One bidder is already prepared. I call it
> the incumbent bidder, or the incumbent. A potential rival bidder, the rival, must pay to prepare. Between
> those two stages, the target stock price can affect who enters the sale.

The script is a spoken text by the author, and it already uses "I" (lines 33, 63, 87). The no-first-person
rule applies to the slides only. The frame 5 speech (lines 95 and 97, section 6) reads the slide label heads
aloud. It is not a second definition.

## 4. Grammar and layout fallout

**Articles.** No a/an change is necessary. "a second buyer" -> "a rival", "an indifferent second buyer" ->
"an indifferent rival", "an outside informed investor" -> "an outside informed trader", "An investor" ->
"An informed trader". Two places need a new article: line 1056 ("with second buyer's value" -> "with the
rival's value") and script line 127 ("second buyer value theta" -> "the rival's value theta").

**Pronouns.** Line 173: "A stronger first buyer weakly cuts its expected auction profit". The "its" refers
to the second buyer in the previous bullet. After the change, "its" reads as the incumbent's profit. Write
"the rival's expected auction profit".

**Plurals.** Line 1321: "more good-synergy buyers" becomes singular ("a good-synergy rival more often"),
because there is one rival. Lines 927 and 949: "uniform first buyers" names value laws, so write "uniform
incumbent values". Script 167: "Indifferent investors may mix. Prepared buyers bid their values." -> "An
indifferent informed trader may mix. Each prepared bidder bids its value."

**Label heads and table heads.** Frame 5 `\DefRow` heads (lines 228, 229), frame 1 column head (158),
frame 7 table rows (281, 282, 285), B6 table row (929), B7 boxes (1005, 1009), B11s row (1178), and B11d
panel head (1293). All new heads are shorter than the old heads, or equal.

**Frame titles and subtitles.** Lines 150 (S1), 168 (S2 subtitle), 201 (S4), 331 (S10), 903 (B5). All are
shorter after the change. The S1 title is `\LARGE`; it gets shorter by 14 characters.

**Length growth and overflow risk.** Most changes shorten the text: first buyer -> incumbent (-2), second
buyer -> rival (-7), informed investor -> informed trader (-2). Only "investor" alone -> "informed trader"
(+7) and the definitions make text longer. Free space comes from the last build (`\vfill` gap for frames
with a pinned intuition or takeaway; bottom margin for frames without one). Rebuild and look at these
frames:

| Frame (page) | Lines | Change | Free space | Risk |
|---|---|---|---|---|
| S5 (p6) | 228, 229, 236 | about +80 characters net | about 20 pt `\vfill` gap; bottom margin 1 pt | **High.** If it overflows, cut the 229 lead to `\textbf{potential rival bidder:} sees the price, then decides whether to prepare.` |
| S18 (p19) | 664 | +14 in a 0.48-width minipage | about 26 pt `\vfill` gap | Medium. Fallback: `(class $H$ buys; class $L$ sells)`, the wording of line 1442. |
| S16 (p17) | 586, 597 | +7 each | about 23 pt `\vfill` gap | Medium: two minipages side by side. |
| S12 (p13) | 440, 441 | +7 each | about 32 pt `\vfill` gap | Low |
| S3 (p4) | 193, 196 | +7 in a 5.3 cm cell; +7 in the takeaway | about 34 pt | Low |
| S4 (p5) | 212 | +22 on one line | about 36 pt | Low. The line can wrap. |
| S9 (p10) | 321 | +7 net; 323 and 324 get shorter | 8 pt bottom margin, no `\vfill` | Low (net shorter) |
| B9 (p37) | 1089, 1090, 1091 | about 0 net | 0 pt bottom margin, no `\vfill` | Low. Check it. |
| S6 (p7) | 257 | +4 in a 2.75 cm node | 15 pt bottom margin | Low |

## 5. Bid sequence: "both bidders learn values after preparation"

- **Line 257, frame 6 timeline, node 5:** `Prepared buyer learns $\theta$; bids; payoffs`. $\theta$ is the rival's
  value only. "Prepared buyer" includes the incumbent, so the node says that any prepared bidder learns
  its value at that step. This is the slide copy of the manuscript clause at `02_model.tex` 165 to 169.
  Proposed: `Rival, if prepared, learns $\theta$; bids; payoffs`.
- Other sequence statements are correct. Do not change them for this fix. Line 228 (the incumbent knows $R$
  and others do not see the draw before bids), lines 172, 231, 285, and 324. In the script: lines 99, 109,
  125, and 135 ("It learns theta only after preparation").
- Line 1090 (B9: "each prepared buyer ... bids its value") and script line 167 ("Prepared buyers bid their
  values") are about bids, not value discovery. They need only the term change.

## 6. Speaker script (`slides_script.md`)

The script must change in these places:

- **Headings** that repeat frame titles: 35 (S1), 77 (S4), 169 (S10). Prepared-answer headings: 325 ("Who is
  the informed investor?" -> "Who is the informed trader?"), 329 ("Don't buyers ..." -> "Don't bidders
  already look at the price?"), 341 ("... the strong first buyer?" -> "... the strong incumbent?").
- **Headline:** line 321 -> "So a stronger incumbent can induce rival entry through a more informative
  stock price. Thank you." This matches slide line 688.
- **Frame 5 speech** (lines 95, 97) must say what the label heads say. 95: "The incumbent is already
  prepared and faces no further cost. Its value R follows public continuous distribution F, ...". 97: "The
  rival sees the price, then decides whether to prepare. Its class j is H, good synergy, or L, poor
  synergy. ... The sale and the rival's identity are public."
- **Specialist:** lines 129 and 327. 129: "The informed trader is an outsider with sector expertise, such as
  a sector-focused long-short fund that researches ...". 327: "It is an outsider with sector expertise,
  such as a sector-focused long-short fund. ..." Drop "The paper calls it" unless the revised paper uses
  that phrase.
- **Fishman, line 59 (judgement):** "In Fishman, the first buyer chooses a preemptive bid" describes another
  model. Use Fishman's own term, "the first bidder", not "the incumbent".
- **Word counts:** the table at lines 14 to 27 is a stated contract ("Word counts cover speech only").
  Recount it after the edits. The title speech grows by about 10 words. Most frames get shorter.

Line table (same mapping as 2a; "keep" rows contain a listed word):

| Line | Current (excerpt) | Proposed |
|---:|---|---|
| 33 | `before the buyer set closes. One buyer is ready. Another buyer must pay to prepare.` | first-use definition, see 3 |
| 35 | `## Frame 1 — Does a stronger first buyer always keep the second buyer out?` | `## Frame 1 — Does a stronger incumbent always keep the rival out?` |
| 39 | `One buyer has done its homework. A second buyer must decide` | `The incumbent has done its homework. The rival must decide` |
| 41 | `Does a stronger first buyer always keep the second buyer out?` | `Does a stronger incumbent always keep the rival out?` |
| 43 | `one more buyer before the buyer set closes. That buyer can compete ... a stronger first buyer helps discover the second buyer` | `one more bidder before the bidder set closes. That bidder can compete ... a stronger incumbent helps discover the rival` |
| 45 | `The second buyer cares ... A stronger first buyer can reduce ... But the buyer can also learn` | `The rival cares ... A stronger incumbent can reduce ... But the rival can also learn` |
| 47 | `the second buyer's synergy` | `the rival's synergy` |
| 49 | `the buyer needs a reason to pay` | `the rival needs a reason to pay` |
| 57 | `A buyer pays before it can bid. A stronger first buyer ... when the second buyer wins` | `The rival pays before it can bid. A stronger incumbent ... when the rival wins` |
| 59 | `In Fishman, the first buyer chooses a preemptive bid.` | `In Fishman, the first bidder chooses a preemptive bid.` |
| 61 | `what the buyer knows ... a stronger first buyer weakly lowers expected second-buyer gross profit` | `what the rival knows ... a stronger incumbent weakly lowers expected rival gross profit` |
| 63 | `why a stronger first buyer can make that price say more` | `why a stronger incumbent can make that price say more` |
| 73 | `an outside informed investor starts with no net position` | `an outside informed trader starts with no net position` |
| 75 | `and the second buyer, who decides ... how much the price tells that buyer` | `and the rival, who decides ... how much the price tells the rival` |
| 77 | `## Frame 4 — This paper: a stronger first buyer can recruit the second` | `## Frame 4 — This paper: a stronger incumbent can recruit the rival` |
| 81 | `A stronger first buyer weakly cuts the second buyer's profit ... recruit the second buyer` | `A stronger incumbent weakly cuts the rival's profit ... recruit the rival` |
| 83 | `the strong first buyer ... never raises second-buyer profit` | `the strong incumbent ... never raises rival profit` |
| 85 | `against the strong first buyer` | `against the strong incumbent` |
| 95 | `First buyer value R follows` | see the frame 5 item above |
| 97 | `Second buyer class j is H ... The sale and second buyer's identity are public.` | see the frame 5 item above |
| 101 | `Neither buyer trades target shares.` | `Neither bidder trades target shares.` |
| 109 | `Then market makers set ... The second buyer sees P` | `market makers` keep; `The rival sees P` |
| 111 | `the informed investor receives the order opportunity` | `the informed trader receives the order opportunity` |
| 115 | `Competitive market makers see only the order X` | keep |
| 117 | `the informed investor's advantage` | `the informed trader's advantage` |
| 125 | `The first buyer knows value R` | `The incumbent knows value R` |
| 127 | `The informed investor sees class j ... does not see second buyer value theta` | `The informed trader sees class j ... does not see the rival's value theta` |
| 129 | `The informed investor is an outside sector specialist, such as` | `The informed trader is an outsider with sector expertise, such as` |
| 133 | `Market makers observe the order X and cannot identify the trader` | keep |
| 135 | `The second buyer sees the price` | `The rival sees the price` |
| 137 | `Market makers use that belief. The second buyer instead conditions` | `Market makers` keep; `The rival instead conditions` |
| 143 | `Take a prepared second buyer ... what the second buyer keeps` | `Take a prepared rival ... what the rival keeps` |
| 145 | `the smaller of first buyer value R and theta` | `the smaller of incumbent value R and theta` |
| 151 | `Second-buyer gross profit B at belief mu` | `Rival gross profit B at belief mu` |
| 153 | `The investor earns signed order q` | `The informed trader earns signed order q` |
| 159 | `set by competitive market makers` | keep |
| 161 | `Investor payoff U sub j multiplies` | `The informed trader's payoff U sub j multiplies` |
| 167 | `when second-buyer gross profit B covers it ... Indifferent investors may mix. Prepared buyers bid their values.` | `when rival gross profit B covers it ... An indifferent informed trader may mix. Each prepared bidder bids its value.` |
| 169 | `## Frame 10 — Strength never raises buyer profit` | `## Frame 10 — Strength never raises rival profit` |
| 173 | `distributions for first buyer value ... a stronger first buyer` | `distributions for incumbent value ... a stronger incumbent` |
| 175 | `Second-buyer gross profit B at every fixed belief` | `Rival gross profit B at every fixed belief` |
| 181 | `part of the buyer's profit gap to shareholders` | `part of the rival's profit gap to shareholders` |
| 193 | `a positive second-buyer gross-profit gap` | `a positive rival gross-profit gap` |
| 195 | `divided by the second-buyer gross-profit gap. At tau, second-buyer gross profit` | `divided by the rival gross-profit gap. At tau, rival gross profit` |
| 207 | `The informed investor places its correct order` | `The informed trader places its correct order` |
| 215 | `Each step strengthens the first buyer.` | `Each step strengthens the incumbent.` |
| 217 | `B sub i is second-buyer gross profit there` | `B sub i is rival gross profit there` |
| 227 | `Against the weak first buyer, the informed investor abstains` | `Against the weak incumbent, the informed trader abstains` |
| 229 | `Against the strong first buyer` | `Against the strong incumbent` |
| 231 | `Against the very strong first buyer` | `Against the very strong incumbent` |
| 243 | `First buyer value is uniform` | `Incumbent value is uniform` |
| 255 | `the second buyer's signal S` | `the rival's signal S` |
| 257 | `second buyer value theta and first buyer value R ... An indifferent second buyer prepares.` | `rival value theta and incumbent value R ... An indifferent rival prepares.` |
| 259 | `strength weakly lowers second-buyer gross profit` | `strength weakly lowers rival gross profit` |
| 261 | `against the weak first buyer ... against the strong first buyer` | `against the weak incumbent ... against the strong incumbent` |
| 263 | `The second buyer still sees the price.` | `The rival still sees the price.` |
| 265 | `The second buyer uses the prior.` | `The rival uses the prior.` |
| 271 | `The investor now chooses presence lambda` | `The informed trader now chooses presence lambda` |
| 273 | `positive spread and second-buyer gross-profit gap` | `positive spread and rival gross-profit gap` |
| 277 | `the investor who learns good synergy buys` | `the informed trader who learns good synergy buys` |
| 285 | `at the strong first buyer F one` | `at the strong incumbent F one` |
| 291 | `The first buyer, values and costs stay fixed.` | `The incumbent, values and costs stay fixed.` |
| 297 | `positive spread and second-buyer gross-profit gap` | `positive spread and rival gross-profit gap` |
| 313 | `against the strong first buyer ... second-buyer gross profit` | `against the strong incumbent ... rival gross profit` |
| 315 | `what the second buyer can learn ... a stronger first buyer cannot raise entry` | `what the rival can learn ... a stronger incumbent cannot raise entry` |
| 319 | `against the strong first buyer` | `against the strong incumbent` |
| 321 | `So a stronger first buyer can bring in the second buyer through the stock price.` | `So a stronger incumbent can induce rival entry through a more informative stock price.` |
| 325 | `### Who is the informed investor? — B5` | `### Who is the informed trader? — B5` |
| 327 | `The paper calls it an outside sector specialist ... the second buyer's synergy class ... Neither buyer trades` | `It is an outsider with sector expertise ... the rival's synergy class ... Neither bidder trades` |
| 329 | `### Don't buyers already look at the price?` | `### Don't bidders already look at the price?` |
| 331 | `The second buyer reads ... the news the second buyer can recover` | `The rival reads ... the news the rival can recover` |
| 335 | `The buyer set ... A stronger first buyer ... to an informed investor and draw another buyer into preparation ... against the strong first buyer` | `The bidder set ... A stronger incumbent ... to an informed trader and draw a rival into preparation ... against the strong incumbent` |
| 339 | `reaches the second buyer ... against the stronger first buyer ... against the weaker buyer` | `reaches the rival ... against the stronger incumbent ... against the weaker incumbent` |
| 341 | `### Is the equilibrium unique between the weak and the strong first buyer? — B3` | `### ... between the weak and the strong incumbent? — B3` |
| 343 | `recruits the high-cost second buyer` | `recruits the high-cost rival` |
| 347 | `Against the weak first buyer ... strong first buyer ... very strong first buyer` | `Against the weak incumbent ... strong incumbent ... very strong incumbent` |
| 351 | `recruits the high-cost second buyer` | `recruits the high-cost rival` |
| 355 | `at the strong first buyer F one` | `at the strong incumbent F one` |

Out of scope, for information only: the script uses "type" for the class at lines 101 ("type-value pair")
and 137 ("type H"), and "case" at line 257. The term table does not cover these words, so this pass leaves
them.

## Counts

Proposed line-level replacements: 143 in the visible text of `slides.tex`, 5 in the comments of `slides.tex`,
and 75 in `slides_script.md`. Total: 223. A line with several hits counts once. The tables also contain 11
"keep" rows.
