# Upgrade preparation: the ideas, the cards, and the hard questions

3 November 2026. Source paths are relative to the project root. Source notes are silent; they are not part of the spoken answers.

The current talk and paper control the answers below. Earlier exchanges supply objections and context. Each use of an earlier objection states its current relevance.

**Main recommendation.** Learn the mechanism, its proof, and its boundaries as one argument. The reserve objection deserves the same daily attention as the headline result.

## 1. The core

This ranking concerns what Austin must recall without a slide. It does not rank the length or technical difficulty of the proofs.

### 1. The economic tension, before the title

A prepared bidder is the incumbent bidder, or incumbent. A potential rival bidder, or rival, must still decide whether to prepare. At each fixed belief, a stronger incumbent weakly reduces the rival's return to preparation.

Strength can also make target proceeds more sensitive to the rival's synergy class. That sensitivity can pay for informed trade. The price then carries news about the synergy class before the rival pays to prepare.

**Why first:** this is the answer to both “What is the paper?” and “Why is the result possible?” Every later answer should connect to it.

Source: `overleaf/slot/sections/03_competition_information.tex:5–23,25–65`; `overleaf/slot/sections/04_equilibrium_results.tex:11–64`.

### 2. The economic object and the clock

Entry means costly preparation for an executable proposal. It does not mean a public bid or a completed acquisition. The rival's identity is public. “Discovery” concerns whether that rival prepares, not a search for an unknown bidder. The relevant interval has a public sale opportunity, a prepared incumbent, a traded target, and an unresolved preparation decision.

**Why second:** a panel can reject the application before it reaches the algebra if these objects remain vague.

Source: `overleaf/slot/sections/02_model.tex:5–38,163–170,221–227`.

### 3. The auction split, and what it excludes

Write \(p\) for the reserve and \(R\) for the incumbent's value. For an admissible rival value \(\theta\), define expected target proceeds \(t(\theta)\) and the rival's gross acquisition profit \(g(\theta)\). Then

\[
t(\theta)=\mathbb E_R\max\{p,\min(R,\theta)\},\qquad
g(\theta)=\mathbb E_R(\theta-\max\{p,R\})_+,
\]
\[
t(\theta)+g(\theta)=\theta.
\]

Average within each class to obtain proceeds \(t_H,t_L\) and gross profits \(g_H,g_L\), conditional on preparation. The spread \(\Delta_T=t_H-t_L\) measures how much target proceeds depend on the class. With ranked classes that both meet the reserve,

\[
\Delta_T+(g_H-g_L)=\mathbb E_H\theta-\mathbb E_L\theta.
\]

A stronger incumbent moves this fixed class gap toward target proceeds. This identity excludes the incumbent's rent. It is not total social surplus.

**Why third:** this is the paper's distinctive economic step. Austin should derive it with three cases on a board.

Source: `overleaf/slot/sections/03_competition_information.tex:5–17,25–65`; `overleaf/slot/appendix/A7_welfare.tex:47–58`.

### 4. Why competitive prices leave a return to information

Market makers anticipate preparation. They still do not know the class. A liquidity trader can place the same order as an informed trader.

After order \(x\), let \(\mu(x)\) be the high-class belief and \(e(x)\) the preparation probability. Write \(t_0\) for expected proceeds without preparation. The competitive execution price is

\[
P(x)=t_0+e(x)[t_L-t_0+\mu(x)\Delta_T].
\]

Subtract this price from the high-class expected payoff, \(t_0+e(x)(t_H-t_0)\). For a purchase after class \(H\), the gross return is

\[
e(1)\Delta_T[1-\mu(1)].
\]

For a sale after class \(L\), it is \(e(-1)\Delta_T\mu(-1)\). Entry, payoff sensitivity, and residual doubt all matter. A price rise alone is not the informed trader's profit.

**Why fourth:** this defeats the most natural rational-expectations objection without an appeal to mispricing.

Source: `overleaf/slot/sections/03_competition_information.tex:72–125`; `overleaf/slot/appendix/A2_beliefs_trading.tex:188–244`.

### 5. The theorem is three strict comparisons

Let \(F_0,F_1,F_2\) denote successively stronger incumbent distributions. Gross rival profit at belief \(\mu\) is \(B_i(\mu)=g_{L,i}+\mu(g_{H,i}-g_{L,i})\). Let \(\pi\) be the prior high-class probability, \(c_H\) the high preparation cost, and \(k\) the nonzero order cost. Let \(\rho\) be the zero-cost share, and \(m,M\) the lower and upper class beliefs. The three conditions are

\[
B_0(\pi)<c_H<B_1(M),\qquad
\Delta_0<k<\rho\kappa\Delta_1,\qquad
B_2(M)<c_H,
\]

where \(\kappa=\min\{m,1-M\}\). The first gives room for recruitment. The second forces abstention at the weak incumbent and both correct orders at the strong incumbent. The third stops high-cost preparation despite informative prices. These bounds apply to every permitted order strategy, including mixtures.

**Why fifth:** the result does not select a convenient equilibrium at the three comparison economies. It also does not assert uniqueness at every intermediate strength.

Source: `overleaf/slot/sections/04_equilibrium_results.tex:11–64,323–349`; `overleaf/slot/appendix/A3_proposition2.tex:1–96`.

### 6. Sensitivity, information, entry, and ownership are separate

A larger \(\Delta_T\) means greater payoff sensitivity. It need not change information if informed orders already remain full. The price can reveal the belief, but it never reveals the class. Entry is preparation; ownership also requires a win. High-class ownership rises exactly when

\[
e_HW_H(F_1)>\rho W_H(F_0),
\]

where \(e_H\) is high-class entry at \(F_1\), and \(W_H(F)\) is the win probability of a prepared high-class rival.

**Why sixth:** these distinctions prevent several plausible but false answers after the talk.

Source: `overleaf/slot/sections/02_model.tex:136–161,221–227`; `overleaf/slot/sections/04_equilibrium_results.tex:25–49,246–312`; `overleaf/slot/appendix/A8_empirical.tex:397–418`.

### 7. The fixed-information comparison identifies the force

Hold the joint law of the class and the pre-entry signal fixed. Keep the class value laws and the independent cost law fixed. Require the signal to contain no further value news conditional on the class. Incumbent strength then weakly reduces entry. The claim is “cannot rise,” not “must fall.”

**Why seventh:** this answers whether the result merely renames ordinary deterrence. It also supplies the right counterfactual for empirical work.

Source: `overleaf/slot/sections/04_equilibrium_results.tex:246–312`; `overleaf/slot/appendix/A6_robustness.tex:8–32`.

### 8. The entry floor and sale commitment are substantive assumptions

The low-cost share maintains entry after every price. That entry keeps target proceeds exposed to the class and supplies a lower bound on trade profits. The seller commits to a fixed reserve. The current paper does not solve the seller's optimal choice of terms.

**Why eighth:** these are central boundaries, not minor technical details. A confident answer must state their work before it cites robustness.

Source: `overleaf/slot/sections/02_model.tex:83–102`; `overleaf/slot/sections/03_competition_information.tex:72–125`; `overleaf/slot/sections/09_conclusion.tex:21–35`.

### 9. Research strengthens one branch, not every outcome

The informed trader privately chooses the probability of successful research. At an even prior, research and entry rise with the spread on the equilibrium branch where a purchase recruits. This rise stops at the cap. Other equilibria can coexist. Research also replaces liquidity orders, which explains the fall in low-class entry on that branch.

**Why ninth:** the extension adds an economic margin. Its qualifications must stay attached to its slogan.

Source: `overleaf/slot/sections/05_research.tex:3–25,33–68,97–114,160–164`.

### 10. The empirical claim and the next research decision

The paper supplies conditional predictions and a measurement protocol. The stated task confirms that no empirical test has run. The key outcome is preparation after a public signal, not a takeover return by itself. Seller choice is an open theoretical step. The thesis plan should turn these gaps into dated decisions, not treat them as completed results.

**Why tenth:** an upgrade panel assesses whether the researcher can distinguish a theorem, an interpretation, and a feasible next step.

Source: `overleaf/slot/sections/08_empirical.tex:3–17,19–35,77–90`; `overleaf/slot/sections/09_conclusion.tex:30–35`. Proposed agenda: `audit/jmp_search_2026_10_30/MEMO.md:114–134,180–200`.

## 2. The card list

### Daily: twelve cards, fifteen minutes

Use eight minutes for D01–D12. Allow about forty seconds per card, including the pause before the answer. Use three minutes for one weak spot from Section 3. Use two minutes to derive one equation without notes. Use the final two minutes to repeat the least fluent answer.

Rotate the two-minute opening and close into the eight-minute block. On those days, omit three cards already fluent. Do not add both extended scripts to the daily load.

#### D01 — Open: what is the question? — daily

