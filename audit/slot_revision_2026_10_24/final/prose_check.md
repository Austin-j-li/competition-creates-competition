# Final prose check: main text of the order-slot manuscript

## Scope and method

- **Text:** the abstract (`main.tex:84-98`) and `sections/01_introduction.tex` to `sections/09_conclusion.tex` in `slot/manuscript/`, branch `slot-revision`.
- **Commit:** the review started at `c78e2c3`. During the review, two commits landed: `9d3c66e` ("Remove the result-status vocabulary from the manuscript") and `da84b08` ("Restore the full fixed-information condition and the scope of the trading bound"). I re-read every changed passage. **All locations below refer to `da84b08`.** The tree was clean apart from an untracked `slot/study_guide/`. Hits that the two new commits removed are listed in Section 6, not in the counts.
- **Standard:** `audit/slot_revision_2026_10_24/STYLE_GUIDE.md`. I applied no other house style. Each proposed replacement uses the guide's register, keeps every `\reg{}`, `\ref`, `\eqref` and citation key of its span, and adds no fact, number, mechanism or hedge. Where a replacement needs a definition, the definition comes from the appendix and the row names the source.
- **Baseline:** for each hit I searched for its wording in `2c56325` (the text the earlier scan read). "Remaining" means that the wording or pattern was already in `2c56325`. "Introduced" means that the rewrite (`0ba3a71` or `c78e2c3`) brought it in. "Partial" means that the rewrite fixed part of an earlier-scan row and left a residue.
- **Tools:** full reads of all ten files; grep for dashes, inflated words, apparatus names, tie-rule acronyms, commands and status words; a sentence-length listing (`/tmp/ccc_slot_scan/final/scripts_prose/longsent.py`); a phrase search of every action row of the earlier scan against the current text and against `2c56325` (`rows.txt`, `new.txt` in the same folder). The PDF builds cleanly at `c78e2c3` and at `da84b08` (`/tmp/ccc_slot_scan/final/build_prose/`): no undefined reference and no unknown registry key.
- **Rules kept:** I edited no repository file and wrote no test. The phrase lists and the sentence-length script print matches only; they assert nothing.
- **Location prefixes:** `main` = `main.tex`; `01` to `09` = `sections/0N_*.tex`.

## 1. Counts

| Category | Hits | Remaining | Introduced | Partial |
|---|---|---|---|---|
| 1. Defensive writing | 15 | 11 | 1 | 3 |
| 2. AI tells | 9 | 8 | 1 | 0 |
| 3. Sentences a reader must restart | 10 ranked, 8 further | ranked: 5 | ranked: 5 | 0 |
| 4. Math-paper apparatus | 8, and 2 optional | 7 (+2) | 1 | 0 |
| 5. Tour, abstract and section mismatches | 8 | 5 | 3 | 0 |

Zero counts that the brief asks about:

- Em dashes or paired dashes: 0.
- Inflated words from guide 2.10 (crucial, key, powerful, robust as praise, highlight, underscore, delve, landscape, "serves as"): 0.
- Forced triads: 0. Every list in the main text has the items that the model has.
- Ornamental end-of-sentence participles: 0.
- Tie-rule acronyms (IM, C1, CM, I0) in the main text: 0.
- One-letter equilibrium forms outside the Figure 2 note: 0.
- Equilibrium-definition condition numbers: 0. Section 2.4 says only "the six conditions".

The earlier defensive scan (63 rows, 56 action rows), against `da84b08`:

| Verdict | Rows | Count |
|---|---|---|
| Resolved | all action rows not listed below | 48 |
| Partial | 11, 16, 18, 22, 63 | 5 |
| Remaining (action not taken) | 10, 15, 52 | 3 |

The earlier scan's top ten: 8 resolved, 2 partial (Section 2).

The two measures are different. A row verdict says whether the rewrite carried out the earlier scan's action. A hit label in Section 3 says whether the quoted text was already in `2c56325`. Thus rows 16 and 18 are partial as rows, while hits D5 and D6 are "remaining", because the quoted clauses were in `2c56325` unchanged.

## 2. The earlier scan's top ten

| # | Earlier location and text (`2c56325`) | Current location and text (`da84b08`) | Verdict |
|---|---|---|---|
| 1 | main:93 "With the information in the price held fixed, entry does not rise." | main:93-94 "With the information in the price held fixed, a stronger incumbent can only lower entry." | Resolved |
| 2 | main:93-95 "entry rises weakly with incumbent strength along the informative branch" | main:94-95 "along the informative branch entry rises and then stays constant" | Resolved |
| 3 | 09:9-13 "the admissible region is exact"; "rises weakly ..., and strictly where the investor mixes"; "a branch beside the equilibrium without research" | 09:9-13: the exactness clause is gone; "beside" became "on a branch that coexists with an equilibrium without research"; "rises weakly" became "rises with incumbent strength and then stays constant; the rise is strict where the investor mixes between a purchase and abstention" | Partial: the old "and strictly where the investor mixes" qualifier comes back as a tail clause (hit D9) |
| 4 | 01:43-47 the uniqueness paragraph ("Uniqueness covers every mixed order profile ..."; "entry does not rise") | 01:44-47 "The reversal comes from the change in information that competition induces. ... a stronger incumbent can only lower entry (Section~\ref{sec:benchmark})." | Resolved |
| 5 | 01:57 "The hypotheses of the main result are strict inequalities, so they define an open set of primitives." | 01:49-59 now opens with the benchmark numbers. The open-set claim stays at 01:34, and its argument stays at 04:59-61. | Resolved |
| 6 | 01:130 "holds no stake, seeks no control, has no role in tendering, and earns only the trading residual" | 01:125 "The investor in this paper is an outside trader, with no part in the auction or in tendering, and earns only the trading residual." | Partial: two negations stay in the lead sentence (hit D7) |
| 7 | 04:42-43 the tie-rule reassurance directly after the main proposition | The intuition now follows the proposition (04:46). One plain sentence closes the discussion at 04:72-73: "Every comparison behind the result is strict, so the unique outcome in each economy is the same however ties are broken." | Resolved (guide Section 4, first point) |
| 8 | 04:160-164 the "smallest margin" paragraph | 04:163-166 gives the positive fact ((H3) holds on \((r_C,h)\)) and points to Table A.x for the margins | Resolved |
| 9 | 06:9 "The two-point cost law of Section~\ref{sec:values} is not needed." | 06:9-10 "The rise of entry in Proposition~\ref{prop:ccc} survives other preparation-cost laws, with or without atoms (Proposition~\ref{prop:atomless})." | Resolved |
| 10 | 07:50-51 and 07:101: subsections that end on "is open" | 07:101 is deleted, and Section 7 ends on reserves (07:105-107). Subsection 7.2 opens with positive scope (07:41-43) and ends on the payment sensitivities (07:54-56). `9d3c66e` also deleted the open statement that `c78e2c3` kept at the start of 7.2 (see Section 6). | Resolved |

