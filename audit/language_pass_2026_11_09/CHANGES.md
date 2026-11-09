# Second language pass on the main deck: change list (9 November 2026)

This list gives each changed sentence on main frames 1 to 19 of `slot/manuscript/slides.tex`. "Now" is the text at commit 8fe159a. "Proposed" is the text in this commit. Sign off or reject each line. The web slides (`presentation/content.js`) have the same words.

The five accuracy fixes have the mark **[Accuracy fix N]**:

1. Frame 5: the four random parts are mutually independent, as in the paper (§2.2).
2. Frame 14: the fixed inputs have names; $\lambda$ moves with $u$.
3. Frame 16: $\widehat\lambda$ has its definition before the existence statement; the word "equilibrium" comes only after existence. The foot line on class $L$ does not change.
4. Frame 18: the moment and its test hold within one public state (Appendix A8).
5. Frame 13: the intuition again says that informed trade stays at $F_2$ and only recruitment stops.

Other changes:

- Frame 16 has a new title. The `## Frame 16` heading in `slot/manuscript/slides_script.md` has the same new title. The speech text does not change.
- The header comment of `slides.tex` has the new rule for $\tau$: "preparation threshold" once, on frame 11, then "threshold". It also lists one name for each object.
- Backups B1 to B17 do not change.

## Frame 1

- Now: The seller seeks a rival bidder for a listed target. A stronger incumbent can help find one, or keep it out.
  Proposed: The seller seeks one more bidder for a listed target. A stronger incumbent can help find the rival, or keep it out.
- Now: The target's stock price can show if preparation is worth its cost.
  Proposed: The stock price can carry news on whether preparation pays.
- Now: The price can cause preparation, not only forecast it.
  Proposed: The price can change whether the rival prepares.
- Now (foot line): Here the sale rule is fixed. The question is entry.
  Proposed: With the sale rule fixed, the question is entry.

## Frame 2

- Now: The rival pays to learn its value for the target before it can bid.
  Proposed: The rival must pay to prepare before it learns its value and can bid.
- Now: Some rival preparation then no longer covers its cost. Entry cannot rise.
  Proposed: Some preparation then no longer pays, so entry cannot rise.
- Now: Here the strength shift is public. The incumbent's own value stays private.
  Proposed: Here strength is public; the incumbent's own value stays private.
- Now (takeaway): This holds when what the rival can learn before preparation stays fixed.
  Proposed: This answer holds the rival's news fixed. A stock price can change what the rival learns.

## Frame 3

- Now (table, price feedback): The decision is rival preparation
  Proposed: The rival decides whether to prepare
- Now (table, takeover trade): An outside informed trader: no net target position, and it cannot bid for control
  Proposed: An outside informed trader holds no net target position and cannot bid for control
- Now (takeaway): An outside informed trader can put news about the rival's synergy in the price. Incumbent strength can raise the return to that trade.
  Proposed: The sale splits one synergy gap between the rival and shareholders. A stronger incumbent can give shareholders more of it, so the informed trader can gain more.

## Frame 4

- Now (lead line): It can also widen the shareholder spread, the good-minus-poor synergy gap in target proceeds. Informed trade can then pay, and the price can recruit the high-cost rival.
  Proposed: It can also widen the shareholder spread, the good-minus-poor gap in target proceeds. The informed trader can then profit, and the price can recruit the high-cost rival.
- Now (item 1): entry can rise from the weak to the strong incumbent, then, at the very strong one, return to its floor set by zero-cost preparation.
  Proposed: entry can rise from the weak to the strong incumbent, then return to its floor at the very strong one.
- Now (item 3): when what the rival can learn before preparation is fixed, a stronger incumbent cannot raise entry.
  Proposed: with the rival's news fixed, a stronger incumbent cannot raise entry.
- Now (extensions): gains for target shareholders when the rival sees the price
  Proposed: gains for target shareholders from a visible price at the strong incumbent

## Frame 5

- Now: Values and costs are per share. The target's standalone value is set to $0$. All agents are risk neutral.
  Proposed: Values and costs are per share; the target's standalone value is $0$; all agents are risk neutral.
- Now (Incumbent row): it knows its value $R$ and faces no further preparation cost. All know the distribution $F$ of $R$, continuous on $[0,\bar r]$; no one else sees $R$ before bids.
  Proposed: no further preparation cost; value $R\sim F$, private until bids; $F$ is public and continuous on $[0,\bar r]$.
