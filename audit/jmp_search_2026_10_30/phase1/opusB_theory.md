# Phase 1, theory angle (Opus B): job-market paper candidates

30 October 2026.

- **Web search** was available. I used it to check novelty and the closest papers. A reference marked "unverified" did not appear in a search result. Section 4 lists the pages I checked.
- **Pilot figures** come from read-only counts of the hand-coded workbook `sec-auction/ref/deal_details_Alex_2026.xlsx` (390 deals, 2009 to 2021). Research assistants coded most deals, and Alex corrected 9. The figures are indicative only.
- **Competition for the same data.** Other teams already read the same filings:
  - Liu, Officer and Tu: 841 to 1,324 deals, with bid paths, counteroffers and a paper on public price signals in private talks.
  - Carlin, Liu, Officer, Pernoud and Tu (NBER 2026): optimal bidder pools.
  - Eckbo, Norli and Thorburn (2026): who starts a sale.
  - Kim and Zheng: the structural cost of one more bidder (287 auctions).
  - Gentry and Stroup (JFE 2019): structural entry.

  So the moat must be the question. Each pitch names a question that these teams do not ask.

## 1. Longlist

Scores are 0 to 10. Weighted = 0.30 × originality + 0.25 × importance + 0.25 × practicality + 0.20 × fit. The scores are provisional.

| # | Idea | Orig. | Imp. | Pract. | Fit | Weighted | Structural |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | **Final means final?** A board that cannot commit to end its sale makes bidders keep money back; the target's bank can sell commitment. | 8 | 8 | 6 | 9 | 7.70 | Yes |
| 2 | **The private-equity floor.** Credit conditions reach the prices strategic bidders pay, through the fund runner-up and through fund entry. | 7 | 8 | 6 | 7 | 7.00 | Yes |
| 3 | **Liquid markets, narrow auctions.** Each NDA signer can leak; where a tip is cheap to trade, boards sell through short lists. | 7 | 7 | 5 | 8 | 6.70 | No |
| 4 | **Do markets read the background?** The proxy first reveals the losing bids; prices should react, and close losers should top the deal or seek appraisal. | 7 | 5 | 8 | 6 | 6.55 | No |
| 5 | **The late-call curse.** Under common values, a late call tells a bidder that earlier calls failed, so late bidders enter less and bid less (a mirror of Gorbenko and Malenko 2024). | 7 | 6 | 5 | 8 | 6.45 | Yes |
| 6 | **The banker's clock.** A fee paid only at completion makes the target's bank end its search early; fee terms predict breadth and price (prior evidence: Hunter and Jagtiani 2003). | 5 | 7 | 7 | 7 | 6.40 | Yes |
| 7 | **When should a board go public?** The board's choice to announce a sale, with CCC's trade stage kept: publicity as information design. | 7 | 6 | 6 | 6 | 6.30 | No |
| 8 | **The warm runner-up.** A target that keeps a dropped bidder in reserve deters price cuts in exclusive talks (overlap risk with the joint informal-bids paper). | 6 | 6 | 6 | 7 | 6.20 | Yes |
| 9 | **Prices that recruit: a field test of CCC.** In public sales and go-shops, late rivals enter after price rises, more so against strong incumbents. | 6 | 6 | 5 | 7 | 5.95 | No |
| 10 | **Is the market check theater?** Legal shocks (Corwin 2015 and Trulia 2016, unverified) change how broadly boards shop; do premiums follow? | 5 | 6 | 7 | 5 | 5.75 | No |
| 11 | **The leak rule.** In the UK, a leak forces an announcement and starts a 28-day deadline; when prices force disclosure, who enters? | 6 | 6 | 4 | 5 | 5.30 | No |

The pitches follow in the order of the weighted score.

## 2. Top 3 pitches

### Pitch 1. Final means final? The cost of a seller who cannot commit

**Question.** How much do target shareholders lose because a board cannot commit to end its own sale, and can the target's bank supply that commitment?

