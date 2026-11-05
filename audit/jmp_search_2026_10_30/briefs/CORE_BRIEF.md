# Core brief: find a job-market paper in M&A

All agents in this search get this brief. Your role brief adds your angle and your output file.

## 1. The person and the goal

Austin Li is a PhD student in Financial Economics at University College London (2024 to 2029). His primary supervisor is Alex Gorbenko, who works on takeover auctions, theory and structural estimation. His secondary supervisor is Brian Healy, who supervises his quantitative work on options and futures. Austin does theory and empirical work. He can build large data pipelines, estimate Bayesian structural models with HMC (JAX, BlackJAX, Stan) and extract facts from SEC filings with language models.

**The goal is to find his job-market paper.** He goes on the market in fall 2029 and targets business schools all over the world. The paper must aim at a top-3 finance journal (Journal of Finance, Review of Financial Studies, Journal of Financial Economics). The job-market paper must be solo. It may use data built with Alex.

## 2. Settled decisions

- **Core field: M&A.** He is most drawn to these three areas:
  - sale-process design: auctions against negotiation, go-shops, standstills, informal bids;
  - bidder participation and entry;
  - information leakage and trading before a deal.
  Other M&A topics are allowed. An idea outside M&A is allowed if it is clearly stronger, but M&A comes first.
- **Method is open.** Structural estimation is a preference, not a requirement. If a good structural idea appears, develop it and do not drop it. A theory paper with sharp empirical verification is also fine.
- **The existing theory paper is one candidate, not the base.** "Competition Creates Competition" (CCC) is a solo theory paper. In it, a stronger incumbent bidder makes the target's stock price more informative about a potential rival bidder. The rival learns from the price before it pays to prepare a bid, so stronger competition can raise entry. Use CCC as one input that you may view from a higher level. Score it against the other ideas. If it loses, it becomes a second paper.
- **Informal bids stays a joint paper with Alex.** It is a structural model of two-stage takeover auctions: informal bids, a latent cutoff, then formal bids. A solo spin-off that uses the same data is allowed. Do not propose the joint paper itself as the job-market paper.
- **The HMC metric study with Sam Livingstone (Statistics) is a separate methods paper.** Computation is a tool for the job-market paper, not its contribution.
- **A census of sale processes will be built.** The joint `sec-auction` pipeline turns the "Background of the Merger" section of SEC merger filings into event-by-event deal ledgers. Version 1 of the instruction is approved, and 8 filings are on disk. The plan scales it to all US public targets with a merger proxy or tender-offer background section, which is thousands of deals. **Risk:** by 2028 or 2029, language-model extraction of filings will be common. So the moat must be the question and the model, not the extraction. For each idea, name the question that no one else with the same data would ask.

**Close work inside the supervision team.** "Deal Terms in Takeovers" (Gorbenko, Green and Mirani, working paper, 2025–26) reportedly uses offer-level data on about 673 mergers and a structural model of bid terms and conditions. A solo job-market paper must not overlap it. Gorbenko and Malenko (JF 2014), Gorbenko (JFE 2019) and Gorbenko and Malenko (JF 2024) are Alex's main takeover-auction papers. An idea that only repeats them on new data is weak.

## 3. Assets and paths

All paths are on this machine. The phase 0 dossier summarizes them: `/home/uctpiaj/work/Projects/competition-creates-competition/audit/jmp_search_2026_10_30/phase0/DOSSIER.md`. Read the dossier first. Then read the sources you need.

