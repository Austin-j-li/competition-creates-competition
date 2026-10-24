# XP1: independent check of the core proofs

Date: 23 October 2026. Scope: R2, R3 and R4.

## 1. Verdicts

**The core theorems hold. The package needs corrections before its certificates and summary tables can support the manuscript.**

| Item | Verdict | Status | Result |
|---|---|---|---|
| 1. Equilibrium and tie rules | confirmed, with clarification | analytical | The tuple is complete. IM is the usual mixed best-response condition. Adopt IM with the stated C1 convention. |
| 2. Posterior bounds and the ceiling | confirmed | analytical | The bound at zero needs β ≤ 1/3. Proposition 2 does not need this bound. |
| 3. Lemmas 2–3 and Proposition 2 | corrected | analytical | All economic conclusions hold. Correct one flow mass, the stated lemma premises, and one proof dependency. |
| 4. Proposition 3 | corrected | computer-assisted | The main correspondence is complete. Correct the summary row and qualify the entry formula at the CM ceiling. |
| 5. Propositions 4–5 | corrected | computer-assisted | Their main statements hold. The CM paragraph omits coexistence at π = πmax. |
| 6. Numbers and margins | corrected | computer-assisted | All 125 displays agree. Fifty-five printed enclosures exclude their values. Six further brackets move endpoints inward. |
| 7. BRIEF §5 | corrected | analytical | The proof method works after the local repairs below. The original interval text does not meet the certificate standard. |

The checked files stay unchanged. No test suite ran. The calculations use the actual primitives through independent scripts.
The scripts import no checked module. No outside source enters this memo.

### Evidence and scope

I read the named proof, memo, registry, scripts, and their saved logs.
I also read the relevant earlier memos and the pinned `main.tex` at commit `01bd5d6`.
The pinned auction formulas agree with TEAM_RULES §3 and P1 §1.1.
The timing agrees: the challenger initially knows neither its class nor its value. Preparation reveals its value.

The independent evidence is in `scripts/XP1/`:

- `xp1_numbers.py`, `xp1_numbers.log`, and `xp1_registry_recompute.csv`: all 125 registry rows, with exact rational endpoints.
- `xp1_signs.py` and `xp1_signs.log`: independent polynomial derivatives and Sturm counts.
- `xp1_equilibria.py` and `xp1_equilibria.log`: support enumeration and explicit prices, posteriors, entry, and all six payoffs.
- `xp1_boundary.py` and `xp1_boundary.log`: the omitted CM endpoint and the distinction between profile bounds and equilibrium bounds.
- `checked_sources.sha256`: hashes of the checked package, including the supplied PDF.

The scripts use fractions throughout. They bound e by its series through term 110 and a rational bound on the tail:

\[
S_{110}=\sum_{n=0}^{110}\frac1{n!},\qquad
S_{110}<e<S_{110}+\frac{112}{111\cdot111!}.
\]

Square roots use integer bounds at scale 10⁹⁰. Rational bisection gives root brackets with width below 10⁻⁹⁵.
The CSV records the full rational endpoints. Decimal bounds use a downward lower endpoint and an upward upper endpoint.

## 2. Equilibrium object and the tie rules

### Complete tuple

**Confirmed; analytical.** The definition supplies the required object:

\[
\mathcal E=(\sigma_H,\sigma_L,P,\mu,\zeta,\text{bids}).
\]

It defines both order distributions, all three prices, all three order posteriors, preparation at every attainable price, and truthful bids.
Condition E2 supplies the price posterior by Bayes' rule. It need not be a separate free component of the tuple.
Every order has positive liquidity mass in both classes. Every feasible investor deviation therefore reaches an attainable price.

The auction convention completes the bids: the incumbent bids R; a prepared challenger bids θ when θ ≥ p.
The reserve excludes inadmissible bids. Value ties have probability zero because F is continuous.
The fixed zero-cost preparation rule also covers zero auction rent.

### Four rule pairs

| Pair | Investor at a trade–abstention tie | High-cost challenger at a preparation tie |
|---|---|---|
| IM, C1 | Any mixture over maximizers | Prepare |
| IM, CM | Any mixture over maximizers | Any preparation probability |
| I0, C1 | Abstain | Prepare |
| I0, CM | Abstain | Any preparation probability |

**Confirmed; analytical.** IM is the usual mixed best-response requirement.
It permits a pure maximizer and every mixture over tied maximizers.
I0 adds a restrictive selection rule. It can remove every equilibrium.

The manuscript should use a mixed Bayesian equilibrium with competitive prices and sequentially optimal preparation.
Use IM as its investor condition. State C1 as the baseline preparation convention, as the pinned manuscript does.
State CM when the result concerns the full preparation correspondence.

### Nonexistence under I0

At prior 1/2, a low-class sale has gross return

\[
K_L(t)=\rho\Delta(r)\frac{b}{2b+t},\qquad 0\le t\le\lambda.
\]

