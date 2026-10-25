# O6. Class H's takeover share in Proposition 2

Report of the mathematics writer to the coordinator, 25 October 2026. This folder holds the LaTeX fragment `O6_proof.tex` (the sentence that part (ii) of Proposition 2 gains, and Step 4 of the proof of Proposition 2 that proves it), the print-only program `o6_shares.py` for the example's values, and this report. Nothing is committed.

## 1. Result

Setting: the hypotheses of Proposition 2. The classes satisfy the class ranking; F_1 is a continuous first-order stochastic strengthening of the continuous F_0; 0 < pi < 1, 0 < rho < 1, k > 0, any slot; (H1) to (H3). Each economy has a unique outcome under all four tie rules (every comparison is strict), so the takeover share is a property of the economy, and no tie phrase is needed.

Definitions (Section 2.4, as in the prose writer's target T-2.6): W_j(F) = E_j[F(theta) 1{theta >= p}]; class H outbids F when W_H(F) = 1; class H's takeover share is the probability that the challenger is of class H, given that the challenger acquires the target, that is Own_H/(Own_H + Own_L) with Own_j = pi_j e_j W_j(F).

1. **General exact condition.** The share rises from F_0 to F_1 exactly when
   e_H W_H(F_1) W_L(F_0) > e_L W_H(F_0) W_L(F_1),
   with e_H = rho + (1 - rho)(b + lambda) and e_L = rho + (1 - rho) b, the class entry at F_1 (entry at F_0 is rho in both classes). This is equation `eq:a3-share` of the fragment; it is the referee's odds condition of W2 "Shared Candidate 3", (e_H/e_L)_1 / (e_H/e_L)_0 > (W_L/W_H)_1 / (W_L/W_H)_0, written without division, so that it also covers W_L = 0.
2. **Under outbidding (the statement).** If W_H(F_1) = 1, then class H outbids F_0 as well, high-class ownership rises strictly from pi rho to pi e_H, and the share rises strictly if W_L(F_0) > 0 and equals one against both incumbents if W_L(F_0) = 0.

The plan's claim (PLAN.md Part 5, O6: "the weak type must win with positive probability against the weaker incumbent") holds exactly, read as W_L(F_0) > 0 under outbidding.

## 2. The argument in words

- Class entry at F_1 comes from Step 4 of the existing proof: only a purchase recruits, class H places it with probability b + lambda and class L with probability b. Entry is independent of (theta, R) given the class, so the probability that a class-j challenger acquires the target factors as pi_j e_j W_j(F).
- Both economies have takeovers by a challenger with positive probability: (H1) gives B_1(M) > c_H > 0, so some class has positive gross profit against F_1 and hence a positive chance to win; first-order dominance gives F_1 <= F_0 pointwise, so each W_j can only be larger against F_0. The two shares are therefore defined.
- For nonnegative x, y, x', y' with positive sums, x/(x + y) > x'/(x' + y') is the same as x y' > x' y. Applied to the class ownership probabilities and divided by pi(1 - pi) rho, this gives the general condition.
- Under outbidding: W_H(F_0) is between W_H(F_1) = 1 and 1, so class H outbids F_0; the condition reduces to e_H W_L(F_0) > e_L W_L(F_1). Since e_H > e_L (because lambda > 0 and rho < 1) and W_L(F_1) <= W_L(F_0), the condition holds whenever W_L(F_0) > 0. If W_L(F_0) = 0, then W_L(F_1) = 0, class L never acquires the target in either economy, and the share is one in both.

## 3. Where the sources differ, and what it changes

- `plan/lens_maintext.md` T-P2 had "strictly when W_L(F_1) > 0". That condition is sufficient, not necessary: when W_L(F_1) = 0 < W_L(F_0), the share rises strictly, from pi/[pi + (1 - pi) W_L(F_0)] < 1 to one. For instance, with point-mass classes h = 10 and ell = 1, a weak incumbent uniform on [0, 2] and a strong incumbent uniform on [3/2, 7/2] (a first-order strengthening: the second distribution function is zero below 3/2 and at most the first above it), W_H = 1 against both, and W_L falls from 1/2 to 0. The prose writer's point 2 for the referee (`wording_targets.md`) reaches the same reading.
- W2 "Shared Candidate 3" writes that strict growth "requires a positive low-class winning probability at the relevant stronger endpoint, or separate treatment of saturation". Read as W_L(F_1) > 0, this is the same sufficient condition; the exact condition under outbidding is W_L(F_0) > 0, and the fragment treats saturation (W_L(F_0) = 0) in the statement itself.
- `plan/lens_theory.md` T10 assumed outbidding of both incumbents. Outbidding F_1 implies outbidding F_0 (W2, "Do the same workarounds cover Proposition 2"), so the statement assumes W_H(F_1) = 1 only.
- Without outbidding the share can fall. W2 "Benchmark verification" gives an incumbent mixture at which W_H drops from 1 to 0.996 and class H's share of challenger acquisitions falls from 0.699521 to 0.698707 (in the research equilibrium, a different comparison), and W2 "The hazard-order conjecture fails" shows that the class ranking alone does not order W_H(F_1)/W_H(F_0) against W_L(F_1)/W_L(F_0). The general condition in Step 4 is the exact statement for that case; the main text states only the outbidding case.
- Effect on the plan: none beyond the wording. The share sentence goes in part (ii) of Proposition 2 with the hypothesis W_H(F_1) = 1 and the condition W_L(F_0) > 0; Step 4 of the proof (A3:75-86) takes the fragment's text, which also drops the example's sentence at A3:85-86 ("In the point-mass benchmark ...") under rule 4. The prose writer's target T-4.1 matches the statement.

## 4. The example

At the example, class H outbids every incumbent on the path (h = 10 > r_2 = 18/5), and W_L(U[0, r]) = ell/r > 0, so the share rises strictly from r_0 to r_1.

| strength | entry in class H | entry in class L | high-class ownership | class H's takeover share |
|---|---|---|---|---|
| r_0 = 6/5 | 1/4 | 1/4 | 1/8 | 6/11 = 0.545455 |
| r_1 = 3 | 0.648803 | 0.396711 | 0.324401 | 0.830691 |
| r_2 = 18/5 | 1/4 | 1/4 | 1/8 | 18/23 = 0.782609 |

At r_1 and the prior 1/2, the share is [3 + (12e - 3) beta]/[4 + (13e - 1) beta] with beta = 294655/10^6; the program evaluates it both from this closed form and from the class ownership probabilities, and the two enclosures overlap (difference within 1e-60). The general condition at (U[0, r_0], U[0, r_1]) has the value 0.408432.

Proposed rows of the numbers table (the names of `plan/lens_delivery.md` 3.1, part A):

| name | exact value | display | computed as |
|---|---|---|---|
| `share_H_r0` | 6/11 | 0.545455 | pi/(pi + (1 - pi) ell/r_0), exact rational |
| `share_H_r1_B` | [3 + (12e - 3) beta]/[4 + (13e - 1) beta] | 0.830691 | pi e_H/(pi e_H + (1 - pi) e_L ell/r_1), interval in e at 60 digits |
| `share_H_r2_B` | 18/23 | 0.782609 | pi/(pi + (1 - pi) ell/r_2), exact rational |

The prose writer's targets T-1.3 and T-4.4b write the first two as `own_share_r0` and `own_share_r1_B`; one set of names is needed. The fragment itself prints no number.

## 5. Printed lines

Command, from a private scratch folder: `python3 -I audit/theory_upgrade_2026_10_25/statements/O6/o6_shares.py` (absolute path). Exit status 0, about 0.1 seconds. Main lines:

```
  lambda         [0.336121768915121, 0.336121768915121]  width 2.72e-61
  b              [0.195615040180315, 0.195615040180315]  width 1.36e-61
  r_0 = 6/5:  W_H = 1   W_L = 5/6
  r_1 = 3:  W_H = 1   W_L = 1/3
  r_2 = 18/5:  W_H = 1   W_L = 5/18
  r_1  entry in class H [0.648802606821577, ...]  entry in class L [0.396711280135236, ...]
       entry [0.522756943478407, ...]  ownership, class H [0.324401303410789, ...]
       class H's share [0.830690945230374, 0.830690945230374]  width 1.17e-60
  r_0: share = 6/11 = 0.5454545454545454   ownership, class H = 1/8
  r_2: share = 18/23 = 0.782608695652174   ownership, class H = 1/8
  closed form    [0.830690945230374, 0.830690945230374]  width 7.0e-61
  difference     [-9.33452291679171e-61, 9.33452291679171e-61]
  condition value [0.408431745639569, 0.408431745639569]
  (h^2 - p^2)/(2h) = 399/80 = 4.9875
  c_H - (h^2 - p^2)/(2h) = 81/80 = 1.0125
  h - r_2 = 32/5 = 6.4   h - r_2 - c_H = 2/5
  root of g_H(r) = c_H in (p, h): 4 + sqrt(63)/2 = 7.9686269665968858858
  h minus that root = 2.0313730334031141142
```

The entry and ownership values agree with the existing rows `entry_r1_B` (0.522757) and `own_r1_B` (0.324401). The last block serves the decisive-advantage lemma of `A.tex` (Lemma A.6 and Corollary 1(e)).

## 6. Build and scan

- `O6_proof.tex` built in a private scratch folder inside a wrapper that loads `../tex/preamble` and stand-ins for the cited labels: exit 0, one page, no warning other than hyperref's empty link targets of the stand-ins.
- Language scan: see the coordinator's summary for this area; no hit is left in the fragment.
