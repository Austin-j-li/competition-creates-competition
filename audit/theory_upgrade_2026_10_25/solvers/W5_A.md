# W5-symmetry-tests: Solver A

The best replacement is a **frequency-weighted impact comparison**. It removes the prior from the recruitment diagnostic, keeps auction objects out of that diagnostic, and unifies it with the result about news conveyed by a zero order. The identification result should distinguish a known prior from an unknown prior. Announcement-return positivity needs uncertainty about preparation, rather than a symmetric prior.

Source boundary: the supplied common and W5 briefs; `SCAN.md`, especially Parts 1 and 2; the two named scan reports; and the current manuscript, principally [A8:3–163](../../../../overleaf/slot/appendix/A8_empirical.tex), [A8:195–237](../../../../overleaf/slot/appendix/A8_empirical.tex), [Section 8](../../../../overleaf/slot/sections/08_empirical.tex), [A1](../../../../overleaf/slot/appendix/A1_payoffs.tex), and [A2](../../../../overleaf/slot/appendix/A2_beliefs_trading.tex). The manuscript working copy has HEAD `69c25f4704f30d9b999856d85d3dbafa1e0bee41`, matching the scan. All claims below are derived from these model primitives. The preparation cost remains zero with probability \(\rho\), and \(c_H\) otherwise.

## Candidate 1: Weight the two impacts by how often the orders occur

Angle: both

Intuition: At an asymmetric prior, a purchase and a sale need not move the posterior by the same amount. Their frequency-weighted posterior movements are nevertheless equal and opposite. Weighting the impacts therefore removes class news and leaves the price effect of changes in preparation. The same statistic measures the news conveyed by an opportunity passing without an order.

### Formal statement

Fix any interior prior \(\pi\), general ranked value classes, and an incumbent law with \(\Delta>0\) and \(\gamma=g_H-g_L>0\). Maintain the full two-sided order pattern used in A.11: the informed investor buys in class H and sells in class L. Define observable order frequencies

\[
f_+=\Pr(X=1)=b+\pi\lambda,\qquad
f_-=\Pr(X=-1)=b+(1-\pi)\lambda,\qquad
f_0=1-f_+-f_-.
\]

Use the manuscript's impacts \(I_+=P(1)-P(0)\), \(I_-=P(0)-P(-1)\), and write \(e_+,e_0,e_-\) for preparation probabilities. Let

\[
A_F(\mu)=t_L-t_0+\Delta\mu.
\]

The exact, tie-rule-independent identity is

\[
\boxed{
f_+I_+-f_-I_-
=f_+(e_+-e_0)A_F(M)
-f_-(e_0-e_-)A_F(m).
}
\tag{1}
\]

Under the original default challenger rule C1, this gives an all-prior signed diagnostic:

- The weighted purchase impact exceeds the weighted sale impact exactly when a purchase raises preparation relative to a zero order.
- It is smaller exactly when a sale lowers preparation relative to a zero order.
- They are equal exactly when preparation is constant across the three orders.

The first and second cases cannot occur together under C1: preparation after a zero order is either \(\rho\) or one. Thus this statement needs **no restriction that \(\pi=1/2\), or even that \(\pi<\tau\)**. It preserves the original full-order pattern and default tie rule.

On the economically central region \(B_F(\pi)<c_H\), preparation after a sale and after zero is \(\rho\). Equation (1) becomes the particularly simple diagnostic and magnitude formula

\[
\boxed{
I_+-\frac{f_-}{f_+}I_-
=(e_+-\rho)A_F(M).
}
\tag{2}
\]

Consequently the left side is positive exactly when the purchase recruits a high-cost challenger, including partial recruitment under CM. It equals the entire entry component of the purchase price. With C1, \(e_+-\rho=(1-\rho)\mathbf 1\{B_F(M)\ge c_H\}\).

This comparison uses prices and the purchase/sale frequency ratio. It requires neither the prior, the slot parameters, the preparation floor, nor the auction payoffs to determine the sign.

There is also an exact connection with A.14(iv). If \(P^{\rm pre}=\mathbb E[P(X)]\) denotes the competitive price before the opportunity, then

\[
\boxed{
P^{\rm pre}-P(0)=f_+I_+-f_-I_-.
}
\tag{3}
\]

Under full orders the zero-order posterior is \(\pi\), at every prior. In the purchase-recruitment region it is therefore bad news about preparation and no news about class, with

