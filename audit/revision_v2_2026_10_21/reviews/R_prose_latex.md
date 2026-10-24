# Review R: prose and LaTeX hygiene of the revised manuscript

Scope: `overleaf/paper-revision/main.tex` and `online_appendix.tex` at commit `ac4e37e` (base `9b9bf3c`).
Logs and PDFs: `overleaf/paper-revision/build/`. The manuscript was not edited.
Line numbers refer to the files at `ac4e37e`. "OA" is `online_appendix.tex`.

Method. I read the two logs, the 46 embedded bibliography records, and every `\citeproc` call.
I read the main text (lines 126 to 1410) in full, and the new Appendix A passages and the new OA passages that the main text depends on.
I flagged sentences over 30 words by script on the added lines of the diff.
For page savings I compiled scratch copies in `/tmp` (not in the repository) with changed spacing.

Counts: 14 "should fix" items (S1 to S14) and 16 "minor" items (M1 to M16).

## Part 1. LaTeX

### Build logs

| Document | Pages | Errors | Warnings | Overfull | Underfull | Font and hyperref |
|---|---:|---:|---:|---:|---:|---|
| `main.tex` | 90 | 0 | 0 | 0 | 0 | none |
| `online_appendix.tex` | 59 | 0 | 0 | 0 | 5 | none |

- Both logs have no undefined reference, no undefined citation, no multiply defined label, and no "Rerun" request.
- The "Font shape ... will be scaled" lines (106 in `main.log`, 110 in the OA log) are information messages from `newtxtext`. They need no fix.
- `pdffonts` shows every font embedded in both PDFs. There is no Type 3 font. The TrueType fonts in `main.pdf` come from the figure PDFs.
- `hyperref` gives no warning. Link colour is set once in `\hypersetup`.

### The five underfull boxes (OA log lines 1202, 1216, 1223, 1230, 1244)

All five already exist in the base build. The cause is long `\texttt` names that have no break point.

| Log line | Place | Fix |
|---|---|---|
| 1202 (badness 1320) | OA line 2618, C.2, `\texttt{correspondence.csv}` | Mild. Add `\allowbreak` after the dot, or accept it. |
| 1216, 1223, 1230 (10000) | `tables/table_reserve_details.tex` lines 24 and 25, the "Complete parameter identity" note | The generated string has break points at `\|` and `\_`, but none at `;`, `,`, `=`, `:`. The renderer must write `\allowbreak{}` after `;` and `=` in this note. |
| 1244 (10000) | OA line 3118, C.6 data dictionary, `two_admissible_bidders_probability` | See the preamble fix below, or write the list as a `description` list. |

Preamble fix for all `\texttt` names with underscores (one line in `online_appendix.tex`, after line 125):

```latex
\renewcommand{\_}{\textunderscore\allowbreak{}}
```

This gives a break after each underscore. It does not change the output elsewhere. The table fix must be made in the renderer (a change outside this review).

### Bibliography format (46 embedded records in `main.tex`, lines 1415 to 1640)

1. The records use one scheme: Chicago author-date, inline `\emph{}` for journal titles, `{``...''}` for article titles, DOI as `\url`.
   Page ranges follow the Chicago rule (`1431--63`, `2481--2513`). The 16 new records follow the 30 old ones.
2. Two format differences remain (see M1 and M2): "The American Economic Review" against "American Economic Review", and a publisher place on one book only.
3. Source line wrapping differs (new records wrap at 72 characters, old ones do not). This has no effect on the PDF.
4. The two OA records (lines 3898 and 3904) are byte-equal to the records in `main.tex`.

### The five uncited records (S7)

See S7 below. Each gets a sentence, or the record goes.

### `\citeproc` display text against the entries

All 41 cited keys match their records: author names, "et al." rule (three or more authors), and year.
Spot checks: Bulow et al. 1999 (three authors), Smith and Sørensen 2000 (macro `S{\o}rensen` renders correctly), Foucault and Frésard 2014, Pernoud and Gleyze 2026 (the record has two authors), Carlin et al. 2026 (five authors).
Seven narrative citations show the year only (`Dow et al. (2017)`, `Edmans et al. (2015)`, `Betton et al. (2014)`, `Lin et al. (2025)`, `Clark (1973)`, `Kyle (1985)`, `Bulow and Klemperer (1996)`). The author names are in the running text and agree with the records.
No mismatch found.

