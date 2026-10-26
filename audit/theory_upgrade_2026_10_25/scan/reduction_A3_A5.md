The reduction is valid for **orders, posteriors, entry, and research intensity** within the stated model. It does not reduce ownership or welfare to \((\Delta_T,\tau)\). The pointwise coexistence criterion generalizes; the benchmark’s cutoff ordering and research-branch endpoint require additional conditions.

**1. Generality table**

Write \(\Delta=\Delta_T\), \(\gamma=g_H-g_L\), \(J=\Delta(1-\tau)\), and \(w_L=t_L-t_0\). In every path comparison below, the classes, reserve, preparation cost, and trading/research primitives remain fixed; only \(F_s\) changes.

“A4 assumptions” means the point-mass/uniform benchmark, \((h,\ell,p,\rho,c_H,k)=(10,1,\tfrac12,\tfrac14,6,\tfrac1{50})\), \(r\in[\tfrac65,\tfrac{18}5]\), and the stated slot band. “A5 assumptions” means the benchmark auction, prior \(1/2\), quadratic research cost, and \(0<\beta\le1/3\). These restrictions appear at [A4:4–8](overleaf/slot/appendix/A4_coexistence.tex:4), [A5:22–33](overleaf/slot/appendix/A5_research.tex:22), and [numbers.tex:5016–5025](overleaf/slot/numbers.tex:5016).