**Spoken answer; about 30 seconds:** “Does a stronger incumbent bidder always deter a potential rival bidder from costly preparation? I call these bidders the incumbent and the rival, and show that strength can make informed trade worthwhile. The price then carries news about the synergy class and can attract the rival despite weakly lower acquisition profits at every fixed belief.”

Source: `overleaf/slot/sections/01_introduction.tex:3–15,27–47`.

#### D02 — Explain the mechanism without notation — daily

“A weak incumbent can leave much of a good match's value with the rival. A stronger incumbent can transfer more of the class value gap to target proceeds, which raises the value of class information. If that makes informed trade worthwhile, the price can induce costly preparation.”

Source: `overleaf/slot/sections/03_competition_information.tex:44–65,102–125`; `overleaf/slot/sections/04_equilibrium_results.tex:11–64`.

#### D03 — Who knows what, and when? — daily

“The incumbent knows its value; the informed trader knows the rival's synergy class; market makers see the order and set the price. The rival sees the price, learns its preparation cost, and decides whether to prepare. Preparation reveals its value and permits a bid under the committed sale rule.”

Source: `overleaf/slot/sections/02_model.tex:83–102,106–134,163–170`.

#### D04 — What are the two auction objects? — daily

“The target-payoff spread is the difference in expected target proceeds across synergy classes, conditional on preparation. The preparation threshold is the belief at which the rival's expected acquisition profit covers the high cost. Incumbent strength weakly raises the spread and, while low-class profit is below that cost, weakly raises the threshold.”

Silent algebra: \(\Delta_T=t_H-t_L\), \(\tau=(c_H-g_L)/(g_H-g_L)\), where \(g_H>g_L\).

Source: `overleaf/slot/sections/03_competition_information.tex:25–42,72–98,129–145`.

#### D05 — Why does informed trade pay at a fair price? — daily

“Market makers price expected entry and average over the two classes. The informed trader knows the class, while liquidity trade prevents the order from proving it. Its gross return equals entry times the target-payoff spread times the market's remaining doubt.”

Source: `overleaf/slot/sections/03_competition_information.tex:72–125`.

#### D06 — Why does the price reveal a belief but never the class? — daily

“A liquidity trader can place every permitted order in either class, so every posterior stays strictly between zero and one. With a positive payoff spread and entry floor, equal prices imply equal class beliefs. The rival can therefore recover the market's belief without learning the class itself.”

Source: `overleaf/slot/sections/02_model.tex:136–161`; `overleaf/slot/appendix/A2_beliefs_trading.tex:1–120,140–144`.

#### D07 — State the result and its proof in words — daily

“At three successively stronger incumbents, strict bounds force an uninformative market, informative trade with extra entry, then informative trade with only floor entry. The weak economy's maximum trade gain falls below cost; the strong economy's minimum correct-order gain exceeds cost. At the last economy, even the best price signal cannot justify the high preparation cost.”

Source: `overleaf/slot/sections/04_equilibrium_results.tex:11–64`; `overleaf/slot/appendix/A3_proposition2.tex:1–96`.

#### D08 — What happens if information stays fixed? — daily

“At every fixed belief, a stronger incumbent weakly lowers the rival's gross profit. If the pre-entry experiment and independent cost law stay fixed, entry cannot rise. The reversal therefore needs a change in the information that reaches the rival.”

Source: `overleaf/slot/sections/04_equilibrium_results.tex:246–312`; `overleaf/slot/appendix/A6_robustness.tex:8–32`.

#### D09 — Why not use a high reserve? — daily

“A high reserve can defeat the reversal, and the displayed example permits it. A price just below the high value earns more than the printed reserve choices and leaves entry at its floor. My result concerns a fixed sale rule; the seller's optimal terms remain an open question.”

Source: `overleaf/slot/appendix/A7_welfare.tex:145–159,193–239`; `overleaf/slot/sections/09_conclusion.tex:30–35`. The strict interior comparison is derived in W1 below, **new, not in the paper**.

#### D10 — Why can this trader know something useful? — daily

“The information concerns target-side facts that affect the rival's fit, before the rival commits to diligence. Exact class knowledge and no private incumbent-value signal are assumptions, not measured facts. Complementary private signals preserve the reversal at suitable parameters, even when the rival's signal is more accurate.”

Source: `overleaf/slot/sections/02_model.tex:21–34,83–91,106–134`; `overleaf/slot/sections/06_robustness.tex:58–82`; `overleaf/slot/appendix/A6_robustness.tex:526–572`.

#### D11 — What evidence do you have, and what is next? — daily

“The paper establishes a mechanism and conditional predictions; I do not yet have an empirical test of this channel. I will first measure public sale intervals with a prepared incumbent and later rival preparation. I will then separate price news about fit from bid anticipation and from the seller's choice of publicity.”

Source for present scope: `overleaf/slot/sections/02_model.tex:5–38`; `overleaf/slot/sections/08_empirical.tex:77–90`; `overleaf/slot/sections/09_conclusion.tex:30–35`. The proposed sequence is advice, not a completed result.

#### D12 — Close: what should the panel remember? — daily

**Spoken answer; about 30 seconds:** “At a fixed sale rule, incumbent strength can make information about the rival more valuable to the stock market. That information can induce preparation, although strength weakly reduces acquisition profit at every fixed belief; the three comparison economies have unique outcomes. The next questions are whether sellers choose terms that preserve this channel and how often it operates.”

Source: `overleaf/slot/sections/04_equilibrium_results.tex:11–64,246–257`; `overleaf/slot/sections/09_conclusion.tex:21–35`.

### Mechanism and proof: every few days

#### M01 — Derive the sale payoff

**Frequency:** every few days. **Answer:** “If the rival wins, it pays the larger of the reserve and incumbent value. If the incumbent wins, it pays the rival's admissible value. Add the rival's profit to target proceeds in each case and the sum is the rival's value.”

Source: `overleaf/slot/sections/03_competition_information.tex:5–17`.

#### M02 — Define stronger without a number

**Frequency:** every few days. **Answer:** “Strength means an upward first-order stochastic shift in the public distribution of incumbent value. The realized value remains private until the bid. This is not a comparative static in an announced offer or an observed bid premium.”

Source: `overleaf/slot/sections/02_model.tex:30–38,51–56`.

#### M03 — What do the reserve assumptions do?

**Frequency:** every few days. **Answer:** “The baseline ranks the class distributions and requires every rival value to meet the reserve. Then stronger competition weakly increases the target-payoff spread. If the low class fails the reserve more often, a sale-completion term can reverse that sign.”

Source: `overleaf/slot/sections/02_model.tex:58–75`; `overleaf/slot/sections/03_competition_information.tex:25–57`.

#### M04 — Why does the incumbent still bid its value?

**Frequency:** every few days. **Answer:** “The incumbent already knows its own value and completed preparation. A truthful bid is weakly dominant in the committed second-price auction, whatever it learns about the rival. The paper imposes that truthful continuation; it does not solve preemptive offers or renegotiation.”

Source: `overleaf/slot/sections/02_model.tex:93–102,174–219`; `overleaf/slot/appendix/A1_payoffs.tex:59–69`.

#### M05 — What does the entry floor buy?

**Frequency:** every few days. **Answer:** “Some rival preparation occurs after every price. That keeps the target claim exposed to the class and gives a positive lower bound on correct-order gains. Without that floor, an uninformative market with no entry survives throughout the displayed example.”

Source: `overleaf/slot/sections/03_competition_information.tex:72–125`. Last sentence: W6 derivation below, **new, not in the paper**; earlier question: `discussion/2026-10-26/ming-email.md:11–19`.

#### M06 — Is the price effect just manipulation?

**Frequency:** every few days. **Answer:** “Market makers anticipate the entry response. With no initial stake, the informed trader earns only the difference between its class-contingent payoff and the execution price, less cost. Common gains from extra entry cancel from that residual, and wrong-signed orders do not pay.”

Source: `overleaf/slot/sections/02_model.tex:106–134`; `overleaf/slot/sections/03_competition_information.tex:102–125`; `overleaf/slot/appendix/A2_beliefs_trading.tex:188–244`.

#### M07 — What is held fixed after a deviation?

**Frequency:** every few days. **Answer:** “A unilateral order deviation faces the candidate price schedule and entry rule. It does not announce a new strategy to market makers. Across incumbent strengths, I solve a new equilibrium and allow the schedules to change.”

Source: `overleaf/slot/sections/02_model.tex:174–219`; `overleaf/slot/appendix/A2_beliefs_trading.tex:188–244`.

#### M08 — Does more entry imply more rival ownership?

**Frequency:** every few days. **Answer:** “Entry is preparation, while ownership also requires the rival to beat the incumbent. High-class ownership rises only if the entry gain outweighs any fall in its conditional win probability. A high-class rival that always outbids both incumbents satisfies that extra condition.”

