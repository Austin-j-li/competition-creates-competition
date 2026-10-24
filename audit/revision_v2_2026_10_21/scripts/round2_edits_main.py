"""Round-2 edits to main.tex. Imported by round2.py.

Item codes in the notes: M = R_math.md, C = R_consistency.md, P = R_prose_latex.md,
F = R_referee.md ranked fix list, D = the round's decisions in the task brief.
"""


def R(eid, old, new, count, why):
    return {"id": eid, "kind": "R", "old": old, "new": new, "count": count, "why": why}


def B(eid, start, end, new, why):
    return {"id": eid, "kind": "B", "start": start, "end": end, "new": new, "why": why}


def S(eid, start, end, pairs, why):
    return {"id": eid, "kind": "S", "start": start, "end": end, "pairs": pairs, "why": why}


ABSTRACT = r"""\begin{abstract}
A stronger incumbent bidder can attract a challenger by making the
target's stock price more informative. I study a takeover auction in
which a prospective buyer sees the price before it pays to prepare a
bid. A stronger incumbent lowers the buyer's acquisition profit at
every belief about its quality. It also makes the proceeds of target
shareholders more sensitive to that quality. An investor who knows the
buyer's quality class therefore gains more from trading on it. For a
set of parameters with positive measure, a stronger incumbent turns an
uninformative price into an informative one. In each economy the
trading and preparation outcomes are unique. Challenger participation
rises, and so does the probability that a challenger from the
high-value class acquires the target. If the information in the price
is held fixed, stronger competition lowers participation. The reversal
also holds when the buyer has a more accurate private signal than the
investor. In the strong-incumbent economy, access to prices raises
expected target proceeds and acquisition surplus net of preparation
costs.
\end{abstract}"""

ROBUSTNESS = r"""The reversal holds at some incumbent strengths and costs for every prior and every pair of classes that differ above the reserve, when the high class has stochastically higher values and both class supports lie above the reserve. It holds for every noise law whose score bound is below one (\hyperref[result-proposition-a-5]{Proposition A.5}). At a given bound, Laplace noise gives the most informative flow experiment at every pure order profile. The size of the effect depends on the noise law: in the strong benchmark economy, entry is 0.522757 under Laplace noise and 0.301509 under logistic noise, against a floor of 0.250000 (\hyperref[sec-noise-and-preparation-costs]{Section 5.1}). The reversal survives atomless preparation costs and private signals that the buyer and the investor hold about different facts, including a buyer signal more accurate than the investor's."""

STAKE = r"""Noise then lets an acquirer conceal share purchases before a bid
(\citeproc{ref-KyleVila1991}{Kyle and Vila 1991}). Large holders trade
on their information (\citeproc{ref-Edmans2009}{Edmans 2009}), monitor,
or intervene as prices feed back to firm decisions
(\citeproc{ref-EdmansGoldsteinJiang2015}{Edmans et al. 2015},
Section II.E; \citeproc{ref-Maug1998}{Maug 1998};
\citeproc{ref-BackEtAl2018}{Back et al. 2018}). The baseline investor
in this paper holds no stake, seeks no control, and earns only the
trading residual; a stake enters only as an extension (Online Appendix
A.12)."""

RESTRICTIONS = r"""Two restrictions rank the classes. The high class, or high-value class,
dominates the low class in the sense of first-order stochastic
dominance, and both class supports lie above the reserve, so that every
value meets it:

\[
G_H(u)\le G_L(u)\quad\text{for every }u,\qquad
G_H(p^-)=G_L(p^-)=0.
\]

Under these restrictions competition widens the class difference in
target proceeds under every incumbent distribution
(\hyperref[result-proposition-1]{Proposition 1}).
\hyperref[pa-results]{Appendix A.1} characterizes the weakest
restriction of this kind. When neither class has a value atom at the
reserve, the spread rises under every strengthening exactly when the
high class dominates above the reserve and the two classes are equally
likely to fall below it, which I call equal admissibility.
\hyperref[sec-design]{Section 6.3} studies a reserve that excludes the
low class, where equal admissibility fails. The structure is the
selective-entry structure of the auction literature. The class indexes
the distribution of the challenger's value, preparation reveals the
value, and the stock price is the pre-entry signal."""

COST = r"""\(c_H>0\). The low cost is zero: a zero-cost challenger is a ready
buyer whose diligence costs nothing at the margin. There is one
challenger. Its cost is zero with probability \(\rho\) and \(c_H\)
otherwise. Paying \(C\) reveals \(\theta\) and permits bidding;
declining leaves the challenger outside the sale. The pair
\((j,\theta)\), the incumbent's value, the preparation cost, and noise
demand are mutually independent, so the cost carries no information
about the class or the value. Conditional on the class, the
challenger's value is independent of flow."""

AUCTION = r"""Before trading, the seller publicly commits to a cash second-price
auction with reserve \(p>0\). The highest admissible bidder acquires the
target and pays the larger of the reserve and the highest competing
admissible bid. There is no sale without an admissible bid. Both bidders
use truthful, weakly dominant bids (\citeproc{ref-Vickrey1961}{Vickrey
1961}; \citeproc{ref-Krishna2010}{Krishna 2010}, Section 2.2), and a
prepared challenger whose value is below the reserve does not bid.
Without a challenger the incumbent buys at the reserve when its value
meets it, so expected no-entry proceeds are \(t_0=p[1-F(p)]\): the board
collects its announced walk-away price from a lone prepared bidder whose
value meets it. A bid equal to the reserve is admissible, and a challenger
indifferent about preparation enters. Because \(F\) is continuous,
acquisition-value ties have probability zero. Preparation indifference
matters at a posterior plateau considered in Section 4, and for the
zero-cost challenger where gross profit is zero, as at the highest
reserve of \hyperref[pa-design]{Appendix A.7}."""

NOISE = r"""Here \(V_T\) is the terminal payoff of a target share and \(Z\) is
independent noise demand with a Laplace density. Up to a constant, its
logarithm is \(-|z|/b\), with slope \(\pm 1/b\). For each pair of
feasible orders, the likelihood ratio of a flow then lies in
\([e^{-2/b},e^{2/b}]\). No order flow is conclusive, in the sense of
bounded private beliefs (\citeproc{ref-SmithSorensen2000}{Smith and
S{\o}rensen 2000}). Each posterior stays in the interval
\([m(\pi),M(\pi)]\) of \hyperref[sec-inference]{Section 3.2}, so the
investor keeps a residual advantage at each flow. A change in the order
also changes the flow density by at most the fraction \(1/b\) of its
level. With \(b>1\), this score bound gives a lower bound on marginal
trading profit on the full order interval. The bound covers mixed orders
and each deviation, and it gives uniqueness in
\hyperref[result-proposition-2]{Proposition 2}. Every density with
\(|(\log f)'|\le 1/b\) has the same two properties. Laplace noise is the
extreme member of this class
(\hyperref[sec-noise-and-preparation-costs]{Section 5.1}), and
\hyperref[result-proposition-a-5]{Proposition A.5} states
\hyperref[result-proposition-2]{Proposition 2} for the whole class.

Three standard models give a Laplace law with scale \(b\). Net noise
demand has this law if noise buy volume and noise sell volume are
independent exponential variables with mean \(b\). It has this law if
it is Gaussian with an exponential variance
(\citeproc{ref-KotzKozubowskiPodgorski2001}{Kotz et al. 2001}), as when
the variance reflects a random level of liquidity trading. It has this
law if noise flow follows a Brownian motion up to an independent
exponential time, such as the arrival of public news. The last model is
the subordination device of Clark (\citeproc{ref-Clark1973}{1973}).
Every member of the class with median zero has tails at least as fat as
an exponential tail (Online Appendix A.6), and asset returns also have
tails fatter than Gaussian tails (\citeproc{ref-Cont2001}{Cont 2001}).
The results rest on tail weight and bounded inference."""

SEQUENCE = r"""incumbent knows its own value. The sequence is as follows. The seller
announces the sale rule. The investor learns the class and trades.
Market makers set the price from flow. The challenger observes the price
and its cost and decides whether to prepare. Prepared bidders learn
their values and submit truthful bids. Ownership and financial payoffs
are realized."""

PROP1 = r"""strengthening of \(F\). (a) For every pair of classes, it weakly
decreases \(g_H\) and \(g_L\), and hence gross acquisition profit at
every fixed belief. (b) Under the restrictions of
\hyperref[sec-values-preparation-and-the-sale]{Section 2.2}, it weakly
increases the target-payoff spread. The decrease in \(g_j\) is strict
when \(\int_p^\infty[1-G_j(u)][F(u)-\tilde F(u)]\,du>0\), and the
increase in (b) is strict when
\(\int_p^\infty[F(u)-\tilde F(u)]D(u)\,du>0\).}"""

FLOOR = r"""A zero-cost challenger pays nothing and prepares after every price.
The floor does three jobs in the proofs. Entry stays at least
\(\rho\), so the denominator in \eqref{eq:paper-10} stays positive
and the price reveals the market's posterior. The residual advantage
stays at least \(\rho\kappa(\pi)\Delta_T\) at every flow
\eqref{eq:paper-11}, the bound that \eqref{eq:paper-a3} sets against
the trading cost. Zero-cost preparation does not respond to the price,
so information can only add entry. The floor \(\rho>0\) is therefore an
assumption with content: at \(\rho=0\), entry can vanish at unfavorable
prices, the price need not reveal the posterior, and the residual has no
positive lower bound. Gross profit is an expected auction rent and never
falls below zero. Any positive low cost below \(B_F(m(\pi))\) in every
economy in the comparison gives the same orders, prices, and entry,
because such a cost is covered at every feasible belief and the
low-cost challenger again prepares at every price."""

