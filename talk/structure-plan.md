# Structure plan: 40-minute session

Paper: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders" (Austin Li).
Stance: author presentation. Genre: conference or job-market talk for a generalist finance-economics room.
Sources: `talk/notes/paper-digest.md`, `talk/notes/audit-adoptions.md` (binding for notation and wording), `audit/talk_consistency/report.md`, `paper/main_filled.md` (line numbers are main.md = main_filled.md lines), `numerics/quantity_registry.csv` (registry names in parentheses), `references.bib`. Built from `talk/notes/plan-A.md` (base) and `talk/notes/plan-B.md` (grafts), then revised in place after an external critique (section 12 logs every point).

---

## 0. Judge's scores and grafts

Scores (1-10) on the seven criteria:

| Criterion | Plan A (concrete-first) | Plan B (mechanism-first) |
|---|---|---|
| (a) Punchline timing and clarity | 7.5. Numbers land at about 4.25 min. But "This paper" gives the result and the control without the "why". The opening also spends 3.25 min on two frames (setting, then the received answer) that one frame can carry | 8.5. The answer comes at about 3.5 min with a visual intuition, and "This paper" carries the "one auction, two claims" support. The cost: a two-panel figure with R, r, h, ℓ, p appears at minute 1.5, before the model |
| (b) Prerequisites (rule 17) | 9. The model and timing come before the mechanism. Each condition is introduced where it is used (floor, high-cost window, trading-cost window) and collected at the theorem | 7.5. Everything is in place before Prop. 2. But frames 4-6 use the investor, the rational price and the entry probability before the model frame defines them. Model at 11.25-13 min |
| (c) Faithfulness | 9. Status tags on the punchline (F50). Strict number rule (registry or printed tables only). F08, F15, F46 and F47 are applied. Gaps: the F16 grid footnote is only in a backup; the Prop. 2 frame names the conditions without their content; the 0.0224 arithmetic sits only in a comment | 7. The frozen numbers on the punchline have no on-screen status (F50). Values found only in the CSV appear on the main line (r2 profit 4.13 and spread 0.939) and in backups (deviation gain 1.619e-2; the 3.6 column of Table 1). Q19 quotes a CSV-only 0.376680 and overstates it ("benchmark-specific"). p sits next to P(X) on the timeline (F31) |
| (d) Timing inside 30-32 min | 8. 31.25 min, realistic, with a concrete cut list. Frame 1 (2 min, text only) is slow | 7.5. 30.75 min with a good cut list. The model starts at 11.25 min, and the mechanism-before-model order invites clarification questions that cost time. Prop. 2 at 3.5 min is heavy |
| (e) Cognitive load, notation | 7.5. X, Z, P and V_T stay off the main line. But frame 6 packs a timeline plus five bullets (schematic rule: at most two reading bullets), frames 5-6 introduce 6-8 symbols each, and F and r̄ sit on the main line | 7. Keeps to at most 5 new symbols per frame. But the main line carries about 38 symbols, including X, Z, P, V_T, μ_X and v_θ, which the proposition does not need |
| (f) Exhibits, PowerPoint | 8. One rebuilt figure, dense (three beliefs, c_H, three markers), used before m and M are formally defined (F40 tension). Native tables and a simple timeline | 8.5. Two focused rebuilt figures (the two returns; profit against cost lines). A native synthesis table. Figure 2 split into panels, bargaining panel (a) only |
| (g) Appendix coverage | 7.5. 18 backups with good question mapping. No closed-form payoffs, notation table, full robustness table or proof-logic frame; Figure 2 is kept whole | 9. 22 backups, including closed forms, notation, proof logic, the full robustness table, a grid summary with verified counts, evidence design, and a reserve-to-pool chain |
| **Total** | **56.5** | **55.0** |

**Base: Plan A.** It has the cleaner dependency path, a stricter number discipline, better status labelling and a lighter main line.

**Grafts from Plan B:**
1. The "one auction, two claims" support line on "This paper", so the punchline carries the why.
2. One Key-question opener replaces A's two opening frames (saves 1.25 min).
3. A native synthesis table (deterrence vs information, same four-row skeleton). After the critique it is backup A18, reached from the theorem frame; the theorem's takeaway carries its chain line.
4. Two focused rebuilt figures in place of A's single dense one: X1 is B's opener design (Δ_T and profit at the prior only), shown after the payment comparison; X2 is B's profit-thresholds figure with c_L and c_H lines. After the critique, m and M are defined on the trading frame, which now precedes X2.
5. Prop. 2 frame: each condition's inequality by name, plus the scope footnote. After the critique the one-line glosses are dropped (they repeat frames 7-8).
6. The benchmark table orientation, with profit and spread rows ("the price, not the prize"), inside A's two-step build.
7. The F16 grid footnote on the main robustness frame.
8. Appendix additions: closed-form payoffs, notation, proof logic, full Table 3, signal-grid summary, evidence design, Figure 2 as two panel frames, bargaining panel (a) only, reserve → price-pool chain.
9. B's speaker hooks.
10. B's "at most 5 new symbols per frame" discipline (one accepted exception, frame 4, met by grouping).

**Corrections applied to both plans:**
- Values found only in the CSV stay off the slides (r2 profit and spread become "lower still" and "wider still", which Prop. 1 supports).
- B's Q19 is answered without a CSV-only number.
- The 0.0224 bound is shown on the slide with its arithmetic.
- Titles are kept to 52 characters or fewer.
- No X, Z, P, V_T or τ on the main line.

---

## 1. Settings and budget

