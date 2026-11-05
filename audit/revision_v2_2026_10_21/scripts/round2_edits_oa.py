"""Round-2 edits to online_appendix.tex. Imported by round2.py.

Item codes in the notes: M = R_math.md, C = R_consistency.md, P = R_prose_latex.md,
F = R_referee.md ranked fix list, D = the round's decisions in the task brief.
"""

from round2_edits_main import B, R, S

MOVE_ANCHOR = "\\section{B. Computer-assisted equilibrium certificates}\\label{oa-b}"

SCOPE = r"""\noindent\textbf{Scope under quality classes.}
The class is \(j\in\{H,L\}\), with prior \(\pi=\Pr(j=H)\).
The investor observes \(j\).
Preparation reveals the value \(\theta\sim G_j\).
Conditional on \(j\), the value is independent of flow and of the preparation decision.
Finite class means imply integrable auction payoffs.
\par
The probability and deviation arguments use the class expectations
\(t_j,g_j\), the spread \(\Delta_T\), and the stated properties of Laplace noise.
They therefore apply to the quality-class model.
A.1--A.4 and A.6 state them at a general prior, with the posterior bounds
\(m(\pi),M(\pi)\) and \(\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}\) of the paper.
The point-mass formulas are special cases.
A.5, A.7, A.9, A.10, and A.14 keep the point-mass benchmark with \(\pi=1/2\) in their displayed formulas, and each says so.
Two further points need care.

\begin{enumerate}
\item
In A.7 the conditional-independence arguments apply to quality classes.
So do the conditional price equation, the measurable inverse, and the convolution argument.
At another prior, Bayes' rule gives the investor-signal probabilities and the class probabilities conditional on the signal.
Those weights enter the posterior identity \eqref{eq:oa-oa-30}, the residuals \eqref{eq:oa-oa-37}--\eqref{eq:oa-oa-38}, and the outcome probabilities after \eqref{eq:oa-oa-41}.
The buyer's private-signal maps update the public class posterior by Bayes' rule.

\item
The reserve enters the auction calculation in A.2 through a boundary term.
With \(D(u)=G_L(u)-G_H(u)\), the general spread is
\[
\Delta_T(F)=pF(p)D(p^-)+\int_p^\infty[1-F(u)]D(u)\,du.
\]
Under the restrictions of Section 2.2 of the paper both class supports lie above the reserve, so \(D(p^-)=0\).
Equal admissibility also gives \(D(p^-)=0\).
The boundary term then vanishes.
Together with the rank condition above the reserve, it gives the spread comparison used in A.4--A.6.
If equal admissibility fails, the boundary term can offset the increase in the integral when the incumbent becomes stronger.
The price and deviation arguments use the resulting \(t_0,t_j,g_j,\Delta_T\).
A.7 uses \(w_j=t_j-t_0\) as well.
\end{enumerate}

The price construction in A.3 requires \(t_L-t_0\ge0\) and \(\Delta_T>0\).
Strict positivity of \(t_L-t_0\) is unnecessary.
The reserve adds no separate term to the residuals.
The common payoff level cancels."""

A1_DEFS = r"""I write \(t_0\) for expected target proceeds without challenger entry,
\(t_H,t_L\) for proceeds conditional on entry and class, and
\(g_H,g_L\) for conditional gross challenger profits. Set
\(\Delta_T=t_H-t_L\) and \(B_r(\mu)=g_L+\mu(g_H-g_L)\), and use the
posterior bounds of the paper,
\(m(\pi)=\pi/[\pi+(1-\pi)e^{2/b}]\),
\(M(\pi)=\pi/[\pi+(1-\pi)e^{-2/b}]\), and
\(\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}\). In the benchmark,
\(m=m(1/2)=(1+e^{2/b})^{-1}\) and \(M=M(1/2)=1-m\). For uniform
incumbents with \(r_0<r_1\), the hypotheses of Proposition 2 are

\[
\begin{aligned}
&B_{r_0}(\pi)<c_H<B_{r_1}(M(\pi)),\\
&\Delta_T(r_0)<k<(1-1/b)\rho\kappa(\pi)\Delta_T(r_1),
\end{aligned}
\tag{OA.1}\label{eq:oa-oa-1}
\]"""

A1_SPACE = r"""To define beliefs and deviations, let \(J\in\{L,H\}\) have
\(\Pr(J=H)=\pi\), and given \(J\) draw the acquisition value \(\theta\)
from \(G_J\); in the benchmark \(\theta=\ell\) or \(h\). Independently of
\((J,\theta)\) and of each other, draw incumbent value \(R\), preparation
cost \(C\), noise demand \(Z\), and an auxiliary random variable \(U\)
uniform on \([0,1]\). A mixed trader strategy is a probability kernel
\(\sigma_J\) on the Borel subsets of \([-1,1]\). It can be implemented
by a Borel quantile map \(q_J(U)\). Conditional randomization therefore
contains no information about the other primitives beyond the trader's
specified signal."""

A1_DENSITY = r"""Define

\[
\begin{aligned}
a_j(x)&=\int_{[-1,1]}f(x-q)\,\sigma_j(dq),\\
\nu(dx)&=[\pi a_H(x)+(1-\pi)a_L(x)]\,dx,\\
\mu_X(x)&=\frac{\pi a_H(x)}{\pi a_H(x)+(1-\pi)a_L(x)}.
\end{aligned}
\tag{OA.2}\label{eq:oa-oa-2}"""

A2_GENERAL = r"""For a general continuous incumbent distribution, let \(D=G_L-G_H\). At
a fixed incumbent value, the expected class difference in payments is

\[
\xi(R)=
\begin{cases}
pD(p^-),&R<p,\\
\int_p^RD(u)\,du,&R\ge p.
\end{cases}
\]

Class expectation and Tonelli's theorem give

\[
\Delta_T(F)=pF(p)D(p^-)+\int_p^\infty[1-F(u)]D(u)\,du,
\qquad
g_j(F)=\int_p^\infty[1-G_j(u)]F(u)\,du.
\tag{OA.6}\label{eq:oa-oa-6}
\]

Appendix A.1 of the paper proves the comparison, its strictness
conditions, and the necessity result. With point masses at \(\ell\) and
\(h\), the kernel is \(\min\{(R-\ell)_+,h-\ell\}\). It reduces to
\((R-\ell)_+\) when incumbent support lies below \(h\)."""

