# Independent check of the Laplace audit

23 October 2026. Stem: XLA.

## Verdict

**Corrected — analytical and computer-assisted.** The substantive conclusions of Propositions 2 and 3 survive this check.
The audit needs corrections about margins, certificate files, proof form, ties, and numerical provenance.
No correction below refutes either proposition at the pinned manuscript.

The manuscript is `overleaf/paper` at `01bd5d6daca14101afb3ef4b0c9e8035ba912181`.
All manuscript references below refer to this commit.
The audited memo is `memos/LA_laplace_audit.md` within the team folder.
The audited proof is `proofs/LA_worked.tex`.

### Six requested items

| Item | Verdict | Result and evidence class |
|---|---|---|
| 1. Audit tables | **Corrected** | The main proof classifications hold. Some hypotheses, open sets, and descriptions need the qualifications in §1. **Analytical.** |
| 2. Proposition 2 margins | **Confirmed**, with a certificate correction | Independent enclosures confirm all four core margins and the return margins. The original CSV loses outward bounds. **Computer-assisted.** |
| 3. Proposition 3 | **Confirmed**, with a scope correction | Three exact equilibria, coexistence, and strict entry order receive certificates. Global equilibrium uniqueness and a continuous branch receive none. **Computer-assisted.** |
| 4. Skipped steps | **Corrected** | The eleven algebraic steps hide no substantive gap. Step 6 uses a conditional expectation, contrary to the audit's explanation. **Analytical.** |
| 5. Worked proof | **Corrected** | The economic proof is sound and non-circular. It compiles. Its literal compliance with BRIEF §5 fails in several places. **Analytical.** |
| 6. Branch note | **Corrected** | The older parent `main` differs from the pinned manuscript. Every pinned table matches the October revision. **Input: local Git records.** |

### Independent evidence

The scripts import no project solver or audited calculation.
They contain no assertions and invoke no test suite.
The interval script uses exact fractions and 65-digit outward interval arithmetic.
It exports bounds through exact binary endpoint fractions, then rounds decimals outward to 42 decimal places.

- `scripts/XLA/independent_intervals.py` produces `independent_intervals.csv` and `independent_intervals_run.log`: 117 quantities.
- `scripts/XLA/provenance.py` produces `provenance_run.log`: committed inputs, table hashes, certificate differences, and local ancestry.
- `scripts/XLA/main_01bd5d6.tex` and `online_appendix_01bd5d6.tex` preserve the two sources read through `git show`.
- `scripts/XLA/compile_run.log` records the proof compilation.
- `scripts/XLA/build/LA_worked.pdf` is the eight-page result. The same folder contains its compiler log and extracted text.

The commands use the project interpreter through the real CLI.
The interval run uses the prescribed CPU slot wrapper.
All files written by this check stay in the two authorized XLA locations.

## 1. Each row of the audit tables

The main text's three propositions receive separate source review.
The review also covers every result row in audit §1a and every condition row in §1b.
The source spans below refer to the two XLA copies of the pinned files.

### Objects, verification, and uniqueness

“Scattered” means the manuscript specifies the components across several displays.
It does not mean that an equilibrium component is absent.
All uniqueness statements below retain the manuscript's truthful-bid convention and null-set qualification.

