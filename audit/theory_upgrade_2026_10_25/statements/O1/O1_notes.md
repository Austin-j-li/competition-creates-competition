# O1. Where floor-entry research ends

Report of the mathematics writer to the coordinator, 25 October 2026. This folder holds the LaTeX fragment for the example part of Appendix A.5 (definitions, Lemma `lem:a5-floor` with equation `eq:a5-floor`, proof, and a short reading of the result); the print-only program that computes every bound the proof cites; this report; and the referee's report. Nothing is committed. Section 9 lists the notation pass of S4, which the referee checks.

## 1. Result

Setting: the example at the prior 1/2 (uniform incumbent on [0, r], h = 10, ell = 1, p = 1/2, rho = 1/4, c_H = 6, k = 1/50, beta = 294655/10^6, 1 + u = e), research cost a = 1/40 and cap lambda_bar = u beta/(1 + u beta), on r in [r_0, r_2] = [6/5, 18/5], when an indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares.

(a) The floor margin phi_rho(r) = rho Delta_T(r) [1 - tau(r)] - k - a lambda_E(r) rises strictly on [r_0, r_2]. Its unique zero is r_Q = 2.166995158219286 (display 2.166995), and r_N < r_Q < r_U < r_C. On (r_N, r_C], tau(r) exceeds the top posterior M_lambda at lambda = min{lambda_Q(Delta_T(r)), lambda_bar} exactly on (r_N, r_Q), and equals it exactly at r_Q and at r_C.

(b) Floor-entry research is an equilibrium exactly on (r_N, r_Q) and on (r_C, r_2], with entry rho. The root lambda_Q(Delta_T(r)) reaches the cap at r_U = 2.434046: lambda_Q(Delta_T(r)) >= lambda_bar exactly when r >= r_U. On [r_N, r_Q], lambda_Q(Delta_T(r)) stays below the cap and rises strictly from 0 to lambda_E(r_Q) = 0.234257. Above r_C research is at the cap.

(c) Recruiting research at the cap is an equilibrium exactly on [r_lambda_bar, r_C] = [1.677633, 3.592659], with entry 0.522757.

(d) On (r_N, r_Q) the equilibria are exactly these two. On [r_Q, r_C] recruiting research at the cap is the unique equilibrium. On (r_C, r_2] floor-entry research at the cap is the unique equilibrium.

The questions the brief adds:
- Where lambda_Q(Delta_T(r)) reaches the cap: at r_U = 2.434046, before r_C = 3.592659 and after r_Q. Condition (U) of `lem:a5-strong` says exactly that the floor-entry root is above the cap, and it holds exactly when r > r_U. On the range (r_N, r_Q) where floor-entry research is an equilibrium, its research stays below lambda_E(r_Q) = 0.234257 < lambda_bar = 0.336122.
- The end at r_N: lambda_Q is 0 there (rho Delta_T(r_N) = 2k), and floor-entry research needs positive research. At r_N the equilibria are zero research (an order at the prior just pays k, so each class may mix between its full order and no order) and recruiting research at the cap with sigma_L(-1) = hat-s_-(r_N)/lambda_bar = 0. This follows from the case analysis of Step 6: at r_N, with positive research and a purchase posterior below the threshold, the purchase would earn rho Delta_T m_lambda - k < 0, and in the recruiting case any sale rate above 0 makes the sale lose. So the coexistence of research at the cap with zero research, which Section 5 and Appendix A.5 state on [r_lambda_bar, r_N), also holds at r_N. As r falls to r_N, lambda_Q(Delta_T(r)) falls to 0.
- The end at r_Q: the purchase posterior at research min{lambda_Q, lambda_bar} equals the threshold; the indifferent challenger prepares, the purchase recruits, and floor-entry research fails. The same happens at r_C with research at the cap. Both ends are excluded.
- Above r_C: floor-entry research at the cap, with entry rho, is the unique equilibrium (Lemma `lem:a5-strong`, which applies because r > r_C > r_U and M at the cap is below tau(r)).

## 2. Definitions (paper notation)

