# W1-coexistence-interval: Solver A

Date: 25 October 2026. Manuscript inspected: `overleaf/slot/`, commit `69c25f4704f30d9b999856d85d3dbafa1e0bee41`. This is a research proposal with derivations, not a manuscript revision. The preparation cost remains exactly the paper's two-point cost, with high cost named \(c_H\).

**Recommendation.** State the unconditional coexistence region and the entry comparison in Candidate 1. For an economic primitive condition that recovers the strength interval, Candidate 2 gives a short analytic theorem covering the benchmark and genuinely dispersed classes. Candidate 3 permits general ranked classes and general incumbent families, and requires single crossing only while no trade can survive. Global monotonicity of \(J\) is unnecessary for the interval claim.

The key manuscript passages are [Proposition 3](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/sections/04_equilibrium_results.tex:254), [the path lemma and threshold order](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A4_coexistence.tex:10), [the pointwise coexistence argument](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A4_coexistence.tex:477), and [the prior classification](/Users/austinli/Projects/competition-creates-competition/overleaf/slot/appendix/A4_coexistence.tex:501). Line references below refer to the inspected source. I also read `SCAN.md` and the two designated scan reports; their pointwise criterion is rederived below.

Throughout, use the default rules IM and C1. Fix the slot, the prior, and all auction primitives except the incumbent distribution. Write

$$
\Delta=\Delta_T>0,\qquad
\gamma=g_H-g_L>0,\qquad
d=\mathbb E_H\theta-\mathbb E_L\theta=\Delta+\gamma,
\qquad q_\pi=\max\{\pi,1-\pi\}.
$$

Thus \(d\) is fixed along an incumbent path. Define \(B_F(\mu)=g_L+\mu\gamma\), \(\tau=(c_H-g_L)/\gamma\), and \(J=\Delta(1-\tau)\). Prices and ownership need additional auction objects; the claims here concern coexistence, orders, posteriors, and entry.

## Candidate 1: A fixed coexistence region and entry that rises whenever coexistence occurs

Angle: reformulate

Intuition: Coexistence requires a purchase to make preparation worthwhile and to pay for its own information. The spread must therefore be large enough to support a recruiting purchase, but small enough that trading against an uninformative price remains unprofitable. These restrictions define a convex region in two economically interpretable coordinates; any stronger incumbent that remains in, or returns to, this region has weakly higher entry on its informative equilibrium.

### Formal statement

For every ranked-class auction satisfying the standing positive-gap assumptions, no informed trade and an informative equilibrium coexist exactly when

$$
\boxed{
\pi<\tau\le M(\pi),\qquad
\frac{k}{1-\tau}\le\Delta\le\frac{k}{\rho q_\pi}.
}
\tag{1}
$$

Intersect this region with the auction's attainable coordinates, including \(0<\Delta<d\). The region in (1) is convex: equivalently,

$$
\pi<\tau\le M(\pi),\qquad
\tau\le1-\frac{k}{\Delta},\qquad
\Delta\le\frac{k}{\rho q_\pi}.
\tag{2}
$$

The informative equilibrium is unique under IM/C1. Its entry exceeds the no-trade entry \(\rho\) by

$$
\boxed{
\mathsf E_I(F)-\mathsf E_N(F)
=(1-\rho)\min\left\{
\frac{(1-\pi)b\Delta(F)}{k},\ b+\pi\lambda
\right\}.
}
\tag{3}
$$

Consequently, if \(F_t\) is stronger than \(F_s\) and coexistence holds at both laws,

$$
\mathsf E_I(F_t)\ge\mathsf E_I(F_s).
\tag{4}
$$

This comparison does not require coexistence at intervening strengths. It is strict if the spread increases and the lower-strength informative equilibrium has a mixed purchase; once purchases are full, entry is constant. These statements concern the informative equilibrium on the coexistence set, not a selection that switches between the informative and uninformative equilibria.

Two unconditional economic restrictions follow:

$$
\tau\le1-\rho q_\pi,
\qquad
\pi<\frac1{1+\rho}.
\tag{5}
$$

The second is a universal upper bound on the prior permitting coexistence, rather than the paper's sharper path-specific prior cutoff. It is necessary, not sufficient for a particular auction path to exhibit coexistence.

### Derivation

