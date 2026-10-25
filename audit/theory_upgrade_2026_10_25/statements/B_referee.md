# Area B: referee assessment

The statement package requires the scope repairs B-01 to B-04 below. The region theorem, the balance argument, both example corollaries, and the two proof conclusions hold. **O5: accept. O9: accept. The uniform, separated and affordable incumbent implies the balance condition.** Decision 4 therefore takes its first branch.

Locations below are relative to `audit/theory_upgrade_2026_10_25/`. Statement item numbers follow the eighteen items in the mathematics writer's notes. The mathematical verdicts are distinct from the notation and language requirements.

## Verdict per statement

| Item | Statement | Verdict | Reason or required repair |
|---|---|---|---|
| 1 | Setting | missing qualifier | Define the positive threshold-reaching rate for `pi < tau < 1`; call it feasible precisely when `tau <= M`. B-05. The path identities hold. |
| 2 | Lemma A.7, the high class | accept | All five forms have the correct return inequalities, investor rules, challenger rules and interior-rate restrictions. The treatment of `tau >= M`, including `tau >= 1`, holds. |
| 3 | Lemma A.8, the low class | accept | The rate is unique under the mixing investor. The abstaining investor's nonexistence band includes equality at the full-sale return, as required. |
| 4 | Lemma A.9, product structure | accept | With `s_+ >= s_-`, the zero-order posterior is at most the prior. Equal posteriors have equal entry in this construction; the price construction is consistent under both challenger rules. |
| 5(a) | Proposition 3, full statement: region | accept | The exact inequalities, uniqueness under the default rules, entry formula, convexity and necessary prior ceiling follow from the referee's region proof. |
| 5(b) | Proposition 3, full statement: sure purchases | accept | The set is an intersection of up-sets and down-sets. The gap sentence refers to the spread range, without attributing an equilibrium to a gap. |
| 5(c)(i) | Balance: up-set and interval | accept | Starting from any point with `J >= k`, the numerator is positive and cannot fall; the positive denominator cannot rise. Strict spread growth strictly lowers the denominator. A positive start margin is unnecessary for this conclusion. |
| 5(c)(ii) | Balance: closed endpoints | accept | Compactness, continuity and the threshold above the prior at the weakest strength are stated. Conditional on a nonempty intersection, the stated extrema exist and give its endpoints. |
| 5(c)(iii) | Uniform incumbent | accept | O9 establishes the product inequality itself, including equality in affordability, and the strict rise of `J`. |
| 5(c)(iv) | Squared balance and threshold-pair entry | missing qualifier | The denominator comparison holds. The equilibrium interpretation needs the mixing challenger rule and a feasible threshold-reaching rate. B-01. |
| 5(d) | Existence at the even prior | accept | O5 covers all cases under its stated threshold and investor hypotheses, including `tau >= 1` and a purchase posterior at the threshold. |
| 6 | Main-text Proposition 3 | accept | Its three parts follow from the full statement. The prior and slot stay fixed, the rules are stated, and strict entry growth is with the spread before full purchases. |
| 7 | Two intervals of coexistence | accept | The exact endpoints and the claim for every slot in the stated band follow from the auction terms. B-06 concerns the strength index only. |
| 8 | Other tie rules, general law | overclaim | The coexistence sets and the interior threshold-pair comparison hold. At `tau = pi`, entry equal to the floor describes a possible construction, not every quiet market or every informative market. B-04. |
| 9 | Example path and marked strengths | missing qualifier | Restore the slot band for the simultaneous marked-strength definitions, particularly the root `r_C`. B-02. |
| 10 | Lemma A.10, example path | accept | The two product margins and endpoint fractions reproduce exactly. The squared-product comparison holds on the entire example path. |
| 11 | Lemma A.11, marked-strength order | accept | The band is explicit. The ordering follows from the path signs and the strict inequalities in the referee's proof. |
| 12 | Forms at the even prior | missing qualifier | State the mixing investor and the default challenger rule for these forms, and retain the slot band for their marked-strength notation. In particular, the displayed full-purchase entry at `r_C` selects the preparing challenger. B-02. |
| 13 | Corollary 2, full statement | accept | The table, all endpoints, the low-class rate, entry profile and existence claim follow under the explicit band and default rules. At `r_A` the threshold pair recruits with probability one. |
| 14 | Main-text Corollary 2 | accept | The even prior, band and both rules are stated. The entry formula applies along the informative branch starting at `r_A`; the drop occurs strictly above `r_C`. |
| 15 | Coexistence at other priors: definitions | accept | The truncated definition of `r_C(pi)` and the conditional definition of `r_pi` avoid unattained roots. The inverse-posterior formula is correct. |
| 16 | Corollary A.2 | accept | All four cases hold for every interior slot. At the lowest prior the singleton is a full purchase, since `M = tau_A`; in case (b), `r_A` is the interior threshold pair. The entry formula covers both boundaries. |
| 17 | Other tie rules in the example | missing qualifier | Restore the band for the even-prior classification, and restrict the printed endpoint evaluations to the example's slot. The general-prior coexistence-set formulas hold. B-02 and B-03. |
| 18 | Figure note on the threshold pair | accept | With the figure's even-prior band, the threshold pair exists under the default rules at `r_A` and under the mixing challenger rule through `r_J`. |

