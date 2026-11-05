# Q3 (story): Who are the investors, and what does $t_0$ do?

## 1. Question and reading

The supervisor asked: "We have a $t_0$, target proceeds when no entry
happens. Who are the investors really? If they are the target firm
shareholders, should they not benefit from the stock price change
nonetheless? If they are outsiders, who can they be? Is there any
modelling device we should introduce to patch up this part of the
story?"

The question mixes five different objects. This memo keeps them apart.

1. **The informed investor.** It observes $\theta$ and submits the order
   $q\in[-1,1]$. Its payoff is $q(V_T-P)-k\lvert q\rvert$. It has no
   initial position (Section 2.3 of the paper).
2. **The noise traders.** They supply the Laplace demand $Z$. The paper
   does not say who they are.
3. **The market makers.** They absorb the net flow $-X$ at
   $P(X)=\mathbb E[V_T\mid X]$ and break even.
4. **The holders who receive $V_T$.** Every share held at the sale
   receives $V_T$. This group includes long-term holders, liquidity
   traders who did not sell, the informed investor, and market makers
   with inventory.
5. **$t_0$.** It is the expected sale proceeds per share when the
   challenger stays out: the incumbent buys at the reserve if $R\ge p$.

I read the question as three sub-questions.

- **(Q3a) Identity.** Who can trade on information about the
  challenger's match value, with no stake in the target? Is that
  credible?
- **(Q3b) Shareholder gain.** Do target shareholders gain from the
  mechanism? Two readings exist. In reading (i), the supervisor asks
  whether holders gain from the price change as a capital gain. In
  reading (ii), the supervisor asks whether an informed investor who
  is also a shareholder would gain from a higher price through its
  stake, even with bad news. This memo answers both.
- **(Q3c) Device.** Which modelling device best closes the gap?

Scope. The memo `Q3_welfare.md` owns the group-by-group ledger
(Claims W1–W7). The stake extension (initial stake $\omega>0$) is
derived in the companion stake memo. This memo does not repeat those
derivations. It adds five new results (Claims S2, S4, S5, S6, S7), an
evidence review, and a ranking of devices.

## 2. Formal setup

Notation follows the paper. Values and costs are per target share. The
incumbent value $R$ has a continuous cdf $F$ on $[0,\bar r]$. The
uniform $U[0,r]$ is the leading case. The challenger value is
$\theta\in\{\ell,h\}$ with prior $1/2$, and $0<p<\ell<r<h$ (eq. 1),
except in Claim S7. Costs: $C\in\{c_L,c_H\}$, $\Pr(c_L)=\rho$. Noise:
$f(z)=e^{-\lvert z\rvert/b}/(2b)$. Posterior bounds:
$m=1/(1+e^{2/b})$, $M=1-m$.

Realized proceeds per share:

$$
Y_0=p\,\mathbf 1\{R\ge p\}\ \text{(no entry)},\qquad
Y_\theta=\max\{p,\min(R,\theta)\}\ \text{(entry, }\theta>p).
$$

Then $t_0=\mathbb E[Y_0]$ and $t_\theta=\mathbb E[Y_\theta]$. Write
$w_L=t_L-t_0$ and $\Delta_T=t_H-t_L$. Under the floor $c_L<B_r(m)$,
eq. (9) gives the cost-averaged entry and the price:

$$
e_r(\mu)=\rho+(1-\rho)\mathbf 1\{B_r(\mu)\ge c_H\},\qquad
P_r(\mu)=t_0+e_r(\mu)\,[\,w_L+\Delta_T\mu\,].
$$

Under full orders $(q_H,q_L)=(1,-1)$, the threshold belief is
$\tau=(c_H-g_L)/(g_H-g_L)$ and the threshold flow is $x^*$ (eq. 12).

**Stake (for Claims S6 and S7 only).** An informed investor with an
initial stake of $\omega\ge0$ shares has the payoff
$\omega V_T+q(V_T-P)-k\lvert q\rvert$, as in the brief. The unit of
$\omega$ is the trading unit, the same unit as $q$.

**Noise decomposition (Claim S5).** Write $Z=Z_+-Z_-$. Here $Z_-$ is
sales by existing holders with liquidity needs, and $Z_+$ is purchases
by liquidity buyers. $Z_+$ and $Z_-$ are independent exponentials with
mean $b$, independent of $(\theta,R,C)$. This is a modelling choice.
The Laplace law of $Z$ does not identify gross volume.

**Accounting scale.** Π (the informed investor's expected gross
profit) is in the paper's units: one trading unit times per-share
values. This matches `Q3_welfare.md` at its normalization (float 1,
trade scale $\lambda=1$).

## 3. Results

### Claim S1 (where $t_0$ enters and where it cancels; analytical)

$t_0$ enters the price level, the inversion (10), the jump of the price
at the entry threshold (A.3), and the shareholder gain (A.41). It
cancels from the investor's residual advantages (11) and from every
trading incentive of an investor with no stake. A stake does not bring
$t_0$ back. A stake brings back only the increments $t_\theta-t_0$.

*Derivation.*

1. *Terminal value.* Given $\theta$ and flow $x$,
   $\mathbb E[V_T\mid\theta,x]=t_0+e(P(x))\,(t_\theta-t_0)$. With no
   entry the holder gets $t_0$. Entry adds $t_\theta-t_0$.
2. *Price.* Eq. (9) and eq. (10) contain $t_0$ as a known constant.
   The inversion
   $\mu_X=[P-t_0-e(P)w_L]/[e(P)\Delta_T]$ needs only that $t_0$ is
   public.
