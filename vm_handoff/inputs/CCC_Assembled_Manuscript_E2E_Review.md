# Competition Creates Competition — End-to-End Review of the Assembled Manuscript

**For Austin Li**  
**Reviewed versions:** `main_filled.pdf` and `online_appendix_filled.pdf`  
**Review date:** 5 September 2026

## Executive judgment

**Keep the paper, its title, and its principal result. Revise this assembled version before submission, but do not restart the model.** The core equilibrium argument survives this review. The acquisition-payoff opposition is correct; the price-sufficiency argument accounts for the buyer's actual information; the global trading argument covers continuous deviations and mixed candidate strategies; and the complementary-information extension uses the appropriate state-dependent entry probabilities.

The principal revisions are about the economic presentation, the treatment of seller continuations, and the evidence supporting the newly assembled numerical layer. The manuscript already has enough substantive theory to organize an ambitious upgrade paper. Whether it ultimately supports a major journal contribution will depend much more on the institutional result developed next than on adding further decimal places or distributional variants.

**The most important additional finding is analytical:** after a reserve removes the positive preparation floor, the same investor orders can support different equilibrium price rules, not just different trading equilibria. Below, we construct a continuum of such equilibria at a single reserve. This does not invalidate the main theorem, whose positive floor rules out precisely this issue. It does mean that the reserve solver must search a *pricing-and-trading* correspondence, rather than silently assign one pricing rule to each order profile.

The reserve table is appropriately labeled exploratory. Its best-found values are not false claims of global optimality. However, exact participation-event reserves improve on both reported best-found revenues, and the numerical contract should include those events explicitly. This is a repair to the numerical design, not a reason to discard the benchmark.

### Priority decisions

| Priority | Finding | Required response |
|---|---|---|
| Before submission | The institution and complementary-information interpretation arrive too late relative to the technical detail. | Add a compact institutional subsection and introduce complementary information in the introduction; retain the simpler benchmark for the proof. |
| Before treating the reserve sweep as a cleared computation | Pricing multiplicity can occur at fixed orders when the entry floor disappears. | Add the exact pricing-pool regression test below; retain pricing regimes separately when deduplicating continuations. |
| Before numerical sign-off | The PDFs specify the new computational layer, but its source, complete outputs, and run manifests are not included in this review's new attachments. | Audit the actual assembled repository. The earlier verification seed is not a substitute for its new searches. |
| Before submission | Some important model restrictions are explicit only online. | State risk neutrality, the traded-asset set, bidder trading restrictions, and the binding-sale implementation in the main model. |
| Before submission | The displayed matched-dividend control does not show the quantity it matches. | Add mean financial price and dividend, or remove the redundant rows and explain the control in prose. |
| Next research stage | Seller choice remains open and is now demonstrably a joint price/trading selection problem. | Develop this as the next theorem; do not equate best-found revenue with the seller's equilibrium objective. |

## Reading and verification record

I read the complete main document, including its paper appendix, and the complete online appendix. I also rendered and visually scanned all pages, inspecting the figures, tables, and key mathematical displays at higher resolution. Locations below refer to the printed page numbers, which coincide with PDF page numbers in these files.

I independently reconstructed the reported payoff and probability calculations from the equations in these PDFs. The executed checks include:

- Nineteen parameter/profile calculations covering the baseline, controls, distributional variants, moderate values, and stated reserve alternatives. Some are intentionally repeated comparison nodes, not nineteen distinct calibrations.
- Direct integration of realized auction payments and buyer profits, independently of the reduced-form payoff formulas, at those nodes.
- The entry and ownership outcomes for all twenty-five accuracy pairs in the complementary-signal table, at both incumbent strengths.
- Separate analytical candidate checks supporting the displayed signal-grid outcomes, including the rows outside the sufficient region for the entry-reversal theorem.
- Continuous-order diagnostic meshes at the three asymmetric nodes.
- A rerun of all three interval certificates using the previously supplied seed implementation, together with a check that the bounds printed in the assembled paper are rounded outward.
- A new analytical pricing-multiplicity test for the reserve continuation and direct numerical evaluation of its equilibrium outcomes.

These checks are not a rerun of the newly assembled repository. In particular, I have not independently reproduced its complete Figure 2 continuation search, all finite-support mixed searches, the reserve coverage counts, or its full source-to-PDF build. The attached verification files identify exactly what was executed here.

**Source convention in this report:** “M” denotes the main PDF; “OA” denotes the online appendix. External literature checks are identified separately. New deductions below are not attributed to the manuscript.

---

## 1. The argument worth putting at the center of the paper

The paper's economic contribution is the distinction between **buying the company** and **trading a claim to what its shareholders receive**.

A high-value challenger may keep most of its advantage when the incumbent is weak. Information about that advantage then matters greatly to the challenger but little to target-share payments. A stronger incumbent can transfer more of the advantage into target proceeds. The same change that reduces acquisition profits can therefore increase the investor's incentive to reveal information through trading.

The identities in Proposition 1 make that distinction particularly clean:

$$
\Delta_T(F)=\mathbb E_F[(R-\ell)_+],
\qquad
G_\theta(F)=\mathbb E_F[(\theta-\max\{p,R\})_+].
$$

The first integrand increases with incumbent value; the second decreases. What the paper subsequently adds is an equilibrium argument showing that the change in information can reverse the participation comparison even after market makers price the entry response and the investor optimizes globally.

**That is the headline.** The no-trade regime, capped orders, asymmetric certificates, and upper participation ceiling explain how the mechanism operates in the model. They should not displace it with a presentation organized around a particular graph shape.

The present introduction is accurate but overloaded with the taxonomy of results. It discusses uniqueness, mixed orders, continuous deviations, three-economy nonmonotonicity, interval certification, correspondence limits, distributional robustness, private signals, welfare, bargaining, and reserve comparisons before the reader has a fully developed institutional picture. The exposition would be stronger if it spent slightly more space explaining *why these two claims have different information incentives* and slightly less previewing the verification apparatus.

**Recommendation:** preserve the payoff opposition and the unique-outcome reversal as the main contribution. Give complementary private information the next most prominent place. Present correspondence and welfare as implications, and the seller problem as the next institutional theorem.

## 2. Mathematical audit

### 2.1 Result-by-result assessment

| Result | Assessment | Reason / precise boundary |
|---|---|---|
| Proposition 1: FOSD opposition | Correct under the stated acquisition institution. | The pointwise payment difference and layer-cake profit identity are valid. Distributional generality is not auction-format generality. |
| Posterior bounds | Correct. | The likelihood-ratio bounds survive arbitrary state-contingent mixtures; conditioning on price preserves the interval. |
| Price sufficiency with a positive entry floor | Correct and central. | The pricing equation explicitly recovers the flow posterior from the observed price. No hidden observation of order flow is supplied to the challenger. |
| Main residual-profit identities | Correct. | The anticipated level and entry response are priced before computing the investor's remaining state advantage. |
| Proposition 2, weak and strong outcomes | Correct under the stated inequalities. | The argument excludes all nonzero weak-economy orders and proves a positive marginal-profit lower bound throughout the strong-economy order interval. |
| Proposition 2, very strong incumbent | Correct as a conditional finite comparison. | The extra hypotheses exclude expensive preparation while preserving full trading. This is not a global single-peakedness theorem. |
| Pooling and full-order thresholds | Correct on the maintained floor/prior domain. | Existence, sufficient uniqueness, and participation feasibility are kept distinct. |
| Proposition 3 | Supported by the analytical argument and reproduced seed certificates. | Exact root existence is combined with global low-type concavity and a uniform high-type derivative cover. It is not an exhaustive correspondence result. |
| Logistic noise and atomless preparation costs | Correct under the support and slope conditions. | The regularity and participation-floor arguments survive; the upper-tail mass changes materially. |
| Complementary private signals | Correct under its separate sufficient conditions. | State-conditioned entry is recomputed and the buyer conditions jointly on price and its private signal. |
| Bargaining result | Correct for the stated verifiable-value fallback institution. | It is an acquisition-stage result, not a solved bargaining/trading/entry equilibrium. |
| Matched welfare result | Correct for access to prices at fixed incumbent strength. | Added entry has nonnegative conditional private surplus and a positive additional allocation term; trading costs coincide. |
| Seller objective and local decomposition | Correct as a selected-continuation objective and conditional local identities. | Selection, global existence, global maximization, and the full price correspondence remain to be established. |

### 2.2 The main proof does not contain the usual feedback shortcut

A common error in this class of models is to compute trading profits as though entry were unanticipated, or to allow a trader's deviation to change public beliefs as though a new equilibrium had been selected. The manuscript does neither.

In M equations (10)–(11), pricing already includes the actual entry policy. In a unilateral deviation, the policy is fixed and the shifted noise density changes the distribution of order flow reaching it. The convolution argument in M Appendix A.3 and OA A.3 makes that distinction explicit. The absolute-continuity/Fubini justification is sufficient even when entry jumps.

The online argument also establishes equivalence of the equilibrium flow law to Lebesgue measure. Consequently, a different version of a pricing function on a flow-null set cannot become a profitable deviation. This closes a genuine technical issue rather than merely asserting that full-support noise “takes care of off-path beliefs.”

I therefore do not recommend changing the benchmark mechanism or withdrawing its outcome-uniqueness claim. The appropriate formulation is **unique trading and on-path entry outcomes under truthful auction implementation**, not uniqueness of every strategy description or of prices at unrealized arguments.

### 2.3 The complementary-signal result deserves a more accessible paper-appendix proof

The full proof in OA A.7 is sound. The important independence statements are

$$
\Theta\perp X\mid T,
\qquad
Y\perp X\mid\Theta.
$$

They justify both the investor's conditional valuation and the buyer's joint posterior. The difference between the two state-conditioned entry rates is then built into

$$
D=e_H(t_H-t_0)-e_L(t_L-t_0),
$$

rather than incorrectly carrying over a common entry rate from the benchmark.