WORST_CASE = r"""\(\pi\) that involves no unit of money. A prior away from one half
narrows the window, since \(\kappa(\pi)<m\) there.

The trading bound in \eqref{eq:paper-a3} is a worst case over every
candidate schedule and every mixture, so the proposition certifies a
corner of the region in which the reversal occurs.
\hyperref[sec-coexistence-and-the-equilibrium-correspondence]{Section
4.3} reports what lies between the two benchmark strengths. No trade is
the unique outcome below a sufficient bound and remains an equilibrium
up to an existence boundary. Three informative equilibria are certified
between these two bounds, and each coexists with no trade. Full orders
are unique above a second sufficient bound. None of these bounds locates
the first informative equilibrium."""

SECTION_5_1 = r"""The reversal holds for the class of noise laws of
\hyperref[sec-trading-and-timing]{Section 2.3}. Let \(\mathcal N_L\)
denote the positive, absolutely continuous densities with
\(|(\log f)'|\le L\) almost everywhere, where \(0<L<1\), and set
\(b=1/L\). \hyperref[result-proposition-a-5]{Proposition A.5} extends the
equilibrium comparison to this class. Its upper cost restriction uses
the supremum of the posterior under full orders, which need not be
attained.

Laplace noise is the extreme member of the class. Among laws with median
zero, it has the thinnest tails at a fixed score bound. It gives the
most informative flow experiment at every pure order profile. The price
construction in Online Appendix A.6 preserves this comparison under its
stated conditions, and Online Appendix A.6 proves both claims.

Under full orders, the Laplace log odds relative to the prior odds equal
\((2/b)\max\{-1,\min\{x,1\}\}\). This is the Gaussian log odds with
variance \(b\), clipped at \(\pm2/b\). The linear part gives closed
forms, and the flat part keeps the market uncertain after extreme flows.
Gaussian noise has no finite score bound, and its posterior bounds do
not lie strictly inside \((0,1)\): an extreme flow all but reveals the
class, the residual advantage vanishes there, and the global argument
fails.

Logistic noise belongs to the class. At a common scale \(b\), logistic
noise equals Laplace noise plus independent noise. Under the same price
construction, the Laplace price experiment therefore Blackwell-dominates
the logistic experiment at the same orders. The logistic posterior
approaches its bounds only as flow tends to infinity.

In the strong benchmark economy, entry is 0.301509 under logistic noise,
compared with 0.522757 under Laplace noise. The logistic flow threshold
is 5.424598398, or 1.495369 noise standard deviations from the center.
The same posterior bounds can thus support different participation
rates, and the probability of favorable information near the upper bound
matters as well. At the same score bound and with full orders held
fixed, entry is 0.376606 under hyperbolic-secant noise and 0.374995 under
Student \(t_3\) noise. These two values are fixed-profile numerical
diagnostics: Online Appendix C.9 computes them without an equilibrium
search under these laws. Both lie between the logistic and the Laplace
values."""

SHAREHOLDERS = r"""Target shareholders gain because entry raises the value of their claim.
The gain is real, not a transfer. A shareholder who holds through the
sale receives \(V_T\), not the interim price. In the benchmark both
values lie above the reserve, so \(t_H>t_0\) and \(t_L>t_0\), and entry
raises expected proceeds in either class. At \(r_1\), price access
raises expected proceeds by 0.257809 per share. Under competitive
pricing the expected interim price rises by the same amount. The
informed investor's expected gross profit at one trading unit per share
of float is 0.140731. This profit is a transfer from liquidity traders:
the current shareholders who sell and the outside investors who buy.
Relative to an economy without the informed investor, initial
shareholders gain in total at every trade scale below 1.831923 trading
units per share of float, even if they bear the whole transfer. Online
Appendix C.9 computes both quantities. Holders who do not trade keep the
full proceeds gain. Holders who must sell bear part of the transfer and
can lose individually. The gain requires the recruiting region of
\hyperref[result-proposition-2]{Proposition 2}, in which high-cost
preparation does not pay at the prior. If high-cost preparation already
pays at the prior but not at the lowest feasible belief, an informative
price deters some preparation and lowers expected proceeds;
\hyperref[result-proposition-a-9]{Proposition A.9} states both cases."""

PROP1C = r"""\protect\phantomsection\label{result-proposition-1c}{\textbf{Proposition
1(c) (the weakest restriction; analytical).}} \emph{For classes
\(G_H,G_L\) with finite means, the spread weakly increases under every
first-order stochastic strengthening of every continuous \(F\) if and
only if \(D(u)\ge0\) for every \(u>p\) and \(D(p^-)\le0\). When neither
class has an atom at \(p\), this condition is exactly first-order
dominance above the reserve together with equal admissibility,
\(G_H(p^-)=G_L(p^-)\).}

\emph{Proof of part (c).} Fix the incumbent's value \(R\)."""

EXTENSION = r"""condition holds exactly when \(D(p^-)=0\), which with the ranking above
the reserve is equal admissibility.

Every result in the paper that assumes the restrictions of
\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} also holds
when they are weakened to the ranking above the reserve and equal
admissibility. Its proof uses only \(D(u)\ge0\) for \(u>p\) and
\(D(p^-)=0\), which give \(g_H\ge g_L\) and \(\Delta_T\ge0\) in
\eqref{eq:paper-6}, the comparison in part (b), and the split identity of
\hyperref[sec-acquisition-profits-and-target-proceeds]{Section 3.1}."""

A7_FORMULA = r"""\bar A_H(1)&=(1-\pi)K,\qquad \bar A_L(1)=\pi K,\\
K&=\Delta_T\int e(x)\frac{f(x-1)f(x+1)}{\pi f(x-1)+(1-\pi)f(x+1)}\,dx,
\end{aligned}
\tag{A.7}\label{eq:paper-a-7}
\]

so at \(\pi=1/2\) the two coincide, \(\bar A_H(1)=\bar A_L(1)=K/2\). The
pointwise ratio \(f(x-s)/f(x-1)\ge e^{-(1-s)/b}\) gives
\(\bar A_j(s)\ge e^{-(1-s)/b}\bar A_j(1)\). Since \((1-s/b)e^{-(1-s)/b}\) is
decreasing on \([0,1]\), the inequality
\(k<(1-1/b)\min\{\bar A_H(1),\bar A_L(1)\}\)"""

PROP_A5 = r"""A.5 (bounded-score noise; analytical).}} \emph{Replace Laplace noise by
any \(f\in\mathcal N_L\).
Keep the quality-class assumptions of
\hyperref[result-proposition-2]{Proposition 2}, with preparation costs
\(C\in\{0,c_H\}\).
Replace the upper posterior in \eqref{eq:paper-a2} by \(\bar\mu_f(\pi)\), so that}

\[
B_{F_0}(\pi)<c_H<B_{F_1}(\bar\mu_f(\pi)).
\]

\emph{Retain \eqref{eq:paper-a3} with \(b=1/L\), namely}

\[
\Delta_T(F_0)<k<(1-L)\rho\kappa(\pi)\Delta_T(F_1).
\]

\emph{Then the weak economy has unique zero orders and entry \(\rho\).
The strong economy has unique full orders \((1,-1)\) and an informative price.
Let}

\[
\begin{aligned}
\tau&=\frac{c_H-g_L(F_1)}{g_H(F_1)-g_L(F_1)},
&\mathcal X_f&=\{x:\mu_f(x;\pi)\ge\tau\},\\
\alpha_H&=\int_{\mathcal X_f}f(x-1)\,dx,
&\alpha_L&=\int_{\mathcal X_f}f(x+1)\,dx.
\end{aligned}
\]

\emph{Total entry satisfies}

\[
\mathsf E_f=\rho+(1-\rho)[\pi\alpha_H+(1-\pi)\alpha_L]>\rho.
\]

\emph{High-class ownership rises exactly when
\([\rho+(1-\rho)\alpha_H]W_H(F_1)>\rho W_H(F_0)\).
The condition holds automatically in the point-mass case with \(W_H=1\).
Part (iii) of \hyperref[result-proposition-2]{Proposition 2} also holds at
a continuous first-order stochastic strengthening \(F_2\) of \(F_1\) with
\(B_{F_2}(M(\pi))<c_H\): orders remain \((1,-1)\), and entry equals \(\rho\).
For fixed \(f,L,\pi,\rho,p,G_H,G_L\) with
\(\mathbb E_H[\max\{\theta,p\}]>\mathbb E_L[\max\{\theta,p\}]\),
these comparisons and the ownership increase hold on a nonempty open set
of uniform strengths and costs \((r_0,r_1,r_2,c_H,k)\), with the zero
preparation cost fixed.}"""

INFORMATIVE = r"""The entry formula and the stated ownership condition follow. The
likelihood ratio is not constant: both conditional densities integrate
to one, so a constant ratio would equal one, and \(f\) would be
two-periodic. No positive integrable density is two-periodic. The
nonconstant ratio therefore exceeds one on a set of positive measure,
so \(\bar\mu_f(\pi)>\pi\) and the strong price experiment is
informative. It strictly Blackwell-dominates the weak constant
experiment."""

ATOMLESS_CONDITIONS = r"""For atomless cost component distributions with
probabilities \(\rho\) and \(1-\rho\), supported within
\([0,2\varepsilon_C]\) and
\([c_H-\varepsilon_C,c_H+\varepsilon_C]\), the sufficient support
restrictions are

\[
\begin{gathered}
2\varepsilon_C<B_{F_1}(m(\pi)),\\
B_{F_0}(\pi)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{F_1}(M(\pi)),
\end{gathered}
\tag{A.24}\label{eq:paper-a-24}
\]

together with \eqref{eq:paper-a3}."""