If \(\pi\ge\tau\), no informed trade entails entry one under C1. Its optimality requires \(\Delta q_\pi\le k\). An informative purchase has posterior strictly above \(\pi\), so its gross return is strictly below \(\Delta(1-\pi)\le k\); an informative sale has posterior strictly below \(\pi\), entry at most one, and return strictly below \(\Delta\pi\le k\). Thus coexistence requires \(\pi<\tau\), as in A4:493–499.

For \(\pi<\tau\), no informed trade gives entry \(\rho\) after every order. Its two possible profitable deviations have gross returns \(\rho\Delta(1-\pi)\) and \(\rho\Delta\pi\). Hence it is an equilibrium exactly when \(\rho\Delta q_\pi\le k\).

Under that inequality, the low class abstains in every equilibrium: any positive sale lowers its posterior and strictly reduces its return below \(\rho\Delta\pi\le k\). Let \(s=\lambda\sigma_H(1)>0\) be the high-class purchase rate. Bayes' rule gives

$$
\mu_+(s)=\frac{\pi(b+s)}{b+\pi s},\qquad
1-\mu_+(s)=\frac{(1-\pi)b}{b+\pi s}.
$$

A purchase that fails to recruit has gross return strictly below its no-trade deviation return, so an informative equilibrium must recruit. Recruitment is feasible precisely when \(\tau\le M(\pi)\). The purchase rate first attaining the threshold is

$$
s^*=\frac{b(\tau-\pi)}{\pi(1-\tau)}.
$$

Among recruiting rates, the gross return

$$
\Delta[1-\mu_+(s)]
=\frac{\Delta(1-\pi)b}{b+\pi s}
$$

decreases strictly in \(s\), and its value at \(s^*\) is \(J\). Therefore a recruiting mixed or full purchase exists exactly when \(J\ge k\); it is unique. At equality it is the threshold purchase with entry one, including a full purchase if \(\tau=M(\pi)\). This proves (1), including its weak boundaries.

The informative rate is

$$
s_I=\min\left\{\lambda,
\frac b\pi\left[\frac{(1-\pi)\Delta}{k}-1\right]\right\}.
$$

Only purchases recruit, their unconditional probability is \(b+\pi s_I\), and entry after a purchase is one. This yields (3). FOSD raises \(\Delta\), giving (4). For convexity, \(1-k/\Delta\) has second derivative \(-2k/\Delta^3<0\), so its hypograph in (2) is convex; the remaining restrictions are half-spaces. The region remains convex after imposing \(\Delta<d\).

Finally the two spread bounds in (1) imply \(1-\tau\ge\rho q_\pi\). Combining this with \(\pi<\tau\) gives \(\pi<1-\rho q_\pi\). If \(\pi\ge1/2\), this is \(\pi<1/(1+\rho)\); if \(\pi<1/2\), that upper bound holds automatically because \(\rho<1\). This proves (5).

### Conditions

No additional auction or path condition beyond the model's ranked, admissible classes, positive gaps, independence, two-point preparation cost, and default IM/C1 rules. For the comparison across strengths, only FOSD is added. Continuity of the strength path is unnecessary for (1)–(5).

Under CM, extra threshold equilibria can occur, so the uniqueness claim and the interpretation of (3) must be confined to the recruiting branch with entry one. I0 removes mixed purchases. These tie rules should not be silently interchanged.

### Benchmark check

Using the manuscript's exact slot declarations \(\beta=0.294655\), \(u=e-1\), and \(\lambda=u\beta/(1+u\beta)\), I obtain

$$
\lambda\approx0.336121769,\quad b\approx0.195615040,
\quad M(1/2)\approx0.731058579.
$$

At prior \(1/2\), the no-trade spread cap is \(2k/\rho=0.16\). Direct evaluation of the benchmark payoff formulas and numerical bisection give

$$
r_A\approx1.393957920,\qquad
r_F\approx1.467127041,\qquad
r_N\approx1.747877538.
$$

At the start, \(\tau_A\approx0.640739076\) and informative entry is approximately \(0.454184856\). Entry reaches \(0.522756943\) at full purchases and stays there through \(r_N\); no-trade entry is \(0.25\). The universal prior ceiling is \(0.8\). The feasibility margin \(1-\rho/2-\tau_A\) is approximately \(0.234260924\).

### What is lost

