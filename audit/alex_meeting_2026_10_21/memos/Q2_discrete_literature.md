# Q2 (literature): discrete microstructure in feedback and takeover models

Memo to the author. Meeting of 21 October 2026, point 2. Workstream: literature.

## 1. Question and reading

The supervisor suggests a "purely discrete setup like the Edmans paper and a few others", with a trading menu that may be one-directional. This memo answers four questions.

- (a) What is the most conventional discrete specification for this paper?
- (b) How do these papers treat off-path order flows? Does a one-directional order set remove the problem?
- (c) Does any of them let the decision maker see the price instead of the flow? What goes wrong?
- (d) What should the author do, and how can the author position a discrete version?

Reading: I read the model sections of the papers marked "read" in Section 2, in the versions named there. I could not read four papers (Glosten and Milgrom 1985; Kyle and Vila 1991; Khanna and Sonti 2004; Diamond and Verrecchia 1987). They are marked "unverified". I use the paper's vocabulary for status: **analytical**, **numerical diagnostic**, **conjecture**, **open**. A claim labelled "literature fact" is a statement I checked in the source text.

Section numbers: the brief calls the flow-versus-price remark "Section 2.2" and the stake discussion "Section 3.5". The published layout of Edmans, Goldstein and Jiang (2015) uses Roman numerals. The flow-versus-price remark is in Section I.B (p. 3775, footnote 7). The stake discussion is in Section II.E (pp. 3787–3788), with the full analysis in Online Appendix B.2. I did not read the Online Appendix.

## 2. Comparison of model specifications

Abbreviations: EGJ = Edmans, Goldstein and Jiang (2015, AER 105(12): 3766–3797). GG = Goldstein and Guembel (2008, RES 75(1): 133–164). DGG = Dow, Goldstein and Guembel (2017, JEEA 15(4): 877–909). BKT = Boleslavsky, Kelly and Taylor (working paper, Oct. 2013; the published version, JET 169: 294–343, 2017, is unverified). BGP = Bond, Goldstein and Prescott (2010, RFS 23(2): 781–820). GOY = Goldstein, Ozdenoren and Yuan (2013, JFE 109(2): 566–582). "DM" = the real decision maker. "MM" = market maker.

### Table 2.1. State, information, orders, noise