3. *Cancellation.* Subtract the price from the terminal value in
   state $H$:
   $A_H=e(t_H-t_0)-e(w_L+\Delta_T\mu_X)=e\Delta_T(1-\mu_X)$. Both $t_0$
   and $e\,w_L$ cancel. State $L$ is the same with the sign reversed.
   This is the "Residuals" step in the proof of Prop. A.2.
4. *Where $t_0$ still matters in the proofs.* In (A.3),
   $P_r(\mu_2)-P_r(\mu_1)=e_r(\mu_2)\Delta_T(\mu_2-\mu_1)
   +[e_r(\mu_2)-e_r(\mu_1)](w_L+\Delta_T\mu_1)$. The second term is
   the jump at the entry threshold. Its sign needs
   $w_L+\Delta_T\mu_1>0$. The paper uses $w_L>0$. So $t_0$ enters price
   sufficiency through $w_L=t_L-t_0$. At $r_1$ the jump is
   $(1-\rho)(w_L+\Delta_T\tau)=0.696250$. The term $w_L$ supplies
   49.4% of it (Section 5).
5. *Dividend diagnostic.* Add a constant $d$ to $V_T$. Then $P$ rises
   by $d$, so $V_T-P$ does not change. This is the same as adding $d$
   to $t_0$, $t_L$ and $t_H$. All differences stay the same. So $t_0$
   behaves like the dividend of Section 6.1. Note: the dividend in
   Section 6.1 is $0.257809$. This number equals the proceeds gain from
   price access at $r_1$, $0.872392-0.614583$. The diagnostic thus adds
   the shareholders' real gain to the price-hidden claim as a lump. The
   mean price then matches, but entry does not.
6. *Stake.* With a stake,
   $\mathbb E[\omega V_T\mid\theta,q]
   =\omega t_0+\omega(t_\theta-t_0)\,\mathbb E[e\mid\theta,q]$.
   The term $\omega t_0$ does not depend on $q$. It cancels from every
   comparison of orders. Only $\omega(t_\theta-t_0)$ times the effect
   of $q$ on entry remains. $\square$

**Consequence.** The concern is not the level of $t_0$. The concern is
that $t_\theta-t_0>0$. Claim S2 shows that this holds for both
challenger types and for every incumbent law.

### Claim S2 (entry raises proceeds with either challenger; analytical)

For every incumbent cdf $F$ and every challenger value $\theta>p$,

$$
Y_\theta-Y_0=p\,\mathbf 1\{R<p\}+(\min\{R,\theta\}-p)_+\ \ge 0,
\qquad
t_\theta-t_0=pF(p)+\int_p^\theta[1-F(u)]\,du>0 .
$$

If $p\ge\theta$, a prepared challenger of value $\theta$ has no
admissible bid and $t_\theta=t_0$.

*Derivation.* If $R<p$, there is no sale without entry, and the
challenger buys at $p$ with entry. If $R\ge p$, the target gets $p$
without entry and $\max\{p,\min(R,\theta)\}$ with entry. The
difference is $(\min\{R,\theta\}-p)_+$. Take expectations. Write the
positive part as $\int_p^\theta\mathbf 1\{R>u\}\,du$ and apply Tonelli,
as in (A.2). The integral is positive because $F(u)<1$ for $u<\bar r$
and $\theta>p$. $\square$

At the benchmark, $t_L-t_0=0.395833$ at $r_0$, $0.458333$ at $r_1$
and $0.465278$ at $r_2$. The increments for $H$ are larger:
$0.4125$, $1.125$, $1.404167$.

**Two consequences.**

1. Every holder of $V_T$ wants entry ex post, with either challenger
   type. A holder has no reason to want the challenger to learn the
   truth in state $L$.
2. The normalization $p\to0$ removes $t_0$ but not the increment:
   $t_L-t_0\to\mathbb E[\min(R,\ell)]$, which is $0.833333$ at $r_1$.
   So Point 4's normalization does not remove Point 3's concern.

### Claim S3 (the price change is not the gain; analytical, summary)

A holder who keeps a share receives $V_T$, not the interim price. The
interim price change is a forecast revision. It creates no value for
holders as a group. Holders gain only from the real effect: the price
recruits entry, and entry moves proceeds from $t_0$ toward $t_\theta$.
`Q3_welfare.md` proves this (Claims W3–W6). Its key facts:

- Market makers break even, so the informed investor's expected gross
  profit $\Pi$ equals the liquidity traders' expected loss (W3).
- At $r_1$ with full orders, $\Pi^{\text{acc}}=0.140731$ with price
  access and $\Pi^{\text{hid}}=0.069104$ without. This memo's script
  reproduces both values to six digits.
- Price access raises expected proceeds by
  $\Delta\mathcal R_T=0.257809$ (eq. A.41).
- Initial shareholders as a group gain
  $0.257809-0.140731=0.117078$ relative to an economy with no informed
  investor (W5). This figure counts *all* liquidity traders as initial
  shareholders. Claim S5 gives a second population reading with a
  different figure.

*Interpretation (not a model result).* The model has one trading
round. If one adds a round before the decision interval, competitive
pricing at that round gives $P_0=\mathbb E[V_T]=\mathcal R_T$. The
expected real gain would then be in the price when the sale
opportunity becomes public. A holder who sells at that date would
also share in it. This statement needs a second trading round and is
outside the current model.

So the answer to reading (i) is: yes, holders benefit, but through
entry, not through the price change. The price change is the
messenger. It is not the payment.

### Claim S4 (shareholders gain only where the price recruits entry; analytical sign, numerical size)

Fix $r$ with the floor $c_L<B_r(m)$ and full orders. Compare the
economy with price access and the economy where the challenger does
not see the price.

