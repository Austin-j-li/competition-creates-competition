# Structural candidates for the job-market paper

30 October 2026. Independent research assessment. Ordinary web search was available and used. No browser, extraction, estimation, code, or tests ran.

## 1. Longlist

Scores follow the fixed rubric: originality (O), importance (I), practicality (P), and placement power and fit (F). Each score ranges from zero to ten. The weights remain 30, 25, 25, and 20. All proposed findings are research hypotheses.

1. **The Price of a Final Deadline** — O 8.5; I 9; P 7; F 9; structural **yes**. Estimate bidder values, preparation duration, delay costs, and the target's cost of another round. Use offers, extension requests, late acceptance, and exits. Compare discretionary extensions with a credible final deadline. HMC fits a finite game; endogenous deadlines and sample selection are hard.
2. **The Right to Return: Standstills and Takeover Competition** — O 8; I 8.5; P 6.5; F 8.5; structural **yes**. Estimate values, preparation costs, value updates, and the option to return. Use NDA refusals, early offers, waivers, and later bids. Compare automatic release at agreement signature with continued restrictions. HMC is feasible after discrete states are integrated out; missing contract terms threaten identification.
3. **Competition by Message: What Targets Tell Their Bidders** — O 8.5; I 8.5; P 5.5; F 8.5; structural **yes**. Estimate values, continuation costs, and bidders' information about rival offers. Use dated messages, subsequent offers, and continued participation. Compare selective messages with common disclosure of rival activity. HMC faces a game of strategic disclosure, incomplete messages, and possible multiple equilibria.
4. **Too Busy to Bid: Capacity in the Market for Corporate Control** — O 8.5; I 8.5; P 4; F 8; structural **no at present**. Candidate primitives are diligence capacity and its opportunity cost. Concurrent assignments, refusals, and participation would supply moments. A staggered sale calendar is the counterfactual. Anonymous bidders prevent a reliable workload measure. HMC cannot repair that missing link.
5. **Who Never Gets Called? The Target's Choice of Potential Buyers** — O 5.5; I 8.5; P 5.5; F 8; structural **yes**, with a defined buyer population. Estimate contact costs and target information about buyer fit. Contacts, refusals, and offers identify a restricted search model. Compare broader solicitation with current outreach. HMC is feasible; the unobserved buyer population and existing research weaken this candidate.
6. **Paid to Close: Adviser Fees and Lost Competition** — O 6.5; I 8.5; P 4.5; F 7; structural **no at present**. Candidate primitives are adviser incentives and the board's control over search. Fee schedules, outreach, and sale duration supply moments. Compare success fees with fees tied to incremental proceeds. Advice remains hidden, so preferences and delegation are not separately identified. HMC is premature.
7. **A Coalition or a Cartel? Joint Bids in Takeover Sales** — O 7; I 8.5; P 5; F 8; structural **yes**, conditional on member histories. Estimate financing capacity, complementary values, and coalition costs. Independent offers, group formation, and joint offers supply moments. Compare unrestricted groups with a ban on combinations between existing bidders. HMC faces discrete coalition choices and scarce independent counteroffers.
8. **The Cost of a Public Sale** — O 7; I 8.5; P 5.5; F 8.5; structural **yes**, conditional on disclosure identification. Estimate buyer awareness, entry costs, and the target's cost of publicity. Public announcements, new contacts, and offers supply moments. Compare mandatory early disclosure with seller discretion. HMC is feasible for a small model; endogenous disclosure and missing abandoned sales are hard.
9. **Why Companies Return to the Sale Market** — O 7.5; I 8; P 4; F 7.5; structural **no at present**. Candidate primitives are target outside options, persistent values, and the cost of renewed search. Pauses, restarts, and repeated offers supply moments. Compare immediate continuation with a pause. Failed efforts without later merger filings lack full histories. HMC would estimate assumptions about those missing efforts.
10. **Competition Creates Competition** — O 8; I 8; P 6; F 7.5; structural **no for the current paper**. Its primitives concern rival quality, preparation costs, and informed trade. Identification requires entry decisions and a prespecified order measure. Price-access restrictions provide a counterfactual. A credible structural likelihood does not yet exist. HMC is not the current constraint.

