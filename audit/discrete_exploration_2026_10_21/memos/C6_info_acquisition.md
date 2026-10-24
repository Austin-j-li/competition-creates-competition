# C6. Costly information acquisition

## 1. Question

Does a stronger incumbent raise the return to research before trade?
Can hidden acquisition create several equilibria and raise entry?
Can this choice repair the equal-noise model's information problem?

**Answer.** Hidden research creates robust coexistence under discrete-Laplace noise, with a suitable preparation cost.
It does not create feedback under equal noise.
Research can raise entry, but its private return does not measure its social value.

## 2. Setup

This memo modifies both the equal-noise model and the discrete-Laplace model.
The first model isolates the failure of feedback.
The second model permits feedback without off-path flows.

### Primitives and timing

Nature draws class $J\in\{H,L\}$, with $\Pr(H)=\pi$.
The benchmark class distributions put all mass at $h$ and $\ell$.
The investor pays $\kappa>0$ before it observes the quality class.
Without acquisition, it does not trade.
The main case keeps acquisition private.
The equilibrium probability of acquisition is $\psi$.

After acquisition, the investor chooses $q\in\{0,1\}$ and pays $kq$, where $k>0$.
It has no initial stake.
The market observes $X=q+Z$ and sets the competitive price.
The challenger sees the price and its independent preparation cost.
Preparation reveals the challenger's exact value and permits a truthful auction bid.

The potential investor is always present before its acquisition choice.
Thus this memo sets exogenous presence to one.
The probability $\psi$ concerns acquisition, rather than exogenous presence.
For positive acquisition, its effect on flow equals an informed presence probability.

The auction has $R\sim U[0,r]$ and $0<p<\ell<r<h$.
The low preparation cost is $c_L=0$, with probability $\rho\in(0,1)$.
The other cost is $c_H>0$.
The main derivation imposes $B_r(\pi)<c_H$.
The benchmark has $\pi=1/2$.

The auction objects match equation (4) in the pinned manuscript:

$$
\begin{aligned}
t_0&=p(1-p/r),&t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&\Delta_T&=(r-\ell)^2/(2r),\\
g_H&=h-r/2-p^2/(2r),&g_L&=(\ell^2-p^2)/(2r),\\
B_r(\mu)&=g_L+\mu(g_H-g_L),&
e_r(\mu)&=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\}.
\end{aligned}
$$

These formulas use $c_L=0$, rather than the manuscript's $c_L=1$.
The research cost does not enter the challenger's preparation cost.

### Equilibrium, beliefs, and ties

The equilibrium concept is perfect Bayesian equilibrium with competitive prices.
It includes the initial acquisition choice and both orders after acquisition.
Each unilateral deviation faces the candidate price and preparation schedules.
An acquisition deviation can choose its later order separately in each class.

On-path beliefs follow Bayes' rule.
In the equal-noise model, set $\Pr(H\mid X=2)=1$ when $\psi=0$.
This completion equals the limit under positive research and high-class purchases.
No other feasible flow needs an off-path belief.
Every integer flow has positive probability under discrete-Laplace noise, even without research.

The investor chooses zero at a trade tie.
The challenger prepares at a preparation tie.
At an acquisition tie, the investor may mix between acquisition and no acquisition.
This last convention permits an interior $\psi$.
It does not alter the rule at a trade tie.

Write $w_L=t_L-t_0>0$.
For any candidate price $P$, its induced entry probability $e(P)\ge\rho$ is fixed.
Competitive prices satisfy

$$P=t_0+e(P)[w_L+\Delta_T\mu_X],\qquad
\mu_X=\frac{P-t_0-e(P)w_L}{e(P)\Delta_T}.$$

Thus the raw posterior is a function of price.
Its average over all flows with that price equals the same posterior.
The challenger therefore recovers $\mu_X$ from price alone.
The resulting price function is

$$P_r(\mu)=t_0+e_r(\mu)(w_L+\Delta_T\mu).$$

For $\mu_2>\mu_1$, its difference is

$$
P_r(\mu_2)-P_r(\mu_1)
=e_r(\mu_2)\Delta_T(\mu_2-\mu_1)
+[e_r(\mu_2)-e_r(\mu_1)](w_L+\Delta_T\mu_1)>0.
$$

The first term is at least $\rho\Delta_T(\mu_2-\mu_1)$.
The second term is nonnegative.
Thus price reveals the posterior, including at price atoms.
The positive floor also excludes alternative pools of distinct posteriors.