- (a) *Recruiting region,* $\tau>1/2$, that is, $c_H>B_r(1/2)$. Price
  access weakly raises entry in each state. If also $\tau<M$, it
  strictly raises expected proceeds $\mathcal R_T$.
- (b) *Screening region,* $m<\tau\le1/2$, that is,
  $B_r(m)<c_H\le B_r(1/2)$. Price access weakly lowers entry in each
  state and strictly lowers $\mathcal R_T$.

*Derivation.* Without price access the posterior is $1/2$. So hidden
entry is $\rho+(1-\rho)\mathbf 1\{B_r(1/2)\ge c_H\}$, the same in both
states. With access, entry at flow $x$ is
$\rho+(1-\rho)\mathbf 1\{\mu_X(x)\ge\tau\}$. In case (a), hidden entry
is $\rho$, and access entry is at least $\rho$ at every flow. Access
entry is $1$ on $\{\mu_X\ge\tau\}$. This set has positive probability
in both states when $\tau<M$, because the flow density is positive
everywhere and $\mu_X$ reaches $M$ for $x\ge1$. In case (b), hidden
entry is $1$. Access entry is $\rho<1$ on $\{\mu_X<\tau\}$. This set has
positive probability in both states when $\tau>m$. Then
$\mathcal R_T=t_0+\tfrac12\sum_\theta\mathbb E[e\mid\theta](t_\theta-t_0)$
and $t_\theta-t_0>0$ (Claim S2) give the signs. Full orders are the
unique trading outcome in both economies whenever the bound (A.6)
holds. That bound uses only the floor and $\Delta_T(r)$, not $c_H$.
$\square$

**Size (numerical diagnostic, $r_1=3$).** Proceeds change by
$-0.193$ to $-0.246$ in the screening region
($c_H\in[3.0,4.25]$). They change by $+0.258$ to $+0.344$ in the
recruiting region ($c_H\in[4.35,6.0]$). Acquisition surplus net of
preparation costs rises in every row (Section 5). The surplus sign in
the screening region is a numerical diagnostic only. The
per-decision contribution $B_r(\mu)-c_H+p^2/r$ (A.40) changes sign on
$[m,\tau]$, so I have no general proof.

**Reading.** Prop. 2 and Prop. A.9 live in the recruiting region:
(A2) places $\tau$ in $(1/2,M)$ at $r_1$. There the price can only add
entry, and holders gain in both states. In the screening region, the
same informed trading deters some entry. Holders then lose, although
acquisition surplus rises, because high-cost preparation by a
low-value challenger is wasteful. In Edmans, Goldstein and Jiang's
(2015) terms, the challenger's entry decision is an *amplifying*
action from the target's point of view in state $L$. Its objective is
the challenger's profit, not the target's value. The paper should
state that its shareholder gain is a feature of the recruiting region.

### Claim S5 (noise traders as shareholders with liquidity needs; analytical decomposition, numerical split)

(a) If $Z_+$ and $Z_-$ are independent exponentials with mean $b$,
then $Z=Z_+-Z_-$ has the Laplace density $f$ of eq. (2). Also

$$
\mathbb E[Z_+\mid Z=z]=z^++\tfrac b2,\qquad
\mathbb E[Z_-\mid Z=z]=z^-+\tfrac b2 .
$$

(b) The liquidity buyers' expected gain is
$\mathbb E[Z^+(V_T-P)]$. The liquidity sellers' expected gain
(relative to holding) is $-\mathbb E[Z^-(V_T-P)]$. The two sum to
$-\Pi$.

*Derivation.* (a) The joint density of $(Z_+,Z_-)$ is
$b^{-2}e^{-(u+v)/b}$ on $u,v\ge0$. On the line $u-v=z$, put $v=u-z$
with $u\ge\max(0,z)$. The density in $u$ is proportional to
$e^{-(2u-z)/b}$. So $u-\max(0,z)$ is exponential with mean $b/2$. This
gives both conditional means. The marginal is
$\int_{z^+}^\infty b^{-2}e^{-(2u-z)/b}\,du
=\tfrac1{2b}e^{(z-2z^+)/b}=\tfrac1{2b}e^{-\lvert z\rvert/b}$.
(b) $(Z_+,Z_-)$ is independent of $(\theta,R,C)$ given $Z$. So
$\mathbb E[Z_+(V_T-P)]=\mathbb E[(Z^++b/2)(V_T-P)]
=\mathbb E[Z^+(V_T-P)]$, because $\mathbb E[V_T-P]=0$ under
competitive pricing. The same holds for $Z_-$. The sum is
$\mathbb E[Z(V_T-P)]=-\Pi$ by Claim W3 of `Q3_welfare.md`. $\square$

**Split at $r_1$ (numerical diagnostic, under this decomposition).**

| Economy | $\Pi$ | Liquidity buyers' loss | Liquidity sellers' loss |
|---|---:|---:|---:|
| Price access | 0.140731 | 0.106037 | 0.034694 |
| Price hidden | 0.069104 | 0.034552 | 0.034552 |

Without access, the two sides share the transfer equally. With access,
almost all of the extra transfer ($0.0716$) falls on liquidity
buyers. The reason: entry jumps at $x^*=0.871>0$. The residual
advantage is largest at high flows. Net noise demand is mostly positive
there. Existing holders who sell for liquidity reasons bear almost no
extra cost from price access ($0.034694$ against $0.034552$).

**Two population readings give two shareholder figures.** Both use
the float normalization of `Q3_welfare.md` (float 1, $\lambda=1$) and
compare price access at $r_1$ with an economy with no informed
investor.

- *Reading A (all liquidity traders are initial shareholders;
  `Q3_welfare.md`, W5).* Initial shareholders gain
  $0.257809-0.140731=0.117078$.
