# Wording pass — main deck discussion

Date: 9 November 2026.
Scope: main frames S1–S19 on the website deck.
Backups B1–B17: survey only.
Method: six readers in parallel, plus a full read by the coordinator.
Status: discussion only. No slide file has changed.

Master files:

- `slot/manuscript/slides.tex` — the deck.
- `presentation/content.js` — the website copy.
- `slot/manuscript/slides_script.md` — the speaker script.

## Top finding

The deck is correct. It is not cold-readable.

A seminar listener hears the script repair each gap.
A website reader reads the slide alone, and gets no repair.
Most faults below exist only for that cold reader.

One fact controls all edits: `slides.tex` and `content.js`
match word for word on S1–S19 today.
Each wording fix must go into both files, in the same pass.
Edit `slides.tex` first, then `content.js`.
If a title changes, the script heading changes too.

## Four faults explain almost everything

### 1. Terms arrive before their definitions

Examples, in order of harm:

- S4 uses “shareholder spread” as the engine of the paper.
  Its definition sits on S8. The script glosses it at frame 4.
  The slide does not.
- S2 and S4 say “at a fixed belief” / “at each belief”.
  Belief about what? The synergy class enters on S5.
- S1 says “preparation” with no content.
  The script says “months of diligence”.
- S12 says “a fixed share”. No frame names that share.
  The share is `ρ κ(π)`.
- S14 says `u = e − 1`. The name “mass ratio” sits only in B10.
- S15 says “the signal S”. The main model gives the rival a price.
  No sentence maps `S` to “the news in the price”.
- S16 says “research rises”. What rises is a success chance.
  Precision does not rise. Learning stays all-or-nothing.
- S17 says “At F1”. The map F1 = strong sits on S5 and S13.
- S18 says `e(1) > ρ`. No sentence on the frame calls that recruitment.

Rule for the pass: at first use on a frame, give the object
its words once, even if an earlier frame defined it.
Result frames stand alone on the website. Readers land mid-deck.

### 2. One object carries several names

| Object | Use this form | Forms to retire |
|---|---|---|
| `B(μ)`, `g_j` | rival gross profit | rival profit; rival's profit; expected auction profit; gross auction profit (figure); acquisition profit (brief) |
| `V_T`, proceeds | target proceeds | sale proceeds; expected proceeds (bare); gains for sellers |
| Fixed-info control | pre-preparation information (noun); fixed-information (modifier) | what the rival can learn / knows; information control; fixed information (bare, except in the tag) |
| `Δ_T` | shareholder spread | the spread (in titles, before definition); target-payoff spread (brief) |
| Beliefs | order belief `μ(x)`; price belief `μ̄`; top belief `M`; band floor `m` | the belief; posterior (brief); top/bottom posterior (brief) |
| `τ` | preparation threshold (first use per frame), then threshold | threshold with no first-use gloss |
| Strength steps | weak / strong / very strong | stronger still; strength (bare, in titles) |
| Orders | stock purchase / stock sale; outcome `X = q` | buy order; sale order as a noun where the deck says purchase |

The word “gross” is load-bearing. Without it, “profit” reads
as profit net of the preparation cost. That reading breaks S2 and S4.

### 3. Titles drop the qualifier that makes them true

Five titles state a strict or bare claim. Their bodies state a
weak or weighted claim:

- S10: “lowers … widens” for `≤` and `≥`. Drops “gross” and “shareholder”.
- S11: “the price reveals the belief”. Needs `Δ_T > 0`, `g_H > g_L`,
  competitive prices, truthful bids. “The belief” has no referent.
- S12: “earns between a fixed share and all of the spread”.
  “Earns” overreads a weak gross bound that allows zero at `Δ_T = 0`.
- S14: “lies exactly between”. Reads as “at the midpoint”. False.
  The gaps are 0.026059 below and 0.000334 above.
- S18: “Purchase impact reveals recruitment”.
  Raw purchase impact reveals nothing. The result needs the
  frequency-weighted gap against sale-order impact.
  Raw impacts compare only at `π = 1/2`.

Rule for result titles S10–S18: one finite claim, present tense,
one result only. Keep “weakly / can / exactly when” in the title
or move the claim into a subtitle. Do not shrink a title by
deleting its truth condition.

