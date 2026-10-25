# Main-text wording targets: the referee's report

Stage S4. The referee read `statements/wording_targets.md`, the prose writer's file, against the formal statements `A.tex`, `B.tex`, `C.tex` and `D.tex`, their notes and referee reports, the proofs in `O1` to `O9`, `plan/NOTATION.md`, and `plan/PLAN.md` (Part 1, S4, S9 and S10, Part 6). The version read carries the keys `share_H_r0`, `share_H_r1_B`, `cH_DA_floor_B`, `cH_afford_ceiling_B` and `res_rQ` in place of the earlier placeholders. These keys agree with `A.tex` and `C.tex`, and each exists in the numbers table.

The marks are those of the brief: "match", "missing qualifier", "overclaim", "wrong".

## Verdict

The file holds 59 targets: 43 match, 11 have a missing qualifier, 5 overclaim, and none is wrong. PLAN S4 acceptance asks for no overclaim and every qualifier present, so the file does not meet it as it stands. Each of the 16 fixes in Part 2 is a clause or a sentence inside its target, and none needs a change to a frozen statement.

The four qualifiers that PLAN S4 names are present, with one condition:
- prior 1/2 and the mixing investor stand in every research target: T-ABS, T-1.5, T-5.3 and T-9.1;
- two-sided trade stands in every test target once T-1.7 and T-9.3 say "always";
- a prior below the threshold stands with the weighted test in T-1.7, T-8.3 and T-9.3;
- the prior and the slot are fixed for the winner trend in T-8.6.

One item is a choice for the coordinator, not a defect. T-4.9 gives Proposition 3(c) a start hypothesis that the frozen main-text form leaves out (Part 5, item 4).

## 1. Marks

