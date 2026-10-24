# N1. Market observables from one order slot

Date: 23 October 2026. Scope: new observable implications of V3.

## 1. Question

Can market data distinguish private information from the extra entry that the information causes?
Four extensions give exact restrictions on prices, order counts, winner identity, and event returns.
They add observable implications without a new trader or a new order opportunity.
They do not edit the paper.

### Common setup and source boundary

Use V3 with the informed menu $\{-1,0,1\}$ and no separate noise.
An informed identity fills one public slot with probability $\lambda$.
Otherwise, a liquidity identity sells, waits, or buys with probabilities $(\beta,1-2\beta,\beta)$.
Assume $0<\lambda<1$ and $0<\beta<1/2$.
The liquidity motive is exogenous.
A zero order means an observed opportunity without trade.

Use the benchmark

$$
(h,\ell,p,\rho,c_L,c_H,k,\pi)
=(10,1,1/2,1/4,0,6,1/50,1/2),
\qquad \beta=1/3,\quad \lambda=6/17.
$$

The equilibrium concept is perfect Bayesian equilibrium of the finite order game.
Bayes' rule applies at all three orders because each has positive liquidity mass in both classes.
No off-path belief enters this unit menu.
At investor indifference, permit any mixture.
At challenger indifference, require preparation.
Acquisition-value ties have probability zero.

The results at $r=3$ and $r=18/5$ are strict under both alternative tie rules in T2.
Fractional order sizes require new off-path beliefs, as X_check explains.
They lie outside this memo.

I checked the auction formulas against equation (4) at commit `01bd5d6` in `overleaf/paper/main.tex`.
The comparison uses the same commit's `online_appendix.tex`, equations OA.16–OA.17.
For $p<\ell<r<h$, write

$$
\begin{aligned}
t_0&=p(1-p/r),& t_H&=r/2+p^2/(2r),\\
t_L&=\ell-(\ell^2-p^2)/(2r),&
g_H&=h-t_H,&g_L&=\ell-t_L,\\
\Delta_T&=t_H-t_L=(r-\ell)^2/(2r),&
B_r(\mu)&=g_L+\mu(g_H-g_L).
\end{aligned}
$$

The price and entry schedules are

$$
\begin{aligned}
e_r(\mu)&=\rho+(1-\rho)\mathbf1\{B_r(\mu)\ge c_H\},\\
P_r(\mu)&=t_0+e_r(\mu)[t_L-t_0+\Delta_T\mu],\\
\tau(r)&=\frac{c_H-g_L}{g_H-g_L}.
\end{aligned}
\tag{1}
$$

The price strictly increases in the posterior.
Thus the challenger can recover the posterior from the price.
The positive entry floor and $\Delta_T>0$ establish this property, including across a jump in entry.

For $3\le r\le18/5$, full informed purchases and sales form the unique order outcome.
T2 §3.4 and X_check §3.4 establish this claim with uniform deviation bounds.
The following inequalities also give the relevant benchmark margins:

$$
\tau(3)=141/200<29/40<4245/5804=\tau(18/5),
$$

$$
\rho\Delta_T(3)(1-29/40)-k=31/1200>0.
$$

Every correctly signed unit order gains at least this amount on the stated strength interval.
Here $\Delta_T$ rises in $r$.
Every wrong-signed order loses money.
At $r=6/5$, the bound $\Delta_T=1/60<k$ instead forces both informed classes to wait.

Define

$$
b=(1-\lambda)\beta=11/51,\quad
M=\frac{b+\lambda}{2b+\lambda}=29/40,\quad
\vartheta=2M-1=9/20,\quad
 d=b+\lambda/2=20/51.
\tag{2}
$$

Under full two-sided orders, the posterior vector on $(-1,0,1)$ is $(1-M,1/2,M)$.
The order probabilities are $(d,1-2d,d)$.
The informed identity probability remains $\lambda$, not $\vartheta$.

At the cap, direct substitution into (1) gives

$$
B_r(M)-6=\frac{100r-29r^2+1}{80r}.
$$

