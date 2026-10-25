# Notation and vocabulary

Frozen at S3 on 25 October 2026, on the work branch `theory-upgrade`. Every later stage writes with these choices: the mathematics writer in S4 to S6, the production assistant in S6, S7 and S11, and the prose writer in S8 to S10. Where `lens_theory.md` 3.6, `lens_maintext.md` 3.6 or `SCAN.md` Part 3 chose otherwise, this file decides, and the row says "differs from the lens plans". A change after S3 goes through the coordinator and is entered here with its date.

Line numbers refer to the files on this branch after the S3 edits. Every S3 edit kept each file's line count, so the line anchors of the lens plans and the referee reports still hold. `progress/S3_draft.md` lists the S3 edits.

Contents: (a) the rule card; (b) vocabulary; (c) symbols; (d) renames by stage and file.

## (a) Rule card

The seven rules of `PLAN.md` Part 2, in full. They bind the manuscript, the comparison note, the slides, figure labels, committed project documents and commit messages. The repository's own instructions ask for status words; rule 1 overrides them. Style guide sections 2.4 and 2.7, and the style guide's advice to say "the benchmark", are void. Example sentences are LaTeX source as it would stand in the manuscript.

### Rule 1. No status labels

> No status labels anywhere in the manuscript, the comparison note or the slides: no "analytical", "computer-assisted", "numerical diagnostic", "certified", or "open" as a status, in titles, sentences, table notes or captions. Style guide sections 2.4 and 2.7 on status are void. A proof may name its method as mathematics ("an exact rational computation shows").

Compliant:
1. `Exact rational arithmetic gives every inequality in this step, and rational bounds on each square root give the research roots.`
2. `Rational interval bounds give \(\lambda_E(r)<\lambda_R(r)<\lb\) at each of the three intermediate strengths.`

### Rule 2. No defensive writing

> No defensive writing. Scope sits inside the claim. A condition is a hypothesis, stated once. No caveat or reassurance paragraphs, no hedges, no answers to imagined referees, no paragraph that ends on a limitation.

Compliant:
1. `If class \(H\) outbids every incumbent on the path, high-class ownership rises along the recruiting branch.`
2. `Wherever the recruiting branch is an equilibrium, entry rises strictly with \(r\).`

Violating, `appendix/A5_research.tex:241–243`:
> The general statement behind this part needs both \(\DT(r)<k\) and \(B_r(1/2)<c_H\): with \(c_H\) small enough that \(B_r(1/2)>c_H\), zero research is still unique, but both cost types prepare and entry is one.

It answers an imagined objection after the proof and ends the part on a limitation. Rewrite, with the scope inside the claim:
> Zero research is the unique equilibrium whenever \(\DT(r)<k\). Entry is then \(\rho\) if \(B_r(1/2)<c_H\), and one if \(B_r(1/2)>c_H\).

### Rule 3. No development-log writing

> No development-log writing. The paper reads as written once. No narration of its own changes ("now", "no longer", "new", "updated", "revised", "corrected", "replaces", "in this version", "previously", when they refer to the paper), no announced upgrades, no process words (registry, script, exercise, checker, certificate, run, verified, file names, keys, "calibration B", weakness codes), no bookkeeping about checks. Comparative statics across strengths stay.

Compliant:
1. `The investor chooses the presence probability \(\lambda\) of Section~\ref{sec:slot} and pays for it.`
2. `Research rises from \(\reg{res_lambda_r155}\) to \(\reg{res_lambda_r165}\) as the incumbent strengthens.` (A comparative static across strengths, which the rule keeps.)

Violating, `sections/05_research.tex:3`:
> So far the investor is present with a fixed probability \(\lambda\); now the investor chooses that probability and pays for it.

Rewrite: compliant sentence 1 above.

Violating, `appendix/A5_research.tex:423–425`:
> \paragraph{Certificates.} The exact program is \nolinkurl{P3_research/P3_research.py} (run log \nolinkurl{P3_research/P3_research.log}). It uses rational arithmetic for every rational quantity and rational intervals for every quantity that depends on \(\eu\).

Rewrite:
> Every display in this part is an exact computation: rational arithmetic for each rational quantity, and rational intervals rounded outward for each quantity that depends on \(\eu\).

### Rule 4. The example is neutral

> The example is neutral. The paper does not call it "the benchmark", "the calibration" or "the main case". Its results are corollaries, at most three in the main text.

Compliant:
1. `In the example, the incumbent is uniform on \([0,r]\) and the two classes are point masses at \(h\) and \(\ell\).`
2. `In the example, research and entry rise together at the three intermediate strengths (Corollary~3).`

Violating, `sections/04_equilibrium_results.tex:121`:
> Proposition~\ref{prop:region} in Appendix~\ref{app:prop2} gives the admissible region at the benchmark auction.

Rewrite:
> Proposition~\ref{prop:region} in Appendix~\ref{app:prop2} gives the recruitment region in the example.

### Rule 5. The style guide otherwise

> The style guide otherwise: the Laplace register, "I", one word per object, numbers only through `\reg`, no bold sentences in running text, four propositions and three corollaries in the main text with descriptive titles and intuition after each, no lemma or definition environments in the main text.

Compliant:
1. `For the uniform incumbent I write \(\tau(r)\) for the preparation threshold.`
2. `With research at the cap, entry at \(r_1\) is \(\reg{res_entry_r1}\).`

### Rule 6. Fixed choices

> Fixed choices: the two-point preparation cost (zero with probability ρ, c_H otherwise); no general cost law; no c_H rename.

Compliant:
1. `The preparation cost is zero with probability \(\rho\) and \(c_H>0\) otherwise.`
2. `A high-cost challenger prepares when gross profit at its belief exceeds \(c_H\), and it abstains when gross profit falls short of \(c_H\).`

### Rule 7. No names of tools, agents, models, sessions or accounts

> No tool, agent, model, session or account names in the manuscript, the comparison note, the slides, any committed project document or any commit message.

Compliant:
1. `The referee checked each renamed symbol against the five referee reports.`
2. Commit message: `Freeze the notation: rename the research polynomial, the research value and the coexistence set`

## (b) Vocabulary

One word for each object. The "where it still stands" column lists the places left after the S3 edits; part (d) assigns each to its stage.

### The example

- **Word:** "the example". The text introduces it once, at the opening of Section 4.2, by its primitives: a uniform incumbent on \([0,r]\), two point-mass classes worth \(h\) and \(\ell\), and the stated values of \(p\), \(\rho\), \(c_H\), \(k\) and the slot, each through `\reg`. Its main-text results are Corollaries 1, 2 and 3, placed after Propositions 2, 3 and 4 (decision 6). Before Section 4.2 the text speaks of "a stronger incumbent" and not of the strength \(r\).
- **The second example:** the complementary-signal economy of Appendix A.6 is "the signal example".
- **Example strengths:** "the strengths \(r_0\), \(r_1\), \(r_2\)" and "the three intermediate strengths", or "the weak, the strong and the very strong incumbent". "Benchmark strengths" is retired.
- **Retired:** "the benchmark", "the benchmark auction", "the benchmark path", "the benchmark set-up", "benchmark strengths", "benchmark volume", "the calibration", "calibration B", "B" or "S(B)" as a name, "Value at B", "the main case", "strong benchmark".
- **Differs from the lens plans:** `lens_maintext.md` 3.6 kept "the benchmark (declared in 2.5)". `PLAN.md` Part 1 and rule 4 override it.
- **Where it still stands:** on every line that the language scan lists. Part (d) names some of these lines; the owner of each file applies rule 4 to every line counted here (S8 the appendix, S9 and S10 the main text, S11 the slides and the note, S7 the figure code).
  - Lines that contain "benchmark", 183 in all: main text 01 (10), 02 (3), 03 (3), 04 (28), 05 (9), 06 (5), 07 (8), 08 (9); appendix A1 (2), A3 (11), A4 (9), A5 (1), A6 (9), A7 (4), A8 (18), A9 (12); `slides.tex` (20); `comparison.tex` (21); `make_figures.py` (1).
  - Lines that contain "calibration": A3 (6), A4 (6), A5 (5), A6 (1), A9 (6), `comparison.tex` (3). "The main case": 02:54.
  - "B" and "S(B)" as names: A3, A4, A6, A9, `comparison.tex` and the figure code.
  - Number keys that end in `_B` keep their names, because keys never print.

### Words for objects

