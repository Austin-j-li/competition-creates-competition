# Phase 1, data angle (Opus C): job-market paper candidates that start from data

30 October 2026. Web search was available. I ran about 20 standard searches. Each reference below is marked "verified" (a search result confirmed the title, the authors and the main claim) or "unverified" (from memory). WRDS was not used. All counts are in the section "Sample sizes", with the request that produced each count.

Data tiers used below:

- **Tier A:** a pilot can run now on the 404 hand-coded reference deals plus CRSP (to run on WRDS).
- **Tier B:** the idea needs the census of sale processes.
- **Tier C:** the idea needs a source with access not yet checked (TAQ, single-stock options history, Dealscan) or a new extraction field.

## 1. Longlist

Weighted score = (30 × Originality + 25 × Importance + 25 × Practicality + 20 × Placement) / 100. All scores are provisional.

| # | Idea (one line) | Orig. | Imp. | Pract. | Place. | Wtd | Structural | Tier |
|---|---|---|---|---|---|---|---|---|
| 1 | **Every NDA leaks.** Measure the price and volume footprint of each private stage of a sale process, find who pays for the leak, and find whether leaks recruit outside bidders. | 8 | 8 | 6 | 8 | 7.50 | yes | A pilot, B full |
| 2 | **The proxy reveals the auction.** The background disclosure tells the market how much competition was left; test whether prices and later rival bids respond to the revealed runner-up. | 7 | 6 | 8 | 6 | 6.80 | yes | A pilot, B full |
| 3 | **Best and final?** Measure whether sellers keep their own bid deadlines, and estimate what the lack of seller commitment costs in price. | 8 | 6 | 4 | 7 | 6.30 | yes | B |
| 4 | **Bidders who team up.** Two bidders merge into a consortium after the first round; compare the joint bid with each member's own earlier bid to measure the collusion discount. | 7 | 6 | 5 | 6 | 6.05 | yes | B |
| 5 | **The seller's bank and its sponsor clients.** Test whether sell-side advisers narrow the bidder pool toward private equity firms they lend to or work for (stapled finance, repeat relationships). | 6 | 7 | 6 | 5 | 6.05 | no | C |
| 6 | **Should a target say it is for sale?** Compare public and confidential sale processes on NDAs, bids and price. The CCC mechanism is one channel. | 5 | 7 | 6 | 6 | 5.95 | no | B |
| 7 | **Sponsor bids follow credit markets.** Within the private process, estimate how financial and strategic bids load on industry returns and on credit spreads between rounds. | 4 | 6 | 9 | 5 | 5.95 | no | A |
| 8 | **The seller's public voice.** Test whether targets time good public news to the private bid calendar, and whether bids respond. It is the target-side mirror of Ahern and Sosyura (2014). | 5 | 6 | 7 | 5 | 5.75 | no | A/B |
| 9 | **CCC test.** The first-day order imbalance after a public sale disclosure, and later rival entry (CCC extension). | 7 | 6 | 3 | 7 | 5.75 | no | C |
| 10 | **Standstills after the 2012 Delaware rulings.** Use the "don't ask, don't waive" bench rulings as a shock to the power of losers to top the winner. | 7 | 5 | 5 | 5 | 5.60 | no | B |
| 11 | **What sellers show bidders.** Compare management projections in the proxy with analyst consensus and with the bids, as seller information design. | 6 | 6 | 5 | 5 | 5.55 | no | C |

Notes on the cut:

- **Dependence on CCC.** Only idea 9 is a CCC extension. Idea 6 uses the CCC mechanism as one channel. Pitch 1 contains one CCC-type test among four facts. Pitch 2 gives CCC its cleanest empirical test (see section 3).
- **Overlap inside the team.** Idea 3 uses the deadline fields that Alex wants for the joint project; its scope must be agreed with him. Idea 7 touches debt commitments, which is near "Deal Terms in Takeovers". Pitch 2 touches deal protection (termination fees, matching rights), which "Deal Terms in Takeovers" may cover; the content of that paper is unverified.
- **Anonymity.** Filings name the winner and hide the losers. Ideas 4, 5 and 10 need only the winner's identity, the loser types and the links between parties inside one filing. No idea needs a loser's identity.
- **Dropped before the scores.** A structural model of auction against negotiation from background sections repeats Gentry and Stroup (2019) and Gorbenko (2019). Informal-to-formal admission is the joint paper. Private bid revisions that track the target's public price are in Liu and Officer (working paper); idea 7 survives only as the bidder-type split.