\[
P(0)-P^{\rm pre}=-f_+(e_+-\rho)A_F(M).
\]

At priors where a zero order already brings certain preparation, the signed interpretation reverses when a sale would deter preparation: zero is then good news about preparation. The original announcement formula extends by replacing \(b+\lambda/2\) with \(b+\pi\lambda\) in the purchase-only recruitment case.

### Derivation

Bayes' rule gives

\[
M=\frac{\pi(b+\lambda)}{f_+},\qquad
m=\frac{\pi b}{f_-},\qquad \mu(0)=\pi.
\]

Subtracting the prior yields

\[
M-\pi=\frac{\pi(1-\pi)\lambda}{f_+},\qquad
\pi-m=\frac{\pi(1-\pi)\lambda}{f_-}.
\tag{4}
\]

Thus \(f_+(M-\pi)=f_-(\pi-m)\), without symmetry of the prior. Since \(A_F\) is affine, write the impacts around preparation after zero:

\[
\begin{aligned}
I_+&=e_0\Delta(M-\pi)+(e_+-e_0)A_F(M),\\
I_-&=e_0\Delta(\pi-m)+(e_0-e_-)A_F(m).
\end{aligned}
\]

Multiply by the corresponding frequencies and use (4), obtaining (1). Full liquidity support gives \(0<m<\pi<M<1\); the class ranking gives \(t_L-t_0\ge0\), so \(A_F(m),A_F(M)>0\). Under C1, if \(e_0=\rho\), then \(e_-=\rho\); if \(e_0=1\), then \(e_+=1\). These facts prove the three sign statements. Equation (3) follows directly by averaging the three conditional prices. It also follows from posterior averaging, \(\sum_x f_x\mu(x)=\pi\).

At a CM tie \(\pi=\tau\), preparation after zero may be interior. Both terms on the right of (1) can then be positive in magnitude and offset each other. The exact identity survives; the three-way sign classification needs C1, or exclusion of this particular tie. Equation (2) remains valid under either rule whenever \(B_F(\pi)<c_H\).

### Announcement returns: the all-prior replacement for strict positivity

This part does not require full orders. Let \(A\) be the event of preparation, let \(f_x=\Pr(X=x)\) for an arbitrary equilibrium, and write \(\Pr(A)=\sum_x f_x e_x\). Cost independence preserves the class posterior conditional on preparation. Therefore

\[
\Delta_x^1=(1-e_x)A_F(\mu_x),\qquad
\Delta_x^0=-e_x A_F(\mu_x).
\]

The no-preparation return is observed only when \(e_x<1\). Averaging both possible reports gives

\[
e_x\Delta_x^1+(1-e_x)\Delta_x^0=0.
\]

The mean return among preparation reports is exactly

\[
\boxed{
\mathbb E[\Delta^1_X\mid A]
=\frac{\sum_x f_x e_x(1-e_x)A_F(\mu_x)}{\Pr(A)}.
}
\tag{5}
\]

With \(\Delta>0\), full liquidity support, and \(0<\rho<1\), every \(A_F(\mu_x)>0\) and every \(e_x\ge\rho>0\). Thus this mean is nonnegative and is **strictly positive exactly when preparation is not already certain**, that is, \(\Pr(A)<1\). This is the unconditional reformulation: it supplies the exact economic boundary, at every prior and under both challenger rules.

A natural primitive sufficient condition retaining A.14's strict-positive claim in every equilibrium is

\[
c_H>B_F(\pi)=(1-\pi)g_L(F)+\pi g_H(F).
\tag{6}
\]

Indeed \(\sum_x f_x B_F(\mu_x)=B_F(\pi)<c_H\), so at least one positive-probability order has \(B_F(\mu_x)<c_H\), hence \(e_x=\rho<1\). No use of \(\pi=1/2\) occurs. Condition (6) is sufficient, not necessary: even when the prior makes preparation profitable, an adverse order can leave preparation uncertain.

### Conditions, including a primitive way to retain the unweighted comparison

Equations (1)–(4) condition on full informed orders, as A.11 does. A simple sufficient condition guaranteeing that order pattern uniquely under either investor tie rule is

\[
\rho\Delta\min\{m(\pi),1-M(\pi)\}>k.
\tag{7}
\]

