# Q3 (welfare): Who gains from the price change? A group-by-group decomposition

## 1. Question and reading

Point 3 asks who the investors are. If they are target shareholders,
should they not gain from the stock price change in any case? This memo
builds the formal accounting. It does not treat the stake extension
(initial position $\omega>0$ for the informed investor) and it does not
treat the narrative. Other memos cover those parts.

The short answer has three parts. First, the price change itself is a
transfer. It creates no value for target shareholders as a group.
Second, price-induced entry is real. It raises expected target
proceeds. Third, the trading loss falls only on shareholders who
trade. The entry gain accrues to all holders in proportion to
holdings. The two groups can therefore disagree, even when
shareholders in total gain.

## 2. Formal setup

Notation follows the paper. Values are per target share. The reserve
satisfies $0<p<\ell<r<h$. The incumbent value is $R\sim U[0,r]$. The
challenger value is $\theta\in\{\ell,h\}$ with prior $1/2$. Objects
$t_0,t_H,t_L,g_H,g_L,\Delta_T$ are as in eq. (4) of the paper.

**Realized terminal payoff.** Let $\tilde V_T$ denote the realized
payment to one target share at the sale. Without entry,
$\tilde V_T=p\mathbf 1\{R\ge p\}$. With entry and value $\theta$,
$\tilde V_T=\max\{p,\min(R,\theta)\}$ if the challenger wins or loses
to the incumbent, with the usual second-price reading. Then
$t_0=\mathbb E[\tilde V_T\mid\text{no entry}]$ and
$t_\theta=\mathbb E[\tilde V_T\mid\text{entry},\theta]$. The paper
writes $V_T$ for this payoff. The price is
$P(X)=\mathbb E[\tilde V_T\mid X]$.

**Population.** Normalize shares outstanding to one unit. Seven
groups exhaust the model.

| Group | Initial holding | Action | Financial payoff |
|---|---|---|---|
| Long-term holders | $1-\omega_Z$ | none | $(1-\omega_Z)\tilde V_T$ |
| Liquidity traders | $\omega_Z$ | net demand $Z$ at $P$ | $(\omega_Z+Z)\tilde V_T-ZP$ |
| Informed investor | $0$ | order $q$ at $P$ | $q(\tilde V_T-P)-k\lvert q\rvert$ |
| Market makers | $0$ | absorb $-X$ | $-X(\tilde V_T-P)$ |
| Incumbent | — | bids $R$ | $(R-\text{payment})\mathbf 1\{\text{wins}\}$ |
| Challenger | — | pays $C$, bids $\theta$ | entry $\times[(\theta-\text{payment})\mathbf 1\{\text{wins}\}-C]$ |
| Seller (board) | — | sets $p$, runs sale | receipt $\tilde V_T$ per share, paid to holders at sale |

Three remarks fix the accounting.

1. The seller is not a separate recipient. The board acts for the
holders. The winning bidder pays $\tilde V_T$ per share to whoever
holds shares at the sale. Seller revenue
$\mathcal R_T=\mathbb E[\tilde V_T]$ must not be added to holder
payoffs. That sum would double count one receipt.
2. Liquidity traders trade for reasons outside the model. Write
$B(Z)$ for that unmodelled benefit. This memo reports financial
payoffs only. It excludes $B(Z)$ from every total. The demand $Z$ is
exogenous and independent of $(\theta,R,C)$, as in the paper.
3. Two ledgers must stay separate. The *auction ledger* divides
ownership value among target holders and bidders, net of preparation
costs. The *trading ledger* divides $\tilde V_T-P$ among the investor,
liquidity traders, and market makers. The trading ledger is zero-sum
before the cost $k\lvert q\rvert$. Only feedback from price to entry
links the two ledgers.

**Trade scale.** The paper bounds orders by $\lvert q\rvert\le 1$ and
calls this a normalized small unit, not ownership of the target. The
paper does not state float size in the same units. Write $\lambda>0$
for trade units per unit of float. The benchmark normalization of
this memo sets $\lambda=1$ and float $=1$. Every trading-ledger
expectation below scales by $\lambda$. Auction-ledger objects do not.
Section 6 states the risk in this normalization.

**Regimes.** Fix $r$. Compare four economies.

- (a) *No informed investor:* $q\equiv0$ imposed. Entry is $\rho$.
- (b) *Informed investor, price access:* the paper equilibrium.
- (c) *Informed investor, no price access:* Section 6.1 of the paper.
  Entry is $\rho$. At $r_1$ orders stay full (Prop. A.9).