| Asset | Path |
|---|---|
| CCC manuscript (order-slot version, LaTeX) | `/home/uctpiaj/work/Projects/competition-creates-competition/overleaf/slot/` (`main.tex`, `sections/`, `appendix/`) |
| CCC compiled PDF | `/home/uctpiaj/work/Projects/competition-creates-competition/audit/jmp_search_2026_10_30/briefs/ccc_order_slot_main.pdf` |
| Informal bids: structural model and HMC estimator | `/home/uctpiaj/work/Projects/HMC_sim/Informal_bids/` (`README.md`, `SPEC.md`, `reports/`, `design/`) and `/home/uctpiaj/work/Projects/HMC_sim/Informal_bids_a1/` |
| HMC reading-group plan | `/home/uctpiaj/work/Projects/HMC_sim/talk_reading_group/` |
| Sale-process ledgers (with Alex) | `/home/uctpiaj/work/Projects/sec-auction/` (`README.md`, `SEC_Deal_Ledger_Extraction_Instruction.md`, `_dev/STATUS.md`, `_dev/ALEX_ALIGNMENT.md`, `ref/` with Alex's collection instructions, voice notes and hand-coded deals) |
| WRDS access, verified | SDC M&A (`sdc.wrds_ma_details`, `sdc.wrds_ma_events`, `sdc.wrds_ma_competition`), CRSP daily (`crsp.dsf`, `crsp.dsi`), the CRSP-Compustat link, Compustat, IBES, WRDS SEC filing index (`wrdssec.dforms`). TAQ access is not checked |
| Options data | ThetaData archive on RDSS (`/mnt/rdss/austin/data/`) |
| Case files of 8 public sale processes | `/home/uctpiaj/work/Projects/competition-creates-competition/empirical/private/` |
| CV | `/home/uctpiaj/work/Projects/JobSearch/Austin_cv.tex` |

## 4. Scoring rubric

Score each idea from 0 to 10 on each criterion. The weights are fixed:

| Criterion | Weight | Question |
|---|---|---|
| Originality | 30 | Has a top-3 finance referee seen this question or mechanism before? |
| Importance | 25 | Does a JF, RFS or JFE editor care about the answer? Does it change how people think about M&A? |
| Practicality | 25 | Is the theory tractable? Does the data exist or can Austin build it? Does it fit in the time before fall 2029? |
| Placement power and fit | 20 | Would the paper get flyouts at strong business schools? Does it use Austin's comparative advantage: theory plus structural estimation, sale-process data, options and microstructure data, Bayesian computation? |

**Your scores are provisional.** The synthesis rescores every idea on one common scale. Score honestly, and do not argue for your own scale.

**Structural flag:** mark "yes" if the idea leads to a credible structural estimation with identified primitives and a policy-relevant counterfactual.

## 5. Output format

Write one Markdown file to the path in your role brief. Use this structure:

1. **Longlist.** About 10 ideas, one line each. Give each idea a short title, its scores on the four criteria, and the structural flag.
2. **Top 3 pitches,** about one page each:
   - **Question:** one sentence.
   - **Why business schools care:** the economic stakes.
   - **The new fact or result:** what the paper shows that no one knows now.
   - **Model:** the economic mechanism, in words. Name the key primitives. Do not derive.
   - **Data:** which sources, what sample, what must be built.
   - **Identification:** what variation identifies the effect or the primitives.
   - **Structural flag:** what is estimated and which counterfactual it answers. Write "not applicable" if there is none.
   - **The question no one else with the same data would ask.**
   - **Closest papers:** 3 to 5 references, with how this idea differs. Mark any reference you did not verify as "unverified".
   - **Main risk** and the **kill test:** the quickest check that would show the idea fails.
   - **Timeline to fall 2029:** what is done by when.
3. **One paragraph on CCC:** where it fits in your view. Is it a job-market paper, a second paper, or a component of one of your ideas?

Most of the value is in the pitches. Make them concrete, and sharp enough that an editor reads past the abstract.

## 6. Rules

- **Independence.** Do not read other files in `audit/jmp_search_2026_10_30/phase1/` or `phase2/`. Do not spawn subagents.
- **Read-only.** Do not edit any file outside your own output file. Do not commit. Do not run any extraction in `sec-auction`.
- **No derivations, no tests.** This is a brainstorm. Do not write proofs, simulations or tests. Your role brief may allow read-only sizing queries.
- **Shared browser.** Do not use the shared `vm_browser`. Other agents use it. Use ordinary web search if your role allows the web.
- **No contact.** Do not send email or messages, and do not contact anyone.
- **Substance over framing.** Austin wants bold framing. Critique what an editor or a hiring committee would stop on regardless of framing. Do not recommend hedges or caveats.
- **Web search.** If web search is not available to you, say so at the top of your output, mark every reference "unverified", and continue. Do not stall.
- **Plain economic language.** Name economic objects: bidders, targets, prices, entry, information. Do not use internal file names or pipeline words in the pitches, except in the Data field.
- **Do not anchor on CCC.** Most of your ideas should not be extensions of CCC.
- **Known CCC extensions.** If you propose a change to CCC, do not repeat directions already explored: Laplace noise against the order slot, costly research by the informed trader, private signals of the rival and the trader, a bargaining payment rule, reserve prices, many quality classes, other laws for preparation costs, and welfare from access to prices.