### 4. Three frames describe a construction, not a conclusion

S14, S15, S16 — your three frames — share one structure fault.
Each frame states conditions and stops. The reader must supply
the last step. Detail follows in the next section.

## Frames 14, 15, 16 in depth

### S14 — Corollary 1. Current title: “Example: the top belief lies exactly between two thresholds”

What the frame must land, in one sentence:
concrete numbers satisfy (H1)–(H3), so Proposition 2 is not empty.

Can a cold reader state that after 20 seconds? No.
The frame never says it. It ends at `M(1/2) ≃ 0.731…`.

Blockers, in order:

1. No conclusion sentence. The reader must check
   `0.705 < 0.731059 < 0.731392`, infer (H1)–(H3), then infer
   Proposition 2. None of that chain is on the frame.
2. “Two thresholds” hides one function at two strengths.
   `τ` is one belief where `B(τ) = c_H` (S11).
   The two numbers are `τ(r1)` and `τ(r2)`.
   `τ` moves because `g_H, g_L` move with `r`. S14 never says so.
3. “Top belief” is a band bound, not a posterior name.
   It equals the purchase belief only under full orders (S13 table).
   S14 says “after a purchase” with no qualifier.
4. `u` has no words on the frame, and two forms:
   `u = λ/b` (S11) and `u = λ/[(1−λ)β]` (S14 foot).
5. Fractions block the one check the reader must do.
   No one compares `4245/5804` with `0.731059` by eye.
   Decimal keys exist in `numbers.tex`. Use them in the statement.
   Keep fractions in the foot or in B10.
6. `r0` is listed, then never used. The equivalence uses `r1, r2` only.
7. The figure label “band for M(1/2)” reads as an error band.
   The shaded set is the interval `(τ(r1), τ(r2))` itself.
8. S14 is the first frame with registry numbers
   (“No registry number before frame 14”, header).
   It must teach the reader to read numbers: per share,
   probabilities of class H, decimals first. It does not yet.

Recommended title:
“The example works: a purchase recruits only against the strong incumbent”

Paste-ready core changes (numbers and keys unchanged):

- “Each class has one sure value per share: θ = h in class H
  (good synergy) and θ = ℓ in class L (poor synergy), with
  (h, ℓ, p) = (…) for the reserve p.”
- “Here τ(r) is the frame 11 preparation threshold at strength r:
  the belief in class H where rival gross profit equals c_H.
  Numerically, τ(r1) = 0.705 and τ(r2) ≈ 0.731392.”
- Add after the display: “All three numbers are probabilities
  that the class is H. Both inequalities are strict, so small
  input changes keep them (B10).”
- Close the statement with: “Recall the mass ratio u = λ/b from
  frame 11. The example sets u = e − 1, so the belief after a
  purchase under full orders is M(1/2) = e/(1+e) ≃ 0.731059,
  and τ(r1) < M(1/2) < τ(r2) holds. Hence (H1)–(H3) hold at
  these numbers, and Proposition 2 applies: entry is ρ, then
  above ρ, then ρ again.”

Author checks before this text is final: CHECK 1 and CHECK 2 below.

### S15 — Fixed information. Current title: “With fixed information, strength cannot raise entry”

What the frame must land: if the rival's news cannot change
when the incumbent strengthens, entry can only fall or stay flat.

The title lands. The statement does not, for a cold reader.

Blockers:

1. `S` is unmapped. In the model the rival sees price `P`, not `S`.
   Add one sentence: “Let S be any signal the rival sees before
   it prepares; in the main model, read S as the news in the
   stock price.” B11 already says “The rival still reads the
   stock price P here”. That sentence belongs on S15.
2. “Fixed” has four objects. One object moves.
   Fixed: joint law of `(j, S)`, class laws `G_j`, reserve, cost law.
   Moved: only `F`. Say so: “Only the incumbent's value law moves.”
   Without that line, “fixed” can read as “the realised signal is fixed”.
3. `F1 ≤ F0` needs its words on this frame:
   “economy 1 has the stronger incumbent”.
   `F0, F1` here are any pair. On S13 they are the paper's steps.
   Say “any two strengths”, or the theorem and table row 1 collide.
