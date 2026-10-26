# W3-research-branch-end: Solver A

## Candidate 1: Continue the recruiting branch through low-class selling

Angle: both

Intuition: A low-class sale need not end the competition-creates-research mechanism. Initially the low class sells only often enough to eliminate its trading profit, so its new sales do not change the research equation at all. If low-class sales eventually become certain, their positive profits add a second return to research and research still rises. The relevant economic branch is therefore “purchases recruit,” allowing the low class's trading strategy to change along it.

**Recommendation.** Use this as the general research result. Retain the present abstention-only interval as the benchmark illustration, or under Candidate 2's sufficient conditions.

**Source boundary.** I read the common brief, W3, the scan and its two named mathematical reports, then the relevant manuscript passages. The manuscript working copy is at commit 69c25f4704f30d9b999856d85d3dbafa1e0bee41. The ingredients below are the trading payoffs in [A2, Informed trading](overleaf/slot/appendix/A2_beliefs_trading.tex:173), research optimality and the full-purchase lemma in [A5](overleaf/slot/appendix/A5_research.tex:64), and the low-class best response in [A4](overleaf/slot/appendix/A4_coexistence.tex:193). The proposed continuation below is derived here; it is not asserted by those sources. No other solver output in workarounds/raw was read.

### Formal statement

Fix the prior at \(1/2\), \(0<\rho<1\), \(k>0\), \(a>0\), \(0<\bar\lambda<1\), and \(0<\beta<1/2\). Retaining the manuscript's \(\beta\le1/3\) is harmless, but this construction does not need the all-profile zero-order posterior bound. Keep the two-point preparation cost exactly as specified, and suppose \(\Delta>0\), \(\gamma>0\) and \(\tau>1/2\).

Use investor rule IM, the manuscript's default permission to mix over best orders. Use challenger rule C1, or CM with full preparation selected at a purchase-threshold equality.

For every \(\Delta>2k\), define \(\Psi(\Delta)\in(0,1)\) as the unique solution of

\[
\boxed{
2a\Psi
=
\Delta m_\Psi-k+
\bigl(\rho\Delta m_\Psi-k\bigr)_+,
\qquad
m_\lambda=\frac{\beta(1-\lambda)}
{2\beta+(1-2\beta)\lambda}.
}
\tag{1}
\]

Set

\[
\lambda_c(\Delta)=\min\{\bar\lambda,\Psi(\Delta)\}.
\tag{2}
\]

There is an equilibrium with positive research, class H purchasing with probability one after success, and full high-cost preparation after a purchase **if and only if**

\[
\boxed{
\Delta>2k,\qquad
\frac12<\tau\le M_{\lambda_c(\Delta)}.
}
\tag{3}
\]

Among equilibria with full recruitment after a purchase, its research intensity and order distributions are unique. This is not a claim of uniqueness among all equilibria: zero research and, under CM, partial recruitment can coexist with it.

Its entry probability is

\[
\boxed{
\mathsf E_c(\Delta)
=
\rho+(1-\rho)
\left[\beta+\left(\frac12-\beta\right)\lambda_c(\Delta)\right].
}
\tag{4}
\]

Before the cap, \(\Psi\) is continuous and strictly increasing in \(\Delta\), and entry is strictly increasing too. At the transition to full low-class selling, these functions can have a kink. After the cap, research and entry are constant while the purchase continues to recruit.

This is a statement in the \((\Delta,\tau)\) plane without an extra auction-shape or cap-before-selling condition. Along any FOSD path, research and entry are weakly increasing on the set of these equilibria, strictly between uncapped points whose spreads differ. Connectivity along a particular strength path additionally requires that the path remain in the recruiting region (3).

### Derivation

**1. Construct the trading profile and its posteriors.**

At a candidate intensity \(\lambda>0\), let \(z\in[0,1]\) denote the conditional probability that class L sells after research success. Thus

\[
\sigma_H=\delta_1,\qquad
\sigma_L=z\delta_{-1}+(1-z)\delta_0.
\]