- At $r_0$ the equilibrium has no trade in both access regimes
  (Prop. 2(i) and Table 2). Regimes (a), (b), and (c) then coincide.

## 3. Results

### Claim W1 (auction ledger; analytical)

Let $e_\theta$ denote the entry probability in state $\theta$. Then

$$\mathcal R_T \;=\; t_0+\tfrac12\big[e_H(t_H-t_0)+e_L(t_L-t_0)\big]
\;=\; t_0+\mathbb E\big[e\,(t_\theta-t_0)\big].$$

Expected bidder payoffs use three incumbent objects. Without entry
the incumbent earns $I_0=(r-p)^2/(2r)$. With entry by a low challenger
it earns $I_L=(r-\ell)^2/(2r)=\Delta_T$. With entry by a high
challenger it earns $I_H=0$, since $h>r$. Hence

$$\Pi_{\text{inc}}=\tfrac12\big[(1-e_H)I_0+e_H I_H+(1-e_L)I_0+e_L I_L\big],
\qquad
\Pi_{\text{chal}}^{\text{gross}}=\tfrac12\big[e_H g_H+e_L g_L\big].$$

*Derivation.* Integrate the payment rule over $R\sim U[0,r]$. Without
entry the incumbent wins if $R\ge p$ and pays $p$. Its expected profit
is $\int_p^r(R-p)\,dR/r=(r-p)^2/(2r)$. With a low challenger the
incumbent wins if $R>\ell$ and pays $\ell$. Its expected profit is
$\int_\ell^r(R-\ell)\,dR/r=(r-\ell)^2/(2r)$. Eq. (4) gives the same
expression for $\Delta_T$. A high challenger always wins, so the
incumbent earns zero. The proceeds formula averages $t_0$ and
$t_\theta$ over entry and state. Both increments satisfy
$t_H>t_0$ and $t_L>t_0$ on the benchmark support, so entry raises
proceeds in either state. $\square$

The identity $I_L=\Delta_T$ is an accounting fact, not a mechanism.
The incumbent rent that a low challenger leaves on the table equals
the sensitivity of target proceeds to challenger quality. Part of any
entry gain to target holders is a transfer from the incumbent. The
rest is new ownership value.

### Claim W2 (acquisition surplus split; analytical)

Let $\mathcal W$ denote ownership value net of preparation costs paid,
as in Table 2, Panel C, of the paper. Then

$$\mathcal W \;=\; \mathcal R_T+\Pi_{\text{inc}}+\Pi_{\text{chal}}^{\text{net}},
\qquad
\Pi_{\text{chal}}^{\text{net}}=\Pi_{\text{chal}}^{\text{gross}}-\mathbb E[\text{prep costs paid}].$$

*Derivation.* In each state of the world the winner's value equals the
payment to target shares plus the winner's profit. A loser earns zero.
Sum over states and take expectations. Subtract preparation costs
once. Without entry the check is
$t_0+I_0=(r^2-p^2)/(2r)=\mathbb E[R\mathbf 1\{R\ge p\}]$. With a high
challenger the check is $t_H+g_H=h$. With a low challenger the check
is $t_L+g_L+I_L=\ell+(r-\ell)^2/(2r)=\mathbb E[\max(R,\ell)]$.
$\square$

Under condition (A1) the challenger split by cost is explicit. The
low-cost challenger always enters. The high-cost challenger enters
only after a favorable price. With $\bar g=(g_H+g_L)/2$ and crossing
probabilities $\alpha_H,\alpha_L$ from eq. (12),

$$\Pi_{\text{chal}}^{\text{net}}
=\rho(\bar g-c_L)+(1-\rho)\,\tfrac12\big[\alpha_H(g_H-c_H)+\alpha_L(g_L-c_H)\big].$$

The term $g_L-c_H$ is negative. A high-cost challenger who prepares
after a favorable price and then learns $\theta=\ell$ loses money ex
post. The decision is sound only in conditional expectation at the
price. This is the same qualification as in eq. (A.40) of the paper.

### Claim W3 (trading ledger; analytical)

In every realization, gross trading payoffs sum to zero:

$$q(\tilde V_T-P)+Z(\tilde V_T-P)-X(\tilde V_T-P)=0,
\qquad X=q+Z.$$