## 3. Hits

The order within each category is by severity, then by position.

### Category 1: defensive writing

**D1. 08:15-21: the control conditions are repeated word for word from Section 4.2. Introduced (`c78e2c3`); mid.**
- Quoted: "The control holds the information that reaches the buyer fixed: the law of the class and of a signal that the challenger observes, the class value laws and the cost law are the same at both strengths. Given the class, the signal tells the challenger nothing more about either value: its own value depends on the signal only through the class, the incumbent's value is independent of the class and the signal, and the two values are independent; the cost is independent of the class, both values and the signal."
- Problem: this repeats 04:188-192. `da84b08` corrected both copies, so the repeat now also means two places to maintain. Guide 2.7: give each scope condition one home and cite the home.
- Proposed: "Proposition~\ref{prop:ccc} gives the first and third comparisons, and the fixed-information control of Section~\ref{sec:benchmark} gives the second (Proposition~\ref{prop:control})." Delete the two sentences after it.

**D2. 06:75-81: the benchmark with the accuracies of \(S(B)\), where entry falls, and an alternative tie rule in words. Remaining (row 52); mid.**
- Quoted: "With the accuracies of the signal example \(S(B)\), the benchmark has a unique equilibrium at each strength when an indifferent investor may mix over its best orders. ... Entry falls from \(\reg{p4_b_signal_r0_entry}\) to \(\reg{p4_b_signal_r1_entry}\). When an investor that is indifferent between abstention and a nonzero order must abstain, neither strength has an equilibrium."
- Problem: this is a high-impact caveat in the middle of the signals result. It restates the default tie rule (02:221), and it describes an alternative tie rule where no figure draws it (guide 2.6, 2.10).
- Proposed: move the paragraph to the Appendix A.6 paragraph on the benchmark with the accuracies of \(S(B)\). Carry `\reg{p4_b_signal_r0_buy_rate}` and `\reg{p4_b_signal_r1_sell_rate}`: no appendix file prints them at present. The paragraph at 06:83-87 keeps the reason in the main text ("at the benchmark the strong trading bound needs an accurate investor signal, and the weak bound then fails").

**D3. 04:83-88: computational bookkeeping in the main results section. Remaining (not in the earlier scan); mid.**
- Quoted: "with \(\eu\) printed upright to separate it from entry \(e(x)\), and the liquidity probability is the exact decimal \(\beta=\reg{beta_B}\). ... Every computation keeps \(\lambda\) unrounded, and every statement that depends on \(\eu\) uses interval arithmetic; Appendix~\ref{app:parameters} lists these declarations."
- Problem: these sentences answer a precision objection, and the paragraph does not need them for its economics. The note on the upright e is a typesetting remark.
- Proposed: "In the benchmark slot the largest likelihood ratio of an order is \(1+u=\eu\), and the liquidity probability is \(\beta=\reg{beta_B}\). The presence probability is therefore \(\lambda=u\beta/(1+u\beta)=\reg{lambda_B}\), with \(b=\reg{b_B}\), and the posterior bounds at the prior are \(M(1/2)=\eu/(1+\eu)=\reg{M_half_B}\) and \(m(1/2)=\reg{m_half_B}\); Appendix~\ref{app:parameters} lists these declarations and the arithmetic behind each value." Move the note on the upright e into the footnote at 02:164-170, where \(\eu\) is first defined.

**D4. 02:8-10: a pre-emption that the earlier scan already flagged. Remaining (row 15); low.**
- Quoted: "Whether a given transaction fits is a question about its chronology, and Section~\ref{sec:empirical} states how to date this interval in a given transaction."
- Problem: the rewrite added the row's text but kept the pre-emption, so "a given transaction" now occurs twice in one sentence.
- Proposed: "Section~\ref{sec:empirical} states how to date this interval in a given transaction."

**D5. 02:115-120: two outsider caveats. Remaining (row 18; one part reworded); low.**
- Quoted: "and cannot acquire the target; a holder with a full hedge counts as an outsider in this sense." and "not from information that either bidder or the target supplies."
- Problem: both clauses answer objections that the text never raises. The second is the old "Neither bidder nor the target supplies this information" in a new form.
- Proposed: "It is an outside sector specialist, such as a sector-focused long-short fund. It holds no net position in the target before trade, has no control rights, and cannot acquire the target. Its information concerns the challenger's fit with the target, and it forms that view from its own research on the target's customers, technology, and demand."