FULL_PROFILE = r"""A useful full-profile existence test is sharper than the uniform
uniqueness bound. At a fixed full-order candidate in the benchmark,

\[
\bar A_H(1)=\bar A_L(1)
=\Delta_T\int e(x)\frac{f(x-1)f(x+1)}{f(x-1)+f(x+1)}\,dx;
\tag{OA.22}\label{eq:oa-oa-22}
\]

(A.7) of the paper gives the general prior. The equality follows by
substituting Bayes' rule into both residuals. The pointwise
density-ratio bound implies \(\bar A_j(s)\ge e^{-(1-s)/b}\bar A_j(1)\).
Since \((1-s/b)e^{-(1-s)/b}\) is decreasing on \([0,1]\),
\(k<(1-1/b)\bar A_H(1)\) makes every correctly signed
marginal profit positive."""

PRICE_CONSTRUCTION = r"""Costs lie in \(\{0,c_H\}\), with probability \(\rho>0\) on zero cost and entry at equality.
Fix the incumbent strength \(r\). Then the schedules of equation (9) of the paper read
\[
e(\mu)=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\qquad
P(\mu)=t_0+e(\mu)[t_L-t_0+\Delta_T\mu].
\]
Entry is nondecreasing in \(\mu\), and for \(\mu_2>\mu_1\),
\[
P(\mu_2)-P(\mu_1)\ge\rho\Delta_T(\mu_2-\mu_1)>0.
\]
Thus \(P\) has a measurable inverse on its image.
For each noise law, apply \(P\) to its flow posterior."""

PROP_A6_OA = r"""For Proposition A.6, let \(H_C=\rho H_C^0+(1-\rho)H_C^1\), with atomless
component laws supported within
\([0,2\varepsilon_C]\) and
\([c_H-\varepsilon_C,c_H+\varepsilon_C]\). Retain (A2) and impose
\(2\varepsilon_C<B_{r_1}(m(\pi))\), and

\[
B_{r_0}(\pi)<c_H-\varepsilon_C<c_H+\varepsilon_C<B_{r_1}(M(\pi)).
\tag{OA.26}\label{eq:oa-oa-26}
\]

Use either the Laplace or logistic noise law. The entry rule is
\(e(\mu)=H_C(B_r(\mu))\). It is continuous and nondecreasing, and
\(e\ge\rho\) because the whole first support lies below gross profit at the
lowest feasible belief \(m(\pi)\) in both economies. Equation
\eqref{eq:oa-oa-9} remains strictly positive even if the component
densities are discontinuous or vanish on subintervals. In the weak
economy, \(e(\pi)=\rho\). In the strong economy, a posterior
sufficiently close to \(M(\pi)\) satisfies \(B_r(\mu)>c_H+\varepsilon_C\); an"""