Market makers break even in expectation. The informed investor's
expected gross profit equals the liquidity traders' expected financial
loss:

$$\mathbb E\big[-X(\tilde V_T-P(X))\big]=0,
\qquad
\underbrace{\mathbb E[q(\tilde V_T-P)]}_{\displaystyle \Pi}
\;=\;-\,\mathbb E[Z(\tilde V_T-P)]\;\ge\;0
\ \text{in any trading equilibrium}.$$

Also $\mathbb E[P]=\mathbb E[\tilde V_T]=\mathcal R_T$.

*Derivation.* The first line holds by $X=q+Z$, state by state. For the
second line, $X$ is measurable with respect to $X$, and
$P(X)=\mathbb E[\tilde V_T\mid X]$. Iterated expectations give
$\mathbb E[X(\tilde V_T-P(X))]=\mathbb E[X\,\mathbb E[\tilde V_T-P(X)\mid X]]=0$.
Take expectations in the first line to get $\Pi=-\mathbb E[Z(\tilde
V_T-P)]$. Non-negativity follows because $q=0$ is feasible, so an
optimal order earns weakly positive gross profit; the net profit is
$\Pi-k\mathbb E\lvert q\rvert$. The last line is iterated expectations
applied to $P$. $\square$

Three consequences answer the supervisor's question in part.

1. *A holder who does not trade gets $\tilde V_T$, not $P$.* An interim
price rise is a mark-to-market gain only. It pays cash only to a
holder who sells. The buyer then holds the claim to $\tilde V_T$.
2. *Initial shareholders cannot in total sell to themselves at a high
price.* Their counterparties are market makers, who break even, and
the informed investor, who gains $\Pi$. The expected cash that initial
shareholders extract at the trading stage is $-\lambda\Pi\le0$.
3. *The price level is not the gain.* The dividend diagnostic in
Section 6.1 of the paper makes the same point. A constant added to the
traded claim raises $P$ and $\tilde V_T$ together. It leaves
$\tilde V_T-P$, entry, and seller revenue unchanged. Only the
information in the price, through entry, changes real payoffs.

### Claim W4 (size of the trading transfer under full orders; analytical)

Fix full orders $(q_H,q_L)=(1,-1)$. Write $a_H(x)=f(x-1)$ and
$a_L(x)=f(x+1)$ for the flow densities, and
$\varphi(x)=a_H(x)a_L(x)/(a_H(x)+a_L(x))$. Then the two legs of the
investor's profit are equal, and

$$\Pi \;=\; \Delta_T\int e_r(\mu_X(x))\,\varphi(x)\,dx,
\qquad
\mathbb E[A_H(X)\mid H]=\mathbb E[A_L(X)\mid L]=\Pi,$$

with residual advantages $A_H,A_L$ as in eq. (11) of the paper. In the
price-hidden economy $e_r\equiv\rho$, so $\Pi^{\text{hid}}=\rho\Delta_T
J$ with the closed form

$$J \;=\; m+\tfrac12 e^{-1/b}\,\mathrm{gd}(1/b),
\qquad m=\frac{1}{1+e^{2/b}},\quad
\mathrm{gd}(y)=2\arctan(e^{y})-\tfrac{\pi}{2}.$$

With price access, entry jumps at the threshold flow $x^*$ of eq. (12),
so $\Pi^{\text{acc}}=\Delta_T\big[\rho J+(1-\rho)J_{\text{tail}}\big]$ with

$$J_{\text{tail}}=\int_{x^*}^{\infty}\varphi(x)\,dx
=\frac{m}{2}+\tfrac14 e^{-1/b}\big[\mathrm{gd}(1/b)-\mathrm{gd}(x^*/b)\big],
\qquad 0<x^*<1.$$

In particular $\Pi^{\text{acc}}>\Pi^{\text{hid}}$ and
$\Pi\le\Delta_T/2$ in either economy (trade scale $\lambda=1$).

*Derivation.* In state $H$ the investor buys one unit. Its expected
gross profit is $\int a_H(x)\,e_r(\mu_X)\Delta_T(1-\mu_X(x))\,dx$ by
eq. (11). Since $1-\mu_X=a_L/(a_H+a_L)$, the integrand is
$\Delta_T e_r(\mu_X)\varphi(x)$. In state $L$ the same steps give
$\int a_L(x)\,e_r(\mu_X)\Delta_T\mu_X(x)\,dx$, and
$\mu_X=a_H/(a_H+a_L)$ gives the identical integrand. The two legs are
therefore equal for every entry schedule $e_r(\cdot)$. The average of
the legs is $\Pi$.

