# Slide inventory: Beamer deck to HTML deck

Source deck: `overleaf/talk/talk.tex` (47 frames: F0 to F16 with F10a and F10b, then A1 to A29).
Inventory built from the `\hypertarget{main:...}` and `\hypertarget{app:...}` markers, not from `label=`.
Speaker notes: `overleaf/talk/script.tex`. Organisation: `talk/structure-plan.md`, sections 1 to 11.

## How to read the "Plan" column

The structure plan has no slide sections of its own. Its sections 1 to 11 are plan chapters.
The "Plan" column therefore gives the chapter and row that governs each frame:

- `§8 Fn` is the frame-by-frame plan for main frames; `§9 An` for backups.
- `§10` gives the planned minutes and the cut rank (never cut, or cut 1 to 6).
- `§11 Qn` lists the anticipated questions the frame answers.

The "Part" column is my proposal for the progress rail of the HTML deck. It groups the main
frames into eight parts in the order of the talk. It adds no slide and moves no slide.

| Part | Name | Frames |
|---|---|---|
| 1 | Question | F1, F2, F3 |
| 2 | Model | F4 |
| 3 | Two claims | F5, F6 |
| 4 | Price | F7, F8 |
| 5 | Theorem | F9 |
| 6 | Numbers | F10, F11 |
| 7 | Boundaries | F12, F13, F14 |
| 8 | Close | F15, F16 |
| B | Backups | A1 to A29, grouped by origin frame |

Rules kept from the Beamer deck:

- Nothing is dropped. Every frame becomes one web slide with the same title and the same number.
- F10a and F10b share the displayed number 10, as in the PDF (`noframenumbering`). On the web they
  are one slide id `f10` with one build step. The overview lists both states. The author can
  instead keep two physical slides; the engine supports both.
- Every backup keeps one origin and one Back control. A5 to A6, A24 to A25 and A27 to A28 keep
  their forward links. Escape also returns to the origin.
- Every number keeps its `% source:` key as a `data-q` attribute. The slide shows the string the
  Beamer deck shows (3 significant digits; enclosures exactly as the registry displays them).
- Status words stay as printed: analytical, computer-assisted, numerical diagnostic, open; inputs
  carry `input`.
- Colour: `cInfo` #AA4B00 for the target-payoff spread and the information chain; `cCost` #006F50
  for preparation costs and the floor and window labels. UCL purple is chrome only.

## Main frames