| Audit row | Verdict | Source and independent assessment |
|---|---|---|
| Proposition 1(a),(b) | **Confirmed** | Main A.1, lines 1749–1842; OA A.2. Indicator integrals give the payoffs. FOSD gives weak comparisons, with the stated strict integral conditions. An equilibrium tuple and uniqueness are inapplicable. |
| Proposition 1(c) | **Confirmed** | Main A.1, lines 1844–1908. The kernel is monotone exactly under the stated restrictions. The two local uniform laws prove necessity. The common mixture preserves its sign. |
| Proposition A.1 | **Confirmed** | Main lines 1913–1935; OA A.1. Integrate the pairwise density inequalities against the product of the two order laws. Bayes and conditional expectation give both posterior bounds. |
| Proposition A.2 | **Confirmed** | Main lines 1941–2004; OA A.3. The entry floor precedes division. The inverse recovers the posterior under every equilibrium profile. The price increment constructs a compatible schedule. |
| Proposition 2(i),(ii) | **Corrected** | Main A.2, lines 2008–2167; OA A.4. Fixed-candidate verification and uniqueness through bounds on every profile are correct. General-class ownership rises only under its separate comparison. The audit's claim column omits this qualification. |
| Proposition 2(iii) | **Confirmed** | Main lines 2168–2187; OA A.5. The spread comparison carries the derivative bound to the stronger incumbent. The posterior ceiling excludes high-cost entry under every profile. Price inversion is unnecessary for that exclusion. |
| Proposition 3 | **Corrected** | Main A.3, lines 2327–2473; OA B.1–B.6. The proof directly checks global deviations against each fixed candidate. An exact root defines the order; its enclosure supplies existence evidence. The audit's word “implicit” must not suggest indirect or circular verification. |
| Proposition A.3 | **Confirmed** | Main lines 2192–2225; OA A.5. The indicator difference proves weak deterrence for a fixed experiment. Strict deterrence needs a positive-probability cost crossing. No equilibrium uniqueness claim occurs. |
| Proposition A.4 | **Confirmed** | Main lines 2230–2323; OA A.5. Pooling existence is exact within the maintained domain. The two uniqueness thresholds are sufficient bounds. The ceiling excludes expensive preparation under every profile. |
| Proposition A.5 | **Corrected** | Main A.4, lines 2478–2693; OA A.6. Every bounded-score density permits the theorem under its stated conditions. The upper cost condition uses the actual supremum `bar_mu_f`, which can be below `M`. The original condition with `M` alone does not suffice for every density. |
| Proposition A.6 | **Confirmed** | Main lines 2752–2803; OA A.6. Cost supports give the floor under every profile. The same translation bound forces orders. The fixed full-order candidate satisfies price and entry conditions. |
| Proposition A.7 | **Confirmed** | Main A.5, lines 2861–3048; OA A.7. Conditional signal laws give the price inverse and residuals. Bounds hold under every signal-contingent mixed profile. The proof then constructs the fixed candidate. |
| Proposition A.8 | **Confirmed** | Main A.6, lines 3052–3098; OA A.8. The stated verifiable-value institution gives the transfer and spread formula. The result concerns the payment stage. It does not solve the induced trading equilibrium. |
| Proposition A.9 | **Confirmed** | Main lines 3100–3209; OA A.9. Both games have full orders under the same global bound. Conditional expected allocation gains prove the welfare result. The separate prior-entry case proves the reverse proceeds sign. |
| Lemma OA.1 | **Corrected** | OA A.6, lines 795–893. The tail result needs median zero. General bounded-score Blackwell dominance covers pure profiles. The logistic decomposition also covers mixed profiles. These scope limits must accompany the audit's short summary. |
| Lemma OA.2 | **Confirmed** | OA A.6, lines 987–998. The weak exclusion uses `K(s) >= ks`. The strong bound subtracts `k + gamma_q s`. The proof covers every profile and constructs the same candidate. |
| OA A.12 | **Confirmed** | OA lines 1571–1717. The stake derivative bound holds for every entry set. Its two sufficient bounds preserve the unique outcomes. At the return economy, constant entry removes the stake effect. Exact stake cutoffs remain open. |
| OA A.13 | **Corrected** | OA lines 1719–1812. There are two analytical claims. The first proves full posterior sufficiency for finitely many classes under Laplace noise. The second needs separation from every feasible posterior mean. Its strong cost condition uses group mean profits. |

The group-separation condition can hold for several classes in each group.
It is not an unrestricted extension to any ordered list of classes.
Classes inside the feasible mean range remain outside the proved trading result.

### Hypotheses, evidence, and open sets