M Appendix A contains the needed formulas, but the proposition precedes several definitions and its proof is dispersed between pp. 37 and 41–43. A referee can reconstruct the logic, but unnecessarily has to assemble it.

**Fix:** put a compact four-step proof immediately after the definitions: joint beliefs; state-conditioned entry and price inversion; residual bounds; weak/strong global optimality and positive additional entry. The detailed conditional laws can remain online. This is a placement improvement, not a missing-proof allegation.

### 2.4 Two small mathematical wording repairs

**M p. 38, Proposition A.9 discussion:** “every additional entrant contributes at least” the reserve term should say **“every additional entrant contributes at least that term in conditional expectation, given the price and preparation cost.”** A realized low-value entrant may incur preparation costs without creating enough realized allocation value to cover them. The proof and subsequent equations correctly use conditional expected surplus; make the sentence equally precise.

**M p. 35, Proposition A.3:** independence of preparation costs is maintained by the model. If the statement is meant to generalize to an arbitrary fixed joint distribution of signal, quality, and cost, the buyer's posterior should be written conditional on its complete information, including its observed cost. Either retain the maintained independence explicitly or use $\Pr(H\mid S,C)$. The pointwise deterrence proof then works unchanged. This is a clarification of the generalized statement, not a counterexample to the benchmark.

---

## 3. An additional issue for seller design: the same orders can support different price equilibria

### 3.1 Why this matters

OA C.6 correctly recognizes that flows with no preparation can pool at the no-entry price and that the buyer must condition on the whole price pool. It gives a convenient candidate construction that activates entry exactly where the raw flow posterior justifies it.

That construction is not the whole pricing correspondence. A larger pool can also be consistent: some flows whose *raw* posterior would justify entry may be pooled with sufficiently unfavorable flows, so that the posterior at the common observed price does not justify entry.

The distinction matters even if the investor's orders are identical. Searching more order profiles cannot, by itself, recover alternative price pools at a fixed profile.

This phenomenon is not being claimed as generally new to feedback theory. Dow, Goldstein, and Guembel's discussion of their Lemma 1 already distinguishes continuation equilibria with different pooling regions. Here we derive an explicit example in this manuscript's own reserve game, suitable for a numerical acceptance test.

### 3.2 Proposition R — A continuum of pricing continuations at fixed full orders (analytical)

Keep the manuscript's benchmark primitives, choose $r=1.2$, and change the reserve to $p=7$. Because $p>r$ and $p>\ell$, the auction payoffs are

$$
t_0=t_L=g_L=0,
\qquad t_H=7,
\qquad g_H=3.
$$

Maintain full orders $(q_H,q_L)=(1,-1)$ and the Laplace scale $b=2$. Write

$$
\mu(x)=\operatorname{logistic}\!\left(\frac{|x+1|-|x-1|}{2}\right).
$$

For **every** cutoff

$$
c\in[-\log 2,0],
$$

there is a continuation equilibrium with price

$$
P_c(x)=
\begin{cases}
0,&x<c,\\
\dfrac{7}{4}\mu(x),&x\ge c,
\end{cases}
$$

no preparation at the zero price, low-cost preparation at every positive price, and no high-cost preparation. The investor's orders are the same in all these equilibria, but prices and entry differ.

#### Proof: acquisition and preparation

At a positive price, the buyer recovers the raw posterior. Its gross acquisition profit is $3\mu$. The lowest raw posterior in the positive-price region is at least

$$
\mu(-\log 2)=\frac13.
$$

Thus the low cost $c_L=1$ is covered; high-cost preparation at $c_H=6$ is impossible.

Let $F_Z(z)=\Pr(Z\le z)$ denote the noise **CDF** in the following calculation. At the zero price, the buyer's posterior is

$$
\bar\mu_c
=
\frac{F_Z(c-1)}{F_Z(c-1)+F_Z(c+1)}.
$$

The monotone likelihood ratio makes this lower-tail posterior nondecreasing in $c$. For every $c\le0$,

$$
\bar\mu_c\le\bar\mu_0=\frac12e^{-1/2}<\frac13.
$$

Therefore even low-cost preparation is strictly unprofitable at the zero price. In particular, the buyer is not mistakenly using the raw posterior within the price pool.

#### Proof: competitive pricing

On the zero-price region there is no entrant and neither bidder meets the reserve, so the terminal stock payoff is zero. On the positive-price region the low-cost challenger enters with probability $\rho=1/4$, and only a high-value challenger buys, paying $7$. Thus its conditional expectation is $(7/4)\mu(x)$, exactly the displayed price.

The positive-price map is strictly increasing in the nonconstant posterior, with the usual correctly conditioned upper price atom. There is no collision with the zero-price pool.

#### Proof: every investor deviation

Against this candidate price and entry policy, residuals are

$$
A_H(x)=\rho p\,[1-\mu(x)]\mathbf 1\{x\ge c\},
\qquad
A_L(x)=\rho p\,\mu(x)\mathbf 1\{x\ge c\}.
$$

Both are nonnegative. Under full orders,

$$
F_H(1)=F_L(1)=J_c.
$$

