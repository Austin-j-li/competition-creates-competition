# Model language: literature and timing

Date: 29 October 2026. Scope: discussion and recommendations only.

## Main finding

**Incumbent bidder and potential rival bidder form a defensible pair, with explicit definitions. Neither label alone encodes the preparation asymmetry.**

Incumbent bidder and prospective challenger also work as defined roles. The sources below do not establish either pair as the most standard terminology. The evidence supports several conventions, each with a different emphasis.

My preferred pair is **incumbent bidder / potential rival bidder**. Use **incumbent / rival** after the definitions. This preference reflects clarity and model fit, not a measured frequency advantage. The shorter pair **incumbent / challenger** remains acceptable if continuity with the manuscript matters more.

The key sentence must state that the incumbent is already prepared. It must also state that the rival decides whether to prepare after the stock price. A label cannot replace these facts.

## Current source and exact timing

I read `CLAUDE.md`, `overleaf/README.md`, and the specified local manuscript and slide sources. The local `overleaf/slot` commit was `eaf30496c9a54e42eff65b1c5b96ded51f811f18`. Its status showed an untracked `build/` directory. This note concerns that local snapshot; I did not synchronize the remote.

The decisive source locations are:

| Location under `overleaf/slot/` | Fact relevant to terminology |
|---|---|
| `main.tex:76–86` | The abstract uses incumbent bidder, prospective challenger, preparation, and entry. |
| `sections/01_introduction.tex:11–15` | The challenger decides before any offer is announced. |
| `sections/02_model.tex:11–19` | One buyer is prepared. Preparation includes diligence, finance, approvals, and evaluation capacity. |
| `sections/02_model.tex:51–56` | The incumbent faces no further entry cost. Its public value distribution determines strength. |
| `sections/02_model.tex:58–77` | Class determines a distribution of the rival's value. The structure permits selective entry. |
| `sections/02_model.tex:83–102` | The rival sees the price, then its cost. Preparation reveals value and permits a bid. |
| `sections/02_model.tex:106–134` | The informed investor starts without a net target position and cannot acquire the target. |
| `sections/02_model.tex:163–187` | Market makers see the order. The rival sees price and cost. Entry means preparation. |
| `sections/05_research.tex:3–18` | Investor research reveals class on success. It differs from buyer preparation. |
| `sections/08_empirical.tex:77–79` | The empirical counterpart is substantive diligence or a proposal that requires costly preparation. |
| `slides.tex:228–236, 281–285` | The deck uses first buyer, second buyer, synergy class, and informed investor. |

The baseline sequence is:

1. The incumbent is prepared and faces no further preparation choice.
2. The seller commits to the sale rule and reserve.
3. The informed trader observes the rival's class. The slot selects the trader or a liquidity trader.
4. Market makers observe the order and set the stock price.
5. The rival observes the stock price, then its own preparation cost.
6. The rival decides whether to prepare. Preparation reveals its acquisition value and permits participation in the auction.
7. Prepared buyers submit admissible bids. The auction determines ownership and payments.

The model takes the incumbent's preparation as given. It does not specify or estimate the incumbent's historical expenditure. Sunk preparation is the correct economic distinction, but a positive historical cost is not an explicit primitive.

The rival's cost can be zero. It still occupies the rival role and follows the preparation rule. Thus **costly bidder** and **unprepared bidder** are poor permanent names.

A prepared incumbent can have a value below the reserve. Therefore, incumbent status does not imply an admissible offer or a completed acquisition. Neither buyer trades target shares.

There is a small timing ambiguity in the prose. The model's sequence says that prepared bidders then learn their values (`02_model.tex:169`). Nearby text and the deck give the incumbent its value earlier (`02_model.tex:165`; `slides.tex:228,281`). The preparation asymmetry is clear. A later language revision should state precisely when the incumbent learns its value.

## Primary evidence of usage

These are examples of usage, not a representative terminology survey. Page numbers refer to the linked version. I distinguish full text from indexed passages and abstract-only access.

