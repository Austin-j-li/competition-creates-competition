# Flash cards for the upgrade talk: a holistic scan

Paper: "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders", order-slot version.
Talk: 19 main frames plus backups, with a full spoken script.

## How to read this report

- Each claim about the paper gives a file and a line.
- Paths start at the project root.
- The short names are these. Talk: `overleaf/slot/slides.tex` and `overleaf/slot/slides_script.md`.
- Paper: `overleaf/slot/sections/` and `overleaf/slot/appendix/`.
- Numbers: `overleaf/slot/numbers.tex`.
- "[benchmark]" marks a use of example numbers. The claim needs the number at that place.
- "New, not in the paper" marks a new step. The step shows its working.
- Older files use older words. One older word names the potential rival bidder. One older word names the informed trader.
- This report uses the talk words only: incumbent bidder, then incumbent; potential rival bidder, then rival.
- Faculty points get a verdict for the slot version: still applies, partly applies, or does not apply.

## 1. The core: what he must own

The list ranks ideas for speech, not for print.
Each item gives the reason for its rank.
Own the idea in words first. Add the algebra second.

**1. One value, two claims.**
Say $t(\theta)+g(\theta)=\theta$ for $\theta\ge p$ without notes.
Say who gets each part at one draw of $R$.
Reason: every later step uses this split.
Source: `overleaf/slot/sections/03_competition_information.tex:10`.

**2. Strength moves the split.**
A stronger incumbent never raises $B(\mu)$ at a fixed belief.
Under the class ranking, it never narrows $\Delta_T$.
Reason: this pair is the whole tension in the talk.
Source: `overleaf/slot/sections/03_competition_information.tex:36`.

**3. The price carries news about the synergy class.**
The price can reveal the belief $\mu(x)$.
The price never reveals the synergy class.
Reason: one slip here ends trust in the market part.
Source: `overleaf/slot/sections/03_competition_information.tex:90`.

**4. No order can settle the class.**
A liquidity trader can place each order in each class.
Each belief stays in $[m(\pi),M(\pi)]$.
Reason: the band gives the informed trader a gain after each order.
Source: `overleaf/slot/sections/02_model.tex:145`.

**5. A correct order earns entry times spread times doubt.**
Use $K_H=e(1)\Delta_T[1-\mu(1)]$ and $K_L=e(-1)\Delta_T\mu(-1)$.
Each gain lies between $\rho\kappa(\pi)\Delta_T$ and $\Delta_T$.
Reason: one line links the auction to the decision to trade.
Source: `overleaf/slot/sections/03_competition_information.tex:105`.

**6. High cost pays only past one belief.**
Use $\tau=(c_H-g_L)/(g_H-g_L)$ when $g_H>g_L$.
At $\tau$, rival gross profit equals the high cost.
Reason: the panel will test entry through this threshold.
Source: `overleaf/slot/sections/03_competition_information.tex:85`.

**7. Three strengths, three outcomes.**
Weak: no informed order, entry $\rho$.
Strong: purchase on good news, sale on poor news, entry above $\rho$.
Very strong: same orders, entry back at $\rho$.
Reason: this table is the talk in nine cells.
Source: `overleaf/slot/sections/04_equilibrium_results.tex:26`.

**8. Strict gaps do the proof.**
At the weak strength, $\Delta_0<k$ stops each order.
At the strong strength, $\rho\kappa(\pi)\Delta_1>k$ forces each correct order.
Reason: he can prove the main result at the board with two bounds.
Source: `overleaf/slot/sections/04_equilibrium_results.tex:54`.

**9. Fixed news gives the old answer.**
Hold the rival's news fixed, and entry cannot rise.
Reason: this control shows that the rise needs new price content.
Source: `overleaf/slot/sections/04_equilibrium_results.tex:246`.

**10. Preparation, sale, and win differ.**
Entry counts payment of the preparation cost.
A win needs the high bid past the reserve.
Reason: half of all traps mix these three events.
Source: `overleaf/slot/sections/07_welfare.tex:64`.

**11. The auction speaks to trade through two numbers.**
The spread $\Delta_T$ sets the gain from trade.
The threshold $\tau$ sets which beliefs recruit.
Reason: this line answers most "is this general?" probes fast.
Source: `overleaf/slot/sections/03_competition_information.tex:131`.

**12. Scope words for each result.**
Each result needs its market state, tie rule, and prior.
Reason: the paper wins on exact scope, not on loud claims.
Source: `overleaf/slot/sections/02_model.tex:210`.

## 2. The card list

### Drill rules

- Daily means each day, out loud, with no notes.
- Every few days means twice a week.
- Lookup only means no drill. Know the frame or backup that holds it.
- The daily set has 15 cards: OPEN-30, OPEN-2, CLOSE-30, A1, A2, B1, B2, C1 to C4, D1 to D3, and E1.
- Say each answer once, slowly. The full set takes under 15 minutes.
- Spoken drafts use talk words. They use no appendix labels.

### Opening and close

**OPEN-30. Cue: "In 30 seconds, what is the paper?" Daily.**

> A public sale has one prepared incumbent bidder.
> A potential rival bidder must pay to prepare, and it sees the stock price first.
> A stronger incumbent cuts the rival's profit at each belief, so the old logic says entry falls.
> But the same strength can widen what shareholders gain from good synergy.
> That gain can pay an informed trader to trade, and a purchase can then recruit the rival.
> Source for the set-up: `overleaf/slot/slides_script.md:33`.

**OPEN-2. Cue: "In two minutes, what is the paper?" Daily.**

> Start with a listed target in a public sale.
> One incumbent bidder has done its work.
> A potential rival bidder faces a bill for diligence, finance, and approvals.
> It must pay that bill before it can bid.
> The old answer holds the rival's news fixed.
> A stronger incumbent then cuts the return to that bill, and entry cannot rise.
> This paper adds one trade before the bill.
> An informed trader with sector knowledge can trade the target stock.
> A liquidity trader can copy each order, so the price carries news about the synergy class.
> The price never reveals the synergy class.
> The sale splits one rival value between shareholders and the rival.
> Good synergy gives shareholders more than poor synergy.
> Call that gap the shareholder spread.
> A stronger incumbent can widen that gap.
> A wider gap can make informed trade pay its cost.
> A purchase then lifts the belief past the point where high-cost preparation pays.
> Entry rises against the strong incumbent.
> Against a very strong incumbent, no price can pay the high cost, and entry returns to its floor.
> Hold the news fixed, and the rise goes away.
> Sources: `overleaf/slot/slides_script.md:39`, `overleaf/slot/slides_script.md:81`.