## 2. Top 3 pitches

### Pitch 1. Every NDA leaks: who pays when a confidential takeover auction reaches the market

**Question.** When a confidential sale process leaks into the target's stock price, which stage leaks? Who pays: the winner, the shareholders who sell early, or the seller through changed competition?

**Why business schools care.** A large part of the takeover premium appears in the target price before the announcement (Schwert 1996). Insider-trading enforcement centres on takeovers. Sellers choose how many parties to bring under a confidentiality agreement, and bankers weigh "leak risk" against competition with no evidence. The United Kingdom forces a public announcement after a leak; the United States does not (UK Takeover Code rule, unverified). No one can say which rule gives target shareholders more, because no one sees the private clock.

**The new fact.** The paper aligns daily prices, volume and option activity on the dates of private events that the market cannot see. These events are first contacts, each cohort of NDAs, first-round bids, cuts, final bids and exclusivity. The paper gives four facts:

1. a stage profile of leakage;
2. a leak elasticity of breadth: the price drift for each extra party under NDA, by party type (a financial sponsor brings lenders and co-investors);
3. the incidence of a leak: whether later bids rise with the part of the price move that the process itself caused, as distinct from public news;
4. the entry effect: whether new parties contact the target after a dated leak.

**Model.** The seller chooses the number and the type of parties to invite. Each party adds competition and a leak hazard. A leak moves the price toward the expected deal price and reaches outside bidders, who may then enter. Bidders state offers relative to the market price, with a pass-through coefficient. The key primitives are:

- the leak hazard per party type;
- the pass-through of a process-caused price move into the next bid;
- the entry response of outside bidders to a leak;
- the bidder value distributions and the entry costs.

**Data.** Census of sale processes: exact event dates, NDA cohort counts and types, bids by bidder, and one new event tag for press reports and "unusual trading" statements in the background text. CRSP daily data (to run on WRDS). Single-stock options: OptionMetrics if access exists, else ThetaData from mid-2012. TAQ if access exists. SEC insider-trading litigation releases serve as a validation set. Sample: about 5,400 completed public-target sales, 2001 to 2025 (see "Sample sizes"). In the reference set, 69% of event rows carry an exact date. The median confidential window is 223 days.

**Identification.**

- *Stage profile.* The event dates stay private until the proxy. A move on those dates is leakage. Placebos are the same deal on shifted dates and matched firms on the same dates.
- *Leak elasticity.* Within a deal, NDA cohorts sign on different days, so the paper compares the days after each cohort. Across deals, cohort size varies at a given target size and industry.
- *Incidence.* Regress the same bidder's revision, from its first bid to its final bid, on the target's price move over that interval. Split the move into a market and industry part (public news) and a residual. Instrument the residual with leak channels that do not change competition: dated press reports in the interval, and whether options on the target trade. Hold competition fixed with the count of live bidders in the final round.
- *Entry.* Compare the hazard of first contact by new parties just after a dated press report with the hazard just before, within the same process.

**Structural flag: yes.** Estimate the four primitives with a Bayesian likelihood (HMC). Counterfactuals:

1. a UK-style forced announcement after an untoward price move;
2. perfect confidentiality;
3. the seller-optimal number of NDAs with and without leaks.

Each counterfactual reports the change in target shareholder value and the transfer from early sellers of the target stock to informed traders.

**The question no one else with the same data would ask.** On the day the fifth confidentiality agreement was signed, a day the market could not see, did the price move? And did the winner later pay for that move?

**Closest papers.**

