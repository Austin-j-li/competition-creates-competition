# S11. The comparison note

Report of the production assistant to the coordinator. Nothing is committed. The only changed file is `slot/manuscript/comparison.tex` (decision 8: status labels and method sections removed, then recast). It falls from 737 to 317 lines and from 16 to 7 pages. Every build product sits outside the repository.

## Structure

- Title: "The order slot and Laplace noise: two trading stages for Competition Creates Competition"; date 25 October 2026; `pdftitle` matches.
- Opening (two paragraphs): the two trading stages; the Laplace set-up identified once as the trading stage of the manuscript of 22 October 2026 with the same title; the citation convention. Numbers without a prefix are the paper's; the prefix L marks the Laplace manuscript's own numbers (Proposition L-2, Proposition L-A.5, Table L-5, Section L-7, Online Appendix L-A.13). Laplace strengths carry the superscript Lap (macro `\Lap`); the Laplace noise scale is ξ.
- Section 1, the two set-ups: shared primitives and the example (by its primitives, through `\reg`); the order slot, described with the paper's words (the alternative-arrival structure of Dow and Gorton 1997; the unit menu, presence and cost of Edmans, Goldstein and Jiang 2015); the Laplace set-up; Table 1 (ten rows: menu, what hides the order, what market makers see, likelihood ratio, posterior bounds, price and belief, the investor's problem, the trading bound, primitives each adds, tie rules in the four phrases); one paragraph on what the two share and where the investor's problem differs.
- Section 2, results side by side: Table 2 (longtable, ten rows, slot column first), then one paragraph per row: beliefs and prices, Proposition 1, Proposition 2 (with the example's region), fixed information, Proposition 3, Proposition 4, robustness, welfare, empirical predictions.
- Section 3, what separates the two set-ups: the order menu (partial sale against mixtures; the object that carries the rise of entry), the number of prices (step entry, fixed information, reserve deterrence, a finite equilibrium list), what the market observes (one opportunity against the net demand of the decision interval; the tie at r_C).
- References: the two cited works.

## What was removed

- Every status label (56 at S3): "analytical", "computer-assisted", "numerical diagnostic", "certified", "open" as a status, the "Status." paragraph and the status sentence of the opening.
- The method sections: the proof method (old §4, lines 365–600: the explicit object, verification against the fixed object, uniqueness through bounds, strict margins, certificates for finite steps, the worked proof of Proposition 2(iii) in both set-ups with its margins table), the checklist (602–619), "Where each set-up stands against the standard" (622–702, with the thin-margins table) and the decision points (705–731).
- Version-history framing: "the slot replaces three certified points", "the earlier", the manuscript-dating paragraph with "every slot number comes from the project registry ... independent outward recomputation", "Calibration B" (paragraph heading and text), "benchmark" (21 lines), "calibration" (3 lines).
- The macros `\rUR`, `\fr`, `\lap`, `\slo`; the sentence that explained `\rUR`.
- The tie codes IM, I0, C1, CM (16), replaced by the four phrases of NOTATION part (b).
- Note-only symbols that collided with the paper (NOTATION part (d), S11): Laplace scale b → ξ; noise demand Z, flow X = q + Z, density f, residuals A_H, A_L, Ā, A(M), β*, e*, Π_L, sale size v, separation γ → words (the sale sizes are stated as fractions of a unit; f appears once, as "the noise density f"); S for the price gap → "the price gap P(1) − P(−1)".
- Retired vocabulary: "no trade" (noun) → quiet market; "informative equilibrium" → informative market; "trade bound" → trading bound; "threshold flow" → "the flow at which the posterior reaches τ"; "execution spread" → price gap; "admissible region", "admissible slots" → the example's region, Corollary 1; "the exclusion reserve" → "the reserve that excludes the low class"; "buyer" for the challenger → the challenger.
- Superseded slot claims: the research branch ending at r_λ̄ and "the equilibrium set with research on (r_N, r_U^R)" (and the key `res_rUR`); "Proposition A.3 ... under rule C1" for every experiment (now stated as Proposition A.2); the conditional execution spread S and identification of (ϑ, λ, β) "among admissible slots"; the coexistence margin at π_max when an indifferent high-cost challenger may prepare with any probability.

## What each row of Table 2 cites (slot column against the S0 baseline)

| Row | Slot citation in the recast note | S0 label | Laplace citation (kept from the note) |
|---|---|---|---|
| Beliefs and prices | Lemmas A.1, A.2, A.3, A.4; Lemma A.5 in the paragraph | Lemmas A.1–A.3 unchanged; A.4 `lem:reduction` and A.5 `lem:twonumbers` are new labels (S0 had A.4 = `lem:a4-path`, A.5 = `lem:a4-order`) | Propositions L-A.1, L-A.2; equation L-11 |
| Proposition 1 | Proposition 1 | 1 | Proposition L-1 |
| Proposition 2 | Proposition 2 | 2 | Proposition L-2 |
| The example's region | Corollary 1, Table 2 | Proposition A.1 `prop:region` → Corollary 1 (decision 7); Table 2 unchanged | Appendix L-A.4 |
| Fixed information | Proposition A.2 | A.3 `prop:control` → A.2 | Proposition L-A.3 |
| Proposition 3 | Proposition 3, Corollary 2, Corollary A.2; Table A.3 in the paragraph | Proposition 3; `cor:example-coexistence` is the new Corollary 2; Corollary A.2 `prop:priors` and Table A.3 unchanged | Propositions L-3, L-A.4 |
| Proposition 4 | Proposition 4, Corollary 3, Proposition A.1 | Proposition 4; `cor:research` is the new Corollary 3; A.2 `prop:researchregion` → A.1 | none |
| Robustness | Propositions A.3, A.4, A.5, A.6; Table A.4 | A.4 → A.3, A.5 → A.4, A.6 → A.5, A.7 → A.6; Table A.4 unchanged | Propositions L-A.6, L-A.5, L-A.7; Online Appendix L-A.13; Table L-4 |
| Welfare | Propositions A.7, A.8, A.9; Table 5 | A.8 → A.7, A.9 → A.8, A.10 → A.9; Table 5 unchanged | Propositions L-A.9, L-A.8; Table L-5 |
| Empirical predictions | Section 8; Propositions A.10–A.13 | A.11 → A.10, A.12 → A.11, A.13 → A.12, A.14 → A.13 | Section L-7 |

Section 3 of the note cites Corollaries 2 and 3, Table A.3, Proposition A.9(b), Section 8 and Online Appendix L-B.2. Printed numbers come from the label map of the current build (139 labels): `prop:region` prints 1 (Corollary 1, full form), `cor:example-coexistence` 2, `cor:research` 3, `prop:priors` A.2 (a corollary), `prop:researchregion` A.1, `prop:control` A.2 through `prop:announcement` A.13, `lem:reduction` A.4, `lem:twonumbers` A.5, `tab:a4-ties` A.3, `tab:classes` A.4, `tab:region` 2, `tab:reserves` 5.

## Laplace results: how each status-worded claim now reads

- Proposition L-3 (three strengths, "computer-assisted"): stated plainly as an equilibrium with a full purchase and a partial sale at 1.55, 1.60 and 1.65, each beside the quiet market, with the sale sizes and the strictly rising entry.
- The branch between the three strengths ("numerical diagnostic") and the full correspondence ("open"): left out. The scope sits in the claim: "between these strengths, Proposition L-3 gives, at 1.55, 1.60 and 1.65, ...".
- Fixed information (closed forms; the Laplace table labelled them a diagnostic): stated plainly, entry falls strictly from 0.562178 to 0.522757, with the reason the note gave.
- Break-even trade scale ("numerical diagnostic"): stated as what the example shows, "in the Laplace example the corresponding scale is 1.831923".
- Every other Laplace claim keeps its content from the note, with the status word removed. No Laplace result is added; the one sentence of new reasoning is that a quiet market ends at the same strength r_N in both set-ups, because against an uninformative price an order of size s earns s(ρΔ_T/2 − k) at the prior 1/2 in both (the numbers `rN` and `lap_rN` agree).

## Numbers

Every number prints through `\reg`; no typed decimal or fraction remains (the margins tables that typed 1/4, 3/4, 6, 1/50, 0.1 and 1 are gone; the half-width prints through `atom_eps`). All keys exist in `numbers.tex`; the build prints no unknown key. The note uses 107 keys, against 145 before. Seven keys are added: `atom_eps`, `res_cap`, `res_entry_cap`, `res_entry_rR`, `res_rQ`, `share_H_r0`, `share_H_r1_B`. Forty keys leave with the removed sections: the margins and worked-proof keys (`lap_return_*`, `lap_margin_A2_*`, `margin_*` of the two margins tables, `gap_r2_rC_B`, `lap_r2_minus_rC`, `lap_spread_increase`, `lap_gH_r2`, `lap_gL_r2`, `lap_Delta_r0`, `lap_Delta_r2`, `tau_r2_frac`, `price_r2_*_B`), the Laplace Proposition 3 bounds (`lap_P3_GammaH_*`, `lap_P3_pool_*`, `lap_P3_psi_*`, `lap_P3_thr_r155`), the threshold-pair entries `entry_th_r1*_B`, `margin_cmend_B`, `res_rN` and `res_rUR`. Five Laplace keys whose value equals a slot key the sentence already prints are not repeated: `lap_M_half` (= `M_half_B`), `lap_m_half` (= `m_half_B`), `lap_entry_r1` (= `entry_r1_B`, "entry ... in both"), `lap_reserve_excl_p` (1.01 = `rsv_points_excl`, "at this reserve"), and `lap_rC` (= `rC_B`, "the entry ceiling ... is the same number in the two set-ups"). No key was renamed. The marked strengths, the prior cut points and the lower end of the informed-share interval print with ≈, as in the paper.

## Build

From `slot/manuscript`: `latexmk -pdf -interaction=nonstopmode -outdir=<private folder>/cbuild comparison.tex`. Exit 0; 7 pages; the log has no unknown key, no undefined reference or citation and no overfull box; the text has no "??"; no Type 3 font. Every page was read as an image at 80 dpi. The paper itself was built the same way into the private folder for the label map (exit 0).

## Language scan

`language_scan.py --no-doc --no-figcode --extra slot/manuscript/comparison.tex`: total 0 counted hits; 4 allowed tie-rule phrases ("may mix" three times, "may prepare with any probability" once). The first pass found 3 counted hits, each rewritten: "run from ... to" (process word) → "lie between ... and"; "Section 3.4" (typed reference) and "Section L-4.2" (typed decimal) → dropped, the lemma and the appendix citation remain.

A manual grep for the retired vocabulary of NOTATION part (b) and the rule-3 words finds only: "open set" twice ("a nonempty open set", mathematics, not a status), "the auction enters orders, posteriors, entry and research" (not the challenger's act), and "manuscript"/"superscript" (substring matches of "script"). Judged compliant.

## Points for the coordinator

- The note identifies the Laplace manuscript by its date, once, as the brief asks; it never narrates a change between the two.
- Scope qualifiers carried into the prose: the default tie rules on the research equation (Proposition 4), the hypotheses Δ_T > 0 and g_H > g_L on the reduction lemma (Lemma A.4), and full two-sided trade with the class-win condition on the winner prediction (Proposition A.12).
- One sentence on the Laplace side is reasoning, not transcription: a quiet market ends at the same r_N in both set-ups, because against an uninformative price an order of size s earns s(ρΔ_T/2 − k) at the prior 1/2 (constant price, entry ρ after every flow, linear payoff). The coordinator may strike it to keep the Laplace side purely transcribed.
- Keys no longer used by the note (45, listed under Numbers; the `lap_*` keys most likely have no other consumer) will show as orphans at S12 and need a keep-or-retire decision there.
- Cross-references to the paper are typed (the note is a separate document). They follow the current label map and need a recheck only if a number moves before S12.