The audit correctly distinguishes an analytical formula from a finite interval certificate.
The thresholds in `numerics/thresholds.py` use `nextafter` around floating-point values.
That operation alone does not certify the exact root.

| Audit condition row | Verdict | Correction or confirmation |
|---|---|---|
| Proposition 1 | **Corrected** | Weak FOSD and support restrictions are structural assumptions. They are not strict inequalities. Part (a) permits every class pair; part (b) needs its ranking and reserve conditions. |
| Proposition A.1 | **Confirmed** | The posterior bound itself needs `b > 0`. The maintained game restricts `b > 1` for the derivative argument. No finite certificate is necessary. |
| Proposition A.2 | **Confirmed** | `Delta_T > 0` and `rho > 0` give inversion. Openness concerns these scalar restrictions within the maintained class assumptions. |
| Proposition 2(i),(ii) | **Corrected** | The listed margins and prior windows are correct. Main Table 2 already prints all four core margins in its notes. The general ownership condition needs separate slack. |
| Proposition 2(iii) | **Confirmed** | The cost, posterior, and strength margins are correct. The stated coordinate intervals are conditional slices through the benchmark, with other coordinates fixed. |
| Proposition 3 | **Confirmed** | Strict endpoint signs, the uniform high-type cover, threshold order, pooling, and entry order receive certificates. The manuscript supplies no parameter box or continuation certificate. See §3. |
| Proposition A.3 | **Corrected** | Weak deterrence requires no strict crossing. Its benchmark strict decline persists locally. A general positive-probability crossing can rely on a cost tie, so strict decline need not define an open region. |
| Proposition A.4 | **Confirmed** | The threshold formulas are analytical; their saved numerical endpoints are floating-point diagnostics. The economic domain must remain explicit. |
| Proposition A.5 | **Corrected** | The logistic benchmark uses the same four margins. General bounded-score noise uses the actual supremum in the upper cost condition. The six-step nonemptiness proof also secures ownership continuity at the chosen threshold. |
| Proposition A.6 | **Confirmed** | The three support margins are positive. Openness refers to scalar coordinates with appropriate cost laws and support restrictions retained. |
| Proposition A.7 | **Confirmed** | All four displayed economic margins are positive. Signal accuracies lie strictly inside `(1/2,1)`. The extra floor column is a diagnostic under zero low cost. |
| Proposition A.8 | **Corrected** | The sign regions `eta < 1/2` and `eta > 1/2` are open relative to the institutional domain. Equality at `eta = 1/2` is a separate boundary result. The allowed endpoint `eta = 0` is not a strict hypothesis. |
| Proposition A.9 | **Confirmed** | The prior exclusion and positive additional-entry event support the two strict gains. The theorem inherits order uniqueness from the earlier bounds. |
| Lemma OA.2 | **Corrected** | The economic cost bounds are strict. The structural condition `gamma_q >= 0` includes a boundary. Openness is relative to that admissible domain. |
| OA A.12 | **Corrected** | The upper stake bounds are strict and correct. `omega = 0` is an allowed endpoint, so the stake region is relatively open at zero. |
| OA A.13 | **Confirmed** | Separation and the two economic windows are strict. No numerical benchmark or explicit open parameter box is supplied for the group extension. |
| Table 4, A/B/D | **Confirmed** | The five economic margins and the ownership margin agree with independent arithmetic. D fails the upper cost condition by `-0.01812165669727...`. |

For the fixed-experiment openness qualification, take a constant signal and choose `c_H = B_F0(pi) > B_F1(pi)`.
The tie rule gives a strict entry decline.
A small increase in the weak incumbent can put both profits below the cost and remove that decline.
Thus strict decline at such a boundary is not itself an open-set claim.

The audit leaves Table 4, case C, outside its numerical check.
Independent exact class integrals now give its six margins:

\[
0.021,\quad
0.058890816750197\ldots,\quad
1/150,\quad
0.001770334089827\ldots,\quad
0.314550686655734\ldots,\quad
1699/2592.
\]

