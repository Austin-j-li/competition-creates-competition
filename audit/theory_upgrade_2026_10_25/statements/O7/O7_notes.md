# O7. Orders that share a posterior

Report of the mathematics writer to the coordinator, 25 October 2026. This folder holds the LaTeX fragment `O7_proof.tex` (the paragraph on constructed tuples for Appendix A.2, with its proof, and the paragraph for Appendix A.5 that applies it to the sale and the zero order in recruiting research), the print-only program `o7_pool.py`, and this report. Nothing is committed.

## 1. Result

**The statement A.2 needs** (the paragraph on constructed tuples, in place of A2:165-170). Let Delta_T > 0. Take a profile, its posteriors mu(x) from (E1), and entry e(x) in [rho, 1] that is nondecreasing in the posterior. Set P(x) = t_0 + e(x) w(mu(x)). Then:

1. P(x) > P(x') whenever mu(x) > mu(x'), and two orders have the same price if and only if they have the same posterior **and the same entry**;
2. zeta(P(x)) = [e(x) - rho]/(1 - rho) is a well-defined preparation rule on the image of P, with values in [0, 1], and the belief that (E2) assigns to P(x) is mu(x);
3. with g_H > g_L: when an indifferent high-cost challenger prepares, entry is a function of the posterior, so equal posteriors give equal prices; when an indifferent high-cost challenger may prepare with any probability, two orders at the posterior tau may carry different entry, and then they have different prices, each revealing tau.

The present text (A2:168-169, "a stated tuple has distinct prices at distinct posteriors, and equal prices at equal posteriors") is right under the first challenger rule and needs "and equal entry" under the second. The repaired paragraph states the equivalence with equal entry and ends with the use the verifications make of it.

**The construction of A.5 meets it.** In recruiting research at the prior 1/2 with tau > 1/2 (class H buys after a success, class L sells with probability z and abstains otherwise), the posteriors after a sale and after no order are b_hat/(2 b_hat + lambda_hat z) and b_hat_0/(2 b_hat_0 + lambda_hat (1 - z)). Both are at most 1/2 < tau, so entry after both orders is rho under all four tie rules. When the two posteriors coincide, which happens exactly when z = beta/(1 - beta) (for every research level), the two orders have the same entry and therefore share a price, and the belief at that price is the common posterior. In the example this happens at exactly one strength on the stretch where recruiting research at the cap is an equilibrium: r = 1.911774629371 (display 1.911775), with z = beta/(1 - beta) = 58931/141069 = 0.417746, common posterior 0.367944 and common price 0.497885. These are the referee's values in W3 "Shared Candidate 1", section 4 (r = 1.911774629371, z = 0.417745925753, posterior 0.367943952646, price 0.497885379020).

The plan's claim (PLAN.md Part 5, O7: "When the sale and the zero order share a posterior during mixed selling, the construction must check equal entry") holds: equal entry holds because both posteriors lie strictly below the threshold.

## 2. The argument in words