- Now (Incumbent row): **Stronger** means a distribution $\widetilde F$ that draws weakly higher values: $\widetilde F(y)\le F(y)$ for each $y$.
  Proposed: **Stronger:** $\widetilde F(y)\le F(y)$ for all $y$.
- Now (Rival row): **Synergy class:** $j=H$ (good synergy) or $j=L$ (poor synergy), with prior $\pi=\Pr(j=H)\in(0,1)$. Its value $\theta$ has distribution $G_j$ in class $j$; each $G_j$ has a finite mean.
  Proposed: **Synergy class** $j\in\{H,L\}$ ($H$ good, $L$ poor synergy), prior $\pi=\Pr(j=H)\in(0,1)$; value $\theta\mid j\sim G_j$, with finite mean.
- Now (Class ranking row): $G_H(y)\le G_L(y)$ for each $y$ — class $H$ draws weakly higher values. Also, for the reserve $p>0$ in the Sale row below, $\theta\ge p$ almost surely under each $G_j$.
  Proposed: $G_H(y)\le G_L(y)$ for all $y$, and $G_H(p^-)=G_L(p^-)=0$: every value meets the reserve $p$ (Sale row).
- Now (Class ranking row): The sale and the rival's identity are public; the synergy class is not, and the rival does not know it before preparation.
  Proposed: The sale and the rival's identity are public; $j$ is not.
- Now (Preparation cost row): $C=0$ with probability $\rho\in(0,1)$; else $C=c_H>0$, the high cost ($H$ in $c_H$ means high, not class $H$).
  Proposed: $\Pr(C=0)=\rho\in(0,1)$, else $C=c_H>0$, the high cost ($H$ for high, not class $H$).
- Now (Preparation cost row): To prepare is to pay $C$, learn $\theta$, and be able to bid; an unprepared rival cannot bid. ($\rho$ is the entry floor on frame 9.)
  Proposed: To prepare is to pay $C$, learn $\theta$ and be able to bid; an unprepared rival cannot bid.
- Now (Sale row): the seller commits before trade to a cash second-price auction with reserve $p>0$; frame 8 states the payment.
  Proposed: the seller commits before trade to a cash second-price auction with reserve $p>0$.
- **[Accuracy fix 1]** Now (foot): The pair $(j,\theta)$ is independent of $R$, $C$ and the trading-slot draws. Neither bidder trades target shares. Frame 6 adds the slot.
  Proposed: $(j,\theta)$, $R$, $C$ and the trading-slot draws (frame 6) are mutually independent. Neither bidder trades target shares.

## Frame 6

- Now: One trading slot comes before preparation. One trader submits one unit order $q$; the realised outcome is $X=q\in\{-1,0,1\}$: $-1$ stock sale order, $0$ no trade, $1$ stock purchase order.
  Proposed: One trader fills the slot with one unit order $q$; the outcome is $X=q\in\{-1,0,1\}$: stock sale order, no order, stock purchase order.
- Now: It observes the synergy class $j$ and chooses an order $q\in\{-1,0,1\}$; each nonzero order costs $k>0$.
  Proposed: It observes $j$ and chooses $q$ at cost $k|q|$, $k>0$.
- Now: With probability $1-\lambda$, the slot goes to a liquidity trader. Its order is drawn as $-1$, $0$, $1$ with probabilities $\beta$, $1-2\beta$, $\beta$, where $0<\beta\le 1/3$.
  Proposed: With probability $1-\lambda$, the slot goes to a liquidity trader: $\Pr(q=1)=\Pr(q=-1)=\beta$, $\Pr(q=0)=1-2\beta$, with $0<\beta\le 1/3$.
- Now: Competitive market makers observe the outcome $X$ only. They set $P(X)=\mathbb{E}[V_T\mid X]$, where $V_T$ is target proceeds per share. In equilibrium, this expectation already allows for the entry that the price itself causes.
  Proposed: Competitive market makers observe $X$ only and set $P(X)=\mathbb{E}[V_T\mid X]$, with $V_T$ target proceeds per share. The expectation includes the entry that the price itself causes.

## Frame 7

- Now (Seller, Observes): — (no private information)
  Proposed: —
- Now (Liquidity trader, Observes): no private information
  Proposed: —