It forces both correct orders strictly under every candidate, using A2's trading bounds. It also guarantees full orders in a hidden-price counterfactual, so the original same-orders counterfactual can be retained when desired. None of the price identities requires the stronger claim of uniqueness.

The unweighted comparison can itself be retained over a useful nonsymmetric region. Maintain (6), C1, and

\[
\pi\ge\tfrac12,\qquad \rho\le\tfrac12.
\tag{8}
\]

Then \(I_+>I_-\) still holds exactly when a purchase recruits. To see this, without recruitment,

\[
I_+-I_-=
\rho\Delta\,
\frac{\pi(1-\pi)\lambda^2(1-2\pi)}{f_+f_-}\le0.
\tag{9}
\]

With recruitment, \(e_+=1\), and direct subtraction gives

\[
I_+-I_-=(1-\rho)(t_L-t_0)
+\Delta\,[M-2\rho\pi+\rho m]>0,
\]

because \(M>\pi\) and \(2\rho\le1\). Economically, the high class is at least as likely as the low class, and ready buyers assignments for at most half of challengers. This is sufficient, far from necessary: at a recruiting point the exact bound is

\[
\rho<
\frac{t_L-t_0+\Delta M}
{t_L-t_0+\Delta(2\pi-m)}.
\]

At \(\pi=1/2\), any \(\rho<1\) works. Conversely, at \(\pi<1/2\), any no-recruitment full-order state is a false positive for the original strict-positive comparison, by (9). A general prior cannot be accommodated by imposing a condition on auction values alone.

### Benchmark check

The exact benchmark declaration \(\beta=0.294655\), \(u=\exp(1)-1\) gives

\[
\lambda=0.336121768915,\quad b=0.195615040180,\quad
f_+=f_-=0.363675924638,
\]

\[
M=0.731058578630,\qquad m=0.268941421370.
\]

At \(r_1=3\), \(\Delta=2/3\), \(\tau=0.705\), and \(A_F(M)=0.945705719087\). The printed impacts are

\[
I_-=0.038509763105,\qquad I_+=0.747789052420.
\]

Equation (2) recovers the entry component \(0.709279289315\). Equation (3) gives the zero-order discount \(0.257947801368\). At \(r_2=3.6\), recruitment stops and both the adjusted entry component and the discount are zero. The sufficient full-order margin in (7) is \(0.024823570228\) at \(r_1\), and \(0.043126528072\) at \(r_2\).

Condition (6) holds throughout \([6/5,18/5]\) with minimum margin

\[
\min_r\{6-B_r(1/2)\}=1.195833333333.
\]

Equation (5) gives preparation-report means \(0.160591936091\) and \(0.701041666667\) at \(r_1,r_2\), agreeing with the manuscript's six-place displays. Condition (8) holds with readiness margin \(1/2-\rho=1/4\); the benchmark prior is its boundary.

Two off-benchmark checks retain every benchmark primitive except the prior:

- At \(\pi=0.4,r=3.6\), \(M=0.644404982645<\tau=0.731392143349\), so no purchase recruits. Nevertheless \(I_+-I_-=0.009707006968>0\). The weighted statistic is zero. Both correct orders are strict, and the full-order forcing margin is \(0.026228615208>0\).
- At \(\pi=0.9,r=3\), even \(m=0.768030683316\) exceeds \(\tau=0.705\). Every challenger prepares after every order and the preparation-report mean is zero. Full orders constitute an equilibrium: the high purchase and low sale earn net returns \(0.006180200367\) and \(0.492020455544\). This shows why A.14 needs an uncertainty boundary when the prior is generalized.

### What is lost

The impact diagnostic now uses order frequencies as well as prices; no auction knowledge is added. It preserves an exact recruitment diagnostic throughout the region where a price can recruit relative to prior information, and adds a signed deterrence implication outside that region. Under CM at an exact prior-threshold tie, only the decomposition is unconditional. The blanket assertion that the preparation-report mean is strictly positive becomes an exact strictness condition with a straightforward primitive guarantee.

## Candidate 2: Make the identification result about what is known about the prior

Angle: reformulate

Intuition: At a known asymmetric prior, informed trades generate a predictable direction of net order flow, which identifies informed presence. At an unknown prior, that imbalance confounds informed presence with the prevalence of class H. Sale-price impact resolves this confounding and identifies the prior together with the slot. Purchases-only order patterns have a different identification structure that survives asymmetry.