All six are positive and agree with the pinned table's printed values.
This adds evidence for the class example; it changes no audit verdict about D.

## 2. Proposition 2 margins and the audit's certificate file

### Independent margins

The auction objects come from integrals of the second-price payments.
They agree with TEAM_RULES §3 and manuscript equations (4), (9), and (12).
The interval calculation uses `M = e/(1+e)` and `m = 1/(1+e)`.

The decimals in this table are approximate values, not the certificate endpoints.
The full outward endpoints are in `scripts/XLA/independent_intervals.csv`.

| Condition | Benchmark margin | Verdict |
|---|---:|---|
| Weak high-cost exclusion | `287/240 = 1.195833333333...` | **Confirmed** |
| Strong high-cost entry | `0.21715482191670732709...` | **Confirmed** |
| Weak trade exclusion | `1/300` | **Confirmed** |
| Strong trade bound | `0.00241178511416626006...` | **Confirmed** |
| Sufficient ownership comparison | `3/4` | **Confirmed** |
| Return high-cost exclusion | `0.00268890226590511226...` | **Confirmed** |
| Return exclusion, posterior units | `0.00033356471940931785...` | **Confirmed** |
| Return trade bound | `0.01156326403578414959...` | **Confirmed** |
| Spread increase from 3 to 3.6 | `49/180` | **Confirmed** |
| Position above the ceiling | `0.00734148120533816666...` | **Confirmed** |

In particular,

\[
\begin{aligned}
g_H(3.6)&=5879/720,&g_L(3.6)&=5/48,\\
g_H(3.6)-g_L(3.6)&=1451/180,&\tau(3.6)&=4245/5804.
\end{aligned}
\]

Thus the two exclusion margins satisfy the exact identity

\[
c_H-B_{3.6}(M)
=\frac{1451}{180}\,[\tau(3.6)-M].
\]

The independent ceiling is `r_C = 3.59265851879466183334...`.
These values confirm `0.002689`, `0.000334`, and `0.00734` at the requested precision.

The three-part prior interval is

\[
(0.46785002968614851184\ldots,\quad
  0.50042430732006322816\ldots).
\]

The lower endpoint binds strong high-cost entry.
The upper endpoint binds high-cost exclusion at 3.6.
The corresponding high-cost interval is `(5.99731109773409488774..., 6.21715482191670732709...)`.
The bounds remain conditional on the other benchmark coordinates.

**Refuted — analytical:** the return cost margin is not “the thinnest in the paper.”
The strong trade margin is smaller even within Proposition 2 and in the same cost units.
The moderate-value trade margin is `0.00080147313927078251...`.
Margins with different units also require a coordinate or normalization before a meaningful comparison.

### The original CSV does not preserve its interval certificates

**Corrected — computer-assisted.** The internal interval calculations give the correct signs.
The decimal export does not preserve outward enclosures.
In `LA/margins.py`, `rec` formats both endpoints with `mp.nstr(..., 40)`.
That operation rounds to nearest; it does not direct the lower endpoint down and the upper endpoint up.

Of 81 interval rows in `LA/margins.csv`, 68 have identical lower and upper decimal strings.
For example, both endpoints of `m_half` equal `0.2689414213699951207488407581781637256349`.
The true value lies strictly below that decimal, as the independent outward interval shows.
An equal decimal pair therefore fails to enclose it.

The audit also describes its displayed bounds as “rounded inward.”
Such numbers can serve as approximate values, but they cannot serve as interval certificates.
This export fault does not change any checked sign or displayed benchmark digit.
The XLA CSV supplies outward decimal enclosures for all quantities recomputed here.

Main Table 2 prints the four core margins in its notes.
Table 4 supplies a dedicated class-margin panel.
The Online Appendix supplies the extension-margin table.
The manuscript still lacks a consolidated table for all three benchmark economies.
It does not print the benchmark return cost margin.

## 3. Proposition 3: exactly what receives a certificate

