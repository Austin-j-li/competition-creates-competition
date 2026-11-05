# Theory register: definitions, information, and result slides

## Recommendation in brief

Put one slide, **Primitives**, at the head of the model block as Slide 4. Define each symbol there with a short gloss, in the form “the second buyer’s value $\theta$”. Repeat the gloss at the first use on each later face. Use the symbol alone after that on the same face. Do not spread first definitions across Slides 4–6, as the deck now does ($F,\pi$ on Slide 4, $k$ on Slide 5, $\Delta_T$ on Slide 6, and $\lambda,\beta,\rho,C,c_H$ on no main face).

Quint asks speakers to define terms with care, reach the model fast, and show only equations with a purpose. Li reserves slides for material that must be exact (definitions, theorems) and reserves the labels Proposition, Lemma, and Corollary for precise, proved claims. The exemplar decks state primitives at the start of the model block. None uses a free glossary slide before the model. B15 can stay as the handout list, with the corrections below.

**Finance-theory words.** Use the terms of Kyle (1985), Glosten–Milgrom (1985), Dow–Gorton (1997), and Edmans–Goldstein–Jiang (2015), in plain form: informed trading, a liquidity trader, competitive market makers with a break-even price $P=\mathbb{E}[V_T\mid X]$, Bayesian posteriors, price informativeness, and feedback from the stock price to a real decision (here, preparation). Three cautions. First, do not call the single slot order $X$ “order flow”: in Kyle, order flow is an aggregate order. Say “the order $X$” or “order realisation $x$”. Second, do not rename the paper’s equilibrium on the face. The paper defines an equilibrium by six conditions (E1)–(E6), with competitive pricing and with an investor deviation that faces fixed $P(\cdot)$ and $e(\cdot)$. That structure is close to perfect Bayesian equilibrium with a break-even pricing rule, and speech can say so in one line. The face should say **Equilibrium** and state the conditions, as those four papers do. Third, “price informativeness” should attach to a stated object: the posterior spread $M(\pi)-m(\pi)$, or $\mu(x)\neq\pi$. A bare claim that a price is “informative” is not a definition.

## 1. The definitions slide

**Place.** Inside the model block, first. It replaces the face line on Slide 4 and the synergy footnote on Slide 5. The timeline line keeps the timing role of Slide 4. A glossary before the model gives symbols with no question to attach them to.

**Exact draft.**

> **Title: Primitives**
>
> - **Sale.** The target has standalone value $0$. Values and costs are per share. Risk neutrality throughout. Before trade, the seller commits to a cash second-price auction with the reserve $p>0$.
> - **First buyer.** Prepared, with no further entry cost. The first buyer’s value is $R$, with law $F$: continuous and public. The draw $R$ stays private until bids. A stronger first buyer is a first-order stochastic strengthening of $F$.
> - **Second buyer.** Its type is $j\in\{H,L\}$: $j=H$ is good synergy, $j=L$ is poor synergy. The prior is $\pi=\Pr(j=H)\in(0,1)$. The second buyer’s value $\theta$ has law $G_j$. **Class ranking:** $G_H(y)\le G_L(y)$ for all $y$, and $G_H(p^-)=G_L(p^-)=0$.
> - **Preparation.** The preparation cost is $C\in\{0,c_H\}$, with $\Pr(C=0)=\rho\in(0,1)$ and $c_H>0$. Payment of $C$ reveals $\theta$ and permits a bid. No payment means no bid.
> - **Trading.** One order comes before the preparation choice. With probability $\lambda\in(0,1)$ the informed investor trades: it observes $j$ and chooses the order $q\in\{-1,0,1\}$; a non-zero order costs $k>0$. With probability $1-\lambda$ the liquidity trader trades and draws $\{-1,0,1\}$ with probabilities $(\beta,\,1-2\beta,\,\beta)$, $0<\beta\le 1/3$. Competitive market makers observe the order $X$ and set the break-even stock price $P=\mathbb{E}[V_T\mid X]$, for the terminal payoff per share $V_T$.
> - $(j,\theta)$, $R$, $C$, and the trading draws are mutually independent. Neither buyer trades target shares.
>
> Timeline: seller commits to $p$ $\to$ order $X$ $\to$ stock price $P$ $\to$ second buyer learns $C$, then prepares or stays out $\to$ bids and payoffs.

