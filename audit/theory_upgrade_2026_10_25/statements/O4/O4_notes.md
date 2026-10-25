# O4. Cheap research on the exact margin

## Result and scope

Proved. The margin at the research intensity that just reaches the preparation threshold is

\[
\varphi_a^*=J-k+(\rho J-k)^+-2a\lambda_E(\tau),\qquad J=\Delta_T(1-\tau).
\]

For a continuously differentiable path before the first cap strength, the cheap-research condition is

\[
[1+\rho\mathbf1\{\rho J>k\}]J'-2a\lambda_E'(\tau)\tau'>0
\quad\text{almost everywhere}.
\]

The prior is one half; classes are ranked, incumbent laws are continuous, the spread and profit gap are positive, and all nonauction primitives are fixed. The threshold exceeds one half throughout the path and is below one before the cap. An indifferent investor may mix and an indifferent high-cost challenger prepares. Full preparation at a purchase also supplies this outcome when an indifferent high-cost challenger may prepare with any probability.

A continuous, strictly increasing exact margin, negative at the first strength and positive at the first cap strength, gives one recruiting interval. On a continuously differentiable path, the derivative condition suffices for strict increase. It begins at the unique zero of the exact margin and ends at the last point where the cap posterior reaches the threshold. The path is compact, its spread and threshold are continuous, and it attains the cap spread after its first strength.

## Argument

The research residual falls strictly with intensity. Its value at lambda_E is exactly phi_a_star. Thus recruitment requires a nonnegative exact margin and lambda_E at most the cap. A nonnegative margin also implies J greater than k, hence a spread greater than 2k, so the research root exists.

The positive part of a continuously differentiable function is absolutely continuous. Its derivative is rho times J_prime where rho J exceeds k; on the equality set J_prime is zero almost everywhere. This gives the displayed derivative almost everywhere, including paths with threshold-sale equalities. Integrating a derivative positive almost everywhere over every nondegenerate subinterval proves strict increase. The endpoint signs then give one root.

At the first cap strength, a positive exact margin implies that the threshold research is strictly below the cap. Threshold monotonicity makes the cap constraint feasible at every earlier strength. Below the cap, the margin alone therefore determines recruitment. From the cap onward, the spread keeps cap research optimal, and O3 gives the final point.

At a point with positive threshold derivative, the condition bounds a by the ratio of [1 + rho times the profitable-sale indicator] J_prime to twice lambda_E_prime times tau_prime. At a point with zero threshold derivative it requires J_prime positive. This form includes a recruiting start at which a sure sale is already profitable.

## The example and the cost variant

The example uses a = 1/40. Its exact margin equals the purchase-only margin on [r_0, r_lambda_bar], because that interval lies below r_N and tau exceeds one half. On [6/5, 7/4], the exact bounds are

- Delta_T_prime at least 11/72;
- 1 minus tau at least 19/55;
- Delta_T at most 9/56;
- tau_prime at most 16875/211288.

They give J_prime at least 21266929/532445760 and the purchase-only margin derivative at least 46061709624985094449/1364098973371103914560, which exceeds its displayed lower bound 0.033767. The cost bound is 54484791118735094449/336923259750000000000, approximately 0.161713. The endpoint margins are negative at r_0 and positive at r_lambda_bar. Lemma A.10(b) gives increasing J on the whole path. For r >= 7/4, phi_a(r) >= J(7/4) - k - 2a lambda_E(r_2) > 0, with J(7/4) = 171/3080; hence the zero is unique on the whole path. Their exact definitions are below.

The print-only computation also takes a = 1/5 with every other primitive fixed. It bounds the purchase-only margin derivative on 120 rational pieces of width 1/50 over [6/5,18/5]; its smallest lower bound is greater than 0.030751008. Consequently J and the exact margin rise. The exact-margin start lies in [2.203523115209391, 2.203523115209392], and the sale profit there lies in [0.006925573540, 0.006925573541]. The purchase-only margin instead vanishes in [2.279293267130884, 2.279293267130885]. Omitting the sale term would place the start too late. The cap is reached near 2.662212, before the same entry ceiling. This variant supplies evidence for the general formula; its numbers are absent from the manuscript-facing fragment.

The planned claim on the exact margin holds. A claim using the purchase-only margin as an exact recruitment condition fails when a sure sale pays. A derivative condition without endpoint signs would establish monotonicity, not the existence of a crossing.

## Sources and placement

Referee report W3, Shared Candidate 1, section 6, and Shared Candidate 2, equation (12); its cost-variant paragraph supplies a comparison. Manuscript locations: appendix/A5_research.tex:286–314 and sections/05_research.tex:119–125. The formal home is Proposition 4(d), label `prop:research`, with condition label `eq:a5-cheap` printed as (CR). No additional numbered result is introduced.

## Number definitions

| Name | Exact value | Display | Derivation |
|---|---|---|---|
| `res_J74_frac` | 171/3080 | 171/3080 | J(7/4), for the positive lower bound beyond 7/4 |
| `res_bound_strength` | 7/4 | 7/4 | right endpoint of the rational derivative bound |
| `res_phi_r0_frac` | -1369550353/60351152400 | -1369550353/60351152400 | J(6/5) - 1/50 - lambda_E(6/5)/20, with J = 113/18480 and lambda_E = 2416171/13716171 |
| `res_phi_rcap` | J(c) - 1/50 - lambda_E(c)/20, where c = frak_r((bar_lambda/20 + 1/50)(1 + e)) and bar_lambda = ((e-1)(58931/200000))/(1+(e-1)(58931/200000)) | 0.017446 | the exact endpoint margin; 0.01744574845681505714 < value < 0.01744574845681505715 |

Here frak_r(y) = 1 + y + sqrt(y squared + 2y), Delta_T(r) = (r-1) squared/(2r), tau(r) = (12r-3/4)/(20r-r squared-1), and lambda_E(tau) is the rational function in the proof. These define the irrational value exactly; the decimal interval supplies its rounding.

## Computation and delivery

`o4_margins.py` reads the example's exact primitives and the existing scalar table, computes rational bounds on every irrational quantity, and prints the results. It contains no assertions. Its rational quadratic root comes from clearing the denominator of the relevant research equation; its cap formula comes from the two signs of the sale term. Euler's number is between its sum through 40 and that sum plus 2/41!, and square roots use integer square roots with outward rational endpoints. Execution exits successfully. Every existing display it compares agrees. Its threshold pair at r = 2 also supplies the three exact fractions in C_notes.md.

The local build and language results are listed in C_notes.md. The independent referee still reads the derivative argument and the endpoint hypotheses.