**Confirmed — computer-assisted.** The independent script reproduces both endpoint signs at every node.
It also reproduces each high-type lower bound across the full root bracket.
It integrates the two tails exactly and uses the four central antiderivatives.
The unilateral derivative holds the candidate schedule fixed.

These displayed decimals are approximate summaries of the outward endpoints in the CSV.

| Strength | Left root sign | Right root sign | Global high-type lower bound | Pooling margin |
|---|---:|---:|---:|---:|
| 1.55 | `+1.14062414165675e-10` | `-9.62438825949291e-11` | `0.0000761777420772341` | `387/49600` |
| 1.60 | `+1.23657029032498e-10` | `-1.21297872728709e-10` | `0.00275319485548009` | `19/3200` |
| 1.65 | `+1.72594427217698e-10` | `-2.42932975998865e-10` | `0.00549217673164318` | `211/52800` |

The high-type calculation uses the mesh `s = i/200`, including both endpoints.
It subtracts the Lipschitz allowance `L_U/400` from the lowest interval lower endpoint.
Every calculation uses the complete candidate bracket, not its midpoint.
All distinct cut positions have disjoint interval bounds.
The low-type calculation coalesces the deviation center with `-v` algebraically.

The corresponding entry enclosures lie strictly inside the manuscript's printed intervals.
Those three intervals are disjoint and strictly ordered.
The floor margins and the maintained-domain margins are positive at all nodes.

The manuscript certifies:

1. An exact root in each stated bracket.
2. The low type's unique best response against the schedule at that root.
3. The high type's unique best response against every candidate schedule within the bracket.
4. Global exclusion of wrong-signed deviations.
5. Bayes consistency, competitive prices, and optimal preparation through the fixed-candidate construction.
6. Coexistence with no trade at the same strength.
7. Strict order of entry across the three economies.

**Corrected — analytical:** “no uniqueness” needs a scope qualification.
The certificate proves unique best responses against each fixed schedule.
It proves neither uniqueness of the root across schedules nor uniqueness of equilibrium.
Coexistence explicitly defeats the latter claim.
The audit describes this distinction in its detailed method; its short labels must retain it.

**Confirmed — open:** the manuscript gives no certificate for a continuous branch between the nodes.
It gives no explicit open parameter box either.
Strict signs and uniform bounds imply local persistence by continuity within the same Laplace family.
That inference does not supply a quantified region or a branch across the three strengths.
The audit's continuity observation is sound when identified as an inference beyond the manuscript's stated certificate.

The audit misses no stronger certified equilibrium claim.
An exact order can be defined as any root inside the proved bracket.
The absence of a closed-form root does not weaken fixed-candidate verification.

## 4. The eleven skipped computations, plus two evidence items

The audit numbers thirteen items in §2.
Items 1–11 concern compressed mathematical steps.
Item 12 concerns diagnostics; item 13 concerns interval order.