For the closed forms, split the integral at $x=\pm1$. For $x\ge1$ the
posterior sits at its bound $M$, so $\varphi(x)=m\,a_H(x)$ and
$\int_1^\infty a_H=1/2$. The left tail is symmetric. The two tails
contribute $m$ in total. For $\lvert x\rvert\le1$,
$\varphi(x)=\frac{1}{4b}e^{-1/b}\operatorname{sech}(x/b)$. The integral
of $\operatorname{sech}$ is the gudermannian $\mathrm{gd}$. This gives
$J$. With access, $e_r$ equals $1$ instead of $\rho$ on
$x\ge x^*$. The extra term integrates $\varphi$ over that half-line,
which gives $J_{\text{tail}}$. The bound $\Pi\le\Delta_T/2$ uses
$e_r\le1$ and $J\le1/2$, since $\varphi$ integrates to at most the
overlap of two densities. Section 5 checks the closed forms against
direct quadrature. $\square$

The formula separates the transfer from the real effect in one line.
The transfer $\Pi$ is proportional to $\Delta_T$ and to the overlap of
the two flow densities. It needs residual uncertainty. It does not
need an entry response: $\Pi^{\text{hid}}>0$ with entry fixed at
$\rho$. The real effect needs the entry response. It appears in
$\mathcal R_T$, not in $\Pi$, except that access raises $e_r$ at high
posteriors and so raises $\Pi$ as a by-product.

### Claim W5 (ex-ante value of initial shareholders; analytical)

Define the ex-ante financial value of the target's initial shareholders
(long-term holders plus liquidity traders, before $B(Z)$) by

$$\mathcal S \;=\; \mathcal R_T-\lambda\Pi.$$

The split $\omega_Z$ cancels from $\mathcal S$. At fixed $r$:

- (c) versus (a): $\mathcal S^{\text{hid}}-\mathcal S^{\text{no inv}}
  =-\lambda\Pi^{\text{hid}}\le0$. Informed trading without price
  access is a pure loss to initial shareholders. Proceeds do not move.
- (b) versus (a): $\mathcal S^{\text{acc}}-\mathcal S^{\text{no inv}}
  =\Delta\mathcal R_T-\lambda\Pi^{\text{acc}}$, where

$$\Delta\mathcal R_T
=\frac{1-\rho}{2}\big[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\big]>0$$

  under the conditions of Prop. 2 at $r_1$ (eq. (A.41) of the paper).
  Initial shareholders gain from the presence of informed trading if
  and only if

$$\lambda \;<\; \lambda^*
\;:=\;\frac{\Delta\mathcal R_T}{\Pi^{\text{acc}}}
\;=\;\frac{(1-\rho)\big[\alpha_H(t_H-t_0)+\alpha_L(t_L-t_0)\big]}
{2\Delta_T\big[\rho J+(1-\rho)J_{\text{tail}}\big]}.$$

- (b) versus (c): $\mathcal S^{\text{acc}}-\mathcal S^{\text{hid}}
  =\Delta\mathcal R_T-\lambda(\Pi^{\text{acc}}-\Pi^{\text{hid}})$.
  Price access alone, given that informed trading exists, helps
  initial shareholders under the weaker condition
  $\lambda<\Delta\mathcal R_T/(\Pi^{\text{acc}}-\Pi^{\text{hid}})$.

*Derivation.* Sum the holder rows of the population table:
$(1-\omega_Z)\tilde V_T+(\omega_Z+Z)\tilde V_T-ZP
=\tilde V_T+Z(\tilde V_T-P)$. Take expectations. Claim W3 replaces the
second term by $-\lambda\Pi$ at trade scale $\lambda$. In regime (a)
entry is $\rho$ and $\Pi=0$. In regime (c) entry is still $\rho$, so
$\mathcal R_T$ matches regime (a), but $\Pi^{\text{hid}}>0$ at $r_1$.
In regime (b) entry is state-contingent with probabilities $\alpha_H,
\alpha_L$. Claim W1 then gives $\Delta\mathcal R_T$. The three
differences follow. $\square$

