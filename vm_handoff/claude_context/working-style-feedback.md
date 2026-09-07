---
name: working-style-feedback
description: "How Austin wants this repository's writing and figure work done (unslop always, subagents for speed, concrete figure rework, Gorbenko voice)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 06d99d85-bea9-4c4f-b9d2-0dbbd46f50cc
  modified: 2026-09-05T17:13:53.184Z
---

On 2026-09-05 Austin rejected a first plan for the manuscript rewrite twice, with three instructions: run the `unslop` skill on all prose I write; rework the graphs concretely (the first renders had overflowing legends and text on top of data, and he called them unpleasant), not just recolor them; and use subagents to expedite large jobs.

**Why:** He reads the output as a finance paper, not as engineering output. Visible AI tells in prose and sloppy figure layout cost him credibility with referees, and a serial single-agent rewrite of a 10k-word paper is too slow for him.

**How to apply:** Any prose for `paper/` goes through unslop before it is shown. Figures are judged from rendered PNGs, iterated until no label touches data, and checked in grayscale. Big editorial or numerical jobs are split across forked subagents writing to separate files, then assembled and voice-checked by the parent. The paper is single-authored: "I", never "we". Voice model: Gorbenko's JF 2024 paper and 2025 handbook chapter (few propositions with descriptive titles, intuition paragraphs after each, proofs in appendix). See [[bold-framing-brief]] and [[numerics-build-status]].