- *Reading B (liquidity sellers are initial shareholders; liquidity
  buyers are outsiders).* Initial shareholders gain
  $0.257809-0.034694=0.223115$. Outside liquidity buyers lose
  $0.106037$ in expectation. Their unmodelled liquidity benefit is
  outside this count.
- `Q3_welfare.md`, W6, splits the float by a fixed holding share
  $\omega_Z$. That is a third partition. Its figures are not
  comparable with reading B.

Draft paragraphs 7.1 and 7.2 use reading B, because 7.1 defines the
liquidity buyers as other investors.

**Reading.** This device names the noise traders. Existing holders hit
by liquidity shocks sell. Outside liquidity buyers buy. It also supplies
an economic reason for the Laplace law. This connects to Point 2. The
split depends on the gross-volume choice $\mathbb E[Z_\pm]=b$. Another
decomposition with the same net law would split $\Pi$ differently.

### Claim S6 (a stake rewards buying in both states; analytical at the full-order schedule)

Fix the full-order candidate schedule at $r_1$:
$e(x)=\rho+(1-\rho)\mathbf 1\{x\ge x^*\}$. For an investor with stake
$\omega$, the stake part of the expected payoff given $\theta$ and
order $q$ is $\omega t_0+\omega(t_\theta-t_0)\Pr(q+Z\ge x^*)\cdot(1-\rho)+\omega(t_\theta-t_0)\rho$.
Its derivative in $q$ is

$$
\omega\,(t_\theta-t_0)\,(1-\rho)\,f(x^*-q)>0
\qquad\text{for both }\theta .
$$

So a stake rewards a higher order in both states. In state $H$ it
adds to the informational motive. In state $L$ it opposes it.

*Derivation.* Differentiate $\Pr(Z\ge x^*-q)=\int_{x^*-q}^\infty f$.
Use Claim S2 for $t_\theta-t_0>0$. $\square$

At the benchmark $r_1$, the marginal stake value per unit of stake is
$0.197784$ in state $H$ at $q=1$ and $0.033717$ in state $L$ at
$q=-1$. The slack in (A3) at $r_1$ is
$(1-1/b)\rho m\Delta_T-k=0.002412$. The $L$-state marginal stake value
per unit of stake is about 14 times this slack. This ratio is only a
scale indicator. The slack is a lower bound on the marginal trading
profit, not its value. The stake thresholds belong to the companion
stake memo.

