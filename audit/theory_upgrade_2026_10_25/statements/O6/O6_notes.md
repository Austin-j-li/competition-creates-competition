# O6. Class H's takeover share

Mathematics writer's result: under Proposition 2 and outbidding at the stronger incumbent, the takeover share rises strictly exactly when `W_L(F_0)>0`. If `W_L(F_0)=0`, the share equals one at both laws. This includes the case in which class L wins at the weaker law and never wins at the stronger one.

## Statement, scope and argument

Source: referee report W2, Shared Candidate 3 and the Proposition 2 discussion; `appendix/A3_proposition2.tex:75-86`. Scope: ranked finite-mean classes, a continuous ordered triple, any interior prior, rho and lambda, `0<beta<1/2`, and (H1)--(H3). Every equilibrium comparison is strict, so the result holds under all four tie rules. Trading is forced abstention at F_0 and full two-sided informed trade at F_1.

Conditional independence gives `Own_{j,1}=pi_j e_j W_j(F_1)` and `Own_{j,0}=pi_j rho W_j(F_0)`, where `e_H=rho+(1-rho)(b+lambda)` and `e_L=rho+(1-rho)b`. Both economies have positive challenger acquisition probability: positive high-class gross profit at F_1 supplies a positive winning probability, and FOSD preserves it at F_0.

Cross multiplication of the two shares gives the exact condition, including zero low-class winning probabilities:

`e_H W_H(F_1) W_L(F_0) > e_L W_H(F_0) W_L(F_1)`.

Under `W_H(F_1)=1`, FOSD gives `W_H(F_0)=1`. Since `e_H>e_L>0` and `W_L(F_1)<=W_L(F_0)`, the condition holds whenever `W_L(F_0)>0`. If that probability is zero, FOSD makes both low-class ownership probabilities zero and both shares one. High-class ownership rises strictly from `pi rho` to `pi e_H` in either case.

The statement remains part (ii) of Proposition 2, label `prop:ccc`, number 2. The exact share condition has label `eq:a3-share`. The full statement stands in `A.tex`; `O6_proof.tex` supplies the statement and complete ownership/share argument for `appendix/A3_proposition2.tex:75-86`.

## Source comparison

The plan's condition using the weaker endpoint is exact. A condition using `W_L(F_1)>0`, as in the main-text lens, is sufficient. W2's wording about a positive low-class probability at the stronger endpoint requires separate treatment of saturation; the cross-product condition and the weaker-endpoint formulation supply that treatment. Outbidding F_1 implies outbidding F_0, so one outbidding hypothesis suffices.

The share is conditional on an acquisition won by the challenger. Completed sales won by the incumbent are outside its denominator. The same-incumbent comparison with zero research belongs to the research result; Proposition 2's strong-economy trading window makes abstention strictly inferior.

## Exact values for the example

With `beta=294655/1000000`, `u=e-1`, `lambda=u beta/(1+u beta)` and `b=beta/(1+u beta)`, class H wins with probability one at all three strengths. The low-class winning probabilities are `5/6`, `1/3` and `5/18`.

| Numerical-table name | Exact value | Six-place display | Derivation |
|---|---|---|---|
| `share_H_r0` | `6/11` | `0.545455` | `pi/[pi+(1-pi) ell/r_0]`. |
| `share_H_r1_B` | `[3+(12e-3) beta]/[4+(13e-1) beta]` | `0.830691` | `pi e_H/[pi e_H+(1-pi)e_L ell/r_1]`. |
| `share_H_r2_B` | `18/23` | `0.782609` | The first formula at r_2. |

The names follow the delivery lens. The wording targets' `own_share_r0` and `own_share_r1_B` refer to the same quantities and take the names in this table.

The print-only computation `python3 -I o6_shares.py` prints the class entry, ownership and share calculations, the cross-product difference, the cost window, and exact coordinates of Corollary 1. Its interval calculation uses 60 decimal digits for Euler's number; rational quantities use exact fractions. The direct and closed-form share values are both `0.830690945230374`; their interval difference contains zero with width below `2e-60`. The cross-product difference is positive, `0.408431745639569`. At r_1, total entry is `0.522756943478407` and high-class ownership is `0.324401303410789`.
