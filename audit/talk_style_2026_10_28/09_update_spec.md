# Update spec — handout on Overleaf, no biotech setup (28 October 2026)

Amends `08_project_spec.md`. Everything not named here stays as built (Overleaf 7b397b7).

## 1. Two versions of the deck

| Where | Version | Builds |
|---|---|---|
| Overleaf (`slides.tex`) | Handout: one page per slide | None. Each slide shows its final state |
| Website (`/talk/`) | Talk version | Click builds, in the order of the "Builds" lines in `SLIDEPACK_30_SLIDES.md` |

Overleaf:
- `slides.tex` gets the Beamer class option `handout`.
- The click markup (`<2->`, `\only<…>`, `\onslide<…>`) is removed, so the source reads as plain frames. Slide 8 keeps
  the number line after the move; slide 9 keeps the threshold mark; slide 10 shows all three columns.
- Result: about 48 pages (title, 16 main slides, 31 backup pages), down from 106.
- The header comment and `START_HERE.txt` say that the Overleaf deck is the handout and the website carries the
  click builds.

Website: built later from the author's edited Overleaf text, in the existing ruled design, with the click order from
the slide text. No change to that plan.

## 2. Setup without the biotech story

The talk keeps a specific informed investor, in the paper's own words (§2.3: "an outside sector specialist, such as
a sector-focused long-short fund … its own research on the target's customers, technology, and demand").

| Slide | Now | New (draft; final wording by the slide writer) |
|---|---|---|
| 3 | Listed biotech company for sale. One late-stage drug. / Second drug company decides: open the data room, or stay out. | A listed company is for sale. One buyer is ready. / The stock still trades. One order comes first. / The second buyer decides: pay for diligence, or stay out. |
| 4 | First buyer: large drug company, diligence done · Second buyer: second drug company · Informed investor: long-short biotech fund · Liquidity trader: index flows | First buyer: diligence done · Second buyer: diligence not yet paid · Informed investor: a long-short sector fund · Liquidity trader: index and fund flows |
| 5 | Good synergy: the drug fills a portfolio gap. Poor synergy: the drug overlaps with drugs the second buyer already sells. | Good synergy: the target's business complements the second buyer's. Poor synergy: it overlaps with what the second buyer already has. |
| B2 | Long-short biotech fund: public portfolio gaps plus own drug research … | Long-short sector fund: what the second buyer already owns is public; how the target's products and customers perform is the fund's own research. Together they show good or poor synergy. It holds no stake before it trades. |
| Script | Biotech story on slides 1, 3, 4, 5, 14 and in the first prepared answer | Same points, generic: a listed company, a ready buyer, a second buyer, a sector fund that follows the target's customers and technology |

Slide 1 opening story (speech): "A listed company announces that it is open to a sale. One buyer has done its
homework. A second buyer must decide whether to pay for months of diligence. Meanwhile the stock trades, and a
sector fund that follows the company's customers trades it too."

## 3. Team and order

1. Slide lines for 3, 4, 5 and B2: Muse Wonder Full.
2. Script update: GPT-6 Astra, fast tier.
3. Lead session: apply both to `slides.tex`, switch to handout, compile, view every page, push to Overleaf.
   Rollback: 7b397b7 (30-minute deck with builds) and 783591e (45-minute deck).

## 4. Open choices

- Informed investor: "a long-short sector fund" (recommended, the paper's words) or keep "long-short biotech fund"
  for the investor only.
- Click markup: remove from the Overleaf source (recommended) or keep it and compile as a handout.
- Same pass: remove the old status subtitles ("General result", "Example only") from the reused backups B3–B15
  (recommended, per the standing rule).
