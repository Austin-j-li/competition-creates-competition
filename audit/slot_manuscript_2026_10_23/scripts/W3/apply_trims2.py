"""Second trim pass on comparison.tex: shorter sentences, split paragraphs, fewer lines. Prints misses."""
import pathlib
root = pathlib.Path(__file__).resolve().parents[4]
src = root/'overleaf/competition_slot/comparison.tex'
t = src.read_text()
reps = [
# intro paragraph 2: split
(r"""Section~\ref{sec:decisions} lists decision points. The Laplace manuscript is the version of 22 October 2026
(main text, Appendix A and the Online Appendix).""",
r"""Section~\ref{sec:decisions} lists decision points.

The Laplace manuscript is the version of 22 October 2026 (main text, Appendix A and the Online Appendix)."""),
# §1 slot timing: shorten
(r"""\paragraph{Timing.} As in the Laplace set-up, with one change at the trading date. The slot draw selects the
investor with probability \(\lambda\) and a liquidity trader otherwise, and the selected trader places its
order. Section 5 of the slot manuscript adds a research stage before this date.""",
r"""\paragraph{Timing.} As in the Laplace set-up, except that at the trading date the slot draw selects the trader
who places the order. Section 5 of the slot manuscript adds a research stage before this date."""),
# Table 1: drop the knob row
(r"""Knob & \(b\) & \(u\) (sets \(M\)); \(\beta\) (sets how often the slot trades)\\
""", ""),
# Results table cells
(r"""Computer-assisted at three nodes. No trade exists exactly up to \(r_N=\reg{lap_rN}\); full orders are unique above \(r_U=\reg{lap_rU}\). The branch between the nodes is a numerical diagnostic; the full correspondence is open.""",
r"""Computer-assisted at three nodes; the branch between them is a numerical diagnostic, and the full correspondence is open."""),
(r"""Section 5: zero research unique at \(r_0\); a research branch on \([\reg{res_rR},\reg{res_rcap})\) with research \(\reg{res_lambda_r155}<\reg{res_lambda_r160}<\reg{res_lambda_r165}\) and entry \(\reg{res_entry_r155}<\reg{res_entry_r160}<\reg{res_entry_r165}\) at \(1.55\), \(1.60\), \(1.65\), beside zero research; research at the cap unique at \(r_1\) and \(r_2\). Branch slope analytical; lists and values computer-assisted.""",
r"""Section 5: zero research unique at \(r_0\); a research branch on \([\reg{res_rR},\reg{res_rcap})\) with entry \(\reg{res_entry_r155}<\reg{res_entry_r160}<\reg{res_entry_r165}\) at \(1.55\), \(1.60\), \(1.65\), beside zero research; research at the cap unique at \(r_1\) and \(r_2\). Slope analytical; lists and values computer-assisted."""),
(r"""Section 6.3: the same vector, \(\reg{p4_s_signal_r0_entry}\to\reg{p4_s_signal_r1_entry}\); at the benchmark, accuracies \((\reg{sig_comp_aT},\reg{sig_comp_d})\) give \(\reg{p4_comp_b_r0_entry}\to\reg{p4_comp_b_r1_entry}\), and \reg{p4_comp_b_no_y_r1_entry} without the challenger's signal. Analytical; values computer-assisted.""",
r"""Section 6.3: the same vector, \(\reg{p4_s_signal_r0_entry}\to\reg{p4_s_signal_r1_entry}\); at the benchmark, accuracies \((\reg{sig_comp_aT},\reg{sig_comp_d})\) give \(\reg{p4_comp_b_r0_entry}\to\reg{p4_comp_b_r1_entry}\), with no rise when the challenger's signal is removed. Analytical; values computer-assisted."""),
# §2 "Three facts" paragraph: split
(r"""Second, the slot replaces three
certified points with a complete equilibrium set. It adds research, coexistence at every prior and derived
observables. Third,""",
r"""Second, the slot replaces three
certified points with a complete equilibrium set. It adds research, coexistence at every prior and derived
observables.

Third,"""),
# §3 coexistence five forms sentence
(r"""The high class uses one of five forms: no trade, a mixed purchase that
recruits, a full purchase, mixed orders at the entry floor, or the threshold pair.""",
r"""The high class uses one of five forms. These are no trade, a mixed purchase that
recruits, a full purchase, mixed orders at the entry floor, and the threshold pair."""),
# §3 research: shorten
(r"""The marginal
cost rises and the research value falls, so they meet once, and the research response moves smoothly with
strength. The benchmark cap sits \reg{margin_lambda_hi_B} below the top of the admissible strip, the same
boundary as the return margin at \(r_2\) in another coordinate. The equilibrium set with research on
\((r_N,r_U^R)=(\reg{res_rN},\reg{res_rUR})\) is open.""",
r"""The marginal
cost rises and the research value falls, so they meet once, and the research response moves smoothly with
strength. The equilibrium set with research on \((r_N,r_U^R)=(\reg{res_rN},\reg{res_rUR})\) is open."""),
# §3 timing: split long sentences
(r"""An exploratory extension with
several slots, outside both manuscripts, keeps the posterior bound and the return to the floor at \(r_2\) for
every finite number of slots; its complete equilibrium list is open. In both set-ups the ceiling \(r_C\) is a
tie event with positive probability, so entry is discontinuous in strength there and the challenger's tie rule
decides entry at \(r_C\) itself.""",
r"""An exploratory extension with
several slots lies outside both manuscripts. It keeps the posterior bound and the return to the floor at
\(r_2\) for every finite number of slots, and its complete equilibrium list is open. In both set-ups the
ceiling \(r_C\) is a tie event with positive probability. Entry is therefore discontinuous in strength there,
and the challenger's tie rule decides entry at \(r_C\) itself."""),
# §3 uniqueness paragraph
(r"""The slot proves uniqueness against three orders and lists the whole
set along the path, with the dependence on the two tie rules in one table (Section 4.3). Three statements depend
on the rules. The strict rise on \([r_A,r_F]\) needs IM; the threshold pair and the entry interval at \(r_C\)
exist only under CM; under I0 the set is empty on \((r_N,r_S]\).""",
r"""The slot proves uniqueness against three orders and lists the whole
set along the path. One table gives the dependence on the two tie rules (Section 4.3). Three statements depend
on the rules. The strict rise on \([r_A,r_F]\) needs IM. The threshold pair and the entry interval at \(r_C\)
exist only under CM. Under I0 the set is empty on \((r_N,r_S]\)."""),
# §3 admissible region: shorten
(r"""The Laplace manuscript asserts that its region is open
and prints prior windows; it does not print the part (iii) margin \(c_H-B_{r_2}(M)=\reg{lap_return_cost}\). The
slot manuscript states the region as an exact band in \(u\) with a table of margins. In the slot the thin margin
appears in five coordinates that measure one distance.""",
r"""The Laplace manuscript asserts that its region is open
and prints prior windows; it does not print the part (iii) margin. The slot manuscript states the region as an
exact band in \(u\) with a table of margins. In the slot the thin margin appears in five coordinates that
measure one distance."""),
# §3 assumptions: shorten
(r"""The Laplace set-up assumes a continuous order, a Laplace law with \(b>1\) and the score bound; Proposition A.5
extends it to every bounded-score density. The slot assumes a unit menu, a presence probability and an exogenous
liquidity motive. An uninformed trader with the model's own trade payoff would not fill the slot. With research
the slot adds a quadratic cost and a cap inside the admissible strip. Neither set-up needs an off-path belief.""",
r"""The Laplace set-up assumes a continuous order and a Laplace law with \(b>1\); Proposition A.5 extends it to
every bounded-score density. The slot assumes a unit menu, a presence probability and an exogenous liquidity
motive; with research it adds a quadratic cost and a cap. Neither set-up needs an off-path belief."""),
# §4.1 tuple sentence split
(r"""The tuple lists the order distribution of
each class, the posterior and the price after every order or flow, the challenger's belief at every price on
the image, the entry rule at every price and cost, and the bids.""",
r"""The tuple lists the order distribution of
each class and the posterior and price after every order or flow. It also lists the challenger's belief at
every price on the image, the entry rule at every price and cost, and the bids."""),
# §4.2 split paragraph
(r"""A lemma whose premises include the conditions under proof cannot supply that step. The
second shortcut""",
r"""A lemma whose premises include the conditions under proof cannot supply that step.

The second shortcut"""),
# §4.3 split paragraph
(r"""It needs the posterior bound at every flow or order, which in the slot is the
zero-order bound and \(\beta\le1/3\). The orders-first route""",
r"""It needs the posterior bound at every flow or order, which in the slot is the
zero-order bound and \(\beta\le1/3\).

The orders-first route"""),
# §4.4 trim last sentence
(r""" A result that holds on an
open set survives a perturbation of every primitive at once, with a radius that the margins bound.""",
r""" A result on an open set
survives a joint perturbation of the primitives, with a radius that the margins bound."""),
# §4.6 Part 3 and Part 4: blank lines between blocks
(r"""and \(A_L=\rho\DT\mu^*\), both in \([\rho\kappa\DT,\DT]\).}
\lap{For a correctly signed order""",
r"""and \(A_L=\rho\DT\mu^*\), both in \([\rho\kappa\DT,\DT]\).}

\lap{For a correctly signed order"""),
(r"""lie in \([\rho\kappa\DT,\DT]\).}
\lap{Step 4:""",
r"""lie in \([\rho\kappa\DT,\DT]\).}

\lap{Step 4:"""),
(r"""(L3) is the one new hypothesis of part (iii).}
\slo{Structural:""",
r"""(L3) is the one new hypothesis of part (iii).}

\slo{Structural:"""),
# §5 Laplace thresholds item
(r"""\item the thresholds \(\fr(k)\), \(r_N\), \(r_U\) and \(r_C\) are closed forms evaluated in binary floats, with
  two float neighbours recorded as bounds; they are analytical formulas without a certificate;""",
r"""\item the thresholds \(\fr(k)\), \(r_N\), \(r_U\) and \(r_C\) are closed forms in binary floats, with two
  float neighbours as bounds, and have no certificate;"""),
# §5 thin margins paragraph: split
(r"""The moderate-value vector has a trade margin of
\reg{lap_moderate_A2_upper}. In the slot""",
r"""The moderate-value vector has a trade margin of
\reg{lap_moderate_A2_upper}.

In the slot"""),
# §6 shorten items 1 and 2
(r"""The Laplace set-up keeps the partial sale and three certified
  nodes with a strict rise on a continuum. The slot keeps a complete equilibrium set, research, coexistence at
  every prior and derived observables. Its price is an exogenous liquidity motive and a unit menu. The two can
  also be nested: one as the model, the other as a remark or an appendix.""",
r"""The Laplace set-up keeps the partial sale and three certified
  nodes with a strict rise. The slot keeps a complete equilibrium set, research, coexistence at every prior and
  derived observables, at the price of an exogenous liquidity motive and a unit menu. The two can also be
  nested: one as the model, the other as a remark or an appendix."""),
]
missing = []
for old, new in reps:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        missing.append(old[:80])
src.write_text(t)
print("replacements:", len(reps) - len(missing), "missing:", len(missing))
for m in missing:
    print("  MISSING:", m)
