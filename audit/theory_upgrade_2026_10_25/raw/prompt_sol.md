You are a referee checking the mathematics of an economic theory paper. This is a READ-ONLY task: do not edit, create or delete any file in the repository. Report in your final message only.

Repository working copy (read it directly): /Users/austinli/Projects/competition-creates-competition/overleaf/slot
Entry point: main.tex. Main text in sections/, appendix in appendix/. Numbers print through \reg{key}; values in numbers.tex.

## The model in one paragraph
A challenger has class j in {H,L} with prior pi; given j its value theta ~ G_j on [0,inf), finite mean. Class ranking: G_H(y) <= G_L(y) for all y, G_H(p-) = G_L(p-) = 0. Incumbent value R ~ F continuous. Second-price auction with reserve p. t_j(F), g_j(F): expected target proceeds and challenger gross profit given entry in class j; t_0 without entry; Delta_T = t_H - t_L; tau = (c_H - g_L)/(g_H - g_L); W_j(F) = E_j[F(theta) 1{theta >= p}] the class-j win probability. Trading is one order slot (a modification of Dow and Gorton 1997): with prob. lambda the informed investor (knows j) places q in {-1,0,1} at cost k|q|; otherwise a liquidity trader sells/abstains/buys w.p. beta, 1-2beta, beta; b = (1-lambda) beta. Competitive prices P(x) = t_0 + e(x)[t_L - t_0 + Delta_T mu(x)]. The challenger sees the price and its cost C in {0,c_H}, Pr(C=0)=rho. Benchmark: point masses h=10, l=1, R ~ U[0,r].

The goal of the larger project: one unified model in which every theorem is stated at the generality its proof supports (general ranked G_H, G_L; a FOSD-ordered family of incumbent laws F; the benchmark only as a worked example), and where more is needed the theorem names the condition, not the benchmark.

## Your task: lens 1 (generality) for these results
- sections/03_competition_information.tex: Proposition 1 (prop:returns) and its proof in appendix/A1_payoffs.tex, including Proposition 1(c).
- appendix/A2_beliefs_trading.tex: lem:beliefs, cor:exclusion, lem:prices, lem:trading.
- appendix/A6_robustness.tex: A.3 prop:control (fixed information), A.4 prop:atomless (cost laws), A.5 prop:classes, A.6 prop:manyclasses, A.7 prop:signals.
- appendix/A7_welfare.tex: A.8 prop:access, A.9 prop:payment, A.10 prop:reserves.
- appendix/A8_empirical.tex: A.11 prop:spread, A.12 prop:informedshare, cor:purchasesonly, A.13 prop:winner, A.14 prop:announcement.
- the main-text sections that state or use these: sections/06_robustness.tex, 07_welfare.tex, 08_empirical.tex.

For each result: hypotheses as stated; what the proof actually uses step by step (closed forms, uniform F, point masses, prior 1/2, specific numbers); the most general statement the proof supports; precise conditions to add. Check this preliminary map and say where it is wrong:
- Already general: Propositions 1 and 2; the A2 lemmas; A.3; A.4; A.5; A.6; A.8; A.10.
- Benchmark-only but should follow from a reduction lemma (the slot game depends on the auction only through Delta_T(F) and tau(F), plus t_0 and t_L in price levels): A.11; A.12 and cor:purchasesonly; A.14 (indexed by r).
- Benchmark-only, real generalization: A.13. Its w_x = mu + (1 - mu) l/r should become mu W_H(F) + (1 - mu) W_L(F), and the claim that the gap rises needs a condition. Derive the general expression and the condition, and say whether the stronger incumbent can reverse the claim.
- Benchmark by design or low value: A.1 (admissible region), A.7 (complementary signals, needs l < r < h), A.9 (payment rule, point masses).

Also flag for each result every use of an auction object other than (Delta_T, tau, t_0, t_L): W_j, g_j levels, t_j levels, welfare/surplus terms, p^2/r and similar closed forms. For each, give the general replacement.

## Output format (final message, Markdown)
1. A table, one row per result: name | label | file:line | stated hypotheses | what the proof uses | most general supported statement | conditions to add | verdict on the preliminary map (agree/disagree and why).
2. A.13 in full: general win-gap formula, condition for the rise, a counterexample family if the rise can fail.
3. A list of every non-(Delta_T, tau, t_0, t_L) auction object used in these results, file:line, general replacement.
4. Anything wrong or overclaimed, file:line.
Cite file:line for every claim about the text. No hedging prose.
