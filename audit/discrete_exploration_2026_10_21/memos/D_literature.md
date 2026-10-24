# D. Literature for discrete feedback and takeover dynamics

Date: 21 October 2026. Workstream: D1. Status: source review complete within the access limits below.

## 1. Question

Which verified sources help with C.1–C.10? Which sources contain discrete trade, several trade dates, and a real decision?

The closest complete precedent is the existing Goldstein–Guembel record.
The new records extend coverage of preemption, sequential entry, stakes, disclosure, and real options.
Several calendar dates do not imply several trade rounds.

## 2. Setup

This memo compares sources. It does not modify either discrete base model or claim a new equilibrium.
The three-point model is the first reference. The discrete-Laplace model is the second reference.
Both retain Reading N, $c_L=0$, and buy-only orders as the initial specification.
No discrete-Laplace candidate result from the brief is an input to this review.

The paper reference is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`, read through its committed `main.tex`.
Relevant locations are Sections 2–4, 5–6, and Appendix A.
The shared payoff formulas agree with equation (4) there. This review does not use them for a new calculation.

Source facts carry the required verification labels.
Each proposed transfer to C.1–C.10 has status **open** until the relevant workstream supplies its own proof.
The source's theorem is distinct from a theorem for either discrete base model.
No new analytical, computer-assisted, or numerical diagnostic result is claimed here.

An abstract verifies only its stated model features and broad results.
For every abstract-only source, equilibrium concepts, off-path beliefs, and both tie rules remain unverified unless an entry states otherwise.
An accessible section preview supports only the quoted passage. It does not establish full-text verification.
For full-text sources, each entry states the sections actually inspected.

Existing records remain in [LIT_extracts.md](../../alex_meeting_2026_10_21/memos/LIT_extracts.md).
Four entries below refer to those records instead of a duplicate bibliography or duplicate extracts.
Their verification status derives from that same-day record, rather than a new source read here.
The prior discrete memos and their independent check supply context, not new literature verification.

The source order below is the relevance rank for this brief.
Extracts are short, verbatim fragments. Each new source contributes at most 25 words in the evidence extracts.
Quoted grammar and technical titles retain their original form.

## 3. Results

### 3.1 Rank 1 — Goldstein and Guembel (2008); existing record A2

**Verification: verified (full text), by reference.** Read the bibliography, URLs, extracts, and formal details in [A2](../../alex_meeting_2026_10_21/memos/LIT_extracts.md#a2-goldstein-and-guembel-2008).

**Model and relevant result.** A2 verifies two trade dates, finite orders, equal three-point noise, and a later real choice.
It also verifies the manipulation equilibrium and the first position's role at the second date.
The real decision maker observes flows in the stated construction.

**What this team can use — open.** This is the first template for C.1, C.2, and C.5.
Use its history-dependent strategy structure. Preserve its distinction between current profit and continuation profit.
Its flow observation does not establish price sufficiency for this project.
Use A2's exact equilibrium and belief qualifications; do not infer uniqueness from its existence result.

### 3.2 Rank 2 — Dow, Goldstein, and Guembel (2017); existing record A3

**Verification: verified (full text), by reference.** The bibliography, URLs, and extracts are in [A3](../../alex_meeting_2026_10_21/memos/LIT_extracts.md#a3-dow-goldstein-and-guembel-2017).

**Model and relevant result.** A3 verifies costly private signals and an endogenous mass of informed investors.
The real choice changes the claim's sensitivity to the state and therefore the private return to research.
The specification uses normal noise and a continuum of investors.

**What this team can use — open.** This is the closest source for C.6 and information-based coexistence.
Use its research-profit condition as an economic template, then derive the discrete investor's actual acquisition payoff.
Its selected continuation and stability conditions matter. It does not provide a discrete, two-round equilibrium.

### 3.3 Rank 3 — Fishman (1988)

**Record.** Michael J. Fishman. 1988. “A Theory of Preemptive Takeover Bidding.” *RAND Journal of Economics* 19(1), 88–101.

**URLs read.** [Author institution: abstract and citation](https://www.kellogg.northwestern.edu/academics-research/research/detail/1988/a-theory-of-preemptive-takeover-bidding/).
[Publisher-supplied bibliography](https://ideas.repec.org/a/rje/randje/v19y1988ispringp88-101.html) supplies the volume omitted from that institutional citation.

**Verification: verified (abstract only).**

**Model.** A takeover auction starts before all bidders acquire costly information.
An initial offer can therefore precede a rival's information decision.
This is a sequence of takeover actions, not verified stock-market trade rounds.

**Relevant result and evidence.** The model explains high initial offers that deter later competition.
The institutional abstract states “acquire costly information after the bidding has begun” and “high premium (\"preemptive\") initial bids”.
Both extracts come from the abstract; no proposition number is verified.

**What this team can use — open.** C.7 can give the incumbent a preemptive offer before the challenger prepares.
C.4 can distinguish deterrence of research from deterrence of an already informed bidder.
An incumbent response specifically to a stock price requires a new argument.

### 3.4 Rank 4 — Bulow and Klemperer (2009)

**Record.** Jeremy Bulow and Paul Klemperer. 2009. “Why Do Sellers (Usually) Prefer Auctions?” *American Economic Review* 99(4), 1544–1575.
DOI: 10.1257/aer.99.4.1544.

**URL read.** [Publisher: record and abstract](https://www.aeaweb.org/articles?id=10.1257/aer.99.4.1544).

**Verification: verified (abstract only).**

**Model.** Participation is costly.
The paper compares a simultaneous auction with a sequence in which potential buyers choose whether to enter.
The abstract also covers contractual terms that affect that sequence.

**Relevant result and evidence.** Sequential entry is more efficient in the stated comparison, while the auction usually yields more revenue.
The abstract states “The sequential process is always more efficient.”
It then states “the auction is more conducive to entry”.
Its intervening discussion attributes a surplus transfer to preemptive bids.

**What this team can use — open.** C.4 and C.7 can separate efficient information costs from seller revenue.
C.8 and C.10 can compare sale procedures or entry subsidies.
The abstract verifies no feedback price path and no theorem about this project's reserve choice.

### 3.5 Rank 5 — Khanna and Mathews (2012)

**Record.** Naveen Khanna and Richmond D. Mathews. 2012.
“Doing battle with short sellers: The conflicted role of blockholders in bear raids.”
*Journal of Financial Economics* 106(2), 229–246. DOI: 10.1016/j.jfineco.2012.06.006.

**URL read.** [Publisher: record, abstract, introduction, and section previews](https://www.sciencedirect.com/science/article/abs/pii/S0304405X12001328).

**Verification: verified (abstract only).** The introduction and Section 4 preview provide additional verified passages; the complete text remains unverified.

**Model.** An informed blockholder can defend a valuable relationship through share purchases.
An uninformed speculator can exploit the conflict between the blockholder's information profit and stake value.
The introduction describes a risk-averse counterparty whose real choice responds to price.
Section 4 adds an earlier trade round to endogenize the speculator's initial position.

**Relevant result and evidence.** A large stake can support costly defensive purchases, but a smaller stake need not prevent manipulation.
Abstract: “a sufficiently large blockholder” and “prevent a bear raid”.
Section 4 preview, on position formation: “we introduce an additional trading round”.
Introduction: “accept the relationship based on the observed price”.

**What this team can use — open.** C.5 must include the stake payoff when an order changes a real choice.
C.2 and C.10 can distinguish an inherited stake from a stake formed through earlier trade.
Exact trade menus, noise support, and the full Section 4 equilibrium remain unverified.
This preview is a dynamic lead, not a verified discrete-noise template.

### 3.6 Rank 6 — Bond, Goldstein, and Prescott (2010)

**Record.** Philip Bond, Itay Goldstein, and Edward Simpson Prescott. 2010.
“Market-Based Corrective Actions.” *Review of Financial Studies* 23(2), 781–820. DOI: 10.1093/rfs/hhp059.

**URLs read.** [Published full text supplied by an author](https://www.dropbox.com/scl/fi/cgz6shs9ok81zk0poa8kv/marketbasedcorrectiveaction-published.pdf?rlkey=w3r425jz5wtxh5ai8xe5dql1z&dl=0).
[Author's source list](https://fnce.wharton.upenn.edu/profile/itayg/) identifies the copy.
[Publisher-supplied bibliography](https://ideas.repec.org/a/oup/rfinst/v23y2010i2p781-820.html) confirms the complete record.

**Verification: verified (full text).** Inspected introduction, Section 1, and Sections 2.1–2.3, pp. 781–788.

**Model.** A security price forms at date 0. A real decision follows at date 1; the security pays at date 2.
The decision maker also receives a private signal.
The market knows the fundamental, while the expected intervention changes the security value.
This is one price date, not two strategic trade rounds.

**Relevant result and evidence.** Feedback can make the fundamental-to-price relation nonmonotone.
Private information helps the decision maker interpret that price.
Section 1, p. 784: “At date 0, the price of the security”.
Section 1.3, p. 786: “the agent observes a noisy signal”.
Abstract, p. 781: “market information and agents’ information are complementary”.

**Formal details.** Definition 1, p. 787, combines rational-expectations prices with optimal intervention.
Footnote 9 permits any intervention probability at indifference. Footnote 10 distinguishes this price condition from a strategic market game.
The inspected passages supply no transplantable investor tie rule or off-path order rule.

**What this team can use — open.** C.7, C.8, and C.10 need a price inference argument after the real policy changes.
C.3 can use the distinction between private information and market information.
This source does not justify direct substitution of flow observation for price observation.

### 3.7 Rank 7 — Bond and Goldstein (2015)

**Record.** Philip Bond and Itay Goldstein. 2015.
“Government Intervention and Information Aggregation by Prices.” *Journal of Finance* 70(6), 2777–2812.
DOI: 10.1111/jofi.12303.

**URLs read.** [Publisher: complete record and abstract](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12303).
[Published full text supplied by an author](https://www.dropbox.com/scl/fi/enj79ssc35hw7ip2t2op0/informationaggregation-published.pdf?rlkey=0jbfjj0krgdwcbpzcc22im6ep&dl=0).
The [author's source list](https://fnce.wharton.upenn.edu/profile/itayg/) identifies that copy.

**Verification: verified (full text).** Inspected abstract, introduction, Section I.A–C, and the start of Section II, pp. 2777–2788.
Policy conclusions below are verified from the abstract and introduction, not their complete proofs.

**Model.** A continuum of risk-averse speculators trades at date 0.
Private signals and the supply shock are normal. Trade size is a choice variable.
At date 1, the government uses price and its private signal to select an intervention.
The security pays at date 2. This specification has one trade date.

**Relevant result and evidence.** More reliance on price can impair the information that price supplies.
Disclosure effects depend on which information the government reveals.
Abstract: “price informativeness is endogenous to government policy”, “limit its reliance on market prices”, and “limit transparency in some dimensions”.
Section I.B, pp. 2785–2786: “a noisy supply shock”.

**Formal details.** Section II studies a linear equilibrium with normal primitives.
The inspected passages do not verify all equilibrium branches or off-path restrictions.
The investor's tie rule remains unverified in those passages.
The government chooses a continuous intervention, so the project's binary entry tie rule is a new requirement.

**What this team can use — open.** C.8 and C.10 can study policy commitment and targeted disclosure.
C.6 can distinguish information aggregation from acquisition of a new signal.
This source does not supply a several-round discrete mechanism.

### 3.8 Rank 8 — Goldstein, Ozdenoren, and Yuan (2013)

**Record.** Itay Goldstein, Emre Ozdenoren, and Kathy Yuan. 2013.
“Trading frenzies and their impact on real investment.” *Journal of Financial Economics* 109(2), 566–582.
DOI: 10.1016/j.jfineco.2013.03.011.

**URLs read.** [Publisher: record and preview](https://www.sciencedirect.com/science/article/abs/pii/S0304405X13000913).
[Published full text supplied by an author](https://www.dropbox.com/scl/fi/98lvvnbyo98mtp1q48p4s/tradingfrenzies-published.pdf?rlkey=s49i24uemx9jw7gtgm1li0kcu&dl=0).
The [author's source list](https://fnce.wharton.upenn.edu/profile/itayg/) identifies that copy.

**Verification: verified (full text).** Inspected abstract, Section 3.1–3.3, and Section 5, pp. 566, 570–572, 574–575.

**Model.** Many risk-neutral speculators receive private and common signals.
They choose orders within $[-1,1]$ and optimally select an endpoint away from indifference.
A price-sensitive supply curve contains a normal shock. A capital provider then uses price and its private signal.
Section 3 places trade at date 0, investment at date 1, and payment at date 2.

**Relevant result and evidence.** Feedback creates a motive to coordinate trade, alongside the usual adverse price effect.
The desirable amount of coordination and the private coordination incentive can conflict.
Section 3: “At date 0, speculators trade”.
Section 3.2: “buy or sell up to a unit”.
Abstract: “they coordinate exactly when it is undesirable”.
Section 3.3: “a continuous function”.

**Formal details.** The stated solution restricts attention to a linear monotone equilibrium.
Section 3.2 explicitly discusses several trade rounds as a more complex alternative, rather than its implemented model.
The inspected passages do not fix a unique investor action at indifference or the project's challenger tie rule.
Off-path restrictions remain unverified.

**What this team can use — open.** C.4 and C.6 can use feedback as a source of strategic complementarity.
C.1 can compare bounded orders with optimal endpoint orders.
Neither endpoint orders nor three calendar dates make this the finite-flow, two-round model needed for C.2.

### 3.9 Rank 9 — Daniel and Hirshleifer (2018)

**Record.** Kent D. Daniel and David Hirshleifer. 2018. “A Theory of Costly Sequential Bidding.”
*Review of Finance* 22(5), 1631–1665.

**URLs read.** [Author: abstract](https://sites.uci.edu/dhirshle/abstracts/a-theory-of-costly-sequential-bidding/).
[Author: published bibliography](https://sites.uci.edu/dhirshle/publications/).
[Publisher-supplied record](https://ideas.repec.org/a/oup/revfin/v22y2018i5p1631-1665..html).

**Verification: verified (abstract only).** The author bibliography confirms the journal version, rather than the older manuscript year.

**Model.** A private-value English auction has a cost to submit or revise a bid.
Every bidder can send a signal through a jump bid.
The model concerns a sequence of auction offers.

**Relevant result and evidence.** Repeated jumps persist even as bid costs approach zero.
Offers can communicate information quickly; initial delays can also communicate information.
Author abstract: “costly to submit or revise a bid”, “bidding occurs in repeated jumps”, and “informative delays in the start of bidding”.

**What this team can use — open.** C.7 can distinguish a cost per revised bid from a sunk preparation cost.
C.3 and C.4 can distinguish information in a delay from information in a stock price.
Do not substitute a jump-bid cost for preparation without a new specification.

### 3.10 Rank 10 — Boleslavsky, Kelly, and Taylor (2017); existing record A7

**Verification: verified (full text), by reference.** This status concerns the author manuscript dated 1 February 2017.
Read the published bibliography, manuscript URL, and exact extracts in [A7](../../alex_meeting_2026_10_21/memos/LIT_extracts.md#a7-boleslavsky-kelly-and-taylor-2017).

**Model and relevant result.** A7 verifies continuous orders and a real policy response.
Its price-only extension requires random prices in the specified region.
The published-version equivalence beyond the recorded manuscript remains unverified.

**What this team can use — open.** C.8, C.9, and C.10 can use its distinction between posterior transmission and exact flow recovery.
This source cautions against a deterministic price rule imposed without an existence argument.
It is not a verified two-round discrete model.

### 3.11 Rank 11 — Eső and Szentes (2007)

**Record.** Péter Eső and Balázs Szentes. 2007.
“Optimal Information Disclosure in Auctions and the Handicap Auction.” *Review of Economic Studies* 74(3), 705–731.
DOI: 10.1111/j.1467-937X.2007.00442.x.

**URL read.** [Oxford institutional record and abstract](https://ora.ox.ac.uk/objects/uuid:ace6b193-2788-417e-b331-3b72c0be23ed).
Its rights note gives the definitive journal citation.

**Verification: verified (abstract only).** The repository offers a manuscript; its complete text was not read here.

**Model.** Buyers initially know estimates of their private values.
The seller can release further signals without observing those signals.
A handicap auction places the buyer's premium choice before information release and later bids.

**Relevant result and evidence.** The optimal mechanism makes all feasible information available under the paper's assumptions.
The abstract states “release, without observing”, “all the information that she can”, and “each buyer picks a price premium”.
It also states “a menu of European call options” for the single-buyer implementation.

**What this team can use — open.** C.10 can change what buyers learn before they commit to payments.
C.8 must distinguish ex ante mechanism commitment from a reserve chosen after price.
This is an information-design precedent. It is not a stock-price or toehold model.

### 3.12 Rank 12 — Bulow, Huang, and Klemperer (1999)

**Record.** Jeremy Bulow, Ming Huang, and Paul Klemperer. 1999. “Toeholds and Takeovers.”
*Journal of Political Economy* 107(3), 427–454. DOI: 10.1086/250068.

**URL read.** [Publisher: record and abstract](https://www.journals.uchicago.edu/doi/abs/10.1086/250068).

**Verification: verified (abstract only).**

**Model.** A potential acquirer owns part of the target before the takeover auction.
The abstract compares the role of that toehold under common and private values.
It also discusses terms that the target can choose.

**Relevant result and evidence.** A toehold can strongly affect the winner and price in a common-value contest.
Abstract: “an enormous impact in”, “common‐value”, and “helps a buyer win an auction, sometimes very cheaply”.
It also discusses “selling a cheap toehold or options”.

**What this team can use — open.** C.10 can let the challenger own target shares before it bids.
C.5 must distinguish a bidder's toehold from an outside investor's passive stake.
The toehold changes auction incentives; a stake-only adjustment to trade profit does not capture that change.
The abstract does not verify an endogenous purchase or disclosure stage.

### 3.13 Rank 13 — Grenadier (1999)

**Record.** Steven R. Grenadier. 1999. “Information Revelation Through Option Exercise.”
*Review of Financial Studies* 12(1), 95–129.

**URL read.** [Author institution: complete citation and abstract](https://www.gsb.stanford.edu/faculty-research/publications/information-revelation-through-option-exercise).

**Verification: verified (abstract only).**

**Model.** Several parties hold real options and possess private information.
They can infer information from other parties' exercise decisions.
The model makes option exercise a strategic information event.

**Relevant result and evidence.** Option exercise can generate endogenous information cascades.
Abstract: “infer the private signals of other agents through their observed exercise strategies”.
It describes “informational cascades” that “may arise endogenously”.

**What this team can use — open.** C.3 and C.4 can let preparation or delay reveal private information.
This source joins real options and social inference.
The verified passage concerns observed exercise, rather than learning from an equilibrium stock price.

### 3.14 Rank 14 — Bikhchandani, Hirshleifer, and Welch (1992)

**Record.** Sushil Bikhchandani, David Hirshleifer, and Ivo Welch. 1992.
“A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades.”
*Journal of Political Economy* 100(5), 992–1026. DOI: 10.1086/261849.

**URLs read.** [Publisher: complete record and abstract](https://www.journals.uchicago.edu/doi/10.1086/261849).
[Author bibliography](https://sites.uci.edu/dhirshle/publications/) confirms the title and pages.

**Verification: verified (abstract only).**

**Model.** People act in sequence and observe earlier actions.
Each person also has private information.
Earlier actions can dominate that person's own information.

**Relevant result and evidence.** The definition concerns information ignored after public action histories.
Publisher abstract: “without regard to his own information”.
The same abstract identifies “fragility of mass behaviors”.

**What this team can use — open.** C.4 must identify the entrant's private signal before it claims a cascade.
A sequence of responses to one common public posterior does not by itself establish this definition.
The abstract supplies no auction pricing or feedback theorem.

**Record caution.** The inspected RePEc record alters one title preposition and reverses the abstract's private-information condition.
The publisher and author bibliography establish the title above. This memo uses the publisher's abstract.

### 3.15 Rank 15 — Aretz, Ilyas, and Kankanhalli (February 2026 version)

**Record.** Kevin Aretz, Hassan Ilyas, and Gaurav Kankanhalli. 2026, February version.
“Technological Progress, Managerial Learning, and the Investment-Stock Price Sensitivity.” Working paper.
No journal, volume, issue, or journal pages apply to the version identified on the author page.

**URL read.** [Author: current paper summary and version date](https://www.kevin-aretz.com/working-papers).
The page uses the title above. The inaccessible external record's title and page count remain unverified.

**Verification: verified (abstract only).** This label covers the author summary and version record; the model's complete text remains unverified.

**Model.** The summary describes a real-options framework.
Managers learn about new technology from installed assets and stock prices.
The empirical analysis relates investment sensitivity to the time since the last capacity purchase.

**Relevant result and evidence.** The summary reports more sensitivity as that elapsed time rises.
Author summary: “a real-options framework”, “installed assets and stock prices”, and “rise with the time since they last acquired new capacity”.

**What this team can use — open.** This is a direct source lead for C.3's link between real options and price information.
Read the model before a claim about an optimal delay threshold or endogenous price formation.
The abstract-level evidence does not verify a takeover mechanism or a discrete equilibrium.

### 3.16 Rank 16 — Banerjee and Breon-Drish (2022)

**Record.** Snehal Banerjee and Bradyn Breon-Drish. 2022. “Dynamics of Research and Strategic Trading.”
*Review of Financial Studies* 35(2), 908–961.

**URLs read.** [Author: publication record](https://snehalbanerjee.github.io/).
[Publisher-supplied abstract and record](https://ideas.repec.org/a/oup/rfinst/v35y2022i2p908-961..html).

**Verification: verified (abstract only).** The publisher page returned an access challenge; the deposited abstract supplies the result below.

**Model.** A strategic trader chooses costly research over time.
Research can fail to produce private information.
Research responds to market conditions.

**Relevant result and evidence.** More frequent public disclosures can encourage private information acquisition.
Abstract: “the trader performs costly research” and “does not always succeed”.
It states “more frequent public disclosures can” “crowd in” “private information acquisition”.

**What this team can use — open.** C.2, C.3, and C.6 can distinguish a research delay from a preparation delay.
The verified abstract supplies no subsequent corporate action that changes the traded payoff.
Pair this dynamic-research lead with the feedback mechanism in existing A3; do not assume their combination is already solved.

### 3.17 Rank 17 — Edmans, Goldstein, and Jiang (2015); existing record A1

**Verification: verified (full text) for the recorded main-text stake passage, by reference.** Appendix B.2 remains unverified.
The bibliography, URLs, and extracts are in [A1](../../alex_meeting_2026_10_21/memos/LIT_extracts.md#a1-edmans-goldstein-and-jiang-2015--initial-stake).

**Model and relevant result.** A1 verifies how an initial stake changes incentives in a corrective-action model.
It preserves the recorded trade asymmetry under the source's assumptions.
It does not establish the same stake result when the real action instead increases payoff sensitivity to quality.

**What this team can use — open.** C.1 and C.5 can compare a passive stake with a stock position chosen through earlier trade.
Use the main-text result within its stated scope. The unread appendix cannot support exact new thresholds.

### 3.18 Rank 18 — Goldstein and Yang (2019)

**Record.** Itay Goldstein and Liyan Yang. 2019. “Good disclosure, bad disclosure.”
*Journal of Financial Economics* 131(1), 118–138. DOI: 10.1016/j.jfineco.2018.08.004.

**URL read.** [Publisher: complete record, abstract, and introduction](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18302241).

**Verification: verified (abstract only).** The introduction was also inspected; the complete model remains unverified.

**Model.** A real decision maker learns from a market price under several dimensions of uncertainty.
Public disclosure changes the information in that price.
The result depends on what the decision maker already knows.

**Relevant result and evidence.** Better public information can worsen real efficiency if it displaces useful price information.
Abstract: “disclosure negatively affects price informativeness”.
For a variable already well known to the decision maker, the abstract states “disclosure always improves price informativeness and real efficiency”.

**What this team can use — open.** C.10 can make target disclosure specific to a known or an unknown dimension.
C.8 should compare the induced price experiment as well as the reserve.
The paper's disclosure result does not establish either sign for this project's entry probability.

### 3.19 Rank 19 — Foucault and Gehrig (2008)

**Record.** Thierry Foucault and Thomas Gehrig. 2008.
“Stock price informativeness, cross-listings, and investment decisions.” *Journal of Financial Economics* 88(1), 146–168.
DOI: 10.1016/j.jfineco.2007.05.007.

**URL read.** [Publisher: complete record, abstract, and introduction](https://www.sciencedirect.com/science/article/abs/pii/S0304405X08000202).

**Verification: verified (abstract only).** The introduction was also inspected; the complete model remains unverified.

**Model.** Managers learn about growth opportunities from stock prices.
A cross-listing expands the information available from markets.
Managers then adjust the amount invested.

**Relevant result and evidence.** Better price information improves investment and can generate a cross-listing premium.
Abstract: “more precise information about the value of their growth opportunities” and “make better investment decisions and trade at a premium”.

**What this team can use — open.** C.10 can distinguish more price signals from more precise individual signals.
This helps explain the economic value of price access in C.3.
The verified passages do not establish an option to wait or several sequential trade rounds.

### 3.20 Rank 20 — Luo (2005)

**Record.** Yuanzhi Luo. 2005. “Do Insiders Learn from Outsiders? Evidence from Mergers and Acquisitions.”
*Journal of Finance* 60(4), 1951–1982. DOI: 10.1111/j.1540-6261.2005.00784.x.

**URL read.** [Publisher: complete record and abstract](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2005.00784.x).
The full-text address redirected to that abstract.

**Verification: verified (abstract only).**

**Model or design.** This is empirical evidence about announced mergers and acquisitions.
The analysis relates the announcement response to later completion.
It examines circumstances in which cancellation or new market information makes learning more useful.

**Relevant result and evidence.** Market reactions predict completion; the paper interprets its evidence as learning by the firms.
Abstract: “market reaction”, “predicts whether the companies later consummate the deal”, and “extract information from the market reaction”.
The abstract also states “when canceling the announced deal is easier”.

**What this team can use — open.** C.3 can motivate a reversible decision before a final commitment.
C.10 can distinguish completion after announcement from discovery of a new bidder before preparation.
This evidence supplies no discrete trading theorem or identified effect of incumbent strength in this project.

### 3.21 Rank 21 — Chen, Goldstein, and Jiang (2007)

**Record.** Qi Chen, Itay Goldstein, and Wei Jiang. 2007.
“Price Informativeness and Investment Sensitivity to Stock Price.” *Review of Financial Studies* 20(3), 619–650.

**URLs read.** [Author institution: abstract](https://business.columbia.edu/faculty/research/price-informativeness-and-investment-sensitivity-stock-prices).
[Publisher-supplied bibliography](https://ideas.repec.org/a/oup/rfinst/v20y2007i3p619-650..html).
The latter fixes the author order, singular “Price”, and issue omitted or altered in the institutional display.

**Verification: verified (abstract only).**

**Model or design.** This is an empirical study of investment sensitivity to stock price.
The two price-information measures are price nonsynchronicity and probability of informed trade.
The analysis includes controls for managerial information and distinguishes capital constraints.

**Relevant result and evidence.** Greater measured private information is associated with greater investment sensitivity.
Institutional abstract: “price nonsynchronicity and probability of informed trading (PIN)” and “a strong positive effect”.
It also states “both the learning channel and the alternative channel contribute”.

**What this team can use — open.** C.3 and C.10 can motivate a real decision that responds to informative prices.
The mechanism should distinguish information from financing conditions.
This is general investment evidence; it does not directly establish takeover entry or an option to delay preparation.

### 3.22 Rank 22 — Bond, Edmans, and Goldstein (2012)

**Record.** Philip Bond, Alex Edmans, and Itay Goldstein. 2012. “The Real Effects of Financial Markets.”
*Annual Review of Financial Economics* 4, 339–360. The publisher assigns no separate numeric issue.
DOI: 10.1146/annurev-financial-110311-101826.

**URL read.** [Publisher: complete record and abstract](https://www.annualreviews.org/content/journals/10.1146/annurev-financial-110311-101826).

**Verification: verified (abstract only).**

**Model or design.** This is a review of theory and empirical evidence on real effects of secondary markets.
It distinguishes useful information for a real choice from forecasts of security cash flows.
It discusses how feedback changes price formation and private trade incentives.

**Relevant result and evidence.** Price forecast accuracy alone need not measure the information useful for real decisions.
Abstract: “information that is useful for the efficiency of real decisions” and “rather than the extent to which they forecast future cash flows”.

**What this team can use — open.** C.2–C.10 should state the real outcome as well as the information statistic.
Use this review for the conceptual frame. Use the individual papers above for specific model claims.

### 3.23 Ranked implications for the menu

All transfers below have status **open**. The source ranks above distinguish relevance from access depth.

- **C.1:** Start with existing A2 and A1. GOY adds endpoint orders, but its aggregate noise is continuous.
- **C.2:** Existing A2 is the verified discrete, two-date benchmark. Khanna–Mathews Section 4 is an additional dynamic lead.
- **C.3:** Distinguish a preparation option, a research option, and an option to cancel an announced acquisition.
  Aretz–Ilyas–Kankanhalli, Banerjee–Breon-Drish, Grenadier, and Luo address different parts of that distinction.
- **C.4:** Use Bulow–Klemperer for costly sequential entry. Use Bikhchandani–Hirshleifer–Welch and Grenadier only after private information enters the observed decision.
- **C.5:** Use existing A2 and A1, then Khanna–Mathews. State who owns the initial position and who makes the real choice.
- **C.6:** Existing A3 is the direct feedback source. Banerjee–Breon-Drish adds the research time dimension.
- **C.7:** Fishman supplies preemption through costly information. Daniel–Hirshleifer supplies repeated jump offers with bid costs.
- **C.8:** Bond–Goldstein supplies policy commitment logic. Eső–Szentes supplies ex ante information and payment design.
- **C.9:** Existing A7 supplies endogenous action randomization and price implementation cautions.
  Its continuous model does not prove a mixed discrete equilibrium.
- **C.10:** Use Bulow–Huang–Klemperer for bidder ownership and Eső–Szentes for information release.
  Bond–Goldstein and Goldstein–Yang show why the content of disclosure matters.

## 4. What it recovers or loses relative to the Laplace paper

**Open.** No cited result establishes the paper's full comparison for either discrete base model.

- **Proposition 1:** The auction payment identity remains this project's object. A feedback citation does not derive it.
- **Proposition 2:** Additional dates, price information, or sequential entry do not establish the competition-induced entry reversal.
- **Proposition 3:** Existing A2 and A3 provide distinct sources of multiplicity.
  Neither transfers the paper's coexistence certificate to discrete orders.
- **A.3–A.4:** A matched information experiment and a no-trade cutoff require this project's own deviation analysis.
- **A.5–A.7 and Section 5:** Normal noise, several signals, and continuous orders do not establish the relevant discrete robustness claims.
- **A.8–A.9 and Section 6:** Auction revenue, investment efficiency, and net acquisition surplus are different objectives.
  Bulow–Klemperer makes the revenue–efficiency distinction especially useful.
- **A.10 and Section 6.3:** Existing A7 and Bond–Goldstein–Prescott caution against an unproved inference or price implementation step.
  A reserve chosen after price requires a continuation specified after each reserve choice.

The main candidate-list qualification concerns timing, not a false theorem in the brief.
Bond–Goldstein–Prescott, Bond–Goldstein, and GOY do not implement several trade rounds in the verified baseline sections.
GOY allows continuous bounded orders and obtains endpoint choices. Its continuous supply shock still differs from finite three-point noise.
The existing A7 record already excludes a discrete interpretation of that source.

## 5. Numerical example

No numerical experiment forms part of this literature review. No script was necessary.
The literature does not verify the candidate parameter window, entry path, ownership figure, or profit figures in brief Section 0.
Those claims remain with workstream B.

## 6. Open issues

1. Obtain complete texts for the abstract-only auction, takeover, real-options, and dynamic-research sources before their formal details enter a specification.
2. Read the current Aretz–Ilyas–Kankanhalli model before a claim about an optimal delay rule.
3. Read Khanna–Mathews Section 4 in full before a claim about its complete two-round equilibrium or its noise support.
4. State what a later challenger learns from an earlier decision beyond the public price.
5. Specify inventory across dates, price observation, and all continuation actions before a two-round deviation proof.
6. Specify a seller's commitment timing before use of information-design results for C.8 or C.10.
7. Preserve the version and appendix limits of existing A1 and A7.

**Access record.** Several publisher pages displayed access challenges. Institutional pages and deposited abstracts supplied the stated alternatives.
The full-text address for Luo returned only its abstract. No login or saved paper download formed part of this review.
Four pre-existing pages remained outside the review. Only the separate review page was used and then closed.

**Brief claims refuted.** No quantitative claim from brief Section 0 was evaluated or refuted here.
The source list does require the timing qualifications in Section 4.
Daniel–Hirshleifer's published record is 2018, not the year of its earlier manuscript.

## 7. Plain summary

Goldstein and Guembel remains the closest source for two discrete trade rounds before a real decision.
Its verified record already exists. It supplies a useful structure, not a ready takeover extension.
Earlier positions change later incentives, and direct flow observation differs from price observation.

Dow, Goldstein, and Guembel remains the closest source for costly information with feedback.
Banerjee and Breon-Drish adds dynamic research, but its verified abstract does not establish feedback through a later corporate action.

Fishman explains high initial takeover offers when a rival still faces an information cost.
Bulow and Klemperer compares costly sequential entry with an auction.
Daniel and Hirshleifer explains repeated jump offers when each bid costs money.
These sources describe different costs and decisions.

Khanna and Mathews is a strong additional lead for stakes and manipulation.
Its Section 4 preview adds an earlier trade round. The full dynamic equilibrium remains unread.

The real-options sources also differ.
Grenadier studies information from other parties' exercise decisions.
Aretz, Ilyas, and Kankanhalli directly links a real-options framework to information from stock prices, but only its current summary is verified.
Luo studies completion after a deal announcement, rather than discovery of an unprepared rival.

Disclosure and seller policy need their own timing rules.
Eső and Szentes studies information release within a committed auction mechanism.
Bond and Goldstein and Goldstein and Yang show why disclosure can change the information that prices provide.

The recommended sequence is two trade rounds, then endogenous research, then preemption or disclosure.
Every transfer requires a new equilibrium argument. No literature citation settles the discrete-Laplace numerical claims.