**D6. 02:19-21: a pre-emption about bids without preparation. Remaining (row 16: the rewrite changed the second sentence, not the first); low.**
- Quoted: "A buyer that does not prepare cannot bid its current expected value instead; it stays out of the sale. The challenger's cost is therefore an entry cost: payment reveals the buyer's value and permits a bid."
- Proposed: "A buyer that does not prepare stays out of the sale, so the challenger's cost is an entry cost: payment reveals the buyer's value and permits a bid."

**D7. 01:125: two negations remain in the lead sentence of the investor paragraph. Partial (row 11); low.**
- Quoted: "The investor in this paper is an outside trader, with no part in the auction or in tendering, and earns only the trading residual."
- Proposed: "The investor in this paper is an outside trader and earns only the trading residual." The next sentence carries the contrast with stakes and tendering.

**D8. 01:79-81: a stacked qualifier in the robustness tour. Remaining (row 10); low.**
- Quoted: "It also survives private signals that the buyer and the investor hold about different facts (Section~\ref{sec:signals}). In an example with its own costs and strengths, the buyer's signal is more accurate than the investor's, and the rise needs both signals."
- Proposed: "It also survives private signals that the buyer and the investor hold about different facts, including a buyer signal more accurate than the investor's, and the rise then needs both signals (Section~\ref{sec:signals})." Section 6.3 keeps the scope ("needs other costs and strengths", 06:85-87).

**D9. 09:10-11: the old "strictly where the investor mixes" qualifier comes back as a tail clause. Partial (row 63); low.**
- Quoted: "and along the informative branch entry rises with incumbent strength and then stays constant; the rise is strict where the investor mixes between a purchase and abstention."
- Proposed: "and along the informative branch entry rises with incumbent strength while the investor mixes between a purchase and abstention, and it stays constant once the high class buys for sure."

**D10. 01:35-36: a statement in the introduction about what uniqueness covers. Remaining; low.**
- Quoted: "In each economy the trading outcome and the on-path preparation outcome are unique."
- Problem: guide 2.2 says that the introduction carries no claim about what uniqueness covers. Proposition 2 says "Each economy then has a unique equilibrium outcome" (04:23).
- Proposed: "In each economy the equilibrium outcome is unique." The math audit should confirm that the "on-path" qualifier carries no content that the proposition's wording omits.

**D11. 02:221: the tie conventions, without the word "tie" and without a pointer. Partial (row 22); low.**
- Quoted: "An indifferent investor may mix over its best orders, and an indifferent high-cost challenger prepares."
- Problem: the sentence stands alone as a paragraph. A reader later meets "however ties are broken" (04:73) and a tie rule in words (06:80-81), and nothing in the text says where the other rules are recorded.
- Proposed: "When ties arise, an indifferent investor may mix over its best orders, and an indifferent high-cost challenger prepares; Table~\ref{tab:a4-ties} in Appendix~\ref{app:coexistence} records each conclusion that another tie rule changes."

**D12. 07:45-46 (also 06:42-43): stacked "weakly" in prose. Remaining; low.**
- Quoted: "A stronger incumbent weakly lowers the challenger's profit, and its effect on the spread weakly has the sign of \(1-2\omega\)." and, at 06:42-43, "weakly raises gross profit at every belief".
- Problem: guide 2.5 keeps "weakly" inside formal statements.
- Proposed: "A stronger incumbent never raises the challenger's profit, and it moves the spread only in the direction of the sign of \(1-2\omega\); the move is strict when \(\E[(R-\ell)_+]\) changes strictly and \(\omega\ne1/2\), and at \(\omega=1/2\) the spread equals \((h-\ell)/2\) at every incumbent distribution." At 06:42-43: "so a mean-preserving spread within a class never lowers gross profit at any belief."

**D13. 02:50-51: the incumbent's value is private, said for the third time. Remaining; low.**
- Quoted: "and its realized value stays undisclosed to the challenger before preparation."
- Problem: 02:35-36 ("keeps the incumbent's realized value private until it bids") and 02:174-176 ("but not \(X\), its class, its value, or the incumbent's value") say the same thing.
- Proposed: "The incumbent's value distribution is public when the sale opportunity becomes visible."

**D14. 03:126-127 and 03:139-141: restatements inside Section 3.3. Remaining; low.**
- Quoted: "but a liquidity order in the same direction is always possible, so some uncertainty about the class survives every order" (this repeats 03:87-88) and "so each class compares one gross return with the trading cost, class \(H\) the return of a purchase and class \(L\) the return of a sale" (this repeats 03:123-124).
- Proposed: at 03:126-127, "Market makers price the entry response, and the posterior bounds of Section~\ref{sec:inference} leave some uncertainty about the class after every order." At 03:139-141, "Each return depends only on the posterior and entry after its own order, so entry after the zero order enters no payoff, and the investor's problem splits by class." Keep the two appendix pointers that follow.

**D15. 02:155-157: the mechanism in negative form, after the introduction has already stated it. Remaining; low.**
- Quoted: "each class reaches each order through a liquidity trader, so no order is conclusive about the class, and the investor therefore keeps a residual advantage after every order."
- Proposed: "The bounds follow from one property of the slot: each class reaches each order through a liquidity trader, so the investor keeps a residual advantage after every order."

### Category 2: AI tells

