# O1. Referee report on the lemma "Research at the entry floor along the path"

Report of the referee to the coordinator, 25 October 2026. Under review: the LaTeX fragment (definitions, the lemma with parts (a) to (d), its proof and the closing paragraph), the print-only program that computes the bounds the proof cites, and the mathematics writer's notes, all in this folder. The referee did not write any of them.

## 1. Verdict

**Accept with listed fixes.** The lemma is true as stated, the proof is complete, every bound it cites is exact, and the program computes what the proof says. The fixes are to notation and wording (Section 3); none touches the mathematics.

The lemma gives the research figure what it needs: floor-entry research is an equilibrium exactly on (r_N, r_Q) and above r_C, with entry rho; recruiting research at the cap is an equilibrium exactly on [r_lambda_bar, r_C], with entry 0.522757; and tau(r) crosses the top posterior at floor research once on (r_N, r_C), at r_Q = 2.166995, with the second equality at r_C itself. On [r_Q, r_C] the recruiting tuple is the unique equilibrium under the default tie rules.

## 2. What was checked

### 2.1 Definitions, re-derived from the model

From Sections 2 and 5, Appendices A.2 and A.5 and the referee report W3:

- Delta_T(r) = (r - 1)^2/(2r); g_L = 3/(8r), g_H = 10 - r/2 - 1/(8r); tau(r) = (c_H - g_L)/(g_H - g_L) = (12r - 3/4)/(20r - r^2 - 1). The quotient rule from the closed forms gives tau'(r) = 3(8r^2 - r + 2)/[2(20r - r^2 - 1)^2]; the two forms agree exactly at six rational strengths.
- m_lambda = beta(1 - lambda)/[2 beta + (1 - 2 beta) lambda], M_lambda = 1 - m_lambda; lambda_E(tau) = beta(2 tau - 1)/[beta + (1 - 2 beta)(1 - tau)], d lambda_E/d tau = beta/[beta + (1 - 2 beta)(1 - tau)]^2 (the numerator 2 beta D + beta(2 tau - 1)(1 - 2 beta) reduces to beta). M at lambda_E(tau) equals tau.
- The floor root: a lambda = rho Delta m_lambda - k has one root in [0, 1) when rho Delta >= 2k, since the gap falls strictly in lambda from rho Delta/2 - k to -k - a; the root rises in Delta. Clearing the denominator gives the quadratic the program uses, a(1 - 2 beta) lambda^2 + [rho Delta beta + k(1 - 2 beta) + 2a beta] lambda + beta(2k - rho Delta) = 0, whose constant term is negative when rho Delta > 2k, so -2C/(B + sqrt(B^2 - 4AC)) is its positive root.
- The recruiting tuple's sale probability: U_L(-1) = rho Delta b_bar/(2 b_bar + lambda_bar s) - k vanishes at s = b_bar(rho Delta - 2k)/(k lambda_bar), and this equals one exactly when rho Delta m_lambda_bar = k, because m_lambda_bar = b_bar/(2 b_bar + lambda_bar). The three regimes (abstain, mix, sell) are those of W3 equation (2).
- The floor margin equals the gap at lambda_E(r), because m at lambda_E equals 1 - tau; and the identity phi_rho = g(lambda_bar, r) + rho Delta (M_cap - tau) + a(lambda_bar - lambda_E) holds term by term (residual below 10^-52 at three strengths).

### 2.2 Each step of the proof