## Issues

### B-01: blocker: threshold-pair scope

**Location:** `statements/B.tex:143–145,180–185`; corresponding scope summary in `statements/B_notes.md:127–134`.

Parts (a) to (c) expressly select a challenger who prepares at indifference. Under that rule an interior threshold pair requires `J = k`. The range `rho J <= k <= J` instead describes the challenger who may prepare with any probability. Moreover, these two inequalities alone do not imply `pi < tau < M`; outside that posterior range the computed threshold rate can be negative or exceed the slot's presence probability.

**Fix:** Preserve the denominator conclusion under the path hypotheses. State the entry comparison separately: when an indifferent investor may mix and an indifferent high-cost challenger may prepare with any probability, the threshold pair's entry is nonincreasing on strengths satisfying `pi < tau < M` and `rho J <= k <= J`. Treat `tau = M` as the full-purchase boundary. Exempt this sentence from the default-rule frame.

### B-02: blocker: example band and rules lack a common home

**Location:** `statements/B.tex:278–287,327–340,443–450`.

The general setting fixes an arbitrary interior slot. The example's marked-strength paragraph does not impose the band that guarantees a ceiling root on the path. The band appears in Lemma A.11 and Corollary 2 as local hypotheses, while the even-prior tie paragraph follows Corollary A.2, which expressly permits every interior slot. Thus the latter paragraph's classification has no stated band. The form definitions also select the default challenger at the ceiling without saying so.

For instance, `lambda = 1/100` and `beta = 1/5` give `M(1/2) = 104/203`, below `tau(r_0) = 195/308`. There is no ceiling root on the example path and no recruiting threshold pair at `r_A`. This slot satisfies the general setting.

**Fix:** Give the marked strengths, forms and even-prior tie classification the explicit band `tau(r_1) < M(1/2) < tau(r_2)`. State that the form list takes the default rules, and name the alternative rule at each exception. Keep the every-slot result of Corollary A.2 separately scoped.

### B-03: blocker: endpoint evaluations depend on the slot

**Location:** `statements/B.tex:457–459`.

The endpoint strength and prior are slot-independent, but its top posterior, zero-order posterior, full-purchase return and entry are not. The printed values are those of the example's slot. At the allowed slot `lambda = 2/5`, `beta = 1/5`, the endpoint instead has top posterior approximately `0.889499248`, full-purchase net return approximately `-0.006401145`, and informative entry approximately `0.443795749`; its purchase rate is approximately `0.212894981`, strictly below the presence probability. The printed full-purchase description therefore fails for an allowed slot.

**Fix:** Keep the singleton coexistence-set claim at general slots. Begin the sentence containing the four slot-dependent evaluations with “At the example's slot”.

### B-04: should fix: entry at a prior equal to the threshold

**Location:** `statements/B.tex:262–263`; `statements/B_notes.md:206`.

When an indifferent high-cost challenger may prepare with any probability and `tau = pi`, a quiet market can have entry above the floor. Constant entry `e` at its pooled price is consistent with abstention whenever `rho <= e <= min{1,k/[Delta_T max{pi,1-pi}]}`. The sentence that “the quiet market keeps entry rho” selects one member of this set. The informative construction also permits above-floor entry after a sale whose posterior is the prior when that sale remains unprofitable.

Using the example's auction at the strength where `tau = pi = 0.645` gives strength approximately `1.503615044` and spread approximately `0.084339444`. A quiet market with entry `0.3` has gross purchase and sale returns approximately `0.008982151` and `0.016319682`, both below the trading cost `0.02`. A recruiting purchase also exists there under the example's slot.

