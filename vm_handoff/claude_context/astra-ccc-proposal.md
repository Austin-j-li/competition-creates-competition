---
name: astra-ccc-proposal
description: 2026-09-05 GPT Astra proposed an alternative upgrade project, "Competition Creates Competition" (takeover entry reversal via target-price feedback); Fable verified the theorem and found the reversal is a regime switch
metadata:
  type: project
---

On 2026-09-05 Austin brought a GPT Astra 6 Pro research proposal, "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders" (`~/Downloads/Competition_Creates_Competition_Project_Proposal.md`), as a candidate replacement for the blockholder paper's failed hump ([[hump-parity-artifact]]). Model: second-price takeover auction with incumbent R~U[0,r], challenger θ∈{ℓ,h}, informed speculator trades target stock (bounded orders, linear cost k, Laplace noise), challenger learns from price before paying diligence cost.

**Why:** Fable's independent check (scratchpad `ccc/verify.py`) reproduced every reported number and found the proof valid. But the "reversal" is a two-point comparison across a trading regime switch: entry is flat at ρ while Δ_T(r)<~k, jumps when informative trading turns on (r≈1.7 in the example), then declines in r and collapses back to ρ when the high-cost threshold exceeds the posterior ceiling 1−μ_ (r≈3.58). Theorem's sufficient bounds are ~4x loose in Δ_T (certified r_0<1.22, r_1∈(2.84,3.58); actual switch ≈1.70 where Δ_T≈7.2k vs the required 29.8k). Seller-optimal reserve p>ℓ makes both economies informative and removes the reversal (proposal's own §11.4).

**How to apply:** If Austin pursues this project, insist on the full E(r) curve as the headline figure, the complementary-signals extension (trader knows the acquirer's own synergy is the seminar-killer), a first-price/negotiation comparison (engine is a second-price identity Δ_T=E[(R−ℓ)_+]), and citing Edmans–Goldstein–Jiang 2012 JF. Ask for the `verification/` archive before trusting the executed-checks claims.

**Update 2026-09-05 (round 2):** Astra's rebuttal found asymmetric equilibria (q_H=1, q_L=-v) at r=1.55–1.65 that my symmetric scan missed; verified exactly. Multiplicity region is ~[1.53, 1.75], and the informative branch is single-peaked near r≈1.70. Also conceded: h=2 works with k=0.002 under the theorem's own conditions; logistic cutoff is 1.5 SD; ceiling is from bounded likelihood ratios. Astra added a two-signal theorem (buyer signal 75% > trader 70%, entry still rises) and a bargaining lemma Δ_η=η(h−ℓ)+(1−2η)E[(R−ℓ)_+]. Lesson: scan asymmetric profiles before claiming a multiplicity map.

**Decision 2026-09-05:** Austin is going with Astra's version of the paper. Astra builds the manuscript bone (main.md + appendix.md, Markdown with LaTeX math); Claude then creates a NEW repository, ports Astra's verification directory, runs the numerical specs from appendix C, fills `[[name]]` placeholders, and converts to LaTeX. Empirics scaffold only this round. No deadlines in documents; state status neutrally; no "theorem is killed if" language.

**Repo created 2026-09-05:** `AustinJunyuLi/competition-creates-competition` (private), local `/Users/austinli/Projects/competition-creates-competition`. Contains Astra's `paper/main.md`, `paper/online_appendix.md`, `paper/quantity_manifest.csv`, plus CLAUDE.md, HANDOFF.md, KICKOFF_PROMPT.md. Missing from Astra's delivery: `references.bib` and the `verification/` directory. Execution session fills 78 derived placeholders via Online Appendix C.
