# Fit and accuracy conflicts: wording pass, 9 November 2026

Status: stopped under SPEC Rev. 2, D3 Exception 1. The wording needs a ruling.
Implementer: takeover agent. Wording owner: the author, then the spec author.
No commit, no stage, no deploy until a ruling.

## 1. Why the pass stopped

The draft in the working tree (`slides.tex` SHA-256 `981a754b…`) builds.
`python3 presentation/build.py` exits 0. `latexmk slides.tex` exits 0.
But 11 of 19 main frames overflow the page. Before the pass, no main frame
overflowed by more than 0.67 pt.

| Frame | Overflow in the draft | Visible effect |
|---|---|---|
| S4 | 6.8 pt | Roadmap line runs into the footline |
| S5 | 11.1 pt | Foot sentence runs into the footline |
| S8 | 26.7 pt | Last two bullets cut |
| S9 | 1.2 pt | Last row touches the footline |
| S10 | 3.1 pt | Intuition touches the footline |
| S11 | 38.9 pt | Intuition cut |
| S13 | 48.2 pt, and the table 15.9 pt too wide | Table runs into the right column; intuition and proof foot cut |
| S14 | 64.0 pt | Last three sentences, intuition and foot cut |
| S15 | 79.6 pt | Exact-fall formula, intuition and foot cut |
| S16 | 87.1 pt | Statement cut mid-sentence; intuition and foot cut |
| S18 | 32.8 pt | Intuition and foot cut |

The prior agent already used the spacing slack on these frames
(figure scale, item spacing, `\vspace`). Spacing alone cannot close
the gaps. The Rev. 2 verbatim text for S14 and S16 is longer again.

## 2. Accuracy conflicts in the Rev. 2 final text

Each item below states a claim that the paper does not support.

1. **S16, CHECK 6.** Rev. 2: "a trader whose research succeeds and shows
   class $L$ abstains". Paper, section 5 (`sections/05_research.tex`):
   "class $L$ abstains while a sale at the entry floor cannot pay its cost,
   $\rho\Delta_T\le2k$; beyond that point it sells just often enough that its
   sale breaks even, and once even a sure sale pays, it sells for sure."
   The paper defines the recruiting equilibrium by class $H$ alone:
   "class $H$ buys after a success and a purchase recruits a high-cost rival".
   B12 shows the class-$L$ sale term $(\rho\Delta_T m_\lambda-k)_+$.
   Proposal: drop the class-$L$ clause from the definition. State the
   three-regime fact in the foot.
2. **S16, CHECK 5.** Rev. 2: "No one observes the chosen $\lambda$ or whether
   research succeeded". The trader observes both. Paper: "Market makers and
   the rival do not observe the research choice". Proposal: "Market makers
   and the rival see neither $\lambda$ nor the outcome".
3. **S15 table note.** Rev. 2: "In row 2 we force the same orders". The
   slide rules bar the first person. Proposal: "Row 2 imposes the same orders".
4. **S9 Beliefs row.** The draft states the price-belief definition twice.
   The appendix replaced one sentence but kept the one before it.
   Proposal: delete the first copy.
5. **S14, CHECK 1.** The draft restricted $u$ to $(u_{lo},u_{hi})$ before the
   equivalence. The registry gives $M_{lo}=\tau(r_1)$ and $M_{hi}=\tau(r_2)$,
   so that form made the equivalence empty. Rev. 2 fixes this with
   "Let only the mass ratio $u$, and with it $M(1/2)$, vary." The proposal
   keeps the Rev. 2 sentence.

Checked and correct: CHECK 2 (the $r_0$ legs of (H1)–(H2) do not involve $u$),
CHECK 3 (the exact-fall formula matches Proposition A.2 in
`appendix/A6_robustness.tex`), CHECK 4 ($K_H=\Delta_T m_\lambda\le\Delta_T/2$
at $e(1)=1$), CHECK 7 (the B12 first-order condition holds $a,k,\rho,\beta$;
$\tau$ enters existence only).

## 3. The proposal

The proposal keeps every condition, symbol, number, citation and title of
the appendix, with one exception: the S14 title is shortened to fit one line.
It cuts repeated words, merges sentences that say the same thing, moves one
display inline (S13, S16), and rebalances column widths on S13 and S16.
Built in a scratch copy: `latexmk` exit 0. Main-frame overflows: S5 0.15 pt
and S13 0.65 pt, the same size as before the pass.

Cuts that a reader may miss:

- S14 title: "The example works: a purchase recruits only against the strong
  incumbent" wraps to two lines. Proposed: "Example: a purchase recruits only
  against the strong incumbent".