- Now (Liquidity trader, Chooses): order in $\{-1,0,1\}$ drawn with probabilities $(\beta,\,1-2\beta,\,\beta)$, in that order
  Proposed: order drawn as on frame 6
- Now (Market makers, Chooses): price $P(X)=\mathbb{E}[V_T\mid X]$
  Proposed: price $P(X)$
- Now (Rival row): price $P$ only (not $X$ separately), then cost $C$; before preparation, neither $j$ nor $\theta$ | prepare or stay out; if it prepares, learn $\theta$, then bid $\theta$
  Proposed: price $P$ only (not $X$), then cost $C$; neither $j$ nor $\theta$ before preparation | prepare or stay out; if prepared, bid $\theta$
- Now: **Order belief:** for a realised value $x$ of $X$, $\mu(x)=\Pr(j=H\mid X=x)$ — the market makers' belief after outcome $X=x$.
  Proposed: **Order belief** (market makers): $\mu(x)=\Pr(j=H\mid X=x)$.
- Now: **Price belief:** for a seen price $\bar P$, $\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)$ — the rival's belief at that price. One price pools all outcomes with that price.
  Proposed: **Price belief** (rival): $\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)$; it pools all $x$ with $P(x)=\bar P$, so it need not equal $\mu(x)$ for one such $x$.

## Frame 8

- Now: Fix a prepared rival with value $\theta\ge p$. For one $R$, shareholders receive $\max\{p,\min(R,\theta)\}$. Averaged over $R$, expected target proceeds are $t(\theta)$. With $(z)_+=\max\{z,0\}$, expected rival gross profit is $g(\theta)=\mathbb E_R[(\theta-\max\{p,R\})_+]$, before cost $C$.
  Proposed: Prepared rival with value $\theta\ge p$: expected target proceeds $t(\theta)=\mathbb E_R[\max\{p,\min(R,\theta)\}]$ and expected rival gross profit $g(\theta)=\mathbb E_R[(\theta-\max\{p,R\})_+]$, before $C$.
- Now: $\mathbb E_j$ denotes expectation under $G_j$. Class means are $t_j=\mathbb E_j[t(\theta)]$ and $g_j=\mathbb E_j[g(\theta)]$.
  Proposed: Class means: $t_j=\mathbb E_j[t(\theta)]$, $g_j=\mathbb E_j[g(\theta)]$, with $\mathbb E_j$ under $G_j$.
- Now: With no prepared rival, the incumbent pays $p$ if $R\ge p$ and $0$ otherwise, so expected target proceeds are $t_0=p[1-F(p)]$.
  Proposed: With no prepared rival, target proceeds are $p\,\mathbf 1\{R\ge p\}$, so $t_0=p[1-F(p)]$.
- Now: **Shareholder spread:** $\Delta_T=t_H-t_L$ — extra expected target proceeds in class $H$ versus class $L$ if the rival prepares.
  Proposed: **Shareholder spread:** $\Delta_T=t_H-t_L$.
- Now: For any probability $\mu$ on class $H$, **rival gross profit** is $B(\mu)=g_L+\mu(g_H-g_L)$, the $\mu$-weighted mean of class gross profits, before $C$. At seen price $\bar P$, net gain from preparation is $B(\bar\mu(\bar P))-C$.
  Proposed: At belief $\mu=\Pr(j=H)$, **rival gross profit** is $B(\mu)=g_L+\mu(g_H-g_L)$; at price $\bar P$, the net gain from preparation is $B(\bar\mu(\bar P))-C$.
- Now: The informed trader who submits $q$ (so $X=q$) earns $q[V_T-P(q)]-k|q|$, with $V_T$ realised target proceeds per share.
  Proposed: The informed trader who submits $q$ (so $X=q$) earns $q[V_T-P(q)]-k|q|$.
- Now: A bidder who loses gets $0$; the incumbent, if it wins, gets $R$ minus its auction payment.
  Proposed: A winning bidder gets its value minus its payment; a losing bidder gets $0$.

## Frame 9

- Now: Solution concept: perfect Bayesian equilibrium with break-even prices from competitive market makers. Orders, prices, beliefs, and preparation must all fit the same $P(\cdot)$ and $e(\cdot)$.
  Proposed: Perfect Bayesian equilibrium with competitive (break-even) prices: orders, prices, beliefs and preparation all fit one pair $P(\cdot)$, $e(\cdot)$.