The manuscript source is commit `9b9bf3ce1a94d5017042192e61c9ceb800d310ba`, `main.tex`, Sections 2–4 and Appendix A.
Its `online_appendix.tex`, A.9, supplies the welfare identity used below.

## 3. Results

### Proposition C6.1 — analytical: reduction to one acquisition choice

Let $\beta$ denote the high-class purchase probability after acquisition.
Set $s=\psi\beta$.
The low-class investor never buys.
Every equilibrium with $\psi>0$ has $\beta=1$, so $s=\psi$.

**Proof.** At any flow, the two residuals from a purchase are

$$V_H(x)-P(x)=e(x)\Delta_T[1-\mu(x)],\qquad
V_L(x)-P(x)=-e(x)\Delta_T\mu(x).$$

A low-class purchase earns at most $-k<0$.
It therefore loses to zero under every schedule.
Let $D_r(s)$ denote the high-class gross return from one purchase against the fixed schedule induced by $s$.
Its net return is $D_r(s)-k$.
The gross value of access to information is

$$\boxed{V_r(s)=\pi[D_r(s)-k]_+.}$$

Here “gross” means before the research cost, but after the trade cost.
Without research, the investor's payoff is zero by the no-trade restriction.
If the high class mixes at a trade tie, its net return is zero.
Then $V_r(s)=0<\kappa$, so acquisition cannot occur.
Positive acquisition therefore requires a strict high-class purchase, which gives $s=\psi$.

The complete acquisition conditions are

$$
\boxed{\begin{array}{rcl}
\psi=0&\Longleftrightarrow&\kappa\ge V_r(0),\\
0<\psi<1&\Longleftrightarrow&\kappa=V_r(\psi),\\
\psi=1&\Longleftrightarrow&\kappa\le V_r(1).
\end{array}}
$$

Each row is a condition on that candidate, rather than an exclusive case across candidates.
For the first row, a deviation pays for information and then uses its optimal order.
For the middle row, acquisition yields zero net surplus and the high-class purchase remains strict.
For the last row, acquisition weakly dominates no acquisition.
The residual formulas verify all feasible later orders.
The stated price construction verifies market and challenger choices. $\square$

With multiplicity, $V(r)$ needs a schedule or an equilibrium selection.
The object $V_r(s)$ makes that dependence explicit.

### Proposition C6.2 — analytical: equal noise adds a research cutoff, but no feedback

Suppose $Z\in\{-1,0,1\}$ has equal probabilities.
For every $s>0$, Bayes' rule gives

$$
\begin{array}{c|cccc}
x&-1&0&1&2\\ \hline
\Pr(H\mid x)&\displaystyle\frac{\pi(1-s)}{1-\pi s}&\pi&\pi&1.
\end{array}
$$

The conditional flow probabilities are $(1-s,1,1,s)/3$ in class $H$.
They are $(1,1,1,0)/3$ in class $L$.
A purchase reaches $0,1,2$, each with probability $1/3$.
Only the first two flows give a positive information rent.
Consequently,

$$
D_r(s)=\frac23 e_r(\pi)(1-\pi)\Delta_T,
\qquad
\boxed{\overline V_3(r)=\pi\left[\frac23\rho(1-\pi)\Delta_T(r)-k\right]_+.}
$$

The second formula uses $B_r(\pi)<c_H$.
The off-path completion gives the same purchase return at $s=0$.
Thus $V_r(s)=\overline V_3(r)$ for every $s\in[0,1]$.

Proposition C6.1 now gives

$$
\psi=\begin{cases}
1,&0<\kappa<\overline V_3(r),\\
\text{any value in }[0,1],&\kappa=\overline V_3(r)>0,\\
0,&\kappa>\overline V_3(r).
\end{cases}
$$

There is no robust coexistence and no strict complementarity.
At the knife-edge cost, the continuum follows from exact acquisition indifference.
Additional entry at flow $2$ cannot raise research rents because that flow reveals the class completely.

Since $\Delta_T'(r)>0$, research incentives rise with $r$ while entry at the prior remains $\rho$.
The exact strength cutoff is $r_\kappa=\mathfrak r(d_\kappa)$, where

$$
d_\kappa=\frac{3(k+\kappa/\pi)}{2\rho(1-\pi)},
\qquad
\mathfrak r(d)=\ell+d+\sqrt{d^2+2\ell d}.
$$