| Item | Setting |
|---|---|
| Total session | 40 minutes, including questions and interruptions (fixed) |
| Planned speech | 30.25 minutes (75.6%): title 0.25 + 16 content frames 30.0 |
| Question reserve | 9.75 minutes (24.4%) |
| Content frames | 16. Frame 10 is a two-step build (10a, 10b) made by duplicating the frame and counts once, so there are 17 physical main frames after the title |
| Appendix | 29 backup frames after `\AppendixStart`. Each is reached from exactly one origin (a main frame, or for A6, A25 and A28 the backup before it) via `\PlaceNav` and returns there via `\BackButton`. Every backup that answers a likely question hangs off a frame that is never cut (section 10) |
| Punchline | Frame 2 opens at 2.25 min. The headline numbers are on screen and spoken by about 2.75 min, and the punchline frame is complete by 4.25 min |
| Class and theme | `\documentclass[11pt,aspectratio=169]{beamer}`, `\usetheme{Madrid}`, `\usepackage{econ-slides-compat}`, `\usefonttheme[onlymath]{serif}` (F29), XeLaTeX |
| Title page | `[plain]`, uncounted. Paper title on two balanced lines; `\author{Austin Li}`; `\institute{}`; `\date{}`. Footline short title "Competition Creates Competition". No affiliation, venue or date |
| Overlays | None: no `\pause`, `\only`, `\onslide` or `\uncover`. The single build (10a → 10b) is a duplicated frame. Backup figure panels (A24 → A25) are separate frames |
| Density caps | ≤ 7 items, ≤ 2 display equations and ≤ 2 colored boxes per frame. The deck has one `ResultBox`, on frame 9. At most 5 new symbols per frame; frame 4 introduces four grouped objects (R and r; θ with h and ℓ; p; the cost law C, c_L, c_H, ρ), the deck's one symbol-dense frame, carried by the timeline boxes and a two-item legend. Text-only main frames: 2, 3, 15, 16 (4 of 16, 25% ≤ 30%). Frame 1 opens with a three-box timeline, so the first picture is on screen at 0.25 min |
| Ending | Frame 16 (Conclusion) is the last main frame and has no navigation. No "Thank you / Questions" frame. References live in the appendix (A29), so the generic "references slide, then thank-you slide, then backups" order is overridden |
| Literature | No review section. Frame 3 is a one-frame positioning against four antecedents |
| Titles | One rendered line, at most 52 characters. Verify in the render: Madrid's frame title at 11 pt, 16:9 holds about 55 characters |
| PowerPoint | Every frame can be rebuilt 1:1 in native PowerPoint: text, native tables (including the one-row, three-cell table on frame 7), equations, pictures of figures (paper PDF or a CSV rebuild exported as SVG and 300-dpi PNG), two simple timelines (three boxes on frame 1, five boxes on frame 4) and one text chain (frame 9). Cost lines in X2 are drawn inside the picture, never overlaid as separate shapes. Any white-box relabels on the X5 fallback are also native shapes. The ResultBox becomes a rounded rectangle with a title bar. No TikZ plots, no underbraced text displays |
| Files | Deck `talk/talk.tex`. Shared number and phrase macros in `talk/results.tex`, each with a registry-name comment. Figures in `talk/figures/`, written by one script `talk/figures/build_talk_figures.py` that reads CSV only and never solves, changes a parameter or drops a branch |
| Number rule | Every number on a slide is either a registry value (`numerics/quantity_registry.csv`) or a value printed in `paper/main_filled.md` or its inserted tables. Slides show 3 significant digits rounded from the registry display. Main-line tables show entry levels, not percentage-point changes; the one pp figure on the main line is 27.28 (`base_entry_change_pp`, frame 10a), and backups show pp changes as printed (27.28, 27.27, 5.15, 27.68, 2.94). Certificate enclosures are shown exactly as the registry displays them and never re-rounded. m is shown once on the main line, as ≈ 0.27 (F42); the one derived main-line number, the bound 0.0224 on frame 7, is written with m symbolic and checked as k + theorem margin 0.00241 (`base_k`, `base_margin_strong_trade`), so no second rounding of m appears. r_C ≈ 3.59 stays off the main line (words: "a ceiling strength") and appears in A20 and A24. Values that exist only in validated CSV output stay off the slides unless a registry key is added first: τ = 0.705, x* = 0.871, B_{r0}(M), B_{r1}(M) = 6.217, B_{r2}(M) = 5.997, the r = 3.6 row of Table 1, the frozen deviation gain 1.619e-2, and the atomless-cost entry at 3.6. Curves in rebuilt figures are plotted from `figures_data/*.csv` (the paper's own figure data); no number is read off a plot |

## 2. Author story

**Research question.** A listed target is publicly in play. One bidder (the incumbent) is already prepared. A second bidder (the challenger) must pay to prepare before it can bid, and it can watch the target's stock price while it decides. Does a stronger incumbent keep that challenger out, or can it draw the challenger in? (main.md 13, 17, 31-39)

**Answer, with the headline number.** A stronger incumbent can draw the challenger in by making the stock price informative about the challenger. At the benchmark, moving the incumbent from r0 = 1.2 to r1 = 3 (`base_r_weak`, `base_r_strong`):
- The challenger's expected gross profit at the prior falls from 4.80 to 4.29 (`base_profit_prior_weak`, `base_profit_prior_strong`).
- Entry rises from 0.250 to 0.523, +27.28 percentage points (`base_entry_weak`, `base_entry_strong`, `base_entry_change_pp`).
- High-value challenger ownership rises from 0.125 to 0.324 (`base_ownership_weak`, `base_ownership_strong`). Shown on frame 10a, not on the punchline frame.

Proposition 2, analytical (main.md 216-257).

**Why it matters.** The received comparative static is that a stronger rival deters costly entry (Fishman 1988; Hirshleifer and Png 1989). It holds when the entrant's information is fixed. In a public sale, the stock trades while a further bidder decides, so the bidder pool depends on what the market reveals. The main line varies incumbent strength only, so the slide implication is tied to that: when the target trades, a stronger rival is not a pure deterrent, and who competes depends on what the price reveals before anyone prepares. The paper's broader reading, that sale terms act through both what a winner pays and what the price reveals (main.md 25, 404), is spoken on the conclusion as the open question it is: the seller's choice of terms is "the next theorem" (main.md 25, 408; C29, C36).

**Contribution: the four items (talk-structures.md).**
1. **Primary takeaway.** Competition creates competition. On a nonempty open set of primitives, strengthening the incumbent turns an uninformative price into an informative one. Entry rises, and so does the probability that a high-value challenger acquires the target, even though the challenger keeps less. Trading and on-path entry are unique in each economy (Prop. 2 (i)-(ii), analytical).
2. **Two supporting claims.**
   - (a) *One auction, two claims.* A stronger incumbent lowers the challenger's gross profit at every fixed belief and raises the target-payoff spread Δ_T (Prop. 1, analytical, any first-order strengthening). A wider spread makes informed trading pay, and the resulting price tells the challenger when expensive preparation is worthwhile.
   - (b) *Information is the channel.* At any fixed information experiment a stronger incumbent cannot raise entry (Prop. A.3, analytical, weak monotonicity). At the benchmark, freezing the investor's orders gives 0.562 → 0.523 (`base_frozen_entry_weak`, `base_frozen_entry_strong`; numerical diagnostic, sign analytical). The punchline states this in words only; the numbers appear on frame 11. Hiding the price gives 0.250 at both strengths (`base_hidden_entry_weak`, `base_hidden_entry_strong`; analytical), but that flat row is implied by the high-cost window (at the prior, expensive preparation never pays: 4.80 and 4.29 < 6). It shows that the rise needs the price, not that deterrence returns, and it is annotated so on frame 11.
3. **Strongest credibility argument.** Prices are rational: market makers price the entry each price induces, so the reversal is not mispricing, and in the model the investor cannot profit by faking good news, because every wrong-signed order has negative gross payoff against every candidate schedule (eq. 11; main.md 197-209, 535). Uniqueness comes from global bounds, not from a guessed profile. Against the weak incumbent the gross advantage per unit is capped by Δ_T(r0) < k. Against the strong incumbent every marginal unit of a correctly signed order earns more than k under every candidate schedule, with arbitrary mixed orders and every unilateral deviation q ∈ [-1, 1] allowed (main.md 21, 233-237; F37 wording).
4. **Boundary audit.** The effect is not monotone in strength. At r2 = 3.6, just above the ceiling strength at which the best price stops covering expensive preparation, trading stays fully informative but entry returns to 0.250 (`base_entry_collapse`). This is shown once, beside the evidence, on frame 10b (and as the r2 marker on X2); leaving it out would let "stronger incumbents attract entry" be heard as a monotone claim. The margin to the ceiling is not stressed (F46): the slide names no ceiling number, and the spoken line says any such strength works and 3.6 is the declared node. The three sufficient conditions appear once, by name and inequality, on the theorem frame. Secondary boundaries stay off the refrain:
   - the intermediate correspondence is open (frame 12, A24);
   - the seller's optimal terms are open (A27, spoken on frame 16);
   - there is no empirical estimate (frame 15, A2).

**Formal payoffs the paper earns (the argument's steps, not extra contributions):**
- a two-returns comparative static (Prop. 1);
- price sufficiency with bounded posteriors (Props. A.1-A.2);
- the reversal theorem (Prop. 2);
- a fixed-experiment deterrence result (Prop. A.3);
- computer-assisted coexistence (Prop. 3);
- robustness (Props. A.5-A.7, Sec. 5.2);
- welfare of price access at r1 (Prop. A.9);
- payment-rule dependence (Prop. A.8).

**Mechanism classification: competing forces, with a complementary chain inside one of them.**
- *Force 1, deterrence (inherited):* a stronger incumbent lowers g_H, g_L and so B_r(μ) at every fixed belief. At any fixed information experiment, entry weakly falls (Prop. A.3).
- *Force 2, information (new):* the same shift widens Δ_T. That raises the investor's residual advantage (entry probability × Δ_T × the market's residual uncertainty) and so its incentive to trade on challenger quality.
- *Chain inside force 2:* wider Δ_T → informed trading pays (trading-cost window) → informative price, with beliefs spanning [m, M] → good news clears the expensive cost (high-cost window) → the expensive challenger enters → entry and high-value ownership rise.
- *Dependency:*
  - Force 2 needs the low-cost floor, so that target proceeds depend on quality after every price, and it needs the price to be seen before entry.
  - The net sign is settled by the three named conditions.
  - Force 1 wins at any fixed experiment (frame 11), and it reasserts itself at very high strength (r2), where even the best price cannot justify c_H.
  - The bargaining backup shows that the opposition itself depends on the payment rule: the spread effect flips sign at η = 1/2.
- *Frame architecture (the chain runs in the order it is spoken):*
  - Frame 5 derives both forces from one payment comparison (the two lines of Prop. 1).
  - Frame 6 shows them at benchmark scale as the two panels of one exhibit (X1).
  - Frame 7 gives the first link of the information force: when trading pays, and hence why the price moves. m and M are defined here, where ρ m Δ_T is first used.
  - Frame 8 gives the second link: what a moving price tells the challenger (floor and high-cost window). It also shows the deterrence force at every belief, after the audience already knows the weak incumbent's price does not move.
  - Frame 9 states the theorem; its takeaway is the chain line. The side-by-side synthesis table is backup A18.

## 3. Claim-evidence ledger

Status column: ledger status, with the paper's result status in parentheses.

| # | Claim (slide wording) | Status | Paper location | Registry names |
|---|---|---|---|---|
| C1 | A stronger incumbent lowers challenger gross profit at every fixed belief and raises the target-payoff spread | supported (analytical, Prop. 1, any continuous F) | main.md 99-137, eqs. 4-6 | `base_spread_weak`, `base_spread_strong`, `base_profit_prior_weak`, `base_profit_prior_strong` |
| C2 | Target proceeds differ across challenger types only when R > ℓ, by R − ℓ | supported (analytical; property of the cash second-price rule) | main.md 17, 137 | none |
| C3 | The price reveals the market's belief, which noise keeps within [m, M]; atoms and entry jumps allowed | supported (analytical, Props. A.1-A.2) | main.md 150-195, eqs. 7-10 | `base_m`, `base_M` |
| C4 | Low-cost floor: a cheap challenger enters after any price. High-cost window: the expensive challenger stays out at the weak prior and enters after the best news against r1 | supported (stated conditions of Prop. 2, shown on X2 from figure data) | main.md 216-235 | `base_c_low`, `base_c_high`, `base_margin_low_cost`, `base_margin_high_prior`, `base_margin_high_ceiling` |
| C5 | Informed trading loses against the weak incumbent and must be at full size against the strong one | supported (analytical) | main.md 197-237, eq. 11 | `base_k`, `base_spread_weak`, `base_spread_strong`, `base_margin_weak_trade`, `base_margin_strong_trade`; 0.0224 = `base_k` + `base_margin_strong_trade` (= (1 − 1/b)ρ m Δ_T(r1) from `base_b`, `base_rho`, `base_m`, `base_spread_strong`) |
| C6 | Prices are rational; the reversal is not mispricing | supported | main.md 21, 79, 189-203 | none |
| C7 | Weak r0: unique no trade, uninformative price, entry ρ | supported (analytical, Prop. 2 (i)) | main.md 233 | `base_entry_weak`, `base_ownership_weak` |
| C8 | Strong r1: unique full orders, informative price, entry > ρ, high-value ownership up | supported (analytical, Prop. 2 (ii)) | main.md 233, 257 | `base_entry_strong`, `base_ownership_strong`, `base_entry_change_pp` |
| C9 | (i)-(ii) hold on a nonempty open set of primitives, for every h > ℓ | supported for (i)-(ii) only (F46). Nonemptiness for every h > ℓ comes from a construction with r0 < r1 near ℓ, not from slack at the benchmark (the benchmark minimum margin is 0.00241 on k = 0.02) | main.md 233, 404, 767 (A.25); Sec. 5.2 | `base_minimum_theorem_margin`, `moderate_minimum_theorem_margin` |
| C10 | Stronger still (r2), where the low-cost floor and profitable trading persist (c_L < B_{r2}(m), k < (1 − 1/b)ρ m Δ_T(r2)) but B_{r2}(M) < c_H: full orders, entry back to ρ | supported at the benchmark and nearby parameters, with all three conditions of part (iii) stated. The paper's open-set wording covering (iii) is **conflicted** (F46); the claim for every h > ℓ is **excluded** | main.md 233 (iii), 250-253, 550 | `base_entry_collapse`, `base_r_high_cost_ceiling` (backup only); high-value ownership 0.125 at r2 from Table 2 Panel A |
| C11 | At r2 profit at the prior is lower still and the spread wider still | supported (analytical; Δ_T' > 0, g_H' < 0, g_L' < 0, main.md 121). Shown in words, no numbers | main.md 99-121 | none |
| C12 | Extra entry tilts toward high-value challengers (α_H > α_L); the strong price experiment strictly Blackwell-dominates the weak one | supported (analytical) | main.md 233, 239-253, eq. 12 | none |
| C13 | Uniqueness allows arbitrary mixed orders and every unilateral deviation q ∈ [-1, 1] | supported. The paper's "every continuous deviation" is **conflicted** wording (F37); slides use the corrected phrase | main.md 21, 89, 233, 237 | none |
| C14 | Freezing orders restores deterrence: 0.562 → 0.523 | numbers: numerical diagnostic; sign: supported (analytical, Prop. A.3, weak monotonicity, so slides say "weakly lowers" or "cannot raise"). main.md 267 prints the numbers without a status (F50) | main.md 267, 554 | `base_frozen_entry_weak`, `base_frozen_entry_strong` |
| C15 | Hiding the price leaves entry at 0.250 at both strengths | supported (analytical; equilibria of the no-price-access game). The flat row is implied by the high-cost window (B_{r1}(1/2) < B_{r0}(1/2) < c_H), so it shows the rise needs the price, not that deterrence returns; frame 11 annotates it that way and frame 2 omits it. The paper's Table 2 note calls these "fixed-profile controls": **conflicted** (F08); slides use the F08 label | main.md 265, 269; Table 2 Panel B | `base_hidden_entry_weak`, `base_hidden_entry_strong` |
| C16 | The reversal runs through what the price reveals ("the price, not the prize") | supported as a comparison of model economies (C14, with C15 showing the price is necessary). Not a causal empirical claim | main.md 269 | as C14, C15 |
| C17 | At r = 1.55, 1.60, 1.65 an informative equilibrium coexists with no trade; entry intervals strictly ordered upward | supported (computer-assisted, Prop. 3). The introduction's general "coexist" is **conflicted** (F48); slides restrict it to three strengths | main.md 23, 273-287, eq. 13 | `cert_a_r`, `cert_b_r`, `cert_c_r`, `cert_a_v_interval`, `cert_b_v_interval`, `cert_c_v_interval` (shown negated as q_L), `cert_a_entry_interval`, `cert_b_entry_interval`, `cert_c_entry_interval` |
| C18 | The full intermediate correspondence; a continuous branch between nodes | **excluded** (open; F48) | main.md 296-304 | none |
| C19 | Numerical continuation branches in Figure 2 | descriptive only (numerical diagnostic; search not exhaustive). Backups A24-A25 | main.md 291-300 | none (`numerics/correspondence.csv` as figure data) |
| C20 | Thresholds: no trade unique below r_P ≈ 1.22 and an equilibrium up to r_N ≈ 1.75; full orders unique above r_U ≈ 2.84; expensive entry impossible above r_C ≈ 3.59 | supported (analytical, Prop. A.4). Backup only (A20, A24); the main line says "a ceiling strength" | main.md 296, 568-602 | `base_r_pool_unique_sufficient`, `base_r_no_trade_exact`, `base_r_full_unique_sufficient`, `base_r_high_cost_ceiling` |
| C21 | The r0 → r1 reversal survives logistic noise, atomless costs, a small value gap, and complementary signals | supported (analytical, Props. A.5-A.7, Sec. 5.2, Table 3) for r0 → r1 only (F47). Each row has its own declared parameters; rows are not compared with each other. "The r2 fall is robust" is **excluded** | main.md 306-341, 733; Table 3 note | `logistic_entry_strong`, `cost_mix_laplace_entry_strong`, `cost_mix_logistic_entry_strong`, `moderate_entry_weak`, `moderate_entry_strong`, `moderate_entry_change_pp`, `signal_entry_weak`, `signal_entry_strong`, `signal_entry_change_pp`, `signal_rho`, `signal_r_weak`, `signal_r_strong` |
| C22 | The reversal holds with a more accurate challenger signal | supported as the declared example (a = 0.70, d = 0.75; analytical). The abstract's unqualified claim is **conflicted** (F16). In the 25-cell grid entry rises 2.81-3.09 pp in the 6 cells meeting Prop. A.7 (analytical), is unchanged in 9 cells with d ≤ 0.75, and falls 4.03-4.49 pp in the 10 cells with d ≥ 0.76 (numerical diagnostic). Footnote on frame 13, also spoken; detail in A6 | main.md 8, 330-336; `tables/table_signal_grid.tex` | `signal_trader_accuracy_value`, `signal_buyer_accuracy_value`, `signal_entry_weak`, `signal_entry_strong` |
| C23 | At r1, price access raises target proceeds and net acquisition surplus | supported at r1 only (analytical, Prop. A.9) | main.md 347-353; Table 2 Panel C | `base_revenue_feedback`, `base_revenue_hidden`, `base_revenue_gain`, `base_net_surplus_gain`; W levels printed in Table 2 Panel C |
| C24 | Price access helps "at any fixed strength" | **conflicted** (main.md 23 vs Prop. A.9; F15). Slides use the r1 wording plus "at r0 no gain" | main.md 23 | none |
| C25 | Matched dividend: mean prices match but entry does not, so information matters, not the price level | descriptive only (diagnostic). The text's "analytical invariance diagnostic" vs registry's numerical diagnostic is **conflicted** (F10); slides tag "diagnostic". Backup A23 | main.md 353 | `base_matched_dividend` |
| C26 | Under Nash bargaining, stronger competition weakly lowers challenger profit for every η; the spread effect is weakly positive for η < 1/2, weakly negative for η > 1/2 | supported (analytical, Prop. A.8; "weakly", F49). Backup A9 | main.md 357-372 | none (figure data `figures_data/bargaining.csv`) |
| C27 | An entry reversal under bargaining; first-price equilibria | **excluded** (not solved). Said aloud when asked | main.md 372, 378, 408 | none |
| C28 | Raising the reserve 0.5 → 1.1 (value classes) raises expected proceeds at both strengths | supported (analytical at listed nodes). Backup A27 | main.md 383-392; Table 4 | `value_reserve_high`, `value_band_halfwidth`, `value_revenue_weak_low_p`, `value_revenue_weak_high_p`, `value_revenue_strong_low_p`, `value_revenue_strong_high_p`, `value_entry_weak_high_p`, `value_entry_strong_high_p` |
| C29 | An optimal reserve or optimal sale terms | **excluded** (open; "the next theorem"). Spoken on frame 16 as the open question | main.md 25, 392, 408 | none |
| C30 | Same orders can support different price pools, beliefs and entry | supported (analytical existence, Prop. A.10). Backup A28 | main.md 396, 991-1047 | `pool_reserve`, `pool_posterior_cutoff_low`, `pool_posterior_cutoff_high`, `pool_entry_cutoff_low`, `pool_entry_cutoff_high`, `pool_revenue_cutoff_low`, `pool_revenue_cutoff_high` |
| C31 | Disclosure records show a costly preparation stage (Imprivata) | descriptive only; frame 1 gray line and A1. Not evidence that a price drew a buyer in | main.md 39 | none |
| C32 | Prices drew a buyer into any real deal; benchmark magnitudes are calibrated | **excluded** (no sample; declared benchmark only) | main.md 39, 398-400 | none |
| C33 | In the model, the investor cannot profit by faking good news: every wrong-signed order has negative gross payoff against every candidate price and entry schedule | supported (analytical): both residual advantages in eq. 11 are positive for every candidate order distribution, so the wrong sign earns their negative; stated for the weak economy in Step 3 and for the certified nodes. Incumbent or target manipulation, toeholds and endogenous research are outside the model | main.md 197-209 (eq. 11), 289, 535, 679 | none |
| C34 | The investor's information is complementary, not superior: the challenger knows its integration plans, a specialist investor knows the target's customers, technology and demand; preparation (diligence) reveals the exact value; the reversal holds with d = 0.75 > a = 0.70 | supported (main.md 17, 37, 330; Prop. A.7 analytical, declared example). The benchmark's perfectly informed investor is a device "so that the mechanism is easy to see" (main.md 37) | main.md 17, 35, 37, 330-336 | `signal_trader_accuracy_value`, `signal_buyer_accuracy_value`, `signal_entry_weak`, `signal_entry_strong` |
| C35 | An empirical test needs the decision to prepare as its outcome, strength measured from information public before that decision, and prices that precede preparation; later returns can reflect anticipated arrival | descriptive only (a design; no sample, effect, instrument or identification strategy) | main.md 398-400; Online Appendix D | none |
| C36 | "Sale terms shape who competes" as a main-line implication | **conflicted** with what the main line shows: the main line varies strength, not terms, and the paper calls the seller's terms "the next theorem". Slides use the strength-based implication; sale terms are spoken on frame 16 as the open question (C29) | main.md 25, 404, 408 | none |
| C37 | Contrasts with Kyle and Vila (1991) and Schwert (1996) | **excluded** from slides: neither is in the paper or `references.bib`. Spoken Q&A only, after the author verifies both; on a slide only after they are added to the paper and the bib | none | none |

## 4. Emphasis ledger

- **Primary takeaway (frames 2, 9, 10a, 16).** A stronger incumbent can bring the challenger in, because it makes the target's stock price informative. At the benchmark, entry goes from 0.250 to 0.523 while the challenger's profit at the prior falls from 4.80 to 4.29 (analytical).
- **Support 1, one auction, two claims (frames 2, 5, 6).** A stronger incumbent lowers what the challenger keeps and raises what target shares reveal about the challenger (Prop. 1). Informed trading then puts that into the price (frame 7), and the price tells the challenger when expensive preparation pays (frame 8). The chain is the theorem's takeaway (frame 9).
- **Support 2, information is the channel (frames 2, 11).** Hold fixed what the price reveals and a stronger incumbent cannot raise entry (Prop. A.3). Freeze the orders and entry falls, 0.562 → 0.523 (numerical diagnostic; sign analytical). Hide the price and the rise disappears (0.250 at both strengths, analytical, implied by the high-cost window).
- **Boundary (frame 10b, once; conditions once on frame 9).** Rise, then fall: at r2 = 3.6, above a ceiling strength, trading stays informative but entry returns to 0.250. It is not repeated on frame 2 or frame 16.

Frames 12-15 (coexistence, robustness, welfare, empirical design) are secondary results. With frame 3 and frame 6 they form the cut list (section 10).

## 5. Color ledger

Madrid's structure blue (#3333B3) carries chrome only: title bar, footline, `\KeyIdea`, `\RunIn`, the ResultBox frame and the navigation buttons. It has no economic meaning. Two concept colors are declared once in the preamble and never used as a good/bad pair:

```latex
\colorlet{cInfo}{cAccentB!80!black}  % #AA4B00, contrast 5.65:1 on white: information force (new)
\colorlet{cCost}{cAccentC!70!black}  % #006F50, contrast 6.20:1 on white: preparation-cost objects (F30)
```

| Object | Baseline or new | Alias | Frames where it recurs |
|---|---|---|---|
| Target-payoff spread Δ_T and the words "target-payoff spread"; the information force; "Trading-cost window" label; the information chain | new (the paper's wedge) | `cInfo` | 5 (Δ_T line of the display), 6 (panel (a) curve, same hex; "spread" in the takeaway), 7 (Δ_T cell of the three-cell table; window label), 9 (window label; chain takeaway), 10a/10b (Δ_T row label), A8 (Δ_T row), A9 (Δ_η curves), A10 (Δ_T in the bounds), A17 (trading-cost margins), A18 (Information column header; chain line) |
| Preparation costs C, c_L, c_H, the probability ρ, the words "cheap / expensive preparation"; "Low-cost floor" and "High-cost window" labels | inherited primitive, colored separately per F30 | `cCost` | 4 (box ④ edge; cost legend item), 8 (c_L and c_H lines inside the X2 picture, same hex; both condition labels), 9 (two condition labels), A15, A17 (floor and window margins), A18 ("low-cost floor" in the Needs row; c_H inside the chain), A20 (c_H in τ) |
| Challenger profit g_H, g_L, B_r(μ); the deterrence force | inherited (baseline) | neutral: black text; figure curves black / dark gray / mid gray with solid, dashed and dotted lines and direct labels | 5, 6 (panel (b)), 8 (curves), 9, A18 (Deterrence column) |
| Entry, high-value ownership, orders (q_H, q_L), strengths r0, r1, r2 | outcomes and labels | neutral; the strong column is **bold** in tables | 7, 9-14 |
| Result-status labels (analytical, computer-assisted, numerical diagnostic, open, input) | bookkeeping | gray `\scriptsize`, never colored or boxed | 2, 5-14 and backups |

Unused on purpose:
- `cAccentA`: Okabe-Ito blue sits too close to Madrid's structure blue, so a cost color would read as chrome.
- `cAccentD`: amber is below 4.5:1 on white.
- `cHighlight`: no overlays.

At most two concept colors are active on any frame (9 and A18 use both). Reused paper figures (X3; X5 rebuilt with the paper palette) keep their own colors, and the text near them stays neutral.

## 6. Notation plan

### 6.1 Symbols on the main line (order of introduction)

| Symbol | Frame | Gloss on the slide | Audit rules applied |
|---|---|---|---|
| R; r | 4 | box ⑤ and legend: "incumbent value R ~ U[0, r], known only to itself; r = incumbent strength (public), a distribution, not a bid". Later "strength r0 → r1", never a bare r beside R | F31, F19 |
| θ ∈ {H, L}; h, ℓ | 4 | "challenger quality θ ∈ {H, L}, worth h or ℓ, equally likely; unknown to the challenger until it prepares". θ is never a number; formulas use h and ℓ directly | F01 |
| p | 4 | box ①: "reserve p" (said aloud). Legend: "p is the reserve price, not the stock price". The stock price is always in words on the main line (no P) | F31 |
| C; c_L, c_H; ρ | 4 | legend (`cCost`): "preparation cost C ∈ {c_L, c_H}, Pr(C = c_L) = ρ, independent of θ"; box ④: "entry = pay C, learn θ, can bid"; ρ = "entry floor" on frames 7-8 | F30, F22, F55 |
| t_H, t_L; Δ_T | 5 | "target-payoff spread Δ_T = t_H − t_L; t_θ = expected target proceeds when a θ-challenger enters" (gray line). T only as this subscript | F04, F36 |
| g_H, g_L | 5 | "g_H = 𝔼[(h − max{p, R})_+]: gross acquisition profit of a high-value challenger (g_L likewise with ℓ)". 𝔼 is safe because 𝖤 is not used anywhere on the main line. General support (R ~ F on [0, r̄], ℓ < r̄ < h) appears only in the gray Prop. 1 scope line | F28 (lowercase), F01, F19, F29 |
| r0, r1 | 6 | "weak r0 = 1.2, strong r1 = 3" (figure markers and subtitle); restated in frame 7's two bullets so that frame 6 can be skipped | F11 |
| μ; m, M; b | 7 | "the price reveals the market's belief μ = Pr(H); noise keeps it within [m, M], m = 1/(1 + e^{2/b}) ≈ 0.27, M = 1 − m (Laplace noise, scale b = 2)". Defined on the frame where ρ m Δ_T is first used, before X2 uses m and M | F40, F42, F31 |
| k; (q_H, q_L) | 7 | "orders (q_H, q_L) ∈ [−1, 1]: the order after a high / low challenger value; trading cost k per unit"; "full orders (1, −1)"; "no trade (0, 0)". No standalone q | F40, F05, F12, F13 |
| B_r(μ) | 8 | "B_r(μ) = g_L + μ(g_H − g_L): the challenger's expected gross profit at belief μ" | F01, F23 |
| r2 | 8 (X2 marker "stronger still r2 = 3.6"), stated on 9 | "stronger still, r2 (benchmark 3.6)" | F11, F46 |

Removed from the main line after the critique (item 15):
- 𝖤 and 𝖮_H: main-line tables and text say "Entry" (first use "Entry = Pr(challenger prepares)") and "High-value (challenger) ownership" (first use "= Pr(high-value challenger acquires the target)", F56). The symbols appear in backups only, always labeled in words (F29). With no 𝖤 on the main line, the 𝔼 on frame 5 cannot be confused with it.
- q alone: only (q_H, q_L). The one exception is the mandated F37 footnote phrase "every unilateral deviation q ∈ [−1, 1]" on frame 9, where q is a dummy variable.
- a, d: frame 13 says "investor accuracy 0.70, challenger accuracy 0.75" in words (F02, F53). The symbols appear in A5, A6 and A26.
- r_C: frames 8 and 10b say "a ceiling strength" in words; X2 shows it only as the crossing of the best-price curve and the c_H line. The symbol and ≈ 3.59 appear in A20 and A24.

Nodes r = 1.55, 1.60, 1.65 (frame 12) are labeled by value, never r_j (F11).

**Backup-only symbols:**
- 𝖤, 𝖮_H, always labeled in words (A20, A21, A22, A24, A26; F29, F55, F56, F09).
- q, U_θ(s) = sΠ_θ(s) − ks (A7, A10, A11; F17, F24).
- X, Z, P(X) (labeled "stock price"), V_T, μ_X(x) = Pr(H ∣ X = x), σ_H, σ_L (A7, A13; F02, F31).
- τ, glossed "belief threshold for costly preparation" with c_H annotated "expensive cost" (F44, F30); x*; α_θ = Pr(X ≥ x* ∣ θ); e_H, e_L without bars (A20; F09, F18, F20, F21).
- r_P, r_N, r_U, r_C (A20, A24; F41, F52).
- Investor signal T, challenger signal Y, accuracies a and d, and Pr(H ∣ P, Y = y) (A5, A6; F13, F44, F53).
- η, t_η, g_{θ,η}, Δ_η (A9; F04, F06, F28, F49).
- κ and pooled belief μ̄ in words (A28; F03, F21).
- ε_C (A14), ε_V (A27), D_0 (A23; F10).
- F, r̄ in general-support statements (A8; F19).

**Never shown anywhere:** v, s_L, u, λ, a_H, a_L, a_±, Q, H_C, h_C, G_θ, F_θ, φ_±, S̄ or F̄_Z, 𝔯(·), Δ_T^{-1}, 𝓔(p, r), 𝓡_T (write "expected target proceeds"), R_max, B_p, c as the pool cutoff, "(A1)-(A3)", "OA.3".

**Wording rules applied on every frame:**
- Role words only: incumbent, challenger, investor, market makers, noise traders. Never "buyer" or "trader" for a model agent (F13).
- "Entry" and "entry floor", never participation, preparation probability or investigation (F55).
- "No-trade equilibrium", never "pooling equilibrium" (F12).
- "Target-payoff spread", never "information spread" (F36).
- "High-value challenger ownership", never "high-quality" (F56).
- Conditions named "low-cost floor", "high-cost window", "trading-cost window" (F35).
- Uniqueness footnote: "arbitrary mixed orders; every unilateral deviation q ∈ [-1, 1]" (F37).
- Certified orders q_L ≈ −0.460, −0.707, −0.903 (F05).
- Margins called "theorem margins" (F44).
- Deterrence at a fixed experiment is weak: "cannot raise entry" or "weakly lowers entry" (Prop. A.3).

### 6.2 Deliberate differences from the paper's current text (paper-sync entries)

| # | Slide version | Paper location that differs | Audit ID |
|---|---|---|---|
| 1 | "quality θ ∈ {H, L}, worth h or ℓ; μ = Pr(H)"; formulas use h, ℓ, never θ as a number | main.md 51, 91, 131-132, 197, 363-364 and others in F01 | F01 |
| 2 | Lowercase g_H, g_L (bargaining g_{θ,η}), written with h and ℓ. The author must pick between F28's lowercase and F01's capital G with v_θ | main.md 131-132 (G_θ(F)), 364 (G_{θ,η}); eq. 6 | F28, F01 |
| 3 | "target-payoff spread Δ_T = t_H − t_L" in text, the A8 table row, and the rebuilt X1 and X4 axis labels | Table 1 row "Information spread"; main.md 897; `numerics/render/tables.py:188`; `numerics/render/figures.py:246, 359` | F36 |
| 4 | Prop. 2 conditions named (low-cost floor, high-cost window, trading-cost window) | main.md 219-229 labels (A1)-(A3) | F35 |
| 5 | "every unilateral deviation q ∈ [-1, 1]" | main.md 21, 233, 334, 821 ("every continuous deviation") | F37 |
| 6 | "entry" and "entry floor" throughout; in backups 𝖤 glossed "Pr(challenger prepares)"; main line says "Entry" in words | abstract (main.md 8), 23, 57, 235, 253; Table 2 note ("preparation probability") | F55 |
| 7 | Role words only; "challenger", never "buyer"; "investor", never "trader" | main.md 19, 35, 269, 330, 357 and others; `tables/table_signal_grid.tex` header "Buyer d" | F13 |
| 8 | Controls table headed "Information controls"; price-hidden rows called "equilibrium of the no-price-access game"; Panel A called "equilibria of the feedback game" | main.md 265 note ("fixed-profile controls"), 267 | F08 |
| 9 | Frozen-order entry labeled "numerical diagnostic; sign analytical (Prop. A.3)" | main.md 267 prints numbers without status | F50 |
| 10 | Welfare stated at r1, plus "at r0 prices are uninformative, so there is no gain" | main.md 23 ("At fixed incumbent strength") | F15 |
| 11 | Matched dividend tagged "diagnostic" | main.md 353 ("analytical invariance diagnostic") | F10 |
| 12 | Open set attached to (i)-(ii) with every h > ℓ; the fall (iii) presented at the benchmark and nearby | main.md 233, 548, 550 | F46 |
| 13 | Robustness claimed for r0 → r1 only | main.md 733 (Prop. A.5 extends all of Prop. 2) | F47 |
| 14 | Coexistence stated at three strengths; elsewhere the search is not exhaustive | main.md 23 | F48 |
| 15 | Certified equilibria written (1, q_L), q_L ≈ −0.460, −0.707, −0.903 at r = 1.55, 1.60, 1.65, with negated registry intervals; no v_j or r_j | main.md 275-287, 645-656, 697; registry and manifest definition prose | F05, F11 |
| 16 | Rebuilt Figure 2 labels asymmetric orders "(1, q_L)", symmetric interior "q_H = −q_L < 1", axis "order size abs(q_L)"; no v or u | `numerics/render/figures.py` Figure 2 annotations "(1, −v)", "(u, −u)" | extends F05 (not in the audit's location list) |
| 17 | No-trade uniqueness bound written r_P ≈ 1.22; thresholds annotated by meaning | main.md 296, 572, 579, 595 (𝔯(k)); Fig. 2 caption omits it | F41, F52 |
| 18 | Complementary-signal example plus the 25-cell grid footnote | main.md 8, 23, after 336 | F16 |
| 19 | Accuracies as probabilities 0.70 and 0.75 (a = 0.70, d = 0.75 in backups) | main.md 336 ("70%", "75%"); manifest display | F53 |
| 20 | Bargaining effects stated "weakly"; transfer in words as t_η | main.md 363 (T_η), 370, 897, 899-906 (P) | F49, F04, F06 |
| 21 | Global bound written U_θ(s) = sΠ_θ(s) − ks | main.md 487-535, 633-679 (F_θ(s)) | F17 |
| 22 | α_θ = Pr(X ≥ x* ∣ θ); e_H, e_L without bars and defined before use | main.md 239-253, 548, 796-806; OA | F09, F18, F20, F21 |
| 23 | Price-pool cutoff κ; pooled belief in words; cited "Prop. A.10" | main.md 991-1047, 1148; OA 759 (OA.3) | F03, F21, F32 |
| 24 | Binary-value alternative reserve stated "p = 1.01" | main.md 383, 1146 (absent from text and registry; new key `binary_reserve_high`) | F39 |
| 25 | Logistic threshold "x* ≈ 5.42, about 1.5 noise s.d." | manifest display of `logistic_flow_threshold` | F38 |
| 26 | "high-value challenger ownership" | OA 216, 1527; manifest rows `base_ownership_*` | F56 |
| 27 | "m = 1/(1 + e^{2/b}) ≈ 0.27" | main.md 1027 | F42 |
| 28 | General-support statements use r̄, never R_max | main.md 359, 897 | F19 |
| 29 | Serif math font so 𝖤 stays distinct in backups; 𝖤 always labeled in words | style only | F29 |

## 7. Exhibit inventory

| Id | Source | Treatment | Target file | Necessity | PowerPoint treatment |
|---|---|---|---|---|---|
| X1 | Figure 1 `figures/two_returns.pdf`; data `figures_data/two_returns.csv` (rows mu = 0.5) | **rebuild from CSV**. Panel (a) Δ_T(r) in `cInfo` (#AA4B00), axis "target-payoff spread Δ_T". Panel (b) (g_H + g_L)/2 in black, axis "challenger's expected profit at the prior". Gray dotted verticals labeled "weak r0 = 1.2", "strong r1 = 3" (`base_r_weak`, `base_r_strong`). x range 1.0-3.8; fonts ≥ 11 pt at 0.92\linewidth; (a)/(b) labels; no title; vector PDF with embedded fonts. *Rationale:* the source axis reads "information spread" (F36); the source panel (b) plots μ = m, M before they are defined (F40); markers tie the curves to the benchmark economies; a crop cannot fix labels. *Status:* rebuilt figure, individual QA required | `talk/figures/two_returns_talk.pdf` (+ `.svg`, 300-dpi `.png`) | Load-bearing but skippable: the two opposed returns at benchmark scale (frame 6); its two numbers are spoken on frame 5 if it is skipped | picture (SVG) |
| X2 | Figure 1 panel (b) data `figures_data/two_returns.csv` (mu ∈ {m, 1/2, M}); inputs `base_c_low`, `base_c_high`, `base_r_*` | **rebuild from CSV**, one panel. Curves: B_r(μ) at μ = M (solid black), 1/2 (dashed dark gray), m (dotted mid gray), with direct labels "best price (M)", "prior", "worst price (m)". Horizontal lines c_H = 6 (solid `cCost`, "expensive cost c_H") and c_L = 1 (dashed `cCost`, "cheap cost c_L"), drawn inside the figure file. Verticals at r0, r1, r2 labeled; the r2 label sits on the right of its vertical, away from the crossing. No r_C tick or label: the ceiling is visible only as the crossing of the best-price curve and the c_H line (the two are about 0.25% of the axis apart, so a tick and the r2 label would collide). y range 0.5-7.5. No computed number printed. *Rationale:* the low-cost floor and the high-cost window are comparisons of cost levels against belief-specific profit curves; no source exhibit draws the cost lines, and two inequalities in text are harder to read than the picture. *Status:* rebuilt figure, individual QA required | `talk/figures/profit_thresholds_talk.pdf` (+ `.svg`, `.png`) | Load-bearing: makes the floor, the window and the r2 ceiling visible before the theorem (frame 8) | picture, cost lines inside it (never redrawn as native lines over the picture, which would misalign on rescale) |
| X3 | Figure 3 `figures/posterior_tail_entry.pdf` | **reuse** (copy; labels Pr(μ_X ≥ τ), "threshold distance M − τ" already comply with F43) | `talk/figures/posterior_tail_entry.pdf` (+ `.png`) | Backup A14 | picture |
| X4 | Figure 4 `figures/bargaining_weight.pdf`; data `figures_data/bargaining.csv` (columns eta, r, Delta_eta) | **rebuild panel (a) only**: Δ_η vs η at r = 1.2 (dashed) and 3 (solid), `cInfo`; η = 1/2 marked; axis "target-payoff spread Δ_η" (F36). Panel (b) dropped: capital G against F28, and a busy log scale. *Status:* rebuilt figure, individual QA required | `talk/figures/bargaining_spread_talk.pdf` (+ `.svg`, `.png`) | Backup A9 | picture |
| X5 | Figure 2 `figures/equilibrium_correspondence.pdf`; data `numerics/correspondence.csv`, `mixed_supports.csv`, `thresholds.csv`, `certificates.csv` | **rebuild from CSV** by adapting the plotting logic in `numerics/render/figures.py` (labels only; no solving; no branch dropped). Two single-panel files: (a) entry vs r; (b) order size abs(q_L) vs r. Relabel per paper-sync #16. Keep: broken lines at unresolved nodes, certified black points with interval bars, analytical shading, r_N, r_U, r_C, and visible "computer-assisted" / "numerical diagnostic" legends (F48). Legend note: "certified enclosures are narrower than the marker; exact intervals in A21", so the bars are not read as missing. Fallback if the rebuild cannot be verified: the source PDF with white-box relabels, which in PowerPoint are native shapes | `talk/figures/equilibrium_correspondence_a_talk.pdf`, `..._b_talk.pdf` (+ `.png`) | Backups A24, A25 | picture (+ native relabel shapes on the fallback) |
| D0 | New simple diagram: three-box opener timeline | **new simple diagram**. Three rounded boxes, two arrows: "Approach or review disclosed" → "Target stock keeps trading" → "Challenger decides whether to pay to prepare" (last box edged `cCost`). *Rationale:* gives the opening question a picture and previews D1. *Status:* new figure, individual QA required | inline in `talk/talk.tex` | Frame 1 | 3 rounded rectangles + 2 arrows + text |
| D1 | New simple diagram: model timeline with agents | **new simple diagram**. Five rounded boxes with explicit `text width`, bold agent name on top, one action line beneath, four arrows, no plotted coordinates: ① **Seller:** commits to a cash second-price auction, reserve p → ② **Investor:** knows θ; trades the target's stock against noise traders → ③ **Market makers:** see only total order flow; set the stock price → ④ **Challenger:** sees the price and its cost C; entry = pay C, learn θ, can bid (box edged `cCost`) → ⑤ **Bidders:** incumbent value R ~ U[0, r], challenger worth h or ℓ; bid truthfully. *Rationale:* the load-bearing assumption is an order of moves (price before entry); each box names who acts, so the primitives need no separate bullet list. *Status:* new figure, individual QA required | inline in `talk/talk.tex` | Frame 4 | 5 rounded rectangles + 4 arrows + text |
| D2 | Causal chain | native text with `\to` in one `cInfo` line (not a diagram) | inline | Frame 9 (takeaway); A18 | one text box |
| T1 | Payment comparison, main.md 17, 137 | **native table**, 2 rows × 4 columns | inline | Frame 5 | native table |
| T2 | Residual advantage, eq. 11 | **native table**, one row × three cells: "entry probability (≥ ρ)" × "`cInfo` target-payoff spread Δ_T" × "market's remaining uncertainty (≥ m)", with the bound ρ m Δ_T ≤ advantage ≤ Δ_T on one line beneath. Replaces the underbraced text display, which renders poorly in Office Math | inline | Frame 7 | native table + one equation |
| T3 | Table 1 (registry scalars) + Table 2 Panel A (`tables/table2_equilibrium_controls.tex`) | **native table**, 6 rows × 2 columns (10a), + 1 column (10b). Row labels in words ("Entry", "High-value ownership") | inline | Frames 10a/10b | native table (two slides) |
| T4 | Table 2 Panels A-B | **native table**, 3 rows + group label × 2 values + status (F08 labels); the hidden row carries the annotation "implied by the high-cost window" | inline | Frame 11 | native table |
| T5 | Prop. 3, eq. 13; registry `cert_*` | **native table**, 3 rows: r, q_H, q_L ≈, Entry ≈ | inline | Frame 12 | native table |
| T6 | Table 3 (`tables/table3_extensions.tex`) | **native table**, 5 rows × 3 columns (specification, weak, strong). The pp column, the Evidence/Unique columns and the ownership columns are dropped; the signals row names its own ρ and strengths; F16 footnote | inline | Frame 13 | native table |
| T7 | Table 2 Panel C | **native table**, 2 rows × 3 columns | inline | Frame 14 | native table |
| T8-T17 | Backup tables | **native tables**: synthesis, deterrence vs information (A18, from the former main frame, with "weakly ↓"); benchmark vs moderate inputs (A19); Table 1 at r0, r1 (A8); margins (A17); Table 2 Panels A-B in full (A22); certificate enclosures (A21); signal-grid summary, 3 rows (A6); Table 3 in full (A26); Table 4 Panel B (A27); notation (A12); in-model vs out-of-model rows (A4) | inline | Backups | native tables |

The paper's tables are never pasted or `\input`. Every rebuilt or new figure is marked "QA complete" only after the standalone asset and each slide page that shows it have been opened and checked. X1 and X2 must use the same hex values as the slide aliases.

## 8. Main deck, frame by frame

Conventions:
- **Bold** = bold lead phrase.
- `[nav: X → Ay]` = a `\PlaceNav` button.
- "gray" = `\graycite` or `\scriptsize` gray text.
- Numbers carry their registry name in parentheses, which becomes a LaTeX comment and a `results.tex` macro.
- A frame with navigation uses `\TakeawayWithNav`, or `\PlaceNav` alone when it has no takeaway.

**Frame 0. Title** (`[plain]`, uncounted). 0.25 min.
- Paper title on two balanced lines; "Austin Li". Nothing else.
- Spoken: one sentence of self-introduction; "questions welcome as we go".

**Frame 1. Does a stronger incumbent keep the challenger out?**
- Subtitle: The decision interval this paper is about
- Content:
  - D0 three-box timeline at the top: approach or review disclosed → target stock keeps trading → challenger decides whether to pay to prepare
  - The **incumbent** bidder is already prepared; the market knows how strong it is, not what it will bid
  - A **challenger** must first pay to prepare an executable bid (diligence, financing, approvals); paying is **entry**
  - **Received answer:** a stronger rival lowers what preparation earns, so it deters entry `\graycite{Fishman 1988; Hirshleifer and Png 1989}`
  - **But** the challenger decides while the stock trades, and it can watch the price
  - Gray line: Imprivata's 2016 proxy separates an unsolicited approach, outreach to potential buyers, and indications of interest conditional on further diligence: a costly preparation stage, not evidence that a price drew anyone in `\graycite{Imprivata 2016}` (main.md 39)
  - Closing line: `\KeyIdea{The twist:}` that price is an equilibrium object, and competition changes what it reveals
- Takeaway: the twist line. Claim status: descriptive setting (C31); received logic supported (Prop. A.3 later confirms it at fixed information).
- Minutes 2.0. Nav: [Which deals fit → A1] (`main:interval`), [Evidence: a design → A2] (`main:evidence`). Notation: none.
- Spoken hooks:
  - "The model needs an interval, not a date; a wholly confidential process does not qualify."
  - "I am not claiming deterrence is wrong. I am claiming it can be outweighed, and I owe you the set of primitives on which that happens."

**Frame 2. This paper** (punchline; headline numbers on screen at about 2.75 min)
- Subtitle: none
- Content:
  - Framing line: A takeover auction in which an informed investor trades the target's stock before a challenger decides whether to pay to prepare a bid; prices are rational, and trading and entry are solved in equilibrium.
  - `\KeyIdea{Competition creates competition}` (gray: analytical): a stronger incumbent can turn an uninformative stock price into an informative one and raise entry.
    - Benchmark: entry 0.250 → 0.523, although the challenger's expected profit at the prior falls 4.80 → 4.29 (`base_entry_weak`, `base_entry_strong`, `base_profit_prior_weak`, `base_profit_prior_strong`)
  - **One auction, two claims:** a stronger incumbent lowers what the challenger keeps but makes target proceeds more sensitive to who the challenger is, and informed trading puts that into the price
  - **Information is the channel:** hold fixed what the price reveals, and a stronger incumbent cannot raise entry, as the textbook says (gray: sign analytical, Prop. A.3)
  - **Implication:** when the target trades, a stronger rival is not a pure deterrent: who competes depends on what the price reveals before anyone prepares.
- Takeaway: the Implication line. Claim status: supported (C7, C8, C14 sign only, C36 wording). Four numbers, all analytical; no diagnostic number on this frame (F50).
- Minutes 2.0. Nav: none. Notation: none (entry and profit in words).
- Spoken route, replacing a roadmap frame: "the model, the two forces, the theorem, the numbers, and the control that shows information does the work."

**Frame 3. What is new relative to learning from prices**
- Subtitle: Four closest antecedents
- Content:
  - **Prices guide real decisions** `\graycite{Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang 2015}`: here the sale rule splits one surplus into a traded claim and the challenger's claim, and competition moves them in opposite directions
  - **Stronger incumbents deter** `\graycite{Fishman 1988}`: kept intact; I add a market that trades before preparation
  - **Auction entry is endogenous** `\graycite{Levin and Smith 1994}`: here entry responds to what the price reveals
- Takeaway (`\TakeawayWithNav`): The increment is the opposition between the two returns to information, and the entry reversal it produces.
- Claim status: positioning. Metadata checked against `references.bib` (Fishman 1988 RAND J. Econ.; Dow, Goldstein and Guembel 2017 JEEA; Edmans, Goldstein and Jiang 2015 AER; Levin and Smith 1994 AER). No "first" or "only".
- Minutes 0.75. Nav: [Related work → A3] (`main:lit`), [References → A29] (`main:refs`). Notation: none.
- Prepared Q&A contrasts, spoken only, never on a slide (C37; neither work is in the paper or `references.bib`; the author verifies both before use):
  - Kyle and Vila (1991), noise trading and takeovers: there the informed trader is the raider, using noise trading to build a position before bidding. Here the investor cannot bid, and the price informs a third party's entry decision.
  - Schwert (1996), pre-bid run-ups: those price moves follow the anticipation of a bid. Here the price moves before the challenger decides whether to prepare, a different timing (frame 15).

**Frame 4. Model: who moves, who knows what, and when** (frames 4 and 5 of the earlier plan, merged)
- Subtitle: The challenger sees the price and its own cost, never the order flow, θ or R
- Content:
  - D1 timeline (five boxes, each naming its agent; see section 7)
  - Legend item 1 (gray-black): 0 < p < ℓ < r < h. The incumbent is already prepared and knows only its own value R; r = incumbent strength (public), a distribution, not a bid. Challenger quality θ ∈ {H, L} is equally likely and unknown to the challenger until it prepares. p is the reserve price, not the stock price.
  - Legend item 2 (`cCost`): **Cost:** preparation cost C ∈ {c_L, c_H}, Pr(C = c_L) = ρ, independent of θ (cheap / expensive preparation)
- Takeaway: none (a schematic plus two legend items). Claim status: model primitives (input); C6.
- Minutes 2.75. Nav: [What is left out → A4] (`main:omit`), [Why would the investor know? → A5] (`main:info`), [Equilibrium → A7] (`main:eq`). Notation: R, r, θ ∈ {H, L}, h, ℓ, p, C, c_L, c_H, ρ (four grouped objects; section 1). The equilibrium definition bullet of the earlier plan moves to A7.
- Spoken:
  - "Read the order of moves once; it is the load-bearing assumption. If preparation came before trading there would be nothing to learn."
  - "Neither bidder trades; the investor knows θ, not R."
  - "The benchmark gives the investor perfect information only to make the mechanism visible; Section 5.3 removes it." (main.md 37; A5)
  - Say "reserve p" and "incumbent strength r" aloud at first use (F31).

**Frame 5. One auction, two claims, opposite responses**
- Subtitle: Cash second-price auction with reserve p: who wins and who pays at incumbent value R
- Content:
  - T1 native table:

    | Incumbent value | High-value challenger | Low-value challenger | Gap in target proceeds |
    |---|---|---|---|
    | R ≤ ℓ | wins, pays max{p, R} | wins, pays max{p, R} | 0 |
    | R > ℓ | wins, pays R | loses; incumbent pays ℓ | R − ℓ |

  - One display, two aligned lines, each with an arrow sign tag:
    - `\textcolor{cInfo}{Δ_T = t_H − t_L = 𝔼[(R − ℓ)_+]}` ↑ (target-payoff spread)
    - g_H = 𝔼[(h − max{p, R})_+] ↓ (challenger's gross profit; g_L likewise)
  - Gray line: Proposition 1 (analytical): both signs hold for any first-order strengthening, R ~ F on [0, r̄], ℓ < r̄ < h (benchmark: uniform, r̄ = r). t_θ = expected target proceeds when a θ-challenger enters.
- Takeaway (`\TakeawayWithNav`): One shift, opposite signs: winning costs the challenger more, and target shares become more sensitive to who the challenger is.
- Claim status: supported, analytical (C1, C2).
- Minutes 2.5. Nav: [Closed forms → A8] (`main:payoffs`), [Other payment rules → A9] (`main:payrule`). Notation: t_H, t_L, Δ_T, g_H, g_L.
- Spoken:
  - Walk the value line. A low-value challenger that loses to a strong incumbent sets what the incumbent pays; that asymmetry is the whole source of the spread.
  - First answer to "why a second-price auction?": "With private values, an open ascending contest ends at the runner-up's value, just as this rule does, which is why takeover-contest models commonly use it. The property that matters is that a losing low-value challenger sets the incumbent's price." Then point to A9: under bargaining the spread effect holds only weakly and can flip sign (F49). First-price equilibria are not solved (C27); say so. (Spoken only; the paper states no equivalence, so no citation goes on the slide.)
  - If frame 6 will be skipped (checkpoint, section 10): "At the benchmark the spread rises from 0.0167 to 0.667 while profit at the prior falls from 4.80 to 4.29."

**Frame 6. A stronger incumbent: spread up, profit down**
- Subtitle: Declared benchmark; weak r0 = 1.2, strong r1 = 3; auction-stage payoffs, before trading and entry (`base_r_weak`, `base_r_strong`)
- Content:
  - X1 figure (rebuilt), width 0.92\linewidth, height about 0.6\textheight. Panel (b) is the challenger's expected profit at the prior, (g_H + g_L)/2.
- Takeaway: From r0 to r1 the spread rises 0.0167 → 0.667 while profit at the prior falls 4.80 → 4.29 (`base_spread_weak`, `base_spread_strong`, `base_profit_prior_weak`, `base_profit_prior_strong`): deterrence at every fixed belief, and more for the stock to reveal.
- Claim status: supported, analytical (C1); gray stamp under the figure.
- Minutes 1.5. Nav: none. Notation: r0, r1. Cut item 2 (section 10).

**Frame 7. Trading pays only against a strong incumbent** (now before the price frame, so the audience learns why the price moves before seeing what it tells the challenger)
- Subtitle: Investor knows θ; orders (q_H, q_L) ∈ [−1, 1] after a high / low challenger value; trading cost k per unit; market makers price anticipated entry
- Content:
  - Definition line: The price reveals the market's belief μ = Pr(H); noise keeps it within [m, M], m = 1/(1 + e^{2/b}) ≈ 0.27, M = 1 − m (Laplace noise, scale b = 2) (`base_m`, `base_M`, `base_b`)
  - T2 native table, one row, three cells: residual advantage per unit = [entry probability, ≥ ρ] × [`cInfo` target-payoff spread Δ_T] × [market's remaining uncertainty, ≥ m]. One display line beneath: ρ m Δ_T ≤ advantage ≤ Δ_T. (Entry ≥ ρ because cheap preparation pays after any price, the low-cost floor, drawn on the next frame.)
  - **Weak r0 = 1.2:** advantage ≤ Δ_T(r0) = 0.0167 < k = 0.02: every order loses, so no trade, (q_H, q_L) = (0, 0) (`base_spread_weak`, `base_k`)
  - **Strong r1 = 3:** each extra unit earns at least (1 − 1/b) ρ m Δ_T(r1) = 0.0224 > k, so full orders (q_H, q_L) = (1, −1). Gray gloss on the factor: "(1 − 1/b) is a haircut for the order's own price impact: with Laplace noise, one more unit erodes the per-unit advantage by at most a fraction 1/b"
  - `\textcolor{cInfo}{\textbf{Trading-cost window}}` Δ_T(r0) < k < (1 − 1/b) ρ m Δ_T(r1)
  - Gray arithmetic line: (1 − 1/2) × 0.25 × m × 0.667 = 0.0224 = k + theorem margin 0.00241 (`base_b`, `base_rho`, `base_m`, `base_spread_strong`, `base_k`, `base_margin_strong_trade`)
- Takeaway (`\TakeawayWithNav`): The same stronger incumbent that lowers the challenger's profit switches informed trading on.
- Claim status: supported, analytical (C3, C5, C33 spoken).
- Density: definition line, table with one display line, three bullets, gray arithmetic: 6 items, 1 display. Render fallback: move the (1 − 1/b) gloss into the speaker note before touching font size.
- Minutes 3.0. Nav: [Global trading bound → A10] (`main:bound`), [Orders, units, costs → A11] (`main:orders`), [Notation → A12] (`main:notation`). Notation: μ, m and M, b, k, (q_H, q_L) (five objects).
- Spoken:
  - "The investor has no position, no control rights and no route to bidding: not a toehold story."
  - "The investor cannot profit by faking good news: a wrong-signed order loses against every price schedule the market could use." (C33; A10)

**Frame 8. Only good news makes expensive preparation pay**
- Subtitle: Profit B_r(μ) = g_L + μ(g_H − g_L) at the worst, prior and best belief a price can induce; costs c_L = 1, c_H = 6 (`base_c_low`, `base_c_high`)
- Content:
  - X2 figure (rebuilt), height about 0.55\textheight; cost lines inside the picture; r2 marker labeled on its right; no r_C label
  - Reading bullet 1 (`cCost` label): **Low-cost floor** c_L < B_{r1}(m): a cheap challenger enters after any price, so entry ≥ ρ (the bound used on the previous frame)
  - Reading bullet 2 (`cCost` label): **High-cost window** B_{r0}(1/2) = 4.80 < c_H = 6 < B_{r1}(M): the expensive challenger stays out at the weak prior and enters after the best news against r1. Beyond a ceiling strength, even the best price falls short (r2, frame 10b) (`base_profit_prior_weak`, `base_c_high`)
- Takeaway: none (the two reading bullets are the reading). Gray stamp: analytical (Props. A.1, A.2, A.4); costs are inputs.
- Claim status: supported (C3, C4, C20 in words).
- Minutes 2.25. Nav: [Reading the price → A13] (`main:suff`), [Why Laplace noise → A14] (`main:laplace`), [Is the floor doing the work? → A15] (`main:floor`). Notation: B_r(μ), r2 (marker).
- Spoken: "Notice that against the weak incumbent the best-price curve also clears c_H. That does not help: we just saw the weak incumbent's price never moves. What the weak incumbent lacks is a price that moves; hold that thought for the control."

**Frame 9. Proposition 2: a stronger incumbent can raise entry**
- Subtitle: Weak r0, strong r1, stronger still r2; all other primitives equal
- Content:
  - One ResultBox titled "Proposition 2 (analytical)":
    - (i) **Weak r0:** unique outcome no trade, (q_H, q_L) = (0, 0); the price is uninformative; entry = ρ
    - (ii) **Strong r1:** unique outcome full orders (1, −1); the price is informative; entry > ρ; a high-value challenger acquires the target more often
    - (iii) **Stronger still, r2,** where the low-cost floor and profitable trading persist but B_{r2}(M) < c_H: full orders, entry back to ρ
  - Below the box, "Under three conditions" (inline math, one line each, names and inequalities only):
    - `\textcolor{cCost}{\textbf{Low-cost floor}}` c_L < B_{r1}(m)
    - `\textcolor{cCost}{\textbf{High-cost window}}` B_{r0}(1/2) < c_H < B_{r1}(M)
    - `\textcolor{cInfo}{\textbf{Trading-cost window}}` Δ_T(r0) < k < (1 − 1/b) ρ m Δ_T(r1)
  - Gray footnote: (i)-(ii) hold on a nonempty open set of primitives, for every h > ℓ; (iii) at the benchmark and nearby. Uniqueness of trading and on-path entry under truthful bidding: arbitrary mixed orders; every unilateral deviation q ∈ [-1, 1].
- Takeaway (`\TakeawayWithNav`, chain in `cInfo`): stronger incumbent → wider Δ_T → informed trading pays → informative price → good news clears c_H → the expensive challenger enters
- Claim status: supported (C7-C10, C13). Density: 3 box items + 3 conditions = 6 items; no display equation; 1 box. Render check: if the chain wraps beside three buttons, drop its first arrow ("wider Δ_T → …").
- Minutes 2.5. Nav: [Proof logic → A16] (`main:proof`), [Margins → A17] (`main:margins`), [Two forces side by side → A18] (`main:forces`). Notation: r2 recalled from X2.
- Spoken: (iii) in words: "the floor and profitable trading still hold at r2; only the best price stops covering expensive preparation."

**Frame 10a. At the benchmark, entry rises from 0.250 to 0.523**
- Subtitle: Declared benchmark; units arbitrary (inputs in backup); unique equilibrium outcomes (analytical)
- Content:
  - Definitions line: Entry = Pr(challenger prepares); high-value challenger ownership = Pr(high-value challenger acquires the target)
  - T3 native table (`\vspace{4pt}` under the title bar; strong column bold):

    | | weak r0 = 1.2 | **strong r1 = 3** |
    |---|---|---|
    | Challenger's profit at the prior B_r(1/2) | 4.80 (`base_profit_prior_weak`) | **4.29** (`base_profit_prior_strong`) |
    | `cInfo` Target-payoff spread Δ_T | 0.0167 (`base_spread_weak`) | **0.667** (`base_spread_strong`) |
    | Investor orders (q_H, q_L) | (0, 0) | **(1, −1)** |
    | Price | uninformative | **informative** |
    | Entry | 0.250 (`base_entry_weak`) | **0.523** (`base_entry_strong`) |
    | High-value ownership | 0.125 (`base_ownership_weak`) | **0.324** (`base_ownership_strong`) |

- Takeaway: Entry rises 27.28 percentage points (`base_entry_change_pp`) while the challenger's profit at the prior falls: the price, not the prize, brings it in.
- Claim status: supported, analytical (C8, C16).
- Minutes 1.5. Nav: none (build step; its buttons live on 10b). Notation: none new.
- Spoken: "Extra entry follows good news, which is likelier when the challenger is high value, so ownership rises too."

**Frame 10b. At the benchmark, entry rises from 0.250 to 0.523** (duplicate of 10a with one added column)
- Added column **very strong r2 = 3.6** (`base_r_collapse`):
  - profit: *lower still* (gray italic)
  - spread: *wider still* (gray italic)
  - orders: (1, −1)
  - price: informative
  - Entry: 0.250 (`base_entry_collapse`)
  - High-value ownership: 0.125 (Table 2 Panel A)
  - The words replace numbers found only in the CSV (C11).
- Takeaway (`\TakeawayWithNav`): Rise, then fall: above a ceiling strength even the best price cannot cover expensive preparation, so entry returns to ρ while trading stays informative.
- Claim status: supported at the benchmark (C10, C11); no claim for every h > ℓ.
- Minutes 1.0. Nav: [Benchmark scale → A19] (`main:scale`), [How entry is computed → A20] (`main:entry`), [Which equilibrium? → A21] (`main:cert`). Notation: none new.
- Spoken:
  - "Any stronger incumbent at which the floor and profitable trading persist but the best price falls short gives the same fall; 3.6 is the declared node." (F46: do not stress the distance to the ceiling.)
  - "The reversal compares economies in which trading is unique, so no equilibrium selection is needed." (A21)

**Frame 11. Freeze the information and deterrence returns**
- Subtitle: Entry at r0 = 1.2 and r1 = 3; equilibria of the feedback game, then information controls
- Content: T4 native table:

  | | r0 = 1.2 | r1 = 3 | Status |
  |---|---|---|---|
  | Equilibrium of the feedback game (price seen, trading re-solved) | 0.250 | **0.523** | analytical |
  | *Information controls* | | | |
  | Frozen informative orders (control, not an equilibrium at r0) | 0.562 (`base_frozen_entry_weak`) | 0.523 (`base_frozen_entry_strong`) | numerical diagnostic; sign analytical (Prop. A.3) |
  | Price hidden from challenger (equilibrium of the no-price-access game) | 0.250 (`base_hidden_entry_weak`) | 0.250 (`base_hidden_entry_strong`) | analytical |

  - Gray note under the hidden row: implied by the high-cost window: without the price, expensive preparation never pays, so only the entry floor remains.
- Takeaway (`\TakeawayWithNav`): Hold the price experiment fixed and a stronger incumbent weakly lowers entry, as the textbook says; the rise comes from what the price reveals.
- Claim status: supported (C14, C15, C16).
- Minutes 2.25. Nav: [Controls in detail → A22] (`main:controls`), [Price level or information? → A23] (`main:welfare`). Notation: none new.
- Spoken hook: "This is the slide to come back to whenever someone doubts the channel. In the strong economy the frozen profile coincides with the equilibrium, so the whole difference comes from the weak economy, where full orders lose money. The hidden-price row is not a second test: it just says that without the price the rise disappears."

**Frame 12. At intermediate strength, equilibria coexist**
- Subtitle: Computer-assisted (Proposition 3): interval arithmetic on exact decimal inputs
- Content:
  - T5 native table:

    | Strength r | q_H | q_L (certified) | Entry (certified) |
    |---|---|---|---|
    | 1.55 (`cert_a_r`) | 1 | ≈ −0.460 (`cert_a_v_interval`, negated) | ≈ 0.545 (`cert_a_entry_interval`) |
    | 1.60 (`cert_b_r`) | 1 | ≈ −0.707 (`cert_b_v_interval`, negated) | ≈ 0.549 (`cert_b_entry_interval`) |
    | 1.65 (`cert_c_r`) | 1 | ≈ −0.903 (`cert_c_v_interval`, negated) | ≈ 0.551 (`cert_c_entry_interval`) |

  - Buy fully after good news, sell partially after bad news; entry intervals strictly ordered upward
  - Each of these economies also has a no-trade equilibrium with entry ρ = 0.25
  - Elsewhere the numerical search is not exhaustive; the full correspondence is open
- Takeaway (`\TakeawayWithNav`): Between r0 and r1 there is multiplicity, and I read no monotone path into the gaps.
- Claim status: computer-assisted (C17); open (C18). F48 wording.
- Minutes 1.5. Nav: [Correspondence → A24] (`main:corr`). Notation: none new. Cut item 3 (section 10); if cut, say on 10b: "At three certified strengths between r0 and r1, an informative equilibrium coexists with no trade; the full correspondence is open."

**Frame 13. The entry reversal survives four model changes**
- Subtitle: Entry, weak to strong incumbent; each row a separate analytical result with its own declared parameters (Prop. 2 (i)-(ii))
- Content:
  - T6 native table:

    | Specification | Weak | Strong |
    |---|---|---|
    | Benchmark: Laplace noise, two cost levels | 0.250 | 0.523 (`base_entry_strong`) |
    | Atomless costs, half-width 0.1 (`cost_halfwidth`) | 0.250 | 0.523 (`cost_mix_laplace_entry_strong`) |
    | Logistic noise | 0.250 | 0.302 (`logistic_entry_strong`) |
    | Small value gap, h = 2, ℓ = 1 (`moderate_h`, `moderate_ell`) | 0.250 (`moderate_entry_weak`) | 0.527 (`moderate_entry_strong`) |
    | Complementary signals (declared example): investor accuracy 0.70, challenger accuracy 0.75; ρ = 0.85, strengths 1.1 vs 2.3 (`signal_trader_accuracy_value`, `signal_buyer_accuracy_value`, `signal_rho`, `signal_r_weak`, `signal_r_strong`) | 0.850 (`signal_entry_weak`) | 0.879 (`signal_entry_strong`) |

  - Gray note under the table: rows differ in ρ and strengths; compare within a row, not across rows.
  - Gray footnote (F16): Signals row is a declared example. In the 25-cell grid of accuracies, entry rises in the 6 cells meeting Prop. A.7 (analytical), is unchanged in 9 cells with challenger accuracy ≤ 0.75, and falls about 4 pp when it is ≥ 0.76, because the challenger's own good signal already triggers entry against the weak incumbent (numerical diagnostic).
- Takeaway (`\TakeawayWithNav`): The r0 → r1 reversal survives logistic noise, atomless costs, complementary private signals (declared example) and a small value gap (F47).
- Claim status: supported, analytical for r0 → r1 (C21); C22 via the footnote.
- Minutes 1.5. Nav: [Full table → A26] (`main:robust`). Notation: none new.
- Spoken:
  - Ask it yourself: "You may wonder why logistic noise shrinks the effect to 0.302. The posterior only approaches its bound in the tails, so good news is less decisive. Same sign, smaller size. Not a joint calibration."
  - Say the F16 line aloud rather than leaving the footnote to be read: "The price matters when the challenger's own signal is informative but not decisive; with a very accurate own signal, it already enters against the weak incumbent."

**Frame 14. Price access raises proceeds and surplus at r1**
- Subtitle: Hold the incumbent at r1 = 3; the challenger sees the price or does not; trading re-solved in both (analytical, Prop. A.9)
- Content:
  - T7 native table:

    | | Price observed | Price hidden | Gain |
    |---|---|---|---|
    | Expected target proceeds | 0.872 (`base_revenue_feedback`) | 0.615 (`base_revenue_hidden`) | 0.258 (`base_revenue_gain`) |
    | Acquisition surplus net of preparation costs | 2.38 (Table 2 Panel C) | 2.30 (Table 2 Panel C) | 0.0802 (`base_net_surplus_gain`) |

  - Same full orders in both economies, so trading costs coincide
  - Each extra entry happens only when its expected profit covers its cost
  - Gray: at r0 prices are uninformative, so there is no gain. The comparison does not rank incumbent strengths or sale mechanisms.
- Takeaway: none (the table and lines are the reading).
- Claim status: supported at r1 (C23; F15 wording; C24 avoided).
- Minutes 1.0. Nav: [Reserve → A27] (`main:reserve`). Notation: none new. Cut item 4 (section 10).
- Spoken guard: "This is a comparison of economies at r1, not a recommendation on process design."

**Frame 15. What an empirical test would have to measure**
- Subtitle: Section 7: a design, not a result
- Content:
  - **Outcome:** the start of substantive diligence or a proposal that needs costly preparation, not the number of public offers
  - **Strength:** measured from information public before that decision
  - **Timing:** price information must precede preparation; a traded stock during confidential negotiations is not enough
  - **Caution:** later target returns can reflect anticipated bidder arrival, so returns followed by entry do not by themselves show learning from prices
  - Gray: design only; no sample, effect, instrument or identification strategy is reported (Online Appendix D pilot)
- Takeaway: none. Claim status: descriptive only (C35); no estimate (C32 excluded).
- Minutes 1.0. Nav: none (the pilot design is A2, reached from frame 1). Notation: none. Cut item 5 (section 10).
- Spoken, only if asked about pre-bid run-ups: the Schwert contrast prepared on frame 3 (C37).

**Frame 16. Conclusion** (last main frame; no navigation)
- Content:
  - `\KeyIdea{A stronger incumbent can bring the challenger in:}` at the benchmark, entry rises from 0.250 to 0.523 although the challenger's profit at the prior falls
  - **Why:** competition makes target proceeds more sensitive to who the challenger is; informed trading puts that into the price; good news draws in the expensive challenger. Freeze that information and deterrence returns.
  - **Implication:** when the target trades, a stronger rival is not a pure deterrent: who competes depends on what the price reveals before anyone prepares.
- Claim status: supported (C7, C8, C14-C16, C36 wording).
- Minutes 1.0. Nav: none. Notation: none new.
- Spoken close, not on the slide: "Which sale terms a seller should choose, when terms move both what the winner pays and what the price reveals, is the next theorem: it needs the full price-and-trading continuation." (C29 as open.)

## 9. Appendix frames

All backups follow `\AppendixStart` in this order (displayed A1, A2, ...), grouped by origin frame. Each carries `\hypertarget{app:...}` and a `\BackButton` to its single origin.

| Label | Title | Content sketch | Linked from | Anticipated question |
|---|---|---|---|---|
| A1 `app:interval` | Which deals have a decision interval | A disclosed approach, strategic review or open contest can create one; none does so automatically; a wholly confidential process does not. Strength = the public distribution of the incumbent's value, not an announced bid. Imprivata's proxy separates approach, outreach and indications of interest conditional on diligence `\graycite{Imprivata 2016; Boone and Mulherin 2007; Gentry and Stroup 2019}`: evidence of a costly preparation stage, not that a price drew anyone in. The paper settles no specific transaction (main.md 33-39) | 1 | "Is this realistic? Which deals fit? Isn't the process usually confidential?" |
| A2 `app:evidence` | Evidence: a design, not a result | Online Appendix D pilot: reconstruct from disclosure records the timing of approaches, public visibility, buyer contacts, diligence, proposals and final selection, separating when an event occurred from when it first became public. First requirement: a publicly understood sale opportunity that stays contestable while a challenger decides. Outcome is the decision to prepare; prices must precede it; later returns can reflect anticipated arrival. Design only: no sample, effect, instrument or identification strategy (main.md 398-400) | 1 | "Can you test it? Is there evidence?" |
| A3 `app:lit` | Related work in more detail | Two lines each, "shows / here", metadata from `references.bib`: Dow, Goldstein and Guembel 2017; Edmans, Goldstein and Jiang 2012, 2015; Fishman 1988; Hirshleifer and Png 1989; Levin and Smith 1994; Roberts and Sweeting 2013; Gentry and Stroup 2019; Persico 2000; Luo 2005; Betton, Eckbo, Thompson and Thorburn 2014; Lin, Ma, Yang and Zhu 2025; Cornelli and Li 2002. Increment line: the opposition of the two returns under a sale rule, and the entry reversal (main.md 27) | 3 | "How is this different from feedback-effect models or auction-entry models?" |
| A4 `app:omit` | What the model leaves out, and why | Native two-row table. **In the model:** neither bidder trades; the investor has no initial position, cannot bid, tender or acquire, and has no control rights; the sale binds all shares (no tendering or holdout); every wrong-signed order loses against every candidate schedule, so the investor cannot profit by faking good news (C33). **Outside the model:** toeholds `\graycite{Bulow, Huang and Klemperer 1999}`; free riding `\graycite{Grossman and Hart 1980}`; announced or jump bids as signals `\graycite{Fishman 1988}` (strength here is a distribution); incumbent or target manipulation and endogenous investor research `\graycite{Goldstein and Guembel 2008}`; first-price and bargaining-with-trading equilibria. No statement on the direction of a toehold effect: the paper does not solve it | 4 | "Wouldn't the incumbent manipulate the price, buy a toehold, or trade on its own value?" |
| A5 `app:info` | Complementary, not superior, information | The challenger knows its own integration plans; a specialist investor may know the target's customers, technology and product demand: different facts about the same acquisition match (main.md 17, 37). Preparation (diligence) is what reveals the exact value to the challenger (main.md 35, 330). The benchmark's perfectly informed investor and uninformed challenger make the mechanism visible; Section 5.3 removes both extremes. The reversal holds with challenger accuracy d = 0.75 above investor accuracy a = 0.70 (Prop. A.7, analytical). Forward button [The signal economy → A6] | 4 | "Why would an investor know the challenger's value when the challenger does not?" |
| A6 `app:signals` | The price helps a challenger with its own signal | Investor signal T (accuracy a), challenger signal Y (accuracy d); the challenger uses Pr(H ∣ P, Y = y) (F44); entry is state dependent (e_H, e_L) but the price still reveals the market posterior. Declared example a = 0.70, d = 0.75: 0.850 → 0.879 (analytical, Prop. A.7). Native summary table from `tables/table_signal_grid.tex`: 6 cells meeting the condition, rise 2.81-3.09 pp (analytical); 9 cells with d ≤ 0.75, unchanged; 10 cells with d ≥ 0.76, fall 4.03-4.49 pp, because the challenger's own good signal already triggers expensive entry against the weak incumbent (numerical diagnostic). Other inputs: ρ = 0.85, c_H = 7.14, k = 0.015, r = 1.1 vs 2.3 (`signal_rho`, `signal_c_high`, `signal_k`, `signal_r_weak`, `signal_r_strong`). Q&A line: the price matters when the challenger's own signal is informative but not decisive | A5 | "What if the challenger knows more than the investor?" |
| A7 `app:eq` | Equilibrium and the two comparisons | Definition (main.md 89): order distributions σ_H, σ_L (mixing allowed; any deviation q ∈ [-1, 1]); a rational price that anticipates entry; Bayesian beliefs from the price; optimal entry; truthful bids. Order flow X = q + Z, Laplace noise with scale b; stock price P(X) = expected target payoff given X (labeled; F31). Two comparisons kept apart: a unilateral deviation is evaluated against fixed price and entry schedules; a cross-economy comparison re-solves them. Uniqueness refers to trading and on-path entry under truthful bidding | 4 | "What is the equilibrium concept? How are deviations evaluated? What exactly is unique?" |
| A8 `app:payoffs` | Acquisition payoffs in closed form | One aligned display (eqs. 4-5): t_0 = p(1 − p/r); t_H = r/2 + p²/(2r); t_L = ℓ − (ℓ² − p²)/(2r); g_H = h − r/2 − p²/(2r); g_L = (ℓ² − p²)/(2r); Δ_T = (r − ℓ)²/(2r). Native table of Table 1 at r0 and r1 (7 rows, printed values; row relabeled "target-payoff spread", F36). Gray line: Prop. 1 for any F on [0, r̄], ℓ < r̄ < h; strict when the change in F has positive integral (main.md 125-137) | 5 | "Where do the curves come from? Is this a uniform-distribution artifact?" |
| A9 `app:payrule` | The payment rule decides the sign of the spread effect | X4 (panel (a) rebuilt). Zero-reserve verifiable-value institution, Nash weight η; in words: "seller gets t_η = (1 − η)·runner-up value + η·winner value" (F06). F49 text: "Stronger incumbent: challenger profit falls weakly for every η. Spread Δ_η = η(h − ℓ) + (1 − 2η)𝔼[(R − ℓ)_+] rises (weakly) if η < 1/2, falls (weakly) if η > 1/2" (Prop. A.8, analytical). Scope: payment stage only; an entry reversal under bargaining is not solved; first-price equilibria are not solved | 5 | "Why a second-price auction? What about negotiation or first-price bids?" |
| A10 `app:bound` | Why trading is unique: a global bound | Weak: gross advantage per unit ≤ Δ_T(r0) < k, so every nonzero order loses and the posterior stays at 1/2. Strong: U_θ(s) = sΠ_θ(s) − ks with Π_θ(s) the expected residual per unit at order size s; U_θ′(s) ≥ (1 − 1/b)ρ m Δ_T(r1) − k > 0 on [0, 1]. Holds against every candidate price and entry schedule, including mixed orders: global, not first-order (main.md 235-237, 487-535). **Investor manipulation (in-model):** both residual advantages in eq. 11 are positive under every candidate order distribution, so a wrong-signed order, such as a low-value investor buying to fake good news and trigger entry, has negative gross payoff and still pays k (main.md 197-209, 535). Incumbent or target manipulation and toeholds: outside the model (A4) | 7 | "Did you assume the informative profile? Mixed strategies? Large deviations? Is this manipulation?" |
| A11 `app:orders` | Orders, units and the trading cost | q ∈ [−1, 1] is a normalized small trading unit, not ownership of the target, measured in the same units as the noise (scale b); the investor has no initial position (main.md 64). k is an execution or position-carrying friction, distinct from adverse-selection price impact, which competitive pricing already generates (main.md 64). Why a corner, unlike Kyle: per-unit advantage is bounded below by ρ m Δ_T because beliefs stay in [m, M], and one more unit erodes it by at most a fraction 1/b (the haircut), so marginal profit stays above k over the whole interval and full orders are the unique best response (A10). Against the weak incumbent the same bounds make every order lose | 7 | "Why bounded orders and a corner solution, unlike Kyle? What is k? Where does (1 − 1/b) come from?" |
| A12 `app:notation` | Notation | Native two-column table of every main-line symbol from section 6.1 with its gloss, in introduction order (`\small` allowed on this backup only) | 7 | "What was m / B_r / Δ_T again?" |
| A13 `app:suff` | The challenger can read the market's belief off the price | Display 1: μ_X(x) = Pr(H ∣ X = x) ∈ [m, M] under any mixed orders (bounded Laplace likelihood ratio e^{±2/b}). Display 2 (words): price = t_0 + (entry probability at that price) × (t_L − t_0 + Δ_T μ). The price is strictly increasing in μ because entry ≥ ρ > 0 and Δ_T > 0. Atoms and entry jumps allowed; no differentiability needed (Props. A.1-A.2, analytical; main.md 150-195). The price is a sufficient statistic for the market's belief | 8 | "The challenger sees the price, not the flow; can it invert it? What about price atoms?" |
| A14 `app:laplace` | Why Laplace noise, and what logistic noise changes | X3 (reuse). Both laws satisfy abs(f′) ≤ f/b, so the global trading bounds hold for both. Laplace: the posterior reaches [m, M] at finite flow (plateau). Logistic: bounds reached only as flow → ∞; threshold x* ≈ 5.42, about 1.5 noise s.d. from the center (`logistic_flow_threshold`, `logistic_threshold_noise_sd`; F38); entry 0.302 vs 0.523 (`logistic_entry_strong`, `base_entry_strong`); atomless costs (ε_C = 0.1): 0.523 and 0.301 (`cost_mix_laplace_entry_strong`, `cost_mix_logistic_entry_strong`). Common scale b, not common variance; not a Blackwell ranking (Props. A.5-A.6) | 8 | "Is Laplace noise doing the work? The plateau looks special." |
| A15 `app:floor` | Why the model needs a low-cost floor | Without entry after every price, target proceeds do not depend on quality, so no informative trading is consistent: nobody prepares and there is nothing to trade on. The floor is part of the mechanism, not a numerical regularizer (main.md 235). It gives the lower bound ρ m Δ_T on the residual advantage. Theorem margin 1.37 (`base_margin_low_cost`). The floor alone gives entry 0.250 at both strengths when the price is hidden (frame 11). Atomless cost supports keep it (Prop. A.6) | 8 | "Isn't the cheap-type floor doing all the work? Why ρ > 0?" |
| A16 `app:proof` | Proof logic in four steps | (1) Weak economy: no order covers k; no trade; entry ρ. (2) Strong economy: the global bound (A10) forces full orders. (3) Under full orders the high-cost window puts the belief threshold inside (1/2, M), so good news crosses it with positive probability; α_H > α_L tilts extra entry to high values. (4) Blackwell: a constant kernel maps the strong experiment to the weak one; no state-independent kernel maps the constant experiment to the strong one. Part (iii): with the floor and profitable trading still in place at r2, B_{r2}(M) < c_H removes expensive entry. What does the work: step 2 (main.md 233-253, 535-550) | 9 | "What does the work in the proof? Is the strong price really more informative?" |
| A17 `app:margins` | Conditions are jointly satisfiable for every h > ℓ | Native table labeled "theorem margins at the benchmark" (Table 2 note; F44): low-cost floor 1.37 (`base_margin_low_cost`); high-cost window 1.20 at the weak prior (`base_margin_high_prior`) and 0.217 at the best strong price (`base_margin_high_ceiling`); trading-cost window 0.00333 (`base_margin_weak_trade`) and 0.00241 (`base_margin_strong_trade`); minimum 0.00241 (`base_minimum_theorem_margin`). Nonemptiness for every h > ℓ comes from a construction: take r0 < r1 close to ℓ, then k, c_H, c_L strictly inside their windows (main.md 404, 767; Sec. 5.2). It is a mathematical construction, not slack at the benchmark and not an effect-size claim. Moderate values h = 2: minimum margin 8.01e-4 (`moderate_minimum_theorem_margin`). Part (iii) not claimed for every h > ℓ (F46) | 9 | "Is this a knife edge? How big is the set? Does it need h = 10ℓ?" |
| A18 `app:forces` | Two forces from one payment rule | T8 native table (header "Information" in `cInfo`; the former main frame): What a stronger incumbent moves: challenger profit B_r(μ) ↓ at every belief / target-payoff spread Δ_T ↑. Who responds: the challenger, at a given belief / the investor, then the price, then the challenger's belief. What it needs: nothing / entry after any price (`cCost` low-cost floor), price seen before entry. Effect on entry: **weakly ↓** (Prop. A.3) / ↑ once trading pays and good news clears c_H. Chain line beneath (D2) | 9 | "Which force wins, and when?" |
| A19 `app:scale` | Benchmark scale: declared, not calibrated | Native two-column table, benchmark vs moderate economy: h 10 / 2; ℓ 1 / 1; p 0.5 / 0.5; ρ 0.25 / 0.25; c_L 1 / 0.3; c_H 6 / 0.89; b 2 / 2; k 0.02 / 0.002; strengths 1.2 → 3 / 1.05 → 1.5; entry 0.250 → 0.523 / 0.250 → 0.527; minimum theorem margin 0.00241 / 8.01e-4 (`base_*`, `moderate_h`, `moderate_ell`, `moderate_p`, `moderate_rho`, `moderate_c_low`, `moderate_c_high`, `moderate_b`, `moderate_k`, `moderate_r_weak`, `moderate_r_strong`, `moderate_entry_weak`, `moderate_entry_strong`, `moderate_minimum_theorem_margin`). Gray: units are arbitrary; magnitudes are not calibrated; the signs are the theorem; nonemptiness holds for every h > ℓ (A17) | 10b | "c_H is several times the target's proceeds and the challenger keeps most of h; is that realistic? Are the magnitudes calibrated?" |
| A20 `app:entry` | How entry and ownership are computed | Display 1: τ = (c_H − g_L)/(g_H − g_L) (c_H underbraced "expensive cost"; τ = "belief threshold for costly preparation"), x* = (b/2) log(τ/(1 − τ)). Display 2: e_H = ρ + (1 − ρ)α_H, e_L = ρ + (1 − ρ)α_L, entry 𝖤 = (e_H + e_L)/2, high-value ownership 𝖮_H = e_H/2, with α_θ = Pr(X ≥ x* ∣ θ) ("probability that order flow crosses the entry threshold"). The high-cost window puts τ ∈ (1/2, M) and x* ∈ (0, 1); α_H > α_L. Above the ceiling strength r_C ≈ 3.59 (`base_r_high_cost_ceiling`), τ > M; the left-limit entry at r_C is 0.506 (`base_laplace_entry_ceiling_left_limit`). Expected target proceeds 0.393 / 0.872 / 0.664 at r0 / r1 / r2 (Table 2 Panel A) | 10b | "Why does high-value ownership rise? Why exactly does entry fall at r2? Where is the ceiling?" |
| A21 `app:cert` | Which equilibrium? What the proof certifies | Opening line: the reversal (frames 9-10) compares economies in which trading and on-path entry are unique, so no selection is needed; multiplicity arises only between them (frame 12). Native table of registry enclosures exactly as displayed: q_L ∈ [−0.46031620, −0.46031618], [−0.70747539, −0.70747537], [−0.90333201, −0.90333198]; entry 𝖤 ∈ [0.5450528898, 0.5450528922], [0.5487563062, 0.5487563085], [0.5513607988, 0.5513608020]. Low type: global strict concavity, and a sign change of its marginal profit at its own order brackets the root (`cert_*_psi_left_lower`, `cert_*_psi_right_upper`, e.g. 0.000000000114 and −0.000000000096 at r = 1.55). High type: cover margin strictly positive over the whole bracket, 0.0000761777, 0.0027531948, 0.0054921767 (`cert_*_high_derivative_lower`). Not proved: uniqueness of the informative profile, absence of mixed equilibria, a branch between nodes | 10b | "Which equilibrium do you select? Are these real equilibria or numerical artifacts?" |
| A22 `app:controls` | Information controls in detail | Prop. A.3 in words: at any fixed information experiment and cost law, entry is weakly decreasing in strength (analytical). It applies within fixed orders, not across order profiles that change with r. The frozen weak profile is a control, not an equilibrium: full orders lose money there because Δ_T(r0) < k. At r1 it coincides with the equilibrium. Price hidden: the challenger uses the prior and enters only at low cost, which the high-cost window implies at both strengths; at r1 the investor still trades full orders. Native table of Table 2 Panels A-B: 𝖤, 𝖮_H, expected target proceeds, status (printed values; F08 labels) | 11 | "Is the frozen control a fair counterfactual? Why is it not an equilibrium? Isn't the hidden-price row true by construction?" |
| A23 `app:welfare` | Price level or information? | F10 text: "Invariance diagnostic: add a dividend D_0 = 0.257809 (the revenue gain from price access) to the traded claim in the price-hidden economy. Mean prices then match, but entry does not, so the information matters, not the price level." Tag "diagnostic" (`base_matched_dividend`); the revenue gain itself is analytical (`base_revenue_gain`). Prop. A.9 at r1: each extra entry is chosen only when expected gross profit covers its cost; the allocation gain includes that profit and sales that would otherwise fail the reserve; transfers excluded. Not a sale mechanism; excluded from surplus; no ranking of strengths or mechanisms | 11 | "Isn't this just a higher price level? Is more entry efficient?" |
| A24 `app:corr` | Trading and entry across strengths: entry | X5 panel (a). Annotations by meaning (F41, F52): no trade unique for r < r_P ≈ 1.22 (`base_r_pool_unique_sufficient`); no trade an equilibrium up to r_N ≈ 1.75 (`base_r_no_trade_exact`); full orders unique above r_U ≈ 2.84 (`base_r_full_unique_sufficient`); expensive entry impossible above r_C ≈ 3.59 (`base_r_high_cost_ceiling`). Legends visible: black points computer-assisted, "enclosures narrower than the marker; exact intervals in A21"; curves numerical diagnostic, broken at unresolved nodes; "multiplicity found; search not exhaustive"; correspondence open. Forward button [Order sizes → A25] | 12 | "What does the whole correspondence look like? Is entry monotone?" |
| A25 `app:corrb` | Trading and entry across strengths: orders | X5 panel (b): order size abs(q_L) vs r, asymmetric (1, q_L), symmetric interior, mixed candidate at the no-trade boundary (numerical diagnostic), q = 0, full orders. Same enclosure legend note | A24 | "Which orders sit behind each branch?" |
| A26 `app:robust` | Robustness in full | Table 3 rebuilt natively: 𝖤 weak / strong / change (pp) / 𝖮_H weak / strong for six rows (Laplace atoms, Laplace mixture, logistic atoms, logistic mixture, moderate values, signals; printed values), each row with its declared ρ and strengths (Table 3 note: distinct parameter vectors, not one joint calibration). Minimum theorem margins: base 2.41e-3, moderate 8.01e-4, signals 1.45e-3 (`base_minimum_theorem_margin`, `moderate_minimum_theorem_margin`, `signal_minimum_theorem_margin`). Note (F47): the r2 fall is shown for the benchmark only | 13 | "Are these the same parameters? How close to the boundary is each row?" |
| A27 `app:reserve` | A higher reserve can raise proceeds; optimal terms are open | Native Table 4 Panel B, labeled "Value classes: p = 0.5 vs p = 1.1" (ε_V = 0.05, `value_band_halfwidth`; F39). Columns: preparation, sale, two admissible bidders, expected proceeds, trading (printed values). Weak proceeds 0.393 → 0.432; strong 0.872 → 1.01; preparation at p = 1.1: 0.540 (weak), 0.512 (strong) (`value_*`). Gray line: "Binary values: p = 0.5 vs p = 1.01." Say aloud: 1.1 sits just above ℓ = 1, so it excludes the low-value challenger. Preparation, sale and two admissible bidders come apart. A feasible improvement, not an optimal reserve. Forward button [Same orders, different prices → A28] | 14 | "What should the seller do? Is there an optimal reserve? Should sellers keep processes public?" |
| A28 `app:pool` | Same orders, different prices | Prop. A.10 (analytical existence; F32): at reserve p = 7 (`pool_reserve`) and r0, the same full orders support price pools below a cutoff κ ∈ [−log 2, 0] (F03). Pooled belief 0.273 vs 0.303, entry 0.152 vs 0.125, proceeds 0.687 vs 0.610 (`pool_posterior_cutoff_low/high`, `pool_entry_cutoff_low/high`, `pool_revenue_cutoff_low/high`). "Same orders, different prices, beliefs, and entry": a continuation must include the price rule. Does not arise on the benchmark support | A27 | "Why can't you just solve the seller's problem? Is the price rule unique given orders?" |
| A29 `app:refs` | References | `\small` list, metadata from `references.bib`: Fishman (1988, RAND J. Econ.); Hirshleifer and Png (1989, RFS); Dow, Goldstein and Guembel (2017, JEEA); Edmans, Goldstein and Jiang (2015, AER); Levin and Smith (1994, AER); Roberts and Sweeting (2013, AER); Gentry and Stroup (2019, JFE); Goldstein and Guembel (2008, REStud); Bulow, Huang and Klemperer (1999, JPE); Grossman and Hart (1980, Bell J. Econ.); Boone and Mulherin (2007, JF); Imprivata (2016, DEFM14A); plus the A3 works as verified. Kyle and Vila (1991) and Schwert (1996) are not listed unless the author first adds them to the paper and the bib | 3 | Citation lookup |

## 10. Timing table

| Frame | Title (short) | Minutes | Start | End (cumulative) |
|---|---|---|---|---|
| 0 | Title | 0.25 | 0.00 | 0.25 |
| 1 | Does a stronger incumbent keep the challenger out? (D0) | 2.00 | 0.25 | 2.25 |
| 2 | This paper (**punchline**) | 2.00 | 2.25 | 4.25 |
| 3 | What is new | 0.75 | 4.25 | 5.00 |
| 4 | Model: who moves, who knows what (D1) | 2.75 | 5.00 | 7.75 |
| 5 | One auction, two claims | 2.50 | 7.75 | 10.25 |
| 6 | Spread up, profit down (X1) | 1.50 | 10.25 | 11.75 |
| 7 | Trading pays only against a strong incumbent | 3.00 | 11.75 | 14.75 |
| 8 | Only good news pays for expensive preparation (X2) | 2.25 | 14.75 | 17.00 |
| 9 | Proposition 2 | 2.50 | 17.00 | 19.50 |
| 10a | Benchmark rise | 1.50 | 19.50 | 21.00 |
| 10b | Benchmark fall | 1.00 | 21.00 | 22.00 |
| 11 | Freeze the information | 2.25 | 22.00 | 24.25 |
| 12 | Equilibria coexist | 1.50 | 24.25 | 25.75 |
| 13 | Robustness | 1.50 | 25.75 | 27.25 |
| 14 | Price access and welfare | 1.00 | 27.25 | 28.25 |
| 15 | What a test would measure | 1.00 | 28.25 | 29.25 |
| 16 | Conclusion | 1.00 | 29.25 | 30.25 |
| | Question reserve | 9.75 | 30.25 | 40.00 |

- **Punchline:** frame 2 opens at 2.25 min. The headline numbers (entry 0.250 → 0.523; profit 4.80 → 4.29) are spoken by about 2.75 min, and the full punchline, with both supports and the implication, is done by 4.25 min. The model is on screen at 5.0 min and the theorem at 17.0 min.
- **Checkpoints and the cut each one triggers** (every cut is decided at a checkpoint that comes before the frame it removes):
  - Frame 3 starts by 4.75 min (planned 4.25). If later, skip frame 3 (cut 1).
  - Frame 5 starts by 9.5 min (planned 7.75; the early checkpoint, since job-market interruptions cluster on frames 1-5). If later, skip frame 6 (cut 2) and speak its two numbers on frame 5.
  - Frame 9 starts by 18.5 min (planned 17.0). If later, skip frames 12 and 14 (cuts 3 and 4).
  - Frame 11 starts by 23.5 min (planned 22.0). If later, also skip frame 15 and give frame 13 as its takeaway sentence (cuts 5 and 6).
- **Frames to skip if behind, in this order.** Each becomes one spoken sentence; the frame stays in the deck.
  1. Frame 3 (−0.75): fold its takeaway into frame 2's spoken route.
  2. Frame 6 (−1.25 net): speak "spread 0.0167 → 0.667, profit at the prior 4.80 → 4.29" on frame 5.
  3. Frame 12 (−1.25 net): the F48 sentence on 10b: "At three certified strengths between r0 and r1, an informative equilibrium coexists with no trade; the full correspondence is open."
  4. Frame 14 (−0.75 net): "At r1, seeing the price raises proceeds and surplus; a comparison of economies, not a recommendation on process design."
  5. Frame 15 (−0.75 net): "A test needs the decision to prepare as the outcome, timed against public prices; the paper gives a design, not an estimate."
  6. Frame 13 (−1.0): 30 seconds, the F47 takeaway only, with "(declared example)".

  Together these recover up to 5.75 minutes. Never cut frames 1, 2, 4, 5, 7, 8, 9, 10a/10b, 11 or 16. Every backup for a likely early or central question hangs off one of these: A1, A2 (1); A4-A7 (4); A8, A9 (5); A10-A12 (7); A13-A15 (8); A16-A18 (9); A19-A21 (10b); A22, A23 (11). Only A3, A29 (3), A24-A25 (12), A26 (13) and A27-A28 (14) hang off cuttable frames.
- **If ahead:** open A10 (global bound) from frame 7 or A24 (correspondence) from frame 12, then return.

## 11. Anticipated questions (job-market audience)

| # | Question | Where answered |
|---|---|---|
| 1 | Is this realistic? Which deals have such an interval? | A1 (from frame 1). Spoken: whether a deal fits is a question about its chronology; the paper settles it for no transaction |
| 2 | Can you test it? Is there evidence? | A2 (direct from frame 1); frame 15. Design only, no sample; returns after entry can reflect anticipated arrival |
| 3 | Isn't this just learning from prices, as in Dow-Goldstein-Guembel? | Frame 3 and A3: the sale rule splits one surplus into a traded claim and the challenger's claim, which competition moves in opposite directions; the entry reversal is the increment |
| 4 | Isn't this Kyle and Vila (1991)? What about pre-bid run-ups (Schwert 1996)? | Spoken only (frame 3 notes; C37): in Kyle-Vila the informed trader is the raider; here the investor cannot bid and the price informs a third party's entry. Run-ups follow an anticipated bid; here the price moves before the challenger decides. Neither citation goes on a slide until it is in the paper and the bib |
| 5 | Why would an investor know the challenger's value when the challenger does not? | Spoken on frame 4 (perfect information only makes the mechanism visible; Section 5.3 removes it); A5 → A6 (complementary information; reversal with d = 0.75 > a = 0.70) |
| 6 | Why can't the challenger bid without preparing, at its expected value? | Spoken, frames 1 and 4: preparation (verification, financing, approvals) is required for an executable bid; a challenger that declines stays out (main.md 35, 57) |
| 7 | Is this manipulation? Couldn't a low-value investor buy to fake good news? | Spoken on frame 7; A10: every wrong-signed order has negative gross payoff against every candidate schedule (in-model). Incumbent or target manipulation: outside the model (A4) |
| 8 | Wouldn't the incumbent buy a toehold, trade on its own value, or tender? | A4 (in-model vs out-of-model rows). Spoken: neither bidder trades in the model; the investor knows θ, not R; the paper does not solve toeholds, so I do not guess their direction |
| 9 | Is strength a signal the incumbent chooses? | A1 + spoken: strength is the public distribution of its value, not an announced bid; announced or jump bids are outside the paper (A4) |
| 10 | What is the equilibrium concept? What exactly is unique? | A7 |
| 11 | Why a second-price auction? What about negotiation or first-price bids? | Spoken on frame 5 (an open ascending contest ends at the runner-up's value; a losing low-value challenger sets the incumbent's price); A9: under bargaining the spread effect holds only weakly and flips sign at η = 1/2; no entry reversal claimed there. First-price not solved |
| 12 | Is this a uniform-distribution artifact? | A8 (Prop. 1 for any F on [0, r̄]) |
| 13 | Why bounded orders and a corner, unlike Kyle? What is k? What is (1 − 1/b)? | Frame 7 gloss; A11 (normalized unit, not ownership; k is a friction separate from price impact; corner from the global bound) |
| 14 | What if k is near zero? | Spoken from frame 7: the result needs k inside the trading-cost window; below Δ_T(r0) trading would pay even against the weak incumbent, and Prop. 2 is silent. Margins in A17 |
| 15 | Did you assume the informative profile? Mixed strategies? Large deviations? | A10 |
| 16 | The challenger sees the price, not the flow; can it really infer the belief? Price atoms? | A13 |
| 17 | What if the challenger could see order flow? | Spoken from A13: the price is a sufficient statistic for the market's belief, so price and flow carry the same belief information here (Props. A.1-A.2) |
| 18 | Is Laplace noise doing the work? | A14: same trading bounds under logistic noise; same sign, smaller size (0.302). Also raised by the speaker on frame 13 |
| 19 | Isn't the cheap-type floor doing all the work? | A15 (from frame 8). Spoken: the floor alone gives entry 0.250 at both strengths when the price is hidden (frame 11) |
| 20 | What does the work in the proof? Is the strong price really more informative? | A16 (global bound; strict Blackwell dominance) |
| 21 | Is it a knife edge? Does it need h = 10ℓ? | A17 (jointly satisfiable for every h > ℓ by construction; benchmark margins); A19 (moderate values h = 2 give 0.250 → 0.527) |
| 22 | Which force wins, and when? | A18 (from frame 9) |
| 23 | Are the magnitudes calibrated? c_H = 6 against target proceeds below 1, and the challenger keeps g_H = 8.46 of h = 10? +27 pp seems large | A19 (from 10b). Spoken: no. Units are arbitrary and the benchmark is declared to show the conditions are jointly satisfiable and to scale the effect; the signs are the theorem; nonemptiness holds for every h > ℓ; the moderate economy (h = 2, c_H = 0.89, k = 0.002) gives 0.250 → 0.527 |
| 24 | Why does high-value ownership rise, not just entry? | A20 (α_H > α_L) |
| 25 | Why does entry fall again at r2? Is it a knife edge next to the ceiling? | Frame 10b (spoken: any such strength works; 3.6 is the declared node); A20 (above r_C the belief threshold exceeds M) |
| 26 | Does the r2 fall survive the extensions? | Spoken: it is shown at the benchmark and nearby parameters and is not claimed under the extensions (F47); the extensions establish the r0 → r1 rise (A26) |
| 27 | Which equilibrium do you select? Are these real equilibria? | Spoken on 10b (the reversal compares economies where trading is unique; no selection needed); A21 (certificates) |
| 28 | Your frozen profile isn't an equilibrium; why is it the right control? And isn't the hidden-price row true by construction? | Frame 11 annotation; A22. Spoken: the frozen profile holds the experiment fixed to isolate deterrence; its numbers are a numerical diagnostic and its sign is a theorem (Prop. A.3). The hidden row is implied by the high-cost window; it shows only that without the price the rise disappears |
| 29 | Why must the price come before preparation? | Frame 4 + spoken: otherwise there is nothing to learn; hiding the price leaves only the entry floor (frame 11) |
| 30 | Isn't it the price level rather than information? | A23 (from frame 11; matched-dividend diagnostic) |
| 31 | What happens between r0 and r1? | Frame 12, A24-A25. Spoken: I report every branch I can certify and read no monotone path into the gaps |
| 32 | Why would a bidder learn from the market if it has its own signal? | Frame 13 row 5 and the spoken F16 line; A6 (holds with d = 0.75 > a = 0.70 where the conditions hold; falls when d ≥ 0.76) |
| 33 | Is more entry good? Should a seller want a strong incumbent or a public process? | Frame 14 (spoken guard), A23: at r1 price access raises proceeds and surplus; the paper does not rank strengths or mechanisms |
| 34 | What is the optimal reserve? What should sellers do? | A27-A28: a higher reserve can help at listed nodes; optimal terms are open because continuations must include price rules; spoken on frame 16 as the next theorem |

## 12. Critique log

Line references in the critique were checked against `paper/main_filled.md` (same numbering as main.md). Corrections: complementary information is at main.md 17 and 37 (not 19), preparation at 35, the Imprivata chronology at 39 (not 37), the wrong-signed-order result at 197-209 (eq. 11) and 535.

| # | Point | Decision | One-line reason |
|---|---|---|---|
| 1 | Trading frame before the price frame; define m, M on the trading frame; keep the "price that moves" hook on the profit-thresholds frame | accepted | The chain is now shown in the order it runs (frames 7 → 8), so X2's weak-incumbent best-price curve cannot be misread as "the weak incumbent is better" |
| 2 | Backup for "why would an investor know θ?" from the model frame; chain A20 from it; spoken clause on the model frame | accepted | A5 (from frame 4) → A6 (the signal economy) answers a likely minute-6 question from never-cut ground; sources corrected to main.md 17, 35, 37, 330 and Prop. A.7 |
| 3 | Answer "is this manipulation?" in-model | accepted | Eq. 11 makes every wrong-signed order lose against every candidate schedule (main.md 197-209, 535); added to A10 and A4's in-model row, and spoken on frame 7 |
| 4 | Price-hidden control is implied by the high-cost window; "weakly lowers" | accepted | Frame 2 now keeps only the fixed-information claim in words; frame 11 annotates the hidden row as implied by the window and says "weakly lowers"; A18 writes "weakly ↓" (Prop. A.3 is weak) |
| 5 | Frame 2 headline only; move ownership and control numbers | accepted | Frame 2 carries four analytical numbers and the channel in words (no diagnostic number, F50); ownership moves to 10a and frozen numbers to 11. Budgeted 2.0 min rather than 1.75, to keep the spoken route |
| 6 | Take frames 7 (X1) and 10 (synthesis) off the main line; early checkpoint | accepted in part | Synthesis → A18 and the early checkpoint (frame 5 by 9.5 min) are adopted, and every cut is now triggered by a checkpoint before it. X1 stays as the first pre-theorem cut, because removing it as well would drop speech to about 28 min, below the fixed 30-32 min band |
| 7 | Re-home likely-question backups to never-cut frames | accepted | A2 direct from frame 1; floor (A15) from frame 8; certificates and selection (A21) from 10b, with the spoken no-selection line; signals (A6) via A5 from frame 4 |
| 8 | Prop. 2 (iii) omits two of its three conditions | accepted | (iii) now reads "where the low-cost floor and profitable trading persist but B_{r2}(M) < c_H" (main.md 233) |
| 9 | r2 = 3.6 sits next to r_C ≈ 3.59 | accepted | X2 shows r_C only as the curve crossing, with the r2 label on the far side; r_C is off the main line; the spoken line on 10b follows F46 |
| 10 | Benchmark scale will be attacked; 10a subtitle lists 8 inputs | accepted | 10a subtitle is now "declared benchmark; units arbitrary (inputs in backup)"; new A19 (from 10b, where the numbers stay on screen) sets benchmark and moderate inputs side by side; Q23 prepared from registry and Table 1 values |
| 11 | Gloss (1 − 1/b); Kyle-style questions on orders and k | accepted | Gloss added on frame 7, in a corrected form that matches the proof (it bounds how fast one more unit erodes the per-unit advantage, from abs(f′) ≤ f/b); A11 covers the normalized unit, k as a separate friction, and the corner |
| 12 | Kyle and Vila (1991), Schwert (1996) | accepted | Spoken contrasts prepared on frame 3 and in Q4; kept off slides and references because neither is in the paper or the bib (source-integrity rule) |
| 13 | "Sale terms" implication outruns the main-line evidence | accepted | Frames 2 and 16 use the strength-based implication; sale terms become the spoken open question on frame 16 (C29, C36) |
| 14 | Merge the model and timeline frames; agent-labelled boxes; optional opener timeline | accepted | Frame 4 is now D1 with agents plus a two-item legend (−1.0 min against the old 3.75); the equilibrium bullet moves to A7; D0 gives frame 1 a picture. C is kept in the legend because F30 and F55 require it on the model slide |
| 15 | Shrink main-line notation | accepted in part | Dropped q alone, 𝖤 and 𝖮_H (words), a and d (words) and r_C (words). Kept t_H, t_L because F04 and F36 require "Δ_T = t_H − t_L"; kept m ≈ 0.27 (F42) and removed the second rounding by writing the 0.0224 arithmetic with m symbolic, checked as k + margin |
| 16 | Robustness table invites cross-row comparison | accepted | pp column dropped; "rows differ in ρ and strengths" note and "(declared example)" added; the F16 line is spoken and the speaker raises the logistic question. The F16 footnote stays on the slide because the audit requires it |
| 17 | A14 title overstates "slack" | accepted | Retitled "Conditions are jointly satisfiable for every h > ℓ" (A17); table labelled "theorem margins at the benchmark"; nonemptiness attributed to the near-ℓ construction |
| 18 | Demote the coexistence frame to a backup | rejected (legend fix accepted) | Demoting it would push speech below the fixed 30-min floor. It stays as the first post-theorem cut, with F48 wording and a one-sentence fallback. The X5 legend now says enclosures are narrower than the marker; the critique's "< 1e-8" was dropped because the q_L enclosures are about 2e-8 to 3e-8 wide |
| 19 | Theorem frame repeats the mechanism frames | accepted | Conditions are shown as names and inequalities only; the takeaway is the chain line, which replaces the synthesis frame; 2.5 min (down from 3.0) |
| 20 | Prepare "why a second-price auction?" | accepted | Spoken answer on frame 5, then A9 for payment-rule dependence ("weakly", F49) and "first-price not solved" (C27). The Fishman and BHK attribution is left out because the paper states no such equivalence |
| 21 | Split A4 into in-model and out-of-model rows | accepted | A4 is now a two-row native table; no statement on toehold direction, which the paper does not solve |
| 22 | Concrete opener fact | accepted | Frame 1 carries the Imprivata chronology as one gray line, framed as a costly preparation stage and not a price drawing a buyer in (main.md 39) |
| 23 | PowerPoint rebuild risks | accepted | X2 cost lines drawn inside the picture; frame 7's underbraced display replaced by a native one-row, three-cell table with the bound beneath; X5 fallback relabels specified as native shapes |
| 24 | Welfare frame value unclear; A22 should be reachable from a never-cut frame | accepted | Frame 14 is the second post-theorem cut and carries the spoken guard; "price level or information?" (A23) now hangs off frame 11 |

**Timing note.** Accepting points 5, 6 (synthesis), 14 and 19 removes about 3.25 minutes. The spoken material added under points 2, 3, 9, 11, 16 and 20 adds about 1.75 minutes on frames 5, 7, 10a/10b, 11 and 13. Taking X1 and coexistence off as well would leave about 26-27 minutes, below the fixed band. To stay inside the fixed 30-32 minute band without restoring cut material, the plan keeps X1 (point 6, in part) and coexistence (point 18). It also adds frame 15, "What an empirical test would have to measure", 1.0 min from main.md 398-400 (Section 7), which gives this finance audience the design question on the main line and is itself cuttable. Planned speech is 30.25 minutes with a 9.75-minute reserve.
