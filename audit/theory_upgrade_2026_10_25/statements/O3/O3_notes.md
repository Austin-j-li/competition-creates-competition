# O3. The last strength with recruiting research at the cap

## Result and scope

Proved. At prior one half, with ranked classes, a continuous incumbent law, positive spread and profit gap, tau above one half, positive research and trading costs, a cap strictly between zero and one, and liquidity share strictly between zero and one half, the capped recruiting outcome exists exactly when

\[
\Delta_T m_{\bar\lambda}-k+(\rho\Delta_T m_{\bar\lambda}-k)^+\ge2a\bar\lambda,
\qquad \tau\le M_{\bar\lambda}.
\]

An indifferent investor may mix and an indifferent high-cost challenger prepares. Full preparation at the purchase is also available when an indifferent high-cost challenger may prepare with any probability. The claim concerns that full-preparation outcome.

On a compact path with continuous reduced coordinates, the capped set is empty, a singleton, or a closed interval. If nonempty, its right endpoint is the maximum of the set where tau is at most the cap posterior. Equality belongs to the outcome set. A plateau of equal threshold and cap posterior lasts through its right end. If the declared path ends before the threshold exceeds the cap posterior, the path endpoint is the last strength.

In the example the threshold rises strictly, and the capped recruiting interval is [r_lambda_bar, r_C], with endpoints approximately 1.677633 and 3.592659.

## Argument

At the cap, the joint-deviation objective is intensity times the average best trading payoff minus its quadratic research cost. Its derivative at the cap has the sign of the first displayed margin. That margin increases strictly in the spread, so it defines one cap spread. Solving its zero separately according to whether the sale profit is zero gives the two expressions in the fragment. The cap spread exceeds twice the trading cost.

The spread is nondecreasing on a path. The threshold is also nondecreasing, because its numerator c_H minus g_L is positive and nondecreasing while its positive denominator g_H minus g_L is nonincreasing. Hence research optimality at the cap defines an upper set and preparation after a purchase defines a lower set. Their closed intersection gives the interval and its endpoints. The sale rule, price pooling with equal entry, and truthful bidding supply the rest of the equilibrium.

For the example, the general auction formulas give a strictly positive spread derivative and a strictly negative low-class profit derivative. The threshold derivative is therefore positive. Existing posterior margins at r_1 and r_2 locate its unique equality with the cap posterior. The cap formula and the positive gap r_N minus r_lambda_bar put the left endpoint before that equality.

## Sources and placement

- Referee report W3, Shared Candidate 1, sections 3 to 6, especially equation (9) and the last-point instruction in section 6.
- Referee report W3, the example's boundary table.
- Manuscript locations: appendix/A5_research.tex:286–314 and sections/05_research.tex:119–144.
- Formal home: Proposition 4(d), label `prop:research`; the example is Corollary 3, label `cor:research`. This fragment introduces no numbered result.
- The overlap with statements/O1/ is part (c) of Lemma `lem:a5-floor`; its accepted proof is unchanged.

## Quantities and computations

No additional number definition is required by this fragment. It uses the existing cap and endpoint values and posterior margins. The print-only computation in statements/O4/ gives the cap endpoint both from the inverse spread formula and from its defining equation; their rational bounds agree. It gives r_C from the threshold equation, with bounds

\[
3.592658518794661833<r_C<3.592658518794661834.
\]

The retained statement includes the empty-set and singleton alternatives. The initial fragment's unconditional naming of two endpoints required nonempty defining sets; the final statement states that hypothesis. The planned last-point claim holds. A first-equality endpoint would be false on a plateau.

## Delivery

The fragment is ready for the Proposition 4 proof. Its local build and language results are listed in C_notes.md. The independent referee still reads this proof and the notation pass in statements/O1/.
