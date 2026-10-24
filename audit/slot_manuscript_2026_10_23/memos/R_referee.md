# R_referee: manuscript referee report

Date: 23 October 2026. Scope: `overleaf/competition_slot/main.tex`, all nine main sections, all nine appendix files, and the supplied 101-page PDF.

## Summary verdict

**Revise before circulation.** The central reversal survives this read. Its proof states the candidate objects and uses bounds on every profile.
The benchmark equilibrium set also survives, with the stated tie rules. The research calculations agree with an independent derivation.

Four demonstrated claim errors need correction:

1. Proposition A.12(a) admits ratios whose implied liquidity probability exceeds the model's bound.
2. Section 6.3 gives the wrong order support for its strong-incumbent signal example.
3. Section 8 excludes an informed-share endpoint that the adopted investor rule permits.
4. Proposition A.9 omits the zero-coefficient exception from its strict comparative static.

These errors do not refute Propositions 1–4. They affect an identification statement, two summaries, and one strictness clause.
The remaining findings concern proof domains, certificate records, and exposition.

**Analytical:** the auction identities, the main reversal, the control, and the principal robustness and welfare arguments are sound.
**Computer-assisted:** the path signs, benchmark thresholds, and research values agree with independent exact or interval calculations.
**Open:** the research equilibrium set on the interval already marked open in Section 5 stays open.
Equilibrium selection, the seller's optimal reserve, and trade under the alternative payment rule also stay open.

No core mathematical claim of BRIEF §§2–5 is refuted. Finding 4 corrects the literal strictness clause in LABELS §1.
The earlier check memos served as source locators. Their verdicts did not substitute for this read.

## Evidence and method

The review read every numbered statement and its appendix proof. The statement map below records all 35 results.
The auction formulas agree with equation (4) of the pinned manuscript at commit `01bd5d6`.
The review made no change to the manuscript, registry, proof packages, or existing calculation files.
No tests, test suite, or outside source entered the review.

The independent CLI calculation is:

```bash
.venv/bin/python audit/slot_manuscript_2026_10_23/scripts/R_referee/recompute.py
```

Its output is `scripts/R_referee/recompute.log`, relative to the team folder.
The program imports no project calculation module. It uses exact fractions and outward interval arithmetic.
It bounds Euler's number by its series through term 100 and the following exact tail bound:

\[
S_{100}=\sum_{n=0}^{100}\frac1{n!},\qquad
S_{100}<\mathrm e<S_{100}+\frac{102}{101\,101!}.
\]

