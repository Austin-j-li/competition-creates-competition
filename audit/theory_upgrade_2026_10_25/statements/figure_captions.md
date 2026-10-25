# Figure captions and notes

Drafts for the prose writer, to place in S9. Each block is LaTeX source as it would stand in the manuscript. The three figures keep their numbers and labels: `fig:beliefs` and `fig:coexistence` in Section 4, `fig:research` in Section 5. Every number prints through `\reg`.

## The coexistence figure

Panels: (a) entry along the whole path; (b) the coexistence region in the \((\DT,\tau)\) plane, beside (a); (c) entry enlarged around the coexistence interval, below.

Replaces `sections/04_equilibrium_results.tex:295-307` (the caption and the notes).

```latex
\caption{Entry and the coexistence region along the example's path.}\label{fig:coexistence}
\par\medskip
\begin{minipage}{\linewidth}\footnotesize\singlespacing
\textit{Notes.} The example at the prior \(1/2\), when an indifferent investor may mix over its best orders and an
indifferent high-cost challenger prepares. Panels (a) and (c) show entry against incumbent strength \(r\) in each
equilibrium of Corollary~\ref{cor:example-coexistence}. Panel (a) covers the path from \(r_0\) to \(r_2\), and panel
(c) enlarges the strengths around the coexistence interval, which the blue band marks from \(r_A\) to \(r_N\). The
figure labels a quiet market by N, a mixed purchase that recruits by R, a full purchase by F, mixed orders at the
entry floor by Q and the threshold pair by T. The thin dashed line is the threshold pair~T. At \(r_A\) its purchase
recruits with probability one, and it is an equilibrium under the default tie rules; on \((r_A,r_J]\) it is an
equilibrium when an indifferent high-cost challenger may prepare with any probability. With a full purchase the low
class abstains up to \(r_N\), mixes from \(r_N\) to \(r_S\), and sells with probability one from \(r_S\); above the
entry ceiling \(r_C\), entry with a full purchase equals \(\rho\). Panel (b) draws the region of
Proposition~\ref{prop:coexistence}(a) at the example's slot, in the plane of the target-payoff spread \(\DT\) and
the preparation threshold \(\tau\): \(1/2<\tau\le M(1/2)\) and \(k/(1-\tau)\le\DT\le2k/\rho\). The dotted lower
edge \(\tau=1/2\) lies outside the region, and the other three edges belong to it. The dashed line
\(\DT=k/(1-M(1/2))\) divides the mixed purchase R, on its left, from the full purchase F. The curve traces
\((\DT(r),\tau(r))\) from \(r_0\): it enters the region at \(r_A\), reaches full purchases at \(r_F\), leaves the
region at \(r_N\), and continues towards \(r_1\) and \(r_2\) beyond the panel. Filled markers belong to a curve, and
open markers do not.
\end{minipage}
```

The sentence on the threshold pair is the one drafted with the statements (`B.tex`, paragraph "Figure 2, the sentence on the threshold pair"). The marked strengths of the paragraph above the figure (`04_equilibrium_results.tex:285-290`) need no change of value; that paragraph's "At the benchmark slot" becomes "At the example's slot".

## The research figure

Panels: (a) research, (b) entry, both over the whole path from \(r_0\) to \(r_2\) on one axis; the inset in (b) enlarges entry along the recruiting branch.

Replaces `sections/05_research.tex:135-145` (the caption and the notes).