- Now (Orders row): let entry $e(x)$ be the probability the rival prepares when the realised outcome is $X=x$. The rival acts on price $P(x)$, not on $x$ itself.
  Proposed: entry $e(x)=\Pr(\text{rival prepares}\mid X=x)$ depends on $x$ only through $P(x)$.
- Now (Orders row): For an informed trader who sees class $j$ and submits $q$ (so $X=q$), expected net payoff is $U_j(q)=q[t_0+e(q)(t_j-t_0)-P(q)]-k|q|$; the term $t_0+e(q)(t_j-t_0)$ is expected target proceeds in class $j$ after $q$.
  Proposed: An informed trader who sees class $j$ has expected payoff $U_j(q)=q[t_0+e(q)(t_j-t_0)-P(q)]-k|q|$ from order $q$, where $t_0+e(q)(t_j-t_0)=\mathbb E[V_T\mid j,X=q]$.
- Now (Orders row): For each $j$, positive probability goes only to orders that maximise $U_j(q)$ at the equilibrium $P(\cdot)$ and $e(\cdot)$.
  Proposed: In each class $j$, it puts positive probability only on $\arg\max_q U_j(q)$ at the equilibrium $P(\cdot)$, $e(\cdot)$.
- Now (Competitive prices row): If the rival prepares, expected target proceeds are $t_L+\mu(x)\Delta_T$; if not, they are $t_0$. Because the $C=0$ rival prepares (last row), $e(x)\ge\rho$: $\rho$ is the entry floor.
  Proposed: The $C=0$ rival always prepares (last row), so $e(x)\ge\rho$: $\rho$ is the entry floor. A purchase **recruits** when $e(1)>\rho$, that is, when it brings in high-cost preparation.
- Now (Beliefs row): the order belief $\mu(x)=\Pr(j=H\mid X=x)$ follows Bayes' rule. The rival's price belief $\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)$ averages over all outcomes $x$ with $P(x)=\bar P$; it need not equal $\mu(x)$ for one such outcome.
  Proposed: $\mu(x)$ and $\bar\mu(\bar P)$ (frame 7) follow Bayes' rule given the order strategy.
- Now (Beliefs row): Liquidity trade gives each outcome positive probability in each class, so Bayes' rule pins down order beliefs.
  Proposed: Liquidity trade gives each outcome positive probability in each class, so Bayes' rule pins down the order beliefs.
- Now (Preparation and bids row): a rival with $C=0$ prepares at each price. With the high cost $C=c_H$, at seen price $\bar P$ it prepares if and only if $B(\bar\mu(\bar P))\ge c_H$.
  Proposed: a rival with $C=0$ prepares at each price; with $C=c_H$, it prepares at price $\bar P$ if and only if $B(\bar\mu(\bar P))\ge c_H$.
- Now (Preparation and bids row): A prepared rival bids $\theta$. The incumbent bids $R$, effective only if $R\ge p$.
  Proposed: Bids are **truthful**: a prepared rival bids $\theta$, the incumbent $R$.

## Frame 10

- Now: Let $F$ and $\widetilde F$ be continuous incumbent value distributions, with $\widetilde F(y)\le F(y)$ for every $y$.
  Proposed: Let $F,\widetilde F$ be continuous incumbent distributions, with $\widetilde F$ stronger: $\widetilde F(y)\le F(y)$ for every $y$.
- Now (gloss): At each value $y$, the stronger distribution puts weakly more mass above $y$.
  Proposed: (removed; frame 5 defines "stronger")
- Now: Hold the reserve and the finite-mean class distributions fixed.
  Proposed: Fix $p$ and the finite-mean class distributions $G_H,G_L$.
- Now (part a): Here $g_j(F)$ is class-$j$ mean rival gross profit under $F$. $B_F(\mu)=g_L(F)+\mu[g_H(F)-g_L(F)]$.
  Proposed: Here $g_j(F)$ and $B_F$ are $g_j$ and $B$ (frame 8) under $F$.
- Now (part b): Under the class ranking, $$G_H(y)\le G_L(y)\quad\text{for every }y,\qquad G_H(p^-)=G_L(p^-)=0,$$ the shareholder spread satisfies $\Delta_T(\widetilde F)\ge\Delta_T(F)$.
  Proposed: Under the class ranking (frame 5), the shareholder spread satisfies $\Delta_T(\widetilde F)\ge\Delta_T(F)$.
