# S4 paper-appendix reorganization (P17, P18, P19, P20, P21)

Draft: `paper/drafts/appendix_A_revised.md`, to be spliced in place of everything from
`## Appendix A {#paper-appendix}` to the end of `paper/main.md`. `paper/main.md` and
`paper/online_appendix.md` were not edited. Nothing committed.

## Subsection and anchor map (old to new)

| Old | New | Anchor |
|---|---|---|
| A.1 Supporting results (Props A.1-A.9 statements) | A.1 Acquisition payoffs and Bayesian pricing (Prop 1 proof, Props A.1, A.2) | `#pa-results` (kept) |
| A.3 Proofs of Propositions 1 to 3 (Prop 2 part) + A.2 trading incentives | A.2 Global trading and the main comparison (order bound, J-test, Prop 2 proof, Props A.3, A.4) | `#pa-proofs` (kept) |
| A.4 The certified equilibria | A.3 Certified asymmetric equilibria (Prop 3 proof) | `#pa-certificate` (kept) |
| A.2 logistic / atomless / nonemptiness formulas + Props A.5, A.6 | A.4 Distributional extensions and nonemptiness | `#pa-calculations` (kept) |
| A.2 complementary signals + Prop A.7 | A.5 Complementary private information | `#pa-signals` (new) |
| A.2 acquisition surplus + Props A.8, A.9 | A.6 Bargaining and access to prices | `#pa-welfare` (new) |
| A.5 The seller's continuation problem | A.7 Seller continuation | `#pa-design` (kept) |
| A.6 Numerical parameters | A.8 Numerical parameter declarations | `#pa-parameters` (kept) |

All six old `{#pa-...}` anchors survive; two new ones added. No file outside `paper/main.md`
references the old anchors.

## Proposition locations (identities unchanged)

| Result | New location | Status label |
|---|---|---|
| Proposition 1 (proof) | A.1 | (statement in body) |
| Proposition A.1 | A.1 | analytical |
| Proposition A.2 | A.1 | analytical |
| Proposition 2 (proof, six steps + part iii) | A.2 | (statement in body) |
| Proposition A.3 | A.2 | analytical |
| Proposition A.4 | A.2 | analytical |
| Proposition 3 (proof) | A.3 | computer-assisted |
| Proposition A.5 | A.4 | analytical |
| Proposition A.6 | A.4 | analytical |
| Proposition A.7 | A.5 | analytical |
| Proposition A.8 | A.6 | analytical |
| Proposition A.9 | A.6 | analytical |
| Proposition A.10 (new: price pooling at fixed orders) | A.7 | analytical |

## Equation tag map (old to new)

Old A.1->A.10, A.2->A.11, A.3->A.29, A.4->A.4, A.5->A.6, A.6->A.21, A.7->A.23, A.8->A.22,
A.9->A.24, A.10->A.25, A.11->A.26, A.12->A.27, A.13->A.28 (bounds split into A.32, A.33),
A.14->A.34, A.15->A.35, A.16->A.33, A.17->A.36, A.18->A.37, A.19->A.39, A.20->A.41,
A.21->A.1, A.22->A.5, A.23->A.8, A.24->A.14, A.25->A.12, A.26->A.13, A.27->A.15,
A.28->A.16, A.29->A.17, A.30->A.18, A.31->A.19, A.32->A.20, A.33/A.34->A.44,
A.35->A.42, A.36->A.53, A.37->A.54, A.38->A.55, A.39->A.56, A.40->A.57.
New tags: A.2 (indicator integrals), A.7 (J-test), A.9 (fixed-experiment indicator),
A.30, A.31 (conditional independences, joint posterior), A.38 (Nash program), A.40
(conditional surplus), A.43 (continuation object), A.45-A.49 (price-pool family),
A.50-A.51 (exact reserve events), A.52 (outcome measures).
The body never cites an appendix equation tag, so no body edits follow from this map.

## Body cross-references the parent must update

- Proposition 3 statement in the body says "benchmark parameters of Appendix A.6"; the
  declarations are now Appendix A.8.
- The appendix cites body tags (2), (4)-(14), (A1)-(A3) as numbered on 2026-09-05. If the
  body agent renumbers displays, these citations need the same renumbering.

## New placeholders (to add to `paper/quantity_manifest.csv`)

| Name | Definition | Type |
|---|---|---|
| `pool_reserve` | Declared reserve for the price-pool family of Proposition A.10 (input 7). | input |
| `pool_posterior_cutoff_low` | Pooled zero-price posterior $\bar\mu_c$ at $c=-\log 2$, from the validated price-pool regression row. | output |
| `pool_posterior_cutoff_high` | Same at $c=0$. | output |
| `pool_entry_cutoff_low` | Total preparation probability $\mathsf E_c$ at $c=-\log 2$. | output |
| `pool_entry_cutoff_high` | Same at $c=0$. | output |
| `pool_revenue_cutoff_low` | Expected seller revenue $\mathcal R_{T,c}$ at $c=-\log 2$. | output |
| `pool_revenue_cutoff_high` | Same at $c=0$. | output |

All 44 placeholders present in the old appendix are retained. Exact-event outcomes
($\mathsf E=\rho$, sale $\rho/2$, $\mathcal R_T=\rho p_L/2$, $\alpha_H=1/2$,
$\alpha_L=e^{-2/b}/2$) and the rational bounds $7/32$, $7/64$, $143/1600$,
$e^{-1/2}/2<1/3$ are written symbolically, so no placeholders were needed for them.