**A1. 08:22-44 (also 01:92-93): one word, "spread", names two objects. Remaining; mid.**
- Quoted: "The spread is the difference between the conditional execution prices of a unit purchase and a unit sale. It has a class component, \(\rho\DT\) times the informed share, ..."
- Problem: Sections 3 to 7 use "the spread" for the target-payoff spread \(\DT\) (03:128, 04:55, 06:34, 07:41-52). In Section 8 the same word names the price spread, and 08:24-25 uses both objects in one sentence. A mean-preserving "spread" (06:42) is a third use.
- Proposed: call the Section 8 object "the price spread" at its definition (08:24), in the heading ("The price spread and its entry component"), and at 08:30-33 and 08:42. 01:92-93 already says "the spread between purchase and sale prices"; keep that form.

**A2. 02:5-30, main:85-88, 08:11-21: several names rotate for the challenger. Remaining; low to mid.**
- Quoted: in Section 2.1, "a further bidder" (02:6), "a prospective buyer" (02:8), "Another buyer" (02:14), "A buyer that does not prepare" (02:19), "The challenger's cost" (02:20), "A buyer knows" (02:23), "the further buyer" (02:29), all for one agent. The abstract moves from "a challenger" to "a prospective buyer" to "the buyer's acquisition profit" to "Challenger entry". In 08:11-21, "the further buyer", "prepared bidder", "the buyer" and "the challenger", "the incumbent" all occur in one paragraph.
- Proposed: in 2.1, give the name once ("Another buyer, the challenger, has not decided whether to prepare.") and then use "the challenger". In the abstract, use "a prospective challenger" and "the challenger's acquisition profit". Section 8 can keep "further buyer" and "prepared bidder" as empirical names; the fix in D1 removes its switch back to "challenger" and "incumbent".

**A3. 08:14 and 07:78: "preparation" in the place of "entry". Remaining; low.**
- Quoted: "Against a strong enough prepared bidder, preparation returns to its floor while the price stays informative." The column header "Preparation" in Table 5 (07:78) holds entry values (`\reg{p2_reserve_points_*_entry}`), and 07:97 and 07:101 read the same numbers as "entry".
- Problem: guide 2.10 says that preparation names the act and its cost, and entry names the probability.
- Proposed: "Against a strong enough prepared bidder, entry returns to its floor while the price stays informative." Change the column header to "Entry".

**A4. 03:97: a label sentence as a paragraph closer. Introduced; low.**
- Quoted: "This is the ceiling of the model."
- Proposed: see R10, which puts the name at the start of the ceiling sentence.

**A5. 02:29-30: a staged opener. Remaining; low.**
- Quoted: "The identity of the further buyer is common knowledge; what the market does not know is how well that buyer fits the target."
- Proposed: "The identity of the challenger is common knowledge, and the market is uncertain only about how well the challenger fits the target."

**A6. 01:17-18: a count-label opener, and a term used only once. Remaining; low.**
- Quoted: "The mechanism runs through two claims on the same acquisition surplus. The challenger holds the acquisition claim, what it keeps if it prepares, bids, and wins; target shareholders hold the traded claim, ..."
- Problem: the opener labels the paragraph (guide 2.1). The text never uses "acquisition claim" again.
- Proposed: "The challenger and target shareholders hold two claims on the same acquisition surplus: the challenger keeps what remains if it prepares, bids, and wins, and target shareholders hold the traded claim, what the cash second-price auction pays them."

**A7. 07:60-61: a count label. Remaining; low.**
- Quoted: "Once the reserve can exclude bidders, three events separate."
- Proposed: "Once the reserve can exclude bidders, preparation, a sale and the meeting of two admissible bidders become different events: \emph{preparation} is the event that the challenger pays its preparation cost, a \emph{sale} occurs when at least one bidder submits an admissible bid, and \emph{two admissible bidders} meet when both the incumbent and a prepared challenger meet the reserve."

**A8. 07:35: a not-X-but-Y opener. Remaining; borderline.**
- Quoted: "The information in the price, not its level, separates the two economies."
- Note: both sides name model objects, and the dividend experiment establishes the distinction, so the exception in guide 2.10 can apply. If the author wants the pattern first and the conclusion second: "A deterministic external dividend of \(\reg{p2_access_proceeds_gain}\) in the hidden-price economy equalizes the mean prices and leaves the orders and entry unchanged, so the information in the price, not its level, separates the two economies."

**A9. main:91 against 01:34 and 09:9: "parameters" and "primitives" for one set. Remaining; low.**
- Proposed: use one word throughout. "Parameters" is the plainer choice: change "primitives" to "parameters" at 01:34 ("on a nonempty open set of parameters") and at 09:9 ("on an open set of parameters").

### Category 3: sentences a reader must restart

The ranking is by failure mode: garden paths first, then references without an antecedent, then overloaded sentences.

**R1. 04:322 (also 04:263-264, 04:276, 04:299-300, 04:312): "no informed trade" as the subject reads as a negation. Introduced, except 04:276; worst.**
- Quoted: "Above \(r_N\) no informed trade fails as an equilibrium." A reader parses "nothing fails". The same trap occurs in "no informed trade ends at \(r_N\) ..., so no informed trade stops being an equilibrium above \(r_N\)" (04:263-264), in Proposition 3(a), "No informed trade and an informative equilibrium coexist exactly on \([r_A,r_N]\)" (04:276), in the figure note, "The figure labels no informed trade by N" (04:299-300), and in "so no informed trade survives as an equilibrium until \(r_N\)" (04:312).
- Note: "no informed trade" is the pattern name that guide 2.6 prescribes. Keep the name, and change the sentence where the name is a subject.
- Proposed: 04:322 "Above \(r_N\) the equilibrium without informed trade fails." 04:262-264 "Full purchases start at \(r_F\), where a full purchase that recruits earns the trading cost, and the equilibrium without informed trade ends at \(r_N\), where a unit order against an uninformative price earns the trading cost." 04:276 "The equilibrium without informed trade and an informative equilibrium coexist exactly on \([r_A,r_N]\)." 04:299-300 "The figure labels the equilibrium without informed trade N, a mixed purchase that recruits R, ...". 04:312 "so the equilibrium without informed trade survives until \(r_N\)".

