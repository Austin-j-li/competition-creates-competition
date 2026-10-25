# Area D referee report

## Decision

The formal results follow from the referee reports with one wording overclaim in Corollary A.3(b). The whole-segment observational-equivalence claim in A.3(b) is correct and is accepted. The statement's subsequent claim that counts and prices identify \(s_+\) needs the known-prior qualifier. The main-text forms of the opening, Proposition A.11/Corollary A.3, and Proposition A.12 also need the fixes below.

No Part 5 proof is assigned to area D.

## Verdicts

| Statement | Verdict | Reason and fix |
|---|---|---|
| Standing paragraph | accept | The fixed-public-state scope, order law, balance identity, informed share, posterior-gap inequality, and entry at the floor when \(\pi<\tau\) match the referee proof. |
| Proposition A.10, price gap and weighted test | accept | Parts (i)–(vi) carry full two-sided trade where required, \(\pi<\tau\) for the weighted test, both challenger tie rules and all three threshold ties, the hidden economy's own full-order condition, the preparing rule for the unweighted comparison, fixed prior and slot, the reserve conditions, and the continuity and actual-crossing conditions at the ceiling. |
| Proposition A.11, counts and prices | accept | The known-prior inversion, sampling variance, prior-\(1/2\) feasibility and incentive bounds, weak/strict investor-tie distinction, and floor-entry sale-price inversion match the referee proof. |
| Corollary A.3(a) | accept | The purchases-only frequencies and the distinction between the realized informed share and the presence probability are correct. Identification of \(s_+\) is correctly restricted to a known prior. |
| Corollary A.3(b) | overclaim | Accept the equilibrium construction on the entire segment, proved below. At lines 228–231, identification of \(s_+\) is stated without the known-prior qualifier used in part (a) and in the referee proof. Write: “The counts therefore identify \(b\) and, at a known prior, \(s_+\); even with the prices, they do not identify \(\lambda\).” |
| Proposition A.12, orders predict the winner | accept | The general sign and strictness condition, arbitrary-prior covariance, prior-\(1/2\) second difference, fixed-slot outbidding trend, and exact uniform-family condition match the referee proofs. Weak and strict trends are distinguished correctly. |
| Proposition A.13, announcement returns | accept | The report-contingent price changes, zero conditional mean, exact uncertainty condition, sufficient prior-profit condition, and identity with the weighted impact difference match the referee proof at every prior. |
| The example | accept | The parts follow the general statements and the referee calculations. The stated domains, endpoints, tie rules, hidden-price comparisons, and recruitment/exclusion bands are carried. |
| Main-text opening | overclaim | At lines 415–418, “Each prediction holds … at every prior” conflicts with results that require the prior \(1/2\), a prior at least \(1/2\), or a prior below the threshold. State that each prediction names its incumbent, prior, trading-pattern, and tie-rule conditions. |
| Main-text Proposition A.10 | accept | Full two-sided trade and the prior-profit condition govern the price-gap discussion; the hidden-price sentence also requires full trade in that economy, which it states. The unweighted test names its prior, zero-cost probability, and challenger tie rule. The trend names fixed prior and slot and the reserve conditions. |
| Main-text Proposition A.11 and Corollary A.3 | overclaim | At line 455, “Prices separate the slots that counts leave together” is categorical, whereas the next sentence gives the entry-floor and known-scale conditions and purchases-only equilibria retain nonidentification even with prices. Write “In the example, prices separate slots with the same counts,” or state the full sale-price conditions in that sentence. |
| Main-text Proposition A.12 | missing qualifier | At lines 468–469, “When no order recruits” does not imply entry \(\rho\): entry can be one after every order. The covariance formula requires \(B_F(M)<c_H\), equivalently floor entry after every order under full two-sided trade. Write: “When gross profit at the top posterior falls short of \(c_H\), entry is \(\rho\) after every order …”. |
| Main-text Proposition A.13 | accept | The exact uncertainty condition, arbitrary-prior scope, prior-profit sufficient condition, and no-order discount match A.13 and A.10. |

Decision 7 and Part 6 are respected: the four propositions print as A.10–A.13, Corollary A.3 keeps its number, and the example is unnumbered. No additional numbered result is introduced.

## Corollary A.3(b): the whole segment