- The price formula gives P(x) - P(x') = e(x) Delta_T [mu(x) - mu(x')] + [e(x) - e(x')] w(mu(x')) (equation `eq:a2-increment`). With entry nondecreasing in the posterior and w >= w_L >= 0, a higher posterior means a strictly higher price, by at least rho Delta_T times the posterior gap.
- At equal posteriors the price gap is [e(x) - e(x')] w(mu), and w(mu) = w_L + Delta_T mu is positive because every posterior is positive (full liquidity support, Lemma A.1(a)). So equal prices force equal entry, and equal posterior with equal entry gives equal price.
- The preparation rule is then a function of the price. At a price, all orders share one posterior, hence one likelihood ratio, and the Bayes odds at the price (a ratio of sums) equal it, which is (E2).
- Under the first challenger rule entry is pinned by the posterior's side of tau and equals one at tau, so equal posteriors give equal entry automatically. Under the second, entry at tau is free in [rho, 1], and two orders at tau with different entry get different prices; each such price has only orders at tau in its preimage, so each reveals tau.
- In recruiting research the two non-purchase posteriors are at most 1/2 (class H puts no mass on them, class L puts mass z and 1 - z), so both lie below tau > 1/2 and both carry entry rho under every tie rule. They coincide exactly when b_hat (1 - z) = b_hat_0 z; since b_hat/b_hat_0 = beta/(1 - 2 beta) does not depend on research, the condition is z = beta/(1 - beta). In the example the sale probability z = hat-s_-(r)/lambda_bar rises strictly from 0 at r_N to 1 at r_S, so it meets beta/(1 - beta) once.

## 3. Every construction in the paper meets the equal-entry condition

- A3: E_0 has one posterior and one price; E_1 and E_2 have the three distinct posteriors (m, pi, M).
- A4: the quiet market has one posterior; in the informative forms with class L abstaining the sale posterior is the prior and the no-order posterior is below it; in the informative forms in which class L sells with positive probability while class H buys for sure, the sale and no-order posteriors are both at most the prior, below tau, so both carry entry rho and may share a price exactly as in A.5; in the forms where both classes mix at the entry floor, entry is rho after every order, so any coincidence of posteriors is a coincidence of prices with equal entry; in the threshold pair only the purchase has the posterior tau.
- A5: zero research has one posterior; floor-entry research has three distinct posteriors; recruiting research is section 1 above; the tuples of the tie remark (`rem:researchties`) have only the purchase at tau.
- A6: the cost-law, signal and many-class constructions prove distinct prices with their own price formulas (entry nondecreasing in the posterior in each case) and do not cite the paragraph for equal posteriors.

So the repair changes no tuple of the paper and no conclusion; it makes the cited paragraph true under the second challenger rule, which `lem:prices` already allows at mu = tau (A2:122-123).

## 4. What it changes in the plan

Nothing in substance. S5 item 1 ("Repair the paragraph that says equal posteriors give equal prices: under the tie rule CM, equal entry is also needed") is met by the first paragraph of the fragment. The A.5 paragraph belongs in the verification of recruiting research (O1's Step 5 already says "orders with equal posteriors have equal entry rho and share a price"; area C's general statement of recruiting research can cite the paragraph the same way).

## 5. Proposed rows of the numbers table

| name | exact value | display | computed as |
|---|---|---|---|
| `r_pool_B` | 1 + D + sqrt(D^2 + 2D), D = (k/rho)[2 + (e - 1) beta/(1 - beta)] | 1.911775 | the strength at which hat-s_-(r)/lambda_bar = beta/(1 - beta); interval in e |
| `pool_mu_B` | k/[rho Delta_T(r_pool)] | 0.367944 | the common posterior after a sale and after no order (also b_bar/(2 b_bar + lambda_bar z) at z = beta/(1 - beta)) |
| `pool_price_B` | t_0 + rho [t_L - t_0 + k/rho] at r_pool | 0.497885 | the common price; Delta_T mu = k/rho there |

Only the A.5 paragraph prints these; if S8 leaves the example sentence out, the rows are not needed. The relation rho Delta_T/k = 2 + (e - 1) beta/(1 - beta) uses lambda_bar/(1 - lambda_bar) = u beta at the example's cap.

## 6. Printed lines

Command, from a private scratch folder: `python3 -I audit/theory_upgrade_2026_10_25/statements/O7/o7_pool.py` (absolute path). Exit status 0, 47 lines, under a second. Main lines:

```
  lambda_bar      [0.336121768915121, 0.336121768915121]  width 2.72e-61
  M at the cap    [0.731058578630005, 0.731058578630005]  width 1.24e-60
  beta/(1 - beta) = 58931/141069 = 0.41774592575264585
  Delta_T there   [0.217424418650686, 0.217424418650686]  width 9.72e-62
  r               [1.91177462937072, 1.91177462937072]  width 6.22e-61
  tau(r)          [0.660836575588494, 0.660836575588494]
  M at the cap minus tau(r) [0.070222003041511, ...]
  rho Delta_T - 2k (positive: class L sells with positive probability) [0.0143561046626715, ...]
  k - rho Delta_T m_cap (positive: class L also abstains with positive probability) [0.00538139195188492, ...]
  z = s/lambda_bar [0.417745925752646, 0.417745925752646]
  z - beta/(1 - beta) [-1.86690458335834e-60, 2.02247996530487e-60]
  posterior after a sale      [0.367943952645577, 0.367943952645577]
  posterior after no order    [0.367943952645577, 0.367943952645577]
  their difference            [-1.40017843751876e-60, 1.40017843751876e-60]
  price after a sale          [0.497885379019505, 0.497885379019505]
  price after no order        [0.497885379019505, 0.497885379019505]
  price after a purchase      [0.962797158484232, 0.962797158484232]
  research gap at the cap, Delta_T m_cap - k - 2 a lambda_bar (positive: research sits at the cap) [0.0216683437467043, ...]
  r = 1.8: z 0.129328; posteriors 0.45, 0.325376, 0.731059; prices 0.48875, 0.483211, 0.921633
  r = 2.0: z 0.654724; posteriors 0.32, 0.412259, 0.731059; prices 0.504375, 0.510141, 0.995265
  r_C (tau = M at the cap) [3.59265851879466, 3.59265851879466]
  strength at which research reaches the cap [1.67763283438508, 1.67763283438508]
```

The pooled strength lies between the strength at which research reaches the cap (1.677633, the existing row `res_rcap`) and the entry ceiling (3.592659, `rC_B`), and between r_N = 1.747878 and r_S = 2.124148, where class L mixes. At 1.8 and 2.0 the sale and no-order posteriors differ in opposite directions, as the monotone sale probability implies.

## 7. Build and scan

- `O7_proof.tex` built in a private scratch folder inside a wrapper that loads `../tex/preamble` and stand-ins for the cited labels: exit 0, one page; the three proposed rows print as unknown names, which is expected.
- Language scan: results in the coordinator's summary for this area.
