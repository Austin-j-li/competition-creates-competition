"""Slides 1-18 (title + main frames F1-F16, with the F10a/F10b build) of talk/talk.tex.

Declarative content for build_pptx.py; positions are Beamer pt read off talk/build/talk.pdf.
Every number is copied from talk.tex (see its "% source:" comments); edit both together.
"""
from build_pptx import (COST, GRAY, INFO, Box, Cell, Eq, Figure, Flow, P, ResultBox, Slide, Table,
                        Text)

L, W = 10.91, 431.72          # Beamer text margin and text width (pt)
EN = " "                  # \enspace


def bullets(y, paras, size="normal", x=L, w=W, name="Bullets"):
    return Text(x, y, w, paras, size=size, name=name)


def takeaway(y, markup, name="Takeaway"):
    return Text(L, y, W, [P(markup, bullet="dot")], size="normal", name=name)


def gray(y, markup, size="footnote", x=L, w=W, name="Note"):
    return Text(x, y, w, [P(markup, color=GRAY)], size=size, name=name)


SLIDES = [
    # ------------------------------------------------------------------ title (plain, uncounted)
    Slide("F0", r"Competition Creates Competition: \\Stock Prices and the Discovery of Takeover Bidders",
          subtitle="Austin Li", kind="title"),

    # ------------------------------------------------------------------ F1 key question
    Slide("F1", "Does a stronger incumbent keep the challenger out?",
          subtitle="The decision interval this paper is about", page="1 / 16",
          body=[
              Flow(name="D0 decision interval", size="footnote", boxes=[
                  Box(28.45, 51.68, 116.53, 24.09, r"Approach or\\review disclosed", pad=(2, 1, 2, 1)),
                  Box(168.26, 51.68, 116.53, 24.09, "Target stock keeps trading", pad=(2, 1, 2, 1)),
                  Box(308.31, 51.18, 116.53, 25.09, r"Challenger decides\\whether to pay to prepare",
                      edge=COST, lw=1.1, pad=(2, 1, 2, 1)),
              ], arrows=[(0, 1), (1, 2)]),
              bullets(86.6, [
                  P(r"The \b{incumbent} bidder is already prepared; the market knows how strong it is, "
                    r"not what it will bid", bullet="ball"),
                  P(r"A \b{challenger} must first pay to prepare an executable bid (diligence, financing, "
                    r"approvals); paying is \b{entry}", bullet="ball", before=3.5),
                  P(r"\b{Received answer:} a stronger rival lowers what preparation earns, so it deters "
                    r"entry \cite{Fishman 1988; Hirshleifer and Png 1989}", bullet="ball", before=3.5),
                  P(r"\b{But} the challenger decides while the stock trades, and it can watch the price",
                    bullet="ball", before=3.5),
                  P(r"\foot{Imprivata’s 2016 proxy separates an unsolicited approach, outreach to potential "
                    r"buyers, and indications of interest conditional on further diligence: a costly "
                    r"preparation stage, not a price drawing anyone in}", bullet="none", before=4.0,
                    color="616161"),
              ], size="small"),
              takeaway(206.4, r"\key{The twist:} what that price reveals depends on how strong the incumbent is"),
          ],
          nav=[("Which deals fit", "app:interval"), ("Evidence: a design", "app:evidence")]),

    # ------------------------------------------------------------------ F2 this paper
    Slide("F2", "This paper", page="2 / 16",
          body=[
              Text(L, 37.5, W, [
                  P("An informed investor trades the target’s stock, which pays off from the sale price, "
                    "before a challenger decides whether to pay to prepare a takeover bid; prices are "
                    "rational, and trading and entry are solved in equilibrium."),
                  P(r"\key{Competition creates competition} \status{(analytical)}: a stronger incumbent can "
                    r"turn an uninformative stock price into an informative one and raise entry",
                    bullet="ball", before=4.2),
                  P(r"\small{Benchmark: entry \b{0.250 $\boldsymbol{\to}$ 0.523} while the challenger’s "
                    r"profit before any news falls \b{4.80 $\boldsymbol{\to}$ 4.29}}", bullet="none",
                    before=0.5),
                  P(r"\b{One auction, two claims:} a strong incumbent can beat a low-value challenger but "
                    r"not a high-value one, so the challenger keeps less while the sale price depends more "
                    r"on who shows up; informed trading puts that into the stock price, and good news "
                    r"justifies expensive preparation", bullet="ball", before=2.5),
                  P(r"\b{Information is the channel:} hold fixed what the price reveals, and a stronger "
                    r"incumbent cannot raise entry, as the textbook says "
                    r"\status{(sign analytical, Prop.~A.3)}", bullet="ball", before=2.5),
              ], name="Body"),
              takeaway(212.5, r"\b{Implication:} when the target trades, a stronger rival is not a pure "
                              r"deterrent, because who competes depends on what the price reveals before "
                              r"anyone prepares."),
          ]),

    # ------------------------------------------------------------------ F3 positioning
    Slide("F3", "What is new relative to learning from prices", subtitle="Four closest antecedents",
          page="3 / 16",
          body=[
              bullets(61.6, [
                  P(r"\b{Prices guide real decisions} \cite{Dow, Goldstein and Guembel 2017; Edmans, "
                    r"Goldstein and Jiang 2015}: here the sale rule splits one surplus into a traded claim "
                    r"and the challenger’s claim, and competition moves them in opposite directions",
                    bullet="ball"),
                  P(r"\b{Stronger incumbents deter} \cite{Fishman 1988}: kept intact; I add a market that "
                    r"trades before preparation", bullet="ball", before=8.7),
                  P(r"\b{Auction entry is endogenous} \cite{Levin and Smith 1994}: here entry responds to "
                    r"what the price reveals", bullet="ball", before=8.7),
              ]),
              takeaway(187.8, "Increment: one sale rule moves the two claims oppositely, producing the "
                              "entry reversal."),
          ],
          nav=[("Related work", "app:lit"), ("References", "app:refs")]),

    # ------------------------------------------------------------------ F4 model (D1 timeline)
    Slide("F4", "Model: who moves, who knows what, and when",
          subtitle=r"The challenger sees the price and its own cost, never the order flow, $\theta$ or $R$",
          page="4 / 16",
          body=[
              # explicit line breaks reproduce the Beamer box line breaks (Calibri sets narrower)
              Flow(name="D1 model timeline", size="footnote", boxes=[
                  Box(14.8 + 87.4 * k, 57.1, 77.4, 73.2,
                      [P(r"\b{%s}" % name, hang=(7.0, 0.0)), P(body, before=0.9)],
                      align="l", anchor="t", number=str(k + 1), pad=(4.2, 2.2, 2.5, 2.0),
                      edge=COST if k == 3 else "737373", lw=1.1 if k == 3 else 0.6)
                  for k, (name, body) in enumerate([
                      ("Seller", r"commits to a\\cash second-price\\auction, reserve $p$"),
                      ("Investor", r"knows $\theta$; trades\\the target’s stock\\against noise\\traders"),
                      ("Market makers", r"see only total\\order flow; price\\the share at\\expected sale\\proceeds"),
                      ("Challenger", r"sees the price\\and its cost $C$;\\entry $=$ pay $C$,\\learn $\theta$, can bid"),
                      ("Bidders", r"incumbent value\\$R\sim U[0,r]$;\\challenger worth\\$h$ or $\ell$; bid\\truthfully"),
                  ])
              ], arrows=[(0, 1), (1, 2), (2, 3), (3, 4)]),
              bullets(146.6, [
                  P(r"$0<p<\ell<r<h$ ($p$ = reserve, not the stock price): the incumbent can beat a "
                    r"low-value challenger, never a high-value one. Strength $r$ is public; only the "
                    r"incumbent knows its value $R$. Quality $\theta\in\{H,L\}$ (worth $h$ or $\ell$), "
                    r"equally likely, learned only by preparing.", bullet="ball"),
                  P(r"\cost{\b{Cost:} preparation cost $C\in\{c_L,c_H\}$, $\Pr(C=c_L)=\rho$, independent "
                    r"of $\theta$ (cheap / expensive preparation)}", bullet="ball", before=5.5),
              ], size="small"),
          ],
          nav=[("What is left out", "app:omit"), ("Why would the investor know?", "app:info"),
               ("Equilibrium", "app:eq")]),

    # ------------------------------------------------------------------ F5 one auction, two claims
    Slide("F5", "One auction, two claims, opposite responses",
          subtitle=r"Cash second-price auction with reserve $p$: who wins and who pays at incumbent value $R$",
          page="5 / 16",
          body=[
              Table(30.0, 57.4, [80.0, 103.0, 110.0, 101.0], [
                  ["Incumbent value", "High-value challenger", "Low-value challenger", "Gap in target proceeds"],
                  [r"$R\le\ell$", r"wins, pays $\max\{p,R\}$", r"wins, pays $\max\{p,R\}$", "$0$"],
                  [r"$R>\ell$", r"wins, pays $R$", r"loses; incumbent pays $\ell$", r"$R-\ell$"],
              ], size="small", row_h=[17.7, 14.85, 14.85], name="T1 payment comparison"),
              Text(L, 111.6, 200, [P(r"As incumbent strength $r$ rises:")], size="small", name="Lead-in"),
              Eq(30.2, 127.4, r"\Info{\Delta_T=t_H-t_L=\mathbb{E}[(R-\ell)_+]\ \uparrow}", size="normal",
                 name="Spread equation"),
              Eq(39.2, 143.6, r"g_H=\mathbb{E}[(h-\max\{p,R\})_+]\ \downarrow", size="normal",
                 name="Profit equation"),
              Text(193.0, 127.6, 249.6, [P(r"\info{target-payoff spread = expected gap (last column)}")],
                   name="Spread label"),
              Text(193.0, 144.4, 249.6, [P(r"challenger’s gross profit ($g_L$ likewise)")],
                   name="Profit label"),
              gray(175.6, r"$t_\theta$ = expected target proceeds when a $\theta$-challenger enters. "
                          r"Proposition 1 (analytical): both signs hold weakly for any first-order "
                          r"strengthening, $R\sim F$ on $[0,\bar r]$, $\ell<\bar r<h$ (strictly in the "
                          r"uniform benchmark, $\bar r=r$)."),
              takeaway(205.9, "One shift, opposite signs: challenger keeps less; target proceeds depend "
                              "more on who it is."),
          ],
          nav=[("Closed forms", "app:payoffs"), ("Other payment rules", "app:payrule")]),

    # ------------------------------------------------------------------ F6 X1
    Slide("F6", "A stronger incumbent: spread up, profit down",
          subtitle=r"Declared benchmark; weak $r_0=1.2$, strong $r_1=3$; auction-stage payoffs, before "
                   r"trading and entry",
          page="6 / 16",
          body=[
              Figure(28.6, 46.2, 396.4, 145.5, "two_returns_talk",
                     alt="Two panels against incumbent strength r from 1 to 3.8. (a) target-payoff spread "
                         "Delta_T rises from 0.0167 at weak r0 = 1.2 to 0.667 at strong r1 = 3. "
                         "(b) challenger's expected profit at the prior falls from 4.80 to 4.29."),
              Text(250.0, 196.8, 192.6, [P(r"\status{analytical (Proposition 1)}", align="r")],
                   name="Status"),
              takeaway(212.6, r"From $r_0$ to $r_1$ the \info{spread} rises 0.0167 $\to$ 0.667 while profit "
                              r"at the prior (before any news) falls 4.80 $\to$ 4.29: deterrence at every "
                              r"fixed belief, and more for the stock to reveal."),
          ]),

    # ------------------------------------------------------------------ F7 trading pays only when strong
    Slide("F7", "Trading pays only against a strong incumbent",
          subtitle=r"Orders $(q_H,q_L)\in[-1,1]$ after a high / low challenger value; trading cost $k$ per "
                   r"unit; prices anticipate entry",
          page="7 / 16",
          body=[
              Text(L, 48.6, W, [
                  P(r"The price reveals the market’s belief $\mu=\Pr(H)$, kept by noise within $[m,M]$: "
                    r"$m=1/(1+e^{2/b})\approx0.27$, $M=1-m$ (Laplace noise, scale $b=2$)"),
                  P(r"\b{Residual advantage} = what the investor knows a share pays minus its price; "
                    r"entry $\ge\rho$ because cheap preparation pays after any price (the low-cost floor, "
                    r"next frame).", before=3.0),
              ], size="small", name="Body"),
              Table(14.9, 103.0, [133.5, 82.9, 20.0, 82.9, 20.0, 84.4], [
                  ["Residual advantage per unit =", r"entry probability\\$(\ge\rho)$", r"$\times$",
                   r"\info{target-payoff\\spread $\Delta_T$}", r"$\times$",
                   r"market’s remaining\\uncertainty $(\ge m)$"],
              ], size="small", align=["l", "c", "c", "c", "c", "c"], row_h=[29.8], midrules=(),
                  valign="t", pad_v=2.6,
                  name="T2 residual advantage"),
              Eq(226.8, 135.7, r"\rho\,m\,\Info{\Delta_T}\ \le\ \text{advantage}\ \le\ \Info{\Delta_T}",
                 size="small", anchor="c", name="Advantage bound"),
              bullets(151.6, [
                  P(r"\b{Weak $r_0=1.2$:} advantage $\le\Delta_T(r_0)=0.0167{}<k=0.02$, so every order "
                    r"loses; no trade $(0,0)$", bullet="ball"),
                  P(r"\b{Strong $r_1=3$:} each extra unit earns $\ge(1-1/b)\,\rho m\Delta_T(r_1)=0.0224>k$, "
                    r"so full orders $(1,-1)$", bullet="ball", before=1.6),
              ], size="small"),
              gray(181.6, r"\info{\b{Trading-cost window}} $\Delta_T(r_0)<k<(1-1/b)\,\rho m\Delta_T(r_1)$ "
                          r"(analytical): with $\rho=0.25$, $(1-1/2)\times0.25\times m\times0.667=0.0224="
                          r"k+{}$theorem margin 0.00241."),
              takeaway(206.8, "The same shift that lowers the challenger’s profit switches informed "
                              "trading on."),
          ],
          nav=[("Global trading bound", "app:bound"), ("Orders, units, costs", "app:orders"),
               ("Notation", "app:notation")]),

    # ------------------------------------------------------------------ F8 X2
    Slide("F8", "Only good news makes expensive preparation pay",
          subtitle=r"$B_r(\mu)=g_L+\mu(g_H-g_L)$ at the worst, prior and best belief a price induces; "
                   r"$c_L=1$ (prob.~$\rho=0.25$), $c_H=6$",
          page="8 / 16",
          body=[
              Figure(10.9, 54.4, 243.5, 169.1, "profit_thresholds_talk",
                     alt="Challenger's profit B_r(mu) against incumbent strength r at the best price (M), "
                         "the prior and the worst price (m), with the expensive cost c_H = 6 and the cheap "
                         "cost c_L = 1 as horizontal lines; verticals at weak r0 = 1.2, strong r1 = 3 and "
                         "stronger still r2 = 3.6."),
              Text(278.9, 55.8, 163.7, [
                  P(r"\cost{\b{Low-cost floor}}" + EN + r"$c_L<B_{r_1}(m)$: a cheap challenger enters "
                    r"after any price, so entry $\ge\rho$ (the bound used on the previous frame)"),
                  P(r"\cost{\b{High-cost window}}" + EN + r"$B_{r_0}(1/2)=4.80<c_H=6<B_{r_1}(M)$: the "
                    r"expensive challenger stays out at the weak prior and enters after the best news "
                    r"against $r_1$. Beyond a ceiling strength, even the best price falls short ($r_2$)",
                    before=6.0),
                  P(r"\status{analytical (Props.~A.1, A.2, A.4); costs are inputs}", before=5.0),
              ], size="small", name="Conditions"),
          ],
          nav=[("Reading the price", "app:suff"), ("Why Laplace noise", "app:laplace"),
               ("Is the floor doing the work?", "app:floor")]),

    # ------------------------------------------------------------------ F9 Proposition 2
    Slide("F9", "Proposition 2: a stronger incumbent can raise entry",
          subtitle=r"Weak $r_0$, strong $r_1$, stronger still $r_2$; all other primitives equal",
          page="9 / 16",
          body=[
              ResultBox(10.9, 53.7, 431.7, 83.6,
                        "Proposition 2 (analytical), under the three conditions below", [
                            P("(i)\t" + r"\b{Weak $r_0$:} unique outcome no trade, $(q_H,q_L)=(0,0)$; the "
                              r"price is uninformative; entry $=\rho$", hang=(18.9, -18.9), line_pt=12.0),
                            P("(ii)\t" + r"\b{Strong $r_1$:} unique outcome full orders $(1,-1)$; the price "
                              r"is informative; entry $>\rho$; a high-value challenger acquires the target "
                              r"more often", hang=(18.9, -18.9), line_pt=12.0),
                            P("(iii)\t" + r"\b{Stronger still, $r_2$,} where the low-cost floor and "
                              r"profitable trading persist but $B_{r_2}(M)<c_H$: full orders, entry back "
                              r"to $\rho$", hang=(18.9, -18.9), line_pt=12.0),
                        ], size="small", title_h=15.5),
              Table(10.9, 144.6, [102.1, 155.0], [
                  [r"\cost{\b{Low-cost floor}}", r"$c_L<B_{r_1}(m)$"],
                  [r"\cost{\b{High-cost window}}", r"$B_{r_0}(1/2)<c_H<B_{r_1}(M)$"],
                  [r"\info{\b{Trading-cost window}}", r"$\Delta_T(r_0)<k<(1-1/b)\,\rho m\Delta_T(r_1)$"],
              ], size="small", rules=False, pad=0.0, row_h=13.3, name="Conditions"),
              gray(153.6, r"(i)–(ii) on a nonempty open set of primitives, every $h>\ell$; (iii) at the "
                          r"benchmark and nearby. Uniqueness: arbitrary mixed orders; every unilateral "
                          r"deviation $q\in[-1,1]$.", x=270.1, w=172.5, name="Scope"),
              takeaway(198.9, r"\info{wider $\Delta_T$ $\to$ informed trading pays $\to$ informative price "
                              r"$\to$ good news clears $c_H$ $\to$ the expensive challenger enters}"),
          ],
          nav=[("Proof logic", "app:proof"), ("Margins", "app:margins"),
               ("Two forces side by side", "app:forces")]),
]

