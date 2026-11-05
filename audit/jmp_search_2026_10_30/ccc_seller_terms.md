# CCC with the seller's terms and one test: project plan

30 October 2026. A planning note, not manuscript text. "To prove" and "to check" mark open items.

## 0. Summary

The paper assumes that the seller commits to a reserve. Its own example shows that a seller who uses that commitment well posts a price near the high class's value. The price is then highly informative, but it recruits no one, and incumbent strength stops mattering. So the project turns the referees' objection into the paper's condition:

> **Competition creates competition when the seller cannot commit to walk away.**

The plan:
- **Theory.** Three regimes: full commitment, limited commitment (a board with a fiduciary out), and partial commitment (takeover defences). The current main result is the limited-commitment case.
- **Test.** Use go-shop windows and other public sale states. Rival entry should rise with incumbent strength where the target's price is informative, and fall where the process is confidential.
- **Feedback version.** Non-fundamental price pressure during the window should raise rival entry, and more so against a strong incumbent.

## 1. The fact that forces the project

These facts come from the model (`sections/02_model.tex`) and the example (`sections/04_equilibrium_results.tex`, Table `tab:reserves` in `sections/07_welfare.tex`):
- The standalone value is 0, and no sale pays 0.
- The seller commits to a cash second-price auction with reserve p > 0.
- Class values are h = 10 and ℓ = 1, each with prior 1/2.
- The incumbent is uniform on [0, r], with r₀ = 1.2, r₁ = 3 and r₂ = 3.6.
- With probability ρ = 1/4 the rival's preparation cost is 0. Otherwise it is c_H = 6.

**A posted price near h.** Take p just below 10.
- The incumbent never meets the reserve, because r ≤ 3.6.
- The low class never meets it either.
- A zero-cost high-class rival still prepares, because its gross profit μ(10 − p) is never negative.
- A high-cost rival never prepares, because μ(10 − p) < 6.

So expected proceeds are p · ρ · π ≈ 10 × ¼ × ½ = **1.25 at every incumbent strength**, and entry is ρ = 0.25 at every strength.

**Compare the paper's reserve table:**

| Reserve | Proceeds at r₀ | Proceeds at r₁ | Entry at r₀ | Entry at r₁ |
|---|---|---|---|---|
| 1/2 (baseline) | 0.393 | 0.873 | 0.25 | 0.523 |
| 1.01 (excludes the low class) | 0.441 | 0.994 | 0.523 | 0.523 |
| 1.55 (also excludes the weak incumbent) | 0.503 | 0.893 | 0.523 | 0.25 |
| just below 10 (posted price) | ≈ 1.25 | ≈ 1.25 | 0.25 | 0.25 |

**Interior reserves do worse.** These are hand calculations, to confirm in T1.
- **At r₀.** A purchase recruits a high-cost rival only while p ≤ 10 − 6/0.731 ≈ 1.79, which matches the paper's 1.793. Proceeds are then at most 1.79 × 0.324 ≈ 0.58.
- **At r₁.** Recruitment needs 0.731 × (10 − (p² + 9)/6) ≥ 6, that is p ≤ 1.326, which matches the paper's 1.325. At p = 1.3, which excludes the low class and still recruits, proceeds are about 0.58 + 0.15 + 0.35 ≈ 1.08: the high-class rival's payment, plus the incumbent's purchase at the reserve when only a low-class rival or no rival prepared. At p = 3, they are 3 × 0.125 ≈ 0.375.
- **At r₂.** No reserve recruits. At p = 1.8, proceeds are about 1.07, and at p = 2.5 about 1.0.

The tie at p = h is resolved by taking p slightly below h. The trading stage cannot change zero-cost entry.

**Reading.** Under its own commitment assumption, the optimal reserve in the example turns the sale into a posted price to the high class. The price is maximally informative (the spread is about p), but no high-cost rival prepares. This is GPT Pro's objection, made exact. To check: the same calculation with continuous classes ("narrow uniform classes" in the paper), where the optimum is interior.

