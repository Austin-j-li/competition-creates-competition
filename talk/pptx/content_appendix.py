"""Slides 19-48: the Appendix divider and the 29 backup frames A1-A29 of talk/talk.tex.

Declarative content for build_pptx.py; positions are Beamer pt read off talk/build/talk.pdf
(text baselines via PyMuPDF span origins, table rules via get_drawings). Every number is copied
from talk.tex (see its "% source:" comments); edit both together.

Helpers below turn the LaTeX geometry into engine records:
  items()   an itemize block (ball bullets, measured item gaps)
  note()    a gray footnote line (\\GrayLine)         takeaway()   the Takeaway line
  ltable()  a booktabs table from the PDF geometry: text left edges of the columns, tabcolsep,
            first-line text baselines of the rows and the rule heights
"""
from build_pptx import Box, Cell, Eq, Figure, P, Slide, Table, Text

L, W = 10.91, 431.72          # Beamer text margin and text width (pt)
SIZE_BP = {"tiny": 5.98, "script": 7.97, "footnote": 8.97, "small": 9.96, "normal": 10.91}
# extra space added to the LaTeX \itemsep so the PPT line pitch (1.2207 x size) reproduces the
# baseline-to-baseline distance between items measured in the PDF
ITEM_ADJ = {"normal": 0.2, "small": 2.2, "footnote": 1.65}


def y_ball(base, size="normal"):
    """Top of a text box whose first line (ball bullet) has the given baseline."""
    return round(base - 0.92 * SIZE_BP[size], 2)


def y_plain(base, size="normal"):
    """Top of a text box whose first line (no bullet) has the given baseline."""
    return round(base - 0.97 * SIZE_BP[size], 2)


def _pitch(size, text):
    """Beamer's baselineskip is 1.7% above the PPT line pitch at normal size; math lines are
    already taller in PowerPoint, so only plain paragraphs are stretched."""
    return 1.017 if (size == "normal" and "$" not in text) else None


def items(base, texts, size="normal", sep=6.0, x=L, w=W, name="Bullets", gaps=None):
    """Itemize block; `base` is the baseline of the first line; sep the LaTeX \\itemsep."""
    paras = []
    for k, t in enumerate(texts):
        before = 0.0 if k == 0 else (gaps[k - 1] if gaps else sep + ITEM_ADJ[size])
        paras.append(P(t, bullet="ball", before=before, line=_pitch(size, t)))
    return Text(x, y_ball(base, size), w, paras, size=size, name=name)


def note(base, markup, size="footnote", x=L, w=W, color="616161", name="Note"):
    return Text(x, y_plain(base, size), w, [P(markup, color=color)], size=size, name=name)


def takeaway(base, markup, name="Takeaway"):
    """Takeaway line: `base` is the baseline of its first line."""
    return Text(L, round(base - 0.95 * SIZE_BP["normal"], 2), W, [P(markup, bullet="dot")],
                size="normal", name=name)


def para(base, markup, size="normal", x=L, w=W, name="Text"):
    return Text(x, y_plain(base, size), w, [P(markup, line=_pitch(size, markup))], size=size, name=name)


def cols_at(xs, x_end, sep):
    """Column text widths and per-column (left, right) margins from the text left edges `xs`,
    the right edge of the last column and the gap `sep` between text areas (= 2 x tabcolsep)."""
    n = len(xs)
    t = sep / 2
    tw = [xs[j + 1] - xs[j] - sep for j in range(n - 1)] + [x_end - xs[-1]]
    pads = [(0.0 if j == 0 else t, 0.0 if j == n - 1 else t) for j in range(n)]
    cols = [tw[j] + pads[j][0] + pads[j][1] for j in range(n)]
    # slack: Calibri is not narrower than the Beamer font everywhere, and a wrapped header line
    # would grow the row. Take 2.5 pt from the gap after each column; widen the last column by 3.
    pads = [(l, max(r - 2.5, 0.0)) for (l, r) in pads]
    cols[-1] += 3.0
    return cols, pads


def ltable(name, xs, x_end, sep, rows, bases, top, bottom, size, align="l", mids=None,
           midrules=(0,), rules=True, lead=None):
    """Booktabs table whose rules and first-line baselines follow the PDF.
    mids: {row index i: y of the midrule below row i}; other rows start at their own text.
    Dense tables (row pitch below ~1.2207 x size, or an explicit `lead`) get an exact line pitch,
    so the taller math font cannot grow the rows."""
    cols, pads = cols_at(xs, x_end, sep)
    mids = mids or {}
    s = SIZE_BP[size]
    pitches = [bases[i + 1] - bases[i] for i in range(len(bases) - 1) if (i not in mids)]
    if lead is None and pitches and min(pitches) / (1.2207 * s) < 1.03:
        lead = round(min(pitches), 2)
    # baseline offset from the row top, measured in the LibreOffice render (math rows: taller descent)
    k = 1.02 * s if lead is None else lead - 0.36 * s
    tops = [b - k for b in bases]
    starts = [top]
    for i in range(1, len(rows)):
        starts.append(mids[i - 1] if (i - 1) in mids else tops[i])
    ends = starts[1:] + [bottom]
    row_h = [round(e - st, 2) for st, e in zip(starts, ends)]
    pad_top = [round(max(0.0, t - st), 2) for t, st in zip(tops, starts)]
    return Table(xs[0], top, cols, rows, size=size, align=align, row_h=row_h, rules=rules,
                 midrules=midrules, valign="t", pad_top=pad_top, col_pads=pads, name=name,
                 line_pt=lead)


def back(target, extra=None):
    return dict(nav=extra or [], back=target)