The theorem does not assert that an arbitrary FOSD path enters the region once, or that coexistence must end at the no-trade cutoff. It retains the full multiplicity mechanism, uniqueness of the recruiting outcome, its exact entry gain, and the economic comparative static across any coexisting strengths. A monotone path can leave and reenter a convex region; convexity is not a substitute for a path condition.

## Candidate 2: Uniform incumbent growth with preparation affordable against the largest rival

Angle: primitive condition

Intuition: When class H can finance preparation even against the incumbent's largest possible bid, its preparation surplus has room to absorb stronger competition. Under uniform incumbent growth and separation of the class supports, the spread widens fast enough that the return to a recruiting purchase rises. Neither challenger class needs to be a point mass.

### Formal statement

Let \(F_r=U[0,r]\) for \(r\in[r_0,r_2]\), with \(p<r_0<r_2\). Suppose

$$
\operatorname{supp}(G_L)\subseteq[p,r_0],\qquad
\operatorname{supp}(G_H)\subseteq[r_2,\infty),\qquad
\boxed{\mathbb E_H\theta-r_2\ge c_H.}
\tag{6}
$$

On the positive-spread domain, \(J(r)\) is strictly increasing. Consequently the coexistence set is an interval for every fixed prior and slot, possibly empty or a singleton. If the path starts with \(\tau(r_0)>1/2\), has attained thresholds \(J(r_A)=k\) and \(\rho\Delta(r_N)/2=k\) with \(r_A<r_N\), and \(\tau(r_N)\le M(1/2)\), then

$$
C(1/2)=[r_A,r_N].
\tag{7}
$$

The additional threshold assumptions in (7) determine the onset, endpoint and nonemptiness. Monotonicity alone cannot imply those features.

### Derivation

Let \(v_H=\mathbb E_H\theta\), \(v_L=\mathbb E_L\theta\), and \(m_{2,L}=\mathbb E_L\theta^2\); the latter is finite by the low-class support bound. Both classes meet the reserve. Every high-class value outbids every incumbent, and every low-class value is below the incumbent's upper support. Integrating the second-price payments gives

$$
g_H=v_H-\frac r2-\frac{p^2}{2r},\qquad
g_L=\frac{m_{2,L}-p^2}{2r},\qquad
\Delta=\frac r2-v_L+\frac{m_{2,L}}{2r}.
\tag{8}
$$

Write \(d=v_H-v_L\), \(\gamma=d-\Delta\), and

$$
A(r)=-g_H'(r)=\frac{r^2-p^2}{2r^2}>0.
$$

Differentiating \(J=\Delta(g_H-c_H)/\gamma\), using \(\gamma'=-\Delta'\), gives the general identity

$$
J'=\frac{d(g_H-c_H)\Delta'-\Delta\gamma A}{\gamma^2}.
\tag{9}
$$

The cost coverage restriction in (6) implies \(v_H-c_H\ge r_2\ge r\), hence

$$
g_H-c_H\ge\frac r2-\frac{p^2}{2r}=rA.
\tag{10}
$$

The low-class support restriction implies

$$
r\Delta'-\Delta
=v_L-\frac{m_{2,L}}r
=\mathbb E_L\!\left[\theta\left(1-\frac\theta r\right)\right]\ge0.
\tag{11}
$$

Substitute (10)–(11) into (9):

