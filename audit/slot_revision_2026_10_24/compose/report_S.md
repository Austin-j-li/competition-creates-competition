# Report S: Remove the result-status vocabulary from the manuscript

## Outcome

The status vocabulary is out of the manuscript. No hypothesis, conclusion, number, inequality, or quantifier changes.

- Branch: `t3/remove-result-status-vocabulary`, based on `c78e2c3`
- Commit: `80804f05afa65aa473d2544b26169f4530b9ab83` ("Remove the result-status vocabulary from the manuscript", with the `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` trailer)
- Not pushed.
- Diff: 15 files changed, 107 insertions, 118 deletions.
- No `\label`, `\eqref`, `\cite`, or `\reg{}` in retained text changes. The only `\ref{}` occurrences that leave sit inside the two method sentences after Propositions 3 and 4, which the brief names for deletion.
- The abstract in [main.tex](slot/manuscript/main.tex) needs no edit. It has no status word. Its one "open" is the mathematics in "open set of parameters".

## Changes by file

Main text, in [slot/manuscript/sections](slot/manuscript/sections):

- [03_competition_information.tex](slot/manuscript/sections/03_competition_information.tex): Proposition 1 title loses "; analytical".
- [04_equilibrium_results.tex](slot/manuscript/sections/04_equilibrium_results.tex): Proposition 2 title loses "; analytical". Proposition 3 title loses "; computer-assisted". The method sentence after Proposition 3 goes (see the deleted list).
- [05_research.tex](slot/manuscript/sections/05_research.tex): Proposition 4 title loses "; part (a) analytical, part (b) computer-assisted". The appendix pointer loses ", with its status". The method sentence after Proposition 4 goes. Three "(computer-assisted)" tags come out: at the research branch interval, at \(r_U\), and at the pointer to the admissible-region proposition. The "open" sentence and the figure note change (see below).
- [06_robustness.tex](slot/manuscript/sections/06_robustness.tex): The appendix pointer loses ", with its status". Eleven tags come out: four ", analytical" or "(analytical)" tags at the propositions on cost laws, classes, many classes, and signals, and seven "(computer-assisted)" tags at the benchmark cost law, the class table, the four-class economy, the price collision, and the three signal computations.
- [07_welfare.tex](slot/manuscript/sections/07_welfare.tex): Three "(analytical)" tags come out. The appendix pointer loses ", with their status". Three benchmark-value tags come out. Two "(computer-assisted; Appendix...)" parentheticals become "(Appendix...)". The reserves table note loses "Values are computer-assisted." The payment-rule scope sentence changes (see below).
- [08_empirical.tex](slot/manuscript/sections/08_empirical.tex): The appendix pointer loses ", with its status". Four ", analytical" tags come out. Six "(computer-assisted)" tags come out at benchmark values. The selection clause in the two-cluster paragraph goes (see below).
- No edit in [01_introduction.tex](slot/manuscript/sections/01_introduction.tex), [02_model.tex](slot/manuscript/sections/02_model.tex), or [09_conclusion.tex](slot/manuscript/sections/09_conclusion.tex). These files hold no status word. The conclusion already phrases the seller's choice of terms as the next step: "The next theoretical step is the seller's choice of terms with the whole pricing and trading continuation retained." That sentence stays, word for word.

Appendix, in [slot/manuscript/appendix](slot/manuscript/appendix). Proof method stays in every case: the Sturm counts, the rational brackets, the outward interval arithmetic, the enclosures of \(\eu\), every script name, every run log, and every certificate paragraph.