- Augustin, Brenner and Subrahmanyam (2019, *Management Science*): informed option trades before 1,859 US takeover announcements, 1996 to 2012, timed from the announcement (verified). This paper times trades from the private stages.
- Fidrmuc and Xia (2022, *European Financial Management*): the legal trades of target insiders change after NDA signatures, 2005 to 2018 (verified). That paper studies insiders' own trades; this paper studies market leakage, its incidence and entry.
- Liu and Officer (working paper, later retitled "Public news, stock-market reactions, and bidding behavior in private merger negotiations"): private bid revisions track the target's market value and its earnings news (verified). This paper separates process-caused leaks from public news and adds entry and process design.
- Betton, Eckbo, Thompson and Thorburn (2014, *Journal of Finance*): public offers reject a costly runup feedback loop (verified). This paper tests the same loop inside private rounds with dated leaks.
- Kacperczyk and Pagnotta (2019, *Review of Financial Studies*): volume and options reveal 3,586 illegal insider trades (verified). This paper supplies the event clock that their tests lack.

**Main risk.** Leaks may cluster at the end of the process (lawyers, boards, lenders), so the stage profile shows one spike. Day-level dates may be too coarse. The incidence instrument may be weak.

**Kill test (four to six weeks).**

1. On the 404 reference deals, compute CRSP abnormal turnover and abnormal returns on exact NDA and bid dates, against shifted placebo dates (run on WRDS). If NDA days and bid days look like placebo days, and the cumulative drift shows no step at cohort dates, drop the stage profile.
2. On the 418 bidders with exact-dated first and final bids (median gap 28 days; revision standard deviation 11.9%), regress the revision on the target residual return. The rough standard error is 0.06. If the pass-through estimate is not distinguishable from both zero and one, the incidence result needs the census before it says anything.

**Timeline.**

- *November 2026 to February 2027:* check access to OptionMetrics and TAQ, run both kill tests and write a five-page memo.
- *March to December 2027:* build the census with exact dates and the press-report tag. Human review covers dates and cohort counts only.
- *January to June 2028:* write the reduced-form facts and a short theory of the seller's breadth choice.
- *July 2028 to May 2029:* run the structural estimation and the counterfactuals.
- *June to September 2029:* finish the draft and present at summer conferences.

### Pitch 2. The proxy reveals the auction: hidden competition after the merger agreement

**Question.** When the merger proxy discloses the confidential auction, does the market reprice the chance of a rival bid? Does the revealed runner-up predict which deals the runner-up later tops?

**Why business schools care.** Delaware courts accept deal protections when a pre-agreement market check took place (unverified). Deal protections are termination fees, matching rights and go-shops. Boards use the same argument. But no one measures how much competition remains after the agreement. Rival bids after the agreement are rare, about 5% of deals by industry counts (Intralinks/Bayes leak reports, verified). The threat of a rival bid still sets the price that arbitrageurs pay. The background section is the mandated disclosure of the process. If it moves prices, it carries information about latent rivals that nothing else carries.

**The new fact.**

1. The filing of the background section is a price event. The target's price relative to the offer, and the option right tail where data exist, move on the filing day.
2. The direction depends on the revealed content. A close runner-up raises the price. A wide market check with few bids lowers it. In the reference set, the median gap between the best bid and the runner-up's last bid is 5.6% of the best bid.
3. The revealed gap predicts rival bids, price bumps and returns of the runner-up after the agreement.

**Model.** The model is a contest after the agreement. The signed bidder holds a matching right and a termination fee. The runner-up knows its value and the target. Unknown rivals arrive at a rate that falls with the breadth of the pre-agreement check. Arbitrage prices equal the offer, times the completion probability, plus the expected value of a rival bid. The key primitives are:

- the runner-up's value distribution, given its last bid;
- the arrival rate of unknown rivals;
- the rival entry cost;
- the deterrent effect of each deal protection.

**Data.** Census fields: the runner-up's last bid, NDA and bidder counts, process type and go-shop terms. EDGAR acceptance time of the first filing with a background (PREM14A, or SC 14D9 for tender offers). CRSP daily prices (TAQ intraday if access exists). Options where available. SDC (to run on WRDS) for rival bids, revised terms and termination fees. Sample: about 5,400 completed sales, plus about 760 candidate deals that filed a preliminary proxy and no definitive proxy (to verify). The main sample keeps cash deals, because the cash offer gives a clean anchor for the price.