### Formal statement

Under full two-sided informed orders, let

\[
v=f_++f_-,\qquad d=f_+-f_-=\mathbb E[X].
\]

Then

\[
v=2b+\lambda,\qquad d=\lambda(2\pi-1).
\tag{10}
\]

**Known prior.** If \(\pi\ne1/2\), counts identify the slot and the informed share of nonzero orders:

\[
\boxed{
\lambda=\frac d{2\pi-1},\quad
b=\frac{v-\lambda}{2},\quad
\beta=\frac{v-\lambda}{2(1-\lambda)},\quad
\vartheta=\frac\lambda v.
}
\tag{11}
\]

If the known prior equals \(1/2\), the imbalance equation loses its information about \(\lambda\). A.12's count-based nonidentification is precisely this balanced-prior case, conditional on the full-order pattern.

**Unknown prior.** Counts alone generally leave a continuum indexed by \(\lambda\):

\[
\pi=\frac12\left(1+\frac d\lambda\right),\qquad
b=\frac{v-\lambda}{2},\qquad
\beta=\frac{v-\lambda}{2(1-\lambda)}.
\tag{12}
\]

For slot feasibility, \(|d|<\lambda<v<1\) and \(\lambda\ge3v-2\) ensure an interior prior, positive liquidity, and \(\beta\le1/3\). Auction and entry inequalities must also hold. At a point where those inequalities and slot feasibility are strict, they remain true for a neighborhood of this continuum.

Maintain the original price-identification region, \(e_-=e_0=\rho\), with known \(\rho\) and \(\Delta>0\). Define a scalar computed from observed counts and the sale impact:

\[
c=\frac{f_- I_-}{\rho\Delta}>0.
\]

Then prices and counts identify **both the prior and the slot**, at every interior prior:

\[
\boxed{
\lambda=2c+\sqrt{4c^2+d^2},\qquad
\pi=\frac12\left(1+\frac d\lambda\right),\qquad
\beta=\frac{v-\lambda}{2(1-\lambda)}.
}
\tag{13}
\]

The symbol \(c\) here is only a calculated moment, not a preparation-cost parameter; \(c_H\) is unchanged.

**Purchases only.** If L abstains and the effective H-purchase rate is \(s_+=\lambda\sigma_H(1)\), then at every prior

\[
f_+=b+\pi s_+,\qquad f_-=b,\qquad
d=\pi s_+,\qquad v=2b+\pi s_+.
\tag{14}
\]

For known \(\pi\), these give

\[
s_+=\frac d\pi,\qquad b=\frac{v-d}{2}.
\]

If H buys with certainty when informed, \(s_+=\lambda\), and counts identify \(\lambda\) at **every** interior prior, including \(1/2\). If H mixes, counts generally identify only \(s_+\) and \(b\), also at every prior. Moreover the realized informed share of nonzero orders in a purchases-only regime is \(\pi s_+/v=d/v\), which counts identify even without knowing the prior. This share differs from the arrival probability \(\lambda\).

### Derivation

Equation (10) is the sum and difference of the full-order frequencies. It gives (11) and (12) immediately. The restriction \(\beta\le1/3\) becomes

\[
\frac{v-\lambda}{2(1-\lambda)}\le\frac13
\quad\Longleftrightarrow\quad \lambda\ge3v-2.
\]

For price identification, (4) and \(I_-=\rho\Delta(\pi-m)\) imply

\[
c=\pi(1-\pi)\lambda.
\]

Substitute \(\pi=(1+d/\lambda)/2\), obtaining

\[
4c=\lambda-\frac{d^2}{\lambda},\qquad
\lambda^2-4c\lambda-d^2=0.
\]

The unique positive root is (13). At \(d=0\), it reduces to \(\lambda=4c\) and \(\pi=1/2\). Since \(f_-=v/2\), this is exactly the existing symmetric-prior formula \(\lambda=2vI_-/(\rho\Delta)\).

For purchases only, liquidity contributes equal buy and sell masses and informed purchases contribute \(\pi s_+\), giving (14). The persistence of nonidentification on a strictly mixed branch is stronger than a mere parameter count. For fixed \(b,s_+\), the class-conditional order laws, on \((-1,0,1)\), are

\[
f_H=(b,1-2b-s_+,b+s_+),\qquad
f_L=(b,1-2b,b).
\tag{15}
\]

