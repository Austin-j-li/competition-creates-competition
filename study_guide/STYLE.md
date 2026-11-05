# Style sheet for the study guide

This file sets the rules for every chapter of the guide. Read all of it before you write or edit a chapter.

## 1. The reader

The reader is an economics undergraduate.

- The reader knows basic probability: events, conditional probability, expectation, and a distribution function.
- The reader is slow with mathematical derivations. A skipped step stops the reader.
- The reader learns the mechanism first and checks it afterward. Numerical examples confuse this reader.
  Qualitative statements help: a direction of change, which condition binds, what happens at an extreme.

The aim: after the guide, the reader can explain each result in words and rebuild each derivation alone.

## 2. Source

The source is the order-slot manuscript in `../overleaf/slot/` (revision 5bad2bc, 26 October 2026).

- Main text: `sections/01_introduction.tex` to `sections/09_conclusion.tex`.
- Proofs and full statements: `appendix/A1_payoffs.tex` to `appendix/A9_parameters.tex`.
- Read the `.tex` files directly. Do not use any older guide, lesson, handout, or the Laplace manuscript.
- Every claim about the paper must have a source line. Do not add results that the paper does not state.
- When the guide adds its own illustration or analogy, say so in the text ("an analogy", "a picture to keep in mind").

## 3. Shape of a chapter

Use this order. Small chapters can merge steps.

1. `chapterplan` box: the question of the chapter in one sentence, then three to five things the reader will be able to do.
2. Intuition first. A short story in words, often with an `analogy` box. Each analogy states where it breaks.
3. The set-up. Define every symbol at its first use in the chapter, in words, even if an earlier chapter defined it.
   A reminder such as "recall that \(\rho\) is the probability that preparation costs nothing" is enough.
4. The derivations (section 4 of this sheet).
5. After each derivation, a short "what this says" paragraph or an `intuition` box.
   Then test the result at an extreme case in words: what happens when \(\rho\) is near zero, when the spread is zero, when the investor is never present.
6. For each result of the paper: a `paperresult` box with the exact statement and hypotheses, a plain reading of each line,
   then the proof as a sequence of numbered steps, with all algebra filled in.
7. A `watchout` box for each hypothesis or distinction that is easy to lose: why it is there and what fails without it.
8. Three to six `checkyourself` boxes in the chapter, placed where they fit. Each question has a label.
   The full worked answers go at the end of the chapter under `\answersection`, one `\answer{\ref{label}}{...}` each.
9. A `chaptersummary` box with four to seven sentences.

## 4. Derivations

This is the most important rule of the guide. Do not skip a step.

- Put each algebraic step on its own line in an `align*` (or `align` with a label).
- Name the rule at each step with `\why{...}`: "Bayes' rule", "divide numerator and denominator by \(\pi\)",
  "the cost is independent of the class", "substitute (4.3)", "\(F(y)=1\) for \(y\ge\bar r\)".
- Put long derivations inside a `derivation` box. The box can break across pages.
- Do not write "clearly", "obviously", "it is easy to see", "simple algebra gives", "it follows immediately", or "one can show".
  If the paper skips a step, fill the step in.
- When a step uses a tool from Chapter 2, cite it: "the tail formula (Section~\ref{sec:toolkit-tail})".
- When an integral appears, say in words what it adds up before you compute it.
- When an inequality changes direction, say why (for example, "multiply by \(-1\)").
- Check every step yourself. An error in a guide is worse than a gap.

## 5. Numbers

- Chapters 1 to 13 contain no decimals and no numerical examples.
- Work with symbols. The paper's example uses two point-mass classes \(h\) and \(\ell\), a reserve \(p\), and an incumbent uniform on \([0,r]\).
  Derive its formulas in these symbols and describe their shape (rising, falling, zero at \(r=\ell\)).
- When a chapter discusses one of the three figures, describe the shapes and name the marked strengths
  (\(r_A\), \(r_F\), \(r_N\), \(r_C\), and so on) without their values. Point to Appendix~\ref{app:numbers} for the values.
- Simple fractions inside an algebraic identity are fine (\(\tfrac12\), \(1/(2+u)\)). A worked numerical case is not.
- If a number is truly necessary, print it with `\reg{key}` from `source/numbers.tex`. Never type a value by hand.

## 6. Language

Write about 80% of the way to ASD-STE100. Soften it where mathematics needs it.

- Descriptive sentences: about 25 words at most. Instructions: about 20 words at most.
- One topic in each paragraph, six sentences at most.
- Noun clusters: three words at most.
- Active voice where an actor exists. Passive voice is fine when it is necessary.
- Simple verb forms. Avoid -ing forms except in fixed names. Avoid the perfect tense.
- Simple words: "use", not "utilize"; "start", not "commence"; "before", not "prior to".
- Keep "the", "a", and "this".
- Use vertical lists for complex text.
- Address the reader as "you" where it helps. Refer to the paper as "the paper" and to its author as "the author" only when needed.

Avoid these marks of machine prose:

- "Not X but Y" and "it's not just X, it's Y" contrasts.
- Staged openers ("Here's the thing", "Let's dive in", "Now, the key insight").
- Triads for rhythm, one-line closing sentences for effect, rhetorical questions as section ends.
- Inflated words: "crucial", "powerful", "elegant", "remarkable", "delve", "landscape", "nuanced".
- Em dashes as general punctuation. Use a full stop, a comma, or a colon.
- Bold labels at the start of paragraphs, except inside the defined boxes.

