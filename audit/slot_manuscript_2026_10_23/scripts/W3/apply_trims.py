"""Replace Section 3 of comparison.tex with sec3_new.tex and apply a list of exact text replacements.
Prints the replacements that did not match."""
import pathlib
root = pathlib.Path(__file__).resolve().parents[4]
src = root/'overleaf/competition_slot/comparison.tex'
new3 = (root/'audit/slot_manuscript_2026_10_23/scripts/W3/sec3_new.tex').read_text()
t = src.read_text()
a = t.index('%==========================================================================================\n\\section{Trade-offs}')
b = t.index('%==========================================================================================\n\\section{The proof method}')
t = t[:a] + new3 + t[b:]
reps = [
(r"\centering\small" + "\n" + r"\caption{The two set-ups.}", r"\centering\footnotesize" + "\n" + r"\caption{The two set-ups.}"),
(r"""Benchmark & \(b=\reg{lap_b}\) & \(1+u=\eu\), \(\beta=\reg{beta_B}\), \(\lambda=\reg{lambda_B}\)\\
\(M(1/2)\) & \reg{lap_M_half} & \reg{M_half_B}\\
Entry at \(r_0,r_1,r_2\) & \reg{entry_r0}, \reg{lap_entry_r1}, \reg{entry_r2} & \reg{entry_r0}, \reg{entry_r1_B}, \reg{entry_r2}\\
\(\Own_H\) at \(r_1\) & \reg{lap_own_r1} & \reg{own_r1_B}\\
""", r"""Benchmark & \(b=\reg{lap_b}\), \(M(1/2)=\reg{lap_M_half}\) & \(1+u=\eu\), \(\beta=\reg{beta_B}\), \(M(1/2)=\reg{M_half_B}\)\\
"""),
(r"""Benchmark entry & \(\reg{entry_r0}\to\reg{lap_entry_r1}\to\reg{entry_r2}\); ownership \(\reg{own_r0}\to\reg{lap_own_r1}\). Analytical (closed forms). & \(\reg{entry_r0}\to\reg{entry_r1_B}\to\reg{entry_r2}\); ownership \(\reg{own_r0}\to\reg{own_r1_B}\). Computer-assisted (interval enclosures).\\
""", ""),
(r"""Noise and order menu & Proposition A.5: the reversal for every bounded-score density; logistic entry \reg{lap_logistic_entry}. Analytical. & Section 6.4, one remark: continuous order sizes need a convention for unused sizes; Laplace noise with \(1+u=\eu^{2/s}\) gives the same top posterior.\\
""", ""),
(r"""Payment rule & Proposition A.8: the spread response has the sign of \(1-2\omega\). Analytical. & Section 7.2: weakly the sign of \(1-2\omega\), strictly when \(\E[(R-\ell)_+]\) changes strictly. Analytical.\\
""", r"""Payment rule & Proposition A.8: the spread response has the sign of \(1-2\omega\). Analytical. & Section 7.2: the same, weakly; strictly when \(\E[(R-\ell)_+]\) changes strictly. Analytical.\\
"""),
(r"""Where a margin concerns the auction alone, it is the same number: the cost window
\((\reg{lap_cH_lo},\reg{lap_cH_hi})\) and the three-part prior window \((\reg{prior_lo_B},\reg{prior_hi_B})\)
are identical, because calibration B gives the slot the Laplace top posterior.""",
r"""Calibration B gives the slot the Laplace top posterior, so every margin that concerns the auction alone is the
same number. The cost window \((\reg{lap_cH_lo},\reg{lap_cH_hi})\) and the three-part prior window
\((\reg{prior_lo_B},\reg{prior_hi_B})\) are identical."""),
(r"""The proof starts from the equilibrium written out as one tuple:
\begin{itemize}[leftmargin=2em,itemsep=0pt]
\item the class-contingent order distributions;
\item the posterior after every order or flow;
\item the price function on every order or flow;
\item the challenger's belief at every price on the image;
\item the entry rule at every price and cost;
\item the bids.
\end{itemize}
The tuple is a proof artifact.""",
r"""The proof starts from the equilibrium written out as one tuple. The tuple lists the order distribution of
each class, the posterior and the price after every order or flow, the challenger's belief at every price on
the image, the entry rule at every price and cost, and the bids. The tuple is a proof artifact."""),
(r"""Under every strategy the posterior after every flow or
order lies in \([m(\pi),M(\pi)]\): from the score bound in the Laplace set-up, from the liquidity floor in the
slot.""",
r"""Under every strategy the posterior after every flow or
order lies in \([m(\pi),M(\pi)]\). The score bound gives this in the Laplace set-up, the liquidity floor in the
slot."""),
(r"""The exclusion margin, its posterior form and the position of \(r_2\) above the
ceiling are the same numbers in both set-ups, because \(M\) is the same.""",
r"""Because \(M\) is the same, the exclusion margin, its posterior form and the position of \(r_2\) above the
ceiling coincide."""),
(r"""Neither tie rule is used at \(r_2\): \(g_L(r_2)>0\) makes
the zero-cost decision strict, the exclusion margin makes the high-cost decision strict, and both investor
comparisons are strict.""",
r"""Neither tie rule is used at \(r_2\). The zero-cost decision is strict because \(g_L(r_2)>0\), the high-cost
decision is strict by the exclusion margin, and both investor comparisons are strict."""),
(r"""The five-part form adds five things: the displayed
tuple, the observation that Step 2 needs no price inversion, the wrong-sign line for class \(L\), the separation
of structural from strict hypotheses, and the margins table.""",
r"""The five-part form adds the displayed tuple and the margins table. It also adds the observation that Step 2
needs no price inversion, the wrong-sign line for class \(L\), and the separation of structural from strict
hypotheses."""),
(r"""\item the thresholds \(\fr(k)\), \(r_N\), \(r_U\) and \(r_C\) are closed forms evaluated in binary floats, with
  two float neighbours recorded as bounds, so they are analytical formulas without a certificate;""",
r"""\item the thresholds \(\fr(k)\), \(r_N\), \(r_U\) and \(r_C\) are closed forms evaluated in binary floats, with
  two float neighbours recorded as bounds; they are analytical formulas without a certificate;"""),
(r"""An independent
check of each package confirmed every core theorem: the posterior bounds; the three outcomes of Proposition 2
under all four tie-rule pairs; the complete equilibrium set on the path; the research results at six strengths;
the information controls; the cost and class extensions; the observables.""",
r"""An independent
check of each package confirmed every core theorem. These are the posterior bounds, the three outcomes of
Proposition 2 under all four tie-rule pairs, and the complete equilibrium set on the path. They also include the
research results at six strengths, the information controls, the cost and class extensions, and the
observables."""),
(r"""In the Laplace
manuscript the strong-trade margin, \reg{lap_margin_A2_upper}, is smaller than the return margin in the same
units, so the return margin is not the thinnest.""",
r"""In the Laplace
manuscript the strong-trade margin, \reg{lap_margin_A2_upper}, is smaller than the return margin in the same
units. The return margin is therefore not the thinnest."""),
(r"""\item \textbf{The fixed-information control and reserve deterrence.} ``Falls strictly'' and strict deterrence at
  the exclusion reserve hold in the Laplace set-up. ``Does not rise'' and flat entry at that reserve hold in the
  slot, with strict deterrence at \reg{rsv_deter}. Each statement is exact in its set-up.""",
r"""\item \textbf{The fixed-information control and reserve deterrence.} The Laplace set-up supports ``falls
  strictly'' and strict deterrence at the exclusion reserve. The slot supports ``does not rise'' and flat entry at
  that reserve, with strict deterrence at \reg{rsv_deter}. Each statement is exact in its set-up."""),
(r"""Slot: the set with research on \((r_N,r_U^R)\); the selection
  between the two outcomes on \([r_A,r_N]\); the seller's reserve with the full continuation; the trading game
  under the bargaining rule.""",
r"""Slot: the set with research on \((r_N,r_U^R)\), and the selection
  between the two outcomes on \([r_A,r_N]\). Both: the seller's reserve with the full continuation, and the
  trading game under the bargaining rule."""),
]
missing = []
for old, new in reps:
    if old in t:
        t = t.replace(old, new, 1)
    else:
        missing.append(old[:70])
src.write_text(t)
print("replacements:", len(reps) - len(missing), "missing:", len(missing))
for m in missing:
    print("  MISSING:", m)
