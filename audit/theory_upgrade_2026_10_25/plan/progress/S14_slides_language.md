# S14 slides language pass

The prose writer (slides language) carried one language pass over the Beamer
deck (`slot/manuscript/slides.tex`), the web deck (`presentation/content.js`)
and the speaker notes (`presentation/notes.md`). Every wording change in the
decks sits in both deck files with the same words. Meaning, hypotheses,
registry keys, frame order, layout options, styling and chart code are as
they were. The opening frames Q1, Q2 and Q3 carry no number from the example,
in either deck, as the author requires.

## First set of changes

The coordinator holds this set in the repository history. Each entry names
the frame, the earlier wording, the wording that stands, and the rule.

- Q1: "Preemptive bids: a first bidder opens high, so the competitor stays
  out" -> "A first bidder bids high at the start to preempt the competitor".
  Label-colon sentence start removed.
- Q2: "Preparing is a choice: costs decide who shows up" -> "A challenger
  prepares only when preparation pays". Label-colon start and punchline
  removed.
- Q2 takeaway: "Strength deters: preparing pays less, so fewer challengers
  come." -> "A stronger incumbent lowers the return to preparation, so fewer
  challengers prepare." Label-colon start removed.
- Q3: "Trade pays, the price becomes informative, good news covers a high
  cost" and "In the example, entry rises: entry_r0 -> entry_r1_B" ->
  "Informed trade pays, so the price becomes informative. Good news then
  covers a high cost" and "So a stronger incumbent can draw the challenger
  in". One idea per sentence; the opening frames state the effect in words
  and carry no number from the example.
- F1 takeaway: "The focus is that interval: after the sale turns public,
  before the challenger decision." -> "That interval runs from the sale
  becoming public to the challenger decision." Filler removed.
- F3 takeaway: "One shift, opposite signs: the challenger keeps less, and
  proceeds depend more on class." -> "Challenger profit falls weakly. The
  target-payoff spread rises weakly." Punchline removed; weak qualifiers
  kept.
- F4: the repeated "Throughout" at the tie-rule sentence removed. Filler
  removed.
- F6 and F10 frame comments: "The benchmark" -> "The example". The example
  keeps its neutral name.
- F7 takeaway: "The shift that cuts challenger profit switches informed
  trade on." -> "The same rise in r that lowers challenger profit makes a
  correct order cover k." Concrete subject and verb.
- F10 takeaway: "Rise, then return: past the entry ceiling ..." -> "Past
  the entry ceiling ..." Punchline removed.
- F11 takeaway: "Deterrence stays at each belief." -> "At a fixed belief, a
  stronger incumbent weakly lowers gross profit." Plain claim with its
  qualifier.
- F12b: "The path is for the slot band of Corollary 1" -> "The path uses
  the slot band of Corollary 1". Concrete verb.
- F13: "Research cost a lambda^2 / 2; a success ..." -> "Research costs
  a lambda^2 / 2. A success ..." One idea per sentence.
- F16: "Outcome: the start of costly preparation." -> "The outcome is the
  start of costly preparation." Label-colon start removed.
- F16 takeaway: "Incumbent strength, the early price path and the start of
  preparation move as a set." -> "Strength, early prices and preparation
  starts must be measured together." Plain economic words.
- A4 takeaway: "Uniqueness proofs use bounds on every profile, not just on
  the candidate tuple." -> "The uniqueness argument applies the bounds to
  every profile." Positive claim in place of a not-X contrast.
- A7: "Auction inputs: B_r(pi) equals ..." -> "B_r(pi) equals ..."
  Label-colon start removed.
- A9: "The example's research inputs: a = ... Marked strengths: ..." ->
  "In the example, a = ... and the cap is ... The marked strengths are ..."
  Label-colon starts removed.