| Frame | Web id | Title (as in talk.tex) | Plan | Part | Sources (registry keys, tables, figures) | Proposed interaction | Notes source | Links |
|---|---|---|---|---|---|---|---|---|
| F0 | `f0` | Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders | §8 F0; §10 0.25 min | 1 | none | Full-bleed title. Keyboard hint fades after 4 s. Theme and font controls live here. | script.tex "Opening" | none |
| F1 | `f1` | Does a stronger incumbent keep the challenger out? | §8 F1; §10 2.00 min, never cut; §11 Q1, Q2, Q6, Q9 | 1 | Imprivata chronology (main.tex §1.1; no number) | D0 three-box timeline builds box by box (3 reveals), then the four bullets, then the twist line. | script.tex block 1 | to A1, A2 |
| F2 | `f2` | This paper | §8 F2; §10 2.00 min, never cut | 1 | `base_entry_weak`, `base_entry_strong`, `base_profit_prior_weak`, `base_profit_prior_strong` | Three claims reveal in order. The four numbers appear with the first claim and carry a hover tooltip (key, status, exact value). No counter animation on a punchline. | block 2 | none |
| F3 | `f3` | What is new relative to learning from prices | §8 F3; §10 0.75 min, cut 1; §11 Q3, Q4 | 1 | citations only | Three rows reveal. | block 3 | to A3, A29 |
| F4 | `f4` | Model: who moves, who knows what, and when | §8 F4; §10 2.75 min, never cut; §11 Q5, Q6, Q8, Q10, Q29 | 2 | inputs shown as symbols only (values in A19) | D1 five-box timeline. Focus or hover on a box shows its information set (main.tex §2.2): what that agent sees and does not see. Boxes are buttons, so the keyboard reaches them. | block 4 | to A4, A5, A7 |
| F5 | `f5` | One auction, two claims, opposite responses | §8 F5; §10 2.50 min, never cut; §11 Q11, Q12 | 3 | none numeric (Proposition 1) | T1 table. A two-state toggle "R ≤ ℓ / R > ℓ" highlights the row and the gap cell. Then the two-line display reveals with its arrows. | block 5 | to A8, A9 |
| F6 | `f6` | A stronger incumbent: spread up, profit down | §8 F6; §10 1.50 min, cut 2 | 3 | `figures_data/two_returns.csv` (fig1: r, Δ_T, B at 1/2); `base_r_weak`, `base_r_strong`, `base_spread_weak`, `base_spread_strong`, `base_profit_prior_weak`, `base_profit_prior_strong`; X1 `talk/figures/two_returns_talk.svg` | SVG rebuilt from the CSV, two panels (a) and (b). Hover or arrow keys move a cursor; the readout shows the CSV value at that r and says "figure data". The two marked strengths show registry values. | block 6 | none |
| F7 | `f7` | Trading pays only against a strong incumbent | §8 F7; §10 3.00 min, never cut; §11 Q7, Q13, Q14, Q15 | 4 | `base_m`, `base_M`, `base_b`, `base_rho`, `base_spread_weak`, `base_k`, `base_spread_strong`, `base_margin_strong_trade` (0.0224 = k + margin) | The three-factor table builds one factor at a time. Then the weak and strong bullets reveal. The gray arithmetic line toggles. | block 7 | to A10, A11, A12 |
| F8 | `f8` | Only good news makes expensive preparation pay | §8 F8; §10 2.25 min, never cut; §11 Q16 to Q19 | 4 | fig1 B at m, 1/2, M (`two_returns.csv`); `base_c_low`, `base_c_high`, `base_rho`, `base_profit_prior_weak`, `base_r_weak`, `base_r_strong`, `base_r_collapse`; X2 `profit_thresholds_talk.svg` | SVG rebuilt from the CSV with the cost lines inside the picture. A slider on r moves a marker; the readout gives B_r(m), B_r(1/2), B_r(M) and the three condition margins by closed form, labelled "fixed-order calculation, not an equilibrium solver". Reveal 1: the floor. Reveal 2: the window. | block 8 | to A13, A14, A15 |
| F9 | `f9` | Proposition 2: a stronger incumbent can raise entry | §8 F9; §10 2.50 min, never cut; §11 Q20, Q21, Q22 | 5 | none numeric | Parts (i), (ii), (iii) reveal inside the result box. Then the three named conditions. Then the chain line. | block 9 | to A16, A17, A18 |
| F10a | `f10` (state 1) | At the benchmark, entry rises from 0.250 to 0.523 | §8 F10a; §10 1.50 min, never cut | 6 | `base_rho`, `base_r_weak`, `base_r_strong`, `base_profit_prior_weak`, `base_profit_prior_strong`, `base_spread_weak`, `base_spread_strong`, `base_entry_weak`, `base_entry_strong`, `base_ownership_weak`, `base_ownership_strong`, `base_entry_change_pp` | T3 table, two columns. Rows reveal top to bottom. Takeaway line last. | block 10a | none |
| F10b | `f10` (state 2) | At the benchmark, entry rises from 0.250 to 0.523 | §8 F10b; §10 1.00 min, never cut; §11 Q23 to Q27 | 6 | as F10a plus `base_r_collapse`, `base_entry_collapse`; ownership 0.125 from `tables/table2_equilibrium_controls.tex` Panel A | The build adds the r₂ column. "lower still" and "wider still" stay words. The number 10 does not change. | block 10b | to A19, A20, A21 |
| F11 | `f11` | Freeze the information and deterrence returns | §8 F11; §10 2.25 min, never cut; §11 Q28, Q30 | 6 | `base_entry_weak`, `base_entry_strong`, `base_frozen_entry_weak`, `base_frozen_entry_strong`, `base_hidden_entry_weak`, `base_hidden_entry_strong` | T4 table with the Status column always visible. A three-way toggle (equilibrium, frozen orders, price hidden) highlights the row and draws two bars. The status word of the row is repeated beside the bars. | block 11 | to A22, A23 |
| F12 | `f12` | At intermediate strength, equilibria coexist | §8 F12; §10 1.50 min, cut 3; §11 Q27, Q31 | 7 | `cert_a_r`, `cert_b_r`, `cert_c_r`, `cert_*_v_interval` (negated), `cert_*_entry_interval`, `base_entry_strong`, `base_rho` | T5 table. Hover on a certified value shows the full enclosure with its outward endpoints, never re-rounded. | block 12 | to A24 |
| F13 | `f13` | The entry reversal survives four model changes | §8 F13; §10 1.50 min, cut 6; §11 Q18, Q26, Q32 | 7 | `base_entry_weak`, `base_entry_strong`, `cost_halfwidth`, `cost_mix_laplace_entry_strong`, `logistic_entry_strong`, `moderate_h`, `moderate_ell`, `moderate_entry_weak`, `moderate_entry_strong`, `signal_trader_accuracy_value`, `signal_buyer_accuracy_value`, `signal_rho`, `signal_r_weak`, `signal_r_strong`, `signal_entry_weak`, `signal_entry_strong`; `tables/table3_extensions.tex`; `tables/table_signal_grid.tex` | T6 rows reveal one at a time. The signal-grid footnote opens on demand and stays in the printed state. | block 13 | to A26 |
| F14 | `f14` | Price access raises proceeds and surplus at r₁ | §8 F14; §10 1.00 min, cut 4; §11 Q33 | 7 | `base_r_strong`, `base_revenue_feedback`, `base_revenue_hidden`, `base_revenue_gain`, `base_net_surplus_gain`; 2.38 and 2.30 from `table2_equilibrium_controls.tex` Panel C | A two-state toggle (price observed, price hidden) highlights the column. The gain column stays. | block 14 | to A27 |
| F15 | `f15` | What an empirical test would have to measure | §8 F15; §10 1.00 min, cut 5; §11 Q2 | 8 | main.tex §7; Online Appendix D | Four items reveal. | block 15 | none (A2 hangs off F1) |
| F16 | `f16` | Conclusion | §8 F16; §10 1.00 min, never cut | 8 | `base_entry_weak`, `base_entry_strong` | No reveal. End key lands here. No navigation, as in the PDF. | block 16 | none |