**Contrast with Edmans, Goldstein and Jiang (2015).** In their model,
a stake is irrelevant to the asymmetry. Their Section II.E ("Zero
Initial Position") says the stake's incentive "is symmetric across
buying and selling, and so cancels out". The reason is that their real
decision is *corrective*: it raises firm value in both states. Here,
entry raises target value in both states, but the price only triggers
entry after good news. At the margin, selling on bad news deters entry
and lowers the value of the stake. (In the recruiting region, state-$L$
entry with price access still equals or exceeds hidden entry, so the
"amplifying" label of Claim S4 applies here only at the margin.) So in this model the stake creates the reluctance
to sell on bad news. In their model the feedback effect creates it.
The stake does not cancel here. This is the formal content of the
supervisor's worry in reading (ii).

*Limit of the claim.* The sign uses the full-order schedule, where
$e(x)$ is nondecreasing in $x$. For an arbitrary candidate schedule
with mixed orders, $\mu_X(x)$ need not be monotone in $x$, so the sign
of the stake term is not known in general.

### Claim S7 (a reserve that excludes the low value removes the $L$-side stake motive; analytical for the strong economy, conjecture for the weak economy)

Take the atom model with $\ell<p<r$. A prepared low-value challenger
has no admissible bid.

(a) $t_L=t_0$ and $g_L=0$. The stake term in state $L$ vanishes for
every candidate schedule.

(b) Suppose the floor $c_L<B_r(m)=m\,g_H$ holds and
$(1-1/b)\rho m\Delta_T(r)>k$. Then for **every** stake $\omega\ge0$
the unique trading outcome is $(q_H,q_L)=(1,-1)$.

(c) The cost: the spread becomes
$\Delta_T(r)=pF(p)+\int_p^{\bar r}[1-F(u)]\,du$. For the uniform,
$\Delta_T(r)=[(r-p)^2+2p^2]/(2r)$ and
$\Delta_T'(r)=(r^2-3p^2)/(2r^2)$. So a stronger incumbent widens the
spread only for $r>\sqrt3\,p$. The minimum spread is
$(\sqrt3-1)p>0$.

*Derivation.* (a) By Claim S2 with $p\ge\ell$. (b) Step 1: the
$L$-type's payoff equals its payoff with no stake, because
$\omega(t_L-t_0)=0$. The global bound (A.6) applies unchanged. So
$\sigma_L=\delta_{-1}$ in every equilibrium. Step 2: given
$\sigma_L=\delta_{-1}$, for each $q\in[-1,1]$ the ratio
$f(x-q)/f(x+1)=\exp\{(\lvert x+1\rvert-\lvert x-q\rvert)/b\}$ is
nondecreasing in $x$. The exponent is constant for $x<-1$, has slope
2 on $[-1,q]$, and is constant for $x>q$. A mixture over $\sigma_H$
keeps this property. So $\mu_X$ is nondecreasing in $x$ for every
$\sigma_H$. By price sufficiency, entry is a nondecreasing function of
$\mu_X$, so $e(x)$ is nondecreasing. Step 3: for the $H$-type,
$U_H(s)=sF_H(s)-ks+\omega(t_H-t_0)\int f(x-s)e(x)\,dx$. The last term
is nondecreasing in $s$ because a shift to the right raises the mean of
a nondecreasing function. So $U_H'(s)\ge(1-s/b)F_H(s)-k>0$, as in
(A.6). A sale by $H$ loses on both terms. So $q_H=1$. (c) Direct
computation from $Y_H-Y_0=p\mathbf 1\{R<p\}+(R-p)_+$. $\square$

*Weak economy (conjecture).* If $\Delta_T(r_0)<k$, the $L$-type never
trades. With $\sigma_L=\delta_0$ and $\sigma_H$ on $[0,1]$, the
posterior is at most $M_1=1/(1+e^{-1/b})$ ($0.622459$ at $b=2$). If
$B_{r_0}(M_1)<c_H$, no price can recruit high-cost entry. The stake
term then vanishes, and no trade stays the unique outcome. I did not
check $H$'s mixed orders that include sales, so this part is a
conjecture.

**Why this device is not free.** With $p=1.1$ the spread falls from
$1.0125$ at $r=1.2$ to $1.005$ at $r=3$ (Section 5). Prop. 1's sign
fails for $r<\sqrt3p$. The minimum spread $(\sqrt3-1)p$ makes no trade
at a weak incumbent hard to obtain together with (A3) at a strong one.
Section 6.3 of the paper points the same way: at the reserve $1.1$,
trading is informative in both economies. That section uses the
value-class variant ($\varepsilon_V=0.05$), not the atom model of this
claim, so it is supporting evidence, not a check. So the device protects the
strong-economy result against stakes. It does not deliver Prop. 2(i)
at the paper's numbers.

### 3.8 Who can the informed outsider be? (evidence review)

**What the model needs.** The sale opportunity is public (Section 2.1).
So the investor does not trade on *whether* a bid will come. It trades
on the *challenger's match value* $\theta$, which the challenger itself
does not know before diligence. Section 2.1 of the paper describes
this as target-side knowledge: customers, technology, product demand.
The investor must also be able to sell short: with $\omega=0$, the
order $q_L=-1$ is a short sale.

Most documented informed trading before takeovers is about bid
*arrival*, not match value. The table rates each candidate by fit to
$\theta$, legality, and evidence.

| Candidate | What it knows | Legal position | Evidence (status) | Fit to $\theta$ | Stake |
|---|---|---|---|---|---|
| Sector-specialist long-short fund (channel checks, expert calls) | Target's customers, technology, demand: the target side of the match | Legal if built from public and non-material facts. Rule 14e-3(a) covers only information that comes from the bidder, the target, or their agents | Cao, Green, Lei and Zhang (2022, working paper, Ohio State Dice Center WP 2022-13): expert calls stress technology and operations, and call volume precedes hedge-fund sales and higher short interest (abstract verified) | **High** | Small or hedged; can short |
| Event-driven and merger-arbitrage funds | Deal process, bidder interest, other bids | Legal on own research | Hsieh and Walkling (2005, JFE 77(3)): changes in arbitrage holdings relate to success, revisions, and the chance of later bids (abstract read from a secondary listing). Jiang, Li and Mei (2018, JF 73(6)): activist arbitrageurs lower the chance of sale to the announced bidder and raise premiums (abstract verified) | Medium | **Large, long** |
| Activist hedge funds (13D) | Firm-specific; often push for a sale | Legal; disclosure at 5% | Greenwood and Schor (2009, JFE 92(3)): activist returns are concentrated in targets later acquired (abstract verified) | Low to medium | **Large, long** |
| Short sellers | Bad news on technology or operations | Legal | Same expert-network evidence as row 1 (sell side) | High for state $L$ | Short |
| Customers or suppliers of the target | Demand and product fit | Corporate trading in a supplier's stock is rare; employees using employer information risk misappropriation | No takeover-specific evidence found | High as a *source*, low as a *trader* | None |
| Buyer-side insiders: lenders, advisers, lawyers | Whether and when the buyer bids; the buyer's plans | Illegal. For a tender offer: Rule 14e-3(a) once a substantial step toward the offer is taken. For any deal, including a negotiated merger: Rule 10b-5 under the classical or misappropriation theory (*United States v. O'Hagan*, 521 U.S. 642, 1997) | Acharya and Johnson (2010, JFE 98(3)): suspicious trading rises with the number of financing participants. Bodnaruk, Massa and Simonov (2009, RFS 22(12)): advisers' affiliated funds take target stakes before deals. Kedia and Zhou (2014, J. Financial Markets 18): pre-announcement trading in target bonds; weak evidence that dealers affiliated with M&A advisers sell before negative news (all abstracts verified) | **Low**: they know what the challenger knows, so the price teaches the challenger nothing | Varies |
| Options traders | A venue, not an identity | As for the underlying information | Cao, Chen and Griffin (2005, J. Business 78(3)): call-volume imbalances predict next-day returns before takeovers. Augustin, Brenner and Subrahmanyam (2019, Management Science 65(12)): positive abnormal volume before about 25% of 1,859 takeovers, mostly short-dated out-of-the-money calls; the SEC litigates about 8% of deals (abstracts verified) | Mostly about arrival | — |
| Target insiders | Technology and customers | Blackouts; Rule 14e-3(a) covers information from the issuer | Ahern (2017, JFE 125(1)): illegal tips originate, on average, from corporate executives and reach buy-side investors after three links (abstract verified) | High but illegal | Large |

Other evidence on price discovery before deals:

- Meulbroek (1992, JF 47(5)), with SEC illegal-trading cases: the
  abnormal return on an insider-trading day averages 3%. Almost half of
  the pre-announcement run-up before takeovers occurs on such days
  (abstract verified). So markets impound informed orders, as the
  model assumes. But the information is about arrival, and the trading
  is illegal.
