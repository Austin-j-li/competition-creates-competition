# Q1 literature: how the literature models what a bidder knows before it pays to enter

Workstream: Point 1, literature. Date: 21 October 2026.
Reading covered: both readings (N and C) from the brief, with the weight on Reading N.

## 1. Question and reading

The supervisor said that a two-point challenger value with prior 1/2 is unconventional. The supervisor suggested that the challenger's value come from one of several distributions, and that the challenger learns the distribution only when it receives information.

This memo answers four questions.

1. What do the closest papers assume that a bidder knows before it pays the entry cost? What do they say entry reveals?
2. Which framework matches the supervisor's suggestion? How does that framework treat asymmetric bidders in a second-price or English auction?
3. How do takeover and feedback models specify types?
4. What should the paper adopt, cite, and say?

Reading N (nature draws the distribution) is the main line. I note where Reading C (the challenger chooses the distribution) has, or does not have, a literature.

**How I checked sources.** I read papers online as text. I saved no file. Section 2 gives a source tier for each paper. The tiers are:

- **P**: I read the primary text (the published version or an accepted manuscript).
- **WP**: I read a working-paper version. The published version may differ.
- **S**: I know the paper only through the description in other papers I read, or from the abstract.
- **U**: I have the bibliographic record only. Treat the content claims as unverified.

## 2. Model-by-model comparison (replaces "Formal setup")

### 2.1 The three poles

Three information assumptions organize the entry literature. Gentry and Li (2014) and Roberts and Sweeting (2013) use the same labels.

| Pole | Name | What the bidder knows before entry | What entry reveals |
|---|---|---|---|
| S | Samuelson (1985) | Its own value, exactly | Nothing about its own value. Entry only commits it to bid. |
| LS | Levin and Smith (1994) | Only the common distribution of values | Its value. |
| AS | Affiliated-signal, selective entry | A signal $s$ that is correlated with its value. Beliefs are $F(v\mid s)$. | Its value. |

AS contains LS (the signal is independent of the value). AS approaches S when the signal becomes perfect. Gentry and Li (2011 working paper, Section 1) state both points. Roberts and Sweeting (2013, Section 2.1) state the same two limits.

### 2.2 Paper by paper

"Cost" is the entry cost. "Asym." says how the paper treats asymmetric bidders.

