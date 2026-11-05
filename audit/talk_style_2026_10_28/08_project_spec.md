# Project spec — 30-minute talk rebuild (for the author's approval, 28 October 2026)

## 1. Goal

Rebuild the talk as a 30-minute theory talk for a 45-minute slot (15 minutes for questions). Update the Overleaf
Beamer deck (Madrid) and the website deck (existing ruled design language) with identical words, frames and numbers.
No change to the paper in this project.

Inputs: `06_outline_30min.md` (slide plan), `07_wider_audience_words.md` (wider-audience words), this spec.

## 2. The informed investor: one running example

Option A (recommended): a biotech sale, used as the one story of the talk (Quint: one real-world story).
Option B: the informed investor alone is a long-short biotech fund; the rest of the talk stays generic.
The story is an illustration. Drug-company deals are often negotiated; the cash second-price auction is the model's
sale rule.

| Model object | In the story |
|---|---|
| Target | A listed biotech company with one late-stage drug, up for sale |
| First buyer | A large drug company that has done its diligence |
| Second buyer | A second drug company deciding whether to open the data room |
| Informed investor | A long-short biotech fund. Which drug companies have gaps in their portfolios is public; how well this drug works in practice is the fund's own research (published data, doctor surveys). Together they tell the fund whether the second buyer is a good fit. Speech: it holds no stake before it trades and trades on its own research |
| Liquidity trader | Index and fund flows that trade the stock for their own reasons |
| Good fit / poor fit | The drug fills a gap in the second buyer's portfolio / it overlaps with drugs the second buyer already sells |
| Diligence bill | Months of scientific, clinical and regulatory review |

