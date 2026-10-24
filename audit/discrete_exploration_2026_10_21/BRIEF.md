# Team 2 brief: exploratory study of discrete trading (21 October 2026)

You coordinate a multi-model research team. This is an **exploratory** effort. The paper keeps
Laplace noise as its benchmark; nothing here edits the paper. The goal is to learn what a discrete
trading stage does to the paper's results, and whether modified setups or added dynamics can
recover lost results or produce new ones.

Repository root: `/home/uctpiaj/work/Projects/competition-creates-competition`. Write only under
`audit/discrete_exploration_2026_10_21/` (memos in `memos/`, scripts in `scripts/<memo stem>/`).

## 0. Baseline facts and decisions

- Paper: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders".
  Read it at the **pinned commit**: `git -C overleaf/paper show 9b9bf3ce1a94d5017042192e61c9ceb800d310ba:main.tex`
  (and `:online_appendix.tex`). Another team is revising the paper in a separate clone; do not read
  or edit `overleaf/paper-revision/`, and never edit `overleaf/paper/`.
- The author's decisions that apply here too:
  - **Reading N:** nature draws the challenger's quality class `j ∈ {H, L}` with prior `π`; the
    value comes from `G_j`; the investor sees the class; preparation reveals the value. Point
    masses at `ℓ`, `h` with `π = 1/2` are the benchmark special case.
  - **`c_L = 0`:** the low-cost type prepares at zero cost, so the entry floor `ρ` holds at every
    belief.
  - **One-directional (buy-only) orders** are the starting point for the discrete model.
- Prior work to read first (in `audit/alex_meeting_2026_10_21/`): `report.html` (overview),
  `memos/SYNTHESIS.md` (verdicts; Part B.2), `memos/Q2_discrete_buy_only.md`,
  `memos/Q2_discrete_sell_only.md`, `memos/Q2_discrete_literature.md`,
  `memos/V_discrete_check.md` (brute-force solver and results; its code is in
  `scripts/V_discrete_check/` and may be reused), `memos/LIT_extracts.md` (verified paper extracts).

### What is already known about the three-point model (equal noise 1/3, buy-only, c_L = 0)

The main mechanism survives: stronger incumbent → wider spread → informed buying pays → good
news → expensive entry. Propositions 2(i)–(ii) and the fixed-experiment control carry over, with
one exact cutoff `k = (2/3)ρ(1 − π)Δ_T` (benchmark `ρΔ_T/3`). But information is all-or-nothing:
middle flows carry no information, the top flow reveals the class, and the investor earns nothing
where entry is recruited. Lost or weakened: Proposition 3 (coexistence), the endogenous trading
asymmetry, the information ceiling behind Proposition 2(iii) (entry returns only above r ≈ 7.97),
the size of the effect (0.25 → 0.375), and robustness (equal noise is a knife-edge; the
Intuitive-Criterion belief at the off-path top flow is needed for existence).

### A candidate fix to verify FIRST (it rests on one unchecked script)

Noise = difference of two independent geometric counts of unit noise orders ("discrete Laplace"),
`P(z) = (1−a)/(1+a) a^{|z|}`, `a = e^{−1/b}`, buy-only orders, `c_L = 0`, benchmark auction values,
`b = 2`, `k = 0.02`, **`c_H = 5`**. Claimed: posteriors take two values in `[0.378, 0.622]`
(`m₁ = 1/(1+e^{1/b})`); every flow on path (no refinement needed); unique no trade at `r₀ = 1.2`
because `k > Δ_T(r₀)`; unique full buying at `r₁ = 3` because `k < ρ m₁ Δ_T(r₁) = 0.063`; entry
0.25 → 0.625 → 0.25 at `r = 1.2, 3, 4.2`; high-class ownership 0.125 → 0.358; admissible `c_H`
window `(4.80, 5.31]`; entry returns to `ρ` near `r ≈ 4` because the best price cannot justify
preparation (information ceiling restored); feedback present (at `r₁` a purchase earns +0.176 with
entry after good news vs +0.060 without), so a Proposition 3 analog may exist, possibly analytic.

