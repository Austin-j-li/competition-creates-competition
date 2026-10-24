Part 1: findings

FINDING:
- Name: The lower-boundary statement incorrectly requires trade at the weak incumbent
- Severity: Critical
- Location: `slot/manuscript/appendix/A3_proposition2.tex:169`, Proposition “The admissible region,” part (b); also its proof at line 208.
- Problem: At the lower slot boundary, the proposition states full orders at all three strengths, although the weak economy strictly requires abstention.
- Proposed fix: State that orders are uniquely zero at the weak strength and uniquely full at the other two strengths.
- Evidence: At \(u=82/59\), the weak economy still has

  \[
  \Delta_0=\frac1{60}<\frac1{50}=k.
  \]

  Under every candidate, each correct order therefore earns at most

  \[
  \Delta_0-k=-\frac1{300}<0,
  \]

  while abstention earns zero. Thus \(\sigma_H=\sigma_L=\delta_0\) at \(r_0\), under all four tie-rule pairs. Even the proposed full-order purchase earns

  \[
  \Delta_0\left(1-\frac{141}{200}\right)-k
  =-\frac{181}{12000}<0.
  \]

  The same sentence says every conclusion of the core proposition holds, but its part (i) explicitly requires no trade. The upstream proof package correctly restricts full orders to the two stronger economies at `proofs/P1_core.tex:1160`. This is a false statement within the boundary proposition. It does not invalidate the core proposition or the interior admissible region.

FINDING:
- Name: The low-class sale rate reuses the target-proceeds symbol
- Severity: Mid
- Location: `slot/manuscript/appendix/A4_coexistence.tex:204`, Lemma “The low class”; lines 263–276 and 317–322 repeat the collision.
- Problem: The appendix uses \(t_L(r)\) for the informed sale rate, although the model already uses this symbol for expected low-class target proceeds.
- Proposed fix: Rename the sale rate \(s_-^*(r)\) throughout Appendix A.4 and retain \(t_L(r)\) for target proceeds.
- Evidence: Section 2 defines \(t_j\) as expected target proceeds at `sections/02_model.tex:193`. Section 3 gives

  \[
  t_L(3)=1-\frac{1-1/4}{6}=\frac78.
  \]

  Appendix A.4 instead gives \(t_L(3)=\lambda\), since \(3>r_S\), where

  \[
  \lambda\in[0.336121768915121197,\;0.336121768915121198].
  \]

  Both meanings occur in the same tuple construction. The price formula needs target proceeds; the order formula needs the sale rate. The upstream package uses \(\bar t(r)\) for the latter at `proofs/P1_core.tex:687`. The earlier \(a_j(x)\) collision does not survive: the merged core uses \(f_j(x)\) for order probabilities.

Part 2: coverage

The audit covers branch `slot`, commit `2c56325`, and the files specified in the brief. The core three-economy proof and the coexistence classification are correct, subject to the two findings above.

I read the assigned manuscript files in full. I consulted only the permitted design brief, registry, proof package, and P1 scripts and logs. I did not read earlier verdicts. I did not edit repository files, write assertions, run a test suite, or compile the manuscript. The repository was clean before and after the audit.

The independent arithmetic worksheet is [recompute.py](scripts/core_2/recompute.py). Its output is [recompute.log](scripts/core_2/recompute.log). The complete value list is [recomputed_values.csv](scripts/core_2/recomputed_values.csv).

The worksheet uses exact fractions, exact polynomial arithmetic, rational root brackets, and outward interval arithmetic at 85 digits. It obtains Euler’s number from

\[
S_{110}=\sum_{n=0}^{110}\frac1{n!},\qquad
S_{110}<\mathrm e<S_{110}+\frac{112}{111\cdot111!}.
\]

Every root bracket for \(r_A,r_J,r_*\) has width below \(10^{-70}\), with opposite endpoint signs. No sign claim rests on a floating-point approximation.

Results and equation groups checked:

- **Model and equilibrium definition.** I checked the observation sets, conditional independence, reserve admissibility, entry timing, and conditions (E1)–(E6) in Section 2. Zero-cost preparation is an explicit selection at a possible zero-rent tie. Continuous incumbent values remove acquisition-value ties. The investor’s deviation holds prices and the entry rule fixed.
- **Truthful bids.** I reproduced Appendix A.1’s comparison against every competing bid. An admissible truthful bidder obtains the positive part of its value minus the required payment. A value below the reserve optimally submits no bid.
- **Uniform auction payoffs.** I integrated the payments and profits over the incumbent value. This reproduces \(t_0,t_H,t_L,g_H,g_L\), \(\Delta_T=(r-\ell)^2/(2r)\), and every derivative in equations `eq:payoffs`, `eq:derivatives`, and `eq:a-payoffs`. The identities \(t_H+g_H=h\) and \(t_L+g_L=\ell\) hold.
- **General payoff formulas and Proposition 1(a)–(b).** I reproduced the indicator integrals and both Tonelli steps in A.1. Atoms at the reserve require the term \(pF(p)D(p^-)\); the manuscript includes it. Finite means justify the integrals. A stochastic strengthening weakly lowers each acquisition profit. Equal admissibility removes the negative reserve term from the spread comparison. The strictness conditions match the resulting integrals.
- **Proposition 1(c).** I independently derived the kernel \(\xi(R)=pD(p^-)\) below the reserve and \(\xi(R)=\int_p^R D(y)\,dy\) above it. Its monotonicity is equivalent to the stated conditions. The shifted uniform distributions prove necessity. Right continuity justifies the pointwise condition above the reserve. Without reserve atoms, the conditions imply equal admissibility.
- **Profit threshold and ownership.** I checked \(B(\mu)=g_L+\mu(g_H-g_L)\), \(\tau=(c_H-g_L)/(g_H-g_L)\), and the benchmark threshold formula. I also checked \(W_H(F)=\mathbb E_H[F(\theta)\mathbf1\{\theta\ge p\}]\). For the uniform benchmark, \(h>r\) gives \(W_H=1\).
- **Order probabilities and beliefs.** I reproduced the likelihood ratios in Section 3 and A.2 for every mixed profile. For the zero order, \(b_0\ge b\) holds exactly when \(\beta\le1/3\). Section 2 states this primitive restriction explicitly. With \(\beta>1/3\), high-class abstention and no low-class abstention yield the stated counterexample. Full orders give \((m,\pi,M)\).
- **Beliefs at pooled prices and the exclusion corollary.** A price posterior is a probability-weighted average of its order posteriors. Thus \(B(M)<c_H\) excludes high-cost preparation under every admissible profile. This result uses the zero-order bound; the three-economy proof can instead force full orders first.
- **Entry and prices lemma.** I reproduced the terminal-payoff expectation and competitive price formula. Equal prices imply equal entry. Since \(e\ge\rho>0\) and \(\Delta_T>0\), equal prices then imply equal posteriors. The price-increment identity has two nonnegative terms and yields the stated strict lower bound. The CM exception at the threshold is explicit.
- **Informed-trading lemma.** I reproduced all six investor payoffs against fixed prices and entry. Wrong orders lose at least \(k\). The correct-order bounds hold for every candidate, including mixtures:

  \[
  \rho\Delta_T[1-M]\le K_H\le\Delta_T,
  \qquad
  \rho\Delta_Tm\le K_L\le\Delta_T.
  \]

  Hence the manuscript’s \(\kappa=\min\{m,1-M\}\) exactly matches the design brief. The bound in (H2) does not assume the proposed equilibrium.

- **Core proposition, part (i).** I checked the explicit zero-order tuple against all six conditions. The universal upper bound proves uniqueness. Bayes consistency gives the prior after every order; entry is \(\rho\); every price equals \(t_0+\rho[t_L-t_0+\Delta_0\pi]\).
- **Core proposition, part (ii).** I checked the full-order tuple against all six conditions and all investor alternatives. The universal lower bound forces full orders in every equilibrium. The entry vector is \((\rho,\rho,1)\), and the three prices differ. I reproduced

  \[
  \mathsf E_1=\rho+(1-\rho)(b+\pi\lambda),\qquad
  e_H=\rho+(1-\rho)(b+\lambda).
  \]

  Conditional independence gives high-class ownership \(\pi e_HW_H(F_1)\). Both the exact ownership condition and its stated sufficient condition are correct.