## Part 2. Prose, "should fix"

### S1. The abstract is hard for a general finance reader
File: `main.tex:129-146`.
Problems:
- "On an open set of primitives" and "price experiment" are theory jargon.
- The first and second sentences name the mechanism, but the abstract never says that the investor sees the challenger's quality class.
- The sentence "On an open set of primitives, strengthening the incumbent changes uninformative prices into informative prices, and the trading and preparation outcomes in each economy are unique" has 35 words.
- "Holding the price experiment fixed restores deterrence" has no meaning for a reader who has not read Section 4.

Replacement (the whole abstract; 11 sentences; each is at most 20 words):

> A stronger incumbent bidder can attract a challenger by making the target's stock price more informative. I study a takeover auction in which a prospective buyer sees the price before it pays to prepare a bid. A stronger incumbent lowers the buyer's acquisition profit at every belief about its quality. It also makes the proceeds of target shareholders more sensitive to that quality. This raises the return to trading on information about the buyer. For a set of parameters with positive measure, a stronger incumbent turns an uninformative price into an informative one. In each economy the trading and preparation outcomes are unique. Challenger participation rises, and so does the probability that a challenger from the high-value class acquires the target. If the information in the price is held fixed, stronger competition lowers participation. The reversal also holds when the buyer knows more about its own fit than the investor does. In the strong-incumbent economy, access to prices raises expected target proceeds and acquisition surplus net of preparation costs.

### S2. Section 2.2 states an independence that contradicts the model
File: `main.tex:360-362`.
The text says "The class and value of the challenger, the incumbent's value, the preparation cost, and noise demand are mutually independent". The value is drawn from `G_j` given the class, so class and value are not independent.
Replacement:

> The cost \(C\), the incumbent's value \(R\), and noise demand \(Z\) are independent of each other and of the challenger's class and value. The value depends on the class only through \(G_j\). The cost therefore carries no information about the class or the value.

### S3. Section 2.3 and Section 5.1 state the same facts twice (brief R18)
Repeated content, with lines:

| Fact | Section 2.3 | Section 5.1 |
|---|---|---|
| Posterior log odds under full orders: `logit π + (2/b) max{-1, min{x,1}}` | 408-410 | 1074-1075 |
| Gaussian: linear log odds, no finite score bound | 411-416 | 1076-1078 |
| The class `|(log f)'| ≤ L` | 418-421 | 1052-1055 (and A.4, 2372) |
| Laplace is the extreme member (thinnest tails, most informative) | 422-425 | 1060-1064 |
| Logistic belongs to the class | 420-421 | 1080 |
| Exponential-difference construction of Laplace noise | 427-431 and 463-466 | none |

Fix. Keep the technical role of the Laplace law and the class in 2.3. Keep the log-odds formula, the Gaussian contrast, and the extreme-member claim in 5.1 only.
Replacement for `main.tex:380-425` (from "Here \(V_T\)" to "(Section 5.1)."):