**CLOSE-30. Cue: "Close in 30 seconds." Daily.**

> Entry rises against the strong incumbent and returns to its floor against the very strong one.
> Strength cuts rival profit and can widen the shareholder spread.
> A wider spread can pay for informed trade, so the price can recruit the rival.
> Freeze the news, and strength cannot raise entry.
> Source: `overleaf/slot/slides_script.md:313`.

**CLOSE-2. Cue: "Close in two minutes, with the extensions." Every few days.**

> The main result compares three strengths with a unique outcome at each one.
> At the weak strength, the spread cannot pay the order cost, so no informed order occurs.
> At the strong strength, good synergy brings a purchase and poor synergy brings a sale.
> Only a purchase recruits a high-cost rival.
> At the very strong strength, trade stays active, but no belief can pay the high cost.
> Two discipline results hold at the same time.
> Strength cuts profit at each fixed belief, and fixed news restores the old answer.
> With costly research, a wider spread buys more research until the cap.
> Entry then sorts toward good synergy.
> Against the strong incumbent, a visible price raises expected proceeds and net surplus.
> In data, recruitment sits in the purchase impact, weighted by order frequency.
> So competition can create competition through the stock price.
> Sources: `overleaf/slot/slides_script.md:313`, `overleaf/slot/slides_script.md:317`.

### A. Story spine

**A1. Cue: "Why should anyone care?" Daily.**
Draft: "One more bidder can change what shareholders receive at first order. The sale rule stays fixed here. The question is who finds that bidder before the set closes."
Source: `overleaf/slot/slides_script.md:43`.

**A2. Cue: "What is new in one line?" Daily.**
Draft: "Competition changes how much the price tells the rival. The sale splits one value between shareholders and the rival. Strength can pay for the news that brings the rival in."
Source: `overleaf/slot/slides_script.md:75`.

**A3. Cue: "What does discovery mean here?" Every few days.**
Draft: "The rival's name is public. The open fact is its synergy class. Discovery means that a known rival starts costly preparation."
Source: `overleaf/slot/sections/02_model.tex:27`.

**A4. Cue: "Where in a real sale are we?" Every few days.**
Draft: "The sale chance is public, the stock still trades, and one more bidder can still come in. A disclosed approach, a strategic review, or an open contest can open that window. A fixed private set has no such window."
Source: `overleaf/slot/sections/02_model.tex:5`.

### B. Auction split

**B1. Cue: "Show the split at one value." Daily.**
Draft: "Fix $\theta\ge p$. Shareholders receive $\max\{p,\min(R,\theta)\}$ and the rival keeps $(\theta-\max\{p,R\})_+$. In mean the two parts sum to $\theta$."
Source: `overleaf/slot/sections/03_competition_information.tex:6`.

**B2. Cue: "Why does strength widen the spread?" Daily.**
Draft: "Each slice of the class gap goes to shareholders when the incumbent outbids the rival at that level. A stronger incumbent moves more slices to shareholders. Under the class ranking, the spread never narrows."
Source: `overleaf/slot/sections/03_competition_information.tex:44`.

**B3. Cue: "State the fixed gap." Every few days.**
Draft: "The spread plus the profit gap equals the class mean gap. Strength does not change that sum. It only moves the split between shareholders and the rival."
Source: `overleaf/slot/sections/03_competition_information.tex:59`.

**B4. Cue: "When can the spread fall?" Every few days.**
Draft: "It can fall when the low class fails the reserve more often. The reserve term then shrinks as strength rises. Equal admissibility plus dominance above the reserve is the exact safe case."
Source: `overleaf/slot/sections/03_competition_information.tex:51`.

**B5. Cue: "Why truthful bids?" Lookup only.**
Draft: "Each prepared bidder bids its value in the cash second-price auction. That bid is weakly dominant. Price news cannot improve the incumbent's bid."
Source: `overleaf/slot/sections/02_model.tex:95`.

### C. Slot logic

**C1. Cue: "Walk through the slot." Daily.**
Draft: "One public slot comes before preparation. With chance $\lambda$ the informed trader fills it, else a liquidity trader fills it. Market makers see only the order $X$ and set $P(X)=\mathbb{E}[V_T\mid X]$."
Source: `overleaf/slot/sections/02_model.tex:111`.

**C2. Cue: "Why does doubt survive?" Daily.**
Draft: "Each class reaches each order through a liquidity trader with mass $b$. The informed trader adds at most $\lambda$. No likelihood ratio can pass $1+u$, so no order settles the class."
Source: `overleaf/slot/sections/03_competition_information.tex:73`.

**C3. Cue: "What does the rival read?" Daily.**
Draft: "The rival sees the price, then its cost. With a positive spread and the entry floor, one price means one belief. The price can reveal the belief, and it never reveals the class."
Source: `overleaf/slot/sections/03_competition_information.tex:88`.

**C4. Cue: "Why does rational pricing not kill the gain?" Daily.**
Draft: "Market makers price the entry that each order brings. The gain that remains is entry times spread times doubt. The order cost still comes off that gain."
Source: `overleaf/slot/sections/03_competition_information.tex:102`.

**C5. Cue: "What do $b$ and $u$ do?" Every few days.**
Draft: "The mass $b=(1-\lambda)\beta$ is liquidity trade in one direction. The ratio $u=\lambda/b$ caps what one order can say. The same $u$ can still give distinct order rates and distinct entry."
Source: `overleaf/slot/sections/02_model.tex:136`.

**C6. Cue: "Why $\beta\le 1/3$ in the base case?" Every few days.**
Draft: "That bound makes no order at least as thick as one direction. The same belief band then holds after no order. The main rise needs only the purchase and sale bounds, so it allows $\beta<1/2$."
Source: `overleaf/slot/appendix/A2_beliefs_trading.tex:87`.

### D. Main result and proof