| Object | The one word | Retired | Where it still stands |
|---|---|---|---|
| \(\DT=t_H-t_L\) | the target-payoff spread; "the spread" once defined | "price spread"; "spread" for the price gap | as the price gap: 01:95–96; 08:28, 08:40; A8:80, A8:131; slides:548; comparison:215, 352 ("execution spread") |
| \(P(1)-P(-1)\) | the price gap, written \(P(1)-P(-1)\); it has no symbol, because \(S\) names signals | "price spread", "spread between purchase and sale prices", "execution spread"; the symbol \(S\) for the gap | 01:95; A8:41–81 (the symbol \(S\), 12 lines); comparison:215, 352 |
| a mean-preserving change of a law | an increase in risk | "mean-preserving spread" | none |
| a bid, a value or a challenger at or above the reserve | admissible (02:101–102, A1:59–60); a challenger is admissible when its value is; "inadmissible" below the reserve; "equal admissibility" is \(G_H(p^-)=G_L(p^-)\) (02:73) | "admissible" for regions, sets, slots, rates, caps and costs | 04:121, 04:131; A3:4; slides:321, 678, 685; comparison:203, 355 ("admissible slots"), 444 |
| the set where (H1) to (H3) hold, `prop:region` | the recruitment region | "admissible region", "admissible set" | 04:121, 04:131; A3:4; slides:321, 678, 685; comparison:203, 444 |
| the parameter set of `prop:researchregion` | the research parameter region | "admissible region of the research parameters", "admissible cap and cost" | none |
| a rate that meets a stated definition | a qualifying rate | "admissible rate" | none |
| \(r_C\), above which no price recruits | the entry ceiling; "the ceiling" only for \(r_C\) | "ceiling" for anything else | slides:387 ("(H3) Ceiling at \(r_2\)"); figure label "ceiling \(r_C\)" (S7) |
| once \(B(M(\pi))<c_H\), no order recruits a high-cost challenger (03:94; Corollary `cor:exclusion`) | the exclusion bound | "the ceiling of the model", "the posterior bound on preparation" | none |
| (H3) | the exclusion condition | "the ceiling (H3)" | slides:387 |
| a high-cost challenger kept out after every order | exclusion: the exclusion bound, the exclusion condition, "strict exclusion at \(r_2\)" (A5:336, A8:94, A8:118), "the exclusion margin" (comparison:559, 567, 577–578) | "exclusion" for the reserve that keeps the low class out, and for ruling out wrong-signed orders | the reserve: 07:107; A7:198, A7:232; A9:202, A9:204; slides:535, 828; comparison:225, 716 ("the exclusion reserve"); wrong-signed orders: comparison:644 |
| a reserve above the low class's values | "a reserve that excludes the low class" (02:74), in full each time | "the exclusion reserve", "exclusion" alone | as in the row above |
| \(m(\pi)\le\mu\le M(\pi)\) | the posterior bounds | "posterior bound" for the exclusion bound | 03:128 ("the upper bound is the spread" means \(K_j\le\DT\); write "and the spread bounds it from above") |
| (H1), (H2) | the high-cost window, the trading-cost window | none | none |
| the lower bound \(\rho\kappa(\pi)\DT\) on a correct order's gross return; the margin \(\rho\kappa(\pi)\DT-k\) | the trading bound; the trading margin | "trade bound", "trade margin" | "trade bound": comparison:167, 422, 579, 688, 689; "trade margin": A6:263, A6:354, A7:226, A7:235, comparison:560, 673 |
| the equilibrium with no informed trade (form N) | a quiet market | "equilibrium without informed trade", "uninformative equilibrium", "no trade" as a noun, "no informed trade" as a name | "no informed trade": 08 (1 line), A4 (9), slides (1), `make_figures.py` (2); "no trade": 04 (1), 05 (2), 08 (1), 09 (1), A4 (1), slides (8), comparison (6), `make_figures.py` (1); "without informed trade": 04 (5); "uninformative equilibrium": main.tex (1), 01 (1), 04 (1), 09 (1) |
| an equilibrium with informed trade | an informative market | "informative equilibrium", "uninformative equilibrium" | main.tex (1 line), 01 (1), 04 (4), 09 (1), A4 (6), slides (1), comparison (3) |
| \(j\in\{H,L\}\) | class \(H\), class \(L\); the high class, the low class; adjective "high-class", "low-class"; in the abstract "a challenger from the high class" | "high-value class", "low-value class", "high-value challenger", "low-value challenger" | main.tex:81; 01:41 |
| the order \eqref{eq:classes} of the class laws | the class ranking | "class order" (an order is a trade) | none; "high-class order" at 04:324 and comparison:382 is an order placed by class \(H\) and stays |
| the entrant | the challenger | "the buyer", "the further buyer" and "the entrant" for the challenger | "buyer": 01:13; 06:79; 08:3, 08:11–13, 08:21, 08:78–79; comparison:346. "Entrant": 01:122; slides:239, 617. "A buyer", "buyers", "a ready buyer" and "the next buyer" for any acquirer stay: 01:7–11, 01:86; 02:7–38, 02:92; 07:45; 09:3; A7:98–123 |
| the entrant's act | prepare (the challenger pays its cost and prepares a bid); a price recruits a high-cost challenger when it makes it prepare | "enter" as the challenger's verb | slides:126, 195, 196 |
| the probability of that act | entry: \(e(x)\) after the order \(x\), \(\Ent\) in total; \(\zeta\), the high-cost preparation probability, is a different object | none | none |
| \(\tau\) | the preparation threshold; "threshold" only for \(\tau\) and the threshold pair | "threshold belief"; "threshold" for a marked strength; "sale threshold \(r_S\)"; "threshold branch", "threshold equilibrium", "threshold entry" | "threshold belief": 04:173, slides:355, comparison:85, figure axis label; marked strengths: A4:107, 110, 116, 120, slides:469, 740, 747, comparison:464, 633, 724; "threshold branch": 04:302 and the figure code; "threshold equilibrium": A5:387, 400; "the threshold entry": A5:55 (write "the entry of the threshold pair"); "threshold flow": comparison:263, 319 (write "the flow at which the posterior reaches \(\tau\)"); A6:540–541 ("the threshold" is the public belief 47/106 at which a challenger with \(S_C=+\) reaches \(\tau\); write it so) |
| \(r_A,\dots,r_C\), \(r_*\), \(r_\pi\), \(r_R\), \(r_{\lb}\), \(r_U\), \(r_Q\) | marked strengths | "thresholds" for these | A4:107–120; slides:469, 740, 747; comparison:464, 633, 724 |
| \(\varphi_a\), \(\varphi_\rho\) in the main text | the recruitment margin, the floor margin (words; the symbols stay in A5) | none | none |

### Tie rules

The paper uses these four phrases, and never the codes, in text, tables, figure labels, captions, the comparison note and the slides.

| Code (retired) | Phrase |
|---|---|
| IM | an indifferent investor may mix over its best orders (short form: "an indifferent investor may mix") |
| I0 | an indifferent investor abstains |
| C1 | an indifferent high-cost challenger prepares |
| CM | an indifferent high-cost challenger may prepare with any probability |

The default pair is "an indifferent investor may mix and an indifferent high-cost challenger prepares". A result that holds under each pair says "under all four tie rules".

Codes still print or stand in source as follows:
- appendix: A1 (2), A2 (6), A3 (4), A4 (59), A5 (19), A6 (6), A7 (1), A8 (9), A9 (1);
- comparison.tex (16);
- make_figures.py (5);
- the main text: none.

### Outcome names

**Coexistence forms** (A4:267–271). These forms arise at a fixed presence probability. The letter appears only in tables and figure legends, in bold roman.

| Letter | Name |
|---|---|
| N | a quiet market |
| R | a mixed purchase that recruits |
| F | a full purchase |
| Q | mixed orders at the entry floor |
| T | the threshold pair |

The forms R and F, together with the threshold pair at \(r_A\) when an indifferent high-cost challenger prepares (A4 Table A.2; Corollary A.2(b)), make up "the informative branch".

**Research outcomes** (Appendix A.5), at the prior \(1/2\). Under the default tie rules, three outcomes exhaust the equilibria (WORKAROUNDS W3.5). The letter appears only in A5 and in tables, in roman.

| Letter | Name | What happens |
|---|---|---|
| Z | zero research | no research is done; when \(\tau>1/2\) it exists exactly when \(\rho\DT\le2k\) (A5:309) |
| R | recruiting research | research is \(\min\{\lambda_R,\lb\}\), class \(H\) buys after a success, and a purchase recruits. The letter covers both cases: "R below the cap" (research \(\lambda_R<\lb\); in the example on \([r_R,r_{\lb})\)) and "R at the cap" (research \(\lb\); in the example on \([r_{\lb},r_C]\)), also written "recruiting research at the cap". Wherever one case is meant, its qualifier stands with the letter, so that the bare letter never names one tuple (part (d), S8, A5). \(\bar{\rm R}\) is retired. |
| Q | floor-entry research | research is \(\min\{\lambda_Q,\lb\}\), both classes trade after a success, no order recruits, and entry is \(\rho\). In the example it holds on \((r_N,r_Q)\), below the cap, and again on \((r_C,r_2]\), at the cap. |

When an indifferent high-cost challenger may prepare with any probability, "the threshold pair" can also arise. It is named in words; T is retired as an A5 tuple name.

The strengths at which R lies below the cap, \([r_R,r_{\lb})\), are "the recruiting branch". The strengths \((r_N,r_Q)\), where Q lies below the cap, are "the floor-entry branch"; above \(r_C\) the text says "floor-entry research at the cap". "The research branch" is retired, because there are two branches with research.

**Letters as decorations.** A form or outcome letter that decorates a symbol is roman. It is a subscript where the subscript slot is free (\(\mathcal E_{\rm N}\), \(\mathcal E_{\rm F}\), \(\Ent_{\rm R}\), \(\Ent_{\rm F}\), \(\Ent_{\rm T}\)), and a superscript where the subscript slot holds an index (\(\DT^{\rm F}\), \(\DT^{\rm N}\), \(\Own_H^{\rm Z}\), \(\Own_H^{\rm R}\)). Italic subscripts name a law (\(B_F\), \(w_F\), \(W_F\), \(\chi_F\)), a strength (\(B_r\), \(w_r\)) or a class (\(e_H\), \(W_H\)). A4:305–393, A4:546 and A5:278–280 write \(\Ent_R\), \(\Ent_F\), \(\Ent_T\) in italic; S8 sets them roman.

