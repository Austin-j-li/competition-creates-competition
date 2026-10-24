# L3 voice comparison: the order-slot draft against the reference draft

**Scope.** This was a scan only. I did not edit any repository file, and I did not run a build.

**Sources.**
- Slot draft: `slot/manuscript/main.tex` and `slot/manuscript/sections/01–09`.
- Reference draft: `laplace/manuscript/main.tex (branch laplace)`, main text lines 149–1503.

**Location format.**
- Slot paths are relative to `slot/manuscript/`. For example, `sections/01_introduction.tex:12` is line 12 of `slot/manuscript/sections/01_introduction.tex`.
- `ref:164` means `laplace/manuscript/main.tex (branch laplace):164`.
- Slot quotes are verbatim LaTeX. Reference quotes give the printed text: they drop the `\citeproc{...}` and `\hyperref[...]{...}` wrappers and the source line breaks.

**Register.** The three sample rewrites in Section 3 use the register of the reference draft. That register has longer sentences when one thought needs them, semicolons, subordinate clauses, and participles where the reference uses them. The brief makes the author's request take priority over the controlled-language, short-sentence style that I otherwise use, and I followed the brief. My own analysis in this report keeps the short-sentence style.

---

## 1. The voice of the reference draft

### Paragraphs
- Each paragraph carries one argument, from claim to consequence. In the introduction and the model, paragraphs are long: the introduction median is about 130 words and 8 sentences. In the results, paragraphs are shorter.
- The best example is the mechanism paragraph at ref:166–185. That one paragraph runs the whole chain:
  1. the two claims;
  2. how the second-price rule splits a challenger's value;
  3. "The expected value gap between the classes is fixed by the classes alone. A stronger incumbent changes only who receives it." (ref:174–175);
  4. sensitivity against profit;
  5. the investor's trade;
  6. market makers who price the entry response;
  7. the close: "A larger gap in target proceeds can make that advantage worth the cost of trading." (ref:184–185).
- The setting paragraph at ref:164 has three sentences, joined by semicolons.

### Sentences
- The mean length is about 16 words, and the range is wide. About 7–9% of the sentences have 30 or more words.
- Long sentences join a condition to its consequence: "A disclosed approach, an announced strategic review, or an open contest can create such an interval if the opportunity becomes public before the buyer set is fixed; only then can a prospective buyer watch the price during the period that matters." (ref:245)
- Short sentences give emphasis, usually after a long one: "Public incumbent strength is a distribution, not a bid." (ref:273). Another example: "A stronger incumbent moves slices to the target. The spread rises and acquisition profit falls." (ref:613–614)
- Semicolons join a claim to its consequence or its contrast. The introduction has about 25 semicolons per 100 sentences.
- A list stays inside its sentence: "Before a buyer can submit a binding offer it must verify the target's contracts, liabilities, and technology, arrange financing and approvals, and commit evaluation capacity that has other uses." (ref:251–254)

### How it introduces the setting
- The decision interval is an economic situation, and the condition for it is in the same sentence (ref:245, quoted above). The next paragraph tells who is prepared, what preparation costs, and why the cost is an entry cost (ref:247–260).
- The evidence is part of the argument and points forward: "Disclosure records support the stage structure. Imprivata's definitive proxy separates ... These records document a costly preparation stage; Section 7 states how to test whether prices draw buyers into it." (ref:279–285)

### How it introduces notation
- The introduction has almost no symbols. It has one inline expression, `\([-1,1]\)` at ref:201.
- In the model, each symbol enters inside a sentence that gives its meaning in words: "At a belief \(\mu=\Pr(j=H)\), the challenger's expected gross profit is \(B(\mu)=g_L+\mu(g_H-g_L)\), because its value depends on the price only through its class." (ref:515–517)
- The class restrictions are prose with one display, not an Assumption environment (ref:318–326). Later text refers to them as "Under these restrictions" (ref:328).
- The equilibrium is one paragraph of prose: "An equilibrium specifies class-contingent order distributions \(\sigma_H,\sigma_L\), a measurable price function, Bayesian beliefs conditional on the observed price, optimal preparation, and truthful bidding." (ref:490–493)
- The timing is prose: "The sequence is as follows. The seller announces the sale rule. The investor learns the class and trades. Market makers set the price from flow. ..." (ref:481–486)

### How it states and explains results
- The main text has three results. Each has an inline bold head with a descriptive title (ref:582–583, ref:785–786, ref:1004–1005). The main text has no lemma, corollary, definition or remark. The formal statements go to the appendix: "Propositions A.1 and A.2 give the formal statements." (ref:730–731)
- Before a result comes a lead-in in plain words: "The main result identifies an open set of economies in which stronger competition changes the unique trading and on-path preparation outcome from an uninformative price with zero-cost preparation only to an informative price with additional high-cost preparation." (ref:778–781)
- After the result, each hypothesis gets one sentence of economics: "Condition (A1) excludes high-cost preparation at the weak-incumbent prior and permits it at favorable strong-incumbent prices. Condition (A2) places the trading cost above every informational return in the weak economy and below the global bound on marginal trading profit in the strong economy." (ref:847–851)
- Conditions are read in words: "Ownership needs its own condition when the class values overlap the incumbent's support. ... It holds whenever the high class rarely loses to the incumbent, and automatically when its values lie above the incumbent's support in both economies." (ref:919–925)