PROP_A6 = r"""A.6 (atomless preparation costs; analytical).}} \emph{Retain the class
assumptions of \hyperref[result-proposition-2]{Proposition 2} and
condition \eqref{eq:paper-a3}, and replace the cost atoms by atomless
distributions satisfying \eqref{eq:paper-a-24}. Under either Laplace or
logistic noise, the unique trading outcomes and the entry reversal in
parts (i) and (ii) of Proposition 2 hold. High-class ownership rises
exactly when \(e_HW_H(F_1)>\rho W_H(F_0)\), where \(e_H\) is entry
conditional on class \(H\) at \(F_1\). This condition holds
automatically when \(W_H=1\) in both economies.}

Let \(H_C\) be the mixed cost CDF; the entry rule is
\(e(\mu)=H_C(B_F(\mu))\), continuous and nondecreasing. The first line
of \eqref{eq:paper-a-24} makes every realization of the component at
zero prepare at every feasible belief in both economies, since gross
profit at the lowest feasible belief \(m(\pi)\) already exceeds the
whole support and gross profit falls with incumbent strength. So
\(e\ge\rho\), and the residual bounds in \eqref{eq:paper-11} are
unchanged. The price increment \eqref{eq:paper-a-3} stays strictly
positive because \(H_C\) is nondecreasing, so the inversion and the
global trading bounds apply. At the weak prior, \(e(\pi)=\rho\) by both
lines of \eqref{eq:paper-a-24}. In the strong economy, beliefs close
enough to \(M(\pi)\) satisfy \(B_{F_1}(\mu)>c_H+\varepsilon_C\), an event
of positive probability under either noise law, and there \(e=1\).
Entry therefore exceeds \(\rho\). Given its class and preparation, the
challenger's value is independent of the price, so high-class ownership
is \(\pi\rho W_H(F_0)\) at \(F_0\) and \(\pi e_HW_H(F_1)\) at \(F_1\),
which gives the stated equivalence. Class-\(H\) flow reaches the event
above with positive probability, so \(e_H>\rho\), and \(W_H=1\) in both
economies gives the increase. The proof needs an atomless distribution,
not a density. Online Appendix A.6 has the details. \(\square\)"""

ACCESS = r"""Without a challenger, ownership value is \(\mathcal V_0(R)=R\mathbf1\{R\ge p\}\).
With a prepared challenger of value \(\theta\) it is
\(\mathcal V_\theta(R)=\max\{R\mathbf1\{R\ge p\},\theta\mathbf1\{\theta\ge p\}\}\).
Splitting at \(R=p\) and \(R=\theta\), for every \(\theta\),

\[
\mathcal V_\theta(R)-\mathcal V_0(R)
=(\theta-\max\{p,R\})_++p\mathbf1\{R<p,\ \theta\ge p\}.
\tag{A.39}\label{eq:paper-a-39}
\]

\Needspace{8\baselineskip}

\protect\phantomsection\label{result-proposition-a-9}{\textbf{Proposition
A.9 (access to prices; analytical).}} \emph{Hold the strong incumbent
\(F_1\) and all other primitives fixed under the conditions of
\hyperref[result-proposition-2]{Proposition 2}; in particular,
high-cost preparation does not pay at the prior,
\(B_{F_1}(\pi)<c_H\). Compare the feedback equilibrium with the
equilibrium in which the challenger cannot observe the target price,
reoptimizing trading and pricing in both. Access to prices strictly
increases expected target proceeds and acquisition surplus net of
preparation costs. The comparison also holds under Propositions A.5
and A.6. The condition \(B_{F_1}(\pi)<c_H\) matters: with Laplace noise,
cost atoms, and the strong-economy inequality of \eqref{eq:paper-a3}, if
instead \(B_{F_1}(m(\pi))<c_H\le B_{F_1}(\pi)\), access strictly lowers
expected target proceeds.}

Couple the two economies on the same realization of
\((j,\theta,R,C,Z)\). In the price-hidden game the challenger's
posterior stays at the prior, and \(B_{F_1}(\pi)\le B_{F_0}(\pi)<c_H\)
by \hyperref[result-proposition-1]{Proposition 1}(a) and
\eqref{eq:paper-a2}, so entry is \(\rho\). The residuals are then
\(\rho\Delta_T(1-\mu_X)\) and \(\rho\Delta_T\mu_X\), and the bound
\eqref{eq:paper-a-6} still applies, so orders are full in both games.
The order-flow experiment and the realized trading cost therefore
coincide, and any resource interpretation of that cost cancels. Price
access changes only whether a high-cost challenger prepares.

Conditional on the price information and preparation cost that induce an
additional preparation decision, \(R\) retains its independent law
\(F_1\) and the value retains its class law, so by
\eqref{eq:paper-a-39} the decision contributes expected allocation value
net of cost

\[
B_{F_1}(\mu_X)-C+pF_1(p)[1-G_L(p^-)].
\tag{A.40}\label{eq:paper-a-40}
\]

Under the restrictions of
\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} the last
factor is one; under equal admissibility it is the same in both
classes. For the uniform incumbent, \(pF_1(p)=p^2/r_1\) when
\(p\le r_1\). Optimal preparation requires \(B_{F_1}(\mu_X)\ge C\), so
each additional preparation decision contributes at least
\(pF_1(p)[1-G_L(p^-)]\ge0\) in conditional expectation, given price
information and preparation cost. A realized low-value preparation may
cost more than the allocation value it creates; the inequality is
conditional, not realized. Zero-cost preparation is unchanged in the
matched comparison, and its paid cost is zero in both economies.
Averaging over the event of additional preparation, for cost atoms,

\[
\begin{aligned}
\Delta\mathcal W
&=(1-\rho)\,\mathbb E\left[
\left\{B_{F_1}(\mu_X)-c_H+pF_1(p)[1-G_L(p^-)]\right\}
\mathbf1\{\mu_X\ge\tau\}\right]>0,\\
\Delta\mathcal R_T
&=(1-\rho)\left[\pi\alpha_H(t_H-t_0)+(1-\pi)\alpha_L(t_L-t_0)\right]>0,
\end{aligned}
\tag{A.41}\label{eq:paper-a-41}
\]

where the second line averages \(t_j-t_0\) over each class's
additional-entry probability. Both inequalities are strict. The strict
upper cost bound \(c_H<B_{F_1}(M(\pi))\) gives positive probability to
\(\mu_X>\tau\), because the posterior equals \(M(\pi)\) on the flow tail
\(x\ge1\). On that event \(B_{F_1}(\mu_X)-c_H>0\), since
\(g_H(F_1)>g_L(F_1)\). Also \(t_H-t_0=\Delta_T+(t_L-t_0)\ge\Delta_T>0\),
\(t_L\ge t_0\), and \(\alpha_H>0\). These facts prove both strict
inequalities, including when \(F_1(p)=0\). Transfers among bidders,
shareholders, market makers, and noise traders cancel and are not
allocation surplus. Under \hyperref[result-proposition-a-6]{Proposition
A.6} the same argument integrates the high-cost component over
\(\{c\le B_{F_1}(\mu_X)\}\); hidden-price entry is again \(\rho\) by
\eqref{eq:paper-a-24}. Under
\hyperref[result-proposition-a-5]{Proposition A.5}, use the integrals
over the entry set in that proposition; the event \(\mu_f>\tau\) has
positive probability by the definition of \(\bar\mu_f(\pi)\). The
external dividend of \hyperref[sec-access-to-prices]{Section 6.1} shifts
the price by a constant and leaves \(V_T-P\), trading, and entry
unchanged.

For the last claim, let \(B_{F_1}(m(\pi))<c_H\le B_{F_1}(\pi)\). With
hidden prices the posterior is \(\pi\), so both cost realizations
prepare and entry is one at every price. The residuals are then at least
\(\kappa(\pi)\Delta_T\ge\rho\kappa(\pi)\Delta_T\), so the strong-economy
inequality of \eqref{eq:paper-a3} again gives full orders in both games.
With access, the posterior equals \(m(\pi)\) on the flow tail
\(x\le-1\), which has positive probability in each class. There the
high-cost realization stays out, because \(B_{F_1}(m(\pi))<c_H\), and
entry is \(\rho\). Entry is at most one at every flow. Expected proceeds
are \(t_0\) plus the class-weighted entry gains, so access changes them
by
\(-\pi\,\mathbb E_H[1-e](t_H-t_0)-(1-\pi)\mathbb E_L[1-e](t_L-t_0)
\le-\pi(1-\rho)\Pr_H(X\le-1)(t_H-t_0)<0\). Online Appendix A.9 computes
the coupling and the atomless-cost integral in the benchmark.
\(\square\)"""

RESERVE_EVENTS_STUB = r"""\subsubsection{Exact reserve events}\label{exact-reserve-events}

Two reserve equalities need the tie rule. At the domain endpoint
\(p_L=h\), the high-value challenger earns no rent, and gross profit at
the lowest feasible belief equals the zero preparation cost. In the
strong economy with the low class excluded, the expensive-entry event
\(Mg_H=c_H\) occurs at \(p_H=\sqrt{2r(h-c_H/M)-r^2}\), which at
\(r=r_1\) lies in \((\ell,r_1)\). Online Appendix A.14 derives both
events, the continuation at each, and its outcome measures.

"""

