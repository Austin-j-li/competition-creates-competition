# Main-text wording targets

The prose writer drafts the target wording of every main-text claim whose wording differs from the current manuscript or is added to it, in the order of the paper, as LaTeX source as it will stand in the manuscript. The referee marks each target "match", "missing qualifier" or "overclaim". The basis is `plan/lens_maintext.md` 3.1, adjusted to rule 4 (the example is neutral), to the vocabulary of `plan/NOTATION.md` part (b), and with every implicit qualifier written out.

Each target gives:

- **Location**: the section, and the current lines it stands in place of, or "added after" a line. Files: `main` is `slot/manuscript/main.tex`; `01` to `09` are `slot/manuscript/sections/01_introduction.tex` to `09_conclusion.tex`.
- **Matches**: the formal result, by `PLAN.md` S5 item (1 = A2, 2 = A3 and A6, 3 = A4, 4 = A5, 5 = A8) and the section of the referee report (W1 to W5).
- **Scope**: prior; tie rules, in the phrases of `NOTATION.md`; trading pattern; named condition; weak or strict.
- **LaTeX**.

Conventions used throughout:

- Every quantity of the example prints through `\reg{}`, and every key exists in the numbers table; the section "Keys used by the targets" lists the keys added to the numbers table for these targets. Constants that are part of a formula or a hypothesis (the prior \(1/2\), \(2k\), \(1/3\), \(3p^2\)) are written as mathematics, as in the current manuscript.
- "The default tie rules" is defined once, in Section 2 (target 2.5): an indifferent investor may mix over its best orders, and an indifferent high-cost challenger prepares.
- "Full two-sided trade": class \(H\) buys and class \(L\) sells, each with probability one. Defined once, at the opening of Section 8 (target 8.1); the introduction says it in words.
- Corollary labels are the frozen ones: Corollary 1 is `prop:region` (second label `cor:ccc-example`), Corollary 2 is `cor:example-coexistence`, and Corollary 3 is `cor:research` in its full statement and `cor:research-short` in the main-text form. The label `sec:benchmark` of Section 4.2 is kept so that no reference breaks; labels do not print.
- "The exact recruitment margin" names \(\varphi_a^*\) in the main text; "the recruitment margin" is not used for it.
- Proposition 1 keeps its statement. Figures and their notes are outside this file (S7).

---

## Abstract

### T-ABS. Second paragraph of the abstract

- **Location**: `main:79–85`, in place of the second paragraph. The first paragraph and the title stay.
- **Matches**: S5 item 2 (Proposition 2 with its share part; Proposition A.5, the open set with ownership); S5 item 3 (Proposition 3(a)); S5 item 1 (the two numbers); S5 item 4 (Proposition 4(a), (b)); Proposition A.8 (access to prices). W1 "Shared Candidate 1"; W3 "Shared Candidate 1" sections 3 to 5; W2 "Shared Candidate 3".
- **Scope**:
  - prior: any prior for the first four sentences; "an even prior" for research;
  - tie rules: "an indifferent investor may mix over its best orders" named for research; the coexistence sentence relies on the default tie rules of the model (see the points for the referee, item 5);
  - trading pattern: none named; research names "the equilibrium in which a purchase after successful research recruits";
  - condition: "on an open set of parameters" governs the first sentence, including the ownership clause; "in the strong-incumbent economy" is the economy \(F_1\) of Proposition 2 under (H1) to (H3);
  - weak or strict: entry rises strictly; "can only lower" is weak; "rises ... and then stays constant".
- No empirical sentence.

```latex
On an open set of parameters, a stronger incumbent turns an uninformative price into an informative one, with unique
trading and preparation outcomes; challenger entry rises, and so does the probability that a challenger from the high
class acquires the target. With the information in the price held fixed, a stronger incumbent can only lower entry.
A quiet market and an informative market coexist exactly on a region of two numbers, the target-payoff spread, which
measures how much target proceeds depend on the challenger's class, and the belief that preparation at the high cost
requires; a stronger incumbent moves the economy across that region, and in the informative market entry rises with
the spread and then stays constant. When the investor pays for research, the prior is even and an indifferent
investor may mix over its best orders, research and entry rise together with the spread until research reaches its
cap, in the equilibrium in which a purchase after successful research recruits. In the strong-incumbent economy,
access to prices raises expected target proceeds and acquisition surplus net of preparation costs.
```

---

## 1. Introduction

### T-1.1. Opening claim

- **Location**: Section 1, `01:8–9`, in place of the sentence "A stronger incumbent then attracts another buyer and raises the probability that a challenger from the high class acquires the target."
- **Matches**: S5 item 2 (Proposition 2 on its open set; Proposition A.5). W2 "Do the same workarounds cover Proposition 2".
- **Scope**: prior: any; tie rules: none needed (every comparison of Proposition 2 is strict); trading pattern: none; condition: "can" marks the existence statement of Proposition 2 on its open set; weak or strict: strict.

```latex
A stronger incumbent can then attract another buyer and raise the probability that a challenger from the high class
acquires the target.
```

### T-1.2. The main result

- **Location**: Section 1, `01:38–43`, in place of the text from "challenger, so entry rises" (line 39) to the end of the paragraph (line 43).
- **Matches**: S5 item 2 (Proposition 2(ii) and its share part). W2 "Shared Candidate 3"; W2 "Do the same workarounds cover Proposition 2" (outbidding at \(F_1\) forces it at \(F_0\)); proof O6.
- **Scope**: prior: any; tie rules: none needed; trading pattern: the strong incumbent's full two-sided trade, stated in the preceding sentence; condition: a prepared high-class challenger beats the strong incumbent for sure; the share clause stands inside that condition and adds that a low-class challenger beats the weak incumbent with positive probability; weak or strict: ownership and share rise strictly under the stated conditions.

```latex
challenger, so entry rises even though acquisition profit falls at every fixed belief. When a prepared high-class
challenger beats the strong incumbent for sure, the probability that a challenger from the high class acquires the
target rises with entry; if, in addition, a low-class challenger beats the weak incumbent with positive probability,
the high class also wins a larger share of the takeovers that go to a challenger. With the very strong incumbent, the
price stays informative, but even the most favorable price fails to justify preparation at the high cost, so entry
returns to its floor.
```

### T-1.3. The example as an illustration of the main result

- **Location**: Section 1, `01:50–59`, in place of the paragraph.
- **Matches**: Corollary 1 (S5 item 2, the full Corollary 1 from Proposition A.1(a)); the example rows of Table 1. W2 "Benchmark verification".
- **Scope**: prior: \(1/2\) for the band in \(u\); the example's prior for the values; tie rules: none needed in the open band; trading pattern: that of Proposition 2; condition: the example's auction and costs; weak or strict: strict band.

```latex
As an illustration, in the example of Section~\ref{sec:benchmark}, entry rises from \reg{entry_r0} at the weak
incumbent to \reg{entry_r1_B} at the strong incumbent, high-class ownership rises from \reg{own_r0} to
\reg{own_r1_B}, and the high class's share of the takeovers that go to a challenger rises from
\reg{share_H_r0} to \reg{share_H_r1_B}. Over the same change, gross acquisition profit at the prior falls
from \reg{Bprior_r0} to \reg{Bprior_r1_B}, while the target-payoff spread rises from \reg{Delta_r0} to
\reg{Delta_r1}. In the example, high-cost preparation stops above the entry ceiling, the strength
\(r_C\approx\reg{rC_B}\). At the example's auction and costs and the prior \(1/2\), the hypotheses of the main
result hold exactly when \(\reg{u_lo_frac}<u<\reg{u_hi_frac}\), where \(u\) is the informed presence mass relative
to the liquidity mass in one direction; equivalently, the top posterior at the prior \(1/2\) lies between the
preparation thresholds of the strong and the very strong incumbent, \(\reg{M_lo_frac}\) and \(\reg{M_hi_frac}\)
(Corollary~\ref{prop:region}).
```

### T-1.4. The two numbers and coexistence

- **Location**: Section 1, `01:61–67`, in place of the paragraph.
- **Matches**: S5 item 1 (the reduction lemma and the two numbers along a path); S5 item 3 (Proposition 3(a) to (c)); Corollary 2. W1 "Shared Candidate 1"; W1 "Solver B 1"; W1 "Solver B 2"; W1 "Solver A 2 and Solver C 3".
- **Scope**:
  - prior: any for the general sentences; \(1/2\) for the example;
  - tie rules: "an indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares", named once for coexistence;
  - trading pattern: the informative market's purchase, mixed or sure;
  - condition: target proceeds and acquisition profit both higher with a high-class challenger (\(\DT>0\), \(g_H>g_L\)); the threshold statement holds while \(g_L\le c_H\); the whole-set interval needs the balance condition, both of its parts;
  - weak or strict: "never narrows", "never lowers" are weak; entry rises strictly while the investor mixes.

```latex
When target proceeds and acquisition profit are both higher with a high-class challenger, the investor's orders, the
posteriors and the challenger's preparation depend on the auction only through two numbers: the target-payoff spread
and the preparation threshold, the belief that a high-cost challenger needs before it prepares
(Section~\ref{sec:twonumbers}). A stronger incumbent never narrows the spread, and it never lowers the threshold while
a challenger known to be in the low class would not prepare at the high cost. When an indifferent investor may mix
over its best orders and an indifferent high-cost challenger prepares, a quiet market, in which the investor does not
trade, and an informative market coexist exactly when the threshold lies above the prior and within reach of a
purchase, and the spread is wide enough that a purchase that just reaches the threshold covers the trading cost but
narrow enough that no order against an uninformative price earns more than it (Section~\ref{sec:coexistence}). In the
informative market, entry depends on the incumbent only through the spread: it rises with the spread while the
investor mixes between a purchase and abstention, and it stays constant once the investor buys for sure. Along any
path of strengthening incumbents, the strengths at which a quiet market coexists with a sure purchase form one
interval. The whole set of strengths with coexistence is one interval when the high class's gross profit exceeds the
high cost against the weakest incumbent and the spread grows, in proportion, at least as fast as that excess shrinks.
As an illustration, in the example at the prior \(1/2\) the strengths with coexistence form the interval from
\(r_A\approx\reg{rA}\) to \(r_N\approx\reg{rN}\), and the investor buys for sure from \(r_F\approx\reg{rF_B}\).
```

### T-1.5. Research

- **Location**: Section 1, `01:69–75`, in place of the paragraph.
- **Matches**: S5 item 4 (Proposition 4(a) to (c)); Corollary 3. W3 "Shared Candidate 1" sections 2 to 5; W2 "Shared Candidate 1"; W3 "The benchmark".
- **Scope**:
  - prior: "the prior is even", that is \(1/2\);
  - tie rules: "an indifferent investor may mix over its best orders" named; the example's list uses the default tie rules (Corollary 3);
  - trading pattern: "the equilibrium in which a purchase after successful research recruits a high-cost challenger";
  - condition: existence needs a spread above twice the trading cost and a threshold above the prior; ownership needs a prepared high-class challenger to beat the incumbent for sure;
  - weak or strict: research rises strictly with the spread up to the cap; entry rises with research.