**Why business schools care.**
- Most US public targets sell through a private process with due dates and a "final" round. In about 75% of deals, the last stage is talks with one bidder (Liu, Officer and Tu).
- Delaware law in general requires a fiduciary out. The board must stay free to take a better offer, so no round is final in law (Kesten 2015).
- If bidders expect one more round, they keep money back in the "final" one. Then the credibility of the process matters as much as its design.
- The answer bears on due dates, standstills and the choice of adviser. Banks compete for sale mandates, and a record of hard due dates becomes part of what they sell.

**The new fact or result.**
- A pilot on 81 hand-coded auctions with a final-round marker, 2009 to 2021:
  - In 46 deals, a bidder raised its own bid after its first final-round bid. In 15 deals, two or more bidders did so.
  - In 64 deals, the data show both the winner's first final-round bid and the signed price. The winner signed above that bid in 56 of them, by a median of 4.2% (interquartile range 2.6% to 7.5%).
  - Limits: only 81 of 390 deals carry the marker, a later addition by Alex, and no record says how those deals were chosen. So the shares may not generalize. Marker dates mix the letter date and the due date. A raise can be a last talk with the winner, not a new contest. Either way, the "final" bid was not the last price.
- The paper will show three results:
  1. how often "final" is final in the full population of sales;
  2. that bidders keep less money back when the target's bank has a record of hard due dates;
  3. the dollar value of commitment to target shareholders.

**Model.**
- A board sells to strategic and financial bidders with different value distributions. It runs a sealed final round. After the bids, it can go back to the top bidders. It cannot commit not to.
- Bidders know the chance of a further round. Each sealed bid trades a sure win now against a lower price later. A soft final round thus becomes an open contest.
- With symmetric private values, this costs the seller nothing, by revenue equivalence. This is the main theoretical risk. The loss must come from one of three sources:
  1. **Asymmetry.** Sealed bids beat open bids for the seller when the strong type's values are flatter and more dispersed (Maskin and Riley 2000; result seen in a secondary summary). Gorbenko and Malenko (2014) and Gorbenko (2019) find more dispersed strategic values. So M&A can be the case in which commitment pays. The model must check this map first.
  2. **No credible walk-away price.** A seller that cannot commit to future reserves loses its reserve (Liu, Mierendorff, Shi and Zhong 2019).
  3. **Entry.** A bidder that expects a further round can wait, or skip the costly early rounds.
- Commitment devices before signature: hard due dates, an announced final round, standstills with "don't ask, don't waive" terms, and the record of the target's bank. The bank is a repeat player. A bank that never reopens a final round makes "final" credible.
- Key primitives: value distributions by bidder type; the chance of a further round, by bank; the board's walk-away value; the cost to prepare a bid.
- Boundary: termination fees and match rights after signature stay out, except as controls. This keeps the paper apart from "Deal Terms in Takeovers" (Gorbenko, Green and Mirani; unverified).

**Data.**
- Sale-process ledgers (`sec-auction`) for US public targets with a merger proxy or tender-offer background, from 2001. Fields: round Finality (announced, inferred, not final); due dates and Deadline outcome (Extended, Enforced); Re-entered; exits with Exit reason; bids by round with Formality; the target's financial adviser.
- Pilot now: `sec-auction/ref/deal_details_Alex_2026.xlsx` (390 deals; 81 with final-round markers; 1,004 formal bid rows) and the 12 deals under review in the ledger app.
- To build: the bank for each workbook deal (the workbook has no adviser column; the ledgers have one); standstill and "don't ask, don't waive" terms from each filing's account of its NDAs; CRSP prices for premiums over the market price.