They do not depend separately on \(\lambda\). Change \(\lambda\) within its feasible interior and set \(\sigma_H(1)=s_+/\lambda\), \(\beta=b/(1-\lambda)\). The entire joint class/order law, posteriors, preparation, prices, and deviation payoffs stay fixed. Therefore an interior mixed equilibrium remains an equilibrium. Even adding the price observations does not generally identify \(\lambda\) on this branch.

### Conditions

All identification is conditional on the stated order pattern and a common public state. The full-order count formula cannot be imposed on a mixed or purchases-only equilibrium. Direct count identification needs the prior to be known; (13) replaces that knowledge with the same known \(\rho,\Delta\) required by the manuscript's existing price inversion. When these objects are unknown, (13) is not an identification claim for them as well.

The names and locations of the benchmark's R and F branches do not generalize merely from count algebra. The invariance in (15), however, proves a local nonidentification result whenever such an interior mixed purchases-only equilibrium exists; it is not restricted to a symmetric prior or uniform incumbents.

### Benchmark check

At the benchmark, \(v=0.727351849276\), \(\vartheta=0.462117157260\), and \(d=0\). Counts alone leave the original multiplicity of slots. Using the \(r_1\) sale impact in (13) recovers \(\lambda=0.336121768915\), \(\pi=0.5\), and \(\beta=0.294655\).

At \(\pi=0.6,r=3\), with every other primitive unchanged,

\[
d=0.067224353783,\quad f_-=0.330063747746,
\quad I_-=0.040734163774.
\]

Counts with the known prior give \(\lambda=d/0.2=0.336121768915\). The price inversion in (13), without supplying the prior, recovers the same \(\lambda\), prior \(0.6\), and liquidity probability \(0.294655\). The same inversion recovers prior \(0.4\) in Candidate 1's no-recruitment example.

A nonsymmetric mixed-purchases example uses the benchmark auction at \(r=1.4,\pi=0.6\). The H indifference condition gives

\[
s_+=\frac b\pi\left(\frac{(1-\pi)\Delta}{k}-1\right)
=0.046575009567.
\]

Here \(\mu_+=0.65>\tau=0.640974440895\), \(\mu_0=0.580754953810<\tau\), and a low-class sale earns \(-0.011428571429\). H is indifferent and mixes under IM. Both the original slot and

\[
\lambda'=0.286121768915,\qquad
\beta'=0.274017376721
\]

produce exactly the same conditional order laws. Their H purchase probabilities are respectively \(0.138565882588\) and \(0.162780377541\). In either equilibrium \(d=0.027945005740\), \(v=0.419175086101\), and prices and preparation are identical. Thus the mixed-branch nonidentification survives a moderate asymmetric prior.

### What is lost

The broad slogan that counts cannot identify informed presence must become conditional: it holds under full orders at a known balanced prior, or generally when the prior is unknown, and it survives on mixed purchases-only branches. With a known asymmetric prior under full orders, the paper gains a positive count-identification result instead. Corollary A.3's core conclusions survive with the rescaling \(2\mathbb E[X]\mapsto\mathbb E[X]/\pi\).

Exact identification away from one-half is not uniformly strong identification. With known prior and independent opportunities, the count inversion has

\[
\operatorname{Var}(\widehat\lambda)
=\frac{v-d^2}{n(2\pi-1)^2}.
\]

It becomes imprecise near one-half. Unknown or poorly measured priors also limit the count inversion. This preserves an economic role for price observations without claiming universal count nonidentification.

## Candidate 3: Separate competitive bidding gains from rescuing a failed sale

Angle: both

Intuition: Entry helps the seller in two different ways. It guarantees an admissible buyer when the incumbent misses the reserve, and it increases the price paid when competitive bidding matters. A stronger incumbent reduces the first benefit but increases the second. The competitive-bidding part is monotone without an extra restriction; the total benefit needs those forces compared explicitly.

### Formal statement

Fix the slot and prior, hence a fixed top posterior \(M\). Let the posterior-mixture value law be

\[
G_M=(1-M)G_L+MG_H.
\]

All challenger values meet the reserve. The entry increment decomposes as

\[
\boxed{
A_F(M)=pF(p)+Q_F(M),\qquad
Q_F(M)=\int_p^\infty [1-F(y)][1-G_M(y)]\,dy.
}
\tag{16}
\]

