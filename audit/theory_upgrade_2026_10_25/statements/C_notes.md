# C. Research statements and proofs

Report of the mathematics writer to the coordinator, 25 October 2026.

## Scope and notation

The general setting has prior one half, ranked classes with finite means and values at least the reserve, a continuous incumbent law, positive terminal-value spread and gross-profit gap, and preparation threshold above one half. The zero preparation cost has probability rho; the other preparation cost remains c_H. Research and trading costs are positive, the cap lies strictly between zero and one, and the liquidity share lies strictly between zero and one half. A path strengthens the incumbent in first-order stochastic dominance with all other primitives fixed.

The research value is Psi, the recruiting root is lambda_R(Delta_T), and the floor-entry root is lambda_Q(Delta_T). Research is the minimum of its root and the cap, written out. The floor root is defined on rho Delta_T >= 2k, in [0,1), and equals zero exactly at equality. The path endpoints are r_- and r_+; subdivision endpoints are r' and r''. The low-class sale probability is sigma_L(-1), and its sale rate is s_- = lambda sigma_L(-1). The exact research margin is varphi_a_star; the purchase-only margin is varphi_a; the floor margin is varphi_rho. The cap strength is r_lambda_bar, the end of floor-entry research below the ceiling is r_Q, and the ceiling is r_C.

The default statements allow an indifferent investor to mix over its best orders and require an indifferent high-cost challenger to prepare. Every extension to another tie rule is stated inside its claim. Positive research has a strict full purchase under all four tie rules. Zero research at the sale boundary has one outcome and many hypothetical-success strategy pairs.

## Statements, sources and destinations

All manuscript locations below are relative to `slot/manuscript/`. The source reports are in `audit/theory_upgrade_2026_10_25/referee/`. The displayed numbers follow the independent corollary counter and the placement in Part 6 of the plan. Lemmas A.1 to A.3 keep their numbers. No appendix table is added.

