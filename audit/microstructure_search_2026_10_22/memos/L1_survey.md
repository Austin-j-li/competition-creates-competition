# L1. Microstructure and corporate decisions

Date: 22 October 2026. Status: source review complete within the stated access limits.

## 1. Scope and method

This survey compares model sections. It does not edit the paper or derive a new equilibrium.
The paper reference is `overleaf/paper` commit `01bd5d6`, Sections 2–4 and its noise discussion.
The sample is purposive. Counts describe this sample, not the whole literature.
The shared auction formulas agree with equation (4) at the pinned commit. No new payoff calculation is used here.

Existing verified facts come from these records, without a new source check:

- [R1: LIT_extracts](../../alex_meeting_2026_10_21/memos/LIT_extracts.md), entries A1–A7.
- [R2: Q2_discrete_literature](../../alex_meeting_2026_10_21/memos/Q2_discrete_literature.md), Tables 2.1–2.2 and R1–R3.
- [R3: D_literature](../../discrete_exploration_2026_10_21/memos/D_literature.md), ranks 6–8 and 12.

`V` means the model passage is verified. `R` means an existing verified record supplies the model passage.
`A` means abstract only. `U` means unverified. An unread field stays `U`, even within a verified paper.
Source results are literature facts. Proposed transfers to this paper have status **open**.

All new source access uses one separate tab. No login, saved paper download, or challenge response occurs.
PDF text passes through memory only. Source files are not stored.
The separate research tab is closed. The three original tabs remain open.


### Access limits and versions

- Subrahmanyam–Titman and Fishman–Hagerty: publisher abstracts accessible; PDF requests returned HTTP 403.
- Subrahmanyam–Titman: the full-text route returned its abstract. A repository search lead returned HTTP 500.
- Bagnoli–Lipman: institutional record accessible; its PDF returned HTTP 403.
- Admati–Pfleiderer: Oxford returned a security page; the Stanford manuscript supplied the model section.
- Maug: the institutional repository displayed a security challenge. The university PDF supplied a scan without usable text.
- Kahn–Winton and Shleifer–Vishny: accessible published scans lacked usable text in this review; their model sections remain unverified.
- Kyle–Vila and Khanna–Sonti: retain R1's earlier access limits. No new attempt or verification occurred.
- Bulow–Huang–Klemperer: retain R3's abstract-only scope. Its stock-purchase stage remains unverified.
- The ECGI survey's old PDF address redirected to a record. Its current source link worked; the author supplied the advance article used here.

Working-paper pages remain attached to working-paper claims.
The Back, Admati–Pfleiderer, and Ozdenoren–Yuan model specifications are not certified as identical to their journal versions.
No test, numerical run, commit, or paper revision forms part of this survey.
No scripts or source downloads are retained.

## 2. Main table

Each row states the decision, informed orders, noise, observations, price, off-path rule, reason, result, and verification scope.
`MM` means market maker. `DM` means real decision maker. `NA` means the field does not apply.
An absent cost term is not evidence that a real market has no costs.