- Now (gloss): Good-synergy values weakly dominate in the first-order sense.
  Proposed: (removed; frame 5 defines the class ranking)
- Now: … $=\mathbb E_H[\theta]-\mathbb E_L[\theta]$. The right side does not depend on $F$.
  Proposed: … $=\mathbb E_H[\theta]-\mathbb E_L[\theta]$, which does not depend on $F$.
- Now (intuition): A stronger incumbent can shift part of the between-class gap in rival gross profit to the target's shareholders.
  Proposed: A stronger incumbent can move part of the good-minus-poor value gap from the rival to target shareholders.

## Frame 11

- Now (subtitle): With a positive spread, the price reveals the order belief
  Proposed: With a positive shareholder spread, the price reveals the order belief
- Now (gloss): Here $b$ is the liquidity mass on one order direction, and $u$ is the mass ratio.
  Proposed: Here $b$ is the liquidity mass on one order direction, $u$ the mass ratio, $M$ the top belief and $m$ the band floor.
- Now: For every pure or mixed order strategy of the informed trader, and for every $x\in\{-1,0,1\}$,
  Proposed: For every order strategy (pure or mixed) and every $x\in\{-1,0,1\}$,
- Now (display, second line): $\Pr(H\mid P(X)=P(x))=\mu(x)$.
  Proposed: $\bar\mu(P(x))=\mu(x)$.
- Now (preparation rule): The price reveals $\mu(x)$. Under the default rule (a rival at the threshold prepares), entry $e(x)$ after order $x$ is
  Proposed: If an indifferent rival prepares, entry $e(x)$ after order $x$ is
- Now (display): $C=c_H:\ \text{prepare exactly when }\mu(x)\ge\tau$, then $e(x)=\rho$ if $\mu(x)<\tau$, $e(x)=1$ if $\mu(x)\ge\tau$.
  Proposed: $e(x)=\rho$ if $\mu(x)<\tau$, $e(x)=1$ if $\mu(x)\ge\tau$. (The first display line repeated the rule above it.)
- Now (intuition): Liquidity trade covers all three outcomes, so an order can move the belief but never to 0 or 1.
  Proposed: A liquidity order can match any informed order, so an order moves the belief but leaves doubt about the class.

## Frame 12

- Now: Let $\Delta_T\ge0$ and $k>0$. Take any order strategy with Bayes beliefs, competitive prices, truthful bids, and $e(x)\in[\rho,1]$.
  Proposed: Fix a shareholder spread $\Delta_T\ge0$ and any order strategy, with Bayes beliefs, competitive prices, truthful bids and $e(x)\in[\rho,1]$. ($k>0$ is on frame 6.)
- Now: Call a purchase ($x=1$) in class $H$ and a sale ($x=-1$) in class $L$ the correct orders.
  Proposed: Call a purchase ($x=1$) in class $H$ and a sale order ($x=-1$) in class $L$ the correct orders.
- Now (gloss): The value $\kappa(\pi)$ is the smallest posterior weight left on the far class when an order moves the belief to a band endpoint.
  Proposed: $\kappa(\pi)$ is a lower bound on the doubt that a correct order leaves.
- Now: For either class $j\in\{H,L\}$, $$\rho\kappa(\pi)\Delta_T\le K_j\le\Delta_T.$$
  Proposed: $$\rho\kappa(\pi)\Delta_T\le K_j\le\Delta_T\qquad(j\in\{H,L\}).$$
- Now: Net of the order cost $k$, a wrong-signed order earns at most $-k<0$. Abstention earns zero, gross and net.
  Proposed: Net of the order cost, wrong-signed orders give $U_H(-1),U_L(1)\le-k<0$; no order earns zero, gross and net.
- Now: The informed trader who sees class $H$ buys if $K_H>k$ and abstains if $K_H<k$. The informed trader who sees class $L$ sells if $K_L>k$ and abstains if $K_L<k$.
  Proposed: The informed trader in class $j$ sends the correct order if $K_j>k$ and no order if $K_j<k$.
- Now: At $K_j=k$, the correct order and abstention are both optimal, as is any mixture of the two.
  Proposed: At $K_j=k$, the correct order, no order and every mixture of the two are optimal.