- Keown and Pinkerton (1981, JF 36(4)) and Jarrell and Poulsen (1989,
  JLEO 5(2)) study the pre-bid run-up: citations verified, content not
  read.
- Samuelson and Rosenthal (1986, JF 41(2)) study target prices as
  indicators of tender offer success: citation verified, content not
  read. This is the closest evidence I found that prices *during* a
  public process carry information about the outcome.

**Conclusion of the review.** The best candidate for the benchmark
investor is a sector-specialist long-short fund. It builds a view of the
challenger's match from its own research on the target's business. Its
trading is legal under the mosaic approach, because the information
does not come from the bidder or the target. It can sell short, which
the $L$ order needs. It has no net exposure, or a small one, before it
trades. Buyer-side insiders are the wrong candidate on two grounds:
their trading is illegal, and they know what the challenger already
knows, so the price would teach the challenger nothing. The realistic
holders in a public sale process are event-driven funds, merger
arbitrageurs and activists. These hold large long stakes. They are the
reason the stake question matters.

A related question is why the specialist trades instead of selling its
view to the challenger. Admati and Pfleiderer (1990, Econometrica
58(4)) compare direct and indirect sale of information (abstract
verified). In practice, a buyer that buys commercial diligence pays for
it as part of preparation. That cost is in $C$. The price gives part of
the specialist's view to the challenger before it pays.

### 3.9 Candidate devices, ranked

| Rank | Device | What changes in the proofs | Pros | Cons |
|---|---|---|---|---|
| 1 | **Named outsider + liquidity-trader noise + accounting corollary** (D1 + D3) | Nothing. Eqs. (2), (9)–(11), Props. A.1–A.4, A.9 unchanged | Answers all three sub-questions. Free. Connects to Point 2 (Laplace = sales minus purchases) | Does not model a holder with a stake. A referee may still ask about large holders |
| 2 | **Informed blockholder with stake $\omega$** (D2; Kyle and Vila 1991; Edmans, Goldstein and Jiang 2015, Section II.E and online Appendix B.2; Khanna and Mathews 2012) | Payoff gets $\omega(t_\theta-t_0)\mathbb E[e\mid\theta,q]$. A.6 needs a stake term. Prop. A.4 (no-trade condition) changes. Prop. A.2 (pricing) does not change | Answers reading (ii) directly. Realistic for event-driven funds. Shows that EGJ's stake irrelevance fails here (Claim S6) | Realistic stakes are large in trading units. The $L$-type then wants to buy (Claim S6), and separation may fail. The companion memo must supply thresholds |
| 3 | **Reserve that excludes the low value** (Claim S7) | $t_L=t_0$. Strong-economy uniqueness holds for every $\omega$ | Removes the $L$-side stake motive. Uses a device already in Section 6.3 | Prop. 1 sign fails for $r<\sqrt3p$. No trade at the weak incumbent is hard to obtain. A robustness remark, not a patch for Prop. 2 |
| 4 | **Deal claim $V_T-t_0$ or derivatives** (D4) | For $\omega=0$: none. $V_T-t_0$ is the share minus a riskless constant, which is the dividend diagnostic | Clarifies that the investor trades the competition premium. Options are the documented venue of pre-deal trading | Not a patch: a stake motive comes from $t_\theta-t_0$, not from $t_0$, so it survives. Options change the payoff shape and add a second market |
| 5 | **Incumbent or challenger trades; toeholds; target disclosure** (D5) | The auction changes (toeholds: Bulow, Huang and Klemperer 1999). A trading incumbent wants to deter entry and so would sell, a manipulation in the sense of Goldstein and Guembel (2008) | Realistic in hostile deals | Toeholds are rare (Betton, Eckbo and Thorburn 2009, JFE 91(2): toeholds are now uncommon, but large and normal in hostile bids; abstract verified). The challenger does not know $\theta$, so its trades carry no information. The board does not hold $\theta$, so disclosure cannot replace the price (`Q3_welfare.md`, W7) |

On device 1, "no initial position" should be read as *no net economic
exposure*. A fund that holds shares and has hedged them with a swap
fixed before the interval has no exposure to $V_T$. In the model it is
an outsider.

## 4. What changes relative to the current paper

No proposition changes under the recommended device. The changes are
statements and one caveat.

- **Section 2.2.** "Neither bidder trades it" and "The investor has no
  control rights" stay. Add who the investor is: an outside specialist
  with no net exposure that can sell short.
- **Section 2.3.** "The investor has no initial position" stays. It
  should read as "no net exposure". Name the noise traders (Claim S5).
  State that $k$ includes the cost of borrowing shares for the
  $L$-state short sale. This parallels Edmans, Goldstein and Jiang's
  reading of their cost $\kappa$.
- **Eq. (11) and Prop. A.2.** Survive. Add one sentence: $t_0$ cancels
  from the residual, so the investor's identity does not matter for
  trading as long as it has no net stake (Claim S1).
- **(A.3).** Survives. It uses $w_L=t_L-t_0>0$. By Claim S2, this holds
  for every incumbent law, so the step does not depend on the uniform.
  The paper can say so.
- **Section 6.1 and Prop. A.9.** Survive. Add the shareholder sentence
  from `Q3_welfare.md` and the region caveat of Claim S4: the gain to
  holders needs the recruiting region $\tau>1/2$.
- **Section 1, last paragraph of the literature review.** The paper
  says that the model abstracts from toeholds. It should also say that
  it abstracts from informed blockholders, and cite Kyle and Vila
  (1991) and Edmans, Goldstein and Jiang (2015).
