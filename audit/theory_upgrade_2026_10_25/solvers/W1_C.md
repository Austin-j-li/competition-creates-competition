# W1-coexistence-interval: Solver C

## Candidate 1: Coexistence as a reduced-coordinate region
Angle: reformulate

Intuition: Coexistence requires three distinct margins: no trade must be unprofitable, a purchase must be able to recruit, and a recruiting purchase must cover its trading cost. These margins define a fixed region in the \((\Delta,\tau)\) plane, with no path assumption. Incumbent strengthening moves the economy toward larger \(\Delta\) and larger \(\tau\), but nothing in the general model says that it stays in that region forever.

Formal statement: Fix an incumbent law \(F\), ranked classes with \(\Delta>0\) and \(\gamma=g_H-g_L>0\), an interior prior \(\pi\), a slot with \(0<\lambda<1\) and \(0<\beta<1/2\), and rules IM/C1. Write
\[
\kappa_\pi:=\max\{\pi,1-\pi\},\qquad M:=M(\pi),\qquad J:=\Delta(1-\tau).
\]
No informed trade and an informative equilibrium coexist **exactly when**
\[
\boxed{
J\ge k,\qquad \pi<\tau\le M,\qquad \rho\Delta\kappa_\pi\le k.
}
\]
Thus the auction enters only through the fixed reduced region
\[
\mathcal C_\pi:=\left\{(\Delta,\tau):
\Delta\ge \frac{k}{1-\tau},\quad
\pi<\tau\le M,\quad
\Delta\le\frac{k}{\rho\kappa_\pi}\right\},
\]
with \(\Delta>0,\gamma>0\) understood. The informative equilibrium is unique, the low class abstains, and only purchases recruit. Its entry is
\[
\boxed{
\mathsf E=\rho+(1-\rho)
\min\left\{\frac{(1-\pi)b\Delta}{k},\,b+\pi\lambda\right\},
}
\]
which is nondecreasing in \(\Delta\), strictly so while the purchase is mixed.

Two equivalent descriptions make the economics especially plain.

* Holding \(\Delta\) fixed and supposing that no trade is feasible, coexistence holds exactly for the threshold interval
  \[
  \pi<\tau\le \min\{M,\,1-k/\Delta\}.
  \]
  The threshold must be high enough that the prior does not already recruit, but low enough that a purchase can recruit profitably.
* Holding \(\tau\in(\pi,M]\cap(-\infty,1)\) fixed, coexistence holds exactly for the spread interval
  \[
  \frac{k}{1-\tau}\le \Delta\le\frac{k}{\rho\kappa_\pi}.
  \]
  A larger spread makes the recruiting purchase profitable but eventually destroys no trade.

For an interval statement along a path, let the classes, reserve, costs, prior, and slot be fixed while \(F_s\) strengthens. On the positive-threshold domain \(c_H\ge g_L\), FOSD gives \(\Delta\uparrow\) and \(\tau\uparrow\). Consequently,
\[
\{\pi<\tau\}\ \text{is an up-set},\qquad
\{\tau\le M\}\ \text{and}\ \{\rho\Delta\kappa_\pi\le k\}\ \text{are down-sets.}
\]
If \(\{J\ge k\}\) is also an up-set, their intersection—the whole coexistence set—is an interval, possibly empty or a singleton. Monotonicity of \(J\) is sufficient but not necessary. At prior \(1/2\), with continuous coordinates and attained crossings, this becomes
\[
C(1/2)=[s_A,\min\{s_N,s_C\}]\cap\{\tau>1/2\},
\]
intersected with the path domain. Corollary A.2 generalizes at every prior by replacing \(r\ge r_A\) with \(J(F)\ge k\); its interval wording needs the same up-set condition.

Derivation: The argument is the distribution-free content of A4's high-, low-, and product-lemmas.

