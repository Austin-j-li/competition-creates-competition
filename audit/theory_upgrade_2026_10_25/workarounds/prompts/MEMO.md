# Brief: write WORKAROUNDS.md

You write the memo that closes a research study on five weaknesses in an economic theory paper. Austin, the single author, reads it to decide what the paper should claim.

## Read

1. `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/workarounds/prompts/BRIEF_common.md`: the model, the paths and Austin's goals. Ignore its task and output sections.
2. The weakness briefs `prompts/W1.md` to `prompts/W5.md` in the same folder.
3. The five referee reports by GPT Astra, `raw/W1_astra_check.md` to `raw/W5_astra_check.md`. These are the authority on what is true.
4. The solver files in `raw/` that the referee reports cite, where you need the derivation or the intuition. Solver files: W1_sol, W1_opus, W1_kimi; W2_sol, W2_opus, W2_muse-wonder (partial), W2_opus-takeover; W3_sol, W3_opus, W3_fable; W4_kimi, W4_sonnet, W4_opus_primitive_condition.json; W5_sol, W5_opus, W5_muse-wonder (partial), W5_opus-takeover.
5. `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/SCAN.md` for context (the reduction lemma, the generality table).

All paths are under `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/workarounds/` unless absolute. READ-ONLY on the repository except the one output file below.

## Rules for content

- Never recommend a statement the referee found false. Where the referee gave a corrected statement, use the corrected one. Where the referee left a point unclear, say so.
- For each weakness, choose the workaround by these criteria in order: true; bold and economically meaningful; fewest and most natural conditions; least new machinery. Combining a reformulation with a condition is allowed. So is concluding that the weakness is real and should simply be stated.
- The preparation cost stays two-point (zero with probability ρ, c_H otherwise). Do not propose a general cost law or a c_H rename.
- Record which model proposed each idea and what the referee confirmed or refuted, in one short line per weakness. Austin wants to see which family contributed what.

## Write `/Users/austinli/Projects/competition-creates-competition/audit/theory_upgrade_2026_10_25/WORKAROUNDS.md`

Audience: Austin wants intuition ("what works, what doesn't, what is the scope"), not an engineering breakdown.

Structure:
1. A short opening paragraph: the net effect for the paper.
2. One section per weakness (W1 to W5):
   - the problem in one or two plain sentences;
   - the workaround in plain words: what we now claim and why it is true;
   - the sentence the main text would carry (bold and plain, one to three sentences, in the paper's voice, "I");
   - what remains weak and how much it matters;
   - provenance: who proposed it, what Astra confirmed or refuted;
   - any manuscript error found along the way.
3. A short closing section: which workarounds make the paper stronger than the benchmark-only version, which are honest concessions, and how they change the six open decisions in SCAN.md (decision 3 on ownership in particular).
4. An appendix with the formal statements and conditions, compact, using the paper's notation.

Style: plain English, short sentences, active voice, no bold labels in running text, no hedging filler, no sales language. Use Unicode math in running text (Δ, τ, W_H), not LaTeX.

Your final reply must be at most 200 words: the output path and a plain summary of the recommendation for each weakness.