# ------------------------------------------------------------------ F10a / F10b benchmark table
_T3_HEAD = ["", r"weak\\$r_0=1.2$", r"\b{strong}\\$\boldsymbol{r_1=3}$"]
_T3_ROWS = [
    [r"Challenger’s profit at the prior $B_r(1/2)$", "4.80", r"\b{4.29}"],
    [r"\info{Target-payoff spread $\Delta_T$}", "0.0167", r"\b{0.667}"],
    [r"Investor orders $(q_H,q_L)$", "$(0,0)$", r"$\boldsymbol{(1,-1)}$"],
    ["Price", "uninformative", r"\b{informative}"],
    ["Entry", "0.250", r"\b{0.523}"],
    ["High-value ownership", "0.125", r"\b{0.324}"],
]
_T3_R2 = [r"stronger still\\$r_2=3.6$", r"\i{\gray{lower still}}", r"\i{\gray{wider still}}", "$(1,-1)$",
          "informative", "0.250", "0.125"]
_ENTRY_NOTE = (r"Entry = Pr(challenger prepares); entry $\rho=0.25$ = only the cheap challenger enters; "
               r"high-value challenger ownership = Pr(high-value challenger acquires the target)")
_T3_SUB = "Declared benchmark; units arbitrary (inputs in backup); unique equilibrium outcomes (analytical)"


