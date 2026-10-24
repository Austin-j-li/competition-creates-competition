# N4: Other strategic traders in the order slot

Date: 23 October 2026. Scripts: `scripts/N4_strategic_traders/`. Paper source: `overleaf/paper` commit `01bd5d6` only.
Base model: `memos/T2_liquidity_trader.md`, variant V3 two, with the checks of `memos/X_check.md`.

## 1. Question

The order slot has two identities: an informed investor and a liquidity trader.
Which new results appear when a trader with its own motive can fill the slot?
Four extensions are developed:

- N4.1 A holder with a stake buys to trigger entry (manipulation by an uninformed trader).
- N4.2 The challenger trades through the slot (toehold purchase and short sale).
- N4.3 The incumbent trades through the slot (jamming).
- N4.4 A foundation for the liquidity trader, and price-sensitive liquidity trade.

Main findings, one line each:

- N4.1: manipulation needs discovery; it has exact stake thresholds $\Omega_2<\Omega_1$; it recovers rising entry across 1.55, 1.60, 1.65.
- N4.2: a rare challenger cannot build a toehold where the price recruits; a frequent one creates a second, toehold equilibrium without discovery.
- N4.3: the incumbent never buys where the price recruits; its valuation trades jam discovery only when it fills the slot with probability at least $0.0765$.
- N4.4: a free holder with a small stake reproduces V3; price-sensitive liquidity makes the ceiling soft, with two equilibria on $[3.11,3.78]$.

### 1.1 Common setup

**Menu.** The informed investor orders $q\in\{-1,0,1\}$ at cost $k|q|$. Each other identity uses the same unit menu.

**Identity draw.** One public order slot. The informed investor fills it with probability $\lambda$ and sees the class $j\in\{H,L\}$.
Otherwise a non-informed identity fills it. The identity draw is independent of the class, the costs, and the incumbent value.
There is no separate noise. The flow $x$ equals the slot order.

**Base liquidity law.** Sell, wait, buy with probabilities $(\beta,1-2\beta,\beta)$. Calibration A: $\beta=1/3$, $\lambda=6/17$.
Write $b=(1-\lambda)\beta=11/51$ (liquidity buy mass, also the sell mass), $c=(1-\lambda)(1-2\beta)=11/51$ (liquidity wait mass), and
$M=(\lambda+b)/(\lambda+2b)=29/40$ (the top posterior under full informed orders).

**Auction objects** (paper equation (4), checked by direct integration in `common.py`). At $r=3$:
$t_0=5/12$, $t_L=7/8$, $t_H=37/24$, $w_L=t_L-t_0=11/24$, $w_H=t_H-t_0=9/8$, $\Delta=2/3$, $g_L=1/8$, $g_H=203/24$.
The recruiting posterior is $\tau(r)=(c_H-g_L)/(g_H-g_L)$: $\tau(6/5)=195/308$, $\tau(3)=141/200$, $\tau(18/5)=4245/5804$.
Write $W=w_L+\Delta\pi=w_L+\Delta/2$ for the uninformed entry gain per share; $W(3)=19/24$.

**Prices and entry.** Competitive market makers set $P(x)=\mathbb E[V_T\mid x]$. The challenger sees the price and its cost.
In each extension I check that the three prices are distinct, so the price reveals the flow.
Entry at posterior $\mu$ is $e(\mu)=\rho+(1-\rho)\mathbf 1\{B_r(\mu)\ge c_H\}$ with $B_r(\mu)=g_L+\mu(g_H-g_L)$.

**Equilibrium concept.** Perfect Bayesian equilibrium of the finite order game. Bayes' rule applies at every flow with positive mass.
An unused flow receives the passive prior belief; this case arises only at one boundary profile, noted in Section 2.1.

**Tie rules.** IM: a trader may mix at indifference. I0: a trader chooses zero at indifference. These apply to every trader with an order decision.
C1: the challenger prepares at indifference. CM: it may mix at indifference. The default pair is IM and C1. I state results under all four pairs where they differ.

**Status labels.** Closed forms with complete proofs are analytical. Exact fractions or rational brackets at stated points are computer-assisted. Grid evidence is a numerical diagnostic.

## 2. Extensions developed

### 2.1 N4.1 Manipulation by an uninformed holder

**Model change.** The non-informed filler is a holder with a stake $\omega\ge0$ in order units. The stake pays $V_T$, its cost is sunk, and it carries no control rights.
With probability $\beta$ a liquidity shock forces a sale. With probability $\beta$ a shock forces a purchase. With probability $1-2\beta$ the holder is free.
The free holder chooses $q$ to maximize

$$
\omega\,\mathbb E[V_T\mid q]+q\big(\mathbb E[V_T\mid q,\text{uninformed}]-P(q)\big)-k|q|.
$$

Both expectations use the prior $\pi=1/2$ on the class and the entry rule at the flow $q$. The informed investor holds no stake, as in the paper.
Let $m$ be the free holder's purchase probability and $m_-$ its sale probability; let $s$ and $t$ be the informed purchase and sale probabilities.
The class-conditional flow masses are

$$
\begin{aligned}
a_H(1)&=\lambda s+b+cm, & a_L(1)&=b+cm,\\
a_H(-1)&=b+cm_-, & a_L(-1)&=\lambda t+b+cm_-,\\
a_H(0)&=\lambda(1-s)+c(1-m-m_-), & a_L(0)&=\lambda(1-t)+c(1-m-m_-).
\end{aligned}
$$