**R2. 05:74: the same garden path with research. Remaining.**
- Quoted: "At the intermediate strengths, no research confirms itself:"
- Proposed: "At the intermediate strengths, the equilibrium without research confirms itself:"

**R3. 04:327-330: ordinal references, and a prepositional phrase that runs into the subject. Introduced.**
- Quoted: "Below the first of these priors even the top posterior cannot reach the threshold once a purchase can pay for itself, and from the last prior on the uninformative equilibrium fails before the prior falls below the threshold;"
- Problem: the reader reads "on the uninformative equilibrium" as one phrase, and must count back to find "the first" and "the last" of three priors.
- Proposed: "Below \(\approx\reg{piA_lo_B}\) even the top posterior cannot reach the threshold once a purchase can pay for itself, and from \(\approx\reg{pimax}\) on, the uninformative equilibrium fails before the prior falls below the threshold;" Both macros already print in the sentence before.

**R4. 01:91-93: "this entry component" has no antecedent in the introduction. Remaining.**
- Quoted: "The purchase impact exceeds the sale impact exactly when a purchase recruits the buyer (Section~\ref{sec:empirical}). In the benchmark, this entry component is \reg{ba_share_r1_B} of the spread between purchase and sale prices."
- Proposed: "A purchase raises the price by more than a sale lowers it, both measured from the price after no order, exactly when the purchase recruits the buyer (Section~\ref{sec:empirical}). The gap comes from the entry component of the spread between purchase and sale prices; in the benchmark, that component is \reg{ba_share_r1_B} of the spread." The impacts are defined at A8:42; the gap equals the entry component by 08:27-28.

**R5. 08:23-28 (also 01:91, 01:94, 09:23): "purchase impact" and "sale impact" are not defined in the main text. Remaining.**
- Quoted: "The purchase impact exceeds the sale impact exactly when a purchase recruits the buyer, and this test needs no knowledge of the auction objects."
- Problem: only A8:42 defines the two impacts (\(I_+=P(1)-P(0)\), \(I_-=P(0)-P(-1)\)).
- Proposed: "The purchase impact, the price after a purchase minus the price after no order, exceeds the sale impact, the price after no order minus the price after a sale, exactly when a purchase recruits the buyer, and this test needs no knowledge of the auction objects."

**R6. 07:54: "To see why" sits two paragraphs after the result that it explains. Remaining.**
- Quoted: "To see why, take \(R>\ell\)."
- Problem: the benchmark number (07:49) and the Bulow-Klemperer contrast (07:50-52) come between this sentence and the sign result (07:45-47).
- Proposed: move 07:54-56 to directly after 07:47, so that the subsection reads: result, why, benchmark number, literature contrast. If the author wants the guide's ending on the sensitivity argument, put the benchmark and literature sentences before the result instead.

**R7. 04:264-269: a forward reference to "the statement", and \(r_J\) listed twice. Introduced.**
- Quoted: "The remaining strength in the statement is the entry ceiling \(r_C\) ... Of the strengths that Figure~\ref{fig:coexistence} marks, \(r_A\), \(r_N\) and \(r_J\) do not depend on the slot. The figure also marks \(r_J\) and the sale threshold \(r_S\), ..."
- Problem: Proposition 3 comes after this paragraph, and "also marks \(r_J\)" repeats a strength from the sentence before.
- Proposed: "The entry ceiling \(r_C\) of Section~\ref{sec:benchmark} also enters the proposition: above it even a purchase at the top posterior cannot recruit a high-cost challenger. Figure~\ref{fig:coexistence} also marks \(r_J\) and the sale threshold \(r_S\), which bound the mixed patterns that the figure draws with the informative branch; \(r_A\), \(r_N\) and \(r_J\) do not depend on the slot, and Appendix~\ref{app:coexistence} defines every marked strength and every pattern in the figure."

**R8. 06:46-48: "high-group class" and "the low group" without a definition. Remaining.**
- Quoted: "Separation asks for a gap between the proceeds of each high-group class and every feasible posterior mean, and the same gap for the low group."
- Proposed: "Separation splits the classes into a high group and a low group, and it asks for a gap between the proceeds of each high-group class and every feasible posterior mean, and the same gap for the low group." The split is in A6:285-286.

**R9. 04:244-246: "The probability in Proposition A.x" points back across a paragraph and a table. Introduced.**
- Quoted: "The probability in Proposition~\ref{prop:control} is \(\reg{p4_control_crossing_r0_r1}\) from \(r_0\) to \(r_1\) and ..."
- Proposed: "Entry falls by the probability that the cost lies between gross profit at the two strengths, which is \(\reg{p4_control_crossing_r0_r1}\) from \(r_0\) to \(r_1\) and \(\reg{p4_control_crossing_r1_r2}\) from \(r_1\) to \(r_2\) (Proposition~\ref{prop:control}): with information fixed, entry stays constant from \(r_0\) to \(r_1\) and falls above the entry ceiling."