### How it carries intuition
- The intuition is causal, and it names the actors: "The market maker prices the entry response. Noise demand still hides the class. The investor's advantage is the entry probability times the spread times the market's residual uncertainty." (ref:751–753)
- Another example: "Dispersion within a class raises the challenger's option value of preparation. Preparation reveals the value, and the challenger profits only when it wins, so its gross profit is convex in the value; a spread around the same mean raises gross profit at every belief." (ref:1249–1253)
- A worked argument starts with an invitation: "To see why, take \(R>\ell\)." (ref:1395)

### How it handles citations and the literature
- Each literature sentence pairs a cited result with how this paper differs, joined by a semicolon and "here": "Edmans et al. (2015) show that corrective real decisions can discourage trading on bad news under rational pricing; here the real decision is the buyer's participation itself." (ref:210)
- A citation supports a model choice in the same sentence that makes the choice: "strategic and financial bidders differ systematically in their valuations (Gorbenko and Malenko 2014)" (ref:275).
- The main text has 4 footnotes.

### How it uses transitions
- Connective words carry the logic. Examples: "Thus" (ref:573), "nevertheless" (ref:941), and "Together, these comparisons identify the source of the reversal" (ref:986).
- A subsection often ends with a link to the next question: "Whether entry rises depends on how this change in payoffs affects equilibrium information." (ref:652–653)

### What not to copy from the reference
The reference is the model for register, not for every passage. The passages below have the habits that the author wants to remove. Do not carry them into the slot draft.
- ref:858–860: "so the proposition certifies a corner of the region in which the reversal occurs."
- ref:866–867: "None of these bounds locates the first informative equilibrium."
- ref:999–1000: "it does not identify the first informative equilibrium."
- ref:1089: "The full correspondence at intermediate strengths is open."
- ref:838–841: "The floor \(\rho>0\) is therefore an assumption with content: ..."
- ref:1153–1159: six short sentences in a row, one on each line. For example: "Laplace noise assigns positive probability to the upper posterior bound. Logistic noise assigns none." This is the slot draft's split-sentence habit, and here it occurs in the reference.

---

## 2. Where the slot draft departs

### Counts

| Measure | Slot (sections 01–09) | Reference (ref:149–1503) |
|---|---|---|
| Formal result environments in the main text | 15 (4 proposition, 3 lemma, 3 corollary, 1 definition, 1 assumption, 3 remark) | 3 (propositions with inline bold heads) |
| `enumerate` or `itemize` blocks | 14 | 0 |
| Cross-references to a Lemma, Corollary, Assumption, Definition or Remark | 21 | 0 |
| Footnotes | 12 | 4 |
| Inline math expressions in the introduction | 12 | 1 |
| Introduction paragraphs (median words) | 19 (93) | 11 (130) |
| Mean words in each sentence | 14.5 | 16.1 |
| Sentences of 30 or more words | about 1% (introduction 0%) | about 7% (introduction 9%) |
| Semicolons per 100 sentences | 4 (introduction 2) | 10 (introduction 25) |
| Paragraphs that start "Two ..." or "Three ..." | 8 | 2 |

A crude splitter produced the sentence measures. It replaces math with a token. Use these values to see the direction of the difference, not as exact values.

### Habit 1: split sentences
The slot draft cuts the reference's joined sentences into separate short ones. The connective word goes, and the logic goes with it.