| Name | Label | File:line | Stated hypotheses | What the proof uses beyond \(\Delta,\tau\) | Most general supported statement; conditions to add |
|---|---|---|---|---|---|
| Proposition 2 | `prop:ccc` | [sections/04:11–44](overleaf/slot/sections/04_equilibrium_results.tex:11); [A3:11–109](overleaf/slot/appendix/A3_proposition2.tex:11) | Ranked classes; continuous \(F_0,F_1,F_2\) ordered by FOSD; interior prior and slot; H1–H3. | FOSD gives \(B_1(\pi)\le B_0(\pi)\) and \(\Delta_2\ge\Delta_1\); price construction uses \(w_L\ge0\). Ownership uses \(W_H(F_i)\). No uniform law, point masses, even prior, or calibrated \(\rho\) enters the equilibrium proof. | **Already general.** Any \(0<\beta<1/2\) works. The exact ownership condition is already stated. FOSD can be replaced by the two scalar comparisons actually used, retaining the payoff-sign conditions. \(\gamma_2>0\) is unnecessary: H3 also handles \(\gamma_2=0\). |
| Proposition A.1 | `prop:region` | [A3:157–221](overleaf/slot/appendix/A3_proposition2.tex:157) | Fixed benchmark auction, costs and three strengths; prior \(1/2\) in (a)–(b); \(1+u=e\) in (c). | Exact \(\Delta_i,\tau_i\), \(\rho=1/4\), \(k=1/50\); numerical comparisons make some H1–H3 bounds redundant. | **Calibration-only as written.** For other auctions, intersect all H1–H3 inequalities; the same numerical band and redundancy claims do not follow. See 3(g). |
| Proposition 3, including full statement | `prop:coexistence` | [sections/04:272–283](overleaf/slot/sections/04_equilibrium_results.tex:272); [A4:287–396](overleaf/slot/appendix/A4_coexistence.tex:287) | A4 assumptions; prior \(1/2\); default IM/C1. | Strict path monotonicity, endpoint signs, and the complete cutoff ordering. The R/Q/T/F algebra itself uses only reduced payoffs. | The pointwise classification and entry formulas extend to general ranked auctions. The displayed interval table requires the crossing and ordering conditions in 3(c). Strict entry growth requires strictly increasing \(\Delta\), not merely FOSD. |
| Path lemma | `lem:a4-path` | [A4:20–62](overleaf/slot/appendix/A4_coexistence.tex:20) | A4 assumptions. | Uniform/point-mass formulas; calibrated polynomial signs for \(J'\) and \([\Delta(1-\tau)^2]'\); \(\tau(r_0)>1/2\), \(\tau(r_2)<3/4\), and endpoint values. | FOSD gives weak growth of \(\Delta,\tau,\Delta\tau\) on the positive-threshold domain. It gives **no general monotonicity of \(J\) or \(\Delta(1-\tau)^2\)**. Strictness and the latter two signs require additional conditions. |
| Threshold-order lemma | `lem:a4-order` | [A4:85–104](overleaf/slot/appendix/A4_coexistence.tex:85) | A4 assumptions and slot band. | The path lemma; \(\rho=1/4\); \(\tau<3/4\); calibrated inequalities ensuring \(r_F<r_N\) and \(r_S<r_1\). | Replace these numerical facts by attained crossings and the scalar ordering inequalities in 3(c). FOSD alone does not imply the ordering. |
| High-class lemma | `lem:a4-high` | [A4:149–190](overleaf/slot/appendix/A4_coexistence.tex:149) | Inherited A4 assumptions; \(\pi<\tau\); candidate with no wrong-signed orders. | Bayes’ rule, entry rule, investor tie rule; \(\tau<1\) when defining \(s^*\). No auction closed form. | The N/Q/R/T/F characterization is pointwise general for \(\Delta>0,\gamma>0,\pi<\tau<1\). For \(\tau\ge1\), remove recruitment/threshold forms and define Q directly by \(\mu_+(s)<\tau\); the displayed \(s^*\) formula cannot be used. |
| Low-class lemma | `lem:a4-low` | [A4:193–221](overleaf/slot/appendix/A4_coexistence.tex:193) | Inherited A4 assumptions; \(\pi<\tau\); no wrong-signed orders. | Strictly decreasing sale posterior and the investor tie rule. | Entire characterization, unique IM sale rate, and I0 nonexistence interval extend pointwise to general ranked auctions with \(\Delta>0,\gamma>0,\pi<\tau\). No upper bound \(\tau<1\) is needed. |
| Product lemma | `lem:a4-product` | [A4:224–255](overleaf/slot/appendix/A4_coexistence.tex:224) | \(\pi<\tau\), \(s\ge t\), inherited payoff assumptions. | \(s\ge t\) implies \(\mu_0\le\pi\); construction uses \(w_L\ge0\), and explicitly checks equal entry at equal posteriors. | General pointwise result. Keep \(s\ge t\), or separately impose the correct entry response at \(\mu_0\). Nonnegative entry gains are automatic for this auction. |
| Corollary A.2 | `prop:priors` | [A4:440–530](overleaf/slot/appendix/A4_coexistence.tex:440) | Benchmark auction/path; any interior prior and slot; IM/C1. | The pointwise proof uses reduced payoffs. Cases (a)–(d) additionally use monotone crossings, \(\tau_A>1/2\), and \(\tau_A<3/4=1-\rho\). | The general criterion replaces \(r\ge r_A\) by \(J(F)\ge k\), exactly as in 3(b). Cases (a)–(d) require the crossing and start-feasibility conditions in 3(e). |
| Proposition 4 | `prop:research` | [sections/05:52–70](overleaf/slot/sections/05_research.tex:52); [A5:233–283](overleaf/slot/appendix/A5_research.tex:233) | Benchmark auction, prior \(1/2\), \(a>0,\beta\le1/3\); calibrated \(a,\bar\lambda\) and six strengths in (b). | Part (a): \(\Delta'(r)>0\) and \(W_H=1\). Part (b): certified scalar margins at the six calibrated strengths. | \(\lambda_R\) is smooth and strictly increasing **as a function of \(\Delta>2k\)**. Along FOSD it is only weakly increasing; \(C^1\) dependence on \(s\) needs \(C^1\) \(\Delta(s)\). Ownership needs its \(W_H\) factor. The six-point pattern generalizes under the corresponding scalar inequalities, not automatically. |
| Joint-deviation lemma | `lem:a5-joint` | [A5:64–82](overleaf/slot/appendix/A5_research.tex:64) | A5 assumptions; fixed candidate prices/entry; quadratic cost \(a>0\). | Success independent of class; fixed deviation-facing prices and entry; strict concavity. | General auction and general prior: use \(V=\pi\max U_H+(1-\pi)\max U_L\). Then \(\hat\lambda=\min\{\bar\lambda,V/a\}\). No further auction object enters. |
| Research bounds | `lem:a5-bounds` | [A5:85–102](overleaf/slot/appendix/A5_research.tex:85) | A5 assumptions; \(0\le\hat\lambda\le\bar\lambda<1\). | Full liquidity support; \(\beta\le1/3\) for the bound covering **the zero order**; even prior for the displayed symmetric bounds. | General ranked auction. The all-order bound retains \(\beta\le1/3\); nonzero-order bounds and the trading arguments need only \(\beta<1/2\). |
| Positive research/full purchase | `lem:a5-buy` | [A5:105–119](overleaf/slot/appendix/A5_research.tex:105) | A5 assumptions; \(\tau>1/2\); positive equilibrium research. | \(V>0\), the entry floor, and \(m_\lambda=1-M_\lambda\). | General ranked auction at prior \(1/2\), with \(\Delta>0,\gamma>0,\tau>1/2\). No requirement \(\tau<1\). The even-prior symmetry cannot simply be dropped. |
| Intermediate research equilibria | `lem:a5-middle` | [A5:122–200](overleaf/slot/appendix/A5_research.tex:122) | A5 assumptions; \(1/2<\tau<1\), \(\rho\Delta<2k\), \(\lambda_E\ne\bar\lambda\). | Research cost/cap, prior \(1/2\), tie rules, and automatic nonnegative entry gains. No uniform/point-mass formula. | The full Z/R/capped-R/T classification is pointwise general under those scalar hypotheses. The excluded \(\lambda_E=\bar\lambda\) boundary needs a separate CM case. Extending the full classification to \(\rho\Delta=2k\) also requires boundary treatment. |
| Strong-incumbent research lemma | `lem:a5-strong` | [A5:203–230](overleaf/slot/appendix/A5_research.tex:203) | A5 assumptions; \(\tau>1/2\), \(M_{\bar\lambda}\ne\tau\), and \(\rho\Delta m_{\bar\lambda}-k>a\bar\lambda\). | Uniform lower bounds on both trading returns; quadratic research best response. | General ranked auction under the same scalar conditions; \(\beta<1/2\) suffices. Condition U is sufficient for uniqueness, not a general necessary condition. |
| Proposition A.2 | `prop:researchregion` | [A5:316–384](overleaf/slot/appendix/A5_research.tex:316) | Calibration B except variable \(a,\bar\lambda\); fixed \(\beta=0.294655\). | Calibrated ordering of intermediate constraints, a bound on \(\varphi_a'\), and numerical inequalities making U redundant inside the displayed window. | **Calibration-only iff region.** For general auctions use the finite-point maxima/minima and additional endpoint conditions stated in 3(f). |
| Research tie remark | `rem:researchties` | [A5:388–407](overleaf/slot/appendix/A5_research.tex:388) | Calibrated research economy; CM versus C1. | Intermediate-point strict margins, numerical T-entry values, and U at/above the ceiling. | General T existence follows from the middle lemma. Its decreasing entry across strengths is not general. Under U, a ceiling tie permits the stated continuum of entry while research stays capped. |
| “The branch at calibration B” | — | [A5:286–314](overleaf/slot/appendix/A5_research.tex:286); [sections/05:119–126](overleaf/slot/sections/05_research.tex:119) | Full calibration B, including \(a=1/40\). | Uniform closed forms, a positive derivative bound for \(\varphi_a\), endpoint signs, and the separately verified ordering \(\bar r_R<r_N\). | The general branch is the intersection in 3(f). Single crossing of \(\varphi_a\) does **not** ensure termination at the cap or the claimed half-open interval. |
| “Access to prices with research” | — | [A5:410–421](overleaf/slot/appendix/A5_research.tex:410) | Calibration B at \(r_1\); visible-price versus hidden-price economy. | U makes order laws, research cost, and trade cost identical; proceeds use \(w_L\); allocation surplus uses \(g_j+pF(p)\). | Generalizes under \(\tau>1/2\), \(M_{\bar\lambda}>\tau\), and U. Replace \(p^2/r_1\) by \(pF(p)\). The signs generalize; the magnitudes require auction objects beyond \((\Delta,\tau)\). |

**2. Reduction lemma**

**Verdict: valid within the stated auction model, including CM and E7.** For research, \(a\) and \(\bar\lambda\) must also be fixed.

The precise statement I would sign is:

> Fix the model’s independence and information structure, the liquidity distribution, \(\pi\in(0,1)\), \(\rho\in(0,1)\), \(k>0\), and the tie rules. For fixed presence, fix \(0<\lambda<1\) and \(0<\beta<1/2\). Consider two auctions with \(\Delta>0\), \(\gamma>0\), and the same \((\Delta,\tau)\). Their equilibrium projections onto \((\sigma_H,\sigma_L,\mu,e)\) coincide. Prices and price-indexed preparation strategies are recovered separately for each auction. With research, fix \(a>0\), \(0<\bar\lambda<1\), and impose E5 after a hypothetical success even at \(\hat\lambda=0\); then the projections onto \((\hat\lambda,\sigma_H,\sigma_L,\mu,e)\) coincide.

The reduced system consists of Bayes’ rule, the threshold entry rule, and

\[
\begin{aligned}
U_H(1)&=e(1)\Delta[1-\mu(1)]-k,&
U_H(-1)&=-e(-1)\Delta[1-\mu(-1)]-k,\\
U_L(-1)&=e(-1)\Delta\mu(-1)-k,&
U_L(1)&=-e(1)\Delta\mu(1)-k,
\end{aligned}
\qquad U_j(0)=0.
\]

These are exactly the cancellations in [A2:195–206](overleaf/slot/appendix/A2_beliefs_trading.tex:195). Research adds
\[
\hat\lambda=\min\{\bar\lambda,V/a\},
\qquad
V=\pi\max_qU_H(q)+(1-\pi)\max_qU_L(q),
\]
as established at [A5:64–82](overleaf/slot/appendix/A5_research.tex:64).

The delicate converse—constructing valid price beliefs from a reduced solution—also works:

1. Entry cannot lower second-price-auction proceeds, so \(w_L\ge0\).
2. Full liquidity support gives \(0<\mu(x)<1\). Hence
   \[
   w(\mu(x))=w_L+\Delta\mu(x)>0.
   \]
3. Distinct posteriors have strictly ordered prices. At a shared posterior, prices agree **exactly when entry probabilities agree**. Therefore
   \[
   P(x)=P(y)
   \quad\Longleftrightarrow\quad
   \bigl(\mu(x),e(x)\bigr)=\bigl(\mu(y),e(y)\bigr).
   \]
4. This price partition is unchanged when auction levels change while \((\Delta,\tau)\) stays fixed. Defining
   \[
   P(x)=t_0+e(x)[w_L+\Delta\mu(x)],
   \qquad
   \zeta(P(x))=\frac{e(x)-\rho}{1-\rho}
   \]
   therefore produces a well-defined preparation strategy and the correct price posterior.

The supporting steps are [A2:57–61](overleaf/slot/appendix/A2_beliefs_trading.tex:57), [A2:145–162](overleaf/slot/appendix/A2_beliefs_trading.tex:145), and the proceeds inequality at [sections/03:15–17](overleaf/slot/sections/03_competition_information.tex:15).

Under CM, two orders can share posterior \(\tau\) and have different entry probabilities. They then have different prices, each revealing the same posterior. A reachable threshold lies in \((0,1)\), so \(w(\tau)>0\) is automatic. Neither \(w_L>0\) nor an additional restriction on \(w(\tau)\) is needed.

The auction-object uses outside the two reduced scalars are:

| Use | Location | Effect on the claim |
|---|---|---|
| \(t_0,t_j\) in conditional terminal payoffs and competitive prices | [A2:128–143](overleaf/slot/appendix/A2_beliefs_trading.tex:128); equilibrium tuples at [A3:31–35](overleaf/slot/appendix/A3_proposition2.tex:31), [A4:273–285](overleaf/slot/appendix/A4_coexistence.tex:273) | Determines price levels; cancels from trading incentives. **No break.** |
| \(g_L,\gamma,c_H\) in preparation optimality | [A2:151–154](overleaf/slot/appendix/A2_beliefs_trading.tex:151) | \(B(\mu)-c_H=\gamma(\mu-\tau)\). Only \(\tau\) and the assumed sign \(\gamma>0\) matter. **No break.** |
| \(w_L\ge0\) in price ordering and tuple construction | [A2:156–170](overleaf/slot/appendix/A2_beliefs_trading.tex:156); [A3:66–70](overleaf/slot/appendix/A3_proposition2.tex:66); [A4:244–253](overleaf/slot/appendix/A4_coexistence.tex:244); [A5:150–170](overleaf/slot/appendix/A5_research.tex:150) | Structural sign condition, automatic for this auction. **No break within the model.** |
| \(w(\tau)>0\) when CM assigns different entries at one posterior | [A2:122–123](overleaf/slot/appendix/A2_beliefs_trading.tex:122), [A2:153–162](overleaf/slot/appendix/A2_beliefs_trading.tex:153) | Automatic at a reachable threshold. **No break**, but the equal-posterior shortcut needs correction; see 4. |
| \(B_i\) and class-ranking integrals in comparisons across incumbent laws | [A1:139–158](overleaf/slot/appendix/A1_payoffs.tex:139); [A3:15–20](overleaf/slot/appendix/A3_proposition2.tex:15) | Establish how the reduced coordinates move. **Path conditions, not a failure of pointwise reduction.** |
| Uniform/point-mass formulas and calibrated constants | [A3:183–219](overleaf/slot/appendix/A3_proposition2.tex:183); [A4:15–62](overleaf/slot/appendix/A4_coexistence.tex:15); [A5:291–300](overleaf/slot/appendix/A5_research.tex:291) | Establish monotonicity, roots, and redundant inequalities. **Additional path restrictions.** |
| \(W_H(F)\) | [A3:75–86](overleaf/slot/appendix/A3_proposition2.tex:75); [A5:280–282](overleaf/slot/appendix/A5_research.tex:280) | Required for ownership. **Ownership lies outside the reduced outcome set.** |
| \(t_L-t_0\) in the value of price access | [A5:410–417](overleaf/slot/appendix/A5_research.tex:410) | Required for the magnitude of expected-proceeds gains. **Outside the reduced outcome set.** |
| \(g_j,c_H,pF(p)\) in allocation surplus | [A5:418–421](overleaf/slot/appendix/A5_research.tex:418) | Required for welfare magnitudes. **Outside the reduced outcome set.** |
| Research cost and cap | [A5:7–20](overleaf/slot/appendix/A5_research.tex:7) | Nonauction primitives that must also be fixed. **Omitting them would make the research version false.** |

The threshold endpoints cause no failure: if \(\tau\le0\), high-cost preparation occurs after every order; if \(\tau\ge1\), it occurs after none. Full support excludes posteriors exactly zero or one, so neither endpoint creates a challenger tie.

**3. Verdicts on (a)–(g)**

**(a) Proved on the stated positive-gap, nonnegative-threshold domain. \(J\) has no general monotonicity.**

Let \(D(y)=G_L(y)-G_H(y)\ge0\). Under the class ranking,

\[
\Delta(F)=\int_p^\infty[1-F(y)]D(y)\,dy,\qquad
\gamma(F)=\int_p^\infty F(y)D(y)\,dy.
\]

Thus FOSD strengthening raises \(\Delta\), lowers each \(g_j\), and lowers \(\gamma\). Their sum is the fixed class-value gap. These are the identities proved at [A1:130–158](overleaf/slot/appendix/A1_payoffs.tex:130).

If \(\gamma>0\) throughout and \(c_H\ge g_L\), the numerator of
\[
\tau=\frac{c_H-g_L}{\gamma}
\]
is nonnegative and nondecreasing while its positive denominator is nonincreasing. Hence \(\tau\), and therefore \(\Delta\tau\), are nondecreasing. Strict FOSD does not guarantee strict changes; the relevant integral must be positive.

A concrete decrease in \(J\): take \(h=10,\ell=1,p=1/2,c_H=2\) and
\[
R_z\sim U[z-0.1,z+0.1],\qquad z\in[7,7.5].
\]
Every incumbent lies between \(\ell\) and \(h\), so exactly
\[
\Delta=z-1,\quad g_L=0,\quad g_H=10-z,\quad
\tau=\frac2{10-z}.
\]
Consequently
\[
J(7)=2,\qquad J(7.5)=1.3,
\]
despite FOSD strengthening and \(1/2<\tau<1\). The benchmark supplies the opposite sign, established in [A4:24–48](overleaf/slot/appendix/A4_coexistence.tex:24). Thus neither sign is general.

**(b) Proved, including uniqueness and the equality boundaries under IM/C1.**

At any admissible auction point,

\[
\boxed{
N\text{ and an informative equilibrium coexist}
\iff
J\ge k,\quad
\pi<\tau\le M(\pi),\quad
\rho\Delta\max\{\pi,1-\pi\}\le k.
}
\]

The distribution-free argument is:

- Under the no-trade inequality, the low class’s unique equilibrium sale rate is zero.
- A positive high-class purchase with entry \(\rho\) earns strictly less than its return at zero purchase rate, which is already at most \(k\).
- An informative equilibrium must therefore recruit after buying. Recruitment is feasible exactly when \(\tau\le M(\pi)\); its maximum gross return among recruiting purchase rates is \(J\).
- Above the recruitment threshold the purchase return decreases strictly with its rate. This gives exactly one recruiting mixed/full purchase outcome.

These are the actual steps at [A4:477–499](overleaf/slot/appendix/A4_coexistence.tex:477). No uniform distribution is used.

Writing \(s=\lambda\sigma_H(1)\), the unique informative rate is
\[
s=\min\left\{\lambda,\,
\frac b\pi\left[\frac{(1-\pi)\Delta}{k}-1\right]\right\}.
\]
Only purchases recruit, giving exactly
\[
\boxed{
\mathsf E
=\rho+(1-\rho)
\min\left\{\frac{(1-\pi)b\Delta}{k},\,b+\pi\lambda\right\}.
}
\]
This is nondecreasing in \(\Delta\), strictly increasing before saturation. The derivation appears at [A4:525–528](overleaf/slot/appendix/A4_coexistence.tex:525).

**(c) The interval claim is proved. Closed endpoints and the full benchmark ordering need further conditions.**

Along FOSD strengthening:

\[
\{\pi<\tau\}=\{B_{F_s}(\pi)<c_H\}
\]
is an up-set, while
\[
\{\tau\le M(\pi)\}=\{B_{F_s}(M(\pi))\ge c_H\}
\]
and the no-trade inequality define down-sets. Therefore, if \(\{J\ge k\}\) is an up-set, their intersection is an interval, possibly empty or a singleton. This uses [A1:147–158](overleaf/slot/appendix/A1_payoffs.tex:147) and the pointwise criterion above.

At prior \(1/2\), with continuous reduced coordinates and attained cutoff boundaries,

\[
C(1/2)
=
[s_A,\min\{s_N,s_C\}]
\cap\{\tau>1/2\},
\]
intersected with the path’s domain. Without continuity/attainment, replace the closed-cutoff notation by the defining inequalities.

A convenient sufficient set recovering the complete benchmark ordering and IM/C1 table is:

\[
\begin{gathered}
\Delta,\ J,\ \tau \text{ continuous and strictly increasing on }[s_0,s_2],\\
\Delta>0,\quad \gamma>0,\quad \tau(s_0)>1/2,\\
J(s_0)<k,\qquad
\rho(1-M)\Delta(s_1)>k,\\
\tau(s_1)<M<\tau(s_2),\qquad M<1-\rho/2.
\end{gathered}
\]

Define \(s_A,s_F,s_N,s_J,s_S,s_C\) by the same scalar equations as in [A4:65–83](overleaf/slot/appendix/A4_coexistence.tex:65). These conditions imply

\[
s_0<s_A<s_F<s_N<s_J<s_S<s_1<s_C<s_2.
\]

In particular, \(s_F<s_N\) requires precisely \(M<1-\rho/2\); the benchmark obtains it from \(\tau(r_2)<3/4\) and \(\rho=1/4\). The consecutive comparisons are displayed at [A4:92–103](overleaf/slot/appendix/A4_coexistence.tex:92).

Global strict monotonicity can be weakened to the corresponding single-crossing sign patterns. For the **additional CM claim that T-entry decreases**, one also needs
\[
\frac{k-\rho J(s)}{\Delta(s)[1-\tau(s)]^2}
\]
to decrease. The paper proves this using increasing \(J\) and increasing \(\Delta(1-\tau)^2\); that extra condition is not needed for the IM/C1 table. See [A4:378–391](overleaf/slot/appendix/A4_coexistence.tex:378).

**(d) Proved, including \(\tau\ge1\).**

If \(\rho\Delta/2\le k\), N exists because \(\tau>1/2\).

Otherwise the low class has the unique positive rate
\[
t=\min\{\lambda,\ b(\rho\Delta/k-2)\}.
\]
At prior \(1/2\),
\[
1-\mu_+(t)=\mu_-(t).
\]

If buying at rate \(t\) does not recruit, choosing \(s=t\) gives the floor-entry Q/full-order equilibrium. If it recruits, its return at \(t\) is at least the low-class return, and the recruiting purchase return decreases continuously thereafter: it either reaches \(k\) before \(\lambda\), giving R, or remains at least \(k\) at \(\lambda\), giving F. In each case \(s\ge t\), so the product lemma applies. The ingredients are [A4:140–147](overleaf/slot/appendix/A4_coexistence.tex:140), [A4:193–255](overleaf/slot/appendix/A4_coexistence.tex:193).

For \(\tau\ge1\), high-cost preparation is impossible because all posteriors are below one. The explicit equilibrium is

\[
s=t=\min\{\lambda,\ b(\rho\Delta/k-2)\},\qquad e\equiv\rho.
\]

Thus existence remains valid; only the recruitment-threshold formula \(s^*\), explicitly introduced for \(\tau<1\), must be omitted. See [A4:149–157](overleaf/slot/appendix/A4_coexistence.tex:149).

**(e) The four prior cases need crossing conditions; several listed assumptions are stronger than necessary.**

The proof’s uses are concentrated at [A4:465–521](overleaf/slot/appendix/A4_coexistence.tex:465).

| Proposed condition | Exact role |
|---|---|
| \(J\) strictly increasing | Sufficient, not necessary. What is needed is an attained start \(J(s_A)=k\) and \(\{J\ge k\}=[s_A,s_2]\). |
| \(\tau\) strictly increasing | Sufficient for unique \(s_\pi\), the singleton in case (a), and the stated threshold endpoints. Global strictness can be replaced by the required level-crossing properties. A plateau at \(\tau_A\) can destroy case (a)’s singleton. |
| \(\Delta\tau\) strictly increasing | Gives a unique \(s_*\) and the cutoff \(\pi_{\max}=\tau(s_*)\). It is **redundant** if \(\Delta>0\) is nondecreasing and \(\tau>0\) is strictly increasing. |
| \(\tau_A<1-\rho\) | A sufficient uniform start-feasibility condition, not necessary for a fixed slot. |
| Continuity | Ensures attained roots, closed upper endpoints, and nondegenerate intervals after strict inequalities. It can be replaced by these properties directly; monotonicity alone does not supply them. |

For a fixed slot, let
\[
\pi_{\rm lo}=M^{-1}(\tau_A).
\]
The sharper start conditions supporting the four cases are

\[
\boxed{
\rho\max\{\pi_{\rm lo},1-\pi_{\rm lo}\}\le1-\tau_A,
\qquad
\rho\tau_A<1-\tau_A.
}
\]

The first makes N feasible at the claimed singleton start. The second gives strict feasibility at \(\pi=\tau_A\) and a nonempty higher-prior window. Convexity of \(\max\{\pi,1-\pi\}\) then gives strict start feasibility for every \(\pi\in(\pi_{\rm lo},\tau_A)\).

For one prior, the corresponding nondegenerate-start condition is simply
\[
\rho\max\{\pi,1-\pi\}<1-\tau_A.
\]

To retain the paper’s \(\pi_{\max}\) formula, also require \(\tau_A\ge1/2\) and an attained interior crossing
\[
\rho\Delta(s_A)\tau_A<k<
\rho\Delta(s_2)\tau(s_2).
\]
Below the even-prior region, the binding no-trade expression is instead \(\rho\Delta\max\{\tau,1-\tau\}\).

**(f) Partly proved; ownership growth and the proposed cap endpoint are false without additional conditions.**

For prior \(1/2\),
\[
m_\lambda=\frac{\beta(1-\lambda)}{2\beta+(1-2\beta)\lambda},
\qquad
m_\lambda'=-\frac{\beta}{[2\beta+(1-2\beta)\lambda]^2}<0.
\]
The root
\[
2a\lambda_R=\Delta m_{\lambda_R}-k
\]
exists uniquely for \(\Delta>2k\), and
\[
\boxed{
\frac{d\lambda_R}{d\Delta}
=\frac{m_{\lambda_R}}{2a-\Delta m_{\lambda_R}'}>0.
}
\]
Thus the root is a smooth, strictly increasing function of \(\Delta\). This generalizes the implicit-function calculation at [A5:266–276](overleaf/slot/appendix/A5_research.tex:266).

Where this branch is an equilibrium,
\[
\mathsf E_R=\rho+(1-\rho)[\beta+(1/2-\beta)\lambda_R]
\]
increases with \(\Delta\) for every \(\beta<1/2\).

Ownership is instead
\[
\boxed{
\mathsf O_H(F)
=\frac12W_H(F)
\left[\rho+(1-\rho)\{\beta+(1-\beta)\lambda_R\}\right].
}
\]
The manuscript removes \(W_H\) because \(h>r\) in its benchmark, explicitly at [A5:280–282](overleaf/slot/appendix/A5_research.tex:280). For two strengths, ownership rises exactly when the product in this display rises. For a differentiable path with \(W_H>0\), the condition is
\[
\frac{W_H'}{W_H}>
-\frac{(1-\rho)(1-\beta)\lambda_R'}
{\rho+(1-\rho)[\beta+(1-\beta)\lambda_R]}.
\]

A valid research-branch counterexample to unconditional ownership growth uses
\[
h=10,\ \ell=1,\ p=\tfrac12,\quad
R\sim U[0,r],\quad
c_H=2.5,\ \rho=.05,\ k=.2,\ \beta=.2,\ a=5,\ \bar\lambda=.9.
\]

| \(r\) | \(\Delta\) | \(\tau\) | \(\lambda_R\) | Entry | \(W_H\) | High-class ownership |
|---:|---:|---:|---:|---:|---:|---:|
| 11 | 4.500 | 0.547980 | 0.139940 | 0.279883 | \(10/11\) | 0.157434 |
| 12 | 4.875 | 0.598485 | 0.149383 | 0.282574 | \(10/12\) | 0.147305 |

Both points—and the intervening path—satisfy the recruiting R conditions. Research and entry rise; ownership falls.

For the branch domain, the maximal positive, interior, recruiting R tuple under C1 satisfies

\[
\boxed{
\frac12<\tau<1,\qquad
\varphi_a=J-k-2a\lambda_E\ge0,\qquad
\lambda_R<\bar\lambda,\qquad
\rho\Delta\le2k.
}
\]

The manuscript’s middle lemma uses strict \(\rho\Delta<2k\) to make every trading choice strict; the R tuple itself survives equality because low-class abstention remains optimal. See [A5:122–162](overleaf/slot/appendix/A5_research.tex:122).

Therefore:

- A continuous branch starting through recruitment equality solves \(\varphi_a=0\). A unique start requires an appropriate negative-to-positive single crossing.
- Every R point has \(J\ge k+2a\lambda_E>k\). Thus \(s_R\ge s_A\) when \(s_A\) denotes the first point with \(J\ge k\); with distinct attained crossings, \(s_R>s_A\).
- Single crossing does **not** ensure that R reaches the research cap before low-class selling becomes profitable.

The two relevant spread thresholds are
\[
\Delta_{\rm cap}=\frac{2a\bar\lambda+k}{m_{\bar\lambda}},
\qquad
\Delta_N=\frac{2k}{\rho}.
\]
For a continuous strictly increasing spread path with both crossings,
\[
\boxed{
s_{\rm cap}\le s_N
\iff
\rho(2a\bar\lambda+k)\le2k\,m_{\bar\lambda}.
}
\]

If \(s_{\rm cap}\le s_N\), the interior branch ends exclusively at the cap. If \(s_N<s_{\rm cap}\), it can end **inclusively** at \(s_N\). The benchmark separately verifies the first ordering at [A5:299–314](overleaf/slot/appendix/A5_research.tex:299).

A counterexample retaining point masses and a uniform incumbent is
\[
h=10,\ell=1,p=.5,\ c_H=4.5,\ k=.5,\rho=.5,\beta=.2,\ a=.01,\bar\lambda=.4,
\quad r\in[4,7.3].
\]
Here \(\varphi_a\) has one negative-to-positive crossing: \(\varphi_a(4)<0\), \(\varphi_a(5)>0\), its derivative exceeds \(0.09\) on \([4,5]\), and it remains positive on \([5,7.3]\). Nevertheless,
\[
m_{\bar\lambda}=0.1875,\qquad
\Delta_N=2,\qquad
\Delta_{\rm cap}=2.709333,
\]
so
\[
r_N=5.828427<r_{\rm cap}=7.281329.
\]
R is an equilibrium at \(r=5\) and at \(r_N\), but cannot continue as the low-class-abstention branch beyond \(r_N\). This disproves the proposed cap ordering and half-open interval under single crossing alone.

For generalizing Proposition A.2, at intermediate points satisfying \(1/2<\tau_i<1\) and \(\rho\Delta_i<2k\), strict recruiting interior research at every point is equivalent to
\[
a>0,\qquad
\max_i\frac{\Delta_i m_{\bar\lambda}-k}{2\bar\lambda}
<a<
\min_i\frac{J_i-k}{2\lambda_{E,i}}.
\]
The benchmark collapses these extrema to the last and first intermediate points using additional monotonicity bounds. Its strong-endpoint uniqueness also needs justification: U is sufficient, and the benchmark proves U automatically within its numerical window at [A5:344–353](overleaf/slot/appendix/A5_research.tex:344).

Finally, the generalized price-access formulas are
\[
\Delta\mathcal R
=(1-\rho)(\bar b+\bar\lambda/2)
[w_L+\Delta M_{\bar\lambda}],
\]
\[
\Delta\mathcal W
=(1-\rho)(\bar b+\bar\lambda/2)
[\gamma(M_{\bar\lambda}-\tau)+pF(p)].
\]
These explain exactly why proceeds and welfare magnitudes require more than \((\Delta,\tau)\), despite the equilibrium reduction. They generalize [A5:417–421](overleaf/slot/appendix/A5_research.tex:417).

**(g) Proposition 2 is already general; Proposition A.1 is calibration-only.**

There is no hidden point-mass or uniform restriction in Proposition 2’s equilibrium proof. Its ownership qualification is also already correct.

For a general three-point comparison with positive gaps, prior \(1/2\), and the maintained FOSD ordering, the H1–H3 slot region is obtained from
\[
\tau_0>1/2,\qquad \Delta_0<k,\qquad
\tau_1<M<
\min\left\{\tau_2,\ 1-\frac{k}{\rho\Delta_1}\right\}.
\]
The benchmark’s \(\tau_2<1-k/(\rho\Delta_1)\) makes the trading bound redundant. At a general prior, the separate restrictions
\[
\pi<\tau_0,\qquad
\tau_1<M(\pi)<\tau_2,\qquad
\kappa(\pi)>\frac{k}{\rho\Delta_1}
\]
must all be retained. The benchmark-specific redundancy checks are at [A3:190–219](overleaf/slot/appendix/A3_proposition2.tex:190).

**4. Other errors or overclaims**

1. **The constructed-tuple shortcut needs an equal-entry qualification under CM.**
   [A2:165–170](overleaf/slot/appendix/A2_beliefs_trading.tex:165) says equal posteriors give equal prices. For general CM equilibria, the correct assertion is: **equal posteriors and equal entry give equal prices**.

   An actual equilibrium counterexample uses
   \[
   h=10,\ell=1,p=.5,\quad F=U[0,2],\quad
   \pi=.5,\rho=.25,k=.2,c_H=73/16,
   \]
   with any admissible slot. Let both informed classes abstain. Every posterior equals \(\pi=\tau=.5\). CM permits
   \[
   e(1)=1,\qquad e(0)=e(-1)=1/4.
   \]
   Then
   \[
   P(1)=15/16,\qquad P(0)=P(-1)=33/64.
   \]
   The high-class purchase gross return is \(1/8<k\), and the low-class sale gross return is \(1/32<k\), so abstention is optimal. This satisfies the equilibrium conditions.

   This shortcut error does **not** invalidate the listed A4/A5 equilibria: their constructions establish equal entry whenever posteriors coincide; see [A4:244–250](overleaf/slot/appendix/A4_coexistence.tex:244).

2. **The coexistence caption needs its C1 endpoint exception.**
   [sections/04:302–303](overleaf/slot/sections/04_equilibrium_results.tex:302) describes T as an equilibrium only under CM. Its \(r_A\) endpoint, with entry one after a purchase, also exists under C1, as the table and proof explicitly state at [A4:297](overleaf/slot/appendix/A4_coexistence.tex:297) and [A4:335–337](overleaf/slot/appendix/A4_coexistence.tex:335). The “CM only” qualification applies to \((r_A,r_J]\).

No substantive contradiction was found in the scoped benchmark propositions. I independently rederived the two derivative polynomials in the path lemma and verified their positivity over the stated intervals using exact Bernstein coefficients. The review used source reading, derivations, and arithmetic evaluations; no repository files were changed and no tests were created or run.