- S14: the fractions of $\tau(r_1)$, $\tau(r_2)$ and the sentence "All three
  numbers are probabilities that the class is $H$" leave the frame. The
  decimals stay, with $=$ for the exact $\tau(r_1)$ and $\approx$ for
  $\tau(r_2)$.
- S15: the gloss "in each class, each signal keeps the same chance at both
  strengths" and the sentence "Entry may stay flat; it cannot go up" leave
  the frame. The table note keeps "Rows 2 and 3 stay flat, as 'cannot rise'
  allows".
- S16: "The cap $\bar\lambda$ is the highest success chance it can buy"
  leaves; $\lambda\in[0,\bar\lambda]$ carries it.
- S8: the caption "One draw with $p<R<\theta$" leaves; the figure already
  labels "one draw $R$".
- S11: the three added $e(x)$ sentences become one clause.

- S14, CHECK 2: Rev. 2 says the $r_0$ legs "hold at these numbers for every
  $u$ in the region". The proposal says the legs at $r_0$ "do not involve $u$".
  This is a weaker statement, not only a shorter one. It is true, and it is
  the reason the equivalence does not mention $r_0$. Choose one.
- S13: the list "the class distributions, $p$, $\pi$, $\rho$, $\lambda$,
  $\beta$, $c_H$ and $k$" becomes "all other inputs stay fixed". The
  intuition says "the top belief misses the threshold" in place of "rival
  gross profit at the top belief stays below $c_H$". By (H3) the two are the
  same, but S13 does not name $\tau$ as the preparation threshold. Choose one.

## 4. The three clauses that Rev. 2 names

| Clause | Rev. 2 final text | Proposed text |
|---|---|---|
| (a) S14 scope | "Fix $\pi=1/2$ and the other inputs below. Let only the mass ratio $u$, and with it $M(1/2)$, vary." | "Fix $\pi=1/2$ and the inputs below. Let only the mass ratio $u=\lambda/b$ of frame 11, and with it $M(1/2)$, vary; the legs of (H1)–(H2) at $r_0$ do not involve $u$." |
| (b) S16 gloss | "Why $2k$: at prior $1/2$, a recruiting purchase earns gross $\Delta_T m_\lambda$ (frame 12, with entry 1). Since $m_\lambda\le 1/2$, that gain can beat $k$ only if $\Delta_T>2k$." | "Why $2k$: a recruiting purchase gains $\Delta_T m_\lambda\le\Delta_T/2$ gross (frame 12), so it beats $k$ only if $\Delta_T>2k$." |
| (c) S16 hold-fixed | "The comparison holds $a$, $k$, $\rho$ and $\beta$ fixed (prior $1/2$ throughout): $\lambda_R$ then moves only through $\Delta_T$ in the first-order condition. The threshold $\tau$ gates existence through $\tau\le M_{\widehat\lambda}$; it does not enter that condition." | "In it, with $a$, $k$, $\rho$ and $\beta$ fixed, research $\widehat\lambda$ rises strictly with $\Delta_T$ up to $\bar\lambda$, then stays there; $\tau$ enters only the existence condition." |

## 5. Line-by-line listing

"Draft" is the working tree as the prior agent left it (`981a754b…`).
"Proposed" is the fitted text. The working tree does not yet hold the
Rev. 2 forms of clauses (a) to (c); section 4 compares those.

### S4

Draft (working tree, prior agent):

```latex
\LargeLine{A stronger incumbent weakly cuts rival gross profit at each belief about synergy. It can also widen the shareholder spread, the good-minus-poor synergy gap in target proceeds. Informed trade can then cover its cost, and the price can recruit the rival, even at the high preparation cost.}
```

Proposed:

```latex
\LargeLine{A stronger incumbent weakly cuts rival gross profit at each belief about synergy. It can also widen the shareholder spread, the good-minus-poor synergy gap in target proceeds. Informed trade can then pay, and the price can recruit the high-cost rival.}
```

### S4

Draft (working tree, prior agent):

```latex
\item \textbf{Non-monotone entry:} entry can rise from the weak to the strong incumbent, then return at the very strong incumbent to its floor, set by zero-cost preparation. Each of the three cases has a unique outcome (Proposition 2).
```

Proposed:

```latex
\item \textbf{Non-monotone entry:} entry can rise from the weak to the strong incumbent, then return to its floor, set by zero-cost preparation, at the very strong one. Each case has a unique outcome (Proposition 2).
```

### S5

Draft (working tree, prior agent):