Why the fund knows something the second buyer does not: it combines a public fact (portfolio gaps) with its own
research on the drug; the second buyer learns about the drug only after it opens the data room. It knows different
facts, not more facts. Paper basis: §2.3 ("its own research on the
target's customers, technology, and demand"); §6 ("investors who follow the target know its customers or its
product market").

Alternative: an enterprise-software target; the informed investor is a technology fund whose channel checks show
whether the target's customers also buy from the second buyer.

Rules for the example: no real fund or company names; no numbers; words only until slide 12.

## 3. Names and notation (locked)

- first buyer, second buyer, informed investor, liquidity trader, market makers, seller
- good fit, poor fit; diligence bill; prepare (action), entry (its chance); stock price; informative, uninformative;
  shareholder spread; buyer profit; belief, top belief, threshold
- Never on any slide, backup or note: incumbent, challenger, fund (alone), specialist investor, live/flat price
- Main-slide symbols: F, π, k, μ, Δ_T, m and M, τ; λ only on slide 14, with a reminder

## 4. Slides (30.0 minutes)

| # | Min | Ends | Title (draft) | Content |
|---|---:|---:|---|---|
| T | 0.5 | 0.5 | Title | Title, author |
| 1 | 2.0 | 2.5 | Does a stronger first buyer always keep the second buyer out? | Received answer at fixed information (Fishman 1988). "The second buyer always reads the stock price. What changes is what the price says." Answer in words. Speech: the biotech story, 20 seconds |
| 2 | 1.0 | 3.5 | The stock price as an information source, inside a takeover sale | Three rows; Edmans, Goldstein and Jiang (2015) bold as anchor; one bold line. Speech: one line per audience; name Fishman and EGJ |
| 3 | 1.5 | 5.0 | Setting: the sale is public, and the stock still trades | Three-box window; the story in one line |
| 4 | 2.0 | 7.0 | Players and timing: one trade happens before the diligence decision | Six players with one-line identities (informed investor = biotech specialist fund); five-step timeline |
| 5 | 2.0 | 9.0 | Information and actions: who knows what, who chooses what | Knows / chooses table; good fit and poor fit in story words; no one sees who traded |
| 6 | 2.0 | 11.0 | Payoffs: one value, two pockets | Target proceeds + buyer profit = value, averaged over the first buyer's value; number line; Δ_T; buyer profit at μ |
| 7 | 1.5 | 12.5 | Equilibrium: best orders, fair prices, Bayes beliefs, diligence that pays | Four lines in words; every order on path |
| 8 | 2.5 | 15.0 | Proposition 1: strength moves value from the second buyer to shareholders | Theorem box; number line with the first buyer's value moving right |
| 9 | 2.0 | 17.0 | Every order leaves the informed investor an edge | Band m(π) ≤ μ ≤ M(π); three uses; band picture |
| 10 | 2.5 | 19.5 | Proposition 2: a stronger first buyer can bring the second buyer in | Three-column box; conditions in words; link to exact conditions |
| 11 | 1.5 | 21.0 | Why each outcome is unique: two bounds settle each economy | Trading bound in words; four-step proof strip |
| 12 | 2.0 | 23.0 | In the example, only a purchase clears the bar | Beliefs figure; rounded readouts; entry 0.25 → 0.52 → 0.25 |
| 13 | 2.0 | 25.0 | Freeze the news, and strength only deters | Control box; three entry rows; "The second buyer still reads the price here. Only what the price can say is frozen." |
| 14 | 2.0 | 27.0 | Extension: when research is costly, strength buys more of it | Setup line; theorem box; small figure; speech links back to who the informed investor is |
| 15 | 1.5 | 28.5 | A recruiting purchase moves the price more than a sale | Three price levels; two predictions; measurement line |
| 16 | 1.5 | 30.0 | Competition can create competition | The one idea; three short implications (evidence, sellers, markets). Spoken last line: "Stock markets help decide who contests a sale." |

Backups, in order: B1 exact Proposition 2 conditions (linked from slide 10, with a return link); B2 who the informed
investor is (legality, evidence after disclosure) — new; B3 coexistence (Proposition 3); B4 scope; B5 price access and
sale terms; B6 order slot in full; B7 payoffs and Proposition 1 in full; B8 equilibrium in full; B9 example inputs and
region; B10 outcome tables and controls in full; B11 research in full; B12 references with the full literature
table; B13 continuous order sizes; B14 predictions in full. Existing backups are reused with the name lock applied.

Cut order if questions run long: 14 → one sentence; 12 → readouts; 15 → takeaway; 11 → one sentence on 10.
Never cut 3–10, 13, 16.

## 5. Writing rules (for the wording draft)

- Slide face about 50 words; speaker notes 120–170 words per slide, complete speech.
- One claim per slide. Results: claim titles. Model slides: "Step: claim".
- No first person on faces; no status labels; no example numbers before slide 12; one metaphor (two pockets).
- Titles must state what a result does, not what it cannot do.
- Conditions in words on faces; exact forms on backups. Scope conditions that matter stay on the face in words.
- Example numbers rounded to two or three decimals on faces; full precision on backups.
- Guardrails: the reversal is conditional; welfare = price-access comparison only; no claim that a public process or
  more disclosure is optimal.
- Correction carried in: payoffs are expectations over the first buyer's value (old slide 8 error).

## 6. Design rules

Beamer (Overleaf): classic Madrid via `ccc-classic.sty`; never the ruled look. Model strip under the frame title
(Players · Timing · Information · Actions · Payoffs · Equilibrium, current step bold). Results in Madrid theorem
blocks. One point per click (overlays). No subtitles, takeaways or footlines on main faces; Madrid's own footline and
slide numbers stay. Backups after `\appendix`.

Website: the existing ruled design (`presentation/DESIGN.md`); never a Beamer theme. Same frames, words, numbers
and click builds. Model strip and theorem box drawn in the ruled language. Speaker notes in `notes.md`, never staged.

New exhibits (both decks): model strip; five-step timeline; knows/chooses table; two-pockets number line (static on
6, moving on 8); belief band with τ mark; three-column Proposition 2 table; proof strip; three-level price diagram.
Reused: decision window (F1), beliefs figure (F8), controls rows (F11), research figure (F13).

## 7. Team and gates

| Step | Who | Output |
|---|---|---|
| 1 Wording | Muse Wonder Full | `presentation/SLIDEPACK_30_VERBATIM.md` in the main worktree: On the slide / Say / Exhibit, for all main slides and the two new backups |
| 2 Paper check (added by the lead; optional) | GPT-6 Astra | Every statement checked against the paper; fixes listed |
| **Gate A** | Author | Exact slide text approved in chat |
| 3a Website deck | Claude Opus (account 1) | `presentation/` content and exhibits; the existing build gate `check_deck.mjs` gets two new constants: total 45 → 30 minutes, first example number slide 16 → 12 |
| 3b Beamer deck | Claude Sonnet (account 2) | `slides.tex` (Overleaf working copy and `slot/manuscript/` mirror), new TikZ exhibits |
| 4 Integration and QA | Lead session | Parity of words and numbers; compile; view every page and every web slide |
| **Gate B** (author's choice) | Author | Look at the compiled PDF and web preview before publishing, or let the lead publish after QA |
| 5 Publish | Lead session | Pull, then push Overleaf; deploy the website with `handout/publish.py` |

Work happens on local `main` in `/home/uctpiaj/work/tmp/ccc-main-slidepack`. Before any change: tag
`talk-45min-2026-10-28`. Rollback points: Overleaf 783591e, Cloudflare version 7aa798bd. Publishing needs a
Cloudflare token on Condenser, requested through a secret prompt at that step. No GitHub push unless asked.
No tests are written or run. The existing build gates (`check_deck.mjs`, the LaTeX compile) run as part of the
build; verification is by viewing every slide in the PDF and the browser. The new pack carries no model or tool
names, so it can be committed.