**Identification.** The filing date follows the SEC review and the legal calendar, not news. The announced price and the winner are already public. The proxy also discloses management projections and the fairness-opinion value ranges, and these move prices too. So the identifying moment is not the mean reaction. It is the cross-deal slope of the reaction on the runner-up gap and the NDA count, with the projection-implied value against the offer as a control. For tender offers, the SC 14D9 arrives near the announcement, so the main sample is one-step mergers. In the structural step, rival outcomes given the revealed gap identify the runner-up's re-entry. Cross-deal variation in fee size and in go-shop terms identifies deterrence. The price reaction identifies the market's beliefs.

**Structural flag: yes.** Estimate the contest after the agreement. Counterfactuals:

1. no matching right;
2. half the termination fee;
3. a go-shop in place of a pre-agreement auction;
4. disclosure of the background at the announcement.

**The question no one else with the same data would ask.** The market learns from the proxy how hard the runner-up pushed. Does it price that, and is it right?

**Closest papers.**

- Boone and Mulherin (2007, *Journal of Finance*, "How are firms sold?"): competition happens mostly before the announcement (verified title; the details are from memory).
- Liu and Mulherin (2019, *Journal of Applied Corporate Finance*): competition, counted with private auctions, did not fall from 1981 to 2014; 388 deals (verified).
- "An options-based approach to forecast competing bids: evidence for Canadian takeover battles" (IWH working paper; verified title; authors unverified). It infers rival-bid probabilities from prices. It does not use process disclosure.
- Officer (2003, *Journal of Financial Economics*): termination fees (unverified).
- Gorbenko, Green and Mirani ("Deal Terms in Takeovers", working paper): possible overlap on deal protection (content unverified).

**Main risk.** The effect is small. A two-point change in the rival-bid probability, times a 10% bump, moves the price by about 0.2%. A target with a signed deal has a quiet price, so a few hundred deals can detect the effect. The bigger risk is overlap with "Deal Terms in Takeovers".

**Kill test (three to four weeks).**

1. Take the CIK from each EDGAR link in the reference set and find the first PREM14A date in the EDGAR index.
2. On WRDS, compute the target's return relative to the offer over days −1 to +1 around that date.
3. Regress the return on the runner-up gap and the NDA count.

If the mean reaction and the slope are both zero, the idea becomes a footnote. Separately, ask Alex whether "Deal Terms in Takeovers" covers deal protection. A yes kills the structural half.

**Timeline.**

- *November 2026 to January 2027:* the kill test and the overlap check.
- *2027:* add three fields (runner-up last bid, go-shop terms, first filing time) to the census build. These share the Pitch 1 build.
- *2028:* the event study and the rival-bid hazard.
- *2029:* the structural contest and the counterfactuals; finish the draft by June 2029.

### Pitch 3. Best and final? Seller commitment in takeover auctions

**Question.** Do sellers keep the deadlines and "final" rounds of their own auctions? What does the lack of commitment cost target shareholders?

**Why business schools care.** Every sale process runs on process letters, deadlines and a "best and final" round. If sellers reopen after low bids, bidders hold back in the round called final. Theory predicts that a seller without commitment earns less. Bankers claim that an extension extracts more. Boards and courts judge processes by these rules. A number for the cost of non-commitment tells a board whether to bind itself. A firm deadline is one tool; a go-shop in place of reopened rounds is another.

**The new fact.**

- How often a round announced as final reopens.
- How often the seller extends a deadline or accepts a late bid.
- How large the bid jumps are after the seller reopens a round.
- Whether bidders bid less in final rounds run by advisers that often reopened before.

A crude pilot shows the effect exists. Take the 82 reference deals with a dated final-round marker. In 14 of them, a bid more than two weeks after the marker beat every bid of the first two weeks. The marker dates the start of the round, not its deadline, so this count is rough.

**Model.** The model is a dynamic auction. The seller announces a final round but can reopen it when the best bid falls below a threshold. Each reopened round costs delay, bidder exit and leak risk. Bidders anticipate the probability of a reopened round and shade their final-round bids. The key primitives are:

- the seller's threshold for a reopened round, and its cost;
- the bidder value distributions;
- the bidders' beliefs that the seller will reopen, which come from the adviser's record.

**Data.** Census fields: due dates, deadline outcome, round finality, late bids and the adviser. Each adviser's past rate of reopened rounds comes from earlier deals in the census. SDC supplies adviser identity (to run on WRDS). Sample: the census, restricted to processes with at least two bidders in a round called final. In the reference set, 101 of 404 deals have formal bids from two or more distinct bidders.