- **Setting.** The reference (ref:164): "One buyer is already prepared, and another has not committed to the diligence that an executable proposal requires; Section 2.1 describes the decision interval ... Incumbent strength is the public distribution of the prepared bidder's value; a stronger incumbent shifts it upward, and no offer is announced before the challenger decides." The slot (sections/01_introduction.tex:11–15): "... requires. Section~\ref{sec:interval} describes the decision interval ... Incumbent strength is the public distribution of the prepared bidder's value, and a stronger incumbent shifts it upward. No offer is announced before the challenger decides." Three sentences become five.
- **Decision interval.** The reference sentence at ref:245 (quoted in Section 1) becomes three sentences at sections/02_model.tex:6–8: "A disclosed approach, an announced strategic review, or an open contest can create such an interval. The opportunity must become public before the buyer set is fixed. Only then can a prospective buyer watch the price during the period that matters." The condition "if" becomes a separate rule with "must".
- **Incumbent strength.** The reference (ref:273–275): "The record can reveal that a strategic acquirer with clear synergies is at the table, or that the prepared party is a financial buyer with a leveraged capital structure, without revealing what either would pay; strategic and financial bidders differ systematically in their valuations ..." The slot (sections/02_model.tex:32–35): "The record can reveal that a strategic acquirer with clear synergies is at the table. It can also reveal that the prepared party is a financial buyer with a leveraged capital structure. In each case it need not reveal what either buyer would pay. Strategic and financial bidders differ systematically in their valuations ..."
- **Preparation.** The reference's single list sentence (ref:251–254) becomes two sentences at sections/02_model.tex:15–16: "Before a buyer can submit a binding offer, it must verify the target's contracts, liabilities, and technology. It must also arrange financing and approvals and commit evaluation capacity that has other uses."
- **Literature.** The reference's semicolon pair at ref:210 becomes two sentences at sections/01_introduction.tex:105–107: "\citet{EdmansGoldsteinJiang2015} show that corrective real decisions can discourage trade on bad news under rational pricing. Here the real decision is the buyer's entry itself."
- **Conclusion.** The reference (ref:1484–1487) has one sentence: "A stronger incumbent can increase the sensitivity of target proceeds to challenger quality, making informed trading profitable and bringing a challenger into the auction." The slot conclusion opens with six sentences of 8 to 17 words (sections/09_conclusion.tex:3–7).

### Habit 2: one argument in several paragraphs, several topics in one paragraph
- The reference mechanism paragraph (ref:166–185) becomes three slot paragraphs (sections/01_introduction.tex:17–22, sections/01_introduction.tex:24–27, sections/01_introduction.tex:29–34).
- The paragraph at sections/01_introduction.tex:24–27 starts with the conclusion of the previous paragraph: "Target shares therefore become more sensitive ...". It then changes topic twice. First it turns to the investor ("It holds no net position in the target."), and then to the gains of shareholders.
- The model has the same pattern. The reference has one paragraph on the prepared buyer and the cost of preparation (ref:247–260). The slot has two (sections/02_model.tex:11–13 and sections/02_model.tex:15–20).

### Habit 3: lists, and paragraphs that start with a label
- The trading stage is two numbered lists. The first is "Trade takes place in one order slot:" with five items (sections/02_model.tex:125–136). The second is "The sequence is as follows:" with six items (sections/02_model.tex:175–184). The reference gives both in prose (ref:390–397, ref:481–486).
- The equilibrium is a Definition (sections/02_model.tex:206–241). It has a tuple, an itemize of six components, and six numbered conditions (E1)–(E6). After it comes a second itemize with the named tie rules IM, C1, I0 and CM (sections/02_model.tex:257–265). The reference uses one paragraph (ref:490–500).
- Many paragraphs start with a label sentence and then list definitions:
  - "Two numbers summarize the slot." (sections/02_model.tex:154)
  - "Two indifferences remain" (sections/02_model.tex:257)
  - "Two comparisons recur." (sections/02_model.tex:267)
  - "Two outcomes summarize an equilibrium." (sections/02_model.tex:273)
  - "Two controls show where the reversal comes from." (sections/04_equilibrium_results.tex:188)
  - "Two functions organize the path." (sections/04_equilibrium_results.tex:257)
- Other paragraphs start with a bare label: "The admissible region is a result." (sections/04_equilibrium_results.tex:116) and "The band is exact." (sections/04_equilibrium_results.tex:123).

### Habit 4: notation in the introduction
The reference introduction has one symbol. The slot introduction has 12 inline expressions, and some of them carry the argument.
- sections/01_introduction.tex:44–45: "Uniqueness covers every mixed order profile on the menu \(\{-1,0,1\}\) and every unilateral deviation. The posterior bounds hold for every profile, and they deliver this uniqueness."
- sections/01_introduction.tex:58–60: "At the benchmark auction primitives, they hold exactly when \(\reg{u_lo_frac}<u<\reg{u_hi_frac}\). Here \(u\) is the informed presence mass relative to the liquidity mass in one direction. The number \(1+u\) is the largest likelihood ratio that one order can carry."
- sections/01_introduction.tex:55 and sections/01_introduction.tex:65–68 bring in the thresholds \(r_C\), \([r_A,r_N]\) and \(r_F\), each with an approximate \(\reg{}\) value.