To derive the inverse, set $(r-\ell)^2=2rd$.
The resulting quadratic has the stated root above $\ell$.
The strength cutoff applies when this root lies below $h$.

If $B_r(\pi)<c_H\le g_H(r)$, the outcomes are

$$
\boxed{\mathsf E=\rho+(1-\rho)\frac{\pi\psi}{3},\qquad
\mathsf O_H=\pi\rho+(1-\rho)\frac{\pi\psi}{3}.}
$$

If $c_H>g_H(r)$, both additional terms vanish.
An interior $\psi$ grades only the bad-news posterior.
Both middle flows still equal the prior, and the top flow still reveals $H$.
Thus endogenous acquisition does not smooth the profitable good-news experiment. $\square$

### Proposition C6.3 — analytical: discrete-Laplace cutoffs and robust coexistence

Let $a=e^{-1/b}\in(0,1)$ and $d=1-a$.
Write $n(z)=(1-a)a^{|z|}/(1+a)$.
The ratio $n(x-1)/n(x)$ equals $a$ for $x\le0$ and $1/a$ for $x\ge1$.
The two conditional flow laws are

$$f_H(x)=(1-s)n(x)+sn(x-1),\qquad f_L(x)=n(x).$$

Set $y=\pi d s$.
Bayes' rule gives two posteriors:

$$
\boxed{\mu_-(s)=\frac{\pi(1-ds)}{1-y},\qquad
\mu_+(s)=\frac{\pi(a+ds)}{a+y}.}
$$

For a deviating purchase, the probabilities of these regions are $a/(1+a)$ and $1/(1+a)$.
Use $1-\mu_-=(1-\pi)/(1-y)$ and $1-\mu_+=(1-\pi)a/(a+y)$.
Then

$$
\boxed{D_r(s)=C_r\left[\frac{e_-}{1-y}+\frac{e_+}{a+y}\right],\qquad
C_r=\frac{\Delta_T(1-\pi)a}{1+a},\quad e_\pm=e_r(\mu_\pm(s)).}
$$

This sum covers the infinite noise support exactly.
It does not require truncation.

Now set $\pi=1/2$ and retain $B_r(1/2)<c_H$.
The lower region always has $e_-=\rho$.
Define

$$
m=\frac{a}{1+a},\quad M=\frac1{1+a},\quad
\tau=\frac{c_H-g_L}{g_H-g_L}.
$$

If $\tau>M$, the upper region also has $e_+=\rho$ for every $s$.
If $1/2<\tau\le M$, its entry threshold is

$$\boxed{s_E=\frac{a(\tau-\pi)}{\pi d(1-\tau)}\in(0,1].}$$

Indeed, $\mu_+\ge\tau$ is equivalent to
$\pi a+\pi ds\ge\tau a+\tau\pi ds$.
Collect the terms in $s$ to obtain the cutoff.
At $s=s_E$, the challenger tie rule gives $e_+=1$.

Within a region of fixed entry rates,

$$
\frac{dD_r}{ds}
=C_r\pi d\left[\frac{\rho}{(1-y)^2}-\frac{e_+}{(a+y)^2}\right].
$$

For $s\le1$ and $\pi=1/2$, we have $1-y\ge a+y$ and $e_+\ge\rho$.
Thus the derivative is negative in each open region.
With $e_+=\rho$, it reaches zero only at the endpoint $s=1$.
At the entry threshold, the gross return jumps upward by

$$D_r(s_E)-D_r(s_E^-)=\frac{C_r(1-\rho)}{a+\pi d s_E}>0.$$

Research therefore has a discrete complementarity through entry.
Within each entry regime, greater expected research instead reduces its private return.

Define the untruncated branch values

$$v(s;e)=\pi\left\{C_r\left[\frac{\rho}{1-\pi ds}+\frac e{a+\pi ds}\right]-k\right\}.$$

For $0<s_E<1$, write

$$v_0=v(0;\rho),\quad v_E^-=v(s_E;\rho),\quad
v_E^+=v(s_E;1),\quad v_1=v(1;1).$$

The exact cost conditions are:

- No research exists iff $\kappa\ge\max(v_0,0)$.
- Full research exists iff $0<\kappa\le v_1$.
- A unique root below $s_E$ exists iff $v_E^-<\kappa<v_0$ and $\kappa>0$.
- A unique root in $[s_E,1)$ exists iff $v_1<\kappa\le v_E^+$ and $\kappa>0$.