- Now (intuition): Gross gain equals entry probability times shareholder spread times residual doubt. Net gain subtracts $k$, so doubt alone does not pay.
  Proposed: Gross gain equals entry probability times shareholder spread times the doubt left after the order. Net gain subtracts the order cost, so doubt alone does not pay.

## Frame 13

- Now: Classes have finite means and satisfy $G_H\le G_L$, $G_H(p^-)=G_L(p^-)=0$.
  Proposed: Classes have finite means and satisfy the class ranking (frame 5).
- Now: Write $\Delta_i=\Delta_T(F_i)$ and $B_i=B_{F_i}$.
  Proposed: Write $\Delta_i=\Delta_T(F_i)$ for the shareholder spread and $B_i=B_{F_i}$.
- Now (gloss): (H2) Order cost $k$ is above the gross-gain cap at $F_0$, below the gross-gain floor at $F_1$.
  Proposed: (H2) At $F_0$ no correct order can cover $k$; at $F_1$ each correct order covers $k$.
- **[Accuracy fix 5]** Now (intuition): A wider shareholder spread pays for informed trade, and a purchase recruits; at $F_2$, the top belief misses the threshold.
  Proposed: A wider shareholder spread pays for informed trade, and a purchase recruits; at $F_2$, trade stays but no order recruits.

## Frame 14

- Now: Each class has one sure value per share: $\theta=h$ in class $H$ (good synergy) and $\theta=\ell$ in class $L$ (poor synergy), with $(h,\ell,p)=(\ldots)$ for the reserve $p$.
  Proposed: Point-mass classes $G_H=\delta_h$, $G_L=\delta_\ell$ and reserve $p$: $(h,\ell,p)=(\ldots)$.
- Now: The incumbent has $R\sim\mathrm{Unif}[0,r]$, and a larger $r$ is a stronger incumbent: $(r_0,r_1,r_2)=(\ldots)$ play the roles of $F_0,F_1,F_2$ on frame 13.
  Proposed: The incumbent has $R\sim\mathrm{Unif}[0,r]$, so a larger $r$ is stronger: $(r_0,r_1,r_2)=(\ldots)$ play the roles of $F_0,F_1,F_2$ (frame 13).
- Now: Write $\tau(r)$ for the frame 11 preparation threshold at strength $r$.
  Proposed: Write $\tau(r)$ for the threshold (frame 11) at strength $r$.
- **[Accuracy fix 2]** Now: Fix $\pi=1/2$ and the inputs below. Let only the frame 11 mass ratio $u=\lambda/b$ vary, and $M(1/2)$ with it; the legs of (H1)–(H2) at $r_0$ do not involve $u$.
  Proposed: Fix $\pi=1/2$ and $\rho$, $c_H$, $k$, $\beta$ (below). Vary only $u$ (frame 11), so $\lambda$ and $M(1/2)$ move with it; the legs of (H1)–(H2) at $r_0$ do not involve $u$.
- Now: The example sets $u=\mathrm e-1$, so the top belief after a purchase is $M(1/2)=\mathrm e/(1+\mathrm e)\simeq\ldots$
  Proposed: The example sets $u=\mathrm e-1$, so $M(1/2)=\mathrm e/(1+\mathrm e)\simeq\ldots$
- Now: Hence (H1)–(H3) hold, and by Proposition 2 entry is $\rho$, then above $\rho$, then $\rho$ again.
  Proposed: Hence (H1)–(H3) hold, and by Proposition 2, $\mathsf E_0=\mathsf E_2=\rho<\mathsf E_1$.
- Now (intuition): … the threshold has risen to just above that same belief.
  Proposed: … the threshold has risen above that same belief.
- Now (foot line): liquidity chance $\beta=\ldots$, which with …
  Proposed: $\beta=\ldots$, which with …

## Frame 15

- Now: Hold fixed the joint distribution of $(j,S)$, the class value distributions $G_j$, the reserve $p$ and the preparation-cost distribution; only the incumbent's distribution moves, from $F_0$ to $F_1$.
  Proposed: Fix $G_j$, $p$, the joint distribution of $(j,S)$ and the distribution of $C$; only $F$ moves, from $F_0$ to $F_1$.
- Now: In economy $i$, given $(j,S)$, the values $\theta\sim G_j$ and $R\sim F_i$ are independent, and $C$ is independent of $j$, $\theta$, $R$ and $S$.
  Proposed: In economy $i$, $$(\theta,R)\mid(j,S)\sim G_j\otimes F_i,\qquad C\perp(j,\theta,R,S).$$
