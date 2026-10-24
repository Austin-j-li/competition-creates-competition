# Synthesis: an EGJ-like microstructure for the paper

Memo to the author, 22 October 2026. Workstream S. This study is exploratory. It edits no file of the paper.

## 0. Sources, conventions and spot-checks

**Sources.** The nine memos in this folder (`L1_survey`, `L2_taxonomy`, `T1`–`T6`, `X_check`) and the coordinator notes in `LEDGER.md`. Every number below comes from one of these memos or from my spot-check script `scripts/SYNTHESIS/spot_check.py` (output `spot_check.out.txt`, receipt `run_receipt.json`). The paper is read at `overleaf/paper` commit `01bd5d6`.

**Benchmark.** $h=10$, $\ell=1$, $p=1/2$, $\rho=1/4$, $c_L=0$, $c_H=6$, $k=1/50$, $\pi=1/2$; strengths $r_0=1.2$, $r_1=3$, $r_2=3.6$. Paper values: entry $0.522757$ at $r_1$; ceiling $r_C=3.592659$; no-trade boundary $r_N=1.747878$; Prop. 3 entry $0.545<0.549<0.551$ at $1.55,1.60,1.65$.

**Labels.** Each result carries one label: analytical, computer-assisted, numerical diagnostic, conjecture, open.

**Tie rules.** The memos use two names for each rule. I use these:

- investor rule M: a tied class may mix (T2, T4, T5 write IM);
- investor rule Z: a tied class does not trade (EGJ's rule; I0);
- challenger rule E: a tied high-cost type prepares (the paper's rule; C1);
- challenger rule X: a tied high-cost type may mix (CM).

**Symbols.** $\tau(r)$ is the posterior at which the high-cost challenger is indifferent. $M$ is the top posterior of class $H$ under full orders. In slot models, $b=(1-\lambda)\beta$ and $u=\lambda/b$, so $M=(1+u)/(2+u)$.

**Spot-checks (one line each).**

- **T6 trade-off: confirmed (analytical claims; my grids are exact at grid points).** The cap is $M\le\tau(3.6)=4245/5804=0.7314$, so $\lambda\le1343/2902=0.4628$. An upward branch of T1's kind needs $M>7309/9680=0.7551$ at $1.55$. On 10,800 exact grid points the purchase payoff never falls to the indifference level.
- **T4/T2 equivalence: confirmed (exact).** With $a=b/(b+\lambda)$ the purchase returns of T4's D1 and T2's V3 are identical (240 exact comparisons, largest difference $0$); $M$ and every payoff threshold coincide; entry above the floor differs by the exact factor $1/(b+\lambda)$.

Details of the spot-checks (`spot_check.out.txt`):

| Item | Value | Memo value |
|---|---|---|
| $\tau(3)$, $\tau(3.6)$, band width | $141/200$, $4245/5804$, $7659/290200=0.0264$ | X §3.9 |
| Margin that forces full purchases at $3.6$: $\rho\Delta_T(1-\tau)-k$ | $899467/20894400=0.0430$ | T6 Result 2 |
| Cap on $\lambda$ at $\beta=1/2$ | $1343/2902=0.462784$ | T6 Result 2 |
| $M$ that a $\{1,2\}$ branch needs at $1.55$ ($\theta=1/3$; $\theta=1/10$) | $0.755062$; $0.786157$ | T6 Result 4: $0.755$; $0.786$ |
| Same at $1.65$ ($\theta=1/10$) | $0.840319$ | T6: $0.840$ |
| Under the cap, such a branch needs $r<$ | $1.525828$ | T6: $1.525828$ |
| Grid, $\theta\le1/3$, $M\le\tau(3.6)$: least purchase payoff when flows $1$ and $2$ recruit, per $\Delta_T$ | $0.2904>\kappa(1.55)=0.2050$ | T6 bound $0.2207$ |
| Grid: largest purchase payoff with flow $\{2\}$ only, per $\Delta_T$ | $0.1998<0.2050$ | T6 Result 4(b) |
| Grid (145,200 points): least sale payoff at $r=3$, per $\Delta_T$ | $0.0691>\kappa(3)=0.03$ | T6 bound $0.0448$ |
| T4/T2 at $\lambda=6/17$, $\beta=1/3$ | $a=11/29$; entry $37/68$ (V3) and $89/116$ (D1); ratio $51/29=1/(b+\lambda)$ | T4 §5 |

The grids add one fact that T6's proof does not state: the least payoff on the grid ($0.290$) lies well above T6's analytical bound ($0.221$). So the bound has slack, and the conclusion holds with a margin on the grid.

## 1. What the literature uses

### 1.1 Model classes, with counts

L1 counts 15 corporate-decision models whose model sections it read or found in verified records (C01–C15). The sample is purposive. The counts describe this sample, not the whole literature (L1 §3).

| Class | Count | Models (L1 id) | How conventional in this literature |
|---|---:|---|---|
| Kyle-type: strategic trader, normal or Brownian noise | 3 | Holmström–Tirole 1993 (C10); Edmans–Manso 2011 (C12); Back et al. 2018 (C14) | Conventional; the default family |
| Noisy rational expectations, normal shock | 3 | Bond–Goldstein 2015 (C07); Goldstein–Ozdenoren–Yuan 2013 (C08); Ozdenoren–Yuan 2008 (C15) | Conventional |
| Discrete three-point (EGJ/GG) | 2 | EGJ 2015 (C01); Goldstein–Guembel 2008 (C02) | Established, but a minority; the closest discrete template |
| One-order arrival | 1 | Dow–Gorton 1997 (C09) | Established, a minority |
| One-sided exponential | 1 | Edmans 2009 (C04) | One use, with a stated tractability reason |
| General full-support density | 1 | Boleslavsky–Kelly–Taylor 2017 manuscript (C05) | One use |
| Uniform noise | 0 | none in the selected versions | Not used |
| Other | 4 | DGG 2017 (C03, normal flow; speculators take prices as given); Bond–Goldstein–Prescott 2010 (C06, price-only); Admati–Pfleiderer 2009 (C11, binary exit); Faure-Grimaud–Gromb 2004 (C13, unordered discrete orders) | Each one of a kind |
| Laplace | 0 | one numerical preprint outside corporate finance (L2 §4) | Unconventional, as the author says |

Four readings follow.

- Normal shocks appear in 7 of the 15 models, through different mechanisms (L1 §3). Normal noise is the default.
- Five of the 15 models are discrete in a broad sense: EGJ, GG, Dow–Gorton, Admati–Pfleiderer, Faure-Grimaud–Gromb (L1 §3). Only EGJ and GG use additive three-point noise.
- L2's interpretation, not an L1 count: some form of a same-size liquidity order appears in 4 of the 15 models (Dow–Gorton, BKT, Admati–Pfleiderer, Faure-Grimaud–Gromb). Only Dow–Gorton is a pure exclusive arrival (L2 §4).
- Neither survey ranks a noise law. Goldstein (2023, p. 13) writes that "feedback-effect models often rely on specifications that are different from the usual ones" (L1 S02). That supports a tractable specification. It does not support one law over another.

### 1.2 The closest references

L1 §6 names five: EGJ (2015), Goldstein–Guembel (2008), Dow–Gorton (1997), Admati–Pfleiderer (2009) and Faure-Grimaud–Gromb (2004). Dow, Goldstein and Guembel (2017) stays essential for information production and for the limits of price observation.

### 1.3 Devices that hide the informed trader's motive

| Device | Verified source | What it hides | What it does not hide |
|---|---|---|---|
| Presence or a liquidity shock that stops trade ($\lambda<1$) | EGJ p. 3787, via the Q2 record R1–R2 (L1 §5.1): "$\lambda<1$ is necessary for the speculator not to be fully revealed when $X=\{-1,1\}$" | The interior flows $\pm1$ | The outer flows $\pm2$ |
| A same-size uninformed speculator | GG pp. 137, 141–142, via record A2 (L1 §5.2) | Sales: flows $-2,-1$ pool the low and the uninformed type | Flow $+2$ still reveals the high state; the uninformed type trades by choice over two dates |
| Informed or liquidity arrival, same size | Dow–Gorton pp. 1095, 1124–1125 (L1 C09, §5.3): information arrival is "perfectly negatively correlated with the arrival of a liquidity trader" | Every order: a buy or a sale can come from either identity | It needs an exogenous liquidity motive |
| A liquidity shock that forces the same trade | Admati–Pfleiderer, July 2007 manuscript p. 7 (L1 C11, §5.4): "independent of her private information, L will need to sell her entire stake" | The exit; its footnote 9 puts exit on path | Published-version equivalence is unverified; the decision comes before trade |
| Informed or noise identity | BKT 2017 manuscript, record A7 | The identity | Orders and densities are continuous |
| Separate orders without identities | Faure-Grimaud–Gromb pp. 990–993 (L1 C13) | Mixed pairs pool identities | Identical pairs reveal; footnote 4: a separating equilibrium fails under aggregate flow |
| Full-support noise | Normal (C10, C12, C14); exponential (Edmans 2009, A6); general densities (BKT) | Every flow is interior | Not finite |

Not verified as corporate devices: random order size, wider bounded noise, and unequal EGJ weights (L1 §5.6). The model sections of Glosten–Milgrom (1985) and of the PIN model (Easley et al. 1996) are unverified; L1 holds abstracts only.

## 2. The obstacle

### 2.1 Bounded noise reveals the top flow

- Suppose additive noise has a largest value $z_{hi}$. Then the flow $1+z_{hi}$ comes only from an informed purchase, and its posterior is $1$ (T3 Result 1(b); L2 G7).
- Presence does not help. An absent investor adds only flows up to $z_{hi}$ (L2 G7). EGJ's own remark covers the flows $\pm1$, not $\pm2$ (§1.3).
- At $r_2=3.6$, $g_H=5879/720\approx8.165>c_H=6$. A challenger who is sure of class $H$ prepares. So informative trade at $3.6$ gives entry at least $\rho+(1-\rho)\pi\alpha f(z_{hi})>\rho$ (T3 Result 2; analytical).
- The two-sided form: for every $\lambda$, every symmetric weight $\theta$ and every $k<0.0315$, each equilibrium at $3.6$ has entry above $\rho$ (T1 Result 6; analytical). Entry $\rho$ would need no purchase at all. But a purchase then earns at least $\tfrac12\rho\Delta_T(1-\tau)-k>0$.
- The best weaker statement: for $\lambda\in[0.582,0.633)$, entry falls from $1/2$ at $r_1$ to $1/4+\lambda/8\approx0.33$ at $r_2$ (T1 Result 7; analytical). Entry returns to $\rho$ only above $r_C(1)=7.969$.
- The smallest repairs are documented failures under BRIEF §2: $c_H\in(8.165,8.458]$, which is above $81\%$ of $h$; or $h\in[7.54,7.83)$; or $r_2>7.969$ (T1 Result 8; T3 Result 2; analytical).

EGJ's presence device still does real work. Under full orders the flow $+1$ has posterior $1/(2-\lambda)$, so it recruits and pays the buyer a residual (T1 Result 2). Feedback survives. The return to the floor does not.

### 2.2 The device that removes the obstacle

Fill the informed trader's order slot, when it is not informed, with a liquidity order of the same size.

- Class $L$ then reaches every flow that class $H$ reaches, through the liquidity order. Every flow is on path, and every posterior is interior, uniformly over all informed strategies (T2 §3.1; X claim 1; analytical).
- The top posterior under full orders is $M=(b+\lambda)/(2b+\lambda)<1$ (T2 eq. 17).
- The device survives EGJ's noise on top. A liquidity buy plus a noise buy reaches flow $2$ in class $L$ too (T2 eq. 6). L2 corrected its edge lemma for this case (L2 §5.2).
- Precedent: Dow–Gorton (1997) uses this device in a corporate model, with a liquidity trader that always trades (verified). Admati–Pfleiderer and GG are close relatives; BKT is the identity form (§1.3).
- A cost: the liquidity motive must be exogenous. An uninformed trader with only the paper's one-date trade payoff prefers zero in every equilibrium found (T2 §3.7; X claim 6; analytical). With $\beta=0$ the top flow reveals again.

### 2.3 A second escape, less EGJ-like

Noise that is unbounded in the direction of the order also works. One-sided geometric noise (T4 D1) or Edmans's exponential noise (T4 D2) with buy-only orders keeps every flow that recruits interior (L2 Refinement 2; T4; analytical). After a parameter match, the buyer's problem is identical to the slot's (spot-check B). This route drops EGJ's bounded noise and informed sales, so it is not the EGJ-like route.

**Correction to BRIEF §3.** "With any noise of bounded support, the top flow can come only from an informed purchase" holds only when the other class cannot place the same order and the bound lies in the order's direction. It fails with a same-size liquidity order (T2, T5, T6) and with noise bounded only on the opposite side (T4) (L2 G7; analytical).

## 3. The candidates

Abbreviations: an. = analytical; c.-a. = computer-assisted; n.d. = numerical diagnostic; NT = no trade; EGJ belief = belief "informed" at an unused extreme flow.

| Candidate | Prop. 2(i) | Prop. 2(ii); entry at $r=3$ | Prop. 2(iii) | Coexistence interval | Entry rises at 1.55–1.65? | Prop. A.9 | Off-path beliefs | Tie rules needed | Region that works | Precedent | Checked |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Paper (Laplace, $q\in[-1,1]$; reference) | yes | yes; $0.523$, pattern $(1,-v)$ | yes; $r_C=3.593$ | contains 1.55–1.65 | yes: $0.545<0.549<0.551$, pure, partial sales (c.-a.) | yes | none | none | $b$ puts $M$ $0.0003$ below the top of the band | Laplace: none | — |
| T1, EGJ's block, equal weights, presence $\lambda$ | yes, every $\lambda$ (an.) | yes, T unique; $1/2$ if $\lambda\ge0.582$, else $1/4+\lambda/8$ (an.) | **no**, every $\lambda,\theta$; best $\approx0.33$ (an.) | knife-edge $r=1.973$ only, rule M (an.) | no (an.) | yes; $\Delta\mathcal R_T=(19+8\lambda)/96$ (an.) | NT on $(1.748,1.973]$ needs EGJ belief; passive: no equilibrium for $r\in(1.748,1.973)$ | none at the benchmark strengths | $\lambda\in(0,1]$ for (i)–(ii) | EGJ item by item (verified) | no |
| T1, $\theta=1/10$, $\lambda=7/10$ | yes (an.) | yes, unique $(1,-v)$ with a mixed sale, $v=0.29$; $0.527$ (c.-a.) | **no**; $0.509$ (an.) | $[1.439,1.80]$ (c.-a.) | yes: $0.419<0.450<0.484$, partial buy (order an.; values c.-a.) | yes; $+0.292$, $+0.456$ (c.-a.) | NT on $(1.748,1.80]$ needs EGJ belief | rule M at $r_1$ and on the branch; rule Z: no equilibrium at $r_1$ | $\lambda\in[0.42,0.86]$ at $\theta=0.1$; $\theta\in[0.01,0.14]$ at $\lambda=0.7$ (grid) | EGJ menu (verified); unequal weights unverified | no |
| T2 V3, one slot, no separate noise ($\beta=1/3$, $\lambda=6/17$) | yes (an.) | yes, unique full orders; $37/68=0.544$ (an.) | yes; $r_C=3.458$ (an.) | $[1.394,1.748]$; full orders from $1.461$ (an.) | no: flat $37/68$; rule X branch falls (c.-a.); strict rise on $[1.394,1.461)$ | yes; $+113/408$, $+5/68$ (an.) | none on the unit menu; with $q\in[-1,1]$, (iii) needs EGJ belief (X) | none for Prop. 2; rule M below $1.461$ | $82/59<u<2686/1559$; $\lambda\in(0.317,0.365)$ at $\beta=1/3$ | Dow–Gorton (verified); BKT; exact finite form unverified | **yes** (X: 7 claims; one correction to the text) |
| T2 V1/V2, slot plus EGJ's equal noise ($\beta=1/3$, $\lambda=6/17$) | yes (an.) | yes, unique; $71/204=0.348$; V2: $1/2$ when $\beta$ is near $1/2$ (an.) | yes; $r_C=3.458$ (an.) | $[1.557,1.748]$ for every $(\lambda,\beta)$ (an.) | no: no informative equilibrium at $1.55$ (an.); strict rise on $(1.557,r_F)$ | yes; $+113/1224$, $+5/204$ (an.) | none | rule M on the rise; V2 mixtures above $r_N$ open | same strip | EGJ noise plus Dow–Gorton slot; combination unverified | no (L2 reproduces fixed-profile values, n.d.) |
| T3 B1, buy-only, $\theta=3/20$, $\lambda=1$ | yes (an.) | yes, full; $5/8$ (c.-a.) | **no**, every bounded law; $5/8$ at $3.6$ (an.) | about $[1.466,1.830]$ (lower end n.d.); full from $1.655$ | yes: $0.495<0.550<0.617$, mixed branch (c.-a.) | yes; $+123/320$, $+31/64$ | NT needs belief $1$ at the unused top flow near its boundary | rule M on the branch | $\theta\in[0.02,0.15]$ at $\lambda=1$ (n.d.); $\lambda=1$ is the edge of EGJ's $\lambda<1$ | EGJ menu (verified); unequal weights unverified | no |
| T4 D1/D2, buy-only, one-sided geometric or exponential noise, $a=e^{-1}$ | yes (an.) | yes, unique; $0.763$; ownership $0.5$ (an.) | yes; $r_C=3.593$, the paper's (an.) | $[1.394,1.748]$; full from $1.467$ (an.) | no: flat; rule X branch falls (c.-a.) | yes; $+0.485$, $+0.154$ (an.) | none | none for Prop. 2 | $a\in(0.367,0.418]$ (an.) | Edmans 2009 exponential law (verified, opposite direction); geometric form unverified | no |
| T5, buy-only slot plus noise $(0.355,0.29,0.355)$, $\lambda=5/11$, $\beta=1/2$ | yes (an.) | yes, unique; $0.383$ (an.) | yes; $r_C=3.509$ (an.) | contains $[1.549,1.748]$ (c.-a.) | yes: $0.3535<0.3822<0.3831$, mixed, mixed, full (c.-a.) | yes; $+0.126$, $+0.036$ | none | rule M at $1.55$, $1.60$ | box of radii $(1/1000,1/1000,1/2000)$ (c.-a.) | Dow–Gorton slot and EGJ noise form; weights and combination unverified | no |
| T6, two-sided slot plus noise $(0.355,0.29,0.355)$, $\lambda=9/20$, $\beta=12/25$ | yes (an.) | yes, T unique; $0.492$; $(1,-v)$ impossible (an.) | yes; $r_C=3.571$ (an.) | $[1.548,1.748]$ (c.-a.) | yes: $0.3505<0.3789<0.3802$, mixed, mixed, full (c.-a.) | yes; $+0.228$, $+0.060$ | none | rule M at $1.55$, $1.60$; rule Z leaves NT only | box of half-width $1/2000$ (c.-a.); grid $\theta\in[0.35,0.365]$ (n.d.) | Dow–Gorton slot (verified); weights and combination unverified | no (same-member cross-check only) |

Notes on the table.

- Prop. A.9 values are the gains in target proceeds and in net surplus at $r_1$.
- The two-sided discrete-Laplace companion, the bar for comparable strength, has Prop. 2(i)–(iii) analytical, entry $0.569$, coexistence on $[1.516,1.748]$ and flat entry there (earlier study; T1 §4.2). It also lacks the upward order at 1.55–1.65.
- EGJ's rule Z removes every upward branch in the table (T1, T3, T5, T6) and T1's $(1,-v)$ at $r_1$.
- On the T5 and T6 branches the price is not monotone in the flow, because flow $0$ is good news and flow $+1$ bad news when $\theta>1/3$ (T5 Result 7; T6 Result 9). Prices still reveal the posterior.

## 4. The trade-off

### 4.1 The band $(\tau(3),\tau(3.6))=(0.705,0.731)$

- Prop. 2(ii) needs a flow with posterior at least $\tau(3)=0.705$. Prop. 2(iii) needs every full-order posterior below $\tau(3.6)=0.7314$. So the top posterior must lie in $[0.705,0.7314)$, a width of $0.026$ (X §3.9; spot-check A).
- The auction and the two strengths set this band. The noise law does not. The threshold $\tau$ rises only about $0.043$ per unit of strength at $r=3$ (X §3.9).
- The reason: the challenger's gain moves fast with the posterior ($\partial B/\partial\mu=25/3$) and slowly with strength ($\partial B/\partial r\approx-0.36$) (X §3.9).
- The paper's own Laplace calibration gives $M=0.731059$, which lies $0.0003$ below the top of the band (X §3.9). The benchmark $r_2=3.6$ sits just above $r_C=3.5927$.

What this means for any discrete version:

- Its knob must put $M$ inside the band. Below the band, nobody recruits at $r_1$: the buy-only discrete Laplace has $M=0.6225$ (L2 §3.4).
- Above the band, entry does not return at $3.6$: logistic noise of variance $8$ has $M=0.783$, and T1's $\lambda=0.7$ fails (L2 §3.4; T6 Result 2).
- In the knob the band is an open interval, not a knife-edge: $\lambda\in(0.317,0.365)$ at $\beta=1/3$ (T2), or $a\in(0.367,0.418]$ (T4).
- So do not count the width of the band against a candidate. Every device, the paper's included, faces it.

### 4.2 T6's result in plain terms

With unit orders and the slot, at the paper's benchmark (T6 Results 2–4; analytical; spot-check A confirmed):

1. Return to the floor at $3.6$ forces full purchases there, because a purchase then earns at least $0.043$ net of $k$.
2. Full purchases put the top posterior at $M$, so $M\le0.731$. This caps $\lambda$ at $0.463$ for every $\beta$. T1's $\lambda=0.7$ is out.
3. An upward informative branch of T1's kind has class $H$ mix while flows $+1$ and $+2$ recruit. Indifference needs the buyer's residual to fall to the trade cost.
4. That needs a top posterior above $0.755$ at $1.55$ when $\theta=1/3$, and above $0.786$ when $\theta=1/10$.
5. Under the cap, such a branch exists only below $r=1.526$.

So, for noise weights $\theta\le1/3$, the return at $3.6$ and an upward branch at 1.55–1.65 exclude each other. The same cap also removes the paper's $(1,-v)$ at $r_1$. The seller earns at least $0.0448\Delta_T$, above $k=0.03\Delta_T$, so it sells fully (T6 Result 3; analytical; spot-check A6).

### 4.3 What does both, and its cost

T5 (buy-only) and T6 (two-sided) find points with Prop. 2(i)–(iii), coexistence and an upward triple at 1.55–1.65 (computer-assisted). Both move the noise toward heavier tails, $\theta=0.355>1/3$. Then only the top flow recruits on the branch. The costs:

- the certified regions are small boxes: half-width $1/2000$ (T6); radii $1/1000$, $1/1000$, $1/2000$ (T5); T6's grid region is $\theta\in[0.35,0.365]$;
- entry is low: $0.383$ (T5) and $0.492$ (T6) at $r_1$; $0.35$–$0.38$ on the branch, against the paper's $0.545$–$0.551$;
- the last step of the rise is small: $0.0013$ (T6) and $0.001$ (T5);
- the triple is mixed, mixed, full, so it needs rule M;
- the price is not monotone in the flow on the branch;
- neither result has an independent check.

The boxes are small because conditions stack. The band applies at $r_1$ and $r_2$. On top of it, the jump payoff at $1.55$ must exceed $k$ (smallest margin $7.1\times10^{-4}$), and a full purchase at $1.60$ must fail (margin $4.0\times10^{-4}$) (T6 Result 7).

### 4.4 Where the upward segment lies with unit orders

In each slot model, the informative branch that coexists with no trade has two parts (T2 §3.6; X §3.5; T4 §3.3; analytical):

- on $[r_A,r_F)$ class $H$ mixes, and entry rises strictly with strength;
- from $r_F$ class $H$ buys fully, and entry is flat.

Their location:

- $r_A$ does not depend on the knob. It is $1.394$ without separate noise (T2 V3, T4) and $1.557$ with EGJ's equal noise (T2 V1/V2; T6 at $\theta=1/3$) (T2 eq. 32).
- $r_F$ depends only on $M$. Across the band it runs from $1.442$ to $1.467$ (spot-check C1).
- So the slot model without noise rises at about $1.39$–$1.47$. X reports entry $0.481$ at $1.40$, $0.532$ at $1.45$ and $37/68=0.544$ from $1.50$ (computer-assisted).
- With EGJ's noise on top, the rise sits at $1.557$–$1.61$ (T6 Result 8(a)). The paper's points 1.55–1.65 fall between the two.

### 4.5 What the continuous order size does

- The paper's Prop. 3 uses pure strategies with a partial sale: $(q_H,q_L)=(1,-v_i)$ with $v=0.46,0.71,0.90$ at $1.55,1.60,1.65$. Entry rises with $v$ (paper, Section 4.3).
- With unit orders a sale is all or nothing. The only continuous margin is a mixture probability. It needs rule M, and EGJ's rule Z removes it (L2 §3.2; T4 §6; T1, T3, T5, T6).
- With the slot inside the band, the seller sells fully at $r_1$, so not even a mixed $(1,-v)$ appears (T6 Result 3; analytical). Without the slot, T1 obtains $(1,-v)$ at $r_1$, but it loses Prop. 2(iii).
- So the strict upward order at the paper's strengths, carried by a partial sale, is a property of continuous order sizes. Unit orders keep a weaker statement: entry rises weakly along the branch that coexists with no trade, strictly where the investor mixes.

## 5. Recommendation

### 5.1 Recommended: the order slot, two-sided, no separate noise

**Specification** (T2 V3 two; checked by X).

1. One public order opportunity precedes the challenger's decision.
2. With probability $\lambda$, the informed investor fills it. It sees the class and chooses $q\in\{-1,0,1\}$ at cost $k$ per unit.
3. With probability $1-\lambda$, a liquidity trader fills it. It sells, abstains or buys one unit with probabilities $\beta$, $1-2\beta$, $\beta$. Its motive is exogenous.
4. Nobody observes the identity. The identity draw is independent of the class, the costs and the incumbent's value.
5. Market makers see the order and set $P=\mathbb E[V_T\mid X]$. The challenger sees the price, as in the paper.

**Knob, range and calibration.**

- The knob is $u=\lambda/((1-\lambda)\beta)$: the odds that an order in a given direction is informed rather than a liquidity order. It sets $M=(1+u)/(2+u)$.
- The informed share of nonzero orders is $2M-1$ (T2 eq. 48). This gives a PIN-like interpretation; its empirical link is unverified.
- Range: $82/59<u<2686/1559$ (T2 eq. 18; X claim 2; analytical). At $\beta=1/3$ this is $0.317<\lambda<0.365$. The informed share of nonzero orders lies between $0.41$ and $0.463$.
- $\beta$ sets how often the slot trades. Entry at $r_1$ is $\rho+(1-\rho)(b+\lambda/2)$. So $\beta$ moves the entry level for a given $M$.
- **Calibration A (checked).** $\beta=1/3$ copies EGJ's equal weights onto the liquidity order. $\lambda=6/17$ gives $M=29/40$.
- **Calibration B (paper match; numerical diagnostic, spot-check C3).** $u=e-1$ gives the paper's top posterior $0.731059$ and so the paper's ceiling $3.592659$ (T4 at $a=e^{-1}$, with spot-check B). Then $\beta=0.2947$ ($\lambda=0.3361$) gives entry $0.522757$ and ownership $0.3244$ at $r_1$ (paper $0.3242$). The return margin at $3.6$ is the paper's own, $0.0003$ in posterior.
- **Story.** An order of standard size arrives. It carries information with probability $\lambda$; otherwise it is a liquidity trade. This is Dow–Gorton's assumption. It is also EGJ's third interpretation of $\lambda$ (an uninformed trader), with an exogenous liquidity motive.

**What it reproduces.**

- Prop. 2(i): no trade is unique at $1.2$, entry $\rho$ (analytical; checked).
- Prop. 2(ii): full orders are unique at $3$; entry $37/68=0.544$, ownership $23/68$ (analytical; checked). Calibration B gives $0.5228$ (numerical diagnostic).
- Prop. 2(iii): full orders are unique at $3.6$, entry $\rho$, prices informative; $r_C=3.458$ (analytical; checked); calibration B gives $3.5927$ (numerical diagnostic).
- The no-trade boundary $r_N=1.747878$ is the paper's value (analytical).
- No trade coexists with informative trade on $[1.394,1.748]$, which contains 1.55–1.65 (analytical; the three-strength values computer-assisted; checked).
- Entry rises weakly along the branch that coexists with no trade: strictly on $[1.394,1.461)$, then flat (analytical; checked).
- Prop. A.9: proceeds rise by $113/408$ and net surplus by $5/68$ at $r_1$ (analytical; checked).
- No claim needs an off-path belief on the unit menu. Prop. 2 holds under all four pairs of tie rules (analytical; checked).
- Each order decision is one comparison $K-k$ with closed-form bounds, so the proofs are short.

**What it loses.**

- The partial sale $(1,-v)$: impossible with unit orders inside the band (analytical; T6 Result 3).
- The strict upward order at 1.55, 1.60, 1.65: entry is flat there (computer-assisted; checked). The strict rise lies at $1.39$–$1.46$ and needs rule M.
- Additive noise: the flow is the slot order itself. The alternative in §5.2 keeps EGJ's noise.
- A free uninformed trader: the liquidity motive must be assumed (analytical; checked).
- Dispersed classes, other priors, atomless costs and private signals are not studied (open).

**What the paper would need to say or change.**

- **Order menu.** Replace $q\in[-1,1]$ with unit orders $\{-1,0,1\}$, as in EGJ. With a continuous menu, a $0.99$ purchase reaches an unused flow. Under the prior belief there it earns $0.0964>0.0446$ at $3.6$ and breaks Prop. 2(iii) (X §4). The continuous menu can stay only with EGJ's convention that an unused order comes from an informed trader.
- **Noise section.** Replace the Laplace law and its score-bound argument with the slot, the knob $u$, and the band argument of §4.1.
- **Model section.** State the exogenous liquidity motive. Cite Dow–Gorton (1997) for the device, EGJ (2015) for the unit menu and the readings of $\lambda$, and Admati–Pfleiderer (2009) for a liquidity shock that forces the same trade.
- **Prop. 3.** Restate it as coexistence on $[r_A,r_N]$, with entry that rises weakly along the informative branch and strictly where the investor mixes.

**How to present the lost results.**

- Present Prop. 3's strict upward order and the $(1,-v)$ pattern as properties of continuous order sizes (§4.5).
- A remark can say: when the investor can sell part of a unit, the partial sale grows with strength and entry rises with it; unit orders cannot carry this.
- An appendix can keep the continuous-order analysis as an extension, with the slot model in the main text.

### 5.2 Alternative: the order slot with EGJ's noise on top

Choose this if the priority is EGJ's own noise and an upward branch near the paper's strengths.

**Specification** (T2 V2; T6 at $\theta=1/3$). The slot of §5.1, plus independent noise $Z\in\{-1,0,1\}$ with equal weights, as in EGJ. The flow is $X=Q+Z$. Example points: $(\lambda,\beta)=(9/20,12/25)$ (T6 Result 8(a)) or $(6/17,1/3)$ (T2).

**Knob and range.** The same strip in $u$. When $\beta\ge82/(82+59u)$, the flow $+1$ also recruits at $r_1$, and entry is $1/2$ (T2 eq. 22).

**What it reproduces.**

- Prop. 2(i)–(iii) with unique full two-sided orders (analytical). Entry is $1/2$ at $r_1$ at $(9/20,12/25)$, and $71/204=0.348$ at $(6/17,1/3)$.
- Coexistence on $[1.557,1.748]$ (analytical).
- An upward branch in closed form on $[1.557,1.609]$ at $(9/20,12/25)$: $A(r)=c[4/(12\kappa(r)-1)-2]$ and entry $1/4+c/(2(12\kappa(r)-1))$, with $c=(1-\lambda)\beta$ (T6 Result 8(a); analytical).
- At $1.56$, $1.58$, $1.60$ all three purchase rates are interior, and entry rises $0.345<0.355<0.366$ (computer-assisted).
- Prop. A.9 (analytical). No off-path belief.

**What it loses.**

- The point $1.55$. Since $r_A=1.557$ for every $(\lambda,\beta)$, no informative equilibrium exists at $1.55$ (T2 eq. 36; analytical).
- The smallest repair is $k\le0.019620$ instead of $0.02$ (T2 eq. 37). It admits the first point only. The other repair is to move the illustrative strengths to 1.56–1.60.
- Entry on the branch is $0.35$–$0.37$, against the paper's $0.545$–$0.551$.
- $(1,-v)$ at $r_1$ (analytical; T6 Result 3). The branch needs rule M.
- No independent check. The V2 mixed correspondence above $r_N$ is open.

### 5.3 Why not the others

- **T1** (EGJ's block as is): no return at $3.6$ for any $\lambda$ or $\theta$ (analytical). Its second knob gives the closest Prop. 3 and the paper's $(1,-v)$ at $r_1$, but it needs mixtures and unverified weights, and (iii) still fails.
- **T3**: no return for any bounded law (analytical).
- **T4**: the same buyer's problem as §5.1 (spot-check B), with the paper's exact ceiling and Edmans's verified exponential law. It is buy-only, drops EGJ's bounded noise, and gives entry $0.763$ and ownership $0.5$. Use it as a cross-reference, not as the EGJ-like model.
- **T5 and T6**: the only setups with the exact triple at 1.55–1.65 together with (iii). Their boxes are small, entry is low, prices are not monotone in the flow, and nobody else checked them. T6 is the fallback if the exact triple is essential.

### 5.4 The comparison

| Criterion | Recommended (§5.1) | Alternative (§5.2) | T6 point |
|---|---|---|---|
| Closeness to EGJ | Unit menu, unit cost, competitive price, $\lambda$; no additive noise | EGJ's block plus the slot | EGJ's block plus the slot; weights $0.355$ |
| Strength | Prop. 2, coexistence, A.9 analytical; checked | Analytical; not checked | Prop. 2 analytical; Prop. 3 computer-assisted; not checked |
| Robustness | Open strip; the band of §4.1 only | Same strip; fails at $1.55$ for every knob | Box of half-width $1/2000$ |
| Entry at $r_1$ (paper $0.523$) | $0.544$ (A); $0.523$ (B) | $1/2$ | $0.492$ |
| Upward order at 1.55–1.65 | No; strict rise at $1.39$–$1.46$ | No at $1.55$; strict rise at $1.557$–$1.61$ | Yes, thin |
| Precedent | Dow–Gorton's device (verified) | Two verified parts; combination unverified | Weights and combination unverified |

## 6. What remains open, ranked

1. **Independent checks** (open). Only T2 V3 has an independent check (X). T1, T3, T4, T5, T6 and T2 V1/V2 have none. T1 and T6 carry same-member cross-checks only; L2 reproduces fixed-profile values of V1 and V3 two (numerical diagnostic). My spot-checks cover T6's trade-off and the T4/T2 equivalence only. The first check to commission is the alternative of §5.2.
2. **The slot with continuous order sizes** (open). An equilibrium analysis with $q\in[-1,1]$, partial sales and EGJ's belief convention (X §4; T6 open issue 6; T4 §6). It decides whether the paper can keep $(1,-v)$ and its Prop. 3 together with the slot.
3. **A foundation for the liquidity motive** (open). The device needs an exogenous motive (T2 §3.7; X claim 6).
4. **The paper's Section 5 extensions under the slot** (open): other priors, dispersed classes, atomless costs, private signals.
5. **Exact certificates for calibration B** (numerical diagnostic now). A rational point near $u=e-1$, $\beta=0.2947$ with exact margins is open.
6. **T5 and T6 limits** (open): the maximal regions, the best entry levels, a branch with three interior purchase rates at 1.55–1.65, and an analytical version of T6 Result 4 for $\theta\in(1/3,1/2)$.
7. **Existence under EGJ's rule Z** where only mixed equilibria exist (T1 open issue 6; open).
8. **Precedent gaps** (unverified): the model sections of Glosten–Milgrom, the PIN model, Kyle (1985), Kyle–Vila, Shleifer–Vishny and Bagnoli–Lipman (RAND, not RFS) (L1; L2 §6). The exact finite slot device has no verified published form beyond Dow–Gorton's version.
9. **An empirical calibration** of $\lambda$ or of the informed share of orders (T2 §3.11; unverified).

## 7. Plain summary

Normal noise is the most common choice: 7 of 15 sampled models. Discrete models are rare. EGJ and Goldstein–Guembel use three-point noise. Dow–Gorton lets an order be informed or a same-size liquidity trade. No corporate model uses Laplace noise.

EGJ's own block cannot return entry to its floor at strength 3.6. Its largest flow can come only from an informed purchase. That flow reveals the high class, and the expensive challenger still prepares there. Presence below one hides only the middle flows.

One device removes the problem. When the informed trader is absent, a liquidity trader places an order of the same size. Then every flow can come from either class, and no price reveals the class. Dow–Gorton use this device.

The paper's benchmark imposes a narrow band on the top posterior: 0.705 to 0.731. The auction sets this band, not the noise. The paper's own Laplace calibration sits at its top edge.

With unit orders, a second limit appears. The band caps the top posterior at 0.731. An upward branch of EGJ's kind needs a top posterior above 0.755. Setups that achieve both live in tiny boxes and give low entry.

Recommendation: one order slot with unit orders, buy, sell or hold, and no separate noise. It gives no trade at 1.2, entry 0.544 at 3, and the floor at 3.6, all analytical. With a second calibration it matches the paper's entry, 0.523, and its ceiling, 3.593. Coexistence holds on 1.394 to 1.748. An independent member checked it. It loses the partial sale and the strict upward entry order at 1.55 to 1.65. Present those as features of continuous order sizes.

Alternative: the same slot with EGJ's noise on top. It keeps a closed-form upward branch, but at 1.557 to 1.61. Nobody else checked it.
