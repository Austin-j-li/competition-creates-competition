# Structure plan B: mechanism-first talk

Paper: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders", Austin Li.
Angle B opens on the question "does a stronger incumbent deter a challenger?" and previews the answer at once with the two opposing returns to information. It then gives each force its own frame with a shared skeleton, adds one synthesis frame, and moves to the minimal model, the theorem in words with its conditions, the benchmark numbers and the fixed-information control.

Sources: `talk/notes/paper-digest.md`, `talk/notes/audit-adoptions.md` (binding for notation and wording), `audit/talk_consistency/report.md`, `paper/main_filled.md` (line numbers below are main.md = main_filled.md lines), `numerics/quantity_registry.csv` (registry names in parentheses), `tables/*.csv`, `figures_data/*.csv`. Every number in this plan was read from those files. Where a slide number has no registry scalar, the plan names the table CSV row that supplies it.

---

## 1. Settings and budget

| Item | Value |
|---|---|
| Total session (fixed) | 40 min, questions and interruptions included |
| Planned speech | 30.75 min (76.9% of the session; inside the 75-80% band) |
| Question reserve | 9.25 min (23.1%) |
| Main deck | title (0.25 min) + 16 content frames (30.5 min); no section dividers, no roadmap frame (the talk states its route aloud on frame 3) |
| Appendix | 22 backups (23 frames; A14 is a duplicated pair) after `\AppendixStart`, each reached from exactly one origin through `\PlaceNav` and returned through `\BackButton` |
| Genre / audience | Author presentation, conference or job-market style, for a generalist finance-economics room |
| Punchline | The answer ("yes, a stronger incumbent can bring the challenger in") lands on frame 2 at about 3.5 min. The headline number (entry 0.25 to 0.52, +27.28 pp) lands on frame 3 at about 4.5 min |
| Look | `\documentclass[11pt,aspectratio=169]{beamer}`, `\usetheme{Madrid}`, `\usepackage{econ-slides-compat}`, `\usefonttheme[onlymath]{serif}` (audit F29), XeLaTeX |
| Title page | `\title{Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders}`, `\author{Austin Li}`, `\institute{}`, `\date{}`. The Madrid footline short title is "Competition Creates Competition" |
| Overlays | None: no `\pause`, `\only`, `\onslide` or `\uncover`. No builds are planned. If rehearsal shows a build is needed, the only candidate is frame 6 as a duplicated frame (6a with the deterrence column only, 6b with both) |
| PowerPoint | Rebuilt 1:1 from the finished deck. Every exhibit is a native table, a figure PDF/PNG, an equation, or a box-and-arrow diagram |
| Resolved skill conflicts | There is no Thank-you frame; the conclusion is the last main frame and has no navigation. References sit in the appendix (this overrides beamer-skill rules 11 and 14). There is no literature section; antecedents appear as gray inline citations on frames 1, 3 and 5 plus the appendix References frame. Each slide has at most 2 colored boxes (the deck uses one `ResultBox`, on frame 10), at most 7 items and at most 2 display equations |

---

## 2. Author story

**Research question.** A takeover target is publicly in play. One bidder (the incumbent) is already prepared, and a challenger must pay to prepare before it can bid. Does a stronger incumbent deter the challenger when the challenger can watch the target's stock price before paying? (main.md 13, 19)

**Answer (headline number).** Not necessarily: a stronger incumbent can attract the challenger. It lowers what the challenger earns at every fixed belief. It also makes target proceeds more sensitive to who the challenger is, so informed trading pays and the stock price becomes informative. Favorable prices then bring in an expensive challenger. At the benchmark, moving the incumbent from strength 1.2 (base_r_weak) to 3 (base_r_strong) lowers the challenger's gross profit at the prior from 4.804167 to 4.291667 (base_profit_prior_weak, base_profit_prior_strong). Over the same move, entry rises from 0.250000 to 0.522757 (base_entry_weak, base_entry_strong), which is +27.28 percentage points (base_entry_change_pp), and high-value challenger ownership rises from 0.125000 to 0.324192 (base_ownership_weak, base_ownership_strong). Status: analytical (Proposition 2; main.md 216-257).

**Why it matters.** The textbook comparative static (a stronger rival deters costly entry; Fishman 1988, Hirshleifer and Png 1989) assumes that information is fixed before the entry decision. In a public sale the stock trades while a further bidder decides. The bidder pool then depends on what the market reveals, and sale terms and rival strength shape competition through two channels: what a winner pays and what the price can reveal before anyone prepares (main.md 13, 400-402).

**Contribution: the four author-story items (talk-structures.md).**
1. **Primary takeaway.** On an open set of primitives, strengthening the incumbent turns an uninformative price into an informative one. Entry rises, and so does the probability that a high-value challenger acquires the target, even though the challenger keeps less (Prop. 2, analytical).
2. **Two supporting claims.**
   (a) *The two returns to information move in opposite directions*: one auction, two claims. A stronger incumbent lowers the challenger's gross profit at every belief and raises the target-payoff spread (Prop. 1, analytical; any first-order stochastic strengthening).
   (b) *The information channel does the work*: freeze the investor's orders and a stronger incumbent lowers entry, 0.562178 to 0.522757 (base_frozen_entry_weak/strong; numerical diagnostic; sign analytical, Prop. A.3). Hide the price and entry stays at 0.250000 (base_hidden_entry_weak/strong; analytical).
3. **Strongest credibility argument.** Prices are rational: market makers price the entry each price induces, so the result is not mispricing. The trading outcome is unique in each economy against arbitrary mixed orders and every unilateral deviation $q\in[-1,1]$, because a global bound on marginal trading profit pins the orders. No candidate order profile is assumed (main.md 21, 237; F37 wording).
4. **Boundary audit.** The result rests on sufficient conditions. There must be a low-cost floor, so some entry happens after any price, together with a high-cost window and a trading-cost window. It is a "can", on a nonempty open set, not a general sign. Entry is not monotone in strength: at 3.6 (base_r_collapse) trading stays informative but entry falls back to 0.250000 (base_entry_collapse). This boundary is shown once, as the named conditions and part (iii) on frame 10, and is not repeated on frames 3 or 16.

**Mechanism classification.** *Competing* forces, with a *complementary chain* inside the information force.
- Force 1, deterrence (standard): a stronger incumbent lowers $g_H,g_L$ and so $B_r(\mu)$ at every belief. At any fixed information, entry falls (Prop. A.3).
- Force 2, information (new): the same shift raises $\Delta_T$. The chain is: $\Delta_T\uparrow$, the investor's residual edge (entry probability x $\Delta_T$ x the market's residual uncertainty) covers the trading cost, the price becomes informative, good news pushes the belief above $\tau$, the expensive challenger prepares, and entry and $\mathsf O_H$ rise.
- Dependency: force 2 needs the entry floor (low-cost entry after any price makes proceeds depend on quality) and a price seen before preparation. The net sign is resolved parametrically by the three named conditions. Force 1 reasserts itself at very strong incumbents, where even the best price cannot cover the expensive cost ($B_{r_2}(M)<c_H$).
- Talk architecture that follows from this: two parallel frames (4 and 5) with the same skeleton (Object / Payment rule / Decision it moves / Sign), then one synthesis frame (6) before the model and the proposition.

---

## 3. Claim-evidence ledger