| Statement and label | Number | Source | Manuscript location | Scope and content |
|---|---|---|---|---|
| Joint deviations, `lem:a5-joint` | Lemma A.12 | A5, joint-deviation proof; W3, Shared Candidate 1, section 3 | `appendix/A5_research.tex:64–83` | General setting; all four tie rules; fixed prices and preparation; the unique best research choice is min{cap,Psi/a}. |
| Profile bounds, `lem:a5-bounds` | Lemma A.13 | W3, Shared Candidate 1, section 1; A5 bounds proof | `appendix/A5_research.tex:85–103` | General setting; all four tie rules; nonzero-order posterior bounds for every beta < 1/2; the zero-order bound under every profile additionally uses beta <= 1/3. Equal prices reveal equal posteriors; wrong-signed orders lose. |
| Strict full purchase, `lem:a5-buy` | Lemma A.14 | W3, Shared Candidate 1, section 1 | `appendix/A5_research.tex:105–120` | General setting; all four tie rules; positive research forces a strictly profitable full high-class purchase, and nonpurchase entry is rho. |
| Low-class sale, `lem:a5-sale` | Lemma A.15 | W3, Shared Candidate 1, section 2, equations (1)–(3) | `appendix/A5_research.tex:122–201`, after the purchase lemma at line 120 | General setting; positive research and full high-class purchase; an indifferent investor may mix, either challenger rule; the unique sale rate, three posteriors, exact boundary choices and best sale profit. |
| Competition creates research, `prop:research` | Proposition 4, full statement | W3, Shared Candidate 1, sections 3–6, and Shared Candidate 2; W2, Shared Candidates 1–3; O3 and O4 | `sections/05_research.tex:36–71`; `appendix/A5_research.tex:122–201,266–314` | General setting and default rules; also the full-preparation choice at a challenger tie. (a) Exact existence and complete outcome. (b) Spread comparative statics, weak and strict cases, fixed-value acquisitions, sale-profit kink and cap spread. (c) Exact ownership trade-off, outbidding and decisive advantage. (d) Compact continuous path; a strictly increasing exact margin, endpoint signs and first attainment of the cap; (CR) suffices on a continuously differentiable path. |
| Ownership at the same incumbent, `par:a5-ownership-ratio` | Unnumbered paragraph after the Proposition 4 proof | W2, Shared Candidate 1, The comparison equilibrium; W3, Candidate 3 | `appendix/A5_research.tex:284` | Where recruiting and zero research coexist, rho Delta_T <= 2k; ratio e_H/rho, strictly increasing below the cap and constant at the cap. |
| Three outcomes, `lem:a5-outcomes` | Lemma A.16 | W3, Candidate 3, equations (13)–(14); O8 | `appendix/A5_research.tex:122–201`, the middle-strength lemma | General setting and default rules; zero research, recruiting research and floor-entry research exhaust outcomes. Correct strict and weak threshold endpoints, positive-tuple uniqueness, boundary strategy family, exact coexistence band. |
| Strong incumbents, `lem:a5-strong` | Lemma A.17 | A5 strong-incumbent proof; W3, Candidate 3 and section 1 | `appendix/A5_research.tex:203–231` | General setting; condition (U) and cap posterior different from threshold; all four tie rules; unique full orders and research at the cap. |
| Other tie rules, `rem:researchties` | Remark A.1 | W3, Candidate 3, challenger mixing and investor abstention, equations (15)–(17) | `appendix/A5_research.tex:387–408` | General setting; interior threshold pair and full cap family when the indifferent challenger may prepare with any probability; exact survival condition when the indifferent investor abstains. |
| Price access with research, `par:a5-access` | Unnumbered paragraph in A.5 | `scan/reduction_A3_A5.md`, section 3(f) | `appendix/A5_research.tex:410–421` | General setting, (U), threshold strictly below cap posterior; all four tie rules; both information regimes have full orders and capped research; exact positive proceeds and net-surplus gains. |
| Floor-entry path, `lem:a5-floor` | Lemma A.18 | `statements/O1/O1_proof.tex`, parts (a)–(d); its referee report, sections 1–3 | `appendix/A5_research.tex:286–314`, example part | Exact example primitives and default rules; accepted floor-margin result, floor research below and above the ceiling, cap research, and uniqueness from r_Q onward. |
| Research equilibria in the example, `cor:research` | Corollary 3, full statement | W3, example boundary table; O1, O3, O4 and O8 | `sections/05_research.tex:59–71,119–144`; `appendix/A5_research.tex:233–264,286–314` | Example and default rules. Part (a) classifies the entire path; part (b) gives the six-strength pattern, with strict intermediate research bounds. |
| Research cap and cost, `prop:researchregion` | Proposition A.1 | A5 parameter-region proof, lines 316–385 | `appendix/A5_research.tex:316–385` | Example with a and cap varying, default rules; exact region for Corollary 3(b)'s six-strength pattern with strict margins. Its beta interval is the stated sufficient range. |
| Other tie rules in the example, `rem:researchties-example` | Continuation of Remark A.1 | W3, Candidate 3, equations (15)–(17); O4 computation, parts 3–5 | `appendix/A5_research.tex:387–408` | Example; intermediate threshold entries, entire cap family at r_C, recruiting gap (r_N,r_S] under investor abstention with full challenger preparation, and strictly profitable threshold pair at r = 2. |
| Main-text research statement, `prop:research-short` | Proposition 4 | Full Proposition 4 | `sections/05_research.tex:52–71` | Same general setting, ties, four parts, cap qualification, ownership conditions and endpoint signs. |
| Main-text example statement, `cor:research-short` | Corollary 3 | Full Corollary 3 and O1 | `sections/05_research.tex:59–71,119–144` | Example and default rules; full path summary, six strengths and constant entry after the cap. |

The short-form labels distinguish the two forms in the standalone document. Integration uses one canonical label per result. The unnumbered paragraphs' standalone reference anchors point to their containing result or appendix section. The example continuation shares the remark number. Proposition A.1 here is the former Proposition A.2: the former Proposition A.1 is full Corollary 1 in area A. The preceding lemma sequence occupies A.1–A.11; area C occupies A.12–A.18.