| Paper | Knows before entry | Value drawn from | Cost | Entry reveals | Auction | Asym. | Tier |
|---|---|---|---|---|---|---|---|
| Samuelson (1985), *Econ. Lett.* 17(1–2): 53–57 | Own value | Common distribution, independent across bidders | Paid after the bidder learns its value | Nothing new about own value | Procurement setting. I did not check the format. | Not checked | S |
| McAfee and McMillan (1987), *Econ. Lett.* 23(4): 343–347 | Only the distribution $F$ | $F$ with density on $[u_l,u_h]$, regular, independent | Fixed $k>0$. They read it as the cost of learning the item's worth or of preparing a bid. | The bidder "learns his valuation" $u$ (Section 2) | Optimal mechanism. First-price sealed-bid with reserve equal to the seller's value induces optimal entry. | Symmetric | P |
| Levin and Smith (1994), *AER* 84(3): 585–599 | Common information only (footnote 3) | All bidders draw from the same distribution (Assumption 3) | Fixed $c$. It covers developing private information, then preparing a bid. | The bidder's private estimate of the value | General mechanism. The equilibrium is symmetric and mixed in entry. | Identical bidders. Footnote 6 notes that asymmetric pure-strategy equilibria exist and sets them aside. | P |
| Ye (2007), *GEB* 58(1): 181–207 | A private preliminary estimate $X_i\sim F$ | After the cost, an updated estimate $S_i=X_i+Y_i$. A common-value variant also exists. | Fixed $c$ | The updated estimate | Indicative bidding against entry-rights auctions | Symmetric | S (described in Section 2 of Kagel, Pevnitskaya and Ye, a study of indicative bidding that I read; the abstract of Ye 2007 gives the rest) |
| Marmer, Shneyerov and Xu (2013), *J. Econometrics* 176(1): 46–58 | A private signal $S_i$, free of charge | $(V_i,S_i)$ affiliated, same joint cdf for all bidders | Fixed $k\ge 0$ | $V_i$ | First-price | "Ex ante symmetric" | WP (Feb 2011) |
| Gentry and Li (2014), *Econometrica* 82(1): 315–344 | A private signal $S_i$, normalized to $U[0,1]$ without loss | $(V,S)$ affiliated, continuous joint density | Fixed $c$ | $V_i$ | "RS auctions". The class includes first-price, Vickrey, English and Dutch. | "Ex ante symmetric" (Assumption 2) | WP (Aug 2011) |
| Roberts and Sweeting (2013), *AER* 103(5): 1830–1861 | A noisy signal $s=v\,e^{\varepsilon}$, $\varepsilon\sim N(0,\sigma^2)$ | Truncated log-normal values, independent across bidders, location differs by type | Type-specific $K_\tau$ | The exact value | Simultaneous second-price (English button) against a sequential mechanism | Two types. Claim 3 below. | P (NBER working paper w17624 read for the model; the AER pages read in part) |
| Bhattacharya, Roberts and Sweeting (2014), *RAND J. Econ.* 45(4): 675–704 | A signal $S_i$ of the cost $C_i$. The cost distribution given $s$ first-order dominates the one given $\tilde s<s$ (model section). | Conditional on the signal | Fixed $K$ | The cost | First-price with free entry against an entry-rights auction | I read the setup as symmetric. I did not check every footnote. | P |
| Gentry and Stroup (2019), *JFE* 132(2): 298–324 | A private signal $S_{ij}=V_{ij}\exp(\varepsilon_{ij})$. The noise-to-signal ratio $\alpha_j\in[0,1]$ measures pre-entry uncertainty. | $V_{ij}$ given $S_{ij}=s$ is log-normal with location $\alpha_j\mu_j+(1-\alpha_j)\ln s$ | Entry cost for bid preparation and diligence | The exact value | Ascending button auction in rounds. Each entrant meets the standing incumbent. Negotiation is the alternative. | Values are pair-specific. The position of the incumbent differs from that of the entrant. | P (accepted manuscript) |
| Quint and Hendricks (2018), *AEJ Micro* 10(2): 118–151 | A real-valued private signal $S_i$ (the "type") | $V_i$ given $S$. Types are independent across bidders. Values may be correlated given $S$. | Same $c$ for all | $V_i$ in due diligence | Indicative bids pick $n$ bidders. Second-price auction at the end. | Exchangeable bidders | P |
| Fishman (1988), *RAND J. Econ.* 19(1): 88–101 | The rival has no private information about the target value (as reported by Cornu and Isakov 2000) | I did not verify the value specification | Investigation cost | The target value | Preemptive bidding game | Not checked | S |
| Hirshleifer and Png (1989), *RFS* 2(4): 587–606 | The bidders are "initially uninformed" and must pay to learn "their independent valuations" (abstract) | I did not verify | Investigation cost, and a cost per overbid (Cornu and Isakov 2000) | The valuation | First bidder: preemptive bid or a lower bid that invites entry | Not checked | S |
| Daniel and Hirshleifer, *Rev. Finance* 22(5): 1631–1665 (2018) | Not read | Not read | Costly bids | Not read | Sequential bidding, jump bids | Not read | U |
| Bulow and Klemperer (1996), *AER* 86(1): 180–194 | The number of bidders is fixed. Footnote 7 says the paper does not model how the number is chosen. | Independent private values and affiliated signals | None in the main model | Not applicable | English auction against negotiation | Not applicable | P (footnote and abstract) |
| Compte and Jehiel (2007), *RAND J. Econ.* 38(2): 355–372 | An "informed" bidder knows $\theta_i$. An "uninformed" bidder knows only the distribution. The information state is private. | $\theta_i$ takes $K$ values, with general probabilities $f(\theta_k)$ (Section 2). Independent across bidders. | Cost $c$ to learn $\theta_i$ | $\theta_i$ | Second-price against ascending price | Informed against uninformed bidders | WP (Oct 2005) |
| Persico (2000), *Econometrica* 68(1): 135–148 | I could not read the model. Compte and Jehiel describe it as a comparison of the incentive to acquire information in first-price and second-price auctions with affiliated values. | Not verified | Not verified | Not verified | First-price and second-price | Not verified | U |