Source: `overleaf/slot/sections/02_model.tex:221–227`; `overleaf/slot/sections/04_equilibrium_results.tex:35–49`.

#### M09 — What happens between the three economies?

**Frequency:** every few days. **Answer:** “An uninformative market and an informative market can coexist at intermediate strengths. The paper characterises that region under stated tie rules. The main three-economy comparison does not require a selection between those intermediate equilibria.”

Source: `overleaf/slot/sections/04_equilibrium_results.tex:323–349,379–424`.

### Scope, evidence, and research: every few days

#### S01 — Is this just an existing feedback paper?

**Frequency:** every few days. **Answer:** “Price feedback and information production already exist in the literature. Here the auction transfers the class value gap toward the traded claim as it reduces the rival's acquisition return. That links competition to the supply of pre-entry information and permits a reversal of deterrence.”

Source: `overleaf/slot/sections/01_introduction.tex:127–161`; `overleaf/slot/sections/03_competition_information.tex:25–65`.

#### S02 — Whose market structure do you use?

**Frequency:** every few days. **Answer:** “The alternative arrival comes from Dow and Gorton. The unit menu, presence probability, and order cost follow Edmans, Goldstein and Jiang's 2015 paper. Dow, Goldstein and Guembel provide the closest information-production antecedent.”

Source: `overleaf/slot/sections/02_model.tex:148–161`; `overleaf/slot/sections/01_introduction.tex:127–132`; `overleaf/slot/comparison.tex:84–94`.

#### S03 — Why can a banker or the target not do this?

**Frequency:** every few days. **Answer:** “A credible direct signal could supply the same useful information. The paper does not compare that channel with prices or prove that the target cannot certify fit. Its contribution concerns the incentive to produce information through trade when direct information is incomplete.”

Source: the specified information structure, `overleaf/slot/sections/02_model.tex:21–28,163–170`; fixed-experiment result, `overleaf/slot/appendix/A6_robustness.tex:8–32`. Interpretation: **new inference**, developed in W3.

#### S04 — Why does research rise?

**Frequency:** every few days. **Answer:** “Research is private and changes the chance that the informed trader learns the class. On the branch where a purchase recruits, a wider payoff spread raises the return to success. The chosen intensity rises until the cap, but this does not establish uniqueness across all research equilibria.”

Source: `overleaf/slot/sections/05_research.tex:3–25,33–68,97–114`.

#### S05 — Why does research reduce low-class entry?

**Frequency:** every few days. **Answer:** “Successful research replaces a possible liquidity order. In the low class, the informed trader sells or abstains, so research removes some liquidity purchases that would have induced entry. Total entry rises on the stated branch because the high-class increase is larger.”

Source: `overleaf/slot/sections/05_research.tex:14–17,47–68`; `overleaf/slot/appendix/A5_research.tex:186–283`.

#### S06 — Who gains from price access?

**Frequency:** every few days. **Answer:** “At the strong comparison economy, access raises expected target proceeds and acquisition surplus net of preparation costs. Full informed orders occur with or without access, so their costs do not explain that difference. Liquidity traders bear adverse-selection losses; the result does not say everyone gains.”

Source: `overleaf/slot/sections/07_welfare.tex:5–39`; `overleaf/slot/appendix/A7_welfare.tex:14–23,47–91`.

#### S07 — State the price-impact prediction correctly

**Frequency:** every few days. **Answer:** “Assume full informed purchases and sales, with the prior below the preparation threshold. Weight each price impact by its order frequency, relative to the no-order price. The purchase side exceeds the sale side exactly when a purchase recruits.”

Source: `overleaf/slot/sections/08_empirical.tex:19–35`; `overleaf/slot/appendix/A8_empirical.tex:57–145`.

#### S08 — Why can orders predict the winner without recruitment?

**Frequency:** every few days. **Answer:** “Orders carry class news even when every cost type makes the same preparation decision after every order. That news predicts the winner if a prepared high-class rival wins more often than a low-class rival. A winner correlation alone therefore does not establish a price effect on entry.”

Source: `overleaf/slot/appendix/A8_empirical.tex:397–418`.

#### S09 — What would make the empirical interpretation fail?

**Frequency:** every few days. **Answer:** “The price may react to preparation already under way, or to the anticipated public bid. Incumbent strength and publicity may also reflect the same sale prospects that attract rivals. I need the chronology and a source of variation that separates those channels.”

Source for chronology: `overleaf/slot/sections/08_empirical.tex:77–90`. Identification assessment: **new inference**; proposed issues also appear in `audit/jmp_search_2026_10_30/ccc_seller_terms.md:109–118`.

#### S10 — Is this the job-market paper?

**Frequency:** every few days. **Answer:** “This is my developed theory chapter; I do not treat the job-market choice as settled. My current plan pairs it with an empirical project on information around private sale processes. I will choose the main paper after a data pilot, a novelty check, and a clear boundary with the joint projects.”

Source for the proposed portfolio: `audit/jmp_search_2026_10_30/MEMO.md:5–20,24–30,114–134,180–200`. This is proposed wording, not evidence of a final personal decision.

### Lookup only

#### L01 — What do the slot parameters mean?

**Frequency:** lookup only. **Answer:** “Lambda is the informed presence probability; beta is each nonzero order probability conditional on a liquidity trader. The unconditional liquidity mass in one direction is \(b=(1-\lambda)\beta\). The ratio \(u=\lambda/b\) fixes the posterior bounds, but does not alone fix order frequencies.”

Source: `overleaf/slot/sections/02_model.tex:106–161`; `overleaf/slot/appendix/A8_empirical.tex:21–54`.

#### L02 — Why one third in one place and one half elsewhere?

**Frequency:** lookup only. **Answer:** “The one-third restriction bounds the zero-order posterior under every strategy. The main three-economy proof needs only the nonzero-order bounds, which hold below one half. Once full informed orders are forced, the zero-order posterior equals the prior.”

Source: `overleaf/slot/appendix/A2_beliefs_trading.tex:1–120`; `overleaf/slot/sections/04_equilibrium_results.tex:11–25`; `overleaf/slot/comparison.tex:165–171`.

#### L03 — What does the Laplace comparison preserve?

**Frequency:** lookup only. **Answer:** “Match the likelihood-ratio bound through \(1+u=\exp(2/\xi)\). This matches extreme posteriors, not the whole signal distribution or the order-choice problem. The Laplace version admits continuous sizes and requires a separate marginal-profit argument.”

Source: `overleaf/slot/comparison.tex:96–132,176–202,291–314`.

#### L04 — What does the numerical example establish?

**Frequency:** lookup only. **Answer:** “The benchmark is a strict numerical witness, not a calibration. Entry moves from one quarter to about one half and returns to one quarter. Its final exclusion margin is small, so I distinguish the initial reversal from the exact third comparison.”

**Benchmark use:** entry \(0.25\to0.522757\to0.25\); final cost margin \(0.002689\). Sources: `overleaf/slot/sections/04_equilibrium_results.tex:89–118`; `overleaf/slot/numbers.tex:107–111,693–694`; `overleaf/slot/appendix/A9_parameters.tex:64–67,271–286`.

#### L05 — Can counts identify informed trade?

**Frequency:** lookup only. **Answer:** “Under full informed orders, counts identify informed presence if the prior is known and differs from one half. At one half, counts identify volume alone. The sale impact can identify more if the required payoff scale and entry conditions are known.”

Source: `overleaf/slot/appendix/A8_empirical.tex:280–307`.

#### L06 — What does the payment-rule comparison prove?

**Frequency:** lookup only. **Answer:** “In the separate bargaining institution, competition moves the spread with the sign of one minus twice the seller's weight. This shows that how the sale splits value matters for the information channel. It does not rank all auctions and negotiations or solve the seller's optimal procedure.”

Source: `overleaf/slot/sections/07_welfare.tex:43–60`; `overleaf/slot/appendix/A7_welfare.tex:95–141`.

### Extended opening: about two minutes

This is a rehearsal piece, not an additional card. Use the short opening during most daily drills.

“Does a stronger incumbent bidder always deter a potential rival bidder from a takeover contest? I call these bidders the incumbent and the rival. The usual force is clear: stronger competition weakly reduces what the rival expects to earn after it pays for preparation. I keep that force and ask whether competition also changes what the rival can learn before it pays.”

Source: `overleaf/slot/sections/01_introduction.tex:3–15`; `overleaf/slot/sections/04_equilibrium_results.tex:246–257`.

“The setting is a public sale opportunity while the target's stock still trades. The incumbent is prepared, but the rival still faces costly diligence before an executable proposal. An informed trader knows facts about the rival's synergy class. Its order can put some of that news into the price, which the rival observes before preparation.”

Source: `overleaf/slot/sections/02_model.tex:5–28,163–170`.

