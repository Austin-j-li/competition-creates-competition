# Q2 (economic side): why Laplace noise, and how to present it

Memo to the author. Meeting of 21 October 2026, supervisor point 2.
Scope: the economic justification of the Laplace density and the literature around it.
The technical side (proof steps, discrete variants) is in other memos.
Script: `audit/alex_meeting_2026_10_21/scripts/Q2_laplace_economic/laplace_economic.py` (print-only).

**How I checked sources.** I had bibliographic records, abstracts, and short summaries. I had no full texts, and I could not fetch pages. So I tag every source:

- **[R]** I saw the bibliographic record and the abstract or a summary of it. I did not read the full text.
- **[S]** The claim comes from a secondary source that quotes the paper.
- **[U]** Unverified. I cite it from memory. Do not cite it before you check it.

No claim below rests on a page or section that I read. If you cite a paper, open it and confirm the exact result first.

---

## 1. Question and reading

The supervisor says that Laplace noise is "largely unconventional" and asks for "very very clear justification" from the technical and the economic side. This memo covers the economic side:

- (a) Microfoundations that produce a Laplace law for net noise demand.
- (b) What the empirical literature says about the distribution of order imbalance and returns.
- (c) Theory papers that use Laplace noise or bounded likelihood ratios.
- (d) How to frame Laplace as a member of a class, not as a special assumption.
- (e) A paragraph for the paper and a sentence for the introduction.

My answer in one line: **the economics needs one property, that no order flow is conclusive. This property defines a large class of noise laws. Laplace is its extreme member, and the Gaussian law is outside it.**

---

## 2. Formal setup

Notation follows the paper.