**R10. 03:93-97: "follows no price", then a label closer. Introduced (closer); remaining (first sentence).**
- Quoted: "A preparation decision that needs a belief above the top posterior therefore follows no price: when \(g_H\ge g_L\), gross profit does not fall with the belief, so once gross profit at the top posterior falls below \(c_H\), no order recruits a high-cost challenger, in or out of equilibrium. This is the ceiling of the model."
- Proposed: "No price can therefore support a preparation decision that needs a belief above the top posterior. This gives the ceiling of the model: when \(g_H\ge g_L\), gross profit does not fall with the belief, so once gross profit at the top posterior falls below \(c_H\), no order recruits a high-cost challenger, in or out of equilibrium."

**Further restart candidates (outside the ten):**

- 04:158-161 (introduced): "The band between the two thresholds has the width it has because ..." Proposed: "The threshold rises slowly with strength, and this sets the width of the band: a high-class challenger outbids every incumbent on the path, and its expected payment \(r/2+p^2/(2r)\) rises by less than one half per unit of strength, a change that is small next to the gap \(g_H-g_L\) in Table~\ref{tab:payoffs}."
- 05:21-24 (remaining): a scope condition ("the prior is \(1/2\) throughout this section") hides in a sentence about conjectures, and the next sentence holds three claims. Proposed: "Market makers and the challenger do not observe the research choice, so they price and decide at a conjectured intensity; throughout this section the prior is \(1/2\). In an equilibrium with research, the conjectured intensity is the investor's best research choice at the equilibrium prices and entry rule, and the order after a success is optimal, including after a deviation from zero research."
- 07:15-17 (remaining): "Each added preparation contributes its gross profit minus its cost, and also the sales that the reserve would otherwise block; ... so each term is positive." The object "the sales" does not fit "contributes", and "each term" has no antecedent. Proposed: "Each added preparation adds its gross profit minus its cost to net surplus, together with the value of any sale that the reserve would otherwise block; a challenger prepares only when its expected gross profit covers its cost, so no added preparation lowers net surplus." See also Section 5: the appendix says "nonnegative" where this sentence says "positive".
- 08:37-39 (remaining in part): "and the investor's incentives limit the shares that the counts allow: at \(r_1\), the shares that the counts and the incentives allow form the interval from ..." Proposed: "and the investor's incentives narrow the shares that the counts allow: at \(r_1\), the shares consistent with both form the interval from \(\approx\reg{theta_min_counts_B}\) to \(\reg{theta_max_full_eq_r1_B}\)."
- 04:189-192 (corrected in `da84b08`): the full control condition is one sentence with a colon, three commas and a semicolon. A split that keeps every condition unchanged: "Given the class, the signal tells the challenger nothing more about either value. Its own value depends on the signal only through the class; the incumbent's value is independent of the class and the signal, and the two values are independent. The cost is independent of the class, both values and the signal." The math audit owns the content.
- 09:9 (remaining): "The comparison holds with unique outcomes ..." The reader cannot tell which comparison. Proposed: "The comparison of the weak, strong and very strong incumbent holds with unique outcomes on an open set of primitives."
- 01:34-36 (remaining): "one with a very strong incumbent at which recruitment stops". Proposed: "against which recruitment stops".
- 04:13-17 (remaining): the frame sentence of Proposition 2 has about 75 words of hypotheses in words. Guide 2.1 accepts 35 to 45 words for a hypothesis sentence. Proposed: end the "Let" sentence after "\(F_2\) strengthen \(F_1\) in the same sense", then "Let \(0<\pi<1\), \(0<\rho<1\), \(k>0\) and a slot \((\lambda,\beta)\) be given, and suppose that ...". This also removes the second frame verb "Fix" (P7).

### Category 4: math-paper apparatus

**P1. 02:72-73: a part letter of a proposition whose main-text statement has only parts (a) and (b). Remaining.**
- Quoted: "Appendix~\ref{app:payoffs} characterizes the weakest restriction of this kind in Proposition~1(c)."
- Proposed: "Appendix~\ref{app:payoffs} characterizes the weakest restriction of this kind: when neither class has a value atom at the reserve, the spread rises under every strengthening exactly when ..." This joins the sentence that follows.

**P2. 04:186, 04:259, 04:272: "Proposition~\ref{prop:region}(a)", a part letter of an appendix result, three times, once inside Proposition 3. Remaining.**
- Proposed: 04:186 "Panel~(b) shows the band of Table~\ref{tab:region} for the top posterior." 04:258-259 "for every slot in the band of Section~\ref{sec:benchmark}". In the Proposition 3 statement, use words: "any slot whose top posterior \(M(1/2)\) lies between \(\tau(r_1)\) and \(\tau(r_2)\)". The math audit should confirm the range of \(\beta\): A4:6-7 allows \(0<\beta<1/2\), and Proposition A.x(a) assumes \(\beta\le1/3\).

**P3. 04:330: a corollary by name where words do the job. Remaining.**
- Quoted: "Corollary~\ref{prop:priors} in Appendix~\ref{app:coexistence} gives the coexistence set at every prior."
- Proposed: "Appendix~\ref{app:coexistence} gives the coexistence set at every prior."

**P4. 03:60-64: a proof step as the subject, and a command. Remaining.**
- Quoted: "The proof works one incumbent value at a time. ... Read the integrand as slices \(D(y)\,dy\) of the class value gap ..."
- Proposed: "At one incumbent value \(R\) that meets the reserve, the target receives \(\min\{R,\max\{\theta,p\}\}\), and the expected class difference in proceeds is \(\int_p^RD(y)\,dy\). Each slice \(D(y)\,dy\) of the class value gap at a level \(y>p\) reaches the target when the incumbent outbids the challenger at that level and pays its bid, and it stays with the challenger otherwise."