### Habit 5: the formal object comes before the economics
- **Class ranking.** The class ranking is an Assumption environment (sections/02_model.tex:67–73). The main text then cites it seven times as "Assumption~\ref{ass:classes}". The reference states the same restriction in prose (ref:318–326).
- **Section 3.** Section 3 puts three lemmas and one corollary in the main text (sections/03_competition_information.tex:97–108, sections/03_competition_information.tex:124–127, sections/03_competition_information.tex:139–150, sections/03_competition_information.tex:168–188). For the same content, the reference uses prose with displays (ref:658–771) and sends the formal statements to the appendix (ref:730–731).
- **Lead-in to the main result.** The main result starts with notation, not with its meaning: "Write \(F_0\), \(F_1\) and \(F_2\) for the three incumbent distributions, \(B_i=B_{F_i}\), \(\Delta_i=\DT(F_i)\), \(M=M(\pi)\), \(m=m(\pi)\) and \(\kappa=\kappa(\pi)\)." (sections/04_equilibrium_results.tex:7–9). Compare the reference lead-in at ref:778–781.
- **After the proposition.** The first paragraph after the proposition is proof bookkeeping, not economics: "Every investor comparison in the proof is strict ... Appendix~\ref{app:prop2} states the three equilibrium tuples and checks each condition of Definition~\ref{def:equilibrium} against them." (sections/04_equilibrium_results.tex:42–45)
- **Explanation of the hypotheses.** The text explains the hypotheses through a lemma, not through what they mean: "By Lemma~\ref{lem:trading}, every correct order earns at most \(\Delta_0-k<0\) in the weak economy and at least \(\rho\kappa\Delta_1-k>0\) in the strong one. The two sides of (H1) set entry." (sections/04_equilibrium_results.tex:47–49). Compare ref:847–851.
- **Conditions as formulas.** A condition stays a formula where the reference reads it in words: "The condition in part~(ii) holds whenever \((1+\rho)W_H(F_1)\ge2\rho W_H(F_0)>0\) and \(b+\lambda>1/2\)." (sections/04_equilibrium_results.tex:62–63). Compare "It holds whenever the high class rarely loses to the incumbent ..." (ref:924–925).

### Habit 6: proof talk in the main text
Some sentences say which part of which proof uses what:
- "Part~(c) is the only use of the bound \(\beta\le1/3\), and Corollary~\ref{cor:exclusion} uses it. Propositions~\ref{prop:ccc} and~\ref{prop:coexistence} and Corollary~\ref{prop:priors} use parts (a), (b) and (d) only, so they hold for every \(\beta<1/2\)." (sections/03_competition_information.tex:117–119)
- "Appendix~\ref{app:prop2} shows that the proof uses each hypothesis once and that (H1) cannot be weakened to \(B_1(\pi)<c_H\)." (sections/04_equilibrium_results.tex:51–52)
- "The upper margin is the smallest margin of Proposition~\ref{prop:ccc} in cost units, and it measures one distance in three units." (sections/04_equilibrium_results.tex:160)

The reference also has some proof talk (ref:498–500). It has less of it, and the proof talk comes after the economics.

### Habit 7: repeated claims
The claim about the residual advantage appears twice in the introduction (sections/01_introduction.tex:32–33 and sections/01_introduction.tex:44–45). It appears again at sections/02_model.tex:163–164, sections/03_competition_information.tex:190–192 and sections/09_conclusion.tex:4–6. Repetition across the introduction, the model and the conclusion is normal. In the introduction, one statement is sufficient.

---

## 3. Sample rewrites

Each rewrite keeps every fact, `\label`, `\ref`, citation key and macro of its span, and adds no fact, number, mechanism or citation. The three spans contain no `\reg{...}` macros. Sample C adds one new cross-reference, `\ref{sec:payoffs}`.

### Sample A: the opening of the introduction

**Original location:** `sections/01_introduction.tex:1–34` (the section head and the first five paragraphs, through the paragraph on the order slot).

```latex
\section{Introduction}\label{sec:intro}

At fixed information, a stronger incumbent reduces a prospective challenger's expected return from entry into a
takeover contest. The challenger must pay preparation costs before it can submit an executable offer, and a
stronger rival lowers what that preparation earns \citep{Fishman1988,HirshleiferPng1989}. I study a force in
the opposite direction. Competition can make the target's stock more informative about the challenger. When a
potential buyer observes that price before it commits to acquisition preparation, the information effect can
outweigh the loss of acquisition profits. A stronger incumbent then attracts another buyer and raises the
probability that a challenger from the high-value class acquires the target.

The setting is a listed target with a public sale opportunity. One buyer is already prepared, and another has
not committed to the diligence that an executable proposal requires; Section~\ref{sec:interval} describes the
decision interval in which that buyer decides while the target's stock trades. Incumbent strength is the public
distribution of the prepared bidder's value; a stronger incumbent shifts it upward, and no offer is announced
before the challenger decides.

The mechanism runs through two claims on the same acquisition surplus. The challenger holds the acquisition
claim, what it keeps if it prepares, bids, and wins; target shareholders hold the traded claim, what the cash
second-price auction pays them. The challenger's value comes from a high-value or a low-value quality class, and
the classes fix the expected value gap between them. A stronger incumbent outbids the challenger more often and
then pays the challenger's bid, so more of the gap reaches target proceeds; a challenger that wins pays more, so
less of the gap remains as acquisition profit at every belief. Target shares therefore become more sensitive to
information about the challenger at the same time as the challenger's own return to preparation falls.

An outside specialist investor with no net position in the target knows the challenger's class and trades on that
sensitivity. The trading stage is one order slot with the alternative-arrival structure of \citet{DowGorton1997}:
with some probability the investor fills the slot, and otherwise a liquidity trader fills it with a sale, a
purchase, or no order. No one observes who placed the order, and a liquidity order in the same direction is always
possible, so no order reveals the class. Under every investor strategy the posterior after every order stays inside
fixed bounds, and the investor keeps a residual advantage after every order; a larger gap in target proceeds can
make that advantage worth the cost of trade. Target shareholders gain when the price recruits entry, because a
holder through the sale receives sale proceeds, not the interim price.
```