Its derivative is $-29/80-1/(80r^2)<0$.
The positive root of $29r^2-100r-1=0$ therefore gives the unique entry ceiling:

$$
r_C=\frac{50+\sqrt{2529}}{29}\approx3.45824702905933.
\tag{3}
$$

On $[3,r_C]$, a purchase recruits the high-cost challenger.
On $(r_C,18/5]$, no order recruits it.
A sale or zero order never recruits it on this interval.
At the ceiling, the challenger tie rule retains extra entry.

**Literature boundary.** One new source check verifies the Glosten–Milgrom abstract on 23 October 2026.
The [institutional record](https://business.columbia.edu/faculty/research/bid-ask-and-transaction-prices-specialist-market-heterogeneously-informed-traders) states that superior information creates a spread with a risk-neutral dealer and zero expected profit.
This supports the adverse-selection comparison only.
The exact arrival law and the full model remain **unverified** here.

L1_survey, C09, supplies the earlier verified Dow–Gorton record for alternative informed and liquidity arrivals of the same size.
That record supports the device, not these takeover predictions.
L1_survey, M04, records Easley–Kiefer–O'Hara–Paperman (1996) at abstract scope.
Its exact PIN formula and the transfer of its estimator remain **unverified** here.
No source claim below exceeds these limits.

## 2. Extensions developed

### 2.1 A spread that separates information from recruited entry

**Status: analytical.**

**Question and model change.** What does a wider spread measure before a takeover contest?
Keep the model unchanged.
Add the conditional transaction spread $S=P_r(1)-P_r(-1)$ as a measured outcome.
Here $P_r(q)$ denotes the price conditional on the observed order $q$.
These are unit execution prices in one opportunity, not quotes from a continuous limit order book.
The separate trade cost $k$ does not enter $S$ directly.

**Result.** On the full-order interval, let $J=\mathbf1\{r\le r_C\}$.
Then

$$
\boxed{
S(r)=\rho\Delta_T(r)\vartheta
+(1-\rho)J[t_L(r)-t_0(r)+\Delta_T(r)M].}
\tag{4}
$$

The first term is the spread when entry stays at its floor.
The second term is the price effect of recruited entry.
It can dominate the spread without a larger informed share.

**Derivation.** Put $A_r(\mu)=t_L-t_0+\Delta_T\mu$.
Equation (1) gives

$$
\begin{aligned}
P_r(-1)&=t_0+\rho A_r(1-M),\\
P_r(0)&=t_0+\rho A_r(1/2),\\
P_r(1)&=t_0+\rho A_r(M)+(1-\rho)J A_r(M).
\end{aligned}
\tag{5}
$$

Subtract the first line from the third.
The terms $t_0$ and $\rho(t_L-t_0)$ cancel.
The posterior difference is $M-(1-M)=\vartheta$.
This yields (4).

For price impact relative to the neutral-order price, subtraction instead gives

$$
\begin{aligned}
P_r(1)-P_r(0)&=\rho\Delta_T\vartheta/2+(1-\rho)J A_r(M),\\
P_r(0)-P_r(-1)&=\rho\Delta_T\vartheta/2.
\end{aligned}
\tag{6}
$$

Thus buy impact exceeds sell impact by exactly the entry term.
The neutral-order price need not equal the price before the slot.
Section 2.4 derives that distinction.

At the benchmark,

$$
\begin{aligned}
S(3)&=3/40+113/160=25/32,\\
S(18/5)&=169/1600,\\
\frac{\text{entry term at }3}{S(3)}&=113/125=0.904.
\end{aligned}
\tag{7}
$$

The informed share remains $9/20$ at both strengths.
Volume remains $40/51$.
The spread falls because extra entry disappears.
The price still reveals the same class posterior.

The collapse also occurs locally at $r_C$.
Each component rises strictly with $r$ while $J$ stays fixed.
Indeed,

$$
\Delta_T'(r)=\tfrac12-\tfrac1{2r^2}>0,
\qquad
\frac{d(t_L-t_0)}{dr}=\frac1{8r^2}>0.
$$

At the ceiling, the right limit of the spread is lower by

$$
(1-\rho)A_{r_C}(M)>0.
\tag{8}
$$

This proves a rise, a discrete fall, and a further rise on the interval around the ceiling.
Exact evaluations give $S(3.45)=27047/29440$ and $S(3.46)=136161/1384000$.

**Economic interpretation.** A buy causes both a better quality belief and extra preparation.
The dealer anticipates both effects in the execution price.
A spread estimate without the entry channel overstates the part due to private information alone.
This is a value-creation component, not a dealer rent.

**Testable prediction.** Near the entry ceiling, buy impact and the spread fall while signed order counts and the informed share stay stable.
Sell impact stays continuous.
Within each regime, a stronger incumbent raises both information components.
At $r=3$, denial of price access reduces the spread from $25/32$ to $3/40$ at unchanged orders.
This access comparison holds at the benchmark because both regimes retain full orders.

**Difference from the current Laplace model.** The general entry component is not unique to the slot.
Laplace tail prices admit the same decomposition with their own posterior cap.
Those tail prices also jump at their entry ceiling.
However, the Laplace model prices aggregate flow, not one observed unit order.
Its full-order posterior varies continuously on $(-1,1)$ and stays constant in the tails.
Thus its maximum price gap is not a literal unit bid–ask spread.
The slot gives an exact unit spread, a direct informed-share interpretation, and only three price outcomes.
It also makes every buy recruit on this branch; Laplace recruits only flows above a positive cutoff.

**Open.** Real quotes contain dealer costs, inventory effects, and several order sizes.
Those components require measurement controls before equation (4) can describe a quoted spread.

### 2.2 Informed trade, volume, and an identification restriction

**Status: analytical.**

**Question and model change.** Can the observed order law identify informed activity?
Keep the model unchanged.
Measure volume, signed imbalance, and directional informed shares.
Permit the informed mixtures that V3 already allows.

Let

$$
s=\lambda\Pr(q=1\mid H,I=1),\qquad
t=\lambda\Pr(q=-1\mid L,I=1).
$$

Wrong-signed orders lose money.
The class prior is $1/2$ throughout this extension.
The conditional masses for a buy are $b+s$ in class H and $b$ in class L.
For a sale, they are $b$ in class H and $b+t$ in class L.
Therefore

$$
\begin{aligned}
D_+&=b+s/2,& D_-&=b+t/2,&D_0&=1-2b-(s+t)/2,\\
v&:=\Pr(Q\ne0)=2b+(s+t)/2,&
\mathbb E[Q]&=(s-t)/2.
\end{aligned}
\tag{9}
$$

The probability per slot of an actual informed trade is $(s+t)/2$.
Divide it by $v$ to obtain

$$
\boxed{\operatorname{PIN}_{\rm slot}=\frac{s+t}{4b+s+t}.}
\tag{10}
$$

This is a population share of informed nonzero orders.
It is a definition here, not an identified estimate from an external PIN method.

Conditional on a buy, informed mass is $s/2$ out of $b+s/2$.
Conditional on a sale, informed mass is $t/2$ out of $b+t/2$.
Hence

$$
\begin{aligned}
\operatorname{PIN}_+&=\frac{s}{2b+s}=2\mu_+-1,\\
\operatorname{PIN}_-&=\frac{t}{2b+t}=1-2\mu_-.
\end{aligned}
\tag{11}
$$

The posterior formulas follow directly from the same class masses.
The pooled share is the order-frequency weighted mean of these directional shares.
It equals $2M-1$ only under the appropriate full-order restrictions.

**Three equilibrium implications.**

- At $r=6/5$, both informed classes wait.
  Then $v=22/51$, the informed share is zero, and mean imbalance is zero.
- At $r=1.55,1.60,1.65$, the full informative equilibrium has $s=\lambda$ and $t=0$.
  Then $v=31/51$, the informed share is $9/31$, and $\mathbb E[Q]=3/17$.
  The normalized imbalance is $(\mathbb E[Q])/v=9/31$.
  Its buy share is $9/20$, but its sale share is zero.
- At $r=3$ and $r=18/5$, both informed classes trade fully.
  Then $v=40/51$, the informed share is $9/20$, and mean imbalance is zero.

For completeness, the intermediate full informative outcomes satisfy the order incentives directly.
Across these three strengths,

$$
\Delta_T\ge121/1240,\qquad
\Delta_T(1-M)-k\ge339/49600>0.
$$

Thus the high class prefers the full purchase at the recruited price.
The low-class gross sale return is at most

$$
\rho\Delta_T/2\le169/10560<1/50=k.
$$

It therefore waits.
All nonbuy posteriors stay at or below $1/2$.
No informed trade also remains an equilibrium because the same upper bound applies to a deviation from that outcome.
These statements agree with T2's full-branch classification.

**Identification result.** Under full two-sided orders, frequencies alone reveal $v=\lambda+2b$.
They do not reveal $\lambda$ and $\beta$ separately.
For example, both parameter pairs

$$
(\lambda,\beta)=(6/17,1/3),\qquad(1/3,23/68)
$$

give $(D_-,D_0,D_+)=(20/51,11/51,20/51)$.
Their informed shares differ: $9/20$ and $17/40$.
Both pairs also satisfy the strict benchmark entry band.
Thus even all three order frequencies do not identify the informed share.

Prices add a restriction if the auction objects and entry floor are known.
From the sell impact in equation (6),

$$
\boxed{
\vartheta=\frac{2[P_r(0)-P_r(-1)]}{\rho\Delta_T(r)},\quad
\lambda=v\vartheta,\quad
\beta=\frac{v(1-\vartheta)}{2(1-v\vartheta)}.}
\tag{12}
$$

The first equality holds because a sale and a neutral order both leave entry at its floor.
The second follows from $\vartheta=\lambda/(\lambda+2b)$.
Substitute $b=(v-\lambda)/2=(1-\lambda)\beta$ to obtain the third.
The benchmark recovers $(\vartheta,\lambda,\beta)=(9/20,6/17,1/3)$ exactly.
A raw total spread cannot replace the sell impact when a buy recruits entry.

**Testable prediction.** High informed activity can coexist with zero average imbalance.
During coexistence, the full informative equilibrium instead has a positive imbalance and a lower pooled informed share.
The restriction $2[P_r(0)-P_r(-1)]=\rho\Delta_T\operatorname{PIN}_{\rm slot}$ applies only on the symmetric full branch.
A violation can reject that branch or its maintained auction and liquidity assumptions.
It need not reject every slot equilibrium.

**Difference from the current Laplace model.** Its investor is always informed and present.
Its independent noise law has no identity parameter $\lambda$ or observed inactive slot.
The posterior cap therefore does not equal an informed arrival share.
Its net noise law alone does not identify gross informed volume.
For illustration, use the independent exponential buy and sell components stated in the pinned paper.
At scale 2, their combined mean gross volume is 4, against one informed unit under full orders.
The ratio of mean informed volume to mean gross volume is then $1/5$.
Yet twice its posterior cap minus one equals $(e-1)/(e+1)$, about $0.4621$.
These are different objects.
Equations (10)–(12) provide a finite-slot link that the current Laplace model does not supply.

**Open.** Equation (12) assumes known $\rho$, $\Delta_T$, and the full symmetric branch.
Unknown auction payoffs or a mixture of branches can destroy identification.
No empirical PIN estimate is claimed here.

### 2.3 Order direction predicts the winner after it stops predicting entry

**Status: analytical.**

**Question and model change.** Does order direction retain real-outcome content above the entry ceiling?
Keep the model unchanged.
Measure preparation and the winner as separate outcomes.
Let $A$ mean that the challenger prepares, and let $W_C$ mean that it wins.

**Derivation.** Conditional on the class, the order contains no information about the incumbent value $R$.
Preparation depends on the order and independent cost, not on the realized class or $R$.
Consequently,

$$
\Pr(H\mid Q=q,A)=\mu_q.
$$

A high-class prepared challenger wins because $h>r$.
A low-class prepared challenger wins when $R<\ell$, with probability $\ell/r$.
Therefore

$$
\boxed{
\Pr(W_C\mid Q=q,A)=\mu_q+(1-\mu_q)\ell/r,
\quad
\Pr(W_C\mid Q=q)=e_q[\mu_q+(1-\mu_q)\ell/r].}
\tag{13}
$$

The first quantity conditions on preparation.
The second quantity includes the entry response.
They are not interchangeable.
The probability that class H acquires the target is $e_q\mu_q$.

For full two-sided orders, subtract the sale outcome from the buy outcome in the first formula:

$$
\boxed{
\Pr(W_C\mid Q=1,A)-\Pr(W_C\mid Q=-1,A)
=\vartheta(1-\ell/r).}
\tag{14}
$$

The derivative in $r$ is $\vartheta\ell/r^2>0$.
Thus the conditional winner gap rises with incumbent strength even across the entry ceiling.
At $r=3$, the gap is $3/10$.
At $r=18/5$, it is $13/40$.

Since $\mathbb E[Q]=0$, the covariance with preparation is

$$
\operatorname{Cov}(Q,\mathbf1_A)=d(e_+-\rho)
=\begin{cases}5/17,&3\le r\le r_C,\\0,&r_C<r\le18/5.\end{cases}
\tag{15}
$$

Above the ceiling, equation (13) similarly gives

$$
\operatorname{Cov}(Q,\mathbf1_{W_C})
=d\rho\vartheta(1-\ell/r)>0.
\tag{16}
$$

At $r=18/5$, this covariance is $13/408$.
Entry has zero directional covariance, but ownership retains positive directional covariance.
The order distribution and the class posterior distribution stay fixed across this change.

Exact benchmark conditional outcomes are:

- At $r=3$, entry after sale, wait, and buy equals $(1/4,1/4,1)$.
  The challenger win probabilities conditional on preparation are $(31/60,2/3,49/60)$.
- At $r=18/5$, entry equals $(1/4,1/4,1/4)$.
  The corresponding conditional win probabilities are $(343/720,23/36,577/720)$.

**Testable prediction.** After entry stops responding to signed orders, buy orders still predict a challenger win among prepared challengers.
With greater incumbent strength, this conditional winner gap becomes larger under the fixed order law.
An entry regression alone can therefore miss information that affects allocation.

**Difference from the current Laplace model.** Its paper already predicts that favorable prices forecast challenger wins.
That qualitative prediction is not new.
Above its ceiling, the same conditional formula holds with the continuous posterior $\mu(X)$.
The slot adds the exact gap $\operatorname{PIN}_{\rm slot}(1-\ell/r)$ and the covariance restriction (16).
Laplace has no general identity between a posterior gap and an informed order share.
For its full-order model, its posterior gap across positive and negative flow is instead $1-e^{-1/2}$ at scale 2.
To derive this value, use $\Pr(X>0\mid H)=1-\tfrac12e^{-1/2}$ and $\Pr(X>0\mid L)=\tfrac12e^{-1/2}$.
Symmetry gives equal sign probabilities, so these two conditional probabilities also determine the sign posteriors.
Above its own ceiling, multiply their gap by $1-\ell/r$ for the conditional winner gap.

**Open.** A public offer can omit earlier preparation decisions and failed participants.
Selection into recorded offers can alter the conditional comparison.
The proposed outcome is preparation before the auction, not only an observed final bid.

### 2.4 Neutral-order losses and the later preparation surprise

**Status: analytical.**

**Question and model change.** What should an event study call the price before the slot and the return after preparation?
Add only passive observation of the preparation decision after the slot.
No second order or strategic action enters the model.
The event must reveal preparation without extra class information or bidder identities that reveal private value.

**Price before the slot.** Let $P^{\rm before}=\mathbb E[P_r(Q)]$ under the selected equilibrium.
This price already includes the expected value of recruitment.
Under full two-sided orders, equations (5) and the symmetric order law give

$$
\begin{aligned}
P^{\rm before}
&=t_0+\rho A_r(1/2)+(1-\rho)dJ A_r(M),\\
P_r(0)-P^{\rm before}&=-(1-\rho)dJ A_r(M).
\end{aligned}
\tag{17}
$$

For the first line, the posterior mean is $1/2$ by Bayes' rule.
Only a buy adds entry above $\rho$, with probability $d$.
The second line then follows from $P_r(0)=t_0+\rho A_r(1/2)$.
A neutral order leaves the posterior at $1/2$ but removes the expected entry increment.
Its price fall therefore does not require bad class news.

At $r=3$, the exact values are

$$
P^{\rm before}=485/544,\qquad P_r(0)=59/96,
\qquad P_r(0)-P^{\rm before}=-113/408.
\tag{18}
$$

The neutral order occurs with probability $11/51$.
It produces an unchanged class belief and a strictly negative price change.
At $r=18/5$, that change is zero because $J=0$.

**Preparation surprise.** Conditional on $Q=q$, preparation reflects only the independent cost draw.
It therefore does not change the class posterior.
The conditional proceeds after public preparation equal

$$
P^{A}_q=t_L+\Delta_T\mu_q=t_0+A_r(\mu_q).
$$

Without preparation, conditional expected proceeds equal $P^{\neg A}_q=t_0$.
Subtract equation (1):

$$
\boxed{
P^{A}_q-P_r(q)=(1-e_q)A_r(\mu_q),\qquad
P^{\neg A}_q-P_r(q)=-e_q A_r(\mu_q).}
\tag{19}
$$

The second expression concerns an event with positive probability only if $e_q<1$.
Both formulas describe dollar price changes per share.
A percentage event return divides each change by $P_r(q)>0$.

The cost-weighted expected change is zero:

$$
e_q(1-e_q)A_r(\mu_q)
+(1-e_q)(-e_q A_r(\mu_q))=0.
\tag{20}
$$

Thus the result does not predict a profitable unconditional price drift.
It predicts event surprises conditional on preparation or its absence.

At $r=3$, the preparation price changes after sale, wait, and buy are

$$
(77/160,\ 19/32,\ 0).
\tag{21}
$$

A buy fully anticipates preparation, so its preparation announcement has no price surprise.
A neutral order instead precedes a large positive surprise if the zero-cost challenger later prepares.
At $r=18/5$, preparation is uncertain after every order.
The corresponding changes are

$$
(5209/9600,\ 673/960,\ 8251/9600).
\tag{22}
$$

Now the preparation price change rises with the class posterior.
The order of event surprises across sale, wait, and buy differs between the two entry regimes.

**Testable prediction.** Below the ceiling, a favorable buy can precede a zero preparation-announcement return.
A neutral slot can produce a negative earlier price change without bad class news.
Above the ceiling, preparation surprises remain positive after every order and rise with the posterior.
A study must separate the slot price change from the later public preparation event.
This distinction also prevents the neutral-order price from being used as the price before the slot.

**Difference from the current Laplace model.** Equations (19)–(20) are general competitive-price identities.
Their signs do not uniquely favor the slot.
The slot adds three exact conditional surprises and positive mass at the unchanged prior belief.
Under full Laplace orders, $\mu(X)=1/2$ only at $X=0$, an event of probability zero.
Its event-return relation varies across interior flows, with flat tail portions and an entry discontinuity.
The slot replaces that relation with a finite set of joint restrictions on order, belief, entry, and return.

**Open.** Actual diligence is often private.
A later public offer can reveal more than the preparation decision.
Equations (19)–(22) require an event that isolates preparation information.
They are not a claim about every takeover announcement.

## 3. Ideas considered and dropped

- **Raw spread as PIN.** Drop this interpretation.
  At $r=3$, extra entry accounts for $90.4\%$ of the unit spread.
  The informed share remains $45\%$ when that price component disappears.
- **The cap statistic as a universal pooled informed share.** Drop this interpretation.
  On the full high-buy branch, the buy share is $9/20$, but the pooled share is $9/31$.
- **Positive average imbalance as a necessary sign of information.** Drop this interpretation.
  Full informed purchases and sales cancel in the average.
  Volume and directional outcomes retain information.
- **Automatic post-order drift.** Drop this prediction.
  Competitive prices imply the exact cancellation in equation (20).
- **A unique new spread-collapse sign against Laplace.** Drop this claim.
  Laplace tail prices also lose an entry component at their ceiling.
  The new content is the observable unit-order restriction and its informed-share link.
- **A new dynamic arrival or strategic-trader model.** Leave these questions outside N1.
  The four extensions need only the existing slot and passive outcome observations.

## 4. Ranking of the extensions

1. **Spread decomposition, §2.1.** Highest interest and strength.
   It separates information from value creation and gives a sharp local prediction at fixed order frequencies.
2. **Informed-share identification, §2.2.** Strongest measurement contribution.
   It gives an explicit failure of identification from counts and an exact price restriction that restores identification under stated assumptions.
3. **Event surprises, §2.4.** Useful for empirical design.
   The neutral-order loss and zero buy-announcement surprise are clear, but public event content needs careful measurement.
4. **Winner identity, §2.3.** Clean and exact, but its qualitative sign already appears in the paper.
   Its additional content is the restriction that links winner gaps to the informed order share.

## 5. Open issues and reproducibility

No empirical dataset enters this memo.
The calibration is illustrative, not an empirical estimate.
The four predictions depend on the selected equilibrium and the stated finite menu.
The full-order strength comparisons are unique on $[3,18/5]$.
The coexistence comparisons explicitly select the full informative branch.
No prediction resolves equilibrium selection in the coexistence interval.

The exact calculation program is
`audit/microstructure_search_2026_10_22/scripts/N1_observables/exact_observables.py`.
Its saved report is `exact_results.txt` in the same folder.
Its receipt points to the input record and lists the arithmetic method, software version, and output hashes.

Run from the repository root:

```bash
.venv/bin/python \
  audit/microstructure_search_2026_10_22/scripts/N1_observables/exact_observables.py \
  --output-dir audit/microstructure_search_2026_10_22/scripts/N1_observables
```

The program finishes in less than one second.
It uses exact rational flow sums and rational auction objects.
Decimals serve only as displays.
It prints every unit-order payoff for each class, not just the candidate's chosen order.
It also prints entry, prices, informed shares, event changes, ownership, and the signs around the entry ceiling.
It contains no tests or assertions.

I ran this interface on the stated benchmark and examined its report.
At $r=3$, the informed buy and sale net payoffs are $49/300$ and $31/1200$.
At $r=18/5$, each correctly signed order nets $1283/28800$.
The spread, entry, volume, and event quantities match the exact formulas above.
The entry-ceiling bracket has positive and negative rational endpoint excess profits, respectively.
No computation needs more than one process or 60 seconds.

Source access used one separate tab after the three existing tabs were listed.
That tab is closed.
The three original tabs remain open at their original URLs.
No login or saved download occurred.
All writes for this work remain in the team folder.
No commit or subtask was created.

## 6. Plain summary

The order slot gives four observable extensions without a new strategic player.

First, a spread combines information and the value of extra entry.
At strength 3, extra entry accounts for $90.4\%$ of the spread.
The spread collapses at the entry ceiling while the informed share and volume stay fixed.
This is a sharper measurement result than a claim that a wider spread means more informed trade.

Second, the informed identity probability and the informed share of actual orders differ.
Order counts alone do not identify them.
On the full symmetric branch, sell impact and volume recover both parameters if the auction objects and entry floor are known.
During coexistence, positive imbalance comes from informed purchases alone.
At greater strength, informed purchases and sales cancel in average imbalance.

Third, orders can stop predicting entry yet continue to predict the winner.
The conditional winner gap equals the informed share times $1-\ell/r$.
That gap grows with incumbent strength under the fixed order law.

Fourth, a neutral order can lower the price without bad class news.
It removes expected extra entry.
A buy can fully anticipate preparation and leave no later preparation-announcement surprise.
No result predicts an unconditional price drift.

Several qualitative effects also occur under Laplace noise.
The new contribution is the exact finite set of restrictions that joins order counts, informed shares, prices, entry, and outcomes.
The main empirical limits are equilibrium selection, unknown auction objects, and public events that reveal more than preparation.
