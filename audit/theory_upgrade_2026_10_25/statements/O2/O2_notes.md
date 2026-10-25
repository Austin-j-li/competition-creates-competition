# O2. Where the bound beta <= 1/3 enters

Report of the mathematics writer to the coordinator, 25 October 2026. This folder holds the LaTeX fragment `O2_proof.tex` (the footnote of Section 2.3, the paragraph "Where beta <= 1/3 enters" for Appendix A.2, and a paragraph that shows the exclusion bound fails for every beta in (1/3, 1/2)), the print-only program `o2_exclusion.py` for one instance of that failure, and this report. Nothing is committed. Result numbers are those after the update (decision 7: Proposition A.1 becomes the full Corollary 1, the later appendix propositions move up by one; Lemmas A.4 to A.6 are those of `A.tex`; the A4 and A5 lemma numbers follow `plan/lens_theory.md` part 4).

## 1. Result

The model's bound beta <= 1/3 is the inequality b_0 >= b, and the paper uses it only through the posterior bound at the zero order, Lemma A.1(c). That bound enters exactly three places:

1. Corollary A.1, the exclusion bound (Section 3.2 states it in words). For every beta in (1/3, 1/2) it fails: section 3 below gives, for every lambda, rho in (0, 1) and every auction with Delta_T > 0 and g_H > g_L, a prior, a high cost with B(M(pi)) < c_H and a trading cost at which an equilibrium has high-cost preparation after the zero order, under all four tie rules.
2. Lemma A.13(a) (`lem:a5-bounds`) at the zero order. Its users need the nonzero orders only (Lemma A.14 uses mu(1) <= M at research lambda_hat; Lemma A.17 uses the bounds on U_H(1) and U_L(-1)); the one step that uses the zero order is the necessity step of the research parameter region (A5:358, "every posterior at r_1 is at most M_lambda_bar"), which sits inside a result that ranges over beta <= 1/3 anyway.
3. Step 1 of the proof of Proposition A.3 (preparation cost laws, `prop:atomless`), at a price that pools the zero order (A6:103-104): the low component prepares at every price because every price belief is at least m.

Two results describe sets of slots and range over the slots of the model, beta <= 1/3:

4. Proposition A.1 (the research parameter region, `prop:researchregion`): its last sentence, "these patterns hold for every beta in (res_beta_lo, 1/3]".
5. Proposition A.11 (identification of the informed share, `prop:informedshare`), parts (a) and (c): "a slot of the model exactly when beta' <= 1/3, that is 3v <= 2 + u'(1 - v)".

Every other result of the paper holds for every beta < 1/2. Section 2 lists them with the reason for each.

## 2. Result by result

Main text.

| result | beta < 1/2? | reason |
|---|---|---|
| Proposition 1 | yes | no slot enters |
| the posterior interval "after every order" and the exclusion bound, Section 3.2 (03:89-97) | uses beta <= 1/3 | the zero order; item 1 above |
| the trading bound, Section 3.3 | yes | nonzero orders only (Lemma A.3(c), A2:219-220) |
| the two numbers, Section 3.4 (target T-3.6) | yes | Lemmas A.4 and A.5 |
| Proposition 2 | yes | Steps 1, 2 and 5 force orders with eq. (A.6), which uses the nonzero orders; Steps 3 and 5 compute the posteriors (m, pi, M) from full orders (Lemma A.1(d)); the exclusion at F_2 uses B_2(mu) <= B_2(M) at those posteriors only (A3:51, A3:90-92, A3:122) |
| Proposition 2(ii), the takeover share | yes | Step 4 (O6) |
| Corollary 1 | yes | the band in u and the prior window do not involve beta; the band is an open interval of lambda at each beta |
| Table 2, row "Liquidity probability beta", region (0, 1/3] and margin 1/3 - beta | domain | the row records the model's domain; at beta < 1/2 it would read (0, 1/2) |
| Proposition 3 | yes | A4 is already stated for 0 < beta < 1/2 (A4:7, A4:460); its lemmas use Lemma A.3 at posteriors computed from the purchase and sale rates |
| Corollary 2, Corollary A.2 | yes | as Proposition 3 |
| Proposition 4 | yes | W3 "Shared Candidate 1" is stated at 0 < beta < 1/2; positive research forces a strict full purchase with the nonzero-order bounds only (W3 section 1, Lemma A.14); the low class's sale rate and the research equation (Lemmas A.15, A.16) compute posteriors from the stated orders; zero research has every posterior 1/2; Lemma A.17 uses the nonzero orders |
| Corollary 3 | yes | at the example's slot, beta = 0.294655 |
| research parameter region (05:154-160) | ranges over beta <= 1/3 | item 4 |
| preparation cost laws, Section 6.1 | uses beta <= 1/3 | item 3 |
| value classes, many classes, signals (Sections 6.2, 6.3) | yes | below |
| welfare and sale terms, Section 7 | yes | below |
| empirical implications, Section 8 | yes, except the identification of the informed share | item 5 |

Appendix.

