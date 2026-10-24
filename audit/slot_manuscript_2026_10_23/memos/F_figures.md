# F_figures: the three figures and their slide versions

Workstream F, 23 October 2026. Script: `scripts/F_figures/make_figures.py`. Run log with the boundary values and the
SHA-256 of each PDF: `scripts/F_figures/run_log.txt`. PNG previews: `scripts/F_figures/png/`.
Output: six vector PDFs in `overleaf/competition_slot/figures/`. No `.tex` file changed.

Every curve is computed from the closed forms of `proofs/P1_core.tex` (Proposition 3, Step 7; Definition of the
thresholds) and `proofs/P3_research.tex` (equations (F), (lamE), (phi); Propositions on the branch and on strong
incumbents) at calibration B. Boundaries use mpmath at 40 digits. The log prints each boundary and each number beside
its registry display value. All 9 boundaries and 25 further values match at display precision.

## 1. Files

| Label | Manuscript file | Size (pt) | Slide file | Size (pt) |
|---|---|---|---|---|
| `fig:beliefs` | `figures/beliefs.pdf` | 468 × 219.6 | `figures/beliefs_talk.pdf` | 532.8 × 223.2 |
| `fig:coexistence` | `figures/coexistence.pdf` | 468 × 424.8 | `figures/coexistence_talk.pdf` | 547.2 × 237.6 |
| `fig:research` | `figures/research.pdf` | 468 × 396 | `figures/research_talk.pdf` | 532.8 × 223.2 |

The manuscript width is 468 pt, which equals the text width with 1 in margins on letter paper. Include each figure at
`width=\linewidth`.

The slide figures have an aspect ratio of 2.3 or more, so that each fits a 16:9 moloch frame with a frame title. In
the deck's preamble, `\textheight` is 243.5 pt and `\linewidth` is 433.3 pt. At `width=\linewidth` the heights are
181 pt (beliefs), 188 pt (coexistence) and 181 pt (research). Include each slide figure with
`\includegraphics[width=\linewidth,height=0.8\textheight,keepaspectratio]{...}`.

## 2. Boundaries used (registry match: all yes)

| Symbol | Value | Registry key |
|---|---|---|
| r_A | 1.393958 | `rA` |
| r_F | 1.467127 | `rF_B` |
| r_N | 1.747878 | `rN` |
| r_J | 1.966097 | `rJ` |
| r_S | 2.124148 | `rS_B` |
| r_C | 3.592659 | `rC_B` |
| r_R | 1.501023 | `res_rR` |
| r̄_R | 1.677633 | `res_rcap` |
| r_U | 2.434046 | `res_rUR` |

Numbers printed inside the figures come from these registry keys: `M_half_B`, `m_half_B`, `tau_r1`, `tau_r2`, `rC_B`
(beliefs); `res_cap` (research); `res_entry_rR`, `res_entry_cap` (research, slide version). The coexistence figures
print symbols only.

## 3. Conventions in all figures

- Colour and line style together: navy solid for no trade and zero research; brick dashed for the interior branch
  (R, research branch); brick solid for the corner branch (F, cap); gray dash-dot for Q; thin black dashes for T.
  A grayscale render keeps every branch distinguishable.
- A filled marker means the branch attains the value at that strength. An open marker means the branch approaches the
  value and does not attain it, or the proposition does not claim it. No line crosses a gap.
- Black dots mark the nodes of the proofs. In the research figure these are r_0, 1.55, 1.60, 1.65, r_1 = 3 and
  r_2 = 3.6 (the six strengths of P3).
- Dotted vertical lines mark the boundaries. Gray shading marks the strengths with no result (research figure).
  Blue shading marks coexistence (coexistence figure) and the band for M (beliefs figure).
- Fonts: manuscript figures use STIX text and STIX math. Slide figures use Fira Sans text and Computer Modern math.
  `pdffonts` shows only TrueType rows (Type 42) in all six files and no Type 3 row. Fira Sans ships as CFF
  OpenType. The script converts its outlines to TrueType with fontTools (error bound 1 font unit), because the
  direct embedding of CFF produces a poppler warning ("Mismatch between font type and embedded font file").
