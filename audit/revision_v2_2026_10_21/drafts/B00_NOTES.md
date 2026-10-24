# Noise revision: formal fragments

The five fragments apply to the source snapshot named in `BRIEF.md`.
Only these draft files change in this contribution.
Each fragment has the required source range and text anchors.
The manuscript sources remain read-only.

## Fragment inventory

- `B01_main_noise.tex` replaces main text lines 828–841 and 858–860. It preserves the figure and the atomless-cost paragraph.
- `B02_main_class_noise.tex` replaces main text lines 1815–1880. It states the class result, gives the proof, retains the logistic example, and corrects the Blackwell comparison.
- `B03_oa_laplace_extreme.tex` inserts a short result after the A.6 heading. It gives separate complete proofs of R8, R9(i), and R10.
- `B04_oa_c5_instruction.tex` replaces Online Appendix lines 2625–2632. Only the final comparison instruction changes in substance.
- `B05_oa_quality_scope.tex` inserts a scope note after the opening paragraph of Online Appendix A. It lists the prior and reserve dependencies in A.1–A.7.

## Labels and notation

These labels remain in B02:

- `logistic-noise`
- `result-proposition-a-5`
- `eq:paper-a-21`
- `eq:paper-a-22`
- `eq:paper-a-23`

These labels are new:

- `oa-a-laplace-extreme`
- `result-lemma-oa-laplace-extreme`
- `oa-a-quality-class-scope`

No label is removed. No existing equation number changes.
The new lemma has a descriptive title and no numerical designation.
Each fragment header lists its new symbols.
No new symbol uses the letter reserved by the brief.
The existing Blackwell citation uses `ref-Blackwell1953`.
No new bibliography record is required.

## Placeholders and numbers

The optional sentence in B01 has `\NUM{entry_hypsec_r1}` and `\NUM{entry_t3_r1}`.
The sentence remains commented out until both values appear in `reconciliation.csv`.
The surrounding text reads correctly without it.
There are no active numerical placeholders.
The existing logistic entry, cutoff, standardized cutoff, and Laplace comparison numbers remain unchanged.
No new numerical estimate is transcribed from the memos.

## Source checks and scope

R8 needs a comparison about the median.
B01 and B03 state that restriction.
B03 proves the equality case as well as the tail inequality.
R9(i) covers every pure order profile, without symmetry or log concavity.
The positive-part comparison makes the scalar differential inequality precise.
The posterior call formula includes the general-prior weights.

R10 uses the paper's logistic scale exactly.
The density in (A.21) has characteristic function `pi*b*t/sinh(pi*b*t)`.
Its first Euler factor is the characteristic function of Laplace noise with scale `b`.
The remaining factors define independent extra noise.
The finite variance sum gives convergence of the random series.
This argument covers mixed order profiles as well as pure profiles.

The common-variance sentence in SYNTHESIS B.6 item 1 has weaker evidence than the common-scale decomposition.
R10 reports common-variance incomparability as a numerical diagnostic, without an analytical proof.
B02 states that status explicitly.
It does not present the diagnostic as a theorem or as a reason to order entry.

R16 uses the posterior supremum under full orders in the upper cost restriction.
The word “attained” must not imply a maximum at a finite flow.
The logistic posterior never attains its upper bound.
B02 defines an essential supremum and allows it to lie below `M(pi)`.
Its posterior and residual bounds use the conservative class constants from `b=1/L`.
The sharper constants from the exact likelihood-ratio bound are unnecessary for this statement.

Online Appendix A.3 already states the needed regularity result at lines 426–464.
It permits every positive density in `W^{1,1}` with `|f'| <= L*f`.
The translation identity, absolute integrability, interchange of integrals, derivative bound, and product rule all apply.
B02 verifies these hypotheses from the score bound.
The price inversion uses the unconditional entry floor from the zero preparation cost.
The price construction requires monotonicity in the posterior, not monotonicity in flow.

The ownership restriction needs care in the general class.
The sufficient Laplace condition based on `alpha_H > 1/2` does not apply to every class member.
B02 uses the exact comparison `e_H(r1)*W_H(r1) > rho*W_H(r0)`.
The point-mass case with `W_H=1` satisfies it automatically.
The nonemptiness argument fixes an interior threshold at a continuity point before it chooses nearby incumbent strengths.
Its openness statement holds with the zero preparation cost fixed.

B05 distinguishes the probability arguments from the point-mass auction formulas.
It includes the unequal-prior correction to the full-profile identity in (OA.22).
It also records the prior weights in the plateau and aggregate entry formulas.
The displayed signal formulas in A.7 retain the equal-prior scope.
Their conditional-independence and measurable-inverse arguments apply to quality classes.
An arbitrary-prior theorem for those displayed signal inequalities is outside this contribution.

The reserve boundary term is `p*F(p)*[G_L(p^-)-G_H(p^-)]`.
Equal admissibility makes this term zero.
Without equal admissibility, it can offset the spread increase under a stronger incumbent.
The reserve enters subsequent arguments through the auction expectations and the spread.
It adds no separate term to the investor residuals.

