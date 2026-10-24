# N2: Dynamics and arrivals in the order slot

Workstream N2 of `NEW_EXTENSIONS_BRIEF.md`. Scripts: `scripts/N2_dynamics/`. Status: complete, 23 October 2026.

## 1. Question

The one-slot model (T2, variant V3) has one public order before the challenger decides.
This memo asks what changes when the decision follows a path of orders:

- several order slots before the decision, with fresh informed arrivals (sequential Glosten–Milgrom trade);
- a random number of arrivals (Poisson);
- one informed investor with one unit of capacity and a free choice of trade date;
- the timing of preparation, and whether a richer price path restores rising entry at 1.55, 1.60, 1.65.

The constraint from T6: entry returns to the floor at $r_2=3.6$ only if every reachable decision posterior
stays below $\tau(18/5)=4245/5804\approx0.7314$.

**Answer in brief.**

1. The cap is on informed volume before the decision, not on the number of trade rounds.
   With one informed unit, every likelihood ratio stays in $[1/(1+u),1+u]$ for every number of slots
   and every timing strategy. So Prop. 2(iii) holds for all $n$ on T2's strip (analytical).
2. With fresh informed arrivals in each slot, the knob must scale: $L_1\le n\ln(1+u)<L_2$,
   with $L_1=\ln(141/59)=0.8712$ and $L_2=\ln(4245/1559)=1.0017$, so $u_n\approx0.93/n$.
   On that strip extra entry at $r_1=3$ falls to zero like $e^{-0.306n}$ (analytical).
   At a fixed knob the ceiling rises from $3.458$ ($n=1$) to $6.251$ ($n=2$) and tends to $7.969$.
3. With entry feedback, the informed buyer wants its trade to be seen; without feedback it hides.
   With a two-sided menu the bad-news investor delays its sale. At the first date the orders are
   $(1,-v)$ with $v\approx0.167$: the paper's full purchase and partial sale, as a timing pattern
   (computer-assisted, $n=2$).
4. A richer price path does not restore rising entry at 1.55–1.65 at the benchmark $k$.
   The obstacle: a last buyer at a history that recruits is indifferent only at the posterior $1-k/\Delta_T(r)$,
   and this is above $\tau(3.6)$ for every $r>1.4675$ (analytical; full list of equilibria for $n=2$, computer-assisted).
5. An unbounded random number of arrivals (Poisson) breaks Prop. 2(iii) for every arrival rate (analytical).

## 2. Extensions developed

### 2.0 Common setup

**Auction and costs.** Reading N with point masses $h=10$, $\ell=1$, prior $\pi=1/2$; $c_L=0$; $c_H=6$ with
probability $1-\rho=3/4$; reserve $p=1/2$; $R\sim U[0,r]$; trade cost $k=1/50$. The objects of TEAM_RULES §3 agree
with direct integration at all six strengths (`n_slots_ladder.out.txt`, Section A, difference exactly zero).
Write $\Delta=\Delta_T$, $w_j=t_j-t_0$, $\tau(r)=(c_H-g_L)/(g_H-g_L)$ and the odds thresholds

$$
T_1=\frac{\tau(3)}{1-\tau(3)}=\frac{141}{59},\qquad T_2=\frac{\tau(18/5)}{1-\tau(18/5)}=\frac{4245}{1559},\qquad
L_i=\ln T_i .
$$

Here $L_1=0.871222$, $L_2=1.001697$ and $\theta:=L_1/L_2=0.869746$.
The revelation ceiling, where $g_H(r)=c_H$, is $\bar r=(32+\sqrt{1008})/8=7.968627$.

**Slot.** Unit orders. The informed menu is two-sided $\{-1,0,1\}$ unless a result says buy-only $\{0,1\}$.
A liquidity order sells, waits, buys with probabilities $(\beta,1-2\beta,\beta)$, $0<\beta<1/2$.
As in T2, $b=(1-\lambda)\beta$, $u=\lambda/b$, and $M=(1+u)/(2+u)$ is the one-slot top posterior.
No separate noise. This is T2's V3 and Dow–Gorton's alternative-arrival device (`L1_survey.md` C09, verified).

**Equilibrium.** Perfect Bayesian equilibrium of the finite order game. Market makers set
$P_t=\mathbb E[V_T\mid h_t]$ from the public order history $h_t$. The challenger sees the prices and its cost, and
decides after the last slot (§2.5 treats an earlier option). Prepared bidders bid their values.

**Beliefs.** Every slot has liquidity mass on each order of the menu. So every order history has positive
probability under every strategy. No result uses an off-path belief.

