# Handout reconciliation: live page against the polished paper

Live page: `inputs/live_handout_2026-10-02.html` (the page served at the site root on 2 October 2026).
Paper: `overleaf/paper/main.tex` (line numbers below refer to this file). Registry:
`numerics/quantity_registry.csv`. Talk: `overleaf/talk/talk.tex` and `talk/structure-plan.md`.

This is a proposal list. No edit is applied. Each item quotes both texts and proposes a wording.
"Author decides" marks a choice the author must make; the mockups keep the live wording there.

## 0. Mechanical pass

- The live page carries 39 `span.q` placeholders over 34 registry keys. All 39 match the registry:
  displayed text equals the registry display string (or its percent form to one decimal), the
  `data-status` equals the registry status, and the tooltip starts with the registry display.
  Zero mismatches.
- No decimal number is typed in prose outside those spans, the generated tables and math.
- Placeholders inside `\( \)` and `\[ \]` resolve to bare values with no tooltip (for example
  `m=0.268941421`). The stale source confirms they were placeholders. This is a hook limitation of
  the math renderer, not a typed value. It is recorded in `migration-notes.md`.
- The 72-page and 57-page PDFs linked on the live page are the peer-release files. The Overleaf
  build of 30 September 2026 has the same `.tex` text and different PDF bytes (see
  `migration-notes.md`, section 1).

## 1. Masthead and opening question

| # | Live text | Paper text | Finding | Proposed wording |
|---|---|---|---|---|
| 1.1 | Status line: "Paper revised 6 September 2026"; colophon: "Theory working paper · Peer-circulation revision, 6 September 2026." | `overleaf/paper/build/main.pdf`: Info CreationDate 30 Sep 2026, 72 pages; `main.tex` identical to `paper/main_filled.tex` (sha256 06a035ed…). | The date names the text revision, not the PDF build. Both are true, but a reader cannot tell which. | "Manuscript text: peer-circulation revision of 6 September 2026. PDF built from the Overleaf working copy on 30 September 2026 (72 and 57 pages)." Show both dates in the Read-the-paper tab. |
| 1.2 | Byline: "Austin Li · UCL School of Management" | `main.tex` line 123: `\author{Austin Li}` (no affiliation). `talk.tex` line 114: `\institute{Department of Economics\\University College London}`. | The handout and the talk name different affiliations. The paper names none. | Author decides. Use one affiliation on all three surfaces. |
| 1.3 | "It also makes what target shareholders receive depend more on the challenger's value, so investors who know that value trade on it." | Abstract, lines 132–135: "Stronger competition lowers the buyer's acquisition profit at every fixed belief but increases the sensitivity of target shareholders' proceeds to its value. This raises the incentive to trade on information about the challenger." | "trade on it" is unconditional. In the weak economy nobody trades (Proposition 2 (i), line 711–713). | "…, so an investor who knows that value has more reason to trade on it." |
| 1.4 | "A stronger competitor can then bring in a buyer that would otherwise stay out: competition creates competition." | Abstract, lines 135–138: "On an open set of primitives, strengthening the incumbent changes uninformative prices into informative prices, with unique trading and on-path preparation outcomes in each economy." | "can" keeps the claim conditional. The stale source carried "Under the paper's conditions"; the live page dropped it. | Keep the sentence. Add the condition once: "Under the conditions of Proposition 2, a stronger competitor can then bring in a buyer that would otherwise stay out." |

## 2. Setting ("Inside a takeover process")