**Identification.** Reopened rounds, given the bids, identify the seller's threshold. Bid increments in reopened rounds show how much bidders shade. Bidder beliefs move with the adviser's record of reopened rounds. A repeat bidder sees that record, so compare final-round bids in the same deal type under advisers with high and low past rates of reopened rounds. The adviser choice is a confound, so add target-size, industry and year controls, and add a within-adviser comparison over time.

**Structural flag: yes.** Estimate the dynamic auction. Counterfactuals:

1. full commitment (no reopened rounds);
2. a binding sealed-bid final round;
3. the value to a seller of an adviser with a reputation for commitment.

**The question no one else with the same data would ask.** When the seller says "final", do bidders believe it, and does the bank's record decide whether they do?

**Closest papers.**

- McAfee and Vincent (1997, *Games and Economic Behavior*), sequentially optimal auctions (unverified).
- Skreta (2015, *Journal of Economic Theory*), optimal auctions without commitment (unverified).
- Ye (2007, *Games and Economic Behavior*), indicative bids and two-stage auctions (unverified).
- Gorbenko and Malenko (2014, *Journal of Finance*), valuations from takeover auction bids (verified in the dossier). This pitch adds the seller's commitment as a primitive.
- Boone, De Maeseneire, Dereeper, Luypaert and Nguyen Thuy (2024, ECGI working paper): first offers in the private phase (verified). That paper studies the start of the process; this pitch studies its end.

**Main risk.** Alex states that he wants the deadline fields for the joint project. A solo paper on them needs his explicit agreement. The deadline codes also need mandatory human review, which makes it the most expensive field in the census.

**Kill test (two to three weeks).**

1. Agree the scope with Alex.
2. On the 12 deals in review and the 82 reference deals with final-round markers, date the deadlines by hand.
3. Count final rounds followed by a higher bid from any party.

If fewer than about one in ten final rounds reopen, the commitment problem is too small for a job-market paper.

**Timeline.**

- *Late 2026:* agree the scope and run the kill test.
- *2027:* include the deadline fields in the census build, with human review of deadlines.
- *2028:* the reduced-form facts and the adviser-record design.
- *2029:* the structural estimation and the counterfactuals.

## 3. Where CCC fits

CCC is a strong theory paper. As a job-market paper it lacks empirical reach. Its model describes a sale opportunity that the public knows about while the target stock trades. But most sale processes stay confidential until the merger agreement. The reference set codes a public sale press release in only one or two deals. The cleanest empirical home for CCC is the period after the agreement, which Pitch 2 studies. There the signed bidder is the incumbent, and a topping bidder is the potential rival. The arbitrage market is the price that the rival watches, and the background disclosure is news about the rival's class. Pitch 1 also contains a direct test of the CCC channel: whether outside bidders contact the target after a dated leak. I recommend that CCC stay a second paper. It can also serve as the theory chapter behind the entry results of Pitch 1 or Pitch 2. If Pitch 2 survives its kill test, CCC gives that pitch the model of rival entry from prices that the structural contest needs.

## Sample sizes

### A. EDGAR quarterly form indexes, filing counts 2000 to 2025

**Request.** `GET https://www.sec.gov/Archives/edgar/full-index/<year>/QTR<n>/form.gz` for 2000 Q1 to 2025 Q4. This is the compressed copy of the same index as `form.idx`. Header: `User-Agent: Austin Li junyu.li.24@ucl.ac.uk`. The run used 104 requests, 433,571,686 bytes and at most 4 requests per second. Each index was streamed and parsed in memory, and no index was saved. Rule: the form type is the first 17 characters of each line. Each count is the number of distinct accession numbers by filing year. A filing with two parties (for example, an SC TO-T) appears twice in the index but counts once here.