| # | Claim (slide wording) | Status | Paper location | Registry names / source |
|---|---|---|---|---|
| C1 | A stronger incumbent lowers the challenger's gross profit at every fixed belief | supported (analytical, Prop. 1) | main.md 91, 99-121, 125-137 | base_profit_prior_weak, base_profit_prior_strong; figures_data/two_returns.csv |
| C2 | The same shift raises the target-payoff spread $\Delta_T=t_H-t_L$ | supported (analytical, Prop. 1) | main.md 125-137, 141-146 | base_spread_weak, base_spread_strong |
| C3 | Stronger competition turns an uninformative price into an informative one; entry and high-value ownership rise (open set, every $h>\ell$) | supported (analytical, Prop. 2 (i)-(ii)) | main.md 216-237, 759-767 | base_entry_weak/strong, base_ownership_weak/strong, base_entry_change_pp |
| C4 | At a stronger incumbent (3.6) trading stays informative but entry returns to $\rho$ | supported at the benchmark and nearby parameters only (F46). The "nonempty open set" wording of Prop. 2 is **conflicted** for part (iii), so the slide does not claim it for every $h>\ell$ | main.md 233, 250-253, 550 | base_r_collapse, base_entry_collapse |
| C5 | Unique trading and on-path entry, against arbitrary mixed orders and every unilateral deviation $q\in[-1,1]$ | supported (analytical). The paper's "every continuous deviation" is **conflicted** wording (F37); the slide uses the corrected phrase | main.md 21, 89, 233, 237 | none |
| C6 | Prices are rational; the reversal is not mispricing | supported | main.md 21, 79, 189-203 | none |
| C7 | Freeze orders at their informative level and deterrence returns: entry 0.562 to 0.523 | supported. Numbers are a **numerical diagnostic** (frozen weak profile is not an equilibrium; deviation gain 1.619e-2); the sign is analytical (Prop. A.3). Main.md 267 prints the numbers unlabeled (F50) | main.md 267, 554 | base_frozen_entry_weak, base_frozen_entry_strong; tables/equilibrium_controls.csv (status text) |
| C8 | Hide the price from the challenger and entry stays at 0.25 at both strengths | supported (analytical; equilibrium of the no-price-access game). The paper's Table 2 note calls these rows "fixed-profile controls", which is **conflicted** (F08); the slide uses the F08 label | main.md 265, 269 | base_hidden_entry_weak, base_hidden_entry_strong |
| C9 | Laplace noise keeps every posterior in $[m,M]$, $m\approx0.27$ | supported (analytical, Prop. A.1) | main.md 150-167 | base_m, base_M |
| C10 | The challenger can read the market's posterior off the price | supported (analytical, Prop. A.2) | main.md 181-187 | none |
| C11 | Expensive preparation is infeasible above $r_C\approx3.59$ | supported (analytical, Prop. A.4) | main.md 296 | base_r_high_cost_ceiling |
| C12 | At $r=1.55,1.60,1.65$ an informative equilibrium (buy fully, sell partially) coexists with no trade; entry strictly ordered upward | supported (computer-assisted, Prop. 3). The introduction's general "coexist" is **conflicted** (F48); the slide restricts it to three strengths | main.md 23, 273-287 | cert_a/b/c_r, cert_a/b/c_v_interval, cert_a/b/c_entry_interval |
| C13 | The full intermediate correspondence | **open** (reported as open; not claimed) | main.md 298-304 | none |
| C14 | Numerical continuation branches in Fig. 2 | descriptive only (numerical diagnostic; the search is not exhaustive). Backup only | main.md 291-300 | numerics/correspondence.csv |
| C15 | The $r_0\to r_1$ reversal survives logistic noise, atomless costs, complementary signals, and a small value gap | supported (analytical: Props. A.5, A.6, A.7, Sec. 5.2) for parts (i)-(ii) only (F47). "The $r_2$ fall is robust" is **excluded** | main.md 306-341, 733 | logistic_entry_strong, cost_mix_laplace_entry_strong, moderate_entry_weak/strong, moderate_entry_change_pp, signal_entry_weak/strong, signal_entry_change_pp; tables/extensions.csv (weak-entry cells without a registry scalar) |
| C16 | The reversal holds with a more accurate challenger signal ($a=0.70$, $d=0.75$) | supported as the declared example (analytical). The unqualified abstract claim is **conflicted** (F16): in the 25-cell grid entry rises in 6 cells (analytical), is unchanged in 9, and falls 4.03-4.49 pp in the 10 cells with $d\ge0.76$ (numerical diagnostic). The footnote and backup carry this | main.md 8, 330-336; tables/table_signal_grid.tex | signal_trader_accuracy_value, signal_buyer_accuracy_value, signal_entry_weak/strong, signal_entry_change_pp |
| C17 | Holding the incumbent at $r_1$, price access raises target proceeds 0.614583 to 0.872392 and net acquisition surplus 2.302083 to 2.382301 (+0.080218) | supported at $r_1$ only (analytical, Prop. A.9). The introduction's "any fixed strength" is **conflicted** (F15) | main.md 23, 347-351, 918 | base_revenue_hidden, base_revenue_feedback, base_revenue_gain, base_net_surplus_gain; W levels from tables/equilibrium_controls.csv |
| C18 | Matched dividend 0.257809: mean prices match, entry does not, so information matters and not the price level | supported as a **numerical diagnostic** (F10). The paper text says "analytical", which is conflicted. Backup only | main.md 353 | base_matched_dividend |
| C19 | The sign of the spread effect depends on the payment rule (bargaining weight $\eta$ vs 1/2) | supported (analytical, Prop. A.8), weakly (F49). Backup only | main.md 357-372, 897 | figures_data/bargaining.csv |
| C20 | An entry reversal under bargaining | **excluded** (not solved; main.md 372) | main.md 372 | none |
| C21 | A higher reserve (1.1) can raise proceeds against both incumbents | supported (analytical at listed nodes; a feasible improvement, not an optimum). Backup only | main.md 383-392 | value_revenue_weak_low_p/high_p, value_revenue_strong_low_p/high_p, value_entry_weak_high_p, value_entry_strong_high_p, value_reserve_high |
| C22 | Optimal reserve / seller's choice of terms / commitment timing | **open**; stated as the next theorem only | main.md 27, 402 | none |
| C23 | Any empirical claim (prices drew bidders in; Imprivata as evidence) | **excluded** (design only; no sample) | main.md 37, 396-398 | none |
| C24 | Same orders, different prices, beliefs and entry (price pooling, Prop. A.10) | supported (analytical; existence only). Backup only | main.md 1004-1047 | pool_reserve, pool_posterior_cutoff_low/high, pool_entry_cutoff_low/high, pool_revenue_cutoff_low/high |

---

## 4. Emphasis ledger

- **Primary takeaway (frames 2, 3, 10, 11, 16).** A stronger incumbent can attract a challenger by making the target's stock price informative. Entry rises from 0.25 to 0.52 (+27.28 pp) while the challenger's gross profit at the prior falls from 4.80 to 4.29.
- **Support 1 (frames 2, 4, 5, 6).** One auction, two claims: competition lowers what the challenger keeps and raises what target shares reveal about the challenger (Prop. 1).
- **Support 2 (frames 3, 12).** Freeze the information and deterrence returns (0.562 to 0.523, numerical diagnostic; sign analytical). Hide the price and entry stays at 0.25.
- **Boundary (shown once, frame 10 only).** Sufficient conditions by name (low-cost floor, high-cost window, trading-cost window) plus part (iii): at a stronger incumbent, entry falls back to $\rho$. Omitting the conditions would misstate "can" as "does", so they are shown once, beside the theorem. Frames 3 and 16 do not repeat them.
- Not given emphasis on the main line: coexistence (frame 13), robustness (frame 14) and welfare (frame 15) are secondary and are the first frames cut if behind.

---

## 5. Color ledger

Madrid's structure blue (about #3333B2) colors the title bars, footline, `ResultBox` frame and navigation buttons. It carries no economic meaning. Concept colors are defined once as aliases in the preamble:

```latex
\colorlet{cInfo}{cAccentB}   % information force (new object)
\colorlet{cCost}{cAccentA}   % preparation-cost objects (F30)
% deterrence force = neutral (standard object): black text, dark-gray figure lines
```