1. If \(\pi<\tau\), no informed trade leaves entry at \(\rho\). A high-class purchase and a low-class sale then earn \(\rho\Delta(1-\pi)\) and \(\rho\Delta\pi\), respectively. Both are at most \(k\) exactly when \(\rho\Delta\kappa_\pi\le k\).
2. Suppose no trade is feasible. The low class's unique equilibrium sale rate is zero. A high-class purchase that does not recruit earns strictly less than its zero-rate return \(\rho\Delta(1-\pi)\le k\), so an informative equilibrium must recruit after a purchase. Recruitment is feasible precisely when \(\tau\le M\).
3. Let \(s=\lambda\sigma_H(1)\). On recruiting purchase rates,
   \[
   1-\mu_+(s)=\frac{(1-\pi)b}{b+\pi s},
   \]
   which is continuous and strictly decreasing in \(s\). At the first recruiting rate \(s^*\), the gross return is \(\Delta(1-\tau)=J\); at a full purchase it is \(\Delta(1-M)\). Hence some recruiting purchase covers \(k\) exactly when \(J\ge k\). Strict monotonicity gives a unique mixed or full purchase rate.
4. In R, indifference gives \(b+\pi s=(1-\pi)b\Delta/k\); in F, \(s=\lambda\). Since entry after the other orders is \(\rho\), total entry is \(\rho+(1-\rho)(b+\pi s)\), yielding the displayed minimum.
5. Finally, \(\pi<\tau\) is necessary under C1. If \(\pi\ge\tau\), no trade has entry one and requires \(\Delta\kappa_\pi\le k\). Any informative purchase or sale then has strictly smaller residual uncertainty and entry no greater than one, so its gross return is strictly below \(k\).

No uniform incumbent, point-mass class, or monotonicity condition enters these steps.

Conditions: The pointwise statement needs only the listed fixed-\(F\) hypotheses. The path interval additionally needs the scalar monotonicities above and the up-set property of \(\{J\ge k\}\). Continuity and attainment are needed only for closed endpoints and notation such as \(s_A,s_N,s_C\); they are not needed for the defining inequalities. Strict entry growth needs a strict increase in \(\Delta\), not merely FOSD.

Benchmark check: Here \(\pi=1/2\), \(k=1/50=0.02\), \(\rho=1/4\), and \(M=e/(1+e)=0.731058579\). Direct evaluation of the benchmark formulas gives
\[
J(r_0)=\frac{113}{18480}=0.006114719<k,\qquad
J(r_2)=0.252192932>k.
\]
The crossing is \(r_A=1.393957920\), where
\(\Delta=0.055669845\) and \(\tau=0.640739076\). No trade binds at
\[
\Delta(r_N)=\frac{2k}{\rho}=0.16,\qquad r_N=1.747877538,
\]
where \(J(r_N)=0.055285899>k\). The recruitment ceiling is \(r_C=3.592658519>r_N\). Thus the reduced region recovers exactly \([r_A,r_N]=[1.393958,1.747878]\), and the full-purchase threshold is \(r_F=1.467127041\).

What is lost: Without the up-set condition there is no universal ordered-strength interval, no common strength \(r_A\) shared across the prior window, and no benchmark-style closed-endpoint table. The fixed-region statement also does not by itself recover the CM threshold branch's decreasing-entry comparative static. Nothing is lost in the pointwise coexistence criterion, uniqueness, or the entry formula and its monotonicity in \(\Delta\).

## Candidate 2: Impose no downward crossing of \(k\), not global monotonicity
Angle: primitive condition

Intuition: The up-set property only rules out a downward crossing of the trading-cost boundary. It does not require \(J\) to rise everywhere: \(J\) may rise, fall, and still remain above \(k\). At \(J=k\), the derivative test collapses to a simple comparison between spread growth and the loss of high-class gross profit.

Formal statement: Take a compact \(C^1\) FOSD path with \(\Delta>0\) and \(\gamma>0\). Let
\[
A:=\Delta+\gamma=\mathbb E_H\theta-\mathbb E_L\theta>0,
\]
which is constant along the path. Suppose that at every point where \(J(s)=k\),
\[
\boxed{
\mathcal B_k(s):=A k\,\Delta'(s)+\Delta(s)^2 g_H'(s)>0.
}
\]
Then \(\{s:J(s)\ge k\}\) is an up-set. Hence the coexistence set in Candidate 1 is an interval under the other stated scalar conditions. Equivalently, the boundary test is
\[
-\,g_H'(s)<\frac{A k\,\Delta'(s)}{\Delta(s)^2}
\qquad\text{whenever }J(s)=k.
\]
This is a condition on the primitive payoff functions \(G_H,G_L,p,F_s\) and the trading cost, evaluated only on the margin that matters for coexistence.