```latex
\DefRow{Incumbent}{\textbf{incumbent bidder, already prepared:} it knows its value $R$ and faces no further preparation cost. All know the distribution $F$ of $R$, continuous on $[0,\bar r]$ with upper bound $\bar r$; no one else sees the draw $R$ before bids. \textbf{Stronger} means a distribution $\widetilde F$ that draws weakly higher values: $\widetilde F(y)\le F(y)$ for each $y$.}
```

Proposed:

```latex
\DefRow{Incumbent}{\textbf{incumbent bidder, already prepared:} it knows its value $R$ and faces no further preparation cost. All know the distribution $F$ of $R$, continuous on $[0,\bar r]$; no one else sees $R$ before bids. \textbf{Stronger} means a distribution $\widetilde F$ that draws weakly higher values: $\widetilde F(y)\le F(y)$ for each $y$.}
```

### S5

Draft (working tree, prior agent):

```latex
\DefRow{Class ranking}{$G_H(y)\le G_L(y)$ for each $y$ --- class $H$ draws weakly higher values. Also, for the reserve $p>0$ in the Sale row below, $\theta\ge p$ almost surely under each $G_j$. The sale and the rival's identity are public. The rival's synergy class is not public, and the rival does not know it before preparation.}
```

Proposed:

```latex
\DefRow{Class ranking}{$G_H(y)\le G_L(y)$ for each $y$ --- class $H$ draws weakly higher values. Also, for the reserve $p>0$ in the Sale row below, $\theta\ge p$ almost surely under each $G_j$. The sale and the rival's identity are public; the synergy class is not, and the rival does not know it before preparation.}
```

### S8

Draft (working tree, prior agent):

```latex
{\footnotesize\raggedright One draw with $p<R<\theta$.\par}
```

### S8

Draft (working tree, prior agent):

```latex
\item $\mathbb E_j$ denotes expectation under $G_j$. Class means are $t_j=\mathbb E_j[t(\theta)]$ and $g_j=\mathbb E_j[g(\theta)]$. With no prepared rival, the incumbent pays $p$ if $R\ge p$ and $0$ otherwise. Expected target proceeds are $t_0=p[1-F(p)]$, where $1-F(p)$ is the chance that $R$ meets the reserve.
```

Proposed:

```latex
\item $\mathbb E_j$ denotes expectation under $G_j$. Class means are $t_j=\mathbb E_j[t(\theta)]$ and $g_j=\mathbb E_j[g(\theta)]$. With no prepared rival, the incumbent pays $p$ if $R\ge p$ and $0$ otherwise, so expected target proceeds are $t_0=p[1-F(p)]$.
```

### S8

Draft (working tree, prior agent):

```latex
\item The informed trader who submits $q$ (so $X=q$) earns $q[V_T-P(q)]-k|q|$, where $V_T$ is realised target proceeds per share and $P(q)$ is the price set after that order.
```

Proposed:

```latex
\item The informed trader who submits $q$ (so $X=q$) earns $q[V_T-P(q)]-k|q|$, with $V_T$ realised target proceeds per share.
```

### S9

Draft (working tree, prior agent):

```latex
\DefRow{Beliefs}{the order belief $\mu(x)=\Pr(j=H\mid X=x)$ follows Bayes' rule. The rival's price belief $\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)$ pools all outcomes with that price. The rival's price belief $\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)$ averages over all outcomes $x$ with $P(x)=\bar P$; it need not equal $\mu(x)$ for one such outcome. Liquidity trade gives each outcome positive probability in each class, so Bayes' rule pins down order beliefs.}
```

Proposed:

```latex
\DefRow{Beliefs}{the order belief $\mu(x)=\Pr(j=H\mid X=x)$ follows Bayes' rule. The rival's price belief $\bar\mu(\bar P)=\Pr(j=H\mid P(X)=\bar P)$ averages over all outcomes $x$ with $P(x)=\bar P$; it need not equal $\mu(x)$ for one such outcome. Liquidity trade gives each outcome positive probability in each class, so Bayes' rule pins down order beliefs.}
```

### S10

Draft (working tree, prior agent):

```latex
\Gloss{Good-synergy values weakly dominate in the first-order sense. Both classes meet the reserve almost surely.}
```

Proposed:

```latex
\Gloss{Good-synergy values weakly dominate in the first-order sense.}
```

### S11

Draft (working tree, prior agent):

```latex
M(\pi)=\dfrac{\pi(1+u)}{\pi(1+u)+1-\pi}.$ Here $b=(1-\lambda)\beta$ is the total liquidity mass for one order direction.\par
```

Proposed:

```latex
M(\pi)=\dfrac{\pi(1+u)}{\pi(1+u)+1-\pi}.$\par
\Gloss{Here $b$ is the liquidity mass on one order direction, and $u$ is the mass ratio.}
```