“The key link comes from the auction. A stronger incumbent can shift more of the class value gap into target proceeds. That makes information about the class more valuable to the informed trader. Trade can then become worthwhile, even though the rival's acquisition profit weakly falls at every fixed belief.”

Source: `overleaf/slot/sections/03_competition_information.tex:25–65,102–125`.

“Under explicit conditions, I obtain three unique outcomes: no informed trade, informative trade with extra entry, then informative trade without extra entry. The result concerns a fixed sale rule and a price before preparation. I will show the mechanism, explain those conditions, and state the limits that matter for seller choice and evidence.”

Source: `overleaf/slot/sections/04_equilibrium_results.tex:11–64`; `overleaf/slot/sections/09_conclusion.tex:30–35`.

### Extended close: about two minutes

“The central result is that competition can alter the information available before rival preparation. A stronger incumbent weakly reduces the rival's acquisition profit at every fixed belief. Under ranked classes that both meet the reserve, it also weakly widens the gap in target proceeds across those classes. A strict increase in that gap can make informed trade worthwhile.”

Source: `overleaf/slot/sections/03_competition_information.tex:25–65`; `overleaf/slot/sections/04_equilibrium_results.tex:11–64`.

“The price carries news about the synergy class; it never reveals the class itself. With the information held fixed, stronger competition cannot raise entry. The reversal comes from the response of information. At the three comparison economies, strict bounds determine the outcome, although intermediate strengths can admit more than one equilibrium.”

Source: `overleaf/slot/appendix/A2_beliefs_trading.tex:1–120`; `overleaf/slot/sections/04_equilibrium_results.tex:11–64,246–257,323–349`.

“Costly research adds a further margin on the branch where a purchase recruits. Within that branch, research and entry rise with the payoff spread until research reaches its cap. Price access also raises expected proceeds and net acquisition surplus at the strong comparison economy. These are conditional claims, not statements that all information or all competition benefits every participant.”

Source: `overleaf/slot/sections/05_research.tex:47–68`; `overleaf/slot/sections/07_welfare.tex:5–39`.

“Two tasks now matter most. The first is to solve the seller's choice of terms, since a high reserve can remove the reversal. The second is to measure public sale intervals and rival preparation, then distinguish information from bid anticipation. Those tasks determine how broadly this mechanism can explain takeover competition.”

Source: `overleaf/slot/appendix/A7_welfare.tex:193–239`; `overleaf/slot/sections/08_empirical.tex:77–90`; `overleaf/slot/sections/09_conclusion.tex:30–35`.

## 3. Weak spots, ranked by danger

The rank combines two risks: damage to the main interpretation and the chance that a concise answer fails. The first six deserve repeated oral practice.

### W1. The seller can choose away the reversal

**Attack:** “Your seller can commit to a reserve. Why tolerate all this information production when a high posted price earns more?”

**Spoken defence:** “The result holds at a fixed sale rule, and this objection limits its seller-choice interpretation. In the displayed example, a price just below the high value does earn more than the reserves in the table. It leaves preparation at its floor and removes the strength comparison. The paper therefore establishes a channel conditional on sale terms; optimal terms remain open.”

**Likely follow-up:** “So the low reserve is irrational?”

**Answer:** “The paper does not establish that this reserve is optimal for its seller. A commitment friction might justify a different rule, but that requires a new argument. I cannot treat the proposed limited-commitment account as an existing result.”

**Status:** **no full defence: best honest line** for seller optimality. The fixed-rule theorem remains supported.

**Sources:** `overleaf/slot/sections/02_model.tex:42–49,93–102`; `overleaf/slot/sections/07_welfare.tex:64–112`; `overleaf/slot/appendix/A7_welfare.tex:145–159,193–239`; `overleaf/slot/sections/09_conclusion.tex:30–35`.

**Earlier point:** still applies, directly. The seller memo targets the slot version. Its proposed commitment account is not a proved interpretation of the current paper: `audit/jmp_search_2026_10_30/ccc_seller_terms.md:3–14,66–78,161–173`.

**Independent calculation — benchmark use.** Use \(h=10\), \(\ell=1\), \(\pi=1/2\), \(\rho=1/4\), \(c_H=6\), \(k=1/50\). The three incumbent supports end at \(1.2,3,3.6\). The slot has \(M=\mathrm e/(1+\mathrm e)\) and \(m=1-M\). Exact input sources: `overleaf/slot/numbers.tex:86,5072–5081,5312`; definitions: `overleaf/slot/comparison.tex:84–100,123–132`.

Take a committed reserve \(p=9.9\). It excludes the incumbent and low-class rival at all three strengths. The auction kernel gives

\[
t_0=t_L=g_L=0,\qquad t_H=p,\qquad g_H=h-p=0.1,\qquad\Delta_T=p.
\]

Thus \(B(\mu)=0.1\mu<6\) for every posterior. Every zero-cost rival prepares; no high-cost rival prepares. At this strictly interior price, even the lowest posterior gives positive expected gross profit to a zero-cost rival. Moreover,

\[
\rho m\Delta_T-k
=\tfrac14(1-M)9.9-0.02
\simeq0.645630>0.
\]

The same bound therefore forces full informed orders. Expected proceeds and sale probability are

\[
\mathbb E[\text{proceeds}]=\pi\rho p=1.2375,\qquad
\Pr(\text{sale})=\pi\rho=0.125,\qquad
\Pr(\text{preparation})=\rho=0.25.
\]

This proof at \(p=9.9\), and the table below, are **new, not in the paper**. They use the paper's reserve kernel. The paper already reports the boundary \(p=h\), with proceeds \(1.25\), under its zero-cost preparation convention (`appendix/A7_welfare.tex:237–239`).

| Reserve, all numbers benchmark-only | Proceeds, weak | Proceeds, strong | Proceeds, very strong | Entry, weak | Entry, strong |
|---|---:|---:|---:|---:|---:|
| \(0.5\) | 0.392708 | 0.872531 | 0.664236 | 0.250000 | 0.522757 |
| \(1.01\) | 0.440564 | 0.994384 | 0.878519 | 0.522757 | 0.522757 |
| \(1.55\) | 0.502822 | 0.893073 | 1.039019 | 0.522757 | 0.250000 |
| \(9.9\) | 1.237500 | 1.237500 | 1.237500 | 0.250000 | 0.250000 |

The first two strength columns reproduce the printed reserve comparisons. The third-strength extensions and the final row follow from the displayed kernel. For reproduction, use

\[
\mathcal R=t_0+\pi e_H(t_H-t_0)+(1-\pi)e_L(t_L-t_0),
\]

with class entry rates implied by each posterior's cost comparison. Full orders are forced in every row except the baseline weak economy; there \(\Delta_T=1/60<k\) forces informed abstention. Sources: `overleaf/slot/appendix/A7_welfare.tex:145–190`; registry comparison: `overleaf/slot/numbers.tex:3229–3235,3274–3280,3319–3325,3364–3370,3409–3415,3454–3460,4292`.

**What this establishes:** the near-high price strictly beats every printed reserve choice at the comparison strengths. It defeats a claim that the displayed low reserve follows from revenue maximisation. It does not disprove the conditional theorem. Nor does this comparison prove a global optimum over every reserve, continuation, or sale mechanism.

**Three corrections to the planning memo:**

- Its “maximally informative” description confuses payoff sensitivity with information. At \(p=9.9\), full orders yield the same \((m,\pi,M)\) as any other full-order equilibrium with this slot. The class remains uncertain. See `ccc_seller_terms.md:49` and `overleaf/slot/comparison.tex:123–132`.
- Its “At \(r_2\). No reserve recruits” statement is false if the reserve can fall below the baseline. For \(p\le1\),
  \[
  B_{3.6,p}(M)=M(10-3.6/2)+(1-M)/(2\cdot3.6)-p^2/(2\cdot3.6).
  \]
  The constant term is \(6.03203332\). Recruitment occurs for \(0<p<0.48024983\); at \(p=0.1\), gross profit is \(6.03064443>6\). The trade bound remains strict because the spread does not depend on \(p\) in this range. This correction is **new, not in the paper**. Sources: `ccc_seller_terms.md:42–49`; `overleaf/slot/sections/04_equilibrium_results.tex:156–176`.
- Its claim that the current result is already the limited-commitment case is unsupported. The paper commits to a positive reserve above zero standalone value. A revised payoff and commitment argument would be new work. Sources: `ccc_seller_terms.md:70–76,167–172`; `overleaf/slot/sections/02_model.tex:42–49,93–102`.

Do not defend the low reserve with an unproved legal or institutional claim.

### W2. The trader's information is unusually well targeted

**Attack:** “Why does an outsider know the rival's class, yet know nothing about the incumbent's value? You assign exactly the information you need.”

**Spoken defence:** “The paper isolates target-side facts about a particular match before the rival completes diligence. Exact class knowledge and no private signal about incumbent value are maintained assumptions. The private-signal extension relaxes the first information asymmetry and permits a better-informed rival at suitable parameters. It does not establish the result with arbitrary correlated news about both bidders.”

