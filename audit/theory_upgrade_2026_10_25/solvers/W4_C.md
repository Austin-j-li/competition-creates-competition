# W4-winner-gap: Solver C

## Candidate 1: Preserve the order–winner association and separate the direct competition effect
Angle: reformulate

Intuition: A purchase is good news about the challenger's class, so it is also good news about winning whenever the high class wins more often. A stronger incumbent lowers both classes' win probabilities, but it need not lower them by the same amount or make their difference larger. The cross-sectional prediction and the fall in win levels are general; only the widening of the purchase–sale winner gap is not.

Formal statement: Define
\[
\Omega(F)=W_H(F)-W_L(F).
\]
In any equilibrium, conditional on preparation,
\[
w_x=\Pr(W\mid X=x,A)=W_L(F)+\mu(x)\Omega(F).
\]
Under full two-sided trade with a fixed prior and slot, \(\mu(-1)=m\), \(\mu(0)=\pi\), and \(\mu(1)=M\). Hence
\[
\boxed{w_1-w_{-1}=(M-m)\Omega(F)\ge0,}
\]
and also \(w_1-w_0=(M-\pi)\Omega(F)\ge0\) and \(w_0-w_{-1}=(\pi-m)\Omega(F)\ge0\). These inequalities are strict exactly when \(\Omega(F)>0\).

A scale-free version uses the prepared-challenger winner odds ratio
\[
\operatorname{OR}_W=\frac{w_1/(1-w_1)}{w_{-1}/(1-w_{-1})}.
\]
Whenever the odds are defined,
\[
\boxed{\operatorname{OR}_W-1=\frac{(M-m)\Omega(F)}{w_{-1}(1-w_1)}\ge0.}
\]
If \(\Omega(F)>0\), the denominator is positive and \(\operatorname{OR}_W>1\); if \(\Omega(F)=0\) and the common win probability is interior, \(\operatorname{OR}_W=1\).

There is also an unconditional level comparative static. If \(F_1\) is stronger than \(F_0\), so that \(F_1(y)\le F_0(y)\) for every \(y\), then \(W_j(F_1)\le W_j(F_0)\) for \(j=H,L\). At any fixed order posterior, therefore,
\[
w_x(F_1)\le w_x(F_0).
\]
Under fixed full orders, all posteriors are interior, so the level fall is strict whenever either class's win probability falls strictly. Strength has an unambiguous direct effect on win levels but an ambiguous effect on their purchase–sale difference.

Finally, at prior \(1/2\), under full orders and post-ceiling entry \(e\equiv\rho\),
\[
\boxed{\operatorname{Cov}(X,\mathbf1_W)=(b+\lambda/2)\rho(M-m)\Omega(F)\ge0.}
\]
It is strictly positive exactly when \(\Omega(F)>0\). Thus orders can predict the winner even when they no longer predict entry, without any monotonicity claim in incumbent strength.

Derivation: First, for a continuous incumbent law and classes whose values all meet the reserve,
\[
W_j(F)=\mathbb E_j[F(\theta)]
=\int \Pr_j(\theta\ge y)\,dF(y)
=\int [1-G_j(y)]\,dF(y).
\]
The left-continuous and right-continuous versions of \(G_j\) differ only on a countable set, which has zero \(F\)-measure. Subtracting the class expressions gives
\[
\boxed{\Omega(F)=\int D(y)\,dF(y)=\mathbb E_F[D(R)]\ge0,}
\]
because \(D=G_L-G_H\ge0\). Moreover, \(\Omega(F)>0\) exactly when \(D>0\) on a set of positive \(F\)-measure.

Preparation depends on the observed price and the independent cost draw, not directly on class. Conditioning on preparation therefore leaves the class posterior at \(\mu(x)\), yielding \(w_x=W_L+\mu(x)\Omega\). The full-order formulas and all three orderings follow immediately. For the odds ratio,
\[
\operatorname{OR}_W-1
=\frac{w_1(1-w_{-1})-w_{-1}(1-w_1)}{w_{-1}(1-w_1)}
=\frac{w_1-w_{-1}}{w_{-1}(1-w_1)}.
\]
For the level comparison, \(F_1(\theta)\le F_0(\theta)\) pointwise implies \(W_j(F_1)\le W_j(F_0)\). For the covariance, full trade at the even prior gives \(\mathbb E[X]=0\) and \(\Pr(X=1)=\Pr(X=-1)=b+\lambda/2\). Since \(\Pr(W\mid X=x)=\rho w_x\) post-ceiling, \(\mathbb E[X\mathbf1_W]=(b+\lambda/2)\rho(w_1-w_{-1})\).

Conditions: The expression for \(w_x\) needs only the model's independence assumptions and a continuous \(F\). The fixed-\((m,\pi,M)\) comparisons need full two-sided trade and a fixed slot; the covariance statement additionally needs prior \(1/2\) and entry \(\rho\) after every order. The weak signs need no extra condition beyond the standing class ranking. Every strict sign must explicitly impose \(\Omega(F)>0\); class ranking alone supplies only \(\Omega(F)\ge0\). No change to the two-point preparation cost is involved.