**D1. Cue: "State H1, H2, H3 in words." Daily.**
Draft: "H1 says that profit at the prior misses the high cost when weak, and profit at the top belief clears it when strong. H2 says that the order cost stops trade when weak and not when strong. H3 says that even the top belief misses the high cost when very strong."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:51`.

**D2. Cue: "Prove it in four steps." Daily.**
Draft: "First, the gain cap $\Delta_0$ falls below $k$, so no order pays at the weak strength. Second, the gain floor $\rho\kappa(\pi)\Delta_1$ clears $k$, so both correct orders must occur at the strong strength. Third, those orders give beliefs $(m,\pi,M)$, and only $M$ recruits."
Source: `overleaf/slot/slides_script.md:235`.

**D3. Cue: "Why unique at the three strengths?" Daily.**
Draft: "The bounds hold for each order plan, mixtures too. Strict gaps to $k$ and to $c_H$ then fix orders, beliefs, and entry. No tie rule can change the outcome at those three points."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:84`.

**D4. Cue: "Count the new entry." Every few days.**
Draft: "A purchase occurs with chance $b+\pi\lambda$ under full orders. Only the high-cost share $1-\rho$ can change its choice. New entry is $(1-\rho)(b+\pi\lambda)$."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:30`.

**D5. Cue: "Does entry mean the rival wins more?" Every few days.**
Draft: "No, not as a rule. High-class ownership rises exactly when $e_HW_H(F_1)>\rho W_H(F_0)$. If the high class beats the strong incumbent for sure, ownership rises with entry."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:35`.

**D6. Cue: "What is an open set worth?" Every few days.**
Draft: "It rules out a knife edge. It does not measure how large the region is. In the example, one margin is small, and Section 3 states that fact in full."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:106`.

### E. Controls and neighbours

**E1. Cue: "Freeze the news. What happens?" Daily.**
Draft: "Hold class, signal, values, and costs fixed. Strength then cuts profit at each belief and can only remove a reason to prepare. Entry cannot rise."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:250`.

**E2. Cue: "Hide the price. What happens?" Every few days.**
Draft: "The rival then acts on the prior and prepares only at zero cost. Trade can stay active at the strong strength. Entry stays at $\rho$ at both strengths [benchmark]."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:308`.

**E3. Cue: "Hold full orders fixed. What happens?" Every few days.**
Draft: "The same three beliefs occur at both strengths. Only the top belief can recruit, so entry holds flat to the ceiling and falls past it. At the weak strength that plan loses money, so it is a control and not an equilibrium."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:300`.