| ID; paper; class | Decision | Informed traders; orders; stake; cost | Noise and relative size | Observation and price | Off-path treatment | Stated reason and main result | Version; scope |
|---|---|---|---|---|---|---|---|
| C01 EGJ 2015; discrete three-point | Manager expands, holds, or contracts | One; perfect binary state; presence probability below one; orders −1,0,1; zero stake; symmetric unit cost | Additive −1,0,1, equal weights; same unit | MM and manager see total flow; competitive conditional-mean price | Intuitive Criterion at unused extreme flows | Exact reason: U; corrective action suppresses bad-news trade | R2 baseline, pp. 3774–3779, 3787; R1 A1 stake, pp. 3787–3788 |
| C02 Goldstein–Guembel 2008; discrete three-point | Manager invests or rejects | One always present; perfect state with probability α, otherwise uninformed; two dates; −1,0,1; zero initial stake; no separate cost term | Independent additive −1,0,1 each date, equal weights | MM and manager see both flows; conditional-mean prices | Constructed equilibrium gives all second flows positive probability; later result uses Intuitive Criterion | Flow observation eases exposition; uninformed sales can cause harmful disinvestment | R1 A2, pp. 136–143, 147 |
| C03 Dow–Goldstein–Guembel 2017; normal additive | Manager selects safe or risky project | Unit mass; costly imperfect binary signals; each order in [−1,1], endpoint choice; zero initial stake term | Normal, full real support; aggregate informed demand bounded | MM sees flow; manager sees price; conditional-mean price | Full-support noise; separate continuation selection | Exact noise rationale: U; endogenous information and multiple equilibria | R1 A3, pp. 880–885 |
| C04 Edmans 2009; one-sided exponential | Manager chooses investment before trade; price affects incentives | One blockholder; endogenous signal accuracy; hold or sell β≤stake α; no short sale; research cost | Positive exponential; endogenous sale size; mean depends on free float | MM sees public news and total demand; conditional-mean price; manager objective uses interim price | Overlap on positive flow; nonpositive flow reveals bad signal, not necessarily state | Closed-form endogenous sale size; block size and managerial myopia | R1 A6, pp. 2487–2494 |
| C05 Boleslavsky–Kelly–Taylor 2017; general density | Authority intervenes to repair state | One trader; informed with probability a, otherwise noise identity; real orders; no initial stake or order cost term | Alternative trader identity; smooth full-support densities on each side; same order domain | Baseline MM and authority see order; competitive price; price-only extension randomizes price | Positive density on each side; informed atoms would reveal state | Exact density rationale: U; asymmetric trade and intervention | R1 A7; 1 February 2017 manuscript, pp. 7–11, 14–20 |
| C06 Bond–Goldstein–Prescott 2010; other RE | Authority takes corrective action | Market knows fundamental; strategic order fields NA in main model | No noise order specified in inspected main model | Authority sees price plus private signal; rational expectations | Order-flow rule NA; price existence is substantive | Exact specification rationale: U; multiplicity and possible nonexistence | R3 rank 6, pp. 781–788; R2 for appendix limit |
| C07 Bond–Goldstein 2015; noisy RE | Government selects continuous intervention | Continuum of risk-averse speculators; normal private signals; continuous orders; stake U; order cost U | Normal supply shock, full support | Government sees price and private signal; linear equilibrium with market clearance | Refinement U | Exact noise rationale: U; reliance on price changes information aggregation | R3 rank 7, pp. 2777–2788 |
| C08 Goldstein–Ozdenoren–Yuan 2013; noisy RE | Capital provider selects investment | Many risk-neutral speculators; private and common normal signals; orders [−1,1], endpoints away from ties; stake U | Price-sensitive supply with normal shock | Capital provider sees price and private signal; linear monotone equilibrium | Refinement and tie selection U | Exact noise rationale: U; feedback creates coordination motives | R3 rank 8, pp. 570–572, 574–575 |
| C09 Dow–Gorton 1997; one-order arrival | Manager selects investment; shareholders select contract | One potential informed trader per period; costly exact-value research succeeds with probability τ; fixed trade x; reverses next period; initial stake U | Liquidity order ±x, equally likely; arrives with probability 1−τ; mutually exclusive with successful information | MM sees order; manager sees price plus own signal; conditional expected present value | Buy and sell occur; stationary equilibrium; other off-path rules U | Exogenous liquidity isolates investment efficiency; informative and inefficient no-information equilibria | V; published JF 52(3), 1087–1129, Sections I–II, pp. 1093–1101; order size, pp. 1124–1125 |
| C10 Holmström–Tirole 1993; Kyle-normal | Manager's two effort choices; owners' contract and insider share | One; costly normal signal; continuous unbounded order; zero initial stake; research cost | Independent normal, full real support; variance tied to free float | Arbitrageurs see total demand; conditional expected net liquidation value; contract uses price | Full-support noise; unique linear equilibrium only | Noise conceals information; liquidity improves information and performance assessment | V; published pp. 683–690 |
| C11 Admati–Pfleiderer 2009; other, binary exit motive | Manager's beneficial or harmful action before trade | One blockholder; private action or impact information; hold or sell entire stake; always present; no separate baseline order cost | Independent Bernoulli shock forces the same whole-stake sale; no additive noise in baseline | Dealers see sale or hold; competitive conditional means; manager's incentive depends on prices | Positive shock probability puts exit on path; alternative trades and zero-shock limit need care | Exact rationale U; exit can discipline, fail to discipline, or harm incentives in different cases | V; July 2007 manuscript, pp. 5–11; later cases not fully reviewed |
| C12 Edmans–Manso 2011; Kyle-normal | Manager and multiple blockholders choose effort before trade | I informed blockholders; exact normal value; continuous orders; each stake β/I; effort cost, no separate order cost | Independent normal additive demand, full real support | Dealer sees aggregate flow; conditional-mean price; manager values stake at price | Full support; unique linear equilibrium | Public blockholder effort separates effort and trade calculations; optimal blockholder count | V; published pp. 2402–2406 |
| C13 Faure-Grimaud–Gromb 2004; other, discrete two-point | Insider effort and decision to go public; later block sale | Separate speculator buys exact information at random public cost; equilibrium orders 0,−d; initial speculative stake U; insider stake 1−α | Liquidity order 0,−d, equal weights; same size; d depends on free float | Dealer sees unordered pair of orders, without identities; conditional-mean price; insider later sells at public price | Different-sized orders identify speculator; footnote discusses failure of separating PBE under aggregate flow | Observation choice avoids the stated existence problem; public trade improves prior incentives | V; published pp. 989–995 |
| C14 Back et al. 2018; Kyle-normal, continuous time | Activist selects effort after share accumulation | One; private initial position, normal prior; continuous trade rate; endogenous final stake; effort cost | Brownian cumulative noise; continuous unbounded support before final date | Dealers see aggregate history; conditional expected terminal value | Admissible strategies; terminal value revealed at final instant | Brownian rationale U; general activism technology can reverse liquidity-efficiency relation | V; December 2016 manuscript, pp. 6–9; journal equivalence U |
| C15 Ozdenoren–Yuan 2008; noisy RE | Feedback reduced form; managerial choice is an interpretation | Continuum; uniform private-signal errors; [0,z], endpoints in solution; stake and order cost U | Normal demand shock; full real support; price-sensitive uninformed demand | Investors see price and private signal; market clearance, no conditional-mean dealer | Exact refinement U; monotone cutoff class | Noise prevents full revelation; feedback amplifies price movements and can produce multiple prices | V; June 2007 manuscript, pp. 4–8; journal equivalence U |
| C16 Subrahmanyam–Titman 1999; unclassified | Public versus private finance | U | U | U | U | Information can make public finance valuable; market-development externality | A; publisher abstract |
| C17 Fishman–Hagerty 1989; unclassified | Disclosure and investment | U | U | U | U | Price information can improve investment; disclosure can exceed social optimum | A; publisher abstract |
| C18 Kyle–Vila 1991; unclassified | Takeover | U; outsider acquires shares, abstract only | Noise provides concealment; exact law U | U | U | Hidden accumulation before takeover | R1 A4, abstract only |
| C19 Khanna–Sonti 2004; unclassified | Value-creating manipulation and real feedback | Retained inventory matters; all exact fields U | U | U | U | Inventory can support value-creating manipulation | R1 A5, abstract only |
| C20 Bagnoli–Lipman 1996; unclassified | Genuine or manipulative takeover bid | Bidder can sell holdings; exact size and private information U | U | U | U | Manipulation affects takeover incidence and efficiency | A; RAND 27(1), 124–147; not RFS |
| C21 Shleifer–Vishny 1986; unclassified | Corporate control, title-level scope only | U | U | U | U | Model and rationale U | Record verified; model U |
| C22 Bulow–Huang–Klemperer 1999; auction, stock market unverified | Takeover auction with toehold | Given bidder ownership; acquisition stage U | U | Auction bids; stock price rule U | U | Toeholds affect auction incentives | R3 rank 12, abstract only |
| C23 Maug 1998; unclassified | Monitoring | Larger stakes and additional purchases, abstract only; exact fields U | U | U | U | Liquidity can improve governance incentives | A; society abstract; scan not read |
| C24 Kahn–Winton 1998; unclassified | Intervention | Institutional stake and speculative trade, abstract only; exact fields U | U | U | U | Speculation can raise or lower intervention | A; society abstract; scan not read |
| M01 Kyle 1985; method reference | NA | One insider; detailed law, stake, order set and cost U | Noise, exact law U at abstract scope | Competitive risk-neutral dealers; sequential auctions | Abstract states terminal revelation; other rules U | Dynamic information revelation and liquidity | A; society record |
| M02 Glosten–Milgrom 1985; method reference | NA | Superior information; all exact fields U | U | Zero-profit risk-neutral specialist; spread | U | Adverse selection explains spread | A; institutional record |
| M03 Easley–O'Hara 1987; method reference | NA | Trade size matters; exact size menu U | U | Dealers condition on size and sequence | U | Large informed orders face worse prices | A; publisher abstract |
| M04 Easley et al. 1996; method reference | NA | Information-based trade; exact fields U | U | Exact price model U | U | Empirical information-risk estimates and spreads | A; publisher-supplied abstract |
| S01 Bond–Edmans–Goldstein 2012; survey | Learning and incentive channels | NA | No preferred law ranked | Multiple price-model traditions | Model-specific | Forecasting efficiency versus information useful for decisions | V; advance article, §§1–4 |
| S02 Goldstein 2023; survey | Real effects of market information | Strategic versus price-taking taxonomy | No preferred law ranked | Kyle versus noisy RE traditions | Model-specific | Feedback changes trade and information incentives | V; published pp. 4–5, 12–19 |