- **Core proposition, part (iii).** Stochastic strengthening gives \(\Delta_2\ge\Delta_1\), so full orders remain uniquely optimal. Every resulting posterior is at most \(M\); (H3) therefore gives entry \(\rho\). This argument also covers \(g_{H,2}=g_{L,2}\). Competitive prices still differ because \(\Delta_2>0\).
- **Core tie rules.** Investor choices and high-cost preparation are strict at all three equilibrium tuples. All four tie-rule pairs therefore give the same outcome. The worksheet prints each correct-order net return and each wrong-order payoff against the fixed benchmark tuples.
- **Necessity of the weak-economy prior condition.** I recomputed the example with \(c_H=47/10\) and third strength 8. All retained hypotheses hold, but \(c_H-B_0(1/2)=-5/48\). The weak economy has entry one. Replacing the original condition by \(B_1(\pi)<c_H\) therefore fails.
- **Admissible region.** I independently solved (H1)–(H3). At prior one half, the exact band is \(82/59<u<2686/1559\). The trade bound adds \(u<19/3\), which is redundant within that band. I checked the presence intervals, both prior intervals, their containment within the trade-bound interval, and the relative open-set statement. The boundary allocation is correct after the first finding’s correction.
- **Path lemma.** I differentiated \(\tau\), \(J\), and \(\Delta_T(1-\tau)^2\). The two printed derivative polynomials match the independent derivation. Exact Sturm variations are 3 and 3 for \(J'\) on \([6/5,18/5]\), and 5 and 5 for the second polynomial on \([6/5,2]\). Both left values are positive. The second polynomial also has no root through \(18/5\), consistent with the main-text summary. Positivity of both factors proves the claim for \(\Delta_T\tau\).
- **Threshold definitions and order.** I checked all six thresholds and each inequality in A.4’s threshold-order lemma. The band implies the complete strict order. Exact root brackets reproduce \(r_A,r_J,r_*\); the closed forms reproduce \(r_F,r_N,r_S,r_C\).
- **High-class and low-class lemmas.** I derived \(\mu_+(s)\), \(\mu_-(t)\), \(s^*\), and every N, Q, R, T, and F case. Strict monotonicity gives uniqueness of each interior rate. I checked the weak and strict inequalities at every endpoint under IM and I0. The formulas are correct after the notation repair.
- **Product structure and complete equilibrium set.** I checked each tuple component and conditions (E1)–(E6). The proof establishes \(s\ge t\) for every eligible pair at prior one half. Thus the zero order cannot recruit. The listed equilibrium set is complete, including \(r_A,r_F,r_N,r_J,r_S,r_C\).
- **Entry along the coexistence branches.** I reproduced \(\mathsf E_R=\rho+(1-\rho)b\Delta_T/(2k)\), its continuous join to F, and the constant segment. The increase applies before the ceiling; entry falls to \(\rho\) above \(r_C\). For T, I derived the displayed ratio and its strict decrease. The proof correctly uses \(r_J<2\).
- **Alternative tie rules.** I checked the extra T branch under CM and the entry interval at \(r_C\). Under I0, neither abstention nor a full sale qualifies on \((r_N,r_S]\), while a mixture is prohibited. The stated empty equilibrium set on that interval is correct.
- **Coexistence at every prior.** I independently derived the set \(C(\pi)\), all four prior cases, and the branch-entry formula. The low class must abstain whenever no trade coexists with an informative equilibrium. I checked the singleton at the lower prior boundary and the open left endpoint in case (c). The CM addition at \(r_\pi\), including \(\pi_{\max}\), and the stricter I0 condition are correct.
- **Fixed-information controls.** With the experiment fixed, every signal gives the same posterior across strengths. Lower gross profit weakly reduces entry under C1. I independently computed every control row in Section 4 from its fixed orders or hidden-price rule.
- **Abstract and introductory core claims.** The claims about entry, uniqueness, coexistence, and the ceiling agree with the audited results. The ownership claim holds on an open neighborhood of the benchmark, where \(W_H=1\).

Number families checked:

- **All 192 distinct registry references in the assigned main text and A.1–A.4, plus the core declarations and margins in A.9.** Every computed value matches the printed precision. The corresponding `numbers.tex` displays match the registry. The CSV records each key separately.
- **Primitives and slot quantities:** all `prim_*` references, exact \(\beta\), \(u,\lambda,b,b_0,m,M\), and \(b+\lambda\).
- **Auction quantities:** all three-strength payoff rows, spreads, prior profits, thresholds, exact threshold fractions, and the auxiliary values of \(J\).
- **Equilibrium and control quantities:** all order posteriors, prices, entry probabilities, ownership probabilities, expected proceeds, and cost-crossing probabilities. Entry at \(r_1\) is \(0.522756943478406672\) to 18 decimal places; ownership is \(0.324401303410788560\).
- **Region quantities:** both slot endpoints, posterior endpoints, presence intervals at both liquidity probabilities, prior windows, and every displayed distance to their boundaries.
- **Core strict margins:** all (H1)–(H3) margins, implied inequalities, ownership margins, the structural liquidity margin, and the modified-cost counterexample.
- **Coexistence quantities:** all threshold levels and gaps, prior cutoffs, the R and T entry examples, the CM endpoint, and the exact polynomial endpoint value.
- **Introduction previews:** the bid–ask entry share and all six research numbers match independent arithmetic. For the latter, I used the declared quadratic cost and the interior condition

  \[
  (k+2a\lambda)\,[2\beta(1-\lambda)+\lambda]
  =\Delta_T\beta(1-\lambda),\qquad a=\frac1{40}.
  \]

  This verifies those six numbers, not the research theorem.

The small return margin is certified. Independent outward enclosures are

\[
\tau(r_2)-M\in
[0.000333564719409317854285,\;0.000333564719409317854286],
\]

\[
c_H-B_{r_2}(M)\in
[0.002688902265905112258710,\;0.002688902265905112258711],
\]

\[
r_C\in
[3.592658518794661833335916,\;3.592658518794661833335917],
\]

\[
r_2-r_C\in
[0.007341481205338166664083,\;0.007341481205338166664084].
\]

The permitted P1 source also uses outward intervals, rather than a rounded value of Euler’s number. Its recorded enclosures agree with these results. The computer-assisted labels on the path and coexistence results match their exact polynomial certificates. The numerical enumeration remains a diagnostic and supplies no proof step.

Not checked:

- The full research, robustness, welfare, and empirical proofs in Sections 5–8 and Appendices A.5–A.8.
- A.9’s non-core examples and margins, except inputs or numbers needed for the explicit computations above.
- The underlying research equilibrium conditions beyond the six introductory numerical previews.
- Figure data, graphical layout, citation accuracy, slides, the comparison note, or the compiled PDF’s visual presentation.
- The independent XP packages or earlier verdicts, which fall outside the permitted source list. I also did not run the historical numerical enumeration.