Speech only: support $[0,\bar r]$ for $F$; finite means and atoms for $G_j$; good synergy as a business that complements the second buyer’s business, poor synergy as overlap. The bound $\bar r$ and $D(y)=G_L(y)-G_H(y)$ stay in backups.

## 2. Slide 5: who observes what

**Exact draft.**

> **Title: Information and actions**
>
> | Player | Observes | When | Chooses |
> |---|---|---|---|
> | Seller | No private draw | Before trade | Commits to the second-price auction with the reserve $p$ |
> | First buyer | The first buyer’s value $R$ | Before bids | Its bid: a value at or above $p$ bids its value |
> | Second buyer | The stock price $P$, then the preparation cost $C$. Not $X$, $j$, $\theta$, or $R$ | After $P$ is set | Prepare (pay $C$, learn $\theta$, bid $\theta$ if $\theta\ge p$) or stay out |
> | Informed investor | The type $j\in\{H,L\}$. Not the second buyer’s value $\theta$ | Before its order, if it trades (probability $\lambda$) | The order $q\in\{-1,0,1\}$, at cost $k$ if $q\neq0$ |
> | Liquidity trader | No information on $j$ | If it trades (probability $1-\lambda$) | Draws $\{-1,0,1\}$ with probabilities $(\beta,\,1-2\beta,\,\beta)$ |
> | Market makers | The order $X$ only. Not the trader identity, not $j$ | After $X$ | The break-even stock price $P=\mathbb{E}[V_T\mid X]$ |
>
> Foot lines: No one observes who trades. Each order has positive probability under each type. Write $\mu(x)=\Pr(j=H\mid X=x)$ for the Bayesian posterior after the order $x$.

Three changes matter. “Knows” becomes “Observes”, the standard head for information sets; “knows” overstates what $P$ gives the second buyer. “Diligence bill” becomes “the preparation cost $C$”, the paper’s one cost object. The second buyer’s row now gives the paper’s order: $P$ first, $C$ after.

## 3. The model block, Slides 4–7

| Slide | Face | To speech |
|---|---|---|
| 4. Primitives | Section 1 draft | Player examples; support, atoms, per-share scale |
| 5. Information and actions | Section 2 draft | What good and poor synergy mean; why the investor can observe $j$ but not $\theta$ |
| 6. Payoffs | Title **Payoffs**. For a prepared second buyer with $\theta\ge p$: $t(\theta)=\mathbb{E}_R[\max\{p,\min(R,\theta)\}]$, $g(\theta)=\mathbb{E}_R[(\theta-\max\{p,R\})_+]$, $t(\theta)+g(\theta)=\theta$. Class means $t_j=\mathbb{E}_j[t(\theta)]$, $g_j=\mathbb{E}_j[g(\theta)]$; the shareholder spread $\Delta_T=t_H-t_L$; proceeds with no entry $t_0=p[1-F(p)]$; gross profit at belief $\mu$, $B(\mu)=g_L+\mu(g_H-g_L)$. Informed trading with order $q$ earns $q[V_T-P(q)]-k\lvert q\rvert$ | “One value, two pockets”. Keep the number line with labels “target proceeds $t(\theta)$” and “gross profit $g(\theta)$”, and label it “at one draw $R$” |
| 7. Equilibrium | Title **Equilibrium**. A definition block: for each $j$, a distribution over orders; $\mu(x)$ and $P(x)$ after each $x$; the second buyer’s belief at each price; preparation at each price and cost; truthful bids. Conditions: (i) each order in use maximises $U_j(q)=q[t_0+e(q)(t_j-t_0)-P(q)]-k\lvert q\rvert$ at the stated $P$ and $e$; (ii) $P(x)=\mathbb{E}[V_T\mid X=x]=t_0+e(x)[t_L-t_0+\Delta_T\mu(x)]$; (iii) Bayes’ rule for $\mu(x)$ and for beliefs at a price, with each $x$ on path; (iv) $C=0$ prepares at each price, and $C=c_H$ prepares exactly when $B$ at its belief reaches $c_H$. Entry after $x$ is $e(x)\ge\rho$ | Tie rules in one line; the full (E1)–(E6) list on B8; “each strength needs a fresh solution” |