## 7. Vocabulary

Use the paper's words. One word keeps one meaning.

| Use | Meaning |
|---|---|
| incumbent | the buyer that has already prepared; value \(R\), distribution \(F\) |
| challenger | the buyer that decides whether to prepare |
| class \(H\), class \(L\); the high class, the low class | the challenger's quality class |
| prepare, preparation; entry | the challenger pays its cost; entry is the probability that it prepares |
| preparation cost \(C\); zero-cost challenger; high-cost challenger | \(C\in\{0,c_H\}\) |
| target proceeds; target-payoff spread \(\DT\) | what the target receives; \(t_H-t_L\) |
| gross acquisition profit \(g_j\), \(B(\mu)\) | the challenger's expected profit before its cost |
| preparation threshold \(\tau\) | the belief at which \(B(\mu)=c_H\) |
| order slot; informed investor; liquidity trader; market makers | the trading set-up |
| posterior, belief; top posterior \(M(\pi)\), bottom posterior \(m(\pi)\) | beliefs about the class |
| class ranking; equal admissibility; decisive advantage | the paper's named conditions |
| strengthening; path; strength \(r\) | first-order stochastic shifts of \(F\) |
| quiet market; informative market; recruit, recruitment | equilibria of Chapter 9 |
| exclusion bound; trading bound; entry floor; entry ceiling \(r_C\) | named bounds |
| default tie rules | an indifferent investor may mix; an indifferent high-cost challenger prepares |
| the example | the point-mass classes with a uniform incumbent |

Do not use:

- "benchmark" for the example. Say "the example".
- Status labels: "analytical", "computer-assisted", "numerical diagnostic", "open" as a status. Say "holds for every ..." or "holds in the example".
- Pipeline words: registry, script, certificate, verified, checker, pipeline, calibration, file names, keys.
- Development-log words about the paper: "new", "now", "no longer", "updated", "revised", "this version", "previously".
- Names of software tools, agents or models.

## 8. Fidelity checklist

Each item below is a mistake that an earlier draft made. Keep every hypothesis.

1. The price reveals the market makers' posterior only when the spread is positive and the entry floor \(\rho\) is positive.
   With a zero spread the price does not move with the posterior.
2. The fixed-information control keeps price information only with a positive spread in each economy that it compares.
3. The signal extension needs the signal to be independent of the auction values given the class.
4. A statement that the price is affine in the posterior holds at a fixed level of entry. Equilibrium prices also reflect entry.
5. In the payment-rule results, the weights give weak directions of the spread. A strict change needs a strict change in the positive-part expectation.
6. Domains of \(\beta\): the posterior bounds common to all orders and the exclusion bound use \(\beta\le 1/3\).
   Proposition 2 states \(0<\beta<1/2\). Copy the domain of each result. Do not harmonize them.
7. Weak and strict: Proposition 1 gives weak inequalities. Strictness needs the integral conditions that the paper states.
8. Tie rules: Proposition 2 holds under all four tie rules. Propositions 3 and 4 use the default tie rules. State the tie rule of each result.
9. Proposition 4 and the research chapter fix the prior at \(1/2\).
10. A stronger incumbent never lowers the threshold only while \(g_L\le c_H\).
11. The clean rise of high-class ownership needs class \(H\) to outbid the stronger incumbent, \(W_H(F_1)=1\).
12. Entry is the probability that the challenger prepares. It includes the zero-cost floor \(\rho\).
13. Comparisons across incumbent strengths solve the equilibrium again in each economy. A deviation faces fixed prices and entry.

## 9. LaTeX

- Write only your own file in `chapters/`. Start it with the `\chapter{...}\label{...}` line that is already there.
- Use only the macros and environments in `preamble.tex`. Do not add packages or `\newcommand` in a chapter.
- Manuscript macros: `\E`, `\1`, `\DT`, `\Ent`, `\Own`, `\lb`, `\fr`, `\eu`, `\Cov`.
- Labels carry the chapter key: `sec:auction-tail`, `eq:beliefs-bayes`, `q:trading-sign`, `fig:coexistence-path`.
- Chapter keys: `ch:story`, `ch:toolkit`, `ch:model`, `ch:auction`, `ch:beliefs`, `ch:trading`, `ch:ccc`, `ch:example`,
  `ch:coexistence`, `ch:research`, `ch:robustness`, `ch:welfare`, `ch:empirical`, `app:numbers` (the chapter of example values).
- Toolkit section labels that other chapters can cite: `sec:toolkit-bayes`, `sec:toolkit-odds`, `sec:toolkit-cdf`,
  `sec:toolkit-expectation`, `sec:toolkit-tail`, `sec:toolkit-maxmin`, `sec:toolkit-fosd`, `sec:toolkit-games`, `sec:toolkit-monotone`.
- Refer to the paper's results by their paper numbers: Proposition 1 to 4, Corollary 1 to 3, and the appendix numbers (Lemma A.2, Proposition A.4).
- Figures: `\includegraphics[width=\linewidth]{beliefs}`, `{coexistence}`, `{research}`, inside a `figure` with a caption in your own words.
- Simple TikZ diagrams are welcome (a timeline, a probability tree, a number line). Keep them inside the text width.
- Build your chapter with `./build.sh <file name without .tex>` from `study_guide/`. Fix every error, every overfull line wider than 2pt, and every undefined control sequence.
  References to other chapters show as ?? in a one-chapter build. That is expected.