For any correctly signed magnitude $s\in[0,1]$, the Laplace likelihood-ratio bound gives

$$
F_\theta(s)\ge e^{-(1-s)/b}J_c.
$$

Together with $|F_\theta'|\le F_\theta/b$, and the fact that $(1-s/b)e^{-(1-s)/b}$ is decreasing on this interval,

$$
U_\theta'(s)\ge(1-1/b)J_c-k.
$$

Since $c\le0$, the whole tail $x\ge1$ is included in the positive-entry region. On this tail, $1-\mu=m=(1+e)^{-1}>1/4$, and its high-state probability is $1/2$. Hence

$$
J_c\ge\frac{\rho p m}{2}>\frac{7}{32}.
$$

Using $b=2$ and $k=1/50$,

$$
U_\theta'(s)>
\frac{7}{64}-\frac1{50}
=
\frac{143}{1600}>0.
$$

Thus the maximum correctly signed order is the unique best response against each candidate schedule over the whole order interval. Wrong-signed orders are inferior to zero. This proves equilibrium existence for every cutoff in the specified interval. No numerical root or equilibrium selection is used in the proof.

### 3.3 Executed values for two members of the family

| Pool cutoff | Investor orders | Posterior at zero price | Total preparation probability | Expected seller revenue |
|---|---|---:|---:|---:|
| $-\log 2$ | $(1,-1)$ | 0.2729788130 | 0.1518051214 | 0.6873641502 |
| $0$ | $(1,-1)$ | 0.3032653299 | 0.1250000000 | 0.6096428364 |

These are ordinary numerical evaluations of analytically established equilibria. The exact global deviation bound above supplies the proof; the decimal values are not interval certificates.

The less informative price rule suppresses preparation at some flows that would justify it if those flows were separately observed. The zero price remains rational because buyers condition on the whole pooled region.

### 3.4 Required change to the numerical contract

The PDFs do not establish whether the new implementation retains this family. OA C.6 discusses price pools but does not explicitly parameterize and search alternative pooling cutoffs at a fixed order profile.

Add this example as an acceptance test. The numerical continuation record should distinguish at least:

- The order profile or support distribution.
- The price-pooling region and its total probability.
- The correctly pooled posterior and preparation decision.
- The positive-price information map.
- The investor's global best-response bounds against that complete schedule.

Do not deduplicate two equilibria solely because their orders or order supports agree. Likewise, **fixed orders imply a fixed price experiment only where the price-sufficiency result applies**. The paper's benchmark controls satisfy that condition; an unrestricted reserve sweep need not.

This addition sharpens the seller-choice program. It does not require solving the entire pricing correspondence before presenting the fixed-reserve upgrade result.

---

## 4. Numerical audit: what reproduces and what is still unreviewed

### 4.1 Central quantitative results reproduce

Selected independent calculations are:

| Object | Independently recomputed value |
|---|---:|
| Benchmark strong entry | 0.5227572973 |
| Benchmark strong high-value ownership | 0.3241924258 |
| Benchmark strong target proceeds | 0.8723920451 |
| Frozen informative-profile entry at weak strength | 0.5621780582 |
| Price-hidden target proceeds at strong strength | 0.6145833333 |
| Fixed-strength acquisition-surplus gain | 0.0802175348 |
| Logistic strong entry | 0.3015088516 |
| Atomless-cost Laplace strong entry | 0.5227147164 |
| Atomless-cost logistic strong entry | 0.3013741277 |
| Moderate-value strong entry | 0.5268046622 |
| Complementary-signal strong entry | 0.8794375516 |

The direct realized-payoff integrations and reduced-form auction calculations differed by at most approximately $1.8\times10^{-15}$ in these checks. This is a floating-point diagnostic, not a rigorous upper bound on all implementation errors.

The numerical checks support the values printed in Tables 1–3 and the stated alternatives in Table 4, to their displayed precision. I did not find evidence of a switched parameter vector, an incorrect welfare subtraction, or an information-removed control being mistaken for the frozen-profile control.

### 4.2 The complementary-signal grid is useful evidence, including its reversals of sign

I reproduced the reported entry and ownership values for all twenty-five accuracy pairs in OA Table 1. Its negative comparisons when the buyer's private signal is sufficiently accurate are economically informative: at those parameters, expensive preparation is already worthwhile after favorable private information in the weak economy.

For the reported weak pooling candidates, let $D_0$ be the conditional-payoff coefficient evaluated at the public prior, incorporating private-signal-dependent entry. The exact correctly signed deviation payoff is

$$
s\{(a-1/2)D_0-k\}.
$$

It is negative at every reported weak-grid candidate. At every reported strong-grid candidate, the low-cost floor and the global full-order marginal-profit bound are positive. Thus these displayed candidates have analytical support beyond simply matching a probability formula.

This does **not** make every pair an entry-reversal theorem or establish weak-economy uniqueness at every pair. The table is right to distinguish failure of a sufficient comparison condition from rejection of a candidate equilibrium. Preserve all rows; do not omit the negative comparisons to make the extension appear uniformly positive.

