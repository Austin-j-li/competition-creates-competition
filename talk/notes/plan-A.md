# Structure plan A (concrete-first): 40-minute session

Paper: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders" (Austin Li).
Stance: author presentation. Genre: conference or job-market talk for a generalist finance-economics room.
Angle A: open on the institutional decision interval, then the received deterrence logic, then the twist and the benchmark numbers as the punchline. The mechanism is built from one auction payoff comparison (frames 7-8) and one price-inference step (frames 9-10).

Number rule used throughout this plan. Every slide number is a registry value (`numerics/quantity_registry.csv`) or a value printed in the paper's Tables 1-4 (`tables/*.tex`, same-stem CSV). Slides show three significant digits, rounded from the registry display. The registry name and full display go in a LaTeX comment and in a shared `talk/results.tex` macro. Certificate enclosures (A7) are shown exactly as the registry displays them and are never re-rounded, because their rounding is outward. A derived number shows its arithmetic in a comment. The single derived number on the main line is 0.0224 (frame 10) = `base_k` 0.02 + `base_margin_strong_trade` 0.00241. Values that exist only in validated CSV output and are printed neither in the paper nor in the registry are kept off the slides: τ = 0.705 and x* = 0.871 at r1 (`tables/equilibrium_controls.csv`), and B_{r1}(M) = 6.217 and B_{r2}(M) = 5.997 (`tables/auction_primitives.csv`). If the author wants any of them on a slide, add a registry key first.

---

## 1. Settings and budget

| Item | Setting |
|---|---|
| Total session | 40 minutes, including questions and interruptions |
| Planned speech | 31.25 minutes (78%): title 0.25 + 17 content frames 31.0 |
| Question reserve | 8.75 minutes (22%) |
| Content frames | 17 (frame 12 is a two-step build, 12a and 12b, made by duplicating the frame; it counts once) |
| Appendix | 18 backups after `\AppendixStart`. Each is reached from exactly one main-frame origin via `\PlaceNav` and returns there via `\BackButton` |
| Punchline | Frame 3 starts at 3.5 min. The headline numbers are on screen and spoken by about 4.25 min |
| Class and theme | `\documentclass[11pt,aspectratio=169]{beamer}`, `\usetheme{Madrid}`, `\usepackage{econ-slides-compat}`, `\usefonttheme[onlymath]{serif}` (F29), XeLaTeX |
| Title page | `[plain]`; paper title on two balanced lines; "Austin Li" only; no affiliation, venue or date |
| Overlays | None. No `\pause`, `\only`, `\onslide`, `\uncover`. A build is a duplicated frame (12a to 12b) |
| Density caps | ≤ 7 bullets, ≤ 2 display equations, ≤ 2 colored boxes per frame (at most one ResultBox on the main line, on frame 11) |
| Ending | Frame 17 (Conclusion) is the last main frame. No navigation on it and no "Thank you / Questions" frame |
| Literature | No review section. Frame 4 is a one-frame positioning against four antecedent groups. References sit in the appendix (A18) |
| PowerPoint | Every frame can be rebuilt 1:1 in native PowerPoint: text, native tables, equations, pictures of figures (paper PDFs or talk rebuilds from CSV), and two simple native diagrams (a five-box timeline and one arrow chain). No TikZ plots |
| Files | Deck at `talk/talk-A.tex` with shared macros in `talk/results.tex`. Talk figures go in `talk/figures/`, written by one plotting script `talk/figures/build_talk_figures.py` that reads CSV only and never solves |

## 2. Author story

**Research question.** When a listed target is in play, one bidder is already prepared, and a second bidder must decide whether to pay preparation costs while it watches the target's stock price, does a stronger incumbent keep that challenger out, or can it draw the challenger in? (main.md 13, 17, 31-37)

**Answer, with the headline number.** A stronger incumbent can draw the challenger in by making the stock price informative about the challenger. At the benchmark, moving the incumbent from r0 = 1.2 to r1 = 3 lowers the challenger's expected profit at the prior from 4.80 to 4.29 (`base_profit_prior_weak`, `base_profit_prior_strong`). Entry still rises from 0.250 to 0.523, +27.3 percentage points (`base_entry_weak`, `base_entry_strong`, `base_entry_change_pp`), and high-value challenger ownership rises from 0.125 to 0.324 (`base_ownership_weak`, `base_ownership_strong`). Proposition 2, analytical, main.md 216-233 and 257.

**Why it matters.** The standard view, and much of the takeover-contest literature, treats a strong incumbent as preemptive. That holds when the entrant's information is fixed. When the entrant learns from a market price before it commits, sale rules, the strength of the known bidder, and price informativeness jointly decide who competes. That changes how one reads bidder-pool formation, sale-process design, and the welfare value of trading in targets.

**Contribution: the four items (talk-structures.md, "Choose the author story").**
1. *Primary takeaway:* competition creates competition. A stronger incumbent can turn an uninformative price into an informative one and raise entry and high-value ownership, with unique trading and on-path entry in each economy (Prop. 2, analytical).
2. *Supporting claims (at most two):*
   (a) *Mechanism.* One auction comparison and one price-inference step. A stronger incumbent lowers the challenger's profit and widens the target-payoff spread Δ_T (Prop. 1, analytical). A wider spread makes informed trading pay, and the resulting price tells the challenger when expensive preparation is worthwhile (eqs. 7-11).
   (b) *Information is the channel.* Freeze the investor's orders and entry falls, 0.562 to 0.523 (numerical diagnostic; the sign is analytical, Prop. A.3). Hide the price and entry is 0.250 at both strengths (analytical).
3. *Strongest credibility argument:* uniqueness comes from global bounds, not from a guessed profile. The weak economy's gross advantage is capped by Δ_T(r0) < k. In the strong economy, each marginal unit of a correctly signed order earns more than k for every candidate schedule, with arbitrary mixed orders and every unilateral deviation q ∈ [-1, 1] allowed. Prices are rational, so the result is not an artifact of mispricing.
4. *Boundary audit:* the effect is not monotone in strength. At r2 = 3.6, above the high-cost ceiling r_C ≈ 3.59 (`base_r_high_cost_ceiling`), trading stays fully informative but entry returns to 0.250 (`base_entry_collapse`). This is shown once, beside the evidence, on frame 12b, because leaving it out would let "stronger incumbents attract entry" be heard as a monotone claim. Secondary boundaries stay off the refrain: the intermediate correspondence is open (frame 14), the seller's optimal terms are open (A12), and there is no empirical estimate (A14).

**Formal payoffs actually earned (not counted as contributions):** a two-returns comparative static (Prop. 1); price sufficiency with bounded posteriors (Props. A.1-A.2); the reversal theorem (Prop. 2); a fixed-experiment deterrence result (Prop. A.3); computer-assisted coexistence (Prop. 3); robustness (Props. A.5-A.7); welfare of price access at r1 (Prop. A.9); payment-rule dependence (Prop. A.8).

**Mechanism classification: competing forces, with a complementary chain inside one of them.**
- Force 1, deterrence (inherited): a stronger incumbent lowers g_H, g_L and B_r(μ) at every fixed belief, so entry falls at any fixed experiment (Prop. A.3).
- Force 2, information (new): the same shift widens Δ_T, which raises the investor's residual advantage (entry probability × Δ_T × residual uncertainty).
- Chain inside force 2: Δ_T up → informed trading pays (trading-cost window) → informative price, with beliefs spanning [m, M] → good news crosses τ (high-cost window) → the expensive challenger enters → entry and O_H rise.
- Dependency: force 2 needs the low-cost floor, so that target proceeds depend on θ at every price, and needs the price to be seen before preparation. The net sign is settled by the three named conditions. Force 1 reasserts at very high strength (r2), where even M cannot justify c_H.
- Frame architecture: frames 7-8 give both forces the same skeleton (object, the decision it moves, sign) from one auction comparison, as the two panels of one exhibit. Frames 9-10 carry the price-inference step. The chain line on frame 10 and the intuition line on frame 11 are the synthesis before and at the proposition.

## 3. Claim-evidence ledger