**Identification.**
- Belief about a further round: how often the bank reopened a final round in its other deals (leave one out), with bank fixed effects and changes in that record over time. Where filings name a fund, the same fund across several banks gives a comparison within one bidder.
- The bank record is not exogenous. A board reopens when final bids disappoint, so the record also reflects the bids that the bank's clients received. The record must therefore condition on the gap between final bids and the board's walk-away value. The structural model does this, because a further round is a decision against that value.
- Holdback: final-round bids relative to earlier informal bids, and the raise after the final round. Prediction: a bank with a hard record gets higher final-round bids and smaller raises after them.
- A shock to one device: in late 2012, Delaware decisions (Complete Genomics; Ancestry.com) put "don't ask, don't waive" standstills in doubt (per practitioner commentary). Compare deals with and without such standstills, before and after.
- Structural: the observed rate of further rounds by bank pins down the bidders' belief. Bids by type pin down the value distributions (as in Gorbenko 2019), and exit reasons give bounds.

**Structural flag.** Yes. The model estimates value distributions by type, the bidders' belief about a further round, and the board's walk-away value. Counterfactuals:
- proceeds when the final round is final, against the observed soft rounds;
- proceeds under a rule that allows, or bans, "don't ask, don't waive" standstills.

**The question no one else with the same data would ask.** "When the target's bank says 'final', how often is it final, and how much money do bidders keep back because they know the answer?" Other teams with process data assume that the board commits to its own rules (Carlin et al. 2026). This paper measures that commitment and puts a price on it.

**Closest papers.**
1. Liu, Mierendorff, Shi and Zhong (AER 2019), "Auctions with Limited Commitment." Theory of a seller who cannot commit to future reserves. This paper takes the problem into staged takeover sales with two bidder types, and measures it.
2. Kesten (Yale Journal on Regulation 2015), "Adjudicating Corporate Auctions." A legal argument: the fiduciary out turns sealed-bid sales into English auctions. It has no model of holdback and no data.
3. Carlin, Liu, Officer, Pernoud and Tu (NBER WP 34846, 2026), "Bidder Pools in Mergers and Acquisitions." Optimal pool size with correlated values. It assumes that the board commits to its procedure; this paper drops that assumption.
4. Choi (University of Chicago Law Review 2021), "Deal Protection Devices." Auction theory of termination fees and match rights after signature. This paper studies commitment before signature.
5. Liu, Officer and Tu (working paper, AEA 2024), "Negotiation, Auction, or Negotiauction?!" Fluid processes and counteroffers in 841 deals. It has no theory of commitment and no data on due dates.

**Main risk and kill test.**
- Risk 1, theory: the two value distributions can be close in shape. Then a soft final round costs little, and the headline number is small.
- Risk 2, the supervision team: Alex's notes call deadline enforcement central to "sale processes and their optimality". The joint informal-bids model also assumes a first-price formal stage with known shading, and that assumption identifies its informal-to-formal wedge. This paper tests that assumption. The test cuts both ways: if final rounds hold, the joint model stands and the commitment loss is small.
- Kill test: once 200 census deals exist, one day of work gives two numbers.
  - (a) The share of final rounds that two or more bidders reopen.
  - (b) The share of the variation in (a) that the bank explains.
  - If (a) is below 10%, or (b) is near zero, the bank channel fails and the paper loses its identification.
  - The hand-coded sample gives (a) now: 15 of 81, about 19%. It cannot give (b).

**Timeline to fall 2029.**
- November–December 2026: agree the boundary with Alex in writing: shared data, separate questions, no termination fees or match rights.
- January–June 2027: theory with two types and a further round. Pilot facts from the hand-coded sample and the 12 reviewed deals.
- July 2027–June 2028: census with reviewed round and due-date records; bank records; standstill terms.
- July 2028–March 2029: structural estimation (HMC) and counterfactuals.
- April–September 2029: draft, internal seminars, job-market version.

### Pitch 2. The private-equity floor: how credit reaches the prices strategic bidders pay

**Question.** When a strategic bidder wins a target that buyout funds also bid for, does its price move with credit conditions, because the funds' leveraged bids set the price and decide who prepares a bid?