def edits() -> list:
    E = []
    # ---------------------------------------------------------------- scope note
    E.append(B("o01", "\\noindent\\textbf{Scope under quality classes.}", "The common payoff level cancels.", SCOPE,
               "C10 scope items 1-3 deleted (the body now prints the general forms); C39; F2/D5"))
    # ---------------------------------------------------------------- A.1
    E.append(R("o02a", "The benchmark has a risk-neutral seller, an incumbent, a potential",
               "The model has a risk-neutral seller, an incumbent, a potential", 1, "C10 general prior"))
    E.append(R("o02b", "its value before bidding. The challenger has value \\(\\ell\\) or \\(h\\)\nwith equal probability, where \\(0<p<\\ell<r<h\\). Neither bidder trades\ntarget equity. An outside investor observes challenger quality and",
               "its value before bidding. The challenger belongs to class\n\\(j\\in\\{H,L\\}\\) with prior \\(\\pi=\\Pr(j=H)\\), "
               "and given its class its value\n\\(\\theta\\) has the law \\(G_j\\) with a finite mean. In the point-mass\n"
               "benchmark the values are \\(h\\) and \\(\\ell\\), \\(\\pi=1/2\\), and\n\\(0<p<\\ell<r<h\\). Neither bidder trades "
               "target equity. An outside investor\nobserves the challenger's class and", 1, "C10 class model with prior pi"))
    E.append(B("o03", "I write \\(t_0\\) for expected target proceeds without challenger entry,",
               "\\tag{OA.1}\\label{eq:oa-oa-1}\n\\]", A1_DEFS, "C10, C3 hypotheses of Proposition 2 at the actual prior"))
    E.append(B("o04", "To define beliefs and deviations, let \\(\\Theta\\in\\{L,H\\}\\) have equal",
               "primitives beyond the trader's specified signal.", A1_SPACE,
               "C5 class variable J; C10 prior pi (R_consistency 5's 'equal probabilities' applied differently)"))
    E.append(R("o05", "Borel functions. Because values and the order interval are bounded, all\nacquisition and trading payoffs are integrable.",
               "Borel functions. Because the class means are finite and the order\ninterval is bounded, all acquisition and trading payoffs are integrable.",
               1, "M5 integrability under finite class means"))
    E.append(B("o06", "For the benchmark, define", "\\tag{OA.2}\\label{eq:oa-oa-2}", A1_DENSITY,
               "C10 prior weights in (OA.2); C5 a_j, sigma_j"))
    E.append(R("o07", "integrates to unity. Tonelli's theorem gives \\(\\int a_\\theta=1\\).\nDominated convergence in \\(q\\) implies continuity of \\(a_\\theta(x)\\),",
               "integrates to unity. Tonelli's theorem gives \\(\\int a_j=1\\).\nDominated convergence in \\(q\\) implies continuity of \\(a_j(x)\\),",
               1, "C5"))
    E.append(R("o08", "\\mu_P=\\mathbb E[\\mathbf1\\{\\Theta=H\\}\\mid\\mathcal G]", "\\mu_P=\\mathbb E[\\mathbf1\\{J=H\\}\\mid\\mathcal G]", 1, "C5"))
    E.append(R("o09", "\\(e^{-2/b}a_L\\le a_H\\le e^{2/b}a_L\\), hence \\(m\\le\\mu_X\\le M\\). Equation",
               "\\(e^{-2/b}a_L\\le a_H\\le e^{2/b}a_L\\). The likelihood ratio adds to the\nprior log odds, hence "
               "\\(m(\\pi)\\le\\mu_X\\le M(\\pi)\\). Equation", 1, "C10 bounds at the actual prior"))
    E.append(R("o10", "bounded below by \\(\\rho\\) at every belief, because the zero-cost\nrealization prepares whenever gross profit is nonnegative, and gross\nprofit is positive at each feasible belief on this support. Conditional on \\(\\Theta\\) and \\(X\\), the",
               "bounded below by \\(\\rho\\) at every belief, because gross profit is\nnonnegative at every belief and the zero-cost "
               "realization prepares\nwhenever it is, by the tie rule at zero. Conditional on \\(J\\) and \\(X\\), the",
               1, "C10 floor without a support restriction; C5"))
    E.append(R("o11", "observation of \\(\\Theta\\) by \\(T\\) and add \\(Y\\). The randomization\n\\(U\\), noise \\(Z\\), incumbent \\(R\\), and cost \\(C\\) remain independent\nof \\((\\Theta,T,Y)\\); \\(T\\) and \\(Y\\) are independent conditional on\n\\(\\Theta\\).",
               "observation of \\(J\\) by \\(T\\) and add \\(Y\\). The randomization\n\\(U\\), noise \\(Z\\), incumbent \\(R\\), and cost "
               "\\(C\\) remain independent\nof \\((J,T,Y)\\); \\(T\\) and \\(Y\\) are independent conditional on\n\\(J\\).",
               1, "C5"))
    # ---------------------------------------------------------------- A.2
    E.append(R("o12", "Without the challenger, the seller receives \\(p\\) if \\(R\\ge p\\). A\nhigh-value challenger wins",
               "In the point-mass benchmark, without the challenger, the seller receives\n\\(p\\) if \\(R\\ge p\\). A high-value "
               "challenger wins", 1, "M5 benchmark scope of the uniform formulas"))
    E.append(B("o13", "For a general continuous incumbent CDF \\(F\\) on \\([0,\\bar r]\\), the",
               "ordering. This completes Proposition 1.", A2_GENERAL,
               "M5 general kernel with the reserve term and point-mass truncation"))
    # ---------------------------------------------------------------- A.3
    E.append(R("o14a", "The function \\(g(P)=[P-t_0-e(P)(t_L-t_0)]/[e(P)\\Delta_T]\\) is Borel on",
               "The function \\(\\iota(P)=[P-t_0-e(P)(t_L-t_0)]/[e(P)\\Delta_T]\\) is Borel on", 1, "C23 iota (g is profit)"))
    E.append(R("o14b", "It satisfies \\(\\mu_X(X)=g(P(X))\\) almost surely.", "It satisfies \\(\\mu_X(X)=\\iota(P(X))\\) almost surely.", 1, "C23"))
    E.append(R("o15", "For construction, put \\(w_L=t_L-t_0>0\\). For \\(\\mu_2>\\mu_1\\),",
               "For construction, put \\(w_L=t_L-t_0\\ge0\\). For \\(\\mu_2>\\mu_1\\),", 1, "C10 weak sign"))
    E.append(R("o16", "Conditional on fundamental quality, expected terminal value under a\nunilateral trading deviation is still \\(t_0+e(P(x))(t_\\theta-t_0)\\).\nSubtracting \\eqref{eq:oa-oa-7} gives \\(A_H=e\\Delta_T(1-\\mu_X)\\) and\n\\(A_L=e\\Delta_T\\mu_X\\). Both residuals are bounded in\n\\([\\rho m\\Delta_T,\\Delta_T]\\).",
               "Conditional on the class \\(j\\), expected terminal value under a\nunilateral trading deviation is still "
               "\\(t_0+e(P(x))(t_j-t_0)\\).\nSubtracting \\eqref{eq:oa-oa-7} gives \\(A_H=e\\Delta_T(1-\\mu_X)\\) and\n"
               "\\(A_L=e\\Delta_T\\mu_X\\). Both residuals are bounded below by\n\\(\\rho\\kappa(\\pi)\\Delta_T\\) and above by "
               "\\(\\Delta_T\\).", 1, "C5, C10"))
    E.append(S("o17", "nonnegative. For sign \\(\\epsilon\\in\\{-1,1\\}\\), define", "\\subsection{A.4. Complete proof of Proposition 2}", [
        ("F_\\epsilon", "\\bar A_\\epsilon", 5),
        ("For \\(U(s)=sF(s)-ks\\), absolute continuity and the product rule imply",
         "For \\(U(s)=s\\bar A(s)-ks\\), with \\(\\bar A=\\bar A_\\epsilon\\), absolute continuity and the\nproduct rule imply", 1),
        ("U'(s)=F(s)+sF'(s)-k\\ge(1-sL)F(s)-k.", "U'(s)=\\bar A(s)+s\\bar A'(s)-k\\ge(1-sL)\\bar A(s)-k.", 1),
    ], "C6 bar A in the convolution lemma"))
    # ---------------------------------------------------------------- A.4
    E.append(R("o18", "\\mathbb E[\\text{trading profit}\\mid\\Theta]\\le", "\\mathbb E[\\text{trading profit}\\mid J]\\le", 1, "C5"))
    E.append(R("o19", "Under zero orders, \\(X=Z\\) is independent of quality. Set \\(e=\\rho\\) and\n\\(P=t_0+\\rho[(t_H+t_L)/2-t_0]\\).",
               "Under zero orders, \\(X=Z\\) is independent of the class. Set \\(e=\\rho\\) and\n"
               "\\(P=t_0+\\rho[\\pi t_H+(1-\\pi)t_L-t_0]\\).", 1, "C10 weak price at the prior"))
    E.append(R("o20a", "\\(F_\\theta(s)\\ge\\rho m\\Delta_T(r_1)\\), and \\eqref{eq:oa-oa-13} with",
               "\\(\\bar A_j(s)\\ge\\rho\\kappa(\\pi)\\Delta_T(r_1)\\), and \\eqref{eq:oa-oa-13} with", 1, "C6, C10"))
    E.append(R("o20b", "U_\\theta'(s)\\ge(1-1/b)\\rho m\\Delta_T(r_1)-k>0.", "U_j'(s)\\ge(1-1/b)\\rho\\kappa(\\pi)\\Delta_T(r_1)-k>0.", 1,
               "C5, C10"))
    E.append(R("o21", "\\mu(x)=\n\\begin{cases}\nm,&x\\le-1,\\\\\n(1+e^{-2x/b})^{-1},&-1<x<1,\\\\\nM,&x\\ge1.\n\\end{cases}",
               "\\mu(x)=\n\\begin{cases}\nm(\\pi),&x\\le-1,\\\\\n\\left[1+\\frac{1-\\pi}{\\pi}e^{-2x/b}\\right]^{-1},&-1<x<1,\\\\\n"
               "M(\\pi),&x\\ge1.\n\\end{cases}", 1, "C10 full-order posterior at the actual prior"))
    E.append(R("o22", "requires \\(\\mu\\ge\\tau\\). The strict inequalities\n\\(B_{r_1}(1/2)<B_{r_0}(1/2)<c_H<B_{r_1}(M)\\) imply \\(\\tau\\in(1/2,M)\\).\nSolving \\eqref{eq:oa-oa-16} gives\n\\(x^*=b\\operatorname{logit}(\\tau)/2\\in(0,1)\\).",
               "requires \\(\\mu\\ge\\tau\\). The inequalities\n\\(B_{r_1}(\\pi)\\le B_{r_0}(\\pi)<c_H<B_{r_1}(M(\\pi))\\) imply\n"
               "\\(\\tau\\in(\\pi,M(\\pi))\\). Solving \\eqref{eq:oa-oa-16} gives\n"
               "\\(x^*=\\frac b2[\\operatorname{logit}\\tau-\\operatorname{logit}\\pi]\\in(0,1)\\).", 1, "C10"))
    E.append(R("o23", "positive. State-specific entry is\n\\(e_\\theta=\\rho+(1-\\rho)\\alpha_\\theta\\), total entry is \\((e_H+e_L)/2\\),\nand high-quality ownership is \\(e_H/2\\) because \\(h>r\\). Each comparison\nis strict.",
               "positive. Class-conditional entry is\n\\(e_j=\\rho+(1-\\rho)\\alpha_j\\), total entry is \\(\\pi e_H+(1-\\pi)e_L\\),\n"
               "and high-class ownership is \\(\\pi e_HW_H(r_1)\\), which equals \\(\\pi e_H\\)\nin the benchmark because "
               "\\(h>r\\). Entry rises strictly, and ownership\nrises under the condition in part (ii) of Proposition 2.",
               1, "C5, C10 entry and ownership at the actual prior"))
    E.append(R("o24", "\\textbf{Nonemptiness.} \\hyperref[oa-a-extensions]{Section A.6} gives a\ndirect primitive construction for every \\(h>\\ell\\). The specified\nbenchmark is also strictly inside the condition region.",
               "\\textbf{Nonemptiness.} \\hyperref[oa-a-extensions]{Section A.6} gives a\ndirect primitive construction in the "
               "point-mass benchmark for every\n\\(h>\\ell\\), and Appendix A.4 of the paper gives one for every ranked pair\n"
               "of classes. The specified benchmark is also strictly inside the\ncondition region.", 1, "C10 scope"))
    # ---------------------------------------------------------------- A.5
    E.append(R("o25", "fix one joint distribution of \\((S,\\Theta)\\) for\nboth strengths, and keep the preparation cost \\(C\\) independent of\n\\((S,\\Theta)\\) with its law",
               "fix one joint distribution of \\((S,J)\\) for\nboth strengths, and keep the preparation cost \\(C\\) independent of\n"
               "\\((S,J)\\) with its law", 1, "C5"))
    E.append(R("o26", "buyer's full information, and I do not claim that version. For",
               "buyer's full information. For", 1, "P-S13 negative clause removed"))
    E.append(R("o27", "For Proposition A.4, define the maintained domain",
               "Proposition A.4 is a point-mass statement, and the rest of this section\nkeeps the benchmark prior "
               "\\(\\pi=1/2\\); the paper's proof of Proposition\nA.4 states the general-prior conditions. For Proposition A.4, "
               "define the\nmaintained domain", 1, "C10 benchmark scope of A.5"))
    E.append(B("o28", "A useful full-profile existence test is sharper than the uniform",
               "\\(k<(1-1/b)J\\) makes every correctly signed\nmarginal profit positive.", FULL_PROFILE,
               "C6 bar A_j(1) replaces J; C5"))
    # ---------------------------------------------------------------- A.6
    E.append(R("o29", "\\mathcal C_L", "\\mathcal N_L", 3, "C20 class N_L"))
    E.append(R("o30a", "Set \\(b=1/L\\) and \\(\\ell_b(z)=e^{-|z|/b}/(2b)\\).",
               "Set \\(b=1/L\\) and write \\(f^{\\mathrm{Lap}}_b(z)=e^{-|z|/b}/(2b)\\) for the Laplace density.", 1,
               "C9 Laplace density named f^Lap_b (ell is the low value); F19"))
    E.append(R("o30b", "Equality at a positive \\(t\\) requires \\(f=\\ell_b\\).", "Equality at a positive \\(t\\) requires \\(f=f^{\\mathrm{Lap}}_b\\).", 1, "C9"))
    E.append(R("o31", "\\label{result-lemma-oa-laplace-extreme}{\\textbf{Lemma\n(Laplace extremality; analytical).}}",
               "\\label{result-lemma-oa-laplace-extreme}{\\textbf{Lemma\nOA.1 (Laplace extremality; analytical).}}", 1,
               "C14 the extremality lemma takes the first number"))
    E.append(R("o32a", "\\(Z_{\\mathrm{log}}\\overset d=Z_{\\mathrm{Lap}}+W\\), where\n\\(W\\overset d=\\sum_{n=2}^{\\infty}Y_n\\) and the \\(Y_n\\) are independent Laplace variables with scales \\(b/n\\).",
               "\\(Z_{\\mathrm{log}}\\overset d=Z_{\\mathrm{Lap}}+\\sum_{n=2}^{\\infty}Z_n\\), where\n\\(Z_{\\mathrm{Lap}}\\) and the "
               "\\(Z_n\\) are independent Laplace variables with scales \\(b\\) and \\(b/n\\).", 1, "C22 Z_n (W and Y are taken)"))
    E.append(R("o32b", "Take independent \\(Y_n\\), \\(n\\ge1\\), with these laws.", "Take independent \\(Z_n\\), \\(n\\ge1\\), with these laws.", 1, "C22"))
    E.append(R("o32c", "\\(Z_{\\mathrm{Lap}}=Y_1\\) is independent of \\(W=\\sum_{n\\ge2}Y_n\\).\nThe product identity gives \\(Z_{\\mathrm{log}}\\overset d=Z_{\\mathrm{Lap}}+W\\).\nThe kernel that adds \\(W\\) does not depend",
               "\\(Z_{\\mathrm{Lap}}=Z_1\\) is independent of the remainder \\(\\sum_{n\\ge2}Z_n\\).\nThe product identity gives "
               "\\(Z_{\\mathrm{log}}\\overset d=Z_1+\\sum_{n\\ge2}Z_n\\).\nThe kernel that adds the remainder does not depend",
               1, "C22"))
    E.append(B("o33", "Costs lie in \\(\\{0,c_H\\}\\), with probability \\(\\rho>0\\) on zero cost and entry at equality.",
               "For each noise law, apply \\(P_r\\) to its flow posterior.", PRICE_CONSTRUCTION,
               "C9 schedules named as in equation (9) of the paper"))
    E.append(R("o34a", "\\log\\frac{\\mu(x)}{1-\\mu(x)}\n=2\\log\\cosh\\left(\\frac{x+1}{2b}\\right)",
               "\\log\\frac{\\mu(x)}{1-\\mu(x)}\n=\\operatorname{logit}\\pi\n+2\\log\\cosh\\left(\\frac{x+1}{2b}\\right)", 1,
               "C3c logit pi as in (A.22)"))
    E.append(R("o34b", "The limits are \\(-2/b\\) and \\(2/b\\), giving the open posterior range\n\\((m,M)\\).",
               "The limits are \\(\\operatorname{logit}\\pi-2/b\\) and\n\\(\\operatorname{logit}\\pi+2/b\\), giving the open "
               "posterior range\n\\((m(\\pi),M(\\pi))\\).", 1, "C3c"))
    E.append(R("o34c", "and \\(w=\\sqrt{\\tau/(1-\\tau)}\\). The square root",
               "and \\(w=\\sqrt{\\tau(1-\\pi)/[(1-\\tau)\\pi]}\\). The square root", 1, "C3c"))
    E.append(R("o34d", "\\(\\mathsf E=\\rho+(1-\\rho)(\\alpha_H+\\alpha_L)/2\\) supply the complete",
               "\\(\\mathsf E=\\rho+(1-\\rho)[\\pi\\alpha_H+(1-\\pi)\\alpha_L]\\) supply the complete", 1, "C3c"))
    E.append(B("o35", "For Proposition A.6, let \\(H_C=\\rho H_L+(1-\\rho)H_H\\), with atomless",
               "sufficiently close to \\(M\\) satisfies \\(B_r(\\mu)>c_H+\\varepsilon_C\\); an", PROP_A6_OA,
               "M1 (blocking) conditions at the actual prior; C27 H_C^0, H_C^1"))
    E.append(R("o36a", "For primitive nonemptiness, fix \\(h>\\ell>p>0\\), \\(b>1\\), and",
               "For primitive nonemptiness in the point-mass benchmark with\n\\(\\pi=1/2\\), fix \\(h>\\ell>p>0\\), \\(b>1\\), and", 1,
               "C10 benchmark scope"))
    E.append(R("o36b", "both arguments. All inequalities have strict slack and persist by\ncontinuity. This is a mathematical nonemptiness construction, not a\nstatement about empirical effect size at every value ratio.",
               "both arguments. All inequalities have strict slack and persist by\ncontinuity.", 1, "C37 disclaimer removed"))
    E.append(R("o37a", "Two further stability results are recorded for completeness.",
               "One further stability result is recorded for completeness.", 1, "C14"))
    E.append(R("o37b", "\\label{result-lemma-oa-1}{\\textbf{Lemma OA.1\n(analytical).}}", "\\label{result-lemma-oa-1}{\\textbf{Lemma OA.2\n(analytical).}}", 1,
               "C14 renumbered; label kept"))
    E.append(R("o38a", "\\(\\Delta_T(r_0)<k\\), and \\(k+\\gamma_q<(1-1/b)\\rho m\\Delta_T(r_1)\\), the",
               "\\(\\Delta_T(r_0)<k\\), and \\(k+\\gamma_q<(1-1/b)\\rho\\kappa(\\pi)\\Delta_T(r_1)\\), the", 1,
               "C10 kappa(pi) in the quadratic-cost lemma"))
    E.append(R("o38b", "threshold, and information comparison are unchanged. This perturbation\nretains the position bound; it does not solve an unbounded-order game.",
               "threshold, and information comparison are unchanged. The position bound\nstays at one.", 1, "C41"))
    E.append(B("o39", "\\Needspace{8\\baselineskip}\n\n\\protect\\phantomsection\\label{result-lemma-oa-2}",
               "lemma is required to generate a reported numerical value in the present\nmanuscript.\n\n", "",
               "M10, C14, P-M15 Lemma OA.2 removed (Proposition 2 holds at every prior); C39"))
    # ---------------------------------------------------------------- A.7
    E.append(R("o40a", "signal, and \\(\\Theta\\) for fundamental quality.", "signal, and \\(J\\) for the class.", 1, "C5"))
    E.append(R("o40b", "Since \\(X\\) depends on quality only through \\(T\\), \\(\\Theta\\) and \\(X\\)\nare conditionally independent given \\(T\\). Also \\(Y\\) is independent of\n\\(X\\) conditional on \\(\\Theta\\).",
               "Since \\(X\\) depends on quality only through \\(T\\), \\(J\\) and \\(X\\)\nare conditionally independent given "
               "\\(T\\). Also \\(Y\\) is independent of\n\\(X\\) conditional on \\(J\\).", 1, "C5"))
    E.append(R("o40c", "with \\(X\\) or the trader's signal, true-state entry conditional on \\(P\\)\nis",
               "with \\(X\\) or the trader's signal, class-conditional entry given \\(P\\)\nis", 1, "C5"))
    E.append(R("o40d", "Let \\(D=e_Hw_H-e_Lw_L\\). As \\(w_H-w_L=\\Delta_T\\) and \\(w_L>0\\),",
               "Let \\(\\Delta_P=e_Hw_H-e_Lw_L\\) be the price loading on the public\nposterior. As \\(w_H-w_L=\\Delta_T\\) "
               "and \\(w_L>0\\),", 1, "C7 Delta_P"))
    E.append(R("o40e", "D=e_L\\Delta_T+(e_H-e_L)w_H\n\\in[\\rho\\Delta_T,", "\\Delta_P=e_L\\Delta_T+(e_H-e_L)w_H\n\\in[\\rho\\Delta_T,", 1, "C7"))
    E.append(R("o40f", "Conditional pricing is \\(P=t_0+e_L(P)w_L+\\mu_XD(P)\\).",
               "Conditional pricing is \\(P=t_0+e_L(P)w_L+\\mu_X\\Delta_P(P)\\).", 1, "C7"))
    E.append(R("o40g", "The positive coefficient \\(D(P)\\) therefore makes", "The positive loading \\(\\Delta_P(P)\\) therefore makes", 1, "C7"))
    E.append(R("o40h", "={}&(\\mu_2-\\mu_1)D(\\mu_1)", "={}&(\\mu_2-\\mu_1)\\Delta_P(\\mu_1)", 1, "C7"))
    E.append(R("o40i", "\\(t_0+e_L(P(x))w_L+aD(P(x))\\) for \\(T=+\\)", "\\(t_0+e_L(P(x))w_L+a\\Delta_P(P(x))\\) for \\(T=+\\)", 1, "C7"))
    E.append(R("o40j", "A_+=(2a-1)(1-\\lambda_X)D,\\qquad\nA_-=(2a-1)\\lambda_XD.",
               "A_+=(2a-1)(1-\\lambda_X)\\Delta_P,\\qquad\nA_-=(2a-1)\\lambda_X\\Delta_P.", 1, "C7"))
    E.append(R("o40k", "\\le(2a-1)\\{\\Delta_T+(1-\\rho)(2d-1)w_H\\}=: \\overline A.",
               "\\le(2a-1)\\{\\Delta_T+(1-\\rho)(2d-1)w_H\\}=: A^+.", 1, "C24 A^+"))
    E.append(R("o40l", "order of magnitude \\(s>0\\) earn at most \\(s(\\overline A-k)<0\\).",
               "order of magnitude \\(s>0\\) earn at most \\(s(A^+-k)<0\\).", 1, "C24"))
    E.append(R("o40m", "Let \\(Q_{\\theta,y}=\\Pr(X\\ge x_y^*\\mid\\Theta=\\theta)\\), with the",
               "Let \\(Q_{j,y}=\\Pr(X\\ge x_y^*\\mid J=j)\\), with the", 1, "C5"))
    E.append(R("o40n", "integrating the joint law of \\((\\Theta,T,Y,Z,C)\\) must reproduce these",
               "integrating the joint law of \\((J,T,Y,Z,C)\\) must reproduce these", 1, "C5"))
    E.append(R("o40o", "No low-cost condition joins them.", "No condition on the low cost joins them.", 1, "P-S4"))
    # ---------------------------------------------------------------- A.8
    E.append(R("o41", "G_{H,\\eta}&=(1-\\eta)(h-r/2),\\\\\nG_{L,\\eta}&=(1-\\eta)\\frac{\\ell^2}{2r}.",
               "g_{H,\\eta}&=(1-\\eta)(h-r/2),\\\\\ng_{L,\\eta}&=(1-\\eta)\\frac{\\ell^2}{2r}.", 1,
               "C1, M11, D3 bargaining profits g_{H,eta}, g_{L,eta}, as in Figure 4"))
    # ---------------------------------------------------------------- A.9
    E.append(R("o42a", "I couple the feedback and price-hidden economies at \\(r=r_1\\) using the\nsame \\((\\Theta,R,C,Z)\\) and full informed orders.",
               "This section computes in the point-mass benchmark with \\(\\pi=1/2\\);\n(A.39)--(A.41) of the paper give the "
               "general class formulas. I couple\nthe feedback and price-hidden economies at \\(r=r_1\\) using the same\n"
               "\\((J,R,C,Z)\\) and full informed orders.", 1, "M3 benchmark label; C5"))
    E.append(R("o42b", "environments. The high-cost type remains out when price information is\nunavailable",
               "environments. The high-cost realization stays out when price information\nis unavailable", 1, "C16"))
    E.append(R("o42c", "marginal full-order flow density \\(g(x)=[f(x-1)+f(x+1)]/2\\) to obtain",
               "marginal full-order flow density \\(\\bar f(x)=[f(x-1)+f(x+1)]/2\\) to obtain", 1, "C23 bar f"))
    E.append(R("o42d", "\\Delta\\mathcal W=(1-\\rho)\\int g(x)\n", "\\Delta\\mathcal W=(1-\\rho)\\int \\bar f(x)\n", 1, "C23"))
    E.append(R("o42e", "For an atomless high-cost component \\(H_H\\), replace the integrand by",
               "For an atomless high-cost component \\(H_C^1\\), replace the integrand by", 1, "C27"))
    E.append(R("o42f", "\\mathbf1\\{c\\le B_r(\\mu_X(x))\\}\\,H_H(dc).", "\\mathbf1\\{c\\le B_r(\\mu_X(x))\\}\\,H_C^1(dc).", 1, "C27"))
    E.append(R("o42g", "Target proceeds increase by averaging \\(t_\\theta-t_0>0\\) over each\nstate's additional-entry probability.",
               "Target proceeds increase by averaging \\(t_j-t_0>0\\) over each\nclass's additional-entry probability.", 1, "C5"))
    E.append(R("o42h", "costs integrate the corresponding state-specific tail probabilities over",
               "costs integrate the corresponding class-conditional tail probabilities over", 1, "C5"))
    E.append(R("o42i", "+\\frac12\\sum_\\theta\\bar e_\\theta\\left(g_\\theta+\\frac{p^2}{r}\\right)",
               "+\\frac12\\sum_j\\bar e_j\\left(g_j+\\frac{p^2}{r}\\right)", 1, "C5"))
    # ---------------------------------------------------------------- A.10
    E.append(R("o43a", "\\qquad\nG(R,v,p)=(v-\\max(p,R))_+.", "\\qquad\ng(R,v,p)=(v-\\max(p,R))_+.", 1, "C1 realized profit g"))
    E.append(R("o43b", "These formulas include no sale when both values fail the reserve. They\nare bounded, Borel, and can be integrated first over \\(R\\) and then over\nany conditional challenger distribution.",
               "These formulas include no sale when both values fail the reserve. The\nrevenue kernel is at most "
               "\\(\\max\\{p,R\\}\\), bounded on the incumbent's\nsupport. The profit kernel satisfies \\(0\\le g(R,v,p)\\le v\\). "
               "Finite class\nmeans therefore make both kernels integrable. Both are Borel and can be\nintegrated first over \\(R\\) "
               "and then over any conditional challenger\ndistribution.", 1, "M5 the profit kernel is bounded by v, not uniformly"))
    E.append(R("o43c", "t_H&=\\frac r2+\\frac{p^2}{2r},\\qquad g_H=h-t_H,\\qquad\n\\Delta_T=\\frac{(r-\\ell)^2}{2r}+\\frac{\\varepsilon_V^2}{6r}.",
               "t_H&=\\frac r2+\\frac{p^2}{2r},\\qquad g_H=h-t_H,\\qquad\n\\Delta_T=\\frac{(r-\\ell)^2+\\varepsilon_V^2/3}{2r}.", 1,
               "C35 one writing of the class spread"))
    E.append(R("o43d", "\\(q_\\theta(p)\\) continuously differentiable on \\(I\\), and an atomless",
               "\\(q_j(p)\\) continuously differentiable on \\(I\\), and an atomless", 1, "C5"))
    E.append(R("o43e", "profit range. Suppose \\(\\mu_\\theta(z;p)\\) is differentiable in \\(p\\) for\nalmost every \\(z\\) and there is an integrable function \\(J(z)\\)",
               "profit range. Suppose \\(\\mu_j(z;p)\\) is differentiable in \\(p\\) for\nalmost every \\(z\\) and there is an "
               "integrable function \\(\\Lambda(z)\\)", 1, "C5; J is now the class variable"))
    E.append(R("o43f", "f(z)\\left|h_C(B_{p,r}(\\mu_\\theta))\\left[-p/r+(g_H-g_L)\\partial_p\\mu_\\theta\\right]\\right|",
               "f(z)\\left|h_C(B_{p,r}(\\mu_j))\\left[-p/r+(g_H-g_L)\\partial_p\\mu_j\\right]\\right|", 1, "C5"))
    E.append(R("o43g", "uniformly on a compact neighborhood of the reserve. These assumptions\nare sufficient, not an assertion that every continuation has them. For\npositive smooth noise",
               "uniformly on a compact neighborhood of the reserve. For\npositive smooth noise", 1, "C41"))
    E.append(R("o43h", "For \\(\\bar e_\\theta(p)=\\int f(z)H_C(B_{p,r}(\\mu_\\theta(z;p)))\\,dz\\),",
               "For \\(\\bar e_j(p)=\\int f(z)H_C(B_{p,r}(\\mu_j(z;p)))\\,dz\\),", 1, "C5"))
    E.append(R("o43i", "\\frac{d\\bar e_\\theta}{dp}\n=\\int f(z)h_C(B_{p,r}(\\mu_\\theta))\n\\left[-\\frac p r+(g_H-g_L)\\frac{\\partial\\mu_\\theta}{\\partial p}\\right]dz.",
               "\\frac{d\\bar e_j}{dp}\n=\\int f(z)h_C(B_{p,r}(\\mu_j))\n\\left[-\\frac p r+(g_H-g_L)\\frac{\\partial\\mu_j}{\\partial p}\\right]dz.",
               1, "C5"))
    E.append(R("o43j", "\\(\\mathcal R_T=t_0+\\sum_\\theta\\bar e_\\theta(t_\\theta-t_0)/2\\), the",
               "\\(\\mathcal R_T=t_0+\\sum_j\\bar e_j(t_j-t_0)/2\\), the", 1, "C5"))
    E.append(R("o43k", "+\\frac12\\sum_\\theta\\frac{d\\bar e_\\theta}{dp}(t_\\theta-t_0).",
               "+\\frac12\\sum_j\\frac{d\\bar e_j}{dp}(t_j-t_0).", 1, "C5"))
    E.append(R("o43l", "For the local decomposition in the paper, impose a neighborhood \\(I\\)\ncontained strictly in",
               "For the local decomposition in the paper, which keeps the benchmark prior\n\\(\\pi=1/2\\), impose a neighborhood \\(I\\) contained strictly in",
               1, "C10 benchmark scope of the local decomposition"))
    # ---------------------------------------------------------------- A.11, A.12
    E.append(R("o44", "Entry is therefore at least \\(\\rho\\) at every price. In the reserve example\nthat the earlier construction used, gross profit at a candidate pooled\nposterior \\(\\bar\\mu\\) was \\(3\\bar\\mu>0\\). A zero-cost buyer who saw that pooled\nprice would prepare, so the prescribed nonpreparation at the pooled price\nfails at the first buyer check, before any pricing or trading check.",
               "Entry is therefore at least \\(\\rho\\) at every price. Any candidate that\nprescribes zero preparation at a pooled "
               "price violates the zero-cost\nbuyer's optimality condition and the tie rule.", 1,
               "M12 over C4 and P-S12: general argument, covers zero gross profit"))
    E.append(S("o45", "\\subsection{A.12. An informed shareholder}", MOVE_ANCHOR, [
        ("a(q)", "\\alpha(q)", 4), ("a'(q)", "\\alpha'(q)", 2),
    ], "C25 entry-set probability alpha(q)"))
    E.append(R("o45b", "-\\int_{\\mathcal X_\\tau\\cap(-\\infty,q)}f(x-q)\\,dx\\right],\n\\qquad\n|\\alpha'(q)|\\le\\frac{\\min\\{\\alpha(q),1-\\alpha(q)\\}}b\\le\\frac1{2b}.",
               "-\\int_{\\mathcal X_\\tau\\cap(-\\infty,q)}f(x-q)\\,dx\\right],\\\\\n|\\alpha'(q)|\\le\\frac{\\min\\{\\alpha(q),1-\\alpha(q)\\}}b\\le\\frac1{2b}.\n\\end{gathered}",
               1, "layout: (OA.62) on two lines after the alpha rename"))
    E.append(R("o45c", "\\[\n\\alpha'(q)=\\frac1b\\left[", "\\[\n\\begin{gathered}\n\\alpha'(q)=\\frac1b\\left[", 1,
               "layout: (OA.62) on two lines after the alpha rename"))
    E.append(R("o45d", "\\tag{OA.59}\\label{eq:oa-oa-59}\n\\]\n\nExpected payoffs then split",
               "\\tag{OA.59}\\label{eq:oa-oa-59}\n\\]\n\nHere the argument is the signed order. Appendix A.2 of the paper uses the\norder magnitude \\(s\\), so its \\(\\bar A_L(s)\\) equals \\(\\bar A_L(-s)\\) here.\nExpected payoffs then split",
               1, "C6 one name, two argument conventions stated"))
    # ---------------------------------------------------------------- Part B
    E.append(S("o46", MOVE_ANCHOR, "\\section{C. Numerical exercises and quantity registry}", [
        ("F_\\epsilon", "\\bar A_\\epsilon", 4), ("F_L", "\\bar A_L", 9), ("F_H", "\\bar A_H", 4),
    ], "C6 bar A in the certificate appendix"))
    # ---------------------------------------------------------------- C.0 to C.9, E
    E.append(R("o47a", "proportional to \\(\\operatorname{sech}(z/b)\\). The Student law has\n\\(\\nu=3\\) degrees of freedom and scale \\(b(\\nu+1)/(2\\sqrt{\\nu})\\). The",
               "proportional to \\(\\operatorname{sech}(z/b)\\). The Student law has\nthree degrees of freedom and scale "
               "\\(2b/\\sqrt3\\). The", 1, "C21 nu is the flow measure"))
    E.append(R("o47b", "upper plateau enters at tau = M; lower plateau enters at B(m) = c\\_L;}",
               "upper plateau enters at tau = M; lower plateau enters at B(m) \\textgreater{}= 0;}", 1,
               "C15 tie rule without c_L (contract source listed for numerics)"))
    E.append(R("o47c", "tails are explicitly bounded. For a bounded residual \\(A\\le\\overline A\\)\nand \\(|q|\\le1\\), a Laplace truncation outside \\([-T,T]\\), \\(T>1\\), loses\nat most \\(\\overline A e^{-(T-1)/b}\\) in per-unit gross profit.",
               "tails are explicitly bounded. For a bounded residual \\(A\\le A^+\\)\nand \\(|q|\\le1\\), a Laplace truncation outside "
               "\\([-\\bar x,\\bar x]\\),\n\\(\\bar x>1\\), loses at most \\(A^+e^{-(\\bar x-1)/b}\\) in per-unit gross\nprofit.",
               1, "C24 A^+; C29 truncation bound bar x"))
    E.append(R("o47d", "bound is \\(2\\overline A/[1+e^{(T-1)/b}]\\).", "bound is \\(2A^+/[1+e^{(\\bar x-1)/b}]\\).", 1, "C24, C29"))
    E.append(R("o47e", "\\epsilon_q=\\max_\\theta\\left\\{\\sup_{q\\in[-1,1]}U_\\theta(q;\\sigma)-\\int U_\\theta(q;\\sigma)\\,d\\sigma_\\theta(q)\\right\\}.",
               "\\epsilon_q=\\max_j\\left\\{\\sup_{q\\in[-1,1]}U_j(q;\\sigma)-\\int U_j(q;\\sigma)\\,d\\sigma_j(q)\\right\\}.", 1, "C5"))
    E.append(R("o47f", "Mandatory probability identities are \\(\\int a_\\theta=1\\),\n\\(\\mathbb E\\mu_X=1/2\\),",
               "Mandatory probability identities are \\(\\int a_j=1\\),\n\\(\\mathbb E\\mu_X=\\pi\\),", 1,
               "C5; prior pi (one half in every declared exercise)"))
    E.append(R("o48", "then reads \\(B_{r_1}(m)-2\\varepsilon_C\\). Verify all\nmargins before assigning an analytical equilibrium label.",
               "then reads \\(B_{r_1}(m)-2\\varepsilon_C\\) and is a strict condition. Verify the\nstrict margins before "
               "assigning an analytical equilibrium label: four for\ncost atoms, where \\(\\zeta_L\\) needs no strict sign, and "
               "five for the\natomless mixture.", 1, "C2, M7 four strict margins for cost atoms"))
    E.append(R("o49", "belief is the prior and both high-cost private-signal types stay out.",
               "belief is the prior and the high-cost realization stays out after either\nprivate signal.", 1, "C16"))
    E.append(R("o50a", "each ratio let \\(D=h-\\ell\\) and examine \\(\\delta_j=D2^{-j}\\) for integer\n\\(j\\) from \\texttt{1} through \\texttt{20}. Define \\(r_1=\\ell+\\delta_j\\)\nand \\(r_0=\\ell+\\delta_j^2/D\\).",
               "each ratio let \\(\\Gamma=h-\\ell\\) and examine \\(\\delta_n=\\Gamma2^{-n}\\) for\ninteger \\(n\\) from \\texttt{1} "
               "through \\texttt{20}. Define\n\\(r_1=\\ell+\\delta_n\\) and \\(r_0=\\ell+\\delta_n^2/\\Gamma\\).", 1,
               "C7 Gamma; C26 index n"))
    E.append(R("o50b", "Keep the sequence of failed and\nsuccessful \\(j\\) values.", "Keep the sequence of failed and\nsuccessful \\(n\\) values.", 1, "C26"))
    E.append(R("o51a", "A mixed candidate with support points \\(q_{\\theta j}\\) and weights\n\\(\\omega_{\\theta j}\\) has conditional density\n\\(a_\\theta(x)=\\sum_j\\omega_{\\theta j}f(x-q_{\\theta j})\\).",
               "A mixed candidate with support points \\(q_{jn}\\) and weights\n\\(\\omega_{jn}\\) has conditional density\n"
               "\\(a_j(x)=\\sum_n\\omega_{jn}f(x-q_{jn})\\).", 1, "U3/D3 class index j, support index n"))
    E.append(R("o51b", "records each state's final support", "records each class's final support", 1, "U3/D3"))
    E.append(R("o52a", "declared reserve alternatives; and the two exact events of the paper\nappendix, the zero-cost floor equality,",
               "declared reserve alternatives; and the two exact events of A.14, the\nzero-cost floor equality,", 1,
               "D6 references follow the moved events"))
    E.append(R("o52b", "and at \\(p_H\\) the high-cost type enters on the upper", "and at \\(p_H\\) the high-cost realization enters on the upper", 1, "C16"))
    E.append(R("o53", "That family needed a positive low preparation cost.\nAt its pooled price, gross profit \\(3\\bar\\mu_c\\) fell below that cost, so the\nbuyer stayed out at the pooled price and prepared at each separate positive price.\nUnder the declared cost law the low cost is zero and \\(3\\bar\\mu_c>0\\).\nThe buyer at the pooled price then prepares. The prescribed preparation policy\nfails its first buyer check, and no member of the family is a continuation.",
               "That family needed a positive low preparation cost.\nAt its pooled price, gross profit fell below that cost, so the\n"
               "buyer stayed out at the pooled price and prepared at each separate positive price.\n"
               "Under the declared cost law the low cost is zero. A candidate that prescribes\nzero preparation at a pooled price "
               "then violates the zero-cost buyer's\noptimality condition and the tie rule, so no member of the family is a\ncontinuation.",
               1, "M12, C4 retired example without its undefined profit"))
    E.append(R("o54", "range schema of C.6. Feed: the exact-event paragraphs of the paper\nappendix and the online summary of C.6.",
               "range schema of C.6. Feed: A.14, the exact-event summary in Appendix A.7\nof the paper, and the online summary of C.6.",
               1, "D6 feed follows the moved events"))
    E.append(R("o55", "weak distributions for \\(\\Delta_\\eta\\) and \\(G_{\\theta,\\eta}\\). The",
               "weak distributions for \\(\\Delta_\\eta\\) and \\(g_{\\theta,\\eta}\\). The", 1, "C1, D3"))
    E.append(R("o55b", "Feed: Figure 4 and Proposition A.8. Parameter values and the change of",
               "The columns \\texttt{G\\_H\\_eta} and \\texttt{G\\_L\\_eta} keep their schema names\nand hold \\(g_{H,\\eta}\\) and \\(g_{L,\\eta}\\). Feed: Figure 4 and Proposition A.8.\nParameter values and the change of",
               1, "C1 schema names mapped to the renamed profits"))
    E.append(R("o56", "\\(k\\). The proceeds gain is the second line of (A.41) in the paper,",
               "\\(k\\). The proceeds gain is the second line of (A.41) in the paper at\n\\(\\pi=1/2\\),", 1,
               "M3, C3a the paper's display now carries the prior"))
    E.append(R("o57", "signal mode uses the conditional laws of Appendix A.7. The exploratory",
               "signal mode uses the conditional laws of Appendix A.7 above. The exploratory", 1, "C33"))
    return E


LEFTOVER = [
    ("\\Theta", 0), ("t_\\theta", 0), ("e_\\theta", 0), ("\\mu_\\theta", 0), ("_\\theta(", 0), ("\\sum_\\theta", 0),
    ("\\max_\\theta", 0), ("F_\\epsilon", 0), ("F_\\theta", 0), ("F_H", 0), ("F_L", 0), ("J_H", 0), ("J_L", 0),
    ("\\overline A", 0), ("G_{H,\\eta}", 0), ("G_{L,\\eta}", 0), ("G_{\\theta,\\eta}", 0), ("G(R,v,p)", 0),
    ("\\mathcal C_L", 0), ("\\ell_b", 0), ("e_r(", 0), ("P_r", 0), ("Lemma OA.3", 0), ("result-lemma-oa-2", 0),
    ("3\\bar\\mu", 0), ("earlier construction", 0), ("B(m) = c\\_L", 0), ("type remains", 0),
    ("private-signal types", 0), ("high-cost type", 0), ("H_H", 0), ("\\nu=3", 0), ("v_L", 0), ("v_H", 0),
]