- [A1_payoffs.tex](slot/manuscript/appendix/A1_payoffs.tex): The status-list sentence at the head goes. The named Proposition 1(c) title loses "; analytical".
- [A2_beliefs_trading.tex](slot/manuscript/appendix/A2_beliefs_trading.tex): Four lemma and corollary titles lose "; analytical". The conventions item now reads "A step that uses a script names the script and its run log." The script and run-log discipline stays.
- [A3_proposition2.tex](slot/manuscript/appendix/A3_proposition2.tex): The admissible-region proposition title loses "; analytical".
- [A4_coexistence.tex](slot/manuscript/appendix/A4_coexistence.tex): Six titles lose their tags. The full statement of Proposition 3 becomes "(full statement)". At the end of the path-lemma proof, "Parts (b) and (c) rest on the exact Sturm counts." now closes the proof, and "Parts (a) and (d) are proved by hand" stays. The cross-check sentence now reads "This cross-check enters no step of the proof." The sentence on the corollary's certificates goes (see the deleted list).
- [A5_research.tex](slot/manuscript/appendix/A5_research.tex): Six lemma and proposition titles lose their tags. The paragraph head "The branch at calibration B (computer-assisted)." becomes "The branch at calibration B." The grid-scan sentence now reads "This scan enters no proof." The grid scan itself, and its script and run log, stay.
- [A6_robustness.tex](slot/manuscript/appendix/A6_robustness.tex): Five proposition titles lose "; analytical". Six paragraph heads lose "(computer-assisted)". The class-economy table note loses "Values are computer-assisted."
- [A7_welfare.tex](slot/manuscript/appendix/A7_welfare.tex): Three proposition titles lose "; analytical". The paragraph head "The benchmark reserves (computer-assisted)." becomes "The benchmark reserves."
- [A8_empirical.tex](slot/manuscript/appendix/A8_empirical.tex): Five proposition and corollary titles lose "; analytical". The Certificates paragraph loses its first, status-sorting sentence. It now opens with "The values come from the script ... It computes every value in interval arithmetic at 60 digits ...", so the computation account stays whole.
- [A9_parameters.tex](slot/manuscript/appendix/A9_parameters.tex): The declarations table keeps its input-versus-derived distinction without the status words. The column head "Status" becomes "Kind". The three "computer-assisted" entries become "derived". The lead sentence now reads "an *input* is a declaration, and a derived value follows from its definition." The signal-vector sentence now ends "each an input."

## Sentences deleted

Each sentence below did status work only. The text around each one stays.

1. After Proposition 3: "Two monotonicity steps of the proof rest on exact Sturm counts, and every other step is analytical (Appendix...)." The appendix proof already names the Sturm counts.
2. After Proposition 4: "The equilibrium lists of part (b) follow from analytical arguments, and exact rational and interval arithmetic settles the strict signs at the benchmark (Appendix...)." The appendix proof already names the arithmetic.
3. In the research section: "On \((r_N,r_U)\), the equilibrium set with research is open."
4. In the empirical section, a clause: ", and which equilibrium a process selects is open." The sentence now reads "processes can form two clusters." The two sentences after it describe both clusters.
5. In the appendix head: "Each statement carries its status once: analytical, computer-assisted, numerical diagnostic, or open."
6. At the end of the existence-at-every-prior proof: "The certificates of Lemma [path] make the corollary computer-assisted."
7. In the Certificates paragraph of the empirical appendix: "The benchmark values of this subsection are computer-assisted, except the band endpoints, the share bounds ..., the incentive margin of the band and the two low-class sale payoffs, which are analytical."
8. In two table notes: "Values are computer-assisted." One note sits under the reserves table. One sits under the class-economy table.
9. In four appendix pointers, the status clause only: ", with its status" in the research, robustness, and empirical sections, and ", with their status" in the welfare section. Each pointer still sends the reader to the full statement and proof.

## Sentences rewritten as positive scope

1. The payment rule. Before: "Proposition [payment] (analytical) isolates this dependence at the payment stage, in a verifiable-value institution with zero reserve; the trading and preparation equilibrium under this rule is open." After: "Proposition [payment] isolates this dependence at the payment stage, in a verifiable-value institution with zero reserve." The payment-stage scope states what the result covers.
2. The research figure note. Before: "The gray band marks the strengths at which the equilibrium set with research is open, and the horizontal axis is broken there." After: "The gray band marks the interval \((r_N,r_U)\) between the two cap ranges, and the horizontal axis is broken there." The sentence before it in the note states the two cap ranges: from \(\bar r_R\) to \(r_N\), and above \(r_U\). The note now names the band by its endpoints.
3. The conclusion needs no rewrite. It already carries the seller's choice of terms as the next theoretical step (see above).

## Remaining grep hits, and why each stays

Command: `grep -niE "analytical|computer-assisted|numerical diagnostic|diagnostic|status|\bopen\b" slot/manuscript/main.tex slot/manuscript/sections/*.tex slot/manuscript/appendix/*.tex`

Output: 20 lines. Every hit is the word "open". No line contains "analytical", "computer-assisted", "diagnostic", or "status".

Mathematics, "open set" and its variants (13 lines):