Write \(b=(1-\lambda)\beta\), \(b_0=(1-\lambda)(1-2\beta)\). The conditional order likelihoods, in order \((-1,0,1)\), are

\[
f_H=(b,b_0,b+\lambda),\qquad
f_L=(b+\lambda z,b_0+\lambda(1-z),b).
\]

Bayes' rule therefore gives

\[
\mu_+=M_\lambda=\frac{b+\lambda}{2b+\lambda},\qquad
\mu_-=\frac{b}{2b+\lambda z},\qquad
\mu_0=\frac{b_0}{2b_0+\lambda(1-z)}.
\tag{5}
\]

In particular, \(\mu_-,\mu_0\le1/2<\tau\), so sales and abstentions have entry \(\rho\). The purchase posterior is independent of \(z\). Full recruitment after the purchase is valid exactly when \(M_\lambda\ge\tau\), with the stated challenger tie rule.

**2. Solve the low class's best response.**

Its sale earns

\[
U_L(-1)=\rho\Delta\frac{b}{2b+\lambda z}-k.
\tag{6}
\]

This expression decreases strictly in \(z\). At \(z=0\) it is \(\rho\Delta/2-k\); at \(z=1\) it is \(\rho\Delta m_\lambda-k\). Under IM the unique consistent sale probability is

\[
\boxed{
z(\Delta,\lambda)=
\begin{cases}
0,&\rho\Delta\le2k,\\[3pt]
\dfrac{b}{\lambda}\left(\dfrac{\rho\Delta}{k}-2\right),
 &\rho\Delta m_\lambda<k<\rho\Delta/2,\\[7pt]
1,&\rho\Delta m_\lambda\ge k.
\end{cases}
}
\tag{7}
\]

Equivalently, clip the middle expression to \([0,1]\). Its maximized trading payoff at this consistent profile is

\[
\max_q U_L(q)=(\rho\Delta m_\lambda-k)_+.
\tag{8}
\]

In the interior mixing region it earns zero, not the sale profit evaluated while keeping its old abstention-only posterior fixed.

**3. Impose research optimality at the candidate prices.**

The high class's purchase earns

\[
U_H(1)=\Delta m_\lambda-k.
\]

The research deviation faces fixed prices and entry. Its success value is

\[
V=\tfrac12 U_H(1)+\tfrac12(\rho\Delta m_\lambda-k)_+,
\]

provided the purchase is strictly profitable, as it will be at the solution. Interior research requires \(a\lambda=V\), giving (1). At the cap it requires \(V\ge a\bar\lambda\), giving the clipping in (2).

For existence and uniqueness, define

\[
H(\lambda;\Delta)
=
2a\lambda-\Delta m_\lambda+k
-(\rho\Delta m_\lambda-k)_+.
\]

The formula for \(m_\lambda\) gives

\[
m_\lambda'=
-\frac{\beta}{[2\beta+(1-2\beta)\lambda]^2}<0.
\]

Thus \(H\) is continuous and strictly increasing in \(\lambda\). For \(\Delta>2k\),

\[
H(0;\Delta)
=
k-\Delta/2-(\rho\Delta/2-k)_+<0,\qquad
H(1;\Delta)=2a+k>0.
\]

There is exactly one root in \((0,1)\). At that root the high-class purchase is strictly profitable: if the positive-part term is zero, its profit is \(2a\lambda>0\); if that term is positive, \(\rho\Delta m_\lambda>k\) implies \(\Delta m_\lambda>k\). The same argument works at a clipped cap satisfying \(H(\bar\lambda;\Delta)\le0\).

If \(\Delta\le2k\), then the full-purchase profile's gross trading return is at most \(\Delta/2\le k\), since \(m_\lambda\le1/2\). No positive-research equilibrium of the stipulated recruiting form is possible. Necessity of a full H purchase at positive research follows from A5's positive-research lemma, whose proof uses no benchmark auction formula.

**4. Complete the equilibrium tuple.**

Choose \(z\) from (7), beliefs from (5), entry \((\rho,\rho,1)\), truthful bids, and prices