LEVEL_SETS = r"""the whole posterior is the same at \(x_1\) and \(x_2\). If two classes
have equal proceeds, compare each with a class whose proceeds differ;
equality then forces the same likelihood ratio on their supports too.
Thus the posterior vector \((\mu_j(x))_j\) is constant on each level set
of \(\bar t_X\), and each level set is an interval because \(\bar t_X\)
is nondecreasing. Each flow density and each posterior component are
continuous, so \(\bar t_X\) is continuous. Under Laplace noise every
order lies in \([-1,1]\), so for \(x\ge1\) each flow density is
\(e^{-x/b}\) times a constant that depends on the class, and for
\(x\le-1\) it is \(e^{x/b}\) times such a constant. All posterior
components are therefore constant outside \([-1,1]\), and
\(\bar t_X(\mathbb R)=\bar t_X([-1,1])\). For \(t\) in this range let
\(x(t)=\inf\{x\in[-1,1]:\bar t_X(x)\ge t\}\). The map \(t\mapsto x(t)\)
is nondecreasing, hence Borel, and continuity gives
\(\bar t_X(x(t))=t\), so \(x(t)\) lies in the level set of \(t\). For
each class the Borel map \(t\mapsto\mu_j(x(t))\) therefore recovers the
posterior component: \(\mu_j(X)=\mu_j(x(\bar t_X(X)))\). The price
reveals \(\bar t_X\), so the tower property gives
\(\Pr(j\mid P)=\mu_j(X)\) almost surely. The argument uses the Laplace
law and \(b>1\); it does not establish the many-class result for every
bounded-score density. If all"""


