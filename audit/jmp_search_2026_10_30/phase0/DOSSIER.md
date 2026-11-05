# Phase 0 dossier: Austin Li's research assets

Facts as of 30 October 2026. The dossier describes what exists and makes no proposals.

Path roots used below:

- `CCC/` = `/home/uctpiaj/work/Projects/competition-creates-competition/`
- `IB/` = `/home/uctpiaj/work/Projects/HMC_sim/`
- `SA/` = `/home/uctpiaj/work/Projects/sec-auction/`
- `CV` = `/home/uctpiaj/work/Projects/JobSearch/Austin_cv.tex`

Web search was used only for the supervisors' publications.

## 1. Person and timeline

- **PhD in Financial Economics**, University College London, 2024 to 2029 (expected). Supervisors: Alex Gorbenko (primary), Brian Healy (secondary) (CV).
- **Market:** fall 2029. Targets: business schools worldwide. The job-market paper must be solo and aim at the Journal of Finance, the Review of Financial Studies or the Journal of Financial Economics (`CCC/audit/jmp_search_2026_10_30/briefs/CORE_BRIEF.md`).
- **Fields on the CV:** corporate finance, market microstructure, asset pricing, quantitative finance.
- **Earlier degrees:** MSc Economics, LSE, 2020 to 2022, Merit; dissertation on population ageing and retirement choices in China. BA Political Science and Economics, Vanderbilt, 2016 to 2020, GPA 3.82 (CV).
- **Work in progress on the CV:** one paper, "Competition Creates Competition" (Section 3).

Research and work experience (CV):

| Role | Dates | Content |
|---|---|---|
| PhD research with Alex Gorbenko | 2025 to now | Bayesian estimator for a two-stage M&A auction (JAX, BlackJAX NUTS, quadrature, data augmentation for selection). SEC-filing extraction with source-anchored facts and a DuckDB database. |
| Quantitative Researcher, Decision Science (under Brian Healy) | Aug 2026 to now | Options-based forecasts of intraday volatility and index returns; trade simulations with bid–ask costs and delays. Reduced 225 million option quotes to 5 million with checks. |
| Quantitative Researcher, Knollwood Research and Trading (under Brian Healy) | Jan 2025 to Aug 2026 | Futures pipelines for ten commodities; crude-oil butterflies on 373 million one-second bars; deep-learning momentum models. Dividend-capture panel of about 101,000 events in eight markets. |
| Research Assistant, CUHK | 2023 to 2024 | Semiparametric single-index models (R, C++). |
| Research Associate, UK Energy Research Centre | 2022 to 2023 | Household credit and price elasticities; two talks in the UK Parliament. |

Teaching: MSc Finance teaching assistant (2024 to now); MSc Law and Finance tutor (April 2026 to now). One talk: INFORMS Revenue Management and Pricing, 2023. Languages: Mandarin, English, Russian (CV).

## 2. Supervisors

### Alex Gorbenko