- Step 0. Every fact is either a closed form (Delta and tau rise; B_r(1/2) = 5 - r/4 + 1/(8r) < 6, so tau > 1/2; tau(r_2) = 4245/5804) or an existing margin of the numbers table (condition (U) at r_1; M_cap - tau(r_1); tau(r_2) - M_cap; r_N - r_lambda_bar). The equivalence "lambda_E(r) <= lambda_bar exactly when r <= r_C" uses only that M rises in lambda and tau rises in r. "g(lambda_bar, r) >= 0 exactly when r >= r_U" uses m at the cap equal to 1/(1 + e), so (U) is Delta(r) >= (k + a lambda_bar)(1 + e)/rho.
- Step 1. For r in (r_N, r_C], lambda_E <= lambda_bar, so min{Lambda, lambda_bar} < lambda_E is the same as Lambda < lambda_E, which is g(lambda_E, r) < 0, which is phi_rho(r) < 0. The equality case splits correctly into phi_rho = 0 and lambda_bar = lambda_E <= Lambda; the second is r = r_C, where Lambda > lambda_bar because r_C > r_U. Correct.
- Step 2. The derivative formula is right (checked against a high-precision difference quotient at five strengths, agreement to 15 places). On a piece [l, u]: Delta' rises (its derivative is 1/r^3), 1 - tau falls, Delta rises, tau' <= T(l, u) because 8r^2 - r + 2 rises (derivative 16r - 1 > 0) and 20r - r^2 - 1 is positive and rises below r = 10, and the denominator {beta + (1 - 2 beta)(1 - tau)}^2 falls in tau. So phi_rho' >= b(l, u). The proof says "Delta', Delta and tau rise" and leaves the last denominator step to the reader; see fix 4.
- Step 3. phi_rho(r_N) = k(1 - 2 tau) - a lambda_E < 0 is immediate from tau > 1/2. On [r_U, r_C] the three terms of the identity are nonnegative, the first vanishing only at r_U and the other two only at r_C, so phi_rho > 0 there. With Step 2 the zero is unique and lies in (r_N, r_U). Correct.
- Step 4. (E1) to (E7) for the floor tuple are each right. The decisive inequality is g(lambda_hat, r) >= 0 for lambda_hat <= Lambda, which makes both trades earn at least a lambda_hat > 0. (E7) is right in both branches (root below the cap, root at or above the cap). The converse uses the default challenger rule at the tie, as it should.
- Step 5. (E1) to (E7) for the recruiting tuple are each right on [r_lambda_bar, r_C]. (E2) handles the pooled case correctly: when the sale and the zero order share a posterior (this happens once, at r = 1.911775, with common posterior 0.367944), both have entry rho and so one price, and the challenger's belief at that price is the common posterior. The purchase earns at least 2a lambda_bar from r_lambda_bar on. Class L's three regimes each satisfy (E5) under the mixing rule. The failures outside the interval ((E3) above r_C, (E7) below r_lambda_bar) are right.
- Step 6. Zero research is excluded because a full order at the prior pays above r_N and the joint-deviation lemma then forces positive research. With positive research the existing lemmas give a strict full purchase and entry rho after the other orders. The two cases on the purchase posterior are exhaustive; in the first, class L's sale is strictly best (its posterior is at least m at the research level), so the tuple is the floor tuple and research solves the floor equation or sits at the cap; in the second, research below the cap contradicts (E7) because the recruiting gap Delta m_lambda - k - 2a lambda is positive below the cap from r_lambda_bar on, and the sale probability is pinned down by the sign pattern of U_L(-1) in s. Correct. Above r_C the strong-incumbent lemma applies because r_C > r_U and M_cap < tau.

### 2.3 The bounds

- The 24 pieces [6/5 + i/10, 6/5 + (i + 1)/10], i = 0, ..., 23, tile [6/5, 18/5] with no gap and no overlap; the last right end is 18/5.
- Every quantity in b(l, u) is a rational number (beta, the primitives, tau and Delta at rational strengths), so b is exact. The referee recomputed all 24 values from an independent implementation of tau and its derivative written from g_H and g_L: the smallest is 5993292043494701003/510152171246294601024 = 0.011748..., on [6/5, 13/10], identical to the program's value; all 24 exceed 1/100.
- A second, different monotonicity argument confirms the sign: interval arithmetic applied directly to the derivative formula on 240 pieces of width 1/100 gives a positive lower bound on every piece (smallest 0.012298), and on 2400 pieces of width 1/1000 as well (smallest 0.012364). The minimum of phi_rho' on the path is at r_0, about 0.012371.
- The signs of phi_rho at the 25 piece ends are negative at 6/5, ..., 21/10 and positive at 11/5, ..., 18/5, so the zero lies in (21/10, 11/5).
- The quantities that involve Euler's number (the cap, M and m at the cap, r_lambda_bar, r_S, r_U, r_C, the floor root) are handled in the program by rational intervals rounded outward on a grid of 10^-60, with e bracketed by a partial sum and the tail bound 2/41!. Square roots use integer square roots with an outward step. The sign of phi_rho at a bracketed strength is read from the values at both bracket ends, which is valid because phi_rho rises.

### 2.4 The program

Executed with `python3 -I` from a private folder: exit status 0, 344 lines, under a second. It prints and asserts nothing. Its output matches the notes line for line. The referee read the whole program: the interval class rounds outward on every operation, the inverse is applied only to positive intervals, the sign function returns zero for an undecided interval and the bracketing routine then stops and reports it (no bracket was undecided), the piece loop covers exactly the 24 pieces, and the tuple reports in its Section 10 compute prices from the auction's terminal values and payoffs from the prices, as the definition of equilibrium does, rather than from the lemma's formulas. Its Section 11 compares 32 displays of the numbers table with its own values; all agree.

