# Manuscript notation and consistency audit

Baseline: the editable Overleaf LaTeX masters, `overleaf/paper/main.tex` and `overleaf/paper/online_appendix.tex`, at commit `6357606` (the 30 September 2026 import). The audit is read-only: it changed no manuscript file.

## Method

Five independent reviews covered both files: notation in the paper and Appendix A; notation in the online appendix and its agreement with the paper; result statements, qualifiers, status labels and numbers against `numerics/quantity_registry.csv` and `audit/peer_polish/claim_ledger.csv`; cross-references, role and concept terms, and captions against Online Appendix E.4; and the carry-over of the talk audit (`audit/talk_consistency/report.md`, `talk/paper-sync.md`). Findings were merged across reviews. Each merged finding was then re-checked independently with an attempt to refute it and fresh use counts. A completeness pass looked for areas no review covered, and its findings (K-numbered) were re-checked the same way. Symbols fixed by the numerical contract (C.0) are treated as coordinated updates, never as find-and-replace.

## Counts

- Reviews reported 175 findings, merged to 76; the completeness pass added 12.
- After re-checking: 71 stand (22 confirmed as stated, 49 with a corrected fix), 5 refuted, 12 not yet re-checked.
- Severity of those standing: High 6, Mid 33, Low 32.
- Adoption class: A (mechanical, safe to apply in the .tex) 24; B (notation or terminology change needing the author's approval) 36; C (touches C.0-locked symbols, numbers or display precision, figure scripts, manifest or registry; report only) 11.

## Class B: notation and terminology decisions

| Id | Severity | Category | Finding | Locations | Talk audit |
|---|---|---|---|---|---|
| M03 | High | notation | theta is both the challenger's numeric value and the H/L quality label; H, L and Theta are undefined in the paper; the OA's v_theta convention is introduced once and then dropped | main.tex:396, main.tex:492-493, main.tex:552-553 … | F01 |
| M06 | High | notation | T is the investor's signal, the locked target subscript, the transfer T_eta, a pointwise revenue function and a truncation bound; t is also a substitution variable | main.tex:447, main.tex:493, main.tex:1020 … | F04 |
| M08 | High | notation | Accuracy a sits next to the flow densities a_H, a_L, a_+, a_- in the same display; a_0, a_1 are also segment endpoints | main.tex:596-598, main.tex:1020, main.tex:1474 … | F02 |
| M12 | High | terminology | 'Pooling' means both the no-trade profile and price pools under full orders | main.tex:1217, main.tex:1728, main.tex:1769 … | F12 |
| M02 | Mid | caption | Figure 2 labels use v and u for order magnitudes, and neither is defined in the notes | main.tex:875, main.tex:847, main.tex:877-896 … | F05 |
| M07 | Mid | notation | The Nash-bargaining proofs write the transfer as P (the stock price), the fallback as z (the noise) and the winning value as V | main.tex:441-442, main.tex:1120, main.tex:2309-2318 … | F06 |
| M09 | Mid | notation | lambda_X is a posterior, but finance readers take lambda for Kyle price impact | main.tex:2114, main.tex:2119, main.tex:2176-2180 … | F07 |
| M11 | Mid | terminology | 'Buyer' names the challenger, the incumbent, any bidder and a share-buying investor; the investor is also called 'trader' | main.tex:131-142, main.tex:195, main.tex:278 … | F13 |
| M13 | Mid | notation | Certified-node index j is undeclared, switches to roman a/b/c, and is reused for mesh and grid; r_c collides with r_C | main.tex:796, main.tex:847-857, main.tex:881-883 … | F11 |
| M18 | Mid | notation | Symbols used before definition or never defined (m, M in Fig. 1 notes; q_H, q_L; events H, L; e(x); e_H; frak r; \mathcal R_T, \mathcal W) | main.tex:575-576, main.tex:599, main.tex:659 … | F40 |
| M20 | Mid | result-statement | Unqualified claim that the reversal survives complementary signals; entry falls in 10 of 25 grid cells | main.tex:140-141, main.tex:227-229, main.tex:1042-1048 … | F16 |
| M23 | Mid | caption | Four thresholds summarized as three objects; r_C has several names; Fig. 2 note omits the no-trade uniqueness bound | main.tex:881-883, main.tex:898-905, main.tex:1728 … | F52 |
| M28 | Mid | notation | Gross acquisition profit has four symbol families: g_H/g_L, G_theta(F), G_{theta,eta}, g_v(p,r) | main.tex:491-494, main.tex:513-514, main.tex:552-553 … | F28 |
| M30 | Mid | notation | Entry rule and candidate price are e_r(mu), P_r(mu) in (A.3) but e(mu), P(mu) in A.5 and the OA; e takes four kinds of arguments | main.tex:625-626, main.tex:633, main.tex:1521 … | F09 |
| M31 | Mid | notation | F is the incumbent CDF and noise CDF but also the per-unit residual convolution F_theta(s), F(s), F_epsilon(s) | main.tex:541-553, main.tex:1553-1606, main.tex:1633 … | F17 |
| M36 | Mid | notation | I, D, g, L, U, J and delta are reused locally for new objects (I is both the high-cost indicator I_y and the preparation indicator) | main.tex:2128, main.tex:2133-2134, main.tex:2198-2202 … | F27 |
| M38 | Mid | notation | B_r loses or changes its strength subscript: B(.), B_p(m) and B_{p,r} | main.tex:492, main.tex:2622, main.tex:2631 … | F23 |
| M39 | Mid | notation | Cost CDF H_C, components H_L, H_H and density h_C reuse the state label H and the locked high value h | main.tex:2057-2063, main.tex:2700, main.tex:2706 … | F22 |
| M40 | Mid | notation | Psi is U_L'(v;1,-v) in the paper but U_-'(v;1,-v) in the OA; A_± and epsilon, zeta carry two meanings | main.tex:1829, main.tex:2243, online_appendix.tex:429 … | F24 |
| M47 | Mid | cross-reference | The price-pooling result is numbered twice (Prop. A.10 and Prop. OA.3) with different wording | main.tex:1403, main.tex:2522-2527, online_appendix.tex:280 … | F32 |
| M49 | Mid | terminology | The margin E has four names (entry, preparation probability, participation, investigation), and 'entry' is used before it is defined | main.tex:138, main.tex:235, main.tex:238 … | F55 |
| M54 | Mid | cross-reference | OA table captions cite 'Table 3'/'Table 4', which collide with the OA's own table numbers | online_appendix.tex:2200, online_appendix.tex:2269, online_appendix.tex:2568 … |  |
| M32 | Low | notation | The noise survival function has two symbols (\overline F_Z, S_Z), and S also means a generic signal, a value class and (sans-serif) the sale probability | main.tex:1666-1667, main.tex:1695-1721, main.tex:2505 … | F20 |
| M33 | Low | notation | The bar decoration has several meanings (bounds, survival function, unconditional entry, pooled posterior); the pooled posterior has two symbols | main.tex:541-542, main.tex:1907, main.tex:2251 … | F21 |
| M34 | Low | notation | The ± subscript means signal realization and also bound in mu_±; subscripts on mu carry five roles | main.tex:598, main.tex:1517, main.tex:1814 … |  |
| M35 | Low | notation | One-step constants A, w, y, t reuse letters with paper-wide meanings | main.tex:1917-1927, main.tex:1984-1993, online_appendix.tex:740-743 … | F26 |
| M37 | Low | notation | Font-only distinctions: \mathbb E / \mathsf E / \mathcal E and others; the locked E takes subscripts and arguments inconsistently | main.tex:455, main.tex:769, main.tex:852 … | F29 |
| M41 | Low | notation | The conditional crossing probability is alpha_theta in the benchmark, I_y in main A.5 and Q_{theta,y} in the OA signal economy | main.tex:767, main.tex:2127-2134, online_appendix.tex:570 … | F18 |
| M44 | Low | notation | T_eta takes (R,theta) in eq. (14) but (R,v) in C.7, and the OA derivation calls it P | main.tex:1124, online_appendix.tex:3097, online_appendix.tex:1067 | F04 |
| M51 | Low | notation | Lemma OA.2 redefines mu_- and mu_+; omega and pi each have two meanings in the OA | online_appendix.tex:816-825, online_appendix.tex:845, online_appendix.tex:2352-2353 … | F25 |
| M59 | Low | result-statement | The deviation qualifier drifts between 'every continuous deviation' and 'every continuous unilateral deviation', and 'continuous' understates the deviation set | main.tex:220, main.tex:480-481, main.tex:724 … | F37 |
| M61 | Low | caption | Figure captions omit the result-status interpretation required by E.4 | main.tex:574-578, main.tex:805, main.tex:967-975 … |  |
| M64 | Low | notation | Greek letters name derived objects: alpha_H/alpha_L, tau, Psi, Gamma_H, phi_±, zeta, delta_j, lambda_X | main.tex:758-770, main.tex:1829, main.tex:2114 … | F44 |
| M65 | Low | notation | \mathfrak r(d) uses the buyer's accuracy d as a dummy; the no-trade uniqueness bound \mathfrak r(k) has no r_ label | main.tex:900, main.tex:1021, main.tex:1734-1736 … | F41 |
| M66 | Low | cross-reference | Condition labels (A1)-(A3) collide with equations (A.1)-(A.3), Propositions A.1-A.3 and Appendix sections A.1-A.3; the OA cites them as unlinked text under one tag (OA.1) | main.tex:698, main.tex:703, main.tex:708 … | F35 |
| M71 | Low | notation | Reserve-derivative notation differs: d mu_theta/dp and de_theta/dp in (A.53)-(A.54) vs partial derivatives in two styles and d bar e_theta/dp in OA.54-56 | main.tex:2695, main.tex:2707, online_appendix.tex:1312 … | F09 |

## Class A: mechanical fixes

| Id | Severity | Category | Finding | Locations | Talk audit |
|---|---|---|---|---|---|
| M01 | Mid | result-statement | Introduction states the price-access gain at any fixed strength; Prop. A.9 holds only at r_1 | main.tex:233-235, main.tex:1060-1068, main.tex:2349-2357 | F15 |
| M14 | Mid | notation | Upper end of incumbent support is \bar r in Prop. 1 but R_max in Sec. 6.2 and Prop. A.8 | main.tex:542, main.tex:551, main.tex:1114 … | F19 |
| M21 | Mid | result-statement | Text calls Table 2's controls 'fixed-profile controls'; the price-hidden rows are reoptimized analytical equilibria | main.tex:810, main.tex:814-817 | F08 |
| M22 | Mid | status-label | Frozen-order entry numbers printed in the text without their numerical-diagnostic status | main.tex:817-818 | F50 |
| M26 | Mid | result-statement | Prop. A.5 and Lemma OA.2 extend all of Prop. 2 under (A1)-(A3), dropping the 'parts (i) and (ii)' qualifier | main.tex:951-952, main.tex:2003-2010, main.tex:2052-2054 … | F47 |
| M45 | Mid | cross-reference | Hyperlinks point to Markdown-era or repository files that do not exist in the LaTeX build; C.8 still speaks of placeholders | main.tex:893, main.tex:976, online_appendix.tex:3126-3128 … |  |
| M46 | Mid | cross-reference | C.2 says to compute r_C 'from A.5', but the OA never defines r_C | online_appendix.tex:654, online_appendix.tex:2278, online_appendix.tex:2280 … |  |
| M50 | Mid | cross-reference | Section numbers A.1-A.8 name different sections in the paper appendix and the OA, and the OA mixes the two | online_appendix.tex:491, online_appendix.tex:1826, online_appendix.tex:1981 … |  |
| M53 | Mid | cross-reference | OA B.6 says certificate precision and mesh are in C.2, but C.0 declares them | online_appendix.tex:1826, online_appendix.tex:1932-1934, online_appendix.tex:2271-2295 | F33 |
| M16 | Low | notation | Subscripts H/L are value states except in c_H and c_L, where they are cost levels | main.tex:407-410, main.tex:625, main.tex:697-707 … | F30 |
| M19 | Low | result-statement | Introduction states coexistence generally; it is established only at three certified strengths | main.tex:229-233, main.tex:845-861, main.tex:916-917 … | F48 |
| M42 | Low | notation | Logistic-noise and full-order posterior objects are decorated inconsistently within Appendix A and between the paper and the OA | main.tex:1652, main.tex:1966, main.tex:1970 … | F43 |
| M43 | Low | notation | W is pointwise gross ownership value in the paper but expected net surplus in the OA, in two fonts | main.tex:2337, main.tex:2339, main.tex:2388 … |  |
| M58 | Low | result-statement | Sec. 6.2 states the bargaining spread effect as signed; Prop. A.8 says 'weakly' | main.tex:1129-1132, main.tex:2302-2307 | F49 |
| M60 | Low | number | Signal accuracies shown as percentages in the text but as probabilities in A.8, tables and C.0; parameter displays break shortest-exact-decimal | main.tex:854, main.tex:1042, main.tex:2759 … | F53 |
| M62 | Low | terminology | The fixed-experiment control goes by six names | main.tex:139, main.tex:224, main.tex:303 … |  |
| M63 | Low | notation | Compound and one-shot shortcuts used fewer than five times | main.tex:552, main.tex:1120, main.tex:1730-1785 … | F45 |
| M68 | Low | result-statement | A.8 declares two negative controls for the price-pool family; C.0 and A.11 declare four | main.tex:2777-2778, online_appendix.tex:1594-1611, online_appendix.tex:1949-1950 … | F51 |
| M69 | Low | result-statement | Unqualified 'unique outcome' in proofs breaks the house qualification of 'unique' | main.tex:1641-1642, main.tex:1743-1744, online_appendix.tex:685-686 |  |
| M70 | Low | terminology | The r_2 economy is 'very strong incumbent' in Table 2 but 'collapse' in the OA | main.tex:811, online_appendix.tex:1881, online_appendix.tex:2110 … |  |
| M72 | Low | notation | Euler's number e is written bare, (1+e)^{-1}, beside the entry function e | main.tex:2574, online_appendix.tex:1408, online_appendix.tex:1526 … | F42 |
| M73 | Low | style | Max brackets differ: max(p,R) in the OA vs max{p,R} in the paper, for identical equations | main.tex:1449, main.tex:2343, online_appendix.tex:326 … |  |
| M75 | Low | notation | phi_Y (capital) in C.3 vs phi_y elsewhere | online_appendix.tex:2513, online_appendix.tex:894, main.tex:2186 |  |
| M76 | Low | terminology | 'High-quality ownership' in the OA and manifest vs 'high-value (challenger) ownership' elsewhere | online_appendix.tex:574, online_appendix.tex:1989, online_appendix.tex:3408 … | F56 |

## Class C: coordinated updates outside the manuscript text (report only)

| Id | Severity | Category | Finding | Locations | Talk audit |
|---|---|---|---|---|---|
| M04 | High | notation | v is both the certified short magnitude and the challenger's realized value; V has further meanings | main.tex:447, main.tex:847-857, main.tex:1813-1832 … | F05 |
| M05 | High | notation | c is the preparation cost, the price-pool cutoff, the central-region centre and a cost integration variable | main.tex:407, main.tex:1917-1927, main.tex:2401 … | F03 |
| M10 | Mid | status-label | Matched dividend called an 'analytical invariance diagnostic' but its registry status is numerical diagnostic | main.tex:1089-1091, tables/table_matched_price.tex:32, online_appendix.tex:2195-2198 … | F10 |
| M25 | Mid | caption | The Table 2 note in the main paper prints margins zeta_L ... zeta_1 that are defined only in the OA | main.tex:811, main.tex:1582, online_appendix.tex:2124-2130 |  |
| M29 | Mid | notation | e_H, e_L are used before definition, mean both unconditional and price-conditional entry, and switch between barred and unbarred; bare e is also Euler's number | main.tex:625, main.tex:637, main.tex:1539-1540 … | F09 |
| M48 | Mid | result-statement | Prop. 2 claims a nonempty open set for all three parts; nonemptiness is proved only for (A1)-(A3), and the r_2 margins are unregistered | main.tex:721-722, main.tex:1002-1003, main.tex:1675-1686 … | F46 |
| M52 | Mid | cross-reference | Margin rows in the manifest and registry cite (OA.68), a derivative bound; the margins are (OA.77) | online_appendix.tex:1688, online_appendix.tex:2130, paper/quantity_manifest.csv:94-103 | F14 |
| M55 | Mid | result-statement | Exact-event table lists p_H outside its defining regime and omits the promised 6.280 reserve node | online_appendix.tex:2853, online_appendix.tex:3048-3053, online_appendix.tex:3066-3072 … | F57 |
| M27 | Low | terminology | Delta_T is called 'target-payoff spread', 'spread of target proceeds' and 'information spread' | main.tex:492, main.tex:544, main.tex:572 … | F36 |
| M67 | Low | number | Standardized logistic threshold printed with 6 decimals; C.8 requires decimal_9 | main.tex:957-958, online_appendix.tex:3158-3159, paper/quantity_manifest.csv:63 | F38 |
| M74 | Low | number | The binary-value alternative reserve p=1.01 (Table 4 Panel A) is not stated in Sec. 6.3 or A.8 and has no registry key | main.tex:1169, main.tex:1193-1195, main.tex:1204 … | F39 |

## Refuted on re-check

- M15 Delta is the target spread (subscript 'target'), the bargaining spread (subscript = eta) and a change operator: The evidence is partly wrong and what remains is intended and clear. (1) \mathcal W and \mathcal R_T are defined in main. The Table 2 note, which main.tex:811 includes via \input and which appears in Sec. 4.2 well before (A.41), says 'R_T e…
- M17 Reserve p, stock price P, strength r, incumbent value R and noise scale b reverse field conventions: The symbols are C.0-locked, and the paper glosses each at first use: main.tex:389-391 'Its acquisition value R is uniform on [0,r] ... An increase in r strengthens the incumbent'; main.tex:397-398 'the reserve p'; eq. (2) at main.tex:441-44…
- M24 Appendix A.2 sends readers to OA A.3 for null-set details, which are in OA A.1: In context, main.tex:1588-1590 closes the differentiation argument of the global order bound (A.5-A.6). That argument covers the absolutely continuous Laplace density, Fubini, and "|F_theta'|<=F_theta/b almost everywhere". The "null-set det…
- M56 Star decoration means 'threshold' on x* but 'optimal/selected' on p* and sigma*: p^* (main.tex:2470, 1 use) and \sigma^*(p) (2 uses, :2470 and :2475) follow the standard convention that a star marks an optimum or equilibrium selection. The notation rules list y^* as 'optimal'. x^* (17 main / 16 OA) is locked by C.0 and …
- M57 Prop. A.3 reuses the benchmark labels r_0, r_1 as arbitrary strengths: main.tex:1705 has "For \(r_1>r_0\), \(B_{r_1}(\mu)\le B_{r_0}(\mu)\)". In the paper r_0 and r_1 are not fixed to the benchmark values. Proposition 2 itself (main.tex:693) opens "Fix \(0<p<\ell<r_0<r_1<h\)" and treats them as a generic order…

## Not yet re-checked

- K01 Numerical-continuation branches in Sec. 4.3 stated as equilibria without their numerical-diagnostic status
- K02 Expected target proceeds R_T goes by four names
- K03 Online Appendix E and Sec. 6.3 mention review and audit process artifacts
- K04 Null-set details cited to Online Appendix A.3, but they are in A.1
- K05 Registry and manifest call Gamma_H 'nonnegative', but the certificate requires it strictly positive
- K06 The 'Unique' table column has three different definitions
- K07 Theorem margins printed to 3 significant figures, while C.8 fixes scientific_10 for margins
- K08 No-trade pooling margin at the certified nodes is enclosed but never reported
- K09 Log-odds written as log(tau/(1-tau)) and as undefined 'logit'; 'logistic' also used as a function
- K10 Exploratory reserve table prints renderer labels 'p L' and 'p H' as plain text
- K11 Mixed-strategy integrals written as d\sigma_H(q) in the paper and \sigma_\theta(dq) in the OA
- K12 OA result numbering shares one counter across lemmas and propositions, and the lemmas have no titles

## Coverage notes

- Figure PDFs were not opened. Axis labels, legends and panel annotations of Figures 1-4 were checked only through their notes and the M02 finding, not against the notation.
- The search-coverage counts in the exploratory reserve table (Panel B, class values r=1.2) show 155 unresolved nodes but only 136 unresolved candidates, while every other row has equal counts (116/116). This may be a count or column inconsistency, but its definition depends on the numerics ledger (numerics/reserve_ranges.csv), which I did not open.
- M45 also applies outside C.8, and I did not report these as new findings. Placeholder or Markdown-era language remains at online_appendix.tex:1859 (C.0 'quantitative placeholder fields'), 2098, 3148, 3533 (E.1 'filled Markdown, LaTeX ... are regenerated'), 3657 and 3669 (E.3 substitution of placeholder keys), although the .tex masters now carry literal numbers.
- Proof mathematics was spot-checked only: formulas (4), (12), (14), (A.11)/(OA.20), (A.46)-(A.49) and the OA B.2 concavity step all reproduce. OA A.2-A.3, A.7-A.10, B.3-B.5, C.2 and C.5-C.7 were not read line by line.
- Bibliographic details (volumes, pages, DOIs) were not checked against external sources. I verified only that the citations and the reference list match, with 21 of 21 in main and 1 of 1 in the OA.
- Talk finding F31 (p/P/r/R/b reverse field conventions, locked by C.0) is not in the verified list, but the talk audit concluded that no paper change is needed, so I did not report it.
- Textual cross-references were checked in main.tex (Section, Appendix and Online Appendix targets) and all resolved correctly except F34. The OA's own self-references (the 'Appendix C' vs 'Section C.6' wording, and 'Sections B and C' at online_appendix.tex:183, which omits D and E) were not reported beyond M50.
- OA Section D (empirical pilot) was read, and no notation or status inconsistencies were found beyond M76 ('High-quality ownership') and M49 ('investigate').

Each finding's evidence, use counts and exact fix are in `findings.json`.
