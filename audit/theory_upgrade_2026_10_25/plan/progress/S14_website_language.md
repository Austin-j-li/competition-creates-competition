# S14 website language

The prose writer made 18 sentence revisions across the six fragments. The meaning, hypotheses, qualifiers, mathematical content, HTML structure, element attributes and numerical placeholders stay unchanged.

## 01 — Setting: 5 revisions

1. Before: “Its strength is public: \(R\) has a continuous distribution \(F\), and a first-order stochastic shift of \(F\) strengthens the incumbent. Public strength is a distribution, not a bid.”
   After: “Its strength is the public distribution \(F\) of \(R\), and a first-order stochastic shift of \(F\) strengthens the incumbent.”
   Rule: state the positive claim and remove the contrast formula.

2. Before: “An outside specialist investor knows the challenger's class, though not its value.”
   After: “An outside specialist investor knows the challenger's class and remains uncertain about its value.”
   Rule: use a direct statement with a concrete subject.

3. Before: “Only the order is public, not who placed it.”
   After: “The order is public; the identity of its trader remains hidden.”
   Rule: replace the contrast formula with two positive facts.

4. Before: “A deviation by the investor is evaluated at the candidate's prices and entry.”
   After: “A deviation by the investor takes the candidate's prices and entry as given.”
   Rule: prefer the active voice and plain economic words.

5. Before: “The numbers and figures come from an example. Its two classes are point masses, the high class at \(h\) and the low class at \(\ell\), so class and value coincide.”
   After: “The example has two point-mass classes, the high class at \(h\) and the low class at \(\ell\), so class and value coincide.”
   Rule: remove filler and begin with the economic object.

## 02 — Mechanism: 3 revisions

1. Before: “Let \(g_H,g_L\) denote expected acquisition profit before the preparation cost, and let \(t_H,t_L\) denote expected target proceeds with preparation.”
   After: “The symbols \(g_H\) and \(g_L\) denote expected acquisition profit before the preparation cost, and \(t_H\) and \(t_L\) denote expected target proceeds with preparation.”
   Rule: replace the expository command with a direct definition.

2. Before: “The rest stays in challenger profit.”
   After: “The remainder stays as challenger profit.”
   Rule: use plain economic wording.

3. Before: “A stronger incumbent never raises the probability that a prepared challenger wins, so for every pair of classes it weakly reduces both \(g_H\) and \(g_L\), and with them gross profit at every belief.”
   After: “A stronger incumbent never raises the probability that a prepared challenger wins. For every pair of classes, it therefore weakly reduces both \(g_H\) and \(g_L\), and gross profit falls weakly at every belief.”
   Rule: give each claim its own sentence and preserve both weak comparisons.

## 03 — Main result: 1 revision

1. Before: “A stronger incumbent can induce the information that brings a second bidder into the sale.”
   After: “A stronger incumbent can attract a second bidder by making the price more informative.”
   Rule: use a concrete subject, an active verb and the paper's own statement of the mechanism.

## 04 — Coexistence and research: 3 revisions

1. Before: “The informed purchase rate is the probability of an informed purchase conditional on class \(H\). Divide it by \(\lambda\) to obtain the purchase probability conditional on investor presence.”
   After: “The informed purchase rate is the probability of an informed purchase conditional on class \(H\); dividing it by \(\lambda\) gives the purchase probability conditional on investor presence.”
   Rule: join the definition to its consequence and remove the expository command.

2. Before: “At fixed prices and entry, the best research choice equals expected net trading profit after a success divided by \(a\), capped at \(\bar\lambda\), so research never has a tie.”
   After: “At fixed prices and entry, the best research choice is unique: it equals expected net trading profit after a success divided by \(a\), capped at \(\bar\lambda\).”
   Rule: state uniqueness directly and simplify the sentence.

3. Before: “It is the only equilibrium on \([r_Q,r_C]\), and floor-entry research at the cap takes over above \(r_C\).”
   After: “It is the only equilibrium on \([r_Q,r_C]\), and floor-entry research at the cap is the equilibrium above \(r_C\).”
   Rule: replace informal wording with a plain equilibrium statement.

## 05 — Extensions: 2 revisions