Benchmark check: Here \(\Omega(r)=1-1/r>0\), \(M=0.7310585786\), \(m=0.2689414214\), and \(M-m=0.4621171573\). At \(r_1=3\),
\[
(w_1,w_{-1})=(0.820705719,\ 0.512627614),
\]
while at \(r_2=3.6\),
\[
(w_1,w_{-1})=(0.805764529,\ 0.472013249).
\]
Both levels fall, but their positive ordering survives. At \(r_2\), entry is at its floor and the covariance is \(0.030344326>0\), matching the manuscript's displayed \(0.030344\).

What is lost: This drops the claim that the winner gap, winner odds ratio, or order–win covariance increases with strength. It replaces that magnitude comparative static with a robust cross-sectional sign, a scale-free odds statement, and a monotone result for win levels. The odds ratio is not a backdoor trend repair: it also falls in the counterexample below.

## Candidate 2: Restore the trend when new incumbent values are more class-separating than average
Angle: primitive condition

Intuition: For a uniform incumbent, the class win-probability gap is the average of \(D\) over the incumbent's possible values. Expanding the support raises that average exactly when class separation at the new upper endpoint exceeds the previous average. The benchmark has maximal separation throughout its relevant upper support; the counterexample adds values at which separation is zero.

Formal statement: Fix full two-sided trade, the prior, and the slot. The purchase–sale winner gap rises between two incumbent laws exactly when \(\Omega\) rises. Two useful primitive versions are:

1. **General FOSD sufficient condition.** If \(D\) is nondecreasing on the union of the compared incumbents' supports, then every FOSD strengthening weakly raises \(\Omega=\mathbb E_F[D(R)]\), and hence weakly widens the winner gap. The rise is strict if the strengthening moves mass across a region where \(D\) strictly rises. A particularly simple special case is that the high class outbids every incumbent on the path: then \(W_H=1\), \(\Omega=1-W_L\), and strengthening weakly lowers \(W_L\).
2. **Exact uniform-family condition.** Let \(F_r=U[0,r]\) and define
\[
\Gamma(r)=\int_0^rD(y)\,dy.
\]
Then
\[
\boxed{\Omega(r)=\frac{\Gamma(r)}{r}.}
\]
For \(r_1>r_0\), the winner gap rises exactly when \(\Gamma(r_1)/r_1>\Gamma(r_0)/r_0\). At a continuity point of \(D\),
\[
\boxed{\Omega'(r)=\frac{rD(r)-\Gamma(r)}{r^2}
=\frac{D(r)-\Omega(r)}{r}.}
\]
Thus the local trend is positive, zero, or negative according as \(D(r)-\Omega(r)\) is positive, zero, or negative. Right derivatives, using the right-continuous function \(D\), give the same test at jumps.

For point-mass classes \(p<\ell<h\), this becomes an exact phase characterization:
\[
\Omega(r)=
\begin{cases}
0, & 0<r\le\ell,\\[2pt]
1-\ell/r, & \ell<r\le h,\\[2pt]
(h-\ell)/r, & r\ge h.
\end{cases}
\]
The gap therefore rises strictly for \(\ell<r<h\) and falls strictly for \(r>h\). The benchmark restriction \(r<h\) is precisely the rising phase; once the incumbent can outbid even the high class, the trend reverses.

Derivation: The general sufficient condition is just the monotone-expectation characterization of FOSD applied to the bounded nondecreasing function \(D\). It is a condition on class separation over incumbent values, not on the preparation cost or the slot. If class densities \(\psi_H,\psi_L\) exist, nondecreasing \(D\) is the local statement \(\psi_L(y)\ge\psi_H(y)\) on the relevant support; atoms are handled directly by the CDFs.

For the uniform family,
\[
\Omega(r)=\int_0^rD(y)\frac{1}{r}\,dy=\frac{\Gamma(r)}{r}.
\]
Differentiating the quotient gives the exact condition. If \(D\) is nondecreasing on \([0,r]\), then \(\Gamma(r)\le rD(r)\), so the uniform sufficient condition is a consequence of the general one. For point masses, \(W_L=1\) for \(r\le\ell\) and \(\ell/r\) thereafter, while \(W_H=1\) for \(r\le h\) and \(h/r\) thereafter; subtracting gives the three phases.

Conditions: The full-order, fixed-slot qualification is what keeps \(M-m\) fixed; without it, the posterior factor must also be differentiated. Monotone \(D\) is sufficient, not necessary. The exact uniform condition is only an endpoint-versus-average comparison and can hold despite interior decreases in \(D\).

A concrete non-necessity example takes \(p=1/2\), \(G_L\) with atoms \(1/2\) at \(1\) and \(1/2\) at \(2\), and \(G_H\) with atoms \(2/5\) at \(3/2\) and \(3/5\) at \(10\). These are ranked classes, but \(D\) successively equals \(1/2,1/10,3/5,0\), so it is not nondecreasing. Nevertheless, for \(2<r<10\),
\[
\Gamma(r)=\frac{3r}{5}-\frac9{10},
\qquad
\Omega(r)=\frac35-\frac{9}{10r},
\]
which rises strictly. Thus imposing monotone \(D\) would discard valid economies; the running-average condition is sharper for the uniform path.