Equation labels are `eq:a5-sale`, `eq:research-exist`, `eq:research-im`, `eq:a5-floor`, `eq:a5-cheap` (CR), and `eq:a5-U` (U). Ordinary equation numbers belong to the integrated appendix counter; the standalone counter is for reading this package.

## Derivations and mathematical choices

1. **Purchase and profile bounds.** Bayes' rule bounds the likelihood ratio of each nonzero order using its positive liquidity mass. A zero order has a different liquidity mass, so its bound under arbitrary strategies needs beta <= 1/3. Positive research needs a positive trading value. If the high-class purchase were nonpositive, a profitable low-class sale would force enough information in a sale to make that purchase positive. Wrong-signed orders lose and abstention earns zero. The strict full-purchase conclusion therefore holds for every beta < 1/2.
2. **Sale rate.** Lemma A.8 at presence lambda and prior one half gives the rate. With a full high-class purchase, a low-class sale has posterior b/(2b+s_-) and entry rho. Its profit falls strictly with s_-. The zero at b(rho Delta_T/k - 2), clipped to [0,lambda], gives the unique rate. In the mixing interval its profit is zero; at a full sale its profit is rho Delta_T m_lambda - k. These cases give its positive-part best payoff. At rho Delta_T = 2k the only positive-research sale rate is zero; at rho Delta_T m_lambda = k it is lambda.
3. **Research and the kink.** The average best success payoff is half the purchase payoff plus half the best sale payoff. Equating it to a lambda gives the exact recruiting equation. Its residual decreases strictly in lambda. At zero it is positive exactly when Delta_T > 2k. Implicit differentiation on either side of rho Delta_T m_lambda = k gives the two slopes; the second exceeds the first. The common research intensity at the kink is (1-rho)k/(2a rho). The cap spread has two cases according to whether the cap lies before that intensity.
4. **Composition and ownership.** A purchase has probability beta + (1/2-beta)lambda. Conditioning on the class gives e_H and e_L directly. Research increases their high-class share, so ranked class values give stochastic improvement of the prepared pool. For a fixed incumbent value, research affects the acquisition probability through e_H. Across incumbent laws the ownership product is e_H W_H/2; the displayed ratio criterion is exact, and outbidding sets W_H to one. Since recruitment at a posterior below one requires g_H > c_H, decisive advantage supplies outbidding on this set.
5. **Outcome exhaustion.** Positive research forces a full purchase. Under the default challenger rule it either recruits fully or does not recruit. The first case has the unique sale rule and recruiting equation. The second forces both trades strictly and gives the floor equation. At the floor root, the recruiting residual is (1-rho) Delta_T m_lambda_Q > 0, so lambda_Q < lambda_R. Clipping both roots gives the coexistence band and eliminates the band when both are capped.
6. **Other ties.** At an interior threshold pair, research optimality is 2a lambda_E = e(1)J-k+(rho J-k)^+. Solving for e(1) gives the stated e_star. At the cap the equality is an inequality, which supplies the entire interval of purchase-entry probabilities. An abstaining investor admits either a zero sale rate or a strictly profitable full sale, exactly as stated in the remark. The research objective itself remains strictly concave.
7. **Access.** Under (U), hidden prices still give strictly profitable full trades and research at the cap. Their costs equal those with price access. The additional purchase-event preparation probability is (1-rho)(b_bar+cap/2). Multiplying it by the conditional terminal-value gain gives proceeds; multiplying it by the conditional allocation gain net of c_H gives gamma(M_cap-tau)+pF(p) for surplus.
8. **Parameter region.** The current cap-and-cost proof concerns the six strengths. Its exact window refers to Corollary 3(b), not to every interval endpoint of Corollary 3(a) for arbitrary costs. The abandoned abstaining-branch result has no separate statement. The general recruiting result includes the profitable-sale term throughout.

## Proof obligations