## 3. Counts by model class

The denominator is **15 corporate-decision models with inspected model passages**, C01–C15.
Eight use existing verified records. Seven have new model-section reads.
The count excludes two surveys, four method records, and nine corporate papers without verified model specifications.
Each model enters one class. Version differences do not create additional observations.

| Model class | Count | Included models |
|---|---:|---|
| Kyle-normal | 3 | C10 Holmström–Tirole; C12 Edmans–Manso; C14 Back et al. |
| Discrete three-point, EGJ/GG | 2 | C01 EGJ; C02 Goldstein–Guembel |
| One-order arrival | 1 | C09 Dow–Gorton |
| Noisy rational expectations | 3 | C07 Bond–Goldstein; C08 Goldstein–Ozdenoren–Yuan; C15 Ozdenoren–Yuan |
| One-sided exponential | 1 | C04 Edmans |
| Uniform noise | 0 | None in the selected versions |
| General density | 1 | C05 Boleslavsky–Kelly–Taylor, 2017 manuscript |
| Other | 4 | C03 normal aggregate flow with competitive speculators; C06 price-only RE; C11 binary exit motive; C13 unordered discrete orders |
| Total | 15 | C01–C15 |

“Kyle-normal” here requires strategic continuous orders and normal noise, including Brownian noise in continuous time.
C03 also uses normal noise, but its informed speculators take prices as given.
Thus four models use the normal additive-flow family; three of those have strategic trade.
Three further models use normal demand or supply shocks in noisy RE markets.
Normal shocks therefore appear in seven models, through distinct mechanisms.

There are five verified discrete specifications in a broader sense: C01, C02, C09, C11, and C13.
They differ in aggregation, trader identity, and corporate timing.
C11 has continuous uncertainty about the action's impact, despite a binary exit menu.
C13 has two-point noise, not EGJ's additive three-point noise.
C15 uses uniform signal errors, not uniform noise orders.
The earlier BKT uniform-order manuscript is not counted alongside its general-density 2017 version.

These counts support several conventional model families. They do not establish which family dominates the literature.

## 4. Extracts per paper

### S01. Bond, Edmans, and Goldstein (2012)