> Here \(V_T\) is the terminal payoff of a target share and \(Z\) is independent noise demand with a Laplace density. Up to a constant, its logarithm is \(-|z|/b\), with slope \(\pm1/b\). For each pair of feasible orders, the likelihood ratio of a flow then lies in \([e^{-2/b},e^{2/b}]\). No order flow is conclusive, in the sense of bounded private beliefs (Smith and Sørensen 2000). Each posterior stays in the interval \([m(\pi),M(\pi)]\) of Section 3.2, so the investor keeps a residual advantage at each flow. A change in the order also changes the flow density by at most the fraction \(1/b\) of its level. With \(b>1\), this score bound gives a lower bound on marginal trading profit on the full order interval. The bound covers mixed orders and each deviation, and it gives uniqueness in Proposition 2. Every density with \(|(\log f)'|\le 1/b\) has the same two properties. Laplace noise is the extreme member of this class (Section 5.1), and Proposition A.5 states Proposition 2 for the whole class.

Replacement for `main.tex:427-440` (the "Three standard models" paragraph):

> Three standard models give a Laplace law. Net noise demand is Laplace if buy volume and sell volume are independent exponential variables with equal means. It is Laplace if it is Gaussian with an exponential variance (Kotz et al. 2001), as with a random number of liquidity traders. It is Laplace if noise flow is a Brownian motion that stops at an independent exponential time, such as the arrival of public news (Clark 1973). Every member of the class has tails at least as fat as an exponential tail, and asset returns also have fat tails (Cont 2001). The results rest on tail weight and bounded inference.

(The last sentence replaces "The class claim is therefore about tail weight and bounded inference, not about a fit of one law to noise demand." It is the same content without the negation.)
Then delete the second statement of the exponential construction: in `main.tex:463-466` shorten "With independent exponential amounts of mean \(b\), their net demand has exactly the Laplace density in \eqref{eq:paper-2}." to "Their net demand is Laplace, as above."
Section 5.1 (`main.tex:1052-1085`): replace the first three paragraphs with:

> The reversal holds for the class \(\mathcal C_L\) of Section 2.3: the positive, absolutely continuous densities with \(|(\log f)'|\le L\) almost everywhere, where \(0<L<1\) and \(b=1/L\). Proposition A.5 extends the equilibrium comparison to this class. Its upper cost restriction uses the supremum of the posterior under full orders, which need not be attained.
>
> Laplace noise is the extreme member of the class. Among laws with median zero, it has the thinnest tails at a fixed score bound. It gives the most informative flow experiment at every pure order profile. The price construction in Online Appendix A.6 preserves this comparison under its stated conditions, and Online Appendix A.6 proves both claims.
>
> Under full orders, the Laplace log odds relative to the prior odds equal \((2/b)\max\{-1,\min\{x,1\}\}\). This is the Gaussian log odds with variance \(b\), clipped at \(\pm 2/b\). Gaussian noise has no finite score bound, and its posterior bounds do not lie strictly inside \((0,1)\).

Savings: about 0.8 page in 2.3 and 0.5 page in 5.1 (double spacing).

### S4. One word for the cost types, one for the classes; "buyer" and "challenger"
Two pairs of labels collide.
- "low-cost" and "low-value" both start with "low". The text also says "the other type's cost" (line 354) and "high- and low-type" (line 862), while the classes are called "classes" (the caption of Figure 2, line 1004, says "high- and low-type").
- "buyer" (49 uses in the main body) and "challenger" (95) name the same agent. Examples: 2.1 "Another buyer has not decided" (line 249); 4.2 "The buyer uses its prior" (line 949); 5.3 "the buyer observes \(Y\)" (lines 1177-1178).

Proposal (global, then check each hit):
1. Use "quality class" and "high class" and "low class" for `j`. Use "cost type" only if a noun is needed. Use "zero-cost" and "high-cost" for the realized cost. Replace "low-cost" by "zero-cost" in the eight places in the main body: lines 198, 354, 356, 693, 781, 830, 856, 1133. The Appendix A text has four more (lines 1845, 1981, 2014, 2072) and the OA has one. (The form "zero-cost" is already used in 5.3 and in the OA, 15 uses.)
2. Line 354: "The other type's cost is zero: a low-cost challenger is a ready buyer whose diligence costs nothing at the margin." becomes "The low cost is zero: a zero-cost challenger is a ready buyer whose diligence costs nothing at the margin."
3. Line 1004, caption of Figure 2: "high- and low-type support magnitudes" becomes "support magnitudes of the high and low classes".
4. Use "challenger" for the agent that decides about preparation and "incumbent" for the prepared bidder. Use "buyer" only in a general sense ("a buyer that declines to prepare"). Change "buyer" to "challenger" in lines 949, 1177-1178 (5.3), and 1376 (Section 7) where it names the entrant. Appendix A has the same pattern (lines 1866, 2004, 2036, 2093, 2099, 2825, 2840, 2984, 3084, 3180, 3230).

### S5. Introduction, line 207: a 34-word sentence that omits a condition (brief R21)
`main.tex:207-208` says the reversal holds "for every prior and every pair of classes with stochastically higher values in the high class and equal chances of a value below the reserve". Proposition 2 also needs the classes to differ above the reserve (`\Gamma>0`).
Replacement:

> The reversal needs no special prior and no point masses. It holds at some incumbent strengths and costs for every pair of classes that differ above the reserve, when the high class has stochastically higher values and both classes are equally likely to fall below the reserve.

### S6. Introduction, line 213: the entry cost does not reveal the value
`main.tex:213`: "Its pre-entry information indexes the distribution of its value, and the entry cost reveals the value". In the model, paying the cost reveals the value; the cost itself is independent of it. Replacement:

> Its pre-entry information indexes the distribution of its value, and paying the entry cost reveals the value.

### S7. Five uncited records: cite at a natural place, or delete
The facts below about each source come from the records and from the citation check of the brief. Confirm the sentence against the paper before you keep it.

| Record | Where | Replacement sentence |
|---|---|---|
| Kotz et al. 2001 | Section 2.3, "Three standard models" (line 429) | Added in S3: "It is Laplace if it is Gaussian with an exponential variance (Kotz et al. 2001), ..." |
| Vickrey 1961 and Krishna 2010 | Section 2.2, line 367 | "Both bidders use truthful, weakly dominant bids (Vickrey 1961; Krishna 2010, Chapter 2), ..." Check the chapter number before use; without it, cite "Krishna 2010" only. |
| Edmans 2009 | Introduction, lines 217-220 (the stake paragraph) | "... and large holders trade, monitor, or intervene as prices feed back to firm decisions (Edmans 2009; Maug 1998; Back et al. 2018; Edmans et al. 2015, Section II.E)." |
| Ye 2007 | Section 2.1, after the Imprivata sentence (line 282) | "These records document a costly preparation stage. Models of two-stage auctions, in which indicative bids precede costly diligence, describe the same structure (Ye 2007); Section 7 states how to test whether prices draw buyers into it." |

If the author does not want these citations, delete the five `\bibitem` blocks (lines 1485-1489, 1545-1551, 1552-1555, 1631-1635, 1636-1639). The reference list then has 41 entries.

### S8. Line 480: a 51-word sentence in the model description
Replacement for the last sentence of Section 2.3 (`main.tex:482-487`):

> The sequence is as follows. The seller announces the sale rule. The investor learns the class and trades. Market makers set the price from flow. The challenger observes the price and its cost, and decides whether to prepare. Prepared bidders learn their values and submit truthful bids. Ownership and financial payoffs are realized.

### S9. Section 6.1, line 1248: a 47-word sentence
Replacement for `main.tex:1247-1256` up to "keep the full proceeds gain":

> At \(r_1\), price access raises expected proceeds by 0.257809 per share. The informed investor's expected gross profit at one trading unit per share of float is 0.140731. This profit is a transfer from liquidity traders. Relative to an economy without the informed investor, initial shareholders gain in total at every trade scale below 1.831923 trading units per share of float. Holders who do not trade keep the full proceeds gain.

Also delete line 1239-1240 "The comparison holds the sale rule and the incumbent distribution fixed." Line 1217 already says "Hold the incumbent at \(r_1\)".

### S10. Section 6.3 repeats the value classes of Section 5.2 (brief R20)
`main.tex:1149-1152` (5.2) points forward to "the value classes of Section 6.3". `main.tex:1343-1347` (6.3) then introduces them again.
Replacement in 5.2 (lines 1149-1153):

> Dispersed values within each class give a nondegenerate example. Let values be uniform with half-width \(\varepsilon_V=0.05\) around \(\ell\) and \(h\), let the prior be one half, and let the investor observe only the class. Section 6.3 uses the same classes. At the reserve \(p=0.5\) both classes lie above the reserve.

Replacement in 6.3 (lines 1343-1347):

> Use the value classes of Section 5.2: uniform values with half-width \(\varepsilon_V=0.05\) around \(\ell\) and \(h\), prior one half. Because the supports have no atom, exclusion does not depend on an acquisition-value atom.

### S11. Introduction: the same content three times, and the setting comes late
- Lines 179-184 (investor paragraph), 463-470 (Section 2.3), and 1383-1385 (Section 7) each state that the investor's view comes from research on the challenger's fit and not from news about whether a bid arrives.
- Line 211 starts with "Rival strength moves the information sensitivity of the traded claim and the entrant's return in opposite directions, so competition can raise participation." This repeats the first two paragraphs.
- Lines 184-187 give a technical sentence ("Laplace noise is the extreme member ... Proposition A.5") in the paragraph about the investor. A finance reader does not need it before Section 2.

Fixes:
1. Delete line 211's first sentence. Start the paragraph "The paper belongs to the literature on the real effects of financial markets (Bond et al. 2012)."
2. Replace lines 184-187 by one sentence: "The model uses a bounded-score noise law, and Section 2.3 explains why." (Or delete; Section 2.3 and A.5 carry the point.)
3. Keep the "research, not news" statement in Section 2.3 only. Shorten lines 180-182 to: "Its information is the challenger's quality class." and delete "It forms that view from research on the target side of the match, not from news on whether a bid arrives."
4. Move the paragraph that starts "The setting is a listed target" (line 191) before the mechanism paragraph (line 160). A reader needs the setting before the mechanism.
Savings: about 0.4 page.

### S12. Online Appendix A.11 refers to a construction the reader cannot see (brief R23)
`online_appendix.tex:1577-1592`. The text says "In the reserve example that the earlier construction used, gross profit at a candidate pooled posterior \(\bar\mu\) was \(3\bar\mu>0\)." and "That construction has no counterpart under the declared cost law."
Replacement for the first paragraph:

> Under a positive low preparation cost, flows with gross profit below that cost could share a no-entry price. The pooled posterior over that preimage could then support more than one price mapping at one order profile. The declared cost law removes this case. Gross profit is nonnegative at every belief on the reserve domain, and the zero-cost realization prepares by the tie rule even where gross profit is zero. Entry is therefore at least \(\rho\) at every price. A zero-cost buyer who sees a pooled price prepares, so no price prescribes nonpreparation for every cost.

### S13. Defensive or negative framing in new passages (anti-defensive pass)
Each item keeps the content and states it as a fact.

| Line | Current | Replacement |
|---|---|---|
| 356 | "There is one challenger with one realized cost, not a low-cost buyer and a high-cost buyer at the same time; \(\rho\) is the probability that the realized cost is zero." | "There is one challenger. Its cost is zero with probability \(\rho\) and \(c_H\) otherwise." |
| 437 | "The class claim is therefore about tail weight and bounded inference, not about a fit of one law to noise demand." | Replaced in S3. |
| 1130 | "The reversal needs no point masses, no large class gap, and no special prior." | "The reversal holds without point masses, with a small class gap, and at any prior." |
| 1269 | "The dividend is a diagnostic on the financial claim: no bidder pays it, the seller cannot choose it, and acquisition surplus excludes it." | "The dividend is a diagnostic on the financial claim. Acquisition surplus excludes it." |
| 1318 | "The trading and preparation game under bargaining is not solved here." | "The trading and preparation game under bargaining is open." (This uses the paper's own status word.) |
| 215-216 | "The model abstracts from toeholds and dispersed-shareholder free riding (...) and takes the investor's information as given; endogenous research would add manipulation through the real decision that responds to the price (...)." | "The model fixes toeholds and dispersed-shareholder free riding out of the sale (Bulow et al. 1999; Grossman and Hart 1980) and takes the investor's information as given. Endogenous research would add manipulation through the real decision that responds to the price (Goldstein and Guembel 2008)." Move the second sentence to the Conclusion if the introduction needs to be shorter; it already appears there (line 1406). |
| 2632 (A.4) | "Laplace and logistic noise are compared at a common scale parameter \(b\), not at a common variance." | "Laplace and logistic noise are compared at a common scale parameter \(b\)." (The caption of Figure 3 already says the same.) |
| 2741 (A.4) | "This is a mathematical nonemptiness construction, not a statement about effect size for every pair of classes." | Delete. The sentence before it ends the argument. |
| 696 (OA A.5) | "...and I do not claim that version." | "...and that version needs a further condition." (Only if that is the intended meaning. Otherwise delete.) |

### S14. Long sentences (over 30 words) in new text, with replacements
| Line | Words | Replacement |
|---|---:|---|
| 216-220 | 35 | "Noise then lets an acquirer conceal share purchases before a bid (Kyle and Vila 1991). Large holders trade, monitor, or intervene as prices feed back to firm decisions (Edmans 2009; Maug 1998; Back et al. 2018; Edmans et al. 2015, Section II.E)." |
| 213 | 33 | "Recent work studies bidder learning about own values and competitors (Pernoud and Gleyze 2026). It also studies post-auction feedback in security-payment design (Liu and Bernhardt 2022) and bidder-pool choice with correlated values (Carlin et al. 2026)." |
| 311-314 | 34 | "Two restrictions rank the classes. The high class dominates the low class in first-order stochastic dominance above the reserve. The two classes are equally likely to fall below the reserve; I call this equal admissibility." |
| 1363-1366 | 35 | "Wherever the target-payoff spread is positive, fixed orders therefore fix what the price reveals. Distinct order-flow posteriors give distinct prices. Only flows with one common posterior, such as a posterior plateau, share a price." |
| 1113-1116 | 33 | "The other component lies above gross profit at the weak prior. It lies below gross profit at the highest strong belief. Its preparation therefore occurs only after sufficiently favorable prices in the strong economy." |
| 891-894 | 33 | "When both classes lie above the reserve, as in the benchmark, every prepared challenger is an admissible bidder. The auction then has two admissible bidders whenever the incumbent's value also meets the reserve." |

Sentences in the three long propositions (lines 596, 787, 808, 864) are statements and are not counted.

## Part 3. Prose, "minor"

M1. Journal name in the records: "The American Economic Review" (Bulow and Klemperer 1996, line 1455; Levin and Smith 1994, line 1564) but "American Economic Review" (Edmans et al. 2015, line 1496; Roberts and Sweeting 2013, line 1615; OA line 3907). Use one form. The journal's own style is "American Economic Review"; change the first two.

M2. Book records: Kotz et al. (line 1545) has "Boston, MA: Birkhäuser"; Krishna (line 1552) has "2nd ed. Academic Press." with no place. Write "Amsterdam: Academic Press" for Krishna, or drop the place for Kotz.

M3. Working-paper records: Liu and Bernhardt (line 1575) and Pernoud and Gleyze (line 1605) give a title and a URL only. Add "Working paper." after the title, as Carlin et al. and Lin et al. do.

M4. The condition tags and the labels differ: the labels `eq:paper-a2` and `eq:paper-a3` show (A1) and (A2); `eq:paper-a-50` to `eq:paper-a-57` show (A.45) to (A.52). This is safe now, but a later editor will confuse them. Rename the labels (`eq:paper-A1`, `eq:paper-A2`) in a later pass.

M5. Lines 188-190: three blank lines in a row after the introduction's investor paragraph. Delete two. No effect on the PDF.

M6. Several new passages put one sentence per source line and use `\par` inside a paragraph (lines 1054-1085, 2397-2650). The result is correct. If the author edits in Overleaf, the long runs of short lines are hard to diff. Optional.

M7. Line 465: "Documented informed trade before bids concerns in the main whether a bid arrives". Replacement: "Documented informed trade before bids mostly concerns whether a bid arrives".

M8. Line 1401, Conclusion: "At fixed orders the price experiment is already tied to those orders wherever the target-payoff spread is positive." This repeats lines 1363-1366. Delete it; keep "The reserve comparisons show why this choice matters."

M9. Section 2.2, line 308: "The incumbent is a bidder, rather than the target's management, and knows its value before bidding." Replacement: "The incumbent is a bidder and knows its value before bidding." (Section 2.2 also names "the target's management" nowhere else.)

M10. Class names: the introduction says "high-value class"; Section 2.2 says "high class" without saying that it is the same; Section 4.2 says "high-value challenger ownership". After the first use in Section 2.2, write "the high class (the high-value class)" once. Use "high-class ownership" for the general model and "high-value ownership" only for the point-mass benchmark.

M11. Section 2.4 and A.4 use "class objects" and "class proceeds". Use "class-level" (for `t_j`, `g_j`) in one place. Optional.

M12. Section 4.2 (line 940): "At every belief and cost realization, the decline in gross acquisition profit can only remove a preparation incentive." Fine in meaning. Simpler: "At every belief and cost realization, a decline in gross acquisition profit can only remove a preparation incentive." No change needed beyond "the" to "a".

M13. Line 1269: "The online matched-price panel reports it beside the hidden and feedback rows." "Online" is ambiguous (web or Online Appendix). Replace: "The matched-price table in the Online Appendix reports it beside the hidden and feedback rows."

M14. OA scope note (`online_appendix.tex:189-277`): it patches the equal-prior formulas with five exceptions (items 1 to 5). A reader must hold the note while reading A.1 to A.7. It is accurate. A later pass should rewrite those formulas for general `π` and delete the note. For now, no change.

M15. OA Lemma OA.2 (line 1025) is a special case of Proposition 2 at every prior (brief R19). Delete it or add one sentence: "Lemma OA.2 is the case \(\pi=1/2\) of Proposition 2." Saves about 0.3 page.

M16. The generated table notes still say "five strict margins", "ζ_L", and `c_L` (brief U1). These contradict the text. The renderer must change. This is the only visible inconsistency between the tables and the prose that I found; I did not re-check the other items of U1 to U4.

## Part 4. Length (main paper 73 to 90 pages)

Page position of the 90 pages in `main.pdf`: body (introduction to conclusion) pages 2-42, references pages 43-49, Appendix A pages 50-90.
The whole document, including the references and Appendix A, is set at double spacing (`\setstretch{2}`, line 142). Appendix A has about 280 words on a page with equations.

Measured on scratch copies (one compile each; repository files unchanged):

| Change | Pages | Saving |
|---|---:|---:|
| None | 90 | 0 |
| Single spacing for the references only | 87 | 3 |
| One-and-a-half spacing for references and Appendix A | 74 | 16 |
| Single spacing for references and Appendix A | 69 | 21 |

How to apply: insert `\begingroup\onehalfspacing` (or `\singlespacing`) before `\section{References}` (line 1411). The text of Section 2.3 and later does not change. The author may keep double spacing if a journal asks for it in the body only. Appendices are usually exempt.

Passages that can move to the Online Appendix without loss (page figures at the current spacing):

| # | Passage | Lines | Pages | Condition |
|---|---|---|---:|---|
| L1 | Appendix A.4 "More than two classes" | 2745-2820 | about 2 | Nothing in the main text refers to it (label `more-than-two-classes` has no `\ref`). Move to the OA after A.6, with one sentence in Section 5.2. |
| L2 | Appendix A.7 "Exact reserve events" | 3248-3295 | about 2 | OA C.6c already holds the event ledger. Keep the statement of the endpoint in A.7 and move the derivation. |
| L3 | Proof of Proposition A.5, nonemptiness part (the six-step construction) | 2520-2582 | about 1 | It repeats "Nonemptiness for every ranked pair of classes" (lines 2691-2744). Replace with: "Choose \(\tau\) in \((\pi,\bar\mu_f(\pi))\) at a continuity point, and repeat the steps of the nonemptiness argument above with \(B_{r_1}(\tau)=c_H\)." |
| L4 | Section 2.3, Laplace justification | 380-440 | about 0.8 | See S3. Move the "Three standard models" paragraph and the Gaussian contrast to Online Appendix A.6 or Section 5.1. |
| L5 | Section 5.1, repeated lines | 1052-1085 | about 0.5 | See S3. |
| L6 | Section 6.1, external-dividend paragraph | 1261-1273 | about 0.5 | The OA A.9 already holds the diagnostic. Keep two sentences: "An analytical invariance diagnostic separates the information effect from the price level. The Online Appendix reports it." |
| L7 | Section 6.3, last paragraph (zero cost, fixed orders) | 1363-1371 | about 0.4 | It restates Appendix A.7 and OA A.11. Keep the first two sentences. |
| L8 | Introduction, related-literature paragraphs | 211-225 | about 0.7 | Cut the first sentence of line 211 (S11) and the paragraph that starts "An informed trader can also hold a stake" to two sentences. The stake extension is in OA A.12. |
| L9 | Proof of Proposition A.5, Laplace-logistic Blackwell paragraph | 2628-2645 | about 0.5 | It repeats Section 5.1 and OA A.6. Keep one sentence and the pointer. |

Total of L1 to L9: about 9 pages at the present spacing, without any change of result. With the spacing change (S for refs and Appendix A at one and a half) the L1, L2, L3, and L9 savings shrink by about one third, so the combined saving is about 16 + 3 = 19 pages. The brief's target for the main text (73 pages) is reached with one-and-a-half spacing in the appendix plus L4 to L8.

The five items L1 to L3, L9 touch proofs. Move them as whole blocks and keep their labels. Rebuild with `latexmk` and check that no `\ref` is undefined.

## Top five

1. S1: rewrite the abstract (jargon, 35-word sentence, no class model).
2. S2: the independence sentence in Section 2.2 contradicts the class model.
3. S3: Section 2.3 and Section 5.1 repeat the Laplace argument; exact replacements given.
4. S4: "low-cost" against "low-value", and "buyer" against "challenger", name two things with one word.
5. Length: single or one-and-a-half spacing for the references and Appendix A saves 16 to 21 pages, measured.