### 4.3 The asymmetric certificates reproduce, including the printed bounds

The seed certificate rerun reproduced the three root brackets and global high-type derivative bounds. I additionally compared the unrounded interval endpoints with the displayed paper bounds. The printed entry intervals enclose the rerun intervals, the high-type lower bounds round downward, the positive left-root bounds round downward, and the negative right-root bounds round upward.

The certificate method is therefore doing real work. It is not a finite deviation grid relabeled as proof. Keep the distinction between:

- Exact equilibrium existence within a certified bracket.
- Numerical continuation between brackets.
- The absence of other equilibria, which has not been proved.

The attached rerun concerns the supplied seed implementation. The new repository's port still requires its own source and output comparison before it is independently cleared.

### 4.4 Add exact reserve events instead of relying only on a finer mesh

Table 4 Panel C reports the highest found reserves $6.280$ and $1.324$. These sit immediately below analytically identifiable participation events.

**Weak-incumbent high-reserve region.** When the reserve exceeds incumbent support and excludes the low class, $g_H=h-p$, $g_L=0$. The low-cost participation floor reaches equality at

$$
p_L=h-\frac{c_L}{m}
=6.2817181715\ldots.
$$

Under the manuscript's entry-at-indifference convention, the floor remains active at equality. The full-order argument remains valid there, and revenue is

$$
\mathcal R_T=\frac{\rho p_L}{2}
=0.7852147714\ldots,
$$

above the table's sampled revenue $0.785000$.

**Strong-incumbent region with the low class excluded.** Under full orders, expensive entry reaches its upper posterior plateau when

$$
M\left(h-\frac r2-\frac{p^2}{2r}\right)=c_H.
$$

For $r=3$, the corresponding reserve is

$$
p_H=\sqrt{2r(h-c_H/M)-r^2}
=1.3252698283\ldots.
$$

At this exact event, the tie convention admits expensive preparation on the upper plateau. Direct evaluation gives entry $0.5064773952\ldots$ and revenue $1.0688544444\ldots$, exceeding the reported sampled value $1.068602$. The low-cost floor and full-order marginal bound are strictly positive there.

These observations do not establish global optimality. They show why an event-driven reserve grid is necessary, especially with cost atoms and posterior plateaus. Add exact floor and ceiling events and evaluate equality symbolically under the declared tie rule; do not substitute a rounded root into an inequality and allow machine error to choose participation.

The same two events apply to the displayed narrow class-value example because the high band remains entirely above the relevant reserve/incumbent support, the low band is excluded, and the class-averaged high value is unchanged. Identical binary and class outcomes in these regions are consequently not evidence of a copy error.

### 4.5 The new search corpus remains an audit boundary

The current PDFs report additional symmetric interior equilibria, broader continuation curves, no mixed equilibria found, and substantial reserve searches. The earlier seed does not contain the whole new implementation. Therefore I do not certify from these PDFs alone:

- Every accepted point on Figure 2's numerical curves.
- The exact extent of the shaded “several equilibria found” region.
- The number and coverage of mixed-profile attempts.
- The reserve counts, unresolved counts, or completeness of found-continuation ranges.
- The claim that every newly accepted numerical row passed the declared refined-deviation checks.

This is a limitation of the available review package, not a finding that the author failed to run those computations. The next audit should inspect source files, immutable inputs, raw accepted and rejected candidates, deviation records, price-pool records, and exercise manifests. The actual commands producing the raw numerical exercises should accompany the rebuild commands in OA E.1.

---

## 5. Economic and institutional revisions

### 5.1 Give the reader a concrete decision before giving the proof taxonomy

The institution needs a short dedicated subsection in the main text, rather than being distributed across the introduction, the late private-information extension, and the empirical scaffold.

It should establish the modeled sequence in ordinary language: a publicly interpretable sale opportunity exists; a prepared buyer is available; another buyer has not committed to executable acquisition preparation; the target trades during that interval; and investors hold relevant target-side information not fully captured by the buyer's own information.

The public information can condition the distribution of $R$. The model does not identify incumbent strength with an observed realized winning bid or an incumbent's strategically chosen preemptive offer. Make that distinction explicit. Otherwise an audience can reasonably ask why changing a bid does not also change signaling and negotiation behavior.

### 5.2 Introduce complementary information early without replacing the simple model

The most avoidable seminar objection is: “Why does a stock trader know the buyer's own acquisition value better than the buyer?” The paper already has a constructive answer, but it appears in Section 5.3.

Move the *interpretation* into the introduction. An acquirer may know its own integration technology; a specialist investor may know different target-side facts. A more accurate private signal need not contain the other signal. Then explain that the benchmark suppresses the buyer's initial signal and gives the investor perfect information to isolate the mechanism; the complementary-signal proposition establishes that those informational extremes are unnecessary.

Do not replace the main benchmark with the full two-signal model merely to answer the objection. That would make the core payoff mechanism harder to see. Nor should the $85\%$ low-cost participation example be presented as a joint empirical calibration of information accuracy and diligence cost. It is a distinct existence illustration.

