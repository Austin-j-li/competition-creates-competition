"""One-off: writes the 28-minute main speech into slides_script.md and recomputes counts and times."""
import re,sys
path='/home/uctpiaj/work/Projects/competition-creates-competition/overleaf/slot/slides_script.md'
old=open(path,encoding='utf8').read()
tail=old[old.index('## Prepared answers'):]
tail=tail.replace("It learns the rival's synergy class, good or poor, rather than its realized value.","It learns the rival's synergy class, good or poor, and no further news about its value. In the point-value example, the class fixes the value.")
F=[
("Title — Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders","""Thank you. I am Austin Li, from the Department of Economics at University College London. This talk concerns a public sale before the bidder set closes. One bidder is already prepared: the incumbent bidder, or the incumbent. A potential rival bidder, the rival, must pay to prepare. Between those two stages, the target stock price can affect who enters the sale."""),
("Frame 1 — Does a stronger incumbent always keep the rival out?","""A listed company announces that it is open to a sale. The incumbent has done its homework. The rival must decide whether to pay for months of diligence. Meanwhile the stock trades, and an informed trader that follows the company's customers trades it too.

Does a stronger incumbent always keep the rival out?

The seller cares about discovery. A public sale tries to find one more bidder before the bidder set closes. Bulow and Klemperer show why one extra bidder can carry first-order value. Here the sale rule stays fixed. The question is whether a stronger incumbent helps discover the rival or ends the search.

The rival cares about the diligence bill. It must check contracts, liabilities and technology, and secure finance and approvals, before an executable offer. A stronger incumbent can reduce the return from that work. But the rival can also learn from the stock price before it pays.

The market matters because prices move before bids move. The informed trader's order can put some of its knowledge into the price. The price can then change the decision to prepare.

The seller's proceeds can depend on rival preparation, the rival needs a reason to pay, and the market can supply news before commitment. The question connects all three."""),
("Frame 2 — The received answer: strength cannot raise entry","""The received answer starts with the return to diligence.

The rival pays before it can bid. A stronger incumbent can make a profitable win less likely and raise the payment when the rival wins. The same work then earns weakly less. Some preparation decisions can cease to pay.

Fishman gives the classic takeover deterrence argument. In Fishman, the first bidder chooses a preemptive bid. Here strength is a public distribution of value, and the realized value stays private until bids.

The logic holds when what the rival knows stays fixed. With the information, values and cost law fixed, entry cannot rise.

I keep that force. I add a target stock price before preparation and let its information respond to competition. The next step is to explain why a stronger incumbent can make that price say more."""),
("Frame 3 — Where the paper sits: price feedback meets costly entry","""Dow, Goldstein and Guembel are the closest antecedent: real decisions feed back into information production. The trading slot takes its alternative arrival from Dow and Gorton, and its unit orders, presence and order cost from Edmans, Goldstein and Jiang's 2015 paper.

Fishman supplies deterrence; Roberts and Sweeting supply selective entry. Here the price supplies information before costly preparation.

Edmans, Goldstein and Jiang's 2012 paper connects target prices to takeover activity. Kyle and Vila study an acquirer's share purchases. Here an outside informed trader starts with no net position.

The new link is the sale. It splits one value between shareholders, whose claim trades, and the rival, who decides whether to enter. Competition changes how much the price tells the rival."""),
("Frame 4 — This paper: a stronger incumbent can recruit the rival","""A stronger incumbent weakly cuts the rival's profit at each belief. It can also widen the shareholder spread, the difference in shareholder proceeds between good and poor synergy. That wider spread can make informed trade worth its cost. The price can then recruit the rival.

Three results carry the argument. First, on an open set of inputs, entry rises from the weak to the strong incumbent, then returns to its floor, with a unique outcome at each of the three strengths. Second, one shift never raises rival profit and never narrows the shareholder spread. Third, freeze the information, and strength cannot raise entry.

Extensions follow: costly research, gains for sellers from a visible price, and a price-impact prediction.

I will set out the model, explain the mechanism and main result, state its fixed-information control, then turn to the extensions."""),
("Frame 5 — Players and the sale rule","""Standalone value is zero. Values and costs are per share. All agents are risk neutral.

The incumbent is already prepared. Its value R follows public continuous distribution F, and R stays private until bids. Strength means a first-order stochastic shift toward higher values.

The rival sees the price, then decides whether to prepare. Its class j is H, good synergy, or L, poor synergy. Prior pi is the chance of H. Value theta has law G sub j. The class ranking puts G sub H weakly below G sub L at every value level, and every value meets reserve p.

Cost C is zero with probability rho, the entry floor; otherwise it is positive high cost c sub H. Payment reveals theta and permits a bid.

The seller commits before trade to a cash second-price auction with positive reserve p. Neither bidder trades target shares."""),
("Frame 6 — Timing: one trading slot, then preparation","""The sequence puts the stock price before the preparation decision.

The seller first commits to reserve p. Next comes the order X: minus one is a sale, zero is no order, and one is a purchase. Then market makers set stock price P. The rival sees P, learns cost C, and decides whether to prepare. Bids and payoffs follow.

Presence lambda is the chance that the informed trader receives the order opportunity. It observes class j and chooses order q from those same three alternatives. A nonzero order costs k, the order cost.

With probability one minus lambda, a liquidity trader receives the opportunity instead. It sells or buys with probability beta each, and otherwise places no order. Beta is at most one third. No one observes which trader placed the order.

Competitive market makers see only the order X. Price P of X equals expected sale proceeds V sub T given X. That expectation includes the preparation response to the price.

A purchase can carry news, but a liquidity purchase can copy it. This uncertainty will preserve the informed trader's advantage."""),
("Frame 7 — Information and choices","""Each player sees a different part of the sale.

The incumbent knows value R and bids R if it meets reserve p.

The informed trader sees class j, good or poor synergy, and no further news about the rival's value. In the point-value example, the class fixes the value. It holds no initial net position and cannot acquire the target. It is an outsider with sector expertise, such as a sector-focused long-short fund that researches the target's customers, technology and demand.

The liquidity trader has no private information about synergy.

Market makers observe the order X and cannot identify the trader.

The rival sees the price, then its cost C. It learns theta only after preparation, and then bids theta.

Order belief mu of x means the probability of class H, good synergy, given the order x. Market makers use that belief. The rival instead conditions on the price. I keep these beliefs distinct until the price-revelation result applies."""),
("Frame 8 — Payoffs","""Take a prepared rival with value theta at least reserve p. The number line separates what shareholders receive from what the rival keeps.

Target proceeds t of theta average the larger of p and the smaller of incumbent value R and theta. Gross auction profit g of theta averages the positive part of theta minus the larger of p and R. Both expectations are over R.

The sum, t of theta plus g of theta, equals theta. The second-price rule divides one value between these two claims.

Class proceeds t sub j and class profit g sub j average these amounts within class j. Without entry, proceeds t sub zero equal reserve p times one minus F evaluated at p.

Shareholder spread Delta T equals t sub H minus t sub L. Rival gross profit B at belief mu equals g sub L plus mu times the difference g sub H minus g sub L.

The informed trader earns its signed order times proceeds minus price, less k on a nonzero order."""),
("Frame 9 — Equilibrium with competitive prices","""This is a perfect Bayesian equilibrium with break-even prices set by competitive market makers.

The informed trader's payoff multiplies its order by the gap between expected proceeds and price, less the order cost. Expected proceeds are t sub zero plus entry e of q times the difference t sub j minus t sub zero.

Price P of x starts with t sub zero, then adds entry e of x times a bracket. The bracket is t sub L minus t sub zero, plus spread Delta T times belief mu of x. Entry e is at least rho.

Liquidity trade makes every order possible in each class, so Bayes' rule determines every belief.

Zero cost prepares. High cost prepares when rival gross profit covers it, including equality. An indifferent informed trader may mix. Each strength needs a fresh equilibrium."""),
("Frame 10 — Strength lowers rival profit and widens the spread","""Proposition one compares two distributions for incumbent value. F tilde lies weakly below F at every value, which means a stronger incumbent. Hold the reserve and both class value laws fixed.

For either synergy class, class profit under F tilde is at most its value under F. Rival gross profit B at every fixed belief also weakly falls.

The second part requires the class ranking. Good synergy has weakly higher values, and every value meets the reserve. Shareholder spread Delta T then weakly rises.

The last identity splits the class value gap. Delta T plus good-synergy profit minus poor-synergy profit equals good-synergy mean value minus poor-synergy mean value. The right side stays fixed as F changes.

Read the diagram as a division of that fixed gap. Strength can transfer part of the rival's profit gap to shareholders. The same auction creates the deterrence force and the return to information."""),
("Frame 11 — Beliefs stay in a band, and the price reveals the belief","""Define liquidity mass b as beta times the quantity one minus lambda. Define u as lambda divided by b.

A liquidity order can copy either informed order, so one order can move the odds of good synergy by a factor of at most one plus u. That gives band floor m and top belief M on the slide.

For every order plan, every belief after a purchase or a sale lies in that band. Beta at most one third extends the band to no order.

With positive spread, a positive rival gross-profit gap and positive entry floor rho, equal prices imply equal order beliefs. The price reveals mu, not the synergy class.

Threshold tau is the belief at which rival gross profit equals high cost. Under the default rule, high cost prepares at or above tau. Entry is rho below tau and one otherwise."""),
("Frame 12 — A correct order earns between a fixed share and all of the spread","""These are gross gains before order cost k, for any order plan with Bayes beliefs, competitive prices and truthful bids.

Under good synergy, the purchase gain equals entry after a purchase times spread Delta T times one minus the purchase belief. Under poor synergy, the sale gain equals entry after a sale times Delta T times the sale belief. In words, entry times spread times doubt.

Kappa is the smaller of band floor m and one minus top belief M. For either class, the gain lies between rho times kappa times Delta T and Delta T itself.

A wrong order earns at most minus k. No order earns zero. The informed trader places its correct order if the gain exceeds k and abstains if the gain falls below k.

With entry and beliefs fixed, a wider spread raises these gross gains."""),
("Frame 13 — Strength can raise entry, then return it to its floor","""Proposition two compares three economies with the same class laws, reserve, costs, prior and order opportunity. F two lies below F one, which lies below F zero. Each step strengthens the incumbent. Beta here can be anything below one half, because the proof uses only the bounds after a purchase and a sale.

Delta sub i is the shareholder spread in economy i; B sub i is rival gross profit there. Three strict conditions do the work.

H one: weak-economy profit at the prior is below high cost, which is below strong-economy profit at top belief M.

H two: the weak spread is below order cost k, which is below rho times kappa times the strong spread.

H three: very-strong-economy profit at M is below high cost.

The table lists orders by synergy class, then beliefs and entry after a sale, no order and a purchase.

Against the weak incumbent, the informed trader abstains in each class. Every belief equals the prior, and entry equals rho.

Against the strong incumbent, the informed trader buys on good synergy and sells on poor synergy. Beliefs are m, pi and M; entry is rho, rho and one.

Against the very strong incumbent, those orders and beliefs persist. Entry returns to rho everywhere.

So a wider spread pays the informed trader to trade, and a purchase recruits. Against the very strong incumbent, profit at the top belief stays below the high cost.

Total entry is rho at both ends. In the middle it adds rho to the product of one minus rho and the sum b plus pi lambda, strictly above rho. Each economy has a unique equilibrium outcome, whichever way ties are broken. With the example's class values and reserve, these strict conditions hold on an open set of inputs.

The proof idea is short. The bounds from the last two frames hold for every candidate outcome. Strict gaps to the order cost and the high cost then fix orders, beliefs and entry. The four steps sit in backup B2."""),
("Frame 14 — Example: the top belief lies exactly between two thresholds","""The example fixes good-synergy value at ten and poor-synergy value at one. Reserve and prior are one half. Entry floor rho is one quarter; high cost is six; order cost k is one fiftieth.

Incumbent value is uniform from zero to r. The three strengths are r equal to one point two, three and three point six.

At these inputs, H one through H three hold exactly when the top belief lies strictly between two thresholds. The strong threshold is zero point seven zero five. The very strong threshold is about zero point seven three one four.

Set u to Euler's number minus one. Then the top belief is about zero point seven three one, below the upper threshold and above the lower one. Backup B10 lists each input and region."""),
("Frame 15 — With fixed information, strength cannot raise entry","""Now hold the information fixed. Fix the joint law of synergy class j and the rival's signal S. Keep both class value laws, reserve and cost law unchanged. The signal carries no further news about values within a class.

When F one lies weakly below F zero, total entry E one is at most E zero. At each unchanged belief, strength weakly lowers rival gross profit. It can remove a reason to prepare.

The table separates three comparisons. The first row solves orders again. Entry rises from rho against the weak incumbent to above rho against the strong incumbent.

The middle row imposes full informed orders at both strengths. Entry is above rho and equal at both. At the weak strength, those imposed orders lose money; this row is a control rather than an equilibrium there.

The last row hides the price and the order. The rival uses the prior. Entry stays at rho at both strengths."""),
("Frame 16 — Costly research rises with the spread, up to the cap","""One change from frame six. The informed trader now chooses presence lambda privately, at quadratic cost, with a cap below one. Market makers and the rival use its equilibrium level. With chance lambda it learns the synergy class and fills the slot. Otherwise liquidity fills the slot.

Keep ranked classes, prior one half, a positive rival gross-profit gap, and tau above one half. Research equals the smaller of the optimal interior root and the cap. The recruiting equilibrium exists exactly when the spread exceeds twice the order cost and the top belief at that research level reaches tau.

In it, research rises strictly with the spread until the cap, then stays fixed. Total entry and good-synergy entry rise with research. Poor-synergy entry falls. Backup B12 states the first-order condition."""),
("Frame 17 — At $F_1$, a visible price raises expected proceeds and net surplus","""Use Proposition two at the strong incumbent F one. Compare price access with a hidden price, with other primitives fixed.

Expected target proceeds and expected surplus net of preparation costs both rise strictly.

Access adds high-cost preparation only after a purchase, where gross profit at the top belief covers the high cost. Backup B4 gives the exact differences."""),
("Frame 18 — Purchase impact reveals recruitment","""Keep ranked classes, positive spread and rival gross-profit gap, full informed orders, and prior pi below threshold tau.

Purchase impact I plus is purchase price minus no-order price. Sale impact I minus is no-order price minus sale price. Weight each by its order frequency.

The weighted purchase impact exceeds the weighted sale impact exactly when purchase entry exceeds rho. At a prior of one half the frequencies match, so the raw impacts compare directly.

With no recruitment, orders can still predict the winner.

In data, date prices before preparation starts, fix the slot in advance, and record no trade as a zero outcome."""),
("Frame 19 — Competition can create competition","""Let me collect the results. Entry rises against the strong incumbent and returns to its floor against the very strong one. Strength weakly cuts rival gross profit and weakly widens the shareholder spread. A wider spread can make informed trade pay, so the price can carry news about synergy.

That rise works only through information: when what the rival can learn stays fixed, a stronger incumbent cannot raise entry.

With costly research, a wider spread pays for more research until the cap, and research sorts entry toward good synergy.

For sellers, a visible price raises expected target proceeds and net surplus against the strong incumbent. For data, a purchase moves the price more than a sale, weighted by frequency, exactly when it recruits.

So a stronger incumbent can induce rival entry through a more informative stock price. Thank you."""),
]
counts=[len(t.split()) for _,t in F]
total=sum(counts); wpm=105.
# cumulative end times from words, rounded to half minutes so the rows add up
out=[];cum=0;tcum=0.0;rows=[]
for (h,t),c in zip(F,counts):
    cum+=c; end=round(cum/wpm*2)/2; dur=end-tcum; tcum=end
    m,s=int(end),int(round((end-int(end))*60))
    rows.append((h,t,dur,f"{m}:{s:02d}"))