### 2.3 Notes on the table

- **Samuelson.** Levin and Smith (1994, footnote 7) call Samuelson's costs "interim": the costs "are not incurred until after each bidder learns his value". Gentry and Li, Marmer et al., and Roberts and Sweeting give the same reading. I did not read Samuelson's own text.
- **Compte and Jehiel.** Footnote 11 of the 2005 version gives a reason for a discrete value set: "there are only $K$ possible signals that a bidder may observe concerning his valuation, and each $\theta_k$ corresponds to an expected valuation given signal $k$". This is the one passage I found that justifies a discrete support on the auction side. The probabilities $f(\theta_k)$ are general. In their footnote 12, they say that a more general imperfect pre-auction signal adds no new insight ("No new insight is gained by doing so").
- **Menezes and Monteiro.** Their 1996 working paper studies bidders who see their values and then decide to enter. This is the S pole. Tier S, from the abstract. The published version (*Rev. Econ. Design* 2000) is unverified.
- **Gentry, Li and Lu (2017), *GEB* 105: 104–111.** This paper extends revenue equivalence to "arbitrarily selective" entry. Tier S, from the abstract.
- **Gorbenko and Malenko (2014), *J. Finance* 69(6): 2513–2555.** The paper already cites it (`main.tex`, line 252). It is a takeover model with two classes of bidders, strategic and financial. Each class has its own value distribution. The abstract says that the estimation uses each bidder's class, that strategic values are more dispersed, and that financial values move with aggregate conditions. This is the structure "class plus conditional value distribution" in the takeover literature. I have the abstract only (tier S). I did not read the model or check its auction format.
- **Bulow and Klemperer (2009), *AER*.** Gentry and Stroup say that this paper shows auctions beat sequential negotiations when bidders have no pre-entry information. They add that Roberts and Sweeting show the result "hinges" on that assumption. Tier S.

## 3. Results

Status labels follow the brief: **analytical** (I derived it), **conjecture** (I believe it, I did not prove it), **open**. This is a literature memo, so I add one label: **source** (stated in a paper I read; the tier from Section 1 is given). I computed nothing, so I use no **numerical diagnostic** label.

### Claim 1. The supervisor's suggestion is the selective-entry framework. [source + analytical]

The framework: a bidder holds pre-entry information $s$, its beliefs about the value are $F(v\mid s)$, it pays $c$, it learns $v$, and it bids. Gentry and Li (2014) call it the affiliated-signal (AS) model. Marmer et al. (2013) and Roberts and Sweeting (2013) call the same structure "selective entry". Gentry and Stroup (2019) use it for takeovers and call the information gap "pre-entry uncertainty".

Reading N is this model with a two-point signal. Let $s=j\in\{H,L\}$ with $\Pr(j=H)=\pi$, and let $F(\cdot\mid j)=G_j$. The supervisor's phrase, as the author reports it, is "choosing from a few different distributions, and only when they receive information can they actually know what distributions they end up at". Reading N matches it as follows: the distribution is fixed by $j$, the information (here the price) tells the challenger about $j$, and the value is drawn only after entry.

**The ordering assumption.** The literature has two forms.

- Affiliation of $(V,S)$ (Gentry and Li, Assumption 3; Marmer et al., Assumption 1).
- First-order dominance of the conditional distribution (Bhattacharya et al., model section: the distribution given $s$ dominates the one given $\tilde s<s$).