Exact rational bisection encloses the roots for coexistence and the prior cutoff.
An independent polynomial calculation reproduces both derivative polynomials and their Sturm counts.
For \(J'\), the variation counts are \((3,3)\) on \([6/5,18/5]\).
For \([\Delta_T(1-\tau)^2]'\), they are \((5,5)\) on \([6/5,2]\).
Both initial signs are positive. These counts establish the two signs used in Proposition 3.

Selected independent values are:

| Object | Independent value, rounded here |
|---|---:|
| Presence probability | 0.336121768915121197397184 |
| Entry at \(r_1\) | 0.522756943478406671709643 |
| High-class ownership at \(r_1\) | 0.324401303410788560366794 |
| \(r_A\) | 1.393957920279251333027115 |
| \(r_F\) | 1.467127041293093798614599 |
| \(r_N\) | 1.747877538267962743567348 |
| \(r_J\) | 1.966097064963998869830784 |
| \(r_S\) | 2.124148132815450673539019 |
| \(r_C\) | 3.592658518794661833335916 |
| Prior interval for (H1)–(H3) | (0.467850029686148512…, 0.500424307320063228…) |
| Research at 1.55, 1.60, 1.65 | 0.237901194995…, 0.279037101523…, 0.316683177856… |
| Research-branch entry at those strengths | 0.507630115665…, 0.513965405209…, 0.519763230368… |
| Price-access proceeds gain at \(r_1\) | 0.257947801368128764778116 |
| Price-access net surplus gain at \(r_1\) | 0.081960230777466029404929 |

The log records outward bounds, including both endpoints. The rounded values above do not define new exact cutoffs.
The calculation also reproduces the three strong-economy prices, spreads, and conditional announcement means.

## Demonstrated findings, ranked by severity

### 1. Major — Proposition A.12(a) omits the admissibility restriction

**Status: analytical; counterexample computer-assisted.**

**File and lines:** `overleaf/competition_slot/appendix/A8_empirical.tex:85–111`, especially lines 89–90.

**Problem.** The proposition says that every ratio \(u'>0\) gives exactly one pair with the observed volume.
Within this model, a pair must also satisfy \(\beta'\le1/3\).
The proof derives the missing restriction but does not impose it in the statement.

For fixed volume \(v\), the unique algebraic solution is

\[
\lambda'=\frac{vu'}{u'+2},\qquad
\beta'=\frac{v}{2+u'(1-v)}.
\]

At the benchmark volume, set \(u'=1/10\). The independent calculation gives

\[
\beta'\in
[0.3587848237033434500020199,\ 0.3587848237033434500020200].
\]

This pair lies outside the model. There is no admissible pair with this ratio and the benchmark volume.

**Fix.** State existence exactly when \(3v\le2+u'(1-v)\). State uniqueness conditional on existence.
At the benchmark volume, this means

\[
u'\ge\frac{3v-2}{1-v},\qquad
\vartheta'\ge3-\frac2v.
\]

Part (c) already verifies admissibility throughout its narrower band. That result survives.

### 2. Major — the main text gives the wrong support in the private-signal example

**Status: analytical; strict payoff computer-assisted.**

**File and lines:** `overleaf/competition_slot/sections/06_robustness.tex:80–83`.
The correct calculation appears at `overleaf/competition_slot/appendix/A6_robustness.tex:505–532`.

**Problem.** The main text says that both investor types mix at both strengths.
At \(r_1=3\), the favorable-signal type buys with probability one.
Its purchase strictly beats abstention:

\[
U_+(1)=\frac25\,m\,\frac{137}{192}-\frac1{50}
\in[0.0567603640160194407137316,\ 0.0567603640160194407137317].
\]

Thus this type cannot mix with abstention. Only the unfavorable-signal type mixes at the strong strength.
At the weak strength, both types mix with trade probability about 0.721409.
At the strong strength, the unfavorable-signal type sells with probability about 0.775969.

**Fix.** Replace the sentence with: “Both types mix at the weak strength. At the strong strength, the favorable type buys fully and the unfavorable type mixes.”
Keep the reported entry values and the I0 nonexistence conclusion. Their supporting calculation survives.
The appendix already contains the correct support.

### 3. Major — Section 8 excludes a valid endpoint under rule IM

**Status: analytical; admissible pair computer-assisted.**

**File and lines:** `overleaf/competition_slot/sections/08_empirical.tex:28–31`.
Related records: `appendix/A8_empirical.tex:91–92,112–116` and `registry/registry.csv:5193`, under the team folder.

**Problem.** The main text excludes the informed share \(19/25=0.76\).
Proposition A.12(b) uses the correct weak inequality. Rule IM permits a full sale at the exact tie.

At the benchmark volume, choose

\[
\vartheta'=\frac{19}{25},\quad
\lambda'=v\vartheta',\quad b'=\frac{v(1-\vartheta')}2.
\]

The implied liquidity probability is about 0.195169418251, within the model's domain.
Full orders give posteriors \((3/25,1/2,22/25)\) and entry \((\rho,\rho,1)\) at \(r_1\).
The purchase posterior exceeds the preparation threshold by \(7/40\).
The decisive investor payoffs are

\[
U_H(1)=\frac23\frac3{25}-\frac1{50}=\frac3{50}>0,
\qquad
U_L(-1)=\frac14\frac23\frac3{25}-\frac1{50}=0.
\]

Rule IM allows the full sale. Wrong-signed orders lose money. The price and entry formulas complete the equilibrium tuple.
Rule I0 excludes the full sale at this endpoint.

**Fix.** Include the upper endpoint under IM. Use an open upper endpoint only for strict investor incentives or rule I0.
Revise the registry note that describes an equilibrium with “iff” and a strict inequality.
Distinguish equilibrium existence from strict incentives in that note.

### 4. Major — the payment proposition omits the zero-coefficient exception

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/appendix/A7_welfare.tex:102–114`.
The same omission occurs at `overleaf/competition_slot/sections/07_welfare.tex:39–40` and LABELS §1.

**Problem.** The statement makes the spread response strict whenever \(\mathbb E[(R-\ell)_+]\) changes strictly.
At \(\omega=1/2\), the spread stays constant:

\[
\Delta_\omega=\omega(h-\ell)+(1-2\omega)\mathbb E[(R-\ell)_+].
\]

Across the two benchmark strengths, the expectation rises by \(13/20\).
At \(\omega=1/2\), the spread change is exactly zero.
The proof correctly adds \(\omega\ne1/2\) at lines 132–135. The statement does not.

**Fix.** State strictness when the expectation changes strictly and \(\omega\ne1/2\).
State that the spread stays fixed at \(\omega=1/2\).
This change preserves the formula and every payment calculation.

### 5. Minor — the purchase-only identification clause needs its own scope

**Status: analytical; illustration computer-assisted.**

**File and lines:** `overleaf/competition_slot/appendix/A8_empirical.tex:85–86,100–101,128–129`.

**Problem.** Part (e) says “when only class H trades.” Its proof assumes that class H buys fully.
Moreover, the proposition's opening condition \(r_S<r<h\) forces both classes to trade.
Thus part (e) is vacuous under that opening condition. It does not state the intended result for another regime.

For a mixed purchase with rate \(s=\lambda\sigma_H(1)\), the counts instead give

\[
2\mathbb E[X]=s,\qquad v=2b+s/2.
\]

At benchmark strength \(r=1.4\), Proposition 3 supplies such an equilibrium.
Here \(\sigma_H(1)\approx0.498837177317\), and \(2\mathbb E[X]\approx0.167670034440\).
The actual presence probability remains about 0.336121768915.
This illustration lies outside \((r_S,h)\). It refutes the unrestricted extension, not the literal vacuous conditional.

**Fix.** State part (e) as a separate result for \(\sigma_H=\delta_1\) and \(\sigma_L=\delta_0\), at prior one half.
Do not apply its formula to branch R. Counts on branch R identify the purchase rate, not the presence probability.

### 6. Minor — Lemma A.3 uses an undefined threshold outside its feasible case

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/appendix/A4_coexistence.tex:147–164`.

**Problem.** The text defines \(s^*\) only when \(\pi<\tau<M(\pi)\).
Lemma A.3 assumes only \(\pi<\tau\), yet its Q and R cases use \(s^*\).
It also includes the cases \(M(\pi)\le\tau\). These cases matter above the ceiling and at small priors.

**Fix.** Define the algebraic expression for \(s^*\) throughout the path when \(\pi<\tau<1\).
Then state that it lies in \((0,\lambda)\) exactly when \(\tau<M(\pi)\).
At equality, it equals \(\lambda\). The existing classification then works without a new argument.

### 7. Minor — make the trading lemma's premises include the payoff basis

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/sections/03_competition_information.tex:168–175` and
`overleaf/competition_slot/appendix/A2_beliefs_trading.tex:126–137`.

**Problem.** Lemma 3 states (E1), (E4), and the entry bounds as its premises.
Its proof invokes the terminal-payoff identity from Step 0, which explicitly uses truthful bids, condition (E6).
Without that condition, (E4) alone does not connect actual proceeds to the truthful-auction objects \(t_j\).

**Fix.** Add (E6), or directly assume the stated class-conditional terminal-payoff identity.
All later applications use candidates that include (E6), so this repair changes no application.
Also change “condition (E5)” to “condition (E6)” at `appendix/A1_payoffs.tex:18`.

### 8. Minor — finish the unrestricted positivity proof for announcement reports

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/appendix/A8_empirical.tex:170–194`.

**Problem.** Parts (i)–(iii) do not assume full orders. The strict positivity proof in part (iii) ends with a fact about \(\mathcal F\).
The general formula is correct, but the last step proves less than the stated scope.
The opening phrase “After the order x” also obscures the average in part (iii).
That part averages across orders. Conditional on a purchase with entry one, the preparation report changes the price by zero.

**Fix.** State the averaging population in part (iii). Add the general argument.
Every equilibrium obeys \(\mathbb E[\mu(X)]=1/2<\tau(r)\).
Thus at least one order has posterior below the threshold and entry \(\rho<1\).
That order has positive probability and positive preparation probability. Its contribution to the conditional mean is positive.
Alternatively, restrict part (iii) to \(\mathcal F\). The broader result needs only the short argument above.

### 9. Minor — the registry still labels a rounded point as an enclosure

**Status: computer-assisted.**

**File and lines:** `audit/slot_manuscript_2026_10_23/registry/registry.csv:5206`.
Cause: `scripts/P5_observables/p5_observables.py:92–93`, relative to the team folder.
Relevant manuscript claims: `appendix/A8_empirical.tex:217–225` and `appendix/A9_parameters.tex:73–77`.

**Problem.** The volume row gives this purported enclosure:

\[
[0.72735184927575112456,\ 0.72735184927575112456].
\]

The independent outward enclosure is

\[
[0.7273518492757511245590493,\ 0.7273518492757511245590494].
\]

The recorded point excludes the true value. The formatter rounds both endpoints to nearest.
The six-place display is correct. The independent XP5 file also supplies a valid wider certificate.
Thus this is a certificate-record defect, not a refutation of the empirical formulas or their printed values.

**Fix.** Serialize lower endpoints downward and upper endpoints upward.
Keep the exact endpoints or a valid outward decimal pair in the merged registry.
Do not describe nearest-rounded endpoint strings as enclosures.
The own calculation demonstrates this row; it does not claim an exhaustive count of affected rows.

### 10. Minor — the open-set summary includes blocks with deliberate failures

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/appendix/A9_parameters.tex:246–255`.

**Problem.** The paragraph says each block defines an open set that contains the benchmark.
Some table rows explicitly fail by design. The atomless-cost third-economy condition has a negative margin at the declared half-width.
The point-class control also fails its recruitment condition. These blocks cannot all define sets that contain their declared examples.
Exact boundary equilibria also use equalities and weak best-response inequalities.

**Fix.** Apply the open-set claim to the positive-margin sufficient conditions for each intended result.
Exclude the declared failure rows and boundary cases from that sentence.
Keep the structural restriction \(\beta\le1/3\) and the relative-openness qualification.
Do not remove valid boundary equilibria to satisfy the strict-margin convention.

### 11. Minor — state the four-class inputs beside their certificate

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/appendix/A6_robustness.tex:345–353` and
`overleaf/competition_slot/appendix/A9_parameters.tex:1–6,47–56`.

**Problem.** The four-class example gives equal priors and “point values close” to the benchmark values.
It does not state the four values. The declarations table does not supply them.
The named script contains them, so the result is reproducible from the repository, but the manuscript's input declaration is incomplete.

**Fix.** Add the values \((1,1001/1000,9999/1000,10)\) and the low/high partition beside the example.
These are the inputs at `scripts/P2_auction/derive.py:479`, relative to the team folder.
The vertex argument and Proposition A.6 remain valid.

### 12. Minor — qualify the lower boundary of the admissible region

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/appendix/A3_proposition2.tex:168–170,199–204` and
`overleaf/competition_slot/sections/04_equilibrium_results.tex:120`.

**Problem.** The blanket “outside this band” sentence includes the lower boundary.
At \(u=u_{\rm lo}\), all three primary C1 outcomes still hold.
Orders remain uniquely full at the two higher strengths, and C1 selects preparation at the purchase tie.
The outcome's robustness to every challenger tie rule fails at this boundary.
The proof already records this distinction, but the summary does not.

**Fix.** Say that the open strict-hypothesis region is exact.
Describe the lower-boundary outcome separately, with its tie-rule qualification.

### 13. Editorial — retain the conditions in the reserve and cluster summaries

**Status: analytical.**

**File and lines:** `overleaf/competition_slot/sections/01_introduction.tex:88–93`,
`sections/09_conclusion.tex:15–19`, and `sections/08_empirical.tex:53–61`.

**Problem.** The reserve summary omits the condition that the top posterior recruits at both strengths.
Exclusion of the low class alone does not imply flat entry. The manuscript's own deterrence reserve gives a counterexample.
At \(p=31/20\), the independent top-profit margins are about 0.177444989697 and −0.078730252613.
Entry therefore falls from about 0.522757 to 0.25, although the low class is excluded at both strengths.
Proposition A.10 correctly distinguishes the two cases.

The cluster paragraph also moves from two possible equilibria to two clusters that processes “therefore form.”
Multiplicity permits those patterns; it does not require both patterns to occur in a sample.
The next sentence correctly leaves selection open.

**Fix.** Add the recruitment condition to the reserve summary.
Say that the model “permits two clusters” at intermediate strengths.
Keep these qualifications at the relevant claims. No general disclaimer is needed.

### 14. Editorial — remove residual notation collisions and shorten repeated explanations

**Status: analytical.**

**Files and lines:**

- `appendix/A9_parameters.tex:23`: “Slot odds” conflicts with the correct interpretation of \(u\). Use “slot mass ratio.”
- `appendix/A7_welfare.tex:76–77`: \(D_0\) conflicts with the reserved CDF gap notation and LABELS §1. Use a named dividend.
- `appendix/A8_empirical.tex:7–8`: \(J_r\) differs from \(J(r)\), and \(d\) differs from the signal accuracy \(d\).
  Use an entry indicator and an order-mass symbol that do not reuse these letters.
- `appendix/A6_robustness.tex:162–176`: \(\Gamma\) denotes both a function and its limit. Name the total mean gap separately.
- `sections/04_equilibrium_results.tex:13`: replace “let F2 be one of F1” with “let F2 strengthen F1.”
- `sections/05_research.tex:66–67`: the best order earns zero, because abstention is available.
  Replace “best order” with “best nonzero order” in the negative-payoff sentence.

The manuscript defines the main notation before use. It distinguishes preparation, ownership, proceeds, and acquisition surplus well.
The long literature paragraphs at `sections/01_introduction.tex:113–150` can be shorter.
The final roadmap sentence at lines 146–152 repeats section names and is hard to scan.

The proof-method account repeats across `sections/02_model.tex:196–199,271–275`,
`sections/04_equilibrium_results.tex:42–53`, and `appendix/A2_beliefs_trading.tex:10–25`.
Keep the definition, one short main-text explanation, and the appendix conventions.
Several full script paths repeat within one appendix paragraph. Define short certificate names once and retain the full path in one location.
This would improve the appendix without a loss of evidence.

## Statement-by-statement proof record

“Confirmed” means that the written argument supports the stated result within its model domain.
It does not mean that every registry row received an independent numerical reconstruction.
The status column distinguishes the proof's analytical and finite computational steps.
File paths in this table start at `overleaf/competition_slot/`.

| Statement | Proof location | Verdict and status |
|---|---|---|
| Proposition 1 | `appendix/A1_payoffs.tex:20–111` | Confirmed, analytical. Indicator integrals, reserve jump, finite means, and both strictness conditions match. |
| Proposition 1(c) | `appendix/A1_payoffs.tex:113–153` | Confirmed, analytical. The monotone kernel and localized continuous distributions prove both directions. The reserve atom exception is explicit. |
| Lemma 1 | `appendix/A2_beliefs_trading.tex:28–68` | Confirmed, analytical. All three orders and the exact use of the liquidity bound receive separate computations. |
| Corollary 1 | `appendix/A2_beliefs_trading.tex:70–77` | Confirmed, analytical. It bounds the price belief, including a price that pools the zero order. |
| Lemma 2 | `appendix/A2_beliefs_trading.tex:79–124` | Confirmed, analytical. Equal prices imply equal entry before the proof infers equal posteriors. CM at the threshold is correctly qualified. |
| Lemma 3 | `appendix/A2_beliefs_trading.tex:126–161` | Correct payoff argument, analytical. Add the explicit premise in finding 7. |
| Proposition 2 | `appendix/A3_proposition2.tex:11–110` | Confirmed, analytical. Each tuple, all six conditions, ownership, and all tie pairs match. Uniqueness uses every-profile bounds. |
| Proposition 3 | `appendix/A4_coexistence.tex:267–362` | Confirmed, computer-assisted. The support cases are exhaustive; the CM threshold branch and the I0 gap are handled. Finding 6 repairs a supporting definition. |
| Corollary 2 | `appendix/A4_coexistence.tex:396–488` | Confirmed, computer-assisted. The four prior cases, exact CM endpoint, and I0 qualification match. Undefined roots are avoided outside their domains. |
| Proposition 4 | `appendix/A5_research.tex:208–239` | Confirmed, computer-assisted. Joint deviations, zero research, both intermediate tuples, and cap uniqueness are justified. CM adds the stated third tuple. |
| Corollary 3 | `appendix/A5_research.tex:241–259` | Confirmed, analytical. The implicit derivative is positive; entry and ownership slopes have the stated signs where the branch is an equilibrium. |
| Proposition A.1 | `appendix/A3_proposition2.tex:157–215` | The exact region and prior ranges are confirmed, analytical. The blanket “outside” wording needs the endpoint qualification stated below. |
| Proposition A.2 | `appendix/A5_research.tex:291–358` | Confirmed, computer-assisted. The lower and upper cost bounds are necessary for the stated strict interior claims. The uniform cap-strip bounds establish sufficiency. |
| Proposition A.3 | `appendix/A6_robustness.tex:8–34` | Confirmed, analytical. The exact crossing probability follows from pointwise optimal-entry indicators under C1. |
| Proposition A.4 | `appendix/A6_robustness.tex:81–127` | Confirmed, analytical. The low-cost floor holds under every profile before the proof forces orders. No atomlessness is used. |
| Proposition A.5 | `appendix/A6_robustness.tex:154–192` | Confirmed, analytical. The construction chooses strengths and costs in a valid order. Continuity preserves the ownership inequality. |
| Proposition A.6 | `appendix/A6_robustness.tex:285–343` | Confirmed, analytical. Separation forces every class's order before the proof infers the posterior vector from the price. Finding 11 concerns its example. |
| Proposition A.7 | `appendix/A6_robustness.tex:429–463` | Confirmed, analytical. The private signal requires class-specific entry. The public-posterior price argument and both trade bounds account for it. |
| Proposition A.8 | `appendix/A7_welfare.tex:14–59` | Confirmed, analytical. The hidden-price tuple is solved separately; orders coincide; the reserve-blocked allocation term is retained. |
| Proposition A.9 | `appendix/A7_welfare.tex:102–136` | Formulas confirmed, analytical. The strictness clause is wrong as written; see finding 4. |
| Proposition A.10 | `appendix/A7_welfare.tex:161–191` | Confirmed, analytical. The proof recomputes reserve-dependent objects and does not assume that the target spread rises across these reserves. |
| Proposition A.11 | `appendix/A8_empirical.tex:45–78` | Confirmed, analytical. Both components rise below the ceiling; only the class component rises above it. The C1 jump and CM interval match. |
| Proposition A.12 | `appendix/A8_empirical.tex:85–131` | Requires revision, analytical. Part (a) omits admissibility; part (e) needs another domain and full purchases. Parts (b)–(d) are supported. |
| Proposition A.13 | `appendix/A8_empirical.tex:141–165` | Confirmed, analytical. Entry leaves the class posterior unchanged conditional on the order; winner and covariance formulas follow. |
| Proposition A.14 | `appendix/A8_empirical.tex:170–200` | Formulas confirmed, analytical. Finding 8 supplies the missing strict-positivity step outside full orders. |
| Lemma A.1 | `appendix/A4_coexistence.tex:19–63` | Confirmed, computer-assisted. Both polynomial identities and root counts agree with the independent derivation. The other signs are analytical. |
| Lemma A.2 | `appendix/A4_coexistence.tex:85–105` | Confirmed, computer-assisted through Lemma A.1. Each threshold inequality follows in the stated band. |
| Lemma A.3 | `appendix/A4_coexistence.tex:153–185` | The five best-response cases are exhaustive, analytical. Finding 6 repairs the domain of its threshold symbol. |
| Lemma A.4 | `appendix/A4_coexistence.tex:187–216` | Confirmed, analytical. The sale return decreases strictly with its rate. The endpoint inequalities give the IM choice and I0 nonexistence. |
| Lemma A.5 | `appendix/A4_coexistence.tex:218–250` | Confirmed, analytical. The price calculation precedes its Bayes and optimal-entry checks. The verification does not assume price sufficiency. |
| Lemma A.6 | `appendix/A5_research.tex:40–59` | Confirmed, analytical. Strict concavity gives the unique research response against fixed prices and entry. |
| Lemma A.7 | `appendix/A5_research.tex:61–79` | Confirmed, analytical. The posterior bounds cover every profile and intensity, including zero. |
| Lemma A.8 | `appendix/A5_research.tex:81–96` | Confirmed, analytical. A profitable sale would also force a profitable purchase. Positive research therefore requires a strict full purchase. |
| Lemma A.9 | `appendix/A5_research.tex:98–176` | Confirmed, analytical. All intensity cases receive separate treatment; the excluded cap/threshold equality is explicit. |
| Lemma A.10 | `appendix/A5_research.tex:178–206` | Confirmed, analytical. Its bound forces both orders and the cap in every candidate. The CM ceiling exception is explicit elsewhere. |

## BRIEF §5: proof-standard assessment

| Requirement | Assessment |
|---|---|
| Explicit equilibrium objects | Met for Propositions 2–4 and the substantive extensions. The common tuple convention supplies prices, both beliefs, entry, and bids. |
| Conditions listed | Definition 1 lists E1–E6. Section 5 adds E7 and treats hypothetical success at zero intensity. Finding 7 repairs one lemma's premises. |
| Verification against the fixed object | Met in the central proofs. Deviations hold prices and entry fixed. The product construction uses direct price algebra before it checks Bayes consistency. |
| Uniqueness under every profile | Met in the core results. Wrong signs are eliminated by payoffs. The bounds cover mixed profiles before candidate orders are selected. |
| Strict hypotheses and margins | Substantially met for the open sufficient regions. The table reports the thin exclusion margin and the declared failures. Findings 3 and 10 distinguish strict interiors from valid ties. |
| Named certificates | Every fully qualified script or log path cited in Appendix A exists. The own calculations reproduce the two finite sign steps. Finding 9 concerns the registry's endpoint serialization. |
| No skipped symmetry step | No proof uses “by symmetry,” “similarly,” or “it is easy” to replace a necessary computation. Findings 8 and 11 identify smaller omissions. |

The main strict margins at B are positive:

\[
\begin{aligned}
c_H-B_0(\pi)&=287/240, & k-\Delta_0&=1/300,\\
B_1(M)-c_H&\approx0.217154821917,
&\rho\kappa\Delta_1-k&\approx0.024823570228,\\
c_H-B_2(M)&\approx0.002688902266.
\end{aligned}
\]

The posterior exclusion margin is about 0.000333564719. It is small but strictly positive.
The report finds no circular step in the central uniqueness proofs.
The corrected certificate sources support the displays; a grid alone would not support completeness.

## Economics and exposition: assessment and open questions

The abstract states the contribution clearly. It separates direct deterrence from the information response and states the fixed-information control.
The introduction explains why the traded claim and the entrant's acquisition claim react differently to competition.
Proposition 1 supplies the economic basis for that distinction.

The preparation cost receives a concrete institutional account at `sections/02_model.tex:14–20,96–102`.
The unit order and the cost of a position receive an account at lines 139–147.
Liquidity motives appear at lines 149–151. The zero-cost buyer's three proof roles appear in Section 3.2.
These explanations support the model's use.

The following questions concern interpretation. They are not demonstrated errors:

1. **Why this research technology?** `sections/05_research.tex:3–11,45–46` defines a hidden success probability and a hard cap.
   It does not explain the economic source of the cap or the quadratic cost.
   The endpoint result puts research at that cap. State what limits research and why success removes a liquidity arrival.
   This explanation matters more than another numerical example.
2. **What is one public opportunity in data?** `sections/08_empirical.tex:63–72` correctly requires a prespecified opportunity and records zero orders.
   Give one operational example of such an opportunity. Trade data alone do not reveal the absence of an opportunity.
3. **How much economic reach does the benchmark establish?** The exact open set is a useful result.
   Its upper exclusion margin is narrow, and the general construction selects strengths near the first class difference.
   Discuss the economic source of this range. No wider robustness claim follows from openness alone.
4. **Can the literature account be shorter?** The introduction identifies the closest feedback mechanism clearly.
   It then adds several paragraphs of related mechanisms. Keep the distinctions that support novelty and move secondary details to footnotes.

The draft uses affirmative prose and keeps its open cases visible. It contains no repeated “we do not claim” disclaimer.
Some proof paragraphs repeat implementation details; finding 14 gives specific places to cut.

## Parallel-version and layout record

The manuscript reads as a model built around the order slot. It does not tell a replacement story.
The only substantive occurrence of “Laplace” is the permitted order-size remark at `sections/06_robustness.tex:87–94`.
The source scan found no displaced noise-law discussion elsewhere in the manuscript.
The benchmark primitives appear as declarations, with no justification by another model.

The review used the supplied PDF as the reader's artifact. It did not rebuild or replace it.
Selected pages were rendered with `pdftoppm` at 105 dpi into `scripts/R_referee/png/`.
The review inspected physical pages 17, 20–22, 25, 28, 30, 35, 56, 78, 83, 93, 97, and 99–101.

| Pages | Material inspected | Observation |
|---|---|---|
| 17, 56, 83, 93 | Main proposition, rate formulas, private-signal proof, identification statement | Displays and labels are legible. No clipping or overlap appears. |
| 20–21, 28, 35, 78, 97 | Region, outcomes, research, reserves, classes, declarations | Columns align. Values and notes fit. The classes table distinguishes its control row. |
| 22, 25, 30 | Belief, coexistence, and research figures | Panels, ceiling markers, tie branches, and the research gap are visible. No label collision appears. |
| 99–101 | Margins table and continuations | All rows and notes fit. The first page is dense but legible with normal PDF enlargement. |

Page 22 also received a text-coordinate inspection. The final table row ends above the footer, with a clear gap.
The build log contains no overfull box, undefined-reference, or missing-character warning.
No demonstrated layout defect emerged from these selected pages. This was not a visual inspection of every PDF page.

## Files written and unresolved work

The report is `memos/R_referee.md`, relative to the team folder.
Supporting files are confined to `scripts/R_referee/`:

- `recompute.py` and `recompute.log`;
- `source_hashes.sha256`;
- `main.txt` and `page22.xml`;
- the 16 page images in `png/`.

The manuscript repairs in findings 1–14 remain unapplied. The review leaves every other workstream's files unchanged.
The original proofs of Propositions 1–4 remain supported within their stated model and tie rules.