def _t3(y, with_r2):
    rows = [_T3_HEAD + ([_T3_R2[0]] if with_r2 else [])]
    for k, r in enumerate(_T3_ROWS):
        rows.append(r + ([_T3_R2[k + 1]] if with_r2 else []))
    cols = [178.9, 74.4, 74.4] + ([74.4] if with_r2 else [])
    cols[-1] = 68.4
    return Table(30.8, y, cols, rows, size="small", align=["l"] + ["c"] * (len(cols) - 1),
                 row_h=[29.7] + [12.9] * 6, name="T3 benchmark" + (" with r2" if with_r2 else ""))


SLIDES += [
    Slide("F10a", "At the benchmark, entry rises from 0.250 to 0.523", subtitle=_T3_SUB, page="10 / 16",
          body=[
              Text(L, 57.6, W, [P(_ENTRY_NOTE)], size="footnote", name="Definitions"),
              _t3(84.1, False),
              takeaway(198.9, "Entry rises 27.28 percentage points while the challenger’s profit at the "
                              "prior falls: the price, not the prize, brings it in."),
          ]),
    Slide("F10b", "At the benchmark, entry rises from 0.250 to 0.523", subtitle=_T3_SUB, page="10 / 16",
          body=[
              Text(L, 53.6, W, [P(_ENTRY_NOTE)], size="footnote", name="Definitions"),
              _t3(79.9, True),
              takeaway(194.9, r"Rise, then fall: past a ceiling strength even the best price cannot "
                              r"cover $c_H$."),
          ],
          nav=[("Benchmark scale", "app:scale"), ("How entry is computed", "app:entry"),
               ("Which equilibrium?", "app:cert")]),

    # ------------------------------------------------------------------ F11 freeze the information
    Slide("F11", "Freeze the information and deterrence returns",
          subtitle=r"Entry at $r_0=1.2$ and $r_1=3$; equilibria of the feedback game, then information "
                   r"controls",
          page="11 / 16",
          body=[
              Table(14.2, 48.5, [173.2, 47.0, 39.0, 49.8, 116.2], [
                  ["", r"$r_0=1.2$", r"$r_1=3$", "Direction", "Status"],
                  [r"Equilibrium of the feedback game\\\foot{(price seen, trading re-solved)}", "0.250",
                   r"\b{0.523}", r"$\uparrow$", r"\statusf{analytical}"],
                  [Cell(r"\i{Information controls}", span=5)],
                  [r"Frozen informative orders $(1,-1)$\\\foot{(imposed at both strengths; control, not "
                   r"an equilibrium at $r_0$)}", "0.562", "0.523", r"$\downarrow$",
                   r"\statusf{numerical diagnostic;\\sign analytical (Prop.~A.3)}"],
                  [r"Price hidden from challenger\\\foot{(equilibrium of the no-price-access game)}",
                   "0.250", "0.250", "flat", r"\statusf{analytical}"],
              ], size="small", align=["l", "c", "c", "c", "l"], row_h=[17.8, 29.5, 14.0, 37.0, 26.5],
                  midrules=(0, 1), name="T4 information controls"),
              gray(176.6, "The price-hidden row is implied by the high-cost window. Without the price, "
                          "expensive preparation never pays and only the entry floor remains."),
              takeaway(206.6, "Hold the price’s information fixed and a stronger incumbent weakly lowers "
                              "entry."),
          ],
          nav=[("Controls in detail", "app:controls"), ("Price level or information?", "app:welfare")]),

    # ------------------------------------------------------------------ F12 coexistence
    Slide("F12", "At intermediate strength, equilibria coexist",
          subtitle="Computer-assisted (Proposition 3): interval arithmetic on exact decimal inputs",
          page="12 / 16",
          body=[
              Table(28.2, 56.1, [60.0, 125.0, 110.0, 102.2], [
                  [r"Strength $r$", r"$q_H$", r"$q_L$ (certified)", "Entry (certified)"],
                  ["1.55", "1", r"$\approx-0.460$", r"$\approx0.545$"],
                  ["1.60", "1", r"$\approx-0.707$", r"$\approx0.549$"],
                  ["1.65", "1", r"$\approx-0.903$", r"$\approx0.551$"],
              ], size="small", align="c", row_h=[20.2, 16.3, 16.3, 16.3], name="T5 certified equilibria"),
              bullets(132.6, [
                  P("Buy fully after good news, sell partially after bad news; certified entry rises from "
                    "one strength to the next, above the 0.523 at $r_1$", bullet="ball"),
                  P(r"Each economy also has a no-trade equilibrium with entry $\rho=0.25$ "
                    r"\status{(analytical, Prop.~A.4)}", bullet="ball", before=3.2),
                  P("Elsewhere the numerical search is not exhaustive; the full correspondence is open",
                    bullet="ball", before=3.2),
              ]),
              takeaway(199.9, "At three certified strengths an informative equilibrium coexists with no "
                              "trade; I claim nothing about entry between them."),
          ],
          nav=[("Correspondence", "app:corr")]),

    # ------------------------------------------------------------------ F13 robustness
    Slide("F13", "The entry reversal survives four model changes",
          subtitle="Entry, weak to strong; each row its own analytical result and declared parameters "
                   "(Prop.~2 (i)–(ii))",
          page="13 / 16",
          body=[
              Table(42.0, 51.8, [300.8, 35.4, 33.4], [
                  ["Specification", "Weak", "Strong"],
                  ["Benchmark: Laplace noise, two cost levels", "0.250", "0.523"],
                  ["Atomless costs, half-width 0.1", "0.250", "0.523"],
                  ["Logistic noise", "0.250", "0.302"],
                  [r"Small value gap, $h=2$, $\ell=1$", "0.250", "0.527"],
                  [r"Complementary signals (declared example): investor accuracy 0.70,\\challenger "
                   r"accuracy 0.75; $\rho=0.85$, strengths 1.1 vs 2.3", "0.850", "0.879"],
              ], size="small", align=["l", "c", "c"], valign=["m"] * 5 + ["t"],
                  row_h=[17.8, 14.9, 12.3, 12.3, 12.3, 26.6], name="T6 robustness"),
              Text(L, 150.6, W, [
                  P(r"Rows differ in $\rho$ and strengths; compare within a row, not across rows.",
                    color=GRAY),
                  P(r"Signal grid, 25 accuracy cells: entry rises in the 6 meeting Prop.~A.7 (analytical) "
                    r"and is unchanged in 9 with challenger accuracy ${}\le0.75$; it falls about 4~pp when "
                    r"challenger accuracy is ${}\ge0.76$, because its own good signal already triggers "
                    r"entry against the weak incumbent (numerical diagnostic).", before=2.0, color=GRAY),
              ], size="footnote", name="Notes"),
              takeaway(199.9, r"The $r_0\to r_1$ reversal survives atomless costs, logistic noise, a small "
                              r"value gap and complementary private signals (declared example)."),
          ],
          nav=[("Full table", "app:robust")]),

    # ------------------------------------------------------------------ F14 price access and welfare
    Slide("F14", r"Price access raises proceeds and surplus at $r_1$",
          subtitle=r"Incumbent held at $r_1=3$; price seen or hidden; trading re-solved in both "
                   r"(Prop.~A.9, analytical)",
          page="14 / 16",
          body=[
              Table(28.2, 64.3, [205.8, 80.0, 74.0, 37.4], [
                  ["", "Price observed", "Price hidden", "Gain"],
                  ["Expected target proceeds", "0.872", "0.615", "0.258"],
                  ["Acquisition surplus net of preparation costs", "2.38", "2.30", "0.0802"],
              ], size="normal", align=["l", "c", "c", "c"], row_h=[22.7, 19.85, 19.85], pad=1.5,
                  name="T7 price access"),
              bullets(138.6, [
                  P("Same full orders in both economies, so trading costs coincide", bullet="ball"),
                  P("Each extra entry happens only when its expected profit covers its cost",
                    bullet="ball", before=4.7),
              ]),
              gray(197.6, r"Gain from unrounded values. At $r_0$ prices are uninformative, so there is no "
                          r"gain. The comparison does not rank incumbent strengths or sale mechanisms."),
          ],
          nav=[("Reserve", "app:reserve")]),

    # ------------------------------------------------------------------ F15 empirical design
    Slide("F15", "What an empirical test would have to measure",
          subtitle="A design in the paper, not a result", page="15 / 16",
          body=[
              bullets(72.6, [
                  P(r"\b{Outcome:} the start of substantive diligence or a proposal that needs costly "
                    r"preparation, not the number of public offers", bullet="ball"),
                  P(r"\b{Strength:} measured from information public before that decision", bullet="ball",
                    before=8.7),
                  P(r"\b{Timing:} price information must precede preparation; a traded stock during "
                    r"confidential negotiations is not enough", bullet="ball", before=8.7),
                  P(r"\b{Caution:} later target returns can reflect anticipated bidder arrival, so returns "
                    r"followed by entry do not by themselves show learning from prices", bullet="ball",
                    before=8.7),
              ]),
              gray(198.6, "Design only; no sample, effect, instrument or identification strategy is "
                          "reported (Online Appendix D pilot)"),
          ]),

    # ------------------------------------------------------------------ F16 conclusion
    Slide("F16", "Conclusion", page="16 / 16",
          body=[
              bullets(65.6, [
                  P(r"\key{A stronger incumbent can bring the challenger in:} at the benchmark, entry "
                    r"rises from 0.250 to 0.523 although the challenger’s expected profit before any "
                    r"news falls", bullet="ball"),
                  P(r"\b{Why:} competition makes target proceeds more sensitive to who the challenger is; "
                    r"informed trading puts that into the price; good news draws in the expensive "
                    r"challenger. Freeze that information and deterrence returns.", bullet="ball",
                    before=20.5),
                  P(r"\b{Implication:} when the target trades, a stronger rival is not a pure deterrent, "
                    r"because who competes depends on what the price reveals before anyone prepares.",
                    bullet="ball", before=20.5),
              ]),
          ]),
]