| result (number after the update; now) | beta < 1/2? | reason |
|---|---|---|
| Definition A.1; Proposition 1(c) (named) | yes | no bound |
| Lemma A.1 (a), (b), (d) | yes | A2:57-79, A2:91 |
| Lemma A.1 (c) | uses beta <= 1/3 | its proof shows the bound fails for beta > 1/3 under the profile sigma_H = delta_0, sigma_L(0) = 0 (A2:73-75) |
| Corollary A.1 | uses beta <= 1/3, and fails above it | item 1 |
| Lemma A.2, Lemma A.3 | yes | Lemma A.1(a) and the conditions listed; Lemma A.3(c) uses Lemma A.1(b) |
| paragraph on constructed tuples; Lemma A.4 (reduction); Lemma A.5 (two numbers) | yes | Lemma A.1(a); Lemma A.5 has no slot |
| Lemma A.6 (decisive advantage) | yes | needs only posteriors below one (Lemma A.1(a)) |
| Corollary 1, full statement (Proposition A.1) | yes | as Corollary 1 |
| Lemmas A.7 to A.11; Proposition 3, full statement; Corollary 2, full statement; Corollary A.2 | yes | A4 is stated at 0 < beta < 1/2 |
| Lemma A.12 (joint deviations) | yes | no posterior bound |
| Lemma A.13 (b) to (d); (a) at the nonzero orders | yes | item 2 |
| Lemma A.13 (a) at the zero order | uses beta <= 1/3 | item 2 |
| Lemmas A.14 to A.17; Proposition 4, full statement; Remark A.1 | yes | as Proposition 4 |
| Corollary 3, full statement | yes | the example's slot |
| Proposition A.1 (A.2), research parameter region | ranges over beta <= 1/3 | item 4; with the domain beta < 1/2 its conditions would extend to beta < res_beta_hi = 0.4897: a_up(beta) > a there (A5:381); the monotonicity bound a_mono(beta) = (lead bound) {beta + (1 - 2 beta)[1 - tau(7/4)]}^2/(2 beta tau'_max) falls from 0.150885 at 1/3 to about 0.125 as beta tends to 1/2, far above a = 1/40; and (U) at r_1 holds at beta = 1/2 (rho Delta_T(r_1)/(1 + e) - k - a lambda_B(1/2) = 0.0133 > 0). Its necessity step at lambda_bar <= lambda_E(r_1) would then need an argument without the zero-order bound. The proposition stays as stated |
| Proposition A.2 (A.3), fixed information | yes | Lemma A.1(d) (A6:40) |
| Proposition A.3 (A.4), preparation cost laws | uses beta <= 1/3 | item 3 |
| Proposition A.4 (A.5), value classes | yes | Proposition 2 |
| Proposition A.5 (A.6), many classes | yes | the sentence at A6:306-308 bounds the posterior vector after every order with beta <= 1/3; the proof uses the vectors after a purchase and a sale only (the strong economy's order bounds), and the weak economy uses no posterior bound. S8 can restrict that sentence to the nonzero orders |
| Proposition A.6 (A.7), complementary signals | yes | the sentence at A6:402-404 bounds nu after every order through Lemma A.1(b)-(c); the order payoffs use nu(1) and nu(-1) only (A6:428-431). S8 can restrict that sentence to the nonzero orders; `A.tex` states the extended proposition with "any slot" |
| Propositions A.7 to A.9 (A.8 to A.10), welfare | yes | forced full orders and the posteriors (m, pi, M) |
| Proposition A.10 (A.11), price gap; A.12 (A.13), winner; A.13 (A.14), announcement | yes | computed at stated equilibria with posteriors from the stated orders |
| Proposition A.11 (A.12), informed share, (a) and (c) | range over beta <= 1/3 | item 5 |
| Proposition A.11 (A.12), (b) and (d) | yes | posteriors of full orders |
| Corollary A.3, counts under purchases only | yes | its proof keeps a perturbed slot inside the domain (A8:162: "it stays at most 1/3"), which works for either domain |
| A.9 tables, row "Domain beta <= 1/3" (A9:111) | domain | |

## 3. The exclusion bound fails for every beta in (1/3, 1/2)

Construction (second paragraph of the fragment). Let class H abstain and class L sell. On the orders (-1, 0, 1), f_H = (b, b_0 + lambda, b) and f_L = (b + lambda, b_0, b). The posteriors are m(pi) after a sale, pi after a purchase, and above M(pi) after no order, because b_0 < b makes the likelihood ratio at the zero order, 1 + lambda/b_0, exceed 1 + u. Choose pi close enough to one that 1 - pi < m(pi) (m(pi) tends to one), a high cost with threshold tau strictly between M(pi) and the zero-order posterior, and k strictly between rho Delta_T (1 - pi) and rho Delta_T m(pi). Entry is (rho, 1, rho) after (-1, 0, 1), nondecreasing in the posterior, so the paragraph on constructed tuples gives distinct prices that reveal the posteriors. The purchase earns rho Delta_T (1 - pi) - k < 0 and the sale rho Delta_T m(pi) - k > 0; wrong-signed orders earn at most -k. Every comparison is strict, so this is an equilibrium under all four tie rules, with B(M(pi)) < c_H and high-cost preparation after the zero order.

Instance (the program): h = 10, ell = 1, p = 1/2, incumbent U[0, 3], rho = 1/4, c_H = 33/4, k = 1/20, pi = 9/10, lambda = 1/2, beta = 2/5. Then b = 1/5, b_0 = 1/10, u = 5/2, M = 63/65, m = 18/25, tau = 39/40, and the zero-order posterior is 54/55 > tau > M.

## 4. Where the sources differ, and what it changes

- The prose writer's target T-2.3 keeps the present footnote ("Propositions 2 and 3 hold for every beta < 1/2") and leaves Proposition 4 to the referee (`wording_targets.md`, point 3). The result above answers both questions: the general Proposition 3 holds for every beta < 1/2, and Proposition 4 joins it. The fragment's footnote states the scope positively, by listing the four places where the bound enters or the domain matters, and says that every other result holds for every beta < 1/2.
- `plan/lens_theory.md` line 330 lists "Corollary A.1, Lemma A.13(a) and condition U" as the places where the zero-order bound enters. Condition U (Lemma A.17) does not use it: the uniqueness step bounds U_H(1) and U_L(-1) only, and the zero-order posterior is computed from full orders after that. The list gains Proposition A.3 (preparation cost laws), which the lens plan does not name.
- `plan/lens_maintext.md` line 68 (iii) says that "the zero-research tuple uses beta <= 1/3". At zero research every order law is the liquidity law, so every posterior is 1/2 for every beta < 1/2; the tuple does not use the bound.
- `plan/lens_maintext.md` line 415 ("Propositions 2 to 4 hold for every beta < 1/2", conditional on the check) is confirmed.
- Effect on the plan: the footnote at 02:123-125 and the paragraph at A2:232-236 take the fragment's text; A3:122 ("The bound at the zero order, Lemma A.1(c), is the only use of beta <= 1/3, and it enters no step") stays true and can go, since the A2 paragraph covers it; the sentences at A6:306-308 and A6:402-404 can be restricted to the nonzero orders in S8; the general statements of Propositions 3 and 4 (areas B and C) need no bound on beta beyond the model's slot. The claim for Propositions 3 and 4 rests on their S5 proofs citing Lemma A.1 only in parts (a), (b) and (d) and Lemma A.13(a) only at the nonzero orders; the referee can check this on the S5 packages.
- The A2 paragraph names "parts (a) and (c) of Proposition A.11"; if area E reorganizes the parts of the identification result, the reference follows the part that defines "a slot of the model".

## 5. Printed lines

Command, from a private scratch folder: `python3 -I audit/theory_upgrade_2026_10_25/statements/O2/o2_exclusion.py` (absolute path). Exit status 0, under a second. Output:

```
Slot: b = 1/5, b_0 = 1/10, u = lambda/b = 5/2; b_0 < b because beta > 1/3
Auction at r = 3: t_0 = 5/12, t_H = 37/24, t_L = 7/8, g_H = 203/24, g_L = 1/8
  Delta_T = 2/3 = 0.666667, g_H - g_L = 25/3 = 8.333333
  tau = 39/40 = 0.975000
Posterior bounds at the prior: m = 18/25 = 0.720000, M = 63/65 = 0.969231
  B(M) = 853/104 = 8.201923; c_H - B(M) = 5/104 = 0.048077
Orders: class H abstains, class L sells
  order -1: f_H = 1/5, f_L = 7/10, posterior = 18/25 = 0.720000, B = 6.125000, entry = 1/4, price = 521/800 = 0.651250
  order +0: f_H = 3/5, f_L = 1/10, posterior = 54/55 = 0.981818, B = 8.306818, entry = 1, price = 673/440 = 1.529545
  order +1: f_H = 1/5, f_L = 1/5, posterior = 9/10 = 0.900000, B = 7.625000, entry = 1/4, price = 109/160 = 0.681250
  posterior after no order minus M: 9/715 = 0.012587
  posterior after no order minus tau: 3/440 = 0.006818
  tau minus M: 3/520 = 0.005769
Order payoffs against the tuple (abstention pays 0)
  class H, order +1: -1/30 = -0.033333
  class H, order -1: -29/300 = -0.096667
  class L, order -1: 7/100 = 0.070000
  class L, order +1: -1/5 = -0.200000
Trading-cost window for these orders: rho Delta_T (1 - pi) = 1/60 < k = 1/20 < rho Delta_T m = 3/25
Prices ordered as posteriors: P(-1) < P(1) < P(0): True
```

The fragment prints no number, so it needs no row of the numbers table; the instance stays in this report.

## 6. Build and scan

- `O2_proof.tex` built in a private scratch folder inside a wrapper that loads `../tex/preamble` and stand-ins for the cited labels: exit 0, one page, no warning other than hyperref's empty link targets of the stand-ins.
- Language scan: results in the coordinator's summary for this area.