Each root solves $v(s;e)=\kappa$ on its stated branch.
The strict lower-branch endpoint follows from entry at equality.
The weak upper-branch endpoint includes $s=s_E$.
The full-research corner includes its acquisition tie.

These cutoffs give at most two distinct acquisition equilibria.
The lower branch can supply either its interior root or the zero corner, but not both.
The upper branch can supply either its interior root or the full corner, but not both.
If $v_1>v_0>0$, both corners coexist throughout $\kappa\in[v_0,v_1]$.
The strict interval $(v_0,v_1)$ gives robust coexistence.
This recovers coexistence, but it does not establish the paper's ordering across three strengths.

The benchmark coexistence example also has an exact proof.
Take $r=3$, $c_H=5$, and $\kappa=1/20$.
The bounds $3/5<a<2/3$ follow from the exponential series; C6.4 gives the lower bound.
The upper bound follows from $e^{1/2}>1+1/2$.
Hence $M>3/5>117/200=\tau$, so full research induces expensive entry.
At this strength,

$$v_0=\frac{19}{600}<\frac1{20},\qquad
v_1=\frac5{12}\frac{a}{(1+a)^2}-\frac1{100}
>\frac{25}{256}-\frac1{100}>\frac1{20}.$$

The bound uses the positive derivative of $a/(1+a)^2$ for $a<1$.
Thus both corners exist with strict acquisition incentives.

There is also an explicit quadratic for each interior root.
Set $L=k+\kappa/\pi$ and $y=\pi ds$.
Multiply the branch equation by $(1-y)(a+y)$:

$$L[a+dy-y^2]=C_r[\rho a+e+(\rho-e)y].$$

Thus retain the roots of

$$
\boxed{Ly^2+[C_r(\rho-e)-Ld]y+C_r(\rho a+e)-La=0}
$$

that lie in the stated branch.
This formula and the endpoint conditions give exact cutoffs in $\kappa$.
They also verify both later trade decisions through Proposition C6.1.

If $\tau>M$, there is one decreasing branch and a unique acquisition equilibrium.
It equals zero for $\kappa\ge\max(v(0;\rho),0)$.
It equals one for $0<\kappa\le v(1;\rho)$.
Otherwise it is the unique interior root.
The same threshold rules cover $s_E=1$, with the upper region reduced to its endpoint. $\square$

### Proposition C6.4 — analytical: the original cost of six blocks recruitment under discrete-Laplace noise

Retain $(h,\ell,p,b)=(10,1,1/2,2)$, $\pi=1/2$, and $c_H=6$.
No acquisition probability can induce expensive entry for any $r\in(1,10)$.

**Proof.** Every feasible posterior is at most $M=(1+e^{-1/2})^{-1}$.
At $r=1$, the limit of the gross profit is

$$B_1(M)=\frac38+9M.$$

For $n\ge2$, successive terms of the series for $e^{1/2}$ have ratio at most $1/6$.
Therefore

$$e^{1/2}\le1+\frac12+\frac{1/8}{1-1/6}=\frac{33}{20}<\frac53.$$

This gives $a>3/5$, hence $M<5/8$ and $B_1(M)<6$.
Both auction profits fall strictly with $r$.
Thus $B_r(\mu)\le B_r(M)<B_1(M)<6$ for $r>1$.
The challenger never prepares at cost $c_H$, so the one-branch case applies. $\square$

This is a documented failure of acquisition as a repair at the original cost of six.
The feedback examples below use $c_H=5$, as in the brief's candidate.
All auction values remain at the benchmark.

### Proposition C6.5 — analytical: a Proposition 2 analog with endogenous research

Use discrete-Laplace noise, $\pi=1/2$, and strengths $r_0<r_1<r_2$.
The following sufficient conditions give unique acquisition outcomes:

$$
\begin{gathered}
\Delta_T(r_0)<k,\qquad
0<\kappa<\frac12[\rho m\Delta_T(r_1)-k],\\
B_{r_0}(1/2)<c_H<B_{r_1}(M),\qquad B_{r_2}(M)<c_H.
\end{gathered}
$$

The first strength has no research and entry $\rho$.
The second strength has full research and entry $(1+\rho)/2$.
The third strength has full research and entry $\rho$.
High-class ownership rises strictly between the first two strengths.