**Fix:** Say “One quiet market has entry rho after every order, and one informative market is constructed as in part (a), with entry rho after a sale.” The region formula needs no change.

### B-05: should fix: threshold-rate definition

**Location:** `statements/B.tex:54–59`.

The setting permits `tau < pi`, while `tau < 1` alone does not give a positive rate. For `tau < pi`, the displayed expression is negative and is not an investor rate in `[0,lambda]`. For `M < tau < 1`, it is an algebraic threshold-reaching quantity outside that feasible interval.

**Fix:** Introduce the expression for `pi < tau < 1` as the positive rate required to reach the threshold, and state that it is feasible exactly when `tau <= M`. The lemmas already impose the needed prior restriction.

### B-06: should fix: frozen notation

**Location:** `statements/O9/O9_proof.tex:18–63`; `statements/O9/O9_notes.md:40–54,68–81`; `statements/B.tex:189–192,239–247`; `statements/O5/O5_proof.tex:12–16,38–94`; corresponding notes.

The uniform proof introduces the referee's `d`, `X` and `A`, although the notation card assigns the class mean gap to `bar Gamma` and requires the other two expressions to be written out. The existence construction uses `t` as a sale rate, and the two-piece economy uses `t` as its strength index; the notation card reserves `t` for proceeds and names path strengths `r`. These are mathematical notation conflicts, independent of the correctness of either proof.

**Fix:** Use `bar Gamma` for the class mean gap, write `g_H-c_H` and `(r^2-p^2)/(2r^2)` in place of the temporary letters, use the existing low-class rate notation for the existence construction, and index the mixture path by `r`. Use the decorated spread `Delta_T` consistently in the notes.

### B-07: minor: derivative at the weakest uniform incumbent

**Location:** `statements/O9/O9_notes.md:20`.

The notes claim a strictly positive derivative bound without the proof's restriction `r > min I`. Under the uniform support hypotheses alone, a low class concentrated at `min I` is allowed. Then both the spread and its derivative vanish at that endpoint, and `J'` is zero there. The strict increase over any nondegenerate interval remains true. The main statement's standing positive-spread hypothesis also excludes this endpoint case.

**Fix:** Give the weak derivative bound on all of `I` and its strict version where the spread is positive, or state `r > min I` as the proof does.

### B-08: should fix: retrospective narrative in the notes

**Location:** `statements/B_notes.md:163–169,229–244,270–276,385–407`; `statements/O5/O5_notes.md:74–78`; `statements/O9/O9_notes.md:56–61,86–94`.

The notes include change narration such as “drops”, “becomes”, “leave”, and “What it changes in the plan”. This is separate from the source locations and exact-value inventory that the brief requires. Rule (3) applies to committed project documents as well as mathematical prose.

**Fix:** Retain the requested source, placement, numbering and exact-value mappings as reference data. State the mathematical scope directly and remove the retrospective narrative. The mathematical text under review contains no status labels, defensive passages, prohibited names or non-neutral name for the example.

## O5: proof assessment

**Verdict: accept.** The conclusion is existence for every continuous incumbent law satisfying the standing positive spread and profit gap, the even prior, a threshold strictly above the prior, and a mixing investor, under either challenger rule. The unrestricted existence claim for every threshold would be false.

Each proof step holds:

1. The even-prior posterior identity equates the distance to truth of a purchase and sale at the same rate. The product construction has the correct price beliefs and entry at coincident posteriors.
2. With the floor return at most the trading cost, the quiet market satisfies both class incentives, including equality.
3. Above that bound, the low-class rate is the unique interior or full-sale rate. Its gross return is at least the trading cost, with equality at an interior rate.
4. If a purchase at that rate does not recruit, the same rate for both classes gives the required floor-entry equilibrium. This covers thresholds at or above one.
5. If it reaches the threshold, the recruiting return there exceeds the trading cost strictly, by the factor `1/rho`. Either a full purchase pays, or its break-even interior rate is strictly larger than the sale rate and has a posterior strictly above the threshold. At the possible full-purchase threshold tie, entry one is permitted under both challenger rules.

The sharpness argument in the notes also holds. With the preparing challenger, the sale return jumps from strictly above the trading cost to strictly below it as the sale posterior crosses the threshold; no sale rate is a best response. Its exact example gives spread `1/60`, threshold `885/2156`, and `rho Delta_T tau < 1/200 < Delta_T tau`. This supports the threshold qualifier already present in the statement.

The even-prior computations gave a quiet market at strength `1.2`; a full purchase with a mixed sale at strength `2`; full orders with recruiting purchases at strength `3`; and full orders with floor entry at strength `3.6` when the high cost is `12`, whose threshold exceeds one. At strength `2`, the sale return is exactly `0.02`. In the last case both correct-order returns are approximately `0.063126528`, with entry `0.25` everywhere. These evaluations agree with the construction; the proof supplies the all-law conclusion.

## O9: proof assessment

**Verdict: accept. Yes: the uniform, separated and affordable incumbent implies the balance condition.**

The auction terms in Step 1 follow by integrating the uniform incumbent's payment and the low class's rent. Their spread is the low-class mean of the squared distance from the incumbent's upper bound, divided by twice that bound. The derivative and the constant sum of the spread and profit gap are correct.

Step 2 supplies the two inequalities needed in Step 3: affordability bounds the high class's net margin from below by `r(r^2-p^2)/(2r^2)`, and separation gives `r Delta_T' >= Delta_T`. Both use nonnegative values and the stated support restrictions. Also the profit gap is at least `c_H > 0`.