| Form | 2000 | 2005 | 2010 | 2015 | 2020 | 2021 | 2025 | Total 2000–2025 |
|---|---|---|---|---|---|---|---|---|
| DEFM14A (definitive merger proxy) | 300 | 253 | 202 | 219 | 179 | 311 | 235 | 5,835 |
| PREM14A (preliminary merger proxy) | 327 | 236 | 183 | 128 | 103 | 181 | 144 | 4,786 |
| DEFM14C (merger information statement) | 24 | 12 | 13 | 12 | 8 | 9 | 22 | 411 |
| SC 14D9 (target response to a tender offer) | 351 | 146 | 125 | 111 | 66 | 60 | 55 | 3,293 |
| SC 14D9/A | 380 | 238 | 566 | 342 | 203 | 163 | 174 | 8,245 |
| SC14D9C (communication before the offer starts) | 129 | 69 | 144 | 116 | 65 | 70 | 88 | 2,758 |
| SC TO-T (third-party tender offer) | 299 | 109 | 116 | 99 | 58 | 46 | 54 | 2,803 |
| SC TO-T/A | 1,029 | 584 | 720 | 445 | 235 | 184 | 219 | 13,122 |
| SC 13E3 (going-private transaction) | 125 | 143 | 95 | 31 | 51 | 36 | 36 | 2,039 |
| PREC14A (contested proxy) | 131 | 79 | 90 | 107 | 93 | 85 | 99 | 2,682 |
| DFAN14A (dissident material) | 348 | 331 | 563 | 553 | 413 | 592 | 589 | 14,159 |
| SC TO-I (issuer tender offer) | 153 | 353 | 487 | 522 | 396 | 374 | 577 | 11,561 |
| S-4 | 781 | 614 | 400 | 349 | 272 | 406 | 217 | 10,672 |
| 425 | 2,888 | 4,323 | 2,663 | 4,775 | 3,361 | 8,309 | 4,463 | 93,629 |
| SC 13D | 3,222 | 2,590 | 1,974 | 1,528 | 1,148 | 1,557 | 0 | 47,883 |

Full annual series for the main target forms (distinct accession numbers):

| Year | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DEFM14A | 300 | 238 | 174 | 184 | 203 | 253 | 285 | 343 | 207 | 137 | 202 | 202 | 148 | 191 | 185 | 219 | 230 | 224 | 246 | 221 | 179 | 311 | 246 | 215 | 257 | 235 |
| PREM14A | 327 | 297 | 224 | 236 | 224 | 236 | 314 | 341 | 178 | 125 | 183 | 167 | 128 | 128 | 119 | 128 | 146 | 137 | 147 | 140 | 103 | 181 | 155 | 126 | 152 | 144 |
| SC 14D9 | 351 | 252 | 226 | 186 | 154 | 146 | 150 | 266 | 145 | 118 | 125 | 130 | 98 | 87 | 93 | 111 | 97 | 85 | 76 | 46 | 66 | 60 | 63 | 58 | 49 | 55 |
| SC TO-T | 299 | 237 | 196 | 147 | 108 | 109 | 109 | 182 | 117 | 97 | 116 | 106 | 84 | 111 | 95 | 99 | 87 | 77 | 67 | 44 | 58 | 46 | 56 | 54 | 48 | 54 |
| SC 13E3 | 125 | 167 | 119 | 176 | 123 | 143 | 121 | 112 | 74 | 92 | 95 | 80 | 46 | 72 | 39 | 31 | 65 | 31 | 34 | 26 | 51 | 36 | 45 | 49 | 51 | 36 |
| Target CIKs (DEFM14A ∪ DEFM14C ∪ SC 14D9) | 576 | 451 | 374 | 342 | 313 | 353 | 392 | 517 | 325 | 235 | 305 | 318 | 239 | 266 | 275 | 310 | 320 | 304 | 317 | 270 | 233 | 361 | 303 | 275 | 306 | 300 |

The last row sums to 8,580 target-years, not deals.

Derived counts from the same run (all in memory):

- **PREM14A episodes** (the first PREM14A of a CIK, with a new episode after 365 days): 4,623.
- **Of these, no DEFM14A by the same CIK within 400 days:** 761. This is a candidate set of withdrawn or topped deals (to verify). The rate is high in 2000 to 2003 (110, 101, 65, 71). This suggests other causes in those years, such as a later filing under another CIK.
- **Distinct CIKs with an SC 14D9:** 2,120. Of these, 577 filed five or more SC 14D9/A amendments and 170 filed ten or more. This is a rough marker of long or contested tender processes.
- **CIKs with a DEFM14A and then an SC 14D9 within 365 days:** 52 (a switch to a tender offer or a hostile offer).