## 2. The lemma: a reserve cannot imitate competition without exclusion

Take both classes admissible (every rival value at or above p). Given a prepared rival of class j with value v_j, the target receives max(p, min(R, v_j)):
- If R < p, the rival wins and pays p.
- Otherwise the second-highest value is paid.

So t_j = E[max(p, min(R, v_j))], and for p ≤ ℓ:
- **The spread.** ∂t_j/∂p = P(R < p) = F(p) for both classes, so ∂(t_H − t_L)/∂p = 0. A reserve below the low class leaves the target-payoff spread unchanged.
- **The rival's profit.** g_j = E[(v_j − max(R, p))₊], with ∂g_j/∂p = −F(p) for both classes. Both profits fall by the same amount, so the reserve is pure deterrence.
- **The incumbent.** It moves the spread smoothly. With r < h, the spread is E[(R − ℓ)₊], which rises with strength because the incumbent's value sometimes falls between the classes.

**Already in the paper.** The algebra is in the example's payoff formulas: the p² terms cancel in Δ_T(r) = (r − ℓ)²/(2r), and both g_j lose p²/(2r). Section 3 also says the reserve term is zero when every value meets the reserve. What is new is only the reading, as a statement about the seller's instrument.

**Consequence (to prove in general):** the seller can open the information channel only by **excluding** the low class. The channel then opens with a jump, as at p = 1.01 in the table. Competition opens it without excluding anyone. This is sharper than "the reserve and the incumbent are substitutes", and it should lead the theory section.

## 3. The headline and the three regimes

**(a) Full commitment.** To prove: the seller-optimal reserve excludes the low class whenever the high class is valuable enough relative to the low class, roughly when π̄·h exceeds ℓ, with π̄ the relevant posterior. The adjustment for entry costs and the incumbent is to work out. Entry then sits at its floor, or is flat, and incumbent strength does not matter. State this as a result, not a concession: committed sellers create information by exclusion, and it recruits no one.

**(b) Limited commitment.** A board must accept any admissible offer above its standalone value, so its effective reserve equals the standalone value.
- **Institutional support:** Revlon duties, and the Delaware requirement of a fiduciary out (Omnicare v. NCS Healthcare, 2003).
- **Theory anchor:** Liu, Mierendorff, Shi and Zhong (AER 2019). A seller without commitment loses its reserve, which moves toward its own value.

The current Proposition 2 is the limited-commitment case, with p equal to the standalone value. To write: a short micro-foundation in which the seller re-optimises after bids, so that p equals the standalone value in equilibrium.

**(c) Partial commitment.** Takeover defences such as a poison pill or a staggered board let a board hold a walk-away price above its standalone value. To prove: the reversal weakens as the credible walk-away price rises, and disappears once it passes the low class's values. This gives a cross-sectional prediction at no extra cost.

**A second possible headline, to check, not to promise.** Under commitment with continuous classes, the reserve that is optimal against a uniform incumbent alone is r/2: 0.6 at r₀ and 1.5 at r₁. It crosses ℓ = 1 as the incumbent strengthens. A stronger incumbent can therefore raise the seller's optimal reserve past the low class, so **competition creates information through the seller's response.** If this survives the full continuation, it saves the reversal even under commitment.

**Other terms, in order of value:**
1. **Publicity.** The seller chooses whether the rival sees the price. The paper's access result shows that access raises proceeds against the strong incumbent inside the recruitment region. To prove: under limited commitment, the seller announces the sale when the incumbent is strong and keeps it confidential when the incumbent is weak. This is also a selection prediction, which the test must handle.
2. **Payment rule.** This already exists in the paper. Competition moves the spread in the direction of 1 − 2ω, so an auction (ω = 0) maximises the channel. It gives a new reason for auctions over negotiation when price recruitment matters.
3. **Deal protection.** A termination fee paid to the incumbent lowers proceeds when the rival wins, so it narrows the spread and deters twice. This item is optional.

## 4. The test