**Likely follow-up:** “If the class is ten or one, does the trader know the value after all?”

**Answer:** “Yes, in the point-value example class knowledge determines value. With dispersed class distributions, it determines a distribution and leaves value uncertainty. I should make that distinction explicit.”

**Status:** **the paper supports this** scoped defence. The prevalence of the assumed information remains unmeasured.

**Sources:** `overleaf/slot/sections/02_model.tex:21–34,58–75,83–91,106–134`; `overleaf/slot/sections/04_equilibrium_results.tex:89–108`; `overleaf/slot/sections/06_robustness.tex:58–82`; `overleaf/slot/appendix/A6_robustness.tex:389–440,526–572`.

**Earlier point:** still applies. Alex's objection to two fixed values is now addressed by class distributions, but the allocation of information remains substantive. Sources: `audit/alex_meeting_2026_10_21/BRIEF.md:133–142`; `discussion/2026-10-26/ming-email.md:11–15`. Do not use the small private-signal perturbation at the baseline as evidence for the distinct example with a more accurate rival.

### W3. A rumour, a banker's call, or target certification could replace the price

**Attack:** “Why must this information travel through a stock price? Why does the target not certify fit, or pay a banker to tell the rival?”

**Spoken defence:** “The paper does not establish that prices dominate credible direct communication. A direct signal with the same information can support the same preparation decision. The distinctive force is that competition changes the return to information produced through trade. If cheap certification already supplies that information, this particular force has less work to do.”

**Likely follow-up:** “So you need a communication failure?”

**Answer:** “I need useful information that the rival does not already receive before preparation. A theory of who can certify it, at what cost, remains outside the paper. I would state that friction rather than assert that sellers or bankers cannot communicate.”

**Status:** **no full defence: best honest line** for the superiority or necessity of prices.

**Derivation — new, not in the paper:** suppose a direct message \(S\) induces the same conditional class beliefs as the price, with no extra within-class value news. At each message the rival faces the same \(B_F(\mu)\) and cost, so it makes the same preparation decision. If the joint law of \((j,S)\) stays fixed as \(F\) strengthens, each \(B_F(\mu)\) weakly falls. Thus entry cannot rise through that fixed message alone. This substitutes an experiment; it does not prove an optimal disclosure policy.

**Sources:** `overleaf/slot/sections/03_competition_information.tex:72–98`; `overleaf/slot/appendix/A6_robustness.tex:8–32`.

**Earlier point:** the concern survives. The older discrete exploration reports a certification exercise, but its numerical optimum belongs to a different environment. Do not transfer that number to the slot. Source: `audit/discrete_exploration_2026_10_21/memos/SYNTHESIS.md:88–99`.

### W4. How common is the required interval?

**Attack:** “Most sale competition develops in private. How many transactions actually have your public-price interval?”

**Spoken defence:** “The relevant population is narrower than all takeovers. It requires a public opportunity, a prepared incumbent, and a rival whose substantive preparation still lies ahead. The paper describes that interval and cites evidence of preparation costs, but it does not estimate its frequency. A prevalence count is therefore my first empirical task.”

**Likely follow-up:** “Can you give us a percentage?”

**Answer:** “I do not have a defensible percentage. I need a dated sample that distinguishes public disclosure, incumbent readiness, rival contacts, and substantive preparation. Counts of filings with a phrase do not supply that denominator.”

**Status:** **no full defence: best honest line** for prevalence.

**Sources:** `overleaf/slot/sections/02_model.tex:5–38`; `overleaf/slot/sections/08_empirical.tex:77–90`. The go-shop count is explicitly a filing-search count, not a count of usable settings: `audit/jmp_search_2026_10_30/ccc_seller_terms.md:85–101,124–129`.

**Earlier point:** still applies to the slot. The local empirical note distinguishes evidence of informed pre-bid trade from the paper's exact information channel: `discussion/jihee_empirical_questions.md:175–206,269–278`. Its cited evidence does not establish prevalence of this interval.

### W5. Theory without a demonstrated fact

**Attack:** “You have a striking theory, but no empirical test. What fact does it explain?”

**Spoken defence:** “I do not claim an observed reversal that the paper already explains. The contribution is a disciplined possibility result: information production can reverse deterrence under explicit conditions. It gives separate predictions for preparation and ownership, which need not move together. The next empirical step must establish the setting and then test the channel.”

**Likely follow-up:** “What would count against your interpretation?”

**Answer:** “A lack of public intervals before rival preparation would restrict its practical reach. Within usable intervals, evidence that the relevant price news arrives only after preparation would contradict the proposed chronology. A failed causal entry prediction would matter more than a positive return around a later bid.”

**Status:** **no full defence: best honest line** for an established empirical explanation. The conditional theory contribution is supported.

**Sources:** `overleaf/slot/sections/04_equilibrium_results.tex:11–49`; `overleaf/slot/sections/08_empirical.tex:3–17,49–69,77–90`; `overleaf/slot/sections/09_conclusion.tex:30–35`. The proposed rejection criteria are **new inference**, not results in the paper.

**Earlier point:** still applies. The earlier note explicitly finds no study of the exact pre-diligence signal within its reviewed set: `discussion/jihee_empirical_questions.md:202–206`. Do not turn that limited literature statement into a claim that no such study exists anywhere.

### W6. The entry floor removes a self-confirming failure

**Attack:** “Without your low-cost rivals, no trade and no entry is an equilibrium at every strength. Is the result an assumption?”

**Spoken defence:** “The floor is substantive: it guarantees some preparation after every price and supports trade profits even without recruitment. Without it, the displayed example admits an uninformative equilibrium with no entry at every strength. The theorem shows that a stronger incumbent forces informative trade once this baseline activity supplies enough payoff exposure. The continuous-cost extension preserves a low-cost component; it does not remove the economic floor.”

**Likely follow-up:** “Does the rise in entry itself need that floor?”

**Answer:** “A selected informative equilibrium can exhibit recruitment without it, as the earlier exchange notes. The paper's strict uniqueness argument does need a positive gain floor. I would not replace that argument with an unsupported claim about equilibrium selection.”

**Status:** **new inference** for the no-floor derivation below. The stated role of the floor and the support-restricted cost extension are supported by the paper.

**Derivation — new, not in the paper; benchmark use.** Set \(\rho=0\), so every rival pays \(c_H=6\). At the prior,

\[
B_F(1/2)=\mathbb E(\theta-\max\{p,R\})_+
\le \mathbb E\theta-p
=\tfrac12(10+1)-\tfrac12=5<6.
\]

This inequality holds for every incumbent distribution because both rival values meet the reserve. Let the informed trader abstain in both classes. Liquidity orders have the same law in both classes, so all three orders leave belief at the prior. No rival prepares, and every price equals \(t_0\). The class then has no effect on target payoff. A nonzero order earns zero gross expected residual and costs \(k>0\), so abstention is optimal. These choices support the uninformative equilibrium at every strength in this benchmark. The claim need not hold in other economies where the prior alone covers the preparation cost.

**Sources:** primitives `overleaf/slot/numbers.tex:5072–5081`; price and profit structure `overleaf/slot/sections/03_competition_information.tex:72–125`; continuous costs `overleaf/slot/sections/06_robustness.tex:9–23`; `overleaf/slot/appendix/A6_robustness.tex:78–155`.

**Earlier point:** still applies and now has a transparent slot derivation. The Ming exchange explicitly raises it: `discussion/2026-10-26/ming-email.md:11–19`. Its exact second-branch endpoints are not needed for this defence.

### W7. Why the slot, and what is new relative to the literature?

**Attack:** “Did you choose an unusual market to force the answer? Why not Kyle? Is this just Dow and Gorton or Edmans, Goldstein and Jiang?”

**Spoken defence:** “The slot uses an established alternative-arrival idea and a finite order menu. Every permitted order has liquidity support, which makes the equilibrium comparisons explicit. The new economic step is the auction's effect on the payoff to information about the rival. I do not claim a general result for every market structure.”

**Likely follow-up:** “Which paper supplies which piece?”

**Answer:** “Dow and Gorton supply alternative arrivals; Edmans, Goldstein and Jiang's 2015 paper supplies the menu, presence, and order-cost devices. Dow, Goldstein and Guembel are the closest information-production antecedent. The 2012 Edmans, Goldstein and Jiang paper concerns takeover effects of prices, a different contribution.”

**Status:** **the paper supports this** positioning. The report does not claim an exhaustive new literature search.

**Sources:** `overleaf/slot/sections/01_introduction.tex:127–161`; `overleaf/slot/sections/02_model.tex:148–161`; `overleaf/slot/comparison.tex:84–132,176–202,291–314`.