### B. Adjusted size of the census: completed public-target sales with a background section

**Request.** The same URL pattern and header, for 2000 Q1 to 2026 Q3: 107 requests and 449,455,485 bytes, parsed in memory. The extra 2026 quarters capture deregistrations after 2025 filings. The method:

1. Define a target episode as the first DEFM14A, DEFM14C or SC 14D9 of a CIK. A new episode starts after 365 days without such a filing.
2. Call an episode "completed" if the same CIK files a Form 15-12G, 15-12B or 15-15D within 400 days. A target usually files this deregistration after the merger closes.

| Year | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Target episodes | 576 | 413 | 359 | 331 | 290 | 343 | 382 | 493 | 315 | 227 | 299 | 311 | 230 | 256 | 272 | 298 | 315 | 295 | 311 | 264 | 229 | 356 | 298 | 269 | 301 | 294 | 8,327 |
| With Form 15 within 400 days | 332 | 259 | 187 | 186 | 191 | 247 | 265 | 326 | 204 | 151 | 221 | 224 | 190 | 206 | 201 | 225 | 230 | 223 | 224 | 206 | 146 | 247 | 205 | 205 | 212 | 225 | 5,738 |
| Filer name like a SPAC | 1 | 0 | 0 | 0 | 2 | 0 | 8 | 13 | 8 | 12 | 4 | 0 | 2 | 5 | 4 | 8 | 5 | 8 | 11 | 8 | 27 | 56 | 41 | 33 | 36 | 17 | 309 |

The completed episodes split by first form: 4,096 DEFM14A, 1,466 SC 14D9 and 176 DEFM14C. For 2001 to 2025, the count is 5,406.

**Estimate.** The census frame is about 5,400 completed public-target sales with a background section, 2001 to 2025, about 220 a year. The deregistration filter removes most acquirer-side proxies and de-SPAC proxies, because those filers stay registered. The frame excludes deals that failed or were topped (see the 761 candidates above). A CRSP price and an exact-dated process cut the frame further; the CRSP-SDC link must run on WRDS.

**Caveats.**

- Raw DEFM14A counts include acquirer proxies for share issues and de-SPAC proxies. The 2021 peak (311) is the SPAC wave.
- SC 13D shows 0 in 2025 because EDGAR renamed the form (structured "SCHEDULE 13D" filings), not because filings stopped.
- Form 15 can follow a going-private deal or a removal from the exchange for other reasons. The "completed" count is thus an upper estimate of completed third-party sales.
- The indexes end in September 2026. A late-2025 episode thus has less than 400 days to show a Form 15, so the 2025 count (225) is a floor.

### C. The reference hand-coded deals (Alex's collection, read in memory, nothing saved)

Source: `sec-auction/ref/deal_details_Alex_2026.xlsx`, parsed from the workbook XML.

- **Size:** 404 deal keys (DealNumber × target name; the dossier counts 401 targets), 9,335 rows, announced 2009 to 2021.
- **Bid rows:** 2,551 informal and 1,004 formal.
- **NDA rows:** 2,619, of which 1,101 are financial, 944 strategic and 574 mixed or unknown. These are rows, not signers: a cohort row can carry several parties. The median is 5 NDA rows per deal, and the 90th percentile is 14.
- **Distinct bidder names per deal:** median 3.
- **Date precision:** of 6,174 NDA and bid rows, 4,236 (69%) carry an exact date.
- **Confidential window,** from the first NDA or bid to the announcement: median 223 days, interquartile range 112 to 504.
- **Same-bidder bid pairs:** 418 bidders have an exact-dated informal bid and a later exact-dated formal bid. The median gap is 28 days. The revision has a median of +1.0%, a mean of +2.9% and a standard deviation of 11.9%.
- **Runner-up gap,** the best last bid against the second-best last bid: 285 deals with two priced bidders, median 5.6% of the best bid, 75th percentile 11.8%.
- **Final rounds:** 82 deals carry a dated final-round marker. In 14 of these, a later bid beat every bid of the first two weeks after the marker. Only 4 deals carry an extension code.
- **Deadline codes:** this collection does not code deadlines systematically.

### D. Options coverage (current file, read only)