- Now: Let an indifferent rival prepare, and let $F_1\le F_0$ (economy 1 has the stronger incumbent). Then entry cannot rise: $$\mathsf E_1\le\mathsf E_0,$$ where $\mathsf E_i$ is total entry in economy $i$. The fall is exact: with $\mu(S)=\Pr(j=H\mid S)$ and $B_i$ rival gross profit at $F_i$, $\mathsf E_0-\mathsf E_1=\Pr\{B_1(\mu(S))<C\le B_0(\mu(S))\}$.
  Proposed: Let $F_1\le F_0$ and let an indifferent rival prepare. With $\mu(S)=\Pr(j=H\mid S)$, $B_i=B_{F_i}$ and total entry $\mathsf E_i$, entry cannot rise, and the fall is exact: $$\mathsf E_1\le\mathsf E_0,\qquad \mathsf E_0-\mathsf E_1=\Pr\{B_1(\mu(S))<C\le B_0(\mu(S))\}$$ (two display lines).

## Frame 16

- Now (title): A wider spread raises the chance the trader learns the class, up to $\bar\lambda$
  Proposed: A wider shareholder spread raises research, up to $\bar\lambda$
- Now: One change from frame 6: before the slot, the informed trader chooses research $\lambda\in[0,\bar\lambda]$ at cost $(a/2)\lambda^2$, with $a>0$ and $0<\bar\lambda<1$.
  Proposed: One change from frame 6: the informed presence $\lambda$ becomes research, chosen before the slot in $[0,\bar\lambda]$ at cost $(a/2)\lambda^2$, with $a>0$ and $0<\bar\lambda<1$.
- Now: Research is all-or-nothing: with probability $\lambda$ the trader learns the synergy class and fills the slot; otherwise liquidity fills it.
  Proposed: With probability $\lambda$, research reveals the synergy class and the trader fills the slot; otherwise liquidity fills it.
- **[Accuracy fix 3]** Now: Market makers and the rival see neither $\lambda$ nor the result; they use the equilibrium $\widehat\lambda$.
  Proposed: Market makers and the rival observe neither $\lambda$ nor the result.
- Now: … $\beta\le1/3$ and preparation threshold $\tau>1/2$.
  Proposed: … $\beta\le1/3$ and threshold $\tau>1/2$.
- Now: At research $\lambda$, write $M_\lambda$ for the top belief after a purchase and $m_\lambda=1-M_\lambda$ for the band floor.
  Proposed: At research $\lambda$, write $M_\lambda$ for the top belief and $m_\lambda=1-M_\lambda$ for the band floor.
- **[Accuracy fix 3]** Now: … equals the expected trading payoff after a success (B12). Equilibrium research is $\widehat\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}$.
  Proposed: … equals the expected trading payoff after a success (B12), and set $\widehat\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}$.
- Now: The recruiting equilibrium, in which a trader whose research shows class $H$ buys and a purchase recruits, exists exactly when
  Proposed: The recruiting equilibrium, in which a trader who learns class $H$ buys and a purchase recruits, exists exactly when
- Now: In it, with $a$, $k$, $\rho$ and $\beta$ fixed, research $\widehat\lambda$ rises strictly …
  Proposed: In it, with $a,k,\rho,\beta,\bar\lambda$ fixed, research $\widehat\lambda$ rises strictly …
- Now (intuition): A wider shareholder spread pays for more research, up to the cap; more research sorts entry toward good synergy.
  Proposed: A wider shareholder spread pays for more research, up to the cap; entry rises under good synergy and falls under poor.
- The foot line on class $L$ does not change: "After a class-$L$ success, the trader abstains while $\rho\Delta_T\le2k$ and otherwise sells with positive probability."

## Frame 17

- Now: Hold the incumbent at $F_1$ (strong) under Proposition 2's hypotheses. Compare two economies: the rival sees the price before it decides whether to prepare, or sees neither the price nor the order. Hold all other primitives fixed.
  Proposed: Under Proposition 2's hypotheses, hold the incumbent at $F_1$ (strong) and all other primitives fixed. Compare economy $1$, where the rival sees the price before it decides whether to prepare, with economy $0$, where it sees neither the price nor the order.
- Now: Market makers still set a competitive price in both economies; only the rival's access changes.
  Proposed: Market makers set a competitive price in both; only the rival's access changes.