**Proof.** A high-class purchase earns no more than $\Delta_T(r_0)-k<0$ at the first strength.
Thus acquisition loses $\kappa$ there under every candidate schedule.

At the second strength, every posterior lies in $[m,M]$.
The residual at every flow is at least $\rho m\Delta_T(r_1)$.
Hence the value of acquisition exceeds $\kappa$ against every schedule induced by any $s$.
This excludes zero and mixed acquisition and forces $\psi=1$.
The high-class order is then strictly one.

With full research, the two posteriors are $m$ and $M$.
Their unconditional probabilities are exactly $1/2$ each.
The lower posterior does not induce expensive entry because $B_r(m)<B_r(1/2)<c_H$.
The upper posterior does induce that entry at $r_1$.
Thus

$$\mathsf E_{r_1}=\rho+\frac{1-\rho}{2},\qquad
\mathsf O_{H,r_1}=\frac\rho2+\frac{1-\rho}{2(1+a)}>\frac\rho2.$$

At $r_2$, the larger spread preserves the strict research bound.
The upper posterior cannot induce expensive entry because $B_{r_2}(M)<c_H$.
Thus entry and high-class ownership return to $\rho$ and $\rho/2$.
The price is still informative. $\square$

At fixed $s$, $V_r(s)$ rises with $r$ within each entry regime.
Only $\Delta_T$ changes in the gross trade return there, and its derivative is positive.
At an interior acquisition equilibrium in such a regime, implicit differentiation gives

$$\frac{d\psi}{dr}=-\frac{\partial V_r(\psi)/\partial r}{\partial V_r(\psi)/\partial\psi}>0.$$

The numerator is positive and the denominator is negative by C6.3.
However, stronger competition can remove expensive entry and cause a downward jump in $V_r(s)$.
Thus “competition creates research” is a local force and a valid reversal, rather than a global monotonicity result.

### Proposition C6.6 — analytical: public acquisition removes the hidden-probability feedback

Suppose acquisition is public before trade.
Conditional on acquisition, prices use the acquired continuation, rather than a mixture with absence.
Suppose this continuation has a unique strict high-class purchase.
Then its research value is

$$\boxed{V_r^{\rm public}=\pi[D_r(1)-k]>0.}$$

Acquisition is full if $\kappa<V_r^{\rm public}$ and zero if $\kappa>V_r^{\rm public}$.
Every acquisition probability is possible at equality.

**Proof.** The acquisition flag is independent of class, so it does not itself change the prior.
After acquisition, the market knows that informed trade is available.
The strict continuation has $\beta=1$ and uses the schedule for $s=1$, whatever the initial $\psi$.
Before acquisition, the investor therefore compares the fixed value $V_r^{\rm public}$ with $\kappa$.
The stated choices follow. $\square$

The uniform bound in Proposition C6.5 also guarantees the required unique strict continuation.
It holds at $r=3$ in the example below.
At $\kappa=0.05$, public acquisition selects full research there, while hidden acquisition permits both corners.
Equal noise has the same research return under public and hidden acquisition.
If the acquired continuation itself has several equilibria, public acquisition still needs a continuation selection.

### Proposition C6.7 — analytical: welfare equals the entry gain less resource costs

Compare research equilibrium $\psi$ with no research at the same $r$.
Without research, only the zero-cost challenger prepares.
Let $\xi=1$ if $k$ is a resource cost and $\xi=0$ if it is a transfer.
Then

$$
\boxed{\Delta\mathcal W
=(1-\rho)\mathbb E\left[\mathbf1\{B_r(\mu_X)\ge c_H\}
\left(B_r(\mu_X)-c_H+\frac{p^2}{r}\right)\right]
-\psi\kappa-\xi\pi\psi k.}
$$

**Proof.** Without entry, allocation value is $R\mathbf1\{R\ge p\}$.
With challenger value $\theta>p$, allocation value is $\max(R,\theta)$.
Their difference satisfies

$$\max(R,\theta)-R\mathbf1\{R\ge p\}
=(\theta-\max(p,R))_++p\mathbf1\{R<p\}.$$

Condition on the price posterior and the preparation cost.
The incumbent retains its independent uniform law.
The conditional allocation gain from extra preparation, net of its cost, is therefore
$B_r(\mu_X)-c_H+p^2/r$.
Average over the added expensive-entry events.