1. Before: “A price can add useful information even when the challenger has a more accurate private signal than the investor.”
   After: “A price can add information even when the challenger has a more accurate private signal than the investor.”
   Rule: remove vague praise and retain the accuracy qualifier.

2. Before: “A deterministic external dividend of [[p2_access_proceeds_gain]] in the hidden-price economy equalizes the mean prices and leaves the orders and entry unchanged, so the information in the price, not its level, separates the two economies.”
   After: “A deterministic external dividend of [[p2_access_proceeds_gain]] in the hidden-price economy equalizes the mean prices and leaves the orders and entry unchanged, so the price's information content distinguishes the two economies.”
   Rule: replace the contrast formula with the positive identification claim.

## 06 — Empirical implications: 4 revisions

1. Before: “Each prediction concerns one target in one public state and names the conditions it needs.”
   After: “Each applies to one target in one public state and states its conditions.”
   Rule: remove repetition and use direct wording.

2. Before: “The weighted difference equals the expected price before the order opportunity minus the price after no order, so the test needs prices and order frequencies and no auction object.”
   After: “The weighted difference equals the expected price before the order opportunity minus the price after no order, so the test uses only prices and order frequencies.”
   Rule: state the data requirement positively and concisely.

3. Before: “Under full two-sided trade, a prepared challenger wins more often after a purchase than after a sale exactly when the incumbent's value falls, with positive probability, where a high-class value beats it with a higher probability than a low-class value.”
   After: “Under full two-sided trade, a prepared challenger wins more often after a purchase than after a sale exactly when there is a positive-probability region in which a high-class value beats the incumbent with a higher probability than a low-class value.”
   Rule: simplify the syntax while preserving the exact-positive-probability condition and both class comparisons.

4. Before: “Because a liquidity order can match the investor's direction, the investor keeps an advantage after every order, and a wider spread can make that advantage worth the trading cost. The price then recruits a challenger that a weaker incumbent could not attract.”
   After: “Because a liquidity order can match the investor's direction, the investor keeps an advantage after every order. A wider spread can make that advantage worth the trading cost, so the price recruits a challenger that a weaker incumbent could not attract.”
   Rule: remove the one-line closer and carry the causal chain in one sentence.

## Build and inspection

- Website build: PASS. All six fragments passed their structural and mathematical checks; the page contains no unresolved numerical placeholder. The paper has 150 pages and the comparison note has 7 pages.
- Display inspection: PASS. The paper tab carries both page counts, both hashes and the text date. All 180 number spans and 53 numbers in formulas match their declared displays, no decimal is typed into the prose, and the page uses only the locked local faces with no network request.
- Diff inspection: PASS. Only prose changed in the six fragments; no markup, formula or numerical placeholder changed.

## Language review

The review covered all six fragments and produced nine ordinary hits and six allowed tie-rule hits. Each hit has the following judgment.

| Fragment and line | Hit | Judgment |
|---|---|---|
| 01:7 | “illustrative” | The label describes the hypothetical sale process. It does not hedge a result. |
| 01:8 | “check” | Checking contracts is a diligence task in the economic setting. |
| 01:42 | “may” | The investor may mix and may place a wrong-signed order. Both permissions belong to the model. |
| 01:42 | “may mix”, first allowed hit | This is the investor's strategy permission. |
| 01:42 | “may mix”, second allowed hit | This is the default tie rule. |
| 01:42 | “may prepare with any probability” | This is an alternative tie rule. |
| 01:43 | Retired example term in an id | The attribute is invisible and had to remain unchanged. The visible heading says “The example”. |
| 03:30 | Retired example term in an id | The attribute is invisible and had to remain unchanged. The visible heading says “The example”. |
| 03:58 | Retired example term in an id | The attribute is invisible and had to remain unchanged. |
| 04:6 | “may mix” | This is the default tie rule. |
| 04:56 | “may prepare with any probability” | This is an alternative tie rule. |
| 04:66 | “interval of strengths” | This is the exact interval claim in the research result. |
| 04:69 | “may mix” | This is the default tie rule in the figure caption. |
| 06:18 | “no longer” | This compares entry above the entry ceiling with entry below it, a permitted comparative static. |
| 06:27 | “could” | This states the weaker incumbent's counterfactual inability to recruit the challenger. It does not express uncertainty about the result. |