**E4. Cue: "What sits between weak and strong?" Every few days.**
Draft: "An uninformative market and an informative market can both hold at one strength. The threshold must sit past the prior and within reach of a purchase. The spread must pay for a recruiting purchase and still fail to pay against a flat price."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:329`.

**E5. Cue: "Why can two markets both hold?" Every few days.**
Draft: "Expect no recruitment, and entry stays at its floor, so trade cannot pay. Expect recruitment, and a purchase lifts entry, so trade can pay. Each view supports itself on the stated region."
Source: `overleaf/slot/sections/04_equilibrium_results.tex:351`.

### F. Extensions

**F1. Cue: "What does research add?" Every few days.**
Draft: "The informed trader picks its chance to learn the class and pays a rising cost. Where a purchase recruits, a wider spread buys more research until the cap. Entry sorts toward good synergy."
Source: `overleaf/slot/sections/05_research.tex:54`.

**F2. Cue: "Who sees the research choice?" Every few days.**
Draft: "No one else sees it. Market makers and the rival use the equilibrium level. A private switch faces the same price plan and the same entry plan."
Source: `overleaf/slot/sections/05_research.tex:19`.

**F3. Cue: "Does a visible price always help the seller?" Every few days.**
Draft: "No. The strict gain holds at the strong strength in the recruitment region. Past that region, a sale price can stop preparation and cut proceeds."
Source: `overleaf/slot/sections/07_welfare.tex:31`.

**F4. Cue: "What if the rival has its own news?" Lookup only.**
Draft: "Two news sources on distinct facts can both matter. The price can still tip the choice when the rival's own news is more exact. That case needs its own costs and strengths."
Source: `overleaf/slot/sections/06_robustness.tex:58`.

**F5. Cue: "What if costs or classes change shape?" Lookup only.**
Draft: "The rise survives broad cost laws in the stated windows. It holds for each ranked pair and each prior at fit strengths and costs. Point values are not essential."
Source: `overleaf/slot/sections/06_robustness.tex:9`.

### G. Data

**G1. Cue: "State the sharp test." Every few days.**
Draft: "Under full two-sided trade with the prior below the threshold, weight each impact by its order rate. The purchase side beats the sale side exactly when a purchase recruits. At an even prior, compare the raw impacts."
Source: `overleaf/slot/sections/08_empirical.tex:19`.

**G2. Cue: "Why record no order?" Every few days.**
Draft: "No order gives the base price for both impacts. A file of trades alone drops that base and bends the order rates. Fix the slot in advance and write no order as zero."
Source: `overleaf/slot/sections/08_empirical.tex:81`.

**G3. Cue: "What counts as entry in data?" Every few days.**
Draft: "Count the start of hard diligence or a plan that needs costly work. Public offers count less. Date strength from public facts before that choice, and date the price before it too."
Source: `overleaf/slot/sections/08_empirical.tex:77`.

**G4. Cue: "Orders predict the winner. Does that prove recruitment?" Lookup only.**
Draft: "No. Orders can predict the winner with entry at its floor. The weighted impact test isolates recruitment on its stated terms."
Source: `overleaf/slot/sections/08_empirical.tex:49`.

### H. Short defences

Full defences sit in Section 3. Drill only the first line here.

**H1. Cue: "Raise the reserve and the result dies." Every few days.**
Draft: "The paper holds sale terms fixed and varies strength. A high reserve can shut the channel in the example. That limit states the scope, and the next step prices the terms."
Source: `overleaf/slot/sections/09_conclusion.tex:30`.

**H2. Cue: "No outsider knows synergy best." Every few days.**
Draft: "The informed trader needs target-side facts, not the rival's board plan. The rival knows its own plans. The two news sources concern distinct facts about one match."
Source: `overleaf/slot/sections/02_model.tex:21`.

**H3. Cue: "Drop the floor and silence always holds." Every few days.**
Draft: "True, an uninformative market then always exists. The floor gives trade a base gain and lets the price reveal the belief. With it, strict gaps select one outcome at the three strengths."
Source: `overleaf/slot/sections/03_competition_information.tex:95`.

**H4. Cue: "This is just price feedback again." Every few days.**
Draft: "The new link is the sale split. One strength shift cuts the rival's claim and widens the traded claim's class gap. No prior feedback result gives that joint move."
Source: `overleaf/slot/sections/01_introduction.tex:127`.

## 3. Weak spots, ranked by danger

Rank means risk in the room, not size of the gap in print.
Each entry gives the attack, the spoken defence, one follow-up, sources, and a status.
Status values are these: "the paper supports this", "new inference", or "no full defence: best honest line".

### W1. The seller can kill the channel with the reserve

**Attack, in panel words:** "Your seller commits to a reserve. In your own example, a price just below $h=10$ pays about $1.25$ at each strength and beats your table. Why would any seller leave $p=1/2$ and invite your effect?"
Sources for the charge: `overleaf/slot/sections/07_welfare.tex:77`, `audit/jmp_search_2026_10_30/ccc_seller_terms.md:25`.

**Check of the arithmetic. New, not in the paper.**
Fix [benchmark] $h=10$, $\ell=1$, $\pi=1/2$, $\rho=1/4$, $c_H=6$, $r\le 3.6$.
Take $p<h$ with $p$ near $h$, so $r<p<h$.
Then $t_0=t_L=g_L=0$, $t_H=p$, $g_H=h-p$, and $\Delta_T=p$.
Source for these kernels: `overleaf/slot/appendix/A7_welfare.tex:158`.
Rival gross profit is $B(\mu)=\mu(h-p)$.
At the top belief $M\approx0.731$, $B(M)<c_H$ for $p$ near $h$.
No high-cost rival prepares, and entry stays at $\rho$.
A sale pays $p$ only in class $H$ with zero cost.
Mean proceeds are $p\rho\pi=p/8\approx1.25$ [benchmark].
Trade stays full, since $\rho\kappa(\pi)\Delta_T$ grows with $p$ and clears $k$.
The price then carries news, and that news recruits no high-cost rival.
At $r_1$ and $p=1.3$, proceeds are about $1.08$ by the same kernels [benchmark].
That value sits below $1.25$.
The planning note states the same ranking: `audit/jmp_search_2026_10_30/ccc_seller_terms.md:42`.
One more fact helps. For $p\le\ell$, $\Delta_T(r)=(r-\ell)^2/(2r)$ has no $p$ term.
Source: `overleaf/slot/sections/04_equilibrium_results.tex:164`.
A low reserve cannot widen the spread. Only exclusion can do that jump.
This reading is new. The algebra sits in the paper.

**Spoken defence (three sentences):** "That calculation is right in the point-mass example, and it sets the scope. This paper holds sale terms fixed and asks what strength does to entry through the price. With full commitment to walk away, the seller can shut that channel, so the claim needs a seller who cannot hold such a price."
Sources: `overleaf/slot/sections/02_model.tex:93`, `overleaf/slot/sections/09_conclusion.tex:30`.

**Likely follow-up:** "Then the result is just a badly set reserve."
**Answer:** "No. At each fixed reserve at or below $\ell$, strength still widens the spread and can switch trade on. The open step joins the choice of terms to the full trade and entry response."
Sources: `overleaf/slot/sections/03_competition_information.tex:38`, `overleaf/slot/sections/09_conclusion.tex:30`.

**Faculty trace:** The reserve table already shows flat entry once the low class fails the reserve.
Source: `overleaf/slot/sections/07_welfare.tex:99`.
Verdict for the slot version: still applies in full.
**Status: no full defence: best honest line.** The line is the scope line in the defence. Do not claim that $p=1/2$ is optimal.

### W2. The outsider knows the class, the rival knows nothing, and no one needs $R$

**Attack:** "Why does your informed trader know the synergy class exactly, yet learn nothing about $\theta$ past the class and nothing about the incumbent's value? And why does the rival start with no view of its own fit?"

**Spoken defence (four sentences):** "The split puts distinct facts in distinct hands. The informed trader holds target-side facts on customers, technology, and demand. The rival holds its own plans, and payoffs need only the class because bids and proceeds average over $R$ and over $\theta$ in the class. Exact class knowledge and a silent rival form the sharp case, and the paper then drops both extremes."
Sources: `overleaf/slot/sections/02_model.tex:21`, `overleaf/slot/sections/02_model.tex:200`.

**Likely follow-up:** "Can that trade be lawful, and can the rival be the better informed party?"
**Answer:** "Yes on both counts, with care. Own research on target-side facts differs from a leaked bid from a duty-bound source. With two imperfect signals on distinct facts, the rise can hold when the rival's signal is more exact, at fit costs and strengths."
Sources: `discussion/jihee_empirical_questions.md:162`, `overleaf/slot/sections/06_robustness.tex:64`.

**Faculty trace:** One faculty note asks what the informed trader's news concerns.
Source: `discussion/2026-10-26/ming-email.md:1`.
One note splits synergy into bidder-side, target-side, and market parts.
Source: `discussion/jihee_empirical_questions.md:57`.
Verdict for the slot version: still applies. The slot changes trade, not who knows what.
**Status: the paper supports this**, for the scope and the signal extension. The law line comes from the faculty note, not from the paper.

### W3. The entry floor does heavy work

**Attack:** "Set $\rho=0$. Silence supports itself: expect no entry, earn no gain, place no order. That equilibrium exists at each strength. Your floor picks the result you like."

**Check. New, not in the paper.**
Set $\rho=0$ and try $e(x)=0$ for each $x$, with no informed order.
Each correct-order gain is $K_j=e\Delta_T\times\text{doubt}=0<k$.
No order then pays, so silence is an equilibrium at each $\Delta_T$.
With $\rho>0$, entry stays at or past $\rho$ after each price.
Source: `overleaf/slot/sections/03_competition_information.tex:86`.
The floor in $K_j$ is then $\rho\kappa(\pi)\Delta_T$, which can clear $k$.
Source: `overleaf/slot/sections/03_competition_information.tex:105`.
The floor also lets one price pin down one belief.
Source: `overleaf/slot/sections/03_competition_information.tex:88`.

**Spoken defence (three sentences):** "That silence does exist with no floor, and I do not hide it. The floor names ready bidders whose extra diligence costs nothing at the margin. With that mass in place, price content has a base load, and strict gaps give one outcome at the three strengths."
Sources: `overleaf/slot/sections/02_model.tex:83`, `overleaf/slot/sections/03_competition_information.tex:95`.

**Likely follow-up:** "Is zero cost with mass $\rho$ just a trick atom?"
**Answer:** "No atom is essential. A low-cost part that always prepares in the stated window does the same work, with atoms or with none. The high-cost part must sit in its stated window."
Source: `overleaf/slot/sections/06_robustness.tex:9`.

**Faculty trace:** One faculty exchange urges a drop of the floor and reports a second, active equilibrium on a strength range.
Source: `discussion/2026-10-26/ming-email.md:1`.
Do not drill those two endpoint numbers. The paper does not state them.
Verdict for the slot version: still applies. The paper keeps $0<\rho<1$ throughout.
Source: `overleaf/slot/sections/02_model.tex:84`.
**Status: new inference** for the $\rho=0$ construction; **the paper supports this** for the floor's three jobs.

### W4. The example window is thin, and the order size never moves

**Attack:** "Your top belief must sit between two thresholds a hair apart. Your prior sits a hair from the edge. And the informed trader can never pick a size. Is the result a tuned unit trade?"

**Facts to own [benchmark]:** The test is $\tau(r_1)=141/200<M(1/2)<4245/5804=\tau(r_2)$.
Source: `overleaf/slot/sections/04_equilibrium_results.tex:111`.
The width in belief units is about $0.0264$ [benchmark].
The cost gap at the top end is $c_H-B_2(M)=0.002689$ [benchmark].
Source: `overleaf/slot/numbers.tex:693`.
With $1+u=\mathrm{e}$, all three parts hold for priors in about $(0.4679,0.5004)$ [benchmark].
Sources: `overleaf/slot/numbers.tex:5082`, `overleaf/slot/numbers.tex:5086`.
Parts (i) and (ii) alone run to about $0.6331$ [benchmark].
Source: `overleaf/slot/numbers.tex:5083`.
The thin top edge comes from $r_2$ alone. A farther $r_2$ widens it.
The threshold slope sets the width, since class $H$ outbids each strength on the path.
Source: `overleaf/slot/sections/04_equilibrium_results.tex:213`.
The unit is a normalised small trading unit, and $k$ is a distinct friction.
Source: `overleaf/slot/sections/02_model.tex:131`.

**Spoken defence (four sentences):** "The thin edge is real, and it belongs to the return leg at one $r_2$ near the ceiling. The rise itself needs an open set, and it holds for each ranked pair and each prior at fit strengths and costs. Unit size gives the liquidity trade its cover, since both trades share one size. A free size choice needs a rule for unused sizes, and the paper does not solve that game."
Sources: `overleaf/slot/sections/06_robustness.tex:27`, `overleaf/slot/sections/02_model.tex:148`.

**Likely follow-up:** "Scale the trade up. Does $k$ still bind?"
**Answer:** "Money units can scale with no change in orders, beliefs, or entry. Share scale matters for who bears the transfer, and the paper gives a break-even scale for first holders. It does not endow the slot with a free size."
Sources: `overleaf/slot/sections/02_model.tex:79`, `overleaf/slot/sections/07_welfare.tex:25`.

**Faculty trace:** Early faculty work calls the two-value, even-prior case unconventional.
Source: `audit/alex_meeting_2026_10_21/BRIEF.md:133`.
Verdict for the slot version: partly applies. Classes and priors are now general. The displayed example stays thin at the top edge.
**Status: no full defence: best honest line** for size choice; **the paper supports this** for the open set and the general classes. Best honest line: "Size choice is outside the slot, and I state that scope."

### W5. Why a price, and not a rumour, a call, or the target itself?

**Attack:** "A banker can call the rival. A rumour can run in the press. The target can open its books and certify fit. Why must news travel through a costly stock trade?"

**Spoken defence (four sentences):** "It need not travel that way in each sale, and the paper never says so. The paper compares strength with price content live and with price content fixed or hidden. A trade puts money past a competitive price and past cost $k$, so its content has a price tag. A call, a rumour, and a data room sit outside that comparison and can run beside the price."
Sources: `overleaf/slot/sections/04_equilibrium_results.tex:246`, `overleaf/slot/sections/02_model.tex:124`.
One more scope fact helps. The open fact is match fit, not a target fact alone.
Source: `overleaf/slot/sections/02_model.tex:21`.
The target can show its own books. Fit still needs the rival side of the match. This last step is **new, not in the paper**.

**Likely follow-up:** "The seller runs outreach in real sales. Your seller does nothing past the reserve."
**Answer:** "Outreach exists, and the paper cites a proxy that splits approach, outreach, and interest that needs more diligence. This paper holds that process fixed and asks what the stock price adds before a rival pays. The choice of sale terms with trade in view is the named next step."
Sources: `overleaf/slot/sections/02_model.tex:34`, `overleaf/slot/sections/09_conclusion.tex:30`.

**Faculty trace:** The faculty notes treat outreach and private steps as the norm.
Source: `discussion/jihee_empirical_questions.md:274`.
Verdict for the slot version: still applies as a scope limit. No version prices banker talk.
**Status: new inference** for the price-tag contrast; **the paper supports this** for the fixed-news and hidden-price comparisons.

### W6. Why this slot? Why not Kyle? Why not Laplace? Is this old feedback?

**Attack:** "Kyle gives you a standard market. Your Laplace draft gave you sizes. Dow and co-authors gave you feedback, and Edmans and co-authors gave you the set-up. What is left, past new labels?"

**Spoken defence (four sentences):** "The slot keeps each order on path, so no off-path belief enters. One gain check per class then gives finite, exact equilibrium lists and a clean research choice. The new economics sits in the sale: one strength shift cuts the rival's claim and widens the traded claim's class gap at the same time. Prior feedback work has no such joint move, since no auction splits the value that way."
Sources: `overleaf/slot/sections/02_model.tex:153`, `overleaf/slot/sections/01_introduction.tex:127`.

**Likely follow-up:** "Match the belief bounds and Laplace is the same model."
**Answer:** "The bounds match when $1+u$ equals the Laplace bound, and the gains match too. The chance of each top signal and the full price law still differ, and Laplace needs a marginal check for sizes. Same bounds do not mean same equilibrium."
Sources: `overleaf/slot/sections/02_model.tex:156`, `overleaf/slot/comparison.tex:123`.

**Detail for Kyle. New, not in the paper.**
A Gaussian flow lets one tail flow near-prove the class.
Doubt then has no fixed floor past zero.
The proof step $K_j\ge\rho\kappa(\pi)\Delta_T$ has no such floor there.
The paper states the pricing kinship and the slot sources, not this contrast.
Source for kinship: `overleaf/slot/sections/02_model.tex:160`.

**Faculty trace:** Early faculty work calls Laplace noise unconventional and urges a discrete set-up.
Source: `audit/alex_meeting_2026_10_21/BRIEF.md:144`.
Later faculty notes ask which stage should lead.
Source: `discussion/2026-10-26/ji-hee-email.md:1`.
Verdict for the slot version: the Laplace charge no longer hits the main text. The "is one slot real?" charge still applies.
**Status: the paper supports this** for sources and bounds; **new inference** for the Kyle contrast.

### W7. How common is this setting?

**Attack:** "Most contests form in private with a fixed set. Name the sales where a public price can still recruit. How many such sales exist?"

**Spoken defence (four sentences):** "The claim needs a public window with one prepared incumbent and an open set. A disclosed approach, a strategic review, or an open contest can give that window. A fixed private set gives no window, and the paper claims nothing there. The paper gives no count, and I will not invent one."
Sources: `overleaf/slot/sections/02_model.tex:5`, `discussion/jihee_empirical_questions.md:274`.

**Likely follow-up:** "Give one concrete case and one scale check."
**Answer:** "The paper cites one proxy that splits approach, outreach, and interest that needs more work. A planning note counts filings that name a go-shop window and finds hundreds of mentions, with true windows still to count. That count is a plan input, not a paper result."
Sources: `overleaf/slot/sections/02_model.tex:34`, `audit/jmp_search_2026_10_30/ccc_seller_terms.md:93`.

**Faculty trace:** Faculty notes stress that public bids show only part of a private process.
Source: `discussion/jihee_empirical_questions.md:274`.
Verdict for the slot version: still applies. The paper states the window and no rate.
**Status: no full defence: best honest line.** Best honest line: "Prevalence is open. The scope is public windows with an open set."

### W8. No test has run. Is this theory with no fact?

**Attack:** "You give five predictions and run none. At upgrade, why should we pass a theory with no fact in hand?"

**Spoken defence (four sentences):** "No test has run, and the talk must say so in plain words. The paper does give one test that needs only prices and order rates on stated terms. It also states how to date the slot, how to write no order, and what counts as preparation. The upgrade claim is a sharp mechanism with a run-ready test, not a settled fact."
Sources: `overleaf/slot/sections/08_empirical.tex:19`, `overleaf/slot/sections/08_empirical.tex:77`.

**Likely follow-up:** "A run-up can mean three things. Your test cannot split them in real data."
**Answer:** "A raw run-up cannot split them, and the paper does not use a raw run-up. On its terms, the weighted purchase side beats the sale side exactly under recruitment. Past those terms, the test needs new work."
Sources: `overleaf/slot/sections/08_empirical.tex:22`, `discussion/jihee_empirical_questions.md:263`.

**Faculty trace:** One planning memo states the same risk in hiring terms.
Source: `audit/jmp_search_2026_10_30/MEMO.md:53`.
Verdict for the slot version: still applies in full.
**Status: no full defence: best honest line.** Best honest line: "The test is stated and not yet run."

### W9. Two markets at one strength, between the headline points

**Attack:** "You stress one outcome at three points. Between them, silence and trade both hold. In the field, which one occurs? Your path has no prediction there."

**Spoken defence (three sentences):** "Both can hold on the stated region, and the paper characterises that region exactly. The headline rise uses three points with one outcome each, so no pick between markets drives it. Between those points, entry in the active market rises with the spread while the high class mixes."
Sources: `overleaf/slot/sections/04_equilibrium_results.tex:329`, `overleaf/slot/sections/04_equilibrium_results.tex:24`.

**Likely follow-up:** "Tie rules move the endpoints. How much of this is tie craft?"
**Answer:** "The three headline outcomes survive each tie pair, since each gap is strict. Coexistence and research use the default pair, and the paper states each change that a new pair brings. Say 'past $r_N$' and 'past $r_C$', not 'at' them."
Sources: `overleaf/slot/sections/02_model.tex:210`, `overleaf/slot/sections/04_equilibrium_results.tex:415`.

**Faculty trace:** Early discrete work finds the same fragility in cruder form, with belief rules at unused flows.
Source: `audit/discrete_exploration_2026_10_21/BRIEF.md:1`.
Verdict for the slot version: partly applies. No unused flow remains. Tie craft still matters at endpoints.
**Status: the paper supports this.**

### W10. The spread result rides on the second-price rule

**Attack:** "Negotiate the price and your spread can fall with strength. Why present a payment-rule artefact as a law of competition?"

**Spoken defence (three sentences):** "The paper states that limit as a result, not as a footnote. With seller weight $\omega$, strength moves the spread with the sign of $1-2\omega$. The second-price case $\omega=0$ loads the runner-up value in full, so auctions best feed the price channel."
Sources: `overleaf/slot/sections/07_welfare.tex:43`, `overleaf/slot/sections/07_welfare.tex:57`.

**Likely follow-up:** "Real takeovers blend auctions and talks. Where does that leave you?"
**Answer:** "It leaves a test of form: the channel fades as weight shifts from the runner-up value to the winner value. The headline claim holds for the stated cash auction. Past that form, sign the weight first."
Source: `overleaf/slot/sections/07_welfare.tex:53`. The test-of-form line is **new, not in the paper**.

**Faculty trace:** No early faculty note presses this point in the files read.
Verdict: no old-name issue. The point hits the slot version as stated.
**Status: the paper supports this** for the sign result; **new inference** for the blend line.

### W11. Entry up, ownership down: the quiet trap

**Attack:** "More preparation need not mean more rival wins, since the strong incumbent also wins more. Do shareholders gain from activity that still loses?"

**Spoken defence (three sentences):** "Entry and wins are distinct events, and the paper keeps them distinct. High-class ownership rises exactly when new entry beats the drop in win chance. With sure outbidding by the high class, that test holds, and the strong incumbent then takes wins only from the low class."
Sources: `overleaf/slot/sections/04_equilibrium_results.tex:66`, `overleaf/slot/sections/04_equilibrium_results.tex:71`.

**Likely follow-up:** "Your slides drop ownership. Will you claim it live by slip?"
**Answer:** "Frame 13 states entry alone, so I state entry alone there. I claim ownership only with its test or with sure outbidding in view."
Sources: `overleaf/slot/slides.tex:450`, `overleaf/slot/sections/04_equilibrium_results.tex:40`.

**Faculty trace:** Early red-team work gives a case with entry up and high-class ownership down.
Source: `audit/alex_meeting_2026_10_21/memos/SYNTHESIS.md:29`.
Verdict for the slot version: still applies. The slot paper now states the exact test.
**Status: the paper supports this.**

### W12. Research holds only at an even prior, with a fitted cap

**Attack:** "Research needs $\pi=1/2$. The cap equals your example presence by choice. Is 'competition creates research' one tuned branch among three?"

**Spoken defence (four sentences):** "The even prior is a stated scope limit, not a hidden one. On that scope, one root gives research for the recruiting branch, and that root rises with the spread to the cap. Zero research and floor research can both hold beside it on stated ranges. At the cap, the branch meets the main result by design, so the talk can join the two claims."
Sources: `overleaf/slot/sections/05_research.tex:19`, `overleaf/slot/sections/05_research.tex:160`.

**Likely follow-up:** "Why does the first-order line skip the price response to research?"
**Answer:** "Research is private, so a switch faces the same price plan. Match then asks that the best private level equal the level in beliefs. A public choice would need a new game."
Source: `overleaf/slot/sections/05_research.tex:19`.

**Faculty trace:** One faculty note asks if an even prior suffices for this result.
Source: `discussion/2026-10-26/alex-email.md:1`.
Verdict for the slot version: still applies. No general-prior research result exists in the paper.
**Status: the paper supports this** on its scope; **no full defence: best honest line** past that scope. Best honest line: "Past an even prior, research is open."

### W13. Is this the job-market paper? What fills the thesis?

**Attack:** "You are in year two. Is this the job-market paper? If the reserve step fails and the test finds no windows, what is left of the thesis?"

**Spoken defence (four sentences):** "No. The current plan makes this paper the second paper and a leaks paper the job-market paper. The two share one line: what a sale puts in the price, and what a price brings to a sale. Cheap kill checks come first, with a set date to switch course if they fail."
Sources: `audit/jmp_search_2026_10_30/MEMO.md:7`, `audit/jmp_search_2026_10_30/MEMO.md:14`.

**Likely follow-up:** "Dates and fallbacks, please. What stops, and when?"
**Answer:** "The gate sits at the end of March 2027 in the plan file. Fail the first leak checks, and exit cascades or a stronger form of this paper steps up. For this paper, price the seller's terms first, then count public windows."
Sources: `audit/jmp_search_2026_10_30/MEMO.md:20`, `audit/jmp_search_2026_10_30/MEMO.md:128`.

**Care note:** Those files state a plan, not a fact. Say "current plan" each time.
Source: `audit/jmp_search_2026_10_30/MEMO.md:1`.
Verdict on names: plan files use short project names. Translate each name into talk words live.
**Status: new inference.** The defence reports plan files. It proves no future outcome.

## 4. Errors to fix first

Fix these lines before any drill. Each entry gives the fault, the proof, and the exact new words.
Do not drill the old words. No file changes form part of this report.

**E1. The reserve result bans what it means to allow.**
Fault: one formal line allows values below the reserve and keeps "the class ranking" in full.
Proof: the ranking needs $G_H(p^-)=G_L(p^-)=0$, so no value can sit below $p$.
Sources: `overleaf/slot/appendix/A7_welfare.tex:161`, `overleaf/slot/sections/02_model.tex:63`.
Consumers: the reserve table, backup B4, and card H1 all restate this result.
Replacement words: "Fix a reserve, and allow class values below it. Keep $G_H(y)\le G_L(y)$ for every $y$, the costs, the slot, and a strengthening $F_1\le F_0$. Compute each class object with the reserve."

**E2. Research privacy drops from the talk.**
Fault: frame 16 and its script say the informed trader picks $\lambda$. They never say that no one else sees the pick.
Proof: the paper states the private pick in full, and the first-order line needs it.
Sources: `overleaf/slot/slides.tex:582`, `overleaf/slot/sections/05_research.tex:19`.
Consumers: frame 16, backup B12, and card F2.
Replacement words, at the head of frame 16 speech: "One change from frame 6. The informed trader picks presence in private. Market makers and the rival use the equilibrium level."

**E3. The slot source drops one parent.**
Fault: script frame 3 says the trading set-up comes from Edmans, Goldstein and Jiang, with no second source.
Proof: the paper gives the slot form to the alternative-arrival device and the unit menu, presence, and cost to the second source.
Sources: `overleaf/slot/slides_script.md:69`, `overleaf/slot/sections/02_model.tex:148`.
Consumers: frame 3, backup B7, backup B14, and defence W6.
Replacement words: "Dow, Goldstein and Guembel give the closest feedback line: real choices feed back into news supply. The slot form follows Dow and Gorton, and the unit menu, presence, and unit cost follow Edmans, Goldstein and Jiang."

**E4. Two script lines say "type" for "class".**
Fault: the script breaks its own locked words at two points.
Proof: the deck locks "synergy class" for $j$.
Sources: `overleaf/slot/slides_script.md:101`, `overleaf/slot/slides_script.md:137`, `overleaf/slot/slides.tex:8`.
Consumers: speech on frames 5 and 7, and each later use of $\mu$.
Replacement words for frame 5: "The class-value pair, $R$, $C$, and the slot draws are independent."
Replacement words for frame 7: "Order belief $\mu(x)$ means the chance of class $H$, good synergy, given the order $X=x$."

**E5. One backup states half the ranking as the whole ranking.**
Fault: backup B8 writes the ranking as $G_H\le G_L$ alone in one summary line.
Proof: dominance alone can let the reserve term flip the spread sign. Frame 10 states the full pair.
Sources: `overleaf/slot/slides.tex:1054`, `overleaf/slot/slides.tex:349`, `overleaf/slot/sections/03_competition_information.tex:51`.
Consumers: backup B8 and card B4.
Replacement words: "(b) Under the class ranking — $G_H\le G_L$ with $G_H(p^-)=G_L(p^-)=0$ — the shareholder spread weakly rises."

**E6. Endpoint words put death at the point, not past it.**
Fault: one backup line says the uninformative market "dies at $r_N$".
Proof: that market still holds at $r_N$ under the default pair. Recruitment likewise holds at $r_C$ and stops past it.
Sources: `overleaf/slot/slides.tex:801`, `overleaf/slot/sections/04_equilibrium_results.tex:415`.
Consumers: backup B3, backup B12, and defence W9.
Replacement words: "The uninformative market holds through $r_N$ and fails past $r_N$. Informative entry holds through $r_C$ and drops to its floor past $r_C$."

**E7. One scope phrase has no plain sense.**
Fault: backup B6 says point values "are not the kind case".
Proof: no term in the paper gives that phrase a sense. A live panel will stop on it.
Source: `overleaf/slot/slides.tex:926`.
Consumers: backup B6 and card F5.
Replacement words: "Point-mass synergy values are not essential."

**E8. The $\beta$ gloss gives the wrong reason.**
Fault: frame 11 glosses $\beta\le1/3$ as cover for each outcome.
Proof: a liquidity trader can place each outcome for each $\beta\in(0,1/2)$. The bound gives $b_0\ge b$, so the same band holds after no order.
Sources: `overleaf/slot/slides.tex:378`, `overleaf/slot/appendix/A2_beliefs_trading.tex:41`.
Consumers: frame 11, backup B2, and card C6.
Replacement words: "With $\beta\le1/3$, no order holds at least as much liquidity mass as one direction, so the same band holds after no order."

**E9. One long fraction cannot be said clean.**
Fault: script frame 14 reads $4245/5804$ in full words.
Proof: the line takes nine words for one bound and invites a digit slip.
Source: `overleaf/slot/slides_script.md:245`.
Consumers: frame 14 speech and defence W4. Keep the exact fraction on the slide face.
Replacement words: "The strong threshold is $0.705$. The very strong threshold is about $0.7314$. The top belief sits just between them."

**E10. Talk and paper name one object two ways, with no bridge.**
Fault: the talk says "shareholder spread" for $\Delta_T$. The paper says "target-payoff spread" for the same object.
Proof: both texts define $\Delta_T=t_H-t_L$ with distinct names.
Sources: `overleaf/slot/slides.tex:306`, `overleaf/slot/sections/02_model.tex:193`.
Consumers: each $\Delta_T$ card and each cross-check with the paper in hand.
Replacement words for first use: "Shareholder spread: $\Delta_T=t_H-t_L$. The paper calls the same object the target-payoff spread."

**E11. Script length breaks the 30-minute brief.**
Fault: the script plans $33.5$ minutes of speech with $11.5$ minutes for questions.
Proof: the upgrade brief in the task names a 30-minute talk. Memorisers lock the long pace in.
Source: `overleaf/slot/slides_script.md:3`.
Consumers: timing on each frame, most at risk on frames 13 to 18.
Replacement plan in words: "Cut frame 14 to the two thresholds in decimals. Cut frame 16 to the existence test and the rise to the cap. Keep frames 10 to 13 and frame 15 at full length."

## 5. Leave out

These items look vital and fail the card test.
Each item states where to find it on demand.

**L1. Decimal tables and margin lists.**
Leave out: price levels, entry rates to six places, and margin rows.
Why: no panel grades recall of a registry. One wrong digit costs more than one clean bound earns.
Find it at: backup B10 and backup B11. Source: `overleaf/slot/slides.tex:1095`.

**L2. Marked strengths past the headline three.**
Leave out: $r_A$, $r_F$, $r_J$, $r_S$, $r_R$, $r_Q$, and kin as memorised values.
Why: each mark needs its tie pair and branch. Say the role in words and open the backup for the value.
Find it at: backup B3 and backup B12. Source: `overleaf/slot/slides.tex:809`.

**L3. Full equilibrium tuples and six-part checks.**
Leave out: tuple parts and check numbers as speech.
Why: live speech needs orders, beliefs, entry, and price order. The full list serves a written check, not an answer.
Find it at: backup B9. Source: `overleaf/slot/slides.tex:1077`.

**L4. Integral forms with $D(y)$ at full length.**
Leave out: the two integral lines as daily recall.
Why: the slice story in words plus $t+g=\theta$ carries the talk. Drill the integrals only if a board proof looms.
Find it at: backup B8, third page. Source: `overleaf/slot/slides.tex:1070`.

**L5. Coexistence branch craft past the region.**
Leave out: mix rates, threshold pairs, and prior bands in full.
Why: the region plus the self-support logic answers the room. Branch craft invites long detours with no gain.
Find it at: backup B3. Source: `overleaf/slot/slides.tex:759`.

**L6. Research roots and cap windows.**
Leave out: root values, cost windows, and three-strength tables.
Why: the card needs the existence test, the rise to the cap, and the private pick. Values invite digit traps.
Find it at: backup B12. Source: `overleaf/slot/slides.tex:1302`.

**L7. Welfare levels and transfer scales.**
Leave out: gain levels, gross transfers, and break-even scales as drill.
Why: signs and scope win the exchange. Levels need the benchmark label each time and slow the pace.
Find it at: backup B4. Source: `overleaf/slot/slides.tex:841`.

**L8. Secondary predictions in full dress.**
Leave out: presence checks, winner gaps, and report means as daily cards.
Why: one clean test beats five half-held tests. Keep the weighted impact test and the winner caveat.
Find it at: backup B13. Source: `overleaf/slot/slides.tex:1381`.

**L9. Laplace algebra in full.**
Leave out: score bounds, scale factors, and flow laws as drill.
Why: the slot carries the talk. One bounds-match line plus one scope line answers the probe.
Find it at: backup B15 and the comparison note. Source: `overleaf/slot/slides.tex:1498`.

**L10. Journal names, years past the spine, and name lists.**
Leave out: full reference recall past the few spine names in the talk.
Why: the panel tests the split, the band, and the bounds. Name recall adds load with no defence value.
Find it at: backup B14. Source: `overleaf/slot/slides.tex:1447`.