One remark, not a fault: the bracketing routine does not print the signs at its initial ends for r_N, r_lambda_bar, r_S, r_U and r_C (it does for r_Q). The brackets agree with the closed forms to 22 places, so the initial signs were right.

### 2.5 Independent recomputation

Done by the referee in a private folder, by methods that differ from the program's:

| Quantity | Referee's value | Program | Method |
|---|---|---|---|
| r_Q | 2.16699515821928588228248724493 | [2.166995158219285882282487, 2.166995158219285882282488] | (i) bisection of tau(r) - M at the floor root, with the floor root from secant iteration at 50 digits; (ii) exact rational bisection of phi_rho written from g_H and g_L; the two agree to 10^-34 |
| lambda_E(r_Q) = floor root at r_Q | 0.23425725606563384864 | [0.234257256065633848, 0.234257256065633849] | both quantities at the referee's r_Q; equal to 20 places |
| tau(r_Q) | 0.67086171285609046754 | [0.670861712856090467, 0.670861712856090468] | |
| r_lambda_bar, r_N, r_S, r_U, r_C | 1.677632834385080818823429, 1.747877538267962743567348, 2.124148132815450673539019, 2.434045526712001135254259, 3.592658518794661833335916 | the same to 22 places | closed forms with e at 50 digits; r_C by root finding |
| phi_rho(r_N), phi_rho(r_U), phi_rho(r_C) | -0.0113912067792, 0.00734637463573, 0.0344957626983 | the same to 12 places | |
| smallest piece bound | 5993292043494701003/510152171246294601024 | identical | exact rationals |
| order r_0 < r_lambda_bar < r_N < r_S < r_Q < r_U < r_1 < r_C < r_2 | holds | holds | |
| entry at the cap | 0.5227569435 | 0.522757 | closed form and the tuple's order law |

Displays: r_Q rounds to 2.166995 and lambda_E(r_Q) to 0.234257 at six places, as the notes propose.

### 2.6 Boundary cases and tie rules

- The open end at r_N. The floor root is 0 at r_N (rho Delta = 2k), so the floor tuple is not defined there, and the lemma's part (b) is stated on the open interval. The recruiting tuple at r_N has s = 0 and U_L(-1) = 0: class L is indifferent and abstains, which the mixing rule allows, so part (c)'s closed left end at r_lambda_bar and its passage through r_N are right. The notes record that zero research at r_N is also an equilibrium (an order at the prior just pays), consistent with the existing text.
- Where the floor root reaches the cap: at r_U, before r_C and after r_Q. The referee's floor root at r_U differs from the cap by less than 10^-14 in the program's brackets, and condition (U) at r_U has margin zero to 12 places, as the proof says.
- r_Q. At the referee's r_Q the floor tuple has purchase posterior equal to tau to 44 places, so B at the purchase price equals c_H; under the default challenger rule the challenger prepares, (E3) fails for the tuple with no preparation, and the floor tuple is excluded at r_Q. At r = 2.2 the gap B - c_H at the purchase price is 0.0649 > 0, so the tuple fails there too, as part (b) says.
- r_C. With research at the cap the purchase posterior equals tau(r_C): the floor tuple fails and the recruiting tuple holds with the indifferent challenger preparing; its sale probability is 1 (r_C > r_S) and class L's sale earns 0.0429 > 0. At r_2 = 3.6 the floor tuple holds (B - c_H = -0.0027 at the purchase price) and the recruiting tuple fails.
- Tie rules. The lemma states the default pair once, in its hypothesis, as the rules require. The floor tuple's trade choices are strict, so it needs no investor rule; the recruiting tuple needs the mixing rule on (r_N, r_S), where class L mixes with zero sale profit; both exclusions at r_Q and r_C use the challenger rule. This matches W3's classification (its equations (2), (13), (14)) and its outcome list for the example.

### 2.7 The language rules on the LaTeX

The coordinator's language scan on the fragment: 0 hits, 2 allowed tie-rule phrases. Read in full: no status label (the method is named as mathematics, "an exact rational computation gives"), no hedge, no narration of the paper's changes, no process word, none of the retired names of the example; the example is called "the example" and named by its primitives; every number prints through `\reg`, fractions included (the step 1/10 and the bound 1/100 through the two proposed rows). The preparation cost is untouched. The fragment builds with the manuscript's preamble and stand-ins for the cited labels: exit 0, four pages, no undefined reference, no overfull box, and every number prints once the four proposed rows are defined.

## 3. Issues