**The gain region is nonempty.** Take any economy that meets the
conditions of Prop. 2 at $r_1$. Then $\Delta\mathcal R_T>0$ and
$\Pi^{\text{acc}}$ is finite. For all small $\lambda$ the entry gain
exceeds the trading loss. Section 5 shows that the benchmark gain is
positive even at $\lambda=1$. That scale lets the investor trade the
whole float. The answer to the supervisor is therefore *yes, in a
stated region*: target shareholders as a group can gain from informed
trading. The gain comes from entry. It never comes from the price
change as such.

Two boundary cases fix the intuition. At $r_0$ there is no trade, so
$\Pi=0$ and $\mathcal S=\mathcal R_T$. At a very strong incumbent $r_2$
(Prop. 2(iii)), orders stay full but entry returns to $\rho$. Then
$\Delta\mathcal R_T=0$ while $\Pi>0$. Informed trading is again a pure
loss to initial shareholders, as in regime (c). The shareholder gain
from informed trading is thus tied to the same intermediate region as
the entry gain. It is not monotone in incumbent strength. (The $r_2$
statement restates Prop. 2(iii) in $\mathcal S$ units: analytical.)

### Claim W6 (split within the shareholder class; analytical)

Long-term holders gain from price-induced entry and bear no trading
loss. Liquidity traders bear the whole trading loss. Relative to no
informed investor at $r_1$:

$$\Delta_{\text{LT}}=(1-\omega_Z)\Delta\mathcal R_T\ge0,
\qquad
\Delta_{\text{liq}}=\omega_Z\Delta\mathcal R_T-\lambda\Pi^{\text{acc}}.$$

Liquidity traders gain if and only if
$\omega_Z/\lambda>\Pi^{\text{acc}}/\Delta\mathcal R_T=1/\lambda^*$.
Relative to the price-hidden economy, they gain from access alone if
and only if
$\omega_Z/\lambda>(\Pi^{\text{acc}}-\Pi^{\text{hid}})/\Delta\mathcal R_T$.

*Derivation.* Read the two holder rows of the population table. Take
expectations in each regime and subtract. The entry gain
$\Delta\mathcal R_T$ accrues per share held. The trading loss
$\lambda\Pi$ accrues per unit traded, and only liquidity traders
trade. $\square$

So "the investors" are two different economic groups in this story.
The informed investor is an outsider with no initial stake. The noise
demand $Z$ is the net demand of target shareholders who must trade for
outside reasons. Holders who sit through the sale gain from the
mechanism. Holders who must trade during the decision interval pay
for it, in expectation. A single representative shareholder hides this
conflict. Section 5 puts numbers on it.

### Claim W7 (board incentives; conjecture)

This claim is short by design. Each item is a **conjecture**. None is
proved here.

1. *Subsidy to informed trading.* A board that acts for all initial
shareholders values $\mathcal S$, not $\mathcal R_T$. A small subsidy
that moves the economy from no trade to the Prop. 2 trading regime
raises $\mathcal S$ if $\Delta\mathcal R_T>\lambda\Pi^{\text{acc}}$
plus the subsidy cost. A board that acts for holders at the sale (the
$\mathcal R_T$ objective of Appendix A.7) would subsidize more often,
since it ignores $\lambda\Pi$.
2. *Disclosure.* Public disclosure of the fact that the investor knows
would induce entry without a trading loss. It would dominate the
trading channel for initial shareholders. But the board in the model
does not know $\theta$. The challenger value is a fact about the
buyer's match, not a fact in the target's files. Disclosure policy
cannot release what the board does not hold. Target-side disclosure
that lowers the investor's cost $k$ acts like the subsidy in item 1.
3. *Reserve.* The seller problem in eq. (A.44) maximizes
$\mathcal R_T(p)$. The initial-shareholder objective subtracts
$\lambda\Pi(p)$. A higher reserve can widen $\Delta_T$ (Section 6.3 of
the paper). By Claim W4 it then also raises $\Pi$ per unit traded. The
two objectives can rank reserves in opposite orders. The seller
problem is open in the paper. The $\mathcal S$ version is open here.

## 4. What changes relative to the current paper

No proposition in the paper changes. This memo adds a population and
two accounting objects, $\Pi$ and $\mathcal S$. The equilibrium
objects $P$, $e_r$, $\mathcal R_T$, and $\mathcal W$ stay as they are.

- **Sections 2.2–2.3 (population gap).** The paper states that neither
  bidder trades and that the investor has no initial position. It does
  not state who holds shares, who supplies $Z$, or who receives
  $V_T$. Section 2 of this memo closes that gap. The closure is free:
  $Z$ stays exogenous, all agents stay risk neutral, and no first-order
  condition changes. The proof steps in Sections 3–4 do not use holder
  identity.