Subtract the research expenditure $\psi\kappa$.
The high class alone trades, with unconditional probability $\pi\psi$.
Subtract its trade cost when that cost uses resources.
All auction and financial transfers cancel. $\square$

For equal noise, with recruitment, this reduces to

$$\Delta\mathcal W_3
=\psi\left[\frac{(1-\rho)\pi}{3}
\left(g_H-c_H+\frac{p^2}{r}\right)-\kappa-\xi\pi k\right].$$

For discrete-Laplace noise, define

$$Q_+(\psi)=\frac{a+\pi d\psi}{1+a}.$$

This is the unconditional probability of upper flows.
When $\psi\ge s_E$, the outcomes and welfare are

$$
\begin{aligned}
\mathsf E&=\rho+(1-\rho)Q_+(\psi),\\
\mathsf O_H&=\pi\rho+(1-\rho)\frac{\pi(a+d\psi)}{1+a},\\
\Delta\mathcal W_D&=(1-\rho)Q_+(\psi)
\left[B_r(\mu_+(\psi))-c_H+\frac{p^2}{r}\right]
-\psi\kappa-\xi\pi\psi k.
\end{aligned}
$$

Below $s_E$, the added entry term vanishes.
Research then has strictly negative social value for every $\psi>0$.
Private rents can persist because informed profits are transfers from other market participants.


## 4. Relation to the Laplace paper

### Results that survive, change, or remain open

| Paper result | C6 conclusion |
|---|---|
| Proposition 1 | Survives. The auction and its two comparative statics remain the same. |
| Proposition 2(i)–(ii) | Equal noise adds an exact research cutoff. Discrete-Laplace gives the strict sufficient research bound in C6.5. |
| Proposition 2(iii) | Equal noise retains the remote posterior-one ceiling. Discrete-Laplace retains its bounded ceiling. |
| Proposition 3 | Robust coexistence returns under discrete-Laplace noise at $c_H=5$. Equal noise gives only a cost knife edge. |
| Proposition A.3 | Survives at fixed acquisition probability and conditional orders. Endogenous acquisition changes that experiment. |
| Proposition A.4 | Changes. Acquisition costs add the cutoffs $V_r(0)$, $V_r(1)$, and both entry-threshold limits. |
| Proposition A.5 | Open for this extension. The logistic continuation and acquisition correspondence require a separate derivation. |
| Proposition A.6 | Open. Atomless preparation costs replace the entry jump with a continuous response. |
| Proposition A.7 | Open. Complementary private information changes the value of research and the entry rule. |
| Proposition A.8 | The auction comparison remains separate. Alternative payment rules change the research spread. |
| Proposition A.9 | Each additional entry retains a positive conditional allocation gain. Net welfare can fall after research costs. |
| Proposition A.10 | Its distinct-posterior pools are absent here because the entry floor is strictly positive. |
| Sections 5–6 | Robustness remains open; C6.7 supplies the extra welfare terms. Reserve choice remains fixed. |

Acquisition does not recover the paper's endogenous asymmetry between purchases and partial sales.
The buy-only restriction removes sales before any optimization.
An interior $\psi$ changes the frequency of informed participation, rather than its order size.
The high-class investor still buys one unit whenever it acquires information.

Under discrete-Laplace noise, interior research does grade both posteriors.
They move continuously from the prior toward $m$ and $M$.
The entry decision still jumps at $s_E$ because the preparation cost has an atom.
Thus graded posteriors do not imply continuous aggregate entry.

### Verified literature comparison