**Earlier point:** partly resolved, partly retained. The demand for a conventional discrete alternative is addressed. A requirement to justify Laplace as the baseline no longer applies. Its deeper concern about bounded inference still applies. The older additive finite-noise candidates can reveal the class at extreme flows; that is not the current alternative-arrival slot. Sources: `audit/alex_meeting_2026_10_21/BRIEF.md:144–153`; `audit/microstructure_search_2026_10_22/memos/SYNTHESIS.md:69–108`.

### W8. Fixed order size, one opportunity, and liquidity motives

**Attack:** “The trader chooses neither size nor timing. Would repeated trade reveal the class and destroy the result?”

**Spoken defence:** “The theorem covers one public opportunity and a unit order menu. This restriction gives a uniform information bound over every allowed deviation. Continuous size and repeated opportunities require further equilibrium analysis. The separate Laplace version supports the main comparison with continuous sizes, but matching posterior bounds does not make the two environments equivalent.”

**Likely follow-up:** “Why does the liquidity trader accept a loss?”

**Answer:** “Its motive lies outside acquisition information, and its order probabilities are exogenous. Those orders provide the cover that leaves a return to private information. The paper does not derive them from a one-period expected-profit objective.”

**Status:** **the paper supports this** restricted defence; no general repetition result is claimed.

**Sources:** `overleaf/slot/sections/02_model.tex:106–161`; `overleaf/slot/sections/05_research.tex:14–17`; `overleaf/slot/appendix/A8_empirical.tex:1–18`; `overleaf/slot/comparison.tex:96–132,181–185,291–314`.

**Earlier point:** still applies. The Ji Hee exchange asks about size, presence, and one opportunity: `discussion/2026-10-26/ji-hee-email.md:14–18`. Older statements about a Laplace net-demand interval should not become descriptions of the slot.

### W9. The example has a narrow window

**Attack:** “You place the top posterior almost exactly below the final threshold. How robust is this?”

**Spoken defence:** “The three-economy example has a small margin at the final exclusion condition. Strict inequalities establish an open set, not a large empirical region. The initial entry reversal needs fewer restrictions than the return to floor entry at that particular third strength. The general class result finds suitable strengths and costs; it does not preserve the same numbers for every class distribution.”

**Likely follow-up:** “Which margin is actually small?”

**Answer, benchmark use:** “The top belief is about 0.731059 and the final threshold about 0.731392. Their gap is about 0.000334, equivalent to a cost margin of about 0.002689. That is the final exclusion margin, not the strong economy's recruitment margin.”

**Status:** **the paper supports this**.

**Sources:** `overleaf/slot/sections/04_equilibrium_results.tex:110–118,181–224`; `overleaf/slot/appendix/A6_robustness.tex:159–203`; `overleaf/slot/appendix/A9_parameters.tex:64–67,271–286`; `overleaf/slot/numbers.tex:17–21,668–669,693–694,5274–5277`.

**Earlier point:** still applies. The exact Laplace derivative bound no longer applies, but the shared top-posterior constraint explains the same tight final margin. Source: `overleaf/slot/comparison.tex:187–202`.

### W10. Uniqueness, ties, and the apparent hump

**Attack:** “Your figure contains several equilibria. Did you select the branch that makes entry rise?”

**Spoken defence:** “The main comparison uses three economies where strict bounds force unique outcomes under the stated equilibrium definition. Intermediate strengths can admit informative and uninformative outcomes. Their branch diagram does not provide an equilibrium-selection rule. The rise between the first two comparison economies does not depend on such a rule.”

**Likely follow-up:** “Does unique really mean all equilibria?”

**Answer:** “It covers all mixtures over the permitted orders and all four stated pairs of trade and high-cost preparation tie rules. The definition still fixes truthful bids and zero-cost preparation. I should keep that scope explicit.”

**Status:** **the paper supports this**.

**Sources:** `overleaf/slot/sections/04_equilibrium_results.tex:11–49,323–349,379–424`; `overleaf/slot/appendix/A1_payoffs.tex:10–69`; `overleaf/slot/appendix/A4_coexistence.tex:1–54,379–451`.

**Earlier point:** old concerns about selecting full Laplace orders require the continuous-size proof. The current theorem has its own finite-menu proof. Neither proof implies uniqueness at every intermediate strength: `discussion/2026-10-26/alex-email.md:7–14`; `overleaf/slot/comparison.tex:176–225`.

### W11. Price-impact asymmetry is not a ready causal test

**Attack:** “You say the price impact reveals recruitment. Why could an asymmetric prior, other news, or deal selection not produce it?”

**Spoken defence:** “The exact identity assumes full informed orders and a prior below the preparation threshold within one public state. Frequency weights remove the class-information component under those assumptions. They do not remove arbitrary news or establish a causal effect in pooled transaction data. An empirical design must defend the timing, conditioning variables, and measurement of the zero outcome.”

**Likely follow-up:** “What does the algebra actually remove?”

**Answer:** “Bayes' rule makes the frequency-weighted upward and downward belief changes cancel. The remaining term is extra preparation after a purchase times its gain to target proceeds. With mixed orders, the no-order outcome can itself carry news and add another term.”

**Status:** **the paper supports this** identity; the causal-design warning is **new inference**.

Silent derivation, already in the paper: define \(w(\mu)=t_L-t_0+\Delta_T\mu\). Under full informed orders,

\[
\bar f(1)(M-\pi)=\bar f(-1)(\pi-m).
\]

With \(\pi<\tau\), entry after a sale and after no order is \(\rho\), so

\[
\bar f(1)I_+-\bar f(-1)I_-
=\bar f(1)[e(1)-\rho]w(M).
\]

**Sources:** `overleaf/slot/appendix/A8_empirical.tex:1–18,21–145,181–208`; `overleaf/slot/sections/08_empirical.tex:77–90`.

**Earlier point:** still applies, with a new slot-specific measurement issue. A scheduled call auction is a proposed empirical counterpart; many submitted orders do not literally form one alternative arrival. The exact identity needs an additional aggregation argument before it becomes an exact identity for that data. This last point is **new inference**, from the contrast between `sections/02_model.tex:106–134` and `sections/08_empirical.tex:81–86`.

### W12. Incumbent strength is not an observed premium

**Attack:** “Your strength variable is a distribution. What would I measure? A high initial offer can be a strategic deterrent.”

**Spoken defence:** “Strength is public information about the incumbent's value distribution before the rival's preparation decision. It is not the incumbent's realised value or a chosen preemptive offer. An observed premium can reflect that information, but it also reflects sale strategy and terms. I need a measurement argument before I use it as strength.”

**Likely follow-up:** “Do go-shops fit a paper with no announced bid?”

**Answer:** “They offer a public window with possible later preparation, which is useful. A signed price, match rights, and deal protection change the sale rule and information. I would treat them as an application that needs a bridge, not as an exact instance of the baseline.”

**Status:** **new inference** about empirical mapping, based on the paper's stated timing.

**Sources:** `overleaf/slot/sections/01_introduction.tex:11–15`; `overleaf/slot/sections/02_model.tex:30–38,93–102,163–170`; `overleaf/slot/sections/08_empirical.tex:77–90`; proposed application `audit/jmp_search_2026_10_30/ccc_seller_terms.md:85–118`.

**Earlier point:** the auction-entry distinction survives. The current talk already distinguishes Fishman's chosen preemptive bid from public distributional strength: `overleaf/slot/slides_script.md:55–63`.

### W13. The research extension has a cap and a private choice

**Attack:** “You make the research probability endogenous, but also remove liquidity orders and impose a cap. Is the monotonic result general?”

**Spoken defence:** “Research raises informed presence in the single opportunity, so it also reduces liquidity cover. The paper treats that substitution explicitly. At an even prior, research rises with the spread on the specified branch where a purchase recruits, until the cap. A unique intensity on that branch does not imply a unique equilibrium.”

**Likely follow-up:** “Why does the first-order condition omit the price derivative?”

**Answer:** “The research choice is private. A unilateral deviation changes success probability at the candidate price and entry schedules. Publicly observed research would require a different analysis.”

**Status:** **the paper supports this**.

**Sources:** `overleaf/slot/sections/05_research.tex:3–25,33–68,97–114`; `overleaf/slot/appendix/A5_research.tex:61–83,186–283,725–747`.

**Earlier point:** the research question now has a formal answer, but the unrestricted slogan in the earlier exchange is too broad. Source: `discussion/2026-10-26/ming-email.md:15`; current restrictions above.

### W14. Proceeds, social surplus, and the informed trader's gains

**Attack:** “Your traders profit at someone else's expense. Why call this welfare-improving?”

**Spoken defence:** “The welfare comparison holds strength fixed and gives the rival access to the price. At the strong comparison economy, access adds preparation with a positive expected net acquisition gain. It raises target proceeds, while informed trade occurs in both economies. Liquidity losses are transfers, and some individual shareholders can lose.”