- **Eq. (11) and $t_0$.** The brief notes that $t_0$ cancels from the
  residual advantage. Claim W4 shows the same fact in levels: $\Pi$
  depends on $\Delta_T$ and $e_r$, not on $t_0$ or $t_L-t_0$. But $t_0$
  does enter holder welfare. It is the floor of $\mathcal R_T$ and so
  of $\mathcal S$. The $t_0$ question is a welfare question, not a
  trading question. That is why it needs the population.
- **Section 6.1 and Prop. A.9 (survive, with a new reading).** Price
  access raises $\mathcal R_T$ and $\mathcal W$. Claim W5 adds that
  access also raises $\Pi$. The net effect on initial shareholders is
  $\Delta\mathcal R_T-\lambda(\Pi^{\text{acc}}-\Pi^{\text{hid}})$. Prop.
  A.9 holds trading costs fixed across the two economies, so its
  $\mathcal W$ comparison is untouched. The $\mathcal S$ comparison is
  a different object: it counts a transfer that $\mathcal W$ excludes
  by design. Both statements can hold at once, and at the benchmark
  both are positive (Section 5).
- **Table 2, Panel C.** The panel reports $\mathcal R_T$ and
  $\mathcal W$. It does not report $\Pi$ or $\mathcal S$. A reader can
  take the panel to say that shareholders gain 0.257809 from access.
  That reading is wrong for initial shareholders who trade. The panel
  needs one more row, or a note that names the excluded transfer.
- **Appendix A.7 (seller objective).** Eq. (A.44) maximizes seller
  revenue. Claim W7, item 3, states the initial-shareholder variant.
  The paper should say which objective the board holds, and why.

## 5. Numerical example

Benchmark vector: $(h,\ell,p,\rho,c_L,c_H,b,k)=(10,1,0.5,0.25,1,6,2,0.02)$,
$(r_0,r_1)=(1.2,3)$. Trade scale $\lambda=1$. The holder split uses the
illustrative value $\omega_Z=0.5$. Totals do not depend on $\omega_Z$.
Status: **numerical diagnostic**. The script is print-only:
`audit/alex_meeting_2026_10_21/scripts/Q3_welfare/welfare_table.py`
(run with `.venv/bin/python`). It computes $\Pi$ by quadrature and by
the closed form of Claim W4. The two routes agree to 12 digits. It
also prints identity residuals for Claim W2. All residuals are below
$10^{-30}$. The script reproduces Table 2 of the paper exactly:
$\mathcal R_T=0.392708$ at $r_0$; $0.872392$ with access and $0.614583$
hidden at $r_1$; $\mathcal W=2.382301$ and $2.302083$; entry $0.522757$.

At $r_1$: $\tau=0.705$, $x^*=0.8712$, $\alpha_H=0.5312$,
$\alpha_L=0.1962$, $J=0.41462$, $J_{\text{tail}}=0.14325$.

| Expected payoff | $r_0$, access | $r_0$, hidden | $r_1$, access (b) | $r_1$, hidden (c) | $r_1$, no investor (a) |
|---|---:|---:|---:|---:|---:|
| Orders $(q_H,q_L)$ | $(0,0)$ | $(0,0)$ | $(1,-1)$ | $(1,-1)$ | imposed $0$ |
| Entry $\mathsf E$ | 0.2500 | 0.2500 | 0.5228 | 0.2500 | 0.2500 |
| Seller proceeds $\mathcal R_T=\mathbb E[\tilde V_T]$ | 0.3927 | 0.3927 | 0.8724 | 0.6146 | 0.6146 |
| Long-term holders $(1-\omega_Z)\mathcal R_T$ | 0.1964 | 0.1964 | 0.4362 | 0.3073 | 0.3073 |
| Liquidity traders $\omega_Z\mathcal R_T-\Pi$ | 0.1964 | 0.1964 | 0.2955 | 0.2382 | 0.3073 |
| **Initial shareholders $\mathcal S=\mathcal R_T-\Pi$** | **0.3927** | **0.3927** | **0.7317** | **0.5455** | **0.6146** |
| Informed investor, gross $\Pi$ | 0 | 0 | 0.1407 | 0.0691 | 0 |
| Informed investor, net $\Pi-k$ | 0 | 0 | 0.1207 | 0.0491 | 0 |
| Market makers | 0 | 0 | 0 | 0 | 0 |
| Incumbent | 0.1552 | 0.1552 | 0.6295 | 0.8646 | 0.8646 |
| Challenger, gross | 1.2010 | 1.2010 | 2.7669 | 1.0729 | 1.0729 |
| Challenger, net of prep costs | 0.9510 | 0.9510 | 0.8804 | 0.8229 | 0.8229 |
| Prep costs paid (expected) | 0.2500 | 0.2500 | 1.8865 | 0.2500 | 0.2500 |
| Acquisition surplus $\mathcal W$ | 1.4990 | 1.4990 | 2.3823 | 2.3021 | 2.3021 |