$$
\begin{aligned}
J'
&\ge\frac{A[d\,r\Delta'-\Delta\gamma]}{\gamma^2}\\
&\ge\frac{A\Delta(d-\gamma)}{\gamma^2}
=\boxed{\frac{A\Delta^2}{\gamma^2}>0}.
\end{aligned}
\tag{12}
$$

This proves the monotonicity without a polynomial root count. Under FOSD, \(B_{F_r}(\pi)\) and \(B_{F_r}(M)\) fall, so \(\{\pi<\tau\}=\{B(\pi)<c_H\}\) is an up-set, \(\{\tau\le M\}=\{B(M)\ge c_H\}\) is a down-set, and the no-trade inequality is a down-set. Intersecting them with the up-set \(\{J\ge k\}\) gives an interval. Continuity and the displayed endpoint conditions then give (7).

### Conditions

The substantive restrictions are the uniform incumbent family, the separation of class supports by the path's endpoint supports, and high-class expected preparation affordability against the largest incumbent. The two-point cost law is unchanged. High-class dispersion can be arbitrary, with finite mean; low-class dispersion can be arbitrary within \([p,r_0]\).

These are sufficient, not necessary. In the point-mass case a weaker sufficient cost bound is

$$
c_H\le h-r_2+\frac\ell2-\frac{p^2}{2r_2}.
\tag{13}
$$

To see this, \(A/\Delta'=(r^2-p^2)/(r^2-\ell^2)\), and

$$
\frac{\Delta\gamma A}{d\Delta'}
<\Delta\frac{A}{\Delta'}
=\frac{(r-\ell)(r^2-p^2)}{2r(r+\ell)}
<\frac{r-\ell}{2}.
$$

Thus \(g_H-c_H\ge(r-\ell)/2\) suffices for (9) to be positive. The resulting upper bound \(h-r+\ell/2-p^2/(2r)\) decreases in \(r>\ell>p\), proving (13). In particular, one can violate the simple cost coverage condition while preserving strict monotonicity.

### Benchmark check

The low-class support is \(\{1\}\), below \(r_0=1.2\) by \(0.2\). The high-class support is \(\{10\}\), above \(r_2=3.6\). The cost coverage margin is

$$
h-r_2-c_H=10-3.6-6=\boxed{0.4}.
$$

Therefore (12) is an analytic proof of the benchmark's rising \(J\) on the entire stated path. Direct formula evaluation gives

$$
J(1.2)\approx0.006114719<0.02,
\qquad J(3.6)\approx0.252192932>0.02,
$$

and \(J'(1.2)\approx0.055388985\), \(J'(3.6)\approx0.081264223\). The derivative values are illustrative calculations; the proof of its sign throughout the interval is (12).

For the desired coexistence endpoint, \(J(r_N)\approx0.055285899>k\), \(\tau(r_0)\approx0.633116883>1/2\), and \(\tau(r_N)\approx0.654463131<M\), the last inequality having margin approximately \(0.076595448\) at the benchmark slot. Thus (7) follows. The weaker point-class bound (13) allows \(c_H\le6.865277778\), with margin \(0.865277778\) at the actual cost; for example, \(c_H=6.6\) fails the simpler coverage condition but still gives rising \(J\).

For an illustration with genuinely dispersed classes, take \(G_L=U[0.75,1.1]\) and \(G_H=U[9,11]\), retaining the benchmark cost, reserve, and incumbent path. Condition (6) still has margin \(0.4\). Equations (8)–(9) give \(J(1.2)\approx0.013040020\), \(J(3.6)\approx0.266716664\), and positive derivatives at both endpoints; the exact sign for all strengths again follows from (12). The companion calculation prints the more precise values.

### What is lost

This theorem covers a substantial set of class distributions but keeps a particular shape of incumbent strengthening and requires separated class supports. It does not follow merely from class H always winning; the incumbent family matters. It does not establish every inequality in the benchmark's full threshold table, nor the CM threshold-branch trend involving \(\Delta(1-\tau)^2\). Those are separate claims. It replaces only the monotonicity ingredient relevant to W1 and then uses explicit endpoint conditions for the advertised interval.

## Candidate 3: Small trading costs and bounded erosion of high-class profit

Angle: primitive condition

Intuition: Coexistence matters only before trading against the no-trade price becomes profitable. Small trading costs make that relevant range of spreads short. If strengthening does not destroy an arbitrarily large amount of high-class auction profit for each unit by which it widens the target's class spread, the recruiting-profit threshold can cross its cost only once within that range, even if it crosses back later.

### Formal statement

Let \(F_s\) be any FOSD family with ranked admissible classes and positive gaps. For a fixed prior let

$$
\Delta_N(\pi)=\frac{k}{\rho q_\pi},\qquad
I_N(\pi)=\{s:\Delta(s)\le\Delta_N(\pi)\}.
$$

Suppose there is a finite constant \(L\ge1\) such that for all \(s<t\) in this no-trade spread range,

$$
\boxed{
g_H(s)-g_H(t)\le L[\Delta(t)-\Delta(s)].
}
\tag{14}
$$

This is an inequality directly on the primitives:

$$
\int_p^\infty [F_s(y)-F_t(y)][1-G_H(y)]\,dy
\le L\int_p^\infty[F_s(y)-F_t(y)]D(y)\,dy.
\tag{15}
$$

If

$$
\boxed{kL\le d\rho^2q_\pi^2,}
\tag{16}
$$

then \(C(\pi)\) is an interval, with no global monotonicity or global up-set assumption on \(J\). The condition

$$
\boxed{kL\le d\rho^2/4}
\tag{17}
$$

works simultaneously at every prior, if (14) holds on \(\{\Delta\le2k/\rho\}\). For continuous paths with strictly increasing \(\Delta\) and strict (16), an attained crossing \(J=k\) in \(I_N\) is unique. At prior \(1/2\), the same endpoint assumptions as in Candidate 2 then give \([s_A,s_N]\).

### Derivation

The crucial change is to study a function with the same sign as \(J-k\), rather than insist that \(J\) itself rises. Define

$$
H_k(s)=g_H(s)-c_H+k-\frac{kd}{\Delta(s)}.
$$

Since \(\gamma=d-\Delta\), direct algebra gives

$$
\boxed{J(s)-k=\frac{\Delta(s)}{\gamma(s)}H_k(s).}
\tag{18}
$$

For \(s<t\) in \(I_N\), (14) implies

$$
\begin{aligned}
H_k(t)-H_k(s)
&=g_H(t)-g_H(s)+kd\left(\frac1{\Delta(s)}-\frac1{\Delta(t)}\right)\\
&\ge\left[\frac{kd}{\Delta(s)\Delta(t)}-L\right]
[\Delta(t)-\Delta(s)]\\
&\ge\left[\frac{d\rho^2q_\pi^2}{k}-L\right]
[\Delta(t)-\Delta(s)]\ge0.
\end{aligned}
\tag{19}
$$

Thus \(\{J\ge k\}\) is an up-set relative to the no-trade range. That is all coexistence needs. The other constraints are the up-set \(\{B_s(\pi)<c_H\}\), the down-set \(\{B_s(M(\pi))\ge c_H\}\), and \(I_N\) itself, a down-set. Their intersection is an interval. No differentiability is required. With strict (16) and strictly increasing \(\Delta\), (19) is strict, giving uniqueness of a threshold crossing in the relevant range. Since \(q_\pi\ge1/2\), (17) implies (16) at every prior.

The economic content of (14) is also expressible as

$$
g_L(s)-g_L(t)\le(L-1)[\Delta(t)-\Delta(s)].
$$

Indeed, \(g_H=g_L+d-\Delta\). The restriction limits the common erosion of challenger surplus relative to the extra class distinction created in target proceeds. Strengthening concentrated below both challenger classes can violate it; that is exactly the force in the disconnected example below.

### Conditions

General ranked classes, any FOSD family, the original two-point preparation cost, fixed slot and prior, and the primitive integral inequality (15). A convenient way to verify (14) on a differentiable path is \(-g_H'(s)\le L\Delta'(s)\); at a flat spread it requires the high-class profit to be flat too. The finite-difference version (15) is the theorem's condition and avoids regularity issues.

Neither (14) nor the small-cost bound is necessary. They are transparent sufficient bounds, and the argument deliberately makes no assertion about \(J\) after the last possible no-trade strength. Even before that point, it is the sign of (18), rather than monotonicity of \(J\) below its threshold, that is controlled.

### Benchmark check

For the point-mass/uniform payoff formulas,

$$
\frac{-g_H'(r)}{\Delta'(r)}
=\frac{r^2-p^2}{r^2-\ell^2}
\le\frac{r_0^2-p^2}{r_0^2-\ell^2}
=\frac{119}{44}=:L,
$$

because the ratio decreases in \(r>\ell>p\). Integrating verifies (14) for every pair on the path. The all-prior cost ceiling is

$$
\frac{d\rho^2}{4L}
=\frac{99}{1904}
\approx0.0519957983.
$$

The actual cost \(k=0.02\) is smaller by \(0.0319957983\), a factor of approximately \(2.59979\). Equivalently, the strict margin in (17) is

$$
d\rho^2/4-kL\approx0.0865340909>0.
$$

This proves interval coexistence at every prior without a global certificate for \(J'\). The benchmark endpoint numbers in Candidate 2 recover \([r_A,r_N]\) at the even prior. For the four cases of Corollary A.2, retain the separate level-crossing and start-feasibility conditions; the latter hold with \(\tau_A\approx0.640739076<1-\rho=0.75\), margin \(0.109260924\). At the benchmark slot, \(M^{-1}(\tau_A)\approx0.396175424\); the two sharper start margins in the scan are approximately \(0.208304780\) and \(0.199076155\).

To see how far the sufficient bound is from necessity, extend the otherwise identical uniform path down to \(r_0=1.01\). The convenient global \(L\) becomes approximately \(38.3134\), making (17)'s trading-cost ceiling only \(0.00367038\), below the actual \(0.02\). Nevertheless Candidate 2 still proves rising \(J\), and the same nonempty coexistence interval survives. A large conservative \(L\) can therefore reject an entirely well-behaved model.

### What is lost

Nothing about the original interval is lost when the endpoint and recruitment conditions hold. What changes is the sufficient assumption: global increasing \(J\) is replaced by a quantitative restriction on primitive profit erosion over the portion of the path where no trade can exist. The entire benchmark equilibrium table, global threshold ordering, and the CM entry trend still require their own arguments.

## Importance of the weakness

### The known counterexample is valid, but does not itself locate a coexistence failure at the benchmark costs

For \(h=10\), \(\ell=1\), \(p=1/2\), \(c_H=2\), and \(R_z\sim U[z-0.1,z+0.1]\), all incumbents lie strictly between the class values. Therefore

$$
\Delta=z-1,\qquad g_L=0,\qquad \gamma=g_H=10-z,
\qquad J=(z-1)\left(1-\frac2{10-z}\right).
$$

This yields exactly \(J(7)=2\) and \(J(7.5)=1.3\). More explicitly,

$$
\frac{dJ}{dz}=1-\frac{18}{(10-z)^2}<0
\quad\text{on }[7,7.5].
$$

These are regular continuous FOSD laws with economically interpretable values: the incumbent is strong enough to eliminate the low class's auction profit and erodes the high class's remaining preparation surplus. The narrow incumbent support is not a singularity; any continuous law wholly between the class values has payoffs determined by its mean in the same way.

However, retaining \(\rho=1/4\), \(\pi=1/2\), and \(k=0.02\), the no-trade deviation returns are \(0.75\) and \(0.8125\), respectively. They vastly exceed \(k\); coexistence is already impossible. At the benchmark slot the second point also has \(\tau=0.8>M\). The example disproves global monotonicity of \(J\), but additional work is needed to demonstrate an actual disconnected coexistence set.

### A disconnected coexistence set with the benchmark values, costs, prior, and slot

Here is that additional work. Keep exactly

$$
h=10,\quad\ell=1,\quad p=1/2,\quad c_H=6,
\quad\rho=1/4,\quad k=1/50,\quad\pi=1/2,
$$

and the benchmark slot used above. Only the incumbent family changes. Define, for \(t\in[0,2]\), the continuous mixture

$$
R_t\sim0.9\,U[m_L(t)-0.01,m_L(t)+0.01]
+0.1\,U[m_H(t)-0.01,m_H(t)+0.01],
$$

where

$$
(m_L(t),m_H(t))=
\begin{cases}
(0.6+0.38t,\ 1.57),&0\le t\le1,\\
(0.98,\ 1.57+0.23(t-1)),&1\le t\le2.
\end{cases}
\tag{20}
$$

Couple the mixture indicator and the within-component uniform draw across strengths. Each realization is nondecreasing in \(t\); hence this is a continuous FOSD path. Every incumbent meets the reserve and is below the high class; the 90 percent component remains below \(\ell\), while the 10 percent component stays above it. Thus

$$
\Delta(t)=0.1[m_H(t)-1],\quad
g_L(t)=0.9[1-m_L(t)],\quad
\gamma(t)=9-\Delta(t),\quad
\tau(t)=\frac{6-g_L(t)}{9-\Delta(t)}.
\tag{21}
$$

Direct substitution gives:

- At \(t=0\): \(\Delta=0.057\), \(g_L=0.36\), \(\tau\approx0.630660852\), and \(J\approx0.021052331>0.02\). Coexistence holds.
- At \(t=1\): \(\Delta=0.057\), \(g_L=0.018\), \(\tau\approx0.668903053\), and \(J\approx0.018872526<0.02\). Coexistence fails.
- At \(t=2\): \(\Delta=0.08\), \(g_L=0.018\), \(\tau\approx0.670627803\), and \(J\approx0.026349776>0.02\). Coexistence holds again.

The other pointwise conditions hold along the entire path: \(1/2<\tau(t)<0.671<M\), and \(\rho\Delta(t)/2\le0.01<0.02\). Thus the middle failure is entirely due to \(J\), not an entry ceiling or the disappearance of no trade.

The components can be located explicitly. In the first stage,

$$
J\ge k
\iff g_L\ge0.194894736842\ldots
\iff t\le0.482763927362\ldots.
$$

In the second stage, writing \(x=\Delta\),

$$
J\ge k
\iff -x^2+3.038x-0.18\ge0.
$$

The relevant root is \(x\approx0.0604524347832\), attained at \(t\approx1.150105860137\). The coexistence set is therefore

$$
\boxed{
C(1/2)=[0,\,0.482763927362\ldots]
\ \cup\ [1.150105860137\ldots,\,2].
}
\tag{22}
$$

This is an exact analytical characterization with displayed approximate endpoints. It is not a grid-based inference. If a strictly increasing spread is desired, replace the first-stage high-component mean by \(1.57+0.001t\) and the second by \(1.571+0.229(t-1)\). Then \(\Delta\) rises strictly; at the middle point \(J\approx0.018905209<k\), while both endpoint inequalities remain strict. Continuity still gives disconnected coexistence. The kink in the path can also be smoothed without changing the strict three-point inequalities.

Economically, the first stage strengthens incumbents who still lose to both classes. It reduces both classes' auction profits without widening their proceeds difference, so the preparation threshold rises and a previously sustainable informative purchase disappears. The second stage strengthens incumbents between the class values, widening the spread and restoring the informative equilibrium. The probability weights and value levels are ordinary, although the bimodal family and its changing direction of improvement are intentionally chosen to isolate these forces. This is a structural possibility, not evidence that disconnected intervals are typical. The example even satisfies \(W_H=1\) and \(h-\sup_t\sup R_t-c_H=2.19>0\): winning for certain and covering preparation at the largest incumbent do not suffice without a restriction on the incumbent family.

The weakness therefore matters for a general theorem about the topology of equilibrium multiplicity, including the prior classification. It does not overturn the stock-price feedback mechanism or the entry comparison on the recruiting branch. The benchmark's connected interval is especially secure: Candidates 2 and 3 each provide an independent analytic reason for it. The original decreasing-\(J\) example also explains why global \(J\) monotonicity imposes more than coexistence needs.

## Other findings (errors in the manuscript, anything surprising)

1. **The current scoped benchmark claim is true.** Proposition 3 and A4 explicitly impose the benchmark. W1 concerns how far that result can be generalized, not an established counterexample to the proposition as written. The new example changes the incumbent family, so it does not contradict the existing scoped theorem.

2. **The benchmark's rising \(J\) has a short analytic proof.** A4:41–48 currently obtains this sign by a degree-six polynomial and a Sturm count. Candidate 2 proves the sign directly from economically meaningful inequalities, even for dispersed classes satisfying (6). This does not replace A4:50–58's separate certificate for \(\Delta(1-\tau)^2\).

3. **The figure note's endpoint exception is real.** Section 04:302–303 says T is an equilibrium only when an indifferent high-cost challenger may mix. At \(r_A\), T has purchase entry one and exists under C1 as well, explicitly in A4:297 and A4:335–337. The CM-only qualification belongs to the additional T points beyond \(r_A\).

4. **Single crossing can be restricted to an observable economic range.** For every prior, coexistence implies \(\Delta\le2k/\rho\). Any reversal of \(J\) beyond that bound is irrelevant to coexistence at every prior. Candidate 3 formalizes that observation without a global path assumption.

5. **The four-case prior statement needs more than interval topology.** Unique attained threshold crossings, start feasibility, and an interior crossing defining the maximum prior still have to be checked. Candidate 1 avoids those assumptions; Candidate 3 removes only the excessive global condition on \(J\), not those endpoint requirements.

### Calculations and verification boundary

I evaluated the auction formulas directly using Python's standard-library rational arithmetic for exact declared inputs and ordinary floating point for displayed roots and the slot's exponential. The reproducible calculation is `audit/theory_upgrade_2026_10_25/solvers/computations/W1_A/derive_w1.py`; it prints the benchmark thresholds and margins, both counterexamples, and an example with dispersed classes. There are no assertions. The displayed decimal roots are numerical approximations; the proofs of monotonicity, interval topology and the two-component characterization are the algebra above. No test suite, test file, fixture, framework, manuscript build, source edit, stage, or commit was used. No other file in `workarounds/raw/` was read.