- The PDFs omit the creation date. Two runs give identical SHA-256 values.

## 4. What each figure shows

### `fig:beliefs`

- (a) The threshold τ(r) on [1.2, 3.6], rising from 0.633117 at r_0 to 0.731392 at r_2. Horizontal lines mark the
  prior 1/2, the top posterior M(1/2) = 0.731059 and the bottom posterior m(1/2) = 0.268941. The gray band between
  m and M holds every posterior that an investor strategy can produce. The strengths r_0, r_1, r_2 are marked, and the
  ceiling r_C is the open circle where τ meets M.
- (b) The same curve on [r_1, r_2] with the vertical axis from 0.700 to 0.735. The blue band spans τ(r_1) = 0.705000
  to τ(r_2) = 0.731392. This is the band for M(1/2) in which r_C lies between r_1 and r_2. The line at M(1/2) of
  calibration B sits 0.000334 below the upper edge. The curve meets it at r_C.
- Layout choice: the zoom is a narrow second panel, because r_C and r_2 differ by 0.007341 and would overlap in (a).

### `fig:coexistence`

- (a) Entry against r on [1.2, 3.6] for all branches at prior 1/2 under rules IM and C1: N (0.25 up to r_N), R (rises
  from 0.454185 at r_A to 0.522757 at r_F), F (0.522757 up to r_C, then the floor 0.25), Q (0.25 on (r_N, r_J), open at
  both ends) and T under CM (thin dashes, from 0.454185 at r_A down to 0.25 at r_J). The shaded interval is
  [r_A, r_N].
- (b) The strengths 1.25 to 2.35, where every boundary but r_C lies. It marks r_A, r_F, r_N, r_J, r_S. Labels above
  the F line give the low class's behaviour: F with abstention (full purchase), F with mixed sales, F with full sales
  (full trade) from r_S. Entry on F is the same in the three parts. The change of the low class at r_S is visible
  only in the label.
- Layout choice: two panels, because the strengths from r_A to r_S use 30% of the axis in a single panel and the
  labels would overlap.

### `fig:research`

- (a) Research intensity λ. Zero research on [r_0, r_N]. The research branch on [r_R, r̄_R) rises from 0.193853 to the
  cap λ̄ = 0.336122. Research at the cap from r̄_R to r_N (open at r_N) and from r_U (open) to 3.6.
- (b) Entry E. Zero research gives 0.25. The branch rises from 0.500846 to 0.522757. At the cap, entry is 0.522757
  up to r_C and 0.25 above r_C. An inset enlarges the rise along the branch (0.4985 to 0.5260). The black node at
  r_2 = 3.6 lies 0.007 to the right of the open marker at r_C and covers most of it.
- The horizontal axis is broken: [1.2, 2.0] on the left, [2.4, 3.6] on the right. The branch spans 0.177 of
  the 0.8 units on the left, so the broken axis keeps it readable.
- The gray bands from r_N to r_U show strengths where P3 proves no claim. The cap line stops at r_N and restarts at
  r_U. No line crosses the band.
- Slide version: one pair of panels on [1.2, 2.0] only, with the endpoint values 0.500846 and 0.522757 printed. The gray
  band carries the label "beyond r_N". The strong incumbents appear in the manuscript version and in `tab:research`.

## 5. Suggested captions (manuscript)

**Figure `fig:beliefs`.** Beliefs and the ceiling at calibration B. Panel (a) plots the threshold belief τ(r) against
the incumbent strength r. The gray band covers the posteriors that any investor strategy can produce, from m(1/2) to
M(1/2). The ceiling r_C is the strength at which τ(r) equals M(1/2). Panel (b) enlarges the strengths from r_1 to r_2.
The blue band holds every top posterior M(1/2) that puts r_C between r_1 and r_2. At calibration B, M(1/2) lies 0.000334
below the upper edge τ(r_2).

