# M1 notes: institutional motivation and Laplace prose

Scope: fragments M1_01 to M1_08. Sources are the memos in
`audit/alex_meeting_2026_10_21/memos/`. Each fragment header states
its anchor, placeholders, bibitem requests, and new symbols.

## Fragments

| File | Target | Source claims |
|---|---|---|
| `M1_01_intro_investor_and_noise.tex` | Insert after main.tex line 177 | Q3_story S3; Q2_laplace_economic Section 3.6 intro sentence |
| `M1_02_roles.tex` | Insert after main.tex line 349 | Q3_story Section 7.1, S5(a); evidence table in Q3_story Section 3.8 |
| `M1_03_laplace_justification.tex` | Replaces main.tex lines 337-340 | Q2_laplace_technical Section 7 draft paragraph; Q2_laplace_economic Section 3.6, Claims 1, 2, 4, 8 |
| `M1_04_t0_cancellation.tex` | Insert after main.tex line 564 | Q3_story S1, S2; SYNTHESIS B.3 item 2 |
| `M1_05_shareholder_gain.tex` | Insert after main.tex line 956 | Q3_story Section 7.2, S4; Q3_welfare W5, W6 |
| `M1_06_empirical_trader.tex` | Insert after main.tex line 1081 | Q3_story Sections 3.8, 4 |
| `M1_07_literature_blockholders.tex` | Insert after main.tex line 205 | LIT_extracts A1, A4; Q3_stake Result 10 items 1, 4, 6; SYNTHESIS B.3 item 5 |
| `M1_08_informed_shareholder.tex` | Insert before online_appendix.tex line 1611 | Q3_stake (S4)-(S7), (S12), (S14), Results 3, 8, 10; Q3_story S6 |

Line numbers refer to `overleaf/paper-revision/` on 21 October 2026.
Apply M1_02 and M1_03 in either order. Their anchors do not overlap.

## Placeholders for the numerics team

| Placeholder | Needed definition |
|---|---|
| `\NUM{Pi_acc}` | Informed investor expected gross profit with price access at `r_1`, at one trading unit per share of float |
| `\NUM{breakeven_scale}` | Break-even trade scale in trading units per share of float, for the net gain of initial shareholders **relative to an economy without the informed investor**. This is the W5 ratio of the proceeds gain to the gross profit with access. It is not the access-alone ratio. Confirm the CSV uses this comparison. |
| `\NUM{Omega_U}` | Benchmark value of the full-order stake bound in M1_08, in order units |
| `\NUM{Omega_0}` | Benchmark value of the no-trade stake bound in M1_08, in order units |

In M1_05 the two `\NUM` values sit in one standalone sentence. Delete
that sentence alone if the numerics do not arrive. The paragraph
then still reads correctly. The header of M1_05 marks the sentence.

No fragment uses the symbol for trade scale from the memos. M1_05
states the scale in words, as trading units per share of float.

## Citation keys in the fragment bodies

Already in the main bibliography: `ref-EdmansGoldsteinJiang2015`.

New `\bibitem` records requested for the citations pass (all keys
from BRIEF Section 7):

- `ref-Meulbroek1992`, `ref-AugustinBrennerSubrahmanyam2019`,
  `ref-AcharyaJohnson2010` (M1_02)
- `ref-SmithSorensen2000`, `ref-Clark1973`, `ref-Cont2001` (M1_03)
- `ref-KyleVila1991`, `ref-Maug1998`, `ref-BackEtAl2018` (M1_07)

One extra check: M1_08 cites `ref-EdmansGoldsteinJiang2015` inside
the Online Appendix. Confirm the Online Appendix has its own
`\bibitem` for that key. Add one if it does not.

The anchor line in the header of M1_07 quotes
`ref-GoldsteinGuembel2008`. That key appears in the header only. The
fragment body does not need it.

Empirical citations in the memo drafts without a key in BRIEF
Sections 5 and 7 do not appear in the fragments. M1_03 therefore
cites no fit claim for Laplace noise. It states the class property,
the three derivations, and one fat-tail fact with `ref-Cont2001`.

## Notation choices

- Classes `j in {H,L}`, prior `\pi`, class proceeds `t_H, t_L`, and
  `\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}` follow the brief notation
  sheet. The word for the investor information state is "class"
  throughout.
- M1_03 writes the full-order log odds with the prior term,
  `logit \pi + (2/b) clip(x)`. At `\pi=1/2` this reduces to the form
  in the technical memo.
- M1_08 states the full-order stake bound with the common floor
  `\kappa(\pi)`. The stake memo proves the bound at `\pi=1/2` with
  `m`. The common-floor form stays sufficient at a general prior,
  because each class floor is at least `\rho\kappa(\pi)\Delta_T` and
  the bound uses the larger gain `w_H`. It coincides with the memo
  formula at the benchmark. The no-trade bound needs no change.
- M1_08 displays carry no equation numbers. Number them in the
  Online Appendix sequence at integration. Renumber the subsection
  title "A.12" to the next free number in Section A.

## Scope points and items not fully verified

1. **Lawful trade (M1_02).** The sentence states the model position
   in short form. The memo basis covers United States law only:
   own-research trade outside the bidder and target information set.
   European market-abuse law received no check in the memos. The
   author may want a jurisdiction word before submission.
2. **Abstract-level sources.** Kyle and Vila (1991), Maug (1998),
   Back et al. (2018), and Acharya and Johnson (2010) rest on
   abstracts in the memos. No full text of Kyle and Vila was read.
   The fragments keep each claim at mechanism level and state no
   theorem, sample detail, or magnitude from these sources.
   Meulbroek (1992) also rests on the publisher abstract. The
   fragment uses it only for the arrival-information contrast.
3. **Positive low-class gain (M1_04, M1_05).** The sentences
   `t_L>t_0` hold at the benchmark, where each class value lies
   above the reserve. In the general ranked model the low-class
   gain can equal zero if the class has no admissible bid. Align
   these sentences with the support condition in the general-model
   rewrite. M1_08 already states the general form.
4. **Split of the transfer (M1_05).** Q3_story Section 7.2 reports
   split values under one gross-volume decomposition. The task
   names no placeholder for them, so M1_05 states the split in
   words from Q3_welfare W6 and reports no split value. Add values
   only with new placeholders from the reconciliation file.
5. **Screening-region surplus.** Q3_story Section 7.2 adds a surplus
   clause for the screening region. Q3_story S4 marks that sign as
   a numerical diagnostic with no general proof. M1_05 omits the
   clause and states only the proceeds loss.
6. **Proposition label (M1_01, M1_03).** Both fragments point to
   `result-proposition-a-5`. In the current manuscript that label
   names the logistic case alone (main.tex lines 1857-1864). The
   fragments assume the noise drafter restates it for the
   bounded-score class. Update the two pointers if the class result
   takes a new label.
7. **Stake cutoffs (M1_08).** The fragment reports the two
   sufficient analytical bounds only. It omits the full-order
   existence cutoff and the partial-sale branch from the stake
   memo. Both rest on numerical work and need placeholders and
   status labels if the author wants them.
8. **Compile check.** The eight fragment bodies compile together in
   a stub article that defines the citation command, the `\NUM`
   placeholder, and the cross-reference labels. The check ran with
   `pdflatex` on 21 October 2026 and produced a PDF with no errors
   and no undefined references in the stub. The stub file stays
   outside the project. Full-manuscript compilation remains with
   the integrator.