- [main.tex:91](slot/manuscript/main.tex:91): "On an open set of parameters" in the abstract.
- [01_introduction.tex:34](slot/manuscript/sections/01_introduction.tex:34): "a nonempty open set of primitives".
- [04_equilibrium_results.tex:60](slot/manuscript/sections/04_equilibrium_results.tex:60): "so they define an open set".
- [04_equilibrium_results.tex:151](slot/manuscript/sections/04_equilibrium_results.tex:151): "Each region is the exact open set on which (H1)--(H3) hold".
- [06_robustness.tex:29](slot/manuscript/sections/06_robustness.tex:29): "a nonempty open set of strengths and costs".
- [09_conclusion.tex:9](slot/manuscript/sections/09_conclusion.tex:9): "on an open set of primitives".
- [A3_proposition2.tex:149](slot/manuscript/appendix/A3_proposition2.tex:149): the paragraph head "The open set."
- [A3_proposition2.tex:151](slot/manuscript/appendix/A3_proposition2.tex:151): "They define an open set in the domain".
- [A6_robustness.tex:159](slot/manuscript/appendix/A6_robustness.tex:159): "a nonempty open set of strengths and costs".
- [A7_welfare.tex:239](slot/manuscript/appendix/A7_welfare.tex:239): "outside the open sets of the proposition".
- [A9_parameters.tex:251](slot/manuscript/appendix/A9_parameters.tex:251): the paragraph head "Open parameter sets."
- [A9_parameters.tex:252](slot/manuscript/appendix/A9_parameters.tex:252): "The open-set statement concerns the sufficient conditions".
- [A9_parameters.tex:254](slot/manuscript/appendix/A9_parameters.tex:254): "these rows define an open set of primitives".

Mathematics, "relatively open", "open interval", and "open band" (5 lines):

- [A3_proposition2.tex:152](slot/manuscript/appendix/A3_proposition2.tex:152): "the set is relatively open".
- [A3_proposition2.tex:166](slot/manuscript/appendix/A3_proposition2.tex:166): "the band is an open interval of \(\lambda\)".
- [A3_proposition2.tex:168](slot/manuscript/appendix/A3_proposition2.tex:168): "The open band is exactly the set on which the strict hypotheses hold".
- [A3_proposition2.tex:198](slot/manuscript/appendix/A3_proposition2.tex:198): "the band is an open interval of \(\lambda\)".
- [A9_parameters.tex:255](slot/manuscript/appendix/A9_parameters.tex:255): "the set is relatively open in the model domain".

Ordinary English, with no link to result status (2 lines):

- [02_model.tex:7](slot/manuscript/sections/02_model.tex:7): "an open contest can create such an interval". The phrase describes a sale process that still admits a further bidder. It names the economic setting, not the state of a proof.
- [04_equilibrium_results.tex:305](slot/manuscript/sections/04_equilibrium_results.tex:305): "Filled markers belong to a branch, and open markers do not". The phrase describes unfilled symbols in a figure, as against filled ones.

## Check results

All runs use the manuscript through its own build interface. No tests were written or run.

1. Build: `cd slot/manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/ccc_slot_scan/build_status main.tex` exits 0. The log ends with "Output written on /private/tmp/ccc_slot_scan/build_status/main.pdf (102 pages, 734446 bytes)."
2. Log scan: `grep -E "undefined|multiply" /tmp/ccc_slot_scan/build_status/main.log` prints nothing. The grep exits 1, as a no-match grep does. No reference is undefined, and no label is multiply defined.
3. Number scan, from the repository root: `python3 audit/slot_manuscript_2026_10_23/scripts/_coordinator/number_scan.py` prints "files scanned: 21; distinct keys used: 676; missing keys: 0" and "literal decimals outside \reg: 0". It exits 0.
4. Final vocabulary grep: 20 hits, each listed above. Each hit is mathematics or ordinary English.
5. Rendered-output read: `pdftotext` on the built PDF, then a grep for "analytical", "computer-assisted", "numerical diagnostic", "diagnostic", and "status", finds no hit. A grep for "is open" and "are open" also finds no hit.
6. `git diff --check` reports no whitespace error.

Scope note on verification: this edit touches manuscript prose only. It changes no numerical exercise, no registry value, and no derived artifact. The checks above cover the change: the manuscript build, its cross-references, and its number discipline. The full numerical pipeline gates do not run here. Do not read this report as a full pipeline pass.