The seller row is a receipt, not a seventh payoff. Do not add it to
the holder rows. Do not add the holder rows to $\mathcal W$: hold
$\mathcal W=\mathcal R_T+\Pi_{\text{inc}}+\Pi_{\text{chal}}^{\text{net}}$
as the check. The trading-ledger rows ($\Pi$ and its mirror loss in
the liquidity row) sit outside $\mathcal W$ by construction.

**Key differences at $r_1$.**

- Entry gain in proceeds: $\Delta\mathcal R_T=0.2578$.
- Trading transfer: $\Pi^{\text{acc}}=0.1407$ with access;
  $\Pi^{\text{hid}}=0.0691$ hidden. Access roughly doubles the
  transfer. The entry jump at $x^*$ raises the residual advantage at
  high posteriors.
- Net gain to initial shareholders, (b) less (a):
  $0.2578-0.1407=+0.1171>0$. Break-even scale $\lambda^*=1.832$.
  Shareholders in total gain even if the investor trades 1.83 times
  the float at the model scale.
- Net gain from access alone, (b) less (c):
  $0.2578-(0.1407-0.0691)=+0.1862>0$. Break-even scale $3.599$.
- Loss from trading without access, (c) less (a): $-0.0691$.
  Proceeds are equal in the two columns. The whole difference is the
  transfer.
- Split of the (b) less (a) gain at $\omega_Z=0.5$: long-term holders
  gain $+0.1289$. Liquidity traders *lose* $-0.0118$. Their break-even
  holding share is $\omega_Z^*=0.546$ at $\lambda=1$. The group total
  hides a loss for the subgroup that trades.
- Liquidity traders do gain from access alone at $\omega_Z=0.5$:
  $+0.0573$, since $\omega_Z>0.278$ (the access-alone break-even).
  Given that informed trading exists, even trading shareholders want
  the challenger to see the price. They would still prefer no informed
  investor at all.
- Cross-$r$ check, $r_0$ to $r_1$ with access:
  $\mathcal S$ rises by $0.3390$. The parts are a direct auction effect
  of $+0.2219$ (hidden proceeds at $r_1$ less proceeds at $r_0$), plus
  the feedback entry gain $+0.2578$, less the trading loss $0.1407$.
  The $r$ comparison mixes a stronger incumbent with the information
  channel. Only the fixed-$r_1$ comparisons isolate the channel.
- Incumbent rent falls with access at $r_1$ ($0.8646\to0.6295$). Part
  of the holder gain is a transfer from the incumbent, as Claim W1
  states. Challenger net profit rises only slightly
  ($0.8229\to0.8804$) because expected prep costs rise from $0.25$ to
  $1.8865$. Most of the gross entry gain is spent on $c_H$ payments.

## 6. Open issues and risks