### 5.3 Explain the participation floor as part of the economics

The floor is not merely a technical bound. Some buyers or opportunities are inexpensive to prepare because of prior familiarity, existing capacity, or otherwise favorable preparation conditions. Their participation makes target proceeds sensitive to acquisition quality even when the market signal is unfavorable. This provides a base return to informative trading.

Without any such state-sensitive participation and without another state-sensitive target payoff, an uninformative/no-entry outcome can remain self-consistent: nobody prepares, target proceeds do not depend on challenger quality, and the investor has no reason to trade on that quality.

The main text should explain this feedback in a brief paragraph beside condition (A1). It makes the role of the assumption intelligible rather than defensive.

### 5.4 Clarify that preparation is required for an executable bid

The model says paying $C$ both reveals the value and permits participation. That is stronger than offering the buyer an optional research report. An uninformed buyer cannot simply skip the cost and bid its current expected value.

Keep the restriction explicit and interpret $C$ as transaction preparation, verification, and commitment of scarce evaluation capacity—not solely the purchase price of an optional signal. The model then studies whether price information makes undertaking that preparation worthwhile.

Likewise, identify $k$ as a trading wedge separate from the adverse-selection price impact already generated by competitive pricing. A possible interpretation is an execution or position-carrying friction; it should not be described as the same adverse-selection spread a second time.

### 5.5 The reserve table changes what “entry” means operationally

In the benchmark $p<\ell$, every challenger that prepares has an admissible valuation and participates meaningfully in the auction. When $p>\ell$, some prepared challengers learn that they cannot meet the reserve. When $p>r$, the incumbent cannot meet it either.

At the weak-incumbent best-found reserve $p=6.280$, the reported preparation probability is $0.25$, but sale probability is only $0.125$: only the low-cost, high-value challenger buys. The incumbent never submits an admissible bid at that reserve, and the probability of two admissible bidders is zero.

This is not an accounting error. It means that the seller's expanded strategy set includes exclusion and no-sale risk, not just recruiting a second competitive bidder. Label $\mathsf E$ as **preparation probability** in the reserve table and add sale probability and the probability of two admissible bidders to the numerical archive. Do not describe every positive preparation outcome in that table as more acquisition competition.

### 5.6 Preserve the institutional evidence boundary

The Imprivata reference supports the separation of an approach, outreach, and diligence-contingent proposals. The manuscript correctly does not claim that it demonstrates a public price-learning interval or a causal stock-price effect on entry.

The targeted primary-source check supports that limited use. It does not turn this example into direct evidence of the mechanism. A stronger institutional introduction eventually needs a short chronology establishing a publicly visible, still-contestable decision interval. That can be a small descriptive exercise; a causal regression is not required to make an upgrade theory manuscript credible.

Keep OA D as a scaffold. Its distinction between event date and first-public date is particularly important. Do not fill it with retrospective private facts as though they were market information at the time.

---

## 6. Presentation and assembly audit

### 6.1 What the assembled version does well

The main text has a coherent progression from acquisition payoffs to inference and equilibrium. The figures do not conflate a frozen information experiment with an equilibrium comparative static. The correspondence figure identifies certificate points separately from numerical lines, and the paper distinguishes existence boundaries from sufficient uniqueness bounds. The welfare section is explicitly a fixed-strength comparison. The reserve table expressly refuses to call the best-found values globally optimal.

The abstract contains 147 words and meets the stated length ceiling. No unresolved `[[...]]` tokens or `??` references were found in the extracted PDFs. A text-boundary scan found no off-page text spans, and the visual inspection found no clipped central formulas or missing tables. These production checks do not replace a source-level build audit.

### 6.2 Specific changes to make