**Notes.**
1. I did not change the first paragraph. It already reads like ref:151–162.
2. The second paragraph goes from five sentences to three, with the reference's semicolons (ref:164). "Consider a listed target" becomes "The setting is a listed target", as in the reference.
3. Paragraphs 3 to 5 of the original (sections/01_introduction.tex:17–34) become two paragraphs: the payoff split, then the trade. The sentence "Target shares therefore become more sensitive ..." moves back to close the payoff paragraph, because its "therefore" points to that argument. The reference puts this sentence at the same position (ref:178–180).
4. The investor's identity becomes the subject of the sentence that introduces the investor, as at ref:187–188. The sentence "It holds no net position in the target." therefore no longer stands alone. The sentence on shareholder gains moves to the end, after the text explains how the price recruits a challenger.
5. All facts come from sections/01_introduction.tex:3–34. One option comes from outside the span: "A stronger incumbent changes only who receives it." (ref:175). The slot draft states the same fact at sections/03_competition_information.tex:80–81. The author can add it after "the classes fix the expected value gap between them".

### Sample B: the trading stage

**Original location:** `sections/02_model.tex:117–185`, subsection "Trading: the order slot".

```latex
\subsection{Trading: the order slot}\label{sec:slot}

An investor observes the challenger's class \(j\). It is an outside sector specialist, such as a sector-focused
long-short fund, and it holds no net position in the target before trade; a holder with a full hedge counts as an
outsider in this sense. Its information concerns the challenger's fit with the target, and it forms that view from
its own research on the target's customers, technology, and demand, not from information that either bidder or the
target supplies.

Trade takes place in one order slot, a single public order opportunity that comes before the challenger's
decision. With probability \(\lambda\in(0,1)\) the informed investor fills the slot: it sees the class \(j\) and
chooses an order \(q\in\{-1,0,1\}\), and a nonzero order costs \(k>0\). With probability \(1-\lambda\) a liquidity
trader fills the slot instead and, for exogenous reasons apart from the sale, sells, abstains, or buys one unit
with probabilities \(\beta\), \(1-2\beta\), and \(\beta\), where \(0<\beta\le1/3\). A liquidity sale comes from a
current shareholder who sells for cash, a liquidity purchase from an outside investor, and an abstention means
that the opportunity passes with no order; I write \(\eta(-1)=\eta(1)=\beta\) and \(\eta(0)=1-2\beta\) for this
liquidity order distribution. No one observes who filled the slot, and the identity draw is independent of the
class, the costs, and the incumbent's value.

Competitive market makers see the order \(X\in\{-1,0,1\}\), set the price \(P=\E[V_T\mid X]\), where \(V_T\) is
the terminal payoff of a target share, and absorb the order at that price; each share held at the sale,
market-maker inventory included, receives \(V_T\). If the investor fills the slot with order \(q\), its order is
the whole order that market makers see, so it trades at the price \(P(q)\) and earns
\begin{equation}\label{eq:profit}
q\,[V_T-P(q)]-k|q|.
\end{equation}
The unit is a normalized small trading unit, not ownership of the target. The cost \(k\) is a separate friction,
such as an execution cost or a cost to carry the position, and it is distinct from adverse-selection price impact,
which the competitive price already generates. The investor's order after bad news is a short sale, and \(k\)
includes the cost to borrow shares.

A liquidity order in a given direction arrives with probability \(b=(1-\lambda)\beta\), and the ratio
\(u=\lambda/b\) is the informed presence mass relative to the liquidity mass in one direction; the number \(1+u\)
is the largest likelihood ratio that one order can carry. Section~\ref{sec:inference} shows that, under every
investor strategy, the posterior after every order lies in \([m(\pi),M(\pi)]\), where
\begin{equation}\label{eq:bounds}
M(\pi)=\frac{\pi(1+u)}{\pi(1+u)+1-\pi},\qquad
m(\pi)=\frac{\pi}{\pi+(1-\pi)(1+u)}.
\end{equation}
The bounds follow from one property of the slot: each class reaches each order through a liquidity trader, so no
order is conclusive about the class, and the investor therefore keeps a residual advantage after every order.

The slot uses the alternative-arrival structure of \citet{DowGorton1997}, in which an informed order and a
liquidity order of the same size are alternative arrivals in one opportunity; in \citet{AdmatiPfleiderer2009}, a
liquidity shock forces the informed holder's own sale, so a sale occurs on path for both motives. The unit order
menu, the presence probability, and the symmetric unit cost follow \citet{EdmansGoldsteinJiang2015}, and
risk-neutral market makers with zero expected profit price each order, as in \citet{GlostenMilgrom1985} and
\citet{Kyle1985}. Here the terminal payoff depends on the price through preparation.

Market makers observe the order \(X\) and nothing else. The challenger observes the price \(P\) and its own cost
\(C\), but not \(X\), its class, its value, or the incumbent's value; the investor observes the class \(j\) but
not the value \(\theta\), and the incumbent knows its own value. The sequence is as follows. The seller announces
the sale rule. The investor learns the class, the slot draw selects the investor with probability \(\lambda\) and
a liquidity trader otherwise, and the selected trader places its order. Market makers set the price from the
order, and the challenger observes the price and its cost and decides whether to prepare. Prepared bidders then
learn their values and submit their bids, and ownership and financial payoffs are realized.
Section~\ref{sec:research} adds a research stage before the investor learns the class.
```