- Notes Q1, Q3, F4, F6, F7, F8, F9, F10, F11, F14, F15, F16, A4, A10, A12:
  staged openers and label starts removed ("This is the trading stage.",
  "Here is why the investor trades.", "Now the challenger's side.",
  "Welfare.", "Four predictions." and the like); the Q3 note states the
  entry effect in words in place of the two registry values, with the
  slide; the F10 and F14 notes lose "carries" metaphors ("The price carries
  the rise", "what carries the result").

## Second set of changes

This set sits in the working tree for the coordinator. Frame numbers follow
the deck labels.

- F1: "Incumbent type gives a public clue to strength. Incumbent value
  stays private" -> "The incumbent's type is public and signals its
  strength. Its value is private". Plain economic words; concrete subject.
- F2: "The challenger learns its value after preparation, not before" ->
  "The challenger learns its value only after preparation". Positive claim
  in place of a not-X contrast.
- F2: "with no link to class" -> "independent of class". Plain economic
  word.
- F3 title: "One auction, two claims, opposite responses" -> "Strength
  raises the spread and lowers challenger profit". Forced triad removed;
  the title states the claim of Proposition 1 in the example.
- F4 (Beamer deck; the web frame carries a diagram in place of this list):
  "One public order opportunity comes first. The name for it is the order
  slot" -> "One public order comes first: the order slot". Filler removed.
- F4: "No observer sees slot identity. The identity draw has no link to
  class, costs or R" (web: "the draw has no link to class, costs or R") ->
  "No observer sees who filled the slot. The draw is independent of class,
  cost and R". Plain economic word.
- F5: "since the zero cost always pays" -> "because a zero-cost challenger
  always prepares". Concrete subject and verb.
- F5: "Entry at least rho and Delta_T > 0 let the challenger recover mu
  from P" -> "Because entry is at least rho and Delta_T > 0, the challenger
  can recover mu from P". Short sentence with a concrete subject.
- F6: the gray line "The inputs illustrate the results." removed from both
  decks. Filler.
- F7: "Buy after H: expected share payoff less price. Sell after L: price
  less expected share payoff" -> "A buy after H earns the expected share
  payoff less the price. A sale after L earns the price less the expected
  share payoff". Label-colon fragments removed.
- F8: "Zero cost always pays; cost c_H pays exactly at beliefs at or past
  tau(r)" -> "A zero-cost challenger always prepares. A challenger with
  cost c_H prepares exactly at beliefs at or past tau(r)". Concrete subject
  and verb; one idea per sentence.
- F8 takeaway: "The entry ceiling r_C sits just below r_2." -> "The entry
  ceiling r_C lies just below r_2." Plain verb.
- F9: "Each condition is a strict inequality: the parts hold on an open
  set of inputs." -> "Each condition is a strict inequality, so the parts
  hold on an open set of inputs." Label-colon join removed.
- F11: "A stronger incumbent then cuts B_r(mu) at each belief: entry can
  only fall" -> "A stronger incumbent then weakly lowers B_r(mu) at each
  belief, so entry can only fall". The weak qualifier of Proposition 1
  stands in the claim; label-colon join removed.
- F11: "Frozen full orders give the same entry ..." -> "The same full
  orders at both strengths give the same entry ..." The bullet uses the
  words of the table row in both decks.
- F11: "With the price hidden, cost c_H never pays at the prior" -> "With
  the price hidden, a challenger with cost c_H never prepares at the
  prior". Concrete subject and verb.
- F12: "Lower bound: a purchase that reaches tau covers k. Upper bound: an
  order against a flat price earns at most k" -> "At the lower bound, a
  purchase that reaches tau covers k. At the upper bound, an order against
  a flat price earns at most k". Label-colon starts removed.
- F13 and A9: "research is ... and entry is ..." -> "research is ...
  Entry is ..." One idea per sentence; every registry key stands in its
  sentence in both decks.
- F13 takeaway: "Research and entry rise together; research at the cap
  holds up to the entry ceiling r_C." -> "Research and entry rise together.
  Research stays at the cap up to the entry ceiling r_C." One idea per
  sentence.
- F14 title: "The reversal survives changes to the model" -> "The reversal
  holds under changes to the model". Plain verb.
- F14 and A10: "The reversal holds with atoms or none" -> "The reversal
  holds with atoms or without atoms". Plain words.
- F14: "many classes need separation" -> "many classes need a separation
  condition". The qualifier stands in full, as in A10.
- F14: "; sale terms sit in the next frame" -> ". The next frame covers
  sale terms". Plain verb.
- F14 takeaway: "One slot and unit orders carry the result across cost,
  value and signal variants." -> "Each variant retains one slot with unit
  orders." Metaphor removed; the takeaway uses the words of the F14 note.
- F15: "Reserves (A.9): at a reserve that excludes the low class entry is
  flat; strict deterrence at rsv_deter also excludes the weak incumbent" ->
  "At a reserve that excludes the low class (A.9), entry is flat. Strict
  deterrence needs the higher reserve rsv_deter, which also excludes the
  weak incumbent". Label-colon start removed; the reserve is the subject
  that excludes, as in A12.
- F17: "Why: strength shifts a value gap to shareholders, trade pays in
  the slot, and a buy order makes high-cost preparation pay" -> "Strength
  shifts a value gap to shareholders. Trade pays in the slot, and a buy
  order makes high-cost preparation pay". Bold label removed.
- F17: "Implication: competition in the auction can create competition for
  entry, via the stock price before preparation" -> "Competition in the
  auction can create competition for entry, through the stock price before
  preparation". Bold label removed; plain word in place of "via".
- A4: "the bounds need no bound on beta past beta < 1/2" -> "the bounds
  need no condition on beta beyond beta < 1/2". Plain words.
- A5: "Each region is cut out by strict inequalities: the results hold on
  an open set of inputs." -> "Each region is cut out by strict
  inequalities, so the results hold on an open set of inputs." Label-colon
  join removed.
- A8: "entry ceiling: top posterior stops short of c_H past r_C" -> "entry
  ceiling: the top posterior stops short of c_H above r_C". Plain word.
- A8: "... join the full purchase on (r_N, r_J); from r_J the full
  purchase is alone" -> "... join the full purchase on (r_N, r_J). From
  r_J, the full purchase is alone". One idea per sentence.
- A9: "Costly research with an alternative arrival has precedent in Dow
  and Gorton 1997." -> "Costly research with an alternative arrival follows
  Dow and Gorton 1997." Concrete verb.
- A11: "Another route keeps every size on path through additive liquidity
  flow" -> "Additive liquidity flow also keeps every size on path".
  Concrete subject.
- A12: "Orders and trade costs match in the two access cases at r_1;
  access adds preparation after a purchase only" -> "Orders and trade costs
  are the same in the two access cases at r_1. Access adds preparation only
  after a purchase". Plain words; "only" sits with the order it limits, as
  in F15.

Speaker notes, second set:

- Q2: "I keep this answer." -> "That effect remains in the model." Plain
  claim with a concrete subject.
- F4: "no price reveals the class for sure" -> "no price reveals the class
  with certainty". The note uses the words of the F4 takeaway.
- F5: "the belief ... is bounded: between m(pi) and M(pi), whatever the
  investor does" -> "the belief ... is bounded between m(pi) and M(pi), for
  every investor strategy". The note uses the words of the F5 display.
- F7: "Between the two, the bounds do not settle the order regime, and the
  label says so. The weak incumbent sits on the left and the strong one on
  the right." -> "Between the two strengths, the bounds do not settle the
  order regime. The weak incumbent is on the left of the figure and the
  strong one is on the right." Filler removed; plain verb.
- F8: "the threshold sits inside the band" -> "the threshold is inside the
  band". Plain verb.
- F10: "The orders switch on at the strong incumbent and stay on. The price
  becomes informative at the strong incumbent, where the orders start." ->
  "The market is quiet at the weak incumbent. At the other two strengths,
  orders are full and the price is informative." Metaphor removed.
- F11: "Freeze the orders at the full-order profile and entry is constant
  up to the entry ceiling." -> "Keep the full orders at both strengths and
  entry is constant up to the entry ceiling." The note uses the words of
  the F11 table row.
- F13: "The figure draws Corollary 3." -> "The figure shows Corollary 3."
  Plain verb.

Bold run-in words stand where the design calls for them: defined terms at
first use (incumbent, challenger, prepare, entry, order slot), the parts of
Proposition 2 and its conditions (H1) to (H3), the step names in A6, the
component names in A3, the topic leads in F2, F16 and A12, and the letters
of the coexistence key. The mechanism chains in the F9 takeaway and the
conclusion stand, because each link is a step of the argument. The lists of
preparation tasks (diligence, finance, approvals) stand, because preparation
has those parts.

## Builds and checks

- Beamer build, from `slot/manuscript`: `latexmk -xelatex
  -interaction=nonstopmode -outdir=<scratch>/mlang/build slides.tex`. Zero
  errors, zero overfull boxes, 35 pages. The changed frames render cleanly
  at 60 dpi (F1 to F17 and the backups with changed lines read with no
  overflow; the F5 entry-rule line wraps within its bullet).
- Web build, from the worktree root: `python3 presentation/build.py` and
  `node presentation/check_deck.mjs` both pass. The check compares 34
  frames (22 main, 12 backup) on order, titles, subtitles, targets and
  links, finds all 156 printed registry keys on the web frames, and reports
  30.25 planned minutes before questions. No check was loosened.
- Language scan on `slot/manuscript/slides.tex`: 16 hits in total, the same
  count as before this set. Judged one by one: "check the books" (Q1) is
  the ordinary verb for diligence; the 14 bold-face hits are the defined
  terms and the coexistence key letters named above; "no longer predict
  entry" (F16) compares strengths above the entry ceiling, a comparative
  static across economies; the 2 "may mix" hits are the stated tie rule.
  Status, defensive, example-naming, name, interval-claim and placeholder
  counts are zero.
- Registry keys on the opening frames: the F0, Q1, Q2 and Q3 frames of
  `slides.tex` contain no registry key. The first printed key in the deck
  sits inside F3.