**What the model needs:**
- a public sale state;
- a prepared incumbent whose strength is public;
- unprepared rivals who decide whether to do diligence;
- a target stock that trades in the meantime.

**Settings, best first:**
1. **Go-shop windows.** The signed buyer has a match right, so a rival must beat the incumbent's value and pays about that value. That is close to the paper's sale rule.
   - The window is explicit, usually 30 to 45 days.
   - Rivals must sign NDAs and do diligence to bid.
   - The target trades throughout.
   - The proxy usually reports how many parties were contacted and how many signed NDAs during the window.
   - **Sample:** EDGAR full-text search, 2001 to 2025, finds 688 DEFM14A filings and 328 SC 14D9 filings that mention "go-shop" (count of 30 October 2026). Some filings mention it only to say there is none, so deals with an actual window are fewer, still to count.
2. **Public unsolicited first bids.** The first public bidder is the incumbent, and its offer premium and financing are public.
3. **Leaked processes.** These are public without the seller's choice, so they are the cleanest answer to the selection problem in section 3. **This is where the leak paper and CCC share data.**
4. **Announced strategic reviews.** These are weaker, because there is often no prepared incumbent.

**Measures:**
- **Entry:** NDAs signed by new parties in the window, and topping bids (SDC competition table).
- **Incumbent strength:** the signed or offered premium over the unaffected price, the bidder type, and whether a match right exists.
- **Price informativeness:** option listing, liquidity, and the paper's own test that compares the purchase impact with the sale impact on TAQ order flow.

**Predictions:**
1. **The sign flip.** In public windows with an informative price, rival entry rises with incumbent strength. In confidential processes, it falls (ordinary deterrence).
2. **The feedback test, the decisive one.** This follows the Edmans, Goldstein and Jiang (2012, JF) approach. Non-fundamental price pressure during the window, such as trading forced by mutual-fund flows, should raise rival entry. The effect should be larger against strong incumbents, because rivals rely on the price only when it is informative. This separates "rivals learn from the price" from "the market predicts entry", which an event study cannot do. Use a flow measure that answers Wardlaw's (2020, JF) critique of the original construction.
3. **The defences.** The reversal is weaker in targets with a pill or a staggered board (regime c).
4. **The paper's own order-flow tests** (section 8): the asymmetry between purchase and sale impacts, and orders that predict the winner.

**Main identification threats:**
- The seller's publicity choice depends on incumbent strength. Model it, or use leaks.
- Strong incumbents may sign in hot industries where rivals are also active. Use industry-by-year effects, and compare windows within the same acquirer type.
- Go-shop entry is rare. NDA counts are more frequent than topping bids and should be the main outcome.

## 5. Kill tests, cheapest first

| # | Test | Cost | Stop if |
|---|---|---|---|
| T1 | Compute the seller-optimal reserve with the full continuation, for point-mass and narrow uniform classes, at r₀, r₁ and r₂ | days | (no stop; this fixes the framing) |
| T2 | Prove the lemma in section 2 and the limited-commitment micro-foundation | 2–3 weeks | the micro-foundation needs assumptions a referee rejects |
| T3 | Check the second headline: does the optimal reserve cross ℓ as strength rises, with the trading continuation? | 2–4 weeks | (if no, drop it; regime b still carries the paper) |
| E1 | Read 50 go-shop proxies for NDA counts in the window, contact counts and dates | 1 week | fewer than about half report NDA counts in the window |
| E2 | Count deals with an actual go-shop window, 2001–2025, and those with a match right | 1 week | fewer than about 300 usable windows |
| E3 | Check access to mutual-fund holdings (Thomson s12 or CRSP mutual funds on WRDS) and single-stock options for go-shop targets | 1 week | no flow data: prediction 2 moves to the revision stage |

## 6. How it fits with the job-market paper

- **One research statement.** The leak paper measures what a private sale puts into the price, and whether boards narrow or widen the sale. CCC says when a price in a public sale draws rivals in, and why that needs a seller who cannot commit.
- **Shared data.** The same census fields serve both papers: NDA dates and counts, public dates, and the press-report tag. So do the same CRSP, TAQ and options infrastructure.
- **Shared variation.** A leak makes a sale public without the seller's choice, which is the variation CCC needs.