For global monotonicity, the analogous exact condition on \(X:=g_H-c_H>0\) is
\[
-\frac{g_H'}{X}\le \frac{A}{\gamma}\frac{\Delta'}{\Delta}.
\]
Thus the proportional decline in the high class's **net** rent must not exceed the spread's proportional growth multiplied by \(A/\gamma\). Candidate 2 imposes this comparison only at \(J=k\), where it simplifies to \(\mathcal B_k>0\).

Derivation: First eliminate \(g_L\) and \(\tau\):
\[
1-\tau
=1-\frac{c_H-g_L}{\gamma}
=\frac{g_H-c_H}{\gamma},
\qquad
\boxed{J=\frac{\Delta X}{\gamma},\quad X=g_H-c_H.}
\]
Since \(A=\Delta+\gamma\) is constant, \(\gamma'=-\Delta'\). Differentiating the quotient gives
\[
\boxed{
J'=\frac{A\Delta'X+\Delta\gamma g_H'}{\gamma^2}.
}
\]
Division by \(\Delta\gamma X\) gives the global net-rent elasticity condition above. At a point with \(J=k\), we have \(X=k\gamma/\Delta\). Substitution yields
\[
A\Delta'X+\Delta\gamma g_H'
=\frac{\gamma}{\Delta}\left(Ak\Delta'+\Delta^2g_H'\right),
\]
so at such a point
\[
J'=\frac{\mathcal B_k}{\Delta\gamma}.
\]
Therefore \(\mathcal B_k>0\) is exactly an upward-crossing condition.