Two cautions. The paper keeps $\mu(x)$ apart from the second buyer’s belief at a price. They agree only after the Slide 9 argument, which needs $\Delta_T>0$ and $e(x)\ge\rho$. Do not merge them on Slide 7. The threshold $\tau=(c_H-g_L)/(g_H-g_L)$ needs $g_H>g_L$; state $\tau$ on Slide 9 with that condition.

## Paper check: traps in the present deck

- B15 glosses $\mu$ as $\Pr(H\mid P)$. The paper sets $\mu(x)=\Pr(j=H\mid X=x)$; the belief at a price is separate. B15 also gives $R\sim U[0,r]$ as the general law (the uniform law is the example alone) and writes $e_r(\mu)$ (the paper writes entry $e(x)$ after the order $x$).
- $t(\theta)$ and $g(\theta)$ are expectations over $R$, not splits at a known $R$. Label the Slide 6 line as one draw.
- Proposition 1(a) needs no class ranking; part (b) needs it. Exact identity, under the ranking: $\Delta_T(F)+g_H(F)-g_L(F)=\mathbb{E}_H[\max\{\theta,p\}]-\mathbb{E}_L[\max\{\theta,p\}]$.
- On Slide 14, $\lambda$ becomes a choice in $[0,\bar\lambda]$ at cost $(a/2)\lambda^2$, made before the investor learns $j$. Say “$\lambda$, now chosen” at first use.

## 4. The rest of the deck

| Slide | Move to theory form | Keep in plain words |
|---|---|---|
| 1 | Line 1 may name objects: “At fixed information, a strengthening of $F$ weakly lowers $B(\mu)$ at each $\mu$.” | The title question and the three-line arc. “Pocket” goes to speech |
| 2–3 | Name the added objects once (a pre-entry price, cost $C$, spread $\Delta_T$; “second price, reserve $p$”). Use “prices guide real decisions” and “feedback” in the Edmans–Goldstein–Jiang sense | The contribution line; the generic setting |
| 8 | Proposition 1 block, with “Let $\tilde F\le F$ strengthen $F$”, the ranking scope per part, and the identity in symbols | One intuition line: one class gap, and strength moves its split |
| 9 | Title **Posterior bounds and the preparation threshold**. State $\mu(x)\in[m(\pi),M(\pi)]$ for each order rule; define $\tau$ under $g_H>g_L$; call $M(\pi)-m(\pi)$ the bound on price informativeness. “Doubt left” becomes residual uncertainty, $1-\mu(1)$ or $\mu(-1)$ | One line: liquidity trade bounds what one order can reveal |
| 10 | Show (H1)–(H3) on the face: $B_0(\pi)<c_H<B_1(M(\pi))$; $\Delta_0<k<\rho\kappa(\pi)\Delta_1$; $B_2(M(\pi))<c_H$, with $\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}$. Replace “Full orders stay” with “orders $(1,-1)$ as at $F_1$; entry $\rho$ after each order” | The three-column outcome read |
| 11 | Gains in symbols: $K_H=e(1)\Delta_T[1-\mu(1)]$, $K_L=e(-1)\Delta_T\mu(-1)$, $\rho\kappa(\pi)\Delta_T\le K_H,K_L\le\Delta_T$. The proof is then two comparisons with $k$ | The four-step proof order |
| 12 | Label it with the paper corollary for the example. State example primitives in one line ($G_H,G_L$ point masses; $F$ uniform on $[0,r]$) before numbers | The figure read |
| 13 | Label the box **Proposition (fixed-information control)** and name the fixed objects: the joint law of type and signal, $G_H,G_L$, the law of $C$. Title: **At fixed information, strength cannot raise entry** | “Freeze the news” in speech alone |
| 14 | Label the box **Proposition 4**, with scope: prior $1/2$, the equilibrium in which a purchase recruits. Mark $\lambda$ as chosen | The title intuition, with “spread” tied to $\Delta_T$ |
| 15–16 | Write impacts as $P(1)-P(0)$ and $P(0)-P(-1)$. No proposition label: the paper gives these as implications, so keep “Prediction” and “Measurement” | Measurement advice; the verbal conclusion |
| Backups | B1 keeps exact form. Cut status words from B3/B11 subtitles; keep “Proposition 3”, “Proposition 4”. Cut “either mood”, “one dial”, “more digging”, and “the price that speaks” from faces. B8 holds (E1)–(E6) and tie rules | Claim titles in words, for fast search in questions |