### S11

Draft (working tree, prior agent):

```latex
\Gloss{With $\beta\le1/3$, liquidity trade covers every outcome, including no trade.}
```

Proposed:

```latex
\Gloss{With $\beta\le1/3$, liquidity trade covers all three outcomes.}
```

### S11

Draft (working tree, prior agent):

```latex
\textbf{Preparation rule.} Define the preparation threshold $\tau=(c_H-g_L)/(g_H-g_L)$.
\Gloss{$B(\mu)\ge c_H\iff\mu\ge\tau$.}
Write $e(x)$ for the entry probability after order $x$. Then $e(x)\in[\rho,1]$, where $\rho$ is the entry floor. Because the price reveals $\mu(x)$, the default preparation rule can be written with $\mu(x)$.
Under the default preparation rule,
\Gloss{A rival at the threshold prepares.}
```

Proposed:

```latex
\textbf{Preparation rule.} Define the preparation threshold $\tau=(c_H-g_L)/(g_H-g_L)$, so $B(\mu)\ge c_H\iff\mu\ge\tau$. The price reveals $\mu(x)$, so under the default rule (a rival at the threshold prepares), entry $e(x)$ after order $x$ is
```

### S13

Draft (working tree, prior agent):

```latex
Classes have finite means and satisfy $G_H\le G_L$, $G_H(p^-)=G_L(p^-)=0$. Steps $F_0$ (weak), $F_1$ (strong) and $F_2$ (very strong) satisfy $F_2\le F_1\le F_0$. The three economies share the class distributions, $p$, $\pi$, $\rho$, $\lambda$, $\beta$, $c_H$ and $k$. Only $F$ steps. Here $\beta\in(0,1/2)$, because only the nonzero-order bounds at $x=\pm1$ are needed.
```

Proposed:

```latex
Classes have finite means and satisfy $G_H\le G_L$, $G_H(p^-)=G_L(p^-)=0$. Steps $F_0$ (weak), $F_1$ (strong) and $F_2$ (very strong) satisfy $F_2\le F_1\le F_0$; only $F$ steps, and all other inputs stay fixed. Here $\beta\in(0,1/2)$ suffices: only the bounds at $x=\pm1$ are needed.
```

### S13

Draft (working tree, prior agent):

```latex
\begin{minipage}[t]{0.42\linewidth}
```

Proposed:

```latex
\begin{minipage}[t]{0.31\linewidth}
```

### S13

Draft (working tree, prior agent):

```latex
\begin{minipage}[t]{0.55\linewidth}
```

Proposed:

```latex
\begin{minipage}[t]{0.67\linewidth}
```

### S13

Draft (working tree, prior agent):

```latex
\Gloss{(H1) Rival gross profit at the prior falls below $c_H$ at $F_0$, but exceeds $c_H$ at the top belief under $F_1$.}
\Gloss{(H2) Order cost $k$ sits above the gross-gain cap at $F_0$ and below the gross-gain floor at $F_1$.}
\Gloss{(H3) At $F_2$, rival gross profit even at the top belief stays below $c_H$.}
```

Proposed:

```latex
\Gloss{(H1) Rival gross profit: below $c_H$ at the prior ($F_0$), above it at the top belief ($F_1$).}
\Gloss{(H2) Order cost $k$ is above the gross-gain cap at $F_0$, below the gross-gain floor at $F_1$.}
\Gloss{(H3) At $F_2$, rival gross profit stays below $c_H$ even at the top belief.}
```

### S13

Draft (working tree, prior agent):

```latex
\vspace{0.3em}
Then the table gives the outcome in each economy. Beliefs and entry are listed by order outcome $x=-1,0,1$.\par
\begin{minipage}[t]{0.55\linewidth}
```

Proposed:

```latex
\vspace{0.15em}
Then orders by class $(H,L)$, and beliefs and entry by order outcome $x=-1,0,1$, are:\par
\begin{minipage}[t]{0.50\linewidth}
```

### S13

Draft (working tree, prior agent):

```latex
Orders by synergy class & Beliefs by order outcome & Entry by order outcome\\
```

Proposed:

```latex
Orders & Beliefs & Entry\\
```

### S13

Draft (working tree, prior agent):

```latex
\begin{minipage}[t]{0.42\linewidth}
```

Proposed:

```latex
\begin{minipage}[t]{0.48\linewidth}
```

### S13

Draft (working tree, prior agent):