**Why business schools care.**
- Credit conditions drive buyout prices and buyout activity (Axelson et al. 2013; Haddad, Loualiche and Plosser 2017).
- Many strategic bidders pay with cash on hand or with stock. Credit should not move their prices, unless a fund is in the contest.
- If funds set a floor, credit policy reaches the market for corporate control through auction competition. Rules on leveraged lending then change what target shareholders get in strategic sales.
- This is a new channel from credit markets to the reallocation of firms.

**The new fact or result.**
- Which sales had a buyout fund among the bidders, and whether that fund's bid tracked credit spreads between rounds.
- Pilot on the 390 hand-coded deals: 224 strategic winners. In 65 of them, a financial bidder also bid, and in 16 it made a formal bid. 189 financial bidders made an informal bid and later a formal bid, a median of 74 days apart. Credit can move in that window.
- The paper will show three results:
  1. A fund's revision between rounds moves with the change in credit spreads over the same window.
  2. A strategic winner's price moves with credit only when a fund is the runner-up.
  3. Credit changes who prepares a bid: fewer funds sign NDAs when credit is tight. So the floor works through entry, not only through the second price.

**Model.**
- Two bidder types. Strategic bidders have synergies and pay from internal funds. Buyout funds have values that rise when debt is cheap.
- Each bidder pays a cost to prepare a bid. A fund prepares only when credit is cheap enough.
- A strategic bidder that meets a fund must beat the fund's leveraged value. So credit enters the strategic price through two numbers: the chance that a fund prepares, and the fund's value when it does.
- Tighter credit lowers both, so strategic winners pay less. Sales with only strategic interest do not change.
- Key primitives: value distributions by type; the credit sensitivity of fund values; preparation costs by type; the board's walk-away value.

**Data.**
- Sale-process ledgers: bidder type; NDA and bid dates by round; bid levels; exits with Exit reason; the winner.
- Pilot now: the 390-deal workbook (type flags; dated informal and formal bids).
- Credit: the ICE BofA US high-yield spread (FRED); a leveraged-loan spread series (source to confirm). CRSP prices for premiums.

**Identification.**
- Time inside the process: a fund's informal and formal bids bracket a credit move that the market sets, not the deal. Strategic bidders in the same process and window are the control. A common shock to target value moves both types; a credit channel moves only the funds.
- Runner-up identity: the theory predicts credit sensitivity only when a fund is the runner-up. Losing bids and exit reasons show the runner-up.
- Candidate shock: the 2013 interagency leveraged-lending guidance cut bank leveraged lending, but the lending moved to nonbanks (Kim, Plosser and Santos 2018). Its effect on buyout bids is not known and can be weak.

**Structural flag.** Yes. Estimate value distributions by type, the credit elasticity of fund values, and preparation costs, in an asymmetric auction with entry. This extends Gorbenko (2019) to credit that changes over time. Counterfactuals:
- proceeds in strategic sales under a leverage cap, or under a credit shock of a given size;
- the share of the premium cycle that credit explains through the fund floor.

**The question no one else with the same data would ask.** "Was a buyout fund among the bidders, and did its lenders set the price that the strategic bidder paid?" Public data show only announced bidders. The funds that bid and lose in private stay out of view, and so does this channel.

**Closest papers.**
1. Axelson, Jenkinson, Strömberg and Weisbach (JF 2013), "Borrow Cheap, Buy High?" Credit drives leverage and prices in 1,157 buyouts. Fund winners only; no strategic prices; no losing bids.
2. Haddad, Loualiche and Plosser (JF 2017), "Buyout Activity: The Impact of Aggregate Discount Rates." Risk premia drive buyout activity. It studies activity, not prices in contested sales.
3. Gorbenko (JFE 2019), "How Do Valuations Impact Outcomes of Asset Sales with Heterogeneous Bidders?" Structural values and participation by type; the premium gap comes from dispersion and participation. Static; no credit channel.
4. Martos-Vila, Rhodes-Kropf and Harford (JFQA 2019), "Financial versus Strategic Buyers." Debt misvaluation helps funds outbid strategic bidders. Theory and aggregate facts; no test inside a sale.
5. Bargeron, Schlingemann, Stulz and Zutter (JFE 2008; seen only in a search summary). Private acquirers pay less than public acquirers. A cross-section of winners; no runner-up channel.