The first term is the value of rescuing an otherwise failed reserve sale. The second is the expected increase in proceeds above the reserve caused by having two admissible bidders.

If \(F_1\le F_0\) is a strengthening, then

\[
\boxed{
Q_{F_1}(M)-Q_{F_0}(M)
\ge M[\Delta(F_1)-\Delta(F_0)]\ge0.
}
\tag{17}
\]

This holds for every continuous FOSD pair and every ranked pair of challenger classes. It is strict whenever the target-payoff spread rises strictly. Thus an unconditional replacement for A.11's trend is: **while purchases recruit, the entry component net of the saved-sale value rises with competitive bidding pressure**. With C1 and full recruitment, the component measured in (2), divided by \(1-\rho\) and then reduced by \(pF(p)\), is exactly \(Q_F(M)\).

To retain monotonicity of the total entry increment, the exact primitive condition for a pair is

\[
\boxed{
\int_p^\infty [F_0(y)-F_1(y)][1-G_M(y)]\,dy
\ \ge\ p[F_0(p)-F_1(p)].
}
\tag{18}
\]

Use a strict inequality for a strict increase. This says that additional competitive payments exceed the loss of entry's insurance against a failed reserve sale. Unlike simply assuming \(A_F(M)\) rises, (18) identifies the two primitive forces and their weights.

Two transparent sufficient specifications are:

1. **The strengthening leaves the probability of meeting the reserve unchanged.** Then \(F_s(p)\) is constant; the right side of (18) is zero. This includes incumbents that always meet the reserve. A strict rise of \(\Delta\) gives strict total growth by (17). It works for arbitrary ranked class distributions and arbitrary continuous FOSD paths satisfying this restriction.
2. **Uniform incumbent expansion with a low reserve.** For \(R\sim U[0,r]\), \(r\ge r_{\min}>p\), suppose all values in both challenger classes are at least \(v_{\min}\), and

   \[
   \min\{v_{\min},r_{\min}\}^2>3p^2.
   \tag{19}
   \]

   Then \(A_{F_r}(\mu)\) rises strictly in \(r\) at every fixed posterior \(\mu\). This is a reserve bound with economic meaning and retains arbitrary ranked class distributions. It includes the benchmark with a nontrivial margin.

The second sufficient condition is not necessary: the exact uniform-family condition uses an average of truncated squared challenger values, derived below. The first is also not necessary, as the benchmark itself shows.

### Derivation

For any admissible challenger value \(\theta\), subtract no-entry proceeds from auction proceeds:

\[
t(\theta)-t_0
=pF(p)+\int_p^\theta[1-F(y)]\,dy.
\]

Average over \(G_M\) to get (16). With \(q(y)=F_0(y)-F_1(y)\ge0\),

\[
Q_{F_1}(M)-Q_{F_0}(M)
=\int_p^\infty q(y)[1-G_M(y)]\,dy.
\]

Since \(1-G_M=1-G_L+MD\ge MD\), this is at least

\[
M\int_p^\infty q(y)D(y)\,dy
=M[\Delta(F_1)-\Delta(F_0)],
\]

proving (17). The change in \(pF(p)\) is \(-pq(p)\), so subtraction gives (18), which is necessary and sufficient for total growth for that pair.

For a uniform incumbent and a fixed value \(\theta\ge p\), the same increment is

\[
t(\theta)-t_0=
\begin{cases}
\displaystyle \frac r2-p+\frac{3p^2}{2r},&\theta\ge r,\\[4pt]
\displaystyle \theta-p+\frac{3p^2-\theta^2}{2r},&p\le\theta\le r.
\end{cases}
\]

The two derivatives agree at \(\theta=r\). Consequently

\[
\frac{\partial A_{F_r}(\mu)}{\partial r}
=\frac{\mathbb E_{G_\mu}[\min\{\theta,r\}^2]-3p^2}{2r^2}.
\tag{20}
\]

The derivative passes through the expectation because it is locally bounded independently of \(\theta\). Equation (20) supplies the exact local sign condition. The lower support bound in (19) makes the numerator strictly positive pointwise, hence at every posterior. If the first-order strengthening also makes \(\Delta\) strict and the full-order pattern persists, both class impacts rise; while recruiting, the entry component, total purchase impact, and total price gap rise as well. The fixed-information class movements \(M-\pi\), \(\pi-m\), and \(M-m\) are all strictly positive.