Two verified overlaps change the ranking. Gentry and Stroup already estimate entry uncertainty and compare auctions, sequential negotiations, and go-shops. Kim and Zheng already estimate the information and operation costs of additional invitations. A larger sample alone cannot distinguish either candidate. See [Gentry and Stroup (2019)](https://corpgov.law.harvard.edu/2019/05/07/entry-competition-in-takeover-auctions/) and [Kim and Zheng, February 2018 draft](https://cdn.vanderbilt.edu/t2-my/my-prd/wp-content/uploads/sites/2637/2017/10/JMP_20180205.pdf).

The supervision overlap is now more precise. The verified March 2026 draft of *Deal Terms in Takeovers* studies formal offers and target valuations of diligence, exclusivity, financing, and regulatory conditions. It uses 673 completed US mergers from 2015–2021. These pitches therefore center on process commitment and bidder information. They do not estimate target discounts for those offer conditions. See [Gorbenko, Green, and Mirani (2026), abstract and Sections 1–2](https://www.brettgreen.info/drafts/deal_terms.pdf).

The joint informal-bids paper estimates the bid wedge and admission cutoff. These candidates instead estimate target continuation, future access, or bidder information. Every likelihood must address selection into the population with a qualifying filing. Counterfactuals hold that target population fixed; they do not identify effects on undisclosed sale attempts. HMC can compute a posterior, but it cannot supply identification.

## 2. Top three pitches

### 1. The Price of a Final Deadline

**Question:** Does a target lose competition because bidders expect another chance after its supposedly final deadline?

**Why business schools care:** Boards face a conflict between today's best offer and tomorrow's possible challenger. Another round can improve today's sale. Yet anticipated extensions can make every earlier round less competitive. The paper prices the target's ability to end its auction. That object matters to boards, advisers, and courts that assess the adequacy of a sale process.

**The new fact or result:** The intended result separates a productive extension from the cost that expected extensions impose before they occur. A target might gain from each observed extension yet lose from its inability to refuse extensions. The empirical contribution must connect that anticipation to initial offers and costly preparation. A count of soft deadlines alone cannot carry the paper.

**Model:** Use a finite game with an initial solicitation, a final solicitation, and at most one extension. Bidders choose whether to prepare, when to submit, and what to offer. Preparation requires a private cost and a random completion time. The target sees submitted offers and extension requests, then chooses whether to continue. Bidders anticipate that choice.

Estimate value distributions, preparation costs and duration, target delay costs, and the cost of another solicitation. Treat target urgency and target quality as correlated latent characteristics. Keep non-price offer attributes fixed within a narrow initial sample.

**Data:** Start with cash offers in US public-target processes from 2005–2026. Require dated final solicitations and enough subsequent text to identify what the target did. Build on the [sale-process instruction](/home/uctpiaj/work/Projects/sec-auction/SEC_Deal_Ledger_Extraction_Instruction.md). Add bidder-specific deadline messages, requests for extra time, and explicit acceptance of late offers. Link SDC outcomes and CRSP prices.

Preserve approximate dates as intervals. The existing instruction infers some non-submissions and exits from deadlines. Those labels cannot serve as independent evidence of strategic delay.

**Identification:** Use the joint likelihood of initial offers, submission times, requests, extensions, subsequent offers, and explicit exits. Bid levels and revisions discipline values; documented diligence progress and requested time discipline preparation duration. Stop-or-continue decisions at comparable leading offers discipline target delay costs. Initial choices under the announced procedure discipline the anticipated continuation rule.

Identification requires a restricted preparation technology and a finite target objective. Do not claim that timestamps alone separate strategic delay from slow diligence. Deadline length, adviser identity, and target distress are endogenous variables, not automatic instruments. Include filed transactions that later fail where their histories exist. Estimate effects for processes within that disclosure population; market-wide failure effects require a broader sample.

**Structural flag:** **Yes.** Compare the estimated discretionary process with a deadline that binds under the model, at the same initially announced date. Also compare an extension rule announced before preparation with an extension chosen after offers arrive. Report target proceeds, preparation expenditure, duration, and allocation. The binding deadline is an economic benchmark, not a claim about current fiduciary law.

JAX or Stan can handle a short game with smooth private shocks. Integrate discrete choices and date intervals out before NUTS. The main computational task is a differentiable equilibrium solution. Additional rounds and unrestricted private histories would make the project too large.

**The question no one else with the same data would ask:** How much does the option to reopen an auction cost the target before it ever exercises that option?

**Closest papers:**

- [Chen and Wang (2023), *Optimal Sequential Selling Mechanism and Deal Protections in Mergers and Acquisitions*, JF](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13235). They characterize optimal sale procedures. This paper estimates the loss from a target's inability to maintain its announced procedure.
- [Gentry and Stroup (2019), *Entry and Competition in Takeover Auctions*, JFE](https://corpgov.law.harvard.edu/2019/05/07/entry-competition-in-takeover-auctions/). Their central object is entry uncertainty. Here, bidders anticipate endogenous continuation after an announced final round.
- [Liu, Officer, and Tu (December 2023 draft), *Negotiation, Auction, or Negotiauction?! Evidence from the Field*](https://www.aeaweb.org/conference/2024/program/paper/rntssT5k). They document fluid procedures and offer sequences. This paper identifies the economic cost of that discretion.
- [Calcagno and Falconieri (2014), *Competition and the Dynamics of Takeover Contests*, JCF](https://openaccess.city.ac.uk/id/eprint/6054/). They model negotiation with an auction option. This paper estimates anticipated deadline revision and costly bidder preparation.

**Main risk and kill test:** The apparent mechanism might consist entirely of diligence delays and retrospective disclosure conventions. First review 50 varied filings directly. Seek explicit final messages, bidder requests, and decisions about late offers, including offers that the target refuses to consider. Kill the idea if those events cannot be separated or if a model without strategic delay explains their joint pattern. Also stop if commitment and urgency remain observationally equivalent under reasonable value distributions.

**Timeline to fall 2029:**

- February–June 2027: Complete the source review. Fix the short game and sample rules.
- 2028 Q1–Q3: Finish the reviewed sample. Obtain first estimates and counterfactuals.
- December 2028–August 2029: Complete the draft. Resolve seminar objections and fix the market version.

### 2. The Right to Return: Standstills and Takeover Competition

**Question:** Does the prospect of a later bid discourage early effort enough to justify restrictions on bidders' right to return?

**Why business schools care:** A bidder can pay for diligence now or wait until another buyer reveals a price and a completed agreement. The right to wait can undermine an early auction. Restrictions can also silence the buyer with the highest later value. The paper compares both effects within the same sale. It asks when a restriction on competition actually buys competition at an earlier stage.

**The new fact or result:** The intended result measures how later access changes early participation, early offers, and the quality of later challengers. The central comparison starts before bidders sign their NDAs. A waiver can increase later bids while an anticipated waiver reduces early effort. The paper must estimate the net effect rather than treat later challenges as the full benefit.

**Model:** A bidder first chooses whether to sign an NDA and prepare an offer. It can instead retain the option to approach later with less private information. An early participant learns about its own value. Values can also change before a later challenge. The target chooses an initial restriction and later decides whether to release it where permitted.

Separate a private waiver request, permission to submit a proposal, and an automatic release event. An outsider that never signs an NDA keeps its existing rights. Estimate value distributions, preparation costs, the precision of diligence, later value updates, and waiver costs. Start with two bidder types and two opportunities to bid.

**Data:** Use the census of public-target processes, with SDC and CRSP links. Add a source review of NDA restrictions, duration, release events, waiver requests, and the rights that survive agreement signature. The present ledger does not contain dedicated standstill fields. Its silence cannot establish an unrestricted NDA. Count prospective bidders that decline an NDA where reported.

Distinguish previous participants from new challengers. Code factual contract content separately from any assessment of enforceability. A usable sample needs terms known before preparation and evidence about later rights. It cannot contain only disputes that produced litigation.

**Identification:** Jointly use NDA acceptance, early offers, announced release terms, waiver decisions, and later challenges. Early participation and offer distributions discipline preparation costs and the value of future access. Changes within the same bidder's offer history discipline value updates, conditional on its selection into a later bid. Automatic release clauses separate contractual eligibility from a target's discretionary invitation. They remain endogenous choices and enter the likelihood as such.

Terms fixed before unexpected public developments provide more useful variation than retrospective waivers alone. A target's weaker initial offers can themselves cause a waiver. The model must allow that feedback. Rare challenges will identify only a restricted update distribution; a flexible tail cannot come from a prior alone.

The 2012 Delaware decisions supply institutional variation worth a first source review. They do not supply a clean universal ban. The *Ancestry.com* transcript expressly rejects that interpretation and discusses a possible commitment benefit. See the [court transcript, printed pages 223–226](https://www.rlf.com/wp-content/uploads/2020/05/6454_In-re-Ancestry.com_.pdf). Any legal design must distinguish changes in disclosure from changes in restrictions.

**Structural flag:** **Yes.** Compare automatic release when a merger agreement is signed, a guaranteed right to request a private waiver, and continued restrictions. Let bidders change their early entry and offers in every counterfactual. Estimate target proceeds, preparation costs, and allocation; do not infer consumer welfare from acquisition values.

A finite game with latent bidder values fits Austin's HMC tools. Integrate discrete eligibility and participation states out. The hard problems are endogenous contract choice, missing terms, and the low frequency of later challenges. No model of financing conditions or target discounts for exclusivity belongs in the initial paper.

**The question no one else with the same data would ask:** What does a target gain today when a bidder gives up the right to wait for tomorrow?

**Closest papers:**

- [Sautter (2013), *Auction Theory and Standstills: Dealing with Friends and Foes in a Sale of Corporate Control*](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2445056_code538190.pdf?abstractid=2207693&mirid=1). This article already develops the early-bid versus later-competition trade-off. The new contribution must be its structural measurement and endogenous NDA participation.
- [Dann and DeAngelo (1983), *Standstill Agreements, Privately Negotiated Stock Repurchases, and the Market for Corporate Control*, JFE](https://www.sciencedirect.com/science/article/abs/pii/0304405X83900144). Their setting concerns substantial shareholders and repurchases. This paper concerns access to private sale information and subsequent bid rights.
- [Chen and Wang (2023), JF](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13235). They explain how optimal protections encourage initial entry. This paper estimates bidder access rights across both stages.
- [Gentry and Stroup (2019), JFE](https://corpgov.law.harvard.edu/2019/05/07/entry-competition-in-takeover-auctions/). Their go-shop comparison establishes a high benchmark. Here, earlier participants and new challengers possess different information and different contractual rights.
- [Gorbenko, Green, and Mirani (March 2026 draft), *Deal Terms in Takeovers*](https://www.brettgreen.info/drafts/deal_terms.pdf). Their offer-level model values non-price conditions. This paper estimates entry before any formal offer and restrictions on later access.

**Main risk and kill test:** The mechanism is known in legal scholarship. Novelty requires a credible quantitative reversal of the policy ranking, or a large measured trade-off. First review 50 ordinary filings across periods, with merger agreements and supplements where necessary. Kill the idea if pre-entry restrictions and release terms remain mostly unknown. Also kill it if observable terms provide no useful separation between early incentives and later exclusion. Resolve the substantive boundary with Alex's joint projects before substantial estimation work.

**Timeline to fall 2029:** Complete the coverage and overlap review by March 2027. Fix the contract taxonomy and model by September 2027. Finish the reviewed sample by June 2028. Complete estimates and policy comparisons by December 2028. Produce the full draft by March 2029. Use spring and summer 2029 seminars for the market revision.

### 3. Competition by Message: What Targets Tell Their Bidders

**Question:** How much takeover competition comes from actual rival offers, and how much comes from what a target tells each bidder about them?

**Why business schools care:** A board controls who gets access and what each bidder learns about the contest. Two identical sets of offers can produce different next offers if bidders receive different messages. Disclosure can raise an existing bidder's offer yet deter a prospective challenger from preparation. The paper would price the target's control over information about competition.

**The new fact or result:** The intended result separates the competitive pressure from a rival's actual offer from the pressure that its disclosure creates. The useful fact is a bidder's response to a documented message about a rival. The useful counterfactual changes that message before the bidder chooses whether to continue. A correlation between bidder counts and premiums cannot establish either object.

**Model:** Use a short contest in which the target observes offers that other bidders do not observe. It can send a truthful message about a rival's presence or a bound on its offer. It can also remain silent. Each recipient updates its beliefs, chooses whether to pay a continuation cost, and submits another offer. The target's message choice is strategic.

Estimate value distributions, continuation costs, target outside values, and a parsimonious prior about hidden competition. Start with verifiable statements and comparable cash offers. Do not add unrestricted bluffing, private target signals, and free message costs to the same model. Those freedoms would absorb almost any observed response.

**Data:** Use contacts, NDA dates, offer histories, and price feedback from the sale-process census. The instruction permits rows for price feedback and differences in bidder information. Add exact recipients, message dates, message content, and the next observable choice. Separate a generic request for improvement from a statement that another offer exists. Distinguish the date a rival submits its offer from the date the recipient learns about it.

A missing message is unobserved communication, not documented silence. CRSP supplies a common valuation benchmark, not bidder beliefs. Start with histories whose communication sequences are explicit.

**Identification:** Use the joint likelihood of target messages, recipients' next offers, continuation choices, and final outcomes. Rival offers elsewhere in the history discipline the truth and content of each statement. Recipients' responses discipline how information changes expected competition. Repeated offers before and after messages help separate persistent bidder values from belief changes. Target decisions about messages must enter the likelihood; message receipt is not random.

Cross-bidder differences in information within one target help absorb common target news. They do not remove selection into messages. Fix a small information structure and require its message and response restrictions to hold jointly. Do not estimate an unrestricted bidder prior separately from an unrestricted disclosure rule. If several belief systems fit equally well and reverse the policy result, the structural claim fails.

**Structural flag:** **Yes**, for a restricted game with observed message content and an explicit equilibrium rule. Compare selective disclosure with a common announcement of the number of bona fide rival offers at a fixed solicitation date. Also compare that rule with continued confidentiality. Let entry and continuation respond. Report target proceeds, preparation expenditure, and allocation. The count rule is a hypothetical process rule, not an interpretation of current disclosure duties.

JAX supports a finite, integrated likelihood; HMC can sample its continuous primitives. The hard work lies in the disclosure equilibrium and the observation process for omitted communications. Full revelation can arise in standard models. The theory must establish why selective disclosure survives before estimation assigns it an economic value.

**The question no one else with the same data would ask:** How much would the target lose if every bidder received the same truthful account of the competition?

**Closest papers:**

- [Ghosh and Liu (2024 draft), *Verifiable Private Disclosure in Auctions*](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4778012_code1233107.pdf?abstractid=4778012&mirid=1). Their baseline can produce full revelation of bidder numbers. This is a direct theoretical obstacle, not merely a related reference. Costly continuation and the timing of messages must supply a distinct empirical mechanism.
- [Lauermann and Wolinsky (2017), *Bidder Solicitation, Adverse Selection, and the Failure of Competition*, AER](https://swlb2.aeaweb.org/articles?id=10.1257%2Faer.20131057). They show that solicitation itself conveys information. This paper uses explicit messages about rival offers after contact.
- [McClellan (2023), *Knowing Your Opponents: Information Disclosure and Auction Design*, GEB](https://www.sciencedirect.com/science/article/pii/S0899825623000404). He studies disclosure of opponent identities and information advantages. This paper estimates target messages about rival activity and the resulting continuation decisions.
- [Gentry and Stroup (2019), JFE](https://corpgov.law.harvard.edu/2019/05/07/entry-competition-in-takeover-auctions/). They recover pre-entry uncertainty. This paper treats the target's information policy as an endogenous source of that uncertainty.
- [Liu, Officer, and Tu (December 2023 draft)](https://www.aeaweb.org/conference/2024/program/paper/rntssT5k). Their offer histories demonstrate that this empirical territory already has detailed data. The contribution must identify the target's control over bidder beliefs.

**Main risk and kill test:** Filings may record offers while omitting the messages that caused them. First review 50 filings for exact message content and recipient-specific subsequent choices. Kill the idea if messages cannot be distinguished from generic price demands. Also kill it if missing communications prevent any credible observation model. Before a large data build, establish whether reasonable disclosure equilibria give the same policy ranking. This candidate ranks third because its information requirements are the least secure.

**Timeline to fall 2029:** Complete the message review by March 2027. Establish a small estimable game by September 2027. Finish the reviewed communication sample by June 2028. Obtain structural estimates by December 2028. Complete a full draft by March 2029. Resolve the equilibrium and missing-message objections before the August 2029 market draft.

## 3. Where CCC fits

CCC is a second paper on the current evidence. Its strongest asset is the reversal: a stronger incumbent can create information that attracts a rival despite lower bidder profits. The structural candidates study target choices that the planned census can observe, while CCC needs informed orders and precisely dated rival preparation. The [manuscript conclusion](/home/uctpiaj/work/Projects/competition-creates-competition/overleaf/slot/sections/09_conclusion.tex) identifies empirical measurement and endogenous sale terms as future work; the census alone cannot identify its price mechanism. Promote CCC only if a separate feasibility review yields observable decisions and distinctive evidence that competing entry models cannot explain. Otherwise, choose the deadline candidate first, subject to its source and identification kill tests.