4. Status is unclear. The tag says “Fixed information”.
   B11 states the same result as Proposition A.2, with the exact
   fall `E0 − E1 = Pr{B1(μ(S)) < C ≤ B0(μ(S))}`.
   Decide CHECK 3: promote the A.2 tag (and the exact fall?) to S15.
5. The table reads as a counterexample. Row 2 is flat:
   “Above floor / Above floor”. Flat fits “cannot rise”.
   The frame never says so. Add: “Rows 2 and 3 are flat.
   Flat is what ‘cannot rise’ allows.”
6. “Full informed orders” has no words on the frame.
   Write “buy in H, sell in L” at each use.
   Row 1 changes orders from `(0,0)` to `(1,−1)` as strength rises.
   That change breaks the fixed-information hypothesis.
   Draw that line on the frame. It is the point of the control.
7. Row 3, “Stock price hidden”, needs its complement:
   “(prior π only)”. The script says it. The slide does not.
8. The intuition restates Proposition 1(a) without naming it.
   Write: “This is Proposition 1(a) belief by belief: at each
   unchanged belief, the stronger incumbent gives weakly lower
   rival gross profit, so strength can only remove reasons
   to prepare, never add one.”

Recommended title and tag (title plain, tag technical —
this keeps one canonical noun and one cold-readable title):

- Title: “If the rival's news cannot change, strength cannot raise entry”
- Tag: “Fixed pre-preparation information”
- Subtitle option: “The control: freeze what the rival can learn”

Note the S2 collision: S2 title (“The received answer: strength
cannot raise entry”) and S15 state the same claim in a title skim.
The subtitle above marks S15 as the control and proof.
Keep S2 as the received view. Do not use the same noun system
in both places: S2 takeaway and S4 bullet 3 should both read
“pre-preparation information”, to match S15.

### S16 — Proposition 4. Current title: “Costly research rises with the spread, up to the cap”

What the frame must land: the trader can pay to raise its
chance to learn the synergy class. A wider shareholder spread
raises that chance, until the cap `λ̄` binds.

A cold reader cannot state that today. Four words blur into one
symbol: research, presence, success, cap — all are `λ`.

Blockers:

1. “Research” never says what rises. On S6, `λ` is an exogenous
   presence chance. On S16 it is a chosen success chance.
   State all-or-nothing learning in the lead-in:
   “With probability λ it succeeds, learns the class in full,
   and fills the slot. With probability 1−λ it fails, learns
   nothing, and liquidity fills the slot.”
   Else “research rises” reads as “estimates get precise”.
2. “The cap” enters in the title, before any definition.
   `λ̄` has no words, no value, no reason on the frame.
   Write “research cap λ̄, the highest success chance it can buy”
   in the lead-in. Optional bridge: at the cap, the research
   economy returns to the Proposition 2 economy (B12).
3. “Privately chooses … use its equilibrium level” reads as a
   contradiction. Add: “No one observes the chosen λ or success.
   Prices and preparation use the equilibrium level λ̂.”
   Confirm CHECK 5 first.
4. “Success” is used (“buys after success”) before definition.
   Define it in the lead-in, as in item 1.
5. The class-L action is missing. S16 defines the H action only.
   B12 suggests “abstains on poor synergy” in the example.
   Supply the general clause. See CHECK 6.
6. `β` first appears inside the entry display.
   The sign of “entry rises” turns on `1/2 − β > 0`.
   Restate “liquidity chance β ≤ 1/3 as on frame 6” on S16.
7. `Δ_T > 2k` (twice) has no link to S12, where the test is `K_j > k`.
   A factor 2 with no gloss reads as an error.
   Supply the route. See CHECK 4.
8. “Rises strictly with Δ_T” states no hold-fixed set.
   Across strengths, `τ` and `g_j` move too, and existence needs
   `τ ≤ M_λ̂`, which fails at high strength.
   Do not let the sentence be heard as “research rises with
   incumbent strength for all r”. Supply the clause. See CHECK 7.
9. The foot line “Fixed-research coexistence: B3” collides with
   “fixed information” on S15, two unlike controls in like words.
   Replace with: “When λ stays exogenous as on frame 6,
   informative and uninformative markets can coexist: B3.”