Their substitution in the product derivative proves nondecrease directly. Differentiating the ratio for `J` gives the lower bound in Step 4. It is strictly positive wherever the spread is positive, and at every strength above the weakest one even when that weakest spread vanishes. Hence the strict-increase conclusion holds. The proof requires no computation to establish its sign.

The supplementary comparisons also reproduce: with high cost `33/5`, the example's balance margin is `4699/8280`; in the affordable uniform economy with low value `1`, reserve `1/2` and interval `[3/2,5]`, the squared-product derivative at strength `5` is `-9801/10000`. With high value `100` and high cost `95`, the derivative of `Delta_T(1-tau)^2` is `-4302639/46200521200`; with high value `10` and high cost `5`, it is `107811/20261200`. Thus the squared condition remains a separate hypothesis.

## Numbers, numbering and rendered document

The exact example margins reproduce as `9667/8280`, `937/5520`, `2/5`, and `27/1451`. The endpoint threshold fractions are `195/308` and `4245/5804`; the initial purchase return is `113/18480`, and the final floor purchase return at the threshold is `263471/4178880`.

For the mixture path, the spread is one tenth of the upper centre minus one, the low-class profit is nine tenths of one minus the lower centre, and the profit gap is nine minus the spread. These give:

| Path strength | Threshold | Recruiting return |
|---|---:|---:|
| 0 | 0.630660852 | 0.021052331 |
| 1 | 0.668903053 | 0.018872526 |
| 2 | 0.670627803 | 0.026349776 |

The coexistence endpoints are exactly `3137/6498` and `(1485-sqrt(2127361))/23`. Across the stated slot band the threshold remains strictly below the top posterior; the quiet-market condition also holds throughout. Solving the purchase-return inequality gives precisely the two claimed components.

The displayed numbering follows decision 7: Proposition 3, main-text Corollary 2, named and unnumbered full statements, Corollary A.2, and the five appendix lemmas A.7 to A.11 conditional on the three preceding lemmas described in the notes. The two region/entry equations and the two existence-proof equations require their stated appendix equation counter at integration. The standalone statements display the former as equations (1) and (2).

The prescribed build of `B.tex` completed in the private referee build directory. I read all seven PDF pages as text and rendered pages. Cross-references resolve. Eleven expected unknown values appear, all with exact definitions in the notes: the eight `twopath_*` values and the three margins `margin_unif_afford_B`, `margin_balance_B_frac`, and `margin_balance_sq_B_frac`. The long placeholder names produce overfull lines of approximately 29.18 points and 2.03 points on page 5; the mathematical content is legible. These are the expected draft values, not additional mathematical findings.

The language scan over the six supplied sources reports no status, defensive, history, prohibited-name or example-naming hits. It reports 125 process hits in the notes and one placeholder mention, plus 23 permitted tie-rule phrases. The source-location and exact-value mappings are required review data; the retrospective narrative is addressed in B-08. The notation conflicts in B-06 are outside that scan's coverage.

All computations were print-only evaluations with exact rational arithmetic for rational quantities and higher-precision arithmetic for roots and slot-dependent values. No tests or test suites were written or executed. The only repository output of this assessment is this report.

The language review of this report treats statement identifiers, source locations and the account of computations as the structured evidence requested by the brief. The mathematical possibilities described in B-04 and B-07 are existence claims.