- **Section 7.** Options markets are a natural place to look for the
  informed trades (Cao, Chen and Griffin 2005; Augustin, Brenner and
  Subrahmanyam 2019). The test must separate match-value information
  from arrival information.
- **Under a stake (device 2).** Prop. A.4 and the global bound (A.6)
  change. The sign of the change is in Claim S6. The size is in the
  companion stake memo.

## 5. Numerical example

Benchmark vector $(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02)$,
$(r_0,r_1,r_2)=(1.2,3,3.6)$. Script (print-only, no assertions, no
output files):
`audit/alex_meeting_2026_10_21/scripts/Q3_story/story_diagnostics.py`.
Run it from the project root with `.venv/bin/python`. It uses scipy
quadrature split at $-1$, $x^*$ and $1$. It reproduces the paper's
$\mathcal R_T=0.872392$ and $0.614583$, the surplus $2.382301$ and
$2.302083$, entry $0.522757$, and the $\Pi$ values of `Q3_welfare.md`.
Status of all numbers: **numerical diagnostic**.

**A. Increments.**

| $r$ | $t_0$ | $t_L-t_0$ | $t_H-t_0$ | $\Delta_T$ |
|---|---:|---:|---:|---:|
| 1.2 | 0.291667 | 0.395833 | 0.412500 | 0.016667 |
| 3.0 | 0.416667 | 0.458333 | 1.125000 | 0.666667 |
| 3.6 | 0.430556 | 0.465278 | 1.404167 | 0.938889 |

**B. Price jump at $r_1$.** $\tau=0.705$, $x^*=0.871222$,
$w_L=0.458333$, jump $=0.696250$. The term $w_L$ supplies 49.4% of the
jump. The slack in (A3) is $0.002412$.

**C. Noise split.** See the table in Claim S5. A Monte Carlo check of
$\mathbb E[Z_\pm\mid Z]$ agrees with the formula to about $0.005$.

**D. Recruiting against screening at $r_1$** (full orders in every row;
$B_{r_1}(m)=2.366$, $B_{r_1}(1/2)=4.292$, $B_{r_1}(M)=6.217$).

| $c_H$ | $\tau$ | Entry, access | Entry, hidden | $\mathcal R_T$ access | $\mathcal R_T$ hidden | $\Delta\mathcal R_T$ | $\Delta\mathcal W$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3.00 | 0.345 | 0.6992 | 1.0000 | 1.015426 | 1.208333 | −0.192908 | +0.152038 |
| 4.00 | 0.465 | 0.6410 | 1.0000 | 0.973091 | 1.208333 | −0.235242 | +0.477826 |
| 4.25 | 0.495 | 0.6273 | 1.0000 | 0.962439 | 1.208333 | −0.245894 | +0.568158 |
| 4.35 | 0.507 | 0.6218 | 0.2500 | 0.958113 | 0.614583 | +0.343530 | +0.623998 |
| 5.00 | 0.585 | 0.5858 | 0.2500 | 0.928459 | 0.614583 | +0.313876 | +0.390946 |
| 6.00 | 0.705 | 0.5228 | 0.2500 | 0.872392 | 0.614583 | +0.257809 | +0.080218 |
| 6.80 | 0.801 | 0.2500 | 0.2500 | 0.614583 | 0.614583 | 0 | 0 |

The row $c_H=6$ is the paper's benchmark. The script also prints rows
for $c_H=3.6$. The sign of $\Delta\mathcal R_T$ switches exactly at
$c_H=B_{r_1}(1/2)$.

**E. Stake signs at $r_1$.** $\partial\,\text{entry}/\partial q$ is
$0.175808$ in state $H$ at $q=1$ and $0.073565$ in state $L$ at $q=-1$.
Both are positive. Per unit of stake, the marginal stake value is
$0.197784$ and $0.033717$.

**F. Excluding reserve, $p=1.1$, atom model.** $t_L-t_0=0$.
$\Delta_T=1.0125$ at $r=1.2$, $0.860$ at $1.5$, the minimum
$0.805256$ at $r=\sqrt3p=1.905$, then $1.005$ at $3$ and $1.204$ at
$3.6$. The one-sided posterior bound is $M_1=0.622459$. At the
benchmark objects, $B_{r_0}(M_1)=5.904<c_H=6$. This only illustrates
the condition of the weak-economy conjecture. The benchmark does not
have an excluding reserve.

## 6. Open issues and risks

1. **Stake sizes.** A blockholder's stake is many trading units, while
   the trading unit is small by the paper's own wording. Device 2 at
   realistic sizes is the large-$\omega$ regime. There the $L$-type
   wants to buy (Claim S6), and Prop. 2(ii) may fail. The companion
   stake memo must give the threshold. Until then, the paper should
   not claim robustness to blockholders.
2. **Thin slack at the benchmark.** The (A3) slack at $r_1$ is
   $0.002412$. Any device that adds a term to the investor's marginal
   payoff must fit in this slack, or the proof of (A.6) must be redone
   with the exact marginal profit.
3. **Gross volume.** Claim S5's split uses $\mathbb E[Z_\pm]=b$. The
   Laplace law fixes net demand only. The split is a diagnostic under
   one decomposition.
4. **Screening region.** Claim S4(b) shows that holders lose from
   informative prices when $\tau\le1/2$. A referee may ask why a board
   would accept a public process in that region. The paper does not
   model the board's choice. `Q3_welfare.md` (W7) flags the related
   board-objective question as open.
5. **Legality claims.** The rows on Rule 14e-3 and *O'Hagan* state US
   law only, from the rule text and case summaries. Rule 14e-3 applies
   to tender offers only. A negotiated merger, such as the disclosed
   approach of Section 2.1, falls under Rule 10b-5 alone. EU law
   (Market Abuse Regulation) was not checked.
