# Language decisions, 29 October 2026

Austin approved these on 29 October 2026. They apply to the order-slot paper, the slides, the
speaker script, the comparison note, the website brief and the web slides. Background:
`recommendation.md` in this folder.

## Actor names

| Object | Old words | New word (first use) | New word (after) |
|---|---|---|---|
| Bidder that is already prepared | first buyer, incumbent, prepared buyer | incumbent bidder | incumbent |
| Bidder that decides whether to prepare | second buyer, challenger | potential rival bidder | rival |
| Model actors in general | buyer, buyers | bidder, bidders | bidder, bidders |
| Financial actor that knows the class | investor, informed investor, specialist investor | informed trader | informed trader |
| Exogenous order | liquidity trader | liquidity trader (no change) | liquidity trader |
| Price setters | market makers | competitive market makers | market makers |

Rules:
- Each document has one first-use definition. The paper defines the names in Section 2 and can
  name them in the introduction. The slides define them on the first model frame.
- "Rival" is the permanent name before and after preparation. "Entry" is the decision to
  prepare. "Entrant" only describes participation status, not the actor.
- Compounds follow the noun: challenger entry -> rival entry; the challenger's cost -> the rival's
  cost; a high-class challenger -> a high-class rival; incumbent strength stays.
- "Buyer" stays only where the text means any acquirer outside the model (for example an
  institutional sentence about who buys companies). Inside the model, use "bidder".
- "Specialist" is not an actor name. Describe sector expertise once in words ("an informed trader
  with sector expertise"). Glosten and Milgrom use "specialist" for the market intermediary.
- Do not shorten "informed trader" to "trader" when a liquidity trader is in the same passage.
- Class words stay as they are ("the high class", "class j"). Do not add "synergy" where the text
  does not already use it.
- "Preparation cost", "incumbent strength", "entry" keep their present meanings.

## Definition text

Paper, Section 2 (adapt the grammar to the paragraph; keep the sense):
> One bidder is already prepared; I call it the incumbent bidder, or the incumbent. It is the
> party that approached the target or a bidder that has completed diligence. A second bidder, the
> potential rival bidder, or the rival, has not decided whether to prepare.

Slides, label heads on the first model frame: **Incumbent** (prepared, no further cost) and
**Rival** (sees the price, then decides whether to prepare). Slides use no first person.

Headline sentence, where the documents state the main claim in one line:
> A stronger incumbent can induce rival entry through a more informative stock price.

## Content fix

`overleaf/slot/sections/02_model.tex` near lines 165-169 says "Prepared bidders then learn their
values". The incumbent knows its value before trade. Change the clause so that only the rival
learns its value when it prepares. Apply the same fix wherever the slides or the website repeat
the sequence.

## Do not change

- Mathematics, symbols, macro names, `\label`/`\ref`/`\hypertarget` keys, `\reg{...}` keys,
  registry numbers, bibliography entries, direct quotations of other authors, file names.
- Code identifiers, CSS classes, HTML ids, JSON keys, URL anchors. Change visible words only.
- The Laplace projects (`overleaf/paper`, `overleaf/talk`, `/laplace/` on the website).
- Words that this table does not cover. This is a terminology pass, not a rewrite.