| Location | Observation | Suggested revision |
|---|---|---|
| M p. 1, abstract | “Unique equilibrium” is broader than the stated outcome-uniqueness result; the paragraph previews many secondary results. | Say “unique trading-and-entry outcome” or “unique equilibrium trading outcome.” Consider retaining only the central reversal, fixed-information control, and complementary-information result in the abstract. |
| M p. 2, opening | “Usually deters” sounds like an empirical frequency statement. | Lead with the exact theoretical benchmark: “At fixed information, a stronger incumbent reduces a challenger's expected return from entering a takeover contest.” |
| M p. 3, mechanism paragraph | A high challenger is said to pay the incumbent's bid without mentioning the reserve. | Write “the larger of the reserve and the incumbent's bid.” The later formulas already do this correctly. |
| M pp. 5–7, model | Risk neutrality and the no-bidder-trading restriction are explicit online but not all explicit here. | Add the model paragraph below; also state that the realized incumbent value is not disclosed to the challenger before preparation. |
| M pp. 12–13 | The proposition label starts at the bottom of a page and its conditions begin on the next. | Keep the opening and conditions together with a page-space reservation; avoid a nearly orphaned theorem opening. |
| M p. 16, Table 2 | Matched-dividend rows repeat hidden-economy seller revenue, so the matched financial price is invisible. | Add mean financial price and dividend, or omit those two rows and retain the exact control in Section 6.1. Do **not** overwrite seller revenue with the dividend-inclusive claim price. |
| M p. 18, Figure 2 | The distinction between analytical and found multiplicity is important but visually secondary. | Put “found multiplicity; search not exhaustive” in the shading key. Retain separate line styles and the existing caption qualification. |
| M p. 21, Figure 3 | The logistic endpoint is drawn as open although its tail probability at the bound is well-defined and equals zero. | Use a closed point at zero tail mass / baseline entry. “Bound unattained” refers to the posterior realization, not an undefined value of the plotted tail-probability function. |
| M p. 23, Table 3 | The minimum theorem margin is useful for checking arithmetic but not a measure of economic magnitude or universal robustness. | Keep the full margins online. Consider replacing the main-table minimum with the actual entry gain, while retaining the theorem-region classification. |
| M p. 27, Table 4 | The long selected-maxima panel attracts attention to a heavily incomplete seller search. | Keep the analytically supported fixed-reserve comparisons in the main paper. Move Panel C and coverage counts to the online appendix until the pricing correspondence and event tests have been checked. |
| M pp. 34–43, paper appendix | Supporting statements, extension formulas, and proof steps require considerable forward/backward navigation. | Group each extension's definitions, statement, and short proof together. Keep the longer regularity work online. |
| M p. 38 | The welfare proof wording can be read ex post. | Insert “in conditional expectation” as explained above. |
| OA pp. 30–37 | The full placeholder registry occupies substantial scholarly appendix space after assembly. | Preserve it in the replication package; optionally replace the printed registry with a concise data dictionary and a precise pointer to the machine-readable version. |
| OA pp. 41–43 | Rebuild instructions are not commands for producing every new raw exercise. | Include the exact raw-exercise commands and actual run manifests in the distributed package. No invented commands or presumed module names. |

The figure and table comments are about communication, not grounds for rejecting the theory.

### 6.3 Suggested main-model insertion

> All strategic agents are risk neutral. The target share is the only traded claim that conveys information about the acquisition match in the benchmark, and neither bidder trades it. The investor has no control rights and cannot acquire the target. The sale mechanism binds all target shares, so shareholder tendering and holdout are outside the modeled continuation. The incumbent's value distribution is public, conditional on information available when the sale opportunity becomes visible, but its realized value is not disclosed to the challenger before preparation.

This aligns the main model with its online probability-space specification rather than adding a new friction.

### 6.4 Suggested institutional paragraph near the opening

> The relevant information is complementary rather than necessarily superior. A potential buyer may know its own integration capabilities while investors specializing in the target hold information about customers, technology, or product demand. A target price can then add to the buyer's private assessment before it commits resources to an executable acquisition proposal. I first isolate the mechanism in a benchmark with a perfectly informed investor and an initially uninformed challenger. I subsequently establish the reversal with distinct imperfect signals, including a buyer signal that is more accurate than the investor's.

The examples are proposed interpretations of the information structure, not empirical claims about a named transaction.

### 6.5 Suggested reserve-continuation paragraph

> Away from the positive-preparation-floor region, a continuation specifies a price-pooling rule as well as investor orders. Different pooling regions may support different buyer posteriors and participation decisions even at the same order profile. I therefore treat orders, price pools, beliefs, and preparation as joint equilibrium objects. Numerical continuations are distinguished by their complete price and trading schedules; a single candidate pricing construction is not an equilibrium-selection rule for the seller.

This belongs in Appendix A.5 and OA C.6. The explicit $p=7$ example above supplies a small regression test for its implementation.

### 6.6 Result status and authorial voice

The assembled text uses first-person singular consistently. That is entirely defensible for a sole-authored manuscript, although it differs from the earlier build specification. This is an authorial choice, not an accuracy problem.

The more consequential convention is result status. The assembled propositions generally omit the agreed status label at the statement, while tables use “proved.” A normal journal manuscript need not label every analytical proposition, but this project deliberately distinguishes analytical, computer-assisted, numerical-diagnostic, and open claims. Preserve that distinction in a single consistent way. In particular, identify Proposition 3 as computer-assisted at its statement, and do not let a figure's accepted numerical line inherit an analytical or computer-assisted label from adjacent certified points.

---

## 7. Literature and contribution assessment

This review includes a targeted primary-source check, not a fresh exhaustive novelty audit or a re-audit of every cited paper's proof.

The central comparison with Dow, Goldstein, and Guembel is correctly chosen. Their model already makes the sensitivity of a traded claim to a real decision important for information-production incentives. The distinctive claim here must remain the **auction-derived opposition** between the prospective buyer's acquisition profit and the information sensitivity of the target claim, together with an equilibrium participation reversal. Generic “market feedback,” endogenous information, or endogenous bidder pools are not new claims.

The current author-hosted Pernoud–Gleyze manuscript remains dated March 2026 and concerns buyers learning about own and competing valuations. The retrieved Liu–Bernhardt author manuscript remains the July 2022 draft concerning market feedback in security-payment auction design. The primary NBER record confirms the Carlin et al. working paper and its DOI. These checks support the present bibliographic identities and the broad distinctions in the introduction; they do not independently clear every possible overlap with their full results.