6. **Evidence gap.** I found no paper that measures informed trading on
   a *named* potential buyer's match value during a public process. The
   evidence supports "prices impound informed orders before deals" and
   "specialists trade on technology and operations news". It does not
   test the model's exact information structure.
7. **Claim S7(b) weak economy.** The no-trade part is a conjecture.
   The $H$-type's mixed orders with sales are not checked.

## 7. Recommendation

In priority order:

1. **Adopt device 1 (named outsider, liquidity-trader noise).** Add the
   Section 2 paragraph below. It extends recommendation 1 of
   `Q3_welfare.md`: that memo asks for a population paragraph, and this
   one supplies the names, the short-sale reading of $q_L=-1$, and the
   Laplace decomposition.
2. **Answer the shareholder question in Section 6.1.** Add the second
   paragraph below. Include the recruiting-region caveat (Claim S4). Use
   the $\Pi$ numbers of `Q3_welfare.md`.
3. **State the role of $t_0$ once, in Section 3.3.** One sentence:
   "$t_0$ and the public entry effect cancel from the residual, so only
   an investor with a net stake has a reason to care about entry for
   its own sake; such an investor gains from entry with either
   challenger type because $t_\theta>t_0$." This is Claims S1 and S2.
4. **Treat the stake as an extension, not as the main model.** Use the
   companion memo's thresholds in Section 5 or the Online Appendix.
   Cite Kyle and Vila (1991), Edmans, Goldstein and Jiang (2015,
   Section II.E and online Appendix B.2), and Khanna and Mathews
   (2012). State the contrast of Claim S6: here the stake does not
   cancel. If the author wants a clean robustness statement, add Claim
   S7 as a remark in Section 6.3.
5. **Add the two literature sentences** (Section 1 and Section 7) from
   Section 4 of this memo.
6. **Do not adopt devices 4 or 5.** Mention the deal claim only as a
   reading of the dividend diagnostic.

Note on citations: the published AER version of Edmans, Goldstein and
Jiang (2015) discusses the initial stake in Section II.E. "Section 3.5"
in the brief is the numbering of the 2015 working paper (Section
3.5.3). Online Appendix B.2 has the same label in both.

### 7.1 Draft paragraph for Section 2.3 (agents and roles)

> Five groups trade or hold target shares while the challenger
> decides. The informed investor is an outside specialist, such as a
> sector-focused long-short fund. It forms its view of the challenger's
> match from its own research on the target's customers, technology,
> and demand, so its information does not come from either bidder or
> from the target. It holds no net exposure to the target before it
> trades; a holder that has hedged its shares is an outsider in this
> sense. Its order in state $L$ is a short sale, and $k$ includes the
> cost of borrowing shares. Noise demand is the net demand of liquidity
> traders, $Z=Z_+-Z_-$: existing shareholders sell $Z_-$ for reasons
> unrelated to the sale, and other investors buy $Z_+$; with independent
> exponential amounts of mean $b$, $Z$ has the Laplace density in (2).
> Competitive market makers absorb the net flow. Every share held at
> the sale, including market-maker inventory, receives $V_T$.

### 7.2 Draft paragraph for Section 6.1 (do shareholders gain?)

> Target shareholders gain from the mechanism through entry, not
> through the price. A shareholder who holds through the sale receives
> $V_T$, whatever the interim price. Entry raises proceeds with either
> challenger type, since $t_H>t_0$ and $t_L>t_0$, so each additional
> preparation decision raises the value of every share. At $r_1$, price
> access raises expected proceeds by 0.257809 per share, the dividend
> used in the diagnostic above. The informed investor's gross profit,
> 0.140731 at the benchmark scale, is a transfer from liquidity
> traders. If liquidity sales and purchases are independent exponential
> amounts, about three quarters of it falls on the outside buyers, and
> existing shareholders who sell bear 0.034694. Relative to an economy
> without the informed investor, existing shareholders then gain
> 0.223115 in total at the scale of one trading unit per share of
> float. This gain needs the recruiting region of Proposition 2, where high-cost
> preparation does not pay at the prior. When the prior already
> justifies high-cost preparation, an informative price deters some
> preparation and lowers expected proceeds, although it raises
> acquisition surplus.

## 8. Plain summary

The supervisor asked who trades on the information in this model, and
whether target shareholders gain.

The trader with information should be an outside specialist, such as
a sector fund that studies the target's customers and technology. Its
view is about how well a particular buyer fits the target, not about
whether a bid will come. That view is legal to trade on if it comes
from its own research. The fund needs no shares before it trades, and
it must be able to sell short. People who know the buyer's plans, such
as the buyer's bankers or lawyers, are the wrong candidates. Their
trading is illegal, and the buyer already knows what they know.

The "noise" traders can be shareholders who sell because they need
cash, and other investors who buy for their own reasons. This reading
also explains the noise law the paper uses.

Shareholders gain, but not from the price change itself. A shareholder
who keeps the shares gets the sale proceeds, not the interim price. The
gain comes because an informative price brings a second buyer into the
sale, and a second buyer raises the proceeds whichever type it is. At
the paper's numbers, the gain is 0.258 per share. Investors who
trade during the process pay the specialist's profit, mostly outside
buyers. The gain needs one condition: without the price,
the expensive buyer would stay out. If it would come in anyway, an
informative price can scare it off, and shareholders lose.

If the specialist already owned many shares, it would want a second
buyer even with bad news. It would then buy instead of sell. That
breaks the clean result. So the main model should keep an outside
specialist and treat a large holder as an extension.