| # | Claim (slide wording) | Status | Paper location | Registry names |
|---|---|---|---|---|
| C1 | A stronger incumbent lowers challenger gross profit at every fixed belief and raises the target-payoff spread | supported (analytical, Prop. 1, any continuous F) | main.md 99-137, eqs. 4-6 | `base_spread_weak`, `base_spread_strong`, `base_profit_prior_weak`, `base_profit_prior_strong` |
| C2 | Target proceeds differ across challenger types only when R > ℓ, by R − ℓ | supported (analytical) | main.md 137 | none (payment rule) |
| C3 | Any price-based belief lies in [m, M]; the challenger can read the market's belief off the price, with atoms and jumps allowed | supported (analytical, Props. A.1-A.2) | main.md 150-195, eqs. 7-10 | `base_m`, `base_M` |
| C4 | Informed trading loses against the weak incumbent and must be at full size against the strong one | supported (analytical) | main.md 197-237, eq. 11 | `base_k`, `base_margin_weak_trade`, `base_margin_strong_trade` |
| C5 | Weak r0: unique no trade, uninformative price, entry ρ | supported (analytical, Prop. 2 i) | main.md 231 | `base_entry_weak`, `base_ownership_weak` |
| C6 | Strong r1: unique full orders, informative price, entry > ρ, high-value ownership up | supported (analytical, Prop. 2 ii) | main.md 231, 257 | `base_entry_strong`, `base_ownership_strong`, `base_entry_change_pp` |
| C7 | (i)-(ii) hold on a nonempty open set of primitives, for every h > ℓ | supported for (i)-(ii) only (F46) | main.md 233, 767 (A.25); Sec. 5.2 | `base_minimum_theorem_margin`, `moderate_minimum_theorem_margin` |
| C8 | Stronger still (r2): full orders, entry back to ρ | supported at the benchmark and nearby parameters; the claim for every h > ℓ is **excluded** (F46) | main.md 233 (iii), 257 | `base_entry_collapse`, `base_r_high_cost_ceiling` |
| C9 | Freezing orders restores deterrence: 0.562 → 0.523 | numbers: numerical diagnostic; sign: supported (analytical, Prop. A.3) | main.md 267, 554 | `base_frozen_entry_weak`, `base_frozen_entry_strong` |
| C10 | Hiding the price leaves entry at 0.250 at both strengths | supported (analytical; equilibria of the no-price-access game, F08) | main.md 269; Table 2 Panel B | `base_hidden_entry_weak`, `base_hidden_entry_strong` |
| C11 | The reversal runs through what the price reveals | supported, as a comparison of model economies (C9 + C10). Not a causal empirical claim | main.md 269 | as C9, C10 |
| C12 | At r = 1.55, 1.60, 1.65 an informative equilibrium coexists with no trade; entry intervals are strictly ordered upward | supported (computer-assisted, Prop. 3) | main.md 273-287, eq. 13 | `cert_a_r`..`cert_c_r`, `cert_a_v_interval`..`cert_c_v_interval` (shown negated as q_L), `cert_a_entry_interval`..`cert_c_entry_interval` |
| C13 | Coexistence at all intermediate strengths; a continuous branch between the nodes | **excluded** (open; F48) | main.md 296-304 | none |
| C14 | Thresholds: no trade unique below r_P ≈ 1.22, an equilibrium up to r_N ≈ 1.75; full orders unique above r_U ≈ 2.84; expensive entry impossible above r_C ≈ 3.59 | supported (analytical, Prop. A.4) | main.md 296, 568-602 | `base_r_pool_unique_sufficient`, `base_r_no_trade_exact`, `base_r_full_unique_sufficient`, `base_r_high_cost_ceiling` |
| C15 | The r0 → r1 reversal survives logistic noise, atomless costs, a small value gap, and complementary signals | supported (analytical, Props. A.5-A.7, Table 3) for r0 → r1 only (F47) | main.md 309-341 | `logistic_entry_strong`, `cost_mix_laplace_entry_strong`, `cost_mix_logistic_entry_strong`, `moderate_entry_weak`, `moderate_entry_strong`, `moderate_entry_change_pp`, `signal_entry_weak`, `signal_entry_strong`, `signal_entry_change_pp` |
| C16 | Across the complete accuracy grid the reversal holds generally | **conflicted** (rises in 6 of 25 cells; falls when d ≥ 0.76, F16). The slides state the declared example plus the grid footnote (A9) | main.md 336; OA C.3; `tables/table_signal_grid.tex` | `signal_trader_accuracy_value`, `signal_buyer_accuracy_value` |
| C17 | At r1, price access raises target proceeds and net acquisition surplus | supported (analytical, Prop. A.9) at r1 only | main.md 347-353; Table 2 Panel C | `base_revenue_feedback`, `base_revenue_hidden`, `base_revenue_gain`, `base_net_surplus_gain` |
| C18 | Price access helps "at any fixed strength" | **conflicted** (intro main.md 23 vs Prop. A.9; F15). The slides use the r1 wording and add "at r0 no gain" | main.md 23 | none |
| C19 | Matched dividend: mean prices match but entry does not, so information matters, not the price level | descriptive only (diagnostic). Status is **conflicted** in the source: text says "analytical invariance diagnostic", registry says numerical diagnostic (F10). The slides tag it "diagnostic" | main.md 353 | `base_matched_dividend` |
| C20 | Under Nash bargaining, stronger competition weakly lowers challenger profit for every η; the spread effect is weakly positive for η < 1/2 and weakly negative for η > 1/2 | supported (analytical, Prop. A.8; "weakly", F49) | main.md 357-372 | none (figure data `figures_data/bargaining.csv`) |
| C21 | An entry reversal under bargaining | **excluded** (not solved; open) | main.md 378 | none |
| C22 | Raising the reserve 0.5 → 1.1 raises expected proceeds at both strengths (listed nodes) | supported (analytical at listed nodes) | main.md 383-392; Table 4 | `value_revenue_weak_low_p`, `value_revenue_weak_high_p`, `value_revenue_strong_low_p`, `value_revenue_strong_high_p`, `value_entry_weak_high_p`, `value_entry_strong_high_p` |
| C23 | An optimal reserve or optimal sale terms | **excluded** (open) | main.md 392, 408 | none |
| C24 | Same orders can support different price pools, beliefs and entry | supported (analytical existence, Prop. A.10), backup only | main.md 394, 991-1047 | `pool_reserve`, `pool_posterior_cutoff_low`, `pool_posterior_cutoff_high`, `pool_entry_cutoff_low`, `pool_entry_cutoff_high`, `pool_revenue_cutoff_low`, `pool_revenue_cutoff_high` |
| C25 | Disclosure records show a costly preparation stage (Imprivata) | descriptive only | main.md 37 | none |
| C26 | Prices drew a buyer into any real deal; benchmark magnitudes are calibrated | **excluded** (no sample; declared benchmark only) | main.md 37, 402-404 | none |
| C27 | The strong price experiment strictly Blackwell-dominates the weak one | supported (analytical, Prop. 2 ii) | main.md 233 | none |
| C28 | Extra entry is tilted toward high-value challengers (α_H > α_L) | supported (analytical) | main.md 239-253, eq. 12 | none |
| C29 | "Uniqueness allows every continuous deviation" | **conflicted** wording (F37). The slides say "every unilateral deviation q ∈ [-1, 1]" | main.md 21, 233 | none |

## 4. Emphasis ledger