ThetaData root list, probe of 5 October 2026 (`/mnt/rdss/austin/data/options/theta-direct/probe-2026-10-05/`, endpoint `/v3/option/list/symbols`, 15,807 roots). Nineteen of 20 checked target tickers are present: ZEN, CTXS, PLAN, SAIL, AVLR, COUP, IMPR, MDVN, PETM, KRA, STEC, DTLK, SYNC, TUC, POM, ZEP, TWTR, ATVI and VMW. Only PENX (Penford) is absent. SPXW expirations in the same probe start on 1 June 2012, so the history probably starts in mid-2012. Three facts are unverified: the start of single-stock history, the subscription entitlement and the licence terms. Tickers are reused, so the root must be mapped by date. OptionMetrics access on WRDS is not checked.

### E. Counts from published papers and counts to run on WRDS

- Augustin, Brenner and Subrahmanyam (2019): 1,859 US takeover targets, 1996 to 2012 (verified).
- Kacperczyk and Pagnotta (2019, RFS): 3,586 illegal insider trades (verified). Their 2024 JF paper uses 530 SEC investigations (verified).
- Liu and Mulherin (2019): 388 deals, 1981 to 2014 (verified).
- Zha Giedt (working paper): 1,006 announcements of strategic-alternative reviews, 1990 to 2014; 41% receive an offer within a year (from a secondary summary, unverified).
- Liu and Officer: one version uses 1,324 acquisitions from 1994 to 2016, and a related AEA paper uses 841 acquisitions from 2005 to 2019. The attribution of these counts is unverified.
- **To run on WRDS:**
  - SDC completed US public-target deals, 2001 to 2025, with a CRSP link;
  - the deals with a competing bid in `sdc.wrds_ma_competition` (11,047 rows in total);
  - OptionMetrics coverage of the census targets;
  - TAQ access.

## Sources

- [Schwert, Markup pricing in mergers and acquisitions (NBER w4863)](https://www.nber.org/papers/w4863.pdf)
- [Betton, Eckbo, Thompson and Thorburn, Merger negotiations with stock market feedback (ECGI)](https://www.ecgi.global/publications/paper-publications/merger-negotiations-with-stock-market-feedback)
- [Liu and Officer, Inside the "black box" of private merger negotiations (AEA 2020)](https://aeaweb.org/conference/2020/preliminary/paper/Nt6yAbSY)
- [Boone et al., Unravelling bidding strategies in M&A transactions (ECGI 2024)](https://www.ecgi.global/node/6052)
- [Fidrmuc and Xia, Target insiders' preferences when trading before takeover announcements (QMRO)](https://qmro.qmul.ac.uk/xmlui/handle/123456789/70944)
- [Augustin, Brenner and Subrahmanyam, Informed options trading prior to takeover announcements (Management Science)](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2018.3122)
- [Kacperczyk and Pagnotta, Legal risk and insider trading (RePEc)](https://ideas.repec.org/a/bla/jfinan/v79y2024i1p305-355.html) and [Chasing private information (CEPR DP13928)](https://repec.cepr.org/repec/cpr/ceprdp/DP13928.pdf)
- [Gentry and Stroup, Entry and competition in takeover auctions (RePEc)](https://ideas.repec.org:443/a/eee/jfinec/v132y2019i2p298-324.html)
- [Liu and Mulherin, How has takeover competition changed over time? (RePEc)](https://ideas.repec.org/a/bla/jacrfn/v31y2019i1p81-94.html)
- [Should a company reveal that it is evaluating strategic alternatives? (Duke FinReg Blog)](https://sites.duke.edu/thefinregblog/2021/06/10/should-a-company-reveal-that-it-is-evaluating-strategic-alternatives/)
- [SS&C Intralinks 2024 M&A Deal Leaks Report](https://www3.intralinks.com/rs/414-BKN-706/images/SS%26C-Intralinks-2024-M%26A-Deal-Leaks-Report.pdf)
- [An options-based approach to forecast competing bids: Canadian takeover battles (IWH)](https://www.iwh-halle.de/en/publications/detail/an-options-based-approach-to-forecast-competing-bids-evidence-for-canadian-takeover-battles)
- [Don't ask, don't waive standstills (Harvard Law School Forum)](https://corpgov.law.harvard.edu/2012/12/18/dont-ask-dont-waive-standstills)