The verified record is [LIT_extracts.md, A3](../../alex_meeting_2026_10_21/memos/LIT_extracts.md#a3-dow-goldstein-and-guembel-2017).
It covers Dow, Goldstein, and Guembel (2017), *JEEA* 15(4), 877–909, DOI `10.1093/jeea/jvw023`.
This memo uses only the facts recorded there.

Their model has many small speculators, costly noisy signals, normal noise, and two trade directions.
The manager observes price and selects a real investment.
The informed mass is endogenous, and an interior mass equates its information return with its cost.
Their selected continuation permits no information alongside positive information when the safe project is optimal at the prior.
Their analysis also distinguishes stable and unstable branches.

The common mechanism is a real decision that changes the return to information production.
Here the decision is challenger entry, and research precedes a single investor's discrete order.
The positive entry floor keeps the claim sensitive to quality even without expensive preparation.
Thus no research does not exist automatically; it needs $\kappa\ge V_r(0)$.
Our upward jump comes from the preparation cost atom.
It can separate two equilibria without an interior equilibrium at the jump.

Their price pools and selected continuation differ from the price sufficiency proved here.
The verified record does not establish a theorem for our discrete acquisition game.
Any stronger source claim about this game is **unverified**.

## 5. Numerical example

### Equal noise, original preparation cost

Use $(h,\ell,p,\rho,k,c_H)=(10,1,1/2,1/4,1/50,6)$ and $\pi=1/2$.
The exact research values are

$$
\overline V_3(1.2)=0,\quad
\overline V_3(3)=\frac4{225},\quad
\overline V_3(3.6)=\frac{629}{21600}.
$$

At $\kappa=1/100$, research changes from zero to one.
The exact spread cutoff is $12/25$, with strength $r_\kappa=2.571054535759\ldots$.
Entry is $0.25$ at $r=1.2$ and $0.375$ at $r=3$ and $r=3.6$.
Its later return requires $r>4+\sqrt{63}/2=7.968626966597\ldots$.
At equality, expensive preparation still occurs after complete good news.

### Discrete-Laplace, candidate preparation cost of five

Use the same auction values, $b=2$, and $c_H=5$.
At $r=3$, the analytical cutoffs evaluate as follows:

$$
\begin{aligned}
a&=0.606530659713\ldots,&\tau&=0.585,\\
s_E&=0.631455407304\ldots,&v_E^-&=0.029489021784\ldots,\\
v_0&=\frac{19}{600}=0.031666666667\ldots,&v_1&=0.087918213417\ldots,\\
v_E^+&=0.094069177396\ldots.
\end{aligned}
$$

These numbers imply the complete cost correspondence at this strength:

| Research cost | Acquisition equilibria |
|---|---|
| $0<\kappa\le v_E^-$ | Full research only. |
| $v_E^-<\kappa<v_0$ | One interior root below $s_E$, and full research. |
| $v_0\le\kappa\le v_1$ | No research and full research. |
| $v_1<\kappa\le v_E^+$ | No research, and one root in $[s_E,1)$. |
| $\kappa>v_E^+$ | No research only. |

**Numerical diagnostic.** Direct evaluations give these examples:

| $\kappa$ | Positive acquisition probability | Entry there | Other equilibrium |
|---|---:|---:|---|
| $0.02$ | $1$ | $0.625$ | None. |
| $0.03$ | $0.410890232219$ and $1$ | $0.25$ and $0.625$ | None. |
| $0.05$ | $1$ | $0.625$ | $\psi=0$, entry $0.25$. |
| $0.09$ | $0.863132221274$ | $0.612429447516$ | $\psi=0$, entry $0.25$. |
| $0.094$ | $0.635073337122$ | $0.591483493695$ | $\psi=0$, entry $0.25$. |
| $0.095$ | None. | — | $\psi=0$, entry $0.25$. |

The conditions in Proposition C6.5 hold for $\kappa=0.02$ and $(r_0,r_1,r_2)=(1.2,3,4.2)$.
They also admit exact rational bounds.
The bounds on $a$ give $m>3/8$ and $3/5<M<5/8$.
Therefore

$$
\frac12[\rho m\Delta_T(3)-k]>\frac{17}{800}>\frac1{50},\qquad
\Delta_T(1.2)=\frac1{60}<\frac1{50},
$$

$$B_{1.2}(1/2)=\frac{1153}{240}<5,\qquad
B_3(M)>B_3(3/5)=\frac{41}{8}>5,\qquad
B_{4.2}(M)<B_{4.2}(5/8)=\frac{104}{21}<5.$$

These inequalities verify the proposition without a decimal comparison.
The research lower bound at $r_1$ is $0.021461722400\ldots>0.02$.
Also $B_{1.2}(1/2)=4.804166666667\ldots<5$.
The upper-posterior gross profits are $B_3(M)=5.312161093349\ldots$ and $B_{4.2}(M)=4.932612129447\ldots$.

Thus acquisition is uniquely $(0,1,1)$.
Entry is $(0.25,0.625,0.25)$ and high-class ownership is $(0.125,0.358422249201\ldots,0.125)$.
The ceiling solves $B_r(M)=5$ at $r=3.986096571638\ldots$.

Research itself need not rise with strength.
At $\kappa=0.06$, the equilibria at $r=3.98$ are $\psi\in\{0,1\}$.
At $r=3.99$, the unique equilibrium has $\psi=0.002194101729\ldots$.
At $r=4$, it has $\psi=0.035613611900\ldots$.
At $r=4.2$, it has $\psi=1$.

The loss of expensive entry first removes the full-research equilibrium.
The larger spread later restores full research without expensive entry.

With the original $c_H=6$, $r=3$, and $\kappa=0.03$, acquisition is uniquely $0.410890232219\ldots$.
Entry stays at $0.25$.
This is graded information without any entry gain.

### Welfare examples

**Numerical diagnostic.** With $\xi=1$, the full-research equilibrium at $r=3$, $c_H=5$, $\kappa=0.02$ gains $0.118310410006\ldots$.
Its entry benefit before research and trade costs is $0.148310410006\ldots$.
At $\kappa=0.094$, the positive equilibrium increases entry but loses $0.036441510220\ldots$ in welfare.
The interior equilibrium at $\kappa=0.03$ loses $0.016435609289\ldots$ and does not change entry.
At $r=4.2$, full research with $\kappa=0.02$ loses $0.03$ because it adds no entry.
These losses remain negative when the trade cost is a transfer.

### Arithmetic record and correction to the brief

The script is [calculations.py](../scripts/C6_info_acquisition/calculations.py).
Its output is [results.txt](../scripts/C6_info_acquisition/results.txt).
Auction inputs use exact fractions.
The discrete-Laplace calculations use 90 decimal places.
The script prints outcomes and contains no assertions.
Its quadratic roots agree with its branch roots to at least 88 decimal places.

The script also evaluates both purchase payoffs from individual integer flows against fixed schedules.
It uses noise values from $-400$ through $400$ for this separate calculation.
The omitted gross high-class payoff is at most

$$\Delta_T\frac{2a^{401}}{1+a}=6.9664\times10^{-88}\quad\text{at }r=3.$$

The direct sums and the exact two-region formulas differ by less than this printed bound.
Every low-class purchase loses to zero at the displayed schedules.
This use of the order interface supports the arithmetic; the propositions supply the equilibrium proofs.

The brief's no-feedback profit of $+0.060$ does not reproduce.
At $r=3$, a high-class purchase earns $+0.058334570734\ldots$ without expensive entry.
It earns $+0.175836426835\ldots$ with that entry.
These are conditional trade profits, rather than ex ante research values.
Their ex ante research values are half these amounts.

## 6. Open issues

- The complete correspondence outside $B_r(\pi)<c_H$ remains open.
- For $\pi>1/2$, a fixed-entry branch can turn upward; the two-equilibrium bound does not cover that case.
- Atomless preparation costs can smooth the jump; their effect on multiplicity needs a separate proof.
- Private research costs or several investors require a different acquisition game.
- Public acquisition needs a continuation selection when the acquired game itself has several equilibria.
- Uninformed trade is prohibited here. A relaxation needs new deviations and can permit manipulation.
- Welfare optimality, research subsidies, and reserve choice remain open.
- No independent second derivation from a separate workstream appears in this memo.

The analytical results cover both later orders and the acquisition deviation.
The numerical examples are high-precision diagnostics, rather than interval certificates.

## 7. Plain summary

The investor can pay for information before it trades.
A stronger incumbent raises the spread between target payoffs.
That wider spread can make research worthwhile.

Equal noise gives a sharp research cutoff.
Hidden research changes the bad-news belief, but both middle flows retain the prior.
The good-news flow still reveals quality completely.
Research cannot profit from the extra entry that this flow induces.
Robust coexistence therefore fails in this model.

Discrete-Laplace noise gives a stronger result.
Research makes both price posteriors more informative.
When good news induces expensive entry, the private return to research jumps upward.
No research and full research can then coexist over an interval of research costs.
Other costs support graded information through an interior acquisition probability.

The original preparation cost of six blocks expensive entry under discrete-Laplace noise at every permitted incumbent strength.
The cost of five in the brief's candidate permits feedback.
With that cost and a research cost of $0.02$, entry follows $0.25\to0.625\to0.25$.
Research is unique at each displayed strength.

Public acquisition removes the dependence of acquired prices on the initial acquisition probability.
At the benchmark middle strength, this removes hidden-acquisition coexistence.

Each additional entry has a positive expected allocation gain.
Research and trade costs can exceed that gain.
Some positive-research equilibria add no entry and reduce welfare.
Thus a private research incentive does not by itself establish a social benefit.