**Tie rules.** Investor: IM (any mixture at indifference) or I0 (no trade at indifference).
Challenger: C1 (prepare at indifference, the paper's rule) or CM (any mixture). Defaults are IM and C1.

**Lemma 0 (interim prices; from `audit/discrete_exploration_2026_10_21/memos/C2_two_rounds.md`, Lemma C2.0).**
The last price reveals the last posterior $\mu_n$, because $e\ge\rho>0$. An interim price is

$$
P_t=\mathbb E[t_0+e(\mu_n)w_j\mid h_t],
$$

not $P(\mu_t)$. For a short-lived investor at $h_t$, the buy residual is $(1-\mu_t)D(h_t)$ and the sale residual is
$\mu_tD(h_t)$, with

$$
D(h_t)=w_H\,\mathbb E[e\mid H,h_t]-w_L\,\mathbb E[e\mid L,h_t]
=\Delta\,\mathbb E[e\mid H,h_t]+w_L\big(\mathbb E[e\mid H,h_t]-\mathbb E[e\mid L,h_t]\big)\ \ge\ \rho\Delta .
$$

The bracket equals $\operatorname{Cov}(e(\mu_n),\mu_n\mid h_t)/[\mu_t(1-\mu_t)]\ge0$, because $e$ is nondecreasing.
This holds under C1 and under every CM mixture at a cutoff. I call the second term the **early-trader term**.

---

### 2.1 Extension A: $n$ slots with fresh informed arrivals

**Model change.** There are $n$ slots before the decision. At each slot, independently, a fresh informed investor
arrives with probability $\lambda$ and sees the class. Otherwise a liquidity order arrives. Each investor trades once
and holds to the sale. This is sequential Glosten–Milgrom trade with the slot of T2 (`L1_survey.md` M02,
abstract level only; Dow–Gorton C09 has one potential informed trader per period, verified).

**Result A1 (analytical). Per-slot likelihood ratios.** Let $c_0=(1-\lambda)(1-2\beta)$.
Under any strategies, a slot order $q$ has likelihood ratio

$$
\frac{(1-\lambda)\eta(q)+\lambda\sigma_H(q)}{(1-\lambda)\eta(q)+\lambda\sigma_L(q)}\in
\Big[\frac{1}{1+\lambda/((1-\lambda)\eta(q))},\,1+\frac{\lambda}{(1-\lambda)\eta(q)}\Big].
$$

For $q=\pm1$ the bound is $[1/(1+u),1+u]$. For $q=0$ it is $[c_0/(c_0+\lambda),(c_0+\lambda)/c_0]$.
This lies inside $[1/(1+u),1+u]$ exactly when $c_0\ge b$, that is $\beta\le1/3$.
So, for $\beta\le1/3$, every posterior after $n$ slots has odds in $[(1+u)^{-n},(1+u)^n]$.
Let $M_n=(1+u)^n/(1+(1+u)^n)$. Then $1-M_n\le\mu\le M_n$ under every strategy.

Under full informed orders (class H buys, class L sells), the zero order has mass $c_0$ in both classes.
So the posterior odds are exactly $(1+u)^D$, where $D$ is the net order imbalance (buys minus sales).

**Result A2 (analytical). The exact strip.** Let $0<\beta\le1/3$. Prop. 2(i)–(iii) hold, with unique full orders at
$r=3$ and $r=3.6$, if and only if

$$
\boxed{L_1\le n\ln(1+u)<L_2}\quad\Longleftrightarrow\quad (141/59)^{1/n}-1\le u<(4245/1559)^{1/n}-1 .
$$

The upper bound is necessary for every $\beta\in(0,1/2)$.

*Proof.*

1. At $r_0=6/5$, $\Delta-k=-1/300<0$. Every nonzero order loses under every schedule. So no informed trade, and entry is $\rho$.
2. Suppose the strip holds. Then $M_n<\tau(3.6)$. By Lemma 0 and Result A1, a correctly signed order earns at least
   $\rho\Delta(r)(1-M_n)-k>\rho\Delta(r)(1-\tau(3.6))-k$.
   This margin is $21563/870600>0$ at $r=3$ and $899467/20894400>0$ at $r=3.6$.
   A wrong-signed order earns $-(1-\mu)D-k<0$ or $-\mu D-k<0$. So full orders are forced at every node.
3. At $r=3$ the history $D=n$ has posterior $M_n\ge\tau(3)$, so it recruits and entry exceeds $\rho$.
   At $r=3.6$ every posterior is at most $M_n<\tau(3.6)$, so entry is $\rho$ while prices stay informative.
4. If $n\ln(1+u)<L_1$, Result A1 caps every posterior below $\tau(3)$. Entry at $r=3$ is then $\rho$.
5. Necessity of the upper bound, any $\beta$: suppose entry is $\rho$ at every history at $r=3.6$.
   Under C1 every terminal posterior is below $\tau(3.6)$; interim posteriors are averages of terminal ones.
   So step 2's margin forces class H to buy fully at every node, and class L never buys.
   Each buy then has ratio exactly $1+u$. The all-buy history has positive probability and odds $(1+u)^n\ge T_2$.
   It recruits, a contradiction. $\square$

The knobs at $\beta=1/3$ (`n_slots_ladder.out.txt`, Section C):

| $n$ | $u$ range | $\lambda$ range at $\beta=1/3$ |
|---|---|---|
| 1 | $[1.38983,\,1.72290)$ | $[0.31660,\,0.36480)$ |
| 2 | $[0.54591,\,0.65012)$ | $[0.15395,\,0.17811)$ |
| 3 | $[0.33697,\,0.39640)$ | $[0.10098,\,0.11671)$ |
| 4 | $[0.24335,\,0.28457)$ | $[0.07503,\,0.08664)$ |
| 6 | $[0.15628,\,0.18169)$ | $[0.04951,\,0.05711)$ |
| 12 | $[0.07530,\,0.08706)$ | $[0.02449,\,0.02820)$ |

So $n\cdot u_n\to[L_1,L_2)$. The informed share of each slot falls like $1/n$.
The total information before the decision, $n\ln(1+u)$, stays in a fixed band.

**Result A3 (analytical bound; exact points computer-assisted; supremum table numerical diagnostic). Dilution of entry.** On the strip, under full orders,

$$
\mathsf E_n(3)-\rho=(1-\rho)\tfrac12\big[\Pr_H(D\ge D^*)+\Pr_L(D\ge D^*)\big],\qquad D^*=\lceil L_1/\ln(1+u)\rceil>\theta n .
$$

The inequality $D^*>\theta n$ holds because $D^*\ln(1+u)\ge L_1$ and $n\ln(1+u)<L_2$.
$D\ge D^*$ needs at least $\lceil\theta n\rceil$ buys. A buy has probability
$\beta(1+u)/(1+u\beta)\le(1+u)/(2+u)=:p_n$ in class H, and less in class L. Hence

$$
\mathsf E_n(3)-\rho\le(1-\rho)\Pr\big(\mathrm{Bin}(n,p_n)\ge\lceil\theta n\rceil\big)\le(1-\rho)\,e^{-n\,\mathrm{KL}(\theta\Vert p_n)} .
$$

As $n\to\infty$, $p_n\to1/2$ and the exponent tends to $\mathrm{KL}(\theta\Vert1/2)=0.306278$.
The supremum of $\mathsf E_n(3)$ over the strip is a **numerical diagnostic** (`n_slots_ladder.out.txt`, Section D;
400-point sweep in $u$, 40-digit floats):

| $n$ | 1 | 2 | 3 | 4 | 6 | 8 | 12 |
|---|---|---|---|---|---|---|---|
| $\beta=1/3$ | 0.54560 | 0.35478 | 0.28563 | 0.26199 | 0.25135 | 0.25125 | 0.25002 |
| $\beta\to1/2$ | 0.62500 | 0.44878 | 0.35145 | 0.30125 | 0.26295 | 0.25325 | 0.25020 |

Exact rational points (Section E, **computer-assisted**): $n=2$, $u=3/5$, $\lambda=1/6$ gives $\mathsf E_2(3)=305/864=0.353009$;
$n=3$, $u=3/8$, $\lambda=1/9$ gives $0.285113$. For $n\ge8$ the history $D=n-1$ can also recruit near the top of the
strip, which explains the small rise at $n=8$.

**Result A4 (computer-assisted). A fixed knob breaks Prop. 2(iii).** Keep calibration A ($\beta=1/3$,
$\lambda=6/17$, $u=18/11$). The top posterior and the ceiling $r_C(M_n)$ (root of $B_r(M_n)=c_H$, T2 eq. (24)) are:

| $n$ | 1 | 2 | 3 | 4 | 8 | $\infty$ |
|---|---|---|---|---|---|---|
| $M_n$ | $29/40$ | $841/962=0.8742$ | $0.9483$ | $0.9797$ | $0.9996$ | $1$ |
| $r_C(M_n)$ | 3.4582 | 6.2508 | 7.3165 | 7.7212 | 7.9635 | 7.9686 |

At $n=2$ the margins $139/144300$ (at $r=3$) and $2537/266400$ (at $r=3.6$) are positive, so full orders are unique.
Entry is $149/289=0.5156$ at $r=3$ and $337/867=0.3887$ at $r=3.6$. For $n\ge3$ the table entries are full-order
values, not equilibrium claims; Result A2, step 5, still gives entry above $\rho$ at 3.6 in every equilibrium.

**Economic reading.** The return of entry to the floor is a cap on the total information that informed orders
carry before the decision. More informed arrivals must each carry less. Then the decision posterior
concentrates near the prior, at rate $1/\sqrt n$, while its support edge stays capped. So recruitment becomes rare.
The one-slot model is the favourable case: one informed order moves the posterior straight to the edge.

**Predictions.**

- At a fixed information content per trade, a longer pre-decision window (more informed trades) raises the
  entry ceiling: challengers appear against stronger incumbents.
- If the ceiling stays at the benchmark, the entry response to prices weakens with the number of trades.
- The informed share per order that the strip allows, $2M_1-1=u_n/(2+u_n)$, falls like $1/n$.
  This is a PIN-like statistic (T2 eq. (48)); the empirical PIN mapping is unverified (`L1_survey.md` M04, abstract only).

**Scorecard (strip, $\beta\le1/3$).** 1: holds, analytical. 2: holds; entry falls with $n$ (Result A3).
3: holds iff the strip holds, analytical. 4: see Extension B. 5: holds at $n=2$ (Extension B).
6: no off-path belief. 7: strict margins; no tie at $r_0,r_1,r_2$. 8: knob $u_n\approx0.93/n$, as above.
9: Dow–Gorton per-period arrivals (verified); Glosten–Milgrom (abstract only). 10: labels as stated.

---

### 2.2 Extension B: two slots — the price path, the early-trader term, and the middle strengths

**Model change.** Extension A with $n=2$ at the rational point $\beta=1/3$, $\lambda=1/6$, $u=3/5$,
$b=c_0=5/18$, $M_1=8/13$, $M_2=64/89=0.719101$. This point lies on the $n=2$ strip.
Script: `two_slot_fresh.py`, output `two_slot_fresh.out.txt`.

**Result B1 (computer-assisted). The benchmark at $r=3$.** Full orders are unique
(margins $179/6675$ at $r=3$ and $14717/320400$ at $r=3.6$). Only the history $(+,+)$ recruits.

- Entry: $305/864=0.353009$ at $r=3$; $1/4$ at $r=3.6$; ceiling $r_C(64/89)=3.325421$.
- Price access raises proceeds by $2003/20736=0.096595$ and net surplus by $143/6912=0.020689$.
  The derivation is T2 eq. (47): extra preparation happens only at $(+,+)$, where $B(64/89)-6+p^2/r>0$.

The price path (exact; decimals for display):

| history | posterior | price | static $P(\mu)$ |
|---|---|---|---|
| start | $1/2$ | $14747/20736=0.711179$ | $0.614583$ |
| $(+)$ | $8/13$ | $6749/7488=0.901309$ | $0.633814$ |
| $(0)$ | $1/2$ | $59/96=0.614583$ | $0.614583$ |
| $(-)$ | $5/13$ | $743/1248=0.595353$ | $0.595353$ |
| $(+,+)$ | $64/89$ | $2893/2136=1.354401$ | — |
| $(-,-)$ | $25/89$ | $4939/8544=0.578066$ | — |

Price impact of one order:

| node | buy impact | sale impact |
|---|---|---|
| start | 0.190130 | 0.115826 |
| after a buy | 0.453092 | 0.286725 |
| after a wait | 0.019231 | 0.019231 |
| after a sale | 0.019231 | 0.017286 |

**Reading.** The opening price already contains expected entry from later discovery ($0.711$ against $0.615$).
Price impact is state dependent. It peaks at the order that can complete the run-up to the entry threshold.
After bad news it is small, because no continuation can recruit.

**Result B2 (computer-assisted). The early-trader term.** At $r=3$, the slot-1 buy has
$D(+)=\Delta\,\mathbb E[e\mid H,+]+w_L(\mathbb E[e\mid H,+]-\mathbb E[e\mid L,+])=0.388889+0.057292$.
The early-trader term is $12.8\%$ of $D(+)$. It pays the first informed buyer for the entry that the next informed
buyer will trigger. Class H's expected net profit is $0.1516$ at slot 1 and $0.1042$ at slot 2.
So early informed traders earn more per order.

**Result B3 (analytical lemma; computer-assisted signs). Every equilibrium at 1.55, 1.60, 1.65.**
At these strengths, under IM and either challenger rule, the equilibria are exactly:

| $r$ | no trade (NT) | full–full (FF) | threshold branch (TH, needs IM and CM) |
|---|---|---|---|
| $31/20$ | $1/4$ | $305/864=0.353009$ | $0.286077$ |
| $8/5$ | $1/4$ | $305/864$ | $0.278129$ |
| $33/20$ | $1/4$ | $305/864$ | $0.271777$ |

Under C1 or I0 only NT and FF remain. FF: class H buys at slot 1, and buys again only after a buy.
TH: class H mixes at both slots ($a_1/\lambda\approx0.666,0.675,0.702$; $a_2/\lambda\approx0.514,0.525,0.518$),
and the high-cost challenger mixes at $(+,+)$ with probability $0.440,0.341,0.263$.

*Derivation.* All margins below are printed in exact form in Part 2 of the output.

1. *No recruitment after a slot-1 sale.* Its final odds are at most $1\cdot(1+u)=8/5<T(r)$, with $T(r)\ge1.831$.
   So $D(-)=\rho\Delta$, and class L's slot-1 sale earns $\mu_1(-)\rho\Delta\le\rho\Delta/2<k$. Class L does not sell at slot 1.
2. *Class L does not sell at slot 2.* A sale lands at a posterior at most $\mu_1\le M_1=8/13<\tau$.
   It earns at most $\rho\Delta\cdot8/13<k$ for $r<1.65622$ (margin $-0.000303$ at $33/20$).
3. *Only $(+,+)$ can recruit.* Every other final history has odds at most $8/5<T(r)$.
4. *No buy at slot 2 after a sale or a wait.* After a sale, $\mu(-,+)\ge1/2$ and the return is at most $\rho\Delta/2<k$.
   After a wait, $\mu_1(0)\ge5/13$ and the return is at most $\rho\Delta\cdot8/13<k$.
5. *Slot 2 after a buy* (prior $m=\mu_1(+)\in[1/2,8/13]$). An interior rate with $e=1$ needs $1-\mu(+,+)=k/\Delta$,
   so $\mu(+,+)=1-k/\Delta(r)\ge0.795>M_2$: impossible. An interior rate with $e=\rho$ needs $\mu(+,+)<1/2$: impossible.
   What remains: full purchase (if $(1+u)\,m/(1-m)\ge T$), no purchase (always valid), or the threshold rate with
   challenger entry $e^*=k/[\Delta(1-\tau)]$ under CM.
6. *Slot 1.* With the full continuation, the return $(5/13)D(+)$ exceeds $k$ ($0.0421,0.0455,0.0491$), so $a_1=\lambda$.
   With no continuation, the return is below $\rho\Delta/2<k$, so $a_1=0$: this is NT.
   With the threshold continuation, the return falls strictly in $a_1$. Its unique root is bracketed by rational bisection.
7. *TH entry.* At the threshold, $(b+a_1)(b+a_2^*)=b^2T$. So $\Pr(+,+)=b^2(1+T)/2$ does not depend on $a_1$, and
   $\mathsf E_{TH}=\rho+(e^*-\rho)\,b^2/[2(1-\tau)]$. It falls because $\Delta(1-\tau)$ rises in $r$ (X_check §3.5). $\square$

**Result B4 (analytical). The obstacle to rising entry, any $n$.** Let all reachable posteriors be at most
$\tau(3.6)$, and let $r>r_\sharp$, where $\Delta(r_\sharp)(1-\tau(3.6))=k$, so $r_\sharp=1.467472$.
A last-slot buyer whose order reaches a recruiting history with $e=1$ earns
$\Delta(1-\mu)\ge\Delta(r)(1-\tau(3.6))>k$. So it buys fully.

- An interior last-slot rate at such a history needs challenger mixing at $\mu=\tau(r)$.
  There $e^*=k/[\Delta(r)(1-\tau(r))]$ falls in $r$.
- An interior rate at a history that does not recruit does not move entry.
- Early-slot rates carry the early-trader term, which pushes them to full orders at the benchmark (B3, step 6).

So rising entry needs a lower $k$, a higher cap, or a device beyond the order slot.

**Reading and predictions.**

- Informed buying is history dependent at middle strengths: a second informed buy follows only a first buy.
  Signed order flow is then positively autocorrelated before contests with moderately strong incumbents.
- No trade coexists with informative trade on at least $[1.4552,1.6562)$ (the range where the lemma holds).
  Entry is flat on the full branch and falls on the threshold branch, as in the one-slot model.
- A selection across branches can still rise ($1/4<0.278<0.353$), as in T6 Result 6.6. It is not one branch.

**Scorecard.** 1–3: hold, analytical/computer-assisted. 4: coexistence holds; no single branch rises; documented failure.
5: holds at $r=3$. 6: none. 7: TH needs IM and CM; FF and NT are strict. 8: as Extension A. 9–10: as Extension A.

---

### 2.3 Extension C: one informed unit and a choice of trade date

**Model change.** There are $n$ slots. With probability $\lambda$ one informed investor is present for the whole
window (EGJ's presence reading). It sees the class and has one unit. At each slot a liquidity order arrives,
unless the investor trades at that slot; its unit order then replaces the liquidity order. The investor can wait,
see the orders, and trade at most once. It holds to the sale.
Menus: two-sided, or buy-only (class L never trades). Concept, beliefs and tie rules as in §2.0.
Script: `single_unit_timing.py`, output `single_unit_timing.out.txt`.

**Result C1 (analytical). The cap is on volume, not on rounds.** For every $n$, every adaptive and mixed timing
strategy, and every order history $h$,

$$
\Pr(h\mid j)=\prod_s\eta(q_s)\,\big[(1-\lambda)+\lambda\,\psi_j(h)\big],\qquad
\psi_j(h)=\sum_t\pi^j_t(h)\,\frac{\mathbf1\{q_t=o_j\}}{\eta(q_t)}+\pi^j_\infty(h)\in[0,1/\beta].
$$

Here $\pi^j_t(h)$ is the probability that the investor trades exactly at slot $t$ along $h$.
$\pi^j_\infty(h)$ is the probability that it never trades, and $o_j$ is its order.
The $\pi$ terms sum to one, and $1/\eta(\pm1)=1/\beta\ge1$.
Hence, for the two-sided menu,

$$
\frac{1}{1+u}\le\frac{\Pr(h\mid H)}{\Pr(h\mid L)}\le1+u,\qquad u=\frac{\lambda}{(1-\lambda)\beta},
$$

and every posterior lies in $[1-M,M]$, the one-slot bound. For the buy-only menu, $\psi_L=1$ and the ratio lies in
$[1-\lambda,\,1+\lambda(1-\beta)/\beta]$. The rule assumes that the investor never takes a slot with a zero order.
A check over 4000 random strategy profiles finds the maximum ratio $29/11=1+u$ in both menus (output, Section 1).

**Result C2 (analytical). Prop. 2(i) and (iii) for every $n$.** Let $M\in[\tau(3),\tau(3.6))$, T2's strip.

- At $r_0$, $\Delta<k$: no informed trade.
- At $r=3.6$, every posterior is at most $M<\tau(3.6)$ by C1, so entry is $\rho$ in every equilibrium.
  With $e=\rho$, a trade at any date earns at least $\rho\Delta(1-M)-k=1283/28800>0$.
  So the present investor trades with probability one, and prices are informative.

**Result C3 (analytical for the buy-only menu, any $n$). Informed trade wants to be seen.**
Consider the profile "class H trades at the first slot". Under it, later orders carry no information,
so the final posterior is $\mu_1(q_1)$. If class H waits, $q_1$ is a liquidity order.
A later buy is read as liquidity, so the investor earns $e(\mu_1(q_1))\Delta(1-\mu_1(q_1))$.
Let $m_0=\mu_1(0)=(1-\lambda)/(2-\lambda)$. Every later date gives the same price, so waiting is worth
$\beta[e(M)\Delta(1-M)-k]^++(1-\beta)[\rho\Delta(1-m_0)-k]^+$.
To trade now is worth $e(M)\Delta(1-M)-k$.

- *With price access at $r=3$* ($e(M)=1$): the first date is optimal if $1-M\ge\rho(1-m_0)$. This holds whenever $M\le3/4$.
  So the profile is an equilibrium for every $n$.
- *With hidden prices, or at $r=3.6$* ($e=\rho$ everywhere): both terms are positive, since $\rho\Delta(1-M)>k$ on the strip.
  So waiting minus trading now equals $(1-\beta)\rho\Delta(M-m_0)>0$, because $m_0<1/2<M$.
  The profile is not an equilibrium. The investor hides.

At $n=2$, $\beta=1/5$, $\lambda=9/22$ ($M=29/40$), the equilibria found are:

| case | equilibrium | entry |
|---|---|---|
| $r=3$, access | first date ($x_H=1$); now $0.163333$ against waiting $0.100476$ | $23/44=0.522727$ |
| $r=3$, access | second date ($x_H=0$) | $23/44$ |
| $r=3$, access | $x_H=467/531$, challenger mixes at $(+,0)$ with probability $0.328370$ (CM) | $0.371333$ |
| $r=3$, hidden | mixed date, $x_H\approx0.485949$ (bracket width below $10^{-10}$) | $1/4$ |
| $r=3.6$, access | the same mixed date | $1/4$ |

These rows are computer-assisted: exact payoffs at rational strategies, with rational brackets for the mixtures.
The grid search (step $1/50$, then bisection) found no other equilibrium. Completeness is a numerical diagnostic.

**Reading.** In Kyle and Glosten–Milgrom, an informed trader prefers to hide in liquidity (M01, M02; abstract only).
Here the feedback reverses this preference. A trade that the market reads as informed recruits the challenger,
and the investor shares the gain $\Delta(1-M)$. A hidden trade earns only $\rho\Delta(1-m_0)$.
So the visibility motive exists exactly when prices can recruit entry. The feedback also creates a coordination
problem on the date. This is a new source of multiple equilibria; the entry level differs across them ($0.523$ against $0.371$).

**Result C4 (computer-assisted, $n=2$). Bad news waits; $(1,-v)$ returns as a timing pattern.**
Take the two-sided menu at calibration A ($\beta=1/3$, $\lambda=6/17$, $M=29/40$).

- *The profile in which both classes trade at the first date is not an equilibrium at $r=3$.* Class L's sale now earns $31/1200$ net.
  If it waits, a liquidity buy at slot 1 (probability $1/3$) looks informed and recruits the challenger.
  Class L then sells at a price that includes entry, and earns $\Delta M-k=0.463$. Its value of waiting is $0.184$.
- *An equilibrium.* Class H trades at slot 1. Class L sells at slot 1 with probability $x_L\approx0.167235$
  and otherwise sells at slot 2 after every first order. Class L is indifferent ($0.041097$ for both dates).
  Class H strictly prefers the first date (gap $0.083191$). Entry is $91/204=0.446078$.
  Entry does not depend on $x_L$: the recruiting histories $(+,+)$ and $(+,0)$ have probability $(1-\beta)[\lambda+2(1-\lambda)\beta]/2$.
- *Prop. A.9 analog.* With hidden prices entry is $\rho$ in every equilibrium (Result C1 with $e=\rho$), and the
  present investor trades once in both regimes. So trade costs cancel. Access raises proceeds by $113/612=0.184641$
  and net surplus by $5/102=0.049020$.
- *At $r=3.6$ and with hidden prices at $r=3$*, both classes hide: a symmetric mixed date $x_H=x_L\approx0.503992$, entry $\rho$.

**Reading.** At the first date the orders are a full purchase and a partial sale, $(1,-0.167)$. The paper's
asymmetry $(1,-v)$ (Prop. 3) comes from the entry response to the sale. Here it comes from the same response,
through timing. A bad-news investor waits to sell into a false run-up that would recruit a poor challenger.
Once the market expects this delay, a sale after a buy is bad news ($\mu(+,-)=0.527$). The run-up then
no longer recruits after the delayed sale.

**Predictions.**

- Informed buying clusters at a focal date (for example, right after the sale becomes public) when entry can respond.
  It spreads over the window for weak or very strong incumbents, and where prices cannot recruit.
- Bad-news trades (short sales) arrive later in the window than good-news purchases, and often after run-ups.

**Scorecard (two-sided, calibration A, $n=2$).** 1: holds, analytical. 2: an equilibrium with entry $0.446>\rho$
(computer-assisted); uniqueness fails in the buy-only case. 3: holds for every $n$, analytical.
4: open (the profile "class H first, class L delays" fails at 1.55–1.65). 5: holds, sign analytical.
6: none. 7: date mixtures need an investor indifferent between two strictly profitable dates; the buy-only
threshold equilibrium needs CM. 8: $u$ on T2's strip, for every $n$. 9: EGJ presence and Dow–Gorton slot (verified);
"sunshine" trade by an informed investor has no verified precedent here (unverified).

---

### 2.4 Extension D: a Poisson number of arrivals

**Model change.** Extension A, but the number of slots $N$ is Poisson with mean $\Lambda>0$. It is independent of
everything else and public, because each arrival is seen.

**Result D1 (analytical). Prop. 2(iii) fails for every $\Lambda>0$ and every $u>0$.** Suppose entry is $\rho$ at every
history at $r=3.6$. Result A2, step 5, applies with the slot count $n$. Choose $n>L_2/\ln(1+u)$; then $\Pr(N=n)>0$.
The all-buy history of length $n$ recruits, a contradiction. Lemma 0 holds with a random horizon.

**Result D2 (analytical; exact factor). A lower bound valid in every equilibrium at calibration A.** At $r=3.6$:

- a slot-1 buy earns at least $\rho\Delta(1-29/40)-k=1283/28800>0$;
- a slot-2 buy after a buy earns at least $\rho\Delta(1-841/962)-k=2537/266400>0$.

So $(+,+)$ has posterior $841/962>\tau(3.6)$ in every equilibrium. Hence

$$
\mathsf E(3.6)\ge\rho+(1-\rho)\,e^{-\Lambda}\frac{\Lambda^2}{2}\cdot\frac{481}{2601}
=0.2605,\ 0.2755,\ 0.2875\quad(\Lambda=1/2,1,2).
$$

**Reading.** PIN-style arrival models with an unbounded count of informed trades (Easley et al. 1996, M04, abstract only)
cannot keep the paper's floor at strong incumbents. The bounded-noise failure returns as "long runs nearly reveal the class".
The ceiling moves to $\bar r=7.969$. A bounded informed volume (Extension C) is the remedy.

---

### 2.5 Remark: the timing of preparation (analytical)

Let the high-cost challenger prepare after any slot. Without a cost of delay, waiting is weakly optimal:
$\mathbb E[\max(B(\mu_n)-c_H,0)\mid h_t]\ge\max(B(\mu_t)-c_H,0)$, since $B$ is affine and $\mu$ is a martingale.
So the decision moves to the last slot and the cap applies to $\mu_n$.
With a probability $\delta$ that the opportunity closes at each delay, early preparation occurs only after strong early news.
Late preparation still uses the top posterior. So an option to prepare early cannot relax the cap; only a binding early
deadline (a smaller $n$) can. The zero-cost type prepares at once.

## 3. Ideas considered and dropped

1. **One long-lived investor who trades at every slot (Kyle style).** A retained position adds C2's inventory term
   (C2 eq. (17)). A two-round version is already in C2. Dropped for scope.
2. **The trade cost as a natural cap on beliefs.** Fails. Near $\tau(3.6)$ a buy that crosses the threshold earns
   about $(1-\mu)\Delta(3.6)\approx0.25\gg k$. With a two-sided menu, once class H stops buying, class L's sales
   make a wait good news, and beliefs keep rising.
3. **A PIN-style event that lasts the whole window, with fresh informed arrivals inside it.** The likelihood ratio
   of a run of buys still grows without bound in $n$. Same conclusion as Extensions A and D.
4. **Separate three-point noise in each slot (V1, V2 or T6 style).** It adds a knob but not a new dynamic effect. Dropped for scope.
5. **A random decision date.** This is a random $n$. If unbounded, Extension D applies. If bounded by $\bar n$, Extension A applies with $\bar n$.

## 4. Ranking

| Rank | Extension | Interest | Strength |
|---|---|---|---|
| 1 | C: one informed unit, date choice | New economics: visibility motive, delayed bad news, $(1,-v)$ at the first date; Prop. 2(iii) for every $n$ | Cap and visibility lemmas analytical; $n=2$ equilibria computer-assisted; middle strengths open |
| 2 | A: $n$ fresh slots, scaling law | Answers T6's constraint exactly; new ceiling prediction | Strip and decay analytical; tables computer-assisted |
| 3 | B: two-slot price path | New observables: state-dependent impact, early-trader term, informed buys after buys; the rising-entry obstacle | Exact; complete equilibrium list at 1.55–1.65 |
| 4 | D: Poisson arrivals | Clean negative corollary | Analytical |

## 5. Open issues

1. **open.** Extension C at 1.55–1.65 with the two-sided menu. The profile "class H first, class L delays" fails there
   (class H prefers to wait). The full date-mixture correspondence is not solved.
2. **open.** Extension C beyond $n=2$. The cap (C1), Prop. 2(iii) (C2) and the visibility lemma (C3) hold for every $n$.
   The equilibrium dates for $n\ge3$ are not computed.
3. **numerical diagnostic.** Completeness of the equilibrium list in Extension C at $n=2$ rests on a grid of step $1/50$ plus bisection.
4. **open.** Extension B covers $n=2$ at one rational point. The middle-strength classification for $n\ge3$ is open;
   Result B4 gives only the obstacle.
5. **open.** Continuous order sizes. X_check shows that a fractional order reaches an unused flow in V3. The same issue applies here.
6. **open.** Empirical content. Every proposed observable (date clustering, delayed short sales, state-dependent impact)
   needs a verified empirical source. None is in the permitted records. N1 covers observables.
7. **unverified.** Glosten–Milgrom, Kyle and Easley et al. are cited at abstract level only (`L1_survey.md` M01, M02, M04).
   "Sunshine" trade is not in the verified records.

## 6. Plain summary

The decision now follows a path of orders, not one order.

The main point is about informed volume. If one informed investor holds one unit, no number of trade rounds
moves beliefs beyond the one-slot bound. So the paper's return to the entry floor at 3.6 survives any number of
slots. The trade date then matters. When prices can recruit the challenger, a good-news investor wants its
trade to be seen, so it trades at a focal date. When prices cannot recruit, it hides by mixing over dates.
A bad-news investor waits, to sell into a false run-up that could recruit a poor challenger. At the first date
the orders are a full purchase and a partial sale, the paper's $(1,-v)$ pattern, now as a timing pattern.

If fresh informed investors arrive at each slot, information accumulates. To keep entry at the floor at 3.6,
each order must carry less information: $u_n\approx0.93/n$. Then extra entry at 3 falls to zero, roughly like
$e^{-0.31n}$. If the information per order stays fixed, the entry ceiling rises from 3.46 to 6.25 at two slots
and tends to 7.97. A Poisson number of arrivals breaks the floor at every arrival rate.

Two slots give a rich price path. The opening price already contains future entry. A buy after a buy moves the
price most, because it can trigger entry. Early informed buyers earn more: part of their return is the entry
that later buyers will trigger.

A richer path does not restore rising entry at 1.55–1.65. A last buyer at a history that recruits would be
indifferent only at a posterior near 0.8, above the 0.731 cap. At two slots the full list of equilibria is no
trade, a flat branch, and a branch whose entry falls.