The Lin–Ma–Yang–Zhu comparison is appropriately about an initiated transaction with payment terms and subsequent learning/withdrawal. A later listing date should not be substituted for a verified manuscript date. Nothing in the current manuscript relies on a proof criticism of that paper for novelty, which is the right decision.

The Imprivata filing is a valid primary source for the limited process description, not evidence that the stock market recruited a bidder. The present paragraph says so. Improve the institutional evidence by establishing the decision interval, not by overstating what this reference supports.

### Targeted external sources checked

- Dow, Goldstein, and Guembel, published *Incentives for Information Production in Markets where Prices Affect Real Investment*, DOI `10.1093/jeea/jvw023`, including the discussion of alternative price-pooling continuations following Lemma 1.
- Pernoud and Gleyze, author-hosted *How Competition Shapes Information in Auctions*, March 2026 manuscript, abstract/model and stated main results.
- Liu and Bernhardt, author-hosted *Simplifying Auction Designs via Market Feedback*, July 11, 2022 manuscript, version and abstract/model distinction.
- Carlin, Liu, Officer, Pernoud, and Tu, NBER working-paper record for *Bidder Pools in Mergers and Acquisitions*, DOI `10.3386/w34846`. The full NBER PDF was not retrieved in this review.
- Imprivata's definitive proxy, SEC accession `0001193125-16-677939`, process discussion and transaction record.
- Finance Theory Group listing for *Payment Methods and Market Feedback in Mergers and Acquisitions*, used only to distinguish listing date from manuscript version.

I did not find a bibliographic change in these checks that requires replacing the central citation structure. I have not certified every DOI or performed a full-model collision audit of every paper in the bibliography in this turn.

---

## 8. Recommended revision sequence

### Before the upgrade circulation

**First, repair the reader's entry into the paper.** Add the compact institutional subsection, introduce complementary private information early, and make the main model self-contained about preferences, traded claims, and the required preparation decision. Correct the reserve omission in the introductory payment sentence.

**Second, separate the established main result from the new seller search.** Keep the fixed-reserve theorem and supporting reserve alternatives. Move the selected exploratory maxima out of the main table, or at least avoid treating them as the numerical resolution of the seller problem. Add the complete pricing-continuation example and the exact reserve-event tests to the online specification.

**Third, audit the actual assembled numerical archive.** Match the independent seed certificates to the port, verify all accepted continuation rows and their global-deviation evidence, inspect pricing-pool handling, and check the source-to-registry-to-table chain. Negative theorem margins must not be confused with failed candidate equilibria; open searches must not be converted into empty equilibrium sets.

**Fourth, make the small presentation edits.** Repair the matched-price display, the logistic endpoint marker, the conditional-welfare sentence, and the fragmented extension-proof organization. Restore a consistent result-status convention.

These changes do not require a first-price model, a globally optimal reserve theorem, or an empirical causal design before the upgrade. They require accurate economic framing and an auditable account of what is already being claimed.

### The next substantive theorem

The seller's problem should now be written with both sources of continuation variation visible:

$$
\sigma=(\text{orders},\text{price mapping},\text{price beliefs},\text{preparation}),
\qquad
\sigma\in\mathcal E(p,r).
$$

Characterize economically meaningful portions of this correspondence before maximizing over reserves. A useful next result could concern seller-optimal discovery, commitment to a sale rule, or a justified selection/refinement that reduces uninformative price pooling. It need not preserve the original comparative-static sign at every reserve.

The most important empirical preparation is a verified account of when the target trades during a public, still-open participation interval. The pilot's current occurrence/disclosure-date distinction is the correct starting point.

**Bottom line:** the paper has a valid and intelligible theoretical engine. The next improvement is not more ornamental robustness. It is to connect that engine more directly to the institution and to handle the full pricing-and-trading continuation when sale terms change.

---

## Appendix: Verification files supplied with this review

`independent_checks.py` reconstructs the displayed nodes, the signal grid, the asymmetric numerical deviations, and the pricing-pool example from the PDF equations. `additional_checks.py` independently integrates realized auction outcomes and checks analytical support for the reported signal-grid candidates. The preserved certificate script is rerun in a separate copy; its interval outputs are compared with the displayed bounds.

The numerical evaluations in the new pricing-pool example are diagnostics. Its equilibrium existence and global optimality follow from Proposition R's analytical proof, including the common rational marginal-profit bound $143/1600$.

The reviewed input hashes are:

- Main PDF SHA-256: `6568203e5266ffe076ec094ef9768b763f7a227813064418fa680c4b6bff1427`.
- Online appendix PDF SHA-256: `734a51c2e4ed130e3cb11597c89d2c32d39a01dad64704ee1979a54427e36922`.

The execution environment for the independent checks was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and mpmath 1.3.0. The figures and tables were reviewed in their supplied rendered PDFs; no new assembled-paper figures were generated and no source manuscript was silently changed.