**O3.** The capped set is the intersection of a closed upper set, defined by the cap research inequality, and a closed lower set, defined by the entry threshold. If nonempty it is an interval ending at the last point where tau <= M_cap. A threshold plateau is included through its right end; a path truncated before the crossing ends at its domain endpoint. The empty-set and singleton alternatives are explicit. In the example the strictly increasing threshold makes the last point r_C. The planned claim holds with these hypotheses.

**O4.** The exact margin is J-k+(rho J-k)^+-2a lambda_E. It is absolutely continuous on the continuously differentiable pre-cap path. Its derivative is the (CR) expression almost everywhere; on the sale-indifference level set J_prime is zero almost everywhere. Continuity, strict increase, a negative initial margin and a positive cap margin give exactly one recruiting start, and O3 gives the last point. The derivative condition suffices for strict increase on a continuously differentiable path. The margin is continuous at the sale boundary, with a derivative jump of rho J_prime when a sure sale becomes profitable. The planned exact-margin claim holds. The purchase-only margin does not determine the start when a sure sale is profitable. At a = 1/5 the exact start is about 2.203523, the sale profit there is about 0.006926, and the purchase-only zero is about 2.279293. Those comparison quantities remain in the proof notes and computation.

**O8.** At zero research all order posteriors and all price beliefs equal the prior; entry is rho and every order has one common price. Correct trades earn rho Delta_T/2-k. At equality their mixtures with abstention give the same outcome, while the unique optimal research choice is zero. The planned outcome classification holds. Unique complete strategy profiles at this boundary would be false. Positive floor-entry research excludes the boundary; Corollary 3 includes zero research at r_N and excludes floor-entry research there.

**O1.** The floor-entry mathematics and notation are in `statements/O1/`. The fragment cites the general floor equation; the piece-end symbols distinguish subdivisions from the full path. Section 6 of its notes describes positive-outcome uniqueness and the zero-research boundary strategy family, consistently with O8. Section 9 identifies this clarification. The referee should read that folder as well as the three proof packages.

## Exact number definitions

For the definitions below, let

\[
\beta=\frac{58931}{200000},\quad
\bar\lambda=\frac{(e-1)\beta}{1+(e-1)\beta},\quad
D(r)=\frac{(r-1)^2}{2r},\quad
T(r)=\frac{12r-3/4}{20r-r^2-1},
\]
\[
L(t)=\frac{\beta(2t-1)}{\beta+(1-2\beta)(1-t)},\quad
J(r)=D(r)[1-T(r)],\quad
c=1+y+\sqrt{y^2+2y},\quad y=(\bar\lambda/20+1/50)(1+e).
\]

These local definitions are for the exact number descriptions; in the manuscript they are Delta_T, tau, lambda_E and r_lambda_bar. Define q as the unique root in (1.747877538267962,2.434045526712002) of

\[
\frac{J(q)}4-\frac1{50}-\frac{L(T(q))}{40}=0.
\]

The derivative bound in O1 proves uniqueness. Thus the two root-dependent entries below have exact definitions, not definitions by rounded decimal.