## 7. Overlap guard

Commitment to a walk-away price is a different object from commitment to deadlines. It is still adjacent to two things:
- Appendix B.2 of "Deal Terms in Takeovers", which varies the target's commitment to exclude weak bidders between rounds;
- Alex's note on "limited commitment power".

Add one question to the Alex conversation: is a solo CCC section on commitment to a walk-away price clear of the joint work?

Go-shop effectiveness is studied by Subramanian (2008) and by Subramanian and Zhao (2020), and go-shops against auctions by Gentry and Stroup (2019). None of these, as far as the search went, conditions go-shop entry on price informativeness or on incumbent strength. To verify.

## 8. Timeline

| Period | Work |
|---|---|
| Nov 2026–Jan 2027 | T1, T2. Rewrite the headline around limited commitment. Add the three regimes |
| Feb–Apr 2027 | T3. The publicity result. E1, E2 and E3. Draft the go-shop test section |
| May–Aug 2027 | The reduced-form go-shop test (prediction 1, and prediction 2 if flow data exist). **Submit** to JF or RFS |
| 2028 | Referee round. The feedback test and the order-flow tests on TAQ, shared with the leak paper |
| By fall 2029 | A revise-and-resubmit, if it comes, on the CV beside the job-market paper |

## 9. References to verify before use

Bulow and Klemperer (1996, AER); Edmans, Goldstein and Jiang (2012, JF); Wardlaw (2020, JF); Liu, Mierendorff, Shi and Zhong (2019, AER), read in the novelty check; Myerson (1981, Mathematics of Operations Research); Omnicare v. NCS Healthcare (Del. 2003); Revlon v. MacAndrews & Forbes (Del. 1986); Subramanian (2008); Subramanian and Zhao (2020, Harvard Law Review), read in the novelty check; Gentry and Stroup (2019, JFE).

## 10. What is new against the current paper

Nothing in the manuscript has changed. This note is a plan.

| Item | Already in the paper | Proposed change | Effect |
|---|---|---|---|
| Seller's commitment | The seller "publicly commits" to a reserve p = 1/2 above a standalone value of 0, and a failed sale pays 0 | State the condition: the board cannot commit to walk away. Set the standalone value equal to the reserve, so that a failed sale pays p | Orders, entry, ownership, thresholds and the recruitment region do not change, because t₀ cancels in the informed trader's class difference e(o)·Δ_T. Proceeds levels rise by p × P(no sale): 0.393 → 0.549 at r₀, 0.873 → 0.912 at r₁, 0.664 → 0.716 at r₂. The access gain at r₁ falls from 0.258 to 0.235 and stays positive. The entry component of the price gap shrinks a little; its sign does not change |
| Full-commitment benchmark | Three illustrative reserves (Table `tab:reserves`) | New proposition: the optimal committed reserve excludes the low class. In the example it is a posted price near h, with entry at ρ at every strength | Answers the objection about the reserve. The table becomes "the optimal reserve by regime" |
| Reserve and spread | In the formulas (the p² terms cancel) | State it as a lemma about the seller's instrument | Explains why a seller cannot imitate competition without excluding the low class |
| Partial commitment | Not present | New result: defences raise the credible walk-away price and weaken the reversal | A new cross-sectional prediction |
| Publicity | Price access is compared exogenously (Proposition `prop:access`) | New result: the seller chooses publicity and announces the sale when the incumbent is strong | A new selection prediction |
| Optimal reserve and strength | Not present | To check: the optimal reserve crosses ℓ as strength rises | Possibly a second headline under commitment |
| Empirics | Predictions only. "Price reaches the rival or not" is already stated, with an opening-auction measurement protocol | Go-shop windows as the setting; a feedback test with non-fundamental price pressure; defences and leaks as variation; a first test with data | The paper gains its first test |