| Paper (status) | State space and prior | Informed trader: information, order set, cost, presence | Noise trader |
|---|---|---|---|
| **EGJ 2015** (read; AER-layout accepted manuscript) | $\theta\in\{H,L\}$, $y=1/2$. Firm value $v(\theta,d)$, $d\in\{-1,0,1\}$ (Table 1). | Present with probability $\lambda\in(0,1)$; nobody else knows. Sees $\theta$ exactly. No initial stake in the core model (stake $\alpha>0$ in Section II.E and Online App. B.2). Order $s\in\{-1,0,1\}$. Cost $\kappa$ per unit, equal for buying and selling. Indifferent: no trade. | $z\in\{-1,0,1\}$, equal probabilities. Always present. |
| **GG 2008** (read; published) | $\omega\in\{l,h\}$, probability 1/2. Invest or not; $V(h,K)=V^+>0>V^-=V(l,K)$; $V(\omega,0)=0$. | Perfect signal with probability $\alpha$; no signal with probability $1-\alpha$ (this "uninformed" type can manipulate). Two dates. $u_t\in\{-1,0,1\}$. No explicit trading cost. Mixed strategies. | $n_t\in\{-1,0,1\}$, equal probabilities, independent across dates. (The 2002 working paper used $\{-1,1\}$.) |
| **DGG 2017** (read; published). *Not discrete.* | $\omega\in\{l,h\}$, 1/2. Project $A\in\{0,1\}$; $V_h>V_0>V_l$. | Continuum of speculators. Each pays $c$ for a signal of precision $\phi>1/2$. Order $x_i\in[-1,1]$. | Liquidity order $n\sim N(0,\sigma^2)$. |
| **Edmans 2009** (read Section I; repository copy). *Partly discrete.* | Public signal $s\in\{s_g,s_b\}$. If $s_g$: $V=X$. If $s_b$: $V\in\{0,X\}$, equal odds. | Blockholder with an initial stake. Pays an effort cost; gets a private signal $i\in\{i_g,i_b\}$ with precision rising in effort. Order: hold, or sell up to the stake (**short sales barred**; buying is in the Internet Appendix, footnote 8). | Liquidity demand $u\ge 0$, exponential (continuous, one-sided). |
| **BKT 2013 WP** (read). *Continuous.* | $\omega\in\{0,1\}$, prior $q$ on 0. Arrow security. | One trader: informed with probability $a$ (type $i\in\{0,1\}$ equals $\omega$), noise with probability $1-a$. Order $t\in\mathbb R$. Mixed strategies on intervals. No trading cost. | Order uniform on $[-1,1]$ (footnote 6: any distribution works). |
| **BGP 2010** (read parts). *Continuous, rational expectations.* | Fundamental $\theta$ continuous. Agent sees $\phi=\theta+\xi$, $\xi$ uniform. | Speculators know $\theta$. Trade through a price function. | No noise trader in the text I read. Appendix B: one market maker, no noise. |
| **GOY 2013** (read parts). *Continuous.* | Normal fundamental. | Speculators with correlated normal signals. Position $x(i)\in[-1,1]$. | Noisy supply (normal). |
| **Glosten and Milgrom 1985** (**unverified**; not read) | Binary value (from secondary descriptions). | Informed traders know the value. One unit per trade; only the direction carries information (secondary description). | Uninformed traders buy or sell with probability 1/2 (secondary description). |
| **Khanna and Sonti 2004** (**unverified** beyond abstract and GG's summary) | Binary state (not confirmed). | Sequential traders. A late trader with an inventory buys after a run of buy orders (GG 2008, pp. 135–136). | Not confirmed. |
| **Kyle and Vila 1991** (**unverified** beyond abstract and Edmans 2009 fn. 17) | Takeover of a firm by a large outsider. | Large outsider buys. Noise trading "provides camouflage" (abstract). | Order law not confirmed. |
| **Diamond and Verrecchia 1987** (**unverified**; not read) | Rational expectations model with a specialist (secondary description). | Informed traders may not sell short (secondary description). | Not confirmed. |
| *This paper (current)* | $\theta\in\{\ell,h\}$, 1/2. | Always present. $q\in[-1,1]$. Cost $k\vert q\vert$. | $Z$ Laplace, $b>1$. |

### Table 2.2. Observation, pricing, equilibrium

| Paper | MM sees; pricing rule | DM sees | Fully revealing flows | Equilibrium and off-path rule | Uniqueness or multiplicity | One-directional trade |
|---|---|---|---|---|---|---|
| **EGJ** | $X=s+z\in\{-2,\dots,2\}$. $p(X)=E(v\mid X)$. | **Order flow $X$**, not the price (Section I.B, p. 3775 and fn. 7). The paper says that with $p$ other equilibria arise, "self-fulfilling". In the equilibria it studies, two flows with the same price lead to the same decision. | $X=\pm2$ when the profile has $s=\pm1$. $X=\pm1$ also reveal when $\lambda=1$ (p. 3787). $X=0$ is uninformative in T. | Perfect Bayesian. Off-path beliefs satisfy the Cho–Kreps Intuitive Criterion (p. 3776, item (v)). At off-path $X=\pm2$ the belief is that the speculator knows the state, "since speculators always lose if they trade against their information" (proof of Prop. 1, p. 3779). Pure strategies only. | NT, T, BNS, SNB. Cutoffs in $\kappa$ (Lemma 1, Prop. 1). No feedback: BNS and SNB coexist on $[\kappa_{NF},\kappa_{NT})$ with "no obvious way to select" (p. 3778). Feedback: BNS is the only pure equilibrium on $[\kappa_T,\min(\kappa_{SNB},\kappa_{NT}))$. | **Endogenous.** BNS and SNB are equilibrium outcomes. Feedback widens the BNS range and narrows the SNB range. |
| **GG** | $Q_t=n_t+u_t$. $p_1=E[V\mid Q_1]$, $p_2=E[V\mid Q_1,Q_2]$. | **Flows $Q_1,Q_2$** (p. 137). (The 2002 working paper had the manager read prices.) | $Q_1=2$ reveals the positively informed speculator (p. 141). | Perfect Bayesian, mixed. Fn. 12: all $Q_2$ occur with positive probability, so "our result does not depend on any assumptions about off-the-path beliefs". Prop. 3 (p. 147) uses the Intuitive Criterion. | No feedback: multiple equilibria (p. 138). Feedback: Prop. 2 gives existence; Prop. 3 says every Intuitive-Criterion equilibrium has manipulation when $\bar V$ is small. | **Endogenous.** Section 6, Prop. 4: manipulation by buying is never profitable. The authors cite this to support short-sale rules. |
| **DGG** | $X=n+\int x_i\,di$. $P(X)=E[V\mid X]$. | **Price** (p. 881: "He observes the share price"). | None (normal noise). | Equilibrium of the continuation game, then information choice. | Lemma 1 (p. 883): other equilibria exist where the MM sets $P=V_0$ on a larger set of flows. "The equilibrium described in Lemma 1 is the only equilibrium that survives" if the firm sees order flow. | Informed buy on $h$, sell on $l$. |
| **Edmans 2009** | Total demand $d=b+u$ and public $s$. $P=E[V\mid d,s]$. | Section II not read. | $d\le0$ reveals a sale, because $u>0$. | Nash (Lemma 1). No off-path flow: $u$ has full support on $(0,\infty)$. | Lemma 1 states the Nash equilibrium; uniqueness not checked. | **Exogenous** short-sales constraint. The paper notes that discrete liquidity trades in Kyle-type corporate-finance models force the informed trader to match their size, so her order does not depend on her stake (p. 9–10 of the repository copy). |
| **BKT WP** | The order $t$; price equals expected payoff (Bertrand). | **Order flow $t$** (stage 3: "observes the trade"). | An order with posterior $\chi(t)>c$ triggers intervention for sure, so $p(t)=1$ (p. 9). | Perfect Bayesian. Fn. 11: all orders in $[-1,1]$ are on path because the noise trader can submit them; no order outside $[-1,1]$ is ever played. | The WP says a unique equilibrium exists when intervention is costly or the flow is noisy. | **By dominance.** A type-0 buy and a type-1 sell are weakly dominated, so trades are "non-negative" without loss (p. 7). |
| **BGP** | No MM in the main model. Trading game (App. B): MM posts a price; speculators buy or sell. | **Price** (App. B: "The agent observes the price"). | Prices fully reveal $\theta$ in the limit case of an uninformed agent (Section 2.4 argument). | Rational expectations. | Multiple equilibria for moderate agent information; **no equilibrium** for poor agent information. In the trading game the MM abstains and trade breaks down (Prop. 7). | — |
| **GOY** | Linear price from noisy supply. | **Price** (through $z(P)$) and a private signal. | None. | Linear Gaussian. | Prop. 1 (high supply elasticity) gives a linear equilibrium; uniqueness not checked. | Position limit $[-1,1]$. |
| **Current paper** | $X=q+Z$. $P=E[V_T\mid X]$. | **Price $P$** and cost $C$. | None: Laplace has full support, posteriors lie in $[m,M]$. | Perfect Bayesian. Every flow is on path. | Prop. 2 (unique) and Prop. 3 (multiplicity between cutoffs). | None. |

Notes on the table.

- Only EGJ and GG are discrete in the full sense (three-point noise, three-point order set, flow seen by the decision maker). Edmans (2009) is discrete in the state and in the order set but has exponential noise. BKT, DGG, BGP and GOY are continuous. They matter here for question (c) only.
- In every discrete model I read, the decision maker sees the flow. DGG and BGP see the price and report multiplicity (DGG) or non-existence and multiplicity (BGP).
- Neither EGJ nor GG uses unequal noise probabilities. The brief's general $(\pi_-,\pi_0,\pi_+)$ has no template in these papers.
- The brief's pinned discrete model copies EGJ item by item (three-point noise, equal probabilities, presence probability $\lambda$, tie rule, $P=E[V\mid X]$). The differences are the challenger's information (price, not flow) and the payoff (an entry channel instead of a managerial decision).

## 3. Results

### 3.1 Literature facts

**R1 (literature fact).** EGJ is the template for each element the brief pins (see the notes above). Section II.E states that "$\lambda<1$ is necessary for the speculator not to be fully revealed when $X=\{-1,1\}$ and thus for trading profits to be nonzero" (p. 3787). The brief's leading case, an always-present investor, is the degenerate boundary of EGJ.

**R2 (literature fact).** EGJ give three readings of $\lambda$ (p. 3787): the speculator is present with probability $\lambda$; she is always present but can trade only with probability $\lambda$ (a liquidity shock); or she is always present and informed only with probability $\lambda$. The third reading lets an uninformed speculator sell to manipulate the price, as in GG. EGJ "do not analyze this framework here". The current paper's investor is always informed when present, so the first two readings fit it. They avoid manipulation.

**R3 (literature fact).** One-directional trade appears in three ways.

- Endogenous by equilibrium: EGJ (BNS), GG (Section 6).
- Endogenous by dominance: BKT (p. 7).
- Exogenous by constraint: Edmans (2009, short-sales constraint; footnote 8 says buying is analysed in the Internet Appendix). EGJ (Section III.B) cite Miller (1977) for prices that are too high when short sales are barred. Diamond and Verrecchia (1987) is the other standard reference (**unverified**).

The supervisor's proposal to switch off one direction is therefore standard in kind. It is exogenous in Edmans (2009) and endogenous in EGJ.

### 3.2 Derived claims for the paper's discrete version

Setting for all claims below. Noise $z\in\{-1,0,1\}$ with probability 1/3 each. The investor is present with probability $\lambda$ and trades $q_\theta$. If absent, the order is 0. Prior 1/2. Flow $X=q+z$. All objects ($t_0$, $\Delta_T$, $B_r$, $e$, $\tau$) are as in Section 1 of the brief.

**C1 (analytical; printed by `flows.py`). Posteriors by flow.** $\Pr(X\mid\theta)$ is a sum of terms $\tfrac13\cdot$(probability of the order), so with equal noise it is a multiple of $1/3$. For each flow the posterior is therefore $0$, $1$, $1/2$ or a $\lambda$-dependent interior value.

| Profile $(q_h,q_l)$ | $\lambda=1$: posterior $\mu_X$ at $X=-2,\dots,2$ | $\lambda=1/2$ |
|---|---|---|
| NT $(0,0)$ | off, 1/2, 1/2, 1/2, off | off, 1/2, 1/2, 1/2, off |
| T $(1,-1)$ | 0, 0, 1/2, 1, 1 | 0, 1/3, 1/2, 2/3, 1 |
| BNS $(1,0)$ | off, 0, 1/2, 1/2, 1 | off, 1/3, 1/2, 1/2, 1 |
| SNB $(0,-1)$ | 0, 1/2, 1/2, 1, off | 0, 1/2, 1/2, 2/3, off |

General $\lambda$: in T, $\mu_{+1}=1/(2-\lambda)$ and $\mu_{-1}=(1-\lambda)/(2-\lambda)$. In BNS, $\mu_{-1}=(1-\lambda)/(2-\lambda)$. These match EGJ's posteriors (p. 3777–3781).

Consequence for the brief's check: with $\lambda=1$ and equal noise, **every flow is either fully revealing or equal to the prior**. No interior flow carries partial information. With $\lambda<1$ the interior flows carry partial information. With unequal $(\pi_-,\pi_0,\pi_+)$ the interior flows carry information even at $\lambda=1$ (for example, in BNS $\mu_0=\pi_-/(\pi_-+\pi_0)$). This follows from Bayes' rule; no paper I read uses it.

**C2 (analytical). Off-path flows by order set.** A flow is on path if some type reaches it with positive probability. Flows reached by deviation only are off path. Take $\lambda$ arbitrary.

| Order set | Feasible flows | NT off-path | Trading profile off-path |
|---|---|---|---|
| $\{-1,0,1\}$ | $-2,\dots,2$ | $X=\pm2$ | T: none. BNS: $X=-2$. SNB: $X=+2$. |
| Buy-only $\{0,1\}$ | $-1,0,1,2$ | $X=2$ | BNS: none. |
| Sell-only $\{-1,0\}$ | $-2,-1,0,1$ | $X=-2$ | SNB: none. |

Derivation: $X\ge q_{\min}-1$ and $X\le q_{\max}+1$. On path, a profile reaches $\{q_\theta+z\}$ for the types it uses, and $z$ has full support on $\{-1,0,1\}$. In a trading profile, the type that trades covers the top (or bottom) flow, and the type that does not trade covers the other end. So the supervisor's statement holds for the trading equilibrium. It does **not** hold for the no-trade equilibrium: one flow remains off path even with a one-directional menu. Prop. 2(i) at $r_0$ is a no-trade statement, so it still needs one off-path belief.

**C3 (analytical). The Intuitive Criterion fixes that belief in one line.** The investor's per-unit payoff from buying in state $\theta$ at flow $x$ is $V_T^\theta-P(x)=e\,\Delta_T[\mathbf 1\{\theta=h\}-\mu_x]$ (eq. (11) of the paper, with $e=e(P(x))$). For state $\ell$ this is $-e\Delta_T\mu_x\le0$ at every belief $\mu_x\in[0,1]$. Add the cost $k>0$: type $\ell$ gets a strictly negative payoff from any buy, at any off-path belief. In NT its equilibrium payoff is 0. Buying is therefore equilibrium-dominated for $\ell$ and not for $h$. The Intuitive Criterion puts $\mu(X=2)=1$ (and $\mu(X=-2)=0$ by the same argument for selling). This is the argument EGJ give in one sentence (p. 3779). It uses the sign structure of (11), so it holds for this paper's payoff.

**C4 (analytical). The belief rule moves the no-trade cutoff.** Take two-sided or buy-only, any $\lambda$. In NT the flows $X=0,1$ have $\mu=1/2$ and $X=2$ is off path. Type $h$ deviating to buy gets

$$\tfrac23\cdot\tfrac12\,e_r(\tfrac12)\Delta_T+\tfrac13\cdot A(X{=}2)-k .$$

Under the Intuitive Criterion $A(X{=}2)=0$ (price reveals $h$), so NT holds iff $k\ge e_r(\tfrac12)\Delta_T/3$. Under the belief $\mu(2)=1/2$ the third term is $\tfrac13\cdot\tfrac12 e_r(\tfrac12)\Delta_T$ and NT holds iff $k\ge e_r(\tfrac12)\Delta_T/2$. The cutoff changes by a factor $3/2$. The belief rule is therefore not a detail. EGJ's value $\kappa_{NT}=\tfrac13(R_H-R_L)$ (p. 3779) is the same expression with $e\Delta_T$ in place of $R_H-R_L$. Compare Prop. A.4 of the paper ($\rho\Delta_T/2\le k$): the factor $1/2$ becomes $1/3$ because one flow in three reveals the deviator.

**C5 (analytical, with a numerical diagnostic). When the challenger sees the price, Prop. A.2 survives only with a floor on the posterior.** The paper's Prop. A.2 uses two facts. (i) Competitive pricing gives $P=t_0+e(P)[t_L-t_0+\Delta_T\mu_X]$, eq. (10). (ii) $e(P)\ge\rho>0$, because the low-cost type enters at every reachable posterior ($c_L<B_r(m)$). Then two flows with the same price have the same posterior, and the price identifies $\mu_X$. Nothing in this argument uses the Laplace shape. It uses only the floor.

In a discrete model with a flow that reveals $\ell$ ($\mu=0$), the floor needs $c_L\le B_r(0)=g_L$. At the benchmark, $g_L(r_1)=0.125$ and $c_L=1$. The floor fails (numerical diagnostic: $g_L=0.3125,\,0.125,\,0.1042$ at $r=1.2,\,3,\,3.6$). Then $e=0$ at revealing-low flows and the price equals $t_0$ at all flows where nobody prepares. Several flows with different posteriors can share the price $t_0$. This is the DGG and EGJ self-fulfilling mechanism.

A pool $S$ of flows priced at $t_0$ is self-fulfilling only if three conditions hold: $S$ contains every flow whose own posterior is below $\mu_L=(c_L-g_L)/(g_H-g_L)$; $S$ contains one flow at or above $\mu_L$; and the pooled posterior is below $\mu_L$. I enumerated all subsets of flows for NT, T, BNS and SNB, $\lambda\in\{1,1/2\}$, $r\in\{1.2,3,3.6\}$ at the benchmark (`flows.py`). **No self-fulfilling pool exists** (numerical diagnostic). The reason is that $\mu_L\approx0.08$–$0.11$ is small and adding any flow with $\mu\ge1/2$ lifts the pooled posterior above it. The result is specific to the benchmark vector. It is not a theorem.

The floor is restored in three ways.

- $c_L\le g_L(r_1)$. For example $c_L=0$ (this connects to point 4; see Section 7).
- Buy-only with $\lambda<1$. The lowest flow is $X=-1$ with $\mu=(1-\lambda)/(2-\lambda)>0$. The floor condition $(1-\lambda)/(2-\lambda)>\mu_L$ is $\lambda<0.8827$ at $r_1$ (numerical diagnostic; $0.9171$ at $r_0$).
- Sell-only does **not** restore it: $X=-2$ is reachable only by $q=-1,z=-1$ and reveals $\ell$ for every $\lambda$. Two-sided trade does not restore it either, for the same reason.

So buy-only with $\lambda<1$ is the one discrete variant that keeps A.2 as written at the benchmark.

**C6 (analytical for pure profiles; numerical diagnostic; sketch of Prop. 2).** Take $\lambda=1$, two-sided, benchmark parameters, $e\equiv e_r(1/2)=\rho$ (since $B_r(1/2)<c_H$ at all three $r$ values). One-step deviation payoffs follow from $q\,e\Delta_T(\mathbf 1\{\theta=h\}-\mu_x)-k|q|$ and the table in C1.

- T needs both types to trade. Type $h$ gets $\tfrac13\cdot\tfrac12 e\Delta_T-k$. So T iff $k<e\Delta_T/6$.
- BNS needs $h$ to buy ($k<e\Delta_T/3$, as in C4) and $\ell$ not to sell ($k\ge e\Delta_T/6$). SNB is the mirror image. They hold on the same interval.
- NT iff $k\ge e\Delta_T/3$.

A grid scan over $k$ with off-path beliefs from C3 (`profiles.py`) reproduces these cutoffs: T below $k/\Delta_T=0.0417=\rho/6$, BNS and SNB on $[0.0417,0.0833)$, NT above $\rho/3=0.0833$. These cutoffs have the form of EGJ's $\kappa_{NF}$ and $\kappa_{NT}$ in the no-feedback case, with $e\Delta_T$ in place of $R_H-R_L$. As I read the typeset formula (p. 3780), $\kappa_{NF}=\tfrac13[\tfrac{1-\lambda}{2-\lambda}+\tfrac12](R_H-R_L)$, which is $\tfrac16(R_H-R_L)$ at $\lambda=1$. My own derivation of the deviation payoff gives the same expression.

At the benchmark $k=0.02$: $\Delta_T(r_0)=0.01667$, so NT holds at $r_0$ ($0.00139\le0.02$). $\Delta_T(r_1)=0.6667$, so T holds at $r_1$ ($0.02<0.0278$). Parts (i) and (ii) of Prop. 2 therefore have discrete analogs with a single cutoff for NT and a separate cutoff for T. The partial-trade region is a **separate interval between them**, not an overlap with NT.

Two findings against the current Prop. 2.

- **Entry at $r_1$ (numerical diagnostic).** Two-sided T gives entry $\tfrac13\cdot1+\tfrac13\rho+\tfrac13\cdot0=0.4167$, above $\rho=0.25$. The last term is 0 because the low-cost type does not prepare after a revealed $\ell$ ($c_L=1>g_L$). With $c_L\le g_L$ it is $0.5$. Buy-only gives $0.3333$.
- **Part (iii) fails at $r_2=3.6$.** After a flow that reveals $h$, the challenger's gross profit is $g_H(r)$, and $g_H(3.6)=8.17>c_H=6$. The high-cost type still prepares. Entry returns to a floor only if $g_H(r)<c_H$, that is $r>7.97$. At $r=8.5$ entry is $\tfrac13\rho+\tfrac13\rho+0=0.1667$, **below** $\rho$. The paper's claim "entry returns to $\rho$" rests on the floor $e\ge\rho$. Without the floor, a stronger incumbent can push entry below $\rho$.

**C7 (analytical for pure profiles, confirmed by a scan; endogenous buy-only).** For $\lambda<1$ the entry jump breaks the BNS–SNB symmetry. Take $r_1$, where the high-cost entry threshold is $\tau=0.705$, and $\lambda>2-1/\tau\approx0.58$. Then the posterior $1/(2-\lambda)$ at $X=1$ exceeds $\tau$, and $e=1$ there.

- In BNS, type $\ell$ deviates to sell. Its flows are $X=-1$ (posterior $(1-\lambda)/(2-\lambda)$, $e=\rho$), $X=0$ (posterior $1/2$) and the off-path $X=-2$. BNS needs $k\ge\rho\Delta_T[\tfrac12\cdot\tfrac13+\tfrac13\tfrac{1-\lambda}{2-\lambda}]$ for $\ell$, and $k<\rho\Delta_T/3$ for $h$.
- In SNB, type $h$ deviates to buy. At $X=1$ its residual is $\Delta_T(1-\lambda)/(2-\lambda)$ with $e=1$. SNB needs $k\ge\rho\Delta_T/6+\Delta_T(1-\lambda)/(3(2-\lambda))$ for $h$, and $k<\rho\Delta_T/3$ for $\ell$.
- Both conditions hold for SNB only if $(1-\lambda)/(2-\lambda)<\rho/2$, that is $\lambda>0.857$ at $\rho=0.25$. So SNB is empty for $\lambda\in(0.582,0.857]$.

The scan (`profiles.py`, $r_1$, Intuitive Criterion beliefs) agrees. T holds below $k/\Delta_T\approx0.04$–$0.07$ (the cutoff depends on $\lambda$). **BNS alone** holds on the whole partial-trade region for $\lambda=0.6,\,0.8,\,0.85$. For $\lambda=0.9$ and $0.95$, SNB returns on the upper part of the region ($k/\Delta_T\ge0.072$ and $\ge0.058$) and BNS is alone below it. At $\lambda=1$ and at $\lambda=1/2$ both exist on the same interval. The window in which buy-only is the unique partial-trade outcome is therefore $\lambda\in(0.58,0.857]$ at the benchmark. It lies inside the C5 floor condition $\lambda<0.883$. This is the same direction of asymmetry as in EGJ (Section II.C, p. 3782: feedback widens the BNS range and narrows the SNB range), generated here by a different channel, the entry jump. Pure strategies only; mixed strategies are not examined.

### 3.3 Answers to (a)–(d)

**(a) The most conventional discrete specification.** EGJ's trading block. State and order set as in Tables 2.1–2.2: noise $z\in\{-1,0,1\}$ with equal probabilities; informed trader present with probability $\lambda<1$; order $s\in\{-1,0,1\}$; cost per unit traded, the same in both directions; indifferent means no trade; MM sees $X=s+z$ and sets $P=E[V\mid X]$; perfect Bayesian equilibrium with the Intuitive Criterion off path; pure-strategy classification NT, T, BNS, SNB. GG use the same noise. For this paper's purpose the one change is that the challenger sees the price, not the flow (see (c)).

**(b) Off-path flows.** Three techniques appear.

- Intuitive Criterion. EGJ use it for the belief at $X=\pm2$ (the speculator knows the state). GG use it in Prop. 3.
- Select an equilibrium in which all flows are on path. GG do this in fn. 12.
- Full-support noise, so no flow is off path. BKT (fn. 11), DGG (normal noise) and Edmans (2009, exponential noise) do this.

The current paper's Laplace noise uses the third technique: every flow is on path. A discrete version gives this up and needs a belief rule. A one-directional order set does **not** remove the problem (C2). It removes it in the trading equilibrium. One flow stays off path in the no-trade equilibrium, which is the equilibrium of Prop. 2(i). That flow's belief is fixed in one line by dominance (C3) and moves the no-trade cutoff by a factor $3/2$ (C4), so the author must state the rule.

**(c) Price versus flow.** In every discrete model I read, the decision maker sees the flow (EGJ, GG; BKT is continuous). DGG, BGP and GOY have the decision maker see the price. DGG report that with the price, other equilibria arise where the MM sets $P=V_0$ on a larger set of flows (p. 883), and that the Lemma 1 equilibrium is the only one that survives if the firm sees order flow. BGP find multiple equilibria and, for poor agent information, no equilibrium when the agent sees the price (Section 2.4; Appendix B, Prop. 7). EGJ assume the manager sees $X$ to avoid these equilibria (Section I.B, p. 3775); their fn. 7 argues that managers can see trading quantities. The difficulty is a circle: the price depends on the decision, and the decision depends on the price. When the price is flat in some range of flows, a pooling price can be self-fulfilling.

For this paper the circle is already closed by Prop. A.2, **if** the floor holds (C5). In the discrete model the floor needs $c_L\le g_L$ (two-sided) or buy-only with $\lambda<1$. So the author has two options: (i) prove a discrete analog of A.2 under the floor (the proof is one line, C5), or (ii) assume the challenger sees $X$ and cite EGJ (p. 3775 and fn. 7). Option (i) keeps the paper's assumption and the paper's information structure. Option (ii) changes the information structure and loses the "price" story that point 3 of the supervisor's list probes.

**(d) Recommendations and positioning sentences.** See Section 7.

## 4. What changes relative to the current paper

| Item in the paper | Discrete version |
|---|---|
| Eq. (2): Laplace noise, $q\in[-1,1]$ | Three-point noise; order set $\{-1,0,1\}$, $\{0,1\}$ or $\{-1,0\}$. |
| Eq. (8), Prop. A.1: $m\le\mu_X\le M$ | **Fails.** Posteriors are exact (C1). $M=1$ at revealing flows. $m=0$ except in buy-only with $\lambda<1$, where $m=(1-\lambda)/(2-\lambda)$. |
| Prop. A.2: price sufficiency | **Survives under a floor** (C5). Fails without it. |
| Eq. (9): $P_r(\mu)$ and eq. (11) residuals | **Survive** pointwise. At revealing flows $A=0$, so the bound $\rho m\Delta_T\le A$ fails. |
| Global order bound (A.6) | **Not needed.** The order set is finite. A one-step deviation check suffices. |
| Closed forms (12): $x^*,\alpha_H,\alpha_L,E,O_H$ | **Replaced** by finite sums, $E=\sum_X\Pr(X)\,e(\mu_X)$ (C6). |
| Tie rule at $r_C$ (A.14) | The tie rule at $B(\mu_X)=c_H$ remains, but now at an atom. Plateau mass is positive by construction. |
| Prop. A.4 (no trade iff $\rho\Delta_T/2\le k$) | Becomes $k\ge\rho\Delta_T/3$ at $\lambda=1$ under the Intuitive Criterion (C4). |
| Prop. 2(i), (ii) | Analogs hold with single cutoffs (C6). |
| Prop. 2(iii) | **Fails at $r_2=3.6$.** Needs $r>7.97$. Entry then falls below $\rho$ unless $c_L\le g_L$ (C6). |
| Prop. A.3 (fixed experiment) | Not examined. |

## 5. Numerical diagnostics

The brief asks for a table in place of a numerical example. Two print-only scripts back the diagnostics. Both run with `.venv/bin/python` and have no assertions.

- `audit/alex_meeting_2026_10_21/scripts/Q2_discrete_literature/flows.py`: flow-by-flow posteriors (C1), benchmark objects $g_L,g_H,B(0),B(m),B(1/2),\tau$, pooling check (C5), buy-only floor, $\lambda=1$ thresholds and entry (C6).
- `audit/alex_meeting_2026_10_21/scripts/Q2_discrete_literature/profiles.py`: scan over $k/\Delta_T$ of the pure profiles NT, T, BNS, SNB at $r=3$ for $\lambda\in\{1,0.95,0.9,0.85,0.8,0.6,0.5\}$, with Intuitive Criterion beliefs (C6, C7).

## 6. Open issues and risks

- **Unread sources.** Glosten and Milgrom (1985), Kyle and Vila (1991), Khanna and Sonti (2004) and Diamond and Verrecchia (1987) are unverified. Do not cite details beyond the abstracts without reading them.
- **Versions.** EGJ: accepted manuscript with AER page numbers. GG: published. DGG: published. BKT: working paper; the journal version may differ. Edmans (2009): repository copy; I read Section I only.
- **EGJ Online Appendix.** I did not read B.2 (initial stake) or Appendix A. Statements about the stake rest on the main text (pp. 3787–3788).
- **Pure profiles only.** C6 and C7 check pure profiles at one vector. Mixed strategies may add equilibria (GG's results are in mixed strategies).
- **Belief rule.** I used the Intuitive Criterion. D1 and other refinements are not examined. Only C3 and C4 depend on the rule.
- **Revealing flows and the investor's residual.** At a revealing flow the residual is zero, so the investor never gains there. This is the reason $e(1/2)$ appears with a factor $1/3$ in C6. If the author expects "entry above $\rho$" as a general result, C6 shows it needs $c_L$ low or the floor.
- **Interaction with point 4.** A discrete version with a flow that reveals $\ell$ requires $c_L\le g_L(r_1)$, except in buy-only with $\lambda$ below the bound in C5. With $\ell=1$ as the unit, $g_L<1/2$, so $c_L=1$ is incompatible with a discrete version that has a flow revealing $\ell$. This is a cross-memo flag for the normalization question.
- **Interaction with point 3.** In EGJ the equilibrium shape does not change with a positive stake (p. 3787–3788; text only). The paper's $t_L>t_0$ means an $\ell$ investor with a stake may want to buy. Not examined here.
- **Corrective versus amplifying action.** EGJ's asymmetry (buying more profitable than selling) depends on the real decision being corrective (p. 3788). C7 shows an entry-based asymmetry for $\lambda$ in $(0.58,0.857]$ at the benchmark. Whether it is the same mechanism is a question for eq. (11): $A_H=e\Delta_T(1-\mu)$, $A_L=e\Delta_T\mu$, with $e$ rising in $\mu$.

## 7. Recommendation

In priority order.

1. **Use EGJ as the template.** Cite EGJ (2015) and GG (2008) for the three-point noise, the order set, the cost per unit traded, the tie rule and the perfect Bayesian concept. It is the closest paper on every axis the brief fixes.
2. **Set $\lambda<1$.** EGJ (p. 3787) say $\lambda<1$ is necessary for non-revealing interior flows. With $\lambda=1$, every flow reveals the state or equals the prior (C1).
3. **If you shut off one direction, choose buy-only.** It keeps the posterior floor $(1-\lambda)/(2-\lambda)$ and Prop. A.2 as written when $\lambda<0.88$ at the benchmark (C5). It is also the unique partial-trade outcome, without any restriction, for $\lambda\in(0.58,0.857]$ at the benchmark (C7). That window lies inside the floor condition. Sell-only has floor 0 for every $\lambda$.
4. **Keep the challenger on the price.** State the floor as an assumption and prove the discrete A.2 in one line (C5). Cite DGG (p. 883) and EGJ (p. 3775, fn. 7) to show that the alternative (flow observation) is common, but is not needed.
5. **State the off-path belief.** Use the Intuitive Criterion. Give the one-line dominance proof (C3). Report that the no-trade cutoff depends on it (C4).
6. **Choose the cost normalization with the discrete model in view.** Use $c_L=0$ or $c_L\le g_L(r_1)$. Keep $c_L=1$ only with Laplace noise.
7. **Rewrite Prop. 2(iii).** In the discrete model entry does not return to $\rho$ at $r_2=3.6$ (C6). Either move $r_2$ above 7.97 or state the result in terms of the revealed-$h$ gross profit $g_H(r)$ against $c_H$.

Positioning sentences the author can use:

> "We model the trading stage in the discrete form of Edmans, Goldstein and Jiang (2015) and Goldstein and Guembel (2008). The noise trader buys, sells, or does not trade one unit, each with probability 1/3. The informed investor, present with probability $\lambda$, trades the same unit or stays out. The market maker sees the total flow, which takes five values, and sets the price equal to the expected terminal value. The challenger sees only the price, and the price identifies the posterior because the low-cost type prepares at every posterior the flow can produce."

If the author uses buy-only:

> "Short sales are shut off, as in Edmans (2009). For intermediate presence probabilities, buy-only trade is also the unique partial-trade equilibrium of the two-sided game, in the way that buy-not-sell trading arises in Edmans, Goldstein and Jiang (2015)."

The second sentence is supported by C7 (numerical diagnostic at the benchmark) and needs the author's own check before it is used.

## 8. Plain summary

The supervisor asks whether the paper can use a discrete trading model. The standard choice is the model of Edmans, Goldstein and Jiang (2015). A noise trader buys, sells, or does not trade one unit with probability one third each. An informed investor, present with some probability, trades one unit or stays out. The market maker sees the total order flow and prices the stock at its expected value. Goldstein and Guembel (2008) use the same noise. Papers with continuous noise, such as Dow, Goldstein and Guembel (2017), have the decision maker watch the price and report a problem with self-fulfilling prices.

For this paper the discrete model needs three decisions. First, the investor should be present with probability below one. Otherwise every order flow either shows the true value or says nothing. Second, shutting off short sales does not remove all off-path flows. One flow stays off path in the no-trade case. A short argument fixes the belief there, and the belief changes the no-trade cutoff by a factor of 3/2. Third, the challenger still sees only the price. The paper's price result survives if the low-cost challenger prepares after every possible order flow. That needs a low cost for the low-cost type, or a buy-only menu with presence probability below 0.88.

At the benchmark, the discrete model keeps the first two parts of the main result. It does not keep the third. Entry does not return to the base rate at the strong incumbent in the paper, and it can fall below it.

I could not read four of the papers in full. Treat claims about them as unverified.