**Likely follow-up:** “Is the identity that proceeds plus rival profit equal value your welfare proof?”

**Answer:** “No, that identity omits the incumbent's rent when it wins. The welfare proof uses allocation values and subtracts preparation costs. It is a comparison of price access, not a general welfare ranking of stronger and weaker incumbents.”

**Status:** **the paper supports this**.

**Sources:** `overleaf/slot/sections/07_welfare.tex:5–39`; `overleaf/slot/appendix/A7_welfare.tex:14–23,47–91`. The extension with endogenous research needs its stated cap conditions: `overleaf/slot/appendix/A5_research.tex:593–623`.

**Earlier point:** Alex's question about holders and outsiders still matters, and the current paper names an outsider with no initial net stake. Old numerical stake bounds belong to other order environments. Do not present them as slot robustness. Sources: `audit/alex_meeting_2026_10_21/BRIEF.md:155–159`; `overleaf/slot/sections/02_model.tex:106–134`; `audit/alex_meeting_2026_10_21/memos/SYNTHESIS.md:178–222`.

### W15. Is preparation really one sunk cost?

**Attack:** “Diligence has stages, finance arrives later, and a rival can stop. Why collapse all that into one cost?”

**Spoken defence:** “The paper studies the commitment to preparation that makes an executable proposal possible. One cost combines information acquisition and readiness to bid. That isolates the entry margin, but it does not describe staged diligence or optimal delay. Continuous cost distributions relax the cost law while retaining the stated support conditions.”

**Likely follow-up:** “Can preparation occur without a public bid?”

**Answer:** “Yes, preparation reveals value, and the rival may then have an inadmissible bid under the reserve extension. Even an admissible rival can lose. That is why preparation, sale completion, and two admissible bids appear as distinct outcomes.”

**Status:** **the paper supports this** restricted interpretation.

**Sources:** `overleaf/slot/sections/02_model.tex:11–19,83–102,221–227`; `overleaf/slot/sections/06_robustness.tex:9–23`; `overleaf/slot/sections/07_welfare.tex:64–112`.

**Earlier point:** still applies. Normalising a positive cost to one changes money units; it does not make a zero preparation cost equivalent to a positive cost. All values and costs must rescale together. Sources: `audit/alex_meeting_2026_10_21/BRIEF.md:161–162`; `overleaf/slot/sections/02_model.tex:79–91`.

### W16. Two classes and one rival seem too special

**Attack:** “Real sales contain many potential rivals and overlapping values. Does your result survive any of that?”

**Spoken defence:** “The two classes can contain dispersed and overlapping value distributions, subject to the ranking and reserve conditions. The paper also gives a many-class result under separation. It does not establish the same price sufficiency for arbitrary posterior vectors or a general contest with many potential rivals. The current result isolates how one rival's entry responds.”

**Likely follow-up:** “Does every distribution give your reversal at the same costs?”

**Answer:** “No. For each ranked pair and prior, the construction chooses suitable incumbent strengths and costs. That is an existence result across environments, not invariance of the benchmark calibration.”

**Status:** **the paper supports this**.

**Sources:** `overleaf/slot/sections/02_model.tex:58–75`; `overleaf/slot/sections/06_robustness.tex:27–54`; `overleaf/slot/appendix/A6_robustness.tex:159–203,246–388`.

**Earlier point:** Alex's distribution-class request is addressed in the current paper. A rival's active choice of its own integration plan is a distinct question, not what the class extension proves. Sources: `audit/alex_meeting_2026_10_21/BRIEF.md:133–142,168–182`; `discussion/2026-10-26/alex-email.md:7–14`.

### W17. The thesis and job-market plan are not settled by this theorem

**Attack:** “Is this your job-market paper? What will the rest of the thesis contain, and what can you finish?”

**Spoken defence:** “This is my developed theory chapter on how public prices can affect a sale. My proposed empirical chapter studies what private sale processes reveal to markets and how that affects later competition. I will choose the job-market paper after the data pilot and novelty assessment. I will also agree clear boundaries with the joint projects.”

**Likely follow-up:** “What are the next concrete milestones?”

**Answer:** “First, resolve seller choice in the current framework and audit the availability of dated preparation records. Second, produce a pilot on private process events and market responses. By the proposed March decision date, choose the main empirical question using evidence and access constraints.”

**Status:** **new inference**: a proposed oral plan, not a report of commitments Austin already made.

**Sources:** `overleaf/slot/sections/09_conclusion.tex:30–35`; `audit/jmp_search_2026_10_30/MEMO.md:5–20,24–30,114–134,180–200`; `audit/jmp_search_2026_10_30/ccc_seller_terms.md:131–155`.

**Earlier point:** the planning memo places CCC as a second paper and proposes a private-process project as the job-market candidate. Treat this as a plan. Its paragraphs headed “The new fact” describe hoped-for findings, not demonstrated results (`MEMO.md:67–75,140–148`). Do not promise journal outcomes or claim a measured response that no pilot established. An empirical chapter on private bidder exits remains a candidate, not a completed third chapter (`MEMO.md:136–157`).

## 4. Errors to fix first

These are proposed replacements. No talk or paper source is changed here. Items 1–7 should be resolved before daily drills make the present wording habitual.

### 1. Remove the implication that the seller necessarily needs discovery

**Location:** `overleaf/slot/slides_script.md:49`: “The seller needs discovery …”

**Problem:** this implies a seller objective or need that the fixed-rule theorem does not establish. The high-price calculation provides a direct counterexample to that broad interpretation.

**Exact replacement:** “The seller's proceeds can depend on rival preparation. The rival needs a reason to pay, and the market can supply news before commitment.”

Support: `overleaf/slot/sections/07_welfare.tex:5–39,64–112`; `overleaf/slot/appendix/A7_welfare.tex:237–239`; W1 above.

### 2. Correct the market-structure attribution

**Location:** `overleaf/slot/slides_script.md:69`.

**Exact replacement:** “Dow, Goldstein and Guembel are the closest antecedent for information production. The alternative arrival comes from Dow and Gorton. The unit menu, presence probability, and order cost follow Edmans, Goldstein and Jiang's 2015 paper.”

Keep the distinct 2012 takeover reference separate at `slides_script.md:73`.

Support: `overleaf/slot/sections/01_introduction.tex:127–137`; `overleaf/slot/sections/02_model.tex:148–161`. The older literature advice at `audit/talk_style_2026_10_28/15_literature_contribution.md:9–15,30–33` needs the same attribution refinement.

### 3. State that research is private

**Locations:** `overleaf/slot/slides.tex:585`; `overleaf/slot/slides_script.md:271`. Both omit a material assumption.

**Exact added wording:** “The research choice is private. Market makers and the rival use its equilibrium level.”

Support: `overleaf/slot/sections/05_research.tex:19–25`; `overleaf/slot/appendix/A5_research.tex:61–83`. This omission also appears in the study guide's review, `audit/study_guide_gptpro_2026_10_30/competition_study_guide.tex:3187–3197`.

### 4. Repair the research coexistence interval

**Location:** `overleaf/slot/slides.tex:1339`: “Zero research coexists on \([r_0,r_N]\).”

**Exact replacement:** “Zero research is an equilibrium on \([r_0,r_N]\). It coexists with research that recruits on \([r_R,r_N]\). At \(r_1\) and \(r_2\), the unique outcome has research at the cap and matches the main three-economy result.”

Support: `overleaf/slot/appendix/A5_research.tex:725–747`; `overleaf/slot/sections/05_research.tex:97–114,160–164`. The distinction is existence versus coexistence, not just an endpoint convention.

### 5. Do not deny value knowledge in the point-value example

**Locations:** `overleaf/slot/slides_script.md:127,327`; related backup `overleaf/slot/slides.tex:908`.

**Exact replacement for the information sentence:** “The informed trader sees the synergy class. In general, that class specifies a distribution of the rival's value. In the point-value example, class knowledge also determines the value.”

The paper's own introductory phrase “though not of its value” needs the same qualification if used orally (`sections/02_model.tex:24–25`).

Support: `overleaf/slot/sections/02_model.tex:58–75`; `overleaf/slot/sections/04_equilibrium_results.tex:89–90`.

### 6. Keep conditions in the close

**Locations:** `overleaf/slot/slides_script.md:317–319`; `overleaf/slot/slides.tex:692,696`.

**Exact replacement for the research sentence:** “At an even prior, research rises with the spread until the cap on the branch where a purchase recruits.”

**Exact replacement for the implications sentence:** “Under the main result's conditions, price access raises expected target proceeds and net acquisition surplus at the strong incumbent. With full informed orders and the prior below the preparation threshold, weighted purchase impact exceeds weighted sale impact exactly when a purchase recruits.”

For the slide, replace “In data, recruitment sits in the frequency-weighted purchase impact” with: “Prediction under full informed orders and \(\pi<\tau\): weighted purchase impact exceeds weighted sale impact exactly when a purchase recruits.”