1. **Trade scale is not in the paper (main risk).** The order bound
$\lvert q\rvert\le1$ is a normalized unit. Float size in the same units
is free. All shareholder-gain statements run through $\lambda$. The
benchmark survives $\lambda=1$ with room ($\lambda^*=1.832$). That
fact is numerical, not structural. A draft that reports $\mathcal S$
must state the float normalization in the model section. Without it,
$\mathcal S$ is not defined.
2. **Holdings versus unbounded noise.** The Laplace demand $Z$ takes
any real value. A liquidity trader with holding $\omega_Z$ ends with
$\omega_Z+Z$, which is negative with positive probability. The ledger
treats all positions as cash-settled claims on $\tilde V_T$. Short
positions and market-maker inventory carry no constraint. This matches
the trading stage of the paper. It does not match a literal share
register. A bounded-float version would need a different noise law or
a holdings constraint. Either change touches the posterior bounds.
3. **The liquidity benefit $B(Z)$ is absent.** Noise traders in this
class of model trade for an outside gain. The memo counts their
financial loss $\Pi$ and excludes $B(Z)$. A full welfare statement
about noise traders needs $B$. The statements about $\mathcal S$ are
statements about financial value to initial holders. The paper's
$\mathcal W$ has the same scope limit.
4. **The trading cost $k\lvert q\rvert$.** The memo treats it as a deadweight
cost outside all ledgers. If it is a fee to a broker, it is a transfer
to an eighth group. Either way it does not enter $\mathcal S$,
$\mathcal R_T$, or $\mathcal W$. It does enter total surplus if a
reader builds one. At $r_1$ the cost is $k=0.02$ per unit traded.
5. **Who holds at the sale.** Trades move shares from initial holders
to the investor and market makers before the sale. Holders at the sale
then include outsiders. This memo values *initial* shareholders ex
ante, before trade. That is the right object for the supervisor's
question. It is not the payoff of the register on the sale date. A
draft should name the date at which "target shareholders" are measured.
6. **Intermediate equilibria.** Claim W4 gives $\Pi$ in closed form
only under full orders. The identity
$\Pi=-\mathbb E[Z(\tilde V_T-P)]$ holds in every equilibrium,
including the partial-sale and mixed equilibria of Prop. 3. Closed
forms for $\Pi$ and $\lambda^*$ on those branches are **open**. The
sign of $\mathcal S^{\text{acc}}-\mathcal S^{\text{no inv}}$ there is
also open.
7. **Interaction with the stake extension.** If the informed investor
holds an initial stake, it shares in $\Delta\mathcal R_T$ and its
orders change. The ledgers then mix. Claims W3–W6 use a zero stake.
The sibling memo on the stake extension owns that case. Do not merge
the two sets of formulas without redoing the order choice.

## 7. Recommendation

In priority order:

1. **Add the population to Sections 2.2–2.3.** One short paragraph
suffices: who holds shares, that $Z$ is net demand from shareholders
who trade for outside reasons, that market makers absorb flow, and
that the winner pays holders at the sale. State the float
normalization that fixes $\lambda$. This costs no proof steps.
2. **Add $\Pi$ and $\mathcal S$ to Section 6.1.** Report the transfer
next to the proceeds gain. State the condition
$\lambda<\lambda^*$ for a net gain to initial shareholders, and the
benchmark values $\Pi^{\text{acc}}=0.1407$, $\lambda^*=1.832$. Add one
row to Table 2, Panel C, or a note with the same content. Do not let
the panel read as a pure shareholder gain of 0.257809.
3. **State the within-class split in one sentence.** Holders who do not
trade gain. Holders who must trade can lose, even when the class gains
in total ($\omega_Z^*=0.546$ at the benchmark). This sentence is the
direct answer to Point 3. It also pre-empts the representative-holder
reading.
4. **Name the board objective before Appendix A.7.** Say whether the
seller maximizes $\mathcal R_T$ (holders at the sale) or $\mathcal S$
(initial holders). Flag the $\mathcal S$ reserve problem as open.
Keep Claim W7 out of the results. At most, state items 1–3 as remarks.
5. **Do not claim a general shareholder gain.** The gain needs the
Prop. 2 region, price access, and $\lambda<\lambda^*$. At $r_2$ and in
the price-hidden economy the same trading is a pure loss to initial
holders. State both signs.

## 8. Plain summary

Shareholders do not gain merely because the stock price moves. A
shareholder who keeps the shares receives the sale proceeds, not the
interim price. A shareholder who sells at the interim price gives the
sale proceeds to the buyer. In total, the original shareholders pay
the informed trader's profit. Market makers in the middle break even.

The real gain is different. An informative price can bring an extra
bidder into the sale. Extra bidding raises the sale proceeds for every
share. At the paper's main numbers, the extra proceeds are 0.258 per
share. The informed trader's profit is 0.141 per share of float. The
original shareholders come out ahead by 0.117 in total.

The total hides a split. Shareholders who hold to the end gain the
full proceeds rise and pay nothing. Shareholders who must trade during
the sale process pay the informed trader's profit. At an even split of
the float, the trading group loses a little even though shareholders
in total gain. If the extra bidder never comes in, as with a very
strong first bidder or a hidden price, informed trading only takes
money from trading shareholders. It gives nothing back.