| # | Live text | Paper text | Finding | Proposed wording |
|---|---|---|---|---|
| 2.1 | Scenario box: "A listed software company announces a strategic review. One buyer is ready to bid. A second sees a possible fit but must investigate the technology, assess contracts and arrange financing." | Section 1.1, lines 314–317: "A disclosed approach, an announced strategic review, or an open contest can create such an interval." Lines 328–331 list verification, financing and approvals. | The scenario is not in the paper. The live page labels it "An illustrative sale process". Consistent with 1.1. | Keep. Keep the label. |
| 2.2 | "Values, cost and noise demand are independent; agents are risk neutral and standalone target value is zero." | Lines 416–418: "Incumbent value, challenger value, preparation cost, and noise demand are mutually independent"; line 373: "The target's known standalone value is normalized to zero." | Consistent. | No change. |
| 2.3 | "A higher \(r\) shifts incumbent values upward; it is not a higher announced bid." | Lines 391–392 and 350: "An increase in \(r\) strengthens the incumbent in the sense of first-order stochastic dominance." "Public incumbent strength is a distribution, not a bid." | Consistent. | No change. |
| 2.4 | Imprivata paragraph: "The record documents the stage; whether a stock price drew any buyer into it is the question for empirical work." | Lines 363–366: "This supports the existence of a costly preparation stage. It is not evidence that a price drew any buyer into that process, which is the question an empirical study would have to answer." | Consistent. | No change. |
| 2.5 | Model-to-record table, row "Entry \(\mathsf E\)": "Not the count of public offers, a narrower outcome." | Section 7, lines 1231–1234: "An empirical counterpart is the start of substantive diligence or the submission of a proposal requiring costly preparation, rather than the number of public offers." | Consistent. | No change. |

## 3. Mechanism ("Two returns to information")

| # | Live text | Paper text | Finding | Proposed wording |
|---|---|---|---|---|
| 3.1 | Mechanism map, information path: "Target payments depend more on challenger value. Information becomes more valuable to the investor. Informed trading becomes worthwhile." | Lines 172–181: "Target shares become more sensitive to information about the challenger … A larger gap in target proceeds can make that advantage worth the cost of trading." | "becomes worthwhile" is unconditional in the map; the paper says "can make". The caption below the map restores the condition. | "Informed trading can become worthwhile." |
| 3.2 | "prepare iff \(B_r(\mu(P))\ge C\)" | Line 425: "a challenger indifferent about preparation enters." | Consistent. | No change. |
| 3.3 | Equilibrium notion (fold): "uniqueness claims below refer to trading and on-path entry under truthful bidding and allow arbitrary mixed orders and every continuous deviation." | Lines 722–724: same words. | Consistent with the paper. The talk uses "every unilateral deviation \(q\in[-1,1]\)" (audit item F37). | Author decides between the paper's phrase and the talk's phrase, then use one everywhere. |
| 3.4 | Figure 1 caption: "The three profit curves hold beliefs fixed at the lower bound, the prior and the upper bound. Values are per target share." | Figure 1 notes, lines 574–578: "panel (b) plots gross challenger profit \(B_r(\mu)\) at the posterior bounds \(m,M\) and the prior \(1/2\). … Values are per target share. These are acquisition-stage payoffs, before solving trading and entry." | Consistent. The last sentence of the paper's note is missing on the web. | Add: "These are acquisition-stage payoffs, before trading and entry are solved." |
| 3.5 | Row label everywhere on the web: "target-payoff spread". | `tables/table1_auction_primitives.tex` row: "Information spread, \(\Delta_T=t_H-t_L\)"; `main.tex` text, line 492: "The target-payoff spread is \(\Delta_T=t_H-t_L\)"; Proposition A.8: "the target's information spread". | The web follows the paper's text. The paper's Table 1 and Proposition A.8 still say "information spread" (audit item F36). | Paper-internal. Author decides; the web should follow the paper's final choice. |
| 3.6 | Notation: \(\theta\in\{\ell,h\}\), \(\mu=\Pr(\theta=h)\). | Lines 396 and 493: same. | Consistent with the paper. The talk writes \(\theta\in\{H,L\}\) worth \(h\) or \(\ell\) (audit item F01). | Author decides. |
| 3.7 | Explorer intro: "The plotted preparation probability assumes full investor orders; away from validated benchmarks, it need not describe an equilibrium." | Line 755–773 (the full-order candidate, eq. 12). | Consistent with the display rule "fixed-order calculation, not an equilibrium solver". | No change. |

## 4. Evidence ("What the paper establishes")