**Main risk and kill test.**
- Risk 1, thin overlap: in the pilot, only 65 of 224 strategic sales had a financial bidder with a recorded bid. Large credit moves between rounds are rare outside a few episodes (2008, 2011, 2015–16, 2020, 2022).
- Risk 2, the joint paper: the revision from an informal to a formal bid also contains the informal-bid wedge that the joint paper estimates. Keep that object in the joint paper. Use only its variation with credit here.
- Kill test, a few hours: on the 189 pilot fund bid pairs, relate the informal-to-formal revision to the change in the high-yield spread over the same window. Use strategic pairs in the same windows as the control. If funds show no credit sensitivity, the strategic channel cannot exist. This needs only FRED and the hand-coded sample.

**Timeline to fall 2029.**
- November 2026–February 2027: kill test; confirm a leveraged-loan spread series.
- March–December 2027: model with entry; first descriptive facts.
- 2028: census of bids by type and round; structural estimation.
- January–September 2029: counterfactuals, draft, job-market version.

### Pitch 3. Liquid markets, narrow auctions: leak risk and the breadth of sale processes

**Question.** Does the risk that a private sale leaks into the target's stock and options make boards sell through shorter lists of bidders, and who bears the cost of the leaks?

**Why business schools care.**
- A broad process raises competition (Bulow and Klemperer 1996, unverified). But each party that signs a confidentiality agreement (NDA) can leak.
- Leaks are common: about 25% of takeovers show abnormal option volume before the announcement (Augustin, Brenner and Subrahmanyam 2019).
- If leak risk narrows sales, the liquidity of a target's securities shapes how the firm is sold. Insider-trading enforcement then becomes part of takeover policy.
- The link runs in a new direction: from the market back to the design of the sale.

**The new fact or result.**
- The first day-by-day count of the outsiders who knew about a sale before its announcement.
- Pilot: the median hand-coded deal has 5 NDA rows, a lower bound on parties, and about 175 days from the first NDA to the announcement (interquartile range 84 to 389 days).
- The paper will show two results:
  1. A dose–response: abnormal option volume and stock drift rise after each wave of NDAs, and more so after larger waves.
  2. A design response: where a tip is cheap to trade, boards invite fewer parties and grant exclusivity sooner, and they leak less per day.

**Model.**
- A board chooses how many bidders to invite. More bidders raise the expected price. Each invited party can leak with a fixed chance each day.
- A tip pays only if its holder can trade on it at a profit and with low risk. Each tipped trader faces a fixed cost or a detection risk. In a liquid market more tipped traders clear that bar, so more of the tip reaches the price.
- This fixed cost is the key assumption. In a one-period Kyle market without it, the price is equally informative at any level of noise trade; only the informed profit rises (Kyle 1985, unverified).
- A leak hurts the incumbent bidder. The run-up raises the price against which the board and shareholders judge the offer, and it alerts rivals. So the incumbent asks for secrecy as a condition of its bid: exclusivity, a short list, standstills.
- Equilibrium: the board trades competition against the incumbent's demand. Liquid targets sell through narrower processes.
- Key primitives: the leak rate per party; the cost or risk of trade on a tip; the effect of a run-up on the deal; the incumbent's outside option.

**Data.**
- Sale-process ledgers: NDA dates and counts by type; contacts; exclusivity; announcement dates.
- Pilot now: the 390-deal workbook (2,619 NDA rows), with CRSP daily prices through the CRSP–Compustat link.
- Market data: CRSP daily (access verified); TAQ (unverified); OptionMetrics on WRDS (unverified) or ThetaData single-stock history (coverage and licence unverified); RavenPack news (one slice read before).