Recommended title:
“A wider spread raises the chance the trader learns the class, up to λ̄”

Short form, if length binds:
“A wider shareholder spread raises research success, up to the cap”
with the lead-in naming “research cap λ̄” in its first two lines.

## Frame map S1–S19

Verdict key: **Fix now** = a cold reader can misread the claim.
**Polish** = clear claim, rough words. **Keep** = sound.

| Frame | Verdict | Main fault | First fix |
|---|---|---|---|
| S1 Question | Polish | Roles undefined until S5; “sale proceeds”; “cost may pay”; target unnamed | Subtitle: “The incumbent is prepared. The rival must pay to prepare.” Use “target proceeds”; “covers its cost” |
| S2 Received answer | Polish | “at a fixed belief” (object missing); “costs fail to pay”; two names for fixed information | “at each belief about synergy”; one noun: pre-preparation information |
| S3 Where paper sits | Polish | “Price news can rise” (category error); “synergy news” (whose?); verbless difference cell | “The price can carry more news…”; “news about the rival's synergy” |
| S4 This paper | Fix now | Shareholder spread undefined here (High); profit without “gross”; “very strong” unnamed; floor undefined | Gloss spread in the large line: “the good-minus-poor synergy gap in target proceeds”. Name all three strengths |
| S5 Players | Polish | `F`, `r̄`, CDF direction wordless; rival may read as knowing own class; independence list ambiguous | “draws weakly higher values”; “the rival does not know its class before preparation” |
| S6 Timing | Polish | `q` vs `X` never bridged; step 5 hides incumbent bid. Note: upstream already reworks S6 — pull first | One line: “One trader submits one unit order q; the realised outcome is X = q” |
| S7 Information | Polish | “an observer” is no player; `μ̄(P̄)` bars wordless; “public primitives” vague | Order belief = market makers' belief; “for a seen price P̄” |
| S8 Payoffs | Fix now | Figure case `p < R < θ` invisible; realised vs expected money unmarked; `B(price belief)` puts English inside `B(·)`; no incumbent or loser payoff | Caption “One draw with p < R < θ”; mark “for one R / expected”; write `B(μ̄(P̄)) − C`; add loser/incumbent line |
| S9 Equilibrium | Fix now | No fixed-point sentence; Orders row overloads four jobs; `B(μ̄)` drops argument; `maximize` (US) vs `realised` (UK) | Lead: “Orders, prices, beliefs, preparation must fit the same P(·), e(·)” |
| S10 Prop. 1 | Fix now | Title strict for weak; drops gross/shareholder; intuition names level, identity moves the gap `g_H − g_L` | Title with “can shift… toward shareholders” or full weakly-form + subtitle. Intuition: “part of the between-class gap in rival gross profit” |
| S11 Belief bounds | Fix now | Two results, two scopes, one title; preparation written in `μ(x)` the rival never sees; `b, u` wordless | Title: “Beliefs stay in the [m, M] band; prices reveal the order belief”. Add bridge: “Because the price reveals μ(x), write the rule with μ(x)” |
| S12 Trading bounds | Fix now | “Fixed share” unnamed; “correct” undefined until late; gross vs net mixed in one sentence; “doubt” slang | Title names `ρκ(π)` and `Δ_T`. Define correct orders first. State net = gross − k |
| S13 Prop. 2 | Polish | Strength order reads back to front; `β < 1/2` vs S11 `β ≤ 1/3` unexplained; (H1)–(H3) glosses use wrong agents (“prior misses c_H”, “purchase clears it”); `b + πλ` unnamed | “Steps F0 (weak), F1 (strong), F2 (very strong)…”. Glosses compare `B` with `c_H`. Name `b + πλ` as purchase probability |
| S14 Cor. 1 | Fix now | See depth section: no conclusion; midpoint misread; fractions | New title + closing sentence + decimals |
| S15 Fixed info | Fix now | See depth section: `S` unmapped; flat rows read as counterexamples | Map `S`; name the mover; label rows; name Prop. 1(a) |
| S16 Research | Fix now | See depth section: success chance, cap, `2k`, L action | All-or-nothing lead-in; CHECK 4–7 |
| S17 Price access | Fix now | Title: `F1`, “visible”, “net” all need recall; drops “target”; three names for one contrast (visible / access / hidden) | “At the strong incumbent (F1), a price the rival can see raises expected target proceeds and surplus net of preparation costs” |
| S18 Purchase impact | Fix now | Title drops “frequency-weighted” and the comparator; `e(1) > ρ` never named as recruitment; no empirical moment; order codes implicit | Weighted title. One line each: price map; recruitment definition; empirical moment (“average the pre-preparation price by order outcome… test the sample analogue”) |
| S19 Conclusion | Fix now | Ends on an S16 detail, not the answer; “recruitment sits in…” is no test; “on an open set” is bookkeeping; drops S4 “can” and uniqueness | Delete the final research line. End on Implication, in the S18 weighted form. Restore “can … unique outcome in each case” |