```latex
When the investor pays for research that can make it informed, the prior is even and an indifferent investor may mix
over its best orders, research and entry rise together with the target-payoff spread until research reaches its cap,
in the equilibrium in which a purchase after successful research recruits a high-cost challenger
(Section~\ref{sec:research}). The investor chooses the probability of success up to a cap, at a quadratic cost.
Where the spread exceeds twice the trading cost and the preparation threshold lies above the prior, this equilibrium
exists exactly when the posterior after a purchase, at the research the investor chooses, reaches the threshold. The
low class's selling on bad news leaves the rise in place: the low class first sells only as often as keeps its sale
at break-even, which adds nothing to the value of research, and once a sure sale pays, the sale's profit adds a
second return to research. When a prepared high-class challenger beats the incumbent for sure, high-class ownership
rises with research. As an illustration, in the example research rises from \reg{res_lambda_r155} at the strength
\reg{str_r155} through \reg{res_lambda_r160} at \reg{str_r160} to \reg{res_lambda_r165} at \reg{str_r165}, and entry
from \reg{res_entry_r155} through \reg{res_entry_r160} to \reg{res_entry_r165}; research reaches its cap at about
\reg{res_rcap} and stays there up to the entry ceiling. In the example, the unique outcome has no research against
the weak incumbent and research at the cap against the strong incumbent.
```

### T-1.6. Welfare and the payment rule

- **Location**: Section 1, `01:86–89`, in place of the sentence "An alternative bargaining institution shows how the payment rule matters: ... (Section~\ref{sec:payment})." The other sentences of `01:85–91` stay; "a reserve that excludes the low class" stays as the phrase of `NOTATION.md`.
- **Matches**: Proposition A.9 (point masses \(\ell\) and \(h\) with \(0<\ell<\bar r<h\)).
- **Scope**: prior: any; tie rules: those of Proposition A.9; trading pattern: none; condition: one value per class, with the incumbent's highest value between them; weak or strict: not applicable.

```latex
With a single value in each class and the incumbent's highest value between them, an alternative bargaining
institution shows how the payment rule matters: the effect of competition on the target-payoff spread depends on the
weight the rule places on the runner-up's value (Section~\ref{sec:payment}).
```

### T-1.7. Empirical implications

- **Location**: Section 1, `01:93–98`, in place of the paragraph.
- **Matches**: S5 item 5 (the weighted price test; orders predict the winner; identification at a known prior and by the sale price). W5 "Shared candidate 1"; W5 "Full two-sided trade"; W5 "Sale-price identification with an unknown prior" (its known-prior part only, decision 5); W4 "general identity and its sign" (Solver C 1, Solver B 3, Solver E 1(a)–(b)); W4 "the covariance constants agree".
- **Scope**:
  - prior: below the threshold for the weighted test; known and different from one half for counts; \(1/2\) for the sale-impact sentence;
  - tie rules: none needed when the prior lies strictly below the threshold;
  - trading pattern: the investor always buys after good news and always sells after bad news, that is, with probability one (full two-sided trade), named once in the LaTeX and governing the paragraph;
  - condition: winners need the incumbent's value to fall, with positive probability, where the classes differ in their chance of beating it; the sale-impact sentence needs the payoff scale and entry at its floor after a sale and after no order;
  - weak or strict: "exactly when"; "more often" is strict.

```latex
When the investor always buys after good news and always sells after bad news and the prior lies below the
preparation threshold, a purchase raises the price by more than a sale lowers it, once each impact is weighted by how often its order
occurs, exactly when the purchase recruits the challenger; the test needs only prices and order frequencies
(Section~\ref{sec:empirical}). The difference comes from the entry component of the price gap between a purchase and
a sale; in the example at the strong incumbent, that component is \reg{ba_share_r1_B} of the price gap. Under the
same trading pattern, a prepared challenger wins more often after a purchase than after a sale whenever the
incumbent's value sometimes falls where a high-class value is more likely than a low-class value to beat it, and
where entry stays at its floor after every order, so that orders no longer predict entry, they still predict the
winner. Order counts identify the informed investor's presence when the prior is known and differs from one half,
and at the prior \(1/2\) the sale impact identifies it, given the payoff scale and entry at its floor after a sale
and after no order.
```

### T-1.8. Roadmap

- **Location**: Section 1, `01:136–140`, in place of the paragraph.
- **Matches**: the structure of `PLAN.md` "S9 and S10"; the numbering map (Corollaries 1 to 3 in full in the appendix).
- **Scope**: not a result.

```latex
Section~\ref{sec:model} sets out the model, and Section~\ref{sec:payoffs} derives the returns to information and the
two numbers through which trading sees the auction. Section~\ref{sec:results} states the main results and introduces
the example. Sections~\ref{sec:research} to~\ref{sec:empirical} cover research, robustness, welfare and sale terms,
and empirical implications, and Section~\ref{sec:conclusion} concludes. Appendix~\ref{app:proofs} states
Propositions~\ref{prop:coexistence} and~\ref{prop:research}, the three corollaries and the results of
Sections~\ref{sec:robustness} to~\ref{sec:empirical} in full, and proves every result.
```

---

## 2. The model

### T-2.1. Paths

- **Location**: Section 2.2, `02:54–55`, in place of "In the main case \(R\) is uniform on \([0,r]\), and an increase in \(r\) strengthens the incumbent." The sentence before it stays.
- **Matches**: S5 item 1 (the path declaration of A2); `NOTATION.md` (c) "Paths".
- **Scope**: definition.

```latex
A path is a family \(\{F_r\}\) of continuous incumbent distributions indexed by a strength \(r\) in an interval, in
which \(F_{r'}\) is a first-order stochastic strengthening of \(F_r\) whenever \(r'>r\), with everything else fixed.
```

### T-2.2. Normalization of money