Citation: “The Real Effects of Financial Markets.” *Annual Review of Financial Economics* 4, 339–360.
DOI: 10.1146/annurev-financial-110311-101826.
Version read: [author-supplied advance article](https://www.dropbox.com/scl/fi/z0dkgbrpr3sfjpp0eaf4k/surveyrealeffects-published.pdf?rlkey=kup120wkgaz74ugqf8ncnspes&dl=0), first posted 9 July 2012.
Its printed pages are 2.1–2.22. These are not final journal page numbers.
The ECGI March 2012 version is also accessible; the advance article supplies this entry.

Verified: Section 1 classifies real effects through price information, price-linked incentives, and nonfundamental price pressure.
Sections 2 and 3 distinguish decision makers who learn from prices from those whose incentives depend on prices.
Sections 4.1–4.7 classify implications, including information production, manipulation, frenzies, blockholders, and disclosure.
The survey cites rational-expectations, sequential-order, and strategic-order traditions together.
It does not give a frequency count or rank a preferred noise distribution.
It does not supply a discrete-versus-continuous taxonomy.

Quote, p. 2.4: “prices both affect and reflect firm cash flows”.
The survey supports the feedback architecture. Individual model sections must support exact order and noise assumptions.

### S02. Goldstein (2023)

Citation: Itay Goldstein. “Information in Financial Markets and Its Real Effects.” *Review of Finance* 27(1), 1–32.
DOI: 10.1093/rof/rfac052. Advance publication: 10 August 2022; issue: February 2023.
Version read: [published article on the author's institutional site](https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/informationrealeffect-published.pdf).
Read Sections 1.3 and 3.1–3.3, pp. 4–5, 12–19.

Verified: Section 3.3, p. 16, distinguishes strategic speculators after Kyle from price takers after Grossman–Stiglitz and Hellwig.
It places GG, EGJ, BKT, and the inventory-manipulation papers in the strategic group.
It places GOY's feedback and coordination mechanism in the price-taker group.
Section 3.1, p. 13, explains why feedback can require different specifications from traditional price models.
The survey does not say that normal noise is mandatory or that discrete models are exceptional.

Quote, p. 13: “feedback-effect models often rely on specifications that are different from the usual ones”.
This is a rationale for a tractable feedback model, not evidence for any particular noise law.

### C01–C08. Existing extracts, by paper

**C01, EGJ:** R2 Tables 2.1–2.2 verify the baseline and its pure-strategy equilibrium definition.
R2 R1–R2 records the presence interpretations and the revealing extreme flows.
R1 A1 verifies the positive-stake discussion only; its missing appendix remains unverified.
The relevant pages are 3775–3779 and 3787–3788.

**C02, GG:** R1 A2, pp. 136–143, verifies two trade dates, information uncertainty, inventories, and three-point additive noise.
Its uninformed trader can submit the same order as an informed trader.
R1 A2, p. 141, records full second-date flow support in the constructed manipulation equilibrium.
The later refinement result at p. 147 does not establish uniqueness in all parameter cases.

**C03, DGG:** R1 A3, pp. 880–885, verifies imperfect signals, bounded continuous positions, normal noise, and costly research.
Price can pool different flows at the safe-project payoff.
The recorded equilibrium selection survives direct flow observation by the firm.
This source does not make price observation automatically equivalent to flow observation.

**C04, Edmans:** R1 A6, pp. 2487–2494, verifies the stake, endogenous sale size, exponential noise, and managerial incentive channel.
A nonpositive flow reveals bad private news, rather than the state when the signal is imperfect.
Its exact rationale, p. 2489, is:

> “allows her trade to be endogenously derived as a function of block size.”

**C05, BKT:** R1 A7 controls the February 2017 version, pp. 7–11 and 14–20.
The noise identity has general full-support side densities; it is not an additive uniform order.
The price-only extension can require random prices.
Do not replace these facts with the earlier manuscript's uniform order specification in R2.

**C06, BGP:** R3 rank 6 verifies the price-first, action-second architecture, pp. 781–788.
The main model specifies rational-expectations prices without an explicit noise-order distribution.
R2's appendix reading verifies a separate market-game limit with no noise.
Neither record supplies a conventional discrete trading block for direct use here.

**C07, BG:** R3 rank 7 verifies continuous orders, normal signals and supply noise, pp. 2777–2788.
The government sees price and its own signal before continuous intervention.
The record does not verify the complete equilibrium correspondence or an order tie rule.

**C08, GOY:** R3 rank 8 verifies positions in [−1,1], endpoint choices, and a normal shock in price-sensitive supply.
The capital provider sees price and its private signal.
The solution uses a linear monotone equilibrium, pp. 570–572 and 574–575.
Endpoint choices do not make the aggregate order-flow experiment finite.

### C09. Dow and Gorton (1997)

Citation: “Stock Market Efficiency and Economic Efficiency: Is There a Connection?” *Journal of Finance* 52(3), 1087–1129.
Version read: [published article, university copy](https://www.bauer.uh.edu/nlangberg/papers_shiva/dow%20gorton%201997%20jf.pdf).
Read Sections I.F–K and II's equilibrium definition and price construction, pp. 1094–1101.
Appendix E, pp. 1124–1125, also confirms the informed order size x and its reversal.

Verified: Successful informed orders and liquidity orders are alternative arrivals, rather than independent additive orders.
Successful information and liquidity arrival are perfectly negatively correlated, by an explicit simplifying assumption.
Liquidity buys and sells have equal probabilities and size x.
An informed trader reverses its position next period, as does the liquidity trader.
The manager sees a buy-price or sell-price signal, plus its own possible information.

Quote, p. 1097: “we have simplified the model by assuming exogenous liquidity trade”.
The source links this choice to its focus on investment efficiency.
The quote does not justify a particular numerical noise variance.

### C10. Holmström and Tirole (1993)

Citation: “Market Liquidity and Performance Monitoring.” *Journal of Political Economy* 101(4), 678–709.
Version read: [published article, university copy](https://people.duke.edu/~qc2/BA532/1993%20JPE%20holmstrom%20and%20tirole.pdf).
Read Sections II–III, pp. 683–690.

Verified: The manager chooses short-term and long-term effort before trade.
Owners choose the contract and the share fraction held by insiders.
One risk-neutral speculator holds no initial shares and chooses signal precision at a convex cost.
Its normal signal concerns long-term value, with independent normal error.
It chooses a continuous, unbounded market order. The linear solution has a normal order distribution.

Liquidity demand is independent normal noise with full real support.
Its variance falls when insiders hold more shares.
Arbitrageurs observe aggregate demand. The price equals conditional expected net liquidation value.
The manager's compensation depends on the price, earnings, and final value.

The source states uniqueness only within linear equilibria.
No finite flow requires an off-path belief because noise has full support.

Quotes, p. 687:

> “liquidity traders serve the purpose of disguising the trades of the informed”

> “We could alternatively have employed these models for our purposes.”

The second quote concerns the rational-expectations alternatives named in footnote 13.
The model does not require a manager who learns a new investment signal after trade.

### C11. Admati and Pfleiderer (2009)

Citation: “The ‘Wall Street Walk’ and Shareholder Activism: Exit as a Form of Voice.”
*Review of Financial Studies* 22(7), 2645–2685.
Version read: [Stanford research paper 1918(R2), July 2007](https://gsb-faculty.stanford.edu/anat-r-admati/files/2022/04/rp1918r2.pdf).
The [institutional record](https://www.gsb.stanford.edu/faculty-research/working-papers/wall-street-walk-shareholder-activism-exit-form-voice) identifies this working paper.
Read Sections 1–2, manuscript pp. 5–11. Published-version equivalence remains unverified.

Verified: A manager chooses a beneficial or harmful binary action before trade.
The action's magnitude has a continuous density on [0,δ̄], with δ̄ positive and possibly infinite.
A large shareholder privately observes the action, its magnitude, or both, across the stated cases.

It holds its stake or sells the whole stake. The size is the existing stake, rather than a normalized unit.

With probability θ, an independent liquidity shock forces exactly the same sale.
Only the shareholder knows its motive. The baseline has no separate additive noise order.
Competitive risk-neutral dealers observe the sale decision and set conditional-mean prices.
The manager cares about interim and final prices. This is discipline before trade, rather than a post-price investment choice.
The baseline has no separate order cost; costly exit is an extension.

The equilibrium concept is Bayesian Nash.
A positive shock probability ensures that exit occurs on path.
The usual ties select managerial action and shareholder sale; some later cases instead require equilibrium mixtures.

Exact passage, manuscript p. 7:

> “independent of her private information, L will need to sell her entire stake in period 1.”

This passage verifies liquidity-motivated trade of the informed order's exact size.
A direct quote that explains the authors' choice of this specification remains unverified.

### C12. Edmans and Manso (2011)

Citation: “Governance Through Trading and Intervention: A Theory of Multiple Blockholders.”
*Review of Financial Studies* 24(7), 2395–2428.
Version read: [published article on the author's site](https://alexedmans.com/wp-content/uploads/2024/06/MB.pdf).
Read Section 2 and Section 2.1, pp. 2402–2406.

Verified: The manager and I blockholders choose effort before trade.
The manager's effort is private. Blockholder effort is public in the core model.
Each blockholder owns β/I shares and observes firm value exactly before trade.
Value contains an independent normal residual. Blockholders choose continuous market orders without a unit bound.

Independent noise demand is normal with variance σ². No finite extreme order exists.
The competitive dealer sees the sum of all orders and sets the conditional-mean price.
The manager values the market price of its stake. Blockholders value both trade profits and the fundamental value of their stakes.
No separate order cost appears in this section. Effort has a private cost.

Proposition 1 gives a unique linear trade equilibrium.
The source does not claim uniqueness over every nonlinear strategy.
Its main result concerns optimal blockholder numbers and the tradeoff between intervention and price information.

Quote, p. 2403:

> “This assumption is made only for tractability, since it allows the trading and effort decisions to be solved separately.”

This rationale concerns public blockholder effort. It does not explain the normal noise law.

### C13. Faure-Grimaud and Gromb (2004)

Citation: “Public Trading and Private Incentives.” *Review of Financial Studies* 17(4), 985–1014.
Version read: [published article, academic reference copy](https://www.edegan.com/pdfs/FaureGrimaud%20Gromb%20(2004)%20-%20Public%20Trading%20and%20Private%20Incentives.pdf).
Read Sections 1.1–1.3 and 2.1, pp. 989–995.

Verified: An insider holds 1−α and chooses effort before trade.
Effort changes the probability of a binary firm value.
A separate speculator pays a publicly observed research cost to observe value perfectly.
The cost has a known cdf on (0,∞), with positive density.
Liquidity demand is 0 or −d, with equal probabilities. Its size depends on free float.

An informed speculator selects 0 at high value and −d at low value.
An uninformed speculator submits zero in the stated representation.
Any different order identifies the speculator and removes its information rent.

The dealer observes the unordered pair of individual orders, not merely their sum and not their identities.
It posts the conditional-mean price. Mixed pairs pool; identical orders reveal value when the speculator is informed.
The insider later can face a public liquidity shock and must sell its whole block at the public price.
It cannot trade anonymously. There is no separate per-order cost in the stated baseline.

A footnote identifies a separating-equilibrium existence problem under aggregate-flow observation with discrete liquidity orders.
The result concerns public trade, information production, and prior intervention incentives.

Exact quote, footnote 4, p. 990:

> “only the aggregate order is observed. In our simplified version, under the latter assumption, a separating perfect bayesian equilibrium would fail to exist”

The quote explains why the observation assumption matters. It is not a claim about all discrete markets.
This two-point model does not conceal every extreme observation.

### C14. Back, Collin-Dufresne, Fos, Li, and Ljungqvist (2018)

Citation: “Activism, Strategic Trading, and Liquidity.” *Econometrica* 86(4), 1431–1463.
The [NBER record](https://www.nber.org/papers/w22893) verifies the published citation.
Version read: [NBER paper 22893, copy with December 2016 cover](https://www.nber.org/system/files/working_papers/w22893/revisions/w22893.rev0.pdf).
Read Section 3 and the equilibrium statement in Section 4, manuscript pp. 6–9.
The journal model and later revisions remain unverified here.

Verified: One activist trades continuously before it chooses costly effort.
Its private information is its initial share position, not an exogenous cash-flow signal.
Dealers assign a normal distribution to that initial position.
The activist chooses a continuous trade rate. No fixed unit menu applies.

Noise demand follows a Brownian motion. Dealers see the aggregate order history.
Competitive prices equal expected terminal value conditional on that history.
The terminal position determines optimal effort and the share value that effort creates.

Admissible strategies satisfy an integrability restriction; the model excludes doubling strategies.
The constructed equilibrium hides the activist's orders during trade, but price equals terminal value at the final instant.
The main result permits positive or negative relations between liquidity and economic efficiency, depending on the activism technology.
The model contains an effort cost and endogenous price impact. It adds no separate per-unit order cost in the inspected objective.

Quote, p. 7:

> “the value V depends on XT in our model.”

This states the departure from the standard price model. A direct rationale for Brownian noise remains unverified.

### C15. Ozdenoren and Yuan (2008)

Citation: “Feedback Effects and Asset Prices.” *Journal of Finance* 63(4), 1939–1975.
The [author's publication page](https://personal.lse.ac.uk/yuan/) verifies the published citation.
Version read: [author manuscript, June 2007](https://personal.lse.ac.uk/yuan/papers/strategicuncertainty.pdf).
Read Sections I and II.A, manuscript pp. 4–8.
Published-version equivalence remains unverified.

Verified: Feedback enters the dividend as a function of aggregate informed investment and the fundamental.
Managerial inference is an interpretation of this function. The baseline does not solve a separate manager's choice.
A unit mass of informed investors receives private signals with uniform errors on [−1,1].
The fundamental has an improper flat prior. A separate cash-flow component is normal.

Each informed investor chooses a position in [0,z]. Risk neutrality gives choices of zero or z away from ties.
Mean-variance uninformed investors provide a price-sensitive demand curve.
An independent normal noise demand prevents full price revelation.
The market clears through informed demand, uninformed demand, and noise demand.
Informed investors observe both their signals and the price.
There is no separate competitive conditional-mean dealer in this specification.

Initial stake and an explicit per-order cost remain unverified.
The equilibrium restriction uses monotone cutoff strategies.
The source distinguishes unique strategies conditional on price from possible multiplicity of prices.
This is noisy rational expectations with normal noise. Uniform signal errors do not make it a uniform-noise model.

Quote, p. 6:

> “This assumption introduces noise in the information aggregation process and prevents the market-clearing price from fully revealing the fundamentals.”

### C16–C24. Sources outside the verified model count

#### C16. Subrahmanyam and Titman (1999)

Citation: “The Going-Public Decision and the Development of Financial Markets.” *Journal of Finance* 54(3), 1045–1082.
[Publisher abstract and issue record](https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00136). Status: **abstract only**.
The abstract links public-market information to private versus public finance and to market-development externalities.
The public-firm advantage depends on information diversity, acquisition cost, and information available without cost.

All order, noise, observation, pricing, stake, and off-path fields remain unverified.
The full-text address returned the abstract. The PDF request returned HTTP 403.
The date of the journal issue is June 1999; the later electronic publication date is not the article's citation year.

#### C17. Fishman and Hagerty (1989)

Citation: “Disclosure Decisions by Firms and the Competition for Price Efficiency.” *Journal of Finance* 44(3), 633–646.
[Publisher abstract and record](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1989.tb04382.x). Status: **abstract only**.
The abstract links voluntary disclosure to price efficiency and investment efficiency.
It reports possible excess expenditure on disclosure relative to the social optimum.
All exact microstructure fields remain unverified. The PDF request returned HTTP 403.

#### C18. Kyle and Vila (1991)

Citation and evidence: **R1 A4**, “Noise Trading and Takeovers,” *RAND Journal of Economics* 22(1), 54–71.
Status: **existing abstract record only**. No new source check.
Noise conceals purchases before a takeover. Exact orders, noise law, stake, costs, and off-path rules remain unverified.
R1 records a login barrier and a limited preview. Those are inherited access limits, not new failures.

#### C19. Khanna and Sonti (2004)

Citation and evidence: **R1 A5**, “Value Creating Stock Manipulation: Feedback Effect of Stock Prices on Firm Value.”
*Journal of Financial Markets* 7(3), 237–270.
Status: **existing abstract record only**. No new source check.
The record verifies the role of retained inventory in value-creating manipulation.
Exact order and noise specifications remain unverified. R1 records publisher and repository access limits.

#### C20. Bagnoli and Lipman (1996)

Citation: “Stock Price Manipulation Through Takeover Bids.” *RAND Journal of Economics* 27(1), 124–147.
[Publisher-supplied record and abstract](https://ideas.repec.org/a/rje/randje/v27y1996ispringp124-147.html).
[Institutional working-paper record, November 1989](https://deepblue.lib.umich.edu/items/78d97ca5-e6cb-4820-aad7-0f1f962c3ab9).
Status: **abstract only**. The outlet in the task's target list needs correction: RAND, not RFS.
The abstract describes a bid that raises the price and lets its owner sell, with consequences for efficient takeovers.
It distinguishes manipulation effects in markets with low and high takeover activity.

The repository PDF returned HTTP 403. All exact microstructure fields remain unverified.

#### C21. Shleifer and Vishny (1986)

Citation: “Large Shareholders and Corporate Control.” *Journal of Political Economy* 94(3), 461–488.
[Author's record and source link](https://shleifer.scholars.harvard.edu/publications/large-shareholders-and-corporate-control).
Status: **record verified; model unverified**.
The author-supplied published PDF is a scan without a usable text layer in this review.
No model claim, noise class, or order menu is inferred from the title or later papers.

#### C22. Bulow, Huang, and Klemperer (1999)

Citation and evidence: **R3 rank 12**, “Toeholds and Takeovers.” *Journal of Political Economy* 107(3), 427–454.
Status: **existing abstract record only**. No new source check.
A bidder owns a toehold before the auction. Its incentive effects differ between common and private values.
The record does not verify an endogenous stock-purchase stage or a noise law.
Do not count a given toehold as a verified market microstructure.

#### C23. Maug (1998)

Citation: “Large Shareholders as Monitors: Is There a Trade-Off between Liquidity and Control?” *Journal of Finance* 53(1), 65–98.
[Journal society's issue record and abstract](https://afajof.org/issue/volume-53-issue-1/).
Status: **abstract only**. The accessible university PDF is a scan without a usable text layer in this review.
The institutional repository displayed a security challenge. No response to that challenge occurred.
The abstract states that liquid markets facilitate larger stakes and additional purchases, which can improve costly monitoring incentives.
All exact order, noise, observation, and off-path fields remain unverified.

#### C24. Kahn and Winton (1998)

Citation: “Ownership Structure, Speculation, and Shareholder Intervention.” *Journal of Finance* 53(1), 99–129.
[Journal society's issue record and abstract](https://afajof.org/issue/volume-53-issue-1/).
Status: **abstract only**. The accessible university PDF is a scan without a usable text layer in this review.
The abstract distinguishes intervention gains on existing shares from changes in speculative profits.
Speculation can raise or lower intervention incentives.
All exact order, noise, observation, and off-path fields remain unverified.

### M01–M04. Method references

These are method records. They do not supply a subsequent corporate decision.
They do not enter the corporate-model count.

- **M01: Kyle (1985).** “Continuous Auctions and Insider Trading.” *Econometrica* 53(6), 1315–1336.
  [Society record and abstract](https://www.econometricsociety.org/publications/econometrica/1985/11/01/continuous-auctions-and-insider-trading).
  **Abstract only.** One risk-neutral insider, noise traders, and competitive risk-neutral dealers; sequential auctions approach continuous trade.
  The abstract states full information revelation by the end of trade. Detailed laws and order constraints remain unverified here.
- **M02: Glosten and Milgrom (1985).** “Bid, Ask, and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders.”
  *Journal of Financial Economics* 14(1), 71–100.
  [Author's institutional record and abstract](https://business.columbia.edu/faculty/research/bid-ask-and-transaction-prices-specialist-market-heterogeneously-informed-traders).
  **Abstract only.** Superior information generates a spread despite a risk-neutral dealer's zero expected profit.
  Unit size, arrival probabilities, and exact off-path rules remain unverified in this abstract-level review.
- **M03: Easley and O'Hara (1987).** “Price, Trade Size, and Information in Securities Markets.”
  *Journal of Financial Economics* 19(1), 69–90.
  [Publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/0304405X87900298).
  [Publisher-supplied citation](https://ideas.repec.org/a/eee/jfinec/v19y1987i1p69-90.html).
  **Abstract only.** Informed investors prefer larger trades at a given price; dealers therefore condition prices on size and sequence.
  Exact size menus and size probabilities remain unverified.
- **M04: Easley, Kiefer, O'Hara, and Paperman (1996).** “Liquidity, Information, and Infrequently Traded Stocks.”
  *Journal of Finance* 51(4), 1405–1436.
  [Publisher-supplied record and abstract](https://ideas.repec.org/a/bla/jfinan/v51y1996i4p1405-36.html).
  **Abstract only.** The study estimates information-based trade risk from trade data and relates it to spreads and volume.
  The exact arrival law and the PIN formula remain unverified here.

The one-order and PIN traditions are relevant leads for method choice.
These four abstracts do not verify every detail of their familiar textbook versions.
They do not prove any takeover-entry result.

## 5. Discrete devices that conceal information

### 5.1 Presence or inability to trade: interior concealment only

**Literature fact.** R2 R1–R2 verifies EGJ's discussion at p. 3787.
The speculator can be absent or unable to trade after a liquidity shock.
A third interpretation permits an uninformed speculator, but EGJ does not analyze that framework there.

Exact source passage, as transcribed in R2:

> “λ<1 is necessary for the speculator not to be fully revealed when X={−1,1}”

This passage concerns interior flows. It does not conceal X=±2 under informed purchases and sales with EGJ's bounded noise.
**Open transfer:** presence alone does not supply a cap below one for every posterior in the proposed market.

### 5.2 A same-size uninformed speculator: asymmetric concealment

**Literature fact.** R1 A2 verifies GG's always-present speculator and its information probability, p. 137.
The uninformed type can submit exactly the same unit sale as the low informed type.
The existing record states, for pp. 141–142:

> “Flows $Q_1=-2,-1$ identify a pool of low and uninformed speculators. They do not identify the low state.”

This is an exact passage from **the verified record**, not a verbatim quotation from the article.
The requested article passage is not transcribed in that record. It remains unavailable under the instruction against a new source check.
The same record verifies that Q₁=2 still reveals the high state.
**Open transfer:** the uninformed type changes incentives and can manipulate the real decision. It is not an exogenous presence draw.

### 5.3 Alternative informed and liquidity arrivals of the same size

**Literature fact.** Dow–Gorton, pp. 1095 and 1124–1125, uses liquidity and informed orders of size x.
Their information-arrival event is, p. 1095:

> “perfectly negatively correlated with the arrival of a liquidity trader.”

This is the authors' explicit simplifying assumption.
A buy can therefore come from a successful informed arrival or from a liquidity arrival.
There is no sum of a maximal informed buy and an independent maximal noise buy.
**Open transfer:** replace the auction's information experiment and rederive trade profits before any entry comparison.

### 5.4 A liquidity shock that forces the informed holder's exact sale

**Literature fact.** Admati–Pfleiderer, July 2007 manuscript p. 7, supplies the exact passage quoted in C11.
The trade has the same size whether private information or liquidity causes exit.
Footnote 9 states that positive shock probability makes exit occur on path.
Footnote 10 explains why other trade sizes can reveal information and remove expected speculative profits.
**Open transfer:** the original model disciplines an earlier managerial action. A challenger who learns after trade requires a new continuation.

### 5.5 Separate orders without identities

**Literature fact.** Faure-Grimaud–Gromb, pp. 990–993, uses individual orders in {0,−d}.
The dealer sees the unordered pair. It does not observe trader identities.
A mixed pair pools identities; an identical pair reveals the informed order when information is acquired.
The article explains the departure from aggregate-flow observation in footnote 4, quoted in C13.
**Open transfer:** this is a discrete precedent, but it neither hides every extreme observation nor copies EGJ's information set.

### 5.6 Random size, wider noise, and imperfect information

**Not verified as discrete corporate devices in this sample:** random order size and wider bounded noise.
Easley–O'Hara's abstract verifies that size affects inference, but it does not verify the required size probabilities.
No inspected source passage supports unequal EGJ noise weights or an added large liquidity order as an established corporate-model convention.
Those remain **open design proposals**, rather than literature facts.

**Literature fact:** C04's imperfect private signal prevents a revealed bad signal from necessarily revealing the state.
This changes what the investor knows; it does not hide its order identity.
C03, C10, C12, and C14 use normal or Brownian noise to retain overlap before the terminal date.
C05 uses overlapping trader identities and continuous densities; informed order atoms could reveal information.
These are continuous alternatives, rather than verified finite-noise repairs.

### 5.7 The requirement for this paper

**Open.** A candidate needs opposite-state probability at the flow that induces expensive preparation.
It also needs profitable trade at the flows reached by the informed investor.
A motive mixture can supply the first property without preserving the investor's earlier payoff threshold.
An off-path convention can define unused prices without preventing on-path revelation.
The literature verifies these distinctions. It does not verify the desired entry path at this paper's benchmark.

## 6. Plain summary

The literature offers several established ways to join corporate decisions with trade.
The two surveys organize the economics by information, incentives, and strategic versus price-taking investors.
Neither survey requires normal noise or identifies one preferred distribution.

EGJ and GG provide the closest three-point models.
Both use unit orders and additive noise with equal probabilities on sale, hold, and purchase.
Their managers observe flows. Price observation requires a separate argument.

Presence uncertainty does not hide EGJ's outer flows.
Other discrete models use a different device.
Dow–Gorton lets either an informed trader or a same-size liquidity trader arrive.
Admati–Pfleiderer lets a liquidity shock force the same whole-stake sale that private information can cause.
GG lets an uninformed speculator submit the same unit sale as an informed speculator.
Each device can conceal the trader's motive or identity. Each also changes incentives or timing.

Faure-Grimaud–Gromb supplies another discrete precedent, but its dealer sees separate orders without their identities.
It does not use EGJ's aggregate-flow information set.
Normal noise, exponential noise, and general continuous densities supply further precedents with different economic purposes.

For an EGJ-like version, the five first references are EGJ, GG, Dow–Gorton, Admati–Pfleiderer, and Faure-Grimaud–Gromb.
DGG remains essential for information-production feedback and the limits of price observation.
No cited passage establishes this paper's complete entry reversal or coexistence result.
No verified discrete source here uses random order size or wider bounded noise to recover that result.
Those choices require their own equilibrium analysis.