### Conditions

The decomposition and competitive-part monotonicity require only the standing all-admissible class ranking, a fixed posterior, and a continuous FOSD strengthening. To interpret the competitive part as the adjusted impact in Candidate 1, maintain full informed orders and purchase-only recruitment. The total-increment trend additionally needs (18) for the comparisons of interest; either sufficient specification above supplies it. Strict class-component trends require a strict rise of \(\Delta\). No condition here changes the preparation cost law.

### Benchmark check

For the declared path, \(v_{\min}=\ell=1\), \(r_{\min}=6/5\), and \(p=1/2\). The margin in (19) is

\[
1-3(1/2)^2=1/4.
\]

Equivalently the minimum class value exceeds \(\sqrt3\,p\) by \(0.133974596216\). In the benchmark,

\[
A_r(M)=\frac12-\frac1{8r}
+M\frac{(r-1)^2}{2r},
\]

\[
A_r'(M)=\frac1{8r^2}
+M\left(\frac12-\frac1{2r^2}\right)>0.
\]

The derivative has its minimum at \(r=1.2\) over the declared \([1.2,3.6]\) path; that minimum is approximately \(0.198495060624\). Over A.11's full-order interval beginning at the exact \(r_S\), its lower limiting value is approximately \(0.312221\). The price-increment trend is therefore well separated from zero in the benchmark, rather than an accidental numerical sign.

### Counterexample with the benchmark classes, costs, slot, and prior

The following construction changes only the incumbent path. It makes the reserve channel explicit and avoids a failure of equilibrium existence or recruitment. For \(z\in[0,1]\), let

\[
R_z\sim
\tfrac1{10}U[0.3+0.3z,\,0.4+0.3z]
+\tfrac9{10}U[1.5+0.01z,\,1.7+0.01z].
\tag{21}
\]

Couple the draws using the same mixture component and the same within-component quantile. Every draw increases with \(z\), proving FOSD. The lower component remains below \(\ell=1\); the upper component stays between \(\ell\) and \(h\). Therefore

\[
\Delta(z)=0.54+0.009z
\]

rises strictly. Nevertheless

\[
\begin{aligned}
pF_0(p)&=0.05,& pF_1(p)&=0,\\
(t_L-t_0)_0&=0.5,&(t_L-t_0)_1&=0.465,\\
A_{F_0}(M)&=0.894771632460,&
A_{F_1}(M)&=0.866351159668.
\end{aligned}
\]

The total entry increment falls by \(0.028420472792\). Its competitive part instead rises by

\[
Q_{F_1}(M)-Q_{F_0}(M)=0.021579527208>0.
\]

The minimum full-order forcing margin along the path is \(0.016307091885>0\). At the endpoints, prior gross profit is \(4.28\) and \(4.2605\), below \(c_H=6\); top gross profit exceeds the cost by \(0.234755575210\) and \(0.213176048002\). Profit at a fixed posterior decreases under FOSD, so purchases recruit and the other orders do not throughout the path. The preparation thresholds rise from \(0.703309692671\) to \(0.705833629156\), staying below \(M=0.731058578630\).

Thus this is a unique-full-order equilibrium comparison with recruitment throughout. The entry component falls from \(0.671078724345\) to \(0.649763369751\), and the total price gap falls from \(0.733464540575\) to \(0.713188949585\), even though the class component rises. All original benchmark costs, including \(c_H\), are unchanged.

### What is lost

Without (18), one gives up monotonicity of entry's total contribution to the target price, while preserving monotonicity of its competitive-bidding contribution. The unconditional statement needs the reserve-rescue term measured or specified if one wants to recover it from impacts. Keeping the total trend requires an economically explicit condition; (19) is a particularly clean sufficient condition for the uniform family, and the first sufficient specification works for more general incumbent families.

## Importance of the weakness

**The impact issue is substantial for an empirical extension, but inexpensive to repair.** A prior of 0.4 is moderate, and the false-positive example changes no other benchmark primitive. Equation (9) shows that any prior slightly below one-half also creates a strict false positive in a full-order state without recruitment. Frequency weighting is preferable to imposing exact prior symmetry: the data already contain the needed frequencies, and the correction does not require estimating a prior or auction primitives. Equations (1) and (3) also add an economically useful deterrence interpretation at high priors.

