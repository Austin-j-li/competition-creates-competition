# Website terminology scan, 29 October 2026

Read-only scan of the website source in the worktree `/home/uctpiaj/work/tmp/ccc-main-slidepack`
(branch `main`, commit `5607e31`), measured against `decisions.md`. No source file was changed.
Line numbers are the line numbers in each file.

## 1. Verdict

**The brief page has no collision.** It has no actor uses of "rival" or "entrant". The only
match for "rival" is "alternative-arrival" (`01-setting.html:79`). "Entry" always means the
decision to prepare. "Trader" is used only for "liquidity trader" and in two generic places
that are correct: "its trader" (`01:32`) and "bidders, shareholders and traders" (`05:12`). The
decisions apply cleanly. Apply the rules below:

- Rename "challenger" to "rival", "investor" to "informed trader", and "specialist" as shown.
- Make "buyer" in the model "bidder" or "rival". Keep "buyer" in only two record uses:
  "outreach to other buyers" (`01:38`, Imprivata) and "a leveraged financial buyer" (`01:67`,
  a term of art in the record column).
- Use the possessive, not an attribute, when "rival" modifies a non-actor noun ("the rival's
  signal", not "a rival signal"). "Rival signal", "rival profit" and "rival value" read as
  "a competing signal", "competing profit" and "competing value".

**The web slides (`presentation/content.js`) collide, and a mechanical pass would invert the
meaning.** The slides use "rival" for the *first* buyer (the incumbent):

- `content.js:84` "Does a strong rival kill the case for diligence"
- `content.js:89` title "a stronger rival pays less for your diligence"
- `content.js:114-115` "Weak rival / Strong rival / Very strong rival" (these are F0, F1, F2)

Line 110 uses "rival" for the second buyer, as `decisions.md` does. Line 129 "highest rival bid"
means any competing bid. Remove these uses in the Overleaf deck before the deck regenerates
`content.js`, and check that the three labels do not come back. Other open items in the slides:

- "Entrant" names the actor at `113` ("what the entrant loses") and `177` ("the entrant claim").
  This breaks the rule that "entrant" describes only participation status.
- "Fund" (about 14 uses) and "outside trader" (`105`, `113`) name the informed trader. The table
  in `decisions.md` does not cover these words, so this is an open decision for the deck. I
  propose no text for it.

## 2. Replacement tables

The tables list every line that needs a change. "No change" lines are listed after each table.

"Prepared buyer" is an old name for the incumbent in `decisions.md`. On the page, "a stronger
prepared bidder" names the incumbent (06:9 ×3, 01:67), so it becomes "incumbent". Keep these
uses, because they describe a state, not an actor:

- "each prepared bidder bids its value" (01:19, both bidders)
- "One bidder is prepared" (01:30, 06:6)
- "prepared rival" (all lines)

### handout/template.html (11)

| Line | Current | Proposed |
|---|---|---|
| 9 | meta description: "draw a second buyer into the sale?" | "draw a rival bidder into the sale?" |
| 13 | og:description: "draw a second buyer into the sale?" | "draw a rival bidder into the sale?" |
| 65 | "When can a stronger bidder draw a second buyer into the sale?" | "When can a stronger bidder draw a rival bidder into the sale?" |
| 66 | "A stronger incumbent leaves a challenger less to gain … depend more on the challenger's quality, so an investor who knows that quality" | "A stronger incumbent bidder leaves a potential rival bidder less to gain … depend more on the rival's quality, so an informed trader who knows that quality" (4) |
| 67 | "carry that knowledge to the challenger before it commits … brings in a high-cost buyer that a weaker incumbent" | "to the rival before it commits … brings in a high-cost rival that a weaker incumbent" (2) |
| 86 | "Does a stronger incumbent keep the next buyer out?" | "Does a stronger incumbent keep a rival out?" |
| 88 | "the bounded belief it gives the challenger" | "the bounded belief it gives the rival" |

No change: "incumbent" at 67 (×2) and 86.

### handout/sections/01-setting.html (43)

| Line | Current | Proposed |
|---|---|---|
| 8 | "One buyer is ready to bid." | "One bidder is ready to bid." |
| 10 | "A buyer that does not prepare … differ across buyers: a buyer with capacity in place" | "A bidder that does not prepare … differ across bidders: a bidder with capacity in place" (3) |
| 14 | "The prepared `<em>incumbent</em>` knows … The `<em>challenger</em>` belongs to a high or a low quality class" | Definition, see §3 (2) |
| 20 | "An outside specialist investor knows the challenger's class and remains uncertain about its value. … before the challenger decides. With probability \(\lambda\) the investor fills the slot" | "An outside `<em>informed trader</em>` with sector expertise knows the rival's class and remains uncertain about the rival's value. … before the rival decides. With probability \(\lambda\) the informed trader fills the slot" (4) |
| 27 | "The challenger sees the price and its own cost" | "The rival sees the price and its own cost" |
| 30 | "One bidder is prepared; the challenger has not decided." | "…; the rival has not decided." |
| 31 | button "The investor learns"; note "The investor learns the challenger's class \(j\). The challenger, the market makers and the incumbent do not." | button "The informed trader learns"; note "The informed trader learns the rival's class \(j\). The rival, the market makers and the incumbent do not." (4) |
| 32 | "the investor places its order" | "the informed trader places its order" |
| 33 | "change the challenger's decision" | "change the rival's decision" |
| 34 | button "The challenger decides"; note "The challenger reads a belief" | button "The rival decides"; note "The rival reads a belief" (2) |
| 38 | "before the set of buyers is fixed; only then can a prospective buyer watch the price" | "before the set of bidders is fixed; only then can a potential rival watch the price" (2) |
| 41 | "class and challenger value … Without a challenger, the incumbent buys … A zero-cost challenger prepares" | "class and the rival's value … Without a rival, the incumbent buys … A zero-cost rival prepares" (3) |
| 42 | "the challenger's belief … The investor may mix … A deviation by the investor … an indifferent investor may mix … an indifferent high-cost challenger prepares … an indifferent investor abstains … an indifferent high-cost challenger may prepare" | "the rival's belief … The informed trader may mix … A deviation by the informed trader … an indifferent informed trader may mix … an indifferent high-cost rival prepares … an indifferent informed trader abstains … an indifferent high-cost rival may prepare" (7) |
| 66 | table: "Visibility dated before the challenger's decision" | "…before the rival's decision" |
| 67 | table: "what the public can infer about the prepared bidder's value" / "Measured before the challenger decides" | "…about the incumbent's value" / "Measured before the rival decides" (2) |
| 70 | table: "The investor" / "Outside flow with a view on the challenger's fit, such as sector specialists" | "The informed trader" / "Outside flow with a view on the rival's fit, such as traders with sector expertise" (3) |
| 78 | "a traded claim and a challenger that decides … the challenger's entry itself … a prospective challenger learns" | "a traded claim and a rival that decides … the rival's entry itself … a potential rival learns" (3) |
| 79 | "the orders of an investor who knows the challenger's class" | "the orders of an informed trader who knows the rival's class" (2) |

No change: "incumbent" at 14 (×2, one becomes the definition), 31, 41 (×4), 42, 44 (×2), 67;
"Competitive market makers" at 27 (already the first-use form); "market makers" at 31 and 33;
"its trader" at 32 (generic sense, correct); "other buyers" at 38 and "financial buyer" at 67
(record uses).

### handout/sections/02-mechanism.html (28)

| Line | Current | Proposed |
|---|---|---|
| 6 | "The challenger uses information … The investor uses the same … reduces the challenger's profit" | "The rival uses … The informed trader uses … reduces the rival's profit" (3) |
| 10 | "at each belief about the challenger's class" | "…about the rival's class" |
| 11 | "Proceeds depend more on the challenger's class" · "The investor earns more" · "to the challenger through the price" | "…on the rival's class" · "The informed trader earns more" · "to the rival through the price" (3) |
| 18 | "the challenger prepares when … with a high-class challenger" | "the rival prepares when … with a high-class rival" (2) |
| 19 | "the incumbent outbids the challenger … stays as challenger profit … a prepared challenger wins" | "the incumbent outbids the rival … stays as the rival's profit … a prepared rival wins" (3) |
| 26 | "from the challenger's profit to target proceeds" | "from the rival's profit…" |
| 28 | aria-label "the challenger's gross profit falling" | "the rival's gross profit falling" |
| 32 | "the investor adds at most \(\lambda\) … every pure or mixed investor strategy" | "the informed trader adds at most \(\lambda\) … every pure or mixed strategy of the informed trader" (2) |
| 40 | "no order recruits a high-cost challenger" | "…a high-cost rival" |
| 41 | "The zero-cost challenger prepares … an indifferent high-cost challenger prepares" | "The zero-cost rival prepares … an indifferent high-cost rival prepares" (2) |
| 45 | "The investor earns from the class information" | "The informed trader earns…" |
| 53 | "so the investor's problem splits by class" | "so the informed trader's problem…" |
| 55 | "the investor's orders … the challenger's preparation … recruit a high-cost challenger … while a challenger known to be in the low class" | "the informed trader's orders … the rival's preparation … recruit a high-cost rival … while a rival known to be in the low class" (4) |
| 58 | "A prepared challenger with value … expected proceeds plus challenger profit" | "A prepared rival with value … expected proceeds plus the rival's profit" (2) |
| 77 | "cancel from the investor's returns" | "cancel from the informed trader's returns" |

No change: "incumbent" at 6, 8, 10, 19 (×5), 26 (×2), 28, 40, 55, 58 (×2), 76; "market makers" at 41 and 45.

### handout/sections/03-result.html (17)

| Line | Current | Proposed |
|---|---|---|
| 6 | "A stronger incumbent can attract a second bidder by making the price more informative. … a purchase recruits a high-cost challenger" | Headline sentence: "A stronger incumbent can induce rival entry through a more informative stock price." … "a purchase recruits a high-cost rival" (2) |
| 19 | "the investor abstains … recruits the high-cost challenger" | "the informed trader abstains … recruits the high-cost rival" (2) |
| 22 | "recruits no high-cost challenger" | "…no high-cost rival" |
| 24 | "a prepared high-class challenger wins … go to a challenger … a low-class challenger beats" | "a prepared high-class rival wins … go to the rival … a low-class rival beats" (3) |
| 33 | stat label "only zero-cost challengers" | "only zero-cost rivals" |
| 37 | "the takeovers that go to a challenger" | "…that go to the rival" |
| 39 | "recruits no high-cost challenger" | "…no high-cost rival" |
| 40 | caption "every posterior that an investor strategy can produce" | "every posterior that a strategy of the informed trader can produce" |
| 43 | "a signal that the challenger observes … tells the challenger nothing more" | "a signal that the rival observes … tells the rival nothing more" (2) |
| 51 | row head "The challenger does not see the price" | "The rival does not see the price" |
| 55 | caption "the investor still trades fully … The challenger uses its prior" | "the informed trader still trades fully … The rival uses its prior" (2) |

No change: "incumbent(s)" at 6 (×2), 23, 24 (×3), 25 (×2), 33, 34, 35, 38 (×2), 39, 40, 43 (×3).

### handout/sections/04-path.html (17)

| Line | Current | Proposed |
|---|---|---|
| 6 | "the investor does not trade … recruits a high-cost challenger … an indifferent investor may mix … an indifferent high-cost challenger prepares" | "the informed trader does not trade … a high-cost rival … an indifferent informed trader may mix … an indifferent high-cost rival prepares" (4) |
| 37 | "conditional on investor presence" | "conditional on the presence of the informed trader" |
| 56 | "When an indifferent investor abstains … When an indifferent high-cost challenger may prepare" | "When an indifferent informed trader abstains … When an indifferent high-cost rival may prepare" (2) |
| 60 | "The investor can also pay … gives the investor the slot … Market makers and the challenger do not observe … the investor's own orders" | "The informed trader can also pay … gives the informed trader the slot … Market makers and the rival do not observe … the informed trader's own orders" (4) |
| 61 | "recruits a high-cost challenger" | "…a high-cost rival" |
| 66 | "at the research the investor chooses … so the challengers who prepare" | "at the research the informed trader chooses … so the rivals who prepare" (2) |
| 68 | "the investor chooses more research" | "the informed trader chooses more research" |
| 69 | caption "an indifferent investor may mix … an indifferent high-cost challenger prepares" | "an indifferent informed trader may mix … an indifferent high-cost rival prepares" (2) |

No change: "incumbent" at 6 (×2), 12, 27 (×2), 66 (×3), 68; "Market makers" at 60.

### handout/sections/05-robustness.html (21)

| Line | Current | Proposed |
|---|---|---|
| 9 | "even when the challenger has a more accurate private signal than the investor. The challenger knows … the investor knows … investor accuracy is \(\alpha_I\) … challenger accuracy is \(\alpha_C\) … Without the challenger's signal" | "even when the rival has a more accurate private signal than the informed trader. The rival knows … the informed trader knows … the informed trader's accuracy is \(\alpha_I\) … the rival's accuracy is \(\alpha_C\) … Without the rival's signal" (7) |
| 12 | "even when the challenger cannot use the price" | "even when the rival cannot use the price" |
| 16 | "a sale to the next buyer at its value … never raises the challenger's profit … the winner pays the next buyer's value" | "a sale to the losing bidder at its value … never raises the rival's profit … the winner pays the losing bidder's value" (3) |
| 20 | "the challenger profit gap … A prepared challenger's profit is convex" | "the rival's profit gap … A prepared rival's profit is convex" (2) |
| 22 | "without the challenger's signal … needs an accurate investor signal … a challenger signal at least as accurate … a more accurate challenger signal" | "without the rival's signal … needs an accurate signal for the informed trader … a signal for the rival at least as accurate … a more accurate signal for the rival" (4) |
| 23 | "The investor's expected gross profit … without the investor" | "The informed trader's expected gross profit … without the informed trader" (2) |
| 39 | caption "A challenger can prepare … where the investor does not trade" | "A rival can prepare … where the informed trader does not trade" (2) |

No change: "incumbent(s)" at 8 (×2), 9 (×2), 12, 16 (×4), 17 (×5), 20 (×2), 21 (×2), 24; "traders" at 12 (generic); "liquidity traders" at 23.

### handout/sections/06-tests.html (21)

| Line | Current | Proposed |
|---|---|---|
| 6 | "a challenger has not yet committed to diligence" | "a rival has not yet committed to diligence" |
| 9 | "reaches the challenger before it decides, a stronger prepared bidder can raise … that the challenger prepares … does not reach the challenger, a stronger prepared bidder can only lower it. Against a strong enough prepared bidder" | "reaches the rival before it decides, a stronger incumbent can raise … that the rival prepares … does not reach the rival, a stronger incumbent can only lower it. Against a strong enough incumbent" (6) |
| 12 | "a purchase recruits the challenger" | "a purchase recruits the rival" |
| 15 | "identify the informed investor's presence" | "identify the informed trader's presence" |
| 18 | "a prepared challenger wins … with a challenger win … Among prepared challengers" | "a prepared rival wins … with a win by the rival … Among prepared rivals" (3) |
| 21 | "the investor's incentives" | "the informed trader's incentives" |
| 22 | "the lowest challenger value" | "the lowest value of the rival" |
| 23 | "whether the challenger prepared" | "whether the rival prepared" |
| 24 | "every challenger prepares after a purchase" | "the rival prepares after every purchase" |
| 25 | "before the challenger's decision" | "before the rival's decision" |
| 27 | takeaway "from the challenger's profit … match the investor's direction, the investor keeps … recruits a challenger" | "from the rival's profit … match the informed trader's direction, the informed trader keeps … recruits a rival" (4) |

No change: "incumbent" at 8 (heading "Entry and incumbent strength"), 18 (×2), 20 (×4), 22 (×3), 25, 27 (×2).

### handout/explorer.js (10)

| Line | Current | Proposed |
|---|---|---|
| 43 | "so only a zero-cost challenger prepares." | "…zero-cost rival prepares." |
| 45 | "recruits a high-cost challenger; the purchase earns" | "…a high-cost rival; …" |
| 46 | "recruits a high-cost challenger." | "…a high-cost rival." |
| 47 | "no order recruits a high-cost challenger." | "…a high-cost rival." |
| 49 | "recruits a high-cost challenger." | "…a high-cost rival." |
| 50 | "no order recruits a high-cost challenger and entry" | "…a high-cost rival and entry" |
| 102 | legend "T: threshold pair (if an indifferent challenger may mix)" | "T: threshold pair (if an indifferent rival may mix)" |
| 137 | annotation "T endpoint (challenger mixing)" | "T endpoint (rival mixing)" |
| 227 | Figure 3 caption "an indifferent high-cost challenger may prepare … Under challenger mixing" | "an indifferent high-cost rival may prepare … When the rival mixes" (2) |

No change: "incumbent strength" at 119, 121, 180, 225. Comments at 3-5 and 107 are not visible.

### Files with no visible change

- `handout/figures.js`: only the axis title "incumbent strength" (184, 186, 226, 228, 300, 302). The comments at 6, 14 and 96 are not visible.
- `handout/charts.js`: the `fig1`-`fig4` builders have the strings "challenger gross profit"
  (182), "weak/strong incumbent" (420) and "challenger profit" (451). The slot page has no
  `chart-fig*` mount, so these strings never show. They come from the Laplace version, so they
  are excluded from this scan.
- `handout/app.js`, `handout/build.py` (the paper-tab text), `handout/slot_data.py`: no hits.
- `presentation/deck.js`: only the axis title "incumbent strength" (257, 313, 351).
  `presentation/figdata.py`: docstrings only (4, 71). `presentation/build.py`: no hits.

### presentation/content.js (occurrence list only, no replacements)

Format: line: terms (a count shows more than one use).

83 buyer×2, second buyer · 84 buyers, **rival (= incumbent)** · 89 **rival (= incumbent, title)** ·
91 buyer · 92 first buyer, second buyer · 93 buyers · 94 buyer · 96 first buyer · 105 outside trader ·
110 rival (= second buyer, title) · 112 first buyer, second buyer, buyer · 113 outside trader,
**entrant (actor)** · 114 **rival×2 (= incumbent)** · 115 **rival (= incumbent)** · 121 buyer×2 (title) ·
124 buyer · 126 second buyer · 129 "highest rival bid" (= any competing bid) · 137 first buyer×2 ·
138 specialist investor · 139 second buyer×2 · 140 second buyer · 143 first buyer · 154 specialist
investor (box label) · 160 market makers (box label; first-use form missing) · 162 second buyer
(box label) · 169 buyer (title) · 171 first buyer, second buyer · 175 buyer · 177 **entrant (actor)** ·
185 second buyer · 186 investor · 188 investor, buyer · 189 second buyer×2, good-fit second buyer ·
196 second buyer (title) · 198 first buyer · 200 first buyer · 201 first buyer, second buyer×2 ·
202 first buyer · 205 buyer (title) · 207 first buyer, buyer · 208 first buyer · 223 second buyer ·
225 buyer · 249 first buyer, second buyer (title) · 252 fund · 296 incumbent · 306 buyer (title) ·
309 buyer · 311 fund · 320 buyers (title) · 323 first buyer · 324 buyer · 330 second buyer ·
346 fund · 348 fund×2 · 362 fund · 369 fund (title) · 372 fund · 373 fund · 380 good-fit buyers ·
404 second buyer, buyer, fund · 410 buyer (title) · 414 incumbent · 415 fund · 449 second buyer ·
452 first-buyer · 459 fund · 466 first buyer, second buyer · 467 buyer · 469 second buyer ·
497 investor · 499 investor · 559 challenger · 560 challenger · 587 challenger · 635 challenger ·
668 incumbent · 683 fund (title) · 685 fund · 687 first buyer · 690 first-buyer · 696 incumbent ·
697 first buyer · 698 challenger · 703 challenger×2 · 713 second buyer · 714 good-fit second buyer ·
715 investor · 716 incumbent.

Lines 121-162 make up the model frames. The definitions in `decisions.md` belong on the first
model frame. In the current web deck, that frame is S5, "One buyer is ready. One buyer still
decides."

## 3. First-use definitions on the brief page

The brief follows the paper's rule: the opening aside *names* the actors, and section 1
*defines* them.

1. **Names in the opening aside** (`template.html:65-66`): "incumbent bidder", "potential rival
   bidder" and "informed trader" appear in full. Wording is in the template table. In the
   question on line 65, "a stronger bidder" is the incumbent. Keep it: the question comes before
   the names, and line 66 gives both full names in the next sentence.
2. **Definition in "Who knows what"** (`01-setting.html:14`). The brief already uses "I" (`03:6`,
   `03:43`), so "I call it" fits. Replace the first two sentences and the challenger sentence with:

   > One bidder is already prepared; I call it the `<em>incumbent bidder</em>`, or the incumbent. It
   > is the party that approached the target or a bidder that has completed diligence. The incumbent
   > knows its acquisition value \(R\). Its strength is the public distribution \(F\) of \(R\), and a
   > first-order stochastic shift of \(F\) strengthens the incumbent. A second bidder, the
   > `<em>potential rival bidder</em>`, or the `<em>rival</em>`, has not decided whether to prepare.
   > The rival belongs to a high or a low quality class, \(j\in\{H,L\}\), and its value \(\theta\)
   > has a class distribution \(G_j\).

   The rest of the paragraph is unchanged ("It knows neither its class nor its value. …").
3. **Informed trader** (`01-setting.html:20`). This is the one place for sector expertise: "An
   outside `<em>informed trader</em>` with sector expertise knows the rival's class and remains
   uncertain about the rival's value."
4. **Market makers.** `01-setting.html:27` already reads "Competitive market makers", and it is the
   first use on the page. No change.
5. **Headline sentence** at `03-result.html:6`: replace the first sentence with "A stronger
   incumbent can induce rival entry through a more informative stock price." Do not put the
   headline into the meta descriptions or the opening answer (`template.html:67`). Those lines get
   only the term change.

## 4. Grammar fallout

- **Articles.** "an investor" becomes "an informed trader", so "an" stays. "a challenger" becomes
  "a rival". No other a/an changes.
- **Attributive "rival".** Use the possessive or "for the rival" for non-actor nouns:
  - "the rival's profit" (02:19, 02:58, 05:20)
  - "the rival's value" (01:41)
  - "the rival's accuracy" (05:9)
  - "a signal for the rival" (05:22)
  - "a win by the rival" (06:18)
  - "the lowest value of the rival" (06:22)

  Keep the compounds that the decisions name: "high-cost rival", "zero-cost rival", "high-class
  rival", "low-class rival", "prepared rival".
- **"Investor" as an attribute.** "Investor strategy" (02:32, 03:40), "investor presence" (04:37)
  and "investor signal" (05:22) become "of the informed trader" phrases. Do not write "trader
  strategy": these passages also contain liquidity traders.
- **Symbol mnemonics.** \(\alpha_I\) and \(\alpha_C\) (05:9) keep their subscripts. The letters no
  longer match the words ("I" for investor, "C" for challenger). The rule fixes the symbols; record
  this for the paper owner.
- **"Every challenger prepares" (06:24).** There is one rival, so "every rival" reads badly. Use
  "the rival prepares after every purchase". This keeps the sense, because each cluster is a
  population of sale processes.
- **Stepper buttons (01:31, 01:34).** "The investor learns" (18 characters) becomes "The informed
  trader learns" (25). The browser check runs at 320 px, so look at the wrap at that width.
  "The challenger decides" becomes shorter.
- **Headings and labels.** No h2 or h3 contains a renamed word. The row head "The investor"
  (01:70) becomes "The informed trader". The row head "The challenger does not see the price"
  (03:51) becomes shorter.
- **Chart text.** The explorer legend (102) and the annotation (137) become shorter. No chart
  legend becomes longer.

## 5. Bid sequence (content fix)

- **`01-setting.html:35`** (stepper, "Bids and sale"): "Prepared bidders learn their values and bid
  them." This implies that the incumbent learns its value at the bid stage. Replace with: "The
  incumbent bids its value. A prepared rival learns its value and bids it." The second sentence
  ("The highest admissible bidder wins …") is unchanged.
- **`01-setting.html:19`** is correct: "Paying \(C\) reveals \(\theta\) … each prepared bidder bids
  its value." The value \(\theta\) is the rival's value. No other brief line repeats the error.
- **`content.js:137`** (for the regeneration step): the incumbent row says "First buyer before
  bids". The decisions say that the incumbent knows its value before trade. Use the deck's
  corrected text when you regenerate. Lines 187 and 498 ("each prepared bidder … bids its value")
  are correct.

## 6. Build and check scripts

- **`handout/build.py`**: its checks are structural only (tags, math delimiters, ids, one h2).
  No actor word is hard-coded, so nothing breaks.
- **`handout/check_display.py`**: no actor words. It checks numbers, fonts and the palette.
- **`handout/check_browser.js:80`**: it expects the active stepper step to contain "Investors
  trade". The current label is "The investor learns", so the check fails today. It will also fail
  after the rename to "The informed trader learns". Other assertions in this file also predate the
  slot page:
  - `plots === 5` (41)
  - `main_filled.pdf` links (60-61)
  - `#sec-evidence` (85)

  Changes to the check script are the owner's decision. I propose no edit.
- **`presentation/check_deck.mjs`**: it has no word list. It fails if a web frame title or
  subtitle differs from `slides.tex` (129-131). If you edit `content.js` by hand before the deck
  changes, every renamed title fails the check. Rename the terms in the deck first, then
  regenerate. This is the plan that is already in place.
- **`presentation/build.py`** and **`deck.js`**: no actor words.

## Count

There are 168 proposed replacements on the brief page:

| File | Replacements |
|---|---|
| `template.html` | 11 |
| `01-setting.html` | 43 |
| `02-mechanism.html` | 28 |
| `03-result.html` | 17 |
| `04-path.html` | 17 |
| `05-robustness.html` | 21 |
| `06-tests.html` | 21 |
| `explorer.js` | 10 |

The count includes the headline sentence (`03:6`). It does not include the content fix at
`01:35`, the occurrences in `content.js` (listed only), or the hidden `charts.js` builders.