## Substantive corrections to the previous text

1. **Welfare wording (P19, spec 13.3).** "every additional entrant contributes at least
   $p^2/r$" replaced by "each additional preparation decision contributes at least $p^2/r$
   in conditional expectation, given price information and preparation cost", with the
   sentence that a realized low-value preparation need not cover its cost.
2. **Fixed-information proposition (P18, spec 13.4).** Proposition A.3 previously said
   "Hold the joint distribution of a signal, challenger quality, and preparation cost
   fixed", conditioning only on the signal. It now states that cost is independent of
   $(S,\Theta)$ with a fixed law, that the experiment and cost law are held fixed as $r$
   varies, and that the buyer's posterior is $\Pr(H\mid S)$; the correlated-cost version
   ($\Pr(H\mid S,C)$) is named as not needed.
3. **Proposition A.4 domain.** The maintained domain $\mathcal D$ was previously only in
   the online appendix; it is now in the statement, and the four thresholds are
   distinguished explicitly (existence boundary, two sufficient uniqueness bounds,
   participation ceiling).
4. **Proposition A.2.** The proof now establishes the floor before dividing, derives the
   inversion from conditional pricing, recovers the posterior by the tower property, and
   includes the increment inequality (A.3) that the old paper appendix only asserted
   ("strictly increasing ... because entry is nondecreasing").
5. **Prop 2 proof.** Necessity (Steps 3, 4) and construction (Step 5) are now separated
   explicitly; the further-strength conditions of part (iii) are kept separate from
   (A1)-(A3). The J-test (A.7) that the price-pool argument uses is now in the paper
   appendix rather than only in OA A.5.
6. **Proposition A.7.** Definitions ($\phi_y,\mu_\pm,w_H,w_L,D$) now precede the
   statement. The proof is a compact four-step chain with the two conditional
   independences, $\mu_X=(1-a)+(2a-1)\lambda_X$, $\Pr(H\mid P,Y)=\phi_y(\mu_P)$,
   $e_H\ge e_L\ge\rho$, $D\ge\rho\Delta_T>0$, the inversion, residual bounds, exclusion,
   global inequality, construction, and the positive-probability additional-preparation
   event. The old text had these dispersed across A.1 and A.2 with references to the
   online appendix for the joint laws.
7. **Proposition A.8.** The four institutional elements (verifiable values, enforceable
   runner-up fallback, zero-reserve no-entry payoff, bargaining weight) are stated before
   the proposition, and the boundary at $\eta=1/2$ is attributed to this institution.
8. **Seller continuation (P20).** (a) Payoff cases over the full reserve domain including
   $p>\ell$ and $p>r$, with the note that the $p<\ell$ formulas must not be applied outside
   their support. (b) The continuation object (A.43) is now the full tuple (orders, price
   mapping, price beliefs, preparation rule), with identity by the whole object. (c) New
   Proposition A.10 and its complete proof (pooled posterior with the CDF $F_Z$, buyer
   checks on both regions, conditional pricing on both regions, global bound $143/1600$),
   plus the explicit statements that it does not establish uniqueness within
   $\mathcal E(7,r_0)$ and that the benchmark floor rules the phenomenon out. (d) Exact
   events $p_L=h-c_L/m$ and $p_H=\sqrt{2r(h-c_H/M)-r^2}$ recorded as analytically
   supported event candidates under the tie rule, not interior strict points. (e) Outcome
   measures $\mathsf E,\mathsf A,\mathsf S,\mathsf C_2$ with
   $\mathsf S=\Pr(R\ge p)+\mathsf A-\mathsf C_2$. (f) The local decomposition now names its
   regularity conditions and says the level objective is the right object at a price pool.
9. **Proposition A.5 / logistic.** Added the sentence that Laplace and logistic at common
   scale share neither variance nor a Blackwell order.
10. **Prop 3 / certificates.** Added the explicit statement that the cover must hold for
    every candidate in the bracket because the root is known only to lie inside it, and
    that no root uniqueness across schedules is used.
11. **Voice.** First person singular throughout; no "we". No mention of reviewers, the
    spec, or assistants. A single citation to Dow, Goldstein, and Guembel (2017) is added
    in A.7 to disclaim novelty for price-pooling multiplicity.

## Checks run

- `pandoc paper/drafts/appendix_A_revised.md -t plain -o /dev/null` exits 0 (warnings are
  the plain-text renderer's refusal of `\tag`/`\tfrac`, as for the current appendix).
- Tags (A.1)-(A.57) sequential; every `(A.n)` cited exists.
- No "we"/"our" in prose; no em dashes.
- Hand-checked arithmetic: $\mu_X(-\log 2)=1/3$ at $b=2$; $\bar\mu_0=e^{-1/2}/2$;
  $m=(1+e)^{-1}>1/4$; $J_c\ge 7m/8>7/32$; $7/64-1/50=143/1600$; $p_L\approx6.2817$,
  $p_H\approx1.3253$ at the benchmark; $Mc_L/m=e<6$; $mc_H/M=6/e>1$; sech form of the
  logistic density; logistic inverse $y=(Aw-1)/(A-w)$.