No unverified analytical step remains in the transcribed R8–R10 and R16 arguments.
The wider class claim does not extend the Proposition 3 certificates.
Those certificates retain their Laplace-specific scope.

## Integration dependencies

Apply B02 after the quality-class revision of Proposition 2 and its nonemptiness argument.
Keep the brief's `pi`, `kappa(pi)`, `W_H`, and zero preparation cost.
Use the exact ownership restriction in B02 for the general noise class.
Keep the atomless-cost revision outside B01 and B02.
Update the old probability declarations elsewhere before use of the new scope note.
Retain the equal-prior designation for the displayed signal formulas in A.7.

## Verification

Both review copies compile from the manuscript sources with these fragments applied.
The final logs contain no undefined references, undefined citations, or overfull lines.
The appendix retains underfull messages in unchanged material.
The affected main text, proposition, proof, logistic example, scope note, extremal result, and C.5 instruction render without clipped text or equations.
This verifies fragment syntax and layout before the other revisions are combined.
It does not replace the final compilation after integration.
The optional numerical sentence remains inactive because the reconciliation file is absent at this handoff.

## Fix round 1

The working copies are the `*.prose.tex` fragments.
This section updates the earlier notes on notation, scope, and nonemptiness.
Only `B01_main_noise.prose.tex`, `B02_main_class_noise.prose.tex`, and `B03_oa_laplace_extreme.prose.tex` change in this round.
The earlier prose edits remain in place.

1. **Prior notation.**
   In B03, proof (iii) now states the logistic characteristic function directly as its Euler product.
   The circle-constant formula is removed.
   The symbol `pi` denotes the prior throughout the fragment.
   The header records this change.

2. **Location condition for the tail claim.**
   B03 states that the density class has no location restriction.
   The lemma requires median zero in part (i) alone.
   B01 now states that restriction in its main-text claim.
   B02 specifies symmetric versions of its examples.
   Laplace, logistic, hyperbolic-secant, and centered Student laws have median zero.
   An independent sum of centered Gaussian and Laplace variables also has median zero.

3. **From flow to price experiments.**
   B03 makes both price claims conditional on measurable prices and sufficiency of the Laplace price for its flow posterior.
   The other price is a garbling of its own flow experiment.
   The proof obtains price dominance by transitivity.
   The new paragraph, "Price construction," states independence, the payoff inequalities, zero preparation cost, positive entry probability, and the tie rule.
   It proves that the constructed price increases strictly in the posterior and has a measurable inverse.
   B01 and B02 now tie their price comparisons to this construction.

4. **Reference to part (iii).**
   The statement and proof in B02 now name part (iii) of Proposition 2 explicitly.
   The statement gives the later-strength cost condition and the resulting full orders and entry.
   The proof states why the larger spread preserves the strict order bound.

5. **Joint nonemptiness and ownership construction.**
   B02 replaces the compressed paragraph with six steps.
   It first fixes an interior threshold at a continuity point of both conditional posterior laws.
   This fixes both conditional entry probabilities before any strength or cost is chosen.
   It then chooses the strong strength, the preparation cost, the weak strength, the order cost, and the later strength, in that order.
   The proof gives the strict inequalities for each choice and explains their joint persistence.
   The proposition names the open coordinates `(r_0,r_1,r_2,c_H,k)` and the fixed primitives, with the other preparation cost zero.

6. **Equality and the essential supremum.**
   In B03, proof (i) now uses continuity to extend the density identity from almost every point to the whole initial interval.
   It then uses a continuous nonnegative difference with zero integral to identify the complete right tail.
   Reflection identifies the left tail.
   B02 names Lebesgue measure as the base measure for its essential supremum.
   It also states equivalence of the flow laws to that measure and equality with the ordinary supremum by continuity.

7. **Other corrections.**
   B03 now reflects the observation when the high-class order lies below the low-class order.
   This preserves the fixed class labels and prior, including for asymmetric noise.
   B02 makes the strict class-value gap explicit in its nonemptiness statement.
   Its constant-ratio argument now states directly why a constant likelihood ratio must equal one.

### Verification for this round

Each changed fragment compiles in a standalone stub under `../verification/B_fix_round_1/`.
The stubs use the corresponding manuscript preamble.
External references use values from the existing manuscript auxiliary files.
The output text was examined in each PDF.

- `B01_stub.pdf`: two pages; main-text scope and price claims appear as revised.
- `B02_stub.pdf`: seven pages; the proposition, all six construction steps, and the logistic example appear in full.
- `B03_stub.pdf`: two pages; the equality proof, product formula, and price conditions appear in full.

The final logs contain no warnings, undefined references, undefined citations, or overfull or underfull boxes.
This is a fragment compilation check; it does not verify final manuscript integration.
No tests were written or run.
Hashes confirm that the five original fragments, the B04 and B05 prose copies, and both manuscript sources remain unchanged.