```latex
Let $\mathsf E_i$ denote total entry at $F_i$.
Then
\[
\mathsf E_0=\mathsf E_2=\rho
<\mathsf E_1=\rho+(1-\rho)(b+\pi\lambda).
\]
At $F_1$, $b+\pi\lambda$ is the probability of a purchase order, $X=1$.
The outcome is unique in each of the three economies. Uniqueness holds under every tie rule at $\mu=\tau$ and at $K_j=k$.
```

Proposed:

```latex
Total entry $\mathsf E_i$ at $F_i$ is $\mathsf E_0=\mathsf E_2=\rho<\mathsf E_1=\rho+(1-\rho)(b+\pi\lambda)$, where $b+\pi\lambda=\Pr(X=1)$ at $F_1$.
The outcome in each economy is unique under every tie rule at $\mu=\tau$ and at $K_j=k$.
```

### S13

Draft (working tree, prior agent):

```latex
\Intuition{A wider shareholder spread pays the informed trader to trade. A purchase then recruits the high-cost rival. At $F_2$, trade stays, but rival gross profit at the top belief stays below $c_H$.}
\FootLine{Proof idea: Proposition 1 with (H2) gives $K_j<k$ at $F_0$ and $K_j>k$ at $F_1,F_2$. Full trade and the frame 11--12 bounds then give the beliefs in the table. (H1) and (H3) set purchase entry through $B_i(M(\pi))$ against $c_H$. Steps: \hyperlink{app:b2}{B2}. Example and open set of inputs: frame 14. Exact form: \hyperlink{app:b1}{B1}.}
```

Proposed:

```latex
\Intuition{A wider shareholder spread pays for informed trade, and a purchase recruits; at $F_2$, the top belief misses the threshold.}
\FootLine{Proof idea: (H2) with Proposition 1 gives $K_j<k$ at $F_0$ and $K_j>k$ at $F_1,F_2$; the frame 11--12 bounds then give the beliefs, and (H1), (H3) compare $B_i(M(\pi))$ with $c_H$. Steps: \hyperlink{app:b2}{B2}. Example: frame 14. Exact form: \hyperlink{app:b1}{B1}.}
```

### S14

Draft (working tree, prior agent):

```latex
\begin{frame}[t,label=S14]{The example works: a purchase recruits only against the strong incumbent}
```

Proposed:

```latex
\begin{frame}[t,label=S14]{Example: a purchase recruits only against the strong incumbent}
```

### S14

Draft (working tree, prior agent):

```latex
The incumbent has $R\sim\mathrm{Unif}[0,r]$. A larger $r$ shifts $R$ up in first-order stochastic dominance, so $r_0,r_1,r_2$ play the roles of $F_0,F_1,F_2$ on frame 13. The three strengths are $(r_0,r_1,r_2)=(\reg{prim_r0},\reg{prim_r1},\reg{prim_r2})$.
Here $\tau(r)$ is the frame 11 preparation threshold at strength $r$: the belief in class $H$ where rival gross profit equals $c_H$. Fix $\pi=1/2$ and the other inputs below. In this equivalence only the mass ratio $u$, and with it $M(1/2)$, varies, with $u\in(\reg{u_lo},\reg{u_hi})$ (equivalently $M(1/2)\in(\reg{M_lo},\reg{M_hi})$ in B10); the other inputs below stay fixed. Then
```

Proposed:

```latex
The incumbent has $R\sim\mathrm{Unif}[0,r]$, and a larger $r$ is a stronger incumbent: $(r_0,r_1,r_2)=(\reg{prim_r0},\reg{prim_r1},\reg{prim_r2})$ play the roles of $F_0,F_1,F_2$ on frame 13.
Write $\tau(r)$ for the frame 11 preparation threshold at strength $r$. Fix $\pi=1/2$ and the inputs below. Let only the mass ratio $u=\lambda/b$ of frame 11, and with it $M(1/2)$, vary; the legs of (H1)--(H2) at $r_0$ do not involve $u$. Then
```

### S14

Draft (working tree, prior agent):

```latex
with $\tau(r_1)=\reg{tau_r1}$ and $\tau(r_2)\approx\reg{tau_r2}$ (fractions $\reg{tau_r1_frac}$ and $\reg{tau_r2_frac}$). All three numbers are probabilities that the class is $H$. Both inequalities are strict, so small input changes keep them (B10). Recall the mass ratio $u=\lambda/b$, $b=(1-\lambda)\beta$, from frame 11. The example sets $u=\mathrm e-1$, so the belief after a purchase under full orders is $M(1/2)=\mathrm e/(1+\mathrm e)\simeq\reg{M_half_B}$, and $\tau(r_1)<M(1/2)<\tau(r_2)$ holds. Hence (H1)--(H3) hold at these numbers, and Proposition 2 applies: entry is $\rho$, then above $\rho$, then $\rho$ again. The weak strength $r_0$ does not appear above: its two legs of (H1)--(H2) hold at these numbers for every $u$ in the region.
```