**Notes.**
1. The two numbered lists (sections/02_model.tex:125–136 and sections/02_model.tex:176–184) become prose. The sequence follows the reference pattern "The sequence is as follows. The seller announces the sale rule. ..." (ref:481–486). Without numbered steps, "before step (2)" (sections/02_model.tex:185) becomes "before the investor learns the class". Step (2) of the original starts with that event, and the research stage at sections/05_research.tex:4 comes "Before it learns the class".
2. The original describes the liquidity trader twice: in list item (3), and again at sections/02_model.tex:149–152. The rewrite gives one description that says what the trader does and who the trader is, as at ref:458–462. "Its motive is exogenous" and "for reasons apart from the sale" become one phrase.
3. The label opener "Two numbers summarize the slot." (sections/02_model.tex:154) is gone. One sentence now defines \(b\) and \(u\). The property that produces the bounds comes directly after the display, as the explanation of the bounds.
4. Short sentences that carry one thought are joined with commas and semicolons, as at ref:475–481. Examples are the two sentences on \(k\) as a friction and the information sets.
5. The rewrite keeps all items that later text uses:
   - the labels `sec:slot`, `eq:profit` and `eq:bounds`;
   - the definition of \(\eta\), which sections/02_model.tex:223, sections/02_model.tex:245, sections/03_competition_information.tex:100 and the appendix use;
   - the bound \(0<\beta\le1/3\), which sections/03_competition_information.tex:117 uses;
   - the independence sentence;
   - "\(k\) includes the cost to borrow shares" and "market-maker inventory included";
   - all five citation keys.

### Sample C: the main result

**Original location:** `sections/04_equilibrium_results.tex:1–69`: the set-up paragraph, Proposition 2 and the discussion after it.

