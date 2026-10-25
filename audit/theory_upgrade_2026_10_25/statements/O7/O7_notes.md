# O7. Pooled orders

Mathematics writer's result: at positive spread and posterior-monotone entry, two orders share a price exactly when they share both their posterior and their entry. Recruiting research gives the sale and zero order equal entry rho, so their coincidence of posteriors is a valid pooled price.

## Scope and argument

Source: `scan/reduction_A3_A5.md`, sections 2 and 4.1; referee report W3, Shared Candidate 1, section 4; the pooled-price arguments in referee report W5. Manuscript locations: `appendix/A2_beliefs_trading.tex:165-170`, and the price-belief argument for recruiting research in A.5. The construction is an unnumbered paragraph beside Lemma A.2; `A.tex` gives it label `par:constructed-tuples`.

Take any interior prior, `0<rho<1`, `0<lambda<1`, `0<beta<1/2`, positive spread, Bayes posteriors and entry in `[rho,1]` nondecreasing across distinct posteriors. The price identity gives, at a common posterior, `P(x)-P(x')=[e(x)-e(x')] w(mu)`. Full liquidity support and positive spread give `w(mu)=w_L+Delta_T mu>0`. Distinct posteriors have strictly ordered prices, since entry is nondecreasing and `w_L>=0`. Thus price equality is exactly equality of the posterior-entry pair. At a pooled price, all orders share the same likelihood ratio, so the ratio of sums in price Bayes' rule gives the common posterior.

When an indifferent high-cost challenger prepares, entry is a function of the posterior. When an indifferent high-cost challenger may prepare with any probability, distinct entry probabilities at tau yield distinct prices revealing that same posterior. These conclusions hold for either investor tie rule.

For recruiting research, when an indifferent investor may mix, take prior one half, `tau>1/2`, positive research below one, a full high-class purchase, and a low-class sale with probability `sigma_L(-1)`. The sale posterior is `b_hat/[2b_hat+lambda_hat sigma_L(-1)]`; the zero-order posterior is `b_0_hat/[2b_0_hat+lambda_hat(1-sigma_L(-1))]`. Both are at most one half, strictly below tau, so both have entry rho under either challenger tie rule. They coincide exactly when `sigma_L(-1)=beta/(1-beta)`, independently of research intensity.

When an indifferent investor may mix, in the example's capped recruiting segment the sale probability rises strictly from zero to one between r_N and r_S. The pooling probability lies in that interval. The ordering `r_lambda_bar < r_N < r_S < r_C` therefore gives exactly one pooling strength within capped recruiting research. The frozen notation writes the probability directly as `sigma_L(-1)` and the rate as `hat s_-(r)`.

## Exact values for the example

Let `beta=294655/1000000`, `k=1/50`, `rho=1/4`. The pooling spread is `(k/rho)[2+(e-1)beta/(1-beta)]`. The function `fr(y)=ell+y+sqrt(y^2+2 ell y)` inverts the example's spread above ell.

| Numerical-table name | Exact value | Six-place display |
|---|---|---|
| `r_pool_B` | `fr((k/rho)[2+(e-1)beta/(1-beta)])` | `1.911775` |
| `pool_mu_B` | `k/[rho Delta_T(r_pool_B)]` | `0.367944` |
| `pool_price_B` | `t_0(r_pool_B)+rho[t_L(r_pool_B)-t_0(r_pool_B)]+k` | `0.497885` |

The sale probability is exactly `58931/141069`. The print-only computation `python3 -I o7_pool.py` prints interval values at 60 decimal digits. At the pooling strength the sale and zero-order posteriors both equal `0.367943952645577`, and both prices equal `0.497885379019505`. The purchase posterior minus tau is `0.070222003041511`; the research return at the cap exceeds its marginal cost by `0.0216683437467043`. The positive-sale and partial-sale margins are `0.0143561046626715` and `0.00538139195188492`. Thus the point has full purchase recruitment, strictly positive research demand at the cap and mixed low-class selling.

## Other constructions and placement

The abstention economy has a common posterior and common entry. Full two-sided orders have distinct posteriors. In A.4, equal nonpurchase posteriors have entry rho; the entry-floor forms have entry rho everywhere, and the threshold pair has only the purchase at tau. In A.5, zero research has common prior entry, floor-entry research has full orders, recruiting research has the equal-entry property above, and threshold research has only the purchase at tau. The signal and many-class constructions use their own price formulas.

The two paragraphs in `O7_proof.tex` supply complete arguments for the A.2 construction and the A.5 application. The numerical rows are used by its example sentence. The plan's equal-entry requirement holds, and each existing construction has the required price beliefs.