Proposed:

```latex
with $\tau(r_1)=\reg{tau_r1}$ and $\tau(r_2)\approx\reg{tau_r2}$. Both inequalities are strict, so small input changes keep them (B10). The example sets $u=\mathrm e-1$, so the top belief after a purchase is $M(1/2)=\mathrm e/(1+\mathrm e)\simeq\reg{M_half_B}$. Hence (H1)--(H3) hold, and by Proposition 2 entry is $\rho$, then above $\rho$, then $\rho$ again.
```

### S15

Draft (working tree, prior agent):

```latex
Let $S$ be any signal the rival sees before it prepares; in the main model, read $S$ as the news in the stock price. Hold fixed the joint distribution of $(j,S)$: in each class, each signal keeps the same chance at both strengths. Also hold fixed the class value distributions $G_j$, the reserve $p$, and the preparation-cost distribution. Only the incumbent's value distribution moves, from $F_0$ to $F_1$. In economy $i$, given $(j,S)$, the rival's value $\theta$ still has distribution $G_j$ and the incumbent's value $R$ has distribution $F_i$, and the two are independent: within a class, $S$ carries no extra news about either value. The preparation cost $C$ is independent of the class, of $\theta$ and $R$, and of $S$.
\Gloss{In words: values, reserve, costs, and what the rival can learn all stay fixed. Only strength moves.}
An indifferent rival prepares. Take any two strengths with $F_1\le F_0$ at every value, so economy 1 has the stronger incumbent. Then entry cannot rise:
```

Proposed:

```latex
Let $S$ be any signal the rival sees before it prepares; in the main model, $S$ is the news in the stock price. Hold fixed the joint distribution of $(j,S)$, the class value distributions $G_j$, the reserve $p$ and the preparation-cost distribution; only the incumbent's distribution moves, from $F_0$ to $F_1$. In economy $i$, given $(j,S)$, the values $\theta\sim G_j$ and $R\sim F_i$ are independent, and $C$ is independent of $j$, $\theta$, $R$ and $S$.
\Gloss{What the rival can learn stays fixed. Only strength moves.}
Let an indifferent rival prepare, and let $F_1\le F_0$ (economy 1 has the stronger incumbent). Then entry cannot rise:
```

### S15

Draft (working tree, prior agent):

```latex
where $\mathsf E_i$ is total entry in economy $i$, the total probability that the rival prepares. Entry may stay flat; it cannot go up. Write $\mu(S)=\Pr(j=H\mid S)$ for the belief the signal leaves, and $B_i$ for rival gross profit at $F_i$. The fall is exact: $\mathsf E_0-\mathsf E_1=\Pr\{B_1(\mu(S))<C\le B_0(\mu(S))\}$, the chance that the cost $C$ sits between rival gross profit at the two strengths, at the unchanged belief.
```

Proposed:

```latex
where $\mathsf E_i$ is total entry in economy $i$. The fall is exact: with $\mu(S)=\Pr(j=H\mid S)$ and $B_i$ rival gross profit at $F_i$, $\mathsf E_0-\mathsf E_1=\Pr\{B_1(\mu(S))<C\le B_0(\mu(S))\}$.
```

### S15

Draft (working tree, prior agent):