| # | Live text | Paper text | Finding | Proposed wording |
|---|---|---|---|---|
| 4.1 | Lead: "Proposition 2 gives conditions under which this reversal is the unique outcome." | Lines 684–687: "changes the unique trading and on-path preparation outcome". Line 722: "Uniqueness refers to trading and on-path entry under truthful bidding". | "the unique outcome" is wider than the theorem. | "…under which this reversal is the unique trading and on-path preparation outcome." |
| 4.2 | Stat strip and lead: "25.0%", "52.3%", "32.4%". | Lines 798–800: "0.250000 to 0.522757 … 0.125000 to 0.324192". Talk: 0.250, 0.523, 0.324. | Display convention only. Percent form reads like an empirical rate. The three surfaces show three formats. | Author decides. Proposal: show 0.250 → 0.523 as on the slides, with the percent as a secondary gloss. |
| 4.3 | "All probabilities on this page are model probabilities, not empirical estimates." (inside the closed fold `#result-detail`) | No single sentence; the paper's Section 7 says no estimate exists (lines 1248–1249). | The hedge is hidden by default while the stat strip is visible. | Move the sentence under the stat strip, always visible. |
| 4.4 | Proposition 2 box: "These comparisons hold on a nonempty open set of primitives, allowing arbitrary mixed orders and every continuous deviation. Off-path pricing rules need not be unique." | Lines 721–724: "These comparisons hold on a nonempty open set of primitives. Uniqueness refers to trading and on-path entry under truthful bidding and allows arbitrary mixed orders and every continuous deviation." | "Off-path pricing rules need not be unique." has no counterpart in `main.tex` or `online_appendix.tex` (search for "off-path": none). | Replace with the paper's sentence: "Uniqueness refers to trading and on-path entry under truthful bidding and allows arbitrary mixed orders and every continuous deviation." Or cite the passage that supports the off-path sentence. |
| 4.5 | Core table caption: "Holding orders fixed isolates the information effect; these orders would not be chosen in equilibrium against the weak incumbent." | Lines 817–818: "Holding informative orders fixed restores deterrence: entry falls from 0.562178 to 0.522757 as the incumbent strengthens." Lines 822–823: "The frozen profile is a control and not an investor equilibrium in the weak economy". | The frozen row removes the change in information and leaves deterrence. The caption says the opposite. | "Holding orders fixed removes the change in information and leaves only deterrence; these orders would not be chosen in equilibrium against the weak incumbent." |
| 4.6 | Core table (`data-table="core_comparison"`): row "Same informative orders" shows 56.2% and 52.3% with no status. | Table 2 Panel B (`tables/table2_equilibrium_controls.tex`): Evidence "numerical diagnostic" for both frozen rows. Registry: `base_frozen_entry_weak`, `base_frozen_entry_strong` are "numerical diagnostic". | The row drops its evidence status. Display rule: accepted rows keep evidence status. | Add a status column: analytical / numerical diagnostic / analytical. Or put "numerical diagnostic" in the row label. |
| 4.7 | Table `equilibrium_controls`, Evidence column: "control" for both frozen rows. (Source: `handout/tables_html.py`, `status_word`, maps "fixed full-order profile" to "control".) | Table 2 Panel B prints "numerical diagnostic". Table 2 note: "control is an experiment role, not an evidence class." | The web prints a role word in the evidence column. "control" is not in the status vocabulary. | Print "numerical diagnostic" in the Evidence column. Put "(control)" in the row label: "Frozen informative orders (control), r = 1.2". |
| 4.8 | Table headers: "Very strong (r = 3.6)". | Table 2 Panel A: "Very strong incumbent (\(r=3.6\))". Talk: "stronger still \(r_2=3.6\)". | Consistent with the paper's tables. | No change. Note the talk's wording differs. |
| 4.9 | Figure 2 caption: "Diamonds mark the computer-assisted certificates. The open diamond identifies a mixed diagnostic, not a new interval proof." | Figure 2 notes, lines 882–887: "Black points carry the certified intervals of Proposition 3. … A hollow diamond marks a mixed candidate's preparation." | Marker words differ between the web figure and the paper figure. The web figure is its own drawing, so its legend may differ. | "Diamonds mark the certified intervals of Proposition 3 (computer-assisted)." Keep the mixed-diagnostic sentence. |
| 4.10 | "A still stronger incumbent can make even the best attainable price insufficient to justify high-cost preparation. Participation then returns to 25.0%. The theorem compares specified economies and does not trace a smooth hump; at intermediate strengths, equilibria can coexist." | Lines 784–789: "At a sufficiently strong incumbent satisfying part (iii), even the largest feasible belief fails to justify high-cost preparation. … it does not impose a monotone path between them." | Consistent. | No change. |
| 4.11 | Proposition 3 paragraph: "These certificates prove existence at the stated nodes; they do not establish an exhaustive correspondence." | Lines 924–926 and 940–941: "They do not prove a differentiable branch or a monotonicity result between the points." "The complete intermediate correspondence is open." | Consistent. | No change. |