\[
P(x)=t_0+e(x)\,[t_L-t_0+\Delta\mu(x)].
\]

Distinct posteriors give distinct prices because entry is nondecreasing in the posterior and \(t_L-t_0\ge0\). If the sale and zero order share a posterior, both have entry \(\rho\), so their prices coincide and reveal that same posterior. Hence price beliefs and the price-indexed preparation rule are well defined. Wrong-signed orders lose at least \(k\); the H purchase is strict; (7) gives L optimality; and (1)–(2) give optimality over joint research and order deviations. These establish all seven equilibrium conditions, including the price construction.

Conversely, positive research with \(\tau>1/2\) forces a full H purchase. If that purchase fully recruits, the same Bayes formulas, L best response, and research condition force (1)–(7). This proves the claimed pointwise characterization.

**5. Monotonicity and the two trading transitions.**

When low-class sales have zero net profit, including the mixing region,

\[
2a\lambda=\Delta m_\lambda-k,\qquad
\frac{d\lambda}{d\Delta}
=
\frac{m_\lambda}{2a-\Delta m_\lambda'}>0.
\tag{9}
\]

Thus the manuscript's \(\lambda_R=\Lambda(\Delta)\) continues unchanged beyond \(\rho\Delta=2k\). At that point the low-class sale probability starts at zero continuously. Within its mixing region, substituting (9) into (7) gives

\[
\frac{dz}{d\lambda}
=
\frac{2a\rho}{k}(1-2\beta)
+\frac{2(1-\rho)\beta}{\lambda^2}>0.
\tag{10}
\]

The low class gradually moves from abstention to certain selling.

When selling becomes certain and earns positive profits,

\[
\boxed{
2a\lambda=(1+\rho)\Delta m_\lambda-2k,\qquad
\frac{d\lambda}{d\Delta}
=
\frac{(1+\rho)m_\lambda}
{2a-(1+\rho)\Delta m_\lambda'}>0.
}
\tag{11}
\]

The regimes join at

\[
\boxed{
\lambda_{\rm sell}=\frac{k(1-\rho)}{2a\rho},\qquad
\Delta_{\rm sell}
=\frac{k}{\rho m_{\lambda_{\rm sell}}}.
}
\tag{12}
\]

The spread formula is relevant only if \(\lambda_{\rm sell}<1\), and the full-selling transition occurs before the cap only if \(\lambda_{\rm sell}<\bar\lambda\). Equality in (12) makes (9) and (11) identical, so research is continuous. Its slope with respect to the spread increases at the transition: comparing the two positive derivatives at the common point leaves the positive numerator \(2a\rho m_\lambda\).

The purchase probability is always \(b+\lambda/2\), independent of \(z\), which proves (4). Therefore entry rises with research through both transitions.

**6. The actual spread at which the continued branch reaches the cap.**

Solving (1) at \(\bar\lambda\) gives

\[
\boxed{
\Delta_{\rm cap}^{c}
=
\begin{cases}
\dfrac{2a\bar\lambda+k}{m_{\bar\lambda}},
 &\bar\lambda\le\lambda_{\rm sell},\\[8pt]
\dfrac{2a\bar\lambda+2k}{(1+\rho)m_{\bar\lambda}},
 &\bar\lambda>\lambda_{\rm sell}.
\end{cases}
}
\tag{13}
\]

If the low class is still mixing, the cap spread is exactly the manuscript's old cap formula. If full selling precedes the cap, the extra profits bring the cap forward relative to the old formula.

**7. What suffices for a connected path from an existing R start to the cap?**

Suppose the spread and threshold are continuous along strength, the spread strictly increases to the value in (13), and an R equilibrium starts at \(s_R\). If

\[
\varphi_a(s)\ge0
\quad\text{from }s_R\text{ to that cap point},
\tag{14}
\]

then the continuation stays recruiting and is connected under IM. Indeed \(\Psi(\Delta)\ge\Lambda(\Delta)\), since the additional low-class profit in (1) is nonnegative. Condition \(\varphi_a\ge0\) is precisely \(\Lambda(\Delta)\ge\lambda_E(\tau)\), so

\[
M_{\Psi(\Delta)}\ge M_{\Lambda(\Delta)}\ge\tau
\]

up to the cap. Research, the sale probability and entry join continuously at the regime boundaries.

An upward single crossing of the old \(\varphi_a\), maintained over this path, is sufficient for (14). **The cap-before-selling condition is unnecessary for this broader branch.** Condition (14) is itself stronger than necessary after full selling: the exact requirement is (3), because low-class profits can support research even when the old abstention-based margin is negative.

This does not turn arbitrary FOSD paths into intervals. Both \(\tau\) and the recruiting frontier rise, and the threshold can overtake that frontier. The unconditional result is the pointwise characterization and monotone outcome formula on its existence set.

### Conditions

The main pointwise theorem adds no distributional or cost-law restriction to the model. It uses the default investor tie rule IM, which matters: under I0 a strictly interior low-class mixture is forbidden. At a full-selling transition where its sale profit is exactly zero, I0 also forbids the full sale. Therefore an I0 version cannot promise the same connected recruiting continuation.

The only challenger-tie selection used is the manuscript's full preparation at equality; CM allows the same selection. No new preparation cost distribution or renaming of \(c_H\) is involved.

### Benchmark check and the reported counterexample

All numbers here were recomputed with Python from the payoff and equilibrium equations; they are rounded illustrations, not new certified manuscript registry values. The benchmark uses the declared exact decimal \(\beta=0.294655\), \(a=1/40\), and the unrounded cap

\[
\bar\lambda
=\frac{(\mathrm e-1)\beta}{1+(\mathrm e-1)\beta}
=0.336121768915.
\]

In the benchmark, \(\lambda_{\rm sell}=1.2>\bar\lambda\), and even the first sale transition comes after the cap. The continuation therefore reproduces the existing benchmark branch exactly:

\[
r_R=1.501022966263,\quad
r_{\rm cap}=1.677632834385,\quad
r_N=1.747877538268.
\]

At the start, \(\lambda=0.1938533819\) and entry is \(0.5008463670\). At the cap, entry is \(0.5227569435\).

For the counterexample in the brief, keep

\[
(h,\ell,p,c_H,k,\rho,\beta,a,\bar\lambda)
=(10,1,.5,4.5,.5,.5,.2,.01,.4).
\]

For \(1<r<10\), the actual auction formulas are

\[
\Delta=\frac{(r-1)^2}{2r},\qquad
g_L=\frac{3}{8r},\qquad
g_H=10-\frac r2-\frac1{8r},\qquad
\tau=\frac{c_H-g_L}{g_H-g_L}.
\tag{15}
\]

The continued recruiting branch has the following values:

- At its start \(r_R=4.0333831675\): \(\lambda=0.0524096102\), sale probability \(z=0\), entry \(0.6078614415\).
- At \(r_N=5.8284271247\): \(\lambda=0.2811461611\), \(z=0\), entry \(0.6421719242\).
- At \(r=6\): \(\lambda=0.2975222167\), \(z=0.0393515590\), entry \(0.6446283325\).
- At \(r=6.5\): \(\lambda=0.3413391745\), \(z=0.1261685970\), entry \(0.6512008762\).
- At \(r=7\): \(\lambda=0.3801014459\), \(z=0.1863858972\), entry \(0.6570152169\).
- At \(r_{\rm cap}=7.2813291029\): \(\lambda=0.4\), \(z=0.2128\), entry \(0.66\).

At the cap, \(M_\lambda=0.8125\), \(\tau=0.7071585015\), and the purchase recruits with posterior margin \(0.1053414985\). The low-class sale posterior is \(0.3690944882\), so its net sale payoff is zero. The H purchase earns \(0.008=2a\lambda\), giving \(V=0.004=a\lambda\). The prices at \((-1,0,1)\) are approximately \((1.2070820113,1.1783250540,3.1498317469)\), and the zero-order posterior is \(0.3478664193<\tau\). Thus the continuation respects price-based entry, rather than only solving a research equation.

Here \(\lambda_{\rm sell}=25\), so the entire continuation to the cap uses low-class mixing; there is no full-selling regime before the cap.

Existence over the whole interval can also be checked with elementary bounds, rather than inferred from the displayed points. On \([4,5]\),

\[
\tau'=\frac{9r^2-\tfrac32r+6}{(20r-r^2-1)^2}
\le\frac{223.5}{63^2},
\]

which, together with \(\Delta'\ge0.46875\), \(\Delta\le1.6\), and \(\tau\le\tau(5)\), gives \(\varphi_a'>0.09719\). Its endpoint signs give the unique upward root above. On \([5,6]\), monotonicity of \(\Delta,\tau,\lambda_E\) yields

\[
\varphi_a
\ge1.6[1-\tau(6)]-.5-.02(.4)
>0.06549.
\]

On \([6,r_{\rm cap}]\), the corresponding bound is

\[
\varphi_a
\ge(25/12)[1-\tau(r_{\rm cap})]-.5-.02(.4)
>0.10208.
\]

Thus (14) holds throughout. The old branch ends at \(r_N\) only because its definition insists on L abstention. Research and entry do not end there.

For a second illustration that actually reaches full low-class selling before the cap, take the same value distributions and reserve, but

\[
(c_H,k,\rho,\beta,a,\bar\lambda)=(4.7,.1,.5,.2,1,.3).
\]

Then

\[
r_R=2.0381294146,\quad
r_N=2.3797958971,\quad
r_{\rm sell}=2.5062626833,\quad
r_{\rm cap}^{c}=6.2592849615.
\]

Research at those four points is respectively
\(0.0138542260,0.0404630721,0.05,0.3\); entry is
\(0.6020781339,0.6060694608,0.6075,0.645\).
At \(r=3\), full low-class selling gives \(\lambda=0.0970511508\), \(U_H=0.1627348678\) and \(U_L=0.0313674339\), so their half-sum is \(a\lambda\). At the cap the two profits are \(0.4333333333\) and \(0.1666666667\), again giving \(a\lambda=0.3\).

Connectivity in this example can be established with short bounds. On \([2,r_N]\), the derivative formula in Candidate 2 gives \(\varphi_a'>0.08057\) using \(\Delta'\ge.375\), \(\Delta\le.4\), \(\tau\le\tau(r_N)\), and

\[
\tau'\le
\frac{9.4r_N^2-3+5.6}{35^2}.
\]

There is one upward start. After \(r_N\), the purchase posterior at the left endpoint minus the preparation threshold at the right endpoint is positive on each of the successive intervals
\([r_N,r_{\rm sell}]\), \([r_{\rm sell},3]\), \([3,4]\), \([4,5]\), and \([5,r_{\rm cap}^{c}]\).
The respective margins exceed \(0.01531,0.00913,0.02097,0.04858,0.03550\). Since both endpoint functions are monotone, these bounds verify recruitment on all five intervals.

### What is lost

The general branch no longer has “class L abstains” as a defining property. It also loses robustness to the I0 tie rule while low-class sales are mixed. No claim is made that every FOSD path stays recruiting until the cap, nor that every equilibrium has increasing entry. What is retained is the central economic comovement—stronger target-payoff incentives induce more research and more entry—on the entire connected recruiting continuation when the path remains in its existence region.

## Candidate 2: Cheap research and a limited zero-cost preparation share preserve the original interval

Angle: primitive condition

Intuition: The original abstention-only branch reaches the cap if the investor can reach that cap before low-class sales become profitable. Its onset crosses once when the expanding purchase return outpaces the rising recruitment requirement after research costs. A sufficiently low research-cost coefficient guarantees this comparison on a declared range of incumbent strengths; a separate bound on the zero-cost preparation share keeps L out until the cap.

### Formal statement

Consider a continuously differentiable FOSD path on a declared interval, with \(\Delta'>0\), \(\gamma>0\) and \(1/2<\tau<1\). Let \(s_{\rm cap}\) be an attained point satisfying

\[
\Delta(s_{\rm cap})
=
\frac{2a\bar\lambda+k}{m_{\bar\lambda}}.
\]

Suppose \(\varphi_a\) is strictly increasing up to \(s_{\rm cap}\), is negative at the interval's initial point, and is strictly positive at \(s_{\rm cap}\). If

\[
\boxed{
\rho(2a\bar\lambda+k)\le2k\,m_{\bar\lambda},
}
\tag{16}
\]

then the original interior R equilibrium exists exactly on
\([s_R,s_{\rm cap})\) within that interval, where \(s_R\) is the unique zero of \(\varphi_a\). It ends at the research cap, with no low-class selling beforehand. This conclusion uses no investor mixing and holds under IM and I0.

The strict-positive endpoint condition is needed for a nondegenerate branch; merely having a unique upward zero after the cap would not establish one.

A usable sufficient condition for the required monotonicity comes directly from bounds on the auction primitives. Suppose throughout the interval

\[
\Delta'\ge d>0,\quad
\Delta\le\Delta_{\max},\quad
\tau\le T<1,\quad
0\le\tau'\le t,\qquad t>0.
\]

Define the following number only when \(d(1-T)>\Delta_{\max}t\):

\[
\boxed{
a_{\rm mono}
=
\frac{
[d(1-T)-\Delta_{\max}t]\,
[\beta+(1-2\beta)(1-T)]^2
}{2\beta t}.
}
\tag{17}
\]

Then \(0<a<a_{\rm mono}\) guarantees \(\varphi_a'>0\).

These are primitive-checkable bounds. In particular, if differentiation under the auction integrals is valid,

\[
\Delta'
=-\int_p^\infty \partial_s F_s(y)\,[G_L(y)-G_H(y)]\,dy,\qquad
g_L'
=\int_p^\infty \partial_s F_s(y)\,[1-G_L(y)]\,dy,
\]

and

\[
\boxed{
\tau'=\frac{-g_L'+\tau\Delta'}{\gamma}.
}
\tag{18}
\]

For example, a lower bound on \(\gamma\) and upper bounds on \(-g_L'\), \(\tau\), and \(\Delta'\) supply \(t\). The economic requirement is that strengthening widen the target-payoff spread fast enough relative to its erosion of the challenger's acquisition profits, with research sufficiently cheap.

### Derivation

The recruitment intensity is

\[
\lambda_E(\tau)
=
\frac{\beta(2\tau-1)}
{\beta+(1-2\beta)(1-\tau)},\qquad
\frac{d\lambda_E}{d\tau}
=
\frac{\beta}{[\beta+(1-2\beta)(1-\tau)]^2}.
\]

Hence

\[
\varphi_a'
=
\Delta'(1-\tau)-\Delta\tau'
-\frac{2a\beta\tau'}
{[\beta+(1-2\beta)(1-\tau)]^2}.
\tag{19}
\]

The declared bounds give

\[
\varphi_a'
\ge
d(1-T)-\Delta_{\max}t
-\frac{2a\beta t}
{[\beta+(1-2\beta)(1-T)]^2}>0
\]

under (17). Formula (18) follows by differentiating
\(\tau=(c_H-g_L)/\gamma\) and using
\(\gamma'=-\Delta'\), since the class-mean gap \(\Delta+\gamma\) is fixed.

Strict monotonicity and the endpoint signs give the unique start. On the resulting interval, \(\varphi_a\ge0\) is equivalent to \(\lambda_R\ge\lambda_E\), and \(\Delta<\Delta(s_{\rm cap})\) is equivalent to \(\lambda_R<\bar\lambda\). Finally, (16) is exactly

\[
\Delta(s_{\rm cap})\le\frac{2k}{\rho}.
\]

Thus L strictly prefers abstention before the cap. These are all the R conditions; no unproved branch ordering is needed.

An economically transparent way to write the same no-selling restriction is

\[
\rho\le
\frac{2k m_{\bar\lambda}}{2a\bar\lambda+k}.
\tag{20}
\]

Alternatively, for a fixed \(\rho<2m_{\bar\lambda}\), it is

\[
a\le
\frac{k}{2\bar\lambda}
\left(\frac{2m_{\bar\lambda}}{\rho}-1\right).
\]

Thus “cheap enough research” can guarantee both single crossing and the desired endpoint, provided the auction path supplies the positive leading margin in (17).

### Benchmark check

On \(r\in[6/5,7/4]\), use the primitive bounds already employed in [the manuscript's branch proof](overleaf/slot/appendix/A5_research.tex:286):

\[
d=\frac{11}{72},\qquad
\Delta_{\max}=\frac9{56},\qquad
1-T=\frac{19}{55},\qquad
t=\frac{16875}{211288}.
\]

Direct evaluation gives

\[
d(1-T)-\Delta_{\max}t=0.039941963290,
\]

\[
a_{\rm mono}=0.161712762601,\qquad
a=0.025,\qquad
\varphi_a'\ge0.033767131656.
\]

The cost coefficient is below this sufficient monotonicity bound by \(0.136712762601\). The initial margin is \(\varphi_a(1.2)=-0.022693027366\), and at the cap it is \(0.017445748457>0\), giving the unique start before the cap.

For the endpoint condition,

\[
m_{\bar\lambda}=0.268941421370,
\]

\[
2k m_{\bar\lambda}-\rho(2a\bar\lambda+k)
=
0.001556134743>0.
\]

Equivalently,

\[
\Delta_{\rm cap}=0.136855409845
<
\Delta_N=0.16,
\]

with spread margin \(0.023144590155\), or strength margin

\[
r_N-r_{\rm cap}=0.070244703883.
\]

The endpoint condition allows \(a\le0.034259351148\), giving margin \(0.009259351148\) over the benchmark \(a=0.025\). At fixed benchmark \(a,\beta,\bar\lambda,k\), it allows
\(\rho\le0.292279275225\), compared with the chosen \(0.25\).

### Conditions and how far they are from necessary

The cost bound (17) is deliberately sufficient. It uses independent worst-case bounds and forces the whole margin to rise, whereas one upward crossing needs only the appropriate sign pattern. A weaker, economically interpretable sufficient condition is that, once \(J>k\), the available purchase margin per unit of recruitment intensity,

\[
\frac{J(s)-k}{2\lambda_E(s)},
\]

crosses the fixed research cost \(a\) only once from below. It need not increase at every strength.

Condition (16), unlike the derivative bound, is exact for ordering the old cap spread and the L-selling threshold, when both are attained along a continuous increasing-spread path. It is necessary for an abstention-only branch to reach its cap while remaining recruiting. It is not necessary for the economically broader branch in Candidate 1 to reach the cap.

### What is lost

Relative to an unrestricted general theorem, the original interval statement requires a path restriction and a bound linking the free-preparation share, research costs, the cap, and trading costs. These are economically meaningful restrictions and have explicit benchmark margins, but they do exclude perfectly regular auctions. Candidate 1 avoids the no-selling restriction by letting the low class adjust.

## Importance of the weakness

The reported counterexample is not based on reversed class ranking, an unusual incumbent distribution, extreme posteriors, or an incumbent that outbids class H: its entire relevant range has \(r<h=10\). The values, preparation cost \(c_H=4.5\), liquidity probability \(0.2\), free-preparation share \(0.5\), and cap \(0.4\) are ordinary interior parameter choices. Research is especially cheap relative to trading: its total cost at the cap is \((a/2)\bar\lambda^2=0.0008\), compared with \(k=0.5\) per trade. That makes a long mixing continuation particularly transparent, but is not essential to the weakness.

In fact, retain every benchmark primitive except increase \(\rho\) from \(0.25\) to \(0.30\). The old recruitment margin and research formula are unchanged, but

\[
r_N=1.666666666667
<
r_{\rm cap}=1.677632834385.
\]

The abstention-only branch now ends before the cap under this modest change. The continuation reaches the same cap with L selling probability \(0.0307464973\); entry rises from \(0.5534802367\) at \(r_N\) to \(0.5545731472\) at the cap.

The weakness therefore matters for the general theorem's branch definition, endpoint, and tie-rule robustness. Under the default IM rule it does not overturn the paper's main research-and-entry mechanism. The best repair turns the omitted region into an additional comparative-statics result: the onset of bad-news sales changes trading behavior without interrupting rising research or entry.

The remaining economic limit is real. A stronger incumbent also raises the preparation threshold, so an unrestricted strength path can leave the recruiting region. Candidate 1 establishes comovement on the recruiting equilibrium set; it does not claim that recruitment survives all strengthening.

## Other findings (errors in the manuscript, anything surprising)

**Increasing \(J\) alone does not imply an upward single crossing of \(\varphi_a\), even on a path where H always wins.** Here is an independently constructed primitive example.

Take \(G_H=\delta_{10}\), \(G_L=\delta_1\), \(p=.5\), \(c_H=4\), \(\rho=.1\), \(k=.55\), \(\beta=.2\), \(a=1.7\), and \(\bar\lambda=.8\). Let

\[
R_\Delta\sim U[\Delta+.9,\Delta+1.1],\qquad
1.1\le\Delta\le2.99.
\]

This is a continuous FOSD path, and every incumbent value lies strictly between \(1\) and \(10\). Therefore

\[
g_L=0,\quad g_H=9-\Delta,\quad
t_L=1,\quad t_H=1+\Delta,
\]

so its target-payoff spread is indeed the indexing variable \(\Delta\), and

\[
\tau=\frac4{9-\Delta},\qquad
J=\frac{\Delta(5-\Delta)}{9-\Delta},\qquad
\frac{dJ}{d\Delta}
=
1-\frac{36}{(9-\Delta)^2}>0
\]

throughout the stated interval. Also

\[
\lambda_E=\frac{\Delta-1}{4(6-\Delta)}.
\]

Nevertheless, direct evaluation gives

\[
\varphi_a(1.1)=-0.0243089641,\qquad
\varphi_a(2)=0.0946428571,\qquad
\varphi_a(2.9)=-0.0726070862.
\]

Its upward and downward zeros are approximately \(1.203586565480\) and \(2.692672076379\). Thus it enters and leaves the recruiting research branch while \(J\) is still rising. Low-class selling cannot explain the failure: \(\rho\Delta<0.3<2k=1.1\) on the whole path. Nor can the cap: (9) implies \(\lambda_R<\Delta/(4a)<0.44<0.8\). The missing comparison is the growth of the purchase margin relative to the rising intensity required for recruitment.

**The research first-order condition needs its factor of two kept straight.** With prior \(1/2\), \(a\lambda=\tfrac12[U_H(1)+\max\{U_L(-1),0\}]\). Equivalently \(2a\lambda=U_H(1)+\max\{U_L(-1),0\}\), not half that sum. This corrects the tentative equation suggested in W3; the current manuscript's abstention-branch equation already has the correct normalization.

**No I0 nonexistence claim for all equilibria follows.** I0 rules out the mixed-sale recruiting continuation. Other equilibria, including nonrecruiting positive research, can remain. The restriction is on the connected recruiting branch.

**Verification performed.** I derived the Bayes posteriors, trading best responses, research conditions and price construction directly from the manuscript. I ran the calculation script at audit/theory_upgrade_2026_10_25/solvers/computations/W3_A/explore_w3.py with the real declared benchmark, the supplied counterexample, the full-selling illustration, and the new single-crossing counterexample. It prints intensities, conditional sale probabilities, posteriors, order payoffs, competitive prices, research-value balances and entry; no assertions or tests were written or run. The numerical values are floating-point evaluations; the general claims above rest on the displayed analytical derivations. No manuscript, numerical pipeline, or repository file other than this designated report was changed.