main=counts[1:]
tbl=[]
for i in range(10):
    a=f"{i+1} | {main[i]}"; b=f"{i+11} | {main[i+10]}" if i+10<len(main) else " | "
    tbl.append(f"| {a} | {b} |")
head=f"""# Competition Creates Competition — spoken script for the 19 main frames

Prepared speech: {tcum:.1f} minutes, including the title. Two minutes stay free within the 30-minute talk for pauses and clarifications.
Proposition 2 proof steps sit in backup B2 and in the prepared answer below; frame 13 states the proof idea in speech.
Headings, time lines, source comments and the word-count table are silent.
The handout has one face per frame. There are no click cues.
Headings match the slide frame titles. Speech uses the locked terms on the slides.
Word counts cover speech only. The title and prepared answers are separate from the main-frame total.

## Speech word counts

Count one whitespace-delimited token as one word. Hyphenated words count as one.

| Frame | Words | Frame | Words |
|---:|---:|---:|---:|
"""+"\n".join(tbl)+f"""

Main frames: **{sum(main):,} words**. Title: **{counts[0]} words**. Prepared speech including title: **{total:,} words**.

"""
body=""
for h,t,d,e in rows:
    unit='minute' if d==1 or d==0.5 else 'minutes'
    body+=f"## {h}\n\n*{d:.1f} {unit} · ends at {e}*\n\n{t}\n\n"
open(path,'w',encoding='utf8').write(head+body+tail)
print(total,tcum); print(counts); print([(r[2],r[3]) for r in rows])