## 5. Implications and robustness

| # | Live text | Paper text | Finding | Proposed wording |
|---|---|---|---|---|
| 5.1 | "The comparison ranks access to information under a fixed sale rule; it does not rank incumbent strengths or sale mechanisms." | Lines 1085–1087: "it does not rank different incumbent strengths or sale mechanisms." | Consistent. | No change. |
| 5.2 | "Proposition A.8 shows that a stronger incumbent weakly reduces challenger profit for every seller share \(\eta\). It raises the target-payoff spread when \(\eta<1/2\), leaves it unchanged at \(\eta=1/2\), and lowers it when \(\eta>1/2\)." | Proposition A.8: "It weakly increases the target's information spread for \(\eta<1/2\), leaves that spread unchanged at \(\eta=1/2\), and weakly decreases it for \(\eta>1/2\). Strictness follows from a positive integral change in the corresponding payoff function." | "raises" and "lowers" drop "weakly". The paper and the talk (audit item F49) say "weakly". | "It weakly raises the target-payoff spread when \(\eta<1/2\), leaves it unchanged at \(\eta=1/2\), and weakly lowers it when \(\eta>1/2\); the comparison is strict when the change in the incumbent distribution has positive integral." |
| 5.3 | Figure 4 caption: "At \(\eta=1\) profits are zero, so that endpoint is omitted only from the log panel; panel (a) retains it." | Eq. (14), line 1114: "\(0\le\eta<1\)". Proposition A.8: "For \(0\le\eta<1\)". Figure 4 notes, line 1154: "The log-scale panel uses the declared domain of seller weights below one." | Panel (a) plots \(\eta=1\), which lies outside the proposition's domain. `handout/README.md` records this as a display rule. | Add: "\(\eta=1\) lies outside the domain of Proposition A.8; panel (a) shows it for the payment identity only." Author decides whether to keep the point. |
| 5.4 | Matched dividend: tooltip status "numerical diagnostic"; text "The dividend is a diagnostic payment". | Line 1089–1090: "an analytical invariance diagnostic". Registry `base_matched_dividend`: "numerical diagnostic". | The paper's adjective and the registry's status differ (talk audit item F10). The web follows the registry. | Author decides. Keep the registry word on the web until the paper changes. |
| 5.5 | "In the private-information extension, the buyer's signal is more accurate than the investor's, yet the price adds useful information." | Lines 1042–1043: "The declared example has buyer accuracy 75% and investor accuracy 70%. Entry rises from 0.850000 to 0.879438." `tables/table_signal_grid.tex`: entry falls in the 10 cells with \(d\ge0.76\) (numerical diagnostic). | The sentence reads as general. The result is the declared example (talk audit item F16). | "In the declared example of the private-information extension, the buyer's signal is more accurate than the investor's, yet the price still adds useful information." |
| 5.6 | "The reversal also survives the paper's logistic-noise example, continuously distributed preparation costs and a narrower gap between acquisition values. The mechanism holds in each; its size changes." | Lines 227–229 and 948–1010. Talk takeaway (F13): "The \(r_0\to r_1\) reversal survives…" and A26: "the \(r_2\) fall is shown for the benchmark only." | The web does not say the fall at \(r_2\) is benchmark-only (talk audit item F47). | Add: "The rise from the weak to the strong incumbent survives each change; the later fall is shown for the benchmark only." |
| 5.7 | Access to prices paragraph with 0.872392, 0.614583, 0.080218. | Proposition A.9 and lines 1083–1087. | Consistent. The paper adds "The comparison also holds under Propositions A.5 and A.6." | Optional: add that sentence. |
| 5.8 | Reserve paragraph: "Raising the reserve from 0.5 to 1.1 increases revenue against both incumbents and supports informative trading in both economies." "This is a feasible improvement, not an optimal reserve." | Lines 1193–1199 and 1209–1211. | Consistent. | No change. |
| 5.9 | Takeaway: "The contribution is a link between the payment rule and the information that recruits bidders. The rule a seller picks sets what a challenger would pay and what the stock price can tell it before it decides to prepare." | Conclusion, lines 1258–1260: "Sale terms therefore affect participation through both the buyer's expected payment and the information supplied by the stock market." | Consistent with the paper. The talk keeps sale terms as the spoken open question and uses the strength-based implication on its main line (structure-plan C36). | Author decides whether the handout's closing line should match the talk's main-line implication. |
| 5.10 | Robustness numbers: 30.2%, 52.3%, 1.495369, 0.1, 25.0% → 52.7%, 85.0% → 87.9%. | Lines 956–958, 995–996, 1003–1004, 1042–1043. | All match the registry (section 0). | No change. |