Benchmark check: On the entire benchmark path, \(D(y)=0\) for \(y<1\), \(D(y)=1\) for \(1\le y<10\), and \(r\le r_2=3.6<h=10\). Consequently
\[
\Gamma(r)=r-1,\qquad \Omega(r)=1-\frac1r,
\qquad rD(r)-\Gamma(r)=1>0.
\]
The strict uniform margin is therefore constant and positive; in derivative form, \(D(r)-\Omega(r)=1/r\), equal to \(1/3\) at \(r_1\) and \(5/18\) at \(r_2\). The simpler high-class-dominance margin is \(h-r_2=6.4\). Numerically, the full-order winner gap is
\[
0.4621171573\left(1-\frac1r\right),
\]
which equals \(0.308078105\) at \(r_1=3\) and \(0.333751280\) at \(r_2=3.6\), matching the manuscript.

What is lost: The original trend is retained only on the set where the explicit \(\Omega\) comparison holds. Monotone \(D\), or high-class dominance, is an economically interpretable sufficient restriction but is not necessary. Outside that set, Candidate 1's sign and level statements remain valid, but no general widening claim should be made.

## Importance of the weakness

The counterexample is not economically extreme, and it can be verified as an equilibrium with an interior slot. Take
\[
G_L=\delta_1,\quad G_H=\delta_2,\quad p=\frac12,\quad R\sim U[0,r],\quad r>2,
\]
with
\[
\pi=\rho=\frac12,\qquad \lambda=\beta=\frac14,\qquad k=\frac1{100},\qquad c_H=1.
\]
The high value is only twice the low value, the liquidity probability \(1/4\) is strictly below the structural bound \(1/3\), and the trading cost is the same order of magnitude as the benchmark's \(1/50\). These are ordinary strong-competition parameters, not limiting or near-zero class separation.

Here \(b=3/16\), \(u=4/3\), \(M=7/10\), \(m=3/10\), and
\[
W_H=\frac2r,\qquad W_L=\frac1r,\qquad \Omega=\frac1r,
\qquad \Delta_T=1-\frac{3}{2r}>\frac14.
\]
Thus the target-payoff spread rises with strength even as the winner gap falls. Also
\[
g_L=\frac{3}{8r},\qquad g_H=\frac{15}{8r},\qquad
B(M)=g_L+M(g_H-g_L)=\frac{57}{40r}<\frac{57}{80}<1=c_H,
\]
so high-cost preparation is excluded and entry is \(\rho\) after every order. The exact gross returns to the correct full orders are
\[
K_H=\rho\Delta_T(1-M)=\frac{3\Delta_T}{20},
\qquad
K_L=\rho\Delta_Tm=\frac{3\Delta_T}{20}.
\]
Both exceed \(3/80=0.0375>k=0.01\); wrong-signed orders lose the trading cost. Full two-sided trade is therefore the unique equilibrium order profile throughout this example.

The full-order winner gap is
\[
(M-m)\Omega=\frac{2}{5r},
\]
which falls from \(0.133333\) at \(r=3\) to \(0.100000\) at \(r=4\). The winner odds ratio also falls, from \(1.710059\) to \(1.535117\), while the post-ceiling covariance remains strictly positive at \(1/(16r)\). This cleanly separates the robust empirical sign from the non-robust trend.

For the paper's economics, the weakness is real but limited. The natural empirical test is whether purchases predict a higher acquisition probability than sales, especially when they no longer predict entry; that sign and the associated covariance survive. The main-text winner paragraph (`overleaf/slot/sections/08_empirical.tex:44-50`) is explicitly benchmark-scoped and reports positive gaps and covariance, not a general strength trend. What must be abandoned is a general version of Proposition A.13(ii)'s rising gap and any interpretation that stronger incumbents necessarily make orders more informative about winning. If that trend is economically desired, Candidate 2 states exactly what must be assumed.

## Other findings

The post-ceiling covariance extends to an arbitrary prior without changing its sign. Under full orders and \(e\equiv\rho\),
\[
\boxed{\operatorname{Cov}(X,\mathbf1_W)=2\pi(1-\pi)\rho\lambda\,\Omega(F).}
\]
Indeed, full orders give \(\mathbb E[X]=\lambda(2\pi-1)\), \(\mathbb E[\mu(X)]=\pi\), and \(\mathbb E[X\mu(X)]=\pi\lambda\), so \(\operatorname{Cov}(X,\mu(X))=2\pi(1-\pi)\lambda\). Multiplying by \(\rho\Omega\) gives the formula. At \(\pi=1/2\), it reduces to \(\rho\lambda\Omega/2\), identical to the manuscript's \((b+\lambda/2)\rho\vartheta\Omega\) because \((b+\lambda/2)\vartheta=\lambda/2\).

No additional benchmark error was found in A.13. The needed generalization is to replace \(1-\ell/r\) by \(\Omega(F)\), impose \(\Omega(F)>0\) for strict signs, and confine the rising-gap statement to the benchmark or to Candidate 2's conditions.