| Audit item | Verdict | Independent reason |
|---|---|---|
| 1. Part (iii), reuse of Steps 4–5 | **Confirmed** | Under every profile, `mu_P <= M` excludes expensive entry. The floor and derivative bound force full orders. Equation (9) constructs prices. |
| 2. Strict decrease of `B_r(M)` | **Confirmed** | Its derivative is `-M/2-C/(2r^2)`, where `C=(1-M)ell^2-p^2`. If `C<0`, `Mr^2+C > ell^2-p^2 > 0`. |
| 3. The larger quadratic root | **Confirmed** | At the benchmark `C>0`, so the roots have opposite signs. In the general domain, a crossing has positive quadratic derivative and is the larger root. OA A.5 retains the domain check. |
| 4. Bounded-score price inversion and residuals | **Confirmed** | Independence and the positive floor give inversion. Positivity and the score bound give the density regularity needed for the translation argument. |
| 5. Null-set transfer | **Confirmed** | Positive conditional flow densities make the equilibrium law equivalent to Lebesgue measure. Every unilateral deviation has a density. Null sets stay null under each deviation. |
| 6. Welfare under A.5 and A.6 | **Corrected** | Equation (A.39) is a realized identity. Equation (A.40) is its conditional expectation. The audit incorrectly calls (A.40) a realized identity. The extension argument itself is valid. |
| 7. Reflection in Lemma OA.1(i) | **Confirmed** | For `f_-(z)=f(-z)`, `f_-'(z)=-f'(-z)`. Positivity, median zero, and the score bound persist. Apply the tail argument to this density. |
| 8. Group residuals in OA A.13 | **Confirmed** | The signed residual is `e(P(x))[t_j-mu(x)·t]`. Separation gives its sign and magnitude `>= rho gamma` under every profile. The derivative bound forces group orders. |
| 9. Integration of density inequalities | **Confirmed** | Integrate `exp(-2/b)f(x-q_L) <= f(x-q_H) <= exp(2/b)f(x-q_L)` against the product law. Each remaining order law has mass one. |
| 10. Common mixture in Proposition 1(c) | **Confirmed** | The spread is linear in the incumbent law. A common component cancels from the difference, which scales by the positive original-law weight. |
| 11. Continuity of `Psi` | **Confirmed** | Residuals converge away from the limiting entry boundary. The density derivative also converges away from its limiting kink. Exponential envelopes permit dominated convergence. |
| 12. Diagnostic curves | **Confirmed** | The manuscript identifies the uncertified continuations, mixed candidate, and additional noise-law exercises as diagnostics. Proposition 3 does not certify those curves. |
| 13. Strict entry order | **Confirmed** | The independent outward intervals at the three root brackets fit inside the printed, disjoint intervals. |

The correction to item 6 matters economically.
For example, take the additional high-cost decision in the low class at `r=3` and `R=2`.
Preparation can occur after favorable flow, but the low challenger loses the auction and creates no allocation gain.
Its realized net gain is `-6`.
Positive expected welfare follows from the posterior-weighted decision, not from a positive realized gain in every state.

### Other compressed steps

The audit omits several short computations from its list.
Each has a valid expansion.

- **The sharper full-order bound, main (A.7); OA (OA.22).** Put `H(s)=(1-s/b)exp(-(1-s)/b)`. Then `H'(s)=-s exp(-(1-s)/b)/b^2 <= 0`. Its minimum is `1-1/b`.
- **The ownership sufficient condition, main Step 6.** Since `x*<1`, `alpha_H>1/2`. Thus `e_H>(1+rho)/2`. Combine this strict bound with the stated weak sufficient comparison and positive `W_H(F_0)`.
- **The many-class price argument, OA A.13.** The two incentive inequalities order supports across classes with different proceeds. The covariance formula then has nonnegative products. Equality forces a common likelihood ratio on the supports. The manuscript supplies the equal-proceeds and Borel-inverse details.
- **Wrong-signed orders under a stake, OA A.12.** Their trade derivative toward zero has magnitude at least `(1-1/b)rho kappa Delta_T+k`. The stake perturbation is below the smaller correct-sign margin. Thus no wrong-signed order can improve on zero.
- **Nonempty regions, main A.4.** The bounded-score construction first chooses a continuity point of the posterior law. This secures ownership continuity despite possible posterior atoms. The six explicit steps preserve both strict economic windows.

These additions reveal no substantive gap in the checked numbered results.
The stronger claim that every proof follows the literal five-part presentation standard still requires the corrections below.

## 5. The worked proof

### Mathematical validity

**Confirmed — analytical.** The stated tuple supports full orders and entry `rho` under H1–H6.
The posterior, price atoms, inverse belief, entry policy, and truthful-bid rule are correct.
Bayes consistency and competitive prices follow directly from the fixed tuple.
The translation lemma proves the derivative bound without a derivative of the entry rule.
The uniqueness argument begins from an arbitrary mixed profile.
Its exclusion step precedes price inversion and uses no conclusion of the theorem.