This function falls strictly in t. On \((r_N,r_S]\), it satisfies

\[
K_L(0)>k,\qquad K_L(\lambda)\le k.
\]

Abstention fails at t = 0. Full sale fails under I0 at t = λ.
An interior rate requires a trade–abstention mixture, which I0 excludes.
Thus both I0 rule pairs have no equilibrium on this entire interval.
At r = r_N, abstention is allowed. At r = r_S, I0 still excludes full sale.

### Correction to the interpretation of u

**Refuted as an interpretation; analytical.** The brief and P1 call u the odds that an order in one direction is informed.
That statement does not hold for arbitrary strategies.
Under full orders, the informed-to-liquidity odds conditional on a purchase are πu. Conditional on a sale, they are \((1-\pi)u\).
At prior 1/2, both odds equal u/2.

The correct definition remains \(u=\lambda/b\).
Describe it as the informed presence mass relative to the liquidity mass in one direction.
It sets the maximum likelihood ratio, \(1+u\). Every proof uses this correct ratio.

## 3. Lemma 1, Corollary 1, and β above one third

### Bounds under every strategy

**Confirmed; analytical.** For an order x with liquidity mass \(b_x\), Bayes' rule gives

\[
\frac{\mu(x)}{1-\mu(x)}
=\frac{\pi}{1-\pi}
 \frac{b_x+\lambda\sigma_H(x)}{b_x+\lambda\sigma_L(x)}.
\]

Since each strategy probability lies in [0,1],

\[
\frac1{1+\lambda/b_x}
\le\frac{a_H(x)}{a_L(x)}\le1+\frac\lambda{b_x}.
\]

At ±1, \(b_x=b\), so the bounds are exactly \(m(\pi)\) and \(M(\pi)\).
At zero, \(b_x=b_0\). The same bounds apply precisely when

\[
b_0\ge b
\iff 1-2\beta\ge\beta
\iff\beta\le\frac13.
\]

The package's counterexample is correct: λ = 6/17 and β = 2/5 give \(\mu_0=41/52>M=26/37\).
The lower zero-order bound fails by the reverse choice of strategies.

### Corollary 1

**Confirmed; analytical.** If β ≤ 1/3, every order posterior lies below M.
Every price posterior is a weighted average of those order posteriors.
Thus \(B(M)<c_H\) excludes optimal high-cost preparation after every price, under every strategy profile.
Here “under every profile” retains Bayes consistency and optimal preparation. It does not describe an arbitrary irrational preparation rule.

The corollary fails above one third. An independent exact example uses

\[
\beta=\frac25,\quad u=\frac85,\quad
\lambda=\frac{16}{41},\quad b=\frac{10}{41},\quad b_0=\frac5{41},\quad M=\frac{13}{18}.
\]

Let H abstain and L sell fully. The zero-order posterior is 21/26.
At r = 18/5,

\[
6-B_r(M)=\frac{479}{6480}>0,\qquad
B_r(21/26)-6=\frac{1919}{3120}>0.
\]

This profile admits high-cost preparation after zero. It fails investor optimality.

### Proposition 2(iii)

**Confirmed for every β < 1/2; analytical.** Its uniqueness proof first forces full orders under every candidate profile:

\[
K_H\ge\rho\Delta_2[1-M]\ge\rho\kappa\Delta_1>k,
\qquad
K_L\ge\rho\Delta_2m\ge\rho\kappa\Delta_1>k.
\]

These bounds use only the posteriors at ±1 and the entry floor.
Every equilibrium therefore has \((\sigma_H,\sigma_L)=(\delta_1,\delta_{-1})\).
Only then does the proof use its posteriors, \((m,\pi,M)\).
All three fall below the preparation threshold under H3.

At calibration B, the strict trading margin at r₂ is 0.043126528071568299… .
The strict preparation margin is 0.002688902265905112… .
At fixed u = e − 1, both margins remain the same when β varies in (1/3,1/2).
The unique equilibrium therefore persists throughout that range.

This argument also explains Propositions 3–5 above one third.
At prior 1/2, their equilibrium rates satisfy s ≥ t, so \(\mu_0\le\pi<\tau\).
In a coexistence economy at another prior, the low class abstains, so t = 0 ≤ s.
Neither proof needs an all-profile bound at zero.

## 4. Lemmas 2–3 and Proposition 2

### Price sufficiency

**Confirmed; analytical.** Fix a candidate object that satisfies Bayes consistency, optimal preparation, and competitive prices.
Its price satisfies

\[
P(x)=t_0+e(x)[t_L-t_0+\Delta\mu(x)].
\]

If two orders share a price, the challenger uses the same preparation probability at that price.
Their entry probabilities therefore coincide. The price equations then imply