**Identification.**
- Dose–response from the calendar. Inside a deal, compare the days after an NDA wave with the days before it. The board and its bank set the calendar, not the market. Later waves add outsiders without a new board decision, so they separate the NDA channel from leaks by directors and bankers.
- Design response from variation across targets in the cost to trade on a tip: listed options or not, option spreads, and the strength of enforcement. Size is the main confound, so compare targets within size and industry cells.
- Who pays: relate leaks to markups and to deal failure, in the frame of Betton, Eckbo, Thompson and Thorburn (2014).

**Structural flag.** No. The paper is a model with sharp reduced-form tests. A weak structural version could estimate the leak rate per party, but it gives no clean policy counterfactual.

**The question no one else with the same data would ask.** "How many outsiders knew about this sale on each day before the announcement, and did the option market know too?" Other teams count bidders. This question turns the NDA calendar into a measure of exposure to insider trading.

**Closest papers.**
1. Acharya and Johnson (JFE 2010), "More Insiders, More Insider Trading: Evidence from Private-Equity Buyouts." More fund and bank participants bring more suspicious trade before buyout announcements. Winner syndicates only; no time path inside the process; no losing bidders; no design response.
2. Augustin, Brenner and Subrahmanyam (Management Science 2019), "Informed Options Trading prior to Takeover Announcements: Insider Trading?" Informed option trade before 1,859 takeovers. No measure of who knew when.
3. Szydlowski, "Leaks and Takeovers" (working paper; journal status unverified). Targets leak to attract bidders. This paper treats leaks as a cost that narrows sales, and it measures them.
4. Kim and Zheng, "How Costly to Sell a Company? A Structural Analysis of Takeover Auctions" (working paper). The cost of one more bidder in 287 auctions, because rivals see confidential data. Their cost works through product markets; this paper's cost works through the stock market.
5. Ahern and Sosyura (RFS 2015), "Rumor Has It: Sensationalism in Financial Media." Merger rumors in the press and their accuracy. This paper dates leaks against the private process.

**Main risk and kill test.**
- Risk 1: no design response. Boards may ignore leak risk, or banks may set breadth by habit. The paper then becomes a measurement paper, which suits JFQA more than JF.
- Risk 2: option data. Access to single-stock option history is not verified.
- Kill test, about two days: on the 390 pilot deals, compare abnormal returns and volume in the 10 days after the first NDA wave with the 10 days before. Check whether the effect grows with the count of signers. If the stock shows no signal, options are unlikely to save the idea. This needs only CRSP and the hand-coded sample.

**Timeline to fall 2029.**
- November 2026–March 2027: kill test; check option and TAQ access.
- April–December 2027: model with costly tips and an incumbent that demands secrecy.
- 2028: census NDA calendars; option and news data; tests of the design response.
- January–September 2029: draft and job-market version.

## 3. Where CCC fits

CCC states a sharp principle: the sale rule decides who owns the surplus, and so what the target's price can teach a rival before entry. The theory is careful and complete, but an editor will stop on its setting and its tests. Its setting is a minority case (a public sale, a prepared incumbent, an unprepared rival who watches the price), and its tests need data that do not exist at scale. My view: CCC is a strong second paper for RFS or a theory journal, and it is the theory section of longlist ideas 7 and 9. It pairs with pitch 3: in CCC a price signal recruits a rival, but in pitch 3 a leak repels the incumbent and narrows the sale. Together they give one research statement: prices before deals can recruit or repel bidders, and the design of the sale decides which.

## 4. Sources checked