```latex
\section{Equilibrium results}\label{sec:results}

\subsection{Competition creates competition}\label{sec:ccc}

The main result compares three economies that differ only in incumbent strength. Against a weak incumbent the
price carries no information and only a zero-cost challenger prepares; against a strong incumbent the price is
informative and a purchase recruits a high-cost challenger; against a very strong incumbent the price stays
informative, but entry returns to its floor. I write \(F_0\), \(F_1\) and \(F_2\) for the three incumbent
distributions, \(B_i=B_{F_i}\) and \(\Delta_i=\DT(F_i)\) for gross profit and the target-payoff spread in each,
and \(M\), \(m\) and \(\kappa\) for \(M(\pi)\), \(m(\pi)\) and \(\kappa(\pi)\).

\begin{proposition}[Competition creates competition; analytical]\label{prop:ccc}
Let the high class dominate the low class, with both class supports above the reserve
(Assumption~\ref{ass:classes}). Let \(F_1\) be a continuous first-order stochastic strengthening of the continuous
incumbent distribution \(F_0\), let \(F_2\) strengthen \(F_1\) in the same sense, and fix \(0<\pi<1\),
\(0<\rho<1\), \(k>0\) and a slot \((\lambda,\beta)\). Suppose that the high cost lies between gross profit at the
prior against \(F_0\) and gross profit at the top posterior against \(F_1\), that the trading cost lies between
the spread at \(F_0\) and the fraction \(\rho\kappa\) of the spread at \(F_1\), and that gross profit at the top
posterior against \(F_2\) falls short of the high cost:
\begin{align*}
&\text{(H1)}\qquad B_0(\pi)<c_H<B_1(M),\\
&\text{(H2)}\qquad \Delta_0<k<\rho\,\kappa\,\Delta_1,\\
&\text{(H3)}\qquad B_2(M)<c_H.
\end{align*}
Then each economy has a unique equilibrium outcome.
(i) Against the weak incumbent \(F_0\), the investor does not trade. Every posterior equals \(\pi\), entry equals
\(\rho\) after every order, and every order has the price \(t_0+\rho\,[t_L-t_0+\Delta_0\pi]\), so the price
carries no information.
(ii) Against the strong incumbent \(F_1\), the investor buys when the class is \(H\) and sells when it is \(L\),
and the posteriors after a sale, no order and a purchase are \(m\), \(\pi\) and \(M\). Only a purchase recruits
the high-cost challenger, so entry after the three orders is \(\rho\), \(\rho\) and \(1\), the price rises from a
sale through no order to a purchase, and entry overall and given class \(H\) is
\[
\Ent_1=\rho+(1-\rho)(b+\pi\lambda)>\rho,\qquad e_H=\rho+(1-\rho)(b+\lambda).
\]
High-class ownership rises from \(\pi\rho W_H(F_0)\) to \(\pi e_HW_H(F_1)\) if and only if
\(e_HW_H(F_1)>\rho\,W_H(F_0)\).
(iii) Against the very strong incumbent \(F_2\), the investor again trades in both directions, with posteriors
\(m\), \(\pi\) and \(M\), and the three prices differ; the price stays informative, but entry returns to \(\rho\)
after every order.
\end{proposition}

The hypotheses separate the two forces of Section~\ref{sec:payoffs}. Hypothesis (H1) concerns acquisition
profit: gross profit at the prior falls short of the high cost against \(F_0\), so an uninformative price recruits
no high-cost challenger, while gross profit at the top posterior exceeds it against \(F_1\), so a purchase can.
Hypothesis (H2) concerns the return to information, and it fixes trading before any order profile is known: by
Lemma~\ref{lem:trading}, every correct order earns at most \(\Delta_0-k<0\) in the weak economy and at least
\(\rho\kappa\Delta_1-k>0\) in the strong one. Hypothesis (H3) stops recruitment at \(F_2\)
(Corollary~\ref{cor:exclusion}).

The trading window in (H2) is nonempty exactly when \(\Delta_0/\Delta_1<\rho\kappa\), that is, when competition
widens the target-payoff spread enough from \(F_0\) to \(F_1\). This condition involves the two incumbent
distributions, the classes, \(\rho\), the slot and \(\pi\), and no unit of money; a prior away from one half
narrows the window, since \(\kappa(\pi)\) falls. For uniform incumbents, (H1)--(H3) are strict inequalities
between continuous functions of \((r_0,r_1,r_2,c_H,k,\rho,\pi,\lambda,\beta)\), so they define an open set, and
Section~\ref{sec:benchmark} gives its slice through the benchmark.

The additional entry favors the high class, which places a purchase with probability \(b+\lambda\) against \(b\)
for the low class. Ownership needs its own condition when the high class can lose to the incumbent, because a
stronger incumbent then lowers \(W_H\). The condition in part~(ii) holds whenever the stronger incumbent does not
cut the high class's chance of winning by too much, \((1+\rho)W_H(F_1)\ge2\rho W_H(F_0)>0\), and class \(H\)
places a purchase more often than not, \(b+\lambda>1/2\). In the point-mass benchmark \(W_H=1\), so ownership
rises.

Part~(iii) completes a rise and a later fall of entry with incumbent strength. Against the very strong incumbent,
even the top posterior fails to justify high-cost preparation, while trading stays informative;
Section~\ref{sec:coexistence} describes the strengths between the three economies.

Every investor comparison in the proof is strict, and every equilibrium posterior lies strictly on one side of
the threshold, so no tie rule is used and the same unique outcome holds under all four pairs of tie rules.
Appendix~\ref{app:prop2} states the three equilibrium tuples, checks each condition of
Definition~\ref{def:equilibrium} against them, and shows that the proof uses each hypothesis once and that (H1)
cannot be weakened to \(B_1(\pi)<c_H\).
```