def edits() -> list:
    E = []
    # ---------------------------------------------------------------- front matter
    E.append(B("m01", r"\begin{abstract}", r"\end{abstract}", ABSTRACT,
               "P-S1 abstract rewrite (short sentences, class information named)"))
    E.append(B("m02", "The informed investor is an outside specialist with no net position in",
               "states the result\nfor the class.\n\n\n\n",
               r"""The informed investor is an outside specialist with no net position in
the target. Its information is the challenger's quality class. Target
shareholders gain when the price recruits entry, because a holder
through the sale receives sale proceeds, not the interim price.

""", "P-S11.2-3 investor paragraph trimmed; P-M5 blank lines; Laplace sentence moves to m04"))
    # P-S11.4: the setting paragraph moves before the mechanism paragraph (done as a pair).
    E.append(B("m03a", "The setting is a listed target with a public sale opportunity.",
                "and no offer is announced before the challenger decides.\n\n", "",
                "P-S11.4 setting paragraph cut from after the investor paragraph"))
    E.append(R("m03b", "The mechanism runs through two claims on the same acquisition surplus.",
               r"""The setting is a listed target with a public sale opportunity. One buyer is already prepared, and another has not committed to the diligence that an executable proposal requires; \hyperref[sec-the-decision-interval]{Section 2.1} describes the decision interval in which that buyer decides while the target's stock trades. Incumbent strength is the public distribution of the prepared bidder's value; a stronger incumbent shifts it upward, and no offer is announced before the challenger decides.

The mechanism runs through two claims on the same acquisition surplus.""", 1,
               "P-S11.4 setting paragraph placed before the mechanism paragraph"))
    E.append(R("m04a", "only a\nlow-cost challenger prepares.", "only a\nzero-cost challenger prepares.", 1,
               "P-S4 zero-cost wording"))
    E.append(B("m04b", "The reversal holds at some incumbent strengths and costs for every prior",
               "including a buyer signal more accurate than the investor's.", ROBUSTNESS,
               "M8, C11, P-S5, F14: class gap and maintained restriction; F4 entry range; F9 bounded-score sentence"))
    E.append(R("m05", "Rival strength moves the information sensitivity of the traded claim and the entrant's return in opposite directions, so competition can raise participation. The paper belongs",
               "The paper belongs", 1, "P-S11.1 repeated first sentence removed"))
    E.append(R("m06", "and the entry cost reveals the value", "and paying the entry cost reveals the value", 1,
               "P-S6 paying the cost reveals the value"))
    E.append(R("m07a", r"(\citeproc{ref-PernoudGleyze2026}{Pernoud and Gleyze 2026}), post-auction feedback",
               r"(\citeproc{ref-PernoudGleyze2026}{Pernoud and Gleyze 2026}). It also studies post-auction feedback",
               1, "P-S14 long sentence split"))
    E.append(R("m07b", r"(\citeproc{ref-LiuBernhardt2022}{Liu and Bernhardt 2022}), and bidder-pool choice",
               r"(\citeproc{ref-LiuBernhardt2022}{Liu and Bernhardt 2022}) and bidder-pool choice",
               1, "P-S14 long sentence split"))
    E.append(R("m08", "and takes the investor's information as given; endogenous research would add",
               "and takes the investor's information as given. Endogenous research would add", 1,
               "P-S13 sentence split (scope kept as a fact)"))
    E.append(B("m09", "Noise then lets an acquirer conceal share purchases before a bid",
               "trading residual; a stake enters only as an extension.", STAKE,
               "P-S14 split; C18/D8 Edmans (2009) cited; C33 pointer to Online Appendix A.12"))
    # ---------------------------------------------------------------- Section 2
    E.append(R("m10", "\\hyperref[sec-complementary-private-information]{Section 5.3} removes\nboth extremes.",
               "\\hyperref[sec-complementary-private-information]{Section 5.3} removes\nboth extremes. "
               "The identity of the natural further buyer is common\nknowledge within the interval. "
               "What the market does not know is how\nwell that buyer fits the target.", 1,
               "F7a identity of the further buyer"))
    E.append(R("m11", "The\nincumbent is a bidder, rather than the target's management, and knows\nits value before bidding.",
               "The\nincumbent is a bidder and knows its value before bidding.", 1, "P-M9"))
    E.append(B("m12", "Two restrictions rank the classes. The high",
               "value, and the stock price is the pre-entry signal.", RESTRICTIONS,
               "F2/D5 maintained restriction: supports above the reserve; equal admissibility to A.1; P-M10"))
    E.append(B("m13", r"\(c_H>0\). The other type's cost is zero: a low-cost",
               "information about the class or the value.", COST,
               "C16, F24, P-S4, P-S13 cost wording; M2 joint independence of (j, theta)"))
    E.append(B("m14", "Before trading, the seller publicly commits to a cash second-price",
               "Preparation indifference matters at a posterior plateau considered\nin Section 4.", AUCTION,
               "D8/P-S7 Vickrey and Krishna cited; F7b no-entry proceeds; tie rule at zero gross profit"))
    E.append(B("m15", r"Here \(V_T\) is the terminal payoff of a target share and \(Z\) is",
               "about tail weight and bounded inference, not about a fit of one law\nto noise demand.", NOISE,
               "P-S3/D6 merge of the Laplace argument; F15 median zero; D8 Kotz et al. cited; C42"))
    E.append(R("m16", r"The trading stage follows the single-auction model of Kyle (\citeproc{ref-Kyle1985}{1985}), with binary information, bounded orders, a linear trading cost, Laplace noise, and a terminal payoff that depends on the price through preparation.",
               r"The trading stage follows the single-auction model of Kyle (\citeproc{ref-Kyle1985}{1985}). It has binary information, bounded orders, a linear trading cost, and Laplace noise. Its terminal payoff depends on the price through preparation.",
               1, "C44 sentence split"))
    E.append(R("m17a", "customers, technology, and demand, not from either bidder or the\ntarget, and trades lawfully on it. Its order",
               "customers, technology, and demand, not from information that either\nbidder or the target supplies. Its order",
               1, "F23 legal claim removed"))
    E.append(R("m17b", "apart from the sale. With independent exponential amounts of mean\n\\(b\\), their net demand has exactly the Laplace density in\n\\eqref{eq:paper-2}. Competitive",
               "apart from the sale. With independent exponential amounts, their net\ndemand is the first Laplace construction above. Competitive",
               1, "P-S3, C12 second statement of the exponential construction shortened"))
    E.append(R("m17c", "bids concerns in the main whether a bid arrives", "bids mostly concerns whether a bid arrives", 1, "P-M7"))
    E.append(B("m18", "incumbent knows its own value. The sequence is: the seller announces the",
               "submit truthful bids; ownership and financial payoffs are realized.", SEQUENCE,
               "P-S8 51-word sentence split"))
    # ---------------------------------------------------------------- Section 3
    E.append(B("m19", r"strengthening of \(F\). (a) For every pair of classes, it weakly",
               r"in (b) is strict when \(\int_p^\infty[F(u)-\tilde F(u)]D(u)\,du>0\).}", PROP1,
               "F2/D5 part (c) moves to Appendix A.1"))
    E.append(R("m20", "often, so that term shrinks. It can outweigh the moved slices when\nthe low class is more often inadmissible. Equal admissibility removes\nit. \\hyperref[paper-appendix]{Appendix A} gives the proof.",
               "often, so that term shrinks. It can outweigh the moved slices when\nthe low class is more often inadmissible. Under the restrictions of\n"
               "\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} every value\nmeets the reserve, and the term is zero. "
               "\\hyperref[pa-results]{Appendix A.1} gives\nthe proof and, in "
               "\\hyperref[result-proposition-1c]{Proposition 1(c)}, the\nweakest restriction under which the spread rises for every strengthening.",
               1, "F2/D5 pointer to Proposition 1(c)"))
    E.append(R("m21", "Adding the two lines of \\eqref{eq:paper-6} under equal admissibility\ngives",
               "Adding the two lines of \\eqref{eq:paper-6} under the restrictions of\n"
               "\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} gives", 1,
               "F2/D5 maintained restriction"))
    E.append(R("m22", "A low-cost challenger pays nothing to prepare, and its expected gross",
               "A zero-cost challenger pays nothing to prepare, and its expected gross", 1, "P-S4"))
    E.append(R("m23", "Price sufficiency holds in every candidate equilibrium. The entry\nfloor needs no condition.",
               "Price sufficiency holds in every candidate equilibrium in which the\nclasses differ in target proceeds, "
               "\\(\\Delta_T>0\\). The entry floor\nneeds no condition.", 1, "F13, C42 Delta_T > 0 stated"))
    E.append(R("m24", "unchanged. Both gains are strictly positive when both class supports\nlie above the reserve, as in the benchmark.",
               "unchanged. Both gains are strictly positive when no class value lies\nat or below the reserve, as in the benchmark.",
               1, "strictness of the entry gains stated exactly (a value atom at the reserve)"))
    # ---------------------------------------------------------------- Section 4
    E.append(R("m25", "from an uninformative price with low-cost preparation only to an",
               "from an uninformative price with zero-cost preparation only to an", 1, "P-S4"))
    E.append(R("m26", "\\emph{Let the classes\nsatisfy the restrictions of\n\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2}, let \\(F_1\\)",
               "\\emph{Let the classes\nsatisfy the restrictions of\n\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2}, so that the\n"
               "high class dominates and both class supports lie above the reserve, let\n\\(F_1\\)", 1,
               "F2/D5 maintained restriction stated in Proposition 2"))
    E.append(B("m27", "A low-cost challenger pays nothing and prepares after every price.",
               "\\(B_F(m(\\pi))\\) in every economy in the comparison gives the same\norders, prices, and entry.", FLOOR,
               "P-S4; F7c floor is an assumption with content; F13 reason for the slack low cost"))
    E.append(R("m28", "\\(\\pi\\) that involves no unit of money. A prior away from one half\nnarrows the window, since \\(\\kappa(\\pi)<m\\) there.",
               WORST_CASE, 1, "F3/D5 worst case and the region between the strengths (no new number)"))
    E.append(R("m29", "stays at the prior and only the low-cost challenger prepares. In the",
               "stays at the prior and only the zero-cost challenger prepares. In the", 1, "P-S4"))
    E.append(R("m30", "probability that the challenger pays its preparation cost. When both\nclasses lie above the reserve, as in the benchmark, every prepared\nchallenger is an admissible bidder, and the auction has two admissible\nbidders whenever the incumbent's value also meets the reserve.",
               "probability that the challenger pays its preparation cost. Under the\nrestrictions of\n"
               "\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} every\nprepared challenger is an admissible bidder. "
               "The auction then has two\nadmissible bidders whenever the incumbent's value also meets the\nreserve.",
               1, "P-S14 split; F2/D5 maintained restriction"))
    E.append(R("m31", "belief and cost realization, the decline in gross acquisition profit can",
               "belief and cost realization, a decline in gross acquisition profit can", 1, "P-M12"))
    E.append(R("m32", "The buyer uses its prior and prepares only at low\ncost.",
               "The challenger uses its prior and prepares only at\nzero cost.", 1, "P-S4"))
    E.append(R("m33", "equilibria with full purchases and partial sales that coexist with no\ntrade.",
               "equilibria with full purchases and partial sales that coexist with no\ntrade. "
               "\\hyperref[result-proposition-2]{Proposition 2} compares\n\\(r_0=1.2\\) with \\(r_1=3\\). "
               "The correspondence below shows what the\nsearch finds between them; it does not identify the first informative\nequilibrium.",
               1, "F3/D5 Section 4.3 sentence"))
    E.append(R("m34", "high- and low-type support magnitudes, with size increasing in",
               "support magnitudes after good and bad news, with size increasing in", 1, "C16 Figure 2 note"))
    E.append(R("m35", "are numerical continuations from the search in Online Appendix C.2, which also examined further pure and finite-support mixed profiles; the full correspondence at intermediate strengths is open.",
               "are numerical continuations from the search in Online Appendix C.2. That search also examined further pure and finite-support mixed profiles. The full correspondence at intermediate strengths is open.",
               1, "C44 sentence split"))
    # ---------------------------------------------------------------- Section 5
    E.append(B("m36", "The reversal holds for a class of noise laws.",
               "noise and 0.374995 under Student \\(t_3\\) noise (Online Appendix C.9).", SECTION_5_1,
               "P-S3/D6 merge; C20 class N_L; F4 diagnostics labeled; F20 paragraphs"))
    E.append(R("m37", "The other component lies above gross profit at the weak prior and below gross profit at the\nhighest strong belief, so its preparation occurs only after sufficiently favorable prices in\nthe strong economy.",
               "The other component lies above gross profit at the weak prior.\nIt lies below gross profit at the highest strong belief.\n"
               "Its preparation therefore occurs only after sufficiently favorable prices in the strong\neconomy.",
               1, "P-S14 split"))
    E.append(B("m38", "The reversal needs no point masses, no large class gap, and no\nspecial prior.",
               "differs above the reserve. Take any prior, noise scale, and low-cost\nprobability.",
               "The reversal holds without point masses, at any prior, and for any\nclass gap above the reserve, however small. "
               "Take any class pair under\nthe restrictions of\n"
               "\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} that\n"
               "differs above the reserve. Take any prior, noise scale, and zero-cost\nprobability.",
               "P-S13 stated as a fact; P-S4"))
    E.append(R("m39", "Appendix C.4 records the numerical examples.",
               "Appendix C.4 records the numerical examples. With more than two\nclasses the price still reveals the whole "
               "posterior over classes, and\nthe comparison extends to two groups of classes (Online Appendix A.13).",
               1, "D6/P-L1 pointer for the moved subsection"))
    E.append(B("m40", "Dispersed values within each class give a nondegenerate example. In the",
               "reserve \\(p=0.5\\) both classes lie above the reserve.",
               "Dispersed values within each class give a nondegenerate example. Let\n"
               "values be uniform with half-width \\(\\varepsilon_V=0.05\\) around \\(\\ell\\)\n"
               "and \\(h\\), let the prior be one half, and let the investor observe only\n"
               "the class. \\hyperref[sec-design]{Section 6.3} uses the same classes. At\n"
               "the reserve \\(p=0.5\\) both classes lie above the reserve.",
               "P-S10, C13 the example is introduced once, here"))
    E.append(R("m41", "B). Equal admissibility matters. At a reserve that excludes the low\nclass, a stronger incumbent can narrow the spread, and\n\\hyperref[sec-design]{Section 6.3} reports deterrence at such a reserve.",
               "B). The restriction to supports above the reserve matters. At a reserve\nthat excludes the low class, "
               "equal admissibility fails, a stronger\nincumbent can narrow the spread, and "
               "\\hyperref[sec-design]{Section 6.3}\nreports deterrence at such a reserve.",
               1, "F2/D5 maintained restriction"))
    E.append(R("m42a", "signals: the investor observes \\(T\\) with accuracy \\(a\\), and the buyer\nobserves \\(Y\\) with accuracy \\(d\\), where \\(a,d\\in(1/2,1)\\). The buyer\nobserves its signal and the price before preparing;",
               "signals: the investor observes \\(T\\) with accuracy \\(a\\), and the\nchallenger observes \\(Y\\) with accuracy "
               "\\(d\\), where \\(a,d\\in(1/2,1)\\).\nThe challenger observes its signal and the price before preparing;",
               1, "P-S4 challenger"))
    E.append(R("m42b", "Private information makes entry state-dependent even conditional on the",
               "Private information makes entry class-dependent even conditional on the", 1, "C5 class wording"))
    E.append(R("m42c", "Entry therefore stays at or above \\(\\rho\\) in each state, the",
               "Entry therefore stays at or above \\(\\rho\\) in each class, the", 1, "C5 class wording"))
    E.append(R("m42d", "The buyer\ncombines that posterior with its own signal.",
               "The challenger\ncombines that posterior with its own signal.", 1, "P-S4 challenger"))
    E.append(R("m42e", "state-dependent pricing, and trading bounds.", "class-dependent pricing, and trading bounds.", 1,
               "C5 class wording"))
    E.append(R("m43", "\\(\\rho\\) in the strong economy. These conditions allow arbitrary mixed\nsignal-contingent orders and every unilateral deviation to an order in \\([-1,1]\\). These conditions allow the buyer's signal to be more accurate than the investor's.",
               "\\(\\rho\\) in the strong economy. The conditions allow arbitrary mixed\nsignal-contingent orders, every unilateral "
               "deviation to an order in\n\\([-1,1]\\), and a buyer signal more accurate than the investor's. The\n"
               "displayed sufficient conditions use the point-mass benchmark and prior\n\\(\\pi=1/2\\).",
               1, "C43 merged sentence; M4 benchmark scope in Section 5.3"))
    # ---------------------------------------------------------------- Section 6
    E.append(R("m44", " The comparison holds the sale rule and the incumbent distribution fixed.", "", 1,
               "P-S9 repeated sentence removed"))
    E.append(B("m45", "Target shareholders gain from the mechanism through entry, not",
               "preparation and lowers expected proceeds.", SHAREHOLDERS,
               "F5/D5 real gain, not a transfer; P-S9 split; C33 pointer to C.9; F10 condition"))
    E.append(R("m46", "its level. The dividend is a diagnostic on the financial claim: no bidder pays it, the seller cannot choose it, and acquisition surplus excludes it. The online matched-price panel reports it beside",
               "its level. The dividend is a diagnostic on the financial claim. No bidder pays it, the seller cannot choose it, and acquisition surplus excludes it. The matched-price table in the Online Appendix reports it beside",
               1, "C44 split (all three facts kept); P-M13"))
    E.append(R("m47", "Without a challenger, the seller receives \\(\\eta R\\). For an incumbent\ndistribution supported on \\([0,R_{\\max}]\\), with \\(\\ell<R_{\\max}<h\\) and\n\\(0\\le\\eta<1\\), the transfer, challenger profit, and target-payoff\nspread are",
               "Without a challenger, the seller receives \\(\\eta R\\). For point-mass\nchallenger values \\(\\ell\\) and \\(h\\), "
               "an incumbent distribution supported\non \\([0,\\bar r]\\) with \\(\\ell<\\bar r<h\\), and \\(0\\le\\eta<1\\), "
               "the\ntransfer, challenger profit, and target-payoff spread are",
               1, "C30 one symbol for the support endpoint; M4 point-mass scope"))
    E.append(R("m48", "G_{\\theta,\\eta}&=(1-\\eta)\\mathbb E[(\\theta-R)_+],\\\\",
               "g_{\\theta,\\eta}&=(1-\\eta)\\mathbb E[(\\theta-R)_+],\\\\", 1,
               "C1, M11, D3 bargaining profit g, as in the Figure 4 labels"))
    E.append(R("m49", "The trading and preparation game under bargaining is not solved here.",
               "The trading and preparation game under bargaining is open.", 1, "P-S13 status word"))
    E.append(R("m50", "embedded in target shares. A reserve that excludes the low-value\nchallenger can widen the difference in target proceeds across challenger\ntypes.",
               "embedded in target shares. A reserve that excludes the low-value class\ncan widen the difference in target proceeds across challenger classes.",
               1, "C16, P-S4, F-report class wording"))
    E.append(B("m51", "To avoid making exclusion depend on an acquisition-value atom, let",
               "preparation reveals the exact value. Increasing the reserve from 0.5 to",
               "Use the value classes of\n\\hyperref[sec-acquisition-values]{Section 5.2}: uniform values with\n"
               "half-width \\(\\varepsilon_V=0.05\\) around \\(\\ell\\) and \\(h\\), prior one\n"
               "half, and an investor who observes only the class. Because the supports\n"
               "have no atom, exclusion does not depend on an acquisition-value atom.\n"
               "Increasing the reserve from 0.5 to",
               "P-S10, C13 back-reference to Section 5.2"))
    E.append(R("m52", "Table~\\ref{tab:4} reports the two reserves. The higher reserve excludes the low-value class and changes both acquisition incentives and the target-payoff spread. It raises expected proceeds in both economies.",
               "Table~\\ref{tab:4} reports the two reserves. The higher reserve excludes the low-value class. "
               "It leaves the restrictions of \\hyperref[sec-values-preparation-and-the-sale]{Section 2.2}, so "
               "\\hyperref[result-proposition-1]{Proposition 1}(b) no longer applies, and a stronger incumbent can "
               "narrow the spread. The higher reserve changes both acquisition incentives and the target-payoff "
               "spread, and it raises expected proceeds in both economies.",
               1, "F2/D5 Section 6.3 sentence"))
    E.append(R("m53", "the domain of Appendix A.7. Wherever the target-payoff spread is positive, fixed orders\ntherefore fix what the price reveals: distinct order-flow posteriors give distinct prices,\nand only flows with one common posterior, such as a posterior plateau, share a price.",
               "the domain of Appendix A.7. Wherever the target-payoff spread is positive, fixed orders\n"
               "therefore fix what the price reveals. Distinct order-flow posteriors give distinct prices.\n"
               "Only flows with one common posterior, such as a posterior plateau, share a price.",
               1, "P-S14 split"))
    E.append(R("m54", "retained, including the continuations that differ through their orders at one reserve.\nAt fixed orders the price experiment is already tied to those orders wherever the\ntarget-payoff spread is positive. The reserve comparisons show why this choice matters.",
               "retained, including the continuations that differ through their orders at one reserve.\n"
               "The reserve comparisons show why this choice matters.",
               1, "P-M8 repeated sentence removed from the conclusion"))
    # ---------------------------------------------------------------- bibliography
    E.append(R("m55a", "\\emph{The American Economic Review} 86 (1): 180--94.",
               "\\emph{American Economic Review} 86 (1): 180--94.", 1, "P-M1/D8 journal name"))
    E.append(R("m55b", "Entry.''} \\emph{The American Economic Review} 84 (3): 585--99.",
               "Entry.''} \\emph{American Economic Review} 84 (3): 585--99.", 1, "P-M1/D8 journal name"))
    E.append(R("m55c", "Boston, MA: Birkh\\\"auser.", "Birkh\\\"auser.", 1, "P-M2/D8 publisher place dropped, as for Krishna"))
    E.append(R("m55d", "via Market Feedback.''}\n\\url{https://warwick",
               "via Market Feedback.''} Working paper.\n\\url{https://warwick", 1, "P-M3/D8 working paper"))
    E.append(R("m55e", "Information in Auctions.''}\n\\url{https://agathepernoud",
               "Information in Auctions.''} Working paper.\n\\url{https://agathepernoud", 1, "P-M3/D8 working paper"))
    E.append(R("m55f", "\\bibitem[\\citeproctext]{ref-Ye2007}\nYe, Lixin. 2007. {``Indicative Bidding and a Theory of Two-Stage\nAuctions.''} \\emph{Games and Economic Behavior} 58 (1): 181--207.\n\\url{https://doi.org/10.1016/j.geb.2005.12.004}.\n\n",
               "", 1, "C18, F18, D8 Ye (2007) removed: only the abstract was verified"))
    # ---------------------------------------------------------------- Appendix A.1
    E.append(R("m56", "\\emph{Floor.} The low-cost challenger pays nothing", "\\emph{Floor.} The zero-cost challenger pays nothing", 1, "P-S4"))
    E.append(R("m57", "then \\eqref{eq:paper-9} with the buyer's own posterior.",
               "then \\eqref{eq:paper-9} with the challenger's own posterior.", 1, "P-S4"))
    E.append(R("m58", "term is zero and the integrand is nonnegative, so the spread rises,\nstrictly exactly when the integral is positive.",
               "term is zero and the integrand is nonnegative, so the spread rises,\nstrictly exactly when the integral is positive. "
               "Equal admissibility,\nwhich also makes the second term zero, gives the same conclusion.",
               1, "F2/D5 part (b) under equal admissibility"))
    E.append(R("m59a", "\\emph{Part (c).} Fix the incumbent's value \\(R\\).", PROP1C, 1,
               "F2/D5 Proposition 1(c) stated in Appendix A.1"))
    E.append(R("m59b", "uniform on \\([x_1-\\eta,x_1+\\eta]\\) and let \\(\\tilde F\\) be the same law\nshifted to \\(x_2\\). Then \\(\\tilde F\\le F\\), and as \\(\\eta\\to0\\),",
               "uniform on \\([x_1-\\delta,x_1+\\delta]\\) and let \\(\\tilde F\\) be the same law\nshifted to \\(x_2\\). Then \\(\\tilde F\\le F\\), and as \\(\\delta\\to0\\),",
               1, "C28 half-width delta (eta is the bargaining weight)"))
    E.append(R("m59c", "\\([0,\\bar r]\\) into both laws; this scales the difference by a positive\nfactor and keeps its sign.",
               "\\([0,\\bar r]\\) into both laws; both mixtures are continuous, and the\nmixing scales the difference by a positive factor and keeps its sign.",
               1, "F-report minor 11 continuity after mixing"))
    E.append(R("m59d", "condition holds exactly when \\(D(p^-)=0\\), which with the ranking above\nthe reserve is the pair of restrictions of\n\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2}.",
               EXTENSION, 1, "F2/D5 equal admissibility kept in A.1; results extend to it"))
    # ---------------------------------------------------------------- Appendix A.2
    E.append(R("m60", "F_H(s)&=\\int f(x-s)A_H(x)\\,dx,\\qquad\nF_L(s)=\\int f(x+s)A_L(x)\\,dx,\\\\\nU_j(s)&=sF_j(s)-ks.",
               "\\bar A_H(s)&=\\int f(x-s)A_H(x)\\,dx,\\qquad\n\\bar A_L(s)=\\int f(x+s)A_L(x)\\,dx,\\\\\nU_j(s)&=s\\bar A_j(s)-ks.",
               1, "C6 expected residual named bar A_j (F is the incumbent cdf)"))
    E.append(B("m61", "J_H&=F_H(1)=(1-\\pi)K,\\qquad J_L=F_L(1)=\\pi K,\\\\",
               "the inequality \\(k<(1-1/b)\\min\\{J_H,J_L\\}\\)", A7_FORMULA,
               "C6 constants J_H, J_L removed"))
    E.append(S("m62", "\\subsubsection{The global order bound}", "\\subsubsection{\\texorpdfstring{Proof of",
               [("F_j", "\\bar A_j", 8)], "C6 bar A_j in (A.5)-(A.6)"))
    E.append(R("m63", "posterior obeys the same bound. The low-cost challenger prepares at",
               "posterior obeys the same bound. The zero-cost challenger prepares at", 1, "P-S4"))
    E.append(R("m64", "that the buyer sees order flow.", "that the challenger sees order flow.", 1, "P-S4"))
    E.append(R("m65", "\\(s>0\\) earns \\(s[F_j(s)-k]\\le s[\\Delta_T(F_0)-k]<0\\)",
               "\\(s>0\\) earns \\(s[\\bar A_j(s)-k]\\le s[\\Delta_T(F_0)-k]<0\\)", 1, "C6"))
    E.append(R("m66", "so only the low-cost\nchallenger prepares", "so only the zero-cost\nchallenger prepares", 1, "P-S4"))
    E.append(R("m67", "jump and at the two plateau atoms. The buyer recovers the posterior from",
               "jump and at the two plateau atoms. The challenger recovers the posterior from", 1, "P-S4"))
    E.append(R("m68", "The low-cost floor and the derivative", "The zero-cost floor and the derivative", 1, "P-S4"))
    E.append(R("m69", "so the buyer's posterior\n\\(\\Pr(H\\mid S)\\)", "so the challenger's posterior\n\\(\\Pr(H\\mid S)\\)", 1, "P-S4"))
    E.append(R("m70", "cost independence makes this the buyer's\ncomplete posterior",
               "cost independence makes this the challenger's\ncomplete posterior", 1, "P-S4"))
    # ---------------------------------------------------------------- Appendix A.3
    E.append(S("m71", "\\subsubsection{Low-type concavity}", "\\subsubsection{Interval signs}",
               [("F_L", "\\bar A_L", 6)], "C6 bar A_L in (A.16)"))
    E.append(S("m72", "\\subsubsection{High-type cover over the whole", "\\subsubsection{\\texorpdfstring{No-trade",
               [("F_H", "\\bar A_H", 2)], "C6 bar A_H in (A.18)"))
    # ---------------------------------------------------------------- Appendix A.4
    E.append(R("m73", "Let \\(\\mathcal C_L\\) denote the positive, absolutely continuous densities\n\\(f\\) with",
               "Let \\(\\mathcal N_L\\) denote the positive, absolutely continuous densities\n\\(f\\) with", 1,
               "C20 class N_L (L is also the low class)"))
    E.append(B("m74", "A.5 (bounded-score noise; analytical).}} \\emph{Replace Laplace noise by",
               "The other preparation cost stays zero.}", PROP_A5,
               "C17, F21 general incumbent distributions; C8 X_f; F-report minor 12"))
    E.append(R("m75a", "They give \\(|F_j'|\\le LF_j\\) and", "They give \\(|\\bar A_j'|\\le L\\bar A_j\\) and", 1, "C6"))
    E.append(R("m75b", "U_j'(s)\\ge(1-sL)F_j(s)-k\n\\ge(1-L)\\rho\\kappa(\\pi)\\Delta_T(r_1)-k>0.",
               "U_j'(s)\\ge(1-sL)\\bar A_j(s)-k\n\\ge(1-L)\\rho\\kappa(\\pi)\\Delta_T(F_1)-k>0.", 1, "C6, C17"))
    E.append(R("m75c", "At \\(r_0\\), every correctly signed nonzero order earns at most\n\\(s[\\Delta_T(r_0)-k]<0\\).",
               "At \\(F_0\\), every correctly signed nonzero order earns at most\n\\(s[\\Delta_T(F_0)-k]<0\\).", 1, "C17"))
    E.append(R("m75d", "At \\(r_1\\), the positive derivative makes unit magnitude strictly optimal for each class.",
               "At \\(F_1\\), the positive derivative makes unit magnitude strictly optimal for each class.", 1, "C17"))
    E.append(B("m75e", "The entry formula and the stated ownership condition follow.\nThe likelihood ratio is not constant.",
               "Hence \\(\\bar\\mu_f(\\pi)>\\pi\\).", INFORMATIVE, "C38 repeated sentence removed, support before conclusion"))
    E.append(R("m75f", "For part (iii) of \\hyperref[result-proposition-2]{Proposition 2},\n\\(\\Delta_T(r_2)\\ge\\Delta_T(r_1)\\) by",
               "For part (iii) of \\hyperref[result-proposition-2]{Proposition 2},\n\\(\\Delta_T(F_2)\\ge\\Delta_T(F_1)\\) by", 1, "C17"))
    E.append(R("m75g", "On \\(\\mathcal E_f\\), Bayes' rule gives", "On \\(\\mathcal X_f\\), Bayes' rule gives", 1, "C8"))
    E.append(R("m75h", "This fixes \\(\\mathcal E_f,\\alpha_H,\\alpha_L\\) before", "This fixes \\(\\mathcal X_f,\\alpha_H,\\alpha_L\\) before", 1, "C8"))
    E.append(R("m76", "has log derivative \\(-\\tanh(z/2b)/b\\), so it belongs to \\(\\mathcal C_{1/b}\\).",
               "has log derivative \\(-\\tanh(z/2b)/b\\), so it belongs to \\(\\mathcal N_{1/b}\\).", 1, "C20"))
    E.append(R("m77", "Laplace and logistic noise are compared at a common scale parameter \\(b\\), not at a common variance.",
               "Laplace and logistic noise are compared at a common scale parameter \\(b\\).", 1, "P-S13"))
    E.append(B("m78", "For atomless cost component distributions with", "together with \\eqref{eq:paper-a3}.",
               ATOMLESS_CONDITIONS, "M1 (blocking), C3b support conditions at the actual prior"))
    E.append(B("m79", "A.6 (atomless preparation costs; analytical).}} \\emph{Replace the cost",
               "an atomless distribution, not a density. Online Appendix A.6 has the\ndetails. \\(\\square\\)", PROP_A6,
               "M1 (blocking): statement and proof at a general prior, with the exact ownership condition"))
    E.append(R("m80", "\\(R\\ge p\\) and, under equal admissibility, zero for \\(R<p\\), so",
               "\\(R\\ge p\\) and, under the restrictions of\n\\hyperref[sec-values-preparation-and-the-sale]{Section 2.2} "
               "or more\ngenerally under equal admissibility, zero for \\(R<p\\), so", 1, "F2/D5"))
    E.append(R("m81", "the low cost fixed at zero. This is a mathematical nonemptiness\nconstruction, not a statement about effect size for every pair of\nclasses.",
               "the low cost fixed at zero.", 1, "C37, P-S13 disclaimer removed"))
    # ---------------------------------------------------------------- Appendix A.5
    E.append(R("m82", "The investor observes a signal \\(T\\in\\{+,-\\}\\) and the buyer a signal\n\\(Y\\in\\{+,-\\}\\), conditionally independent given quality, with",
               "This subsection uses the point-mass benchmark with prior \\(\\pi=1/2\\).\nThe investor observes a signal "
               "\\(T\\in\\{+,-\\}\\) and the challenger a\nsignal \\(Y\\in\\{+,-\\}\\), conditionally independent given quality, with",
               1, "M4, C3d benchmark scope; P-S4"))
    E.append(R("m83", "quality, their bounds, and the buyer's combined posteriors are",
               "quality, their bounds, and the challenger's combined posteriors are", 1, "P-S4"))
    E.append(R("m84", "State-conditioned entry rates and the coefficient on public beliefs are",
               "Class-conditioned entry rates and the price loading on public beliefs are", 1, "C5, C7"))
    E.append(R("m85", "D&=e_Hw_H-e_Lw_L.", "\\Delta_P&=e_Hw_H-e_Lw_L.", 1, "C7 price loading Delta_P"))
    E.append(R("m86", "Entry is state-dependent even conditional on the price, so the\nbenchmark's common preparation rate is not reused here; \\(D\\) carries\nthe two rates separately.",
               "Entry is class-dependent even conditional on the price, so the\nbenchmark's common preparation rate is not reused "
               "here; the price\nloading \\(\\Delta_P\\) carries the two rates separately.", 1, "C5, C7"))
    E.append(R("m87", "\\emph{In the\ncomplementary-signal economy, choose \\(0<p<\\ell<r_0<r_1<h\\) and suppose}",
               "\\emph{In the\npoint-mass complementary-signal economy with \\(\\pi=1/2\\), choose\n\\(0<p<\\ell<r_0<r_1<h\\) and suppose}",
               1, "M4, F25 benchmark scope of Proposition A.7"))
    E.append(R("m88", "\\Theta\\perp X\\mid T,\\qquad Y\\perp X\\mid\\Theta .", "J\\perp X\\mid T,\\qquad Y\\perp X\\mid J .", 1,
               "C5 class variable J"))
    E.append(R("m89", "\\emph{Step 2: state-conditioned entry and price inversion.} Because the\nlaw of \\(Y\\) given quality does not depend on \\(X\\), true-state entry",
               "\\emph{Step 2: class-conditioned entry and price inversion.} Because the\nlaw of \\(Y\\) given quality does not depend "
               "on \\(X\\), class-conditional entry", 1, "C5"))
    E.append(S("m90", "\\subsubsection{Proof}\\label{proof}", "\\subsection{A.6 Bargaining", [
        ("D=e_L\\Delta_T+(e_H-e_L)w_H\\ \\in\\ ", "\\Delta_P=e_L\\Delta_T+(e_H-e_L)w_H\\ \\in\\ ", 1),
        ("\\qquad D\\ge\\rho\\Delta_T>0.", "\\qquad \\Delta_P\\ge\\rho\\Delta_T>0.", 1),
        ("P=t_0+e_L(P)w_L+\\mu_XD(P),", "P=t_0+e_L(P)w_L+\\mu_X\\Delta_P(P),", 1),
        ("{D(P)}.", "{\\Delta_P(P)}.", 1),
        ("so the positive coefficient\n\\(D(P)\\)", "so the positive loading\n\\(\\Delta_P(P)\\)", 1),
        ("\\((\\mu_2-\\mu_1)D(\\mu_1)", "\\((\\mu_2-\\mu_1)\\Delta_P(\\mu_1)", 1),
        ("+aD(P(x))\\)", "+a\\Delta_P(P(x))\\)", 1),
        ("A_+=(2a-1)(1-\\lambda_X)D,\\qquad A_-=(2a-1)\\lambda_XD,", "A_+=(2a-1)(1-\\lambda_X)\\Delta_P,\\qquad A_-=(2a-1)\\lambda_X\\Delta_P,", 1),
        ("=:\\overline A.", "=:A^+.", 1),
        ("\\(s(\\overline A(r_0)-k)<0\\)", "\\(s(A^+(r_0)-k)<0\\)", 1),
        ("the buyer's\nfavorable posterior", "the challenger's\nfavorable posterior", 1),
        ("\\(\\Pr(Y=+\\mid\\Theta)>0\\) in both states.", "\\(\\Pr(Y=+\\mid J)>0\\) in both classes.", 1),
    ], "C7 Delta_P; C24 A^+; C5 J; P-S4"))
    # ---------------------------------------------------------------- Appendix A.6
    E.append(R("m91", "The institution of \\hyperref[sec-the-payment-rule]{Section 6.2} has four\nelements:",
               "The displayed bargaining formulas use point-mass challenger values\n\\(\\ell\\) and \\(h\\). The institution of\n"
               "\\hyperref[sec-the-payment-rule]{Section 6.2} has four elements:", 1, "M4 point-mass scope"))
    E.append(R("m92", "\\([0,R_{\\max}]\\) with \\(0<\\ell<R_{\\max}<h\\).", "\\([0,\\bar r]\\) with \\(0<\\ell<\\bar r<h\\).", 1, "C30"))
    E.append(R("m93", "gives \\(G_{\\theta,\\eta}\\) in \\eqref{eq:paper-14}.", "gives \\(g_{\\theta,\\eta}\\) in \\eqref{eq:paper-14}.", 1,
               "C1, M11, D3"))
    E.append(R("m94", "boundary at one half. That boundary is a property of this institution's\npayment rule; the proposition does not solve a private-value first-price\nauction or a bargaining-and-trading equilibrium. Online Appendix A.8\ntreats the endpoints. \\(\\square\\)",
               "boundary at one half. That boundary is a property of this institution's\npayment rule. Online Appendix A.8 treats the endpoints. \\(\\square\\)",
               1, "C40 disclaimer kept in the Online Appendix only"))
    E.append(B("m95", "Without a challenger, ownership value is \\(\\mathcal V_0(R)=R\\mathbf1\\{R\\ge p\\}\\).",
               "Appendix A.9 states the coupling and the atomless-cost integral.\n\\(\\square\\)", ACCESS,
               "M3 general-class welfare proof; C3a prior weights; F5, F10/D5 recruiting condition stated; C5"))
    # ---------------------------------------------------------------- Appendix A.7
    E.append(R("m96", "\\subsection{A.7 Seller continuation}\\label{pa-design}\n\n",
               "\\subsection{A.7 Seller continuation}\\label{pa-design}\n\n"
               "This section uses the point-mass benchmark with prior \\(\\pi=1/2\\), so\nclass expectations carry equal weights. "
               "Its class extension uses the\nuniform value bands of \\hyperref[sec-acquisition-values]{Section 5.2}.\n\n",
               1, "M4, C5 benchmark scope of A.7"))
    E.append(R("m97", "the buyer's\nbeliefs at every realized price including price atoms",
               "the challenger's\nbeliefs at every realized price including price atoms", 1, "P-S4"))
    E.append(R("m98", "state-conditioned entry. Expected seller revenue", "class-conditioned entry. Expected seller revenue", 1, "C5"))
    E.append(R("m99", "&=t_0(p,r)+\\frac12\\sum_{\\theta\\in\\{H,L\\}}e_\\theta(p,r;\\sigma)\n[t_\\theta(p,r)-t_0(p,r)],\\\\",
               "&=t_0(p,r)+\\frac12\\sum_{j\\in\\{H,L\\}}e_j(p,r;\\sigma)\n[t_j(p,r)-t_0(p,r)],\\\\", 1, "C5 class index j"))
    E.append(R("m100", "Distinct raw order-flow posteriors give distinct prices, and the buyer\nrecovers",
               "Distinct raw order-flow posteriors give distinct prices, and the challenger\nrecovers", 1, "P-S4"))
    E.append(R("m101a", "+\\frac12\\sum_\\theta\\frac{de_\\theta}{dp}(t_\\theta-t_0).", "+\\frac12\\sum_j\\frac{de_j}{dp}(t_j-t_0).", 1, "C5"))
    E.append(R("m101b", "\\(\\mu_\\theta(z;p)\\) is the posterior reached in state \\(\\theta\\) at\nnoise realization \\(z\\), then",
               "\\(\\mu_j(z;p)\\) is the posterior reached in class \\(j\\) at\nnoise realization \\(z\\), then", 1, "C5"))
    E.append(R("m101c", "\\frac{de_\\theta}{dp}\n=\\int f(z)\\,h_C(B_{p,r}(\\mu_\\theta))\n\\left[-\\frac p r+(g_H-g_L)\\frac{d\\mu_\\theta(z;p)}{dp}\\right]dz.",
               "\\frac{de_j}{dp}\n=\\int f(z)\\,h_C(B_{p,r}(\\mu_j))\n\\left[-\\frac p r+(g_H-g_L)\\frac{d\\mu_j(z;p)}{dp}\\right]dz.", 1, "C5"))
    E.append(R("m102", "full object \\eqref{eq:paper-a-43} and with the endpoint reserve\n\\eqref{eq:paper-a-50} and the ceiling event \\eqref{eq:paper-a-51} included.",
               "full object \\eqref{eq:paper-a-43} and with the endpoint reserve\n\\(p_L\\) and the ceiling event \\(p_H\\) included.", 1,
               "D6 references follow the moved exact reserve events"))
    # ---------------------------------------------------------------- Appendix A.8
    E.append(R("m103", "In each vector the preparation cost is \\(0\\) with probability \\(\\rho\\) and\n\\(c_H\\) otherwise.",
               "In each vector the preparation cost is \\(0\\) with probability \\(\\rho\\) and\n\\(c_H\\) otherwise. "
               "The prior is \\(\\pi=1/2\\) in each vector.", 1, "C33 prior stated"))
    E.append(R("m104", "The atomless-value half-width is \\(\\varepsilon_V=\\) 0.05.", "The atomless-value half-width is \\(\\varepsilon_V=0.05\\).", 1, "C34"))
    return E