Frames that already work and must keep their form:
S1 three columns and “cause … not only forecast”;
S2 subtitle (the best fixed-information sentence in the opening);
S3 table and “The decision is rival preparation”;
S4 three-sentence chain order and modal “can”;
S5 `c_H` parenthetical and “Neither bidder trades target shares”;
S7 “outcome X, not who traded” and “One price pools…”;
S8 spread gloss and `μ`-weighted gloss;
S9 liquidity-Bayes sentence and price decomposition;
S12 gloss “holds for every trading plan” (rename to order strategy);
S13 table structure, proof-idea foot line (with anchors added);
S19 LargeLine as the answer to S1.

## Consistency rules to lock before editing

Add these lines to the locked-words header in `slides.tex`
(next to the present list at lines 8–11). Then hold every
surface to them: deck, web copy, script, brief, figure labels.

1. Distribution, never law, for `F, G_j, C, (j, S)`.
   Already fixed upstream. Lock it so it does not return.
2. Rival gross profit for `B(μ)` and `g_j`. Never drop “gross”.
3. Target proceeds. Never “sale proceeds”.
4. Shareholder spread at first use on each frame or page.
   Bare “spread” only after that first use.
5. Pre-preparation information (noun).
   Fixed-information (modifier only).
6. Preparation threshold at first use per frame for `τ`.
7. Belief names: order belief, price belief, top belief,
   band floor. “Posterior” only if the frame defines it as such.
8. Weak / strong / very strong. Never “stronger still”.
9. News in prose. Signal only for `S` on S15 and for the
   rival's private signal in the scope extension.
10. Spelling: choose -ise. `maximise, realised, favourable`.
    One slip today: “maximize” (S9) beside “realised” (S7, S9).
11. Hyphens: modifier takes a hyphen, noun does not.
    “second-price auction”, “fixed-information control”,
    “sale-order impact”, “high-cost rival”.
12. One name for one trading object: order strategy
    (retire order profile, trading plan, candidate outcome
    where they mean the same object on S11–S13).

Title grammar for result frames S10–S18:

- One claim, present tense, locked names in full at first use.
- Weak or strict word present: “weakly”, “can”, “exactly when”.
- Scope in a subtitle, not in a longer title.
  Only S1 and S2 carry subtitles today.
  Give S10, S11, S15, S17, S18 subtitles.
- Aim at 55 characters or fewer. Over the line today:
  S12 (65), S17 (63 plus maths), S14 (59), S11 (56).
  These counts show wrap risk. No render was made in this pass.

## The website brief renames the deck

A cold visitor lands on the brief tab (`docs/index.html`,
source `handout/sections/*`) before any slide.
That surface renames five locked objects:

- “target-payoff spread” for shareholder spread.
- “top/bottom posterior” for top belief / band floor.
- “quality class”, “high-class / low-class” for synergy class.
- “acquisition profit” for rival gross profit.
- “challenger” on figure axes for rival.

It also adds names with no slide counterpart: exclusion bound,
trading bound, high-cost window, two returns to information,
“Competition creates research”, heading “Robustness, welfare
and sale terms” (the deck's `W` is acquisition surplus net of
preparation costs, not welfare).

None of this contradicts a result. All of it breaks the thread
for a reader who moves from brief to talk.
Fix in `handout/sections/*` and the figure code, then rebuild.
Do not edit `docs/index.html` alone.
Order: after the main deck, per your scope for this pass.

Two talk-tab items cost one line each:

- The parts list paraphrases titles while the lead claims
  “the same titles”. Relabel it “Parts of the talk, in short”,
  or quote real titles.
- Keyboard help says “Next step”. The deck has no click builds.
  Write “Next frame / Back”.

One drift to repair in the same rebuild: the script and
`content.js` agree at 28.0 minutes in a 30-minute talk, 57 frames.
`presentation/README.md` and `presentation/DESIGN.md` still say
33.5 minutes, a 45-minute slot, and 56 frames in places.
Nothing checks those prose restatements. That is how they drifted.

## Do not redo: three upstream commits

Local branch `slot-revision` is 3 behind `origin/main`.
Pull before any edit. These items are already fixed there:

- `c6ecb56` — distribution, not law, across paper, slides,
  website, course, script. Skip every law edit in this report.
- `d6267a1` — website rebuild with that wording.
- `12a0df3` — incumbent shown on the S6 timing frame;
  S11 threshold rule in symbols (`B(μ) ≥ c_H ⇔ μ ≥ τ`).
  Do not re-argue S6 incumbent visibility.
  Note: that commit removes the plain-words threshold gloss.
  That change strengthens the case for rule 6 above.

## Seven questions only you can answer

Paste-ready text waits on these. All other fixes need no answer.

- CHECK 1 (S14). In the equivalence, which inputs are free?
  Reading here: only `u`, hence `M`, varies, with `u` in its
  B10 interval. Confirm, so the scope sentence can be written.
- CHECK 2 (S14). Role of `r0`: do the two weak-strength legs
  `B0(π) < c_H` and `Δ0 < k` hold for every `u` in the region?
  If yes, one sentence on S14 can explain why `r0` vanishes.
- CHECK 3 (S15). Promote “Proposition A.2” to the S15 tag?
  Promote the exact-fall formula too? It names the mechanism
  in one line. It adds one object, `μ(S)`.
- CHECK 4 (S16). Route from S12 `K_j > k` to S16 `Δ_T > 2k`.
  Guess here: at `π = 1/2`, doubt at the band floor caps at 1/2.
  Confirm before a gloss is written.
- CHECK 5 (S16). Observability: chosen `λ` unseen,
  only equilibrium `λ̂` enters prices and beliefs?
  The rewrite in the depth section asserts this. Confirm.
- CHECK 6 (S16). Class-L action in the recruiting equilibrium
  of Proposition 4: sells, abstains, or may mix?
  B12 suggests abstention in the example only.
- CHECK 7 (S16). Hold-fixed set for “λ̂ rises strictly with Δ_T”:
  which of `τ, g_H, g_L, F` stay fixed?

## Recommended edit order

1. Pull `origin/main` into `slot-revision`. Re-check S6 and S11.
2. Answer CHECK 1–7 (one line each suffices).
3. Rewrite S14, S15, S16. These three carry the paper's logic:
   example, control, research. Keep every number, key,
   inequality direction, tie rule, and backup link.
4. Fix five titles: S10, S12, S17, S18, plus S11 split.
   Add subtitles for scope where the title would grow.
5. Repair S4 (spread gloss, gross, three strengths, floor).
   This frame feeds S19. Then mirror S4 in S19 and delete
   the final research line on S19.
6. Add bridges on S5–S13: `X = q`; seen price `P̄`;
   generic `μ` vs `μ(x)`; realised vs expected money;
   `b` as one-direction liquidity mass; `b + πλ` as purchase
   probability; correct (H1)–(H3) gloss agents.
7. Run the term ledger across S1–S19 in both files.
   Update script headings and the script where speech
   now contradicts the slide (“hidden price”, “sale impact”).
8. Only then: brief renames in `handout/sections/*`,
   figure axes, talk-tab labels, README/DESIGN counts.
   Rebuild the website. Render the deck. Read every page.
   Check title wraps on the render, not from character counts.

## What this pass did not do

- No slide, web, or script file changed.
- No render. Title-wrap verdicts rest on length.
- Backups B1–B17: term-leak survey only.
- Figure PDFs: labels read from source macros, not from PDFs.
- Paper manuscript: out of scope, unread.
- Numbers: none checked against the registry, none changed.
  Every proposal keeps numbers, cites, and result numbers fixed.