Fix \(b\), \(s_+\), and \(\pi\). For any \(\lambda'\in[s_+,1-3b]\), set
\[
\beta'=\frac{b}{1-\lambda'},\qquad \sigma'_H(1)=\frac{s_+}{\lambda'},
\]
with class \(L\) abstaining. The bounds give \(0<\sigma'_H(1)\le1\) and \(0<\beta'\le1/3\). The class-conditional order laws, in the order \((-1,0,1)\), are
\[
f'_H=(b,1-2b-s_+,b+s_+)=f_H,\qquad f'_L=(b,1-2b,b)=f_L.
\]
They do not depend on \(\lambda'\). Every posterior therefore stays unchanged. Since preparation depends on the posterior and price, and the competitive price depends on the posterior and preparation, entry and prices stay unchanged. Every deviation payoff for either class also stays unchanged, so the original best-response comparisons remain valid. The mixing rule permits the interior mixtures and both endpoints: \(\sigma'_H(1)=1\) at \(\lambda'=s_+\), and \(\beta'=1/3\) at \(\lambda'=1-3b\). Acquisition probabilities conditional on each order are likewise unchanged because entry and the class posterior are unchanged.

This proves observational equivalence on the entire stated segment. Identification of \(s_+=\E[X]/\pi\) retains its known-prior qualifier.

## Issues

1. **blocker: lines 228–231, Corollary A.3(b).** Identification of \(s_+\) lacks the known-prior qualifier. **Fix:** “The counts therefore identify \(b\) and, at a known prior, \(s_+\); even with the prices, they do not identify \(\lambda\).”
2. **should fix: lines 415–418, main-text opening.** “Each prediction holds … at every prior” overstates the prior-specific results. **Fix:** say that each prediction names its incumbent, prior, trading-pattern, and tie-rule conditions.
3. **minor: line 455, main-text informed-share paragraph.** “Prices separate the slots that counts leave together” omits the conditions supplied only by the following sentence and is false for the purchases-only construction. **Fix:** restrict the sentence to the example, or state the sale-price conditions there.
4. **should fix: lines 468–469, main-text winner paragraph.** “When no order recruits” does not imply the floor-entry covariance formula when entry is one after every order. **Fix:** assume \(B_F(M)<c_H\) and state entry \(\rho\) after every order before giving the formula.

## Calculations

A print-only calculation at 70-digit precision used \(\beta=294655/10^6\), \(u=\mathrm e-1\), \(\rho=1/4\), \(M=\mathrm e/(1+\mathrm e)\), \(w_3(M)=11/24+2M/3\), and \(W_{F_3}(M)=1/3+2M/3\). It reproduced the seven values in the notes:

- weighted impact difference at \(r_1\): 0.2579478013681287647781157082705427097540947971381523471;
- uniform reserve margin: \(1/4\);
- winner-trend margins at \(r_1\) and \(r_2\): \(1/3\) and \(5/18\);
- class component of the winner covariance at \(r_1\): 0.02801014740959343311643196249195429161444628629450020817;
- recruitment component of the winner covariance at \(r_1\): 0.2238531834333279308144102717653935614910802653966151837;
- winner second difference at \(r_1\): 0.6155292893150024396255796209109181371825723200825282596.

The two covariance components sum to 0.2518633308429213639308422342573478531055265516911153919, the stated winner covariance. The weighted impact difference agrees with the negative of the stated no-order price change to its printed precision.

For the referee's purchases-only illustration, the whole segment is approximately \([0.046575009567,0.41315487945905510926]\). At the original slot, the referee's alternative, and both endpoints, the calculation gave identical class-conditional order laws. The endpoints gave \(\sigma'_H(1)=1\) and \(\beta'=1/3\), respectively, as the proof requires.

## Build and language

The statements built into the private build folder as a nine-page document. All pages were read. The second pass has no undefined references or overfull boxes. The seven numerical placeholders listed in the notes print as expected, and their exact values appear above.

The language review reports one interval-expression hit at line 281. It states an exact almost-everywhere condition for monotonicity on a mathematical interval, not an unsupported path claim, and is acceptable. The remaining hits are the permitted tie-rule phrases. No status label, defensive passage, development narration, process term, or non-neutral example name appears in the statements.
