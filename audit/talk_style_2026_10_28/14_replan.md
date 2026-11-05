# Replan, version 2 (28 October 2026)

Constraints from the author: at most 20 main frames (title and backups extra); 30–35 minutes of speech in a
45-minute slot; old motivation from the website; model block (current Beamer slides 3–7) unchanged; results in an
intuitive, business way; no "Lemma A.1, Lemma A.2" language on main slides.

## Main frames (20) — about 34 minutes

| # | Title | On the slide | Source | Min | Ends |
|---|---|---|---|---:|---:|
| T | Title | title, author | as now | 0.5 | 0.5 |
| **Motivation** | | | | | |
| 1 | Does a stronger bidder in a merger auction always deter others from entering? | three columns: sellers must find the second buyer; buyers pay before they know; prices move before bids move. Footline: Bulow and Klemperer (1996) | website S1, word for word | 2.0 | 2.5 |
| 2 | The received answer: a stronger rival pays less for your diligence | three bullets; "The logic holds when what the buyer knows stays fixed." Footline: Fishman; Hirshleifer and Png; auction entry | website S2, word for word | 1.5 | 4.0 |
| 3 | The stock price as an information source, inside a takeover sale | literature table, Edmans, Goldstein and Jiang (2015) bold | current slide 2 | 1.0 | 5.0 |
| 4 | This paper: strength can pay for the signal that brings the second buyer in | the large line (strength taxes profit and pays for information); preview: weak, strong, very strong; roadmap | website S4; "flat/live" → "uninformative/informative", "rival" → "first buyer", roadmap updated | 1.5 | 6.5 |
| **Model** (unchanged) | | | | | |
| 5 | Model: primitives | as now | current 3 | 1.5 | 8.0 |
| 6 | Trading and timing | as now | current 4 | 2.0 | 10.0 |
| 7 | Information and choices | as now | current 5 | 2.0 | 12.0 |
| 8 | Payoffs | as now | current 6 | 2.0 | 14.0 |
| 9 | Equilibrium with competitive prices | as now | current 7 | 1.5 | 15.5 |
| **Mechanism** | | | | | |
| 10 | Strength moves value from the second buyer to shareholders | box in words: at each belief, buyer profit B(μ) weakly falls; the shareholder spread Δ_T weakly rises; one identity (spread + profit gap = fixed class gap); number line with the first buyer's value moving right | current 8, rewritten | 2.0 | 17.5 |
| 11 | Every order leaves the informed investor an edge | belief band picture; three plain lines: a liquidity trader can copy every order, so the belief μ stays between m(π) and M(π); the gap to certainty is the investor's trading profit, so a wide spread pays for trade; the high cost pays only when μ reaches the threshold τ, so M(π) caps entry | current 9, rewritten | 1.5 | 19.0 |
| **Main result** | | | | | |
| 12 | A stronger first buyer can bring the second buyer in | box: three columns (informed orders, stock price, entry) for weak, strong, very strong; three conditions in words; unique outcomes, open set; button to exact (H1)–(H3) on B1 | current 10, rewritten | 2.5 | 21.5 |
| 13 | Why each outcome is unique: two bounds settle each economy | four-step strip in words (spread too thin to pay k; even at the floor a correct order pays k; a purchase lifts the belief to M ≥ τ; M < τ, entry back to the floor) | current 11, rewritten | 1.5 | 23.0 |
| 14 | In the example, against the strong first buyer only a purchase clears the bar | beliefs figure; rounded numbers; inputs in one small line | current 12, rewritten | 2.0 | 25.0 |
| 15 | Freeze the news, and strength cannot raise entry | three entry rows; "The second buyer still reads the stock price; only what the price can say is frozen." | current 13, rewritten | 2.0 | 27.0 |
| **Extensions** | | | | | |
| 16 | Informative and uninformative markets can share one strength | Proposition 3 in words; coexistence figure; scope in one small line | 45-minute S19–S20, rewritten | 1.5 | 28.5 |
| 17 | A wider spread pays for more research, and research brings entry | Proposition 4 in words; small research figure; prior 1/2 | current 14, rewritten | 1.5 | 30.0 |
| **So what** | | | | | |
| 18 | Let the second buyer see the price, and shareholders gain | price access at the strong first buyer raises target proceeds and surplus net of preparation costs (under Proposition 2's conditions); sale terms set the payment to win and what the price can reveal | 45-minute S24, rewritten | 1.5 | 31.5 |
| 19 | Recruitment shows up in the purchase impact | price diagram; two predictions; measurement line | current 15, rewritten | 1.5 | 33.0 |
| 20 | Competition can create competition | the one idea; three implications | current 16 | 1.0 | 34.0 |

Cut order if questions run long: 16 → one sentence; 18 → one sentence; 13 → one line on 12; 14 → readouts only.
Never cut 1, 2, 4, 5–12, 15, 20.

## Rules for slides 10–20

- Business-intuitive claim titles. Statements in plain words, with a few glossed symbols that link to the model
  block (the shareholder spread Δ_T, buyer profit B(μ), the belief μ, the top belief M(π), the threshold τ, the entry
  floor ρ, the order cost k).
- At most one displayed formula per slide, only where the speech uses it.
- Main-text labels (Proposition 1–4, Corollary 1) only as a small tag in the box title. No appendix labels
  (Lemma A.1–A.3, Proposition A.2, A.10, A.12) on main faces.
- Scope that changes meaning stays, in words: conditions hold together on an open set; the reversal is conditional;
  research at prior 1/2; full two-sided trade for the winner prediction; the welfare gain is the price-access
  comparison at the strong first buyer.

## Backups

B1–B15 as now (B3 coexistence and B5 sale terms keep the exact statements). New B16 "Posterior and trading bounds
in full": the formal content of current slides 9 and 11, with the paper's lemma labels.

## Work order

1. Slide text: Muse Wonder Full writes slides 4 and 10–20 and B16; slides 1–2 copied word for word from the website
   text; slides 3 and 5–9 copied from the current `slides.tex`.
2. In parallel: GPT-6.1 Sol updates the script (whole talk, longer motivation); GPT-6 Astra checks slides 4 and 10–20
   against the paper; Claude Opus rebuilds the handout.
3. Lead session: apply the check, compile, view every page, push to Overleaf. Rollback: 28e690d.

## Variant: at most 17 main frames (about 30 minutes)

Condense three frames; nothing leaves the deck, it moves to speech or a backup.

| Cut | Where it goes | Spoken line kept | Saves |
|---|---|---|---:|
| 13 Why each outcome is unique | backup B16 (with the formal bounds); button from slide 12 | on slide 12: "The bounds on the last slide settle each column for every order plan, so each outcome is the only one." | 1.5 |
| 16 Informative and uninformative markets share one strength | backup B3 (Proposition 3 in full) | on slide 17: "Between the weak and the strong first buyer, both kinds of market can exist at one strength; the backup has the region." | 1.5 |
| 18 Let the second buyer see the price | the "Sellers" line of the conclusion; backup B5 in full | on slide 20: the price-access result in one sentence | 1.5 |

Order with 17 frames: T · 1 motivation question · 2 received answer · 3 literature · 4 this paper · 5–9 model ·
10 Proposition 1 · 11 posterior bounds · 12 Proposition 2 · 14 example · 15 control · 17 research · 19 tests ·
20 conclusion. Time about 29.5 minutes; 1 minute of the saving can go to slides 1 and 12.