```latex
{\footnotesize\raggedright In row 1 the orders change with strength, from $(0,0)$ to $(1,-1)$, so the distribution of $(j,S)$ changes and the hypothesis above fails. In row 2 we force the same orders at both strengths; the rival still reads the price. At the weak strength those orders lose money, so row 2 is a control, not an equilibrium. Rows 2 and 3 are flat: flat is what `cannot rise' allows.\par}
```

Proposed:

```latex
{\footnotesize\raggedright In row 1 the orders change with strength, so the distribution of $(j,S)$ changes. Row 2 imposes the same orders at both strengths; at the weak strength they lose money, so row 2 is a control, not an equilibrium. Rows 2 and 3 stay flat, as `cannot rise' allows.\par}
```

### S15

Draft (working tree, prior agent):

```latex
\Intuition{This is Proposition 1(a) belief by belief: at each unchanged belief the stronger incumbent gives weakly lower rival gross profit, so strength can only remove reasons to prepare, never add one.}
```

Proposed:

```latex
\Intuition{At each unchanged belief, strength weakly lowers rival gross profit (Proposition 1(a)): it only removes reasons to prepare.}
```

### S16

Draft (working tree, prior agent):

```latex
\noindent One change from frame 6. The informed trader now chooses its research level $\lambda\in[0,\bar\lambda]$ before the slot, at cost $(a/2)\lambda^2$, with $a>0$ and $0<\bar\lambda<1$. Research is all-or-nothing: with probability $\lambda$ it succeeds, the trader learns the synergy class in full, and it fills the slot. With probability $1-\lambda$ it fails, the trader learns nothing, and liquidity fills the slot instead. The cap $\bar\lambda$ is the highest success chance it can buy. No one observes the chosen $\lambda$ or whether research succeeded; market makers and the rival set prices and preparation at the equilibrium level $\widehat\lambda$ below.\par\vspace{-0.5em}
```

Proposed:

```latex
\noindent One change from frame 6: before the slot, the informed trader chooses research $\lambda\in[0,\bar\lambda]$ at cost $(a/2)\lambda^2$, with $a>0$ and $0<\bar\lambda<1$. Research is all-or-nothing: with probability $\lambda$ the trader learns the synergy class and fills the slot; otherwise liquidity fills it. Market makers and the rival see neither $\lambda$ nor the outcome; they use the equilibrium $\widehat\lambda$.\par\vspace{-0.5em}
```

### S16

Draft (working tree, prior agent):

```latex
\begin{minipage}[t]{0.46\linewidth}\raggedright
Assume the class ranking of frames 10 and 13, prior $\pi=1/2$, spread $\Delta_T>0$, rival profit gap $g_H>g_L$, liquidity chance $\beta\le1/3$ as on frame 6, and threshold $\tau>1/2$.
```

Proposed:

```latex
\begin{minipage}[t]{0.48\linewidth}\raggedright
Assume the class ranking, prior $\pi=1/2$, $\Delta_T>0$, $g_H>g_L$, $\beta\le1/3$ and threshold $\tau>1/2$.
```

### S16

Draft (working tree, prior agent):

```latex
At research $\lambda$, write $M_\lambda$ for the top belief after a purchase; at prior $1/2$ the band floor is $m_\lambda=1-M_\lambda$.
For $\Delta_T>2k$, let $\lambda_R(\Delta_T)\in(0,1)$ be the unique research level where marginal cost $a\lambda$ meets the marginal gain from a higher success chance; \hyperlink{app:b12}{B12} gives the first-order condition. Equilibrium research is that level, cut off at the cap: $\widehat\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}$.
\Gloss{The threshold is $2k$, not $k$: at prior $1/2$ the frame 12 gross gain after a recruiting purchase is $\Delta_T m_\lambda$, and the band floor $m_\lambda$ is at most $1/2$, so the gain beats the order cost $k$ only if $\Delta_T>2k$ (B12).}
```

Proposed:

```latex
At research $\lambda$, write $M_\lambda$ for the top belief after a purchase and $m_\lambda=1-M_\lambda$ for the band floor.
For $\Delta_T>2k$, let $\lambda_R(\Delta_T)\in(0,1)$ be the unique level where marginal cost $a\lambda$ equals the expected trading payoff after a success (\hyperlink{app:b12}{B12}). Equilibrium research is $\widehat\lambda=\min\{\lambda_R(\Delta_T),\bar\lambda\}$.
```

### S16

Draft (working tree, prior agent):

```latex
\begin{minipage}[t]{0.51\linewidth}\raggedright
The recruiting equilibrium, in which a trader whose research succeeds and shows class $H$ buys, a trader whose research succeeds and shows class $L$ abstains, and a purchase is the only order that brings in the high-cost rival, exists exactly when
```

Proposed:

```latex
\begin{minipage}[t]{0.49\linewidth}\raggedright
The recruiting equilibrium, in which a trader whose research shows class $H$ buys and a purchase recruits the high-cost rival, exists exactly when
```

### S16

Draft (working tree, prior agent):

```latex
\Gloss{The spread pays for trade, and a purchase clears $\tau$.}
In this equilibrium, research $\widehat\lambda$ rises strictly as $\Delta_T$ widens, until it reaches $\bar\lambda$; past that point it stays at $\bar\lambda$. This rise holds with $a$, $k$, $\rho$ and $\beta$ fixed, so $\lambda_R$ moves with $\Delta_T$ alone through the first-order condition in B12; $\tau$ enters only the existence condition $\tau\le M_{\widehat\lambda}$ above. Total entry is, with the $1/2$ from the prior,
\[
\mathsf E=\rho+(1-\rho)[\beta+(1/2-\beta)\widehat\lambda].
\]
Where research does rise, $\mathsf E$ and entry in class $H$ rise strictly with it, while entry in class $L$ falls strictly.
```

Proposed:

```latex
\Gloss{Why $2k$: a recruiting purchase gains $\Delta_T m_\lambda\le\Delta_T/2$ gross (frame 12), so it beats $k$ only if $\Delta_T>2k$.}
In it, with $a$, $k$, $\rho$ and $\beta$ fixed, research $\widehat\lambda$ rises strictly with $\Delta_T$ up to $\bar\lambda$, then stays there; $\tau$ enters only the existence condition. Total entry is $\mathsf E=\rho+(1-\rho)[\beta+(1/2-\beta)\widehat\lambda]$.
Where research rises, $\mathsf E$ and class-$H$ entry rise strictly; class-$L$ entry falls strictly.
```

### S16

Draft (working tree, prior agent):

```latex
\Intuition{A wider shareholder spread raises the payoff to a successful look at the class, so the trader buys a higher success chance until the cap binds. More success sorts entry toward good synergy.}
\FootLine{First-order condition, branches, class entry formulas, and the research figure: \hyperlink{app:b12}{B12}. When $\lambda$ stays exogenous as on frame 6, informative and uninformative markets can coexist: \hyperlink{app:b3}{B3}.}
```

Proposed:

```latex
\Intuition{A wider shareholder spread pays for more research, up to the cap; more research sorts entry toward good synergy.}
\FootLine{After a class-$L$ success: abstain while $\rho\Delta_T\le2k$, else sell with positive probability. Details: \hyperlink{app:b12}{B12}. Exogenous $\lambda$: \hyperlink{app:b3}{B3}.}
```

### S18

Draft (working tree, prior agent):

```latex
\Gloss{At the prior $\pi$, rival gross profit falls short of $c_H$; $\tau$ is the threshold belief, and $g_H>g_L$ orders class gross profits.}
Write $P(1)$, $P(0)$ and $P(-1)$ for the prices after a purchase, no order, and a sale order. Write $e(1)$ for entry after a purchase and $\rho$ for the entry floor; $e(1)>\rho$ is recruitment. Here $b$ is the liquidity mass in one direction and $\lambda$ is informed presence.
```

Proposed:

```latex
\Gloss{At the prior $\pi$, rival gross profit falls short of $c_H$.}
$P(x)$ is the price after order $x$, and $e(1)>\rho$ means that a purchase recruits.
```

## 6. Resolution, 9 November 2026

The author moved the pass forward on the proposal, with two instructions:
redraw the frame 14 figure, and run one more style pass with Fable.
The shipped text is the proposal of sections 3 and 4, plus the changes below.
Section 5 lists the proposal before these changes.

**Frame 14 figure.** The crop of `beliefs_talk.pdf` panel (b) scaled a
7.4-inch figure into a 4.7 cm column, so the band label ran across the curve
and the axis. A new figure, `figures/band_talk.pdf`, is drawn at the column
width on white paper by `make_band_talk.py` (beside `make_figures.py`). The
band label is three short lines in the free corner above the curve. The
printed values stay `\reg` overlays. The web figure (`presentation/deck.js`)
puts the band label in the same corner.

**Fable style pass.** 15 edits, all the same length or shorter. All were
applied, with one change: on S16 "nor the outcome" becomes "nor the result",
not "nor its success", because "its" has an unclear antecedent. Two of Fable's
open points were also applied: S16 says "preparation threshold $\tau>1/2$",
and its foot is a full sentence ("After a class-$L$ success, the trader
abstains while $\rho\Delta_T\le2k$ and otherwise sells with positive
probability."). The edit list is in the session scratch area, not in the repo.

**Web fit.** `DECK.audit()` flagged S5 (32 px) and S16 (6 px). Two cuts:
- S5 foot: "The pair $(j,\theta)$ is independent of $R$, $C$ and the
  trading-slot draws. Neither bidder trades target shares. Frame 6 adds the
  slot." The list "informed trader, liquidity trader, competitive market
  makers" leaves; frame 6 states it.
- S16: "a purchase recruits the high-cost rival" becomes "a purchase
  recruits". The deck header defines "recruits" as high-cost entry past
  the floor.

**Checks at the end.** `presentation/build.py` from an empty `dist/`: exit 0;
57 frames match `slides.tex` and `slides_script.md`. `latexmk slides.tex`:
exit 0; one main-frame overflow, 0.65 pt on S13 (before the pass: 0.67 pt on
S16). In the browser: `DECK.selfCheck()` reports no errors and no math
errors; `DECK.audit()` returns `[]`.