## Backup frames

Each backup keeps one origin. "Back" returns to that origin at the step it was left.

| Frame | Web id | Title (as in talk.tex) | Plan | Origin | Sources | Proposed interaction | Notes source | Forward |
|---|---|---|---|---|---|---|---|---|
| A1 | `a1` | Which deals have a decision interval | §9 A1; §11 Q1, Q9 | F1 | none | Bullets. | script.tex "A1" | none |
| A2 | `a2` | Evidence: a design, not a result | §9 A2; §11 Q2 | F1 | main.tex §7; OA D | Bullets. | "A2" | none |
| A3 | `a3` | Related work in more detail | §9 A3; §11 Q3 | F3 | `references.bib` metadata | "Shows / Here" table. Row hover highlights the pair. | "A3" | none |
| A4 | `a4` | What the model leaves out, and why | §9 A4; §11 Q7, Q8, Q9 | F4 | none | Two-row table. | "A4" | none |
| A5 | `a5` | Complementary, not superior, information | §9 A5; §11 Q5 | F4 | `signal_buyer_accuracy_value`, `signal_trader_accuracy_value` | Bullets. | "A5" | to A6 |
| A6 | `a6` | The price helps a challenger with its own signal | §9 A6; §11 Q5, Q32 | A5 | `signal_trader_accuracy_value`, `signal_buyer_accuracy_value`, `signal_entry_weak`, `signal_entry_strong`, `signal_rho`, `signal_c_high`, `signal_k`, `signal_r_weak`, `signal_r_strong`; `tables/table_signal_grid.tex` | Grid summary table with status column. | "A6" | none |
| A7 | `a7` | Equilibrium and the two comparisons | §9 A7; §11 Q10 | F4 | none | Bullets. | "A7" | none |
| A8 | `a8` | Acquisition payoffs in closed form | §9 A8; §11 Q12 | F5 | `tables/table1_auction_primitives.tex`; `base_r_weak`, `base_r_strong`, `base_spread_weak`, `base_spread_strong`, `base_profit_prior_weak`, `base_profit_prior_strong` | Closed forms in KaTeX; table. | "A8" | none |
| A9 | `a9` | The payment rule decides the sign of the spread effect | §9 A9; §11 Q11 | F5 | `figures_data/bargaining.csv` (fig4, declared η grid); X4 `bargaining_spread_talk.svg` | SVG rebuilt from the CSV. An η slider snaps to the declared grid and reads the two series; the readout says "weakly" at every η. | none in script.tex; use structure-plan §9 A9 and the "Standing Q&A stance" paragraph on bargaining | none |
| A10 | `a10` | Why trading is unique: a global bound | §9 A10; §11 Q7, Q15 | F7 | none | Display in KaTeX; bullets. | "A10" | none |
| A11 | `a11` | Orders, units and the trading cost | §9 A11; §11 Q13, Q14 | F7 | none | Bullets. | "A11" | none |
| A12 | `a12` | Notation | §9 A12 | F7 | structure-plan §6.1 | Two-column glossary. The same content feeds the G-key panel, so one source serves two surfaces. | none in script.tex; use structure-plan §6.1 | none |
| A13 | `a13` | The challenger can read the market's belief off the price | §9 A13; §11 Q16, Q17 | F8 | none | Two displays; bullets. | "A13" | none |
| A14 | `a14` | Why Laplace noise, and what logistic noise changes | §9 A14; §11 Q18 | F8 | `figures_data/posterior_tails.csv` (fig3); `logistic_flow_threshold`, `logistic_threshold_noise_sd`, `logistic_entry_strong`, `base_entry_strong`, `cost_halfwidth`, `cost_mix_laplace_entry_strong`, `cost_mix_logistic_entry_strong`; X3 `posterior_tail_entry_talk.svg` | SVG rebuilt from the CSV, two panels; a toggle dims one noise law. Closed and open end markers kept as in the paper. | "A14" | none |
| A15 | `a15` | Why the model needs a low-cost floor | §9 A15; §11 Q19 | F8 | `base_margin_low_cost`, `base_hidden_entry_weak`, `base_hidden_entry_strong` | Bullets. | "A15" | none |
| A16 | `a16` | Proof logic in four steps | §9 A16; §11 Q20 | F9 | none | Four steps reveal, then part (iii). | "A16" | none |
| A17 | `a17` | Conditions are jointly satisfiable for every h > ℓ | §9 A17; §11 Q21 | F9 | `base_margin_low_cost`, `base_margin_high_prior`, `base_margin_high_ceiling`, `base_margin_weak_trade`, `base_margin_strong_trade`, `base_minimum_theorem_margin`, `moderate_h`, `moderate_minimum_theorem_margin` | Margin table. | "A17" | none |
| A18 | `a18` | Two forces from one payment rule | §9 A18; §11 Q22 | F9 | none | Two-column table; chain line. Column hover dims the other force. | "A18" | none |
| A19 | `a19` | Benchmark scale: declared, not calibrated | §9 A19; §11 Q23 | F10b | `base_h`, `base_ell`, `base_p`, `base_rho`, `base_c_low`, `base_c_high`, `base_b`, `base_k`, `moderate_h`, `moderate_ell`, `moderate_p`, `moderate_rho`, `moderate_c_low`, `moderate_c_high`, `moderate_b`, `moderate_k`, `base_r_weak`, `base_r_strong`, `moderate_r_weak`, `moderate_r_strong`, `base_entry_weak`, `base_entry_strong`, `moderate_entry_weak`, `moderate_entry_strong`, `base_minimum_theorem_margin`, `moderate_minimum_theorem_margin` | Two tables side by side. Inputs carry the `input` status on hover. | "A19" | none |
| A20 | `a20` | How entry and ownership are computed | §9 A20; §11 Q24, Q25 | F10b | `base_r_high_cost_ceiling`, `base_laplace_entry_ceiling_left_limit`; proceeds 0.393, 0.872, 0.664 from `table2_equilibrium_controls.tex` Panel A | Displays in KaTeX; bullets. | "A20" | none |
| A21 | `a21` | Which equilibrium? What the proof certifies | §9 A21; §11 Q27 | F10b | `cert_*_r`, `cert_*_v_interval`, `cert_*_entry_interval`, `cert_*_high_derivative_lower`, `cert_a_psi_left_lower`, `cert_a_psi_right_upper` | Enclosure table printed exactly. | "A21" | none |
| A22 | `a22` | Information controls in detail | §9 A22; §11 Q28 | F11 | `tables/table2_equilibrium_controls.tex` Panels A and B | Full table with the Status column. | "A22" | none |
| A23 | `a23` | Price level or information? | §9 A23; §11 Q30 | F11 | `base_matched_dividend`, `base_revenue_gain` | Bullets. | "A23" | none |
| A24 | `a24` | Trading and entry across strengths: entry | §9 A24; §11 Q31 | F12 | `numerics/correspondence.csv`, `certificates.csv`, `thresholds.csv`, `mixed_supports.csv`; `base_r_pool_unique_sufficient`, `base_r_no_trade_exact`, `base_r_full_unique_sufficient`, `base_r_high_cost_ceiling`; X5a `equilibrium_correspondence_a_talk.svg` | SVG rebuilt from the CSV with the legend as toggles. Broken lines, interval bars, multiplicity ticks and analytical shading stay. Hover shows the evidence status of the branch. | "A24" | to A25 |
| A25 | `a25` | Trading and entry across strengths: orders | §9 A25 | A24 | X5b `equilibrium_correspondence_b_talk.svg`; `cert_*_v_interval` | Same as A24 for order sizes. | none in script.tex; the "A24" block covers both panels | none |
| A26 | `a26` | Robustness in full | §9 A26; §11 Q26 | F13 | `tables/table3_extensions.tex`; `base_entry_change_pp`, `moderate_entry_change_pp`, `signal_entry_change_pp`; `base_minimum_theorem_margin`, `moderate_minimum_theorem_margin`, `signal_minimum_theorem_margin` | Full table. | "A26" | none |
| A27 | `a27` | A higher reserve can raise proceeds; optimal terms are open | §9 A27; §11 Q34 | F14 | `base_p`, `value_reserve_high`, `value_band_halfwidth`; `tables/table4_reserve_comparisons.tex` Panel B; `value_entry_weak_high_p`, `value_entry_strong_high_p`, `value_revenue_weak_low_p`, `value_revenue_weak_high_p`, `value_revenue_strong_low_p`, `value_revenue_strong_high_p` | Table. | "A27" | to A28 |
| A28 | `a28` | Same orders, different prices | §9 A28; §11 Q34 | A27 | `pool_reserve`, `pool_posterior_cutoff_low`, `pool_posterior_cutoff_high`, `pool_entry_cutoff_low`, `pool_entry_cutoff_high`, `pool_revenue_cutoff_low`, `pool_revenue_cutoff_high` | Table. | "A28" | none |
| A29 | `a29` | References | §9 A29 | F3 | `references.bib` | Two columns. | none in script.tex | none |

## Merges and splits

- No frame is merged away and no frame is split. The only change of physical count is F10a and
  F10b, which become one web slide with a build step. Reason: the PDF already shows them as one
  number, and a build step is the web form of a duplicated frame.
- A24 and A25 stay two slides. The two panels of Figure 2 are too dense for one web slide, and
  the PDF keeps them apart.

## Engine chrome (no new content)

The HTML deck adds controls only: an overview (O), a notes panel (N) fed by `script.tex`, a
glossary panel (G) fed by the A12 content, a help panel (?), a projector theme (T), fullscreen (F),
reset (R), and a progress rail by part. Arrow keys and Space advance; Escape returns from a backup.
The notes panel also shows the checkpoint rule from script.tex (frame 3 by 4.75 min; frame 5 by
9.5 min; frame 9 by 18.5 min; frame 11 by 23.5 min).