| Object | Baseline / new | Alias (hex) | Frames where it recurs |
|---|---|---|---|
| Information force: $\Delta_T$, "target-payoff spread", "informed trading", "informative price", full orders $(q_H,q_L)=(1,-1)$, the investor's residual edge | new | `cInfo` = cAccentB vermillion (#D55E00) | 2 (panel (a) line, the word "spread" in the takeaway), 3 (lead phrase of support 1), 5 (lead label, $\Delta_T$ display), 6 (Information column header, chain arrows), 10 (trading-cost window), 11 ($\Delta_T$ row, orders row), 12 (feedback row label), 16 (the phrase "informative price") |
| Deterrence force: $B_r(\mu)$, $g_H,g_L$, "the challenger keeps less" | baseline (standard) | neutral: black text; figure lines #404040 (solid $\mu=M$, dashed $\mu=1/2$, dotted $\mu=m$) | 2 (panel (b)), 4, 6 (Deterrence column), 9 (curves), 11 ($B_r(1/2)$ row), 12 (frozen row) |
| Preparation-cost objects: $c_L$, $c_H$, $\rho$ (entry floor), $\tau$ ("belief threshold for costly preparation"), condition names "low-cost floor" and "high-cost window" | model primitives kept separate from value subscripts (F30) | `cCost` = cAccentA blue (#0072B2) | 4 ($C$ in the decision row), 7 (cost law), 8 (timeline box 4), 9 (horizontal lines $c_L=1$, $c_H=6$; $\tau$ in bullet 2), 10 (the two cost conditions), 11 (parameter line) |
| Outcomes: entry $\mathsf E$, high-value ownership $\mathsf O_H$, headline numbers | outcome | neutral bold | 3, 11, 12, 13, 14, 15, 16 |
| Result-status words (analytical, computer-assisted, numerical diagnostic, open, input) | label | gray `\small` text, never colored or boxed | 2, 9-15 |
| cAccentC (#009E73), cAccentD (#E69F00) | not used on the main line | reserved | Not used, to keep at most 2 concept colors per slide and to avoid a vermillion-green pair |

Rules: colored text is always bold or in display math. cAccentB and cAccentA text only appears bold, because vermillion is below 4.5:1 contrast on white for normal text. The rebuilt figures use the same hex values. The reused backup figures (posterior_tail_entry.pdf, equilibrium_correspondence rebuild) keep the paper palette (#1f3b73 navy, #b5533c rust), so their frames keep nearby text neutral. There are no red-green pairs and no more than 2 concept colors on any slide.

---

## 6. Notation plan

Rules applied throughout: C.0 locked symbols are unchanged. Quality is $\theta\in\{H,L\}$ and never a number (F01). Role words are only incumbent, challenger, investor, market makers, and noise traders (F13). Say "reserve $p$" and "incumbent strength $r$" aloud at first use; afterwards write "strength $r_0\to r_1$", never a bare $r$ once $r_0,r_1$ exist (F31). $\mathbb E$ never appears on a frame that shows $\mathsf E$ (F29). The words are "entry" and "entry floor", never "participation" or "investigation" (F55). $m,M$ are defined before any figure uses them (F40).

### Main-line symbols

| Symbol | Frame introduced | Gloss on the slide | Adoption rule applied |
|---|---|---|---|
| $R$, $r$ | 2 (subtitle) | "incumbent value $R\sim U[0,r]$; $r$ = incumbent strength" | F31 legend; $\bar r=r$ said once on backup A4 (F19) |
| $h$, $\ell$ | 2 (subtitle) | "challenger worth $h=10$ or $\ell=1$" | F01 |
| $p$ | 2 (subtitle) | "reserve $p=0.5$" | F31; never beside $P$ without labels |
| $\theta\in\{H,L\}$, $v_\theta$ | 4 | "challenger quality $\theta\in\{H,L\}$, worth $v_H=h$ or $v_L=\ell$" | F01 |
| $\mu$ | 4 | "public belief $\mu=\Pr(H)$" | F01 |
| $g_\theta$ | 4 | "gross acquisition profit of a type-$\theta$ challenger", $g_\theta=\mathbb E[(v_\theta-\max\{p,R\})_+]$ | F28 lowercase, combined with F01 $v_\theta$ |
| $B_r(\mu)$ | 4 | "expected gross profit at belief $\mu$": $B_r(\mu)=g_L+\mu(g_H-g_L)$ | F23 (strength is the only subscript) |
| $C$ | 4 | "preparation cost $C$" | F30, F22 |
| $\Delta_T$, $t_H$, $t_L$ | 5 | "target-payoff spread $\Delta_T=t_H-t_L$: expected target proceeds with a high- vs a low-value challenger"; $\Delta_T=\mathbb E[(R-\ell)_+]$ | F36, F04 (T only as the subscript), F28 |
| $c_L,c_H,\rho$ | 7 | "cost $C\in\{c_L,c_H\}$, $\Pr(C=c_L)=\rho$, independent of $\theta$; cheap/expensive preparation" | F30, F22 (two atoms only) |
| $q$, $k$ | 7 | "investor order $q\in[-1,1]$, trading cost $k\lvert q\rvert$" | F24 ($U_\theta$ not shown) |
| $X$, $Z$, $b$ | 8 | "order flow $X=q+Z$; noise demand $Z$, Laplace with scale $b$" | F31 ($b$ = noise scale) |
| $P(X)$, $V_T$ | 8 | "stock price $P(X)=\mathbb E[V_T\mid X]$; $V_T$ = payoff of a target share" | F31, F29 (no $\mathsf E$ on frame 8) |
| $\mu_X$ | 9 | "market's posterior $\mu_X=\Pr(H\mid X)$, readable from the price" | F02, F43 |
| $m$, $M$ | 9 (subtitle, above the figure) | "posterior band $[m,M]$, $m=1/(1+e^{2/b})\approx0.27$, $M=1-m$" | F40, F42 |
| $\tau$ | 9 | "belief threshold for costly preparation", $\tau=(c_H-g_L)/(g_H-g_L)$, with $c_H$ annotated "expensive cost" | F44, F30 |
| $r_0,r_1,r_2$ | 10 | "weak, strong, stronger incumbent (benchmark 1.2, 3, 3.6)" | F11 (reserved for these three) |
| $(q_H,q_L)$ | 10 | "order after a high / low challenger value" | F40, F05 |
| condition names | 10 | "low-cost floor", "high-cost window", "trading-cost window" | F35 (never "(A1)") |
| $\mathsf E$ | 11 | "Entry $\mathsf E$ = Pr(challenger prepares)" | F29 (serif math font keeps $\mathsf E$ distinct), F55 |
| $\mathsf O_H$ | 11 | "high-value challenger ownership $\mathsf O_H$ = Pr(high-value challenger acquires the target)" | F56 |
| $r=1.55,1.60,1.65$; $q_L$ values | 13 | nodes labeled by value; "$q_H=1$, $q_L\approx-0.460,-0.707,-0.903$" | F05, F11 (no $v$, no $r_j$), F53 (1.55/1.60/1.65 as a column) |
| $a$, $d$ | 14 | "investor accuracy $a=0.70$, challenger accuracy $d=0.75$" (probabilities, no percent) | F02, F13, F53 |
| $r_C$ | 9 (bullet, in words: "impossible beyond $r_C\approx3.59$") | "expensive entry impossible above $r_C$" | F41, F52 |

Backup-only symbols: $e_H,e_L$ (F09), $\alpha_H,\alpha_L$ (F18, F20), $x^*$, $r_P,r_N,r_U$ (F41), $U_\theta(s)=s\,\Pi_\theta(s)-ks$ (F17), $t_\eta,g_{\theta,\eta},\Delta_\eta,\eta$ (F04, F06, F28, F49), $D_0$ (F10), $\kappa$ (F03), $\bar\mu$ (F21), $\mathsf A,\mathsf C_2,\mathsf S$ are shown in words only. Never shown: $a_H,a_L,a_\pm$ (F02), $\lambda_X$ (F07), $v,s_L$ (F05), $G_\theta$ (F28), $\mathfrak r(\cdot)$, $\Delta_T^{-1}$ (F41), $H_C,h_C$ (F22), $Q_{\theta,y}$ (F18), $\overline F_Z$ (F20), $\phi_\pm$ (F44), $\mathcal E(p,r)$ (F29), "(A1)-(A3)" (F35), $B_p$ (F23), $F_\theta$ (F17).

### Collision guards on slides
- $R$ (incumbent value) vs $\mathcal R_T$: $\mathcal R_T$ is never shown; write "target proceeds" in words.
- $T$: used only as the subscript in $\Delta_T$ and $V_T$. The investor's signal is described in words (F04).
- $c$: only $c_L,c_H$; the price-pool cutoff on backup A20 is written in words (F03).
- $H/L$: subscripts on $c$ index cost levels, which is spoken on frame 7 and shown in `cCost` (F30).
- $e$: only as the exponential in $m=1/(1+e^{2/b})$. Per-state entry $e_H,e_L$ is backup only.

### Deliberate differences from the paper's current text (paper-sync entries)

| # | Slide version | Paper text now | Audit ID | Paper location |
|---|---|---|---|---|
| S1 | Quality $\theta\in\{H,L\}$, values $v_H=h$, $v_L=\ell$; $\mu=\Pr(H)$ | $\theta\in\{\ell,h\}$ as a number; $\mu=\Pr(\theta=h)$ | F01 | main.md 51, 91 |
| S2 | $g_\theta=\mathbb E[(v_\theta-\max\{p,R\})_+]$ (lowercase $g$, value $v_\theta$) | $G_\theta(F)=\mathbb E_F[(\theta-\max\{p,R\})_+]$ | F28 + F01 (the author must pick one; slides use lowercase with $v_\theta$) | main.md 131-132 |
| S3 | "target-payoff spread" on the rebuilt Figure 1 axis and on the bargaining backup axis | "information spread" (figure axis labels, Table 1, Prop. A.8) | F36 | numerics/render/figures.py 246, 359; tables.py 188; main.md 897 |
| S4 | Conditions named "low-cost floor", "high-cost window", "trading-cost window" | (A1), (A2), (A3) | F35 | main.md 219-229 |
| S5 | "Uniqueness: arbitrary mixed orders; every unilateral deviation $q\in[-1,1]$" | "every continuous deviation" | F37 | main.md 21, 233, 334, 821 |
| S6 | Part (iii) stated at the benchmark and nearby; open-set claim for (i)-(ii) with every $h>\ell$ | open-set claim covers all three parts | F46 | main.md 233, 550 |
| S7 | Panel B header "Information controls"; frozen row "control, not an equilibrium at $r_0$"; price-hidden row "equilibrium of the no-price-access game" | "fixed-profile controls" for both | F08 | main.md 265, 267 |
| S8 | Frozen numbers labeled "numerical diagnostic; sign analytical (Prop. A.3)" | numbers unlabeled | F50 | main.md 267 |
| S9 | Certified nodes: "$q_H=1$, $q_L\approx-0.460,-0.707,-0.903$ at $r=1.55,1.60,1.65$" | $(1,-v_j)$ at $r_j$ | F05, F11 | main.md 275-287 |
| S10 | "Coexistence established at three strengths (computer-assisted); elsewhere search not exhaustive" | the introduction states coexistence generally | F48 | main.md 23 |
| S11 | Welfare "holding the incumbent at $r_1$"; "at $r_0$ no gain" | "at any fixed strength" | F15 | main.md 23 |
| S12 | Robustness covers the $r_0\to r_1$ reversal only | Prop. A.5 extends all of Prop. 2 | F47 | main.md 733 |
| S13 | Signals example plus the grid footnote (6 rise / 9 unchanged / 10 fall) | unqualified reversal | F16 | main.md 8, 23, after 336 |
| S14 | Accuracies as probabilities $a=0.70$, $d=0.75$; "challenger accuracy" | "70%", "75%", "buyer accuracy" | F53, F13 | main.md 336 |
| S15 | Matched dividend labeled "diagnostic" | "analytical invariance diagnostic" | F10 | main.md 353 |
| S16 | "No-trade equilibrium", "no-trade existence boundary $r_N$", $r_P$ for the no-trade uniqueness bound | "pooling"; $\mathfrak r(k)$ | F12, F41, F52 | main.md 296, 568-595 |
| S17 | $e_\theta=\rho+(1-\rho)\alpha_\theta$, $\mathsf E=(e_H+e_L)/2$, $\mathsf O_H=e_H/2$ (backup A12) | $e_H$ used before definition | F09 | main.md 239-253, 548 |
| S18 | "Entry = paying the preparation cost $C$" defined on the timing frame | "entry" used before definition; "participation", "investigation" | F55 | main.md 57, 235, 253 |
| S19 | "High-value challenger ownership" | "high-quality ownership" (OA, manifest) | F56 | OA 216; manifest |
| S20 | Logistic threshold "$x^*\approx5.42$, about 1.5 noise s.d." | 1.495369 at 6 decimals | F38 | manifest row 63 |
| S21 | Bargaining: "weakly" rises / falls; transfer in words as $t_\eta$ | "positive / negative"; $T_\eta$ and $P$ | F49, F04, F06 | main.md 363, 370, 899-906 |
| S22 | Binary-value reserve alternative labeled "$p=1.01$" (backup A19) | 1.01 absent from main.md and registry; appears only in tables/table4 | F39 | main.md 383, 1146; new key binary_reserve_high |
| S23 | "Challenger", never "buyer"; "investor", never "trader" | mixed | F13 | main.md 19, 35, 269, 330, 357 and others |
| S24 | $m=1/(1+e^{2/b})\approx0.27$ written with the exponent | bare $e$ | F42 | main.md 1027 |

---

## 7. Exhibit inventory

| ID | Source | Treatment | Target file (talk/figures/) | Necessity | PowerPoint treatment |
|---|---|---|---|---|---|
| X1 | figures/two_returns.pdf; data figures_data/two_returns.csv | **Rebuild from CSV**. Panel (a) $\Delta_T(r)$ in #D55E00. Panel (b) restricted to the prior, $B_r(1/2)$, in #404040. Axis labels in words: (a) "target-payoff spread", (b) "challenger's expected gross profit at the prior". Dotted verticals at 1.2 and 3 labeled "weak", "strong". $x$ range 1.0-3.8. Slide-scale fonts (>= 11 pt at 0.92\linewidth), vector PDF, embedded fonts, `(a)/(b)` labels, no title. Rationale: the source axis says "information spread" (contradicts F36); panel (b) plots $\mu=m,M$, which the opener has not defined (F40); markers are needed to tie the curves to the benchmark economies. Crop or reuse cannot fix labels. Inputs: two_returns.csv columns r, mu, Delta_T, B_r(mu); markers from base_r_weak, base_r_strong. Status: rebuilt figure, individual QA required | two_returns_opener.pdf (+ .png at 300 dpi) | Load-bearing: the visual anchor of the preview (frame 2) | Insert the PNG (or the PDF converted to EMF) as a picture; the two markers are native dotted lines + text boxes over the picture if editing is wanted |
| X2 | figures/two_returns.pdf panel (b); figures_data/two_returns.csv; inputs base_c_low, base_c_high; registry base_r_high_cost_ceiling | **Rebuild from CSV**. One panel: $B_r(\mu)$ at $\mu=m$ (dotted), $1/2$ (dashed), $M$ (solid), #404040, direct labels "$\mu=M$ (best price)", "$\mu=1/2$ (prior)", "$\mu=m$ (worst price)". Horizontal lines $c_H=6$ (solid, #0072B2, label "expensive cost $c_H$") and $c_L=1$ (dashed, #0072B2, label "cheap cost $c_L$"). Verticals at 1.2, 3, 3.6; a light marker at $r_C$. $y$ range 0.5-7.5. Rationale: the high-cost window and low-cost floor are visual comparisons of cost levels against belief-specific profit curves, and no source exhibit draws the cost lines. Inputs: CSV curves; cost lines are declared inputs; no new computed number is printed. Status: rebuilt figure, individual QA required | profit_thresholds.pdf (+ .png) | Load-bearing: makes conditions 1-2 and part (iii) visible before the theorem (frame 9) | Picture; the cost lines may be redrawn as native lines if the plot area is calibrated |
| X3 | paper Table 1 and Table 2 Panel A (tables/auction_primitives.csv, equilibrium_controls.csv); registry | **Native table** (booktabs, 3 value columns, 5 rows, 3 decimals; `\vspace{4pt}` under the Madrid title bar) | none (inline LaTeX) | Load-bearing (frame 11) | Native PowerPoint table |
| X4 | paper Table 2 Panels A-B (tables/equilibrium_controls.csv); registry | **Native table** (3 rows x 3 value columns + status column) | none | Load-bearing (frame 12) | Native table |
| X5 | Timing (main.md 85) | **New simple diagram**: 5 boxes in a left-to-right timeline, 4 arrows; box 4 edged in #0072B2 ("challenger sees $P$ and $C$; prepares or stays out"). Rationale: the order of moves (price before preparation) is the load-bearing assumption. A numbered list reads as a menu, while a timeline shows that the price is fixed before the entry decision. Status: new figure, individual QA required | inline TikZ, boxes and arrows only (no plotting) | Supporting (frame 8) | 5 native rounded rectangles + 4 arrows + text |
| X6 | Synthesis (frames 4-5) | **Native table**, 2 columns (Deterrence / Information) x 4 rows (same skeleton), plus one inline causal chain with arrows | none | Load-bearing (frame 6) | Native table + one text line |
| X7 | Prop. 3 (registry cert_*) | **Native table** (3 rows: $r$, $q_L$, $\mathsf E$) | none | Supporting (frame 13) | Native table |
| X8 | Table 3 (tables/extensions.csv); registry | **Native table** (5 rows: economy, $\mathsf E$ weak, $\mathsf E$ strong); Evidence/Unique columns dropped and stated in a footnote | none | Supporting (frame 14) | Native table |
| X9 | Table 2 Panel C; registry | **Native table** (3 rows x 2 columns: price hidden / price observed) | none | Supporting (frame 15) | Native table |
| X10 | figures/equilibrium_correspondence.pdf; data numerics/correspondence.csv, numerics/mixed_supports.csv, numerics/certificates.csv, numerics/thresholds.csv | **Rebuild from CSV** by re-running the paper renderer's figure-2 logic in a talk-local script, changing labels only. Legend "asymmetric: $q_H=1$, partial sale $\lvert q_L\rvert$", "symmetric interior". No $v$ or $u$ (F05). Thresholds labeled by meaning (F41, F52). "computer-assisted" and "numerical diagnostic" legends stay visible (F48). Panel (a) only on A14a, panel (b) on A14b (duplicated frames, no overlays). Rationale: the source legend uses $v$/$u$ (F05) and is too dense at slide size. Status: rebuilt figure, individual QA required | equilibrium_correspondence_a.pdf, equilibrium_correspondence_b.pdf | Backup A14 | Picture |
| X11 | figures/posterior_tail_entry.pdf | **Reuse** as is (labels $\Pr(\mu_X\ge\tau)$, "total entry", "threshold distance $M-\tau$" comply with F43) | copy: posterior_tail_entry.pdf | Backup A9 | Picture |
| X12 | figures/bargaining_weight.pdf panel (a); figures_data/bargaining.csv | **Rebuild panel (a) from CSV** with the axis "target-payoff spread $\Delta_\eta$" (F36); $\eta=1/2$ marked; weak/strong curves. Panel (b) dropped (it uses capital $G$, against F28, and a busy log scale). Status: rebuilt figure, individual QA required | bargaining_spread.pdf | Backup A5 | Picture |
| X13 | Table 1 (tables/auction_primitives.csv) | **Native table**: 7 rows x 3 columns (1.2 / 3 / 3.6) | none | Backup A2 | Native table |
| X14 | tables/table_signal_grid.tex | **Native summary table** (3 rows: conditions met / unchanged / falls, with counts and pp ranges) instead of the 25-row longtable | none | Backup A16 | Native table |
| X15 | Table 4 Panel B (tables/reserve_comparisons.csv) | **Native table**, one panel (value classes, $p=0.5$ vs $p=1.1$; 4 rows x 5 columns); the Panel A rows are given in a note line with "$p=1.01$" labeled (F39) | none | Backup A19 | Native table |

The build script `talk/figures/build_figures.py` only reads CSV. It never solves, changes a parameter, or drops a branch, and it writes vector PDFs with embedded fonts plus 300-dpi PNGs for PowerPoint. Each rebuilt figure is marked "QA complete" only after the standalone asset and every slide using it have been inspected.

---

## 8. Main deck, frame by frame

Minutes are planned speech. "Takeaway" is the one normal-size reading line (`\Takeaway` / `\TakeawayWithNav`). Number sources are in parentheses. Status is written in small gray at the foot of exhibit frames.

### Frame 0 (title, plain, uncounted) - 0.25 min
Title and "Austin Li" only. Spoken: one sentence of self-introduction and "questions welcome as we go".

### Frame 1 - "Does a stronger incumbent deter a challenger?" - 1.25 min
- **Subtitle:** A listed target in play: one bidder prepared, one deciding whether to pay to prepare
- **Content (single column):**
  - A takeover target is publicly in play; its stock keeps trading.
  - The **incumbent** bidder has already prepared.
  - A **challenger** must first pay to prepare (diligence, financing, approvals); call that **entry**. Without it the challenger cannot bid.
  - Received answer: a stronger rival lowers what preparation earns, so it deters entry. `\graycite{Fishman 1988; Hirshleifer and Png 1989; Levin and Smith 1994}`
  - But the challenger decides *while the stock trades*, and it can watch the price.
  - **Key question:** can a stronger incumbent bring the challenger *in*, through what the price reveals?
- **Takeaway:** none (text frame; the last bullet is the question)
- **Claim status:** motivation (C1 in words)
- **Nav:** `\PlaceNav` "When does this apply?" to A1
- **Notation introduced:** none (words only)
- Speaker hook (from the old deck): "The model needs an interval, not a date. A wholly confidential process does not qualify."

### Frame 2 - "One auction, two claims, opposite responses" - 2.5 min
- **Subtitle:** Incumbent value $R\sim U[0,r]$, strength $r$; challenger worth $h=10$ or $\ell=1$; reserve $p=0.5$
- **Content:** exhibit X1 (two_returns_opener.pdf, width 0.92\linewidth, height about 0.58\textheight). (a) target-payoff spread rising in $r$ (vermillion); (b) challenger's expected gross profit at the prior falling in $r$ (gray); markers "weak" at 1.2, "strong" at 3.
- **Takeaway:** "A stronger incumbent: the challenger keeps less (b), but target proceeds depend more on **who the challenger is** (a)."
- Status foot: "analytical (Prop. 1); acquisition-stage payoffs, before trading and entry"
- **Spoken (the preview of the answer):** a high-value challenger pays $\max\{p,R\}$, which rises with $r$. A low-value challenger loses to a strong incumbent, and then the incumbent pays only $\ell$. So shareholders' proceeds now differ by challenger type. That gap is what an informed investor trades on, and the talk's answer is: yes, the second effect can win.
- **Claim status:** C1, C2 supported
- **Nav:** "Payoff formulas" to A2
- **Notation introduced:** $R$, $r$, $h$, $\ell$, $p$ (5)

### Frame 3 - "This paper" - 1.75 min
- **Content:**
  - Framing line: "A takeover auction in which a challenger sees the target's stock price before paying to prepare; prices rational, trading and entry solved in equilibrium."
  - `\KeyIdea{Competition creates competition.}` A stronger incumbent turns an uninformative price into an informative one; entry rises **from 0.25 to 0.52** (+27.28 pp) although the challenger's gross profit at the prior falls from 4.80 to 4.29. (base_entry_weak, base_entry_strong, base_entry_change_pp, base_profit_prior_weak/strong)
    - The probability that a high-value challenger acquires the target rises from 0.125 to 0.324. (base_ownership_weak/strong)
  - **One auction, two claims** (cInfo lead): competition lowers what the challenger keeps and raises what target shares reveal about it.
  - **Freeze the information and deterrence returns:** entry then falls, 0.562 to 0.523. (base_frozen_entry_weak/strong)
  - **Implication:** sale terms and rival strength shape the bidder pool through what a winner pays *and* through what the price reveals before anyone prepares.
  - Gray line: `\graycite{Closest: Dow, Goldstein and Guembel 2017 (prices guide real decisions); Edmans, Goldstein and Jiang 2015}`. New here: the sale rule splits one surplus into a traded claim and the entrant's claim, and competition moves them in opposite directions.
- **Takeaway:** the Implication line serves as the capstone
- **Claim status:** C3, C7 supported (C7 numbers are numerical diagnostic; stated as such aloud, labeled on frame 12)
- **Nav:** "References" to A21; "Evidence?" to A22
- **Notation introduced:** none new (numbers in words: "entry", "high-value challenger acquires")
- Spoken route (replaces a roadmap frame): "two forces, the model, the theorem, the numbers, and the control that shows information is doing the work."

### Frame 4 - "Force 1, deterrence: the challenger keeps less" - 1.75 min
- **Subtitle:** At a fixed belief, a stronger incumbent raises what a winning challenger must pay
- **Content (skeleton shared with frame 5):**
  - **Object:** challenger quality $\theta\in\{H,L\}$, worth $v_H=h$ or $v_L=\ell$; public belief $\mu=\Pr(H)$
    $$B_r(\mu)=g_L+\mu\,(g_H-g_L),\qquad g_\theta=\mathbb E\big[(v_\theta-\max\{p,R\})_+\big]$$
  - **Payment rule:** a winning challenger pays $\max\{p,R\}$, so a stronger incumbent means a larger payment
  - **Decision it moves:** the challenger prepares iff $B_r(\mu)\ge$ its preparation cost $\textcolor{cCost}{C}$
  - **Sign:** $g_H,g_L$ fall in $r$, so at any *fixed* belief fewer costs are covered and **entry falls**
- **Takeaway:** "With information held fixed, competition deters: the textbook force, and it stays in the model."
- **Claim status:** C1 supported (Prop. 1; Prop. A.3 for the fixed-information sign)
- **Nav:** "Any incumbent distribution" to A4
- **Notation introduced:** $\theta$/$v_\theta$, $\mu$, $g_\theta$, $B_r$, $C$ (5)

### Frame 5 - "Force 2, information: informed trading pays more" - 2.25 min
- **Subtitle:** The same payment rule, read by target shareholders
- **Content (same skeleton):**
  - **Object:** target-payoff spread $\textcolor{cInfo}{\Delta_T}=t_H-t_L$, expected target proceeds with a high- minus a low-value challenger
    $$\textcolor{cInfo}{\Delta_T}=\mathbb E\big[(R-\ell)_+\big]=\frac{(r-\ell)^2}{2r}\ \ \text{(uniform)}$$
  - **Payment rule:** if $R>\ell$, a high-value challenger wins and pays $R$; a low-value one loses and the incumbent pays $\ell$. The gap is $(R-\ell)_+$
  - **Decision it moves:** an investor who knows $\theta$ trades target shares against noise. With rational prices its edge = entry probability $\times\ \Delta_T\ \times$ the market's residual uncertainty; it trades iff the edge beats its trading cost
  - **Sign:** $\Delta_T$ rises in $r$, so trading can pay, the price turns informative, good news brings in an expensive challenger, and **entry rises**
- **Takeaway:** "Competition raises the value of knowing who the challenger is, and that knowledge reaches the challenger through the price."
- **Claim status:** C2 supported; the chain previews C3
- **Nav:** "Other payment rules" to A5 (bargaining)
- **Notation introduced:** $\Delta_T$ ($t_H,t_L$) (1-3)
- Speaker hook: "the investor has no position, no control rights and no route to bidding: not a toehold story."

### Frame 6 - "Which force wins depends on what the price reveals" - 1.5 min
- **Content:** exhibit X6, a native table:

  | | Deterrence | \textcolor{cInfo}{Information} |
  |---|---|---|
  | What moves | $B_r(\mu)\downarrow$ at every belief | $\Delta_T\uparrow$ |
  | Who responds | challenger, at a given belief | investor, then price, then challenger's belief |
  | Needs | nothing | some entry after any price; price seen before preparation |
  | Entry | $\downarrow$ | $\uparrow$ once the price is informative |

  One chain line below: stronger incumbent $\to$ $\Delta_T\uparrow$ $\to$ trading pays $\to$ informative price $\to$ good news $\to$ expensive challenger prepares
- **Takeaway:** "Information wins when trading pays only against the strong incumbent and good news moves the expensive challenger across its threshold."
- **Claim status:** mechanism synthesis (C1, C2, C3)
- **Nav:** "Is the floor doing the work?" to A6
- **Notation introduced:** none

### Frame 7 - "Model: four roles around one public sale" - 1.75 min
- **Content:**
  - **Seller:** commits *before trading* to a cash second-price auction with reserve $p$
  - **Incumbent:** prepared; value $R\sim U[0,r]$, private until it bids; strength $r$ is a public distribution, not a bid
  - **Challenger:** quality $\theta\in\{H,L\}$ equally likely, unknown until it prepares; cost $\textcolor{cCost}{C\in\{c_L,c_H\}}$, $\Pr(C=c_L)=\textcolor{cCost}{\rho}$, independent of $\theta$ (cheap / expensive preparation)
  - **Investor:** knows $\theta$; order $q\in[-1,1]$, trading cost $k\lvert q\rvert$; no control rights, cannot bid
  - **Noise traders and market makers:** random demand; competitive market makers see only total order flow and set a rational price
  - Gray legend (F31): "$p$ = reserve, $r$ = incumbent strength, $R$ = its value"
- **Takeaway:** "One challenger with one realized cost: the cheap draw keeps entry positive after any price; the expensive draw responds to news."
- **Claim status:** setup (input)
- **Nav:** "What is excluded" to A7; "Notation" to A23
- **Notation introduced:** $c_L,c_H,\rho,q,k$ (5)

### Frame 8 - "Timing: the price arrives before the entry decision" - 1.75 min
- **Content:** exhibit X5 (timeline, 5 boxes):
  (1) Seller commits to the auction and $p$, then (2) Investor learns $\theta$ and submits $q$, then (3) Market makers see $X=q+Z$ and set $P(X)$, then (4) Challenger sees $P$ and its cost $C$ and prepares (**entry**) or stays out, then (5) Prepared bidders learn values and bid truthfully; winner pays $\max\{p,\text{runner-up bid}\}$.
  Below: $$X=q+Z,\quad Z\sim\text{Laplace}(b),\qquad P(X)=\mathbb E[V_T\mid X]$$
  - **Entry** = the challenger pays preparation cost $C$ (learns $\theta$, can bid). The challenger sees $P$ and $C$, not $X$, $\theta$ or $R$
  - **Equilibrium:** optimal (possibly mixed) orders, rational price, Bayesian beliefs, optimal entry, truthful bids
- **Takeaway:** none (diagram + two reading lines, at most two per the schematic rule)
- **Claim status:** setup (input); C6
- **Nav:** "Equilibrium and price inversion" to A8
- **Notation introduced:** $X,Z,b,P,V_T$ (5)

### Frame 9 - "Only good news makes expensive preparation pay" - 2.5 min
- **Subtitle:** Laplace noise keeps every posterior in $[m,M]$, $m=1/(1+e^{2/b})\approx0.27$, $M=1-m$ (base_m, base_M; $b=2$)
- **Content:** exhibit X2 (profit_thresholds.pdf, about 0.52\textheight), then two reading bullets:
  - The challenger reads the market's posterior $\mu_X=\Pr(H\mid X)$ off the price; under any orders it stays in $[m,M]$
  - Expensive preparation needs belief $\ge\textcolor{cCost}{\tau}=\dfrac{\textcolor{cCost}{c_H}-g_L}{g_H-g_L}$ (inline, $c_H$ = expensive cost): never at the weak prior, possible after good news against the strong incumbent, impossible beyond $r_C\approx3.59$ (base_r_high_cost_ceiling)
- **Takeaway:** none (two reading bullets are the reading)
- Status foot: "analytical (Props. A.1, A.2, A.4); benchmark $c_L=1$, $c_H=6$ (input)"
- **Claim status:** C9, C10, C11 supported
- **Nav:** "Why Laplace noise" to A9
- **Notation introduced:** $m,M,\mu_X,\tau$ ($r_C$ in words) (4-5)
- Worked-example role: the figure is the worked example for $B_r$, $m$, $M$, $\tau$ within one frame of their definitions.

### Frame 10 - "Proposition 2: a stronger incumbent raises entry" - 3.5 min
- **Subtitle:** Weak incumbent $r_0$ vs strong $r_1$ vs stronger $r_2$; unique trading and on-path entry in each economy
- **Content:** one `ResultBox` (the only colored box):
  - (i) **Weak $r_0$:** no trade, $q_H=q_L=0$; uninformative price; entry $=\rho$
  - (ii) **Strong $r_1$:** full orders $(q_H,q_L)=\textcolor{cInfo}{(1,-1)}$ (order after a high / low challenger value); informative price; entry $>\rho$; higher high-value ownership
  - (iii) **Stronger $r_2$:** trading stays informative, but entry falls back to $\rho$ (even the best price cannot cover $c_H$)

  Below the box, **Conditions** (inline math):
  - \textcolor{cCost}{\textbf{Low-cost floor}} $c_L<B_{r_1}(m)$: a cheap challenger prepares after any price
  - \textcolor{cCost}{\textbf{High-cost window}} $B_{r_0}(1/2)<c_H<B_{r_1}(M)$: an expensive challenger stays out at the weak prior and enters after the best strong price
  - \textcolor{cInfo}{\textbf{Trading-cost window}} $\Delta_T(r_0)<k<(1-1/b)\,\rho\, m\,\Delta_T(r_1)$: trading loses against $r_0$ and pays against $r_1$, even at the worst price

  Footnote (small gray): "Holds on a nonempty open set of primitives (every $h>\ell$) for (i)-(ii); (iii) at the benchmark and nearby. Uniqueness: arbitrary mixed orders; every unilateral deviation $q\in[-1,1]$. Analytical."
- **TakeawayWithNav:** "**Intuition:** against $r_0$ no order covers its cost; against $r_1$ even the smallest edge $\rho m\Delta_T$ beats $k$, so full orders are forced."
- **Claim status:** C3, C4 (benchmark wording), C5 supported
- **Nav:** "Proof logic" to A10; "Conditions and margins" to A11
- **Notation introduced:** $r_0,r_1,r_2$, $q_H,q_L$, condition names (5)
- Density check: 3 box items + 3 condition items = 6 (at most 7); no display equations; 1 box.

### Frame 11 - "Benchmark: entry rises from 0.25 to 0.52" - 2.0 min
- **Subtitle:** $h=10$, $\ell=1$, $p=0.5$, $\rho=0.25$, $c_L=1$, $c_H=6$, $b=2$, $k=0.02$ (declared inputs: base_h ... base_k)
- **Content:** exhibit X3, a native table:

  | | weak $r_0=1.2$ | strong $r_1=3$ | stronger $r_2=3.6$ |
  |---|---|---|---|
  | Gross profit at prior $B_r(1/2)$ | 4.80 | 4.29 | 4.13 |
  | \textcolor{cInfo}{Target-payoff spread $\Delta_T$} | 0.017 | 0.667 | 0.939 |
  | Investor orders $(q_H,q_L)$ | $(0,0)$ | \textcolor{cInfo}{$(1,-1)$} | $(1,-1)$ |
  | **Entry $\mathsf E$** = Pr(challenger prepares) | 0.250 | **0.523** | 0.250 |
  | **High-value ownership $\mathsf O_H$** | 0.125 | **0.324** | 0.125 |

  Sources: base_profit_prior_weak (4.804167), base_profit_prior_strong (4.291667), tables/auction_primitives.csv r = 3.6 B_prior (4.134722); base_spread_weak (0.016667), base_spread_strong (0.666667), auction_primitives.csv r = 3.6 Delta_T (0.938889); orders from tables/equilibrium_controls.csv analytical rows; base_entry_weak (0.250000), base_entry_strong (0.522757), base_entry_collapse (0.250000); base_ownership_weak (0.125000), base_ownership_strong (0.324192), equilibrium_controls.csv r = 3.6 O_H (0.125). Displayed to 3 decimals (profit to 2).
  Gray note: "$\mathsf O_H$ = Pr(high-value challenger acquires the target). Rounded from validated outputs. Analytical."
- **Takeaway:** "Entry +27.28 pp (base_entry_change_pp) while the challenger's gross profit falls: the price, not the prize, brings it in."
- **Claim status:** C3, C4 supported
- **Nav:** "Entry and ownership formulas" to A12
- **Notation introduced:** $\mathsf E$, $\mathsf O_H$ (2)

### Frame 12 - "Freeze the information and deterrence returns" - 2.5 min
- **Subtitle:** Entry $\mathsf E$ at weak $r_0=1.2$ and strong $r_1=3$; Panel A = equilibria of the feedback game, below = information controls
- **Content:** exhibit X4, a native table:

  | | $r_0$ | $r_1$ | Status |
  |---|---|---|---|
  | \textcolor{cInfo}{Feedback equilibrium} (price seen, trading re-solved) | 0.250 | 0.523 | analytical |
  | *Information controls* | | | |
  | Frozen informative orders (control, not an equilibrium at $r_0$) | 0.562 | 0.523 | numerical diagnostic; sign analytical (Prop. A.3) |
  | Price hidden from challenger (equilibrium of the no-price-access game) | 0.250 | 0.250 | analytical |

  Sources: base_entry_weak/strong; base_frozen_entry_weak (0.562178), base_frozen_entry_strong (0.522757); base_hidden_entry_weak/strong (0.250000).
- **Takeaway:** "Hold the information fixed and a stronger incumbent deters, as the textbook says; the rise comes from the information trading generates."
- **Claim status:** C7 (numerical diagnostic + analytical sign), C8 supported
- **Nav:** "The controls in detail" to A13
- **Notation introduced:** none
- Speaker hook: "In the strong economy the frozen profile coincides with the equilibrium, so the whole difference comes from the weak economy. Its deviation gain is 1.619e-2: a control, not an equilibrium."

### Frame 13 - "Between the two economies, equilibria coexist" - 1.5 min [skip if behind]
- **Subtitle:** Computer-assisted: interval arithmetic on exact decimal inputs at three strengths
- **Content:** exhibit X7, a native table:

  | $r$ | $q_H$ | $q_L$ (certified) | Entry $\mathsf E$ (certified) |
  |---|---|---|---|
  | 1.55 | 1 | $\approx-0.460$ | $\approx0.5451$ |
  | 1.60 | 1 | $\approx-0.707$ | $\approx0.5488$ |
  | 1.65 | 1 | $\approx-0.903$ | $\approx0.5514$ |

  (cert_a/b/c_r; cert_a/b/c_v_interval negated, e.g. $q_L\in[-0.46031620,-0.46031618]$; cert_a/b/c_entry_interval, both endpoints round to the shown 4 decimals)
  - Each coexists with the no-trade equilibrium (entry $=\rho$); entry strictly ordered upward
  - Elsewhere the numerical search is not exhaustive; the full correspondence is **open**
- **Takeaway:** "Buy fully, sell partially: the path from $r_0$ to $r_1$ has multiplicity, and the talk claims no monotone path."
- **Claim status:** C12 (computer-assisted), C13 (open)
- **Nav:** "Correspondence figure" to A14; "Certificates" to A15
- **Notation introduced:** none new (nodes by value, F11)

### Frame 14 - "The reversal survives four changes in primitives" - 1.5 min [skip if behind]
- **Subtitle:** Entry $\mathsf E$, weak to strong incumbent; each row a separate analytical result (parts (i)-(ii) of Prop. 2)
- **Content:** exhibit X8, a native table:

  | Economy | $\mathsf E$ weak | $\mathsf E$ strong |
  |---|---|---|
  | Benchmark (Laplace noise, two cost atoms) | 0.250 | 0.523 |
  | Atomless costs (half-width 0.1) | 0.250 | 0.523 |
  | Logistic noise | 0.250 | 0.302 |
  | Small value gap ($h=2$, $\ell=1$) | 0.250 | 0.527 |
  | Complementary signals ($a=0.70$, $d=0.75$) | 0.850 | 0.879 |

  Sources: base_entry_weak/strong; cost_halfwidth, cost_mix_laplace_entry_strong (0.522715), weak from tables/extensions.csv (0.25); logistic_entry_strong (0.301509), weak from extensions.csv (0.25); moderate_h, moderate_ell, moderate_entry_weak (0.250000), moderate_entry_strong (0.526805); signal_trader_accuracy_value, signal_buyer_accuracy_value, signal_entry_weak (0.850000), signal_entry_strong (0.879438). Rows 4-5 use their own declared parameter vectors (spoken: not a joint calibration).
  Footnote (small gray, F16): "Signals: declared example. In the 5 x 5 accuracy grid entry rises in the 6 cells meeting Prop. A.7 (analytical), is unchanged in 9, and falls when $d\ge0.76$ (numerical diagnostic)."
- **Takeaway:** "The rise from $r_0$ to $r_1$ does not rest on Laplace noise, cost atoms, a tenfold value gap, or an all-knowing investor."
- **Claim status:** C15, C16 supported (with F16 footnote); the $r_2$ fall is not claimed here (F47)
- **Nav:** "Signal grid" to A16; "Full robustness table" to A17
- **Notation introduced:** $a$, $d$ (in words)

### Frame 15 - "Seeing the price raises proceeds and surplus" - 1.25 min [skip if behind]
- **Subtitle:** Hold the incumbent at $r_1=3$; the challenger either sees the price or does not; trading re-solved in both
- **Content:** exhibit X9, a native table:

  | | Price hidden | Price observed |
  |---|---|---|
  | Entry $\mathsf E$ | 0.250 | 0.523 |
  | Expected target proceeds | 0.614583 | 0.872392 |
  | Net acquisition surplus | 2.302083 | 2.382301 (+0.080218) |

  Sources: base_hidden_entry_strong, base_entry_strong, base_revenue_hidden, base_revenue_feedback, W from tables/equilibrium_controls.csv (2.302083, 2.382301), base_net_surplus_gain.
  - Gray line: "At $r_0$ prices are uninformative, so access changes nothing. The comparison does not rank incumbent strengths or sale mechanisms." (F15)
- **Takeaway:** "Each extra preparation covers its own cost in expectation, so price access adds entry and value. Analytical (Prop. A.9)."
- **Claim status:** C17 supported
- **Nav:** "Price level or information?" to A18; "Reserve comparisons" to A19
- **Notation introduced:** none

### Frame 16 - "Conclusion" - 1.25 min (no navigation)
- **Content:**
  - `\KeyIdea{A stronger incumbent can attract a challenger.}` It makes the target's price \textcolor{cInfo}{informative} about the challenger, and entry rises (0.25 to 0.52 at the benchmark) although the challenger keeps less.
  - **Deterrence is still there:** freeze the information and entry falls.
  - **Implication:** sale terms and rival strength shape the bidder pool through what a winner pays *and* through what the stock price reveals before anyone prepares.
- **Claim status:** C3, C7
- **Nav:** none (hard rule)
- Spoken close: "The next theorem is the seller's: choosing terms with the full price-and-trading continuation retained." (C22, stated as open; not on the slide)

**Main-line density audit.** Text-only frames are 1, 3, 7 and 16 (4 of 16 = 25%, under 30%). Every other frame carries an equation, table, diagram or figure. There is one `ResultBox` in the deck. No frame has more than 2 display equations or more than 7 items, and no frame introduces more than 5 new symbols. Titles are at most 52 characters, which should fit one line at 11 pt 16:9 Madrid (verify in render).

---

## 9. Appendix frames

After `\AppendixStart`. Each backup has one origin and one `\BackButton` to that origin (`main:*` / `app:*` pairs).

| Label | Title | Content sketch | Linked from | Anticipated question |
|---|---|---|---|---|
| A1 `app:interval` | The decision interval | Sale opportunity publicly understood while stock trades and a further bidder can enter (disclosed approach, strategic review, open contest; none automatic). A wholly confidential process does not qualify. Incumbent strength = public distribution, not an announced bid. The paper settles no specific transaction (main.md 33-39) | Frame 1 | "Which deals does this describe? Isn't the process usually confidential?" |
| A2 `app:payoffs` | Acquisition payoffs in closed form | Eq. (4): $t_0,t_H,t_L,g_H,g_L,\Delta_T$ (1 display, aligned) + X13 native table at 1.2 / 3 / 3.6 from tables/auction_primitives.csv (t_0 0.291667 / 0.416667 / 0.430556; t_H 0.704167 / 1.541667 / 1.834722; t_L 0.687500 / 0.875000 / 0.895833; g_H 9.295833 / 8.458333 / 8.165278; g_L 0.312500 / 0.125000 / 0.104167; $\Delta_T$ 0.016667 / 0.666667 / 0.938889; $B_r(1/2)$ 4.804167 / 4.291667 / 4.134722). Analytical | Frame 2 | "Where do the curves come from?" |
| A3 | (reserved; not used) | | | |
| A4 `app:prop1` | Proposition 1 for any incumbent distribution | $R\sim F$ on $[0,\bar r]$, $\ell<\bar r<h$ (in the benchmark $\bar r=r$); an FOSD strengthening weakly raises $\Delta_T(F)=\mathbb E_F[(R-\ell)_+]$ and weakly lowers $g_\theta(F)=\mathbb E_F[(v_\theta-\max\{p,R\})_+]$; strict when the change has positive integral. Proof idea: if $R\le\ell$ both types pay the same; if $R>\ell$ the gap is $(R-\ell)_+$ (main.md 125-137). Analytical | Frame 4 | "Is this a uniform-distribution artifact?" |
| A5 `app:bargaining` | The payment rule sets the sign | X12 (bargaining_spread.pdf). F49 text: "Stronger incumbent: challenger profit falls weakly for every $\eta$. Spread $\Delta_\eta=\eta(h-\ell)+(1-2\eta)\,\mathbb E[(R-\ell)_+]$ rises (weakly) if $\eta<1/2$, falls (weakly) if $\eta>1/2$." Seller gets $t_\eta=(1-\eta)\cdot$runner-up value $+\,\eta\cdot$winner value (F06). Scope: payment-stage only; no entry reversal claimed under bargaining. Analytical (Prop. A.8) | Frame 5 | "Is this special to second-price auctions?" |
| A6 `app:floor` | The low-cost floor is part of the mechanism | Without some entry after any price, target proceeds do not depend on quality, so no informative trading is consistent: nobody prepares and there is nothing to trade on (main.md 235). The floor bounds the investor's edge below by $\rho m\Delta_T$ (eq. 11: $\rho m\Delta_T\le$ edge $\le\Delta_T$). Theorem margin for the floor: 1.37 (base_margin_low_cost) | Frame 6 | "Isn't the cheap-type floor doing all the work?" |
| A7 `app:excluded` | What the model leaves out, and why | Toeholds and free riding (Bulow, Huang and Klemperer 1999; Grossman and Hart 1980); endogenous investor research and manipulation (Goldstein and Guembel 2008); signaling through announced bids (strength is a distribution); tendering and holdout (sale binds all shares); investor cannot bid or acquire. Each is a different model, not a robustness check | Frame 7 | "What about toeholds / manipulation / the incumbent signaling?" |
| A8 `app:equilibrium` | Equilibrium, deviations, and price inversion | Definition (main.md 89). Two comparisons kept apart: a unilateral deviation is evaluated against fixed price and entry schedules; a cross-economy comparison re-solves them. Price sufficiency: $\mu_X=\dfrac{P-t_0-e(P)(t_L-t_0)}{e(P)\Delta_T}$ (1 display), which allows price atoms and entry jumps (Props. A.1, A.2). Analytical | Frame 8 | "How can the challenger know the posterior if it doesn't see order flow?" |
| A9 `app:laplace` | Why Laplace noise, and what logistic changes | X11 (posterior_tail_entry.pdf). Bounded likelihood ratio $e^{-2/b}\le f(x-q)/f(x-q')\le e^{2/b}$ gives $[m,M]$; both laws have $\lvert f'\rvert\le f/b$, so the trading bounds hold for both. Logistic entry at $r_1$ 0.301509 (logistic_entry_strong); threshold $x^*\approx5.42$, about 1.5 noise s.d. from the center (logistic_flow_threshold, logistic_threshold_noise_sd; F38). Same scale, not same variance; not a Blackwell ranking | Frame 9 | "Why this noise law? Isn't the plateau special?" |
| A10 `app:proof` | Proof logic: a global bound pins the orders | Steps: (1) weak economy: any unit earns at most $\Delta_T(r_0)<k$, so every nonzero order loses; posterior = prior; entry = $\rho$. (2) Strong economy: the residual edge is at least $\rho m\Delta_T(r_1)$ under every candidate schedule; $U_\theta(s)=s\,\Pi_\theta(s)-ks$ has $U_\theta'(s)\ge(1-1/b)\rho m\Delta_T-k>0$ on $[0,1]$, so the full correctly signed order dominates every smaller one (global, not first-order; F17). (3) Favorable prices cross $\tau$ with positive probability. (4) Blackwell: a constant kernel maps the strong experiment to the weak one, not conversely. What does the work: step 2 | Frame 10 | "Why unique? Did you assume a candidate profile? Mixed strategies?" |
| A11 `app:conditions` | The three conditions at the benchmark | Condition, formal inequality, theorem margin (F44 "theorem margins"): low-cost floor 1.37 (base_margin_low_cost); high-cost window at the weak prior 1.20 (base_margin_high_prior) and at the best strong price 0.217 (base_margin_high_ceiling); trading-cost window, weak side 3.33e-3 (base_margin_weak_trade), strong side 2.41e-3 (base_margin_strong_trade). Nonempty for every $h>\ell$ by taking $r_0,r_1$ close to $\ell$ (Sec. 5.2; A.4); mathematical nonemptiness, not an effect size. Analytical | Frame 10 | "How robust are the inequalities? Is this a knife edge?" |
| A12 `app:formulas` | Entry and ownership in closed form | Eq. (12) with F09: $\tau$, $x^*=\frac b2\log\frac{\tau}{1-\tau}$, $\alpha_H=1-\tfrac12e^{(x^*-1)/b}$, $\alpha_L=\tfrac12e^{-(x^*+1)/b}$ ("probability that order flow crosses the entry threshold in state $H$/$L$"; F18, F20); $e_\theta=\rho+(1-\rho)\alpha_\theta$, $\mathsf E=(e_H+e_L)/2$, $\mathsf O_H=e_H/2$ (2 displays). $\alpha_H>\alpha_L$: the extra entry tilts to high values. Target proceeds at 1.2 / 3 / 3.6: 0.392708 / 0.872392 / 0.664236 (tables/equilibrium_controls.csv). Analytical | Frame 11 | "Why does high-value ownership rise more than proportionally?" |
| A13 `app:controls` | The information controls in detail | Prop. A.3 (fixed signal, fixed cost law, posterior independent of $r$): entry weakly decreasing in $r$ (analytical). Frozen weak profile: investor deviation gain 1.619e-2 (tables/equilibrium_controls.csv), so it is a control, not an equilibrium; in the strong economy it coincides with the equilibrium profile. Price-hidden rows: unique re-solved equilibria (full orders at $r_1$, entry $\rho$). Applies within fixed orders, not across order profiles that change with $r$ | Frame 12 | "Your frozen profile isn't an equilibrium; why is it the right control?" |
| A14a/b `app:corr` | Trading and entry across incumbent strengths | X10 panel (a) on A14a, panel (b) on A14b (duplicated frames; A14b's Back returns to frame 13, A14a links forward to A14b). F41 annotations: "no trade unique for $r<r_P\approx1.22$; no trade an equilibrium up to $r_N\approx1.75$; full orders unique above $r_U\approx2.84$; high-cost entry impossible above $r_C\approx3.59$" (base_r_pool_unique_sufficient, base_r_no_trade_exact, base_r_full_unique_sufficient, base_r_high_cost_ceiling). Legend keeps "computer-assisted" (black points with interval bars) and "numerical diagnostic" (continuations, broken at unresolved nodes; mixed candidate). "Multiplicity found; search not exhaustive"; the correspondence is open | Frame 13 | "What happens between 1.2 and 3? Is entry monotone?" |
| A15 `app:certs` | How the three equilibria are certified | Interval arithmetic on exact decimals. Low type: global strict concavity, and a sign change of the low type's marginal profit at its own order brackets the root (sign tests e.g. 1.14e-10 / -9.6e-11 at 1.55: cert_a_psi_left_lower, cert_a_psi_right_upper). High type: high-type cover margin positive over the whole bracket, 7.62e-5, 2.75e-3, 5.49e-3 (cert_a/b/c_high_derivative_lower). Full intervals for $q_L$ and $\mathsf E$ from cert_*_v_interval (negated) and cert_*_entry_interval. Not proved: uniqueness of the informative profile, absence of mixed equilibria, a continuous branch. Computer-assisted | Frame 13 | "What exactly is proved by computer?" |
| A16 `app:signals` | Complementary signals: the full accuracy grid | X14: rises 2.81-3.09 pp in the 6 cells meeting Prop. A.7 (analytical); unchanged in 9 cells with $d\le0.75$; falls 4.03-4.49 pp in all 10 cells with $d\ge0.76$, where the challenger's own good signal already triggers expensive entry against the weak incumbent (numerical diagnostic) (tables/table_signal_grid.tex). The price matters when the challenger's own signal is informative but not decisive. Other inputs: $\rho=0.85$, $c_H=7.14$, $k=0.015$, $r=1.1$ vs 2.3 (signal_*) | Frame 14 | "What if the challenger knows more than the investor?" |
| A17 `app:robust` | Robustness: full table | Table 3 rebuilt natively: $\mathsf E$ weak / strong / $\Delta\mathsf E$ (pp) / $\mathsf O_H$ weak / strong for the six rows (tables/extensions.csv; registry: base_entry_change_pp 27.28, moderate_entry_change_pp 27.68, signal_entry_change_pp 2.94; atomless logistic 0.301374 cost_mix_logistic_entry_strong). Minimum theorem margins: base 2.41e-3, moderate 8.01e-4, signal 1.45e-3 (base/moderate/signal_minimum_theorem_margin). Note (F47): the $r_2$ fall is shown for the benchmark only | Frame 14 | "Are these the same parameters? How close to the boundary?" |
| A18 `app:dividend` | Price level or information? | F10 text: "Invariance diagnostic: add a dividend $D_0=0.257809$ (the revenue gain from price access; base_matched_dividend, base_revenue_gain) to the traded claim in the price-hidden economy. Mean prices then match, but entry does not, so the information matters, not the price level." Tag: diagnostic; the revenue gain itself is analytical. Not a feasible mechanism; excluded from surplus | Frame 15 | "Isn't this just a higher price level attracting entry?" |
| A19 `app:reserve` | Sale terms: a higher reserve can help | X15 (value classes, half-width 0.05, $p=0.5$ vs $p=1.1$): weak proceeds 0.392665 to 0.432173, strong 0.872367 to 1.014500; preparation at $p=1.1$: 0.540309 (weak), 0.511638 (strong) (value_* keys). Note: "Binary values: $p=0.5$ vs $p=1.01$" (tables/reserve_comparisons.csv; no registry key, F39). The alternative sits just above $\ell=1$ and excludes the low-value challenger; preparation, sale and two admissible bidders separate (Table 4). A feasible improvement, not an optimal reserve; optimal terms open. Button to A20 | Frame 15 | "What should the seller do? Optimal reserve?" |
| A20 `app:pool` | Same orders, different prices | Prop. A.10 (F32): at reserve 7 (pool_reserve) under full orders, prices pool below a cutoff (words, F03). Pooled posterior 0.272979 vs 0.303265, preparation 0.151805 vs 0.125000, proceeds 0.687364 vs 0.609643 (pool_* keys). "Same orders, different prices, beliefs, and entry": a continuation must include the price rule. Existence only; does not arise on the benchmark support. Back returns to A19 | A19 | "Why can't you just solve for the seller's optimal reserve?" |
| A21 `app:refs` | References | Fishman (1988, RAND J. Econ.); Hirshleifer and Png (1989, RFS); Levin and Smith (1994, AER); Dow, Goldstein and Guembel (2017, JEEA); Edmans, Goldstein and Jiang (2015, AER); Goldstein and Guembel (2008, REStud); plus the primary paper. One gray positioning line: the increment is the opposition of the two returns under a sale rule and the participation reversal. Metadata checked against references.bib | Frame 3 | "How does this differ from feedback-effect models?" |
| A22 `app:evidence` | Empirical implications (design only) | Outcome: start of substantive diligence or a costly proposal, not counts of offers. Strength measured from information public before the decision. Prices must precede preparation; later returns can reflect anticipated arrival. Pilot (Online App. D) reconstructs chronologies from disclosure records; design only, no sample, no identification strategy (main.md 396-398) | Frame 3 | "Is there evidence? How would you test it?" |
| A23 `app:notation` | Notation | Native 2-column table: every main-line symbol from Section 6 with its gloss, in introduction order | Frame 7 | "What was $\tau$ / $m$ again?" |

(Label A3 is unused so that A-numbers match main-frame order; the rendered appendix numbering is whatever `\AppendixStart` assigns. A23 (notation) is placed just before A21 (References) in the build. A14 is two duplicated frames.)

---

## 10. Timing table

| Frame | Title | Min | Cumulative |
|---|---|---|---|
| 0 | Title | 0.25 | 0.25 |
| 1 | Does a stronger incumbent deter a challenger? | 1.25 | 1.50 |
| 2 | One auction, two claims, opposite responses | 2.50 | 4.00 |
| 3 | This paper | 1.75 | 5.75 |
| 4 | Force 1, deterrence: the challenger keeps less | 1.75 | 7.50 |
| 5 | Force 2, information: informed trading pays more | 2.25 | 9.75 |
| 6 | Which force wins depends on what the price reveals | 1.50 | 11.25 |
| 7 | Model: four roles around one public sale | 1.75 | 13.00 |
| 8 | Timing: the price arrives before the entry decision | 1.75 | 14.75 |
| 9 | Only good news makes expensive preparation pay | 2.50 | 17.25 |
| 10 | Proposition 2: a stronger incumbent raises entry | 3.50 | 20.75 |
| 11 | Benchmark: entry rises from 0.25 to 0.52 | 2.00 | 22.75 |
| 12 | Freeze the information and deterrence returns | 2.50 | 25.25 |
| 13 | Between the two economies, equilibria coexist | 1.50 | 26.75 |
| 14 | The reversal survives four changes in primitives | 1.50 | 28.25 |
| 15 | Seeing the price raises proceeds and surplus | 1.25 | 29.50 |
| 16 | Conclusion | 1.25 | 30.75 |
| | Question reserve | 9.25 | 40.00 |

- **Punchline:** the answer is spoken on frame 2 at about 3.5 min. The headline number is on screen at the start of frame 3, about 4.0-4.5 min. The model is on screen by 11.25 min and the theorem by 17.25 min.
- **Checkpoints:** start frame 7 by 12.5 min, start frame 10 by 18.5 min, start frame 12 by 24 min.
- **If behind (cut in this order; each becomes one spoken sentence, and the frame stays in the deck):**
  1. Frame 15 (welfare): "Price access raises proceeds and surplus at $r_1$." Saves 1.25 min.
  2. Frame 13 (coexistence): "Between the two economies equilibria coexist; I certify three by computer; the full map is open." Saves 1.25 min.
  3. Frame 14 (robustness): "Survives logistic noise, atomless costs, a small value gap and a better-informed challenger." Saves 1.25 min.
  4. Compress frames 7-8 to 2 min together by reading the timeline only. Saves 1.5 min.
  5. Compress frame 6 to 0.5 min (read the chain line only). Saves 1 min.
  Frames 2, 3, 9, 10, 11, 12 and 16 are never cut.
- **If ahead:** open A10 (proof logic) from frame 10 or A14 (correspondence) from frame 13.

---

## 11. Anticipated questions (job-market audience)

| # | Question | Answer route |
|---|---|---|
| Q1 | How is this different from feedback-effect models (Dow-Goldstein-Guembel)? | Spoken: the sale rule splits one surplus into a traded claim and the entrant's claim, and competition moves them in opposite directions; the reversal in entry is the increment. A21 |
| Q2 | Why can't the challenger bid without preparing? | Spoken: preparation (diligence, financing, verification) is required for an executable bid; declining means staying out. A1 |
| Q3 | Is this special to second-price auctions? | A5: under bargaining the sign of the spread effect flips at seller weight 1/2; no entry reversal is claimed there |
| Q4 | Isn't the cheap-type floor doing all the work? | A6: without it no informative trading is consistent; it is part of the mechanism. The floor alone gives entry $\rho$ at every strength (price-hidden row, frame 12) |
| Q5 | Why Laplace noise? | A9: bounded likelihood ratio; logistic gives the same trading bounds, lower entry (0.302) |
| Q6 | The investor knows the challenger's value better than the challenger. Realistic? | Frame 14 row 5 and A16: the reversal holds with a more accurate challenger signal (0.75 vs 0.70) where the conditions hold; falls when $d\ge0.76$ |
| Q7 | Is this mispricing? Are prices rational? | Spoken + A8: market makers price anticipated entry; the investor keeps only the residual edge from noise |
| Q8 | Uniqueness: did you assume the order profile? Mixed strategies? | A10: a global bound on marginal profit; arbitrary mixed orders, every unilateral deviation $q\in[-1,1]$ |
| Q9 | What happens between the two strengths? Is entry monotone in strength? | Frame 13, A14: coexistence at three certified strengths; entry falls back at 3.6; full correspondence open |
| Q10 | Which equilibrium do you select? | Spoken: none; each certified branch is reported, and no monotone path is read into the gaps. A15 |
| Q11 | +27 pp seems large. Is the benchmark calibrated? | Spoken: declared parameters, not a calibration; the moderate-value row (h = 2) gives a similar rise (0.250 to 0.527); nonemptiness holds for every $h>\ell$, not an effect-size claim (A11) |
| Q12 | Should a seller want a strong incumbent? Welfare? | Frame 15, A18: at fixed strength price access helps; the paper does not rank strengths or mechanisms |
| Q13 | What is the optimal reserve? | A19-A20: a higher reserve can help at listed nodes; optimal terms are open because continuations include price rules |
| Q14 | Could the investor or incumbent manipulate the price to deter the challenger? | A7: endogenous research and manipulation are excluded (Goldstein-Guembel 2008); the investor cannot bid |
| Q15 | Toeholds, free riding, tendering? | A7: excluded; the sale binds all shares |
| Q16 | Is incumbent strength a signal the incumbent chooses? | Spoken + A1: strength is the public distribution of its value, not an announced bid; signaling is outside the paper |
| Q17 | What is the trading cost $k$, and why is it needed? | Spoken: an execution or carrying friction separate from price impact; it creates the trading-cost window. A11 margins |
| Q18 | The frozen control is not an equilibrium; why is it informative? | A13: it isolates deterrence at fixed information; the analytical sign is Prop. A.3; the price-hidden economy is a true equilibrium comparison |
| Q19 | Does the fall at $r_2$ survive the extensions? | Spoken: shown at the benchmark and nearby; not claimed under the extensions (the atomless-cost row of tables/equilibrium_controls.csv reports entry 0.376680 at 3.6, so the fall is benchmark-specific) |
| Q20 | Is there evidence? Which deals? | A22 and A1: design only; the paper settles no specific transaction |
| Q21 | Why must the price come before preparation? | Frame 8 + spoken: if preparation precedes trading there is nothing to learn; hiding the price gives entry 0.25 at both strengths (frame 12) |
| Q22 | Why does high-value ownership rise more than entry? | A12: $\alpha_H>\alpha_L$, so the extra entry tilts toward high values |