| Name for the number table | Exact value | Printed value | Computation |
|---|---|---|---|
| `res_J74_frac` | 171/3080 | 171/3080 | J(7/4), for the positive lower bound on the remainder of the path in O4. |
| `res_bound_strength` | 7/4 | 7/4 | Right endpoint of the rational derivative bound in O4. |
| `res_phi_r0_frac` | -1369550353/60351152400 | -1369550353/60351152400 | J(6/5)-1/50-L(T(6/5))/20; J(6/5)=113/18480 and L(T(6/5))=2416171/13716171. |
| `res_phi_rcap` | J(c)-1/50-L(T(c))/20 | 0.017446 | Exact cap endpoint margin; 0.01744574845681505714 < value < 0.01744574845681505715. |
| `res_beta_upper` | 1/3 | 1/3 | Upper endpoint of the stated sufficient beta interval in Proposition A.1. |
| `str_r200` | 2 | 2 | Strength of the threshold pair under investor abstention. |
| `res_I0CM_lambda_r200` | 1355413/6055413 | 0.223835 | L(T(2)), with T(2)=93/140. |
| `res_I0CM_e1_r200` | 292690607/813155460 | 0.359944 | [L(T(2))/20+1/50-(J(2)/4-1/50)]/J(2), where J(2)=47/560 and the sale term equals 11/11200. |
| `res_I0CM_entry_r200` | 40439906511409/140685489814428 | 0.287449 | 1/4+(e_star-1/4)[beta+(1/2-beta)L(T(2))], with e_star the preceding fraction. |
| `res_rQ` (from O1) | q | 2.166995 | The unique zero defined above; 2.166995158219285882282487 < q < 2.166995158219285882282488. |
| `res_lambda_floor_rQ` (from O1) | L(T(q)) | 0.234257 | 0.234257256065633848 < value < 0.234257256065633849. |
| `res_floor_step` (from O1) | 1/10 | 1/10 | Width of each rational piece in the floor-margin bound. |
| `res_floor_dphi_lb` (from O1) | 1/100 | 1/100 | Lower bound for the floor-margin derivative; the smallest exact piece bound is 5993292043494701003/510152171246294601024 > 1/100. |

The first nine definitions belong to this package; the final four are the accepted O1 definitions. The scalar table and its generation remain the coordinator's integration task. Every numerical example value in the statement and proof fragments uses `\reg`. Algebraic coefficients, prior and general-domain hypotheses remain mathematical constants.

The computation also reproduces the existing displays for the cap, recruiting start, cap strength, no-trade bound, entry ceiling, sale bound, condition-(U) threshold, intermediate research and entries, threshold entries, and the price-access gains. All displayed comparisons agree.

## Files and consumer checks

The deliverables are `C.tex`, `C_notes.md`, `O3/O3_proof.tex`, `O3/O3_notes.md`, `O4/O4_proof.tex`, `O4/O4_notes.md`, `O4/o4_margins.py`, `O8/O8_proof.tex` and `O8/O8_notes.md`, all under `audit/theory_upgrade_2026_10_25/statements/`. The floor-equation reference and subdivision notation in `O1/O1_proof.tex` and the printed subdivision symbols in `O1/o1_bounds.py` follow the same conventions.

The computation was invoked through its command-line interface with the exact example primitives and the cost variant a = 1/5. Its output is in the private `wC/o4_output2.txt`. It contains no assertions. Exact fractions and outward rational bounds give the signs, roots, threshold tuples and displayed comparisons. Execution exits successfully. The cost variant uses 120 rational intervals of width 1/50, and the smallest derivative lower bound exceeds 0.030751008.

LaTeX compilation uses the shared preamble and only the private folder `wC/build2/`. The ordinary statement build and all five display builds exit successfully. The ordinary statement build has seven distinct expected missing-number names: `res_rQ`, `res_lambda_floor_rQ`, `res_beta_upper`, `str_r200`, `res_I0CM_lambda_r200`, `res_I0CM_e1_r200` and `res_I0CM_entry_r200`. Private display wrappers supply the thirteen exact-definition displays and stand-ins for external references solely for page inspection. In these builds all references resolve, every number prints, and there are no warnings, overfull or underfull boxes. Their page counts are eight for the statements, four for the floor-entry proof, and two each for the cap, cheap-research and zero-research proofs. Every page was rendered and read; equations, boundary brackets and reference numbers are legible, with no clipping. No build product is in the repository.

## Language judgments

The language scan covers all five LaTeX sources, all five notes documents and both computation sources. The statement and the floor-entry, cap and cheap-research fragments have zero counted hits. The zero-research fragment has two fraction hits, both the literal prior one half required by C-16; they express the fixed prior in the general claim and its Bayes calculation. The tie phrases are allowed mathematical conventions.

The notes' source reports, obligation identifiers, destinations, number definitions and command-line evidence are documentary metadata required for this handoff. Every process match names one of these objects. The computation heading about polynomial identities describes its printed calculation and belongs to the same documentary category. The word “open” in the zero-research notes denotes the excluded endpoints of (r_N,r_Q), a mathematical interval. Exact fractions in the notes specify the requested number definitions. The sources contain no tool, account or personal names. Source comments remain under the coordinator's C-15 instruction and are due for removal at the transplant.