```latex
\caption{Research and entry along the example's path.}\label{fig:research}
\par\medskip
\begin{minipage}{\linewidth}\footnotesize\singlespacing
\textit{Notes.} The example with \(a=\reg{res_a}\) and \(\lb=\reg{res_cap}\), at the prior \(1/2\), when an
indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares. Panel (a) shows
research \(\lambda\) and panel (b) shows entry; the inset enlarges entry along the recruiting branch. Zero research
is an equilibrium from \(r_0\) to \(r_N\). Recruiting research starts at \(r_R\), reaches the cap at \(r_{\lb}\) and
stays at the cap up to the entry ceiling \(r_C\); its entry rises from \(\reg{res_entry_rR}\) to
\(\reg{res_entry_cap}\) and keeps that value up to \(r_C\). In recruiting research the low class abstains up to
\(r_N\), mixes from \(r_N\) to \(r_S\), and sells with probability one from \(r_S\). From \(r_N\) to \(r_Q\), floor-entry
research coexists with it: both classes trade after a success, no order recruits, entry stays at \(\rho\), and
research rises with strength towards \(\reg{res_lambda_floor_rQ}\) at \(r_Q\). From \(r_Q\) to \(r_C\), recruiting
research at the cap is the only equilibrium. Above \(r_C\), floor-entry research at the cap is the only equilibrium,
with entry \(\rho\). Black dots mark \(r_0\), the three intermediate strengths, \(r_1\) and \(r_2\). Filled markers
belong to a curve, and open markers do not; at \(r_N\) the filled marker belongs to zero research, and at \(r_C\) to
recruiting research at the cap.
\end{minipage}
```

Text near the figure that its content touches, for S9 (the wording targets cover most of it):
- `05_research.tex:119-130`: the passage on \([r_{\lb},r_N)\) and on \(r_U\) follows Corollary 3: research at the cap coexists with zero research on \([r_{\lb},r_N]\), recruiting research at the cap lasts to \(r_C\), floor-entry research lies on \((r_N,r_Q)\) with \(r_Q\approx\reg{res_rQ}\). The figure marks \(r_R\), \(r_{\lb}\), \(r_N\), \(r_Q\) and \(r_C\), and not \(r_U\).
- `05_research.tex:148`: "The research branch in Figure~\ref{fig:research}" becomes "The recruiting branch in Figure~\ref{fig:research}", as in the wording targets.

## The beliefs figure

The content is unchanged. The axis label of panel (a) reads "preparation threshold, \(\tau(r)\)", and the leader to the open marker reads "entry ceiling \(r_C\)".

In `sections/04_equilibrium_results.tex:170-178`:
- the caption "Beliefs and the entry ceiling in the benchmark." becomes "Beliefs and the entry ceiling in the example.";
- the notes' "Panel (a) plots the threshold belief \(\tau(r)\)" becomes "Panel (a) plots the preparation threshold \(\tau(r)\)", and "the benchmark value lies" becomes "the example's value lies".

## In-figure words

Every word that prints inside the figures, for the scan of rules 1 to 4.
- Coexistence, paper: "entry", "incumbent strength", "zoom in (c)", "N", "F", "F above \(r_C\)", "preparation threshold", "target-payoff spread", "\(M(1/2)\)", "prior \(\pi=1/2\)", "coexistence region", "R", "\(r_0\), \(r_A\), \(r_F\), \(r_N\), \(r_J\), \(r_S\), \(r_C\)", "N: quiet market", "Q: mixed orders at the entry floor", "R: mixed purchase that recruits", "T: threshold pair", "F: full purchase", "mixed sales", "full trade", "coexistence".
- Coexistence, slides: the same letters, "threshold" on the region's vertical axis, "coexistence", and the legend "N quiet market", "R mixed purchase that recruits", "F full purchase", "Q mixed orders at the entry floor", "T threshold pair".
- Research, paper: "research intensity", "entry", "incumbent strength", "cap \(\bar\lambda=\reg{res_cap}\)", "zero research", "recruiting research", "recruiting research at the cap", "floor-entry research", "entry along the recruiting branch", "\(r_R\), \(r_{\bar\lambda}\), \(r_N\), \(r_Q\), \(r_C\)".
- Research, slides: "zero", "recruiting", "floor-entry" and the same marks.
- Beliefs: "preparation threshold", "threshold \(\tau(r)\)", "top posterior", "bottom posterior", "prior 1/2", "entry ceiling \(r_C\)", "band for \(M(1/2)\)" and the values of \(M(1/2)\), \(m(1/2)\), \(\tau(r_1)\), \(\tau(r_2)\) and \(r_C\).