**Figure `fig:coexistence`.** Entry against the incumbent strength at the prior 1/2, for each equilibrium branch under
rules IM and C1. Panel (a) covers the path from r_0 to r_2. Panel (b) enlarges the strengths from 1.25 to 2.35. Branch N
has no informed trade. Branch R has a mixed purchase that recruits the high-cost challenger. On branch F the high class
buys fully. The low class abstains up to r_N, mixes from r_N to r_S, and sells fully from r_S. Branch Q has mixed orders at
the entry floor. The dashed black line shows the threshold branch T, which exists under rule CM only. The blue band
from r_A to r_N marks the strengths at which N and an informative equilibrium coexist. Filled markers belong to a branch.
Open markers do not. Above r_C, entry on F equals the floor ρ.

**Figure `fig:research`.** Research and entry against the incumbent strength at calibration B, with research cost
a = 1/40 and cap λ̄ = 0.336122. Panel (a) shows the research intensity λ. Panel (b) shows total entry E. Zero research is
an equilibrium from r_0 to r_N. The research branch runs from r_R to r̄_R. Along it, research and entry rise strictly.
Research stays at the cap from r̄_R to r_N and above r_U. At the cap, entry equals 0.522757 up to r_C and the floor ρ
above r_C. Black dots mark the strengths r_0, 1.55, 1.60, 1.65, r_1 and r_2. Section 5 characterizes the equilibria
outside the gray bands. The horizontal axis skips the strengths from 2.0 to 2.4. The inset in (b) enlarges entry along
the branch.

Slide notes (one line each, no caption on slides):
- `beliefs_talk`: "The threshold stays between the prior and the top posterior; the ceiling r_C sits just below r_2."
- `coexistence_talk`: "No trade and an informative equilibrium coexist from r_A to r_N; entry on the informative branch rises, then stays flat."
- `research_talk`: "Research rises along the branch while zero research remains an equilibrium; entry rises with it."

## 6. Points for the coordinator and the writers

1. **Open interval.** P3 gives no result on (r_N, r_U) = (1.747878, 2.434046). The research figure shades it and breaks
   the cap line there. Its exact enumeration finds a cap equilibrium at 1.8, 2.0, 2.2 and 2.4. These are not claims. If P3 or
   its checker extends the result, redraw with one change to the script.
2. **Closed or open at r_N and r_C in the research figure.** Zero research is drawn closed at r_N, following the P3 memo
   ("an equilibrium exactly when ρΔ_T ≤ 2k"). The proposition on intermediate strengths assumes the strict inequality.
   The cap equilibrium is drawn open at r_N, as in P3 (r̄_R, r_N). At r_C both ends are open, because the proposition on
   strong incumbents assumes M_λ̄ ≠ τ(r). The coexistence figure draws F closed at r_C, as in P1 under rule C1.
   The XP3 check should confirm the closed end of zero research at r_N.
3. **Numbers in the figures.** Beliefs and research print registry display strings. If a registry value changes, rerun
   the script. The run log shows any mismatch.
4. **Notation.** The figures use `E` for entry, `λ` for research intensity, `\bar\lambda` for the cap, `a` for the research
   cost, `r_N`, `r_J`, `r_S`, `r_C` for the P1 boundaries, `r_R`, `\bar r_R`, `r_U` for the research boundaries. The
   research boundary r_U is `res_rUR` (P3 writes r_U^R). The writers should use the same symbols or ask for a rerun.
5. **Axis labels** follow the pattern "word, symbol": "incumbent strength, r"; "total entry, E"; "research intensity, λ";
   "threshold belief, τ(r)".
6. **No claim refuted.** The log values equal the registry rows. P1 and P3 values at the plotted nodes are the registry
   values.

## 7. Checks run

- Run log: 9 boundaries and 25 other values against the registry, all equal at six decimals.
- `pdffonts` on all six PDFs: embedded TrueType only. Two runs of the script give identical SHA-256 values.
- A throwaway document (deleted) included the three manuscript figures with pdfLaTeX. A second throwaway document
  used the deck's own preamble (moloch, Fira Sans, 16:9) and placed each slide figure in a frame with a frame title.
  Both compile with embedded fonts. I read the three frame renders: each figure fits with room below it.
- Every PNG at 110 dpi was read for overlap and clipping, after the last change to each figure. Grayscale renders of the coexistence and research figures keep
  every branch distinguishable.