Associate Professor of Economics and Finance, UCL School of Management and Department of Economics. His site lists three research areas: the timing and method of payment in M&A; bidder heterogeneity and its effect on participation and outcomes of asset sales; deals between entrepreneurs and private equity or venture capital investors. Source for the list below: [his research page](https://sites.google.com/site/agorbenko/research), cross-checked against [RePEc](https://ideas.repec.org/a/eee/jfinec/v131y2019i1p88-117.html) and [UCL Discovery](https://discovery-pp.ucl.ac.uk/id/eprint/10154224).

| Paper | Outlet | Question and method |
|---|---|---|
| Strategic and Financial Bidders in Takeover Auctions (with A. Malenko) | JF 2014, 69(6) | Structural estimation of bidder valuations from private bids in takeover auctions. Financial bidders value about a quarter of targets (mature, underperforming firms) higher; strategic synergies are more dispersed. |
| Auctions with Endogenous Initiation (with A. Malenko) | JF 2024, 79(2) | Theory with evidence. A bidder's approach reveals optimism, so sales are mostly seller-initiated under common values and bidder-initiated under private values. Activism and toeholds raise bidder initiation. |
| How Do Valuations Impact Outcomes of Asset Sales with Heterogeneous Bidders? | JFE 2019, 131(1) | Structural estimation from all bids in takeover auctions, 2000 to 2012. The premium gap between strategic and financial acquirers comes mainly from valuation dispersion and bidder participation, not from mean valuations. |
| The Timing and Method of Payment in Mergers when Acquirers are Financially Constrained (with A. Malenko) | RFS 2018, 31(10) | Theory. Constraints delay initiation but not the maximum price, because stock can pay; cash use rises with synergies. |
| Competition among Sellers in Securities Auctions (with A. Malenko) | AER 2011, 101(5) | Theory. Sellers compete for bidders through the security they accept; large markets select cash. |
| CDS Auctions (with M. Chernov, I. Makarov) | RFS 2013, 26(3) | Theory and data on CDS settlement auctions; bonds trade about 6% too low on auction day. |
| Venture Capital Contracts (with M. Ewens, A. Korteweg) | JFE 2022, 143(1) | Structural model of VC contract terms; VCs take more equity than is optimal for startups. |
| Temporary vs Permanent Shocks (with I. Strebulaev) | RFS 2010, 23(7) | Dynamic capital-structure model. |
| Conceptual Framework and Theory of M&A | Handbook chapter, Edward Elgar, 2025 | Review of M&A theory. Listed on his site; unverified. |
| Deal Terms in Takeovers (with B. Green, S. Mirani) | Working paper, 2025 | Listed on his site with no abstract; unverified. |
| Distressed Investment, Corporate Debt Liquidity, and Capital Structure (with D. Orlov) | Working paper | Seminar abstract: a distressed investor buys debt and can restructure the firm in bankruptcy ([TSE](https://www.tse-fr.eu/seminars/2026-joint-finance-theory-seminar-distressed-investment-corporate-debt-liquidity-and-capital-structure)). |

In his voice notes Alex says he has "a different project" on bid conditions "with Brett and Shreye" (`SA/ref/alex_voice_notes_2026-08.docx`, ¶19). This is likely the "Deal Terms in Takeovers" paper. The match is unverified.

### Brian Healy

The search found no academic publication. Public profile ([QuantMinds](https://informaconnect.com/quantminds-international/speakers/brian-healy/)): founder and CEO of Decision Science and of Algo Trading Ltd; former options trader and quant at five banks; PhD in Finance (University College Dublin); interests in computational finance, machine learning and derivative pricing. A [UCD page](https://www.ucd.ie/quinn/facultyresearch/phdresearch/phdstudents/brianhealy/) lists a PhD thesis "Using option implied information for improved returns". It is probably the same person; this is unverified. On the CV he supervises Austin's industry work.

### What Alex wants the sale-process data to answer

Sources: the instruction header (`SA/SEC_Deal_Ledger_Extraction_Instruction.md`), Alex's collection instructions and email of 3 March 2026 (`SA/ref/CollectionInstructions_Alex_2026.pdf`), and his voice notes of August 2026 (`SA/ref/alex_voice_notes_2026-08.docx`, 182 paragraphs, ¶ numbers below).

- **Research label:** "Informal bids, information, selection and competition in takeover processes."
- **Core record:** each NDA signer with its type (strategic or financial; public or private; non-US); each whole-company bid, per share or as a range, informal or formal; event order; who started the sale (target, bidder bid, bidder interest without a bid, activist); the investment bank; press releases of a sale process and of bids.
- **Formality against conditions:** keep procedural formality apart from conditions (financing, diligence, exclusivity), so that estimation can treat a heavily conditional formal bid as informal. Record the absence of financing guarantees (¶19–20, ¶47–49).
- **Selection of the first approacher:** the bidder that approaches first can differ from the others. Its exit after round-one diligence is informative (¶23).
- **Rounds:** infer the number and boundaries of informal and formal rounds from the target's actions, not from the filing's labels (¶168).
- **Deadlines:** record revisions and extensions. They can show the target's limited commitment power (¶62, ¶169).
- **Exit reasons:** a stated reason (below market value, at or below the indication) bounds the final valuation (¶83, ¶173).
- **Target stock price through the process:** premiums over the market price, not dollar bids, are the comparable object. A deal without a market-price benchmark leaves the estimation sample (¶91, ¶95, ¶117).
- **Announcement returns:** relate market reactions to features of the sale process (¶33).
- **Mandatory human review:** round boundaries, deadlines, unknown bidder types, uncertain NDA counts, exit reasons and conditions (¶166–182).

## 3. CCC: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders"

Solo theory paper. Master: `CCC/overleaf/slot/` (commit 631a853); PDF in `CCC/audit/jmp_search_2026_10_30/briefs/`. Main text about 16,000 words; proof appendix about 41,000 words. Slides and a comparison with an earlier Laplace-noise version sit beside it.

**Setting** (`sections/02_model.tex`). A listed target has a publicly known sale opportunity while its stock still trades. An incumbent bidder is already prepared. The public knows the distribution of its value; a first-order shift of that distribution makes the incumbent stronger. A potential rival bidder belongs to a high or a low quality class (prior π). Each class draws a value from its own distribution, and the high class dominates. The rival knows neither its class nor its value. After it sees the stock price, it learns its preparation cost: zero with probability ρ, otherwise a high cost. Payment reveals its value and permits a bid. The sale is a cash second-price auction with a reserve.

**Trading.** An outside informed trader (no position, no control) knows the rival's class. Trade uses one order slot, after Dow and Gorton (1997). With probability λ the informed trader fills it and buys, sells or abstains at a cost k. Otherwise a liquidity trader sells, abstains or buys. Competitive market makers price the order and anticipate the entry it causes. A liquidity order can match every informed order, so every posterior stays inside fixed bounds.

**Results.**

1. *Two returns to information* (Proposition 1, `sections/03_competition_information.tex`). A stronger incumbent weakly lowers the rival's gross profit at every belief. It weakly raises the target-payoff spread, the difference in target proceeds between a high-class and a low-class rival. The sum is constant: competition moves the class value gap from the rival's profit to target proceeds. Trading and preparation see the auction only through two numbers, the spread and the preparation threshold.
2. *Competition creates competition* (Proposition 2, `sections/04_equilibrium_results.tex`). Three economies have unique outcomes on an open parameter set. Against a weak incumbent the price is uninformative and only zero-cost rivals prepare. Against a strong incumbent the high class buys, the low class sells, and a purchase brings in a high-cost rival. Entry rises although profit falls at every belief. When a prepared high-class rival surely beats the strong incumbent, high-class ownership also rises. Against a very strong incumbent the price stays informative but entry falls back to its floor. Controls: with orders held fixed, or with the price hidden from the rival, a stronger incumbent can only lower entry.
3. *Coexistence* (Proposition 3). Uninformative and informative markets coexist exactly on a stated region of the spread and the threshold. Informative entry rises with the spread.
4. *Costly research* (Proposition 4, `sections/05_research.tex`). The informed trader chooses research at a quadratic cost up to a cap. At prior 1/2, research and entry rise with the spread until research reaches the cap. Zero research is also an equilibrium there.
5. *Robustness* (`sections/06_robustness.tex`): other preparation-cost laws; all ranked class pairs and priors (uniform incumbents); more than two classes under a separation condition; private signals of the rival and the informed trader at prior 1/2.
6. *Welfare and sale terms* (`sections/07_welfare.tex`). Rival access to prices raises expected proceeds and net acquisition surplus against the strong incumbent. Under a bargaining payment rule with seller weight ω, competition moves the spread in the direction of the sign of 1 − 2ω. A reserve that excludes the low class can make entry flat in incumbent strength.

**Empirical predictions** (`sections/08_empirical.tex`). Each prediction holds for one target in one public state, under named conditions.

- When the price reaches the rival before its decision, a stronger incumbent can raise entry. When it does not, a stronger incumbent can only lower entry.
- Under full two-sided trade with the prior below the threshold, the purchase impact exceeds the sale impact, each weighted by its order frequency, exactly when a purchase recruits. The test uses only prices and order frequencies.
- Order counts identify the informed trader's presence when the prior is known and differs from 1/2. The sale impact identifies it at prior 1/2.
- A prepared rival wins more often after a purchase than after a sale. Orders can predict the winner where they do not predict entry.
- A report that reveals only preparation moves the price up on average when preparation was still uncertain.
- At intermediate strengths, processes can form two clusters: an uninformative one and a buy-only one.
- **Measurement protocol:** preparation is the start of substantive diligence or a costly proposal. Incumbent strength uses information public before that decision. The order is the first prespecified order opportunity after the sale becomes public, for example the sign of the opening-auction imbalance on the first day after disclosure, with a small imbalance coded as no order.

**Open items.** The conclusion names the seller's choice of sale terms, with the full pricing and trading continuation, as the next theoretical step (`sections/09_conclusion.tex`). No empirical test exists and no data for the measurement protocol exist. Further concessions (`CCC/audit/theory_upgrade_2026_10_25/WORKAROUNDS.md`): the research results hold at prior 1/2 only; the research equilibrium needs an informed trader who may mix; along a general path, coexistence can come in pieces; ownership rises only under an outbidding condition or a stated trade-off.

**Alex's reactions** to the earlier Laplace-noise version (21 October 2026; `CCC/audit/alex_meeting_2026_10_21/BRIEF.md` §2): let the rival draw from one of several distributions, not two values at prior 1/2; justify Laplace noise or use a discrete set-up; say who the informed traders are; normalize the low cost. The current version uses class distributions with a general prior, the discrete slot, an outside informed trader and a zero low cost.

## 4. Informal bids: the joint structural paper with Alex

**Model** (`IB/Informal_bids/README.md`, `IB/Informal_bids/SPEC.md` §2). Each auction has J bidders (three by default). A bidder's value is normal. Its informal bid is a fixed multiple of its value; the parameter κ is the log wedge between informal and formal bid levels. Each auction has a latent cutoff, linear in covariates plus noise. A bidder is admitted when its informal bid plus noise passes the cutoff plus a shift for strategic type (δ) and for bid-range width (δw). The data keep an auction only if at least one bidder is admitted, and the likelihood corrects for this selection. Admitted bidders submit formal bids equal to the equilibrium shading of the value plus a diligence update.

**Estimator.** Bayesian HMC (NUTS) in JAX and BlackJAX and in Stan, all in fp64. The marginal form integrates the cutoff by Gauss–Hermite quadrature (8 parameters). The augmented form samples one cutoff per auction (208 dimensions at 200 auctions). Specifications: an exogenous-covariate control, and N1 to N3 and N5 with bid-built covariates and shifts.

**State** (`IB/talk_reading_group/structure-plan.md` §1, 29 October 2026).

- Done: build milestones M0 to M9 and their numerical gates. The computational study for Sam Livingstone is complete: 1,725 fits, figures F1 to F5, a 15-page manuscript. A defect in the far tail of the selection quadrature is fixed on an open branch (`IB/Informal_bids_a1/`).
- Not done: the economic study. Simulation-based calibration, Monte Carlo recovery and milestones M10 to M15 did not run. Specifications N1 to N3 do not exist: no bid-built covariates, no type shift, no range bids, no dropout model.
- Earlier reports (December 2025 to February 2026, `IB/Informal_bids/reports/`) use an old Metropolis-within-Gibbs engine, which SPEC v2 drops (SPEC §3). They report that γ and κ are recovered in 126 runs (`reports/28-01-26/report.pdf`). A dropout pilot finds cutoff parameters sensitive to voluntary dropout, and type-dependent dropout biases the type shift (`reports/17-02-26/analytical_report.pdf`).
- Open decisions (SPEC §7): is an observed informal bid a point or an interval; κ is identified only because formal shading 1 − 1/J is known; whether to keep bid-built covariates; the law of J; whether admission noise is economic; the dropout model; what separates a type shift from type-dependent dropout (a dropout-only shifter such as a break-up fee).

**Planned data.** The sale-process ledgers (Section 5). The plan is about 20 auctions (structure-plan §1). The HMC manuscript cites samples of 349 to 841 sales in earlier work (structure-plan §8).

## 5. The sale-process ledgers (joint with Alex)

**What one ledger is** (`SA/README.md`; `SA/SEC_Deal_Ledger_Extraction_Instruction.md`, Parts A and D). A language model reads one SEC merger filing, mainly its "Background of the Merger" section, and writes an Excel workbook with four sheets:

- **Deal ledger:** one row per substantive event, in order, with a quotation of at most 30 words and the page. It has 29 columns.
- **Rounds:** one line per bidding round.
- **Questions:** up to five open coding questions, plus review items.
- **Deal facts:** deal-level fields.

Fields by measurement target:

| Target | Fields |
|---|---|
| Bidder entry and exit | Event labels Target interest, Bidder interest, Contact (first contacts, with direction, including parties that decline), NDA signed (dated at execution); Count (bidder units on cohort rows); Type (Strategic, Financial, Mixed, Unknown); exits (Dropped by target, Withdrew, Did not submit, Not selected at signing) with Exit reason; Re-entered; Rounds "Who was in"; Deal facts "Auction screen" (more than one acquirer with an NDA). |
| Timing of contacts and NDAs | When (as the filing states it), Sort date, Date from and Date to (bounds the filing supports); Process and Round on every row. |
| Informal and formal bids | Bid and Bid reaffirmed rows; Price low and Price high (per share), Stock %, CVR or earnout; Formality (Formal by markup, by a round announced as final, or by definitive negotiation; else Informal); Conditions (None, Light, Heavy) with Due diligence, Financing, Regulatory, Antitrust, Exclusivity; Rounds "Bids received". |
| Process type | Initiation (target-led, bidder-led, mixed, activist-influenced); Number of processes; Rounds Finality (announced final, inferred final, not final); Due dates and Deadline outcome (Extended, Enforced, …); Exclusivity changed; Go-shop changed (go-shop solicitation opens a round); Sale process announced, Bid announced, Merger announced; Activist; Adviser. |

The ledger does not record market prices. A stock-price path is a separate enrichment step that no one has specified (`SA/_dev/ALEX_ALIGNMENT.md` §13). Conversion of enterprise-value bids to per-share prices is deferred (`SA/_dev/STATUS.md`).

**Deals and state** (`SA/_dev/STATUS.md`, 15 October 2026).

- Instruction Version 1, approved 28 September 2026, amended 8, 9, 12 and 14 October. Every rule traces to a ruling in `SA/_dev/alignment_sprint/DECISIONS.md`.
- `SA/raw_filing/` holds 8 filings with hashes: Datalink, Kraton, Mac-Gray, Penford, PetSmart, Providence & Worcester, sTec, Synacor (filed 2013 to 2021).
- A shared web review app lists 12 deals: the 8, plus Medivation, Zep, Pepco Holdings and Imprivata. Each has fresh machine extractions. Each is marked "In review". The mechanical checker reports 2 errors and 18 warnings. There is no substantive acceptance yet.
- `SA/extraction/` is empty: no workbook is exported. A comparison with Alex's hand-coded workbook is pending.
- Extractions run only on Austin's command, blind, with one instruction and one filing per isolated run (`SA/README.md`).

**Reference data** (`SA/ref/`, "for evaluation only"):

- `deal_details_Alex_2026.xlsx`: 401 targets, 9,335 event rows, announced 2009 to 2021 (353 DEFM14A, 31 SC TO-T, 17 PREM14A). Rows include 2,551 informal and 1,004 formal bid rows. Columns include Compustat gvkey, the SDC deal number, bidder type, per-share bid or range, bid type, rough date and an all-cash flag. Per Alex's email, research assistants of another group ("Chicago guys") collected it; Alex corrected 9 deals, and he calls earlier deals "collected poorly".
- `seed.csv`: 389 deals (348 DEFM14A, 15 PREM14A, 26 SC TO-T), filed 2000 to 2022, mostly 2010 to 2021; 368 have a usable EDGAR link.

**Scale-up and cost.** The core brief states the plan: all US public targets with a merger proxy or tender-offer background section, thousands of deals. The `sec-auction` repository has no written scale-up plan or budget. The only cost evidence: the best-graded configuration took 10 to 15 minutes and USD 2.5 to 3.6 per deal on two test deals (`SA/_dev/model_comparison_2026-09/README.md`). Alex requires mandatory human review of several fields until extraction proves reliable (voice notes ¶166, ¶182).

## 6. Other data and tools

**WRDS** (REST API, read access verified 14 September 2026; `CCC/empirical/private/access_diagnostic.json`):

| Table | Rows | Server-side filters |
|---|---|---|
| `sdc.wrds_ma_details` | 1,628,107 (147 columns) | CUSIP, deal number |
| `sdc.wrds_ma_events` | 2,255,381 | date, deal number |
| `sdc.wrds_ma_competition` | 11,047 | deal number |
| `crsp.dsf` / `crsp.dsi` | 107,682,104 / 26,051 | CUSIP, date, PERMNO |
| `crsp.ccmxpf_linktable` / `crsp.crsp_cik_map` | 92,711 / 68,879 | gvkey, PERMNO |
| `comp.company` | 58,413 | gvkey |
| `ibes.statsum_epsus` | 15,134,401 | ticker, CUSIP, dates |
| `wrdssec.dforms` | 43,665,868 | CIK, filing date |

The REST catalogue also lists `optionm`, `taqmsec`, `tfn`, `ciq`, `boardex` and `audit` (`wrds_catalogue.json`). Read access to these is not checked. RavenPack news analytics (`rpna`) was read for an energy slice on 9 July 2026 (`/mnt/rdss/austin/data/external/wrds/MANIFEST.md`).

**Options data.**

- The AWS archive `s3://ds-thetadata-options` holds 5-second SPXW greeks and quotes: 1,088 same-day sessions, 1 June 2022 to 2 October 2026, with Athena tables (`/home/uctpiaj/work/Projects/Options/spx-0dte-research/DATA.md`). It serves the same-day index-options research of that project. The files do not name the account owner.
- A ThetaData terminal on the server listed 15,807 option roots on 5 October 2026 (`/mnt/rdss/austin/data/options/theta-direct/probe-2026-10-05/`). All pulls so far are index products (SPXW, SPX, RUTW, XSP, VIX family, SPY, QQQ).
- Single-stock option history for takeover targets is not pulled. Its coverage and licence terms are unverified.

**The 8 case files** (`CCC/empirical/private/`, `CCC/empirical/raw/sec/`). WRDS pulls of 14 September 2026 for Imprivata (2016) and Zendesk, Citrix, Anaplan, SailPoint, Avalara, Coupa and Kohl's (2022). Each has CRSP daily prices (369 to 503 days), the CRSP–Compustat link, Compustat company data, IBES forecast snapshots, SDC deal records with events and competing-bid tables, and the EDGAR submission index (`pilot_coverage.json`). The repository does not document why these cases were chosen.

**Options and futures research:** industry work with internal reports (Section 1).

## 7. Other collaborations

**Borda nonresponse bounds, with Stefan Feuerriegel (LMU)** (`/home/uctpiaj/work/Projects/borda-nonresponse-bounds/README.md`). The question: a platform shows a person two AI answers and asks which is better, but who votes is not random. The target is the sharp identified set of a pre-specified Borda contrast under a sensitivity parameter, and its breakdown value. Status on 2 October 2026: a literature table exists; the choice of sensitivity model is open and blocks the rest; the theory deck has not started; no simulation has run.

**HMC metric study, with Sam Livingstone (UCL Statistical Science)** (`IB/talk_reading_group/structure-plan.md`). The question, open in Hird and Livingstone (arXiv:2604.09286, §5.1): how many directions an adaptive NUTS metric should learn, net of the cost of adaptation. Result: a few learned directions give the best net efficiency. The informal-bids posterior is one test target. Austin presents to Sam's reading group on 3 November 2026. Sam asked for that session before any further step, so no joint paper is agreed.

## 8. The literature tracker

`Austin-j-li/research-feed` (private, read through the GitHub API) is a production pipeline for narrated research videos, not a reading list. An editorial contract (`docs/EDITORIAL.md`) sets three 30-minute episodes a week:

- Monday: financial economics, including governance, microstructure and M&A auctions.
- Wednesday: Bayesian statistics and MCMC.
- Friday: quant finance.

The ledger on `main` is empty. Six episodes exist on work branches since 17 October 2026:

- **19 October, finance:** common ownership (Backus, Conlon and Sinkinson 2019 and 2021; Gilje, Gormley and Levit; Antón, Ederer, Giné and Schmalz).
- **26 October, finance:** "Competition or Bargaining? Auctions in Takeovers and Treasuries" (Bulow and Klemperer, "Auctions vs. Negotiations"; Schwert, "Markup Pricing in Mergers and Acquisitions"; Hortaçsu, Kastl and Zhang on Treasury bid shading; Boyarchenko, Lucca and Veldkamp on dealer information).
- **Other four:** MCMC diagnostics; posterior approximation; the factor zoo and machine-learning return prediction; from forecast to position.

An automated pipeline picks the papers, so the tracker shows topics in rotation, not necessarily Austin's own reading.

## 9. Constraints

- **Solo paper.** The job-market paper is solo. It may use data built with Alex. The informal-bids paper stays joint; a solo spin-off on the same data is allowed. The HMC study is a separate methods paper (core brief).
- **Time.** About 35 months to the fall 2029 market. Austin also holds an industry research job and two teaching roles (CV).
- **Data storage.** Ingested data go to `/mnt/rdss/austin/data/<project>/<dataset>/`, with a receipt (source, request, date, size, SHA-256). Do not store ingested data on the work disk or in `/tmp`. RDSS is a slow network share: use daily or larger Parquet files (`/mnt/rdss/austin/data/README.md`).
- **WRDS data and a public repository.** The CCC GitHub repository is public (checked 30 October 2026). The WRDS pulls in `CCC/empirical/` stay out of git only through the local `.git/info/exclude`.
- **Options archive.** The files do not state the owner of the SPXW archive or its terms for academic use.
- **Ledger production.** Extraction runs only on Austin's command. Alex requires human review of key fields. No ledger is accepted yet (Section 5).