For a two-point signal, affiliation is the same as the monotone likelihood ratio. Derivation: write the joint density as $f(v,j)=\pi_j\,g_j(v)$. Affiliation requires $f(z\vee z')\,f(z\wedge z')\ge f(z)\,f(z')$ for all pairs. Pairs with the same signal hold trivially. Take $z=(v,L)$ and $z'=(v',H)$ with $v>v'$. Then $z\vee z'=(v,H)$ and $z\wedge z'=(v',L)$. The condition becomes $f(v,H)f(v',L)\ge f(v,L)f(v',H)$. Divide by $\pi(1-\pi)$ and the density of the signal. The result is $g_H(v)/g_L(v)\ge g_H(v')/g_L(v')$. So the ratio rises in $v$. This implies $G_H$ first-order dominates $G_L$, but the reverse does not hold. The brief's main assumption (first-order dominance) is therefore weaker than affiliation and matches the weaker of the two forms in the literature. [analytical]

### Claim 2. The current paper is the AS model with degenerate conditional distributions. [analytical]

Set $G_H=\delta_h$ and $G_L=\delta_\ell$. Then the class $j$ and the value $\theta$ coincide. "Learn the class" and "learn the value" collapse into one step. This collapse is what reads as unconventional. All AS papers separate the two steps.

**Bridge to the paper's objects.** In a second-price auction with reserve $p$ and independent private values, truthful bids are weakly dominant. So the paper's per-value objects carry over without change. Write $t(\theta)=E[\,1\{\max(R,\theta)\ge p\}\max\{p,\min(R,\theta)\}\,]$ and $g(\theta)=E[(\theta-\max\{p,R\})_+]$. Then $t_j=\int t\,dG_j$ and $g_j=\int g\,dG_j$.

I checked that this gives the paper's closed forms for the uniform incumbent. For example, with $\theta=\ell$:
$t(\ell)=\frac{p^2}{r}+\frac{\ell^2-p^2}{2r}+\ell\frac{r-\ell}{r}=\ell-\frac{\ell^2-p^2}{2r}=t_L$.
Also $g(\ell)=\frac{(\ell-p)p}{r}+\frac{(\ell-p)^2}{2r}=\frac{\ell^2-p^2}{2r}=g_L$.
For $\theta<p$ the challenger cannot win, so $t(\theta)=t_0$ and $g(\theta)=0$. The derivation workstream should use this bridge for the checks in the brief, Section 3.1. I do not attempt those checks here.

### Claim 3. Asymmetric bidders in a second-price or English auction. [source + analytical]

The supervisor said that asymmetric information would not cause a headache in a second-price auction. The literature agrees, and it shows where the difficulty moves.

1. **Stage 2 is easy.** With private values, each entrant bids its value. This is a dominant strategy and does not depend on beliefs about rivals. Roberts and Sweeting (NBER working paper, Section 2.2): "entrants know their values so it is a dominant strategy for each entrant to bid its value." Asymmetry in the value distributions then changes nothing in the bids. It changes only the entry decision.
2. **Entry is where asymmetry enters.** Roberts and Sweeting allow two bidder types. Types differ in the location of the value distribution. They use a type-symmetric equilibrium with one entry threshold per type. The threshold solves a zero-profit condition (their equation (1)).
3. **Multiplicity.** With two types, several entry equilibria can exist when the types are similar. Roberts and Sweeting choose the equilibrium in which the type with the higher mean values has the lower threshold. They report that this equilibrium is unique when the types differ only in location and the reaction functions are S-shaped. They solve the model numerically. I read this as a warning for Prop. 3 of the paper, where multiplicity already appears.
4. **Without selection.** Athey, Levin and Seira (2011), as reported by Roberts and Sweeting: in the type-symmetric mixed equilibrium with non-selective entry and asymmetric types, if the weaker type enters with positive probability, the stronger type enters with probability one. Tier S.
5. **Format matters under asymmetry.** Roberts and Sweeting (AER) say that with asymmetric bidders a seller may prefer a first-price auction with type-specific reserves to a second-price auction with one reserve. They give a numerical example. The AER page I read is cut off, so I do not give the exact statement. The paper keeps the second-price rule, so this point is a caution, not a result you need.
6. **Most selective-entry papers assume ex ante symmetric bidders.** Gentry and Li (Assumption 2), Marmer et al. and Quint and Hendricks (exchangeable) do. Levin and Smith set asymmetric equilibria aside (footnote 6).
7. **Closest to the paper's structure.** Gentry and Stroup model a standing incumbent and a sequence of entrants who meet it in an ascending button auction (their description of the sequential game). The entrant's choice rests on a private signal and the history. In the paper, the incumbent is already prepared, and the challenger decides on the basis of a public price. Compte and Jehiel (2007) have an asymmetry of information states (informed and uninformed bidders) in second-price and ascending auctions.

### Claim 4. Two features of the paper have no counterpart in the AS papers I read. [conjecture]

1. **The signal is public and comes from a third party.** In every AS paper I read, the signal is the bidder's own private draw, and the signals are independent across bidders. In the paper's benchmark, the challenger's own pre-entry information is of the LS type. The information about its value reaches it only through the stock price. An investor who observes the class $j$ shapes that price. In Section 5.3 of the paper, the challenger also holds a private binary signal $Y$ of accuracy $d$ about its value. There the challenger has an AS-type signal of its own, and the public price comes on top of it. So the mapping to the AS model is closer in Section 5.3 than in the benchmark. The benchmark is the clean case of a signal that is purely public.
2. **The signal is endogenous.** In the AS papers, the information structure is fixed. In the paper, the price depends on the investor's order, and market makers anticipate entry.

I found one nearby case of entry that depends on a public signal. In Roberts and Sweeting's sequential mechanism, later buyers see earlier entry decisions and bids. But those observations concern rivals, not the observer's own value.

A third, smaller difference: the cost $C$ arrives after the price and is private to the challenger. The AS papers I read use a cost that the bidder knows when it decides.

I did not find a paper with all of these features. My search was not exhaustive, so this is a conjecture, not a proof of novelty.

### Claim 5. In the feedback literature, a binary state with equal prior is conventional. In the auction-entry literature, it is not. [source]

This split is the main answer to the supervisor's remark.

| Paper (tier) | State or type | Prior | Noise or flow |
|---|---|---|---|
| Edmans, Goldstein and Jiang (2015), *AER* 105(12): 3766–3797 (P). Section I.A: "The prior probability that the state is $\theta=H$ is $y=\tfrac12$, which is common knowledge." | Binary, $H$ or $L$ | $1/2$, stated as given | Noise trader $z\in\{-1,0,1\}$ with equal probability. The speculator is present with probability $\lambda$, has no initial position, and pays $\kappa$ for a trade of $\pm1$. A speculator who is indifferent does not trade. These appear in Section I.B. |
| Goldstein and Guembel, *Rev. Econ. Stud.* 75(1): 133–164 (2008). I read only the 2002 working paper (WP). | State $\omega\in\{l,h\}$ with productivity $\mu_h>\mu_l$ | "Equal probability" | Noise trader order $n_t\in\{-1,1\}$ with equal probability. The speculator trades $\{-1,0,1\}$. The published version is not read. |
| Dow, Goldstein and Guembel, *JEEA* 15(4): 877–909 (2017). I read the 2007 WP. | Binary payoff $R_h$ or $R_l$ | "Equal probability" | Normal noise. Speculator orders in $[-1,1]$. |
| Kyle (1985), *Econometrica* 53(6) | Normal value | Normal | Normal. This is standard and I did not re-read it. |

Note on the brief: the brief puts the Edmans et al. noise specification in "Section 2.2". In the AER text it is Section I.B ("Trade in the Financial Market"). The state and prior are in Section I.A.

On the auction-entry side, every model in Section 2.2 that I could read uses a continuous value or signal (McAfee–McMillan, Levin–Smith, Gentry–Li, Roberts–Sweeting, Gentry–Stroup). The one exception is a $K$-point support with general probabilities (Compte–Jehiel). I found no auction-entry model with a two-point value and prior $1/2$. My search is not exhaustive.

The paper joins both sides. The investor's binary state and the 1/2 prior come from the feedback side. The same binary state is also the challenger's value. The second use is what the auction-entry reader finds unusual.

For takeover models I could not verify the type specification in Fishman (1988) or Hirshleifer and Png (1989). Do not cite them for a specification until the text is checked.

### Claim 6. Reading C has no direct counterpart. [source + open]

No paper in Section 2.2 lets the bidder choose the distribution of its own value before entry. The nearest are information-acquisition models, where the bidder chooses an experiment or a signal accuracy:

- Persico (2000), tier U.
- Compte and Jehiel (2007), where a bidder chooses whether to pay to learn its value.
- Bergemann and Välimäki, on information acquisition and efficient mechanism design (Compte and Jehiel cite it). Tier S, and I did not check the details.

These choose how much to learn. Reading C chooses which distribution to draw from. The second choice needs a model of why one distribution is better. In a second-price auction, the choice has a clear value: the challenger prefers the distribution with the higher expected $g_j$ net of its cost. A menu of FOSD-ordered distributions would always select the top element unless each element has a cost or risk attached. [conjecture] I do not recommend Reading C unless the supervisor confirms that meaning.

### Claim 7. The 1/2 prior has two defenses, and a general prior costs little. [conjecture for item 1; analytical for item 2]

1. In the Gentry–Li normalization, the signal is $S\sim U[0,1]$ without loss of generality. A class defined by "signal above or below the median" has prior exactly $1/2$. So a binary class with prior $1/2$ is a median split of the standard signal. [conjecture]
2. A general prior $\pi$ changes the posterior bounds in a direct way. The posterior is $\mu=\pi L/(\pi L+1-\pi)$, where the Laplace likelihood ratio satisfies $L\in[e^{-2/b},e^{2/b}]$. So $m_\pi=\pi e^{-2/b}/(\pi e^{-2/b}+1-\pi)$ and $M_\pi=\pi e^{2/b}/(\pi e^{2/b}+1-\pi)$. At $\pi=1/2$ this gives the paper's $m=1/(1+e^{2/b})$. [analytical]

## 4. What changes relative to the current paper

- **Equation (1) and Section 2.2.** The text says the challenger has value $\theta\in\{\ell,h\}$ "with equal prior probabilities". Under Reading N this becomes a class $j$ with prior $\pi$ and conditional distribution $G_j$. The current text is the case $G_j=\delta$. Nothing in the existing propositions is invalidated by a framing change alone.
- **Section 6.3 (value classes).** It is already a non-degenerate $G_j$ (uniform, half-width 0.05). The memo suggests moving this case from a robustness check to the main specification, or at least pointing to it in Section 2.2.
- **Introduction, lines 203–205 of `main.tex`.** The auction-entry paragraph cites Samuelson, McAfee–McMillan, Levin–Smith, Gentry–Stroup and Roberts–Sweeting. It does not say what the challenger knows before entry. One sentence on the three poles (Section 2.1) would place the paper.
- **References.** Missing from the bibliography: Ye (2007); Marmer, Shneyerov and Xu (2013); Gentry and Li (2014); Bhattacharya, Roberts and Sweeting (2014); Quint and Hendricks (2018); Compte and Jehiel (2007). Optional: Gentry, Li and Lu (2017); Bulow and Klemperer (2009).
- **Posterior bounds (eqs. 7–8).** They generalize with $\pi$ (Claim 7).
- **Proofs.** I did not examine the effect of a non-degenerate $G_j$ on the proofs of Props. 1, 2, A.2 and A.3. That is the derivation workstream.

## 5. Numerical example

Not applicable. This is a literature memo. I wrote no script.

## 6. Open issues and risks

1. **Source tiers.** Samuelson (1985), Ye (2007), Fishman (1988), Hirshleifer and Png (1989) and Athey, Levin and Seira (2011) are known only through other papers. Persico (2000) and Daniel and Hirshleifer (2018) are unverified. The brief dates Daniel and Hirshleifer to 1998. The journal record I found gives 2018 (*Review of Finance* 22(5)). I did not check whether a 1998 working paper exists, and I did not read the model. Goldstein and Guembel (2008) and Dow et al. (2017) were read in working-paper versions.
2. **Version differences.** For Gentry and Li, the 2011 working paper says that AS "nests" LS and "approaches" S as a limit. The published abstract says it nests both. Cite the published statement only after you check the final text.
3. **Search coverage.** I did not find an auction-entry model with a two-point value and prior $1/2$, or one with a public third-party signal. My search was not exhaustive.
4. **Referee risk.** A referee may say that the public signal turns the problem into information design by a third party. Claim 4 names the difference but does not answer this point.
5. **Multiplicity.** Roberts and Sweeting show multiple entry equilibria when types are close. The paper already has this in Prop. 3. A non-degenerate $G_j$ may add more.
6. **Closed forms.** The paper's closed forms (eq. 12) use two-point values. With a general $G_j$ they may not survive. The derivation workstream should report which ones do.

## 7. Recommendation

In priority order:

1. **Adopt Reading N in the selective-entry vocabulary.** Specify a quality class $j\in\{H,L\}$ with prior $\pi$ and a conditional value distribution $G_j$, with $G_H$ first-order dominating $G_L$. Keep the two-point values as the benchmark (the case $G_j=\delta$), and say so. Say that the monotone likelihood ratio is the form that matches affiliation, and that first-order dominance is enough for the rankings.
2. **Cite the poles and the framework.** Use Samuelson (1985) for the S pole and Levin and Smith (1994) for the LS pole. Use Gentry and Li (2014) for the formal definition of the AS model, Roberts and Sweeting (2013) for second-price and asymmetric types, Gentry and Stroup (2019) for takeovers, and Quint and Hendricks (2018) for due diligence. Use Compte and Jehiel (2007, footnote 11) to defend a discrete value set. Use Gorbenko and Malenko (2014), which the paper already cites, as the takeover-side example of a class with its own value distribution (check the model text first; I have the abstract only). Cite Edmans et al. (2015) and Dow et al. (2017) to defend the binary state with equal prior on the feedback side.
3. **Use these terms.** "Selective entry" and "pre-entry signal" (Roberts–Sweeting, Marmer et al.). "Affiliated-signal model" only if you assume affiliation. "Pre-entry uncertainty" (Gentry–Stroup). "LS pole" and "S pole". Say "preparation cost" and add "(entry cost in the auction literature)" once. Say "class" for $j$. Avoid "type" for $j$, because it also names the investor's information.
4. **Do not pursue Reading C** unless the supervisor confirms it. No auction-entry model has it (Claim 6).
5. **Check the unverified items** in Section 6 before the draft goes out.

**Text the author can use.** These are drafts. Edit them to fit the paper's voice.

> The challenger's problem fits the selective-entry framework (Samuelson 1985; Levin and Smith 1994; Gentry and Li 2014; Roberts and Sweeting 2013). A bidder holds pre-entry information that indexes the distribution of its value, and the entry cost reveals the value.
>
> Here the pre-entry information is the stock price. The price is public, and an investor who observes the quality class shapes it. The class plays the role of the signal, and the conditional distribution $G_j$ plays the role of $F(v\mid s)$.
>
> The two-point value in the benchmark is the case in which each $G_j$ is a point mass. Section 6.3 gives a case in which it is not.

## 8. Plain summary

The supervisor thought a two-point challenger value, with probability one half each, was unusual. I checked how the literature models a bidder who must pay to enter an auction.

There are three standard cases. The bidder knows its value before entry (Samuelson). It knows nothing but the distribution (Levin and Smith). Or it holds a signal that is correlated with its value (the selective-entry or affiliated-signal model of Gentry and Li, and of Roberts and Sweeting). The third case matches the supervisor's idea. The signal picks the distribution, and paying the cost reveals the value.

The paper is this third case with one change. The pre-entry signal is the stock price, which is public. The paper also makes each class carry exactly one value, so the class and the value are the same thing. That is why it looks odd to an auction reader.

The one-half prior is normal in the feedback literature. Edmans, Goldstein and Jiang (2015) and the Goldstein papers use it. Auction-entry papers use continuous values. I found no auction-entry paper with a two-point value.

Second-price auctions make asymmetric bidders easy. Each bidder bids its value. Asymmetry matters only for the decision to enter. Roberts and Sweeting show how to handle this with type-specific thresholds.

I recommend that the paper adopt this framework: a class with a general prior and a value distribution for each class. The current model is the special case in which each distribution is a single point. I could not verify a few references. Section 6 lists them.