- Orders $q\in[-1,1]$. Flow $X=q+Z$. Noise $Z$ has density $f$. Laplace: $f_b(z)=e^{-|z|/b}/(2b)$, $b>1$.
- Score: $s_f(z)=f'(z)/f(z)$.
- Class: $\mathcal F_b=\{f>0,\ f \text{ absolutely continuous},\ |f'|\le f/b \text{ a.e.}\}$. Equivalently, $\log f$ is $(1/b)$-Lipschitz.
- Any two orders differ by at most 2. Write $\varepsilon=2/b$.
- Laplace characteristic function: $\varphi(t)=1/(1+b^2t^2)$.
- Under full orders $(+1,-1)$ and equal priors, the posterior is $\mu_f(x)=f(x-1)/[f(x-1)+f(x+1)]$.
- Benchmark: $b=2$, so $E|Z|=2$ and $\Pr(|Z|\le1)=1-e^{-1/2}=0.393$.

A remark on the supervisor's phrase "clean linear posterior". Under full orders the log posterior odds are
$$\log\frac{\mu(x)}{1-\mu(x)}=\frac{|x+1|-|x-1|}{b},$$
which is linear in $x$ on $(-1,1)$ with slope $2/b$ and constant outside. The log odds are linear for the Gaussian law too. The Gaussian log odds are linear on all of $\mathbb R$, so they are unbounded. The posterior probability itself is not linear in the flow under either law. The Laplace log odds are clipped at $\pm 2/b$. The clipping is the useful feature.

---

## 3. Results

### 3.1 Microfoundations (task a)

**Claim 1 (analytical). Net noise demand is Laplace if noise buy volume and noise sell volume are independent exponential variables with the same mean $b$.**

Derivation. Let $B,S\sim\mathrm{Exp}(\text{mean } b)$ be independent and $Z=B-S$. For $z\ge0$,
$$f_Z(z)=\int_0^\infty \tfrac1b e^{-(s+z)/b}\,\tfrac1b e^{-s/b}\,ds=\frac{e^{-z/b}}{b^2}\cdot\frac b2=\frac{e^{-z/b}}{2b}.$$
By symmetry the same holds for $z<0$. In characteristic functions, $\frac1{1-ibt}\cdot\frac1{1+ibt}=\frac1{1+b^2t^2}$.

Numerical diagnostic (script, part A1): quadrature of the density at six points matches $f_b$ to 12 digits.

- Primitive: buy and sell volumes from noise traders are non-negative, memoryless, and have equal means.
- Plausibility: medium. Equal means means no systematic noise pressure in one direction. Exponential is the maximum-entropy law for a positive volume with a given mean (Claim 5), and it has a coefficient of variation of 1. Buy and sell volumes are likely positively correlated. A common volume factor $V$ gives $Z=V(E_1-E_2)$, a scale mixture of Laplace laws. By Claim 8(ii) this stays in the class if $V$ has a positive floor. If $V$ can approach zero, the score can become unbounded near $z=0$ (Claim 3).
- What breaks: unequal means. Then $Z$ is asymmetric Laplace (see Claim 7).

**Claim 2 (analytical). A Gaussian with an exponentially distributed variance is Laplace.**

Derivation. Let $Z\mid V\sim N(0,V)$ and $V\sim \mathrm{Exp}(\text{mean }\mu_V)$. Then
$$E e^{itZ}=E e^{-t^2V/2}=\frac1{1+t^2\mu_V/2}.$$
This equals $1/(1+b^2t^2)$ if and only if $\mu_V=2b^2$. The same argument with $V\sim\mathrm{Gamma}(\kappa,\text{scale }2b^2)$ gives $(1+b^2t^2)^{-\kappa}$. This is the symmetric variance-gamma law (Madan and Seneta 1990 [R]). The Laplace law is the case $\kappa=1$.

Numerical diagnostic (script, A2): quadrature agrees with $f_b$ to 12 digits.

- Primitive: the variance of noise flow is random with an exponential law. Two readings. (i) A random number of small noise orders. Given $N$ orders, the sum is nearly $N(0,Ns^2)$, so a roughly exponential $N$ gives a Laplace law. (ii) Random volatility.
- Plausibility: medium. Stochastic-volatility models give exponential-tailed returns. Drăgulescu and Yakovenko (2002) [R] show this for the Heston model. By standard facts, the stationary variance in the Heston model is gamma. It is exponential only at one parameter value (shape 1). I did not check this fact in a source [U]. A gamma shape below 1 puts too much mass near zero variance. Then the score is unbounded (Claim 3).
- Source for the representation: Park and Casella (2008, JASA) use it for the Bayesian lasso [R: the summary says the Gibbs sampler exploits it]. Kozubowski and Podgórski (2020, *The American Statistician* 74(4), 407–412) revisit it [R: record only].

**Claim 3 (analytical). Difference of two $\mathrm{Gamma}(\kappa,\text{scale } b)$ volumes, or a normal with $\mathrm{Gamma}(\kappa)$ variance: the score is bounded by $1/b$ if and only if $\kappa\ge1$.**

Derivation. The density is $f(z)\propto x^{\nu}K_{\nu}(x)$ with $x=|z|/b$ and $\nu=\kappa-\tfrac12$. The constant is $1/[\sqrt\pi\,\Gamma(\kappa)\,b\,2^{\nu}]$ (script, part E, checks it against a direct convolution at $\kappa=2$). The standard Bessel identity $\frac{d}{dx}[x^\nu K_\nu(x)]=-x^\nu K_{\nu-1}(x)$ gives, for $z>0$,
$$s_f(z)=-\frac1b\,\frac{K_{\nu-1}(x)}{K_\nu(x)}.$$
For fixed $x$, $K_\mu(x)$ increases in $|\mu|$. If $\kappa\ge1$ then $\nu\ge\frac12$ and $|\nu-1|\le\nu$, so the ratio is at most 1. It equals 1 at $\kappa=1$. If $\kappa<1$ then $0<\nu<\frac12$ and the ratio exceeds 1. It grows like $x^{2\nu-1}$ as $x\to0$, so the score is unbounded at the origin. I used these Bessel facts from memory, not from DLMF online [U]. The script computes the score on a grid. Result: the grid maximum is $0.5000$ at $\kappa=1$. For $\kappa\in\{1.5,2,3,6\}$ the grid values ($0.495,0.490,0.481,0.453$) lie below $0.5$ only because the score reaches $1/b$ in the limit $z\to\infty$. The bound $1/b$ holds and is not attained. For $\kappa=0.75$ and $0.6$ the grid maxima are $338$ and $11352$ and grow as the grid nears $z=0$.

Meaning: the Laplace law is the boundary of the "gamma volume" family. More dispersed volumes ($\kappa<1$) break the bounded likelihood ratio. Smoother volumes ($\kappa>1$) keep it.

**Claim 4 (analytical). Brownian noise demand evaluated at an independent exponential time is Laplace.**

Derivation. Let the cumulative noise flow be $\sigma W_T$ with $T\sim\mathrm{Exp}(\text{mean }\tau)$ independent of $W$. Given $T$, the flow is $N(0,\sigma^2T)$. By Claim 2 with $\mu_V=\sigma^2\tau=2b^2$, the flow is Laplace with $b=\sigma\sqrt{\tau/2}$.

Numerical diagnostic (script, A3, A4): with $\sigma=1.3$ and $\tau=4.7337$, a Monte Carlo of $4\times10^6$ draws gives $E|W|=2.0018$ (target 2), excess kurtosis $3.001$ (target 3), and tail probabilities within 0.0002 of the Laplace values.

- Primitive: noise orders arrive as a diffusion. The price is set at a memoryless random time. In a sale process this time is the first public event: a bid announcement, a filing, a leak, or an inspection. If events arrive at a Poisson rate $1/\tau$, the horizon is exponential.
- Plausibility: the best of the three, in my judgment. It needs no assumption about volumes. It needs a Poisson clock and independent noise flow. This is the same idea as subordination: Clark (1973, *Econometrica* 41(1), 135–155) [R] treats returns as Brownian motion in operational time. Ané and Geman (2000, *J. Finance* 55(5), 2259–2284) [R] use the number of trades as the clock. A comment by Murphy and Izzeldin disputes parts of that evidence [R: working-paper record]. I use these papers only for the time-change idea.
- Caution: in the model, the investor's order $q$ is one bounded order, and the noise is added to it. In the microfoundation, the investor trades over the same window. The model abstracts from this.

**Claim 5 (analytical). Laplace maximizes differential entropy among all densities with $E|Z|=b$.**

Derivation. Let $g$ have $E_g|Z|=b$. Then $0\le \mathrm{KL}(g\|f_b)=-h(g)-\int g\log f_b=-h(g)+\log(2b)+E_g|Z|/b$, so $h(g)\le \log(2b)+1=h(f_b)$. Equality holds only for $g=f_b$.

Numerical diagnostic (script, C): with $E|Z|=2$, entropy is 2.386 (Laplace), 2.367 (logistic), 2.369 (Student $t_3$), 2.338 (Gaussian).

- Primitive: market makers know only the mean absolute size of noise demand.
- Plausibility: low as a stand-alone argument. The Gaussian law has the same status with a variance constraint. The choice of constraint is not an economic primitive. Use this claim as support, not as the main argument.

**Claim 6 (analytical). Discrete analogue: a geometric number of noise orders gives a two-sided geometric law.**

Derivation. Let $N$ be geometric, $\Pr(N=n)=(1-s)s^n$. Each of the $N$ orders is $\pm1$ with probability $\frac12$. The generating function of the net sum is
$$\frac{1-s}{1-\frac s2(z+z^{-1})}=\frac{(1-\theta)^2}{(1-\theta z)(1-\theta z^{-1})},\qquad \theta=\frac{1-\sqrt{1-s^2}}{s},$$
because $\frac{s}{2}=\frac{\theta}{1+\theta^2}$ and $1-s=\frac{(1-\theta)^2}{1+\theta^2}$. The right side is the generating function of the difference of two independent geometric variables with ratio $\theta$. Its pmf is $\frac{1-\theta}{1+\theta}\theta^{|n|}$.

A Poisson count with an exponentially distributed intensity is geometric. So independent Poisson buy and sell counts with exponential intensities also give this pmf.

Numerical diagnostic (script, B1, B2): the pmf matches to 10 digits at $n=0,1,2,5,10,20$ ($s=0.9$), and at $n=0,1,3,7$ for two geometric counts ($q=0.55$).

Continuous limit. For a geometric sum with success probability $p$ and symmetric terms of variance $\sigma^2$, scale $t\to t\sqrt p$. The characteristic function tends to $1/(1+\sigma^2t^2/2)$, a Laplace law with $b^2=\sigma^2/2$. This is a sketch of the standard geometric-stability result. The literature name is "geometric stable laws" (Kozubowski and Podgórski [R], and Kozubowski and Rachev 1994 [U]).

- Primitive: the number of noise orders in the window is geometric. This is the natural discrete noise for the supervisor's discrete variant. The likelihood ratio of two flows is bounded by $\theta^{-|\Delta q|}$.
- Plausibility: medium. It needs a memoryless count, which Poisson arrivals with a random intensity give.

**Claim 7 (analytical). Asymmetric buy and sell noise.**

If buy volume has mean $b_B$ and sell volume has mean $b_S$, then $Z=B-S$ is asymmetric Laplace. Its score is $-1/b_B$ for $z>0$ and $+1/b_S$ for $z<0$. Under full orders,
$$M=\frac1{1+e^{-2/b_B}},\qquad m=\frac1{1+e^{2/b_S}}.$$
Numerical diagnostic (script, H, last lines): with $b_B=2$, $b_S=3$ the posterior limits are 0.731059 and 0.339244, equal to the formulas. Then $m\ne 1-M$. The paper's proofs use $M=1-m$ (Prop. A.1 uses equal priors and symmetry). A sale process may have net buy pressure, so this case matters (see section 6).

**Summary table (status of each story).**

| Story | Primitive | Plausibility for a target in a sale process |
|---|---|---|
| Exp − Exp | independent exponential buy and sell volumes, equal means | medium; volume floor needed |
| Normal, exponential variance | random number of small orders, or random volatility | medium; variance must not pile up near zero |
| Brownian at exponential time | diffusive noise flow, Poisson news clock | best; the clock is the first public event |
| Geometric count (discrete) | memoryless number of orders | medium; fits the discrete variant |
| Max entropy given $E\lvert Z\rvert$ | only mean absolute noise volume known | weak alone |

### 3.2 Empirical evidence (task b)

I report what each source supports, with its verification tag. I found no source that reports the shape of order imbalance or signed volume in terms of Laplace fits.

1. **Returns have heavier tails than the Gaussian law.** Cont (2001, *Quantitative Finance* 1(2), 223–236) [R]. Secondary quotes give a power-law-like tail with index between 2 and 5, and say the exact tail form is hard to pin down [S]. The same summary lists a figure of excess kurtosis from 2 to 50 for daily returns from a 1997 preprint, not from Cont [S]. I do not use the 2 to 50 figure.
2. **Power laws for returns and volume.** Gabaix, Gopikrishnan, Plerou and Stanley (2003, *Nature* 423, 267–270) [R] explain power-law fluctuations of returns, volume, and number of trades by the trades of large funds. The exponents (about 3 for returns, about 3/2 for volume) come from a 2007 *Physica A* abstract that the search returned [S]. I did not identify its authors. The follow-up is Gabaix et al. (2006, *QJE* 121(2), 461–504) [R].
3. **Laplace and asymmetric Laplace fits.** Kozubowski and Podgórski (2001, *Mathematical and Computer Modelling* 34(9–11), 1003–1021) [R]. The abstract says that asymmetric Laplace laws fit financial data, including currency exchange rates, better than the normal model. I did not see the fit tables. Madan and Seneta (1990, *J. Business* 63(4), 511–524) [R] start from the fact that normal tails are too light for daily returns.
4. **Exponential bulk at medium horizons.** Silva, Prange and Yakovenko (2004, *Physica A* 344(1), 227–235) [R]. For lags from about an hour to a month, more than 99% of the return distribution follows an exponential law. At shorter lags the tails are power laws. The crossover to the Gaussian law at long lags matches the Heston model. Drăgulescu and Yakovenko (2002, *Quantitative Finance* 2(6), 443–453) [R] show exponential tails in the Heston model and a good fit to the Dow Jones index for lags of 1 to 250 days.
5. **Order imbalance.** Plerou, Gopikrishnan, Gabaix and Stanley (2002, *Phys. Rev. E* 66, 027104) [R] define imbalance by trade counts and by shares, and study price response. The summary does not give a tail exponent for the imbalance. I do not cite one. Chordia and Subrahmanyam (2004, *JFE* 72, 485–518) [R] and Chordia, Roll and Subrahmanyam (2002, *JFE* 65, 111–130) [R] study autocorrelated imbalances and returns. They are not distribution studies.
6. **Large uninformed flows exist.** Coval and Stafford (2007, *JFE* 86(2), 479–512) [R]. Funds with large outflows sell, and funds with large inflows buy. The abstract reports price pressure in the stocks they hold in common, and profits for the liquidity providers on the other side. These trades follow investor flows, not news about the firm (my reading of the abstract). This is the right kind of evidence for the model's noise: large trades that carry no information about $\theta$.

**What the evidence supports.**

- The Gaussian law is a poor description. Returns and volume have fat tails. (Supported by items 1, 2, 3.)
- An exponential bulk at medium horizons is common. (Items 3, 4.)
- Large uninformed flows occur, so a big imbalance is not proof of information. (Item 6.)

**What it does not support.**

- No source shows that noise demand in a single stock is Laplace. Noise demand is not observable. Observed imbalance mixes informed and uninformed flow.
- At short horizons the far tail is a power law, which is heavier than exponential (items 1, 2, 4). A Laplace law understates the far tail.

**Implication.** The evidence argues against the Gaussian law and for the class of fat-tailed laws. It does not argue for Laplace in particular. This is why the class framing in section 3.4 is the right one. The two facts fit together as follows. If $f\in\mathcal F_b$ then $f(z)\ge f(0)e^{-|z|/b}$ (Claim 8 below, part iii). So the class contains only laws with tails at least as fat as an exponential. Power-law tails satisfy this.

### 3.3 Theory literature (task c)

I ran several searches. I looked for Laplace or double-exponential noise in Kyle-type models, in feedback models, in global games, and in microstructure models in general. **I found no paper in these fields that uses Laplace noise for noise trading** (numerical diagnostic: a search result, not a proof of absence). The device appears in neighbouring fields. The nearest economic-theory antecedent is bounded private beliefs.

| Paper | Tag | What it uses the device for |
|---|---|---|
| Smith and Sørensen (2000), "Pathological outcomes of observational learning", *Econometrica* 68(2), 371–398 | [R] | Heterogeneous-preference social learning. The working-paper abstract says wrong herds occur if and only if private signals have uniformly bounded strength [R]. Bounded likelihood ratio is the same property as the paper's eq. (8). Here it limits what the price can reveal. |
| Acemoglu, Dahleh, Lobel, Ozdaglar (2011), "Bayesian learning in social networks", *REStud* 78(4), 1201–1236 | [R] | Unbounded private beliefs give asymptotic learning in most networks. Bounded beliefs do not, with exceptions. |
| Dwork, McSherry, Nissim, Smith (2006), "Calibrating noise to sensitivity in private data analysis", TCC 2006, LNCS 3876, 265–284 | [R] | Laplace noise scaled to sensitivity gives bounded output likelihood ratio (differential privacy). I did not see the $e^\varepsilon$ statement in the text. The statement follows from eq. (8) with $\varepsilon=2/b$ and the sensitivity of the order range equal to 2 (analytical). So the paper's eq. (8) is exactly $\varepsilon$-differential privacy of the investor's order, with $\varepsilon=2/b$. For the pair of full orders, Laplace attains the bound at every flow with $|x|\ge1$. This is a mathematical fact. It is not an economic justification. Use it as a remark at most. |
| Kou (2002), "A jump-diffusion model for option pricing", *Management Science* 48(8), 1086–1101 | [R] | Double-exponential jump sizes. The abstract motivates it by the peaked, heavy-tailed return law and the volatility smile, and by a balance of realism and tractability. The memoryless property as the source of closed forms was not in the text I saw [U]. Kou and Wang (2004, *Management Science* 50) [R] extend it. This is a precedent in finance for choosing an exponential law for tractability and fit. |
| Madan and Seneta (1990); Madan, Carr, Chang (1998), "The variance gamma process and option pricing", *European Finance Review* (now *Review of Finance*) 2(1), 79–105 | [R] | Brownian motion with a gamma clock. The symmetric case with gamma shape 1 is the Laplace law (Claim 2, analytical). |
| Kotz, Kozubowski, Podgórski (2001), *The Laplace Distribution and Generalizations*, Birkhäuser | [R: record only] | The reference book. I could not confirm which chapter covers the mixture and geometric-sum results. |
| Kyle (1985) | cited in the paper | Gaussian noise, linear equilibrium. |
| Rochet and Vila (1994), "Insider trading without normality", *REStud* 61(1), 131–152 | [R: record only] | Non-normal distributions in a Kyle-type model. I did not see the abstract. |
| Bagnoli, Viswanathan, Holden (2001), "On the existence of linear equilibria in models of market making", *Mathematical Finance* 11(1), 1–31 | [R] | Necessary and sufficient conditions for linear equilibria. The abstract says they exist for some non-normal laws, including the uniform. |
| Nöldeke and Tröger (2004), Bonn Econ Discussion Paper 19/2004 | [R] | A linear equilibrium in the Rochet–Vila model exists if and only if the joint law of noise and payoff is elliptical. |
| Edmans, Goldstein, Jiang (2015), "Feedback effects, asymmetric trading, and the limits to arbitrage", *AER* 105(12), 3766–3797 | [R]; noise detail [S] | The discrete model. A snippet of the working-paper appendix shows a noise trader with $z\in\{-1,0,1\}$ with equal probability [S]. I could not confirm the meaning of $\lambda$. |
| Goldstein and Guembel (2008), "Manipulation and the allocational role of prices", *REStud* 75(1), 133–164 | [R]; noise detail from `memos/LIT_extracts.md` (full text read there, not by me) | Price feedback to investment. Section 2.2: two trade dates, noise $n_t\in\{-1,0,1\}$ with probability 1/3 each, and a market maker who sees $Q_t=u_t+n_t$. This is the conventional discrete noise, with no Laplace law. |
| Dow, Goldstein, Guembel (2017), "Incentives for information production in markets where prices affect real investment", *JEEA* 15(4), 877–909 | not seen by me; detail from `memos/LIT_extracts.md` only | Bounded speculator orders $x_i\in[-1,1]$ with Gaussian noise $n\sim N(0,\sigma^2)$, Section 2, eq. (1). This is the same bounded-order structure as the paper, with the Gaussian noise that the supervisor expects. The extract gives the posterior in its eq. (2). With Gaussian $\varphi$ the posterior tends to 0 or 1 as the flow grows (my reading). |
| Edmans, Goldstein, Jiang (2012), "The real effects of financial markets: the impact of prices on takeovers", *J. Finance* 67, 933–972 | [R] | This is an empirical paper, not a model. Do not cite it as a modelling precedent for noise. |

How the findings read for the supervisor:

- No microstructure paper I found uses Laplace noise. The supervisor's concern is fair.
- The property used (bounded likelihood ratio, or bounded private beliefs) is standard in learning theory. There it is the benchmark case where learning stays incomplete.
- The Gaussian law is the default in continuous Kyle models because of linearity. The existence literature (Bagnoli et al.; Nöldeke and Tröger) shows that linearity in the price rule is special to some laws. This model does not need a linear price rule.
- Kou (2002) is a precedent in finance for an exponential law chosen for tractability and fit.

### 3.4 Robustness framing (task d)

**Claim 8 (analytical). Properties of the class $\mathcal F_b$.**

(i) $f\in\mathcal F_b$ if and only if $f(z+\delta)\le e^{|\delta|/b}f(z)$ for all $z,\delta$. Proof: $\log f$ is absolutely continuous with $|(\log f)'|\le1/b$, so integrate. Hence any two orders have a flow likelihood ratio in $[e^{-2/b},e^{2/b}]$, which gives $m\le\mu_X\le M$ with the paper's $m,M$.

(ii) Closure. A mixture $\int f_\theta\,d\nu(\theta)$ of members is a member. A convolution $f*g$ with $f\in\mathcal F_b$ and $g$ any density is in $\mathcal F_b$. Proof: $|(f*g)'|=|f'*g|\le (f/b)*g=(f*g)/b$. The mixture proof is the same with the integral over $\theta$.

Numerical diagnostic (script, F): Laplace(2) + N(0,1) has $\sup|s|=0.50001$ (the excess over 0.5 is grid error). A mixture of Laplace scales (2, 3, 4) has $\sup|s|=0.386$. An asymmetric Laplace with means 2 and 3 has $\sup|s|=0.500$.

(iii) Tails. Every $f\in\mathcal F_b$ satisfies $f(z)\ge f(0)e^{-|z|/b}$. The class contains only laws with tails at least as fat as an exponential.

(iv) Members. Laplace($b$): $|s|=1/b$ a.e. (extreme). Logistic with scale $b$: $|s|=|\tanh(z/2b)|/b<1/b$. Student $t_\nu$ with scale $s_0$: $|s|=(\nu+1)|z|/(\nu s_0^2+z^2)$, with maximum $(\nu+1)/(2s_0\sqrt\nu)$ at $|z|=s_0\sqrt\nu$. So $s_0=b(\nu+1)/(2\sqrt\nu)$ gives $\sup|s|=1/b$. Cauchy ($\nu=1$) has $s_0=b$. Variance gamma with $\kappa\ge1$ (Claim 3). Asymmetric Laplace with $b=\min(b_B,b_S)$. Any Gaussian convolved with a member. The script confirms the Student-$t$ maximum on a grid ($0.50000$ for $\nu=1,3,5$).

(v) Non-members. The Gaussian law ($|s|=|z|/\sigma^2$ is unbounded). Any law with bounded support (the likelihood ratio is infinite at the edges). Any law whose tails are lighter than exponential.

(vi) Extremality. Let $f\in\mathcal F_b$ be symmetric. Under full orders,
$$\Big|\log\frac{\mu_f(x)}{1-\mu_f(x)}\Big|\le\frac{\min\{2|x|,2\}}{b}=\Big|\log\frac{\mu_{f_b}(x)}{1-\mu_{f_b}(x)}\Big|.$$
Proof. By symmetry $\log f(x-1)=\log f(1-x)$. For $0\le x\le1$ the points $1-x$ and $1+x$ are $2x$ apart, so the Lipschitz bound gives at most $2x/b$. For $x\ge1$ the points $x-1,x+1$ are 2 apart, so at most $2/b$. The case $x<0$ follows by symmetry. $\square$

Numerical diagnostic (script, G, last lines): the gap between $|\text{log-odds}|$ and the envelope is $\le 2\times10^{-15}$ for Laplace and $0$ for logistic and Student $t$ with $\nu=1,3,5$.

So at a given $b$, **Laplace makes every flow as informative as the bound allows.** It sets the upper envelope for the posterior curve. For a non-member such as the Gaussian, the posterior goes to 0 or 1 (script, G: $\mu(40)=0.999997$ against $M=0.7311$).

**Claim 9 (numerical diagnostic, fixed profile). The size of entry depends on the noise law inside the class. Laplace gives the largest value in my examples.**

At the strong benchmark ($r_1=3$, $\tau=0.705$, full orders, same $b=2$ bound), the entry probability $E=\rho+(1-\rho)(\alpha_H+\alpha_L)/2$ is (script, part H):

| Noise law (sup score $1/b$) | Entry $E$ | Sup of posterior |
|---|---|---|
| Laplace | 0.522723 (paper: 0.522757) | 0.73106 |
| Logistic | 0.301511 (paper: 0.301509) | 0.73106 |
| Variance gamma, $\kappa=2$ | 0.252061 | 0.72975 |
| Student $t_5$ | 0.343130 | 0.73016 |
| Student $t_3$ | 0.374979 | 0.72906 |
| Student $t_1$ (Cauchy) | 0.358249 | 0.72361 |
| Gaussian ($E\lvert Z\rvert=b$, not in the class) | 0.367029 | 1.00000 |

The Laplace value differs from the paper by $3\times10^{-5}$, a grid error from the jump in the indicator. The logistic value agrees to $2\times10^{-6}$. This is a fixed-profile comparison, as in the paper's Figure 3. It is not an equilibrium check. I did not verify that full orders are optimal for the other laws. The Gaussian row is not a claim about Prop. 2; the proof route fails for it.

Reading: for every member the sign pattern needs only $\tau<\sup\mu_f$ (entry above $\rho$). The magnitude depends on where the mass sits. The benchmark numbers (0.52 against 0.25) are Laplace numbers. Laplace attains the bound $M$ on the whole half-line $x\ge1$. I did not prove that Laplace gives the largest entry for every $f\in\mathcal F_b$ (**conjecture**).

**Two cautions on the class statement.**

1. Prop. A.5 as printed says that $|f'|\le f/b$ is all that steps 1 to 5 of the proof use. I did not re-check the proof. With a general $f$, condition (A2) should use $M_f=\sup\mu_f$, and the closed forms (12) become an integral over the set $\{x:\mu_f(x)\ge\tau\}$.
2. For Student $t$, the posterior is not monotone in the flow. It rises, then falls back toward $\frac12$ in the far tail (script, G: $\mu=0.725$ at $x=5$, $0.549$ at $x=40$ for $t_3$). The set $\{\mu\ge\tau\}$ has two edges (script, H). Laplace and logistic are log-concave, so their likelihood ratio is monotone. If any proof step uses monotonicity of $\mu_X$ in $x$, restrict the class to log-concave members. This subclass still holds Laplace, logistic, and Laplace + Gaussian (convolution of log-concave densities is log-concave, a standard fact [U]). **Open:** the technical memo should check whether a step uses monotonicity.

Suggested statement for the paper (Section 5.1 or Appendix A.4): "Proposition A.5′. The conclusions of Proposition 2 hold for every noise density $f\in\mathcal F_b$, with $m,M$ replaced by $m_f,M_f$ in (A1)–(A3). Laplace is the member that attains $m,M$."
Status: **conjecture** until the technical check is done. The logistic proof already in the paper is a special case.

### 3.5 The strongest economic argument

**The economics needs one property: no order flow is conclusive.** Whatever size of imbalance the market maker sees, noise could have produced it. Formally, the likelihood ratio of any two feasible orders is bounded by $e^{2/b}$. This is an economic statement about noise demand. Large uninformed flows are common (fund redemptions, index and fund rebalancing, other traders with unrelated signals, arbitrage positions on the announced process). This list is my reasoning. Only the fund-flow case rests on a source I checked (Coval and Stafford 2007). In a sale process, any trader whose demand does not depend on $\theta$ counts as noise. Gaussian noise says the opposite: a flow 10 standard deviations out is near-certain proof of information. The evidence on fat tails (Cont; Gabaix et al.) contradicts this. The bounded-score class is exactly the class of laws whose tails are at least exponential. Laplace is its extreme member. It is the law where the bound holds at every flow, so it gives the cleanest closed forms.

### 3.6 Draft text (task e)

**Paragraph for Section 2.3 (about 240 words).**

> Noise demand has a Laplace density for one reason: no order flow is conclusive. For any two feasible orders, the likelihood ratio of a flow is at most $e^{2/b}$. So the price never shows the investor's information with certainty. The posterior bounds and the global trading bound use this property. It holds for every noise law whose log density is $1/b$-Lipschitz. The Laplace law is the extreme member of this class. The logistic law is another member, and Section 5.1 shows that the results hold under logistic noise. The Gaussian law is not in the class, because a Gaussian flow in the tail is nearly conclusive. Three standard models give a Laplace law. Net noise demand is Laplace if noise buy volume and noise sell volume are independent exponential variables with equal means. It is Laplace if it is Gaussian with an exponentially distributed variance, as with a random number of liquidity traders. It is Laplace if noise orders follow a Brownian motion that stops at an independent exponential time, such as the arrival of public news. In each case the law is the variance-gamma law of Madan and Seneta (1990) with unit shape. Returns and volume have fatter tails than the Gaussian law (Cont 2001; Gabaix, Gopikrishnan, Plerou, and Stanley 2003). Laplace laws fit returns better than the normal law (Kozubowski and Podgórski 2001). Large uninformed flows occur, as with fund fire sales (Coval and Stafford 2007).

(Each sentence has 25 words or fewer. The paragraph claims only what the paper proves: the posterior bounds, the global trading bound, and the logistic case. The wider class claim is a conjecture until the technical check is done; see Claim 9. Check every citation before use; see the tags in 3.2 and 3.3.)

**One sentence for the introduction (25 words).**

> Laplace noise is the extreme case of a class of noise laws in which no order flow is conclusive; logistic noise gives the same results.

(Once Prop. A.5′ is proved for the whole class, replace "logistic noise gives the same results" with "the results hold for the class".)

---

## 4. What changes relative to the current paper

- No proposition changes.
- Section 2.3 (after eq. 2): add the paragraph in 3.6. It replaces the one-line "The bounded likelihood ratios of this density limit the information that any order can reveal."
- Introduction: add the sentence in 3.6.
- Section 5.1 and Appendix A.4: restate Prop. A.5 for the class $\mathcal F_b$, after the technical check (Claim 9, caution 1 and 2). This is optional but it answers the supervisor directly.
- Section 5.1: add one line that the benchmark entry numbers are Laplace numbers and that other members give smaller entry at the same $b$ (Claim 9).
- Do not describe eq. (2) as "a linear posterior". Say "piecewise-linear log odds with a bounded range".

---

## 5. Numerical example

Script: `audit/alex_meeting_2026_10_21/scripts/Q2_laplace_economic/laplace_economic.py`. Run with `.venv/bin/python -I`. It takes about 8 seconds and prints only. It has these parts:

- A. Three microfoundations against $f_b$ at $b=2$ (quadrature and Monte Carlo).
- B. Discrete analogues.
- C. Entropy at $E|Z|=b$.
- D. Score bound and $m,M$ for Laplace, logistic, Student $t$, Gaussian.
- E. Variance-gamma score by $\kappa$.
- F. Closure under mixtures and convolution.
- G. Posterior curves and the log-odds envelope.
- H. Fixed-profile entry at the strong benchmark, and asymmetric Laplace limits.

Key printed values at $b=2$: $m=0.268941$, $M=0.731059$, $\tau=0.705$. Entry under Laplace 0.522723 (paper 0.522757); under logistic 0.301511 (paper 0.301509).

---

## 6. Open issues and risks

1. **No direct evidence of Laplace noise demand.** Noise demand is unobservable. Do not claim a fit. Claim a class. (Open.)
2. **Far tail.** Short-horizon returns and volume have power-law tails. Laplace is thinner there. Power-law members of the class give a non-monotone posterior (Claim 9). Whether the proof needs monotonicity is open.
3. **Volume floor.** A common random volume factor, or a gamma shape below 1, can make the score unbounded near zero (Claim 3). The class needs noise volume bounded away from zero. In the model, $b>1$ means typical noise exceeds the investor's maximum order. A quiet period would break the class. (Analytical.)
4. **Asymmetry.** With unequal buy and sell noise, $m\ne1-M$ (Claim 7). The paper's proofs use symmetry. A sale process may have net buy pressure. Open: restate A1–A3 with $m,M$ separate.
5. **Entry magnitudes depend on the law.** The headline numbers are Laplace numbers and form an upper envelope in my examples (Claim 9). A referee may say the noise law was picked to maximize the result. Report a second member in the main text. (Conjecture on maximality.)
6. **Gaussian noise.** The proof route fails (the bound $m=0$ makes A3 impossible). Whether Prop. 2 holds under Gaussian noise is open. I did not test it.
7. **Differential privacy remark.** It is a true mathematical equivalence, but economists will not take it as a justification. Use it, if at all, in a footnote.
8. **Verification.** I read no full text. All page-level claims are unverified. See the tags.

---

## 7. Recommendation

In priority order:

1. Replace the one-line justification in Section 2.3 with the paragraph in 3.6. Add the one-sentence version to the introduction. Check the citations first.
2. Restate the argument in the paper as a class statement. Say "no flow is conclusive". Present Laplace as the extreme member. Do not say "Laplace is realistic".
3. Ask the technical memo to confirm that Prop. A.5 extends to $\mathcal F_b$, and whether any step needs monotone likelihood ratios. If yes, restrict to log-concave members.
4. Report one more noise law in Section 5.1 (for example variance gamma or Student $t$) next to the logistic number, and say that Laplace sets the upper envelope. This answers the likely referee question in advance.
5. Lead with the Brownian-at-exponential-time story (Claim 4) for economic plausibility, and the exponential-volume story (Claim 1) for the simplest intuition. Put the entropy fact and the privacy remark in a footnote.
6. For the meeting: tell the supervisor that no Kyle-type paper I found uses Laplace noise. The property used is the bounded private belief of the learning literature. The Gaussian law is the one case that fails.
7. Before citing any source here, read the cited result in the full text.

---

## 8. Plain summary

The supervisor asked why the noise is Laplace. The best answer is that the model does not need Laplace in particular. It needs one idea: no order flow is conclusive. However large the imbalance, noise could have caused it. A Gaussian law breaks this idea, because a huge Gaussian imbalance is nearly proof of information. Real order flow and returns have fat tails, so the Gaussian law is the weaker choice.

Many laws keep the idea. These include the logistic law, Student-t laws, and any mix of them. Laplace is the extreme case. It makes each flow as informative as the bound allows. This is why it gives clean closed forms. It also means that the headline entry numbers in the paper are the largest in my examples. Other laws, such as the logistic, give smaller numbers. The direction of the result stays the same.

There are three simple stories that produce a Laplace law. (1) Noise buy volume and noise sell volume are independent exponential variables with equal means. (2) The noise is Gaussian, but its variance is exponential. (3) Noise orders follow a random walk that stops at a random time, such as the arrival of news. Story (3) fits a sale process best.

I found no paper in microstructure that uses Laplace noise. The same idea appears in the learning literature as bounded private beliefs, and Laplace noise is standard in privacy research and option pricing. I could not read full texts, so every citation needs a check before use. The paragraph in section 3.6 is ready for the paper.

---

## References (with verification tags)

- Acemoglu, D., M. Dahleh, I. Lobel, A. Ozdaglar (2011), "Bayesian learning in social networks", *Review of Economic Studies* 78(4), 1201–1236. [R]
- Ané, T., H. Geman (2000), "Order flow, transaction clock, and normality of asset returns", *Journal of Finance* 55(5), 2259–2284. [R]
- Bagnoli, M., S. Viswanathan, C. Holden (2001), "On the existence of linear equilibria in models of market making", *Mathematical Finance* 11(1), 1–31. [R]
- Chordia, T., R. Roll, A. Subrahmanyam (2002), "Order imbalance, liquidity, and market returns", *Journal of Financial Economics* 65, 111–130. [R]
- Chordia, T., A. Subrahmanyam (2004), "Order imbalance and individual stock returns: theory and evidence", *Journal of Financial Economics* 72, 485–518. [R]
- Clark, P. K. (1973), "A subordinated stochastic process model with finite variance for speculative prices", *Econometrica* 41(1), 135–155. [R]
- Cont, R. (2001), "Empirical properties of asset returns: stylized facts and statistical issues", *Quantitative Finance* 1(2), 223–236. [R], tail index [S]
- Coval, J., E. Stafford (2007), "Asset fire sales (and purchases) in equity markets", *Journal of Financial Economics* 86(2), 479–512. [R]
- Drăgulescu, A., V. Yakovenko (2002), "Probability distribution of returns in the Heston model with stochastic volatility", *Quantitative Finance* 2(6), 443–453. [R]
- Dwork, C., F. McSherry, K. Nissim, A. Smith (2006), "Calibrating noise to sensitivity in private data analysis", TCC 2006, LNCS 3876, 265–284. [R]
- Edmans, A., I. Goldstein, W. Jiang (2012), "The real effects of financial markets: the impact of prices on takeovers", *Journal of Finance* 67, 933–972. [R] (empirical)
- Edmans, A., I. Goldstein, W. Jiang (2015), "Feedback effects, asymmetric trading, and the limits to arbitrage", *American Economic Review* 105(12), 3766–3797. [R], appendix noise detail [S]
- Gabaix, X., P. Gopikrishnan, V. Plerou, H. E. Stanley (2003), "A theory of power-law distributions in financial market fluctuations", *Nature* 423, 267–270. [R]; exponents [S]
- Gabaix, X., P. Gopikrishnan, V. Plerou, H. E. Stanley (2006), "Institutional investors and stock market volatility", *Quarterly Journal of Economics* 121(2), 461–504. [R]
- Goldstein, I., A. Guembel (2008), "Manipulation and the allocational role of prices", *Review of Economic Studies* 75(1), 133–164. [R]
- Dow, J., I. Goldstein, A. Guembel (2017), "Incentives for information production in markets where prices affect real investment", *Journal of the European Economic Association* 15(4), 877–909. Not seen by me; model detail from `memos/LIT_extracts.md`
- Kotz, S., T. Kozubowski, K. Podgórski (2001), *The Laplace Distribution and Generalizations*, Birkhäuser. [R: record only]
- Kou, S. G. (2002), "A jump-diffusion model for option pricing", *Management Science* 48(8), 1086–1101. [R]
- Kou, S. G., H. Wang (2004), "Option pricing under a double exponential jump diffusion model", *Management Science* 50. [R]
- Kozubowski, T., K. Podgórski (2001), "Asymmetric Laplace laws and modeling financial data", *Mathematical and Computer Modelling* 34(9–11), 1003–1021. [R]
- Kozubowski, T., K. Podgórski (2020), "Gaussian mixture representation of the Laplace distribution revisited: bibliographical connections and extensions", *The American Statistician* 74(4), 407–412. [R: record only]
- Kozubowski, T., S. Rachev (1994), "The theory of geometric stable distributions and its use in modeling financial data", *European Journal of Operational Research* 74, 310–324. [U]
- Kyle, A. (1985), *Econometrica* 53. (cited in the paper; I did not check details)
- Madan, D., E. Seneta (1990), "The variance gamma (V.G.) model for share market returns", *Journal of Business* 63(4), 511–524. [R]
- Madan, D., P. Carr, E. Chang (1998), "The variance gamma process and option pricing", *European Finance Review* 2(1), 79–105. [R]
- Nöldeke, G., T. Tröger (2004), Bonn Econ Discussion Paper 19/2004. [R]
- Park, T., G. Casella (2008), "The Bayesian lasso", *Journal of the American Statistical Association* 103. [R: pages not checked]
- Plerou, V., P. Gopikrishnan, X. Gabaix, H. E. Stanley (2002), "Quantifying stock-price response to demand fluctuations", *Physical Review E* 66, 027104. [R]
- Rochet, J.-C., J.-L. Vila (1994), "Insider trading without normality", *Review of Economic Studies* 61(1), 131–152. [R: record only]
- Silva, A. C., R. E. Prange, V. M. Yakovenko (2004), "Exponential distribution of financial returns at mesoscopic time lags: a new stylized fact", *Physica A* 344(1), 227–235. [R]
- Smith, L., P. Sørensen (2000), "Pathological outcomes of observational learning", *Econometrica* 68(2), 371–398. [R]