## 6. Tables

| # | Table | Finding | Proposed change |
|---|---|---|---|
| 6.1 | `core_comparison` | No status column (item 4.6). | Add status. |
| 6.2 | `equilibrium_controls` | "control" in the Evidence column (item 4.7). | Print the registry status; move the role word to the label. |
| 6.3 | `comparative_statics` | Row "\(x^*\), threshold order flow" shows "∞" with tooltip "unattainable" at \(r=1.2\) and \(r=3.6\). `tables/equilibrium_controls.csv` stores "unattainable". | Consistent with the paper's convention (the bound is unattained). Keep the tooltip word visible on hover. |
| 6.4 | `extensions` (Table 3) | Panel labels and the "Minimum margin" column match `tables/table3_extensions.tex` and the registry margins. | No change. |
| 6.5 | `reserve_comparisons` (Table 4) | Panel A uses \(p=1.01\), Panel B \(p=1.1\); matches `table4_reserve_comparisons.tex`. | No change. |
| 6.6 | `certificates` | Full-precision entry enclosures are shown. | Keep outward endpoints. The slides show the registry's shortened display; both are allowed. |
| 6.7 | `welfare` (Panel C) | Matches Table 2 Panel C. | No change. |
| 6.8 | Table 1 on the web | Row label "target-payoff spread" (item 3.5). | Follow the paper's final choice. |

## 7. Figure captions

| Figure | Finding | Proposed change |
|---|---|---|
| 1 | Missing the paper's last note sentence (item 3.4). | Add it. |
| 2 | Marker vocabulary (item 4.9). Shading, broken lines, multiplicity ticks and the open diamond match the display rules. | Reword the diamond sentence. |
| 3 | Matches the paper's Figure 3 notes, including the closed point at zero threshold distance and "not a Blackwell ranking". | No change. |
| 4 | \(\eta=1\) endpoint (item 5.3). | Add the domain sentence. |

## 8. What the mockups change

One line. The masthead status line applies item 1.1 ("Text revised 6 September 2026 · PDF built
30 September 2026") to show the version stamp the Read-the-paper tab needs. Every other string
is the live text, including the byline (item 1.2, author decides) and the prose of the opening
and of the mechanism section. The evidence-section items (4.3, 4.6, 4.7) are outside the
mockup's scope; the slides mockup shows the convention they ask for (a visible status word beside
every number) on frames 2, 6, 8 and 10.