- lambda_Q(Delta_T), for rho Delta_T >= 2k: the unique lambda in [0, 1) with a lambda = rho Delta_T m_lambda - k. The gap rho Delta_T m_lambda - k - a lambda falls strictly in lambda (from rho Delta_T/2 - k >= 0 to -k - a) and rises strictly in Delta_T, so the root is unique, positive when rho Delta_T > 2k, and rises strictly and continuously in Delta_T. The research of floor-entry research is min{lambda_Q(Delta_T), lambda_bar}, written out. After clearing 2 beta + (1 - 2 beta) lambda the equation is a(1 - 2beta) lambda^2 + [rho Delta_T beta + k(1 - 2beta) + 2a beta] lambda + beta(2k - rho Delta_T) = 0, whose positive root is -2C/(B + sqrt(B^2 - 4AC)); the proof uses only the monotone gap, and the program uses the quadratic.
- Floor-entry research (rho Delta_T(r) > 2k): research min{lambda_Q(Delta_T(r)), lambda_bar}, class H buys, class L sells, posteriors (m, 1/2, M) at that research, no preparation by the high-cost challenger, prices t_0 + rho w(mu), entry rho.
- Recruiting research at the cap: research lambda_bar, class H buys, class L sells with probability sigma_L(-1) = hat-s_-(r)/lambda_bar, where hat-s_-(r) = min{lambda_bar, b_bar [rho Delta_T(r)/k - 2]^+} is the low-class sale rate of `lem:a4-low` at the presence lambda_bar and b_bar = (1 - lambda_bar) beta, and abstains otherwise; class L abstains up to r_N, mixes on (r_N, r_S) with its sale just paying k, and sells with probability one from r_S = 2.124148; only the purchase recruits; entry rho + (1 - rho)[beta + (1/2 - beta) lambda_bar].
- Floor margin phi_rho(r) = rho Delta_T(r) [1 - tau(r)] - k - a lambda_E(r). Since m at lambda_E(r) equals 1 - tau(r), phi_rho(r) is the gap rho Delta_T(r) m_lambda - k - a lambda at lambda = lambda_E(r). It is a rational function of r with rational coefficients; Euler's number does not enter.
- r_Q: the zero of phi_rho on [r_0, r_2].

## 3. The argument in words

The plan names the difficulty: tau(r) and the top posterior at floor-entry research both rise with strength. The proof turns the comparison of the two into the sign of one function.