**Notes.**
1. **Lead-in.** The lead-in gives the three outcomes in one sentence with semicolons, as at ref:778–781. The notation sentence comes last, directly before the result that uses it. The notation stays because later text uses it (sections/04_equilibrium_results.tex:111, sections/04_equilibrium_results.tex:117, sections/06_robustness.tex:11 and the appendix).
2. **Format of the result.** The proposition stays in the amsthm environment. The plain style of that environment already prints an inline bold head ("**Proposition 2** (Competition creates competition; analytical).") with an italic body. It also keeps `\label{prop:ccc}` for the 39 references to it. If the author wants the reference's head, which is all bold (ref:785–786), a theorem-style change in `main.tex` gives it, and no section file changes. The reference's `\phantomsection\label` device can also give that head. But with that device, `\ref` prints the correct number only after a `\refstepcounter{proposition}`.
3. **Hypotheses and parts in words.** One sentence states the hypotheses in words before the display. The tags (H1)–(H3) stay, because sections/04_equilibrium_results.tex:111, sections/04_equilibrium_results.tex:117, the note to Table 2 (sections/04_equilibrium_results.tex:148), sections/06_robustness.tex:11 and the appendix refer to them. To rename the tags, those places must change too. The parts are now in words. The rewrite removes the \(\delta_q\) notation from the statement, because the words say the same; the table at sections/04_equilibrium_results.tex:206 still uses \(\delta_q\), which sections/03_competition_information.tex:90 defines. Formulas that words cannot carry stay: entry, \(e_H\), the ownership condition, and the price in part (i).
4. **Order of the discussion.** After the result, the intuition comes first and the bookkeeping comes last. The facts about the tie rules and the structure of the proof become a closing paragraph of two sentences that ends on the appendix pointer. Nothing is deleted.
5. **Glosses to check.** Two glosses restate inequalities of the span in words: "that is, when competition widens the target-payoff spread enough from \(F_0\) to \(F_1\)" (for \(\Delta_0/\Delta_1<\rho\kappa\)), and "class \(H\) places a purchase more often than not" (for \(b+\lambda>1/2\)). The opening "The hypotheses separate the two forces of Section~\ref{sec:payoffs}" is a reading of (H1) as a condition on profit and (H2) as a condition on the spread. The author should check that these readings say what the author means.

---

## 4. What the slot draft does better and should keep

1. **Every number prints through `\reg{...}`.** The reference puts decimals directly in the prose ("Entry nevertheless rises from 0.250000 to 0.522757", ref:941–942) and in a display of certified intervals in the main text (ref:1010–1017).
2. **One topic in each paragraph of the introduction's tour of results:**
   - coexistence (sections/01_introduction.tex:64–70);
   - research (sections/01_introduction.tex:72–78);
   - robustness (sections/01_introduction.tex:80–86);
   - welfare and sale terms (sections/01_introduction.tex:88–94);
   - tests (sections/01_introduction.tex:96–100).

   The reference puts classes, dispersion, noise laws, cost laws, signals, coexistence, non-monotonicity and welfare into one paragraph of about 300 words (ref:206).
3. **One word for one thing.** The slot draft uses "entry" (223 times) and "entry cost" (sections/02_model.tex:19–20). The reference moves among "participation cost" (ref:259), "Preparation rises" (ref:199) and "Entry nevertheless rises" (ref:941) for the same thing.
4. **Bold statements where the reference hedges.**
   - The slot draft states the complete equilibrium set on the path (sections/04_equilibrium_results.tex:296–322). The reference says "it does not identify the first informative equilibrium" (ref:999–1000) and "The full correspondence at intermediate strengths is open." (ref:1089).
   - The slot draft says "Together, the two controls locate the reversal. Incumbent strength changes the information that trading generates, and the entry response to that information exceeds the direct deterrence effect." (sections/04_equilibrium_results.tex:248–249). The reference says the entry response "can exceed" the deterrence effect (ref:986–988).
5. **The zero-cost floor without the hedge.** sections/03_competition_information.tex:158–161 keeps the "three jobs" of the floor and drops the reference's "The floor \(\rho>0\) is therefore an assumption with content: ..." (ref:838–841).
6. **Intuition passages that already match the target register.** Keep them as they are:
   - the slices argument (sections/03_competition_information.tex:60–69);
   - "A stronger incumbent leaves the value gap between the classes unchanged. It moves the gap from the challenger's profit to target proceeds." (sections/03_competition_information.tex:80–81);
   - "The class that the prior favors binds, because the price already leans toward it." (sections/03_competition_information.tex:198–199);
   - "Entry rises strictly along R because the purchase rate adjusts." (sections/04_equilibrium_results.tex:352);
   - "A success takes the place of a liquidity order because the opportunity has room for one order. ... More research therefore also removes liquidity orders, and it reduces the camouflage of the investor's own orders." (sections/05_research.tex:16–19).
7. **A trading section with one mechanism.** The slot draft does not have the reference's digression on noise laws: score bounds, three ways to build the Laplace law, and citations on tail weight (ref:407–439). The model section therefore stays on the paper's one mechanism.
8. **Paragraphs already in the reference's register.** The first paragraph of the introduction (sections/01_introduction.tex:3–9) and the main-result paragraph (sections/01_introduction.tex:36–41) are close to ref:151–162 and ref:192–201. Sample A keeps the first paragraph unchanged.
9. **Exact empirical statements.** One example: "The purchase impact exceeds the sale impact exactly when a purchase recruits the buyer." (sections/01_introduction.tex:96–97). The reference states its predictions less exactly (ref:1468–1474).
10. **Secondary literature in footnotes.** The footnotes at sections/01_introduction.tex:111–112, sections/01_introduction.tex:117–120, sections/01_introduction.tex:124–128 and sections/01_introduction.tex:133–136 keep each literature paragraph on one contrast. The reference's equivalent paragraph is about 230 words of citations (ref:212). Keep the footnotes, but join each main "X show ...; here ..." pair into one sentence again, as at ref:210.
