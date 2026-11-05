# Role brief, phase 1: ideas that start from data (Opus C)

Read `CORE_BRIEF.md` in this folder, then `../phase0/DOSSIER.md`.

## Your angle

Generate job-market paper candidates that start from data Austin has or can build:
- the census of sale processes from merger filings;
- SDC, CRSP, Compustat, IBES and the SEC filing index on WRDS;
- the ThetaData options archive;
- TAQ, if access exists.

Look for a new fact that matters. Then give a reduced-form design that establishes it, and a structural design that explains it and supports a counterfactual. For each idea, name the question that no one else with the same data would ask.

## Sizing counts (allowed)

**Do not connect to WRDS.** A login there waits for a two-factor approval on Austin's phone, so it stalls.

Instead, size the filing samples from the public EDGAR quarterly form indexes: `https://www.sec.gov/Archives/edgar/full-index/<year>/QTR<n>/form.idx`. Example: count the DEFM14A, PREM14A, SC TO-T and SC 14D9 filings per year from 2000 to 2025.
- Send the header `User-Agent: Austin Li junyu.li.24@ucl.ac.uk`. This is the string that the ledger tools use. Make at most 5 requests per second.
- Stream each index and count in memory. Do not save the indexes.
- If you must save a result, save it under `/mnt/rdss/austin/data/competition-creates-competition/jmp_sizing_2026_10_30/` with a receipt: source, request, date, size and SHA-256. Never write data to `/home/uctpiaj/work` or `/tmp`.
- For counts that need SDC or TAQ, use sample sizes from published papers and cite them, or mark the count "to run on WRDS".
- Report each count with the request that produced it.

## Output

`/home/uctpiaj/work/Projects/competition-creates-competition/audit/jmp_search_2026_10_30/phase1/opusC_data.md`, in the format of section 5 of the core brief. Add a section "Sample sizes" with the counts and their queries.

## Rules

The rules in section 6 of the core brief apply, except that the sizing counts above are allowed. You may use ordinary web search. Do not use the shared `vm_browser`.