The proof establishes part (iii), conditional on the auction objects and maintained truthful implementation.
Its account of the rise at the first two economies cites Proposition 2(i),(ii).
That reference is a dependency, not a circular proof of part (iii).
Null-set qualifications match the pinned manuscript's uniqueness scope.

### BRIEF §5 compliance

| Requirement | Verdict | Evidence and correction |
|---|---|---|
| Explicit tuple | **Confirmed** | Section 1 specifies orders, all-flow prices and posteriors, beliefs on the price image, entry, and bids. Every deviation stays in that image. |
| Listed conditions | **Confirmed** | C1–C5 cover Bayes, price competition, entry, orders, and truthful bids. |
| Direct fixed-object computation | **Corrected** | The main computations are valid. At source line 225, the low-class wrong-sign argument uses “symmetrically” without its computation. The standard expressly excludes that shortcut. |
| Uniqueness through every-profile bounds | **Confirmed** | Steps 1–4 apply to arbitrary mixed profiles. Equivalent flow laws transfer null-set identities to all deviations. |
| Strict hypotheses, margins, open set | **Corrected** | H1 contains weak dominance and support equalities. H2 states continuity. These are structural conditions, not strict inequalities. Several strict scalar restrictions lack their own table rows. |

The omitted wrong-sign computation is

\[
\Pi_L(+s)
=-s\int_{\mathbb R} f(x-s)A_L(x)\,dx-ks<0
=\Pi_L(0),\qquad s>0.
\]

The proof should separate structural assumptions from strict economic restrictions.
Its scalar table also needs `k>0`, `c_H>0`, `pi>0`, and `1-pi>0`.
At the benchmark these margins are `1/50`, `6`, `1/2`, and `1/2`.
The text should identify the coordinate topology for its open set.
The displayed coordinate intervals already give the correct benchmark slices.

If the package also invokes (A1)–(A2) to present the full reversal, it needs their four margins in the same proof package.
The audit CSV records those margins, but the worked proof's table does not display them.
Its rounded claim `B_1.2(1/2)=4.804` should use an approximation sign or `1153/240`.

The proof needs no investor selection rule for these strict best responses.
For a literal statement of both tie conventions, it can permit any mixture over investor maximizers.
The challenger prepares at indifference.
At `r=3.6`, both challenger cost decisions are strict, so neither convention affects the outcome.

The source labels the theorem analytical and the margins computer-assisted.
Those labels are appropriate.
The exported CSV fault in §2 weakens the cited numerical record, not the theorem's algebra.
The worked proof's own displayed interval bounds for the three return margins enclose the independent values.

### Compilation

**Confirmed — input: compiler output.** The prescribed `latexmk` command compiles the unedited source successfully.
The output contains eight pages, with no fatal error.
The output directory is under `scripts/XLA/build/` to preserve the audited files.

The compiler reports two overfull boxes, of about `0.506` points and `67.761` points.
The larger box belongs to the margins table at source lines 317–334.
The log also reports bookmark warnings for mathematical text.
Compilation succeeds; the table layout needs repair before publication.

## 6. What the branch note means for the pinned manuscript

**Confirmed — input: local Git records.** Two separate repositories must remain distinct.

| Object | Commit or reference | Relevant state |
|---|---|---|
| Pinned manuscript repository | `overleaf/paper`, `01bd5d6daca14101afb3ef4b0c9e8035ba912181` | The model declares zero low cost. The benchmark, proofs, and tables refer to that model. |
| Parent numerical revision | `revision/alex-2026-10-21`, `f367a0ef9d6b67ed1c010b72b21b0d55a9725a49` | The October manifests declare zero low cost. All ten pinned table files match this revision byte for byte. |
| Parent local main | `1eb6d2cfd70fdfca98bbf4557d666bd04417e1df` | September numerical records use low costs 1, 0.3, and 1 for benchmark, moderate values, and signals. |

At the accepted Laplace atomic-cost feedback row for `r=3`, the two numerical layers give:

| Quantity | Parent main | October revision |
|---|---:|---:|
| Entry | `0.5227572972597381` | `0.5227572972597381` |
| High-class ownership | `0.3241924257758909` | `0.3241924257758909` |
| Target proceeds | `0.8723920450946406` | `0.8723920450946406` |
| Net surplus | `2.382300868169776` | `2.632300868169776` |
| Expected preparation cost | `1.8865437835584278` | `1.6365437835584278` |

The exact cost difference is `rho c_L = 1/4`.
The independent zero-cost calculation gives surplus `2.63230086816977413154...`.
It agrees with the pinned manuscript's `2.632301`.
The positive floor margins explain why zero low cost and cost 1 give the same benchmark orders, prices, and entry.

The certificate CSVs differ only in `threshold_margin_lower` at the three certified nodes.
Each increases by exactly 1 in the October revision.
This column records the low-cost floor; its name does not identify `M_v-tau`.
The root signs, high-type bounds, entry intervals, and pooling margins are unchanged.
The independent calculations in §3 verify them directly under zero low cost.

**Corrected — input: local Git records.** The audit's timestamp range omits a later registry run.
`c8_registry.json` records `2026-10-21T20:51:41.083534+00:00`, after the stated 19:48 endpoint.
Every listed October exercise manifest records `passed: true`.
These flags describe saved records; this check does not rerun the research producers or the full release gate.

Local ancestry shows that the numerical revision is absent from parent `main` and cached `origin/main`.
No cached remote-tracking branch contains its head.
This establishes the local branch separation.
It does not establish the current server state without a remote query.
The audit's unqualified word “unpushed” exceeds this local evidence.

**Refuted — analytical:** the pinned manuscript's benchmark numbers do not reproduce “only on a branch.”
They also follow from its stated primitives and the independent arithmetic here.
The October branch identifies the saved numerical pipeline that matches its tables.
The older parent layer cannot substitute for the pinned manuscript in the comparison.

The pinned repository contains the manuscript, appendix, figures, and LaTeX tables.
It does not contain the parent `numerics/` directory.
Its `source-provenance.json` retains migration metadata dated 30 September.
That metadata does not certify the later manuscript or its revised table hashes.

The evidence therefore supports a package-provenance issue.
It supplies no contradiction in the pinned Proposition 2 margins or Proposition 3 certificates.
The comparison note should assess the pinned proof and identify the matching numerical revision separately.

## 7. Tie rules and final corrections for the comparison

**Corrected — analytical.** The audit's statement that the challenger tie rule “never binds” at benchmark Proposition 2 is too broad.
At `r=3`, the high-cost challenger is indifferent at the interior flow cutoff `x*`.
That event has zero flow probability, so the tie rule does not change expected entry or the investor's incentives there.
At the ceiling, equality holds on a tail with positive probability and the rule affects entry.

The audit also gives `g_L=0` as a reason for zero-cost indifference in the general class model.
The relevant object is the complete posterior profit `B(mu)`.
With positive feasible posterior weights, `g_L=0<g_H` still gives `B(mu)>0`.
Zero-cost indifference requires `B(mu)=0`; a low-class atom at the reserve alone does not establish it.

The following claims need correction before the comparison uses the audit:

1. Retain the general-class ownership condition in the Proposition 2 summary.
2. Retain the actual posterior supremum in the general bounded-score result.
3. Credit Table 2's four printed margins.
4. Describe the return margin as narrow, without the false superlative.
5. Use outward certificate endpoints, or label rounded decimals as approximations.
6. Describe Proposition 3 as direct fixed-candidate verification, with unique conditional best responses.
7. Distinguish conditional expected welfare from realized welfare.
8. Describe the worked proof as sound, with the listed failures of literal proof-standard compliance.
9. Keep the pinned manuscript separate from the parent numerical `main`.
10. Qualify statements about remote publication by the local evidence available.

**Open:** the first informative equilibrium, equilibrium completeness between certified nodes, a certified continuous branch, and exact stake cutoffs remain outside these proofs.
No audited file changes in this workstream.