| Target | Mark | Finding | Fix |
|---|---|---|---|
| T-ABS | match | Every clause follows: Proposition 2 with the open set of A.tex "Value classes and priors"; the fixed-information control under the default challenger rule; Proposition 3(a); Proposition 4(a), (b) at prior 1/2 with the mixing investor; the access proposition at \(F_1\). | none |
| T-1.1 | match | "Can" carries the existence statement; the ownership rise is on the open set (point 14). | none |
| T-1.2 | missing qualifier | The share clause stands as a second "when" clause, so it can be read without outbidding at \(F_1\). The formal statement gives the share rise from \(W_L(F_0)>0\) only under \(W_H(F_1)=1\); otherwise the exact condition is (eq:a3-share). | 2.1 |
| T-1.3 | match | Corollary 1(a), (d); the share keys match A.tex. | none |
| T-1.4 | missing qualifier | The region is closed at \(\DT=\DT^{\rm N}\), but "no order against an uninformative price covers it" excludes a unit order that just earns \(k\), so the boundary fails. The rest matches the reduction lemma, the two-numbers lemma and Proposition 3(a) to (c). | 2.2 |
| T-1.5 | match | Proposition 4(a) to (c) at prior 1/2 with the mixing investor; Lemma `lem:a5-sale` for the low class; Corollary 3. The last sentence holds under all four tie rules (point 15). | none |
| T-1.6 | match | Proposition `prop:payment`: point masses with \(0<\ell<\bar r<h\); the spread effect has the sign of \(1-2\omega\). | none |
| T-1.7 | missing qualifier | "Buys after good news and sells after bad news" admits mixing, and under mixing the weighted test is not "exactly when" (Proposition A.10(i): the term \(e(0)\DT[\pi-\mu(0)]\) enters). Full trade, with probability one, is the hypothesis of A.10(ii). The scope line claims "with probability one", but the LaTeX lacks it. | 2.3 |
| T-1.8 | match | Proposition 2 stands in full in Section 4.1, so the appendix list is right. | none |
| T-2.1 | match | NOTATION (c) "Paths"; "first-order stochastic strengthening" is Proposition 1's own phrase. | none |
| T-2.2 | match | A common rescale of values, reserve and the costs \(c_H\), \(k\), \(a\) leaves every comparison and \(\Psi/a\) unchanged. | none |
| T-2.3 | overclaim | "Only the posterior bound at the zero order uses \(\beta\le1/3\)" leaves out the research parameter region and the slot-feasibility statements of identification, which range over the model's slots (A.tex `par:beta-scope`; O2). It also lists Propositions 2 and 3 only, where O2 gives Propositions 1 to 4. A-17 assigns this target the O2 text. | 2.4 |
| T-2.4 | match | Notation. | none |
| T-2.5 | overclaim | Table `tab:a4-ties` covers coexistence in the example at prior 1/2 only (its caption says so). The other tie-rule changes stand elsewhere: the general region (B.tex "Other tie rules"), research (`rem:researchties`) and the empirical tests (A.10(iii)). "Records each conclusion that another tie rule changes" therefore says more than the table holds. The default-rule sentence is right, and it makes the defaults the model's standing rule (point 5). | 2.5 |
| T-2.6 | match | Definitions agree with D.tex and A.tex Proposition 2(ii). | none |
| T-3.1 | missing qualifier | Proposition 1 is weak ("weakly decreases", "weakly increases"), but "this lowers acquisition profit ... makes target proceeds more sensitive" reads as strict for every continuous distribution. The present sentence leans on the uniform closed forms, which move to Section 4.2. | 2.6 |
| T-3.2 | match | \(\bar\Gamma=\DT+\gamma\) (A.tex `lem:twonumbers`). | none |
| T-3.3 | match | Weak, as Proposition 1. | none |
| T-3.4 | match | Notation. | none |
| T-3.5 | match | Pointer. | none |
| T-3.6 | missing qualifier | The reduction lemma fixes the research cost \(a\) and the cap \(\lb\) for "the same research". The list "prior, costs, slot and tie rules" leaves the cap out, since the cap is neither a cost nor the slot in the research section. The threshold sentence carries its qualifier \(g_L\le c_H\), which is \(\tau\ge0\) in `lem:twonumbers`. | 2.7 |
| T-4.1 | match | A.tex Proposition 2(ii) and O6, word for word in substance. | none |
| T-4.2 | match | Pointer to the open set of T-4.4. | none |
| T-4.3 | missing qualifier | "A stronger incumbent lowers that chance when class \(H\) can lose" is strict, but \(W_H\) is only nonincreasing (Proposition 1). Likewise, "the takeovers ... shift toward class \(H\)" is strict only when \(W_L(F_0)>0\) (Proposition 2(ii)). The sufficient condition, the recruitment sentence and the decisive-advantage sentence match `lem:decisive`. | 2.8 |
| T-4.3b | match | Pointer. | none |
| T-4.4 | match | The declarations and the open-set sentence agree with Corollary 1 and the parameters table. | none |
| T-4.4a | match | Corollary 1(a) and (c); the entry and ownership at other priors in the band follow from Proposition 2 with \(W_H=1\). The title and label differ from A.tex (Part 3). | Part 3 |
| T-4.4b | match | Corollary 1(d), (e) and `lem:decisive`; the share rises strictly because \(W_L(r_0)>0\) (O6). | none |
| T-4.5 | match | The closed forms re-derived from the auction agree, and \(\tau(r)\) at the example's values is \((12r-3/4)/(20r-r^2-1)\). | none |
| T-4.6 | match | Full Corollary 1(b). For \(u>\) `u_hi_frac`, \(M>\tau(r_2)\), so either full orders at \(r_2\) recruit or the orders of part (iii) fail, and a conclusion fails at \(r_2\). | none |
| T-4.6a | match | Caption. | none |
| T-4.7 | match | D.tex example (b): \(B_r(M)\) falls strictly above \(\ell\), so (H3) holds on \((r_C,h)\). | none |
| T-4.8 | overclaim | "In an informative market a purchase recruits a high-cost challenger": by NOTATION an informative market is any equilibrium with informed trade, and between the weak and the strong incumbent mixed orders at the entry floor (form Q on \((r_N,r_J)\)) are informative and recruit no one. The "covers" boundary of T-1.4 recurs here. | 2.9 |
| T-4.9 | match | (a) is B.tex (a) and (b) is B.tex (b) without its gap sentence; (c) holds under the hypotheses as written. Its start hypothesis is absent from the frozen main-text form (Part 5, item 4). | Part 5, item 4 |
| T-4.10 | match | B.tex (a) to (c); "where the threshold is positive" lies inside the \(\tau\ge0\) of `lem:twonumbers`. | none |
| T-4.11 | match | B.tex main-text Corollary 2, with the band of Corollary 1 equal to \(\tau(r_1)<M<\tau(r_2)\). The label differs (point 9). | Part 3 |
| T-4.12 | match | B.tex (c)(i), (c)(iii), Lemma `lem:a4-path`(b) and full Corollary 2. The numbers are ordered as stated: \(r_A<1.40<1.45<r_F\). | none |
| T-4.13 | match | A.tex Corollary 1(e); its keys equal those of A.tex. | none |
| T-4.14 | match | Corollary A.2 (b) to (d). | none |
| T-5.1 | match | Rule 3 sentence. | none |
| T-5.2 | match | Lemma `lem:a5-sale`, equation (eq:research-im), and the unique root for \(\DT>2k\). The margin defined is the exact margin \(\varphi_a^*\). The vocabulary conflicts with NOTATION (Part 5, item 3). | Part 3 |
| T-5.3 | missing qualifier | Parts (a) to (c) match C.tex. Part (d) lacks four hypotheses of C.tex (d): a compact path with continuous spread and threshold; a spread at the weakest incumbent below the cap spread, with the path reaching it; a margin that rises strictly, where the target says "rises" with no strictness; and a margin condition stated only up to the first cap strength. | 2.10 |
| T-5.4 | missing qualifier | "The research schedule kinks upward at that point" needs the sale to become strictly profitable below the cap (C.tex main-text (b)). In the example research is at its cap first. "Tips toward recruitment once and does not tip back" holds only up to the cap, since recruitment ends at the entry ceiling. | 2.11 |
| T-5.5 | match | C.tex Corollary 3(a), (b), Lemma `lem:a5-floor` and Lemma `lem:a5-outcomes`. The printed cap uses "=" with a rounded value (Part 3). | Part 3 |
| T-5.6 | match | Proposition 4(b). The rising posterior gap holds at the three strengths (Part 6). The cap display matches T-5.5 (Part 3). | Part 3 |
| T-5.7 | overclaim | "The recruitment margin rises along the path": O4 and C-06 prove a strict rise on \([r_0,7/4]\), which contains \([r_0,r_{\lb}]\), and on the rest of the path only that the margin is positive. Proposition 4(d) needs the rise only up to \(r_{\lb}\). The rest of the target matches Corollary 3 and the ordering \(r_{\lb}<r_N<r_S\). | 2.12 |
| T-5.8 | match | \(r_A<r_R\). Two keys print \(r_A\) (Part 3). | Part 3 |
| T-5.9 | missing qualifier | Proposition A.1 (`prop:researchregion`) is exact for the six-strength pattern with \(\lambda_E<\lambda_R<\lb\) at each intermediate strength. The main-text Corollary 3 does not list the intermediate strengths, so "the equilibria of Corollary 3 at the three intermediate strengths" leaves the pattern, and its "below the cap", unstated. | 2.13 |
| T-8.1 | match | D.tex standing paragraph and example (a). | none |
| T-8.2 | overclaim | "Against a strong enough prepared bidder, entry returns to its floor while the price stays informative" reads as a law. Proposition 2(iii) shows that it can happen under (H3), and on a path whose spread stays below \(k/(\rho\kappa)\) full trade can fail. The first sentence already says "can raise". | 2.14 |
| T-8.3 | match | A.10(i), (ii), (iv) and (vi)(b), (c). The trend uses the prepared-challenger rule of (vi)(c), which the default of T-2.5 supplies, so the scope line's "tie rules: none needed" holds for the test only. The reserve condition at the lowest compared strength suffices (point 13). | none |
| T-8.4 | match | D.tex example (c); the keys equal the main-text form of D. | none |
| T-8.5 | match | A.11(a), (b), (c) and the example (d) under the default investor rule. The joint identification can be added (point 12). | none |
| T-8.6 | match | A.12(ii), (iii), (v). The covariance needs only entry at its floor after every order, which follows from A.12(i). | none |
| T-8.7 | missing qualifier | "An opportunity that passes with no order is bad news about entry when a purchase recruits" is stated generally but needs \(\pi<\tau\), so that \(e(0)=\rho\); for \(\tau\le\pi\), \(e(0)=1\). D's main-text form puts it under full two-sided trade while gross profit at the prior falls short of \(c_H\). The rest matches A.13(i) to (iv). | 2.15 |
| T-8.8 | match | Full Corollary 2 and the D example (h) under the default rules. | none |
| T-9.1 | match | As T-ABS; "entry rises while the high class mixes" is B.tex (a). | none |
| T-9.2 | match | `prop:access` (under Proposition 2's hypotheses, at \(F_1\)), `prop:payment` and `prop:reserves`(a); "only a purchase recruits at both strengths" is \(B_0(\pi)<c_H<B_1(M)\le B_0(M)\). | none |
| T-9.3 | missing qualifier | The same "always" as T-1.7. | 2.3 |

## 2. Fixes

Each fix keeps the rest of its target.

### 2.1 T-1.2

```latex
challenger, so entry rises even though acquisition profit falls at every fixed belief. When a prepared high-class
challenger beats the strong incumbent for sure, the probability that a challenger from the high class acquires the
target rises with entry; if, in addition, a low-class challenger beats the weak incumbent with positive probability,
the high class also wins a larger share of the takeovers that go to a challenger. With the very strong incumbent, the
price stays informative, but even the most favorable price fails to justify preparation at the high cost, so entry
returns to its floor.
```

### 2.2 T-1.4

In place of "but narrow enough that no order against an uninformative price covers it":

```latex
but narrow enough that no order against an uninformative price earns more than it
```

### 2.3 T-1.7 and T-9.3

T-1.7, first clause:

```latex
When the investor always buys after good news and always sells after bad news and the prior lies below the
preparation threshold,
```

T-9.3, the same words: "where the investor always buys after good news and always sells after bad news and the prior lies below the preparation threshold". The unchanged sentence at `01:38` uses the phrase for the derived equilibrium of Proposition 2 and needs no change.

### 2.4 T-2.3

The footnote of `O2/O2_proof.tex`, lines 7 to 10:

```latex
\footnote{The posterior bound common to all orders, and through it the exclusion bound of
Section~\ref{sec:inference}, use \(\beta\le1/3\). The research parameter region and the slot-feasibility statements
in identification range over the slots of the model. The other results hold for every \(0<\beta<1/2\)
(Appendix~\ref{app:beliefs}).}
```

### 2.5 T-2.5

```latex
When ties arise, an indifferent investor may mix over its best orders, and an indifferent high-cost challenger
prepares. I call these the default tie rules. Where another tie rule changes a conclusion, the appendix states the
change beside the result, and Table~\ref{tab:a4-ties} in Appendix~\ref{app:coexistence} collects the changes for
coexistence in the example at the prior \(1/2\).
```

### 2.6 T-3.1

```latex
A stronger incumbent outbids a prepared challenger more often, and when it does, it pays the challenger's bid.
Proposition~\ref{prop:returns} shows that this weakly lowers acquisition profit at every fixed belief and weakly
raises the sensitivity of target proceeds to challenger quality, for every continuous incumbent distribution; the
second effect uses the class ranking~\eqref{eq:classes}.
```

### 2.7 T-3.6

In place of the third sentence of the first paragraph:

```latex
Two auctions with the same spread and the same threshold, and with every other primitive and the tie rules the
same, therefore have the same equilibrium orders, posteriors and entry, and, when the investor chooses research, the
same research.
```

### 2.8 T-4.3

In the first paragraph, "and a stronger incumbent lowers that chance when class \(H\) can lose" becomes:

```latex
and a stronger incumbent can lower that chance when class \(H\) can lose.
```

The end of that paragraph:

```latex
the stronger incumbent then takes wins only from the low class, and when a low-class challenger can beat the weak
incumbent, the takeovers that go to the challenger shift toward class \(H\).
```

### 2.9 T-4.8

```latex
Between the weak and the strong incumbent of Proposition~\ref{prop:ccc}, two equilibria can hold against the same
incumbent. In a quiet market the investor does not trade, the price carries no information, and entry stays at its
floor; in the informative market that coexists with it, a purchase recruits a high-cost challenger. The two numbers
of Section~\ref{sec:twonumbers} decide where both exist: the threshold must lie above the prior and within reach of
a purchase, and the spread must be wide enough that a purchase that just reaches the threshold covers the trading
cost, yet narrow enough that no order against an uninformative price earns more than it.
```

### 2.10 T-5.3, part (d)

```latex
\item Along a compact path of such distributions with continuous spread and threshold, suppose that the spread
against the weakest incumbent is below the value at which research reaches its cap and that the path reaches that
value. Suppose that, up to the strength at which research reaches its cap, the recruitment margin rises strictly, is
negative against the weakest incumbent and is positive where research reaches its cap. Then the equilibrium exists
exactly on an interval of strengths. On it, research rises from the recruitment intensity to the cap and then stays
at the cap, up to the last strength at which the threshold does not exceed the top posterior at the cap.
```

With the vocabulary item of Part 5, item 3, "the recruitment margin" here and in T-5.2, T-5.4 and T-5.7 reads "the exact recruitment margin".

### 2.11 T-5.4

Second paragraph, last sentence:

```latex
Once a sure sale pays, the sale's profit is a second return to research, and if research is still below its cap at
that point, the research schedule kinks upward there.
```

Fourth paragraph, second sentence:

```latex
When the recruitment margin rises up to the strength at which research reaches its cap, the race tips toward
recruitment once below the cap, and part~(d) keeps the equilibrium on one interval of strengths, which ends where
even research at the cap leaves the posterior after a purchase below the threshold.
```

### 2.12 T-5.7

```latex
The example meets the condition of Proposition~\ref{prop:research}(d): the recruitment margin rises strictly from
\(r_0\) to \(r_{\lb}\), is negative at \(r_0\) and is positive at \(r_{\lb}\).
```

### 2.13 T-5.9

```latex
The pattern of Corollary~\ref{cor:research} at these strengths (zero research alone at \(r_0\), zero research and
recruiting research below the cap at each of the three intermediate strengths, and a unique outcome with full orders
and research at the cap at \(r_1\) and \(r_2\)) holds with strict margins exactly when
```

### 2.14 T-8.2

```latex
Against a strong enough prepared bidder, entry can return to its floor while the price stays informative.
```

### 2.15 T-8.7

In place of the sentence that begins "An opportunity that passes with no order":

```latex
Under full two-sided trade at a prior below the preparation threshold, an opportunity that passes with no order is no
news about the class and, when a purchase recruits, bad news about entry: in the example at \(r_1\), the price after
no order minus the expected price before the opportunity is \(\reg{pdrop_neutral_r1_B}\), and the size of this drop
is the weighted difference of the price-impact test.
```

## 3. Notes on rows marked "match"

- **Corollary titles and labels.** T-4.4a has the title "Where the example meets Proposition 2", while A.tex has "Recruitment and ownership in the example". The labels `cor:region` (T-4.4a) and `cor:coexistence` (T-4.11) differ from the frozen labels (point 9; Part 5, item 1). T-5.5's `cor:research` is the full statement's label in C.tex, whose main-text form carries `cor:research-short`.
- **The rounded cap.** T-5.5 writes \(\lb=\reg{res_cap}\), and the T-5.6 note writes the same. Under C-14 the frozen short corollary omits the rounded cap, and the other fragments print it with \(\approx\). Write "\(\lb\approx\reg{res_cap}\)" or "the cap at the presence probability of the example's slot".
- **Two keys for \(r_A\).** T-1.4 and T-4.12 print `rA`, and T-5.8 prints `res_rA`. Both hold 1.393958, so one key serves all three.
- **Vocabulary of the margin.** T-5.2 attaches "recruitment margin" to the exact margin (Part 5, item 3).
- **Scope lines that do not print.** T-8.3's "tie rules: none needed" covers the test but not the trend (row T-8.3). The "Matches" lines of T-1.6, T-8.2 and T-9.2 cite appendix propositions by the count before decision 7; the LaTeX cites labels, so the printed numbers follow the label map.
- **Optional.** T-8.5 can add the joint identification of presence and the prior (point 12). T-5.3 can add the clause of C's main-text form on the alternative challenger rule (point 6). T-8.1 can take D's wording "names the incumbent, prior, trading-pattern and tie-rule conditions it needs, and concerns one target in one public state".

## 4. The points for the referee, settled

1. **Proposition 3(c), the uniform case (O9).** O9 holds (`O9/O9_proof.tex`; B.tex (c)(iii)). Part (c) stands as drafted, with no fallback, and T-4.12 cites "the condition of Proposition 3(c)".
2. **Strictness of the takeover share (O6).** By A.tex Proposition 2(ii) and O6, the share is nondecreasing, rises strictly exactly when \(W_L(F_0)>0\), and equals one at both laws when \(W_L(F_0)=0\). T-4.1 is right. The lens condition \(W_L(F_1)>0\) is sufficient only.
3. **The liquidity footnote (O2).** O2 gives Propositions 1 to 4 for every \(0<\beta<1/2\), and also Corollaries 1 and 2 and Corollary A.2; Corollary 3 holds at its slot. The bound \(\beta\le1/3\) enters the common posterior bound at the zero order, the exclusion bound (Corollary A.1) and the zero-order part of the research bounds. The research parameter region and the slot-feasibility parts of identification range over the model's slots. Proposition 4 therefore joins the list, and the footnote is the text of `O2/O2_proof.tex`, lines 7 to 10 (fix 2.4; A-17).
4. **Proposition 4(d) (O3, O4).** The answers come from C.tex (d), O3 and O4:
   - "rises" is strict, and only up to the first strength at which research reaches its cap;
   - the path is compact, with continuous spread and threshold, \(\tau<1\) up to that strength, and a spread at the weakest incumbent below the cap spread;
   - \(\DT>2k\) is no separate hypothesis: a nonnegative exact margin gives \(J>k\), so \(\DT>2J>2k\) on the recruiting set, and beyond the cap the spread is at least the cap spread;
   - the end is \(\max\{r:\tau(r)\le M_{\lb}\}\), the last strength, and a plateau at \(M_{\lb}\) belongs to the set through its last point.
   T-5.2 defines the exact margin \(\varphi_a^*\), as (d) requires (fix 2.10).
5. **Tie rules in the summary sentences.** T-2.5 and the present `02:216–218` make the default tie rules the model's standing rule ("When ties arise ..."). A summary sentence without a tie phrase is read under them, so T-ABS and T-9.1 need no phrase for coexistence. Under the default rules each summary is exact (B.tex (a); C.tex (a), (b)). The mixing-investor phrase stays wherever research is summarized, because PLAN S4 names it.
6. **Proposition 4 under the other challenger rule.** There is no missing qualifier: T-5.3 states the default rules, and every conclusion holds under them. C.tex adds that the same recruiting outcome is available when an indifferent high-cost challenger may prepare with any probability and prepares fully after a purchase. The main text can carry that clause, as C's main-text form does, or leave it to the appendix.
7. **Research in the two-numbers passage.** The reduction lemma (A.tex `lem:reduction`) holds at every prior \(\pi\in(0,1)\). With research it makes the projected equilibrium sets, research included, coincide, with \(\Psi=\pi\max_qU_H(q)+(1-\pi)\max_qU_L(q)\). "The same research" therefore holds at every prior. It needs the research cost and the cap held fixed (fix 2.7), not the prior 1/2.
8. **The anchor of Proposition A.1 (research region).** Under decision 7 the research-region proposition prints as A.1. With strict margins it gives exactly the six-strength pattern of the full Corollary 3(b):
   - zero research alone at \(r_0\);
   - zero research and recruiting research with \(\lambda_E<\lambda_R<\lb\) at each intermediate strength;
   - full orders and research at the cap, uniquely, at \(r_1\) and \(r_2\).
   The prose writer's reading holds. The main-text Corollary 3 does not list the intermediate strengths, so T-5.9 names the pattern (fix 2.13).
9. **Labels.** The frozen labels are:
   - Corollary 1: `prop:region` for the full statement, with `cor:ccc-example` as its second label (A.tex);
   - Corollary 2: `cor:example-coexistence` (B.tex);
   - Corollary 3: `cor:research` for the full statement and `cor:research-short` for the main-text form (C.tex).
   The targets' `cor:region` and `cor:coexistence` differ, and D's label stub uses `cor:coexistence` (Part 5, item 1). `prop:spread` is the label of Proposition A.10, which carries the weighted test in part (ii) and the price-gap decomposition in part (iv).
10. **The highest strength of a uniform path.** No symbol is needed. The frozen main-text form says "the smallest \(r\)" and "the largest \(r\)", and T-4.9's "the lowest strength" and "the highest strength" match it.
11. **Ranked classes in the robustness paragraph.** Proposition A.6 (complementary signals, A.tex) holds for ranked finite-mean classes at prior one half. The signal sentence of `01:77–83` states no class restriction and needs no change. If it gains "for any ranked classes", the prior one half comes with it.
12. **Identification with an unknown prior.** Decision 5 leaves out only the unknown-prior local result, the identified set of W5 (D.tex, comment to Proposition A.11). Proposition A.11(c) carries the sale-price inversion with the counts, which identifies presence and the prior in closed form, and D's main-text form states it. T-8.5 can add "and with the mean order the sale impact identifies both the presence probability and the prior". Leaving it out is no error.
13. **The lowest strength in the entry-component trend.** The condition binds only at the weakest incumbent of the stretch compared. In A.10(vi)(b) the derivative of \(w_r(\mu)\) is \((\E_\mu[\min\{\theta,r\}^2]-3p^2)/(2r^2)\), and \(\min\{\theta,r\}\) rises with \(r\). Every stretch of a path is a path, so the frozen "lowest strength on the path" reads the same. "Considered" can read "compared".
14. **Ownership in the abstract and the opening claim.** A.tex "Value classes and priors" covers every ranked pair with a positive mean gap, every prior and every slot. It gives a nonempty set, defined by strict inequalities, on which the hypotheses and the ownership conclusion of Proposition 2 hold. Around the example, \(e_HW_H(F_1)>\rho W_H(F_0)\) is strict and continuous. T-ABS and T-1.1 match.
15. **Uniqueness in the example's research list.** The sentence holds under all four tie rules, so T-1.5 needs no qualifier.
    - At \(r_0\), under all four tie rules every positive-research equilibrium has \(U_H(1)>0\) (C.tex `lem:a5-buy`). But \(U_H(1)\le\Delta_0-k<0\) by (H2). Zero research then has strict abstention after a hypothetical success, because \(\rho\Delta_0<2k\).
    - At \(r_1\), \(r_U<r_1<r_C\). The example part of `rem:researchties` and Lemma `lem:a5-strong` give a unique equilibrium under all four tie rules at every strength above \(r_U\) other than \(r_C\).

## 5. Formal statements that look inconsistent with another

None of these is mathematical; each is a label or a word.

1. **Corollary labels.** The four places do not agree:
   - B.tex labels Corollary 2 `cor:example-coexistence`, while D.tex defines a stub `cor:coexistence` for the same corollary and cites it in its example (e) and (h);
   - the targets use `cor:coexistence`;
   - A.tex gives the full Corollary 1 `prop:region` and `cor:ccc-example`, D.tex cites `prop:region`, and the targets use `cor:region`.
   One label per corollary, fixed before S8, settles all four places.
2. **The order of the marked strengths.** D.tex's stub numbers `lem:a4-order` A.5, so D prints "Lemma A.5" in its example (a). A.tex numbers the two-numbers lemma `lem:twonumbers` A.5, and B.tex and C.tex cite it so. B.tex numbers `lem:a4-order` A.11.
3. **"The recruitment margin".** NOTATION (b) and (c) give the words "the recruitment margin" to \(\varphi_a=\DT(1-\tau)-k-2a\lambda_E\) and call \(\varphi_a^*\), which adds \((\rho J-k)^+\), "the exact margin". C.tex's main-text Proposition 4(d) speaks of "the exact recruitment margin" \(\varphi_a^*\). T-5.2 to T-5.7 give "the recruitment margin" to \(\varphi_a^*\), so one word names two objects. The main text needs only \(\varphi_a^*\). Either the targets write "the exact recruitment margin", or NOTATION records that the main-text words name \(\varphi_a^*\). In the example the two margins agree on \([r_0,r_{\lb}]\) (O4).
4. **Proposition 3(c), a choice for the coordinator.** B.tex's main-text Proposition 3(c) leaves out the start hypothesis "\(g_H>c_H\) against the weakest incumbent", and its comment says that the interval claim does not use it. T-4.9(c), T-1.4 and T-4.10 keep it, and both versions are true. Keeping it lets "the spread grows, in proportion, at least as fast as that excess shrinks" read correctly, because the proportional reading needs a positive excess. Dropping it matches the frozen form, against which the S9 fidelity read compares. Recommended: Proposition 3(c) as frozen ("the product of the spread and \(g_H-c_H\) does not fall with strength"). The introduction and the intuition keep the proportional words with the start hypothesis.

## 6. Language and numbers in the LaTeX targets

- **Language scan.** The scan of the LaTeX blocks of all 59 targets finds 8 hits, each judged:
  - "likely", four hits, is probability ("more likely than a low-class value to beat it", "a purchase becomes more likely");
  - "no longer", two hits, compares states ("orders no longer predict entry"), which rule 3 allows;
  - "interval of strengths", two hits in T-5.3(d) and T-5.4, rests on Proposition 4(d), whose qualifiers fix 2.10 supplies.
  The six "may mix" hits are the tie phrase. There is no status word. The only example naming is the label `sec:benchmark`, which does not print.
- **Vocabulary.** Apart from Part 5, item 3, every target uses the NOTATION words: "quiet market", "informative market", "the entry ceiling", "the entry floor", "floor-entry research", "the recruiting branch", "the informative branch", "mixed orders at the entry floor" and the tie phrases. "Another buyer" in T-1.1 lies in `01:7–11`, which NOTATION keeps. "Enter the region" in T-4.10 has the economy as its subject.
- **Numbers.** Every number prints through `\reg`:
  - every `\reg` key in the targets exists in the numbers table, and no decimal is typed;
  - the typed constants are the prior \(1/2\) and the constants of hypotheses and formulas (\(2k\), \(1/3\), \(3p^2\), and the halves of the closed forms), as the targets' conventions state;
  - every label the targets cite exists in the manuscript, except those the targets define (`sec:twonumbers` and the corollary labels).
- **Recomputed values.**
  - The share at \(r_1\), recomputed from \(e_H\), \(e_L\) and \(W_L(r_1)=1/3\) at the example's slot, is 0.830691 and agrees with `share_H_r1_B`.
  - At the recruiting research of Table 4, \(M_\lambda-\tau\) is 0.026344, 0.049472 and 0.069442 at the strengths 1.55, 1.60 and 1.65. T-5.6's "rises above the threshold by more" therefore holds at the three strengths. No formal statement states it, but Table 4's \(\lambda_E\) and research columns show it.