**P5. 04:165: proof talk about which part uses which hypothesis. Remaining.**
- Quoted: "parts~(i) and~(ii) of Proposition~\ref{prop:ccc} do not use (H3)."
- Proposed: "parts~(i) and~(ii) of Proposition~\ref{prop:ccc} hold without the ceiling."

**P6. 05:29: an imperative "write". Introduced.**
- Quoted: "At intensity \(\lambda\), write \(M_\lambda\) for that top posterior ..."
- Proposed: "At intensity \(\lambda\), I write \(M_\lambda\) for that top posterior ..."

**P7. 07:5-7: commands in expository prose. Remaining.**
- Quoted: "Hold the incumbent at \(F_1\) and compare the equilibrium of Proposition~\ref{prop:ccc} with that of an economy in which the challenger does not see the price."
- Proposed: "At the strong incumbent \(F_1\), I compare the equilibrium of Proposition~\ref{prop:ccc} with that of an economy in which the challenger does not see the price."

**P8. 04:12-14 and 04:272: proposition frames other than one "Let ... and suppose that". Remaining.**
- Proposition 2 uses "Let ..., let ..., and let .... Fix ... and suppose that"; Proposition 3 opens with "Take". Proposed: see the last item of the further restart candidates for Proposition 2. For Proposition 3: "Let the auction be the benchmark auction at the prior \(1/2\), and let the slot lie in the band ..." (with the wording of P2).

**Optional (allowed by the guide; listed for completeness):**

- 02:198-199: "Definition~\ref{def:equilibrium} in Appendix~\ref{app:proofs} states the six conditions in full." Guide 2.6 allows this single pointer. Optional words: "Appendix~\ref{app:proofs} states the formal definition."
- 03:5: "Consider a prepared challenger with value \(\theta\ge p\)." This command opens a derivation, which guide 2.10 allows. Optional: "A prepared challenger with value \(\theta\ge p\) pays \(\max\{p,R\}\) if it wins; if it loses, the incumbent pays \(\theta\)."
- Cross-listed, not counted again: the typesetting note at 04:83-84 (D3), and the tie rule in words at 06:80-81 (D2).

### Category 5: mismatches between the tour, the abstract and the sections

**T1. 01:61-62: the tour credits Section 4.3 with a set that it does not give, over a range that nothing covers. Remaining; mid.**
- Quoted: "Section~\ref{sec:coexistence} gives the complete equilibrium set between and beyond the benchmark strengths."
- Problem: Section 4.3 says that Appendix A.4 lists the complete set (04:259, 04:273-274). Proposition 3 and A.4 cover the path \([r_0,r_2]\) only (A4:6), so "beyond" the benchmark strengths has no support in 4.3.
- Proposed: "Informative and uninformative equilibria coexist on an interval of strengths (Section~\ref{sec:coexistence}), and Appendix~\ref{app:coexistence} lists the complete equilibrium set along the benchmark path."

**T2. main:92-93 and 01:38-40, against 04:63-67 and Proposition 2(ii): the ownership rise without its condition. Remaining; mid.**
- Quoted: abstract, "Challenger entry rises, and so does the probability that a challenger from the high-value class acquires the target." Introduction, "the probability that a challenger from the high-value class owns the target rises with it."
- Problem: Section 4.1 says that "Ownership needs its own condition when the high class can lose to the incumbent". Proposition 2(ii) is an "if and only if". The abstract sentence reads as an existence claim on an open set. The introduction sentence describes the outcome of the main result as if no condition applied. Guide 2.2 keeps any qualifier without which a sentence is false. The math audit owns the verdict on truth.
- Proposed (introduction): "... so entry rises even though acquisition profit falls at every fixed belief, and under a condition on the high class's chance to win, which the benchmark meets, the probability that a challenger from the high-value class owns the target rises with it."

**T3. 01:134-138: the roadmap. Remaining; low to mid.**
- Quoted: "Sections~\ref{sec:research} to~\ref{sec:empirical} cover research, robustness, sale terms and empirical implications ... Appendix~\ref{app:proofs} states the results of Sections~\ref{sec:robustness} to~\ref{sec:empirical} in full and proves every result."
- Problem: Section 5 says that the appendix gives each of its results in full (05:26-27), and A.4 holds the full statement of Proposition 3. Section 7 is "Welfare and sale terms".
- Proposed: "Sections~\ref{sec:research} to~\ref{sec:empirical} cover research, robustness, welfare and sale terms, and empirical implications, and Section~\ref{sec:conclusion} concludes. Appendix~\ref{app:proofs} states the full form of Proposition~\ref{prop:coexistence} and the results of Sections~\ref{sec:research} to~\ref{sec:empirical} in full, and proves every result."

**T4. 01:52-54: the benchmark paragraph repeats the main-result paragraph. Introduced; low.**
- Quoted: "Against a strong enough incumbent, entry returns to its floor while the price stays informative, so entry is non-monotone in strength;"
- Problem: 01:40-42 already says this. Guide 2.2 gives this paragraph the numbers of the tour.
- Proposed: "In the benchmark, high-cost preparation stops above the entry ceiling, the strength \(r_C\approx\reg{rC_B}\)."