Severity: "fix before transplant" (the coordinator or the mathematics writer changes the fragment before S8 moves it into A.5), "low" (a wording improvement), "remark" (no change required).

1. **Fix before transplant. Notation differs from the S3 freeze.** `plan/NOTATION.md` part (c) fixes the floor root as lambda_Q(Delta), with research min{lambda_Q, lambda_bar} written out, and lists "lens choice Lambda_rho" as the collision it avoids (Lambda_r is the research polynomial of A.5). Its part (b) names the outcome "floor-entry research" (letter Q), the capped recruiting outcome "recruiting research at the cap" (R-bar retired), and the strengths "the floor-entry branch". The fragment uses Lambda_rho, lambda*_rho, "research at the entry floor" and "the recruiting tuple at the cap" throughout, including the lemma's title, the two definition paragraphs, parts (b) to (d) and the closing paragraph. Fix: Lambda_rho(Delta_T) to lambda_Q(Delta_T); lambda*_rho to min{lambda_Q, lambda_bar} written out (or one short symbol entered in the freeze); "research at the entry floor" to "floor-entry research"; "the recruiting tuple at the cap" to "recruiting research at the cap" (the fragment keeps "tuple" where it means the tuple itself, as in "(E1): ... give the stated posteriors"). The mathematics is unchanged. The notes already flag the Lambda collision (their item 6) and defer to the freeze.
2. **Fix before transplant. Two symbols of the fragment need rows in the freeze.** The floor margin phi_rho and the sale probability s(r) are not in `NOTATION.md`. phi_rho sits well beside the recruitment margin phi_a. The letter s is also the first letter of the rates s_+ and s_- of A.4, which are presence times probability, while s(r) here is a probability; one distinct symbol (or the frozen hat-s form with its own subscript) avoids a reader taking s for a rate. The coordinator enters the chosen symbols in the freeze with today's date.
3. **Low. The pooled-price sentence should name equal entry.** Step 5 (E2) says "orders with equal posteriors share a price". It is right here because both posteriors are at most 1/2 and so both have entry rho, and the S5 repair of the A.2 paragraph on constructed tuples will state equal entry as a second hypothesis. Write "orders with equal posteriors have equal entry rho and share a price", so the sentence matches the repaired paragraph.
4. **Low. One monotonicity step is left implicit.** Step 2 says "Delta', Delta and tau rise" and concludes phi_rho' >= b(l, u); the bound on the last term also uses that {beta + (1 - 2 beta)(1 - tau)}^2 falls as tau rises. Add "and the denominator of the last term falls" or the equivalent.
5. **Low. Placement comments.** The two comment lines at the head of the fragment ("Placement: ...") are development notes; they leave with the transplant.
6. **Remark. The notes.** The coordinator's language scan on the notes gives 11 process hits ("program", "scan", "checked", stage codes). The notes are a report to the coordinator and use the stage codes of the plan, so the referee sees nothing to change; the coordinator decides whether Section 8 of the notes stays in the repository.
7. **Remark. Proposed rows.** `res_rQ` (2.166995), `res_lambda_floor_rQ` (0.234257), `res_floor_step` (1/10) and `res_floor_dphi_lb` (1/100) are correct and are what the fragment prints. The delivery plan also proposes a margin row for the smallest piece bound (0.011748); the fragment as written states the clean bound 1/100 and prints nothing else, so that row serves A.9 only if the coordinator wants the margin there.
8. **Remark. The two-sided statement of part (b).** "Research at the entry floor is an equilibrium exactly on (r_N, r_Q) and on (r_C, r_2]" is read within the tuple's domain rho Delta_T(r) > 2k, which the definition paragraph states. No change needed; if the prose writer wants the domain in the lemma, "for r > r_N" after "exactly" does it.

## 4. For the coordinator

- The proof discharges obligation O1: one crossing on (r_N, r_C), at r_Q, plus the equality at r_C, with the floor root reaching the cap at r_U in between.
- Step 6 of the proof and the sale probability restate on the path what the planned general lemmas of S5 (the three-outcome classification and the sale rule) will give; the fragment stands on its own with the lemmas that exist today, and Step 6 can later cite the general lemmas, as the notes say.
- The figure (S7) can take from this lemma: the floor-entry curve from 0 at r_N to 0.234257 at r_Q, both ends excluded, and at the cap above r_C; the recruiting curve at the cap from r_lambda_bar to r_C, both ends included; entry rho on the floor-entry branch and 0.522757 on the capped recruiting segment.
- Nothing in this folder was changed by the referee except the addition of this report. The referee's computation and test build live in a private folder outside the repository.