## 1. Questions

**A. Consolidate the three-point model** (equal noise, buy-only, presence probability `λ ∈ (0, 1]`,
Reading N, `c_L = 0`): full equilibrium characterization with mixed strategies; a table of every
paper result (Props. 1–3, A.3–A.10, Sections 5–6) marked survives / changes / dies / not applicable.

**B. Verify and develop the discrete-Laplace model**: confirm or refute every claim above; a full
Proposition 2 analog with proof; an analog of Proposition 3 (coexistence) — analytic if possible;
welfare and ownership; the general-prior version.

**C. Recover or create results by modifying the setup or adding dynamics.** Spread the team across
this menu; each item should return at least one proposition with a status label, or a documented
failure:
1. Geometric-count noise with two-sided orders `{−1, 0, 1}`.
2. Two trading rounds before the entry decision (a price path; does information aggregate?).
3. An option to delay preparation (the challenger can wait and watch another price).
4. Several potential challengers in sequence (does entry cascade? does one entrant's decision
   inform the next through the price?).
5. An informed investor with a stake, in the discrete model (manipulation by buying).
6. Costly information acquisition by the investor (does competition raise research incentives?).
7. The incumbent responds to the price (jump bids or preemption, as in Fishman 1988).
8. The seller sets the reserve after it observes the price.
9. Unequal noise with challenger mixing at indifference: a discrete analog of Proposition 3.
10. Anything else promising (for example the challenger trades before it enters, or target
    disclosure), if you can justify it.

**D. Literature** on discrete feedback models with dynamics, sequential entry, real options with
learning from prices, and manipulation through real decisions. Paper fetching and reading go
through the browser (see §2).

## 2. Team and tools

- [Two bullets on the delegation set-up removed before publication on GitHub.]
- **Browser tasks run one at a time** through the shared browser on the VM
  (list the existing tabs, open its own tab, close it at the end, never close the
  user's tabs, no logins, no downloads saved). The browser blocks `file://`; for visual checks of
  an HTML report, serve the folder on `127.0.0.1` with a free port (not 8765), and stop the server
  afterwards.
- Pair the analytical work: each key claim gets a second, independent derivation or a brute-force
  check by a second, independent member.
- CPU: another team runs heavy numerics on this machine. Use **at most 8 worker processes** in
  total for brute-force runs.
- The root disk has little space (about 1.6 GB free). Keep large outputs on
  `/home/uctpiaj/work`; do not install packages; Python is
  `/home/uctpiaj/work/Projects/competition-creates-competition/.venv/bin/python` (numpy, scipy,
  mpmath).

## 3. Rules

1. Do not write tests of any type. Print-only scripts are allowed; scripts with assertions are not.
2. Do not edit anything outside `audit/discrete_exploration_2026_10_21/`. Do not commit or push.
3. Do not name AI models, agents, or tools in memos or the report.
4. Status labels: analytical, computer-assisted, numerical diagnostic, conjecture, open. Show every
   derivation. A documented failure is a result.
5. Cite only verified sources; mark others "unverified".
6. Do not hand any part of your task to others.

## 4. Deliverables

1. Memos in `memos/`, each with: question; setup; results with status and derivations; what it
   recovers or loses relative to the Laplace paper; numerical example; open issues; a plain summary
   of at most 300 words.
2. `memos/SYNTHESIS.md` after a red-team pass: verdicts on the key claims, a ranked list of the
   modifications that recover or create results, and a recommendation.
3. `report.html`: a polished, plain-language report in the style of
   `audit/alex_meeting_2026_10_21/report.html` (theme variables with fallbacks, inline SVG charts,
   status chips, responsive layout, no model names). Check it visually at 728 px and 390 px,
   light and dark.
4. A final summary: what was found, the strongest new results and what remains open.
