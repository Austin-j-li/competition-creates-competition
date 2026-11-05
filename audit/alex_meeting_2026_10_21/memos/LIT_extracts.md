# Verified literature extracts

Date: 21 October 2026. Scope: the four supervisor points in the shared brief.

## 1. Question and reading

This memo records source specifications. It does not derive a replacement model.
Priority follows the retrieval brief. Each entry states the version actually read.
A search excerpt does not verify a model detail.

## 2. Formal setup

The notation below follows each source. It need not match the current paper.
“Verified” means that the cited passage was read in the full text.
“Partial” means that some requested fields remain unverified.
“Open” marks an unresolved source question. It does not mean that the source omits the feature.

## 3. Results: source extracts

The entries below separate source facts from any interpretation.

### A1. Edmans, Goldstein, and Jiang (2015) — initial stake

**Citation.** Alex Edmans, Itay Goldstein, and Wei Jiang. “Feedback Effects, Asymmetric Trading, and the Limits to Arbitrage.” *American Economic Review* 105(12), 3766–3797.

**Version read.** [Published article, Columbia copy](https://business.columbia.edu/sites/default/files-efs/pubfiles/6040/Jiang_Feedback_effects.pdf). Relevant passage: Section II.E, pp. 3787–3788, “Zero Initial Position.” This is the published counterpart of the requested Section 3.5. [Journal record](https://www.aeaweb.org/articles?id=10.1257/aer.20141271).

**Status: partial.** The published stake discussion is verified. Appendix B.2 is not yet verified.

1. The extension gives the speculator an initial stake $\alpha>0$. A sale of one share leaves $\alpha-1$ shares. A purchase leaves $\alpha+1$ shares.
2. Correct disinvestment raises the stake value in state $L$. Correct investment raises it in state $H$. The source says these stake incentives are symmetric.
3. The source retains a positive cost interval with a buy/not-sell equilibrium and no sell/not-buy equilibrium. It reports no converse interval.
4. The reported difference between the two cost thresholds is $\frac{4x}{3}\frac{1-\lambda}{2-\lambda}$. It does not depend on $\alpha$.
5. Short quote, p. 3788: “the asymmetry between buying on good news and selling on bad news remains”.
6. The same section distinguishes corrective actions from amplifying actions. The stake result belongs to the corrective-action model. It is not a theorem about all price feedback.

**Requested fields outside this extract.** The coordinator covers the baseline model. This entry does not replace that review. Appendix B.2 must verify the payoff formula, restrictions on $\alpha$, and all stake thresholds.

**Access issue.** The journal's [Supplemental Appendix link](https://www.aeaweb.org/articles/materials/4583) returned a connection refusal. The author's [link labelled web appendix](https://alexedmans.com/wp-content/uploads/2021/04/LTAAppendix.pdf) displayed a 33-page main manuscript. It contains references to B.2, but no B.2 text. The old London faculty URL redirects to a faculty index.

### A2. Goldstein and Guembel (2008)

**Citation.** Itay Goldstein and Alexander Guembel. “Manipulation and the Allocational Role of Prices.” *Review of Economic Studies* 75(1), 133–164.

**Version read.** Published article, [author-hosted copy](https://www.dropbox.com/scl/fi/5gr4si7275exrabrjixpr/manipulation-published.pdf?rlkey=h12py9cnhgqtkm3k5sixos4bp&dl=0). The author’s [Wharton page](https://fnce.wharton.upenn.edu/profile/itayg/) identifies this copy. The inline viewer supplied the full text, including the appendix.

**Status: verified for the requested model fields.** These are source facts. No new analytical result is claimed.

1. **States and decision.** Section 2.1, pp. 136–137, equations (1)–(2): $\omega\in\{l,h\}$, each with probability $1/2$. The manager chooses $k\in\{0,K\}$. Values are $V(h,K)=V^+>0$, $V(l,K)=V^-<0$, and $V(\omega,0)=0$. The firm uses retained earnings. Assets in place are omitted; footnote 7 says their inclusion does not affect the analysis.
2. **Information.** Section 2.2, p. 137: one speculator is present. With probability $\alpha$, he observes the state perfectly. Otherwise his signal is $\varnothing$. This is uncertainty about his information, rather than his presence. In the feedback model, the manager has no private signal. Equation (3) assumes $\bar V=(V^++V^-)/2>0$.
3. **Orders and noise.** Section 2.2: two trade dates. At each date, $u_t\in\{-1,0,1\}$. Noise $n_t\in\{-1,0,1\}$ has probability $1/3$ on each point. The two noise orders are independent. Orders are simultaneous market orders. Short sales are allowed. The baseline imposes no extra sale cost or inventory constraint.
4. **Information sets and prices.** The market maker observes $Q_t=u_t+n_t$. He sets $p_1(Q_1)=E[V\mid Q_1]$ and $p_2(Q_1,Q_2)=E[V\mid Q_1,Q_2]$. The manager observes both flows. The speculator’s second order can depend on $s,Q_1,u_1$. Section 2.2 expressly substitutes flow observation for price observation to ease exposition.
5. **Stake and objective.** Section 4.2, pp. 142–143, expressly states a zero initial position. The appendix proof of Proposition 2 distinguishes continuation profit from the second transaction’s profit. After two purchases, total profit is $2V-p_1-p_2$. The first position therefore matters at the second date.
6. **Equilibrium.** Section 2.2, pp. 137–138: Perfect Bayesian Nash Equilibrium, with optimal orders, optimal investment, competitive prices, Bayes’ rule, and correct strategy beliefs. Mixed strategies are allowed. Section 3 says some parameter values have no pure equilibrium.
7. **Constructed manipulation equilibrium.** Proposition 2 and Section 4.1, equations (5)–(11), pp. 140–141: the informed high type buys first. The low and uninformed types use the same sale probability $1-\mu$. The source gives $0\leq\mu<(1-\alpha)/(3-\alpha)$. A sufficient condition is equation (4): $(\alpha/2)V^-+(1-\alpha)\bar V<0$.
8. **Revelation.** In this equilibrium, $Q_1=2$ reveals the high signal. Flows $Q_1=-2,-1$ identify a pool of low and uninformed speculators. They do not identify the low state. The manager rejects the project there. Conditional on $Q_1=0,1$, he rejects after $Q_2=-2,-1$. All other paths lead to investment. See Section 4.1, pp. 141–142.
9. **Off-path beliefs.** Footnote 12, p. 141: indifferent types mix over all three second-date actions with positive probability. All second-date flows then occur. Short quote: “does not depend on any assumptions about off-the-path beliefs.” This statement concerns the constructed equilibrium.
10. **Multiplicity.** Section 3 expressly allows multiple equilibria. Proposition 2 proves existence of manipulation, not uniqueness. Section 5, Proposition 3, p. 147, adds the Intuitive Criterion. For sufficiently small positive $\bar V$, every equilibrium then has first-date sales by the uninformed type. The source does not generally exclude equilibria without manipulation at intermediate feedback strength.
11. **Initial ownership caveat.** Section 4.2, p. 143, says a long stake suffers from the wrong investment decision. It does not establish that its zero-stake manipulation result survives a positive stake.

**Implication for the brief.** This source supports a discrete noise menu. Its two-date manipulation mechanism cannot be copied into a one-date model without a new argument.

### A3. Dow, Goldstein, and Guembel (2017)

**Citation.** James Dow, Itay Goldstein, and Alexander Guembel. “Incentives for Information Production in Markets where Prices Affect Real Investment.” *Journal of the European Economic Association* 15(4), 877–909. DOI: 10.1093/jeea/jvw023.

**Version read.** [Published article, author-hosted copy](https://www.dropbox.com/scl/fi/n16t80i2wi3om8zlanjp3/informationproduction-published.pdf?rlkey=rm623i5vped0m9f5liyos6nui&dl=0), linked on the [Wharton author page](https://fnce.wharton.upenn.edu/profile/itayg/). The inline viewer supplied the complete 33-page article.

**Status: verified for the requested model fields.** Source facts follow. Write $a$ for the source’s signal accuracy.

1. **States and claim.** Section 2, p. 880: $\omega\in\{l,h\}$, each with probability $1/2$. The firm chooses $A\in\{0,1\}$. The safe choice pays $V_0$. The risky choice pays $V_\omega$, with $V_h>V_0>V_l$. Shares pay their proportional part of the selected project. No other security pays a state-contingent payoff. Thus information ceases to affect the claim when the safe project is selected.
2. **Information.** Section 2, pp. 880–881: a unit mass of risk-neutral speculators can each pay $c>0$ for a binary signal. Its accuracy is $a>1/2$. Signals are independent across speculators conditional on the state. The endogenous informed mass is $\alpha$. The manager has no state signal and observes the share price.
3. **Orders.** Each speculator can choose $x_i\in[-1,1]$. Short sales are allowed up to one unit. An informed speculator buys one unit after a high signal and sells one after a low signal. Each speculator is too small to affect price. Uninformed speculators do not trade; see footnote 3 and Lemma 2. The baseline has an information cost, rather than a per-order cost. No initial stake term appears in this specification.
4. **Noise and observation.** Section 2, p. 881, equation (1): $n\sim N(0,\sigma^2)$ and $X=n+\int_0^\alpha x_i\,di$. The market maker sees only $X$. Conditional aggregate informed orders are $\pm\alpha(2a-1)$. Normal noise has support $\mathbb R$.
5. **Posterior.** Section 3.1, p. 882, equation (2):

   $$\Pr(h\mid X;\alpha)=\frac{\varphi(X-\alpha(2a-1))}{\varphi(X-\alpha(2a-1))+\varphi(X+\alpha(2a-1))}.$$

   Here $\varphi$ denotes the $N(0,\sigma^2)$ density. For $\alpha>0$, no finite flow fully reveals the state.
6. **Investment and price.** Equations (3)–(7), pp. 882–883: invest in the risky project when its posterior expected payoff exceeds $V_0$. The cutoff $\bar X(\alpha)$ solves equality. The selected price equals the posterior risky payoff above that cutoff. It equals $V_0$ at or below it. The firm selects the risky project iff $P(X)>V_0$.
7. **Price pooling and selection.** Lemma 1 and the next discussion, p. 883: many flows share price $V_0$. There are other continuation equilibria. If the safe project is optimal at the prior, one can have $P(X)=V_0$ for every flow. The authors select Lemma 1’s equilibrium because only it survives direct flow observation by the firm. Short quote: “the firm can observe order flow directly.” This is an explicit selection argument, not a price-sufficiency theorem.
8. **Information equilibrium.** Section 3.3, p. 884, equations (10)–(12): an interior informed mass satisfies $\Pi(\widehat\alpha)=c$. The no-information corner requires $\Pi(0)<c$. The full-information corner requires $\Pi(1)\geq c$. The authors focus on equilibria stable under small changes in informed mass. An interior stable solution requires a downward slope of $\Pi$ at the solution.
9. **Uniqueness and multiplicity.** Section 3.4, Propositions 1–2, p. 885: the selected model has a unique information equilibrium if the risky project is optimal at the prior. If the safe project is optimal, a no-information equilibrium always exists. Additional positive-information equilibria can coexist when $c\leq\Pi_{\max}$. Section 3.4.3 distinguishes stable and unstable branches. It does not claim unconditional uniqueness of the entire price-feedback game.
10. **Off-path issue.** Full-support normal noise leaves no impossible finite flow. The main unresolved coordination issue concerns price rules and project choice. The source uses the continuation selection above, rather than a stated D1 or Intuitive Criterion refinement there.

**Correction to the brief.** The published outlet is JEEA, not JFQA. This paper uses continuous bounded orders and normal noise. It is not an example of discrete trade.

### A4. Kyle and Vila (1991)

**Citation.** Albert S. Kyle and Jean-Luc Vila. “Noise Trading and Takeovers.” *RAND Journal of Economics* 22(1), 54–71. DOI: 10.2307/2601007.

**Version reached.** [JSTOR journal record and abstract](https://www.jstor.org/stable/2601007); [ProQuest preview](https://www.proquest.com/openview/8657f899a9845295555489bbcd7dccf0/1.pdf?pq-origsite=gscholar&cbl=47440); [RePEc record](https://ideas.repec.org/a/rje/randje/v22y1991ispringp54-71.html).

**Status: no full-text verification.** JSTOR required a login for the full text. ProQuest supplied a short preview. A search for the working paper and the five Scholar versions found no accessible full text. No login was attempted.

The abstract verifies only the broad mechanism: noise lets an outside acquirer conceal share purchases before a takeover. It says neither dilution nor a large incumbent stake is necessary. This does not verify any specific noise law, order menu, initial acquirer stake, takeover cost, or equilibrium refinement. Those fields remain **open**. Do not cite this entry for model details.

### A5. Khanna and Sonti (2004)

**Citation.** Naveen Khanna and Ramana Sonti. “Value Creating Stock Manipulation: Feedback Effect of Stock Prices on Firm Value.” *Journal of Financial Markets* 7(3), 237–270. DOI: 10.1016/j.finmar.2003.11.004.

**Version reached.** [ISB repository record and abstract](https://eprints.exchange.isb.edu/id/eprint/1064/). The record expressly says that full text is unavailable. The [publisher page](https://www.sciencedirect.com/science/article/pii/S1386418103000454) and [SSRN working-paper page](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=199454) returned access challenges. Scholar’s seven versions supplied no accessible full-text alternative.

**Status: no full-text verification.** The abstract states that manipulation can raise firm value when a trader retains stock inventory. It does not verify the inventory size, signal distribution, order menu, noise probabilities, or refinement. These fields remain **open**.

**Correction to the retrieval brief.** This paper appeared in *Journal of Financial Markets*, not *Journal of Financial Intermediation*. The institutional record verifies that correction.

### A6. Edmans (2009)

**Citation.** Alex Edmans. “Blockholder Trading, Market Efficiency, and Managerial Myopia.” *Journal of Finance* 64(6), 2481–2513.

**Version read.** [Published article on the author’s website](https://alexedmans.com/wp-content/uploads/2024/06/Blockholders.pdf), including the printed appendix. The separate Internet Appendix was not read.

**Status: verified for the core model.** The Internet Appendix extensions remain unverified.

1. **States and public news.** Section I, pp. 2487–2488: one share exists. A blockholder owns $\alpha$ shares; atomistic shareholders own $1-\alpha$. A good public signal establishes $V=X>0$. After a bad public signal, $V\in\{0,X\}$ with equal probabilities. The market analysis conditions on this bad signal.
2. **Private information.** The blockholder selects effort $\mu\in[0,1]$ at cost $c\mu^2/2$. Her binary signal has accuracy $(1+\mu)/2$. Equation (1) gives posteriors $(1+\mu)/2$ and $\pi_b=(1-\mu)/2$. She is always present. The source assumes $X\leq8c$ for the stated interior effort solution.
3. **Orders and ownership.** Section I and footnote 8: she holds after good private news and sells $\beta\leq\alpha$ after bad private news. Her demand is $b=0$ or $b=-\beta$. The sale size is endogenous. The baseline prohibits short sales. It has no separate fixed trade cost. Its stake therefore restricts the amount she can sell.
4. **Noise.** Section I, pp. 2488–2489:

   $$f(u)=\begin{cases}\lambda e^{-\lambda u},&u>0,\\0,&u\leq0,\end{cases}\qquad \lambda=\frac{1}{\nu(1-\alpha)},\quad\nu\leq1.$$

   Noise demand is one-sided exponential. It is not Laplace. The source links mean noise volume to free float. It also discusses a downward shift of the distribution.
5. **Observation and price.** The competitive market maker observes public news and $d=b+u$. Lemma 1, equations (2)–(3), pp. 2489–2490, gives

   $$P(d)=\begin{cases}\pi_bX,&d\leq0,\\\pi_mX,&d>0,\end{cases}\quad
   \pi_m=\frac{1+e^{-\lambda\beta}+\mu(1-e^{-\lambda\beta})}{2(1+e^{-\lambda\beta})}.$$

   A nonpositive flow reveals the bad private signal, not the state, unless $\mu=1$. Positive flows pool sale and hold orders. The exponential law makes price constant on the positive-flow region.
6. **Equilibrium and solution.** Section I.A calls the solution a Nash equilibrium with optimal effort and trade and zero expected market-maker profit. Equations (4)–(5) give $\mu=\beta X/(4c)$ and $\beta=\min\{1/\lambda,\alpha\}$. The appendix proof of Lemma 1, pp. 2505–2506, holds conjectured effort and sale size fixed before it imposes consistency. No D1 or Intuitive Criterion restriction is stated in that characterization. Do not cite it for a general uniqueness theorem outside its specified strategy structure.
7. **Economic decision.** Section II, pp. 2493–2494: the manager selects long-term investment before the public signal and trade. His objective weights interim price by $\omega$ and final value by $1-\omega$. Equations (10)–(11) describe that choice. He does not make a post-price entry decision. Thus this is governance through price incentives, not the same timing as the current takeover model.
8. **Why exponential noise?** Section I, p. 2489, states its technical role: it permits an endogenous sale size in closed form with binary firm value. Short quote: “allows her trade to be endogenously derived as a function of block size.” The same passage says the broad block-size mechanism does not depend on that functional form.

**Implication for the brief.** This is a direct source for sell-only trade, a positive initial stake, and an explicit tractability defense of nonnormal noise. It does not supply a Laplace-noise precedent.

### A7. Boleslavsky, Kelly, and Taylor (2017)

**Citation.** Raphael Boleslavsky, David L. Kelly, and Curtis R. Taylor. “Selloffs, Bailouts, and Feedback: Can Asset Markets Inform Policy?” *Journal of Economic Theory* 169, 294–343.

**Version read.** [Author manuscript dated 1 February 2017](https://static1.squarespace.com/static/5271497de4b03475d0dd1240/t/589f5b3bd482e9cad933994f/1486838588850/Jet_Final.pdf), linked from the [author’s publication list](https://ralphboleslavsky.squarespace.com/research). The publisher’s accepted-manuscript URL returned 404. Page numbers below refer to the author manuscript.

**Status: verified for the baseline and the price-only extension.** This source uses continuous orders, not a discrete menu.

1. **States and presence.** Section 3, pp. 7–8: $\omega=0$ with prior $q$ and $\omega=1$ with prior $1-q$. One trader is informed with probability $a$ and a noise trader otherwise. These are alternative trader identities. There is no additive noise order alongside an informed order. The informed trader sees the state perfectly.
2. **Claim and action.** An Arrow security pays the terminal state. The authority can pay $c$ to change the state to one with certainty. The baseline assumes $q<c<1$. Thus the authority does not intervene at the prior. The trader has no initial stake term in equations (2)–(3).
3. **Order set.** The trader selects $t\in\mathbb R$. Positive $t$ denotes a sale. Purchases and short sales have no quantity bound. There is no per-order trade cost. Lemma 3.1 excludes weakly dominated wrong-direction trades from the equilibria studied. The bad informed type sells; the good informed type buys. Mixed distributions may initially contain atoms.
4. **Noise.** Section 3, p. 8: the noise trader sells with probability $s\in(0,1)$ and buys with probability $1-s$. Conditional densities $f_s$ and $f_b$ have full support on $[0,\infty)$ and $(-\infty,0]$. They are continuously differentiable on their respective sides and have finite first moments. No named normal, Laplace, or exponential law is imposed.
5. **Observation.** In the baseline, the order is public. Both the market maker and authority see $t$. The authority acts after the trade. Section 6 separately removes the authority’s access to the order.
6. **Price and profits.** Section 3, p. 9, equations (1)–(3), with $\chi(t)=\Pr(\omega=0\mid t)$ and intervention probability $\alpha(t)$:

   $$p(t)=1-\chi(t)+\alpha(t)\chi(t),$$
   $$u_0(t)=t(1-\chi(t))(1-\alpha(t)),\qquad
   u_1(t)=-t\chi(t)(1-\alpha(t)).$$

   Equation (4) gives intervention probability zero if $\chi<c$, one if $\chi>c$, and any probability at equality.
7. **Revelation and beliefs.** Section 3, equations (5)–(6), pp. 10–11: an informed atom at a positive order reveals the bad state. An informed atom at a negative order reveals the good state. Lemma A.2 excludes atoms and gaps in the positive-profit equilibrium. Full-support noise keeps finite continuous orders possible under either state. No D1 or Intuitive Criterion refinement appears in the stated PBE definition.
8. **Equilibrium concept.** Section 3, p. 9: Perfect Bayesian equilibrium, sequentially rational orders and intervention, with Bayes-consistent beliefs. The authors focus on the weak-dominance restriction above.
9. **Multiplicity and uniqueness.** Section 5, Propositions 5.1–5.2, pp. 14–15: define $\widehat\chi=q[a+(1-a)s]/[qa+(1-a)s]$. If $c\leq\widehat\chi$, multiple equilibria exist and the bad type earns zero. If $c>\widehat\chi$, the positive-profit equilibrium is unique within the stated restriction. Its bad-type order distribution has support $[m_0^\dagger,\infty)$. The authority never intervenes for $t<Jm_0^\dagger$, where $J=(1-q)/(1-c)$. Above that point it intervenes with probability $1-Jm_0^\dagger/t$. Its posterior is then constant at $c$. Equation (10) pins down $m_0^\dagger$ through a unique normalization root.
10. **Price-only extension.** Section 6, Proposition 6.1, pp. 18–20, equation (11): the authority observes only price. For $c\in(\widehat\chi,1)$, the unique equilibrium has random prices in the large-sale region. The market maker selects $p=1$ with probability $1-Jm_0^\dagger/t$ and $p=1-c$ otherwise. The authority intervenes exactly at price one. Both prices imply the same posterior $c$. The source claims posterior transmission, not recovery of the exact large order.
11. **Short quote.** Section 6, p. 19: “no equilibrium exists in which the market maker uses a deterministic pricing function for all sell orders.”

**Correction to the retrieval brief.** The outlet is JET, not JFE. This model also warns against treating price observation and order observation as automatically equivalent.

### B8. Levin and Smith (1994)

**Citation.** Dan Levin and James L. Smith. “Equilibrium in Auctions with Entry.” *American Economic Review* 84(3), 585–599.

**Version read.** [Published article, academic reference copy](https://kylewoodward.com/blog-data/pdfs/references/levin+smith-the-american-economic-review-1994A.pdf), 15 pages. All references below use journal pages.

**Status: verified for the entry model.** Trade-flow fields do not apply.

1. **Before entry.** Section I, pp. 586–587, Assumptions 1–4 and footnote 3: $N$ symmetric risk-neutral potential bidders know the mechanism and $N$. They may share public information. Each pays fixed real cost $c$ to develop and evaluate private information and prepare a bid. Entry precedes private estimates. Short quote, p. 587: “the entry fee is paid before bidders obtain estimates”.
2. **Values.** Assumption 2 uses compact value and estimate supports. Assumption 3 gives every bidder the same distribution. The paper covers common values, independent private values, and a conditional-independent affiliated private-value model. It does not impose a single uniform or binary value distribution throughout.
3. **What entry reveals.** Assumption 4 reveals the actual bidder count before bids. Since entry precedes private estimates, entry does not screen private values. The entrant’s value draw retains the common distribution. The private-value version therefore differs from selective entry after a private value signal.
4. **Mechanism.** The seller selects a highest-bid-wins mechanism, reserves that may depend on bidder count, and an entry fee $e$. Seller value is zero. Assumption 5 assumes a unique increasing symmetric Nash bid function at each bidder count. Footnote 4 selects that symmetric equilibrium if asymmetric bid equilibria also exist.
5. **Entry equation.** Equation (1), p. 587, averages the net payoff from entry across the binomial number of rival entrants:

   $$\sum_{n=1}^{N}\binom{N-1}{n-1}(q^*)^{n-1}(1-q^*)^{N-n}E[\pi\mid n,m]=0.$$

   The net payoff already includes $c$. Equation (2) also includes fee $e$. Total entry is binomial with parameters $N,q^*$. The authors focus on an interior entry regime.
6. **Uniqueness and multiplicity.** Footnote 6, p. 587, states uniqueness of the symmetric entry probability in the setting discussed there. It also admits asymmetric equilibria. One example selects a fixed subset of certain entrants. This is symmetry-based selection, not unconditional uniqueness of the game. No off-path belief refinement is needed for the stated private-value entry calculation.
7. **Distribution uncertainty extension.** Section I.B.2, pp. 593–594: an unknown parameter $z$ has common prior density $g(z)$. Values are conditionally iid with cdf $F(v\mid z)$. This induces affiliation. Proposition 7 distinguishes second-price and first-price mechanisms. This provides a source for uncertainty about a value distribution, but the latent parameter is shared across bidders.
8. **Limits.** The paper does not model a bidder who chooses a distribution before diligence. It does not contain a traded security, a market maker, noise orders, or an initial informed stake.

### B9. Ye (2007)

**Citation.** Lixin Ye. “Indicative Bidding and a Theory of Two-Stage Auctions.” *Games and Economic Behavior* 58(1), 181–207. DOI: 10.1016/j.geb.2005.12.004.

**Version reached.** [Publisher abstract and preview](https://www.sciencedirect.com/science/article/abs/pii/S089982560500165X); [bibliographic record](https://ideas.repec.org/a/eee/gamebe/v58y2007i1p181-207.html). The PDF link returned to the purchase page. Scholar’s seven versions and a search of the author’s university domain produced no accessible copy of this paper.

**Status: no full-text verification.** The abstract establishes costly value discovery and the distinction between nonbinding indicative bids and binding entry-right bids. The exact pre-entry signal, conditional value law, entry cost, disclosed information, and equilibrium assumptions remain **open**. Later papers’ descriptions do not substitute for this source.

### B10. Marmer, Shneyerov, and Xu (2013)

**Citation.** Vadim Marmer, Artyom Shneyerov, and Pai Xu. “What Model for Entry in First-Price Auctions? A Nonparametric Approach.” *Journal of Econometrics* 176(1), 46–58. DOI: 10.1016/j.jeconom.2013.04.005. [Publication record](https://ideas.repec.org/a/eee/econom/v176y2013i1p46-58.html).

**Version read.** [Author manuscript dated 3 April 2012](https://vadimmarmer.com/files/selectentry_joe_revision_12.pdf). The model references below use that version’s section, equation, and page numbers.

**Status: verified for this version’s entry model.** Published equation numbers were not checked.

1. **Information before cost.** Section 2.1, p. 5: nature draws $(V_i,S_i)$ independently across $N\geq2$ risk-neutral potential bidders. Each sees only $S_i$, at no cost. A bidder learns $V_i$ only after it pays $k\geq0$. Short quote: “they do not observe $V_i$.”
2. **Distribution.** The common joint cdf is $F(v,s)$. Both marginals equal $F(\cdot)$ after a signal normalization. Assumption 1 uses support $[\underline v,\bar v]^2$, continuous positive marginal density, and regular conditional distributions. There is no required binary or uniform value law.
3. **Ranking.** Assumption 2, p. 6, requires higher signals to give FOSD-better values conditional on a value at least the reserve. The assumptions allow an imperfect signal. Independence of $V_i,S_i$ gives the Levin–Smith limit. Perfect information gives the Samuelson limit; see equation (2).
4. **Entry selection.** The source restricts attention to symmetric Perfect Bayesian Nash equilibria with a signal cutoff $\bar s(N)$. Entry reveals $S_i\geq\bar s(N)$, not the exact signal or value. Equation (1) gives the entrant cdf:

   $$F(v\mid S_i\geq s)=\frac{\int_s^{\bar v}F(v\mid\widetilde s)\,dF(\widetilde s)}{1-F(s)}.$$

5. **Auction information.** Entrants learn their own values. Only values at least reserve $r$ produce bids. These firms are called active bidders. They know $N$ but do not know the active bidder count. They submit sealed first-price bids. The highest bid wins.
6. **Bid rule.** Section 2.1, equation (3), p. 6, gives the first-price differential equation. For a conjectured cutoff $s$, its slope is

   $$B_v(v;s,N)=\frac{(v-B(v;s,N))(N-1)(1-F(s))f(v\mid S_i\geq s)}{F(s)+(1-F(s))F(v\mid S_i\geq s)}.$$

   The source supplies the reserve boundary condition. The entrant’s uncertainty concerns rival entry and value, rather than market-maker order inference.
7. **Entry and uniqueness.** Lemma 2 gives expected gross profit $\Pi(s,\widetilde s,N)$ in equation (4). Assumptions 3–4 require continuity and strict increase along the common-cutoff argument. Proposition 1 and equation (5), pp. 7–8, give a unique symmetric cutoff equilibrium. An interior cutoff solves $k=\Pi(\bar s(N),\bar s(N),N)$. Corner cases have no entry or full entry. This uniqueness claim remains within the symmetric cutoff class.
8. **Post-entry values.** Section 2.2, equation (7), gives active bidders’ cdf $F^*(v\mid N)=F(v\mid S_i\geq\bar s(N),V_i\geq r)$. This differs from the distribution conditional on one bidder’s own signal.
9. **Nonapplicable fields.** There is no noise trade, market maker, stock price, or initial trading stake. No D1 or Intuitive Criterion is specified in the model characterization.

**Correction to the retrieval brief.** The outlet is *Journal of Econometrics*, not *Journal of Economic Theory*.

### B11. Gentry and Li (2014)

**Citation.** Matthew Gentry and Tong Li. “Identification in Auctions with Selective Entry.” *Econometrica* 82(1), 315–344. DOI: 10.3982/ECTA10293. [LSE publication record](https://researchonline.lse.ac.uk/id/eprint/66053/).

**Version read.** [Cemmap working paper CWP38/12, November 2012](https://www.cemmap.ac.uk/wp-content/uploads/2020/08/CWP3812.pdf). LSE restricts its accepted version to registered users. Section and equation numbers below refer to the working paper.

**Status: verified for this version’s symmetric entry model.** The published text and its numbering remain unverified.

1. **Sequence.** Section 1.1, pp. 6–7: each of $N$ potential bidders first sees a private signal $S_i$ about an unknown private value $V_i$. Entry costs $c$. Entrants then learn their exact values and submit bids. The cost can include value discovery, opportunity cost, and bid preparation.
2. **Distribution and prior.** Assumption 1, pp. 7–8, gives a common continuous joint cdf $F(v,s)$. Values have a bounded positive support. Value-signal pairs are independent across bidders. Signals have a uniform marginal on $[0,1]$ by normalization. Values need not be uniform. Higher signals give FOSD-better conditional values:

   $$s'\geq s\ \Longrightarrow\ F(v\mid s')\leq F(v\mid s).$$

   The authors use this weaker order instead of full affiliation. The label “Affiliated-Signal” does not mean cross-bidder affiliation here.
3. **Information at the auction.** Bidders know $N$ before entry. In the baseline they do not observe entrant count $n$ until the auction ends. Footnote 7 explains the alternative with known $n$.
4. **Entry information.** Section 1.2, pp. 9–10: a symmetric entry strategy has cutoff $s^*$. Entry implies $S_i\geq s^*$, but reveals neither its exact realization nor the value. Equation (1) gives

   $$F^*(v;s^*)=\frac{1}{1-s^*}\int_{s^*}^{1}F(v\mid t)\,dt.$$

5. **Auction and profit.** The core exposition uses a second-price sealed-bid auction. Entrants bid true values. Equation (2) gives the probability of beating all potential rivals:

   $$[s^*+(1-s^*)F^*(v;s^*)]^{N-1}.$$

   Equation (3) gives gross expected profit before value discovery:

   $$\Pi(s;s^*,N)=\int_0^{\bar v}[1-F(y\mid s)]
   [s^*+(1-s^*)F^*(y;s^*)]^{N-1}\,dy.$$

6. **Uniqueness.** Proposition 1, pp. 10–11, states a unique payoff-equivalent threshold representation within symmetric pure-strategy Bayesian Nash equilibria. An interior threshold solves equation (4), $\Pi(s^*;s^*,N)=c$. There are full-entry and no-entry corners. Footnote 11 expressly permits other asymmetric equilibria. It does not establish uniqueness across all strategy classes.
7. **Technical regularity.** Assumption 2 requires continuity of the integrated conditional cdf. This includes the perfectly informative limit, even though its conditional cdf has a jump. The paper also nests the uninformative-signal limit.
8. **Nonapplicable fields.** There is no stock trade, noise order, market maker, initial trading stake, or price-feedback decision. The entry characterization does not invoke D1 or the Intuitive Criterion.

**Use for point 1.** This is a particularly close source for a bidder that knows a conditional value distribution before it pays for exact value discovery. It does not let that bidder choose the distribution.

### B12. Roberts and Sweeting (2013)

**Citation.** James W. Roberts and Andrew Sweeting. “When Should Sellers Use Auctions?” *American Economic Review* 103(5), 1830–1861. DOI: 10.1257/aer.103.5.1830.

**Version read.** [Published article, academic reference copy](https://kylewoodward.com/blog-data/pdfs/references/roberts+sweeting-the-american-economic-review-2013A.pdf). The separate online appendix was not read. Journal page numbers apply below.

**Status: verified for the stated model and equilibrium restrictions.** The appendix proofs remain unverified.

1. **Values and known types.** Section I.A, p. 1835: the seller has one object and zero value without a sale. Potential buyers have known public types $\tau$, with known counts $N_\tau$. Values are independent private values on $[0,\bar V]$, with type-specific cdf $F_V^\tau$. The numerical specification uses lognormal values with an upper truncation. Type labels and their distributions are common knowledge.
2. **Before entry.** Section I.A, p. 1836: a buyer must pay $K_\tau$ before it can participate. Payment reveals its exact value. Before payment it sees

   $$S_{i\tau}=V_{i\tau}e^{\varepsilon_{i\tau}},\qquad
   \varepsilon_{i\tau}\sim N(0,\sigma_{\varepsilon\tau}^2).$$

   Signal errors are iid across bidders. Bayes’ rule gives its conditional value distribution. This formula was also checked visually because the text layer omits part of the paragraph.
3. **Information content.** A signal supplies information about the buyer’s own value, not rival values. Vanishing signal variance approaches exact pre-entry value information. Increasing variance approaches the uninformative-signal benchmark. An entry decision at a given threshold reveals that the private signal exceeds that threshold.
4. **Simultaneous mechanism.** Section I.B, pp. 1836–1837: potential buyers decide on entry simultaneously. Entrants discover their values, then bid in a second-price or open ascending auction. They bid to value. The highest value wins and pays the second-highest entrant value, subject to reserve $R$. Equation (1) sets expected auction profit at the type-specific threshold equal to $K_\tau$.
5. **Entry equilibrium and multiplicity.** Section I.B uses type-symmetric Bayesian Nash equilibrium. With multiple types, several equilibria can exist. The authors select an equilibrium where the higher-mean type has the lower entry threshold. They state parameter and reaction-function conditions for uniqueness within that selected class. They do not claim unconditional uniqueness of simultaneous entry.
6. **Sequential mechanism.** Section I.C, p. 1838: the seller approaches buyers in a known order that may depend on type, but not on private signals. Each buyer sees past entry decisions and bids. It then chooses whether to pay and learn its value. A new entrant faces the incumbent in an ascending knockout. The winner can submit a jump bid. A firm cannot return after exit. To prove uniqueness for more than two rounds, a firm can submit a jump bid only when it first becomes incumbent.
7. **What bids reveal.** Section I.C, equations (2)–(7), pp. 1839–1840: entry thresholds depend on the history and the posterior about incumbent value. The jump schedule separates incumbent values below the top pool. An observed separating bid reveals incumbent value through the inverse schedule. The highest-value interval pools. Thus jump bids reveal more than entry alone.
8. **Refinement.** Section I.C, pp. 1840–1841: the sequential solution is a PBE. All firms must bid to value in knockouts, on and off the path. Later entrants must draw the same inference from an off-path jump bid. A second belief restriction follows D1. It excludes value types with weaker deviation incentives. The authors use that restriction to exclude lower-value pools. Short quote: “consistent with the D1 refinement”.
9. **Limits.** There is no stock market, noise order, market maker, or informed initial stake. Public buyer types differ from an unknown latent distribution class observed only by a stock trader.

### C13. Noise-law search — verified hit and search limits

**Status: partial search.** A verified Laplace-order example follows. It is a numerical finance preprint. It does not establish a standard analytical convention.

**Verified hit: Friedrich and Teichmann (2020).** Paul Friedrich and Josef Teichmann, “Deep Investing in Kyle’s Single Period Model,” arXiv:2006.13889v1, 24 June 2020. No journal, volume, or page range is claimed. [Full HTML text read](https://arxiv.org/html/2006.13889v1). The HTML masthead also prints a later document date; the identifier fixes the version cited here.

1. **Core model.** Section 2, equations (2.1)–(2.2): the insider knows terminal value $Z=z$ and chooses a real-valued order $x$. The maker observes $x+Y$ and sets $P(x+Y)=E[Z\mid X+Y=x+Y]$. The insider maximizes $x(z-E[P(x+Y)])$. The model has an insider, additive independent noise, and a competitive conditional-mean price. It has no post-price real decision or initial stake term.
2. **Verified Laplace order.** Section 3.3 replaces normal laws by several alternatives. One exercise draws **both** terminal value $Z$ and noise order $Y$ from Laplace laws. The specified moments are $E[Y]=0$, $\operatorname{Var}(Y)=1$, $E[Z]=0.5$, and $\operatorname{Var}(Z)=4$. Thus this passage does concern the noise order. A later exercise changes only the value law and retains normal noise; that later exercise would not qualify by itself.
3. **Purpose and strength.** The device explores numerical equilibrium outside the normal specification. The section reports approximately linear numerical solutions in the both-Laplace exercise. It does not prove existence or uniqueness for Laplace noise. It does not use bounded likelihood ratios for a feedback theorem.
4. **Short quote.** Section 3.3: “both be distributed as Laplace”.
5. **Cost extension.** Section 3.4 separately adds a proportional cost $\varepsilon|x|$. This must not be attributed automatically to the Section 3.3 Laplace exercise.

**Other verified relevant sources.** Edmans (2009), A6 above, explicitly uses one-sided exponential noise for a closed-form sale size. Boleslavsky, Kelly, and Taylor (2017), A7 above, allows general full-support buy and sell densities. Neither passage names Laplace noise. These are distinct forms of precedent.

**Search record.** Scholar queries included `"noise trading" "Laplace"`, `"noise trader" "double exponential"`, and `"noise" "Laplace" "Kyle"`. Many results concerned return distributions, fundamental-value distributions, transforms, or artificial observation error. Such matches do not verify Laplace noise orders. Further search results and access limits follow below.

**Search continuation and limits.** Direct SSRN search for `Laplace noise trading` returned a security challenge. No login or challenge submission was attempted. An indexed SSRN search used `site:papers.ssrn.com "Laplace" "noise" trading`. A separate Scholar search used `"noise" "bounded likelihood ratio" finance`. The displayed matches mostly concerned signals, returns, or observation error. No additional full text verified a bounded-likelihood-ratio **noise-order** assumption. This is an access-limited search result, not a claim that no such paper exists. Those matches remain **unverified**.

### C14. Chordia and Subrahmanyam (2004)

**Citation.** Tarun Chordia and Avanidhar Subrahmanyam. “Order Imbalance and Individual Stock Returns: Theory and Evidence.” *Journal of Financial Economics* 72(3), 485–518. DOI: 10.1016/S0304-405X(03)00175-2. [Publication record](https://dro.deakin.edu.au/articles/journal_contribution/Order_imbalance_and_individual_stock_returns_theory_and_evidence/21028486).

**Version read.** [UCLA working-paper PDF](https://escholarship.org/content/qt34k8f3pv/qt34k8f3pv.pdf), body dated 7 October 2002. Its repository cover says 2000-10-07. This discrepancy must remain visible. The body date identifies the text read. Section and page references below use the working paper.

**Status: verified for the distributional question in this version.** The published text was not checked.

1. **Model distribution.** Section 2, pp. 6–7, equation (1): terminal payoff equals a positive mean plus two independent zero-mean normal shocks. Informed traders learn one shock just before the second trade date. Nobody observes the residual shock before liquidation.
2. **Liquidity orders.** A discretionary liquidity trader has demand $2z_1$ and can split it across two dates. A separate exogenous trade $z_2$ arrives at date two. Both $z_1,z_2$ are independent $N(0,v_z)$ variables, independent of payoff shocks. This is normal noise, not Laplace noise.
3. **Price mechanism.** Traders and market makers have exponential utility with common risk aversion $R$. They act competitively. Prices clear the market. Equations (2)–(3) conjecture linear prices. Lemma 1, equations (4)–(7), gives a **unique linear** equilibrium conditional on the equal split. This is not the risk-neutral conditional-mean price rule of the current paper.
4. **Empirical object.** Section 3, pp. 14–17, uses NYSE transaction data for 1988–1998. Order imbalance measures signed transactions or dollars. It is observed aggregate trade imbalance, not a separately observed exogenous noise order.
5. **Distributional facts.** Section 3.2 and Table 1 report means, medians, correlations, and autocorrelations. The unscaled imbalance measures have positive means and medians. First-lag transaction-imbalance autocorrelation is about 33%; its scaled counterpart is about 23%. These are the source’s descriptive results, not a new numerical diagnostic.
6. **What the facts do not establish.** This version does not supply a Laplace fit for noise orders. Its descriptive imbalance moments cannot identify the marginal law of an unobserved noise component. Short quote, Section 2: “normally distributed with zero mean and common variance”.
7. **Other fields.** There is no auction entry cost or post-price takeover decision. The theory uses continuous holdings, without the current paper’s unit order menu. Its characterization concerns linear competitive equilibrium rather than a discrete-game off-path refinement.

### D15. Meulbroek (1992) — short empirical note

**Citation.** Lisa K. Meulbroek. “An Empirical Analysis of Illegal Insider Trading.” *Journal of Finance* 47(5), 1661–1699. DOI: 10.1111/j.1540-6261.1992.tb04679.x.

**Version read.** [Publisher abstract and citation](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1992.tb04679.x). The full-text route returned to the abstract. Scholar versions and a working-paper search did not produce an accessible full text.

**Status: partial; abstract only.** The abstract reports SEC data on illegal insider trade. It reports an average abnormal return of 3% on insider-trade days. It also says almost half of the takeover run-up occurs on such days. These statements were read in the publisher’s abstract. The sample construction and causal interpretation were not checked.

**Use and limit.** This supports the broad claim that informed pre-announcement trade can affect price. It does not establish that a trader knows a potential bidder’s valuation or causes bidder discovery. No model specification is attributed to this empirical source. Short quote: “almost half of the pre-announcement stock price run-up”.

### D16. Augustin, Brenner, and Subrahmanyam (2019) — short empirical note

**Citation.** Patrick Augustin, Menachem Brenner, and Marti G. Subrahmanyam. “Informed Options Trading Prior to Takeover Announcements: Insider Trading?” *Management Science* 65(12), 5697–5720. DOI: 10.1287/mnsc.2018.3122.

**Versions read.** [Full working paper, May 2015](https://www.mcgill.ca/desautels/files/desautels/abs_2015_may_0.pdf), titled “Informed Options Trading prior to M&A Announcements: Insider Trading?” Also the [published abstract and citation](https://pubsonline.informs.org/doi/10.1287/mnsc.2018.3122). The published PDF route returned to the abstract. References below identify the version.

**Status: verified short note from the working paper; published full text unverified.**

- Working paper Section 3 uses 1,859 takeover transactions over 1996–2012 with target stock and option data. Section 5.1 examines abnormal option volume before announcements. About 25% of deals have statistically significant abnormal volumes at the 5% level.
- Working paper Section 5.1 and the published abstract locate stronger abnormal activity in short-dated out-of-the-money calls. Section 6 examines alternative explanations. Later sections compare SEC cases with the broad sample.
- The published abstract reports that the SEC litigates about 8% of sample deals. This is a published abstract fact. It does not identify all remaining abnormal trade as illegal trade.
- The study concerns information about takeover announcements and trade in target options. It does not identify knowledge of an undiscovered challenger’s private valuation. It does not establish price-induced bidder entry.
- This is an empirical source. The requested order menu, noise law, market-maker strategy, and equilibrium refinement are not its structural specifications. Short quote from the published abstract: “short-dated, out-of-the-money calls”.

## 4. What changes relative to the current paper

These are source comparisons, not new analytical claims about the current model.

- The published stake discussion in A1 concerns corrective investment. Its symmetry argument does not itself prove that the takeover model’s stake extension preserves Proposition 2.
- A2 verifies the three-point noise menu. It also distinguishes revelation of a trader’s information status from revelation of the state.
- A3 and A7 treat the distinction between price observation and flow observation explicitly. Their equilibrium restrictions matter for any comparison with Proposition A.2.
- A6 gives a sell-only model with a positive stake and continuous sale size. It states a technical reason for exponential noise.
- B10 and B11 give conditional value distributions before costly value discovery. Neither source requires a binary value distribution.
- B12 makes public bidder types and private preliminary signals distinct. It also separates equilibrium selection from a uniqueness claim.
- C13 supplies one verified numerical Laplace example. C14 supplies no empirical Laplace fit.

No retrieved passage proves or disproves the current paper’s main propositions. That question remains **open** in this retrieval memo.

## 5. Numerical example

No new numerical example was computed. This is a source-retrieval assignment. Reported numbers above belong to the cited papers and identified versions. There is no calculation script.

## 6. Open issues and risks

1. **Open:** obtain and inspect Edmans–Goldstein–Jiang Appendix B.2. The stake thresholds and admissible stake range remain unverified.
2. **Open:** obtain the full Kyle–Vila, Khanna–Sonti, and Ye texts. Their abstract-level descriptions cannot support exact model specifications.
3. **Open:** obtain Meulbroek’s full text before reliance on sample details or a causal interpretation.
4. **Open:** compare working-paper specifications with the published versions of B10, B11, C14, and D16. Their version labels must remain attached to the extracts.
5. **Open:** extend the bounded-likelihood-ratio search. The present access-limited search cannot establish absence of precedent.
6. The source results quoted here were not independently re-proved. None is labelled **analytical** as a new result of this memo. No new **numerical diagnostic** or **conjecture** is offered.

## 7. Recommendation

1. Use B10 and B11 for the sequence of preliminary information, costly entry, and exact value discovery.
2. Use A2 and A6 for precise comparisons of discrete noise, sale restrictions, and initial ownership.
3. Use A3 and A7 when the text discusses price observation, flow observation, or equilibrium uniqueness.
4. Present C13 as limited numerical precedent. Use A6 for an explicit tractability rationale for nonnormal noise.
5. Retain the unresolved source fields above. Do not fill them from later papers’ summaries.

## 8. Plain summary

Several sources directly support parts of the proposed extensions. The closest entry models give bidders a preliminary signal before they pay to discover their exact values. Their conditional value distributions can be continuous. A binary value prior is therefore not essential to that sequence.

The microstructure precedents differ sharply. Goldstein–Guembel uses discrete noise and two trade dates. Edmans uses one-sided exponential noise and a blockholder who can sell existing shares. Dow–Goldstein–Guembel uses normal noise and many small traders. Boleslavsky–Kelly–Taylor uses continuous orders and alternative trader identities. These features cannot be interchanged without a new argument.

Price observation also needs care. Some sources select an equilibrium that survives direct flow observation. Another needs random prices when the decision maker sees only price.

One numerical preprint explicitly uses Laplace noise orders. This verifies a precedent, but it does not establish a standard analytical assumption or an empirical fit. Chordia–Subrahmanyam instead assumes normal liquidity orders in the version read.

The unresolved sources remain clearly marked below.

## Coverage table

“Yes” verifies the stated scope in the identified full-text version. It does not certify unread appendices or published-version equivalence.

| Paper | Version read | Verified |
|---|---|---|
| Edmans, Goldstein, Jiang (2015) | Published II.E; B.2 unavailable | partial |
| Goldstein, Guembel (2008) | Published full text and appendix | yes |
| Dow, Goldstein, Guembel (2017) | Published full text | yes |
| Kyle, Vila (1991) | Journal abstract and preview only | no |
| Khanna, Sonti (2004) | Institutional abstract only | no |
| Edmans (2009) | Published core model and printed appendix | yes |
| Boleslavsky, Kelly, Taylor (2017) | Author manuscript, 1 February 2017 | yes |
| Levin, Smith (1994) | Published full text | yes |
| Ye (2007) | Publisher abstract and preview only | no |
| Marmer, Shneyerov, Xu (2013) | Author manuscript, 3 April 2012 | yes |
| Gentry, Li (2014) | Cemmap CWP38/12, November 2012 | yes |
| Roberts, Sweeting (2013) | Published model and stated restrictions | yes |
| Laplace / bounded-likelihood-ratio search | Scholar and indexed SSRN; direct SSRN blocked | partial |
| Friedrich, Teichmann (2020), extra hit | arXiv v1 full HTML, Sections 2 and 3.3 | yes |
| Chordia, Subrahmanyam (2004) | UCLA PDF body dated 7 October 2002 | yes |
| Meulbroek (1992) | Publisher abstract only | partial |
| Augustin, Brenner, Subrahmanyam (2019) | May 2015 full paper; published abstract | yes |