- **Primary takeaway (frames 3, 11, 12, 17):** a stronger incumbent can bring the challenger in, because it makes the target's stock price informative. At the benchmark, entry goes from 0.250 to 0.523 while the challenger's profit at the prior falls from 4.80 to 4.29 (analytical).
- **Support 1, mechanism (frames 7-10):** one auction comparison (spread up, profit down) and one price-inference step (the price reveals the market's belief; trading pays only when the spread is wide).
- **Support 2, information controls (frame 13):** freeze orders and entry falls, 0.562 → 0.523 (numerical diagnostic; sign analytical); hide the price and entry stays at 0.250 (analytical).
- **Boundary (frame 12b only):** rise, then fall. At r2 = 3.6 > r_C ≈ 3.59, trading stays informative but entry returns to 0.250. It is not repeated on frame 3 or frame 17.

Frames 14-16 (coexistence, robustness, welfare) are secondary results that deepen the story. They are the first cuts if the talk runs behind (section 10).

## 5. Color ledger

Madrid's structure blue (indigo, `#3333B3`) carries titles, the ResultBox, `\RunIn` labels and `\KeyIdea`. Concept colors are declared once in the preamble and never used as a good/bad pair:

```latex
\colorlet{cInfo}{cAccentB!80!black}  % #AA4B00, contrast 5.6:1 on white
\colorlet{cCost}{cAccentC!70!black}  % #006F50, contrast 6.2:1 on white
```

| Object | Baseline or new | Alias | Frames where it recurs |
|---|---|---|---|
| Target-payoff spread Δ_T (and the words "target-payoff spread") | new (the paper's wedge) | `cInfo` (cAccentB darkened) | 7 (display), 8 (panel (a) line, same hex in the rebuilt figure), 10 (display, weak/strong lines, trading-cost window), 11 (trading-cost window in the box), A1, A2, A11 (Δ_η line in the rebuilt Figure 4) |
| The information chain "wider Δ_T → trading pays → informative price → good news crosses τ → expensive challenger enters" | new (mechanism) | `cInfo` | 10 (chain line), 11 (intuition line, "what the price can tell" phrase only) |
| Preparation costs c_L, c_H, the probability ρ, the words "cheap / expensive preparation" | inherited primitive, colored separately per F30 | `cCost` (cAccentC darkened) | 6 (cost bullet, low-cost floor), 8 (dashed c_H = 6 line in panel (b)), 9 (c_H in the τ display, high-cost window), 10 (ρ in the lower bound), 11 (three conditions), 12b (ρ in the takeaway), A2, A4, A15 |
| Challenger profit g_H, g_L, B_r(μ); deterrence | inherited (baseline force) | neutral black; the curves in the rebuilt panel (b) are black and two grays | 2, 7, 8, 9, 11 |
| Entry E, ownership O_H, orders (q_H, q_L), strengths r0, r1, r2 | outcomes and labels | neutral; the strong-economy row is **bold** in tables | 11-17 |
| Result-status labels | bookkeeping | gray `\scriptsize` | 7, 8, 11-16 and backups |

Unused on purpose: `cAccentA` (Okabe-Ito blue sits too close to Madrid's structure blue), `cAccentD` (amber is under 4.5:1 on white), and `cHighlight` (no overlays). At most two concept colors are active on any frame (frames 9, 10, 11: `cInfo` + `cCost`).

## 6. Notation plan

### 6.1 Symbols on the main line

| Symbol | Introduced on frame | Gloss on the slide | Audit rule applied |
|---|---|---|---|
| r; R | 5 | "incumbent value R ~ U[0, r], known only to itself; r = incumbent strength (public)". Later only "strength r0 → r1", never a bare r beside R | F31, F19 |
| θ ∈ {H, L}; h, ℓ | 5 | "challenger quality θ ∈ {H, L}, worth h or ℓ, equally likely". θ is never written as a number | F01 |
| p | 5 | "reserve price p", said aloud at first use. The stock price is always in words (no P on the main line) | F31 |
| C; c_L, c_H; ρ | 5 (C), 6 (the rest) | "Entry = the challenger pays preparation cost C (learns θ, can bid)"; "C = c_L (cheap) with probability ρ, c_H (expensive) otherwise, independent of θ"; ρ = "entry floor" | F55, F30, F22 |
| q; k; b | 6 | "investor's order q ∈ [-1, 1], trading cost k·abs(q)"; "noise traders: Laplace demand with scale b > 1" | F31, F13 |
| t_H, t_L; Δ_T | 7 | "target-payoff spread Δ_T = t_H − t_L; t_θ = expected target proceeds after a θ-challenger enters". T appears only as this subscript | F04, F36 |
| g_H, g_L; F, r̄ | 7 | "g_H(F) = 𝔼_F[(h − max{p, R})_+], challenger's gross acquisition profit (g_L likewise)"; "R ~ F on [0, r̄], ℓ < r̄ < h" (benchmark: F uniform, r̄ = r). 𝔼 is allowed here because 𝖤 is not on this frame | F28, F01, F19, F29 |
| μ; B_r(μ) | 8 | "public belief μ = Pr(H)"; "B_r(μ) = g_L + μ(g_H − g_L): expected gross profit at belief μ" | F01, F23 |
| m, M | 8 (words), 9 (formula) | "lowest and highest belief any price can induce"; m = 1/(1 + e^{2/b}) ≈ 0.27, M = 1 − m ≈ 0.73 (b = 2) | F40, F42 |
| τ | 9 | "belief threshold for costly preparation", with c_H annotated "expensive cost" beside the formula | F44, F30 |
| q_H, q_L; (1, −1) | 10 | "(q_H, q_L): order after a high / low challenger value"; "full orders (1, −1)" | F40, F05 |
| r0, r1, r2 | 11 (defined), 8 (figure markers labeled "r0 = 1.2", "r1 = 3", "r2 = 3.6") | "weak, strong, stronger-still incumbent" | F11 |
| 𝖤; 𝖮_H | 12 | "Entry 𝖤 = Pr(challenger prepares)"; "high-value challenger ownership 𝖮_H = Pr(high-value challenger acquires the target)". No 𝔼 on frames 12-16 | F29, F55, F56, F09 |
| r_C | 12b | "above r_C ≈ 3.59 even the most favorable price cannot cover expensive preparation" | F11, F41 |

Symbols kept off the main line and introduced only in backups: X, Z, P, μ_X(x) (A3; F02); x*, α_θ = Pr(X ≥ x* ∣ θ), e_H, e_L without bars (A4; F09, F18, F20, F21); U_θ(s) = sΠ_θ(s) − ks (A1; F17, F24); r_N, r_P, r_U (A6; F41, F52); a, d, T, Y and Pr(H ∣ P, Y = y) (A9; F13, F44, F53); η, t_η, g_{θ,η}, Δ_η (A11; F06, F28, F49); κ, μ̄ (A13; F03, F21); ε_C (A8); ε_V (A12); D_0 (A10; F10). Never shown anywhere: v, s_L, λ, a_H, a_L, a_±, Q, H_C, h_C, 𝔯(·), Δ_T^{-1}, 𝓔(p, r), R_max, B_p, "(A1)-(A3)", "OA.3".

Wording rules applied on every frame: the only role words are incumbent, challenger, investor, market makers, and noise traders (F13; never "buyer", never "trader"). "Entry" and "entry floor" replace participation, preparation probability, and investigation (F55). Say "no-trade equilibrium", never "pooling equilibrium" (F12). Say "target-payoff spread", never "information spread" (F36). Say "high-value challenger ownership" (F56). Conditions are named "low-cost floor", "high-cost window", "trading-cost window" (F35). Certified nodes are labeled by value r = 1.55, 1.60, 1.65 (F11), with q_L ≈ −0.460, −0.707, −0.903 (F05). Uniqueness footnote: "arbitrary mixed orders; every unilateral deviation q ∈ [-1, 1]" (F37). Accuracies are written as probabilities 0.70 and 0.75 (F53).

### 6.2 Deliberate differences from the paper's current text (paper-sync entries)

| # | Slide version | Paper location that differs | Audit ID |
|---|---|---|---|
| 1 | "quality θ ∈ {H, L}, worth h or ℓ; μ = Pr(H)"; formulas use h, ℓ, never θ as a number | main.md 51, 91, 131-132, 197, 363-364 and others listed in F01 | F01 |
| 2 | Lowercase g_H(F), g_L(F), written with h and ℓ; bargaining g_{θ,η} | main.md 131-132 (G_θ(F)), 364 (G_{θ,η}); eq. (6) | F28 (overrides F01's capital G) |
| 3 | "target-payoff spread Δ_T = t_H − t_L" in text, Table 1 row, and the rebuilt Figure 1 and Figure 4 axis labels | Table 1 row "Information spread"; main.md 897; `numerics/render/tables.py:188`; `numerics/render/figures.py:246, 359` | F36 |
| 4 | Prop. 2 conditions named (low-cost floor, high-cost window, trading-cost window) | main.md 219-229 labels (A1)-(A3) | F35 |
| 5 | "every unilateral deviation q ∈ [-1, 1]" | main.md 21, 233, 334, 821 ("every continuous deviation") | F37 |
| 6 | "entry" and "entry floor" throughout | abstract (main.md 8) and 23 ("participation"); 235 ("participation floor", "investigation") | F55 |
| 7 | Role words only; "challenger" never "buyer" | main.md 19, 35, 269, 330, 357 and others | F13 |
| 8 | Table 2 Panel B headed "Information controls"; price-hidden rows called equilibria of the no-price-access game | main.md 265 note (calls them fixed-profile controls; "only Panel A rows are equilibrium outcomes"), 267 | F08 |
| 9 | Frozen-order entry labeled "numerical diagnostic; sign analytical" | main.md 267 prints the numbers without status | F50 |
| 10 | Welfare stated at r1, plus "at r0 no gain" | main.md 23 ("At fixed incumbent strength") | F15 |
| 11 | Matched dividend tagged "diagnostic" | main.md 353 ("analytical invariance diagnostic") | F10 |
| 12 | Open set attached to parts (i)-(ii); the fall (iii) presented at the benchmark and nearby | main.md 233, 548, 550 | F46 |
| 13 | Robustness claimed for r0 → r1 only | main.md 733 (Prop. A.5 extends all of Prop. 2) | F47 |
| 14 | Coexistence stated at three strengths; elsewhere the search is not exhaustive | main.md 23 | F48 |
| 15 | Certified equilibria written (1, q_L) with q_L ≈ −0.460, −0.707, −0.903 at r = 1.55, 1.60, 1.65 and negated registry intervals; no v_j, r_j | main.md 275-287, 645-656, 697; registry and manifest definitions | F05, F11 |
| 16 | Rebuilt Figure 2 labels asymmetric orders "(1, q_L)" and symmetric interior orders "q_H = −q_L < 1"; no v or u | `numerics/render/figures.py` Figure 2 annotations "(1, −v)", "(u, −u)", "v, asymmetric" | new (extends F05; not in the audit's location list) |
| 17 | No-trade uniqueness bound written r_P ≈ 1.22; thresholds annotated by meaning | main.md 296, 572, 579, 595 (𝔯(k)); Fig. 2 caption omits it | F41, F52 |
| 18 | Complementary-signal example plus the 25-cell grid footnote | main.md 8, 23, after 336 | F16 |
| 19 | Accuracies as probabilities (a = 0.70, d = 0.75) | main.md 336 ("75%", "70%"); manifest display | F53 |
| 20 | Bargaining effects stated "weakly" | main.md 370, 897 | F49 |
| 21 | Bargaining transfer t_η, in words | main.md 363 (T_η), 899-906 (P) | F04, F06 |
| 22 | Global bound written U_θ(s) = sΠ_θ(s) − ks | main.md 487-535, 633-679 (F_θ(s)) | F17 |
| 23 | Crossing probability α_θ = Pr(X ≥ x* ∣ θ); e_H, e_L without bars | main.md 239-253, 548, 796-806; OA | F09, F18, F20, F21 |
| 24 | Price-pool cutoff κ; pooled posterior in words; cited as "Prop. A.10" | main.md 991-1047, 1148; OA 759 (OA.3) | F03, F21, F32 |
| 25 | Binary-value alternative reserve p = 1.01 stated on the reserve backup | main.md 383, 1146 | F39 |
| 26 | Logistic threshold "x* ≈ 5.42, about 1.5 noise s.d." | manifest display of `logistic_flow_threshold` | F38 |
| 27 | "high-value challenger ownership" | OA 216, 1527; manifest rows `base_ownership_*` | F56 |
| 28 | "m = 1/(1 + e^{2/b}) ≈ 0.27" | main.md 1027 | F42 |
| 29 | The general-support statement uses r̄ everywhere (bargaining too), never R_max | main.md 359, 897 | F19 |
| 30 | Serif math font so 𝖤 stays distinct; 𝖤 always labeled in words | style only (no paper text change) | F29 |

## 7. Exhibit inventory

| Id | Source | Treatment | Target file | Necessity | PowerPoint treatment |
|---|---|---|---|---|---|
| X1 | Figure 1 `figures/two_returns.pdf`; data `figures_data/two_returns.csv` (r 1.005-3.8, μ ∈ {m, 1/2, M}) | **rebuild from CSV**. Panel (a) Δ_T(r) in `cInfo`; panel (b) B_r(μ) at μ = m, 1/2, M in black and grays with direct labels; dashed `cCost` line at c_H = 6 (`base_c_high`); vertical gray markers labeled r0 = 1.2, r1 = 3, r2 = 3.6; x range 1.0-3.8; slide-size fonts; (a)/(b) labels; no title | `talk/figures/two_returns_talk.pdf` (+ `.svg`, 300-dpi `.png`) | Load-bearing for the two opposed returns (frame 8). The source axis reads "information spread", which conflicts with F36 ("overlay or re-render"). The markers and the c_H line tie the figure to frames 9-12. The source data exist, so no values are read off pixels | picture (SVG) |
| X2 | Figure 2 `figures/equilibrium_correspondence.pdf`; data `numerics/correspondence.csv`, `mixed_supports.csv`, `thresholds.csv`, `certificates.csv` | **rebuild from CSV**, adapting the plotting code in `numerics/render/figures.py` without solving or dropping branches. Relabel "(1, −v)" to "(1, q_L)", "(u, −u)" to "symmetric interior (q_H = −q_L < 1)", and the panel (b) axis to "order size, abs(q_L)". Keep broken lines at unresolved nodes, certified points with interval bars, shading, and r_N, r_U, r_C; r_P mentioned in text | `talk/figures/equilibrium_correspondence_talk.pdf` (+ `.svg`, `.png`) | Backup A6 only. The source uses v and u, which F05 bars from slides. If the rebuild cannot be verified, fall back to the source PDF with white-box relabels drawn over "(1, −v)" and the v/u labels | picture |
| X3 | Figure 3 `figures/posterior_tail_entry.pdf` | **reuse** (copy; labels already match the audit rules) | `talk/figures/posterior_tail_entry.pdf` (+ `.png`) | Backup A8: explains why logistic entry (0.302) is below Laplace entry (0.523) | picture |
| X4 | Figure 4 `figures/bargaining_weight.pdf`; data `figures_data/bargaining.csv` (η 0-1 by 0.01; r = 1.2, 3) | **rebuild from CSV**. Axis "target-payoff spread Δ_η" (F36); profits g_{H,η}, g_{L,η} (F28, F01); η = 1/2 marked; log scale kept for panel (b) | `talk/figures/bargaining_weight_talk.pdf` (+ `.svg`, `.png`) | Backup A11. The source labels read "information spread" and capital G_{θ,η} | picture |
| D1 | New simple diagram: timeline of five boxes (seller commits → investor trades → market makers price → challenger sees price, draws cost, decides → prepared bidders bid) | **new simple diagram**, native TikZ nodes with explicit `text width`, 4 arrows, no plotted coordinates | inline in `talk-A.tex` (no file) | Frame 6. The load-bearing assumption is an order of moves (price before commitment). A timeline shows it in one glance where a sentence needs a second reading. No source figure exists | 5 rounded rectangles + 4 arrows |
| D2 | Causal chain (frames 2 and 10) | native text with `\to` inside one centered line; not a diagram | inline | A genuine causal chain, where the direction is the content | one text box |
| T1 | Payment comparison, main.md 137 | **native table** (2 rows × 4 columns) | inline | Frame 7: the whole mechanism in one comparison | native table |
| T2 | Table 2 Panel A (`tables/table2_equilibrium_controls.tex`, `equilibrium_controls.csv`) | **native table**, excerpt: rows r0, r1 (12a) + r2 (12b); columns orders, price, 𝖤, 𝖮_H | inline | Frame 12: headline outcomes | native table (two slides) |
| T3 | Table 2 Panel B | **native table**, excerpt with F08 labels: feedback equilibrium, frozen orders, price hidden × r0, r1, status | inline | Frame 13 | native table |
| T4 | Proposition 3, eq. 13; registry `cert_*` | **native table**: r, q_H, q_L ≈, 𝖤 ≈ | inline | Frame 14 | native table |
| T5 | Table 3 (`tables/table3_extensions.tex`, `extensions.csv`) | **native table**, 5 rows × 4 columns (drop Evidence/Unique columns and O_H; status in subtitle) | inline | Frame 15 | native table |
| T6 | Table 2 Panel C | **native table**, 2 rows × 3 columns | inline | Frame 16 | native table |
| T7 | Table 4 Panel B (`reserve_comparisons.csv`) | **native table**, 4 rows × 6 columns | inline | Backup A12 | native table |
| T8 | Table 2 Panels A-B in full | **native table**, rebuilt (not `\input`) with 𝖤, 𝖮_H, and target proceeds | inline | Backup A5 | native table |

The paper's own tables are never pasted or `\input`. Every rebuilt figure gets individual QA: open the asset, then open each slide page that shows it.

## 8. Main deck, frame by frame

Notation for content: **bold** = bold lead phrase; `[nav: X]` = a `\PlaceNav` button; the gray line = `\graycite` or `\scriptsize` gray. Numbers carry their registry name in parentheses (the LaTeX comment in the deck).

**Frame 0. Title** (`[plain]`, uncounted)
- Title: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders" on two balanced lines. Author: Austin Li. No affiliation, venue or date.
- Minutes 0.25. Status: n/a.

**Frame 1. A sale is in play while the target's stock trades**
- Subtitle: The decision interval this paper is about
- Content:
  - **Target:** listed; a sale is publicly in play (disclosed approach, strategic review, open contest); the stock keeps trading
  - **Incumbent bidder:** already prepared; the market knows how strong it is, not what it will bid
  - **Challenger:** a second prospective bidder; to make an executable bid it must first pay for diligence, financing and approvals
  - **While the challenger decides,** it can watch the target's stock price
  - Closing line: `\KeyIdea{Key question:}` When the incumbent is stronger, does the challenger stay out, or can it be drawn in?
- Takeaway: the Key-question line.
- Claim status: descriptive setting (C25). Minutes 2.0. Nav: [Which deals fit] → A14 (`main:interval`). Notation: none.

**Frame 2. The received answer: a stronger rival deters entry**
- Subtitle: Preemption and entry costs at fixed information
- Content:
  - Centered chain (D2): stronger incumbent → costlier to win → lower return to preparation → less entry
  - Preparation is sunk before bidding; an unprepared challenger cannot bid `\graycite{Fishman 1988; Hirshleifer and Png 1989}`
  - The logic holds whenever the challenger's information is fixed `\graycite{Levin and Smith 1994}`
  - I keep this force intact
- Takeaway (`\Takeaway`): The twist: the price the challenger watches is itself an equilibrium object, and competition changes what it reveals.
- Claim status: supported as the received logic (Prop. A.3 later confirms it at fixed information). Minutes 1.25. Nav: none. Notation: none.

**Frame 3. This paper** (punchline; lands at about 3.5-4.25 min)
- Subtitle: none
- Content:
  - Framing line: A takeover auction in which an informed investor trades the target's stock before a second bidder decides whether to pay to prepare a bid. Prices are rational.
  - **Competition creates competition** (analytical). A stronger incumbent can turn an uninformative stock price into an informative one and raise entry.
    - Benchmark: entry 0.250 → 0.523 (`base_entry_weak`, `base_entry_strong`); high-value challenger ownership 0.125 → 0.324 (`base_ownership_weak`, `base_ownership_strong`), although the challenger's expected profit at the prior falls 4.80 → 4.29 (`base_profit_prior_weak`, `base_profit_prior_strong`)
  - **Information is the channel.** Hold the investor's orders fixed and entry falls, 0.562 → 0.523 (numerical diagnostic) (`base_frozen_entry_weak`, `base_frozen_entry_strong`); hide the price and entry stays at 0.250 (`base_hidden_entry_weak`, `base_hidden_entry_strong`)
  - **Implication:** what the auction makes the winner pay also sets what the stock price can reveal before anyone prepares.
- Takeaway: the Implication line.
- Claim status: supported (C5, C6, C9 numbers as numerical diagnostic, C10). Status tags on this frame: "(analytical)" after the first lead and "(numerical diagnostic)" after the frozen numbers (F50), both gray. Minutes 2.5. Nav: none. Notation: none; entry is in words.

**Frame 4. What is new relative to learning from prices**
- Subtitle: Four closest antecedents
- Content:
  - **Prices guide real decisions** `\graycite{Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang 2015}`: here the sale rule splits one surplus into a traded claim and the challenger's claim, which competition moves in opposite directions
  - **Stronger rivals deter** `\graycite{Fishman 1988; Hirshleifer and Png 1989}`: kept; I add a market that trades before preparation
  - **Auction entry is endogenous** `\graycite{Levin and Smith 1994; Roberts and Sweeting 2013; Gentry and Stroup 2019}`: here entry responds to what the price reveals
- Takeaway: The increment is the opposition between the two returns to information and the entry reversal it produces.
- Claim status: positioning. Every citation is verified against `references.bib` at drafting; no priority claims ("first", "only"). Minutes 0.75. Nav: [Related work] → A17 (`main:lit`), [References] → A18 (`main:refs`). Notation: none.

**Frame 5. Model: two bidders and a cash auction**
- Subtitle: Primitives in words; one restriction
- Content:
  - **Incumbent:** already prepared; value R ~ U[0, r], known only to itself; r = incumbent strength (public)
  - **Challenger:** quality θ ∈ {H, L}, worth h or ℓ, equally likely; it does not know θ
  - **Entry** = the challenger pays preparation cost C (learns θ, can bid); otherwise it stays out
  - **Seller:** commits before any trading to a cash second-price auction with reserve price p; bids are truthful
  - Restriction (display 1): 0 < p < ℓ < r < h
  - Gray legend: p = reserve price (not the stock price). A stronger incumbent is a first-order shift in the distribution of R, not an announced bid
- Takeaway: none (setup frame).
- Claim status: model primitives (input). Minutes 2.0. Nav: [What is left out] → A16 (`main:omit`). Notation: R, r, θ, H/L, h, ℓ, C, p.

**Frame 6. The challenger sees the price before it commits**
- Subtitle: Timing, information, and the one load-bearing assumption
- Content:
  - D1 timeline, five boxes: ① Seller commits to the auction → ② Investor learns θ and trades q → ③ Market makers see order flow and set the price → ④ Challenger sees the price, draws its cost, decides to enter → ⑤ Prepared bidders bid
  - **Investor:** knows θ; trades q ∈ [-1, 1] at cost k·abs(q); cannot bid, no control rights. **Noise traders:** Laplace demand, scale b > 1
  - **Cost:** C = c_L (cheap) with probability ρ, c_H (expensive) otherwise; independent of θ (`cCost`)
  - **Low-cost floor (load-bearing):** a cheap challenger always enters, so entry ≥ ρ and target proceeds always depend on θ
  - **Equilibrium:** investor may mix; price = expected target payoff given flow, anticipating entry; Bayesian beliefs from the price; optimal entry; truthful bids
  - Gray line: Benchmark (input): h = 10, ℓ = 1, p = 0.5, ρ = 0.25, c_L = 1, c_H = 6, b = 2, k = 0.02 (`base_h`, `base_ell`, `base_p`, `base_rho`, `base_c_low`, `base_c_high`, `base_b`, `base_k`)
- Takeaway: none (the timeline is the message).
- Claim status: model (input). Minutes 2.0. Nav: [Why an entry floor] → A15 (`main:floor`). Notation: q, k, b, c_L, c_H, ρ.

**Frame 7. Target proceeds differ across challengers only if R > ℓ**
- Subtitle: Cash second-price auction with reserve p; realized incumbent value R
- Content:
  - T1 native table:

    | Incumbent value | High-value challenger | Low-value challenger | Gap in target proceeds |
    |---|---|---|---|
    | R ≤ ℓ | wins, pays max{p, R} | wins, pays max{p, R} | 0 |
    | R > ℓ | wins, pays R | loses; incumbent pays ℓ | R − ℓ |
  - **Proposition 1** (analytical). R ~ F on [0, r̄], ℓ < r̄ < h. A first-order strengthening of F moves (display 1, two aligned lines):
    - target-payoff spread `\textcolor{cInfo}{Δ_T(F) = t_H − t_L = 𝔼_F[(R − ℓ)_+]}` ↑
    - challenger profit g_H(F) = 𝔼_F[(h − max{p, R})_+] ↓ (g_L likewise)
  - Gray line: t_θ = expected target proceeds after a θ-challenger enters; benchmark F uniform, r̄ = r
- Takeaway (`\TakeawayWithNav`): One shift, opposite signs: winning gets costlier, and target shares become more sensitive to who the challenger is.
- Claim status: supported, analytical (C1, C2). Minutes 2.5. Nav: [Other payment rules] → A11 (`main:payrule`). Notation: t_H, t_L, Δ_T, g_H, g_L, F, r̄.

**Frame 8. Stronger incumbent: spread up, challenger profit down**
- Subtitle: Benchmark h = 10, ℓ = 1, p = 0.5, b = 2; auction-stage payoffs, before trading and entry
- Content:
  - One line above the figure: B_r(μ) = g_L + μ(g_H − g_L) is expected profit at belief μ = Pr(H); m and M are the lowest and highest belief any price can induce (next slide)
  - X1 figure (rebuilt), full width: (a) Δ_T(r); (b) B_r(μ) at μ = m, 1/2, M, dashed c_H = 6, markers r0, r1, r2
- Takeaway: From r0 = 1.2 to r1 = 3, the spread rises from 0.0167 to 0.667 (`base_spread_weak`, `base_spread_strong`) and profit at the prior falls from 4.80 to 4.29 (`base_profit_prior_weak`, `base_profit_prior_strong`). Deterrence at every fixed belief, and more for the stock to reveal.
- Claim status: supported, analytical (C1). Status stamp "analytical" in gray under the figure. Minutes 1.75. Nav: none. Notation: μ, B_r(μ), m and M (in words).

**Frame 9. The price reveals the market's belief, within [m, M]**
- Subtitle: What the challenger can learn, and what it needs to learn
- Content:
  - Noise traders cap what any order can reveal. Display 1: m ≤ belief ≤ M, with m = 1/(1 + e^{2/b}) ≈ 0.27 and M = 1 − m ≈ 0.73 at b = 2 (`base_m`, `base_M`)
  - The price rises strictly with the belief (entry floor ρ > 0), so the challenger reads the market's belief off the price; atoms and jumps are allowed
  - The expensive challenger enters when B_r(μ) ≥ c_H, that is when (display 2): μ ≥ τ = (c_H − g_L)/(g_H − g_L), with c_H underbraced "expensive cost" and τ labeled "belief threshold for costly preparation"
  - **High-cost window:** B_{r0}(1/2) = 4.80 < c_H = 6 < B_{r1}(M): no expensive entry at the prior against r0; good news can clear τ against r1 (`base_profit_prior_weak`, `base_c_high`)
- Takeaway: Price information changes entry only if some feasible price can carry the belief across τ.
- Claim status: supported, analytical (C3; the window is a stated condition). Minutes 2.25. Nav: [Price sufficiency] → A3 (`main:suff`), [When entry can vanish] → A13 (`main:pool`). Notation: m, M (formula), τ.

**Frame 10. Informed trading pays only against a strong incumbent**
- Subtitle: Market makers price anticipated entry; the investor keeps only a residual
- Content:
  - Display 1 (underbraced): residual advantage per unit = (entry probability) × `\textcolor{cInfo}{Δ_T}` × (market's remaining uncertainty), so ρ m Δ_T ≤ advantage ≤ Δ_T
  - **Weak r0:** advantage ≤ Δ_T(r0) = 0.0167 < k = 0.02, so every order loses: no trade (`base_spread_weak`, `base_k`; margin 0.00333, `base_margin_weak_trade`)
  - **Strong r1:** each extra unit of a correctly signed order earns at least (1 − 1/b) ρ m Δ_T(r1) = 0.0224 > k, so full orders (q_H, q_L) = (1, −1): order after high / low value (0.0224 = `base_k` + `base_margin_strong_trade`)
  - **Trading-cost window:** Δ_T(r0) < k < (1 − 1/b) ρ m Δ_T(r1)
  - Chain line (D2, `cInfo`): stronger incumbent → wider Δ_T → trading pays → informative price → good news crosses τ → expensive challenger enters
- Takeaway: the chain line (it is the synthesis of the two forces).
- Claim status: supported, analytical (C4). Minutes 2.25. Nav: [Global trading bound] → A1 (`main:bound`). Notation: q_H, q_L, (1, −1).

**Frame 11. Proposition 2: a stronger incumbent raises entry**
- Subtitle: Analytical; weak r0 vs strong r1, all other primitives equal
- Content: one ResultBox titled "Proposition 2 (analytical)":
  - **Conditions:** low-cost floor, high-cost window, trading-cost window (frames 6, 9, 10)
  - (i) **Weak r0:** unique outcome is no trade; the price is uninformative; entry = ρ
  - (ii) **Strong r1:** unique outcome is full orders (1, −1); the price is informative; entry > ρ; high-value challenger ownership is higher than at r0
  - (iii) **Stronger still, r2** with B_{r2}(M) < c_H: full orders, but entry returns to ρ
  - (i)-(ii) hold on a nonempty open set of primitives, for every h > ℓ
  - Below the box, gray footnote: Uniqueness of trading and on-path entry under truthful bidding: arbitrary mixed orders; every unilateral deviation q ∈ [-1, 1].
- Takeaway (`\TakeawayWithNav`): **Intuition:** the stronger incumbent lowers what entry earns but raises what the price can tell the challenger; inside the three windows the second effect wins.
- Claim status: supported (C5-C8, C29 wording). Minutes 3.0. Nav: [Margins and open set] → A2 (`main:slack`). Notation: r0, r1, r2.

**Frame 12a. At the benchmark, entry rises from 0.250 to 0.523**
- Subtitle: Unique equilibrium outcomes of Proposition 2 at the benchmark (analytical)
- Content:
  - Definitions line: Entry 𝖤 = Pr(challenger prepares); high-value challenger ownership 𝖮_H = Pr(high-value challenger acquires the target)
  - T2 native table:

    | Incumbent strength | Orders (q_H, q_L) | Price | Entry 𝖤 | Ownership 𝖮_H |
    |---|---|---|---|---|
    | weak, r0 = 1.2 | (0, 0) | uninformative | 0.250 (`base_entry_weak`) | 0.125 (`base_ownership_weak`) |
    | **strong, r1 = 3** | **(1, −1)** | **informative** | **0.523** (`base_entry_strong`) | **0.324** (`base_ownership_strong`) |
- Takeaway: Profit at the prior fell (4.80 → 4.29), yet entry rose by 27.3 percentage points (`base_entry_change_pp`): the extra entry follows favorable prices, which are more likely when the challenger is high value.
- Claim status: supported, analytical (C6, C28). Minutes 1.25. Nav: none (build step). Notation: 𝖤, 𝖮_H.

**Frame 12b. At the benchmark, entry rises from 0.250 to 0.523** (duplicate of 12a with one added row)
- Content: T2 plus the row: very strong, r2 = 3.6 | (1, −1) | informative | 0.250 (`base_entry_collapse`) | 0.125 (Table 2 Panel A; `equilibrium_controls.csv`)
- Takeaway (`\TakeawayWithNav`): Rise, then fall: above r_C ≈ 3.59 (`base_r_high_cost_ceiling`) even the most favorable price cannot cover expensive preparation, so entry returns to ρ while trading stays informative.
- Claim status: supported at the benchmark (C8; no claim for every h > ℓ). Minutes 0.75. Nav: [How entry is computed] → A4 (`main:entryformula`). Notation: r_C.

**Frame 13. Freeze the information and deterrence returns**
- Subtitle: Entry 𝖤 at r0 = 1.2 and r1 = 3; controls that fix or remove the price experiment
- Content: T3 native table:

  | | r0 = 1.2 | r1 = 3 | Status |
  |---|---|---|---|
  | Equilibrium of the feedback game | 0.250 | 0.523 | analytical |
  | *Information controls* | | | |
  | Frozen informative orders (control, not an equilibrium at r0) | 0.562 (`base_frozen_entry_weak`) | 0.523 (`base_frozen_entry_strong`) | numerical diagnostic; sign analytical (Prop. A.3) |
  | Price hidden from challenger (equilibrium of the no-price-access game) | 0.250 (`base_hidden_entry_weak`) | 0.250 (`base_hidden_entry_strong`) | analytical |
- Takeaway (`\TakeawayWithNav`): Hold the price experiment fixed and a stronger incumbent lowers entry; the reversal comes from what the price reveals.
- Claim status: supported (C9, C10, C11). Minutes 2.0. Nav: [Controls in detail] → A5 (`main:controls`). Notation: none new.

**Frame 14. In between, informative and no-trade equilibria coexist**
- Subtitle: Computer-assisted (Proposition 3): interval arithmetic on exact decimal inputs
- Content:
  - T4 native table:

    | Strength r | q_H | q_L (certified) | Entry 𝖤 (certified) |
    |---|---|---|---|
    | 1.55 (`cert_a_r`) | 1 | ≈ −0.460 (`cert_a_v_interval`, negated) | ≈ 0.545 (`cert_a_entry_interval`) |
    | 1.60 (`cert_b_r`) | 1 | ≈ −0.707 (`cert_b_v_interval`) | ≈ 0.549 (`cert_b_entry_interval`) |
    | 1.65 (`cert_c_r`) | 1 | ≈ −0.903 (`cert_c_v_interval`) | ≈ 0.551 (`cert_c_entry_interval`) |
  - Buy fully after good news, sell partially after bad news; entry intervals are strictly ordered upward
  - Each of these economies also has a no-trade equilibrium with entry ρ = 0.25
  - Elsewhere the numerical search is not exhaustive; the full correspondence is open
- Takeaway: none (the three bullets are the reading).
- Claim status: computer-assisted (C12); open (C13). Minutes 1.5. Nav: [Figure 2 and thresholds] → A6 (`main:corresp`), [Certificates] → A7 (`main:cert`). Notation: none new.

**Frame 15. The entry reversal survives four changes to primitives**
- Subtitle: Entry 𝖤 at the weak and strong incumbent; each row uses its own declared parameters (analytical)
- Content: T5 native table:

  | Specification | Weak | Strong | Change (pp) |
  |---|---|---|---|
  | Benchmark: Laplace noise, two cost levels | 0.250 | 0.523 | 27.3 (`base_entry_change_pp`) |
  | Logistic noise | 0.250 | 0.302 (`logistic_entry_strong`) | 5.15 (Table 3) |
  | Atomless costs, Laplace | 0.250 | 0.523 (`cost_mix_laplace_entry_strong`) | 27.3 (Table 3: 27.27) |
  | Small value gap, h = 2, ℓ = 1 | 0.250 (`moderate_entry_weak`) | 0.527 (`moderate_entry_strong`) | 27.7 (`moderate_entry_change_pp`) |
  | Complementary signals: investor accuracy a = 0.70, challenger accuracy d = 0.75 | 0.850 (`signal_entry_weak`) | 0.879 (`signal_entry_strong`) | 2.94 (`signal_entry_change_pp`) |
- Takeaway (`\TakeawayWithNav`): The sign survives in every row; the size depends on how much posterior mass the noise puts near the upper bound.
- Claim status: supported, analytical for r0 → r1 (C15); the grid limit (C16) is in A9. Minutes 1.25. Nav: [Noise tails] → A8 (`main:logistic`), [Private signals] → A9 (`main:signals`). Notation: a, d in words beside the numbers.

**Frame 16. Price access raises proceeds and surplus at r1**
- Subtitle: Hold the incumbent at r1 = 3; compare with a challenger who cannot see the price (analytical, Prop. A.9)
- Content:
  - T6 native table:

    | | Price observed | Price hidden | Gain |
    |---|---|---|---|
    | Expected target proceeds | 0.872 (`base_revenue_feedback`) | 0.615 (`base_revenue_hidden`) | 0.258 (`base_revenue_gain`) |
    | Acquisition surplus net of preparation costs | 2.38 (Table 2 Panel C) | 2.30 (Table 2 Panel C) | 0.0802 (`base_net_surplus_gain`) |
  - Same full orders in both economies, so trading costs coincide
  - Each extra entry happens only when expected profit covers its cost
  - At r0 prices are uninformative, so there is no gain
- Takeaway: none (the table and three lines are the reading).
- Claim status: supported at r1 (C17; F15 wording, C18 avoided). Minutes 1.0. Nav: [Welfare accounting] → A10 (`main:welfare`), [Reserve] → A12 (`main:reserve`). Notation: none new.

**Frame 17. Conclusion** (last main frame; no navigation)
- Content:
  - `\KeyIdea{A stronger incumbent can bring the challenger in:}` at the benchmark, entry goes from 0.250 to 0.523 although profit at the prior falls
  - **Why:** competition makes target shares more sensitive to the challenger's value; informed trading makes the price informative; good news draws in the expensive challenger. Freeze that information and deterrence returns.
  - **Implication:** sale terms shape who competes through two channels: what the winner pays, and what the stock price reveals before anyone prepares.
- Claim status: supported (C5, C6, C9-C11). Minutes 1.0. Nav: none. Notation: none new.

## 9. Appendix frames

All backups come after `\AppendixStart` (frames numbered A1, A2, ...). Each carries `\hypertarget{app:...}` and `\BackButton{main:...}` pointing to its single origin.

| Label | Title | Content sketch | Linked from | Anticipated question |
|---|---|---|---|---|
| A1 `app:bound` | Why trading is unique: a global bound | Weak: gross advantage per unit ≤ Δ_T(r0) < k, so every nonzero order loses and the posterior stays at 1/2. Strong: U_θ(s) = sΠ_θ(s) − ks, with Π_θ(s) the expected residual per unit at order size s; U_θ'(s) ≥ (1 − 1/b) ρ m Δ_T(r1) − k > 0 for all s ∈ [0, 1]; wrong-signed orders lose. The bound holds against every candidate price and entry schedule, including mixed orders. Two comparisons: a unilateral deviation holds schedules fixed; the cross-strength comparison re-solves them. Status analytical (main.md 235-237, 487-535) | 10 | "Did you assume the informative profile? What about mixed strategies or large deviations?" |
| A2 `app:slack` | The conditions hold with slack, for every h > ℓ | Theorem margins at the benchmark: low-cost floor 1.37 (`base_margin_low_cost`); high-cost window 1.20 and 0.217 (`base_margin_high_prior`, `base_margin_high_ceiling`); trading-cost window 0.00333 and 0.00241 (`base_margin_weak_trade`, `base_margin_strong_trade`); minimum 0.00241 (`base_minimum_theorem_margin`). Nonemptiness: choose r0 < r1 close to ℓ, then k, c_H, c_L strictly inside their windows (main.md 767); a mathematical construction, not an effect-size claim. Moderate values h = 2: entry 0.250 → 0.527, minimum margin 8.01e-4 (`moderate_minimum_theorem_margin`). Part (iii) is not claimed for every h > ℓ (F46) | 11 | "Is this a knife edge? How big is the set? Does it need h = 10ℓ?" |
| A3 `app:suff` | The challenger can read the market's belief off the price | Display 1: μ_X(x) = Pr(H ∣ X = x) ∈ [m, M] for any mixed orders (bounded Laplace likelihood ratio e^{±2/b}). Display 2: price = t_0 + e(P)[t_L − t_0 + Δ_T μ], so μ is recovered from the price because e(P)Δ_T > 0. Atoms and entry jumps are allowed; no differentiability needed. Props. A.1-A.2, analytical (main.md 150-195) | 9 | "The challenger sees the price, not the flow; can it really invert it? What about price atoms?" |
| A4 `app:entryformula` | How entry is computed at the benchmark | Display 1: τ = (c_H − g_L)/(g_H − g_L), x* = (b/2) log(τ/(1 − τ)). Display 2: e_H = ρ + (1 − ρ)α_H, e_L = ρ + (1 − ρ)α_L, 𝖤 = (e_H + e_L)/2, 𝖮_H = e_H/2, with α_θ = Pr(X ≥ x* ∣ θ) in words. The high-cost window puts τ ∈ (1/2, M) and x* ∈ (0, 1); α_H > α_L tilts extra entry to high values. The strong experiment strictly Blackwell-dominates the weak one. Above r_C ≈ 3.59, τ > M; at r_C the left-limit entry is 0.506 (`base_laplace_entry_ceiling_left_limit`) | 12b | "Why does high-value ownership rise? Why exactly does entry fall at r2?" |
| A5 `app:controls` | Information controls in detail | Prop. A.3 in words: at any fixed information experiment and cost law, entry is weakly decreasing in r (analytical). Frozen orders are not an equilibrium at r0 (full orders are unprofitable there since Δ_T(r0) < k) and coincide with the equilibrium at r1. Price hidden: the challenger uses the prior and enters only at low cost; at r1 the investor still trades full orders. T8 native table: 𝖤, 𝖮_H, target proceeds for all Panel A-B rows (Table 2). F08 labels | 13 | "Is the frozen control a fair counterfactual? Why isn't it an equilibrium?" |
| A6 `app:corresp` | Trading and entry across incumbent strengths | X2 rebuilt Figure 2. Annotations by meaning (F41, F52): no trade unique for r < r_P ≈ 1.22 (`base_r_pool_unique_sufficient`); no trade an equilibrium up to r_N ≈ 1.75 (`base_r_no_trade_exact`); full orders unique above r_U ≈ 2.84 (`base_r_full_unique_sufficient`); expensive entry impossible above r_C ≈ 3.59 (`base_r_high_cost_ceiling`). Labels visible: black points computer-assisted; curves numerical diagnostic, broken at unresolved nodes; "multiplicity found; search not exhaustive"; full correspondence open | 14 | "What does the whole equilibrium correspondence look like? Which equilibrium is selected?" |
| A7 `app:cert` | What the computer-assisted proof certifies | Native table of registry enclosures shown exactly: q_L ∈ [−0.46031620, −0.46031618], [−0.70747539, −0.70747537], [−0.90333201, −0.90333198]; 𝖤 ∈ [0.5450528898, 0.5450528922], [0.5487563062, 0.5487563085], [0.5513607988, 0.5513608020]. The low type's marginal profit at its own order changes sign in the bracket (`cert_*_psi_left_lower`, `cert_*_psi_right_upper`); high-type cover margins 0.0000761777, 0.0027531948, 0.0054921767 (`cert_*_high_derivative_lower`). Does not prove uniqueness of the informative profile, exclude mixed equilibria, or certify a branch between nodes | 14 | "How do you know these are equilibria and not numerical artifacts?" |
| A8 `app:logistic` | Noise tails decide how often good news clears τ | X3 Figure 3 (reuse). Logistic threshold x* ≈ 5.42, about 1.5 noise s.d. from the center (`logistic_flow_threshold`, `logistic_threshold_noise_sd`); entry 0.302 vs 0.523 (`logistic_entry_strong`, `base_entry_strong`); atomless costs (ε_C = 0.1, `cost_halfwidth`): 0.523 and 0.301 (`cost_mix_laplace_entry_strong`, `cost_mix_logistic_entry_strong`). Fixed-profile comparison at a common scale b, not common variance; not a Blackwell ranking. Props. A.5-A.6 analytical | 15 | "Is Laplace noise doing the work? The posterior plateau looks special." |
| A9 `app:signals` | The price helps even a better-informed challenger | Investor signal T (accuracy a = 0.70), challenger signal Y (accuracy d = 0.75) (`signal_trader_accuracy_value`, `signal_buyer_accuracy_value`); entry 0.850 → 0.879 (`signal_entry_weak`, `signal_entry_strong`), analytical (Prop. A.7). The challenger combines Pr(H ∣ P, Y = y); entry is state dependent (e_H, e_L); the price still reveals the market posterior. Footnote (F16): "Grid of 25 (a, d): rises in 6 cells meeting Prop. A.7 (analytical); unchanged in 9 cells with d ≤ 0.75; falls about 4 pp when d ≥ 0.76, because the challenger's own good signal already triggers entry against the weak incumbent (numerical diagnostic)." Verify the counts against `tables/table_signal_grid.tex` at drafting | 15 | "Why would a bidder learn anything from the market about its own acquisition?" |
| A10 `app:welfare` | Why price access raises surplus, and a level diagnostic | Prop. A.9 at r1: each extra entry is chosen only when expected gross profit covers its cost; the allocation gain includes that profit and sales that would otherwise fail the reserve; transfers excluded. Invariance diagnostic (F10): "add a dividend D_0 = 0.257809 (the revenue gain from price access) to the traded claim in the price-hidden economy. Mean prices then match, but entry does not, so the information matters, not the price level." Tag "diagnostic". Not a sale mechanism; excluded from surplus. The ranking does not compare strengths or mechanisms | 16 | "Is more entry efficient? Isn't this just a higher price level?" |
| A11 `app:payrule` | The payment rule decides the sign of the spread effect | X4 rebuilt Figure 4. Zero-reserve verifiable-value institution with Nash weight η. In words: "seller gets t_η = (1 − η)·runner-up value + η·winner value". Display: g_{H,η} = (1 − η)𝔼[(h − R)_+]; Δ_η = η(h − ℓ) + (1 − 2η)𝔼[(R − ℓ)_+], R ~ F on [0, r̄], ℓ < r̄ < h. A stronger incumbent weakly lowers challenger profit for every η; Δ_η rises (weakly) if η < 1/2 and falls (weakly) if η > 1/2 (Prop. A.8, analytical). An entry reversal under bargaining is not solved (open) | 7 | "Is this special to second-price auctions? What about negotiations or first-price bids?" |
| A12 `app:reserve` | A higher reserve can raise proceeds; optimal terms are open | T7 native table, Table 4 Panel B, labeled "Value classes: p = 0.5 vs p = 1.1" (F39; ε_V = 0.05, `value_band_halfwidth`): weak proceeds 0.393 → 0.432; strong 0.872 → 1.01; entry at p = 1.1 is 0.540 (weak) and 0.512 (strong); sale and two-admissible-bidder columns from `reserve_comparisons.csv`. Say that 1.1 sits just above ℓ = 1, so it excludes the low-value challenger. Binary panel reserve p = 1.01 in a gray line. Entry, sale and two admissible bidders come apart. Feasible improvement, not an optimal reserve; seller-optimal terms open | 16 | "What should the seller do? Is there an optimal reserve?" |
| A13 `app:pool` | When entry can vanish, prices can pool | Prop. A.10 (analytical existence): at reserve p = 7 (`pool_reserve`) and r0, the same full orders support price pools below a cutoff κ ∈ [−log 2, 0]; same orders, different prices, beliefs and entry: pooled belief 0.273 vs 0.303, entry 0.152 vs 0.125, proceeds 0.687 vs 0.610 (`pool_posterior_cutoff_low/high`, `pool_entry_cutoff_low/high`, `pool_revenue_cutoff_low/high`). Does not arise on the benchmark support. Lesson: a continuation must include the price rule | 9 | "Is the price rule unique given orders? What if the entry floor fails?" |
| A14 `app:interval` | Which deals have a decision interval | A disclosed approach, strategic review or open contest can create one; a wholly confidential process does not. Imprivata's proxy separates approach, outreach, and indications of interest conditional on diligence `\graycite{Imprivata 2016; Boone and Mulherin 2007; Gentry and Stroup 2019}`: evidence of a costly preparation stage, not that a price drew anyone in. Empirical counterpart: start of substantive diligence, not public offers; incumbent strength measured from pre-decision information; later returns can reflect anticipated arrival. Pilot is a design only; no sample | 1 | "Is this realistic? Can you test it?" |
| A15 `app:floor` | Why the model needs a low-cost floor | Low-cost floor c_L < B_{r1}(m) (margin 1.37): some entry at every price keeps target proceeds sensitive to θ. Without it: nobody prepares → proceeds do not depend on quality → nothing to trade on → no informative trading is consistent. Part of the mechanism, not a numerical regularizer (main.md 235). Atomless cost supports keep it (Prop. A.6) | 6 | "Why do you need ρ > 0? Isn't the floor doing all the work?" |
| A16 `app:omit` | What the model leaves out | Neither bidder trades; the investor cannot bid or tender. Excluded: toeholds and free riding `\graycite{Bulow, Huang and Klemperer 1999; Grossman and Hart 1980}`; endogenous investor research and manipulation `\graycite{Goldstein and Guembel 2008}`; announced bids (strength is a distribution); other auction formats solved in full. Each is a next step, not a result | 5 | "Wouldn't the incumbent manipulate the price or buy a toehold? Why doesn't it trade?" |
| A17 `app:lit` | Related work in more detail | Two lines each, verified against `references.bib`: Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang 2012, 2015; Fishman 1988; Hirshleifer and Png 1989; Levin and Smith 1994; Roberts and Sweeting 2013; Gentry and Stroup 2019; Persico 2000; Luo 2005; Betton et al. 2014; Lin, Ma, Yang and Zhu 2025; Cornelli and Li 2002. Each with "shows / here" | 4 | "How is this different from X?" |
| A18 `app:refs` | References | `\small` list of the works cited on main frames and in A14-A17, metadata taken from `references.bib` | 4 | Citation lookup |

## 10. Timing table

| Frame | Title (short) | Minutes | Start | End |
|---|---|---|---|---|
| 0 | Title | 0.25 | 0.00 | 0.25 |
| 1 | A sale is in play while the stock trades | 2.00 | 0.25 | 2.25 |
| 2 | Received answer: deterrence | 1.25 | 2.25 | 3.50 |
| 3 | This paper (**punchline**) | 2.50 | 3.50 | 6.00 |
| 4 | What is new | 0.75 | 6.00 | 6.75 |
| 5 | Model: two bidders, cash auction | 2.00 | 6.75 | 8.75 |
| 6 | Challenger sees the price first | 2.00 | 8.75 | 10.75 |
| 7 | Proceeds differ only if R > ℓ | 2.50 | 10.75 | 13.25 |
| 8 | Spread up, profit down | 1.75 | 13.25 | 15.00 |
| 9 | Price reveals belief within [m, M] | 2.25 | 15.00 | 17.25 |
| 10 | Trading pays only against strong incumbent | 2.25 | 17.25 | 19.50 |
| 11 | Proposition 2 | 3.00 | 19.50 | 22.50 |
| 12a | Benchmark rise | 1.25 | 22.50 | 23.75 |
| 12b | Benchmark fall | 0.75 | 23.75 | 24.50 |
| 13 | Freeze the information | 2.00 | 24.50 | 26.50 |
| 14 | Equilibria coexist in between | 1.50 | 26.50 | 28.00 |
| 15 | Robustness | 1.25 | 28.00 | 29.25 |
| 16 | Price access and welfare | 1.00 | 29.25 | 30.25 |
| 17 | Conclusion | 1.00 | 30.25 | 31.25 |
| | Question reserve | 8.75 | 31.25 | 40.00 |

- **Punchline:** frame 3 opens at 3.5 min; the benchmark numbers (0.250 → 0.523, profit 4.80 → 4.29) are spoken by about 4.25 min.
- **Checkpoints:** Proposition 2 on screen by 19.5-20.5 min; the controls table (frame 13) by 24.5-25.5 min. If frame 11 starts after 21.5 min, cut from the list below.
- **Frames to skip if behind, in this order:**
  1. Frame 4 (−0.75): say its takeaway line aloud on frame 3's Implication; the buttons are reachable from A17/A18 in Q&A through the appendix.
  2. Frame 16 (−1.0): skip; answer from A10 if asked.
  3. Frame 14 (−1.5): one spoken sentence on 12b ("between r0 and r1, informative and no-trade equilibria coexist at three certified strengths").
  4. Frame 15 (−1.25): compress to 20 s ("the sign survives logistic noise, atomless costs, a small value gap and a better-informed challenger").
  5. Frame 8 (−1.0): speak its numbers on frame 7 and move on.
  Together these recover up to 5.5 minutes. Never cut frames 3, 5-7, 9-13 or 17.
- **If ahead:** open A1 from frame 10 or A6 from frame 14, then return.

## 11. Anticipated questions (job-market audience)

| # | Question | Where answered |
|---|---|---|
| 1 | Is this realistic? Which deals have such an interval? | A14 (from frame 1); spoken: whether a given deal fits is a question about its chronology, and the paper settles it for no transaction |
| 2 | Isn't this just learning from prices, as in Dow-Goldstein-Guembel? | Frame 4 and A17: the increment is the opposition between the two claims on one surplus, and the entry reversal |
| 3 | Why can't the challenger bid without preparing, at its expected value? | Spoken, from frame 5: preparation is required for an executable bid (verification, financing, approvals); a challenger that declines stays out (main.md 35, 57) |
| 4 | Why do you need the low-cost floor? Is ρ doing all the work? | A15 |
| 5 | Did you assume the informative profile? What about mixed strategies or big deviations? | A1 |
| 6 | Is it a knife edge? Does it need h = 10ℓ? | A2 (every h > ℓ; moderate values h = 2) |
| 7 | Is Laplace noise special? The posterior plateau looks convenient | A8 (logistic noise: same sign, smaller size) |
| 8 | Why would a bidder learn about its own acquisition from the market? | A9 (complementary information; d = 0.75 > a = 0.70 still works; grid footnote) |
| 9 | Which equilibrium is selected between r0 and r1? | A6, A7; spoken: the paper does not select; the correspondence is open |
| 10 | How do you know the certified points are equilibria? | A7 |
| 11 | Why does high-value ownership rise, not just entry? | A4 (α_H > α_L) |
| 12 | Why does entry fall again at r2? Is the effect monotone? | Frame 12b; A4 (r_C, τ > M) |
| 13 | Is the frozen-order control a legitimate counterfactual? | A5; spoken: it is a control that holds the experiment fixed, labeled numerical diagnostic, and its sign is a theorem (Prop. A.3) |
| 14 | Isn't it the price level, not information? | A10 (matched-dividend diagnostic) |
| 15 | Is more entry good? Welfare? | Frame 16; A10 (at r1 only; does not rank strengths or mechanisms) |
| 16 | Does this depend on the second-price rule? First-price or negotiation? | A11 (sign of the spread effect flips at η = 1/2; entry under bargaining open); spoken: first-price not solved |
| 17 | What should the seller do? Optimal reserve? | A12 (feasible improvement; optimal terms open); A13 if the pooling issue comes up |
| 18 | Wouldn't the incumbent or the investor manipulate the price, or buy a toehold? | A16 |
| 19 | Why doesn't the incumbent trade on its own value? | A16; spoken: neither bidder trades in the benchmark; the investor knows θ, not R |
| 20 | Why a linear trading cost k? What if k is near zero? | Spoken, from frame 10: k is an execution or carrying friction separate from price impact; the result needs k inside the trading-cost window, and outside it Proposition 2 says nothing; A2 gives the margins |
| 21 | Are the magnitudes calibrated to real deals? | Spoken: no; a declared benchmark shows that the conditions are jointly satisfiable and scales the effect; signs are the theorem |
| 22 | Can you test it? | A14 (design only, no sample; returns before entry can reflect anticipated arrival) |
| 23 | Is the strong-economy price really more informative? | A4 (strict Blackwell dominance at the same noise law) |
| 24 | What if the challenger could see order flow, not the price? | Spoken, from A3: the price is a sufficient statistic for the market's belief, so here the price and the flow carry the same belief information (Props. A.1-A.2) |