## (c) Symbols

One symbol per object. The "state" column is either "applied in S3" or "S\(n\)", the stage that carries the rename out. Counts are the uses at the time of the S3 check. The symbols were checked against these sources:
- `sections/*.tex`, `appendix/*.tex`, `main.tex`, `comparison.tex`, `slides.tex` and `make_figures.py`;
- the referee reports `W1.md` to `W5.md` and `second_opinion.md`.

Free letters left after these choices: υ, Θ, Σ, Υ and \(\epsilon\) (ϵ; \(\varepsilon\) is the half-width of the atomless cost law in A6, A9 and 06). The choices below take ι (the weights of A6's posterior vectors), ξ (the Laplace noise scale; A1's \(\xi\) becomes \(\Gamma\)), ψ (the pooling weight of A6) and Ξ (A4's \(\Xi_J\)). A letter taken after S3 goes through the coordinator.

**Paths.** A path is a family \(F_r\) of continuous incumbent laws indexed by the strength \(r\) on an interval, with \(F_{r'}\) first-order dominating \(F_r\) for \(r'>r\). It carries \(\DT(r)=\DT(F_r)\), \(\tau(r)=\tau(F_r)\), \(B_r(\mu)=B_{F_r}(\mu)\) and \(W_j(r)=W_j(F_r)\). The uniform family \(F_r=U[0,r]\) of the example is one path. A2 declares this once (S5), and every path statement (the reduction lemma of A2, Proposition 3(b) and (c), Proposition 4(c) and (d), the winner trend of A8) uses it. The referees' path indices \(s\) and \(t\) (\(F_s\), \(B_s\), \(\Delta(s)\), \(s_N\), \(s_C\), \(R_t\)) become \(r\); \(s\) is the base letter of the rates and \(t\) of the proceeds. The three economies of Proposition 2 keep their numeral index \(i\in\{0,1,2\}\) (\(F_i\), \(\Delta_i\), \(B_i\), \(t_{j,i}\)); on a path \(F_i\) stands for \(F_{r_i}\), and no symbol puts a numeral strength in the index of \(F\).

**The spread as an argument.** General statements write the spread as \(\DT\), as the paper does, and the (spread, threshold) plane is the \((\DT,\tau)\) plane: \(\lambda_R(\DT)\), \(\lambda_Q(\DT)\), \(\DT^{\rm F}\), \(\DT^{\rm N}\). No bare \(\Delta\) is used; the referees' bare \(\Delta\) maps to \(\DT\). The letter \(\Delta\) carries these decorations: \(\Delta_0,\Delta_1,\Delta_2\) (the spread at \(F_i\), A3, A6, A9), \(\Delta_\omega\) (A7), \(\Delta_P\) and \(\bar\Delta_P\) (A6), \(\Delta^1_x,\Delta^0_x\) (A8), \(\DT\), \(\DT^{\rm F}\), \(\DT^{\rm N}\). A further decoration goes through the coordinator.

### Kept as they stand (the model)

| Symbol | Meaning | Home |
|---|---|---|
| \(j\in\{H,L\}\), \(\pi\) | class, prior \(\Pr(j=H)\) | 02:57 |
| \(G_j\), \(\theta\), \(D=G_L-G_H\) | value law of class \(j\), a value drawn from it, the gap of the laws | 02:58–60 |
| \(p\) | the reserve | 02:59 |
| \(F\), \(\bar r\), \(R\), \(r\) | incumbent law, its support bound, the incumbent's value, the uniform incumbent's strength | 02:52–55 |
| \(h\), \(\ell\) | the example's class values | 02:78 (moves to Section 4.2 in S9) |
| \(C\), \(\rho\), \(c_H\) | preparation cost, zero-cost probability, high cost (rule 6: unchanged) | 02:91 |
| \(\lambda\), \(\beta\), \(b=(1-\lambda)\beta\), \(b_0\), \(u=\lambda/b\) | presence, liquidity, liquidity masses, the informed-to-liquidity ratio | 02:119–142, A2:32 |
| \(\eta(x)\) | the liquidity order law: \(\eta(\pm1)=\beta\), \(\eta(0)=1-2\beta\). The referees' \(\eta\) (W1.4 \(-g_H'/\Delta'\), W2.6 \(\Delta/\gamma\)) is a different object and is written out (part (d), S5) | A1:7; A2, A5, A6 |
| \(\hat b\), \(\hat b_0\); \(\bar b\), \(\bar b_0\) | the liquidity masses at the conjectured research \(\hat\lambda\); at the cap \(\lb\) | A5:25; A5:211, A5:221 |
| \(M(\pi)\), \(m(\pi)\); \(M_\lambda\), \(m_\lambda\) | top and bottom posteriors; at the prior \(1/2\) and intensity \(\lambda\) | 02:146; 05:29–30 |
| \(q\), \(x\), \(X\), \(k\), \(\kappa(\pi)\) | own order, a generic order, the observed order, trading cost, trading-bound fraction | 02:120–130, 03:121 |
| \(\mu(x)\), \(P(x)\), \(\bar P\), \(\bar\mu(\bar P)\) | posterior, price, a price in the image of \(P\), the challenger's belief at that price. \(\bar P\) never means the expected price, which is \(\E[P(X)]\) (renamed table) | 02:181, A1:22–36 |
| \(e(x)\), \(\Ent\), \(e_j\) | entry after an order, total entry, entry in class \(j\) | 02:191, 02:225, A3:79 |
| \(\eu\) | Euler's number (only for \(1+u=\eu\)) | 02:163 |
| \(t(\theta)\), \(g(\theta)\), \(t_0\), \(t_j\), \(g_j\) | proceeds and profit at a value, proceeds without entry, class expectations | 02:107, 02:196–199 |
| \(\DT\) | the target-payoff spread | 02:199 |
| \(B(\mu)\), \(B_F\), \(B_r\) | gross profit at a belief | 02:202 |
| \(\tau\), \(J(r)=\DT(r)[1-\tau(r)]\) | preparation threshold; the return of a purchase that just reaches \(\tau\) | 03:99; A4:15 |
| \(K_j\) | gross return of a correct order | 03:119 |
| \(W_H(F)\), \(W_L(F)\), \(\Own_H\) | win probability by class, high-class ownership | 02:225–228 |
| \(w_j=t_j-t_0\), \(w(\mu)\) | entry gain by class and at a belief | A2:23–24 |
| \(\sigma_j\), \(f_j(x)\), \(\zeta\), \(\mathcal E\) | the investor's order law, order probability in class \(j\), high-cost preparation probability, the equilibrium tuple | A1:12–27 |
| \(I_+\), \(I_-\) | purchase and sale impacts | A8:42–43 |
| \(\vartheta=\lambda/(2b+\lambda)=u/(2+u)\) | the informed share of nonzero orders under full trade. It equals \(M-m\) only at the prior \(1/2\): at \(b=0.2\), \(\lambda=0.3\), \(\pi=0.7\), \(\vartheta=0.429\) and \(M-m=0.371\). A8:8 writes \(\vartheta=2M-1=M-m\) at the prior \(1/2\); S5, which extends A8 to every prior, defines \(\vartheta\) by the share | A8:8, A8:39–40 |
| \(\chi_r=\1\{B_r(M)\ge c_H\}\); \(\chi_F=\1\{B_F(M)\ge c_H\}\) | whether a purchase recruits, against \(r\) on a path and against a law \(F\) (referee W4 \(\chi\)) | A8:7; S5 |
| \(v=\Pr(X\ne0)\) | the volume, the frequency of nonzero orders | A8:8 |
| \(e^*\) | entry after a purchase in the threshold pair (A4: \(k/J\); A5 adds the research term) | A4:271, A5:57 |
| \(s^*\), \(s_R\), \(s_Q\) | purchase rates of the threshold pair and of forms R and Q | A4:152, A4:268–270 |
| \(\hat\lambda\), \(\Pi\), \(a\), \(\lb\), \(a_{\rm mono}\), \(a_{\rm lo}\), \(a_{\rm up}\), \(a_{\max}\) | conjectured intensity, research objective, research cost, cap, research-cost bounds | A5:75, A5:131, 05:4, A5:291–326 |

`SCAN.md` proposed \(\Sigma\) in place of \(\mathcal E\) and \(\psi_j\) in place of \(f_j\). Both stay as they are, which differs from the lens plans. The glyph \(\mathcal E\) is distinct from \(\E\) and \(\Ent\) and has many uses across A1 to A3. The referee's \(\psi_H\), \(\psi_L\) are the paper's \(f_H\), \(f_L\).

### Renamed in S3 or later

| Symbol | Meaning | Home | Collision avoided; referee form | Uses at S3 | State |
|---|---|---|---|---|---|
| \(\Lambda_r(\lambda)\) (was \(F_r\)) | the research polynomial, whose root in \((0,1)\) is the research choice at \(r\) | A5 \eqref{eq:a5-F} | \(F\), the incumbent law | A5: 27 lines | applied in S3 |
| \(\Psi\) (was \(V\)) | research value: the expected trading payoff after a success | A5:32 | \(V_T\), the target's value; referee W3 \(V\) | A5: 24 lines | applied in S3 |
| \(\mathcal C(\pi)\) (was \(C(\pi)\)) | the strengths of the example's path in \([r_0,r_2]\) at which, at the prior \(\pi\), a quiet market and an informative market coexist under the default tie rules (Corollary A.2). The general set of decision 3, in the \((\DT,\tau)\) plane, has no symbol: it is "the coexistence region" | A4:441 | \(C\), the cost; the margin \(C\) of A7:196 | A4: 16 lines | applied in S3 |
| \(\widetilde{\mathcal C}(\pi)\) (was \(\mathcal C_{\rm CM}(\pi)\)) | the same set when an indifferent high-cost challenger may prepare with any probability: \(\mathcal C(\pi)\cup\{r_\pi\}\) for \(\tau(r_A)<\pi\le\pi_{\max}\), and \(\mathcal C(\pi)\) for every other prior | A4:564–566 | a tie code in a subscript | A4: 2 | S8 |
| \(s_+\), \(s_-\) (were \(s\), \(t\)) | the informed investor's purchase rate and sale rate. In A4 and A8, \(s_+=\lambda\sigma_H(1)\) and \(s_-=\lambda\sigma_L(-1)\), the high-class purchase rate and the low-class sale rate; in the signal example (A6:524–531), \(s_\pm=\lambda\sigma_\pm(\pm1)\), the rates after the investor's signals \(\pm\) | A4:135; A6:524 | \(t\), proceeds; \(z\) (A6, A7); referee W5 \(s_+\) agrees | A4: 59 and 43 lines; A6: 6 and 10; A8: 5 \(s_+\) | applied in S3 |
| \(\hat s_-(r)\) (was \(s_-^*(r)\)) | the unique qualifying low-class sale rate when an indifferent investor may mix, at any prior: \(0\) if \(\rho\DT\pi\le k\); the rate at which the sale just earns \(k\) if \(\rho\DT m(\pi)<k<\rho\DT\pi\); \(\lambda\) if \(\rho\DT m(\pi)\ge k\). At the prior \(1/2\) it equals \(s_Q(r)\) on \((r_N,r_S)\) only. The sale probability is \(\sigma_L(-1)=\hat s_-(r)/\lambda\) (A4:275), at the cap \(\hat s_-(r)/\lb\) | A4:204 | the star of \(s^*\), \(e^*\), \(r_*\); the O1 draft's \(s(r)\) | A4: 9 lines | applied in S3 |
| \(r_{\lb}\) (was \(\bar r_R\)) | the strength at which recruiting research reaches the cap | 05:119–125 | \(\bar r\), the support bound; second opinion \(\bar r_R\); referee W3 \(r_{\rm cap}\). The slides and the note have no `\lb` macro and write \(r_{\bar\lambda}\) | 05: 5; A5: 8; A9: 2 lines | applied in S3; slides, figure code in S7, S11 |
| \(r_Q\) | the end of floor-entry research below the entry ceiling: the zero of the floor margin \(\varphi_\rho\), where \(\tau(r_Q)=M_\lambda\) at \(\lambda=\lambda_Q(\DT(r_Q))\); about 2.167 in the example. Floor-entry research holds on \((r_N,r_Q)\) and again, at the cap, on \((r_C,r_2]\) | S5 (A5, from the O1 lemma), S6, S7 | \(r_X\) reads as the order \(X\); referee W3 \(r_X\) | none | S5 |
| \(r_-,r_+\) | the two ends of a path of strengths, \(r\in[r_-,r_+]\) (Proposition 4(d), A5). Pieces of a subdivision inside a proof are written \([r',r'']\) | S4 (25 October 2026), S5 (A5) | the O1 draft's \(r_\pm\) for pieces | none | S5 |
| \(\alpha_I\), \(\alpha_C\) (were \(a_T\), \(d\)) | accuracy of the investor's and of the challenger's signal | 06:61; A6:384–389 | \(a\), the research cost; \(d\), the argument of \(\fr\) and the mean gap | 06: 5; A6: 41; A9: 7 lines | applied in S3 |
| \(\lambda_R(\DT)\); \(\lambda_R(r)\) in the example | recruiting research: the root in \((0,1)\) of \(2a\lambda=\DT m_\lambda-k+(\rho\DT m_\lambda-k)^+\). It equals the root of \eqref{eq:research} wherever \(\rho\DT m_\lambda\le k\) at that root, which covers the strengths where the low class mixes as well as those where it abstains. In the example the two agree at every strength, because the kink \((1-\rho)k/(2a\rho)\) is \(1.2>1\). Research is \(\min\{\lambda_R,\lb\}\), written out | 05:42; A5 | lens choice \(\Lambda(\Delta)\) collides with \(\Lambda_r\); a star collides with \(r_*\), \(s^*\), \(e^*\); referee W2 \(\Lambda(\Delta)\), W3 \(L(\Delta)\) and \(c(\Delta)\) | 05: 9; A5: 27 | kept; general form in S5 |
| \(\lambda_Q(\DT)\), for \(\rho\DT\ge2k\) | floor-entry research: the unique root in \([0,1)\) of \(a\lambda=\rho\DT m_\lambda-k\), zero exactly when \(\rho\DT=2k\) (domain set in S4, 25 October 2026); research is \(\min\{\lambda_Q,\lb\}\), written out. In the example \(\lambda_Q(\DT(r))\) reaches the cap exactly at \(r_U\) | S5 (A5, from the O1 lemma) | \(Q\), \(q\); \(\Lambda_r\); the O1 draft's \(\Lambda_\rho\) and \(\lambda^*_\rho\); referee W3 \(Q\) and \(q\) | none | S5 |
| \(\lambda_E(\tau)\); \(\lambda_E(r)=\lambda_E(\tau(r))\) in the example | recruitment intensity: the \(\lambda\) at which \(M_\lambda=\tau\) | 05:32 | the general statements take \(\tau\) as the argument; the example keeps \(r\), declared once | 05: 8; A5: 45 | S5, S8 |
| \(\varphi_a\); \(\varphi_a^*\) | recruitment margin \(\DT(1-\tau)-k-2a\lambda_E\); the exact margin adds \((\rho J-k)^+\) | A5:57 | A6's \(\phi_\pm\), renamed below; referee W3 \(\phi_a\) is the same object | A5: 22; A9: 1 | kept; \(\varphi_a^*\) in S5 if used |
| \(\varphi_\rho(r)=\rho\DT(r)[1-\tau(r)]-k-a\lambda_E(r)\) | the floor margin: the gap \(\rho\DT m_\lambda-k-a\lambda\) of floor-entry research at \(\lambda=\lambda_E(r)\), since \(m_{\lambda_E(r)}=1-\tau(r)\); its unique zero is \(r_Q\) | S5 (A5, from the O1 lemma) | the pair of \(\varphi_a\); the O1 notes' gap \(g(\lambda,r)\) collides with \(g_j\) and is written out | none | S5 |
| \(\lb(\beta)=u\beta/(1+u\beta)\) (was \(\lambda_B(\beta)\)) | the cap as a function of \(\beta\) | A5:373–378 | "calibration B", \(B(\mu)\) | A5: 4 | S8 |
| \(\tilde\lambda\) (was \(z\) in \(\Pi(z,\sigma')\)); \(\min\{\lb,\Psi/a\}\), written out (was \(z^*\)) | a research deviation; the best research choice | A5:65–80 | \(z\) in A6 and A7; \(\lambda'\), the alternative slot's presence in A8:90–138; the prime of derivatives (\(\lambda_R'\), \(\DT'\)) | A5: 5 lines | S8 |
| \(\gamma=g_H-g_L\) | the profit gap | S5 (A3, A4) | A6:354's separation distance \(\gamma\), renamed \(\varsigma\) | none in this meaning | S5; \(\varsigma\) in S8 |
| \(\bar\Gamma=\E_H\theta-\E_L\theta=\DT+\gamma\) | the class mean gap | A6:165 | WORKAROUNDS and referee \(d\) | A6: 5 | kept |
| \(\Gamma(x)\) (A1's \(\xi(R)\) becomes \(\Gamma(R)\)) | the integrated gap of the class laws, with A1's general definition: \(\Gamma(x)=\int_p^xD(y)\,dy\) for \(x\ge p\) and \(pD(p^-)\) for \(x<p\), so that \(\DT(F)=\E_F[\Gamma(R)]\). Under the class ranking \(D(p^-)=0\) and \(D=0\) below \(p\), so \(\int_0^xD=\int_p^xD\), and \(\Gamma\) is nondecreasing with limit \(\bar\Gamma\). The lower limit matters only in A7's part on values below the reserve | A1:178–184; A6:165 | one function, two symbols (A1's \(\xi\), A6's \(\Gamma\)); referee W4 \(\xi(R)\) and \(\Gamma(r)=\int_0^rD\) | A1: 9 lines (\(\xi\)); A6: 9 | S8 (A1) |
| \(\DT^{\rm F}=k/(1-M)\), \(\DT^{\rm N}=k/(\rho\max\{\pi,1-\pi\})\) | the spreads at which a full purchase that recruits, and a unit order against a quiet market, just earn \(k\) | S5 (A4) | \(\DT(F)\), the spread at the law \(F\): the form letter is a roman superscript; WORKAROUNDS \(\Delta_F\), \(\Delta_N\) | none | S5 |
| \(\max\{\pi,1-\pi\}\), written out | the larger prior | A4:434 | \(q\), the order; WORKAROUNDS \(q_\pi\) | A4: 2 | kept |
| \(\Omega(F)=W_H(F)-W_L(F)\) | the win-probability gap | S5 (A8) | none; referee W4 \(\Omega\) agrees | none | S5 |
| \(W_F(\mu)=W_L(F)+\mu\,\Omega(F)\) (was \(w_x\)) | the win probability of a prepared challenger at the belief \(\mu\) against \(F\); after the order \(x\) it is \(W_F(\mu(x))\), and the unconditional win probability is \(e(x)\,W_F(\mu(x))\). It parallels \(B_F(\mu)\) and \(w_F(\mu)\) | A8:166–191 | \(w_j\), \(w(\mu)\), the entry gain; \(W_j(F)\) takes a law; referee W4 \(w_x\), and W4's \(y_x\) is \(e(x)W_F(\mu(x))\) | A8: 8 lines (167, 172, 173, 183–185, 190, 191) | S5, S8 |
| \(\1_{\rm prep}\), \(\1_{\rm acq}\) (were the events \(A\), \(W\) and the indicator \(Y\)) | the indicators that the challenger prepares and that it acquires the target. A conditional probability reads "given preparation"; the generic indicator \(Y\) and its conditional means \(y_x\) are written out for each of the two indicators | A8:166–236 | \(A\), the old \(A_r\) and W1's \(A\); \(W\) beside \(W_j\), \(W_F\); \(Y\), the highest competing bid (A1:59) and A6's old signal | A8: 18 lines | S8 |
| \(w_r(\mu)\), \(w_F(\mu)\) (was \(A_r(\mu)\)) | the entry gain \(w(\mu)\) against \(r\) or \(F\) | A2:23–24 | two symbols for one object; referee W5 \(A_F\), \(A(\mu)\) | A8: 22; A9: 1 | S8 |
| \(\bar f(x)=\Pr(X=x)\) | the unconditional order probability; A8:8's \(\bar f\) is \(\bar f(\pm1)\) under full trade at the prior \(1/2\) | A8:8 | referee W5 \(f_\pm\), \(f_x\) (unconditional) against \(f_j\) and A6's \(f_\pm\) (conditional) | A8: 2 | S5, S8 |
| \(\E[P(X)]\), written out (was \(\bar P\) in A8) | the expected price before the order opportunity | A8:230–232 | \(\bar P\), a price in the image of \(P\) (A1 to A6); the weighted test of S5 (W5.1) is \(\E[P(X)]-P(0)\) | A8: 3 lines | S5, S8 |
| \(\mathcal E_{\rm F}(F)\) (was \(\mathcal F\) in A8, \(\mathcal E_1\) and \(\mathcal E_2\) in A3 and A7); \(\mathcal E_{\rm N}(F)\) (was \(\mathcal E_0\)) | the full-order tuple and the quiet-market tuple at the law \(F\). A3 writes \(\mathcal E_{\rm N}(F_0)\), \(\mathcal E_{\rm F}(F_1)\) and \(\mathcal E_{\rm F}(F_2)\); A8, at a fixed strength, writes \(\mathcal E_{\rm F}\) | A8:21; A3:31, A3:58, A3:94; A7:26 | \(F\), the law; one tuple with two names | A8: 12; A3: 12; A7: 1 | S8 |
| \(\fr(y)\) (was \(\fr(d)\)) | the root above \(\ell\) of \(\DT(r)=y\) | main.tex:57; A4:17 | \(d\) | A4:17–18 | S8; main.tex comment in S10 |
| \(S_I\), \(S_C\) (were \(T\), \(Y\)); the values \(\pm\) (were \(t\), \(y\)) | the investor's and the challenger's signals in the signal example, each with values \(\pm\): \(f_\pm\), \(\sigma_\pm\), "\(S_I=\pm\)", "\(S_C=\pm\)". The challenger's signal \(S\) of Proposition A.4 (A6:8–29) keeps its name. The letter \(S\) names signals only: the price gap is written \(P(1)-P(-1)\), and "S(B)" is retired | A6:384–411; A6:8–29 | \(T\) in \(\DT\) and the form T; \(Y\), the highest competing bid in A1:59; the price gap \(S\) of A8:41–81 | A6: 13 lines (\(T\)), 15 (\(Y\)), 8 (\(t\), \(y\)) | S8 |
| \(\nu_I(x)\) (was \(\nu(x)\)) | the posterior that the investor's signal is \(+\) after the order \(x\) | A6:398 | \(\nu\), the posterior vector of A6:279–352 | A6: 9 lines | S8 |
| \(\mu^C_\pm(\mu)\) (was \(\phi_\pm(\mu)\), \(\phi_y\)) | the challenger's belief after its own signal at the public belief \(\mu\) | A6:392, A6:405–406 | \(\varphi_a\) | A6: 12; A9: 2 | S8 |
| \(M^I\), \(m^I\) (were \(\mu_+\), \(\mu_-\)) | the top and bottom public posteriors when the investor's signal has accuracy \(\alpha_I\) | A6:391 | \(\mu_\pm(s)\) as functions of the rate (A4:155); \(\mu(x)\); the subscript slot of \(M_\lambda\) | A6: 10; A9: 3 | S8 |
| \(\zeta_\pm(\mu)\) (was \(I_\pm(\mu)\), \(I_y(\mu)\)) | high-cost preparation probability after the challenger's signal | A6:407–411 | \(I_\pm\), the price impacts of A8 | A6: 6 lines | S8 |
| \(\bar\Delta_P\) (was \(D^+\)) | the largest price response to the public posterior, the upper bound on \(\Delta_P\) | A6:394, A6:415 | \(D=G_L-G_H\) | A6: 8 | S8 |
| the number of classes, in words (was \(J\)) | "finitely many classes \(j\)"; no symbol is needed | A6:279 | \(J(r)\); \(n\), the sample size of W5.3 | A6: 1 | S8 |
| \(\varsigma\) (was \(\gamma\)) | separation distance of two class groups | A6:354, A9:183 | \(\gamma=g_H-g_L\). It stays beside \(\sigma_j\): \(\varsigma\) is a scalar on three lines with no subscript, while \(\sigma_j\) always carries a class index | A6: 2; A9: 1 | S8 |
| \(\mu_{\mathcal H}\) (was \(z\)) | the posterior of the class group \(\mathcal H\) | A6:332–342 | \(z\) | A6: 9 lines | S8 |
| \(\bar t(0)\), \(\bar t(1)\) (were \(z_0\), \(z_1\)) | conditional mean proceeds at the orders \(0\) and \(1\), normalized | A6:371–373 | \(z\) | A6: 2 lines | S8 |
| \(2\alpha_I-1\) (was \(z\)) and \(k/(m\rho\DT(r_1))\) (was \(z_*\)), written out | the investor's signal precision; the least precision for the strong bound | A6:507–510 | \(z\) | A6: 3 lines | S8 |
| \(\psi\) (was \(w\)) | the mixing weight in class 2 of the pooling example | A6:362–379; A9:189 | \(w\), the entry gain; \(\varpi\) would sit beside the prior \(\pi\) | A6: 7; A9: 1 | S8 |
| \(\iota_j\) (was \(w_j\)) | the weights in \([1,1+u]\) that span the posterior vectors \(\nu_j=\pi_j\iota_j/\sum_l\pi_l\iota_l\) | A6:352 | \(w_j\), the entry gain | A6: 1 | S8 |
| \(\Phi\), \(\Phi^0\), \(\Phi^1\), \(\bar c_0\) (were \(H_C\), \(H^0\), \(H^1\), \(L\)) | the cost law of the robustness result; its low-cost component, with support in \([0,\bar c_0]\), which plays the role of the zero cost; its high-cost component, with support in \([c_-,c_+]\) | A6:73–146; A9:174 | the class letters \(H\), \(L\); rule 6 keeps the two-point cost everywhere else | A6: 11; A9: 1 | S8 |
| the joint law of \((\theta,R)\) given \((j,S)\), in words (was \(\mathcal L_i(\theta,R\mid j,S)\)) | the condition of Proposition A.4 | A6:11, A6:22 | \(\mathcal L\), the low group of classes (A6:285–340), which keeps the symbol | A6: 2 | S8 |
| \(\theta\), \(\theta_*\) (were \(v\), \(v_*\)); \(t(\theta)\), \(g(\theta)\) (were \(t_v\), \(g_v\)); \(F(\theta)\), written out (was \(W_v\)) | a value (A1: a bidder's; A6, A7: a challenger's); the lowest value at which the classes start to differ above the reserve; proceeds and profit at the value \(\theta\), as in 03:12; the win probability at the value \(\theta\), which is \(F(\theta)\) for \(\theta\ge p\) and zero below \(p\) | A1:59–65; A6:167–194, A6:245–265; A7:146–158; 06:33–36 | \(v\), the volume of A8; the note's sale size \(v\); \(t_v\) duplicates \(t(\theta)\) | A1: 6 lines; A6: 15; A7: 9; 06: 3 | S8; 06 in S9 |
| the fallback \(\min\{R,\theta\}\), the winner's value \(\max\{R,\theta\}\) and the payment \(T_\omega\), written so (were \(z\), \(V\), \(P\)) | the Nash-bargaining step of the payment rule | A7:119–124 | \(z\), the order unit; \(V\) beside \(V_T\) and the old research \(V\); \(P\), the stock price. \(T_\omega\) keeps its name: the subscript separates it from the form T | A7: 5 lines | S8 |
| the order unit, in words (was \(z\)) | the size of one order, in shares per share of float | A7:72–76; 07:27–28 | \(z\) in A5, A6 and the bargaining step | A7: 2; 07: 2 | S8; 07 in S9 |
| margins written as expressions (were \(T\), \(C\), \(J\)) | trading margin \(\rho\kappa\DT-k\), prior-cost margin \(c_H-B(1/2)\), top-posterior margin \(B(M)-c_H\) | A7:196–200; A9:201–204 | \(\DT\); the cost \(C\); \(J(r)\) | A7: 2; A9: 4 | S8 |
| margin columns named in words (were \(C_0\), \(C_1\), \(T_0\), \(T_H\), \(T_L\), \(C_2\), \(O\)) | the margins of the Proposition 2 economies; each word is defined in the notes by its expression | A9:231–247 | the cost \(C\); \(T\) in \(\DT\) and the form T; \(O\) beside \(\Own\) | A9: 4 lines | S8 |
| \(\Xi_J\) (was \(Q_J\)) | the polynomial with no real root in A4's proof of uniqueness of \(r_A\) | A4:43–48; A9:123 | the form Q | A4: 4; A9: 1 | S8 |
| the numerator and the denominator of \(\tau(r)\), written out (were \(N_\tau\), \(D_\tau\)) | the two polynomials of \(\tau(r)\) in A4's sign argument | A4:32–38 | \(N\), the form; \(D\); \(n\) and \(d\) | A4: 4 lines | S8 |
| \(k/(\rho m)\), written out (was \(D_S\)) | the spread at \(r_S\), so that \(r_S=\fr(k/(\rho m))\) | A8:15 | \(D\) | A8: 1 | S8 |
| \(\E[X]\), written out | expected order flow, in identification | S5 (A8) | referee W5 \(d\) | none | S5 |
| \(\bar f(1)I_+-\bar f(-1)I_-\), written out | the weighted impact difference | S5 (A8) | referee W5 \(T\) | none | S5 |
| \(\pi(1-\pi)\lambda=\bar f(-1)I_-/(\rho\DT)\), written out | the sale-price inversion (decision 5) | S5 (A8) | referee W5 \(Q\) | none | S5 |
| \(\xi\) (was \(s\) in the main text and the slides, \(b\) in the note) | the scale of the Laplace noise in the footnote on additive liquidity flow | 02:162–164 | \(s\), the base letter of the rates; \(b\), the liquidity mass | 02: 2 lines; slides: 1; comparison: 2 | S10, S11 |

### Marked strengths

Each is a strength of the example at the prior \(1/2\) unless an argument says otherwise. All print through `\reg`.

| Symbol | Definition | Home |
|---|---|---|
| \(r_0\), \(r_1\), \(r_2\) | the weak, the strong and the very strong incumbent of Proposition 2 in the example | 04, Section 4.2 |
| \(r_A\) | the root of \(J(r)=k\) in \((r_0,r_2)\): the informative branch starts | A4:67 |
| \(r_F\) | \(\fr(k/(1-M))\): a full purchase that recruits just earns \(k\) | A4:69 |
| \(r_N\), \(r_N(\pi)\) | \(\fr(2k/\rho)\): a unit order against a quiet market just earns \(k\); at the prior \(\pi\), \(\fr(k/(\rho\max\{\pi,1-\pi\}))\) | A4:71, A4:434 |
| \(r_J\) | the root of \(\rho J(r)=k\) | A4:73 |
| \(r_S\) | \(\fr(k/(\rho m))\): a full sale just earns \(k\) | A4:75 |
| \(r_C\) | the entry ceiling: above it, gross profit at the top posterior falls short of \(c_H\) | 04:164 |
| \(r_*\) | the root of \(\rho\DT(r)\tau(r)=k\) | A4:82 |
| \(r_\pi\) | the root of \(\tau(r_\pi)=\pi\), for \(\tau(r_0)\le\pi\le\tau(r_2)\): the open left end of \(\mathcal C(\pi)\) in Corollary A.2(c), and the point that \(\widetilde{\mathcal C}(\pi)\) adds to \(\mathcal C(\pi)\) when \(\tau(r_A)<\pi\le\pi_{\max}\) | A4:436, A4:450, A4:564 |
| \(r_R\) | recruiting research starts: \(\DT(1-\tau)=k+2a\lambda_E\) | 05:119–122 |
| \(r_{\lb}\) | recruiting research reaches the cap | 05:119–122 |
| \(r_U\) | \(\fr((k+a\lb)(1+\eu)/\rho)\), the strength at which floor-entry research \(\lambda_Q(\DT(r))\) reaches the cap. At every strength above it other than \(r_C\), full orders and research at the cap are the unique outcome under every pair of tie rules (A5:204–208). Under the default tie rules uniqueness already holds from \(r_Q\) on (the O1 lemma, part (d)) | 05:128, A5:257 |
| \(r_Q\) | the zero of the floor margin \(\varphi_\rho\), where \(\tau(r_Q)=M_\lambda\) at \(\lambda=\lambda_Q(\DT(r_Q))\): floor-entry research below the entry ceiling ends; \(r_N<r_Q<r_U<r_C\) | S5 |

The comparison note's \(r_U^R\) (`comparison.tex:36`, the macro `\rUR`) becomes \(r_U\), as in the paper. Strengths of the other set-up in the note carry the roman superscript \({\rm Lap}\), for example \(r_U^{\rm Lap}\) (S11).

## (d) Renames by stage and file

Each stage applies its part by exact replacement, keeps the mathematics identical, rebuilds and reads every changed page. The coexistence-form and research-outcome letters keep their roman or bold roman type. The symbol renames of S3 itself are done (`progress/S3_draft.md`).

### S5, the mathematics writer (appendix proofs)

Write with part (c) from the first line:
- the path \(F_r\), declared once in A2 (part (c), **Paths**), and \(\DT\) as the spread in every general statement (no bare \(\Delta\));
- \(\gamma\), \(\bar\Gamma\), \(\Gamma\), \(\DT^{\rm F}\), \(\DT^{\rm N}\), \(\Omega\), \(W_F(\mu)\), \(w_F(\mu)\), \(\chi_F\), \(\bar f(x)\) and \(\E[P(X)]\);
- \(\lambda_R(\DT)\) and \(\lambda_Q(\DT)\), with \(\min\{\cdot,\lb\}\) written out, and the floor margin \(\varphi_\rho\) beside \(\varphi_a\);
- \(\vartheta=\lambda/(2b+\lambda)\) wherever A8 leaves the prior \(1/2\);
- \(\lambda_E(\tau)\), \(r_Q\) and the tie phrases;
- the balance condition undivided, \(\bigl(\DT\,(g_H-c_H)\bigr)'\ge0\), as W1 recommends.

Map the referee's symbols to the paper's on entry.
- All reports: \(\Delta\) → \(\DT\); \(d\) → \(\bar\Gamma\) or \(\E[X]\); \(\psi_j\) → \(f_j\); a path index \(s\) or \(t\) → \(r\).
- W1:
  - \(\eta=-g_H'/\Delta'\), \(X=g_H-c_H\) and \(Y=\eta\Delta\) → the undivided balance condition, with \(g_H-c_H\) written out (\(\eta\) is the liquidity order law, \(X\) the observed order, \(Y\) the highest competing bid);
  - \(A=(r^2-p^2)/(2r^2)\) → written out (\(A\) was the preparation event); the Lipschitz constant \(L\) → in words (\(L\) is the class);
  - \(\mathsf E_I\) → \(\Ent\) of the informative market, \(\Ent_{\rm R}\) or \(\Ent_{\rm F}\) as the form is;
  - \(F_s\), \(B_s\), \(s_N\), \(s_C\), \(R_t\), \(m_L(t)\), \(m_H(t)\) → \(F_r\), \(B_r\), \(r_N\), \(r_C\), \(R\) at \(F_r\), and the posteriors at \(r\).
- W2:
  - \(\Lambda(\Delta)\) → \(\lambda_R(\DT)\); \(\eta=\Delta/\gamma\) → \(\DT/\gamma\), written out;
  - \(q_H(x)\), the fixed-value kernel of Proposition 4(b) → \(1-G_H(x)\) for \(x\ge p\) and \(1\) below \(p\), away from atoms of \(G_H\), written out (\(q\) is the order);
  - \(O_H\) → \(\Own_H\).
- W3 (and WORKAROUNDS W3.1, W3.4):
  - \(L(\Delta)\) → \(\lambda_R\); \(c(\Delta)\) → \(\min\{\lambda_R,\lb\}\); \(Q\) → \(\lambda_Q\); \(q\) → \(\min\{\lambda_Q,\lb\}\); \(r_X\) → \(r_Q\);
  - \(z\), the low-class sale probability → \(\sigma_L(-1)\), whose rate is \(s_-=\lambda\sigma_L(-1)\);
  - \(\lambda_S=(1-\rho)k/(2a\rho)\), the kink → written out;
  - \(V\) → \(\Psi\); \(r_{\rm cap}\) → \(r_{\lb}\); \(\phi_a\) → \(\varphi_a\).
- W4:
  - \(\xi(R)\) → \(\Gamma(R)\); \(\chi\) → \(\chi_F\);
  - \(w_x\) → \(W_F(\mu(x))\); \(y_x\) → \(e(x)\,W_F(\mu(x))\);
  - \(Q=W_H/W_L\) → written out; \(\operatorname{OR}_W\) and \(\operatorname{RR}\) → "the odds ratio" and "the risk ratio", in words.
- W5:
  - \(A_F\), \(A(\mu)\) → \(w_F(\mu)\); \(f_\pm\), \(f_x\) → \(\bar f(\pm1)\), \(\bar f(x)\); \(e_x\), \(e_\pm\) → \(e(x)\); \(\mu_x\) → \(\mu(x)\);
  - \(S\) → \(P(1)-P(-1)\), written out; \(T\) and \(Q\) → written out;
  - \(\delta=F-\tilde F\) → written out (\(\delta_q\) is the point mass of A2:32); \(G_M\) → \((1-M)G_L+MG_H\), written out; \(Q_F(M)\) → its integral, written out;
  - \(\ell_0\) → "the lowest challenger value", \(\underline\theta\); \(r_{\min}\) → "the lowest strength on the path", \(\underline r\);
  - \(\Delta^1_X\) → \(\Delta^1_x\); the sample size \(n\) → in words.

The O1 draft (`statements/O1/O1_proof.tex`, the mathematics writer's), when S5 places it in A5:
- \(\Lambda_\rho(\DT)\) → \(\lambda_Q(\DT)\); \(\lambda^*_\rho(\DT)\) → \(\min\{\lambda_Q(\DT),\lb\}\), written out (\(\Lambda_\rho\) beside \(\Lambda_r\), the star beside \(r_*\), \(s^*\), \(e^*\));
- \(s(r)\), the low-class sale probability at the cap → \(\sigma_L(-1)=\hat s_-(r)/\lb\), as A4:275 writes it (\(s\) is the base letter of the rates);
- \(\varphi_\rho\) stays (part (c)); the notes' gap \(g(\lambda,r)\) → \(\rho\DT m_\lambda-k-a\lambda\), written out;
- "research at the entry floor" → "floor-entry research"; "the recruiting tuple at the cap" → "recruiting research at the cap" (part (b), research outcomes).

### S7, the production assistant (`make_figures.py`, figure labels)

Line numbers drift while the file is edited, so each item names the string.
- `r"$\bar r_R$"` → `r"$r_{\bar\lambda}$"`; `r_R-bar` in the docstring, the check list and the log lines → `r_lambda-bar`.
- `threshold belief, $\tau(r)$` (axis label) → `preparation threshold, $\tau(r)$`.
- `ceiling $r_C$` → `entry ceiling $r_C$`.
- `total entry, $E$`, in both coexistence panels and the research panel → `entry, $\mathsf{E}$` (the paper's \(\Ent\)).
- `Q: mixed orders at the floor` → `Q: mixed orders at the entry floor`.
- `N: no informed trade` (label and comment) → `N: quiet market`.
- `T: threshold branch` with `(rule CM)` → `T: threshold pair`. The tie rule moves to the caption, in words.
- The legend list: `N no trade` → `N quiet market`; `R mixed purchase` → `R mixed purchase that recruits`; `Q mixed orders` → `Q mixed orders at the entry floor`; `T threshold (CM)` → `T threshold pair`.
- `research branch` (both annotations) → `recruiting branch`.
- `equilibrium set not characterized` and `beyond $r_N$` go. The filled research figure (decision 2) draws:
  - zero research to \(r_N\);
  - recruiting research below the cap on \([r_R,r_{\lb})\), labelled `recruiting branch`, and at the cap on \([r_{\lb},r_C]\);
  - floor-entry research on \((r_N,r_Q)\), labelled `floor-entry branch`, and at the cap on \((r_C,r_2]\);
  - marks at \(r_R\), \(r_{\bar\lambda}\), \(r_N\), \(r_Q\) and \(r_C\). The `$r_U$` mark goes, as the lens plans say: \(r_U\) ends no drawn piece.
- The coexistence-region panel (decision 3) has the target-payoff spread \(\DT\) and the preparation threshold \(\tau\) on its axes, with the prior \(\pi\) marked on the threshold axis, and is labelled `coexistence region`.
- Docstrings, comments and log lines that still say "the thresholds r_A, ...", "threshold branch", "under rule CM", "benchmark path", "rules IM and C1", "Research branch", "cap=lambda_B" and "F_r" (the research polynomial) → "the marked strengths", "threshold pair", the tie phrases, "the example", "recruiting branch", "cap=lambda-bar(beta)" and "Lambda_r". Rule 3 covers committed text.

### S8, the prose writer (appendix and A9)

The rule-1 to rule-4 sweep of each file runs with the language scan; this list covers notation and vocabulary only. Part (b) lists the vocabulary lines by file.

**A1:**
- the tie codes (2);
- \(v\) → \(\theta\) at 59–65;
- \(\xi\) → \(\Gamma\) at 178–216 (9 lines), with A1's definition (part (c)).

**A2:**
- the tie codes (6);
- the path \(F_r\), declared once (S5).

**A3:**
- 4: "the admissible region at the benchmark" → "the recruitment region in the example";
- \(\mathcal E_0\) → \(\mathcal E_{\rm N}(F_0)\), \(\mathcal E_1\) → \(\mathcal E_{\rm F}(F_1)\), \(\mathcal E_2\) → \(\mathcal E_{\rm F}(F_2)\) at 31–138 (12 lines);
- the tie codes (4).

**A4:**
- the tie codes (59);
- \(\fr(d)\) → \(\fr(y)\) at 17–18;
- \(N_\tau,D_\tau\) → the numerator and denominator of \(\tau(r)\), written out, at 32–38;
- \(Q_J\) → \(\Xi_J\) at 43–48;
- 107, 110, 116, 120: "threshold" for a marked strength → "marked strength" (157's "the threshold" is \(\tau\) and stays). The caption at 116, "Thresholds of the benchmark path at calibration B", becomes "Marked strengths of the example at the prior \(1/2\)". The header at 120, "Threshold & Definition & Value at B", becomes "Strength & Definition & Value in the example".
- \(\mathcal C_{\rm CM}\) → \(\widetilde{\mathcal C}\) at 564–570;
- \(\Ent_R\), \(\Ent_F\), \(\Ent_T\) → \(\Ent_{\rm R}\), \(\Ent_{\rm F}\), \(\Ent_{\rm T}\) at 305–393 and 546;
- the form names of part (b) beside the bold letters at 267–271;
- "no informed trade" (9 lines) and "no trade" (1) → "a quiet market"; "informative equilibrium" (6) → "an informative market".

**A5:**
- The research outcome R is written with its qualifier on every line, so that the letter never means two tuples.
  - Below the cap: 128, 137, 148, 161, 178, 190, 194, 250, 278, 287, 290, 301, 302 and 362 → "R below the cap". On lines that speak of strengths (278, 287, 290, 301–302), "the recruiting branch" can stand instead. 287 then reads "R below the cap exists exactly on \([r_R,r_{\lb})\)".
  - At the cap: \((\bar{\rm R})\) at 131, 137, 164, 191 and 313 → "R at the cap", or "recruiting research at the cap" in running text.
  - The item labels of Lemma `lem:a5-middle` become "(R below the cap)" and "(R at the cap)"; 250 lists the set as "zero research and R below the cap".
- The tuple T → "the threshold pair" at 133, 138, 173 (the Step 4 header), 194, 251, 313 and 400. "Threshold equilibrium" at 387 and 400 → "the threshold pair". "The threshold entry" at 55 → "the entry of the threshold pair".
- \(z\) → \(\tilde\lambda\) at 65–79 (5 lines); \(z^*\) at 66 → \(\min\{\lb,\Psi/a\}\).
- \(\lambda_B(\beta)\) → \(\lb(\beta)\) at 373–378.
- \(\Ent_R\) → \(\Ent_{\rm R}\) at 278–280.
- The tie codes (19).
- The outcome Q, \(\lambda_Q\), \(\varphi_\rho\) and \(r_Q\), from S5.

**A6:**
- The signal example, 384–560:
  - \(T,Y\) → \(S_I,S_C\); the values \(t\), \(y\) → \(\pm\) (\(f_\pm\), \(\sigma_\pm\), \(S_I=\pm\), \(S_C=\pm\)) at 397–456;
  - \(\nu(x)\) → \(\nu_I(x)\) (9 lines); \(\nu\) stays the posterior vector at 279–352;
  - \(\phi_\pm\), \(\phi_y\) → \(\mu^C_\pm\); \(\mu_\pm\) → \(M^I,m^I\); \(I_\pm\), \(I_y\) → \(\zeta_\pm\); \(D^+\) → \(\bar\Delta_P\);
  - 540–541: "the threshold" → the public belief at which a challenger with \(S_C=+\) reaches \(\tau\) (part (b)).
- Single-letter renames elsewhere:
  - \(v\), \(v_*\) → \(\theta\), \(\theta_*\) at 167–194 and 265; \(t_v,g_v,W_v\) → \(t(\theta),g(\theta),F(\theta)\) at 245–247;
  - \(z\) → \(\mu_{\mathcal H}\) at 332–342;
  - \(w_j\) → \(\iota_j\) at 352;
  - \(z_0,z_1\) → \(\bar t(0),\bar t(1)\) at 371–373;
  - \(w\) → \(\psi\) at 362–379;
  - \(z\) → \(2\alpha_I-1\) and \(z_*\) → \(k/(m\rho\DT(r_1))\) at 507–510;
  - \(J\) → "finitely many classes" at 279;
  - \(\gamma\) → \(\varsigma\) at 354–355;
  - \(\mathcal L_i(\theta,R\mid j,S)\) at 11 and 22 → "the joint law of \((\theta,R)\) given \((j,S)\)", in words; \(\mathcal L\) stays the low group at 285–340.
- \(S\) at 9–29 stays the challenger's signal. The names "S(B)" and "B" at 467–521 → "the signal example" and "the example".
- \(H_C,H^0,H^1,L\) → \(\Phi,\Phi^0,\Phi^1,\bar c_0\) at 73–146.
- "trade margin" at 263 and 354 → "trading margin".
- The tie codes (6).

**A7:**
- the margins \(T,C,J\) at 196–200 → expressions;
- the order unit \(z\) at 72–76 → in words;
- the bargaining step at 119–124: \(z\) → \(\min\{R,\theta\}\), \(V\) → \(\max\{R,\theta\}\), \(P\) → \(T_\omega\);
- \(v\) and \(t_v,g_v,W_v\) → \(\theta\) and \(t(\theta),g(\theta),F(\theta)\1\{\theta\ge p\}\) at 146–158;
- \(\mathcal E_1\) at 26 → \(\mathcal E_{\rm F}(F_1)\);
- "trade margin" at 226 and 235 → "trading margin";
- "exclusion" for the reserve at 198 and 232 → "a reserve that excludes the low class";
- the tie code (1).

**A8:**
- \(A_r\) → \(w_r\) (22);
- \(\mathcal F\) → \(\mathcal E_{\rm F}\) (12);
- \(\vartheta\) at 8 and 39–40: defined as \(\lambda/(2b+\lambda)\), equal to \(M-m\) at the prior \(1/2\);
- the events \(A\), \(W\), the indicator \(Y\), \(w_x\) and \(y_x\) at 166–236 (18 lines) → \(\1_{\rm prep}\), \(\1_{\rm acq}\), \(W_F(\mu(x))\) and \(e(x)W_F(\mu(x))\), as part (c) writes them, before \(W_F\) is used;
- \(D_S\) → \(k/(\rho m)\) at 15;
- the price gap \(S\) at 41–81 → \(P(1)-P(-1)\); "spread" for the price gap at 80 and 131 → "the price gap";
- \(\bar P\) at 230–232 → \(\E[P(X)]\);
- \(\lambda'\), \(b'\), \(\beta'\), \(u'\), \(\vartheta'\) at 90–138 stay: the prime marks the alternative slot, and A5's research deviation takes \(\tilde\lambda\);
- the tie codes (9);
- "a quiet market" for N.

**A9:**
- 123: \(Q_J\) → \(\Xi_J\);
- 174: \(L\) → \(\bar c_0\);
- 183: \(\gamma\) → \(\varsigma\);
- 189: \(w\) and \(1-w\) → \(\psi\) and \(1-\psi\);
- 194–197:
  - \(\phi_\pm\) → \(\mu^C_\pm\) and \(\mu_\pm\) → \(M^I,m^I\);
  - the columns "\(S(B)\)" and "B" → "the signal example" and "the example";
- 201–204: the margins \(T,C,J\) → expressions;
- 231–247: the column labels \(C_0\), \(C_1\), \(T_0\), \(T_H\), \(T_L\), \(C_2\), \(O\) → words, each defined in the notes by its expression (for example "high-cost window", "recruitment", "trading-cost window", "purchase bound", "sale bound", "exclusion", "ownership");
- "Value at B" and every "B" header → "the example";
- the tie code (1).

Kept on purpose, so that the sweep does not treat them as leftovers:
- \(V\), the winner's value, goes in the bargaining step (A7:119–123), and \(\mathcal V_0\), the allocation value (A7:47–51), stays; neither is the old research value;
- the class proceeds \(t_1,t_2,t_3\) of the pooling example stay beside \(t_0\), because the classes there are numbered from 1;
- \(T_\omega\) stays (part (c));
- \(\Delta^1_x\), \(\Delta^0_x\) (A8:201–224) stay (part (c), **The spread as an argument**).

### S9 and S10, the prose writer (main text)

**Introduce the example** at the opening of Section 4.2. Before it, the text says "a stronger incumbent" rather than \(r\). This applies to 02:52–55, where \(r\) is the "uniform benchmark strength", and to Sections 3 and 4.1.

**Remaining sentences that use "benchmark"**, each with its vocabulary:
- 01:40–41: "which the benchmark meets", "the high-value class" → "which the example meets", "the high class" (S10);
- 01:95–96: "the spread between purchase and sale prices; in the benchmark" → "the price gap; in the example" (S10);
- 04:121, 04:131: "the admissible region at the benchmark auction" → "the recruitment region in the example";
- 05:46–53, 05:59, 05:102, 05:119, 05:138: "the benchmark" → "the example";
- 08:3–4, 08:11–12: "a further buyer", "the buyer prepares", "the benchmark auction" → "a challenger", "the challenger prepares", "the example";
- 08:28, 08:40: "price spread" → "price gap", "benchmark volume" → "the example's volume".

These are examples; rule 4 applies to every line part (b) counts.

**Vocabulary lines** (part (b) lists them all):
- the challenger: 01:13, 01:122, 06:79 ("buyer signal" → "challenger signal"), 08:13, 08:21, 08:78–79;
- 03:128: "the upper bound is the spread" → "and the spread bounds it from above";
- 04:173: "threshold belief" → "preparation threshold"; 04:302: "threshold branch" → "the threshold pair";
- 07:107: "exclusion" for the reserve → "a reserve that excludes the low class".

**Symbols:**
- 06:33–36: \(v_*\) → \(\theta_*\);
- 02:162–164: the Laplace scale \(s\) → \(\xi\);
- 07:27–28: the order unit \(z\) → in words ("if one order unit is a given number of shares per share of float, initial shareholders gain ... whenever that number is below \(\reg{p2_access_break_even}\)").

**Rule 3:** 05:3 → the rewrite in the rule card.

**Quiet market:**
- Define it at its first use, in Proposition 3, "Quiet and informative markets".
- Carry it through 01, 04, 05, 08 and 09, and the abstract (main.tex:79–82).

**"The research branch"** → "the recruiting branch" at:
- 05:44–58, 05:108–152;
- the rows of Table 3;
- the notes to Figure 3.

**Words for symbols:** "the recruitment margin" stands for \(\varphi_a\) and "the floor margin" for \(\varphi_\rho\) in Section 5.

**main.tex** (S10, with the abstract):
- 81: "high-value class" → "the high class";
- 57, the comment: "root of Delta_T(r) = d above ell" → "root of Delta_T(r) = y above ell".

### S11, the production assistant (slides and the comparison note)

**slides.tex:**
- 484 and 776: `\bar r_R` → `r_{\bar\lambda}`. The slides define no `\lb`, so the macro does not work there.
- 321, 678 and 685: "admissible region", "Admissible set" and "The admissible region at the benchmark set-up" → "the recruitment region" and "The recruitment region in the example".
- 387: "(H3) Ceiling at \(r_2\)" → "(H3) Exclusion at \(r_2\)".
- 366, 421, 754 and 796: "ceiling" refers to \(r_C\) each time. Write "entry ceiling".
- 548: "spread" for the price gap → "price gap"; 239, 241 and 412 keep "spread" for \(\DT\).
- 126, 195, 196, 239 and 617: "enter", "entrant" → "prepare", "challenger".
- 355: "threshold belief" → "preparation threshold"; 469, 740 and 747: "threshold" for a marked strength → "marked strength".
- 535 and 828: "exclusion" for the reserve → "a reserve that excludes the low class".
- 814: the Laplace scale \(s\) → \(\xi\).
- 612–626, the notation frame:
  - "benchmark class values" → "the example's class values";
  - "no entrant, \(H\) entrant, \(L\) entrant" → "no entry, a class-\(H\) challenger, a class-\(L\) challenger";
  - the rest checked against part (c).

**comparison.tex:**
- 36: `\rUR` → \(r_U\); 73: the sentence that explains the macro goes.
- The other set-up's strengths carry \({\rm Lap}\), \(r_N\) included.
- 301 and 691 spell `\bar\lambda`; the note has no `\lb`.
- Check the whole note against part (c). The note's own symbols that collide with the paper's: \(b\) (two meanings; the Laplace scale becomes \(\xi\)), \(s\), \(f\), \(A_H\), \(A_L\), \(\bar A\), \(A(M)\) (→ \(w_F\)), \(\beta^*\), \(e^*\), \(\Pi_L\), \(z\), \(J\), \(\gamma\) (separation → \(\varsigma\)), \(v\) (the sale size, beside the paper's volume and value) and \(Z\) (the noise demand, beside the research outcome Z). They stand at 96, 109–112, 130, 205, 210, 245–262, 286, 301, 303, 352, 410–411, 421 and 492. Each takes the paper's symbol where the object is the paper's, and a \({\rm Lap}\) superscript where it belongs to the other set-up.
- The tie codes (16) → the phrases.
- Every status label goes (decision 8; the language scan lists them).
- The vocabulary lines of part (b): "trade bound" (167, 422, 579, 688, 689) and "trade margin" (560, 673) → "trading bound", "trading margin"; "execution spread" (215, 352) → "the price gap"; "threshold" for marked strengths (464, 633, 724); "threshold flow" (263, 319); "the exclusion reserve" (225, 716); "admissible" (203, 355, 444).