def moves() -> list:
    """Blocks cut from main.tex and appended to Part A of the Online Appendix (D6, P-L1, P-L2)."""
    classes = [
        R("v01", "\\subsubsection{More than two classes}\\label{more-than-two-classes}",
          "\\subsection{A.13. More than two classes}\\label{oa-a-classes}", 1, "heading in the Online Appendix"),
        R("v02", "as in \\hyperref[sec-equilibrium]{Section 2.4}; the investor observes",
          "as in Section 2.4 of the paper; the investor observes", 1, "cross-document reference"),
        R("v03", "T_X", "\\bar t_X", 6, "C29 posterior mean of class proceeds"),
        R("v04", "the whole posterior is the same at \\(x_1\\) and \\(x_2\\). The posterior is\ntherefore a measurable function of \\(\\bar t_X\\), hence of the price. If all",
          LEVEL_SETS, 1, "M6 level-set and measurability step written in full"),
        R("v05", "Steps 3 to 6 of the proof of\n\\hyperref[result-proposition-2]{Proposition 2}.",
          "Steps 3 to 6 of the proof of\nProposition 2 of the paper.", 1, "cross-document reference"),
        R("v06", "\\eqref{eq:paper-a2} and \\eqref{eq:paper-a3}.", "(A1) and (A2) of the paper.", 1, "cross-document reference"),
    ]
    reserve = [
        R("v11", "\\subsubsection{Exact reserve events}\\label{exact-reserve-events}\n\nOne participation equality",
          "\\subsection{A.14. Exact reserve events}\\label{oa-a-reserve-events}\n\n"
          "This section works in the point-mass benchmark of Appendix A.7 of the paper,\nwith \\(\\pi=1/2\\). One participation equality",
          1, "heading and scope in the Online Appendix"),
        R("v12", "gross profit is \\(B_p(m)=m(h-p)\\).",
          "gross profit is \\(B_{p,r}(m)=m(h-p)\\), which does not\ndepend on \\(r\\) in this region.", 1, "C31"),
        R("v13", "\n\\tag{A.45}\\label{eq:paper-a-50}", "", 1, "tag removed; the display is unnumbered here"),
        R("v14", "\n\\tag{A.46}\\label{eq:paper-a-51}", "", 1, "tag removed; the display is unnumbered here"),
        R("v15", "The inversion above and the global\nbound of \\hyperref[pa-proofs]{Appendix A.2} apply",
          "The inversion in Appendix A.7 of the paper and the global\nbound of its Appendix A.2 apply", 1,
          "cross-document reference"),
        R("v16", "the expensive type on it.", "the high-cost realization on it.", 1, "C16"),
    ]
    return [
        {"id": "mv1", "start": "\\subsubsection{More than two classes}\\label{more-than-two-classes}",
         "end": "\\subsection{A.5 Complementary private information}", "edits": classes,
         "why": "D6, P-L1, F6b: More than two classes to Online Appendix A.13"},
        {"id": "mv2", "start": "\\subsubsection{Exact reserve events}\\label{exact-reserve-events}",
         "end": "\\subsubsection{Outcome measures}", "edits": reserve, "stub": RESERVE_EVENTS_STUB,
         "why": "D6, P-L2: Exact reserve events to Online Appendix A.14"},
    ]