- **Location**: Section 2.2, `02:78–88`. Lines 78–83 (the example's classes and \eqref{eq:order}) and the last sentence of line 87–88 go to Section 4.2 (target 4.2); the general sentence of lines 85–87 stays as below.
- **Matches**: not a result; rule 4 (the example enters at Section 4.2).
- **Scope**: holds for every primitive.

```latex
The general statements need no normalization of money: a common positive rescale of every value, the reserve, and
every preparation, trading and research cost rescales prices and payoffs by the same factor, while orders, beliefs,
entry, and ownership do not change.
```

### T-2.3. The liquidity footnote

- **Location**: Section 2.3, the footnote at `02:123–125`, in place of its text.
- **Matches**: proof O2: Propositions 1 to 4 hold for every \(0<\beta<1/2\); the bound \(\beta\le1/3\) enters the posterior bound common to all orders, the exclusion bound, and the research parameter region and the slot-feasibility statements of identification, which range over the model's slots.
- **Scope**: liquidity probability; the rest as in each proposition.

```latex
\footnote{The posterior bound common to all orders, and through it the exclusion bound of
Section~\ref{sec:inference}, use \(\beta\le1/3\). The research parameter region and the slot-feasibility statements
in identification range over the slots of the model. The other results hold for every \(0<\beta<1/2\)
(Appendix~\ref{app:beliefs}).}
```

### T-2.4. Notation along a path

- **Location**: Section 2.4, `02:202–204`, in place of "When the incumbent's distribution matters, ... \(B_r\)."
- **Matches**: `NOTATION.md` (c) "Paths".
- **Scope**: notation.

```latex
When the incumbent's distribution matters, I write \(g_j(F)\), \(\DT(F)\), and \(B_F\); along a path, I write
\(g_j(r)\), \(\DT(r)\), and \(B_r\) for the objects at \(F_r\).
```

### T-2.5. The default tie rules

- **Location**: Section 2.4, `02:216–218`, in place of the paragraph.
- **Matches**: `NOTATION.md` (b) "Tie rules"; Table A.2 (`tab:a4-ties`).
- **Scope**: definition of the phrase "the default tie rules".

```latex
When ties arise, an indifferent investor may mix over its best orders, and an indifferent high-cost challenger
prepares. I call these the default tie rules. Where another tie rule changes a conclusion, the appendix states the
change beside the result, and Table~\ref{tab:a4-ties} in Appendix~\ref{app:coexistence} collects the changes for
coexistence in the example at the prior \(1/2\).
```

### T-2.6. Winning, outbidding and the takeover share

- **Location**: Section 2.4, `02:226–228`, in place of the sentence that defines \(W_H(F)\); the sentence on entry and ownership (`02:225–226`) stays before it.
- **Matches**: S5 item 2 (the share part of Proposition 2); W2 "Shared Candidate 3".
- **Scope**: definitions.

```latex
The probability that a prepared challenger of class \(j\) wins against the incumbent distribution \(F\) is
\(W_j(F)=\E_j\bigl[F(\theta)\1\{\theta\ge p\}\bigr]\), and class \(H\) outbids the incumbent \(F\) when
\(W_H(F)=1\), so that a prepared class-\(H\) challenger beats it for sure. Entry in class \(j\), \(e_j\), is the
probability that the challenger prepares given class \(j\), and class \(H\)'s takeover share is the probability that
the challenger is of class \(H\), given that the challenger acquires the target.
```

---

## 3. Competition and information

### T-3.1. Lead-in to Proposition 1

- **Location**: Section 3.1, `03:19–39`, in place of the closed forms and the sentence after them (these go to Section 4.2, target 4.5). Proposition 1 follows unchanged.
- **Matches**: Proposition 1 (unchanged); the slice argument of `03:60–70`.
- **Scope**: (a) every pair of classes; (b) under the class ranking; weak in both parts, as Proposition 1 states.

```latex
A stronger incumbent outbids a prepared challenger more often, and when it does, it pays the challenger's bid.
Proposition~\ref{prop:returns} shows that this weakly lowers acquisition profit at every fixed belief and weakly
raises the sensitivity of target proceeds to challenger quality, for every continuous incumbent distribution; the
second effect uses the class ranking~\eqref{eq:classes}.
```

### T-3.2. The class-gap identity

- **Location**: Section 3.1, `03:76–78`, in place of "The identity holds ... to target proceeds." The example's clause "in the benchmark the right side is \(h-\ell\) at every \(r\)" goes to target 4.5.
- **Matches**: Proposition 1, the sum of the two lines of \eqref{eq:spread}.
- **Scope**: every incumbent distribution, under the class ranking.

```latex
The identity holds for every incumbent distribution, and its right side does not depend on the incumbent. A stronger
incumbent leaves the value gap between the classes unchanged; it moves the gap from the challenger's profit to target
proceeds.
```

### T-3.3. The end of Section 3.1

- **Location**: Section 3.1, `03:80–82`, in place of the paragraph. The limit as \(r\) approaches \(\ell\) goes to target 4.5.
- **Matches**: Proposition 1.
- **Scope**: weak, as Proposition 1.

```latex
A stronger incumbent therefore never narrows the spread and never raises gross acquisition profit at any belief.
Whether entry rises depends on how this change in payoffs affects the information in the price.
```

### T-3.4. The threshold along a path

- **Location**: Section 3.2, `03:99–100`, in place of "For the uniform incumbent I write \(\tau(r)\)."
- **Matches**: `NOTATION.md` (c) "Paths".
- **Scope**: notation.

```latex
Along a path I write \(\tau(r)\).
```

### T-3.5. The split by class

- **Location**: Section 3.3, `03:140–141`, in place of "Appendix~\ref{app:beliefs} gives ... along the benchmark path."
- **Matches**: Lemma on the trading bound (A2); the coexistence results of A4.
- **Scope**: every tuple.

```latex
Appendix~\ref{app:beliefs} gives the formal statement and proof of the trading bound, and the coexistence results of
Section~\ref{sec:coexistence} rest on this split.
```

### T-3.6. What the market sees of the auction

- **Location**: Section 3, added after `03:141` as Section 3.4.
- **Matches**: S5 item 1 (the reduction lemma: trading, posteriors and entry depend on the auction only through the spread and the threshold, and a stronger incumbent raises both). `SCAN.md` Part 2; W1 "Solver B 1" (the threshold can fall where it is negative).
- **Scope**:
  - prior: any (the reduction lemma holds at every prior, with research included);
  - other primitives: the research cost and the cap are held fixed with the rest, in the words "every other primitive";
  - tie rules: the same tie rules in both auctions;
  - trading pattern: every equilibrium;
  - condition: \(\DT>0\) and \(g_H>g_L\); the threshold statement holds while \(g_L\le c_H\), which persists along a path once it holds;
  - weak or strict: weak ("never narrows", "never lowers", "never raises", "never widens").

```latex
\subsection{What the market sees of the auction}\label{sec:twonumbers}

When the spread is positive and class \(H\)'s gross profit exceeds class \(L\)'s, the investor's orders, the market
makers' posteriors and the challenger's preparation depend on the auction only through the target-payoff spread
\(\DT\) and the preparation threshold \(\tau\). The spread sets what an informed order earns at each posterior and
level of entry, and the threshold sets which posteriors recruit a high-cost challenger. Two auctions with the same
spread and the same threshold, and with every other primitive and the tie rules the same, therefore have the same
equilibrium orders, posteriors and entry, and, when the investor chooses research, the same research. Prices add the
levels \(t_0\) and \(t_L\), and ownership adds which bidder wins, so results on ownership carry class \(H\)'s chance
of beating the incumbent.

A stronger incumbent never narrows the spread (Proposition~\ref{prop:returns}). It never lowers the threshold while a
challenger known to be in class \(L\) would not prepare at the high cost, \(g_L\le c_H\): it never raises class
\(L\)'s profit and never widens the profit gap between the classes, so a challenger needs at least as favorable a
belief before preparation at the high cost pays. Along a path, once \(g_L\le c_H\) holds, it holds against every
stronger incumbent. Coexistence in Section~\ref{sec:coexistence} and research in Section~\ref{sec:research} are
statements about these two numbers, and Appendix~\ref{app:beliefs} gives the formal statement and its proof.
```

---

## 4. Equilibrium results

### T-4.1. Proposition 2, part (ii): the takeover share

- **Location**: Section 4.1, added after `04:39` (the display of the ownership condition in part (ii)). The rest of Proposition 2 stays.
- **Matches**: S5 item 2 (Proposition 2 gains class \(H\)'s share of takeovers under outbidding). W2 "Shared Candidate 3" (odds \((e_H/e_L)(W_H/W_L)\)); W2 "Do the same workarounds cover Proposition 2" (outbidding at \(F_1\) forces it at \(F_0\)); proof O6.
- **Scope**: prior: any; tie rules: none needed; trading pattern: the full two-sided trade of part (ii); condition: \(W_H(F_1)=1\); weak or strict: ownership rises strictly; the share rises strictly exactly when \(W_L(F_0)>0\) and equals one at both incumbents otherwise.

```latex
If class \(H\) outbids \(F_1\), it outbids \(F_0\) as well, high-class ownership rises, and class \(H\)'s takeover
share rises strictly when \(W_L(F_0)>0\); when \(W_L(F_0)=0\), the share equals one against both incumbents.
```

### T-4.2. Open set, end of the hypotheses paragraph

- **Location**: Section 4.1, `04:57–61`, in place of "For uniform incumbents, (H1)--(H3) are strict inequalities ... slice through the benchmark." The uniform sentence goes to Section 4.2 (target 4.4).
- **Matches**: Proposition A.5 (the open set); Corollary 1.
- **Scope**: not a result in itself.

```latex
Section~\ref{sec:benchmark} shows that (H1)--(H3) hold together on an open set of primitives.
```

### T-4.3. After Proposition 2: ownership and the decisive advantage

- **Location**: Section 4.1, `04:63–67`, in place of the paragraph.
- **Matches**: S5 item 2 (Proposition 2(ii); the decisive-advantage lemma). W2 "Shared Candidate 2", subsection "Decisive advantage" (DA gives \(W_H=1\) at every recruiting economy with \(\gamma>0\); in Proposition 2, DA gives \(W_{H,1}=1\) and FOSD forces \(W_{H,0}=1\)); W2 "Shared Candidate 3".
- **Scope**:
  - prior: any;
  - tie rules: none needed;
  - trading pattern: that of Proposition 2(ii);
  - condition: the decisive advantage on a family of incumbent distributions; \(g_H>g_L\) for the recruitment sentence; (H1);
  - weak or strict: the sufficient condition for part (ii) is stated with its strict and weak parts.

```latex
The additional entry favors the high class, which places a purchase with probability \(b+\lambda\), while the low
class places one with probability \(b\). High-class ownership multiplies entry in class \(H\) by class \(H\)'s chance
of beating the incumbent, and a stronger incumbent can lower that chance when class \(H\) can lose. The condition in
part~(ii) holds whenever the stronger incumbent leaves the high class a good chance to win,
\((1+\rho)W_H(F_1)\ge2\rho W_H(F_0)>0\), and the high class places a purchase more often than not,
\(b+\lambda>1/2\). When class \(H\) outbids \(F_1\), its chance to win is one against both incumbents, so ownership
rises with entry in class \(H\); the stronger incumbent then takes wins only from the low class, and when a low-class
challenger can beat the weak incumbent, the takeovers that go to the challenger shift toward class \(H\).

Values and costs alone give outbidding when class \(H\) has a decisive advantage on a family of incumbent
distributions: against every distribution in the family at which class \(H\)'s gross profit exceeds \(c_H\), class
\(H\) outbids the incumbent. When \(g_H>g_L\), a price recruits a high-cost challenger only where class \(H\)'s gross
profit exceeds \(c_H\), because gross profit at every posterior below one falls short of \(g_H\). Under a decisive
advantage, (H1) therefore gives \(W_H(F_1)=1\), and the share statement of part~(ii) applies.
```

### T-4.3b. The end of Section 4.1

- **Location**: Section 4.1, `04:71`, in place of "and Section~\ref{sec:coexistence} describes the strengths between the three economies."
- **Matches**: Proposition 3.
- **Scope**: pointer.

```latex
and Section~\ref{sec:coexistence} describes where quiet and informative markets coexist between the three economies.
```

### T-4.4. Section 4.2: title and the example

- **Location**: Section 4.2, `04:75–87`, in place of the title and the two declaration paragraphs. The text absorbs `02:78–83`, `02:87–88` (units), `02:203–204` (the uniform notation, which the path notation of target 2.4 covers) and the uniform sentence of `04:57–61`. Corollary 1 follows directly.
- **Matches**: Corollary 1 (S5 item 2); Table A.9 declarations; Proposition A.5 (open set).
- **Scope**: declarations; the open-set sentence is strict.

```latex
\subsection{The example and the fixed-information control}\label{sec:benchmark}

In the example, the two classes are point masses: \(G_H\) puts all its mass on \(h=\reg{prim_h}\) and \(G_L\) on
\(\ell=\reg{prim_ell}\), so the class and the value coincide. The incumbent is uniform on \([0,r]\), so an increase in
\(r\) strengthens it and the strengths form a path. The prior is \(\pi=\reg{prim_pi}\), the reserve
\(p=\reg{prim_p}\), the zero-cost probability \(\rho=\reg{prim_rho}\), the high cost \(c_H=\reg{prim_cH}\) and the
trading cost \(k=\reg{prim_k}\), and money is measured in units of the low value. The weak, the strong and the very
strong incumbent have the strengths \(r_0=\reg{prim_r0}\), \(r_1=\reg{prim_r1}\) and \(r_2=\reg{prim_r2}\). Values,
the reserve and every strength of the path satisfy
\begin{equation}\label{eq:order}
0<p<\ell<r<h.
\end{equation}

In the example's slot the largest likelihood ratio of an order is \(1+u=\eu\), and the liquidity probability is
\(\beta=\reg{beta_B}\). The presence probability is therefore \(\lambda=u\beta/(1+u\beta)=\reg{lambda_B}\), with
\(b=\reg{b_B}\), and the posterior bounds at the prior are \(M(1/2)=\eu/(1+\eu)=\reg{M_half_B}\) and
\(m(1/2)=\reg{m_half_B}\); Appendix~\ref{app:parameters} lists these values and the arithmetic behind each. With the
example's classes and reserve, (H1)--(H3) are strict inequalities between continuous functions of
\((r_0,r_1,r_2,c_H,k,\rho,\pi,\lambda,\beta)\), so they hold on an open set of these parameters that contains the
example.
```

### T-4.4a. Corollary 1

- **Location**: Section 4.2, added after target 4.4.
- **Matches**: S5 item 2 (the full Corollary 1, from Proposition A.1(a) and (c)); Proposition 2(ii) entry and ownership formulas. W2 "Benchmark verification".
- **Scope**:
  - prior: \(1/2\) for the band in \(u\); the prior band at \(1+u=\eu\);
  - tie rules: none needed in the open band (Proposition A.1(b) treats the boundaries);
  - trading pattern: that of Proposition 2;
  - condition: the example's auction and costs, strengths \(r_0,r_1,r_2\), \(0<\beta\le1/3\);
  - weak or strict: strict band; entry and ownership rise strictly.

```latex
\begin{corollary}[Recruitment and ownership in the example]\label{prop:region}\label{cor:ccc-example}
In the example at the prior \(1/2\), (H1)--(H3) hold if and only if \(\reg{u_lo_frac}<u<\reg{u_hi_frac}\), that is,
if and only if the top posterior lies between the preparation thresholds of the strong and the very strong
incumbent, \(\tau(r_1)=\reg{M_lo_frac}<M(1/2)<\reg{M_hi_frac}=\tau(r_2)\). In the example's slot, with \(1+u=\eu\),
they hold if and only if the prior lies between \(\approx\reg{prior_lo_B}\) and \(\approx\reg{prior_hi_B}\). On
this set class \(H\) outbids every incumbent on the path, entry rises from \(\rho\) to \(\rho+(1-\rho)(b+\pi\lambda)\),
and high-class ownership rises from \(\pi\rho\) to \(\pi[\rho+(1-\rho)(b+\lambda)]\).
\end{corollary}
```

### T-4.4b. Reading of Corollary 1: entry, ownership and the decisive advantage

- **Location**: Section 4.2, `04:113–119`, in place of the paragraph; it follows Corollary 1 and Table 1.
- **Matches**: Corollary 1; S5 item 2 (the share part and the decisive-advantage lemma, the cost window \(399/80\le c_H\le32/5\)). W2 "Decisive advantage" (equivalence on the full uniform family); W2 "Benchmark verification".
- **Scope**: prior: the example's; tie rules: none needed; trading pattern: that of Proposition 2; condition: point-mass classes and a uniform incumbent of any strength for the equivalence; weak or strict: the equivalence is "\(\ge\)"; the example's cost exceeds the bound strictly.

```latex
Table~\ref{tab:payoffs} reports the acquisition payoffs, and the two forces move in opposite directions from \(r_0\)
to \(r_1\): gross acquisition profit at the prior falls from \(\reg{Bprior_r0}\) to \(\reg{Bprior_r1_B}\), while the
target-payoff spread rises from \(\reg{Delta_r0}\) to \(\reg{Delta_r1}\). In the example's slot, entry rises from
\(\reg{entry_r0}\) at \(r_0\) to \(\reg{entry_r1_B}\) at \(r_1\), and high-class ownership from \(\reg{own_r0}\) to
\(\reg{own_r1_B}\). Class \(H\) outbids every incumbent on the path, because \(h\) exceeds \(r_2\), and the strong
incumbent takes wins only from the low class, so class \(H\)'s takeover share rises from \(\reg{share_H_r0}\) to
\(\reg{share_H_r1_B}\). At \(r_2\) entry returns to \(\reg{entry_r2}\) and the three prices still differ;
Table~\ref{tab:outcomes} lists the three equilibrium tuples. With point-mass classes and a uniform incumbent of any
strength, class \(H\) has a decisive advantage exactly when \(c_H\ge(h^2-p^2)/(2h)\), and the example's high cost
exceeds \((h^2-p^2)/(2h)=\reg{cH_DA_floor_B}\): against every uniform incumbent at which a price recruits a
high-cost challenger, class \(H\) outbids the incumbent.
```

### T-4.5. The two numbers in closed form

- **Location**: Section 4.2, added after target 4.4b; it carries `03:19–35` (the closed forms, with the labels `eq:payoffs` and `eq:derivatives`), the example's clause of `03:76` and the limit of `03:80–81`.
- **Matches**: Proposition 1 in the example; the class-gap identity; the closed form of \(\tau(r)\) (`O1_referee.md` 2.1 confirms \(\tau(r)=(12r-3/4)/(20r-r^2-1)\) at the example's values).
- **Scope**: the example's classes and reserve, \(p<r\); the derivative signs hold for \(r>\ell\).

```latex
Integration over \(R\) gives
\begin{equation}\label{eq:payoffs}
\begin{aligned}
t_0&=p\Bigl(1-\frac pr\Bigr),&
t_H&=\frac r2+\frac{p^2}{2r},\\
t_L&=\ell-\frac{\ell^2-p^2}{2r},&
g_H&=h-\frac r2-\frac{p^2}{2r},\\
g_L&=\frac{\ell^2-p^2}{2r},&
\DT(r)&=\frac{(r-\ell)^2}{2r},
\end{aligned}
\end{equation}
with the derivatives
\begin{equation}\label{eq:derivatives}
\DT'(r)=\frac12-\frac{\ell^2}{2r^2}>0,\qquad
g_H'(r)=-\frac12+\frac{p^2}{2r^2}<0,\qquad
g_L'(r)=-\frac{\ell^2-p^2}{2r^2}<0,
\end{equation}
and the preparation threshold
\[
\tau(r)=\frac{2rc_H-(\ell^2-p^2)}{2rh-r^2-\ell^2}.
\]
The right side of the class-gap identity of Section~\ref{sec:profits} is \(h-\ell\) at every \(r\). The spread
approaches zero as \(r\) approaches \(\ell\), since the incumbent then almost never outbids a class-\(L\)
challenger, and Table~\ref{tab:payoffs} reports both numbers at the three strengths.
```

### T-4.6. The band

- **Location**: Section 4.2, `04:121–127`, in place of the paragraph.
- **Matches**: Corollary 1 and its full statement (Proposition A.1(b)).
- **Scope**: as Corollary 1.

```latex
Appendix~\ref{app:prop2} states Corollary~\ref{prop:region} in full. Below the band a purchase at \(r_1\) does not
recruit a high-cost challenger, and above it a conclusion of Proposition~\ref{prop:ccc} fails at \(r_2\) or at
\(r_1\). Table~\ref{tab:region} gives the recruitment region in decimals, with the example's slot and its distance
to each boundary.
```

### T-4.6a. Table 2 caption

- **Location**: Section 4.2, `04:131`, in place of the caption text.
- **Matches**: Corollary 1.
- **Scope**: caption.

```latex
\caption{The recruitment region in the example.}\label{tab:region}
```

### T-4.7. The width of the band and the entry ceiling

- **Location**: Section 4.2, `04:155–165`, in place of the two paragraphs.
- **Matches**: Corollary 1; the exclusion bound (`cor:exclusion`); Proposition 2.
- **Scope**: the example; strict where stated.

```latex
Both ends of the band are preparation thresholds: the lower end \(\tau(r_1)\) is the belief that a purchase needs to
recruit a high-cost challenger against the strong incumbent, and the upper end \(\tau(r_2)\) is the belief at which a
purchase would still recruit one against the very strong incumbent. The threshold rises slowly with strength, and
this sets the width of the band: class \(H\) outbids every incumbent on the path, and its expected payment
\(r/2+p^2/(2r)\) rises by less than one half per unit of strength, a change that is small next to the gap
\(g_H-g_L\) in Table~\ref{tab:payoffs}.

Gross profit at every belief falls strictly with strength above \(\ell\), so the exclusion condition (H3) holds at
every strength in \((r_C,h)\), where the entry ceiling \(r_C=\reg{rC_B}\) is the strength at which
\(\tau(r)=M(1/2)\); parts~(i) and~(ii) of Proposition~\ref{prop:ccc} hold without the exclusion condition.
Table~\ref{tab:margins} in Appendix~\ref{app:parameters} records every hypothesis and its positive margin in the
example.
```

### T-4.8. Section 4.3: lead-in to Proposition 3

- **Location**: Section 4.3, `04:256–270`, in place of the two paragraphs.
- **Matches**: S5 item 3 (the region theorem).
- **Scope**: as Proposition 3(a); no strength symbol, since the marked strengths belong to Corollary 2.

```latex
Between the weak and the strong incumbent of Proposition~\ref{prop:ccc}, two equilibria can hold against the same
incumbent. In a quiet market the investor does not trade, the price carries no information, and entry stays at its
floor; in the informative market that coexists with it, a purchase recruits a high-cost challenger. The two numbers
of Section~\ref{sec:twonumbers} decide where both exist: the threshold must lie above the prior and within reach of
a purchase, and the spread must be wide enough that a purchase that just reaches the threshold covers the trading
cost, yet narrow enough that no order against an uninformative price earns more than it.
```

### T-4.9. Proposition 3

- **Location**: Section 4.3, `04:272–283`, in place of the proposition.
- **Matches**: S5 item 3. (a) W1 "Shared Candidate 1" (the region, uniqueness under the default challenger rule, the entry formula); (b) W1 "Solver B 1" (the full-purchase interval; gaps lie at spreads below the sure-purchase cutoff); (c) W1 "Solver B 2" (the balance condition) and W1 "Solver A 2 and Solver C 3" (uniform incumbents and preparation affordability), with proof O9 for the uniform instance.
- **Scope**:
  - prior: any \(0<\pi<1\);
  - tie rules: "an indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares", named in the statement;
  - trading pattern: the informative market's purchase, mixed or sure; class \(L\) abstains;
  - condition: \(\DT>0\), \(g_H>g_L\); the region; the balance condition of (c), which is the frozen main-text form (the product of the spread and \(g_H-c_H\) does not fall), and the uniform instance;
  - weak or strict: the region has weak inequalities except \(\pi<\tau\); entry rises strictly while class \(H\) mixes; "does not fall" is weak.
- Part (c) is the frozen main-text form of Proposition 3(c) and omits the start hypothesis \(g_H>c_H\) against the weakest incumbent, which the interval claim does not use. The introduction (T-1.4) and the intuition (T-4.10) keep the proportional words, "the spread grows, in proportion, at least as fast as that excess shrinks", together with the start hypothesis, because the proportional reading needs a positive excess.

```latex
\begin{proposition}[Quiet and informative markets]\label{prop:coexistence}
Let the classes satisfy the class ranking~\eqref{eq:classes}, let \(0<\pi<1\), \(0<\rho<1\), \(k>0\) and a slot
\((\lambda,\beta)\) be given, and let an indifferent investor mix over its best orders and an indifferent high-cost
challenger prepare. Take an incumbent distribution with a positive spread \(\DT\) and \(g_H>g_L\), and write \(\tau\)
for its preparation threshold.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
\item A quiet market and an informative market coexist if and only if
\[
\pi<\tau\le M(\pi),\qquad \frac{k}{1-\tau}\le\DT\le\frac{k}{\rho\max\{\pi,1-\pi\}}.
\]
The informative market is then unique: class \(L\) abstains, only a purchase recruits a high-cost challenger, and
entry is
\[
\rho+(1-\rho)\min\Bigl\{\frac{(1-\pi)\,b\,\DT}{k},\;b+\pi\lambda\Bigr\},
\]
which rises strictly with the spread while class \(H\) mixes between a purchase and abstention and is constant once
class \(H\) buys for sure.
\item Along a path of such distributions, the strengths at which a quiet market coexists with an informative market
in which class \(H\) buys for sure form an interval, and every other strength with coexistence lies below it.
\item Along a path on which the product of the spread and \(g_H-c_H\) does not fall with strength, the strengths
with coexistence form an interval, at every prior. Uniform incumbents on \([0,r]\), with \(r\) in a closed interval,
satisfy this condition when every low-class value lies between the reserve and the lowest strength, every high-class
value is at least the highest strength, and class \(H\)'s mean value exceeds the highest strength by at least
\(c_H\).
\end{enumerate}
\end{proposition}
```

### T-4.10. Intuition for Proposition 3

- **Location**: Section 4.3, `04:311–324`, in place of the three paragraphs (the reading of the example moves to targets 4.12 and 4.13).
- **Matches**: Proposition 3(a) to (c); W1 "Shared Candidate 1" after eq. 2 (the entry ranking across gaps); W1 "Solver B 1".
- **Scope**: as Proposition 3; the threshold rises only where it is positive, which holds on the region.

```latex
Coexistence comes from the entry response itself. In a quiet market entry stays at its floor after every order, so an
informed order earns at most \(\rho\max\{\pi,1-\pi\}\) times the spread, and the upper bound on the spread keeps that
from exceeding the trading cost. An informative market changes the entry response to a purchase, and with it the
return to trade: a purchase that reaches the threshold recruits, and the lower bound on the spread lets it cover the
trading cost.

Entry rises with the spread while class \(H\) mixes, because the purchase rate adjusts. While class \(H\) mixes, a
recruiting purchase earns exactly the trading cost, so a wider spread needs a more informative purchase; the purchase
rate rises, and entry rises with it until class \(H\) buys for sure. Entry depends on the incumbent only through the
spread, so between two incumbents at which the markets coexist, entry in the informative market is at least as high
against the one with the wider spread.

A stronger incumbent never narrows the spread, and where the threshold is positive it never lowers the threshold, so
the two numbers pull in opposite directions: a wider spread raises what a recruiting purchase earns, and a higher
threshold makes recruitment harder. As the incumbent strengthens, the economy can enter the region, leave it, and
enter it again. The strengths with a sure purchase are never split, because each condition that defines them holds on
one side of a single strength, and a mixed purchase needs a narrower spread than a sure one, so the other strengths
with coexistence lie below them. When class \(H\)'s gross profit exceeds the high cost against the weakest incumbent,
the whole set stays in one piece if the spread grows, in proportion, at least as fast as that excess shrinks; part~(c)
states the condition as a product, which does not fall.
```

### T-4.11. Corollary 2

- **Location**: Section 4.3, added after target 4.10.
- **Matches**: S5 item 3 (the full Corollary 2: coexistence on \([r_A,r_N]\) and the shape of entry); the current Proposition 3 and its appendix statement.
- **Scope**:
  - prior: \(1/2\);
  - tie rules: the default tie rules, named in the statement;
  - trading pattern: the informative market that coexists with a quiet market; full purchases above \(r_F\);
  - condition: a slot in the band of Corollary 1;
  - weak or strict: entry rises strictly on \([r_A,r_F]\) and is constant on \([r_F,r_N]\).

```latex
\begin{corollary}[Coexistence in the example]\label{cor:example-coexistence}
In the example at the prior \(1/2\), let the slot lie in the band of Corollary~\ref{prop:region}, and let an
indifferent investor mix over its best orders and an indifferent high-cost challenger prepare. The strengths at
which a quiet market and an informative market coexist form the interval \([r_A,r_N]\). In the informative market
that coexists with a quiet market, entry is \(\rho+(1-\rho)\min\{b\DT(r)/(2k),\,b+\lambda/2\}\); it rises strictly
on \([r_A,r_F]\) and is constant on \([r_F,r_N]\). With a full purchase, entry keeps this value up to the entry
ceiling \(r_C\) and equals \(\rho\) above it.
\end{corollary}
```

### T-4.12. Reading of Corollary 2

- **Location**: Section 4.3, `04:285–290`, in place of the paragraph, together with `04:323–324`; it follows Corollary 2.
- **Matches**: Proposition 3(c) in the example (the uniform instance: \(\ell\in[p,r_0]\), \(h\ge r_2\), \(h-r_2\ge c_H\)); Corollary 2; the marked strengths of A4. W1 "Consolidated benchmark numerical check".
- **Scope**:
  - prior: \(1/2\) and the example's slot for the numbers; every prior for the interval statement;
  - tie rules: the default tie rules (Corollary 2);
  - trading pattern: as named for each stretch (mixed or full purchase; mixed orders at the entry floor; the low class abstains, mixes, sells for sure);
  - condition: the uniform instance of Proposition 3(c);
  - weak or strict: as in Corollary 2.

```latex
The example satisfies the condition of Proposition~\ref{prop:coexistence}(c): its incumbent is uniform, \(\ell\) lies
between \(p\) and \(r_0\), and \(h\) exceeds \(r_2\) by more than \(c_H\), so at every prior the strengths with
coexistence form one interval. In the example's slot, coexistence starts at \(r_A\approx\reg{rA}\), where a purchase
that just reaches the threshold and recruits earns the trading cost; class \(H\) buys for sure from
\(r_F\approx\reg{rF_B}\), where a full purchase that recruits earns the trading cost; and the quiet market ends at
\(r_N\approx\reg{rN}\), where a unit order against an uninformative price earns the trading cost. Entry in the
informative market is \(\reg{entry_rA_B}\) at \(r_A\), \(\reg{entry_mb_r140_B}\) at \(\reg{str_r140}\) and
\(\reg{entry_mb_r145_B}\) at \(\reg{str_r145}\), and from \(r_F\) it stays at \(\reg{entry_r1_B}\) up to the entry
ceiling \(r_C\approx\reg{rC_B}\). Above \(r_N\) the informative market with a full purchase remains, and on
\((r_N,r_J)\), with \(r_J\approx\reg{rJ}\), mixed orders at the entry floor join it. The low class abstains up to
\(r_N\), mixes on \((r_N,r_S)\) and sells for sure from \(r_S\approx\reg{rS_B}\), the strength at which a full sale
earns the trading cost. Figure~\ref{fig:coexistence} draws the path through the region and the entry it produces,
and Appendix~\ref{app:coexistence} lists every equilibrium along the path.
```

### T-4.13. The high cost of the example

- **Location**: Section 4.3, added after target 4.12.
- **Matches**: S5 item 2 (the cost window \(399/80\le c_H\le32/5\)); the uniform instance of Proposition 3(c); the decisive advantage of Section 4.1.
- **Scope**: the example; weak bounds, met strictly.

```latex
The example's high cost lies between the two bounds that these conditions place on it. It is at most
\(h-r_2=\reg{cH_afford_ceiling_B}\), so class \(H\)'s value covers the high cost against the strongest incumbent
and Proposition~\ref{prop:coexistence}(c) applies, and it is at least \((h^2-p^2)/(2h)=\reg{cH_DA_floor_B}\), so
class \(H\) has the decisive advantage of Section~\ref{sec:ccc}.
```

### T-4.14. Coexistence at other priors

- **Location**: Section 4.3, `04:326–332`, in place of the paragraph.
- **Matches**: Corollary A.2 (`prop:priors`), unchanged.
- **Scope**: the example's slot; the default tie rules (Corollary A.2).

```latex
Coexistence also holds away from the even prior. In the example's slot it starts at the same strength \(r_A\) for
every prior between \(\approx\reg{piA_lo_B}\) and \(\approx\reg{piA_hi}\), and it starts later, where the prior
reaches the threshold, for priors up to \(\approx\reg{pimax}\). Below \(\approx\reg{piA_lo_B}\) even the top
posterior cannot reach the threshold once a purchase can pay for itself, and from \(\approx\reg{pimax}\) on, the
quiet market ends before the prior falls below the threshold. Appendix~\ref{app:coexistence} gives the coexistence
set at every prior (Corollary~\ref{prop:priors}).
```

---

## 5. Competition creates research

### T-5.1. Opening

- **Location**: Section 5, `05:3`, in place of the clause "So far the investor is present with a fixed probability \(\lambda\); now the investor chooses that probability and pays for it." The rest of `05:3–27` stays.
- **Matches**: not a result; rule 3.
- **Scope**: none.

```latex
With research, the investor chooses the presence probability \(\lambda\) of Section~\ref{sec:slot} and pays for it.
```

### T-5.2. Lead-in to Proposition 4

- **Location**: Section 5, `05:29–51`, in place of the three paragraphs; `\label{eq:research}` stays on the display, which gains the positive part.
- **Matches**: S5 item 4 (the weak type's selling adds the sale's profit to the research equation); W3 "Shared Candidate 1" sections 2, 3 and 5; W3 section 6 (the exact margin \(\phi_a^*=J-k+(\rho J-k)^+-2a\lambda_E\)); proof O4.
- **Scope**:
  - prior: \(1/2\) (stated for the section at `05:22`);
  - tie rules: "an indifferent investor may mix over its best orders" for the low class's mixing;
  - trading pattern: class \(H\) buys after a success and a purchase recruits; class \(L\) abstains, mixes or sells for sure;
  - condition: \(1/2<\tau<1\) for the recruitment intensity; \(\DT>2k\) for the root;
  - weak or strict: the root is unique in \((0,1)\).

```latex
Research raises the top posterior that a purchase can reach. At intensity \(\lambda\), I write \(M_\lambda\) for that
top posterior and \(m_\lambda=1-M_\lambda\) for the bottom posterior, the posterior bounds of
Section~\ref{sec:inference} at the prior \(1/2\) when the presence probability is \(\lambda\). When \(1/2<\tau<1\),
the \emph{recruitment intensity} \(\lambda_E(\tau)\) is the research level at which a full purchase just reaches the
threshold, \(M_\lambda=\tau\), so a full purchase recruits exactly when research is at least \(\lambda_E(\tau)\).

Consider the equilibrium in which class \(H\) buys after a success and a purchase recruits a high-cost challenger.
When an indifferent investor may mix over its best orders, class \(L\) abstains while a sale at the entry floor
cannot pay its cost, \(\rho\DT\le2k\); beyond that point it sells just often enough that its sale breaks even, and
once even a sure sale pays, it sells for sure. A sale never recruits, and a sale that breaks even adds nothing to the
value of research, so research optimality at an interior intensity reads
\begin{equation}\label{eq:research}
2a\lambda=\DT\,m_\lambda-k+\bigl(\rho\DT\,m_\lambda-k\bigr)^+ .
\end{equation}
The left side rises with \(\lambda\), and the right side falls, because more research removes camouflage. When
\(\DT>2k\), the two sides meet at one intensity \(\lambda_R(\DT)\in(0,1)\), and research is the smaller of
\(\lambda_R(\DT)\) and the cap \(\lb\). The \emph{exact recruitment margin} is the right side of \eqref{eq:research}
minus its left side at the recruitment intensity; it is positive exactly when, at the research level that just lets a
purchase recruit, the value of a success exceeds the marginal cost of research.
```

### T-5.3. Proposition 4

- **Location**: Section 5, `05:52–71`, in place of the proposition. The example part (the present part (b)) becomes Corollary 3 (target 5.5).
- **Matches**: S5 item 4; `lens_theory.md` 3.7, T3 (parts (a) to (d)). (a) W3 "Shared Candidate 1" sections 1 to 4 (existence condition); (b) W3 section 5 and W2 "Shared Candidate 1" (entry by class); (c) W2 "Ranking and recommendation" item 2 and W2 "Decisive advantage"; (d) W3 section 6 (one upward crossing, no later downward exit, attainment of the cap, then the last point of \(\{\tau\le M_{\lb}\}\)); proofs O3 and O4.
- **Scope**:
  - prior: \(1/2\);
  - tie rules: "an indifferent investor may mix over its best orders and an indifferent high-cost challenger prepares", named in the statement, with the sentence of C's main-text form that the recruiting outcome is also available when an indifferent high-cost challenger may prepare with any probability and prepares fully at the purchase;
  - trading pattern: class \(H\) buys after a success and a purchase recruits; class \(L\) as in the lead-in;
  - condition: \(\DT>0\), \(g_H>g_L\), \(1/2<\tau<1\); (a) \(\DT>2k\); (c) outbidding; (d) a compact path with continuous spread and threshold, the spread against the weakest incumbent below the cap spread and reached by the path, and, up to the strength at which research reaches its cap, an exact recruitment margin that rises strictly, is negative against the weakest incumbent and is positive where research reaches the cap;
  - weak or strict: research rises strictly below the cap; entry and class entries move strictly with research; ownership "does not fall", strictly below the cap where the spread rises strictly.

```latex
\begin{proposition}[Competition creates research]\label{prop:research}
Let the classes satisfy the class ranking~\eqref{eq:classes} and the prior be \(1/2\), and let an indifferent
investor mix over its best orders and an indifferent high-cost challenger prepare. Take incumbent distributions with
a positive spread, \(g_H>g_L\) and \(1/2<\tau<1\), and consider the equilibrium in which class \(H\) buys after a
success and a purchase recruits a high-cost challenger. The same recruiting outcome is available when an indifferent
high-cost challenger may prepare with any probability and prepares fully at the purchase.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
\item The equilibrium exists if and only if \(\DT>2k\) and \(\tau\le M_\lambda\) at
\(\lambda=\min\{\lambda_R(\DT),\lb\}\), which is then the investor's research.
\item Research rises strictly with the spread until it reaches the cap and then stays at the cap. Entry,
\(\rho+(1-\rho)[\beta+(1/2-\beta)\lambda]\), and entry in class \(H\) rise with research, and entry in class \(L\)
falls.
\item When class \(H\) outbids the incumbent, high-class ownership equals half the entry in class \(H\). Along a path
on which class \(H\) outbids every incumbent, ownership does not fall with strength, and it rises strictly where
research is below the cap and the spread rises strictly.
\item Along a compact path of such distributions with continuous spread and threshold, suppose that the spread
against the weakest incumbent is below the value at which research reaches its cap and that the path reaches that
value. Suppose that, up to the strength at which research reaches its cap, the exact recruitment margin rises
strictly, is negative against the weakest incumbent and is positive where research reaches its cap. Then the
equilibrium exists exactly on an interval of strengths. On it, research rises from the recruitment intensity to the
cap and then stays at the cap, up to the last strength at which the threshold does not exceed the top posterior at
the cap.
\end{enumerate}
\end{proposition}
```

### T-5.4. Intuition for Proposition 4

- **Location**: Section 5, `05:73–81`, in place of the two paragraphs; it folds in `05:44–46` and `05:115–117`.
- **Matches**: Proposition 4(b) to (d); W2 "Shared Candidate 3" (entrant composition); W3 section 5 (the kink at the switch only).
- **Scope**: as Proposition 4.

```latex
A wider spread raises the return to a purchase, so the investor chooses more research, and a purchase becomes more
likely; the posterior after a purchase then rises further above the threshold. Research adds informed purchases in
class \(H\) and removes liquidity orders in both classes, and the first effect dominates, so entry rises with slope
\((1-\rho)(1/2-\beta)\) in research. Entry in class \(H\) rises and entry in class \(L\) falls, so the challengers who
prepare are more often of class \(H\).

The low class's selling leaves this mechanism in place. A sale never recruits, and while the low class mixes, its sale
breaks even, so a success has the same value as when the low class abstains. Once a sure sale pays, the sale's
profit is a second return to research, and if research is still below its cap at that point, the research schedule
kinks upward there.

High-class ownership multiplies entry in class \(H\) by class \(H\)'s chance of beating the incumbent. When class
\(H\) outbids the incumbent, that chance is one, so ownership rises with research, as part~(c) states.

Along a path the spread and the threshold race as in Section~\ref{sec:coexistence}: a stronger incumbent raises what
a recruiting purchase earns and the belief it must reach. When the exact recruitment margin rises up to the strength
at which research reaches its cap, the race tips toward recruitment once below the cap, and part~(d) keeps the
equilibrium on one interval of strengths, which ends where even research at the cap leaves the posterior after a
purchase below the threshold.
```

### T-5.5. Corollary 3

- **Location**: Section 5, added after target 5.4, before Table 4.
- **Matches**: S5 item 4 (the full Corollary 3: no research at the weakest strength, two equilibria at middle strengths, the recruiting equilibrium at the cap up to the entry ceiling, and the three-outcome lemma); W3 "The benchmark" (the list under the default tie rules); `O1_referee.md` section 1 (floor-entry research exactly on \((r_N,r_Q)\) and above \(r_C\); uniqueness on \([r_Q,r_C]\)).
- **Scope**:
  - prior: \(1/2\);
  - tie rules: the default tie rules, named in the statement;
  - trading pattern: named for each outcome;
  - condition: \(a=\reg{res_a}\), \(\lb\approx\reg{res_cap}\), the example's slot;
  - weak or strict: "exactly on" each set; entry rises strictly on \([r_R,r_{\lb}]\).

```latex
\begin{corollary}[Research equilibria in the example]\label{cor:research-short}
In the example at the prior \(1/2\), with the research cost \(a=\reg{res_a}\) and the cap \(\lb\approx\reg{res_cap}\), let
an indifferent investor mix over its best orders and an indifferent high-cost challenger prepare. Write
\(r_R\approx\reg{res_rR}\), \(r_{\lb}\approx\reg{res_rcap}\), \(r_N\approx\reg{res_rN}\),
\(r_Q\approx\reg{res_rQ}\) and \(r_C\approx\reg{res_rC}\). On the path from \(r_0\) to \(r_2\):
\begin{enumerate}[label=(\roman*),leftmargin=2em]
\item zero research, with entry \(\rho\), is an equilibrium exactly on \([r_0,r_N]\);
\item recruiting research is an equilibrium exactly on \([r_R,r_C]\); research is below the cap on \([r_R,r_{\lb})\)
and at the cap on \([r_{\lb},r_C]\), and entry rises from \(\reg{res_entry_rR}\) at \(r_R\) to
\(\reg{res_entry_cap}\) at \(r_{\lb}\) and keeps that value up to \(r_C\);
\item floor-entry research, in which both classes trade after a success, no order recruits and entry is \(\rho\), is
an equilibrium exactly on \((r_N,r_Q)\), below the cap, and on \((r_C,r_2]\), at the cap;
\item there is no other equilibrium.
\end{enumerate}
The unique equilibrium thus has zero research at \(r_0\), recruiting research at the cap at \(r_1\) and floor-entry
research at the cap at \(r_2\); at \(r_1\) and \(r_2\) it is the equilibrium of Proposition~\ref{prop:ccc} with
\(\lambda=\lb\).
\end{corollary}
```

### T-5.6. Table 4: note and reading

- **Location**: Section 5, the note of Table 4 at `05:102–104`, in place of its text; the row label "Entry on the research branch" (`05:95`) and "High-class ownership on the branch" (`05:96`) read "on the recruiting branch"; the reading at `05:108–117`, in place of the two paragraphs (lines 115–117 go to target 5.4).
- **Matches**: Proposition 4(b); Corollary 3(ii).
- **Scope**: the example; the three intermediate strengths lie on the recruiting branch, \([r_R,r_{\lb})\).

```latex
\textit{Notes.} The example with \(a=\reg{res_a}\) and \(\lb\approx\reg{res_cap}\). The spread, the threshold and
\(\lambda_E\) are rational numbers; the other entries are rounded to six places.
```

```latex
Research and entry rise together across the three intermediate strengths in Table~\ref{tab:research}: research rises
from \(\reg{res_lambda_r155}\) through \(\reg{res_lambda_r160}\) to \(\reg{res_lambda_r165}\), and entry rises from
\(\reg{res_entry_r155}\) through \(\reg{res_entry_r160}\) to \(\reg{res_entry_r165}\). A stronger incumbent widens
the target-payoff spread, so a purchase earns more and the investor chooses more research; the posterior after a
purchase then rises above the threshold by more, and a purchase becomes more likely.
Proposition~\ref{prop:research}(b) states the same comovement wherever the equilibrium exists.
```

### T-5.7. Reading of Corollary 3

- **Location**: Section 5, `05:119–130`, in place of the two paragraphs (\(r_U\) leaves the main text).
- **Matches**: Corollary 3; Proposition 4(d) in the example (cheap-research margin; the margin negative at \(r_0\) and positive at the cap); W3 "The benchmark".
- **Scope**: as Corollary 3; the default tie rules.

```latex
The research cap is the presence probability of the example's slot, so research at the cap reproduces that slot. The
example meets the condition of Proposition~\ref{prop:research}(d): the exact recruitment margin rises strictly from
\(r_0\) to \(r_{\lb}\), is negative at \(r_0\) and is positive at \(r_{\lb}\). A researched purchase first recruits at \(r_R\),
where a purchase that just reaches the threshold also pays for its research, \(\DT(1-\tau)=k+2a\lambda_E\); there
research is \(\reg{res_lambda_rR}\) and entry \(\reg{res_entry_rR}\). Research reaches its cap at \(r_{\lb}\) and
stays there up to the entry ceiling. The low class starts to sell at \(r_N\) and sells for sure from
\(r_S\approx\reg{rS_B}\); research is at its cap before either strength, so in the example the sale's profit leaves
research unchanged.

Zero research holds up to \(r_N\), where an informed order at the entry floor starts to pay, and floor-entry research
starts there. The recruiting equilibrium therefore coexists with zero research from \(r_R\) to \(r_N\) and with
floor-entry research from \(r_N\) to \(r_Q\); from \(r_Q\) to \(r_C\) it is the only equilibrium, and above \(r_C\)
floor-entry research at the cap is the only equilibrium. Against the weak incumbent every nonzero order after a
success loses, so research is zero there. Figure~\ref{fig:research} draws the three equilibria along the path.
```

### T-5.8. Comparison with coexistence

- **Location**: Section 5, `05:148–152`, in place of the paragraph.
- **Matches**: Corollaries 2 and 3.
- **Scope**: the example.

```latex
The recruiting branch in Figure~\ref{fig:research} starts later than the informative branch of
Section~\ref{sec:coexistence}, which starts at \(r_A\approx\reg{rA}\), because a purchase must pay for research
as well as for trade. The two branches also adjust in different ways: with a fixed presence probability the purchase
rate adjusts through a mixture of the high class, while with research the intensity adjusts and the high class buys
with probability one after a success.
```

### T-5.9. The research parameter region

- **Location**: Section 5, `05:155–157`, in place of "The equilibrium patterns of Proposition~\ref{prop:research}(b) hold with strict margins exactly when"; the rest of `05:154–160` stays.
- **Matches**: Proposition A.2 (`prop:researchregion`), re-anchored to Corollary 3 (point 8 below).
- **Scope**: \(\beta=\reg{beta_B}\); strict margins; the six-strength pattern of Proposition A.1 (`prop:researchregion`), exact with \(\lambda_E<\lambda_R<\lb\) at each intermediate strength.

```latex
The pattern of Corollary~\ref{cor:research-short} at these strengths (zero research alone at \(r_0\), zero research
and recruiting research below the cap at each of the three intermediate strengths, and a unique outcome with full
orders and research at the cap at \(r_1\) and \(r_2\)) holds with strict margins exactly when
```

---

## 8. Empirical implications

The four predictions are the price-impact test with the price gap (target 8.3), the identification of the informed investor's presence (8.5), winners (8.6) and announcements (8.7). Each is stated in general form; the example's numbers follow as illustrations.

### T-8.1. Opening

- **Location**: Section 8, `08:3–9`, in place of the paragraph.
- **Matches**: S5 item 5; W5 "Full two-sided trade"; the example's full-trade range (A8).
- **Scope**: prior: every prior for the informed share; \(1/2\) for the example; tie rules: none needed above \(r_S\), where every trade choice is forced; trading pattern: full two-sided trade, defined here; condition: the example's slot for the range; weak or strict: not applicable.

```latex
The model gives predictions for publicly visible sale processes in which one bidder is prepared and a challenger has
not yet committed to diligence. Each prediction names the incumbent, prior, trading-pattern and tie-rule conditions
it needs, and concerns one target in one public state; Appendix~\ref{app:empirical} states each in full and proves it. Under full two-sided trade,
class \(H\) buys and class \(L\) sells, each with probability one, and the informed share of nonzero orders is
\(u/(2+u)\) at every prior. In the example at the prior \(1/2\) and the example's slot, full two-sided trade is the
unique outcome at every strength between \(r_S\), the strength at which a full sale earns the trading cost, and \(h\);
this range contains \(r_1\), the entry ceiling \(r_C\) and \(r_2\).
```

### T-8.2. Entry and incumbent strength

- **Location**: Section 8, `08:11–17`, in place of the paragraph.
- **Matches**: Proposition 2; Proposition A.4 (`prop:control`).
- **Scope**: as Proposition 2 ("can raise" is the existence statement on its open set); "can only lower" is weak.

```latex
\paragraph{Entry and incumbent strength.} When the price reaches the challenger before its decision, a stronger
prepared bidder can raise the probability that the challenger prepares; in the example, that probability rises by
\(\reg{entry_jump_B}\) from \(r_0\) to \(r_1\). When the price does not reach the challenger, a stronger prepared
bidder can only lower it. Against a strong enough prepared bidder, entry can return to its floor while the price stays
informative. Proposition~\ref{prop:ccc} gives the first and third comparisons, and the fixed-information control of
Section~\ref{sec:benchmark} gives the second (Proposition~\ref{prop:control}).
```

### T-8.3. Prediction 1: price impacts and the price gap

- **Location**: Section 8, `08:19–26`, in place of the paragraph.
- **Matches**: S5 item 5 (the weighted price test at every prior, the same moment as the announcement result; the entry-component trend under the reserve condition). W5 "Shared candidate 1" (\(I_+-(f_-/f_+)I_-=(e_+-\rho)A_F(M)\) under full two-sided informed trade and \(B_F(\pi)<c_H\)); W5 "Exact identity with A.14(iv)"; W5 "Entry-component trend: exact condition and counterexamples".
- **Scope**:
  - prior: below the preparation threshold, any such prior; the equal-frequency remark at \(1/2\);
  - tie rules: none needed for the test, since the prior lies strictly below the threshold; the trend uses the prepared-challenger rule of Proposition A.10(vi)(c), which the default tie rules of Section 2 supply;
  - trading pattern: full two-sided trade, named;
  - condition: \(\pi<\tau\); the trend needs a uniform incumbent, the prior and the slot fixed, full two-sided trade and recruitment persisting, and \(3p^2<\min\{\underline\theta,\underline r\}^2\);
  - weak or strict: "exactly when"; the trend is "rises".

```latex
\paragraph{The price gap and its entry component.} Under full two-sided trade at a prior below the preparation
threshold, the purchase impact \(P(1)-P(0)\), weighted by the frequency of a purchase, exceeds the sale impact
\(P(0)-P(-1)\), weighted by the frequency of a sale, exactly when a purchase recruits the challenger
(Proposition~\ref{prop:spread}). The weighted difference equals the expected price after the order opportunity minus
the price after no order, so the test needs prices and order frequencies and no auction object; at the prior \(1/2\)
the two frequencies are equal, and the test compares the two impacts directly. Under the same conditions the price
gap \(P(1)-P(-1)\) has a class component, \(\rho\DT\,[M(\pi)-m(\pi)]\), and an entry component, which is positive
exactly when a purchase recruits; the whole entry component sits in the purchase impact. As the incumbent
strengthens, entry adds more to the price through competition and less by rescuing a sale that the incumbent alone
would not complete. With a uniform incumbent and the prior and the slot fixed, the entry component rises with
strength while full two-sided trade and recruitment persist, when \(3p^2<\min\{\underline\theta,\underline r\}^2\),
where \(\underline\theta\) is the lowest challenger value and \(\underline r\) the lowest strength compared; the
example meets this condition.
```

### T-8.4. Prediction 1 in the example

- **Location**: Section 8, `08:28–31`, in place of the paragraph.
- **Matches**: Proposition A.11 in the example (A8); the existing example values.
- **Scope**: the example at \(r_1\), \(r_2\) and \(r_C\); full two-sided trade.

```latex
In the example at \(r_1\), the price gap is \(\reg{ba_r1_B}\), and its entry component is \(\reg{ba_share_r1_B}\) of
it. With a hidden price, the price gap would be \(\reg{ba_class_r1_B}\). At \(r_2\) the price gap is
\(\reg{ba_r2_B}\), the class component alone, and at the entry ceiling \(r_C\) it falls by \(\reg{ba_jump_rC_B}\).
```

### T-8.5. Prediction 2: the informed investor's presence

- **Location**: Section 8, `08:33–42`, in place of the two paragraphs.
- **Matches**: S5 item 5 (the informed share identified at a known prior and by the sale price); decision 5 (the known-prior result and the sale-price inversion; the unknown-prior local result left out). W5 "Full two-sided trade"; W5 "Sale-price identification with an unknown prior" (the inversion \(\pi(1-\pi)\lambda=\bar f(-1)I_-/(\rho\DT)\)).
- **Scope**:
  - prior: known and different from one half for counts; known, including \(1/2\), for the sale impact; the sale impact and the mean order together identify an unknown prior with the presence probability (Proposition A.11(c));
  - tie rules: none needed;
  - trading pattern: full two-sided trade;
  - condition: entry after a sale and after no order at its floor; the payoff scale \(\rho\DT\) known;
  - weak or strict: identification is exact.

```latex
\paragraph{The informed share.} Under full two-sided trade the mean order is \(\lambda(2\pi-1)\), so order counts
identify the informed investor's presence when the prior is known and differs from one half
(Proposition~\ref{prop:informedshare}). The sale impact identifies presence at any known prior, one half included:
when entry after a sale and after no order sits at its floor and the payoff scale \(\rho\DT\) is known, the sale
impact weighted by the frequency of a sale, divided by \(\rho\DT\), equals \(\pi(1-\pi)\lambda\), and together with
the mean order \(\lambda(2\pi-1)\) it identifies both the presence probability and the prior. At the prior
\(1/2\) the counts depend on the slot only through the volume of nonzero orders, so prices separate slots that counts
cannot. In the example at \(r_1\), the shares consistent with the counts and the investor's incentives form the
interval from \(\approx\reg{theta_min_counts_B}\) to \(\reg{theta_max_full_eq_r1_B}\), and a slot with share
\(\reg{alt_theta_B}\) has the example's volume and entry, but its price gap at \(r_1\) is \(\reg{alt_ba_r1_B}\),
against \(\reg{ba_r1_B}\).
```

### T-8.6. Prediction 3: winners

- **Location**: Section 8, `08:44–50`, in place of the paragraph.
- **Matches**: S5 item 5 (orders predict the winner: the sign is general, the covariance holds after the ceiling, the gap widens under outbidding). W4 "the general identity and its sign" (gap \((M-m)\Omega\), positive iff \(\Pr_F(D(R)>0)>0\)); W4 "the covariance constants agree" (\(\Cov(X,\text{win})=2\pi(1-\pi)\rho\lambda\Omega\) where entry is at its floor); W4 "High-class outbidding: the useful shared economic condition".
- **Scope**:
  - prior: any for the sign and the covariance; fixed for the trend;
  - tie rules: none needed;
  - trading pattern: full two-sided trade, named, at every strength the trend compares;
  - condition: the incumbent's value falls with positive probability where the class laws differ; entry at its floor after every order for the covariance; class \(H\) outbids every incumbent, prior and slot fixed for the trend;
  - weak or strict: the sign is "exactly when"; the trend is weak ("does not narrow"), strict where the low class loses wins.

```latex
\paragraph{Winners.} Under full two-sided trade, a prepared challenger wins more often after a purchase than after a
sale exactly when the incumbent's value falls, with positive probability, where a high-class value is more likely
than a low-class value to beat it; the gap is \(M(\pi)-m(\pi)\) times the difference between the classes' chances of
beating the incumbent (Proposition~\ref{prop:winner}). Orders predict the winner even where they no longer predict
entry: where entry stays at its floor after every order, as above the entry ceiling, the order still covaries
positively with a challenger win under the same condition, and not with entry. With the prior and the slot fixed and
full two-sided trade at each strength compared, when class \(H\) outbids every incumbent the gap does not narrow as
the incumbent strengthens, and it widens wherever the stronger incumbent takes wins from the low class. Among
prepared challengers, the share of the high class at each price is the price-implied posterior, which rises with the
price under full two-sided trade. In the example class \(H\) outbids every incumbent, and the gap is
\(\reg{wgap_r1_B}\) at \(r_1\) and \(\reg{wgap_r2_B}\) at \(r_2\); the covariance of the order with entry is
\(\reg{cov_entry_r1_B}\) at \(r_1\) and zero at \(r_2\).
```

### T-8.7. Prediction 4: announcements

- **Location**: Section 8, `08:52–57`, in place of the paragraph.
- **Matches**: S5 item 5 (the exact announcement condition; the weighted test as the same moment). W5 "Announcement returns and A.14 positivity"; W5 "Exact identity with A.14(iv)".
- **Scope**:
  - prior: every prior;
  - tie rules: every equilibrium, so no tie rule is needed;
  - trading pattern: any for the positivity; full two-sided trade at a prior below the preparation threshold, with a recruiting purchase, for the no-order drop;
  - condition: preparation still uncertain after some order;
  - weak or strict: "exactly when"; the mean over both reports is zero.

```latex
\paragraph{Announcements.} If a public event after the price reveals only whether the challenger prepared, the mean
price change over preparation reports is positive exactly when preparation was still uncertain after some order, at
every prior and in every equilibrium (Proposition~\ref{prop:announcement}); in the example it is
\(\reg{evprep_mean_r1_B}\) at \(r_1\). The mean change over both reports, with their model probabilities, is zero. Under
full two-sided trade at a prior below the preparation threshold, an opportunity that passes with no order is no news
about the class and, when a purchase recruits, bad news about entry: in the example at \(r_1\), the price after no
order minus the expected price before the opportunity is \(\reg{pdrop_neutral_r1_B}\), and the size of this drop is
the weighted difference of the price-impact test.
```

### T-8.8. Two clusters

- **Location**: Section 8, `08:59–62`, in place of "At one public strength in the range ... In one cluster there is no informed trade, the mean order is zero and the three prices coincide." The rest of the paragraph stays, with "in the benchmark" at `08:62–63` reading "in the example".
- **Matches**: Corollary 2 (coexistence on \([r_A,r_N]\), full purchase on \([r_F,r_N]\)).
- **Scope**: the example at the prior \(1/2\); the default tie rules.

```latex
\paragraph{Two clusters at intermediate strengths.} In the example, at one public strength in the range
\((r_F,r_N)\) of Section~\ref{sec:coexistence}, processes can form two clusters. In one cluster the market is quiet:
the mean order is zero and the three prices coincide.
```

---

## 9. Conclusion

### T-9.1. Results

- **Location**: Section 9, `09:9–15`, in place of the paragraph.
- **Matches**: Proposition 2; Proposition 3(a); the two numbers (S5 item 1); Proposition 4(a), (b).
- **Scope**:
  - prior: any for the first two sentences; even for research;
  - tie rules: "an indifferent investor may mix over its best orders" named for research; coexistence relies on the default tie rules (point 5 below);
  - trading pattern: the recruiting equilibrium for research;
  - condition: "on an open set of parameters";
  - weak or strict: entry rises strictly while the high class mixes.

```latex
The comparison of the weak, strong and very strong incumbent holds with unique outcomes on an open set of
parameters. A quiet market and an informative market coexist exactly on a region of the target-payoff spread and the
preparation threshold, and a stronger incumbent moves the economy across that region; in the informative market,
entry rises with the spread while the high class mixes between a purchase and abstention and stays constant once it
buys for sure. When information is costly, competition creates research: at an even prior, when an indifferent
investor may mix over its best orders, research and entry rise together with the spread until research reaches its
cap, in the equilibrium in which a purchase after successful research recruits, and the low class's selling does not
interrupt the rise.
```

### T-9.2. Sale terms

- **Location**: Section 9, `09:17–21`, in place of the paragraph.
- **Matches**: Proposition A.8 (`prop:access`, under the hypotheses of Proposition 2, at \(F_1\)); Proposition A.9 (point masses with \(0<\ell<\bar r<h\)); Proposition A.10 (`prop:reserves`).
- **Scope**: the hypotheses of Proposition 2 for access; one value per class with the incumbent's highest value between them for the payment rule.

```latex
Sale terms affect entry through the challenger's expected payment and through the information in the stock price.
Under the hypotheses of the main result, access to prices raises target proceeds and acquisition surplus net of
preparation costs against the strong incumbent, and, with a single value in each class and the incumbent's highest
value between them, the weight that the payment rule places on the runner-up's value decides how competition moves
the target-payoff spread. A reserve that excludes the low class can make the price informative against both
incumbents; if informed trade is then full and only a purchase recruits at both strengths, entry is flat in
incumbent strength.
```

### T-9.3. The next step and the tests

- **Location**: Section 9, `09:23–26`, in place of the paragraph.
- **Matches**: S5 item 5 (the weighted test).
- **Scope**: the investor always buys after good news and always sells after bad news, which is probability one; the prior below the threshold.

```latex
The next theoretical step is the seller's choice of terms with the whole pricing and trading continuation retained.
The empirical tests ask whether the challenger's preparation in visible sale processes responds to incumbent
strength when the price precedes the decision, and, where the investor always buys after good news and always sells
after bad news and the prior lies below the preparation threshold, whether a purchase raises the price by more than a sale lowers
it once each impact is weighted by how often its order occurs, as Section~\ref{sec:empirical} predicts where a
purchase recruits.
```

---

## Keys used by the targets

Every `\reg` key in the targets exists in the numbers table. The keys added to the table for these targets are:

| Key | Quantity | Value | Used in |
|---|---|---|---|
| `share_H_r0` | class \(H\)'s takeover share at \(r_0\) in the example: \(\pi\rho/[\pi\rho+(1-\pi)\rho W_L(r_0)]\) with \(W_L(r_0)=\ell/r_0\) | \(6/11\approx0.545455\) | T-1.3, T-4.4a, T-4.4b |
| `share_H_r1_B` | class \(H\)'s takeover share at \(r_1\) in the example's slot: \(\pi e_H/[\pi e_H+(1-\pi)e_LW_L(r_1)]\), with \(e_H=\rho+(1-\rho)(b+\lambda)\), \(e_L=\rho+(1-\rho)b\), \(W_L(r_1)=\ell/r_1\) | \(\approx0.830691\) | T-1.3, T-4.4a, T-4.4b |
| `cH_DA_floor_B` | the decisive-advantage bound \((h^2-p^2)/(2h)\) at the example's \(h\) and \(p\) | \(399/80\) | T-4.4b, T-4.13 |
| `cH_afford_ceiling_B` | the affordability bound \(h-r_2\) of the uniform instance of Proposition 3(c) | \(32/5\) | T-4.13 |
| `res_rQ` | \(r_Q\): the end of floor-entry research below the entry ceiling, the zero of the floor margin, \(\tau(r_Q)=M_\lambda\) at \(\lambda=\lambda_Q(\DT(r_Q))\) | \(\approx2.166995\) | T-5.5 |

The key `rA` prints the start of coexistence \(r_A\) in T-1.4, T-4.12 and T-5.8; `res_rA` holds the same value and is not used.

---

## Points settled by the referee

1. **Proposition 3(c), the uniform instance (proof O9).** The proof stands. Part (c) stands without the fallback, and T-4.12 cites "the condition of Proposition 3(c)".
2. **Proposition 2, strictness of the takeover share (proof O6).** The share is nondecreasing, rises strictly exactly when \(W_L(F_0)>0\), and equals one at both incumbents when \(W_L(F_0)=0\). T-4.1 is right.
3. **The liquidity footnote (proof O2).** Propositions 1 to 4 hold for every \(0<\beta<1/2\); the footnote of T-2.3 is the text of the proof.
4. **Proposition 4(d) (proofs O3 and O4).** "Rises" is strict and only up to the first strength at which research reaches its cap; the path is compact with continuous spread and threshold, \(\tau<1\) up to that strength, and a spread against the weakest incumbent below the cap spread; \(\DT>2k\) is no separate hypothesis; the end is the last strength with \(\tau\le M_{\lb}\). T-5.3(d) states this.
5. **Tie rules in the summary sentences on coexistence.** The default tie rules are the model's standing rule (T-2.5), so T-ABS and T-9.1 need no tie phrase for coexistence. The mixing-investor phrase stays wherever research is summarized.
6. **Proposition 4 under the other challenger rule.** Not a missing qualifier. T-5.3 carries the sentence of the frozen main-text form on the alternative rule.
7. **Research in the two-numbers passage.** The reduction lemma holds at every prior; "the same research" needs the research cost and the cap held fixed, which T-3.6 states.
8. **The anchor of Proposition A.1 (research region).** The proposition gives exactly the six-strength pattern; T-5.9 names the pattern.
9. **Labels.** Corollary 1 is `prop:region` (second label `cor:ccc-example`), Corollary 2 is `cor:example-coexistence`, Corollary 3 is `cor:research` with the main-text form `cor:research-short`. `prop:spread` is the label of Proposition A.10.
10. **The highest strength of a uniform path.** No symbol is needed; the targets use "the lowest strength" and "the highest strength".
11. **Ranked classes in the robustness paragraph.** The signal sentence of `01:77–83` needs no change.
12. **Identification with an unknown prior.** Proposition A.11(c) carries the sale-price inversion with the counts; T-8.5 states that the sale impact and the mean order identify both the presence probability and the prior.
13. **The lowest strength in the entry-component trend.** The condition binds at the weakest incumbent of the stretch compared; T-8.3 reads "compared".
14. **Ownership in the abstract and the opening claim.** T-ABS and T-1.1 match Proposition A.5.
15. **Uniqueness in the example's research list.** The sentence holds under all four tie rules, so T-1.5 needs no qualifier.

---

## Changes after the referee

The referee marked 43 targets "match", 11 "missing qualifier" and 5 "overclaim". Every mark other than "match" is applied, together with every settled point and the coordinator's decisions. The list of issues WR-01 to WR-28 is not part of the referee's report, so each change is named by its target, and a decision that carries a number keeps it.

**Marks other than "match"**

| Target | Mark | Change |
|---|---|---|
| T-1.2 | missing qualifier | The share clause is a clause of the sentence about outbidding at the strong incumbent ("if, in addition, a low-class challenger beats the weak incumbent with positive probability"); the scope line says so. |
| T-1.4 | missing qualifier | "covers it" reads "earns more than it". |
| T-1.7, T-9.3 | missing qualifier | "always buys ... always sells" stands for "buys ... sells"; the scope lines say probability one. |
| T-2.3 | overclaim | The footnote is the text of the footnote in the proof of the liquidity bound: the common posterior bound and the exclusion bound use \(\beta\le1/3\), the research parameter region and the slot-feasibility statements of identification range over the model's slots, and the other results hold for every \(0<\beta<1/2\). Proposition 4 is in the list of results that hold. |
| T-2.5 | overclaim | The sentence says that the appendix states a change beside each result and that the table collects the changes for coexistence in the example at the prior \(1/2\). |
| T-3.1 | missing qualifier | "weakly lowers" and "weakly raises the sensitivity of target proceeds", as Proposition 1 states. |
| T-3.6 | missing qualifier | "with every other primitive and the tie rules the same" stands for "with the same prior, costs, slot and tie rules", so that the research cost and the cap are included. The scope line records that the reduction lemma holds at every prior. |
| T-4.3 | missing qualifier | "can lower that chance"; the shift in the takeover share is stated for the case in which a low-class challenger can beat the weak incumbent. |
| T-4.8 | overclaim | "the informative market that coexists with it" stands for "an informative market"; "earns more than it" for "covers it". |
| T-5.3 | missing qualifier | Part (d) takes the four hypotheses of the full statement: a compact path with continuous spread and threshold, a spread against the weakest incumbent below the cap spread that the path reaches, a margin that rises strictly, and the margin condition up to the strength at which research reaches its cap. |
| T-5.4 | missing qualifier | The kink needs research below its cap at the switch, and the race tips "once below the cap". |
| T-5.7 | overclaim | The margin "rises strictly from \(r_0\) to \(r_{\lb}\), is negative at \(r_0\) and is positive at \(r_{\lb}\)". |
| T-5.9 | missing qualifier | The sentence names the six-strength pattern, with research below the cap at the intermediate strengths. |
| T-8.2 | overclaim | "entry can return to its floor". |
| T-8.7 | missing qualifier | The sentence on the no-order opportunity holds under full two-sided trade at a prior below the preparation threshold, and says that it is no news about the class. |

**Coordinator decisions**

- **T-4.9 (WR-18).** Part (c) is the frozen main-text form: "the product of the spread and \(g_H-c_H\) does not fall with strength", with the uniform instance and no start hypothesis. T-1.4 and T-4.10 keep the proportional words together with the start hypothesis; the last sentence of T-4.10 says that part (c) states the condition as a product.
- **Corollary labels (WR-26).** Corollary 1 is `prop:region` with `cor:ccc-example` (T-4.4a, T-1.3, T-4.6, T-4.11), titled "Recruitment and ownership in the example"; Corollary 2 is `cor:example-coexistence` (T-4.11); Corollary 3 is `cor:research-short` in the main-text environment (T-5.5, T-5.9), the label of its full statement being `cor:research`. The frozen full statement of Corollary 1 in A.tex holds `prop:region` and `cor:ccc-example`, and the frozen main-text form holds `form:ccc-example-main`. Where the main-text environment of T-4.4a and the appendix statement both carry `prop:region`, one of them gives the label up when the manuscript is assembled.
- **The exact recruitment margin (WR-20, WR-28).** T-5.2 defines "the exact recruitment margin"; T-5.3(d), T-5.4 and T-5.7 use the words, and a line among the conventions records the vocabulary.
- **The cap (WR-21).** T-5.5, its scope line and the note of T-5.6 write \(\lb\approx\reg{res_cap}\).
- **One key for \(r_A\) (WR-22).** T-5.8 prints `rA`, as T-1.4 and T-4.12 do.
- **The scope line (WR-23).** The scope line of T-8.3 says that no tie rule is needed for the test and that the trend uses the prepared-challenger rule, which the default tie rules supply.
- **Optional changes (WR-24, WR-25).** The referee lists three. I adopted all three: T-5.3 carries the sentence on the alternative challenger rule from the main-text form of Proposition 4; T-8.5 adds that the sale impact and the mean order identify both the presence probability and the prior; T-8.1 takes the wording of the frozen main-text opening of Section 8 ("names the incumbent, prior, trading-pattern and tie-rule conditions it needs, and concerns one target in one public state"). T-8.3 reads "compared" for "considered" (referee point 13).
- **Placeholders.** Every key is real: no placeholder is left, and the closing table is "Keys used by the targets".

**Disagreements**

None.

**Language scan**

No LaTeX block holds a status word, a defensive phrase, a development word or a process word. The hits in the LaTeX blocks are the label `sec:benchmark` (it does not print), the tie phrases, "more likely" as a probability, "no longer" in a comparison across states ("orders no longer predict entry"), and "interval of strengths" in T-5.3(d) and T-5.4, which rests on Proposition 4(d). The hits outside the LaTeX blocks are references that locate a target and name its source, and quotations of the text a target replaces.