- Now: Superscripts $1$ and $0$ denote price access and access to neither price nor order.
  Proposed: (removed; the economy numbers above give the superscripts)
- Now: Both economies keep unique full informed orders (class $H$ buys; class $L$ sells).
  Proposed: Both economies keep unique **full informed orders**: class $H$ buys; class $L$ sells.
- Now: Access adds preparation after a purchase only, where gross profit at the top belief, $B_1(M(\pi))$, exceeds $c_H$.
  Proposed: Access adds high-cost preparation only after a purchase, where rival gross profit at the top belief, $B_1(M(\pi))$, exceeds $c_H$.
- Now (intuition): The price tells the rival the belief after a purchase. Access then adds high-cost preparation only there, where gross profit covers $c_H$.
  Proposed: Access adds a bidder only where the price shows that preparation covers the high cost.

## Frame 18

- **[Accuracy fix 4]** Now: Assume the class ranking, $\Delta_T>0$, $g_H>g_L$, full two-sided trade (class $H$ buys; class $L$ sells), and $\pi<\tau$.
  Proposed: Within one public state (fixed target, prior, slot and incumbent distribution), assume the class ranking, $\Delta_T>0$, $g_H>g_L$, full informed orders (frame 17) and $\pi<\tau$.
- Now: $P(x)$ is the price after order $x$, and $e(1)>\rho$ means that a purchase recruits.
  Proposed: (removed; frame 6 defines $P(x)$ and frame 9 defines "recruits")
- Now (display): $\bar f(1)I_+-\bar f(-1)I_->0$ on one line, $\Longleftrightarrow e(1)>\rho$ on the next.
  Proposed: $\bar f(1)I_+-\bar f(-1)I_->0\quad\Longleftrightarrow\quad e(1)>\rho$ on one line, as the second display.
- Now: At $\pi=1/2$, the order frequencies are equal, so
  Proposed: At $\pi=1/2$, $\bar f(1)=\bar f(-1)$, so
- Now (intuition, second sentence): So frequency-weighted purchase impact exceeds frequency-weighted sale-order impact exactly when a purchase recruits.
  Proposed: So, weighted by order frequency, a purchase raises the price more than a sale order lowers it exactly when a purchase recruits.
- Now (foot line): With no recruitment ($e(x)=\rho$ after each outcome), orders still predict the winner when $W_H>W_L$: B13.
  Proposed: With no recruitment ($e(\cdot)=\rho$), orders can still predict the winner: B13. (The undefined $W_H>W_L$ leaves; "can" keeps the condition, which B13 states.)
- **[Accuracy fix 4]** Now (foot line): Empirical moment: average the pre-preparation price by order outcome over slots fixed in advance, record no order as an outcome, and test the sample analogue of $\bar f(1)I_+-\bar f(-1)I_->0$.
  Proposed: Empirical moment: within one public state, average the pre-preparation price by order outcome, no order included, over slots fixed in advance; test the sample analogue of $\bar f(1)I_+-\bar f(-1)I_->0$.

## Frame 19

- Now (lead line): A stronger incumbent can induce rival entry through a more informative stock price.
  Proposed: A stronger incumbent does not always keep the rival out: it can make the stock price more informative, and that price can recruit the rival.
- Now (Discipline): Strength weakly cuts rival gross profit and weakly widens the shareholder spread. With pre-preparation information fixed, strength cannot raise entry.
  Proposed: Strength weakly cuts rival gross profit and weakly widens the shareholder spread; with the rival's news fixed, it cannot raise entry.
- Now (label): **Implication.**
  Proposed: **Extensions.** The bullet now has two sentences. A new bullet, **Prediction.**, holds the data sentence.
- Now: (no sentence on research)
  Proposed (Extensions): Where the recruiting equilibrium exists, a wider shareholder spread raises costly research by the informed trader, up to its cap.
- Now (Implication): At the strong incumbent, letting the rival see the price raises expected target proceeds and acquisition surplus net of preparation costs.
  Proposed (Extensions): no change to this sentence.
- Now (Implication): In data, frequency-weighted purchase impact exceeds frequency-weighted sale-order impact exactly when a purchase recruits.
  Proposed (Prediction): In data, weighted by order frequency, a purchase raises the price more than a sale order lowers it exactly when a purchase recruits.