To prove the up-set claim, suppose instead that \(J(s)\ge k\) but \(J(t)<k\) for some \(t>s\). Let \(u\) be the last crossing of \(k\) in \([s,t]\). Continuity gives \(J(u)=k\) and \(J<k\) immediately to its right, hence \(J'(u)\le0\). This contradicts \(\mathcal B_k(u)>0\). Strictness also makes every crossing isolated, so the last-crossing argument is valid.

The condition is strictly weaker than monotonicity. For example, on the shifted-uniform family \(R_z\sim U[z-0.1,z+0.1]\), take \(h=10,\ell=1,p=1/2,c_H=2\), \(z\in[1.1,7.5]\), and \(k=1\). Then
\[
\Delta=z-1,\qquad g_H=10-z,\qquad \gamma=10-z,
\qquad J=\frac{(z-1)(8-z)}{10-z}.
\]
Here \(J\) rises to a maximum at \(z=10-\sqrt{18}\) and then falls. Nevertheless, in \(x=z-1\), the equation \(J=1\) is \(x^2-8x+9=0\), whose roots are \(4\pm\sqrt7\). Only the lower root lies on the path; the higher root is \(4+\sqrt7>6.5\). At that sole crossing, \(\mathcal B_1=9-(4-\sqrt7)^2=8\sqrt7-14>0\). Thus the boundary condition holds and \(\{J\ge1\}\) is an up-set even though \(J\) is not monotone.

Conditions: The derivative formulation requires a \(C^1\) path, positive \(\Delta,\gamma\), and the fixed class-mean gap \(A\). At \(J=k>0\), \(X>0\) is automatic. The test is sufficient, not necessary: a tangency at \(J=k\) can preserve the up-set property while giving \(\mathcal B_k=0\). A nondifferentiable path can instead impose directly that every crossing of \(k\) is from below.

Benchmark check: The unique crossing is \(r_A=1.393957920\). There,
\[
\Delta=0.055669845,\qquad
\Delta'=0.242681698,\qquad
g_H'=-0.435670425,\qquad A=9,\quad k=0.02.
\]
Consequently,
\[
Ak\Delta'=0.043682706,\qquad
-\Delta^2g_H'=0.001350200,
\]
and therefore
\[
\mathcal B_k(r_A)=0.042332506>0.
\]
The existing Sturm certificate proves the stronger global monotonicity; Candidate 3 proves it by hand. The numbers here show how much slack the weaker boundary comparison has at the actual coexistence threshold.

What is lost: The condition uses differentiability and a crossing check, and it does not determine the sign of \(J'\) away from \(k\). It supplies the up-set needed for coexistence, not monotone comparative statics for other objects such as the CM threshold branch. It also does not provide closed-form thresholds or the rest of the benchmark's threshold ordering.

## Candidate 3: A cost-cover condition on uniform point-mass paths
Angle: primitive condition

Intuition: \(J\) rises when the spread gain outweighs the proportional loss of high-class net rent. A transparent way to ensure this is to make the high value exceed the strongest incumbent value by at least the preparation cost. In the paper's uniform point-mass environment, that single economic inequality implies strict monotonicity of \(J\).

Formal statement: Let \(G_H=\delta_h\), \(G_L=\delta_\ell\), \(R_r\sim U[0,r]\), and \(0<p<\ell<r<h\). On any strength path \(r\in[r_{\min},r_{\max}]\), suppose
\[
\boxed{r+c_H\le h\quad\text{throughout the path},}
\]
or equivalently \(r_{\max}+c_H\le h\). Then
\[
J'(r)>0\qquad\text{for every }r\in(r_{\min},r_{\max}).
\]
In particular, \(\{J\ge k\}\) is an up-set, and the original coexistence-interval claim holds whenever the remaining conditions in Candidate 1 hold.

Derivation: Write \(A=h-\ell\). For the uniform point-mass economy,
\[
\Delta=\frac{(r-\ell)^2}{2r},\qquad
\gamma=A-\Delta,\qquad
g_H=h-\frac{r^2+p^2}{2r},\qquad
X=g_H-c_H.
\]
Also,
\[
\Delta'=\frac{r^2-\ell^2}{2r^2},\qquad
g_H'=-\frac{r^2-p^2}{2r^2}.
\]
Using the derivative identity from Candidate 2,
\[
\operatorname{sgn}(J')
=\operatorname{sgn}\!\left\{
A(r^2-\ell^2)X-\Delta\gamma(r^2-p^2)
\right\}.
\]
The cost-cover inequality \(r+c_H\le h\) implies
\[
X=h-c_H-\frac{r^2+p^2}{2r}
\ge r-\frac{r^2+p^2}{2r}
=\frac{r^2-p^2}{2r}>0.
\]
It therefore suffices to compare the two remaining terms. Since \(0<\gamma<A\) and \(r>\ell\),
\[
A(r^2-\ell^2)=A(r-\ell)(r+\ell)>\gamma(r-\ell)^2.
\]
Multiplying by \((r^2-p^2)/(2r)>0\) gives
\[
A(r^2-\ell^2)\frac{r^2-p^2}{2r}
>\gamma\frac{(r-\ell)^2}{2r}(r^2-p^2)
=\Delta\gamma(r^2-p^2).
\]
Combining this with the lower bound on \(X\) proves \(J'>0\), including when \(r+c_H=h\).

The exact local condition is weaker. At a given \(r\), \(J'(r)>0\) precisely when
\[
c_H<\bar c(r):=g_H(r)-
\frac{\Delta(r)\gamma(r)(r^2-p^2)}
{(h-\ell)(r^2-\ell^2)},
\]
with weak inequality giving the corresponding weak derivative sign. The cost-cover condition is a simple sufficient bound, not a necessary one.

Conditions: This proof uses both point-mass classes and the uniform-on-\([0,r]\) family. It does not extend verbatim to shifted supports or arbitrary ranked class distributions. It only certifies the missing \(J\)-up-set; the other coexistence and threshold-order hypotheses must still be checked separately.

Benchmark check: The binding point is the strongest incumbent \(r_2=18/5=3.6\):
\[
r_2+c_H=3.6+6=9.6<10=h,
\qquad h-r_2-c_H=0.4.
\]
Thus the benchmark satisfies the sufficient condition with a positive margin of \(2/5\). It follows analytically that \(J\) strictly increases throughout \([6/5,18/5]\), from \(0.006114719\) to \(0.252192932\), crossing \(k=0.02\) once at \(r_A=1.393957920\). This hand argument can replace the degree-six Sturm count used for the \(J'\) component of A4's path lemma; the separate certificate for \(\Delta(1-\tau)^2\) is unaffected.

The simpler condition is materially stronger than necessary. At \(r_2\), the exact local cost bound is
\[
\bar c(r_2)=7.271599981,
\]
so the exact local slack at \(c_H=6\) is \(1.271599981\). By contrast, the sufficient endpoint bound alone would require \(c_H\le h-r_2=6.4\).

What is lost: The condition is confined to the uniform point-mass environment and is conservative. It does not establish monotonicity of \(\Delta(1-\tau)^2\), the full benchmark equilibrium table, or the CM threshold-branch trend. Its payoff is a short economic sufficient condition for the original \(J\)-interval mechanism, including a hand proof at the benchmark.

## Importance of the weakness

The weakness is real for a general FOSD theorem, but it does not disturb the current benchmark-labelled proposition or its calibrated economics. Proposition 3 and Corollary A.2 explicitly restrict themselves to the benchmark path, where monotonicity is certified. The problem arises only if their interval language is lifted to arbitrary ranked classes and incumbent paths without carrying over a crossing condition.

the referee's counterexample is mathematically plain, not a knife-edge or a failure of the maintained class ranking. For \(R_z\sim U[z-0.1,z+0.1]\) with support between \(\ell=1\) and \(h=10\),
\[
\Delta=z-1,\qquad g_H=10-z,\qquad g_L=0,\qquad
\tau=\frac{2}{10-z},
\]
and therefore
\[
J(z)=\frac{(z-1)(8-z)}{10-z},
\qquad
J'(z)=1-\frac{18}{(10-z)^2}.
\]
At \(z=7\) and \(z=7.5\), the respective values are
\[
(\tau,J)=(2/3,2),\qquad (\tau,J)=(0.8,1.3),
\]
while \(J'=-1\) and \(J'=-1.88\). The thresholds are interior and comparable in magnitude to the benchmark's \(0.633\) to \(0.731\). The incumbent distributions are simply narrow uniform shifts, and high-class gross profit remains above the preparation cost. These are reasonable parameter choices, so the general theorem cannot dismiss them.

There is also a clear diagnosis: in this shifted-support family,
\[
J'=1-\frac{c_H(h-\ell)}{\gamma^2},
\]
so \(J\) rises exactly while \(\gamma^2\ge c_H(h-\ell)\). The turning point is \(\gamma=\sqrt{c_H(h-\ell)}=\sqrt{18}\), or \(z=10-\sqrt{18}\approx5.757\). The counterexample lies on the strong-incumbent side of that turning point, where recruitment is approaching its ceiling and net high-class rent is shrinking quickly. This is economically meaningful rather than a numerical singularity.

Two qualifications limit the practical severity. First, the reported points have \(J=2\) and \(1.3\), far above the benchmark trading cost \(k=0.02\); the decline alone does not make \(J\ge k\) fail at that calibration. Second, at the benchmark \(\rho=1/4\) and prior \(1/2\), the no-trade returns at those points would be \(\rho\Delta/2=0.75\) and \(0.8125\), also far above \(k\). Thus those points are not counterexamples to the benchmark's coexistence set: no trade already fails for a different reason. They are counterexamples to unconditional monotonicity, and hence to the proposed general proof strategy.

Overall, this is a moderate generality issue and a small benchmark issue. The central economics—multiplicity from the entry response, a unique coexisting informative branch, and entry increasing with the spread—survives verbatim. What must be abandoned is only the unconditional claim that these margins line up into the same interval on every ordered strength path.

## Other findings

* The identity \(J=\Delta(g_H-c_H)/\gamma\) is useful beyond the proofs above. In particular, \(J\ge k>0\) already implies \(g_H>c_H\) and \(\tau<1\), so \(\tau<1\) need not be imposed separately inside the coexistence region.
* The up-set condition is the right minimal path assumption for the interval intersection. Requiring \(J\) strictly increasing is stronger, and Candidate 2 shows that the difference can matter even on very simple shifted-uniform paths.
* Neither the reduced-region result nor the no-downward-crossing test generalizes A4's additional CM claim that threshold-branch entry falls. That claim separately uses increasing \(J\) and increasing \(\Delta(1-\tau)^2\) (A4's Step 7). Candidate 3 supplies only the first of those two properties.
* The benchmark's cost-cover inequality gives a new hand proof of the \(J\)-monotonicity component of the path lemma. I found no additional substantive error in the scoped coexistence passages.
