# Role brief, phase 2: novelty check of the shortlist (GPT Astra, with the shared browser)

Read `CORE_BRIEF.md` in this folder (sections 1, 2 and 4), then `../phase2/SYNTHESIS.md`. You may read any file in `../phase1/` for the closest papers that each source cited.

## Your task

For each of nine shortlisted ideas, decide how new it is. Find the closest published papers and working papers. Read them, do not rely on search snippets. Then say what would still be new, or say that the idea is occupied.

## Tools

Use the shared Chrome browser (`vm_browser`) to open and read full papers: SSRN, NBER, journal pages, authors' sites, Google Scholar. You are the only agent that drives the browser now.
- **Open new tabs for your work.** You may close only tabs that you opened.
- **Never touch tabs 0 to 4.** They hold Austin's mail, two Overleaf projects and a ChatGPT chat. Do not select, navigate, reload or close them.
- Do not sign in to anything, submit forms or download files.
- Ordinary web search is also fine.

## Specific questions

Answer each question with references, each marked **read** (you opened the full text or the abstract page) or **unverified**.

**First, "Deal Terms in Takeovers"** (Gorbenko, Green and Mirani, March 2026 draft; try `https://www.brettgreen.info/drafts/deal_terms.pdf`; a 30 October 2026 seminar abstract mentions 820 mergers). Read the introduction, the data section and the model section. Report exactly which process objects it covers, with page numbers: exclusivity, deadlines and final rounds, standstills, diligence access, bid revisions, regulatory conditions, financing, losing bidders, prices after signing. This one read decides the overlap for several ideas below.

1. **A. Seller commitment.** Has anyone measured how often "final" rounds or bid deadlines in takeover sales reopen, or estimated the cost of a seller's limited commitment? Check structural work on auctions with limited commitment in any market (procurement, real estate, spectrum, used goods). Check work on banks or advisers with a reputation for hard deadlines.
2. **B. Process leaks.** Has anyone aligned confidentiality-agreement (NDA) or first-contact dates from "Background of the Merger" sections with stock or option trading on those dates? Has anyone related the number of parties under NDA to informed trading before announcements, beyond Acharya and Johnson (2010)? Has anyone shown that leak risk changes the breadth of sale processes? Read Szydlowski ("Leaks and Takeovers") and Fidrmuc and Xia (2022).
3. **C. Standstills.** Has anyone studied, empirically, how "don't ask, don't waive" standstills, or the 2012 Delaware decisions (Complete Genomics, Ancestry.com), changed participation, topping bids or prices? Is there a model of standstills beyond Sautter (2013)?
4. **D. Informative exits.** Has anyone documented clustered bidder exits after data-room access or management presentations, or the effect of one bidder's withdrawal on other bidders in takeover sales?
5. **E. The price after exclusivity.** Has anyone compared the final merger price with the winner's last bid before exclusivity ("re-trading", price cuts in exclusive talks)? Does any paper relate exclusivity length to price changes?
6. **F. Antitrust selects the buyer.** Has anyone studied how antitrust risk changes which bidders enter a sale process or win, before announcement?
7. **H. The proxy reveals the auction.** Has anyone studied the market reaction to the first filing of the background section (PREM14A or SC 14D9), or used the disclosed runner-up bid to predict topping bids or merger-arbitrage spreads?
8. **I. The private-equity floor.** Has anyone shown that credit conditions move the prices that strategic acquirers pay when a private-equity fund is the runner-up, or that credit changes fund entry within a sale process?
9. **J. Competition for the record.** After Corwin (2015) and Trulia (2016), has anyone separated the number of contacts in a market check from the bidders' real opportunity to bid? Read Cain, Griffith, Jackson and Davidoff Solomon, and Gatti and Gelter.

**Last, with at most a fifth of your effort:** list 5 to 10 job-market papers from 2022 to 2026 on M&A or sale processes, with the author, the school, the verified placement and the title. Use school placement pages, candidate pages and SSRN. Prefer fewer verified entries over many guesses.

## Output

`/home/uctpiaj/work/Projects/competition-creates-competition/audit/jmp_search_2026_10_30/phase2/astra_novelty.md`. For each idea give:
- a verdict: **open**, **partly occupied** (say what remains open) or **occupied**;
- the 3 to 6 closest papers, each with one sentence on its content and one on the difference;
- the single fact that decides the verdict.

Start the file with the Deal Terms report.

## Rules

- Write only your output file. Do not edit other files and do not commit.
- No code, no derivations and no tests. Do not start subagents.
- Do not contact anyone.
- Plain language and short sentences.