Title rule: model slides take object titles (Primitives, Payoffs, Equilibrium); result slides take the paper label plus a short formal claim. Long business clause titles (“Every order leaves the informed investor an edge”) should give way to that pattern.

## 5. A new notation budget

Li allows seven pieces and cuts any symbol with fewer than three uses. Exemplar model blocks run from 6 to 20 families. Seven symbols here force one phrase (“buyer profit”, “spread”) to carry $B$, $g_H$, $g_L$, and $\Delta_T$ with no mark to separate them. That cost now exceeds the memory cost.

| Tier | Symbols | Rule |
|---|---|---|
| Persistent (4 groups) | Values: $R,F$; $j\in\{H,L\},\pi,\theta$; reserve $p$. Entry: $C,c_H,\rho,e(x)$. Trading: $\lambda,q,X,P,k,\mu$. Payoffs: $\Delta_T,B(\mu)$; from Slide 9, $m(\pi),M(\pi),\tau$ | Defined on Slides 4, 6, and 9. Each on at least three faces. Gloss at first use per face; bare after that on that face |
| Local to one face | $G_j,\beta$ (Slide 4); $V_T$ (Slides 4, 7); $t_j,g_j,t_0$ (Slide 6); $K_H,K_L,\kappa$ (Slides 10–11); $F_0,F_1,F_2$ (Slide 10) | Define, use, drop. No later face presumes them |
| Backup only | $\bar r$, $D(y)$, $b=(1-\lambda)\beta$, $u=\lambda/b$, strategy functions, $W_j(F)$, example values and strengths, $\bar\lambda$, $a$ | Off main faces. Corrected B15 serves handout readers |

Trade-off, plainly: fifteen persistent families exceed Li’s cap. The deck pays with one definitions slide, a gloss per face, and figure labels that pair word and symbol (“the threshold $\tau$”, “the top belief $M$”). The gain is checkable propositions and exact objects for questions. Spoken pairs $p/P$ and $m/M$ need care: say “the reserve $p$” and “the stock price $P$” in full when both sit on one face.

## Questions for the author

1. Locked names against finance use: Kyle and Glosten–Milgrom say “informed trader” (Kyle also “noise trader”, not liquidity trader), and takeover writing says “bidder” more often than “buyer”. The drafts keep first buyer, second buyer, and informed investor. Should any locked name change, or should speech note the standard term once?
2. Should Slide 4 carry the timeline line, as drafted, or should timing keep its own slide?
3. Should (H1)–(H3) sit on the Slide 10 face, or stay on B1 alone?
4. Does the persistent tier of fifteen families stand, with glosses as the memory aid?