Why this device: it nests V3 exactly at $m=m_-=0$, and the forced trades keep both nonzero flows on path. It also gives the uninformed trader a motive to trade on the real decision, as in Goldstein and Guembel (verified, `LIT_extracts.md` A2). Their mechanism uses two trade dates; this one uses the entry response in one date.

**Lemma 1 (the holder's gains) — analytical.** Against any schedule with entry $e(x)$ and posterior $\mu(x)$,

$$
G_+=\omega\,[e(1)-e(0)]\,W+e(1)\Delta[\pi-\mu(1)]-k,\qquad
G_-=\omega\,[e(-1)-e(0)]\,W+e(-1)\Delta[\mu(-1)-\pi]-k .
$$

*Proof.* Entry depends on the flow only through the price, and the cost is independent of the class. So $\mathbb E[V_T\mid j,x]=t_0+e(x)w_j$.
Average over the prior: $\mathbb E[V_T\mid x,\text{uninformed}]=t_0+e(x)W$. The price is $t_0+e(x)[w_L+\Delta\mu(x)]$.
Subtract: the uninformed residual at $x$ is $e(x)\Delta[\pi-\mu(x)]$. The stake term is $\omega$ times the change of $t_0+e(x)W$ between the flow $q$ and the flow $0$. $\square$

The stake pays terminal proceeds, not the interim price. The holder values a share at the prior; the market values it at $\mu(x)$. These are the two separate expectations above.

**Lemma 2 (structure) — analytical.** Suppose $s\ge t$ (this holds in every case below: the informed H buys fully whenever L sells at all). Then in every equilibrium:

- (a) $\mu(-1)\le1/2$ and $\mu(0)\le1/2$, so $e(-1)=e(0)=\rho$.
- (b) $G_-=\rho\Delta[\mu(-1)-1/2]-k<0$: the free holder never sells, at every stake and strength.
- (c) If flow 1 does not recruit, $G_+=\rho\Delta[1/2-\mu(1)]-k<0$ because $\mu(1)\ge1/2$: the free holder buys only if its purchase recruits. Manipulation needs discovery.
- (d) If flow 1 recruits, $G_+(m)=\omega(1-\rho)W-\Delta[\mu(1;m)-1/2]-k$ with $\mu(1;m)=(\lambda s+b+cm)/(\lambda s+2b+2cm)$ strictly decreasing in $m$. So $G_+$ strictly increases in $m$: each free purchase lowers the mimic's loss of the next one.

*Proof.* (a) $a_H(-1)\le a_L(-1)$ directly. $a_H(0)\le a_L(0)$ iff $s\ge t$. Both posteriors are below $\tau>1/2$. (b), (c), (d) follow from Lemma 1 and $a_H(1)\ge a_L(1)$. $\square$

**Proposition 1 (phase in the stake) — analytical.** Fix $r$ with full informed purchase ($r_F\le r<r_C$, where $\Delta(r_F)=4/55$ and $\tau(r_C)=M$). Define

$$
\Omega_1=\frac{\Delta(M-\tfrac12)+k}{(1-\rho)W},\qquad
\Omega_2=\frac{\Delta(\tau-\tfrac12)+k}{(1-\rho)W},\qquad
m_{\max}=\frac{\lambda(1-\tau)-b(2\tau-1)}{c(2\tau-1)} .
$$

Since $\tau<M$, $\Omega_2<\Omega_1$ and $m_{\max}>0$; $m_{\max}$ is the free purchase probability at which $\mu(1)=\tau$. Under IM and CM the equilibria with $s=1$ are exactly:

| Label | Free holder | Entry at flow 1 | Exists iff |
|---|---|---|---|
| V3 | $m=0$ | $1$ | $\omega\le\Omega_1$ |
| M | $m=m^*=\dfrac{\lambda\Delta/(2A)-\lambda-2b}{2c}$, $A=\omega(1-\rho)W-k$ | $1$ | $\Omega_2<\omega<\Omega_1$ (and $m^*<\min\{m_{\max},1\}$) |
| M′ | $m=m_{\max}\le1$ | $e^*=\dfrac{k+\rho\omega W}{\omega W-\Delta(\tau-\tfrac12)}$ | $\omega\ge\Omega_2$, and $e^*\Delta(1-\tau)\ge k$ |

If $m_{\max}>1$, replace $m_{\max}$ by $1$ in M and add the pure profile $m=1$ with entry $1$ for $\omega\ge[\Delta(\mu(1;1)-\tfrac12)+k]/[(1-\rho)W]$.
Under C1, M′ exists only at $\omega=\Omega_2$, where $e^*=1$. Under I0, M and M′ do not exist. No equilibrium has $m>m_{\max}$.
The informed L sells at the rate of T2, equation (31); it does not affect flow 1.

*Proof.* By Lemma 2(c), a profile with $m>m_{\max}$ has $e(1)=\rho$ and $G_+<0$, so the free holder would not buy. Hence $m\le m_{\max}$.
For $m=0$ with $e(1)=1$: $G_+(0)\le0$ iff $\omega\le\Omega_1$, by substitution of $\mu(1;0)=M$.
For $0<m<m_{\max}$ with $e(1)=1$: IM requires $G_+(m)=0$. By Lemma 2(d) the root is unique; solve $\Delta\lambda/[2(\lambda+2b+2cm)]=A$ for $m^*$.
A root exists iff $G_+(0)<0<G_+(m_{\max})$. Substitution of $\mu(1;m_{\max})=\tau$ gives $G_+(m_{\max})=\omega(1-\rho)W-\Delta(\tau-\tfrac12)-k$, which is positive iff $\omega>\Omega_2$.
For $m=m_{\max}$: the challenger is indifferent and may mix (CM). Write $G_+=\omega(e-\rho)W+e\Delta(\tfrac12-\tau)-k$; it is linear in $e$ with slope $\omega W-\Delta(\tau-\tfrac12)$.
At $e=\rho$ it equals $-k<0$. At $e=1$ it is nonnegative iff $\omega\ge\Omega_2$. Then a unique $e^*\in(\rho,1]$ solves $G_+=0$; the slope is positive because $\Omega_2>\Delta(\tau-\tfrac12)/W$.
The informed H purchase has return $e(1)\Delta[1-\mu(1)]$. In V3 and M this is at least $\Delta(1-M)\ge k$ for $r\ge r_F$. In M′ it is $e^*\Delta(1-\tau)$, which gives the stated condition.
Wrong-signed informed orders lose by T2, Section 3.2. The L sale return does not involve flow 1. $\square$

**Corollary (the Proposition 2 analog) — analytical.**

- (i) At $r_0=6/5$: $\Delta=1/60<k$, so $s=0$ against every schedule; then $\mu(1)=1/2$, flow 1 does not recruit, and Lemma 2(c) gives $m=0$. No trade is the unique outcome for every stake.
  The stake belongs to the holder, not to the informed investor, so nothing can trigger the top flow. This part was fragile in C5 (binding at $\omega=0.18$); here it is robust.
- (ii) At $r_1=3$: V3 is the unique equilibrium iff $\omega<\Omega_2(3)=376/1425\approx0.2639$ (IM, CM). Under C1 and IM it is unique iff $\omega\le\Omega_2$.
  Under I0 it is unique iff $\omega\le\Omega_1(3)=136/475\approx0.2863$. For $\omega>\Omega_1$ no equilibrium exists under C1 or I0; under CM and IM only M′ exists.
- (iii) At $r_2=18/5$: full informed orders hold by T2's bound, $\mu(1;m)\le M<\tau(18/5)$ for every $m$, so flow 1 never recruits and $m=0$. Entry is $\rho$ for every stake.

The nonexistence above $\Omega_1$ under the paper's tie rules is the same failure as C5, Proposition 4. An entry jump at the posterior $\tau$ cannot be crossed without a challenger mixture. It is a documented failure, not a gap in the computation.

**Benchmark values at $r=3$ — computer-assisted** (`n41_holder.py`, output `n41_holder.out.txt`; every profile verified by direct best responses of the holder, both informed classes, and the challenger, under all four tie pairs):

| Stake $\omega$ | Equilibria (IM/CM) | Free purchase $m$ | $e(1)$ | Entry $\mathsf E$ |
|---|---|---|---|---|
| $0$, $1/10$, $1/4$ | V3 only | $0$ | $1$ | $37/68$ |
| $\Omega_2=376/1425$ | V3; M′ with $e^*=1$ | $0$; $80/451$ | $1$ | $37/68$; $1597/2788$ |
| $392/1425$ | V3; M; M′ | $0$; $m^*$ with $\mu(1)=143/200$; $80/451$ | $1$; $1$; $67/73$ | $0.5441$; $0.5578$; $0.5374$ |
| $\Omega_1=136/475$ | V3 (holder indifferent); M′ | $0$; $80/451$ | $1$; $e^*<1$ | $0.5441$; $0.5090$ |
| $1$ | M′ only | $80/451$ | $523/1572$ | $0.2856$ |
| $10$ | M′ only | $80/451$ | $2399/9336$ | $0.2530$ |

A grid of 200 purchase probabilities confirms the sign structure of $G_+$: one root at $m^*$ inside the recruiting range when $\Omega_2<\omega<\Omega_1$, and a downward jump at $m_{\max}$.
At $r=6/5$ and $r=18/5$ the largest holder gain over the grid is $-k$ and $-0.0541$ for $\omega\in\{0,1,10,100\}$.
The profile $m=1$ with $t=1$ leaves flow 0 unused; it never recruits at $r=3$, so it is not an equilibrium under any belief there.

**Comparison with C5.** In the three-point model with an informed low-class manipulator, $\Omega_2(3)=152/75\approx2.03$ and $\Omega_1(3)\approx2.60$.
The slot thresholds are about eight times smaller. Two reasons: a slot purchase reaches the recruiting flow with certainty, while a three-point purchase reaches it with probability $1/3$; and the uninformed holder's entry gain is $W=w_L+\Delta/2$, not $w_L$.
The slot makes manipulation cheap.

**Phase in strength — numerical diagnostic on the grid, exact at each point.** On $[r_F,r_C)=[1.4610,3.4582)$ both thresholds rise with $r$:

| $r$ | $1.47$ | $1.55$ | $1.60$ | $1.65$ | $2$ | $2.5$ | $3$ | $3.4$ |
|---|---|---|---|---|---|---|---|---|
| $\Omega_2$ | $0.0907$ | $0.0978$ | $0.1024$ | $0.1073$ | $0.1448$ | $0.2032$ | $0.2639$ | $0.3133$ |
| $\Omega_1$ | $0.1087$ | $0.1195$ | $0.1264$ | $0.1333$ | $0.1807$ | $0.2395$ | $0.2863$ | $0.3166$ |
| $m_{\max}$ | $1.029$ | $0.969$ | $0.932$ | $0.897$ | $0.672$ | $0.403$ | $0.177$ | $0.021$ |

Manipulation is cheapest where discovery has just started, because the camouflage loss $\Delta(\mu-\tfrac12)$ is small there, and dearest at the ceiling.
For $r\le1.5$ the free holder can buy with certainty and flow 1 still recruits.

**The three intermediate strengths — computer-assisted.** At $31/20$, $8/5$, $33/20$, no trade is an equilibrium for every stake ($r\le r_N$; the free holder's deviation earns $-k$).
For $\omega\in[\Omega_1(33/20),\bar\omega_H(31/20))=[859/6445,\,0.1831)$, Proposition 1 leaves M′ as the unique informative equilibrium at each strength (IM, CM).
Here $\bar\omega_H(r)=k\Delta/(2W[k-\rho\Delta(1-\tau)])$ is the stake at which $e^*\Delta(1-\tau)=k$. Its entry rises strictly across the three strengths:

| $\omega$ | $\mathsf E(31/20)$ | $\mathsf E(8/5)$ | $\mathsf E(33/20)$ |
|---|---|---|---|
| $7/50$ | $0.526748$ | $0.535758$ | $0.546267$ |
| $3/20$ | $0.503570$ | $0.510910$ | $0.519454$ |

The reason: $e^*$ has denominator $\omega W-\Delta(\tau-\tfrac12)$, and $\Delta(\tau-\tfrac12)$ rises faster in $r$ than $\omega W$. A stronger incumbent raises the holder's camouflage loss, so the challenger must enter more often to keep the holder indifferent.
This recovers the feature that V3 lost: coexistence of no trade with an informative equilibrium whose entry rises across 1.55, 1.60, 1.65. The cost is the tie rule CM and a stake in a narrow window.
At $\omega=11/100$ all three informative branches coexist, and each rises across the three strengths (V3 is flat at $37/68$; M gives $0.5968,0.6329,0.6678$; M′ gives $0.6313,0.6501,0.6724$).

**Welfare at $r=3$ — computer-assisted** (per share; $\mathcal W$ is the winner's value less preparation and trading costs; the identity $S=T+\text{incumbent}+\text{challenger}+\text{preparation}$ holds exactly in every row):

| Outcome | Proceeds $T$ | Challenger net | Incumbent | Informed | Holder trade | Holder total | $\mathcal W$ |
|---|---|---|---|---|---|---|---|
| hidden price | $0.6146$ | $1.0729$ | $0.8646$ | $0.0091$ | $-0.0248$ | $\omega T-0.0248$ | $2.5364$ |
| V3 | $0.8915$ | $1.1219$ | $0.6121$ | $0.0334$ | $-0.0491$ | $\omega T-0.0491$ | $2.6099$ |
| M, $\omega=0.27$ | $0.9076$ | $1.0872$ | $0.5977$ | $0.0351$ | $-0.0498$ | $0.1953$ | $2.5764$ |
| M′, $\omega=\Omega_2$ | $0.9143$ | $1.0729$ | $0.5918$ | $0.0357$ | $-0.0501$ | $0.1912$ | $2.5625$ |
| M′, $\omega=0.3$ | $0.8292$ | $1.0729$ | $0.6692$ | $0.0284$ | $-0.0431$ | $0.2057$ | $2.5549$ |
| M′, $\omega=1$ | $0.6476$ | $1.0729$ | $0.8345$ | $0.0126$ | $-0.0281$ | $0.6195$ | $2.5386$ |
| M′, $\omega=10$ | $0.6174$ | $1.0729$ | $0.8621$ | $0.0099$ | $-0.0257$ | $6.1480$ | $2.5359$ |

Readings:

- Near the threshold, manipulation creates value for target shareholders: proceeds rise from $0.8915$ to $0.9143$. For a large stake they fall toward the hidden-price level.
- Manipulation destroys most of the social value of discovery: $2.6099\to2.5625$ at $\Omega_2$, and to $2.5359$ at $\omega=10$, against $2.5364$ with the price hidden. The loss is the preparation cost $c_H$ of fooled entry in class L.
- The challenger loses its whole rent in M′: it is indifferent at the recruiting flow, and its payoff equals the hidden-price value $103/96$. The incumbent gains it back as the stake grows.
- The holder gains from manipulation at $\omega=0.27$ ($0.1953$ against $0.1917$ in V3 at the same stake). At $\omega=1$ it earns $0.6195$ in M′ against $0.8425$ if it could commit not to manipulate. A large holder would pay for such a commitment.

**Status.** Lemmas 1 and 2, Proposition 1, and the Corollary: analytical. Benchmark values, the entry triple, and the welfare ledger: computer-assisted. The phase table: numerical diagnostic.

**Testable prediction.** Where a large non-bidding holder owns the target, abnormal purchases precede preparation, and entry after a price rise is less than certain and falls with the holder's stake. Entry triggered by such purchases is marginal (the challenger is indifferent), and a share $1-\tau$ of it occurs in the low class.

### 2.2 N4.2 The challenger in the slot

**Model change.** The challenger learns its cost before the slot; this is a timing change from the paper, as in C10, Result T3.
With probability $\chi$ it fills the slot and submits one order. Identity probabilities are $(\lambda,\chi,1-\lambda-\chi)$.
The liquidity buy and sell masses are held at calibration A's $b=11/51$: the liquidity trader sells and buys with probability $b/(1-\lambda-\chi)$ each.
The challenger's presence therefore replaces liquidity abstentions, and $\chi\le2/17$ keeps the abstention probability above $0.185$. This separates the strategic effect from a mechanical loss of camouflage.
Bids stay truthful. The challenger in the slot knows that the flow is its own, so it decides on the prior. The low-cost type prepares; the high-cost type does not, because $B_r(1/2)<c_H$ at all three strengths ($4.29$ at $r=3$).
The challenger outside the slot conditions on "not in the slot". Its posterior $\mu_{\rm out}(x)$ excludes the challenger's own mass. The market maker's posterior $\mu_{\rm mm}(x)$ includes it.
The price at $x$ sums the terminal value over identities, with each in-slot type's own entry.

**Lemma 3 (in-slot gains against the V3 schedule, limit $\chi\to0$) — analytical.**

$$
\text{low-cost purchase: } (1-e(1))\,w_L+\Delta[\tfrac12-e(1)\mu(1)]-k,\qquad
\text{high-cost sale: } \rho\,[w_L+\Delta\mu(-1)]-k .
$$

*Proof.* The low-cost type values a share at $t_0+w_L+\Delta/2$: it enters for sure and holds the prior. The price at flow 1 is $t_0+e(1)[w_L+\Delta\mu(1)]$.
The high-cost type values a share at $t_0$: it does not enter. The price at flow $-1$ is $t_0+\rho[w_L+\Delta\mu(-1)]$. Subtract and pay $k$. $\square$

| $r$ | $e(1)$ | $\mu(1)$ | Low-cost purchase gain | High-cost sale gain |
|---|---|---|---|---|
| $6/5$ | $\rho$ | $1/2$ | $453/1600=0.2831$ | $389/4800=0.0810$ |
| $3$ | $1$ | $29/40$ | $-17/100=-0.1700$ | $337/2400=0.1404$ |
| $18/5$ | $\rho$ | $29/40$ | $6031/9600=0.6282$ | $4633/28800=0.1609$ |

Where the price recruits, the purchase is priced as a possibly informed purchase with certain entry; the low-cost challenger loses the information rent $\Delta(\mu(1)-\tfrac12)+k$ and abstains.
Where it does not recruit, the market under-weights the challenger's certain entry, and the purchase earns $(1-\rho)w_L$ plus a small information term. The high-cost type sells everywhere: the price over-weights entry relative to its own zero entry.

**Equilibria — computer-assisted** (`n42_challenger.py`; all pure challenger profiles, informed pure orders and exact indifference roots, IM and C1):

| $r$ | $\chi$ | Equilibria |
|---|---|---|
| $6/5$ | $1/51,\,1/17,\,2/17$ | Unique: no informed trade; low-cost buys, high-cost sells; entry $1/4$. |
| $3$ | $1/51,\,1/17$ | Unique: full informed orders; low-cost abstains; high-cost sells; entry $37/68$, ownership $23/68$, proceeds $485/544$, as in V3. |
| $3$ | $2/17$ | Two: (a) discovery, $s=1$, $t=0.5058$, low-cost abstains, entry $37/68$; (b) toehold, $s=0$, low-cost buys, $t=0.5058$, entry $1/4$. |
| $18/5$ | $1/51,\,1/17$ | Unique: full informed orders; low-cost buys, high-cost sells; entry $1/4$. |
| $18/5$ | $2/17$ | Unique: $s=0.9192$ (the challenger's purchases raise $P(1)$), $t=1$; low-cost buys, high-cost sells; entry $1/4$. |

The informed L mixes at $\chi=2/17$ because the high-cost challenger's sales pull $P(-1)$ toward $t_0$ until the L sale return equals $k$ exactly.

**The crowding-out threshold — analytical.** In the toehold profile at $r=3$, flow 1 carries liquidity purchases (value $v_{\rm liq}=t_0+\rho W=59/96$) and low-cost challenger purchases (value $v_{\rm ch}=t_0+W=29/24$).
The informed H purchase there is worth $v_H=t_0+\rho w_H=67/96$, because flow 1 does not recruit. The profile is an equilibrium iff $v_H-P(1)-k\le0$ with $P(1)=(b\,v_{\rm liq}+\chi\rho\,v_{\rm ch})/(b+\chi\rho)$, that is iff

$$
\chi\ \ge\ \bar\chi=\frac{b\,(v_{\rm liq}-v_H+k)}{\rho\,(v_H-k-v_{\rm ch})}=\frac{352}{3417}\approx0.1030 .
$$

The enumeration at $\bar\chi\mp10^{-3}$ confirms the switch. Just above $\bar\chi$ the toehold equilibrium still recruits through the abstention flow: with $s=0$ and $t=0.896$, an abstention signals class H, $\mu_{\rm out}(0)=0.758$, and entry is $0.480$. At $\chi=2/17$, $t$ falls to $0.506$, no flow recruits, and entry is $1/4$.

**The Proposition 2 analog.** With the liquidity masses held fixed, parts (i) and (iii) hold for every $\chi\le2/17$, and part (ii) holds uniquely for $\chi<\bar\chi$.
With the plain liquidity law instead ($\beta=1/3$ for the liquidity trader, so $b$ falls with $\chi$), part (iii) fails for $\chi\ge742/22831\approx0.0325$ because $M(\chi)$ rises above $\tau(18/5)$. That failure is a mechanical loss of camouflage, not a toehold effect.

**Reading.** A rare challenger cannot profit from a toehold where the price recruits, and the discovery channel is intact. A frequent challenger creates a coordination failure.
If the informed investor abstains, a purchase is priced with the challenger's certain entry, and the informed purchase loses. If it buys, flow 1 recruits and the challenger's purchase loses.
The challenger that will not bid sells the target short. The legal status of such orders is outside the model and unverified. Kyle–Vila and Bagnoli–Lipman are abstract-only records (`L1_survey.md` C18, C20) and are cited as unverified.

**Testable prediction.** Bidder toehold purchases concentrate where the price does not move entry: weak incumbents and incumbents above the ceiling. In the recruiting band, prospective bidders do not buy before they prepare. Prospective bidders that walk away have sold before they walk.

**Status.** Lemma 3 and the threshold $\bar\chi$: analytical. The equilibrium tables: computer-assisted. Mixed challenger strategies are not enumerated (open).

### 2.3 N4.3 The incumbent in the slot

**Model change.** The incumbent knows its own value $R\sim U[0,r]$ and not the class. With probability $\chi$ it fills the slot and submits one order.
Identity probabilities are $(\lambda,\chi,1-\lambda-\chi)$, with the liquidity masses held at $b=11/51$ as in N4.2.
Its payoff is the trade, $q(V_T-P(q))-k|q|$, plus $\zeta$ times its auction profit, which is $(R-p)^+$ without a challenger and $(R-\theta_j)^+$ with one.
The scale $\zeta\ge1$ stands for the number of target shares per order unit; the auction profit is per target share. I report $\zeta=1$ and $\zeta=10$.
The challenger is never in the slot. It sees the price; the three prices are distinct in every case below, so it infers the flow.
Its posterior $\mu_{\rm mm}(x)$ includes the incumbent's orders, because it does not know who filled the slot.
Conditional on $R$ and entry $e$, the share is worth $(1-e)\,p\,\mathbf 1\{R\ge p\}+e\,\mathbb E_j\max\{p,\min(R,\theta_j)\}$.
The incumbent's strategy is a cutoff rule: sell iff $R<R_s$, buy iff $R\ge R_b$. Each cutoff is a one-dimensional fixed point, because $P(-1)$ depends on the sellers' value distribution and $P(1)$ on the buyers'.
The script solves each by bisection with exact signs and checks the rule against all three orders at 61 values of $R$.

**Result N4.3.1 (no purchase where the price recruits) — analytical at the benchmark.** At $r=3$ in the recruiting equilibrium ($e(1)=1$, $e(0)=e(-1)=\rho$), an incumbent with value $R\ge1$ gains from a purchase

$$
\frac{1+R}{2}-P(1)-k-\zeta(1-\rho)\frac{R}{2}=\frac12+\frac{R}{2}\big[1-\zeta(1-\rho)\big]-P(1)-k .
$$

*Derivation.* With entry, the share pays $\tfrac12\cdot1+\tfrac12 R$ (the incumbent beats the low class at price 1 and loses to the high class at price $R$). Its auction profit falls from $R-p$ to $\tfrac12(R-1)$, a loss of $R/2$, times the entry increase $1-\rho$.
For $\zeta=1$ the expression is linear in $R$ with slope $1/8$, so its maximum on $[1,3]$ is at $R=3$: $\tfrac12+\tfrac38-\tfrac{163}{120}-\tfrac1{50}=-0.5033<0$. For $R<1$ the share is worth less and the expression is smaller. For $\zeta>1$ the slope is negative. $\square$
The incumbent never buys at a recruiting flow, at every presence $\chi$ and every scale. The script confirms $R_b=r$ at $\chi\in\{1/51,\dots,11/51\}$ and $\zeta\in\{1,10\}$.

**Result N4.3.2 (the low-value incumbent sells) — computer-assisted.** At $r=3$ the incumbent sells iff $R<R_s$, with $R_s\approx0.713$ at $\chi=1/51$ and $0.640$ at $\chi=2/17$.
Such an incumbent knows that its own bid fails the reserve or barely clears it, so the share is worth less to it than the sale price $P(-1)\approx0.57$.
Its sales pool with the informed low-class sale and pull $P(-1)$ toward $t_0$. The full-order recruiting equilibrium is verified on a grid of step $1/510$ up to $\chi=71/510\approx0.139$. From $\chi=12/85\approx0.141$ the informed L sale return turns negative. Then L must mix; that case is not classified. Entry and ownership are unchanged: flow $-1$ never recruits.

**Result N4.3.3 (a jammed equilibrium needs a frequent incumbent) — computer-assisted.** Consider the hypothesis that flow 1 does not recruit. Then flows 0 and 1 carry the same entry $\rho$, the auction term drops out of the incumbent's order comparison, and the scale $\zeta$ is irrelevant.
An incumbent with $R\ge R_b$ buys because its own high bid makes the share worth more than the price. Here $R_b\approx1.47$ at $\chi=13/170$ and $1.51$ at $\chi=2/17$, with a buy share near one half.
Its purchases dilute the challenger's posterior: $\mu_{\rm mm}(1)=(\lambda+b+\chi q)/(\lambda+2b+2\chi q)$ with $q=\Pr(R\ge R_b)$.
The hypothesis is self-consistent iff $\mu_{\rm mm}(1)<\tau(3)$, which on a grid of step $1/510$ first holds at $\chi=13/170\approx0.0765$ ($\mu_{\rm mm}(1)=0.7046$). At $\chi=1/17$ it fails ($0.7088$); at $\chi=2/17$ it holds ($0.6958$).
So for $\chi\ge0.0765$ a jammed equilibrium coexists with the recruiting one at $r=3$: no flow recruits, entry is $\rho$, and discovery fails. Selection between the two is open.

| $r$ | $\chi$ | Recruiting equilibrium | Jammed or non-recruiting equilibrium |
|---|---|---|---|
| $3$ | $1/51,\,1/17$ | $R_b=r$, $R_s\approx0.71,0.68$; entry $37/68$ | none ($\mu_{\rm mm}(1)>\tau$) |
| $3$ | $2/17$ | $R_b=r$, $R_s\approx0.64$; entry $37/68$ | $R_b\approx1.51$, $R_s\approx0.64$; entry $1/4$ |
| $18/5$ | all | none ($M<\tau$) | $R_b\approx1.92$ to $2.10$, $R_s\approx0.85$ to $0.72$; entry $1/4$ |
| $6/5$ | all | none (no informed trade) | sell iff $R<p$, buy iff $R\ge p$; entry $1/4$ |

**Reading.** In the slot a trader can trigger entry but cannot jam it by intent. Jamming would have to be anticipated. In the recruiting equilibrium the incumbent's own purchase raises entry, and that costs it more than any trading gain.
Jamming occurs only as a by-product of the incumbent's ordinary trading on its own valuation. It needs an incumbent in the slot often enough to be mistaken for the informed investor.
This is the mirror image of N4.1: the beneficiary of entry can create the recruiting flow; the victim of entry cannot remove it. Parts (i) and (iii) of Proposition 2 hold for every $\chi\le2/17$; part (ii) is unique for $\chi<0.0765$.
The scale caveat runs one way: a larger $\zeta$ only strengthens abstention in the recruiting equilibrium and leaves the jammed equilibrium unchanged.

**Testable prediction.** Incumbent bidders do not buy target shares in the window where the price recruits; they sell when their own valuation is low. Where incumbents trade often, order flow is less informative and entry responds less to prices.

**Status.** N4.3.1 analytical at the benchmark values. N4.3.2 and N4.3.3 computer-assisted (rational brackets; 61-point best-response checks). Mixed informed sales for $\chi\ge3/17$ and selection: open.

### 2.4 N4.4 A foundation for the liquidity trader, and price-sensitive liquidity trade

**(a) The holder with liquidity shocks — analytical (corollary of Proposition 1).**
A free holder with no stake abstains at every outcome (T2, Section 3.7; X_check claim 6). With a stake $\omega<\Omega_2(r)$ under IM and CM, or $\omega\le\Omega_1(r)$ under I0, the free holder also abstains, and V3 is the unique equilibrium.
So V3 is the reduced form of a holder with exogenous liquidity shocks and a small stake. The shocks stay exogenous: the stake adds only a threshold below which a free choice changes nothing.
Admati and Pfleiderer (verified, `L1_survey.md` C11) supply a shock that forces a sale of exactly the informed order's size. A forced purchase shock has no verified precedent; it stays open.

**(b) Price-sensitive liquidity trade.** My reading of "the liquidity probability responds to prices" is this. Participation responds to the cost of trading at the anticipated price, which is the adverse-selection cost at the flow plus $k$.
The alternative reading, participation as a function of the price level, was not run.

*Model change.* The non-informed filler has no stake. With probability $\hat\beta$ it has a purchase motive, and with probability $\hat\beta$ a sale motive; the motive carries a private benefit $v\sim U[0,\bar v]$ per unit.
It buys iff $v\ge\kappa_+=e(1)\Delta[\mu(1)-\tfrac12]+k$ and sells iff $v\ge\kappa_-=e(-1)\Delta[\tfrac12-\mu(-1)]+k$ (Lemma 1 with $\omega=0$). Participation is $1-\kappa/\bar v$.
The buy mass $b_+=(1-\lambda)\hat\beta(1-\kappa_+/\bar v)$ is a fixed point, because $\mu(1)=(\lambda+b_+)/(\lambda+2b_+)$ under full informed orders.
Calibration: $\hat\beta=2/5$ and $\bar v=51/50$ reproduce $b_+=11/51$ at $r=3$ on the recruiting piece, so calibration A is nested.

*Lemma 4 (existence) — analytical.* Write $\hat B=(1-\lambda)\hat\beta$ and $\varphi(b)=\hat B\max\{0,1-\kappa_+(b)/\bar v\}$. On each entry piece $\kappa_+$ falls in $b$, so $\varphi$ rises; at $b_\tau$ (where $\mu(1)=\tau$) the entry drops from $1$ to $\rho$, so $\varphi$ jumps up.
Then $\psi(b)=\varphi(b)-b$ has $\psi(0)>0$, because $\kappa_+(0)=\Delta/2+k<\bar v$. Also $\psi(\hat B)\le0$, and $\psi$ has only an upward jump. An upward jump cannot carry $\psi$ from positive to nonpositive, so $\psi$ crosses zero continuously. A fixed point exists. $\square$

*Closed form.* On a piece with entry $e_1$, the fixed point solves

$$
2b^2+\big[\lambda-2\hat B(1-k/\bar v)\big]b-\hat B(1-k/\bar v)\lambda+\frac{\hat B e_1\Delta\lambda}{2\bar v}=0 .
$$

A root is an equilibrium iff its own piece is self-consistent: $\mu(1;b)\ge\tau$ on the recruiting piece, $\mu(1;b)<\tau$ on the other.

*Results — computer-assisted* (`n44_liquidity.py`, rational root brackets):

| $r$ | Recruiting piece ($e_1=1$) | Non-recruiting piece ($e_1=\rho$) | Equilibria |
|---|---|---|---|
| $6/5$ | no informed trade | $b=220/867$, $\mu=1/2$ | unique, entry $\rho$ |
| $3$ | $b=11/51$, $\mu(1)=29/40\ge\tau$: consistent | $b=0.24489$, $\mu(1)=0.7094>\tau$: inconsistent | unique, entry $37/68$ |
| $18/5$ | $b=0.19754$, $\mu(1)=0.7359\ge\tau$: consistent | $b=0.24117$, $\mu(1)=0.7113<\tau$: consistent | two (under C1) |

Both pieces are self-consistent exactly for $r\in[3.1106,3.7839]$ (brackets to nine digits), under C1. The fixed-noise ceiling $r_C=3.4582$ lies inside this band.
Under CM a third fixed point with a mixing challenger may sit at $\mu(1)=\tau$ inside the band; it is not computed.
Below $3.1106$ the recruiting equilibrium is unique; above $3.7839$ the non-recruiting one is unique.
In the thin equilibrium at $18/5$, uninformed purchase participation is $0.763$; in the thick one it is $0.932$.

*Reading.* The entry response raises the adverse-selection cost of an uninformed purchase by the factor $1/\rho=4$. Uninformed buyers withdraw exactly when the price recruits.
Thinner camouflage raises the recruiting posterior, so recruitment is self-fulfilling on a band of strengths. The information ceiling becomes soft: at $r_2=18/5$ the return to the floor is one of two equilibria.
Proposition 2(iii) therefore holds only as a selection. The informed H purchase and the L sale remain strict best responses on both pieces (returns $0.228$ and $0.048$ at $18/5$).

*Testable prediction.* Uninformed purchase participation drops, and the informed share of purchases jumps, when the price starts to recruit. In the band of strengths near the ceiling, entry can switch with liquidity conditions that have no fundamental content.

**Status.** (a) analytical. (b) Lemma 4 analytical; the closed form analytical; the benchmark values and the band computer-assisted. The L sale side and the coexistence region ($r\le r_N$) are not analysed under price-sensitive participation (open).

## 3. Ideas considered and dropped

- **A stake for the informed investor.** Done in C5 and Online Appendix A.12; the slot version would repeat Lemma 1 with $w_j$ in place of $W$. Not redone.
- **The Goldstein–Guembel two-date inventory mechanism** (sell, depress the decision, buy back). It needs two trade dates; that is N2's direction.
- **Control rights or tendering for the holder.** The paper's sale mechanism binds all shares; a holder with control changes the auction, not the slot.
- **A challenger with class information at the slot.** It violates Reading N; under Reading N the challenger's order reveals its cost only.
- **Bid shading with a toehold.** Bulow, Huang and Klemperer is abstract-only; C10 open issue 7. Bids stay truthful here.
- **Continuous order sizes for the incumbent or the challenger.** The unit menu keeps every flow on path; a fractional order needs an off-path belief (X_check, Section 4, item 2).

## 4. Ranking

1. **N4.1 Manipulation by an uninformed holder.** Exact thresholds, a complete phase, a welfare ledger, and the recovery of rising entry across 1.55, 1.60, 1.65. Strongest and most interesting.
2. **N4.4(b) Price-sensitive liquidity.** A new multiplicity band around the ceiling with a clean fixed-point structure and a sharp participation prediction.
3. **N4.2 The challenger in the slot.** A clean closed-form threshold for crowding-out and a short-sale result; the toehold equilibrium needs a frequent challenger.
4. **N4.3 The incumbent in the slot.** A clean asymmetry (trigger yes, jam no) and a presence threshold for a jammed equilibrium. The scale of the incumbent's auction stake is a caveat.

## 5. Open issues

- **N4.1.** Below $r_F$ the informed rate and the holder's rate are coupled; not classified. Above $\bar\omega_H$ at low strength, M′ needs a partial informed purchase; not classified. Selection among V3, M, M′ is open; M has the unstable complementarity noted in C5. Whether $\Omega_1$ and $\Omega_2$ are monotone in $r$ is a grid result. The stake is in order units, not a share of equity. A privately known stake is not studied.
- **N4.2.** Mixed challenger strategies and $\chi>2/17$ are not enumerated. The timing change (cost known before the slot) is an assumption. The legal status of a prospective bidder's short sale is unverified.
- **N4.3.** The scale $\zeta$ is a free parameter; the results are stated for $\zeta\ge1$. Mixed informed sales for $\chi\ge12/85$ are not classified. Selection between the recruiting and the jammed equilibrium is open. The cutoffs are rational brackets, not closed forms.
- **N4.4.** Under CM a third equilibrium with a mixing challenger at $\mu(1)=\tau$ may exist in the band; not computed. The forced purchase shock has no verified precedent. The sale side under price-sensitive participation and the coexistence region are not analysed. A holder with both a stake and price-sensitive participation is not studied. The price-level reading of "responds to prices" was not run.

## 6. Plain summary

Four traders with their own motives can fill the order slot.

A holder with a stake can buy to trigger entry. It never sells, and buys only where its purchase recruits the high-cost challenger: manipulation needs discovery.
At strength 3 the pure slot outcome survives for stakes below $0.264$ order units. Between $0.264$ and $0.286$ it coexists with two manipulation outcomes. Above $0.286$ only a manipulation outcome with a mixing challenger exists, and the paper's tie rules give no equilibrium.
These thresholds are about eight times smaller than in the three-point model, because a slot purchase reaches the recruiting flow for sure.
The weak and very strong economies are immune at every stake. Manipulation raises proceeds near the threshold, moves the challenger's rent to shareholders, and destroys most of the social value of discovery.
At the intermediate strengths a stake between $0.133$ and $0.183$ gives one informative equilibrium whose entry rises strictly across 1.55, 1.60, 1.65. The slot had lost that feature.

The challenger cannot build a toehold where the price recruits: its purchase is priced as a possibly informed one. It buys where the price does not recruit, and the type that will not bid sells short.
If the challenger fills the slot with probability above $0.103$, a second equilibrium appears in which its purchases crowd out the informed purchase.

The incumbent never buys where the price recruits, because its purchase would raise entry. It sells when its own value is low. If it fills the slot with probability above $0.0765$, its valuation trades jam discovery as a by-product.

The liquidity trader can be a holder with shocks and a small stake. If liquidity participation responds to the cost of trading, the ceiling becomes soft: on strengths $3.11$ to $3.78$ a thin-liquidity recruiting equilibrium coexists with a thick-liquidity one.