**The count-identification issue changes the theorem's content.** Exact nonidentification under full orders with a known prior is a balanced-prior rank failure. An asymmetric prior gives a better positive identification theorem, while an unknown prior restores genuine count ambiguity. Priors near one-half give weak count information in finite samples. The paper can state these distinctions plainly and retain a role for prices. Corollary A.3's purchases-only identities and its mixed-branch nonidentification are not fundamentally symmetry-dependent.

**The announcement issue is a strictness condition rather than a mechanism failure.** Both the zero conditional mean and the nonnegative preparation-report mean extend to every prior. Strict positivity needs preparation to remain uncertain. A prior of 0.9 is high but economically intelligible and produces a zero mean with all other benchmark parameters unchanged. Condition (6) is natural, has a large benchmark margin, and makes the original strict-positive statement valid in every equilibrium without imposing a symmetric prior.

**The price-increment trend has a separate economic limitation.** Construction (21) is deliberately transparent rather than a proposed calibration, but it does not use extreme costs, tiny trading-cost slack, reversed class ranking, or vanishing recruitment. Only ten percent of incumbent draws cross the reserve, while the remaining draws strengthen slightly. The failure reflects a real distinction between improving competitive bids and reducing the need for another bidder to make a sale possible. It does not undermine rising \(\Delta\), informative prices, or the entry mechanism. It does undermine a universal claim that all components of execution-price impacts grow with incumbent strength.

## Other findings (errors in the manuscript, anything surprising)

1. **The current A8 and Section 8 explicitly impose the benchmark and prior one-half.** Their statements are not false on that stated scope. The changes above are needed when upgrading the paper to the general class model; they should not be described as invalidating the existing benchmark calculations.

2. **The informed share and posterior gap should be separated at general priors.** Under full orders the realized informed share is always \(\lambda/v\). The convenient equality \(\lambda/v=M-m=2M-1\) is specific to one-half. For example, at prior 0.6 the posterior gap is \(0.447454669331\), while the informed share remains \(0.462117157260\). Generalizing A.11 by retaining the symbol \(\vartheta\) simultaneously for these objects would silently introduce another error. The general class component is \(\rho\Delta(M-m)\), not \(\rho\Delta\lambda/v\).

3. **A positive mean preparation-announcement return does not identify price-induced recruitment.** With no recruitment at all and \(e(x)\equiv\rho\), (5) becomes

   \[
   \mathbb E[\Delta^1_X\mid A]=(1-\rho)A_F(\pi)>0.
   \]

   At the benchmark's post-ceiling \(r_2\), this mean is \(0.701041666667\), larger than the recruiting-state mean at \(r_1\). This is consistent with the manuscript, but it matters when presenting empirical implications: the frequency-weighted impact comparison isolates an entry response to order information, whereas preparation-announcement positivity by itself does not.

4. **CM ties should be handled at the observed entry probabilities.** Equations (1), (2), and (5) do that automatically. A binary recruitment indicator should not replace \((e_+-\rho)/(1-\rho)\) at a partially recruiting top-posterior tie. At a prior-threshold tie the signed decomposition in (1) is the appropriate statement.

5. **Ceilings and hidden-price comparisons still need their own hypotheses.** A downward jump at a unique ceiling requires continuous auction payoffs, a crossing of \(B_F(M)-c_H\), persistence of full orders on both sides, and the specified tie rule. Frequency weighting does not supply these conditions. Condition (7) is a convenient way to preserve full orders in the visible and hidden economies. Along a fixed-slot FOSD path, \(B_F(M)\) is nonincreasing; strict spread growth makes its decline strict because \(1-G_H\ge D\) and \(M>0\), so there is at most one crossing, with existence still requiring the endpoint inequalities.

Numerical work: `audit/theory_upgrade_2026_10_25/solvers/computations/W5_A/calculate.py` was run through Python's CLI, and its printed output is saved at `audit/theory_upgrade_2026_10_25/solvers/computations/W5_A/calculation_output.txt`. It uses 55-digit decimal arithmetic, the exact declared decimal liquidity probability, a decimal exponential for the slot ratio, and analytic piecewise-linear auction integrals for each uniform component. The printed benchmark prices and announcement means agree with `numbers.tex`; the off-benchmark cases print posteriors, entry probabilities, impacts, preparation-report means, and investor payoffs. These calculations are numerical illustrations supporting the displayed algebra, not interval certificates or new release results.
