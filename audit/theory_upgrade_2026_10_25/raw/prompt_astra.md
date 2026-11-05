You are a referee checking the mathematics of an economic theory paper. This is a READ-ONLY task: do not edit, create or delete any file in the repository. Report in your final message only.

Repository working copy (read it directly): /Users/austinli/Projects/competition-creates-competition/overleaf/slot
Entry point: main.tex. Main text in sections/, appendix in appendix/. Numbers print through \reg{key}; their values are in numbers.tex.

## The model in one paragraph
A challenger has class j in {H,L} with prior pi; given j its value theta ~ G_j on [0,inf), finite mean. Class ranking: G_H(y) <= G_L(y) for all y, and G_H(p-) = G_L(p-) = 0 (every value meets the reserve p). An incumbent has value R ~ F, continuous. Second-price auction with reserve p. t_j(F), g_j(F) are expected target proceeds and challenger gross profit given entry in class j; t_0 proceeds without entry; Delta_T(F) = t_H - t_L; tau(F) = (c_H - g_L)/(g_H - g_L) is the posterior at which a high-cost challenger is indifferent. Trading is one order slot (a modification of Dow and Gorton 1997): with prob. lambda the informed investor (knows j) places q in {-1,0,1} at cost k|q|; otherwise a liquidity trader sells/abstains/buys w.p. beta, 1-2beta, beta. Competitive prices; the challenger sees the price and its cost C in {0,c_H} (Pr(C=0)=rho) and prepares. The benchmark is point masses h=10, l=1, R ~ U[0,r].

## Your task: lenses 1 and 2 for appendix/A3_proposition2.tex, appendix/A4_coexistence.tex, appendix/A5_research.tex, and the main-text statements in sections/04_equilibrium_results.tex and sections/05_research.tex. Use appendix/A1_payoffs.tex and appendix/A2_beliefs_trading.tex as the toolkit.

Results in scope: Proposition 2 (prop:ccc) and its proof in A3; Proposition A.1 (prop:region); Proposition 3 (prop:coexistence) and its full statement and proof in A4, with Lemmas lem:a4-path, lem:a4-order, lem:a4-high, lem:a4-low, lem:a4-product; Corollary A.2 (prop:priors); Proposition 4 (prop:research), Lemmas lem:a5-joint, lem:a5-bounds, lem:a5-buy, lem:a5-middle, lem:a5-strong, Proposition A.2 (prop:researchregion), Remark rem:researchties, and the paragraphs "The branch at calibration B" and "Access to prices with research".

### Lens 1: generality
For each result above give: hypotheses as stated; what the proof actually uses, step by step (closed forms, uniform F, point masses, prior 1/2, specific numbers such as rho = 1/4 or tau < 3/4); the most general statement the proof supports for general ranked classes (G_H, G_L) and a first-order stochastically ordered family of continuous incumbent laws F_s; and any condition that must be added, stated precisely.

### Lens 2: the reduction lemma, ADVERSARIALLY
Proposed claim (treat it as a hypothesis to break, not a fact): "Fix pi, the slot (lambda, beta), rho, k and the tie rules. At any F with Delta_T(F) > 0 and g_H(F) > g_L(F), the set of equilibrium outcomes (order laws sigma_H, sigma_L; posteriors mu(x); entry e(x) after each order) depends on the auction (F, G_H, G_L, p, c_H) only through (Delta_T(F), tau(F)). Prices are then P(x) = t_0 + e(x)[t_L - t_0 + Delta_T mu(x)], so price levels also use t_0 and t_L. With research (condition E7) the same holds." Try hard to find a step anywhere in A2-A5 that uses more than (Delta_T, tau): e.g. price ordering/injectivity needing w_L = t_L - t_0 >= 0 or w(tau) > 0; ties under rule CM where two orders share posterior tau with different entry; tau <= 0 or tau >= 1; ownership or win probabilities W_j(F); welfare terms; t_0 in "access to prices". State for each use whether it breaks the claim or only adds a side condition.

Also check these specific candidate generalizations, each one adversarially (prove or give a counterexample):
(a) Monotonicity: under the class ranking, along a FOSD-increasing family, Delta_T weakly increases, g_H and g_L weakly decrease, g_H - g_L weakly decreases (via the split identity Delta_T + g_H - g_L = E_H max(theta,p) - E_L max(theta,p)), so tau weakly increases when c_H > g_L; Delta_T * tau weakly increases. J = Delta_T (1 - tau) has no general sign.
(b) Pointwise coexistence at a general prior: no informed trade and an informative equilibrium coexist at F iff J(F) >= k, pi < tau(F) <= M(pi), and rho Delta_T(F) max{pi, 1-pi} <= k (rules IM, C1). At such F the informative equilibrium is unique and its entry is rho + (1-rho) min{(1-pi) b Delta_T/k, b + pi lambda}, a nondecreasing function of Delta_T alone.
(c) Along a FOSD path, the coexistence set is an interval whenever {s : J(F_s) >= k} is an up-set; at prior 1/2 it is [s_A, min(s_N, s_C)] intersected with {tau > 1/2}. Which further conditions recover the benchmark ordering r_0 < r_A < r_F < r_N < r_J < r_S < r_1 < r_C < r_2 and the table of the full statement?
(d) Existence at prior 1/2: at every F with Delta_T > 0, g_H > g_L and tau(F) > 1/2, an equilibrium exists under rules IM and C1 (case split: rho Delta_T/2 <= k gives N; otherwise Q, R or F). Is this right? What about tau >= 1?
(e) Corollary A.2 cases (a)-(d): which of J strictly increasing, tau strictly increasing, Delta_T tau strictly increasing, tau_A < 1 - rho, continuity along the path are needed?
(f) Research (prior 1/2): lambda_R depends on F only through Delta_T, as a C^1 strictly increasing function of Delta_T on Delta_T > 2k; entry on the branch rises with Delta_T; ownership equals (1/2) W_H(F) [rho + (1-rho)(beta + (1-beta) lambda_R)], so its rise needs a condition (W_H = 1 on the path, i.e. the high class outbids every incumbent, or a stated trade-off). The branch start solves phi_a = J - k - 2a lambda_E(tau) = 0, which needs a single-crossing condition; s_R >= s_A always; the branch is an interval [s_R, s_bar_R) under single crossing of phi_a and s_bar_R <= s_N. Check each.
(g) Proposition 2 and A.1: is Proposition 2 already general (as its statement suggests)? Is A.1 calibration-only?

## Output format (final message, Markdown)
1. A table, one row per result: name | label | file:line | stated hypotheses | what the proof uses beyond Delta_T and tau | most general supported statement | conditions to add.
2. Reduction lemma: verdict, a precise statement you would sign, and the list of every use of auction objects other than (Delta_T, tau), with file:line and whether it breaks the claim.
3. Verdicts on (a)-(g): proved / false (with counterexample) / needs condition X.
4. Anything else wrong or overclaimed that you find in these files, with file:line.
Be concrete; cite file:line for every claim about the text. No hedging prose.