\[
e\Delta[\mu(x)-\mu(x')]=0.
\]

Since e ≥ ρ > 0 and Δ > 0, their posteriors coincide.
Thus the challenger recovers the order posterior from the price.
This proof does not assume that the price already reveals the posterior.

For \(\mu_2>\mu_1\), optimal preparation gives \(e_2\ge e_1\), and

\[
P_2-P_1
=e_2\Delta(\mu_2-\mu_1)
 +(e_2-e_1)[t_L-t_0+\Delta\mu_1]
\ge\rho\Delta(\mu_2-\mu_1)>0.
\]

This direct algebra also verifies price sufficiency for a constructed tuple.
It avoids an implication in the wrong direction in the product lemma at P1 lines 653–655.
That passage invokes Lemma 2, whose premises include E2–E4, while it seeks to establish those conditions.
Use the displayed algebra first. Then compute the price posterior and verify preparation.
The repair is local; it adds no assumption.

### Investor payoffs and lemma premises

**Confirmed, with a premise correction; analytical.** Hold the candidate's price and entry functions fixed throughout a deviation.
Direct subtraction gives

\[
\begin{array}{c|ccc}
 & -1&0&1\\\hline
H&-e_-\Delta(1-\mu_-)-k&0&e_+\Delta(1-\mu_+)-k\\
L&e_-\Delta\mu_--k&0&-e_+\Delta\mu_+-k
\end{array}
\]

Wrong-sign orders lose at least k. Each class therefore compares one correct order with abstention.
The zero-order entry decision affects neither correct-order return.

Lemma 3's opening sentence mentions E4 alone. Its all-profile bounds also require E1 and the imposed entry floor.
State those premises explicitly: Bayes posteriors, competitive prices, \(e\in[\rho,1]\), and \(\Delta\ge0\).
These premises already hold for every tuple to which Proposition 2 applies.

### H1–H3 and every conclusion

**Confirmed; analytical.** The hypotheses are sufficient:

\[
\begin{split}
&B_0(\pi)<c_H<B_1(M),\\
&\Delta_0<k<\rho\min\{m,1-M\}\Delta_1,\\
&B_2(M)<c_H.
\end{split}
\]

The auction comparison gives \(B_1(\pi)\le B_0(\pi)<c_H\) and \(\Delta_2\ge\Delta_1\).
The first inequality stops preparation at the prior in economy 1.
The second extends the strict trading bound to economy 2.

| Economy | Bound for every candidate | Forced orders | Posteriors | Entry after (−1,0,1) |
|---|---|---|---|---|
| F₀ | Correct net return ≤ Δ₀ − k < 0 | Both abstain | (π,π,π) | (ρ,ρ,ρ) |
| F₁ | Correct net return ≥ ρκΔ₁ − k > 0 | H buys; L sells | (m,π,M) | (ρ,ρ,1) |
| F₂ | Correct net return ≥ ρκΔ₂ − k > 0 | H buys; L sells | (m,π,M) | (ρ,ρ,ρ) |

For each row, set \(P(x)=t_0+e(x)[t_L-t_0+\Delta_i\mu(x)]\).
Set \(\zeta(P(x))=(e(x)-\rho)/(1-\rho)\), and use the truthful bids above.
The displayed flow probabilities give Bayes consistency.
The strict preparation inequalities give optimal entry. The price formula gives competitive prices.
The bounds in the table give investor optimality against this fixed tuple.
They also force every equilibrium to use that tuple.

No investor or high-cost preparation tie occurs in these three economies.
All four rule pairs therefore give the same unique outcome.

### Flow correction

**Corrected; analytical.** P1 line 356 omits informed abstention from the zero-order mass in economy 0.
The correct expression is

\[
a_H(x)=a_L(x)=(1-\lambda)\eta(x)+\lambda\mathbf1\{x=0\}.
\]

The two class masses remain equal. Every posterior still equals π.
Thus this slip changes no equilibrium, price, or entry value.

### Ownership

**Confirmed; analytical.** Under full orders,

\[
e_H=\rho+(1-\rho)(b+\lambda),\qquad
e_L=\rho+(1-\rho)b,
\]
\[
\mathsf E_1=\rho+(1-\rho)(b+\pi\lambda),\qquad
\mathsf O_{H,1}=\pi e_HW_H(F_1).
\]

Conditional on the class, the order and preparation cost are independent of θ and R.
Thus the win probability factors as stated. Ownership rises exactly when

\[
[\rho+(1-\rho)(b+\lambda)]W_H(F_1)>\rho W_H(F_0).
\]

The extra condition \(b+\lambda>1/2\) correctly transfers the pinned manuscript's sufficient ownership condition.
In the benchmark, \(W_H=1\), so ownership rises to 0.324401303410788560… .

The example with \(c_H=47/10\) is correct.
It gives \(c_H-B_0(1/2)=-5/48\), entry 1 at r₀, and entry 0.522757 at r₁.
Thus \(B_1(\pi)<c_H\) cannot replace the weak-economy condition.

## 5. Proposition 3: complete correspondence

### Independent reduction

**Confirmed; analytical.** Wrong-sign orders never occur. Set \(s=\lambda\sigma_H(1)\) and \(t=\lambda\sigma_L(-1)\).
The flow law is

\[
a_H=(b,b_0+\lambda-s,b+s),\qquad
a_L=(b+t,b_0+\lambda-t,b).
\]

At prior 1/2, the correct-order gross returns are

\[
K_H=e_+\Delta\frac b{2b+s},\qquad
K_L=\rho\Delta\frac b{2b+t}.
\]

The sale posterior never exceeds 1/2, while τ > 1/2 throughout the path.
Thus high-cost preparation never follows a sale.
Each return falls strictly with its rate on each fixed entry piece.
The only supports are zero, full, one interior root on each entry piece, and the preparation threshold.
This list includes simultaneous mixtures by both classes.

The unique low-class rate under IM is

\[
t(r)=\begin{cases}
0,&r\le r_N,\\
b[\rho\Delta(r)/k-2],&r_N<r<r_S,\\
\lambda,&r\ge r_S.
\end{cases}
\]

The possible high-class rates are

\[
\begin{array}{c|cc}
\text{form}&s&e_+\\\hline
N&0&\rho\\
R&b[\Delta/k-2]&1\\
F&\lambda&1\text{ below the ceiling; }\rho\text{ above it}\\
Q&b[\rho\Delta/k-2]&\rho\\
T&b(2\tau-1)/(1-\tau)&k/J
\end{array}
\]

Every admissible pair satisfies s ≥ t.
For N and R, t = 0. For F, s = λ ≥ t. For Q, s = t.
For T, the inequality s ≥ t is equivalent to \(\rho J\le k\), its own feasibility condition.
Consequently \(\mu_0\le1/2<\tau\), even when β > 1/3.

These facts exclude extra equilibria from zero-order preparation.
They also exclude high-class sales and every additional threshold support.

### Thresholds and their order

**Confirmed; computer-assisted.** The definitions and values are:

| Threshold | Equation | Value at B |
|---|---|---|
| r_A | J = k | 1.393957920279251333… |
| r_F | Δ(1 − M) = k | 1.467127041293093799… |
| r_N | ρΔ/2 = k | 1.747877538267962744… |
| r_J | ρJ = k | 1.966097064963998870… |
| r_S | ρΔm = k | 2.124148132815450674… |
| r_C | τ = M | 3.592658518794661833… |

For every slot in the stated band,

\[
r_0<r_A<r_F<r_N<r_J<r_S<r_1<r_C<r_2.
\]

The independent derivatives reproduce both printed polynomials.
For J′, the Sturm variations are 3 at both path endpoints. Its numerator is positive at r₀.
For \([\Delta(1-\tau)^2]'\), the variations are 5 at r₀ and at 2. Its numerator is positive at r₀.
Both root counts are zero. The denominators are positive on the required intervals.

The derivative of τ has positive numerator proportional to \(8r^2-r+2\).
The product Δτ increases because both factors are positive and increase.
These signs supply uniqueness of r_A, r_J, and r_*.

One useful missing displayed step is

\[
\rho J(2)-k=\frac{11}{11200}>0.
\]

It gives r_J < 2 and makes the denominator argument for entry on T explicit.

### Main table under IM, C1

| Strength | Complete equilibrium set |
|---|---|
| [r₀,r_A) | N |
| r_A | N; T with e₊ = 1 |
| (r_A,r_F) | N; R |
| [r_F,r_N] | N; F |
| (r_N,r_J) | F; Q |
| [r_J,r₂] | F |

**Confirmed; computer-assisted.** No additional equilibrium survives the independent support reduction.
Q contains mixtures by both classes. F contains a low-class mixture on \((r_N,r_S)\).
Thus “full purchase” does not mean that both classes use full orders along all of F.

### CM and I0

Under IM, CM adds T on \((r_A,r_J]\).
At r_J it has e₊ = ρ and the same rates as the limit of Q.
C1 excludes that limit because preparation changes at the threshold.
At r_C, CM admits every e₊ in [ρ,1] on F.

Both I0 pairs give:

| Strength | Complete equilibrium set |
|---|---|
| [r₀,r_F] | N |
| (r_F,r_N] | N; F |
| (r_N,r_S] | empty |
| (r_S,r₂] | F |

Under I0, CM still gives the continuum of entry probabilities at r_C.

**Corrected; analytical.** P1 line 910 gives one set on the entire interval \((r_N,r_S]\).
Replace that row with these three rows:

| Strength | IM, C1 | IM, CM | Either I0 pair |
|---|---|---|---|
| (r_N,r_J) | F; Q | F; Q; T | empty |
| r_J | F | F; T | empty |
| (r_J,r_S] | F | F | empty |

### Entry on every branch

**Confirmed, with a CM qualification; analytical.** The branch formulas are

\[
\begin{split}
\mathsf E_N=\mathsf E_Q&=\rho,\\
\mathsf E_R&=\rho+(1-\rho)\frac{b\Delta}{2k},\\
\mathsf E_F&=\rho+(1-\rho)(b+\lambda/2)\quad(r<r_C),\\
\mathsf E_F&=\rho\quad(r>r_C),\\
\mathsf E_T&=\rho+\frac b2\frac{k-\rho J}{\Delta(1-\tau)^2}.
\end{split}
\]

At r_C, C1 gives the upper value. CM gives the full interval

\[
\mathsf E_F(r_C)
=\rho+(e_+-\rho)(b+\lambda/2)
\in[\rho,\mathsf E_1].
\]

P1's displayed formula and its statement about entry “up to r_C” need this qualification under CM.

Entry on R rises strictly and joins F continuously at r_F.
On T, its numerator falls strictly and its positive denominator rises strictly through r_J < 2.
Thus entry on T falls strictly from 0.454184855929613328… to ρ.
At 1.55, 1.60, and 1.65, its values are 0.341462, 0.321311, and 0.305208.
Entry on F is 0.522757 at all three strengths under C1.

### Independent program use

The support calculation covers 5,808 exact rational cases across twelve slots and all four rule pairs.
The slots include β = 1/5, 1/3, 2/5, and 49/100.
It finds zero differences from the corrected piecewise correspondence.
Calibration B adds 484 interval cases and 2,892 cases with other priors. Both calculations find zero differences.

These finite grids carry **numerical diagnostic** status. The analytical support reduction supplies completeness.
The exact sign certificates carry **computer-assisted** status.
An exact ceiling example also verifies all four pairs at r = 31/10, β = 2/5, and u = 239/166.
It retains the full CM interval at the threshold, rather than one chosen entry probability.

## 6. Proposition 4: the admissible region

**Confirmed; analytical.** At prior 1/2, \(m=1-M=1/(2+u)\).
The two slot-independent margins are

\[
c_H-B_0(1/2)=\frac{287}{240}>0,\qquad
k-\Delta_0=\frac1{300}>0.
\]

The other conditions reduce to

\[
\begin{split}
M>\frac{141}{200}&\iff u>\frac{82}{59},\\
M<\frac{4245}{5804}&\iff u<\frac{2686}{1559},\\
\frac{\rho\Delta_1}{2+u}>k&\iff u<\frac{19}{3}.
\end{split}
\]

The upper band limit implies the last condition.
Thus the stated band is necessary and sufficient for H1–H3 at these benchmark strengths.
It also gives the stated failure of recruitment below the lower endpoint and return to full preparation above the upper endpoint.
The exact boundary outcomes depend on C1 versus CM, as P1 states.

| Parameter section | Exact admissible region |
|---|---|
| Slot, prior 1/2 | \(82/59<\lambda/[(1-\lambda)\beta]<2686/1559\) |
| Presence at fixed β | \(82\beta/(59+82\beta)<\lambda<2686\beta/(1559+2686\beta)\) |
| Prior at B, H1–H3 | \(141/(141+59e)<\pi<4245/(4245+1559e)\) |
| Prior at B, H1–H2 | \(141/(141+59e)<\pi<195/308\) |
| Prior at B, strong trading bound alone | \(3e/(22+3e)<\pi<22/(22+3e)\) |

The first prior interval has endpoints 0.467850029686148512… and 0.500424307320063228… .
Their six-place displays are correct. Use approximation signs for decimal endpoint equivalents.
The exact open interval differs slightly from an interval whose endpoints are those rounded decimal strings.

The slot region is open for \(0<\beta<1/2\).
The model restriction β ≤ 1/3 gives a relatively open section of that region.
Treat β ≤ 1/3 as a structural restriction, not as a strict inequality.

## 7. Proposition 5: every prior

### Main result under IM, C1

**Confirmed; computer-assisted.** If π < τ, no trade requires

\[
\rho\Delta\max\{\pi,1-\pi\}\le k.
\]

This condition forces t = 0 in every equilibrium.
For s > 0, an order below the preparation threshold earns less than the no-trade purchase.
Thus an informative equilibrium must reach \(\tau\le\mu_+(s)\le M(\pi)\) and must satisfy \(J(r)\ge k\).
Those conditions are also sufficient: choose F if its return covers k; otherwise choose the unique R or T root.
Its zero posterior lies below π, so the constructed tuple has no extra preparation after zero.

If π ≥ τ, no trade under C1 induces entry 1 after every order.
If it is optimal, then \(\Delta\max\{\pi,1-\pi\}\le k\).
Every positive purchase or sale lowers its own correct-order return below this no-trade bound.
Thus no informative equilibrium coexists with no trade there.

The exact coexistence set is therefore

\[
C_{\mathrm{C1}}(\pi)=
\{r\in[r_0,r_2]:r\ge r_A,\ \pi<\tau(r)\le M(\pi),\
\rho\Delta(r)\max\{\pi,1-\pi\}\le k\}.
\]

The three cut points at B are

\[
\begin{split}
\pi_A^{\rm lo}&=0.396175423610453727\ldots,\\
\tau_A&=0.640739075708409578\ldots,\\
\pi_{\max}&=0.650059160618111936\ldots.
\end{split}
\]

The first depends on u. The last two depend only on the auction and costs.
The four cases in Proposition 5 are correct under IM, C1.
At \(\pi=\pi_A^{\rm lo}\), the set is the singleton \(\{r_A\}\); its informative equilibrium uses a full purchase.
At \(\pi=\tau_A\), the lower strength endpoint r_A is excluded.
At \(\pi=\pi_{\max}\), the set is empty under C1.

The proof uses \(\tau_A<3/4\) to show that no trade remains optimal at r_A for every prior.
The independent margin is 0.109260924291590422… .
For priors above τ_A, the last nonempty interval ends when \(\rho\Delta(r_\pi)\pi=k\).
Its unique boundary is \(r_\pi=r_*\), which gives the stated πmax.

The informative entry formula is correct:

\[
\mathsf E=\rho+(1-\rho)
\min\{(1-\pi)b\Delta/k,\ b+\pi\lambda\}.
\]

It rises during a mixed purchase and stays constant during a full purchase.

### Domain repairs

**Corrected; analytical.** P1 line 816 defines rπ even when π > τ(r₂), where no path root exists.
Define rπ only for π in \([\tau(r_0),\tau(r_2)]\).
Handle π > τ(r₂) directly: no path strength satisfies π < τ(r).
At π = τ(r₀), use rπ = r₀; the strict inequality holds only above it.

Also define rC only when its feasible set is nonempty, or use an empty-set convention.
For small priors, \(M(\pi)<\tau(r_0)\), so a “largest strength” does not exist.
The displayed set formula needs neither undefined object.
The interval cases use both objects only where their required roots or maxima exist.

### Omitted CM endpoint

**Refuted as stated; computer-assisted.** The paragraph at P1 lines 892–895 misses a point outside its case (c).
For IM, CM, the exact correction is

\[
C_{\mathrm{CM}}(\pi)=C_{\mathrm{C1}}(\pi)\ \cup\
\begin{cases}
\{r_\pi\},&\tau_A<\pi\le\pi_{\max},\\
\varnothing,&\text{otherwise}.
\end{cases}
\]

At a prior tie π = τ(r), CM permits the no-trade tuple to use entry ρ.
It is optimal exactly when \(\rho\Delta\max\{\pi,1-\pi\}\le k\).
A positive informative purchase requires \(\Delta(1-\pi)>k\), strictly.
These conditions reduce to \(r_A<r\le r_*\), or \(\tau_A<\pi\le\pi_{\max}\).
The upper endpoint belongs to this set. The lower endpoint does not.

Here is an explicit counterexample to the paragraph's endpoint scope at B:

\[
r=r_*,\qquad\pi=\tau(r_*)=\pi_{\max},\qquad
\rho\Delta(r_*)\pi=k.
\]

The two tuples are:

| Component | No trade | Informative trade |
|---|---|---|
| Orders | \((\delta_0,\delta_0)\) | \((\delta_1,\delta_0)\) |
| Posteriors | (π,π,π) | \((\pi,\mu_0,M(\pi))\) |
| Entry | (ρ,ρ,ρ) | (ρ,ρ,1) |
| Prices | \(t_0+\rho[t_L-t_0+\Delta\pi]\) at all orders | \(t_0+e(x)[t_L-t_0+\Delta\mu(x)]\) |
| Bids | Truthful | Truthful |

For the informative tuple,

\[
\mu_0=\frac{\pi b_0}{\pi b_0+(1-\pi)(b_0+\lambda)}
=0.454139509157646915\ldots<\pi,
\]
\[
M(\pi)=0.834698467246826669\ldots,\qquad
\Delta[1-M(\pi)]-k
\in[0.000342952490169732737184,\ 0.000342952490169732737185].
\]

H strictly buys in the informative tuple. H strictly abstains in the no-trade tuple.
L is indifferent between sale and abstention in both tuples, because \(\rho\Delta\pi=k\).
Both IM and I0 permit its abstention.
CM permits high-cost abstention at the sale posterior π = τ.
Thus coexistence also holds here under I0, CM.

For I0, C1, the package's strict full-purchase condition is correct.
For I0, CM, add the prior-tie endpoints above whenever \(\Delta(r_\pi)[1-M(\pi)]>k\).
The B counterexample satisfies this strict condition.

## 8. Registry, intervals, and margins

### Display precision

**Confirmed; computer-assisted.** All 125 rows agree at the precision of their `display` field.
No row differs beyond its display precision. This includes the rational displays, all margins, and both calibration comparisons.
The full recomputation is `scripts/XP1/xp1_registry_recompute.csv`.

The main margins are:

| Margin | Independent value |
|---|---|
| c_H − B₀(π) | 287/240 = 1.195833333333… |
| B₁(M) − c_H | 0.217154821916707327… |
| k − Δ₀ | 1/300 = 0.003333333333… |
| ρκΔ₁ − k | 0.024823570228332520… |
| c_H − B₂(M) | 0.002688902265905112… |
| M − τ(r₁) | 0.026058578630004879… |
| τ(r₂) − M | 0.000333564719409318… |
| ρκΔ₂ − k | 0.043126528071568299… |

Every displayed value in the full margins table rounds correctly.
The formulas that subtract a rounded band endpoint should instead cite the exact endpoint or its registry key.
This change keeps each margin equal to its stated formula.

### Fifty-five enclosures exclude their values

**Refuted as certificates; computer-assisted.** The following complete list identifies all 55 affected registry rows:

```text
lambda_B, b_B, b0_B, M_half_B, m_half_B,
entry_r1_B, eH_r1_B, eL_r1_B, own_r1_B,
price_r0, price_r1_m1_B, price_r1_0_B, price_r1_p1_B,
price_r2_m1_B, price_r2_0_B, price_r2_p1_B,
margin_recruit_B, margin_kstrong_B, margin_return_B,
margin_return_post_B, margin_recruit_post_B, margin_kstrong2_B,
margin_u_lo_B, margin_u_hi_B, margin_lambda_lo_B, margin_lambda_hi_B,
prior_lo_B, prior_hi_B, prior_kappa_lo_B, prior_kappa_hi_B,
margin_prior_lo_B, margin_prior_hi_B,
rN, rF_B, rS_B, rC_B,
gap_rA_r0_B, gap_rF_rA_B, gap_rN_rF_B, gap_rJ_rN_B,
gap_rS_rJ_B, gap_r1_rS_B, gap_rC_r1_B, gap_r2_rC_B,
entry_mb_r140_B, entry_mb_r145_B,
entry_th_r155_B, entry_th_r160_B, entry_th_r165_B,
b_plus_lambda_B,
nec_margin_recruit_B, nec_margin_kstrong_B, nec_margin_return_B,
margin_kstrong_r2pt0_B, rF_A
```

For example, the registry prints a point interval for λ:

\[
[0.336121768915121197,\ 0.336121768915121197].
\]

The independent outward enclosure is

\[
\lambda_B\in
[0.336121768915121197397183,\ 0.336121768915121197397184].
\]

The published point excludes λ.
The same defect affects even the rational price \(0.3927083333\ldots\), which has no e dependence.

The cause is `ivstr` at `p1_common.py:204–206`.
It uses nearest decimal conversion for both endpoints. `Registry.add_iv` calls that function at line 261.
The saved logs use the same formatter. Their printed decimal intervals require the same repair.
The interval arithmetic inside the program and the decimal serialization are separate issues.

### Six more brackets fail outward serialization

These six broad brackets still contain their true values. Their printed endpoints fail to preserve the original certified brackets:

| Key | Endpoint that moves inward |
|---|---|
| rJ | upper |
| rstar | lower |
| tau_rJ | upper |
| pimax | upper |
| Delta_rA | both |
| entry_rA_B | both |

The script reconstructs the package's width-10⁻¹³ rational brackets independently before this comparison.
`Registry.add_bracket` at lines 263–271 uses nearest binary-float formatting.
The root brackets in `p1_certificates.log` use the same nearest conversion.
Their agreement with a true root does not make the serialization outward.

The remaining broad registry intervals contain their values and preserve their endpoints at the printed precision:
`rA`, `tau_rA`, `piA_hi`, `piA_lo_B`, `margin_piA_lo_B`, and `margin_piA_hi`.
Their formatter still lacks a general outward guarantee.

Use exact rational endpoint strings, or floor the lower decimal and ceil the upper decimal.
Certify each display from those exact endpoints, without an intermediate binary float.
The independent CSV supplies valid replacement enclosures for every row.

### Four gaps are lower bounds, not the stated differences

**Corrected; computer-assisted.** `p1_numbers.py:232–234` substitutes one endpoint of a root bracket into four gaps.
Those calculations give useful positive lower bounds. They do not enclose the actual gaps named by their registry notes.

| Key | Actual gap, outward decimal enclosure |
|---|---|
| gap_rA_r0_B | [0.193957920279251333, 0.193957920279251334] |
| gap_rF_rA_B | [0.073169121013842465, 0.073169121013842466] |
| gap_rJ_rN_B | [0.218219526696036126, 0.218219526696036127] |
| gap_rS_rJ_B | [0.158051067851451803, 0.158051067851451804] |

For each true gap, subtract the whole root interval.
Alternatively, label the existing quantity explicitly as a certified lower bound.
The six-place gap displays and every sign remain correct.

### Status and attribution repairs

The package's interval labels need the corrected serialization before its printed enclosures serve as certificates.
The independent rational calculations certify every display separately.
The proof remains analytical where no finite sign calculation enters it.
The two path signs retain computer-assisted status.

P1's claim about the brief's r_F value is stale.
The current brief already gives r_F,B = 1.467127 and identifies 1.460985 as calibration A.
Thus the mathematical calibration distinction is correct, but the attribution to the current brief is false.
The earlier T2 and X numbers at calibration A remain correct for that calibration.

## 9. BRIEF §5: proof-by-proof assessment

| Result | Object and conditions | Fixed-object verification | Bounds for every profile | Strict margins and evidence |
|---|---|---|---|---|
| Lemma 1 | Explicit flow law | Direct Bayes calculation | Holds for arbitrary class strategies | Exact β condition; correct support domain |
| Lemma 2 | E1–E4 and E6 stated | Equal-price argument is direct | Uses no proposed investor strategy | State Δ > 0 and g_H > g_L explicitly |
| Lemma 3 | Add E1 and the entry floor to its opening premises | All six payoffs hold P and e fixed | ±1 posterior bounds suffice | Δ ≥ 0 is structural; k > 0 excludes wrong signs |
| Corollary 1 | Specify optimal preparation and Bayes beliefs | Direct bound on the price posterior | Yes, including zero when β ≤ 1/3 | Strict B(M) < c_H |
| Proposition 2 | Complete tuples recoverable from Definition 1 | Correct after the zero-mass slip | Yes; forces orders before entry | All five substantive strict margins are positive |
| Path and order lemmas | Explicit equations and domains | Polynomial identities and endpoint signs | Applies throughout the stated band | Independent exact Sturm counts and rational brackets |
| High-class lemma | Five explicit rate–entry pairs | Each case compares the fixed purchase return with k | Zero, full, interior, and threshold exhaust all supports | The strict side conditions and exact tie equalities are stated |
| Low-class lemma | Three explicit rate cases | The sale return falls strictly from its zero-rate value to its full-rate value | Gives one IM rate and the whole I0 gap | The two endpoint inequalities determine every boundary |
| Product lemma | Rates, prices, beliefs, and entry stated | Replace the backwards invocation of Lemma 2 | Necessary class supports are exhaustive | No new primitive restriction |
| Proposition 3 | Complete forms and low-class rate | All six conditions follow after the product repair | Wrong signs and all possible supports excluded | Correct main table; repair the summary and CM endpoint formula |
| Proposition 4 | Exact admissible region stated | Algebraic equivalences | Uses the forced-order bound outside the band | Exact cutoffs; decimal equivalents are approximate |
| Proposition 5 | Complete N, R, T, and F tuples through the product construction | Direct return inequalities | Includes π ≥ τ and all low-class supports | Main C1 set holds; repair root domains and CM endpoint scope |

The price lemma's strict premises hold uniformly on the benchmark path:

\[
\Delta(r)\ge\frac1{60}>0,\qquad
g_H(r)-g_L(r)\ge\frac{1451}{180}>0.
\]

The additional margins for the path argument include

\[
k-J(r_0)=\frac{1283}{92400}>0,\qquad
\frac34-\tau(r_2)=\frac{27}{1451}>0,\qquad
\rho J(2)-k=\frac{11}{11200}>0.
\]

The margins table should add these conditions, or identify them as derived inequalities with a named exact certificate.
It should also record \(3/4-\tau_A>0\) for the general-prior proof.
The primitive domains and the structural weak restrictions should remain separate from the open set of substantive hypotheses.
Exact tie equalities define boundary equilibria. The strict-margin rule must not delete those boundary cases.

## 10. Corrections and remaining work

The main conclusions of Propositions 2–5 are confirmed under their stated baseline rules.
Their economic mechanism and admissible region survive this independent check.
The following repairs remain in the checked package:

1. Correct the interpretation of u in the brief and P1.
2. Add the missing premises to Lemma 3.
3. Correct the no-trade zero-order mass in Proposition 2.
4. Verify the product construction by direct price algebra before it invokes price sufficiency.
5. Split the erroneous summary row on \((r_N,r_S]\).
6. Give the full CM entry interval at r_C in the displayed entry formula.
7. Restrict the domains of rπ and rC in the general-prior section.
8. Add the CM endpoint at π = πmax; distinguish I0, C1 from I0, CM there.
9. Replace the defective interval serialization and the four gap enclosures.
10. Correct the stale attribution of r_F to the current brief.
11. Add the derived strict margins and use exact cutoff symbols in their formulas.

No core theorem remains mathematically open within this scope.
The finite grids do not establish completeness by themselves. The support reduction and exact signs supply that argument.
The checked files need the listed repairs; this memo does not apply them.