Support: `overleaf/slot/sections/05_research.tex:47–68`; `overleaf/slot/sections/07_welfare.tex:5–18`; `overleaf/slot/sections/08_empirical.tex:19–35`.

### 7. The planned speech exceeds the requested duration

**Locations:** `overleaf/slot/slides_script.md:3,27,269,283,295,311`.

The current schedule allocates 33.5 minutes to prepared speech. The brief asks for 30 minutes. The existing word count is 3,523, but the time problem concerns the planned explanation and pauses, not words alone.

**Exact replacement for the timing contract:** “Prepared speech: 28 minutes, including the title and close. Keep two minutes within the 30-minute talk for pauses and brief clarifications. Detailed research, welfare algebra, and equilibrium branches remain available for questions.”

**Proposed time budget, not an existing source fact:** title and frames 1–4, five minutes; frames 5–9, seven; frames 10–13, eight; frames 14–15, four; frames 16–18, three; close, one. Total: 28 minutes. Use one sentence each for the research and welfare results in the short route. Retain the full-information control and the main proof idea. A timed rehearsal must confirm this plan; a new header alone does not shorten the speech.

Earlier faculty guidance also asked for about 30 minutes within a longer slot: `audit/talk_style_2026_10_28/00_synthesis.md:3–5,43–72`.

### 8. Repair the endpoint language

**Location:** `overleaf/slot/slides.tex:801`.

**Exact replacement:** “The uninformative market exists through \(r_N\) and disappears above it. On the branch that recruits, entry remains high through \(r_C\) and returns to its floor above it.”

This uses the default rule that an indifferent high-cost rival prepares. Under the flexible rule, the ceiling itself admits intermediate entry.

Support: `overleaf/slot/sections/04_equilibrium_results.tex:379–424`; `overleaf/slot/appendix/A8_empirical.tex:261–275,551–573`.

### 9. Restore the reserve condition in a standalone robustness answer

**Location:** `overleaf/slot/slides.tex:1054`, where the class ranking is abbreviated by dominance alone.

**Exact replacement:** “Assume \(G_H(y)\le G_L(y)\) for every \(y\), and both class supports meet the reserve. Under these conditions, the target-payoff spread weakly rises with incumbent strength.”

Support: `overleaf/slot/sections/02_model.tex:58–75`; `overleaf/slot/sections/03_competition_information.tex:25–57`.

### 10. Avoid a universal claim about additive liquidity flow

**Location:** `overleaf/slot/slides.tex:1506`: “Additive liquidity flow also keeps every size on path.”

**Exact replacement:** “Full-support additive liquidity flow gives every observed flow positive density. Continuous order sizes require a separate analysis of all size deviations.”

Support: `overleaf/slot/sections/02_model.tex:148–161`; `overleaf/slot/comparison.tex:96–132,291–314`. Bounded additive noise does not justify the original broad wording.

### 11. Replace the opaque phrase about point masses

**Location:** `overleaf/slot/slides.tex:926`: “Point-mass synergy values are not the kind case.”

**Exact replacement:** “Point-mass synergy values are not essential. Ranked classes with dispersed values also admit a reversal at suitable strengths and costs.”

Support: `overleaf/slot/sections/06_robustness.tex:27–43`; `overleaf/slot/appendix/A6_robustness.tex:159–203`.

### 12. Make the posterior-band explanation speakable

**Location:** `overleaf/slot/slides_script.md:183–195`, the spoken definitions of the likelihood ratio and posterior bounds.

**Exact replacement for the central explanation:** “A liquidity order can copy either informed order. This limits how far one order can move the odds of the high synergy class. The bounds apply to every allowed strategy, so the informed trader retains some information advantage even after market makers see the order.”

Keep the formulas on the slide and define the lower and upper beliefs by pointing to them. Do not recite each fraction unless asked.

Support: `overleaf/slot/sections/02_model.tex:136–161`; `overleaf/slot/appendix/A2_beliefs_trading.tex:1–120`.

### 13. A paper statement needs repair before it supports a reserve defence

**Location:** `overleaf/slot/appendix/A7_welfare.tex:161–163`.

The reserve proposition permits values below the reserve, then retains “the class ranking.” Its baseline definition includes no values below the reserve. This is a formal statement inconsistency, not a failure of the displayed reserve arithmetic.

**Exact replacement for the first two sentences:** “Fix a reserve and allow class values below it. Retain \(G_H(y)\le G_L(y)\) for every \(y\), the costs, the slot, and a strengthening \(F_1\le F_0\). Compute each class object at the stated reserve.”

Support: baseline definition `overleaf/slot/sections/02_model.tex:58–75`; intended kernel and proof `overleaf/slot/appendix/A7_welfare.tex:145–190`. The same inconsistency is identified in `audit/study_guide_gptpro_2026_10_30/competition_study_guide.tex:3171–3185`.

Do not memorise a reserve defence that claims the baseline admissibility assumption remains true after the reserve excludes the low class.

### 14. Separate sufficient reserve examples from necessary conditions

**Locations:** `overleaf/slot/slides.tex:868,881–882`.

The first shorthand makes flat entry sound automatic once both prices are informative. The second makes one displayed reserve sound necessary for strict deterrence.

**Exact replacement for the first statement:** “If full informed orders occur and only a purchase recruits at both strengths, entry is flat.”

**Exact replacement for the second statement:** “The displayed higher reserve gives strict deterrence. In this example, a reserve that excludes the low class must also exceed the weak incumbent's support for strict deterrence.”

**Benchmark use, for questions only:** the paper gives the strict interval \(1.325270<p<1.792723\). The displayed \(p=1.55\) lies inside it; it is not the only reserve that works.

Support: `overleaf/slot/appendix/A7_welfare.tex:161–190,212–239`; `overleaf/slot/numbers.tex:3191,3462,5252`.

## 5. Leave out

1. **The full numerical registry.** Keep only the entry sequence, the narrow final margin, and the high-price counterexample on demand. The example illustrates conditions; it does not estimate economic magnitudes. Sources: `overleaf/slot/appendix/A9_parameters.tex:3–6,64–67,271–286`.

2. **The complete sequence of strength cutoffs.** Recall the economic boundaries: informed trade begins, uninformative trade disappears, recruitment ends. Look up the intermediate thresholds and endpoint tables. They matter for a technical follow-up, but displace the mechanism in daily practice. Source: `overleaf/slot/sections/04_equilibrium_results.tex:323–424`.

3. **Old Laplace numbers and old additive-noise equilibria.** Keep their economic lessons and source distinctions. Do not memorise their ownership values, partial-sale sizes, or off-path completions as slot answers. Source: `overleaf/slot/comparison.tex:176–225,291–314`.

4. **A list of every cited paper.** Recall four roles: deterrence, information production, alternative arrival, and the finite menu. Keep the 2012 and 2015 Edmans, Goldstein and Jiang papers distinct. A citation list cannot substitute for the new auction mechanism. Sources: `overleaf/slot/sections/01_introduction.tex:127–161`; `overleaf/slot/sections/02_model.tex:148–161`.

5. **Exact research roots and polynomial certificates.** Recall the private-choice objective, the branch conditions, and the cap. Derive the first-order condition when needed. Detailed endpoint arithmetic belongs in the appendix. Sources: `overleaf/slot/appendix/A5_research.tex:61–83,186–283,725–747`.

6. **Claims of universal robustness.** Avoid cards headed “any costs,” “any distributions,” or “the rival can know more” without their restrictions. Use one card per economic assumption and one sentence on what remains open. Sources: `overleaf/slot/sections/06_robustness.tex:9–82`.

7. **An optimal seller story that is still a proposal.** Do not turn limited commitment, target certification costs, or a particular legal duty into an established defence. The current paper fixes sale terms and names seller choice as future work. Sources: `overleaf/slot/sections/02_model.tex:93–102`; `overleaf/slot/sections/09_conclusion.tex:30–35`; `audit/jmp_search_2026_10_30/ccc_seller_terms.md:66–83,161–173`.

8. **Prevalence percentages from keyword searches.** A filing count is not a transaction count, and neither establishes the chronology that the theorem requires. The first empirical deliverable should supply that denominator. Sources: `audit/jmp_search_2026_10_30/ccc_seller_terms.md:93–101,124–129`; `overleaf/slot/sections/08_empirical.tex:77–90`.

9. **Speculative thesis results and journal promises.** Prepare a coherent research question, the next deliverable, the main risk, and a decision date. The planning memo's desired facts remain proposals. Source: `audit/jmp_search_2026_10_30/MEMO.md:67–75,114–134,140–157,180–200`.

10. **The entire talk as a verbatim card deck.** Cards should permit Austin to restart the argument from any economic cue. Use the short opening and close for verbal consistency. For the body, alternate the words, the algebra, and the strongest objection.