**T5. 01:76-81 against Section 6: the order of the robustness results. Remaining; low.**
- The tour goes classes and priors, then many classes, then costs, then signals. Section 6 goes costs (6.1), classes (6.2), signals (6.3), and 06:3 lists them in that order.
- Proposed: "The rise in entry survives other laws of preparation costs, with or without atoms (Section~\ref{sec:costs}). For every prior and every pair of classes that satisfy the class ranking and differ above the reserve, the reversal holds at some incumbent strengths and costs (Section~\ref{sec:classes}); with more than two classes, it holds under a separation condition. ..." Then the signals sentence of D8.

**T6. 01:76 against 06:27-28: two wordings for one class condition. Introduced (06); low.**
- Quoted: "classes that satisfy the class ranking and differ above the reserve" (introduction); "The classes satisfy the class ranking~\eqref{eq:classes} and have different means" (Section 6.2).
- Note: under the class ranking the two conditions are equivalent: with first-order dominance and both supports above the reserve, the classes differ exactly when their means differ. Use one wording in both places.
- Proposed: at 06:27-28, "The classes satisfy the class ranking~\eqref{eq:classes} and differ above the reserve, and the reserve, the prior, the zero-cost probability and the slot are arbitrary." This is the introduction's form; 06:33 already uses "differ above the reserve".

**T7. main:91-92, 01:35-36, 04:23, 09:9: four wordings of the uniqueness claim. Remaining; low.**
- The four forms are "unique trading and preparation outcomes", "the trading outcome and the on-path preparation outcome are unique", "a unique equilibrium outcome" and "unique outcomes".
- Proposed: apply the D10 text at 01:35-36 ("In each economy the equilibrium outcome is unique."). The conclusion's "unique outcomes" (09:9) is then consistent with it, and the abstract's "unique trading and preparation outcomes" (main:91-92) can stay, because it names the two outcomes in plain words.

**T8. 04:256: the coexistence opener ties Proposition 2 to the benchmark strengths. Introduced; low.**
- Quoted: "Proposition~\ref{prop:ccc} compares the weak and strong economies at \(r_0\) and \(r_1\)".
- Problem: Proposition 2 is stated for general \(F_0\), \(F_1\) and \(F_2\).
- Proposed: "At the benchmark, Proposition~\ref{prop:ccc} compares the weak and strong economies at \(r_0\) and \(r_1\), and between those strengths an informative equilibrium coexists with an uninformative one."

## 4. Items checked and found consistent

- The intro tour order (main result, control, benchmark numbers, coexistence, research, robustness, welfare and sale terms, empirical) matches the abstract order and the section order, apart from T5.
- Coexistence lies between the two economies: \(r_N=\reg{rN}\approx1.748<r_1=3\).
- The window of priors with the same start of coexistence (\(\approx0.396\) to \(\approx0.641\)) contains the benchmark prior \(1/2\) (01:66 against 04:325-327).
- The \(S(B)\) example has a buyer signal more accurate than the investor's (\(d=0.75>a_T=0.70\)), as 01:80-81 says.
- The strength \(1.60\) in the two-cluster paragraph lies in \((r_F,r_N)=(1.467,1.748)\) (08:61-66).
- The research tour (01:68-74) matches Proposition 4 and the abstract. The welfare qualifiers ("in the strong-incumbent economy" in the abstract and introduction, "in the recruitment region" in the conclusion) are consistent in substance: under (H1), gross profit at the prior against \(F_1\) is below \(c_H\).
- The kept contrasts of guide 2.10 are in place, once each: "a holder through the sale receives sale proceeds, not the interim price" (01:32, 07:24), "Public incumbent strength is a distribution, not a bid" (02:32), and the control row note (04:236).

## 5. For the math audit (outside this brief)

- 07:17 says "so each term is positive". A7:45 says "Each term is nonnegative, and \(w_H=w_L+\Delta_1\ge\Delta_1>0\), so the gain is positive." The main-text sentence states a stronger property for each term.
- T2 (ownership in the abstract and introduction) and D10 (the "on-path" qualifier) need a mathematical verdict.
- P2: the range of \(\beta\) in the band that Proposition 3 cites.

## 6. Changes after `c78e2c3` that bear on this check

`9d3c66e` removed every status word from the main text: the proposition titles, the per-sentence tags, the table note in Table 5, the method sentences after Propositions 3 and 4, and the open statements. Before that commit, I counted status tags at `c78e2c3` against `2c56325`: Section 6, 11 against 4; Section 7, 7 against 2; Section 8, 10 against 1. That exceeded guide 2.7 ("once for each cluster"). The commit removes this finding. It also removes two restart hits: "under this rule" before the rule existed (old 07:43-44), and an open sentence that repeated the Figure 3 note (old 05:131).

The commit departs from the guide in four places. These decisions came after the reviewed commit, and I do not count them as defects:

- Guide 2.4 and 2.7 put the status in each proposition title and once in each cluster of prose results. The main text now carries no status.
- The Figure 3 note (05:143-144) says that the gray band "marks the interval \((r_N,r_U)\) between the two cap ranges". It no longer says what the band means, so a reader cannot tell why the axis breaks there. One clause would fix this without a status word, for example: "where the appendix does not characterize the equilibrium set with research".
- Subsection 7.2 no longer says that the trading and preparation equilibrium under the bargaining rule is not solved. Guide Section 4 (fifth point) kept that statement, because positive scope alone can make a reader assume that the trading equilibrium follows.
- The two-cluster paragraph (08:61-62) no longer says that equilibrium selection is open. Guide 2.7 names this paragraph as the one home of that scope, because selection limits a test that a reader might run.

`da84b08` corrected the control condition in 04:189-192 and 08:18-21. D1 stays, because the condition still prints twice.