| Source and location | Exact short quotation | Relevance and limit |
|---|---|---|
| Hirshleifer and Png (1989), *Facilitation of Competing Bids and the Price of a Takeover Target*, abstract, journal pp. 587–606. [Publisher](https://academic.oup.com/rfs/article-abstract/2/4/587/1586915) | “first bidder”; “second bidder”; “incur costs to learn their (independent) valuations” | Direct M&A precedent for ordinal bidder names and costly investigation. The first bid precedes the second buyer's investigation. The current paper lacks that initial bid. Access: publisher abstract and matching author abstract. |
| Fishman (1988), *A Theory of Preemptive Takeover Bidding*, abstract, journal pp. 88–101. [Author's institution](https://www.kellogg.northwestern.edu/academics-research/research/detail/1988/a-theory-of-preemptive-takeover-bidding/) | “acquire costly information after the bidding has begun” | The abstract establishes a crucial timing difference. It does not establish that incumbent/challenger is Fishman's preferred pair. Access: institutional abstract; published full text unavailable through the web tool. |
| Bulow and Klemperer (2009), *Why Do Sellers (Usually) Prefer Auctions?*, author manuscript, Section I, pp. 5–6; Appendix A, p. 36. [Full text](https://www.nuff.ox.ac.uk/Economics/Papers/2009/w5/wdaforweb29jun09.pdf) | “incumbent bidder (that is, the first entrant)” | Clear usage of incumbent bidder. Potential entrants observe earlier bids; the incumbent is the survivor with the current offer. The label can pass to another bidder. This is stronger than sunk preparation alone. |
| Gentry and Stroup, *Entry and Competition in Takeover Auctions*, accepted manuscript dated 12 November 2018, p. 18; published in 2019. [Accepted manuscript](https://researchonline.lse.ac.uk/id/eprint/90604/1/Gentry_Entry-and-competition.pdf) | “the winner becomes the incumbent” | Direct M&A usage. The incumbent is a role in sequential negotiations, after a contest between buyers who entered. Access: indexed primary passage; direct PDF access failed. The same role appears in the accessible 2014 draft, Section VI.A, p. 32. [2014 draft](https://www.aeaweb.org/conference/2015/retrieve.php?pdfid=8445&tk=KaGZd6BA) |
| Gentry and Stroup, 23 December 2014 draft, Section I, pp. 8–9. [Full text](https://www.aeaweb.org/conference/2015/retrieve.php?pdfid=8445&tk=KaGZd6BA) | “potential bidders”; “due diligence” | The authors distinguish possible buyers, formal participation, and investigation of the target. These passages support potential bidder and the link between entry and diligence. The cited pages are from the earlier draft, not the journal version. |
| Roberts and Sweeting (2013), *When Should Sellers Use Auctions?*, abstract; author manuscript dated 9 August 2012, Section 1, p. 3. [Publisher](https://swlb2.aeaweb.org/articles?id=10.1257%2Faer.103.5.1830); [author manuscript](https://econweb.umd.edu/~sweeting/SWEETING_usingauctions.pdf) | “entry is costly and selective”; “After entry, they find out their values for sure” | Supports entry after an informative signal but before exact value knowledge. The empirical application is timber, so this is auction terminology rather than direct M&A evidence. |
| Maskin and Riley (2000), *Asymmetric Auctions*, Section 2, p. 415. [Author's institutional copy](https://scholar.harvard.edu/files/maskin/files/asymmetric_auctions.pdf) | “one buyer as ‘strong’ (s) and the other as ‘weak’ (w)” | Supports distribution-based strength language. Their text links it to stochastic dominance; later results impose stronger restrictions. This does not transfer those results to the current model. Access: indexed primary page; direct PDF fetch timed out. Inner quotation marks are typographic normalization. |
| Gorbenko and Malenko (2014), *Strategic and Financial Bidders in Takeover Auctions*, abstract and introduction, p. 2513. [Author's full text](https://www.mit.edu/~amalenko/stratfin.pdf) | “valuations (maximum willingness to pay)”; “different types of bidders” | Supports valuation language and a warning about type. Here types are strategic versus financial buyers. Those categories do not identify preparation status or high versus low match quality. |
| Edmans, Goldstein, and Jiang (2015), *Feedback Effects, Asymmetric Trading, and the Limits to Arbitrage*, Section I.B, p. 3774. [Author's institutional copy](https://business.columbia.edu/sites/default/files-efs/pubfiles/6040/Jiang_Feedback_effects.pdf) | “The speculator has no initial position in the firm.” | Close precedent for the outside financial actor. The paper uses speculator and outside investor language. Its trade mechanism differs from the current slot mechanism. |
| Glosten and Milgrom (1985), *Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders*, Section 1, p. 71. [Institutional copy](https://pages.stern.nyu.edu/~lpederse/courses/LAP/papers/Information%2CFundamental/GlostenMilgrom85.pdf) | “the economic function of the specialists and the floor traders is that of middlemen” | Specialist can denote an intermediary who holds inventory. It is therefore a risky short name for this paper's informed trader. Access: indexed primary page; direct fetch failed. |

The Australian Takeovers Panel also uses **potential rival bidders** in Guidance Note 7, paragraph 27. Paragraph 26 uses **potential competing bidder** in a due-diligence context. This is primary institutional usage, not evidence of dominance in economics journals. [Guidance Note 7, paragraphs 26–27](https://takeovers.gov.au/guidance-notes/gn7).

The inspected academic sources provide stronger direct support for incumbent, potential bidder, potential entrant, and first/second bidder than for the exact phrase prospective challenger. I did not verify that exact phrase in matching primary M&A theory here. That result does not establish that the phrase is absent from the literature.

## Actor labels and semantic traps

| Candidate | Assessment against this model |
|---|---|
| **Incumbent bidder** | Acceptable with a definition tied to completed preparation. Readers may infer an existing offer, prior ownership, or product-market incumbency. None follows here. |
| **Prospective challenger** | Clear about optional participation after definition. Challenger alone can suggest an active competing offer. Neither word states whether diligence is complete. |
| **Potential rival bidder** | My preferred second label. Potential preserves the entry margin; bidder locates the rivalry in the sale. The phrase still needs a preparation definition. |
| **Potential entrant** | Established auction language. Use only after entry into this sale process is defined. Bare entrant can suggest product-market entry. |
| **First bidder / second bidder** | Direct precedent in takeover theory. Here first must mean first prepared, since the model does not order initial public offers. |
| **First buyer / second buyer** | Understandable ordinal labels. They do not imply two completed acquisitions, but they hide the economic asymmetry without a definition. |
| **Initial bidder / initiating bidder** | Avoid as the default. These labels imply an initial offer or an act that starts the sale. The model also allows a public strategic review. |
| **Prepared bidder / potential bidder** | Very precise at the initial node. Less suitable as permanent names, since the rival can become prepared too. |
| **Informed bidder / uninformed bidder** | Avoid as actor names. The rival can learn from price and then learn its value through preparation. The informed trader is a separate actor. |

The two proposed pairs accurately describe the model only through their definitions. They are not technical codes for sunk cost versus optional cost. In particular, public knowledge of a prepared buyer differs from a public standing bid.

## Recommended vocabulary and first use

The following sentences are proposals for discussion. They are not edits to the manuscript or deck.

| Object | Preferred term | Proposed first-use definition |
|---|---|---|
| Prepared buyer | **Incumbent bidder**, then incumbent | The incumbent bidder completed preparation before the model begins. Its preparation costs are sunk, and it faces no further preparation choice. |
| Buyer with the entry choice | **Potential rival bidder**, then rival | The potential rival bidder observes the target's stock price before it decides whether to prepare. Preparation reveals its acquisition value and permits a bid. |
| Real decision | **Entry**, with preparation as its meaning | Entry means the decision to incur the preparation cost and become eligible to bid. Preparation includes due diligence and the other requirements for an executable offer. |
| Cost | **Preparation cost**, also entry cost after definition | Preparation cost becomes sunk when the buyer incurs it. It can be zero. |
| Comparative static | **Incumbent strength** | A stronger incumbent has an acquisition-value distribution that dominates the original distribution in the first-order stochastic sense. |
| Monetary private value | **Acquisition value**, or valuation at first use | Acquisition value is the buyer's maximum willingness to pay for the target, per share. |
| Financial actor | **Informed trader** | An outside informed trader observes the rival's synergy type and trades target shares. It has no initial net position or control rights. It cannot acquire the target. |
| Economic interpretation | **Sector specialist**, within the trader's description | The informed trader can represent an investor with expertise in the target's sector. |
| Latent class | **Synergy type**, explicitly latent at first use | The rival's latent synergy type determines the distribution of its acquisition value. The informed trader observes this type; the rival initially does not. |
| Trader's costly action | **Information acquisition**, then research | The trader chooses research intensity before it learns the synergy type. Successful research reveals the type. |

### Entry and due diligence

Use **entry** freely in theory after its first definition. It connects the mechanism to the auction literature. Use **preparation** when the text explains the actual decision. Use **due diligence** for the investigative component and its empirical proxy.

Do not define entry as a public bid, a win, or a completed acquisition. In the baseline, class supports lie above the reserve, so a prepared rival bids. The reserve extension can separate preparation from an admissible bid (`02_model.tex:75,99`). The definition should survive that extension.

Preparation is broader than due diligence in the current manuscript. A global replacement of preparation with due diligence would omit finance, approvals, and capacity. Likewise, buyer preparation and trader research are separate information-acquisition decisions with different payoffs.

### Strength and valuation

Retain **strength** as a defined shorthand. State the distributional comparison at first use:

\[
\widetilde F(y)\le F(y)\qquad\text{for every }y.
\]

This comparison concerns the public distribution of incumbent value. It does not mean a higher announced offer, larger balance sheet, greater market power, or more aggressive bids at the same value. A higher mean alone does not establish the stipulated order.

Keep **acquisition value** distinct from the **auction payment** and **acquisition profit**. Value is willingness to pay. Profit deducts the auction payment, and net profit also deducts preparation cost.

### Trader and specialist

**Informed investor** is also accurate and appears in the current deck. My preference for informed trader identifies the economic action and separates this actor from either acquirer. **Informed speculator** has close precedent, but it need not replace a clear trader label.

Use sector specialist only as an institutional explanation. Avoid the standalone names specialist and fund. They can confuse the informed trader with a market intermediary or a financial acquirer. Also avoid activist, arbitrageur, or insider unless the text defines the added implications.

### Synergy class and type

**Synergy type** uses familiar economic vocabulary, but it requires the latent qualification. The variable is initially unknown to the rival. It is not the rival's observed private information before preparation.

The current **synergy class** is mathematically accurate and can remain. It usefully distinguishes the distribution index from the realized value. I found no evidence that synergy class is a universal M&A term, or that type must replace it.

If the author prefers type, use **high-synergy type / low-synergy type** throughout both documents. Define the ranking through the conditional value distributions:

\[
\theta\mid j\sim G_j,\qquad G_H(y)\le G_L(y)\quad\text{for every }y.
\]

This ranking does not mean that every high-type realization exceeds every low-type realization. In the general model, the trader knows the distribution class, not the exact value. Exact class knowledge reveals exact value only in the special case with one value per class.

High and low are relative labels. **Good/poor synergy** can imply an absolute welfare judgment that the distributional ranking does not establish. **Quality class** can also sound like a ranking of management quality. Synergy locates the heterogeneity in the acquisition match.

The formal model specifies acquisition values rather than a separate accounting measure of merger synergies. Thus synergy type is an economic interpretation of the latent state. It should not imply a specific cost-saving or revenue formula absent from the model.

## Paper and deck alignment

Use the same permanent actor names in both documents. Introduce the slide labels once as incumbent bidder (already prepared) and potential rival bidder (preparation remains optional). Subsequent slides can use incumbent and rival.

If the author retains challenger, use incumbent bidder and potential challenger at first use in both documents. State the same preparation distinction. There is no substantive reason to change a well-defined challenger solely to claim greater disciplinary conformity.

The model overview should define entry, strength, the trader, and the latent synergy variable before the first result. A one-line mapping can bridge the current deck: first buyer means incumbent; second buyer means potential rival.

The highest-priority issue is **price versus bid**. The rival learns from a target stock price before the auction. It does not infer the incumbent's value from an initial takeover offer. That timing difference distinguishes this mechanism from the closest preemptive-bid models.

## Limits and disposition

This note establishes usage in selected primary sources. It does not rank phrase frequencies across the discipline. The exact pair incumbent bidder / prospective challenger remains a defensible local convention, not a verified universal standard.

Some sources were accessible only as abstracts or indexed primary passages. Those limits appear beside the relevant evidence. Draft page references do not claim to match journal pagination. The note does not import empirical estimates or legal conclusions from those sources.

I wrote only this note. I did not edit the paper, deck, website, or canonical instructions. I did not download outside files, create tests, or run tests. I checked the note against the local source passages and the cited web evidence.