- Liu, Mierendorff, Shi and Zhong (AER 2019): [AEA page](https://www.aeaweb.org/doi/10.1257/aer.20170882)
- Kesten (2015): [CLS Blue Sky summary](https://clsbluesky.law.columbia.edu/2015/07/28/adjudicating-corporate-auctions/), [FSU repository](https://ir.law.fsu.edu/articles/593)
- Carlin, Liu, Officer, Pernoud and Tu (2026): [NBER WP 34846](https://www.nber.org/papers/w34846)
- Choi (2021): [University of Chicago Law Review](https://lawreview.uchicago.edu/print-archive/deal-protection-devices)
- Liu, Officer and Tu: [AEA 2024 program](https://www.aeaweb.org/conference/2024/program/paper/rntssT5k), [AFA listing](https://afajof.org/management/viewp.php?n=36876), [Liu and Officer, CLS Blue Sky](https://clsbluesky.law.columbia.edu/2019/06/18/inside-the-black-box-of-private-merger-negotiations/), [Liu CV](https://haslam.utk.edu/wp-content/uploads/2021/12/Liu-CV-2026.pdf)
- Eckbo, Norli and Thorburn (2026): [ECGI](https://www.ecgi.global/publications/working-papers/who-initiates-takeovers)
- Kim and Zheng: [working paper](https://econ.ntu.edu.tw/wp-content/uploads/2023/10/How-Costly-to-Sell-a-Company-A-Structural-Analysis-of-Takeover-Auctions.pdf)
- Gentry and Stroup (JFE 2019): [RePEc](https://ideas.repec.org/a/eee/jfinec/v132y2019i2p298-324.html)
- Bulow and Klemperer (AER 2009): [RePEc](https://ideas.repec.org/p/cpr/ceprdp/7411.html)
- Maskin and Riley (2000): [author PDF](https://maskin.scholars.harvard.edu/resource/pdf-38), [Kirkegaard summary](https://www.uoguelph.ca/economics/sites/uoguelph.ca.economics/files/public/documents/2011-01.pdf)
- "Don't ask, don't waive" decisions: [Harvard Law Forum](https://corpgov.law.harvard.edu/2012/12/18/dont-ask-dont-waive-standstills), [Jones Day](https://www.jonesday.com/en/insights/2013/01/dont-ask-dont-waive-standstill-provisions-a-tool-to-maximize-value-or-willful-blindness)
- Axelson, Jenkinson, Strömberg and Weisbach: [NBER](https://www.nber.org/papers/w15952)
- Haddad, Loualiche and Plosser: [NBER](https://www.nber.org/papers/w22414.pdf)
- Martos-Vila, Rhodes-Kropf and Harford: [RePEc](https://ideas.repec.org/a/cup/jfinqa/v54y2019i6p2635-2661_12.html)
- Kim, Plosser and Santos: [New York Fed](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr815.pdf?la=en)
- Acharya and Johnson: [RePEc](https://ideas.repec.org/a/eee/jfinec/v98y2010i3p500-523.html)
- Augustin, Brenner and Subrahmanyam: [NYU PDF](https://pages.stern.nyu.edu/~mbrenner/research/brenner-patrick-subrahmanyam-informed-trading.pdf), [Hebrew University record](https://cris.huji.ac.il/en/publications/informed-options-trading-prior-to-takeover-announcements-insider-/)
- Szydlowski: [CLS Blue Sky summary](https://clsbluesky.law.columbia.edu/2020/01/27/leaks-and-takeovers)
- Ahern and Sosyura: [RePEc](https://ideas.repec.org/a/oup/rfinst/v28y2015i7p2050-2093..html)
- Betton, Eckbo, Thompson and Thorburn: [ECGI](https://www.ecgi.global/publications/working-papers/merger-negotiations-with-stock-market-feedback)
- Hunter and Jagtiani (2003): [RePEc](https://ideas.repec.org/a/wly/revfec/v12y2003i1p65-81.html)
- Leak reports (practitioner): [Intralinks](https://www.intralinks.com/resources/blog/ma-deal-leaks-negotiating-tactic-what-data-shows)
- UK 28-day deadline: [Takeover Code Rule 2.6](https://code.thetakeoverpanel.org.uk/tp/rules/rule-2/rule-2-6.html)
- Go-shops: [Subramanian (2008)](https://hls.harvard.edu/bibliography/go-shops-vs-no-shops-in-private-equity-deals-evidence-and-implications)
