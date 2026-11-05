# Role brief, phase 1: ideas that start from structural estimation (GPT Sol)

Read `CORE_BRIEF.md` in this folder, then `../phase0/DOSSIER.md`. You may read every source path in the core brief.

## Your angle

Generate job-market paper candidates whose core is a structural model of an M&A process. The model must be estimable with data Austin has or can build. The leading data source is the census of sale processes: contacts, NDAs, informal bids, formal bids, rounds and winners, plus prices from SDC and CRSP.

For each idea, state:
- the primitives to estimate;
- the moments or the likelihood that identify them, and the variation behind identification;
- the counterfactual a business-school audience cares about. Examples: a different sale procedure, a disclosure rule, a ban on standstills, a change in insider-trading enforcement, a different seller strategy;
- whether estimation is feasible with HMC tools like those in `HMC_sim/Informal_bids` (JAX, BlackJAX, Stan), and where it would be hard: likelihood without a closed form, multiple equilibria, selection.

Do not propose the joint informal-bids paper itself. A solo spin-off with a distinct question is allowed. Structural ideas outside M&A are allowed only if they are clearly stronger.

## Output

`/home/uctpiaj/work/Projects/competition-creates-competition/audit/jmp_search_2026_10_30/phase1/sol_structural.md`, in the format of section 5 of the core brief.

## Rules

The rules in section 6 of the core brief apply. No derivations, no code and no tests. Do not use the shared `vm_browser` or any browser tool. You may use ordinary web search if your tools allow it.