The line-level output and counts are in the private `wC/language2.txt`. Every retained hit is covered by the documentary-metadata, fixed-prior or mathematical-interval judgment above.

## Remaining work for integration

- The referee reads C and the three proof packages, together with the notation pass in `statements/O1/`.
- The coordinator supplies the thirteen number definitions through the existing numbers pipeline and applies the canonical labels and counters in the full manuscript.
- The proof fragments for O3 and O4 belong to Proposition 4(d); O8 belongs to the three-outcome lemma; none introduces another numbered result. Their repeated statement headings are for separate reading.
- The manuscript, figure, slides and comparison note take the same five intervals and boundary choices from Corollary 3. The price-access paragraph carries its own general hypotheses.

No planned mathematical claim fails in its stated scope. The qualifications above are part of the statements: last feasible endpoint on a plateau, exact sale profit in the research margin, endpoint signs for a crossing, and outcome uniqueness at zero research. Integration and the independent referee's reading remain with the coordinator.

## Changes after the referee

The issue identifiers below follow Section 8 of the referee report; that report contains no JSON block. All findings are accepted. C-15 follows the coordinator's instruction to retain the source comments until the transplant.

| Issue | Treatment |
|---|---|
| C-01 | Both main-text ownership comparisons explicitly concern recruiting research. |
| C-02 | Full and short forms use strict increase of the continuous exact margin before the cap. The threshold is below one through the first cap strength. The cheap-research proof establishes the monotone form first and (CR) as a sufficient derivative condition. |
| C-03 | The research-intensity ratio exceeds one and therefore the cap; it is not identified with a strength. |
| C-04 | The margin is continuous at the sale boundary; its derivative has the stated jump at a crossing into profitable selling. The condition permits a recruiting start with a profitable sure sale. |
| C-05 | The cap proof cites Lemma A.5 for path monotonicity. |
| C-06 | Lemma A.10(b) and J(7/4) = 171/3080 give a strictly positive purchase-only margin from 7/4 to r_2, completing whole-path uniqueness. |
| C-07 | The general setting contains the sole labelled floor equation, on rho Delta_T >= 2k, with the root in [0,1) and zero exactly at equality. The outcome lemma and the proof fragments cite it. |
| C-08 | Full-path ends are r_- and r_+; floor-proof subdivisions and their printed computation labels use r' and r''. The arithmetic is unchanged. |
| C-09 | The sale lemma cites Lemma A.8 at presence lambda and prior one half. |
| C-10 | The main-text existence condition names lambda_R as the unique root of its equation and gives research as its minimum with the cap. |
| C-11 | The full statement defines the cap spread in part (b); the short form writes its meaning in words. |
| C-12 | Both ownership statements cite Lemma A.6 for decisive advantage. |
| C-13 | The liquidity-share variation is explicit, and its entry at r_1 uses the formula in beta and the cap. |
| C-14 | The short corollary omits the rounded cap and uses the weak, strong and very strong incumbent phrases. The parameter statement and the cap and floor proof fragments use approximation signs for the rounded cap. |
| C-15 | Source comments remain for removal at the transplant, as directed by the coordinator. |
| C-16 | The zero-research display and its Bayes step use one half for the prior. |

The additional number definition is `res_J74_frac`, exact value and display 171/3080. Every other number definition in this package retains its exact value. The print-only calculation gives the tail bound J(7/4) - k - 2a lambda_E(r_2) = 67628113741/3619682728200, approximately 0.018683436870, strictly positive. This bound is evidence here; the proof prints its sign, so it requires no second number definition.

Both affected computations exit successfully. The floor-root bracket remains [2.166995158219285882282487, 2.166995158219285882282488], and its smallest piece bound remains 5993292043494701003/510152171246294601024. Their output is in the private `wC/o1_output2.txt` and `wC/o4_output2.txt`. The build and language judgments above cover all sixteen findings.