1. Facts along the path (Step 0). Delta_T and tau rise; 1/2 < tau(r) <= tau(r_2) = 4245/5804 < 1; lambda_E(r) <= lambda_bar exactly when r <= r_C. Existing margins give r_U < r_1 < r_C < r_2 ((U) at r_1, margin 0.016421; M_cap - tau(r_1) = 0.026059; tau(r_2) - M_cap = 0.000334) and r_lambda_bar < r_N (margin 0.070245). Since m at the cap is 1/(1 + e), the gap at the cap, rho Delta_T(r) m_lambda_bar - k - a lambda_bar, is nonnegative exactly when r >= r_U, so lambda_Q(Delta_T(r)) is at or above the cap exactly when r >= r_U.
2. The comparison (Step 1). On (r_N, r_C], lambda_E(r) <= lambda_bar. Then tau > M at min{lambda_Q, lambda_bar} iff min{lambda_Q, lambda_bar} < lambda_E iff lambda_Q < lambda_E (the cap cannot bind below lambda_E) iff the gap at lambda_E is negative (the gap falls in lambda and vanishes at lambda_Q) iff phi_rho(r) < 0. Equality tau = M at min{lambda_Q, lambda_bar} holds iff phi_rho(r) = 0 or lambda_bar = lambda_E(r) <= lambda_Q, and the second case is r = r_C.
3. Monotonicity (Step 2). phi_rho' = rho[Delta_T'(1 - tau) - Delta_T tau'] - a beta tau'/{beta + (1 - 2beta)(1 - tau)}^2. On a piece [r_-, r_+] each factor is bounded by its value at an end (Delta_T', Delta_T, tau rise; 8r^2 - r + 2 rises; 20r - r^2 - 1 is positive and rises; the denominator {beta + (1 - 2beta)(1 - tau)}^2 of the last term falls as tau rises), which gives the piece bound, the right side of the display in Step 2. On the 24 pieces of width 1/10 that partition [6/5, 18/5], exact rational arithmetic gives a piece bound of at least 1/100; the smallest piece bound is 0.011748 on [6/5, 13/10].
4. The zero (Step 3). phi_rho(r_N) = k(1 - 2 tau(r_N)) - a lambda_E(r_N) < 0, because rho Delta_T(r_N) = 2k. On [r_U, r_C], phi_rho = [rho Delta_T m_lambda_bar - k - a lambda_bar] + rho Delta_T (M_cap - tau) + a(lambda_bar - lambda_E): the first term is the margin of (U), nonnegative from r_U and zero only at r_U; the other two are nonnegative and zero only at r_C. So phi_rho > 0 on [r_U, r_C], and the unique zero r_Q lies in (r_N, r_U). Exact signs of phi_rho at rational strengths locate r_Q.
5. Existence of floor-entry research (Step 4): (E1) to (E7) condition by condition; both trades earn rho Delta_T m_lambda_hat - k >= a lambda_hat > 0, so both are strict; research optimality holds whether the root is below or at the cap. The tuple fails exactly when tau <= M at its research, because the indifferent challenger then prepares after a purchase. With Step 1: (r_N, r_Q); above r_C the research is at the cap and tau > M_cap.
6. Existence of recruiting research at the cap (Step 5): (E1) to (E7) with the sale rate hat-s_-(r); the purchase earns at least 2a lambda_bar from r_lambda_bar on; class L's three regimes (abstain, mix with zero sale profit, sell) are each consistent with (E5) when an indifferent investor may mix. Orders with equal posteriors (the sale and no order, once, at r = 1.911775) have equal entry rho and share a price. Outside [r_lambda_bar, r_C] the tuple fails: (E3) above r_C, (E7) below r_lambda_bar.
7. Every equilibrium above r_N (Step 6). Zero research fails because an order at the prior pays. Positive research gives a strict full purchase and entry rho after the other orders (`lem:a5-buy`). If the purchase posterior is below tau, class L sells strictly, research solves the floor-entry equation or sits at the cap, and the tuple is floor-entry research. If it reaches tau, research is at the cap (the recruiting gap Delta_T m_lambda - k - 2a lambda is positive below the cap from r_lambda_bar on), the low-class sale rate s_- = lambda_bar sigma_L(-1) is pinned down by (E5), and the tuple is recruiting research at the cap. On (r_C, r_2], `lem:a5-strong` gives uniqueness.

## 4. Printed lines

Command (from a private scratch folder): `python3 -I` followed by the program's path. Exit status 0, 345 lines, about 0.1 seconds. The program keeps the draft's labels in its printed lines ("floor root" for lambda_Q, "b" for the piece bound); the mathematics is the same.

```
  e in [2.718281828459045235360287471352, 2.718281828459045235360287471353]  (partial sum to n = 40, tail at most 2/41!)
  cap lambda_bar = u beta/(1 + u beta) in [0.336121768915121197397183, 0.336121768915121197397184]  -> 0.336122
  r = 6/5   differences (integration minus closed form): t0 0, tH 0, tL 0, gH 0, gL 0 ; Delta 0 ; tau 0 ; tau display form 0
  (the same at 7/4, 2, 3, 18/5)
  [1.2, 1.3]  b = 0.011748   phi'(l) = 0.012371   phi'(u) = 0.016714   b <= min(phi'(l), phi'(u)): True
  [2.1, 2.2]  b = 0.026430   phi'(l) = 0.027666   phi'(u) = 0.027680   b <= min(phi'(l), phi'(u)): True
  [3.5, 3.6]  b = 0.017539   phi'(l) = 0.019321   phi'(u) = 0.018274   b <= min(phi'(l), phi'(u)): True
  number of pieces: 24 ; last right end equals r_2: True
  smallest b: 0.011748047 (rounded down), on [6/5, 13/10]
  smallest b at least 1/100: True
  exact smallest b: 5993292043494701003/510152171246294601024
  For comparison, single pieces: b(6/5, 7/4) = 0.006898, b(17/10, 5/2) = 0.013251, b(5/2, 18/5) = 0.004775, b(17/10, 18/5) = -0.025271
  r_N: rho Delta = 2k, Delta = 4/25; bracket [1.7478775382679627435673, 1.7478775382679627435674]
  r_U:   Delta = (k + a cap)(1 + e)/rho; bracket [2.4340455267120011352542, 2.4340455267120011352543]; closed form [2.4340455267120011352542, 2.4340455267120011352543]
  r_C:   tau = e/(1 + e);               bracket [3.5926585187946618333359, 3.5926585187946618333360]
  phi(r_N) in [-0.011391206780, -0.011391206779] (sign -1)
  phi(r_U) in [0.007346374635, 0.007346374636] (sign 1); (U) margin rho Delta m_cap - k - a cap at r_U in [-0.000000000001, 0.000000000001]
  phi(r_C) in [0.034495762698, 0.034495762699] (sign 1); (U) margin at r_C in [0.034495762698, 0.034495762699]
    r_N < r_S: True   (1.747878 < 2.124148)
    r_S < r_Q: True   (2.124148 < 2.166995)
    r_Q < r_U: True   (2.166995 < 2.434046)
  bracket [2.166995158219285882282487, 2.166995158219285882282488], width 5.92e-31; undecided midpoint: None
  r_Q = 2.166995158219286 (15 decimals) -> display 2.166995
  tau(r_Q) in [0.670861712856090467, 0.670861712856090468] -> 0.670862
  lambda_E(r_Q) in [0.234257256065633848, 0.234257256065633849] -> 0.234257
  floor root minus lambda_E at the left end:  [-0.000000000001, 0.000000000000] (sign -1)
  floor root minus lambda_E at the right end: [0.000000000000, 0.000000000001] (sign 1)
  floor root at r_Q below the cap: True  (cap 0.336122)
```

Section 9 of the output tabulates, at 16 strengths from 1.75 to 3.6, lambda_Q, whether it is capped, the top posterior at floor-entry research, tau, and the signs of tau - M and phi_rho: they are opposite at every strength up to 3.59 and both positive at 3.6, above r_C. Section 10 builds the two tuples from the auction rules (prices from the terminal values, payoffs from the prices) and prints (E2), (E3), (E5) and (E7):
- floor-entry research at 9/5, 2, 21/10, 43/20: prices distinct, no preparation consistent with the beliefs, both trades strict best, research optimal to within 2e-58; at 11/5 (above r_Q) the high-cost challenger's gross profit at the purchase price exceeds c_H, so (E3) fails, as the lemma says; at 18/5 (above r_C, research at the cap) all hold;
- recruiting research at the cap at 17/10, 7/4, 9/5, 2, 21/10, 11/5, 3, 7/2: all hold, entry 0.522757 at each; class L ties between the sale and abstention exactly at 7/4, 9/5, 2 and 21/10 (sale probability sigma_L(-1) = 0.005196, 0.129328, 0.654724, 0.931856); at 18/5 (E3) fails, as the lemma says.

Section 11 prints each relied-on row of the numbers table beside its display; all 32 agree ("same"), none differs.

## 5. Proposed rows of the numbers table

| name | exact value | display | meaning |
|---|---|---|---|
| `res_rQ` | the zero of phi_rho; 2.166995158219285882282487 < r_Q < 2.166995158219285882282488 | 2.166995 | end of floor-entry research below the entry ceiling; uniqueness under the default rules from here |
| `res_lambda_floor_rQ` | lambda_E(r_Q) in [0.234257256065633848, 0.234257256065633849] | 0.234257 | research of floor-entry research at r_Q |
| `res_floor_step` | 1/10 | 1/10 | width of the pieces in the bound on phi_rho' |
| `res_floor_dphi_lb` | 1/100 | 1/100 | lower bound on phi_rho' over [r_0, r_2]; the smallest piece bound is 5993292043494701003/510152171246294601024 = 0.011748... |

The names `res_rQ` and `res_lambda_floor_rQ` are the ones the lens plans propose. Existing rows the fragment prints: `res_a`, `res_cap`, `tau_r2`, `margin_res_bound_r1_B`, `margin_res_tau_r1_B`, `margin_res_tau_r2_B`, `margin_res_rN_B`, `res_entry_cap`. Rows the argument relies on through symbols: `res_rN`, `res_rcap`, `res_rUR`, `res_rC`, `rS_B`.

## 6. Dependencies and placement

- Cited objects: Lemmas `lem:a4-low` (the sale rate hat-s_-), `lem:a5-joint`, `lem:a5-bounds` (a) and (c), `lem:a5-buy`, `lem:prices` (b) to (d), `lem:a5-strong`; displays `eq:a5-U`, `eq:a2-terminal`, `eq:a5-payoffs`; the paragraph on constructed tuples in `app:beliefs`; the formula for d lambda_E/d tau in the paragraph on derived functions of A.5; the root map frak_r of A.4; B_r(1/2) = 5 - r/4 + 1/(8r).
- The proof recalls the definitions of r_N, r_lambda_bar, r_U and r_C in one sentence; when S8 defines them earlier in the example part, that sentence shortens to a pointer.
- Overlap with the general lemmas of area C. Step 6 (every equilibrium above r_N is one of the two tuples) and the sale rate restate on the path what `lem:a5-outcomes` and `lem:a5-sale` give in general; `statements/C.tex` states both. The fragment proves them from the lemmas that exist today, so it stands on its own; at the transplant, Step 6 can cite `lem:a5-outcomes`. That lemma, as stated in `statements/C.tex`, says at the prior 1/2 when an indifferent investor may mix and an indifferent high-cost challenger prepares, with tau > 1/2: zero research exists exactly when rho Delta_T <= 2k; recruiting research, with research min{lambda_R, lambda_bar}, exists exactly when Delta_T > 2k and 1/2 < tau <= M at that research; floor-entry research exists exactly when rho Delta_T > 2k and tau > M at min{lambda_Q, lambda_bar}; and every equilibrium is one of the three, each with a unique tuple.
- Placement: in the example part of A.5, with the outcome list on the path and before the research-parameter-region proposition. The lemma's part (d) for [r_Q, r_C] carries the plan's "uniqueness under the defaults from r_Q". Corollary 3 (full statement) in `statements/C.tex` draws its three-outcome list on the path from this lemma.

## 7. Beyond the plan's wording

1. "Ends once, and nowhere else before the entry ceiling." The exact form: on (r_N, r_C], tau equals M at min{lambda_Q, lambda_bar} exactly at r_Q and at r_C. The second point is the ceiling itself, where research at the cap makes the purchase posterior e/(1 + e) = tau(r_C). Uniqueness of r_Q holds on (r_N, r_C), which leaves out r_C, and the lemma states both points.
2. lambda_Q(Delta_T(r)) reaches the cap at r_U, which also starts condition (U). This connects the two cap ranges of Figure `fig:research`: from r_U on, floor-entry research would sit at the cap, but it is an equilibrium there only once a purchase at the cap fails to recruit, above r_C.
3. r_S = 2.124148 < r_Q. On the coexistence range (r_N, r_Q), recruiting research at the cap has class L mixing on (r_N, r_S) and selling with probability one on [r_S, r_Q). Research is at the cap at r_N and at r_S, so the low class's sale leaves research unchanged on the example path.
4. The monotonicity covers the whole path [r_0, r_2]. One piece over [17/10, 18/5] gives a negative bound (-0.025271). A shorter route uses one piece [17/10, 5/2] (bound 0.013251) together with r_N > 17/10 (from r_N = (29 + 6 sqrt 6)/25) and r_U < 5/2 (which needs one more margin row); the 24-piece version needs no extra comparison and gives the sign of phi_rho on the whole path.
5. Tie rules. Floor-entry research has strict trade choices, and away from r_Q and r_C no challenger tie, so its existence on (r_N, r_Q) and (r_C, r_2] holds under either investor rule. Recruiting research at the cap needs the mixing rule on (r_N, r_S): when an indifferent investor abstains it fails there (the gap (1.748, 2.124] of the lens plans). When an indifferent high-cost challenger may prepare with any probability, floor-entry research also exists at r_Q and at r_C, and the families of the tie remark join the list; these belong to `rem:researchties` (stated in `statements/C.tex`), not to this lemma. Uniqueness on (r_C, r_2] holds under every pair of tie rules by `lem:a5-strong`; the lemma states the default rules once for all parts.
6. Notation follows `plan/NOTATION.md` (Section 9). The floor margin phi_rho sits next to the recruitment margin phi_a.
7. The value r_Q is the referee's r_X (2.166995158219), and lambda_E(r_Q) is the referee's floor research at that strength (0.234257256066).

## 8. Other checks

- Build in a private scratch folder: the shared preamble with the absolute path of the manuscript's numbers table, stand-ins for the cited labels and test values for the four proposed rows; `latexmk -pdf -interaction=nonstopmode -halt-on-error` exit 0, 4 pages, no warnings, no overfull boxes. All four pages read after the notation pass.
- Language scan of the fragment and this report: see Section 9.
- Nothing fails. The repository holds no build product from this work.

## 9. Notation pass

The S4 brief asks for the frozen notation of `plan/NOTATION.md` (part (d), S5, the paragraph on the O1 draft) and for fixes 3, 4 and 5 of `O1_referee.md` Section 3. The mathematics is unchanged: every statement, case split, inequality and printed number is as the referee accepted it. The changes, in `O1_proof.tex`:

1. The floor-entry root Lambda_rho(Delta_T) is lambda_Q(Delta_T) everywhere (definition paragraph, lemma parts (b), the proof, closing paragraph). The domain stays rho Delta_T >= 2k with lambda_Q = 0 at rho Delta_T = 2k, which the proof uses at r_N; on rho Delta_T > 2k it is the freeze's root in (0, 1). Inside the proof, lambda_Q stands for lambda_Q(Delta_T(r)), declared in the proof's first sentence, as Lambda_rho did before.
2. lambda*_rho(Delta_T) is min{lambda_Q(Delta_T), lambda_bar}, written out: in the definition of floor-entry research, lemma part (a) ("tau(r) exceeds the top posterior M_lambda at lambda = min{lambda_Q(Delta_T(r)), lambda_bar}"), Steps 1, 4 and 6, and the closing paragraph. In Steps 4 and 6 the tuple's research is lambda_hat = min{lambda_Q, lambda_bar}, so most comparisons read in lambda_hat.
3. The sale probability s(r) of recruiting research at the cap is sigma_L(-1) = hat-s_-(r)/lambda_bar, with hat-s_-(r) = min{lambda_bar, b_bar [rho Delta_T(r)/k - 2]^+}, the low-class sale rate of `lem:a4-low` at the presence lambda_bar (A4's three cases at the prior 1/2; the two forms agree: hat-s_- = lambda_bar exactly when rho Delta_T m_lambda_bar >= k, because m_lambda_bar = b_bar/(2 b_bar + lambda_bar)). The tuple's definition gives sigma_L(-1) and sigma_L(0) = 1 - hat-s_-(r)/lambda_bar. The posteriors read mu(-1) = b_bar/(2 b_bar + hat-s_-(r)) and mu(0) = b_bar_0/(2 b_bar_0 + lambda_bar - hat-s_-(r)); Step 5 writes f_L = (b_bar + hat-s_-, b_bar_0 + lambda_bar - hat-s_-, b_bar) and splits on hat-s_- = 0, in (0, lambda_bar), = lambda_bar. Step 6 works with the rate s_- = lambda_bar sigma_L(-1), as the freeze defines s_-, and ends with s_- = hat-s_-(r). The fragment cites `lem:a4-low` for the first time.
4. The gap g(lambda, r) of the proof is written out: the proof's first sentence names "the gap" rho Delta_T(r) m_lambda - k - a lambda as a function of lambda, and each value is written in full where it matters (Step 0 "the gap at lambda_bar, rho Delta_T(r) m_lambda_bar - k - a lambda_bar"; Step 3 the bracket [rho Delta_T(r) m_lambda_bar - k - a lambda_bar]; Step 4 "Psi - a lambda_bar = rho Delta_T m_lambda_bar - k - a lambda_bar"; Step 6 "a lambda_hat = rho Delta_T m_lambda_hat - k").
5. "Research at the entry floor" is "floor-entry research" (paragraph title, definition, lemma title "Floor-entry research along the path", parts (b) and (d), Steps 4 and 6, closing paragraph); above r_C it is "floor-entry research at the cap", as the freeze asks. "The recruiting tuple at the cap" is "recruiting research at the cap" (definition, parts (c) and (d), Steps 5 and 6, closing paragraph). "Tuple" stays where it means the tuple itself ("is the tuple with", "the tuple is not an equilibrium"). "Floor research" in the closing paragraph is "the research lambda_Q(Delta_T(r)) of floor-entry research".
6. Step 2, local symbols: the piece ends l and u are r_- and r_+ (u is the informed-to-liquidity ratio, 1 + u = e, in A.5), and the local name b(l, u) of the piece bound is dropped (b is the liquidity mass); the bound is the right side of the first display line, and the proof says "the right side of the first line is at least 1/100 on each piece". T(r_-, r_+), the bound on tau', keeps its letter, which A.5 does not use otherwise.
7. Fix 3 (Step 5, (E2)): "orders with equal posteriors have equal entry rho and share a price", which matches the paragraph on constructed tuples with equal entry as a hypothesis.
8. Fix 4 (Step 2): "and the denominator {beta + (1 - 2 beta)[1 - tau]}^2 of the last term falls as tau rises, so on the piece it is at least its value at r_+".
9. Fix 5: the two comment lines at the head of the fragment are gone; the fragment opens with its paragraph title.

In this report: the same renames throughout (title, Sections 1 to 3, 5 to 7); the program's printed lines in Section 4 keep the program's own labels, since the program is unchanged; Section 6 points to the general lemmas of `statements/C.tex`. Build after the pass: exit 0, 4 pages, no warnings, no overfull boxes, no unknown number once the four proposed rows are defined. The referee checks this pass.