SLIDES = [
    Slide("APPX", "Appendix", kind="divider"),

    # ------------------------------------------------------------------ A1 (p20)
    Slide("A1", "Which deals have a decision interval", page="A1 / 29",
          body=[
              items(52.4, [
                  "A disclosed approach, an announced strategic review or an open contest can create "
                  "one; none does so automatically",
                  "A wholly confidential process does not: no prospective challenger could watch the "
                  "price while it mattered",
                  "Strength = the public distribution of the incumbent’s value, not an announced bid",
                  r"Imprivata’s proxy separates an unsolicited approach, outreach to potential buyers, "
                  r"and indications of interest conditional on diligence, which is evidence of a costly "
                  r"preparation stage, not that a price drew anyone in \cite{Imprivata 2016; Boone and "
                  r"Mulherin 2007; Gentry and Stroup 2019}",
              ]),
              note(197.0, "Whether a deal fits is a question about its chronology; the paper settles it "
                          "for no specific transaction (Section 1.1)."),
          ], **back("main:interval")),

    # ------------------------------------------------------------------ A2 (p21)
    Slide("A2", "Evidence: a design, not a result", page="A2 / 29",
          body=[
              items(65.2, [
                  r"\b{Pilot (Online Appendix D):} reconstruct from disclosure records the timing of "
                  r"approaches, public visibility, buyer contacts, diligence, proposals and final selection",
                  "Separate when an event occurred from when it first became public",
                  r"\b{First requirement:} a publicly understood sale opportunity that stays contestable "
                  r"while a challenger decides",
                  r"\b{Outcome:} the decision to prepare; prices must precede it",
                  r"\b{Caution:} later returns can reflect anticipated arrival",
              ]),
              note(188.7, "Design only: no sample, effect, instrument or identification strategy is "
                          "reported (Section 7)."),
          ], **back("main:evidence")),

    # ------------------------------------------------------------------ A3 (p22)
    Slide("A3", "Related work in more detail",
          subtitle="Increment: under one sale rule the two returns move oppositely, which produces the "
                   "entry reversal",
          page="A3 / 29",
          body=[
              ltable("T Related work", xs=[10.9, 161.5, 303.5], x_end=436.7, sep=5.98, size="script",
                     rows=[
                         ["Work", "Shows", "Here"],
                         ["Dow, Goldstein and Guembel (2017)", "investment feeds back on information",
                          "one surplus, two opposed claims"],
                         ["Edmans, Goldstein and Jiang (2015)", "real actions curb bad-news trading",
                          "rivals shift claim sensitivity"],
                         ["Edmans, Goldstein and Jiang (2012)", "prices affect takeover activity",
                          "a challenger learns its own value"],
                         [r"Fishman (1988);\\Hirshleifer and Png (1989)", "stronger rivals deter preparation",
                          "kept at fixed information (Prop.~A.3)"],
                         [r"Levin and Smith (1994);\\Gentry and Stroup (2019)", "the bidder pool is endogenous",
                          "entry responds to the price"],
                         ["Roberts and Sweeting (2013)", "selective entry shapes procedure",
                          "sale terms left open"],
                         ["Persico (2000)", "formats shape bidders’ information",
                          "the informed party is not a bidder"],
                         ["Luo (2005)", "learning from announcement returns", "learning precedes entry"],
                         ["Betton et al. (2014); Lin et al. (2025)", "negotiation feedback; payment choice",
                          "cash fixed; entry of a new bidder"],
                         ["Cornelli and Li (2002)", "arbitrage positions affect tenders",
                          "the investor does not tender"],
                         [r"Pernoud and Gleyze (2026);\\Liu and Bernhardt (2022);\\Carlin et al. (2026)",
                          r"learning own values and rivals;\\post-auction feedback;\\bidder-pool choice",
                          "the informed party trades outside the auction, before entry"],
                     ],
                     bases=[60.4, 75.5, 85.9, 96.4, 106.8, 126.8, 146.7, 157.1, 167.6, 178.1, 188.5, 199.0],
                     top=50.15, bottom=223.13, mids={0: 65.41}, lead=9.5),
          ], **back("main:lit")),

    # ------------------------------------------------------------------ A4 (p23)
    Slide("A4", "What the model leaves out, and why", page="A4 / 29",
          body=[
              ltable("T Model scope", xs=[28.0, 113.7], x_end=425.5, sep=11.95, size="small",
                     rows=[
                         [r"\b{In the model}",
                          "Neither bidder trades. The investor has no initial position, cannot bid, "
                          "tender or acquire, and has no control rights. The sale binds all shares (no "
                          "tendering or holdout). Every wrong-signed order loses against every candidate "
                          "schedule, so the investor cannot profit by faking good news."],
                         [r"\b{Outside the model}",
                          r"Toeholds \cite{Bulow, Huang and Klemperer 1999}; free riding \cite{Grossman and "
                          r"Hart 1980}; announced or jump bids as signals \cite{Fishman 1988} (strength here "
                          r"is a distribution); incumbent or target manipulation and endogenous investor "
                          r"research \cite{Goldstein and Guembel 2008}; first-price and "
                          r"bargaining-with-trading equilibria."],
                     ],
                     bases=[64.6, 121.1], top=50.57, bottom=175.73, mids={0: 107.17}),
              takeaway(201.0, "The paper does not solve toeholds, so it makes no statement on the "
                              "direction of a toehold effect."),
          ], **back("main:omit")),

    # ------------------------------------------------------------------ A5 (p24)
    Slide("A5", "Complementary, not superior, information", page="A5 / 29",
          body=[
              items(65.9, [
                  "The challenger knows its own integration plans; a specialist investor may know the "
                  "target’s customers, technology and product demand",
                  "Different facts about the same acquisition match",
                  "Preparation (diligence) is what reveals the exact value to the challenger",
                  "The benchmark’s perfectly informed investor and uninformed challenger make the "
                  "mechanism visible; Section~5.3 removes both extremes",
                  r"The reversal holds with challenger accuracy $d=0.75$ above investor accuracy $a=0.70$ "
                  r"\status{(Prop.~A.7, analytical)}",
              ]),
          ], **back("main:info", [("The signal economy", "app:signals")])),

    # ------------------------------------------------------------------ A6 (p25)
    Slide("A6", "The price helps a challenger with its own signal", page="A6 / 29",
          body=[
              items(47.0, [
                  r"Investor signal $T$ (accuracy $a$), challenger signal $Y$ (accuracy $d$); the "
                  r"challenger uses\\$\Pr(H\mid P,\,Y=y)$, $P$~= stock price",   # Beamer's line break
                  r"Entry is state dependent: $e_H$, $e_L$ = entry probability when the challenger is "
                  r"high / low value; the price still reveals the market posterior",
                  r"Declared example $a=0.70$, $d=0.75$: entry 0.850 $\to$ 0.879 "
                  r"\status{(analytical, Prop.~A.7)}; $\rho=0.85$, $c_H=7.14$, $k=0.015$, strengths 1.1 "
                  r"vs 2.3",
              ], size="small", gaps=[5.1, 5.1]),
              ltable("T Signal grid", xs=[66.6, 97.9, 226.5, 314.8], x_end=387.0, sep=11.96, size="small",
                     align=["c", "l", "c", "l"],
                     rows=[
                         ["Cells", "Accuracy grid (25 cells)", "Entry change (pp)", "Status"],
                         ["6", r"meet Prop.~A.7", "rises 2.81 to 3.09", r"\status{analytical}"],
                         ["9", r"$d\le0.75$, condition not met", "unchanged", r"\status{numerical diagnostic}"],
                         ["10", r"$d\ge0.76$", "falls 4.03 to 4.49", r"\status{numerical diagnostic}"],
                     ],
                     bases=[145.8, 163.4, 175.3, 187.3], top=133.83, bottom=193.24, mids={0: 151.58}),
              takeaway(215.5, "The price matters when the challenger’s own signal is informative but "
                              "not decisive."),
          ], **back("app:info")),

    # ------------------------------------------------------------------ A7 (p26)
    Slide("A7", "Equilibrium and the two comparisons", page="A7 / 29",
          body=[
              items(68.3, [
                  r"\b{Definition:} order distributions $\sigma_H,\sigma_L$ (mixing allowed; any deviation "
                  r"$q\in[-1,1]$); a rational price that anticipates entry; Bayesian beliefs from the "
                  r"price; optimal entry; truthful bids",
                  r"Order flow $X=q+Z$, Laplace noise $Z$ with scale $b$; stock price $P(X)$ = expected "
                  r"target payoff given $X$",
                  r"\b{Two comparisons kept apart:} a unilateral deviation is evaluated against fixed "
                  r"price and entry schedules; a cross-economy comparison re-solves them",
                  r"\b{Uniqueness} refers to trading and on-path entry under truthful bidding",
              ]),
          ], **back("main:eq")),

    # ------------------------------------------------------------------ A8 (p27)
    Slide("A8", "Acquisition payoffs in closed form", page="A8 / 29",
          body=[
              Eq(46.6, 46.5, r"t_0=p(1-p/r),", size="small", name="Eq t0"),
              Eq(184.4, 45.2, r"t_H=r/2+p^2/(2r),", size="small", name="Eq tH"),
              Eq(306.1, 45.2, r"t_L=\ell-(\ell^2-p^2)/(2r),", size="small", name="Eq tL"),
              Eq(46.2, 61.5, r"g_H=h-r/2-p^2/(2r),", size="small", name="Eq gH"),
              Eq(184.0, 61.5, r"g_L=(\ell^2-p^2)/(2r),", size="small", name="Eq gL"),
              Eq(305.8, 61.5, r"\Delta_T=(r-\ell)^2/(2r)", size="small", color="AA4B00", name="Eq spread"),
              ltable("T Closed forms", xs=[79.5, 255.9, 322.0], x_end=374.0, sep=11.96, size="footnote",
                     align=["l", "c", "c"],
                     rows=[
                         ["", r"weak $r_0=1.2$", r"strong $r_1=3$"],
                         [r"Proceeds without a challenger, $t_0$", "0.292", "0.417"],
                         [r"Proceeds with a high-value challenger, $t_H$", "0.704", "1.54"],
                         [r"Proceeds with a low-value challenger, $t_L$", "0.688", "0.875"],
                         [r"Gross profit of a high-value challenger, $g_H$", "9.30", "8.46"],
                         [r"Gross profit of a low-value challenger, $g_L$", "0.313", "0.125"],
                         [r"\info{Target-payoff spread, $\Delta_T=t_H-t_L$}", "0.0167", "0.667"],
                         [r"Expected gross profit at the prior, $B_r(1/2)$", "4.80", "4.29"],
                     ],
                     bases=[90.7, 106.8, 117.2, 127.6, 138.0, 148.4, 158.8, 169.2],
                     top=79.85, bottom=174.73, mids={0: 96.06}),
              note(186.9, r"Proposition 1 (analytical) holds for any $F$ on $[0,\bar r]$, "
                          r"$\ell<\bar r<h$; strict when the change in $F$ has positive integral over the "
                          r"relevant range."),
              takeaway(215.0, "The closed forms are the uniform case; the two signs are not a "
                              "uniform-distribution artifact."),
          ], **back("main:payoffs")),

    # ------------------------------------------------------------------ A9 (p28)
    Slide("A9", "The payment rule decides the sign of the spread effect", page="A9 / 29",
          body=[
              Figure(10.9, 40.62, 215.1, 149.92, "bargaining_spread_talk",
                     alt="Target-payoff spread Delta_eta against the seller's bargaining weight eta from 0 "
                         "to 1, for the weak incumbent r0 = 1.2 (solid) and the strong incumbent r1 = 3 "
                         "(dashed). The two lines cross at eta = 1/2, near 4.5; the strong line is steeper "
                         "and higher below 1/2 and lower above."),
              Text(248.4, y_plain(51.6, "small"), 194.3, [
                  P(r"Zero-reserve verifiable-value institution, Nash weight $\eta$: seller gets "
                    r"$t_\eta=(1-\eta)\cdot$runner-up value + $\eta\cdot$winner value"),
                  P(r"Stronger incumbent: challenger profit falls weakly for every $\eta$. Spread "
                    r"$\Info{\Delta_\eta}=\eta(h-\ell)+(1-2\eta)\,\mathbb{E}[(R-\ell)_+]$ rises (weakly) "
                    r"if $\eta<1/2$, falls (weakly) if $\eta>1/2$, for any $R\sim F$ on $[0,\bar r]$, "
                    r"$\ell<\bar r<h$, $0\le\eta<1$ \status{(Prop.~A.8, analytical)}", before=5.8),
              ], size="small", name="Bargaining text"),
              takeaway(206.4, "Payment stage only: an entry reversal under bargaining is not solved, and "
                              "first-price equilibria are not solved."),
          ], **back("main:payrule")),

    # ------------------------------------------------------------------ A10 (p29)
    Slide("A10", "Why trading is unique: a global bound", page="A10 / 29",
          body=[
              items(48.8, [
                  r"\b{Weak:} gross advantage per unit $\le\Delta_T(r_0)<k$, so every nonzero order loses "
                  r"and the posterior stays at $1/2$",
                  r"\b{Strong:} with $\Pi_\theta(s)$ the expected residual per unit at order size $s$,",
              ], sep=4.0, name="Bullets 1"),
              Eq(231.18, 83.0, r"U_\theta(s)=s\,\Pi_\theta(s)-ks,\qquad U_\theta'(s)\ \ge\ (1-1/b)\,\rho m\,"
                             r"\Info{\Delta_T(r_1)}-k\ >\ 0\quad\text{on }[0,1]", size="normal",
                 name="Marginal profit bound", anchor="c"),
              items(121.0, [
                  "Holds against every candidate price and entry schedule, including mixed orders: "
                  "global, not first-order",
                  r"\b{Investor manipulation (in-model):} both residual advantages in eq.~(11) are "
                  r"positive under every candidate order distribution, so a wrong-signed order, such as a "
                  r"low-value investor buying to fake good news and trigger entry, has negative gross "
                  r"payoff and still pays $k$",
                  "Incumbent or target manipulation and toeholds: outside the model (A4)",
              ], sep=4.0, name="Bullets 2"),
          ], **back("main:bound")),

    # ------------------------------------------------------------------ A11 (p30)
    Slide("A11", "Orders, units and the trading cost", page="A11 / 29",
          body=[
              items(60.5, [
                  r"$q\in[-1,1]$ is a normalized small trading unit, not ownership of the target, "
                  r"measured in the same units as the noise (scale $b$); the investor has no initial "
                  r"position",
                  r"$k$ is an execution or position-carrying friction, distinct from adverse-selection "
                  r"price impact, which competitive pricing already generates",
                  r"\b{Why a corner, unlike Kyle:} the per-unit advantage is at least $\rho m\Delta_T$ "
                  r"because beliefs stay in $[m,M]$, and one more unit erodes it by at most a fraction "
                  r"$1/b$ (the haircut)",
                  "So marginal profit stays above $k$ over the whole interval, and full orders are the "
                  "unique best response (A10)",
                  "Against the weak incumbent the same bounds make every order lose",
              ]),
          ], **back("main:orders")),

    # ------------------------------------------------------------------ A12 (p31)
    Slide("A12", "Notation", page="A12 / 29",
          body=[
              ltable("T Notation 1", xs=[10.1, 88.1], x_end=212.5, sep=11.96, size="footnote",
                     rows=[
                         ["Symbol", "Meaning"],
                         [r"$R$; $r$", r"incumbent value $R\sim U[0,r]$; $r$ = incumbent strength"],
                         [r"$\theta\in\{H,L\}$; $h,\ell$", r"challenger quality; worth $h$ or $\ell$"],
                         [r"$p$", "reserve price (not the stock price)"],
                         [r"$C$; $c_L,c_H$; $\rho$", r"preparation cost; cheap, expensive; $\Pr(C=c_L)$"],
                         [r"$t_H,t_L$", "expected target proceeds when a high / low-value challenger enters"],
                         [r"$\Delta_T$", r"target-payoff spread $t_H-t_L$"],
                         [r"$g_H,g_L$", "gross acquisition profit of a high / low-value challenger"],
                     ],
                     bases=[65.7, 82.3, 104.2, 115.2, 126.2, 148.1, 170.0, 181.0],
                     top=54.48, bottom=197.58, mids={0: 71.24}),
              ltable("T Notation 2", xs=[231.8, 274.1], x_end=404.5, sep=11.96, size="footnote",
                     rows=[
                         ["Symbol", "Meaning"],
                         [r"$r_0,r_1$", "weak, strong incumbent"],
                         [r"$\mu$", r"market’s belief $\Pr(H)$ revealed by the price"],
                         [r"$m,M$", r"bounds on $\mu$: $m=1/(1+e^{2/b})$, $M=1-m$"],
                         [r"$b$", "scale of the Laplace noise"],
                         [r"$k$", "trading cost per unit"],
                         [r"$(q_H,q_L)$", "orders after a high / low challenger value"],
                         [r"$B_r(\mu)$", r"challenger’s expected gross profit at belief $\mu$"],
                         [r"$r_2$", "stronger still incumbent"],
                     ],
                     bases=[65.7, 82.3, 93.3, 115.8, 137.7, 148.7, 159.7, 181.6, 203.5],
                     top=54.48, bottom=209.16, mids={0: 71.24}),
          ], **back("main:notation")),

    # ------------------------------------------------------------------ A13 (p32)
    Slide("A13", "The challenger can read the market’s belief off the price", page="A13 / 29",
          body=[
              items(55.3, [
                  r"Under any mixed orders the posterior from order flow is bounded (Laplace likelihood "
                  r"ratio within $e^{\pm2/b}$):",
              ], name="Bullets 1"),
              Eq(231.59, 81.6, r"\mu_X(x)=\Pr(H\mid X=x)\in[m,M]", size="normal", name="Posterior bound", anchor="c"),
              Eq(228.01, 98.2, r"\text{price}=t_0+(\text{entry probability at that price})\times"
                             r"(t_L-t_0+\Delta_T\,\mu)", size="normal", name="Price equation", anchor="c"),
              items(141.9, [
                  r"$t_0$ = expected target proceeds without a challenger",
                  r"The price is strictly increasing in $\mu$, because entry $\ge\rho>0$ and $\Delta_T>0$",
                  r"Atoms and entry jumps allowed; no differentiability needed "
                  r"\status{(Props.~A.1–A.2, analytical)}",
              ], sep=3.0, name="Bullets 2"),
              takeaway(196.1, "The price is a sufficient statistic for the market’s belief, so the "
                              "challenger loses nothing by seeing the price rather than the flow."),
          ], **back("main:suff")),

    # ------------------------------------------------------------------ A14 (p33)
    Slide("A14", "Why Laplace noise, and what logistic noise changes", page="A14 / 29",
          body=[
              Figure(18.0, 31.31, 417.6, 122.4, "posterior_tail_entry_talk",
                     alt="Two panels against the threshold distance M minus tau from 0 to about 0.23. "
                         "(a) Pr(mu_X >= tau) under full orders: Laplace (solid) from 0.34 to 0.5, logistic "
                         "(dashed) from 0 to 0.5. (b) Total entry E: Laplace from 0.51 to 0.62, logistic "
                         "from 0.25 to 0.62."),
              items(165.9, [
                  r"Both noise densities $f$ satisfy $|f'|\le f/b$, so the global trading bounds hold "
                  r"for both",
                  r"Laplace: the posterior reaches $[m,M]$ at finite flow; logistic: only as flow "
                  r"$\to\infty$ ($x^*\approx5.42$, about 1.5 noise s.d. from the center)",
                  r"Entry 0.302 vs 0.523; atomless costs ($\varepsilon_C=0.1$): 0.523 and 0.301. Common "
                  r"scale $b$, not common variance; not a Blackwell ranking "
                  r"\status{(analytical, Props.~A.5–A.6)}",
              ], size="footnote", sep=0.0),
          ], **back("main:laplace")),

    # ------------------------------------------------------------------ A15 (p34)
    Slide("A15", "Why the model needs a low-cost floor", page="A15 / 29",
          body=[
              items(68.9, [
                  "Without entry after every price, target proceeds do not depend on quality, so no "
                  "informative trading is consistent: nobody prepares and there is nothing to trade on",
                  r"The \cost{low-cost floor} is part of the mechanism, not a numerical regularizer",
                  r"It gives the lower bound $\rho m\Delta_T$ on the residual advantage",
                  "Theorem margin at the benchmark: 1.37",
                  "The floor alone gives entry 0.250 at both strengths when the price is hidden",
                  r"Atomless cost supports keep it \status{(Prop.~A.6, analytical)}",
              ]),
          ], **back("main:floor")),

    # ------------------------------------------------------------------ A16 (p35)
    Slide("A16", "Proof logic in four steps", page="A16 / 29",
          body=[
              Text(L, y_ball(47.7), W, [
                  P(r"\key{1.}" + "\t" + r"\b{Weak economy:} no order covers $k$; no trade; entry $\rho$",
                    hang=(21.8, -14.8)),
                  P(r"\key{2.}" + "\t" + r"\b{Strong economy:} the global bound (A10) forces full orders",
                    hang=(21.8, -14.8), before=5.2),
                  P(r"\key{3.}" + "\t" + r"Under full orders the high-cost window puts the belief "
                    r"threshold inside $(1/2,M)$, so good news crosses it with positive probability; "
                    r"$\alpha_H>\alpha_L$ (good news is likelier when the challenger is high value, "
                    r"$\alpha_\theta=\Pr(\text{order flow crosses the entry threshold}\mid\theta)$) tilts "
                    r"extra entry to high values", hang=(21.8, -14.8), before=5.2),
                  P(r"\key{4.}" + "\t" + r"\b{Blackwell:} a constant kernel maps the strong experiment to "
                    r"the weak one; no state-independent kernel maps the constant experiment to the strong "
                    r"one", hang=(21.8, -14.8), before=5.2),
              ], size="normal", name="Steps"),
              para(180.0, r"\b{Part (iii):} with the floor and profitable trading still in place at $r_2$, "
                          r"$B_{r_2}(M)<c_H$ removes expensive entry.", name="Part iii"),
              takeaway(214.2, "What does the work: step 2, a bound that holds against every candidate "
                              "schedule."),
          ], **back("main:proof")),

    # ------------------------------------------------------------------ A17 (p36)
    Slide("A17", r"Conditions are jointly satisfiable for every $h>\ell$", page="A17 / 29",
          body=[
              ltable("T Theorem margins", xs=[73.5, 234.9, 347.4], x_end=380.1, sep=11.96, size="small",
                     align=["l", "l", "r"], midrules=(0, 5), mids={0: 58.51, 5: 123.92},
                     rows=[
                         [Cell("Theorem margins at the benchmark", span=3)],
                         [r"\cost{Low-cost floor}", r"$B_{r_1}(m)-c_L$", "1.37"],
                         [r"\cost{High-cost window}, weak prior", r"$c_H-B_{r_0}(1/2)$", "1.20"],
                         [r"\cost{High-cost window}, best strong price", r"$B_{r_1}(M)-c_H$", "0.217"],
                         [r"\info{Trading-cost window}, weak", r"$k-\Delta_T(r_0)$", "0.00333"],
                         [r"\info{Trading-cost window}, strong", r"$(1-1/b)\rho m\Delta_T(r_1)-k$", "0.00241"],
                         ["Minimum", "", "0.00241"],
                     ],
                     bases=[52.7, 70.3, 82.3, 94.2, 106.2, 118.1, 135.7], top=40.76, bottom=141.67),
              items(155.6, [
                  r"Nonemptiness for every $h>\ell$ comes from a construction: take $r_0<r_1$ close to "
                  r"$\ell$, then $k$, $c_H$, $c_L$ strictly inside their windows",
                  r"A mathematical construction, not slack at the benchmark and not an effect-size "
                  r"claim; moderate values $h=2$: minimum margin $8.01\times10^{-4}$",
                  r"Part (iii) is not claimed for every $h>\ell$",
              ], size="small", gaps=[4.05, 4.05]),
          ], **back("main:margins")),

    # ------------------------------------------------------------------ A18 (p37)
    Slide("A18", "Two forces from one payment rule", page="A18 / 29",
          body=[
              ltable("T Two forces", xs=[26.3, 131.8, 268.5], x_end=427.2, sep=11.96, size="small",
                     rows=[
                         ["", "Deterrence", r"\info{Information}"],
                         ["What a stronger incumbent moves", r"challenger profit $B_r(\mu)\downarrow$ at every belief",
                          r"\info{target-payoff spread $\Delta_T\uparrow$}"],
                         ["Who responds", "the challenger, at a given belief",
                          "the investor, then the price, then the challenger’s belief"],
                         ["What it needs", "nothing",
                          r"entry after any price (\cost{low-cost floor}); price seen before entry"],
                         ["Effect on entry", r"\b{weakly} $\downarrow$ \status{(Prop.~A.3)}",
                          r"$\uparrow$ once trading pays and good news clears \cost{$c_H$}"],
                     ],
                     bases=[61.4, 81.4, 107.7, 134.0, 160.3], top=47.75, bottom=178.89, mids={0: 67.89}),
              takeaway(204.1, r"\info{stronger incumbent $\to$ wider $\Delta_T$ $\to$ informed trading pays "
                              r"$\to$ informative price $\to$ good news clears} \cost{$c_H$} "
                              r"\info{$\to$ the expensive challenger enters}"),
          ], **back("main:forces")),

    # ------------------------------------------------------------------ A19 (p38)
    Slide("A19", "Benchmark scale: declared, not calibrated", page="A19 / 29",
          body=[
              ltable("T Inputs", xs=[26.2, 59.9, 118.4], x_end=158.2, sep=11.96, size="small",
                     align=["l", "c", "c"],
                     rows=[
                         ["Input", "Benchmark", "Moderate"],
                         ["$h$", "10", "2"], [r"$\ell$", "1", "1"], ["$p$", "0.5", "0.5"],
                         [r"$\rho$", "0.25", "0.25"], ["$c_L$", "1", "0.3"], ["$c_H$", "6", "0.89"],
                         ["$b$", "2", "2"], ["$k$", "0.02", "0.002"],
                     ],
                     bases=[52.2, 69.8, 81.7, 93.7, 105.6, 117.6, 129.5, 141.5, 153.5],
                     top=40.22, bottom=159.41, mids={0: 57.97}),
              ltable("T Outcomes", xs=[186.9, 307.1, 379.9], x_end=440.8, sep=11.96, size="small",
                     align=["l", "c", "c"],
                     rows=[
                         ["", "Benchmark", "Moderate"],
                         ["Strengths", r"$1.2\to3$", r"$1.05\to1.5$"],
                         ["Entry", r"$0.250\to0.523$", r"$0.250\to0.527$"],
                         ["Minimum theorem margin", "0.00241", r"$8.01\times10^{-4}$"],
                     ],
                     bases=[82.1, 99.7, 111.6, 123.6], top=70.11, bottom=129.52, mids={0: 87.86}),
              note(173.1, r"Units are arbitrary; magnitudes are not calibrated; the signs are the "
                          r"theorem; nonemptiness holds for every $h>\ell$ (A17)."),
              takeaway(202.7, r"A moderate economy with $h=2$ gives a rise of similar size (0.250 $\to$ "
                              r"0.527), so the benchmark scale is a declaration, not the mechanism."),
          ], **back("main:scale")),

    # ------------------------------------------------------------------ A20 (p39)
    Slide("A20", "How entry and ownership are computed", page="A20 / 29",
          body=[
              Eq(229.54, 51.6, r"\tau=\frac{\Cost{c_H}-g_L}{g_H-g_L}\quad\text{(}\Cost{c_H\text{ = expensive "
                             r"cost}}\text{)},\qquad x^*=\frac b2\log\frac{\tau}{1-\tau},\qquad "
                             r"\alpha_\theta=\Pr(X\ge x^*\mid\theta)", size="normal", name="Entry threshold", anchor="c"),
              Eq(231.69, 84.2, r"e_H=\rho+(1-\rho)\alpha_H,\qquad e_L=\rho+(1-\rho)\alpha_L,\qquad "
                             r"\mathsf E=\frac{e_H+e_L}{2},\qquad \mathsf O_H=\frac{e_H}{2}",
                 size="normal", name="Entry and ownership", anchor="c"),
              items(137.0, [
                  r"$\tau$ = belief threshold for costly preparation; $\alpha_\theta$ = probability that "
                  r"order flow crosses the entry threshold; entry $\mathsf E$ = Pr(challenger prepares); "
                  r"high-value ownership $\mathsf O_H$ = Pr(high-value challenger acquires the target)",
                  r"The high-cost window puts $\tau\in(1/2,M)$ and $x^*\in(0,1)$; $\alpha_H>\alpha_L$",
                  r"Above the ceiling strength $r_C\approx3.59$, $\tau>M$; the left-limit entry at $r_C$ "
                  r"is 0.506",
                  r"Expected target proceeds 0.393 / 0.872 / 0.664 at $r_0$ / $r_1$ / $r_2$",
              ], size="small", gaps=[4.4, 4.5, 4.5]),
          ], **back("main:entry")),

    # ------------------------------------------------------------------ A21 (p40)
    Slide("A21", "Which equilibrium? What the proof certifies", page="A21 / 29",
          body=[
              para(47.2, r"The reversal (frames 9–10) compares economies in which trading and on-path "
                         r"entry are unique, so no selection is needed; multiplicity arises only between "
                         r"them (frame 12).", size="small", name="Lead-in"),
              ltable("T Certified nodes", xs=[35.2, 63.6, 188.7, 317.9], x_end=418.3, sep=11.96,
                     size="footnote", align="c",
                     rows=[
                         [r"$r$", r"$q_L\in$", r"Entry $\mathsf E\in$", r"High-type cover margin $\ge$"],
                         ["1.55", r"$[-0.46031620,\,-0.46031618]$", r"$[0.5450528898,\,0.5450528922]$", "0.0000761777"],
                         ["1.60", r"$[-0.70747539,\,-0.70747537]$", r"$[0.5487563062,\,0.5487563085]$", "0.0027531948"],
                         ["1.65", r"$[-0.90333201,\,-0.90333198]$", r"$[0.5513607988,\,0.5513608020]$", "0.0054921767"],
                     ],
                     bases=[83.6, 100.2, 111.1, 122.1], top=72.32, bottom=127.74, mids={0: 89.07}),
              items(141.9, [
                  r"\b{Low type:} global strict concavity; a sign change of its marginal profit at its own "
                  r"order brackets the root (0.000000000114 and $-0.000000000096$ at $r=1.55$)",
                  r"\b{High type:} cover margin strictly positive over the whole bracket (last column)",
                  r"\b{Not proved:} uniqueness of the informative profile, absence of mixed equilibria, a "
                  r"branch between nodes",
              ], size="small", gaps=[3.9, 4.0]),
              note(216.2, r"computer-assisted (Proposition 3): interval arithmetic on exact decimal inputs",
                   size="script", name="Status"),
          ], **back("main:cert")),

    # ------------------------------------------------------------------ A22 (p41)
    Slide("A22", "Information controls in detail", page="A22 / 29",
          body=[
              items(50.7, [
                  r"Prop.~A.3 \status{(analytical)}: at any fixed information experiment and cost law, "
                  r"entry weakly falls with strength; within fixed orders, not across order profiles that "
                  r"change with $r$",
                  r"The frozen weak profile is a control, not an equilibrium: full orders lose money there "
                  r"because $\Delta_T(r_0)<k$; at $r_1$ it coincides with the equilibrium",
              ], size="small", gaps=[2.7]),
              ltable("T Controls", xs=[10.9, 137.1, 157.9, 195.1, 298.6, 368.0], x_end=440.2, sep=9.96,
                     size="script", align=["l", "c", "c", "c", "c", "l"],
                     midrules=(0, 3, 6), mids={0: 113.43, 3: 143.48, 6: 173.81},
                     rows=[
                         ["", r"$r$", r"Entry $\mathsf E$", r"High-value ownership $\mathsf O_H$",
                          "Target proceeds", "Status"],
                         [r"\i{Equilibria of the feedback game}", "1.2", "0.250", "0.125", "0.393", r"\gray{analytical}"],
                         ["", "3", "0.523", "0.324", "0.872", r"\gray{analytical}"],
                         ["", "3.6", "0.250", "0.125", "0.664", r"\gray{analytical}"],
                         [Cell(r"\i{Frozen informative orders} (control, not an equilibrium at $r_0$)", span=6)],
                         ["", "1.2", "0.562", "0.351", "0.520", r"\gray{numerical diagnostic}"],
                         ["", "3", "0.523", "0.324", "0.872", r"\gray{numerical diagnostic}"],
                         [Cell(r"\i{Price hidden from challenger} (equilibrium of the no-price-access game)", span=6)],
                         ["", "1.2", "0.250", "0.125", "0.393", r"\gray{analytical}"],
                         ["", "3", "0.250", "0.125", "0.615", r"\gray{analytical}"],
                     ],
                     bases=[108.8, 122.5, 130.7, 138.8, 152.9, 161.0, 169.2, 183.2, 191.3, 199.5],
                     top=99.49, bottom=204.3),
              note(212.5, r"Price hidden: the challenger enters only at low cost (high-cost window); at "
                          r"$r_1$ the investor still trades full orders."),
          ], **back("main:controls")),

    # ------------------------------------------------------------------ A23 (p42)
    Slide("A23", "Price level or information?", page="A23 / 29",
          body=[
              items(62.9, [
                  r"\b{Invariance diagnostic:} add a dividend $D_0=0.257809$ (the revenue gain from price "
                  r"access) to the traded claim in the price-hidden economy. Mean prices then match, but "
                  r"entry does not, so the information matters, not the price level. \status{(diagnostic)}",
                  "The revenue gain itself, 0.258, is analytical",
                  r"Prop.~A.9 at $r_1$: each extra entry is chosen only when expected gross profit covers "
                  r"its cost; the allocation gain includes that profit and sales that would otherwise fail "
                  r"the reserve; transfers excluded",
                  "The dividend is not a sale mechanism and is excluded from surplus; no ranking of "
                  "strengths or mechanisms",
              ]),
          ], **back("main:welfare")),

    # ------------------------------------------------------------------ A24 (p43)
    Slide("A24", "Trading and entry across strengths: entry", page="A24 / 29",
          body=[
              Figure(32.5, 30.12, 388.6, 157.0, "equilibrium_correspondence_a_talk",
                     alt="Equilibrium entry against incumbent strength r from 1.0 to 3.8. No trade (entry "
                         "0.25) is unique below r_P = 1.22 and exists up to r_N = 1.75; asymmetric orders "
                         "(1, q_L) with certified entry near 0.55 between 1.55 and 1.65; symmetric interior "
                         "orders from about 1.75; full orders unique above r_U = 2.84, with entry falling "
                         "slightly to 0.50 at r_C = 3.59, then back to 0.25 with no expensive entry."),
              note(198.1, r"No trade unique for $r<r_P\approx1.22$, an equilibrium up to "
                          r"$r_N\approx1.75$; full orders unique above $r_U\approx2.84$; expensive entry "
                          r"impossible above $r_C\approx3.59$ \status{(analytical, Prop.~A.4; shaded: "
                          r"unique)}; full correspondence open.", color="000000", name="Caption"),
          ], **back("main:corr", [("Order sizes", "app:corrb")])),

    # ------------------------------------------------------------------ A25 (p44)
    Slide("A25", "Trading and entry across strengths: orders", page="A25 / 29",
          body=[
              Figure(32.5, 33.71, 388.6, 157.0, "equilibrium_correspondence_b_talk",
                     alt="Order size |q_L| against incumbent strength r from 1.0 to 3.8. No trade (0) up "
                         "to about 1.75; asymmetric orders (1, q_L) rising from 0.2 to 1 between 1.5 and "
                         "1.7 through certified nodes 0.460, 0.707, 0.903; full orders (1, -1) at 1 from "
                         "about 1.7; symmetric interior orders and a mixed candidate at r_N shown as "
                         "numerical diagnostics."),
              note(201.6, r"No trade is $(0,0)$. Certified nodes: $|q_L|\approx0.460,\,0.707,\,0.903$ "
                          r"(computer-assisted); the curve through them and the mixed candidate are "
                          r"numerical diagnostics; no branch between nodes is claimed.", color="000000",
                   name="Caption"),
          ], **back("app:corr")),

    # ------------------------------------------------------------------ A26 (p45)
    Slide("A26", "Robustness in full", page="A26 / 29",
          body=[
              ltable("T Robustness in full", xs=[21.5, 140.0, 213.4, 250.1, 291.6, 348.9, 392.5],
                     x_end=432.1, sep=8.97, size="footnote", align=["l", "l", "c", "c", "c", "c", "c"],
                     rows=[
                         ["", r"$\rho$; strengths", r"$\mathsf E$ weak", r"$\mathsf E$ strong", "Change (pp)",
                          r"$\mathsf O_H$ weak", r"$\mathsf O_H$ strong"],
                         ["Laplace, cost atoms", r"0.25; $1.2\to3$", "0.250", "0.523", "27.28", "0.125", "0.324"],
                         ["Laplace, cost mixture", r"0.25; $1.2\to3$", "0.250", "0.523", "27.27", "0.125", "0.324"],
                         ["Logistic, cost atoms", r"0.25; $1.2\to3$", "0.250", "0.302", "5.15", "0.125", "0.162"],
                         ["Logistic, cost mixture", r"0.25; $1.2\to3$", "0.250", "0.301", "5.14", "0.125", "0.162"],
                         [r"Moderate values ($h=2$)", r"0.25; $1.05\to1.5$", "0.250", "0.527", "27.68", "0.125", "0.327"],
                         [r"Signals ($a=0.70$, $d=0.75$)", r"0.85; $1.1\to2.3$", "0.850", "0.879", "2.94", "0.425", "0.449"],
                     ],
                     bases=[58.4, 75.0, 86.0, 96.9, 107.9, 118.9, 129.8],
                     top=47.19, bottom=135.49, mids={0: 63.94}),
              items(156.2, [
                  r"Minimum theorem margins: base $2.41\times10^{-3}$, moderate $8.01\times10^{-4}$, "
                  r"signals $1.45\times10^{-3}$",
                  r"Distinct parameter vectors, not one joint calibration; all rows analytical (Props.~2, "
                  r"A.5–A.7); entry $\mathsf E$ = Pr(challenger prepares), $\mathsf O_H$ = high-value "
                  r"ownership; pp from unrounded probabilities",
              ], size="small", gaps=[4.7]),
              takeaway(211.8, r"The rise from $r_0$ to $r_1$ holds in every row; the $r_2$ fall is shown "
                              r"for the benchmark only."),
          ], **back("main:robust")),

    # ------------------------------------------------------------------ A27 (p46)
    Slide("A27", "A higher reserve can raise proceeds; optimal terms are open", page="A27 / 29",
          body=[
              para(53.9, r"Value classes: $p=0.5$ vs $p=1.1$ ($\varepsilon_V=0.05$)", size="small",
                   name="Lead-in"),
              ltable("T Reserve comparison", xs=[21.6, 120.5, 177.0, 209.9, 310.5, 393.8], x_end=431.9,
                     sep=11.96, size="footnote", align=["l", "c", "c", "c", "c", "l"],
                     rows=[
                         ["Economy, reserve", "Preparation", "Sale", "Two admissible bidders",
                          "Expected proceeds", "Trading"],
                         [r"Weak $r=1.2$, $p=0.5$", "0.250", "0.688", "0.146", "0.393", "no trade"],
                         [r"Weak $r=1.2$, $p=1.1$", "0.540", "0.392", "0.0280", "0.432", "full orders"],
                         [r"Strong $r=3$, $p=0.5$", "0.523", "0.920", "0.436", "0.872", "full orders"],
                         [r"Strong $r=3$, $p=1.1$", "0.512", "0.749", "0.200", "1.01", "full orders"],
                     ],
                     bases=[80.1, 96.7, 107.6, 118.6, 129.5], top=68.81, bottom=135.19, mids={0: 85.56}),
              note(153.8, r"Binary values: $p=0.5$ vs $p=1.01$. \status{Analytical at the listed nodes.}"),
              items(174.3, ["Preparation, sale and two admissible bidders come apart"]),
              takeaway(198.1, "A feasible improvement, not an optimal reserve: optimal terms are open."),
          ], **back("main:reserve", [("Same orders, different prices", "app:pool")])),

    # ------------------------------------------------------------------ A28 (p47)
    Slide("A28", "Same orders, different prices", page="A28 / 29",
          body=[
              para(50.5, r"Prop.~A.10 (analytical existence): at reserve $p=7$ and $r_0$, the same full "
                         r"orders $(1,-1)$ support price pools below a cutoff $\kappa\in[-\log2,\,0]$.",
                   size="small", name="Lead-in"),
              ltable("T Price pools", xs=[126.4, 243.3, 303.2], x_end=327.2, sep=11.96, size="small",
                     align=["l", "c", "c"],
                     rows=[
                         ["", r"$\kappa=-\log2$", r"$\kappa=0$"],
                         ["Pooled belief", "0.273", "0.303"],
                         ["Entry", "0.152", "0.125"],
                         ["Expected target proceeds", "0.687", "0.610"],
                     ],
                     bases=[91.3, 108.9, 120.9, 132.8], top=79.36, bottom=138.77, mids={0: 97.11}),
              items(160.0, ["Same orders, different prices, beliefs, and entry",
                            "Does not arise on the benchmark support"], sep=3.0),
              takeaway(197.3, "A continuation must include the price rule, so the seller’s problem "
                              "cannot be solved over orders alone."),
          ], **back("app:reserve")),

    # ------------------------------------------------------------------ A29 (p48)
    Slide("A29", "References", page="A29 / 29",
          body=[
              Text(10.1, y_plain(50.5, "footnote"), 211.5, [
                  P(t, before=(3.0 if k else 0.0)) for k, t in enumerate([
                      r"Betton, Eckbo, Thompson and Thorburn (2014). \i{J. Finance} 69.",
                      r"Boone and Mulherin (2007). \i{J. Finance} 62.",
                      r"Bulow, Huang and Klemperer (1999). \i{J. Polit. Econ.} 107.",
                      "Carlin, Liu, Officer, Pernoud and Tu (2026). NBER Working Paper 34846.",
                      r"Cornelli and Li (2002). \i{Rev. Financ. Stud.} 15.",
                      r"Dow, Goldstein and Guembel (2017). \i{J. Eur. Econ. Assoc.} 15.",
                      r"Edmans, Goldstein and Jiang (2012). \i{J. Finance} 67.",
                      r"Edmans, Goldstein and Jiang (2015). \i{Amer. Econ. Rev.} 105.",
                      r"Fishman (1988). \i{RAND J. Econ.} 19.",
                  ])
              ], size="footnote", name="References 1"),
              Text(231.8, y_plain(50.5, "footnote"), 211.5, [
                  P(t, before=(3.0 if k else 0.0)) for k, t in enumerate([
                      r"Gentry and Stroup (2019). \i{J. Financ. Econ.} 132.",
                      r"Goldstein and Guembel (2008). \i{Rev. Econ. Stud.} 75.",
                      r"Grossman and Hart (1980). \i{Bell J. Econ.} 11.",
                      r"Hirshleifer and Png (1989). \i{Rev. Financ. Stud.} 2.",
                      "Imprivata, Inc. (2016). Definitive merger proxy, Form DEFM14A.",
                      r"Levin and Smith (1994). \i{Amer. Econ. Rev.} 84.",
                      "Lin, Ma, Yang and Zhu (2025). Working paper.",
                      "Liu and Bernhardt (2022). Working paper.",
                      r"Luo (2005). \i{J. Finance} 60.",
                      "Pernoud and Gleyze (2026). Working paper.",
                      r"Persico (2000). \i{Econometrica} 68.",
                      r"Roberts and Sweeting (2013). \i{Amer. Econ. Rev.} 103.",
                  ])
              ], size="footnote", name="References 2"),
          ], **back("main:refs")),
]