# After the move of (A.45) and (A.46), later tags move up by two (C19, P-M4 label names follow).
RETAG = [("A.47", "A.45"), ("A.48", "A.46"), ("A.49", "A.47"), ("A.50", "A.48"),
         ("A.51", "A.49"), ("A.52", "A.50")]
RELABEL = [("eq:paper-a-52", "eq:paper-a-45"), ("eq:paper-a-53", "eq:paper-a-46"),
           ("eq:paper-a-54", "eq:paper-a-47"), ("eq:paper-a-55", "eq:paper-a-48"),
           ("eq:paper-a-56", "eq:paper-a-49"), ("eq:paper-a-57", "eq:paper-a-50"),
           ("eq:paper-a2", "eq:paper-cond-1"), ("eq:paper-a3", "eq:paper-cond-2")]

# Strings that must not survive (allowed count 0), or that survive only at named places.
LEFTOVER = [
    ("\\Theta", 0), ("t_\\theta", 0), ("e_\\theta", 0), ("\\mu_\\theta", 0), ("\\sum_\\theta", 0),
    ("F_j", 0), ("F_H(", 0), ("F_L(", 0), ("F_L'", 0), ("F_H'", 0), ("J_H", 0), ("J_L", 0),
    ("\\overline A", 0), ("G_{\\theta,\\eta}", 0), ("R_{\\max}", 0), ("\\mathcal C_", 0),
    ("\\mathcal E_f", 0), ("ref-Ye2007", 0), ("c_L", 0), ("lawfully", 0), ("type's cost", 0),
    ("low-cost", 2), ("high- and low-type", 0), ("The American Economic Review", 0),
    ("eq:paper-a2}", 0), ("eq:paper-a3}", 0), ("\\varepsilon_V=\\)", 0),
]
